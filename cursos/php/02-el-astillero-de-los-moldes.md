# RAMA R02 · El Astillero de los Moldes: objetos

```meta
tipo: tronco
posicion: 2
```

## R02-N01 · Clases y objetos

```meta
tipo: tema
padre: R01-N10
precio: 10
criatura: skeleton
temas: poo.clases, poo.constructores
```

### Crónica

Pasando la roca de la Sirena empieza el **Astillero**. Hay moldes de madera colgados de las paredes: el molde de un bote, el de una balsa, el de un velero. Con cada molde los carpinteros arman muchos barcos iguales, y después cada uno se pinta distinto, lleva su propia carga y su propio nombre.

—Hasta ahora guardabas los datos de un barco en un array y las cuentas en funciones sueltas —dice {mentor}—. En el Astillero, el **molde** junta las dos cosas: qué datos tiene un barco y qué sabe hacer. Ese molde se llama **clase**, {heroe}, y cada barco hecho con él es un **objeto**.

### Objetivos

- Entender qué es una clase y qué es un objeto.
- Declarar propiedades con tipo y métodos.
- Crear objetos con `new` e inicializarlos con un constructor.
- Usar `$this` para referirse al objeto actual.
- Abreviar el constructor con la *promoción de propiedades*.
- Mostrar un objeto como texto con `__toString`.

### Antes de empezar

- Funciones con tipos y `strict_types` (R01-N08) y arrays asociativos (R01-N07).

### Explicación

#### Del array a la clase
Con lo que sabés, un barco es un array y lo que hace son funciones sueltas:
```php
$barco = ['nombre' => 'Gaviota', 'capacidad' => 500, 'carga' => 0];
function cargar(array $barco, float $kilos): array { … }
```
Nada impide escribir `$barco['capcidad']` (mal escrito) o pasarle a `cargar` un
array que no es un barco. Una **clase** define la forma exacta:
```php
class Barco
{
    public string $nombre;
    public float $capacidad;
    public float $carga = 0;          // valor inicial

    public function cargar(float $kilos): void
    {
        $this->carga += $kilos;
    }

    public function libre(): float
    {
        return $this->capacidad - $this->carga;
    }
}
```
- Las **propiedades** son los datos de cada objeto, con su tipo.
- Los **métodos** son funciones que pertenecen a la clase.
- **`$this`** es "el objeto sobre el que se llamó el método".
- Los nombres de clase van en *PascalCase* (`Barco`, `CajonDeCarga`).

#### Crear objetos
```php
$gaviota = new Barco();          // un objeto nuevo, hecho con el molde
$gaviota->nombre = 'Gaviota';     // -> accede a propiedades y métodos
$gaviota->capacidad = 500;
$gaviota->cargar(120);
echo $gaviota->libre();          // 380
```
Cada objeto tiene **sus propios** valores: cargar la *Gaviota* no cambia la carga
de otro barco.

#### El constructor
Es un método especial, **`__construct`**, que se ejecuta al hacer `new`. Sirve
para que el objeto nazca completo:
```php
class Barco
{
    public string $nombre;
    public float $capacidad;
    public float $carga = 0;

    public function __construct(string $nombre, float $capacidad)
    {
        $this->nombre = $nombre;
        $this->capacidad = $capacidad;
    }
}
$gaviota = new Barco('Gaviota', 500);
```

#### Promoción de propiedades
Declarar la propiedad, recibir el parámetro y asignarlo es tan común que PHP 8
permite hacerlo en una sola línea, poniendo la visibilidad en el parámetro:
```php
class Barco
{
    public float $carga = 0;

    public function __construct(
        public string $nombre,
        public float $capacidad,
    ) {}
}
```
Es exactamente lo mismo que la versión larga. En el Puerto se usa esta.

#### Mostrar un objeto
`echo $gaviota;` da `Object of class Barco could not be converted to string`. Si
querés que un objeto se pueda mostrar, definí **`__toString`**:
```php
public function __toString(): string
{
    return "{$this->nombre} ({$this->carga}/{$this->capacidad} kg)";
}
```
Para depurar, `print_r($objeto)` y `var_dump($objeto)` muestran todas las
propiedades.

#### Los objetos se comparten, no se copian
Asignar un objeto a otra variable **no lo copia**: las dos variables apuntan al
mismo objeto.
```php
$otro = $gaviota;
$otro->cargar(50);          // ¡también cargó a $gaviota!
$copia = clone $gaviota;    // una copia independiente
```
Con los arrays pasa lo contrario (se copian). Esto es terreno de **trolls**.

#### Propiedades que no existen
Escribir `$gaviota->capcidad = 600;` (mal escrito) crea una propiedad nueva y PHP
8.2 avisa: `Deprecated: Creation of dynamic property Barco::$capcidad is
deprecated`. Leé esos avisos: casi siempre es un nombre mal escrito.

### Código de ejemplo

```php
<?php
declare(strict_types=1);
/*
 * El molde del Astillero: una clase Barco con constructor, métodos y __toString.
 */
class Barco
{
    public float $carga = 0;

    public function __construct(
        public string $nombre,
        public float $capacidad,
    ) {}

    public function cargar(float $kilos): bool
    {
        if ($kilos <= 0 || $kilos > $this->libre()) {
            return false;
        }
        $this->carga += $kilos;
        return true;
    }

    public function libre(): float
    {
        return $this->capacidad - $this->carga;
    }

    public function porcentaje(): float
    {
        return round($this->carga / $this->capacidad * 100, 1);
    }

    public function __toString(): string
    {
        return "{$this->nombre}: {$this->carga}/{$this->capacidad} kg ({$this->porcentaje()}%)";
    }
}

$gaviota = new Barco('Gaviota', 500);
$albatros = new Barco('Albatros', 1200);

$gaviota->cargar(120);
$gaviota->cargar(300);
echo "¿Entran 200 kg más en la Gaviota? ", $gaviota->cargar(200) ? 'sí' : 'no', "\n";
$albatros->cargar(950);

echo $gaviota, "\n";
echo $albatros, "\n";
echo "Libre en el Albatros: ", $albatros->libre(), " kg\n";

// Los objetos se comparten
$mismo = $gaviota;
$mismo->cargar(30);
echo "Después de cargar \$mismo: ", $gaviota, "\n";
$copia = clone $gaviota;
$copia->cargar(40);
echo "Original: {$gaviota->carga} kg · copia: {$copia->carga} kg\n";

// Una lista de objetos
$flota = [$gaviota, $albatros, new Barco('Tortuga', 200)];
foreach ($flota as $barco) {
    echo "- ", $barco->nombre, " tiene ", $barco->libre(), " kg libres\n";
}
```

### Salida esperada

```
¿Entran 200 kg más en la Gaviota? no
Gaviota: 420/500 kg (84%)
Albatros: 950/1200 kg (79.2%)
Libre en el Albatros: 250 kg
Después de cargar $mismo: Gaviota: 450/500 kg (90%)
Original: 450 kg · copia: 490 kg
- Gaviota tiene 50 kg libres
- Albatros tiene 250 kg libres
- Tortuga tiene 200 kg libres
```

### ¿Para qué sirve?

Casi todo el PHP moderno está hecho con clases: un `Usuario`, un `Producto`, un `Pedido`. Laravel, WordPress (en su parte nueva) y todas las bibliotecas que vas a instalar con Composer son clases. Además, una clase le pone nombre a las cosas del problema: un `Barco` que sabe cargarse es mucho más claro que un array y tres funciones sueltas.

### Errores habituales

**Esqueleto: la propiedad mal escrita.** `$barco->capcidad = 600;` da
`Deprecated: Creation of dynamic property Barco::$capcidad`. Y leerla da
`Warning: Undefined property: Barco::$capcidad`.

**Esqueleto: olvidarse el `$this->`.** Adentro de un método, `$carga += $kilos;`
usa una variable local `$carga` que no existe: `Undefined variable $carga`. La
propiedad es `$this->carga`.

**Slime: `$this->$carga`.** Con `$` después de la flecha, PHP busca una propiedad
cuyo nombre sea el **valor** de `$carga`. Es `$this->carga`, sin `$`.

**Troll: creer que se copió.** `$b = $a;` con objetos no copia: los dos cambian
juntos. Para una copia, `clone`.

**Goblin: `echo` de un objeto.** `Object of class Barco could not be converted to
string`: definí `__toString` o mostrá sus propiedades.

**Esqueleto: la propiedad sin valor.** Una propiedad con tipo que nunca se asignó da
`Typed property Barco::$nombre must not be accessed before initialization`.
Inicializala en el constructor.

### Misión R02-N01-M1 · El molde del cajón

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí la clase `Cajon` con:

- propiedades promovidas en el constructor: `contenido` (texto), `ancho`, `alto` y
  `largo` (en metros, decimales) y `pesoKg` (decimal);
- `volumen(): float` — ancho × alto × largo, redondeado a 3 decimales;
- `densidad(): float` — kilos por metro cúbico, redondeado a 1 decimal;
- `esPesado(): bool` — si pesa más de 100 kg;
- `__toString(): string` — `Cajón de yerba (0.216 m³, 65 kg)`.

Creá tres cajones (yerba 0.6×0.6×0.6 de 65 kg, hierro 0.4×0.3×0.5 de 180 kg,
plumas 1×1×1 de 12 kg) y mostralos con su densidad y si son pesados.

#### Criterio de aprobación

- Usa promoción de propiedades en el constructor.
- Los métodos usan `$this` y tienen tipos.
- La salida coincide con la esperada.

#### Salida esperada

```
Cajón de yerba (0.216 m³, 65 kg)
  densidad: 300.9 kg/m³
Cajón de hierro (0.06 m³, 180 kg)
  densidad: 3000 kg/m³ · PESADO
Cajón de plumas (1 m³, 12 kg)
  densidad: 12 kg/m³
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - El molde del cajón: clase con constructor promovido y métodos.

class Cajon
{
    public function __construct(
        public string $contenido,
        public float $ancho,
        public float $alto,
        public float $largo,
        public float $pesoKg,
    ) {}

    public function volumen(): float
    {
        return round($this->ancho * $this->alto * $this->largo, 3);
    }

    public function densidad(): float
    {
        return round($this->pesoKg / ($this->ancho * $this->alto * $this->largo), 1);
    }

    public function esPesado(): bool
    {
        return $this->pesoKg > 100;
    }

    public function __toString(): string
    {
        return "Cajón de {$this->contenido} ({$this->volumen()} m³, {$this->pesoKg} kg)";
    }
}

$cajones = [
    new Cajon('yerba', 0.6, 0.6, 0.6, 65),
    new Cajon('hierro', 0.4, 0.3, 0.5, 180),
    new Cajon('plumas', 1, 1, 1, 12),
];

foreach ($cajones as $cajon) {
    echo $cajon, "\n";
    echo "  densidad: ", $cajon->densidad(), " kg/m³", $cajon->esPesado() ? " · PESADO" : "", "\n";
}
```

### Misión R02-N01-M2 · La cuenta del almacén

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El almacén del puerto les fía a los marineros. Escribí la clase `CuentaCorriente`
con el titular, el saldo (arranca en 0) y el límite de fiado (se pasa al crearla).
Métodos:

- `comprar(float $monto): bool` — suma deuda (el saldo baja); si pasaría el límite
  de fiado, no hace nada y devuelve `false`;
- `pagar(float $monto): void` — el saldo sube;
- `estado(): string` — `al día`, `debe` o `a favor`.

Creá dos cuentas y ejecutá los movimientos del ejemplo, mostrando el resultado de
cada uno. Mostrá también qué pasa si asignás la cuenta de Bron a otra variable y
comprás con esa variable.

#### Criterio de aprobación

- Los movimientos se hacen con métodos, no cambiando el saldo desde afuera.
- `comprar` respeta el límite.
- La salida coincide con la esperada.

#### Salida esperada

```
Kira compra 3200: ok
Kira compra 2500: rechazado
Kira: 800 (a favor)
Bron compra 1800: ok
Bron: 0 (al día)
Después de comprar con $otra: Bron: -500 (debe)
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 2 - La cuenta del almacén: estado que cambia con métodos.

class CuentaCorriente
{
    public float $saldo = 0;

    public function __construct(
        public string $titular,
        public float $limiteFiado,
    ) {}

    public function comprar(float $monto): bool
    {
        if ($this->saldo - $monto < -$this->limiteFiado) {
            return false;
        }
        $this->saldo -= $monto;
        return true;
    }

    public function pagar(float $monto): void
    {
        $this->saldo += $monto;
    }

    public function estado(): string
    {
        return match (true) {
            $this->saldo < 0 => 'debe',
            $this->saldo > 0 => 'a favor',
            default => 'al día',
        };
    }

    public function __toString(): string
    {
        return "{$this->titular}: {$this->saldo} ({$this->estado()})";
    }
}

$kira = new CuentaCorriente('Kira', 5000);
$bron = new CuentaCorriente('Bron', 2000);

echo "Kira compra 3200: ", $kira->comprar(3200) ? 'ok' : 'rechazado', "\n";
echo "Kira compra 2500: ", $kira->comprar(2500) ? 'ok' : 'rechazado', "\n";
$kira->pagar(4000);
echo $kira, "\n";

echo "Bron compra 1800: ", $bron->comprar(1800) ? 'ok' : 'rechazado', "\n";
$bron->pagar(1800);
echo $bron, "\n";

$otra = $bron;
$otra->comprar(500);
echo "Después de comprar con \$otra: ", $bron, "\n";
```

### Misión R02-N01-M3 · Del array a la clase

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Este programa guarda los pasajeros en arrays y los procesa con funciones sueltas.
Reescribilo con una clase `Pasajero` (nombre, edad, destino, con promoción de
propiedades) que tenga los métodos `esMenor(): bool`, `tarifa(): int` (menores
2500, el resto 5000) y `__toString()`. El programa principal tiene que dar
**exactamente la misma salida** que el original.

#### Criterio de aprobación

- No quedan funciones sueltas: la lógica está en métodos.
- La salida es idéntica a la del programa original.

#### Código inicial

```php
<?php
function esMenor(array $p): bool { return $p['edad'] < 18; }
function tarifa(array $p): int { return esMenor($p) ? 2500 : 5000; }

$pasajeros = [
    ['nombre' => 'Kira', 'edad' => 17, 'destino' => 'Valle'],
    ['nombre' => 'Bron', 'edad' => 45, 'destino' => 'Forjas'],
    ['nombre' => 'Tomi', 'edad' => 9, 'destino' => 'Valle'],
];
$total = 0;
foreach ($pasajeros as $p) {
    echo "{$p['nombre']} ({$p['edad']}) a {$p['destino']}: $", tarifa($p), esMenor($p) ? " [menor]" : "", "\n";
    $total += tarifa($p);
}
echo "Recaudación: $$total\n";
```

#### Salida esperada

```
Kira (17) a Valle: $2500 [menor]
Bron (45) a Forjas: $5000
Tomi (9) a Valle: $2500 [menor]
Recaudación: $10000
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - Del array a la clase: la misma salida con objetos.

class Pasajero
{
    public function __construct(
        public string $nombre,
        public int $edad,
        public string $destino,
    ) {}

    public function esMenor(): bool
    {
        return $this->edad < 18;
    }

    public function tarifa(): int
    {
        return $this->esMenor() ? 2500 : 5000;
    }

    public function __toString(): string
    {
        return "{$this->nombre} ({$this->edad}) a {$this->destino}: $" . $this->tarifa() . ($this->esMenor() ? " [menor]" : "");
    }
}

$pasajeros = [
    new Pasajero('Kira', 17, 'Valle'),
    new Pasajero('Bron', 45, 'Forjas'),
    new Pasajero('Tomi', 9, 'Valle'),
];
$total = 0;
foreach ($pasajeros as $p) {
    echo $p, "\n";
    $total += $p->tarifa();
}
echo "Recaudación: $$total\n";
```

### Encargo R02-N01-E1 · El termotanque inteligente

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una empresa de artefactos quiere simular un termotanque. Escribí la clase
`Termotanque` con la capacidad en litros, la temperatura actual (arranca en 15°)
y la temperatura deseada (se pasa al crearlo, por defecto 60). Métodos:

- `calentar(int $minutos): void` — sube 1.5° por minuto sin pasar la deseada;
- `usarAgua(int $litros): void` — por cada litro usado entra agua fría y la
  temperatura baja `30 / capacidad` grados por litro, sin bajar de 15;
- `listoParaBanarse(): bool` — si está a 40° o más;
- `__toString()` — `Termotanque 80 l: 42.5° (deseada 60°)`.

Simulá la mañana del ejemplo: calentar 20 minutos, usar 40 litros, calentar 10
minutos, usar 60 litros; mostrando el estado y si está listo después de cada paso.

#### Criterio de aprobación

- La temperatura nunca pasa la deseada ni baja de 15.
- Usa un valor por defecto en el constructor.
- La salida coincide con la esperada.

#### Salida esperada

```
Calienta 20 min → Termotanque 80 l: 45° (deseada 60°) · listo
Usa 40 l → Termotanque 80 l: 30° (deseada 60°) · todavía no
Calienta 10 min → Termotanque 80 l: 45° (deseada 60°) · listo
Usa 60 l → Termotanque 80 l: 22.5° (deseada 60°) · todavía no
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - El termotanque inteligente: estado con límites.

class Termotanque
{
    public float $temperatura = 15;

    public function __construct(
        public int $capacidad,
        public int $deseada = 60,
    ) {}

    public function calentar(int $minutos): void
    {
        $this->temperatura = min($this->deseada, $this->temperatura + 1.5 * $minutos);
    }

    public function usarAgua(int $litros): void
    {
        $this->temperatura = max(15, $this->temperatura - $litros * 30 / $this->capacidad);
    }

    public function listoParaBanarse(): bool
    {
        return $this->temperatura >= 40;
    }

    public function __toString(): string
    {
        return "Termotanque {$this->capacidad} l: " . round($this->temperatura, 1) . "° (deseada {$this->deseada}°)";
    }
}

$termo = new Termotanque(80);
$pasos = [['calentar', 20], ['usar', 40], ['calentar', 10], ['usar', 60]];
foreach ($pasos as [$accion, $cantidad]) {
    if ($accion === 'calentar') {
        $termo->calentar($cantidad);
        echo "Calienta $cantidad min → ";
    } else {
        $termo->usarAgua($cantidad);
        echo "Usa $cantidad l → ";
    }
    echo $termo, $termo->listoParaBanarse() ? " · listo" : " · todavía no", "\n";
}
```

### Prueba del sello

#### ¿Qué diferencia hay entre una clase y un objeto?

La clase es el molde (define qué datos y qué métodos hay); el objeto es una cosa concreta hecha con ese molde, con sus propios valores.

#### ¿Qué es `$this`?

El objeto sobre el que se está ejecutando el método.

#### ¿Cuándo se ejecuta `__construct`?

Al crear el objeto con `new`.

#### ¿Qué hace `public function __construct(public string $nombre) {}`?

Declara la propiedad `$nombre`, la recibe por parámetro y la asigna, todo en una línea (promoción de propiedades).

#### Si hacés `$b = $a;` con objetos y cambiás `$b`, ¿cambia `$a`?

Sí: las dos variables apuntan al mismo objeto. Para una copia independiente se usa `clone`.

### Soluciones (docente)

Sale de `21-PHP/09-Clases-Objetos`, reescrito desde cero con la transición "del array a la clase" (misión 3), que es lo que más cuesta al pasar de funciones a objetos. Las propiedades todavía son `public`: el encapsulamiento se ve en el nodo siguiente. En el encargo, `usarAgua(40)` con 80 litros baja 15°.

## R02-N02 · Encapsulamiento y readonly

```meta
tipo: tema
padre: R02-N01
precio: 10
criatura: troll
temas: poo.encapsulamiento, poo.records
```

### Crónica

En el Astillero hay un barco con un cartel en el timón: *"Solo el capitán"*. Un grumete curioso lo giró una noche y el barco terminó encallado. Desde entonces, el timón se maneja con una palanca que revisa el rumbo antes de moverlo.

—Si cualquiera puede tocar cualquier cosa de un objeto, tarde o temprano alguien lo rompe —dice {mentor}—. Los datos importantes se **esconden** y se cambian solo a través de métodos que controlan que el cambio tenga sentido. Y lo que no debe cambiar nunca, {heroe}, se marca para que nadie pueda.

### Objetivos

- Usar la visibilidad `public`, `private` y `protected`.
- Proteger el estado de un objeto con métodos que validan.
- Escribir *getters* y métodos con nombres del dominio en lugar de *setters* sueltos.
- Validar en el constructor para que un objeto nunca nazca inválido.
- Usar propiedades y clases `readonly` para datos que no cambian.
- Crear "objetos valor" inmutables que devuelven un objeto nuevo en lugar de cambiar.

### Antes de empezar

- Clases, objetos y constructores (R02-N01).

### Explicación

#### El problema de lo público
Con la `CuentaCorriente` del nodo anterior, nada impide:
```php
$cuenta->saldo = 999999;    // plata de la nada
$cuenta->limiteFiado = -5;  // un límite que no tiene sentido
```
Todo el control que pusiste en `comprar()` se saltea escribiendo directo.

#### Visibilidad
| Palabra | ¿Quién puede usarla? |
|---|---|
| `public` | cualquiera |
| `private` | solo los métodos de **esta** clase |
| `protected` | esta clase y las que heredan de ella (lo vas a ver en herencia) |

```php
class CuentaCorriente
{
    private float $saldo = 0;

    public function saldo(): float        // un "getter": solo lectura
    {
        return $this->saldo;
    }

    public function depositar(float $monto): void
    {
        if ($monto <= 0) {
            throw new InvalidArgumentException('El depósito tiene que ser positivo');
        }
        $this->saldo += $monto;
    }
}
$cuenta->saldo = 999999;   // Error: Cannot access private property CuentaCorriente::$saldo
```
Desde afuera, leer o escribir `$cuenta->saldo` da `Cannot access private
property CuentaCorriente::$saldo`. El único camino es `depositar()`, que valida.

`throw new InvalidArgumentException('…')` **corta** el método con un error que
dice qué pasó. Las excepciones se ven a fondo en su propio nodo; por ahora,
alcanza con saber que frenan un cambio inválido.

#### Getters sí, setters con cuidado
- Un **getter** (`saldo()`, `nombre()`) deja leer sin dejar cambiar.
- Un **setter** genérico (`setSaldo($x)`) vuelve a abrir la puerta. En lugar de
  eso, métodos que digan **qué pasa en el mundo**: `depositar`, `extraer`,
  `cerrar`, `renombrar`.

#### Validar en el constructor
Un objeto no debería poder **nacer** inválido:
```php
public function __construct(private string $titular, private float $limite)
{
    if (trim($titular) === '') {
        throw new InvalidArgumentException('Falta el titular');
    }
    if ($limite < 0) {
        throw new InvalidArgumentException('El límite no puede ser negativo');
    }
}
```
Así, cualquier `CuentaCorriente` que exista en el programa es válida.

#### `readonly`: se asigna una vez
Una propiedad `readonly` se asigna **una sola vez** (en el constructor) y después
no se puede cambiar, ni siquiera desde adentro de la clase:
```php
class Pasaje
{
    public function __construct(
        public readonly string $codigo,
        public readonly string $destino,
    ) {}
}
$p = new Pasaje('A-102', 'Valle');
echo $p->codigo;            // se puede leer
$p->destino = 'Imperio';    // Error: Cannot modify readonly property Pasaje::$destino
```
Es cómodo: se puede dejar `public` porque nadie la puede cambiar. Desde PHP 8.2,
`readonly class Pasaje { … }` hace `readonly` todas las propiedades.

#### Objetos valor inmutables
Algunas cosas se definen solo por su valor: un monto de dinero, una fecha, un
punto en el mapa. Conviene que sean **inmutables**: en lugar de cambiar, devuelven
un objeto nuevo.
```php
readonly class Dinero
{
    public function __construct(public int $centavos) {}

    public function sumar(Dinero $otro): Dinero
    {
        return new Dinero($this->centavos + $otro->centavos);
    }
}
$a = new Dinero(1000);
$b = $a->sumar(new Dinero(250));   // $a sigue valiendo 1000
```
Así se evitan los **trolls**: nadie cambia un objeto que otro está usando.

### Código de ejemplo

```php
<?php
declare(strict_types=1);
/*
 * El timón con palanca: private, validación en el constructor y readonly.
 */
class CuentaCorriente
{
    private float $saldo = 0;
    private array $movimientos = [];

    public function __construct(
        public readonly string $titular,
        private float $limiteFiado,
    ) {
        if (trim($titular) === '') {
            throw new InvalidArgumentException('Falta el titular');
        }
        if ($limiteFiado < 0) {
            throw new InvalidArgumentException('El límite no puede ser negativo');
        }
    }

    public function saldo(): float
    {
        return $this->saldo;
    }

    public function comprar(string $detalle, float $monto): bool
    {
        if ($monto <= 0 || $this->saldo - $monto < -$this->limiteFiado) {
            return false;
        }
        $this->saldo -= $monto;
        $this->movimientos[] = "- $monto $detalle";
        return true;
    }

    public function pagar(float $monto): void
    {
        if ($monto <= 0) {
            throw new InvalidArgumentException('El pago tiene que ser positivo');
        }
        $this->saldo += $monto;
        $this->movimientos[] = "+ $monto pago";
    }

    public function movimientos(): array
    {
        return $this->movimientos;     // devuelve una copia: los arrays se copian
    }
}

readonly class Dinero
{
    public function __construct(public int $centavos) {}

    public function sumar(Dinero $otro): Dinero
    {
        return new Dinero($this->centavos + $otro->centavos);
    }

    public function __toString(): string
    {
        return '$' . number_format($this->centavos / 100, 2, ',', '.');
    }
}

$cuenta = new CuentaCorriente('Kira', 5000);
$cuenta->comprar('yerba', 4200);
$cuenta->comprar('sal', 1500);           // pasaría el límite: no se hace
$cuenta->pagar(3000);
echo "{$cuenta->titular} tiene saldo ", $cuenta->saldo(), "\n";
foreach ($cuenta->movimientos() as $m) {
    echo "  $m\n";
}

// Lo privado no se toca desde afuera
try {
    echo $cuenta->saldo;
} catch (Error $e) {
    echo "No se puede: ", $e->getMessage(), "\n";
}
// Lo readonly no se cambia
try {
    $cuenta->titular = 'Bron';
} catch (Error $e) {
    echo "No se puede: ", $e->getMessage(), "\n";
}
// Un objeto no nace inválido
try {
    new CuentaCorriente('   ', 1000);
} catch (InvalidArgumentException $e) {
    echo "No se creó: ", $e->getMessage(), "\n";
}

// Un objeto valor inmutable
$precio = new Dinero(125050);
$conEnvio = $precio->sumar(new Dinero(150000));
echo "Precio: $precio · con envío: $conEnvio\n";
```

### Salida esperada

```
Kira tiene saldo -1200
  - 4200 yerba
  + 3000 pago
No se puede: Cannot access private property CuentaCorriente::$saldo
No se puede: Cannot modify readonly property CuentaCorriente::$titular
No se creó: Falta el titular
Precio: $1.250,50 · con envío: $2.750,50
```

### ¿Para qué sirve?

En un sistema real, el saldo de una cuenta, el stock de un producto o el estado de un pedido no pueden cambiar "porque sí": tienen reglas. Encapsular es poner esas reglas en un solo lugar (el método) para que ninguna parte del sistema las pueda saltear. Los objetos `readonly` son la base de los datos que se pasan entre capas (los DTO) en Laravel y en cualquier API.

### Errores habituales

**Troll: tocar lo privado desde afuera.**
```
PHP Fatal error:  Uncaught Error: Cannot access private property CuentaCorriente::$saldo
```
Usá el getter (`$cuenta->saldo()`) o el método que corresponda.

**Troll: cambiar un `readonly`.** `Cannot modify readonly property Pasaje::$destino`.
Si tiene que cambiar, no es `readonly`; si es un objeto valor, devolvé uno nuevo.

**Ogro: un setter que no valida.** `setLimite(-500)` deja el objeto roto. Validá en
cada método que cambia el estado.

**Troll: devolver el objeto interno.** Si un getter devuelve un **objeto** privado,
quien lo recibe lo puede modificar (los objetos se comparten). Devolvé una copia
(`clone`) o un objeto inmutable.

**Slime: `readonly` sin tipo.** `public readonly $x;` da error: las propiedades
`readonly` necesitan tipo.

### Misión R02-N02-M1 · El timón con palanca

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí la clase `Timon` con el rumbo en grados (0 a 359) como propiedad
**privada**. Métodos:

- `girar(int $grados): void` — gira a la derecha (positivo) o a la izquierda
  (negativo), dando la vuelta: 350 + 20 = 10, y 10 − 30 = 340 (usá `%` y sumá 360
  si queda negativo);
- `rumbo(): int` — el getter;
- `puntoCardinal(): string` — `N` (de 315 a 44), `E` (45 a 134), `S` (135 a 224),
  `O` (225 a 314).

El constructor recibe el rumbo inicial y lanza `InvalidArgumentException` si no está
entre 0 y 359. Probá los giros del ejemplo e intentá crear un timón con 400.

#### Criterio de aprobación

- El rumbo es `private` y solo cambia con `girar`.
- El constructor valida.
- La salida coincide con la esperada.

#### Salida esperada

```
Gira   20 →  10° (N)
Gira  -30 → 340° (N)
Gira   90 →  70° (E)
Gira  180 → 250° (O)
Gira -400 → 210° (S)
No se creó: Rumbo inválido: 400
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - El timón con palanca: estado privado que solo cambia con métodos.

class Timon
{
    public function __construct(private int $rumbo)
    {
        if ($rumbo < 0 || $rumbo > 359) {
            throw new InvalidArgumentException("Rumbo inválido: $rumbo");
        }
    }

    public function girar(int $grados): void
    {
        $this->rumbo = ($this->rumbo + $grados) % 360;
        if ($this->rumbo < 0) {
            $this->rumbo += 360;
        }
    }

    public function rumbo(): int
    {
        return $this->rumbo;
    }

    public function puntoCardinal(): string
    {
        return match (true) {
            $this->rumbo >= 45 && $this->rumbo < 135 => 'E',
            $this->rumbo >= 135 && $this->rumbo < 225 => 'S',
            $this->rumbo >= 225 && $this->rumbo < 315 => 'O',
            default => 'N',
        };
    }
}

$timon = new Timon(350);
foreach ([20, -30, 90, 180, -400] as $giro) {
    $timon->girar($giro);
    printf("Gira %4d → %3d° (%s)\n", $giro, $timon->rumbo(), $timon->puntoCardinal());
}
try {
    new Timon(400);
} catch (InvalidArgumentException $e) {
    echo "No se creó: ", $e->getMessage(), "\n";
}
```

