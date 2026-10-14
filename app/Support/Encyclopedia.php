<?php

namespace App\Support;

use App\Enums\NodeType;
use App\Models\Course;
use App\Models\Node;
use App\Models\NodeUnlock;
use App\Models\User;
use App\Services\TreeAccess;
use Illuminate\Support\Collection;
use Illuminate\Support\Str;

/**
 * La Gran Enciclopedia del Código (D104): los personajes y las criaturas de todo el universo, leídos de las
 * fichas de docs/historias/PERSONAJES.md (CharacterSheets), con lo que el alumno ya descubrió.
 *
 * Lo no descubierto va en silueta, con el nombre y dónde aparece: **su texto nunca sale del servidor** (como
 * las páginas bloqueadas de Mis Crónicas). Se descubre al abrir el nodo de su «Primera aparición» (o el del
 * jefe, o el raíz del curso si la ficha no lo dice). Los protagonistas, los guías y el bestiario común se ven
 * siempre. Las imágenes van en public/img/enciclopedia/ (scripts/enciclopedia/imagenes.py).
 */
class Encyclopedia
{
    public const MASTERS = 'maestros';

    public const BESTIARY = 'bestiario';

    /** Lo que se le muestra al alumno de cada ficha, en este orden (lo demás es para generar las imágenes). */
    public const FIELDS = ['Rol', 'Curso y rol', 'Qué es', 'Qué error representa', 'Cómo se lo vence', 'Qué explica', 'Edad y sexo',
        'Personalidad', 'Le gusta', 'Defecto o miedo', 'Objeto', 'Frase', 'Cómo habla', 'Relaciones'];

    /** El lenguaje que dice entre paréntesis la sección de cada mundo. */
    private const WORLDS = ['Python' => 'python', 'C' => 'c', 'C++' => 'cpp', 'HTML y CSS' => 'html', 'Java' => 'java', 'PHP' => 'php'];

    /** Los nodos que abrió el alumno (id → posición). */
    private ?Collection $unlocked = null;

    /** @var array<int, Collection<int, Node>> Los nodos publicados de cada curso, una sola consulta por curso. */
    private array $nodes = [];

    public function __construct(private readonly User $user) {}

    /**
     * Todas las entradas, en el orden de las fichas. Las no descubiertas, sin `fields`.
     *
     * @return Collection<int, array<string, mixed>>
     */
    public function entries(): Collection
    {
        $courses = Course::where('is_published', true)->orderBy('id')->get();
        $protagonists = collect(config('game.protagonists'))->mapWithKeys(fn (array $hero, string $language) => [$hero['name'] => $language]);

        return CharacterSheets::all()->map(function (array $sheet) use ($courses, $protagonists) {
            $fields = self::fields($sheet['body']);
            $section = $sheet['section'];
            $language = preg_match('/\(([^)]+)\)$/u', $section, $m) ? (self::WORLDS[$m[1]] ?? null) : null;
            $protagonist = $sheet['protagonist'];
            $language ??= $protagonist ? ($protagonists[$sheet['name']] ?? null) : null;
            // La clave de un protagonista es un lenguaje (python) o el slug de un curso (ingles-primaria, D106).
            $course = $language ? $courses->firstWhere(fn (Course $course) => $course->language->value === $language || $course->slug === $language) : null;
            $creature = isset($fields['Qué es']) || isset($fields['Qué error representa']);
            $world = $language !== null && ! $protagonist;
            if ($world && ! $course) {
                return null; // el curso de ese mundo todavía no está publicado
            }

            $target = $world ? $this->target($course, $fields, $creature) : null;
            $discovered = ! $world || $this->user->isStaff() || ($target && $this->isUnlocked($target));
            $name = trim(preg_replace('/\s*\([^)]*\)$/u', '', $sheet['name']));
            $key = Str::slug($name);
            $boss = $creature && $target?->type === NodeType::Boss;

            return [
                'key' => $key,
                'name' => $name,
                'section' => $creature ? self::BESTIARY : self::MASTERS,
                'group' => match (true) {
                    $protagonist => 'Los protagonistas',
                    ! $world => preg_replace('/\s*\(.*\)$/u', '', $section),
                    default => $section,
                },
                'course' => $course,
                'portrait' => self::image($key),
                'figure' => self::image($key.'-cuerpo'),
                'discovered' => $discovered,
                'boss' => $boss,
                'defeated' => $boss && $discovered && app(TreeAccess::class)->isCompleted($this->user, $target),
                'where' => $this->where($course, $target, $boss),
                'fields' => $discovered ? collect(self::FIELDS)->filter(fn ($label) => isset($fields[$label]))->mapWithKeys(fn ($label) => [$label => $fields[$label]])->all() : [],
            ];
        })->filter()->values();
    }

