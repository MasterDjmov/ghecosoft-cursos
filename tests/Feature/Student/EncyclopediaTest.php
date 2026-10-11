<?php

use App\Enums\ItemReason;
use App\Livewire\Student\Encyclopedia as Page;
use App\Models\Currency;
use App\Models\Item;
use App\Models\NodeUnlock;
use App\Models\User;
use App\Services\Inventory;
use App\Services\NodeUnlocker;
use App\Support\CharacterSheets;
use App\Support\Encyclopedia;
use App\Support\EncyclopediaItems;
use Livewire\Livewire;

/*
 * La Gran Enciclopedia del Código (D104): personajes y criaturas de todo el universo. Lo no descubierto va en
 * silueta con su pista, y su texto nunca sale del servidor. La ven todos los alumnos.
 */

beforeEach(function () {
    CharacterSheets::$file = tempnam(sys_get_temp_dir(), 'fichas');
    file_put_contents(CharacterSheets::$file, <<<'MD'
## 1. Los protagonistas
### Mia
- **Curso y rol:** Python. Protagonista.

## 2. Los guías (aparecen en todos los cursos)
### Gheco
- **Rol:** el guía de todos.

## El Valle de la Serpiente (Python)
### Tilo
- **Rol:** el vecino.
- **Frase:** «Secreto de Tilo.»
- **Primera aparición:** Python, Clase 0.

### Ninfa
- **Rol:** aparece más adelante.
- **Altura y contextura:** alta, solo para las imágenes.
- **Personalidad:** secreta, la de Ninfa ([python.md](python.md)).
- **Primera aparición:** Python, R01-N01.

### El Jefe Cristal (jefe de R01)
- **Rol:** el jefe de R01 de Python.
- **Qué es:** un cristal, secreto del jefe.
MD);
    $this->data = makeCourse();
    $this->data['root']->update(['code' => 'R00-N01']);
    $this->data['topic1']->update(['code' => 'R01-N01']);
    $this->data['topic2']->update(['code' => 'R01-N02', 'type' => 'boss', 'title' => 'Jefe: el Cristal']);
    $this->student = enrolledStudent($this->data['course']);
});

afterEach(function () {
    @unlink(CharacterSheets::$file);
    CharacterSheets::$file = null;
});

function entry(User $user, string $key): array
{
    return (new Encyclopedia($user))->entries()->firstWhere('key', $key);
}

test('lo no descubierto va sin su texto, con dónde aparece; protagonistas y guías, siempre', function () {
    expect(entry($this->student, 'mia')['discovered'])->toBeTrue()
        ->and(entry($this->student, 'gheco')['discovered'])->toBeTrue()
        ->and(entry($this->student, 'tilo'))->toMatchArray(['discovered' => false, 'fields' => [], 'section' => Encyclopedia::MASTERS])
        ->and(entry($this->student, 'tilo')['where'])->toBe('Python · «Clase 0»')
        ->and(entry($this->student, 'el-jefe-cristal'))->toMatchArray(['section' => Encyclopedia::BESTIARY, 'boss' => true, 'discovered' => false]);

    Livewire::actingAs($this->student)->test(Page::class)
        ->call('show', Encyclopedia::MASTERS)
        ->assertSee('Tilo')
        ->call('open', 'tilo')
        ->assertSee('data-test="entry-locked"', false)
        ->assertDontSee('Secreto de Tilo');
});

test('se descubre al abrir el nodo de su primera aparición, y solo con lo que es para el alumno', function () {
    app(NodeUnlocker::class)->unlock($this->student, $this->data['root']);

    expect(entry($this->student, 'tilo')['fields'])->toHaveKey('Frase')
        ->and(entry($this->student, 'ninfa')['discovered'])->toBeFalse();

    NodeUnlock::create(['user_id' => $this->student->id, 'node_id' => $this->data['topic1']->id, 'price_paid' => 0, 'unlocked_at' => now()]);
    $ninfa = entry($this->student, 'ninfa');
    expect($ninfa['discovered'])->toBeTrue()
        ->and($ninfa['fields'])->not->toHaveKey('Altura y contextura')
        ->and($ninfa['fields']['Personalidad'])->toBe('secreta, la de Ninfa.');

    Livewire::actingAs($this->student)->test(Page::class, ['section' => Encyclopedia::MASTERS])
        ->call('open', 'tilo')
        ->assertSee('Secreto de Tilo');
});

