<?php

use App\Enums\CoinReason;
use App\Enums\SubmissionStatus;
use App\Livewire\Admin\Students\Show as StudentShow;
use App\Livewire\Admin\Submissions\Show as ReviewShow;
use App\Livewire\Student\PracticeCard;
use App\Models\Badge;
use App\Models\Currency;
use App\Models\PracticeMark;
use App\Models\Submission;
use App\Models\User;
use App\Services\Ledger;
use App\Services\NodeUnlocker;
use App\Services\PracticeSubmitter;
use App\Services\SubmissionReviewer;
use App\Services\TreeAccess;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Livewire\Livewire;

beforeEach(function () {
    $this->data = makeCourse();
    $this->student = enrolledStudent($this->data['course']);
    app(NodeUnlocker::class)->unlock($this->student, $this->data['root']);
    $this->practice = $this->data['root']->practices()->first(); // obligatoria: 10 monedas + 10 XP
    $this->admin = User::factory()->admin()->create();
    $this->ledger = app(Ledger::class);
    $this->coin = Currency::forCourse($this->data['course']);
});

test('el alumno entrega código y el docente recibe el aviso', function () {
    Livewire::actingAs($this->student)->test(PracticeCard::class, ['practice' => $this->practice])
        ->call('submit', code: 'print("hola")')
        ->assertHasNoErrors();

    $submission = Submission::firstOrFail();
    expect($submission->attempt)->toBe(1)
        ->and($submission->status)->toBe(SubmissionStatus::Submitted)
        ->and($this->admin->notifications()->count())->toBe(1);
});

test('no se entrega un nodo cerrado, sin abono, ni dos veces seguidas', function () {
    $submitter = app(PracticeSubmitter::class);
    $closed = $this->data['topic1']->practices()->first();

    expect(fn () => $submitter->submit($this->student, $closed, 'x=1'))->toThrow(DomainException::class, 'Abrí');

    $submitter->submit($this->student, $this->practice, 'x=1');
    expect(fn () => $submitter->submit($this->student, $this->practice, 'x=2'))->toThrow(DomainException::class, 'esperando');

    $this->student->subscriptions()->update(['ends_at' => now()->subDay()]);
    Submission::query()->update(['status' => 'redo']);
    expect(fn () => $submitter->submit($this->student, $this->practice, 'x=3'))->toThrow(DomainException::class, 'abono');
});

test('aprobar paga una sola vez aunque se apruebe otro intento', function () {
    $submitter = app(PracticeSubmitter::class);
    $reviewer = app(SubmissionReviewer::class);
    $balanceBefore = $this->ledger->balance($this->student, $this->coin);

    $first = $submitter->submit($this->student, $this->practice, 'print(1)');
    $reward = $reviewer->approve($first, $this->admin);

    expect($reward->coins)->toBe(10)
        ->and($this->ledger->balance($this->student, $this->coin))->toBe($balanceBefore + 10);

    // Un segundo intento aprobado (por ejemplo, creado a mano) no vuelve a pagar.
    $second = Submission::create(['practice_id' => $this->practice->id, 'user_id' => $this->student->id, 'attempt' => 2, 'submitted_at' => now()]);
    $again = $reviewer->approve($second, $this->admin);

    expect($again->coins)->toBe(0)
        ->and($this->ledger->balance($this->student, $this->coin))->toBe($balanceBefore + 10);
    expect(fn () => $reviewer->approve($first->fresh(), $this->admin))->toThrow(DomainException::class);
});

test('la última obligatoria completa el nodo y da la XP extra una sola vez', function () {
    $reviewer = app(SubmissionReviewer::class);
    $submission = app(PracticeSubmitter::class)->submit($this->student, $this->practice, 'print(1)');

    $reward = $reviewer->approve($submission, $this->admin);

    expect($reward->nodeCompleted)->toBeTrue()
        ->and($reward->xp)->toBe(10 + config('game.node_completed_xp'))
        ->and($this->student->fresh()->xp_total)->toBe(10 + config('game.node_completed_xp'));
});

test('vencer a un jefe da su XP y su insignia', function () {
    ['course' => $course, 'root' => $root, 'topic1' => $boss] = $this->data;
    $badge = Badge::create(['code' => 'jefe', 'name' => 'Cazador']);
    $boss->update(['type' => 'boss', 'badge_id' => $badge->id]);

    approveRequiredPractices($this->student, $root);
    $this->ledger->credit($this->student, $this->coin, 10, CoinReason::ManualAdjustment, note: 'test');
    app(NodeUnlocker::class)->unlock($this->student, $boss);

    $reviewer = app(SubmissionReviewer::class);
    [$a, $b] = $boss->practices()->where('is_required', true)->get()->all();
    $reviewer->approve(app(PracticeSubmitter::class)->submit($this->student, $a, 'x'), $this->admin);
    $reward = $reviewer->approve(app(PracticeSubmitter::class)->submit($this->student, $b, 'y'), $this->admin);

    expect($reward->badge?->id)->toBe($badge->id)
        ->and($this->student->badges()->pluck('badges.id')->all())->toBe([$badge->id])
        ->and($reward->xp)->toBe(config('game.node_completed_xp') + config('game.boss_defeated_xp'));
});

