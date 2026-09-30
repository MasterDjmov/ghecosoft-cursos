# RAMA S03 · Senda de los Mensajes Veloces: tu API con JavaScript

```meta
tipo: senda
posicion: 8
```

## S03-N01 · JavaScript en el navegador: el DOM y `fetch`

```meta
tipo: tema
padre: R05-N08
precio: 3
moneda: comodin
criatura: skeleton
ejecutable: no
temas: js.fundamentos, js.dom, js.eventos, js.fetch
usa: web.api-rest, html.estructura
```

### Crónica

El tercer camino desde la Encrucijada baja hasta el palomar del Puerto. Cientos de palomas mensajeras entran y salen sin parar: llevan una pregunta corta a la torre y vuelven con la respuesta atada a la pata, sin que nadie tenga que caminar hasta allá. En la ventana del palomar, un tablero cambia solo cada vez que llega una paloma.

—En el Faro armaste una API que responde JSON —dice {mentor}—. Hasta ahora la probabas con `curl`. Pero quien la usa de verdad es el **navegador**: una página que manda palomas —pedidos con `fetch`— y cambia solo el pedacito que hace falta, sin recargar. Para eso necesitás un poco de la otra lengua del Puerto, {heroe}: **JavaScript**.

### Objetivos

- Leer y escribir JavaScript básico partiendo de lo que ya sabés de PHP.
- Buscar y modificar elementos de la página (el DOM) y reaccionar a eventos.
- Pedir datos a tu API con `fetch` y `async`/`await`, y manejar los errores.
- Mostrar datos del servidor sin abrir agujeros de XSS (`textContent`).
- Servir la página y la API juntas con `php -S` y un `router.php`.

### Antes de empezar

- La Encrucijada de los Sellos (R05-N08), en especial la API REST en JSON (R05-N03) y el HTML de la Oficina de Correos (R03).

### Explicación

#### JavaScript en dos minutos (para quien ya sabe PHP)
JavaScript corre **en el navegador** de quien visita la página; PHP corre en el
servidor. Se parecen más de lo que parece:
| PHP | JavaScript |
|---|---|
| `$nombre = 'Kira';` | `const nombre = 'Kira';` (o `let` si va a cambiar) |
| `"Hola, {$nombre}"` | `` `Hola, ${nombre}` `` (con comillas invertidas) |
| `[1, 2, 3]` | `[1, 2, 3]` |
| `['nombre' => 'Kira', 'vida' => 90]` | `{ nombre: 'Kira', vida: 90 }` (un objeto) |
| `$barco['nombre']` | `barco.nombre` |
| `count($lista)` | `lista.length` |
| `foreach ($lista as $x)` | `for (const x of lista)` |
| `array_map(fn ($x) => $x * 2, $lista)` | `lista.map((x) => x * 2)` |
| `array_filter($lista, fn ($x) => $x > 2)` | `lista.filter((x) => x > 2)` |
| `===`, `!==` | `===`, `!==` (igual que en PHP: siempre los de tres) |
| `echo` para depurar | `console.log(...)` y se ve en la consola (F12) |

La **consola del navegador** (F12 → Consola) es tu mejor amiga: ahí salen los errores
de JavaScript con su línea. La pestaña **Red** muestra cada pedido que hace la página,
con su código y su respuesta: es tu `curl` visual.

#### El DOM: la página como objetos
El navegador convierte el HTML en un árbol de objetos, el **DOM**. Desde JavaScript se
busca un elemento y se lo cambia:
```js
const titulo = document.querySelector('h1');          // el primero que coincide (selector de CSS)
const filas = document.querySelectorAll('tr.alerta');  // todos
titulo.textContent = 'Salidas de hoy';                 // cambia el texto
titulo.classList.add('destacado');                     // agrega una clase

const item = document.createElement('li');             // crea un elemento nuevo
item.textContent = 'Albatros';
item.dataset.id = 3;                                   // queda como data-id="3"
document.querySelector('ul').append(item);             // lo agrega al final
lista.replaceChildren(...items);                       // reemplaza todo el contenido
```

#### Eventos
La página reacciona a lo que hace el usuario con **eventos**:
```js
boton.addEventListener('click', () => { ... });
selector.addEventListener('change', cargarSalidas);    // cambió un <select>
buscador.addEventListener('input', filtrar);            // cada tecla en un <input>
```
Si una lista tiene muchos elementos que se pueden tocar, se escucha **en la lista** y se
averigua cuál fue con `evento.target.closest('li')` (delegación de eventos): funciona
también para los elementos que se agregan después.

#### `fetch`, promesas y `async`/`await`
`fetch(url)` hace un pedido HTTP **sin recargar la página**. La respuesta tarda, así que
`fetch` devuelve una **promesa** (un "te lo mando cuando llegue"). Adentro de una
función `async`, `await` espera la respuesta y el código se lee de arriba hacia abajo:
```js
async function cargar() {
    const respuesta = await fetch('/api/salidas');
    if (!respuesta.ok) {                                // ok es true para los códigos 200 a 299
        throw new Error(`El servidor respondió ${respuesta.status}`);
    }
    const salidas = await respuesta.json();            // el JSON convertido en arrays y objetos
    ...
}
```
Ojo: `fetch` **no** falla con un 404 o un 500; solo falla si no hay red. Por eso hay que
mirar `respuesta.ok` (o `respuesta.status`). Los errores se atajan con
`try { … } catch (error) { … }`, igual que en PHP. Si la API devuelve un JSON de error
(`{"error": "No existe ese puerto"}`), leelo con `await respuesta.json()` para mostrar
el mensaje.

Para armar una URL con datos del usuario, `encodeURIComponent(texto)` (como
`urlencode` en PHP).

#### Mostrar datos sin abrir agujeros
| Para mostrar | Usá | Nunca |
|---|---|---|
| texto que viene del servidor o del usuario | `elemento.textContent = texto` | `elemento.innerHTML = texto` |

`innerHTML` interpreta el texto como HTML: si un barco se llama
`<img src=x onerror=alert(1)>`, se ejecuta. Es el mismo XSS de la Oficina de Correos,
ahora del lado del navegador. Con `createElement` y `textContent` no hay forma de que
un dato se convierta en código.

#### La página y la API juntas
La página (`index.html`, `app.js`) y la API viven en el **mismo** servidor, así el
navegador las deja hablar sin permisos especiales. En tu compu, un `router.php` manda
lo que empieza con `/api/` a tu API y deja que `php -S` sirva el resto tal cual:
```php
<?php
// php -S localhost:8000 -t public router.php
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (str_starts_with($ruta, '/api/')) {
    require __DIR__ . '/api.php';
    return true;
}
return false;   // index.html, app.js y los CSS los sirve php -S
```
En un hosting con Apache se hace lo mismo con una línea de `.htaccess`
(`RewriteRule ^api/ api.php [L]`, con `api.php` dentro de `public_html`).

### Código de ejemplo

El **tablón de salidas en vivo**: la tabla se carga desde la API, el filtro por destino
pide de nuevo sin recargar la página y las salidas con problemas se marcan.

`esquema.sql`
```sql
DROP TABLE IF EXISTS salida;
CREATE TABLE salida (
    id INT AUTO_INCREMENT PRIMARY KEY,
    barco VARCHAR(40) NOT NULL,
    destino VARCHAR(40) NOT NULL,
    hora TIME NOT NULL,
    estado ENUM('a horario', 'demorado', 'cancelado') NOT NULL DEFAULT 'a horario'
);
INSERT INTO salida (barco, destino, hora, estado) VALUES
    ('Gaviota', 'Colonia', '10:15', 'demorado'),
    ('Albatros', 'Montevideo', '08:30', 'a horario'),
    ('Tritón', 'Piriápolis', '17:45', 'cancelado'),
    ('Estrella del Sur', 'Montevideo', '13:00', 'a horario');
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`router.php`
```php
<?php
// Se prueba con: php -S localhost:8000 -t public router.php
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (str_starts_with($ruta, '/api/')) {
    require __DIR__ . '/api.php';
    return true;
}
return false;
```

`api.php`
```php
<?php
declare(strict_types=1);

$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

function responder(int $estado, mixed $datos): never
{
    http_response_code($estado);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($datos, JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR);
    exit;
}

$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($ruta === '/api/salidas') {
    $destino = $_GET['destino'] ?? '';
    $sql = "SELECT barco, destino, TIME_FORMAT(hora, '%H:%i') AS hora, estado FROM salida";
    if ($destino !== '') {
        $s = $pdo->prepare("$sql WHERE destino = ? ORDER BY hora");
        $s->execute([$destino]);
    } else {
        $s = $pdo->query("$sql ORDER BY hora");
    }
    responder(200, $s->fetchAll());
}
if ($ruta === '/api/destinos') {
    responder(200, $pdo->query('SELECT DISTINCT destino FROM salida ORDER BY destino')->fetchAll(PDO::FETCH_COLUMN));
}
responder(404, ['error' => 'No existe ese recurso']);
```

`public/index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Tablón de salidas</title>
    <style>
        .alerta { color: #b00020; }
        td { padding: 0.2rem 0.8rem; }
    </style>
</head>
<body>
    <h1>Tablón de salidas</h1>
    <label>Destino
        <select id="destino"><option value="">Todos</option></select>
    </label>
    <button id="actualizar">Actualizar</button>
    <p id="estado"></p>
    <table>
        <thead><tr><th>Hora</th><th>Barco</th><th>Destino</th><th>Estado</th></tr></thead>
        <tbody id="salidas"></tbody>
    </table>
    <script src="app.js"></script>
</body>
</html>
```

`public/app.js`
```js
const tabla = document.querySelector('#salidas');
const selector = document.querySelector('#destino');
const estado = document.querySelector('#estado');

async function pedirJson(url) {
    const respuesta = await fetch(url);
    if (!respuesta.ok) {
        throw new Error(`el servidor respondió ${respuesta.status}`);
    }
    return respuesta.json();
}

function fila(salida) {
    const tr = document.createElement('tr');
    for (const valor of [salida.hora, salida.barco, salida.destino, salida.estado]) {
        const td = document.createElement('td');
        td.textContent = valor;
        tr.append(td);
    }
    if (salida.estado !== 'a horario') {
        tr.classList.add('alerta');
    }
    return tr;
}

async function cargarSalidas() {
    estado.textContent = 'Cargando…';
    const destino = selector.value;
    const url = destino === '' ? '/api/salidas' : `/api/salidas?destino=${encodeURIComponent(destino)}`;
    try {
        const salidas = await pedirJson(url);
        tabla.replaceChildren(...salidas.map(fila));
        estado.textContent = `${salidas.length} salida(s)`;
    } catch (error) {
        estado.textContent = `No se pudieron cargar las salidas: ${error.message}`;
    }
}

async function cargarDestinos() {
    for (const destino of await pedirJson('/api/destinos')) {
        selector.append(new Option(destino, destino));
    }
}

selector.addEventListener('change', cargarSalidas);
document.querySelector('#actualizar').addEventListener('click', cargarSalidas);
cargarDestinos();
cargarSalidas();
```

Cargá `esquema.sql` en la base `puerto`, corré `php -S localhost:8000 -t public router.php`
y abrí `http://localhost:8000`. Abrí también F12 → Red y mirá los pedidos a `/api/...`
cada vez que cambiás el destino: la página nunca se recarga.

### ¿Para qué sirve?

Así funcionan casi todas las aplicaciones web de hoy: la página se carga una vez y después conversa con el servidor por detrás, pidiendo solo los datos. Tu API de PHP puede atender a esta página, a una app de celular y a otro sistema a la vez. Y saber leer la pestaña Red y la consola te deja encontrar en minutos si un error es del navegador (JavaScript) o del servidor (PHP).

### Errores habituales

**Esqueleto: `Cannot read properties of null (reading 'addEventListener')`.** El
`querySelector` no encontró el elemento: el `id` está mal escrito o el `<script>` está
en el `<head>` y corre antes de que exista el HTML. Poné el `<script>` al final del
`<body>`.

**Troll: el 404 que "anduvo".** `fetch` no falla con un 404 ni con un 500: si no mirás
`respuesta.ok`, intentás leer como datos un mensaje de error.

**Goblin: `Unexpected token '<'` al leer el JSON.** La API respondió HTML (un aviso de
PHP o una página de error) en lugar de JSON. Abrí la respuesta en la pestaña Red: ahí
está el aviso de PHP.

**Ogro: olvidarse el `await`.** Sin `await`, `fetch(...)` devuelve la promesa, no la
respuesta, y `respuesta.ok` es `undefined`.

**Orco: `innerHTML` con datos.** Si un dato del servidor tiene HTML, se ejecuta. Siempre
`textContent`.

**Esqueleto: la página anda pero la API da 404.** Levantaste `php -S` sin el
`router.php`, y los pedidos a `/api/...` buscan un archivo que no existe.

### Misión S03-N01-M1 · El buscador de barcos

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá una API con `GET /api/barcos`, que devuelve los barcos de la tabla (`nombre`,
`bandera`, `capacidad` en toneladas) ordenados por nombre, y una página que los muestra
en una lista (`Albatros · Argentina · 1200 t`). Arriba de la lista, un `<input>` de
búsqueda que **filtra mientras se escribe** (evento `input`), sin volver a pedir los
datos: coincide si el nombre **contiene** lo escrito, sin distinguir mayúsculas. Debajo
del buscador, `2 de 5 barcos`, o `Ningún barco coincide con «zz».` si no queda ninguno.

Cargá cinco barcos (uno con un nombre peligroso para probar el escapado:
`<b>Pirata</b>`, que tiene que verse tal cual). Entregá el proyecto en un zip.

#### Criterio de aprobación

- Los datos se piden una sola vez; el filtro trabaja sobre la lista en memoria.
- La lista se arma con `createElement` y `textContent` (el nombre con HTML se ve como texto).
- El contador y el mensaje de "ninguno" son correctos.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS barco;
CREATE TABLE barco (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL UNIQUE,
    bandera VARCHAR(30) NOT NULL,
    capacidad INT NOT NULL
);
INSERT INTO barco (nombre, bandera, capacidad) VALUES
    ('Gaviota', 'Uruguay', 450), ('Albatros', 'Argentina', 1200), ('Tortuga', 'Brasil', 80),
    ('Gavilán', 'Chile', 300), ('<b>Pirata</b>', 'Desconocida', 66);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`router.php`
```php
<?php
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (str_starts_with($ruta, '/api/')) {
    require __DIR__ . '/api.php';
    return true;
}
return false;
```

`api.php`
```php
<?php
declare(strict_types=1);

$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

header('Content-Type: application/json; charset=utf-8');
if (parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH) === '/api/barcos') {
    $barcos = $pdo->query('SELECT nombre, bandera, capacidad FROM barco ORDER BY nombre')->fetchAll();
    echo json_encode($barcos, JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR);
    exit;
}
http_response_code(404);
echo json_encode(['error' => 'No existe ese recurso']);
```

`public/index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Buscador de barcos</title>
</head>
<body>
    <h1>Barcos del Puerto</h1>
    <input id="buscar" placeholder="Buscar por nombre…" autocomplete="off">
    <p id="cuenta">Cargando…</p>
    <ul id="barcos"></ul>
    <script src="app.js"></script>
</body>
</html>
```

`public/app.js`
```js
const lista = document.querySelector('#barcos');
const buscador = document.querySelector('#buscar');
const cuenta = document.querySelector('#cuenta');
let barcos = [];

function item(barco) {
    const li = document.createElement('li');
    li.textContent = `${barco.nombre} · ${barco.bandera} · ${barco.capacidad} t`;
    return li;
}

function mostrar() {
    const texto = buscador.value.trim().toLowerCase();
    const visibles = barcos.filter((b) => b.nombre.toLowerCase().includes(texto));
    lista.replaceChildren(...visibles.map(item));
    cuenta.textContent = visibles.length === 0
        ? `Ningún barco coincide con «${buscador.value.trim()}».`
        : `${visibles.length} de ${barcos.length} barcos`;
}

async function cargar() {
    try {
        const respuesta = await fetch('/api/barcos');
        if (!respuesta.ok) {
            throw new Error(`el servidor respondió ${respuesta.status}`);
        }
        barcos = await respuesta.json();
        mostrar();
    } catch (error) {
        cuenta.textContent = `No se pudieron cargar los barcos: ${error.message}`;
    }
}

buscador.addEventListener('input', mostrar);
cargar();
```

### Misión S03-N01-M2 · El parte del tiempo

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

El faro publica el **parte del tiempo** de cada puerto. Armá la base (tablas `parte`
y `alerta`, una alerta pertenece a un parte) y la API:

- `GET /api/puertos`: la lista de nombres de puertos (también los que todavía no
  tienen parte).
- `GET /api/parte?puerto=Colonia`: `{"puerto": "Colonia", "temperatura": 17.5, "viento": 22,
  "alertas": ["Niebla hasta las 10"]}`; si el puerto no tiene parte, **404** con
  `{"error": "Todavía no hay parte para Ushuaia"}`; sin `puerto`, **400**.

La página tiene un `<select>` con los puertos. Al elegir uno muestra `Cargando…` y
después la tarjeta: `Colonia: 17,5 °C · viento 22 km/h` y la lista de alertas, o
`Sin alertas` si no tiene. Si la API responde un error, muestra **el mensaje que manda
la API**. Entregá el proyecto en un zip.

#### Criterio de aprobación

- La API responde los códigos correctos y el JSON de error.
- La página lee el mensaje de error del JSON cuando `respuesta.ok` es falso.
- La temperatura se muestra con coma decimal (`toLocaleString('es-AR')`).

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS alerta;
DROP TABLE IF EXISTS parte;
DROP TABLE IF EXISTS puerto;
CREATE TABLE puerto (nombre VARCHAR(40) PRIMARY KEY);
CREATE TABLE parte (
    id INT AUTO_INCREMENT PRIMARY KEY,
    puerto VARCHAR(40) NOT NULL UNIQUE,
    temperatura DECIMAL(4, 1) NOT NULL,
    viento INT NOT NULL,
    FOREIGN KEY (puerto) REFERENCES puerto (nombre)
);
CREATE TABLE alerta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parte_id INT NOT NULL,
    texto VARCHAR(100) NOT NULL,
    FOREIGN KEY (parte_id) REFERENCES parte (id)
);
INSERT INTO puerto VALUES ('Colonia'), ('Montevideo'), ('Ushuaia');
INSERT INTO parte (puerto, temperatura, viento) VALUES ('Colonia', 17.5, 22), ('Montevideo', 19, 35);
INSERT INTO alerta (parte_id, texto) VALUES (1, 'Niebla hasta las 10');
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`router.php`
```php
<?php
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (str_starts_with($ruta, '/api/')) {
    require __DIR__ . '/api.php';
    return true;
}
return false;
```

