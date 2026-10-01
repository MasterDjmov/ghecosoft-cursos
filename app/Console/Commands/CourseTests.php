<?php

namespace App\Console\Commands;

use App\Support\CourseImport\CourseFileParser;
use App\Support\CourseImport\ImportReport;
use App\Support\LocalCodeRunner;
use Illuminate\Console\Attributes\Description;
use Illuminate\Console\Attributes\Signature;
use Illuminate\Console\Command;
use Illuminate\Support\Str;

/**
 * Corrección asistida (D73): corre la solución de referencia de cada práctica contra su ejemplo y sus
 * pruebas, en esta compu (python3, gcc/g++, java, php8.3), y avisa lo que no coincide. Con --fill
 * escribe en los .md la salida de las pruebas que todavía no la tienen, así ninguna se escribe a mano.
 * Trabaja sobre los archivos del curso (cursos/…), no sobre la base.
 */
#[Signature('app:course-tests {path : Carpeta del curso (por ejemplo cursos/cpp)} {--fill : Completar en los .md las salidas que faltan} {--only= : Solo las prácticas cuyo código empieza así (R02, R02-N03…)}')]
#[Description('Verifica las pruebas de un curso con la solución de referencia (y completa las salidas que faltan)')]
class CourseTests extends Command
{
    private const MODES_WITH_CODE = ['codigo', 'ambos', 'codigo y archivo'];

    public function handle(): int
    {
        $folder = rtrim((string) $this->argument('path'), '/');
        $paths = is_dir($folder) ? glob($folder.'/*.md') : [];
        sort($paths);
        if ($paths === []) {
            $this->error("No hay archivos .md en {$folder}.");

            return self::FAILURE;
        }
        $files = array_map(fn ($path) => ['name' => basename($path), 'content' => file_get_contents($path)], $paths);

        $report = new ImportReport;
        $data = (new CourseFileParser)->parse($files, $report);
        $language = Str::lower((string) ($data['course']['meta']['lenguaje'] ?? ''));
        // Margen amplio: hay prácticas que miden rendimiento (sin optimizar tardan unos segundos).
        $runner = new LocalCodeRunner($language, timeout: 20);
        if (! $runner->available()) {
            $this->error("No encuentro con qué correr «{$language}» en esta compu (python3, gcc, g++, java o php).");

            return self::FAILURE;
        }
        $this->info("Probando {$folder} con ".basename($runner->binary).'…');

        $only = Str::upper((string) $this->option('only'));
        $fills = [];      // código de la práctica → [número de prueba => salida]
        $problems = [];
        $totals = ['practicas' => 0, 'pruebas' => 0, 'bien' => 0, 'mal' => 0, 'sin salida' => 0, 'salteadas' => 0];

        foreach ($data['nodes'] as $node) {
            foreach ($node['practices'] as $practice) {
                if ($only !== '' && ! str_starts_with($practice['code'], $only)) {
                    continue;
                }
                $fields = $practice['fields'];
                $mode = CourseFileParser::normalize($practice['meta']['entrega'] ?? 'codigo');
                $reference = (string) ($fields['reference_solution'] ?? '');
                $hasExample = filled($fields['expected_output'] ?? null);
                if (! in_array($mode, self::MODES_WITH_CODE, true) || (! $hasExample && $practice['tests'] === [])) {
                    continue;
                }
                if ($reference === '' || ! $runner->canRun($reference)) {
                    $totals['salteadas']++;
                    $practice['tests'] !== [] && $problems[] = [$practice['code'], '—', $reference === '' ? 'sin solución de referencia' : 'no se puede correr acá (base, ventana, web…)'];

                    continue;
                }

                $totals['practicas']++;
                $cases = [];
                if ($hasExample) {
                    $cases[] = ['label' => 'ejemplo', 'input' => $fields['sample_input'] ?? null, 'expected' => $fields['expected_output'], 'test' => null];
                }
                foreach ($practice['tests'] as $number => $test) {
                    $cases[] = ['label' => ($number + 1).($test['name'] !== '' ? " «{$test['name']}»" : ''), 'input' => $test['input'], 'expected' => $test['expected'], 'test' => $number];
                }

                $results = $runner->runMany($reference, array_column($cases, 'input'));
                foreach ($cases as $i => $case) {
                    [$output, $error] = $results[$i];
                    $totals['pruebas']++;
                    if ($error !== null) {
                        $totals['mal']++;
                        $problems[] = [$practice['code'], $case['label'], 'la solución de referencia falla: '.Str::limit($error, 120)];
                    } elseif ($case['expected'] === null) {
                        $totals['sin salida']++;
                        if (LocalCodeRunner::normalize($output) === '') {
                            $problems[] = [$practice['code'], $case['label'], 'la solución no muestra nada con esa entrada'];
                        } else {
                            $fills[$practice['code']][$case['test']] = LocalCodeRunner::normalize($output);
                        }
                    } elseif (LocalCodeRunner::matches($output, $case['expected'])) {
                        $totals['bien']++;
                    } else {
                        $totals['mal']++;
                        $problems[] = [$practice['code'], $case['label'], 'no coincide: '.$this->firstDifference($output, $case['expected'])];
                    }
                }
            }
        }

        $this->table(['Prácticas', 'Casos', 'Coinciden', 'No coinciden', 'Sin salida', 'Salteadas'], [array_values($totals)]);
        if ($problems !== []) {
            $this->table(['Práctica', 'Caso', 'Problema'], $problems);
        }

        if ($fills !== []) {
            if ($this->option('fill')) {
                $written = $this->fill($paths, $fills);
                $this->info("Completé {$written} salida(s) en los .md. Revisalas antes de commitear.");
            } else {
                $this->comment(array_sum(array_map('count', $fills)).' prueba(s) sin salida: con --fill se completan con la de la solución de referencia.');
            }
        }

        return $totals['mal'] === 0 ? self::SUCCESS : self::FAILURE;
    }

