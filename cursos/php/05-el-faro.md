# RAMA R05 · El Faro: aplicaciones completas

```meta
tipo: tronco
posicion: 5
```

## R05-N01 · MVC sin framework: router y controladores

```meta
tipo: tema
padre: R04-N09
precio: 10
criatura: skeleton
temas: web.mvc, diseno.capas
```

### Crónica

En la punta del muelle más largo está el **Faro**, la construcción más alta del Puerto. Desde su cúpula, un guardián dirige a todos los barcos que llegan de noche: a cada uno le mira la bandera y le señala una dársena. No carga nada ni atiende a nadie: solo **dirige**, y cada dársena sabe qué hacer con lo suyo.

—Tus sistemas ya tienen muchas páginas, y cada una repite lo mismo al empezar —dice {mentor}—. En el Faro trabajamos distinto: **todos** los pedidos entran por una sola puerta, un **router** mira la dirección y el método y se los pasa al **controlador** que corresponde. El controlador pide los datos al **modelo** y se los da a la **vista**. Tres piezas, {heroe}: así están hechos todos los frameworks.

### Objetivos

- Entender el patrón MVC: modelo, vista y controlador.
- Mandar todos los pedidos a un solo `index.php` (controlador frontal).
- Escribir un router que elige el controlador según el método y la ruta, con parámetros (`/barcos/12`).
- Organizar el proyecto en clases con namespaces y autoload.
- Devolver 404 y 405 cuando la ruta o el método no existen.

### Antes de empezar

- Plantillas y `public/` (R03-N08), namespaces y autoload (R02-N10), repositorios (R04-N08).

### Explicación

#### Modelo, vista y controlador
| Pieza | Hace | En el Puerto |
|---|---|---|
| **Modelo** | los datos y sus reglas | entidades y repositorios (`Barco`, `BarcoRepositorio`) |
| **Vista** | mostrar | plantillas PHP en `vistas/` |
| **Controlador** | recibir el pedido, decidir y responder | clases con métodos (`BarcoControlador::mostrar`) |

El controlador **no** escribe SQL (lo hace el modelo) ni HTML (lo hace la vista):
coordina.

#### Direcciones lindas y un solo punto de entrada
En lugar de `barco.php?id=12`, se usan rutas como **`/barcos/12`**. Para eso, todos
los pedidos van a `public/index.php`:
- con `php -S`, pasándolo como *router*: `php -S localhost:8000 -t public public/index.php`;
- en Apache (XAMPP, hosting), con un `.htaccess` en `public/` (lo ves en el nodo de
  hosting).

`index.php` lee la ruta y el método:
```php
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);    // /barcos/12 (sin ?x=1)
$metodo = $_SERVER['REQUEST_METHOD'];                        // GET, POST…
```
Con `php -S`, los archivos que existen (CSS, imágenes) se sirven solos si el router
devuelve `false`:
```php
if (PHP_SAPI === 'cli-server' && is_file(__DIR__ . $ruta)) {
    return false;
}
```

#### Un router chico
```php
class Router
{
    private array $rutas = [];

    public function get(string $patron, callable $accion): void
    {
        $this->rutas['GET'][$patron] = $accion;
    }

    public function post(string $patron, callable $accion): void
    {
        $this->rutas['POST'][$patron] = $accion;
    }

    public function despachar(string $metodo, string $ruta): string
    {
        foreach ($this->rutas[$metodo] ?? [] as $patron => $accion) {
            // /barcos/{id} → #^/barcos/(\d+)$#
            $regex = '#^' . preg_replace('#\{\w+\}#', '(\d+)', $patron) . '$#';
            if (preg_match($regex, $ruta, $partes)) {
                return $accion(...array_map('intval', array_slice($partes, 1)));
            }
        }
        // ¿Existe con otro método? 405; si no, 404.
        …
    }
}
```
Y las rutas se declaran en un solo lugar:
```php
$router->get('/barcos', [$barcos, 'lista']);
$router->get('/barcos/{id}', [$barcos, 'mostrar']);
$router->post('/barcos', [$barcos, 'crear']);
```
`[$objeto, 'metodo']` es un **callable**: una forma de pasar "este método de este
objeto" para llamarlo después (lo ves a fondo en el nodo siguiente).

#### Los controladores
```php
class BarcoControlador
{
    public function __construct(private BarcoRepositorio $barcos, private Vista $vista) {}

    public function mostrar(int $id): string
    {
        $barco = $this->barcos->buscar($id) ?? throw new NoEncontrado("No existe el barco $id");
        return $this->vista->render('barcos/ficha', ['barco' => $barco]);
    }
}
```
Recibe sus dependencias por el constructor (inyección), devuelve la respuesta como
texto y lanza excepciones que el `index.php` convierte en páginas de error.

#### La estructura
```
faro/
├── public/index.php          ← punto de entrada: arma todo y despacha
├── src/
│   ├── Router.php
│   ├── Vista.php
│   ├── Controladores/BarcoControlador.php
│   └── Modelo/{Barco.php, BarcoRepositorio.php}
├── vistas/{layout.php, barcos/lista.php, barcos/ficha.php, error.php}
└── config.php
```
Con namespaces (`Faro\Controladores\…`) y un autoload PSR-4 (Composer o
`spl_autoload_register`).

### Código de ejemplo

`esquema.sql`
```sql
DROP TABLE IF EXISTS barco;
CREATE TABLE barco (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(40) NOT NULL UNIQUE, capacidad DECIMAL(8, 2) NOT NULL);
INSERT INTO barco (nombre, capacidad) VALUES ('Gaviota', 450), ('Albatros', 1200), ('Tortuga', 80);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`src/Router.php`
```php
<?php
declare(strict_types=1);

namespace Faro;

class Router
{
    private array $rutas = [];

    public function get(string $patron, callable $accion): void
    {
        $this->rutas['GET'][$patron] = $accion;
    }

    public function post(string $patron, callable $accion): void
    {
        $this->rutas['POST'][$patron] = $accion;
    }

    public function despachar(string $metodo, string $ruta): string
    {
        $otroMetodo = false;
        foreach ($this->rutas as $metodoRuta => $rutas) {
            foreach ($rutas as $patron => $accion) {
                $regex = '#^' . preg_replace('#\{\w+\}#', '(\d+)', $patron) . '$#';
                if (!preg_match($regex, $ruta, $partes)) {
                    continue;
                }
                if ($metodoRuta !== $metodo) {
                    $otroMetodo = true;
                    continue;
                }
                return $accion(...array_map('intval', array_slice($partes, 1)));
            }
        }
        throw $otroMetodo ? new MetodoNoPermitido($metodo) : new NoEncontrado("No existe la página $ruta");
    }
}

class NoEncontrado extends \RuntimeException {}

class MetodoNoPermitido extends \RuntimeException {}
```

`src/Vista.php`
```php
<?php
declare(strict_types=1);

namespace Faro;

class Vista
{
    public function __construct(private string $carpeta) {}

    public function render(string $__vista, array $__datos = [], ?string $__layout = 'layout'): string
    {
        extract($__datos);
        ob_start();
        require $this->carpeta . "/$__vista.php";
        $contenido = ob_get_clean();
        return $__layout === null ? $contenido : $this->render($__layout, ['contenido' => $contenido] + $__datos, null);
    }
}

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}
```

`src/Modelo/Barco.php`
```php
<?php
declare(strict_types=1);

namespace Faro\Modelo;

readonly class Barco
{
    public function __construct(public ?int $id, public string $nombre, public float $capacidad) {}
}
```

`src/Modelo/BarcoRepositorio.php`
```php
<?php
declare(strict_types=1);

namespace Faro\Modelo;

use PDO;

class BarcoRepositorio
{
    public function __construct(private PDO $pdo) {}

    /** @return Barco[] */
    public function todos(): array
    {
        return array_map(fn($f) => new Barco((int) $f['id'], $f['nombre'], (float) $f['capacidad']), $this->pdo->query('SELECT * FROM barco ORDER BY nombre')->fetchAll());
    }

    public function buscar(int $id): ?Barco
    {
        $s = $this->pdo->prepare('SELECT * FROM barco WHERE id = ?');
        $s->execute([$id]);
        $f = $s->fetch();
        return $f === false ? null : new Barco((int) $f['id'], $f['nombre'], (float) $f['capacidad']);
    }

    public function crear(string $nombre, float $capacidad): int
    {
        $this->pdo->prepare('INSERT INTO barco (nombre, capacidad) VALUES (?, ?)')->execute([$nombre, $capacidad]);
        return (int) $this->pdo->lastInsertId();
    }
}
```

`src/Controladores/BarcoControlador.php`
```php
<?php
declare(strict_types=1);

namespace Faro\Controladores;

use Faro\Modelo\BarcoRepositorio;
use Faro\NoEncontrado;
use Faro\Vista;

class BarcoControlador
{
    public function __construct(private BarcoRepositorio $barcos, private Vista $vista) {}

    public function inicio(): string
    {
        return $this->vista->render('inicio', ['titulo' => 'El Faro', 'cantidad' => count($this->barcos->todos())]);
    }

    public function lista(): string
    {
        return $this->vista->render('barcos/lista', ['titulo' => 'Barcos', 'barcos' => $this->barcos->todos()]);
    }

    public function mostrar(int $id): string
    {
        $barco = $this->barcos->buscar($id) ?? throw new NoEncontrado("No existe el barco $id");
        return $this->vista->render('barcos/ficha', ['titulo' => $barco->nombre, 'barco' => $barco]);
    }

    public function crear(): string
    {
        $nombre = trim($_POST['nombre'] ?? '');
        $capacidad = filter_var($_POST['capacidad'] ?? '', FILTER_VALIDATE_FLOAT);
        if ($nombre === '' || $capacidad === false || $capacidad <= 0) {
            http_response_code(422);
            return $this->vista->render('barcos/lista', ['titulo' => 'Barcos', 'barcos' => $this->barcos->todos(), 'error' => 'Nombre y capacidad válidos, por favor.']);
        }
        $id = $this->barcos->crear($nombre, $capacidad);
        header("Location: /barcos/$id", true, 303);
        return '';
    }
}
```

`vistas/layout.php`
```php
<?php use function Faro\e; ?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title><?= e($titulo) ?> · El Faro</title></head>
<body>
    <nav><a href="/">Inicio</a> · <a href="/barcos">Barcos</a></nav>
    <?= $contenido ?>
</body>
</html>
```

`vistas/inicio.php`
```php
<h1>El Faro</h1>
<p>Hay <?= $cantidad ?> barcos registrados.</p>
```

`vistas/barcos/lista.php`
```php
<?php use function Faro\e; ?>
<h1>Barcos</h1>
<?php if (isset($error)): ?><p><strong><?= e($error) ?></strong></p><?php endif; ?>
<ul>
    <?php foreach ($barcos as $b): ?>
        <li><a href="/barcos/<?= $b->id ?>"><?= e($b->nombre) ?></a></li>
    <?php endforeach; ?>
</ul>
<form method="post" action="/barcos">
    <input name="nombre" placeholder="Nombre"> <input name="capacidad" placeholder="Capacidad"> <button>Agregar</button>
</form>
```

`vistas/barcos/ficha.php`
```php
<?php use function Faro\e; ?>
<h1><?= e($barco->nombre) ?></h1>
<p>Capacidad: <?= $barco->capacidad ?> kg</p>
<p><a href="/barcos">Volver</a></p>
```

`vistas/error.php`
```php
<?php use function Faro\e; ?>
<h1><?= e($titulo) ?></h1>
<p><?= e($mensaje) ?></p>
```

`public/index.php`
```php
<?php
declare(strict_types=1);
/*
 * El guardián del Faro: controlador frontal, router, controladores y vistas.
 * Se prueba con: php -S localhost:8000 -t public public/index.php
 */
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (PHP_SAPI === 'cli-server' && $ruta !== '/' && is_file(__DIR__ . $ruta)) {
    return false;                                   // CSS, imágenes: los sirve php -S
}

spl_autoload_register(function (string $clase): void {
    if (str_starts_with($clase, 'Faro\\')) {
        $archivo = __DIR__ . '/../src/' . str_replace('\\', '/', substr($clase, 5)) . '.php';
        if (is_file($archivo)) {
            require $archivo;
        }
    }
});
require_once __DIR__ . '/../src/Router.php';        // trae también las excepciones del router
require_once __DIR__ . '/../src/Vista.php';         // trae también la función e()

use Faro\Controladores\BarcoControlador;
use Faro\MetodoNoPermitido;
use Faro\Modelo\BarcoRepositorio;
use Faro\NoEncontrado;
use Faro\Router;
use Faro\Vista;

$c = require __DIR__ . '/../config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);
$vista = new Vista(__DIR__ . '/../vistas');
$barcos = new BarcoControlador(new BarcoRepositorio($pdo), $vista);

$router = new Router();
$router->get('/', [$barcos, 'inicio']);
$router->get('/barcos', [$barcos, 'lista']);
$router->get('/barcos/{id}', [$barcos, 'mostrar']);
$router->post('/barcos', [$barcos, 'crear']);

try {
    echo $router->despachar($_SERVER['REQUEST_METHOD'], $ruta);
} catch (NoEncontrado $e) {
    http_response_code(404);
    echo $vista->render('error', ['titulo' => 'No encontrado', 'mensaje' => $e->getMessage()]);
} catch (MetodoNoPermitido $e) {
    http_response_code(405);
    echo $vista->render('error', ['titulo' => 'Método no permitido', 'mensaje' => "Esta dirección no acepta {$e->getMessage()}."]);
}
```

### ¿Para qué sirve?

Laravel, Symfony, CodeIgniter y casi todos los frameworks web de cualquier lenguaje son MVC con un router. Cuando en la Senda de Laravel escribas `Route::get('/barcos/{id}', [BarcoController::class, 'show'])`, vas a saber exactamente qué pasa por debajo, porque lo construiste. Y un sistema chico sin framework, armado así, se mantiene ordenado aunque crezca.

### Errores habituales

**Esqueleto: todas las rutas dan 404.** Con `php -S` hay que pasar `index.php` como
router (`php -S localhost:8000 -t public public/index.php`); si no, `/barcos/12`
busca un archivo que no existe.

**Esqueleto: `Class "Faro\…" not found`.** El namespace no coincide con la carpeta o el
archivo no se llama como la clase: el autoload no lo encuentra.

**Ogro: el `$_GET` en la ruta.** `$_SERVER['REQUEST_URI']` trae también `?x=1`: usá
`parse_url(…, PHP_URL_PATH)` antes de comparar.

**Troll: el controlador con SQL y HTML.** Si el controlador arma consultas y
`echo`s, volviste al código mezclado. SQL al modelo, HTML a la vista.

**Slime: el orden de las rutas.** Con patrones más generales antes que los
específicos (`/barcos/{id}` antes que `/barcos/nuevo`), el primero se queda con el
pedido. Declará primero las rutas fijas.

### Misión R05-N01-M1 · Las rutas de la biblioteca

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá una aplicación MVC chica para la biblioteca, con el router del ejemplo (podés
copiarlo) y **sin base de datos** (los libros en un repositorio en memoria dentro del
modelo):

- `GET /` — portada con la cantidad de libros;
- `GET /libros` — lista, con un filtro opcional `?autor=` (el controlador lo lee de
  `$_GET`);
- `GET /libros/{id}` — ficha (404 si no existe);
- `GET /autores` — los autores con la cantidad de libros de cada uno;
- cualquier otra ruta, 404; `POST /libros`, 405 (todavía no se pueden cargar).

Organizá en `src/` con namespaces `Biblioteca\…` y autoload, y vistas con layout.

#### Criterio de aprobación

- Un solo punto de entrada y un router con rutas con parámetros.
- Controladores que usan el modelo y las vistas; nada de SQL ni HTML en el controlador.
- 404 y 405 con su página de error.

#### Solución de referencia

`src/Router.php`
```php
<?php
declare(strict_types=1);

namespace Biblioteca;

class Router
{
    private array $rutas = [];

    public function get(string $patron, callable $accion): void
    {
        $this->rutas['GET'][$patron] = $accion;
    }

    public function despachar(string $metodo, string $ruta): string
    {
        $otroMetodo = false;
        foreach ($this->rutas as $metodoRuta => $rutas) {
            foreach ($rutas as $patron => $accion) {
                if (!preg_match('#^' . preg_replace('#\{\w+\}#', '(\d+)', $patron) . '$#', $ruta, $partes)) {
                    continue;
                }
                if ($metodoRuta !== $metodo) {
                    $otroMetodo = true;
                    continue;
                }
                return $accion(...array_map('intval', array_slice($partes, 1)));
            }
        }
        throw new ErrorHttp($otroMetodo ? 405 : 404, $otroMetodo ? "No se acepta $metodo en $ruta" : "No existe $ruta");
    }
}

class ErrorHttp extends \RuntimeException
{
    public function __construct(public readonly int $estado, string $mensaje)
    {
        parent::__construct($mensaje);
    }
}
```

`src/Modelo/Libros.php`
```php
<?php
declare(strict_types=1);

namespace Biblioteca\Modelo;

class Libros
{
    private array $libros = [
        1 => ['titulo' => 'Rayuela', 'autor' => 'Julio Cortázar'],
        2 => ['titulo' => 'Ficciones', 'autor' => 'Jorge Luis Borges'],
        3 => ['titulo' => 'Bestiario', 'autor' => 'Julio Cortázar'],
        4 => ['titulo' => 'El Aleph', 'autor' => 'Jorge Luis Borges'],
        5 => ['titulo' => 'Poemas de otoño', 'autor' => 'Olga Orozco'],
    ];

    public function todos(string $autor = ''): array
    {
        return array_filter($this->libros, fn(array $l) => $autor === '' || stripos($l['autor'], $autor) !== false);
    }

    public function buscar(int $id): ?array
    {
        return $this->libros[$id] ?? null;
    }

    public function porAutor(): array
    {
        $cuenta = array_count_values(array_column($this->libros, 'autor'));
        ksort($cuenta);
        return $cuenta;
    }
}
```

`src/Controladores/LibroControlador.php`
```php
<?php
declare(strict_types=1);

namespace Biblioteca\Controladores;

use Biblioteca\ErrorHttp;
use Biblioteca\Modelo\Libros;

class LibroControlador
{
    public function __construct(private Libros $libros, private \Closure $vista) {}

    public function portada(): string
    {
        return ($this->vista)('portada', ['titulo' => 'Biblioteca', 'cantidad' => count($this->libros->todos())]);
    }

    public function lista(): string
    {
        $autor = trim($_GET['autor'] ?? '');
        return ($this->vista)('lista', ['titulo' => 'Libros', 'libros' => $this->libros->todos($autor), 'autor' => $autor]);
    }

    public function ficha(int $id): string
    {
        $libro = $this->libros->buscar($id) ?? throw new ErrorHttp(404, "No existe el libro $id");
        return ($this->vista)('ficha', ['titulo' => $libro['titulo'], 'libro' => $libro]);
    }

    public function autores(): string
    {
        return ($this->vista)('autores', ['titulo' => 'Autores', 'autores' => $this->libros->porAutor()]);
    }
}
```

`vistas/layout.php`
```php
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title><?= htmlspecialchars($titulo) ?> · Biblioteca</title></head>
<body><nav><a href="/">Inicio</a> · <a href="/libros">Libros</a> · <a href="/autores">Autores</a></nav><?= $contenido ?></body>
</html>
```

`vistas/portada.php`
```php
<h1>Biblioteca popular</h1>
<p><?= $cantidad ?> libros en el catálogo.</p>
```

`vistas/lista.php`
```php
<h1>Libros<?= $autor !== '' ? ' de «' . htmlspecialchars($autor) . '»' : '' ?></h1>
<ul>
    <?php foreach ($libros as $id => $l): ?>
        <li><a href="/libros/<?= $id ?>"><?= htmlspecialchars($l['titulo']) ?></a> (<?= htmlspecialchars($l['autor']) ?>)</li>
    <?php endforeach; ?>
</ul>
```

`vistas/ficha.php`
```php
<h1><?= htmlspecialchars($libro['titulo']) ?></h1>
<p>de <?= htmlspecialchars($libro['autor']) ?></p>
```

`vistas/autores.php`
```php
<h1>Autores</h1>
<ul><?php foreach ($autores as $autor => $n): ?><li><?= htmlspecialchars($autor) ?>: <?= $n ?></li><?php endforeach; ?></ul>
```

`vistas/error.php`
```php
<h1>Error <?= $estado ?></h1>
<p><?= htmlspecialchars($mensaje) ?></p>
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Mision 1 - Las rutas de la biblioteca: un router, un controlador y vistas.
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (PHP_SAPI === 'cli-server' && $ruta !== '/' && is_file(__DIR__ . $ruta)) {
    return false;
}
spl_autoload_register(function (string $clase): void {
    $archivo = __DIR__ . '/../src/' . str_replace('\\', '/', substr($clase, strlen('Biblioteca\\'))) . '.php';
    if (str_starts_with($clase, 'Biblioteca\\') && is_file($archivo)) {
        require $archivo;
    }
});
require_once __DIR__ . '/../src/Router.php';

use Biblioteca\Controladores\LibroControlador;
use Biblioteca\ErrorHttp;
use Biblioteca\Modelo\Libros;
use Biblioteca\Router;

$vista = function (string $__vista, array $__datos): string {
    extract($__datos);
    ob_start();
    require __DIR__ . "/../vistas/$__vista.php";
    $contenido = ob_get_clean();
    ob_start();
    require __DIR__ . '/../vistas/layout.php';
    return ob_get_clean();
};

$libros = new LibroControlador(new Libros(), $vista);
$router = new Router();
$router->get('/', [$libros, 'portada']);
$router->get('/libros', [$libros, 'lista']);
$router->get('/libros/{id}', [$libros, 'ficha']);
$router->get('/autores', [$libros, 'autores']);

try {
    echo $router->despachar($_SERVER['REQUEST_METHOD'], $ruta);
} catch (ErrorHttp $e) {
    http_response_code($e->estado);
    echo $vista('error', ['titulo' => "Error {$e->estado}", 'estado' => $e->estado, 'mensaje' => $e->getMessage()]);
}
```

### Misión R05-N01-M2 · El router que entiende nombres

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

El router del ejemplo solo acepta números en los parámetros. Mejoralo:

- los parámetros pueden llevar un tipo: `{id:num}` (solo dígitos, llega como `int`)
  o `{slug}` (letras minúsculas, números y guiones, llega como `string`);
- además de `get` y `post`, agregá `put` y `delete`, y que un formulario pueda
  simular `DELETE` con un campo oculto `_metodo` (los formularios HTML solo mandan
  GET y POST);
- `despachar` pasa los parámetros **con nombre** a la acción
  (`$accion(...$parametros)` con un array asociativo usa argumentos con nombre).

Probalo con un controlador de noticias: `GET /noticias/{slug}`,
`GET /noticias/{id:num}/comentarios`, `DELETE /noticias/{id:num}` (que responde
`Noticia N borrada`), y un formulario con `_metodo=DELETE`.

#### Criterio de aprobación

- Los parámetros tienen tipo y llegan con nombre.
- `_metodo` permite simular PUT y DELETE desde un formulario.
- 404 y 405 siguen funcionando.

#### Solución de referencia

`src/Router.php`
```php
<?php
declare(strict_types=1);

namespace Noticias;

class Router
{
    private array $rutas = [];

    public function get(string $p, callable $a): void { $this->agregar('GET', $p, $a); }

    public function post(string $p, callable $a): void { $this->agregar('POST', $p, $a); }

    public function put(string $p, callable $a): void { $this->agregar('PUT', $p, $a); }

    public function delete(string $p, callable $a): void { $this->agregar('DELETE', $p, $a); }

    private function agregar(string $metodo, string $patron, callable $accion): void
    {
        $tipos = [];
        $regex = preg_replace_callback('#\{(\w+)(?::(num))?\}#', function (array $m) use (&$tipos): string {
            $tipos[$m[1]] = ($m[2] ?? '') === 'num' ? 'int' : 'string';
            return $tipos[$m[1]] === 'int' ? '(?P<' . $m[1] . '>\d+)' : '(?P<' . $m[1] . '>[a-z0-9-]+)';
        }, $patron);
        $this->rutas[] = ['metodo' => $metodo, 'regex' => "#^$regex$#", 'tipos' => $tipos, 'accion' => $accion];
    }

    public function despachar(string $metodo, string $ruta, array $post = []): string
    {
        if ($metodo === 'POST' && in_array($post['_metodo'] ?? '', ['PUT', 'DELETE'], true)) {
            $metodo = $post['_metodo'];
        }
        $otroMetodo = false;
        foreach ($this->rutas as $r) {
            if (!preg_match($r['regex'], $ruta, $m)) {
                continue;
            }
            if ($r['metodo'] !== $metodo) {
                $otroMetodo = true;
                continue;
            }
            $parametros = [];
            foreach ($r['tipos'] as $nombre => $tipo) {
                $parametros[$nombre] = $tipo === 'int' ? (int) $m[$nombre] : $m[$nombre];
            }
            return ($r['accion'])(...$parametros);
        }
        http_response_code($otroMetodo ? 405 : 404);
        return $otroMetodo ? "Método $metodo no permitido" : "No existe $ruta";
    }
}
```

`src/NoticiaControlador.php`
```php
<?php
declare(strict_types=1);

namespace Noticias;

class NoticiaControlador
{
    public function ver(string $slug): string
    {
        return 'Noticia: ' . ucfirst(str_replace('-', ' ', $slug));
    }

    public function comentarios(int $id): string
    {
        return "Comentarios de la noticia $id (" . gettype($id) . ')';
    }

    public function borrar(int $id): string
    {
        return "Noticia $id borrada";
    }

    public function formulario(): string
    {
        return '<form method="post" action="/noticias/7"><input type="hidden" name="_metodo" value="DELETE"><button>Borrar la 7</button></form>';
    }
}
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Mision 2 - El router que entiende nombres: tipos, métodos y _metodo.
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
require __DIR__ . '/../src/Router.php';
require __DIR__ . '/../src/NoticiaControlador.php';

use Noticias\NoticiaControlador;
use Noticias\Router;

$noticias = new NoticiaControlador();
$router = new Router();
$router->get('/noticias/{id:num}/comentarios', [$noticias, 'comentarios']);
$router->get('/noticias/{slug}', [$noticias, 'ver']);
$router->delete('/noticias/{id:num}', [$noticias, 'borrar']);
$router->get('/', [$noticias, 'formulario']);

echo $router->despachar($_SERVER['REQUEST_METHOD'], $ruta, $_POST);
```

### Misión R05-N01-M3 · El controlador flaco

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Este "controlador" de pedidos hace todo: lee el POST, valida, calcula el total con
descuentos, escribe el SQL y arma el HTML con `echo`. Reorganizalo en MVC:

- `Modelo\Pedido` (entidad) y `Modelo\CalculadoraDePrecios` (la regla: 10% de
  descuento desde $50000, envío gratis desde $80000, si no $3500);
- `Modelo\PedidoRepositorio` con PDO;
- `Controladores\PedidoControlador` con `formulario()` y `guardar()`, que solo
  coordina;
- vistas `formulario.php` y `resumen.php`.

El comportamiento tiene que ser el mismo. Probá un pedido de $60000 y uno de $90000.

#### Criterio de aprobación

- El controlador no tiene SQL, HTML ni cálculos de precios.
- La regla de precios está en una clase del modelo.
- El comportamiento es el mismo que el del código original.

#### Código inicial

```php
<?php
$pdo = new PDO('mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'root', '');
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $subtotal = (float) $_POST['subtotal'];
    $descuento = $subtotal >= 50000 ? $subtotal * 0.10 : 0;
    $envio = $subtotal >= 80000 ? 0 : 3500;
    $total = $subtotal - $descuento + $envio;
    $pdo->prepare('INSERT INTO pedido (cliente, subtotal, total) VALUES (?, ?, ?)')->execute([$_POST['cliente'], $subtotal, $total]);
    echo "<h1>Pedido de " . htmlspecialchars($_POST['cliente']) . "</h1><p>Descuento: $descuento · Envío: $envio · Total: $total</p>";
    exit;
}
echo '<form method="post"><input name="cliente"><input name="subtotal"><button>Pedir</button></form>';
```

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS pedido;
CREATE TABLE pedido (id INT AUTO_INCREMENT PRIMARY KEY, cliente VARCHAR(60) NOT NULL, subtotal DECIMAL(12, 2) NOT NULL, total DECIMAL(12, 2) NOT NULL);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`src/Modelo/Pedido.php`
```php
<?php
declare(strict_types=1);

