<?php

use App\Models\CourseCompletion;
use App\Models\GlossaryTerm;
use App\Models\User;
use App\Services\PracticeSubmitter;
use App\Services\SubmissionReviewer;
use App\Support\CvData;
use App\Support\Glossary;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Facades\Storage;

/*
 * Mis Crónicas, etapa 3 (D80): el portal (una pieza del misterio por curso, al terminarlo), las Crónicas en
 * el CV y los personajes de cuerpo entero en las páginas.
 */

beforeEach(function () {
    Storage::fake('public');
    $this->made = makeCourse();
    $this->course = $this->made['course'];
    GlossaryTerm::create(['key' => 'story.portal_piece', 'course_id' => $this->course->id, 'singular' => 'Lo que vio Ofidia', 'plural' => 'Lo que vio Ofidia', 'gender' => 'f', 'lore' => 'SECRETO: un viajero con las manos manchadas de plomo.']);
    GlossaryTerm::create(['key' => 'mentor.name', 'course_id' => $this->course->id, 'singular' => 'Ofidia', 'plural' => 'Ofidia', 'gender' => 'f']);
    Glossary::flush($this->course->id);
    $this->student = studentWithRootOpen($this->made);
});

test('la pieza del portal se lee al terminar el curso; antes se ve sin su texto', function () {
    $url = route('student.chronicles', ['libro' => 'portal']);
    $this->actingAs($this->student)->get($url)
        ->assertOk()
        ->assertSee('Pieza 0 de 1')
        ->assertSee('para que Ofidia te cuente lo que sabe')
        ->assertDontSee('SECRETO');

    CourseCompletion::create(['user_id' => $this->student->id, 'course_id' => $this->course->id, 'completed_at' => now(), 'days_taken' => 20]);
    $this->actingAs($this->student)->get($url)
        ->assertSee('Pieza 1 de 1')
        ->assertSee('Lo que vio Ofidia')
        ->assertSee('SECRETO: un viajero');
});

test('el CV muestra las páginas desbloqueadas y las piezas del portal', function () {
    $this->made['root']->update(['chronicle' => 'Despertás en un valle.']);
    $practice = $this->made['root']->practices()->first();
    app(SubmissionReviewer::class)->approve(app(PracticeSubmitter::class)->submit($this->student, $practice, 'print(1)'), User::factory()->admin()->create(), null);

    $data = CvData::for($this->student->fresh());
    expect($data['chronicles'])->toMatchArray(['pieces' => 0, 'totalPieces' => 1])
        ->and($data['chronicles']['pages'])->toBeGreaterThan(0);
});

test('una página abierta muestra a quien habla de cuerpo entero', function () {
    $this->made['root']->update(['chronicle' => 'Despertás en un valle.']);
    GlossaryTerm::where('key', 'mentor.name')->where('course_id', $this->course->id)->update(['figure_path' => 'glossary/ofidia-entera.jpg']);
    Glossary::flush($this->course->id);
    $practice = $this->made['root']->practices()->first();
    app(SubmissionReviewer::class)->approve(app(PracticeSubmitter::class)->submit($this->student, $practice, 'print(1)'), User::factory()->admin()->create(), null);

    $this->actingAs($this->student)->get(route('student.chronicles', ['libro' => $this->course->slug]))
        ->assertSee('data-test="chronicle-figure"', false)
        ->assertSee('glossary/ofidia-entera.jpg', false);
});

test('app:glossary-portraits --figuras carga los cuerpos enteros, las líderes por su nombre', function () {
    $dir = storage_path('framework/testing/figuras-'.uniqid());
    File::ensureDirectoryExists($dir);
    $png = base64_decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=');
    file_put_contents("{$dir}/ofidia.png", $png);
    file_put_contents("{$dir}/bron.png", $png);

    $this->artisan('app:glossary-portraits', ['path' => $dir, '--figuras' => true, '--apply' => true])->assertSuccessful();

    expect(GlossaryTerm::where('key', 'mentor.name')->where('course_id', $this->course->id)->value('figure_path'))->not->toBeNull()
        ->and(GlossaryTerm::where('key', 'companion.uses')->whereNull('course_id')->value('figure_path'))->not->toBeNull()
        ->and(GlossaryTerm::where('key', 'mentor.name')->where('course_id', $this->course->id)->value('icon_path'))->toBeNull();
    File::deleteDirectory($dir);
});
