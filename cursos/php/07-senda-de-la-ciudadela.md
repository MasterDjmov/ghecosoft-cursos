# RAMA S02 · Senda de la Ciudadela: el framework Laravel

```meta
tipo: senda
posicion: 7
```

## S02-N01 · Rutas, controladores y vistas con Blade

```meta
tipo: tema
padre: R05-N08
precio: 3
moneda: comodin
criatura: skeleton
ejecutable: no
```

### Crónica

El segundo camino desde la Encrucijada sube por una colina hasta una fortaleza de piedra clara: la **Ciudadela de Laravel**. Adentro todo tiene su lugar: una sala para las rutas, otra para los controladores, un taller donde se dibujan las vistas, una bodega que ya sabe hablar con MariaDB. Los guardias no dejan pasar un formulario sin su sello ni a un visitante sin su nombre.

—Todo lo que construiste a mano en el Faro —dice {mentor}, señalando los muros—: el router, los controladores, las plantillas, la conexión, las pruebas. Acá ya viene hecho, probado por miles de programadores y ordenado siempre igual. Un **framework** no te ahorra entender, {heroe}: te ahorra repetir. Y como ya sabés cómo funciona por dentro, vas a entender cada sala.

### Objetivos

- Instalar un proyecto de Laravel con Composer y recorrer sus carpetas.
- Definir rutas con parámetros, restricciones y nombres.
- Escribir controladores que preparan los datos y devuelven vistas.
- Armar vistas con Blade: escapado, condicionales, bucles y un componente de diseño.
- Probar las páginas con las pruebas HTTP de Laravel (`php artisan test`).

### Antes de empezar

- La Encrucijada de los Sellos (R05-N08). Vas a usar sobre todo Composer (R02-N10), las plantillas (R03-N08), el router y los controladores (R05-N01) y PHPUnit (R05-N04).

### Explicación

#### Instalar Laravel
Laravel se instala con Composer, como cualquier biblioteca, pero en lugar de `require`
se usa `create-project`, que descarga el esqueleto completo de una aplicación:
```bash
composer create-project laravel/laravel:^12.0 ciudadela
cd ciudadela
php artisan serve
```
Abrí `http://127.0.0.1:8000` y vas a ver la página de bienvenida. Laravel 12 funciona
con **PHP 8.2 o más nuevo** (el de XAMPP alcanza). `artisan` es la navaja suiza del
proyecto: crea archivos, corre las migraciones, las pruebas y el servidor. Con
`php artisan list` ves todo lo que sabe hacer.

> Existe también el instalador `laravel new`, que pregunta por "kits de inicio" con
> React, Vue o Livewire. En esta senda usamos el esqueleto limpio para ver cada pieza.

#### Las carpetas que importan
| Carpeta | Qué va ahí |
|---|---|
| `routes/web.php` | las rutas: qué URL atiende qué código |
| `app/Http/Controllers/` | los controladores |
| `app/Models/` | los modelos (la tabla hecha clase, en el próximo nodo) |
| `resources/views/` | las vistas Blade (`.blade.php`) |
| `database/migrations/` | la estructura de las tablas, como código |
| `tests/Feature/` | las pruebas que piden páginas |
| `public/` | lo único que se publica: `index.php`, imágenes, CSS |
| `.env` | la configuración de esta compu (nunca se sube al repositorio) |

Es el mismo orden que armaste en el Faro, con un nombre fijo para cada cosa: cualquier
programador de Laravel abre tu proyecto y sabe dónde buscar.

#### Rutas
Una ruta une un verbo y una URL con el código que responde:
```php
Route::get('/salidas', [SalidaController::class, 'index'])->name('salidas.index');
Route::get('/salidas/{codigo}', [SalidaController::class, 'show'])->name('salidas.show');
Route::redirect('/', '/salidas');
Route::view('/contacto', 'contacto');          // una vista sin controlador
```
- `{codigo}` es un **parámetro**: llega como argumento al método del controlador.
  `{categoria?}` lo hace opcional (y el argumento necesita un valor por defecto).
- Las **restricciones** filtran los parámetros: `->whereNumber('id')`,
  `->whereIn('categoria', ['entradas', 'postres'])`. Si no cumple, la ruta no coincide
  y Laravel responde **404** solo.
- El **nombre** permite generar la URL sin escribirla: `route('salidas.show', 'PM-101')`
  devuelve `http://…/salidas/PM-101`. Si mañana cambiás la URL, los enlaces siguen
  funcionando.

`php artisan route:list` muestra todas las rutas de la aplicación.

#### Controladores
```bash
php artisan make:controller SalidaController
```
Un controlador es una clase con un método por acción. Recibe los parámetros de la ruta
y, si lo pide, el `Request` (el pedido con todo lo que trae):
```php
public function index(Request $request): View
{
    $destino = $request->query('destino');          // ?destino=Montevideo
    return view('salidas.index', ['destino' => $destino]);
}
```
`view('salidas.index', [...])` busca `resources/views/salidas/index.blade.php` y le pasa
las variables. `abort(404)` corta y responde "no encontrado".

Para filtrar y ordenar listas, Laravel trae las **colecciones**: `collect($array)`
envuelve un array y le da métodos encadenables como `where`, `sortBy`, `map`, `count` o
`when` (que aplica un filtro solo si la condición es verdadera).

#### Vistas con Blade
Blade es el lenguaje de plantillas de Laravel. Se compila a PHP común, pero se escribe
más corto y más seguro:
| Blade | Hace |
|---|---|
| `{{ $nombre }}` | muestra **escapado** (con `htmlspecialchars`, como tu función `e()`) |
| `{!! $html !!}` | muestra **sin escapar** (solo para HTML en el que confiás) |
| `@if (…) … @elseif (…) … @else … @endif` | condicionales |
| `@foreach ($lista as $clave => $valor) … @endforeach` | bucles |
| `@forelse ($lista as $x) … @empty … @endforelse` | bucle con un caso "no hay nada" |
| `@class(['activo' => $condicion])` | arma el atributo `class` según condiciones |

El diseño común (la cabecera, el menú, el pie) va en un **componente**:
`resources/views/components/layout.blade.php` se usa como `<x-layout>` y lo que va
adentro llega en la variable `$slot`. Los atributos se declaran con `@props`:
```blade
@props(['titulo' => 'Puerto'])
<title>{{ $titulo }}</title>
...
<main>{{ $slot }}</main>
```
```blade
<x-layout titulo="Salidas">  ... contenido ...  </x-layout>
<x-layout :titulo="$codigo"> ... </x-layout>      {{-- con : pasa una expresión PHP --}}
```

#### Probar sin abrir el navegador
Laravel trae PHPUnit configurado y un cliente HTTP de prueba: la prueba "pide" una
página y revisa la respuesta, sin servidor.
```bash
php artisan make:test SalidasTest      # crea tests/Feature/SalidasTest.php
php artisan test
```
```php
$this->get('/salidas')->assertOk()->assertSee('Albatros');
$this->get('/salidas/PM-999')->assertNotFound();
$this->get('/')->assertRedirect('/salidas');
```
`assertSeeInOrder([...])` comprueba el orden y `assertDontSee` que algo **no** aparezca.
Borrá los `ExampleTest.php` que trae el esqueleto si cambiás la página de inicio: uno
espera que `/` responda 200.

### Código de ejemplo

El **tablón de salidas** del Puerto: la lista de barcos que zarpan hoy, con filtro por
destino y una página de detalle. Los datos todavía están en el controlador; en el
próximo nodo pasan a MariaDB.

`routes/web.php`
```php
<?php

use App\Http\Controllers\SalidaController;
use Illuminate\Support\Facades\Route;

Route::redirect('/', '/salidas');
Route::get('/salidas', [SalidaController::class, 'index'])->name('salidas.index');
Route::get('/salidas/{codigo}', [SalidaController::class, 'show'])->name('salidas.show');
```

`app/Http/Controllers/SalidaController.php`
```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\View\View;

class SalidaController extends Controller
{
    private const SALIDAS = [
        'PM-101' => ['barco' => 'Albatros', 'destino' => 'Montevideo', 'hora' => '08:30', 'estado' => 'a horario'],
        'PM-102' => ['barco' => 'Gaviota', 'destino' => 'Colonia', 'hora' => '10:15', 'estado' => 'demorado'],
        'PM-103' => ['barco' => 'Estrella del Sur', 'destino' => 'Montevideo', 'hora' => '13:00', 'estado' => 'a horario'],
        'PM-104' => ['barco' => 'Tritón', 'destino' => 'Piriápolis', 'hora' => '17:45', 'estado' => 'cancelado'],
    ];

    public function index(Request $request): View
    {
        $destino = $request->query('destino');
        $salidas = collect(self::SALIDAS)
            ->when($destino, fn ($salidas) => $salidas->where('destino', $destino));

        return view('salidas.index', ['salidas' => $salidas, 'destino' => $destino]);
    }

    public function show(string $codigo): View
    {
        $salida = self::SALIDAS[$codigo] ?? abort(404);

        return view('salidas.show', ['codigo' => $codigo, 'salida' => $salida]);
    }
}
```

`resources/views/components/layout.blade.php`
```blade
@props(['titulo' => 'Puerto'])
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>{{ $titulo }} · Puerto de los Mensajeros</title>
</head>
<body>
    <header><a href="{{ route('salidas.index') }}">Tablón de salidas</a></header>
    <main>
        {{ $slot }}
    </main>
</body>
</html>
```

`resources/views/salidas/index.blade.php`
```blade
<x-layout titulo="Salidas">
    <h1>Salidas de hoy</h1>
    @if ($destino)
        <p>Con destino a {{ $destino }} · <a href="{{ route('salidas.index') }}">ver todas</a></p>
    @endif
    <table>
        <tr><th>Código</th><th>Barco</th><th>Destino</th><th>Hora</th></tr>
        @forelse ($salidas as $codigo => $salida)
            <tr>
                <td><a href="{{ route('salidas.show', $codigo) }}">{{ $codigo }}</a></td>
                <td>{{ $salida['barco'] }}</td>
                <td>{{ $salida['destino'] }}</td>
                <td>{{ $salida['hora'] }}</td>
            </tr>
        @empty
            <tr><td colspan="4">No hay salidas con ese destino.</td></tr>
        @endforelse
    </table>
</x-layout>
```

`resources/views/salidas/show.blade.php`
```blade
<x-layout :titulo="$codigo">
    <h1>{{ $codigo }} · {{ $salida['barco'] }}</h1>
    <p>Destino: {{ $salida['destino'] }} · sale a las {{ $salida['hora'] }}</p>
    <p @class(['estado', 'alerta' => $salida['estado'] !== 'a horario'])>{{ ucfirst($salida['estado']) }}</p>
</x-layout>
```

`tests/Feature/SalidasTest.php`
```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class SalidasTest extends TestCase
{
    public function test_la_raiz_lleva_al_tablon(): void
    {
        $this->get('/')->assertRedirect('/salidas');
    }

    public function test_lista_todas_las_salidas_en_orden(): void
    {
        $this->get('/salidas')
            ->assertOk()
            ->assertSeeInOrder(['Albatros', 'Gaviota', 'Estrella del Sur', 'Tritón']);
    }

    public function test_filtra_por_destino(): void
    {
        $this->get('/salidas?destino=Montevideo')
            ->assertOk()
            ->assertSee('Albatros')
            ->assertSee('Estrella del Sur')
            ->assertDontSee('Gaviota');
    }

    public function test_avisa_si_no_hay_salidas(): void
    {
        $this->get('/salidas?destino=Rosario')->assertSee('No hay salidas con ese destino.');
    }

    public function test_muestra_el_detalle(): void
    {
        $this->get('/salidas/PM-104')->assertOk()->assertSee('Tritón')->assertSee('Cancelado');
    }

    public function test_un_codigo_que_no_existe_da_404(): void
    {
        $this->get('/salidas/PM-999')->assertNotFound();
    }
}
```

Con `php artisan serve` probalo en el navegador (`/salidas`, `/salidas?destino=Colonia`,
`/salidas/PM-102`) y con `php artisan test`:
```
   PASS  Tests\Feature\SalidasTest
  ✓ la raiz lleva al tablon
  ✓ lista todas las salidas en orden
  ✓ filtra por destino
  ✓ avisa si no hay salidas
  ✓ muestra el detalle
  ✓ un codigo que no existe da 404

  Tests:    6 passed (13 assertions)
```

### ¿Para qué sirve?

Laravel es el framework de PHP más usado del mundo: lo vas a encontrar en ofertas de trabajo, en sistemas de gestión, tiendas y APIs. Todo proyecto de Laravel tiene la misma forma, así que lo que aprendas acá sirve para leer y modificar cualquiera. Y las pruebas HTTP te dejan cambiar el código con tranquilidad: si algo se rompe, te enterás antes que el cliente.

### Errores habituales

**Esqueleto: `Route [salidas.ver] not defined`.** El nombre que usás en `route()` no
existe (o está mal escrito). Mirá los nombres con `php artisan route:list`.

**Esqueleto: `View [salida.index] not found`.** La vista no está donde el punto dice:
`salidas.index` es `resources/views/salidas/index.blade.php`, con la extensión
`.blade.php` completa.

**Esqueleto: `Undefined variable $salidas` en la vista.** La vista solo ve lo que le
pasa el controlador en el array de `view()`. Revisá que la clave se llame igual.

**Orco: `{!! !!}` con datos del usuario.** Muestra el texto sin escapar: si alguien
escribe `<script>`, se ejecuta. Siempre `{{ }}`, salvo HTML que generaste vos.

**Ogro: la prueba que espera 200 en `/`.** El `ExampleTest.php` del esqueleto falla en
cuanto cambiás la ruta de inicio. Borralo o adaptalo.

**Ogro: el orden de las rutas.** `/salidas/{codigo}` declarada antes que
`/salidas/buscar` se "come" la segunda (`buscar` pasa como código). Las rutas fijas van
primero, o restringí el parámetro.

### Misión S02-N01-M1 · La carta del bodegón

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

En un proyecto de Laravel nuevo, armá la **carta del bodegón del puerto**. Un
`CartaController` guarda estos platos (nombre, categoría, precio):

| Plato | Categoría | Precio |
|---|---|---|
| Rabas | entradas | 5200 |
| Empanadas de pescado | entradas | 3800 |
| Merluza a la romana | principales | 9500 |
| Cazuela de mariscos | principales | 14750.5 |
| Flan casero | postres | 3100 |

