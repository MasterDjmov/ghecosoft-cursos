from genphp import m
from php_r01 import NILO, ELEFA, IARA, PICO, GHECO

CUPULA = "La cúpula del Faro"
MAQUINAS = "La sala de máquinas del Faro"
MAQUINAS_MSJ = "Los mensajes de las máquinas"
BANCO = "El banco de pruebas de la lámpara"
GUARDIA = "El libro de guardia"
LAMPARA = "La lámpara del Faro"
TORMENTA = "La noche de la tormenta"
ENCRUCIJADA = "La Encrucijada de los Sellos"
MAREA = "Marea (farera de 45, alta y fuerte, pelo gris ondulado con un pañuelo violeta, impermeable largo amarillo oscuro, farol de señales con un vidrio violeta y uno cian)"
DRAGON = "el Dragón del Faro (dragón marino negro y violeta enorme, alas como velas rotas, cuerpo de olas y relámpagos violetas, ojos como lámparas cian)"
IARA_R = IARA
FERMIN = "Fermín (anciano bajo y encorvado, barba blanca larga, anteojos redondos de bronce, guardapolvo gris, gorro de lana, farol cian)"

NODOS = [
    {
        "titulo": "R05-N01 · MVC sin framework: router y controladores",
        "misiones": [
            m(id="R05-N01-P1", titulo="Cada barco a su dársena",
              lugar=CUPULA, personajes="Nilo, Marea, Gheco",
              carta="Router | una tabla de rutas: 'GET /barcos' => controlador · llega el pedido, se busca su ruta y se llama a quien corresponde · no carga nada: dirige",
              recompensa="xp 10, oro 10",
              escena="""
                  En la punta del muelle más largo está **el Faro**: el mismo por el que llegó Nilo, con la lámpara apagada desde hace veinte años. En la cúpula lo espera **Marea, la farera**. Aunque el Faro no alumbra, ella sigue dirigiendo a los barcos: a cada uno le mira la bandera y le señala una dársena. —Cada barco, a su dársena —dice.
              """,
              sugiere="Un array de rutas con el método y la dirección como clave (`'GET /barcos'`) y una función como valor. El router busca la clave y llama a esa función.",
              desafio="Completá el router para que cada pedido vaya a su controlador.",
              inicial='''
                  <?php
                  $rutas = [
                      'GET /barcos' => fn () => 'Lista de barcos',
                      'GET /horarios' => fn () => 'Horario del ferry',
                  ];

                  function despachar(array $rutas, string $metodo, string $ruta): string
                  {
                      return 'Lista de barcos';
                  }

                  echo despachar($rutas, 'GET', '/barcos') . "\\n";
                  echo despachar($rutas, 'GET', '/horarios') . "\\n";
              ''',
              solucion='''
                  <?php
                  $rutas = [
                      'GET /barcos' => fn () => 'Lista de barcos',
                      'GET /horarios' => fn () => 'Horario del ferry',
                  ];

                  function despachar(array $rutas, string $metodo, string $ruta): string
                  {
                      $controlador = $rutas["$metodo $ruta"];
                      return $controlador();
                  }

                  echo despachar($rutas, 'GET', '/barcos') . "\\n";
                  echo despachar($rutas, 'GET', '/horarios') . "\\n";
              ''',
              al_superar="Cada pedido llega a su dársena. Marea asiente: —Así se dirige. Sin cargar nada.",
              imagen=["La cúpula de un faro de noche, con la lámpara apagada en el centro y el mar lleno de barcos con banderas abajo.",
                      MAREA + " señala con el farol una dársena.", NILO + " mira los barcos por la ventana.", GHECO + " sobre la lámpara apagada."]),
            m(id="R05-N01-P2", titulo="El barco que no tiene dársena",
              lugar=CUPULA, personajes="Nilo, Marea, Gheco",
              criatura="esqueleto",
              carta="404 y 405 | la ruta no existe: 404 · la ruta existe pero no con ese método: 405 · se distingue para avisar bien",
              recompensa="xp 15, oro 15",
              escena="""
                  Llega un barco con una bandera que nadie conoce y el router se rompe: `Undefined array key`. Un **esqueleto** sube por la escalera. Llega otro que quiere *borrar* el horario del ferry, algo que no se puede.
              """,
              sugiere="Si la ruta con ese método no está: fijate si la dirección existe con **otro** método (405) o no existe para nada (404).",
              desafio="Devolvé 404 o 405 según corresponda.",
              inicial='''
                  <?php
                  $rutas = ['GET /barcos' => fn () => '200 Lista de barcos', 'GET /horarios' => fn () => '200 Horario del ferry'];

                  function despachar(array $rutas, string $metodo, string $ruta): string
                  {
                      return $rutas["$metodo $ruta"]();
                  }

                  echo despachar($rutas, 'GET', '/barcos') . "\\n";
                  echo despachar($rutas, 'GET', '/fantasmas') . "\\n";
                  echo despachar($rutas, 'DELETE', '/horarios') . "\\n";
              ''',
              solucion='''
                  <?php
                  $rutas = ['GET /barcos' => fn () => '200 Lista de barcos', 'GET /horarios' => fn () => '200 Horario del ferry'];

                  function despachar(array $rutas, string $metodo, string $ruta): string
                  {
                      if (isset($rutas["$metodo $ruta"])) {
                          return $rutas["$metodo $ruta"]();
                      }
                      foreach (array_keys($rutas) as $clave) {
                          if (explode(' ', $clave, 2)[1] === $ruta) {
                              return "405 Metodo no permitido";
                          }
                      }
                      return "404 No encontrado";
                  }

                  echo despachar($rutas, 'GET', '/barcos') . "\\n";
                  echo despachar($rutas, 'GET', '/fantasmas') . "\\n";
                  echo despachar($rutas, 'DELETE', '/horarios') . "\\n";
              ''',
              al_superar="Cada barco raro recibe su respuesta honesta. El esqueleto baja la escalera, desilusionado.",
              imagen=["El mar de noche visto desde la cúpula del faro, con un barco de bandera rara dando vueltas sin dársena.",
                      MAREA + " cruza los brazos.", NILO + " agita una bandera roja.", "Un esqueleto chiquito subiendo la escalera de caracol.", GHECO + " sobre la baranda."]),
            m(id="R05-N01-P3", titulo="La ruta con número",
              lugar=CUPULA, personajes="Nilo, Gheco",
              carta="Parámetros de ruta | /barcos/12 → id 12 · preg_match('#^/barcos/(\\\\d+)$#', $ruta, $m) · $m[1] es el número",
              recompensa="xp 15, oro 15",
              escena="""
                  Los barcos ya no piden «la lista»: piden «el barco 12». Nilo escribió una ruta por cada barco, del 1 al 40, y el barco 41 se quedó afuera.
              """,
              sugiere="Una sola ruta con un patrón: `preg_match('#^/barcos/(\\d+)$#', $ruta, $m)` reconoce cualquier número, y `$m[1]` lo da.",
              desafio="Reconocé la ruta con el número y pasáselo al controlador.",
              inicial='''
                  <?php
                  function verBarco(int $id): string
                  {
                      return "Barco $id";
                  }

                  function despachar(string $ruta): string
                  {
                      if ($ruta === '/barcos/12') {
                          return verBarco(12);
                      }
                      return "404";
                  }

                  foreach (['/barcos/12', '/barcos/41', '/barcos/abc'] as $r) {
                      echo despachar($r) . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function verBarco(int $id): string
                  {
                      return "Barco $id";
                  }

                  function despachar(string $ruta): string
                  {
                      if (preg_match('#^/barcos/(\\d+)$#', $ruta, $m)) {
                          return verBarco((int) $m[1]);
                      }
                      return "404";
                  }

                  foreach (['/barcos/12', '/barcos/41', '/barcos/abc'] as $r) {
                      echo despachar($r) . "\\n";
                  }
              ''',
              al_superar="El barco 41 entra, y también el 42, el 43 y cualquiera que venga. «abc» no es un número: 404.",
              imagen=["Una fila larga de barcos con banderas de puntitos de distintos colores, entrando uno por uno al puerto.",
                      NILO + " anota en una libreta, por primera vez sin que se lo pidan.", GHECO + " sobre la libreta."]),
            m(id="R05-N01-P4", titulo="Modelo, vista y controlador",
              lugar=CUPULA, personajes="Nilo, Marea, Gheco",
              carta="MVC | el controlador recibe el pedido · le pide los datos al modelo · se los pasa a la vista · cada uno con su trabajo",
              recompensa="xp 15, oro 15",
              escena="""
                  El controlador de Nilo hace todo: busca los barcos, los filtra y arma el HTML. Cuando Marea quiere la misma lista en otro formato, hay que reescribirlo entero.
              """,
              sugiere="Separá: el **modelo** da los datos (`BarcoModelo::activos()`), la **vista** arma el texto (`vistaLista()`) y el **controlador** junta los dos.",
              desafio="Separá el controlador en modelo, vista y controlador.",
              inicial='''
                  <?php
                  function controladorBarcos(): string
                  {
                      $barcos = [['nombre' => 'Gaviota', 'activo' => true], ['nombre' => 'Tortuga', 'activo' => false], ['nombre' => 'Delfin', 'activo' => true]];
                      $html = "<ul>";
                      foreach ($barcos as $b) {
                          if ($b['activo']) {
                              $html .= "<li>{$b['nombre']}</li>";
                          }
                      }
                      return $html . "</ul>";
                  }

                  echo controladorBarcos() . "\\n";
              ''',
              solucion='''
                  <?php
                  final class BarcoModelo
                  {
                      public static function activos(): array
                      {
                          $barcos = [['nombre' => 'Gaviota', 'activo' => true], ['nombre' => 'Tortuga', 'activo' => false], ['nombre' => 'Delfin', 'activo' => true]];
                          return array_values(array_filter($barcos, fn ($b) => $b['activo']));
                      }
                  }

                  function vistaLista(array $barcos): string
                  {
                      return "<ul>" . implode('', array_map(fn ($b) => "<li>" . htmlspecialchars($b['nombre']) . "</li>", $barcos)) . "</ul>";
                  }

                  function vistaTexto(array $barcos): string
                  {
                      return implode(', ', array_column($barcos, 'nombre'));
                  }

                  function controladorBarcos(string $formato): string
                  {
                      $barcos = BarcoModelo::activos();
                      return $formato === 'texto' ? vistaTexto($barcos) : vistaLista($barcos);
                  }

                  echo controladorBarcos('html') . "\\n";
                  echo controladorBarcos('texto') . "\\n";
              ''',
              al_superar="La misma lista sale en dos formatos sin tocar el modelo. Marea la lee en voz alta, barco por barco.",
              imagen=["Tres mesas en la cúpula del faro: una con fichas de barcos, otra con un tablero de dibujos y otra con un timón, unidas por flechas de luz.",
                      MAREA + " pasa una ficha de una mesa a otra.", NILO + " sigue las flechas.", GHECO + " sobre el timón."]),
        ],
    },
    {
        "titulo": "R05-N02 · Closures, callables y generadores",
        "misiones": [
            m(id="R05-N02-P1", titulo="Las palancas intercambiables",
              lugar=MAQUINAS, personajes="Nilo, Gheco",
              carta="Closures | $f = fn ($x) => $x * 2; · una función guardada en una variable · se pasa a otra función · use ($tasa) trae una variable de afuera",
              recompensa="xp 10, oro 10",
              escena="""
                  En la sala de máquinas del Faro hay un tablero lleno de palancas intercambiables: cada palanca es una instrucción que se puede sacar y enchufar en otro lado. Nilo quiere una palanca que aplique un recargo, y que el porcentaje se pueda cambiar.
              """,
              sugiere="`function recargo(float $tasa): Closure { return fn ($precio) => $precio * (1 + $tasa); }` fabrica una palanca. Con `array_map` se aplica a todos los precios.",
              desafio="Escribí la fábrica de palancas y aplicá dos recargos distintos.",
              inicial='''
                  <?php
                  $precios = [100, 250, 40];

                  function recargo(float $tasa): Closure
                  {
                      return fn ($precio) => $precio;
                  }

                  echo implode(', ', array_map(recargo(0.1), $precios)) . "\\n";
                  echo implode(', ', array_map(recargo(0.5), $precios)) . "\\n";
              ''',
              solucion='''
                  <?php
                  $precios = [100, 250, 40];

                  function recargo(float $tasa): Closure
                  {
                      return fn ($precio) => round($precio * (1 + $tasa), 2);
                  }

                  echo implode(', ', array_map(recargo(0.1), $precios)) . "\\n";
                  echo implode(', ', array_map(recargo(0.5), $precios)) . "\\n";
              ''',
              al_superar="Dos palancas, una fábrica. Nilo saca una del tablero y la enchufa al revés. Por suerte, no pasa nada.",
              imagen=["Un tablero de bronce lleno de palancas de distintos colores enchufadas en una pared de la sala de máquinas del faro.",
                      NILO + " enchufa una palanca.", GHECO + " colgado de otra palanca."]),
            m(id="R05-N02-P2", titulo="La cinta en cadena",
              lugar=MAQUINAS, personajes="Nilo, Iara, Gheco",
              carta="Encadenar | array_filter elige · array_map transforma · array_reduce junta en un valor · usort ordena con una función",
              recompensa="xp 15, oro 15",
              escena="""
                  Iara pide el total de kilos de los barcos que van al Valle, en un solo número. Nilo escribió tres bucles uno detrás del otro, con variables por todos lados.
              """,
              sugiere="Filtrá los del Valle con `array_filter`, quedate con los kilos con `array_map` y sumalos con `array_reduce`.",
              desafio="Calculá el total encadenando las tres funciones.",
              inicial='''
                  <?php
                  $viajes = [
                      ['barco' => 'Gaviota', 'destino' => 'Valle', 'kilos' => 300],
                      ['barco' => 'Albatros', 'destino' => 'Forjas', 'kilos' => 820],
                      ['barco' => 'Tortuga', 'destino' => 'Valle', 'kilos' => 510],
                  ];
                  echo "Al Valle: ? kg\\n";
              ''',
              solucion='''
                  <?php
                  $viajes = [
                      ['barco' => 'Gaviota', 'destino' => 'Valle', 'kilos' => 300],
                      ['barco' => 'Albatros', 'destino' => 'Forjas', 'kilos' => 820],
                      ['barco' => 'Tortuga', 'destino' => 'Valle', 'kilos' => 510],
                  ];
                  $alValle = array_filter($viajes, fn ($v) => $v['destino'] === 'Valle');
                  $kilos = array_map(fn ($v) => $v['kilos'], $alValle);
                  $total = array_reduce($kilos, fn ($suma, $k) => $suma + $k, 0);
                  echo "Al Valle: $total kg\\n";
              ''',
              al_superar="Ochocientos diez kilos. Iara lo anota; Nilo borra sus tres bucles con alivio.",
              imagen=["Una cinta transportadora de bronce que pasa por tres máquinas: un colador, una prensa y una balanza.",
                      IARA + " mira la balanza del final.", NILO + " pone cajones en la cinta.", GHECO + " sobre la balanza."]),
            m(id="R05-N02-P3", titulo="De a un cajón",
              lugar=MAQUINAS, personajes="Nilo, Gheco",
              carta="Generadores | function cajones() { yield …; } · da los valores de a uno, a medida que se piden · no carga todo en memoria",
              recompensa="xp 15, oro 15",
              escena="""
                  La cinta trae cajones desde la bodega. Nilo intenta bajar todos juntos «para ganar tiempo» y la cinta se traba con un crujido. Marea lo mira sin decir nada.
              """,
              sugiere="Una función con `yield` da los cajones de a uno: `foreach (cajones(5) as $c)` los recibe a medida que los necesita.",
              desafio="Convertí la función en un generador que entregue de a un cajón.",
              inicial='''
                  <?php
                  function cajones(int $cantidad): array
                  {
                      $todos = [];
                      for ($i = 1; $i <= $cantidad; $i++) {
                          $todos[] = "cajon $i";
                      }
                      return $todos;
                  }

                  $c = cajones(5);
                  echo "Tipo: " . get_debug_type($c) . "\\n";
                  foreach ($c as $cajon) {
                      echo "Llega el $cajon\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function cajones(int $cantidad): Generator
                  {
                      for ($i = 1; $i <= $cantidad; $i++) {
                          yield "cajon $i";
                      }
                  }

                  $c = cajones(5);
                  echo "Tipo: " . get_debug_type($c) . "\\n";
                  foreach ($c as $cajon) {
                      echo "Llega el $cajon\\n";
                  }
              ''',
              al_superar="Los cajones llegan de a uno, sin trabar la cinta. Podrían ser cinco o cinco millones.",
              imagen=["Una cinta transportadora que sale de un túnel oscuro trayendo un solo cajón a la vez, en fila, con espacio entre ellos.",
                      NILO + " recibe un cajón.", GHECO + " sentado en el próximo cajón."]),
            m(id="R05-N02-P4", titulo="Ordenar con una función",
              lugar=MAQUINAS, personajes="Nilo, Gheco",
              carta="usort | usort($lista, fn ($a, $b) => $a['kilos'] <=> $b['kilos']) · la función dice quién va primero · para varios criterios: [$a1, $a2] <=> [$b1, $b2]",
              recompensa="xp 10, oro 10",
              escena="""
                  Marea quiere que los barcos entren por destino y, dentro de cada destino, del más liviano al más pesado. Nilo los ordenó solo por destino y los cargueros pesados entran primero, tapando la dársena.
              """,
              sugiere="`usort` con la nave espacial sobre dos criterios: `[$a['destino'], $a['kilos']] <=> [$b['destino'], $b['kilos']]`.",
              desafio="Ordená por destino y después por kilos.",
              inicial='''
                  <?php
                  $barcos = [
                      ['nombre' => 'Albatros', 'destino' => 'Valle', 'kilos' => 820],
                      ['nombre' => 'Gaviota', 'destino' => 'Forjas', 'kilos' => 300],
                      ['nombre' => 'Delfin', 'destino' => 'Valle', 'kilos' => 90],
                      ['nombre' => 'Condor', 'destino' => 'Forjas', 'kilos' => 760],
                  ];
                  usort($barcos, fn ($a, $b) => $a['destino'] <=> $b['destino']);
                  foreach ($barcos as $b) {
                      echo "{$b['destino']}: {$b['nombre']} ({$b['kilos']})\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $barcos = [
                      ['nombre' => 'Albatros', 'destino' => 'Valle', 'kilos' => 820],
                      ['nombre' => 'Gaviota', 'destino' => 'Forjas', 'kilos' => 300],
                      ['nombre' => 'Delfin', 'destino' => 'Valle', 'kilos' => 90],
                      ['nombre' => 'Condor', 'destino' => 'Forjas', 'kilos' => 760],
                  ];
                  usort($barcos, fn ($a, $b) => [$a['destino'], $a['kilos']] <=> [$b['destino'], $b['kilos']]);
                  foreach ($barcos as $b) {
                      echo "{$b['destino']}: {$b['nombre']} ({$b['kilos']})\\n";
                  }
              ''',
              al_superar="Los livianos entran primero y la dársena no se tapa. Marea baja el farol.",
              imagen=["Barcos de distintos tamaños haciendo fila en dos columnas frente al faro, de chicos a grandes.",
                      NILO + " ordena la fila con una bandera.", GHECO + " sobre el barco más chico."]),
        ],
    },
    {
        "titulo": "R05-N03 · Una API REST en JSON",
        "misiones": [
            m(id="R05-N03-P1", titulo="Las máquinas no quieren gaviotas",
              lugar=MAQUINAS_MSJ, personajes="Nilo, Gheco",
              carta="Responder JSON | header('Content-Type: application/json') · echo json_encode($datos) · las máquinas leen datos, no colores",
              recompensa="xp 10, oro 10",
              escena="""
                  A la torre del Faro llegan mensajes de otras máquinas: la aduana pregunta qué barcos llegaron hoy. Nilo les contesta con una página llena de colores y una gaviota dibujada. Las máquinas no entienden nada.
              """,
              sugiere="Respondé con `json_encode($barcos)`: datos ordenados que cualquier máquina entiende. Con `JSON_PRETTY_PRINT` queda legible para las personas también.",
              desafio="Contestá en JSON.",
              inicial='''
                  <?php
                  $barcos = [['nombre' => 'Gaviota', 'kilos' => 300], ['nombre' => 'Albatros', 'kilos' => 820]];
                  echo "<h1 style='color:violet'>Barcos de hoy</h1> (con una gaviota dibujada)\\n";
              ''',
              solucion='''
                  <?php
                  $barcos = [['nombre' => 'Gaviota', 'kilos' => 300], ['nombre' => 'Albatros', 'kilos' => 820]];
                  echo json_encode(['datos' => $barcos], JSON_PRETTY_PRINT) . "\\n";
              ''',
              al_superar="La aduana lee los datos al instante y contesta con un «gracias» en JSON. Nilo lo enmarca.",
              imagen=["Una máquina de bronce con lucecitas que recibe un papel con llaves y corchetes dibujados como adornos, sin letras.",
                      NILO + " le da el papel a la máquina.", GHECO + " sobre la máquina."]),
            m(id="R05-N03-P2", titulo="Leer lo que mandan",
              lugar=MAQUINAS_MSJ, personajes="Nilo, Gheco",
              criatura="goblin",
              carta="Cuerpo JSON | json_decode(file_get_contents('php://input'), true) · si viene roto, json_decode da null: 400 · json_last_error_msg() dice por qué",
              recompensa="xp 15, oro 15",
              escena="""
                  El correo de otro puerto manda paquetes para registrar en JSON. Uno llegó roto, con una llave sin cerrar, y el programa de Nilo lo registró como un paquete vacío. Un **goblin** se lo llevó.
              """,
              sugiere="Decodificá con `json_decode($cuerpo, true)`. Si da `null` y el cuerpo no era `null`, el JSON está roto: se responde 400 con el motivo.",
              desafio="Rechazá con 400 el cuerpo roto y registrá el bueno.",
              inicial='''
                  <?php
                  function registrar(string $cuerpo): string
                  {
                      $datos = json_decode($cuerpo, true);
                      return "201 Registrado: " . ($datos['contenido'] ?? '');
                  }

                  echo registrar('{"contenido": "telas", "kilos": 12}') . "\\n";
                  echo registrar('{"contenido": "sal", "kilos": ') . "\\n";
              ''',
              solucion='''
                  <?php
                  function registrar(string $cuerpo): string
                  {
                      $datos = json_decode($cuerpo, true);
                      if (!is_array($datos)) {
                          return "400 JSON invalido: " . json_last_error_msg();
                      }
                      return "201 Registrado: " . ($datos['contenido'] ?? '');
                  }

                  echo registrar('{"contenido": "telas", "kilos": 12}') . "\\n";
                  echo registrar('{"contenido": "sal", "kilos": ') . "\\n";
              ''',
              al_superar="El paquete roto vuelve con su 400 y el motivo. El otro puerto lo arregla y lo manda de nuevo. El goblin se queda con las manos vacías.",
              imagen=["Un paquete de papel madera roto en una esquina sobre una mesa del faro, con la cuerda suelta.",
                      "Un goblin flaco intentando llevarse el paquete.", NILO + " lo sostiene con una mano.", GHECO + " sobre la cuerda."]),
            m(id="R05-N03-P3", titulo="Cada acción, su método",
              lugar=MAQUINAS_MSJ, personajes="Nilo, Marea, Gheco",
              carta="REST | GET /envios lista · GET /envios/3 uno · POST /envios crea (201) · PUT modifica · DELETE borra (204) · cada respuesta con su código",
              recompensa="xp 15, oro 15",
              escena="""
                  Marea propone que la API de envíos hable como un faro: una señal para cada cosa. Leer, crear y borrar con el mismo método es como prender la misma luz para todo.
              """,
              sugiere="Una función `api()` que según el método y si hay un id, lista, muestra, crea o borra, y devuelve el código que corresponde.",
              desafio="Completá la API con los cuatro casos y sus códigos.",
              inicial='''
                  <?php
                  $envios = [1 => 'telas', 2 => 'sal'];

                  function api(array &$envios, string $metodo, ?int $id, ?string $contenido = null): string
                  {
                      return "200 " . json_encode($envios);
                  }

                  echo api($envios, 'GET', null) . "\\n";
                  echo api($envios, 'POST', null, 'yerba') . "\\n";
                  echo api($envios, 'GET', 3) . "\\n";
                  echo api($envios, 'DELETE', 1) . "\\n";
                  echo api($envios, 'GET', 1) . "\\n";
              ''',
              solucion='''
                  <?php
                  $envios = [1 => 'telas', 2 => 'sal'];

                  function api(array &$envios, string $metodo, ?int $id, ?string $contenido = null): string
                  {
                      if ($metodo === 'GET' && $id === null) {
                          return "200 " . json_encode($envios);
                      }
                      if ($metodo === 'POST' && $id === null) {
                          $nuevo = max(array_keys($envios)) + 1;
                          $envios[$nuevo] = $contenido;
                          return "201 " . json_encode(['id' => $nuevo, 'contenido' => $contenido]);
                      }
                      if (!isset($envios[$id])) {
                          return "404 " . json_encode(['error' => "no existe el envio $id"]);
                      }
                      if ($metodo === 'GET') {
                          return "200 " . json_encode(['id' => $id, 'contenido' => $envios[$id]]);
                      }
                      if ($metodo === 'DELETE') {
                          unset($envios[$id]);
                          return "204";
                      }
                      return "405";
                  }

                  echo api($envios, 'GET', null) . "\\n";
                  echo api($envios, 'POST', null, 'yerba') . "\\n";
                  echo api($envios, 'GET', 3) . "\\n";
                  echo api($envios, 'DELETE', 1) . "\\n";
                  echo api($envios, 'GET', 1) . "\\n";
              ''',
              al_superar="Cada pedido recibe su señal. Marea prende el farol en violeta para los 201 y en cian para los 200, por puro gusto.",
              imagen=["La ventana del faro con un farol de señales que alterna una luz violeta y una cian hacia el mar.",
                      MAREA + " cambia el vidrio del farol.", NILO + " anota las señales en una libreta.", GHECO + " sobre el farol."]),
            m(id="R05-N03-P4", titulo="422: lo que no se puede procesar",
              lugar=MAQUINAS_MSJ, personajes="Nilo, Gheco",
              carta="Errores en JSON | 400 el pedido está mal armado · 422 está bien armado pero los datos no sirven · {\"errores\": {\"campo\": \"motivo\"}}",
              recompensa="xp 15, oro 15",
              escena="""
                  Una aplicación manda un envío con kilos negativos y sin destino. El JSON está bien armado, pero los datos no sirven. La API de Nilo contesta «400», y la aplicación no sabe qué corregir.
              """,
              sugiere="Si el JSON se pudo leer pero los datos no pasan la validación, es **422**, con los errores por campo en el cuerpo.",
              desafio="Devolvé 422 con los errores de cada campo.",
              inicial='''
                  <?php
                  function crearEnvio(array $datos): string
                  {
                      if (($datos['kilos'] ?? 0) <= 0 || ($datos['destino'] ?? '') === '') {
                          return "400";
                      }
                      return "201";
                  }

                  echo crearEnvio(['kilos' => -3]) . "\\n";
                  echo crearEnvio(['kilos' => 8, 'destino' => 'Valle']) . "\\n";
              ''',
              solucion='''
                  <?php
                  function crearEnvio(array $datos): string
                  {
                      $errores = [];
                      if (!is_int($datos['kilos'] ?? null) || $datos['kilos'] <= 0) {
                          $errores['kilos'] = 'tiene que ser un entero positivo';
                      }
                      if (trim($datos['destino'] ?? '') === '') {
                          $errores['destino'] = 'es obligatorio';
                      }
                      if ($errores !== []) {
                          return "422 " . json_encode(['errores' => $errores]);
                      }
                      return "201";
                  }

                  echo crearEnvio(['kilos' => -3]) . "\\n";
                  echo crearEnvio(['kilos' => 8, 'destino' => 'Valle']) . "\\n";
              ''',
              al_superar="La aplicación lee los dos errores, corrige y vuelve a mandar. Esta vez, 201.",
              imagen=["Una máquina de bronce del faro que devuelve un papel con dos marcas rojas y recibe otro con un tilde verde.",
                      NILO + " entre la máquina y el papel.", GHECO + " sobre la máquina."]),
        ],
    },
    {
        "titulo": "R05-N04 · Pruebas con PHPUnit",
        "misiones": [
            m(id="R05-N04-P1", titulo="El banco de pruebas",
              lugar=BANCO, personajes="Nilo, Gheco",
              carta="Probar | se escribe lo que se espera y se compara con lo que sale · si no coincide, la prueba falla y dice dónde · con PHPUnit: $this->assertSame($esperado, $real)",
              recompensa="xp 10, oro 10",
              escena="""
                  El ingeniero del Faro revisaba la lámpara a mano cada noche. Un día se enfermó y nadie supo cómo revisarla. Desde entonces hay un **banco de pruebas**: se aprieta un botón y prueba las cuarenta cosas, siempre igual. Nilo lo mira con envidia: es una máquina que no se olvida de nada.
              """,
              sugiere="En el navegador no hay PHPUnit, así que acá armamos la idea con una función `afirmar($esperado, $real, $nombre)` que dice «ok» o «FALLA». En tu compu, las misiones usan PHPUnit de verdad.",
              desafio="Completá `afirmar` y encontrá la prueba que falla.",
              inicial='''
                  <?php
                  function tarifa(int $kilos): int
                  {
                      return $kilos * 3 + 10;
                  }

                  function afirmar(mixed $esperado, mixed $real, string $nombre): void
                  {
                  }

                  afirmar(10, tarifa(0), 'sin carga paga el despacho');
                  afirmar(40, tarifa(10), 'diez kilos');
                  afirmar(300, tarifa(100), 'cien kilos');
              ''',
              solucion='''
                  <?php
                  function tarifa(int $kilos): int
                  {
                      return $kilos * 3 + 10;
                  }

                  function afirmar(mixed $esperado, mixed $real, string $nombre): void
                  {
                      if ($esperado === $real) {
                          echo "ok    $nombre\\n";
                      } else {
                          echo "FALLA $nombre: esperaba " . var_export($esperado, true) . " y dio " . var_export($real, true) . "\\n";
                      }
                  }

                  afirmar(10, tarifa(0), 'sin carga paga el despacho');
                  afirmar(40, tarifa(10), 'diez kilos');
                  afirmar(300, tarifa(100), 'cien kilos');
              ''',
              al_superar="Dos pruebas pasan y una falla: esperaba 300 y dio 310. Nilo hace la cuenta a mano: 3 × 100 + 10 = 310. La tarifa estaba bien; la que estaba mal escrita era la prueba. La corrige, y el banco queda en verde.",
              imagen=["Un banco de pruebas de bronce junto a la lámpara del faro, con tres lucecitas: dos verdes y una que parpadea.",
                      NILO + " aprieta el botón del banco.", GHECO + " sobre las lucecitas."]),
            m(id="R05-N04-P2", titulo="La excepción esperada",
              lugar=BANCO, personajes="Nilo, Gheco",
              carta="Probar errores | también se prueba que falle cuando tiene que fallar · con PHPUnit: $this->expectException(InvalidArgumentException::class)",
              recompensa="xp 15, oro 15",
              escena="""
                  La lámpara no debe prenderse con una intensidad negativa. Nilo probó solo los casos buenos, y nadie se dio cuenta de que con -5 la lámpara se prendía igual, al revés.
              """,
              sugiere="Una prueba que llama con -5 y espera que se lance `InvalidArgumentException`: si no se lanza, la prueba falla.",
              desafio="Hacé que `prender` rechace lo negativo y que la prueba lo compruebe.",
              inicial='''
                  <?php
                  function prender(int $intensidad): string
                  {
                      return "Lampara al $intensidad%";
                  }

                  function esperaExcepcion(callable $codigo, string $nombre): void
                  {
                      try {
                          $codigo();
                          echo "FALLA $nombre: no lanzo nada\\n";
                      } catch (InvalidArgumentException $e) {
                          echo "ok    $nombre\\n";
                      }
                  }

                  echo prender(80) . "\\n";
                  esperaExcepcion(fn () => prender(-5), 'rechaza lo negativo');
              ''',
              solucion='''
                  <?php
                  function prender(int $intensidad): string
                  {
                      if ($intensidad < 0 || $intensidad > 100) {
                          throw new InvalidArgumentException("intensidad imposible: $intensidad");
                      }
                      return "Lampara al $intensidad%";
                  }

                  function esperaExcepcion(callable $codigo, string $nombre): void
                  {
                      try {
                          $codigo();
                          echo "FALLA $nombre: no lanzo nada\\n";
                      } catch (InvalidArgumentException $e) {
                          echo "ok    $nombre\\n";
                      }
                  }

                  echo prender(80) . "\\n";
                  esperaExcepcion(fn () => prender(-5), 'rechaza lo negativo');
              ''',
              al_superar="La lámpara ya no se prende al revés, y el banco de pruebas lo vigila para siempre.",
              imagen=["La lámpara enorme del faro con una perilla de intensidad de bronce y una traba roja en la zona baja.",
                      NILO + " gira la perilla.", GHECO + " sobre la traba."]),
            m(id="R05-N04-P3", titulo="Muchos casos, una prueba",
              lugar=BANCO, personajes="Nilo, Iara, Gheco",
              carta="Proveedor de datos | una lista de casos [entrada, esperado] · la misma prueba con cada uno · con PHPUnit: #[DataProvider('casos')]",
              recompensa="xp 15, oro 15",
              escena="""
                  Iara tiene una lista de veinte pesos con la tarifa que corresponde a cada uno. Nilo escribió veinte pruebas casi iguales y en la catorce copió mal el número.
              """,
              sugiere="Una lista de casos `[kilos, esperado]` y un `foreach` que prueba cada uno con la misma función.",
              desafio="Probá la tarifa con la lista de casos de Iara.",
              inicial='''
                  <?php
                  function tarifa(int $kilos): int
                  {
                      return $kilos <= 0 ? 0 : $kilos * 3 + 10;
                  }

                  $casos = [[0, 0], [1, 13], [10, 40], [-4, 0]];
                  echo "Casos probados: 0\\n";
              ''',
              solucion='''
                  <?php
                  function tarifa(int $kilos): int
                  {
                      return $kilos <= 0 ? 0 : $kilos * 3 + 10;
                  }

                  $casos = [[0, 0], [1, 13], [10, 40], [-4, 0]];
                  $fallas = 0;
                  foreach ($casos as [$kilos, $esperado]) {
                      $real = tarifa($kilos);
                      if ($real !== $esperado) {
                          $fallas++;
                          echo "FALLA con $kilos kg: esperaba $esperado y dio $real\\n";
                      }
                  }
                  echo "Casos probados: " . count($casos) . ", fallas: $fallas\\n";
              ''',
              al_superar="Cuatro casos, una sola prueba. Iara le pasa los otros dieciséis.",
              imagen=["Una hoja larga de la libreta de Iara con pares de pesitas y monedas dibujadas, colgando del banco de pruebas.",
                      IARA + " le pasa la hoja.", NILO + " la engancha en el banco.", GHECO + " sobre la hoja."]),
        ],
    },
    {
        "titulo": "R05-N05 · Errores, logs y configuración",
        "misiones": [
            m(id="R05-N05-P1", titulo="El libro de guardia",
              lugar=GUARDIA, personajes="Nilo, Iara, Gheco",
              carta="Log | cada cosa que pasa, con hora, nivel y mensaje · niveles: DEBUG, INFO, WARNING, ERROR · se escribe en un archivo, no en la pantalla",
              recompensa="xp 10, oro 10",
              escena="""
                  Una madrugada, la lámpara de prueba se apagó y nadie sabía por qué: Nilo, que estaba de guardia, solo recordaba «un ruido raro». Desde entonces hay un **libro de guardia**. Esa noche, por primera vez en el viaje, Nilo anota **todo**. Iara lee el libro de punta a punta y se tiene que sentar.
              """,
              sugiere="Una clase `Registro` con `anotar(string $nivel, string $mensaje)` que guarda el renglón con la hora que le pasan (acá fija, para que el ejemplo dé siempre igual) y lo escribe en un archivo con `FILE_APPEND`.",
              desafio="Completá el registro y anotá los tres sucesos.",
              inicial='''
                  <?php
                  final class Registro
                  {
                      public function __construct(private string $archivo)
                      {
                      }

                      public function anotar(string $hora, string $nivel, string $mensaje): void
                      {
                      }
                  }

                  $libro = new Registro('guardia.log');
                  $libro->anotar('02:10', 'INFO', 'lampara encendida');
                  $libro->anotar('03:47', 'WARNING', 'ruido raro en el motor');
                  $libro->anotar('03:52', 'ERROR', 'lampara apagada');
                  echo is_file('guardia.log') ? file_get_contents('guardia.log') : "(el libro esta vacio)\\n";
              ''',
              solucion='''
                  <?php
                  final class Registro
                  {
                      public function __construct(private string $archivo)
                      {
                      }

                      public function anotar(string $hora, string $nivel, string $mensaje): void
                      {
                          file_put_contents($this->archivo, "[$hora] $nivel: $mensaje\\n", FILE_APPEND);
                      }
                  }

                  $libro = new Registro('guardia.log');
                  $libro->anotar('02:10', 'INFO', 'lampara encendida');
                  $libro->anotar('03:47', 'WARNING', 'ruido raro en el motor');
                  $libro->anotar('03:52', 'ERROR', 'lampara apagada');
                  echo is_file('guardia.log') ? file_get_contents('guardia.log') : "(el libro esta vacio)\\n";
              ''',
              al_superar="A las 3:47, un ruido raro; a las 3:52, la lámpara apagada. Ahora se sabe. Iara, sentada, le aplaude a Nilo despacito.",
              imagen=["Un libro grueso abierto sobre una mesa en la cúpula del faro, lleno de renglones de rayitas, con una vela al lado.",
                      NILO + " escribe en el libro con concentración.", IARA + " sentada, con la boca abierta.", GHECO + " sobre la vela."]),
            m(id="R05-N05-P2", titulo="Del aviso a la excepción",
              lugar=GUARDIA, personajes="Nilo, Gheco",
              criatura="orco",
              carta="set_error_handler | convierte los avisos (Warning) en excepciones · así no pasan callados · se restaura con restore_error_handler()",
              recompensa="xp 15, oro 15",
              escena="""
                  Un **orco** pide la clave `'presion'` de un sensor que no la tiene. PHP avisa con un `Warning`, sigue con `null`, y la lámpara calcula con un cero que nadie pidió.
              """,
              sugiere="`set_error_handler` recibe una función que lanza `ErrorException`. Así el aviso corta el programa y se puede atrapar.",
              desafio="Convertí el aviso en una excepción y atrapala.",
              inicial='''
                  <?php
                  $sensor = ['temperatura' => 40];

                  try {
                      $presion = $sensor['presion'];
                      echo "Presion: " . ($presion * 2) . "\\n";
                  } catch (ErrorException $e) {
                      echo "Detenido: " . $e->getMessage() . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  set_error_handler(function (int $nivel, string $mensaje): bool {
                      throw new ErrorException($mensaje, 0, $nivel);
                  });

                  $sensor = ['temperatura' => 40];

                  try {
                      $presion = $sensor['presion'];
                      echo "Presion: " . ($presion * 2) . "\\n";
                  } catch (ErrorException $e) {
                      echo "Detenido: " . $e->getMessage() . "\\n";
                  }
                  restore_error_handler();
              ''',
              al_superar="El aviso ya no pasa callado: frena todo y dice qué faltaba. El orco se va a buscar un sensor menos vigilado.",
              imagen=["Un panel de sensores con relojitos de aguja lisos en la sala de máquinas, uno con la aguja suelta.",
                      "Un orco asoma detrás del panel.", NILO + " con el libro de guardia bajo el brazo.", GHECO + " sobre un relojito."]),
            m(id="R05-N05-P3", titulo="Fuera de servicio",
              lugar=GUARDIA, personajes="Nilo, Marea, Gheco",
              carta="Desarrollo y producción | en la compu: mostrar todo · en el servidor: display_errors=0, al visitante un mensaje amable, el detalle al log",
              recompensa="xp 15, oro 15",
              escena="""
                  En la puerta del Faro hay un cartel para los visitantes: *«Faro momentáneamente fuera de servicio»*, sin detalles técnicos. El sistema de Nilo, en cambio, le mostraba al visitante la ruta de los archivos y la línea del error.
              """,
              sugiere="Según el entorno: en `desarrollo` se muestra el detalle; en `produccion`, el mensaje amable para el visitante y el detalle al registro.",
              desafio="Mostrá lo que corresponde en cada entorno.",
              inicial='''
                  <?php
                  function paginaDeError(Throwable $e, string $entorno, array &$log): string
                  {
                      return "Error en " . $e->getFile() . ": " . $e->getMessage();
                  }

                  $log = [];
                  $e = new RuntimeException('no hay aceite en la lampara');
                  echo paginaDeError($e, 'produccion', $log) . "\\n";
                  echo "Renglones en el log: " . count($log) . "\\n";
              ''',
              solucion='''
                  <?php
                  function paginaDeError(Throwable $e, string $entorno, array &$log): string
                  {
                      if ($entorno === 'desarrollo') {
                          return "Error: " . $e->getMessage();
                      }
                      $log[] = "ERROR: " . $e->getMessage();
                      return "Faro momentaneamente fuera de servicio";
                  }

                  $log = [];
                  $e = new RuntimeException('no hay aceite en la lampara');
                  echo paginaDeError($e, 'desarrollo', $log) . "\\n";
                  echo paginaDeError($e, 'produccion', $log) . "\\n";
                  echo "Renglones en el log: " . count($log) . "\\n";
              ''',
              al_superar="El visitante ve el cartel amable; Marea lee el detalle en el log. Le falta aceite a la lámpara.",
              imagen=["La puerta del faro con un cartel liso de madera con el dibujo de una lámpara tachada, sin letras.",
                      MAREA + " cuelga el cartel.", NILO + " le alcanza una aceitera.", GHECO + " sobre el cartel."]),
            m(id="R05-N05-P4", titulo="Lo que cambia, en la configuración",
              lugar=GUARDIA, personajes="Nilo, Gheco",
              carta=".env | lo que cambia entre la compu y el servidor (claves, base, modo) va en un archivo aparte · nunca en el código · nunca en git",
              recompensa="xp 10, oro 10",
              escena="""
                  La clave de la base de datos del Faro estaba escrita en el medio del código. Cuando Nilo lo compartió para pedir ayuda, la clave viajó con él. Pico se la sabía al día siguiente.
              """,
              sugiere="Leé un archivo `.env` con renglones `CLAVE=valor` y armá un array de configuración. El código pide `$config['DB_PASS']`, sin saber cuál es.",
              desafio="Leé la configuración del archivo `.env`.",
              inicial='''
                  <?php
                  file_put_contents('.env', "APP_ENV=produccion\\nDB_NAME=faro\\nDB_PASS=no-se-lo-digas-a-pico\\n");

                  $config = ['APP_ENV' => 'desarrollo', 'DB_PASS' => 'faro123'];
                  echo "Entorno: {$config['APP_ENV']}\\n";
                  echo "Base: " . ($config['DB_NAME'] ?? '?') . "\\n";
                  echo "Clave cargada: " . (strlen($config['DB_PASS']) > 0 ? 'si' : 'no') . "\\n";
              ''',
              solucion='''
                  <?php
                  file_put_contents('.env', "APP_ENV=produccion\\nDB_NAME=faro\\nDB_PASS=no-se-lo-digas-a-pico\\n");

                  $config = [];
                  foreach (file('.env', FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $renglon) {
                      [$clave, $valor] = explode('=', $renglon, 2);
                      $config[trim($clave)] = trim($valor);
                  }
                  echo "Entorno: {$config['APP_ENV']}\\n";
                  echo "Base: " . ($config['DB_NAME'] ?? '?') . "\\n";
                  echo "Clave cargada: " . (strlen($config['DB_PASS']) > 0 ? 'si' : 'no') . "\\n";
              ''',
              al_superar="La clave vive en su archivo, lejos del código que se comparte. Pico tendrá que averiguarla de otra manera.",
              imagen=["Un cofrecito de madera cerrado con un candado chiquito, sobre la mesa del faro, al lado de un libro abierto.",
                      PICO + " mira el cofrecito con interés.", NILO + " lo tapa con la mano.", GHECO + " sobre el candado."]),
        ],
    },
    {
        "titulo": "R05-N06 · Subir a un hosting",
        "misiones": [
            m(id="R05-N06-P1", titulo="La lista de la mudanza",
              lugar=LAMPARA, personajes="Nilo, Elefa, Gheco",
              carta="Antes de subir | public/ como raíz · .env de producción · sin dependencias de desarrollo · HTTPS · probar después · con una lista, no de memoria",
              recompensa="xp 10, oro 10",
              escena="""
                  Para que los barcos de verdad vean el sistema, hay que llevarlo a la costa. Elefa le entrega a Nilo un papel con tres cosas: *un dominio, un hosting, una base de datos*. —Si lo hacés con una lista, la mudanza sale bien. Si lo hacés de memoria —y lo mira— siempre se olvida algo.
              """,
              sugiere="Recorré la lista de chequeo contra lo que está preparado y mostrá lo que falta.",
              desafio="Mostrá qué falta para poder subir.",
              inicial='''
                  <?php
                  $lista = ['raiz en public/', '.env de produccion', 'composer sin --dev', 'HTTPS', 'base importada'];
                  $listo = ['raiz en public/', 'HTTPS', 'base importada'];
                  echo "Todo listo para subir\\n";
              ''',
              solucion='''
                  <?php
                  $lista = ['raiz en public/', '.env de produccion', 'composer sin --dev', 'HTTPS', 'base importada'];
                  $listo = ['raiz en public/', 'HTTPS', 'base importada'];
                  $falta = array_diff($lista, $listo);
                  if ($falta === []) {
                      echo "Todo listo para subir\\n";
                  } else {
                      foreach ($falta as $f) {
                          echo "Falta: $f\\n";
                      }
                  }
              ''',
              al_superar="Faltan dos cosas, y ahora se sabe cuáles. Elefa asiente: la mudanza no va a olvidar nada.",
              imagen=["Una lista larga de papel con casilleros, algunos tildados, clavada en la pared del faro, sin letras.",
                      ELEFA + " señala un casillero vacío con el bastón.", NILO + " con una caja de mudanza en los brazos.", GHECO + " sobre la caja."]),
            m(id="R05-N06-P2", titulo="Lo privado no se ve",
              lugar=LAMPARA, personajes="Nilo, Gheco",
              criatura="troll",
              carta="Raíz pública | solo public/ se ve desde la web · .env, src/, vendor/ quedan afuera · si alguien pide /.env: 403 o 404",
              recompensa="xp 15, oro 15",
              escena="""
                  En el primer intento de subida, el `.env` quedó dentro de la carpeta pública y cualquiera lo podía bajar escribiendo `/.env`. Un **troll** ya lo estaba leyendo.
              """,
              sugiere="Una función que decide si una dirección se puede servir: solo lo que está bajo `public/` y no empieza con punto.",
              desafio="Escribí la regla que protege lo privado.",
              inicial='''
                  <?php
                  function sePuedeVer(string $ruta): bool
                  {
                      return true;
                  }

                  foreach (['/index.php', '/css/faro.css', '/.env', '/../src/Faro.php'] as $r) {
                      echo $r . ": " . (sePuedeVer($r) ? '200' : '403') . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function sePuedeVer(string $ruta): bool
                  {
                      if (str_contains($ruta, '..')) {
                          return false;
                      }
                      foreach (explode('/', trim($ruta, '/')) as $parte) {
                          if (str_starts_with($parte, '.')) {
                              return false;
                          }
                      }
                      return true;
                  }

                  foreach (['/index.php', '/css/faro.css', '/.env', '/../src/Faro.php'] as $r) {
                      echo $r . ": " . (sePuedeVer($r) ? '200' : '403') . "\\n";
                  }
              ''',
              al_superar="El `.env` deja de verse. El troll se queda mirando una puerta cerrada.",
              imagen=["Dos habitaciones del faro: una con la puerta abierta y llena de luz, otra cerrada con candado.",
                      "Un troll pegado a la puerta cerrada, mirando por la cerradura.", NILO + " le pone el candado.", GHECO + " sobre el candado."]),
            m(id="R05-N06-P3", titulo="La lente es un vitral",
              lugar=LAMPARA, personajes="Nilo, Marea, Gheco",
              carta="Diagnóstico | después de subir, un script revisa: versión de PHP, extensiones, carpetas con permiso de escritura, conexión a la base · y se borra",
              recompensa="xp 15, oro 15",
              escena="""
                  Limpiando la lámpara grande para la mudanza, Nilo y Marea descubren que la lente no es de vidrio común: es **un vitral**, con el plomo trabajado como el de las Forjas. El faro por el que llegó Nilo no es solo un faro. Antes de seguir, Marea le pide revisar que todo esté en su lugar.
              """,
              sugiere="Revisá cada requisito con lo que tiene el servidor (`PHP_VERSION`, `extension_loaded`) y mostrá ok o falta. Usá `version_compare`.",
              desafio="Completá el diagnóstico.",
              inicial='''
                  <?php
                  $requisitos = ['php' => '8.2.0', 'extensiones' => ['pdo', 'json', 'mbstring']];
                  echo "Diagnostico: todo bien\\n";
              ''',
              solucion='''
                  <?php
                  $requisitos = ['php' => '8.2.0', 'extensiones' => ['pdo', 'json', 'mbstring']];
                  $ok = version_compare(PHP_VERSION, $requisitos['php'], '>=');
                  echo "PHP 8.2 o mas nuevo: " . ($ok ? 'ok' : 'falta') . "\\n";
                  foreach ($requisitos['extensiones'] as $ext) {
                      echo "Extension $ext: " . (extension_loaded($ext) ? 'ok' : 'falta') . "\\n";
                  }
              ''',
              al_superar="Todo en su lugar. Marea limpia la lente con la manga y la luz del farol de señales pasa a través de ella en cuatro colores.",
              imagen=["La lente enorme de la lámpara del faro, hecha de vidrios de colores unidos con plomo como un vitral redondo, iluminada desde atrás.",
                      MAREA + " limpia la lente con la manga.", NILO + " mira los colores con la boca abierta.", GHECO + " sobre el marco de la lente."]),
        ],
    },
    {
        "titulo": "R05-N07 · Jefe final: el Dragón del Faro",
        "misiones": [
            m(id="R05-N07-P1", titulo="Las reservas que se pisan",
              lugar=TORMENTA, personajes="Nilo, Gheco",
              criatura="dragon",
              carta="Reglas del dominio | la regla vive en una clase, no en la página · dos reservas no se pisan si una termina antes de que empiece la otra · se prueba sin base",
              recompensa="xp 15, oro 15",
              escena="""
                  La noche en que Nilo termina su último sistema, el mar se agita como la noche en que llegó. De entre las olas se levanta el **Dragón del Faro**, hecho de todo lo que puede salir mal. Su primer ataque: dos reservas de amarre para el mismo día.
              """,
              sugiere="Dos reservas se pisan si `inicioA < finB && inicioB < finA`. Con fechas `DateTimeImmutable` se comparan con `<`.",
              desafio="Escribí `sePisan` y probala con los tres casos.",
              inicial='''
                  <?php
                  function sePisan(array $a, array $b): bool
                  {
                      return false;
                  }

                  $r1 = [new DateTimeImmutable('2026-11-01'), new DateTimeImmutable('2026-11-04')];
                  $r2 = [new DateTimeImmutable('2026-11-03'), new DateTimeImmutable('2026-11-05')];
                  $r3 = [new DateTimeImmutable('2026-11-04'), new DateTimeImmutable('2026-11-06')];
                  echo "1 y 2: " . (sePisan($r1, $r2) ? 'se pisan' : 'libres') . "\\n";
                  echo "1 y 3: " . (sePisan($r1, $r3) ? 'se pisan' : 'libres') . "\\n";
              ''',
              solucion='''
                  <?php
                  function sePisan(array $a, array $b): bool
                  {
                      return $a[0] < $b[1] && $b[0] < $a[1];
                  }

                  $r1 = [new DateTimeImmutable('2026-11-01'), new DateTimeImmutable('2026-11-04')];
                  $r2 = [new DateTimeImmutable('2026-11-03'), new DateTimeImmutable('2026-11-05')];
                  $r3 = [new DateTimeImmutable('2026-11-04'), new DateTimeImmutable('2026-11-06')];
                  echo "1 y 2: " . (sePisan($r1, $r2) ? 'se pisan' : 'libres') . "\\n";
                  echo "1 y 3: " . (sePisan($r1, $r3) ? 'se pisan' : 'libres') . "\\n";
              ''',
              al_superar="Una reserva sale el 4 y la otra entra el 4: no se pisan. Las otras dos sí, y se rechaza la segunda. El Dragón ruge: perdió una ola.",
              imagen=["Un faro de noche en medio de una tormenta, con un dragón enorme enroscado y relámpagos violetas.",
                      DRAGON + " ruge con la boca abierta.", NILO + " en la cúpula, sosteniendo dos papeles de reserva.", GHECO + " sobre la baranda."]),
            m(id="R05-N07-P2", titulo="La API y la web, juntas",
              lugar=TORMENTA, personajes="Nilo, Marea, Gheco",
              criatura="dragon",
              carta="Una regla, dos caras | el mismo servicio atiende a la web (HTML) y a la API (JSON) · la regla no se repite · cada cara solo cambia la forma de contestar",
              recompensa="xp 15, oro 15",
              escena="""
                  El Dragón ataca por dos lados: por la web, con personas que reservan, y por la API, con máquinas que reservan. Nilo había copiado la regla en los dos lados, y en uno se olvidó de validar.
              """,
              sugiere="Un servicio `Reservas::reservar()` con la regla. La web y la API lo llaman y solo cambian cómo muestran la respuesta.",
              desafio="Hacé que la web y la API usen el mismo servicio.",
              inicial='''
                  <?php
                  final class Reservas
                  {
                      private array $ocupados = ['2026-11-03'];

                      public function reservar(string $dia): bool
                      {
                          if (in_array($dia, $this->ocupados, true)) {
                              return false;
                          }
                          $this->ocupados[] = $dia;
                          return true;
                      }
                  }

                  function web(Reservas $r, string $dia): string
                  {
                      return "<p>Reservado el $dia</p>";
                  }

                  function api(Reservas $r, string $dia): string
                  {
                      return $r->reservar($dia) ? json_encode(['ok' => true]) : json_encode(['ok' => false]);
                  }

                  $servicio = new Reservas();
                  echo web($servicio, '2026-11-03') . "\\n";
                  echo api($servicio, '2026-11-08') . "\\n";
                  echo api($servicio, '2026-11-08') . "\\n";
              ''',
              solucion='''
                  <?php
                  final class Reservas
                  {
                      private array $ocupados = ['2026-11-03'];

                      public function reservar(string $dia): bool
                      {
                          if (in_array($dia, $this->ocupados, true)) {
                              return false;
                          }
                          $this->ocupados[] = $dia;
                          return true;
                      }
                  }

                  function web(Reservas $r, string $dia): string
                  {
                      return $r->reservar($dia) ? "<p>Reservado el $dia</p>" : "<p>El $dia ya esta ocupado</p>";
                  }

                  function api(Reservas $r, string $dia): string
                  {
                      return $r->reservar($dia) ? json_encode(['ok' => true]) : json_encode(['ok' => false, 'error' => 'ocupado']);
                  }

                  $servicio = new Reservas();
                  echo web($servicio, '2026-11-03') . "\\n";
                  echo api($servicio, '2026-11-08') . "\\n";
                  echo api($servicio, '2026-11-08') . "\\n";
              ''',
              al_superar="Las personas y las máquinas reciben la misma verdad, cada una en su idioma. Marea levanta el farol: el Dragón retrocede.",
              imagen=["Dos ventanas de la cúpula del faro: por una entran personas con papeles y por la otra palomas mecánicas con mensajes.",
                      MAREA + " ilumina las dos ventanas con el farol.", NILO + " en el medio, con el libro de guardia.", GHECO + " sobre el farol."]),
            m(id="R05-N07-P3", titulo="Encendé la lámpara",
              lugar=TORMENTA, personajes="Nilo, Elefa, Marea, Gheco",
              criatura="dragon",
              carta="Todo el Puerto | reglas probadas · datos protegidos · capas ordenadas · errores registrados · una API para las máquinas y una web para las personas",
              recompensa="xp 25, oro 30", item="Morral del Correo Mayor",
              escena="""
                  —Esta vez no hay un solo truco —dice Elefa, parada al lado de Nilo en la cúpula—. El dragón se vence con un sistema **entero**. Todo lo que aprendiste en el Puerto, junto. Encendé la lámpara.
              """,
              sugiere="El sistema arranca en orden: carga la configuración, prueba las reglas, revisa la base y, si todo da ok, prende la lámpara. Si algo falla, lo registra y no prende.",
              desafio="Completá el arranque del sistema del Faro.",
              inicial='''
                  <?php
                  function arrancar(array $config, callable $pruebas, callable $base, array &$log): string
                  {
                      return "Lampara encendida";
                  }

                  $log = [];
                  $pruebasOk = fn () => true;
                  $baseOk = fn () => true;
                  $baseCaida = fn () => throw new RuntimeException('la bodega no responde');

                  echo arrancar(['APP_ENV' => 'produccion'], $pruebasOk, $baseCaida, $log) . "\\n";
                  echo arrancar(['APP_ENV' => 'produccion'], $pruebasOk, $baseOk, $log) . "\\n";
                  echo implode("\\n", $log) . "\\n";
              ''',
              solucion='''
                  <?php
                  function arrancar(array $config, callable $pruebas, callable $base, array &$log): string
                  {
                      try {
                          if (($config['APP_ENV'] ?? '') === '') {
                              throw new RuntimeException('falta la configuracion');
                          }
                          if (!$pruebas()) {
                              throw new RuntimeException('las pruebas fallan');
                          }
                          $base();
                          $log[] = "INFO: lampara encendida";
                          return "Lampara encendida";
                      } catch (RuntimeException $e) {
                          $log[] = "ERROR: " . $e->getMessage();
                          return "Faro momentaneamente fuera de servicio";
                      }
                  }

                  $log = [];
                  $pruebasOk = fn () => true;
                  $baseOk = fn () => true;
                  $baseCaida = fn () => throw new RuntimeException('la bodega no responde');

                  echo arrancar(['APP_ENV' => 'produccion'], $pruebasOk, $baseCaida, $log) . "\\n";
                  echo arrancar(['APP_ENV' => 'produccion'], $pruebasOk, $baseOk, $log) . "\\n";
                  echo implode("\\n", $log) . "\\n";
              ''',
              al_superar="Cuando el Dragón cae, la lámpara se prende y el vitral de la lente proyecta colores sobre todo el Puerto. Elefa le da a Nilo un morral nuevo, con un compartimiento numerado para cada pedido: **el Morral del Correo Mayor**. Nada se pierde y todo se encuentra.",
              imagen=["El faro encendido de noche, con la luz saliendo en haces de cuatro colores a través de una lente de vitral, y el mar calmo.",
                      DRAGON + " cayendo al mar, deshaciéndose en olas.", NILO + " con un morral de cuero nuevo cruzado.", ELEFA + " a su lado en la cúpula.", MAREA + " sosteniendo el farol de señales en alto.", GHECO + " sobre la lámpara."]),
        ],
    },
    {
        "titulo": "R05-N08 · La Encrucijada de los Sellos",
        "misiones": [
            m(id="R05-N08-P1", titulo="Para quien llegue",
              lugar=ENCRUCIJADA, personajes="Nilo, Elefa, Gheco",
              carta="Lo que llevás | variables, decisiones, bucles, arrays, funciones · clases e interfaces · la web, la sesión, la seguridad · la base · el MVC, la API, las pruebas",
              recompensa="xp 15, oro 15", item="Mensaje para quien llegue",
              escena="""
                  En la plaza, junto a la fuente con forma de sello de lacre, Elefa le da a Nilo un sobre amarillento, sellado con un sello de vidrio de colores. Dice *para quien llegue*. —Lo guardé veinte años. Creo que ahora es tuyo. —Cuando Nilo rompe el sello, el vidrio muestra un instante un balcón con cuatro portales: una espiral, un engranaje, un vitral y un arco de fuego.
              """,
              sugiere="Recorré lo que aprendiste en cada parte del Puerto y mostralo, rama por rama, con un `foreach` sobre un array asociativo.",
              desafio="Armá el resumen del viaje, una línea por rama.",
              inicial='''
                  <?php
                  $viaje = [
                      'Muelle' => 'variables, decisiones, bucles, arrays y funciones',
                      'Astillero' => 'clases, interfaces, enums y excepciones',
                      'Oficina' => 'la web, sesiones y seguridad',
                      'Bodega' => 'SQL, PDO y transacciones',
                      'Faro' => 'MVC, API, pruebas y el hosting',
                  ];
                  echo "Ramas recorridas: 0\\n";
              ''',
              solucion='''
                  <?php
                  $viaje = [
                      'Muelle' => 'variables, decisiones, bucles, arrays y funciones',
                      'Astillero' => 'clases, interfaces, enums y excepciones',
                      'Oficina' => 'la web, sesiones y seguridad',
                      'Bodega' => 'SQL, PDO y transacciones',
                      'Faro' => 'MVC, API, pruebas y el hosting',
                  ];
                  foreach ($viaje as $rama => $aprendido) {
                      echo "$rama: $aprendido\\n";
                  }
                  echo "Ramas recorridas: " . count($viaje) . "\\n";
              ''',
              al_superar="Cinco ramas, un viaje entero. El sobre ya no está en blanco: Nilo sabe para quién era. Era para él.",
              imagen=["Una plaza de noche con una fuente con forma de sello de lacre violeta, y un sobre abierto que proyecta en el aire la imagen de un balcón con cuatro portales: una espiral, un engranaje, un vitral y un arco de fuego.",
                      ELEFA + " le entrega el sobre.", NILO + " sostiene el sobre abierto, maravillado.", GHECO + " en el borde de la fuente."]),
            m(id="R05-N08-P2", titulo="Buen día, Elefa",
              lugar=ENCRUCIJADA, personajes="Nilo, Elefa, Iara, Gheco",
              carta="Tres caminos | la Arena (un RPG por turnos) · el Bastión de Laravel · el Palomar (JavaScript con fetch) · optativos: son tuyos",
              recompensa="xp 10, oro 10",
              escena="""
                  A la mañana siguiente, Nilo baja a la plaza. Iara, Fermín, Marea y Pico lo esperan en la fuente, y Elefa, sentada en el borde con la trompa en el agua. —Buen día, Elefa —dice Nilo, sin pensarlo. Elefa sonríe.
              """,
              sugiere="Un `match` que, según el camino elegido, diga a dónde lleva. Cualquier otro camino: «todavía no se abrió».",
              desafio="Escribí el cartel de la Encrucijada.",
              inicial='''
                  <?php
                  function camino(string $eleccion): string
                  {
                      return "todavia no se abrio";
                  }

                  foreach (['arena', 'bastion', 'palomar', 'luna'] as $c) {
                      echo "$c: " . camino($c) . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function camino(string $eleccion): string
                  {
                      return match ($eleccion) {
                          'arena' => 'un RPG por turnos',
                          'bastion' => 'el framework Laravel',
                          'palomar' => 'JavaScript que habla con tu API',
                          default => 'todavia no se abrio',
                      };
                  }

                  foreach (['arena', 'bastion', 'palomar', 'luna'] as $c) {
                      echo "$c: " . camino($c) . "\\n";
                  }
              ''',
              al_superar="Tres caminos salen de la fuente. A la luna, todavía no. Gheco señala las Sendas: el viaje sigue, si Nilo quiere.",
              imagen=["Una plaza al amanecer con una fuente con forma de sello y tres caminos: uno a una arena, uno a una fortaleza de piedra clara y uno a un palomar.",
                      ELEFA + " sentada en el borde de la fuente, sonriendo.", NILO + " saluda con la mano.", IARA + " al lado, con la libreta.", GHECO + " señalando los caminos."]),
        ],
    },
]