namespace Tienda\Modelo;

readonly class Pedido
{
    public function __construct(public string $cliente, public float $subtotal, public float $descuento, public float $envio)
    {
    }

    public function total(): float
    {
        return $this->subtotal - $this->descuento + $this->envio;
    }
}
```

`src/Modelo/CalculadoraDePrecios.php`
```php
<?php
declare(strict_types=1);

namespace Tienda\Modelo;

class CalculadoraDePrecios
{
    public const DESDE_DESCUENTO = 50000;
    public const DESCUENTO = 0.10;
    public const DESDE_ENVIO_GRATIS = 80000;
    public const ENVIO = 3500;

    public function armar(string $cliente, float $subtotal): Pedido
    {
        $descuento = $subtotal >= self::DESDE_DESCUENTO ? $subtotal * self::DESCUENTO : 0;
        $envio = $subtotal >= self::DESDE_ENVIO_GRATIS ? 0 : self::ENVIO;
        return new Pedido($cliente, $subtotal, $descuento, $envio);
    }
}
```

`src/Modelo/PedidoRepositorio.php`
```php
<?php
declare(strict_types=1);

namespace Tienda\Modelo;

use PDO;

class PedidoRepositorio
{
    public function __construct(private PDO $pdo) {}

    public function guardar(Pedido $p): int
    {
        $this->pdo->prepare('INSERT INTO pedido (cliente, subtotal, total) VALUES (?, ?, ?)')->execute([$p->cliente, $p->subtotal, $p->total()]);
        return (int) $this->pdo->lastInsertId();
    }
}
```

`src/Controladores/PedidoControlador.php`
```php
<?php
declare(strict_types=1);

namespace Tienda\Controladores;

use Tienda\Modelo\CalculadoraDePrecios;
use Tienda\Modelo\PedidoRepositorio;

class PedidoControlador
{
    public function __construct(private CalculadoraDePrecios $precios, private PedidoRepositorio $pedidos, private \Closure $vista) {}

    public function formulario(): string
    {
        return ($this->vista)('formulario', []);
    }

    public function guardar(array $datos): string
    {
        $pedido = $this->precios->armar(trim($datos['cliente'] ?? ''), (float) ($datos['subtotal'] ?? 0));
        $this->pedidos->guardar($pedido);
        return ($this->vista)('resumen', ['pedido' => $pedido]);
    }
}
```

`vistas/formulario.php`
```php
<form method="post"><input name="cliente"><input name="subtotal"><button>Pedir</button></form>
```

`vistas/resumen.php`
```php
<h1>Pedido de <?= htmlspecialchars($pedido->cliente) ?></h1>
<p>Descuento: <?= $pedido->descuento ?> · Envío: <?= $pedido->envio ?> · Total: <?= $pedido->total() ?></p>
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Mision 3 - El controlador flaco: el mismo comportamiento, separado en MVC.
spl_autoload_register(function (string $clase): void {
    $archivo = __DIR__ . '/../src/' . str_replace('\\', '/', substr($clase, strlen('Tienda\\'))) . '.php';
    if (is_file($archivo)) {
        require $archivo;
    }
});

use Tienda\Controladores\PedidoControlador;
use Tienda\Modelo\CalculadoraDePrecios;
use Tienda\Modelo\PedidoRepositorio;

$c = require __DIR__ . '/../config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
$vista = function (string $__vista, array $__datos): string {
    extract($__datos);
    ob_start();
    require __DIR__ . "/../vistas/$__vista.php";
    return ob_get_clean();
};
$controlador = new PedidoControlador(new CalculadoraDePrecios(), new PedidoRepositorio($pdo), $vista);

echo $_SERVER['REQUEST_METHOD'] === 'POST' ? $controlador->guardar($_POST) : $controlador->formulario();
```

### Encargo R05-N01-E1 · La agenda de la peluquería

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Una peluquería quiere su agenda de turnos en la web, con MVC y MariaDB (tabla
`turno`: fecha, hora, cliente, servicio). Rutas:

- `GET /turnos` — los turnos del día de hoy o del día pedido con `?dia=AAAA-MM-DD`
  (validado), ordenados por hora;
- `GET /turnos/nuevo` — formulario;
- `POST /turnos` — valida (fecha válida, hora entre 09:00 y 19:30 en múltiplos de 30
  minutos, cliente y servicio de una lista) y guarda; si la hora ya está ocupada ese
  día (`UNIQUE (fecha, hora)` → `1062`), vuelve al formulario con el error;
- `POST /turnos/{id}/cancelar` — borra el turno y vuelve al día.

Con router, controlador, repositorio, vistas con layout, CSRF y PRG.

#### Criterio de aprobación

- Estructura MVC completa con un solo punto de entrada.
- La regla de horarios está en el modelo; el `1062` se atrapa y se muestra.
- Las acciones POST tienen CSRF y redirigen.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS turno;
CREATE TABLE turno (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    cliente VARCHAR(60) NOT NULL,
    servicio ENUM('corte', 'color', 'peinado', 'barba') NOT NULL,
    UNIQUE (fecha, hora)
);
INSERT INTO turno (fecha, hora, cliente, servicio) VALUES ('2026-10-06', '10:00', 'Ana Pérez', 'corte'), ('2026-10-06', '11:30', 'Beto Díaz', 'barba');
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`src/Router.php`
```php
<?php
declare(strict_types=1);

namespace Pelu;

class Router
{
    private array $rutas = [];

    public function get(string $p, callable $a): void
    {
        $this->rutas['GET'][$p] = $a;
    }

    public function post(string $p, callable $a): void
    {
        $this->rutas['POST'][$p] = $a;
    }

    public function despachar(string $metodo, string $ruta): string
    {
        foreach ($this->rutas[$metodo] ?? [] as $patron => $accion) {
            if (preg_match('#^' . preg_replace('#\{\w+\}#', '(\d+)', $patron) . '$#', $ruta, $m)) {
                return $accion(...array_map('intval', array_slice($m, 1)));
            }
        }
        http_response_code(404);
        return 'No existe esa página.';
    }
}
```

`src/Agenda.php`
```php
<?php
declare(strict_types=1);

namespace Pelu;

use PDO;
use PDOException;

class Agenda
{
    public const SERVICIOS = ['corte', 'color', 'peinado', 'barba'];

    public function __construct(private PDO $pdo) {}

    public static function fechaValida(string $texto): bool
    {
        $f = \DateTimeImmutable::createFromFormat('!Y-m-d', $texto);
        return $f !== false && $f->format('Y-m-d') === $texto;
    }

    /** Devuelve los errores por campo. */
    public function validar(array $d): array
    {
        $errores = [];
        if (!self::fechaValida($d['fecha'])) {
            $errores['fecha'] = 'La fecha no es válida.';
        }
        if (!preg_match('/^(\d{2}):(\d{2})$/', $d['hora'], $m) || $m[2] % 30 !== 0 || $d['hora'] < '09:00' || $d['hora'] > '19:30') {
            $errores['hora'] = 'Los turnos son de 09:00 a 19:30, cada media hora.';
        }
        if (trim($d['cliente']) === '') {
            $errores['cliente'] = 'Falta el nombre.';
        }
        if (!in_array($d['servicio'], self::SERVICIOS, true)) {
            $errores['servicio'] = 'Elegí un servicio de la lista.';
        }
        return $errores;
    }

    public function delDia(string $fecha): array
    {
        $s = $this->pdo->prepare("SELECT id, TIME_FORMAT(hora, '%H:%i') AS hora, cliente, servicio FROM turno WHERE fecha = ? ORDER BY hora");
        $s->execute([$fecha]);
        return $s->fetchAll();
    }

    /** Guarda el turno; devuelve false si la hora ya estaba ocupada. */
    public function reservar(array $d): bool
    {
        try {
            $this->pdo->prepare('INSERT INTO turno (fecha, hora, cliente, servicio) VALUES (?, ?, ?, ?)')->execute([$d['fecha'], $d['hora'], trim($d['cliente']), $d['servicio']]);
            return true;
        } catch (PDOException $e) {
            if (($e->errorInfo[1] ?? null) === 1062) {
                return false;
            }
            throw $e;
        }
    }

    public function cancelar(int $id): ?string
    {
        $s = $this->pdo->prepare('SELECT fecha FROM turno WHERE id = ?');
        $s->execute([$id]);
        $fecha = $s->fetchColumn();
        if ($fecha === false) {
            return null;
        }
        $this->pdo->prepare('DELETE FROM turno WHERE id = ?')->execute([$id]);
        return $fecha;
    }
}
```

`src/TurnoControlador.php`
```php
<?php
declare(strict_types=1);

namespace Pelu;

class TurnoControlador
{
    public function __construct(private Agenda $agenda, private \Closure $vista) {}

    public function dia(): string
    {
        $dia = $_GET['dia'] ?? date('Y-m-d');
        if (!Agenda::fechaValida($dia)) {
            $dia = date('Y-m-d');
        }
        return ($this->vista)('dia', ['titulo' => "Turnos del $dia", 'dia' => $dia, 'turnos' => $this->agenda->delDia($dia)]);
    }

    public function nuevo(array $datos = [], array $errores = []): string
    {
        $datos += ['fecha' => date('Y-m-d'), 'hora' => '09:00', 'cliente' => '', 'servicio' => 'corte'];
        return ($this->vista)('formulario', ['titulo' => 'Nuevo turno', 'datos' => $datos, 'errores' => $errores]);
    }

    public function crear(): string
    {
        $d = [];
        foreach (['fecha', 'hora', 'cliente', 'servicio'] as $campo) {
            $d[$campo] = trim((string) ($_POST[$campo] ?? ''));
        }
        $errores = $this->agenda->validar($d);
        if ($errores === [] && !$this->agenda->reservar($d)) {
            $errores['hora'] = 'Esa hora ya está ocupada.';
        }
        if ($errores !== []) {
            http_response_code(422);
            return $this->nuevo($d, $errores);
        }
        $_SESSION['flash'] = "Turno reservado: {$d['fecha']} {$d['hora']}.";
        header('Location: /turnos?dia=' . $d['fecha'], true, 303);
        return '';
    }

    public function cancelar(int $id): string
    {
        $fecha = $this->agenda->cancelar($id);
        if ($fecha === null) {
            http_response_code(404);
            return 'No existe ese turno.';
        }
        $_SESSION['flash'] = 'Turno cancelado.';
        header('Location: /turnos?dia=' . $fecha, true, 303);
        return '';
    }
}
```

`vistas/layout.php`
```php
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title><?= htmlspecialchars($titulo) ?> · Peluquería Rulos</title></head>
<body>
    <nav><a href="/turnos">Agenda</a> · <a href="/turnos/nuevo">Nuevo turno</a></nav>
    <?php if ($flash !== null): ?><p><strong><?= htmlspecialchars($flash) ?></strong></p><?php endif; ?>
    <h1><?= htmlspecialchars($titulo) ?></h1>
    <?= $contenido ?>
</body>
</html>
```

`vistas/dia.php`
```php
<form method="get"><input type="date" name="dia" value="<?= $dia ?>"> <button>Ver</button></form>
<?php if ($turnos === []): ?><p>No hay turnos.</p><?php endif; ?>
<ul>
    <?php foreach ($turnos as $t): ?>
        <li><?= $t['hora'] ?> · <?= htmlspecialchars($t['cliente']) ?> (<?= $t['servicio'] ?>)
            <form method="post" action="/turnos/<?= $t['id'] ?>/cancelar" style="display:inline">
                <input type="hidden" name="csrf" value="<?= $csrf ?>"><button>Cancelar</button>
            </form></li>
    <?php endforeach; ?>
</ul>
```

`vistas/formulario.php`
```php
<form method="post" action="/turnos">
    <input type="hidden" name="csrf" value="<?= $csrf ?>">
    <?php foreach (['fecha' => 'date', 'hora' => 'time', 'cliente' => 'text'] as $campo => $tipo): ?>
        <p><input type="<?= $tipo ?>" name="<?= $campo ?>" value="<?= htmlspecialchars($datos[$campo]) ?>">
            <?php if (isset($errores[$campo])): ?><strong><?= $errores[$campo] ?></strong><?php endif; ?></p>
    <?php endforeach; ?>
    <select name="servicio"><?php foreach (\Pelu\Agenda::SERVICIOS as $s): ?><option <?= $datos['servicio'] === $s ? 'selected' : '' ?>><?= $s ?></option><?php endforeach; ?></select>
    <?php if (isset($errores['servicio'])): ?><strong><?= $errores['servicio'] ?></strong><?php endif; ?>
    <button>Reservar</button>
</form>
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Encargo - La agenda de la peluquería: MVC con MariaDB, CSRF y PRG.
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (PHP_SAPI === 'cli-server' && $ruta !== '/' && is_file(__DIR__ . $ruta)) {
    return false;
}
session_start();
date_default_timezone_set('America/Argentina/Buenos_Aires');
foreach (['Router', 'Agenda', 'TurnoControlador'] as $clase) {
    require __DIR__ . "/../src/$clase.php";
}

use Pelu\Agenda;
use Pelu\Router;
use Pelu\TurnoControlador;

$_SESSION['csrf'] ??= bin2hex(random_bytes(32));
if ($_SERVER['REQUEST_METHOD'] === 'POST' && !hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
    http_response_code(403);
    exit('Pedido no válido.');
}
$c = require __DIR__ . '/../config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);

$vista = function (string $__vista, array $__datos): string {
    $__datos['csrf'] = $_SESSION['csrf'];
    extract($__datos);
    ob_start();
    require __DIR__ . "/../vistas/$__vista.php";
    $contenido = ob_get_clean();
    $flash = $_SESSION['flash'] ?? null;
    unset($_SESSION['flash']);
    ob_start();
    require __DIR__ . '/../vistas/layout.php';
    return ob_get_clean();
};

$turnos = new TurnoControlador(new Agenda($pdo), $vista);
$router = new Router();
$router->get('/turnos', [$turnos, 'dia']);
$router->get('/turnos/nuevo', [$turnos, 'nuevo']);
$router->post('/turnos', [$turnos, 'crear']);
$router->post('/turnos/{id}/cancelar', [$turnos, 'cancelar']);

echo $router->despachar($_SERVER['REQUEST_METHOD'], $ruta);
```

### Prueba del sello

#### ¿Qué hace cada pieza del MVC?

El modelo maneja los datos y sus reglas; la vista los muestra; el controlador recibe el pedido, le pide al modelo lo que necesita y elige la vista.

#### ¿Qué es un controlador frontal?

Un único archivo (`public/index.php`) por el que entran todos los pedidos; ahí se arma todo y el router decide a quién pasárselo.

#### ¿Por qué se usa `parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH)`?

Para quedarse solo con la ruta (`/barcos/12`) sin la query string (`?x=1`).

#### ¿Qué diferencia hay entre responder 404 y 405?

404: la ruta no existe. 405: la ruta existe, pero no acepta ese método (por ejemplo, un POST a una ruta que solo es GET).

#### ¿Cómo se simula un `DELETE` desde un formulario HTML?

Con un campo oculto (`_metodo=DELETE`) que el router lee cuando llega un POST, porque los formularios solo mandan GET y POST.

### Soluciones (docente)

Nodo nuevo, base de la Senda de Laravel. Todos los proyectos se prueban con `php -S localhost:8000 -t public public/index.php` (el tercer argumento es el router). En la misión 2, llamar a `$accion(...$parametros)` con un array asociativo usa argumentos con nombre (PHP 8.1): por eso los nombres de la ruta tienen que coincidir con los de los parámetros del método.

## R05-N02 · Closures, callables y generadores

```meta
tipo: tema
padre: R05-N01
precio: 10
criatura: troll
temas: func.closures, func.orden-superior, func.iteradores
```

### Crónica

En la sala de máquinas del Faro hay un tablero lleno de palancas intercambiables: cada palanca es una **instrucción** que se puede sacar y enchufar en otro lado. Y hay una cinta que no para de traer cajones desde la bodega: no los trae todos juntos, que no entrarían, sino **de a uno**, a medida que se necesitan.

—En PHP, las funciones también se pueden guardar, pasar y enchufar donde haga falta —dice {mentor}—. Y cuando los datos son demasiados para la memoria, se los trae de a uno con un **generador**. Con esas dos herramientas, {heroe}, escribís código más corto… y que no se ahoga con archivos gigantes.

### Objetivos

- Usar funciones como valores: closures, `fn`, `use` por valor y por referencia.
- Reconocer los callables: nombres de función, `[$objeto, 'metodo']`, `[Clase::class, 'metodo']` y la sintaxis `metodo(...)`.
- Escribir funciones que reciben y devuelven funciones (orden superior).
- Encadenar transformaciones de datos (`array_map`, `array_filter`, `array_reduce`, `usort`).
- Escribir generadores con `yield` para recorrer datos grandes sin cargarlos en memoria.

### Antes de empezar

- Funciones anónimas y `fn` (R01-N08), arrays y sus funciones (R01-N07).

### Explicación

#### Closures y `use`
```php
$iva = 0.21;
$conIva = function (float $precio) use ($iva): float {   // copia $iva al crearse
    return $precio * (1 + $iva);
};
$iva = 0.105;
echo $conIva(100);   // 121: la closure se quedó con 0.21
```
- `use ($x)` **copia** el valor en el momento de crear la función.
- `use (&$x)` usa la variable **por referencia**: ve y cambia la de afuera.
- `fn` captura sola las variables de afuera (por valor) y es de una sola expresión.

#### Callables
Todo lo que se puede "llamar":
```php
$f1 = 'strtoupper';                         // el nombre de una función
$f2 = [$repositorio, 'buscar'];             // método de un objeto
$f3 = [Conversor::class, 'aKm'];            // método estático
$f4 = strtoupper(...);                      // "first-class callable" (PHP 8.1): la función como objeto
$f5 = $repositorio->buscar(...);            // lo mismo con un método
echo $f4('hola');                           // HOLA
```
El tipo para parámetros es `callable` (o `Closure`, si se quiere solo closures).

#### Orden superior: funciones que reciben o devuelven funciones
```php
function multiplicador(float $factor): Closure
{
    return fn(float $x): float => $x * $factor;
}
$doble = multiplicador(2);
echo $doble(21);    // 42

function aplicarATodos(array $datos, callable ...$pasos): array
{
    foreach ($pasos as $paso) {
        $datos = array_map($paso, $datos);
    }
    return $datos;
}
aplicarATodos([' kira ', 'BRON'], trim(...), strtolower(...), ucfirst(...));   // ['Kira', 'Bron']
```

#### Transformar datos en cadena
```php
$totalValle = array_sum(
    array_map(fn($v) => $v['kilos'],
        array_filter($viajes, fn($v) => $v['destino'] === 'Valle')));

$porDestino = array_reduce($viajes, function (array $acc, array $v): array {
    $acc[$v['destino']] = ($acc[$v['destino']] ?? 0) + $v['kilos'];
    return $acc;
}, []);
```
`array_reduce` "reduce" un array a un solo valor (un número, o un array de resumen),
pasando un acumulador de vuelta en vuelta.

#### Generadores: `yield`
Una función con `yield` no devuelve todo junto: **produce** valores de a uno, y se
pausa entre cada uno:
```php
function numerosPares(int $hasta): Generator
{
    for ($i = 0; $i <= $hasta; $i += 2) {
        yield $i;                     // entrega un valor y se pausa acá
    }
}
foreach (numerosPares(10) as $n) { echo $n, ' '; }   // 0 2 4 6 8 10
```
Para qué sirve: leer un archivo de 2 GB renglón por renglón, o recorrer un millón de
filas de la base, **sin** cargarlo todo en memoria:
```php
function renglones(string $archivo): Generator
{
    $f = fopen($archivo, 'r');
    try {
        while (($linea = fgets($f)) !== false) {
            yield rtrim($linea, "\n");
        }
    } finally {
        fclose($f);                   // se cierra aunque se corte el recorrido
    }
}
```
- `yield $clave => $valor` produce pares con clave.
- `yield from otroGenerador()` delega en otro.
- Los generadores se pueden encadenar: uno lee, otro filtra, otro transforma… y
  solo hay **un** renglón en memoria a la vez.
- Un generador puede ser infinito (`while (true) { yield … }`): el que lo recorre
  decide cuándo parar.

`memory_get_peak_usage()` muestra cuánta memoria usó el programa: con generadores
se nota la diferencia.

### Código de ejemplo

```php
<?php
declare(strict_types=1);
/*
 * La sala de máquinas: closures, callables, orden superior y generadores.
 */
// use por valor y por referencia
$iva = 0.21;
$conIva = fn(float $p): float => round($p * (1 + $iva), 2);
$contador = 0;
$contar = function () use (&$contador): void {
    $contador++;
};
$iva = 0.105;
$contar();
$contar();
echo "Con IVA: ", $conIva(100), " · contador: $contador\n";

// Callables y first-class callables
$pasos = [trim(...), mb_strtolower(...), ucwords(...)];
$limpiar = fn(string $t): string => array_reduce($pasos, fn(string $acc, callable $f) => $f($acc), $t);
echo "Limpio: ", $limpiar('   KIRA DEL valle  '), "\n";

// Una función que devuelve funciones
function tarifa(float $porKilo, float $minimo): Closure
{
    return fn(float $kilos): float => max($minimo, $kilos * $porKilo);
}
$correo = tarifa(150, 800);
$express = tarifa(420, 2500);
foreach ([2, 12] as $kilos) {
    echo "$kilos kg: correo ", $correo($kilos), ", express ", $express($kilos), "\n";
}

// Transformar en cadena
$viajes = [
    ['destino' => 'Valle', 'kilos' => 420], ['destino' => 'Imperio', 'kilos' => 1100],
    ['destino' => 'Valle', 'kilos' => 380], ['destino' => 'Forjas', 'kilos' => 90],
];
$porDestino = array_reduce($viajes, function (array $acc, array $v): array {
    $acc[$v['destino']] = ($acc[$v['destino']] ?? 0) + $v['kilos'];
    return $acc;
}, []);
arsort($porDestino);
echo "Por destino: ", json_encode($porDestino), "\n";

// Generadores
function renglonesDeCarga(int $cantidad): Generator
{
    mt_srand(7);
    for ($i = 1; $i <= $cantidad; $i++) {
        yield $i => ['barco' => 'B' . mt_rand(1, 20), 'kilos' => mt_rand(10, 900)];
    }
}

function soloPesados(iterable $renglones, int $minimo): Generator
{
    foreach ($renglones as $n => $r) {
        if ($r['kilos'] >= $minimo) {
            yield $n => $r;
        }
    }
}

$total = 0;
$cantidad = 0;
foreach (soloPesados(renglonesDeCarga(200000), 850) as $n => $r) {
    $total += $r['kilos'];
    $cantidad++;
    if ($cantidad <= 3) {
        echo "  renglón $n: {$r['barco']} con {$r['kilos']} kg\n";
    }
}
echo "Pesados: $cantidad, total $total kg\n";
echo "Memoria usada: ", memory_get_peak_usage() < 4 * 1024 * 1024 ? 'menos de 4 MB' : 'mucha', "\n";
```

### Salida esperada

```
Con IVA: 121 · contador: 2
Limpio: Kira Del Valle
2 kg: correo 800, express 2500
12 kg: correo 1800, express 5040
Por destino: {"Imperio":1100,"Valle":800,"Forjas":90}
  renglón 1: B16 con 860 kg
  renglón 20: B6 con 882 kg
  renglón 28: B1 con 898 kg
Pesados: 11381, total 9961484 kg
Memoria usada: menos de 4 MB
```

### ¿Para qué sirve?

Los callables están en todos lados: el router del nodo anterior guarda `[$controlador, 'metodo']`, Laravel define rutas y *middlewares* con closures, y las colecciones de Laravel son cadenas de `map`/`filter`/`reduce`. Los generadores son la forma de procesar archivos y consultas enormes (importar un CSV de un millón de filas, exportar todas las ventas del año) sin quedarse sin memoria en un hosting compartido.

### Errores habituales

**Troll: `use` que no ve los cambios.** `use ($total)` copia el valor al crear la
función: sumarle adentro no cambia el `$total` de afuera. Para eso, `use (&$total)`
(o mejor, devolver el valor).

**Esqueleto: la variable de afuera en una `function`.** Sin `use`, una closure
`function () { return $iva; }` no ve `$iva`: `Undefined variable $iva`. Las `fn` sí la
ven.

**Ogro: recorrer un generador dos veces.** Un generador se consume: el segundo
`foreach` no produce nada (o da `Cannot traverse an already closed generator`). Si
necesitás los datos otra vez, volvé a llamar a la función.

**Goblin: `count()` de un generador.** Un generador no es un array: `count($gen)` da
error. Contá mientras lo recorrés, o `iterator_to_array` (que carga todo en
memoria… justo lo que querías evitar).

**Ogro: `array_filter` y las claves.** Encadenando `array_filter`, las claves quedan con
huecos: si después necesitás una lista, `array_values`.

### Misión R05-N02-M1 · El filtro de la bitácora

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La bitácora del Faro se procesa con **pasos** configurables. Escribí:

- `function tuberia(callable ...$pasos): Closure` — devuelve una función que recibe
  un array y le aplica los pasos en orden;
- `function filtrar(callable $condicion): Closure`, `function transformar(callable $f):
  Closure` y `function ordenarPor(string $campo, bool $desc = false): Closure` —
  cada una devuelve un paso (una closure que recibe un array y devuelve otro).

Con eso, armá dos tuberías sobre la lista de viajes del ejemplo: "los viajes al
Valle con más de 300 kg, ordenados por kilos de mayor a menor, como texto
`BARCO (KILOS kg)`" y "todos los viajes, con los kilos pasados a toneladas,
ordenados por barco". Mostrá el resultado de las dos.

#### Criterio de aprobación

- Las funciones reciben y devuelven closures.
- Las tuberías se arman combinando pasos, sin repetir código.
- La salida coincide con la esperada.

#### Salida esperada

```
Cóndor (760 kg), Gaviota (420 kg)
Albatros: 1.1 t
Cóndor: 0.76 t
Gaviota: 0.42 t
Petrel: 0.28 t
Tortuga: 0.09 t
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - El filtro de la bitácora: funciones que arman funciones.

function tuberia(callable ...$pasos): Closure
{
    return fn(array $datos): array => array_reduce($pasos, fn(array $acc, callable $paso) => $paso($acc), $datos);
}

function filtrar(callable $condicion): Closure
{
    return fn(array $datos): array => array_values(array_filter($datos, $condicion));
}

function transformar(callable $f): Closure
{
    return fn(array $datos): array => array_map($f, $datos);
}

function ordenarPor(string $campo, bool $desc = false): Closure
{
    return function (array $datos) use ($campo, $desc): array {
        usort($datos, fn($a, $b) => $desc ? $b[$campo] <=> $a[$campo] : $a[$campo] <=> $b[$campo]);
        return $datos;
    };
}

$viajes = [
    ['barco' => 'Gaviota', 'destino' => 'Valle', 'kilos' => 420],
    ['barco' => 'Albatros', 'destino' => 'Imperio', 'kilos' => 1100],
    ['barco' => 'Petrel', 'destino' => 'Valle', 'kilos' => 280],
    ['barco' => 'Cóndor', 'destino' => 'Valle', 'kilos' => 760],
    ['barco' => 'Tortuga', 'destino' => 'Forjas', 'kilos' => 90],
];