### Misión R02-N02-M2 · El pasaje inmutable

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `readonly` `Pasaje` con código, pasajero, destino y precio (en
centavos, `int`). El constructor valida que el código tenga el formato `A-123`
(una letra mayúscula, guion y tres dígitos: podés usar `preg_match('/^[A-Z]-\d{3}$/',
$codigo)`) y que el precio sea positivo. Como es inmutable, en lugar de cambiarlo
tiene métodos que devuelven un pasaje **nuevo**:

- `conDescuento(int $porcentaje): Pasaje`;
- `cambiarDestino(string $destino, int $recargo): Pasaje` — nuevo destino y precio
  más el recargo.

Mostrá que el pasaje original no cambia después de pedir las variantes, e intentá
crear uno con código `a-12`.

#### Criterio de aprobación

- La clase es `readonly` y las variantes devuelven objetos nuevos.
- El constructor valida el código y el precio.
- La salida coincide con la esperada.

#### Salida esperada

```
Original:  A-102 Kira → Valle: $5.000,00
Descuento: A-102 Kira → Valle: $4.000,00
Cambio:    A-102 Kira → Imperio: $6.800,00
El original sigue igual: A-102 Kira → Valle: $5.000,00
No se creó: Código inválido: a-12
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 2 - El pasaje inmutable: readonly class y métodos que devuelven otro objeto.

readonly class Pasaje
{
    public function __construct(
        public string $codigo,
        public string $pasajero,
        public string $destino,
        public int $centavos,
    ) {
        if (!preg_match('/^[A-Z]-\d{3}$/', $codigo)) {
            throw new InvalidArgumentException("Código inválido: $codigo");
        }
        if ($centavos <= 0) {
            throw new InvalidArgumentException('El precio tiene que ser positivo');
        }
    }

    public function conDescuento(int $porcentaje): Pasaje
    {
        return new Pasaje($this->codigo, $this->pasajero, $this->destino, intdiv($this->centavos * (100 - $porcentaje), 100));
    }

    public function cambiarDestino(string $destino, int $recargo): Pasaje
    {
        return new Pasaje($this->codigo, $this->pasajero, $destino, $this->centavos + $recargo);
    }

    public function __toString(): string
    {
        return "{$this->codigo} {$this->pasajero} → {$this->destino}: $" . number_format($this->centavos / 100, 2, ',', '.');
    }
}

$original = new Pasaje('A-102', 'Kira', 'Valle', 500000);
$barato = $original->conDescuento(20);
$otro = $original->cambiarDestino('Imperio', 180000);

echo "Original:  $original\n";
echo "Descuento: $barato\n";
echo "Cambio:    $otro\n";
echo "El original sigue igual: $original\n";

try {
    new Pasaje('a-12', 'Bron', 'Forjas', 300000);
} catch (InvalidArgumentException $e) {
    echo "No se creó: ", $e->getMessage(), "\n";
}
```

### Misión R02-N02-M3 · El inventario con reglas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí la clase `Inventario` con un array **privado** `producto => cantidad`.
Métodos:

- `ingresar(string $producto, int $cantidad): void` — suma; si la cantidad no es
  positiva, lanza `InvalidArgumentException`;
- `retirar(string $producto, int $cantidad): void` — resta; si no hay suficiente,
  lanza `InvalidArgumentException` con el mensaje `No hay 30 de harina (quedan 20)`;
- `cantidad(string $producto): int` — 0 si no existe;
- `productos(): array` — una copia del array ordenada por nombre.

Ejecutá los movimientos del ejemplo dentro de un `try`/`catch` para cada uno,
mostrando `ok` o el mensaje del error, y al final el inventario.

#### Criterio de aprobación

- El array es privado y solo cambia con `ingresar` y `retirar`.
- Los movimientos inválidos lanzan excepciones con mensajes claros.
- La salida coincide con la esperada.

#### Salida esperada

```
ingresar 50 harina: ok
retirar 30 harina: ok
retirar 30 harina: No hay 30 de harina (quedan 20)
ingresar 0 aceite: La cantidad tiene que ser positiva (0)
ingresar 12 aceite: ok
retirar 1 sal: No hay 1 de sal (quedan 0)
Array
(
    [aceite] => 12
    [harina] => 20
)
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - El inventario con reglas: array privado y validación en cada método.

class Inventario
{
    private array $stock = [];

    public function ingresar(string $producto, int $cantidad): void
    {
        if ($cantidad <= 0) {
            throw new InvalidArgumentException("La cantidad tiene que ser positiva ($cantidad)");
        }
        $this->stock[$producto] = $this->cantidad($producto) + $cantidad;
    }

    public function retirar(string $producto, int $cantidad): void
    {
        $hay = $this->cantidad($producto);
        if ($cantidad > $hay) {
            throw new InvalidArgumentException("No hay $cantidad de $producto (quedan $hay)");
        }
        $this->stock[$producto] = $hay - $cantidad;
    }

    public function cantidad(string $producto): int
    {
        return $this->stock[$producto] ?? 0;
    }

    public function productos(): array
    {
        $copia = $this->stock;
        ksort($copia);
        return $copia;
    }
}

$inv = new Inventario();
$movimientos = [
    ['ingresar', 'harina', 50],
    ['retirar', 'harina', 30],
    ['retirar', 'harina', 30],
    ['ingresar', 'aceite', 0],
    ['ingresar', 'aceite', 12],
    ['retirar', 'sal', 1],
];
foreach ($movimientos as [$accion, $producto, $cantidad]) {
    try {
        $inv->$accion($producto, $cantidad);
        echo "$accion $cantidad $producto: ok\n";
    } catch (InvalidArgumentException $e) {
        echo "$accion $cantidad $producto: ", $e->getMessage(), "\n";
    }
}
print_r($inv->productos());
```

### Encargo R02-N02-E1 · El rango de fechas de la reserva

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un hotel del puerto toma reservas por noches. Escribí la clase `readonly`
`Estadia` con fecha de entrada y de salida como textos `AAAA-MM-DD` (se comparan
bien como texto porque tienen ese formato). El constructor valida con
`preg_match('/^\d{4}-\d{2}-\d{2}$/', …)` el formato y que la salida sea posterior a
la entrada. Métodos:

- `noches(): int` — con `(strtotime($salida) - strtotime($entrada)) / 86400`
  (86400 segundos por día), convertido a `int`;
- `seSuperponeCon(Estadia $otra): bool` — dos estadías se superponen si una
  empieza antes de que termine la otra (y viceversa);
- `__toString()` — `2026-10-03 → 2026-10-07 (4 noches)`.

Revisá las reservas del ejemplo contra una ya confirmada e intentá crear una con
la salida antes que la entrada.

#### Criterio de aprobación

- La clase es `readonly` y valida en el constructor.
- `seSuperponeCon` recibe otro objeto `Estadia`.
- La salida coincide con la esperada.

#### Salida esperada

```
Confirmada: 2026-10-03 → 2026-10-07 (4 noches)
2026-10-01 → 2026-10-03 (2 noches): libre
2026-10-06 → 2026-10-09 (3 noches): OCUPADO
2026-10-04 → 2026-10-05 (1 noche): OCUPADO
2026-10-07 → 2026-10-10 (3 noches): libre
Pedido rechazado: La salida (2026-10-10) tiene que ser después de la entrada (2026-10-12)
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - El rango de fechas de la reserva: un objeto valor que se compara con otro.

readonly class Estadia
{
    public function __construct(public string $entrada, public string $salida)
    {
        foreach ([$entrada, $salida] as $fecha) {
            if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $fecha)) {
                throw new InvalidArgumentException("Fecha inválida: $fecha");
            }
        }
        if ($salida <= $entrada) {
            throw new InvalidArgumentException("La salida ($salida) tiene que ser después de la entrada ($entrada)");
        }
    }

    public function noches(): int
    {
        return (int) ((strtotime($this->salida) - strtotime($this->entrada)) / 86400);
    }

    public function seSuperponeCon(Estadia $otra): bool
    {
        return $this->entrada < $otra->salida && $otra->entrada < $this->salida;
    }

    public function __toString(): string
    {
        $n = $this->noches();
        return "{$this->entrada} → {$this->salida} ($n " . ($n === 1 ? 'noche' : 'noches') . ")";
    }
}

$confirmada = new Estadia('2026-10-03', '2026-10-07');
echo "Confirmada: $confirmada\n";
$pedidos = [['2026-10-01', '2026-10-03'], ['2026-10-06', '2026-10-09'], ['2026-10-04', '2026-10-05'], ['2026-10-07', '2026-10-10'], ['2026-10-12', '2026-10-10']];
foreach ($pedidos as [$entrada, $salida]) {
    try {
        $pedido = new Estadia($entrada, $salida);
        echo "$pedido: ", $pedido->seSuperponeCon($confirmada) ? 'OCUPADO' : 'libre', "\n";
    } catch (InvalidArgumentException $e) {
        echo "Pedido rechazado: ", $e->getMessage(), "\n";
    }
}
```

### Prueba del sello

#### ¿Qué diferencia hay entre `private` y `public`?

`public` se puede usar desde cualquier lado; `private` solo desde los métodos de la misma clase.

#### ¿Por qué conviene validar en el constructor?

Para que ningún objeto pueda existir en un estado inválido: si los datos están mal, no se crea.

#### ¿Qué pasa si intentás cambiar una propiedad `readonly` después de crear el objeto?

Da el error `Cannot modify readonly property`.

#### ¿Qué es un objeto valor inmutable?

Un objeto que se define por su valor y no cambia nunca: sus métodos devuelven un objeto nuevo en lugar de modificarlo (como `Dinero` o `Pasaje`).

#### ¿Por qué `depositar()` es mejor que `setSaldo()`?

Porque dice qué pasa en el mundo y puede validar la regla (el monto positivo); un `setSaldo` genérico deja poner cualquier valor.

### Soluciones (docente)

Sale de `21-PHP/09-Clases-Objetos` (la parte de `readonly`) y se amplía con encapsulamiento, validación en el constructor y objetos valor. Se usa `throw new InvalidArgumentException` antes del nodo de excepciones, con la explicación mínima; el `try`/`catch` de las misiones es el mismo patrón que se profundiza en R02-N09. En la misión 3, `$inv->$accion(...)` llama al método cuyo nombre está en la variable: conviene comentarlo.

## R02-N03 · Static, constantes de clase y fábricas

```meta
tipo: tema
padre: R02-N02
precio: 10
criatura: goblin
temas: poo.static, diseno.patrones
```

### Crónica

En la puerta del Astillero hay una pizarra que no es de ningún barco en particular: dice cuántos barcos se botaron este año, el calado máximo permitido en el puerto y el precio de la madera. Todos los carpinteros la miran, pero no pertenece a ninguno.

—Hay datos que son de **cada** barco, como su nombre, y datos que son del **molde entero**, como cuántos barcos se hicieron con él —dice {mentor}—. Los segundos se marcan `static`. Y a veces, {heroe}, conviene tener varias puertas para fabricar un barco, cada una con un nombre que diga cómo.

### Objetivos

- Declarar constantes de clase y usarlas con `self::` y `NombreClase::`.
- Usar propiedades y métodos `static`, que pertenecen a la clase y no a un objeto.
- Escribir *métodos de fábrica* (constructores con nombre) para crear objetos de distintas maneras.
- Reconocer cuándo `static` ayuda y cuándo es un estado global disfrazado.

### Antes de empezar

- Encapsulamiento, validación en el constructor y `readonly` (R02-N02).

### Explicación

#### Constantes de clase
Un valor fijo que tiene que ver con la clase se declara adentro de ella:
```php
class Barco
{
    public const CALADO_MAXIMO = 12.5;     // metros
    private const TARIFA_AMARRE = 800;     // por metro de eslora

    public function amarre(float $eslora): float
    {
        return $eslora * self::TARIFA_AMARRE;   // adentro: self::
    }
}
echo Barco::CALADO_MAXIMO;                     // afuera: NombreClase::
```
Las constantes pueden ser `public` o `private`. Se escriben en MAYÚSCULAS.

#### Propiedades y métodos `static`
Pertenecen a la **clase**: hay una sola copia compartida por todos los objetos, y
se usan sin crear ninguno.
```php
class Barco
{
    private static int $botados = 0;

    public function __construct(public string $nombre)
    {
        self::$botados++;                 // ojo: con $ después de ::
    }

    public static function botados(): int
    {
        return self::$botados;
    }
}
new Barco('Gaviota');
new Barco('Albatros');
echo Barco::botados();                    // 2
```
Adentro de un método `static` **no hay `$this`** (no se llamó sobre ningún objeto).

Para funciones de ayuda que no necesitan un objeto también se usan métodos
estáticos: `Conversor::millasAKm(10)`.

#### Métodos de fábrica
Un constructor solo tiene un nombre (`new`). Cuando un objeto se puede crear de
varias maneras, se agregan **métodos estáticos** con nombres claros que devuelven
el objeto:
```php
readonly class Dinero
{
    private function __construct(public int $centavos) {}   // private: solo desde adentro

    public static function deCentavos(int $centavos): self
    {
        return new self($centavos);
    }

    public static function dePesos(float $pesos): self
    {
        return new self((int) round($pesos * 100));
    }

    public static function cero(): self
    {
        return new self(0);
    }
}
$precio = Dinero::dePesos(1250.50);     // se lee solo
```
`self` como tipo de retorno significa "un objeto de esta clase".

#### `self::` y `static::`
Adentro de la clase, `self::` es **la clase donde está escrito** el código, y
`static::` es **la clase sobre la que se llamó** (importa con herencia, en el
próximo nodo). Por ahora, `self::`.

#### Cuidado con el estado estático
Una propiedad `static` que cambia es, en el fondo, una **variable global**:
cualquier parte del programa la puede tocar y es difícil de probar. Usala para
contadores simples o valores de configuración; para todo lo demás, objetos.

### Código de ejemplo

```php
<?php
declare(strict_types=1);
/*
 * La pizarra del Astillero: constantes, static y métodos de fábrica.
 */
class Barco
{
    public const CALADO_MAXIMO = 12.5;
    private const TARIFA_AMARRE = 800;
    private static int $botados = 0;

    private function __construct(
        public readonly string $nombre,
        public readonly float $eslora,
        public readonly float $calado,
    ) {
        if ($calado > self::CALADO_MAXIMO) {
            throw new InvalidArgumentException("{$nombre} cala {$calado} m: no entra al puerto");
        }
        self::$botados++;
    }

    public static function velero(string $nombre): self
    {
        return new self($nombre, 12, 2.1);
    }

    public static function carguero(string $nombre, float $eslora): self
    {
        return new self($nombre, $eslora, $eslora / 20);
    }

    /** Crea un barco a partir de un texto "Nombre;eslora;calado". */
    public static function desdeTexto(string $linea): self
    {
        [$nombre, $eslora, $calado] = explode(';', $linea);
        return new self(trim($nombre), (float) $eslora, (float) $calado);
    }

    public static function botados(): int
    {
        return self::$botados;
    }

    public function amarrePorDia(): float
    {
        return $this->eslora * self::TARIFA_AMARRE;
    }
}

$flota = [
    Barco::velero('Brisa'),
    Barco::carguero('Coloso', 180),
    Barco::desdeTexto('Gaviota; 24; 3.2'),
];
foreach ($flota as $b) {
    printf("%-8s eslora %5.1f m, calado %4.1f m, amarre $%s/día\n", $b->nombre, $b->eslora, $b->calado, number_format($b->amarrePorDia(), 0, ',', '.'));
}

try {
    Barco::carguero('Leviatán', 300);
} catch (InvalidArgumentException $e) {
    echo "Rechazado: ", $e->getMessage(), "\n";
}
echo "Calado máximo del puerto: ", Barco::CALADO_MAXIMO, " m\n";
echo "Barcos botados: ", Barco::botados(), "\n";
```

### Salida esperada

```
Brisa    eslora  12.0 m, calado  2.1 m, amarre $9.600/día
Coloso   eslora 180.0 m, calado  9.0 m, amarre $144.000/día
Gaviota  eslora  24.0 m, calado  3.2 m, amarre $19.200/día
Rechazado: Leviatán cala 15 m: no entra al puerto
Calado máximo del puerto: 12.5 m
Barcos botados: 3
```

### ¿Para qué sirve?

Los métodos de fábrica están en todas partes: en PHP, `DateTimeImmutable::createFromFormat()`; en Laravel, `Usuario::create([...])` y `Carbon::now()`. Hacen que el código se lea como una frase y permiten validar o preparar los datos antes de crear el objeto. Las constantes de clase ponen nombre a los "números mágicos" (`Pedido::ESTADO_PAGADO` en lugar de `3`).

### Errores habituales

**Esqueleto: `$this` en un método estático.** `Using $this when not in object
context`: un método `static` no tiene objeto. Pasale lo que necesite por parámetro.

**Slime: `self::botados` sin `$`.** Las propiedades estáticas llevan `$` después de
`::` (`self::$botados`); las constantes no (`self::TARIFA`).

**Goblin: llamar un método de objeto como estático.** `Barco::amarrePorDia()` da
`Non-static method Barco::amarrePorDia() cannot be called statically`: primero creá
el objeto.

**Troll: el estado estático compartido.** Si dos partes del programa usan el mismo
contador estático, se pisan. Es una variable global: usala poco.

**Esqueleto: `new` de un constructor privado.** `Call to private Barco::__construct()
from global scope`: esa clase se crea solo con sus métodos de fábrica.

### Misión R02-N03-M1 · Los boletos numerados

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La boletería del ferry numera los boletos sin repetir. Escribí la clase `Boleto`
con:

- una constante `PRECIO_BASE = 5000` y una constante `RECARGO_NOCTURNO = 0.25`;
- un contador `static` privado que asigna el número al crearlo: `B-0001`,
  `B-0002`… (con `sprintf('B-%04d', …)`);
- propiedades `readonly` para el número, el pasajero y si es nocturno;
- `precio(): float` que aplica el recargo si es nocturno;
- `static emitidos(): int`.

Emití cuatro boletos del ejemplo, mostralos y mostrá cuántos se emitieron y la
recaudación total.

#### Criterio de aprobación

- El número sale del contador `static`.
- Los valores fijos son constantes de clase.
- La salida coincide con la esperada.

#### Salida esperada

```
B-0001 Kira: $5000
B-0002 Bron (nocturno): $6250
B-0003 Lía: $5000
B-0004 Olmo (nocturno): $6250
Emitidos: 4 · recaudación: $22500
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - Los boletos numerados: constantes y un contador static.

class Boleto
{
    public const PRECIO_BASE = 5000;
    public const RECARGO_NOCTURNO = 0.25;
    private static int $ultimo = 0;

    public readonly string $numero;

    public function __construct(
        public readonly string $pasajero,
        public readonly bool $nocturno = false,
    ) {
        self::$ultimo++;
        $this->numero = sprintf('B-%04d', self::$ultimo);
    }

    public function precio(): float
    {
        return $this->nocturno ? self::PRECIO_BASE * (1 + self::RECARGO_NOCTURNO) : self::PRECIO_BASE;
    }

    public static function emitidos(): int
    {
        return self::$ultimo;
    }
}

$boletos = [
    new Boleto('Kira'),
    new Boleto('Bron', nocturno: true),
    new Boleto('Lía'),
    new Boleto('Olmo', nocturno: true),
];
$total = 0;
foreach ($boletos as $b) {
    echo "{$b->numero} {$b->pasajero}", $b->nocturno ? ' (nocturno)' : '', ": $", $b->precio(), "\n";
    $total += $b->precio();
}
echo "Emitidos: ", Boleto::emitidos(), " · recaudación: $", $total, "\n";
```

### Misión R02-N03-M2 · La temperatura de tres maneras

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Los barcos que llegan anotan la temperatura del agua en distintas escalas.
Escribí una clase `readonly` `Temperatura` que guarde siempre los **grados
Celsius**, con constructor **privado** y tres fábricas:

- `Temperatura::celsius(float $c)`;
- `Temperatura::fahrenheit(float $f)` — `c = (f − 32) × 5 / 9`;
- `Temperatura::kelvin(float $k)` — `c = k − 273.15`; si el kelvin es negativo,
  `InvalidArgumentException`.

Y los métodos `enFahrenheit(): float`, `esHelada(): bool` (menos de 0 °C) y
`__toString()` (`12.5 °C`, con un decimal). Convertí las lecturas del ejemplo.

#### Criterio de aprobación

- El constructor es privado y los objetos se crean con las fábricas.
- Las fábricas devuelven `self`.
- La salida coincide con la esperada.

#### Salida esperada

```
Gaviota: 12.5 °C (54.5 °F)
Vikingo: -2.0 °C (28.4 °F) ¡agua helada!
Explorador: 17.0 °C (62.6 °F)
Lectura descartada: No existe una temperatura de -5 K
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 2 - La temperatura de tres maneras: constructor privado y fábricas.

readonly class Temperatura
{
    private function __construct(public float $celsius) {}

    public static function celsius(float $c): self
    {
        return new self($c);
    }

    public static function fahrenheit(float $f): self
    {
        return new self(($f - 32) * 5 / 9);
    }

    public static function kelvin(float $k): self
    {
        if ($k < 0) {
            throw new InvalidArgumentException("No existe una temperatura de $k K");
        }
        return new self($k - 273.15);
    }

    public function enFahrenheit(): float
    {
        return round($this->celsius * 9 / 5 + 32, 1);
    }

    public function esHelada(): bool
    {
        return $this->celsius < 0;
    }

    public function __toString(): string
    {
        return number_format($this->celsius, 1) . ' °C';
    }
}

$lecturas = [
    ['Gaviota', Temperatura::celsius(12.5)],
    ['Vikingo', Temperatura::fahrenheit(28.4)],
    ['Explorador', Temperatura::kelvin(290.15)],
];
foreach ($lecturas as [$barco, $t]) {
    echo "$barco: $t (", $t->enFahrenheit(), " °F)", $t->esHelada() ? ' ¡agua helada!' : '', "\n";
}
try {
    Temperatura::kelvin(-5);
} catch (InvalidArgumentException $e) {
    echo "Lectura descartada: ", $e->getMessage(), "\n";
}
```

### Misión R02-N03-M3 · La caja de herramientas del cambista

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Convertí el conversor del cambista (R01-N08) en una clase de **utilidades** con
métodos estáticos: `Cambio::aPesos`, `Cambio::convertir` y `Cambio::mostrar`. Las
cotizaciones van en una **constante privada** de la clase. Agregá
`Cambio::monedas(): array` que devuelva la lista de monedas ordenada. La clase no
se instancia: su constructor es privado.

Mostrá la lista de monedas y los mismos cambios de aquella misión.

#### Criterio de aprobación

- Todos los métodos son `static` y usan `self::`.
- Las cotizaciones son una constante privada.
- La salida coincide con la esperada.

#### Salida esperada

```
Monedas: denario, engranaje, escama, lingote
10 denarios = 3,68 lingotes
1 lingote = 4,15 escamas
250 escamas = 97,62 engranajes
Moneda desconocida: perla
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - La caja de herramientas del cambista: una clase de utilidades estáticas.

final class Cambio
{
    private const COTIZACIONES = ['denario' => 1250.0, 'lingote' => 3400.0, 'escama' => 820.0, 'engranaje' => 2100.0];

    private function __construct() {}

    public static function monedas(): array
    {
        $monedas = array_keys(self::COTIZACIONES);
        sort($monedas);
        return $monedas;
    }

    public static function aPesos(float $cantidad, string $moneda): ?float
    {
        return isset(self::COTIZACIONES[$moneda]) ? $cantidad * self::COTIZACIONES[$moneda] : null;
    }

    public static function convertir(float $cantidad, string $de, string $a): ?float
    {
        $pesos = self::aPesos($cantidad, $de);
        if ($pesos === null || !isset(self::COTIZACIONES[$a])) {
            return null;
        }
        return round($pesos / self::COTIZACIONES[$a], 2);
    }

    public static function mostrar(float $cantidad, string $de, string $a): string
    {
        $resultado = self::convertir($cantidad, $de, $a);
        if ($resultado === null) {
            return 'Moneda desconocida: ' . (isset(self::COTIZACIONES[$de]) ? $a : $de);
        }
        return number_format($cantidad, 0, ',', '.') . ' ' . self::plural($de, $cantidad)
            . ' = ' . number_format($resultado, 2, ',', '.') . ' ' . self::plural($a, $resultado);
    }

    private static function plural(string $moneda, float $cantidad): string
    {
        return $cantidad == 1 ? $moneda : $moneda . 's';
    }
}

echo "Monedas: ", implode(', ', Cambio::monedas()), "\n";
echo Cambio::mostrar(10, 'denario', 'lingote'), "\n";
echo Cambio::mostrar(1, 'lingote', 'escama'), "\n";
echo Cambio::mostrar(250, 'escama', 'engranaje'), "\n";
echo Cambio::mostrar(5, 'perla', 'denario'), "\n";
```

### Encargo R02-N03-E1 · El código de producto

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un mayorista identifica cada producto con un código `RUBRO-NUMERO` (`ALM-0042`).
Escribí la clase `readonly` `CodigoProducto` con:

- una constante `RUBROS` con los rubros válidos (`ALM` almacén, `LIM` limpieza,
  `BEB` bebidas, `FRE` frescos) y sus nombres;
- constructor privado y dos fábricas: `desdeTexto(string $codigo)` (acepta
  minúsculas y espacios: `" alm-42 "` es `ALM-0042`) y `nuevo(string $rubro,
  int $numero)`;
- validación: rubro conocido y número entre 1 y 9999, si no
  `InvalidArgumentException`;
- `rubroNombre(): string` y `__toString()` con el número en 4 cifras.

Procesá los códigos del ejemplo mostrando cada uno normalizado con su rubro, o el
error.

#### Criterio de aprobación

- Las dos fábricas terminan llamando al mismo constructor, que valida.
- Los rubros son una constante de clase.
- La salida coincide con la esperada.

#### Salida esperada

```
« alm-42 »   → ALM-0042 (almacén)
«BEB-0007»   → BEB-0007 (bebidas)
«lim-15000»  → error: Número fuera de rango: 15000
«ZAP-12»     → error: Rubro desconocido: ZAP
«FRE12»      → error: Formato inválido: FRE12
«fre-3»      → FRE-0003 (frescos)
Nuevo: BEB-0088
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - El código de producto: fábricas que normalizan y un constructor que valida.

readonly class CodigoProducto
{
    public const RUBROS = ['ALM' => 'almacén', 'LIM' => 'limpieza', 'BEB' => 'bebidas', 'FRE' => 'frescos'];

    private function __construct(public string $rubro, public int $numero)
    {
        if (!isset(self::RUBROS[$rubro])) {
            throw new InvalidArgumentException("Rubro desconocido: $rubro");
        }
        if ($numero < 1 || $numero > 9999) {
            throw new InvalidArgumentException("Número fuera de rango: $numero");
        }
    }

    public static function nuevo(string $rubro, int $numero): self
    {
        return new self(strtoupper($rubro), $numero);
    }

    public static function desdeTexto(string $codigo): self
    {
        $partes = explode('-', strtoupper(trim($codigo)));
        if (count($partes) !== 2 || !ctype_digit($partes[1])) {
            throw new InvalidArgumentException("Formato inválido: " . trim($codigo));
        }
        return new self($partes[0], (int) $partes[1]);
    }

    public function rubroNombre(): string
    {
        return self::RUBROS[$this->rubro];
    }

    public function __toString(): string
    {
        return sprintf('%s-%04d', $this->rubro, $this->numero);
    }
}

$entradas = [' alm-42 ', 'BEB-0007', 'lim-15000', 'ZAP-12', 'FRE12', 'fre-3'];
foreach ($entradas as $texto) {
    try {
        $codigo = CodigoProducto::desdeTexto($texto);
        echo str_pad("«{$texto}»", 14), " → $codigo (", $codigo->rubroNombre(), ")\n";
    } catch (InvalidArgumentException $e) {
        echo str_pad("«{$texto}»", 14), " → error: ", $e->getMessage(), "\n";
    }
}
echo "Nuevo: ", CodigoProducto::nuevo('beb', 88), "\n";
```

### Prueba del sello

#### ¿Qué diferencia hay entre una propiedad normal y una `static`?

La normal es de cada objeto (cada uno tiene la suya); la `static` es de la clase, una sola compartida, y se usa sin crear objetos.

#### ¿Por qué no se puede usar `$this` en un método `static`?

Porque un método estático se llama sobre la clase, no sobre un objeto: no hay "objeto actual".

#### ¿Cómo se escribe una propiedad estática y una constante desde adentro de la clase?

`self::$propiedad` (con `$`) y `self::CONSTANTE` (sin `$`).

#### ¿Qué es un método de fábrica?

Un método estático con un nombre claro que crea y devuelve un objeto de la clase, por ejemplo `Dinero::dePesos(12.5)`.

#### ¿Para qué se hace privado un constructor?

Para que los objetos solo se puedan crear con los métodos de fábrica de la clase.

### Soluciones (docente)

Nodo nuevo (el capítulo original solo nombra `static`). Se presenta `static::` sin profundizar; aparece con sentido en herencia. En la misión 2, 28.4 °F son −2 °C (agua helada de mar). En el encargo, `FRE12` falla por formato, `lim-15000` por rango y `ZAP-12` por rubro: tres errores distintos para probar.

## R02-N04 · Herencia

```meta
tipo: tema
padre: R02-N03
precio: 10
criatura: troll
temas: poo.herencia
```

### Crónica

En el fondo del Astillero hay un árbol genealógico pintado en la pared: arriba, la **Embarcación**, con casco y nombre; de ella salen el **Velero**, que además tiene velas, y el **Remolcador**, que además tiene motor y cuerda de arrastre. Todos son embarcaciones, pero cada uno agrega lo suyo.

—No hace falta escribir dos veces lo que tienen en común —dice {mentor}—. El velero **hereda** todo de la embarcación y solo agrega lo que lo hace distinto. Pero heredar es un compromiso, {heroe}: si el hijo cambia algo del padre, tiene que seguir cumpliendo lo que el padre prometía.

### Objetivos

- Crear una clase hija con `extends` que reutiliza la clase padre.
- Llamar al constructor y a los métodos del padre con `parent::`.
- Usar `protected` para compartir datos con las clases hijas.
- Redefinir (sobrescribir) métodos respetando su firma.
- Impedir la herencia o la redefinición con `final`.
- Distinguir "es un" (herencia) de "tiene un" (composición).

### Antes de empezar

- Encapsulamiento (R02-N02) y constantes y `static` (R02-N03).

### Explicación

