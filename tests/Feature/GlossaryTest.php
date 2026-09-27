<?php

use App\Models\GlossaryTerm;

test('term() usa el término del curso, después el general y después el valor por defecto', function () {
    ['course' => $course] = makeCourse();

    expect(term('coin.course'))->toBe('moneda')
        ->and(term('coin.course', null, 3))->toBe('monedas');

    GlossaryTerm::create(['key' => 'coin.course', 'singular' => 'runa', 'plural' => 'runas', 'gender' => 'f']);
    expect(term('coin.course', $course, 2))->toBe('runas');

    GlossaryTerm::create(['key' => 'coin.course', 'course_id' => $course->id, 'singular' => 'escama', 'plural' => 'escamas', 'gender' => 'f']);
    expect(term('coin.course', $course, 2))->toBe('escamas')
        ->and(term('coin.course', null, 2))->toBe('runas');
});

test('una clave desconocida no rompe la pantalla', function () {
    expect(term('algo.inexistente'))->toBe('Algo.inexistente');
});