    private function firstDifference(string $output, string $expected): string
    {
        $got = explode("\n", LocalCodeRunner::normalize($output));
        $want = explode("\n", LocalCodeRunner::normalize($expected));
        foreach (range(0, max(count($got), count($want)) - 1) as $line) {
            if (($got[$line] ?? null) !== ($want[$line] ?? null)) {
                return 'en la línea '.($line + 1).' esperaba «'.($want[$line] ?? '(nada)').'» y salió «'.($got[$line] ?? '(nada)').'»';
            }
        }

        return 'difieren';
    }

    /**
     * Escribe las salidas en los .md: llena un ```salida vacío o, si la prueba no lo tiene, agrega uno
     * al final de la prueba.
     *
     * @param  list<string>  $paths
     * @param  array<string, array<int, string>>  $fills
     */
    private function fill(array $paths, array $fills): int
    {
        $written = 0;
        foreach ($paths as $path) {
            $lines = preg_split('/\R/u', file_get_contents($path));
            $out = [];
            $practice = null;
            $inTests = false;
            $test = -1;
            $fence = null;
            $hasOutput = false;

            // Cierra la prueba actual: si le faltaba el bloque ```salida y hay salida, lo agrega.
            $closeTest = function () use (&$out, &$practice, &$test, &$hasOutput, &$written, $fills) {
                if ($test >= 0 && ! $hasOutput && isset($fills[$practice][$test])) {
                    while ($out !== [] && trim(end($out)) === '') {
                        array_pop($out);
                    }
                    array_push($out, '```salida', ...[...explode("\n", $fills[$practice][$test]), '```', '']);
                    $written++;
                }
                $hasOutput = false;
            };

            foreach ($lines as $index => $line) {
                if ($fence !== null) {
                    $out[] = $line;
                    if (preg_match('/^\s*'.preg_quote($fence, '/').'\s*$/', $line)) {
                        $fence = null;
                    }

                    continue;
                }
                if (preg_match('/^\s*(```+|~~~+)\s*([\w+-]*)\s*$/', $line, $m)) {
                    $isOutput = $inTests && $test >= 0 && Str::lower($m[2]) === 'salida';
                    $hasOutput = $hasOutput || $isOutput;
                    $next = $lines[$index + 1] ?? null;
                    if ($isOutput && $next !== null && preg_match('/^\s*'.preg_quote($m[1], '/').'\s*$/', $next) && isset($fills[$practice][$test])) {
                        // ```salida vacío: se llena (la línea de cierre la agrega la vuelta siguiente).
                        array_push($out, $line, ...explode("\n", $fills[$practice][$test]));
                        $written++;
                        $fence = $m[1];

                        continue;
                    }
                    $fence = $m[1];
                    $out[] = $line;

                    continue;
                }
                if (preg_match('/^(#{2,5})\s+(.*)$/u', $line, $m)) {
                    $level = strlen($m[1]);
                    if ($inTests && ($level <= 5)) {
                        $closeTest();
                    }
                    if ($level === 5 && $inTests) {
                        $test++;
                    } elseif ($level <= 4) {
                        $inTests = $level === 4 && CourseFileParser::normalize($m[2]) === 'pruebas';
                        $test = -1;
                        if ($level <= 3) {
                            $practice = preg_match('/^(Misi[oó]n|Encargo|Pr[aá]ctica|Desaf[ií]o)\s+(\S+)/iu', $m[2], $p) ? Str::upper($p[2]) : null;
                        }
                    }
                }
                $out[] = $line;
            }
            if ($inTests) {
                $closeTest();
            }

            $content = implode("\n", $out);
            if ($content !== implode("\n", $lines)) {
                file_put_contents($path, $content);
            }
        }

        return $written;
    }
}