#### `extends`
```php
class Embarcacion
{
    public function __construct(
        protected string $nombre,
        protected float $eslora,
    ) {}

    public function describir(): string
    {
        return "{$this->nombre} ({$this->eslora} m)";
    }
}

class Velero extends Embarcacion
{
    public function __construct(string $nombre, float $eslora, private int $velas)
    {
        parent::__construct($nombre, $eslora);   // arma la parte del padre
    }

    public function describir(): string        // redefine el del padre
    {
        return parent::describir() . " con {$this->velas} velas";
    }
}
```
- `Velero` **es una** `Embarcacion`: tiene todo lo del padre (propiedades y métodos)
  y agrega lo suyo.
- `parent::__construct(...)` ejecuta el constructor del padre. **Si el hijo tiene
  constructor propio y no lo llama, la parte del padre queda sin inicializar.**
- `parent::describir()` llama a la versión del padre desde la del hijo.

#### `protected`
- `private`: solo la misma clase (¡ni siquiera las hijas!).
- `protected`: la clase y sus hijas.
- `public`: cualquiera.

En una clase pensada para heredar, lo que las hijas necesitan tocar va
`protected`.

#### Redefinir métodos
El hijo puede reemplazar un método del padre, pero con una **firma compatible**:
mismos parámetros (o más, con valor por defecto) y un tipo de retorno igual o más
específico. Si no, PHP no deja:
```
PHP Fatal error:  Declaration of Velero::describir(int $x): string must be compatible with Embarcacion::describir(): string
```
Es una garantía: donde el programa espera una `Embarcacion`, cualquier hija tiene
que funcionar igual de bien.

#### `final`
- `final class Remolcador` — nadie puede heredar de ella.
- `final public function tasa()` — las hijas no la pueden redefinir.

Usalo cuando una regla no se tiene que poder cambiar (una tasa, un cálculo de
seguridad).

#### `instanceof` y el tipo del padre
```php
$v = new Velero('Brisa', 12, 3);
var_dump($v instanceof Velero);        // true
var_dump($v instanceof Embarcacion);   // true: un velero ES una embarcación
function amarrar(Embarcacion $e): void { … }   // acepta veleros, remolcadores…
```

#### ¿Herencia o composición?
Heredá solo si la frase **"un X es un Y"** es verdadera siempre: *un velero es una
embarcación* ✔. Si la frase es **"un X tiene un Y"**, no se hereda: *un barco
tiene un motor* → el barco tiene una propiedad `Motor`. Heredar para "reutilizar
código" cuando no es un "es un" termina en clases raras (un `Barco extends Motor`)
y en **trolls**. Lo vas a ver a fondo en el nodo de traits y composición.

### Código de ejemplo

```php
<?php
declare(strict_types=1);
/*
 * El árbol del Astillero: una clase padre y dos hijas.
 */
class Embarcacion
{
    public const TASA_POR_METRO = 500;

    public function __construct(
        protected string $nombre,
        protected float $eslora,
    ) {}

    public function nombre(): string
    {
        return $this->nombre;
    }

    public function tasaPuerto(): float
    {
        return $this->eslora * self::TASA_POR_METRO;
    }

    public function describir(): string
    {
        return "{$this->nombre} ({$this->eslora} m)";
    }
}

class Velero extends Embarcacion
{
    public function __construct(string $nombre, float $eslora, private int $velas)
    {
        parent::__construct($nombre, $eslora);
    }

    public function describir(): string
    {
        return parent::describir() . " - velero de {$this->velas} velas";
    }
}

final class Remolcador extends Embarcacion
{
    public function __construct(string $nombre, float $eslora, private int $potenciaHp)
    {
        parent::__construct($nombre, $eslora);
    }

    public function tasaPuerto(): float
    {
        // Los remolcadores pagan la mitad: trabajan para el puerto.
        return parent::tasaPuerto() / 2;
    }

    public function puedeArrastrar(Embarcacion $otra): bool
    {
        return $this->potenciaHp >= $otra->tasaPuerto() / 10;
    }

    public function describir(): string
    {
        return parent::describir() . " - remolcador de {$this->potenciaHp} HP";
    }
}

$flota = [
    new Embarcacion('Balsa', 6),
    new Velero('Brisa', 12, 3),
    new Remolcador('Toro', 25, 1500),
];

foreach ($flota as $e) {
    printf("%-50s tasa $%s\n", $e->describir(), number_format($e->tasaPuerto(), 0, ',', '.'));
}

$toro = $flota[2];
$titan = new Embarcacion('Titán', 320);
echo "¿Toro arrastra a Brisa? ", $toro->puedeArrastrar($flota[1]) ? 'sí' : 'no', "\n";
echo "¿Toro arrastra a Titán? ", $toro->puedeArrastrar($titan) ? 'sí' : 'no', "\n";
var_dump($flota[1] instanceof Embarcacion, $flota[1] instanceof Remolcador);
```

### Salida esperada

```
Balsa (6 m)                                        tasa $3.000
Brisa (12 m) - velero de 3 velas                   tasa $6.000
Toro (25 m) - remolcador de 1500 HP                tasa $6.250
¿Toro arrastra a Brisa? sí
¿Toro arrastra a Titán? no
bool(true)
bool(false)
```

### ¿Para qué sirve?

Los frameworks usan herencia todo el tiempo: en Laravel, cada modelo de la base de datos `extends Model` y cada controlador `extends Controller`, y así heredan cientos de métodos listos. Saber qué heredás, qué podés redefinir y cómo llamar al padre es lo que te deja usar esas herramientas sin romperlas.

### Errores habituales

**Troll: no llamar a `parent::__construct`.** Si el hijo tiene constructor y no llama
al del padre, sus propiedades quedan vacías:
```
PHP Fatal error:  Uncaught Error: Typed property Embarcacion::$nombre must not be accessed before initialization
```

**Esqueleto: `private` en el padre.** Si el padre declara `private $nombre`, la hija
no lo ve (`Undefined property`). Lo que comparten va `protected`.

**Slime: la firma incompatible.**
`Declaration of Velero::describir(int $x): string must be compatible with
Embarcacion::describir(): string`. Respetá los parámetros y el retorno del padre.

**Goblin: heredar de una clase final.** `Class Lancha cannot extend final class
Remolcador`.

**Ogro: herencia para reutilizar código.** Si "un X es un Y" suena raro, no
heredes: usá composición (una propiedad).

### Misión R02-N04-M1 · Los empleados del puerto

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El Puerto paga sueldos a tres tipos de empleados. Escribí la clase `Empleado`
(nombre y sueldo básico, `protected`) con `sueldo(): float` y `recibo(): string`, y
dos hijas:

- `Estibador` — cobra además $1200 por cada **hora extra** (se pasa al crearlo);
- `Capitan` — cobra un 30% más por **responsabilidad**, y su `recibo()` agrega el
  barco que comanda.

Las hijas llaman al constructor del padre y usan `parent::sueldo()` en lugar de
repetir la cuenta. Mostrá los recibos del ejemplo y el total a pagar.

#### Criterio de aprobación

- Usa `extends`, `parent::__construct` y `parent::sueldo()`.
- Las propiedades compartidas son `protected`.
- La salida coincide con la esperada.

#### Salida esperada

```
Nara   $650.000,00
Bron   $716.800,00
Kira   $1.170.000,00 (capitán del Gaviota)
Total: $2.536.800,00
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - Los empleados del puerto: herencia y parent::.

class Empleado
{
    public function __construct(protected string $nombre, protected float $basico) {}

    public function sueldo(): float
    {
        return $this->basico;
    }

    public function recibo(): string
    {
        return sprintf('%-6s $%s', $this->nombre, number_format($this->sueldo(), 2, ',', '.'));
    }
}

class Estibador extends Empleado
{
    public const POR_HORA_EXTRA = 1200;

    public function __construct(string $nombre, float $basico, private int $horasExtra)
    {
        parent::__construct($nombre, $basico);
    }

    public function sueldo(): float
    {
        return parent::sueldo() + $this->horasExtra * self::POR_HORA_EXTRA;
    }
}

class Capitan extends Empleado
{
    public function __construct(string $nombre, float $basico, private string $barco)
    {
        parent::__construct($nombre, $basico);
    }

    public function sueldo(): float
    {
        return parent::sueldo() * 1.30;
    }

    public function recibo(): string
    {
        return parent::recibo() . " (capitán del {$this->barco})";
    }
}

$empleados = [
    new Empleado('Nara', 650000),
    new Estibador('Bron', 700000, 14),
    new Capitan('Kira', 900000, 'Gaviota'),
];
$total = 0;
foreach ($empleados as $e) {
    echo $e->recibo(), "\n";
    $total += $e->sueldo();
}
echo "Total: $", number_format($total, 2, ',', '.'), "\n";
```

### Misión R02-N04-M2 · El padre olvidado

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Este programa tiene **tres** errores de herencia: uno no deja ni cargar el
archivo, otro corta el programa al ejecutarse y otro hace que un dato del padre no
se vea desde la hija. Encontralos, corregilos y dejá un comentario en cada
corrección.

#### Criterio de aprobación

- Corrige los tres errores sin cambiar la salida pedida.
- Cada corrección tiene su comentario.
- La salida coincide con la esperada.

#### Código inicial

```php
<?php
declare(strict_types=1);

class Vehiculo
{
    public function __construct(private string $patente, protected int $ruedas) {}

    public function descripcion(): string
    {
        return "{$this->patente} con {$this->ruedas} ruedas";
    }
}

class Camion extends Vehiculo
{
    public function __construct(string $patente, private float $toneladas)
    {
    }

    public function descripcion(int $detalle): string
    {
        return "Camión {$this->patente}: " . parent::descripcion() . ", {$this->toneladas} t";
    }
}

$c = new Camion('AB123CD', 12.5);
echo $c->descripcion(), "\n";
```

#### Salida esperada

```
Camión AB123CD: AB123CD con 6 ruedas, 12.5 t
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 2 - El padre olvidado: tres errores de herencia corregidos.

class Vehiculo
{
    // 3. $patente era private: la hija no la ve. Pasa a protected.
    public function __construct(protected string $patente, protected int $ruedas) {}

    public function descripcion(): string
    {
        return "{$this->patente} con {$this->ruedas} ruedas";
    }
}

class Camion extends Vehiculo
{
    public function __construct(string $patente, private float $toneladas)
    {
        // 2. Faltaba llamar al constructor del padre: patente y ruedas quedaban sin valor.
        parent::__construct($patente, 6);
    }

    // 1. La firma tenía un parámetro que el padre no tiene: incompatible.
    public function descripcion(): string
    {
        return "Camión {$this->patente}: " . parent::descripcion() . ", {$this->toneladas} t";
    }
}

$c = new Camion('AB123CD', 12.5);
echo $c->descripcion(), "\n";
```

### Misión R02-N04-M3 · Las cuentas del banco del puerto

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El banco del puerto tiene una clase `Cuenta` con titular y saldo (`protected`), y
los métodos `depositar`, `extraer` (devuelve `bool`: no deja el saldo negativo) y
`saldo()`. Hay dos tipos especiales:

- `CajaDeAhorro` — solo permite **3 extracciones** por mes (lleva la cuenta); la
  cuarta se rechaza aunque haya saldo. Tiene `finDeMes()` que suma un 2% de
  interés y reinicia el contador.
- `CuentaCorriente` — permite quedar en negativo hasta un **descubierto** que se
  pasa al crearla; `extraer` se redefine para eso.

`depositar` y `saldo` son `final` en `Cuenta` (nadie los tiene que cambiar).
Ejecutá los movimientos del ejemplo mostrando cada resultado.

#### Criterio de aprobación

- Las hijas redefinen `extraer` con la misma firma.
- `depositar` y `saldo` son `final`.
- La salida coincide con la esperada.

#### Salida esperada

```
Ahorro, extracción 1 de 1000: ok
Ahorro, extracción 2 de 2000: ok
Ahorro, extracción 3 de 500: ok
Ahorro, extracción 4 de 100: rechazada
Ahorro a fin de mes: 6630
Ahorro, extracción de 100 en el mes nuevo: ok
Corriente, extrae 6000: ok (saldo -4000)
Corriente, extrae 2000: rechazada (saldo -4000)
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - Las cuentas del banco del puerto: redefinir con la misma firma y final.

class Cuenta
{
    protected float $saldo = 0;

    public function __construct(protected string $titular) {}

    final public function depositar(float $monto): void
    {
        $this->saldo += $monto;
    }

    public function extraer(float $monto): bool
    {
        if ($monto > $this->saldo) {
            return false;
        }
        $this->saldo -= $monto;
        return true;
    }

    final public function saldo(): float
    {
        return $this->saldo;
    }
}

class CajaDeAhorro extends Cuenta
{
    public const EXTRACCIONES_POR_MES = 3;
    private int $extracciones = 0;

    public function extraer(float $monto): bool
    {
        if ($this->extracciones >= self::EXTRACCIONES_POR_MES) {
            return false;
        }
        $ok = parent::extraer($monto);
        if ($ok) {
            $this->extracciones++;
        }
        return $ok;
    }

    public function finDeMes(): void
    {
        $this->saldo = round($this->saldo * 1.02, 2);
        $this->extracciones = 0;
    }
}

class CuentaCorriente extends Cuenta
{
    public function __construct(string $titular, private float $descubierto)
    {
        parent::__construct($titular);
    }

    public function extraer(float $monto): bool
    {
        if ($this->saldo - $monto < -$this->descubierto) {
            return false;
        }
        $this->saldo -= $monto;
        return true;
    }
}

$ahorro = new CajaDeAhorro('Kira');
$ahorro->depositar(10000);
foreach ([1000, 2000, 500, 100] as $i => $monto) {
    echo "Ahorro, extracción ", $i + 1, " de $monto: ", $ahorro->extraer($monto) ? 'ok' : 'rechazada', "\n";
}
$ahorro->finDeMes();
echo "Ahorro a fin de mes: ", $ahorro->saldo(), "\n";
echo "Ahorro, extracción de 100 en el mes nuevo: ", $ahorro->extraer(100) ? 'ok' : 'rechazada', "\n";

$corriente = new CuentaCorriente('Bron', 5000);
$corriente->depositar(2000);
echo "Corriente, extrae 6000: ", $corriente->extraer(6000) ? 'ok' : 'rechazada', " (saldo ", $corriente->saldo(), ")\n";
echo "Corriente, extrae 2000: ", $corriente->extraer(2000) ? 'ok' : 'rechazada', " (saldo ", $corriente->saldo(), ")\n";
```

### Encargo R02-N04-E1 · Las entradas del teatro

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El teatro del puerto vende tres tipos de entrada. Escribí `Entrada` (función,
fila y precio base `protected`, con `precio(): float` y `__toString()`) y las
hijas:

- `EntradaEstudiante` — 40% de descuento, pero **no** para las funciones de
  estreno (se pasa `bool $estreno` al crear la entrada base);
- `EntradaVip` — un recargo fijo de $6000 y, si la fila es 1 o 2, un 10% más;
  además el `__toString()` agrega `(incluye copa de bienvenida)`.

Las hijas reutilizan `parent::precio()` y `parent::__toString()`. Vendé las
entradas del ejemplo y mostrá la recaudación por tipo (usá `get_class($entrada)`
como clave de un array asociativo).

#### Criterio de aprobación

- Las hijas usan `parent::` en lugar de repetir cálculos.
- La recaudación por tipo se arma con un array asociativo.
- La salida coincide con la esperada.

#### Salida esperada

```
La tempestad, fila 8: $12.000,00
La tempestad, fila 10: $7.200,00
Estreno: El faro, fila 5: $15.000,00
Estreno: El faro, fila 1: $23.100,00 (incluye copa de bienvenida)
La tempestad, fila 4: $18.000,00 (incluye copa de bienvenida)
Recaudación:
  Entrada: $12.000,00
  EntradaEstudiante: $22.200,00
  EntradaVip: $41.100,00
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - Las entradas del teatro: herencia con parent:: y agrupación por clase.

class Entrada
{
    public function __construct(
        protected string $funcion,
        protected int $fila,
        protected float $base,
        protected bool $estreno = false,
    ) {}

    public function precio(): float
    {
        return $this->base;
    }

    public function __toString(): string
    {
        return sprintf('%s, fila %d: $%s', $this->funcion, $this->fila, number_format($this->precio(), 2, ',', '.'));
    }
}

class EntradaEstudiante extends Entrada
{
    public function precio(): float
    {
        return $this->estreno ? parent::precio() : parent::precio() * 0.6;
    }
}

class EntradaVip extends Entrada
{
    public function precio(): float
    {
        $precio = parent::precio() + 6000;
        return $this->fila <= 2 ? $precio * 1.10 : $precio;
    }

    public function __toString(): string
    {
        return parent::__toString() . ' (incluye copa de bienvenida)';
    }
}

$vendidas = [
    new Entrada('La tempestad', 8, 12000),
    new EntradaEstudiante('La tempestad', 10, 12000),
    new EntradaEstudiante('Estreno: El faro', 5, 15000, estreno: true),
    new EntradaVip('Estreno: El faro', 1, 15000, estreno: true),
    new EntradaVip('La tempestad', 4, 12000),
];
$porTipo = [];
foreach ($vendidas as $entrada) {
    echo $entrada, "\n";
    $tipo = get_class($entrada);
    $porTipo[$tipo] = ($porTipo[$tipo] ?? 0) + $entrada->precio();
}
echo "Recaudación:\n";
foreach ($porTipo as $tipo => $monto) {
    echo "  $tipo: $", number_format($monto, 2, ',', '.'), "\n";
}
```

### Prueba del sello

#### ¿Qué hace `parent::__construct(...)`?

Ejecuta el constructor de la clase padre, para que inicialice su parte del objeto.

#### ¿Qué diferencia hay entre `private` y `protected`?

`private` lo ve solo la misma clase; `protected` lo ven también las clases hijas.

#### ¿Qué significa que un método sea `final`?

Que las clases hijas no lo pueden redefinir.

#### Si `Velero extends Embarcacion`, ¿un velero pasa `instanceof Embarcacion`?

Sí: un velero es una embarcación, y se puede usar donde se espera una `Embarcacion`.

#### ¿Cuándo no conviene heredar?

Cuando la relación no es "es un" sino "tiene un" (un barco tiene un motor): ahí se usa composición.

### Soluciones (docente)

Sale de `21-PHP/10-Herencia-Polimorfismo` (la parte de `extends` y `parent::`); las clases abstractas y el polimorfismo van en el nodo siguiente. En la misión 2, los tres errores son la firma incompatible (fatal al cargar), el `parent::__construct` que falta (fatal al ejecutar) y `private $patente` (no se ve desde la hija). En la misión 3, la cuarta extracción de la caja de ahorro se rechaza aunque haya saldo: es la regla del límite mensual, no la del saldo.

## R02-N05 · Clases abstractas y polimorfismo

```meta
tipo: tema
padre: R02-N04
precio: 10
criatura: ogre
temas: poo.abstractas, poo.polimorfismo
```

### Crónica

El capataz del Astillero tiene una lista de trabajos pendientes: un casco de velero, una hélice de remolcador, un ancla. A cada carpintero le dice lo mismo: *"Terminá tu pieza"*. Cada uno sabe cómo se termina la suya: el de velas cose, el herrero forja, el de madera lija. El capataz no necesita saber los detalles.

—Esa es la magia —dice {mentor}—. Das **una sola orden**, y cada objeto la cumple a su manera. Se llama **polimorfismo**. Y hay moldes, {heroe}, que existen solo para que otros los completen: nadie construye "una pieza" genérica.

### Objetivos

- Declarar clases y métodos abstractos.
- Entender por qué una clase abstracta no se puede instanciar.
- Aprovechar el polimorfismo: tratar objetos distintos de la misma manera.
- Reemplazar cadenas de `if` por tipo con métodos redefinidos.
- Usar el patrón "método plantilla": el padre define los pasos, las hijas los detalles.

### Antes de empezar

- Herencia, `parent::` y redefinición de métodos (R02-N04).

### Explicación

#### Clases abstractas
Algunas clases son **conceptos generales** que no tiene sentido crear: nadie
fabrica "una figura", sino un círculo o un rectángulo. Se marcan `abstract`:
```php
abstract class Figura
{
    abstract public function area(): float;      // sin cuerpo: cada hija lo define

    public function describir(): string          // un método normal, heredado
    {
        return static::class . ' de área ' . round($this->area(), 2);
    }
}
```
- Un **método abstracto** declara la firma pero no el código: cada hija está
  **obligada** a escribirlo.
- `new Figura()` da `Cannot instantiate abstract class Figura`.
- Si una hija se olvida de implementar un método abstracto:
  ```
  Class Circulo contains 1 abstract method and must therefore be declared abstract or implement the remaining methods (Figura::area)
  ```
- `static::class` da el nombre de la clase real del objeto (`Circulo`,
  `Rectangulo`).

#### Polimorfismo
```php
class Circulo extends Figura
{
    public function __construct(private float $radio) {}
    public function area(): float { return M_PI * $this->radio ** 2; }
}
class Rectangulo extends Figura
{
    public function __construct(private float $ancho, private float $alto) {}
    public function area(): float { return $this->ancho * $this->alto; }
}

$figuras = [new Circulo(1), new Rectangulo(2, 3)];
foreach ($figuras as $f) {
    echo $f->describir(), "\n";   // cada una calcula SU área
}
```
El bucle no pregunta "¿sos un círculo?": llama a `area()` y cada objeto responde
con su versión. Si mañana se agrega un `Triangulo`, el bucle no cambia.

#### Adiós a los `if` por tipo
Sin polimorfismo, el código se llena de esto:
```php
if ($tipo === 'circulo') { $area = M_PI * $r ** 2; }
elseif ($tipo === 'rectangulo') { $area = $a * $b; }
elseif … // y cada tipo nuevo obliga a tocar todos estos if
```
Con polimorfismo, cada clase sabe lo suyo. Cuando veas un `match` o un `switch`
sobre "qué tipo de cosa es", pensá si no conviene una jerarquía de clases. Ese
`if` repetido es el ogro escondido.

#### El método plantilla
El padre define **el orden de los pasos** y deja algunos abstractos:
```php
abstract class Envio
{
    public function costo(): float                 // la plantilla
    {
        return $this->base() + $this->recargo() + $this->seguro();
    }
    abstract protected function base(): float;     // cada tipo define su base
    protected function recargo(): float { return 0; }   // opcional: por defecto 0
    private function seguro(): float { return 500; }    // igual para todos
}
```
Las hijas solo completan `base()` (y `recargo()` si quieren). El cálculo general
no se repite en ningún lado.

### Código de ejemplo

```php
<?php
declare(strict_types=1);
/*
 * El capataz del Astillero: una clase abstracta y el polimorfismo.
 */
abstract class Pieza
{
    public function __construct(protected string $codigo) {}

    abstract public function horasDeTrabajo(): float;

    abstract protected function material(): string;

    // Método plantilla: igual para todas, usa lo que cada hija define.
    public function presupuesto(float $valorHora): float
    {
        return round($this->horasDeTrabajo() * $valorHora + $this->costoMaterial(), 2);
    }

    protected function costoMaterial(): float
    {
        return 0;
    }

    public function orden(): string
    {
        return sprintf('%-6s %-12s %-8s %5.1f h', $this->codigo, static::class, $this->material(), $this->horasDeTrabajo());
    }
}

class Vela extends Pieza
{
    public function __construct(string $codigo, private float $metros2)
    {
        parent::__construct($codigo);
    }

    public function horasDeTrabajo(): float
    {
        return $this->metros2 * 0.5;
    }

    protected function material(): string
    {
        return 'lona';
    }

    protected function costoMaterial(): float
    {
        return $this->metros2 * 1800;
    }
}

class Helice extends Pieza
{
    public function __construct(string $codigo, private int $palas)
    {
        parent::__construct($codigo);
    }

    public function horasDeTrabajo(): float
    {
        return 6 + $this->palas * 2.5;
    }

    protected function material(): string
    {
        return 'bronce';
    }

    protected function costoMaterial(): float
    {
        return 45000;
    }
}

class Remo extends Pieza
{
    public function horasDeTrabajo(): float
    {
        return 1.5;
    }

    protected function material(): string
    {
        return 'madera';
    }
}

$pendientes = [new Vela('V-01', 24), new Helice('H-07', 4), new Remo('R-11'), new Remo('R-12')];
$total = 0;
foreach ($pendientes as $pieza) {
    $precio = $pieza->presupuesto(7500);
    $total += $precio;
    echo $pieza->orden(), '  $', number_format($precio, 2, ',', '.'), "\n";
}
echo "Total del pedido: $", number_format($total, 2, ',', '.'), "\n";

try {
    new Pieza('X-00');
} catch (Error $e) {
    echo "No se puede: ", $e->getMessage(), "\n";
}
```

### Salida esperada

```
V-01   Vela         lona      12.0 h  $133.200,00
H-07   Helice       bronce    16.0 h  $165.000,00
R-11   Remo         madera     1.5 h  $11.250,00
R-12   Remo         madera     1.5 h  $11.250,00
Total del pedido: $320.700,00
No se puede: Cannot instantiate abstract class Pieza
```

### ¿Para qué sirve?

El polimorfismo es lo que hace que un sistema crezca sin romperse: un carrito que calcula el envío de cualquier transportista, un sistema de pagos que acepta tarjeta, transferencia o Mercado Pago con la misma llamada `cobrar()`, un juego donde cada enemigo ataca a su manera. En los frameworks, los controladores y los comandos son clases que completan métodos que el framework llama.

### Errores habituales

**Esqueleto: instanciar la abstracta.** `Cannot instantiate abstract class Pieza`:
creá una de sus hijas.

**Esqueleto: el método abstracto sin implementar.** `Class Remo contains 1 abstract
method and must therefore be declared abstract or implement the remaining methods
(Pieza::material)`: la hija tiene que escribir todos los abstractos.

**Slime: un método abstracto con cuerpo.** `abstract public function area(): float
{ … }` da error: los abstractos terminan en `;`.

**Goblin: la visibilidad más cerrada.** Si el padre lo declara `public`, la hija no
lo puede hacer `protected` ni `private`: `Access level to Remo::horasDeTrabajo()
must be public`.

**Ogro: el `if` por tipo.** `if ($pieza instanceof Vela) … elseif ($pieza
instanceof Helice)`: casi siempre es un método que falta en la jerarquía.

### Misión R02-N05-M1 · Las figuras del velero

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El velero tiene velas de distintas formas y el velero necesita saber cuánta lona
comprar. Escribí la clase abstracta `Figura` con `area(): float` y
`perimetro(): float` abstractos, y un método `ficha(): string` que muestre el
nombre de la clase (`static::class`), el área y el perímetro con dos decimales.
Implementá `Rectangulo`, `Circulo` y `TrianguloRectangulo` (catetos `a` y `b`; la
hipotenusa es `sqrt(a² + b²)`).

Mostrá las fichas de las velas del ejemplo, el total de lona (suma de áreas) y la
vela más grande (recorriendo con polimorfismo, sin preguntar el tipo).

#### Criterio de aprobación

- `Figura` es abstracta y sus hijas implementan los dos métodos.
- El total y el máximo se calculan sin `instanceof` ni `if` por tipo.
- La salida coincide con la esperada.

#### Salida esperada

```
TrianguloRectangulo área   24.00  perímetro  24.00
Rectangulo          área   22.00  perímetro  19.00
Circulo             área    7.07  perímetro   9.42
TrianguloRectangulo área    6.00  perímetro  12.00
Lona total: 59.07 m²
La más grande: TrianguloRectangulo área   24.00  perímetro  24.00
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - Las figuras del velero: clase abstracta y polimorfismo.

abstract class Figura
{
    abstract public function area(): float;

    abstract public function perimetro(): float;

    public function ficha(): string
    {
        return sprintf('%-19s área %7.2f  perímetro %6.2f', static::class, $this->area(), $this->perimetro());
    }
}

class Rectangulo extends Figura
{
    public function __construct(private float $ancho, private float $alto) {}

    public function area(): float
    {
        return $this->ancho * $this->alto;
    }

    public function perimetro(): float
    {
        return 2 * ($this->ancho + $this->alto);
    }
}

class Circulo extends Figura
{
    public function __construct(private float $radio) {}

    public function area(): float
    {
        return M_PI * $this->radio ** 2;
    }

    public function perimetro(): float
    {
        return 2 * M_PI * $this->radio;
    }
}

class TrianguloRectangulo extends Figura
{
    public function __construct(private float $a, private float $b) {}

    public function area(): float
    {
        return $this->a * $this->b / 2;
    }

    public function perimetro(): float
    {
        return $this->a + $this->b + sqrt($this->a ** 2 + $this->b ** 2);
    }
}

$velas = [new TrianguloRectangulo(6, 8), new Rectangulo(4, 5.5), new Circulo(1.5), new TrianguloRectangulo(3, 4)];
$total = 0;
$mayor = $velas[0];
foreach ($velas as $vela) {
    echo $vela->ficha(), "\n";
    $total += $vela->area();
    if ($vela->area() > $mayor->area()) {
        $mayor = $vela;
    }
}
printf("Lona total: %.2f m²\n", $total);
echo "La más grande: ", $mayor->ficha(), "\n";
```

### Misión R02-N05-M2 · Los medios de pago

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La tienda del puerto acepta varios medios de pago. Escribí la clase abstracta
`MedioDePago` con un **método plantilla** `cobrar(float $monto): string` que
calcula `monto + recargo(monto)` y devuelve el texto
`Efectivo: $10.000,00 (recargo $0,00)` (si el recargo es negativo, dice
`descuento` con el monto en positivo). `recargo()` es abstracto y `protected`.
Las hijas:

- `Efectivo` — sin recargo;
- `Tarjeta` — recargo según las **cuotas** (se pasa al crearla): 1 cuota 0%, 3
  cuotas 10%, 6 cuotas 20%, otras cantidades 35%; el nombre que muestra es
  `Tarjeta (3 cuotas)`;
- `Transferencia` — un 5% de **descuento** (recargo negativo) si el monto supera
  los $50000.

Cobrá los pagos del ejemplo.

#### Criterio de aprobación

- `cobrar` está solo en la clase abstracta; las hijas definen `recargo`.
- Hay un método `nombre()` que las hijas pueden redefinir.
- La salida coincide con la esperada.

#### Salida esperada