Una sola ruta con nombre `carta` atiende `/carta` (todos los platos) y
`/carta/{categoria}` (solo esa categoría); la categoría solo puede ser `entradas`,
`principales` o `postres`, y cualquier otra da 404. La vista muestra cada plato con el
precio en formato argentino (`$ 14.750,50`), la cantidad de platos listados
(`1 plato`, `2 platos`) y enlaces a las tres categorías hechos con `route()`. Usá un
componente de diseño. Escribí las pruebas y entregá el proyecto en un zip **sin**
`vendor/` ni `node_modules/`.

#### Criterio de aprobación

- Una sola ruta con parámetro opcional y `whereIn`; los enlaces salen de `route()`.
- Los precios y la cantidad se muestran bien, y las pruebas cubren la carta completa, una categoría y el 404.
- `php artisan test` pasa.

#### Solución de referencia

`routes/web.php`
```php
<?php

use App\Http\Controllers\CartaController;
use Illuminate\Support\Facades\Route;

Route::get('/carta/{categoria?}', [CartaController::class, 'index'])
    ->whereIn('categoria', CartaController::CATEGORIAS)
    ->name('carta');
```

`app/Http/Controllers/CartaController.php`
```php
<?php

namespace App\Http\Controllers;

use Illuminate\View\View;

class CartaController extends Controller
{
    public const CATEGORIAS = ['entradas', 'principales', 'postres'];

    private const PLATOS = [
        ['nombre' => 'Rabas', 'categoria' => 'entradas', 'precio' => 5200],
        ['nombre' => 'Empanadas de pescado', 'categoria' => 'entradas', 'precio' => 3800],
        ['nombre' => 'Merluza a la romana', 'categoria' => 'principales', 'precio' => 9500],
        ['nombre' => 'Cazuela de mariscos', 'categoria' => 'principales', 'precio' => 14750.5],
        ['nombre' => 'Flan casero', 'categoria' => 'postres', 'precio' => 3100],
    ];

    public function index(?string $categoria = null): View
    {
        $platos = collect(self::PLATOS)
            ->when($categoria, fn ($platos) => $platos->where('categoria', $categoria));

        return view('carta', [
            'platos' => $platos,
            'categoria' => $categoria,
            'categorias' => self::CATEGORIAS,
        ]);
    }
}
```

`resources/views/components/layout.blade.php`
```blade
@props(['titulo' => 'Bodegón del Puerto'])
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>{{ $titulo }}</title>
</head>
<body>
    <main>{{ $slot }}</main>
</body>
</html>
```

`resources/views/carta.blade.php`
```blade
<x-layout :titulo="$categoria ? 'Carta · ' . ucfirst($categoria) : 'Carta'">
    <h1>Carta del bodegón</h1>
    <nav>
        <a href="{{ route('carta') }}">Todo</a>
        @foreach ($categorias as $cat)
            <a href="{{ route('carta', $cat) }}" @class(['activa' => $cat === $categoria])>{{ ucfirst($cat) }}</a>
        @endforeach
    </nav>
    <p>{{ $platos->count() }} {{ $platos->count() === 1 ? 'plato' : 'platos' }}</p>
    <ul>
        @foreach ($platos as $plato)
            <li>{{ $plato['nombre'] }} · $ {{ number_format($plato['precio'], 2, ',', '.') }}</li>
        @endforeach
    </ul>
</x-layout>
```

`tests/Feature/CartaTest.php`
```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class CartaTest extends TestCase
{
    public function test_la_carta_completa_muestra_todo_con_precios(): void
    {
        $this->get('/carta')
            ->assertOk()
            ->assertSee('5 platos')
            ->assertSeeInOrder(['Rabas', 'Empanadas de pescado', 'Merluza a la romana', 'Cazuela de mariscos', 'Flan casero'])
            ->assertSee('$ 14.750,50')
            ->assertSee('$ 5.200,00');
    }

    public function test_una_categoria_muestra_solo_sus_platos(): void
    {
        $this->get('/carta/postres')
            ->assertOk()
            ->assertSee('1 plato')
            ->assertSee('Flan casero')
            ->assertDontSee('Rabas');
    }

    public function test_los_enlaces_salen_de_las_rutas(): void
    {
        $this->get('/carta')->assertSee(route('carta', 'principales'));
    }

    public function test_una_categoria_que_no_existe_da_404(): void
    {
        $this->get('/carta/bebidas')->assertNotFound();
    }
}
```

### Misión S02-N01-M2 · El conversor de nudos

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Los capitanes miden la velocidad en **nudos** (1 nudo = 1,852 km/h). Armá un conversor
con un `ConversorController` y dos rutas con nombre:

- `GET /conversor` (`conversor`): muestra un formulario (método GET) con un campo
  `nudos`. Si llega `?nudos=12`, **redirige** a `/conversor/12`. Si llega algo que no es
  un entero (`?nudos=doce`), vuelve a mostrar el formulario con el mensaje
  `Escribí una cantidad entera de nudos.`
- `GET /conversor/{nudos}` (`conversor.resultado`): solo acepta números
  (`whereNumber`) y muestra `12 nudos son 22,22 km/h`, con un enlace para convertir otro.

Probá los cuatro casos: el formulario, la redirección, el resultado y el 404 de
`/conversor/doce`, además del mensaje de error. Entregá el proyecto en un zip.

#### Criterio de aprobación

- La redirección usa `redirect()->route(...)` y el resultado tiene la restricción numérica.
- La conversión se muestra con dos decimales y coma.
- Las pruebas cubren los cinco casos y pasan.

#### Solución de referencia

`routes/web.php`
```php
<?php

use App\Http\Controllers\ConversorController;
use Illuminate\Support\Facades\Route;

Route::get('/conversor', [ConversorController::class, 'formulario'])->name('conversor');
Route::get('/conversor/{nudos}', [ConversorController::class, 'resultado'])
    ->whereNumber('nudos')
    ->name('conversor.resultado');
```

`app/Http/Controllers/ConversorController.php`
```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class ConversorController extends Controller
{
    private const KMH_POR_NUDO = 1.852;

    public function formulario(Request $request): View|RedirectResponse
    {
        $nudos = $request->query('nudos');
        if ($nudos === null) {
            return view('conversor.formulario', ['error' => null]);
        }
        if (! is_string($nudos) || ! ctype_digit($nudos)) {
            return view('conversor.formulario', ['error' => 'Escribí una cantidad entera de nudos.']);
        }

        return redirect()->route('conversor.resultado', ['nudos' => $nudos]);
    }

    public function resultado(string $nudos): View
    {
        $kmh = (int) $nudos * self::KMH_POR_NUDO;

        return view('conversor.resultado', ['nudos' => (int) $nudos, 'kmh' => $kmh]);
    }
}
```

`resources/views/conversor/formulario.blade.php`
```blade
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Conversor de nudos</title></head>
<body>
    <h1>Conversor de nudos</h1>
    @if ($error)
        <p class="error">{{ $error }}</p>
    @endif
    <form action="{{ route('conversor') }}" method="get">
        <label>Nudos <input name="nudos" value="{{ request('nudos') }}"></label>
        <button>Convertir</button>
    </form>
</body>
</html>
```

`resources/views/conversor/resultado.blade.php`
```blade
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>{{ $nudos }} nudos</title></head>
<body>
    <p>{{ $nudos }} nudos son {{ number_format($kmh, 2, ',', '.') }} km/h</p>
    <a href="{{ route('conversor') }}">Convertir otro</a>
</body>
</html>
```

`tests/Feature/ConversorTest.php`
```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ConversorTest extends TestCase
{
    public function test_muestra_el_formulario(): void
    {
        $this->get('/conversor')->assertOk()->assertSee('name="nudos"', false);
    }

    public function test_redirige_al_resultado(): void
    {
        $this->get('/conversor?nudos=12')->assertRedirect(route('conversor.resultado', 12));
    }

    public function test_convierte_a_kilometros_por_hora(): void
    {
        $this->get('/conversor/12')->assertOk()->assertSee('12 nudos son 22,22 km/h');
    }

    public function test_avisa_si_no_es_un_entero(): void
    {
        $this->get('/conversor?nudos=doce')
            ->assertOk()
            ->assertSee('Escribí una cantidad entera de nudos.')
            ->assertSee('value="doce"', false);
    }

    public function test_el_resultado_solo_acepta_numeros(): void
    {
        $this->get('/conversor/doce')->assertNotFound();
    }
}
```

### Misión S02-N01-M3 · El menú del puerto

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá el sitio institucional del Puerto con tres páginas hechas con `Route::view` y
nombre: `/` (`inicio`), `/horarios` (`horarios`) y `/contacto` (`contacto`). Las tres
usan un componente `<x-layout>` que recibe el título y dibuja un **menú** con enlaces a
las tres páginas; el enlace de la página actual lleva la clase `activo` (usá
`request()->routeIs()` y `@class`). Los horarios (lunes a viernes 8 a 18, sábados 9 a
13) se muestran en una tabla. El `<title>` de cada página es `Título · Puerto`.

Probá que las tres páginas respondan, que el título sea el correcto y que en
`/horarios` el enlace activo sea el de Horarios y no el de Inicio. Entregá el proyecto
en un zip.

#### Criterio de aprobación

- El menú está en el componente (no repetido en cada vista) y los enlaces salen de `route()`.
- Solo el enlace de la página actual tiene la clase `activo`.
- Las pruebas pasan.

#### Solución de referencia

`routes/web.php`
```php
<?php

use Illuminate\Support\Facades\Route;

Route::view('/', 'paginas.inicio')->name('inicio');
Route::view('/horarios', 'paginas.horarios')->name('horarios');
Route::view('/contacto', 'paginas.contacto')->name('contacto');
```

`resources/views/components/layout.blade.php`
```blade
@props(['titulo'])
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>{{ $titulo }} · Puerto</title>
</head>
<body>
    <nav>
        @foreach (['inicio' => 'Inicio', 'horarios' => 'Horarios', 'contacto' => 'Contacto'] as $ruta => $texto)
            <a href="{{ route($ruta) }}" @class(['activo' => request()->routeIs($ruta)])>{{ $texto }}</a>
        @endforeach
    </nav>
    <main>{{ $slot }}</main>
</body>
</html>
```

`resources/views/paginas/inicio.blade.php`
```blade
<x-layout titulo="Inicio">
    <h1>Puerto de los Mensajeros</h1>
    <p>Todos los pedidos, despachados con su sello.</p>
</x-layout>
```

`resources/views/paginas/horarios.blade.php`
```blade
<x-layout titulo="Horarios">
    <h1>Horarios de atención</h1>
    <table>
        <tr><td>Lunes a viernes</td><td>8 a 18</td></tr>
        <tr><td>Sábados</td><td>9 a 13</td></tr>
    </table>
</x-layout>
```

`resources/views/paginas/contacto.blade.php`
```blade
<x-layout titulo="Contacto">
    <h1>Contacto</h1>
    <p>Escribinos a la torre del Puerto: torre@puerto.test</p>
</x-layout>
```

`tests/Feature/MenuTest.php`
```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class MenuTest extends TestCase
{
    public function test_las_tres_paginas_responden_con_su_titulo(): void
    {
        $this->get('/')->assertOk()->assertSee('<title>Inicio · Puerto</title>', false);
        $this->get('/horarios')->assertOk()->assertSee('<title>Horarios · Puerto</title>', false);
        $this->get('/contacto')->assertOk()->assertSee('<title>Contacto · Puerto</title>', false);
    }

    public function test_marca_solo_el_enlace_actual(): void
    {
        $this->get('/horarios')
            ->assertSee('<a href="' . route('horarios') . '" class="activo">Horarios</a>', false)
            ->assertDontSee('class="activo">Inicio', false);
    }

    public function test_muestra_los_horarios(): void
    {
        $this->get('/horarios')->assertSeeInOrder(['Lunes a viernes', '8 a 18', 'Sábados', '9 a 13']);
    }
}
```

### Encargo S02-N01-E1 · Los avisos del faro

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

El faro publica **avisos a los navegantes**, cada uno con número, título, nivel
(`info`, `alerta` o `peligro`) y texto. Guardá cinco avisos en un `AvisoController` y
armá:

- `/avisos`: la lista con un **resumen** arriba (`2 de peligro · 1 de alerta · 2 de
  info`, con `countBy` de las colecciones) y cada aviso con su nivel en mayúsculas;
  con `?nivel=peligro` filtra, y si el nivel no tiene avisos (o no existe) muestra
  `No hay avisos de ese nivel.` (usá `@forelse`).
- `/avisos/{numero}` (solo números): el aviso completo, con la clase CSS `aviso-peligro`,
  `aviso-alerta` o `aviso-info` según el nivel; 404 si no existe.

Escribí las pruebas: el resumen, el filtro, el caso vacío, el detalle con su clase y el
404. Entregá el proyecto en un zip.

#### Criterio de aprobación

- El resumen sale de `countBy` y el filtro usa `when`.
- El detalle arma la clase según el nivel y responde 404 cuando corresponde.
- Las pruebas pasan.

#### Solución de referencia

`routes/web.php`
```php
<?php

use App\Http\Controllers\AvisoController;
use Illuminate\Support\Facades\Route;

Route::get('/avisos', [AvisoController::class, 'index'])->name('avisos.index');
Route::get('/avisos/{numero}', [AvisoController::class, 'show'])->whereNumber('numero')->name('avisos.show');
```

`app/Http/Controllers/AvisoController.php`
```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Collection;
use Illuminate\View\View;

class AvisoController extends Controller
{
    private function avisos(): Collection
    {
        return collect([
            ['numero' => 1, 'nivel' => 'peligro', 'titulo' => 'Tormenta en la bahía', 'texto' => 'Vientos de 80 km/h desde las 18.'],
            ['numero' => 2, 'nivel' => 'info', 'titulo' => 'Nuevo muelle', 'texto' => 'Habilitado el muelle 7 para cabotaje.'],
            ['numero' => 3, 'nivel' => 'alerta', 'titulo' => 'Niebla matinal', 'texto' => 'Visibilidad reducida hasta las 10.'],
            ['numero' => 4, 'nivel' => 'peligro', 'titulo' => 'Restos flotando', 'texto' => 'Contenedor a la deriva frente a la boya 3.'],
            ['numero' => 5, 'nivel' => 'info', 'titulo' => 'Faro en mantenimiento', 'texto' => 'Luz de respaldo el jueves por la noche.'],
        ])->keyBy('numero');
    }

    public function index(Request $request): View
    {
        $nivel = $request->query('nivel');
        $todos = $this->avisos();

        return view('avisos.index', [
            'resumen' => $todos->countBy('nivel')->sortKeys(),
            'avisos' => $todos->when($nivel, fn ($avisos) => $avisos->where('nivel', $nivel)),
        ]);
    }

    public function show(int $numero): View
    {
        $aviso = $this->avisos()->get($numero) ?? abort(404);

        return view('avisos.show', ['aviso' => $aviso]);
    }
}
```

