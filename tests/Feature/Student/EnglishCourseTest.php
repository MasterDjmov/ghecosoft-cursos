<?php

use App\Exceptions\NodeLocked;
use App\Livewire\Admin\Courses\Form as CourseForm;
use App\Livewire\Student\CourseDetail;
use App\Livewire\Student\CourseTree;
use App\Livewire\Student\Hero as HeroPage;
use App\Livewire\Student\Inventory as InventoryPage;
use App\Livewire\Student\NodeView;
use App\Livewire\Student\Shop as ShopPage;
use App\Models\Course;
use App\Models\Item;
use App\Models\Node;
use App\Models\NodeStep;
use App\Models\User;
use App\Services\CourseImporter;
use App\Services\Heroes;
use App\Services\NodeUnlocker;
use App\Services\StepCompleter;
use App\Services\TreeAccess;
use App\Support\CvData;
use App\Support\EnglishExercise;
use App\Support\TreeGraph;
use App\Support\UnlockMessages;
use Livewire\Livewire;

/*
 * Crónicas en Inglés (D106): un curso que se comprueba solo. Los episodios (nodos) se completan al superar sus
 * micro-misiones, se abren sin monedas, cuentan para el CV y se muestran como una biblioteca.
 */

function importEnglishPrimaria(): Course
{
    $files = collect(glob(base_path('cursos/ingles-primaria/*.md')))->sort()
        ->map(fn (string $file) => ['name' => basename($file), 'content' => file_get_contents($file)])
        ->values()->all();
    $report = app(CourseImporter::class)->import($files, dryRun: false);
    expect($report->errors)->toBe([]);

    $course = Course::where('slug', 'ingles-primaria')->firstOrFail();
    $course->update(['is_published' => true]);

    return $course->fresh();
}

/** Supera todas las micro-misiones de un episodio, como lo haría el navegador. */
function passEpisode($student, Node $node): void
{
    foreach ($node->steps()->get() as $step) {
        app(StepCompleter::class)->complete($student, $step, EnglishExercise::PASSED);
    }
}

test('el formato del ejercicio se arma y avisa lo que está mal', function () {
    $ok = EnglishExercise::parse("tipo: completar\nconsigna: Pintá.\nbanco: red, blue\n- [#EF4444] {red}\n- The glass is {blue|cyan}.");
    expect($ok['errors'])->toBe([])
        ->and($ok['exercise']['type'])->toBe('fill')
        ->and($ok['exercise']['items'][0]['swatch'])->toBe('#EF4444')
        ->and($ok['exercise']['items'][1]['parts'][1]['hole'])->toBe(['blue', 'cyan']);

    $free = EnglishExercise::parse("tipo: escribir\n- {Hello|Hi}! My name is {*nombre}.");
    expect($free['exercise']['items'][0]['parts'][2])->toBe(['free' => 'name']);

    expect(EnglishExercise::parse("tipo: volar\n- x")['errors'][0])->toContain('desconocido')
        ->and(EnglishExercise::parse("tipo: escuchar\nopciones: a, b\n- c")['errors'][0])->toContain('no está en «opciones:»')
        ->and(EnglishExercise::parse("tipo: completar\nbanco: a\n- sin huecos")['errors'][0])->toContain('no tiene huecos')
        ->and(EnglishExercise::parse("tipo: responder\n- Question?")['errors'][0])->toContain('=>');
});

test('el curso de Primaria se importa sin prácticas y cada micro-misión con su ejercicio', function () {
    $course = importEnglishPrimaria();

    expect($course->language->isSelfChecked())->toBeTrue()
        // Los Talleres (raíz + 4 + 3 ramas), las Forjas, el Puerto y la Ciudadela (8 de tronco + 4 ramas cada una).
        ->and($course->nodes()->count())->toBe(44)
        ->and($course->nodes()->where('is_published', true)->count())->toBe(44)
        ->and($course->nodes()->where('type', 'extra')->count())->toBe(15)
        ->and($course->nodes()->whereHas('practices')->exists())->toBeFalse();

    $step = NodeStep::where('code', 'R00-N01-P2')->whereIn('node_id', $course->nodes()->pluck('id'))->first();
    expect($step->englishExercise()['type'])->toBe('fill')
        ->and($step->expected_output)->toBe(EnglishExercise::PASSED)
        ->and($step->translation)->toContain('El vidrio es rojo')
        ->and($step->wordList()[0])->toBe(['en' => 'window', 'es' => 'ventana, vitral']);
});