`api.php`
```php
<?php
declare(strict_types=1);

$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

function responder(int $estado, mixed $datos): never
{
    http_response_code($estado);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($datos, JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR);
    exit;
}

$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($ruta === '/api/puertos') {
    responder(200, $pdo->query('SELECT nombre FROM puerto ORDER BY nombre')->fetchAll(PDO::FETCH_COLUMN));
}
if ($ruta === '/api/parte') {
    $puerto = trim($_GET['puerto'] ?? '');
    if ($puerto === '') {
        responder(400, ['error' => 'Falta el puerto']);
    }
    $s = $pdo->prepare('SELECT id, puerto, temperatura, viento FROM parte WHERE puerto = ?');
    $s->execute([$puerto]);
    $parte = $s->fetch() ?: responder(404, ['error' => "Todavía no hay parte para $puerto"]);

    $s = $pdo->prepare('SELECT texto FROM alerta WHERE parte_id = ? ORDER BY id');
    $s->execute([$parte['id']]);
    responder(200, [
        'puerto' => $parte['puerto'],
        'temperatura' => (float) $parte['temperatura'],
        'viento' => (int) $parte['viento'],
        'alertas' => $s->fetchAll(PDO::FETCH_COLUMN),
    ]);
}
responder(404, ['error' => 'No existe ese recurso']);
```

`public/index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Parte del tiempo</title>
</head>
<body>
    <h1>Parte del tiempo</h1>
    <select id="puerto"><option value="">Elegí un puerto…</option></select>
    <section id="parte"></section>
    <script src="app.js"></script>
</body>
</html>
```

`public/app.js`
```js
const selector = document.querySelector('#puerto');
const tarjeta = document.querySelector('#parte');

function parrafo(texto) {
    const p = document.createElement('p');
    p.textContent = texto;
    return p;
}

async function pedirJson(url) {
    const respuesta = await fetch(url);
    const datos = await respuesta.json();
    if (!respuesta.ok) {
        throw new Error(datos.error ?? `el servidor respondió ${respuesta.status}`);
    }
    return datos;
}

async function mostrarParte() {
    if (selector.value === '') {
        tarjeta.replaceChildren();
        return;
    }
    tarjeta.replaceChildren(parrafo('Cargando…'));
    try {
        const parte = await pedirJson(`/api/parte?puerto=${encodeURIComponent(selector.value)}`);
        const temperatura = parte.temperatura.toLocaleString('es-AR');
        const alertas = document.createElement('ul');
        for (const texto of parte.alertas) {
            const li = document.createElement('li');
            li.textContent = texto;
            alertas.append(li);
        }
        tarjeta.replaceChildren(
            parrafo(`${parte.puerto}: ${temperatura} °C · viento ${parte.viento} km/h`),
            parte.alertas.length === 0 ? parrafo('Sin alertas') : alertas,
        );
    } catch (error) {
        tarjeta.replaceChildren(parrafo(error.message));
    }
}

async function cargarPuertos() {
    for (const puerto of await pedirJson('/api/puertos')) {
        selector.append(new Option(puerto, puerto));
    }
}

selector.addEventListener('change', mostrarParte);
cargarPuertos();
```

### Misión S03-N01-M3 · Los viajes con un clic

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Con las tablas `barco` y `viaje` (un barco hace muchos viajes), armá la API:

- `GET /api/barcos`: `id` y `nombre` de cada barco, por nombre.
- `GET /api/barcos/{id}/viajes`: `{"barco": "Albatros", "viajes": [{"destino": ...,
  "fecha": "2026-10-15", "pasajeros": 120}, ...]}` por fecha; **404** si el barco no
  existe.

La página muestra la lista de barcos; al **hacer clic** en uno, lo marca con la clase
`elegido` (y se la saca al anterior) y muestra al costado `Viajes de Albatros`, cada
viaje como `15/10/2026 · Colonia · 120 pasajeros` y el total (`Total: 330 pasajeros`),
o `Sin viajes agendados.` Usá **un solo** `addEventListener` en la lista (delegación
con `closest`) y guardá el id en `data-id`. Entregá el proyecto en un zip.

#### Criterio de aprobación

- La API responde el detalle y el 404, con consultas preparadas.
- Un solo escuchador en la lista; el id viaja en `data-id`.
- Solo el barco elegido tiene la clase `elegido`, y la fecha se muestra `dd/mm/aaaa`.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS viaje;
DROP TABLE IF EXISTS barco;
CREATE TABLE barco (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(40) NOT NULL UNIQUE);
CREATE TABLE viaje (
    id INT AUTO_INCREMENT PRIMARY KEY,
    barco_id INT NOT NULL,
    destino VARCHAR(40) NOT NULL,
    fecha DATE NOT NULL,
    pasajeros INT NOT NULL,
    FOREIGN KEY (barco_id) REFERENCES barco (id)
);
INSERT INTO barco (nombre) VALUES ('Albatros'), ('Gaviota'), ('Tortuga');
INSERT INTO viaje (barco_id, destino, fecha, pasajeros) VALUES
    (1, 'Montevideo', '2026-10-20', 210), (1, 'Colonia', '2026-10-15', 120), (2, 'Piriápolis', '2026-10-18', 45);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`router.php`
```php
<?php
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (str_starts_with($ruta, '/api/')) {
    require __DIR__ . '/api.php';
    return true;
}
return false;
```

`api.php`
```php
<?php
declare(strict_types=1);

$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

function responder(int $estado, mixed $datos): never
{
    http_response_code($estado);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($datos, JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR);
    exit;
}

$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($ruta === '/api/barcos') {
    $barcos = $pdo->query('SELECT id, nombre FROM barco ORDER BY nombre')->fetchAll();
    responder(200, array_map(fn ($b) => ['id' => (int) $b['id'], 'nombre' => $b['nombre']], $barcos));
}
if (preg_match('#^/api/barcos/(\d+)/viajes$#', $ruta, $m)) {
    $s = $pdo->prepare('SELECT nombre FROM barco WHERE id = ?');
    $s->execute([(int) $m[1]]);
    $nombre = $s->fetchColumn() ?: responder(404, ['error' => 'No existe ese barco']);

    $s = $pdo->prepare('SELECT destino, fecha, pasajeros FROM viaje WHERE barco_id = ? ORDER BY fecha');
    $s->execute([(int) $m[1]]);
    $viajes = array_map(fn ($v) => [...$v, 'pasajeros' => (int) $v['pasajeros']], $s->fetchAll());
    responder(200, ['barco' => $nombre, 'viajes' => $viajes]);
}
responder(404, ['error' => 'No existe ese recurso']);
```

`public/index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Viajes por barco</title>
    <style>
        .elegido { font-weight: bold; }
        li[data-id] { cursor: pointer; }
    </style>
</head>
<body>
    <h1>Barcos</h1>
    <ul id="barcos"></ul>
    <section id="detalle"></section>
    <script src="app.js"></script>
</body>
</html>
```

`public/app.js`
```js
const lista = document.querySelector('#barcos');
const detalle = document.querySelector('#detalle');

function elemento(etiqueta, texto) {
    const el = document.createElement(etiqueta);
    el.textContent = texto;
    return el;
}

function fechaLocal(iso) {
    const [anio, mes, dia] = iso.split('-');
    return `${dia}/${mes}/${anio}`;
}

async function pedirJson(url) {
    const respuesta = await fetch(url);
    const datos = await respuesta.json();
    if (!respuesta.ok) {
        throw new Error(datos.error ?? `el servidor respondió ${respuesta.status}`);
    }
    return datos;
}

async function mostrarViajes(id) {
    try {
        const { barco, viajes } = await pedirJson(`/api/barcos/${id}/viajes`);
        const total = viajes.reduce((suma, v) => suma + v.pasajeros, 0);
        const ul = document.createElement('ul');
        ul.append(...viajes.map((v) => elemento('li', `${fechaLocal(v.fecha)} · ${v.destino} · ${v.pasajeros} pasajeros`)));
        detalle.replaceChildren(
            elemento('h2', `Viajes de ${barco}`),
            viajes.length === 0 ? elemento('p', 'Sin viajes agendados.') : ul,
            elemento('p', `Total: ${total} pasajeros`),
        );
    } catch (error) {
        detalle.replaceChildren(elemento('p', error.message));
    }
}

lista.addEventListener('click', (evento) => {
    const item = evento.target.closest('li[data-id]');
    if (!item) {
        return;
    }
    lista.querySelector('.elegido')?.classList.remove('elegido');
    item.classList.add('elegido');
    mostrarViajes(item.dataset.id);
});

async function cargar() {
    const barcos = await pedirJson('/api/barcos');
    lista.replaceChildren(...barcos.map((b) => {
        const li = elemento('li', b.nombre);
        li.dataset.id = b.id;
        return li;
    }));
}

cargar();
```

### Encargo S03-N01-E1 · Pasajeros por destino

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

La API da un solo recurso, `GET /api/viajes`, con todos los viajes (`destino`,
`pasajeros`). **Todo el cálculo lo hace JavaScript**: agrupá por destino con `reduce`,
ordená de mayor a menor (y por nombre si empatan) y mostrá una tabla con el destino,
los pasajeros y una **barra** de `█`, un bloque cada 50 pasajeros (redondeando para
abajo, al menos uno). Abajo: `Total: 815 pasajeros en 6 viajes`. Un botón
`Actualizar` vuelve a pedir los datos (probalo agregando un viaje en la base).
Entregá el proyecto en un zip.

#### Criterio de aprobación

- La API no agrupa ni suma: devuelve los viajes tal cual.
- El agrupado usa `reduce`, el orden desempata por nombre y las barras son correctas.
- El botón vuelve a pedir y redibuja sin duplicar filas.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS viaje;
CREATE TABLE viaje (id INT AUTO_INCREMENT PRIMARY KEY, destino VARCHAR(40) NOT NULL, pasajeros INT NOT NULL);
INSERT INTO viaje (destino, pasajeros) VALUES
    ('Montevideo', 210), ('Colonia', 120), ('Piriápolis', 45),
    ('Colonia', 90), ('Montevideo', 140), ('Buenos Aires', 210);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`router.php`
