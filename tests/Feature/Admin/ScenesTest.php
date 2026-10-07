<?php

use App\Livewire\Admin\Scenes;
use App\Models\User;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Livewire\Livewire;

/*
 * Historia → Escenas (D88): las imágenes de las micro-misiones por curso, con su ID, el pedido y la subida.
 */

function courseWithStep(): array
{
    $made = makeCourse();
    $step = $made['root']->steps()->create([
        'code' => 'R00-N01-P1', 'title' => 'El pergamino habla', 'position' => 1, 'expected_output' => 'Hola',
        'place' => 'La orilla del río', 'image_prompt' => '- Mia en la orilla del río.',
    ]);

    return [...$made, 'step' => $step];
}

test('el administrador ve las micro-misiones con su ID, su pedido y si falta la imagen', function () {
    ['course' => $course] = courseWithStep();

    $this->actingAs(User::factory()->admin()->create())->get(route('admin.scenes', ['curso' => $course->slug]))
        ->assertOk()
        ->assertSee('r00-n01-p1')
        ->assertSee('Mia en la orilla del río.')
        ->assertSee('Falta la imagen')
        ->assertSee('data-test="copy-prompt"', false);
});

test('sube la imagen de una micro-misión y la puede quitar', function () {
    Storage::fake('public');
    ['course' => $course, 'step' => $step] = courseWithStep();

    Livewire::actingAs(User::factory()->admin()->create())
        ->test(Scenes::class, ['courseSlug' => $course->slug])
        ->set("uploads.{$step->id}", UploadedFile::fake()->image('escena.png', 1376, 768))
        ->assertHasNoErrors();

    $path = $step->fresh()->image_path;
    expect($path)->toStartWith('practice-refs/');
    Storage::disk('public')->assertExists($path);

    Livewire::actingAs(User::factory()->admin()->create())
        ->test(Scenes::class, ['courseSlug' => $course->slug])
        ->call('removeImage', $step->id);
    expect($step->fresh()->image_path)->toBeNull();
});

test('no acepta archivos que no son imágenes', function () {
    ['course' => $course, 'step' => $step] = courseWithStep();

    Livewire::actingAs(User::factory()->admin()->create())
        ->test(Scenes::class, ['courseSlug' => $course->slug])
        ->set("uploads.{$step->id}", UploadedFile::fake()->create('escena.php', 5, 'text/x-php'))
        ->assertHasErrors("uploads.{$step->id}");
    expect($step->fresh()->image_path)->toBeNull();
});

test('el docente no entra a Escenas', function () {
    $this->actingAs(User::factory()->teacher()->create())->get(route('admin.scenes'))->assertRedirect();
});
