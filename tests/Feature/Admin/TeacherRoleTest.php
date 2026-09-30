<?php

use App\Enums\Role;
use App\Livewire\Admin\Courses\Cohorts;
use App\Livewire\Admin\Messages;
use App\Livewire\Admin\Students\Index as StudentsIndex;
use App\Livewire\Admin\Students\Show as StudentsShow;
use App\Livewire\Admin\Submissions\Show as SubmissionsShow;
use App\Models\Cohort;
use App\Models\CourseSubscription;
use App\Models\PracticeMessage;
use App\Models\Submission;
use App\Models\User;
use App\Services\PracticeMessenger;
use App\Services\PracticeSubmitter;
use Livewire\Livewire;

/*
 * Rol docente (D72): corrige, responde y atiende a los alumnos de sus comisiones (en el curso de cada
 * comisión). No ve pagos, no edita cursos ni monedas. El administrador sigue pudiendo todo.
 */

beforeEach(function () {
    $this->data = makeCourse();
    $this->course = $this->data['course'];
    $this->practice = $this->data['root']->practices()->first();
    $this->teacher = User::factory()->teacher()->create();
    $this->cohort = Cohort::create(['course_id' => $this->course->id, 'teacher_id' => $this->teacher->id, 'name' => 'Martes']);

    // Uno en la comisión del docente y otro sin comisión; los dos abrieron la clase 0.
    $this->mine = studentWithRootOpen($this->data);
    CourseSubscription::where('user_id', $this->mine->id)->update(['cohort_id' => $this->cohort->id]);
    $this->other = studentWithRootOpen($this->data);

    $this->mineSubmission = app(PracticeSubmitter::class)->submit($this->mine, $this->practice, 'print("mio")');
    $this->otherSubmission = app(PracticeSubmitter::class)->submit($this->other, $this->practice, 'print("ajeno")');
});

test('el docente entra a lo suyo y no a lo del administrador', function () {
    $this->actingAs($this->teacher)->get(route('home'))->assertRedirect(route('admin.submissions.index'));
    foreach (['admin.submissions.index', 'admin.messages', 'admin.students.index', 'admin.cohorts'] as $route) {
        $this->actingAs($this->teacher)->get(route($route))->assertOk();
    }
    $this->actingAs($this->teacher)->get(route('admin.syllabus', $this->course))->assertOk();
    foreach (['admin.dashboard', 'admin.requests', 'admin.settings', 'admin.courses.index', 'admin.universe', 'admin.students.create', 'admin.glossary'] as $route) {
        $this->actingAs($this->teacher)->get(route($route))->assertRedirect(route('home'));
    }
});

test('el docente solo ve y corrige las entregas de los alumnos de sus comisiones', function () {
    $this->actingAs($this->teacher)->get(route('admin.submissions.index'))
        ->assertOk()->assertSee($this->mine->fullName())->assertDontSee($this->other->fullName());

    $this->actingAs($this->teacher)->get(route('admin.submissions.show', $this->mineSubmission))->assertOk();
    $this->actingAs($this->teacher)->get(route('admin.submissions.show', $this->otherSubmission))->assertForbidden();

    Livewire::actingAs($this->teacher)->test(SubmissionsShow::class, ['submission' => $this->mineSubmission])
        ->set('comment', 'Muy bien')->call('approve');
    expect($this->mineSubmission->fresh()->status->value)->toBe('approved')
        ->and($this->mineSubmission->fresh()->reviewed_by)->toBe($this->teacher->id);
});

test('una entrega del alumno en otro curso no le llega al docente de su comisión en este', function () {
    $other = makeCourse();
    $sub = CourseSubscription::create(['user_id' => $this->mine->id, 'course_id' => $other['course']->id, 'starts_at' => now(), 'ends_at' => now()->addDays(30)]);
    $otherCourseSubmission = Submission::create(['practice_id' => $other['root']->practices()->first()->id, 'user_id' => $this->mine->id, 'attempt' => 1, 'submitted_at' => now()]);

    expect($this->teacher->can('review', $otherCourseSubmission))->toBeFalse()
        ->and($this->teacher->can('review', $this->mineSubmission))->toBeTrue()
        ->and($sub->cohort_id)->toBeNull();
});

test('el docente recibe el aviso de una entrega o consulta de su alumno, no de los demás', function () {
    $this->teacher->notifications()->delete();
    app(PracticeMessenger::class)->send($this->mine, $this->practice, $this->mine, '¿Está bien?');
    app(PracticeMessenger::class)->send($this->other, $this->practice, $this->other, 'Consulta ajena');

    $kinds = $this->teacher->fresh()->notifications->pluck('data.body');
    expect($kinds->filter(fn ($b) => str_contains($b, 'Está bien'))->count())->toBe(1)
        ->and($kinds->filter(fn ($b) => str_contains($b, 'ajena'))->count())->toBe(0);

    // Y en Mensajes solo el hilo de su alumno.
    Livewire::actingAs($this->teacher)->test(Messages::class)
        ->assertSee($this->mine->fullName())->assertDontSee($this->other->fullName());
    expect($this->teacher->can('viewThread', [PracticeMessage::class, $this->practice, $this->other]))->toBeFalse()
        ->and($this->teacher->can('send', [PracticeMessage::class, $this->practice, $this->mine]))->toBeTrue();
});