`resources/views/components/layout.blade.php`
```blade
@props(['titulo' => 'Avisos'])
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>{{ $titulo }} · Faro</title></head>
<body>
    <main>{{ $slot }}</main>
</body>
</html>
```

`resources/views/avisos/index.blade.php`
```blade
<x-layout titulo="Avisos a los navegantes">
    <h1>Avisos a los navegantes</h1>
    <p>
        @foreach ($resumen as $nivel => $cantidad)
            {{ $cantidad }} de {{ $nivel }}@if (! $loop->last) · @endif
        @endforeach
    </p>
    <ul>
        @forelse ($avisos as $aviso)
            <li>
                <strong>{{ strtoupper($aviso['nivel']) }}</strong>
                <a href="{{ route('avisos.show', $aviso['numero']) }}">{{ $aviso['titulo'] }}</a>
            </li>
        @empty
            <li>No hay avisos de ese nivel.</li>
        @endforelse
    </ul>
</x-layout>
```

`resources/views/avisos/show.blade.php`
```blade
<x-layout :titulo="$aviso['titulo']">
    <article @class(['aviso', 'aviso-' . $aviso['nivel']])>
        <h1>Aviso {{ $aviso['numero'] }} · {{ $aviso['titulo'] }}</h1>
        <p>{{ $aviso['texto'] }}</p>
    </article>
    <a href="{{ route('avisos.index') }}">Todos los avisos</a>
</x-layout>
```

`tests/Feature/AvisosTest.php`
```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class AvisosTest extends TestCase
{
    public function test_muestra_el_resumen_por_nivel(): void
    {
        $this->get('/avisos')->assertOk()->assertSee('1 de alerta')->assertSee('2 de info')->assertSee('2 de peligro');
    }

    public function test_filtra_por_nivel(): void
    {
        $this->get('/avisos?nivel=peligro')
            ->assertSee('Tormenta en la bahía')
            ->assertSee('Restos flotando')
            ->assertDontSee('Niebla matinal');
    }

    public function test_avisa_cuando_no_hay_avisos(): void
    {
        $this->get('/avisos?nivel=calma')->assertSee('No hay avisos de ese nivel.');
    }

    public function test_el_detalle_lleva_la_clase_del_nivel(): void
    {
        $this->get('/avisos/3')
            ->assertOk()
            ->assertSee('class="aviso aviso-alerta"', false)
            ->assertSee('Visibilidad reducida hasta las 10.');
    }

    public function test_un_aviso_que_no_existe_da_404(): void
    {
        $this->get('/avisos/99')->assertNotFound();
    }
}
```

### Prueba del sello

#### ¿Qué diferencia hay entre `{{ $texto }}` y `{!! $texto !!}` en Blade?

`{{ }}` escapa el texto con `htmlspecialchars` (seguro contra XSS); `{!! !!}` lo muestra tal cual, y solo se usa con HTML en el que confiás.

#### ¿Para qué sirve ponerle nombre a una ruta?

Para generar la URL con `route('nombre', $parametros)` en lugar de escribirla: si la URL cambia, los enlaces y redirecciones siguen funcionando.

#### ¿Qué pasa si pedís `/carta/bebidas` y la ruta tiene `->whereIn('categoria', [...])` sin `bebidas`?

La ruta no coincide y Laravel responde 404 sin llegar al controlador.

#### ¿Dónde busca Laravel la vista `salidas.show`?

En `resources/views/salidas/show.blade.php`: cada punto es una carpeta.

#### ¿Qué hace `$this->get('/salidas')->assertOk()` en una prueba?

Pide la página a la aplicación sin servidor ni navegador y comprueba que respondió 200.

### Soluciones (docente)

Contenido nuevo (en FullCursos no hay Laravel). Las soluciones se verifican sobre un proyecto limpio de Laravel 12 (`composer create-project laravel/laravel:^12.0`) con `php artisan test`. Se corrige descomprimiendo el zip, corriendo `composer install`, `cp .env.example .env`, `php artisan key:generate` y `php artisan test`, y mirando las páginas con `php artisan serve`.

## S02-N02 · Migraciones, Eloquent y formularios con MariaDB

```meta
tipo: tema
padre: S02-N01
precio: 10
criatura: troll
ejecutable: no
```

### Crónica

En el sótano de la Ciudadela hay una bodega que no se parece a la del Puerto: no hay que escribir `CREATE TABLE` a mano ni armar cada consulta con `prepare`. Las tablas se describen en unos pergaminos numerados —las **migraciones**— y cada registro se maneja como un objeto. Un guardia revisa cada formulario antes de que toque la bodega: si falta un dato, lo devuelve con una nota que dice qué corregir.

—Es la misma MariaDB de siempre, {heroe} —dice {mentor}—. Laravel escribe el SQL por vos, con consultas preparadas, y te deja pensar en barcos y viajes en lugar de filas y columnas. Pero no te olvides de lo que pasa abajo: cuando algo falle, lo vas a encontrar porque sabés SQL.

### Objetivos

- Conectar Laravel con MariaDB o MySQL desde el `.env`.
- Describir las tablas con migraciones y cargarlas con seeders y factories.
- Consultar y modificar datos con Eloquent, incluidas las relaciones uno a muchos.
- Armar un ABM con `Route::resource`, formularios con `@csrf`, validación y mensajes en español.
- Probar con una base de datos que se reinicia en cada prueba.

### Antes de empezar

- El nodo anterior (rutas, controladores y Blade) y la Bodega del Puerto (R04), en especial relaciones, `JOIN` y consultas preparadas.

### Explicación

#### Conectar con MariaDB
El proyecto nuevo viene configurado con SQLite. Para usar MariaDB (o MySQL), creá la
base en phpMyAdmin o en la consola:
```sql
CREATE DATABASE ciudadela CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
y cambiá estas líneas del `.env`:
```ini
DB_CONNECTION=mariadb
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=ciudadela
DB_USERNAME=root
DB_PASSWORD=
```
(con MySQL, `DB_CONNECTION=mysql`). Después, `php artisan migrate` crea las tablas.
Las **pruebas** no tocan esa base: el `phpunit.xml` del proyecto usa SQLite en memoria,
que se crea y se destruye en cada corrida. El mismo código funciona en las dos porque
Laravel arma el SQL según el motor.

#### Migraciones
Una migración es una clase que **crea o cambia** una tabla. Se versionan con el código:
cualquiera que baje el proyecto corre `php artisan migrate` y tiene las mismas tablas.
```bash
php artisan make:model Barco -mf     # el modelo, su migración (-m) y su factory (-f)
```
```php
Schema::create('barcos', function (Blueprint $table) {
    $table->id();                                  // BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY
    $table->string('nombre', 60)->unique();        // VARCHAR(60) con índice único
    $table->string('bandera', 40);
    $table->decimal('eslora', 6, 2);               // DECIMAL(6,2)
    $table->timestamps();                          // created_at y updated_at
});
```
| Método | Columna |
|---|---|
| `string('x', 80)` | `VARCHAR(80)` |
| `text('x')` | `TEXT` |
| `integer('x')`, `unsignedInteger('x')` | `INT` |
| `decimal('x', 10, 2)` | `DECIMAL(10,2)` |
| `boolean('x')` | `TINYINT(1)` |
| `date('x')`, `dateTime('x')` | `DATE`, `DATETIME` |
| `foreignId('barco_id')->constrained()` | `BIGINT UNSIGNED` + clave foránea a `barcos.id` |
| `->nullable()`, `->default(0)`, `->unique()` | modificadores |

| Comando | Hace |
|---|---|
| `php artisan migrate` | corre las migraciones que faltan |
| `php artisan migrate:rollback` | deshace la última tanda |
| `php artisan migrate:fresh --seed` | borra todo, migra de cero y carga los seeders |

Una migración que ya corrió en el servidor **no se edita**: para cambiar la tabla se
escribe otra (`Schema::table('barcos', fn ($t) => $t->string('puerto')->nullable())`).

#### Eloquent: la tabla hecha clase
Cada tabla tiene un **modelo**. Por convención, el modelo `Barco` usa la tabla `barcos`
(el plural en inglés: casi siempre agrega una `s`; si no te sirve, `protected $table = 'camiones';`).
```php
class Barco extends Model
{
    protected $fillable = ['nombre', 'bandera', 'eslora'];    // lo que se puede asignar en masa
    protected function casts(): array
    {
        return ['eslora' => 'decimal:2'];
    }
}
```
```php
$barco = Barco::create(['nombre' => 'Albatros', 'bandera' => 'Argentina', 'eslora' => 32.5]);
Barco::orderBy('nombre')->get();                  // SELECT * FROM barcos ORDER BY nombre
Barco::where('bandera', 'Uruguay')->count();
Barco::find(3);                                   // o null
Barco::findOrFail(3);                             // o 404
$barco->update(['eslora' => 33]);
$barco->delete();
Barco::where('nombre', 'like', "%{$texto}%")->paginate(5);   // de a 5, con ?page=2
```
Todas estas consultas son **preparadas**: el valor viaja aparte, como con PDO. En la
vista, `{{ $barcos->links() }}` dibuja los enlaces de las páginas, y
`->withQueryString()` los hace conservar los filtros (`?buscar=…`).

`$fillable` es una defensa: `Barco::create($request->all())` sin ella dejaría que
alguien agregue al formulario un campo que no pusiste (como `es_admin`).

#### Relaciones
Un barco hace muchos viajes; cada viaje es de un barco:
```php
// migración de viajes
$table->foreignId('barco_id')->constrained()->cascadeOnDelete();

class Barco extends Model
{
    public function viajes(): HasMany { return $this->hasMany(Viaje::class); }
}
class Viaje extends Model
{
    public function barco(): BelongsTo { return $this->belongsTo(Barco::class); }
}
```
```php
$barco->viajes;                               // la colección de sus viajes
$barco->viajes()->create(['destino' => 'Colonia', ...]);   // barco_id se completa solo
$viaje->barco->nombre;
Viaje::with('barco')->get();                  // trae los barcos en UNA consulta más
```
Sin `with`, recorrer 100 viajes y mostrar `$viaje->barco->nombre` hace 101 consultas
(el problema "N+1").

#### Formularios, validación y ABM
`Route::resource('barcos', BarcoController::class)` crea las siete rutas de un ABM:
| Verbo y ruta | Método | Nombre |
|---|---|---|
| `GET /barcos` | `index` | `barcos.index` |
| `GET /barcos/create` | `create` | `barcos.create` |
| `POST /barcos` | `store` | `barcos.store` |
| `GET /barcos/{barco}` | `show` | `barcos.show` |
| `GET /barcos/{barco}/edit` | `edit` | `barcos.edit` |
| `PUT /barcos/{barco}` | `update` | `barcos.update` |
| `DELETE /barcos/{barco}` | `destroy` | `barcos.destroy` |

(`->except('show')` o `->only([...])` para quedarte con algunas). Si el método recibe
`Barco $barco`, Laravel busca el barco por el `id` de la URL y responde **404** si no
existe: es el *route model binding*.

Todo formulario `POST` lleva `@csrf` (el token que hiciste a mano en R03-N05; sin él,
error 419). Los navegadores solo mandan GET y POST: `@method('PUT')` y
`@method('DELETE')` agregan un campo oculto que Laravel entiende.

```php
$datos = $request->validate([
    'nombre' => ['required', 'string', 'max:60', Rule::unique('barcos')->ignore($barco?->id)],
    'eslora' => ['required', 'numeric', 'between:3,400'],
], [
    'nombre.required' => 'Poné el nombre del barco.',
    'nombre.unique' => 'Ya hay un barco con ese nombre.',
]);
```
Si algo no pasa, `validate` **vuelve al formulario solo**, con los errores y lo que el
usuario había escrito. En la vista, `old('nombre', $barco->nombre)` recupera el valor y
`@error('nombre') … {{ $message }} … @enderror` muestra el mensaje. Si pasa, devuelve
solo los campos validados: pasalos a `create` o `update`.

Después de guardar se **redirige** (el patrón PRG de R03-N03) con un mensaje de una sola
vez: `redirect()->route('barcos.index')->with('ok', 'Barco registrado.')`, y la vista lo
lee con `session('ok')`.

Otras reglas útiles: `email`, `integer`, `min:10` (en textos, caracteres), `in:a,b,c`,
`date`, `after_or_equal:today`, `exists:barcos,id`, `nullable`.

#### Probar con base de datos
```php
use RefreshDatabase;       // cada prueba arranca con las tablas vacías y recién migradas

Barco::factory()->count(3)->create();                  // datos de prueba con la factory
$this->post('/barcos', [...])->assertRedirect(route('barcos.index'));
$this->assertDatabaseHas('barcos', ['nombre' => 'Albatros']);
$this->post('/barcos', [])->assertSessionHasErrors(['nombre', 'eslora']);
$this->seed();             // corre el DatabaseSeeder
```

### Código de ejemplo

El **registro de barcos** del Puerto: un ABM completo con MariaDB, validación en
español y pruebas.

`database/migrations/2026_09_01_000001_create_barcos_table.php`
```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('barcos', function (Blueprint $table) {
            $table->id();
            $table->string('nombre', 60)->unique();
            $table->string('bandera', 40);
            $table->decimal('eslora', 6, 2);
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('barcos');
    }
};
```

`app/Models/Barco.php`
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Barco extends Model
{
    use HasFactory;

    protected $fillable = ['nombre', 'bandera', 'eslora'];

    protected function casts(): array
    {
        return ['eslora' => 'decimal:2'];
    }
}
```

`database/factories/BarcoFactory.php`
```php
<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

class BarcoFactory extends Factory
{
    public function definition(): array
    {
        return [
            'nombre' => ucfirst(fake()->unique()->word()) . ' ' . fake()->numberBetween(1, 99),
            'bandera' => fake()->randomElement(['Argentina', 'Uruguay', 'Brasil', 'Chile']),
            'eslora' => fake()->randomFloat(2, 8, 120),
        ];
    }
}
```