```
Efectivo: $10.000,00 (recargo $0,00)
Tarjeta (1 cuota): $10.000,00 (recargo $0,00)
Tarjeta (6 cuotas): $102.000,00 (recargo $17.000,00)
Tarjeta (12 cuotas): $114.750,00 (recargo $29.750,00)
Transferencia: $30.000,00 (recargo $0,00)
Transferencia: $80.750,00 (descuento $4.250,00)
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 2 - Los medios de pago: el método plantilla cobrar().

abstract class MedioDePago
{
    public function cobrar(float $monto): string
    {
        $recargo = $this->recargo($monto);
        $detalle = $recargo < 0 ? 'descuento $' . self::pesos(-$recargo) : 'recargo $' . self::pesos($recargo);
        return sprintf('%s: $%s (%s)', $this->nombre(), self::pesos($monto + $recargo), $detalle);
    }

    abstract protected function recargo(float $monto): float;

    protected function nombre(): string
    {
        return static::class;
    }

    private static function pesos(float $monto): string
    {
        return number_format($monto, 2, ',', '.');
    }
}

class Efectivo extends MedioDePago
{
    protected function recargo(float $monto): float
    {
        return 0;
    }
}

class Tarjeta extends MedioDePago
{
    public function __construct(private int $cuotas) {}

    protected function recargo(float $monto): float
    {
        $porcentaje = match ($this->cuotas) {
            1 => 0,
            3 => 0.10,
            6 => 0.20,
            default => 0.35,
        };
        return $monto * $porcentaje;
    }

    protected function nombre(): string
    {
        return "Tarjeta ({$this->cuotas} " . ($this->cuotas === 1 ? 'cuota' : 'cuotas') . ')';
    }
}

class Transferencia extends MedioDePago
{
    protected function recargo(float $monto): float
    {
        return $monto > 50000 ? -$monto * 0.05 : 0;
    }
}

$pagos = [
    [new Efectivo(), 10000],
    [new Tarjeta(1), 10000],
    [new Tarjeta(6), 85000],
    [new Tarjeta(12), 85000],
    [new Transferencia(), 30000],
    [new Transferencia(), 85000],
];
foreach ($pagos as [$medio, $monto]) {
    echo $medio->cobrar($monto), "\n";
}
```

### Misión R02-N05-M3 · Chau a los if

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Este programa calcula la tarifa de amarre con un `match` por tipo de barco, y cada
vez que llega un tipo nuevo hay que tocarlo. Reescribilo con una clase abstracta
`Barco` (nombre y eslora) con `tarifa(): float` abstracta, y las hijas `Velero`,
`Pesquero` y `Crucero`. El programa tiene que mostrar **exactamente la misma
salida** y no puede quedar ningún `match` ni `if` sobre el tipo. Después agregá un
tipo nuevo, `Yate` ($1500 por metro más $20000 fijos), sin tocar el bucle.

#### Criterio de aprobación

- No hay `match`/`if` sobre el tipo: cada clase define su `tarifa`.
- El bucle no cambia al agregar `Yate`.
- La salida coincide con la esperada (la original más el yate).

#### Código inicial

```php
<?php
$barcos = [
    ['tipo' => 'velero', 'nombre' => 'Brisa', 'eslora' => 12],
    ['tipo' => 'pesquero', 'nombre' => 'Don Pepe', 'eslora' => 18],
    ['tipo' => 'crucero', 'nombre' => 'Aurora', 'eslora' => 250],
];
foreach ($barcos as $b) {
    $tarifa = match ($b['tipo']) {
        'velero' => $b['eslora'] * 400,
        'pesquero' => $b['eslora'] * 300 * 0.5,
        'crucero' => $b['eslora'] * 900 + 150000,
    };
    echo "{$b['nombre']}: $", number_format($tarifa, 0, ',', '.'), "\n";
}
```

#### Salida esperada

```
Brisa: $4.800
Don Pepe: $2.700
Aurora: $375.000
Capricho: $53.000
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - Chau a los if: cada tipo de barco sabe su tarifa.

abstract class Barco
{
    public function __construct(public readonly string $nombre, protected float $eslora) {}

    abstract public function tarifa(): float;
}

class Velero extends Barco
{
    public function tarifa(): float
    {
        return $this->eslora * 400;
    }
}

class Pesquero extends Barco
{
    public function tarifa(): float
    {
        return $this->eslora * 300 * 0.5;    // los pesqueros pagan la mitad
    }
}

class Crucero extends Barco
{
    public function tarifa(): float
    {
        return $this->eslora * 900 + 150000;
    }
}

class Yate extends Barco
{
    public function tarifa(): float
    {
        return $this->eslora * 1500 + 20000;
    }
}

$barcos = [new Velero('Brisa', 12), new Pesquero('Don Pepe', 18), new Crucero('Aurora', 250), new Yate('Capricho', 22)];
foreach ($barcos as $b) {
    echo "{$b->nombre}: $", number_format($b->tarifa(), 0, ',', '.'), "\n";
}
```

### Encargo R02-N05-E1 · Las notificaciones del sistema

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un sistema de turnos médicos avisa a los pacientes por distintos canales. Escribí
la clase abstracta `Notificacion` (destinatario y mensaje) con un método
plantilla `enviar(): string` que:

1. valida el destinatario con `esDestinoValido()` (abstracto); si no es válido,
   devuelve `[CANAL] destino inválido: …`;
2. recorta el mensaje con `mensajeParaCanal()` (por defecto, el mensaje entero);
3. devuelve `[CANAL] a DESTINO: MENSAJE`.

Las hijas: `Email` (válido si `filter_var($d, FILTER_VALIDATE_EMAIL)` no es
`false`), `Sms` (válido si son 10 dígitos; el mensaje se corta a 40 caracteres con
`mb_substr` y `…` si era más largo) y `WhatsApp` (válido si empieza con `+549` y
tiene 13 dígitos después del `+`; el mensaje empieza con `👋 `). El `CANAL` es el
nombre de la clase en mayúsculas. Enviá las notificaciones del ejemplo.

#### Criterio de aprobación

- `enviar` es el método plantilla de la clase abstracta.
- Cada canal define su validación y, si hace falta, su recorte.
- La salida coincide con la esperada.

#### Salida esperada

```
[EMAIL] a ana.perez@correo.com.ar: Recordatorio: turno con la Dra. Molina el martes 14 a las 9:40.
[EMAIL] destino inválido: ana.perez@
[SMS] a 3804123456: Recordatorio: turno con la Dra. Molina e…
[SMS] destino inválido: 380-412345
[WHATSAPP] a +5493804123456: 👋 Recordatorio: turno con la Dra. Molina el martes 14 a las 9:40.
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - Las notificaciones del sistema: un método plantilla con pasos abstractos.

abstract class Notificacion
{
    public function __construct(protected string $destino, protected string $mensaje) {}

    public function enviar(): string
    {
        $canal = strtoupper(static::class);
        if (!$this->esDestinoValido()) {
            return "[$canal] destino inválido: {$this->destino}";
        }
        return "[$canal] a {$this->destino}: {$this->mensajeParaCanal()}";
    }

    abstract protected function esDestinoValido(): bool;

    protected function mensajeParaCanal(): string
    {
        return $this->mensaje;
    }
}

class Email extends Notificacion
{
    protected function esDestinoValido(): bool
    {
        return filter_var($this->destino, FILTER_VALIDATE_EMAIL) !== false;
    }
}

class Sms extends Notificacion
{
    protected function esDestinoValido(): bool
    {
        return strlen($this->destino) === 10 && ctype_digit($this->destino);
    }

    protected function mensajeParaCanal(): string
    {
        return mb_strlen($this->mensaje) > 40 ? mb_substr($this->mensaje, 0, 40) . '…' : $this->mensaje;
    }
}

class WhatsApp extends Notificacion
{
    protected function esDestinoValido(): bool
    {
        return str_starts_with($this->destino, '+549') && strlen($this->destino) === 14 && ctype_digit(substr($this->destino, 1));
    }

    protected function mensajeParaCanal(): string
    {
        return '👋 ' . $this->mensaje;
    }
}

$texto = 'Recordatorio: turno con la Dra. Molina el martes 14 a las 9:40.';
$avisos = [
    new Email('ana.perez@correo.com.ar', $texto),
    new Email('ana.perez@', $texto),
    new Sms('3804123456', $texto),
    new Sms('380-412345', $texto),
    new WhatsApp('+5493804123456', $texto),
];
foreach ($avisos as $aviso) {
    echo $aviso->enviar(), "\n";
}
```

### Prueba del sello

#### ¿Se puede hacer `new` de una clase abstracta?

No: da `Cannot instantiate abstract class`. Se crean objetos de sus hijas.

#### ¿Qué obliga un método abstracto?

A que cada clase hija (no abstracta) lo implemente con esa misma firma.

#### ¿Qué es el polimorfismo?

Que objetos de clases distintas respondan a la misma llamada, cada uno a su manera: el código que los usa no necesita saber de qué clase es cada uno.

#### ¿Qué es un método plantilla?

Un método del padre que define los pasos de un proceso y llama a métodos que las hijas completan.

#### ¿Qué señal indica que falta polimorfismo?

Un `if`/`match` que pregunta de qué tipo es algo para decidir qué hacer, repetido en varios lugares.

### Soluciones (docente)

Sale de `21-PHP/10-Herencia-Polimorfismo` (clases abstractas), ampliado con el método plantilla y la refactorización de la misión 3, que es el ejercicio clave del nodo. En el encargo, el emoji de WhatsApp se muestra bien en cualquier terminal moderna; si en Windows sale raro, es la consola (probar en la terminal de VS Code).

## R02-N06 · Interfaces

```meta
tipo: tema
padre: R02-N05
precio: 10
criatura: goblin
temas: poo.interfaces
```

### Crónica

En la aduana del Astillero hay un cartel con tres reglas: *"Todo lo que se cargue en un barco tiene que tener **peso**. Todo lo que se asegure tiene que tener **valor**. Todo lo que se exporte tiene que tener **país de origen**."* Un cajón de fruta cumple las tres; un pasajero, solo la primera; un cuadro, las dos primeras.

—Esos carteles son **contratos** —dice {mentor}—. No dicen qué es cada cosa ni de qué molde viene: dicen qué tiene que saber hacer para pasar. En PHP se llaman **interfaces**, {heroe}, y una clase puede firmar todos los contratos que quiera.

### Objetivos

- Declarar interfaces con métodos y constantes.
- Implementar una o varias interfaces en una clase.
- Pedir una interfaz como tipo de parámetro para aceptar objetos de clases que no tienen nada en común.
- Distinguir cuándo usar una interfaz y cuándo una clase abstracta.
- Conocer algunas interfaces de PHP: `Countable`, `Stringable` y `JsonSerializable`.

### Antes de empezar

- Clases abstractas y polimorfismo (R02-N05).

### Explicación

#### Declarar una interfaz
Una interfaz lista **qué métodos** tiene que tener una clase, sin código:
```php
interface Pesable
{
    public function pesoKg(): float;
}

interface Asegurable
{
    public const PRIMA = 0.02;          // las interfaces pueden tener constantes
    public function valorDeclarado(): float;
}
```

#### Implementarla
```php
class CajonDeFruta implements Pesable, Asegurable
{
    public function __construct(private float $kilos, private float $valor) {}

    public function pesoKg(): float { return $this->kilos; }
    public function valorDeclarado(): float { return $this->valor; }
}
```
- Una clase **hereda de una sola** clase, pero **implementa todas las interfaces**
  que quiera.
- Si falta un método del contrato:
  ```
  Class CajonDeFruta contains 1 abstract method and must therefore be declared abstract or implement the remaining methods (Asegurable::valorDeclarado)
  ```

#### Usar la interfaz como tipo
Acá está la gracia: una función que pide `Pesable` acepta **cualquier** objeto que
firme el contrato, aunque sean de clases sin relación:
```php
function cargaTotal(Pesable ...$cosas): float
{
    return array_sum(array_map(fn(Pesable $c) => $c->pesoKg(), $cosas));
}
cargaTotal(new CajonDeFruta(20, 5000), new Pasajero('Kira', 58));
```
Un pasajero y un cajón no tienen nada en común… salvo que se pueden pesar. La
función no los conoce: conoce el contrato. Si le pasás algo que no lo cumple:
```
cargaTotal(): Argument #1 must be of type Pesable, Ancla given
```

#### ¿Interfaz o clase abstracta?
| | Interfaz | Clase abstracta |
|---|---|---|
| ¿Tiene código? | no (solo firmas y constantes) | sí, puede tener métodos completos |
| ¿Propiedades? | no | sí |
| ¿Cuántas por clase? | todas las que quieras | una sola (se hereda de una) |
| Responde a | "¿qué **sabe hacer**?" | "¿qué **es**?" |

Regla práctica: para **capacidades** que comparten cosas distintas (pesable,
exportable, notificable), interfaz. Para una familia que comparte código (piezas,
cuentas), clase abstracta. Y se combinan: una clase abstracta puede implementar
una interfaz.

#### Interfaces que trae PHP
| Interfaz | Método | Para |
|---|---|---|
| `Countable` | `count(): int` | que `count($objeto)` funcione |
| `Stringable` | `__toString(): string` | se implementa sola si tenés `__toString` |
| `JsonSerializable` | `jsonSerialize(): mixed` | controlar qué sale en `json_encode($objeto)` |

```php
class Bodega implements Countable
{
    private array $cajones = [];
    public function count(): int { return count($this->cajones); }
}
echo count(new Bodega());   // 0
```

### Código de ejemplo

```php
<?php
declare(strict_types=1);
/*
 * Los carteles de la aduana: interfaces como contratos.
 */
interface Pesable
{
    public function pesoKg(): float;
}

interface Asegurable
{
    public const PRIMA = 0.02;

    public function valorDeclarado(): float;
}

class CajonDeFruta implements Pesable, Asegurable
{
    public function __construct(private string $fruta, private float $kilos, private float $valor) {}

    public function pesoKg(): float
    {
        return $this->kilos;
    }

    public function valorDeclarado(): float
    {
        return $this->valor;
    }

    public function __toString(): string
    {
        return "cajón de {$this->fruta}";
    }
}

class Pasajero implements Pesable
{
    public function __construct(private string $nombre, private float $kilos, private float $equipaje) {}

    public function pesoKg(): float
    {
        return $this->kilos + $this->equipaje;
    }

    public function __toString(): string
    {
        return "pasajero {$this->nombre}";
    }
}

class Cuadro implements Asegurable
{
    public function __construct(private string $titulo, private float $valor) {}

    public function valorDeclarado(): float
    {
        return $this->valor;
    }

    public function __toString(): string
    {
        return "cuadro «{$this->titulo}»";
    }
}

class Bodega implements Countable
{
    private array $carga = [];

    public function subir(Pesable $cosa): void
    {
        $this->carga[] = $cosa;
    }

    public function peso(): float
    {
        return array_sum(array_map(fn(Pesable $c): float => $c->pesoKg(), $this->carga));
    }

    public function count(): int
    {
        return count($this->carga);
    }
}

function seguro(Asegurable ...$cosas): float
{
    $total = 0;
    foreach ($cosas as $c) {
        $total += $c->valorDeclarado() * Asegurable::PRIMA;
    }
    return $total;
}

$manzanas = new CajonDeFruta('manzanas', 22, 18000);
$kira = new Pasajero('Kira', 58, 12);
$retrato = new Cuadro('La Capitana', 450000);

$bodega = new Bodega();
$bodega->subir($manzanas);
$bodega->subir($kira);
echo "En la bodega: ", count($bodega), " cosas, ", $bodega->peso(), " kg\n";
echo "Seguro de $manzanas y $retrato: $", number_format(seguro($manzanas, $retrato), 2, ',', '.'), "\n";

foreach ([$manzanas, $kira, $retrato] as $cosa) {
    $contratos = [];
    if ($cosa instanceof Pesable) {
        $contratos[] = 'Pesable';
    }
    if ($cosa instanceof Asegurable) {
        $contratos[] = 'Asegurable';
    }
    echo ucfirst((string) $cosa), ": ", implode(' + ', $contratos), "\n";
}

try {
    $bodega->subir($retrato);
} catch (TypeError $e) {
    echo "Un cuadro no se pesa: ", explode(', called', $e->getMessage())[0], "\n";
}
```

### Salida esperada

```
En la bodega: 2 cosas, 92 kg
Seguro de cajón de manzanas y cuadro «La Capitana»: $9.360,00
Cajón de manzanas: Pesable + Asegurable
Pasajero Kira: Pesable
Cuadro «La Capitana»: Asegurable
Un cuadro no se pesa: Bodega::subir(): Argument #1 ($cosa) must be of type Pesable, Cuadro given
```

### ¿Para qué sirve?

Las interfaces permiten cambiar una pieza por otra sin tocar el resto: un sistema que guarda datos a través de una interfaz `Repositorio` puede usar hoy archivos y mañana MariaDB; uno que envía mensajes con `Notificador` puede pasar de mail a WhatsApp. Es la base de las pruebas automáticas (se reemplaza la pieza real por una de mentira) y de todo Laravel, que está armado sobre contratos (`Illuminate\Contracts`).

### Errores habituales

**Esqueleto: el contrato incompleto.** `Class X contains 1 abstract method and must
therefore be declared abstract or implement the remaining methods (Pesable::pesoKg)`:
faltó implementar un método de la interfaz.

**Goblin: el objeto que no firmó.** `Argument #1 ($cosa) must be of type Pesable,
Cuadro given`: el objeto no implementa esa interfaz.

**Slime: `extends` con una interfaz.** Las clases **implementan** interfaces
(`implements`); `extends` es para heredar de una clase (entre interfaces sí se usa
`extends`: `interface Exportable extends Pesable`).

**Goblin: la firma distinta.** Si la interfaz dice `pesoKg(): float` y la clase
escribe `pesoKg(): int|string`, no es compatible.

**Ogro: interfaces de un solo uso.** Una interfaz que implementa una sola clase y
nunca se usa como tipo no aporta: agregala cuando haya dos cosas que la cumplan.

### Misión R02-N06-M1 · Lo que se puede exportar

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El puerto exporta productos a otras regiones. Escribí la interfaz `Exportable`
con `origen(): string` y `arancel(): float` (el porcentaje, `0.15` es 15%), y la
interfaz `Pesable` con `pesoKg(): float`. Implementalas en:

- `Vino` (bodega, litros, precio): exportable y pesable (un litro pesa 1.3 kg con
  la botella); arancel 15%;
- `Artesania` (descripción, precio, provincia): solo exportable; arancel 5%;
- `Contenedor` (código, peso): solo pesable.

Escribí `function derechoDeExportacion(Exportable $e, float $precio): float` y
`function flete(Pesable ...$cosas): float` ($120 por kilo). Calculá los derechos y
el flete de la carga del ejemplo.

#### Criterio de aprobación

- Dos interfaces; `Vino` implementa las dos.
- Las funciones piden la interfaz como tipo, no la clase.
- La salida coincide con la esperada.

#### Salida esperada

```
Derecho del vino (bodega Chañarmuyo): $81.000,00
Derecho del poncho (La Rioja): $19.000,00
Flete de vino y contenedor: $116.040,00
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - Lo que se puede exportar: dos interfaces y funciones que las piden.

interface Exportable
{
    public function origen(): string;

    public function arancel(): float;
}

interface Pesable
{
    public function pesoKg(): float;
}

class Vino implements Exportable, Pesable
{
    public function __construct(public readonly string $bodega, private float $litros, public readonly float $precio) {}

    public function origen(): string
    {
        return "bodega {$this->bodega}";
    }

    public function arancel(): float
    {
        return 0.15;
    }

    public function pesoKg(): float
    {
        return $this->litros * 1.3;
    }
}

class Artesania implements Exportable
{
    public function __construct(public readonly string $descripcion, public readonly float $precio, private string $provincia) {}

    public function origen(): string
    {
        return $this->provincia;
    }

    public function arancel(): float
    {
        return 0.05;
    }
}

class Contenedor implements Pesable
{
    public function __construct(public readonly string $codigo, private float $kilos) {}

    public function pesoKg(): float
    {
        return $this->kilos;
    }
}

function derechoDeExportacion(Exportable $e, float $precio): float
{
    return $precio * $e->arancel();
}

function flete(Pesable ...$cosas): float
{
    return array_sum(array_map(fn(Pesable $c): float => $c->pesoKg(), $cosas)) * 120;
}

$torrontes = new Vino('Chañarmuyo', 90, 540000);
$poncho = new Artesania('poncho de vicuña', 380000, 'La Rioja');
$caja = new Contenedor('CX-77', 850);

echo "Derecho del vino (", $torrontes->origen(), "): $", number_format(derechoDeExportacion($torrontes, $torrontes->precio), 2, ',', '.'), "\n";
echo "Derecho del poncho (", $poncho->origen(), "): $", number_format(derechoDeExportacion($poncho, $poncho->precio), 2, ',', '.'), "\n";
echo "Flete de vino y contenedor: $", number_format(flete($torrontes, $caja), 2, ',', '.'), "\n";
```

### Misión R02-N06-M2 · La bitácora contable

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí la clase `Bitacora` que guarda anotaciones (textos) en un array privado e
implementa:

- `Countable` — `count($bitacora)` da la cantidad de anotaciones;
- `JsonSerializable` — `json_encode($bitacora)` produce
  `{"barco":"Gaviota","anotaciones":["…","…"],"total":2}`;
- `Stringable` (con `__toString`) — una anotación por renglón, numeradas.

Con `anotar(string $texto): void` que ignora textos vacíos. Mostrá los tres usos
con las anotaciones del ejemplo. Para el JSON usá
`json_encode($bitacora, JSON_UNESCAPED_UNICODE)` para que se vean las tildes.

#### Criterio de aprobación

- Implementa las tres interfaces de PHP.
- `count()` y `json_encode()` funcionan directamente sobre el objeto.
- La salida coincide con la esperada.

#### Salida esperada

```
Anotaciones: 3
1. Zarpamos del muelle 3 a las 6:10.
2. Viento del sur, 15 nudos.
3. Llegamos al Valle con toda la carga.
{"barco":"Gaviota","anotaciones":["Zarpamos del muelle 3 a las 6:10.","Viento del sur, 15 nudos.","Llegamos al Valle con toda la carga."],"total":3}
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 2 - La bitácora contable: Countable, JsonSerializable y Stringable.

class Bitacora implements Countable, JsonSerializable, Stringable
{
    private array $anotaciones = [];

    public function __construct(private string $barco) {}

    public function anotar(string $texto): void
    {
        if (trim($texto) !== '') {
            $this->anotaciones[] = trim($texto);
        }
    }

    public function count(): int
    {
        return count($this->anotaciones);
    }

    public function jsonSerialize(): array
    {
        return ['barco' => $this->barco, 'anotaciones' => $this->anotaciones, 'total' => count($this)];
    }

    public function __toString(): string
    {
        $renglones = [];
        foreach ($this->anotaciones as $i => $texto) {
            $renglones[] = ($i + 1) . ". $texto";
        }
        return implode("\n", $renglones);
    }
}

$bitacora = new Bitacora('Gaviota');
$bitacora->anotar('Zarpamos del muelle 3 a las 6:10.');
$bitacora->anotar('   ');
$bitacora->anotar('Viento del sur, 15 nudos.');
$bitacora->anotar('Llegamos al Valle con toda la carga.');

echo "Anotaciones: ", count($bitacora), "\n";
echo $bitacora, "\n";
echo json_encode($bitacora, JSON_UNESCAPED_UNICODE), "\n";
```

### Misión R02-N06-M3 · El guardián de los contratos

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El puerto tiene una **interfaz** `Almacenamiento` para guardar mensajes, con
`guardar(string $clave, string $texto): void`, `leer(string $clave): ?string` y
`claves(): array`. Hay que poder cambiar dónde se guardan sin tocar el resto del
programa. Implementá:

- `AlmacenEnMemoria` — con un array privado;
- `AlmacenEnArchivo` — cada mensaje es un archivo `CLAVE.txt` en una carpeta que
  se pasa al crearlo (usá `file_put_contents`, `file_get_contents`,
  `file_exists`, `glob` y `basename`; creá la carpeta con `mkdir` si no existe).

Escribí `function correo(Almacenamiento $a): void` que guarde tres mensajes, lea
uno que existe y uno que no, y liste las claves ordenadas. Llamala con los dos
almacenes (para el de archivo, usá la carpeta `sys_get_temp_dir() . '/correo-puerto'`
y borrá sus archivos al empezar para que la prueba sea repetible).

#### Criterio de aprobación

- `correo()` pide la interfaz, no una clase concreta.
- Las dos implementaciones dan la misma salida.
- La salida coincide con la esperada.

#### Salida esperada

```
En memoria:
  forjas: Pedido de 200 lingotes.
  luna: (no hay)
  claves: forjas, imperio, valle
En archivos:
  forjas: Pedido de 200 lingotes.
  luna: (no hay)
  claves: forjas, imperio, valle
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - El guardián de los contratos: la misma función con dos implementaciones.

interface Almacenamiento
{
    public function guardar(string $clave, string $texto): void;

    public function leer(string $clave): ?string;

    public function claves(): array;
}

class AlmacenEnMemoria implements Almacenamiento
{
    private array $datos = [];

    public function guardar(string $clave, string $texto): void
    {
        $this->datos[$clave] = $texto;
    }

    public function leer(string $clave): ?string
    {
        return $this->datos[$clave] ?? null;
    }

    public function claves(): array
    {
        $claves = array_keys($this->datos);
        sort($claves);
        return $claves;
    }
}

class AlmacenEnArchivo implements Almacenamiento
{
    public function __construct(private string $carpeta)
    {
        if (!is_dir($carpeta)) {
            mkdir($carpeta, 0775, true);
        }
    }

    private function ruta(string $clave): string
    {
        return $this->carpeta . '/' . $clave . '.txt';
    }

    public function guardar(string $clave, string $texto): void
    {
        file_put_contents($this->ruta($clave), $texto);
    }

    public function leer(string $clave): ?string
    {
        return file_exists($this->ruta($clave)) ? file_get_contents($this->ruta($clave)) : null;
    }

    public function claves(): array
    {
        $claves = array_map(fn(string $f): string => basename($f, '.txt'), glob($this->carpeta . '/*.txt'));
        sort($claves);
        return $claves;
    }
}

function correo(Almacenamiento $a): void
{
    $a->guardar('valle', 'Llegan 3 barcos el martes.');
    $a->guardar('forjas', 'Pedido de 200 lingotes.');
    $a->guardar('imperio', 'Cambió la tarifa del denario.');
    echo "  forjas: ", $a->leer('forjas') ?? '(no hay)', "\n";
    echo "  luna: ", $a->leer('luna') ?? '(no hay)', "\n";
    echo "  claves: ", implode(', ', $a->claves()), "\n";
}

$carpeta = sys_get_temp_dir() . '/correo-puerto';
foreach (glob($carpeta . '/*.txt') ?: [] as $archivo) {
    unlink($archivo);
}

echo "En memoria:\n";
correo(new AlmacenEnMemoria());
echo "En archivos:\n";
correo(new AlmacenEnArchivo($carpeta));
```

### Encargo R02-N06-E1 · Los descuentos combinables

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un supermercado del barrio combina promociones. Escribí la interfaz `Promocion`
con `aplicar(float $total, array $carrito): float` (devuelve el **descuento**, no
el total) y `descripcion(): string`. Implementá:

- `PorcentajeDia` — un porcentaje los días que se indiquen (se le pasan el día de
  la compra y el día de la promo, `'miércoles'`, y el porcentaje);
- `LlevaTresPagaDos` — sobre un producto: por cada 3 unidades, una gratis;
- `MontoMinimo` — $2000 de descuento si el total supera los $25000.

Escribí la clase `Caja` que recibe una lista de `Promocion` y un método
`cobrar(array $carrito): void` (el carrito es `producto => [cantidad, precio]`) que
muestra el subtotal, cada promo que aplique (descuento mayor que 0) y el total.

#### Criterio de aprobación

- `Caja` solo conoce la interfaz `Promocion`.
- Agregar una promo nueva no cambia `Caja`.
- La salida coincide con la esperada.

#### Salida esperada

```
Subtotal: $35.400,00
  - 10% los miércoles: $3.540,00
  - 3x2 en yerba: $8.400,00
  - $2000 menos en compras de más de $25000: $2.000,00
Total: $21.460,00
---
Subtotal: $3.300,00
  - 10% los miércoles: $330,00
Total: $2.970,00
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - Los descuentos combinables: una caja que solo conoce la interfaz.

interface Promocion
{
    public function aplicar(float $total, array $carrito): float;

    public function descripcion(): string;
}

class PorcentajeDia implements Promocion
{
    public function __construct(private string $hoy, private string $dia, private float $porcentaje) {}

    public function aplicar(float $total, array $carrito): float
    {
        return $this->hoy === $this->dia ? $total * $this->porcentaje / 100 : 0;
    }

    public function descripcion(): string
    {
        return "{$this->porcentaje}% los {$this->dia}";
    }
}

class LlevaTresPagaDos implements Promocion
{
    public function __construct(private string $producto) {}

    public function aplicar(float $total, array $carrito): float
    {
        if (!isset($carrito[$this->producto])) {
            return 0;
        }
        [$cantidad, $precio] = $carrito[$this->producto];
        return intdiv($cantidad, 3) * $precio;
    }

    public function descripcion(): string
    {
        return "3x2 en {$this->producto}";
    }
}

class MontoMinimo implements Promocion
{
    public function aplicar(float $total, array $carrito): float
    {
        return $total > 25000 ? 2000 : 0;
    }

    public function descripcion(): string
    {
        return '$2000 menos en compras de más de $25000';
    }
}

class Caja
{
    /** @param Promocion[] $promos */
    public function __construct(private array $promos) {}

    public function cobrar(array $carrito): void
    {
        $subtotal = 0;
        foreach ($carrito as [$cantidad, $precio]) {
            $subtotal += $cantidad * $precio;
        }
        echo "Subtotal: $", number_format($subtotal, 2, ',', '.'), "\n";
        $descuentos = 0;
        foreach ($this->promos as $promo) {
            $descuento = $promo->aplicar($subtotal, $carrito);
            if ($descuento > 0) {
                echo "  - ", $promo->descripcion(), ": $", number_format($descuento, 2, ',', '.'), "\n";
                $descuentos += $descuento;
            }
        }
        echo "Total: $", number_format($subtotal - $descuentos, 2, ',', '.'), "\n";
    }
}

$caja = new Caja([new PorcentajeDia('miércoles', 'miércoles', 10), new LlevaTresPagaDos('yerba'), new MontoMinimo()]);
$caja->cobrar(['yerba' => [7, 4200], 'fideos' => [2, 1100], 'aceite' => [1, 3800]]);
echo "---\n";
$caja->cobrar(['fideos' => [3, 1100]]);
```

### Prueba del sello

#### ¿Cuántas clases puede heredar una clase y cuántas interfaces puede implementar?

Hereda de una sola clase, pero puede implementar todas las interfaces que quiera.

#### ¿Qué puede tener una interfaz?

Firmas de métodos públicos y constantes; no tiene propiedades ni código.

#### ¿Qué gana una función que pide una interfaz como tipo de parámetro?

Acepta cualquier objeto que cumpla el contrato, sin importar su clase: se puede cambiar la implementación sin tocar la función.

