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

test('la imagen chica de un ítem se arma la primera vez y, sin imagen, no hay ninguna', function () {
    Storage::fake('public');
    $jpg = imagecreatetruecolor(600, 600);
    ob_start();
    imagejpeg($jpg);
    Storage::disk('public')->put('practice-refs/grande.jpg', ob_get_clean());
    $item = Item::create(['code' => 'vara', 'name' => 'Vara', 'kind' => 'weapon', 'image_path' => 'practice-refs/grande.jpg']);

    expect($item->thumbUrl())->toEndWith('item-thumbs/grande.webp')
        ->and(getimagesize(Storage::disk('public')->path('item-thumbs/grande.webp'))[0])->toBe(Item::THUMB_PX)
        ->and(Item::create(['code' => 'nada', 'name' => 'Nada', 'kind' => 'weapon'])->thumbUrl())->toBeNull();
});

test('app:item-images crea el ítem de historia de una micro-misión para ponerle la imagen antes de que alguien lo gane', function () {
    Storage::fake('public');
    ['course' => $course, 'root' => $root] = makeCourse(['slug' => 'arcadia']);
    \App\Models\NodeStep::create(['node_id' => $root->id, 'code' => 'R00-N01-P1', 'position' => 1, 'title' => 'Revancha', 'expected_output' => 'ok', 'solution' => 'ok', 'xp_reward' => 10, 'coin_reward' => 0, 'item' => 'Fotograma Congelado']);
    $dir = storage_path('framework/testing/items-'.uniqid());
    File::ensureDirectoryExists($dir);
    file_put_contents($dir.'/arcadia-fotograma-congelado.png', base64_decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='));

    $this->artisan('app:item-images', ['path' => $dir])->expectsOutputToContain('ítem de historia')->assertSuccessful();
    expect(Item::where('code', 'arcadia-fotograma-congelado')->exists())->toBeFalse();

    $this->artisan('app:item-images', ['path' => $dir, '--apply' => true])->assertSuccessful();
    $item = Item::where('code', 'arcadia-fotograma-congelado')->first();
    expect($item->name)->toBe('Fotograma Congelado')
        ->and($item->course_id)->toBe($course->id)
        ->and(Storage::disk('public')->exists($item->image_path))->toBeTrue();

    File::deleteDirectory($dir);
});