```php
<?php
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (str_starts_with($ruta, '/api/')) {
    require __DIR__ . '/api.php';
    return true;
}
return false;
```

`api.php`
```php
<?php
declare(strict_types=1);

$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

header('Content-Type: application/json; charset=utf-8');
if (parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH) === '/api/viajes') {
    $viajes = $pdo->query('SELECT destino, pasajeros FROM viaje ORDER BY id')->fetchAll();
    echo json_encode(array_map(fn ($v) => ['destino' => $v['destino'], 'pasajeros' => (int) $v['pasajeros']], $viajes),
        JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR);
    exit;
}
http_response_code(404);
echo json_encode(['error' => 'No existe ese recurso']);
```

`public/index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Pasajeros por destino</title>
</head>
<body>
    <h1>Pasajeros por destino</h1>
    <button id="actualizar">Actualizar</button>
    <table>
        <tbody id="destinos"></tbody>
    </table>
    <p id="total"></p>
    <script src="app.js"></script>
</body>
</html>
```

`public/app.js`
```js
const cuerpo = document.querySelector('#destinos');
const total = document.querySelector('#total');

function celda(texto) {
    const td = document.createElement('td');
    td.textContent = texto;
    return td;
}

function agrupar(viajes) {
    const porDestino = viajes.reduce((acumulado, viaje) => {
        acumulado[viaje.destino] = (acumulado[viaje.destino] ?? 0) + viaje.pasajeros;
        return acumulado;
    }, {});
    return Object.entries(porDestino)
        .map(([destino, pasajeros]) => ({ destino, pasajeros }))
        .sort((a, b) => b.pasajeros - a.pasajeros || a.destino.localeCompare(b.destino));
}

async function cargar() {
    try {
        const respuesta = await fetch('/api/viajes');
        if (!respuesta.ok) {
            throw new Error(`el servidor respondió ${respuesta.status}`);
        }
        const viajes = await respuesta.json();
        cuerpo.replaceChildren(...agrupar(viajes).map(({ destino, pasajeros }) => {
            const tr = document.createElement('tr');
            tr.append(celda(destino), celda(pasajeros), celda('█'.repeat(Math.max(1, Math.floor(pasajeros / 50)))));
            return tr;
        }));
        const suma = viajes.reduce((s, v) => s + v.pasajeros, 0);
        total.textContent = `Total: ${suma} pasajeros en ${viajes.length} viajes`;
    } catch (error) {
        total.textContent = `No se pudieron cargar los viajes: ${error.message}`;
    }
}

document.querySelector('#actualizar').addEventListener('click', cargar);
cargar();
```

### Prueba del sello

#### ¿`fetch` lanza un error si la API responde 404?

No: `fetch` solo falla si no hay red. Hay que mirar `respuesta.ok` (o `respuesta.status`) y actuar.

#### ¿Por qué se usa `textContent` y no `innerHTML` para mostrar datos del servidor?

Porque `innerHTML` interpreta el texto como HTML y un dato con `<script>` o `onerror` se ejecutaría (XSS); `textContent` lo muestra como texto.

#### ¿Para qué sirve `await`?

Para esperar el resultado de una promesa (como la respuesta de `fetch`) dentro de una función `async`, y escribir el código de arriba hacia abajo.

#### ¿Qué hace `evento.target.closest('li')` en un escuchador puesto en la lista?

Encuentra el `<li>` donde se hizo clic (aunque se haya tocado algo de adentro): así un solo escuchador atiende a todos los elementos, incluso los que se agregan después.

#### ¿Qué hace el `router.php` con `php -S`?

Manda los pedidos que empiezan con `/api/` a la API en PHP y, con `return false`, deja que el servidor entregue tal cual los demás archivos (`index.html`, `app.js`).

### Soluciones (docente)

Sale de `22-JS-Vanilla` (08-DOM, 09-Eventos, 15-Async-Await-Fetch), llevado a una API de PHP con MariaDB. Cada solución se verifica levantando `php -S … -t public router.php` con el SQL cargado y manejando la página en un navegador real (Chromium), sin errores en la consola ni avisos de PHP. Para corregir: cargar el SQL, levantar el servidor y usar la página con F12 abierto (Consola y Red).

## S03-N02 · Formularios, sesión y errores: la página que escribe

```meta
tipo: tema
padre: S03-N01
precio: 10
criatura: troll
ejecutable: no
temas: js.formularios
usa: js.fetch, web.sesiones
```

### Crónica

Hasta ahora las palomas solo traían noticias. Pero en el palomar también hay que **mandar**: pedidos nuevos, correcciones, bajas. Y no cualquiera puede escribir en los libros del Puerto: la torre tiene que saber quién manda cada paloma, y devolver con una nota clara la que llegó mal escrita.

—Una página que escribe es otra cosa, {heroe} —dice {mentor}—. Hay que mandar los datos como corresponde, mostrar cada error al lado del campo que lo causó, saber quién está del otro lado y cerrar la puerta a los pedidos que llegan disfrazados desde otro sitio. Todo lo que aprendiste en la Oficina de Correos, ahora sin recargar la página.

### Objetivos

- Enviar formularios con `fetch` (POST, PUT, PATCH, DELETE) y cuerpos JSON.
- Mostrar los errores de validación (422) al lado de cada campo y los demás errores en un aviso.
- Mantener una sesión con cookies entre la página y la API, y reaccionar a un 401.
- Defender la API de pedidos falsificados desde otro sitio (CSRF).
- Organizar la página con un **estado** y una función que la **dibuja**.

### Antes de empezar

- El nodo anterior (DOM y `fetch`), las sesiones y el login de la Oficina de Correos (R03-N04 a R03-N06) y la API REST (R05-N03).

### Explicación

#### Enviar un formulario sin recargar
El evento `submit` avisa cuando se envía el formulario. `preventDefault()` frena el
envío normal (el que recarga la página) y lo hacemos nosotros con `fetch`:
```js
formulario.addEventListener('submit', async (evento) => {
    evento.preventDefault();
    const datos = Object.fromEntries(new FormData(formulario));   // { nombre: '...', bandera: '...' }
    const respuesta = await fetch('/api/barcos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...datos, capacidad: Number(datos.capacidad) }),
    });
    ...
});
```
`FormData` junta los campos por su atributo `name`; todos llegan como **texto**, así que
los números se convierten con `Number(...)`. Mientras se envía, desactivá el botón
(`boton.disabled = true`) para que un doble clic no mande dos veces, y reactivalo en un
`finally`.

Los atributos `required` o `type="email"` del HTML ayudan al usuario, pero **no
protegen**: cualquiera puede mandar un pedido a la API sin pasar por tu página. La
validación de verdad es siempre la del servidor.

#### Una función para hablar con la API
Todos los pedidos tienen lo mismo: mandar JSON, leer JSON, y convertir un código de
error en una excepción. Se escribe una vez:
```js
class ErrorApi extends Error {
    constructor(estado, cuerpo) {
        super(cuerpo?.error ?? `el servidor respondió ${estado}`);
        this.estado = estado;                 // 401, 403, 404, 422…
        this.campos = cuerpo?.campos ?? {};   // { nombre: 'Poné el nombre.' }
    }
}

async function api(metodo, ruta, datos) {
    const respuesta = await fetch(ruta, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: datos === undefined ? undefined : JSON.stringify(datos),
    });
    const cuerpo = respuesta.status === 204 ? null : await respuesta.json();
    if (!respuesta.ok) {
        throw new ErrorApi(respuesta.status, cuerpo);
    }
    return cuerpo;
}
```
`?.` y `??` funcionan igual que en PHP (`cuerpo?.error` no falla si `cuerpo` es `null`).

#### Qué hacer con cada error
| Código | Significa | La página |
|---|---|---|
| 422 | datos inválidos (`campos`) | muestra cada mensaje al lado de su campo |
| 401 | no hay sesión (o venció) | vuelve al formulario de ingreso |
| 403 | hay sesión, pero no permiso | avisa "no podés hacer eso" |
| 404 | ya no existe (otro lo borró) | avisa y lo saca de la lista |
| 500 | error del servidor | un aviso general; el detalle queda en el log de PHP |

Para los errores por campo, poné un lugar vacío debajo de cada uno
(`<small class="error" data-campo="nombre"></small>`), limpialos antes de enviar y
llenalos con `error.campos`.

#### La sesión: cookies que viajan solas
La sesión de PHP funciona igual que en la Oficina de Correos: la API hace
`session_start()` y guarda al usuario en `$_SESSION` al ingresar. El navegador guarda la
cookie de sesión y `fetch` la **manda sola** en cada pedido a la misma página. Al
cargar, la página pregunta `GET /api/sesion`: si responde el usuario, ya estaba adentro;
si responde 401, muestra el ingreso. Al salir, `DELETE /api/sesion` destruye la sesión.

Configurá la cookie con `httponly` (JavaScript no la puede leer: un XSS no la roba) y
`samesite=Lax` (no viaja en pedidos de otros sitios que cambian datos):
```php
session_set_cookie_params(['httponly' => true, 'samesite' => 'Lax']);
session_start();
```

#### CSRF en una API
En la Oficina de Correos cada formulario llevaba un token. Una API que **solo acepta
JSON** tiene una defensa más simple: un formulario HTML de otro sitio no puede mandar
`Content-Type: application/json`, y un `fetch` de otro sitio con ese encabezado necesita
un permiso especial (CORS) que tu API no da. Así que la API rechaza todo lo que cambia
datos y no llega como JSON:
```php
if ($metodo !== 'GET' && !str_starts_with($_SERVER['CONTENT_TYPE'] ?? '', 'application/json')) {
    responder(415, ['error' => 'Mandá los datos como JSON']);
}
```
Junto con `samesite=Lax`, cierra la puerta a los pedidos falsificados.

#### Estado y dibujo
Cuando la página hace muchas cosas (editar una fila, filtrar, borrar), tocar el DOM en
cada lugar se vuelve un lío. El orden que usan todos los frameworks de JavaScript es
simple: **los datos en una variable** (el estado) y **una función que dibuja** la
página a partir de ellos. Cada acción cambia el estado y llama a `dibujar()`:
```js
const estado = { tareas: [], filtro: 'todas' };

function dibujar() {
    const visibles = estado.tareas.filter(...);
    lista.replaceChildren(...visibles.map(itemTarea));
    contador.textContent = ...;
}

async function agregar(texto) {
    estado.tareas.push(await api('POST', '/api/tareas', { texto }));
    dibujar();
}
```

`confirm('¿Borrar?')` muestra una pregunta con Aceptar y Cancelar y devuelve `true` o
`false`: úsalo antes de borrar.

### Código de ejemplo

Las **notas del capitán**: cada usuario ingresa con su clave y ve solo sus notas; puede
agregar y borrar, la sesión sobrevive a una recarga y la API rechaza lo que no llega
como JSON. Usuarios de prueba: `Kira` / `ancla123` y `Bron` / `timon456`.

`esquema.sql`
```sql
DROP TABLE IF EXISTS nota;
DROP TABLE IF EXISTS usuario;
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL UNIQUE,
    clave_hash VARCHAR(255) NOT NULL
);
CREATE TABLE nota (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    texto VARCHAR(200) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario (id)
);
INSERT INTO usuario (nombre, clave_hash) VALUES
    ('Kira', '$2y$10$fu7iXdxu9Ep1C8AMf0uv/OzRg7.2L3r6SXq6TzN6nIoDR03ZVFrR.'),
    ('Bron', '$2y$10$DhjPPvro3/hEguiP4g2p7u/q6XroVWbO8YFp5QUEHkA5wa.S6n9kC');
INSERT INTO nota (usuario_id, texto) VALUES (1, 'Revisar las velas'), (2, 'Secreto de Bron'), (1, 'Pagar el amarre');
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`router.php`
```php
<?php
// php -S localhost:8000 -t public router.php
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (str_starts_with($ruta, '/api/')) {
    require __DIR__ . '/api.php';
    return true;
}
return false;
```

`api.php`
```php
<?php
declare(strict_types=1);

session_set_cookie_params(['httponly' => true, 'samesite' => 'Lax']);
session_start();

$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

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
        $datos = json_decode(file_get_contents('php://input') ?: '{}', true, flags: JSON_THROW_ON_ERROR);
    } catch (JsonException) {
        responder(400, ['error' => 'El cuerpo no es un JSON válido']);
    }
    return is_array($datos) ? $datos : responder(400, ['error' => 'Se esperaba un objeto JSON']);
}

function usuario(): array
{
    return $_SESSION['usuario'] ?? responder(401, ['error' => 'Tenés que ingresar']);
}

$metodo = $_SERVER['REQUEST_METHOD'];
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

// Contra CSRF: todo lo que cambia datos tiene que llegar como JSON.
if ($metodo !== 'GET' && !str_starts_with($_SERVER['CONTENT_TYPE'] ?? '', 'application/json')) {
    responder(415, ['error' => 'Mandá los datos como JSON']);
}

if ($ruta === '/api/sesion') {
    if ($metodo === 'GET') {
        responder(200, ['nombre' => usuario()['nombre']]);
    }
    if ($metodo === 'POST') {
        $d = leerJson();
        $s = $pdo->prepare('SELECT id, nombre, clave_hash FROM usuario WHERE nombre = ?');
        $s->execute([trim((string) ($d['nombre'] ?? ''))]);
        $u = $s->fetch();
        if (!$u || !password_verify((string) ($d['clave'] ?? ''), $u['clave_hash'])) {
            responder(401, ['error' => 'Usuario o clave incorrectos']);
        }
        session_regenerate_id(true);
        $_SESSION['usuario'] = ['id' => (int) $u['id'], 'nombre' => $u['nombre']];
        responder(200, ['nombre' => $u['nombre']]);
    }
    if ($metodo === 'DELETE') {
        $_SESSION = [];
        session_destroy();
        responder(204);
    }
    responder(405, ['error' => "Método $metodo no permitido"]);
}

if ($ruta === '/api/notas') {
    $yo = usuario();
    if ($metodo === 'GET') {
        $s = $pdo->prepare('SELECT id, texto FROM nota WHERE usuario_id = ? ORDER BY id DESC');
        $s->execute([$yo['id']]);
        responder(200, array_map(fn ($n) => ['id' => (int) $n['id'], 'texto' => $n['texto']], $s->fetchAll()));
    }
    if ($metodo === 'POST') {
        $texto = trim((string) (leerJson()['texto'] ?? ''));
        if ($texto === '' || mb_strlen($texto) > 200) {
            responder(422, ['error' => 'Datos inválidos', 'campos' => [
                'texto' => $texto === '' ? 'Escribí la nota.' : 'La nota tiene hasta 200 letras.',
            ]]);
        }
        $pdo->prepare('INSERT INTO nota (usuario_id, texto) VALUES (?, ?)')->execute([$yo['id'], $texto]);
        responder(201, ['id' => (int) $pdo->lastInsertId(), 'texto' => $texto]);
    }
    responder(405, ['error' => "Método $metodo no permitido"]);
}

