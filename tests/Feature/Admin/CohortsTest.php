<?php

use App\Livewire\Admin\Courses\Cohorts;
use App\Livewire\Admin\Students\Show;
use App\Models\CoinTransaction;
use App\Models\CourseSubscription;
use App\Models\EnrollmentRequest;
use App\Models\User;
use App\Services\EnrollmentApprover;
use App\Services\StudentAccounts;
use Livewire\Livewire;

/** Comisiones: se crean en el curso y se asignan después sin tocar el progreso. */
beforeEach(function () {
    $this->admin = User::factory()->admin()->create();
    $this->actingAs($this->admin);
});

test('el docente crea, edita, cierra y borra comisiones de un curso', function () {
    ['course' => $course] = makeCourse();

    $this->get(route('admin.courses.edit', $course))->assertOk()->assertSee('Comisiones');

    Livewire::test(Cohorts::class, ['course' => $course])
        ->call('create')
        ->set('name', 'Martes tarde')
        ->set('modality', 'in_person')
        ->set('schedule_text', 'Mar 18 a 20 h')
        ->set('starts_on', '2026-10-06')
        ->call('save')
        ->assertHasNoErrors()
        ->assertSee('Martes tarde');

    $cohort = $course->cohorts()->firstOrFail();
    expect($cohort->schedule_text)->toBe('Mar 18 a 20 h')
        ->and($cohort->starts_on->format('Y-m-d'))->toBe('2026-10-06')
        ->and($cohort->is_open_for_enrollment)->toBeTrue();

    Livewire::test(Cohorts::class, ['course' => $course])
        ->call('edit', $cohort->id)
        ->set('name', 'Martes noche')
        ->call('save')
        ->call('toggleOpen', $cohort->id);

    expect($cohort->fresh())->name->toBe('Martes noche')->is_open_for_enrollment->toBeFalse();

    Livewire::test(Cohorts::class, ['course' => $course])->call('delete', $cohort->id);
    expect($course->cohorts()->count())->toBe(0);
});

test('no se editan comisiones de otro curso', function () {
    ['course' => $course] = makeCourse();
    ['course' => $other] = makeCourse();
    $foreign = $other->cohorts()->create(['name' => 'Ajena']);

    Livewire::test(Cohorts::class, ['course' => $course])->call('delete', $foreign->id)->assertNotFound();
    expect($foreign->fresh())->not->toBeNull();
});

test('asignar la comisión después no toca monedas, abono ni aperturas', function () {
    ['course' => $course] = makeCourse();
    $student = enrolledStudent($course);
    $cohort = $course->cohorts()->create(['name' => 'Jueves']);
    $subscription = CourseSubscription::where('user_id', $student->id)->firstOrFail();
    $coins = CoinTransaction::where('user_id', $student->id)->count();

    Livewire::test(Show::class, ['user' => $student])
        ->assertSee('Sin comisión')
        ->call('changeCohort', $course->id, (string) $cohort->id);

    $fresh = $subscription->fresh();
    expect($fresh->cohort_id)->toBe($cohort->id)
        ->and($fresh->ends_at->equalTo($subscription->ends_at))->toBeTrue()
        ->and(CoinTransaction::where('user_id', $student->id)->count())->toBe($coins);

    Livewire::test(Show::class, ['user' => $student])->call('changeCohort', $course->id, '');
    expect($subscription->fresh()->cohort_id)->toBeNull();
});

test('no se asigna una comisión de otro curso', function () {
    ['course' => $course] = makeCourse();
    ['course' => $other] = makeCourse();
    $student = enrolledStudent($course);
    $foreign = $other->cohorts()->create(['name' => 'Ajena']);

    Livewire::test(Show::class, ['user' => $student])->call('changeCohort', $course->id, (string) $foreign->id);

    expect(CourseSubscription::where('user_id', $student->id)->value('cohort_id'))->toBeNull();
});

test('al renovar sin elegir comisión, sigue en la que tenía', function () {
    ['course' => $course] = makeCourse();
    $student = enrolledStudent($course);
    $cohort = $course->cohorts()->create(['name' => 'Jueves']);
    app(StudentAccounts::class)->changeCohort($student, $course, $cohort->id);

    $renewal = EnrollmentRequest::create(['user_id' => $student->id, 'course_id' => $course->id, 'kind' => 'renewal', 'type' => 'contact']);
    $subscription = app(EnrollmentApprover::class)->approve($renewal, $this->admin);

    expect($subscription->cohort_id)->toBe($cohort->id);
});
