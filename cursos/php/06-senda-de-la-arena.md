# RAMA S01 · Senda de la Arena: un RPG por turnos

```meta
tipo: senda
posicion: 6
```

## S01-N01 · El modelo de la Arena: personajes, enemigos y dados

```meta
tipo: tema
padre: R05-N08
precio: 3
moneda: comodin
criatura: slime
ejecutable: no
temas: juegos.turnos
usa: poo.abstractas, prog.enums, poo.interfaces
```

### Crónica

El primer camino desde la Encrucijada termina en la **Arena del Puerto**: un círculo de arena rodeado de gradas, donde los marineros ponen a prueba su valor contra criaturas traídas de todo el mundo. En la puerta, un maestro de armas anota a cada luchador en su pizarra: nombre, vida, fuerza, lo que lleva en la mochila.

—Acá vas a construir un **juego** —dice {mentor}—: un RPG por turnos que se juega en la terminal. Pero un juego es un sistema como cualquier otro, {heroe}: primero se diseña el **modelo**. ¿Qué es un personaje? ¿Qué sabe hacer? ¿Y cómo tiramos los dados sin que el azar nos impida probar el juego?

### Objetivos

- Modelar personajes con una clase abstracta, herencia y encapsulamiento.
- Representar los tipos de enemigo con un enum con sus valores base.
- Armar un inventario de objetos con límites.
- Aislar el azar detrás de una interfaz `Dados` con una versión con semilla (repetible) y una fija (para probar).

### Antes de empezar

- La Encrucijada de los Sellos (R05-N08): toda la rama de objetos, en especial clases abstractas, interfaces y enums.

### Explicación

#### El modelo
| Clase | Es | Sabe |
|---|---|---|
| `Personaje` (abstracta) | alguien que pelea | recibir daño, curarse, decir si está vivo |
| `Heroe` | el jugador | usar objetos de su inventario, subir de nivel |
| `Enemigo` | una criatura | su tipo (un enum) define la vida y el ataque |
| `Objeto` | una poción, una bomba | cuánto cura o cuánto daña |
| `Inventario` | la mochila | guardar hasta N objetos, sacar uno |

La vida es **privada** y solo cambia con `recibirDanio` y `curar`, que respetan los
límites (nunca menos de 0 ni más que el máximo): ningún error del motor puede dejar a
un personaje con vida negativa.

#### El azar, bajo control
Un juego necesita dados, pero un programa con `random_int` es imposible de probar:
cada vez da distinto. La solución es la misma que con los repositorios: una
**interfaz** y varias implementaciones.
```php
interface Dados
{
    public function tirar(int $caras): int;   // de 1 a $caras
}

final class DadosConSemilla implements Dados      // el juego de verdad (con semilla, repetible)
{
    public function __construct(int $semilla) { mt_srand($semilla); }
    public function tirar(int $caras): int { return mt_rand(1, $caras); }
}

final class DadosTrucados implements Dados        // para las pruebas: tiradas fijas
{
    public function __construct(private array $tiradas) {}
    public function tirar(int $caras): int { return array_shift($this->tiradas) ?? 1; }
}
```
Con la **misma semilla**, `mt_rand` da siempre la misma secuencia: el combate se
puede repetir exacto (ideal para buscar un error). Para jugar "de verdad", la semilla
sale de la hora (`time()`).

### Código de ejemplo

```php
<?php
declare(strict_types=1);
/*
 * La pizarra del maestro de armas: el modelo del RPG.
 */
interface Dados
{
    public function tirar(int $caras): int;
}

final class DadosConSemilla implements Dados
{
    public function __construct(int $semilla)
    {
        mt_srand($semilla);
    }

    public function tirar(int $caras): int
    {
        return mt_rand(1, $caras);
    }
}

enum TipoEnemigo: string
{
    case Slime = 'slime';
    case Goblin = 'goblin';
    case Orco = 'orco';
    case Dragon = 'dragón';

    public function vida(): int
    {
        return match ($this) {
            self::Slime => 12,
            self::Goblin => 20,
            self::Orco => 45,
            self::Dragon => 120,
        };
    }

    public function ataque(): int
    {
        return match ($this) {
            self::Slime => 3,
            self::Goblin => 5,
            self::Orco => 9,
            self::Dragon => 18,
        };
    }
}

abstract class Personaje
{
    private int $vida;

    public function __construct(public readonly string $nombre, private int $vidaMaxima, protected int $ataque)
    {
        $this->vida = $vidaMaxima;
    }

    public function recibirDanio(int $cantidad): int
    {
        $antes = $this->vida;
        $this->vida = max(0, $this->vida - max(0, $cantidad));
        return $antes - $this->vida;
    }

    public function curar(int $cantidad): int
    {
        $antes = $this->vida;
        $this->vida = min($this->vidaMaxima, $this->vida + max(0, $cantidad));
        return $this->vida - $antes;
    }

    public function vida(): int
    {
        return $this->vida;
    }

    public function vidaMaxima(): int
    {
        return $this->vidaMaxima;
    }

    public function ataque(): int
    {
        return $this->ataque;
    }

    public function estaVivo(): bool
    {
        return $this->vida > 0;
    }

    public function barra(): string
    {
        $llenos = (int) round($this->vida / $this->vidaMaxima * 10);
        return '[' . str_repeat('#', $llenos) . str_repeat('.', 10 - $llenos) . "] {$this->vida}/{$this->vidaMaxima}";
    }
}

final class Enemigo extends Personaje
{
    public function __construct(public readonly TipoEnemigo $tipo)
    {
        parent::__construct(ucfirst($tipo->value), $tipo->vida(), $tipo->ataque());
    }
}

readonly class Objeto
{
    public function __construct(public string $nombre, public int $cura = 0, public int $danio = 0) {}
}

final class Inventario
{
    private array $objetos = [];

    public function __construct(private int $capacidad) {}

    public function guardar(Objeto $o): bool
    {
        if (count($this->objetos) >= $this->capacidad) {
            return false;
        }
        $this->objetos[] = $o;
        return true;
    }

    public function sacar(string $nombre): ?Objeto
    {
        foreach ($this->objetos as $i => $o) {
            if ($o->nombre === $nombre) {
                unset($this->objetos[$i]);
                return $o;
            }
        }
        return null;
    }

    public function contenido(): array
    {
        return array_count_values(array_map(fn(Objeto $o) => $o->nombre, $this->objetos));
    }
}

final class Heroe extends Personaje
{
    public readonly Inventario $mochila;

    public function __construct(string $nombre)
    {
        parent::__construct($nombre, 60, 8);
        $this->mochila = new Inventario(4);
    }

    public function usar(string $objeto, ?Personaje $objetivo = null): string
    {
        $o = $this->mochila->sacar($objeto) ?? throw new DomainException("No tenés $objeto");
        if ($o->cura > 0) {
            return "{$this->nombre} usa $objeto y recupera " . $this->curar($o->cura) . ' de vida';
        }
        return "{$this->nombre} tira $objeto: " . $objetivo->recibirDanio($o->danio) . " de daño a {$objetivo->nombre}";
    }
}

$dados = new DadosConSemilla(2026);
$kira = new Heroe('Kira');
foreach ([new Objeto('poción', cura: 20), new Objeto('poción', cura: 20), new Objeto('bomba', danio: 25), new Objeto('pan', cura: 5), new Objeto('escudo')] as $o) {
    echo "Guardar {$o->nombre}: ", $kira->mochila->guardar($o) ? 'ok' : 'la mochila está llena', "\n";
}
echo "Mochila: ", json_encode($kira->mochila->contenido(), JSON_UNESCAPED_UNICODE), "\n";

$orco = new Enemigo(TipoEnemigo::Orco);
echo "{$kira->nombre} {$kira->barra()} contra {$orco->nombre} {$orco->barra()}\n";
$tirada = $dados->tirar(6);
echo "Kira tira un $tirada y pega ", $orco->recibirDanio($kira->ataque() + $tirada), "\n";
echo $kira->usar('bomba', $orco), "\n";
echo "{$orco->nombre} {$orco->barra()}\n";
$kira->recibirDanio(35);
echo $kira->usar('poción'), " → {$kira->barra()}\n";
echo "Curar de más no pasa el máximo: +", $kira->curar(500), " → {$kira->barra()}\n";
echo "Tiradas con la semilla 2026: ", implode(' ', array_map(fn() => $dados->tirar(20), range(1, 5))), "\n";
```

### Salida esperada

```
Guardar poción: ok
Guardar poción: ok
Guardar bomba: ok
Guardar pan: ok
Guardar escudo: la mochila está llena
Mochila: {"poción":2,"bomba":1,"pan":1}
Kira [##########] 60/60 contra Orco [##########] 45/45
Kira tira un 4 y pega 12
Kira tira bomba: 25 de daño a Orco
Orco [##........] 8/45
Kira usa poción y recupera 20 de vida → [########..] 45/60
Curar de más no pasa el máximo: +15 → [##########] 60/60
Tiradas con la semilla 2026: 15 19 17 2 18
```

### ¿Para qué sirve?

Todo juego de rol, de cartas o de estrategia se arma con un modelo así: entidades con reglas y un azar controlado. Controlar el azar con una semilla es lo mismo que se hace en los sistemas serios para reproducir un error ("con la semilla 2026 falla en el turno 7"), y la interfaz `Dados` es el mismo truco de la inyección de dependencias que usaste con los repositorios.

### Errores habituales

**Troll: la vida pública.** Si `$vida` es `public`, cualquier parte del juego la puede
dejar en `-15`. Privada, con métodos que respetan los límites.

**Ogro: `random_int` adentro del modelo.** Hace el juego imposible de probar. El azar
entra por la interfaz `Dados`.

**Ogro: la semilla en cada tirada.** Llamar a `mt_srand` antes de cada `mt_rand`
reinicia la secuencia y da siempre el mismo número. Una sola vez, al crear los dados.

**Esqueleto: el objeto que no está.** `sacar('espada')` de una mochila sin espada
devuelve `null`: revisalo antes de usarlo (o lanzá una excepción con nombre).

**Goblin: la barra con división por cero.** Si la vida máxima fuera 0, la barra
dividiría por cero: valídalo en el constructor.

### Misión S01-N01-M1 · Los luchadores de la Arena

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Agregá al modelo una **clase de héroe**: un enum `Clase` con `Guerrero` (vida 70,
ataque 9, defensa 3), `Maga` (vida 45, ataque 13, defensa 1) y `Arquero` (vida 55,
ataque 11, defensa 2). El `Heroe` recibe su clase en el constructor y la **defensa**
se resta a todo el daño que recibe (nunca menos de 1). Creá un héroe de cada clase,
hacé que cada uno reciba un golpe de 10 y otro de 2, y mostrá su barra de vida
después de cada golpe.

#### Criterio de aprobación

- La clase del héroe es un enum con sus valores.
- La defensa se aplica en `recibirDanio` (redefinido) y el daño mínimo es 1.
- La salida coincide con la esperada.

#### Salida esperada

```
Bron (guerrero)
  golpe de 10 → recibe 7 [#########.] 63/70
  golpe de 2 → recibe 1 [#########.] 62/70
Lía (maga)
  golpe de 10 → recibe 9 [########..] 36/45
  golpe de 2 → recibe 1 [########..] 35/45
Olmo (arquero)
  golpe de 10 → recibe 8 [#########.] 47/55
  golpe de 2 → recibe 1 [########..] 46/55
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - Los luchadores de la Arena: una clase de héroe con defensa.

enum Clase: string
{
    case Guerrero = 'guerrero';
    case Maga = 'maga';
    case Arquero = 'arquero';

    public function vida(): int
    {
        return match ($this) { self::Guerrero => 70, self::Maga => 45, self::Arquero => 55 };
    }

    public function ataque(): int
    {
        return match ($this) { self::Guerrero => 9, self::Maga => 13, self::Arquero => 11 };
    }

    public function defensa(): int
    {
        return match ($this) { self::Guerrero => 3, self::Maga => 1, self::Arquero => 2 };
    }
}

abstract class Personaje
{
    private int $vida;

    public function __construct(public readonly string $nombre, private int $vidaMaxima, protected int $ataque)
    {
        $this->vida = $vidaMaxima;
    }

    public function recibirDanio(int $cantidad): int
    {
        $antes = $this->vida;
        $this->vida = max(0, $this->vida - max(0, $cantidad));
        return $antes - $this->vida;
    }

    public function barra(): string
    {
        $llenos = (int) round($this->vida / $this->vidaMaxima * 10);
        return '[' . str_repeat('#', $llenos) . str_repeat('.', 10 - $llenos) . "] {$this->vida}/{$this->vidaMaxima}";
    }
}

final class Heroe extends Personaje
{
    public function __construct(string $nombre, public readonly Clase $clase)
    {
        parent::__construct($nombre, $clase->vida(), $clase->ataque());
    }

    public function recibirDanio(int $cantidad): int
    {
        return parent::recibirDanio(max(1, $cantidad - $this->clase->defensa()));
    }
}

foreach ([new Heroe('Bron', Clase::Guerrero), new Heroe('Lía', Clase::Maga), new Heroe('Olmo', Clase::Arquero)] as $h) {
    echo "{$h->nombre} ({$h->clase->value})\n";
    foreach ([10, 2] as $golpe) {
        $recibido = $h->recibirDanio($golpe);
        echo "  golpe de $golpe → recibe $recibido {$h->barra()}\n";
    }
}
```

### Misión S01-N01-M2 · Los dados trucados

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `DadosTrucados` (recibe un array de tiradas y las devuelve en orden; si se
terminan, vuelve a empezar) y una función `ataque(Personaje $a, Personaje $d, Dados
$dados): string` con esta regla: se tira un **d20**; con 1 es **pifia** (0 de daño),
con 20 es **crítico** (el doble del ataque más un d6), con 2 a 19 el daño es el
ataque más un d6 si la tirada supera 5, o la mitad del ataque (redondeado para
abajo) si no. Probá la regla con tiradas trucadas que cubran los cuatro casos y
mostrá cada ataque.