test('una micro-misión de inglés sin ejercicio no se importa', function () {
    $md = "# CURSO\n\n```meta\nslug: ingles-roto\ntitulo: Roto\nlenguaje: english\n```\n\n## R00-N01 · Uno\n\n```meta\ntipo: raiz\n```\n\n"
        ."### Micro-misión R00-N01-P1 · Hola\n#### Inglés\nHello.\n";
    $report = app(CourseImporter::class)->import([['name' => 'x.md', 'content' => $md]], dryRun: true);

    expect(implode(' ', $report->errors))->toContain('no tiene «Ejercicio»');
});

test('un episodio se completa al superar sus misiones y abre a los siguientes sin monedas', function () {
    $course = importEnglishPrimaria();
    $root = $course->rootNode;
    $episode2 = $course->nodes()->where('code', 'R01-N01')->first();
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $root);
    $access = app(TreeAccess::class);

    // Con el primer episodio a medias, el segundo no se abre.
    app(StepCompleter::class)->complete($student, $root->steps()->first(), EnglishExercise::PASSED);
    expect($access->isCompleted($student, $root))->toBeFalse()
        ->and(fn () => app(NodeUnlocker::class)->unlock($student, $episode2))->toThrow(NodeLocked::class);

    passEpisode($student, $root);
    expect($access->isCompleted($student, $root))->toBeTrue()
        ->and($access->state($student, $episode2))->toBe(TreeAccess::STATE_AVAILABLE);

    app(NodeUnlocker::class)->unlock($student, $episode2);
    expect($access->state($student, $episode2))->toBe(TreeAccess::STATE_UNLOCKED);
    passEpisode($student, $episode2);
    expect($access->state($student, $episode2))->toBe(TreeAccess::STATE_COMPLETED);
});

test('lo que manda el navegador tiene que decir «superada»', function () {
    $course = importEnglishPrimaria();
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $course->rootNode);

    expect(fn () => app(StepCompleter::class)->complete($student, $course->rootNode->steps()->first(), 'cualquier cosa'))
        ->toThrow(InvalidArgumentException::class);
});

test('el CV muestra el curso de inglés con sus episodios terminados, también el primero', function () {
    $english = importEnglishPrimaria();
    $python = makeCourse();
    $student = enrolledStudent($english);
    app(NodeUnlocker::class)->unlock($student, $english->rootNode);
    $student = enrolledStudent($python['course'], $student);
    app(NodeUnlocker::class)->unlock($student, $python['root']);

    passEpisode($student, $english->rootNode);

    $courses = collect(CvData::for($student)['courses'])->keyBy('course.id');
    expect($courses->keys())->toContain($python['course']->id)->toContain($english->id)
        ->and($courses[$english->id]['skills'])->toContain($english->rootNode->title);
});

test('la mochila tiene una solapa por curso con abono, y Ámbar vende lo de Ada', function () {
    $course = importEnglishPrimaria();
    $this->artisan('app:game-items');
    $student = enrolledStudent($course);

    Livewire::actingAs($student)->test(InventoryPage::class)
        ->assertSee('Crónicas en Inglés');
    Livewire::actingAs($student)->test(ShopPage::class, ['course' => $course])
        ->assertOk()->assertSee('El puesto de Ámbar')->assertSee('Lápiz de Ada')->assertDontSee('Pluma de Escribiente');
    expect(Item::where('code', Item::ECHO_FEATHER)->value('course_id'))->toBe($course->id);
});

