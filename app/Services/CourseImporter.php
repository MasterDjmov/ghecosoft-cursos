<?php

namespace App\Services;

use App\Enums\Language;
use App\Enums\NodeType;
use App\Enums\PracticeEnvironment;
use App\Enums\SubmissionMode;
use App\Models\Badge;
use App\Models\Branch;
use App\Models\Course;
use App\Models\Currency;
use App\Models\GlossaryTerm;
use App\Models\Node;
use App\Models\Practice;
use App\Support\CourseImport\CourseFileParser;
use App\Support\CourseImport\ImportReport;
use App\Support\Glossary;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;
use Throwable;

/**
 * Importa un curso completo desde el formato de docs/FORMATO-CURSO.md (Fase 7).
 *
 * - Todo va en una transacción: con un error no se guarda nada. En modo "revisar" se deshace
 *   al final, así el informe dice exactamente qué pasaría.
 * - Actualiza por código (R01, R01-N02, R01-N02-M1): reimportar no duplica ni borra, y el
 *   progreso de los alumnos (aperturas, entregas, movimientos) queda intacto.
 * - Lo que está en la base y no en el archivo no se toca: solo se avisa.
 */
class CourseImporter
{
    /** Claves del diccionario que valen para toda la plataforma (el resto va al curso). */
    private const GENERAL_KEYS = ['world.name', 'hero.name', 'coin.wildcard', 'xp', 'xp.short', 'level'];

    private const GENERAL_PREFIXES = ['level.', 'companion.', 'state.'];

    private const NODE_TYPES = [
        'raiz' => NodeType::Root, 'tema' => NodeType::Topic, 'jefe' => NodeType::Boss, 'extra' => NodeType::Extra,
        'ventana' => NodeType::Topic, 'senda' => NodeType::Topic,
    ];

    private const MODES = [
        'codigo' => SubmissionMode::Code, 'archivo' => SubmissionMode::File, 'ambos' => SubmissionMode::Both,
        'codigo y archivo' => SubmissionMode::Both, 'ninguna' => SubmissionMode::None, 'sin entrega' => SubmissionMode::None,
    ];

    private ImportReport $report;

    private Course $course;

    /** @param  list<array{name: string, content: string}>  $files */
    public function import(array $files, bool $dryRun = true): ImportReport
    {
        $this->report = new ImportReport;
        $data = (new CourseFileParser)->parse($files, $this->report);
        $this->validate($data);

        if (! $this->report->ok()) {
            return $this->report;
        }

        DB::beginTransaction();
        try {
            $this->apply($data);
        } catch (Throwable $e) {
            DB::rollBack();
            report($e);
            $this->report->error('No se pudo importar: '.$e->getMessage());

            return $this->report;
        }

        if ($dryRun || ! $this->report->ok()) {
            DB::rollBack();
            $dryRun && $this->report->ok() && $this->report->note('Revisión: no se guardó nada. Si está bien, importalo.');
        } else {
            DB::commit();
            Glossary::flush(null);
            Glossary::flush($this->course->id);
            $this->report->courseUrl = route('admin.courses.tree', $this->course);
        }

        return $this->report;
    }

