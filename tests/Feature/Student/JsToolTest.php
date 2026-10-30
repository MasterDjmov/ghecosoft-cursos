<?php

use App\Enums\Language;
use App\Models\NodeStep;
use App\Models\User;
use App\Services\CourseImporter;
use App\Support\JsMission;

/*
 * D115: JavaScript corre en el navegador de quien ejecuta, en una caja sandbox="allow-scripts" SIN mismo origen
 * (no ve la sesión ni las cookies de la plataforma) y sin red (la CSP no deja salir; fetch va al Puerto simulado).
 * Herramientas → La caja de la Feria: el staff siempre; el alumno, con el abono de un curso de JavaScript.
 * El comportamiento de la caja se prueba en Chrome con node scripts/js-micro/probar-caja.mjs.
 */

test('JavaScript corre para los alumnos en el navegador', function () {
    expect(Language::JavaScript->runsForStudents())->toBeTrue()
        ->and(Language::JavaScript->studentCanRun())->toBeTrue()
        ->and(Language::JavaScript->extension())->toBe('js');
});

test('la caja de JavaScript solo lleva allow-scripts: nunca mismo origen, formularios ni ventanas, y sin red', function () {
    $caja = file_get_contents(resource_path('js/runners/js-caja.js'));
    $runners = collect(glob(resource_path('js/runners/{*,*/*}.js'), GLOB_BRACE))->map(fn ($f) => file_get_contents($f))->implode("\n");

    // Todo sandbox que aparezca en los ejecutores (en el código o en sus comentarios) es "" (HTML) o "allow-scripts" (JS).
    preg_match_all('/sandbox[\'"]?\s*[,=:]\s*[\'"]([^\'"]*)[\'"]/', $runners, $values);
    expect(array_unique($values[1]))->each->toBeIn(['', 'allow-scripts']);

    expect($caja)->toContain("frame.setAttribute('sandbox', 'allow-scripts')")
        ->and($caja)->toContain("default-src 'none'")
        ->and($caja)->toContain("connect-src 'none'")
        ->and($caja)->not->toContain('unsafe-eval')
        ->and($runners)->not->toMatch('/allow-(forms|popups|top-navigation|modals|downloads|pointer-lock)/')
        ->and($caja)->not->toMatch("/setAttribute\\('sandbox',[^)]*allow-same-origin/");
});

test('el staff entra a la caja de la Feria aunque no haya curso de JavaScript', function () {
    $this->actingAs(User::factory()->admin()->create())
        ->get(route('student.js-tool'))
        ->assertOk()
        ->assertSee('La caja de la Feria')
        ->assertSee('data-test="js-board"', false)
        ->assertSee('data-test="js-example-puerto"', false);
});

test('un alumno sin abono de JavaScript no entra ni ve la caja en el menú', function () {
    $student = User::factory()->create();
    makeCourse(['language' => 'javascript', 'is_published' => true]);

    $this->actingAs($student)->get(route('student.js-tool'))->assertForbidden();
    $this->actingAs($student)->get(route('student.worlds'))->assertDontSee('data-test="menu-js-tool"', false);
});

test('con el abono vigente de un curso de JavaScript publicado, el alumno la usa', function () {
    ['course' => $course] = makeCourse(['language' => 'javascript', 'is_published' => true]);
    $student = enrolledStudent($course);

    $this->actingAs($student)->get(route('student.js-tool'))->assertOk();
    $this->actingAs($student)->get(route('student.worlds'))->assertSee('data-test="menu-js-tool"', false);
});

test('el abono de otro curso no alcanza', function () {
    ['course' => $python] = makeCourse(['is_published' => true]);
    makeCourse(['language' => 'javascript', 'is_published' => true]);
    $student = enrolledStudent($python);

    $this->actingAs($student)->get(route('student.js-tool'))->assertForbidden();
});

const JS_STEP_MD = <<<'MD'
### Micro-misión R00-N01-P1 · El farol

#### Página
```html
<p id="cartel">apagado</p><button id="prender">Prender</button>
```

#### Eventos
```
click #prender
EVENTO
```

#### Estado
```
#cartel
cookie visto
```

#### Almacenamiento
```
local veces = 2
cookie nombre = Nima
```

#### Salida esperada
```
── Estado ──
#cartel: prendido
cookie visto: si
```

#### Solución
```javascript
document.querySelector('#prender').addEventListener('click', () => { document.querySelector('#cartel').textContent = 'prendido'; document.cookie = 'visto=si'; });
```


MD;

function jsCourseReport(string $event = 'esperar 100'): array
{
    $md = str_replace(['lenguaje: python', '### Misión R00-N01-M1'], ['lenguaje: javascript', str_replace('EVENTO', $event, JS_STEP_MD).'### Misión R00-N01-M1'], file_get_contents(base_path('tests/Fixtures/curso-ejemplo.md')));
    $report = app(CourseImporter::class)->import([['name' => 'curso.md', 'content' => $md]], dryRun: false);

    return [$report, NodeStep::where('code', 'R00-N01-P1')->first()];
}

test('el importador junta la página, los eventos, el Estado y lo guardado de una micro-misión de JavaScript', function () {
    [$report, $step] = jsCourseReport();

    expect($report->errors)->toBe([])
        ->and(json_decode($step->checks, true))->toBe([
            'page' => '<p id="cartel">apagado</p><button id="prender">Prender</button>',
            'events' => "click #prender\nesperar 100",
            'checks' => "#cartel\ncookie visto",
            'storage' => ['local' => ['veces' => '2']],
            'cookies' => 'nombre=Nima',
        ])
        ->and($step->expected_output)->toBe("── Estado ──\n#cartel: prendido\ncookie visto: si");
});

test('un evento que la caja no entiende es un error del importador', function () {
    [$report] = jsCourseReport('saltar #prender');

    expect(implode("\n", $report->errors))->toContain('evento que no se entiende: «saltar #prender»');
});

test('los otros archivos de una micro-misión de JavaScript se leen por su nombre', function () {
    $text = "vec2.js\n```javascript\nexport const a = 1;\n```\n\nheroe.js\n```javascript\nimport { a } from './vec2.js';\nexport default a;\n```";

    expect(JsMission::files($text))->toBe([
        'vec2.js' => 'export const a = 1;',
        'heroe.js' => "import { a } from './vec2.js';\nexport default a;",
    ])->and(json_decode(JsMission::encode(['files' => $text]), true)['files'])->toHaveKey('vec2.js');
});
