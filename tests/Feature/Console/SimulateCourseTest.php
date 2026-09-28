<?php

use App\Models\CourseCompletion;
use App\Models\User;

test('el súper test hace cursar un curso completo y todos los controles dan bien', function () {
    ['course' => $course] = makeCourse();
    User::factory()->admin()->create();

    $this->artisan('app:simulate-course', ['course' => $course->slug, '--days' => 25])
        ->expectsOutputToContain('Sin errores inesperados del sistema')
        ->assertSuccessful();

    expect(User::where('email', 'like', '%@simulacion.test')->count())->toBe(5)
        ->and(CourseCompletion::where('course_id', $course->id)->count())->toBe(5);

    // Se puede repetir borrando la anterior.
    $this->artisan('app:simulate-course', ['course' => $course->slug])->assertFailed();
});

test('el súper test no corre en producción', function () {
    ['course' => $course] = makeCourse();
    app()->detectEnvironment(fn () => 'production');

    $this->artisan('app:simulate-course', ['course' => $course->slug])->assertFailed();
});