test('el alumno ve la biblioteca y el episodio, y «Leer» muestra el episodio entero', function () {
    $course = importEnglishPrimaria();
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $course->rootNode);

    Livewire::actingAs($student)->test(CourseDetail::class, ['course' => $course])
        ->assertSee('Ir a la biblioteca');

    Livewire::actingAs($student)->test(CourseTree::class, ['course' => $course])
        ->assertSee('Elegí qué leer o practicar')
        ->assertSee('Iris Arrives')
        ->assertSee('Se abre al terminar');

    Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode])
        ->assertSee('This is Ada.')
        ->assertDontSee('Teo has an orange glass.');

    Livewire::actingAs($student)->withQueryParams(['leer' => 1])->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode])
        ->assertSee('Escuchar todo')
        ->assertSee('Teo has an orange glass.');
});

test('el alumno resuelve una misión desde la página del episodio', function () {
    $course = importEnglishPrimaria();
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $course->rootNode);
    $step = $course->rootNode->steps()->first();

    Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode])
        ->call('completeStep', $step->id, EnglishExercise::PASSED, '')
        ->assertReturned(['ok' => true, 'xp' => $step->xp_reward]);
});

test('decir la frase en voz alta da un poco de XP, una sola vez por micro-misión', function () {
    $course = importEnglishPrimaria();
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $course->rootNode);
    [$first, $second] = $course->rootNode->steps()->take(2)->get()->all();
    $xp = (int) config('game.spoken_xp');

    $page = Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode]);
    $page->call('speakStep', $first->id)->assertReturned(['ok' => true, 'xp' => $xp]);
    $page->call('speakStep', $first->id)->assertReturned(['ok' => true, 'xp' => 0]);
    // La segunda todavía no se puede jugar: no da nada.
    $page->call('speakStep', $second->id)->assertReturned(['ok' => false, 'error' => 'Esta micro-misión todavía no está disponible.']);

    expect($student->fresh()->xp_total)->toBe($xp)
        ->and($student->xpTransactions()->where('reason', 'spoke_aloud')->count())->toBe(1);
});

test('una misión superada se puede repasar: se juega de nuevo sin volver a pagar', function () {
    $course = importEnglishPrimaria();
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $course->rootNode);
    [$first, $second] = $course->rootNode->steps()->take(2)->get()->all();
    app(StepCompleter::class)->complete($student, $first, EnglishExercise::PASSED);
    $xp = $student->fresh()->xp_total;

    $page = Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode])
        ->assertSee('Repasar')
        ->set('replay', $first->id)
        ->assertSeeHtml('data-test="en-replay-done"');
    $page->call('completeStep', $first->id, EnglishExercise::PASSED, '')->assertReturned(['ok' => true, 'xp' => 0]);
    expect($student->fresh()->xp_total)->toBe($xp);

    // Una que todavía no superó no se «repasa»: sigue siendo la que toca.
    $page->set('replay', $second->id)->assertDontSeeHtml('data-test="en-replay-done"');
});

test('el admin guarda un curso de inglés con el primer episodio gratis; uno de programación necesita precio', function () {
    $english = importEnglishPrimaria();
    $admin = User::factory()->admin()->create();

    Livewire::actingAs($admin)->test(CourseForm::class, ['course' => $english])
        ->set('root_price', 0)->set('is_featured', true)
        ->call('save')->assertHasNoErrors();
    expect($english->fresh()->root_price)->toBe(0)
        ->and($english->rootNode->fresh()->price)->toBe(0);

    $python = makeCourse()['course'];
    Livewire::actingAs($admin)->test(CourseForm::class, ['course' => $python])
        ->set('root_price', 0)
        ->call('save')->assertHasErrors('root_price');
});

test('sin abono, la biblioteca deja probar el primer episodio y lleva a pedir el abono', function () {
    $course = importEnglishPrimaria();
    $student = User::factory()->create();

    Livewire::actingAs($student)->test(CourseTree::class, ['course' => $course])
        ->assertSee('Estás probando')
        ->assertSee('Practicar gratis')
        ->assertSee('Pedir abono')
        ->assertDontSee('Empezar');

    Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode])
        ->assertSee('This is Ada.');
});