#### Criterio de aprobación

- `DadosTrucados` implementa la interfaz `Dados`.
- La regla cubre pifia, crítico, golpe normal y golpe débil.
- La salida coincide con la esperada.

#### Salida esperada

```
Turno 1: d20=1 pifia: Kira hace 0 a Troll (le queda 70)
Turno 2: d20=20 crítico: Kira hace 22 a Troll (le queda 48)
Turno 3: d20=12 golpe: Kira hace 12 a Troll (le queda 36)
Turno 4: d20=5 golpe débil: Kira hace 4 a Troll (le queda 32)
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 2 - Los dados trucados: probar una regla de combate sin azar.

interface Dados
{
    public function tirar(int $caras): int;
}

final class DadosTrucados implements Dados
{
    private int $posicion = 0;

    public function __construct(private array $tiradas) {}

    public function tirar(int $caras): int
    {
        $valor = $this->tiradas[$this->posicion % count($this->tiradas)];
        $this->posicion++;
        return $valor;
    }
}

final class Personaje
{
    public function __construct(public readonly string $nombre, public int $vida, public readonly int $ataque) {}
}

function ataque(Personaje $a, Personaje $d, Dados $dados): string
{
    $d20 = $dados->tirar(20);
    [$danio, $tipo] = match (true) {
        $d20 === 1 => [0, 'pifia'],
        $d20 === 20 => [$a->ataque * 2 + $dados->tirar(6), 'crítico'],
        $d20 > 5 => [$a->ataque + $dados->tirar(6), 'golpe'],
        default => [intdiv($a->ataque, 2), 'golpe débil'],
    };
    $d->vida = max(0, $d->vida - $danio);
    return "d20=$d20 $tipo: {$a->nombre} hace $danio a {$d->nombre} (le queda {$d->vida})";
}

$kira = new Personaje('Kira', 60, 9);
$troll = new Personaje('Troll', 70, 11);
$dados = new DadosTrucados([1, 20, 4, 12, 3, 5]);   // pifia; crítico + d6=4; golpe + d6=3; débil
foreach (range(1, 4) as $turno) {
    echo "Turno $turno: ", ataque($kira, $troll, $dados), "\n";
}
```

### Misión S01-N01-M3 · La mochila con peso

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Cambiá el inventario: en lugar de una cantidad máxima de objetos, tiene un **peso
máximo** (en kg). Cada `Objeto` tiene peso. `guardar` rechaza lo que no entra (y dice
cuánto sobra), `sacar` devuelve el objeto, `pesoActual()` y `resumen()` muestra cada
objeto con su cantidad y el peso total. Además, `masPesado(): ?Objeto`. Llenala con
los objetos del ejemplo (capacidad 10 kg) y mostrá qué entra y qué no.

#### Criterio de aprobación

- El límite es por peso y el mensaje dice cuánto se pasa.
- El resumen agrupa por nombre.
- La salida coincide con la esperada.

#### Salida esperada

```
espada guardado
poción guardado
poción guardado
escudo guardado
yunque no entra: se pasa por 10.5 kg
cuerda no entra: se pasa por 0.3 kg
antorcha guardado
Mochila: antorcha x1, escudo x1, espada x1, poción x2 (9.4/10 kg)
Lo más pesado: escudo
Sin el escudo: antorcha x1, espada x1, poción x2 (5.4/10 kg)
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - La mochila con peso: un inventario con límite de kilos.

readonly class Objeto
{
    public function __construct(public string $nombre, public float $peso) {}
}

final class Mochila
{
    /** @var Objeto[] */
    private array $objetos = [];

    public function __construct(private float $capacidad) {}

    public function pesoActual(): float
    {
        return array_sum(array_map(fn(Objeto $o) => $o->peso, $this->objetos));
    }

    public function guardar(Objeto $o): string
    {
        $exceso = $this->pesoActual() + $o->peso - $this->capacidad;
        if ($exceso > 0) {
            return "{$o->nombre} no entra: se pasa por " . round($exceso, 2) . ' kg';
        }
        $this->objetos[] = $o;
        return "{$o->nombre} guardado";
    }

    public function sacar(string $nombre): ?Objeto
    {
        foreach ($this->objetos as $i => $o) {
            if ($o->nombre === $nombre) {
                unset($this->objetos[$i]);
                return $o;
            }
        }
        return null;
    }

    public function masPesado(): ?Objeto
    {
        $mayor = null;
        foreach ($this->objetos as $o) {
            if ($mayor === null || $o->peso > $mayor->peso) {
                $mayor = $o;
            }
        }
        return $mayor;
    }

    public function resumen(): string
    {
        $cantidades = array_count_values(array_map(fn(Objeto $o) => $o->nombre, $this->objetos));
        ksort($cantidades);
        $partes = array_map(fn($n, $c) => "$n x$c", array_keys($cantidades), $cantidades);
        return implode(', ', $partes) . ' (' . $this->pesoActual() . "/{$this->capacidad} kg)";
    }
}

$mochila = new Mochila(10);
foreach ([new Objeto('espada', 3.5), new Objeto('poción', 0.5), new Objeto('poción', 0.5), new Objeto('escudo', 4), new Objeto('yunque', 12), new Objeto('cuerda', 1.8), new Objeto('antorcha', 0.9)] as $o) {
    echo $mochila->guardar($o), "\n";
}
echo "Mochila: ", $mochila->resumen(), "\n";
echo "Lo más pesado: ", $mochila->masPesado()->nombre, "\n";
$mochila->sacar('escudo');
echo "Sin el escudo: ", $mochila->resumen(), "\n";
```

### Encargo S01-N01-E1 · La tienda del herrero

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Antes de entrar a la Arena, el héroe pasa por la tienda del herrero. Modelá:

- el enum `Rareza` (`comun`, `raro`, `epico`) con un multiplicador de precio (1, 2.5,
  6) y un símbolo (`·`, `*`, `**`);
- `Arma` (`readonly`: nombre, daño base, rareza) con `precio()` = daño × 150 ×
  multiplicador;
- `Tienda` con su lista de armas y `comprar(Heroe $h, string $arma): string` que
  verifica el oro del héroe, se lo descuenta y le equipa el arma (el ataque del héroe
  pasa a ser su ataque base más el daño del arma).

Mostrá el catálogo ordenado por precio y tres compras del ejemplo (una sin oro
suficiente).

#### Criterio de aprobación

- Usa un enum con métodos para la rareza.
- La compra valida el oro y actualiza el ataque.
- La salida coincide con la esperada.

#### Salida esperada

```
· daga (+3): 450 de oro
· espada larga (+6): 900 de oro
* arco élfico (+7): 2625 de oro
** martillo del volcán (+12): 10800 de oro
Kira no puede comprar martillo del volcán: cuesta 10800 y tiene 3000
Kira compra arco élfico: ataque 15, le quedan 375 de oro
Kira no puede comprar espada larga: cuesta 900 y tiene 375
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - La tienda del herrero: enums con precio y un héroe que se equipa.

enum Rareza: string
{
    case Comun = 'comun';
    case Raro = 'raro';
    case Epico = 'epico';

    public function multiplicador(): float
    {
        return match ($this) { self::Comun => 1, self::Raro => 2.5, self::Epico => 6 };
    }

    public function simbolo(): string
    {
        return match ($this) { self::Comun => '·', self::Raro => '*', self::Epico => '**' };
    }
}

readonly class Arma
{
    public function __construct(public string $nombre, public int $danio, public Rareza $rareza) {}

    public function precio(): int
    {
        return (int) ($this->danio * 150 * $this->rareza->multiplicador());
    }
}

final class Heroe
{
    public ?Arma $arma = null;

    public function __construct(public readonly string $nombre, public int $oro, private int $ataqueBase) {}

    public function ataque(): int
    {
        return $this->ataqueBase + ($this->arma?->danio ?? 0);
    }
}

final class Tienda
{
    /** @param Arma[] $armas */
    public function __construct(private array $armas) {}

    public function catalogo(): array
    {
        $lista = $this->armas;
        usort($lista, fn(Arma $a, Arma $b) => $a->precio() <=> $b->precio());
        return $lista;
    }

    public function comprar(Heroe $h, string $nombre): string
    {
        foreach ($this->armas as $arma) {
            if ($arma->nombre !== $nombre) {
                continue;
            }
            if ($h->oro < $arma->precio()) {
                return "{$h->nombre} no puede comprar $nombre: cuesta {$arma->precio()} y tiene {$h->oro}";
            }
            $h->oro -= $arma->precio();
            $h->arma = $arma;
            return "{$h->nombre} compra $nombre: ataque {$h->ataque()}, le quedan {$h->oro} de oro";
        }
        return "No hay $nombre en la tienda";
    }
}

$tienda = new Tienda([
    new Arma('daga', 3, Rareza::Comun), new Arma('espada larga', 6, Rareza::Comun),
    new Arma('arco élfico', 7, Rareza::Raro), new Arma('martillo del volcán', 12, Rareza::Epico),
]);
foreach ($tienda->catalogo() as $a) {
    echo "{$a->rareza->simbolo()} {$a->nombre} (+{$a->danio}): {$a->precio()} de oro\n";
}
$kira = new Heroe('Kira', 3000, 8);
echo $tienda->comprar($kira, 'martillo del volcán'), "\n";
echo $tienda->comprar($kira, 'arco élfico'), "\n";
echo $tienda->comprar($kira, 'espada larga'), "\n";
```

### Prueba del sello

#### ¿Por qué la vida del personaje es privada?

Para que solo cambie con `recibirDanio` y `curar`, que respetan los límites (nunca menos de 0 ni más que el máximo).

#### ¿Por qué el azar entra por una interfaz `Dados`?

Para poder cambiar los dados de verdad por unos trucados en las pruebas y repetir exactamente un combate.

#### ¿Qué pasa si llamás a `mt_srand(2026)` y después tirás varias veces?

Salen siempre los mismos números en el mismo orden: la semilla fija la secuencia.

#### ¿Qué ventaja tiene que los tipos de enemigo sean un enum?

Cada tipo lleva sus valores (vida, ataque) en un solo lugar, y no puede haber un tipo mal escrito.

#### ¿Qué hace `?->` en `$this->arma?->danio`?

Si `$this->arma` es `null`, devuelve `null` en lugar de dar error (el operador *nullsafe*).

### Soluciones (docente)

Sale de `21-PHP/21-RPG-Modelo`, reorganizado: el azar se inyecta con la interfaz `Dados` (semilla o trucados) para poder probar el juego, y la vida es privada. Las salidas dependen de `mt_srand`/`mt_rand`, que dan la misma secuencia en cualquier PHP 7.1 o más nuevo.

## S01-N02 · El motor de combate

```meta
tipo: tema
padre: S01-N01
precio: 10
criatura: goblin
ejecutable: no
temas: diseno.patrones
usa: juegos.turnos
```

### Crónica

En el centro de la Arena hay un reloj de arena gigante: cada vez que cae, le toca a otro luchador. Un juez anota cada golpe en un pergamino que después se lee en voz alta para todo el público. Los goblins pelean a lo loco, los orcos siempre van contra el más débil, y el dragón… el dragón espera el momento justo.

—Un combate es una **máquina de turnos** —dice {mentor}—: quién ataca, a quién, con qué, y cuándo termina. Y cada enemigo piensa distinto, {heroe}. Si escribís esa forma de pensar como una **estrategia** intercambiable, agregar un monstruo nuevo es escribir una clase, no tocar el motor.

### Objetivos

- Escribir un motor de combate por turnos con un bucle y una condición de fin.
- Separar la forma de pensar de cada enemigo con el patrón estrategia (una interfaz).
- Registrar el combate en una bitácora y resumirlo al final.
- Devolver el resultado como un enum.
- Probar un combate completo con dados trucados.

### Antes de empezar

- El modelo de la Arena (S01-N01) e interfaces y composición (R02-N06, R02-N07).

### Explicación

#### El bucle del combate
```php
while ($heroe->estaVivo() && $this->quedanEnemigos() && $turno <= self::MAX_TURNOS) {
    $this->turnoDelHeroe($turno);
    foreach ($this->enemigosVivos() as $enemigo) {
        $this->turnoDelEnemigo($enemigo);
    }
    $turno++;
}
```
Tres formas de terminar: el héroe cae, caen todos los enemigos o se llega al límite
de turnos (para que un combate imposible no quede girando para siempre).

#### Cada enemigo piensa distinto: estrategias
```php
interface Estrategia
{
    /** Decide qué hace el enemigo este turno. */
    public function decidir(Enemigo $yo, Heroe $heroe, Dados $dados): Accion;
}
```
- `Atolondrada` (goblin): ataca siempre.
- `Prudente` (orco): si le queda menos del 30% de vida, se cura una vez.
- `Paciente` (dragón): carga fuego un turno y al siguiente ataca con el triple.

El motor no sabe **cómo** piensa cada uno: le pregunta a su estrategia. Agregar un
enemigo nuevo es escribir una clase que implemente `Estrategia`.

#### La bitácora
Cada acción se agrega a un array de textos: se muestra al final o de a poco. Separar
"lo que pasó" de "cómo se muestra" deja usar el mismo motor en la terminal o en una
página web.

#### El resultado
```php
enum Resultado: string
{
    case Victoria = 'victoria';
    case Derrota = 'derrota';
    case Empate = 'empate';          // se llegó al límite de turnos
}
```

### Código de ejemplo

