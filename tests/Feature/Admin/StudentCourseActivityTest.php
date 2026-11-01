<?php

use App\Enums\XpReason;
use App\Livewire\Admin\Students\Index as StudentsIndex;
use App\Models\NodeVisit;
use App\Models\User;
use App\Services\Ledger;
use App\Support\CourseActivity;
use Carbon\CarbonImmutable;
use Livewire\Livewire;

test('cada curso del alumno muestra su XP y los días con y sin actividad desde que entró', function () {
    $this->travelTo(CarbonImmutable::parse('2026-11-01 12:00'));
    ['course' => $course, 'root' => $root] = makeCourse();
    $student = enrolledStudent($course);
    $student->subscriptions()->update(['starts_at' => now()->subDays(5)]);

    app(Ledger::class)->addXp($student, 30, XpReason::ManualAdjustment, course: $course);
    NodeVisit::create(['user_id' => $student->id, 'node_id' => $root->id, 'course_id' => $course->id,
        'visited_on' => now()->subDays(3)->toDateString(), 'first_at' => now()->subDays(3), 'last_at' => now()->subDays(3)]);

    $activity = CourseActivity::for($student, [$course->id => now()->subDays(5)->toImmutable()])[$course->id];
    $states = collect($activity['days'])->mapWithKeys(fn ($d) => [$d['date']->toDateString() => $d['state']]);

    expect($activity['xp'])->toBe(30)
        ->and($activity['days'])->toHaveCount(CourseActivity::DAYS)
        ->and($states['2026-11-01'])->toBe('on')       // ganó XP hoy
        ->and($states['2026-10-29'])->toBe('on')       // miró un nodo
        ->and($states['2026-10-30'])->toBe('off')
        ->and($states['2026-10-27'])->toBe('off')      // el día que entró, sin actividad
        ->and($states['2026-10-20'])->toBe('before')   // todavía no estaba en el curso
        ->and($activity['last']->isToday())->toBeTrue();

    Livewire::actingAs(User::factory()->admin()->create())->test(StudentsIndex::class)
        ->call('toggle', $student->id)
        ->assertSee('data-test="course-activity-'.$course->id.'"', false)
        ->assertSee('Última actividad');
});
