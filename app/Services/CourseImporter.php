<?php

namespace App\Services;

use App\Enums\BranchKind;
use App\Enums\CourseLevel;
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
use App\Rules\SafeUpload;
use App\Support\CourseImport\CourseFileParser;
use App\Support\CourseImport\ImportReport;
use App\Support\Glossary;
use App\Support\PracticeReferences;
use App\Support\TopicCatalog;
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
        'ventana' => NodeType::Window, 'senda' => NodeType::Topic,
    ];

    private const LEVELS = [
        'desde cero' => CourseLevel::Beginner, 'inicial' => CourseLevel::Beginner, 'intermedio' => CourseLevel::Intermediate, 'avanzado' => CourseLevel::Advanced,
    ];

    private const MODES = [
        'codigo' => SubmissionMode::Code, 'archivo' => SubmissionMode::File, 'ambos' => SubmissionMode::Both,
        'codigo y archivo' => SubmissionMode::Both, 'ninguna' => SubmissionMode::None, 'sin entrega' => SubmissionMode::None,
    ];

    private ImportReport $report;

    private Course $course;

    /** La carpeta del curso, para las capturas de «Cómo debe quedar» (D77); null si se importa desde la web. */
    private ?string $assetsDir = null;

    private bool $dryRun = true;

    /** @param  list<array{name: string, content: string}>  $files */
    public function import(array $files, bool $dryRun = true, ?string $assetsDir = null): ImportReport
    {
        $this->report = new ImportReport;
        $this->assetsDir = $assetsDir ? (realpath($assetsDir) ?: null) : null;
        $this->dryRun = $dryRun;
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
        if (filled($meta['nivel'] ?? null) && ! isset(self::LEVELS[CourseFileParser::normalize($meta['nivel'])])) {
            $this->report->error("Nivel «{$meta['nivel']}» desconocido (desde_cero, intermedio, avanzado).");
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
                $extensions = array_map('trim', explode(',', Str::lower(str_replace('.', '', (string) ($practice['meta']['extensiones'] ?? '')))));
                if ($blocked = array_intersect($extensions, SafeUpload::BLOCKED)) {
                    $this->report->error("{$practice['where']}: por seguridad no se aceptan entregas ".implode(', ', $blocked).'.');
                }
                $environment = CourseFileParser::normalize($practice['meta']['entorno'] ?? 'navegador');
                if (! in_array($environment, ['navegador', 'local'], true)) {
                    $this->report->error("{$practice['where']}: entorno «{$practice['meta']['entorno']}» desconocido (navegador o local).");
                }
                foreach ($practice['tests'] as $number => $test) {
                    $label = "{$practice['where']}: {$practice['code']}, prueba ".($number + 1).($test['name'] !== '' ? " «{$test['name']}»" : '');
                    if ($test['expected'] === null) {
                        $this->report->warning("{$label} sin salida: no se guarda (completala con app:course-tests --fill).");
                    }
                }
                if ($practice['tests'] !== [] && in_array(self::MODES[$mode] ?? null, [SubmissionMode::File, SubmissionMode::None], true)) {
                    $this->report->warning("{$practice['where']}: {$practice['code']} tiene pruebas pero se entrega como archivo o sin entrega: no se van a poder correr.");
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
        $this->applyRequirements($data['nodes'], $nodes);
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
            'syllabus' => ($course['syllabus'] ?? '') ?: null,
            'level' => isset($meta['nivel']) ? self::LEVELS[CourseFileParser::normalize($meta['nivel'])] ?? null : null,
            'is_featured' => isset($meta['destacado']) ? self::yes($meta['destacado']) : null,
            'is_upcoming' => isset($meta['proximamente']) ? self::yes($meta['proximamente']) : null,
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
            $kind = match (CourseFileParser::normalize($branch['meta']['tipo'] ?? 'tronco')) {
                'extra', 'extras' => BranchKind::Extra,
                'senda' => BranchKind::Path,
                'tronco' => BranchKind::Trunk,
                default => null,
            };
            if ($kind === null) {
                $this->report->error("Rama {$code}: tipo «{$branch['meta']['tipo']}» desconocido (tronco, extra o senda).");

                continue;
            }
            $model = $result[$code] ?? new Branch(['course_id' => $this->course->id, 'code' => $code]);
            $model->fill([
                'title' => $branch['title'],
                'position' => (int) ($branch['meta']['posicion'] ?? $branch['order']),
                'kind' => $kind,
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
            if ($typeKey === 'senda') {
                $this->report->warning("{$where}: «senda» es un tipo de rama (# RAMA con «tipo: senda»); el nodo se guarda como tema.");
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
            if ($currency === 'comodin' && $type === NodeType::Root) {
                $this->report->warning("{$where}: el raíz se paga siempre con la moneda del curso.");
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
                'price_currency_id' => $type !== NodeType::Root && $currency === 'comodin' ? $wildcard->id : null,
                'video_url' => $meta['video'] ?? null,
                'chronicle' => $fields['chronicle'] ?? null,
                'objectives' => $fields['objectives'] ?? null,
                'before_you_start' => $fields['before_you_start'] ?? null,
                'content' => $fields['content'] ?? null,
                'example_code' => $fields['example_code'] ?? null,
                'example_language' => filled($fields['example_code'] ?? null) ? $this->course->language->value : null,
                // "ejecutable: no": el ejemplo se muestra y se copia, pero no se corre en el navegador (pygame, hardware…).
                'example_runnable' => self::yes($meta['ejecutable'] ?? 'si'),
                'sample_input' => $fields['sample_input'] ?? null,
                'expected_output' => $fields['expected_output'] ?? null,
                'use_cases' => $fields['use_cases'] ?? null,
                'common_errors' => $fields['common_errors'] ?? null,
                'beast_key' => $beast ?: null,
                'topics' => $this->topics($meta['temas'] ?? '', $where, 'temas'),
                'uses' => $this->topics($meta['usa'] ?? '', $where, 'usa'),
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
            // Todo nodo publicado tiene al menos una obligatoria: un nodo sin hojas no se gana ni se completa.
            $hasRequired = collect($node['practices'])->contains(fn ($p) => isset($p['meta']['obligatoria']) ? self::yes($p['meta']['obligatoria']) : $p['required_default']);
            if (! $hasRequired) {
                $model->is_published
                    ? $this->report->error("{$where}: el nodo {$node['code']} no tiene ninguna práctica obligatoria (una ### Misión). Todo nodo publicado necesita al menos una; si todavía no está listo, poné «publicado: no».")
                    : $this->report->warning("{$where}: el nodo {$node['code']} no tiene prácticas obligatorias; queda sin publicar hasta que tenga una.");
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
                ...$this->references($practice, $model),
                'reference_solution' => $fields['reference_solution'] ?? null,
                'coin_reward' => max(0, (int) ($meta['monedas'] ?? $meta['recompensa'] ?? 0)),
                'xp_reward' => max(0, (int) ($meta['xp'] ?? 10)),
                'position' => $index + 1,
            ]);
            $this->save('prácticas', $model);
            $this->applyTests($model, $practice['tests']);
        }

        $missing = $existing->keys()->diff(collect($data['practices'])->pluck('code'));
        foreach ($missing as $code) {
            $this->report->note("La práctica {$code} de {$node->code} está en la base pero no en el archivo: quedó sin tocar.");
        }
    }

    /**
     * «Cómo debe quedar» (D77): copia las capturas de la carpeta del curso al disco público. Sin carpeta
     * (desde la web, que sube solo los .md) o con una imagen que no sirve, quedan las que ya tenía.
     *
     * @return array{reference_mobile?: ?string, reference_desktop?: ?string}
     */
    private function references(array $practice, Practice $model): array
    {
        $wanted = $practice['references'] ?? [];
        if ($wanted === []) {
            return ['reference_mobile' => null, 'reference_desktop' => null];
        }
        if ($this->assetsDir === null) {
            $this->report->warning("{$practice['where']}: {$practice['code']} tiene capturas («Cómo debe quedar»): desde la web no se suben; cargalas con `php artisan app:import-course` o desde el editor de la práctica.");

            return [];
        }

        $columns = [];
        foreach (['mobile' => 'reference_mobile', 'desktop' => 'reference_desktop'] as $device => $column) {
            if (! isset($wanted[$device])) {
                $columns[$column] = null;

                continue;
            }
            $path = realpath($this->assetsDir.'/'.ltrim($wanted[$device], '/'));
            $problem = $path === false ? 'no se encuentra'
                : (! str_starts_with($path, $this->assetsDir.DIRECTORY_SEPARATOR) ? 'está fuera de la carpeta del curso' : PracticeReferences::check($path));
            if ($problem) {
                $this->report->warning("{$practice['where']}: {$practice['code']}: la captura «{$wanted[$device]}» {$problem}; queda la que tenía.");

                continue;
            }
            $columns[$column] = $this->dryRun ? 'practice-refs/(revisión)' : PracticeReferences::store($path);
            $this->report->count('capturas', $model->{$column} === $columns[$column] ? 'unchanged' : ($model->{$column} ? 'updated' : 'created'));
        }

        return $columns;
    }

    /**
     * Pruebas extra (D73): no tienen actividad de alumnos colgando, así que se reemplazan enteras
     * cuando cambian. Las que no tienen salida no se guardan (ya hubo aviso).
     */
    private function applyTests(Practice $practice, array $tests): void
    {
        $wanted = collect($tests)->filter(fn ($test) => $test['expected'] !== null)->values()
            ->map(fn ($test, $index) => ['position' => $index + 1, 'name' => Str::limit($test['name'] ?: 'Prueba '.($index + 1), 255, ''), 'input' => $test['input'], 'expected_output' => $test['expected']]);
        $current = $practice->tests()->get(['position', 'name', 'input', 'expected_output'])
            ->map(fn ($test) => ['position' => $test->position, 'name' => $test->name, 'input' => $test->input, 'expected_output' => $test->expected_output]);

        if ($wanted->all() === $current->all()) {
            $wanted->isNotEmpty() && $this->report->count('pruebas', 'unchanged');

            return;
        }
        $practice->tests()->delete();
        $practice->tests()->createMany($wanted->all());
        $this->report->count('pruebas', $current->isEmpty() ? 'created' : 'updated');
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

    /**
     * Temas del universo ("temas: html.formularios, css.selectores", D70). Una clave que no está en
     * cursos/temas.md se guarda igual (el mapa la muestra como tema suelto) y se avisa.
     *
     * @return list<string>|null
     */
    private function topics(string $value, string $where, string $key): ?array
    {
        $topics = collect(preg_split('/[\s,;]+/', Str::lower($value), -1, PREG_SPLIT_NO_EMPTY))->unique()->values();
        foreach ($topics->reject(fn ($topic) => TopicCatalog::has($topic)) as $unknown) {
            $this->report->warning("{$where}: el tema «{$unknown}» de «{$key}» no está en cursos/temas.md.");
        }

        return $topics->isEmpty() ? null : $topics->all();
    }

    /** Requisitos extra ("requiere: R03-N02, R05-N01"), además del padre. */
    private function applyRequirements(array $nodes, array $models): void
    {
        foreach ($nodes as $node) {
            $model = $models[$node['code']] ?? null;
            if (! $model) {
                continue;
            }
            $codes = collect(preg_split('/[\s,;]+/', (string) ($node['meta']['requiere'] ?? ''), -1, PREG_SPLIT_NO_EMPTY))
                ->map(fn ($code) => Str::upper($code))->unique();
            if ($model->isRoot() && $codes->isNotEmpty()) {
                $this->report->warning("{$node['where']}: el raíz no tiene requisitos; se ignora «requiere».");

                continue;
            }

            $ids = [];
            foreach ($codes as $code) {
                $required = $models[$code] ?? Node::where('course_id', $this->course->id)->where('code', $code)->first();
                if (! $required) {
                    $this->report->error("{$node['where']}: el requisito {$code} de {$node['code']} no existe.");

                    continue;
                }
                $ids[] = $required->id;
            }

            $before = $model->requirements()->pluck('nodes.id')->sort()->values()->all();
            $after = collect($ids)->reject(fn ($id) => $id === $model->parent_id)->sort()->values()->all();
            if ($before === $after) {
                continue;
            }
            // Sin validar ciclos acá: se revisa todo junto al final (padres + requisitos).
            $model->requirements()->sync($after);
            $this->report->count('requisitos', 'updated');
        }
    }

    /** Un nodo no puede depender de sí mismo, ni por padre ni por requisitos extra. */
    private function checkCycles(): void
    {
        $nodeIds = Node::where('course_id', $this->course->id)->pluck('id');
        $codes = Node::where('course_id', $this->course->id)->pluck('code', 'id');
        $edges = Node::where('course_id', $this->course->id)->whereNotNull('parent_id')->pluck('parent_id', 'id')
            ->map(fn ($parent) => [$parent])->all();
        foreach (DB::table('node_requirements')->whereIn('node_id', $nodeIds)->get() as $row) {
            $edges[$row->node_id][] = $row->required_node_id;
        }

        $state = []; // 1 = visitando, 2 = listo
        $visit = function (int $id) use (&$visit, &$state, $edges): ?int {
            $state[$id] = 1;
            foreach ($edges[$id] ?? [] as $next) {
                if (($state[$next] ?? 0) === 1) {
                    return $id;
                }
                if (($state[$next] ?? 0) === 0 && ($found = $visit($next)) !== null) {
                    return $found;
                }
            }
            $state[$id] = 2;

            return null;
        };

        foreach ($nodeIds as $id) {
            if (($state[$id] ?? 0) === 0 && ($found = $visit($id)) !== null) {
                $this->report->error('Los requisitos forman un ciclo en el nodo '.($codes[$found] ?? "#{$found}").'.');

                return;
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