#### ¿Para qué sirve implementar `Countable`?

Para que `count($objeto)` funcione sobre ese objeto.

#### ¿Cuándo conviene una interfaz y cuándo una clase abstracta?

Interfaz para capacidades que comparten cosas distintas ("qué sabe hacer"); clase abstracta para una familia que comparte código ("qué es").

### Soluciones (docente)

Sale de `21-PHP/11-Interfaces-Traits` (la parte de interfaces; los traits van en el nodo siguiente). La misión 3 anticipa el patrón repositorio de la rama de MariaDB: la misma función trabaja con memoria o con archivos, y más adelante con la base. Usa la carpeta temporal del sistema y la limpia al empezar para que se pueda ejecutar muchas veces.

## R02-N07 · Traits y composición

```meta
tipo: tema
padre: R02-N06
precio: 10
criatura: troll
temas: poo.composicion, diseno.inyeccion
```

### Crónica

Un aprendiz del Astillero quiere que su bote tenga motor, así que dibuja un bote que **es** un motor con casco. El maestro carpintero le borra el dibujo: *"Un bote no es un motor. Un bote **tiene** un motor. Y mañana le vas a querer poner uno más grande."* Del otro lado del taller, un herrero pega la misma etiqueta de fecha de fabricación en todas las piezas, sean velas, remos o anclas.

—Hay dos maneras de reusar sin heredar —dice {mentor}—. Armar un objeto **con** otros objetos adentro, que se pueden cambiar. Y pegarle a varias clases el mismo pedacito de código, como esa etiqueta. Lo primero se llama **composición**; lo segundo, **trait**. Y ojo, {heroe}: la composición casi siempre gana.

### Objetivos

- Preferir la composición ("tiene un") a la herencia cuando no hay un "es un".
- Recibir las piezas por el constructor (inyección de dependencias) para poder cambiarlas.
- Delegar: que un objeto le pida el trabajo a otro.
- Escribir y usar traits para compartir código entre clases sin relación.
- Conocer los riesgos de los traits.

### Antes de empezar

- Herencia (R02-N04) e interfaces (R02-N06).

### Explicación

#### Composición: armar objetos con objetos
```php
class Motor
{
    public function __construct(private int $hp) {}
    public function velocidadMaxima(float $pesoTon): float
    {
        return round($this->hp / $pesoTon / 2, 1);
    }
}

class Bote
{
    public function __construct(private string $nombre, private float $pesoTon, private Motor $motor) {}

    public function velocidad(): float
    {
        return $this->motor->velocidadMaxima($this->pesoTon);   // delega
    }

    public function cambiarMotor(Motor $nuevo): void
    {
        $this->motor = $nuevo;
    }
}
$bote = new Bote('Lucero', 2, new Motor(40));
```
- El bote **tiene** un motor (una propiedad).
- El bote no sabe calcular la velocidad: se lo **delega** al motor.
- El motor se puede **cambiar** en cualquier momento. Con herencia, el tipo de
  motor quedaría fijo para siempre.

#### Inyección de dependencias
Fijate que el bote **no hace** `new Motor(...)` adentro: lo **recibe** por el
constructor. Eso se llama **inyección de dependencias** y es clave:
- se puede armar el bote con cualquier motor;
- si el parámetro es una **interfaz** (`Propulsion`), sirve un motor, una vela o
  unos remos;
- en las pruebas se le pasa un motor "de mentira".

Laravel hace esto automáticamente en todos sus controladores.

#### Traits: pegar código en varias clases
Un **trait** es un paquete de métodos (y propiedades) que se "copia" dentro de
cualquier clase con `use`:
```php
trait ConFechaDeFabricacion
{
    private string $fabricado = '';

    public function marcarFabricado(string $fecha): void
    {
        $this->fabricado = $fecha;
    }

    public function fabricado(): string
    {
        return $this->fabricado === '' ? 'sin fecha' : $this->fabricado;
    }
}

class Vela   { use ConFechaDeFabricacion; }
class Ancla  { use ConFechaDeFabricacion; }
```
`Vela` y `Ancla` no tienen nada en común para heredar, pero las dos ganan esos
métodos. Una clase puede usar varios traits (`use A, B;`).

#### Cuidado con los traits
- Un trait **no es un tipo**: no se puede pedir `ConFechaDeFabricacion $x` como
  parámetro. Para eso, una interfaz (y el trait la implementa por las clases).
- Si dos traits traen un método con el mismo nombre, hay conflicto y hay que
  resolverlo a mano (`insteadof`).
- Esconden de dónde sale el código: si una clase usa cinco traits, cuesta saber
  qué hace. Usalos para cosas chicas y transversales (fechas, registro, formato).

#### La regla del Astillero
1. ¿Es un "es un" verdadero? → herencia.
2. ¿Es un "tiene un"? → composición (una propiedad, recibida por el constructor).
3. ¿Es un pedacito de código repetido en clases sin relación? → trait (o una
   clase aparte con la que se compone).

### Código de ejemplo

```php
<?php
declare(strict_types=1);
/*
 * El bote que tiene un motor: composición, delegación y un trait.
 */
interface Propulsion
{
    public function empuje(): float;

    public function descripcion(): string;
}

class Motor implements Propulsion
{
    public function __construct(private int $hp) {}

    public function empuje(): float
    {
        return $this->hp * 1.0;
    }

    public function descripcion(): string
    {
        return "motor de {$this->hp} HP";
    }
}

class Vela implements Propulsion
{
    public function __construct(private float $metros2, private float $vientoNudos) {}

    public function empuje(): float
    {
        return $this->metros2 * $this->vientoNudos * 0.1;
    }

    public function descripcion(): string
    {
        return "vela de {$this->metros2} m² con viento de {$this->vientoNudos} nudos";
    }
}

trait ConRegistro
{
    private array $registro = [];

    protected function anotar(string $texto): void
    {
        $this->registro[] = $texto;
    }

    public function registro(): array
    {
        return $this->registro;
    }
}

class Bote
{
    use ConRegistro;

    public function __construct(private string $nombre, private float $pesoTon, private Propulsion $propulsion)
    {
        $this->anotar("botado con {$propulsion->descripcion()}");
    }

    public function velocidad(): float
    {
        return round($this->propulsion->empuje() / $this->pesoTon / 2, 1);
    }

    public function cambiarPropulsion(Propulsion $nueva): void
    {
        $this->anotar("cambia a {$nueva->descripcion()}");
        $this->propulsion = $nueva;
    }

    public function __toString(): string
    {
        return "{$this->nombre}: {$this->velocidad()} nudos ({$this->propulsion->descripcion()})";
    }
}

$bote = new Bote('Lucero', 2, new Motor(40));
echo $bote, "\n";
$bote->cambiarPropulsion(new Vela(18, 12));
echo $bote, "\n";
$bote->cambiarPropulsion(new Motor(90));
echo $bote, "\n";
echo "Registro:\n";
foreach ($bote->registro() as $i => $linea) {
    echo "  ", $i + 1, ". $linea\n";
}
```

### Salida esperada

```
Lucero: 10 nudos (motor de 40 HP)
Lucero: 5.4 nudos (vela de 18 m² con viento de 12 nudos)
Lucero: 22.5 nudos (motor de 90 HP)
Registro:
  1. botado con motor de 40 HP
  2. cambia a vela de 18 m² con viento de 12 nudos
  3. cambia a motor de 90 HP
```

### ¿Para qué sirve?

Los sistemas grandes se arman como un mecano: un `ServicioDePedidos` que **tiene** un repositorio, un calculador de envíos y un notificador, todos recibidos por el constructor. Cambiar de transportista o de base de datos es pasarle otra pieza. Laravel usa traits en todos lados (`HasFactory`, `Notifiable`, `SoftDeletes`): cuando los veas en un modelo, vas a saber qué son.

### Errores habituales

**Troll: heredar en lugar de componer.** `class Bote extends Motor` compila, pero un
bote no es un motor: después no se puede cambiar el motor ni tener dos.

**Troll: el `new` escondido.** Si el bote hace `new Motor(40)` adentro de su
constructor, queda atado a ese motor. Recibilo por parámetro.

**Esqueleto: el trait como tipo.** `function f(ConRegistro $x)` da error cuando le
pasás un objeto: un trait no es un tipo. Usá una interfaz.

**Slime: dos traits con el mismo método.** `Trait method X::m has not been applied
as Y::m, because of collision with Z::m`: resolvelo con `insteadof` o renombrá.

**Ogro: la clase con cinco traits.** Nadie entiende de dónde sale cada método.
Si un trait crece, probablemente es una clase aparte para componer.

### Misión R02-N07-M1 · La linterna del faro

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El faro tiene una **linterna** que usa una **fuente de luz** intercambiable.
Escribí la interfaz `FuenteDeLuz` con `lumenes(): int`, `consumoWatts(): float` y
`nombre(): string`, e implementala en `Lampara` (incandescente: 1500 lúmenes,
100 W), `Led` (se le pasan los watts; da 110 lúmenes por watt) y `Candil` (200
lúmenes, 0 W). La clase `Linterna` **recibe** una fuente por el constructor y
tiene:

- `alcanceMillas(): float` — `sqrt(lúmenes) / 5`, con un decimal;
- `costoNoche(int $horas, float $precioKwh): float` — watts × horas / 1000 × precio;
- `cambiarFuente(FuenteDeLuz $f): void`.

Probá la linterna con las tres fuentes, 12 horas por noche a $95 el kWh.

#### Criterio de aprobación

- `Linterna` compone una `FuenteDeLuz` recibida por el constructor.
- Los cálculos se delegan en la fuente.
- La salida coincide con la esperada.

#### Salida esperada

```
lámpara incandescente: 1500 lm, alcance 7.7 millas, $114.00 por noche
LED de 30 W: 3300 lm, alcance 11.5 millas, $34.20 por noche
candil de aceite: 200 lm, alcance 2.8 millas, $0.00 por noche
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - La linterna del faro: composición con una pieza intercambiable.

interface FuenteDeLuz
{
    public function lumenes(): int;

    public function consumoWatts(): float;

    public function nombre(): string;
}

class Lampara implements FuenteDeLuz
{
    public function lumenes(): int
    {
        return 1500;
    }

    public function consumoWatts(): float
    {
        return 100;
    }

    public function nombre(): string
    {
        return 'lámpara incandescente';
    }
}

class Led implements FuenteDeLuz
{
    public function __construct(private float $watts) {}

    public function lumenes(): int
    {
        return (int) ($this->watts * 110);
    }

    public function consumoWatts(): float
    {
        return $this->watts;
    }

    public function nombre(): string
    {
        return "LED de {$this->watts} W";
    }
}

class Candil implements FuenteDeLuz
{
    public function lumenes(): int
    {
        return 200;
    }

    public function consumoWatts(): float
    {
        return 0;
    }

    public function nombre(): string
    {
        return 'candil de aceite';
    }
}

class Linterna
{
    public function __construct(private FuenteDeLuz $fuente) {}

    public function cambiarFuente(FuenteDeLuz $fuente): void
    {
        $this->fuente = $fuente;
    }

    public function alcanceMillas(): float
    {
        return round(sqrt($this->fuente->lumenes()) / 5, 1);
    }

    public function costoNoche(int $horas, float $precioKwh): float
    {
        return round($this->fuente->consumoWatts() * $horas / 1000 * $precioKwh, 2);
    }

    public function informe(): string
    {
        return sprintf('%s: %d lm, alcance %.1f millas, $%.2f por noche', $this->fuente->nombre(), $this->fuente->lumenes(), $this->alcanceMillas(), $this->costoNoche(12, 95));
    }
}

$linterna = new Linterna(new Lampara());
echo $linterna->informe(), "\n";
$linterna->cambiarFuente(new Led(30));
echo $linterna->informe(), "\n";
$linterna->cambiarFuente(new Candil());
echo $linterna->informe(), "\n";
```

### Misión R02-N07-M2 · El sello de auditoría

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La oficina del puerto quiere saber **quién** creó y modificó cada registro. Escribí
el trait `Auditable` con:

- propiedades privadas `$creadoPor` y `$modificaciones` (un array);
- `registrarCreacion(string $usuario): void`;
- `registrarCambio(string $usuario, string $detalle): void`;
- `historial(): string` — `creado por Ana; 2 cambio/s (último: Bron, cambió el precio)`.

Usalo en dos clases sin relación: `Producto` (nombre, precio, con
`cambiarPrecio(float $precio, string $usuario)`) y `Proveedor` (razón social,
teléfono, con `cambiarTelefono(string $tel, string $usuario)`). Los métodos de
cambio registran el cambio con el trait. Mostrá el historial de cada uno después
de los cambios del ejemplo.

#### Criterio de aprobación

- El trait se usa en dos clases que no heredan una de otra.
- Los métodos de cambio usan los métodos del trait.
- La salida coincide con la esperada.

#### Salida esperada

```
Yerba: creado por Ana; 2 cambio/s (último: Ana, cambió el precio de 4500 a 4650)
Molino: creado por Kira; 0 cambio/s
Molino: creado por Kira; 1 cambio/s (último: Bron, cambió el teléfono a 380-4999999)
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 2 - El sello de auditoría: un trait en dos clases sin relación.

trait Auditable
{
    private string $creadoPor = '';
    private array $modificaciones = [];

    public function registrarCreacion(string $usuario): void
    {
        $this->creadoPor = $usuario;
    }

    public function registrarCambio(string $usuario, string $detalle): void
    {
        $this->modificaciones[] = ['usuario' => $usuario, 'detalle' => $detalle];
    }

    public function historial(): string
    {
        $texto = "creado por {$this->creadoPor}; " . count($this->modificaciones) . ' cambio/s';
        if ($this->modificaciones !== []) {
            $ultimo = end($this->modificaciones);
            $texto .= " (último: {$ultimo['usuario']}, {$ultimo['detalle']})";
        }
        return $texto;
    }
}

class Producto
{
    use Auditable;

    public function __construct(private string $nombre, private float $precio, string $usuario)
    {
        $this->registrarCreacion($usuario);
    }

    public function cambiarPrecio(float $precio, string $usuario): void
    {
        $this->registrarCambio($usuario, "cambió el precio de {$this->precio} a $precio");
        $this->precio = $precio;
    }
}

class Proveedor
{
    use Auditable;

    public function __construct(private string $razonSocial, private string $telefono, string $usuario)
    {
        $this->registrarCreacion($usuario);
    }

    public function cambiarTelefono(string $telefono, string $usuario): void
    {
        $this->registrarCambio($usuario, "cambió el teléfono a $telefono");
        $this->telefono = $telefono;
    }
}

$yerba = new Producto('Yerba 1 kg', 4200, 'Ana');
$yerba->cambiarPrecio(4500, 'Bron');
$yerba->cambiarPrecio(4650, 'Ana');
$molino = new Proveedor('Molino del Puerto SA', '380-4123456', 'Kira');

echo "Yerba: ", $yerba->historial(), "\n";
echo "Molino: ", $molino->historial(), "\n";
$molino->cambiarTelefono('380-4999999', 'Bron');
echo "Molino: ", $molino->historial(), "\n";
```

### Misión R02-N07-M3 · El heredero equivocado

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Alguien armó un `Pedido` que **hereda** de `CalculadoraDeEnvio` solo para usar su
método, y ahora el pedido "es" una calculadora y no se le puede cambiar el
transportista. Reescribilo con **composición**: una interfaz `Envio` con
`costo(float $kilos): float` y `nombre(): string`, dos implementaciones (`Correo`
—$800 fijos más $150 por kilo— y `Moto` —$2500 fijos, solo hasta 5 kg: si pesa
más, lanza `InvalidArgumentException`—), y un `Pedido` que **recibe** el envío por
el constructor. Mostrá el mismo pedido con los dos envíos y un pedido pesado con
moto.

#### Criterio de aprobación

- `Pedido` ya no hereda de nada: compone un `Envio`.
- El envío se recibe por el constructor (o un método para cambiarlo).
- La salida coincide con la esperada.

#### Código inicial

```php
<?php
class CalculadoraDeEnvio
{
    public function costoEnvio(float $kilos): float { return 800 + 150 * $kilos; }
}

class Pedido extends CalculadoraDeEnvio
{
    public function __construct(private float $subtotal, private float $kilos) {}
    public function total(): float { return $this->subtotal + $this->costoEnvio($this->kilos); }
}

echo (new Pedido(12000, 3))->total(), "\n";
```

#### Salida esperada

```
Pedido de 3 kg por correo: $13250
Pedido de 3 kg por moto: $14500
No se puede: La moto lleva hasta 5 kg (este pesa 12)
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - El heredero equivocado: de herencia a composición.

interface Envio
{
    public function costo(float $kilos): float;

    public function nombre(): string;
}

class Correo implements Envio
{
    public function costo(float $kilos): float
    {
        return 800 + 150 * $kilos;
    }

    public function nombre(): string
    {
        return 'correo';
    }
}

class Moto implements Envio
{
    public function costo(float $kilos): float
    {
        if ($kilos > 5) {
            throw new InvalidArgumentException("La moto lleva hasta 5 kg (este pesa $kilos)");
        }
        return 2500;
    }

    public function nombre(): string
    {
        return 'moto';
    }
}

class Pedido
{
    public function __construct(private float $subtotal, private float $kilos, private Envio $envio) {}

    public function total(): float
    {
        return $this->subtotal + $this->envio->costo($this->kilos);
    }

    public function resumen(): string
    {
        return "Pedido de {$this->kilos} kg por {$this->envio->nombre()}: $" . $this->total();
    }
}

echo (new Pedido(12000, 3, new Correo()))->resumen(), "\n";
echo (new Pedido(12000, 3, new Moto()))->resumen(), "\n";
try {
    echo (new Pedido(30000, 12, new Moto()))->resumen(), "\n";
} catch (InvalidArgumentException $e) {
    echo "No se puede: ", $e->getMessage(), "\n";
}
```

### Encargo R02-N07-E1 · El sistema de alarmas del depósito

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una empresa de seguridad instala alarmas en depósitos. Una `Central` **tiene**
varios sensores y varios avisadores, todos recibidos por el constructor:

- interfaz `Sensor` con `lugar(): string` y `activado(array $lecturas): bool`;
  implementaciones `SensorPuerta` (activado si `$lecturas['puerta_abierta']` es
  `true`) y `SensorTemperatura` (activado si `$lecturas['temperatura']` supera un
  máximo que se pasa al crearlo);
- interfaz `Avisador` con `avisar(string $mensaje): string`; implementaciones
  `Sirena` (`UUUUUH: …`) y `Mensaje` (`SMS a 380…: …`, el número se pasa al crearlo).

`Central::revisar(array $lecturas): void` revisa todos los sensores y, por cada uno
activado, avisa por **todos** los avisadores. Si no hay nada, muestra `Todo en
orden`. Usá un trait `ConHora` que tenga `hora(): string` y que devuelva una hora
fija que se configura con `fijarHora(string $h)` (para que la salida sea
repetible), y usalo en la central para anteponer la hora a cada aviso. Revisá las
tres rondas del ejemplo.

#### Criterio de aprobación

- La central compone sensores y avisadores recibidos por el constructor.
- Agregar un sensor o un avisador nuevo no cambia `Central`.
- Usa un trait para la hora.
- La salida coincide con la esperada.

#### Salida esperada

```
[22:00] Todo en orden
[01:30] UUUUUH: alarma en portón norte
[01:30] SMS a 3804123456: alarma en portón norte
[04:15] UUUUUH: alarma en portón norte
[04:15] SMS a 3804123456: alarma en portón norte
[04:15] UUUUUH: alarma en cámara de frío
[04:15] SMS a 3804123456: alarma en cámara de frío
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - El sistema de alarmas del depósito: composición de muchas piezas y un trait.

interface Sensor
{
    public function lugar(): string;

    public function activado(array $lecturas): bool;
}

interface Avisador
{
    public function avisar(string $mensaje): string;
}

class SensorPuerta implements Sensor
{
    public function __construct(private string $lugar) {}

    public function lugar(): string
    {
        return $this->lugar;
    }

    public function activado(array $lecturas): bool
    {
        return ($lecturas['puerta_abierta'] ?? false) === true;
    }
}

class SensorTemperatura implements Sensor
{
    public function __construct(private string $lugar, private float $maxima) {}

    public function lugar(): string
    {
        return $this->lugar;
    }

    public function activado(array $lecturas): bool
    {
        return ($lecturas['temperatura'] ?? 0) > $this->maxima;
    }
}

class Sirena implements Avisador
{
    public function avisar(string $mensaje): string
    {
        return "UUUUUH: $mensaje";
    }
}

class Mensaje implements Avisador
{
    public function __construct(private string $telefono) {}

    public function avisar(string $mensaje): string
    {
        return "SMS a {$this->telefono}: $mensaje";
    }
}

trait ConHora
{
    private string $hora = '00:00';

    public function fijarHora(string $hora): void
    {
        $this->hora = $hora;
    }

    public function hora(): string
    {
        return $this->hora;
    }
}

class Central
{
    use ConHora;

    /**
     * @param Sensor[] $sensores
     * @param Avisador[] $avisadores
     */
    public function __construct(private array $sensores, private array $avisadores) {}

    public function revisar(array $lecturas): void
    {
        $hubo = false;
        foreach ($this->sensores as $sensor) {
            if (!$sensor->activado($lecturas)) {
                continue;
            }
            $hubo = true;
            foreach ($this->avisadores as $avisador) {
                echo "[{$this->hora()}] ", $avisador->avisar("alarma en {$sensor->lugar()}"), "\n";
            }
        }
        if (!$hubo) {
            echo "[{$this->hora()}] Todo en orden\n";
        }
    }
}

$central = new Central(
    [new SensorPuerta('portón norte'), new SensorTemperatura('cámara de frío', 8)],
    [new Sirena(), new Mensaje('3804123456')],
);
$rondas = [
    ['22:00', ['puerta_abierta' => false, 'temperatura' => 4]],
    ['01:30', ['puerta_abierta' => true, 'temperatura' => 5]],
    ['04:15', ['puerta_abierta' => true, 'temperatura' => 11.5]],
];
foreach ($rondas as [$hora, $lecturas]) {
    $central->fijarHora($hora);
    $central->revisar($lecturas);
}
```

### Prueba del sello

#### ¿Cuándo se usa composición en lugar de herencia?

Cuando la relación es "tiene un" (un bote tiene un motor) y no "es un".

#### ¿Qué es la inyección de dependencias?

Recibir las piezas que un objeto necesita (por el constructor, casi siempre) en lugar de crearlas adentro con `new`, para poder cambiarlas.

#### ¿Qué es delegar?

Que un objeto le pida a otro que haga una parte del trabajo (el bote le pide la velocidad al motor).

#### ¿Qué es un trait?

Un paquete de métodos y propiedades que se incorpora a una clase con `use`, para compartir código entre clases sin relación.

#### ¿Se puede usar un trait como tipo de un parámetro?

No: un trait no es un tipo. Para eso se usa una interfaz.

### Soluciones (docente)

Sale de `21-PHP/11-Interfaces-Traits` (traits) y `16-Composicion-Delegacion` del capítulo de Java, adaptado. La idea central del nodo es la inyección de dependencias: se retoma en R04 (repositorios) y en la Senda de Laravel (el contenedor). En el encargo, el trait `ConHora` usa una hora fija a propósito para que la salida sea repetible; en un sistema real devolvería `date('H:i')`.

## R02-N08 · Enums y fechas

```meta
tipo: tema
padre: R02-N07
precio: 10
criatura: goblin
temas: prog.enums, prog.fechas
```

### Crónica

En el despacho de pasajes, los empleados anotaban el estado de cada reserva a mano: *"pagado"*, *"Pagada"*, *"pago ok"*, *"PAG"*. Nadie sabía cuántas reservas estaban realmente pagadas. Y con las fechas era peor: *"3/10"*, *"el sábado"*, *"10-03-26"*.

—Cuando un dato solo puede tomar **unos pocos valores fijos**, no se escribe como texto libre: se usa un **enum** —dice {mentor}—. Y las fechas, {heroe}, tienen su propio tipo: con él, sumar diez días o saber cuántas noches hay entre dos fechas deja de ser un dolor de cabeza.

### Objetivos

- Declarar enums puros y respaldados (con valor `string` o `int`).
- Agregarles métodos y usarlos con `match`.
- Convertir desde texto con `from` y `tryFrom`, y listar los casos con `cases()`.
- Trabajar fechas con `DateTimeImmutable`: crear, formatear, sumar y comparar.
- Calcular diferencias con `diff` y validar fechas escritas por una persona.

### Antes de empezar

- Clases, métodos estáticos (R02-N03) e interfaces (R02-N06).

### Explicación

#### Enums puros
Un **enum** es un tipo con una lista cerrada de valores posibles:
```php
enum Clima
{
    case Soleado;
    case Nublado;
    case Tormenta;
}
$hoy = Clima::Tormenta;
var_dump($hoy === Clima::Tormenta);   // true
```
Una función que pide `Clima $c` **solo** acepta esos tres casos: se acabaron los
`"tormenta"`, `"Tormenta"` y `"tormeta"`.

#### Enums respaldados
Si hay que guardarlos (en la base de datos, en un JSON), cada caso lleva un valor:
```php
enum Estado: string
{
    case Pendiente = 'pendiente';
    case Pagado = 'pagado';
    case Cancelado = 'cancelado';
}
echo Estado::Pagado->value;    // pagado
echo Estado::Pagado->name;     // Pagado
```

#### Desde un texto
```php
Estado::from('pagado');     // Estado::Pagado
Estado::from('pagada');     // ValueError: "pagada" is not a valid backing value…
Estado::tryFrom('pagada');  // null (sin error)
Estado::cases();            // [Estado::Pendiente, Estado::Pagado, Estado::Cancelado]
```
`tryFrom` es ideal para validar lo que llega de un formulario: si da `null`, el
dato es inválido.

#### Métodos y constantes en un enum
```php
enum Estado: string
{
    case Pendiente = 'pendiente';
    case Pagado = 'pagado';
    case Cancelado = 'cancelado';

    public function etiqueta(): string
    {
        return match ($this) {
            self::Pendiente => 'Pendiente de pago',
            self::Pagado => 'Pagado',
            self::Cancelado => 'Cancelado',
        };
    }

    public function puedeCancelarse(): bool
    {
        return $this === self::Pendiente;
    }
}
```
Un `match ($this)` que cubre todos los casos no necesita `default`: si mañana
agregás un caso y te olvidás de él, el `UnhandledMatchError` te avisa. Los enums
pueden implementar interfaces y tener métodos estáticos.

#### Fechas con `DateTimeImmutable`
```php
date_default_timezone_set('America/Argentina/Buenos_Aires');

$llegada = new DateTimeImmutable('2026-10-03 09:40');
echo $llegada->format('d/m/Y H:i');            // 03/10/2026 09:40
$salida = $llegada->modify('+10 days');        // otro objeto: el original no cambia
$vence = $llegada->add(new DateInterval('P1M2D'));   // + 1 mes y 2 días
$hoy = new DateTimeImmutable();                // ahora
```
- **Siempre `DateTimeImmutable`** (no `DateTime`): cada operación devuelve una
  fecha nueva y no modifica la original (¡los trolls otra vez!).
- Configurá la zona horaria al principio, o las horas salen corridas.

Letras de `format` más usadas:
| Letra | Da | Ejemplo |
|---|---|---|
| `d` / `m` / `Y` | día, mes, año | `03`, `10`, `2026` |
| `H:i:s` | hora, minutos, segundos | `09:40:00` |
| `N` | día de la semana (1 lunes … 7 domingo) | `6` |
| `t` | cantidad de días del mes | `31` |

Los nombres de días y meses que da `format` están en inglés (`l` → `Saturday`).
Para castellano, lo más simple es un array: `['lunes', 'martes', …][$fecha->format('N') - 1]`.

#### Comparar y medir
```php
$a < $b;                          // las fechas se comparan con < > ==
$diferencia = $a->diff($b);       // un DateInterval
echo $diferencia->days;           // días totales entre las dos
```
`$diferencia->days` es el total de días; `->m` y `->d` son los meses y días
"sueltos" (2 meses y 21 días).

#### Validar una fecha escrita por una persona
`createFromFormat` lee un texto con un formato:
```php
$fecha = DateTimeImmutable::createFromFormat('!d/m/Y', '31/02/2026');
echo $fecha->format('Y-m-d');     // 2026-03-03 (!): "corrió" los días que sobran
```
PHP no rechaza el 31 de febrero: lo convierte en 3 de marzo. Para validar, se
vuelve a formatear y se compara con el texto original:
```php
function fechaValida(string $texto): ?DateTimeImmutable
{
    $f = DateTimeImmutable::createFromFormat('!d/m/Y', $texto);
    return $f !== false && $f->format('d/m/Y') === $texto ? $f : null;
}
```
El `!` pone la hora en 00:00 (si no, toma la hora actual).

### Código de ejemplo

```php
<?php
declare(strict_types=1);
/*
 * El despacho de pasajes: enums para los estados y fechas inmutables.
 */
date_default_timezone_set('America/Argentina/Buenos_Aires');

enum Estado: string
{
    case Pendiente = 'pendiente';
    case Pagado = 'pagado';
    case Cancelado = 'cancelado';

    public function etiqueta(): string
    {
        return match ($this) {
            self::Pendiente => 'Pendiente de pago',
            self::Pagado => 'Pagado',
            self::Cancelado => 'Cancelado',
        };
    }

    public function puedeCancelarse(): bool
    {
        return $this === self::Pendiente;
    }
}

const DIAS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'];

function fechaLarga(DateTimeImmutable $f): string
{
    return DIAS[(int) $f->format('N') - 1] . ' ' . $f->format('d/m/Y');
}

function fechaValida(string $texto): ?DateTimeImmutable
{
    $f = DateTimeImmutable::createFromFormat('!d/m/Y', $texto);
    return $f !== false && $f->format('d/m/Y') === $texto ? $f : null;
}

// Enums
$reservas = [['Kira', 'pagado'], ['Bron', 'pendiente'], ['Lía', 'pagada'], ['Olmo', 'cancelado']];
foreach ($reservas as [$nombre, $texto]) {
    $estado = Estado::tryFrom($texto);
    if ($estado === null) {
        echo "$nombre: estado desconocido «{$texto}»\n";
        continue;
    }
    echo "$nombre: ", $estado->etiqueta(), $estado->puedeCancelarse() ? ' (se puede cancelar)' : '', "\n";
}
echo "Estados posibles: ", implode(', ', array_map(fn(Estado $e) => $e->value, Estado::cases())), "\n";

// Fechas
$llegada = new DateTimeImmutable('2026-10-03 09:40');
$salida = $llegada->modify('+10 days');
echo "Llega: ", fechaLarga($llegada), " a las ", $llegada->format('H:i'), "\n";
echo "Sale: ", fechaLarga($salida), " (", $llegada->diff($salida)->days, " noches)\n";
echo "Vence el pago: ", $llegada->add(new DateInterval('P1M2D'))->format('d/m/Y'), "\n";
echo "Último día del mes: ", $llegada->modify('last day of this month')->format('d/m/Y'), "\n";
$navidad = new DateTimeImmutable('2026-12-25');
$falta = $llegada->diff($navidad);
echo "Hasta Navidad: {$falta->days} días ({$falta->m} meses y {$falta->d} días)\n";

// Validar fechas escritas a mano
foreach (['31/12/2026', '31/02/2026', '3/10/2026'] as $texto) {
    echo "$texto: ", fechaValida($texto) ? 'válida' : 'inválida', "\n";
}
```