    /** Errores que se ven sin tocar la base. */
    private function validate(array $data): void
    {
        $meta = $data['course']['meta'];
        foreach (['slug', 'titulo', 'lenguaje'] as $key) {
            if (blank($meta[$key] ?? null)) {
                $this->report->error("Falta «{$key}» en el bloque meta de # CURSO.");
            }
        }
        if (filled($meta['slug'] ?? null) && ! preg_match('/^[a-z0-9]+(-[a-z0-9]+)*$/', $meta['slug'])) {
            $this->report->error('El slug del curso va en minúsculas y con guiones: «python» o «python-desde-cero».');
        }
        if (filled($meta['lenguaje'] ?? null) && ! Language::tryFrom(Str::lower($meta['lenguaje']))) {
            $this->report->error("Lenguaje «{$meta['lenguaje']}» desconocido. Valores: ".collect(Language::cases())->pluck('value')->implode(', ').'.');
        }

        if ($data['nodes'] === []) {
            $this->report->error('El archivo no tiene nodos (## R01-N01 · Título).');

            return;
        }

        $codes = [];
        $roots = 0;
        foreach ($data['nodes'] as $node) {
            $where = $node['where'];
            if (isset($codes[$node['code']])) {
                $this->report->error("{$where}: el nodo {$node['code']} está repetido.");
            }
            $codes[$node['code']] = true;

            $type = Str::lower(CourseFileParser::normalize($node['meta']['tipo'] ?? 'tema'));
            if (! isset(self::NODE_TYPES[$type])) {
                $this->report->error("{$where}: tipo «{$node['meta']['tipo']}» desconocido (raiz, tema, jefe, extra, ventana).");
            }
            $roots += $type === 'raiz' ? 1 : 0;

            $practiceCodes = [];
            foreach ($node['practices'] as $practice) {
                if (isset($practiceCodes[$practice['code']])) {
                    $this->report->error("{$practice['where']}: la práctica {$practice['code']} está repetida en el nodo.");
                }
                $practiceCodes[$practice['code']] = true;

                $mode = CourseFileParser::normalize($practice['meta']['entrega'] ?? 'codigo');
                if (! isset(self::MODES[$mode])) {
                    $this->report->error("{$practice['where']}: entrega «{$practice['meta']['entrega']}» desconocida (codigo, archivo, ambos, ninguna).");
                }
                $environment = CourseFileParser::normalize($practice['meta']['entorno'] ?? 'navegador');
                if (! in_array($environment, ['navegador', 'local'], true)) {
                    $this->report->error("{$practice['where']}: entorno «{$practice['meta']['entorno']}» desconocido (navegador o local).");
                }
            }
        }

        if ($roots !== 1) {
            $this->report->error("El curso tiene que tener exactamente un nodo con «tipo: raiz» (hay {$roots}).");
        }
    }

    private function apply(array $data): void
    {
        $this->course = $this->applyCourse($data['course']);
        $this->report->courseTitle = $this->course->title;
        Currency::forCourse($this->course);

        $this->applyGlossary($data['glossary']);
        $branches = $this->applyBranches($data['branches']);
        $nodes = $this->applyNodes($data['nodes'], $branches);
        $this->applyParents($data['nodes'], $nodes);
        $this->checkCycles();
        $this->checkEconomy($data['nodes'], $nodes);
        $this->reportLeftovers($data, $nodes);
    }

    private function applyCourse(array $course): Course
    {
        $meta = $course['meta'];
        $model = Course::firstOrNew(['slug' => $meta['slug']]);
        $model->fill(array_filter([
            'title' => $meta['titulo'] ?? null,
            'short_description' => $meta['descripcion_corta'] ?? null,
            'description' => $course['description'] ?: null,
            'language' => Str::lower($meta['lenguaje']),
            'root_price' => isset($meta['precio_raiz']) ? (int) $meta['precio_raiz'] : null,
            'subscription_days' => isset($meta['dias_abono']) ? (int) $meta['dias_abono'] : null,
        ], fn ($value) => $value !== null));

        // "publicado" vale solo al crear: después se publica u oculta desde el admin.
        if (! $model->exists) {
            $model->is_published = self::yes($meta['publicado'] ?? 'no');
            $model->position = (int) Course::max('position') + 1;
        }
        $this->save('curso', $model);

        return $model;
    }

    private function applyGlossary(array $rows): void
    {
        foreach ($rows as $row) {
            if (! preg_match('/^[a-z0-9_]+(\.[a-z0-9_]+)*$/', $row['key'])) {
                $this->report->warning("{$row['where']}: clave «{$row['key']}» inválida (minúsculas y puntos); se ignora.");

                continue;
            }
            $general = match ($row['scope']) {
                'general', 'plataforma' => true,
                'curso' => false,
                default => in_array($row['key'], self::GENERAL_KEYS, true) || Str::startsWith($row['key'], self::GENERAL_PREFIXES),
            };
            $gender = match (CourseFileParser::normalize($row['gender'])) {
                'f', 'femenino' => 'f',
                'm', 'masculino', '' => 'm',
                default => null,
            };
            if ($gender === null) {
                $this->report->warning("{$row['where']}: género «{$row['gender']}» desconocido (f o m); se usa m.");
                $gender = 'm';
            }

            $term = GlossaryTerm::firstOrNew(['key' => $row['key'], 'course_id' => $general ? null : $this->course->id]);
            $term->fill([
                'singular' => Str::limit($row['singular'], 255, ''),
                'plural' => $row['plural'] !== '' ? Str::limit($row['plural'], 255, '') : null,
                'gender' => $gender,
                'short_description' => $row['short_description'] !== '' ? Str::limit($row['short_description'], 255, '') : null,
                'lore' => $row['lore'] !== '' ? str_replace('<br>', "\n", $row['lore']) : null,
            ]);
            $this->save('diccionario', $term);
        }
    }

