<?php

use App\Livewire\Admin\Students\Index as StudentsIndex;
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
