<?php

namespace App\Support\CourseImport;

use Illuminate\Support\Str;

/**
 * Lee el formato de curso (docs/FORMATO-CURSO.md) y devuelve una estructura sin tocar la base.
 *
 *   # CURSO                      datos del curso (bloque meta), ### Descripción y ### Temario
 *   # DICCIONARIO                una tabla | clave | singular | plural | género | descripción | historia | ámbito |
 *   # RAMA R01 · Título          una rama (bloque meta opcional)
 *   ## R01-N01 · Título          un nodo: bloque meta + ### secciones
 *   ### Misión R01-N01-M1 · …    una práctica (Misión = obligatoria; Encargo/Desafío = optativa): meta + #### partes
 *   ### Micro-misión R01-N01-P1 · …  un paso corto que se comprueba solo (D84): meta + #### partes
 *   #### Pruebas                 pruebas extra del docente (D73): ##### Nombre + bloques ```entrada y ```salida
 *
 * Los bloques ```meta llevan líneas "clave: valor". Lo que está dentro de un bloque de código
 * nunca se toma como título.
 */
class CourseFileParser
{
    /** Sección del nodo (título normalizado) → columna. */
    public const NODE_SECTIONS = [
        'cronica' => 'chronicle',
        'objetivo' => 'objectives',
        'objetivos' => 'objectives',
        'antes de empezar' => 'before_you_start',
        'explicacion' => 'content',
        'codigo de ejemplo' => 'example_code',
        'ejemplo' => 'example_code',
        'entrada de ejemplo' => 'sample_input',
        'salida esperada' => 'expected_output',
        'para que sirve' => 'use_cases',
        'errores habituales' => 'common_errors',
        'prueba del sello' => 'self_check',
        'soluciones' => 'teacher_solutions',
        'soluciones para el docente' => 'teacher_solutions',
    ];

    /** Parte de una práctica (título normalizado) → columna. */
    public const PRACTICE_PARTS = [
        'consigna' => 'instructions',
        'criterio' => 'approval_criteria',
        'criterio de aprobacion' => 'approval_criteria',
        'codigo inicial' => 'starter_code',
        'entrada' => 'sample_input',
        'entrada de ejemplo' => 'sample_input',
        'salida esperada' => 'expected_output',
        'solucion' => 'reference_solution',
        'solucion de referencia' => 'reference_solution',
        'pruebas' => 'tests',
        'como debe quedar' => 'references',
        'como tiene que quedar' => 'references',
        'asi tiene que quedar' => 'references',
    ];

    /** Parte de una micro-misión (título normalizado) → columna (D84). */
    public const STEP_PARTS = [
        'escena' => 'scene',
        'gheco sugiere' => 'hint',
        'pista' => 'hint',
        'desafio' => 'challenge',
        'codigo inicial' => 'starter_code',
        'entrada' => 'sample_input',
        'salida esperada' => 'expected_output',
        'solucion' => 'solution',
        'al superarla' => 'success_text',
        'imagen' => 'image_prompt',
    ];

    /** Columnas que guardan código: se toma el contenido del primer bloque ``` si lo hay. */
    private const CODE_FIELDS = ['example_code', 'sample_input', 'expected_output', 'starter_code', 'reference_solution', 'solution'];

    private const SEPARATOR = '\s*[·:–—-]\s*';

    private array $result;

    private ImportReport $report;

    /** Dónde se está escribiendo: ['course'|'glossary'|'branch'|'node'|'practice', ...]. */
    private ?string $block = null;

    private ?int $nodeIndex = null;

    private ?int $practiceIndex = null;

    private ?int $stepIndex = null;

    private ?string $section = null;

    private ?string $part = null;

    private ?int $questionIndex = null;

    private ?string $currentBranch = null;

    /** @param  list<array{name: string, content: string}>  $files */
    public function parse(array $files, ImportReport $report): array
    {
        $this->report = $report;
        $this->result = ['course' => ['meta' => [], 'description' => '', 'syllabus' => ''], 'glossary' => [], 'branches' => [], 'nodes' => []];

        foreach ($files as $file) {
            $this->parseFile($file['name'], $file['content']);
        }

        return $this->finish();
    }

