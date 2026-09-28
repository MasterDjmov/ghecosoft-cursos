<?php

use App\Livewire\Admin\Nodes\Edit;
use App\Livewire\Settings\Privacy;
use App\Livewire\Student\CourseDetail;
use App\Livewire\Student\PracticeCard;
use App\Models\User;
use App\Rules\SafeUpload;
use App\Services\CourseImporter;
use App\Services\NodeUnlocker;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Livewire\Livewire;

const FAKE_PDF = "%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF\n";
const FAKE_EXE = "MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xFF\xFF\x00\x00This program cannot be run in DOS mode";

beforeEach(function () {
    Storage::fake('local');
    $this->data = makeCourse();
    $this->student = enrolledStudent($this->data['course']);
    app(NodeUnlocker::class)->unlock($this->student, $this->data['root']);
    $this->practice = $this->data['root']->practices()->first();
    $this->practice->update(['submission_mode' => 'file', 'allowed_extensions' => 'py,txt,pdf,zip']);
});

function submitFile(UploadedFile $file)
{
    return Livewire::actingAs(test()->student)->test(PracticeCard::class, ['practice' => test()->practice])
        ->set('file', $file)
        ->call('submit');
}

test('una entrega tiene que ser lo que dice su extensión', function () {
    submitFile(UploadedFile::fake()->createWithContent('tarea.pdf', FAKE_EXE))->assertHasErrors('file');
    submitFile(UploadedFile::fake()->createWithContent('tarea.zip', 'no soy un zip'))->assertHasErrors('file');
    submitFile(UploadedFile::fake()->createWithContent('tarea.py', FAKE_EXE))->assertHasErrors('file');

    submitFile(UploadedFile::fake()->createWithContent('tarea.pdf', FAKE_PDF))->assertHasNoErrors();
    submitFile(UploadedFile::fake()->createWithContent('tarea.py', "print('hola')\n"))->assertHasNoErrors();
});

test('nunca se aceptan archivos del servidor ni ejecutables, aunque vengan disfrazados', function () {
    submitFile(UploadedFile::fake()->createWithContent('tarea.php.txt', '<?php system($_GET["c"]);'))->assertHasErrors('file');

    expect(SafeUpload::isBlocked('.htaccess'))->toBeTrue()
        ->and(SafeUpload::isBlocked('virus.EXE'))->toBeTrue()
        ->and(SafeUpload::isBlocked('juego.py'))->toBeFalse();
});

test('el docente no puede habilitar entregas peligrosas, ni a mano ni importando', function () {
    $this->actingAs(User::factory()->admin()->create());

    Livewire::test(Edit::class, ['course' => $this->data['course'], 'node' => $this->data['root']])
        ->call('editPractice', $this->practice->id)
        ->set('practiceMode', 'file')
        ->set('practiceExtensions', 'py, php')
        ->call('savePractice')
        ->assertHasErrors('practiceExtensions');

    $course = preg_replace('/entrega: codigo/', "entrega: archivo\nextensiones: py, exe", file_get_contents(base_path('tests/Fixtures/curso-ejemplo.md')), 1);
    $report = app(CourseImporter::class)->import([['name' => 'curso.md', 'content' => $course]], dryRun: true)->toArray();

    expect(collect($report['errors'])->implode(' '))->toContain('no se aceptan entregas exe');
});

test('comprobantes y autorizaciones: la foto o el PDF tienen que ser de verdad', function () {
    $course = $this->data['course'];
    $newcomer = User::factory()->create();

    Livewire::actingAs($newcomer)->test(CourseDetail::class, ['course' => $course])
        ->set('receipt', UploadedFile::fake()->createWithContent('pago.pdf', FAKE_EXE))
        ->call('sendReceipt')
        ->assertHasErrors('receipt');

    Livewire::actingAs($newcomer)->test(Privacy::class)
        ->set('authorization', UploadedFile::fake()->createWithContent('nota.jpg', '<html><script>alert(1)</script></html>'))
        ->call('uploadAuthorization')
        ->assertHasErrors('authorization');

    Livewire::actingAs($newcomer)->test(CourseDetail::class, ['course' => $course])
        ->set('receipt', UploadedFile::fake()->createWithContent('pago.pdf', FAKE_PDF))
        ->call('sendReceipt')
        ->assertHasNoErrors();
});