if (preg_match('#^/api/notas/(\d+)$#', $ruta, $m) && $metodo === 'DELETE') {
    $yo = usuario();
    $s = $pdo->prepare('DELETE FROM nota WHERE id = ? AND usuario_id = ?');   // solo las propias
    $s->execute([(int) $m[1], $yo['id']]);
    $s->rowCount() === 1 ? responder(204) : responder(404, ['error' => 'No existe esa nota']);
}

responder(404, ['error' => 'No existe ese recurso']);
```

`public/index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Notas del capitán</title>
    <style>.error, .aviso { color: #b00020; }</style>
</head>
<body>
    <h1>Notas del capitán</h1>
    <p id="aviso" class="aviso"></p>

    <section id="ingreso" hidden>
        <h2>Ingresar</h2>
        <form id="form-ingreso">
            <label>Usuario <input name="nombre" autocomplete="username"></label>
            <label>Clave <input name="clave" type="password" autocomplete="current-password"></label>
            <button>Entrar</button>
        </form>
        <p id="aviso-ingreso" class="aviso"></p>
    </section>

    <section id="panel" hidden>
        <p><span id="saludo"></span> · <button id="salir">Salir</button></p>
        <form id="form-nota">
            <input name="texto" placeholder="Nueva nota…" autocomplete="off">
            <button>Agregar</button>
            <small id="error-nota" class="error"></small>
        </form>
        <ul id="notas"></ul>
    </section>

    <script src="app.js"></script>
</body>
</html>
```

`public/app.js`
```js
class ErrorApi extends Error {
    constructor(estado, cuerpo) {
        super(cuerpo?.error ?? `el servidor respondió ${estado}`);
        this.estado = estado;
        this.campos = cuerpo?.campos ?? {};
    }
}

async function api(metodo, ruta, datos) {
    const respuesta = await fetch(ruta, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: datos === undefined ? undefined : JSON.stringify(datos),
    });
    const cuerpo = respuesta.status === 204 ? null : await respuesta.json();
    if (!respuesta.ok) {
        throw new ErrorApi(respuesta.status, cuerpo);
    }
    return cuerpo;
}

const ingreso = document.querySelector('#ingreso');
const panel = document.querySelector('#panel');
const formIngreso = document.querySelector('#form-ingreso');
const avisoIngreso = document.querySelector('#aviso-ingreso');
const formNota = document.querySelector('#form-nota');
const errorNota = document.querySelector('#error-nota');
const lista = document.querySelector('#notas');
const aviso = document.querySelector('#aviso');

function mostrarIngreso(mensaje = '') {
    panel.hidden = true;
    ingreso.hidden = false;
    avisoIngreso.textContent = mensaje;
}

function atender(error) {
    if (error.estado === 401) {
        mostrarIngreso('Tu sesión venció: ingresá de nuevo.');
    } else {
        aviso.textContent = error.message;
    }
}

function itemNota(nota) {
    const li = document.createElement('li');
    li.dataset.id = nota.id;
    const texto = document.createElement('span');
    texto.textContent = nota.texto;
    const borrar = document.createElement('button');
    borrar.className = 'borrar';
    borrar.textContent = 'Borrar';
    li.append(texto, ' ', borrar);
    return li;
}

async function entrar(nombre) {
    document.querySelector('#saludo').textContent = `Hola, ${nombre}`;
    ingreso.hidden = true;
    panel.hidden = false;
    const notas = await api('GET', '/api/notas');
    lista.replaceChildren(...notas.map(itemNota));
}

formIngreso.addEventListener('submit', async (evento) => {
    evento.preventDefault();
    const boton = formIngreso.querySelector('button');
    boton.disabled = true;
    try {
        const yo = await api('POST', '/api/sesion', Object.fromEntries(new FormData(formIngreso)));
        formIngreso.reset();
        avisoIngreso.textContent = '';
        await entrar(yo.nombre);
    } catch (error) {
        avisoIngreso.textContent = error.message;
    } finally {
        boton.disabled = false;
    }
});

formNota.addEventListener('submit', async (evento) => {
    evento.preventDefault();
    errorNota.textContent = '';
    try {
        const nota = await api('POST', '/api/notas', Object.fromEntries(new FormData(formNota)));
        lista.prepend(itemNota(nota));
        formNota.reset();
    } catch (error) {
        if (error.estado === 422) {
            errorNota.textContent = error.campos.texto ?? error.message;
        } else {
            atender(error);
        }
    }
});

lista.addEventListener('click', async (evento) => {
    if (!evento.target.matches('button.borrar') || !confirm('¿Borrar la nota?')) {
        return;
    }
    const item = evento.target.closest('li');
    try {
        await api('DELETE', `/api/notas/${item.dataset.id}`);
        item.remove();
    } catch (error) {
        atender(error);
    }
});

document.querySelector('#salir').addEventListener('click', async () => {
    await api('DELETE', '/api/sesion');
    mostrarIngreso('Saliste. ¡Buen viaje!');
});

api('GET', '/api/sesion')
    .then((yo) => entrar(yo.nombre))
    .catch(() => mostrarIngreso());
```

Probalo con dos navegadores (o uno normal y otro en modo incógnito): Kira y Bron ven
cada uno sus notas. En la pestaña Red mirá el pedido a `/api/sesion` al cargar: con la
cookie responde 200; sin ella, 401. Y probá desde la terminal que la API no acepta
formularios comunes:
```bash
curl -i -X POST -d "texto=hola" http://localhost:8000/api/notas     # 415
```

### ¿Para qué sirve?

Es el esqueleto de cualquier aplicación con usuarios: ingresar, ver lo propio, cargar y borrar, con errores claros y sin recargar. La función `api()` y el patrón estado → dibujar son los mismos que vas a encontrar (con otros nombres) en React, Vue o Livewire. Y la API queda lista para que la use también una app de celular: la seguridad está en el servidor, no en la página.

### Errores habituales

**Troll: `Unexpected end of JSON input`.** Llamaste `respuesta.json()` en una respuesta
204 (sin cuerpo). Preguntá por el 204 antes de leer.

**Ogro: el formulario recarga la página.** Faltó `evento.preventDefault()`, o el
escuchador está en el botón (`click`) en vez de en el formulario (`submit`).

**Goblin: la capacidad llega como texto.** `FormData` da todo como texto: `"300"`. Si la
API espera un número, convertilo con `Number(...)` (y la API igual lo tiene que validar).

**Orco: esconder el botón no es seguridad.** Si solo la capitana puede despachar, la
**API** tiene que responder 403 a los demás. Esconder el botón es comodidad, no
protección: cualquiera manda el pedido con `curl`.

**Troll: la sesión que "se pierde".** Cada `php -S` nuevo no borra las sesiones, pero si
cambiás de `localhost` a `127.0.0.1` la cookie es de otro sitio. Usá siempre la misma
dirección.

**Esqueleto: el mensaje de error que no aparece.** El `data-campo` del HTML no coincide
con la clave de `campos` que manda la API (`nombre` ≠ `Nombre`).

### Misión S03-N02-M1 · El alta de barcos

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Una página con la lista de barcos (por nombre: `Albatros · Argentina · 1200 t`) y un
formulario para registrar uno nuevo **sin recargar**. La API:

- `GET /api/barcos` y `POST /api/barcos` (solo JSON: si no, 415);
- validación con estos mensajes por campo (422 con `campos`): `nombre` obligatorio y
  de hasta 40 letras (`Poné el nombre (hasta 40 letras).`), `bandera` obligatoria
  (`Poné la bandera.`), `capacidad` entero mayor que 0
  (`La capacidad es un número entero mayor que 0.`);
- nombre repetido: 422 con `Ya existe un barco con ese nombre.` en el campo `nombre`
  (atajando el error 1062 de MariaDB);
- si sale bien, 201 con el barco creado.

La página muestra cada error **debajo de su campo** (y los borra al volver a enviar),
desactiva el botón mientras envía y, si sale bien, muestra `Barco Tritón registrado.`,
vacía el formulario y actualiza la lista. Entregá el proyecto en un zip.

#### Criterio de aprobación

- La API valida todo y responde 201, 415 y 422 cuando corresponde.
- Los errores aparecen al lado de cada campo y se limpian al reenviar.
- La lista se actualiza sin recargar la página.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS barco;
CREATE TABLE barco (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL UNIQUE,
    bandera VARCHAR(30) NOT NULL,
    capacidad INT NOT NULL
);
INSERT INTO barco (nombre, bandera, capacidad) VALUES ('Gaviota', 'Uruguay', 450), ('Albatros', 'Argentina', 1200);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`router.php`
```php
<?php
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (str_starts_with($ruta, '/api/')) {
    require __DIR__ . '/api.php';
    return true;
}
return false;
```

`api.php`
```php
<?php
declare(strict_types=1);

$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

function responder(int $estado, mixed $datos): never
{
    http_response_code($estado);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($datos, JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR);
    exit;
}

function leerJson(): array
{
    try {
        $datos = json_decode(file_get_contents('php://input') ?: '{}', true, flags: JSON_THROW_ON_ERROR);
    } catch (JsonException) {
        responder(400, ['error' => 'El cuerpo no es un JSON válido']);
    }
    return is_array($datos) ? $datos : responder(400, ['error' => 'Se esperaba un objeto JSON']);
}

function comoJson(array $b): array
{
    return ['id' => (int) $b['id'], 'nombre' => $b['nombre'], 'bandera' => $b['bandera'], 'capacidad' => (int) $b['capacidad']];
}

$metodo = $_SERVER['REQUEST_METHOD'];
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($metodo !== 'GET' && !str_starts_with($_SERVER['CONTENT_TYPE'] ?? '', 'application/json')) {
    responder(415, ['error' => 'Mandá los datos como JSON']);
}

if ($ruta === '/api/barcos' && $metodo === 'GET') {
    responder(200, array_map('comoJson', $pdo->query('SELECT * FROM barco ORDER BY nombre')->fetchAll()));
}

if ($ruta === '/api/barcos' && $metodo === 'POST') {
    $d = leerJson();
    $nombre = trim((string) ($d['nombre'] ?? ''));
    $bandera = trim((string) ($d['bandera'] ?? ''));
    $capacidad = $d['capacidad'] ?? null;

    $errores = [];
    if ($nombre === '' || mb_strlen($nombre) > 40) {
        $errores['nombre'] = 'Poné el nombre (hasta 40 letras).';
    }
    if ($bandera === '') {
        $errores['bandera'] = 'Poné la bandera.';
    }
    if (!is_int($capacidad) || $capacidad <= 0) {
        $errores['capacidad'] = 'La capacidad es un número entero mayor que 0.';
    }
    if ($errores !== []) {
        responder(422, ['error' => 'Datos inválidos', 'campos' => $errores]);
    }

    try {
        $pdo->prepare('INSERT INTO barco (nombre, bandera, capacidad) VALUES (?, ?, ?)')->execute([$nombre, $bandera, $capacidad]);
    } catch (PDOException $e) {
        if (($e->errorInfo[1] ?? null) === 1062) {
            responder(422, ['error' => 'Datos inválidos', 'campos' => ['nombre' => 'Ya existe un barco con ese nombre.']]);
        }
        throw $e;
    }
    responder(201, comoJson(['id' => $pdo->lastInsertId(), 'nombre' => $nombre, 'bandera' => $bandera, 'capacidad' => $capacidad]));
}

responder(404, ['error' => 'No existe ese recurso']);
```

`public/index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Registro de barcos</title>
    <style>.error { color: #b00020; display: block; }</style>
</head>
<body>
    <h1>Registro de barcos</h1>
    <form id="alta">
        <label>Nombre <input name="nombre" autocomplete="off"></label>
        <small class="error" data-campo="nombre"></small>
        <label>Bandera <input name="bandera" autocomplete="off"></label>
        <small class="error" data-campo="bandera"></small>
        <label>Capacidad (t) <input name="capacidad" inputmode="numeric"></label>
        <small class="error" data-campo="capacidad"></small>
        <button>Registrar</button>
    </form>
    <p id="aviso"></p>
    <ul id="barcos"></ul>
    <script src="app.js"></script>
</body>
</html>
```

`public/app.js`
```js
class ErrorApi extends Error {
    constructor(estado, cuerpo) {
        super(cuerpo?.error ?? `el servidor respondió ${estado}`);
        this.estado = estado;
        this.campos = cuerpo?.campos ?? {};
    }
}

async function api(metodo, ruta, datos) {
    const respuesta = await fetch(ruta, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: datos === undefined ? undefined : JSON.stringify(datos),
    });
    const cuerpo = respuesta.status === 204 ? null : await respuesta.json();
    if (!respuesta.ok) {
        throw new ErrorApi(respuesta.status, cuerpo);
    }
    return cuerpo;
}

const formulario = document.querySelector('#alta');
const aviso = document.querySelector('#aviso');
const lista = document.querySelector('#barcos');

async function cargarLista() {
    const barcos = await api('GET', '/api/barcos');
    lista.replaceChildren(...barcos.map((b) => {
        const li = document.createElement('li');
        li.textContent = `${b.nombre} · ${b.bandera} · ${b.capacidad} t`;
        return li;
    }));
}

function mostrarErrores(campos) {
    for (const lugar of formulario.querySelectorAll('[data-campo]')) {
        lugar.textContent = campos[lugar.dataset.campo] ?? '';
    }
}

formulario.addEventListener('submit', async (evento) => {
    evento.preventDefault();
    const boton = formulario.querySelector('button');
    const datos = Object.fromEntries(new FormData(formulario));
    mostrarErrores({});
    aviso.textContent = '';
    boton.disabled = true;
    try {
        const barco = await api('POST', '/api/barcos', {
            ...datos,
            capacidad: datos.capacidad.trim() === '' ? null : Number(datos.capacidad),
        });
        aviso.textContent = `Barco ${barco.nombre} registrado.`;
        formulario.reset();
        await cargarLista();
    } catch (error) {
        if (error.estado === 422) {
            mostrarErrores(error.campos);
        } else {
            aviso.textContent = error.message;
        }
    } finally {
        boton.disabled = false;
    }
});

