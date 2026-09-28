<?php

namespace App\Services;

use App\Enums\BranchKind;
use App\Enums\NodeType;
use App\Exceptions\TreeEditRefused;
use App\Models\Branch;
use App\Models\Course;
use App\Models\Currency;
use App\Models\EnrollmentRequest;
use App\Models\Node;
use App\Models\NodeResource;
use App\Models\Practice;
use App\Support\Reorder;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

/**
 * Arma y edita el árbol de un curso desde el admin. Todo lo que se llevaría
 * el historial de un alumno (abrir, entregar, pagar) se rechaza con un mensaje.
 */
class TreeEditor
{
    /** Crea el curso con su moneda y su nodo raíz ("clase 0"). */
    public function createCourse(array $data): Course
    {
        return DB::transaction(function () use ($data) {
            $course = Course::create($data);
            Currency::forCourse($course);

            Node::create([
                'course_id' => $course->id,
                'type' => NodeType::Root,
                'title' => 'Clase 0',
                'price' => $course->root_price,
                'position' => 0,
            ]);

            return $course;
        });
    }

    /** El raíz cuesta lo mismo que las monedas que se acreditan al aprobar el pago. */
    public function updateCourse(Course $course, array $data): Course
    {
        $wasPublished = $course->is_published;

        DB::transaction(function () use ($course, $data) {
            $course->update($data);
            $course->nodes()->where('type', NodeType::Root)->update(['price' => $course->root_price]);
        });

        // Quienes pidieron "Avisame cuando salga" se enteran al publicarlo.
        if (! $wasPublished && $course->is_published) {
            app(CourseCatalog::class)->announceRelease($course);
        }

        return $course;
    }

    public function deleteCourse(Course $course): void
    {
        $hasStudents = $course->subscriptions()->exists()
            || EnrollmentRequest::where('course_id', $course->id)->exists()
            || $course->nodes()->whereHas('unlocks')->exists();

        if ($hasStudents) {
            throw new TreeEditRefused('El curso ya tiene alumnos: no se puede borrar. Despublicalo para ocultarlo.');
        }

        DB::transaction(function () use ($course) {
            $files = NodeResource::whereIn('node_id', $course->nodes()->select('id'))->pluck('file_path')->filter();
            Storage::disk('local')->delete($files->all());
            Storage::disk('public')->delete(array_filter([$course->logo, $course->cover]));

            $course->nodes()->update(['parent_id' => null]);
            $course->delete();
        });
    }

    public function createBranch(Course $course, string $title, BranchKind|bool $kind = BranchKind::Trunk): Branch
    {
        if (is_bool($kind)) {
            $kind = $kind ? BranchKind::Extra : BranchKind::Trunk;
        }

        return $course->branches()->create([
            'title' => $title,
            'kind' => $kind,
            'position' => Reorder::next($course->branches()),
        ]);
    }

    /**
     * Requisitos extra de un nodo (además del padre): nodos del mismo curso que no dependan de él.
     *
     * @param  list<int>  $requiredIds
     */
    public function setRequirements(Node $node, array $requiredIds): void
    {
        $requiredIds = array_values(array_unique(array_map('intval', $requiredIds)));
        if ($node->isRoot() && $requiredIds !== []) {
            throw new TreeEditRefused('El nodo raíz no tiene requisitos.');
        }

        $allowed = $this->allowedParents($node->course, $node)->pluck('id');
        $invalid = array_diff($requiredIds, $allowed->all());
        if ($invalid !== []) {
            throw new TreeEditRefused('Un requisito no puede ser el mismo nodo ni uno que dependa de él (formaría un ciclo).');
        }

        // El padre ya es requisito: no se repite.
        $node->requirements()->sync(array_values(array_diff($requiredIds, [$node->parent_id])));
    }

    public function deleteBranch(Branch $branch): void
    {
        if ($branch->nodes()->exists()) {
            throw new TreeEditRefused('La rama tiene nodos: movelos a otra rama o borralos primero.');
        }

        $branch->delete();
    }

    public function createNode(Course $course, array $data): Node
    {
        $type = NodeType::from($data['type'] instanceof NodeType ? $data['type']->value : $data['type']);
        if ($type === NodeType::Root) {
            throw new TreeEditRefused('Cada curso tiene un solo nodo raíz.');
        }

        $this->assertValidParent($course, null, $data['parent_id'] ?? null);

        return Node::create([
            ...$data,
            'course_id' => $course->id,
            'position' => Reorder::next(Node::where('course_id', $course->id)->where('branch_id', $data['branch_id'] ?? null)),
        ]);
    }

    public function updateNode(Node $node, array $data): Node
    {
        if ($node->isRoot()) {
            // El raíz no cuelga de nada, no va en una rama y su precio sale del curso.
            unset($data['type'], $data['parent_id'], $data['branch_id'], $data['price'], $data['price_currency_id']);
        } else {
            if (isset($data['type']) && NodeType::from($data['type'] instanceof NodeType ? $data['type']->value : $data['type']) === NodeType::Root) {
                throw new TreeEditRefused('Cada curso tiene un solo nodo raíz.');
            }
            $this->assertValidParent($node->course, $node, $data['parent_id'] ?? $node->parent_id);
        }

        $node->update($data);

        return $node;
    }