test('la plataforma deja usar el micrófono solo a ella misma (el extra «hablar»)', function () {
    $this->get('/login')->assertHeader('Permissions-Policy', 'camera=(), microphone=(self), geolocation=(), payment=(), usb=()');
});

test('Ada es la protagonista: niña en Primaria y de 15 en Secundaria, con sus seis aspectos y Folio entre las monturas', function () {
    $primaria = importEnglishPrimaria();
    $secundaria = Course::create(['title' => 'Crónicas en Inglés · Secundaria', 'slug' => 'ingles-secundaria', 'language' => 'english', 'is_published' => true, 'root_price' => 0]);

    expect(Heroes::protagonistOf($primaria))->toMatchArray(['name' => 'Ada', 'slug' => 'ada'])
        ->and(Heroes::protagonistOf($secundaria))->toMatchArray(['name' => 'Ada', 'slug' => 'ada-15'])
        ->and(Heroes::protagonistOf(makeCourse()['course'])['name'])->toBe('Mia');
    foreach (['ada', 'ada-15'] as $slug) {
        foreach (range(1, 6) as $look) {
            expect(public_path("img/protagonistas/{$slug}/{$look}.webp"))->toBeFile();
        }
    }
    foreach (range(1, 5) as $level) {
        expect(public_path("img/monturas/folio/n{$level}.webp"))->toBeFile();
    }
    expect(config('game.mounts.species.folio'))->toBe('Folio');

    $student = enrolledStudent($primaria);
    app(NodeUnlocker::class)->unlock($student, $primaria->rootNode);
    Livewire::actingAs($student)->test(CourseTree::class, ['course' => $primaria])
        ->assertSee('Tomá el control de Ada');
    Livewire::actingAs($student)->test(HeroPage::class, ['course' => $primaria])
        ->assertOk()->assertSee('Aprendiz del Profe');
});

test('Eco crece con los episodios terminados y se ve en la ficha de Ada y al terminar un episodio', function () {
    $course = importEnglishPrimaria();
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $course->rootNode);
    app(Heroes::class)->create($student, $course, 1, ['strength' => 6, 'dexterity' => 6, 'intelligence' => 6, 'luck' => 6]);
    foreach (['pichon', 'joven', 'adulto'] as $form) {
        expect(public_path("img/mascotas/eco/{$form}.webp"))->toBeFile();
    }

    expect(app(Heroes::class)->pet($student, $course))->toMatchArray(['form' => 'pichon', 'done' => 0, 'grewNow' => false])
        ->and(app(Heroes::class)->pet($student, $course)['next'])->toBe(['label' => 'Eco joven', 'at' => 10, 'missing' => 10]);

    // Con el umbral en 2 para no tener que terminar diez episodios.
    config()->set('game.protagonists.ingles-primaria.pet.stages.1.at', 2);
    passEpisode($student, $course->rootNode);
    $second = $course->nodes()->where('code', 'R01-N01')->firstOrFail();
    app(NodeUnlocker::class)->unlock($student, $second);
    passEpisode($student, $second);

    expect(app(Heroes::class)->pet($student, $course))->toMatchArray(['form' => 'joven', 'done' => 2, 'grewNow' => true]);
    Livewire::actingAs($student)->test(HeroPage::class, ['course' => $course])
        ->assertSee('Eco joven')->assertSee('le faltan 23 para ser Eco adulto');
    Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $second])
        ->assertSee('¡Eco creció! Ahora es Eco joven.');
    // Secundaria arranca con Eco joven.
    expect(collect(config('game.protagonists.ingles-secundaria.pet.stages'))->first()['form'])->toBe('joven');
});

