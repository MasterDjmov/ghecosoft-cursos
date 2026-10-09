<?php

use App\Models\Item;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Facades\Storage;

/** app:item-images: las imágenes de los ítems de una vez, por el código del ítem. */
test('app:item-images carga por el código, no pisa las que ya tienen imagen y saltea lo que no reconoce', function () {
    Storage::fake('public');
    $dir = storage_path('framework/testing/items-'.uniqid());
    File::ensureDirectoryExists($dir);
    $png = base64_decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=');
    file_put_contents($dir.'/vara.png', $png);
    file_put_contents($dir.'/tunica.png', $png);
    file_put_contents($dir.'/vacaciones.png', $png);
    file_put_contents($dir.'/falsa.png', 'esto no es una imagen');
    $vara = Item::create(['code' => 'vara', 'name' => 'Vara', 'kind' => 'weapon']);
    $tunica = Item::create(['code' => 'tunica', 'name' => 'Túnica', 'kind' => 'armor', 'image_path' => 'practice-refs/vieja.png']);
    $falsa = Item::create(['code' => 'falsa', 'name' => 'Falsa', 'kind' => 'weapon']);

    $this->artisan('app:item-images', ['path' => $dir])->assertSuccessful();
    expect($vara->fresh()->image_path)->toBeNull();

    $this->artisan('app:item-images', ['path' => $dir, '--apply' => true])
        ->expectsOutputToContain('no hay un ítem con ese código')
        ->expectsOutputToContain('ya tiene imagen')
        ->assertSuccessful();
    expect(Storage::disk('public')->exists($vara->fresh()->image_path))->toBeTrue()
        ->and($tunica->fresh()->image_path)->toBe('practice-refs/vieja.png')
        ->and($falsa->fresh()->image_path)->toBeNull();

    $this->artisan('app:item-images', ['path' => $dir, '--apply' => true, '--replace' => true])->assertSuccessful();
    expect($tunica->fresh()->image_path)->not->toBe('practice-refs/vieja.png');

    File::deleteDirectory($dir);
});