    /** @return array<string, Branch> código → rama */
    private function applyBranches(array $branches): array
    {
        $result = Branch::where('course_id', $this->course->id)->whereNotNull('code')->get()->keyBy('code')->all();

        foreach ($branches as $code => $branch) {
            $kind = CourseFileParser::normalize($branch['meta']['tipo'] ?? 'tronco');
            if ($kind === 'senda') {
                $this->report->warning("Rama {$code}: las Sendas llegan en la Fase 8; por ahora se guarda como rama optativa (extra).");
            }
            $model = $result[$code] ?? new Branch(['course_id' => $this->course->id, 'code' => $code]);
            $model->fill([
                'title' => $branch['title'],
                'position' => (int) ($branch['meta']['posicion'] ?? $branch['order']),
                'is_extra' => in_array($kind, ['extra', 'senda'], true),
            ]);
            $this->save('ramas', $model);
            $result[$code] = $model;
        }

        return $result;
    }

    /** @return array<string, Node> código → nodo */
    private function applyNodes(array $nodes, array $branches): array
    {
        $existing = Node::where('course_id', $this->course->id)->whereNotNull('code')->get()->keyBy('code');
        $wildcard = Currency::wildcard();
        $positions = [];
        $result = [];

        foreach ($nodes as $node) {
            $meta = $node['meta'];
            $where = $node['where'];
            $typeKey = CourseFileParser::normalize($meta['tipo'] ?? 'tema');
            $type = self::NODE_TYPES[$typeKey];
            if (in_array($typeKey, ['ventana', 'senda'], true)) {
                $this->report->warning("{$where}: el tipo «{$typeKey}» llega en la Fase 8; por ahora se guarda como tema.");
            }

            $model = $existing[$node['code']] ?? null;
            if ($model === null && $type === NodeType::Root) {
                // El raíz que ya existía (por ejemplo, el del curso demo) adopta el código.
                $model = Node::where('course_id', $this->course->id)->where('type', NodeType::Root)->first();
            }
            if ($model && $model->isRoot() !== ($type === NodeType::Root)) {
                $this->report->error("{$where}: el nodo {$node['code']} no puede pasar de raíz a otro tipo ni al revés.");

                continue;
            }
            $model ??= new Node(['course_id' => $this->course->id]);

            $branchCode = Str::upper($meta['rama'] ?? $node['branch'] ?? '');
            if ($type === NodeType::Root && $branchCode !== '') {
                $this->report->warning("{$where}: el raíz no va en una rama (ponelo antes de la primera # RAMA); se ignora la rama.");
            }
            $branch = null;
            if ($type !== NodeType::Root && $branchCode !== '') {
                $branch = $branches[$branchCode] ?? null;
                if (! $branch) {
                    $this->report->error("{$where}: la rama {$branchCode} no existe.");

                    continue;
                }
            }

            $currency = CourseFileParser::normalize($meta['moneda'] ?? 'curso');
            if ($currency === 'comodin' && $type !== NodeType::Extra) {
                $this->report->warning("{$where}: solo los nodos extra se pagan con comodines (hasta la Fase 8); se cobra en la moneda del curso.");
            }
            if (filled($meta['requiere'] ?? null)) {
                $this->report->warning("{$where}: «requiere» (requisitos múltiples) llega en la Fase 8; por ahora solo cuenta «padre».");
            }

            $beast = $meta['criatura'] ?? null;
            if (filled($beast)) {
                $beast = Str::startsWith($beast, 'beast.') ? Str::lower($beast) : 'beast.'.Str::slug($beast, '_');
            }

            $fields = $node['fields'];
            $positionKey = $branch?->id ?? 0;
            $model->fill([
                'code' => $node['code'],
                'title' => Str::limit($node['title'], 255, ''),
                'type' => $type,
                'branch_id' => $branch?->id,
                'position' => $type === NodeType::Root ? 0 : ($positions[$positionKey] = ($positions[$positionKey] ?? 0) + 1),
                'price' => $type === NodeType::Root ? $this->course->root_price : (int) ($meta['precio'] ?? ($model->exists ? $model->price : 10)),
                'price_currency_id' => $type === NodeType::Extra && $currency === 'comodin' ? $wildcard->id : null,
                'video_url' => $meta['video'] ?? null,
                'chronicle' => $fields['chronicle'] ?? null,
                'objectives' => $fields['objectives'] ?? null,
                'before_you_start' => $fields['before_you_start'] ?? null,
                'content' => $fields['content'] ?? null,
                'example_code' => $fields['example_code'] ?? null,
                'example_language' => filled($fields['example_code'] ?? null) ? $this->course->language->value : null,
                'sample_input' => $fields['sample_input'] ?? null,
                'expected_output' => $fields['expected_output'] ?? null,
                'use_cases' => $fields['use_cases'] ?? null,
                'common_errors' => $fields['common_errors'] ?? null,
                'beast_key' => $beast ?: null,
                'self_check' => $node['self_check'] ?: null,
                'teacher_solutions' => $fields['teacher_solutions'] ?? null,
            ]);
            // Un nodo nuevo se publica salvo que diga lo contrario; uno existente cambia solo si el archivo lo dice.
            if (isset($meta['publicado']) || ! $model->exists) {
                $model->is_published = self::yes($meta['publicado'] ?? 'si');
            }
            if ($type === NodeType::Root) {
                $model->parent_id = null;
            }
            $model->badge_id = $type === NodeType::Boss ? $this->badgeFor($node) : null;
            $this->save('nodos', $model);
            $result[$node['code']] = $model;

            $this->applyPractices($model, $node);
        }

        return $result;
    }

