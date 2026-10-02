<?php

use App\Models\CourseCompletion;
use App\Models\GlossaryTerm;
use App\Models\User;
use App\Services\PracticeSubmitter;
use App\Services\SubmissionReviewer;
use App\Support\Chronicles;
use App\Support\Glossary;

/*
 * Mis Crónicas (D80): el prólogo para todos y el libro de cada curso empezado, que se abre al completar
 * nodos. Lo bloqueado se ve en silueta, pero su texto nunca llega al navegador.
 */

beforeEach(function () {
    $this->made = makeCourse();
    $this->made['root']->update(['chronicle' => 'Despertás en un valle desconocido.']);
    $this->made['topic1']->update(['chronicle' => 'SECRETO: la serpiente habla.', 'title' => 'Tema oculto']);
    $this->student = studentWithRootOpen($this->made);
});

function approveRoot(array $made, User $student): void
{
    $practice = $made['root']->practices()->first();
    $submission = app(PracticeSubmitter::class)->submit($student, $practice, 'print("hola")');
    app(SubmissionReviewer::class)->approve($submission, User::factory()->admin()->create(), null);
}

test('el prólogo lo ve cualquiera, aunque no haya empezado ningún curso', function () {
    $this->actingAs(User::factory()->create())->get(route('student.chronicles'))
        ->assertOk()
        ->assertSee('data-test="chronicle-prologue"', false)
        ->assertSee('Se llega aprendiendo');
});

test('una página se abre al completar su nodo; antes se ve en silueta y sin su texto', function () {
    $book = (new Chronicles($this->student))->book($this->made['course']);
    $pages = collect($book)->flatMap(fn ($chapter) => $chapter['pages']);
    $root = $pages->firstWhere('node_id', $this->made['root']->id);
    $topic = $pages->firstWhere('node_id', $this->made['topic1']->id);

    expect($root['unlocked'])->toBeFalse()->and($root['html'])->toBeNull()
        ->and($root['missing'])->toContain('Completá «Clase 0»')
        ->and($topic['title'])->toBe('Una página por descubrir')
        ->and($topic['html'])->toBeNull();

    $html = $this->actingAs($this->student)->get(route('student.chronicles', ['libro' => $this->made['course']->slug]))->assertOk()->getContent();
    expect($html)->toContain('data-test="chronicle-locked"')
        ->and($html)->not->toContain('SECRETO')
        ->and($html)->not->toContain('Tema oculto')
        ->and($html)->not->toContain('Despertás en un valle');

    approveRoot($this->made, $this->student);
    $this->actingAs($this->student)->get(route('student.chronicles', ['libro' => $this->made['course']->slug]))
        ->assertSee('Despertás en un valle')
        ->assertDontSee('SECRETO');
});

test('el menú late con las páginas nuevas y se calma al abrir el libro', function () {
    approveRoot($this->made, $this->student);

    $this->actingAs($this->student)->get(route('student.worlds'))->assertSee('data-test="chronicles-new"', false);
    $this->actingAs($this->student)->get(route('student.chronicles'))->assertOk();
    $this->actingAs($this->student)->get(route('student.worlds'))->assertDontSee('data-test="chronicles-new"', false);

    expect((new Chronicles($this->student->fresh()))->newCount())->toBe(0);
});

test('el epílogo se lee al terminar el curso', function () {
    GlossaryTerm::create(['key' => 'story.course_completed', 'course_id' => $this->made['course']->id, 'singular' => '¡Terminaste!', 'plural' => '¡Terminaste!', 'gender' => 'm', 'lore' => 'El Valle es tuyo.']);
    Glossary::flush($this->made['course']->id);
    $epilogue = fn () => collect((new Chronicles($this->student))->book($this->made['course']))->last()['pages'][0];
    expect($epilogue()['kind'])->toBe('epilogue')->and($epilogue()['unlocked'])->toBeFalse();

    CourseCompletion::create(['user_id' => $this->student->id, 'course_id' => $this->made['course']->id, 'completed_at' => now(), 'days_taken' => 10]);
    expect($epilogue()['unlocked'])->toBeTrue()->and($epilogue()['html'])->not->toBeEmpty();
});

test('el administrador no entra a Mis Crónicas de alumno', function () {
    $this->actingAs(User::factory()->admin()->create())->get(route('student.chronicles'))->assertForbidden();
});
