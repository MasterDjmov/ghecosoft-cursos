<?php

use App\Livewire\Admin\Statistics;
use App\Models\Cohort;
use App\Models\CourseSubscription;
use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use App\Models\StepAttempt;
use App\Models\User;
use App\Services\ActivityLog;
use App\Support\ProgressStats;
use Illuminate\Support\Facades\DB;
use Livewire\Livewire;

/** D107 fase 2: el panel de Estadísticas (embudo, micro-misiones difíciles, trabados, aparatos). */
function statsAttempt(User $user, NodeStep $step, bool $passed, ?string $answer = null): void
{
    StepAttempt::create([
        'user_id' => $user->id, 'node_step_id' => $step->id, 'node_id' => $step->node_id, 'course_id' => $step->node->course_id,
        'passed' => $passed, 'kind' => $passed ? null : 'bad', 'answer' => $answer, 'created_at' => now(),
    ]);
}

beforeEach(function () {
    $this->made = makeCourse();
    $this->made['root']->update(['code' => 'R00-N01']);
    $this->step = NodeStep::create(['node_id' => $this->made['root']->id, 'code' => 'R00-N01-P1', 'position' => 1, 'title' => 'El pergamino habla', 'expected_output' => 'He goes', 'solution' => 'He goes']);
    $this->ana = studentWithRootOpen($this->made);
    $this->beto = studentWithRootOpen($this->made);

    // Ana falla tres veces y no la supera; Beto falla una y la supera.
    foreach (['He go', 'He goe', 'He go'] as $answer) {
        statsAttempt($this->ana, $this->step, false, $answer);
    }
    statsAttempt($this->beto, $this->step, false, 'Beto escribió');
    statsAttempt($this->beto, $this->step, true);
    NodeStepCompletion::create(['user_id' => $this->beto->id, 'node_step_id' => $this->step->id, 'completed_at' => now()]);
    app(ActivityLog::class)->visit($this->ana, $this->made['root']);

    foreach ([[$this->ana, 'mobile'], [$this->beto, 'desktop']] as [$user, $device]) {
        DB::table('user_accesses')->insert(['user_id' => $user->id, 'accessed_on' => today(), 'device' => $device, 'os' => 'android', 'browser' => 'chrome', 'first_at' => now(), 'last_at' => now()]);
    }
});

test('cuenta intentos, fallos, trabados, el embudo y las respuestas equivocadas más repetidas', function () {
    $stats = new ProgressStats(User::where('role', 'student')->select('id'), $this->made['course']->id);

    expect($stats->summary())->toMatchArray(['students' => 2, 'attempts' => 5, 'fails' => 4, 'success_rate' => 20, 'visits' => 1, 'stuck' => 1]);

    $hard = $stats->hardestSteps()->first();
    expect($hard)->toMatchArray(['title' => 'El pergamino habla', 'fails' => 4, 'students' => 2, 'pending' => 1, 'per_pass' => 5.0])
        ->and($hard['answers']->first())->toBe(['text' => 'He go', 'times' => 2, 'students' => 1]);

    expect($stats->stuck()->sole()['student']->id)->toBe($this->ana->id);

    expect($stats->funnel()->firstWhere('code', 'R00-N01'))->toMatchArray(['unlocked' => 2, 'seen' => 1, 'finished' => 1]);

    expect($stats->devices()->pluck('students', 'device')->all())->toBe(['desktop' => 1, 'mobile' => 1]);
});

test('el administrador ve el panel con sus filtros', function () {
    Livewire::actingAs(User::factory()->admin()->create())
        ->test(Statistics::class)
        ->assertSee('Elegí un curso para ver su embudo.')
        ->assertSee('He go')
        ->assertSee('data-test="stuck-'.$this->ana->username.'"', false)
        ->set('course', (string) $this->made['course']->id)
        ->assertSee('2 abrieron · 1 miraron · 1 terminaron')
        ->set('student', (string) $this->beto->id)
        ->assertDontSee('data-test="stuck-'.$this->ana->username.'"', false)
        ->assertSee('el recorrido de '.$this->beto->fullName());
});

test('el docente ve solo a los alumnos de sus comisiones', function () {
    $teacher = User::factory()->teacher()->create();
    $cohort = Cohort::create(['course_id' => $this->made['course']->id, 'teacher_id' => $teacher->id, 'name' => 'Martes']);
    CourseSubscription::where('user_id', $this->ana->id)->update(['cohort_id' => $cohort->id]);
    $rival = Cohort::create(['course_id' => $this->made['course']->id, 'teacher_id' => User::factory()->teacher()->create()->id, 'name' => 'Jueves']);
    CourseSubscription::where('user_id', $this->beto->id)->update(['cohort_id' => $rival->id]);

    $this->actingAs($teacher)->get(route('admin.statistics'))->assertOk();

    Livewire::actingAs($teacher)
        ->test(Statistics::class)
        ->assertSee('data-test="stuck-'.$this->ana->username.'"', false)
        ->assertSee('He go')
        ->assertDontSee('Beto escribió')
        ->assertDontSee($this->beto->fullName())
        ->assertDontSee('Jueves')
        // La comisión de otro docente no muestra nada.
        ->set('cohort', (string) $rival->id)
        ->assertDontSee('data-test="stuck-'.$this->ana->username.'"', false)
        ->assertDontSee('Beto escribió');
});

test('un alumno no entra a Estadísticas', function () {
    $this->actingAs($this->ana)->get(route('admin.statistics'))->assertRedirect(route('home'));
    $this->actingAs($this->ana)->getJson(route('admin.statistics'))->assertForbidden();
});

test('el Inicio muestra el resumen y el enlace a Estadísticas', function () {
    $this->actingAs(User::factory()->admin()->create())->get(route('admin.dashboard'))
        ->assertOk()
        ->assertSee('data-test="stats-overview"', false)
        ->assertSee(route('admin.statistics'));
});