    private function parseFile(string $name, string $content): void
    {
        // Solo la sangría: un tabulador adentro del texto es parte de la salida (print("a\tb")).
        $content = preg_replace_callback('/^\t+/m', fn ($m) => str_repeat('    ', strlen($m[0])), $content);
        $lines = self::unwrap(preg_split('/\R/u', $content));
        $fence = null;          // marcador del bloque de código abierto (``` o ~~~)
        $metaTarget = null;     // el bloque abierto es ```meta
        $buffer = [];

        foreach ($lines as $number => $line) {
            $where = $name.':'.($number + 1);

            if ($fence !== null) {
                if (preg_match('/^\s*'.preg_quote($fence, '/').'\s*$/', $line)) {
                    if ($metaTarget !== null) {
                        $this->applyMeta($buffer, $where);
                        $buffer = [];
                        $metaTarget = null;
                    } else {
                        $this->append($line);
                    }
                    $fence = null;

                    continue;
                }
                if ($metaTarget !== null) {
                    $buffer[] = $line;
                } else {
                    $this->append($line);
                }

                continue;
            }

            if (preg_match('/^\s*(```+|~~~+)\s*([\w+-]*)\s*$/', $line, $m)) {
                $fence = $m[1];
                if (Str::lower($m[2]) === 'meta') {
                    $metaTarget = true;
                    $buffer = [];
                } else {
                    $this->append($line);
                }

                continue;
            }

            if (preg_match('/^(#{1,4})\s+(.+?)\s*#*\s*$/u', $line, $m)) {
                $this->heading(strlen($m[1]), trim($m[2]), $where);

                continue;
            }

            if ($this->block === 'glossary') {
                $this->glossaryRow($line, $where);

                continue;
            }

            $this->append($line);
        }

        if ($fence !== null) {
            $this->report->error("{$name}: quedó un bloque de código sin cerrar ({$fence}).");
        }
    }