test('el docente ve la ficha de sus alumnos (sin cuenta, monedas ni seguridad) y les resetea la clave', function () {
    $this->actingAs($this->teacher)->get(route('admin.students.show', $this->mine))
        ->assertOk()->assertSee('data-test="teacher-account-actions"', false)
        ->assertDontSee('data-test="account-form"', false)->assertDontSee('data-test="account-security"', false)->assertDontSee('Ajuste manual');
    $this->actingAs($this->teacher)->get(route('admin.students.show', $this->other))->assertForbidden();

    Livewire::actingAs($this->teacher)->test(StudentsShow::class, ['user' => $this->mine])->call('resetPassword')->assertHasNoErrors();
    expect($this->mine->fresh()->must_change_password)->toBeTrue();

    Livewire::actingAs($this->teacher)->test(StudentsShow::class, ['user' => $this->mine])->call('adjust')->assertForbidden();
    Livewire::actingAs($this->teacher)->test(StudentsShow::class, ['user' => $this->mine])->call('promote')->assertForbidden();
});

test('el docente suma un alumno a su comisión desde Alumnos, pero no mueve alumnos de otro docente', function () {
    Livewire::actingAs($this->teacher)->test(StudentsIndex::class)
        ->assertSee($this->mine->fullName())->assertDontSee($this->other->fullName())
        ->set('tab', 'sumar')->set('search', $this->other->username)
        ->assertSee($this->other->fullName())->assertDontSee($this->other->email)
        ->call('toggle', $this->other->id)->assertSee('data-test="student-courses"', false)
        ->call('assignCohort', $this->other->id, $this->course->id, (string) $this->cohort->id);
    expect(CourseSubscription::where('user_id', $this->other->id)->value('cohort_id'))->toBe($this->cohort->id);

    $rival = User::factory()->teacher()->create();
    $rivalCohort = Cohort::create(['course_id' => $this->course->id, 'teacher_id' => $rival->id, 'name' => 'Jueves']);
    Livewire::actingAs($rival)->test(StudentsIndex::class)
        ->call('assignCohort', $this->other->id, $this->course->id, (string) $rivalCohort->id)->assertForbidden();
    expect(CourseSubscription::where('user_id', $this->other->id)->value('cohort_id'))->toBe($this->cohort->id);
});

test('el docente crea comisiones a su nombre y no toca las de otros', function () {
    $adminCohort = Cohort::create(['course_id' => $this->course->id, 'name' => 'Del admin']);

    Livewire::actingAs($this->teacher)->test(Cohorts::class, ['course' => $this->course])
        ->assertSee('Martes')->assertDontSee('Del admin')
        ->set('name', 'Sábados')->call('save');
    expect(Cohort::where('name', 'Sábados')->value('teacher_id'))->toBe($this->teacher->id);

    Livewire::actingAs($this->teacher)->test(Cohorts::class, ['course' => $this->course])->call('delete', $adminCohort->id)->assertNotFound();
    expect($adminCohort->fresh())->not->toBeNull();
});

test('el administrador hace docente a un alumno, filtra las entregas por docente y lo vuelve a alumno', function () {
    $admin = User::factory()->admin()->create();
    $candidate = User::factory()->create();

    Livewire::actingAs($admin)->test(StudentsShow::class, ['user' => $candidate])->call('promote');
    expect($candidate->fresh()->role)->toBe(Role::Teacher);

    $this->actingAs($admin)->get(route('admin.submissions.index', ['docente' => $this->teacher->id]))
        ->assertOk()->assertSee($this->mine->fullName())->assertDontSee($this->other->fullName());

    Livewire::actingAs($admin)->test(StudentsIndex::class)->set('tab', 'docentes')->call('demote', $this->teacher->id);
    expect($this->teacher->fresh()->role)->toBe(Role::Student)
        ->and($this->cohort->fresh()->teacher_id)->toBeNull();
});

test('el temario del curso lo ven el administrador y los docentes, con las resoluciones; el alumno no', function () {
    $this->practice->update(['instructions' => 'Mostrá un saludo.', 'reference_solution' => 'print("solucion secreta")']);

    $this->actingAs($this->teacher)->get(route('admin.syllabus', $this->course))
        ->assertOk()->assertSee('Mostrá un saludo.')->assertSee('solucion secreta')->assertSee('Tema 1');
    $this->actingAs(User::factory()->admin()->create())->get(route('admin.syllabus', $this->course))->assertOk();
    $this->actingAs($this->mine)->get(route('admin.syllabus', $this->course))->assertRedirect(route('home'));
});