`database/seeders/DatabaseSeeder.php`
```php
<?php

namespace Database\Seeders;

use App\Models\Barco;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        Barco::create(['nombre' => 'Albatros', 'bandera' => 'Argentina', 'eslora' => 32.5]);
        Barco::create(['nombre' => 'Gaviota', 'bandera' => 'Uruguay', 'eslora' => 18]);
        Barco::create(['nombre' => 'Estrella del Sur', 'bandera' => 'Argentina', 'eslora' => 54.2]);
    }
}
```

`routes/web.php`
```php
<?php

use App\Http\Controllers\BarcoController;
use Illuminate\Support\Facades\Route;

Route::redirect('/', '/barcos');
Route::resource('barcos', BarcoController::class)->except('show');
```

`app/Http/Controllers/BarcoController.php`
```php
<?php

namespace App\Http\Controllers;

use App\Models\Barco;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Validation\Rule;
use Illuminate\View\View;

class BarcoController extends Controller
{
    private const MENSAJES = [
        'nombre.required' => 'Poné el nombre del barco.',
        'nombre.max' => 'El nombre tiene hasta 60 letras.',
        'nombre.unique' => 'Ya hay un barco con ese nombre.',
        'bandera.required' => 'Poné la bandera.',
        'eslora.required' => 'Poné la eslora.',
        'eslora.numeric' => 'La eslora es un número de metros.',
        'eslora.between' => 'La eslora va de 3 a 400 metros.',
    ];

    public function index(): View
    {
        return view('barcos.index', ['barcos' => Barco::orderBy('nombre')->get()]);
    }

    public function create(): View
    {
        return view('barcos.create', ['barco' => new Barco()]);
    }

    public function store(Request $request): RedirectResponse
    {
        $barco = Barco::create($this->validar($request));

        return redirect()->route('barcos.index')->with('ok', "Barco «{$barco->nombre}» registrado.");
    }

    public function edit(Barco $barco): View
    {
        return view('barcos.edit', ['barco' => $barco]);
    }

    public function update(Request $request, Barco $barco): RedirectResponse
    {
        $barco->update($this->validar($request, $barco));

        return redirect()->route('barcos.index')->with('ok', "Barco «{$barco->nombre}» actualizado.");
    }

    public function destroy(Barco $barco): RedirectResponse
    {
        $barco->delete();

        return redirect()->route('barcos.index')->with('ok', "Barco «{$barco->nombre}» dado de baja.");
    }

    private function validar(Request $request, ?Barco $barco = null): array
    {
        return $request->validate([
            'nombre' => ['required', 'string', 'max:60', Rule::unique('barcos')->ignore($barco?->id)],
            'bandera' => ['required', 'string', 'max:40'],
            'eslora' => ['required', 'numeric', 'between:3,400'],
        ], self::MENSAJES);
    }
}
```

`resources/views/components/layout.blade.php`
```blade
@props(['titulo' => 'Registro de barcos'])
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>{{ $titulo }} · Puerto</title>
</head>
<body>
    @if (session('ok'))
        <p class="ok">{{ session('ok') }}</p>
    @endif
    <main>{{ $slot }}</main>
</body>
</html>
```

`resources/views/barcos/index.blade.php`
```blade
<x-layout>
    <h1>Registro de barcos</h1>
    <a href="{{ route('barcos.create') }}">Registrar un barco</a>
    <table>
        <tr><th>Nombre</th><th>Bandera</th><th>Eslora</th><th></th></tr>
        @forelse ($barcos as $barco)
            <tr>
                <td>{{ $barco->nombre }}</td>
                <td>{{ $barco->bandera }}</td>
                <td>{{ number_format($barco->eslora, 2, ',', '.') }} m</td>
                <td>
                    <a href="{{ route('barcos.edit', $barco) }}">Editar</a>
                    <form action="{{ route('barcos.destroy', $barco) }}" method="post">
                        @csrf
                        @method('DELETE')
                        <button>Dar de baja</button>
                    </form>
                </td>
            </tr>
        @empty
            <tr><td colspan="4">Todavía no hay barcos registrados.</td></tr>
        @endforelse
    </table>
</x-layout>
```

`resources/views/barcos/_campos.blade.php`
```blade
@csrf
<label>Nombre <input name="nombre" value="{{ old('nombre', $barco->nombre) }}"></label>
@error('nombre') <p class="error">{{ $message }}</p> @enderror
<label>Bandera <input name="bandera" value="{{ old('bandera', $barco->bandera) }}"></label>
@error('bandera') <p class="error">{{ $message }}</p> @enderror
<label>Eslora (m) <input name="eslora" value="{{ old('eslora', $barco->eslora) }}"></label>
@error('eslora') <p class="error">{{ $message }}</p> @enderror
<button>Guardar</button>
```

`resources/views/barcos/create.blade.php`
```blade
<x-layout titulo="Registrar un barco">
    <h1>Registrar un barco</h1>
    <form action="{{ route('barcos.store') }}" method="post">
        @include('barcos._campos')
    </form>
</x-layout>
```

`resources/views/barcos/edit.blade.php`
```blade
<x-layout :titulo="'Editar ' . $barco->nombre">
    <h1>Editar {{ $barco->nombre }}</h1>
    <form action="{{ route('barcos.update', $barco) }}" method="post">
        @method('PUT')
        @include('barcos._campos')
    </form>
</x-layout>
```

`tests/Feature/BarcosTest.php`
```php
<?php

namespace Tests\Feature;

use App\Models\Barco;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class BarcosTest extends TestCase
{
    use RefreshDatabase;

    public function test_lista_los_barcos_por_nombre(): void
    {
        $this->seed();

        $this->get('/barcos')
            ->assertOk()
            ->assertSeeInOrder(['Albatros', 'Estrella del Sur', 'Gaviota'])
            ->assertSee('54,20 m');
    }

    public function test_registra_un_barco(): void
    {
        $this->post('/barcos', ['nombre' => 'Tritón', 'bandera' => 'Chile', 'eslora' => '41.5'])
            ->assertRedirect(route('barcos.index'))
            ->assertSessionHas('ok', 'Barco «Tritón» registrado.');

        $this->assertDatabaseHas('barcos', ['nombre' => 'Tritón', 'bandera' => 'Chile']);
    }

    public function test_rechaza_datos_invalidos_con_mensajes_en_espanol(): void
    {
        $this->from('/barcos/create')
            ->post('/barcos', ['nombre' => '', 'bandera' => 'Chile', 'eslora' => '2'])
            ->assertRedirect('/barcos/create')
            ->assertSessionHasErrors([
                'nombre' => 'Poné el nombre del barco.',
                'eslora' => 'La eslora va de 3 a 400 metros.',
            ]);

        $this->assertDatabaseCount('barcos', 0);
    }

    public function test_no_repite_nombres_pero_deja_editar_el_propio(): void
    {
        $albatros = Barco::factory()->create(['nombre' => 'Albatros']);

        $this->post('/barcos', ['nombre' => 'Albatros', 'bandera' => 'Chile', 'eslora' => 10])
            ->assertSessionHasErrors(['nombre' => 'Ya hay un barco con ese nombre.']);

        $this->put("/barcos/{$albatros->id}", ['nombre' => 'Albatros', 'bandera' => 'Brasil', 'eslora' => 30])
            ->assertSessionHasNoErrors();
        $this->assertSame('Brasil', $albatros->fresh()->bandera);
    }

    public function test_da_de_baja_un_barco(): void
    {
        $barco = Barco::factory()->create();

        $this->delete("/barcos/{$barco->id}")->assertRedirect(route('barcos.index'));
        $this->assertModelMissing($barco);
    }

    public function test_editar_un_barco_que_no_existe_da_404(): void
    {
        $this->get('/barcos/99/edit')->assertNotFound();
    }
}
```

Con MariaDB configurada: `php artisan migrate:fresh --seed`, `php artisan serve` y
probá el ABM en `/barcos`. Mirá también la tabla en phpMyAdmin: son filas comunes, con
`created_at` y `updated_at` completados por Laravel.

### ¿Para qué sirve?

Casi todo sistema de gestión es un conjunto de ABM con relaciones: clientes y facturas, alumnos y notas, barcos y viajes. Con migraciones, Eloquent y la validación de Laravel, un ABM completo y seguro (consultas preparadas, CSRF, datos validados) sale en una tarde, y las migraciones hacen que el mismo esquema se arme igual en tu compu, en la de un compañero y en el hosting.

### Errores habituales

**Troll: `Add [nombre] to fillable property`.** `create` con un campo que no está en
`$fillable`: Laravel lo frena para protegerte. Agregalo a la lista (solo si el usuario
puede cargarlo).

**Troll: `Attempt to read property "nombre" on null`.** `Barco::find` no encontró nada
y devolvió `null`. Usá `findOrFail` o el *route model binding*, que responden 404.

**Esqueleto: `Table 'ciudadela.barcos' doesn't exist`.** Falta `php artisan migrate`, o
el modelo busca otro nombre de tabla: Laravel pluraliza en inglés, y `Camion` busca
`camions` y `Pais` busca `pais`. Si el nombre no sale solo, poné `protected $table`.

**Goblin: `419 Page Expired`.** El formulario no tiene `@csrf` (o la sesión venció).

**Ogro: editar una migración que ya corrió.** En tu compu la arreglás con
`migrate:fresh`, pero en el servidor ya está aplicada y el cambio nunca llega. Siempre
una migración nueva.

**Ogro: `unique` que no deja editar.** Al editar, el barco "choca" consigo mismo.
`Rule::unique('barcos')->ignore($barco->id)`.

**Esqueleto: `SQLSTATE[HY000] [1045] Access denied`.** Usuario o clave del `.env`
equivocados, o MariaDB apagado. Después de cambiar el `.env` con el servidor andando,
reinicialo (`php artisan serve`).

### Misión S02-N02-M1 · La bodega con stock

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Creá el modelo `Producto` con su migración: `nombre` (hasta 80 letras), `precio`
(`DECIMAL(10,2)`) y `stock` (entero sin signo). El `DatabaseSeeder` carga:

| Nombre | Precio | Stock |
|---|---|---|
| Soga de amarre | 8500 | 12 |
| Farol a querosén | 23000 | 0 |
| Ancla chica | 61000.5 | 3 |
| Boya naranja | 4200 | 25 |

La página `/productos` muestra solo los productos **con stock**, ordenados por nombre,
cada uno con su precio y stock; abajo, `Sin stock: 1 producto` (o `N productos`) y el
**valor de la bodega** (la suma de precio × stock de todos): `Valor de la bodega:
$ 390.001,50`. Probala con `RefreshDatabase` y `$this->seed()`, y corré
`php artisan migrate:fresh --seed` contra tu MariaDB. Entregá el proyecto en un zip.

#### Criterio de aprobación

- La tabla sale de una migración y los datos de un seeder.
- Las consultas usan Eloquent (`where`, `orderBy`) y el valor total se calcula bien.
- Las pruebas pasan y el proyecto migra en MariaDB.

#### Solución de referencia

`database/migrations/2026_09_01_000001_create_productos_table.php`
```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('productos', function (Blueprint $table) {
            $table->id();
            $table->string('nombre', 80);
            $table->decimal('precio', 10, 2);
            $table->unsignedInteger('stock');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('productos');
    }
};
```

`app/Models/Producto.php`
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Producto extends Model
{
    protected $fillable = ['nombre', 'precio', 'stock'];

    protected function casts(): array
    {
        return ['precio' => 'decimal:2', 'stock' => 'integer'];
    }
}
```

`database/seeders/DatabaseSeeder.php`
```php
<?php

namespace Database\Seeders;

use App\Models\Producto;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        Producto::create(['nombre' => 'Soga de amarre', 'precio' => 8500, 'stock' => 12]);
        Producto::create(['nombre' => 'Farol a querosén', 'precio' => 23000, 'stock' => 0]);
        Producto::create(['nombre' => 'Ancla chica', 'precio' => 61000.5, 'stock' => 3]);
        Producto::create(['nombre' => 'Boya naranja', 'precio' => 4200, 'stock' => 25]);
    }
}
```

`routes/web.php`
```php
<?php

use App\Http\Controllers\ProductoController;
use Illuminate\Support\Facades\Route;

Route::get('/productos', [ProductoController::class, 'index'])->name('productos.index');
```

`app/Http/Controllers/ProductoController.php`
```php
<?php

namespace App\Http\Controllers;

use App\Models\Producto;
use Illuminate\View\View;

class ProductoController extends Controller
{
    public function index(): View
    {
        return view('productos.index', [
            'productos' => Producto::where('stock', '>', 0)->orderBy('nombre')->get(),
            'sinStock' => Producto::where('stock', 0)->count(),
            'valor' => Producto::all()->sum(fn (Producto $p) => $p->precio * $p->stock),
        ]);
    }
}
```

`resources/views/productos/index.blade.php`
```blade
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Bodega</title></head>
<body>
    <h1>La bodega</h1>
    <table>
        <tr><th>Producto</th><th>Precio</th><th>Stock</th></tr>
        @foreach ($productos as $producto)
            <tr>
                <td>{{ $producto->nombre }}</td>
                <td>$ {{ number_format($producto->precio, 2, ',', '.') }}</td>
                <td>{{ $producto->stock }}</td>
            </tr>
        @endforeach
    </table>
    <p>Sin stock: {{ $sinStock }} {{ $sinStock === 1 ? 'producto' : 'productos' }}</p>
    <p>Valor de la bodega: $ {{ number_format($valor, 2, ',', '.') }}</p>
</body>
</html>
```

`tests/Feature/BodegaTest.php`
```php
<?php

namespace Tests\Feature;