test('una optativa paga comodines', function () {
    ['topic1' => $topic1, 'root' => $root] = $this->data;
    approveRequiredPractices($this->student, $root);
    $this->ledger->credit($this->student, $this->coin, 10, CoinReason::ManualAdjustment, note: 'test');
    app(NodeUnlocker::class)->unlock($this->student, $topic1);
    $optional = $topic1->practices()->where('is_required', false)->first();

    app(SubmissionReviewer::class)->approve(app(PracticeSubmitter::class)->submit($this->student, $optional, 'x'), $this->admin);

    expect($this->ledger->balance($this->student, Currency::wildcard()))->toBe(3);
});

test('Rehacer pide comentario, no paga y permite volver a entregar', function () {
    $submission = app(PracticeSubmitter::class)->submit($this->student, $this->practice, 'print(1)');

    Livewire::actingAs($this->admin)->test(ReviewShow::class, ['submission' => $submission])
        ->call('redo')
        ->assertHasErrors('comment')
        ->set('comment', 'Falta la ciudad')
        ->call('redo');

    expect($submission->fresh()->status)->toBe(SubmissionStatus::Redo)
        ->and($submission->comments()->value('body'))->toBe('Falta la ciudad')
        ->and($this->student->notifications()->where('data->kind', 'submission.redo')->exists())->toBeTrue();

    $retry = app(PracticeSubmitter::class)->submit($this->student, $this->practice, 'print(2)');
    expect($retry->attempt)->toBe(2);
});

test('aprobar desde la bandeja lleva a la siguiente sin corregir', function () {
    $other = enrolledStudent($this->data['course']);
    app(NodeUnlocker::class)->unlock($other, $this->data['root']);
    $first = app(PracticeSubmitter::class)->submit($this->student, $this->practice, 'a');
    $second = app(PracticeSubmitter::class)->submit($other, $this->practice, 'b');

    Livewire::actingAs($this->admin)->test(ReviewShow::class, ['submission' => $first])
        ->call('approve')
        ->assertRedirect(route('admin.submissions.show', $second));
});

test('una práctica sin entrega se marca como completada y paga lo que tenga', function () {
    $this->practice->update(['submission_mode' => 'none', 'coin_reward' => 2, 'xp_reward' => 5]);

    Livewire::actingAs($this->student)->test(PracticeCard::class, ['practice' => $this->practice])
        ->call('toggleMark')
        ->assertDispatched('practice-approved');

    expect(Submission::where('user_id', $this->student->id)->value('status'))->toBe(SubmissionStatus::Approved)
        ->and(app(TreeAccess::class)->isCompleted($this->student, $this->data['root']))->toBeTrue();
});

test('en una práctica con entrega, la marca es personal y no aprueba nada', function () {
    Livewire::actingAs($this->student)->test(PracticeCard::class, ['practice' => $this->practice])->call('toggleMark');

    expect(Submission::count())->toBe(0)
        ->and(PracticeMark::where('user_id', $this->student->id)->exists())->toBeTrue();
});

test('los archivos de una entrega van al disco privado y solo los ve su autor y el docente', function () {
    Storage::fake('local');
    $this->practice->update(['submission_mode' => 'file', 'allowed_extensions' => 'py,zip']);

    Livewire::actingAs($this->student)->test(PracticeCard::class, ['practice' => $this->practice])
        ->set('file', UploadedFile::fake()->create('tarea.exe', 5))
        ->call('submit')
        ->assertHasErrors('file')
        ->set('file', UploadedFile::fake()->createWithContent('tarea.py', 'print(1)'))
        ->call('submit')
        ->assertHasNoErrors();

    $submission = Submission::firstOrFail();
    Storage::disk('local')->assertExists($submission->file_path);

    $this->actingAs($this->student)->get(route('files.submission', $submission))->assertOk();
    $this->actingAs($this->admin)->get(route('files.submission', $submission))->assertOk();
    $this->actingAs(User::factory()->create())->get(route('files.submission', $submission))->assertForbidden();
});

test('un alumno no comenta ni ve entregas ajenas, ni entra a la bandeja', function () {
    $submission = app(PracticeSubmitter::class)->submit($this->student, $this->practice, 'print("codigo ajeno")');
    $intruder = User::factory()->create();

    // Sin abono, la otra cuenta prueba la Clase 0 (D71): ve la práctica, nunca las entregas del alumno.
    Livewire::actingAs($intruder)->test(PracticeCard::class, ['practice' => $this->practice])
        ->assertDontSee('codigo ajeno')
        ->set('comment', 'Hola')->call('addComment', $submission->id)->assertForbidden();
    $this->actingAs($intruder)->get(route('admin.submissions.show', $submission))->assertRedirect(route('home'));
    $this->actingAs($intruder)->get(route('admin.submissions.index'))->assertRedirect(route('home'));
});

