<?php

use App\Livewire\Admin\Story;
use App\Models\StoryFragment;
use App\Models\User;
use App\Services\PracticeSubmitter;
use App\Services\SubmissionReviewer;
use App\Support\Chronicles;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Livewire\Livewire;

/*
 * La sala de guion de Mis Crónicas (D80, etapa 2): el administrador lee el libro con todo abierto, ve dónde
 * falta crónica y cuelga fragmentos (texto e imagen) que el alumno lee al llegar a ese lugar.
 */

beforeEach(function () {
    Storage::fake('public');
    $this->admin = User::factory()->admin()->create();
    $this->made = makeCourse();
    $this->made['root']->update(['chronicle' => 'Despertás en un valle desconocido.']);
    $this->student = studentWithRootOpen($this->made);
});

test('con todo abierto se lee el libro entero y se marca dónde falta crónica', function () {
    Livewire::actingAs($this->admin)->test(Story::class, ['courseSlug' => $this->made['course']->slug])
        ->assertSee('Despertás en un valle desconocido.')
        ->assertSee('data-test="chronicle-empty"', false)
        ->assertSee('Tema 1');
});

test('el administrador cuelga un fragmento con imagen en un nodo; el alumno lo lee al completarlo', function () {
    Livewire::actingAs($this->admin)->test(Story::class, ['courseSlug' => $this->made['course']->slug])
        ->call('newFragment', 'node_completed', $this->made['root']->id)
        ->set('title', 'Una carta de Ferrum')
        ->set('body', 'El plomo de tu primer vitral, {heroe}, salió de mi fragua.')
        ->set('image', UploadedFile::fake()->image('carta.png', 600, 400))
        ->call('saveFragment')
        ->assertHasNoErrors();

    $fragment = StoryFragment::first();
    expect($fragment->node_id)->toBe($this->made['root']->id)
        ->and(Storage::disk('public')->exists($fragment->image_path))->toBeTrue();

    $url = route('student.chronicles', ['libro' => $this->made['course']->slug]);
    $this->actingAs($this->student)->get($url)->assertDontSee('salió de mi fragua')->assertDontSee($fragment->image_path);

    $practice = $this->made['root']->practices()->first();
    app(SubmissionReviewer::class)->approve(app(PracticeSubmitter::class)->submit($this->student, $practice, 'print(1)'), $this->admin, null);

    $this->actingAs($this->student)->get($url)
        ->assertSee('Una carta de Ferrum')
        ->assertSee('salió de mi fragua')
        ->assertSee($fragment->image_path, false);
});

test('«Ver como» muestra el libro de un alumno, con lo bloqueado en silueta y sin editar', function () {
    $this->made['topic1']->update(['chronicle' => 'SECRETO del tema.']);

    Livewire::actingAs($this->admin)->test(Story::class, ['courseSlug' => $this->made['course']->slug, 'viewAs' => (string) $this->student->id])
        ->assertSee($this->student->fullName())
        ->assertDontSee('SECRETO del tema.')
        ->assertDontSee('data-test="add-fragment-node"', false);
});

test('los fragmentos de una rama y del final se abren con ella', function () {
    StoryFragment::create(['course_id' => $this->made['course']->id, 'trigger' => 'course_completed', 'title' => 'Posdata', 'body' => 'Volvé cuando quieras.']);

    $last = collect((new Chronicles($this->student))->book($this->made['course']))->last();
    expect($last['title'])->toBe('Epílogo')
        ->and($last['pages'][0]['unlocked'])->toBeFalse()
        ->and($last['pages'][0]['html'])->toBeNull();
});

test('solo el administrador entra a la sala de guion', function () {
    $this->actingAs(User::factory()->teacher()->create())->get(route('admin.story'))->assertRedirect();
    $this->actingAs($this->student)->get(route('admin.story'))->assertRedirect();
    $this->actingAs($this->admin)->get(route('admin.story'))->assertOk()->assertSee('Se llega aprendiendo');
});