use App\Models\Producto;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class BodegaTest extends TestCase
{
    use RefreshDatabase;

    public function test_muestra_solo_lo_que_tiene_stock_por_nombre(): void
    {
        $this->seed();

        $this->get('/productos')
            ->assertOk()
            ->assertSeeInOrder(['Ancla chica', 'Boya naranja', 'Soga de amarre'])
            ->assertDontSee('Farol a querosén')
            ->assertSee('$ 61.000,50');
    }

    public function test_cuenta_lo_que_no_tiene_stock_y_suma_el_valor(): void
    {
        $this->seed();

        $this->get('/productos')
            ->assertSee('Sin stock: 1 producto')
            ->assertSee('Valor de la bodega: $ 390.001,50');
    }

    public function test_con_la_bodega_vacia_el_valor_es_cero(): void
    {
        Producto::create(['nombre' => 'Remo', 'precio' => 900, 'stock' => 0]);

        $this->get('/productos')->assertSee('Sin stock: 1 producto')->assertSee('Valor de la bodega: $ 0,00');
    }
}
```

### Misión S02-N02-M2 · El buzón de reclamos

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá el **buzón de reclamos** del Puerto con el modelo `Reclamo` (`email`, `categoria`,
`texto` y fechas) y dos rutas: `GET /reclamos/create` muestra el formulario y
`POST /reclamos` lo guarda. Reglas:

- `email`: obligatorio y con formato de correo;
- `categoria`: obligatoria, una de `demora`, `carga` o `atencion` (un `<select>`);
- `texto`: obligatorio, de 10 a 500 caracteres.

Cada regla tiene su mensaje **en español**. Si hay errores, el formulario vuelve con los
mensajes debajo de cada campo y con lo que se había escrito (también la categoría
elegida). Si está todo bien, se guarda y se redirige al formulario vacío con el mensaje
`Reclamo N° 1 recibido. Te respondemos a tu@correo.` (con el número y el correo reales).

Probá el reclamo válido (con `assertDatabaseHas`), uno con los tres campos mal (con sus
mensajes, y que no se guardó nada) y que el formulario conserve lo escrito. Entregá el
proyecto en un zip.

#### Criterio de aprobación

- La validación usa `$request->validate` con mensajes propios y `in:` para la categoría.
- El formulario lleva `@csrf`, `old()` y `@error`, y después de guardar se redirige.
- Las pruebas pasan.

#### Solución de referencia

`database/migrations/2026_09_01_000001_create_reclamos_table.php`
```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('reclamos', function (Blueprint $table) {
            $table->id();
            $table->string('email');
            $table->string('categoria', 20);
            $table->text('texto');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('reclamos');
    }
};
```

`app/Models/Reclamo.php`
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Reclamo extends Model
{
    public const CATEGORIAS = ['demora' => 'Demora', 'carga' => 'Carga dañada', 'atencion' => 'Atención'];

    protected $fillable = ['email', 'categoria', 'texto'];
}
```

`routes/web.php`
```php
<?php

use App\Http\Controllers\ReclamoController;
use Illuminate\Support\Facades\Route;

Route::get('/reclamos/create', [ReclamoController::class, 'create'])->name('reclamos.create');
Route::post('/reclamos', [ReclamoController::class, 'store'])->name('reclamos.store');
```

`app/Http/Controllers/ReclamoController.php`
```php
<?php

namespace App\Http\Controllers;

use App\Models\Reclamo;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class ReclamoController extends Controller
{
    public function create(): View
    {
        return view('reclamos.create', ['categorias' => Reclamo::CATEGORIAS]);
    }

    public function store(Request $request): RedirectResponse
    {
        $datos = $request->validate([
            'email' => ['required', 'email'],
            'categoria' => ['required', 'in:' . implode(',', array_keys(Reclamo::CATEGORIAS))],
            'texto' => ['required', 'string', 'between:10,500'],
        ], [
            'email.required' => 'Poné tu correo para poder responderte.',
            'email.email' => 'Ese correo no parece válido.',
            'categoria.required' => 'Elegí de qué se trata.',
            'categoria.in' => 'Elegí una categoría de la lista.',
            'texto.required' => 'Contanos qué pasó.',
            'texto.between' => 'El reclamo tiene que tener entre 10 y 500 letras.',
        ]);

        $reclamo = Reclamo::create($datos);

        return redirect()->route('reclamos.create')
            ->with('ok', "Reclamo N° {$reclamo->id} recibido. Te respondemos a {$reclamo->email}.");
    }
}
```

`resources/views/reclamos/create.blade.php`
```blade
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Buzón de reclamos</title></head>
<body>
    <h1>Buzón de reclamos</h1>
    @if (session('ok'))
        <p class="ok">{{ session('ok') }}</p>
    @endif
    <form action="{{ route('reclamos.store') }}" method="post">
        @csrf
        <label>Correo <input name="email" value="{{ old('email') }}"></label>
        @error('email') <p class="error">{{ $message }}</p> @enderror

        <label>Categoría
            <select name="categoria">
                <option value="">Elegí…</option>
                @foreach ($categorias as $valor => $texto)
                    <option value="{{ $valor }}" @selected(old('categoria') === $valor)>{{ $texto }}</option>
                @endforeach
            </select>
        </label>
        @error('categoria') <p class="error">{{ $message }}</p> @enderror

        <label>Reclamo <textarea name="texto">{{ old('texto') }}</textarea></label>
        @error('texto') <p class="error">{{ $message }}</p> @enderror

        <button>Enviar</button>
    </form>
</body>
</html>
```

`tests/Feature/ReclamosTest.php`
```php
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ReclamosTest extends TestCase
{
    use RefreshDatabase;

    public function test_guarda_un_reclamo_valido(): void
    {
        $this->post('/reclamos', ['email' => 'kira@puerto.test', 'categoria' => 'demora', 'texto' => 'El barco salió dos horas tarde.'])
            ->assertRedirect(route('reclamos.create'))
            ->assertSessionHas('ok', 'Reclamo N° 1 recibido. Te respondemos a kira@puerto.test.');

        $this->assertDatabaseHas('reclamos', ['email' => 'kira@puerto.test', 'categoria' => 'demora']);
    }

    public function test_rechaza_los_tres_campos_mal(): void
    {
        $this->post('/reclamos', ['email' => 'kira', 'categoria' => 'clima', 'texto' => 'Mal.'])
            ->assertSessionHasErrors([
                'email' => 'Ese correo no parece válido.',
                'categoria' => 'Elegí una categoría de la lista.',
                'texto' => 'El reclamo tiene que tener entre 10 y 500 letras.',
            ]);

        $this->assertDatabaseCount('reclamos', 0);
    }

    public function test_el_formulario_conserva_lo_escrito(): void
    {
        $this->followingRedirects()
            ->from('/reclamos/create')
            ->post('/reclamos', ['email' => 'kira@puerto.test', 'categoria' => 'carga', 'texto' => 'Corto'])
            ->assertSee('value="kira@puerto.test"', false)
            ->assertSee('<option value="carga" selected>', false)
            ->assertSee('El reclamo tiene que tener entre 10 y 500 letras.');
    }
}
```

### Misión S02-N02-M3 · Los viajes de cada barco

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Partí del registro de barcos del ejemplo (migración, modelo y seeder) y agregá los
**viajes**: tabla `viajes` con `barco_id` (clave foránea, que se borra con el barco),
`destino`, `fecha` (`DATE`) y `pasajeros` (entero). Relacioná los modelos con `hasMany`
y `belongsTo`.

- `GET /barcos/{barco}`: el barco con sus viajes ordenados por fecha
  (`15/10/2026 · Colonia · 120 pasajeros`), el total de pasajeros y un formulario para
  cargar un viaje nuevo. Si el barco no existe, 404.
- `POST /barcos/{barco}/viajes`: valida (destino obligatorio, fecha válida, pasajeros
  entre 1 y 500) y crea el viaje **a través de la relación**; vuelve a la página del
  barco con el mensaje `Viaje a Colonia agendado.`
- `GET /viajes`: todos los viajes con el nombre de su barco, cargados con `with` (para
  no hacer una consulta por viaje).

Probá las tres rutas, la validación y que al borrar un barco se borren sus viajes.
Entregá el proyecto en un zip.

#### Criterio de aprobación

- La clave foránea está en la migración y las relaciones en los modelos.
- El viaje se crea con `$barco->viajes()->create(...)` y la lista usa `with('barco')`.
- Las pruebas pasan y el proyecto migra en MariaDB.

#### Solución de referencia

`database/migrations/2026_09_01_000001_create_barcos_table.php`
```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('barcos', function (Blueprint $table) {
            $table->id();
            $table->string('nombre', 60)->unique();
            $table->string('bandera', 40);
            $table->decimal('eslora', 6, 2);
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('barcos');
    }
};
```

`database/migrations/2026_09_01_000002_create_viajes_table.php`
```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('viajes', function (Blueprint $table) {
            $table->id();
            $table->foreignId('barco_id')->constrained()->cascadeOnDelete();
            $table->string('destino', 60);
            $table->date('fecha');
            $table->unsignedSmallInteger('pasajeros');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('viajes');
    }
};
```

`app/Models/Barco.php`
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Barco extends Model
{
    use HasFactory;

    protected $fillable = ['nombre', 'bandera', 'eslora'];

    protected function casts(): array
    {
        return ['eslora' => 'decimal:2'];
    }

    public function viajes(): HasMany
    {
        return $this->hasMany(Viaje::class);
    }
}
```

`app/Models/Viaje.php`
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Viaje extends Model
{
    protected $fillable = ['destino', 'fecha', 'pasajeros'];

    protected function casts(): array
    {
        return ['fecha' => 'date', 'pasajeros' => 'integer'];
    }

    public function barco(): BelongsTo
    {
        return $this->belongsTo(Barco::class);
    }
}
```

`database/factories/BarcoFactory.php`
```php
<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

class BarcoFactory extends Factory
{
    public function definition(): array
    {
        return [
            'nombre' => ucfirst(fake()->unique()->word()) . ' ' . fake()->numberBetween(1, 99),
            'bandera' => fake()->randomElement(['Argentina', 'Uruguay', 'Brasil', 'Chile']),
            'eslora' => fake()->randomFloat(2, 8, 120),
        ];
    }
}
```

`database/seeders/DatabaseSeeder.php`
```php
<?php

namespace Database\Seeders;

use App\Models\Barco;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $albatros = Barco::create(['nombre' => 'Albatros', 'bandera' => 'Argentina', 'eslora' => 32.5]);
        $gaviota = Barco::create(['nombre' => 'Gaviota', 'bandera' => 'Uruguay', 'eslora' => 18]);

        $albatros->viajes()->create(['destino' => 'Montevideo', 'fecha' => '2026-10-20', 'pasajeros' => 210]);
        $albatros->viajes()->create(['destino' => 'Colonia', 'fecha' => '2026-10-15', 'pasajeros' => 120]);
        $gaviota->viajes()->create(['destino' => 'Piriápolis', 'fecha' => '2026-10-18', 'pasajeros' => 45]);
    }
}
```

`routes/web.php`
```php
<?php

use App\Http\Controllers\BarcoController;
use App\Http\Controllers\ViajeController;
use Illuminate\Support\Facades\Route;

Route::get('/barcos/{barco}', [BarcoController::class, 'show'])->name('barcos.show');
Route::post('/barcos/{barco}/viajes', [ViajeController::class, 'store'])->name('barcos.viajes.store');
Route::get('/viajes', [ViajeController::class, 'index'])->name('viajes.index');
```

`app/Http/Controllers/BarcoController.php`
```php
<?php

namespace App\Http\Controllers;

use App\Models\Barco;
use Illuminate\View\View;

class BarcoController extends Controller
{
    public function show(Barco $barco): View
    {
        $viajes = $barco->viajes()->orderBy('fecha')->get();

        return view('barcos.show', [
            'barco' => $barco,
            'viajes' => $viajes,
            'pasajeros' => $viajes->sum('pasajeros'),
        ]);
    }
}
```

`app/Http/Controllers/ViajeController.php`
```php
<?php

namespace App\Http\Controllers;

use App\Models\Barco;
use App\Models\Viaje;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class ViajeController extends Controller
{
    public function index(): View
    {
        return view('viajes.index', ['viajes' => Viaje::with('barco')->orderBy('fecha')->get()]);
    }

    public function store(Request $request, Barco $barco): RedirectResponse
    {
        $datos = $request->validate([
            'destino' => ['required', 'string', 'max:60'],
            'fecha' => ['required', 'date'],
            'pasajeros' => ['required', 'integer', 'between:1,500'],
        ], [
            'destino.required' => 'Poné el destino.',
            'fecha.required' => 'Poné la fecha del viaje.',
            'fecha.date' => 'Esa fecha no es válida.',
            'pasajeros.required' => 'Poné la cantidad de pasajeros.',
            'pasajeros.between' => 'Los pasajeros van de 1 a 500.',
        ]);

        $viaje = $barco->viajes()->create($datos);

        return redirect()->route('barcos.show', $barco)->with('ok', "Viaje a {$viaje->destino} agendado.");
    }
}
```

`resources/views/barcos/show.blade.php`
```blade
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>{{ $barco->nombre }}</title></head>
<body>
    <h1>{{ $barco->nombre }} ({{ $barco->bandera }})</h1>
    @if (session('ok'))
        <p class="ok">{{ session('ok') }}</p>
    @endif
    <ul>
        @forelse ($viajes as $viaje)
            <li>{{ $viaje->fecha->format('d/m/Y') }} · {{ $viaje->destino }} · {{ $viaje->pasajeros }} pasajeros</li>
        @empty
            <li>Sin viajes agendados.</li>
        @endforelse
    </ul>
    <p>Total: {{ $pasajeros }} pasajeros</p>

    <h2>Agendar un viaje</h2>
    <form action="{{ route('barcos.viajes.store', $barco) }}" method="post">
        @csrf
        <label>Destino <input name="destino" value="{{ old('destino') }}"></label>
        @error('destino') <p class="error">{{ $message }}</p> @enderror
        <label>Fecha <input type="date" name="fecha" value="{{ old('fecha') }}"></label>
        @error('fecha') <p class="error">{{ $message }}</p> @enderror
        <label>Pasajeros <input type="number" name="pasajeros" value="{{ old('pasajeros') }}"></label>
        @error('pasajeros') <p class="error">{{ $message }}</p> @enderror
        <button>Agendar</button>
    </form>
</body>
</html>
```

`resources/views/viajes/index.blade.php`
```blade
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Viajes</title></head>
<body>
    <h1>Todos los viajes</h1>
    <ul>
        @foreach ($viajes as $viaje)
            <li>{{ $viaje->fecha->format('d/m/Y') }} · {{ $viaje->barco->nombre }} → {{ $viaje->destino }}</li>
        @endforeach
    </ul>
</body>
</html>
```

