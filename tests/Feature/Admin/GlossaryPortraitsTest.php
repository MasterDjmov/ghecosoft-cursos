<?php

use App\Models\GlossaryTerm;
use App\Support\Glossary;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Facades\Storage;

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