$pesadosAlValle = tuberia(
    filtrar(fn($v) => $v['destino'] === 'Valle' && $v['kilos'] > 300),
    ordenarPor('kilos', desc: true),
    transformar(fn($v) => "{$v['barco']} ({$v['kilos']} kg)"),
);
echo implode(', ', $pesadosAlValle($viajes)), "\n";

$enToneladas = tuberia(
    transformar(fn($v) => ['barco' => $v['barco'], 'toneladas' => $v['kilos'] / 1000]),
    ordenarPor('barco'),
);
foreach ($enToneladas($viajes) as $v) {
    echo "{$v['barco']}: {$v['toneladas']} t\n";
}
```

### Misión R05-N02-M2 · El lector de registros gigantes

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El servidor del Faro guarda un registro de accesos con un renglón por pedido:
`FECHA HORA METODO RUTA CODIGO MILISEGUNDOS`. Leé el registro de la entrada
estándar con un **generador** `renglones()` (sobre `STDIN`) y encadená otros dos:

- `parsear(iterable $renglones): Generator` — convierte cada renglón en un array con
  las 6 partes (saltea los renglones mal formados);
- `soloErrores(iterable $pedidos): Generator` — deja pasar los de código 400 o más.

Con eso calculá, sin guardar todos los pedidos en un array: la cantidad total de
pedidos válidos, cuántos fueron errores, la ruta con más errores y el pedido más
lento (en milisegundos).

#### Criterio de aprobación

- Usa generadores encadenados; no guarda el registro completo en memoria.
- Los renglones mal formados se saltean.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
2026-10-03 09:00:01 GET /barcos 200 35
2026-10-03 09:00:02 GET /barcos/7 404 12
2026-10-03 09:00:05 POST /barcos 201 88
renglon roto
2026-10-03 09:01:11 GET /barcos/7 404 10
2026-10-03 09:02:30 GET /reporte 500 1250
2026-10-03 09:03:00 GET /barcos 200 41
2026-10-03 09:03:30 DELETE /barcos/3 405 5
```

#### Salida esperada

```
Pedidos válidos: 7
Errores: 4
Ruta con más errores: /barcos/7 (2)
El más lento: GET /reporte (1250 ms, 09:02:30)
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 2 - El lector de registros gigantes: generadores encadenados.

function renglones($flujo): Generator
{
    while (($linea = fgets($flujo)) !== false) {
        yield trim($linea);
    }
}

function parsear(iterable $renglones): Generator
{
    foreach ($renglones as $linea) {
        $partes = explode(' ', $linea);
        if (count($partes) !== 6 || !ctype_digit($partes[4]) || !ctype_digit($partes[5])) {
            continue;
        }
        [$fecha, $hora, $metodo, $ruta, $codigo, $ms] = $partes;
        yield ['hora' => $hora, 'metodo' => $metodo, 'ruta' => $ruta, 'codigo' => (int) $codigo, 'ms' => (int) $ms];
    }
}

function soloErrores(iterable $pedidos, array &$contador): Generator
{
    foreach ($pedidos as $p) {
        $contador['total']++;
        if ($contador['total'] === 1 || $p['ms'] > $contador['lento']['ms']) {
            $contador['lento'] = $p;
        }
        if ($p['codigo'] >= 400) {
            yield $p;
        }
    }
}

$contador = ['total' => 0, 'lento' => null];
$errores = 0;
$porRuta = [];
foreach (soloErrores(parsear(renglones(STDIN)), $contador) as $p) {
    $errores++;
    $porRuta[$p['ruta']] = ($porRuta[$p['ruta']] ?? 0) + 1;
}
arsort($porRuta);

echo "Pedidos válidos: {$contador['total']}\n";
echo "Errores: $errores\n";
echo "Ruta con más errores: ", array_key_first($porRuta), " (", reset($porRuta), ")\n";
echo "El más lento: {$contador['lento']['metodo']} {$contador['lento']['ruta']} ({$contador['lento']['ms']} ms, {$contador['lento']['hora']})\n";
```

#### Pruebas

##### Sin errores
```entrada
2026-10-03 09:00:01 GET /a 200 10
2026-10-03 09:00:02 GET /b 301 20
```
```salida
Pedidos válidos: 2
Errores: 0
Ruta con más errores:  ()
El más lento: GET /b (20 ms, 09:00:02)
```

##### Todo roto
```entrada
hola
1 2 3
```
```salida
Pedidos válidos: 0
Errores: 0
Ruta con más errores:  ()
El más lento:   ( ms, )
```

##### Empate de errores
```entrada
2026-10-03 09:00:01 GET /a 404 1
2026-10-03 09:00:02 GET /b 404 1
```
```salida
Pedidos válidos: 2
Errores: 2
Ruta con más errores: /a (1)
El más lento: GET /a (1 ms, 09:00:01)
```

### Misión R05-N02-M3 · El número de turno infinito

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La oficina del Puerto numera los turnos así: `A001` a `A999`, después `B001`… hasta
`Z999`, y vuelve a `A001`. Escribí un **generador infinito** `turnos(string $desde =
'A001')` que produzca los números para siempre a partir de uno dado. Después:

1. mostrá los 5 primeros desde `A001`;
2. mostrá los 4 siguientes a `A998` (cruza a la B);
3. mostrá los 3 siguientes a `Z998` (vuelve a la A);
4. con un segundo generador `cadaN(iterable $origen, int $n)`, que deja pasar uno de
   cada `n`, mostrá los 4 primeros turnos de cada 250 desde `A001`.

Usá `break` para cortar cada recorrido.

#### Criterio de aprobación

- `turnos` es un generador infinito (`while (true)`).
- Los recorridos se cortan desde afuera.
- La salida coincide con la esperada.

#### Salida esperada

```
A001 A002 A003 A004 A005
A998 A999 B001 B002
Z998 Z999 A001
A001 A251 A501 A751
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - El número de turno infinito: un generador que no termina.

function turnos(string $desde = 'A001'): Generator
{
    $letra = ord($desde[0]);
    $numero = (int) substr($desde, 1);
    while (true) {
        yield chr($letra) . str_pad((string) $numero, 3, '0', STR_PAD_LEFT);
        $numero++;
        if ($numero > 999) {
            $numero = 1;
            $letra = $letra === ord('Z') ? ord('A') : $letra + 1;
        }
    }
}

function cadaN(iterable $origen, int $n): Generator
{
    $i = 0;
    foreach ($origen as $valor) {
        if ($i++ % $n === 0) {
            yield $valor;
        }
    }
}

function primeros(iterable $origen, int $cantidad): array
{
    $resultado = [];
    foreach ($origen as $valor) {
        if (count($resultado) === $cantidad) {
            break;
        }
        $resultado[] = $valor;
    }
    return $resultado;
}

echo implode(' ', primeros(turnos(), 5)), "\n";
echo implode(' ', primeros(turnos('A998'), 4)), "\n";
echo implode(' ', primeros(turnos('Z998'), 3)), "\n";
echo implode(' ', primeros(cadaN(turnos(), 250), 4)), "\n";
```

### Encargo R05-N02-E1 · La exportación de ventas

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Una distribuidora exporta sus ventas a CSV para el contador. La tabla tiene muchas
filas, así que el exportador no puede cargarlas todas en memoria. Escribí:

- `function filasDe(PDO $pdo, string $sql, array $parametros = []): Generator` —
  ejecuta la consulta preparada y hace `yield` de cada fila con `fetch()`;
- `function comoCsv(iterable $filas, array $columnas): Generator` — produce los
  renglones CSV (el primero con los títulos) usando `fputcsv` sobre
  `php://memory` para escapar bien las comas y comillas;
- un programa que exporta las ventas de octubre de 2026 (con un parámetro) a la
  salida estándar, y al final muestra por `STDERR` cuántas filas exportó (así la
  cuenta no se mezcla con el CSV).

El `esquema.sql` trae ventas de ejemplo (algunas fuera de octubre, y clientes con
comas y comillas en el nombre, para probar el escapado).

#### Criterio de aprobación

- La lectura de la base y el armado del CSV son generadores encadenados.
- Los textos con comas y comillas quedan bien escapados.
- La salida coincide con la esperada.

#### Salida esperada

```
id,fecha,cliente,total
2,2026-10-01,"Kiosco ""El Farol""",4200.50
3,2026-10-02,"Ferretería Ancla, SRL",96000.00
4,2026-10-15,"Fonda La Trompa Alegre",32150.00
5,2026-10-31,"Almacén Don Pepe",1200.00
Filas exportadas: 4
```

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS venta;
CREATE TABLE venta (id INT AUTO_INCREMENT PRIMARY KEY, fecha DATE NOT NULL, cliente VARCHAR(60) NOT NULL, total DECIMAL(10, 2) NOT NULL);
INSERT INTO venta (fecha, cliente, total) VALUES
    ('2026-09-30', 'Almacén Don Pepe', 18500), ('2026-10-01', 'Kiosco "El Farol"', 4200.5),
    ('2026-10-02', 'Ferretería Ancla, SRL', 96000), ('2026-10-15', 'Fonda La Trompa Alegre', 32150),
    ('2026-10-31', 'Almacén Don Pepe', 1200), ('2026-11-01', 'Kiosco "El Farol"', 800);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`exportar.php`
```php
<?php
declare(strict_types=1);
// Encargo - La exportación de ventas: generadores de la base al CSV.
$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);

function filasDe(PDO $pdo, string $sql, array $parametros = []): Generator
{
    $s = $pdo->prepare($sql);
    $s->execute($parametros);
    while (($fila = $s->fetch()) !== false) {
        yield $fila;
    }
}

function comoCsv(iterable $filas, array $columnas): Generator
{
    $memoria = fopen('php://memory', 'r+');
    $renglon = function (array $valores) use ($memoria): string {
        ftruncate($memoria, 0);
        rewind($memoria);
        fputcsv($memoria, $valores, ',', '"', '');
        rewind($memoria);
        return stream_get_contents($memoria);
    };
    yield $renglon($columnas);
    foreach ($filas as $fila) {
        yield $renglon(array_map(fn($c) => $fila[$c], $columnas));
    }
    fclose($memoria);
}

$exportadas = 0;
$filas = filasDe($pdo, 'SELECT id, fecha, cliente, total FROM venta WHERE fecha >= ? AND fecha < ? ORDER BY fecha, id', ['2026-10-01', '2026-11-01']);
foreach (comoCsv($filas, ['id', 'fecha', 'cliente', 'total']) as $n => $linea) {
    echo $linea;
    if ($n > 0) {
        $exportadas++;
    }
}
fwrite(STDERR, "Filas exportadas: $exportadas\n");
```

### Prueba del sello

#### ¿Qué diferencia hay entre `use ($x)` y `use (&$x)`?

`use ($x)` copia el valor al crear la closure; `use (&$x)` usa la variable de afuera por referencia (ve y hace cambios en ella).

#### ¿Qué es `strtoupper(...)`?

Un *first-class callable*: la función `strtoupper` como objeto, lista para guardarla o pasarla a otra función.

#### ¿Qué hace `yield`?

Entrega un valor desde un generador y lo pausa hasta que se pida el siguiente.

#### ¿Por qué un generador ahorra memoria?

Porque produce los valores de a uno, a medida que se recorren, en lugar de armar un array con todos.

#### ¿Qué pasa si recorrés dos veces el mismo generador?

La segunda vez no produce nada (o da error): un generador se consume. Hay que volver a llamar a la función.

### Soluciones (docente)

Sale de `21-PHP/14-Closures-Funcional` y `18-Generadores`. En el encargo, el conteo va por `STDERR` para no mezclarse con el CSV (probarlo con `php exportar.php > ventas.csv` y ver que el mensaje sigue en la terminal). `fputcsv` con el último parámetro `''` (sin carácter de escape) es lo recomendado desde PHP 8.4 y funciona igual en 8.2.

## R05-N03 · Una API REST en JSON

```meta
tipo: tema
padre: R05-N02
precio: 10
criatura: goblin
temas: web.api-rest, arch.json
usa: web.http
```

### Crónica

A la torre del Faro llegan cada vez más mensajes que no son de personas: son de **otras máquinas**. El sistema de la aduana pregunta qué barcos llegaron hoy; una aplicación de celular quiere mostrar el horario del ferry; el correo de otro puerto manda paquetes para registrar. No quieren páginas con colores y botones: quieren **datos**, ordenados, en un idioma que cualquier máquina entienda.

—Ese idioma es **JSON** —dice {mentor}—, y la forma ordenada de pedir y mandar datos por HTTP se llama **API REST**. Cada cosa tiene su dirección, cada acción su método y cada resultado su código. Si lo hacés bien, {heroe}, cualquier programa del mundo puede hablar con tu Puerto.

### Objetivos

- Entender qué es una API REST: recursos, métodos HTTP y códigos de estado.
- Responder JSON con el encabezado correcto y `json_encode`.
- Leer el cuerpo JSON de un pedido con `php://input` y `json_decode`.
- Implementar listar, ver, crear, modificar y borrar un recurso.
- Devolver errores en JSON con el código que corresponde (400, 404, 405, 422).
- Probar una API con `curl`.

### Antes de empezar

- MVC con router (R05-N01), consultas preparadas (R04-N05) y repositorios (R04-N08).

### Explicación

#### Recursos, métodos y códigos
En REST, cada **cosa** (un barco, un pedido) es un **recurso** con su dirección, y el
**método** HTTP dice qué hacer:
| Método y ruta | Hace | Responde |
|---|---|---|
| `GET /api/barcos` | lista | `200` y un array |
| `GET /api/barcos/7` | uno | `200`, o `404` si no existe |
| `POST /api/barcos` | crea | `201 Created` y el barco creado |
| `PUT /api/barcos/7` | reemplaza | `200` y el barco modificado |
| `DELETE /api/barcos/7` | borra | `204 No Content` (sin cuerpo) |

Otros códigos: **`400`** el JSON está mal formado, **`422`** el JSON está bien pero
los datos no pasan la validación, **`405`** el método no se acepta en esa ruta.

#### Responder JSON
```php
function responder(int $estado, mixed $datos): never
{
    http_response_code($estado);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($datos, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR);
    exit;
}
responder(200, ['id' => 7, 'nombre' => 'Gaviota', 'capacidad' => 450.0]);
```
- `JSON_UNESCAPED_UNICODE` deja las tildes como están (sin `ñ`).
- Los arrays asociativos salen como objetos (`{"id": 7}`); las listas, como arrays
  (`[1, 2]`). Un objeto con `JsonSerializable` decide cómo se convierte.

#### Leer JSON
Un cliente manda el cuerpo como JSON, **no** como formulario: `$_POST` queda vacío. Se
lee así:
```php
$cuerpo = file_get_contents('php://input');
try {
    $datos = json_decode($cuerpo, true, flags: JSON_THROW_ON_ERROR);
} catch (JsonException) {
    responder(400, ['error' => 'El cuerpo no es un JSON válido']);
}
```
Después se valida igual que un formulario: tipos, rangos, obligatorios.

#### Errores en JSON
Los errores también se responden en JSON, con un formato fijo:
```json
{"error": "Datos inválidos", "campos": {"capacidad": "Tiene que ser un número mayor que 0"}}
```
Así el cliente puede mostrar los errores al lado de cada campo.

#### Probar con `curl`
`curl` es un programa de terminal para hacer pedidos HTTP (viene en Linux, macOS y
Windows 10+):
```bash
curl http://localhost:8000/api/barcos
curl -X POST http://localhost:8000/api/barcos -H "Content-Type: application/json" -d '{"nombre":"Delfín","capacidad":300}'
curl -X DELETE -i http://localhost:8000/api/barcos/4       # -i muestra el código y los encabezados
```
(También hay programas gráficos como Postman, Insomnia o la extensión Thunder Client
de VS Code.)

#### Seguridad en una API
- Las APIs públicas usan **tokens** en lugar de sesiones (un encabezado
  `Authorization: Bearer …`), porque sus clientes no son navegadores: la Senda de
  JavaScript lo trabaja.
- Si la usa JavaScript de **otro** dominio, hacen falta los encabezados **CORS**
  (`Access-Control-Allow-Origin`).
- Todo lo de siempre sigue valiendo: consultas preparadas, validación, no mostrar
  errores internos.

### Código de ejemplo

`esquema.sql`
```sql
DROP TABLE IF EXISTS barco;
CREATE TABLE barco (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(40) NOT NULL UNIQUE, capacidad DECIMAL(8, 2) NOT NULL);
INSERT INTO barco (nombre, capacidad) VALUES ('Gaviota', 450), ('Albatros', 1200), ('Tortuga', 80);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`public/index.php`
```php
<?php
declare(strict_types=1);
/*
 * La API del Faro: un recurso REST con JSON.
 * Se prueba con: php -S localhost:8000 -t public public/index.php   y curl
 */
$c = require __DIR__ . '/../config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);

function responder(int $estado, mixed $datos = null): never
{
    http_response_code($estado);
    if ($datos !== null) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($datos, JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR);
    }
    exit;
}

function leerJson(): array
{
    try {
        $datos = json_decode(file_get_contents('php://input'), true, flags: JSON_THROW_ON_ERROR);
    } catch (JsonException) {
        responder(400, ['error' => 'El cuerpo no es un JSON válido']);
    }
    is_array($datos) || responder(400, ['error' => 'Se esperaba un objeto JSON']);
    return $datos;
}

function validarBarco(array $d): array
{
    $errores = [];
    if (!is_string($d['nombre'] ?? null) || trim($d['nombre']) === '' || mb_strlen($d['nombre']) > 40) {
        $errores['nombre'] = 'Obligatorio, hasta 40 caracteres';
    }
    if (!is_int($d['capacidad'] ?? null) && !is_float($d['capacidad'] ?? null) || ($d['capacidad'] ?? 0) <= 0) {
        $errores['capacidad'] = 'Tiene que ser un número mayor que 0';
    }
    if ($errores !== []) {
        responder(422, ['error' => 'Datos inválidos', 'campos' => $errores]);
    }
    return ['nombre' => trim($d['nombre']), 'capacidad' => (float) $d['capacidad']];
}

function comoJson(array $fila): array
{
    return ['id' => (int) $fila['id'], 'nombre' => $fila['nombre'], 'capacidad' => (float) $fila['capacidad']];
}

function buscar(PDO $pdo, int $id): array
{
    $s = $pdo->prepare('SELECT * FROM barco WHERE id = ?');
    $s->execute([$id]);
    return $s->fetch() ?: responder(404, ['error' => "No existe el barco $id"]);
}

$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$metodo = $_SERVER['REQUEST_METHOD'];

try {
    if ($ruta === '/api/barcos') {
        if ($metodo === 'GET') {
            responder(200, array_map('comoJson', $pdo->query('SELECT * FROM barco ORDER BY id')->fetchAll()));
        }
        if ($metodo === 'POST') {
            $d = validarBarco(leerJson());
            $pdo->prepare('INSERT INTO barco (nombre, capacidad) VALUES (?, ?)')->execute([$d['nombre'], $d['capacidad']]);
            header('Location: /api/barcos/' . $pdo->lastInsertId());
            responder(201, comoJson(buscar($pdo, (int) $pdo->lastInsertId())));
        }
        responder(405, ['error' => "Método $metodo no permitido"]);
    }
    if (preg_match('#^/api/barcos/(\d+)$#', $ruta, $m)) {
        $id = (int) $m[1];
        $barco = buscar($pdo, $id);
        match ($metodo) {
            'GET' => responder(200, comoJson($barco)),
            'PUT' => (function () use ($pdo, $id) {
                $d = validarBarco(leerJson());
                $pdo->prepare('UPDATE barco SET nombre = ?, capacidad = ? WHERE id = ?')->execute([$d['nombre'], $d['capacidad'], $id]);
                responder(200, comoJson(buscar($pdo, $id)));
            })(),
            'DELETE' => (function () use ($pdo, $id) {
                $pdo->prepare('DELETE FROM barco WHERE id = ?')->execute([$id]);
                responder(204);
            })(),
            default => responder(405, ['error' => "Método $metodo no permitido"]),
        };
    }
    responder(404, ['error' => 'No existe ese recurso']);
} catch (PDOException $e) {
    if (($e->errorInfo[1] ?? null) === 1062) {
        responder(422, ['error' => 'Datos inválidos', 'campos' => ['nombre' => 'Ya existe un barco con ese nombre']]);
    }
    error_log($e->getMessage());
    responder(500, ['error' => 'Error interno']);
}
```

### ¿Para qué sirve?

Las APIs son la forma en que se hablan los sistemas: la app de un banco con su servidor, una tienda con Mercado Pago, el sistema de facturación con AFIP/ARCA, un frontend en JavaScript o React con su backend en PHP. La Senda de los Mensajes Veloces arma una aplicación web completa que consume una API como esta, y Laravel tiene rutas `api` con todo esto resuelto.

### Errores habituales

**Goblin: leer JSON de `$_POST`.** Con `Content-Type: application/json`, `$_POST`
está vacío: el cuerpo se lee de `php://input`.

**Goblin: el texto que parece JSON.** Sin `header('Content-Type: application/json')`,
muchos clientes lo tratan como texto. Y un `echo` o un aviso de PHP antes del JSON
lo rompe: un solo `Warning` y el cliente recibe algo que no es JSON válido.

**Ogro: 200 para todo.** Responder `200` con `{"error": …}` confunde a los clientes
(que miran primero el código). Usá 201, 204, 400, 404, 422 según corresponda.

**Troll: mostrar la excepción al cliente.** Devolver `$e->getMessage()` de un
`PDOException` expone la estructura de la base. Registralo con `error_log` y
respondé `500` con un mensaje genérico.

**Goblin: el tipo de un número en JSON.** `{"capacidad": "300"}` trae un texto, no un
número. Decidí si lo aceptás (`is_numeric`) o lo rechazás (`is_int`/`is_float`), y
sé consistente.

### Misión R05-N03-M1 · La API de las mareas

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Escribí una API de solo lectura (sin base de datos: los datos en un array en el
código) con el horario de mareas de tres puertos:

- `GET /api/puertos` — lista de puertos (`codigo` y `nombre`);
- `GET /api/puertos/{codigo}/mareas` — las mareas de ese puerto, con un filtro
  opcional `?tipo=pleamar` o `?tipo=bajamar` (otro valor: `422` con el error);
- códigos inexistentes: `404`; cualquier método que no sea `GET`: `405`;
- todas las respuestas en JSON con `Content-Type: application/json`, incluidos los
  errores (`{"error": "…"}`).

#### Criterio de aprobación

- Responde JSON con el encabezado y el código correctos.
- Valida el filtro y responde 404/405/422 con un JSON de error.

#### Solución de referencia

`public/index.php`
```php
<?php
declare(strict_types=1);
// Mision 1 - La API de las mareas: una API de solo lectura en JSON.
const PUERTOS = [
    'MEN' => ['nombre' => 'Puerto de los Mensajeros', 'mareas' => [['hora' => '06:10', 'tipo' => 'pleamar', 'altura' => 4.2], ['hora' => '12:25', 'tipo' => 'bajamar', 'altura' => 0.8], ['hora' => '18:35', 'tipo' => 'pleamar', 'altura' => 4.0]]],
    'VAL' => ['nombre' => 'Muelle del Valle', 'mareas' => [['hora' => '07:00', 'tipo' => 'pleamar', 'altura' => 2.1], ['hora' => '13:10', 'tipo' => 'bajamar', 'altura' => 0.3]]],
    'FOR' => ['nombre' => 'Dársena de las Forjas', 'mareas' => []],
];

function responder(int $estado, array $datos): never
{
    http_response_code($estado);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($datos, JSON_UNESCAPED_UNICODE);
    exit;
}

$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    responder(405, ['error' => 'Esta API es de solo lectura']);
}
if ($ruta === '/api/puertos') {
    responder(200, array_map(fn($codigo) => ['codigo' => $codigo, 'nombre' => PUERTOS[$codigo]['nombre']], array_keys(PUERTOS)));
}
if (preg_match('#^/api/puertos/([A-Z]{3})/mareas$#', $ruta, $m)) {
    $puerto = PUERTOS[$m[1]] ?? responder(404, ['error' => "No existe el puerto {$m[1]}"]);
    $tipo = $_GET['tipo'] ?? '';
    if ($tipo !== '' && !in_array($tipo, ['pleamar', 'bajamar'], true)) {
        responder(422, ['error' => 'El tipo es pleamar o bajamar']);
    }
    $mareas = array_values(array_filter($puerto['mareas'], fn($x) => $tipo === '' || $x['tipo'] === $tipo));
    responder(200, ['puerto' => $puerto['nombre'], 'mareas' => $mareas]);
}
responder(404, ['error' => 'No existe ese recurso']);
```

### Misión R05-N03-M2 · La API de tareas

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Escribí una API REST completa para una lista de **tareas** en MariaDB (tabla `tarea`:
título, hecha `BOOLEAN`, prioridad `baja`/`media`/`alta`, creada `DATETIME`):

- `GET /api/tareas` (con `?hecha=0|1` opcional), `GET /api/tareas/{id}`;
- `POST /api/tareas` — crea con título (1 a 100 caracteres) y prioridad (por
  defecto `media`), responde `201` y el encabezado `Location`;
- `PATCH /api/tareas/{id}` — cambia **solo** los campos que vengan (`titulo`,
  `hecha`, `prioridad`), validando cada uno;
- `DELETE /api/tareas/{id}` — `204`;
- errores: JSON mal formado `400`, validación `422` con los campos, inexistente `404`.

En las respuestas, `hecha` es un booleano de JSON (`true`/`false`), no `1`/`0`.

#### Criterio de aprobación

- Los cinco endpoints con los códigos correctos.
- `PATCH` actualiza solo los campos enviados.
- Los tipos del JSON son los correctos (`id` entero, `hecha` booleano).

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS tarea;
CREATE TABLE tarea (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    hecha BOOLEAN NOT NULL DEFAULT FALSE,
    prioridad ENUM('baja', 'media', 'alta') NOT NULL DEFAULT 'media',
    creada DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO tarea (titulo, hecha, prioridad) VALUES ('Pintar el casco', FALSE, 'alta'), ('Cambiar las velas', TRUE, 'media');
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Mision 2 - La API de tareas: GET, POST, PATCH y DELETE con JSON.
$c = require __DIR__ . '/../config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);
const PRIORIDADES = ['baja', 'media', 'alta'];

function responder(int $estado, ?array $datos = null): never
{
    http_response_code($estado);
    if ($datos !== null) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($datos, JSON_UNESCAPED_UNICODE);
    }
    exit;
}

function cuerpo(): array
{
    try {
        $d = json_decode(file_get_contents('php://input'), true, flags: JSON_THROW_ON_ERROR);
    } catch (JsonException) {
        responder(400, ['error' => 'JSON inválido']);
    }
    return is_array($d) ? $d : responder(400, ['error' => 'Se esperaba un objeto JSON']);
}

function validar(array $d, bool $parcial): array
{
    $errores = [];
    $limpio = [];
    if (array_key_exists('titulo', $d) || !$parcial) {
        $t = is_string($d['titulo'] ?? null) ? trim($d['titulo']) : '';
        $t === '' || mb_strlen($t) > 100 ? $errores['titulo'] = 'De 1 a 100 caracteres' : $limpio['titulo'] = $t;
    }
    if (array_key_exists('hecha', $d)) {
        is_bool($d['hecha']) ? $limpio['hecha'] = (int) $d['hecha'] : $errores['hecha'] = 'Tiene que ser true o false';
    }
    if (array_key_exists('prioridad', $d) || !$parcial) {
        $p = $d['prioridad'] ?? 'media';
        in_array($p, PRIORIDADES, true) ? $limpio['prioridad'] = $p : $errores['prioridad'] = 'baja, media o alta';
    }
    if ($errores !== []) {
        responder(422, ['error' => 'Datos inválidos', 'campos' => $errores]);
    }
    return $limpio;
}

