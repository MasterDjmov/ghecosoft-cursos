<?php

use App\Livewire\Admin\Glossary as GlossaryAdmin;
use App\Models\GlossaryTerm;
use App\Models\User;
use App\Support\Glossary;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Facades\Storage;
use Livewire\Livewire;

/** Retratos del Diccionario: uno general para todos los cursos que usan el mismo personaje. */
test('un curso sin retrato propio usa el general si es el mismo personaje, y no si lo renombró', function () {
    $course = makeCourse()['course'];
    GlossaryTerm::create(['key' => 'beast.slime', 'course_id' => null, 'singular' => 'slime', 'plural' => 'slimes', 'gender' => 'm', 'icon_path' => 'glossary/slime.jpg']);
    GlossaryTerm::create(['key' => 'mentor.name', 'course_id' => null, 'singular' => 'el profe', 'plural' => 'el profe', 'gender' => 'm', 'icon_path' => 'glossary/profe.jpg']);
    GlossaryTerm::create(['key' => 'beast.slime', 'course_id' => $course->id, 'singular' => 'Slime', 'plural' => 'slimes', 'gender' => 'm']);
    GlossaryTerm::create(['key' => 'mentor.name', 'course_id' => $course->id, 'singular' => 'Ofidia', 'plural' => 'Ofidia', 'gender' => 'f']);
    Glossary::flush(null);
    Glossary::flush($course->id);

    expect(app(Glossary::class)->resolve('beast.slime', $course)['icon_path'])->toBe('glossary/slime.jpg')
        ->and(app(Glossary::class)->resolve('mentor.name', $course)['icon_path'])->toBeNull();
});

test('app:glossary-portraits carga los retratos por el nombre del archivo y saltea lo que no reconoce', function () {
    Storage::fake('public');
    $dir = storage_path('framework/testing/retratos-'.uniqid());
    File::ensureDirectoryExists($dir);
    $png = base64_decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=');
    file_put_contents($dir.'/personaje_mia.png', $png);
    file_put_contents($dir.'/troll.png', $png);
    file_put_contents($dir.'/vacaciones.png', $png);

    $this->artisan('app:glossary-portraits', ['path' => $dir])->assertSuccessful();
    expect(GlossaryTerm::whereNull('course_id')->whereNotNull('icon_path')->count())->toBe(0);

    $this->artisan('app:glossary-portraits', ['path' => $dir, '--apply' => true])->expectsOutputToContain('no lo reconozco')->assertSuccessful();
    $mia = GlossaryTerm::where('key', 'companion.theory')->whereNull('course_id')->first();
    expect($mia->singular)->toBe('Mia')
        ->and(Storage::disk('public')->exists($mia->icon_path))->toBeTrue()
        ->and(GlossaryTerm::where('key', 'beast.troll')->whereNull('course_id')->value('icon_path'))->not->toBeNull();

    File::deleteDirectory($dir);
});

test('el tamaño de los retratos se elige en el Diccionario y se usa en los nodos', function () {
    $data = makeCourse();
    $student = studentWithRootOpen($data);
    $data['root']->update(['content' => 'Teoría', 'common_errors' => 'Errores', 'beast_key' => 'beast.slime']);
    GlossaryTerm::create(['key' => 'companion.theory', 'course_id' => null, 'singular' => 'Mia', 'plural' => 'Mia', 'gender' => 'f', 'icon_path' => 'glossary/mia.jpg']);
    GlossaryTerm::create(['key' => 'beast.slime', 'course_id' => null, 'singular' => 'slime', 'plural' => 'slimes', 'gender' => 'm', 'icon_path' => 'glossary/slime.jpg']);
    Glossary::flush(null);

    $node = fn () => $this->actingAs($student)->get(route('student.node', [$data['course'], $data['root']]));
    $node()->assertSee('width: 48px', false)->assertSee('width: 80px', false);

    $admin = User::factory()->admin()->create();
    Livewire::actingAs($admin)->test(GlossaryAdmin::class)
        ->assertSee('Tamaño de los retratos')
        ->set('companionSize', 300)->call('savePortraitSizes')->assertHasErrors('companionSize')
        ->set('companionSize', 64)->set('beastSize', 120)->call('savePortraitSizes')->assertHasNoErrors();

    $node()->assertSee('width: 64px', false)->assertSee('width: 120px', false);
});

test('el Diccionario general lista los personajes propios de cada curso y abre su edición en ese curso', function () {
    $course = makeCourse()['course'];
    GlossaryTerm::create(['key' => 'mentor.name', 'course_id' => $course->id, 'singular' => 'Ofidia', 'plural' => 'Ofidia', 'gender' => 'f']);
    // El mismo personaje que el general (toma su retrato): no hace falta listarlo.
    GlossaryTerm::create(['key' => 'beast.slime', 'course_id' => $course->id, 'singular' => 'slime', 'plural' => 'slimes', 'gender' => 'm']);

    Livewire::actingAs(User::factory()->admin()->create())
        ->test(GlossaryAdmin::class)
        ->assertSee('data-test="course-characters"', false)
        ->assertSee('Ofidia')
        ->assertDontSee("editIn({$course->id}, 'beast.slime')", false)
        ->call('editIn', $course->id, 'mentor.name')
        ->assertSet('scope', (string) $course->id)
        ->assertSet('singular', 'Ofidia');
});

test('la portada suma los personajes propios de los cursos publicados que tienen retrato', function () {
    $course = makeCourse()['course'];
    $course->update(['is_published' => true]);
    GlossaryTerm::create(['key' => 'mentor.name', 'course_id' => $course->id, 'singular' => 'Ofidia', 'plural' => 'Ofidia', 'gender' => 'f', 'icon_path' => 'glossary/ofidia.jpg', 'short_description' => 'Serpiente sabia.']);
    GlossaryTerm::create(['key' => 'companion.theory', 'course_id' => $course->id, 'singular' => 'Sin Foto', 'plural' => 'Sin Foto', 'gender' => 'f']);

    $this->get('/')->assertOk()->assertSee('Ofidia')->assertSee('glossary/ofidia.jpg', false)->assertSee('Serpiente sabia.')->assertDontSee('Sin Foto');
});
