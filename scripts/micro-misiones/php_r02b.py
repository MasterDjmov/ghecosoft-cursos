from genphp import m
from php_r01 import NILO, ELEFA, IARA, PICO, GHECO

ADUANA = "La aduana del Astillero"
PLANOS = "El cajón de los planos viejos"
PASAJES = "El despacho de pasajes"
GRUA = "La Grúa de la Tormenta"
SELLOS = "Los moldes con sello"
MOLDES_VIEJOS = "El fondo de los moldes viejos"
GOLEM = "el Gólem del Astillero (gigante hecho de tablas de barco, clavos torcidos y sogas, con un timón incrustado en el pecho, un brazo más largo que el otro y ojos de brasa violeta)"

NODOS = [
    {
        "titulo": "R02-N06 · Interfaces",
        "misiones": [
            m(id="R02-N06-P1", titulo="Todo lo que se carga tiene peso",
              lugar=ADUANA, personajes="Nilo, Gheco",
              carta="interface | interface ConPeso { public function peso(): float; } · class Cajon implements ConPeso · un contrato que se firma",
              recompensa="xp 10, oro 10",
              escena="""
                  En la aduana del Astillero hay un cartel: *«Todo lo que se cargue en un barco tiene que tener peso»*. Un cajón de fruta y un pasajero no se parecen en nada, pero los dos tienen que poder decir cuánto pesan.
              """,
              sugiere="Una interfaz es un contrato: `interface ConPeso { public function peso(): float; }`. Cada clase que la firma con `implements` tiene que escribir `peso()`.",
              desafio="Hacé que `Cajon` y `Pasajero` firmen el contrato `ConPeso`.",
              inicial='''
                  <?php
                  interface ConPeso
                  {
                      public function peso(): float;
                  }

                  class Cajon
                  {
                      public function __construct(private float $kilos)
                      {
                      }
                  }

                  class Pasajero
                  {
                      public function __construct(private string $nombre, private float $kilos)
                      {
                      }
                  }

                  function cargaTotal(ConPeso ...$cosas): float
                  {
                      $total = 0;
                      foreach ($cosas as $c) {
                          $total += $c->peso();
                      }
                      return $total;
                  }

                  echo "Carga: " . cargaTotal(new Cajon(40), new Pasajero('Olmo', 72.5)) . " kg\\n";
              ''',
              solucion='''
                  <?php
                  interface ConPeso
                  {
                      public function peso(): float;
                  }

                  class Cajon implements ConPeso
                  {
                      public function __construct(private float $kilos)
                      {
                      }

                      public function peso(): float
                      {
                          return $this->kilos;
                      }
                  }

                  class Pasajero implements ConPeso
                  {
                      public function __construct(private string $nombre, private float $kilos)
                      {
                      }

                      public function peso(): float
                      {
                          return $this->kilos;
                      }
                  }

                  function cargaTotal(ConPeso ...$cosas): float
                  {
                      $total = 0;
                      foreach ($cosas as $c) {
                          $total += $c->peso();
                      }
                      return $total;
                  }

                  echo "Carga: " . cargaTotal(new Cajon(40), new Pasajero('Olmo', 72.5)) . " kg\\n";
              ''',
              al_superar="El cajón y el pasajero suben al mismo barco, sin tener nada en común salvo el contrato. Olmo pregunta por qué lo pesaron. Nadie le explica.",
              imagen=["La aduana del astillero con una balanza grande y un cartel liso con el dibujo de una balanza, sin letras.",
                      "Un pasajero parado en la balanza al lado de un cajón de fruta.", NILO + " mira la aguja.", GHECO + " sobre el cartel."]),
            m(id="R02-N06-P2", titulo="Dos contratos a la vez",
              lugar=ADUANA, personajes="Nilo, Pico, Gheco",
              criatura="esqueleto",
              carta="Varias interfaces | class Cuadro implements ConPeso, ConValor · una clase puede firmar muchas · un parámetro pide solo la que usa",
              recompensa="xp 15, oro 15",
              escena="""
                  Para asegurar algo, la aduana pide que tenga **valor**. Un cuadro tiene peso y valor; Pico, que intenta subir a un barco, no tiene ninguno de los dos. El programa de Nilo intenta asegurar a Pico y salta un **esqueleto**: el método que no existe.
              """,
              sugiere="`Cuadro` firma los dos contratos: `implements ConPeso, ConValor`. La función `asegurar` pide un `ConValor`: a Pico, que no firma nada, no se le puede pasar.",
              desafio="Hacé que `Cuadro` firme `ConValor` y asegurá solo lo que tiene valor.",
              inicial='''
                  <?php
                  interface ConPeso
                  {
                      public function peso(): float;
                  }

                  interface ConValor
                  {
                      public function valor(): int;
                  }

                  class Cuadro implements ConPeso
                  {
                      public function peso(): float
                      {
                          return 3.5;
                      }
                  }

                  class Gaviota
                  {
                  }

                  function asegurar($cosa): string
                  {
                      return "Seguro por " . ($cosa->valor() * 2) . " sellos";
                  }

                  echo asegurar(new Cuadro()) . "\\n";
                  echo asegurar(new Gaviota()) . "\\n";
              ''',
              solucion='''
                  <?php
                  interface ConPeso
                  {
                      public function peso(): float;
                  }

                  interface ConValor
                  {
                      public function valor(): int;
                  }

                  class Cuadro implements ConPeso, ConValor
                  {
                      public function peso(): float
                      {
                          return 3.5;
                      }

                      public function valor(): int
                      {
                          return 400;
                      }
                  }

                  class Gaviota
                  {
                  }

                  function asegurar(ConValor $cosa): string
                  {
                      return "Seguro por " . ($cosa->valor() * 2) . " sellos";
                  }

                  echo asegurar(new Cuadro()) . "\\n";
                  $pico = new Gaviota();
                  echo $pico instanceof ConValor ? asegurar($pico) : "Pico: no se asegura\\n";
              ''',
              al_superar="El cuadro queda asegurado. Pico, sin seguro, se va volando ofendida con el cartel de la aduana en el pico.",
              imagen=["Un cuadro envuelto en papel madera sobre el mostrador de la aduana, con un sello de lacre violeta.",
                      PICO + " intenta pararse en el mostrador.", NILO + " la ataja con las manos.", "Un esqueleto chiquito asoma detrás del mostrador.", GHECO + " sobre el cuadro."]),
            m(id="R02-N06-P3", titulo="Countable",
              lugar=ADUANA, personajes="Nilo, Iara, Gheco",
              carta="Interfaces de PHP | Countable → count($obj) · Stringable → __toString · JsonSerializable → json_encode($obj)",
              recompensa="xp 15, oro 15",
              escena="""
                  Iara lleva la lista de cosas de la bodega de un barco en un objeto `Bodega`. Quiere preguntar `count($bodega)` como con cualquier array, pero PHP no sabe contar un objeto.
              """,
              sugiere="Si `Bodega` implementa `Countable` (que trae PHP) y escribe `count(): int`, la función `count($bodega)` la usa.",
              desafio="Hacé que la bodega se pueda contar con `count()`.",
              inicial='''
                  <?php
                  class Bodega
                  {
                      private array $cosas = [];

                      public function guardar(string $cosa): void
                      {
                          $this->cosas[] = $cosa;
                      }
                  }

                  $b = new Bodega();
                  $b->guardar('harina');
                  $b->guardar('sal');
                  $b->guardar('aceite');
                  echo "En la bodega: " . (is_countable($b) ? count($b) : '?') . "\\n";
              ''',
              solucion='''
                  <?php
                  class Bodega implements Countable
                  {
                      private array $cosas = [];

                      public function guardar(string $cosa): void
                      {
                          $this->cosas[] = $cosa;
                      }

                      public function count(): int
                      {
                          return count($this->cosas);
                      }
                  }

                  $b = new Bodega();
                  $b->guardar('harina');
                  $b->guardar('sal');
                  $b->guardar('aceite');
                  echo "En la bodega: " . (is_countable($b) ? count($b) : '?') . "\\n";
              ''',
              al_superar="Tres cosas en la bodega, contadas como se cuenta cualquier lista. Iara lo anota sin levantar la vista.",
              imagen=["La bodega de un barco con tres estantes: harina, sal y aceite.",
                      IARA + " cuenta con el lápiz.", NILO + " sostiene un farol.", GHECO + " sobre una bolsa."]),
        ],
    },
    {
        "titulo": "R02-N07 · Traits y composición",
        "misiones": [
            m(id="R02-N07-P1", titulo="Un bote tiene un motor",
              lugar=PLANOS, personajes="Nilo, Gheco",
              carta="Composición | el bote TIENE un motor: __construct(private Motor $motor) · se puede cambiar por otro · delegar: $this->motor->arrancar()",
              recompensa="xp 10, oro 10",
              escena="""
                  Un aprendiz dibujó un bote que **es** un motor con casco. El maestro carpintero le borró el dibujo: *«Un bote no es un motor. Un bote tiene un motor. Y mañana le vas a querer poner uno más grande.»*
              """,
              sugiere="El bote recibe su motor por el constructor y le **delega** el trabajo: `$this->motor->arrancar()`. Cambiar el motor es pasar otro objeto.",
              desafio="Rearmá el bote para que tenga un motor y pruébalo con dos motores distintos.",
              inicial='''
                  <?php
                  class Motor
                  {
                      public function __construct(private int $caballos)
                      {
                      }

                      public function arrancar(): string
                      {
                          return "brrr ({$this->caballos} HP)";
                      }
                  }

                  class Bote extends Motor
                  {
                  }

                  echo (new Bote(10))->arrancar() . "\\n";
              ''',
              solucion='''
                  <?php
                  class Motor
                  {
                      public function __construct(private int $caballos)
                      {
                      }

                      public function arrancar(): string
                      {
                          return "brrr ({$this->caballos} HP)";
                      }
                  }

                  class Bote
                  {
                      public function __construct(private string $nombre, private Motor $motor)
                      {
                      }

                      public function salir(): string
                      {
                          return "{$this->nombre}: " . $this->motor->arrancar();
                      }
                  }

                  echo (new Bote('Gaviota', new Motor(10)))->salir() . "\\n";
                  echo (new Bote('Gaviota', new Motor(40)))->salir() . "\\n";
              ''',
              al_superar="El bote de Nilo estrena motor grande sin que nadie toque el bote. Sale disparado y vuelve, mojado y feliz.",
              imagen=["Un bote violeta con un motor fuera de borda nuevo, saliendo rápido del astillero y levantando espuma.",
                      NILO + " al timón, con la bufanda al viento.", GHECO + " agarrado a la gorra."]),
            m(id="R02-N07-P2", titulo="La etiqueta de fecha",
              lugar=PLANOS, personajes="Nilo, Gheco",
              carta="trait | trait ConFabricacion { … } · use ConFabricacion; en cada clase · pega el mismo código en clases sin relación",
              recompensa="xp 15, oro 15",
              escena="""
                  Del otro lado del taller, un herrero pega la misma etiqueta de fecha de fabricación en todas las piezas: velas, remos, anclas. Nilo copió el método `etiqueta()` en cada clase, y en el remo se le escapó una falta de ortografía.
              """,
              sugiere="Un `trait` guarda el método una sola vez; cada clase lo incorpora con `use ConFabricacion;`.",
              desafio="Pasá el método repetido a un trait y usalo en las dos clases.",
              inicial='''
                  <?php
                  class Vela
                  {
                      public string $fecha = '2026-10-03';

                      public function etiqueta(): string
                      {
                          return static::class . " - fabricación: {$this->fecha}";
                      }
                  }

                  class Remo
                  {
                      public string $fecha = '2026-10-05';

                      public function etiqueta(): string
                      {
                          return static::class . " - fabricasion: {$this->fecha}";
                      }
                  }

                  echo (new Vela())->etiqueta() . "\\n";
                  echo (new Remo())->etiqueta() . "\\n";
              ''',
              solucion='''
                  <?php
                  trait ConFabricacion
                  {
                      public function etiqueta(): string
                      {
                          return static::class . " - fabricación: {$this->fecha}";
                      }
                  }

                  class Vela
                  {
                      use ConFabricacion;

                      public string $fecha = '2026-10-03';
                  }

                  class Remo
                  {
                      use ConFabricacion;

                      public string $fecha = '2026-10-05';
                  }

                  echo (new Vela())->etiqueta() . "\\n";
                  echo (new Remo())->etiqueta() . "\\n";
              ''',
              al_superar="Las dos etiquetas salen iguales, del mismo molde. El herrero guarda su sello de fechas, contento.",
              imagen=["Un taller del astillero con una vela doblada y un remo apoyados en la pared, cada uno con una etiqueta de madera lisa colgando.",
                      NILO + " cuelga una etiqueta.", GHECO + " sobre el remo."]),
            m(id="R02-N07-P3", titulo="El plano de la barcaza",
              lugar=PLANOS, personajes="Nilo, Elefa, Gheco",
              carta="Inyección | las piezas se reciben por el constructor (no se crean adentro) · así se cambian sin tocar la clase · se puede probar con una pieza de mentira",
              recompensa="xp 15, oro 15",
              escena="""
                  Buscando planos de motores en el cajón de los planos viejos, Nilo encuentra uno raro: **una barcaza hecha para llevar un solo vidrio enorme**, encargada hace veinte años por alguien con las manos manchadas de plomo. En el programa del inventario, la barcaza crea su propia grúa adentro y nadie la puede cambiar por la grúa grande que haría falta para un vidrio así.
              """,
              sugiere="En vez de `new Grua(…)` adentro del constructor, la barcaza **recibe** la grúa: `__construct(private Grua $grua)`. Así se le puede dar la grande.",
              desafio="Hacé que la barcaza reciba su grúa por el constructor y cargá el vidrio con la grande.",
              inicial='''
                  <?php
                  class Grua
                  {
                      public function __construct(public int $toneladas)
                      {
                      }
                  }

                  class Barcaza
                  {
                      private Grua $grua;

                      public function __construct()
                      {
                          $this->grua = new Grua(2);
                      }

                      public function cargar(string $que, int $toneladas): string
                      {
                          return $toneladas <= $this->grua->toneladas
                              ? "Cargado: $que"
                              : "La grua no puede con $que";
                      }
                  }

                  echo (new Barcaza())->cargar('un vidrio enorme', 9) . "\\n";
              ''',
              solucion='''
                  <?php
                  class Grua
                  {
                      public function __construct(public int $toneladas)
                      {
                      }
                  }

                  class Barcaza
                  {
                      public function __construct(private Grua $grua)
                      {
                      }

                      public function cargar(string $que, int $toneladas): string
                      {
                          return $toneladas <= $this->grua->toneladas
                              ? "Cargado: $que"
                              : "La grua no puede con $que";
                      }
                  }

                  echo (new Barcaza(new Grua(2)))->cargar('un vidrio enorme', 9) . "\\n";
                  echo (new Barcaza(new Grua(10)))->cargar('un vidrio enorme', 9) . "\\n";
              ''',
              al_superar="Con la grúa grande, el vidrio entra en la barcaza. En la esquina del plano hay un dibujo: un vitral. Elefa guarda el plano en su armadura sin decir nada.",
              imagen=["Un cajón de planos viejos abierto con un plano amarillento desplegado de una barcaza que lleva un vidrio enorme de colores, sin letras.",
                      NILO + " sostiene el plano a la luz de un farol.", ELEFA + " detrás, en sombra.", GHECO + " sobre el cajón."]),
        ],
    },
    {
        "titulo": "R02-N08 · Enums y fechas",
        "misiones": [
            m(id="R02-N08-P1", titulo="Pagado, Pagada, PAG",
              lugar=PASAJES, personajes="Nilo, Iara, Gheco",
              carta="enum | enum Estado: string { case Pagada = 'pagada'; case Pendiente = 'pendiente'; } · solo esos valores · Estado::from('pagada')",
              recompensa="xp 10, oro 10",
              escena="""
                  En el despacho de pasajes, cada empleado anotaba el estado de las reservas como le parecía: *«pagado»*, *«Pagada»*, *«PAG»*. Iara las contó tres veces y le dio tres números distintos. Es la primera vez que Nilo la ve perder la paciencia.
              """,
              sugiere="Con un enum, el estado solo puede ser uno de los casos. `Estado::tryFrom($texto)` da el caso, o `null` si el texto no es válido.",
              desafio="Contá cuántas reservas están pagadas usando el enum, y avisá las que no se entienden.",
              inicial='''
                  <?php
                  enum Estado: string
                  {
                      case Pagada = 'pagada';
                      case Pendiente = 'pendiente';
                  }

                  $anotadas = ['pagada', 'Pagada', 'pendiente', 'PAG', 'pagada'];
                  $pagadas = 0;
                  foreach ($anotadas as $texto) {
                      if (str_starts_with(strtolower($texto), 'pag')) {
                          $pagadas++;
                      }
                  }
                  echo "Pagadas: $pagadas\\n";
              ''',
              solucion='''
                  <?php
                  enum Estado: string
                  {
                      case Pagada = 'pagada';
                      case Pendiente = 'pendiente';
                  }

                  $anotadas = ['pagada', 'Pagada', 'pendiente', 'PAG', 'pagada'];
                  $pagadas = 0;
                  foreach ($anotadas as $texto) {
                      $estado = Estado::tryFrom($texto);
                      if ($estado === null) {
                          echo "No se entiende: $texto\\n";
                      } elseif ($estado === Estado::Pagada) {
                          $pagadas++;
                      }
                  }
                  echo "Pagadas: $pagadas\\n";
              ''',
              al_superar="Dos pagadas seguras y dos para revisar. Iara respira hondo y vuelve a ser Iara.",
              imagen=["El mostrador de un despacho de pasajes de barco con pilas de boletos y sellos de colores, sin letras.",
                      IARA + " con el pelo un poco despeinado, revolviendo papeles.", NILO + " le alcanza un sello.", GHECO + " sobre una pila de boletos."]),
            m(id="R02-N08-P2", titulo="El enum que sabe cosas",
              lugar=PASAJES, personajes="Nilo, Gheco",
              carta="Métodos en enums | public function etiqueta(): string { return match ($this) { … }; } · cases() lista todos",
              recompensa="xp 15, oro 15",
              escena="""
                  Cada clase de pasaje tiene su precio: cubierta, camarote y suite. Nilo escribió los precios en un `if` aparte, lejos del enum, y al agregar la suite se olvidó de ponerle precio.
              """,
              sugiere="El enum puede tener métodos: `precio()` con un `match ($this)` que cubra todos los casos. Si falta uno, `match` falla en lugar de dar cero.",
              desafio="Escribí el método `precio` en el enum y recorré todos los casos con `cases()`.",
              inicial='''
                  <?php
                  enum Clase
                  {
                      case Cubierta;
                      case Camarote;
                      case Suite;
                  }

                  function precio(Clase $c): int
                  {
                      if ($c === Clase::Cubierta) {
                          return 30;
                      }
                      if ($c === Clase::Camarote) {
                          return 80;
                      }
                      return 0;
                  }

                  foreach (Clase::cases() as $c) {
                      echo $c->name . ": " . precio($c) . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  enum Clase
                  {
                      case Cubierta;
                      case Camarote;
                      case Suite;

                      public function precio(): int
                      {
                          return match ($this) {
                              Clase::Cubierta => 30,
                              Clase::Camarote => 80,
                              Clase::Suite => 200,
                          };
                      }
                  }

                  foreach (Clase::cases() as $c) {
                      echo $c->name . ": " . $c->precio() . "\\n";
                  }
              ''',
              al_superar="La suite cuesta lo que tiene que costar. Un turista que había reservado la suite gratis se lleva un disgusto.",
              imagen=["Un ferry de pasajeros en el puerto con tres niveles de ventanas, de las más chicas abajo a las más grandes arriba.",
                      NILO + " señala el piso de arriba.", GHECO + " sobre la chimenea."]),
            m(id="R02-N08-P3", titulo="Diez días después",
              lugar=PASAJES, personajes="Nilo, Iara, Gheco",
              carta="Fechas | new DateTimeImmutable('2026-10-03') · ->modify('+10 days') · ->format('d/m/Y') · inmutable: devuelve una fecha nueva",
              recompensa="xp 15, oro 15",
              escena="""
                  Un barco sale el 3 de octubre y vuelve diez días después. Nilo sumó 10 al día y le dio el 13… de un mes con cuarenta días. Iara tiene el calendario en la libreta y no le da.
              """,
              sugiere="Con `DateTimeImmutable` las fechas se suman bien: `$salida->modify('+10 days')` devuelve otra fecha, y `format('d/m/Y')` la muestra.",
              desafio="Calculá la vuelta con `modify` y mostrá las dos fechas con formato.",
              inicial='''
                  <?php
                  $salida = '2026-10-28';
                  [$anio, $mes, $dia] = explode('-', $salida);
                  $vuelta = ($dia + 10) . "/$mes/$anio";
                  echo "Sale: $dia/$mes/$anio\\n";
                  echo "Vuelve: $vuelta\\n";
              ''',
              solucion='''
                  <?php
                  $salida = new DateTimeImmutable('2026-10-28');
                  $vuelta = $salida->modify('+10 days');
                  echo "Sale: " . $salida->format('d/m/Y') . "\\n";
                  echo "Vuelve: " . $vuelta->format('d/m/Y') . "\\n";
              ''',
              al_superar="Vuelve el 7 de noviembre, un día que sí existe. Iara cierra el calendario.",
              imagen=["Un calendario de pared en el despacho de pasajes con dos días marcados con sellos de lacre violeta, sin números.",
                      IARA + " marca el calendario.", NILO + " cuenta con los dedos.", GHECO + " sobre el calendario."]),
            m(id="R02-N08-P4", titulo="¿Cuántas noches?",
              lugar=PASAJES, personajes="Nilo, Gheco",
              criatura="goblin",
              carta="diff | $a->diff($b)->days da los días entre dos fechas · DateTimeImmutable::createFromFormat('d/m/Y', $t) valida lo que escribió una persona",
              recompensa="xp 15, oro 15",
              escena="""
                  Un pasajero escribió su llegada como «31/02/2026». El programa de Nilo la aceptó y calculó las noches como pudo: un **goblin** se llevó dos días en el camino.
              """,
              sugiere="`createFromFormat('!d/m/Y', $texto)` lee la fecha; si la fecha no existe, PHP la «corrige» sola (el 31 de febrero pasa a marzo). Compará: si al volver a formatearla no da el mismo texto, era inválida.",
              desafio="Rechazá la fecha inválida y calculá las noches de la válida.",
              inicial='''
                  <?php
                  function noches(string $llegada, string $salida): string
                  {
                      $a = DateTimeImmutable::createFromFormat('!d/m/Y', $llegada);
                      $b = DateTimeImmutable::createFromFormat('!d/m/Y', $salida);
                      return $a->diff($b)->days . " noches";
                  }

                  echo noches('31/02/2026', '05/03/2026') . "\\n";
                  echo noches('01/03/2026', '05/03/2026') . "\\n";
              ''',
              solucion='''
                  <?php
                  function fecha(string $texto): ?DateTimeImmutable
                  {
                      $f = DateTimeImmutable::createFromFormat('!d/m/Y', $texto);
                      return ($f !== false && $f->format('d/m/Y') === $texto) ? $f : null;
                  }

                  function noches(string $llegada, string $salida): string
                  {
                      $a = fecha($llegada);
                      $b = fecha($salida);
                      if ($a === null || $b === null) {
                          return "Fecha invalida";
                      }
                      return $a->diff($b)->days . " noches";
                  }

                  echo noches('31/02/2026', '05/03/2026') . "\\n";
                  echo noches('01/03/2026', '05/03/2026') . "\\n";
              ''',
              al_superar="El 31 de febrero no existe, y ahora el programa lo sabe. El goblin devuelve los dos días.",
              imagen=["Un boleto de barco sobre el mostrador con un casillero de fecha tachado con un sello rojo, sin letras.",
                      "Un goblin se va corriendo con dos hojitas de calendario.", NILO + " sostiene el boleto.", GHECO + " sobre el sello."]),
        ],
    },
    {
        "titulo": "R02-N09 · Excepciones",
        "misiones": [
            m(id="R02-N09-P1", titulo="La grúa trabada",
              lugar=GRUA, personajes="Nilo, Gheco",
              carta="throw | throw new RuntimeException('motivo'); corta y avisa · try { … } catch (RuntimeException $e) { $e->getMessage() }",
              recompensa="xp 10, oro 10",
              escena="""
                  Una noche de tormenta, la grúa del muelle 2 se traba con un contenedor colgando. El programa de la grúa ni se entera: sigue diciendo «todo bien» mientras el contenedor se balancea.
              """,
              sugiere="Si el peso supera lo que aguanta la grúa, `levantar()` tiene que **lanzar** una excepción. Quien la llama la atrapa con `try`/`catch` y avisa.",
              desafio="Lanzá una `RuntimeException` cuando el peso es demasiado y atrapala para avisar.",
              inicial='''
                  <?php
                  function levantar(int $toneladas): string
                  {
                      if ($toneladas > 5) {
                          return "todo bien";
                      }
                      return "Levantado: $toneladas t";
                  }

                  foreach ([3, 8] as $t) {
                      echo levantar($t) . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function levantar(int $toneladas): string
                  {
                      if ($toneladas > 5) {
                          throw new RuntimeException("la grua no aguanta $toneladas t");
                      }
                      return "Levantado: $toneladas t";
                  }

                  foreach ([3, 8] as $t) {
                      try {
                          echo levantar($t) . "\\n";
                      } catch (RuntimeException $e) {
                          echo "Aviso: " . $e->getMessage() . "\\n";
                      }
                  }
              ''',
              al_superar="La grúa avisa a tiempo y el contenedor baja despacio. Nadie termina con un contenedor en la cabeza.",
              imagen=["Una grúa grande de un muelle de noche con tormenta, con un contenedor colgando y relámpagos violetas.",
                      NILO + " le hace señas al operario desde abajo.", GHECO + " sobre la cadena."]),
            m(id="R02-N09-P2", titulo="El salvavidas del finally",
              lugar=GRUA, personajes="Nilo, Gheco",
              carta="finally | try { … } catch (…) { … } finally { … } · lo de finally pasa siempre, falle o no · para asegurar la carga y limpiar",
              recompensa="xp 15, oro 15", item="Salvavidas del finally",
              escena="""
                  Nilo trepa a la grúa para destrabarla, resbala y cae al agua. Lo saca un **salvavidas** que alguien había atado a la grúa «por si acaso». En el protocolo nuevo dice: *antes de irte, asegurá la carga*, pase lo que pase.
              """,
              sugiere="Lo que va en `finally` se ejecuta **siempre**: si todo salió bien y si hubo una excepción. Ahí va «Carga asegurada.».",
              desafio="Mové el aviso de la carga a un `finally` para que aparezca en los dos intentos.",
              inicial='''
                  <?php
                  function maniobrar(int $toneladas): void
                  {
                      try {
                          if ($toneladas > 5) {
                              throw new RuntimeException("se trabo con $toneladas t");
                          }
                          echo "Maniobra lista\\n";
                          echo "Carga asegurada.\\n";
                      } catch (RuntimeException $e) {
                          echo "Fallo: " . $e->getMessage() . "\\n";
                      }
                  }

                  maniobrar(3);
                  maniobrar(9);
              ''',
              solucion='''
                  <?php
                  function maniobrar(int $toneladas): void
                  {
                      try {
                          if ($toneladas > 5) {
                              throw new RuntimeException("se trabo con $toneladas t");
                          }
                          echo "Maniobra lista\\n";
                      } catch (RuntimeException $e) {
                          echo "Fallo: " . $e->getMessage() . "\\n";
                      } finally {
                          echo "Carga asegurada.\\n";
                      }
                  }

                  maniobrar(3);
                  maniobrar(9);
              ''',
              al_superar="Nilo se queda con el salvavidas: **el Salvavidas del `finally`**. Equipado, en cada expedición lo saca una vez del agua.",
              imagen=["El agua oscura y revuelta junto a una grúa de noche, con un salvavidas blanco con franjas violetas atado con una soga.",
                      NILO + " empapado, agarrado al salvavidas, sin gorra.", GHECO + " sentado en el salvavidas, seco."]),
            m(id="R02-N09-P3", titulo="Una excepción con nombre",
              lugar=GRUA, personajes="Nilo, Iara, Gheco",
              carta="Excepciones propias | class SinCupo extends RuntimeException · con datos extra · se atrapa por su nombre: catch (SinCupo $e)",
              recompensa="xp 15, oro 15",
              escena="""
                  Las grúas fallan por muchas cosas: viento, peso, falta de cupo en el barco. Todas lanzan la misma `RuntimeException` y Iara no puede separar en su informe cuántas fueron por falta de cupo.
              """,
              sugiere="Una clase `SinCupo extends RuntimeException` con un dato extra (cuánto faltó). Se atrapa por su nombre antes que las demás.",
              desafio="Creá la excepción `SinCupo` y atrapala aparte para el informe.",
              inicial='''
                  <?php
                  function cargar(string $barco, int $libres, int $cajones): void
                  {
                      if ($cajones > $libres) {
                          throw new RuntimeException("sin cupo en $barco");
                      }
                      echo "$barco: $cajones cajones cargados\\n";
                  }

                  $sinCupo = 0;
                  foreach ([['Gaviota', 10, 4], ['Tortuga', 3, 7], ['Albatros', 5, 9]] as [$b, $l, $c]) {
                      try {
                          cargar($b, $l, $c);
                      } catch (RuntimeException $e) {
                          echo "Error: " . $e->getMessage() . "\\n";
                      }
                  }
                  echo "Por falta de cupo: $sinCupo\\n";
              ''',
              solucion='''
                  <?php
                  class SinCupo extends RuntimeException
                  {
                      public function __construct(public readonly string $barco, public readonly int $faltan)
                      {
                          parent::__construct("sin cupo en $barco");
                      }
                  }

                  function cargar(string $barco, int $libres, int $cajones): void
                  {
                      if ($cajones > $libres) {
                          throw new SinCupo($barco, $cajones - $libres);
                      }
                      echo "$barco: $cajones cajones cargados\\n";
                  }

                  $sinCupo = 0;
                  foreach ([['Gaviota', 10, 4], ['Tortuga', 3, 7], ['Albatros', 5, 9]] as [$b, $l, $c]) {
                      try {
                          cargar($b, $l, $c);
                      } catch (SinCupo $e) {
                          $sinCupo++;
                          echo "{$e->barco}: faltan {$e->faltan} lugares\\n";
                      }
                  }
                  echo "Por falta de cupo: $sinCupo\\n";
              ''',
              al_superar="El informe de Iara sale con su columna de «falta de cupo». La subraya dos veces.",
              imagen=["Un informe de papel sobre un barril en el muelle, con columnas de puntitos de colores, sin letras.",
                      IARA + " subraya una columna con el lápiz.", NILO + " con el salvavidas colgado al hombro.", GHECO + " sobre el barril."]),
        ],
    },
    {
        "titulo": "R02-N10 · Namespaces, autoload y Composer",
        "misiones": [
            m(id="R02-N10-P1", titulo="Dos timones",
              lugar=SELLOS, personajes="Nilo, Gheco",
              criatura="esqueleto",
              carta="namespace | namespace Velero; class Timon {} · \\\\Velero\\\\Timon y \\\\Remolque\\\\Timon conviven · use Velero\\\\Timon;",
              recompensa="xp 10, oro 10",
              escena="""
                  Dos talleres hicieron un molde llamado `Timon`, uno para veleros y otro para remolcadores. Nilo llevó el equivocado a cada taller, dos veces. Ahora cada taller pone su sello en los moldes: `Velero\\Timon` y `Remolque\\Timon`.
              """,
              sugiere="Cada clase va en su `namespace`, como un apellido. En un solo archivo se puede escribir `namespace Velero { … }` y `namespace Remolque { … }`, y usarlas por su nombre completo.",
              desafio="Poné cada `Timon` en su namespace y usá los dos.",
              inicial='''
                  <?php
                  class Timon
                  {
                      public function girar(): string
                      {
                          return "timon de velero";
                      }
                  }

                  class Timon
                  {
                      public function girar(): string
                      {
                          return "timon de remolcador";
                      }
                  }
              ''',
              solucion='''
                  <?php
                  namespace Velero {
                      class Timon
                      {
                          public function girar(): string
                          {
                              return "timon de velero";
                          }
                      }
                  }

                  namespace Remolque {
                      class Timon
                      {
                          public function girar(): string
                          {
                              return "timon de remolcador";
                          }
                      }
                  }

                  namespace {
                      echo (new Velero\\Timon())->girar() . "\\n";
                      echo (new Remolque\\Timon())->girar() . "\\n";
                  }
              ''',
              al_superar="Cada timón a su taller, al primer intento. El esqueleto que había nacido de la confusión se desarma solo.",
              imagen=["Dos timones de madera iguales sobre una mesa, cada uno con un sello de lacre de distinto color colgando.",
                      NILO + " lleva un timón en cada mano.", GHECO + " sobre uno de los timones."]),
            m(id="R02-N10-P2", titulo="El bibliotecario de moldes",
              lugar=SELLOS, personajes="Nilo, Gheco",
              carta="Autoload | spl_autoload_register(fn ($clase) => require __DIR__ . '/src/' . str_replace('\\\\\\\\', '/', $clase) . '.php') · trae cada clase cuando se usa",
              recompensa="xp 15, oro 15",
              escena="""
                  En la entrada del Astillero hay un bibliotecario que, cuando alguien pide un molde, sabe en qué estante buscarlo. El programa de Nilo, en cambio, tiene un `require` por cada molde, y se olvidó uno.
              """,
              sugiere="`spl_autoload_register` recibe una función que, dado el nombre de la clase, hace el `require` del archivo que corresponde. Así no hace falta un `require` por clase.",
              desafio="Registrá el autoload para que encuentre las clases en la carpeta `src/`.",
              inicial='''
                  <?php
                  @mkdir('src');
                  file_put_contents('src/Ancla.php', '<?php class Ancla { public function bajar(): string { return "ancla abajo"; } }');
                  file_put_contents('src/Vela.php', '<?php class Vela { public function izar(): string { return "vela arriba"; } }');

                  require 'src/Ancla.php';

                  echo (new Ancla())->bajar() . "\\n";
                  echo (new Vela())->izar() . "\\n";
              ''',
              solucion='''
                  <?php
                  @mkdir('src');
                  file_put_contents('src/Ancla.php', '<?php class Ancla { public function bajar(): string { return "ancla abajo"; } }');
                  file_put_contents('src/Vela.php', '<?php class Vela { public function izar(): string { return "vela arriba"; } }');

                  spl_autoload_register(function (string $clase): void {
                      require 'src/' . $clase . '.php';
                  });

                  echo (new Ancla())->bajar() . "\\n";
                  echo (new Vela())->izar() . "\\n";
              ''',
              al_superar="Cada molde aparece cuando se lo nombra. El bibliotecario del Astillero le guiña un ojo a Nilo: colega.",
              imagen=["Un bibliotecario anciano en la entrada del astillero frente a estantes con moldes de madera, cada uno con un sello.",
                      NILO + " le pide un molde.", GHECO + " sobre el estante."]),
            m(id="R02-N10-P3", titulo="Apellido y carpeta",
              lugar=SELLOS, personajes="Nilo, Iara, Gheco",
              carta="PSR-4 | la clase Puerto\\\\Muelle\\\\Grua va en src/Muelle/Grua.php · el namespace es la carpeta · Composer arma el autoload con esta regla",
              recompensa="xp 15, oro 15",
              escena="""
                  Iara propone una regla para que nadie se pierda: el apellido de cada molde dice en qué carpeta está. `Puerto\\Muelle\\Grua` va en `src/Muelle/Grua.php`. Es la misma regla que usa Composer.
              """,
              sugiere="En el autoload, sacá el prefijo `Puerto\\` y cambiá las `\\` por `/` para armar la ruta: `str_replace('\\\\', '/', …)`.",
              desafio="Completá el autoload con la regla PSR-4.",
              inicial='''
                  <?php
                  @mkdir('src/Muelle', 0777, true);
                  file_put_contents('src/Muelle/Grua.php', '<?php namespace Puerto\\Muelle; class Grua { public function nombre(): string { return static::class; } }');

                  spl_autoload_register(function (string $clase): void {
                      require 'src/' . $clase . '.php';
                  });

                  echo (new Puerto\\Muelle\\Grua())->nombre() . "\\n";
              ''',
              solucion='''
                  <?php
                  @mkdir('src/Muelle', 0777, true);
                  file_put_contents('src/Muelle/Grua.php', '<?php namespace Puerto\\Muelle; class Grua { public function nombre(): string { return static::class; } }');

                  spl_autoload_register(function (string $clase): void {
                      $relativa = substr($clase, strlen('Puerto\\\\'));
                      require 'src/' . str_replace('\\\\', '/', $relativa) . '.php';
                  });

                  echo (new Puerto\\Muelle\\Grua())->nombre() . "\\n";
              ''',
              al_superar="El molde aparece en su carpeta, como dice su apellido. Iara pega la regla en la puerta del Astillero.",
              imagen=["Un armario de carpetas de madera, unas dentro de otras, con sellos de colores en cada cajón, sin letras.",
                      IARA + " pega un papel en la puerta del armario.", NILO + " abre un cajón.", GHECO + " sobre el armario."]),
        ],
    },
    {
        "titulo": "R02-N11 · Jefe: el Gólem del Astillero",
        "misiones": [
            m(id="R02-N11-P1", titulo="El brazo de tablas sueltas",
              lugar=MOLDES_VIEJOS, personajes="Nilo, Gheco",
              criatura="dragon",
              carta="Encapsular | los datos private · se cambian con métodos que validan · nada de propiedades públicas que cualquiera pisa",
              recompensa="xp 15, oro 15",
              escena="""
                  En el fondo del Astillero, donde se guardan los moldes viejos, se mueve el **Gólem del Astillero**: un gigante de tablas y clavos pegados a las apuradas. Su brazo largo es una clase con todo público: cualquiera le cambia el stock a un número negativo, y el brazo se desarma.
              """,
              sugiere="Hacé `private` el stock y escribí `retirar()`, que no deja sacar más de lo que hay.",
              desafio="Protegé el stock del inventario.",
              inicial='''
                  <?php
                  class Inventario
                  {
                      public int $tablas = 10;
                  }

                  $inv = new Inventario();
                  $inv->tablas -= 4;
                  $inv->tablas -= 9;
                  echo "Tablas: {$inv->tablas}\\n";
              ''',
              solucion='''
                  <?php
                  class Inventario
                  {
                      private int $tablas = 10;

                      public function retirar(int $cantidad): void
                      {
                          if ($cantidad > $this->tablas) {
                              echo "No alcanza: hay {$this->tablas}\\n";
                              return;
                          }
                          $this->tablas -= $cantidad;
                      }

                      public function tablas(): int
                      {
                          return $this->tablas;
                      }
                  }

                  $inv = new Inventario();
                  $inv->retirar(4);
                  $inv->retirar(9);
                  echo "Tablas: " . $inv->tablas() . "\\n";
              ''',
              al_superar="El brazo largo del Gólem se queda quieto, con sus tablas contadas. El Gólem mira el brazo, confundido.",
              imagen=["El fondo oscuro de un astillero con moldes viejos apilados y polvo.",
                      GOLEM + " con el brazo largo trabado.", NILO + " con un martillo de carpintero, frente a él.", GHECO + " sobre un molde."]),
            m(id="R02-N11-P2", titulo="El catch vacío",
              lugar=MOLDES_VIEJOS, personajes="Nilo, Gheco",
              criatura="dragon",
              carta="No esconder errores | un catch vacío los traga · se atrapa lo que se sabe manejar · se avisa con el mensaje · lo demás, que suba",
              recompensa="xp 15, oro 15",
              escena="""
                  En el pecho del Gólem, detrás del timón, hay un `catch` vacío: cada error que le pasa, se lo traga y sigue caminando como si nada. Por eso se le caen las piezas sin que nadie sepa por qué.
              """,
              sugiere="Un `catch` vacío esconde el problema. Mostrá el mensaje de la excepción y contá cuántas piezas fallaron.",
              desafio="Hacé que el `catch` avise el error en lugar de tragárselo.",
              inicial='''
                  <?php
                  function clavar(string $pieza, int $clavos): void
                  {
                      if ($clavos < 2) {
                          throw new InvalidArgumentException("$pieza necesita al menos 2 clavos");
                      }
                      echo "$pieza: firme\\n";
                  }

                  foreach (['timon' => 4, 'brazo' => 1, 'pierna' => 3] as $pieza => $clavos) {
                      try {
                          clavar($pieza, $clavos);
                      } catch (InvalidArgumentException $e) {
                      }
                  }
                  echo "Golem armado\\n";
              ''',
              solucion='''
                  <?php
                  function clavar(string $pieza, int $clavos): void
                  {
                      if ($clavos < 2) {
                          throw new InvalidArgumentException("$pieza necesita al menos 2 clavos");
                      }
                      echo "$pieza: firme\\n";
                  }

                  $fallas = 0;
                  foreach (['timon' => 4, 'brazo' => 1, 'pierna' => 3] as $pieza => $clavos) {
                      try {
                          clavar($pieza, $clavos);
                      } catch (InvalidArgumentException $e) {
                          $fallas++;
                          echo "Falla: " . $e->getMessage() . "\\n";
                      }
                  }
                  echo $fallas === 0 ? "Golem armado\\n" : "Piezas con falla: $fallas\\n";
              ''',
              al_superar="El Gólem se queda quieto, mirándose el brazo flojo. Por primera vez alguien le dice qué le pasa.",
              imagen=["Primer plano del pecho de madera del Gólem, con un timón incrustado que tiene un hueco oscuro en el centro.",
                      NILO + " ilumina el hueco con un farol.", GHECO + " asomado al hueco."]),
            m(id="R02-N11-P3", titulo="Rearmar el Gólem",
              lugar=MOLDES_VIEJOS, personajes="Nilo, Elefa, Gheco",
              criatura="dragon",
              carta="Todo junto | interfaz para lo común · cada pieza su clase · enum para los estados · excepciones con nombre · composición antes que herencia",
              recompensa="xp 25, oro 30", item="Martillo del Carpintero de Moldes",
              escena="""
                  El Gólem no se vence a martillazos: se lo vence **rearmando**. Cada pieza con su responsabilidad, sus datos protegidos, sus contratos claros y sus errores con nombre. Nilo tiene que rearmarlo pieza por pieza.
              """,
              sugiere="Una interfaz `Pieza` con `revisar(): Estado`; cada pieza la implementa; el `Golem` **tiene** sus piezas (composición) y cuenta cuántas están firmes.",
              desafio="Completá las clases para que el Gólem se revise solo.",
              inicial='''
                  <?php
                  enum Estado: string
                  {
                      case Firme = 'firme';
                      case Floja = 'floja';
                  }

                  interface Pieza
                  {
                      public function revisar(): Estado;
                      public function nombre(): string;
                  }

                  class Tabla
                  {
                      public function __construct(private string $nombre, private int $clavos)
                      {
                      }
                  }

                  class Golem
                  {
                      public function __construct(private array $piezas)
                      {
                      }

                      public function revisar(): void
                      {
                      }
                  }

                  (new Golem([new Tabla('timon', 4), new Tabla('brazo', 1), new Tabla('pierna', 3)]))->revisar();
              ''',
              solucion='''
                  <?php
                  enum Estado: string
                  {
                      case Firme = 'firme';
                      case Floja = 'floja';
                  }

                  interface Pieza
                  {
                      public function revisar(): Estado;
                      public function nombre(): string;
                  }

                  final class Tabla implements Pieza
                  {
                      public function __construct(private string $nombre, private int $clavos)
                      {
                      }

                      public function revisar(): Estado
                      {
                          return $this->clavos >= 2 ? Estado::Firme : Estado::Floja;
                      }

                      public function nombre(): string
                      {
                          return $this->nombre;
                      }
                  }

                  final class Golem
                  {
                      /** @param Pieza[] $piezas */
                      public function __construct(private array $piezas)
                      {
                      }

                      public function revisar(): void
                      {
                          $firmes = 0;
                          foreach ($this->piezas as $p) {
                              $estado = $p->revisar();
                              echo $p->nombre() . ": " . $estado->value . "\\n";
                              if ($estado === Estado::Firme) {
                                  $firmes++;
                              }
                          }
                          echo "Firmes: $firmes de " . count($this->piezas) . "\\n";
                      }
                  }

                  (new Golem([new Tabla('timon', 4), new Tabla('brazo', 1), new Tabla('pierna', 3)]))->revisar();
              ''',
              al_superar="Pieza por pieza, el Gólem queda revisado: sabe qué tiene flojo y por qué. Se sienta entre los moldes viejos, tranquilo, y deja caer el martillo con el que lo habían armado: **el Martillo del Carpintero de Moldes**. Elefa hace sonar la campana tres veces.",
              imagen=["El fondo del astillero con el Gólem sentado tranquilo entre moldes viejos, con las piezas ordenadas.",
                      GOLEM + " sentado, con los ojos de brasa más suaves.", NILO + " levanta un martillo de carpintero del piso.", ELEFA + " llega con el bastón en alto.", GHECO + " sobre la cabeza del Gólem."]),
        ],
    },
]
