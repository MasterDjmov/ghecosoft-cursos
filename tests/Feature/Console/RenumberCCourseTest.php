<?php

use App\Models\Badge;
use App\Models\Branch;
use App\Models\Node;

/*
 * C según el apunte de Programación I: entran el preprocesador (R01-N08) y pilas y colas (R03-N04), y la migración
 * corre los nodos que siguen (con sus prácticas e insignias) para que el importador cree limpios los nuevos.
 */

test('corre los nodos de C un lugar, con sus prácticas y las insignias de los jefes', function () {
    $made = makeCourse(['slug' => 'c', 'language' => 'c']);
    $course = $made['course'];
    $branch = fn ($code) => Branch::create(['course_id' => $course->id, 'code' => $code, 'title' => $code, 'kind' => 'trunk', 'position' => 1]);
    $r01 = $branch('R01');
    $r03 = $branch('R03');
    $node = fn ($code, $b, $title) => Node::create(['course_id' => $course->id, 'branch_id' => $b->id, 'code' => $code, 'type' => 'topic', 'title' => $title, 'price' => 10]);
    $bibliotecas = $node('R01-N08', $r01, 'Bibliotecas estándar útiles');
    $golem = $node('R01-N09', $r01, 'Jefe: el Gólem de Escoria');
    $punteros = $node('R03-N04', $r03, 'Punteros a función');
    $sanguijuela = $node('R03-N05', $r03, 'Jefe: la Sanguijuela de las Minas');
    $golem->practices()->create(['code' => 'R01-N09-M1', 'title' => 'El portón']);
    Badge::create(['code' => 'c_r01_n09', 'course_id' => $course->id, 'name' => 'Rompe Escoria']);
    Badge::create(['code' => 'c_r03_n05', 'course_id' => $course->id, 'name' => 'Ni una fuga']);

    $migration = require database_path('migrations/2026_10_08_000055_renumber_c_course_codes.php');
    $migration->up();

    expect($bibliotecas->fresh()->code)->toBe('R01-N09')
        ->and($golem->fresh()->code)->toBe('R01-N10')
        ->and($punteros->fresh()->code)->toBe('R03-N05')
        ->and($sanguijuela->fresh()->code)->toBe('R03-N06')
        ->and($golem->practices()->value('code'))->toBe('R01-N10-M1')
        ->and(Badge::where('code', 'c_r01_n10')->value('name'))->toBe('Rompe Escoria')
        ->and(Badge::where('code', 'c_r03_n06')->value('name'))->toBe('Ni una fuga')
        ->and(Badge::where('code', 'c_r01_n09')->exists())->toBeFalse();

    // Una segunda vez no hace nada: el Gólem ya está en R01-N10.
    $migration->up();
    expect($golem->fresh()->code)->toBe('R01-N10')->and($bibliotecas->fresh()->code)->toBe('R01-N09');
});
