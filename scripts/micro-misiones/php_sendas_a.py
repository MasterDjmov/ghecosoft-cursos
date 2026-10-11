from genphp import m
from php_r01 import NILO, ELEFA, IARA, PICO, GHECO

ARENA = "La Arena del Puerto"
RELOJ = "El reloj de arena gigante"
TABLERO = "El tablero de honor"
PALCO = "El palco del Campeón"
PALOMAR = "El palomar del Puerto"
VENTANA = "La ventana del palomar"
FERMIN = "Fermín (anciano bajo y encorvado, barba blanca larga, anteojos redondos de bronce, guardapolvo gris, gorro de lana, farol cian)"
CAMPEON = "el Campeón Eterno (guerrero alto de armadura antigua de bronce gastada y capa roja raída, sin cara: dentro del casco cerrado solo hay luz cian y engranajes)"
ORCA = "la Orca de los Mensajes (orca gigante negra y blanca con vetas violetas que brillan, con la boca llena de sobres)"

NODOS = [
    {
        "titulo": "S01-N01 · El modelo de la Arena: personajes, enemigos y dados",
        "misiones": [
            m(id="S01-N01-P1", titulo="Anotarse en la pizarra",
              lugar=ARENA, personajes="Nilo, Gheco",
              carta="El modelo | abstract class Personaje con vida y fuerza privadas · recibirDanio() nunca baja de 0 · vivo() pregunta, no se adivina",
              recompensa="xp 10, oro 10",
              escena="""
                  El primer camino desde la Encrucijada termina en la **Arena del Puerto**: un círculo de arena rodeado de gradas. En la puerta, un maestro de armas anota a cada luchador. Nilo se anota como «Nilo, el que no se olvida». Iara, atrás, tose.
              """,
              sugiere="La vida es privada y solo cambia con `recibirDanio()`, que nunca la deja negativa: `max(0, $this->vida - $danio)`.",
              desafio="Completá el personaje para que la vida no baje de 0.",
              inicial='''
                  <?php
                  abstract class Personaje
                  {
                      public function __construct(public readonly string $nombre, private int $vida)
                      {
                      }

                      public function recibirDanio(int $danio): void
                      {
                          $this->vida -= $danio;
                      }

                      public function vida(): int
                      {
                          return $this->vida;
                      }
                  }

                  final class Heroe extends Personaje
                  {
                  }

                  $nilo = new Heroe('Nilo', 30);
                  $nilo->recibirDanio(12);
                  $nilo->recibirDanio(40);
                  echo "{$nilo->nombre}: {$nilo->vida()} de vida, " . ($nilo->vida() > 0 ? 'en pie' : 'fuera de combate') . "\\n";
              ''',
              solucion='''
                  <?php
                  abstract class Personaje
                  {
                      public function __construct(public readonly string $nombre, private int $vida)
                      {
                      }

                      public function recibirDanio(int $danio): void
                      {
                          $this->vida = max(0, $this->vida - $danio);
                      }

                      public function vida(): int
                      {
                          return $this->vida;
                      }

                      public function vivo(): bool
                      {
                          return $this->vida > 0;
                      }
                  }

                  final class Heroe extends Personaje
                  {
                  }

                  $nilo = new Heroe('Nilo', 30);
                  $nilo->recibirDanio(12);
                  $nilo->recibirDanio(40);
                  echo "{$nilo->nombre}: {$nilo->vida()} de vida, " . ($nilo->vivo() ? 'en pie' : 'fuera de combate') . "\\n";
              ''',
              al_superar="Cero de vida, no menos. Nilo, fuera de combate antes de empezar, se ríe: es solo el modelo.",
              imagen=["La entrada de una arena circular de arena con gradas, de noche, con antorchas y una pizarra grande en la puerta con dibujitos de luchadores.",
                      NILO + " anotándose en la pizarra con tiza.", GHECO + " sobre la pizarra."]),
            m(id="S01-N01-P2", titulo="Los enemigos del enum",
              lugar=ARENA, personajes="Nilo, Gheco",
              carta="Enum con datos | enum Enemigo: string { case Goblin = 'goblin'; … public function vida(): int { return match ($this) { … }; } }",
              recompensa="xp 15, oro 15",
              escena="""
                  El maestro de armas trae criaturas de todo el mundo, y cada tipo tiene su vida y su fuerza. Nilo las escribió sueltas en tres arrays distintos, y al goblin le puso la vida del dragón.
              """,
              sugiere="Un enum con un método `vida()` y otro `fuerza()`, cada uno con un `match`. Todo lo de cada tipo, en un solo lugar.",
              desafio="Completá los métodos del enum.",
              inicial='''
                  <?php
                  enum Enemigo: string
                  {
                      case Goblin = 'goblin';
                      case Orco = 'orco';
                      case Dragon = 'dragon';

                      public function vida(): int
                      {
                          return 0;
                      }

                      public function fuerza(): int
                      {
                          return 0;
                      }
                  }

                  foreach (Enemigo::cases() as $e) {
                      echo "{$e->value}: vida {$e->vida()}, fuerza {$e->fuerza()}\\n";
                  }
              ''',
              solucion='''
                  <?php
                  enum Enemigo: string
                  {
                      case Goblin = 'goblin';
                      case Orco = 'orco';
                      case Dragon = 'dragon';

                      public function vida(): int
                      {
                          return match ($this) {
                              Enemigo::Goblin => 12,
                              Enemigo::Orco => 25,
                              Enemigo::Dragon => 90,
                          };
                      }

                      public function fuerza(): int
                      {
                          return match ($this) {
                              Enemigo::Goblin => 3,
                              Enemigo::Orco => 6,
                              Enemigo::Dragon => 14,
                          };
                      }
                  }

                  foreach (Enemigo::cases() as $e) {
                      echo "{$e->value}: vida {$e->vida()}, fuerza {$e->fuerza()}\\n";
                  }
              ''',
              al_superar="Cada criatura con lo suyo. El goblin ya no tiene la vida del dragón, para alivio de todos.",
              imagen=["Tres jaulas abiertas en el borde de la arena: una con un goblin, otra con un orco y otra, enorme, con la sombra de un dragón.",
                      NILO + " mira la jaula grande desde lejos.", GHECO + " sobre la jaula del goblin."]),
            m(id="S01-N01-P3", titulo="Dados trucados",
              lugar=ARENA, personajes="Nilo, Gheco",
              carta="Aislar el azar | interface Dados { public function tirar(int $caras): int; } · DadosFijos para probar · DadosConSemilla para jugar siempre igual",
              recompensa="xp 15, oro 15",
              escena="""
                  Para probar el juego, Nilo necesita que los dados caigan siempre igual. Con `rand()` cada partida es distinta y no hay forma de saber si el combate anda bien.
              """,
              sugiere="Una interfaz `Dados` y una clase `DadosFijos` que devuelve, en orden, los valores que le pasaste. El juego no sabe si son de verdad o trucados.",
              desafio="Escribí `DadosFijos` y usala para tirar tres veces.",
              inicial='''
                  <?php
                  interface Dados
                  {
                      public function tirar(int $caras): int;
                  }

                  final class DadosFijos implements Dados
                  {
                      public function __construct(private array $valores)
                      {
                      }

                      public function tirar(int $caras): int
                      {
                          return 1;
                      }
                  }

                  $d = new DadosFijos([6, 2, 5]);
                  echo "Tiradas: " . $d->tirar(6) . ", " . $d->tirar(6) . ", " . $d->tirar(6) . "\\n";
              ''',
              solucion='''
                  <?php
                  interface Dados
                  {
                      public function tirar(int $caras): int;
                  }

                  final class DadosFijos implements Dados
                  {
                      private int $siguiente = 0;

                      public function __construct(private array $valores)
                      {
                      }

                      public function tirar(int $caras): int
                      {
                          $valor = $this->valores[$this->siguiente % count($this->valores)];
                          $this->siguiente++;
                          return min($valor, $caras);
                      }
                  }

                  $d = new DadosFijos([6, 2, 5]);
                  echo "Tiradas: " . $d->tirar(6) . ", " . $d->tirar(6) . ", " . $d->tirar(6) . "\\n";
              ''',
              al_superar="Seis, dos, cinco. Siempre. Ahora el combate se puede probar, y Pico, que apuesta en las gradas, se queda sin negocio.",
              imagen=["Tres dados de hueso grandes sobre una mesa de madera en la arena, mostrando puntitos.",
                      NILO + " tira los dados.", PICO + " en las gradas, mirando con interés.", GHECO + " sobre un dado."]),
        ],
    },
    {
        "titulo": "S01-N02 · El motor de combate",
        "misiones": [
            m(id="S01-N02-P1", titulo="El reloj de arena",
              lugar=RELOJ, personajes="Nilo, Gheco",
              carta="Bucle de turnos | while (los dos vivos) { ataca uno; si el otro sigue vivo, ataca el otro; } · termina cuando cae alguno",
              recompensa="xp 10, oro 10",
              escena="""
                  En el centro de la Arena hay un reloj de arena gigante: cada vez que cae, le toca a otro luchador. Pico se instala en las gradas y le roba los maníes a todo el mundo. El combate de Nilo no termina nunca: el bucle no pregunta si alguien cayó.
              """,
              sugiere="El bucle sigue mientras **los dos** estén vivos. Después de cada golpe, si el atacado cayó, se sale.",
              desafio="Completá el bucle de turnos.",
              inicial='''
                  <?php
                  $heroe = ['nombre' => 'Nilo', 'vida' => 20, 'fuerza' => 7];
                  $goblin = ['nombre' => 'goblin', 'vida' => 12, 'fuerza' => 4];
                  $turno = 1;
                  echo "Gano: ?\\n";
              ''',
              solucion='''
                  <?php
                  $heroe = ['nombre' => 'Nilo', 'vida' => 20, 'fuerza' => 7];
                  $goblin = ['nombre' => 'goblin', 'vida' => 12, 'fuerza' => 4];
                  $turno = 1;
                  while ($heroe['vida'] > 0 && $goblin['vida'] > 0) {
                      $goblin['vida'] = max(0, $goblin['vida'] - $heroe['fuerza']);
                      echo "Turno $turno: Nilo pega {$heroe['fuerza']}, al goblin le quedan {$goblin['vida']}\\n";
                      if ($goblin['vida'] === 0) {
                          break;
                      }
                      $heroe['vida'] = max(0, $heroe['vida'] - $goblin['fuerza']);
                      echo "Turno $turno: el goblin pega {$goblin['fuerza']}, a Nilo le quedan {$heroe['vida']}\\n";
                      $turno++;
                  }
                  echo "Gano: " . ($heroe['vida'] > 0 ? $heroe['nombre'] : $goblin['nombre']) . "\\n";
              ''',
              al_superar="Dos turnos y el goblin cae. El reloj de arena se da vuelta solo, aliviado.",
              imagen=["Un reloj de arena gigante de bronce en el centro de la arena, con la arena cayendo y antorchas alrededor.",
                      NILO + " con una espada de madera frente a un goblin.", PICO + " en las gradas con un maní en el pico.", GHECO + " sobre el reloj."]),
            m(id="S01-N02-P2", titulo="Cada enemigo piensa distinto",
              lugar=RELOJ, personajes="Nilo, Gheco",
              carta="Estrategia | interface Estrategia { public function elegir(array $rivales): string; } · cada enemigo con la suya · agregar uno es una clase, no tocar el motor",
              recompensa="xp 15, oro 15",
              escena="""
                  Los goblins pelean a lo loco, los orcos siempre van contra el más débil. El motor de Nilo tenía un `if` por cada criatura, y cuando llegó el troll nadie supo dónde agregarlo.
              """,
              sugiere="Cada forma de pensar es una clase que implementa `Estrategia`. `ContraElMasDebil` elige al de menos vida; `AlPrimero` elige el primero.",
              desafio="Escribí las dos estrategias.",
              inicial='''
                  <?php
                  interface Estrategia
                  {
                      /** @param array<string, int> $rivales nombre => vida */
                      public function elegir(array $rivales): string;
                  }

                  $rivales = ['Nilo' => 20, 'Iara' => 8, 'Fermin' => 14];
                  echo "El orco ataca a: ?\\n";
                  echo "El goblin ataca a: ?\\n";
              ''',
              solucion='''
                  <?php
                  interface Estrategia
                  {
                      /** @param array<string, int> $rivales nombre => vida */
                      public function elegir(array $rivales): string;
                  }

                  final class ContraElMasDebil implements Estrategia
                  {
                      public function elegir(array $rivales): string
                      {
                          return array_search(min($rivales), $rivales, true);
                      }
                  }

                  final class AlPrimero implements Estrategia
                  {
                      public function elegir(array $rivales): string
                      {
                          return array_key_first($rivales);
                      }
                  }

                  $rivales = ['Nilo' => 20, 'Iara' => 8, 'Fermin' => 14];
                  echo "El orco ataca a: " . (new ContraElMasDebil())->elegir($rivales) . "\\n";
                  echo "El goblin ataca a: " . (new AlPrimero())->elegir($rivales) . "\\n";
              ''',
              al_superar="El orco va contra Iara, que levanta la libreta como escudo. El goblin, contra Nilo, que estaba primero. El motor no se enteró de nada.",
              imagen=["La arena con un orco que apunta hacia una chica con una libreta y un goblin que corre hacia un muchacho con gorra.",
                      IARA + " levanta la libreta como escudo.", NILO + " esquiva al goblin.", GHECO + " sobre el reloj de arena."]),
            m(id="S01-N02-P3", titulo="La bitácora del juez",
              lugar=RELOJ, personajes="Nilo, Gheco",
              carta="Bitácora | cada golpe se anota en un array · al final se resume · el resultado es un enum: Victoria, Derrota, Empate",
              recompensa="xp 15, oro 15",
              escena="""
                  Un juez anota cada golpe en un pergamino que después se lee en voz alta para todo el público. El motor de Nilo mostraba los golpes mientras pasaban y al final no sabía decir quién había ganado.
              """,
              sugiere="Guardá cada golpe en `$bitacora[]`, y devolvé el resultado como un caso del enum `Resultado`. El resumen sale de contar la bitácora.",
              desafio="Completá el resumen del combate.",
              inicial='''
                  <?php
                  enum Resultado: string
                  {
                      case Victoria = 'victoria';
                      case Derrota = 'derrota';
                  }

                  function combatir(int $vidaHeroe, int $vidaRival, array $golpes): array
                  {
                      return [Resultado::Victoria, []];
                  }

                  [$resultado, $bitacora] = combatir(10, 9, [['heroe', 4], ['rival', 3], ['heroe', 5]]);
                  echo "Golpes: " . count($bitacora) . "\\n";
                  echo "Resultado: {$resultado->value}\\n";
              ''',
              solucion='''
                  <?php
                  enum Resultado: string
                  {
                      case Victoria = 'victoria';
                      case Derrota = 'derrota';
                  }

                  function combatir(int $vidaHeroe, int $vidaRival, array $golpes): array
                  {
                      $bitacora = [];
                      foreach ($golpes as [$quien, $danio]) {
                          if ($quien === 'heroe') {
                              $vidaRival = max(0, $vidaRival - $danio);
                          } else {
                              $vidaHeroe = max(0, $vidaHeroe - $danio);
                          }
                          $bitacora[] = "$quien pega $danio";
                          if ($vidaHeroe === 0 || $vidaRival === 0) {
                              break;
                          }
                      }
                      return [$vidaRival === 0 ? Resultado::Victoria : Resultado::Derrota, $bitacora];
                  }

                  [$resultado, $bitacora] = combatir(10, 9, [['heroe', 4], ['rival', 3], ['heroe', 5]]);
                  echo implode("\\n", $bitacora) . "\\n";
                  echo "Golpes: " . count($bitacora) . "\\n";
                  echo "Resultado: {$resultado->value}\\n";
              ''',
              al_superar="El juez lee la bitácora en voz alta y el público aplaude en el momento justo. Pico aprovecha el aplauso para robar más maníes.",
              imagen=["Un juez con un pergamino largo leyendo en voz alta frente a las gradas llenas de la arena.",
                      NILO + " saluda al público.", PICO + " robando maníes en las gradas.", GHECO + " sobre el pergamino."]),
        ],
    },
    {
        "titulo": "S01-N03 · Oleadas, experiencia y el ranking en MariaDB",
        "misiones": [
            m(id="S01-N03-P1", titulo="Las puertas que se abren",
              lugar=TABLERO, personajes="Nilo, Gheco",
              carta="Oleadas con yield | function oleadas() { for (…) yield $n => [...]; } · cada oleada más difícil que la anterior · se generan a medida que hacen falta",
              recompensa="xp 10, oro 10",
              escena="""
                  Las puertas de la Arena se abren una y otra vez, y cada vez salen más criaturas. Nilo armó las cien oleadas de una vez al empezar, y el juego tarda un minuto en arrancar.
              """,
              sugiere="Un generador que da la oleada `n` con `n` goblins y, cada tres, un orco más. Se piden solo las que se juegan.",
              desafio="Escribí el generador de oleadas.",
              inicial='''
                  <?php
                  function oleadas(int $hasta): array
                  {
                      return [];
                  }

                  foreach (oleadas(4) as $n => $enemigos) {
                      echo "Oleada $n: " . implode(', ', $enemigos) . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function oleadas(int $hasta): Generator
                  {
                      for ($n = 1; $n <= $hasta; $n++) {
                          $enemigos = array_fill(0, $n, 'goblin');
                          for ($o = 0; $o < intdiv($n, 3); $o++) {
                              $enemigos[] = 'orco';
                          }
                          yield $n => $enemigos;
                      }
                  }

                  foreach (oleadas(4) as $n => $enemigos) {
                      echo "Oleada $n: " . implode(', ', $enemigos) . "\\n";
                  }
              ''',
              al_superar="Las oleadas salen de a una, cada vez más grandes. El juego arranca al instante.",
              imagen=["Las puertas de hierro de la arena abriéndose y un grupo de goblins saliendo en fila.",
                      NILO + " con escudo, esperándolos.", GHECO + " sobre la puerta."]),
            m(id="S01-N03-P2", titulo="Subir de nivel",
              lugar=TABLERO, personajes="Nilo, Gheco",
              carta="Una regla clara | cada nivel pide nivel × 100 de experiencia · se puede subir varios de golpe · se devuelve qué niveles se subieron",
              recompensa="xp 15, oro 15",
              escena="""
                  Después de una oleada enorme, Nilo ganó tanta experiencia que debería subir dos niveles, pero el juego solo le sube uno y el resto se pierde.
              """,
              sugiere="Mientras la experiencia alcance para el siguiente nivel (`nivel × 100`), se descuenta y se sube. Un `while`, no un `if`.",
              desafio="Completá `ganarExperiencia`.",
              inicial='''
                  <?php
                  final class Heroe
                  {
                      public int $nivel = 1;
                      public int $experiencia = 0;

                      public function ganarExperiencia(int $puntos): array
                      {
                          $this->experiencia += $puntos;
                          $subidas = [];
                          if ($this->experiencia >= $this->nivel * 100) {
                              $this->experiencia -= $this->nivel * 100;
                              $this->nivel++;
                              $subidas[] = $this->nivel;
                          }
                          return $subidas;
                      }
                  }

                  $nilo = new Heroe();
                  $subio = $nilo->ganarExperiencia(350);
                  echo "Subio a: " . implode(' y ', $subio) . "\\n";
                  echo "Nivel {$nilo->nivel}, sobran {$nilo->experiencia}\\n";
              ''',
              solucion='''
                  <?php
                  final class Heroe
                  {
                      public int $nivel = 1;
                      public int $experiencia = 0;

                      public function ganarExperiencia(int $puntos): array
                      {
                          $this->experiencia += $puntos;
                          $subidas = [];
                          while ($this->experiencia >= $this->nivel * 100) {
                              $this->experiencia -= $this->nivel * 100;
                              $this->nivel++;
                              $subidas[] = $this->nivel;
                          }
                          return $subidas;
                      }
                  }

                  $nilo = new Heroe();
                  $subio = $nilo->ganarExperiencia(350);
                  echo "Subio a: " . implode(' y ', $subio) . "\\n";
                  echo "Nivel {$nilo->nivel}, sobran {$nilo->experiencia}\\n";
              ''',
              al_superar="Nivel 3, con 50 de sobra. Nilo festeja dos veces, una por cada nivel.",
              imagen=["Una columna de luz cian que sube alrededor de un luchador en el centro de la arena, con chispas.",
                      NILO + " con los brazos arriba dentro de la columna de luz.", GHECO + " girando alrededor."]),
            m(id="S01-N03-P3", titulo="El tablero de honor",
              lugar=TABLERO, personajes="Nilo, Fermín, Gheco",
              carta="Ranking | INSERT preparado por partida · SELECT … ORDER BY oleada DESC, puntos DESC LIMIT 3 · la base guarda; la página solo muestra",
              recompensa="xp 15, oro 15",
              escena="""
                  Quien cae queda grabado en el **tablero de honor** de la entrada. Fermín sube de la Bodega a llevar el tablero: dice que un puntaje que no se guarda no existió.
              """,
              sugiere="Guardá cada partida con un `INSERT` preparado y mostrá los tres mejores ordenados por oleada y, si empatan, por puntos.",
              desafio="Completá el guardado y el ranking.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
                  $db->exec('CREATE TABLE partida (id INTEGER PRIMARY KEY, nombre TEXT, oleada INTEGER, puntos INTEGER)');

                  $partidas = [['Nilo', 7, 420], ['Iara', 9, 380], ['Fermin', 7, 510], ['Pico', 2, 30]];
                  echo "Top 3:\\n";
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
                  $db->exec('CREATE TABLE partida (id INTEGER PRIMARY KEY, nombre TEXT, oleada INTEGER, puntos INTEGER)');

                  $partidas = [['Nilo', 7, 420], ['Iara', 9, 380], ['Fermin', 7, 510], ['Pico', 2, 30]];
                  $guardar = $db->prepare('INSERT INTO partida (nombre, oleada, puntos) VALUES (?, ?, ?)');
                  foreach ($partidas as $p) {
                      $guardar->execute($p);
                  }

                  echo "Top 3:\\n";
                  $top = $db->query('SELECT nombre, oleada, puntos FROM partida ORDER BY oleada DESC, puntos DESC LIMIT 3');
                  foreach ($top as $i => $f) {
                      echo ($i + 1) . ". {$f['nombre']}: oleada {$f['oleada']}, {$f['puntos']} puntos\\n";
                  }
              ''',
              al_superar="Iara primera, Fermín segundo, Nilo tercero. Pico, cuarto, intenta borrar el tablero con el ala. No puede: está en la base.",
              imagen=["Un tablero de honor de madera en la entrada de la arena con tres placas de bronce brillando, sin letras.",
                      FERMIN + " cuelga el tablero.", IARA + " sonríe orgullosa.", NILO + " aplaude.", PICO + " frotando el tablero con el ala.", GHECO + " sobre la placa de arriba."]),
        ],
    },
    {
        "titulo": "S01-N04 · Jefe de la Arena: el Campeón Eterno",
        "misiones": [
            m(id="S01-N04-P1", titulo="Las órdenes del jugador",
              lugar=PALCO, personajes="Nilo, Gheco",
              criatura="dragon",
              carta="Leer órdenes | while (($orden = fgets(STDIN)) !== false) · match (trim($orden)) { 'atacar' => …, 'curar' => …, default => 'orden desconocida' }",
              recompensa="xp 15, oro 15",
              escena="""
                  En el palco más alto espera el **Campeón Eterno**: nadie lo venció en cien años. Para enfrentarlo hay que presentar un juego que lea las órdenes de una persona de verdad. El juego de Nilo ignora lo que escribe el jugador.
              """,
              sugiere="Leé cada renglón con `fgets(STDIN)` hasta que no haya más, y con un `match` decidí qué hace cada orden.",
              desafio="Hacé que el juego responda a cada orden.",
              inicial='''
                  <?php
                  $vida = 20;
                  echo "Vida final: $vida\\n";
              ''',
              entrada="atacar\ncurar\nbailar\natacar\n",
              solucion='''
                  <?php
                  $vida = 20;
                  $golpes = 0;
                  while (($orden = fgets(STDIN)) !== false) {
                      echo match (trim($orden)) {
                          'atacar' => "Golpe numero " . (++$golpes) . "\\n",
                          'curar' => "Vida: " . ($vida = min(30, $vida + 5)) . "\\n",
                          default => "Orden desconocida: " . trim($orden) . "\\n",
                      };
                  }
                  echo "Vida final: $vida\\n";
              ''',
              al_superar="El juego contesta cada orden, y a «bailar» le dice que no la conoce. El Campeón inclina el casco: acepta el desafío.",
              imagen=["El palco más alto de la arena, con un trono de piedra y una figura con armadura antigua sentada.",
                      CAMPEON + " sentado en el trono.", NILO + " frente a él, con un papel de órdenes.", GHECO + " sobre el papel."]),
            m(id="S01-N04-P2", titulo="Guardar y continuar",
              lugar=PALCO, personajes="Nilo, Gheco",
              criatura="dragon",
              carta="Estado en JSON | json_encode del estado al guardar · json_decode al cargar · si el archivo falta o está roto, partida nueva",
              recompensa="xp 15, oro 15",
              escena="""
                  El combate contra el Campeón dura horas. Nilo tiene que poder guardar la partida y seguir mañana. Su juego, en cambio, empieza de cero cada vez.
              """,
              sugiere="Guardá el estado con `json_encode` en un archivo. Al cargar, si no existe o no se puede leer, devolvé una partida nueva.",
              desafio="Completá guardar y cargar.",
              inicial='''
                  <?php
                  function nueva(): array
                  {
                      return ['oleada' => 1, 'vida' => 30];
                  }

                  function guardar(array $estado, string $archivo): void
                  {
                  }

                  function cargar(string $archivo): array
                  {
                      return nueva();
                  }

                  guardar(['oleada' => 8, 'vida' => 17], 'partida.json');
                  $estado = cargar('partida.json');
                  echo "Seguis en la oleada {$estado['oleada']} con {$estado['vida']} de vida\\n";
                  $otra = cargar('no-existe.json');
                  echo "Partida nueva: oleada {$otra['oleada']}\\n";
              ''',
              solucion='''
                  <?php
                  function nueva(): array
                  {
                      return ['oleada' => 1, 'vida' => 30];
                  }

                  function guardar(array $estado, string $archivo): void
                  {
                      file_put_contents($archivo, json_encode($estado));
                  }

                  function cargar(string $archivo): array
                  {
                      if (!is_file($archivo)) {
                          return nueva();
                      }
                      $estado = json_decode(file_get_contents($archivo), true);
                      return is_array($estado) ? $estado : nueva();
                  }

                  guardar(['oleada' => 8, 'vida' => 17], 'partida.json');
                  $estado = cargar('partida.json');
                  echo "Seguis en la oleada {$estado['oleada']} con {$estado['vida']} de vida\\n";
                  $otra = cargar('no-existe.json');
                  echo "Partida nueva: oleada {$otra['oleada']}\\n";
              ''',
              al_superar="La partida se guarda en la oleada 8. Mañana se sigue. El Campeón, que nunca durmió, no entiende para qué.",
              imagen=["Un pergamino enrollado con un sello de lacre violeta sobre el borde del palco, al lado de un casco antiguo.",
                      NILO + " guarda el pergamino en su morral.", GHECO + " sobre el casco."]),
            m(id="S01-N04-P3", titulo="Ganarle al que aprende",
              lugar=PALCO, personajes="Nilo, Gheco",
              criatura="dragon",
              carta="Todo el juego | modelo, dados, motor con estrategias, oleadas, experiencia, ranking y partidas guardadas · cada pieza en su clase · el azar con semilla",
              recompensa="xp 25, oro 30",
              escena="""
                  Dicen que el Campeón no es una persona sino un juego perfecto, hecho por una programadora que ya no está, que aprende de cada luchador: repite la jugada que más le sirvió. Para ganarle, el juego de Nilo tiene que variar sus jugadas con dados de semilla fija.
              """,
              sugiere="`mt_srand(7)` fija la semilla: así el juego varía las jugadas, pero siempre de la misma forma (y se puede probar). El Campeón aprende la jugada más repetida; si Nilo no repite, no la adivina.",
              desafio="Completá el combate con las jugadas al azar con semilla.",
              inicial='''
                  <?php
                  $jugadas = ['tajo', 'estocada', 'finta'];
                  $aciertosCampeon = 0;
                  $vistas = [];
                  for ($ronda = 1; $ronda <= 6; $ronda++) {
                      $jugada = 'tajo';
                      $prediccion = $vistas === [] ? 'tajo' : array_search(max($vistas), $vistas, true);
                      if ($prediccion === $jugada) {
                          $aciertosCampeon++;
                      }
                      $vistas[$jugada] = ($vistas[$jugada] ?? 0) + 1;
                  }
                  echo "El Campeon adivino $aciertosCampeon de 6\\n";
              ''',
              solucion='''
                  <?php
                  mt_srand(7);
                  $jugadas = ['tajo', 'estocada', 'finta'];
                  $aciertosCampeon = 0;
                  $vistas = [];
                  for ($ronda = 1; $ronda <= 6; $ronda++) {
                      $jugada = $jugadas[mt_rand(0, count($jugadas) - 1)];
                      $prediccion = $vistas === [] ? 'tajo' : array_search(max($vistas), $vistas, true);
                      if ($prediccion === $jugada) {
                          $aciertosCampeon++;
                      }
                      $vistas[$jugada] = ($vistas[$jugada] ?? 0) + 1;
                  }
                  echo "El Campeon adivino $aciertosCampeon de 6\\n";
                  echo $aciertosCampeon < 3 ? "Gana Nilo\\n" : "Gana el Campeon\\n";
              ''',
              al_superar="El Campeón no adivina. Después de cien años, alguien le gana. Se saca el casco, y adentro no hay nadie: solo luz y engranajes que, por primera vez, se detienen a descansar.",
              imagen=["El palco de la arena con el casco del Campeón en el piso, del que sale luz cian y engranajes quietos, y el público de pie aplaudiendo.",
                      CAMPEON + " de rodillas, sin casco.", NILO + " con la espada de madera en alto.", GHECO + " sobre el casco."]),
        ],
    },
    {
        "titulo": "S03-N01 · JavaScript en el navegador: el DOM y `fetch`",
        "misiones": [
            m(id="S03-N01-P1", titulo="La respuesta atada a la pata",
              lugar=PALOMAR, personajes="Nilo, Gheco",
              carta="La API para fetch | la página pide con fetch('/api/barcos') · PHP contesta JSON con su encabezado · la paloma lleva solo datos",
              recompensa="xp 10, oro 10",
              escena="""
                  El tercer camino desde la Encrucijada baja hasta el palomar. Cientos de palomas llevan una pregunta corta a la torre y vuelven con la respuesta atada a la pata. Nilo, que se pasó el viaje corriendo con cartas, mira a las palomas con una mezcla de admiración y celos.
              """,
              sugiere="Del lado de PHP, `fetch` necesita JSON. Una función `responder()` que devuelva el código y el cuerpo con `json_encode`, incluso cuando no hay datos (una lista vacía).",
              desafio="Completá la respuesta de la API para las dos preguntas.",
              inicial='''
                  <?php
                  $barcos = ['Forjas' => ['Gaviota', 'Tortuga'], 'Valle' => []];

                  function responder(array $barcos, string $destino): string
                  {
                      return implode(', ', $barcos[$destino]);
                  }

                  echo responder($barcos, 'Forjas') . "\\n";
                  echo responder($barcos, 'Valle') . "\\n";
              ''',
              solucion='''
                  <?php
                  $barcos = ['Forjas' => ['Gaviota', 'Tortuga'], 'Valle' => []];

                  function responder(array $barcos, string $destino): string
                  {
                      return "200 " . json_encode(['destino' => $destino, 'barcos' => $barcos[$destino] ?? []]);
                  }

                  echo responder($barcos, 'Forjas') . "\\n";
                  echo responder($barcos, 'Valle') . "\\n";
              ''',
              al_superar="Las palomas vuelven con respuestas que la página entiende, aunque la lista venga vacía. Nilo le da una miga a cada una.",
              imagen=["Un palomar de piedra junto al mar, de noche, con cientos de palomas mensajeras entrando y saliendo por las ventanitas.",
                      NILO + " le ata un papelito a la pata de una paloma.", GHECO + " sobre el techo del palomar."]),
            m(id="S03-N01-P2", titulo="textContent, no innerHTML",
              lugar=PALOMAR, personajes="Nilo, Pico, Gheco",
              criatura="troll",
              carta="Mostrar sin XSS | en JS, elemento.textContent = dato (nunca innerHTML con datos del servidor) · en PHP, json_encode ya escapa bien para JSON",
              recompensa="xp 15, oro 15",
              escena="""
                  Una paloma trajo un nombre de barco con un truco: `<img onerror=…>`. El tablero de la ventana lo metió como HTML y se ejecutó. Un **troll** venía escondido en la paloma… o era Pico disfrazado.
              """,
              sugiere="En el navegador, el dato va con `textContent`. Acá practicamos la misma idea en PHP: al armar HTML, el dato pasa por `htmlspecialchars`; al mandar JSON, por `json_encode`.",
              desafio="Mostrá el nombre tramposo sin que se ejecute, en HTML y en JSON.",
              inicial='''
                  <?php
                  $nombre = '<img src=x onerror="robar()">';
                  echo "<li>$nombre</li>\\n";
                  echo '{"barco":"' . $nombre . '"}' . "\\n";
              ''',
              solucion='''
                  <?php
                  $nombre = '<img src=x onerror="robar()">';
                  echo "<li>" . htmlspecialchars($nombre) . "</li>\\n";
                  echo json_encode(['barco' => $nombre]) . "\\n";
              ''',
              al_superar="El truco aparece como texto, desarmado. La paloma tramposa se saca el disfraz: era Pico. Nilo lo perdona, como siempre.",
              imagen=["La ventana del palomar con un tablero de madera donde se ven las respuestas de las palomas, y una paloma rara con plumas pegadas.",
                      PICO + " disfrazado de paloma, con plumas grises pegadas.", NILO + " le saca una pluma, riéndose.", GHECO + " sobre el tablero."]),
            m(id="S03-N01-P3", titulo="El router del servidor chico",
              lugar=PALOMAR, personajes="Nilo, Gheco",
              carta="router.php | con php -S, un router decide: si la dirección empieza con /api, contesta la API · si es un archivo que existe, return false (lo sirve tal cual) · si no, la página",
              recompensa="xp 15, oro 15",
              escena="""
                  Para probar la página y la API juntas en la compu, Nilo levanta el servidor chico de PHP. Pero todas las direcciones le devuelven la página, incluso `/api/barcos`.
              """,
              sugiere="Una función que, según la dirección, decida: `/api/…` → API; un archivo estático conocido → servir el archivo; cualquier otra → la página.",
              desafio="Completá la decisión del router.",
              inicial='''
                  <?php
                  function decidir(string $ruta, array $archivos): string
                  {
                      return 'pagina';
                  }

                  $archivos = ['/app.js', '/estilos.css'];
                  foreach (['/', '/api/barcos', '/app.js', '/horarios'] as $r) {
                      echo "$r -> " . decidir($r, $archivos) . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function decidir(string $ruta, array $archivos): string
                  {
                      if (str_starts_with($ruta, '/api/')) {
                          return 'api';
                      }
                      if (in_array($ruta, $archivos, true)) {
                          return 'archivo';
                      }
                      return 'pagina';
                  }

                  $archivos = ['/app.js', '/estilos.css'];
                  foreach (['/', '/api/barcos', '/app.js', '/horarios'] as $r) {
                      echo "$r -> " . decidir($r, $archivos) . "\\n";
                  }
              ''',
              al_superar="Cada pedido llega a donde tiene que llegar. La página, la API y los archivos conviven en el servidor chico.",
              imagen=["Tres caminos de palomas que salen del palomar en distintas direcciones: hacia la torre, hacia un estante con frascos y hacia una ventana.",
                      NILO + " dirige las palomas con una bandera.", GHECO + " sobre la bandera."]),
        ],
    },
    {
        "titulo": "S03-N02 · Formularios, sesión y errores: la página que escribe",
        "misiones": [
            m(id="S03-N02-P1", titulo="El error al lado del campo",
              lugar=VENTANA, personajes="Nilo, Iara, Gheco",
              carta="422 para la página | {\"errores\": {\"campo\": \"motivo\"}} · la página pone cada mensaje al lado de su campo · los demás errores, en un aviso general",
              recompensa="xp 10, oro 10",
              escena="""
                  La página de pedidos mostraba «Error» arriba de todo, y el cliente no sabía qué campo corregir. Iara quiere el error al lado del campo, como en sus formularios de papel.
              """,
              sugiere="La API contesta 422 con `errores` por campo. Acá armamos el HTML del formulario con cada error al lado de su campo, como lo haría la página.",
              desafio="Dibujá el formulario con el error al lado de cada campo.",
              inicial='''
                  <?php
                  $respuesta = json_decode('{"errores":{"kilos":"tiene que ser mayor que 0"}}', true);
                  foreach (['destino', 'kilos'] as $campo) {
                      echo "<label>$campo <input name=\\"$campo\\"></label>\\n";
                  }
                  echo "<p>Error</p>\\n";
              ''',
              solucion='''
                  <?php
                  $respuesta = json_decode('{"errores":{"kilos":"tiene que ser mayor que 0"}}', true);
                  foreach (['destino', 'kilos'] as $campo) {
                      $error = $respuesta['errores'][$campo] ?? null;
                      echo "<label>$campo <input name=\\"$campo\\">" . ($error ? " <small>" . htmlspecialchars($error) . "</small>" : "") . "</label>\\n";
                  }
              ''',
              al_superar="El error aparece justo donde hay que corregir. Iara aprueba con un tilde en la libreta.",
              imagen=["Un formulario de papel en la ventana del palomar con una notita pegada al lado de un casillero.",
                      IARA + " pega la notita.", NILO + " sostiene el formulario.", GHECO + " sobre la notita."]),
            m(id="S03-N02-P2", titulo="401: primero, entrar",
              lugar=VENTANA, personajes="Nilo, Gheco",
              carta="401 y 403 | 401: no sabemos quién sos (que entre) · 403: sabemos quién sos y no podés · la página reacciona distinto a cada uno",
              recompensa="xp 15, oro 15",
              escena="""
                  No cualquiera puede escribir en los libros del Puerto. Pero la API de Nilo contesta igual a quien no entró y a quien entró sin permiso, y la página no sabe si mandar al login o mostrar «no podés».
              """,
              sugiere="Sin usuario en la sesión: 401. Con usuario pero sin el rol que hace falta: 403. Con todo bien: 200.",
              desafio="Devolvé el código correcto en cada caso.",
              inicial='''
                  <?php
                  function borrarEnvio(array $sesion): string
                  {
                      return isset($sesion['usuario']) && $sesion['rol'] === 'admin' ? "200 Borrado" : "403 No podes";
                  }

                  echo borrarEnvio([]) . "\\n";
                  echo borrarEnvio(['usuario' => 'nilo', 'rol' => 'mensajero']) . "\\n";
                  echo borrarEnvio(['usuario' => 'elefa', 'rol' => 'admin']) . "\\n";
              ''',
              solucion='''
                  <?php
                  function borrarEnvio(array $sesion): string
                  {
                      if (!isset($sesion['usuario'])) {
                          return "401 Primero hay que entrar";
                      }
                      if (($sesion['rol'] ?? '') !== 'admin') {
                          return "403 No podes";
                      }
                      return "200 Borrado";
                  }

                  echo borrarEnvio([]) . "\\n";
                  echo borrarEnvio(['usuario' => 'nilo', 'rol' => 'mensajero']) . "\\n";
                  echo borrarEnvio(['usuario' => 'elefa', 'rol' => 'admin']) . "\\n";
              ''',
              al_superar="El visitante va al login; Nilo ve «no podés»; Elefa borra. Cada uno recibe lo suyo.",
              imagen=["Tres palomas en la ventana del palomar, cada una con un sobre de distinto color en la pata.",
                      NILO + " lee un sobre con cara de decepción.", GHECO + " sobre la ventana."]),
            m(id="S03-N02-P3", titulo="Estado y dibujo",
              lugar=VENTANA, personajes="Nilo, Gheco",
              carta="Estado + dibujar | todo lo que muestra la página sale de un estado · cada cambio actualiza el estado y se vuelve a dibujar · nunca se toca la pantalla a mano",
              recompensa="xp 15, oro 15",
              escena="""
                  La página de Nilo agregaba y sacaba cosas de la pantalla a mano, y después de tres pedidos ya no coincidía con lo que había en la torre. Gheco le propone una regla: la pantalla siempre se **dibuja** a partir de un **estado**.
              """,
              sugiere="Una función `dibujar(array $estado): string` arma todo a partir del estado. Agregar un pedido es cambiar el estado y dibujar de nuevo.",
              desafio="Escribí `dibujar` y usala después de cada cambio.",
              inicial='''
                  <?php
                  $estado = ['pedidos' => ['telas'], 'cargando' => false];

                  function dibujar(array $estado): string
                  {
                      return '';
                  }

                  echo dibujar($estado) . "\\n";
                  $estado['pedidos'][] = 'sal';
                  echo dibujar($estado) . "\\n";
                  $estado['cargando'] = true;
                  echo dibujar($estado) . "\\n";
              ''',
              solucion='''
                  <?php
                  $estado = ['pedidos' => ['telas'], 'cargando' => false];

                  function dibujar(array $estado): string
                  {
                      if ($estado['cargando']) {
                          return "[esperando a la paloma...]";
                      }
                      return "[" . count($estado['pedidos']) . " pedidos: " . implode(', ', $estado['pedidos']) . "]";
                  }

                  echo dibujar($estado) . "\\n";
                  $estado['pedidos'][] = 'sal';
                  echo dibujar($estado) . "\\n";
                  $estado['cargando'] = true;
                  echo dibujar($estado) . "\\n";
              ''',
              al_superar="La pantalla siempre dice la verdad, porque sale del estado. Nilo deja de pelearse con el tablero.",
              imagen=["Un tablero de madera en la ventana del palomar que se redibuja solo con tiza mágica cian.",
                      NILO + " mira el tablero redibujarse.", GHECO + " con una tiza en la mano."]),
        ],
    },
    {
        "titulo": "S03-N03 · Jefe del Palomar: la Orca de los Mensajes",
        "misiones": [
            m(id="S03-N03-P1", titulo="Cien pedidos por segundo",
              lugar=PALOMAR, personajes="Nilo, Gheco",
              criatura="dragon",
              carta="429 | contar los pedidos de cada uno en una ventana de tiempo · si se pasa del límite, 429 Demasiados pedidos · la torre sabe decir «esperá»",
              recompensa="xp 15, oro 15",
              escena="""
                  Una tarde el mar se levanta frente al palomar y salta la **Orca de los Mensajes**: manda cien pedidos por segundo para tapar la torre. Las demás palomas no pueden pasar.
              """,
              sugiere="Contá los pedidos de cada uno por segundo en `$contador[\"$quien@$segundo\"]`. Si pasa de 3, contestá 429.",
              desafio="Limitá a 3 pedidos por segundo por remitente.",
              inicial='''
                  <?php
                  $pedidos = [['orca', 1], ['orca', 1], ['orca', 1], ['orca', 1], ['orca', 1], ['nilo', 1], ['orca', 2]];
                  $contador = [];
                  foreach ($pedidos as [$quien, $segundo]) {
                      echo "$quien: 200\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $pedidos = [['orca', 1], ['orca', 1], ['orca', 1], ['orca', 1], ['orca', 1], ['nilo', 1], ['orca', 2]];
                  $contador = [];
                  foreach ($pedidos as [$quien, $segundo]) {
                      $clave = "$quien@$segundo";
                      $contador[$clave] = ($contador[$clave] ?? 0) + 1;
                      echo $contador[$clave] > 3 ? "$quien: 429 Esperá\\n" : "$quien: 200\\n";
                  }
              ''',
              al_superar="La Orca recibe «esperá» y las palomas de Nilo pasan. La Orca se zambulle, ofendida, y vuelve a intentar al segundo siguiente.",
              imagen=["Una orca gigante saltando del mar frente al palomar con la boca llena de sobres.",
                      ORCA + " en pleno salto.", NILO + " en la ventana del palomar, con un cartel liso con una mano levantada.", GHECO + " sobre el cartel."]),
            m(id="S03-N03-P2", titulo="Dos personas, el mismo botón",
              lugar=PALOMAR, personajes="Nilo, Fermín, Gheco",
              criatura="dragon",
              carta="UNIQUE manda | si dos aprietan a la vez, la base decide · el segundo INSERT falla por UNIQUE · se convierte en un 409 claro",
              recompensa="xp 15, oro 15",
              escena="""
                  La Orca confunde las respuestas: dos personas reservan el último lugar del ferry al mismo tiempo, y las dos reciben «confirmado». Fermín, de visita, sacude la cabeza: —Eso lo tiene que frenar la bodega.
              """,
              sugiere="Con `UNIQUE (viaje, asiento)`, el segundo `INSERT` falla. Atrapá la `PDOException` y contestá 409 «ese lugar ya se reservó».",
              desafio="Dejá que la base garantice la regla y convertí su error en un mensaje claro.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE reserva (viaje INTEGER, asiento INTEGER, persona TEXT)');
                  $reservar = $db->prepare('INSERT INTO reserva VALUES (?, ?, ?)');

                  foreach ([[1, 40, 'Olmo'], [1, 40, 'Lia']] as $r) {
                      $reservar->execute($r);
                      echo "201 Confirmado para {$r[2]}\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE reserva (viaje INTEGER, asiento INTEGER, persona TEXT, UNIQUE (viaje, asiento))');
                  $reservar = $db->prepare('INSERT INTO reserva VALUES (?, ?, ?)');

                  foreach ([[1, 40, 'Olmo'], [1, 40, 'Lia']] as $r) {
                      try {
                          $reservar->execute($r);
                          echo "201 Confirmado para {$r[2]}\\n";
                      } catch (PDOException $e) {
                          echo "409 Ese lugar ya se reservo ({$r[2]})\\n";
                      }
                  }
              ''',
              al_superar="Un solo lugar, una sola reserva. Lía recibe un mensaje claro y elige otro asiento. La Orca pierde una veta violeta.",
              imagen=["El último asiento de un ferry con dos manos tocando el mismo sello de reserva al mismo tiempo.",
                      FERMIN + " cruza los brazos.", NILO + " sostiene el sello.", GHECO + " sobre el asiento."]),
            m(id="S03-N03-P3", titulo="Sin pedidos superpuestos",
              lugar=PALOMAR, personajes="Nilo, Iara, Gheco",
              criatura="dragon",
              carta="Polling prolijo | se pregunta cada tanto si hay novedades · si un pedido no volvió, no se manda otro · se pide solo lo nuevo (desde el último id)",
              recompensa="xp 25, oro 30",
              escena="""
                  La página de novedades pregunta cada segundo, aunque la paloma anterior no haya vuelto. Las palomas se chocan en el aire y la Orca se las traga de a montones. Iara propone una regla: no se manda una paloma nueva si la anterior sigue en camino, y se pide solo lo nuevo.
              """,
              sugiere="Guardá el último id recibido y si hay un pedido en camino. En cada tic: si está en camino, se saltea; si no, se pide lo que tenga id mayor al último.",
              desafio="Completá el polling sin pedidos superpuestos.",
              inicial='''
                  <?php
                  $novedades = [1 => 'llego el ferry', 2 => 'salio la Gaviota', 3 => 'tormenta al norte'];
                  $tics = [['tic', 2], ['tic', 2], ['vuelve', 0], ['tic', 3], ['vuelve', 0]];
                  $ultimo = 0;
                  $enCamino = false;
                  foreach ($tics as [$evento, $hasta]) {
                      echo "Pido todo\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $novedades = [1 => 'llego el ferry', 2 => 'salio la Gaviota', 3 => 'tormenta al norte'];
                  $tics = [['tic', 2], ['tic', 2], ['vuelve', 0], ['tic', 3], ['vuelve', 0]];
                  $ultimo = 0;
                  $enCamino = false;
                  $pedidoHasta = 0;
                  foreach ($tics as [$evento, $hasta]) {
                      if ($evento === 'tic') {
                          if ($enCamino) {
                              echo "Tic: hay una paloma en camino, espero\\n";
                              continue;
                          }
                          $enCamino = true;
                          $pedidoHasta = $hasta;
                          echo "Tic: pido desde el $ultimo\\n";
                      } else {
                          foreach ($novedades as $id => $texto) {
                              if ($id > $ultimo && $id <= $pedidoHasta) {
                                  echo "Nuevo: $texto\\n";
                                  $ultimo = $id;
                              }
                          }
                          $enCamino = false;
                      }
                  }
              ''',
              al_superar="Las palomas ya no se chocan, y cada una trae solo lo nuevo. La Orca, sin nada que tragar, se va mar adentro. El palomar queda en paz.",
              imagen=["El palomar al atardecer con palomas saliendo de a una, ordenadas, y una orca alejándose en el horizonte.",
                      IARA + " anota en la libreta cada paloma que sale.", NILO + " suelta una paloma.", GHECO + " sobre el techo."]),
        ],
    },
]