    private function badgeFor(array $node): ?int
    {
        $name = $node['meta']['insignia'] ?? null;
        if (blank($name)) {
            $this->report->warning("{$node['where']}: el jefe {$node['code']} no tiene «insignia».");

            return null;
        }
        $badge = Badge::firstOrNew(['code' => Str::slug($this->course->slug.'-'.$node['code'], '_')]);
        $badge->fill([
            'course_id' => $this->course->id,
            'name' => Str::limit($name, 255, ''),
            'description' => filled($node['meta']['insignia_descripcion'] ?? null) ? Str::limit($node['meta']['insignia_descripcion'], 255, '') : null,
        ]);
        $this->save('insignias', $badge);

        return $badge->id;
    }

    private function applyPractices(Node $node, array $data): void
    {
        $existing = $node->exists ? Practice::where('node_id', $node->id)->whereNotNull('code')->get()->keyBy('code') : collect();

        foreach ($data['practices'] as $index => $practice) {
            $meta = $practice['meta'];
            $fields = $practice['fields'];
            $mode = self::MODES[CourseFileParser::normalize($meta['entrega'] ?? 'codigo')];
            $required = isset($meta['obligatoria']) ? self::yes($meta['obligatoria']) : $practice['required_default'];
            $usesFile = in_array($mode, [SubmissionMode::File, SubmissionMode::Both], true);

            $model = $existing[$practice['code']] ?? new Practice(['node_id' => $node->id, 'code' => $practice['code']]);
            if ($model->exists && $model->is_required !== $required && $model->hasStudentActivity()) {
                $this->report->warning("{$practice['where']}: {$practice['code']} cambia de ".($required ? 'optativa a obligatoria' : 'obligatoria a optativa').' y ya tiene entregas de alumnos.');
            }
            if ($required && blank($fields['approval_criteria'] ?? null) && $mode !== SubmissionMode::None) {
                $this->report->warning("{$practice['where']}: {$practice['code']} no tiene «Criterio de aprobación».");
            }

            $model->fill([
                'title' => Str::limit($practice['title'], 255, ''),
                'instructions' => $fields['instructions'] ?? null,
                'approval_criteria' => $fields['approval_criteria'] ?? null,
                'is_required' => $required,
                'submission_mode' => $mode,
                'environment' => CourseFileParser::normalize($meta['entorno'] ?? 'navegador') === 'local' ? PracticeEnvironment::Local : PracticeEnvironment::Browser,
                'allowed_extensions' => $usesFile ? (Str::of($meta['extensiones'] ?? '')->lower()->replaceMatches('/[\s.]+/', '')->toString() ?: null) : null,
                'starter_code' => $fields['starter_code'] ?? null,
                'sample_input' => $fields['sample_input'] ?? null,
                'expected_output' => $mode === SubmissionMode::None ? null : ($fields['expected_output'] ?? null),
                'reference_solution' => $fields['reference_solution'] ?? null,
                'coin_reward' => max(0, (int) ($meta['monedas'] ?? $meta['recompensa'] ?? 0)),
                'xp_reward' => max(0, (int) ($meta['xp'] ?? 10)),
                'position' => $index + 1,
            ]);
            $this->save('prácticas', $model);
        }

        $missing = $existing->keys()->diff(collect($data['practices'])->pluck('code'));
        foreach ($missing as $code) {
            $this->report->note("La práctica {$code} de {$node->code} está en la base pero no en el archivo: quedó sin tocar.");
        }
    }