function tarea(PDO $pdo, int $id): array
{
    $s = $pdo->prepare('SELECT id, titulo, hecha, prioridad FROM tarea WHERE id = ?');
    $s->execute([$id]);
    $t = $s->fetch() ?: responder(404, ['error' => "No existe la tarea $id"]);
    return ['id' => (int) $t['id'], 'titulo' => $t['titulo'], 'hecha' => (bool) $t['hecha'], 'prioridad' => $t['prioridad']];
}

$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$metodo = $_SERVER['REQUEST_METHOD'];

if ($ruta === '/api/tareas') {
    if ($metodo === 'GET') {
        $hecha = $_GET['hecha'] ?? null;
        $sql = 'SELECT id FROM tarea' . ($hecha === null ? '' : ' WHERE hecha = ?') . ' ORDER BY id';
        $s = $pdo->prepare($sql);
        $s->execute($hecha === null ? [] : [(int) ($hecha === '1')]);
        responder(200, array_map(fn($id) => tarea($pdo, (int) $id), $s->fetchAll(PDO::FETCH_COLUMN)));
    }
    if ($metodo === 'POST') {
        $d = validar(cuerpo(), false);
        $pdo->prepare('INSERT INTO tarea (titulo, prioridad) VALUES (?, ?)')->execute([$d['titulo'], $d['prioridad']]);
        $id = (int) $pdo->lastInsertId();
        header("Location: /api/tareas/$id");
        responder(201, tarea($pdo, $id));
    }
    responder(405, ['error' => 'Método no permitido']);
}
if (preg_match('#^/api/tareas/(\d+)$#', $ruta, $m)) {
    $id = (int) $m[1];
    $actual = tarea($pdo, $id);
    if ($metodo === 'GET') {
        responder(200, $actual);
    }
    if ($metodo === 'PATCH') {
        $d = validar(cuerpo(), true);
        if ($d !== []) {
            $sets = implode(', ', array_map(fn($campo) => "$campo = ?", array_keys($d)));
            $pdo->prepare("UPDATE tarea SET $sets WHERE id = ?")->execute([...array_values($d), $id]);
        }
        responder(200, tarea($pdo, $id));
    }
    if ($metodo === 'DELETE') {
        $pdo->prepare('DELETE FROM tarea WHERE id = ?')->execute([$id]);
        responder(204);
    }
    responder(405, ['error' => 'Método no permitido']);
}
responder(404, ['error' => 'No existe ese recurso']);
```

### Misión R05-N03-M3 · El cliente de la API

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Del otro lado de una API hay un **cliente**. Escribí `cliente.php`, un programa de
terminal que consume la API de tareas de la misión 2 (levantala con `php -S` en
otra terminal) usando `file_get_contents` con un **contexto de flujo**
(`stream_context_create`) para mandar el método, los encabezados y el cuerpo:

- una función `pedir(string $metodo, string $ruta, ?array $cuerpo = null): array` que
  devuelve `['estado' => 201, 'datos' => [...]]` (el código sale de
  `$http_response_header[0]`; con `'ignore_errors' => true` no se corta en 4xx);
- crea una tarea, la marca como hecha con `PATCH`, intenta crear una inválida
  (muestra los errores de campo que devuelve la API) y lista las pendientes.

Para esta entrega no hay salida esperada fija (depende de los datos): mostrá cada
paso con el código recibido.

#### Criterio de aprobación

- Usa `stream_context_create` con método, encabezados y cuerpo JSON.
- Lee el código de estado y decodifica las respuestas.
- Muestra los errores de validación que manda la API.

#### Solución de referencia

`cliente.php`
```php
<?php
declare(strict_types=1);
// Mision 3 - El cliente de la API: consumir JSON con file_get_contents y un contexto.
const BASE = 'http://localhost:8000';

function pedir(string $metodo, string $ruta, ?array $cuerpo = null): array
{
    $contexto = stream_context_create(['http' => [
        'method' => $metodo,
        'header' => "Content-Type: application/json\r\nAccept: application/json\r\n",
        'content' => $cuerpo === null ? '' : json_encode($cuerpo),
        'ignore_errors' => true,          // no cortar con los 4xx: queremos leer el error
    ]]);
    $respuesta = file_get_contents(BASE . $ruta, false, $contexto);
    preg_match('#HTTP/\S+ (\d{3})#', $http_response_header[0] ?? '', $m);
    return ['estado' => (int) ($m[1] ?? 0), 'datos' => $respuesta === '' ? null : json_decode($respuesta, true)];
}

$nueva = pedir('POST', '/api/tareas', ['titulo' => 'Revisar el ancla', 'prioridad' => 'alta']);
echo "Crear: {$nueva['estado']} → tarea {$nueva['datos']['id']}\n";

$hecha = pedir('PATCH', "/api/tareas/{$nueva['datos']['id']}", ['hecha' => true]);
echo "Marcar hecha: {$hecha['estado']} → hecha = ", var_export($hecha['datos']['hecha'], true), "\n";

$mala = pedir('POST', '/api/tareas', ['titulo' => '', 'prioridad' => 'urgente']);
echo "Crear inválida: {$mala['estado']}\n";
foreach ($mala['datos']['campos'] ?? [] as $campo => $mensaje) {
    echo "  $campo: $mensaje\n";
}

$pendientes = pedir('GET', '/api/tareas?hecha=0');
echo "Pendientes: {$pendientes['estado']} → ", implode(', ', array_column($pendientes['datos'], 'titulo')), "\n";
```

### Encargo R05-N03-E1 · La API del stock para la app del depósito

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Un depósito quiere una app de celular para sus repositores. Hacé la API que la
alimenta, con MariaDB (tablas `producto` y `movimiento`) y un **token** fijo:

- todos los pedidos tienen que traer el encabezado `Authorization: Bearer
  deposito-2026` (el token va en `config.php`); si no, `401` con
  `{"error": "No autorizado"}` (compará con `hash_equals`);
- `GET /api/productos?buscar=…` — productos que coinciden por nombre o código;
- `GET /api/productos/{codigo}` — el producto y sus **últimos 5 movimientos**;
- `POST /api/productos/{codigo}/movimientos` — `{"tipo": "entrada"|"salida",
  "cantidad": N}`: en una **transacción** con `FOR UPDATE`, registra el movimiento y
  actualiza el stock; una salida que deja el stock negativo responde `409 Conflict`
  con el stock disponible.

#### Criterio de aprobación

- Todas las rutas exigen el token (401 si falta o es incorrecto).
- Los movimientos se registran en una transacción; el 409 no deja nada a medias.
- Las respuestas son JSON con los tipos correctos.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS movimiento;
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (codigo CHAR(6) PRIMARY KEY, nombre VARCHAR(60) NOT NULL, stock INT NOT NULL CHECK (stock >= 0)) ENGINE=InnoDB;
CREATE TABLE movimiento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo CHAR(6) NOT NULL,
    tipo ENUM('entrada', 'salida') NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    FOREIGN KEY (codigo) REFERENCES producto(codigo)
) ENGINE=InnoDB;
INSERT INTO producto VALUES ('ACE001', 'Aceite girasol 1,5 l', 24), ('YER001', 'Yerba mate 1 kg', 6), ('SAL001', 'Sal fina 500 g', 40);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => '', 'token' => 'deposito-2026'];
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Encargo - La API del stock: token, búsqueda y movimientos en transacción.
$c = require __DIR__ . '/../config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);

function responder(int $estado, array $datos): never
{
    http_response_code($estado);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($datos, JSON_UNESCAPED_UNICODE);
    exit;
}

$token = preg_replace('/^Bearer\s+/', '', $_SERVER['HTTP_AUTHORIZATION'] ?? '');
if (!hash_equals($c['token'], $token)) {
    responder(401, ['error' => 'No autorizado']);
}

$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$metodo = $_SERVER['REQUEST_METHOD'];

if ($ruta === '/api/productos' && $metodo === 'GET') {
    $s = $pdo->prepare('SELECT codigo, nombre, stock FROM producto WHERE nombre LIKE :n OR codigo LIKE :c ORDER BY codigo');
    $texto = '%' . trim($_GET['buscar'] ?? '') . '%';
    $s->execute(['n' => $texto, 'c' => $texto]);
    responder(200, array_map(fn($p) => ['codigo' => $p['codigo'], 'nombre' => $p['nombre'], 'stock' => (int) $p['stock']], $s->fetchAll()));
}

if (preg_match('#^/api/productos/([A-Z]{3}\d{3})(/movimientos)?$#', $ruta, $m)) {
    $codigo = $m[1];
    if (($m[2] ?? '') === '' && $metodo === 'GET') {
        $s = $pdo->prepare('SELECT codigo, nombre, stock FROM producto WHERE codigo = ?');
        $s->execute([$codigo]);
        $p = $s->fetch() ?: responder(404, ['error' => "No existe $codigo"]);
        $movs = $pdo->prepare('SELECT tipo, cantidad FROM movimiento WHERE codigo = ? ORDER BY id DESC LIMIT 5');
        $movs->execute([$codigo]);
        responder(200, ['codigo' => $p['codigo'], 'nombre' => $p['nombre'], 'stock' => (int) $p['stock'],
            'movimientos' => array_map(fn($x) => ['tipo' => $x['tipo'], 'cantidad' => (int) $x['cantidad']], $movs->fetchAll())]);
    }
    if (($m[2] ?? '') === '/movimientos' && $metodo === 'POST') {
        $d = json_decode(file_get_contents('php://input'), true);
        if (!is_array($d) || !in_array($d['tipo'] ?? '', ['entrada', 'salida'], true) || !is_int($d['cantidad'] ?? null) || $d['cantidad'] <= 0) {
            responder(422, ['error' => 'tipo: entrada|salida, cantidad: entero positivo']);
        }
        $pdo->beginTransaction();
        try {
            $s = $pdo->prepare('SELECT stock FROM producto WHERE codigo = ? FOR UPDATE');
            $s->execute([$codigo]);
            $stock = $s->fetchColumn();
            if ($stock === false) {
                $pdo->rollBack();
                responder(404, ['error' => "No existe $codigo"]);
            }
            $nuevo = (int) $stock + ($d['tipo'] === 'entrada' ? $d['cantidad'] : -$d['cantidad']);
            if ($nuevo < 0) {
                $pdo->rollBack();
                responder(409, ['error' => 'Stock insuficiente', 'disponible' => (int) $stock]);
            }
            $pdo->prepare('INSERT INTO movimiento (codigo, tipo, cantidad) VALUES (?, ?, ?)')->execute([$codigo, $d['tipo'], $d['cantidad']]);
            $pdo->prepare('UPDATE producto SET stock = ? WHERE codigo = ?')->execute([$nuevo, $codigo]);
            $pdo->commit();
            responder(201, ['codigo' => $codigo, 'stock' => $nuevo]);
        } catch (PDOException $e) {
            $pdo->rollBack();
            error_log($e->getMessage());
            responder(500, ['error' => 'Error interno']);
        }
    }
}
responder(404, ['error' => 'No existe ese recurso']);
```

### Prueba del sello

#### ¿Qué código se responde al crear un recurso, y cuál al borrarlo?

`201 Created` al crear (con el recurso y el encabezado `Location`) y `204 No Content` al borrar.

#### ¿Por qué `$_POST` está vacío cuando llega un JSON?

Porque PHP solo llena `$_POST` con formularios; un cuerpo JSON se lee de `php://input` y se decodifica con `json_decode`.

#### ¿Qué diferencia hay entre responder 400 y 422?

400: el pedido está mal formado (el JSON no se puede leer). 422: el JSON está bien, pero los datos no pasan la validación.

#### ¿Qué hace `JSON_UNESCAPED_UNICODE`?

Deja las tildes y las ñ tal cual en el JSON, en lugar de convertirlas a `ñ`.

#### ¿Qué diferencia hay entre `PUT` y `PATCH`?

`PUT` reemplaza el recurso entero (se mandan todos los campos); `PATCH` cambia solo los campos que se envían.

### Soluciones (docente)

Nodo nuevo. Se prueba con `php -S localhost:8000 -t public public/index.php` y `curl` (o Thunder Client en VS Code). En la misión 2, el `UPDATE` del `PATCH` arma la lista de columnas con los nombres del array ya validado (vienen de la lista de campos permitidos, no del cliente), y los valores van como parámetros. La misión 3 no tiene salida esperada porque depende de lo que haya en la base: se corrige mirando que cada paso muestre el código correcto. En el encargo, con `php -S` el encabezado `Authorization` llega en `$_SERVER['HTTP_AUTHORIZATION']`; en Apache a veces hace falta una línea en el `.htaccess` (se ve en el nodo de hosting).

## R05-N04 · Pruebas con PHPUnit

```meta
tipo: tema
padre: R05-N03
precio: 10
criatura: ogre
temas: cal.pruebas
usa: cal.build
```

### Crónica

El ingeniero del Faro revisaba la lámpara a mano cada noche: encendía, medía, anotaba. Un día se enfermó y nadie supo cómo revisarla; esa misma noche la lámpara falló. Desde entonces, junto a la lámpara hay un **banco de pruebas**: se aprieta un botón y en un segundo prueba las cuarenta cosas que el ingeniero revisaba, siempre igual, sin olvidarse de ninguna.

—Cada vez que tocás el código, podés romper algo que andaba —dice {mentor}—. Probar todo a mano cada vez es imposible. Las **pruebas automáticas** son programas que prueban tus programas: se escriben una vez y se corren siempre. Y el ogro de los errores silenciosos, {heroe}, les tiene terror.

### Objetivos

- Instalar PHPUnit con Composer y configurarlo.
- Escribir pruebas con `TestCase` y las aserciones más comunes.
- Probar que se lancen las excepciones esperadas.
- Probar muchos casos con `#[DataProvider]`.
- Aislar la lógica de la base usando repositorios en memoria (dobles de prueba).
- Leer el resultado de las pruebas y usarlas para cambiar el código sin miedo.

### Antes de empezar

- Composer y autoload (R02-N10), interfaces y repositorios (R02-N06, R04-N08).

### Explicación

#### Instalar
```bash
composer require --dev phpunit/phpunit ^11
```
`--dev` porque solo hace falta para desarrollar (en el servidor no se instala). Y un
`phpunit.xml` en la raíz del proyecto:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit bootstrap="vendor/autoload.php" colors="true">
    <testsuites>
        <testsuite name="Faro">
            <directory>tests</directory>
        </testsuite>
    </testsuites>
</phpunit>
```
Se corre con:
```bash
vendor/bin/phpunit
```

#### La primera prueba
Las pruebas van en `tests/`, en clases que terminan en `Test` y heredan de
`TestCase`; cada método que empieza con `test` es una prueba:
```php
use PHPUnit\Framework\TestCase;

final class CalculadoraTest extends TestCase
{
    public function testSinDescuentoPorDebajoDelMinimo(): void
    {
        $calc = new CalculadoraDePrecios();
        $pedido = $calc->armar('Ana', 40000);
        $this->assertSame(0.0, $pedido->descuento);
        $this->assertSame(3500.0, $pedido->envio);
    }
}
```
Una buena prueba tiene tres partes: **preparar** (crear los objetos), **actuar**
(llamar al método) y **verificar** (las aserciones).

#### Aserciones más usadas
| Aserción | Pasa si… |
|---|---|
| `assertSame($esperado, $real)` | son idénticos (`===`, mismo tipo) |
| `assertEquals($esperado, $real)` | son iguales (`==`) |
| `assertEqualsWithDelta(0.3, $real, 0.0001)` | floats casi iguales |
| `assertTrue($x)`, `assertFalse($x)`, `assertNull($x)` | … |
| `assertCount(3, $array)` | tiene 3 elementos |
| `assertContains('x', $array)` | el array contiene el valor |
| `assertStringContainsString('ok', $texto)` | el texto contiene… |
| `assertInstanceOf(Barco::class, $obj)` | es de esa clase |

Siempre **esperado primero**, después el real (así el mensaje de error se lee bien).

#### Probar excepciones
```php
public function testNoAceptaCapacidadNegativa(): void
{
    $this->expectException(InvalidArgumentException::class);
    $this->expectExceptionMessage('capacidad');       // un pedazo del mensaje
    new Barco(null, 'Gaviota', -5);                   // tiene que lanzar
}
```

#### Muchos casos: `DataProvider`
```php
use PHPUnit\Framework\Attributes\DataProvider;

#[DataProvider('bisiestos')]
public function testBisiesto(int $anio, bool $esperado): void
{
    $this->assertSame($esperado, Calendario::esBisiesto($anio));
}

public static function bisiestos(): array
{
    return [
        'común' => [2026, false],
        'múltiplo de 4' => [2024, true],
        'siglo' => [1900, false],
        'cada 400' => [2000, true],
    ];
}
```
Cada fila es una prueba; el nombre (la clave) aparece si falla.

#### Aislar la base: dobles de prueba
Las pruebas tienen que ser **rápidas** y **repetibles**. Si la lógica recibe una
**interfaz** de repositorio (R04-N08), en la prueba se le pasa una versión en
memoria:
```php
$servicio = new ServicioReservas(new ReservaRepositorioEnMemoria());
```
Y `setUp()` prepara lo común antes de cada prueba:
```php
private ServicioReservas $servicio;

protected function setUp(): void
{
    $this->servicio = new ServicioReservas(new ReservaRepositorioEnMemoria());
}
```

#### Leer el resultado
```
...F.                                                               5 / 5 (100%)

1) CalculadoraTest::testEnvioGratisDesde80000
Failed asserting that 3500.0 is identical to 0.0.
```
Un punto por prueba que pasa; `F` falló (una aserción no se cumplió); `E` hubo un
error (una excepción inesperada). El detalle dice qué se esperaba y qué pasó.

#### Qué probar
- Las **reglas del negocio**: descuentos, límites, estados, validaciones.
- Los **casos borde**: cero, vacío, el límite exacto, el día 29 de febrero.
- Cada **error** que corregís: primero una prueba que falla, después el arreglo.
  Así ese error no vuelve nunca.

### Código de ejemplo

`composer.json`
```json
{
    "name": "puerto/faro-pruebas",
    "require": { "php": ">=8.2" },
    "require-dev": { "phpunit/phpunit": "^11.5" },
    "autoload": { "psr-4": { "Faro\\": "src/" } }
}
```

`phpunit.xml`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit bootstrap="vendor/autoload.php" colors="false">
    <testsuites>
        <testsuite name="Faro">
            <directory>tests</directory>
        </testsuite>
    </testsuites>
</phpunit>
```

`src/Tarifario.php`
```php
<?php
declare(strict_types=1);

namespace Faro;

use InvalidArgumentException;

final class Tarifario
{
    public const MINIMO = 800;
    public const POR_KILO = 150;
    public const RECARGO_URGENTE = 0.5;

    public function precio(float $kilos, bool $urgente = false): float
    {
        if ($kilos <= 0) {
            throw new InvalidArgumentException("El peso tiene que ser positivo: $kilos");
        }
        $precio = max(self::MINIMO, $kilos * self::POR_KILO);
        return $urgente ? $precio * (1 + self::RECARGO_URGENTE) : $precio;
    }
}
```

`tests/TarifarioTest.php`
```php
<?php
declare(strict_types=1);

use Faro\Tarifario;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;

final class TarifarioTest extends TestCase
{
    private Tarifario $tarifario;

    protected function setUp(): void
    {
        $this->tarifario = new Tarifario();
    }

    public function testPaquetesChicosPaganElMinimo(): void
    {
        $this->assertSame(800.0, $this->tarifario->precio(2));
    }

    public function testLosGrandesPaganPorKilo(): void
    {
        $this->assertSame(1800.0, $this->tarifario->precio(12));
    }

    public function testUrgenteTieneRecargo(): void
    {
        $this->assertSame(2700.0, $this->tarifario->precio(12, urgente: true));
    }

    #[DataProvider('pesosInvalidos')]
    public function testRechazaPesosInvalidos(float $kilos): void
    {
        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('positivo');
        $this->tarifario->precio($kilos);
    }

    public static function pesosInvalidos(): array
    {
        return ['cero' => [0], 'negativo' => [-3.5]];
    }

    #[DataProvider('limites')]
    public function testElLimiteDelMinimo(float $kilos, float $esperado): void
    {
        $this->assertEqualsWithDelta($esperado, $this->tarifario->precio($kilos), 0.001);
    }

    public static function limites(): array
    {
        return [
            'justo en el mínimo' => [5.3333, 800.0],
            'apenas pasa' => [5.34, 801.0],
        ];
    }
}
```

### ¿Para qué sirve?

Las pruebas automáticas son lo que permite cambiar un sistema grande sin miedo: esta misma plataforma tiene cientos de pruebas que se corren antes de cada cambio. En cualquier empresa se pide saber escribirlas, y Laravel trae PHPUnit (y Pest, que se basa en él) configurado, con ayudas para probar rutas, formularios y la base de datos.

### Errores habituales

**Ogro: la prueba que no prueba nada.** Una prueba sin aserciones pasa siempre (PHPUnit
la marca como *risky*). Cada prueba verifica algo.

**Esqueleto: `No tests executed!`.** La clase no termina en `Test`, el método no
empieza con `test` (o no tiene `#[Test]`), o el `phpunit.xml` apunta a otra carpeta.

**Goblin: `assertEquals` con tipos distintos.** `assertEquals(0, '0')` pasa (compara
con `==`). Para no dejar pasar goblins, `assertSame`.

**Ogro: comparar floats exactos.** `assertSame(0.3, 0.1 + 0.2)` falla. Para decimales,
`assertEqualsWithDelta`.

**Troll: pruebas que dependen de otras o de la base.** Si una prueba necesita que otra
haya corrido antes, o datos que "estaban" en la base, falla según el día. Cada prueba
prepara lo suyo (`setUp`, repositorios en memoria).

### Misión R05-N04-M1 · Las pruebas del CUIT

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Llevá la validación del CUIT (R01-N08-E1) a una clase `Faro\Cuit` con un método de
fábrica `Cuit::desdeTexto(string $texto): self` (lanza `InvalidArgumentException` si
es inválido), `__toString()` con el formato `20-12345678-6` y `tipo(): string`
(`persona` si empieza con 20, 23, 24 o 27; `empresa` si empieza con 30, 33 o 34).
Escribí `tests/CuitTest.php` con:

- un `DataProvider` de CUITs válidos (con y sin guiones) que verifica el formato;
- un `DataProvider` de inválidos (largo, letras, verificador mal) que espera la
  excepción;
- pruebas del `tipo()`.

Entregá el proyecto con `composer.json`, `phpunit.xml`, `src/` y `tests/` (sin
`vendor/`). Todas las pruebas tienen que pasar.

#### Criterio de aprobación

- Usa `DataProvider` para válidos e inválidos y `expectException`.
- `vendor/bin/phpunit` termina en `OK`.

#### Solución de referencia

`composer.json`
```json
{
    "require-dev": { "phpunit/phpunit": "^11.5" },
    "autoload": { "psr-4": { "Faro\\": "src/" } }
}
```

`phpunit.xml`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit bootstrap="vendor/autoload.php" colors="false">
    <testsuites>
        <testsuite name="Cuit"><directory>tests</directory></testsuite>
    </testsuites>
</phpunit>
```

`src/Cuit.php`
```php
<?php
declare(strict_types=1);

namespace Faro;

use InvalidArgumentException;

final class Cuit
{
    private const PESOS = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2];

    private function __construct(private string $digitos) {}

    public static function desdeTexto(string $texto): self
    {
        $digitos = str_replace(['-', ' '], '', trim($texto));
        if (strlen($digitos) !== 11 || !ctype_digit($digitos)) {
            throw new InvalidArgumentException("El CUIT tiene 11 números: $texto");
        }
        $suma = 0;
        for ($i = 0; $i < 10; $i++) {
            $suma += (int) $digitos[$i] * self::PESOS[$i];
        }
        $verificador = match ($resto = 11 - $suma % 11) {
            11 => 0,
            10 => -1,
            default => $resto,
        };
        if ($verificador !== (int) $digitos[10]) {
            throw new InvalidArgumentException("El dígito verificador no coincide: $texto");
        }
        return new self($digitos);
    }

    public function tipo(): string
    {
        return in_array(substr($this->digitos, 0, 2), ['30', '33', '34'], true) ? 'empresa' : 'persona';
    }

    public function __toString(): string
    {
        return substr($this->digitos, 0, 2) . '-' . substr($this->digitos, 2, 8) . '-' . $this->digitos[10];
    }
}
```

`tests/CuitTest.php`
```php
<?php
declare(strict_types=1);

use Faro\Cuit;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;

final class CuitTest extends TestCase
{
    #[DataProvider('validos')]
    public function testFormateaLosValidos(string $texto, string $esperado): void
    {
        $this->assertSame($esperado, (string) Cuit::desdeTexto($texto));
    }

    public static function validos(): array
    {
        return [
            'con guiones' => ['20-12345678-6', '20-12345678-6'],
            'sin guiones' => ['20123456786', '20-12345678-6'],
            'con espacios' => [' 30 71234567 1 ', '30-71234567-1'],
        ];
    }

    #[DataProvider('invalidos')]
    public function testRechazaLosInvalidos(string $texto): void
    {
        $this->expectException(InvalidArgumentException::class);
        Cuit::desdeTexto($texto);
    }

    public static function invalidos(): array
    {
        return [
            'corto' => ['2012345678'],
            'con letras' => ['20-1234567A-6'],
            'verificador mal' => ['27-25123456-3'],
            'vacío' => [''],
        ];
    }

    public function testTipoPersonaYEmpresa(): void
    {
        $this->assertSame('persona', Cuit::desdeTexto('20-12345678-6')->tipo());
        $this->assertSame('empresa', Cuit::desdeTexto('30-71234567-1')->tipo());
    }
}
```

### Misión R05-N04-M2 · Las pruebas de las reservas

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Tomá el `ServicioReservas` de R04-N08-M2 (con su interfaz y el repositorio en
memoria) y escribí sus pruebas, **sin base de datos**:

- `setUp()` crea el servicio con un repositorio en memoria nuevo;
- reservar en un muelle libre funciona y queda guardado (`assertCount` sobre
  `delMuelle`);
- una reserva que se superpone lanza `DomainException` con el nombre del barco que
  ya estaba;
- dos reservas que se tocan en el borde (una termina el 7, la otra empieza el 7)
  **no** se superponen;
- más de 3 días, o la fecha de salida anterior a la de entrada, se rechazan
  (`DataProvider`);
- las reservas en muelles distintos no se afectan.

#### Criterio de aprobación

- Las pruebas usan el repositorio en memoria (no hay base).
- Cubren el caso normal, los errores y el caso borde.
- `vendor/bin/phpunit` termina en `OK`.

#### Solución de referencia

`composer.json`
```json
{
    "require-dev": { "phpunit/phpunit": "^11.5" },
    "autoload": { "psr-4": { "Faro\\": "src/" } }
}
```

`phpunit.xml`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit bootstrap="vendor/autoload.php" colors="false">
    <testsuites>
        <testsuite name="Reservas"><directory>tests</directory></testsuite>
    </testsuites>
</phpunit>
```

`src/Reserva.php`
```php
<?php
declare(strict_types=1);

namespace Faro;

use DateTimeImmutable;

readonly class Reserva
{
    public function __construct(public string $barco, public int $muelle, public DateTimeImmutable $desde, public DateTimeImmutable $hasta) {}

    public function seSuperponeCon(Reserva $otra): bool
    {
        return $this->desde < $otra->hasta && $otra->desde < $this->hasta;
    }
}
```

`src/ReservaRepositorio.php`
```php
<?php
declare(strict_types=1);

namespace Faro;

interface ReservaRepositorio
{
    /** @return Reserva[] */
    public function delMuelle(int $muelle): array;

    public function guardar(Reserva $r): void;
}
```