    private function heading(int $level, string $text, string $where): void
    {
        if ($level === 1) {
            $this->resetInner();
            $this->nodeIndex = null;
            $normalized = self::normalize($text);

            if ($normalized === 'curso') {
                $this->block = 'course';
            } elseif ($normalized === 'diccionario') {
                $this->block = 'glossary';
            } elseif (preg_match('/^RAMA\s+(\S+)'.self::SEPARATOR.'(.+)$/iu', $text, $m)) {
                $code = Str::upper($m[1]);
                $this->block = 'branch';
                $this->currentBranch = $code;
                if (isset($this->result['branches'][$code])) {
                    $this->report->error("{$where}: la rama {$code} está repetida.");
                }
                $this->result['branches'][$code] = ['code' => $code, 'title' => trim($m[2]), 'meta' => [], 'order' => count($this->result['branches']) + 1];
            } else {
                $this->block = null;
                $this->report->warning("{$where}: título «{$text}» desconocido; se ignora hasta el próximo título de nivel 1.");
            }

            return;
        }

        if ($level === 2) {
            $this->resetInner();
            if (! preg_match('/^(\S+)'.self::SEPARATOR.'(.+)$/u', $text, $m) || ! str_contains($m[1], '-')) {
                $this->block = null;
                $this->nodeIndex = null;
                $this->report->error("{$where}: un nodo se escribe «## R01-N01 · Título» (falta el ID).");

                return;
            }
            $this->block = 'node';
            $this->result['nodes'][] = [
                'code' => Str::upper($m[1]), 'title' => trim($m[2]), 'branch' => $this->currentBranch,
                'meta' => [], 'fields' => [], 'self_check' => [], 'practices' => [], 'steps' => [], 'where' => $where,
            ];
            $this->nodeIndex = array_key_last($this->result['nodes']);

            return;
        }

        if ($this->block === 'course' && $level === 3) {
            $this->section = ['descripcion' => 'description', 'temario' => 'syllabus'][self::normalize($text)] ?? null;
            if ($this->section === null) {
                $this->report->warning("{$where}: sección del curso «{$text}» desconocida; se ignora.");
            }

            return;
        }

        if ($this->nodeIndex === null || ! in_array($this->block, ['node', 'practice', 'step'], true)) {
            $this->report->warning("{$where}: título «{$text}» fuera de un nodo; se ignora.");

            return;
        }

        if ($level === 3) {
            $this->part = null;
            $this->questionIndex = null;
            $this->stepIndex = null;

            if (preg_match('/^Micro[\s-]?misi[oó]n\s+(\S+)'.self::SEPARATOR.'(.+)$/iu', $text, $m)) {
                $this->block = 'step';
                $this->section = null;
                $this->practiceIndex = null;
                $this->result['nodes'][$this->nodeIndex]['steps'][] = [
                    'code' => Str::upper($m[1]), 'title' => trim($m[2]), 'meta' => [], 'fields' => [], 'where' => $where,
                ];
                $this->stepIndex = array_key_last($this->result['nodes'][$this->nodeIndex]['steps']);

                return;
            }

            if (preg_match('/^(Misi[oó]n|Encargo|Pr[aá]ctica|Desaf[ií]o)\s+(\S+)'.self::SEPARATOR.'(.+)$/iu', $text, $m)) {
                $this->block = 'practice';
                $this->section = null;
                $kind = self::normalize($m[1]);
                $this->result['nodes'][$this->nodeIndex]['practices'][] = [
                    'code' => Str::upper($m[2]), 'title' => trim($m[3]),
                    'required_default' => in_array($kind, ['mision', 'practica'], true),
                    'meta' => [], 'fields' => [], 'where' => $where,
                ];
                $this->practiceIndex = array_key_last($this->result['nodes'][$this->nodeIndex]['practices']);

                return;
            }

            $this->block = 'node';
            $this->practiceIndex = null;
            $key = self::normalize($text);
            $this->section = self::NODE_SECTIONS[$key] ?? null;
            if ($this->section === null) {
                $this->report->warning("{$where}: sección «{$text}» desconocida; se ignora.");
            }

            return;
        }

        // Nivel 4: parte de una micro-misión, de una práctica o pregunta de la Prueba del sello.
        if ($this->block === 'step') {
            $key = self::normalize($text);
            $this->part = self::STEP_PARTS[$key] ?? null;
            if ($this->part === null) {
                $this->report->warning("{$where}: parte de micro-misión «{$text}» desconocida; se ignora.");
            }

            return;
        }

        if ($this->block === 'practice') {
            $key = self::normalize($text);
            $this->part = self::PRACTICE_PARTS[$key] ?? null;
            if ($this->part === null) {
                $this->report->warning("{$where}: parte de práctica «{$text}» desconocida; se ignora.");
            }

            return;
        }

        if ($this->section === 'self_check') {
            $this->result['nodes'][$this->nodeIndex]['self_check'][] = ['question' => $text, 'answer' => ''];
            $this->questionIndex = array_key_last($this->result['nodes'][$this->nodeIndex]['self_check']);

            return;
        }

        $this->append(str_repeat('#', $level).' '.$text);
    }

    private function append(string $line): void
    {
        if ($this->block === 'course') {
            if ($this->section !== null) {
                $this->result['course'][$this->section] .= $line."\n";
            }

            return;
        }

        if ($this->nodeIndex === null) {
            return;
        }

        $node = &$this->result['nodes'][$this->nodeIndex];

        if ($this->block === 'step' && $this->stepIndex !== null) {
            if ($this->part !== null) {
                $node['steps'][$this->stepIndex]['fields'][$this->part] = ($node['steps'][$this->stepIndex]['fields'][$this->part] ?? '').$line."\n";
            }

            return;
        }

        if ($this->block === 'practice' && $this->practiceIndex !== null) {
            if ($this->part !== null) {
                $node['practices'][$this->practiceIndex]['fields'][$this->part] = ($node['practices'][$this->practiceIndex]['fields'][$this->part] ?? '').$line."\n";
            }

            return;
        }

        if ($this->section === 'self_check') {
            if ($this->questionIndex !== null) {
                $node['self_check'][$this->questionIndex]['answer'] .= $line."\n";
            }

            return;
        }

        if ($this->section !== null) {
            $node['fields'][$this->section] = ($node['fields'][$this->section] ?? '').$line."\n";
        }
    }

