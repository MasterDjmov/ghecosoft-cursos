<?php

use App\Models\Badge;
use App\Models\Branch;
use App\Models\Node;

/*
 * C++ con Qt obligatorio: la Senda de los Vitrales (S02) pasa a ser la rama R06, con la Encrucijada al final, y la
 * migración renombra la rama, los nodos, sus prácticas y la insignia del jefe para que el importador los encuentre.
 */

test('la Senda de Qt pasa a ser la rama R06 y la Encrucijada su último nodo', function () {
    $made = makeCourse(['slug' => 'cpp', 'language' => 'cpp']);
    $course = $made['course'];
    $r05 = Branch::create(['course_id' => $course->id, 'code' => 'R05', 'title' => 'El Taller del Juego', 'kind' => 'trunk', 'position' => 5]);
    $s02 = Branch::create(['course_id' => $course->id, 'code' => 'S02', 'title' => 'Los Vitrales', 'kind' => 'path', 'position' => 7]);
    $node = fn ($code, $b, $title) => Node::create(['course_id' => $course->id, 'branch_id' => $b->id, 'code' => $code, 'type' => 'topic', 'title' => $title, 'price' => 3]);
    $crossroads = $node('R05-N07', $r05, 'La Encrucijada de los Engranajes');
    $windows = $node('S02-N01', $s02, 'Los Vitrales: ventanas, señales y slots');
    $drawing = $node('S02-N03', $s02, 'Dibujar, el mouse y el modelo-vista');
    $gargoyle = $node('S02-N04', $s02, 'Jefe de los Vitrales: la Gárgola del Editor');
    $gargoyle->practices()->create(['code' => 'S02-N04-M1', 'title' => 'El editor de niveles']);
    Badge::create(['code' => 'cpp_s02_n04', 'course_id' => $course->id, 'name' => 'Sello de la Gárgola']);

    $migration = require database_path('migrations/2026_10_08_000056_renumber_cpp_course_codes.php');
    $migration->up();

    expect($s02->fresh()->code)->toBe('R06')
        ->and($windows->fresh()->code)->toBe('R06-N01')
        ->and($drawing->fresh()->code)->toBe('R06-N04')
        ->and($gargoyle->fresh()->code)->toBe('R06-N05')
        ->and($crossroads->fresh()->code)->toBe('R06-N06')
        ->and($gargoyle->practices()->value('code'))->toBe('R06-N05-M1')
        ->and(Badge::where('code', 'cpp_r06_n05')->value('name'))->toBe('Sello de la Gárgola');

    // Una segunda vez no hace nada: ya no hay S02-N04.
    $migration->up();
    expect($gargoyle->fresh()->code)->toBe('R06-N05')->and($crossroads->fresh()->code)->toBe('R06-N06');
});