`src/ReservaRepositorioEnMemoria.php`
```php
<?php
declare(strict_types=1);

namespace Faro;

final class ReservaRepositorioEnMemoria implements ReservaRepositorio
{
    private array $reservas = [];

    public function delMuelle(int $muelle): array
    {
        return array_values(array_filter($this->reservas, fn(Reserva $r) => $r->muelle === $muelle));
    }

    public function guardar(Reserva $r): void
    {
        $this->reservas[] = $r;
    }
}
```

`src/ServicioReservas.php`
```php
<?php
declare(strict_types=1);

namespace Faro;

use DateTimeImmutable;
use DomainException;

final class ServicioReservas
{
    public const MAX_DIAS = 3;

    public function __construct(private ReservaRepositorio $repositorio) {}

    public function reservar(string $barco, int $muelle, string $desde, string $hasta): Reserva
    {
        $nueva = new Reserva($barco, $muelle, new DateTimeImmutable($desde), new DateTimeImmutable($hasta));
        $dias = $nueva->desde->diff($nueva->hasta)->days;
        if ($nueva->hasta <= $nueva->desde || $dias > self::MAX_DIAS) {
            throw new DomainException('Una reserva va de 1 a ' . self::MAX_DIAS . ' días');
        }
        foreach ($this->repositorio->delMuelle($muelle) as $existente) {
            if ($nueva->seSuperponeCon($existente)) {
                throw new DomainException("El muelle $muelle ya está reservado por {$existente->barco}");
            }
        }
        $this->repositorio->guardar($nueva);
        return $nueva;
    }
}
```

`tests/ServicioReservasTest.php`
```php
<?php
declare(strict_types=1);

use Faro\ReservaRepositorioEnMemoria;
use Faro\ServicioReservas;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;

final class ServicioReservasTest extends TestCase
{
    private ReservaRepositorioEnMemoria $repo;
    private ServicioReservas $servicio;

    protected function setUp(): void
    {
        $this->repo = new ReservaRepositorioEnMemoria();
        $this->servicio = new ServicioReservas($this->repo);
    }

    public function testReservaEnMuelleLibre(): void
    {
        $r = $this->servicio->reservar('Gaviota', 1, '2026-10-05', '2026-10-07');
        $this->assertSame('Gaviota', $r->barco);
        $this->assertCount(1, $this->repo->delMuelle(1));
    }

    public function testNoDejaSuperponer(): void
    {
        $this->servicio->reservar('Gaviota', 1, '2026-10-05', '2026-10-07');
        $this->expectException(DomainException::class);
        $this->expectExceptionMessage('Gaviota');
        $this->servicio->reservar('Albatros', 1, '2026-10-06', '2026-10-08');
    }

    public function testLasQueSeTocanEnElBordeNoSeSuperponen(): void
    {
        $this->servicio->reservar('Gaviota', 1, '2026-10-05', '2026-10-07');
        $this->servicio->reservar('Tortuga', 1, '2026-10-07', '2026-10-08');
        $this->assertCount(2, $this->repo->delMuelle(1));
    }

    #[DataProvider('periodosInvalidos')]
    public function testRechazaPeriodosInvalidos(string $desde, string $hasta): void
    {
        $this->expectException(DomainException::class);
        $this->servicio->reservar('Gaviota', 1, $desde, $hasta);
    }

    public static function periodosInvalidos(): array
    {
        return [
            'más de 3 días' => ['2026-10-01', '2026-10-06'],
            'al revés' => ['2026-10-06', '2026-10-01'],
            'el mismo día' => ['2026-10-06', '2026-10-06'],
        ];
    }

    public function testMuellesDistintosNoSeAfectan(): void
    {
        $this->servicio->reservar('Gaviota', 1, '2026-10-05', '2026-10-07');
        $this->servicio->reservar('Albatros', 2, '2026-10-05', '2026-10-07');
        $this->assertCount(1, $this->repo->delMuelle(1));
        $this->assertCount(1, $this->repo->delMuelle(2));
    }
}
```

### Misión R05-N04-M3 · Primero la prueba

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Hacelo al revés: **primero las pruebas**, después el código (se llama *desarrollo
guiado por pruebas*, TDD). La clase `Faro\Carrito` tiene que cumplir estas reglas, y
tus pruebas las tienen que describir antes de escribirla:

- `agregar(string $codigo, float $precio, int $cantidad = 1)`: si el producto ya
  está, suma la cantidad; cantidad o precio no positivos, `InvalidArgumentException`;
- `quitar(string $codigo)`;
- `cantidadTotal(): int` y `subtotal(): float`;
- `total(): float` con descuentos: 5% si hay 10 o más unidades, 10% si el subtotal
  supera $100000 (no se acumulan: se aplica el mayor);
- un carrito vacío tiene total 0.

Entregá las pruebas y la clase. Contá en un comentario al principio del archivo de
pruebas en qué orden las escribiste y cuál falló primero.

#### Criterio de aprobación

- Las pruebas cubren todas las reglas, incluido que los descuentos no se acumulan.
- `vendor/bin/phpunit` termina en `OK`.

#### Solución de referencia

`composer.json`
```json
{
    "require-dev": { "phpunit/phpunit": "^11.5" },
    "autoload": { "psr-4": { "Faro\\": "src/" } }
}
```

`phpunit.xml`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit bootstrap="vendor/autoload.php" colors="false">
    <testsuites>
        <testsuite name="Carrito"><directory>tests</directory></testsuite>
    </testsuites>
</phpunit>
```

`src/Carrito.php`
```php
<?php
declare(strict_types=1);

namespace Faro;

use InvalidArgumentException;

final class Carrito
{
    /** @var array<string, array{precio: float, cantidad: int}> */
    private array $items = [];

    public function agregar(string $codigo, float $precio, int $cantidad = 1): void
    {
        if ($precio <= 0 || $cantidad <= 0) {
            throw new InvalidArgumentException('Precio y cantidad tienen que ser positivos');
        }
        $this->items[$codigo] = ['precio' => $precio, 'cantidad' => ($this->items[$codigo]['cantidad'] ?? 0) + $cantidad];
    }

    public function quitar(string $codigo): void
    {
        unset($this->items[$codigo]);
    }

    public function cantidadTotal(): int
    {
        return array_sum(array_column($this->items, 'cantidad'));
    }

    public function subtotal(): float
    {
        return array_sum(array_map(fn(array $i) => $i['precio'] * $i['cantidad'], $this->items));
    }

    public function total(): float
    {
        $descuento = 0.0;
        if ($this->cantidadTotal() >= 10) {
            $descuento = 0.05;
        }
        if ($this->subtotal() > 100000) {
            $descuento = max($descuento, 0.10);
        }
        return round($this->subtotal() * (1 - $descuento), 2);
    }
}
```

`tests/CarritoTest.php`
```php
<?php
declare(strict_types=1);
// Orden en que se escribieron: vacío, agregar, sumar cantidades, quitar, inválidos,
// descuento por cantidad, descuento por monto, no se acumulan. La primera en fallar
// fue la del carrito vacío (la clase todavía no existía).

use Faro\Carrito;
use PHPUnit\Framework\TestCase;

final class CarritoTest extends TestCase
{
    public function testUnCarritoVacioTotalCero(): void
    {
        $c = new Carrito();
        $this->assertSame(0, $c->cantidadTotal());
        $this->assertSame(0.0, (float) $c->total());
    }

    public function testAgregarSumaCantidadesDelMismoProducto(): void
    {
        $c = new Carrito();
        $c->agregar('YER', 4200, 2);
        $c->agregar('YER', 4200);
        $this->assertSame(3, $c->cantidadTotal());
        $this->assertSame(12600.0, $c->subtotal());
    }

    public function testQuitar(): void
    {
        $c = new Carrito();
        $c->agregar('YER', 4200);
        $c->agregar('SAL', 900);
        $c->quitar('YER');
        $this->assertSame(900.0, $c->subtotal());
    }

    public function testRechazaCantidadesInvalidas(): void
    {
        $this->expectException(InvalidArgumentException::class);
        (new Carrito())->agregar('YER', 4200, 0);
    }

    public function testCincoPorCientoDesdeDiezUnidades(): void
    {
        $c = new Carrito();
        $c->agregar('SAL', 900, 10);
        $this->assertSame(8550.0, $c->total());
    }

    public function testDiezPorCientoDesdeCienMil(): void
    {
        $c = new Carrito();
        $c->agregar('PON', 120000);
        $this->assertSame(108000.0, $c->total());
    }

    public function testLosDescuentosNoSeAcumulan(): void
    {
        $c = new Carrito();
        $c->agregar('MAT', 12000, 10);
        $this->assertSame(108000.0, $c->total());      // 10% (el mayor), no 15%
    }
}
```

### Encargo R05-N04-E1 · Las pruebas de la liquidación de sueldos

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Un estudio contable liquida sueldos con reglas simplificadas y te pide una clase con
pruebas, porque "cada mes algo sale mal". `Faro\Liquidacion`:

- `new Liquidacion(float $basico, int $antiguedad, bool $presentismo)`;
- `antiguedad()`: 1% del básico por año;
- `presentismo()`: 8,33% de (básico + antigüedad) si corresponde;
- `bruto()`: básico + antigüedad + presentismo;
- `descuentos()`: 17% del bruto (jubilación 11%, obra social 3%, ley 19032 3%);
- `neto()`: bruto − descuentos, redondeado a 2 decimales.

Escribí las pruebas primero, con un `DataProvider` de **cinco casos reales**
calculados a mano (en un comentario, la cuenta de uno de ellos) que verifique el
neto, más pruebas de cada concepto por separado y de que el básico no puede ser
negativo.

#### Criterio de aprobación

- Un `DataProvider` con cinco casos y la cuenta de uno en un comentario.
- Pruebas por concepto y de los errores.
- `vendor/bin/phpunit` termina en `OK`.

#### Solución de referencia

`composer.json`
```json
{
    "require-dev": { "phpunit/phpunit": "^11.5" },
    "autoload": { "psr-4": { "Faro\\": "src/" } }
}
```

`phpunit.xml`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit bootstrap="vendor/autoload.php" colors="false">
    <testsuites>
        <testsuite name="Sueldos"><directory>tests</directory></testsuite>
    </testsuites>
</phpunit>
```

`src/Liquidacion.php`
```php
<?php
declare(strict_types=1);

namespace Faro;

use InvalidArgumentException;

final class Liquidacion
{
    public const POR_ANIO = 0.01;
    public const PRESENTISMO = 0.0833;
    public const DESCUENTOS = 0.17;

    public function __construct(private float $basico, private int $antiguedad, private bool $presentismo)
    {
        if ($basico < 0 || $antiguedad < 0) {
            throw new InvalidArgumentException('El básico y la antigüedad no pueden ser negativos');
        }
    }

    public function antiguedad(): float
    {
        return $this->basico * self::POR_ANIO * $this->antiguedad;
    }

    public function presentismo(): float
    {
        return $this->presentismo ? ($this->basico + $this->antiguedad()) * self::PRESENTISMO : 0.0;
    }

    public function bruto(): float
    {
        return $this->basico + $this->antiguedad() + $this->presentismo();
    }

    public function descuentos(): float
    {
        return $this->bruto() * self::DESCUENTOS;
    }

    public function neto(): float
    {
        return round($this->bruto() - $this->descuentos(), 2);
    }
}
```

`tests/LiquidacionTest.php`
```php
<?php
declare(strict_types=1);

use Faro\Liquidacion;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;

final class LiquidacionTest extends TestCase
{
    #[DataProvider('casos')]
    public function testNeto(float $basico, int $anios, bool $presentismo, float $neto): void
    {
        $this->assertEqualsWithDelta($neto, (new Liquidacion($basico, $anios, $presentismo))->neto(), 0.01);
    }

    public static function casos(): array
    {
        // Caso "con todo": básico 800000, 5 años → antigüedad 40000;
        // presentismo 8,33% de 840000 = 69972; bruto 909972;
        // descuentos 17% = 154695.24; neto 755276.76.
        return [
            'con todo' => [800000, 5, true, 755276.76],
            'sin presentismo' => [800000, 5, false, 697200.00],
            'recién ingresado' => [650000, 0, true, 584440.35],
            'veinte años' => [900000, 20, false, 896400.00],
            'básico cero' => [0, 3, true, 0.00],
        ];
    }

    public function testAntiguedadUnoPorCientoPorAnio(): void
    {
        $this->assertEqualsWithDelta(40000, (new Liquidacion(800000, 5, false))->antiguedad(), 0.001);
    }

    public function testPresentismoSobreBasicoMasAntiguedad(): void
    {
        $l = new Liquidacion(800000, 5, true);
        $this->assertEqualsWithDelta(69972, $l->presentismo(), 0.001);
        $this->assertSame(0.0, (new Liquidacion(800000, 5, false))->presentismo());
    }

    public function testDescuentosDelDiecisietePorCiento(): void
    {
        $this->assertEqualsWithDelta(154695.24, (new Liquidacion(800000, 5, true))->descuentos(), 0.001);
    }

    public function testNoAceptaBasicoNegativo(): void
    {
        $this->expectException(InvalidArgumentException::class);
        new Liquidacion(-1, 0, false);
    }
}
```

### Prueba del sello

#### ¿Por qué PHPUnit se instala con `--dev`?

Porque solo hace falta para desarrollar y probar; en el servidor de producción no se instala.

#### ¿Qué diferencia hay entre `assertSame` y `assertEquals`?

`assertSame` compara con `===` (mismo tipo y valor); `assertEquals` con `==` (convierte los tipos).

#### ¿Para qué sirve un `DataProvider`?

Para correr la misma prueba con muchos casos distintos (cada fila es una prueba con nombre).

#### ¿Cómo se prueba que un método lanza una excepción?

Con `$this->expectException(Clase::class)` antes de llamar al método (y, si se quiere, `expectExceptionMessage`).

#### ¿Por qué conviene probar la lógica con un repositorio en memoria?

Porque las pruebas quedan rápidas y repetibles, sin depender de una base de datos ni de sus datos.

### Soluciones (docente)

Sale de `21-PHP/20-Testing-PHPUnit`, con PHPUnit 11 (compatible con PHP 8.2 o más). Las misiones se corrigen con `composer install` y `vendor/bin/phpunit`: no tienen salida esperada, tienen que terminar en `OK`. En el encargo, los netos de los casos están calculados con las reglas de la consigna (la cuenta de "con todo" está en el comentario); conviene hacer uno a mano en clase.

## R05-N05 · Errores, logs y configuración

```meta
tipo: tema
padre: R05-N04
precio: 10
criatura: troll
temas: cal.logging, arch.config
usa: err.excepciones
```

### Crónica

Una madrugada, la lámpara del Faro se apagó. A la mañana nadie sabía por qué: no había ninguna nota, ningún registro, nada. El guardián nocturno solo recordaba "un ruido raro". Desde entonces hay un **libro de guardia**: cada cosa que pasa se anota con la hora, qué tan grave es y qué se hizo. Y en la puerta hay un cartel distinto para los visitantes: *"Faro momentáneamente fuera de servicio"*, sin detalles técnicos.

—En tu compu querés ver **todos** los errores, con el archivo y la línea —dice {mentor}—. En el servidor, los visitantes **nunca** tienen que verlos: se les muestra un mensaje amable y el detalle va al **registro**. Y lo que cambia entre tu compu y el servidor, {heroe}, no se escribe en el código: va en la **configuración**.

### Objetivos

- Configurar cómo muestra y registra PHP los errores en desarrollo y en producción.
- Convertir avisos en excepciones con `set_error_handler`.
- Atrapar todo lo que se escapa con `set_exception_handler` y mostrar una página de error amable.
- Escribir un registro (log) propio con niveles.
- Separar la configuración del código con un archivo `.env` por entorno.

### Antes de empezar

- Excepciones (R02-N09) y el MVC con punto de entrada único (R05-N01).

### Explicación

#### Mostrar o registrar
| Directiva | En tu compu (desarrollo) | En el servidor (producción) |
|---|---|---|
| `error_reporting` | `E_ALL` | `E_ALL` |
| `display_errors` | `On`: se ven en la página | **`Off`**: nunca al visitante |
| `log_errors` | `On` | `On` |
| `error_log` | un archivo o la terminal | un archivo fuera de `public/` |

Se configuran en `php.ini` o, al principio del programa:
```php
error_reporting(E_ALL);
ini_set('display_errors', $esDesarrollo ? '1' : '0');
ini_set('log_errors', '1');
ini_set('error_log', __DIR__ . '/../logs/php.log');
```
Mostrar errores en producción es peligroso: revelan rutas, consultas SQL, nombres de
tablas… información que usa quien ataca.

#### Los avisos, como excepciones
Un `Warning: Undefined array key` deja seguir al programa con datos malos. Muchos
proyectos (Laravel entre ellos) los convierten en excepciones, para que no pasen
desapercibidos:
```php
set_error_handler(function (int $nivel, string $mensaje, string $archivo, int $linea): bool {
    throw new ErrorException($mensaje, 0, $nivel, $archivo, $linea);
});
```

#### El último manotazo: `set_exception_handler`
Toda excepción que nadie atrapó termina en esta función. Es el lugar para registrar
el detalle y mostrar una página amable:
```php
set_exception_handler(function (Throwable $e) use ($logger, $esDesarrollo): void {
    $id = bin2hex(random_bytes(4));                       // un código para buscar en el log
    $logger->error("[$id] " . $e->getMessage(), ['archivo' => $e->getFile(), 'linea' => $e->getLine()]);
    http_response_code(500);
    echo $esDesarrollo ? "<pre>$e</pre>" : "Algo salió mal. Si escribís a soporte, pasales el código $id.";
});
```
Con `register_shutdown_function` y `error_get_last()` se atrapan hasta los errores
fatales (quedarse sin memoria), que no pasan por los manejadores.

#### Un registro con niveles
Además de los errores, conviene registrar lo que pasa: quién entró, qué pedido se
canceló, cuánto tardó una importación. Un registro con **niveles**:
| Nivel | Para |
|---|---|
| `debug` | detalles para desarrollar (se apagan en producción) |
| `info` | lo normal: "se registró un usuario" |
| `warning` | algo raro pero no grave: "intento de login fallido" |
| `error` | algo falló: "no se pudo mandar el mail" |

```
[2026-10-03 09:40:12] WARNING: Login fallido {"email":"kira@puerto.ar","ip":"10.0.0.5"}
```
Una línea por evento, con fecha, nivel, mensaje y datos en JSON: fácil de leer y de
buscar con `grep`. **Nunca** se registran contraseñas ni números de tarjeta.

#### Configuración por entorno: `.env`
Lo que cambia entre tu compu y el servidor (datos de la base, modo de depuración, la
dirección del sitio, claves de servicios) va en un archivo `.env` que **no** se sube
al repositorio:
```
APP_ENTORNO=produccion
APP_DEBUG=false
DB_DSN="mysql:host=localhost;dbname=puerto;charset=utf8mb4"
DB_USUARIO=puerto
DB_CLAVE="una-clave-larga"
```
Se lee con `parse_ini_file($ruta, false, INI_SCANNER_TYPED)` (convierte `true`,
`false` y los números) y se valida al arrancar: si falta algo obligatorio, mejor
fallar enseguida con un mensaje claro que a mitad de un pedido. En el repositorio se
sube un `.env.ejemplo` con las claves y sin los valores reales.

### Código de ejemplo

`.env`
```ini
APP_ENTORNO=produccion
APP_DEBUG=false
LOG_NIVEL=info
```

`src/Logger.php`
```php
<?php
declare(strict_types=1);

final class Logger
{
    private const NIVELES = ['debug' => 0, 'info' => 1, 'warning' => 2, 'error' => 3];

    public function __construct(private string $archivo, private string $minimo = 'debug', private ?Closure $reloj = null) {}

    public function log(string $nivel, string $mensaje, array $contexto = []): void
    {
        if (self::NIVELES[$nivel] < self::NIVELES[$this->minimo]) {
            return;
        }
        $cuando = $this->reloj ? ($this->reloj)() : date('Y-m-d H:i:s');
        $linea = "[$cuando] " . strtoupper($nivel) . ": $mensaje" . ($contexto === [] ? '' : ' ' . json_encode($contexto, JSON_UNESCAPED_UNICODE));
        file_put_contents($this->archivo, $linea . PHP_EOL, FILE_APPEND | LOCK_EX);
    }

    public function info(string $m, array $c = []): void { $this->log('info', $m, $c); }

    public function warning(string $m, array $c = []): void { $this->log('warning', $m, $c); }

    public function error(string $m, array $c = []): void { $this->log('error', $m, $c); }

    public function debug(string $m, array $c = []): void { $this->log('debug', $m, $c); }
}
```

`main.php`
```php
<?php
declare(strict_types=1);
/*
 * El libro de guardia: configuración por entorno, avisos como excepciones, un log y un manejador final.
 */
require __DIR__ . '/src/Logger.php';

$env = parse_ini_file(__DIR__ . '/.env', false, INI_SCANNER_TYPED);
foreach (['APP_ENTORNO', 'APP_DEBUG', 'LOG_NIVEL'] as $clave) {
    if (!array_key_exists($clave, $env)) {
        exit("Falta $clave en el .env\n");
    }
}
$debug = $env['APP_DEBUG'] === true;
$archivoLog = sys_get_temp_dir() . '/faro-guardia.log';
@unlink($archivoLog);
$logger = new Logger($archivoLog, $env['LOG_NIVEL'], fn() => '2026-10-03 03:10:00');

set_error_handler(function (int $nivel, string $mensaje, string $archivo, int $linea): bool {
    throw new ErrorException($mensaje, 0, $nivel, $archivo, $linea);
});
set_exception_handler(function (Throwable $e) use ($logger, $debug, $archivoLog): void {
    $logger->error('Excepción sin atrapar: ' . $e->getMessage(), ['tipo' => get_class($e), 'linea' => $e->getLine()]);
    echo $debug ? "DETALLE: $e\n" : "El Faro está momentáneamente fuera de servicio.\n";
    echo "--- libro de guardia ---\n", file_get_contents($archivoLog);
});

echo "Entorno: {$env['APP_ENTORNO']} (debug: ", $debug ? 'sí' : 'no', ")\n";
$logger->debug('Esto no se registra: el nivel mínimo es info');
$logger->info('Se encendió la lámpara', ['hora' => '19:00']);
$logger->warning('La lámpara titila', ['intensidad' => '72%']);

try {
    $lecturas = ['viento' => 18];
    $oleaje = $lecturas['oleaje'];                    // un aviso que ahora es una excepción
    echo "Oleaje: $oleaje\n";
} catch (ErrorException $e) {
    $logger->warning('Falta un sensor', ['detalle' => $e->getMessage()]);
    echo "Sensor de oleaje sin datos: se usa el último valor conocido.\n";
}

echo intdiv(10, 0);                                   // nadie lo atrapa: lo toma el manejador final
```

### Salida esperada

```
Entorno: produccion (debug: no)
Sensor de oleaje sin datos: se usa el último valor conocido.
El Faro está momentáneamente fuera de servicio.
--- libro de guardia ---
[2026-10-03 03:10:00] INFO: Se encendió la lámpara {"hora":"19:00"}
[2026-10-03 03:10:00] WARNING: La lámpara titila {"intensidad":"72%"}
[2026-10-03 03:10:00] WARNING: Falta un sensor {"detalle":"Undefined array key \"oleaje\""}
[2026-10-03 03:10:00] ERROR: Excepción sin atrapar: Division by zero {"tipo":"DivisionByZeroError","linea":42}
```

### ¿Para qué sirve?

Un sistema en producción sin registro es una caja negra: cuando algo falla, no hay cómo saber qué pasó. Con un buen log, el "no me anda" de un usuario se convierte en "el pedido 1042 falló a las 03:10 porque el proveedor de pagos no respondió". Laravel trae todo esto (`APP_DEBUG`, el archivo `.env`, `storage/logs/laravel.log`, `Log::warning(...)`), y es lo primero que se configura al subir un sistema.

### Errores habituales

**Troll: `display_errors` encendido en el servidor.** Cualquiera ve rutas, consultas y
datos internos. En producción, siempre apagado.

**Troll: el `.env` en el repositorio o en `public/`.** Si `.env` está en la carpeta
pública, cualquiera lo descarga con la contraseña de la base. Va fuera de `public/`
y en el `.gitignore`.

**Ogro: el `catch` que se traga todo.** `catch (Throwable $e) {}` sin registrar nada
es un error que pasó y nadie sabe. Registralo siempre.

**Troll: registrar contraseñas.** `$logger->info('Login', $_POST)` guarda la
contraseña en texto plano en el log. Elegí qué datos registrar.

**Goblin: el log que no se puede escribir.** Si la carpeta de logs no tiene permiso de
escritura, `file_put_contents` falla con un aviso. En el servidor, revisá los
permisos (lo ves en el nodo de hosting).

### Misión R05-N05-M1 · El registro del muelle

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Registro` que guarda eventos en memoria (un array) con nivel,
mensaje y contexto, y un nivel mínimo configurable. Métodos: `info`, `warning`,
`error`, `lineas(): array` (los textos formateados `[NIVEL] mensaje {json}`) y
`contar(): array` (`nivel => cantidad`). El contexto nunca tiene que incluir claves
llamadas `clave`, `password` o `tarjeta`: si vienen, se reemplazan por `***`.

Registrá los eventos del ejemplo con nivel mínimo `warning` y mostrá las líneas y el
conteo.

#### Criterio de aprobación

- Filtra por nivel mínimo.
- Oculta los datos sensibles del contexto.
- La salida coincide con la esperada.

#### Salida esperada

```
[WARNING] Login fallido {"usuario":"bron","clave":"***"}
[ERROR] No se pudo cobrar {"cliente":"Ana","tarjeta":"***","monto":12000}
[WARNING] Cajón sin etiqueta {"cajon":"C-17"}
Array
(
    [warning] => 2
    [error] => 1
)
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - El registro del muelle: niveles y datos sensibles ocultos.

final class Registro
{
    private const NIVELES = ['info' => 1, 'warning' => 2, 'error' => 3];
    private const SENSIBLES = ['clave', 'password', 'tarjeta'];
    private array $eventos = [];

    public function __construct(private string $minimo = 'info') {}

    private function log(string $nivel, string $mensaje, array $contexto): void
    {
        if (self::NIVELES[$nivel] < self::NIVELES[$this->minimo]) {
            return;
        }
        foreach (self::SENSIBLES as $clave) {
            if (array_key_exists($clave, $contexto)) {
                $contexto[$clave] = '***';
            }
        }
        $this->eventos[] = ['nivel' => $nivel, 'mensaje' => $mensaje, 'contexto' => $contexto];
    }

    public function info(string $m, array $c = []): void { $this->log('info', $m, $c); }

    public function warning(string $m, array $c = []): void { $this->log('warning', $m, $c); }

    public function error(string $m, array $c = []): void { $this->log('error', $m, $c); }

    public function lineas(): array
    {
        return array_map(fn(array $e) => '[' . strtoupper($e['nivel']) . "] {$e['mensaje']}" . ($e['contexto'] === [] ? '' : ' ' . json_encode($e['contexto'], JSON_UNESCAPED_UNICODE)), $this->eventos);
    }

    public function contar(): array
    {
        return array_count_values(array_column($this->eventos, 'nivel'));
    }
}