cargarLista();
```

### Misión S03-N02-M2 · Editar y borrar en la lista

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

La lista de precios de la bodega (`producto`: `nombre`, `precio`), editable en el lugar.
La API tiene `GET /api/productos`, `PUT /api/productos/{id}` (valida: nombre
obligatorio, `Poné el nombre.`; precio número mayor que 0,
`El precio tiene que ser mayor que 0.`) y `DELETE /api/productos/{id}` (204, o 404 si ya
no existe).

La página guarda los productos en un **estado** y los dibuja con una función. Cada fila
muestra `Boya naranja · $ 4.200,00` con los botones **Editar** y **Borrar**:

- **Editar** convierte esa fila en dos campos con los valores actuales y los botones
  **Guardar** y **Cancelar** (una sola fila en edición a la vez). Guardar manda el PUT;
  si la API responde 422, el mensaje aparece en la fila y sigue en edición; si sale
  bien, la fila vuelve a mostrarse con los datos nuevos. Cancelar la deja como estaba.
- **Borrar** pregunta con `confirm` y manda el DELETE; muestra `Producto borrado.` Si la
  API responde 404 (alguien lo borró antes), muestra `Ese producto ya no existe.` y lo
  saca igual de la lista.

Entregá el proyecto en un zip.

#### Criterio de aprobación

- Hay un estado (`productos`, `editando`) y una función `dibujar()`; las acciones cambian el estado y redibujan.
- La edición muestra los errores 422 en la fila y Cancelar no manda nada.
- El borrado atiende el 404.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(60) NOT NULL, precio DECIMAL(10, 2) NOT NULL);
INSERT INTO producto (nombre, precio) VALUES ('Soga de amarre', 8500), ('Farol a querosén', 23000), ('Boya naranja', 4200);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`router.php`
```php
<?php
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (str_starts_with($ruta, '/api/')) {
    require __DIR__ . '/api.php';
    return true;
}
return false;
```

`api.php`
```php
<?php
declare(strict_types=1);

$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

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
        $datos = json_decode(file_get_contents('php://input') ?: '{}', true, flags: JSON_THROW_ON_ERROR);
    } catch (JsonException) {
        responder(400, ['error' => 'El cuerpo no es un JSON válido']);
    }
    return is_array($datos) ? $datos : responder(400, ['error' => 'Se esperaba un objeto JSON']);
}

function comoJson(array $p): array
{
    return ['id' => (int) $p['id'], 'nombre' => $p['nombre'], 'precio' => (float) $p['precio']];
}

$metodo = $_SERVER['REQUEST_METHOD'];
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($metodo !== 'GET' && !str_starts_with($_SERVER['CONTENT_TYPE'] ?? '', 'application/json')) {
    responder(415, ['error' => 'Mandá los datos como JSON']);
}

if ($ruta === '/api/productos' && $metodo === 'GET') {
    responder(200, array_map('comoJson', $pdo->query('SELECT * FROM producto ORDER BY nombre')->fetchAll()));
}

if (preg_match('#^/api/productos/(\d+)$#', $ruta, $m)) {
    $id = (int) $m[1];
    $s = $pdo->prepare('SELECT * FROM producto WHERE id = ?');
    $s->execute([$id]);
    $s->fetch() ?: responder(404, ['error' => 'Ese producto ya no existe.']);

    if ($metodo === 'PUT') {
        $d = leerJson();
        $nombre = trim((string) ($d['nombre'] ?? ''));
        $precio = $d['precio'] ?? null;
        $errores = [];
        if ($nombre === '') {
            $errores['nombre'] = 'Poné el nombre.';
        }
        if (!is_int($precio) && !is_float($precio) || $precio <= 0) {
            $errores['precio'] = 'El precio tiene que ser mayor que 0.';
        }
        if ($errores !== []) {
            responder(422, ['error' => 'Datos inválidos', 'campos' => $errores]);
        }
        $pdo->prepare('UPDATE producto SET nombre = ?, precio = ? WHERE id = ?')->execute([$nombre, $precio, $id]);
        responder(200, comoJson(['id' => $id, 'nombre' => $nombre, 'precio' => $precio]));
    }
    if ($metodo === 'DELETE') {
        $pdo->prepare('DELETE FROM producto WHERE id = ?')->execute([$id]);
        responder(204);
    }
    responder(405, ['error' => "Método $metodo no permitido"]);
}

responder(404, ['error' => 'No existe ese recurso']);
```

`public/index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Precios de la bodega</title>
    <style>.error { color: #b00020; }</style>
</head>
<body>
    <h1>Precios de la bodega</h1>
    <p id="aviso"></p>
    <ul id="productos"></ul>
    <script src="app.js"></script>
</body>
</html>
```

`public/app.js`
```js
class ErrorApi extends Error {
    constructor(estado, cuerpo) {
        super(cuerpo?.error ?? `el servidor respondió ${estado}`);
        this.estado = estado;
        this.campos = cuerpo?.campos ?? {};
    }
}

async function api(metodo, ruta, datos) {
    const respuesta = await fetch(ruta, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: datos === undefined ? undefined : JSON.stringify(datos),
    });
    const cuerpo = respuesta.status === 204 ? null : await respuesta.json();
    if (!respuesta.ok) {
        throw new ErrorApi(respuesta.status, cuerpo);
    }
    return cuerpo;
}

const lista = document.querySelector('#productos');
const aviso = document.querySelector('#aviso');
const estado = { productos: [], editando: null, error: '' };

const pesos = (n) => '$ ' + n.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

function crear(etiqueta, texto, propiedades = {}) {
    const el = Object.assign(document.createElement(etiqueta), propiedades);
    if (texto !== undefined) {
        el.textContent = texto;
    }
    return el;
}

function fila(producto) {
    const li = crear('li');
    li.dataset.id = producto.id;
    if (estado.editando === producto.id) {
        li.append(
            crear('input', undefined, { name: 'nombre', value: producto.nombre }),
            crear('input', undefined, { name: 'precio', value: String(producto.precio) }),
            crear('button', 'Guardar', { className: 'guardar' }),
            crear('button', 'Cancelar', { className: 'cancelar' }),
            crear('small', estado.error, { className: 'error' }),
        );
    } else {
        li.append(
            crear('span', `${producto.nombre} · ${pesos(producto.precio)}`),
            ' ',
            crear('button', 'Editar', { className: 'editar' }),
            crear('button', 'Borrar', { className: 'borrar' }),
        );
    }
    return li;
}

function dibujar() {
    lista.replaceChildren(...estado.productos.map(fila));
}

async function guardar(li, id) {
    const nombre = li.querySelector('[name=nombre]').value;
    const precio = Number(li.querySelector('[name=precio]').value.replace(',', '.'));
    try {
        const actualizado = await api('PUT', `/api/productos/${id}`, { nombre, precio });
        estado.productos = estado.productos.map((p) => (p.id === id ? actualizado : p));
        estado.editando = null;
    } catch (error) {
        if (error.estado !== 422) {
            throw error;
        }
        estado.error = Object.values(error.campos).join(' ');
    }
}

async function borrar(id) {
    try {
        await api('DELETE', `/api/productos/${id}`);
        aviso.textContent = 'Producto borrado.';
    } catch (error) {
        if (error.estado !== 404) {
            throw error;
        }
        aviso.textContent = 'Ese producto ya no existe.';
    }
    estado.productos = estado.productos.filter((p) => p.id !== id);
}

lista.addEventListener('click', async (evento) => {
    const boton = evento.target.closest('button');
    if (!boton) {
        return;
    }
    const li = boton.closest('li');
    const id = Number(li.dataset.id);
    try {
        if (boton.matches('.editar')) {
            estado.editando = id;
            estado.error = '';
        } else if (boton.matches('.cancelar')) {
            estado.editando = null;
        } else if (boton.matches('.guardar')) {
            await guardar(li, id);
        } else if (boton.matches('.borrar') && confirm('¿Borrar el producto?')) {
            await borrar(id);
        }
    } catch (error) {
        aviso.textContent = error.message;
    }
    dibujar();
});

api('GET', '/api/productos').then((productos) => {
    estado.productos = productos;
    dibujar();
});
```

### Misión S03-N02-M3 · Los pedidos con permiso

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Los marineros cargan **pedidos** a la bodega y solo la capitana los despacha. Tabla
`usuario` con `es_capitan` y tabla `pedido` (`usuario_id`, `detalle`, `estado`
`pendiente` o `despachado`). Usuarios: `Kira` / `ancla123` (capitana) y `Bron` /
`timon456` (marinero). La API (todo con sesión: sin ella, 401):

- `GET/POST/DELETE /api/sesion` como en el ejemplo (el GET y el POST devuelven también
  `es_capitan`);
- `GET /api/pedidos`: la capitana ve **todos** (con el nombre de quien lo pidió); un
  marinero, **solo los suyos**;
- `POST /api/pedidos` (`detalle` obligatorio): carga un pedido propio;
- `PATCH /api/pedidos/{id}` con `{"estado": "despachado"}`: solo la capitana; a los
  demás, **403** `Solo la capitana despacha pedidos.`

La página: ingreso, `Hola, Bron (marinero)` / `Hola, Kira (capitana)`, la lista
(`#2 · 3 sogas · pendiente · de Bron`), el formulario para pedir y, **solo para la
capitana**, un botón **Despachar** en los pendientes. Recordá: esconder el botón no
alcanza, la API tiene que rechazar. Entregá el proyecto en un zip.

#### Criterio de aprobación

- La API revisa la sesión y el permiso en cada pedido (401 y 403).
- Un marinero no ve pedidos ajenos, ni en la página ni en la API.
- La página muestra el botón solo a la capitana y se actualiza al despachar.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS usuario;
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL UNIQUE,
    clave_hash VARCHAR(255) NOT NULL,
    es_capitan BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE TABLE pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    detalle VARCHAR(100) NOT NULL,
    estado ENUM('pendiente', 'despachado') NOT NULL DEFAULT 'pendiente',
    FOREIGN KEY (usuario_id) REFERENCES usuario (id)
);
INSERT INTO usuario (nombre, clave_hash, es_capitan) VALUES
    ('Kira', '$2y$10$fu7iXdxu9Ep1C8AMf0uv/OzRg7.2L3r6SXq6TzN6nIoDR03ZVFrR.', TRUE),
    ('Bron', '$2y$10$DhjPPvro3/hEguiP4g2p7u/q6XroVWbO8YFp5QUEHkA5wa.S6n9kC', FALSE),
    ('Lía', '$2y$10$dQ/7TQeRuUhQPF8fe2A3Fe/WF4CyZkuHGPgowW9ad.EKR8rVfBode', FALSE);
INSERT INTO pedido (usuario_id, detalle) VALUES (3, 'Un farol'), (2, '3 sogas');
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`router.php`
```php
<?php
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (str_starts_with($ruta, '/api/')) {
    require __DIR__ . '/api.php';
    return true;
}
return false;
```

`api.php`
```php
<?php
declare(strict_types=1);

session_set_cookie_params(['httponly' => true, 'samesite' => 'Lax']);
session_start();

$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

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
        $datos = json_decode(file_get_contents('php://input') ?: '{}', true, flags: JSON_THROW_ON_ERROR);
    } catch (JsonException) {
        responder(400, ['error' => 'El cuerpo no es un JSON válido']);
    }
    return is_array($datos) ? $datos : responder(400, ['error' => 'Se esperaba un objeto JSON']);
}

function usuario(): array
{
    return $_SESSION['usuario'] ?? responder(401, ['error' => 'Tenés que ingresar']);
}

$metodo = $_SERVER['REQUEST_METHOD'];
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($metodo !== 'GET' && !str_starts_with($_SERVER['CONTENT_TYPE'] ?? '', 'application/json')) {
    responder(415, ['error' => 'Mandá los datos como JSON']);
}

if ($ruta === '/api/sesion') {
    if ($metodo === 'GET') {
        responder(200, usuario());
    }
    if ($metodo === 'POST') {
        $d = leerJson();
        $s = $pdo->prepare('SELECT * FROM usuario WHERE nombre = ?');
        $s->execute([trim((string) ($d['nombre'] ?? ''))]);
        $u = $s->fetch();
        if (!$u || !password_verify((string) ($d['clave'] ?? ''), $u['clave_hash'])) {
            responder(401, ['error' => 'Usuario o clave incorrectos']);
        }
        session_regenerate_id(true);
        $_SESSION['usuario'] = ['id' => (int) $u['id'], 'nombre' => $u['nombre'], 'es_capitan' => (bool) $u['es_capitan']];
        responder(200, $_SESSION['usuario']);
    }
    if ($metodo === 'DELETE') {
        $_SESSION = [];
        session_destroy();
        responder(204);
    }
    responder(405, ['error' => "Método $metodo no permitido"]);
}

function pedidos(PDO $pdo, array $yo): array
{
    $sql = 'SELECT p.id, p.detalle, p.estado, u.nombre AS de FROM pedido p JOIN usuario u ON u.id = p.usuario_id';
    if ($yo['es_capitan']) {
        $s = $pdo->query("$sql ORDER BY p.id");
    } else {
        $s = $pdo->prepare("$sql WHERE p.usuario_id = ? ORDER BY p.id");
        $s->execute([$yo['id']]);
    }
    return array_map(fn ($p) => [...$p, 'id' => (int) $p['id']], $s->fetchAll());
}

if ($ruta === '/api/pedidos') {
    $yo = usuario();
    if ($metodo === 'GET') {
        responder(200, pedidos($pdo, $yo));
    }
    if ($metodo === 'POST') {
        $detalle = trim((string) (leerJson()['detalle'] ?? ''));
        if ($detalle === '' || mb_strlen($detalle) > 100) {
            responder(422, ['error' => 'Datos inválidos', 'campos' => ['detalle' => 'Escribí qué necesitás (hasta 100 letras).']]);
        }
        $pdo->prepare('INSERT INTO pedido (usuario_id, detalle) VALUES (?, ?)')->execute([$yo['id'], $detalle]);
        responder(201, ['id' => (int) $pdo->lastInsertId(), 'detalle' => $detalle, 'estado' => 'pendiente', 'de' => $yo['nombre']]);
    }
    responder(405, ['error' => "Método $metodo no permitido"]);
}

if (preg_match('#^/api/pedidos/(\d+)$#', $ruta, $m) && $metodo === 'PATCH') {
    $yo = usuario();
    if (!$yo['es_capitan']) {
        responder(403, ['error' => 'Solo la capitana despacha pedidos.']);
    }
    if ((leerJson()['estado'] ?? null) !== 'despachado') {
        responder(422, ['error' => 'Datos inválidos', 'campos' => ['estado' => 'El único cambio posible es a despachado.']]);
    }
    $s = $pdo->prepare("UPDATE pedido SET estado = 'despachado' WHERE id = ?");
    $s->execute([(int) $m[1]]);
    $s->rowCount() === 1 ? responder(204) : responder(404, ['error' => 'No existe ese pedido (o ya estaba despachado)']);
}

responder(404, ['error' => 'No existe ese recurso']);
```