```php
<?php
declare(strict_types=1);
/*
 * El reloj de arena de la Arena: un motor de combate con estrategias.
 */
interface Dados
{
    public function tirar(int $caras): int;
}

final class DadosConSemilla implements Dados
{
    public function __construct(int $semilla)
    {
        mt_srand($semilla);
    }

    public function tirar(int $caras): int
    {
        return mt_rand(1, $caras);
    }
}

abstract class Personaje
{
    private int $vida;

    public function __construct(public readonly string $nombre, private int $vidaMaxima, public readonly int $ataque)
    {
        $this->vida = $vidaMaxima;
    }

    public function recibirDanio(int $n): int
    {
        $antes = $this->vida;
        $this->vida = max(0, $this->vida - $n);
        return $antes - $this->vida;
    }

    public function curar(int $n): int
    {
        $antes = $this->vida;
        $this->vida = min($this->vidaMaxima, $this->vida + $n);
        return $this->vida - $antes;
    }

    public function vida(): int { return $this->vida; }

    public function porcentaje(): float { return $this->vida / $this->vidaMaxima; }

    public function estaVivo(): bool { return $this->vida > 0; }
}

final class Heroe extends Personaje
{
    public int $pociones = 2;
}

enum TipoAccion
{
    case Atacar;
    case Curarse;
    case Cargar;
}

readonly class Accion
{
    public function __construct(public TipoAccion $tipo, public int $potencia = 0) {}
}

interface Estrategia
{
    public function decidir(Enemigo $yo, Heroe $heroe, Dados $dados): Accion;
}

final class Atolondrada implements Estrategia
{
    public function decidir(Enemigo $yo, Heroe $heroe, Dados $dados): Accion
    {
        return new Accion(TipoAccion::Atacar, $yo->ataque + $dados->tirar(4));
    }
}

final class Prudente implements Estrategia
{
    private bool $yaSeCuro = false;

    public function decidir(Enemigo $yo, Heroe $heroe, Dados $dados): Accion
    {
        if (!$this->yaSeCuro && $yo->porcentaje() < 0.3) {
            $this->yaSeCuro = true;
            return new Accion(TipoAccion::Curarse, 15);
        }
        return new Accion(TipoAccion::Atacar, $yo->ataque + $dados->tirar(6));
    }
}

final class Paciente implements Estrategia
{
    private bool $cargado = false;

    public function decidir(Enemigo $yo, Heroe $heroe, Dados $dados): Accion
    {
        if (!$this->cargado) {
            $this->cargado = true;
            return new Accion(TipoAccion::Cargar);
        }
        $this->cargado = false;
        return new Accion(TipoAccion::Atacar, $yo->ataque * 3);
    }
}

final class Enemigo extends Personaje
{
    public function __construct(string $nombre, int $vida, int $ataque, public readonly Estrategia $estrategia)
    {
        parent::__construct($nombre, $vida, $ataque);
    }
}

enum Resultado: string
{
    case Victoria = 'victoria';
    case Derrota = 'derrota';
    case Empate = 'empate';
}

final class Combate
{
    public const MAX_TURNOS = 30;
    private array $bitacora = [];

    /** @param Enemigo[] $enemigos */
    public function __construct(private Heroe $heroe, private array $enemigos, private Dados $dados) {}

    public function pelear(): Resultado
    {
        for ($turno = 1; $turno <= self::MAX_TURNOS; $turno++) {
            $vivos = array_values(array_filter($this->enemigos, fn(Enemigo $e) => $e->estaVivo()));
            if ($vivos === []) {
                return Resultado::Victoria;
            }
            $this->turnoDelHeroe($turno, $vivos);
            foreach ($vivos as $enemigo) {
                if ($enemigo->estaVivo() && $this->heroe->estaVivo()) {
                    $this->turnoDelEnemigo($enemigo);
                }
            }
            if (!$this->heroe->estaVivo()) {
                return Resultado::Derrota;
            }
        }
        return Resultado::Empate;
    }

    private function turnoDelHeroe(int $turno, array $vivos): void
    {
        if ($this->heroe->porcentaje() < 0.35 && $this->heroe->pociones > 0) {
            $this->heroe->pociones--;
            $this->bitacora[] = "T$turno {$this->heroe->nombre} toma una poción (+" . $this->heroe->curar(25) . ')';
            return;
        }
        usort($vivos, fn(Enemigo $a, Enemigo $b) => $a->vida() <=> $b->vida());   // ataca al más débil
        $objetivo = $vivos[0];
        $danio = $objetivo->recibirDanio($this->heroe->ataque + $this->dados->tirar(6));
        $this->bitacora[] = "T$turno {$this->heroe->nombre} golpea a {$objetivo->nombre}: $danio" . ($objetivo->estaVivo() ? " (le quedan {$objetivo->vida()})" : ' ¡y lo derrota!');
    }

    private function turnoDelEnemigo(Enemigo $e): void
    {
        $accion = $e->estrategia->decidir($e, $this->heroe, $this->dados);
        $this->bitacora[] = match ($accion->tipo) {
            TipoAccion::Atacar => "   {$e->nombre} ataca: " . $this->heroe->recibirDanio($accion->potencia) . " (a {$this->heroe->nombre} le quedan {$this->heroe->vida()})",
            TipoAccion::Curarse => "   {$e->nombre} se cura " . $e->curar($accion->potencia),
            TipoAccion::Cargar => "   {$e->nombre} respira hondo y junta fuego…",
        };
    }

    public function bitacora(): array
    {
        return $this->bitacora;
    }
}

$heroe = new Heroe('Kira', 90, 11);
$enemigos = [
    new Enemigo('Goblin', 18, 4, new Atolondrada()),
    new Enemigo('Orco', 40, 7, new Prudente()),
    new Enemigo('Dragón joven', 55, 6, new Paciente()),
];
$combate = new Combate($heroe, $enemigos, new DadosConSemilla(7));
$resultado = $combate->pelear();
echo implode("\n", $combate->bitacora()), "\n";
echo "Resultado: {$resultado->value} en ", count(array_filter($combate->bitacora(), fn($l) => str_starts_with($l, 'T'))), " turnos\n";
```

### Salida esperada

```
T1 Kira golpea a Goblin: 15 (le quedan 3)
   Goblin ataca: 5 (a Kira le quedan 85)
   Orco ataca: 9 (a Kira le quedan 76)
   Dragón joven respira hondo y junta fuego…
T2 Kira golpea a Goblin: 3 ¡y lo derrota!
   Orco ataca: 9 (a Kira le quedan 67)
   Dragón joven ataca: 18 (a Kira le quedan 49)
T3 Kira golpea a Orco: 15 (le quedan 25)
   Orco ataca: 13 (a Kira le quedan 36)
   Dragón joven respira hondo y junta fuego…
T4 Kira golpea a Orco: 17 (le quedan 8)
   Orco se cura 15
   Dragón joven ataca: 18 (a Kira le quedan 18)
T5 Kira toma una poción (+25)
   Orco ataca: 12 (a Kira le quedan 31)
   Dragón joven respira hondo y junta fuego…
T6 Kira toma una poción (+25)
   Orco ataca: 13 (a Kira le quedan 43)
   Dragón joven ataca: 18 (a Kira le quedan 25)
T7 Kira golpea a Orco: 16 (le quedan 7)
   Orco ataca: 9 (a Kira le quedan 16)
   Dragón joven respira hondo y junta fuego…
T8 Kira golpea a Orco: 7 ¡y lo derrota!
   Dragón joven ataca: 16 (a Kira le quedan 0)
Resultado: derrota en 8 turnos
```

### ¿Para qué sirve?

El patrón estrategia está en todas partes fuera de los juegos: distintas formas de calcular un envío, de cobrar (tarjeta, transferencia), de ordenar una lista, de exportar un reporte. Y un motor que produce una bitácora en lugar de imprimir es lo que permite mostrar el mismo combate en la terminal, en una página web o mandarlo por una API.

### Errores habituales

**Ogro: el bucle sin límite.** Si dos luchadores se curan más de lo que se pegan, el
combate nunca termina. Siempre un máximo de turnos (y un resultado de empate).

**Troll: modificar la lista mientras se la recorre.** Sacar enemigos muertos del array
adentro del `foreach` que lo recorre saltea elementos. Filtrá antes (o marcá y limpiá
después).

**Ogro: el `match` por tipo de enemigo en el motor.** Si el motor pregunta "¿sos un
dragón?", cada enemigo nuevo obliga a tocarlo. Esa decisión va en la estrategia.

**Troll: una estrategia compartida.** Si dos orcos comparten el **mismo** objeto
`Prudente`, cuando uno se cura el otro "ya se curó". Cada enemigo con su propia
instancia.

**Esqueleto: el muerto que ataca.** Si un enemigo muere en el turno del héroe y después
igual ataca, falta revisar `estaVivo()` antes de su turno.

### Misión S01-N02-M1 · La estrategia del chamán

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Agregá una estrategia nueva, `Chaman`, **sin tocar el motor**: el chamán cura a su
**aliado más herido** (el enemigo vivo con menor porcentaje de vida, que puede ser
él mismo) si alguno está por debajo del 50%; si no, ataca con su ataque más un d4.
Para eso la estrategia necesita conocer a sus aliados: recibilos en el constructor
de `Chaman` (un array por referencia a la lista de enemigos, o un objeto `Banda` que
la contenga). Armá un combate de Kira contra un goblin, un orco y un chamán con la
semilla 11 y mostrá la bitácora y el resultado.

#### Criterio de aprobación

- `Chaman` implementa `Estrategia` y el motor no cambia.
- Cura al aliado más herido cuando corresponde.
- La salida coincide con la esperada.

#### Salida esperada

```
T1 Kira golpea a Goblin: 16
   Goblin ataca: 8
   Chamán cura a Goblin: +12
   Orco ataca: 7
T2 Kira golpea a Goblin: 14
   Chamán lanza un rayo: 5
   Orco ataca: 10
T3 Kira golpea a Chamán: 18
   Chamán cura a Chamán: +12
   Orco ataca: 7
T4 Kira golpea a Chamán: 14
   Chamán cura a Chamán: +12
   Orco ataca: 10
T5 Kira golpea a Chamán: 14
   Orco ataca: 7
T6 Kira golpea a Orco: 18
   Orco ataca: 7
T7 Kira golpea a Orco: 13
   Orco ataca: 8
T8 Kira golpea a Orco: 4
Resultado: victoria
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - La estrategia del chamán: un enemigo nuevo sin tocar el motor.

interface Dados { public function tirar(int $caras): int; }

final class DadosConSemilla implements Dados
{
    public function __construct(int $semilla) { mt_srand($semilla); }

    public function tirar(int $caras): int { return mt_rand(1, $caras); }
}

abstract class Personaje
{
    private int $vida;

    public function __construct(public readonly string $nombre, private int $vidaMaxima, public readonly int $ataque)
    {
        $this->vida = $vidaMaxima;
    }

    public function recibirDanio(int $n): int { $a = $this->vida; $this->vida = max(0, $this->vida - $n); return $a - $this->vida; }

    public function curar(int $n): int { $a = $this->vida; $this->vida = min($this->vidaMaxima, $this->vida + $n); return $this->vida - $a; }

    public function vida(): int { return $this->vida; }

    public function porcentaje(): float { return $this->vida / $this->vidaMaxima; }

    public function estaVivo(): bool { return $this->vida > 0; }
}

final class Heroe extends Personaje {}

final class Banda
{
    /** @var Enemigo[] */
    public array $miembros = [];
}

interface Estrategia
{
    /** Devuelve lo que pasó, para la bitácora. */
    public function actuar(Enemigo $yo, Heroe $heroe, Dados $dados): string;
}

final class Atolondrada implements Estrategia
{
    public function actuar(Enemigo $yo, Heroe $heroe, Dados $dados): string
    {
        return "{$yo->nombre} ataca: " . $heroe->recibirDanio($yo->ataque + $dados->tirar(4));
    }
}

final class Chaman implements Estrategia
{
    public function __construct(private Banda $banda) {}

    public function actuar(Enemigo $yo, Heroe $heroe, Dados $dados): string
    {
        $vivos = array_filter($this->banda->miembros, fn(Enemigo $e) => $e->estaVivo());
        usort($vivos, fn(Enemigo $a, Enemigo $b) => $a->porcentaje() <=> $b->porcentaje());
        $herido = $vivos[0] ?? null;
        if ($herido !== null && $herido->porcentaje() < 0.5) {
            return "{$yo->nombre} cura a {$herido->nombre}: +" . $herido->curar(12);
        }
        return "{$yo->nombre} lanza un rayo: " . $heroe->recibirDanio($yo->ataque + $dados->tirar(4));
    }
}

final class Enemigo extends Personaje
{
    public function __construct(string $nombre, int $vida, int $ataque, public readonly Estrategia $estrategia)
    {
        parent::__construct($nombre, $vida, $ataque);
    }
}

// El motor de siempre: no sabe nada del chamán.
function pelear(Heroe $heroe, array $enemigos, Dados $dados): array
{
    $bitacora = [];
    for ($turno = 1; $turno <= 30; $turno++) {
        $vivos = array_values(array_filter($enemigos, fn(Enemigo $e) => $e->estaVivo()));
        if ($vivos === []) {
            return [$bitacora, 'victoria'];
        }
        usort($vivos, fn($a, $b) => $a->vida() <=> $b->vida());
        $bitacora[] = "T$turno {$heroe->nombre} golpea a {$vivos[0]->nombre}: " . $vivos[0]->recibirDanio($heroe->ataque + $dados->tirar(6));
        foreach ($vivos as $e) {
            if ($e->estaVivo() && $heroe->estaVivo()) {
                $bitacora[] = '   ' . $e->estrategia->actuar($e, $heroe, $dados);
            }
        }
        if (!$heroe->estaVivo()) {
            return [$bitacora, 'derrota'];
        }
    }
    return [$bitacora, 'empate'];
}

$banda = new Banda();
$banda->miembros = [new Enemigo('Goblin', 18, 4, new Atolondrada()), new Enemigo('Orco', 35, 6, new Atolondrada()), new Enemigo('Chamán', 22, 3, new Chaman($banda))];
[$bitacora, $resultado] = pelear(new Heroe('Kira', 80, 12), $banda->miembros, new DadosConSemilla(11));
echo implode("\n", $bitacora), "\nResultado: $resultado\n";
```

