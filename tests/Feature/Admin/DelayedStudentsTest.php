<?php

use App\Livewire\Admin\Students\Delayed;
use App\Models\Cohort;
use App\Models\CourseSubscription;
use App\Models\DelayReminder;
use App\Models\User;
use App\Notifications\PlatformNotification;
use App\Services\DelayedStudents;
use App\Services\PracticeSubmitter;
use Illuminate\Support\Facades\Notification;
use Livewire\Livewire;

/*
 * Alumnos demorados: abono vigente y sin avanzar hace 7 días o más. El docente ve y avisa solo a los de sus
 * comisiones; el aviso va por mail y a la campanita, con copia interna.
 */

beforeEach(function () {
    Notification::fake();
    $this->data = makeCourse();
    $this->course = $this->data['course'];
    $this->teacher = User::factory()->teacher()->create();
    $this->cohort = Cohort::create(['course_id' => $this->course->id, 'teacher_id' => $this->teacher->id, 'name' => 'Martes']);

    $this->travel(-10)->days();
    $this->mine = studentWithRootOpen($this->data);
    CourseSubscription::where('user_id', $this->mine->id)->update(['cohort_id' => $this->cohort->id]);
    $this->other = studentWithRootOpen($this->data);
    $this->travelBack();
});

test('aparece quien no avanza hace 7 días o más, y no quien avanzó', function () {
    $rows = app(DelayedStudents::class)->for(User::factory()->admin()->create());
    expect($rows->pluck('student.id')->all())->toEqualCanonicalizing([$this->mine->id, $this->other->id])
        ->and($rows->first()['days'])->toBe(10);

    app(PracticeSubmitter::class)->submit($this->other, $this->data['root']->practices()->first(), 'print(1)');

    $rows = app(DelayedStudents::class)->for(User::factory()->admin()->create());
    expect($rows->pluck('student.id')->all())->toBe([$this->mine->id]);
});

test('con el abono vencido o recién empezado no está demorado', function () {
    CourseSubscription::where('user_id', $this->mine->id)->update(['ends_at' => now()->subDay()]);
    CourseSubscription::where('user_id', $this->other->id)->update(['starts_at' => now()->subDays(2)]);

    expect(app(DelayedStudents::class)->for(User::factory()->admin()->create()))->toBeEmpty();
});

test('con 6 días sin avanzar todavía no está demorado', function () {
    $this->travel(-6)->days();
    app(PracticeSubmitter::class)->submit($this->other, $this->data['root']->practices()->first(), 'print(1)');
    $this->travelBack();

    expect(app(DelayedStudents::class)->for(User::factory()->admin()->create())->pluck('student.id')->all())
        ->toBe([$this->mine->id]);
});

test('el docente ve y avisa solo a los de sus comisiones', function () {
    $this->actingAs($this->teacher)->get(route('admin.students.delayed'))
        ->assertOk()->assertSee($this->mine->fullName())->assertDontSee($this->other->fullName());

    Livewire::actingAs($this->teacher)->test(Delayed::class)
        ->call('open', $this->mine->id, $this->course->id)
        ->assertSet('studentId', $this->mine->id)
        ->set('body', 'Hola, ¿te trabaste? Escribime.')
        ->call('send')->assertHasNoErrors();

    expect(DelayReminder::where('user_id', $this->mine->id)->where('sent_by', $this->teacher->id)->count())->toBe(1);
    Notification::assertSentTo($this->mine, PlatformNotification::class, fn ($n) => $n->kind === 'delay-reminder' && $n->body === 'Hola, ¿te trabaste? Escribime.');

    Livewire::actingAs($this->teacher)->test(Delayed::class)
        ->call('open', $this->other->id, $this->course->id)->assertForbidden();
    expect(DelayReminder::where('user_id', $this->other->id)->exists())->toBeFalse();
});

test('el alumno no entra a la pantalla de demorados', function () {
    $this->actingAs($this->mine)->get(route('admin.students.delayed'))->assertRedirect(route('home'));
});
