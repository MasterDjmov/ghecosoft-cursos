<?php

use App\Livewire\Student\Worlds;
use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use App\Models\NodeVisit;
use App\Models\User;
use App\Services\NodeUnlocker;
use Livewire\Livewire;

// D118: el carrusel de «Seguí donde dejaste» arranca en lo último que se usó.

function worldsOrder(User $user): array
{
    return Livewire::actingAs($user)->test(Worlds::class)->viewData('mine')
        ->map(fn (array $world) => $world['course']->title)->all();
}

function usedCourses(User $student): array
{
    $first = makeCourse(['title' => 'Primero', 'position' => 1]);
    $second = makeCourse(['title' => 'Segundo', 'position' => 2]);
    $third = makeCourse(['title' => 'Tercero', 'position' => 3]);

    foreach ([$first, $second, $third] as $made) {
        enrolledStudent($made['course'], $student);
        app(NodeUnlocker::class)->unlock($student, $made['root']);
    }
    // Abrieron todos a la vez y hace tiempo: el orden sale de lo que se use después.
    $student->nodeUnlocks()->update(['unlocked_at' => now()->subMonth()]);

    return [$first, $second, $third];
}

test('sin uso reciente quedan en el orden de los cursos', function () {
    $student = User::factory()->create();
    usedCourses($student);

    expect(worldsOrder($student))->toBe(['Primero', 'Segundo', 'Tercero']);
});

test('primero va lo último que el alumno miró', function () {
    $student = User::factory()->create();
    [$first, , $third] = usedCourses($student);

    foreach ([[$first, 2], [$third, 1]] as [$made, $hours]) {
        NodeVisit::create([
            'user_id' => $student->id, 'node_id' => $made['root']->id, 'course_id' => $made['course']->id,
            'visited_on' => today(), 'views' => 1, 'first_at' => now()->subHours($hours), 'last_at' => now()->subHours($hours),
        ]);
    }

    expect(worldsOrder($student))->toBe(['Tercero', 'Primero', 'Segundo']);
});

test('al staff, que no deja visitas, lo ordena lo que practicó', function () {
    $admin = User::factory()->admin()->create();
    [, , $third] = usedCourses($admin);

    $step = NodeStep::create(['node_id' => $third['root']->id, 'code' => 'T-P1', 'position' => 1, 'title' => 'Paso', 'expected_output' => 'hola']);
    NodeStepCompletion::create(['user_id' => $admin->id, 'node_step_id' => $step->id, 'completed_at' => now()]);

    expect(worldsOrder($admin)[0])->toBe('Tercero');
});

test('lo vencido no le gana a lo que se puede seguir, aunque sea más reciente', function () {
    $student = User::factory()->create();
    [$first, $second] = usedCourses($student);

    NodeVisit::create([
        'user_id' => $student->id, 'node_id' => $second['root']->id, 'course_id' => $second['course']->id,
        'visited_on' => today(), 'views' => 1, 'first_at' => now(), 'last_at' => now(),
    ]);
    $student->subscriptions()->where('course_id', $second['course']->id)->update(['ends_at' => now()->subDay()]);

    expect(worldsOrder($student))->toBe(['Primero', 'Tercero', 'Segundo']);
});