`public/index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Pedidos de la bodega</title>
    <style>.aviso { color: #b00020; }</style>
</head>
<body>
    <h1>Pedidos de la bodega</h1>
    <p id="aviso" class="aviso"></p>

    <form id="form-ingreso" hidden>
        <label>Usuario <input name="nombre"></label>
        <label>Clave <input name="clave" type="password"></label>
        <button>Entrar</button>
    </form>

    <section id="panel" hidden>
        <p><span id="saludo"></span> · <button id="salir">Salir</button></p>
        <form id="form-pedido">
            <input name="detalle" placeholder="¿Qué necesitás?" autocomplete="off">
            <button>Pedir</button>
        </form>
        <ul id="pedidos"></ul>
    </section>

    <script src="app.js"></script>
</body>
</html>
```

`public/app.js`
```js
class ErrorApi extends Error {
    constructor(estado, cuerpo) {
        super(cuerpo?.error ?? `el servidor respondió ${estado}`);
        this.estado = estado;
        this.campos = cuerpo?.campos ?? {};
    }
}

async function api(metodo, ruta, datos) {
    const respuesta = await fetch(ruta, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: datos === undefined ? undefined : JSON.stringify(datos),
    });
    const cuerpo = respuesta.status === 204 ? null : await respuesta.json();
    if (!respuesta.ok) {
        throw new ErrorApi(respuesta.status, cuerpo);
    }
    return cuerpo;
}

const estado = { yo: null, pedidos: [] };
const aviso = document.querySelector('#aviso');
const formIngreso = document.querySelector('#form-ingreso');
const panel = document.querySelector('#panel');
const lista = document.querySelector('#pedidos');

function itemPedido(pedido) {
    const li = document.createElement('li');
    li.dataset.id = pedido.id;
    li.append(`#${pedido.id} · ${pedido.detalle} · ${pedido.estado} · de ${pedido.de}`);
    if (estado.yo.es_capitan && pedido.estado === 'pendiente') {
        const boton = document.createElement('button');
        boton.textContent = 'Despachar';
        li.append(' ', boton);
    }
    return li;
}

function dibujar() {
    formIngreso.hidden = estado.yo !== null;
    panel.hidden = estado.yo === null;
    if (estado.yo) {
        const rol = estado.yo.es_capitan ? 'capitana' : 'marinero';
        document.querySelector('#saludo').textContent = `Hola, ${estado.yo.nombre} (${rol})`;
        lista.replaceChildren(...estado.pedidos.map(itemPedido));
    }
}

async function entrar(yo) {
    estado.yo = yo;
    estado.pedidos = await api('GET', '/api/pedidos');
    dibujar();
}

function atender(error) {
    if (error.estado === 401) {
        estado.yo = null;
        dibujar();
    }
    aviso.textContent = error.message;
}

formIngreso.addEventListener('submit', async (evento) => {
    evento.preventDefault();
    try {
        await entrar(await api('POST', '/api/sesion', Object.fromEntries(new FormData(formIngreso))));
        formIngreso.reset();
        aviso.textContent = '';
    } catch (error) {
        aviso.textContent = error.message;
    }
});

document.querySelector('#form-pedido').addEventListener('submit', async (evento) => {
    evento.preventDefault();
    try {
        estado.pedidos.push(await api('POST', '/api/pedidos', Object.fromEntries(new FormData(evento.target))));
        evento.target.reset();
        aviso.textContent = '';
        dibujar();
    } catch (error) {
        aviso.textContent = error.campos.detalle ?? '';
        if (error.estado !== 422) {
            atender(error);
        }
    }
});

lista.addEventListener('click', async (evento) => {
    if (!evento.target.matches('button')) {
        return;
    }
    const id = Number(evento.target.closest('li').dataset.id);
    try {
        await api('PATCH', `/api/pedidos/${id}`, { estado: 'despachado' });
        estado.pedidos = estado.pedidos.map((p) => (p.id === id ? { ...p, estado: 'despachado' } : p));
        dibujar();
    } catch (error) {
        atender(error);
    }
});

document.querySelector('#salir').addEventListener('click', async () => {
    await api('DELETE', '/api/sesion');
    estado.yo = null;
    dibujar();
});

api('GET', '/api/sesion')
    .then(entrar)
    .catch(() => {
        estado.yo = null;
        dibujar();
    });
```

### Encargo S03-N02-E1 · Las tareas del muelle

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Una lista de **tareas del muelle** guardada en MariaDB (`tarea`: `texto`, `hecha`). La
API: `GET /api/tareas`, `POST /api/tareas` (`texto` obligatorio, hasta 100 letras:
`Escribí la tarea (hasta 100 letras).`), `PATCH /api/tareas/{id}` con `{"hecha": true}`
o `false`, y `DELETE /api/tareas/{id}`.

La página, con estado y `dibujar()`:

- un formulario para agregar (el error, al lado);
- cada tarea con una **casilla** (`checkbox`) para marcarla hecha (tachada con la clase
  `hecha`) y un botón **Borrar**;
- tres botones de filtro, **Todas**, **Pendientes** y **Hechas**, que filtran en la
  página sin pedir de nuevo (el activo lleva la clase `activo`);
- el contador `2 pendientes · 1 hecha` (con singular y plural bien puestos).

Entregá el proyecto en un zip.

#### Criterio de aprobación

- Cada acción pasa por la API y después actualiza el estado y redibuja.
- Los filtros no piden nada a la API.
- El contador respeta singular y plural, y la validación llega hasta la página.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS tarea;
CREATE TABLE tarea (id INT AUTO_INCREMENT PRIMARY KEY, texto VARCHAR(100) NOT NULL, hecha BOOLEAN NOT NULL DEFAULT FALSE);
INSERT INTO tarea (texto, hecha) VALUES ('Baldear la cubierta', FALSE), ('Revisar amarras', TRUE), ('Cargar agua', FALSE);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`router.php`
```php
<?php
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (str_starts_with($ruta, '/api/')) {
    require __DIR__ . '/api.php';
    return true;
}
return false;
```

`api.php`
```php
<?php
declare(strict_types=1);

$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

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
        $datos = json_decode(file_get_contents('php://input') ?: '{}', true, flags: JSON_THROW_ON_ERROR);
    } catch (JsonException) {
        responder(400, ['error' => 'El cuerpo no es un JSON válido']);
    }
    return is_array($datos) ? $datos : responder(400, ['error' => 'Se esperaba un objeto JSON']);
}

function comoJson(array $t): array
{
    return ['id' => (int) $t['id'], 'texto' => $t['texto'], 'hecha' => (bool) $t['hecha']];
}

$metodo = $_SERVER['REQUEST_METHOD'];
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($metodo !== 'GET' && !str_starts_with($_SERVER['CONTENT_TYPE'] ?? '', 'application/json')) {
    responder(415, ['error' => 'Mandá los datos como JSON']);
}

if ($ruta === '/api/tareas') {
    if ($metodo === 'GET') {
        responder(200, array_map('comoJson', $pdo->query('SELECT * FROM tarea ORDER BY id')->fetchAll()));
    }
    if ($metodo === 'POST') {
        $texto = trim((string) (leerJson()['texto'] ?? ''));
        if ($texto === '' || mb_strlen($texto) > 100) {
            responder(422, ['error' => 'Datos inválidos', 'campos' => ['texto' => 'Escribí la tarea (hasta 100 letras).']]);
        }
        $pdo->prepare('INSERT INTO tarea (texto) VALUES (?)')->execute([$texto]);
        responder(201, ['id' => (int) $pdo->lastInsertId(), 'texto' => $texto, 'hecha' => false]);
    }
    responder(405, ['error' => "Método $metodo no permitido"]);
}

if (preg_match('#^/api/tareas/(\d+)$#', $ruta, $m)) {
    $id = (int) $m[1];
    $s = $pdo->prepare('SELECT * FROM tarea WHERE id = ?');
    $s->execute([$id]);
    $tarea = $s->fetch() ?: responder(404, ['error' => 'No existe esa tarea']);
    if ($metodo === 'PATCH') {
        $hecha = leerJson()['hecha'] ?? null;
        if (!is_bool($hecha)) {
            responder(422, ['error' => 'Datos inválidos', 'campos' => ['hecha' => 'Tiene que ser true o false.']]);
        }
        $pdo->prepare('UPDATE tarea SET hecha = ? WHERE id = ?')->execute([(int) $hecha, $id]);
        responder(200, comoJson([...$tarea, 'hecha' => $hecha]));
    }
    if ($metodo === 'DELETE') {
        $pdo->prepare('DELETE FROM tarea WHERE id = ?')->execute([$id]);
        responder(204);
    }
    responder(405, ['error' => "Método $metodo no permitido"]);
}

responder(404, ['error' => 'No existe ese recurso']);
```

`public/index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Tareas del muelle</title>
    <style>
        .hecha span { text-decoration: line-through; }
        .activo { font-weight: bold; }
        .error { color: #b00020; }
    </style>
</head>
<body>
    <h1>Tareas del muelle</h1>
    <form id="nueva">
        <input name="texto" placeholder="Nueva tarea…" autocomplete="off">
        <button>Agregar</button>
        <small id="error" class="error"></small>
    </form>
    <nav id="filtros">
        <button data-filtro="todas">Todas</button>
        <button data-filtro="pendientes">Pendientes</button>
        <button data-filtro="hechas">Hechas</button>
    </nav>
    <p id="contador"></p>
    <ul id="tareas"></ul>
    <script src="app.js"></script>
</body>
</html>
```

`public/app.js`
```js
class ErrorApi extends Error {
    constructor(estado, cuerpo) {
        super(cuerpo?.error ?? `el servidor respondió ${estado}`);
        this.estado = estado;
        this.campos = cuerpo?.campos ?? {};
    }
}

async function api(metodo, ruta, datos) {
    const respuesta = await fetch(ruta, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: datos === undefined ? undefined : JSON.stringify(datos),
    });
    const cuerpo = respuesta.status === 204 ? null : await respuesta.json();
    if (!respuesta.ok) {
        throw new ErrorApi(respuesta.status, cuerpo);
    }
    return cuerpo;
}

const estado = { tareas: [], filtro: 'todas' };
const lista = document.querySelector('#tareas');
const formulario = document.querySelector('#nueva');
const error = document.querySelector('#error');

const plural = (n, singular, varias) => `${n} ${n === 1 ? singular : varias}`;

function itemTarea(tarea) {
    const li = document.createElement('li');
    li.dataset.id = tarea.id;
    li.classList.toggle('hecha', tarea.hecha);
    const casilla = document.createElement('input');
    casilla.type = 'checkbox';
    casilla.checked = tarea.hecha;
    const texto = document.createElement('span');
    texto.textContent = tarea.texto;
    const borrar = document.createElement('button');
    borrar.textContent = 'Borrar';
    li.append(casilla, ' ', texto, ' ', borrar);
    return li;
}

function dibujar() {
    const visibles = estado.tareas.filter((t) =>
        estado.filtro === 'todas' || (estado.filtro === 'hechas') === t.hecha);
    lista.replaceChildren(...visibles.map(itemTarea));
    const hechas = estado.tareas.filter((t) => t.hecha).length;
    document.querySelector('#contador').textContent =
        `${plural(estado.tareas.length - hechas, 'pendiente', 'pendientes')} · ${plural(hechas, 'hecha', 'hechas')}`;
    for (const boton of document.querySelectorAll('#filtros button')) {
        boton.classList.toggle('activo', boton.dataset.filtro === estado.filtro);
    }
}

formulario.addEventListener('submit', async (evento) => {
    evento.preventDefault();
    error.textContent = '';
    try {
        estado.tareas.push(await api('POST', '/api/tareas', Object.fromEntries(new FormData(formulario))));
        formulario.reset();
        dibujar();
    } catch (e) {
        error.textContent = e.campos.texto ?? e.message;
    }
});

lista.addEventListener('click', async (evento) => {
    const li = evento.target.closest('li');
    if (!li || !evento.target.matches('input, button')) {
        return;
    }
    const id = Number(li.dataset.id);
    try {
        if (evento.target.matches('input')) {
            const actualizada = await api('PATCH', `/api/tareas/${id}`, { hecha: evento.target.checked });
            estado.tareas = estado.tareas.map((t) => (t.id === id ? actualizada : t));
        } else {
            await api('DELETE', `/api/tareas/${id}`);
            estado.tareas = estado.tareas.filter((t) => t.id !== id);
        }
    } catch (e) {
        error.textContent = e.message;
    }
    dibujar();
});

document.querySelector('#filtros').addEventListener('click', (evento) => {
    if (evento.target.dataset.filtro) {
        estado.filtro = evento.target.dataset.filtro;
        dibujar();
    }
});

