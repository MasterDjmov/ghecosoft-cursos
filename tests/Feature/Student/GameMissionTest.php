<?php

use App\Models\NodeStep;
use App\Models\User;
use App\Services\CourseImporter;

/*
 * D126, fase 4: las micro-misiones de juego (C con SDL3) las comprueba el robot de Arcadia en el navegador. El importador
 * junta sus «Eventos» y su «Estado» en `checks` (App\Support\GameMission) y la vista muestra «Comprobar».
 */

const GAME_STEP_MD = <<<'MD'
### Micro-misión R00-N01-P1 · La ventana azul

#### Desafío
Pintá el fondo de azul.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void) {
    return 0;
}
```

#### Eventos
```
cuadros 10
EVENTO
```

#### Estado
```
ventana
ESTADO
```

#### Salida esperada
```
── Estado ──
ventana: «Mi juego» 640x480
pixel 5 5: #0000ff
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void) {
    return 0;
}
```


MD;

function gameCourseReport(string $event = 'tecla Espacio', string $state = 'pixel 5 5'): array
{
    $step = str_replace(['EVENTO', 'ESTADO'], [$event, $state], GAME_STEP_MD);
    $md = str_replace(['lenguaje: python', '### Misión R00-N01-M1'], ['lenguaje: c', $step.'### Misión R00-N01-M1'], file_get_contents(base_path('tests/Fixtures/curso-ejemplo.md')));
    $report = app(CourseImporter::class)->import([['name' => 'curso.md', 'content' => $md]], dryRun: false);

    return [$report, NodeStep::where('code', 'R00-N01-P1')->first()];
}

test('el importador junta los eventos y el Estado de una micro-misión de juego', function () {
    [$report, $step] = gameCourseReport();

    expect($report->errors)->toBe([])
        ->and(json_decode($step->checks, true))->toBe([
            'events' => "cuadros 10\ntecla Espacio",
            'checks' => ['ventana', 'pixel 5 5'],
        ])
        ->and($step->expected_output)->toBe("── Estado ──\nventana: «Mi juego» 640x480\npixel 5 5: #0000ff");
});

test('un evento o un pedido del Estado que el robot no entiende es un error del importador', function () {
    [$report] = gameCourseReport('saltar alto', 'pixel arriba');

    expect(implode("\n", $report->errors))
        ->toContain('evento que no se entiende: «saltar alto»')
        ->toContain('el pixel va con su x y su y');
});

test('la micro-misión de juego se ve con Jugar y Comprobar, sin «pegá la salida»', function () {
    [, $step] = gameCourseReport();
    $admin = User::factory()->admin()->create();

    $this->actingAs($admin)->get(route('student.node', [$step->node->course, $step->node]))
        ->assertOk()
        ->assertSee('data-test="game-board"', false)
        ->assertSee('data-test="game-check"', false)
        ->assertDontSee('data-test="step-paste"', false);
});
