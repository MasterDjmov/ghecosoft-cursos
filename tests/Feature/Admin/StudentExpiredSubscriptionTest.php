<?php

use App\Livewire\Admin\Requests;
use App\Livewire\Admin\Students\Index as StudentsIndex;
use App\Models\EnrollmentRequest;
use App\Models\User;
use Carbon\CarbonImmutable;
use Livewire\Livewire;

test('el panel de alumnos marca en rojo los cursos con el abono vencido y dice cuándo vence cada uno', function () {
    $this->travelTo(CarbonImmutable::parse('2026-11-17 12:00'));
    ['course' => $vigente] = makeCourse();
    ['course' => $vencido] = makeCourse();
    $student = enrolledStudent($vigente);
    $student->subscriptions()->update(['ends_at' => now()->addDays(10)]);
    enrolledStudent($vencido, $student);
    $student->subscriptions()->where('course_id', $vencido->id)
        ->update(['starts_at' => now()->subDays(40), 'ends_at' => now()->subDays(3)]);

    Livewire::actingAs(User::factory()->admin()->create())->test(StudentsIndex::class)
        ->assertSee('1 abono vencido')
        ->call('toggle', $student->id)
        ->assertSee('Abono vigente · vence el 27/11')
        ->assertSee('Abono vencido · venció el 14/11')
        ->assertSee('VENCIDO el 14/11: renovar')
        ->assertSee('renueva el abono (vence el 27/11)');
});

test('un curso renovado no cuenta como vencido aunque tenga un abono viejo', function () {
    ['course' => $course] = makeCourse();
    $student = enrolledStudent($course);
    $student->subscriptions()->first()->replicate()->fill(['starts_at' => now()->subDays(60), 'ends_at' => now()->subDays(30)])->save();

    Livewire::actingAs(User::factory()->admin()->create())->test(StudentsIndex::class)
        ->assertDontSee('abono vencido')
        ->assertDontSee('abonos vencidos');
});

test('el administrador puede renovar por 6 meses: arranca cuando vence el abono vigente', function () {
    $this->travelTo(CarbonImmutable::parse('2026-11-17 12:00'));
    ['course' => $course] = makeCourse();
    $student = enrolledStudent($course);
    $student->subscriptions()->update(['ends_at' => CarbonImmutable::parse('2026-11-27 12:00')]);

    Livewire::actingAs(User::factory()->admin()->create())->test(StudentsIndex::class)
        ->call('toggle', $student->id)
        ->set('enrollCourseId', (string) $course->id)
        ->set('enrollMonths', '6')
        ->call('enroll');

    $last = $student->subscriptions()->latest('ends_at')->first();
    expect($last->starts_at->toDateString())->toBe('2026-11-27')
        ->and($last->ends_at->toDateString())->toBe('2027-05-27');
});

test('una duración que no está en la lista no se acepta', function () {
    ['course' => $course] = makeCourse();
    $student = enrolledStudent($course);
    $count = $student->subscriptions()->count();

    Livewire::actingAs(User::factory()->admin()->create())->test(StudentsIndex::class)
        ->call('toggle', $student->id)
        ->set('enrollCourseId', (string) $course->id)
        ->set('enrollMonths', '60')
        ->call('enroll');

    expect($student->subscriptions()->count())->toBe($count);
});

test('al aprobar una solicitud se puede elegir un año de abono', function () {
    ['course' => $course] = makeCourse();
    $student = User::factory()->create();
    $request = EnrollmentRequest::create(['user_id' => $student->id, 'course_id' => $course->id, 'kind' => 'new', 'type' => 'contact']);

    Livewire::actingAs(User::factory()->admin()->create())->test(Requests::class)
        ->call('review', $request->id, 'approve')
        ->set('months', '12')
        ->call('confirm');

    $subscription = $student->subscriptions()->first();
    expect((int) round($subscription->starts_at->diffInMonths($subscription->ends_at)))->toBe(12);
});