test('el hilo de comentarios avisa al otro lado', function () {
    $submission = app(PracticeSubmitter::class)->submit($this->student, $this->practice, 'a');

    Livewire::actingAs($this->student)->test(PracticeCard::class, ['practice' => $this->practice])
        ->set('comment', '¿Está bien así?')
        ->call('addComment', $submission->id)
        ->assertHasNoErrors();

    expect($this->admin->notifications()->where('data->kind', 'comment')->exists())->toBeTrue();
});

test('ajuste manual: motivo obligatorio y no deja saldo negativo', function () {
    $wildcard = Currency::wildcard();

    Livewire::actingAs($this->admin)->test(StudentShow::class, ['user' => $this->student])
        ->set('target', (string) $wildcard->id)->set('amount', 5)->set('reason', '')
        ->call('adjust')->assertHasErrors('reason')
        ->set('reason', 'Participación en clase')->call('adjust')->assertHasNoErrors()
        ->set('amount', -50)->set('reason', 'Corrección')->call('adjust')->assertHasErrors('amount')
        ->set('target', 'xp')->set('amount', 30)->set('reason', 'Bonus')->call('adjust')->assertHasNoErrors();

    expect($this->ledger->balance($this->student, $wildcard))->toBe(5)
        ->and($this->student->fresh()->xp_total)->toBe(30);
});

test('las pantallas nuevas cargan', function () {
    $submission = app(PracticeSubmitter::class)->submit($this->student, $this->practice, 'print(1)');

    $this->actingAs($this->admin)->get(route('admin.submissions.index'))->assertOk()->assertSee($this->student->fullName());
    $this->actingAs($this->admin)->get(route('admin.submissions.show', $submission))->assertOk()->assertSee('print(1)');
    $this->actingAs($this->admin)->get(route('admin.students.index'))->assertOk();
    $this->actingAs($this->admin)->get(route('admin.students.show', $this->student))->assertOk();
    $this->actingAs($this->admin)->get(route('admin.submissions.next'))->assertRedirect(route('admin.submissions.show', $submission));
    $this->actingAs($this->student)->get(route('movements'))->assertOk()->assertSee('Inscripción');
    $this->actingAs($this->student)->get(route('student.node', [$this->data['course'], $this->data['root']]))->assertOk()->assertSee('Esperando corrección');
});

test('el docente puede ejecutar una entrega de C++ al corregir; el alumno de C++ no ejecuta en la plataforma', function () {
    $this->data['course']->update(['language' => 'cpp']);
    $submission = Submission::create(['practice_id' => $this->practice->id, 'user_id' => $this->student->id, 'attempt' => 1,
        'code' => "#include <iostream>\nint main() { std::cout << 42; }", 'submitted_at' => now()]);

    $this->actingAs($this->admin)->get(route('admin.submissions.show', $submission))
        ->assertOk()->assertSee('title="Ejecutar (Ctrl+Enter)"', false);

    $this->actingAs($this->student)->get(route('student.node', [$this->data['course'], $this->data['root']]))
        ->assertOk()->assertDontSee('title="Ejecutar (Ctrl+Enter)"', false);
});

test('el docente ejecuta una entrega de Java con el ejecutor local o con el comando para la terminal (D67, D69)', function () {
    $this->data['course']->update(['language' => 'java']);
    $this->practice->update(['sample_input' => "3\n"]);
    $submission = Submission::create(['practice_id' => $this->practice->id, 'user_id' => $this->student->id, 'attempt' => 1,
        'code' => "class Ayuda {}\npublic class Tablas { public static void main(String[] a) {} }", 'submitted_at' => now()]);

    $this->actingAs($this->admin)->get(route('admin.submissions.show', $submission))
        ->assertOk()->assertSee('data-test="local-run"', false)->assertSee('Descargar Tablas.java')
        ->assertSee('java -cp . Tablas', false)->assertSee('title="Ejecutar (Ctrl+Enter)"', false)
        ->assertSee('127.0.0.1:17017', false);

    // Desde D85 el alumno también ejecuta Java, con el ejecutor de su propia compu.
    $this->actingAs($this->student)->get(route('student.node', [$this->data['course'], $this->data['root']]))
        ->assertOk()->assertSee('data-test="java-runner-hint"', false);
});

test('el docente puede ejecutar una entrega de PHP al corregir; el alumno de PHP no ejecuta en la plataforma (D68)', function () {
    $this->data['course']->update(['language' => 'php']);
    $submission = Submission::create(['practice_id' => $this->practice->id, 'user_id' => $this->student->id, 'attempt' => 1,
        'code' => "<?php\necho trim(fgets(STDIN)) * 2;", 'submitted_at' => now()]);

    $this->actingAs($this->admin)->get(route('admin.submissions.show', $submission))
        ->assertOk()->assertSee('title="Ejecutar (Ctrl+Enter)"', false)->assertDontSee('data-test="local-run"', false);

    $this->actingAs($this->student)->get(route('student.node', [$this->data['course'], $this->data['root']]))
        ->assertOk()->assertDontSee('title="Ejecutar (Ctrl+Enter)"', false);
});