`tests/Feature/ViajesTest.php`
```php
<?php

namespace Tests\Feature;

use App\Models\Barco;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ViajesTest extends TestCase
{
    use RefreshDatabase;

    public function test_muestra_el_barco_con_sus_viajes_por_fecha(): void
    {
        $this->seed();
        $albatros = Barco::where('nombre', 'Albatros')->first();

        $this->get("/barcos/{$albatros->id}")
            ->assertOk()
            ->assertSeeInOrder(['15/10/2026 · Colonia · 120 pasajeros', '20/10/2026 · Montevideo · 210 pasajeros'])
            ->assertSee('Total: 330 pasajeros')
            ->assertDontSee('Piriápolis');
    }

    public function test_un_barco_que_no_existe_da_404(): void
    {
        $this->get('/barcos/99')->assertNotFound();
    }

    public function test_agenda_un_viaje_por_la_relacion(): void
    {
        $barco = Barco::factory()->create();

        $this->post("/barcos/{$barco->id}/viajes", ['destino' => 'Colonia', 'fecha' => '2026-11-02', 'pasajeros' => 80])
            ->assertRedirect(route('barcos.show', $barco))
            ->assertSessionHas('ok', 'Viaje a Colonia agendado.');

        $this->assertSame(1, $barco->viajes()->count());
    }

    public function test_valida_el_viaje(): void
    {
        $barco = Barco::factory()->create();

        $this->post("/barcos/{$barco->id}/viajes", ['destino' => '', 'fecha' => 'mañana', 'pasajeros' => 900])
            ->assertSessionHasErrors([
                'destino' => 'Poné el destino.',
                'fecha' => 'Esa fecha no es válida.',
                'pasajeros' => 'Los pasajeros van de 1 a 500.',
            ]);
    }

    public function test_la_lista_muestra_el_barco_de_cada_viaje(): void
    {
        $this->seed();

        $this->get('/viajes')->assertSeeInOrder(['Albatros → Colonia', 'Gaviota → Piriápolis', 'Albatros → Montevideo']);
    }

    public function test_al_borrar_el_barco_se_borran_sus_viajes(): void
    {
        $this->seed();

        Barco::where('nombre', 'Albatros')->first()->delete();

        $this->assertDatabaseCount('viajes', 1);
    }
}
```

### Encargo S02-N02-E1 · El catálogo con buscador

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Con el modelo `Producto` de la primera misión (`nombre`, `precio`, `stock`), armá un
**catálogo** en `/catalogo`:

- de a **5 productos por página**, ordenados por nombre, con los enlaces de páginas
  (`{{ $productos->links() }}`);
- un buscador (`?buscar=soga`) que filtra por nombre con `like` y que **se mantiene** al
  cambiar de página (`withQueryString`);
- un orden opcional `?orden=precio` (de menor a mayor); cualquier otro valor ordena por
  nombre;
- el texto `Mostrando 6 a 10 de 12 productos` (con `firstItem`, `lastItem` y `total` del
  paginador), o `No encontramos productos con «farol».` si no hay resultados.

Un seeder carga 12 productos. Probá la primera y la segunda página, el buscador, que los
enlaces conserven `buscar`, el orden por precio y el caso sin resultados. Entregá el
proyecto en un zip.

#### Criterio de aprobación

- La consulta usa `paginate(5)` con `withQueryString()` y el filtro con `when`.
- El orden solo acepta `precio` o `nombre` (nada que venga del usuario va directo a `orderBy`).
- Las pruebas pasan y el proyecto migra en MariaDB.

#### Solución de referencia

`database/migrations/2026_09_01_000001_create_productos_table.php`
```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('productos', function (Blueprint $table) {
            $table->id();
            $table->string('nombre', 80);
            $table->decimal('precio', 10, 2);
            $table->unsignedInteger('stock');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('productos');
    }
};
```

`app/Models/Producto.php`
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Producto extends Model
{
    protected $fillable = ['nombre', 'precio', 'stock'];

    protected function casts(): array
    {
        return ['precio' => 'decimal:2', 'stock' => 'integer'];
    }
}
```

`database/seeders/DatabaseSeeder.php`
```php
<?php

namespace Database\Seeders;

use App\Models\Producto;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $productos = [
            ['Ancla chica', 61000.5], ['Boya naranja', 4200], ['Brújula de bolsillo', 15800],
            ['Cabo de nailon', 6300], ['Chaleco salvavidas', 27500], ['Defensa de goma', 9900],
            ['Linterna estanca', 12400], ['Mapa de la bahía', 3500], ['Remo de madera', 18200],
            ['Silbato de auxilio', 1500], ['Soga de amarre', 8500], ['Soga de remolque', 11200],
        ];
        foreach ($productos as [$nombre, $precio]) {
            Producto::create(['nombre' => $nombre, 'precio' => $precio, 'stock' => 10]);
        }
    }
}
```

`routes/web.php`
```php
<?php

use App\Http\Controllers\CatalogoController;
use Illuminate\Support\Facades\Route;

Route::get('/catalogo', CatalogoController::class)->name('catalogo');
```

`app/Http/Controllers/CatalogoController.php`
```php
<?php

namespace App\Http\Controllers;

use App\Models\Producto;
use Illuminate\Http\Request;
use Illuminate\View\View;

class CatalogoController extends Controller
{
    public function __invoke(Request $request): View
    {
        $buscar = trim((string) $request->query('buscar', ''));
        $orden = $request->query('orden') === 'precio' ? 'precio' : 'nombre';

        $productos = Producto::query()
            ->when($buscar !== '', fn ($consulta) => $consulta->where('nombre', 'like', "%{$buscar}%"))
            ->orderBy($orden)
            ->paginate(5)
            ->withQueryString();

        return view('catalogo', ['productos' => $productos, 'buscar' => $buscar]);
    }
}
```

`resources/views/catalogo.blade.php`
```blade
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Catálogo</title></head>
<body>
    <h1>Catálogo del Puerto</h1>
    <form action="{{ route('catalogo') }}" method="get">
        <input name="buscar" value="{{ $buscar }}" placeholder="Buscar…">
        <button>Buscar</button>
    </form>
    @if ($productos->isEmpty())
        <p>No encontramos productos con «{{ $buscar }}».</p>
    @else
        <p>Mostrando {{ $productos->firstItem() }} a {{ $productos->lastItem() }} de {{ $productos->total() }} productos</p>
        <ul>
            @foreach ($productos as $producto)
                <li>{{ $producto->nombre }} · $ {{ number_format($producto->precio, 2, ',', '.') }}</li>
            @endforeach
        </ul>
        {{ $productos->links() }}
    @endif
</body>
</html>
```

`tests/Feature/CatalogoTest.php`
```php
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class CatalogoTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();
        $this->seed();
    }

    public function test_la_primera_pagina_trae_cinco_por_nombre(): void
    {
        $this->get('/catalogo')
            ->assertOk()
            ->assertSee('Mostrando 1 a 5 de 12 productos')
            ->assertSeeInOrder(['Ancla chica', 'Boya naranja', 'Brújula de bolsillo', 'Cabo de nailon', 'Chaleco salvavidas'])
            ->assertDontSee('Defensa de goma');
    }

    public function test_la_segunda_pagina_sigue_donde_termino_la_primera(): void
    {
        $this->get('/catalogo?page=2')
            ->assertSee('Mostrando 6 a 10 de 12 productos')
            ->assertSeeInOrder(['Defensa de goma', 'Linterna estanca', 'Mapa de la bahía', 'Remo de madera', 'Silbato de auxilio']);
    }

    public function test_busca_y_conserva_la_busqueda_en_los_enlaces(): void
    {
        $this->get('/catalogo?buscar=soga')
            ->assertSee('Mostrando 1 a 2 de 2 productos')
            ->assertSee('Soga de amarre')
            ->assertSee('Soga de remolque')
            ->assertDontSee('Ancla chica');

        $this->get('/catalogo?buscar=o')->assertSee('buscar=o&amp;page=2', false);
    }

    public function test_ordena_por_precio(): void
    {
        $this->get('/catalogo?orden=precio')->assertSeeInOrder(['Silbato de auxilio', 'Mapa de la bahía', 'Boya naranja']);
    }

    public function test_un_orden_desconocido_ordena_por_nombre(): void
    {
        $this->get('/catalogo?orden=stock;DROP')->assertOk()->assertSeeInOrder(['Ancla chica', 'Boya naranja']);
    }

    public function test_avisa_si_no_hay_resultados(): void
    {
        $this->get('/catalogo?buscar=farol')->assertSee('No encontramos productos con «farol».');
    }
}
```

### Prueba del sello

#### ¿Por qué no se edita una migración que ya corrió en el servidor?

Porque el servidor no la vuelve a correr: el cambio nunca llegaría. Para cambiar una tabla se escribe una migración nueva.

#### ¿Para qué sirve `$fillable`?

Para decir qué campos se pueden asignar en masa (`create`, `update`): así nadie puede colar un campo extra en el formulario, como `es_admin`.

#### ¿Qué hace `$request->validate([...])` si un dato no pasa?

Vuelve al formulario solo, con los mensajes de error y lo que el usuario había escrito (para `old()`); si todo pasa, devuelve los datos validados.

#### ¿Qué pasa si una ruta recibe `Barco $barco` y el id no existe?

Laravel responde 404 sin entrar al método: es el *route model binding*.

#### ¿Qué problema evita `Viaje::with('barco')`?

El "N+1": sin `with`, mostrar el barco de cada viaje hace una consulta por viaje; con `with`, una sola más para todos los barcos.

### Soluciones (docente)

Contenido nuevo. Cada solución se verifica sobre Laravel 12 con `php artisan test` (SQLite en memoria, como trae el `phpunit.xml`) y además con `php artisan migrate:fresh --seed` contra MariaDB (`DB_CONNECTION=mariadb`). Para corregir: `composer install`, `.env` apuntando a una base vacía, `php artisan key:generate`, `php artisan migrate:fresh --seed`, `php artisan test` y una recorrida con `php artisan serve`.

## S02-N03 · Jefe de la Ciudadela: el Grifo de los Registros

```meta
tipo: jefe
padre: S02-N02
precio: 10
criatura: dragon
ejecutable: no
insignia: Guardián de la Ciudadela
insignia_descripcion: Venciste al Grifo de los Registros: construiste sistemas completos con Laravel y MariaDB, con reglas del negocio y pruebas.
```

### Crónica

Sobre la torre más alta de la Ciudadela anida el **Grifo de los Registros**: mitad águila, mitad león, y memoria de archivo. Cada mañana baja a revisar los libros del Puerto y, si encuentra dos barcos en el mismo muelle el mismo día, un calado que no entra o una anotación sin fecha, arranca la página con el pico.

—No lo vas a espantar con más código, {heroe} —dice {mentor}—, sino con **reglas**: que la base no pueda quedar en un estado imposible, que cada formulario diga qué corregir y que haya una prueba para cada cosa que el Grifo busca. Cuando no encuentre nada que arrancar, se va a quedar a cuidar tus libros.

### Objetivos

- Construir con Laravel dos sistemas completos sobre MariaDB, desde las migraciones hasta las pruebas.
- Separar la validación de los datos (formato) de las **reglas del negocio** (lo que el sistema no puede permitir).
- Combinar relaciones, filtros, paginación y mensajes de una sola vez en un ABM.

### Antes de empezar

- Toda la Senda de la Ciudadela.

### Explicación

#### Validar el formato y validar el negocio
`$request->validate` revisa que cada dato tenga **forma** correcta: que la fecha sea una
fecha, que el muelle exista. Pero "este muelle ya está ocupado ese día" o "este barco
no entra en ese muelle" dependen de **otros datos** de la base: son reglas del negocio.
Se revisan después de validar y, si fallan, se vuelve al formulario igual que un error
común:
```php
if (Reserva::where('muelle_id', $muelle->id)->whereDate('fecha', $datos['fecha'])->exists()) {
    return back()->withErrors(['fecha' => 'Ese muelle ya está reservado para esa fecha.'])->withInput();
}
```
`whereDate` compara solo la fecha, en MariaDB y en SQLite por igual. `back()` vuelve a
la página anterior, `withErrors` llena los `@error` y `withInput` los `old()`.

#### El tiempo en las pruebas
Las reglas con "hoy" (`after_or_equal:today`) cambian de resultado según el día en que
corrés las pruebas. Laravel deja **fijar la fecha**: `$this->travelTo(now()->setDate(2026, 10, 1))`
hace que `now()` y `today` sean ese día durante la prueba.

#### Filtros que se combinan
Para listar con varios filtros opcionales (`?barco=2&tipo=incidente`), cada filtro es
un `when` sobre la misma consulta. Si además necesitás contar por tipo con **los mismos**
filtros, armá una función que los aplique y usala en las dos consultas: así la lista y
el resumen nunca se contradicen.

### Misión S02-N03-M1 · Los turnos de los muelles

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 40
```

#### Consigna

El Puerto tiene tres muelles, cada uno con su **calado máximo** (la profundidad): Norte
(8,5 m), Este (12 m) y Sur (5 m). Construí con Laravel el sistema de **reservas de
muelle**:

- **Tablas** (migraciones): `muelles` (`nombre` único, `calado` `DECIMAL(4,1)`) y
  `reservas` (`muelle_id` con clave foránea, `barco`, `fecha` `DATE`, `calado`
  `DECIMAL(4,1)`). Un seeder carga los tres muelles.
- `GET /reservas`: cada muelle ordenado por nombre con su calado
  (`Muelle Este · hasta 12,0 m`) y debajo sus reservas por fecha
  (`03/10/2026 · Albatros (6,5 m)`) o `Libre` si no tiene.
- `GET /reservas/create` y `POST /reservas`: el formulario, con el muelle en un
  `<select>`. Validación con mensajes en español: muelle que exista, barco obligatorio,
  fecha de hoy en adelante, calado entre 1 y 20. Reglas del negocio:
  - un muelle tiene **una sola reserva por día**: `Ese muelle ya está reservado para esa fecha.`
  - el calado del barco no puede superar el del muelle:
    `El muelle Sur admite hasta 5,0 m de calado.`
  
  Si todo está bien, `Reserva confirmada: Albatros en el muelle Norte el 03/10/2026.`
- `DELETE /reservas/{reserva}`: cancela, con `Reserva de Albatros cancelada.`

Escribí las pruebas (con la fecha fijada): la lista, una reserva válida, cada error de
validación, las dos reglas del negocio (y que la misma fecha en **otro** muelle sí se
pueda) y la cancelación. Entregá el proyecto en un zip, sin `vendor/`.

#### Criterio de aprobación

- Las tablas salen de migraciones con su clave foránea, y los muelles de un seeder.
- La validación y las reglas del negocio están separadas, y los errores vuelven al formulario con lo escrito.
- La lista carga las reservas con `with` (sin una consulta por muelle).
- Las pruebas pasan y el proyecto migra en MariaDB.

#### Solución de referencia

`database/migrations/2026_09_01_000001_create_muelles_table.php`
```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('muelles', function (Blueprint $table) {
            $table->id();
            $table->string('nombre', 30)->unique();
            $table->decimal('calado', 4, 1);
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('muelles');
    }
};
```

