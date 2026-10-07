<?php

use App\Livewire\Admin\Courses\Form;
use App\Livewire\Admin\Students\Show;
use App\Models\Course;
use App\Models\EnrollmentRequest;
use App\Models\Submission;
use App\Models\User;
use App\Services\PracticeSubmitter;
use App\Services\StudentAccounts;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Livewire\Livewire;

/*
 * Borrados (D87): un curso con alumnos se borra entero solo escribiendo su nombre corto; un alumno se elimina
 * desde su ficha escribiendo su usuario. Solo el administrador, y con sus archivos privados.
 */

test('un curso con alumnos se borra con todo solo escribiendo su nombre corto', function () {
    Storage::fake('local');
    $made = makeCourse();
    $student = studentWithRootOpen($made);
    $practice = $made['root']->practices()->first();
    app(PracticeSubmitter::class)->submit($student, $practice, 'print(1)');
    $receipt = EnrollmentRequest::where('user_id', $student->id)->first();
    Storage::disk('local')->put('receipts/r.pdf', 'x');
    $receipt->update(['receipt_path' => 'receipts/r.pdf']);
    $xp = $student->fresh()->xp_total;
    $admin = User::factory()->admin()->create();

    Livewire::actingAs($admin)->test(Form::class, ['course' => $made['course']])
        ->assertSee('data-test="delete-impact"', false)
        ->set('deleteConfirm', 'otro')
        ->call('deleteWithStudents')
        ->assertHasErrors('deleteConfirm');
    expect(Course::find($made['course']->id))->not->toBeNull();

    Livewire::actingAs($admin)->test(Form::class, ['course' => $made['course']])
        ->set('deleteConfirm', $made['course']->slug)
        ->call('deleteWithStudents')
        ->assertRedirect(route('admin.courses.index'));

    expect(Course::find($made['course']->id))->toBeNull()
        ->and(Submission::where('user_id', $student->id)->exists())->toBeFalse()
        ->and(EnrollmentRequest::where('user_id', $student->id)->exists())->toBeFalse()
        ->and(User::find($student->id))->not->toBeNull()
        ->and($student->fresh()->xp_total)->toBe($xp);
    Storage::disk('local')->assertMissing('receipts/r.pdf');
});

test('el alumno se elimina desde su ficha con sus archivos, escribiendo su usuario', function () {
    Storage::fake('local');
    $made = makeCourse();
    $student = studentWithRootOpen($made);
    $practice = $made['root']->practices()->first();
    $practice->update(['submission_mode' => 'file']);
    $submission = app(PracticeSubmitter::class)->submit($student, $practice, null, UploadedFile::fake()->create('tarea.zip', 5, 'application/zip'));
    $file = $submission->file_path;
    $admin = User::factory()->admin()->create();

    Livewire::actingAs($admin)->test(Show::class, ['user' => $student])
        ->set('deleteConfirm', 'mal')
        ->call('deleteAccount')
        ->assertHasErrors('deleteConfirm');

    Livewire::actingAs($admin)->test(Show::class, ['user' => $student])
        ->set('deleteConfirm', $student->username)
        ->call('deleteAccount')
        ->assertRedirect(route('admin.students.index'));

    expect(User::find($student->id))->toBeNull()
        ->and(Course::find($made['course']->id))->not->toBeNull();
    if ($file) {
        Storage::disk('local')->assertMissing($file);
    }
});

test('el docente no elimina alumnos', function () {
    $made = makeCourse();
    $student = studentWithRootOpen($made);
    $teacher = User::factory()->teacher()->create();
    // El alumno es de una comisión del docente: puede ver su ficha, pero no eliminarlo.
    $cohort = $made['course']->cohorts()->create(['name' => 'Tarde', 'teacher_id' => $teacher->id]);
    $student->subscriptions()->update(['cohort_id' => $cohort->id]);

    Livewire::actingAs($teacher)->test(Show::class, ['user' => $student])
        ->set('deleteConfirm', $student->username)
        ->call('deleteAccount')
        ->assertForbidden();
    expect(User::find($student->id))->not->toBeNull();
});

test('no se eliminan cuentas de docentes ni administradores por este camino', function () {
    expect(fn () => app(StudentAccounts::class)->delete(User::factory()->teacher()->create()))
        ->toThrow(InvalidArgumentException::class);
});