### Misión S01-N02-M2 · El combate trucado

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Usá el motor del ejemplo (copialo) con **dados trucados** para comprobar tres
situaciones, cada una con su propio combate y su verificación al final (mostrá `OK`
o `FALLA` según el resultado esperado):

1. Kira (vida 20, ataque 50) contra un goblin (vida 18): gana en el primer turno.
2. Kira (vida 10, ataque 1, sin pociones) contra un orco (vida 40, ataque 12): pierde.
3. Kira (vida 999, ataque 0) contra un goblin (vida 18): termina en **empate** a los 30
   turnos.

Mostrá solo el resultado y la cantidad de líneas de la bitácora de cada combate.

#### Criterio de aprobación

- Usa `DadosTrucados` para que cada combate sea predecible.
- Verifica el resultado esperado de cada caso.
- La salida coincide con la esperada.

#### Salida esperada

```
gana   victoria en 1 líneas: OK
pierde derrota en 2 líneas: OK
empata empate en 60 líneas: OK
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 2 - El combate trucado: probar el motor con resultados conocidos.

interface Dados { public function tirar(int $caras): int; }

final class DadosTrucados implements Dados
{
    private int $i = 0;

    public function __construct(private array $tiradas) {}

    public function tirar(int $caras): int { return $this->tiradas[$this->i++ % count($this->tiradas)]; }
}

abstract class Personaje
{
    private int $vida;

    public function __construct(public readonly string $nombre, private int $vidaMaxima, public readonly int $ataque) { $this->vida = $vidaMaxima; }

    public function recibirDanio(int $n): int { $a = $this->vida; $this->vida = max(0, $this->vida - $n); return $a - $this->vida; }

    public function curar(int $n): int { $a = $this->vida; $this->vida = min($this->vidaMaxima, $this->vida + $n); return $this->vida - $a; }

    public function vida(): int { return $this->vida; }

    public function porcentaje(): float { return $this->vida / $this->vidaMaxima; }

    public function estaVivo(): bool { return $this->vida > 0; }
}

final class Heroe extends Personaje { public int $pociones = 0; }

final class Enemigo extends Personaje {}

enum Resultado: string { case Victoria = 'victoria'; case Derrota = 'derrota'; case Empate = 'empate'; }

final class Combate
{
    public const MAX_TURNOS = 30;
    public array $bitacora = [];

    public function __construct(private Heroe $heroe, private array $enemigos, private Dados $dados) {}

    public function pelear(): Resultado
    {
        for ($turno = 1; $turno <= self::MAX_TURNOS; $turno++) {
            $vivos = array_values(array_filter($this->enemigos, fn(Enemigo $e) => $e->estaVivo()));
            if ($vivos === []) {
                return Resultado::Victoria;
            }
            $this->bitacora[] = "T$turno golpe: " . $vivos[0]->recibirDanio($this->heroe->ataque + $this->dados->tirar(6));
            foreach ($vivos as $e) {
                if ($e->estaVivo()) {
                    $this->bitacora[] = "  {$e->nombre}: " . $this->heroe->recibirDanio($e->ataque);
                }
            }
            if (!$this->heroe->estaVivo()) {
                return Resultado::Derrota;
            }
        }
        return Resultado::Empate;
    }
}

$casos = [
    'gana' => [new Heroe('Kira', 20, 50), [new Enemigo('Goblin', 18, 4)], Resultado::Victoria],
    'pierde' => [new Heroe('Kira', 10, 1), [new Enemigo('Orco', 40, 12)], Resultado::Derrota],
    'empata' => [new Heroe('Kira', 999, 0), [new Enemigo('Goblin', 1000, 1)], Resultado::Empate],
];
foreach ($casos as $nombre => [$heroe, $enemigos, $esperado]) {
    $combate = new Combate($heroe, $enemigos, new DadosTrucados([0]));
    $resultado = $combate->pelear();
    echo str_pad($nombre, 7), $resultado->value, ' en ', count($combate->bitacora), ' líneas: ', $resultado === $esperado ? 'OK' : 'FALLA', "\n";
}
```

### Misión S01-N02-M3 · La crónica del juez

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El juez quiere una **crónica** del combate para leer en voz alta, no una lista de
golpes. Escribí una clase `Cronista` que reciba la bitácora de un combate (en un
formato estructurado: cada entrada es un array con `turno`, `quien`, `accion`,
`objetivo` y `valor`) y produzca:

- el total de daño que hizo cada luchador;
- el golpe más fuerte (quién, a quién, en qué turno);
- cuántas veces se curó cada uno;
- un párrafo final con el resultado ("Tras 7 turnos, Kira venció a…").

Generá la bitácora estructurada con un combate con la semilla 3 (adaptá el motor para
que guarde arrays en lugar de textos) y mostrá la crónica.

#### Criterio de aprobación

- La bitácora es estructurada (arrays) y la crónica sale de procesarla.
- Calcula totales, el máximo y los conteos con funciones de arrays.
- La salida coincide con la esperada.

#### Salida esperada

```
Kira hizo 58 de daño
Orco hizo 50 de daño
Goblin hizo 6 de daño
Golpe más fuerte: Kira a Goblin, 15 en el turno 1
Curas: {"Kira":1}
Tras 6 turnos, Kira venció a Goblin y Orco (le quedaron 17 de vida).
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - La crónica del juez: procesar una bitácora estructurada.

mt_srand(3);
$heroe = ['nombre' => 'Kira', 'vida' => 48, 'ataque' => 10, 'pociones' => 1];
$enemigos = [['nombre' => 'Goblin', 'vida' => 20, 'ataque' => 5], ['nombre' => 'Orco', 'vida' => 38, 'ataque' => 8]];
$bitacora = [];
$turno = 0;
while ($heroe['vida'] > 0 && array_filter($enemigos, fn($e) => $e['vida'] > 0) && $turno < 30) {
    $turno++;
    if ($heroe['vida'] < 25 && $heroe['pociones'] > 0) {
        $heroe['pociones']--;
        $heroe['vida'] += 25;
        $bitacora[] = ['turno' => $turno, 'quien' => 'Kira', 'accion' => 'cura', 'objetivo' => 'Kira', 'valor' => 25];
    } else {
        foreach ($enemigos as $i => $e) {
            if ($e['vida'] > 0) {
                $danio = min($e['vida'], $heroe['ataque'] + mt_rand(1, 6));
                $enemigos[$i]['vida'] -= $danio;
                $bitacora[] = ['turno' => $turno, 'quien' => 'Kira', 'accion' => 'golpe', 'objetivo' => $e['nombre'], 'valor' => $danio];
                break;
            }
        }
    }
    foreach ($enemigos as $e) {
        if ($e['vida'] > 0 && $heroe['vida'] > 0) {
            $danio = min($heroe['vida'], $e['ataque'] + mt_rand(1, 4));
            $heroe['vida'] -= $danio;
            $bitacora[] = ['turno' => $turno, 'quien' => $e['nombre'], 'accion' => 'golpe', 'objetivo' => 'Kira', 'valor' => $danio];
        }
    }
}

final class Cronista
{
    public function __construct(private array $bitacora) {}

    public function danioPorLuchador(): array
    {
        $totales = [];
        foreach (array_filter($this->bitacora, fn($e) => $e['accion'] === 'golpe') as $e) {
            $totales[$e['quien']] = ($totales[$e['quien']] ?? 0) + $e['valor'];
        }
        arsort($totales);
        return $totales;
    }

    public function golpeMasFuerte(): array
    {
        $golpes = array_values(array_filter($this->bitacora, fn($e) => $e['accion'] === 'golpe'));
        usort($golpes, fn($a, $b) => $b['valor'] <=> $a['valor'] ?: $a['turno'] <=> $b['turno']);
        return $golpes[0];
    }

    public function curas(): array
    {
        return array_count_values(array_column(array_filter($this->bitacora, fn($e) => $e['accion'] === 'cura'), 'quien'));
    }
}

$cronista = new Cronista($bitacora);
foreach ($cronista->danioPorLuchador() as $quien => $total) {
    echo "$quien hizo $total de daño\n";
}
$g = $cronista->golpeMasFuerte();
echo "Golpe más fuerte: {$g['quien']} a {$g['objetivo']}, {$g['valor']} en el turno {$g['turno']}\n";
echo "Curas: ", json_encode($cronista->curas()), "\n";
$ganador = $heroe['vida'] > 0 ? 'Kira venció a ' . implode(' y ', array_column($enemigos, 'nombre')) : 'Kira cayó en la arena';
echo "Tras $turno turnos, $ganador (le quedaron {$heroe['vida']} de vida).\n";
```

### Encargo S01-N02-E1 · El torneo automático

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

La Arena organiza un **torneo**: cuatro héroes (con distintas vidas y ataques) pelean
cada uno contra la misma banda de enemigos, **cinco veces** cada uno, con semillas
distintas (1 a 5). Usá el motor (sin bitácora de textos, solo el resultado y los
turnos) y mostrá una tabla con, para cada héroe: victorias, derrotas, empates,
promedio de turnos de las victorias y el porcentaje de victorias. Ordená la tabla por
porcentaje de victorias y, a igual porcentaje, por menos turnos promedio.

#### Criterio de aprobación

- Cada combate es independiente (héroe y enemigos nuevos cada vez) y usa su semilla.
- La tabla se ordena con dos criterios.
- La salida coincide con la esperada.

#### Salida esperada

```
Nombre   V   D   E   Turnos      %
Nara     5   0   0      6.0   100%
Bron     5   0   0      7.6   100%
Tomi     3   2   0      7.7    60%
Olmo     2   3   0      7.0    40%
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - El torneo automático: muchos combates con semilla y una tabla de posiciones.

function combate(array $heroe, array $enemigos, int $semilla): array
{
    mt_srand($semilla);
    for ($turno = 1; $turno <= 30; $turno++) {
        $vivo = null;
        foreach ($enemigos as $i => $e) {
            if ($e['vida'] > 0) {
                $vivo = $i;
                break;
            }
        }
        if ($vivo === null) {
            return ['victoria', $turno - 1];
        }
        $enemigos[$vivo]['vida'] -= $heroe['ataque'] + mt_rand(1, 6);
        foreach ($enemigos as $e) {
            if ($e['vida'] > 0) {
                $heroe['vida'] -= $e['ataque'] + mt_rand(1, 4);
            }
        }
        if ($heroe['vida'] <= 0) {
            return ['derrota', $turno];
        }
    }
    return ['empate', 30];
}

$banda = [['vida' => 15, 'ataque' => 2], ['vida' => 25, 'ataque' => 3], ['vida' => 40, 'ataque' => 4]];
$heroes = [
    'Bron' => ['vida' => 110, 'ataque' => 9],
    'Nara' => ['vida' => 70, 'ataque' => 14],
    'Olmo' => ['vida' => 62, 'ataque' => 9],
    'Tomi' => ['vida' => 70, 'ataque' => 8],
];
$tabla = [];
foreach ($heroes as $nombre => $heroe) {
    $fila = ['nombre' => $nombre, 'victoria' => 0, 'derrota' => 0, 'empate' => 0, 'turnos' => []];
    foreach (range(1, 5) as $semilla) {
        [$resultado, $turnos] = combate($heroe, $banda, $semilla);
        $fila[$resultado]++;
        if ($resultado === 'victoria') {
            $fila['turnos'][] = $turnos;
        }
    }
    $fila['porcentaje'] = $fila['victoria'] * 100 / 5;
    $fila['promedio'] = $fila['turnos'] === [] ? 99 : array_sum($fila['turnos']) / count($fila['turnos']);
    $tabla[] = $fila;
}
usort($tabla, fn($a, $b) => $b['porcentaje'] <=> $a['porcentaje'] ?: $a['promedio'] <=> $b['promedio']);
printf("%-6s %3s %3s %3s %8s %6s\n", 'Nombre', 'V', 'D', 'E', 'Turnos', '%');
foreach ($tabla as $f) {
    printf("%-6s %3d %3d %3d %8s %5.0f%%\n", $f['nombre'], $f['victoria'], $f['derrota'], $f['empate'], $f['turnos'] === [] ? '-' : number_format($f['promedio'], 1), $f['porcentaje']);
}
```

### Prueba del sello

#### ¿Por qué el combate tiene un máximo de turnos?

Para que un combate imposible (nadie puede ganar) termine igual, con un empate, en lugar de girar para siempre.

#### ¿Qué es el patrón estrategia?

Separar una forma de decidir en una interfaz con varias implementaciones intercambiables: el motor le pregunta a la estrategia qué hacer, sin saber cómo decide.

#### ¿Por qué cada enemigo necesita su propia instancia de estrategia?

Porque algunas estrategias guardan estado (ya me curé, estoy cargando fuego): si dos enemigos comparten la misma, se mezclan.

#### ¿Qué ventaja tiene una bitácora estructurada (arrays) sobre una de textos?

Que se puede procesar (sumar daños, buscar el golpe más fuerte) y mostrar de distintas maneras.

#### ¿Cómo se hace predecible un combate para probarlo?

Con dados trucados o con una semilla fija.

### Soluciones (docente)

Sale de `21-PHP/22-RPG-Motor-Combate`, con el patrón estrategia agregado (el original decidía con `match` por tipo). En la misión 2, los dados trucados con `[0]` hacen que el azar no sume nada: los resultados dependen solo de la vida y el ataque.