`database/migrations/2026_09_01_000002_create_reservas_table.php`
```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('reservas', function (Blueprint $table) {
            $table->id();
            $table->foreignId('muelle_id')->constrained();
            $table->string('barco', 60);
            $table->date('fecha');
            $table->decimal('calado', 4, 1);
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('reservas');
    }
};
```

`app/Models/Muelle.php`
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Muelle extends Model
{
    protected $fillable = ['nombre', 'calado'];

    protected function casts(): array
    {
        return ['calado' => 'decimal:1'];
    }

    public function reservas(): HasMany
    {
        return $this->hasMany(Reserva::class);
    }
}
```

`app/Models/Reserva.php`
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Reserva extends Model
{
    protected $fillable = ['muelle_id', 'barco', 'fecha', 'calado'];

    protected function casts(): array
    {
        return ['fecha' => 'date', 'calado' => 'decimal:1'];
    }

    public function muelle(): BelongsTo
    {
        return $this->belongsTo(Muelle::class);
    }
}
```

`database/seeders/DatabaseSeeder.php`
```php
<?php

namespace Database\Seeders;

use App\Models\Muelle;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        Muelle::create(['nombre' => 'Norte', 'calado' => 8.5]);
        Muelle::create(['nombre' => 'Este', 'calado' => 12]);
        Muelle::create(['nombre' => 'Sur', 'calado' => 5]);
    }
}
```

`routes/web.php`
```php
<?php

use App\Http\Controllers\ReservaController;
use Illuminate\Support\Facades\Route;

Route::redirect('/', '/reservas');
Route::resource('reservas', ReservaController::class)->only(['index', 'create', 'store', 'destroy']);
```

`app/Http/Controllers/ReservaController.php`
```php
<?php

namespace App\Http\Controllers;

use App\Models\Muelle;
use App\Models\Reserva;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class ReservaController extends Controller
{
    public function index(): View
    {
        $muelles = Muelle::with(['reservas' => fn ($consulta) => $consulta->orderBy('fecha')])
            ->orderBy('nombre')
            ->get();

        return view('reservas.index', ['muelles' => $muelles]);
    }

    public function create(): View
    {
        return view('reservas.create', ['muelles' => Muelle::orderBy('nombre')->get()]);
    }

    public function store(Request $request): RedirectResponse
    {
        $datos = $request->validate([
            'muelle_id' => ['required', 'exists:muelles,id'],
            'barco' => ['required', 'string', 'max:60'],
            'fecha' => ['required', 'date', 'after_or_equal:today'],
            'calado' => ['required', 'numeric', 'between:1,20'],
        ], [
            'muelle_id.required' => 'Elegí un muelle.',
            'muelle_id.exists' => 'Ese muelle no existe.',
            'barco.required' => 'Poné el nombre del barco.',
            'fecha.required' => 'Poné la fecha.',
            'fecha.date' => 'Esa fecha no es válida.',
            'fecha.after_or_equal' => 'No se reserva para un día que ya pasó.',
            'calado.required' => 'Poné el calado del barco.',
            'calado.between' => 'El calado va de 1 a 20 metros.',
        ]);

        $muelle = Muelle::findOrFail($datos['muelle_id']);

        if ((float) $datos['calado'] > (float) $muelle->calado) {
            $maximo = number_format((float) $muelle->calado, 1, ',', '.');

            return back()->withErrors(['calado' => "El muelle {$muelle->nombre} admite hasta {$maximo} m de calado."])->withInput();
        }
        if ($muelle->reservas()->whereDate('fecha', $datos['fecha'])->exists()) {
            return back()->withErrors(['fecha' => 'Ese muelle ya está reservado para esa fecha.'])->withInput();
        }

        $reserva = $muelle->reservas()->create($datos);

        return redirect()->route('reservas.index')->with('ok',
            "Reserva confirmada: {$reserva->barco} en el muelle {$muelle->nombre} el {$reserva->fecha->format('d/m/Y')}.");
    }

    public function destroy(Reserva $reserva): RedirectResponse
    {
        $reserva->delete();

        return redirect()->route('reservas.index')->with('ok', "Reserva de {$reserva->barco} cancelada.");
    }
}
```

`resources/views/components/layout.blade.php`
```blade
@props(['titulo' => 'Turnos de los muelles'])
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>{{ $titulo }} · Puerto</title>
</head>
<body>
    @if (session('ok'))
        <p class="ok">{{ session('ok') }}</p>
    @endif
    <main>{{ $slot }}</main>
</body>
</html>
```

`resources/views/reservas/index.blade.php`
```blade
<x-layout>
    <h1>Turnos de los muelles</h1>
    <a href="{{ route('reservas.create') }}">Reservar un muelle</a>
    @foreach ($muelles as $muelle)
        <h2>Muelle {{ $muelle->nombre }} · hasta {{ number_format($muelle->calado, 1, ',', '.') }} m</h2>
        <ul>
            @forelse ($muelle->reservas as $reserva)
                <li>
                    {{ $reserva->fecha->format('d/m/Y') }} · {{ $reserva->barco }} ({{ number_format($reserva->calado, 1, ',', '.') }} m)
                    <form action="{{ route('reservas.destroy', $reserva) }}" method="post">
                        @csrf
                        @method('DELETE')
                        <button>Cancelar</button>
                    </form>
                </li>
            @empty
                <li>Libre</li>
            @endforelse
        </ul>
    @endforeach
</x-layout>
```

`resources/views/reservas/create.blade.php`
```blade
<x-layout titulo="Reservar un muelle">
    <h1>Reservar un muelle</h1>
    <form action="{{ route('reservas.store') }}" method="post">
        @csrf
        <label>Muelle
            <select name="muelle_id">
                <option value="">Elegí…</option>
                @foreach ($muelles as $muelle)
                    <option value="{{ $muelle->id }}" @selected(old('muelle_id') == $muelle->id)>{{ $muelle->nombre }}</option>
                @endforeach
            </select>
        </label>
        @error('muelle_id') <p class="error">{{ $message }}</p> @enderror
        <label>Barco <input name="barco" value="{{ old('barco') }}"></label>
        @error('barco') <p class="error">{{ $message }}</p> @enderror
        <label>Fecha <input type="date" name="fecha" value="{{ old('fecha') }}"></label>
        @error('fecha') <p class="error">{{ $message }}</p> @enderror
        <label>Calado (m) <input name="calado" value="{{ old('calado') }}"></label>
        @error('calado') <p class="error">{{ $message }}</p> @enderror
        <button>Reservar</button>
    </form>
</x-layout>
```

`tests/Feature/ReservasTest.php`
```php
<?php

namespace Tests\Feature;

use App\Models\Muelle;
use App\Models\Reserva;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ReservasTest extends TestCase
{
    use RefreshDatabase;

    private Muelle $norte;
    private Muelle $este;
    private Muelle $sur;

    protected function setUp(): void
    {
        parent::setUp();
        $this->travelTo(now()->setDate(2026, 10, 1)->startOfDay());
        $this->seed();
        $this->norte = Muelle::where('nombre', 'Norte')->first();
        $this->este = Muelle::where('nombre', 'Este')->first();
        $this->sur = Muelle::where('nombre', 'Sur')->first();
    }

    private function reservar(array $datos)
    {
        return $this->from('/reservas/create')->post('/reservas', $datos + [
            'muelle_id' => $this->norte->id, 'barco' => 'Albatros', 'fecha' => '2026-10-03', 'calado' => '6.5',
        ]);
    }

    public function test_lista_los_muelles_con_sus_reservas(): void
    {
        $this->norte->reservas()->create(['barco' => 'Gaviota', 'fecha' => '2026-10-09', 'calado' => 3]);
        $this->norte->reservas()->create(['barco' => 'Albatros', 'fecha' => '2026-10-03', 'calado' => 6.5]);

        $this->get('/reservas')
            ->assertOk()
            ->assertSeeInOrder([
                'Muelle Este · hasta 12,0 m', 'Libre',
                'Muelle Norte · hasta 8,5 m', '03/10/2026 · Albatros (6,5 m)', '09/10/2026 · Gaviota (3,0 m)',
                'Muelle Sur · hasta 5,0 m', 'Libre',
            ]);
    }

    public function test_confirma_una_reserva_valida(): void
    {
        $this->reservar([])
            ->assertRedirect(route('reservas.index'))
            ->assertSessionHas('ok', 'Reserva confirmada: Albatros en el muelle Norte el 03/10/2026.');

        $this->assertSame(1, $this->norte->reservas()->count());
    }

    public function test_valida_los_datos(): void
    {
        $this->reservar(['muelle_id' => 99, 'barco' => '', 'fecha' => '2026-09-30', 'calado' => '25'])
            ->assertRedirect('/reservas/create')
            ->assertSessionHasErrors([
                'muelle_id' => 'Ese muelle no existe.',
                'barco' => 'Poné el nombre del barco.',
                'fecha' => 'No se reserva para un día que ya pasó.',
                'calado' => 'El calado va de 1 a 20 metros.',
            ]);

        $this->assertDatabaseCount('reservas', 0);
    }

    public function test_hoy_se_puede_reservar(): void
    {
        $this->reservar(['fecha' => '2026-10-01'])->assertSessionHasNoErrors();
    }

    public function test_el_barco_tiene_que_entrar_en_el_muelle(): void
    {
        $this->reservar(['muelle_id' => $this->sur->id, 'calado' => '6.5'])
            ->assertSessionHasErrors(['calado' => 'El muelle Sur admite hasta 5,0 m de calado.']);

        $this->assertDatabaseCount('reservas', 0);
    }

    public function test_una_sola_reserva_por_muelle_y_por_dia(): void
    {
        $this->reservar([])->assertSessionHasNoErrors();

        $this->reservar(['barco' => 'Tritón'])
            ->assertSessionHasErrors(['fecha' => 'Ese muelle ya está reservado para esa fecha.']);
        $this->reservar(['barco' => 'Tritón', 'muelle_id' => $this->este->id])->assertSessionHasNoErrors();

        $this->assertDatabaseCount('reservas', 2);
    }

    public function test_el_formulario_vuelve_con_lo_escrito(): void
    {
        $this->followingRedirects()
            ->reservar(['muelle_id' => $this->sur->id, 'barco' => 'Estrella del Sur', 'calado' => '7'])
            ->assertSee('value="Estrella del Sur"', false)
            ->assertSee('El muelle Sur admite hasta 5,0 m de calado.');
    }

    public function test_cancela_una_reserva(): void
    {
        $reserva = Reserva::create(['muelle_id' => $this->este->id, 'barco' => 'Gaviota', 'fecha' => '2026-10-05', 'calado' => 3]);

        $this->delete("/reservas/{$reserva->id}")
            ->assertRedirect(route('reservas.index'))
            ->assertSessionHas('ok', 'Reserva de Gaviota cancelada.');
        $this->assertModelMissing($reserva);
    }
}
```

### Misión S02-N03-M2 · El libro de a bordo

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 40
```

#### Consigna

Cada barco lleva un **libro de a bordo** donde se anotan sus salidas, llegadas e
incidentes. Construí el ABM completo con Laravel:

- **Tablas**: `barcos` (`nombre` único) y `entradas` (`barco_id` con clave foránea que se
  borra con el barco, `tipo`, `fecha` `DATE`, `nota` que puede quedar vacía). Un seeder
  carga tres barcos (Albatros, Gaviota, Tritón) y **doce** entradas.
- `GET /entradas`: las entradas de la más nueva a la más vieja
  (`12/09/2026 · Tritón · INCIDENTE · Rotura del timón`), **10 por página**. Dos filtros
  opcionales que se combinan (`?barco=2&tipo=incidente`) con un formulario de `<select>`,
  que se conservan al cambiar de página. Arriba, un **resumen** por tipo con los mismos
  filtros: `Salidas: 5 · Llegadas: 4 · Incidentes: 3`.
- Alta, edición y baja (`Route::resource` sin `show`), con validación en español:
  barco que exista, tipo `salida`, `llegada` o `incidente`, fecha válida y **no
  futura** (es un libro de lo que ya pasó), y la **nota obligatoria solo para los
  incidentes** (`required_if`). Mensajes: `Entrada agregada al libro de Albatros.`,
  `Entrada actualizada.`, `Entrada borrada.`

Probá la paginación, cada filtro y los dos juntos, que el resumen respete los filtros,
el alta, la validación (incluida la nota del incidente y la fecha futura), la edición y
la baja. Entregá el proyecto en un zip.

#### Criterio de aprobación

- Los filtros se aplican con `when` desde **una sola** función, que usan la lista y el resumen.
- La paginación conserva los filtros y el orden es de la más nueva a la más vieja.
- La validación usa `required_if` y `before_or_equal:today`, con mensajes propios.
- Las pruebas pasan y el proyecto migra en MariaDB.

#### Solución de referencia

`database/migrations/2026_09_01_000001_create_barcos_table.php`
```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('barcos', function (Blueprint $table) {
            $table->id();
            $table->string('nombre', 60)->unique();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('barcos');
    }
};
```

`database/migrations/2026_09_01_000002_create_entradas_table.php`
```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('entradas', function (Blueprint $table) {
            $table->id();
            $table->foreignId('barco_id')->constrained()->cascadeOnDelete();
            $table->string('tipo', 10);
            $table->date('fecha');
            $table->string('nota', 200)->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('entradas');
    }
};
```

`app/Models/Barco.php`
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Barco extends Model
{
    protected $fillable = ['nombre'];

    public function entradas(): HasMany
    {
        return $this->hasMany(Entrada::class);
    }
}
```

`app/Models/Entrada.php`
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Entrada extends Model
{
    public const TIPOS = ['salida' => 'Salidas', 'llegada' => 'Llegadas', 'incidente' => 'Incidentes'];

    protected $fillable = ['barco_id', 'tipo', 'fecha', 'nota'];

    protected function casts(): array
    {
        return ['fecha' => 'date'];
    }

    public function barco(): BelongsTo
    {
        return $this->belongsTo(Barco::class);
    }
}
```

`database/seeders/DatabaseSeeder.php`
```php
<?php

namespace Database\Seeders;

