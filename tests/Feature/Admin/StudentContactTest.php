<?php

use App\Livewire\Admin\Students\Index;
use App\Models\StudentContact;
use App\Models\User;
use App\Notifications\PlatformNotification;
use Illuminate\Support\Facades\Notification;
use Livewire\Livewire;

/** Escribirle a un alumno desde *Alumnos* (por ejemplo, uno nuevo que está probando la Clase 0). */
test('el administrador le escribe a un alumno nuevo: campanita y mail con respuesta a él, y queda anotado', function () {
    Notification::fake();
    $admin = User::factory()->admin()->create(['email' => 'profe@example.com']);
    $student = User::factory()->create(['name' => 'Benja', 'phone' => '380 456-9221', 'email' => 'benja@example.com']);

    Livewire::actingAs($admin)->test(Index::class, ['tab' => 'nuevos'])
        ->call('toggle', $student->id)
        ->assertSee('data-test="student-contact"', false)
        ->assertSee('https://wa.me/3804569221?text=', false)
        ->call('openContact')
        ->assertSet('contactBody', fn ($body) => str_contains($body, '¡Hola, Benja!'))
        ->set('contactBody', 'Hola Benja, ¿te ayudo con algo de la clase de prueba?')
        ->call('sendContact')
        ->assertHasNoErrors()
        ->assertSee('¿te ayudo con algo de la clase de prueba?');

    expect(StudentContact::where('user_id', $student->id)->sole()->sent_by)->toBe($admin->id);
    Notification::assertSentTo($student, PlatformNotification::class, function (PlatformNotification $n) use ($student) {
        $mail = $n->toMail($student);

        return $n->kind === 'contact' && $mail->replyTo === [['profe@example.com', $n->replyName]];
    });
});

test('un docente no le escribe a un alumno que no es de sus comisiones', function () {
    $teacher = User::factory()->teacher()->create();
    $student = User::factory()->create();

    expect($teacher->can('contact', $student))->toBeFalse();
    expect(User::factory()->admin()->create()->can('contact', $student))->toBeTrue();
});