## S01-N03 · Oleadas, experiencia y el ranking en MariaDB

```meta
tipo: tema
padre: S01-N02
precio: 10
criatura: orc
ejecutable: no
temas: juegos.guardado
usa: func.iteradores, sql.desde-codigo
```

### Crónica

Los combates sueltos ya no alcanzan: el público quiere ver hasta dónde llega cada luchador. Las puertas de la Arena se abren una y otra vez, y cada vez salen más criaturas y más fuertes. Quien sobrevive gana experiencia y sube de nivel; quien cae, queda grabado en el **tablero de honor** de la entrada, con su nombre y la oleada a la que llegó.

—Ahora tu juego necesita **memoria** —dice {mentor}—. Las oleadas se generan de a una, a medida que hacen falta, y los puntajes se guardan en la Bodega para que duren para siempre. Todo lo que aprendiste en el Puerto, {heroe}, ahora juega para vos.

### Objetivos

- Generar oleadas de enemigos con dificultad creciente usando un generador.
- Dar experiencia y subir de nivel al héroe con una regla clara.
- Guardar las partidas en MariaDB y mostrar un ranking con consultas preparadas.
- Guardar y cargar el estado de una partida en JSON.

### Antes de empezar

- El motor de combate (S01-N02), generadores (R05-N02) y repositorios con PDO (R04-N08).

### Explicación

#### Oleadas con un generador
Las oleadas son potencialmente infinitas: un generador las produce de a una:
```php
function oleadas(Dados $dados): Generator
{
    for ($n = 1; ; $n++) {
        $cantidad = min(1 + intdiv($n, 2), 5);                // más enemigos cada dos oleadas, hasta 5
        $fuerza = 1 + ($n - 1) * 0.25;                          // un 25% más fuertes cada vez
        yield $n => array_map(fn() => crearEnemigo($dados, $fuerza), range(1, $cantidad));
    }
}
foreach (oleadas($dados) as $n => $enemigos) {
    if (pelear($heroe, $enemigos) !== Resultado::Victoria) {
        break;                                                 // el héroe cayó: se termina la partida
    }
}
```

#### Experiencia y niveles
Cada enemigo derrotado da experiencia; al juntar la necesaria, el héroe sube de
nivel: más vida máxima, más ataque y se cura entero. Una curva típica: para el nivel
`n` hacen falta `50 * n²` puntos acumulados. Al subir, los extras se aplican una
sola vez (y puede subir más de un nivel de golpe).

#### El ranking en la Bodega
```sql
CREATE TABLE partida (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jugador VARCHAR(30) NOT NULL,
    oleada INT NOT NULL,
    nivel INT NOT NULL,
    puntos INT NOT NULL,
    jugada DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_partida_puntos (puntos)
);
```
```php
$top = $pdo->prepare('SELECT jugador, MAX(puntos) AS mejor, COUNT(*) AS partidas
                      FROM partida GROUP BY jugador ORDER BY mejor DESC LIMIT ?');
```
Un repositorio `Ranking` guarda la partida y arma el top, como en la Bodega.

#### Guardar la partida en JSON
Para continuar otro día, el estado (héroe, oleada, experiencia, semilla) se guarda
con `json_encode` y se carga con `json_decode`. Un objeto que implementa
`JsonSerializable` decide qué se guarda, y un método de fábrica `desdeArray()` lo
reconstruye.

### Código de ejemplo

`esquema.sql`
```sql
DROP TABLE IF EXISTS partida;
CREATE TABLE partida (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jugador VARCHAR(30) NOT NULL,
    oleada INT NOT NULL,
    nivel INT NOT NULL,
    puntos INT NOT NULL,
    jugada DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_partida_puntos (puntos)
);
INSERT INTO partida (jugador, oleada, nivel, puntos) VALUES ('Bron', 4, 3, 610), ('Olmo', 6, 4, 980), ('Bron', 5, 3, 720);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`main.php`
```php
<?php
declare(strict_types=1);
/*
 * Las puertas de la Arena: oleadas con un generador, niveles y el ranking en MariaDB.
 */
final class Heroe implements JsonSerializable
{
    public int $vida;
    public int $nivel = 1;
    public int $experiencia = 0;

    public function __construct(public readonly string $nombre, public int $vidaMaxima = 60, public int $ataque = 9)
    {
        $this->vida = $vidaMaxima;
    }

    public function ganarExperiencia(int $puntos): array
    {
        $this->experiencia += $puntos;
        $subidas = [];
        while ($this->experiencia >= 50 * $this->nivel ** 2) {
            $this->nivel++;
            $this->vidaMaxima += 12;
            $this->ataque += 3;
            $this->vida = $this->vidaMaxima;
            $subidas[] = $this->nivel;
        }
        return $subidas;
    }

    public function jsonSerialize(): array
    {
        return ['nombre' => $this->nombre, 'vida' => $this->vida, 'vidaMaxima' => $this->vidaMaxima, 'ataque' => $this->ataque, 'nivel' => $this->nivel, 'experiencia' => $this->experiencia];
    }

    public static function desdeArray(array $d): self
    {
        $h = new self($d['nombre'], $d['vidaMaxima'], $d['ataque']);
        $h->vida = $d['vida'];
        $h->nivel = $d['nivel'];
        $h->experiencia = $d['experiencia'];
        return $h;
    }
}

function oleadas(): Generator
{
    for ($n = 1; ; $n++) {
        $cantidad = min(1 + intdiv($n, 2), 5);
        $fuerza = 1 + ($n - 1) * 0.25;
        $enemigos = [];
        for ($i = 1; $i <= $cantidad; $i++) {
            $enemigos[] = ['vida' => (int) round(mt_rand(10, 20) * $fuerza), 'ataque' => (int) round(mt_rand(2, 5) * $fuerza)];
        }
        yield $n => $enemigos;
    }
}