    public function deleteNode(Node $node): void
    {
        if ($node->isRoot()) {
            throw new TreeEditRefused('El nodo raíz no se borra: es la entrada al curso.');
        }
        if ($node->children()->exists()) {
            throw new TreeEditRefused('Otros nodos dependen de este: cambiales el requisito antes de borrarlo.');
        }
        if ($node->hasStudentActivity()) {
            throw new TreeEditRefused('Algún alumno ya abrió este nodo o entregó una hoja: despublicalo en lugar de borrarlo.');
        }

        DB::transaction(function () use ($node) {
            Storage::disk('local')->delete($node->resources()->pluck('file_path')->filter()->all());
            $node->delete();
        });
    }

    /** Copia el nodo con sus hojas y recursos, sin publicar, al lado del original. */
    public function duplicateNode(Node $node): Node
    {
        if ($node->isRoot()) {
            throw new TreeEditRefused('El nodo raíz no se duplica.');
        }

        return DB::transaction(function () use ($node) {
            $copy = $node->replicate(['position', 'code']);
            $copy->title = Str::limit($node->title.' (copia)', 255, '');
            $copy->is_published = false;
            $copy->position = Reorder::next(Node::where('course_id', $node->course_id)->where('branch_id', $node->branch_id));
            $copy->save();

            $copy->requirements()->sync($node->requirements()->pluck('nodes.id'));

            foreach ($node->practices as $practice) {
                $copy->practices()->create($practice->only($practice->getFillable()));
            }

            foreach ($node->resources as $resource) {
                $data = $resource->only($resource->getFillable());
                if ($resource->file_path) {
                    $data['file_path'] = 'resources/'.Str::uuid().'.'.pathinfo($resource->file_path, PATHINFO_EXTENSION);
                    Storage::disk('local')->copy($resource->file_path, $data['file_path']);
                }
                $copy->resources()->create($data);
            }

            return $copy;
        });
    }

    public function createPractice(Node $node, array $data): Practice
    {
        return $node->practices()->create([
            ...$data,
            'position' => Reorder::next($node->practices()),
        ]);
    }

    public function deletePractice(Practice $practice): void
    {
        if ($practice->hasStudentActivity()) {
            throw new TreeEditRefused('Esta hoja ya tiene entregas o marcas de alumnos: no se puede borrar.');
        }
        if ($practice->is_required && $this->isLastRequired($practice)) {
            throw new TreeEditRefused(self::LAST_REQUIRED);
        }

        $practice->delete();
    }

    /** Pasar una hoja de obligatoria a optativa: no puede dejar a un nodo publicado sin obligatorias. */
    public function assertCanBeOptional(Practice $practice): void
    {
        if ($practice->is_required && $this->isLastRequired($practice)) {
            throw new TreeEditRefused(self::LAST_REQUIRED);
        }
    }

    /**
     * Todo nodo publicado tiene al menos una práctica obligatoria: un nodo sin hojas no se puede
     * ganar ni completar.
     */
    public function assertPublishable(Node $node): void
    {
        if (! $node->practices()->where('is_required', true)->exists()) {
            throw new TreeEditRefused('Para publicarlo, el nodo necesita al menos una '.term('practice', $node->course).' obligatoria.');
        }
    }

    private const LAST_REQUIRED = 'Es la única práctica obligatoria de un nodo publicado: agregá otra o despublicá el nodo primero.';

    private function isLastRequired(Practice $practice): bool
    {
        $node = $practice->node;

        return $node->is_published
            && ! $node->practices()->where('is_required', true)->whereKeyNot($practice->id)->exists();
    }

    public function deleteResource(NodeResource $resource): void
    {
        if ($resource->file_path) {
            Storage::disk('local')->delete($resource->file_path);
        }

        $resource->delete();
    }

    /**
     * Nodos que pueden ser requisito de $node: del mismo curso, sin él mismo ni
     * los que dependen de él (evita ciclos).
     *
     * @return Collection<int, Node>
     */
    public function allowedParents(Course $course, ?Node $node = null): Collection
    {
        $excluded = $node ? [$node->id, ...$this->descendantIds($node)] : [];

        return $course->nodes()
            ->whereNotIn('id', $excluded)
            ->orderByRaw("type = 'root' desc")
            ->orderBy('branch_id')
            ->orderBy('position')
            ->get();
    }

    /**
     * Los que dependen de $node, directa o indirectamente: por padre o por requisito extra.
     *
     * @return list<int>
     */
    public function descendantIds(Node $node): array
    {
        $ids = [];
        $frontier = [$node->id];

        while ($frontier !== []) {
            $children = Node::whereIn('parent_id', $frontier)->pluck('id');
            $dependents = DB::table('node_requirements')->whereIn('required_node_id', $frontier)->pluck('node_id');
            $frontier = $children->merge($dependents)->unique()->diff([...$ids, $node->id])->values()->all();
            $ids = [...$ids, ...$frontier];
        }

        return $ids;
    }

    private function assertValidParent(Course $course, ?Node $node, ?int $parentId): void
    {
        if ($parentId === null) {
            throw new TreeEditRefused('Elegí de qué nodo depende (su requisito).');
        }

        $valid = $this->allowedParents($course, $node)->contains('id', $parentId);
        if (! $valid) {
            throw new TreeEditRefused('Ese requisito no es válido: tiene que ser otro nodo del curso que no dependa de este.');
        }
    }
}
