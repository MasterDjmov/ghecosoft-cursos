<?php

use App\Livewire\Admin\Nodes\Edit;
use App\Models\Badge;
use App\Models\NodeResource;
use App\Models\User;
use App\Services\NodeUnlocker;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Livewire\Livewire;

beforeEach(function () {
    $this->admin = User::factory()->admin()->create();
    $this->actingAs($this->admin);
});

test('"+ Nueva hoja" agrega una práctica al final del nodo', function () {
    ['course' => $course, 'topic1' => $topic1] = makeCourse();

    Livewire::test(Edit::class, ['course' => $course, 'node' => $topic1])
        ->call('newPractice')
        ->set('practiceTitle', 'Misión 3')
        ->set('practiceInstructions', 'Mostrá tu nombre.')
        ->set('practiceRequired', false)
        ->set('practiceMode', 'both')
        ->set('practiceExtensions', 'PY, txt')
        ->set('practiceCoins', 4)
        ->set('practiceXp', 20)
        ->call('savePractice')
        ->assertHasNoErrors();

    $practice = $topic1->practices()->reorder()->latest('id')->first();

    expect($practice->title)->toBe('Misión 3')
        ->and($practice->is_required)->toBeFalse()
        ->and($practice->allowed_extensions)->toBe('py,txt')
        ->and($practice->coin_reward)->toBe(4)
        ->and($practice->position)->toBe($topic1->practices()->max('position'));
});

test('llegar con ?hoja=nueva abre las hojas', function () {
    ['course' => $course, 'topic1' => $topic1] = makeCourse();

    Livewire::withQueryParams(['hoja' => 'nueva'])
        ->test(Edit::class, ['course' => $course, 'node' => $topic1])
        ->assertSet('initialTab', 'practices')
        ->assertSet('practiceId', null);
});

test('guardar el nodo: un jefe guarda su insignia y el contenido se previsualiza sin HTML crudo', function () {
    ['course' => $course, 'root' => $root, 'topic1' => $topic1] = makeCourse();
    $badge = Badge::create(['code' => 'jefe', 'name' => 'Jefe vencido']);

    Livewire::test(Edit::class, ['course' => $course, 'node' => $topic1])
        ->set('type', 'boss')
        ->set('badge_id', $badge->id)
        ->set('content', "## Hola\n\n<script>alert(1)</script>")
        ->set('example_code', 'print(1)')
        ->call('save')
        ->assertHasNoErrors()
        ->assertSeeHtml('<h2>Hola</h2>')
        ->assertDontSeeHtml('<script>alert(1)</script>');

    $topic1->refresh();
    expect($topic1->badge_id)->toBe($badge->id)
        ->and($topic1->example_language)->toBe('python');
});

test('el editor rechaza un requisito que forma un ciclo', function () {
    ['course' => $course, 'topic1' => $topic1, 'topic2' => $topic2] = makeCourse();

    Livewire::test(Edit::class, ['course' => $course, 'node' => $topic1])
        ->set('parent_id', $topic2->id)
        ->call('save');

    expect($topic1->fresh()->parent_id)->not->toBe($topic2->id);
});

test('ordenar hojas por arrastre', function () {
    ['course' => $course, 'topic1' => $topic1] = makeCourse();
    [$first, $second, $third] = $topic1->practices()->get()->all();

    Livewire::test(Edit::class, ['course' => $course, 'node' => $topic1])->call('sortPractice', $third->id, 0);

    expect($topic1->practices()->pluck('id')->all())->toBe([$third->id, $first->id, $second->id]);
});

describe('recursos', function () {
    beforeEach(fn () => Storage::fake('local'));

    test('un archivo va al disco privado con nombre UUID', function () {
        ['course' => $course, 'root' => $root] = makeCourse();

        Livewire::test(Edit::class, ['course' => $course, 'node' => $root])
            ->set('resourceType', 'file')
            ->set('resourceTitle', 'Apunte')
            ->set('resourceFile', UploadedFile::fake()->createWithContent('apunte clase 0.pdf', "%PDF-1.4\n%%EOF\n"))
            ->call('addResource')
            ->assertHasNoErrors();

        $resource = NodeResource::firstOrFail();
        expect($resource->original_name)->toBe('apunte clase 0.pdf')
            ->and($resource->file_path)->toMatch('/^resources\/[0-9a-f-]{36}\.pdf$/');
        Storage::disk('local')->assertExists($resource->file_path);
    });

    test('no se aceptan extensiones fuera de la lista', function () {
        ['course' => $course, 'root' => $root] = makeCourse();

        Livewire::test(Edit::class, ['course' => $course, 'node' => $root])
            ->set('resourceType', 'file')
            ->set('resourceTitle', 'Script')
            ->set('resourceFile', UploadedFile::fake()->create('shell.php', 1))
            ->call('addResource')
            ->assertHasErrors('resourceFile');
    });

    test('solo descarga el recurso quien abrió el nodo (y el docente)', function () {
        ['course' => $course, 'root' => $root] = makeCourse();
        Storage::disk('local')->put('resources/x.pdf', 'PDF');
        $resource = $root->resources()->create(['type' => 'file', 'title' => 'Apunte', 'file_path' => 'resources/x.pdf', 'original_name' => 'apunte.pdf']);

        $this->get(route('files.resource', $resource))->assertOk()->assertDownload('apunte.pdf');

        $student = enrolledStudent($course);
        $this->actingAs($student)->get(route('files.resource', $resource))->assertForbidden();

        app(NodeUnlocker::class)->unlock($student, $root);
        $this->actingAs($student)->get(route('files.resource', $resource))->assertOk();

        auth()->logout();
        $this->get(route('files.resource', $resource))->assertRedirect(route('login'));
    });
});

test('tocar una hoja en el árbol dibujado abre esa hoja para editar', function () {
    ['course' => $course, 'topic1' => $topic1] = makeCourse();
    $practice = $topic1->practices()->first();

    Livewire::withQueryParams(['hoja' => (string) $practice->id])
        ->test(Edit::class, ['course' => $course, 'node' => $topic1])
        ->assertSet('initialTab', 'practices')
        ->assertSet('practiceId', $practice->id)
        ->assertSet('practiceTitle', $practice->title);
});