use App\Models\Barco;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $albatros = Barco::create(['nombre' => 'Albatros']);
        $gaviota = Barco::create(['nombre' => 'Gaviota']);
        $triton = Barco::create(['nombre' => 'Tritón']);

        $libro = [
            [$albatros, 'salida', '2026-09-01', null],
            [$albatros, 'llegada', '2026-09-02', null],
            [$gaviota, 'salida', '2026-09-03', null],
            [$gaviota, 'incidente', '2026-09-04', 'Niebla cerrada, fondeo de dos horas'],
            [$gaviota, 'llegada', '2026-09-05', null],
            [$triton, 'salida', '2026-09-06', null],
            [$albatros, 'salida', '2026-09-07', 'Carga completa'],
            [$triton, 'llegada', '2026-09-08', null],
            [$albatros, 'incidente', '2026-09-09', 'Hombre al agua, rescatado'],
            [$albatros, 'llegada', '2026-09-10', null],
            [$triton, 'salida', '2026-09-11', null],
            [$triton, 'incidente', '2026-09-12', 'Rotura del timón'],
        ];
        foreach ($libro as [$barco, $tipo, $fecha, $nota]) {
            $barco->entradas()->create(['tipo' => $tipo, 'fecha' => $fecha, 'nota' => $nota]);
        }
    }
}
```

`routes/web.php`
```php
<?php

use App\Http\Controllers\EntradaController;
use Illuminate\Support\Facades\Route;

Route::redirect('/', '/entradas');
Route::resource('entradas', EntradaController::class)->except('show');
```

`app/Http/Controllers/EntradaController.php`
```php
<?php

namespace App\Http\Controllers;

use App\Models\Barco;
use App\Models\Entrada;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class EntradaController extends Controller
{
    public function index(Request $request): View
    {
        $barco = $request->integer('barco') ?: null;
        $tipo = array_key_exists((string) $request->query('tipo'), Entrada::TIPOS) ? $request->query('tipo') : null;

        $filtrar = fn (Builder $consulta) => $consulta
            ->when($barco, fn ($c) => $c->where('barco_id', $barco))
            ->when($tipo, fn ($c) => $c->where('tipo', $tipo));

        $cantidades = $filtrar(Entrada::query())->pluck('tipo')->countBy();
        $entradas = $filtrar(Entrada::with('barco'))
            ->orderByDesc('fecha')
            ->orderByDesc('id')
            ->paginate(10)
            ->withQueryString();

        return view('entradas.index', [
            'entradas' => $entradas,
            'resumen' => collect(Entrada::TIPOS)->map(fn ($texto, $clave) => "{$texto}: " . $cantidades->get($clave, 0)),
            'barcos' => Barco::orderBy('nombre')->get(),
            'barco' => $barco,
            'tipo' => $tipo,
        ]);
    }

    public function create(): View
    {
        return view('entradas.create', ['entrada' => new Entrada(), 'barcos' => Barco::orderBy('nombre')->get()]);
    }

    public function store(Request $request): RedirectResponse
    {
        $entrada = Entrada::create($this->validar($request));

        return redirect()->route('entradas.index')->with('ok', "Entrada agregada al libro de {$entrada->barco->nombre}.");
    }

    public function edit(Entrada $entrada): View
    {
        return view('entradas.edit', ['entrada' => $entrada, 'barcos' => Barco::orderBy('nombre')->get()]);
    }

    public function update(Request $request, Entrada $entrada): RedirectResponse
    {
        $entrada->update($this->validar($request));

        return redirect()->route('entradas.index')->with('ok', 'Entrada actualizada.');
    }

    public function destroy(Entrada $entrada): RedirectResponse
    {
        $entrada->delete();

        return redirect()->route('entradas.index')->with('ok', 'Entrada borrada.');
    }

    private function validar(Request $request): array
    {
        return $request->validate([
            'barco_id' => ['required', 'exists:barcos,id'],
            'tipo' => ['required', 'in:' . implode(',', array_keys(Entrada::TIPOS))],
            'fecha' => ['required', 'date', 'before_or_equal:today'],
            'nota' => ['nullable', 'required_if:tipo,incidente', 'string', 'max:200'],
        ], [
            'barco_id.required' => 'Elegí el barco.',
            'barco_id.exists' => 'Ese barco no existe.',
            'tipo.required' => 'Elegí el tipo de entrada.',
            'tipo.in' => 'El tipo es salida, llegada o incidente.',
            'fecha.required' => 'Poné la fecha.',
            'fecha.date' => 'Esa fecha no es válida.',
            'fecha.before_or_equal' => 'El libro anota lo que ya pasó: la fecha no puede ser futura.',
            'nota.required_if' => 'Contá qué pasó en el incidente.',
            'nota.max' => 'La nota tiene hasta 200 letras.',
        ]);
    }
}
```

`resources/views/components/layout.blade.php`
```blade
@props(['titulo' => 'Libro de a bordo'])
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>{{ $titulo }} · Puerto</title>
</head>
<body>
    @if (session('ok'))
        <p class="ok">{{ session('ok') }}</p>
    @endif
    <main>{{ $slot }}</main>
</body>
</html>
```

`resources/views/entradas/index.blade.php`
```blade
<x-layout>
    <h1>Libro de a bordo</h1>
    <form action="{{ route('entradas.index') }}" method="get">
        <select name="barco">
            <option value="">Todos los barcos</option>
            @foreach ($barcos as $b)
                <option value="{{ $b->id }}" @selected($barco === $b->id)>{{ $b->nombre }}</option>
            @endforeach
        </select>
        <select name="tipo">
            <option value="">Todos los tipos</option>
            @foreach (\App\Models\Entrada::TIPOS as $clave => $texto)
                <option value="{{ $clave }}" @selected($tipo === $clave)>{{ $texto }}</option>
            @endforeach
        </select>
        <button>Filtrar</button>
    </form>
    <p>{{ $resumen->implode(' · ') }}</p>
    <a href="{{ route('entradas.create') }}">Anotar</a>
    <ul>
        @forelse ($entradas as $entrada)
            <li>
                {{ $entrada->fecha->format('d/m/Y') }} · {{ $entrada->barco->nombre }} · {{ strtoupper($entrada->tipo) }}@if ($entrada->nota) · {{ $entrada->nota }}@endif
                <a href="{{ route('entradas.edit', $entrada) }}">Editar</a>
                <form action="{{ route('entradas.destroy', $entrada) }}" method="post">
                    @csrf
                    @method('DELETE')
                    <button>Borrar</button>
                </form>
            </li>
        @empty
            <li>No hay entradas con esos filtros.</li>
        @endforelse
    </ul>
    {{ $entradas->links() }}
</x-layout>
```

`resources/views/entradas/_campos.blade.php`
```blade
@csrf
<label>Barco
    <select name="barco_id">
        <option value="">Elegí…</option>
        @foreach ($barcos as $barco)
            <option value="{{ $barco->id }}" @selected(old('barco_id', $entrada->barco_id) == $barco->id)>{{ $barco->nombre }}</option>
        @endforeach
    </select>
</label>
@error('barco_id') <p class="error">{{ $message }}</p> @enderror
<label>Tipo
    <select name="tipo">
        @foreach (\App\Models\Entrada::TIPOS as $clave => $texto)
            <option value="{{ $clave }}" @selected(old('tipo', $entrada->tipo) === $clave)>{{ $clave }}</option>
        @endforeach
    </select>
</label>
@error('tipo') <p class="error">{{ $message }}</p> @enderror
<label>Fecha <input type="date" name="fecha" value="{{ old('fecha', $entrada->fecha?->format('Y-m-d')) }}"></label>
@error('fecha') <p class="error">{{ $message }}</p> @enderror
<label>Nota <input name="nota" value="{{ old('nota', $entrada->nota) }}"></label>
@error('nota') <p class="error">{{ $message }}</p> @enderror
<button>Guardar</button>
```

`resources/views/entradas/create.blade.php`
```blade
<x-layout titulo="Anotar en el libro">
    <h1>Anotar en el libro</h1>
    <form action="{{ route('entradas.store') }}" method="post">
        @include('entradas._campos')
    </form>
</x-layout>
```

`resources/views/entradas/edit.blade.php`
```blade
<x-layout titulo="Editar la entrada">
    <h1>Editar la entrada</h1>
    <form action="{{ route('entradas.update', $entrada) }}" method="post">
        @method('PUT')
        @include('entradas._campos')
    </form>
</x-layout>
```

`tests/Feature/LibroTest.php`
```php
<?php

namespace Tests\Feature;

use App\Models\Barco;
use App\Models\Entrada;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class LibroTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();
        $this->travelTo(now()->setDate(2026, 9, 15)->startOfDay());
        $this->seed();
    }

    private function barco(string $nombre): Barco
    {
        return Barco::where('nombre', $nombre)->first();
    }

    public function test_lista_de_la_mas_nueva_de_a_diez(): void
    {
        $this->get('/entradas')
            ->assertOk()
            ->assertSee('Salidas: 5 · Llegadas: 4 · Incidentes: 3')
            ->assertSeeInOrder(['12/09/2026 · Tritón · INCIDENTE · Rotura del timón', '11/09/2026 · Tritón · SALIDA'])
            ->assertSee('03/09/2026')
            ->assertDontSee('02/09/2026');

        $this->get('/entradas?page=2')->assertSeeInOrder(['02/09/2026 · Albatros · LLEGADA', '01/09/2026 · Albatros · SALIDA']);
    }

    public function test_filtra_por_barco_y_el_resumen_acompana(): void
    {
        $this->get('/entradas?barco=' . $this->barco('Albatros')->id)
            ->assertSee('Salidas: 2 · Llegadas: 2 · Incidentes: 1')
            ->assertSee('Hombre al agua, rescatado')
            ->assertDontSee('Tritón ·');
    }

    public function test_filtra_por_tipo(): void
    {
        $this->get('/entradas?tipo=incidente')
            ->assertSee('Salidas: 0 · Llegadas: 0 · Incidentes: 3')
            ->assertSeeInOrder(['Rotura del timón', 'Hombre al agua, rescatado', 'Niebla cerrada']);
    }

    public function test_combina_los_filtros_y_los_conserva_al_paginar(): void
    {
        $gaviota = $this->barco('Gaviota');

        $this->get("/entradas?barco={$gaviota->id}&tipo=incidente")
            ->assertSee('Salidas: 0 · Llegadas: 0 · Incidentes: 1')
            ->assertSee('Niebla cerrada')
            ->assertDontSee('Rotura del timón');

        $this->get('/entradas?tipo=salida&page=1')->assertSee('Salidas: 5');
        $this->get('/entradas?barco=' . $gaviota->id)->assertDontSee('page=2', false);
        for ($i = 0; $i < 10; $i++) {
            $gaviota->entradas()->create(['tipo' => 'salida', 'fecha' => '2026-09-13']);
        }
        $this->get('/entradas?barco=' . $gaviota->id)->assertSee('barco=' . $gaviota->id . '&amp;page=2', false);
    }

    public function test_un_tipo_desconocido_no_filtra(): void
    {
        $this->get('/entradas?tipo=tormenta')->assertSee('Salidas: 5 · Llegadas: 4 · Incidentes: 3');
    }

    public function test_agrega_una_entrada(): void
    {
        $this->post('/entradas', ['barco_id' => $this->barco('Albatros')->id, 'tipo' => 'salida', 'fecha' => '2026-09-15'])
            ->assertRedirect(route('entradas.index'))
            ->assertSessionHas('ok', 'Entrada agregada al libro de Albatros.');

        $this->assertDatabaseCount('entradas', 13);
    }

    public function test_valida_la_entrada(): void
    {
        $this->post('/entradas', ['barco_id' => 99, 'tipo' => 'naufragio', 'fecha' => '2026-09-16'])
            ->assertSessionHasErrors([
                'barco_id' => 'Ese barco no existe.',
                'tipo' => 'El tipo es salida, llegada o incidente.',
                'fecha' => 'El libro anota lo que ya pasó: la fecha no puede ser futura.',
            ]);
    }

    public function test_el_incidente_necesita_nota_y_lo_demas_no(): void
    {
        $albatros = $this->barco('Albatros')->id;

        $this->post('/entradas', ['barco_id' => $albatros, 'tipo' => 'incidente', 'fecha' => '2026-09-14', 'nota' => ''])
            ->assertSessionHasErrors(['nota' => 'Contá qué pasó en el incidente.']);
        $this->post('/entradas', ['barco_id' => $albatros, 'tipo' => 'llegada', 'fecha' => '2026-09-14', 'nota' => ''])
            ->assertSessionHasNoErrors();
    }

    public function test_edita_y_borra(): void
    {
        $entrada = Entrada::where('nota', 'Rotura del timón')->first();

        $this->get("/entradas/{$entrada->id}/edit")->assertOk()->assertSee('value="2026-09-12"', false);
        $this->put("/entradas/{$entrada->id}", [
            'barco_id' => $entrada->barco_id, 'tipo' => 'incidente', 'fecha' => '2026-09-12', 'nota' => 'Rotura del timón, remolcado',
        ])->assertSessionHas('ok', 'Entrada actualizada.');
        $this->assertSame('Rotura del timón, remolcado', $entrada->fresh()->nota);

        $this->delete("/entradas/{$entrada->id}")->assertSessionHas('ok', 'Entrada borrada.');
        $this->assertModelMissing($entrada);
    }
}
```

### Prueba del sello

#### ¿Qué diferencia hay entre validar el formato y validar una regla del negocio?

El formato se revisa con el dato solo (es una fecha, es un número); la regla del negocio depende de otros datos de la base (el muelle ya está ocupado ese día). La segunda se revisa después de validar.

#### ¿Qué hace `back()->withErrors([...])->withInput()`?

Vuelve al formulario anterior con esos mensajes para `@error` y con lo que el usuario había escrito para `old()`.

#### ¿Por qué se fija la fecha en las pruebas con `travelTo`?

Porque las reglas con "hoy" darían distinto según el día en que se corran las pruebas; con la fecha fija, siempre dan igual.

#### ¿Qué hace la regla `required_if:tipo,incidente`?

Hace obligatorio el campo solo cuando `tipo` vale `incidente`; en los demás casos puede quedar vacío.

#### ¿Por qué la lista y el resumen usan la misma función de filtros?

Para que los dos cuenten exactamente lo mismo: si se aplicaran por separado, un cambio en uno podría dejarlos contradiciéndose.

### Soluciones (docente)

Contenido nuevo. Las dos soluciones se verifican sobre Laravel 12 con `php artisan test` (con la fecha fijada con `travelTo`) y con `php artisan migrate:fresh --seed` contra MariaDB. La regla "una reserva por muelle y por día" se revisa con `whereDate` (así funciona igual en SQLite y en MariaDB). Si un alumno quiere más, el próximo paso natural es el login y los permisos, que quedan para el curso de Laravel.