### Salida esperada

```
Kira: Pagado
Bron: Pendiente de pago (se puede cancelar)
Lía: estado desconocido «pagada»
Olmo: Cancelado
Estados posibles: pendiente, pagado, cancelado
Llega: sábado 03/10/2026 a las 09:40
Sale: martes 13/10/2026 (10 noches)
Vence el pago: 05/11/2026
Último día del mes: 31/10/2026
Hasta Navidad: 82 días (2 meses y 21 días)
31/12/2026: válida
31/02/2026: inválida
3/10/2026: inválida
```

### ¿Para qué sirve?

Los estados de un pedido, los roles de un usuario, los métodos de pago o los talles de una remera son enums: con ellos el sistema no puede tener un estado mal escrito. Y las fechas están en todas partes: vencimientos, turnos, reservas, cuotas, antigüedad de un empleado. Laravel guarda los enums respaldados directo en la base de datos y usa Carbon, que es un `DateTimeImmutable` con más métodos.

### Errores habituales

**Goblin: `from` con un valor inválido.** `ValueError: "pagada" is not a valid backing
value for enum Estado`. Con datos de afuera, usá `tryFrom` y revisá el `null`.

**Esqueleto: el caso mal escrito.** `Estado::Pagada` da `Undefined constant
Estado::Pagada`: los casos son los que declaraste.

**Troll: `DateTime` que cambia solo.** Con `DateTime` (no inmutable),
`$vence = $hoy->modify('+30 days')` modifica también `$hoy`. Usá
`DateTimeImmutable`.

**Ogro: el 31 de febrero.** `createFromFormat` lo acepta y lo corre a marzo. Validá
comparando con el texto original.

**Ogro: la zona horaria.** Sin `date_default_timezone_set`, las horas pueden salir
corridas 3 horas (UTC). Configurala una vez al principio.

### Misión R02-N08-M1 · Los talles de la tienda náutica

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La tienda náutica vende camperas en talles. Escribí el enum respaldado `Talle`
(`S`, `M`, `L`, `XL`, con valores `'s'`, `'m'`, `'l'`, `'xl'`) con los métodos:

- `pecho(): int` — centímetros de pecho: 92, 100, 108, 116;
- `recargo(): float` — 0 para S y M, 0.10 para L, 0.20 para XL;
- `static paraPecho(int $cm): ?self` — el talle más chico cuyo pecho sea mayor o
  igual a la medida (o `null` si no hay).

Leé pedidos de la entrada (`NOMBRE;TALLE` o `NOMBRE;medida en cm`), convertí con
`tryFrom` (aceptando mayúsculas) o con `paraPecho`, y mostrá el precio de cada
campera (base $58000 más el recargo). Los talles inválidos se informan.

#### Criterio de aprobación

- `Talle` es un enum respaldado con métodos.
- Usa `tryFrom` para el texto y un método estático para la medida.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
Kira;m
Bron;XL
Lía;105
Olmo;xxl
Tomi;130
```

#### Salida esperada

```
Kira: talle M (100 cm) $58.000
Bron: talle XL (116 cm) $69.600
Lía: talle L (108 cm) $63.800
Olmo: no hay talle para «xxl»
Tomi: no hay talle para «130»
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - Los talles de la tienda náutica: enum respaldado con métodos.
const PRECIO_BASE = 58000;

enum Talle: string
{
    case S = 's';
    case M = 'm';
    case L = 'l';
    case XL = 'xl';

    public function pecho(): int
    {
        return match ($this) {
            self::S => 92,
            self::M => 100,
            self::L => 108,
            self::XL => 116,
        };
    }

    public function recargo(): float
    {
        return match ($this) {
            self::S, self::M => 0,
            self::L => 0.10,
            self::XL => 0.20,
        };
    }

    public static function paraPecho(int $cm): ?self
    {
        foreach (self::cases() as $talle) {
            if ($talle->pecho() >= $cm) {
                return $talle;
            }
        }
        return null;
    }
}

while (($linea = fgets(STDIN)) !== false) {
    if (trim($linea) === '') {
        continue;
    }
    [$nombre, $dato] = explode(';', trim($linea));
    $talle = ctype_digit($dato) ? Talle::paraPecho((int) $dato) : Talle::tryFrom(strtolower($dato));
    if ($talle === null) {
        echo "$nombre: no hay talle para «{$dato}»\n";
        continue;
    }
    $precio = PRECIO_BASE * (1 + $talle->recargo());
    echo "$nombre: talle {$talle->name} ({$talle->pecho()} cm) $", number_format($precio, 0, ',', '.'), "\n";
}
```

#### Pruebas

##### Medidas en el borde
```entrada
Ana;92
Beto;116
Caro;117
Dani;1
```
```salida
Ana: talle S (92 cm) $58.000
Beto: talle XL (116 cm) $69.600
Caro: no hay talle para «117»
Dani: talle S (92 cm) $58.000
```

##### Talles en mayúscula y minúscula
```entrada
Eva;S
Fede;xl
Gabi;XXS
```
```salida
Eva: talle S (92 cm) $58.000
Fede: talle XL (116 cm) $69.600
Gabi: no hay talle para «XXS»
```

### Misión R02-N08-M2 · El vencimiento de las cuotas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Una casa de electrodomésticos vende en cuotas que vencen **el día 10 de cada
mes**, empezando el mes siguiente a la compra. Si el día 10 cae sábado o domingo,
el vencimiento pasa al lunes siguiente. Leé la fecha de compra (`DD/MM/AAAA`,
validándola) y la cantidad de cuotas, y mostrá la fecha de cada vencimiento con el
nombre del día en castellano. Al final, mostrá cuántos días hay entre la compra y
el último vencimiento.

#### Criterio de aprobación

- Valida la fecha comparando con el texto original.
- Usa `DateTimeImmutable` y `modify`/`add`.
- Corre los vencimientos del fin de semana al lunes.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
28/09/2026
6
```

#### Salida esperada

```
Fecha de compra: Cuotas: 
Cuota 1: lunes 12/10/2026
Cuota 2: martes 10/11/2026
Cuota 3: jueves 10/12/2026
Cuota 4: lunes 11/01/2027
Cuota 5: miércoles 10/02/2027
Cuota 6: miércoles 10/03/2027
Días entre la compra y el último vencimiento: 163
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 2 - El vencimiento de las cuotas: fechas inmutables y fines de semana.
date_default_timezone_set('America/Argentina/Buenos_Aires');
const DIAS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'];

function fechaValida(string $texto): ?DateTimeImmutable
{
    $f = DateTimeImmutable::createFromFormat('!d/m/Y', $texto);
    return $f !== false && $f->format('d/m/Y') === $texto ? $f : null;
}

function habil(DateTimeImmutable $f): DateTimeImmutable
{
    return (int) $f->format('N') >= 6 ? $f->modify('next monday') : $f;
}

echo "Fecha de compra: ";
$compra = fechaValida(trim(fgets(STDIN)));
echo "Cuotas: ";
$cuotas = (int) trim(fgets(STDIN));
echo "\n";
if ($compra === null) {
    echo "Fecha inválida.\n";
    exit(1);
}

// El día 10 del mes siguiente: el primero del mes que viene, más 9 días.
$primerDia = $compra->modify('first day of next month')->modify('+9 days');
$ultimo = $compra;
for ($n = 1; $n <= $cuotas; $n++) {
    $vence = habil($primerDia->add(new DateInterval('P' . ($n - 1) . 'M')));
    echo "Cuota $n: ", DIAS[(int) $vence->format('N') - 1], ' ', $vence->format('d/m/Y'), "\n";
    $ultimo = $vence;
}
echo "Días entre la compra y el último vencimiento: ", $compra->diff($ultimo)->days, "\n";
```

#### Pruebas

##### Una cuota en enero
```entrada
15/12/2026
1
```
```salida
Fecha de compra: Cuotas:
Cuota 1: lunes 11/01/2027
Días entre la compra y el último vencimiento: 27
```

##### Fecha inválida
```entrada
31/02/2026
3
```
```salida
Fecha de compra: Cuotas:
Fecha inválida.
```

##### Compra el día 10
```entrada
10/01/2027
3
```
```salida
Fecha de compra: Cuotas:
Cuota 1: miércoles 10/02/2027
Cuota 2: miércoles 10/03/2027
Cuota 3: lunes 12/04/2027
Días entre la compra y el último vencimiento: 92
```

### Misión R02-N08-M3 · El semáforo de los pedidos

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Los pedidos de un comercio pasan por estados en un orden fijo: `Nuevo` →
`Preparando` → `Enviado` → `Entregado`, y desde `Nuevo` o `Preparando` se puede ir a
`Cancelado`. Escribí el enum respaldado `EstadoPedido` con:

- `puedePasarA(self $nuevo): bool` — con un `match ($this)` que devuelva si la
  transición es válida (`in_array($nuevo, [...], true)`);
- `color(): string` — `gris`, `amarillo`, `azul`, `verde` y `rojo`;
- `esFinal(): bool` — entregado o cancelado.

Escribí la clase `Pedido` con el estado privado (arranca en `Nuevo`) y
`cambiarA(EstadoPedido $nuevo): void`, que lanza `LogicException` si la transición
no es válida. Ejecutá la historia del ejemplo, mostrando cada cambio o el error.

#### Criterio de aprobación

- Las reglas de transición están en el enum.
- `Pedido` no deja pasar transiciones inválidas.
- La salida coincide con la esperada.

#### Salida esperada

```
Pedido 1042: preparando (amarillo)
Pedido 1042: No se puede pasar de preparando a entregado
Pedido 1042: enviado (azul)
Pedido 1042: No se puede pasar de enviado a cancelado
Pedido 1042: entregado (verde) - terminado
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - El semáforo de los pedidos: un enum que conoce sus transiciones.

enum EstadoPedido: string
{
    case Nuevo = 'nuevo';
    case Preparando = 'preparando';
    case Enviado = 'enviado';
    case Entregado = 'entregado';
    case Cancelado = 'cancelado';

    public function puedePasarA(self $nuevo): bool
    {
        $permitidos = match ($this) {
            self::Nuevo => [self::Preparando, self::Cancelado],
            self::Preparando => [self::Enviado, self::Cancelado],
            self::Enviado => [self::Entregado],
            self::Entregado, self::Cancelado => [],
        };
        return in_array($nuevo, $permitidos, true);
    }

    public function color(): string
    {
        return match ($this) {
            self::Nuevo => 'gris',
            self::Preparando => 'amarillo',
            self::Enviado => 'azul',
            self::Entregado => 'verde',
            self::Cancelado => 'rojo',
        };
    }

    public function esFinal(): bool
    {
        return $this === self::Entregado || $this === self::Cancelado;
    }
}

class Pedido
{
    private EstadoPedido $estado = EstadoPedido::Nuevo;

    public function __construct(public readonly int $numero) {}

    public function estado(): EstadoPedido
    {
        return $this->estado;
    }

    public function cambiarA(EstadoPedido $nuevo): void
    {
        if (!$this->estado->puedePasarA($nuevo)) {
            throw new LogicException("No se puede pasar de {$this->estado->value} a {$nuevo->value}");
        }
        $this->estado = $nuevo;
    }
}

$pedido = new Pedido(1042);
foreach ([EstadoPedido::Preparando, EstadoPedido::Entregado, EstadoPedido::Enviado, EstadoPedido::Cancelado, EstadoPedido::Entregado] as $nuevo) {
    try {
        $pedido->cambiarA($nuevo);
        $e = $pedido->estado();
        echo "Pedido {$pedido->numero}: {$e->value} ({$e->color()})", $e->esFinal() ? ' - terminado' : '', "\n";
    } catch (LogicException $ex) {
        echo "Pedido {$pedido->numero}: ", $ex->getMessage(), "\n";
    }
}
```

### Encargo R02-N08-E1 · La liquidación de vacaciones

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

En Argentina, los días de vacaciones dependen de la **antigüedad** al 31 de
diciembre del año: hasta 5 años, 14 días; más de 5 y hasta 10, 21 días; más de 10
y hasta 20, 28 días; más de 20, 35 días. Escribí el enum `Tramo` (con los cuatro
tramos y un método `dias(): int`) y un método estático
`Tramo::paraAntiguedad(int $anios): self`.

Leé de la entrada renglones `NOMBRE;FECHA_DE_INGRESO` (DD/MM/AAAA) y el año a
liquidar en el primer renglón. Para cada empleado, calculá la antigüedad en años
completos al 31/12 de ese año (con `diff(...)->y`), el tramo y los días. Las
fechas inválidas se informan. Mostrá una tabla y el total de días a otorgar.

#### Criterio de aprobación

- El tramo es un enum con `dias()` y una fábrica estática.
- La antigüedad se calcula con `DateTimeImmutable::diff`.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
2026
Ana;15/03/2023
Bruno;01/10/2019
Carla;20/07/2014
Diego;30/02/2010
Elena;02/01/2001
```

#### Salida esperada

```
Vacaciones 2026
  Ana    ingresó 15/03/2023 ·  3 años · 14 días
  Bruno  ingresó 01/10/2019 ·  7 años · 21 días
  Carla  ingresó 20/07/2014 · 12 años · 28 días
  Diego: fecha de ingreso inválida (30/02/2010)
  Elena  ingresó 02/01/2001 · 25 años · 35 días
Total de días a otorgar: 98
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - La liquidación de vacaciones: un enum de tramos y antigüedad con diff.
date_default_timezone_set('America/Argentina/Buenos_Aires');

enum Tramo
{
    case HastaCinco;
    case HastaDiez;
    case HastaVeinte;
    case MasDeVeinte;

    public function dias(): int
    {
        return match ($this) {
            self::HastaCinco => 14,
            self::HastaDiez => 21,
            self::HastaVeinte => 28,
            self::MasDeVeinte => 35,
        };
    }

    public static function paraAntiguedad(int $anios): self
    {
        return match (true) {
            $anios <= 5 => self::HastaCinco,
            $anios <= 10 => self::HastaDiez,
            $anios <= 20 => self::HastaVeinte,
            default => self::MasDeVeinte,
        };
    }
}

function fechaValida(string $texto): ?DateTimeImmutable
{
    $f = DateTimeImmutable::createFromFormat('!d/m/Y', $texto);
    return $f !== false && $f->format('d/m/Y') === $texto ? $f : null;
}

$anio = (int) trim(fgets(STDIN));
$corte = new DateTimeImmutable("$anio-12-31");
$total = 0;
echo "Vacaciones $anio\n";
while (($linea = fgets(STDIN)) !== false) {
    if (trim($linea) === '') {
        continue;
    }
    [$nombre, $texto] = explode(';', trim($linea));
    $ingreso = fechaValida($texto);
    if ($ingreso === null) {
        echo "  $nombre: fecha de ingreso inválida ($texto)\n";
        continue;
    }
    $antiguedad = $ingreso->diff($corte)->y;
    $dias = Tramo::paraAntiguedad($antiguedad)->dias();
    $total += $dias;
    printf("  %-6s ingresó %s · %2d años · %2d días\n", $nombre, $ingreso->format('d/m/Y'), $antiguedad, $dias);
}
echo "Total de días a otorgar: $total\n";
```

#### Pruebas

##### Bordes de tramos
```entrada
2026
Uno;31/12/2021
Dos;01/01/2021
Tres;31/12/2016
Cuatro;31/12/2006
```
```salida
Vacaciones 2026
  Uno    ingresó 31/12/2021 ·  5 años · 14 días
  Dos    ingresó 01/01/2021 ·  5 años · 14 días
  Tres   ingresó 31/12/2016 · 10 años · 21 días
  Cuatro ingresó 31/12/2006 · 20 años · 28 días
Total de días a otorgar: 77
```

##### Sin empleados
```entrada
2026
```
```salida
Vacaciones 2026
Total de días a otorgar: 0
```

### Prueba del sello

#### ¿Qué ventaja tiene un enum sobre un texto como `"pagado"`?

Solo admite los valores declarados: no puede haber un estado mal escrito, y las funciones pueden pedir ese tipo.

#### ¿Qué diferencia hay entre `from` y `tryFrom`?

Con un valor que no existe, `from` lanza un `ValueError` y `tryFrom` devuelve `null`.

#### ¿Por qué se usa `DateTimeImmutable` y no `DateTime`?

Porque sus operaciones devuelven una fecha nueva sin modificar la original; con `DateTime`, `modify` cambia el objeto y puede afectar a otras partes del programa.

#### ¿Qué pasa con `createFromFormat('!d/m/Y', '31/02/2026')`?

No da error: devuelve el 3 de marzo. Para validar hay que volver a formatear la fecha y compararla con el texto original.

#### ¿Qué da `$a->diff($b)->days`?

La cantidad total de días entre las dos fechas.

### Soluciones (docente)

Sale de `21-PHP/19-Fechas-Enums`, ampliado con validación de fechas escritas a mano, transiciones de estado (misión 3) y el caso real de las vacaciones (Ley de Contrato de Trabajo, art. 150, simplificado: no se consideran los seis meses mínimos de trabajo en el año). En la misión 2, sumar meses al día 10 con `DateInterval('PnM')` nunca desborda (el 10 existe en todos los meses); si fuera el día 31, habría que tener cuidado.

## R02-N09 · Excepciones

```meta
tipo: tema
padre: R02-N08
precio: 10
criatura: troll
temas: err.excepciones
```

### Crónica

Una noche de tormenta, la grúa del muelle 2 se trabó con un contenedor colgando. El operario no sabía qué hacer y lo dejó ahí; a la mañana, el contenedor cayó sobre un bote. Desde entonces hay un protocolo pegado en cada grúa: *si algo falla, avisá a quien sabe resolverlo, y antes de irte, asegurá la carga*.

—Los programas también fallan: un archivo que no está, un dato imposible, una base de datos que no responde —dice {mentor}—. Lo peor es fallar en silencio. Una **excepción** es un aviso que sube hasta alguien que sabe qué hacer. Y siempre, {heroe}, siempre se asegura la carga.

### Objetivos

- Lanzar excepciones con `throw` cuando algo no puede seguir.
- Atraparlas con `try`/`catch` y usar `finally` para limpiar.
- Conocer la jerarquía: `Throwable`, `Exception`, `Error` y las excepciones de PHP.
- Crear excepciones propias con datos extra.
- Atrapar varios tipos, encadenar excepciones y decidir dónde atrapar.

### Antes de empezar

- Clases y herencia (R02-N04). Ya usaste `throw new InvalidArgumentException` en los nodos anteriores.

### Explicación

#### Lanzar
Cuando un método recibe algo con lo que no puede trabajar, **no** devuelve un valor
raro (`-1`, `false`, `null`): lanza una excepción.
```php
function dividir(float $a, float $b): float
{
    if ($b == 0) {
        throw new InvalidArgumentException('No se puede dividir por cero');
    }
    return $a / $b;
}
```
`throw` corta la función en ese punto y la excepción "sube" por las llamadas hasta
que alguien la atrape. Si nadie la atrapa, el programa termina con
`PHP Fatal error:  Uncaught InvalidArgumentException: No se puede dividir por cero`.

#### Atrapar: `try`, `catch` y `finally`
```php
try {
    $resultado = dividir(10, 0);
    echo "Resultado: $resultado\n";      // no se ejecuta
} catch (InvalidArgumentException $e) {
    echo "Error: ", $e->getMessage(), "\n";
} finally {
    echo "Cálculo terminado\n";          // se ejecuta siempre, haya error o no
}
```
- El `try` encierra el código que puede fallar.
- El `catch` indica **qué tipo** de excepción atrapa y recibe el objeto.
- El `finally` se ejecuta siempre: ahí se cierra un archivo, se libera un recurso,
  se "asegura la carga".

Métodos útiles del objeto: `getMessage()`, `getCode()`, `getLine()`, `getFile()`,
`getPrevious()`.

#### La jerarquía
```
Throwable (interfaz)
├── Error                  ← errores del propio PHP (TypeError, DivisionByZeroError,
│                            ValueError, UnhandledMatchError…)
└── Exception              ← los de tu programa
    ├── InvalidArgumentException   (un argumento inválido)
    ├── DomainException            (una regla del negocio que no se cumple)
    ├── LogicException             (un error del programador)
    └── RuntimeException           (algo que falló al ejecutar: un archivo, la red)
        └── …
```
Un `catch (Exception $e)` atrapa cualquier excepción de tu programa, pero **no**
un `TypeError` (que es un `Error`). `catch (Throwable $t)` atrapa todo: se usa solo
en el nivel más alto, para mostrar un mensaje amable y registrar el problema.

#### Excepciones propias
Una clase que hereda de una excepción de PHP le da nombre al problema y puede
llevar datos:
```php
class StockInsuficiente extends DomainException
{
    public function __construct(public readonly string $producto, public readonly int $pedido, public readonly int $hay)
    {
        parent::__construct("No hay $pedido de $producto (quedan $hay)");
    }
}
```
Así quien la atrapa sabe exactamente qué pasó (`catch (StockInsuficiente $e)`) y
tiene los datos para reaccionar (`$e->hay`).

#### Varios tipos
```php
try { … }
catch (StockInsuficiente $e) { … }                        // el más específico primero
catch (InvalidArgumentException | DomainException $e) { … }   // dos tipos en uno
```
PHP prueba los `catch` en orden y entra en el **primero** que coincide.

#### Encadenar
Cuando atrapás una excepción técnica y lanzás una del problema, pasá la original
como tercer argumento para no perder el detalle:
```php
catch (RuntimeException $e) {
    throw new PedidoFallido('No se pudo guardar el pedido', 0, $e);   // $e es la "previa"
}
```

#### ¿Dónde atrapar?
- **Lanzá** donde detectás el problema (en lo profundo: un método, una clase).
- **Atrapá** donde podés **hacer algo**: mostrar un mensaje, reintentar, usar otro
  valor. Casi siempre es arriba, en el programa principal o en el controlador.
- Nunca un `catch` vacío: esconder el error es peor que dejarlo caer. Ese es el
  **troll** de este nodo.

### Código de ejemplo

```php
<?php
declare(strict_types=1);
/*
 * El protocolo de la grúa: lanzar, atrapar, finally y excepciones propias.
 */
class StockInsuficiente extends DomainException
{
    public function __construct(public readonly string $producto, public readonly int $pedido, public readonly int $hay)
    {
        parent::__construct("No hay $pedido de $producto (quedan $hay)");
    }
}

class Deposito
{
    private array $stock = ['harina' => 40, 'sal' => 12];
    private bool $grúaOcupada = false;

    public function despachar(string $producto, int $cantidad): void
    {
        if ($cantidad <= 0) {
            throw new InvalidArgumentException("Cantidad inválida: $cantidad");
        }
        if (!isset($this->stock[$producto])) {
            throw new DomainException("No trabajamos $producto");
        }
        if ($cantidad > $this->stock[$producto]) {
            throw new StockInsuficiente($producto, $cantidad, $this->stock[$producto]);
        }
        $this->grúaOcupada = true;
        try {
            $this->stock[$producto] -= $cantidad;
            echo "  Despachados $cantidad de $producto\n";
        } finally {
            $this->grúaOcupada = false;     // se asegura la carga, pase lo que pase
        }
    }

    public function grúaLibre(): bool
    {
        return !$this->grúaOcupada;
    }
}

$deposito = new Deposito();
$pedidos = [['harina', 10], ['sal', 30], ['aceite', 2], ['harina', -1], ['sal', 12]];

foreach ($pedidos as [$producto, $cantidad]) {
    echo "Pedido: $cantidad de $producto\n";
    try {
        $deposito->despachar($producto, $cantidad);
    } catch (StockInsuficiente $e) {
        echo "  Falta stock: ", $e->getMessage(), ". ¿Mandamos las {$e->hay} que hay?\n";
    } catch (InvalidArgumentException | DomainException $e) {
        echo "  Rechazado (", get_class($e), "): ", $e->getMessage(), "\n";
    }
}
echo "La grúa quedó ", $deposito->grúaLibre() ? 'libre' : 'trabada', "\n";

// Errores de PHP: también son Throwable
try {
    echo intdiv(10, 0);
} catch (DivisionByZeroError $e) {
    echo "Error de PHP: ", $e->getMessage(), "\n";
}

// Encadenar: la excepción del problema guarda la técnica
try {
    try {
        throw new RuntimeException('El disco no responde');
    } catch (RuntimeException $tecnica) {
        throw new DomainException('No se pudo registrar el despacho', 0, $tecnica);
    }
} catch (DomainException $e) {
    echo $e->getMessage(), " (causa: ", $e->getPrevious()->getMessage(), ")\n";
}
```

### Salida esperada

```
Pedido: 10 de harina
  Despachados 10 de harina
Pedido: 30 de sal
  Falta stock: No hay 30 de sal (quedan 12). ¿Mandamos las 12 que hay?
Pedido: 2 de aceite
  Rechazado (DomainException): No trabajamos aceite
Pedido: -1 de harina
  Rechazado (InvalidArgumentException): Cantidad inválida: -1
Pedido: 12 de sal
  Despachados 12 de sal
La grúa quedó libre
Error de PHP: Division by zero
No se pudo registrar el despacho (causa: El disco no responde)
```

### ¿Para qué sirve?

En un sistema web, las excepciones son la forma normal de manejar lo que sale mal: un producto sin stock, un usuario que no existe, una base de datos caída. Laravel convierte automáticamente ciertas excepciones en páginas de error (404, 403) y registra las demás en un archivo de log. Saber lanzarlas con nombres claros y atraparlas donde se puede hacer algo es lo que hace que un sistema falle con elegancia.

### Errores habituales

**Troll: el `catch` vacío.** `catch (Exception $e) {}` hace desaparecer el error: el
programa sigue con datos rotos y nadie se entera. Como mínimo, mostralo o
registralo.

**Goblin: atrapar `Exception` y esperar un `TypeError`.** Los errores de PHP
(`TypeError`, `DivisionByZeroError`) son `Error`, no `Exception`. Para los dos,
`Throwable`.

**Ogro: el `catch` general primero.** Si `catch (Exception $e)` está antes que
`catch (StockInsuficiente $e)`, el segundo nunca se ejecuta.

**Troll: devolver `false` en lugar de lanzar.** Quien llama se olvida de revisar el
`false` y sigue como si nada. Si no se puede seguir, lanzá.

**Esqueleto: la excepción que no existe.** `throw new StockInsuficient(...)` (mal
escrito) da `Class "StockInsuficient" not found`, y el error original se pierde.

### Misión R02-N09-M1 · La calculadora del cambista

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé operaciones de la entrada, una por renglón, con el formato `NUMERO OPERADOR
NUMERO` (`12 / 4`). Escribí `function calcular(string $linea): float` que:

- lanza `InvalidArgumentException` si el renglón no tiene 3 partes o los números
  no son numéricos (`is_numeric`);
- lanza `DomainException` si el operador no es `+`, `-`, `*` o `/`;
- lanza `DivisionByZeroError('División por cero')` si se divide por cero
  (comprobá el cero antes de dividir).

El programa principal atrapa cada tipo por separado y muestra un mensaje distinto,
y en un `finally` cuenta las operaciones procesadas. Al final muestra cuántas
salieron bien y cuántas mal.

#### Criterio de aprobación

- `calcular` lanza excepciones y no muestra nada.
- Hay un `catch` para cada tipo y un `finally`.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
12 / 4
7 * 1.5
10 / 0
3 ^ 2
hola + 1
5 - 8
```

#### Salida esperada

```
12 / 4 = 3
7 * 1.5 = 10.5
10 / 0 → División por cero
3 ^ 2 → no se puede: Operador desconocido: ^
hola + 1 → dato inválido: No son números: hola y 1
5 - 8 = -3
Procesadas: 6 · bien: 3 · mal: 3
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - La calculadora del cambista: lanzar y atrapar por tipo.

function calcular(string $linea): float
{
    $partes = explode(' ', trim($linea));
    if (count($partes) !== 3) {
        throw new InvalidArgumentException('Formato: NUMERO OPERADOR NUMERO');
    }
    [$a, $op, $b] = $partes;
    if (!is_numeric($a) || !is_numeric($b)) {
        throw new InvalidArgumentException("No son números: $a y $b");
    }
    $a = (float) $a;
    $b = (float) $b;
    if ($op === '/' && $b == 0) {
        throw new DivisionByZeroError('División por cero');
    }
    return match ($op) {
        '+' => $a + $b,
        '-' => $a - $b,
        '*' => $a * $b,
        '/' => $a / $b,
        default => throw new DomainException("Operador desconocido: $op"),
    };
}

$procesadas = 0;
$bien = 0;
while (($linea = fgets(STDIN)) !== false) {
    if (trim($linea) === '') {
        continue;
    }
    try {
        $resultado = calcular($linea);
        echo trim($linea), " = ", round($resultado, 4), "\n";
        $bien++;
    } catch (InvalidArgumentException $e) {
        echo trim($linea), " → dato inválido: ", $e->getMessage(), "\n";
    } catch (DomainException $e) {
        echo trim($linea), " → no se puede: ", $e->getMessage(), "\n";
    } catch (DivisionByZeroError $e) {
        echo trim($linea), " → ", $e->getMessage(), "\n";
    } finally {
        $procesadas++;
    }
}
echo "Procesadas: $procesadas · bien: $bien · mal: ", $procesadas - $bien, "\n";
```

#### Pruebas

##### Todo bien
```entrada
1 + 1
2 * -3
9 / 3
```
```salida
1 + 1 = 2
2 * -3 = -6
9 / 3 = 3
Procesadas: 3 · bien: 3 · mal: 0
```

##### Todo mal
```entrada
1 / 0
1 % 2
uno + dos
2 +
```
```salida
1 / 0 → División por cero
1 % 2 → no se puede: Operador desconocido: %
uno + dos → dato inválido: No son números: uno y dos
2 + → dato inválido: Formato: NUMERO OPERADOR NUMERO
Procesadas: 4 · bien: 0 · mal: 4
```

