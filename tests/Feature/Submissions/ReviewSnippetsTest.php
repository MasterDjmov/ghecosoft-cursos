<?php

use App\Livewire\Admin\Submissions\Show;
use App\Models\ReviewSnippet;
use App\Models\User;
use App\Services\PracticeSubmitter;
use Livewire\Livewire;

/* D73: los comentarios guardados de cada docente, para insertarlos con un clic al corregir. */

beforeEach(function () {
    $this->admin = User::factory()->admin()->create();
    $this->made = makeCourse();
    $this->student = studentWithRootOpen($this->made);
    $this->submission = app(PracticeSubmitter::class)->submit($this->student, $this->made['root']->practices()->first(), 'print("hola")');
});

test('guarda el comentario escrito, para este curso o para todos, sin repetirlo', function () {
    $component = Livewire::actingAs($this->admin)->test(Show::class, ['submission' => $this->submission])
        ->assertDontSee('data-test="review-snippets"', false)
        ->set('comment', '  Bien, pero revisá los nombres de las variables.  ')
        ->call('saveSnippet')
        ->call('saveSnippet')
        ->set('comment', 'Probá con números negativos.')
        ->set('snippetForAll', true)
        ->call('saveSnippet')
        ->assertSee('data-test="review-snippets"', false)
        ->assertSee('Probá con números negativos.');

    $snippets = ReviewSnippet::orderBy('position')->get();
    expect($snippets->pluck('body')->all())->toBe(['Bien, pero revisá los nombres de las variables.', 'Probá con números negativos.'])
        ->and($snippets[0]->course_id)->toBe($this->made['course']->id)
        ->and($snippets[1]->course_id)->toBeNull()
        ->and($snippets->pluck('user_id')->unique()->all())->toBe([$this->admin->id]);

    // Vacío no se guarda.
    $component->set('comment', '')->call('saveSnippet')->assertHasErrors('comment');
});

test('cada docente ve y borra solo los suyos, y los de otro curso no salen', function () {
    $other = User::factory()->admin()->create();
    $mine = ReviewSnippet::create(['user_id' => $this->admin->id, 'course_id' => null, 'body' => 'El mío para todos']);
    $foreign = ReviewSnippet::create(['user_id' => $other->id, 'course_id' => null, 'body' => 'El de otro docente']);
    ReviewSnippet::create(['user_id' => $this->admin->id, 'course_id' => makeCourse()['course']->id, 'body' => 'De otro curso']);

    Livewire::actingAs($this->admin)->test(Show::class, ['submission' => $this->submission])
        ->assertSee('El mío para todos')
        ->assertDontSee('El de otro docente')
        ->assertDontSee('De otro curso')
        ->call('deleteSnippet', $foreign->id)
        ->call('deleteSnippet', $mine->id)
        ->assertDontSee('El mío para todos');

    expect(ReviewSnippet::find($foreign->id))->not->toBeNull()
        ->and(ReviewSnippet::find($mine->id))->toBeNull();
});
