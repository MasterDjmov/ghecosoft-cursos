<?php

use App\Enums\SubmissionStatus;
use App\Livewire\Admin\Dashboard;
use App\Models\PracticeMessage;
use App\Models\Submission;
use App\Models\User;
use App\Support\PracticeStats;
use Livewire\Livewire;

/** Estadísticas del panel: lo que más hacen los alumnos y dónde se traban. */
function statsSubmission(int $practiceId, User $user, int $attempt, SubmissionStatus $status, ?array $check = null, $when = null): Submission
{
    $submission = Submission::create(['practice_id' => $practiceId, 'user_id' => $user->id, 'attempt' => $attempt, 'submitted_at' => $when ?? now()]);
    $submission->forceFill(['status' => $status, 'check_result' => $check])->save();

    return $submission;
}

test('cuenta entregas, rehacer, pruebas que fallan y consultas, y arma los rankings', function () {
    $made = makeCourse();
    [$mission1, $mission2, $optional] = $made['topic1']->practices()->orderBy('id')->get()->all();
    [$ana, $beto, $caro] = User::factory()->count(3)->create()->all();

    // Misión 1: Ana la rehízo dos veces; Beto salió de una pero falló una prueba.
    statsSubmission($mission1->id, $ana, 1, SubmissionStatus::Redo);
    statsSubmission($mission1->id, $ana, 2, SubmissionStatus::Redo);
    statsSubmission($mission1->id, $ana, 3, SubmissionStatus::Approved);
    statsSubmission($mission1->id, $beto, 1, SubmissionStatus::Submitted, ['passed' => 1, 'total' => 3]);
    // La optativa: la eligieron los tres, sin problemas.
    foreach ([$ana, $beto, $caro] as $student) {
        statsSubmission($optional->id, $student, 1, SubmissionStatus::Approved, ['passed' => 2, 'total' => 2]);
    }
    // Misión 2: una consulta de Caro (la respuesta del docente no cuenta).
    PracticeMessage::create(['practice_id' => $mission2->id, 'student_id' => $caro->id, 'author_id' => $caro->id, 'body' => '¿Cómo?']);
    PracticeMessage::create(['practice_id' => $mission2->id, 'student_id' => $caro->id, 'author_id' => User::factory()->admin()->create()->id, 'body' => 'Así.']);
    // Lo que entrega el staff y lo viejo (fuera del período) no cuentan.
    statsSubmission($mission2->id, User::factory()->admin()->create(), 1, SubmissionStatus::Redo);
    statsSubmission($mission2->id, $caro, 1, SubmissionStatus::Redo, null, now()->subDays(60));

    $stats = new PracticeStats(since: now()->subDays(30));
    expect($stats->summary())->toMatchArray([
        'total' => 7, 'students' => 3, 'approved' => 4, 'redo' => 2, 'pending' => 1, 'failing' => 1, 'redo_rate' => 33, 'questions' => 1,
    ]);
    expect($stats->mostChosen()->first())->toMatchArray(['title' => 'Encargo', 'students' => 3, 'is_required' => false]);
    expect($stats->hardest()->pluck('title')->all())->toBe(['Misión 1', 'Misión 2'])
        ->and($stats->hardest()->first())->toMatchArray(['redo' => 2, 'attempts' => 2.0, 'failing' => 1]);

    // Desde el principio aparece la entrega vieja de Caro.
    expect((new PracticeStats)->summary()['redo'])->toBe(3);

    Livewire::actingAs(User::factory()->admin()->create())
        ->test(Dashboard::class)
        ->assertSee('data-test="practice-stats"', false)
        ->assertSee('data-test="stats-by-course"', false)
        ->assertSee('Donde más se traban')
        ->set('statsCourse', (string) $made['course']->id)
        ->assertDontSee('data-test="stats-by-course"', false)
        ->assertSee('Encargo');
});