    /** Segunda pasada: con todos los nodos creados, se enlaza cada uno con su padre. */
    private function applyParents(array $nodes, array $models): void
    {
        foreach ($nodes as $node) {
            $model = $models[$node['code']] ?? null;
            if (! $model || $model->isRoot()) {
                continue;
            }
            $parentCode = Str::upper(trim($node['meta']['padre'] ?? ''));
            if ($parentCode === '') {
                $this->report->error("{$node['where']}: el nodo {$node['code']} no tiene «padre».");

                continue;
            }
            $parent = $models[$parentCode] ?? Node::where('course_id', $this->course->id)->where('code', $parentCode)->first();
            if (! $parent) {
                $this->report->error("{$node['where']}: el padre {$parentCode} de {$node['code']} no existe.");

                continue;
            }
            if ($parent->id === $model->id) {
                $this->report->error("{$node['where']}: el nodo {$node['code']} no puede ser su propio padre.");

                continue;
            }
            $model->parent_id = $parent->id;
            if ($model->isDirty('parent_id')) {
                $model->save();
            }
        }
    }

    private function checkCycles(): void
    {
        $parents = Node::where('course_id', $this->course->id)->pluck('parent_id', 'id');
        $codes = Node::where('course_id', $this->course->id)->pluck('code', 'id');

        foreach ($parents->keys() as $id) {
            $seen = [];
            for ($current = $id; $current !== null; $current = $parents[$current] ?? null) {
                if (isset($seen[$current])) {
                    $this->report->error('Los requisitos forman un ciclo en el nodo '.($codes[$id] ?? "#{$id}").'.');

                    return;
                }
                $seen[$current] = true;
            }
        }
    }

    /** Aviso si las obligatorias de un nodo no alcanzan para pagar a sus hijos. */
    private function checkEconomy(array $nodes, array $models): void
    {
        $earned = [];
        foreach ($nodes as $node) {
            $earned[$node['code']] = collect($node['practices'])
                ->filter(fn ($p) => isset($p['meta']['obligatoria']) ? self::yes($p['meta']['obligatoria']) : $p['required_default'])
                ->sum(fn ($p) => max(0, (int) ($p['meta']['monedas'] ?? $p['meta']['recompensa'] ?? 0)));
        }

        foreach ($nodes as $node) {
            $model = $models[$node['code']] ?? null;
            $parentCode = Str::upper(trim($node['meta']['padre'] ?? ''));
            if (! $model || $model->isRoot() || $model->price_currency_id || ! isset($earned[$parentCode])) {
                continue;
            }
            if ($earned[$parentCode] < $model->price) {
                $this->report->warning("Economía: las obligatorias de {$parentCode} pagan {$earned[$parentCode]} y {$node['code']} cuesta {$model->price}.");
            }
        }
    }

    private function reportLeftovers(array $data, array $models): void
    {
        $inFile = array_keys($models);
        $left = Node::where('course_id', $this->course->id)
            ->where(fn ($q) => $q->whereNull('code')->orWhereNotIn('code', $inFile))
            ->pluck('title');
        if ($left->isNotEmpty()) {
            $this->report->note('Nodos del curso que no están en el archivo (quedaron sin tocar): '.$left->implode(', ').'.');
        }
    }

    /** Guarda y cuenta si se creó, cambió o quedó igual. */
    private function save(string $entity, Model $model): void
    {
        $result = ! $model->exists ? 'created' : ($model->isDirty() ? 'updated' : 'unchanged');
        $model->save();
        $this->report->count($entity, $result);
    }

    private static function yes(mixed $value): bool
    {
        return in_array(CourseFileParser::normalize((string) $value), ['si', 'yes', 'true', '1', 'verdadero'], true);
    }
}
