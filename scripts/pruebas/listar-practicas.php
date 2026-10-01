<?php
// Lista las prácticas de código que leen entrada y todavía no tienen #### Pruebas (D73), con su consigna,
// la entrada y la salida de ejemplo, para escribirles pruebas. Desde la carpeta del proyecto:
//   php scripts/pruebas/listar-practicas.php cursos/cpp [R01] > /tmp/cpp.txt
require 'vendor/autoload.php';
$files = [];
foreach (glob($argv[1].'/*.md') as $f) $files[] = ['name' => basename($f), 'content' => file_get_contents($f)];
$d = (new App\Support\CourseImport\CourseFileParser)->parse($files, new App\Support\CourseImport\ImportReport);
$only = $argv[2] ?? '';
foreach ($d['nodes'] as $n) foreach ($n['practices'] as $p) {
    $f = $p['fields'];
    $mode = App\Support\CourseImport\CourseFileParser::normalize($p['meta']['entrega'] ?? 'codigo');
    if (!in_array($mode, ['codigo','ambos'], true) || blank($f['sample_input'] ?? null) || blank($f['expected_output'] ?? null) || blank($f['reference_solution'] ?? null)) continue;
    if ($only && !str_starts_with($p['code'], $only)) continue;
    if ($p['tests']) continue;
    echo "=============== {$p['code']} · {$p['title']}\n";
    echo "CONSIGNA:\n".trim($f['instructions'] ?? '')."\n";
    echo "ENTRADA:\n{$f['sample_input']}\n";
    echo "SALIDA:\n".implode("\n", array_slice(explode("\n", $f['expected_output']), 0, 12))."\n";
}