    /** @param  list<string>  $lines */
    private function applyMeta(array $lines, string $where): void
    {
        $meta = [];
        foreach ($lines as $line) {
            if (trim($line) === '' || str_starts_with(trim($line), '#')) {
                continue;
            }
            if (! preg_match('/^\s*([\p{L}_ ]+?)\s*:\s*(.*)$/u', $line, $m)) {
                $this->report->warning("{$where}: línea de meta sin «clave: valor»: «".trim($line).'».');

                continue;
            }
            // "precio: 10   # comentario" → 10 (el # tiene que ir después de un espacio).
            $value = preg_replace('/\s+#.*$/u', '', $m[2]);
            $meta[str_replace(' ', '_', self::normalize($m[1]))] = trim($value, " \t\"'");
        }

        match (true) {
            $this->block === 'course' => $this->result['course']['meta'] = [...$this->result['course']['meta'], ...$meta],
            $this->block === 'branch' && $this->currentBranch !== null => $this->result['branches'][$this->currentBranch]['meta'] = $meta,
            $this->block === 'practice' && $this->practiceIndex !== null => $this->result['nodes'][$this->nodeIndex]['practices'][$this->practiceIndex]['meta'] = $meta,
            $this->block === 'step' && $this->stepIndex !== null => $this->result['nodes'][$this->nodeIndex]['steps'][$this->stepIndex]['meta'] = $meta,
            $this->block === 'node' && $this->nodeIndex !== null => $this->result['nodes'][$this->nodeIndex]['meta'] = $meta,
            default => $this->report->warning("{$where}: bloque meta fuera de lugar; se ignora."),
        };
    }

    private function glossaryRow(string $line, string $where): void
    {
        $line = trim($line);
        if (! str_starts_with($line, '|')) {
            return;
        }
        $cells = array_map('trim', explode('|', trim($line, '|')));
        $first = self::normalize($cells[0] ?? '');
        if ($first === 'clave' || preg_match('/^:?-{2,}:?$/', $cells[0] ?? '')) {
            return; // encabezado o separador
        }
        if (count($cells) < 2 || $cells[0] === '') {
            $this->report->warning("{$where}: fila del diccionario incompleta; se ignora.");

            return;
        }
        $this->result['glossary'][] = [
            'key' => Str::lower(trim($cells[0], '` ')),
            'singular' => $cells[1],
            'plural' => $cells[2] ?? '',
            'gender' => $cells[3] ?? '',
            'short_description' => $cells[4] ?? '',
            'lore' => $cells[5] ?? '',
            'scope' => self::normalize($cells[6] ?? ''),
            'where' => $where,
        ];
    }

    private function resetInner(): void
    {
        $this->section = null;
        $this->part = null;
        $this->practiceIndex = null;
        $this->stepIndex = null;
        $this->questionIndex = null;
    }

    /**
     * Si el archivo entero viene envuelto en un bloque ```markdown (como lo copia un chat), se lo saca.
     *
     * @param  list<string>  $lines
     * @return list<string>
     */
    private static function unwrap(array $lines): array
    {
        $first = array_key_first(array_filter($lines, fn ($line) => trim($line) !== ''));
        $last = array_key_last(array_filter($lines, fn ($line) => trim($line) !== ''));
        if ($first === null || $first === $last) {
            return $lines;
        }
        if (preg_match('/^\s*(`{3,}|~{3,})\s*(markdown|md)?\s*$/i', $lines[$first], $open)
            && preg_match('/^\s*'.preg_quote($open[1], '/').'\s*$/', $lines[$last])) {
            return array_slice($lines, $first + 1, $last - $first - 1);
        }

        return $lines;
    }

