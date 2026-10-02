<?php

use App\Livewire\Admin\Universe as AdminUniverse;
use App\Livewire\Student\Universe;
use App\Models\Course;
use App\Models\UniverseVote;
use App\Models\User;
use App\Support\UniverseGraph;
use Livewire\Livewire;

/*
 * El Universo del alumno (D81): mira el mapa de todos los cursos sin ver lo que no abrió, y vota
 * «Quiero aprender esto» a los temas que ningún curso enseña y a los cursos que vienen.
 */

beforeEach(function () {
    $this->made = makeCourse();
    $this->made['topic1']->update(['topics' => ['prog.variables'], 'title' => 'Tema secreto']);
    $this->student = studentWithRootOpen($this->made);
});

test('el alumno ve el Universo en su menú, con sus nodos abiertos y los demás sin nombre', function () {
    $this->actingAs($this->student)->get(route('student.worlds'))->assertSee('data-test="menu-universe"', false);

    $graph = UniverseGraph::build($this->student);
    $nodes = collect($graph['nodes'])->keyBy('id');

    expect($nodes[$this->made['root']->id]['title'])->toBe('Clase 0')
        ->and($nodes[$this->made['root']->id]['url'])->toContain('/cursos/')
        ->and($nodes[$this->made['topic1']->id]['title'])->toBeNull()
        ->and($nodes[$this->made['topic1']->id]['url'])->toBeNull()
        ->and(json_encode($graph))->not->toContain('Tema secreto')
        ->and(json_encode($graph))->not->toContain('/admin/')
        ->and($graph)->not->toHaveKey('voters');

    $this->actingAs($this->student)->get(route('student.universe'))
        ->assertOk()
        ->assertSee('data-test="student-universe"', false)
        ->assertDontSee('Tema secreto');
});

test('un curso sin publicar no aparece para el alumno; uno que viene, sí', function () {
    Course::create(['title' => 'Borrador', 'slug' => 'borrador', 'language' => 'python', 'is_published' => false]);
    $upcoming = Course::create(['title' => 'Rust', 'slug' => 'rust', 'language' => 'other', 'is_published' => false, 'is_upcoming' => true]);

    $titles = collect(UniverseGraph::build($this->student)['courses'])->pluck('title');

    expect($titles)->not->toContain('Borrador')
        ->and($titles->contains('Rust'))->toBe($upcoming->fresh()->isUpcoming());
});

test('vota una vez un tema que nadie enseña; votar de nuevo saca el voto', function () {
    $component = Livewire::actingAs($this->student)->test(Universe::class);

    expect($component->instance()->toggleVote('topic:css.posicion'))->toBe(['voted' => true, 'count' => 1])
        ->and(UniverseVote::where('user_id', $this->student->id)->count())->toBe(1)
        ->and($component->instance()->toggleVote('topic:css.posicion'))->toBe(['voted' => false, 'count' => 0]);
});

test('no se vota lo que ya se enseña, lo que no existe ni un curso publicado', function (string $target) {
    expect(UniverseGraph::canVoteFor($target))->toBeFalse();
    Livewire::actingAs($this->student)->test(Universe::class)->call('toggleVote', $target)->assertForbidden();
})->with([
    'tema que enseña un curso' => 'topic:prog.variables',
    'tema que no existe' => 'topic:no.existe',
    'cualquier cosa' => 'node:1',
]);

test('el docente ve quién pidió qué, y el administrador no vota', function () {
    UniverseVote::create(['user_id' => $this->student->id, 'target' => 'topic:css.posicion']);
    $admin = User::factory()->admin()->create();

    Livewire::actingAs($admin)->test(AdminUniverse::class)
        ->assertSee('data-test="universe-requests"', false)
        ->assertSee($this->student->fullName());

    $this->actingAs($admin)->get(route('student.universe'))->assertForbidden();
});
