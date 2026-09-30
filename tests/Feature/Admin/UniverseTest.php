<?php

use App\Models\Node;
use App\Models\User;
use App\Services\CourseImporter;
use App\Support\TopicCatalog;
use App\Support\UniverseGraph;

function courseFileWithTopics(string $temas, string $usa = ''): array
{
    $content = file_get_contents(base_path('tests/Fixtures/curso-ejemplo.md'));
    $meta = "padre: R00-N01\nprecio: 10\ncriatura: esqueleto\ntemas: {$temas}".($usa ? "\nusa: {$usa}" : '');

    return [['name' => 'curso.md', 'content' => str_replace("padre: R00-N01\nprecio: 10\ncriatura: esqueleto", $meta, $content)]];
}

test('el catálogo de temas lee familias, alcance y temas en orden', function () {
    $catalog = TopicCatalog::parse(<<<'MD'
        ## web · Web
        alcance: compartido

        - web.http · Cómo funciona la web · pedido y respuesta
        - web.api-rest · APIs REST

        ## prog · Fundamentos
        alcance: lenguaje

        - prog.bucles · Bucles · while y for
        MD);

    expect(array_keys($catalog['families']))->toBe(['web', 'prog'])
        ->and($catalog['families']['web']['scope'])->toBe('compartido')
        ->and($catalog['families']['web']['topics'])->toBe(['web.http', 'web.api-rest'])
        ->and($catalog['families']['prog']['scope'])->toBe('lenguaje')
        ->and($catalog['topics']['web.http']['description'])->toBe('pedido y respuesta')
        ->and($catalog['topics']['web.api-rest']['description'])->toBe('')
        ->and($catalog['topics']['prog.bucles']['order'])->toBeGreaterThan($catalog['topics']['web.api-rest']['order']);
});

test('el catálogo real de cursos/temas.md tiene todos los temas que usan los cursos', function () {
    expect(TopicCatalog::families())->toHaveKeys(['prog', 'html', 'css', 'sql', 'juegos'])
        ->and(TopicCatalog::has('html.formularios'))->toBeTrue()
        ->and(TopicCatalog::has('html.inventado'))->toBeFalse();
});

test('el importador guarda lo que un nodo enseña y lo que usa; un tema fuera del catálogo se guarda y se avisa', function () {
    $report = app(CourseImporter::class)->import(courseFileWithTopics('prog.variables, html.inventado', 'prog.salida'), dryRun: false);

    $node = Node::where('code', 'R01-N01')->firstOrFail();
    expect($report->errors)->toBe([])
        ->and($node->topics)->toBe(['prog.variables', 'html.inventado'])
        ->and($node->uses)->toBe(['prog.salida'])
        ->and(collect($report->warnings)->implode(' '))->toContain('«html.inventado»');
});

test('el mapa arma los temas con quién los enseña y quién los usa, y marca los sueltos', function () {
    app(CourseImporter::class)->import(courseFileWithTopics('prog.variables, html.inventado', 'prog.salida'), dryRun: false);
    $node = Node::where('code', 'R01-N01')->firstOrFail();

    $topics = collect(UniverseGraph::build()['topics'])->keyBy('key');

    expect($topics['prog.variables']['taught'])->toBe([$node->id])
        ->and($topics['prog.salida']['used'])->toBe([$node->id])
        ->and($topics['html.estructura']['taught'])->toBe([])
        ->and($topics['html.inventado']['loose'])->toBeTrue();
});

test('solo el docente entra al universo', function () {
    app(CourseImporter::class)->import(courseFileWithTopics('prog.variables'), dryRun: false);

    $this->actingAs(User::factory()->create())->get(route('admin.universe'))->assertRedirect(route('home'));
    $this->actingAs(User::factory()->admin()->create())->get(route('admin.universe'))
        ->assertOk()->assertSee('data-test="universe-map"', false)->assertSee('Temas compartidos')->assertSee('Cobertura de cada lenguaje');
});