/** Un curso de inglés chico con dos temporadas: los Talleres (raíz + 3) y las Forjas (2 de tronco + 1 rama). */
function importEnglishSeasons(): Course
{
    $step = fn (string $code) => "### Micro-misión {$code}-P1 · Hello\n#### Inglés\nHello.\n#### Ejercicio\ntipo: leer\n\n";
    $node = fn (string $code, string $meta) => "## {$code} · Episodio {$code}\n\n```meta\n{$meta}\n```\n\n".$step($code);
    $md = "# CURSO\n\n```meta\nslug: ingles-temporadas\ntitulo: Temporadas\nlenguaje: english\nprecio_raiz: 0\npublicado: si\n```\n\n"
        .$node('R00-N01', 'tipo: raiz')
        ."# RAMA R01 · Los Talleres\n\n```meta\ntipo: tronco\nposicion: 1\n```\n\n"
        .$node('R01-N01', "padre: R00-N01\nprecio: 0").$node('R01-N02', "padre: R00-N01\nprecio: 0").$node('R01-N03', "padre: R00-N01\nprecio: 0")
        ."# RAMA R02 · Las Forjas\n\n```meta\ntipo: tronco\nposicion: 2\n```\n\n"
        .$node('R02-N01', "padre: R00-N01\nprecio: 0").$node('R02-N02', "padre: R02-N01\nprecio: 0")
        .$node('R02-N03', "tipo: extra\npadre: R02-N01\nprecio: 0");
    $report = app(CourseImporter::class)->import([['name' => 'x.md', 'content' => $md]], dryRun: false);
    expect($report->errors)->toBe([]);

    return Course::where('slug', 'ingles-temporadas')->firstOrFail();
}

test('la temporada siguiente se abre con la mayor parte del tronco de la anterior, y las ramas no cuentan', function () {
    $course = importEnglishSeasons();
    $code = fn (string $c) => $course->nodes()->where('code', $c)->first();
    $student = enrolledStudent($course);
    $access = app(TreeAccess::class);
    app(NodeUnlocker::class)->unlock($student, $course->rootNode);
    passEpisode($student, $course->rootNode);

    // Los Talleres tienen 4 de tronco: hacen falta 3. Con 2 terminados, las Forjas siguen cerradas.
    app(NodeUnlocker::class)->unlock($student, $code('R01-N01'));
    passEpisode($student, $code('R01-N01'));
    $forjas = $code('R02-N01');
    expect($access->startsSeason($forjas))->toBeTrue()
        ->and($access->unlockBlockers($student, $forjas))->toContain(TreeAccess::BLOCK_SEASON_INCOMPLETE)
        ->and(implode(' ', UnlockMessages::for($student, $forjas)))->toContain('Terminá 3 de los 4 episodios de «Los Talleres» (llevás 2)')
        ->and(fn () => app(NodeUnlocker::class)->unlock($student, $forjas))->toThrow(NodeLocked::class);

    app(NodeUnlocker::class)->unlock($student, $code('R01-N02'));
    passEpisode($student, $code('R01-N02'));
    expect($access->state($student, $forjas))->toBe(TreeAccess::STATE_AVAILABLE);

    // La rama (extra) cuelga del episodio y no cuenta para el tronco de las Forjas.
    app(NodeUnlocker::class)->unlock($student, $forjas);
    passEpisode($student, $forjas);
    expect($access->startsSeason($code('R02-N03')))->toBeFalse()
        ->and($access->state($student, $code('R02-N03')))->toBe(TreeAccess::STATE_AVAILABLE)
        ->and($access->seasonProgress($student, $forjas))->toMatchArray(['done' => 1, 'total' => 2, 'needed' => 2]);

    Livewire::actingAs($student)->test(CourseTree::class, ['course' => $course])
        ->assertSee('Temporada 2')->assertSee('Las Forjas')->assertSee('Ramas:')
        ->assertSee('3 de 4 episodios');
});

test('el árbol de un curso con temporadas se dibuja para el alumno y en el panel (el padre llega a medias)', function () {
    $course = importEnglishSeasons();
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $course->rootNode);

    $states = collect(TreeGraph::forStudent($course, $student)['nodes'])->pluck('state', 'id');
    expect($states[$course->nodes()->where('code', 'R02-N01')->value('id')])->toBe(TreeAccess::STATE_LOCKED);

    $this->actingAs(User::factory()->admin()->create())->get(route('admin.students.tree', [$student, $course]))
        ->assertOk()->assertSee('data-test="student-journey"', false);
});
