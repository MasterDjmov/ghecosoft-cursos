<?php

use App\Livewire\Admin\Nodes\Edit;
use App\Models\Practice;
use App\Models\User;
use App\Services\CourseImporter;
use App\Support\CourseImport\CourseFileParser;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Facades\Storage;
use Livewire\Livewire;

/*
 * «Así tiene que quedar» (D77): las capturas de la página resuelta (celular y compu) de una práctica. Se
 * importan desde la carpeta del curso, se suben desde el editor y el alumno las ve para comparar.
 */

beforeEach(function () {
    Storage::fake('public');
    $this->dir = storage_path('framework/testing/curso-'.uniqid());
    File::ensureDirectoryExists($this->dir.'/capturas');
    $this->png = fn (int $w, int $h) => UploadedFile::fake()->image('x.png', $w, $h)->getContent();
});

afterEach(fn () => File::deleteDirectory($this->dir));

/** El curso de ejemplo con «Cómo debe quedar» en la misión R00-N01-M2. */
function courseWithReferences(string $references): array
{
    $content = file_get_contents(base_path('tests/Fixtures/curso-ejemplo.md'));
    $mission = strpos($content, '### Misión R00-N01-M2');
    $at = strpos($content, '#### Consigna', $mission);
    $content = substr($content, 0, $at)."#### Cómo debe quedar\n\n{$references}\n\n".substr($content, $at);

    return [['name' => 'curso.md', 'content' => $content]];
}

test('el formato acepta una línea por pantalla, con o sin acentos ni comillas', function () {
    expect(CourseFileParser::parseReferences("celular: capturas/a.webp\n- Compu: `capturas/b.png`"))
        ->toBe(['mobile' => 'capturas/a.webp', 'desktop' => 'capturas/b.png'])
        ->and(CourseFileParser::parseReferences("Móvil: m.png\notra cosa"))->toBe(['mobile' => 'm.png']);
});

test('el comando copia las capturas de la carpeta del curso, una sola vez aunque se reimporte', function () {
    file_put_contents($this->dir.'/capturas/m.png', ($this->png)(390, 900));
    file_put_contents($this->dir.'/capturas/d.png', ($this->png)(1280, 800));
    $files = courseWithReferences("celular: capturas/m.png\ncompu: capturas/d.png");

    $report = app(CourseImporter::class)->import($files, dryRun: false, assetsDir: $this->dir);
    expect($report->ok())->toBeTrue();

    $practice = Practice::where('code', 'R00-N01-M2')->first();
    expect($practice->reference_mobile)->toStartWith('practice-refs/')
        ->and(Storage::disk('public')->exists($practice->reference_mobile))->toBeTrue()
        ->and(Storage::disk('public')->exists($practice->reference_desktop))->toBeTrue();

    app(CourseImporter::class)->import($files, dryRun: false, assetsDir: $this->dir);
    expect(Storage::disk('public')->files('practice-refs'))->toHaveCount(2);
});

test('una captura que no existe, que no es imagen o que está fuera de la carpeta no se copia', function () {
    file_put_contents($this->dir.'/capturas/falsa.png', '<?php echo "no soy una imagen";');
    $files = courseWithReferences("celular: capturas/falsa.png\ncompu: ../../../../.env");

    $report = app(CourseImporter::class)->import($files, dryRun: false, assetsDir: $this->dir);
    $warnings = implode(' ', $report->warnings);

    expect($warnings)->toContain('no es una imagen válida')
        ->and($warnings)->toMatch('/fuera de la carpeta del curso|no se encuentra/')
        ->and(Storage::disk('public')->files('practice-refs'))->toBeEmpty();
});

test('desde la web (solo los .md) avisa y deja las capturas que tenía', function () {
    $files = courseWithReferences('celular: capturas/m.png');
    app(CourseImporter::class)->import($files, dryRun: false);
    Practice::where('code', 'R00-N01-M2')->update(['reference_mobile' => 'practice-refs/vieja.png']);

    $report = app(CourseImporter::class)->import($files, dryRun: false);

    expect(implode(' ', $report->warnings))->toContain('desde la web no se suben')
        ->and(Practice::where('code', 'R00-N01-M2')->value('reference_mobile'))->toBe('practice-refs/vieja.png');
});

test('el administrador las sube y las quita desde el editor de la práctica', function () {
    $this->actingAs(User::factory()->admin()->create());
    ['course' => $course, 'topic1' => $topic1] = makeCourse(['language' => 'html']);
    $practice = $topic1->practices()->first();

    Livewire::test(Edit::class, ['course' => $course, 'node' => $topic1])
        ->call('editPractice', $practice->id)
        ->set('practiceRefMobile', UploadedFile::fake()->image('celular.png', 390, 900))
        ->call('savePractice')
        ->assertHasNoErrors();
    expect($practice->fresh()->reference_mobile)->toStartWith('practice-refs/');

    Livewire::test(Edit::class, ['course' => $course, 'node' => $topic1])
        ->call('editPractice', $practice->id)
        ->set('practiceRefRemove', ['mobile'])
        ->call('savePractice');
    expect($practice->fresh()->reference_mobile)->toBeNull();
});

test('el alumno ve «Así tiene que quedar» y puede comparar en la vista previa', function () {
    $made = makeCourse(['language' => 'html']);
    $student = studentWithRootOpen($made);
    $made['root']->practices()->first()->update(['reference_mobile' => 'practice-refs/celular.png', 'reference_desktop' => 'practice-refs/compu.png']);

    $this->actingAs($student)->get(route('student.node', [$made['course'], $made['root']]))
        ->assertOk()
        ->assertSee('data-test="expected-references"', false)
        ->assertSee('practice-refs/celular.png', false)
        ->assertSee('data-test="compare-reference"', false);
});
