<?php

use App\Models\Badge;
use App\Models\Branch;
use App\Models\Node;
use App\Models\NodeUnlock;

/*
 * Java según el programa de la cátedra: la migración renombra ramas, nodos, prácticas e insignias para que el
 * importador encuentre los mismos nodos con su código nuevo (sin repetidos y sin perder el progreso).
 */

test('renombra las ramas, los nodos, sus prácticas y las insignias, aunque los códigos se crucen', function () {
    $made = makeCourse(['slug' => 'java', 'language' => 'java']);
    $course = $made['course'];
    $branch = fn ($code, $title) => Branch::create(['course_id' => $course->id, 'code' => $code, 'title' => $title, 'kind' => 'trunk', 'position' => 1]);
    $corrientes = $branch('S02', 'Senda de las Corrientes: Java moderno');
    $boveda = $branch('R04', 'La Bóveda Imperial');
    $node = fn ($code, $b) => Node::create(['course_id' => $course->id, 'branch_id' => $b->id, 'code' => $code, 'type' => 'topic', 'title' => $code, 'price' => 10]);
    $streams = $node('S02-N01', $corrientes);
    $leviatan = $node('S02-N05', $corrientes);
    $archivos = $node('R04-N01', $boveda);
    $streams->practices()->create(['code' => 'S02-N01-M1', 'title' => 'Ríos']);
    $archivos->practices()->create(['code' => 'R04-N01-M1', 'title' => 'CSV']);
    Badge::create(['code' => 'java_s02_n05', 'course_id' => $course->id, 'name' => 'Domador de Corrientes']);
    $student = studentWithRootOpen($made);
    NodeUnlock::create(['user_id' => $student->id, 'node_id' => $archivos->id, 'unlocked_at' => now()]);

    $migration = require database_path('migrations/2026_10_08_000053_reorder_java_course_codes.php');
    $migration->up();

    expect($corrientes->fresh()->code)->toBe('R04')
        ->and($boveda->fresh()->code)->toBe('S01')
        ->and($streams->fresh()->code)->toBe('R04-N01')
        ->and($leviatan->fresh()->code)->toBe('R04-N06')
        ->and($archivos->fresh()->code)->toBe('S01-N01')
        ->and($streams->practices()->value('code'))->toBe('R04-N01-M1')
        ->and($archivos->practices()->value('code'))->toBe('S01-N01-M1')
        ->and(Badge::where('code', 'java_r04_n06')->value('name'))->toBe('Domador de Corrientes')
        ->and(NodeUnlock::where('user_id', $student->id)->where('node_id', $archivos->id)->exists())->toBeTrue();

    // Una segunda vez no hace nada: el curso ya tiene el orden nuevo.
    $migration->up();
    expect($streams->fresh()->code)->toBe('R04-N01')->and($archivos->fresh()->code)->toBe('S01-N01');
});

test('sin el curso de Java (o con otro orden) no toca nada', function () {
    $made = makeCourse(['slug' => 'java-otro', 'language' => 'java']);
    $other = Branch::create(['course_id' => $made['course']->id, 'code' => 'S02', 'title' => 'Senda de las Corrientes', 'kind' => 'path', 'position' => 1]);

    (require database_path('migrations/2026_10_08_000053_reorder_java_course_codes.php'))->up();

    expect($other->fresh()->code)->toBe('S02');
});