$registro = new Registro('warning');
$registro->info('Llegó la Gaviota', ['muelle' => 1]);
$registro->warning('Login fallido', ['usuario' => 'bron', 'clave' => 'faro2026']);
$registro->error('No se pudo cobrar', ['cliente' => 'Ana', 'tarjeta' => '4509 1234 5678 9012', 'monto' => 12000]);
$registro->warning('Cajón sin etiqueta', ['cajon' => 'C-17']);
foreach ($registro->lineas() as $linea) {
    echo $linea, "\n";
}
print_r($registro->contar());
```

### Misión R05-N05-M2 · La página de error amable

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá un sitio chico (`public/index.php`) que lea `APP_DEBUG` de un `.env` (fuera de
`public/`) y tenga:

- `set_error_handler` que convierte avisos en `ErrorException`;
- `set_exception_handler` que registra el error en `logs/errores.log` (con un código
  de 8 caracteres al azar) y responde **500** con una página amable que muestra el
  código; si `APP_DEBUG` es `true`, además muestra el mensaje y la línea;
- tres rutas por `?pagina=`: `inicio` (anda), `roto` (lee una clave que no existe de
  un array: se convierte en excepción) y `division` (divide por cero);
- `?pagina=log` muestra las últimas 5 líneas del log (solo si `APP_DEBUG` es `true`;
  si no, 404).

#### Criterio de aprobación

- Los errores responden 500 con un código y quedan en el log.
- Con `APP_DEBUG=false` no se muestra ningún detalle técnico.
- El `.env` y los logs están fuera de `public/`.

#### Solución de referencia

`.env`
```ini
APP_DEBUG=false
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Mision 2 - La página de error amable: log con código y detalles solo en desarrollo.
$env = parse_ini_file(__DIR__ . '/../.env', false, INI_SCANNER_TYPED);
$debug = ($env['APP_DEBUG'] ?? false) === true;
ini_set('display_errors', '0');
$log = __DIR__ . '/../logs/errores.log';
if (!is_dir(dirname($log))) {
    mkdir(dirname($log), 0775, true);
}

set_error_handler(function (int $nivel, string $mensaje, string $archivo, int $linea): bool {
    throw new ErrorException($mensaje, 0, $nivel, $archivo, $linea);
});
set_exception_handler(function (Throwable $e) use ($debug, $log): void {
    $codigo = bin2hex(random_bytes(4));
    file_put_contents($log, date('Y-m-d H:i:s') . " [$codigo] " . get_class($e) . ': ' . $e->getMessage() . " (línea {$e->getLine()})" . PHP_EOL, FILE_APPEND | LOCK_EX);
    http_response_code(500);
    echo '<h1>Algo salió mal</h1><p>Ya estamos avisados. Código: <code>' . $codigo . '</code></p>';
    if ($debug) {
        echo '<pre>' . htmlspecialchars(get_class($e) . ': ' . $e->getMessage() . ' en la línea ' . $e->getLine()) . '</pre>';
    }
});

switch ($_GET['pagina'] ?? 'inicio') {
    case 'inicio':
        echo '<h1>El Faro</h1><p>Todo en orden.</p>';
        break;
    case 'roto':
        $sensores = ['viento' => 18];
        echo 'Oleaje: ' . $sensores['oleaje'];
        break;
    case 'division':
        echo intdiv(10, 0);
        break;
    case 'log':
        if (!$debug) {
            http_response_code(404);
            exit('No existe esa página.');
        }
        $lineas = is_file($log) ? file($log, FILE_IGNORE_NEW_LINES) : [];
        echo '<pre>' . htmlspecialchars(implode("\n", array_slice($lineas, -5))) . '</pre>';
        break;
    default:
        http_response_code(404);
        echo 'No existe esa página.';
}
```

### Misión R05-N05-M3 · El cargador de configuración

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí la clase `Config` que carga la configuración de un **texto** con formato
`.env` (para probarla sin archivos, recibe el contenido como texto; usá
`parse_ini_string` con `INI_SCANNER_TYPED`) y:

- aplica valores **por defecto** para las claves que no vienen;
- valida las **obligatorias** (`DB_DSN`, `DB_USUARIO`) y lanza `RuntimeException` con
  **todas** las que faltan juntas;
- valida que `APP_ENTORNO` sea `local`, `pruebas` o `produccion`;
- `get(string $clave): mixed` (lanza si no existe) y `esProduccion(): bool`;
- en producción, fuerza `APP_DEBUG` a `false` aunque el archivo diga `true` (y avisa
  con un mensaje en `advertencias()`).

Probala con tres textos: uno completo de producción con `APP_DEBUG=true`, uno local
mínimo y uno al que le faltan las dos obligatorias.

#### Criterio de aprobación

- Junta todas las obligatorias que faltan en un solo error.
- Aplica los valores por defecto y la regla de producción.
- La salida coincide con la esperada.

#### Salida esperada

```
== producción
entorno: produccion · debug: false · zona: America/Argentina/Buenos_Aires
aviso: APP_DEBUG estaba en true en producción: se apagó
== local mínimo
entorno: local · debug: false · zona: America/Argentina/Buenos_Aires
== incompleto
error: Faltan en la configuración: DB_DSN, DB_USUARIO
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - El cargador de configuración: valores por defecto, obligatorias y reglas.

final class Config
{
    private const DEFECTOS = ['APP_ENTORNO' => 'local', 'APP_DEBUG' => false, 'APP_ZONA' => 'America/Argentina/Buenos_Aires'];
    private const OBLIGATORIAS = ['DB_DSN', 'DB_USUARIO'];
    private const ENTORNOS = ['local', 'pruebas', 'produccion'];

    private array $valores;
    private array $advertencias = [];

    public function __construct(string $contenido)
    {
        $leido = parse_ini_string($contenido, false, INI_SCANNER_TYPED);
        if ($leido === false) {
            throw new RuntimeException('El archivo de configuración tiene errores de formato');
        }
        $this->valores = $leido + self::DEFECTOS;
        $faltan = array_filter(self::OBLIGATORIAS, fn($c) => !array_key_exists($c, $this->valores));
        if ($faltan !== []) {
            throw new RuntimeException('Faltan en la configuración: ' . implode(', ', $faltan));
        }
        if (!in_array($this->valores['APP_ENTORNO'], self::ENTORNOS, true)) {
            throw new RuntimeException("APP_ENTORNO inválido: {$this->valores['APP_ENTORNO']}");
        }
        if ($this->esProduccion() && $this->valores['APP_DEBUG'] === true) {
            $this->valores['APP_DEBUG'] = false;
            $this->advertencias[] = 'APP_DEBUG estaba en true en producción: se apagó';
        }
    }

    public function get(string $clave): mixed
    {
        return array_key_exists($clave, $this->valores) ? $this->valores[$clave] : throw new RuntimeException("No existe la clave $clave");
    }

    public function esProduccion(): bool
    {
        return $this->valores['APP_ENTORNO'] === 'produccion';
    }

    public function advertencias(): array
    {
        return $this->advertencias;
    }
}

$textos = [
    'producción' => "APP_ENTORNO=produccion\nAPP_DEBUG=true\nDB_DSN=\"mysql:host=localhost;dbname=puerto\"\nDB_USUARIO=puerto\n",
    'local mínimo' => "DB_DSN=\"mysql:host=localhost;dbname=puerto\"\nDB_USUARIO=root\n",
    'incompleto' => "APP_ENTORNO=local\n",
];
foreach ($textos as $nombre => $texto) {
    echo "== $nombre\n";
    try {
        $c = new Config($texto);
        echo "entorno: ", $c->get('APP_ENTORNO'), " · debug: ", var_export($c->get('APP_DEBUG'), true), " · zona: ", $c->get('APP_ZONA'), "\n";
        foreach ($c->advertencias() as $a) {
            echo "aviso: $a\n";
        }
    } catch (RuntimeException $e) {
        echo "error: ", $e->getMessage(), "\n";
    }
}
```

### Encargo R05-N05-E1 · El monitor de la tienda

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una tienda online guarda su registro en formato de una línea por evento:
`[FECHA HORA] NIVEL: mensaje {json}`. El dueño quiere un **resumen diario** para
revisar a la mañana. Escribí un programa que lea el registro de la entrada estándar
(con un generador, como en R05-N02) y muestre:

- la cantidad de eventos por nivel;
- los errores, con la hora y el mensaje;
- las IP con 3 o más `Login fallido` (posible ataque), a partir del JSON del contexto;
- el pedido más caro confirmado (`Pedido confirmado` con `total` en el JSON).

Los renglones que no respetan el formato se cuentan aparte como `ilegibles`.

#### Criterio de aprobación

- Lee con un generador y decodifica el JSON del contexto.
- Detecta las IP sospechosas y el pedido más caro.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
[2026-10-03 08:00:01] INFO: Pedido confirmado {"pedido":1041,"total":18500}
[2026-10-03 08:05:12] WARNING: Login fallido {"email":"ana@x.com","ip":"10.0.0.7"}
[2026-10-03 08:05:20] WARNING: Login fallido {"email":"ana@x.com","ip":"10.0.0.7"}
[2026-10-03 08:05:31] WARNING: Login fallido {"email":"root@x.com","ip":"10.0.0.7"}
[2026-10-03 09:12:45] ERROR: No se pudo mandar el mail {"pedido":1041}
[2026-10-03 10:30:00] INFO: Pedido confirmado {"pedido":1042,"total":96400}
esto no es un renglón válido
[2026-10-03 11:02:10] WARNING: Login fallido {"email":"beto@x.com","ip":"10.0.0.9"}
[2026-10-03 12:40:33] ERROR: El proveedor de pagos no respondió {"pedido":1043}
[2026-10-03 13:00:00] INFO: Pedido confirmado {"pedido":1044,"total":7200}
```

#### Salida esperada

```
Eventos: ERROR 2, INFO 3, WARNING 4 · ilegibles 1
Errores:
  09:12:45 No se pudo mandar el mail
  12:40:33 El proveedor de pagos no respondió
IP sospechosas: 10.0.0.7 (3 intentos)
Pedido más caro: 1042 por $96.400,00
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - El monitor de la tienda: leer un log con un generador y resumirlo.

function eventos($flujo, int &$ilegibles): Generator
{
    while (($linea = fgets($flujo)) !== false) {
        if (!preg_match('/^\[(\S+) (\S+)\] (\w+): (.*?)(?: (\{.*\}))?$/', trim($linea), $m)) {
            $ilegibles++;
            continue;
        }
        yield ['hora' => $m[2], 'nivel' => $m[3], 'mensaje' => $m[4], 'contexto' => isset($m[5]) ? (json_decode($m[5], true) ?? []) : []];
    }
}

$ilegibles = 0;
$porNivel = [];
$errores = [];
$fallidosPorIp = [];
$masCaro = null;
foreach (eventos(STDIN, $ilegibles) as $e) {
    $porNivel[$e['nivel']] = ($porNivel[$e['nivel']] ?? 0) + 1;
    if ($e['nivel'] === 'ERROR') {
        $errores[] = "{$e['hora']} {$e['mensaje']}";
    }
    if ($e['mensaje'] === 'Login fallido' && isset($e['contexto']['ip'])) {
        $fallidosPorIp[$e['contexto']['ip']] = ($fallidosPorIp[$e['contexto']['ip']] ?? 0) + 1;
    }
    if ($e['mensaje'] === 'Pedido confirmado' && ($masCaro === null || $e['contexto']['total'] > $masCaro['total'])) {
        $masCaro = $e['contexto'];
    }
}

ksort($porNivel);
echo "Eventos: ", implode(', ', array_map(fn($n, $c) => "$n $c", array_keys($porNivel), $porNivel)), " · ilegibles $ilegibles\n";
echo "Errores:\n";
foreach ($errores as $error) {
    echo "  $error\n";
}
$sospechosas = array_filter($fallidosPorIp, fn($n) => $n >= 3);
echo "IP sospechosas: ", $sospechosas === [] ? 'ninguna' : implode(', ', array_map(fn($ip, $n) => "$ip ($n intentos)", array_keys($sospechosas), $sospechosas)), "\n";
echo "Pedido más caro: {$masCaro['pedido']} por $", number_format($masCaro['total'], 2, ',', '.'), "\n";
```

#### Pruebas

##### Sin errores ni sospechosos
```entrada
[2026-10-03 08:00:01] INFO: Arranca el día {}
[2026-10-03 08:10:00] INFO: Pedido confirmado {"pedido":7,"total":1500.5}
```
```salida
Eventos: INFO 2 · ilegibles 0
Errores:
IP sospechosas: ninguna
Pedido más caro: 7 por $1.500,50
```

##### Casi todo ilegible
```entrada
basura
[sin cierre INFO: x {}
[2026-10-03 08:10:00] INFO: Pedido confirmado {"pedido":8,"total":100}
```
```salida
Eventos: INFO 1 · ilegibles 2
Errores:
IP sospechosas: ninguna
Pedido más caro: 8 por $100,00
```

##### Dos IP con dos intentos
```entrada
[2026-10-03 08:00:01] WARNING: Login fallido {"email":"a@x.com","ip":"1.1.1.1"}
[2026-10-03 08:00:02] WARNING: Login fallido {"email":"a@x.com","ip":"1.1.1.1"}
[2026-10-03 08:00:03] WARNING: Login fallido {"email":"b@x.com","ip":"2.2.2.2"}
[2026-10-03 08:00:04] WARNING: Login fallido {"email":"b@x.com","ip":"2.2.2.2"}
[2026-10-03 09:00:00] INFO: Pedido confirmado {"pedido":9,"total":20000}
[2026-10-03 09:30:00] INFO: Pedido confirmado {"pedido":10,"total":19999}
```
```salida
Eventos: INFO 2, WARNING 4 · ilegibles 0
Errores:
IP sospechosas: ninguna
Pedido más caro: 9 por $20.000,00
```

### Prueba del sello

#### ¿Por qué se apaga `display_errors` en producción?

Porque los mensajes de error revelan rutas, consultas y datos internos que le sirven a quien ataca; en producción los errores se registran, no se muestran.

#### ¿Para qué sirve `set_exception_handler`?

Para atrapar toda excepción que nadie atrapó: registrarla y mostrar una página de error amable.

#### ¿Qué ventaja tiene convertir los avisos en excepciones?

Que un aviso (como una clave que no existe) no deja seguir al programa con datos malos: se lo trata como un error.

#### ¿Qué va en el archivo `.env` y por qué no se sube al repositorio?

Lo que cambia entre entornos: datos de la base, modo de depuración, claves. No se sube porque tiene contraseñas; se sube un `.env.ejemplo` sin los valores reales.

#### ¿Qué datos no se registran nunca en un log?

Contraseñas, números de tarjeta y cualquier dato sensible.

### Soluciones (docente)

Nodo nuevo. En el ejemplo, el reloj del `Logger` es una closure fija para que la salida sea repetible (en un sistema real es `date()`). En la misión 2, el log queda en `logs/errores.log` fuera de `public/`; en XAMPP hay que verificar que PHP pueda escribir ahí.

## R05-N06 · Subir a un hosting

```meta
tipo: tema
padre: R05-N05
precio: 10
criatura: slime
temas: web.despliegue
```

### Crónica

Hasta hoy, tu Faro solo alumbraba adentro de tu compu. Para que lo vean los barcos de verdad hay que llevarlo a la costa: un lugar que esté prendido día y noche, con una dirección que todos conozcan. {mentor} te entrega un papel con tres cosas escritas: *un dominio, un hosting, una base de datos*.

—Subir un sistema es mudarse —dice—. Hay que llevar los archivos correctos (y dejar los que no van), preparar la base, cambiar la configuración, poner el candado del HTTPS y revisar que todo ande. Si lo hacés con una lista, {heroe}, la mudanza sale bien. Si lo hacés de memoria, siempre se olvida algo.

### Objetivos

- Conocer las piezas: dominio, hosting compartido, cPanel, base de datos y HTTPS.
- Preparar un proyecto para producción: `public/` como raíz, `.env` de producción, dependencias sin `--dev`.
- Subir los archivos por FTP/SFTP, por el administrador de archivos o con Git.
- Crear la base de datos y el usuario en cPanel e importar el esquema.
- Configurar `.htaccess` para el controlador frontal y proteger lo privado.
- Revisar el sitio después de subirlo con un script de diagnóstico.

### Antes de empezar

- Errores y configuración por entorno (R05-N05), el MVC con punto de entrada único (R05-N01) y MariaDB (rama 4).

### Explicación