api('GET', '/api/tareas').then((tareas) => {
    estado.tareas = tareas;
    dibujar();
});
```

### Prueba del sello

#### ¿Para qué sirve `evento.preventDefault()` en el `submit` de un formulario?

Para frenar el envío normal (que recarga la página) y mandar los datos nosotros con `fetch`.

#### ¿Qué tiene que hacer la página cuando la API responde 422?

Mostrar cada mensaje de `campos` al lado del campo que lo causó, sin perder lo que el usuario escribió.

#### ¿Cómo sabe la API quién hizo el pedido si `fetch` no manda el usuario?

Por la cookie de sesión: el navegador la guarda al ingresar y `fetch` la manda sola en cada pedido al mismo sitio.

#### ¿Por qué rechazar lo que no llega como JSON protege contra CSRF?

Porque un formulario de otro sitio no puede mandar `Content-Type: application/json`, y un `fetch` de otro sitio con ese encabezado necesita un permiso (CORS) que la API no da.

#### Si la página no muestra el botón Despachar a un marinero, ¿alcanza?

No: cualquiera puede mandar el pedido a la API con `curl`. La API tiene que revisar el permiso y responder 403.

### Soluciones (docente)

Sale de `22-JS-Vanilla` (09-Eventos, 15-Async-Await-Fetch, 16-JSON, 17-Manejo-Errores), sobre las sesiones y el login de R03 y la API de R05-N03. Cada solución se verifica con el SQL cargado, `php -S … -t public router.php` y un navegador real (Chromium) que ingresa, carga, edita y borra, además de pedidos directos a la API (401, 403, 404, 415). Para corregir, usar la página con F12 abierto y probar el 403 con `curl` o desde la consola.

## S03-N03 · Jefe del Palomar: el Leviatán de los Mensajes

```meta
tipo: jefe
padre: S03-N02
precio: 10
criatura: dragon
ejecutable: no
insignia: Mensajero Veloz
insignia_descripcion: Venciste al Leviatán de los Mensajes: construiste aplicaciones de una sola página que conversan en vivo con tu API de PHP y MariaDB.
usa: js.fetch, js.formularios, sql.modelo
```

### Crónica

Una tarde el mar se levanta frente al palomar y asoma el **Leviatán de los Mensajes**: una serpiente enorme que se traga las palomas en pleno vuelo, confunde las respuestas y manda cien pedidos por segundo para tapar la torre. Las páginas que dependen de recargar se quedan mudas; las que no revisan lo que reciben muestran cualquier cosa.

—Hoy tus páginas tienen que ser rápidas y tercas, {heroe} —dice {mentor}—. Que se enteren solas de lo nuevo, que no se traben si un pedido tarda, que la base no acepte lo imposible aunque dos personas aprieten el botón a la vez, y que la torre sepa decir "esperá" cuando la inundan. Así se espanta un Leviatán.

### Objetivos

- Construir dos aplicaciones de una sola página sobre una API de PHP con MariaDB.
- Dejar que la base de datos garantice las reglas (restricciones `UNIQUE`) y convertir sus errores en mensajes claros.
- Mantener una página actualizada con consultas periódicas (*polling*) sin pedidos superpuestos.
- Limitar la cantidad de pedidos (429) para proteger el servidor.

### Antes de empezar

- Toda la Senda de los Mensajes Veloces.

### Explicación

#### Que la base cuide la regla
"Un muelle, una reserva por día" se puede revisar con un `SELECT` antes del `INSERT`…
pero si dos personas reservan en el mismo instante, las dos ven el muelle libre y las
dos insertan. La forma segura es que **la base** lo impida con una restricción:
```sql
UNIQUE KEY un_barco_por_dia (muelle_id, fecha)
```
El segundo `INSERT` falla con el error **1062** (clave duplicada), que la API convierte
en un 422 con un mensaje claro, como ya hiciste con los nombres repetidos.

#### Enterarse de lo nuevo: *polling*
Un chat necesita mostrar los mensajes de los demás sin que nadie recargue. En un
hosting compartido (sin procesos que queden corriendo) la forma más simple es
**preguntar cada tanto**:
```js
let ultimoId = 0;
let pidiendo = false;

async function traerNuevos() {
    if (pidiendo) return;                 // si el pedido anterior no volvió, no se apila otro
    pidiendo = true;
    try {
        const nuevos = await api('GET', `/api/mensajes?desde=${ultimoId}`);
        ...                               // agregar a la lista
        ultimoId = nuevos.at(-1)?.id ?? ultimoId;
    } finally {
        pidiendo = false;
    }
}
const reloj = setInterval(traerNuevos, 1000);   // cada segundo
clearInterval(reloj);                            // para frenarlo (al salir)
```
El parámetro `desde` hace que cada pedido traiga **solo lo nuevo**: la API responde
`WHERE id > ?`, que con la clave primaria es instantáneo.

#### Decir "esperá": el código 429
Si alguien manda cien mensajes por segundo, la API responde **429 Too Many Requests**.
Contar cuántos mandó en los últimos segundos es una consulta:
```sql
SELECT COUNT(*) FROM mensaje WHERE autor = ? AND creado > NOW() - INTERVAL 10 SECOND
```
(con un índice en `(autor, creado)`). La página muestra el mensaje y no reintenta sola.

#### Fechas entre el navegador y PHP
Un `<input type="date">` da y recibe la fecha como `2026-10-03`, el mismo formato de
MariaDB: viaja así en el JSON y solo se convierte a `03/10/2026` para mostrarla.

### Misión S03-N03-M1 · El tablero de los muelles

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 40
```

#### Consigna

El **tablero de reservas** de los muelles, en una sola página. La base tiene `muelle`
(`nombre`, `calado` máximo: Norte 8,5 m, Este 12 m, Sur 5 m) y `reserva` (`muelle_id`,
`barco`, `fecha`, `calado`) con una restricción **única** por muelle y fecha. La API:

- `GET /api/tablero?fecha=2026-10-03`: los muelles por nombre, cada uno con su reserva
  de ese día o `null`; 400 si la fecha no es válida.
- `POST /api/reservas`: valida (422 con `campos`) que el barco no esté vacío
  (`Poné el nombre del barco.`), que la fecha no haya pasado
  (`No se reserva para un día que ya pasó.`), que el calado vaya de 1 a 20
  (`El calado va de 1 a 20 metros.`), que el muelle exista y que el barco entre
  (`El muelle Sur admite hasta 5,0 m de calado.`). Si el muelle ya está ocupado ese
  día, el error **1062** se convierte en `Ese muelle ya está reservado para ese día.`
- `DELETE /api/reservas/{id}`: 204, o 404.

La página tiene un `<input type="date">` que empieza en **hoy**; al cambiarlo, el
tablero se vuelve a pedir. Cada muelle se muestra como `Muelle Este · hasta 12,0 m ·
Libre` o `Muelle Norte · hasta 8,5 m · Albatros (6,5 m)` con un botón **Cancelar**;
arriba, `2 de 3 muelles libres`. El formulario (muelle, barco, calado) reserva para el
día elegido, muestra los errores al lado de cada campo y, si sale bien,
`Reserva confirmada: Albatros en el muelle Norte el 03/10/2026.` y redibuja el tablero.
Entregá el proyecto en un zip.

#### Criterio de aprobación

- La regla "una reserva por muelle y día" la garantiza un `UNIQUE` de la base, y la API traduce el 1062.
- La página no se recarga nunca: cambiar de día, reservar y cancelar redibujan el tablero.
- Los errores de cada campo aparecen al lado del campo.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS reserva;
DROP TABLE IF EXISTS muelle;
CREATE TABLE muelle (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(30) NOT NULL UNIQUE, calado DECIMAL(4, 1) NOT NULL);
CREATE TABLE reserva (
    id INT AUTO_INCREMENT PRIMARY KEY,
    muelle_id INT NOT NULL,
    barco VARCHAR(40) NOT NULL,
    fecha DATE NOT NULL,
    calado DECIMAL(4, 1) NOT NULL,
    UNIQUE KEY un_barco_por_dia (muelle_id, fecha),
    FOREIGN KEY (muelle_id) REFERENCES muelle (id)
);
INSERT INTO muelle (nombre, calado) VALUES ('Norte', 8.5), ('Este', 12), ('Sur', 5);
INSERT INTO reserva (muelle_id, barco, fecha, calado) VALUES
    (1, 'Gaviota', CURDATE() + INTERVAL 1 DAY, 3),
    (2, 'Estrella del Sur', CURDATE(), 9.5);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`router.php`
```php
<?php
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (str_starts_with($ruta, '/api/')) {
    require __DIR__ . '/api.php';
    return true;
}
return false;
```

`api.php`
```php
<?php
declare(strict_types=1);

$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

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
        $datos = json_decode(file_get_contents('php://input') ?: '{}', true, flags: JSON_THROW_ON_ERROR);
    } catch (JsonException) {
        responder(400, ['error' => 'El cuerpo no es un JSON válido']);
    }
    return is_array($datos) ? $datos : responder(400, ['error' => 'Se esperaba un objeto JSON']);
}

function fechaValida(mixed $texto): ?DateTimeImmutable
{
    if (!is_string($texto)) {
        return null;
    }
    $fecha = DateTimeImmutable::createFromFormat('!Y-m-d', $texto);
    return $fecha && $fecha->format('Y-m-d') === $texto ? $fecha : null;
}

function invalido(array $campos): never
{
    responder(422, ['error' => 'Datos inválidos', 'campos' => $campos]);
}

$metodo = $_SERVER['REQUEST_METHOD'];
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($metodo !== 'GET' && !str_starts_with($_SERVER['CONTENT_TYPE'] ?? '', 'application/json')) {
    responder(415, ['error' => 'Mandá los datos como JSON']);
}

if ($ruta === '/api/tablero' && $metodo === 'GET') {
    $fecha = fechaValida($_GET['fecha'] ?? '') ?? responder(400, ['error' => 'La fecha tiene que ser AAAA-MM-DD']);
    $s = $pdo->prepare(
        'SELECT m.id, m.nombre, m.calado, r.id AS reserva_id, r.barco, r.calado AS calado_barco
         FROM muelle m LEFT JOIN reserva r ON r.muelle_id = m.id AND r.fecha = ?
         ORDER BY m.nombre'
    );
    $s->execute([$fecha->format('Y-m-d')]);
    responder(200, array_map(fn ($f) => [
        'id' => (int) $f['id'],
        'nombre' => $f['nombre'],
        'calado' => (float) $f['calado'],
        'reserva' => $f['reserva_id'] === null ? null
            : ['id' => (int) $f['reserva_id'], 'barco' => $f['barco'], 'calado' => (float) $f['calado_barco']],
    ], $s->fetchAll()));
}

if ($ruta === '/api/reservas' && $metodo === 'POST') {
    $d = leerJson();
    $barco = trim((string) ($d['barco'] ?? ''));
    $fecha = fechaValida($d['fecha'] ?? null);
    $calado = $d['calado'] ?? null;

    $errores = [];
    if ($barco === '' || mb_strlen($barco) > 40) {
        $errores['barco'] = 'Poné el nombre del barco.';
    }
    if ($fecha === null) {
        $errores['fecha'] = 'Esa fecha no es válida.';
    } elseif ($fecha < new DateTimeImmutable('today')) {
        $errores['fecha'] = 'No se reserva para un día que ya pasó.';
    }
    if ((!is_int($calado) && !is_float($calado)) || $calado < 1 || $calado > 20) {
        $errores['calado'] = 'El calado va de 1 a 20 metros.';
    }
    $s = $pdo->prepare('SELECT * FROM muelle WHERE id = ?');
    $s->execute([(int) ($d['muelle_id'] ?? 0)]);
    $muelle = $s->fetch();
    if (!$muelle) {
        $errores['muelle_id'] = 'Ese muelle no existe.';
    } elseif (!isset($errores['calado']) && $calado > (float) $muelle['calado']) {
        $maximo = number_format((float) $muelle['calado'], 1, ',', '.');
        $errores['calado'] = "El muelle {$muelle['nombre']} admite hasta $maximo m de calado.";
    }
    if ($errores !== []) {
        invalido($errores);
    }

    try {
        $pdo->prepare('INSERT INTO reserva (muelle_id, barco, fecha, calado) VALUES (?, ?, ?, ?)')
            ->execute([$muelle['id'], $barco, $fecha->format('Y-m-d'), $calado]);
    } catch (PDOException $e) {
        if (($e->errorInfo[1] ?? null) === 1062) {
            invalido(['muelle_id' => 'Ese muelle ya está reservado para ese día.']);
        }
        throw $e;
    }
    responder(201, [
        'id' => (int) $pdo->lastInsertId(),
        'mensaje' => "Reserva confirmada: $barco en el muelle {$muelle['nombre']} el {$fecha->format('d/m/Y')}.",
    ]);
}

if (preg_match('#^/api/reservas/(\d+)$#', $ruta, $m) && $metodo === 'DELETE') {
    $s = $pdo->prepare('DELETE FROM reserva WHERE id = ?');
    $s->execute([(int) $m[1]]);
    $s->rowCount() === 1 ? responder(204) : responder(404, ['error' => 'Esa reserva ya no existe.']);
}

responder(404, ['error' => 'No existe ese recurso']);
```

`public/index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Tablero de los muelles</title>
    <style>.error { color: #b00020; display: block; }</style>
</head>
<body>
    <h1>Tablero de los muelles</h1>
    <label>Día <input type="date" id="fecha"></label>
    <p id="libres"></p>
    <ul id="tablero"></ul>

    <h2>Reservar</h2>
    <form id="reservar">
        <label>Muelle <select name="muelle_id"></select></label>
        <small class="error" data-campo="muelle_id"></small>
        <label>Barco <input name="barco" autocomplete="off"></label>
        <small class="error" data-campo="barco"></small>
        <label>Calado (m) <input name="calado" inputmode="decimal"></label>
        <small class="error" data-campo="calado"></small>
        <small class="error" data-campo="fecha"></small>
        <button>Reservar</button>
    </form>
    <p id="aviso"></p>
    <script src="app.js"></script>
</body>
</html>
```