### Misión R02-N09-M2 · Las excepciones del banco

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El banco del puerto necesita excepciones con nombre. Escribí:

- `class SaldoInsuficiente extends DomainException` — con `readonly` el saldo
  disponible y el monto pedido; mensaje `Saldo insuficiente: pediste 5000 y tenés 3200`;
- `class CuentaBloqueada extends DomainException` — con el titular;
- `class Cuenta` con titular, saldo, bloqueada (`bool`) y
  `extraer(float $monto): void` que lanza `InvalidArgumentException` (monto no
  positivo), `CuentaBloqueada` o `SaldoInsuficiente`, y `bloquear(): void`.

Ejecutá los movimientos del ejemplo. Cuando salta `SaldoInsuficiente`, el programa
**ofrece** extraer lo que hay (usando las propiedades de la excepción) y lo extrae.

#### Criterio de aprobación

- Dos excepciones propias que heredan de `DomainException`, con datos `readonly`.
- El programa usa los datos de la excepción para reaccionar.
- La salida coincide con la esperada.

#### Salida esperada

```
Extrajo 3000. Saldo: 5200
Movimiento rechazado: Monto inválido: -50
Saldo insuficiente: pediste 6000 y tenés 5200. Te damos los 5200 que hay.
Saldo: 0
Cuenta bloqueada por el banco
La cuenta de Kira está bloqueada: llamá al banco.
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 2 - Las excepciones del banco: excepciones propias con datos.

class SaldoInsuficiente extends DomainException
{
    public function __construct(public readonly float $disponible, public readonly float $pedido)
    {
        parent::__construct("Saldo insuficiente: pediste $pedido y tenés $disponible");
    }
}

class CuentaBloqueada extends DomainException
{
    public function __construct(public readonly string $titular)
    {
        parent::__construct("La cuenta de $titular está bloqueada");
    }
}

class Cuenta
{
    private bool $bloqueada = false;

    public function __construct(public readonly string $titular, private float $saldo) {}

    public function extraer(float $monto): void
    {
        if ($monto <= 0) {
            throw new InvalidArgumentException("Monto inválido: $monto");
        }
        if ($this->bloqueada) {
            throw new CuentaBloqueada($this->titular);
        }
        if ($monto > $this->saldo) {
            throw new SaldoInsuficiente($this->saldo, $monto);
        }
        $this->saldo -= $monto;
    }

    public function bloquear(): void
    {
        $this->bloqueada = true;
    }

    public function saldo(): float
    {
        return $this->saldo;
    }
}

$cuenta = new Cuenta('Kira', 8200);
foreach ([3000, -50, 6000, 'bloquear', 100] as $movimiento) {
    if ($movimiento === 'bloquear') {
        $cuenta->bloquear();
        echo "Cuenta bloqueada por el banco\n";
        continue;
    }
    try {
        $cuenta->extraer($movimiento);
        echo "Extrajo $movimiento. Saldo: ", $cuenta->saldo(), "\n";
    } catch (SaldoInsuficiente $e) {
        echo $e->getMessage(), ". Te damos los {$e->disponible} que hay.\n";
        $cuenta->extraer($e->disponible);
        echo "Saldo: ", $cuenta->saldo(), "\n";
    } catch (CuentaBloqueada $e) {
        echo $e->getMessage(), ": llamá al banco.\n";
    } catch (InvalidArgumentException $e) {
        echo "Movimiento rechazado: ", $e->getMessage(), "\n";
    }
}
```

### Misión R02-N09-M3 · El archivo que no estaba

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí la clase `LectorDeTarifas` con `leer(string $ruta): array`, que lee un
archivo de texto con renglones `destino;precio` y devuelve `destino => precio`.
Tiene que:

- lanzar `RuntimeException` si el archivo no existe (comprobalo con `file_exists`
  antes de abrirlo);
- abrirlo con `fopen` y leerlo con `fgets` dentro de un `try`, y **cerrarlo en el
  `finally`** con `fclose` (aunque un renglón falle);
- lanzar `UnexpectedValueException` con el número de renglón si un precio no es
  numérico, encadenando nada (es el error original).

El programa principal crea un archivo temporal válido y otro con un renglón roto
(con `file_put_contents` en `sys_get_temp_dir()`), intenta leer los dos y uno
inexistente, y muestra el resultado o el error de cada uno. Contá con una
propiedad estática cuántos archivos se cerraron, para mostrar que el `finally`
corre siempre.

#### Criterio de aprobación

- El archivo se cierra en el `finally`.
- Cada error lanza una excepción distinta con un mensaje claro.
- La salida coincide con la esperada.

#### Salida esperada

```
tarifas-ok.txt: 3 tarifas (valle, forjas, imperio)
tarifas-rota.txt: archivo con errores. Renglón 2: el precio «cinco mil» no es un número
tarifas-perdida.txt: No existe el archivo tarifas-perdida.txt
Archivos cerrados: 2
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - El archivo que no estaba: finally para cerrar siempre.

class LectorDeTarifas
{
    public static int $cerrados = 0;

    public function leer(string $ruta): array
    {
        if (!file_exists($ruta)) {
            throw new RuntimeException('No existe el archivo ' . basename($ruta));
        }
        $archivo = fopen($ruta, 'r');
        try {
            $tarifas = [];
            $numero = 0;
            while (($linea = fgets($archivo)) !== false) {
                $numero++;
                if (trim($linea) === '') {
                    continue;
                }
                [$destino, $precio] = explode(';', trim($linea));
                if (!is_numeric($precio)) {
                    throw new UnexpectedValueException("Renglón $numero: el precio «{$precio}» no es un número");
                }
                $tarifas[$destino] = (float) $precio;
            }
            return $tarifas;
        } finally {
            fclose($archivo);
            self::$cerrados++;
        }
    }
}

$dir = sys_get_temp_dir();
file_put_contents("$dir/tarifas-ok.txt", "valle;1800\nforjas;5250.5\nimperio;12999\n");
file_put_contents("$dir/tarifas-rota.txt", "valle;1800\nforjas;cinco mil\n");

$lector = new LectorDeTarifas();
foreach (['tarifas-ok.txt', 'tarifas-rota.txt', 'tarifas-perdida.txt'] as $nombre) {
    echo "$nombre: ";
    try {
        $tarifas = $lector->leer("$dir/$nombre");
        echo count($tarifas), " tarifas (", implode(', ', array_keys($tarifas)), ")\n";
    } catch (UnexpectedValueException $e) {
        echo "archivo con errores. ", $e->getMessage(), "\n";
    } catch (RuntimeException $e) {
        echo $e->getMessage(), "\n";
    }
}
echo "Archivos cerrados: ", LectorDeTarifas::$cerrados, "\n";
unlink("$dir/tarifas-ok.txt");
unlink("$dir/tarifas-rota.txt");
```

### Encargo R02-N09-E1 · La importación de clientes

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una empresa migra su lista de clientes desde una planilla. Cada renglón de la
entrada es `NOMBRE;EMAIL;EDAD`. Escribí:

- `class ClienteInvalido extends InvalidArgumentException` con el **campo** que
  falló (`readonly`);
- `class Cliente` (`readonly`) cuyo constructor valida: nombre no vacío, email válido
  (`FILTER_VALIDATE_EMAIL`), edad entera entre 18 y 110; y lanza `ClienteInvalido`
  con el campo y un mensaje;
- `class Importador` con `importar(iterable $renglones): array` que devuelve
  `['ok' => [...clientes], 'errores' => [renglón => mensaje]]`: **no** se corta en
  el primer error, sigue con el resto.

Si un email se repite, el segundo cuenta como error del campo `email` con el
mensaje `email repetido`. Mostrá el resumen: importados, errores por renglón y
cuántos errores hubo por campo.

#### Criterio de aprobación

- La validación está en el constructor de `Cliente` y lanza una excepción propia.
- El importador atrapa cada error y sigue.
- Cuenta los errores por campo usando la propiedad de la excepción.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
Ana Pérez;ana@correo.com;34
;bruno@correo.com;40
Carla Gómez;carla@;29
Diego Ruiz;diego@correo.com;16
Elena Sosa;ana@correo.com;52
Fabián Díaz;fabian@correo.com;treinta
Gala Ríos;gala@correo.com;61
```

#### Salida esperada

```
Importados: 2
  Ana Pérez <ana@correo.com>, 34 años
  Gala Ríos <gala@correo.com>, 61 años
Errores:
  renglón 2: falta el nombre
  renglón 3: email inválido: carla@
  renglón 4: edad fuera de rango: 16
  renglón 5: email repetido
  renglón 6: edad no numérica: treinta
  edad: 2
  email: 2
  nombre: 1
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - La importación de clientes: validar con excepciones y seguir.

class ClienteInvalido extends InvalidArgumentException
{
    public function __construct(public readonly string $campo, string $mensaje)
    {
        parent::__construct($mensaje);
    }
}

readonly class Cliente
{
    public function __construct(public string $nombre, public string $email, public int $edad)
    {
        if (trim($nombre) === '') {
            throw new ClienteInvalido('nombre', 'falta el nombre');
        }
        if (filter_var($email, FILTER_VALIDATE_EMAIL) === false) {
            throw new ClienteInvalido('email', "email inválido: $email");
        }
        if ($edad < 18 || $edad > 110) {
            throw new ClienteInvalido('edad', "edad fuera de rango: $edad");
        }
    }
}

class Importador
{
    public function importar(iterable $renglones): array
    {
        $ok = [];
        $errores = [];
        $emails = [];
        foreach ($renglones as $numero => $renglon) {
            [$nombre, $email, $edad] = array_pad(explode(';', trim($renglon)), 3, '');
            try {
                $edadValida = filter_var($edad, FILTER_VALIDATE_INT);
                if ($edadValida === false) {
                    throw new ClienteInvalido('edad', "edad no numérica: $edad");
                }
                $cliente = new Cliente($nombre, $email, $edadValida);
                if (isset($emails[$cliente->email])) {
                    throw new ClienteInvalido('email', 'email repetido');
                }
                $emails[$cliente->email] = true;
                $ok[] = $cliente;
            } catch (ClienteInvalido $e) {
                $errores[$numero] = $e;
            }
        }
        return ['ok' => $ok, 'errores' => $errores];
    }
}

$renglones = [];
$numero = 0;
while (($linea = fgets(STDIN)) !== false) {
    $numero++;
    if (trim($linea) !== '') {
        $renglones[$numero] = $linea;
    }
}

$resultado = (new Importador())->importar($renglones);
echo "Importados: ", count($resultado['ok']), "\n";
foreach ($resultado['ok'] as $c) {
    echo "  {$c->nombre} <{$c->email}>, {$c->edad} años\n";
}
echo "Errores:\n";
$porCampo = [];
foreach ($resultado['errores'] as $renglon => $e) {
    echo "  renglón $renglon: ", $e->getMessage(), "\n";
    $porCampo[$e->campo] = ($porCampo[$e->campo] ?? 0) + 1;
}
ksort($porCampo);
foreach ($porCampo as $campo => $cantidad) {
    echo "  $campo: $cantidad\n";
}
```

#### Pruebas

##### Todo válido
```entrada
Ana;ana@x.com;18
Beto;beto@x.com;110
```
```salida
Importados: 2
  Ana <ana@x.com>, 18 años
  Beto <beto@x.com>, 110 años
Errores:
```

##### Bordes de edad
```entrada
Uno;uno@x.com;17
Dos;dos@x.com;111
Tres;tres@x.com;18.5
```
```salida
Importados: 0
Errores:
  renglón 1: edad fuera de rango: 17
  renglón 2: edad fuera de rango: 111
  renglón 3: edad no numérica: 18.5
  edad: 3
```

### Prueba del sello

#### ¿Qué hace `throw`?

Lanza una excepción: corta la ejecución en ese punto y la excepción sube hasta el primer `catch` que la atrape (o termina el programa).

#### ¿Cuándo se ejecuta el bloque `finally`?

Siempre, haya habido una excepción o no (y aunque el `try` tenga un `return`).

#### ¿Un `catch (Exception $e)` atrapa un `TypeError`?

No: `TypeError` es un `Error`, no una `Exception`. Los dos son `Throwable`.

#### ¿Para qué sirve crear una excepción propia?

Para darle nombre al problema (que se pueda atrapar por separado) y llevar datos extra que ayuden a reaccionar.

#### ¿Por qué un `catch` vacío es un error?

Porque esconde el problema: el programa sigue con datos rotos y nadie se entera de qué pasó.

### Soluciones (docente)

Sale de `21-PHP/12-Excepciones`, ampliado con la jerarquía, excepciones con datos y `finally` para liberar recursos (misión 3). En el encargo, `array_pad` evita el aviso de clave inexistente cuando un renglón tiene menos campos.

## R02-N10 · Namespaces, autoload y Composer

```meta
tipo: tema
padre: R02-N09
precio: 10
criatura: skeleton
temas: prog.modulos, cal.build
```

### Crónica

El Astillero ya tiene cientos de moldes y hubo un problema: dos talleres hicieron un molde llamado `Timon`, uno para veleros y otro para remolcadores. Nadie sabía cuál era cuál. Ahora cada taller pone su sello en los moldes: *Taller Velero / Timon*, *Taller Remolque / Timon*. Y en la entrada hay un bibliotecario que, cuando alguien pide un molde, sabe en qué estante buscarlo.

—Cuando un proyecto crece, se necesitan **apellidos** para las clases y alguien que las **busque solo** —dice {mentor}—. Los apellidos son los *namespaces*; el bibliotecario, el *autoload*. Y para usar moldes que hicieron otros talleres del mundo, {heroe}, está el mercado más grande del Puerto: **Composer**.

### Objetivos

- Organizar las clases en namespaces y usarlas con `use`.
- Seguir la convención PSR-4: un archivo por clase y carpetas que coinciden con el namespace.
- Cargar clases automáticamente con `spl_autoload_register`.
- Crear un proyecto con Composer, instalar una biblioteca y usar su autoload.
- Entender `composer.json`, `composer.lock` y la carpeta `vendor/`.

### Antes de empezar

- Organizar el código en archivos (R01-N09) y clases (toda la rama).

### Explicación

#### Namespaces
Un **namespace** es el "apellido" de una clase. Se declara en la primera línea del
archivo (después de `<?php` y `declare`):
```php
<?php
declare(strict_types=1);

namespace Puerto\Astillero;

class Timon { … }
```
El nombre completo de la clase es `Puerto\Astillero\Timon`. Otra clase `Timon` en
`Puerto\Remolque` no choca con esta.

#### `use`: importar un nombre
Para no escribir el nombre completo cada vez:
```php
use Puerto\Astillero\Timon;
use Puerto\Remolque\Timon as TimonRemolque;   // "as" para dos con el mismo nombre

$t = new Timon();
```
Las clases de PHP (como `DateTimeImmutable` o `InvalidArgumentException`) están en
el namespace **global**: adentro de un namespace se escriben con `\` adelante
(`new \DateTimeImmutable()`) o se importan con `use DateTimeImmutable;`.

#### PSR-4: una convención para encontrar las clases
La comunidad PHP acordó una regla (PSR-4):
- **una clase por archivo**, y el archivo se llama como la clase: `Timon.php`;
- el namespace coincide con las carpetas a partir de una raíz:
```
src/
└── Astillero/
    └── Timon.php      ← namespace Puerto\Astillero; class Timon
```
(`Puerto\` corresponde a `src/`, y cada parte que sigue es una carpeta.)

#### Autoload: que PHP busque solo
En lugar de un `require` por clase, se registra una función que PHP llama cada vez
que se usa una clase que todavía no conoce:
```php
spl_autoload_register(function (string $clase): void {
    $prefijo = 'Puerto\\';
    if (!str_starts_with($clase, $prefijo)) {
        return;                                   // no es nuestra: que la busque otro
    }
    $relativa = substr($clase, strlen($prefijo));            // Astillero\Timon
    $archivo = __DIR__ . '/src/' . str_replace('\\', '/', $relativa) . '.php';
    if (file_exists($archivo)) {
        require $archivo;
    }
});
```
Ese es todo el secreto del autoload. En la práctica, nadie lo escribe a mano: lo
hace Composer.

#### Composer
**Composer** es el gestor de paquetes de PHP: instala bibliotecas hechas por otros
(desde *packagist.org*) y genera el autoload. Se instala desde *getcomposer.org*
(en Windows hay un instalador; en Linux, `sudo apt install composer`).

Un proyecto nuevo:
```bash
mkdir mi-proyecto && cd mi-proyecto
composer init                  # pregunta nombre, descripción… (o escribí el composer.json a mano)
composer require nesbot/carbon # instala una biblioteca de fechas
```
Queda así:
| Archivo | Qué es |
|---|---|
| `composer.json` | lo que tu proyecto necesita (lo escribís vos) |
| `composer.lock` | las versiones **exactas** que se instalaron (se sube al repositorio) |
| `vendor/` | las bibliotecas descargadas (**no** se sube: se regenera con `composer install`) |
| `vendor/autoload.php` | el autoload de todo: tus clases y las de las bibliotecas |

Para que Composer cargue también **tus** clases, se agrega en `composer.json`:
```json
"autoload": {
    "psr-4": { "Puerto\\": "src/" }
}
```
y se ejecuta `composer dump-autoload`. El programa arranca con una sola línea:
```php
require __DIR__ . '/vendor/autoload.php';
```

#### Versiones
`"nesbot/carbon": "^3.8"` significa "la 3.8 o cualquier 3.x más nueva, pero no la
4". Composer elige la más nueva que funcione con **tu** versión de PHP.
`composer install` instala lo que dice el `.lock` (lo que usa un compañero o el
servidor); `composer update` busca versiones nuevas y actualiza el `.lock`.

### Código de ejemplo

`composer.json`
```json
{
    "name": "puerto/astillero",
    "description": "Ejemplo del Puerto: namespaces, autoload PSR-4 y una biblioteca",
    "require": {
        "php": ">=8.2",
        "nesbot/carbon": "^3.8"
    },
    "autoload": {
        "psr-4": { "Puerto\\": "src/" }
    }
}
```

`src/Astillero/Barco.php`
```php
<?php
declare(strict_types=1);

namespace Puerto\Astillero;

use Carbon\CarbonImmutable;

class Barco
{
    public function __construct(
        public readonly string $nombre,
        public readonly CarbonImmutable $botado,
    ) {}

    public function antiguedad(CarbonImmutable $hoy): string
    {
        return $this->botado->locale('es')->diffForHumans($hoy, ['syntax' => \Carbon\CarbonInterface::DIFF_ABSOLUTE]);
    }
}
```

`src/Astillero/Registro.php`
```php
<?php
declare(strict_types=1);

namespace Puerto\Astillero;

use Countable;

class Registro implements Countable
{
    /** @var Barco[] */
    private array $barcos = [];

    public function agregar(Barco $barco): void
    {
        $this->barcos[] = $barco;
    }

    public function count(): int
    {
        return count($this->barcos);
    }

    /** @return Barco[] */
    public function todos(): array
    {
        return $this->barcos;
    }
}
```

`main.php`
```php
<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

use Carbon\CarbonImmutable;
use Puerto\Astillero\Barco;
use Puerto\Astillero\Registro;

$hoy = CarbonImmutable::create(2026, 10, 3);
$registro = new Registro();
$registro->agregar(new Barco('Gaviota', CarbonImmutable::create(2019, 4, 12)));
$registro->agregar(new Barco('Albatros', CarbonImmutable::create(2026, 8, 20)));
$registro->agregar(new Barco('Tortuga', CarbonImmutable::create(1998, 1, 5)));

echo "Barcos en el registro: ", count($registro), "\n";
foreach ($registro->todos() as $barco) {
    echo "- {$barco->nombre}: botado el ", $barco->botado->locale('es')->isoFormat('D [de] MMMM [de] YYYY'),
        " (", $barco->antiguedad($hoy), ")\n";
}
echo "Clase completa: ", Barco::class, "\n";
```

### Salida esperada

```
Barcos en el registro: 3
- Gaviota: botado el 12 de abril de 2019 (7 años)
- Albatros: botado el 20 de agosto de 2026 (1 mes)
- Tortuga: botado el 5 de enero de 1998 (28 años)
Clase completa: Puerto\Astillero\Barco
```

### ¿Para qué sirve?

Todo proyecto PHP moderno arranca con `composer.json` y `require 'vendor/autoload.php'`: Laravel, Symfony, WordPress con plugins nuevos. En packagist.org hay más de 400.000 bibliotecas listas: para generar PDF, mandar mails, leer planillas de Excel, cobrar con Mercado Pago. Saber instalarlas y organizar tus clases con namespaces es el paso de "scripts sueltos" a "proyecto profesional".

### Errores habituales

**Esqueleto: la clase que no se encuentra.**
```
PHP Fatal error:  Uncaught Error: Class "Puerto\Astillero\Barco" not found
```
Revisá que el archivo se llame igual que la clase, que el namespace coincida con
las carpetas y que ejecutaste `composer dump-autoload` después de cambiar el
`autoload`.

**Esqueleto: las clases de PHP adentro de un namespace.** Dentro de
`namespace Puerto;`, `new DateTimeImmutable()` busca `Puerto\DateTimeImmutable`.
Escribí `\DateTimeImmutable` o importala con `use`.

**Slime: `namespace` después de otro código.** La declaración de namespace va antes
que cualquier otra cosa (salvo `declare`): `Namespace declaration statement has to
be the very first statement`.

**Ogro: subir `vendor/` al repositorio.** Son miles de archivos que se regeneran con
`composer install`. Se sube `composer.json` y `composer.lock`; `vendor/` va en el
`.gitignore`.

**Goblin: la versión de PHP.** `Your requirements could not be resolved…` o
`requires php >=8.3`: la biblioteca pide una versión más nueva que la tuya. Pedí una
versión anterior de la biblioteca o actualizá PHP.

### Misión R02-N10-M1 · El autoload hecho a mano

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Sin Composer, armá un proyecto con esta estructura:

```
correo/
├── main.php
└── src/
    ├── Envios/
    │   ├── Carta.php        ← namespace Correo\Envios
    │   └── Paquete.php      ← namespace Correo\Envios
    └── Tarifas/
        └── Tarifario.php    ← namespace Correo\Tarifas
```

- `Carta` (destinatario, gramos) y `Paquete` (destinatario, kilos) implementan una
  interfaz `Correo\Envios\Envio` (en `src/Envios/Envio.php`) con `pesoGramos(): int`
  y `destinatario(): string`.
- `Tarifario::precio(Envio $e): float` — $500 hasta 100 g, $1500 hasta 1 kg, y
  $1500 más $900 por cada kilo (o fracción) extra.
- `main.php` registra un autoload PSR-4 con `spl_autoload_register` (prefijo
  `Correo\` → `src/`), crea tres envíos y muestra su precio.

#### Criterio de aprobación

- Una clase por archivo, con namespaces que coinciden con las carpetas.
- No hay `require` de clases sueltas: todo lo carga el autoload.
- La salida coincide con la esperada.

#### Salida esperada

```
Kira (40 g): $500
Bron (750 g): $1500
Lía (3200 g): $4200
```

#### Solución de referencia

`src/Envios/Envio.php`
```php
<?php
declare(strict_types=1);

namespace Correo\Envios;

interface Envio
{
    public function pesoGramos(): int;

    public function destinatario(): string;
}
```

`src/Envios/Carta.php`
```php
<?php
declare(strict_types=1);

namespace Correo\Envios;

class Carta implements Envio
{
    public function __construct(private string $destinatario, private int $gramos) {}

    public function pesoGramos(): int
    {
        return $this->gramos;
    }

    public function destinatario(): string
    {
        return $this->destinatario;
    }
}
```

`src/Envios/Paquete.php`
```php
<?php
declare(strict_types=1);

namespace Correo\Envios;

class Paquete implements Envio
{
    public function __construct(private string $destinatario, private float $kilos) {}

    public function pesoGramos(): int
    {
        return (int) round($this->kilos * 1000);
    }

    public function destinatario(): string
    {
        return $this->destinatario;
    }
}
```

`src/Tarifas/Tarifario.php`
```php
<?php
declare(strict_types=1);

namespace Correo\Tarifas;

use Correo\Envios\Envio;

class Tarifario
{
    public static function precio(Envio $envio): float
    {
        $gramos = $envio->pesoGramos();
        if ($gramos <= 100) {
            return 500;
        }
        if ($gramos <= 1000) {
            return 1500;
        }
        return 1500 + ceil(($gramos - 1000) / 1000) * 900;
    }
}
```

`main.php`
```php
<?php
declare(strict_types=1);
// Mision 1 - El autoload hecho a mano: PSR-4 con spl_autoload_register.

spl_autoload_register(function (string $clase): void {
    $prefijo = 'Correo\\';
    if (!str_starts_with($clase, $prefijo)) {
        return;
    }
    $archivo = __DIR__ . '/src/' . str_replace('\\', '/', substr($clase, strlen($prefijo))) . '.php';
    if (file_exists($archivo)) {
        require $archivo;
    }
});

use Correo\Envios\Carta;
use Correo\Envios\Paquete;
use Correo\Tarifas\Tarifario;

$envios = [new Carta('Kira', 40), new Paquete('Bron', 0.75), new Paquete('Lía', 3.2)];
foreach ($envios as $envio) {
    echo $envio->destinatario(), " (", $envio->pesoGramos(), " g): $", Tarifario::precio($envio), "\n";
}
```

### Misión R02-N10-M2 · Mi primer proyecto con Composer

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Creá un proyecto con Composer que use la biblioteca **Carbon** para armar el
**calendario de mareas** del puerto (datos de mentira, para practicar fechas):

1. `composer.json` con `nesbot/carbon` y un autoload PSR-4 `Mareas\` → `src/`.
2. `src/Calendario.php` (`namespace Mareas`) con
   `pleamares(CarbonImmutable $desde, int $dias): array` — la primera pleamar es a
   las 06:10 del día `$desde` y cada una llega **12 horas y 25 minutos** después
   de la anterior; devuelve todas las que caen dentro de esos días.
3. `main.php` muestra las pleamares de 3 días desde el 5 de octubre de 2026,
   agrupadas por día, con el nombre del día en castellano
   (`->locale('es')->isoFormat('dddd D')`) y la hora (`->format('H:i')`).

Entregá el `.zip` **sin** la carpeta `vendor/` (el profe la regenera con
`composer install`).

#### Criterio de aprobación

- `composer.json` tiene la dependencia y el autoload PSR-4.
- `main.php` solo hace `require __DIR__ . '/vendor/autoload.php'`.
- El `.zip` no incluye `vendor/`.
- La salida coincide con la esperada.

#### Salida esperada

```
Lunes 5: 06:10 y 18:35
Martes 6: 07:00 y 19:25
Miércoles 7: 07:50 y 20:15
```

#### Solución de referencia

`composer.json`
```json
{
    "name": "puerto/mareas",
    "require": {
        "php": ">=8.2",
        "nesbot/carbon": "^3.8"
    },
    "autoload": {
        "psr-4": { "Mareas\\": "src/" }
    }
}
```

`src/Calendario.php`
```php
<?php
declare(strict_types=1);

namespace Mareas;

use Carbon\CarbonImmutable;

class Calendario
{
    /** @return CarbonImmutable[] */
    public function pleamares(CarbonImmutable $desde, int $dias): array
    {
        $fin = $desde->startOfDay()->addDays($dias);
        $marea = $desde->setTime(6, 10);
        $resultado = [];
        while ($marea < $fin) {
            $resultado[] = $marea;
            $marea = $marea->addHours(12)->addMinutes(25);
        }
        return $resultado;
    }
}
```

`main.php`
```php
<?php
declare(strict_types=1);
// Mision 2 - Mi primer proyecto con Composer: Carbon y autoload PSR-4.

require __DIR__ . '/vendor/autoload.php';

use Carbon\CarbonImmutable;
use Mareas\Calendario;

$porDia = [];
foreach ((new Calendario())->pleamares(CarbonImmutable::create(2026, 10, 5), 3) as $marea) {
    $dia = $marea->locale('es')->isoFormat('dddd D');
    $porDia[$dia][] = $marea->format('H:i');
}
foreach ($porDia as $dia => $horas) {
    echo ucfirst($dia), ": ", implode(' y ', $horas), "\n";
}
```

### Misión R02-N10-M3 · Los dos timones

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Dos talleres hicieron una clase `Timon` distinta, y el programa necesita las dos.
Armá un proyecto con Composer (sin dependencias externas, solo el autoload PSR-4
`Astillero\` → `src/`) con:

- `src/Velero/Timon.php` — `namespace Astillero\Velero`, gira en pasos de 15°;
- `src/Remolque/Timon.php` — `namespace Astillero\Remolque`, gira en pasos de 5° y
  tiene un límite de ±45°;
- las dos con `girar(int $pasos): void` y `angulo(): int`.

`main.php` importa las dos con `use … as …`, gira cada una y muestra el ángulo, y
muestra el nombre completo de cada clase con `::class`. Usá también
`\DateTimeImmutable` (con la barra) dentro de una de las clases para registrar el
último giro con una fecha fija (`new \DateTimeImmutable('2026-10-03 10:00')`).

#### Criterio de aprobación

- Dos clases con el mismo nombre en distintos namespaces, sin choques.
- Usa `use … as …` para importarlas.
- La salida coincide con la esperada.

#### Salida esperada

```
Remolque, último giro: nunca
Astillero\Velero\Timon: 60°
Astillero\Remolque\Timon: 45° (límite 45)
Remolque, último giro: 03/10/2026 10:00
```

#### Solución de referencia

`composer.json`
```json
{
    "name": "puerto/timones",
    "autoload": {
        "psr-4": { "Astillero\\": "src/" }
    }
}
```

`src/Velero/Timon.php`
```php
<?php
declare(strict_types=1);

namespace Astillero\Velero;

class Timon
{
    private int $angulo = 0;

    public function girar(int $pasos): void
    {
        $this->angulo += $pasos * 15;
    }

    public function angulo(): int
    {
        return $this->angulo;
    }
}
```

`src/Remolque/Timon.php`
```php
<?php
declare(strict_types=1);

namespace Astillero\Remolque;

class Timon
{
    public const LIMITE = 45;
    private int $angulo = 0;
    private ?\DateTimeImmutable $ultimoGiro = null;

    public function girar(int $pasos): void
    {
        $this->angulo = max(-self::LIMITE, min(self::LIMITE, $this->angulo + $pasos * 5));
        $this->ultimoGiro = new \DateTimeImmutable('2026-10-03 10:00');
    }

    public function angulo(): int
    {
        return $this->angulo;
    }

    public function ultimoGiro(): string
    {
        return $this->ultimoGiro?->format('d/m/Y H:i') ?? 'nunca';
    }
}
```

`main.php`
```php
<?php
declare(strict_types=1);
// Mision 3 - Los dos timones: el mismo nombre en dos namespaces.

