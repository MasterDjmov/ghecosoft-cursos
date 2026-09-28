<?php

use App\Enums\XpReason;
use App\Livewire\Admin\Authorizations;
use App\Livewire\Settings\Privacy;
use App\Livewire\Settings\Profile;
use App\Models\CourseCompletion;
use App\Models\GuardianAuthorization;
use App\Models\User;
use App\Services\Ledger;
use App\Services\NodeUnlocker;
use App\Services\PracticeSubmitter;
use App\Services\Ranking;
use App\Services\SubmissionReviewer;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Livewire\Livewire;

function studentInCourse(array $data, array $attributes = []): User
{
    $student = enrolledStudent($data['course'], User::factory()->create($attributes));
    app(NodeUnlocker::class)->unlock($student, $data['root']);

    return $student;
}

test('el ranking del curso ordena por la XP ganada en ese curso', function () {
    $data = makeCourse();
    $other = makeCourse();
    $ana = studentInCourse($data, ['name' => 'Ana', 'last_name' => 'Díaz']);
    $beto = studentInCourse($data, ['name' => 'Beto', 'last_name' => 'Sosa', 'ranking_display' => 'nickname', 'nickname' => 'betodev']);
    $ledger = app(Ledger::class);

    $ledger->addXp($ana, 30, XpReason::ManualAdjustment, course: $data['course'], note: 'x');
    $ledger->addXp($beto, 50, XpReason::ManualAdjustment, course: $data['course'], note: 'x');
    $ledger->addXp($ana, 500, XpReason::ManualAdjustment, course: $other['course'], note: 'otro curso');

    $rows = app(Ranking::class)->forCourse($data['course']);

    expect($rows->pluck('name')->all())->toBe(['betodev', 'Ana D.'])
        ->and($rows->first()['position'])->toBe(1);
});

test('el ranking del curso lo ven solo los que entraron al curso', function () {
    $data = makeCourse();
    $student = studentInCourse($data);

    $this->actingAs($student)->get(route('student.ranking.course', $data['course']))->assertOk()->assertSee('Top 10 del curso');
    $this->actingAs(User::factory()->create())->get(route('student.ranking.course', $data['course']))->assertForbidden();
});

test('el ranking global y el CV son opt-in', function () {
    $data = makeCourse();
    $student = studentInCourse($data, ['birth_date' => now()->subYears(25)]);
    app(Ledger::class)->addXp($student, 40, XpReason::ManualAdjustment, note: 'x');

    expect(app(Ranking::class)->global()->pluck('user_id'))->not->toContain($student->id);
    $this->get(route('cv.show', $student->username))->assertNotFound()->assertSee('Este perfil es privado')->assertDontSee($student->name);

    Livewire::actingAs($student)->test(Privacy::class)->set('cv_public', true)->call('save')->assertHasNoErrors();

    expect(app(Ranking::class)->global()->pluck('user_id'))->toContain($student->id);
    $this->get(route('cv.show', $student->username))->assertOk()->assertSee($student->fullName())->assertSee($data['course']->title);
});

test('sin fecha de nacimiento o siendo menor sin autorización no se puede publicar el CV', function () {
    $noAge = User::factory()->create(['birth_date' => null]);
    Livewire::actingAs($noAge)->test(Privacy::class)->set('cv_public', true)->call('save')->assertHasErrors('cv_public');

    $minor = User::factory()->create(['birth_date' => now()->subYears(15)]);
    Livewire::actingAs($minor)->test(Privacy::class)->set('cv_public', true)->call('save')->assertHasErrors('cv_public');

    expect($minor->fresh()->cv_public)->toBeFalse();
});

test('el menor sube la autorización, el docente la aprueba y ahí puede publicar', function () {
    Storage::fake('local');
    $minor = User::factory()->create(['birth_date' => now()->subYears(15)]);
    $admin = User::factory()->admin()->create();

    Livewire::actingAs($minor)->test(Privacy::class)
        ->assertSee('Autorización de tu adulto responsable')
        ->set('authorization', UploadedFile::fake()->createWithContent('nota.pdf', "%PDF-1.4\n%%EOF\n"))
        ->call('uploadAuthorization')
        ->assertHasNoErrors();

    $authorization = GuardianAuthorization::firstOrFail();
    Storage::disk('local')->assertExists($authorization->file_path);
    expect($admin->notifications()->count())->toBe(1);

    $this->actingAs(User::factory()->create())->get(route('files.authorization', $authorization))->assertForbidden();
    $this->actingAs($admin)->get(route('files.authorization', $authorization))->assertOk();

    Livewire::actingAs($admin)->test(Authorizations::class)
        ->call('review', $authorization->id, 'reject')->assertHasErrors('notes.'.$authorization->id)
        ->call('review', $authorization->id, 'approve')->assertHasNoErrors();

    expect($minor->fresh()->publicProfileBlocker())->toBeNull();
    Livewire::actingAs($minor)->test(Privacy::class)->set('cv_public', true)->call('save')->assertHasNoErrors();
    expect($minor->fresh()->hasPublicProfile())->toBeTrue();
});

test('el CV nunca muestra código ni comentarios, y el dueño ve la vista previa', function () {
    $data = makeCourse();
    $student = studentInCourse($data, ['birth_date' => now()->subYears(30)]);
    $submission = app(PracticeSubmitter::class)->submit($student, $data['root']->practices()->first(), 'print("secreto")');
    app(SubmissionReviewer::class)->approve($submission, User::factory()->admin()->create(), 'Comentario privado del profe');

    $this->actingAs($student)->get(route('cv.show', $student->username))
        ->assertOk()->assertSee('Vista previa')->assertDontSee('secreto')->assertDontSee('Comentario privado');
});

test('completar todos los nodos guarda el curso completado con los días', function () {
    $data = makeCourse();
    ['course' => $course, 'root' => $root, 'topic1' => $topic1, 'topic2' => $topic2] = $data;
    $topic2->delete(); // curso: raíz → tema 1 (+ extra, que no cuenta)
    $student = studentInCourse($data);
    $admin = User::factory()->admin()->create();
    $reviewer = app(SubmissionReviewer::class);
    $submitter = app(PracticeSubmitter::class);

    $reviewer->approve($submitter->submit($student, $root->practices()->first(), 'a'), $admin);
    app(NodeUnlocker::class)->unlock($student, $topic1);
    [$a, $b] = $topic1->practices()->where('is_required', true)->get()->all();
    $reviewer->approve($submitter->submit($student, $a, 'a'), $admin);
    $reward = $reviewer->approve($submitter->submit($student, $b, 'b'), $admin);

    expect($reward->courseCompleted)->toBeTrue()
        ->and(CourseCompletion::where('user_id', $student->id)->where('course_id', $course->id)->value('days_taken'))->toBeGreaterThanOrEqual(1);
});

test('el usuario no puede ser solo números', function () {
    $user = User::factory()->create();

    Livewire::actingAs($user)->test(Profile::class)
        ->set('username', '30123456')
        ->call('updateProfileInformation')
        ->assertHasErrors(['username' => 'not_regex']);
});

test('las pantallas nuevas cargan', function () {
    $admin = User::factory()->admin()->create();
    $student = User::factory()->create();

    $this->actingAs($admin)->get(route('admin.authorizations'))->assertOk();
    $this->actingAs($student)->get(route('student.ranking'))->assertOk()->assertSee('Ranking global');
    $this->actingAs($student)->get(route('privacy'))->assertOk();
    $this->get(route('cv.show', 'no-existe'))->assertNotFound();
});