function pelear(Heroe $h, array $enemigos): bool
{
    foreach ($enemigos as $e) {
        while ($e['vida'] > 0) {
            $e['vida'] -= $h->ataque + mt_rand(1, 6);
            if ($e['vida'] > 0) {
                $h->vida -= $e['ataque'] + mt_rand(0, 2);
                if ($h->vida <= 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

final class Ranking
{
    public function __construct(private PDO $pdo) {}

    public function guardar(string $jugador, int $oleada, int $nivel, int $puntos): void
    {
        $this->pdo->prepare('INSERT INTO partida (jugador, oleada, nivel, puntos) VALUES (?, ?, ?, ?)')->execute([$jugador, $oleada, $nivel, $puntos]);
    }

    public function top(int $cantidad): array
    {
        $s = $this->pdo->prepare('SELECT jugador, MAX(puntos) AS mejor, MAX(oleada) AS oleada, COUNT(*) AS partidas FROM partida GROUP BY jugador ORDER BY mejor DESC, jugador LIMIT ?');
        $s->bindValue(1, $cantidad, PDO::PARAM_INT);
        $s->execute();
        return $s->fetchAll();
    }
}

mt_srand(2026);
$kira = new Heroe('Kira');
$puntos = 0;
$alcanzada = 0;
foreach (oleadas() as $n => $enemigos) {
    if ($n > 10) {
        echo "¡Kira sobrevivió a las 10 oleadas!\n";   // el generador es infinito: cortamos acá
        break;
    }
    $alcanzada = $n;
    if (!pelear($kira, $enemigos)) {
        echo "Oleada $n: Kira cae ante ", count($enemigos), " enemigos\n";
        break;
    }
    $ganado = 20 * count($enemigos) * $n;
    $puntos += $ganado;
    $subidas = $kira->ganarExperiencia($ganado);
    echo "Oleada $n: ", count($enemigos), " enemigo/s vencidos, +$ganado", $subidas === [] ? '' : ' · ¡sube al nivel ' . implode(' y ', $subidas) . '!', " (vida {$kira->vida}/{$kira->vidaMaxima})\n";
}

$guardado = json_encode($kira);
echo "Partida guardada: $guardado\n";
$cargada = Heroe::desdeArray(json_decode($guardado, true));
echo "Cargada: {$cargada->nombre}, nivel {$cargada->nivel}, ataque {$cargada->ataque}\n";

$c = require __DIR__ . '/config.php';
$ranking = new Ranking(new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]));
$ranking->guardar('Kira', $alcanzada, $kira->nivel, $puntos);
echo "Tablero de honor:\n";
foreach ($ranking->top(3) as $i => $f) {
    printf("%d. %-5s %5d puntos (oleada %d, %d partida/s)\n", $i + 1, $f['jugador'], $f['mejor'], $f['oleada'], $f['partidas']);
}
```

### Salida esperada

```
Oleada 1: 1 enemigo/s vencidos, +20 (vida 56/60)
Oleada 2: 2 enemigo/s vencidos, +80 · ¡sube al nivel 2! (vida 72/72)
Oleada 3: 2 enemigo/s vencidos, +120 · ¡sube al nivel 3! (vida 84/84)
Oleada 4: 3 enemigo/s vencidos, +240 · ¡sube al nivel 4! (vida 96/96)
Oleada 5: 3 enemigo/s vencidos, +300 (vida 84/96)
Oleada 6: 4 enemigo/s vencidos, +480 · ¡sube al nivel 5! (vida 108/108)
Oleada 7: 4 enemigo/s vencidos, +560 · ¡sube al nivel 6 y 7! (vida 132/132)
Oleada 8: 5 enemigo/s vencidos, +800 · ¡sube al nivel 8! (vida 144/144)
Oleada 9: 5 enemigo/s vencidos, +900 · ¡sube al nivel 9! (vida 156/156)
Oleada 10: 5 enemigo/s vencidos, +1000 · ¡sube al nivel 10! (vida 168/168)
¡Kira sobrevivió a las 10 oleadas!
Partida guardada: {"nombre":"Kira","vida":168,"vidaMaxima":168,"ataque":36,"nivel":10,"experiencia":4500}
Cargada: Kira, nivel 10, ataque 36
Tablero de honor:
1. Kira   4500 puntos (oleada 10, 1 partida/s)
2. Olmo    980 puntos (oleada 6, 1 partida/s)
3. Bron    720 puntos (oleada 5, 2 partida/s)
```

### ¿Para qué sirve?

Los generadores sirven para todo lo que se produce de a poco y sin fin conocido: oleadas, páginas de resultados, eventos. Un ranking guardado en la base con un top armado por SQL es lo mismo que el ranking de esta plataforma, la tabla de posiciones de un torneo o los "más vendidos" de una tienda. Y guardar el estado en JSON es cómo muchas apps guardan "tu progreso".

### Errores habituales

**Ogro: el generador infinito sin `break`.** Recorrer `oleadas()` sin condición de corte
cuelga el programa. El `foreach` tiene que terminar cuando el héroe cae.

**Ogro: subir un solo nivel.** Si una oleada da experiencia para dos niveles, un `if`
sube solo uno: usá un `while`.

**Goblin: el `LIMIT` como texto.** `execute([3])` con la emulación activada da `LIMIT
'3'` y un error: `bindValue(…, PDO::PARAM_INT)` (R04-N05).

**Troll: guardar objetos enteros sin control.** `serialize($heroe)` guarda todo, y al
cargar un archivo modificado puede crear objetos inesperados. `JsonSerializable` y
`desdeArray` deciden exactamente qué se guarda y cómo se reconstruye.

**Esqueleto: las columnas del ranking.** `SELECT jugador, puntos … GROUP BY jugador`
da un puntaje cualquiera del grupo: pedí `MAX(puntos)`.

### Misión S01-N03-M1 · Las puertas de la Arena

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí el generador `oleadas(int $semilla): Generator` con estas reglas: la oleada
`n` trae `min(n, 6)` enemigos; cada quinta oleada (5, 10, 15…) es de **jefe**: un solo
enemigo con 10 veces la vida y el doble de ataque; la fuerza crece un 20% por
oleada. Cada enemigo es un array con `nombre` (`Goblin`, `Orco`, `Troll` según su
vida: menos de 20, menos de 40, o más), `vida` y `ataque`. Mostrá un resumen de las
primeras 10 oleadas (cantidad, nombres agrupados y vida total), sin pelear.

#### Criterio de aprobación

- Es un generador infinito que se corta desde afuera.
- Cada quinta oleada es de jefe.
- La salida coincide con la esperada.

#### Salida esperada

```
Oleada  1: 1 Goblin                     vida total   15
Oleada  2: 2 Goblin                     vida total   36
Oleada  3: 3 Orco                       vida total   68
Oleada  4: 1 Goblin, 3 Orco             vida total  102
Oleada  5: 1 Jefe Troll                 vida total  270
Oleada  6: 4 Orco, 2 Troll              vida total  194
Oleada  7: 5 Orco, 1 Troll              vida total  180
Oleada  8: 3 Orco, 3 Troll              vida total  225
Oleada  9: 3 Orco, 3 Troll              vida total  247
Oleada 10: 1 Jefe Troll                 vida total  420
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - Las puertas de la Arena: un generador infinito de oleadas.

function nombrePorVida(int $vida): string
{
    return match (true) {
        $vida < 20 => 'Goblin',
        $vida < 40 => 'Orco',
        default => 'Troll',
    };
}

function oleadas(int $semilla): Generator
{
    mt_srand($semilla);
    for ($n = 1; ; $n++) {
        $fuerza = 1 + ($n - 1) * 0.2;
        if ($n % 5 === 0) {
            $vida = (int) round(15 * 10 * $fuerza);
            yield $n => [['nombre' => 'Jefe ' . nombrePorVida($vida), 'vida' => $vida, 'ataque' => (int) round(8 * $fuerza)]];
            continue;
        }
        $enemigos = [];
        for ($i = 0; $i < min($n, 6); $i++) {
            $vida = (int) round(mt_rand(10, 22) * $fuerza);
            $enemigos[] = ['nombre' => nombrePorVida($vida), 'vida' => $vida, 'ataque' => (int) round(mt_rand(2, 5) * $fuerza)];
        }
        yield $n => $enemigos;
    }
}

foreach (oleadas(42) as $n => $enemigos) {
    if ($n > 10) {
        break;
    }
    $nombres = array_count_values(array_column($enemigos, 'nombre'));
    ksort($nombres);
    $texto = implode(', ', array_map(fn($nombre, $cant) => "$cant $nombre", array_keys($nombres), $nombres));
    printf("Oleada %2d: %-28s vida total %4d\n", $n, $texto, array_sum(array_column($enemigos, 'vida')));
}
```

### Misión S01-N03-M2 · El tablero de honor

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Escribí el repositorio `TableroDeHonor` con PDO para la tabla `partida` del ejemplo,
con estos métodos (todos con consultas preparadas):

- `registrar(string $jugador, int $oleada, int $puntos, string $clase)`;
- `top(int $n)`: los mejores puntajes **por jugador** (el máximo de cada uno);
- `mejorPorClase()`: el mejor jugador de cada clase (`guerrero`, `maga`, `arquero`)
  con su puntaje (una subconsulta o un `JOIN` contra el máximo por clase);
- `posicion(string $jugador): ?int`: en qué puesto del top está un jugador (contando
  cuántos jugadores tienen un máximo mayor que el suyo, más uno).

Cargá las partidas del esquema, registrá dos nuevas y mostrá el top 5, los mejores
por clase y la posición de dos jugadores (uno que no existe).

#### Criterio de aprobación

- Todo el SQL está en el repositorio, con parámetros.
- El top agrupa por jugador y el mejor por clase se resuelve en SQL.
- La salida coincide con la esperada.

#### Salida esperada

```
Top 5:
  1. Kira: 1150
  2. Lía: 980
  3. Tomi: 910
  4. Nara: 880
  5. Bron: 720
Mejores por clase:
  guerrero: Bron (720)
  maga: Lía (980)
  arquero: Kira (1150)
Olmo: puesto 6
Zoe: nunca jugó
```

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS partida;
CREATE TABLE partida (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jugador VARCHAR(30) NOT NULL,
    clase ENUM('guerrero', 'maga', 'arquero') NOT NULL,
    oleada INT NOT NULL,
    puntos INT NOT NULL,
    INDEX idx_partida_puntos (puntos)
);
INSERT INTO partida (jugador, clase, oleada, puntos) VALUES
    ('Bron', 'guerrero', 4, 610), ('Lía', 'maga', 6, 980), ('Bron', 'guerrero', 5, 720),
    ('Olmo', 'arquero', 3, 450), ('Nara', 'maga', 5, 880), ('Tomi', 'arquero', 6, 910);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`main.php`
```php
<?php
declare(strict_types=1);
// Mision 2 - El tablero de honor: un ranking con SQL.

final class TableroDeHonor
{
    public function __construct(private PDO $pdo) {}

    public function registrar(string $jugador, int $oleada, int $puntos, string $clase): void
    {
        $this->pdo->prepare('INSERT INTO partida (jugador, clase, oleada, puntos) VALUES (?, ?, ?, ?)')->execute([$jugador, $clase, $oleada, $puntos]);
    }

    public function top(int $n): array
    {
        $s = $this->pdo->prepare('SELECT jugador, MAX(puntos) AS mejor FROM partida GROUP BY jugador ORDER BY mejor DESC, jugador LIMIT ?');
        $s->bindValue(1, $n, PDO::PARAM_INT);
        $s->execute();
        return $s->fetchAll();
    }

    public function mejorPorClase(): array
    {
        return $this->pdo->query(
            'SELECT p.clase, p.jugador, p.puntos FROM partida p
             JOIN (SELECT clase, MAX(puntos) AS maximo FROM partida GROUP BY clase) m ON m.clase = p.clase AND m.maximo = p.puntos
             ORDER BY p.clase'
        )->fetchAll();
    }

    public function posicion(string $jugador): ?int
    {
        $s = $this->pdo->prepare('SELECT MAX(puntos) FROM partida WHERE jugador = ?');
        $s->execute([$jugador]);
        $suyo = $s->fetchColumn();
        if ($suyo === null) {
            return null;
        }
        $s = $this->pdo->prepare('SELECT COUNT(*) FROM (SELECT jugador FROM partida GROUP BY jugador HAVING MAX(puntos) > ?) mejores');
        $s->execute([$suyo]);
        return (int) $s->fetchColumn() + 1;
    }
}

$c = require __DIR__ . '/config.php';
$tablero = new TableroDeHonor(new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]));
$tablero->registrar('Kira', 7, 1150, 'arquero');
$tablero->registrar('Olmo', 5, 700, 'arquero');

echo "Top 5:\n";
foreach ($tablero->top(5) as $i => $f) {
    echo "  ", $i + 1, ". {$f['jugador']}: {$f['mejor']}\n";
}
echo "Mejores por clase:\n";
foreach ($tablero->mejorPorClase() as $f) {
    echo "  {$f['clase']}: {$f['jugador']} ({$f['puntos']})\n";
}
foreach (['Olmo', 'Zoe'] as $jugador) {
    $p = $tablero->posicion($jugador);
    echo "$jugador: ", $p === null ? 'nunca jugó' : "puesto $p", "\n";
}
```

### Misión S01-N03-M3 · Continuar la partida

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí la clase `Partida` (héroe con nombre, clase, vida, nivel y experiencia;
número de oleada; semilla; y la mochila como `objeto => cantidad`) que implementa
`JsonSerializable` y tiene `Partida::desdeJson(string $json): self`, que **valida**
lo que carga: si falta un campo o un valor no tiene sentido (vida negativa, nivel
menor que 1, clase desconocida), lanza `UnexpectedValueException` con el motivo.

Mostrá: una partida guardada como JSON (con `JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE`),
que al cargarla de nuevo queda igual (compará los dos JSON), y el error de tres
archivos "tramposos": uno con nivel 0, uno con la clase `dios` y uno sin la oleada.

#### Criterio de aprobación

- Implementa `JsonSerializable` y un método de fábrica que valida.
- Guardar y cargar da el mismo JSON.
- La salida coincide con la esperada.

#### Salida esperada

```
{
    "heroe": {
        "nombre": "Kira",
        "clase": "arquero",
        "vida": 47,
        "nivel": 3,
        "experiencia": 610
    },
    "oleada": 5,
    "semilla": 2026,
    "mochila": {
        "poción": 2,
        "flecha de fuego": 6
    }
}
¿Queda igual al cargarla? sí
nivel cero: rechazado (Valores imposibles en la partida)
clase dios: rechazado (Clase desconocida: dios)
sin oleada: rechazado (Falta el campo oleada)
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - Continuar la partida: guardar en JSON y cargar validando.

final class Partida implements JsonSerializable
{
    public const CLASES = ['guerrero', 'maga', 'arquero'];

    public function __construct(
        public readonly string $nombre,
        public readonly string $clase,
        public readonly int $vida,
        public readonly int $nivel,
        public readonly int $experiencia,
        public readonly int $oleada,
        public readonly int $semilla,
        public readonly array $mochila,
    ) {
        if (!in_array($clase, self::CLASES, true)) {
            throw new UnexpectedValueException("Clase desconocida: $clase");
        }
        if ($vida < 0 || $nivel < 1 || $oleada < 1 || $experiencia < 0) {
            throw new UnexpectedValueException('Valores imposibles en la partida');
        }
    }

    public function jsonSerialize(): array
    {
        return ['heroe' => ['nombre' => $this->nombre, 'clase' => $this->clase, 'vida' => $this->vida, 'nivel' => $this->nivel, 'experiencia' => $this->experiencia],
            'oleada' => $this->oleada, 'semilla' => $this->semilla, 'mochila' => $this->mochila];
    }

    public static function desdeJson(string $json): self
    {
        try {
            $d = json_decode($json, true, flags: JSON_THROW_ON_ERROR);
        } catch (JsonException) {
            throw new UnexpectedValueException('El archivo no es un JSON válido');
        }
        foreach (['heroe', 'oleada', 'semilla', 'mochila'] as $campo) {
            if (!array_key_exists($campo, $d)) {
                throw new UnexpectedValueException("Falta el campo $campo");
            }
        }
        $h = $d['heroe'];
        return new self($h['nombre'], $h['clase'], $h['vida'], $h['nivel'], $h['experiencia'], $d['oleada'], $d['semilla'], $d['mochila']);
    }
}

$partida = new Partida('Kira', 'arquero', 47, 3, 610, 5, 2026, ['poción' => 2, 'flecha de fuego' => 6]);
$json = json_encode($partida, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
echo $json, "\n";
$otra = json_encode(Partida::desdeJson($json), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
echo "¿Queda igual al cargarla? ", $otra === $json ? 'sí' : 'no', "\n";

$tramposos = [
    'nivel cero' => str_replace('"nivel": 3', '"nivel": 0', $json),
    'clase dios' => str_replace('"arquero"', '"dios"', $json),
    'sin oleada' => json_encode(array_diff_key($partida->jsonSerialize(), ['oleada' => 0])),
];
foreach ($tramposos as $nombre => $contenido) {
    try {
        Partida::desdeJson($contenido);
        echo "$nombre: se cargó (¡no debería!)\n";
    } catch (UnexpectedValueException $e) {
        echo "$nombre: rechazado ({$e->getMessage()})\n";
    }
}
```

### Encargo S01-N03-E1 · Los logros del luchador

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Los juegos premian con **logros**. Leé de la entrada estándar el historial de
partidas de un jugador (`oleada;puntos;clase;pociones_usadas;minutos`, una por
renglón) y calculá qué logros desbloqueó. Cada logro es un objeto que implementa la
interfaz `Logro` (`nombre(): string` y `cumplido(array $partidas): bool`):

- **Primera sangre**: jugó al menos una partida;
- **Sobreviviente**: llegó a la oleada 10 alguna vez;
- **Sin ayuda**: ganó 500 puntos o más en una partida sin usar pociones;
- **Versátil**: jugó con las tres clases;
- **Maratón**: sumó más de 120 minutos en total;
- **Constante**: sus últimas tres partidas mejoraron cada una a la anterior.

Mostrá cada logro con `[x]` o `[ ]` y el porcentaje desbloqueado.

#### Criterio de aprobación

- Cada logro es una clase que implementa la interfaz.
- Agregar un logro no cambia el programa principal.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
3;420;guerrero;2;18
6;780;maga;1;35
10;1250;arquero;3;52
5;610;maga;0;25
7;890;guerrero;1;30
```

#### Salida esperada

```
[x] Primera sangre
[x] Sobreviviente
[x] Sin ayuda
[x] Versátil
[x] Maratón
[ ] Constante
Desbloqueaste 5 de 6 (83%)
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - Los logros del luchador: una interfaz y muchas reglas.

interface Logro
{
    public function nombre(): string;

    public function cumplido(array $partidas): bool;
}

final class PrimeraSangre implements Logro
{
    public function nombre(): string { return 'Primera sangre'; }

    public function cumplido(array $p): bool { return $p !== []; }
}

final class Sobreviviente implements Logro
{
    public function nombre(): string { return 'Sobreviviente'; }

    public function cumplido(array $p): bool { return max(array_column($p, 'oleada') ?: [0]) >= 10; }
}

final class SinAyuda implements Logro
{
    public function nombre(): string { return 'Sin ayuda'; }

    public function cumplido(array $p): bool
    {
        return array_filter($p, fn($x) => $x['pociones'] === 0 && $x['puntos'] >= 500) !== [];
    }
}

final class Versatil implements Logro
{
    public function nombre(): string { return 'Versátil'; }

    public function cumplido(array $p): bool { return count(array_unique(array_column($p, 'clase'))) === 3; }
}

final class Maraton implements Logro
{
    public function nombre(): string { return 'Maratón'; }

    public function cumplido(array $p): bool { return array_sum(array_column($p, 'minutos')) > 120; }
}

final class Constante implements Logro
{
    public function nombre(): string { return 'Constante'; }

    public function cumplido(array $p): bool
    {
        $ultimas = array_column(array_slice($p, -3), 'puntos');
        return count($ultimas) === 3 && $ultimas[0] < $ultimas[1] && $ultimas[1] < $ultimas[2];
    }
}

$partidas = [];
while (($linea = fgets(STDIN)) !== false) {
    if (trim($linea) === '') {
        continue;
    }
    [$oleada, $puntos, $clase, $pociones, $minutos] = explode(';', trim($linea));
    $partidas[] = ['oleada' => (int) $oleada, 'puntos' => (int) $puntos, 'clase' => $clase, 'pociones' => (int) $pociones, 'minutos' => (int) $minutos];
}

$logros = [new PrimeraSangre(), new Sobreviviente(), new SinAyuda(), new Versatil(), new Maraton(), new Constante()];
$cumplidos = 0;
foreach ($logros as $logro) {
    $ok = $logro->cumplido($partidas);
    $cumplidos += (int) $ok;
    echo $ok ? '[x] ' : '[ ] ', $logro->nombre(), "\n";
}
printf("Desbloqueaste %d de %d (%.0f%%)\n", $cumplidos, count($logros), $cumplidos * 100 / count($logros));
```

#### Pruebas

##### Una partida
```entrada
1;100;maga;1;10
```
```salida
[x] Primera sangre
[ ] Sobreviviente
[ ] Sin ayuda
[ ] Versátil
[ ] Maratón
[ ] Constante
Desbloqueaste 1 de 6 (17%)
```

##### Constante
```entrada
2;100;guerrero;0;50
3;200;maga;0;50
4;300;arquero;0;50
```
```salida
[x] Primera sangre
[ ] Sobreviviente
[ ] Sin ayuda
[x] Versátil
[x] Maratón
[x] Constante
Desbloqueaste 4 de 6 (67%)
```

##### Sin partidas
```entrada
```
```salida
[ ] Primera sangre
[ ] Sobreviviente
[ ] Sin ayuda
[ ] Versátil
[ ] Maratón
[ ] Constante
Desbloqueaste 0 de 6 (0%)
```

### Prueba del sello

#### ¿Por qué las oleadas se producen con un generador?

Porque son potencialmente infinitas: el generador crea cada oleada recién cuando hace falta, y el juego corta cuando el héroe cae.

#### ¿Por qué se usa `while` y no `if` para subir de nivel?

Porque una oleada puede dar experiencia para más de un nivel: el `while` sube todos los que correspondan.

#### ¿Cómo se arma un ranking con el mejor puntaje de cada jugador?

Con `GROUP BY jugador` y `MAX(puntos)`, ordenado de mayor a menor.

#### ¿Para qué sirve `JsonSerializable` al guardar una partida?

Para decidir exactamente qué datos del objeto se guardan en el JSON.

#### ¿Por qué hay que validar una partida al cargarla?

Porque el archivo pudo modificarse (o romperse): sin validar, el juego podría arrancar con valores imposibles.

### Soluciones (docente)

Sale de `21-PHP/23-RPG-Proyecto` (oleadas y guardado de puntajes), llevado a MariaDB. Las salidas dependen de `mt_srand`, que es repetible. En la misión 3, la validación está en el constructor, así que ni siquiera el programa puede crear una partida imposible.

## S01-N04 · Jefe de la Arena: el Campeón Eterno

```meta
tipo: jefe
padre: S01-N03
precio: 10
criatura: dragon
insignia: Campeón de la Arena
insignia_descripcion: Venciste al Campeón Eterno: programaste un RPG por turnos completo en PHP.
ejecutable: no
usa: juegos.turnos, cal.build, sql.desde-codigo
```

### Crónica

En el palco más alto de la Arena, envuelto en una capa gastada, espera el **Campeón Eterno**: nadie lo venció en cien años. Dicen que no es una persona sino un juego perfecto, hecho por una programadora que ya no está, que aprende de cada luchador. Para enfrentarlo hay que presentar **tu propio juego**, entero, jugable, y ganarle con él.

—Todo lo de la Arena, junto —dice {mentor}—: el modelo, el motor, las oleadas, el ranking, guardar y continuar. Y esta vez, {heroe}, lo juega una persona: el juego lee lo que escribe y le responde.

### Objetivos

- Integrar el modelo, el motor, las oleadas y el ranking en un juego completo.
- Leer las órdenes del jugador desde la terminal y responder a cada una.
- Organizar el proyecto con Composer, namespaces y MariaDB.

### Antes de empezar

- Toda la Senda de la Arena (S01-N01 a S01-N03).

### Explicación

#### Un juego que se juega
Hasta ahora el héroe peleaba solo. Ahora cada turno del héroe lo decide el
**jugador**, escribiendo una orden:
```
Turno 3 · Kira [#######...] 42/60 · Orco [###.......] 14/45
> atacar
```
El programa lee con `fgets(STDIN)` (como en R01-N04), interpreta la orden, la
ejecuta y muestra qué pasó. Las órdenes inválidas no gastan el turno.

Probar un juego interactivo a mano es lento: se guardan las órdenes en un archivo y
se redirige (`php juego.php < partida.txt`), con una semilla fija para que salga
siempre igual. Así se prueban las misiones.

### Misión S01-N04-M1 · El duelo con el Campeón

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Escribí el **duelo** entre el jugador y el Campeón Eterno (vida 100, ataque 7), en un
solo archivo con `strict_types`. El héroe (vida 90, ataque 10, 2 pociones, 1 bomba)
recibe una orden por turno desde la entrada:

- `atacar` — daño: ataque + d6;
- `defender` — este turno recibe la mitad del daño (redondeado para abajo);
- `pocion` — cura 30 (si le quedan; si no, `No te quedan pociones` y no gasta el turno);
- `bomba` — 35 de daño fijo (una sola vez);
- `estado` — muestra la vida y lo que le queda, sin gastar el turno;
- cualquier otra cosa — `Orden desconocida` y no gasta el turno.

El Campeón **aprende**: si el jugador atacó los dos turnos anteriores, defiende (y
recibe la mitad); si le queda menos de un cuarto de la vida, ataca con el doble. Usá
`mt_srand(7)` y `mt_rand` para los dados. El duelo termina cuando alguien cae o se
termina la entrada, y muestra el resultado.

#### Criterio de aprobación

- Lee las órdenes de la entrada y las inválidas no gastan el turno.
- El Campeón decide según lo que hizo el jugador y su vida.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
atacar
defender
estado
atacar
bomba
volar
pocion
defender
atacar
pocion
atacar
atacar
```

#### Salida esperada

```
Turno 1 · Kira [##########] 90/90 · Campeón [##########] 100/100
> atacar
  Kira ataca: 14
  El Campeón golpea: 12
Turno 2 · Kira [#########.] 78/90 · Campeón [#########.] 86/100
> defender
  Kira levanta el escudo
  El Campeón golpea: 4
Turno 3 · Kira [########..] 74/90 · Campeón [#########.] 86/100
> estado
  Pociones: 2 · bombas: 1
Turno 3 · Kira [########..] 74/90 · Campeón [#########.] 86/100
> atacar
  Kira ataca: 13
  El Campeón golpea: 9
Turno 4 · Kira [#######...] 65/90 · Campeón [#######...] 73/100
> bomba
  ¡Kira tira la bomba! 35 de daño
  El Campeón golpea: 11
Turno 5 · Kira [######....] 54/90 · Campeón [####......] 38/100
> volar
  Orden desconocida
Turno 5 · Kira [######....] 54/90 · Campeón [####......] 38/100
> pocion
  Kira toma una poción: +30
  El Campeón golpea: 13
Turno 6 · Kira [########..] 71/90 · Campeón [####......] 38/100
> defender
  Kira levanta el escudo
  El Campeón golpea: 6
Turno 7 · Kira [#######...] 65/90 · Campeón [####......] 38/100
> atacar
  Kira ataca: 15
  El Campeón golpea: 26
Turno 8 · Kira [####......] 39/90 · Campeón [##........] 23/100
> pocion
  Kira toma una poción: +30
  El Campeón golpea: 24
Turno 9 · Kira [#####.....] 45/90 · Campeón [##........] 23/100
> atacar
  Kira ataca: 12
  El Campeón golpea: 20
Turno 10 · Kira [###.......] 25/90 · Campeón [#.........] 11/100
> atacar
  Kira ataca: 14
¡Kira venció al Campeón Eterno en 10 turnos!
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Jefe de la Arena - El duelo con el Campeón: un juego que lee las órdenes del jugador.

mt_srand(7);
$heroe = ['vida' => 90, 'max' => 90, 'ataque' => 10, 'pociones' => 2, 'bombas' => 1];
$campeon = ['vida' => 100, 'max' => 100, 'ataque' => 7];
$historial = [];
$turno = 1;

function barra(int $vida, int $max): string
{
    $llenos = (int) round(max(0, $vida) / $max * 10);
    return '[' . str_repeat('#', $llenos) . str_repeat('.', 10 - $llenos) . '] ' . max(0, $vida) . "/$max";
}

while ($heroe['vida'] > 0 && $campeon['vida'] > 0 && ($linea = fgets(STDIN)) !== false) {
    $orden = strtolower(trim($linea));
    echo "Turno $turno · Kira ", barra($heroe['vida'], $heroe['max']), " · Campeón ", barra($campeon['vida'], $campeon['max']), "\n> $orden\n";

    $defiendeHeroe = false;
    $campeonDefiende = count($historial) >= 2 && array_slice($historial, -2) === ['atacar', 'atacar'];
    switch ($orden) {
        case 'atacar':
            $danio = $heroe['ataque'] + mt_rand(1, 6);
            if ($campeonDefiende) {
                $danio = intdiv($danio, 2);
            }
            $campeon['vida'] -= $danio;
            echo "  Kira ataca: $danio", $campeonDefiende ? ' (el Campeón se defendió)' : '', "\n";
            break;
        case 'defender':
            $defiendeHeroe = true;
            echo "  Kira levanta el escudo\n";
            break;
        case 'pocion':
            if ($heroe['pociones'] === 0) {
                echo "  No te quedan pociones\n";
                continue 2;
            }
            $heroe['pociones']--;
            $antes = $heroe['vida'];
            $heroe['vida'] = min($heroe['max'], $heroe['vida'] + 30);
            echo "  Kira toma una poción: +", $heroe['vida'] - $antes, "\n";
            break;
        case 'bomba':
            if ($heroe['bombas'] === 0) {
                echo "  No te quedan bombas\n";
                continue 2;
            }
            $heroe['bombas']--;
            $campeon['vida'] -= 35;
            echo "  ¡Kira tira la bomba! 35 de daño\n";
            break;
        case 'estado':
            echo "  Pociones: {$heroe['pociones']} · bombas: {$heroe['bombas']}\n";
            continue 2;
        default:
            echo "  Orden desconocida\n";
            continue 2;
    }
    $historial[] = $orden;

    if ($campeon['vida'] > 0) {
        $danio = $campeon['ataque'] + mt_rand(1, 6);
        if ($campeon['vida'] < $campeon['max'] / 4) {
            $danio *= 2;
        }
        if ($defiendeHeroe) {
            $danio = intdiv($danio, 2);
        }
        $heroe['vida'] -= $danio;
        echo "  El Campeón golpea: $danio\n";
    }
    $turno++;
}

if ($campeon['vida'] <= 0) {
    echo "¡Kira venció al Campeón Eterno en " . count($historial) . " turnos!\n";
} elseif ($heroe['vida'] <= 0) {
    echo "Kira cayó. El Campeón sigue invicto.\n";
} else {
    echo "Se terminaron las órdenes: el duelo queda pendiente.\n";
}
```

#### Pruebas

##### Bomba y pociones
```entrada
bomba
bomba
pocion
pocion
pocion
```
```salida
Turno 1 · Kira [##########] 90/90 · Campeón [##########] 100/100
> bomba
  ¡Kira tira la bomba! 35 de daño
  El Campeón golpea: 11
Turno 2 · Kira [#########.] 79/90 · Campeón [#######...] 65/100
> bomba
  No te quedan bombas
Turno 2 · Kira [#########.] 79/90 · Campeón [#######...] 65/100
> pocion
  Kira toma una poción: +11
  El Campeón golpea: 12
Turno 3 · Kira [#########.] 78/90 · Campeón [#######...] 65/100
> pocion
  Kira toma una poción: +12
  El Campeón golpea: 9
Turno 4 · Kira [#########.] 81/90 · Campeón [#######...] 65/100
> pocion
  No te quedan pociones
Se terminaron las órdenes: el duelo queda pendiente.
```

##### Ataca siempre
```entrada
atacar
atacar
atacar
atacar
atacar
atacar
atacar
atacar
atacar
atacar
atacar
atacar
atacar
atacar
atacar
```
```salida
Turno 1 · Kira [##########] 90/90 · Campeón [##########] 100/100
> atacar
  Kira ataca: 14
  El Campeón golpea: 12
Turno 2 · Kira [#########.] 78/90 · Campeón [#########.] 86/100
> atacar
  Kira ataca: 12
  El Campeón golpea: 10
Turno 3 · Kira [########..] 68/90 · Campeón [#######...] 74/100
> atacar
  Kira ataca: 6 (el Campeón se defendió)
  El Campeón golpea: 11
Turno 4 · Kira [######....] 57/90 · Campeón [#######...] 68/100
> atacar
  Kira ataca: 8 (el Campeón se defendió)
  El Campeón golpea: 13
Turno 5 · Kira [#####.....] 44/90 · Campeón [######....] 60/100
> atacar
  Kira ataca: 7 (el Campeón se defendió)
  El Campeón golpea: 13
Turno 6 · Kira [###.......] 31/90 · Campeón [#####.....] 53/100
> atacar
  Kira ataca: 7 (el Campeón se defendió)
  El Campeón golpea: 9
Turno 7 · Kira [##........] 22/90 · Campeón [#####.....] 46/100
> atacar
  Kira ataca: 6 (el Campeón se defendió)
  El Campeón golpea: 11
Turno 8 · Kira [#.........] 11/90 · Campeón [####......] 40/100
> atacar
  Kira ataca: 6 (el Campeón se defendió)
  El Campeón golpea: 12
Kira cayó. El Campeón sigue invicto.
```

##### Órdenes desconocidas
```entrada
nadar
estado
```
```salida
Turno 1 · Kira [##########] 90/90 · Campeón [##########] 100/100
> nadar
  Orden desconocida
Turno 1 · Kira [##########] 90/90 · Campeón [##########] 100/100
> estado
  Pociones: 2 · bombas: 1
Se terminaron las órdenes: el duelo queda pendiente.
```

### Misión S01-N04-M2 · La Arena completa

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 40
```

#### Consigna

Armá el juego completo como un **proyecto con Composer** (namespace `Arena\`, PSR-4,
sin dependencias externas) y MariaDB:

```
arena/
├── composer.json
├── esquema.sql          ← tabla partida (jugador, clase, oleada, puntos)
├── config.php
├── juego.php            ← el programa: lee las órdenes de STDIN
└── src/
    ├── Dados.php, DadosConSemilla.php
    ├── Clase.php        ← enum: guerrero, maga, arquero (vida, ataque, defensa)
    ├── Heroe.php, Enemigo.php, Personaje.php
    ├── Oleadas.php      ← generador de oleadas
    └── Ranking.php      ← repositorio PDO
```

El juego:
1. lee el nombre y la clase del jugador (dos primeros renglones);
2. va oleada por oleada; en cada turno el jugador elige `atacar N` (al enemigo número
   N de la oleada), `pocion` o `huir` (termina la partida guardando lo logrado);
3. entre oleadas, el héroe recupera un 30% de la vida y gana una poción cada dos
   oleadas;
4. al terminar (cae, huye o se acaba la entrada), guarda la partida en el ranking y
   muestra el top 3 con la posición del jugador.

Usá una semilla fija (`--semilla` no hace falta: fijala en `juego.php` con 99) para
que la partida del ejemplo sea repetible.

#### Criterio de aprobación

- Proyecto con Composer y PSR-4; el SQL solo en `Ranking`.
- Las órdenes inválidas o con un número de enemigo inexistente no gastan el turno.
- La partida se guarda y el top muestra la posición del jugador.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
Lía
maga
atacar 1
atacar 1
atacar 2
atacar 1
atacar 9
atacar 1
atacar 2
pocion
atacar 2
atacar 1
atacar 1
atacar 2
atacar 2
huir
```

#### Salida esperada

```
¡Lía (maga) entra a la Arena! Vida 60, ataque 14
== Oleada 1: 1. Orco (18)
  Lía golpea al Orco 1: 17
  Orco ataca: 6 (vida 54)
  Lía golpea al Orco 1: 1 ¡cae!
  ¡Oleada superada! Puntos: 60 · vida 60 · pociones 2
== Oleada 2: 1. Orco (22), 2. Goblin (23)
  Lía golpea al Goblin 2: 15
  Orco ataca: 8 (vida 52)
  Goblin ataca: 10 (vida 42)
  Lía golpea al Orco 1: 16
  Orco ataca: 6 (vida 36)
  Goblin ataca: 7 (vida 29)
  Orden inválida: «atacar 9»
  Lía golpea al Orco 1: 6 ¡cae!
  Goblin ataca: 10 (vida 19)
  Lía golpea al Goblin 2: 8 ¡cae!
  ¡Oleada superada! Puntos: 200 · vida 37 · pociones 3
== Oleada 3: 1. Troll (24), 2. Orco (27)
  Poción: +23 (vida 60)
  Troll ataca: 6 (vida 54)
  Orco ataca: 6 (vida 48)
  Lía golpea al Orco 2: 15
  Troll ataca: 7 (vida 41)
  Orco ataca: 9 (vida 32)
  Lía golpea al Troll 1: 16
  Troll ataca: 9 (vida 23)
  Orco ataca: 8 (vida 15)
  Lía golpea al Troll 1: 8 ¡cae!
  Orco ataca: 9 (vida 6)
  Lía golpea al Orco 2: 12 ¡cae!
  ¡Oleada superada! Puntos: 410 · vida 24 · pociones 2
== Oleada 4: 1. Orco (32), 2. Orco (30), 3. Troll (34)
  Lía golpea al Orco 2: 20
  Orco ataca: 9 (vida 15)
  Orco ataca: 11 (vida 4)
  Troll ataca: 4 (vida 0)
Fin: Lía cayó en la arena en la oleada 4 con 410 puntos
Tablero de honor:
  1. Nara (610)
  2. Lía (410)
  3. Bron (380)
Lía quedó en el puesto 2
```

#### Solución de referencia

`composer.json`
```json
{
    "name": "puerto/arena",
    "require": { "php": ">=8.2" },
    "autoload": { "psr-4": { "Arena\\": "src/" } }
}
```

`esquema.sql`
```sql
DROP TABLE IF EXISTS partida;
CREATE TABLE partida (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jugador VARCHAR(30) NOT NULL,
    clase VARCHAR(10) NOT NULL,
    oleada INT NOT NULL,
    puntos INT NOT NULL,
    INDEX idx_partida_puntos (puntos)
);
INSERT INTO partida (jugador, clase, oleada, puntos) VALUES ('Bron', 'guerrero', 3, 380), ('Tomi', 'arquero', 2, 160), ('Nara', 'maga', 4, 610);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`src/Dados.php`
```php
<?php
declare(strict_types=1);

namespace Arena;

interface Dados
{
    public function tirar(int $caras): int;
}
```

`src/DadosConSemilla.php`
```php
<?php
declare(strict_types=1);

namespace Arena;

final class DadosConSemilla implements Dados
{
    public function __construct(int $semilla)
    {
        mt_srand($semilla);
    }

    public function tirar(int $caras): int
    {
        return mt_rand(1, $caras);
    }
}
```

`src/Clase.php`
```php
<?php
declare(strict_types=1);

namespace Arena;

enum Clase: string
{
    case Guerrero = 'guerrero';
    case Maga = 'maga';
    case Arquero = 'arquero';

    public function vida(): int { return match ($this) { self::Guerrero => 90, self::Maga => 60, self::Arquero => 70 }; }

    public function ataque(): int { return match ($this) { self::Guerrero => 9, self::Maga => 14, self::Arquero => 11 }; }

    public function defensa(): int { return match ($this) { self::Guerrero => 3, self::Maga => 1, self::Arquero => 2 }; }
}
```

`src/Personaje.php`
```php
<?php
declare(strict_types=1);

namespace Arena;

abstract class Personaje
{
    private int $vida;

    public function __construct(public readonly string $nombre, private int $vidaMaxima, public readonly int $ataque)
    {
        $this->vida = $vidaMaxima;
    }

    public function recibirDanio(int $n): int
    {
        $antes = $this->vida;
        $this->vida = max(0, $this->vida - max(0, $n));
        return $antes - $this->vida;
    }

    public function curar(int $n): int
    {
        $antes = $this->vida;
        $this->vida = min($this->vidaMaxima, $this->vida + $n);
        return $this->vida - $antes;
    }

    public function vida(): int { return $this->vida; }

    public function vidaMaxima(): int { return $this->vidaMaxima; }

    public function estaVivo(): bool { return $this->vida > 0; }
}
```

`src/Heroe.php`
```php
<?php
declare(strict_types=1);

namespace Arena;

final class Heroe extends Personaje
{
    public int $pociones = 2;

    public function __construct(string $nombre, public readonly Clase $clase)
    {
        parent::__construct($nombre, $clase->vida(), $clase->ataque());
    }

    public function recibirDanio(int $n): int
    {
        return parent::recibirDanio(max(1, $n - $this->clase->defensa()));
    }
}
```

`src/Enemigo.php`
```php
<?php
declare(strict_types=1);

namespace Arena;

final class Enemigo extends Personaje {}
```

`src/Oleadas.php`
```php
<?php
declare(strict_types=1);

namespace Arena;

use Generator;

final class Oleadas
{
    private const NOMBRES = ['Goblin', 'Orco', 'Troll'];

    public function __construct(private Dados $dados) {}

    /** @return Generator<int, Enemigo[]> */
    public function generar(): Generator
    {
        for ($n = 1; ; $n++) {
            $fuerza = 1 + ($n - 1) * 0.3;
            $enemigos = [];
            for ($i = 0; $i < min(1 + intdiv($n, 2), 4); $i++) {
                $tipo = self::NOMBRES[min(2, intdiv($this->dados->tirar(6) + $n - 1, 3))];
                $enemigos[] = new Enemigo($tipo, (int) round((8 + $this->dados->tirar(10)) * $fuerza), (int) round((2 + $this->dados->tirar(3)) * $fuerza));
            }
            yield $n => $enemigos;
        }
    }
}
```

`src/Ranking.php`
```php
<?php
declare(strict_types=1);

namespace Arena;

use PDO;

final class Ranking
{
    public function __construct(private PDO $pdo) {}

    public function guardar(string $jugador, string $clase, int $oleada, int $puntos): void
    {
        $this->pdo->prepare('INSERT INTO partida (jugador, clase, oleada, puntos) VALUES (?, ?, ?, ?)')->execute([$jugador, $clase, $oleada, $puntos]);
    }

    public function top(int $n): array
    {
        $s = $this->pdo->prepare('SELECT jugador, MAX(puntos) AS mejor FROM partida GROUP BY jugador ORDER BY mejor DESC, jugador LIMIT ?');
        $s->bindValue(1, $n, PDO::PARAM_INT);
        $s->execute();
        return $s->fetchAll();
    }

    public function posicion(string $jugador): int
    {
        $s = $this->pdo->prepare('SELECT COUNT(*) + 1 FROM (SELECT jugador FROM partida GROUP BY jugador HAVING MAX(puntos) > (SELECT MAX(puntos) FROM partida WHERE jugador = ?)) t');
        $s->execute([$jugador]);
        return (int) $s->fetchColumn();
    }
}
```

`juego.php`
```php
<?php
declare(strict_types=1);
// Jefe de la Arena - La Arena completa: un RPG jugable con Composer y MariaDB.
require __DIR__ . '/vendor/autoload.php';

use Arena\Clase;
use Arena\DadosConSemilla;
use Arena\Enemigo;
use Arena\Heroe;
use Arena\Oleadas;
use Arena\Ranking;

$leer = fn(): ?string => ($l = fgets(STDIN)) === false ? null : trim($l);
$dados = new DadosConSemilla(99);
$nombre = $leer() ?? 'Anónimo';
$clase = Clase::tryFrom(strtolower($leer() ?? '')) ?? Clase::Guerrero;
$heroe = new Heroe($nombre, $clase);
echo "¡$nombre ({$clase->value}) entra a la Arena! Vida {$heroe->vida()}, ataque {$heroe->ataque}\n";

$puntos = 0;
$oleadaAlcanzada = 0;
$fin = null;
foreach ((new Oleadas($dados))->generar() as $n => $enemigos) {
    $oleadaAlcanzada = $n;
    echo "== Oleada $n: ", implode(', ', array_map(fn(Enemigo $e, $i) => ($i + 1) . ". {$e->nombre} ({$e->vida()})", $enemigos, array_keys($enemigos))), "\n";
    while ($heroe->estaVivo() && array_filter($enemigos, fn(Enemigo $e) => $e->estaVivo())) {
        $orden = $leer();
        if ($orden === null || $orden === 'huir') {
            $fin = $orden === null ? 'se acabaron las órdenes' : 'huyó';
            break 2;
        }
        if ($orden === 'pocion') {
            if ($heroe->pociones === 0) {
                echo "  No quedan pociones\n";
                continue;
            }
            $heroe->pociones--;
            echo "  Poción: +", $heroe->curar(30), " (vida {$heroe->vida()})\n";
        } elseif (preg_match('/^atacar (\d+)$/', $orden, $m) && isset($enemigos[$m[1] - 1]) && $enemigos[$m[1] - 1]->estaVivo()) {
            $objetivo = $enemigos[$m[1] - 1];
            $danio = $objetivo->recibirDanio($heroe->ataque + $dados->tirar(6));
            echo "  $nombre golpea al {$objetivo->nombre} {$m[1]}: $danio", $objetivo->estaVivo() ? '' : ' ¡cae!', "\n";
            if (!$objetivo->estaVivo()) {
                $puntos += 10 * $n;
            }
        } else {
            echo "  Orden inválida: «{$orden}»\n";
            continue;
        }
        foreach ($enemigos as $e) {
            if ($e->estaVivo() && $heroe->estaVivo()) {
                echo "  {$e->nombre} ataca: ", $heroe->recibirDanio($e->ataque + $dados->tirar(4)), " (vida {$heroe->vida()})\n";
            }
        }
    }
    if (!$heroe->estaVivo()) {
        $fin = 'cayó en la arena';
        break;
    }
    $puntos += 50 * $n;
    $heroe->curar((int) round($heroe->vidaMaxima() * 0.3));
    if ($n % 2 === 0) {
        $heroe->pociones++;
    }
    echo "  ¡Oleada superada! Puntos: $puntos · vida {$heroe->vida()} · pociones {$heroe->pociones}\n";
}

echo "Fin: $nombre $fin en la oleada $oleadaAlcanzada con $puntos puntos\n";
$c = require __DIR__ . '/config.php';
$ranking = new Ranking(new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]));
$ranking->guardar($nombre, $clase->value, $oleadaAlcanzada, $puntos);
echo "Tablero de honor:\n";
foreach ($ranking->top(3) as $i => $f) {
    echo "  ", $i + 1, ". {$f['jugador']} ({$f['mejor']})\n";
}
echo "$nombre quedó en el puesto ", $ranking->posicion($nombre), "\n";
```

### Prueba del sello

#### ¿Por qué las órdenes inválidas no gastan el turno?

Para que un error de tipeo del jugador no lo castigue: se avisa y se vuelve a pedir la orden.

#### ¿Cómo se prueba un juego que lee lo que escribe el jugador?

Guardando las órdenes en un archivo y redirigiendo la entrada (`php juego.php < partida.txt`), con una semilla fija para que el azar salga siempre igual.

#### ¿Qué hace `continue 2` adentro de un `switch` que está en un `while`?

Salta a la siguiente vuelta del `while` (un `continue` solo actuaría como `break` del `switch`).

#### ¿Dónde está el SQL en el proyecto de la Arena?

Solo en el repositorio `Ranking`: el resto del juego no sabe que existe una base.

#### ¿Qué tiene que pasar cuando se termina la entrada a mitad de una oleada?

El juego termina prolijamente: guarda lo logrado y muestra el ranking, sin avisos ni errores.

### Soluciones (docente)

Jefe de la Senda: integra el modelo, el motor, las oleadas y el ranking de `21-PHP/21` a `23`, con el azar controlado para poder corregir con una entrada fija. La misión 1 se corrige con `php duelo.php < entrada.txt`; la 2 con `composer install` y `php juego.php < entrada.txt` (con el esquema cargado). Los alumnos pueden jugar de verdad quitando la semilla fija (`time()` en lugar de 99).