    /** @return array{discovered: int, total: int} */
    public static function count(Collection $entries, string $section): array
    {
        $of = $entries->where('section', $section);

        return ['discovered' => $of->where('discovered', true)->count(), 'total' => $of->count()];
    }

    /**
     * Los renglones «- **Rótulo:** texto» de la ficha (con sus sub-renglones), sin los enlaces a los .md.
     *
     * @return array<string, string>
     */
    public static function fields(string $body): array
    {
        $fields = [];
        $label = null;
        foreach (preg_split('/\R/u', $body) as $line) {
            if (preg_match('/^- \*\*(.+?):\*\*\s*(.*)$/u', $line, $m)) {
                $label = $m[1];
                $fields[$label] = $m[2];
            } elseif ($label !== null && preg_match('/^\s+\S/u', $line)) {
                $fields[$label] .= "\n".$line;
            } elseif (trim($line) !== '') {
                $label = null;
            }
        }

        return array_map(fn (string $text) => trim(preg_replace(
            ['/\s*\(\[[^\]]*\]\([^)]*\.md[^)]*\)\)/u', '/\[([^\]]+)\]\([^)]*\)/u'],
            ['', '$1'],
            $text,
        )), $fields);
    }

    /**
     * El nodo donde aparece: el de su «Primera aparición» («C, R01-N02», «HTML y CSS, Clase 0») o, en las
     * criaturas, el jefe de la rama que dice su rol («el jefe de R02 de C»); si no dice, el raíz del curso.
     */
    private function target(Course $course, array $fields, bool $creature): ?Node
    {
        $text = $fields['Primera aparición'] ?? ($creature ? ($fields['Rol'] ?? '') : '');
        $nodes = $this->nodes[$course->id] ??= $course->nodes()->where('is_published', true)
            ->orderBy('position')->orderBy('id')->with('branch:id,title')->get(['id', 'course_id', 'branch_id', 'code', 'type', 'title']);
        $root = $nodes->first(fn (Node $node) => $node->type === NodeType::Root);
        if (! preg_match('/\bR\d\d(?:-N\d\d)?\b/u', $text, $m)) {
            return $root;
        }
        $code = $m[0];
        if (str_contains($code, '-N')) {
            return $nodes->firstWhere('code', $code) ?? $root;
        }
        $branch = $nodes->filter(fn (Node $node) => str_starts_with((string) $node->code, $code.'-'));

        return ($creature ? $branch->first(fn (Node $node) => $node->type === NodeType::Boss) : null) ?? $branch->first() ?? $root;
    }

    /** La pista: «C · «Variables y tipos»»; en un jefe, su rama (el nodo se llama como él). */
    private function where(?Course $course, ?Node $target, bool $boss): ?string
    {
        if (! $course) {
            return null;
        }
        $world = Str::before($course->title, ':');
        if ($boss && $target->branch) {
            return $world.' · jefe de «'.$target->branch->title.'»';
        }

        return $target ? $world.' · «'.$target->title.'»' : $world;
    }

    private function isUnlocked(Node $node): bool
    {
        $this->unlocked ??= NodeUnlock::where('user_id', $this->user->id)->pluck('node_id')->flip();

        return $this->unlocked->has($node->id);
    }

    private static function image(string $name): ?string
    {
        return is_file(public_path("img/enciclopedia/{$name}.webp")) ? asset("img/enciclopedia/{$name}.webp") : null;
    }
}