#### Las piezas
| Pieza | Qué es | Ejemplo |
|---|---|---|
| **Dominio** | el nombre del sitio | `faro.com.ar` (en Argentina, en nic.ar) |
| **Hosting** | una computadora siempre prendida que sirve tu sitio | un plan compartido con PHP y MySQL/MariaDB |
| **cPanel** | el panel web para administrar el hosting | archivos, bases, correos, dominios |
| **Base de datos** | MariaDB/MySQL del hosting | se crea desde cPanel |
| **HTTPS** | el candado: la conexión cifrada | un certificado gratuito (Let's Encrypt / AutoSSL) |

La mayoría de los hostings compartidos de la región usan **cPanel** con **Apache**,
PHP (se elige la versión en *Select PHP Version* o *MultiPHP Manager*) y MariaDB.

#### Preparar el proyecto
- **La raíz pública** tiene que ser `public/`. En cPanel, al agregar un dominio o
  subdominio se elige su carpeta (*Document Root*): apuntala a
  `…/mi-proyecto/public`. Si el hosting no deja elegirla (el dominio principal usa
  `public_html`), se sube el proyecto **fuera** de `public_html` y se copia el
  contenido de `public/` adentro, ajustando las rutas del `index.php`.
- **Dependencias**: en el servidor, `composer install --no-dev --optimize-autoloader`
  (sin PHPUnit). Si el hosting no tiene Composer ni SSH, se corre en tu compu y se
  sube la carpeta `vendor/`.
- **`.env` de producción**: `APP_DEBUG=false`, los datos de la base del hosting, la
  dirección real. Se crea en el servidor (no viaja con el código).
- **Nada de sobra**: no se suben `tests/`, `.git/`, archivos de prueba ni copias
  (`index.php.bak`): lo que está en la raíz pública se puede descargar.

#### Subir los archivos
- **Administrador de archivos** de cPanel: subís un `.zip` y lo descomprimís ahí.
- **FTP/SFTP** con un programa como FileZilla (SFTP es el cifrado: preferilo).
- **Git**: si el hosting tiene SSH, `git clone` y después `git pull` en cada cambio
  (cPanel también tiene *Git Version Control*).

#### La base de datos en cPanel
1. *MySQL Databases*: crear la base (cPanel le agrega un prefijo:
   `usuario_puerto`).
2. Crear un **usuario** con una contraseña larga y agregarlo a la base con
   **todos los privilegios** de esa base.
3. *phpMyAdmin*: elegir la base, pestaña **Importar**, subir el `esquema.sql`.
4. Poner esos datos en el `.env` del servidor (`DB_DSN` con el nombre con prefijo,
   `DB_USUARIO`, `DB_CLAVE`). El host casi siempre es `localhost`.

#### `.htaccess`: el controlador frontal en Apache
Con `php -S` se pasaba el router; en Apache, un `.htaccess` en `public/` manda todo
lo que no sea un archivo existente a `index.php`:
```apache
# public/.htaccess
Options -Indexes
RewriteEngine On
RewriteCond %{HTTP:Authorization} .
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^ index.php [L]
```
- `Options -Indexes` evita que se listen los archivos de una carpeta sin
  `index.php`.
- Las dos líneas de `Authorization` hacen llegar ese encabezado a PHP (para las
  APIs con token).
- Si por alguna razón una carpeta privada queda dentro de la raíz pública, un
  `.htaccess` con `Require all denied` la bloquea.

#### HTTPS
En cPanel, *SSL/TLS Status* o *AutoSSL* emite un certificado gratuito. Después se
fuerza HTTPS agregando al `.htaccess`:
```apache
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```
y las cookies de sesión se marcan como seguras (`session.cookie_secure = 1`).

#### Revisar después de subir
Un **script de diagnóstico** revisa en un minuto lo que suele fallar: la versión de
PHP, las extensiones (`pdo_mysql`, `mbstring`), que se pueda escribir en las
carpetas de logs y subidas, que la base conecte y que `APP_DEBUG` esté apagado. Se
usa y **se borra** (o se protege), porque da información del servidor.

#### La lista de la mudanza
1. `composer install --no-dev` (o subir `vendor/`).
2. Subir los archivos (sin `tests/`, `.git`, `.env` de tu compu).
3. Raíz del dominio → `public/`.
4. Crear la base y el usuario; importar el esquema.
5. Crear el `.env` de producción (`APP_DEBUG=false`).
6. Permisos de escritura en `logs/` y en la carpeta de subidas.
7. HTTPS con AutoSSL y la redirección en `.htaccess`.
8. Correr el diagnóstico, probar el sitio de punta a punta, borrar el diagnóstico.

### Código de ejemplo

`public/diagnostico.php`
```php
<?php
declare(strict_types=1);
/*
 * El diagnóstico de la mudanza: revisa el servidor después de subir el sitio.
 * Se usa una vez y se borra (da información del servidor).
 */
header('Content-Type: text/plain; charset=utf-8');

$chequeos = [];
$chequeos['PHP 8.2 o más'] = version_compare(PHP_VERSION, '8.2.0', '>=');
foreach (['pdo_mysql', 'mbstring', 'fileinfo', 'json'] as $extension) {
    $chequeos["extensión $extension"] = extension_loaded($extension);
}
$chequeos['display_errors apagado'] = !filter_var(ini_get('display_errors'), FILTER_VALIDATE_BOOLEAN);
$chequeos['zona horaria configurada'] = date_default_timezone_get() !== 'UTC';

$raiz = dirname(__DIR__);
foreach (['logs', 'subidas'] as $carpeta) {
    if (!is_dir("$raiz/$carpeta")) {
        @mkdir("$raiz/$carpeta", 0775, true);
    }
    $chequeos["se puede escribir en $carpeta/"] = is_writable("$raiz/$carpeta");
}
$chequeos['el .env no está en public/'] = !is_file(__DIR__ . '/.env');

$env = is_file("$raiz/.env") ? parse_ini_file("$raiz/.env", false, INI_SCANNER_TYPED) : [];
$chequeos['APP_DEBUG en false'] = ($env['APP_DEBUG'] ?? null) === false;

$ok = 0;
foreach ($chequeos as $nombre => $resultado) {
    echo $resultado ? '[ OK ] ' : '[FALLA] ', $nombre, "\n";
    $ok += (int) $resultado;
}
echo "\n$ok de ", count($chequeos), " chequeos bien.\n";
```

`.env`
```ini
APP_DEBUG=false
```

### ¿Para qué sirve?

Un sistema que solo corre en tu compu no le sirve a nadie. Saber subirlo a un hosting compartido (el lugar más barato y común en la región para sitios chicos y medianos) es lo que te permite entregar un trabajo a un cliente, publicar tu portfolio o poner en marcha el sistema de un comercio. Esta misma plataforma vive en un hosting con cPanel.

### Errores habituales

**Slime: todo da 404 menos la portada.** Falta el `.htaccess` con las reglas de
reescritura (o el hosting no tiene `mod_rewrite`).

**Troll: la raíz en la carpeta del proyecto.** Si el dominio apunta a la carpeta del
proyecto y no a `public/`, cualquiera descarga `.env` o `config.php` desde el
navegador.

**Esqueleto: `Access denied for user` en el servidor.** Los datos de la base del hosting
no son los de tu compu: el nombre de la base y del usuario llevan el prefijo de la
cuenta, y el usuario tiene que estar agregado a la base con privilegios.

**Goblin: `could not find driver` o funciones que no existen.** El hosting usa otra
versión de PHP o le falta una extensión: elegí la versión en cPanel y activá
`pdo_mysql` y `mbstring`.

**Slime: los permisos.** Si PHP no puede escribir en `logs/` o `subidas/`, fallan los
logs y las subidas. Las carpetas van con permiso `755` (o `775`), los archivos con
`644`; nunca `777`.

### Misión R05-N06-M1 · El diagnóstico a medida

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Extendé el diagnóstico del ejemplo para tu propio sistema:

- que lea el `.env` y pruebe la **conexión a la base** con esos datos (atrapando la
  excepción: si falla, muestra `[FALLA] conexión a la base: MOTIVO` sin la
  contraseña);
- que verifique que existan las **tablas** que tu sistema necesita (una lista en el
  código), con `SHOW TABLES`;
- que revise el **tamaño máximo de subida** (`upload_max_filesize`) y avise si es
  menor que 2 MB (convertí `2M`, `512K` a bytes con una función);
- que solo se pueda usar con un parámetro secreto `?clave=…` que también está en el
  `.env` (`DIAGNOSTICO_CLAVE`); sin ella, responde 404.

#### Criterio de aprobación

- Prueba la conexión y las tablas con los datos del `.env`.
- Convierte los tamaños de PHP a bytes.
- Está protegido por una clave del `.env`.

#### Solución de referencia

`.env`
```ini
APP_DEBUG=false
DB_DSN="mysql:host=localhost;dbname=puerto;charset=utf8mb4"
DB_USUARIO=root
DB_CLAVE=""
DIAGNOSTICO_CLAVE=faro-2026
```

`esquema.sql`
```sql
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(40) NOT NULL);
CREATE TABLE pedido (id INT AUTO_INCREMENT PRIMARY KEY, cliente VARCHAR(40) NOT NULL);
```

`public/diagnostico.php`
```php
<?php
declare(strict_types=1);
// Mision 1 - El diagnóstico a medida: base, tablas, tamaños y una clave.
$raiz = dirname(__DIR__);
$env = parse_ini_file("$raiz/.env", false, INI_SCANNER_TYPED) ?: [];
if (!isset($env['DIAGNOSTICO_CLAVE']) || !hash_equals((string) $env['DIAGNOSTICO_CLAVE'], $_GET['clave'] ?? '')) {
    http_response_code(404);
    exit('No existe esa página.');
}
header('Content-Type: text/plain; charset=utf-8');
const TABLAS = ['producto', 'pedido'];

function aBytes(string $valor): int
{
    $valor = trim($valor);
    $numero = (int) $valor;
    return match (strtoupper(substr($valor, -1))) {
        'G' => $numero * 1024 ** 3,
        'M' => $numero * 1024 ** 2,
        'K' => $numero * 1024,
        default => $numero,
    };
}

function linea(bool $ok, string $texto): void
{
    echo $ok ? '[ OK ] ' : '[FALLA] ', $texto, "\n";
}

linea(version_compare(PHP_VERSION, '8.2.0', '>='), 'PHP ' . PHP_MAJOR_VERSION . '.' . PHP_MINOR_VERSION);
linea(aBytes((string) ini_get('upload_max_filesize')) >= 2 * 1024 ** 2, 'subidas de hasta ' . ini_get('upload_max_filesize'));
try {
    $pdo = new PDO((string) $env['DB_DSN'], (string) $env['DB_USUARIO'], (string) ($env['DB_CLAVE'] ?? ''), [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
    linea(true, 'conexión a la base');
    $existentes = $pdo->query('SHOW TABLES')->fetchAll(PDO::FETCH_COLUMN);
    foreach (TABLAS as $tabla) {
        linea(in_array($tabla, $existentes, true), "tabla $tabla");
    }
} catch (PDOException $e) {
    linea(false, 'conexión a la base: ' . preg_replace('/\(using password: \w+\)/', '', $e->getMessage()));
}
```

### Misión R05-N06-M2 · La mudanza del sistema

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Prepará para producción uno de tus proyectos anteriores con base de datos (por
ejemplo, el ABM de R04-N06 o la agenda de R05-N01-E1). Entregá un `.zip` con:

- el proyecto con la estructura `public/`, `src/`, `vistas/`;
- `public/.htaccess` con el controlador frontal, `Options -Indexes`, la redirección a
  HTTPS y el pase del encabezado `Authorization`;
- `.env.ejemplo` con todas las claves y valores de ejemplo (y el código leyendo la
  configuración del `.env`, no de un `config.php` con datos reales);
- `esquema.sql` listo para importar en phpMyAdmin (sin `CREATE DATABASE` ni `USE`,
  porque la base la crea cPanel con prefijo);
- `MUDANZA.md`: la lista de pasos de la mudanza **para ese proyecto** (qué carpeta
  va de raíz, qué permisos, qué datos van en el `.env`, cómo se prueba).

Si tenés acceso a un hosting (o a uno gratuito de prueba), subilo y agregá la
dirección en `MUDANZA.md`.

#### Criterio de aprobación

- La raíz pública es `public/` y el `.htaccess` está completo.
- La configuración sale del `.env` y hay un `.env.ejemplo` sin datos reales.
- `MUDANZA.md` tiene la lista completa para ese proyecto.

#### Solución de referencia

`public/.htaccess`
```apache
Options -Indexes
RewriteEngine On

# Forzar HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Pasar el encabezado Authorization a PHP (APIs con token)
RewriteCond %{HTTP:Authorization} .
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

# Todo lo que no sea un archivo o carpeta real va al controlador frontal
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^ index.php [L]
```

`.env.ejemplo`
```ini
APP_ENTORNO=produccion
APP_DEBUG=false
APP_URL=https://turnos.ejemplo.com.ar
DB_DSN="mysql:host=localhost;dbname=cuenta_turnos;charset=utf8mb4"
DB_USUARIO=cuenta_turnos
DB_CLAVE="cambiar-por-una-clave-larga"
```

`src/config.php`
```php
<?php
declare(strict_types=1);
// Lee la configuración del .env (fuera de public/) y la valida al arrancar.

function configuracion(): array
{
    static $config = null;
    if ($config === null) {
        $ruta = __DIR__ . '/../.env';
        $config = is_file($ruta) ? parse_ini_file($ruta, false, INI_SCANNER_TYPED) : false;
        if ($config === false) {
            http_response_code(500);
            exit('Falta el archivo .env (copiá .env.ejemplo y completalo).');
        }
        foreach (['DB_DSN', 'DB_USUARIO', 'DB_CLAVE'] as $clave) {
            if (!array_key_exists($clave, $config)) {
                http_response_code(500);
                exit("Falta $clave en el .env.");
            }
        }
        ini_set('display_errors', ($config['APP_DEBUG'] ?? false) === true ? '1' : '0');
    }
    return $config;
}
```

`MUDANZA.md`
```md
# Mudanza de la agenda de turnos

1. En la compu: `composer install --no-dev` (este proyecto no tiene dependencias).
2. Subir por el Administrador de archivos un .zip con `public/`, `src/`, `vistas/` y `esquema.sql`
   a `/home/cuenta/turnos/` (fuera de public_html). No subir `.env` ni `tests/`.
3. En cPanel → Dominios: el subdominio `turnos` con Document Root `/home/cuenta/turnos/public`.
4. MySQL Databases: crear `cuenta_turnos` y el usuario `cuenta_turnos` con todos los privilegios.
5. phpMyAdmin → `cuenta_turnos` → Importar `esquema.sql`.
6. Copiar `.env.ejemplo` a `.env` en `/home/cuenta/turnos/` y completar la clave de la base.
7. Permisos: carpetas 755, archivos 644; `logs/` con escritura para PHP.
8. SSL/TLS Status → AutoSSL para `turnos.ejemplo.com.ar`.
9. Probar: la agenda, un turno nuevo, un turno repetido (tiene que avisar), cancelar.
10. Borrar el diagnóstico si se usó.
```

### Misión R05-N06-M3 · El respaldo de la base

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

En un hosting compartido a veces no hay `mysqldump` ni acceso por consola. Escribí
`respaldo.php`, que genera un **respaldo en SQL** de las tablas que se le indiquen
usando solo PDO:

- para cada tabla, `SHOW CREATE TABLE` da la instrucción para recrearla;
- los datos se exportan como `INSERT INTO tabla (cols) VALUES (…), (…);` usando
  `$pdo->quote()` para cada valor (y `NULL` sin comillas);
- el archivo empieza con `SET FOREIGN_KEY_CHECKS = 0;` y termina con `= 1;`, para
  poder importar en cualquier orden;
- se lee con un generador (una fila por vez).

Mostrá el respaldo por pantalla con las tablas del ejemplo y, para comprobar que
sirve, **restauralo** en otra tabla temporal y compará las cantidades de filas.

#### Criterio de aprobación

- Genera `CREATE TABLE` e `INSERT` con los valores escapados con `quote()`.
- El respaldo se puede volver a importar.
- La salida coincide con la esperada.

#### Salida esperada

```
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `producto`;
CREATE TABLE `producto` (
  `codigo` char(5) NOT NULL,
  `nombre` varchar(60) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `vence` date DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
INSERT INTO `producto` (`codigo`, `nombre`, `precio`, `vence`) VALUES
  ('SAL01', 'Sal O\'Brien', '900.00', NULL),
  ('YER01', 'Yerba \"La Riojana\"', '4200.00', '2027-06-30');
DROP TABLE IF EXISTS `renglon`;
CREATE TABLE `renglon` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` char(5) NOT NULL,
  `cantidad` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `codigo` (`codigo`),
  CONSTRAINT `renglon_ibfk_1` FOREIGN KEY (`codigo`) REFERENCES `producto` (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
INSERT INTO `renglon` (`id`, `codigo`, `cantidad`) VALUES
  ('1', 'YER01', '3'),
  ('2', 'SAL01', '10'),
  ('3', 'YER01', '1');
SET FOREIGN_KEY_CHECKS = 1;
-- Restaurado: productos 2/2, renglones 3/3
-- Nombre con comillas: Sal O'Brien
```

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS renglon;
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (codigo CHAR(5) PRIMARY KEY, nombre VARCHAR(60) NOT NULL, precio DECIMAL(10, 2) NOT NULL, vence DATE NULL);
CREATE TABLE renglon (id INT AUTO_INCREMENT PRIMARY KEY, codigo CHAR(5) NOT NULL, cantidad INT NOT NULL, FOREIGN KEY (codigo) REFERENCES producto(codigo));
INSERT INTO producto VALUES ('YER01', 'Yerba "La Riojana"', 4200, '2027-06-30'), ('SAL01', 'Sal O\'Brien', 900, NULL);
INSERT INTO renglon (codigo, cantidad) VALUES ('YER01', 3), ('SAL01', 10), ('YER01', 1);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`respaldo.php`
```php
<?php
declare(strict_types=1);
// Mision 3 - El respaldo de la base: CREATE TABLE e INSERT con PDO, y la prueba de restaurarlo.
$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);

function respaldo(PDO $pdo, array $tablas): Generator
{
    yield "SET FOREIGN_KEY_CHECKS = 0;";
    foreach ($tablas as $tabla) {
        $crear = $pdo->query("SHOW CREATE TABLE `$tabla`")->fetch();
        yield "DROP TABLE IF EXISTS `$tabla`;";
        yield $crear['Create Table'] . ';';
        $filas = $pdo->query("SELECT * FROM `$tabla`");
        $valores = [];
        $columnas = null;
        while ($fila = $filas->fetch()) {
            $columnas ??= '(`' . implode('`, `', array_keys($fila)) . '`)';
            $valores[] = '(' . implode(', ', array_map(fn($v) => $v === null ? 'NULL' : $pdo->quote((string) $v), $fila)) . ')';
        }
        if ($valores !== []) {
            yield "INSERT INTO `$tabla` $columnas VALUES\n  " . implode(",\n  ", $valores) . ';';
        }
    }
    yield "SET FOREIGN_KEY_CHECKS = 1;";
}

$sql = '';
foreach (respaldo($pdo, ['producto', 'renglon']) as $instruccion) {
    echo $instruccion, "\n";
    $sql .= $instruccion . "\n";
}

// Prueba: contar, borrar todo, restaurar y volver a contar
$contar = fn() => $pdo->query('SELECT (SELECT COUNT(*) FROM producto) AS productos, (SELECT COUNT(*) FROM renglon) AS renglones')->fetch();
$antes = $contar();
$pdo->exec('SET FOREIGN_KEY_CHECKS = 0; DROP TABLE renglon; DROP TABLE producto; SET FOREIGN_KEY_CHECKS = 1;');
$pdo->exec($sql);
$despues = $contar();
echo "-- Restaurado: productos {$despues['productos']}/{$antes['productos']}, renglones {$despues['renglones']}/{$antes['renglones']}\n";
echo "-- Nombre con comillas: ", $pdo->query("SELECT nombre FROM producto WHERE codigo = 'SAL01'")->fetchColumn(), "\n";
```

### Encargo R05-N06-E1 · El sitio del comercio del barrio

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Una verdulería del barrio quiere un sitio sencillo: portada, lista de precios del día
(desde MariaDB) y un formulario de pedidos para retirar. Hacelo **listo para subir**:

- estructura `public/` (con su `.htaccess`), `src/`, `vistas/`, `logs/`;
- configuración desde `.env` (y un `.env.ejemplo`);
- manejador de errores que registra en `logs/` y muestra una página amable;
- la lista de precios con la fecha de actualización y los pedidos guardados en la
  base con CSRF y validación;
- un `LEEME.md` para el dueño (no técnico): cómo actualizar los precios desde
  phpMyAdmin y dónde ver los pedidos;
- el `MUDANZA.md` con los pasos para subirlo.

Probalo en tu compu con `php -S … public/index.php` y, si podés, subilo a un
hosting de prueba.

#### Criterio de aprobación

- Pasa la lista de la mudanza completa (raíz pública, `.env`, errores, permisos).
- La web funciona de punta a punta con MariaDB.
- Los documentos para el dueño y para la mudanza están completos.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS precio;
CREATE TABLE precio (id INT AUTO_INCREMENT PRIMARY KEY, producto VARCHAR(40) NOT NULL UNIQUE, unidad ENUM('kg', 'atado', 'unidad') NOT NULL, precio DECIMAL(10, 2) NOT NULL, actualizado DATE NOT NULL);
CREATE TABLE pedido (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(60) NOT NULL, telefono VARCHAR(20) NOT NULL, detalle VARCHAR(500) NOT NULL, creado DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);
INSERT INTO precio (producto, unidad, precio, actualizado) VALUES
    ('Tomate', 'kg', 2800, '2026-10-03'), ('Lechuga', 'unidad', 1200, '2026-10-03'), ('Acelga', 'atado', 1500, '2026-10-03'), ('Papa', 'kg', 1100, '2026-10-02');
```

`.env`
```ini
APP_DEBUG=false
DB_DSN="mysql:host=localhost;dbname=puerto;charset=utf8mb4"
DB_USUARIO=root
DB_CLAVE=""
```

`src/app.php`
```php
<?php
declare(strict_types=1);

function config(): array
{
    static $c = null;
    return $c ??= parse_ini_file(__DIR__ . '/../.env', false, INI_SCANNER_TYPED) ?: [];
}

function pdo(): PDO
{
    static $pdo = null;
    return $pdo ??= new PDO((string) config()['DB_DSN'], (string) config()['DB_USUARIO'], (string) (config()['DB_CLAVE'] ?? ''), [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);
}

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}

function instalarManejadores(): void
{
    ini_set('display_errors', (config()['APP_DEBUG'] ?? false) === true ? '1' : '0');
    set_error_handler(fn(int $n, string $m, string $a, int $l): bool => throw new ErrorException($m, 0, $n, $a, $l));
    set_exception_handler(function (Throwable $e): void {
        $log = __DIR__ . '/../logs/errores.log';
        if (!is_dir(dirname($log))) {
            mkdir(dirname($log), 0775, true);
        }
        file_put_contents($log, date('c') . ' ' . get_class($e) . ': ' . $e->getMessage() . PHP_EOL, FILE_APPEND | LOCK_EX);
        http_response_code(500);
        echo '<h1>Uy, algo falló</h1><p>Probá de nuevo en un rato o llamanos al 380-4123456.</p>';
    });
}
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Encargo - El sitio del comercio del barrio: listo para subir.
session_start();
require __DIR__ . '/../src/app.php';
instalarManejadores();
$_SESSION['csrf'] ??= bin2hex(random_bytes(32));

$errores = [];
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
    $nombre = trim($_POST['nombre'] ?? '');
    $telefono = trim($_POST['telefono'] ?? '');
    $detalle = trim($_POST['detalle'] ?? '');
    if ($nombre === '') {
        $errores[] = 'Dejanos tu nombre.';
    }
    if (!preg_match('/^[\d\s+-]{8,20}$/', $telefono)) {
        $errores[] = 'El teléfono no es válido.';
    }
    if (mb_strlen($detalle) < 3 || mb_strlen($detalle) > 500) {
        $errores[] = 'Contanos qué querés llevar.';
    }
    if ($errores === []) {
        pdo()->prepare('INSERT INTO pedido (nombre, telefono, detalle) VALUES (?, ?, ?)')->execute([$nombre, $telefono, $detalle]);
        $_SESSION['flash'] = "¡Gracias, $nombre! Te avisamos cuando esté listo.";
        header('Location: /', true, 303);
        exit;
    }
}
$precios = pdo()->query("SELECT producto, unidad, precio, DATE_FORMAT(actualizado, '%d/%m') AS fecha FROM precio ORDER BY producto")->fetchAll();
$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']);
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Verdulería Doña Rosa</title></head>
<body>
    <h1>Verdulería Doña Rosa</h1>
    <?php if ($flash): ?><p><strong><?= e($flash) ?></strong></p><?php endif; ?>
    <h2>Precios de hoy</h2>
    <ul>
        <?php foreach ($precios as $p): ?>
            <li><?= e($p['producto']) ?>: $<?= number_format((float) $p['precio'], 0, ',', '.') ?> el <?= $p['unidad'] ?> (al <?= $p['fecha'] ?>)</li>
        <?php endforeach; ?>
    </ul>
    <h2>Pedí para retirar</h2>
    <?php foreach ($errores as $error): ?><p><?= e($error) ?></p><?php endforeach; ?>
    <form method="post">
        <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
        <input name="nombre" placeholder="Tu nombre"> <input name="telefono" placeholder="Teléfono">
        <textarea name="detalle" placeholder="2 kg de tomate, 1 lechuga…"></textarea>
        <button>Hacer el pedido</button>
    </form>
</body>
</html>
```

`LEEME.md`
```md
# Cómo usar el sitio (para Rosa)

**Actualizar los precios:** entrá a cPanel → phpMyAdmin → base `cuenta_verduleria` → tabla `precio` →
pestaña Examinar. Hacé doble clic en el precio para cambiarlo y en la fecha para poner la de hoy.

**Ver los pedidos:** misma base, tabla `pedido`, pestaña Examinar. Los más nuevos están al final
(podés hacer clic en la columna `creado` para ordenarlos).
```

`MUDANZA.md`
```md
# Mudanza de la verdulería

1. Subir `public/`, `src/`, `esquema.sql` a `/home/cuenta/verduleria/`. Crear `logs/` (755).
2. Dominio → Document Root `/home/cuenta/verduleria/public`.
3. Crear la base `cuenta_verduleria` y su usuario; importar `esquema.sql`.
4. Crear `.env` desde `.env.ejemplo` con `APP_DEBUG=false` y los datos de la base.
5. AutoSSL y la redirección a HTTPS del `.htaccess`.
6. Probar: la lista de precios, un pedido, un pedido con el teléfono mal.
```

### Prueba del sello

#### ¿Qué carpeta tiene que ser la raíz pública del dominio y por qué?

`public/`: así la web no puede llegar al código, al `.env` ni a los datos del resto del proyecto.

#### ¿Para qué sirve el `.htaccess` con `RewriteRule ^ index.php`?

Para que Apache mande a `index.php` todos los pedidos que no son un archivo real, así funciona el router con direcciones como `/barcos/12`.

#### ¿Qué cambia en el `.env` de producción?

`APP_DEBUG=false` y los datos de la base del hosting (con el prefijo de la cuenta), entre otros.

#### ¿Por qué se instalan las dependencias con `--no-dev` en el servidor?

Porque las de desarrollo (como PHPUnit) no hacen falta para que el sitio funcione y agregan archivos de más.

#### ¿Por qué se borra el script de diagnóstico después de usarlo?

Porque muestra información del servidor (versiones, carpetas, configuración) que le sirve a quien ataca.

### Soluciones (docente)

Nodo nuevo, pensado para hostings con cPanel como el de esta plataforma. Las misiones se prueban en la compu (`php -S … public/index.php`); subirlas a un hosting es opcional pero muy recomendable (hay hostings gratuitos de prueba). En la misión 3, `$pdo->quote()` escapa los valores según la conexión; para bases grandes conviene `mysqldump` si el hosting lo permite (cPanel tiene *Backup* y phpMyAdmin tiene *Exportar*).

## R05-N07 · Jefe final: el Dragón del Faro

```meta
tipo: jefe
padre: R05-N06
precio: 10
criatura: dragon
insignia: Sello del Dragón del Faro
insignia_descripcion: Venciste al Dragón del Faro: construiste un sistema web completo en PHP, probado y listo para subir.
usa: web.mvc, web.api-rest, cal.pruebas, sql.desde-codigo
```

### Crónica

La noche en que terminás tu último sistema, el mar se agita. De entre las olas se levanta el **Dragón del Faro**, hecho de todo lo que aprendiste y de todo lo que puede salir mal: formularios sin validar, consultas pegadas, reservas que se pisan, errores a la vista, pruebas que nadie escribió. Viene a apagar la luz del Faro.

—Esta vez no hay un solo truco —dice {mentor}, parada a tu lado en la cúpula—. El dragón se vence con un sistema **entero**: reglas probadas, datos protegidos, capas ordenadas, una API para las máquinas y una web para las personas. Todo lo que aprendiste en el Puerto, {heroe}, junto. Encendé la lámpara.

### Objetivos

- Diseñar un dominio con reglas y probarlo con PHPUnit sin base de datos.
- Montar ese dominio en un sistema MVC con MariaDB, login, web y API.
- Aplicar todas las defensas del Puerto y dejar el sistema listo para subir.

### Antes de empezar

- Todo el camino principal. En especial: repositorios (R04-N08), MVC (R05-N01), API (R05-N03), PHPUnit (R05-N04), configuración (R05-N05) y hosting (R05-N06).

### Explicación

#### El sistema: amarras del Puerto
El Puerto alquila **amarras** (lugares para atar un barco) por noche. Cada amarra
tiene un largo máximo y un precio por noche. Los **navegantes** se registran y
reservan: una amarra no puede tener dos reservas que se superpongan, un barco no
puede ser más largo que la amarra, y una reserva va de 1 a 14 noches. Cancelar solo
se puede hasta el día anterior a la llegada, y se cobra un 10% de la reserva como
cargo.

#### Cómo se reparte
| Misión | Qué se construye |
|---|---|
| 1 | el **dominio**: entidades, reglas y un repositorio en memoria, **probados con PHPUnit** |
| 2 | el **sistema**: el mismo dominio con un repositorio de MariaDB, web con login y una API JSON |

Separar así es exactamente lo que hacen los equipos profesionales: las reglas del
negocio no saben nada de la web ni de la base, y por eso se pueden probar solas.

#### El escudo completo
Antes de entregar, repasá las tres listas: la de la Oficina (escapar, CSRF, validar,
permisos, PRG), la de la Bodega (parámetros, transacciones, claves, índices,
repositorios) y la de la mudanza (`public/`, `.env`, errores, `.htaccess`).

### Misión R05-N07-M1 · El dominio probado

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 30
```

#### Consigna

Escribí el **dominio** del sistema de amarras con Composer (namespace `Amarras\`,
PSR-4), **sin base de datos**:

- `Amarra` (`readonly`: código, largo máximo en metros, precio por noche);
- `Reserva` (`readonly`: id opcional, código de amarra, navegante, largo del barco,
  llegada y salida como `DateTimeImmutable`, estado `activa`/`cancelada` con un enum);
  con `noches()`, `seSuperponeCon(Reserva)`;
- la interfaz `RepositorioReservas` (`deAmarra(string $codigo): array`,
  `buscar(int $id): ?Reserva`, `guardar(Reserva $r): Reserva`) y
  `RepositorioReservasEnMemoria`;
- `ServicioAmarras` con `reservar(Amarra $a, string $navegante, float $largo, string
  $llegada, string $salida): Reserva` y `cancelar(int $id, string $navegante,
  DateTimeImmutable $hoy): float` (devuelve el cargo). Lanza `ReglaRota` (una
  `DomainException` propia) con un mensaje claro para cada regla:
  - 1 a 14 noches;
  - el barco no puede ser más largo que la amarra;
  - no se superpone con otra reserva **activa** de la misma amarra;
  - solo el navegante de la reserva la puede cancelar;
  - se cancela hasta el día anterior a la llegada;
  - el cargo es el 10% de noches × precio.

Y las pruebas en `tests/` con PHPUnit, cubriendo **cada regla**, los casos borde
(llegar el día que otro se va, cancelar justo el día anterior) y que una reserva
cancelada libera la amarra. Todas tienen que pasar.

#### Criterio de aprobación

- El dominio no usa PDO ni `$_POST`: es PHP puro.
- Hay al menos una prueba por regla y los casos borde.
- `vendor/bin/phpunit` termina en `OK`.

#### Solución de referencia

`composer.json`
```json
{
    "name": "puerto/amarras-dominio",
    "require": { "php": ">=8.2" },
    "require-dev": { "phpunit/phpunit": "^11.5" },
    "autoload": { "psr-4": { "Amarras\\": "src/" } }
}
```

`phpunit.xml`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit bootstrap="vendor/autoload.php" colors="false">
    <testsuites>
        <testsuite name="Amarras"><directory>tests</directory></testsuite>
    </testsuites>
</phpunit>
```

`src/Amarra.php`
```php
<?php
declare(strict_types=1);

namespace Amarras;

readonly class Amarra
{
    public function __construct(public string $codigo, public float $largoMaximo, public float $precioNoche) {}
}
```

`src/Estado.php`
```php
<?php
declare(strict_types=1);

namespace Amarras;

enum Estado: string
{
    case Activa = 'activa';
    case Cancelada = 'cancelada';
}
```

`src/Reserva.php`
```php
<?php
declare(strict_types=1);

namespace Amarras;

use DateTimeImmutable;

readonly class Reserva
{
    public function __construct(
        public ?int $id,
        public string $amarra,
        public string $navegante,
        public float $largo,
        public DateTimeImmutable $llegada,
        public DateTimeImmutable $salida,
        public Estado $estado = Estado::Activa,
    ) {}

    public function noches(): int
    {
        return (int) $this->llegada->diff($this->salida)->days * ($this->salida > $this->llegada ? 1 : -1);
    }

    public function seSuperponeCon(Reserva $otra): bool
    {
        return $this->llegada < $otra->salida && $otra->llegada < $this->salida;
    }

    public function conId(int $id): self
    {
        return new self($id, $this->amarra, $this->navegante, $this->largo, $this->llegada, $this->salida, $this->estado);
    }

    public function cancelada(): self
    {
        return new self($this->id, $this->amarra, $this->navegante, $this->largo, $this->llegada, $this->salida, Estado::Cancelada);
    }
}
```

`src/ReglaRota.php`
```php
<?php
declare(strict_types=1);

namespace Amarras;

class ReglaRota extends \DomainException {}
```

`src/RepositorioReservas.php`
```php
<?php
declare(strict_types=1);

namespace Amarras;

interface RepositorioReservas
{
    /** @return Reserva[] */
    public function deAmarra(string $codigo): array;

    public function buscar(int $id): ?Reserva;

    public function guardar(Reserva $r): Reserva;
}
```

`src/RepositorioReservasEnMemoria.php`
```php
<?php
declare(strict_types=1);

namespace Amarras;

final class RepositorioReservasEnMemoria implements RepositorioReservas
{
    /** @var array<int, Reserva> */
    private array $reservas = [];
    private int $ultimoId = 0;

    public function deAmarra(string $codigo): array
    {
        return array_values(array_filter($this->reservas, fn(Reserva $r) => $r->amarra === $codigo));
    }

    public function buscar(int $id): ?Reserva
    {
        return $this->reservas[$id] ?? null;
    }

    public function guardar(Reserva $r): Reserva
    {
        $r = $r->id === null ? $r->conId(++$this->ultimoId) : $r;
        $this->reservas[$r->id] = $r;
        return $r;
    }
}
```

`src/ServicioAmarras.php`
```php
<?php
declare(strict_types=1);

namespace Amarras;

use DateTimeImmutable;

final class ServicioAmarras
{
    public const MAX_NOCHES = 14;
    public const CARGO_CANCELACION = 0.10;

    public function __construct(private RepositorioReservas $reservas) {}

    public function reservar(Amarra $amarra, string $navegante, float $largo, string $llegada, string $salida): Reserva
    {
        $nueva = new Reserva(null, $amarra->codigo, $navegante, $largo, new DateTimeImmutable($llegada), new DateTimeImmutable($salida));
        $noches = $nueva->noches();
        if ($noches < 1 || $noches > self::MAX_NOCHES) {
            throw new ReglaRota('Una reserva va de 1 a ' . self::MAX_NOCHES . " noches (pediste $noches)");
        }
        if ($largo > $amarra->largoMaximo) {
            throw new ReglaRota("El barco mide $largo m y la amarra {$amarra->codigo} admite hasta {$amarra->largoMaximo} m");
        }
        foreach ($this->reservas->deAmarra($amarra->codigo) as $existente) {
            if ($existente->estado === Estado::Activa && $nueva->seSuperponeCon($existente)) {
                throw new ReglaRota("La amarra {$amarra->codigo} está ocupada en esas fechas");
            }
        }
        return $this->reservas->guardar($nueva);
    }

    public function cancelar(int $id, string $navegante, Amarra $amarra, DateTimeImmutable $hoy): float
    {
        $reserva = $this->reservas->buscar($id) ?? throw new ReglaRota("No existe la reserva $id");
        if ($reserva->navegante !== $navegante) {
            throw new ReglaRota('Solo quien reservó puede cancelar');
        }
        if ($reserva->estado === Estado::Cancelada) {
            throw new ReglaRota('La reserva ya estaba cancelada');
        }
        if ($hoy >= $reserva->llegada) {
            throw new ReglaRota('Se cancela hasta el día anterior a la llegada');
        }
        $this->reservas->guardar($reserva->cancelada());
        return round($reserva->noches() * $amarra->precioNoche * self::CARGO_CANCELACION, 2);
    }
}
```

`tests/ServicioAmarrasTest.php`
```php
<?php
declare(strict_types=1);

use Amarras\Amarra;
use Amarras\Estado;
use Amarras\ReglaRota;
use Amarras\RepositorioReservasEnMemoria;
use Amarras\ServicioAmarras;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;

final class ServicioAmarrasTest extends TestCase
{
    private RepositorioReservasEnMemoria $repo;
    private ServicioAmarras $servicio;
    private Amarra $a1;

    protected function setUp(): void
    {
        $this->repo = new RepositorioReservasEnMemoria();
        $this->servicio = new ServicioAmarras($this->repo);
        $this->a1 = new Amarra('A1', 12, 18000);
    }

    public function testReservaValida(): void
    {
        $r = $this->servicio->reservar($this->a1, 'kira', 9.5, '2026-11-01', '2026-11-04');
        $this->assertSame(1, $r->id);
        $this->assertSame(3, $r->noches());
        $this->assertSame(Estado::Activa, $r->estado);
    }

    #[DataProvider('nochesInvalidas')]
    public function testNochesFueraDeRango(string $llegada, string $salida): void
    {
        $this->expectException(ReglaRota::class);
        $this->expectExceptionMessage('noches');
        $this->servicio->reservar($this->a1, 'kira', 9, $llegada, $salida);
    }

    public static function nochesInvalidas(): array
    {
        return ['cero' => ['2026-11-01', '2026-11-01'], 'al revés' => ['2026-11-05', '2026-11-01'], 'quince' => ['2026-11-01', '2026-11-16']];
    }

    public function testCatorceNochesSiSePuede(): void
    {
        $this->assertSame(14, $this->servicio->reservar($this->a1, 'kira', 9, '2026-11-01', '2026-11-15')->noches());
    }

    public function testBarcoDemasiadoLargo(): void
    {
        $this->expectException(ReglaRota::class);
        $this->expectExceptionMessage('admite hasta 12');
        $this->servicio->reservar($this->a1, 'kira', 12.5, '2026-11-01', '2026-11-03');
    }

    public function testNoSeSuperpone(): void
    {
        $this->servicio->reservar($this->a1, 'kira', 9, '2026-11-01', '2026-11-05');
        $this->expectException(ReglaRota::class);
        $this->expectExceptionMessage('ocupada');
        $this->servicio->reservar($this->a1, 'bron', 8, '2026-11-04', '2026-11-06');
    }

    public function testLlegarElDiaQueOtroSeVa(): void
    {
        $this->servicio->reservar($this->a1, 'kira', 9, '2026-11-01', '2026-11-05');
        $r = $this->servicio->reservar($this->a1, 'bron', 8, '2026-11-05', '2026-11-06');
        $this->assertSame(2, $r->id);
    }

    public function testCancelarCobraElDiezPorCiento(): void
    {
        $r = $this->servicio->reservar($this->a1, 'kira', 9, '2026-11-01', '2026-11-04');
        $cargo = $this->servicio->cancelar($r->id, 'kira', $this->a1, new DateTimeImmutable('2026-10-31'));
        $this->assertSame(5400.0, $cargo);
        $this->assertSame(Estado::Cancelada, $this->repo->buscar($r->id)->estado);
    }

    public function testNoSeCancelaElMismoDia(): void
    {
        $r = $this->servicio->reservar($this->a1, 'kira', 9, '2026-11-01', '2026-11-04');
        $this->expectException(ReglaRota::class);
        $this->expectExceptionMessage('día anterior');
        $this->servicio->cancelar($r->id, 'kira', $this->a1, new DateTimeImmutable('2026-11-01'));
    }

    public function testSoloQuienReservoCancela(): void
    {
        $r = $this->servicio->reservar($this->a1, 'kira', 9, '2026-11-01', '2026-11-04');
        $this->expectException(ReglaRota::class);
        $this->expectExceptionMessage('Solo quien reservó');
        $this->servicio->cancelar($r->id, 'bron', $this->a1, new DateTimeImmutable('2026-10-20'));
    }

    public function testUnaCanceladaLiberaLaAmarra(): void
    {
        $r = $this->servicio->reservar($this->a1, 'kira', 9, '2026-11-01', '2026-11-04');
        $this->servicio->cancelar($r->id, 'kira', $this->a1, new DateTimeImmutable('2026-10-20'));
        $otra = $this->servicio->reservar($this->a1, 'bron', 8, '2026-11-02', '2026-11-03');
        $this->assertSame('bron', $otra->navegante);
    }
}
```

### Misión R05-N07-M2 · El sistema en el Faro

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 30
```

#### Consigna

Montá el dominio de la misión 1 en un **sistema completo** (podés copiar sus clases
a `src/`):

- **Base** (`esquema.sql`): `navegante` (usuario único, nombre, hash), `amarra`
  (código, largo máximo, precio) y `reserva` (amarra, navegante, largo, llegada,
  salida, estado), con claves foráneas e índice por amarra.
- **`RepositorioReservasPdo`** que implementa la interfaz del dominio; el
  `ServicioAmarras` se usa **sin cambios**. La reserva se hace en una **transacción**
  que bloquea las reservas de esa amarra (`SELECT … FOR UPDATE`) antes de revisar la
  superposición.
- **Web** (MVC con router, `.env`, manejador de errores):
  `GET /login`, `POST /login`, `POST /salir`, `GET /amarras` (las amarras con su
  precio), `POST /reservas` (formulario con amarra, largo y fechas; los errores del
  dominio se muestran en la página), `GET /mis-reservas` y
  `POST /reservas/{id}/cancelar`.
- **API** (`GET /api/disponibles?llegada=…&salida=…&largo=…`): JSON con las amarras
  libres para esas fechas en las que entra el barco, sin login.

Con CSRF, sesiones con solo el id, consultas preparadas y PRG. El esquema trae los
navegantes `kira` (`ancla123`) y `bron` (`faro2026`) y cuatro amarras.

#### Criterio de aprobación

- El dominio de la misión 1 se usa sin cambios, con un repositorio PDO.
- La reserva no puede superponerse ni con dos pedidos simultáneos (transacción y `FOR UPDATE`).
- La web y la API funcionan de punta a punta y pasan todas las listas del escudo.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS reserva;
DROP TABLE IF EXISTS amarra;
DROP TABLE IF EXISTS navegante;
CREATE TABLE navegante (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(60) NOT NULL,
    hash VARCHAR(255) NOT NULL
) ENGINE=InnoDB;
CREATE TABLE amarra (
    codigo CHAR(3) PRIMARY KEY,
    largo_maximo DECIMAL(5, 2) NOT NULL,
    precio_noche DECIMAL(10, 2) NOT NULL
) ENGINE=InnoDB;
CREATE TABLE reserva (
    id INT AUTO_INCREMENT PRIMARY KEY,
    amarra CHAR(3) NOT NULL,
    navegante VARCHAR(20) NOT NULL,
    largo DECIMAL(5, 2) NOT NULL,
    llegada DATE NOT NULL,
    salida DATE NOT NULL,
    estado ENUM('activa', 'cancelada') NOT NULL DEFAULT 'activa',
    FOREIGN KEY (amarra) REFERENCES amarra(codigo),
    FOREIGN KEY (navegante) REFERENCES navegante(usuario),
    INDEX idx_reserva_amarra (amarra, llegada)
) ENGINE=InnoDB;
INSERT INTO navegante (usuario, nombre, hash) VALUES
    ('kira', 'Kira Valdez', '$2y$10$R7flf57cYzLAnMr14xX56OhKUJ5qlAco9VY/EbWmghiXoQB.vb5yS'),
    ('bron', 'Bron', '$2y$10$sY48d8IabcyzFGOVp12ZpuujEDnEgiSNQdtdVIB1rIGD4/BG9LYF6');
INSERT INTO amarra VALUES ('A1', 12, 18000), ('A2', 12, 18000), ('B1', 20, 32000), ('C1', 8, 9500);
INSERT INTO reserva (amarra, navegante, largo, llegada, salida) VALUES ('A1', 'bron', 10, '2026-11-01', '2026-11-05');
```

`.env`
```ini
APP_DEBUG=false
DB_DSN="mysql:host=localhost;dbname=puerto;charset=utf8mb4"
DB_USUARIO=root
DB_CLAVE=""
```

`src/Amarra.php`
```php
<?php
declare(strict_types=1);

namespace Amarras;

readonly class Amarra
{
    public function __construct(public string $codigo, public float $largoMaximo, public float $precioNoche) {}
}
```

`src/Estado.php`
```php
<?php
declare(strict_types=1);

namespace Amarras;

enum Estado: string
{
    case Activa = 'activa';
    case Cancelada = 'cancelada';
}
```

`src/Reserva.php`
```php
<?php
declare(strict_types=1);

namespace Amarras;

use DateTimeImmutable;

readonly class Reserva
{
    public function __construct(
        public ?int $id,
        public string $amarra,
        public string $navegante,
        public float $largo,
        public DateTimeImmutable $llegada,
        public DateTimeImmutable $salida,
        public Estado $estado = Estado::Activa,
    ) {}

    public function noches(): int
    {
        return (int) $this->llegada->diff($this->salida)->days * ($this->salida > $this->llegada ? 1 : -1);
    }

    public function seSuperponeCon(Reserva $otra): bool
    {
        return $this->llegada < $otra->salida && $otra->llegada < $this->salida;
    }

    public function conId(int $id): self
    {
        return new self($id, $this->amarra, $this->navegante, $this->largo, $this->llegada, $this->salida, $this->estado);
    }

    public function cancelada(): self
    {
        return new self($this->id, $this->amarra, $this->navegante, $this->largo, $this->llegada, $this->salida, Estado::Cancelada);
    }
}
```

`src/ReglaRota.php`
```php
<?php
declare(strict_types=1);

namespace Amarras;

class ReglaRota extends \DomainException {}
```

`src/RepositorioReservas.php`
```php
<?php
declare(strict_types=1);

namespace Amarras;

interface RepositorioReservas
{
    /** @return Reserva[] */
    public function deAmarra(string $codigo): array;

    public function buscar(int $id): ?Reserva;

    public function guardar(Reserva $r): Reserva;
}
```

`src/ServicioAmarras.php`
```php
<?php
declare(strict_types=1);

namespace Amarras;

use DateTimeImmutable;

final class ServicioAmarras
{
    public const MAX_NOCHES = 14;
    public const CARGO_CANCELACION = 0.10;

    public function __construct(private RepositorioReservas $reservas) {}

    public function reservar(Amarra $amarra, string $navegante, float $largo, string $llegada, string $salida): Reserva
    {
        $nueva = new Reserva(null, $amarra->codigo, $navegante, $largo, new DateTimeImmutable($llegada), new DateTimeImmutable($salida));
        $noches = $nueva->noches();
        if ($noches < 1 || $noches > self::MAX_NOCHES) {
            throw new ReglaRota('Una reserva va de 1 a ' . self::MAX_NOCHES . " noches (pediste $noches)");
        }
        if ($largo > $amarra->largoMaximo) {
            throw new ReglaRota("El barco mide $largo m y la amarra {$amarra->codigo} admite hasta {$amarra->largoMaximo} m");
        }
        foreach ($this->reservas->deAmarra($amarra->codigo) as $existente) {
            if ($existente->estado === Estado::Activa && $nueva->seSuperponeCon($existente)) {
                throw new ReglaRota("La amarra {$amarra->codigo} está ocupada en esas fechas");
            }
        }
        return $this->reservas->guardar($nueva);
    }

    public function cancelar(int $id, string $navegante, Amarra $amarra, DateTimeImmutable $hoy): float
    {
        $reserva = $this->reservas->buscar($id) ?? throw new ReglaRota("No existe la reserva $id");
        if ($reserva->navegante !== $navegante) {
            throw new ReglaRota('Solo quien reservó puede cancelar');
        }
        if ($reserva->estado === Estado::Cancelada) {
            throw new ReglaRota('La reserva ya estaba cancelada');
        }
        if ($hoy >= $reserva->llegada) {
            throw new ReglaRota('Se cancela hasta el día anterior a la llegada');
        }
        $this->reservas->guardar($reserva->cancelada());
        return round($reserva->noches() * $amarra->precioNoche * self::CARGO_CANCELACION, 2);
    }
}
```

`src/RepositorioReservasPdo.php`
```php
<?php
declare(strict_types=1);

namespace Amarras;

use DateTimeImmutable;
use PDO;

final class RepositorioReservasPdo implements RepositorioReservas
{
    public function __construct(private PDO $pdo) {}

    private function desdeFila(array $f): Reserva
    {
        return new Reserva((int) $f['id'], $f['amarra'], $f['navegante'], (float) $f['largo'], new DateTimeImmutable($f['llegada']), new DateTimeImmutable($f['salida']), Estado::from($f['estado']));
    }

    public function deAmarra(string $codigo): array
    {
        // Se llama dentro de la transacción de la reserva: FOR UPDATE bloquea esas filas.
        $s = $this->pdo->prepare('SELECT * FROM reserva WHERE amarra = ? FOR UPDATE');
        $s->execute([$codigo]);
        return array_map($this->desdeFila(...), $s->fetchAll());
    }

    public function buscar(int $id): ?Reserva
    {
        $s = $this->pdo->prepare('SELECT * FROM reserva WHERE id = ?');
        $s->execute([$id]);
        $f = $s->fetch();
        return $f === false ? null : $this->desdeFila($f);
    }

    public function guardar(Reserva $r): Reserva
    {
        if ($r->id === null) {
            $this->pdo->prepare('INSERT INTO reserva (amarra, navegante, largo, llegada, salida, estado) VALUES (?, ?, ?, ?, ?, ?)')
                ->execute([$r->amarra, $r->navegante, $r->largo, $r->llegada->format('Y-m-d'), $r->salida->format('Y-m-d'), $r->estado->value]);
            return $r->conId((int) $this->pdo->lastInsertId());
        }
        $this->pdo->prepare('UPDATE reserva SET estado = ? WHERE id = ?')->execute([$r->estado->value, $r->id]);
        return $r;
    }

    public function delNavegante(string $usuario): array
    {
        $s = $this->pdo->prepare('SELECT * FROM reserva WHERE navegante = ? ORDER BY llegada');
        $s->execute([$usuario]);
        return array_map($this->desdeFila(...), $s->fetchAll());
    }
}
```

`src/Datos.php`
```php
<?php
declare(strict_types=1);

namespace Amarras;

use PDO;

/** Lo que no es del dominio: navegantes, amarras y la búsqueda de disponibles. */
final class Datos
{
    public function __construct(private PDO $pdo) {}

    public function autenticar(string $usuario, string $clave): ?array
    {
        $s = $this->pdo->prepare('SELECT id, usuario, nombre, hash FROM navegante WHERE usuario = ?');
        $s->execute([mb_strtolower(trim($usuario))]);
        $n = $s->fetch();
        return $n !== false && password_verify($clave, $n['hash']) ? $n : null;
    }

    public function navegante(int $id): ?array
    {
        $s = $this->pdo->prepare('SELECT id, usuario, nombre FROM navegante WHERE id = ?');
        $s->execute([$id]);
        return $s->fetch() ?: null;
    }

    /** @return Amarra[] */
    public function amarras(): array
    {
        return array_map(fn($f) => new Amarra($f['codigo'], (float) $f['largo_maximo'], (float) $f['precio_noche']), $this->pdo->query('SELECT * FROM amarra ORDER BY codigo')->fetchAll());
    }

    public function amarra(string $codigo): ?Amarra
    {
        foreach ($this->amarras() as $a) {
            if ($a->codigo === $codigo) {
                return $a;
            }
        }
        return null;
    }

    public function disponibles(string $llegada, string $salida, float $largo): array
    {
        $s = $this->pdo->prepare(
            "SELECT a.codigo, a.largo_maximo, a.precio_noche FROM amarra a
             WHERE a.largo_maximo >= ? AND NOT EXISTS (
                 SELECT 1 FROM reserva r WHERE r.amarra = a.codigo AND r.estado = 'activa' AND r.llegada < ? AND ? < r.salida)
             ORDER BY a.precio_noche, a.codigo"
        );
        $s->execute([$largo, $salida, $llegada]);
        return array_map(fn($f) => ['codigo' => $f['codigo'], 'largo_maximo' => (float) $f['largo_maximo'], 'precio_noche' => (float) $f['precio_noche']], $s->fetchAll());
    }
}
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Jefe final - El sistema en el Faro: el dominio probado, sobre MariaDB, con web y API.
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (PHP_SAPI === 'cli-server' && $ruta !== '/' && is_file(__DIR__ . $ruta)) {
    return false;
}
spl_autoload_register(function (string $clase): void {
    $archivo = __DIR__ . '/../src/' . substr($clase, strlen('Amarras\\')) . '.php';
    if (str_starts_with($clase, 'Amarras\\') && is_file($archivo)) {
        require $archivo;
    }
});

use Amarras\Datos;
use Amarras\ReglaRota;
use Amarras\RepositorioReservasPdo;
use Amarras\ServicioAmarras;

$env = parse_ini_file(__DIR__ . '/../.env', false, INI_SCANNER_TYPED);
ini_set('display_errors', ($env['APP_DEBUG'] ?? false) === true ? '1' : '0');
set_error_handler(fn(int $n, string $m, string $a, int $l): bool => throw new ErrorException($m, 0, $n, $a, $l));
set_exception_handler(function (Throwable $e): void {
    error_log($e->getMessage());
    http_response_code(500);
    echo 'El Faro está momentáneamente fuera de servicio.';
});
date_default_timezone_set('America/Argentina/Buenos_Aires');
session_start();

$pdo = new PDO((string) $env['DB_DSN'], (string) $env['DB_USUARIO'], (string) ($env['DB_CLAVE'] ?? ''), [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);
$datos = new Datos($pdo);
$repo = new RepositorioReservasPdo($pdo);
$servicio = new ServicioAmarras($repo);
$_SESSION['csrf'] ??= bin2hex(random_bytes(32));
$metodo = $_SERVER['REQUEST_METHOD'];

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}

function ir(string $ruta, ?string $flash = null): never
{
    if ($flash !== null) {
        $_SESSION['flash'] = $flash;
    }
    header("Location: $ruta", true, 303);
    exit;
}

function pagina(string $titulo, string $cuerpo): string
{
    $flash = $_SESSION['flash'] ?? null;
    unset($_SESSION['flash']);
    return '<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>' . e($titulo) . ' · Amarras del Puerto</title></head><body>'
        . '<nav><a href="/amarras">Amarras</a> · <a href="/mis-reservas">Mis reservas</a></nav>'
        . ($flash !== null ? '<p><strong>' . e($flash) . '</strong></p>' : '') . '<h1>' . e($titulo) . '</h1>' . $cuerpo . '</body></html>';
}

function campoCsrf(): string
{
    return '<input type="hidden" name="csrf" value="' . $_SESSION['csrf'] . '">';
}

// La API: sin sesión, solo lectura
if ($ruta === '/api/disponibles') {
    header('Content-Type: application/json; charset=utf-8');
    $fecha = fn(string $c) => ($f = DateTimeImmutable::createFromFormat('!Y-m-d', $_GET[$c] ?? '')) && $f->format('Y-m-d') === $_GET[$c] ? $_GET[$c] : null;
    $llegada = $fecha('llegada');
    $salida = $fecha('salida');
    $largo = filter_var($_GET['largo'] ?? '', FILTER_VALIDATE_FLOAT);
    if ($llegada === null || $salida === null || $salida <= $llegada || $largo === false || $largo <= 0) {
        http_response_code(422);
        echo json_encode(['error' => 'llegada y salida (AAAA-MM-DD, salida posterior) y largo (metros) son obligatorios']);
        exit;
    }
    echo json_encode($datos->disponibles($llegada, $salida, $largo), JSON_UNESCAPED_UNICODE);
    exit;
}

if ($metodo === 'POST' && !hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
    http_response_code(403);
    exit('Pedido no válido.');
}

if ($ruta === '/login') {
    $error = '';
    if ($metodo === 'POST') {
        $n = $datos->autenticar($_POST['usuario'] ?? '', $_POST['clave'] ?? '');
        if ($n !== null) {
            session_regenerate_id(true);
            $_SESSION['navegante_id'] = (int) $n['id'];
            ir('/amarras');
        }
        $error = '<p>Usuario o contraseña incorrectos.</p>';
    }
    echo pagina('Entrar', $error . '<form method="post">' . campoCsrf() . '<input name="usuario"> <input type="password" name="clave"> <button>Entrar</button></form>');
    exit;
}

$yo = isset($_SESSION['navegante_id']) ? $datos->navegante($_SESSION['navegante_id']) : null;
if ($yo === null) {
    ir('/login');
}

if ($ruta === '/salir' && $metodo === 'POST') {
    $_SESSION = [];
    session_destroy();
    ir('/login');
}

if ($ruta === '/amarras' && $metodo === 'GET') {
    $filas = '';
    foreach ($datos->amarras() as $a) {
        $filas .= '<li>' . e($a->codigo) . ": hasta {$a->largoMaximo} m, $" . number_format($a->precioNoche, 0, ',', '.') . ' la noche</li>';
    }
    $opciones = implode('', array_map(fn($a) => '<option>' . e($a->codigo) . '</option>', $datos->amarras()));
    echo pagina('Amarras', "<p>Hola, " . e($yo['nombre']) . "</p><ul>$filas</ul>"
        . '<form method="post" action="/reservas">' . campoCsrf() . "<select name=\"amarra\">$opciones</select>"
        . '<input name="largo" placeholder="Largo (m)"> <input type="date" name="llegada"> <input type="date" name="salida"> <button>Reservar</button></form>'
        . '<form method="post" action="/salir">' . campoCsrf() . '<button>Salir</button></form>');
    exit;
}

if ($ruta === '/reservas' && $metodo === 'POST') {
    $amarra = $datos->amarra($_POST['amarra'] ?? '');
    $largo = filter_var($_POST['largo'] ?? '', FILTER_VALIDATE_FLOAT);
    if ($amarra === null || $largo === false || !strtotime($_POST['llegada'] ?? '') || !strtotime($_POST['salida'] ?? '')) {
        ir('/amarras', 'Completá la amarra, el largo y las dos fechas.');
    }
    $pdo->beginTransaction();
    try {
        $r = $servicio->reservar($amarra, $yo['usuario'], $largo, $_POST['llegada'], $_POST['salida']);
        $pdo->commit();
        ir('/mis-reservas', "Reservaste la amarra {$amarra->codigo} por {$r->noches()} noche/s.");
    } catch (ReglaRota $e) {
        $pdo->rollBack();
        ir('/amarras', $e->getMessage());
    }
}

if ($ruta === '/mis-reservas' && $metodo === 'GET') {
    $filas = '';
    foreach ($repo->delNavegante($yo['usuario']) as $r) {
        $filas .= '<li>' . e($r->amarra) . ' · ' . $r->llegada->format('d/m') . ' al ' . $r->salida->format('d/m') . " · {$r->estado->value}";
        if ($r->estado->value === 'activa') {
            $filas .= " <form method=\"post\" action=\"/reservas/{$r->id}/cancelar\" style=\"display:inline\">" . campoCsrf() . '<button>Cancelar</button></form>';
        }
        $filas .= '</li>';
    }
    echo pagina('Mis reservas', $filas === '' ? '<p>No tenés reservas.</p>' : "<ul>$filas</ul>");
    exit;
}

if (preg_match('#^/reservas/(\d+)/cancelar$#', $ruta, $m) && $metodo === 'POST') {
    $reserva = $repo->buscar((int) $m[1]);
    if ($reserva === null) {
        http_response_code(404);
        exit('No existe esa reserva.');
    }
    try {
        $cargo = $servicio->cancelar($reserva->id, $yo['usuario'], $datos->amarra($reserva->amarra), new DateTimeImmutable('today'));
        ir('/mis-reservas', 'Reserva cancelada. Cargo: $' . number_format($cargo, 2, ',', '.'));
    } catch (ReglaRota $e) {
        ir('/mis-reservas', $e->getMessage());
    }
}

http_response_code(404);
echo pagina('No encontrado', '<p>No existe esa página.</p>');
```

### Prueba del sello

#### ¿Por qué el dominio no usa PDO ni `$_POST`?

Para que las reglas del negocio se puedan probar solas, rápido y sin base de datos, y se puedan usar desde la web, la API o la terminal sin cambios.

#### ¿Cómo evita el sistema que dos personas reserven la misma amarra en el mismo segundo?

La reserva se hace en una transacción y el repositorio lee las reservas de esa amarra con `FOR UPDATE`: la segunda espera y, cuando lee, ya ve la primera.

#### ¿Por qué la API de disponibles responde 422 con fechas inválidas?

Porque el pedido está bien formado pero sus datos no sirven (fechas mal escritas o salida anterior a la llegada).

#### ¿Qué ventaja da que `ServicioAmarras` reciba la interfaz `RepositorioReservas`?

Que se puede usar con el repositorio en memoria en las pruebas y con el de PDO en el sistema, sin cambiar una línea del servicio.

#### ¿Qué revisás antes de subir el sistema?

Las tres listas: la de la Oficina (escapar, CSRF, validar, permisos, PRG), la de la Bodega (parámetros, transacciones, claves, repositorios) y la de la mudanza (`public/`, `.env`, errores, `.htaccess`).

### Soluciones (docente)

Jefe final del camino principal, escrito desde cero: integra todo el curso. La misión 1 se corrige con `vendor/bin/phpunit`; la 2, con `php -S localhost:8000 -t public public/index.php` y el esquema cargado. El `ServicioAmarras` y las entidades son idénticos en las dos misiones (se copian): es el punto del jefe. En la misión 2, cancelar compara con la fecha de hoy: para probarlo, conviene reservar fechas futuras.

## R05-N08 · La Encrucijada de los Sellos

```meta
tipo: ventana
padre: R05-N07
precio: 10
```

### Crónica

Con el Dragón vencido, el Faro vuelve a alumbrar. Bajás de la cúpula y en la plaza del Puerto encontrás una fuente con forma de sello de lacre gigante. De ella salen tres caminos: uno lleva a una arena donde se oyen espadas; otro, a una ciudadela de cristal con un escudo rojo en la puerta; el tercero, a una torre llena de palomas mensajeras que van y vienen sin parar.

{mentor} te espera sentada en el borde de la fuente, con la trompa apoyada en el agua.

—Ya hablás la lengua del Puerto, {heroe}. Lo que sigue no es obligatorio: es **tuyo**. Pero antes de elegir, mirá hacia atrás. ¿Qué te llevás de este viaje?

### Objetivos

- Repasar todo el camino principal y reconocer lo que aprendiste.
- Conocer las Sendas optativas que salen de acá.

### Explicación

#### Lo que ya sabés hacer

- **El Muelle de las Primeras Cartas**: variables, tipos, textos, entrada, decisiones, bucles, arrays, funciones y organizar el código en archivos.
- **El Astillero de los Moldes**: clases, encapsulamiento, herencia, interfaces, traits, enums, fechas, excepciones, namespaces y Composer.
- **La Oficina de Correos**: la web: HTTP, formularios, validación, XSS y CSRF, sesiones, login, subida de archivos y plantillas.
- **La Bodega del Puerto**: MySQL y MariaDB: tablas, consultas, relaciones, PDO, consultas preparadas, ABM, transacciones, índices y repositorios.
- **El Faro**: MVC con router, closures y generadores, APIs en JSON, pruebas con PHPUnit, errores y configuración, y subir a un hosting.

Con eso podés construir y publicar sistemas web completos: un sistema de turnos, una tienda, un panel de gestión o la API de una aplicación. Lo que sigue son **especializaciones**.

#### Las Sendas

Cada Senda es un camino optativo: no hace falta para completar el curso, y su entrada se paga con **comodines** (los que ganaste con los encargos). Adentro, los nodos se pagan con sellos, como siempre.

- **Senda de la Arena**: un **RPG por turnos** jugable en la terminal: héroes y enemigos con inteligencia, combate, oleadas y el ranking guardado en MariaDB.
- **Senda de la Ciudadela de Laravel**: el framework de PHP más usado: rutas, controladores, Blade, Eloquent con MySQL, validación, autenticación y pruebas.
- **Senda de los Mensajes Veloces**: una **aplicación web con JavaScript** que habla con tu API en PHP: `fetch`, JSON, una página que se actualiza sin recargar y autenticación con tokens.

Y si todavía no la hiciste, la **Senda del Escaparate** (HTML y CSS), que salía del Muelle, le da a todos tus sistemas una cara prolija.

### Misión R05-N08-M1 · Mirá hacia atrás

```meta
entrega: ninguna
entorno: navegador
monedas: 0
xp: 20
```

#### Consigna

Antes de elegir tu Senda, tomate cinco minutos:

1. ¿Cuál fue el tema que más te costó? ¿Qué te ayudó a entenderlo?
2. ¿Qué sistema de todo el camino te dio más orgullo?
3. ¿Qué te gustaría construir ahora con PHP?

Charlalo con el profe en la próxima clase (o escribíselo). Cuando lo tengas, marcá la misión como completada.

#### Criterio de aprobación

- Pensaste las tres preguntas y lo charlaste con el profe.

### Prueba del sello

#### ¿Cuántas Sendas salen de la Encrucijada y con qué se paga su entrada?

Tres (la Arena, la Ciudadela de Laravel y los Mensajes Veloces), y la entrada se paga con comodines.

#### ¿Hace falta completar una Senda para terminar el curso?

No: las Sendas son optativas.

### Soluciones (docente)

Nodo de cierre del tronco (tipo `ventana`), como la Encrucijada de los otros cursos. La misión es de reflexión y no se entrega. La Senda del Escaparate (HTML y CSS) brota del jefe de la rama 1, no de acá.

