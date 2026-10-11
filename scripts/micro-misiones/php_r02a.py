from genphp import m
from php_r01 import NILO, ELEFA, IARA, PICO, GHECO

ASTILLERO = "El Astillero de los Moldes"
TIMON = "El barco del timón"
PIZARRA = "La pizarra de la puerta"
ARBOL = "El árbol de las embarcaciones"
CAPATAZ = "La lista del capataz"

NODOS = [
    {
        "titulo": "R02-N01 · Clases y objetos",
        "misiones": [
            m(id="R02-N01-P1", titulo="El molde del bote",
              lugar=ASTILLERO, personajes="Nilo, Gheco",
              carta="Clase y objeto | class Bote { public string $nombre; } · $b = new Bote(); · $b->nombre = 'Gaviota'; · un molde, muchos botes",
              recompensa="xp 10, oro 10",
              escena="""
                  Pasando la roca de la Sirena empieza el **Astillero**: moldes de madera colgados de las paredes, uno para cada tipo de barco. Con el molde del bote, los carpinteros arman muchos botes iguales. A Nilo le dan uno para que lo bautice.
              """,
              sugiere="`new Bote()` crea un bote nuevo con el molde. Sus datos se escriben y se leen con la flecha: `$b->nombre`.",
              desafio="Creá dos botes con el molde y ponele nombre y color a cada uno.",
              inicial='''
                  <?php
                  class Bote
                  {
                      public string $nombre = '';
                      public string $color = '';
                  }

                  $a = ___;
                  $a->nombre = 'Gaviota';
                  $a->color = 'violeta';

                  echo "{$a->nombre} ({$a->color})\\n";
              ''',
              solucion='''
                  <?php
                  class Bote
                  {
                      public string $nombre = '';
                      public string $color = '';
                  }

                  $a = new Bote();
                  $a->nombre = 'Gaviota';
                  $a->color = 'violeta';

                  $b = new Bote();
                  $b->nombre = 'Albatros';
                  $b->color = 'blanco';

                  echo "{$a->nombre} ({$a->color})\\n";
                  echo "{$b->nombre} ({$b->color})\\n";
              ''',
              al_superar="Nilo pinta el suyo de violeta, como su bufanda, y le pone *Gaviota*. Ya hay catorce barcos que se llaman *Gaviota*.",
              imagen=["Un astillero de madera de noche, con moldes de barcos colgados de las paredes y dos botes recién armados.",
                      NILO + " pinta un bote de violeta con un pincel grande.", GHECO + " sobre la proa."]),
            m(id="R02-N01-P2", titulo="El constructor",
              lugar=ASTILLERO, personajes="Nilo, Gheco",
              criatura="troll",
              carta="Constructor | public function __construct(public string $nombre, public int $carga) {} · el objeto nace con sus datos · promoción de propiedades",
              recompensa="xp 10, oro 10",
              escena="""
                  Un bote salió del astillero sin nombre: alguien se olvidó de ponérselo después de crearlo. Un **troll** se escondió en el hueco del nombre. —Que nazca con su nombre —dice Gheco—, no que se lo pongan después.
              """,
              sugiere="Con `__construct(public string $nombre, public int $carga)` el bote **recibe** sus datos al crearse: `new Bote('Gaviota', 120)`. Así nunca nace vacío.",
              desafio="Escribí el constructor con promoción de propiedades y creá los botes con sus datos.",
              inicial='''
                  <?php
                  class Bote
                  {
                      public string $nombre;
                      public int $carga;
                  }

                  $b = new Bote();
                  echo "{$b->nombre}: {$b->carga} kg\\n";
              ''',
              solucion='''
                  <?php
                  class Bote
                  {
                      public function __construct(
                          public string $nombre,
                          public int $carga,
                      ) {
                      }
                  }

                  $b = new Bote('Gaviota', 120);
                  $c = new Bote('Tortuga', 40);
                  echo "{$b->nombre}: {$b->carga} kg\\n";
                  echo "{$c->nombre}: {$c->carga} kg\\n";
              ''',
              al_superar="Los botes salen del molde con su nombre puesto. El troll se queda sin hueco donde vivir.",
              imagen=["Un molde de bote de madera abierto del que sale un bote terminado con una plaquita lisa en la proa.",
                      "Un troll se va enojado arrastrando los pies.", NILO + " empuja el bote al agua.", GHECO + " sobre el molde."]),
            m(id="R02-N01-P3", titulo="Lo que sabe hacer un barco",
              lugar=ASTILLERO, personajes="Nilo, Iara, Gheco",
              carta="Métodos | public function cargar(int $kg): void { $this->carga += $kg; } · $this es el objeto que recibe el pedido",
              recompensa="xp 15, oro 15",
              escena="""
                  Iara anota la carga de cada bote a mano, y se equivoca de bote. —Que el bote sepa cargarse solo —le dice Nilo, orgulloso de haber entendido algo—. —¿Lo anotaste? —contesta Iara.
              """,
              sugiere="Un método es una función adentro de la clase. Con `$this->carga` el bote cambia **su** carga, no la de otro.",
              desafio="Escribí el método `cargar` y usalo para cargar los dos botes.",
              inicial='''
                  <?php
                  class Bote
                  {
                      public function __construct(public string $nombre, public int $carga = 0)
                      {
                      }

                      // Escribí cargar acá
                  }

                  $a = new Bote('Gaviota');
                  $b = new Bote('Tortuga');
                  $a->cargar(30);
                  $b->cargar(12);
                  $a->cargar(5);
                  echo "{$a->nombre}: {$a->carga} kg\\n";
                  echo "{$b->nombre}: {$b->carga} kg\\n";
              ''',
              solucion='''
                  <?php
                  class Bote
                  {
                      public function __construct(public string $nombre, public int $carga = 0)
                      {
                      }

                      public function cargar(int $kilos): void
                      {
                          $this->carga += $kilos;
                      }
                  }

                  $a = new Bote('Gaviota');
                  $b = new Bote('Tortuga');
                  $a->cargar(30);
                  $b->cargar(12);
                  $a->cargar(5);
                  echo "{$a->nombre}: {$a->carga} kg\\n";
                  echo "{$b->nombre}: {$b->carga} kg\\n";
              ''',
              al_superar="Cada bote lleva su cuenta. Iara tacha una columna entera de su libreta, aliviada.",
              imagen=["Dos botes en un muelle del astillero, uno más cargado de cajones que el otro.",
                      IARA + " compara los botes con la libreta.", NILO + " sube un cajón a un bote.", GHECO + " sobre un cajón."]),
            m(id="R02-N01-P4", titulo="El bote se presenta",
              lugar=ASTILLERO, personajes="Nilo, Gheco",
              carta="__toString | public function __toString(): string · el objeto sabe mostrarse con echo · una sola vez, en la clase",
              recompensa="xp 10, oro 10",
              escena="""
                  Cada vez que alguien pregunta por un bote, Nilo arma el texto a mano, y cada vez lo arma distinto. Gheco le muestra que el bote mismo puede saber presentarse.
              """,
              sugiere="Con `__toString()` el objeto devuelve su texto, y `echo $bote` lo usa solo.",
              desafio="Escribí `__toString` para que `echo $bote` muestre «Gaviota (120 kg)».",
              inicial='''
                  <?php
                  class Bote
                  {
                      public function __construct(public string $nombre, public int $carga)
                      {
                      }
                  }

                  $botes = [new Bote('Gaviota', 120), new Bote('Albatros', 800)];
                  foreach ($botes as $b) {
                      echo $b . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  class Bote
                  {
                      public function __construct(public string $nombre, public int $carga)
                      {
                      }

                      public function __toString(): string
                      {
                          return "{$this->nombre} ({$this->carga} kg)";
                      }
                  }

                  $botes = [new Bote('Gaviota', 120), new Bote('Albatros', 800)];
                  foreach ($botes as $b) {
                      echo $b . "\\n";
                  }
              ''',
              al_superar="Los botes se presentan solos, siempre igual. Nilo le enseña al suyo a decir «violeta» también. No funciona.",
              imagen=["Dos botes amarrados con plaquitas lisas en la proa que brillan suave, como si hablaran.",
                      NILO + " escucha con la mano en la oreja.", GHECO + " sobre una plaquita."]),
        ],
    },
    {
        "titulo": "R02-N02 · Encapsulamiento y readonly",
        "misiones": [
            m(id="R02-N02-P1", titulo="Solo el capitán",
              lugar=TIMON, personajes="Nilo, Pico, Gheco",
              carta="private | private int $rumbo; · desde afuera no se toca · se cambia solo con un método que revisa",
              recompensa="xp 10, oro 10",
              escena="""
                  En el Astillero hay un barco con un cartel en el timón: *«Solo el capitán»*. Una noche, **Pico** se posó en el timón, lo giró con las patas y el barco terminó encallado. Nilo jura que Pico no lo hizo a propósito.
              """,
              sugiere="Si el rumbo es `private`, nadie lo cambia desde afuera. El método `girar()` lo cambia, pero solo si el ángulo está entre 0 y 359.",
              desafio="Hacé privado el rumbo y que `girar` rechace los ángulos imposibles.",
              inicial='''
                  <?php
                  class Barco
                  {
                      public int $rumbo = 0;

                      public function girar(int $grados): void
                      {
                          $this->rumbo = $grados;
                      }

                      public function rumbo(): int
                      {
                          return $this->rumbo;
                      }
                  }

                  $b = new Barco();
                  $b->girar(90);
                  $b->girar(720);
                  echo "Rumbo: " . $b->rumbo() . "\\n";
              ''',
              solucion='''
                  <?php
                  class Barco
                  {
                      private int $rumbo = 0;

                      public function girar(int $grados): void
                      {
                          if ($grados < 0 || $grados > 359) {
                              echo "Rumbo imposible: $grados\\n";
                              return;
                          }
                          $this->rumbo = $grados;
                      }

                      public function rumbo(): int
                      {
                          return $this->rumbo;
                      }
                  }

                  $b = new Barco();
                  $b->girar(90);
                  $b->girar(720);
                  echo "Rumbo: " . $b->rumbo() . "\\n";
              ''',
              al_superar="El timón ahora solo gira con la palanca que revisa el rumbo. Pico lo intenta igual y se queda mirando el timón, ofendido.",
              imagen=["El timón de un barco de madera con una palanca de bronce al lado, en un astillero de noche.",
                      PICO + " parado sobre el timón, empujándolo con las patas.", NILO + " lo mira con cariño.", GHECO + " sobre la palanca."]),
            m(id="R02-N02-P2", titulo="Nacer válido",
              lugar=TIMON, personajes="Nilo, Gheco",
              criatura="ogro",
              carta="Validar en el constructor | throw new InvalidArgumentException('…') · el objeto nunca nace con datos imposibles",
              recompensa="xp 15, oro 15",
              escena="""
                  Del Astillero salió un barco con calado negativo. Nadie se dio cuenta hasta que intentó amarrar y un **ogro** se rió del agujero en el muelle.
              """,
              sugiere="Si el constructor revisa el dato y lanza una excepción cuando no tiene sentido, el objeto **nunca existe** inválido. Para probarlo, el intento va dentro de `try { … } catch (InvalidArgumentException $e) { … }`.",
              desafio="Validá el calado en el constructor: tiene que ser mayor que 0.",
              inicial='''
                  <?php
                  class Barco
                  {
                      public function __construct(public readonly string $nombre, public readonly float $calado)
                      {
                      }
                  }

                  try {
                      $b = new Barco('Gaviota', -3);
                      echo "Botado: {$b->nombre}\\n";
                  } catch (InvalidArgumentException $e) {
                      echo "Rechazado: " . $e->getMessage() . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  class Barco
                  {
                      public function __construct(public readonly string $nombre, public readonly float $calado)
                      {
                          if ($calado <= 0) {
                              throw new InvalidArgumentException("calado imposible para $nombre");
                          }
                      }
                  }

                  try {
                      $b = new Barco('Gaviota', -3);
                      echo "Botado: {$b->nombre}\\n";
                  } catch (InvalidArgumentException $e) {
                      echo "Rechazado: " . $e->getMessage() . "\\n";
                  }
              ''',
              al_superar="El barco con calado negativo no llega a existir. El ogro se queda sin chiste.",
              imagen=["Un barco a medio armar en una grada del astillero, con un sello rojo de rechazo pegado en el casco, sin letras.",
                      "Un ogro se rasca la cabeza, decepcionado.", NILO + " pega el sello.", GHECO + " sobre el casco."]),
            m(id="R02-N02-P3", titulo="Lo que no cambia nunca",
              lugar=TIMON, personajes="Nilo, Elefa, Gheco",
              carta="readonly | public readonly string $matricula · se asigna una vez, en el constructor · después, error si se toca",
              recompensa="xp 10, oro 10",
              escena="""
                  La matrícula de un barco se graba una vez y no se cambia nunca. Pero en el programa de Nilo, cualquiera la puede pisar. Elefa sella la matrícula con su bastón: —Lo que se graba, queda.
              """,
              sugiere="Con `readonly`, la propiedad se asigna en el constructor y después no se puede cambiar: intentarlo da un `Error` que se puede atrapar.",
              desafio="Marcá la matrícula como `readonly` para que el intento de cambiarla falle.",
              inicial='''
                  <?php
                  class Barco
                  {
                      public function __construct(public string $matricula)
                      {
                      }
                  }

                  $b = new Barco('PM-0042');
                  try {
                      $b->matricula = 'PIRATA-1';
                      echo "Cambiada a {$b->matricula}\\n";
                  } catch (Error $e) {
                      echo "No se puede: la matricula es de solo lectura\\n";
                  }
                  echo "Matricula: {$b->matricula}\\n";
              ''',
              solucion='''
                  <?php
                  class Barco
                  {
                      public function __construct(public readonly string $matricula)
                      {
                      }
                  }

                  $b = new Barco('PM-0042');
                  try {
                      $b->matricula = 'PIRATA-1';
                      echo "Cambiada a {$b->matricula}\\n";
                  } catch (Error $e) {
                      echo "No se puede: la matricula es de solo lectura\\n";
                  }
                  echo "Matricula: {$b->matricula}\\n";
              ''',
              al_superar="La matrícula queda grabada. Elefa asiente. —¿Cómo me llamo? —pregunta. Nilo mira la matrícula, como si ahí estuviera la respuesta.",
              imagen=["La proa de un barco con una placa de bronce grabada con dibujitos de olas y un sello de lacre violeta encima, sin letras.",
                      ELEFA + " sella la placa con el bastón.", NILO + " mira la placa.", GHECO + " sobre la proa."]),
            m(id="R02-N02-P4", titulo="El precio que no se pisa",
              lugar=TIMON, personajes="Nilo, Iara, Gheco",
              carta="Objeto valor | inmutable · conSuma() devuelve un objeto NUEVO · el original queda igual · seguro para compartir",
              recompensa="xp 15, oro 15",
              escena="""
                  Iara y Nilo comparten el mismo objeto `Precio` para dos presupuestos. Nilo le suma un recargo al suyo… y el de Iara también cambia. —¿Quién tocó mi precio? —pregunta Iara, con el lápiz en alto.
              """,
              sugiere="Si `Precio` es `readonly`, no se puede cambiar: `conRecargo()` devuelve un **precio nuevo** y el viejo queda igual.",
              desafio="Hacé que `conRecargo` devuelva un precio nuevo en lugar de cambiar el que hay.",
              inicial='''
                  <?php
                  class Precio
                  {
                      public function __construct(public int $sellos)
                      {
                      }

                      public function conRecargo(int $extra): Precio
                      {
                          $this->sellos += $extra;
                          return $this;
                      }
                  }

                  $base = new Precio(100);
                  $nilo = $base->conRecargo(20);
                  echo "Iara: {$base->sellos}\\n";
                  echo "Nilo: {$nilo->sellos}\\n";
              ''',
              solucion='''
                  <?php
                  final class Precio
                  {
                      public function __construct(public readonly int $sellos)
                      {
                      }

                      public function conRecargo(int $extra): Precio
                      {
                          return new Precio($this->sellos + $extra);
                      }
                  }

                  $base = new Precio(100);
                  $nilo = $base->conRecargo(20);
                  echo "Iara: {$base->sellos}\\n";
                  echo "Nilo: {$nilo->sellos}\\n";
              ''',
              al_superar="Cada uno con su precio. Iara baja el lápiz.",
              imagen=["Dos papeles de presupuesto sobre una mesa del astillero, con sellos de lacre de distinto tamaño, sin letras.",
                      IARA + " protege su papel con la mano.", NILO + " sostiene el suyo.", GHECO + " entre los dos papeles."]),
        ],
    },
    {
        "titulo": "R02-N03 · Static, constantes de clase y fábricas",
        "misiones": [
            m(id="R02-N03-P1", titulo="El calado máximo",
              lugar=PIZARRA, personajes="Nilo, Iara, Gheco",
              carta="Constantes de clase | const CALADO_MAXIMO = 12; · self::CALADO_MAXIMO adentro · Barco::CALADO_MAXIMO afuera",
              recompensa="xp 10, oro 10",
              escena="""
                  Para no olvidarse del calado máximo del puerto, Nilo lo escribió con tiza en la proa de cada barco, y en tres puso un número distinto. Iara los borra uno por uno. El dato es del **molde**, no de cada barco.
              """,
              sugiere="Una constante de clase se escribe una vez: `const CALADO_MAXIMO = 12;`. Adentro de la clase se usa como `self::CALADO_MAXIMO`.",
              desafio="Reemplazá los números sueltos por la constante de la clase.",
              inicial='''
                  <?php
                  class Barco
                  {
                      public function __construct(public string $nombre, public float $calado)
                      {
                      }

                      public function entra(): bool
                      {
                          return $this->calado <= 15;
                      }
                  }

                  foreach ([new Barco('Gaviota', 4), new Barco('Leviatan', 14)] as $b) {
                      echo $b->nombre . ": " . ($b->entra() ? "entra" : "no entra") . " (maximo 12 m)\\n";
                  }
              ''',
              solucion='''
                  <?php
                  class Barco
                  {
                      const CALADO_MAXIMO = 12;

                      public function __construct(public string $nombre, public float $calado)
                      {
                      }

                      public function entra(): bool
                      {
                          return $this->calado <= self::CALADO_MAXIMO;
                      }
                  }

                  foreach ([new Barco('Gaviota', 4), new Barco('Leviatan', 14)] as $b) {
                      echo $b->nombre . ": " . ($b->entra() ? "entra" : "no entra") . " (maximo " . Barco::CALADO_MAXIMO . " m)\\n";
                  }
              ''',
              al_superar="Un solo número, en un solo lugar. Iara guarda la tiza en el bolsillo de Nilo. Se cae por el agujero.",
              imagen=["Una pizarra negra en la puerta de un astillero con un dibujo de un barco y una línea de agua marcada, sin números.",
                      IARA + " borra la proa de un barco con un trapo.", NILO + " con una tiza en la mano.", GHECO + " sobre la pizarra."]),
            m(id="R02-N03-P2", titulo="¿Cuántos se botaron?",
              lugar=PIZARRA, personajes="Nilo, Gheco",
              carta="static | private static int $botados = 0; · es de la clase, no de un objeto · self::$botados++ en el constructor",
              recompensa="xp 15, oro 15",
              escena="""
                  La pizarra de la puerta dice cuántos barcos se botaron este año. Nilo puso el contador adentro de cada barco, y cada barco dice «1».
              """,
              sugiere="Un contador que es de **todos** los barcos va `static`: `private static int $botados = 0;` y en el constructor `self::$botados++`.",
              desafio="Hacé que el contador sea de la clase y que cuente todos los barcos botados.",
              inicial='''
                  <?php
                  class Barco
                  {
                      private int $botados = 0;

                      public function __construct(public string $nombre)
                      {
                          $this->botados++;
                      }

                      public function botados(): int
                      {
                          return $this->botados;
                      }
                  }

                  new Barco('Gaviota');
                  new Barco('Albatros');
                  $ultimo = new Barco('Tortuga');
                  echo "Botados este año: " . $ultimo->botados() . "\\n";
              ''',
              solucion='''
                  <?php
                  class Barco
                  {
                      private static int $botados = 0;

                      public function __construct(public string $nombre)
                      {
                          self::$botados++;
                      }

                      public static function botados(): int
                      {
                          return self::$botados;
                      }
                  }

                  new Barco('Gaviota');
                  new Barco('Albatros');
                  new Barco('Tortuga');
                  echo "Botados este año: " . Barco::botados() . "\\n";
              ''',
              al_superar="La pizarra dice 3. El capataz del Astillero, que había contado con los dedos, también dice 3. Por primera vez coinciden.",
              imagen=["Una pizarra en la puerta del astillero con tres palitos marcados con tiza, y tres barcos en el agua detrás.",
                      NILO + " agrega un palito con la tiza.", GHECO + " sobre la pizarra."]),
            m(id="R02-N03-P3", titulo="Dos puertas para fabricar",
              lugar=PIZARRA, personajes="Nilo, Gheco",
              carta="Fábricas | public static function velero(string $n): self { return new self($n, 'velero', 2); } · constructores con nombre",
              recompensa="xp 15, oro 15",
              escena="""
                  Para pedir un velero hay que acordarse de pasarle «velero» y 2 mástiles; para un remolcador, «remolcador» y 0. Nilo pidió un velero con 0 mástiles, que todavía está en la grada sin saber cómo moverse.
              """,
              sugiere="Un método `static` que crea el objeto con los datos correctos: `Barco::velero('Brisa')`. El nombre del método dice qué se fabrica.",
              desafio="Escribí las fábricas `velero` y `remolcador`.",
              inicial='''
                  <?php
                  class Barco
                  {
                      public function __construct(public string $nombre, public string $tipo, public int $mastiles)
                      {
                      }
                  }

                  $a = new Barco('Brisa', 'velero', 0);
                  $b = new Barco('Forzudo', 'remolcador', 0);
                  echo "{$a->nombre}: {$a->tipo}, {$a->mastiles} mastiles\\n";
                  echo "{$b->nombre}: {$b->tipo}, {$b->mastiles} mastiles\\n";
              ''',
              solucion='''
                  <?php
                  class Barco
                  {
                      public function __construct(public string $nombre, public string $tipo, public int $mastiles)
                      {
                      }

                      public static function velero(string $nombre): self
                      {
                          return new self($nombre, 'velero', 2);
                      }

                      public static function remolcador(string $nombre): self
                      {
                          return new self($nombre, 'remolcador', 0);
                      }
                  }

                  $a = Barco::velero('Brisa');
                  $b = Barco::remolcador('Forzudo');
                  echo "{$a->nombre}: {$a->tipo}, {$a->mastiles} mastiles\\n";
                  echo "{$b->nombre}: {$b->tipo}, {$b->mastiles} mastiles\\n";
              ''',
              al_superar="El velero sale con sus dos mástiles y se va navegando, aliviado.",
              imagen=["Dos puertas de taller en el astillero, una con un dibujo de una vela y otra con un dibujo de un ancla, de las que salen un velero y un remolcador.",
                      NILO + " entre las dos puertas, señalando.", GHECO + " sobre el marco de una puerta."]),
        ],
    },
    {
        "titulo": "R02-N04 · Herencia",
        "misiones": [
            m(id="R02-N04-P1", titulo="La Embarcación y el Velero",
              lugar=ARBOL, personajes="Nilo, Gheco",
              carta="extends | class Velero extends Embarcacion · hereda todo lo del padre · agrega lo suyo",
              recompensa="xp 10, oro 10",
              escena="""
                  En el fondo del Astillero hay un árbol genealógico pintado en la pared: arriba la **Embarcación**, y de ella salen el **Velero** y el **Remolcador**. Nilo copió en el velero todo lo de la embarcación, y en la copia se olvidó el método que presenta al barco.
              """,
              sugiere="Con `class Velero extends Embarcacion` el velero hereda todo de la embarcación, incluida `presentar()`. Solo agrega lo suyo: las velas.",
              desafio="Hacé que `Velero` herede de `Embarcacion`.",
              inicial='''
                  <?php
                  class Embarcacion
                  {
                      public function __construct(public string $nombre)
                      {
                      }

                      public function presentar(): string
                      {
                          return "Soy {$this->nombre}";
                      }
                  }

                  class Velero
                  {
                      public int $velas = 3;
                  }

                  $v = new Velero('Brisa');
                  echo $v->presentar() . " y tengo {$v->velas} velas\\n";
              ''',
              solucion='''
                  <?php
                  class Embarcacion
                  {
                      public function __construct(public string $nombre)
                      {
                      }

                      public function presentar(): string
                      {
                          return "Soy {$this->nombre}";
                      }
                  }

                  class Velero extends Embarcacion
                  {
                      public int $velas = 3;
                  }

                  $v = new Velero('Brisa');
                  echo $v->presentar() . " y tengo {$v->velas} velas\\n";
              ''',
              al_superar="El velero se presenta como cualquier embarcación y, además, muestra sus velas. Nilo pregunta dónde va la gaviota en el árbol. Nadie le contesta.",
              imagen=["Una pared de madera con un árbol genealógico pintado: arriba un casco de barco simple y abajo un velero y un remolcador, sin letras.",
                      NILO + " señala la rama del velero.", GHECO + " sobre la rama de arriba."]),
            m(id="R02-N04-P2", titulo="parent::",
              lugar=ARBOL, personajes="Nilo, Gheco",
              carta="parent:: | parent::__construct($nombre) llama al constructor del padre · parent::presentar() reusa su método",
              recompensa="xp 15, oro 15",
              escena="""
                  El Remolcador tiene un constructor propio, para su cuerda de arrastre, y se olvidó de llamar al del padre: el remolcador salió sin nombre.
              """,
              sugiere="Dentro del constructor del hijo, `parent::__construct($nombre);` le pasa el nombre al padre. Y `parent::presentar()` reusa lo que el padre ya sabe decir.",
              desafio="Llamá al constructor del padre y reusá su `presentar()`.",
              inicial='''
                  <?php
                  class Embarcacion
                  {
                      protected string $nombre = '(sin nombre)';

                      public function __construct(string $nombre)
                      {
                          $this->nombre = $nombre;
                      }

                      public function presentar(): string
                      {
                          return "Soy {$this->nombre}";
                      }
                  }

                  class Remolcador extends Embarcacion
                  {
                      public function __construct(string $nombre, private int $cuerda)
                      {
                      }

                      public function presentar(): string
                      {
                          return "Arrastro con {$this->cuerda} m de cuerda";
                      }
                  }

                  echo (new Remolcador('Forzudo', 40))->presentar() . "\\n";
              ''',
              solucion='''
                  <?php
                  class Embarcacion
                  {
                      protected string $nombre = '(sin nombre)';

                      public function __construct(string $nombre)
                      {
                          $this->nombre = $nombre;
                      }

                      public function presentar(): string
                      {
                          return "Soy {$this->nombre}";
                      }
                  }

                  class Remolcador extends Embarcacion
                  {
                      public function __construct(string $nombre, private int $cuerda)
                      {
                          parent::__construct($nombre);
                      }

                      public function presentar(): string
                      {
                          return parent::presentar() . " y arrastro con {$this->cuerda} m de cuerda";
                      }
                  }

                  echo (new Remolcador('Forzudo', 40))->presentar() . "\\n";
              ''',
              al_superar="El Forzudo se presenta con nombre y cuerda. Remolca al velero de Nilo, que se había quedado sin viento.",
              imagen=["Un remolcador robusto tirando con una cuerda gruesa de un velero chico en la bahía del astillero.",
                      NILO + " saluda desde el velero.", GHECO + " sobre la cuerda."]),
            m(id="R02-N04-P3", titulo="Es un o tiene un",
              lugar=ARBOL, personajes="Nilo, Iara, Gheco",
              carta="Herencia o no | «un velero ES una embarcación» → extends · «un barco TIENE un capitán» → propiedad · si no es «es un», no se hereda",
              recompensa="xp 10, oro 10",
              escena="""
                  Nilo hizo que `Capitan` herede de `Barco` «para tener el nombre del barco a mano». Ahora el capitán tiene calado y se puede amarrar. Iara lo mira con la ceja levantada.
              """,
              sugiere="Un capitán no **es** un barco: el barco **tiene** un capitán. Sacá el `extends` y guardá el capitán como una propiedad del barco.",
              desafio="Rearmá las clases: el barco tiene un capitán.",
              inicial='''
                  <?php
                  class Barco
                  {
                      public float $calado = 4;

                      public function __construct(public string $nombre)
                      {
                      }
                  }

                  class Capitan extends Barco
                  {
                      public string $persona = 'Marina';
                  }

                  $c = new Capitan('Gaviota');
                  echo "{$c->persona} tiene calado {$c->calado}\\n";
              ''',
              solucion='''
                  <?php
                  class Capitan
                  {
                      public function __construct(public string $persona)
                      {
                      }
                  }

                  class Barco
                  {
                      public float $calado = 4;

                      public function __construct(public string $nombre, public Capitan $capitan)
                      {
                      }
                  }

                  $b = new Barco('Gaviota', new Capitan('Marina'));
                  echo "{$b->nombre} tiene capitana: {$b->capitan->persona}\\n";
              ''',
              al_superar="La capitana Marina se baja del agua, donde la habían amarrado por error, y sube a su barco.",
              imagen=["Una capitana de barco subiendo por una escalerita a la cubierta de un velero en el astillero.",
                      IARA + " anota con la ceja levantada.", NILO + " le tiende la mano a la capitana.", GHECO + " sobre la baranda."]),
            m(id="R02-N04-P4", titulo="final",
              lugar=ARBOL, personajes="Nilo, Elefa, Gheco",
              carta="final | final class: no se hereda · final public function: no se redefine · para lo que no tiene que cambiar",
              recompensa="xp 15, oro 15",
              escena="""
                  Un aprendiz creó un `BarcoGratis` que hereda de `Tarifa` y redefine el precio a cero. Elefa se enteró. —Hay cosas que no se heredan para cambiarlas —dice, y golpea el piso con el bastón.
              """,
              sugiere="Marcá el método `precio()` como `final` para que ninguna hija lo pueda redefinir, y sacá la clase que lo pisa.",
              desafio="Protegé el cálculo de la tarifa con `final` y usá la tarifa de verdad.",
              inicial='''
                  <?php
                  class Tarifa
                  {
                      public function precio(int $kilos): int
                      {
                          return $kilos * 3 + 10;
                      }
                  }

                  class BarcoGratis extends Tarifa
                  {
                      public function precio(int $kilos): int
                      {
                          return 0;
                      }
                  }

                  $t = new BarcoGratis();
                  echo "A pagar: " . $t->precio(20) . "\\n";
              ''',
              solucion='''
                  <?php
                  class Tarifa
                  {
                      final public function precio(int $kilos): int
                      {
                          return $kilos * 3 + 10;
                      }
                  }

                  $t = new Tarifa();
                  echo "A pagar: " . $t->precio(20) . "\\n";
              ''',
              al_superar="La tarifa vuelve a ser la misma para todos. El aprendiz paga lo que debe. Elefa no dice nada, pero la campana suena una vez.",
              imagen=["Una oficina del astillero con un cofre de sellos cerrado con un candado de bronce con forma de sello.",
                      ELEFA + " golpea el piso con el bastón.", NILO + " cierra el candado.", GHECO + " sobre el cofre."]),
        ],
    },
    {
        "titulo": "R02-N05 · Clases abstractas y polimorfismo",
        "misiones": [
            m(id="R02-N05-P1", titulo="Terminá tu pieza",
              lugar=CAPATAZ, personajes="Nilo, Gheco",
              carta="abstract | abstract class Pieza · abstract public function terminar(): string; · no se instancia · cada hija la completa",
              recompensa="xp 10, oro 10",
              escena="""
                  El capataz del Astillero le dice a cada carpintero lo mismo: *«Terminá tu pieza»*. Cada uno sabe cómo se termina la suya. Nilo corre entre los talleres llevando la orden, y por primera vez no tiene que explicar nada.
              """,
              sugiere="Una clase `abstract` declara el método sin escribirlo; cada hija lo escribe. Faltan la `Vela` y el `Ancla`.",
              desafio="Escribí las clases hijas para que cada pieza se termine a su manera.",
              inicial='''
                  <?php
                  abstract class Pieza
                  {
                      abstract public function terminar(): string;
                  }

                  class Casco extends Pieza
                  {
                      public function terminar(): string
                      {
                          return "Casco: lijado";
                      }
                  }

                  $piezas = [new Casco()];
                  foreach ($piezas as $p) {
                      echo $p->terminar() . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  abstract class Pieza
                  {
                      abstract public function terminar(): string;
                  }

                  class Casco extends Pieza
                  {
                      public function terminar(): string
                      {
                          return "Casco: lijado";
                      }
                  }

                  class Vela extends Pieza
                  {
                      public function terminar(): string
                      {
                          return "Vela: cosida";
                      }
                  }

                  class Ancla extends Pieza
                  {
                      public function terminar(): string
                      {
                          return "Ancla: forjada";
                      }
                  }

                  $piezas = [new Casco(), new Vela(), new Ancla()];
                  foreach ($piezas as $p) {
                      echo $p->terminar() . "\\n";
                  }
              ''',
              al_superar="Tres piezas, una sola orden. El capataz no necesita saber cómo se cose una vela.",
              imagen=["Tres talleres del astillero lado a lado: uno con un casco de madera, otro con una vela grande y otro con un ancla en la fragua.",
                      NILO + " corre entre los talleres con un papel en la mano.", GHECO + " sobre su gorra."]),
            m(id="R02-N05-P2", titulo="Adiós a los if por tipo",
              lugar=CAPATAZ, personajes="Nilo, Gheco",
              criatura="ogro",
              carta="Polimorfismo | en vez de if ($x instanceof A) … elseif (B) … · cada clase sabe su respuesta · se agrega una clase, no un if",
              recompensa="xp 15, oro 15",
              escena="""
                  La función de Nilo para calcular la tarifa de amarre tiene un `if` por cada tipo de barco. Llegó un tipo nuevo, la balsa, y como nadie agregó su `if`, pagó cero. Un **ogro** se ríe desde la balsa.
              """,
              sugiere="Que cada barco sepa su propia tarifa: un método `amarre()` en cada clase. Así la función solo pregunta `$b->amarre()`.",
              desafio="Reemplazá el `if` por tipo por un método en cada clase, y agregá la `Balsa` (paga 5).",
              inicial='''
                  <?php
                  abstract class Barco
                  {
                  }

                  class Velero extends Barco
                  {
                  }

                  class Carguero extends Barco
                  {
                  }

                  class Balsa extends Barco
                  {
                  }

                  function amarre(Barco $b): int
                  {
                      if ($b instanceof Velero) {
                          return 20;
                      } elseif ($b instanceof Carguero) {
                          return 90;
                      }
                      return 0;
                  }

                  foreach ([new Velero(), new Carguero(), new Balsa()] as $b) {
                      echo get_class($b) . ": " . amarre($b) . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  abstract class Barco
                  {
                      abstract public function amarre(): int;
                  }

                  class Velero extends Barco
                  {
                      public function amarre(): int
                      {
                          return 20;
                      }
                  }

                  class Carguero extends Barco
                  {
                      public function amarre(): int
                      {
                          return 90;
                      }
                  }

                  class Balsa extends Barco
                  {
                      public function amarre(): int
                      {
                          return 5;
                      }
                  }

                  foreach ([new Velero(), new Carguero(), new Balsa()] as $b) {
                      echo get_class($b) . ": " . $b->amarre() . "\\n";
                  }
              ''',
              al_superar="La balsa paga sus cinco sellos. El ogro se baja de la balsa, mojado y sin chiste.",
              imagen=["Una balsa de troncos amarrada al lado de un velero y un carguero en el astillero.",
                      "Un ogro sentado en la balsa, riéndose.", NILO + " le muestra un papel con un sello.", GHECO + " sobre un tronco."]),
            m(id="R02-N05-P3", titulo="El método plantilla",
              lugar=CAPATAZ, personajes="Nilo, Iara, Gheco",
              carta="Método plantilla | el padre fija los pasos en un método final · las hijas completan solo el paso que cambia",
              recompensa="xp 15, oro 15",
              escena="""
                  Todos los barcos se botan igual: se revisan, se pintan y se echan al agua. Solo la pintura cambia. Nilo escribió los tres pasos en cada clase y en una se olvidó de revisar. Iara encuentra el barco sin revisar flotando torcido.
              """,
              sugiere="El padre tiene `botar()` con los tres pasos en orden y un paso abstracto, `pintar()`, que cada hija completa.",
              desafio="Escribí `botar()` en la clase padre y dejá a las hijas solo con su pintura.",
              inicial='''
                  <?php
                  abstract class Barco
                  {
                      abstract protected function pintar(): string;
                  }

                  class Velero extends Barco
                  {
                      protected function pintar(): string
                      {
                          return "blanco";
                      }

                      public function botar(): void
                      {
                          echo "Pintado de " . $this->pintar() . ". Al agua.\\n";
                      }
                  }

                  (new Velero())->botar();
              ''',
              solucion='''
                  <?php
                  abstract class Barco
                  {
                      abstract protected function pintar(): string;

                      final public function botar(): void
                      {
                          echo "Revisado.\\n";
                          echo "Pintado de " . $this->pintar() . ".\\n";
                          echo "Al agua.\\n";
                      }
                  }

                  class Velero extends Barco
                  {
                      protected function pintar(): string
                      {
                          return "blanco";
                      }
                  }

                  class Gaviota extends Barco
                  {
                      protected function pintar(): string
                      {
                          return "violeta";
                      }
                  }

                  (new Velero())->botar();
                  (new Gaviota())->botar();
              ''',
              al_superar="Los dos barcos se botan revisados. El violeta, por supuesto, es el de Nilo.",
              imagen=["Una grada del astillero con un barco violeta deslizándose al agua y otro blanco esperando su turno.",
                      IARA + " tilda una lista.", NILO + " festeja con los brazos arriba.", GHECO + " sobre la grada."]),
        ],
    },
]
