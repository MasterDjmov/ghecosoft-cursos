<?php

use App\Models\CourseCompletion;
use App\Models\User;
use Illuminate\Mail\Events\MessageSending;
use Illuminate\Support\Facades\Event;

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

test('la simulación nunca manda mails de verdad, aunque el .env tenga un SMTP', function () {
    ['course' => $course] = makeCourse();
    User::factory()->admin()->create();
    // Un SMTP que no existe (y que no es 127.0.0.1, que la plataforma ignora): un solo mail lo haría notar.
    config(['mail.default' => 'smtp', 'mail.mailers.smtp.host' => 'smtp.no-existe.invalid', 'mail.mailers.smtp.port' => 2525]);
    $drivers = [];
    Event::listen(MessageSending::class, function () use (&$drivers) {
        $drivers[] = config('mail.default');
    });

    $this->artisan('app:simulate-course', ['course' => $course->slug, '--days' => 25])
        ->expectsOutputToContain('Sin errores inesperados del sistema')
        ->assertSuccessful();

    // Ni un solo mail: con el mailer de mentira, los avisos quedan solo en la campanita.
    expect($drivers)->toBe([]);
});