test('el jefe se descubre al llegar a su nodo y queda vencido al completarlo', function () {
    NodeUnlock::create(['user_id' => $this->student->id, 'node_id' => $this->data['topic2']->id, 'price_paid' => 0, 'unlocked_at' => now()]);

    // «Tema 2» no tiene prácticas obligatorias: abrirlo ya es completarlo.
    expect(entry($this->student, 'el-jefe-cristal'))->toMatchArray(['discovered' => true, 'defeated' => true])
        ->and(entry($this->student, 'el-jefe-cristal')['fields']['Qué es'])->toBe('un cristal, secreto del jefe.');
});

test('la ven todos los alumnos, también sin abono; los mundos sin publicar no aparecen', function () {
    $trial = User::factory()->create();
    $this->actingAs($trial)->get(route('student.encyclopedia'))->assertOk()->assertSee('data-test="encyclopedia-cover"', false);
    $this->actingAs($trial)->get(route('student.encyclopedia', ['seccion' => 'maestros']))->assertOk()->assertSee('Tilo');

    $this->data['course']->update(['is_published' => false]);
    expect((new Encyclopedia($trial))->entries()->pluck('key')->all())->toBe(['mia', 'gheco']);

    auth()->logout();
    $this->get(route('student.encyclopedia'))->assertRedirect(route('login'));
});

test('artefactos: dónde se consigue siempre; descripción y bonos, recién al tenerlo', function () {
    $course = $this->data['course'];
    $amulet = Item::create(['code' => 'amuleto-prueba', 'name' => 'Amuleto de Prueba', 'kind' => 'accessory', 'rarity' => 'rare',
        'course_id' => $course->id, 'defense' => 2, 'description' => 'Secreto del amuleto.', 'in_shop' => true, 'price' => 40, 'droppable' => true]);
    $this->data['root']->steps()->create(['code' => 'R00-N01-P1', 'title' => 'La prueba', 'position' => 1, 'item' => 'Amuleto de Prueba', 'expected_output' => 'x']);

    $entry = fn () => (new EncyclopediaItems($this->student))->artifacts()->firstWhere('key', 'item-amuleto-prueba');
    expect($entry())->toMatchArray(['discovered' => false, 'fields' => []])
        ->and($entry()['sources'])->toContain('Python · micro-misión «La prueba» («Clase 0»)')
        ->and(collect($entry()['sources'])->join(' '))->toContain('a 40 de oro')->toContain('Botín raro de las expediciones de Python');

    Livewire::actingAs($this->student)->test(Page::class, ['section' => 'artefactos'])
        ->call('open', 'item-amuleto-prueba')
        ->assertSee('data-test="entry-sources"', false)
        ->assertDontSee('Secreto del amuleto.');

    app(Inventory::class)->grant($this->student, $amulet, 1, ItemReason::StepReward, $amulet);
    expect($entry()['discovered'])->toBeTrue()
        ->and($entry()['fields'])->toMatchArray(['Bonos' => '+2 DEF', 'Qué es' => 'Secreto del amuleto.']);
});

test('monedas: la del curso se ve al inscribirse; el comodín y el oro, siempre', function () {
    $other = User::factory()->create();
    $coins = fn (User $user) => (new EncyclopediaItems($user))->coins()->keyBy('key');

    expect($coins($other)['coin-'.Currency::forCourse($this->data['course'])->code]['discovered'])->toBeFalse()
        ->and($coins($other)['coin-'.Currency::wildcard()->code]['discovered'])->toBeTrue()
        ->and($coins($this->student)['coin-'.Currency::forCourse($this->data['course'])->code]['fields']['Tenés'])->toStartWith('10 ');
});