require __DIR__ . '/vendor/autoload.php';

use Astillero\Remolque\Timon as TimonRemolque;
use Astillero\Velero\Timon as TimonVelero;

$velero = new TimonVelero();
$remolque = new TimonRemolque();
echo "Remolque, último giro: ", $remolque->ultimoGiro(), "\n";
$velero->girar(4);
$remolque->girar(4);
$remolque->girar(8);
echo TimonVelero::class, ": ", $velero->angulo(), "°\n";
echo TimonRemolque::class, ": ", $remolque->angulo(), "° (límite ", TimonRemolque::LIMITE, ")\n";
echo "Remolque, último giro: ", $remolque->ultimoGiro(), "\n";
```

### Encargo R02-N10-E1 · El generador de recibos

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Una contadora del barrio quiere un generador de recibos. Armá un proyecto con
Composer, autoload PSR-4 `Recibos\` → `src/` y la biblioteca **Carbon**:

- `src/Modelo/Item.php` — `readonly` con descripción, cantidad y precio unitario;
- `src/Modelo/Recibo.php` — número, cliente, fecha (`CarbonImmutable`) y una lista
  de ítems; `total(): float` y `vencimiento(): CarbonImmutable` (30 días después,
  pero si cae sábado o domingo, el lunes siguiente: Carbon tiene `isWeekend()` y
  `next(CarbonImmutable::MONDAY)`);
- `src/Salida/Texto.php` — `render(Recibo $r): string` que arma el recibo como texto
  con renglones alineados, la fecha escrita en castellano
  (`isoFormat('D [de] MMMM [de] YYYY')`) y el total con `number_format`.

`main.php` arma un recibo del ejemplo (fecha 2 de octubre de 2026) y lo muestra.
Entregá sin `vendor/`.

#### Criterio de aprobación

- Clases separadas en `Modelo` y `Salida`, con namespaces y PSR-4.
- Usa Carbon para la fecha y el vencimiento.
- La salida coincide con la esperada.

#### Salida esperada

```
RECIBO N.º 00142
Cliente: Almacén Don Pepe
Fecha: 2 de octubre de 2026
----------------------------------------
IVA mensual              1 x  45.000,00
Recibos de sueldo        4 x   6.500,00
Alta en ARCA             1 x  18.000,00
----------------------------------------
TOTAL                         $89.000,00
Vence: 2 de noviembre de 2026
```

#### Solución de referencia

`composer.json`
```json
{
    "name": "puerto/recibos",
    "require": {
        "php": ">=8.2",
        "nesbot/carbon": "^3.8"
    },
    "autoload": {
        "psr-4": { "Recibos\\": "src/" }
    }
}
```

`src/Modelo/Item.php`
```php
<?php
declare(strict_types=1);

namespace Recibos\Modelo;

readonly class Item
{
    public function __construct(public string $descripcion, public int $cantidad, public float $unitario) {}

    public function subtotal(): float
    {
        return $this->cantidad * $this->unitario;
    }
}
```

`src/Modelo/Recibo.php`
```php
<?php
declare(strict_types=1);

namespace Recibos\Modelo;

use Carbon\CarbonImmutable;

class Recibo
{
    /** @var Item[] */
    private array $items = [];

    public function __construct(public readonly int $numero, public readonly string $cliente, public readonly CarbonImmutable $fecha) {}

    public function agregar(Item $item): void
    {
        $this->items[] = $item;
    }

    /** @return Item[] */
    public function items(): array
    {
        return $this->items;
    }

    public function total(): float
    {
        return array_sum(array_map(fn(Item $i): float => $i->subtotal(), $this->items));
    }

    public function vencimiento(): CarbonImmutable
    {
        $vence = $this->fecha->addDays(30);
        return $vence->isWeekend() ? $vence->next(CarbonImmutable::MONDAY) : $vence;
    }
}
```

`src/Salida/Texto.php`
```php
<?php
declare(strict_types=1);

namespace Recibos\Salida;

use Recibos\Modelo\Recibo;

class Texto
{
    public function render(Recibo $r): string
    {
        $fecha = fn($f) => $f->locale('es')->isoFormat('D [de] MMMM [de] YYYY');
        $lineas = [];
        $lineas[] = sprintf('RECIBO N.º %05d', $r->numero);
        $lineas[] = "Cliente: {$r->cliente}";
        $lineas[] = 'Fecha: ' . $fecha($r->fecha);
        $lineas[] = str_repeat('-', 40);
        foreach ($r->items() as $item) {
            $lineas[] = sprintf('%-22s %3d x %10s', $item->descripcion, $item->cantidad, number_format($item->unitario, 2, ',', '.'));
        }
        $lineas[] = str_repeat('-', 40);
        $lineas[] = sprintf('%-26s %13s', 'TOTAL', '$' . number_format($r->total(), 2, ',', '.'));
        $lineas[] = 'Vence: ' . $fecha($r->vencimiento());
        return implode("\n", $lineas);
    }
}
```

`main.php`
```php
<?php
declare(strict_types=1);
// Encargo - El generador de recibos: un proyecto con namespaces y Carbon.

require __DIR__ . '/vendor/autoload.php';

use Carbon\CarbonImmutable;
use Recibos\Modelo\Item;
use Recibos\Modelo\Recibo;
use Recibos\Salida\Texto;

$recibo = new Recibo(142, 'Almacén Don Pepe', CarbonImmutable::create(2026, 10, 2));
$recibo->agregar(new Item('IVA mensual', 1, 45000));
$recibo->agregar(new Item('Recibos de sueldo', 4, 6500));
$recibo->agregar(new Item('Alta en ARCA', 1, 18000));
echo (new Texto())->render($recibo), "\n";
```

### Prueba del sello

#### ¿Para qué sirve un namespace?

Para darle un "apellido" a las clases y que dos clases con el mismo nombre en distintos namespaces no choquen.

#### ¿Qué dice la convención PSR-4?

Una clase por archivo, el archivo se llama como la clase, y las carpetas coinciden con las partes del namespace a partir de una raíz.

#### ¿Qué hace `spl_autoload_register`?

Registra una función que PHP llama cuando se usa una clase que todavía no se cargó, para que la busque y la incluya.

#### ¿Qué diferencia hay entre `composer.json` y `composer.lock`?

`composer.json` dice qué necesita el proyecto (con rangos de versiones); `composer.lock` guarda las versiones exactas instaladas.

#### ¿Por qué no se sube la carpeta `vendor/`?

Porque se regenera con `composer install` a partir de `composer.lock`: son miles de archivos que no hace falta versionar.

### Soluciones (docente)

Sale de `21-PHP/15-Namespaces-Autoload` y `16-Composer`. Se usa Carbon porque es la biblioteca de fechas de Laravel (se retoma en la Senda). Los proyectos con Composer se corrigen descomprimiendo, corriendo `composer install` y después `php main.php`; conviene tener instalado Composer en la compu del aula. En el encargo, el recibo del 2 de octubre vence el 1 de noviembre, que cae domingo: pasa al lunes 2.

## R02-N11 · Jefe: el Gólem del Astillero

```meta
tipo: jefe
padre: R02-N10
precio: 10
criatura: dragon
insignia: Sello del Gólem
insignia_descripcion: Venciste al Gólem del Astillero: diseñás sistemas con clases, interfaces, enums y excepciones.
usa: poo.interfaces, prog.enums, err.excepciones, cal.build
```

### Crónica

En el fondo del Astillero, donde se guardan los moldes viejos, algo se mueve. Es el **Gólem del Astillero**: un gigante hecho de tablas, clavos y moldes mal armados. Cada pieza fue pegada a las apuradas, sin plan: clases que heredan de lo que no son, datos públicos que cualquiera cambia, errores escondidos en `catch` vacíos. Por eso se cae a pedazos a cada paso… y por eso es tan peligroso.

—No se lo vence a martillazos —dice {mentor}—. Se lo vence **rearmando**: cada pieza con su responsabilidad, sus datos protegidos, sus contratos claros y sus errores con nombre. Hacé eso, {heroe}, y el Gólem se desarma solo.

### Objetivos

- Diseñar un sistema mediano con clases, herencia o composición, interfaces, enums y excepciones.
- Proteger las reglas del negocio con encapsulamiento y validación.
- Organizar un proyecto con namespaces, autoload PSR-4 y Composer.

### Antes de empezar

- Todos los nodos del Astillero de los Moldes (R02-N01 a R02-N10).

### Explicación

#### Cómo diseñar antes de escribir
1. **Subrayá los sustantivos** de la consigna: casi siempre son clases (barco,
   reparación, taller) o valores (dinero, fecha).
2. **Subrayá los verbos**: son métodos (reparar, cobrar, entregar).
3. Para cada dato, preguntate: ¿puede cambiar? ¿con qué reglas? Lo que no cambia,
   `readonly`; lo que cambia con reglas, `private` con un método que valide.
4. ¿Hay valores fijos (estados, tipos)? → **enum**.
5. ¿Hay cosas distintas que se usan igual? → **interfaz** (o clase abstracta si
   comparten código).
6. ¿Qué puede salir mal? → una **excepción con nombre** para cada problema del
   negocio.
7. El programa principal solo **lee, llama y muestra**.

#### La lista de control del Gólem
| El Gólem hace… | Vos hacés… |
|---|---|
| propiedades `public` que cualquiera cambia | `private` + métodos con reglas, o `readonly` |
| `if ($tipo === 'velero')` por todos lados | polimorfismo |
| estados como textos (`"en reparacion"`) | un enum |
| `return false` cuando algo falla | excepciones con nombre |
| `catch (Exception $e) {}` | atrapar donde se puede hacer algo |
| todo en un archivo de 800 líneas | namespaces y una clase por archivo |
| `new` de las dependencias adentro | recibirlas por el constructor |

### Misión R02-N11-M1 · El taller de reparaciones

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

El taller del Astillero repara embarcaciones. Escribí el sistema en un solo
archivo, con `strict_types`:

- **Embarcaciones**: clase abstracta `Embarcacion` (matrícula `readonly`, eslora) con
  `costoPorHora(): float` abstracto. Hijas: `Bote` ($12000/h), `Velero` ($15000/h
  más $2000 por cada vela) y `Lancha` ($18000/h; si tiene más de 150 HP, 20% más).
- **Estado de la reparación**: enum respaldado `Estado` con `Ingresada`,
  `EnReparacion`, `Lista` y `Entregada`, y un método `siguiente(): ?self` (el
  estado que sigue, o `null` si es el último).
- **Reparación**: clase con la embarcación, la descripción, las horas trabajadas
  (privadas) y el estado (privado). Métodos: `trabajar(float $horas)` (solo si está
  `EnReparacion`; si no, lanza `EstadoInvalido`), `avanzar()` (pasa al estado
  siguiente; si ya está entregada, `EstadoInvalido`), `costo(): float` y
  `estado(): Estado`.
- **Excepciones propias**: `EstadoInvalido extends DomainException` y
  `EmbarcacionDesconocida extends DomainException`.
- **Taller**: guarda las reparaciones por matrícula; `ingresar(Embarcacion $e,
  string $descripcion)`, `reparacion(string $matricula): Reparacion` (lanza
  `EmbarcacionDesconocida`), `informe(): string` con todas ordenadas por matrícula.

El programa lee comandos de la entrada hasta el final:
`INGRESA;TIPO;MATRICULA;ESLORA;EXTRA;DESCRIPCION` (EXTRA es la cantidad de velas o
los HP, 0 para botes), `AVANZA;MATRICULA`, `TRABAJA;MATRICULA;HORAS` e `INFORME`.
Cada comando muestra el resultado o el error atrapado (sin cortar el programa).

#### Criterio de aprobación

- Usa clase abstracta, enum con método, excepciones propias y encapsulamiento.
- No hay `if`/`match` sobre el tipo de embarcación para calcular costos (salvo al
  crearla a partir del texto del comando).
- Los errores se atrapan en el programa principal y no lo cortan.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
INGRESA;velero;LR-1024;9.5;3;cambio de jarcias
INGRESA;lancha;LR-0077;7.2;200;motor que no arranca
INGRESA;bote;LR-2230;4;0;pintura del casco
TRABAJA;LR-1024;2
AVANZA;LR-1024
TRABAJA;LR-1024;3.5
AVANZA;LR-0077
TRABAJA;LR-0077;6
AVANZA;LR-0077
AVANZA;LR-0077
AVANZA;LR-0077
TRABAJA;LR-9999;1
INGRESA;submarino;LR-0001;30;0;periscopio
INFORME
```

#### Salida esperada

```
Ingresó LR-1024 (velero): cambio de jarcias
Ingresó LR-0077 (lancha): motor que no arranca
Ingresó LR-2230 (bote): pintura del casco
Error: LR-1024 está ingresada: no se puede trabajar
LR-1024 pasa a en reparación
LR-1024: +3.5 h
LR-0077 pasa a en reparación
LR-0077: +6 h
LR-0077 pasa a lista
LR-0077 pasa a entregada
Error: LR-0077 ya fue entregada
Error: No hay ninguna embarcación LR-9999 en el taller
Error: Tipo desconocido: submarino
LR-0077  lancha  Entregada       6.0 h  $129.600,00
LR-1024  velero  EnReparacion    3.5 h  $73.500,00
LR-2230  bote    Ingresada       0.0 h  $0,00
Facturado: $203.100,00
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Jefe R02 - El taller de reparaciones: abstracta, enum, excepciones y encapsulamiento.

class EstadoInvalido extends DomainException {}

class EmbarcacionDesconocida extends DomainException {}

enum Estado: string
{
    case Ingresada = 'ingresada';
    case EnReparacion = 'en reparación';
    case Lista = 'lista';
    case Entregada = 'entregada';

    public function siguiente(): ?self
    {
        return match ($this) {
            self::Ingresada => self::EnReparacion,
            self::EnReparacion => self::Lista,
            self::Lista => self::Entregada,
            self::Entregada => null,
        };
    }
}

abstract class Embarcacion
{
    public function __construct(public readonly string $matricula, protected float $eslora) {}

    abstract public function costoPorHora(): float;

    public function tipo(): string
    {
        return strtolower(static::class);
    }
}

class Bote extends Embarcacion
{
    public function costoPorHora(): float
    {
        return 12000;
    }
}

class Velero extends Embarcacion
{
    public function __construct(string $matricula, float $eslora, private int $velas)
    {
        parent::__construct($matricula, $eslora);
    }

    public function costoPorHora(): float
    {
        return 15000 + 2000 * $this->velas;
    }
}

class Lancha extends Embarcacion
{
    public function __construct(string $matricula, float $eslora, private int $hp)
    {
        parent::__construct($matricula, $eslora);
    }

    public function costoPorHora(): float
    {
        return $this->hp > 150 ? 18000 * 1.2 : 18000;
    }
}

class Reparacion
{
    private float $horas = 0;
    private Estado $estado = Estado::Ingresada;

    public function __construct(public readonly Embarcacion $embarcacion, public readonly string $descripcion) {}

    public function trabajar(float $horas): void
    {
        if ($this->estado !== Estado::EnReparacion) {
            throw new EstadoInvalido("{$this->embarcacion->matricula} está {$this->estado->value}: no se puede trabajar");
        }
        if ($horas <= 0) {
            throw new InvalidArgumentException("Horas inválidas: $horas");
        }
        $this->horas += $horas;
    }

    public function avanzar(): void
    {
        $siguiente = $this->estado->siguiente();
        if ($siguiente === null) {
            throw new EstadoInvalido("{$this->embarcacion->matricula} ya fue entregada");
        }
        $this->estado = $siguiente;
    }

    public function estado(): Estado
    {
        return $this->estado;
    }

    public function horas(): float
    {
        return $this->horas;
    }

    public function costo(): float
    {
        return $this->horas * $this->embarcacion->costoPorHora();
    }
}

class Taller
{
    /** @var array<string, Reparacion> */
    private array $reparaciones = [];

    public function ingresar(Embarcacion $e, string $descripcion): void
    {
        if (isset($this->reparaciones[$e->matricula])) {
            throw new DomainException("{$e->matricula} ya está en el taller");
        }
        $this->reparaciones[$e->matricula] = new Reparacion($e, $descripcion);
    }

    public function reparacion(string $matricula): Reparacion
    {
        return $this->reparaciones[$matricula] ?? throw new EmbarcacionDesconocida("No hay ninguna embarcación $matricula en el taller");
    }

    public function informe(): string
    {
        $copia = $this->reparaciones;
        ksort($copia);
        $lineas = [];
        $total = 0;
        foreach ($copia as $matricula => $r) {
            $lineas[] = sprintf('%-8s %-7s %-14s %4.1f h  $%s', $matricula, $r->embarcacion->tipo(), $r->estado()->name, $r->horas(), number_format($r->costo(), 2, ',', '.'));
            $total += $r->costo();
        }
        $lineas[] = 'Facturado: $' . number_format($total, 2, ',', '.');
        return implode("\n", $lineas);
    }
}

function crearEmbarcacion(string $tipo, string $matricula, float $eslora, int $extra): Embarcacion
{
    return match ($tipo) {
        'bote' => new Bote($matricula, $eslora),
        'velero' => new Velero($matricula, $eslora, $extra),
        'lancha' => new Lancha($matricula, $eslora, $extra),
        default => throw new InvalidArgumentException("Tipo desconocido: $tipo"),
    };
}

$taller = new Taller();
while (($linea = fgets(STDIN)) !== false) {
    $campos = explode(';', trim($linea));
    if ($campos[0] === '') {
        continue;
    }
    try {
        switch ($campos[0]) {
            case 'INGRESA':
                [, $tipo, $matricula, $eslora, $extra, $descripcion] = $campos;
                $taller->ingresar(crearEmbarcacion($tipo, $matricula, (float) $eslora, (int) $extra), $descripcion);
                echo "Ingresó $matricula ($tipo): $descripcion\n";
                break;
            case 'AVANZA':
                $r = $taller->reparacion($campos[1]);
                $r->avanzar();
                echo "{$campos[1]} pasa a {$r->estado()->value}\n";
                break;
            case 'TRABAJA':
                $taller->reparacion($campos[1])->trabajar((float) $campos[2]);
                echo "{$campos[1]}: +{$campos[2]} h\n";
                break;
            case 'INFORME':
                echo $taller->informe(), "\n";
                break;
            default:
                echo "Comando desconocido: {$campos[0]}\n";
        }
    } catch (DomainException | InvalidArgumentException $e) {
        echo "Error: ", $e->getMessage(), "\n";
    }
}
```

#### Pruebas

##### Solo informe
```entrada
INFORME
```
```salida
Facturado: $0,00
```

##### Bote completo
```entrada
INGRESA;bote;B-1;3;0;remos
AVANZA;B-1
TRABAJA;B-1;1.5
AVANZA;B-1
AVANZA;B-1
INFORME
```
```salida
Ingresó B-1 (bote): remos
B-1 pasa a en reparación
B-1: +1.5 h
B-1 pasa a lista
B-1 pasa a entregada
B-1      bote    Entregada       1.5 h  $18.000,00
Facturado: $18.000,00
```

##### Lancha chica sin recargo
```entrada
INGRESA;lancha;L-1;5;150;aceite
AVANZA;L-1
TRABAJA;L-1;2
INFORME
```
```salida
Ingresó L-1 (lancha): aceite
L-1 pasa a en reparación
L-1: +2 h
L-1      lancha  EnReparacion    2.0 h  $36.000,00
Facturado: $36.000,00
```

### Misión R02-N11-M2 · El alquiler de botes

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 30
```

#### Consigna

El Puerto alquila botes a los turistas. Armá un **proyecto con Composer** (autoload
PSR-4 `Alquiler\` → `src/`, sin dependencias externas) con esta estructura:

```
alquiler/
├── composer.json
├── main.php
└── src/
    ├── Modelo/
    │   ├── Dinero.php           ← readonly: centavos (int), sumar, multiplicar, __toString
    │   ├── TipoBote.php         ← enum: Kayak, Remo, Pedalin, con tarifaPorHora(): Dinero
    │   ├── Bote.php             ← código (readonly), tipo, disponible (privado)
    │   └── Alquiler.php         ← bote, cliente, horas, total(): Dinero
    ├── Repositorio/
    │   ├── Botes.php            ← interfaz: guardar, buscar(código): Bote, disponibles(): array
    │   └── BotesEnMemoria.php   ← implementación con un array
    ├── Excepciones/
    │   ├── BoteNoDisponible.php
    │   └── BoteInexistente.php
    └── Servicio/
        └── Muelle.php           ← recibe el repositorio por el constructor
```

Reglas del negocio (en `Muelle`):
- `alquilar(string $codigo, string $cliente, int $horas): Alquiler` — el bote tiene
  que existir y estar disponible; las horas, entre 1 y 8; queda no disponible.
- `devolver(string $codigo): void` — vuelve a estar disponible.
- Tarifas por hora: kayak $4500, bote a remo $6000, pedalín $7500. Si el alquiler
  es de 4 horas o más, 15% de descuento (usá `Dinero::multiplicar`).
- `resumen(): string` — lo recaudado y los botes disponibles.

`main.php` carga los botes del ejemplo en el repositorio y procesa los comandos de
la entrada (`ALQUILA;CODIGO;CLIENTE;HORAS`, `DEVUELVE;CODIGO`, `RESUMEN`)
mostrando el resultado o el error. Entregá el `.zip` sin `vendor/`.

#### Criterio de aprobación

- Una clase por archivo, con namespaces y PSR-4.
- `Dinero` es inmutable y trabaja en centavos; `TipoBote` es un enum con método.
- `Muelle` depende de la **interfaz** `Botes`, recibida por el constructor.
- Los errores son excepciones propias y se atrapan en `main.php`.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
ALQUILA;K-01;Kira;2
ALQUILA;K-01;Bron;1
ALQUILA;P-07;Familia Díaz;4
ALQUILA;R-03;Lía;12
ALQUILA;X-99;Olmo;1
DEVUELVE;K-01
ALQUILA;K-01;Bron;3
RESUMEN
```

#### Salida esperada

```
Kira alquila K-01 (kayak) por 2 h: $9.000,00
No se pudo: El bote K-01 está alquilado
Familia Díaz alquila P-07 (pedalín) por 4 h: $25.500,00
No se pudo: Se alquila de 1 a 8 horas (pediste 12)
No se pudo: No existe el bote X-99
Devuelto K-01
Bron alquila K-01 (kayak) por 3 h: $13.500,00
Recaudado: $48.000,00
Disponibles: K-02, R-03
```

#### Solución de referencia

`composer.json`
```json
{
    "name": "puerto/alquiler",
    "autoload": {
        "psr-4": { "Alquiler\\": "src/" }
    }
}
```

`src/Modelo/Dinero.php`
```php
<?php
declare(strict_types=1);

namespace Alquiler\Modelo;

readonly class Dinero
{
    private function __construct(public int $centavos) {}

    public static function pesos(float $pesos): self
    {
        return new self((int) round($pesos * 100));
    }

    public static function cero(): self
    {
        return new self(0);
    }

    public function sumar(Dinero $otro): self
    {
        return new self($this->centavos + $otro->centavos);
    }

    public function multiplicar(float $factor): self
    {
        return new self((int) round($this->centavos * $factor));
    }

    public function __toString(): string
    {
        return '$' . number_format($this->centavos / 100, 2, ',', '.');
    }
}
```

`src/Modelo/TipoBote.php`
```php
<?php
declare(strict_types=1);

namespace Alquiler\Modelo;

enum TipoBote: string
{
    case Kayak = 'kayak';
    case Remo = 'bote a remo';
    case Pedalin = 'pedalín';

    public function tarifaPorHora(): Dinero
    {
        return Dinero::pesos(match ($this) {
            self::Kayak => 4500,
            self::Remo => 6000,
            self::Pedalin => 7500,
        });
    }
}
```

`src/Modelo/Bote.php`
```php
<?php
declare(strict_types=1);

namespace Alquiler\Modelo;

class Bote
{
    private bool $disponible = true;

    public function __construct(public readonly string $codigo, public readonly TipoBote $tipo) {}

    public function disponible(): bool
    {
        return $this->disponible;
    }

    public function ocupar(): void
    {
        $this->disponible = false;
    }

    public function liberar(): void
    {
        $this->disponible = true;
    }
}
```

`src/Modelo/Alquiler.php`
```php
<?php
declare(strict_types=1);

namespace Alquiler\Modelo;

readonly class Alquiler
{
    public const HORAS_DESCUENTO = 4;
    public const DESCUENTO = 0.15;

    public function __construct(public Bote $bote, public string $cliente, public int $horas) {}

    public function total(): Dinero
    {
        $total = $this->bote->tipo->tarifaPorHora()->multiplicar($this->horas);
        return $this->horas >= self::HORAS_DESCUENTO ? $total->multiplicar(1 - self::DESCUENTO) : $total;
    }
}
```

`src/Repositorio/Botes.php`
```php
<?php
declare(strict_types=1);

namespace Alquiler\Repositorio;

use Alquiler\Modelo\Bote;

interface Botes
{
    public function guardar(Bote $bote): void;

    public function buscar(string $codigo): Bote;

    /** @return Bote[] */
    public function disponibles(): array;
}
```

`src/Repositorio/BotesEnMemoria.php`
```php
<?php
declare(strict_types=1);

namespace Alquiler\Repositorio;

use Alquiler\Excepciones\BoteInexistente;
use Alquiler\Modelo\Bote;

class BotesEnMemoria implements Botes
{
    /** @var array<string, Bote> */
    private array $botes = [];

    public function guardar(Bote $bote): void
    {
        $this->botes[$bote->codigo] = $bote;
    }

    public function buscar(string $codigo): Bote
    {
        return $this->botes[$codigo] ?? throw new BoteInexistente("No existe el bote $codigo");
    }

    public function disponibles(): array
    {
        $libres = array_filter($this->botes, fn(Bote $b): bool => $b->disponible());
        ksort($libres);
        return array_values($libres);
    }
}
```

`src/Excepciones/BoteNoDisponible.php`
```php
<?php
declare(strict_types=1);

namespace Alquiler\Excepciones;

class BoteNoDisponible extends \DomainException {}
```

`src/Excepciones/BoteInexistente.php`
```php
<?php
declare(strict_types=1);

namespace Alquiler\Excepciones;

class BoteInexistente extends \DomainException {}
```

`src/Servicio/Muelle.php`
```php
<?php
declare(strict_types=1);

namespace Alquiler\Servicio;

use Alquiler\Excepciones\BoteNoDisponible;
use Alquiler\Modelo\Alquiler;
use Alquiler\Modelo\Bote;
use Alquiler\Modelo\Dinero;
use Alquiler\Repositorio\Botes;
use InvalidArgumentException;

class Muelle
{
    private Dinero $recaudado;

    public function __construct(private Botes $botes)
    {
        $this->recaudado = Dinero::cero();
    }

    public function alquilar(string $codigo, string $cliente, int $horas): Alquiler
    {
        if ($horas < 1 || $horas > 8) {
            throw new InvalidArgumentException("Se alquila de 1 a 8 horas (pediste $horas)");
        }
        $bote = $this->botes->buscar($codigo);
        if (!$bote->disponible()) {
            throw new BoteNoDisponible("El bote $codigo está alquilado");
        }
        $bote->ocupar();
        $alquiler = new Alquiler($bote, $cliente, $horas);
        $this->recaudado = $this->recaudado->sumar($alquiler->total());
        return $alquiler;
    }

    public function devolver(string $codigo): void
    {
        $this->botes->buscar($codigo)->liberar();
    }

    public function resumen(): string
    {
        $libres = array_map(fn(Bote $b): string => $b->codigo, $this->botes->disponibles());
        return "Recaudado: {$this->recaudado}\nDisponibles: " . implode(', ', $libres);
    }
}
```

`main.php`
```php
<?php
declare(strict_types=1);
// Jefe R02 - El alquiler de botes: un proyecto con Composer, namespaces y capas.

require __DIR__ . '/vendor/autoload.php';

use Alquiler\Modelo\Bote;
use Alquiler\Modelo\TipoBote;
use Alquiler\Repositorio\BotesEnMemoria;
use Alquiler\Servicio\Muelle;

$repositorio = new BotesEnMemoria();
foreach ([['K-01', TipoBote::Kayak], ['K-02', TipoBote::Kayak], ['R-03', TipoBote::Remo], ['P-07', TipoBote::Pedalin]] as [$codigo, $tipo]) {
    $repositorio->guardar(new Bote($codigo, $tipo));
}
$muelle = new Muelle($repositorio);

while (($linea = fgets(STDIN)) !== false) {
    $campos = explode(';', trim($linea));
    try {
        switch ($campos[0]) {
            case 'ALQUILA':
                $alquiler = $muelle->alquilar($campos[1], $campos[2], (int) $campos[3]);
                echo "{$alquiler->cliente} alquila {$alquiler->bote->codigo} ({$alquiler->bote->tipo->value}) por {$alquiler->horas} h: {$alquiler->total()}\n";
                break;
            case 'DEVUELVE':
                $muelle->devolver($campos[1]);
                echo "Devuelto {$campos[1]}\n";
                break;
            case 'RESUMEN':
                echo $muelle->resumen(), "\n";
                break;
        }
    } catch (DomainException | InvalidArgumentException $e) {
        echo "No se pudo: ", $e->getMessage(), "\n";
    }
}
```

### Prueba del sello

#### ¿Qué pistas de la consigna indican las clases y los métodos?

Los sustantivos suelen ser clases o valores; los verbos, métodos.

#### ¿Qué conviene usar para los estados de una reparación?

Un enum: solo admite los estados declarados y puede tener métodos (como el estado siguiente).

#### ¿Por qué `Muelle` recibe la interfaz `Botes` y no `BotesEnMemoria`?

Para no depender de dónde se guardan los botes: mañana se puede pasar un repositorio con base de datos sin cambiar `Muelle`.

#### ¿Por qué `Dinero` trabaja en centavos enteros y es inmutable?

Los enteros evitan los errores de redondeo de los `float`, y la inmutabilidad evita que alguien cambie un monto que otro está usando.

#### ¿Dónde se atrapan las excepciones del negocio en estos proyectos?

En el programa principal (`main.php`), que es donde se puede hacer algo: mostrar el error y seguir con el próximo comando.

### Soluciones (docente)

Jefe de la rama 2: integra todo el Astillero. La misión 1 es un solo archivo para corregir rápido el diseño (abstracta, enum, excepciones); la 2 es un proyecto con Composer en capas (modelo, repositorio, servicio), el mismo esqueleto que se usa en la rama de MariaDB, donde `BotesEnMemoria` se reemplaza por un repositorio con PDO. El capítulo original no tenía jefe en este punto: se escribió desde cero. Al corregir la misión 2: `composer install` y `php main.php < entrada.txt`.