`public/app.js`
```js
class ErrorApi extends Error {
    constructor(estado, cuerpo) {
        super(cuerpo?.error ?? `el servidor respondió ${estado}`);
        this.estado = estado;
        this.campos = cuerpo?.campos ?? {};
    }
}

async function api(metodo, ruta, datos) {
    const respuesta = await fetch(ruta, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: datos === undefined ? undefined : JSON.stringify(datos),
    });
    const cuerpo = respuesta.status === 204 ? null : await respuesta.json();
    if (!respuesta.ok) {
        throw new ErrorApi(respuesta.status, cuerpo);
    }
    return cuerpo;
}

const estado = { fecha: '', muelles: [] };
const selectorFecha = document.querySelector('#fecha');
const tablero = document.querySelector('#tablero');
const formulario = document.querySelector('#reservar');
const aviso = document.querySelector('#aviso');

const metros = (n) => n.toLocaleString('es-AR', { minimumFractionDigits: 1, maximumFractionDigits: 1 });

function hoy() {
    const d = new Date();
    return [d.getFullYear(), String(d.getMonth() + 1).padStart(2, '0'), String(d.getDate()).padStart(2, '0')].join('-');
}

function itemMuelle(muelle) {
    const li = document.createElement('li');
    const ocupacion = muelle.reserva === null ? 'Libre' : `${muelle.reserva.barco} (${metros(muelle.reserva.calado)} m)`;
    li.append(`Muelle ${muelle.nombre} · hasta ${metros(muelle.calado)} m · ${ocupacion}`);
    if (muelle.reserva !== null) {
        const boton = document.createElement('button');
        boton.textContent = 'Cancelar';
        boton.dataset.reserva = muelle.reserva.id;
        li.append(' ', boton);
    }
    return li;
}

function dibujar() {
    tablero.replaceChildren(...estado.muelles.map(itemMuelle));
    const libres = estado.muelles.filter((m) => m.reserva === null).length;
    document.querySelector('#libres').textContent = `${libres} de ${estado.muelles.length} muelles libres`;
    const selector = formulario.querySelector('[name=muelle_id]');
    const elegido = selector.value;
    selector.replaceChildren(...estado.muelles.map((m) => new Option(m.nombre, m.id)));
    selector.value = elegido || selector.value;
}

async function cargar() {
    estado.fecha = selectorFecha.value;
    estado.muelles = await api('GET', `/api/tablero?fecha=${estado.fecha}`);
    dibujar();
}

function mostrarErrores(campos) {
    for (const lugar of formulario.querySelectorAll('[data-campo]')) {
        lugar.textContent = campos[lugar.dataset.campo] ?? '';
    }
}

formulario.addEventListener('submit', async (evento) => {
    evento.preventDefault();
    const datos = Object.fromEntries(new FormData(formulario));
    mostrarErrores({});
    aviso.textContent = '';
    try {
        const calado = datos.calado.trim() === '' ? null : Number(datos.calado.replace(',', '.'));
        const r = await api('POST', '/api/reservas', { ...datos, muelle_id: Number(datos.muelle_id), calado, fecha: estado.fecha });
        aviso.textContent = r.mensaje;
        formulario.querySelector('[name=barco]').value = '';
        formulario.querySelector('[name=calado]').value = '';
        await cargar();
    } catch (error) {
        if (error.estado === 422) {
            mostrarErrores(error.campos);
        } else {
            aviso.textContent = error.message;
        }
    }
});

tablero.addEventListener('click', async (evento) => {
    const id = evento.target.dataset.reserva;
    if (!id || !confirm('¿Cancelar la reserva?')) {
        return;
    }
    try {
        await api('DELETE', `/api/reservas/${id}`);
        aviso.textContent = 'Reserva cancelada.';
    } catch (error) {
        aviso.textContent = error.message;
    }
    await cargar();
});

selectorFecha.addEventListener('change', cargar);
selectorFecha.value = hoy();
cargar();
```

### Misión S03-N03-M2 · El chat del puerto

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 40
```

#### Consigna

El **chat del puerto**: cualquiera entra con un nombre y conversa con los demás en vivo.
La API (con sesión):

- `POST /api/sesion` con `{"nombre": "Kira"}`: de 2 a 20 letras, números o espacios
  (`El nombre tiene de 2 a 20 letras o números.`); `GET` devuelve quién sos o 401;
  `DELETE` sale.
- `GET /api/mensajes?desde=ID`: los mensajes con id mayor que `ID`, en orden, hasta 50,
  cada uno con `id`, `autor`, `texto` y `hora` (`HH:MM`). Sin sesión, 401.
- `POST /api/mensajes` con `{"texto": "..."}`: de 1 a 200 letras
  (`El mensaje tiene de 1 a 200 letras.`). Si el autor ya mandó **3 mensajes en los
  últimos 10 segundos**, responde **429** `Esperá unos segundos antes de mandar otro mensaje.`

La página: el ingreso con el nombre y, adentro, la lista de mensajes
(`[14:05] Kira: hola`, los propios con la clase `mio`), el campo para escribir y **Salir**.
Pide los mensajes nuevos **cada segundo** (sin pedidos superpuestos y usando `desde`),
nunca muestra un mensaje dos veces, muestra el texto **tal cual** (un mensaje con
`<b>` se ve con los signos) y, al mandar, pide enseguida los nuevos en lugar de
esperar. Si la API responde 429 o 422, muestra el mensaje; si responde 401, vuelve al
ingreso. Al salir, frena las consultas. Probalo con dos navegadores. Entregá el
proyecto en un zip.

#### Criterio de aprobación

- La API usa `desde` con `WHERE id > ?` y cuenta los envíos recientes con una consulta (429).
- La página consulta con `setInterval`, no superpone pedidos, no duplica mensajes y frena al salir.
- Los mensajes se muestran con `textContent`.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS mensaje;
CREATE TABLE mensaje (
    id INT AUTO_INCREMENT PRIMARY KEY,
    autor VARCHAR(20) NOT NULL,
    texto VARCHAR(200) NOT NULL,
    creado DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX autor_creado (autor, creado)
);
INSERT INTO mensaje (autor, texto, creado) VALUES ('Elefa', 'Bienvenidos al chat del puerto', NOW() - INTERVAL 1 HOUR);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`router.php`
```php
<?php
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (str_starts_with($ruta, '/api/')) {
    require __DIR__ . '/api.php';
    return true;
}
return false;
```

`api.php`
```php
<?php
declare(strict_types=1);

session_set_cookie_params(['httponly' => true, 'samesite' => 'Lax']);
session_start();

$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

const LIMITE_MENSAJES = 3;
const LIMITE_SEGUNDOS = 10;

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
        $datos = json_decode(file_get_contents('php://input') ?: '{}', true, flags: JSON_THROW_ON_ERROR);
    } catch (JsonException) {
        responder(400, ['error' => 'El cuerpo no es un JSON válido']);
    }
    return is_array($datos) ? $datos : responder(400, ['error' => 'Se esperaba un objeto JSON']);
}

function autor(): string
{
    return $_SESSION['autor'] ?? responder(401, ['error' => 'Entrá con tu nombre']);
}

function comoJson(array $m): array
{
    return ['id' => (int) $m['id'], 'autor' => $m['autor'], 'texto' => $m['texto'], 'hora' => $m['hora']];
}

$metodo = $_SERVER['REQUEST_METHOD'];
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($metodo !== 'GET' && !str_starts_with($_SERVER['CONTENT_TYPE'] ?? '', 'application/json')) {
    responder(415, ['error' => 'Mandá los datos como JSON']);
}

if ($ruta === '/api/sesion') {
    if ($metodo === 'GET') {
        responder(200, ['nombre' => autor()]);
    }
    if ($metodo === 'POST') {
        $nombre = trim((string) (leerJson()['nombre'] ?? ''));
        if (!preg_match('/^[\p{L}\d ]{2,20}$/u', $nombre)) {
            responder(422, ['error' => 'Datos inválidos', 'campos' => ['nombre' => 'El nombre tiene de 2 a 20 letras o números.']]);
        }
        session_regenerate_id(true);
        $_SESSION['autor'] = $nombre;
        responder(200, ['nombre' => $nombre]);
    }
    if ($metodo === 'DELETE') {
        $_SESSION = [];
        session_destroy();
        responder(204);
    }
    responder(405, ['error' => "Método $metodo no permitido"]);
}

if ($ruta === '/api/mensajes') {
    $autor = autor();
    if ($metodo === 'GET') {
        $s = $pdo->prepare("SELECT id, autor, texto, DATE_FORMAT(creado, '%H:%i') AS hora
                            FROM mensaje WHERE id > ? ORDER BY id LIMIT 50");
        $s->execute([max(0, (int) ($_GET['desde'] ?? 0))]);
        responder(200, array_map('comoJson', $s->fetchAll()));
    }
    if ($metodo === 'POST') {
        $texto = trim((string) (leerJson()['texto'] ?? ''));
        if ($texto === '' || mb_strlen($texto) > 200) {
            responder(422, ['error' => 'Datos inválidos', 'campos' => ['texto' => 'El mensaje tiene de 1 a 200 letras.']]);
        }
        $s = $pdo->prepare('SELECT COUNT(*) FROM mensaje WHERE autor = ? AND creado > NOW() - INTERVAL ? SECOND');
        $s->execute([$autor, LIMITE_SEGUNDOS]);
        if ((int) $s->fetchColumn() >= LIMITE_MENSAJES) {
            header('Retry-After: ' . LIMITE_SEGUNDOS);
            responder(429, ['error' => 'Esperá unos segundos antes de mandar otro mensaje.']);
        }
        $pdo->prepare('INSERT INTO mensaje (autor, texto) VALUES (?, ?)')->execute([$autor, $texto]);
        responder(201, ['id' => (int) $pdo->lastInsertId()]);
    }
    responder(405, ['error' => "Método $metodo no permitido"]);
}

responder(404, ['error' => 'No existe ese recurso']);
```

`public/index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Chat del puerto</title>
    <style>
        .mio { font-weight: bold; }
        .aviso { color: #b00020; }
        #mensajes { max-height: 60vh; overflow-y: auto; }
    </style>
</head>
<body>
    <h1>Chat del puerto</h1>
    <p id="aviso" class="aviso"></p>

    <form id="form-ingreso" hidden>
        <label>Tu nombre <input name="nombre" autocomplete="off"></label>
        <button>Entrar</button>
    </form>

    <section id="chat" hidden>
        <p><span id="saludo"></span> · <button id="salir">Salir</button></p>
        <ul id="mensajes"></ul>
        <form id="form-mensaje">
            <input name="texto" placeholder="Escribí un mensaje…" autocomplete="off">
            <button>Mandar</button>
        </form>
    </section>

    <script src="app.js"></script>
</body>
</html>
```

`public/app.js`
```js
class ErrorApi extends Error {
    constructor(estado, cuerpo) {
        super(cuerpo?.error ?? `el servidor respondió ${estado}`);
        this.estado = estado;
        this.campos = cuerpo?.campos ?? {};
    }
}

async function api(metodo, ruta, datos) {
    const respuesta = await fetch(ruta, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: datos === undefined ? undefined : JSON.stringify(datos),
    });
    const cuerpo = respuesta.status === 204 ? null : await respuesta.json();
    if (!respuesta.ok) {
        throw new ErrorApi(respuesta.status, cuerpo);
    }
    return cuerpo;
}

const aviso = document.querySelector('#aviso');
const formIngreso = document.querySelector('#form-ingreso');
const chat = document.querySelector('#chat');
const lista = document.querySelector('#mensajes');
const formMensaje = document.querySelector('#form-mensaje');

const estado = { yo: null, ultimoId: 0, pidiendo: false, reloj: null };

function mostrarIngreso(mensaje = '') {
    clearInterval(estado.reloj);
    estado.yo = null;
    chat.hidden = true;
    formIngreso.hidden = false;
    aviso.textContent = mensaje;
}

function itemMensaje(m) {
    const li = document.createElement('li');
    li.textContent = `[${m.hora}] ${m.autor}: ${m.texto}`;
    li.classList.toggle('mio', m.autor === estado.yo);
    return li;
}

async function traerNuevos() {
    if (estado.pidiendo || estado.yo === null) {
        return;
    }
    estado.pidiendo = true;
    try {
        const nuevos = await api('GET', `/api/mensajes?desde=${estado.ultimoId}`);
        if (nuevos.length > 0) {
            lista.append(...nuevos.map(itemMensaje));
            estado.ultimoId = nuevos.at(-1).id;
            lista.scrollTop = lista.scrollHeight;
        }
    } catch (error) {
        if (error.estado === 401) {
            mostrarIngreso('Tu sesión terminó: entrá de nuevo.');
        }
    } finally {
        estado.pidiendo = false;
    }
}

function entrar(nombre) {
    estado.yo = nombre;
    estado.ultimoId = 0;
    lista.replaceChildren();
    document.querySelector('#saludo').textContent = `Conversando como ${nombre}`;
    formIngreso.hidden = true;
    chat.hidden = false;
    aviso.textContent = '';
    traerNuevos();
    estado.reloj = setInterval(traerNuevos, 1000);
}

formIngreso.addEventListener('submit', async (evento) => {
    evento.preventDefault();
    try {
        const yo = await api('POST', '/api/sesion', Object.fromEntries(new FormData(formIngreso)));
        formIngreso.reset();
        entrar(yo.nombre);
    } catch (error) {
        aviso.textContent = error.campos.nombre ?? error.message;
    }
});

formMensaje.addEventListener('submit', async (evento) => {
    evento.preventDefault();
    aviso.textContent = '';
    try {
        await api('POST', '/api/mensajes', Object.fromEntries(new FormData(formMensaje)));
        formMensaje.reset();
        await traerNuevos();
    } catch (error) {
        if (error.estado === 401) {
            mostrarIngreso('Tu sesión terminó: entrá de nuevo.');
        } else {
            aviso.textContent = error.campos.texto ?? error.message;
        }
    }
});

document.querySelector('#salir').addEventListener('click', async () => {
    await api('DELETE', '/api/sesion');
    mostrarIngreso('Saliste del chat.');
});

api('GET', '/api/sesion')
    .then((yo) => entrar(yo.nombre))
    .catch(() => mostrarIngreso());
```

### Prueba del sello

#### ¿Por qué la regla "una reserva por muelle y día" va en un `UNIQUE` de la base y no solo en un `SELECT` previo?

Porque si dos personas reservan a la vez, las dos ven el muelle libre y las dos insertan; el `UNIQUE` hace que la segunda falle (error 1062) pase lo que pase.

#### ¿Qué es el *polling*?

Preguntarle a la API cada tanto (por ejemplo cada segundo, con `setInterval`) si hay algo nuevo, para mostrarlo sin recargar.

#### ¿Para qué sirve el parámetro `desde` en `/api/mensajes?desde=41`?

Para que la API mande solo los mensajes con id mayor que 41: cada consulta trae lo nuevo y la página no repite mensajes.

#### ¿Por qué la página no manda otra consulta si la anterior no volvió?

Porque si el servidor anda lento los pedidos se apilarían, lo cargarían más y podrían llegar desordenados y duplicar mensajes.

#### ¿Qué significa el código 429?

"Demasiados pedidos": el servidor pide que esperes antes de mandar otro. Protege la API de quien la inunda.

### Soluciones (docente)

Sale de `22-JS-Vanilla` (14-Promesas, 15-Async-Await-Fetch, 17-Manejo-Errores) sobre la API de R05-N03 y las restricciones de R04. Las dos soluciones se verifican con el SQL cargado, `php -S … -t public router.php` y Chromium: el tablero cambiando de día, reservando (con los errores de campo, el 1062 y el calado) y cancelando; el chat con **dos navegadores a la vez**, los mensajes del otro llegando por *polling*, el 429 y el texto con `<b>` mostrado tal cual. En un hosting compartido el *polling* cada segundo es liviano (una consulta por clave primaria); para muchos usuarios se sube a cada 3–5 segundos.