    /** Limpia los textos y saca el código de los bloques ```. */
    private function finish(): array
    {
        $this->result['course']['description'] = trim($this->result['course']['description']);
        // Temario: un tema por línea (acepta lista con - o *).
        $this->result['course']['syllabus'] = trim(preg_replace('/^\s*[-*]\s+/m', '', $this->result['course']['syllabus']));

        foreach ($this->result['nodes'] as &$node) {
            $node['fields'] = self::cleanFields($node['fields']);
            $node['self_check'] = array_map(fn ($item) => ['question' => trim($item['question']), 'answer' => trim($item['answer'])], $node['self_check']);
            foreach ($node['practices'] as &$practice) {
                $practice['tests'] = self::parseTests($practice['fields']['tests'] ?? '');
                $practice['references'] = self::parseReferences($practice['fields']['references'] ?? '');
                unset($practice['fields']['tests'], $practice['fields']['references']);
                $practice['fields'] = self::cleanFields($practice['fields']);
            }
            foreach ($node['steps'] as &$step) {
                $step['fields'] = self::cleanFields($step['fields']);
            }
        }

        return $this->result;
    }

    /**
     * «#### Cómo debe quedar» (D77): una línea por pantalla, con la ruta de la captura relativa a la carpeta
     * del curso: «celular: capturas/R01-N01-M1-celular.webp» y «compu: …».
     *
     * @return array{mobile?: string, desktop?: string}
     */
    public static function parseReferences(string $text): array
    {
        $references = [];
        foreach (preg_split('/\R/', $text) as $line) {
            if (preg_match('/^\s*[-*]?\s*(celular|m[oó]vil|compu|computadora|escritorio)\s*:\s*`?([^`]+?)`?\s*$/iu', $line, $m)) {
                $device = in_array(self::normalize($m[1]), ['celular', 'movil'], true) ? 'mobile' : 'desktop';
                $references[$device] = trim($m[2]);
            }
        }

        return $references;
    }

    /**
     * «#### Pruebas» (D73): cada «##### Nombre» lleva un bloque ```entrada (opcional) y uno ```salida.
     * Una prueba sin salida queda con expected = null (app:course-tests --fill la completa).
     *
     * @return list<array{name: string, input: ?string, expected: ?string}>
     */
    public static function parseTests(string $text): array
    {
        $tests = [];
        foreach (preg_split('/^#####\s+/m', $text) as $index => $chunk) {
            if ($index === 0) {
                continue; // lo que va antes del primer «#####»
            }
            [$name, $body] = array_pad(explode("\n", $chunk, 2), 2, '');
            $blocks = [];
            preg_match_all('/^\s*(```+|~~~+)\s*(entrada|salida)[ \t]*\n(.*?)\n?^\s*\1\s*$/msi', $body, $matches, PREG_SET_ORDER);
            foreach ($matches as $m) {
                $blocks[Str::lower($m[2])] = rtrim($m[3]);
            }
            $tests[] = [
                'name' => trim(preg_replace('/\s*#+\s*$/', '', $name)),
                'input' => $blocks['entrada'] ?? null,
                'expected' => isset($blocks['salida']) && $blocks['salida'] !== '' ? $blocks['salida'] : null,
            ];
        }

        return $tests;
    }

    private static function cleanFields(array $fields): array
    {
        foreach ($fields as $field => $text) {
            $text = trim($text, "\n");
            // [ \t]* y no \s* después del lenguaje: una entrada puede empezar con una línea vacía (a propósito).
            if (in_array($field, self::CODE_FIELDS, true) && preg_match('/^\s*(```+|~~~+)[\w+-]*[ \t]*\n(.*?)\n\s*\1\s*$/s', trim($text), $m)) {
                $text = $m[2];
            }
            $fields[$field] = in_array($field, self::CODE_FIELDS, true) ? rtrim($text) : trim($text);
        }

        return $fields;
    }

    /** "¿Para qué sirve? (Bron)" → "para que sirve". */
    public static function normalize(string $text): string
    {
        $text = preg_replace('/\([^)]*\)/u', '', $text);
        $text = Str::of(Str::ascii($text))->lower()->replaceMatches('/[^a-z0-9 ]+/', ' ')->squish();

        return (string) $text;
    }
}
