from genphp import m
from php_r01 import NILO, ELEFA, IARA, PICO, GHECO

TUBOS = "La sala de los tubos de bronce"
CONSULTAS = "La ventanilla de consultas"
ENVIOS = "La ventanilla de envíos"
FONDA = "La Fonda del Puerto"
TABLERO = "El tablero de avisos"
ARCHIVOS = "La sala de archivos"
REVISOR = "El revisor de paquetes"
CARTELES = "Las veinte ventanillas"
ULTIMO_PISO = "El último piso de la Oficina"
GORGONA = "la Gorgona de los Formularios (mujer-serpiente de túnica violeta cerrada y cola gris, con el pelo hecho de cintas de papel y serpientes de pergamino, ojos violetas, una pluma enorme como lanza)"
SIMULA = "Acá no hay servidor: el pedido se simula con un array, igual al que PHP arma solo cuando llega uno de verdad."

NODOS = [
    {
        "titulo": "R03-N01 · Cómo funciona la web",
        "misiones": [
            m(id="R03-N01-P1", titulo="Cada cilindro llega solo",
              lugar=TUBOS, personajes="Nilo, Gheco",
              carta="La web | llega un pedido (método + dirección) · PHP arma la respuesta · casi siempre HTML · cada pedido es nuevo, sin memoria",
              recompensa="xp 10, oro 10",
              escena="""
                  En la Oficina de Correos, cientos de tubos de bronce bajan del techo. De cada uno cae un cilindro con un pedido: *«mandame la lista de barcos»*. Cada cilindro llega solo, sin saber nada del anterior. —¡Son como yo! —dice Nilo, emocionado—. No se acuerdan de nada.
              """,
              sugiere="Una página PHP es texto que el servidor manda al navegador. Con `foreach` se arma una lista HTML: un `<li>` por barco. " + SIMULA,
              desafio="Armá la lista HTML de barcos que pide el cilindro.",
              inicial='''
                  <?php
                  $barcos = ['Gaviota', 'Albatros', 'Tortuga'];
                  echo "<ul>\\n";
                  echo "</ul>\\n";
              ''',
              solucion='''
                  <?php
                  $barcos = ['Gaviota', 'Albatros', 'Tortuga'];
                  echo "<ul>\\n";
                  foreach ($barcos as $b) {
                      echo "  <li>$b</li>\\n";
                  }
                  echo "</ul>\\n";
              ''',
              al_superar="El cilindro vuelve por el tubo con la lista. En algún lugar del mundo, un navegador muestra tres barcos.",
              imagen=["Una sala alta con cientos de tubos de bronce que bajan del techo y cilindros de mensajes cayendo en canastos.",
                      NILO + " atrapa un cilindro en el aire.", GHECO + " sobre un tubo."]),
            m(id="R03-N01-P2", titulo="La tabla de horarios",
              lugar=TUBOS, personajes="Nilo, Iara, Gheco",
              carta="Tablas HTML | <table> · <tr> por fila · <th> encabezado · <td> dato · se arma con un foreach sobre un array de arrays",
              recompensa="xp 15, oro 15",
              escena="""
                  Un cilindro pide el horario del ferry. Iara tiene los datos en su libreta, ordenados en filas; Nilo tiene que convertirlos en una tabla HTML.
              """,
              sugiere="Un `<tr>` por cada viaje, con un `<td>` por dato. La fila de encabezados va con `<th>`.",
              desafio="Completá las filas de la tabla con los viajes.",
              inicial='''
                  <?php
                  $viajes = [
                      ['destino' => 'Forjas', 'hora' => '08:30'],
                      ['destino' => 'Valle', 'hora' => '13:00'],
                  ];
                  echo "<table>\\n";
                  echo "<tr><th>Destino</th><th>Hora</th></tr>\\n";
                  echo "</table>\\n";
              ''',
              solucion='''
                  <?php
                  $viajes = [
                      ['destino' => 'Forjas', 'hora' => '08:30'],
                      ['destino' => 'Valle', 'hora' => '13:00'],
                  ];
                  echo "<table>\\n";
                  echo "<tr><th>Destino</th><th>Hora</th></tr>\\n";
                  foreach ($viajes as $v) {
                      echo "<tr><td>{$v['destino']}</td><td>{$v['hora']}</td></tr>\\n";
                  }
                  echo "</table>\\n";
              ''',
              al_superar="El horario sale por el tubo en forma de tabla. Iara compara con su libreta: coincide.",
              imagen=["Un tablero de horarios de madera con dibujitos de barcos y relojes, sin letras ni números.",
                      IARA + " le dicta desde la libreta.", NILO + " arma el tablero.", GHECO + " sobre un reloj dibujado."]),
            m(id="R03-N01-P3", titulo="No encontrado",
              lugar=TUBOS, personajes="Nilo, Gheco",
              criatura="esqueleto",
              carta="Códigos de estado | 200 bien · 404 no está · 302 redirige · 500 falló el servidor · se elige según lo que pasó",
              recompensa="xp 15, oro 15",
              escena="""
                  Un cilindro pide el barco *Fantasma*, que no existe. La oficina de Nilo contesta igual con «200: todo bien» y una página vacía. Un **esqueleto** se asoma del tubo: un nombre sin cuerpo.
              """,
              sugiere="La respuesta lleva un código: 200 si se encontró, 404 si no. Una función que, según si el barco existe, devuelve el código y el texto.",
              desafio="Devolvé 404 cuando el barco no existe.",
              inicial='''
                  <?php
                  function responder(string $barco, array $barcos): string
                  {
                      return "200 OK: $barco";
                  }

                  $barcos = ['Gaviota', 'Albatros'];
                  echo responder('Gaviota', $barcos) . "\\n";
                  echo responder('Fantasma', $barcos) . "\\n";
              ''',
              solucion='''
                  <?php
                  function responder(string $barco, array $barcos): string
                  {
                      if (!in_array($barco, $barcos, true)) {
                          return "404 No encontrado: $barco";
                      }
                      return "200 OK: $barco";
                  }

                  $barcos = ['Gaviota', 'Albatros'];
                  echo responder('Gaviota', $barcos) . "\\n";
                  echo responder('Fantasma', $barcos) . "\\n";
              ''',
              al_superar="El cilindro del Fantasma vuelve con un 404 honesto. El esqueleto se mete otra vez en el tubo.",
              imagen=["Un tubo de bronce del que asoma un esqueleto chiquito con un cilindro vacío en la mano.",
                      NILO + " le devuelve el cilindro con un sello rojo.", GHECO + " sobre el tubo."]),
        ],
    },
    {
        "titulo": "R03-N02 · Formularios con GET",
        "misiones": [
            m(id="R03-N02-P1", titulo="Un barco a la luna",
              lugar=CONSULTAS, personajes="Nilo, Gheco",
              carta="$_GET | ?destino=Forjas llega como $_GET['destino'] · siempre texto · puede faltar o venir vacío · se filtra con lo que llega",
              recompensa="xp 10, oro 10",
              escena="""
                  En la ventanilla de consultas, el viajero anota el destino que busca y Nilo le devuelve los barcos que coinciden. Un chico escribe en el destino: «la luna». Nilo le busca un barco a la luna durante media hora.
              """,
              sugiere="Leé el destino con `$_GET['destino'] ?? ''`. Si no hay ninguno que coincida, se dice. " + SIMULA,
              desafio="Filtrá los barcos según el destino que llega en la dirección.",
              inicial='''
                  <?php
                  $_GET = ['destino' => 'la luna'];
                  $barcos = ['Gaviota' => 'Forjas', 'Albatros' => 'Valle', 'Tortuga' => 'Forjas'];

                  foreach ($barcos as $nombre => $destino) {
                      echo "$nombre va a $destino\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $_GET = ['destino' => 'la luna'];
                  $barcos = ['Gaviota' => 'Forjas', 'Albatros' => 'Valle', 'Tortuga' => 'Forjas'];

                  $pedido = trim($_GET['destino'] ?? '');
                  $encontrados = 0;
                  foreach ($barcos as $nombre => $destino) {
                      if ($pedido === '' || $destino === $pedido) {
                          echo "$nombre va a $destino\\n";
                          $encontrados++;
                      }
                  }
                  if ($encontrados === 0) {
                      echo "No hay barcos a $pedido\\n";
                  }
              ''',
              al_superar="No hay barcos a la luna, y ahora el programa lo dice en un segundo. El chico se va, decepcionado, a probar con «Forjas».",
              imagen=["Una ventanilla de consultas con una pizarra de casilleros y, en el cielo de la ventana, una luna enorme.",
                      "Un chico señala la luna.", NILO + " revisa una lista de barcos, perplejo.", GHECO + " sobre la pizarra."]),
            m(id="R03-N02-P2", titulo="El enlace con parámetros",
              lugar=CONSULTAS, personajes="Nilo, Gheco",
              carta="http_build_query | ['destino' => 'Valle de la Serpiente', 'pagina' => 2] → destino=Valle+de+la+Serpiente&pagina=2 · codifica los espacios y los signos",
              recompensa="xp 10, oro 10",
              escena="""
                  Nilo arma a mano los enlaces de la próxima página: `?destino=Valle de la Serpiente&pagina=2`. El espacio rompe el enlace y el navegador se pierde a mitad de camino.
              """,
              sugiere="`http_build_query($datos)` arma la parte de la dirección con todo bien codificado.",
              desafio="Armá el enlace con `http_build_query`.",
              inicial='''
                  <?php
                  $destino = 'Valle de la Serpiente';
                  $pagina = 2;
                  echo "/barcos?destino=$destino&pagina=$pagina\\n";
              ''',
              solucion='''
                  <?php
                  $destino = 'Valle de la Serpiente';
                  $pagina = 2;
                  echo "/barcos?" . http_build_query(['destino' => $destino, 'pagina' => $pagina]) . "\\n";
              ''',
              al_superar="El enlace llega entero a destino. El navegador ya no se pierde a mitad de camino.",
              imagen=["Un cilindro de mensaje viajando por un tubo de bronce con un papel enrollado prolijo adentro.",
                      NILO + " lo empuja dentro del tubo.", GHECO + " siguiéndolo por afuera."]),
            m(id="R03-N02-P3", titulo="De a tres por página",
              lugar=CONSULTAS, personajes="Nilo, Iara, Gheco",
              criatura="orco",
              carta="Paginar | por página fija · desde = (pagina - 1) * por · array_slice($lista, desde, por) · validar que la página exista",
              recompensa="xp 15, oro 15",
              escena="""
                  La lista de barcos ya es tan larga que el tubo se atasca. Iara propone mandarla de a tres. Alguien pide la página 99 y un **orco** sale de donde termina la lista.
              """,
              sugiere="`array_slice($barcos, ($pagina - 1) * 3, 3)` corta la página. Si la página es menor que 1 o mayor que la última, se usa la última (o la primera).",
              desafio="Mostrá la página pedida, cuidando que exista.",
              inicial='''
                  <?php
                  $_GET = ['pagina' => '99'];
                  $barcos = ['Gaviota', 'Albatros', 'Tortuga', 'Triton', 'Colonia', 'Condor', 'Delfin'];
                  $pagina = (int) $_GET['pagina'];
                  foreach (array_slice($barcos, ($pagina - 1) * 3, 3) as $b) {
                      echo "$b\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $_GET = ['pagina' => '99'];
                  $barcos = ['Gaviota', 'Albatros', 'Tortuga', 'Triton', 'Colonia', 'Condor', 'Delfin'];
                  $porPagina = 3;
                  $ultima = (int) ceil(count($barcos) / $porPagina);
                  $pagina = max(1, min($ultima, (int) ($_GET['pagina'] ?? 1)));
                  echo "Pagina $pagina de $ultima\\n";
                  foreach (array_slice($barcos, ($pagina - 1) * $porPagina, $porPagina) as $b) {
                      echo "$b\\n";
                  }
              ''',
              al_superar="La página 99 no existe, así que va la última. El orco no encuentra dónde esconderse.",
              imagen=["Tres pilas de papeles prolijas sobre un mostrador, cada una atada con una cinta de distinto color.",
                      IARA + " ata una pila.", NILO + " lleva otra al tubo.", "Un orco asoma detrás del mostrador, sin nada que agarrar.", GHECO + " sobre una pila."]),
        ],
    },
    {
        "titulo": "R03-N03 · Formularios con POST y validación",
        "misiones": [
            m(id="R03-N03-P1", titulo="Peso: bastante",
              lugar=ENVIOS, personajes="Nilo, Iara, Gheco",
              carta="Validar | un array $errores · un error por campo · si está vacío, se procesa · si no, se muestran los errores",
              recompensa="xp 10, oro 10",
              escena="""
                  En la ventanilla de envíos, los formularios llegan con de todo: el peso dice «bastante», el destino está en blanco. Nilo los mandaba igual. Iara le enseña a devolverlos con cada error marcado.
              """,
              sugiere="Revisá cada campo y guardá el error en `$errores['peso']`, `$errores['destino']`… Al final, si `$errores` está vacío se acepta; si no, se muestran. " + SIMULA,
              desafio="Validá el peso (un número positivo) y el destino (no vacío).",
              inicial='''
                  <?php
                  $_POST = ['peso' => 'bastante', 'destino' => ''];
                  echo "Envio aceptado: {$_POST['peso']} kg a {$_POST['destino']}\\n";
              ''',
              solucion='''
                  <?php
                  $_POST = ['peso' => 'bastante', 'destino' => ''];
                  $errores = [];
                  $peso = trim($_POST['peso'] ?? '');
                  $destino = trim($_POST['destino'] ?? '');

                  if (!is_numeric($peso) || $peso <= 0) {
                      $errores['peso'] = 'El peso tiene que ser un numero mayor que 0.';
                  }
                  if ($destino === '') {
                      $errores['destino'] = 'Falta el destino.';
                  }

                  if ($errores === []) {
                      echo "Envio aceptado: $peso kg a $destino\\n";
                  } else {
                      foreach ($errores as $campo => $error) {
                          echo "$campo: $error\\n";
                      }
                  }
              ''',
              al_superar="El formulario vuelve con sus dos errores. El cliente escribe «8» y «Forjas», y el paquete sale bien.",
              imagen=["Un formulario de papel con dos casilleros marcados con círculos rojos, sin letras, sobre el mostrador de envíos.",
                      IARA + " marca los círculos con el lápiz.", NILO + " sostiene el paquete.", GHECO + " sobre el formulario."]),
            m(id="R03-N03-P2", titulo="Sin borrar lo que estaba bien",
              lugar=ENVIOS, personajes="Nilo, Iara, Gheco",
              carta="Volver a mostrar | value=\"<?= htmlspecialchars($valor) ?>\" · lo que el cliente ya escribió vuelve cargado · nadie quiere escribir todo de nuevo",
              recompensa="xp 15, oro 15",
              escena="""
                  El formulario volvía con los errores, pero vacío: el cliente tenía que escribir todo de nuevo, también lo que estaba bien. Iara se lo devuelve a Nilo con una nota: *«no borres lo bueno»*.
              """,
              sugiere="El campo vuelve con su valor: `value=\"…\"`. Con `htmlspecialchars` se escapa por si trae comillas.",
              desafio="Mostrá el campo del nombre con lo que ya había escrito el cliente.",
              inicial='''
                  <?php
                  $_POST = ['nombre' => 'Rosa "la del muelle"', 'peso' => ''];
                  echo '<input name="nombre" value="">' . "\\n";
                  echo "Falta el peso.\\n";
              ''',
              solucion='''
                  <?php
                  $_POST = ['nombre' => 'Rosa "la del muelle"', 'peso' => ''];
                  $nombre = $_POST['nombre'] ?? '';
                  echo '<input name="nombre" value="' . htmlspecialchars($nombre) . '">' . "\\n";
                  echo "Falta el peso.\\n";
              ''',
              al_superar="Rosa solo completa el peso. Le agradece a Nilo con una sonrisa; Nilo se la pasa a Iara, que es quien la merece.",
              imagen=["Un formulario de papel con un casillero ya escrito (rayitas de tinta) y otro vacío marcado, sobre el mostrador.",
                      IARA + " escribe una nota corta.", NILO + " le entrega el formulario a una señora sonriente.", GHECO + " sobre el tintero."]),
            m(id="R03-N03-P3", titulo="GET para ver, POST para mandar",
              lugar=ENVIOS, personajes="Nilo, Gheco",
              carta="Método | $_SERVER['REQUEST_METHOD'] dice GET o POST · GET: mostrar el formulario · POST: procesarlo",
              recompensa="xp 10, oro 10",
              escena="""
                  La misma página muestra el formulario y lo procesa. El programa de Nilo intentaba procesar también cuando alguien solo quería ver el formulario, y se quejaba de campos vacíos que nadie había mandado todavía.
              """,
              sugiere="Según el método: con `GET` se muestra el formulario; con `POST` se procesa. Probalo con los dos pedidos.",
              desafio="Completá la función para que haga una cosa u otra según el método.",
              inicial='''
                  <?php
                  function atender(string $metodo, array $post): string
                  {
                      return ($post['destino'] ?? '') === '' ? "Error: falta el destino" : "Enviado a {$post['destino']}";
                  }

                  echo atender('GET', []) . "\\n";
                  echo atender('POST', ['destino' => 'Valle']) . "\\n";
              ''',
              solucion='''
                  <?php
                  function atender(string $metodo, array $post): string
                  {
                      if ($metodo === 'GET') {
                          return "Formulario vacio para completar";
                      }
                      return ($post['destino'] ?? '') === '' ? "Error: falta el destino" : "Enviado a {$post['destino']}";
                  }

                  echo atender('GET', []) . "\\n";
                  echo atender('POST', ['destino' => 'Valle']) . "\\n";
              ''',
              al_superar="Quien viene a mirar, mira. Quien viene a mandar, manda. La ventanilla deja de quejarse sola.",
              imagen=["Una ventanilla con dos bandejas de madera, una vacía para retirar formularios y otra con formularios completos.",
                      NILO + " separa los papeles en las dos bandejas.", GHECO + " sobre una bandeja."]),
            m(id="R03-N03-P4", titulo="Uno de la lista",
              lugar=ENVIOS, personajes="Nilo, Gheco",
              criatura="goblin",
              carta="select y radio | el valor tiene que estar en la lista permitida · in_array($x, $permitidos, true) · el navegador no garantiza nada",
              recompensa="xp 15, oro 15",
              escena="""
                  El formulario de envíos tiene un `select` con tres destinos. Un **goblin** mandó el formulario a mano, sin navegador, con el destino «la cueva del goblin». El programa lo aceptó.
              """,
              sugiere="El servidor revisa que el valor esté en la lista: `in_array($destino, $permitidos, true)`. Lo que no está, se rechaza.",
              desafio="Rechazá los destinos que no están en la lista.",
              inicial='''
                  <?php
                  $permitidos = ['Forjas', 'Valle', 'Ciudadela'];
                  foreach (['Valle', 'la cueva del goblin'] as $destino) {
                      echo "Enviado a $destino\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $permitidos = ['Forjas', 'Valle', 'Ciudadela'];
                  foreach (['Valle', 'la cueva del goblin'] as $destino) {
                      if (in_array($destino, $permitidos, true)) {
                          echo "Enviado a $destino\\n";
                      } else {
                          echo "Destino no permitido: $destino\\n";
                      }
                  }
              ''',
              al_superar="El paquete a la cueva del goblin se queda en el Puerto. El goblin, sin paquete, patea una piedra.",
              imagen=["Un formulario arrugado sobre el mostrador junto a un mapa del puerto con tres destinos marcados con banderines.",
                      "Un goblin flaco del otro lado del mostrador, con cara de inocente.", NILO + " rechaza el formulario con un sello rojo.", GHECO + " sobre el mapa."]),
        ],
    },
    {
        "titulo": "R03-N04 · Sesiones y cookies",
        "misiones": [
            m(id="R03-N04-P1", titulo="El mozo sin memoria",
              lugar=FONDA, personajes="Nilo, Gheco",
              carta="Sin memoria | cada pedido HTTP llega solo · lo que no se guarda en algún lado, se pierde · el servidor guarda una libreta por visitante: la sesión",
              recompensa="xp 10, oro 10",
              escena="""
                  Elefa manda a Nilo a atender la fonda. Cada vez que alguien se acerca, Nilo le pregunta de nuevo qué quería. *«Ya te lo dije hace cinco minutos»*, protesta una clienta. Nilo no tiene memoria: como HTTP.
              """,
              sugiere="Acá la sesión se simula con un array `$libreta` que dura entre un pedido y el siguiente. Guardá el pedido la primera vez y leelo la segunda.",
              desafio="Hacé que el mozo se acuerde del pedido de la clienta.",
              inicial='''
                  <?php
                  $libreta = [];

                  function atender(array &$libreta, ?string $pide): string
                  {
                      if ($pide !== null) {
                          return "Anotado: $pide";
                      }
                      return "Perdon, ¿que queria?";
                  }

                  echo atender($libreta, 'guiso de pescado') . "\\n";
                  echo atender($libreta, null) . "\\n";
              ''',
              solucion='''
                  <?php
                  $libreta = [];

                  function atender(array &$libreta, ?string $pide): string
                  {
                      if ($pide !== null) {
                          $libreta['pedido'] = $pide;
                          return "Anotado: $pide";
                      }
                      return isset($libreta['pedido']) ? "Ya sale su {$libreta['pedido']}" : "Perdon, ¿que queria?";
                  }

                  echo atender($libreta, 'guiso de pescado') . "\\n";
                  echo atender($libreta, null) . "\\n";
              ''',
              al_superar="«Ya sale su guiso de pescado.» La clienta casi aplaude. Nilo mira la libreta: no se acordaba de nada, pero estaba anotado.",
              imagen=["La ventanilla de una fonda del puerto con ollas humeantes y un pizarrón de dibujitos de comida.",
                      NILO + " con un delantal encima de la chaqueta, anotando en una libreta.", "Una clienta esperando con los brazos cruzados.", GHECO + " sobre una olla."]),
            m(id="R03-N04-P2", titulo="Una cookie para que te acuerdes",
              lugar=FONDA, personajes="Nilo, Iara, Elefa, Gheco",
              carta="Cookie y sesión | el servidor le da al visitante una ficha (la cookie con el id) · y guarda sus datos bajo ese id (la sesión) · cada pedido trae la ficha",
              recompensa="xp 15, oro 15", se_abre="«¡Buen día, Elefa!»",
              escena="""
                  Iara le da a Nilo un talonario de fichas numeradas: a cada cliente le entrega una, y en su libreta anota lo que pidió cada número. De paso, le da una galletita con su nombre estampado: *«una cookie, para que te acuerdes»*.
              """,
              sugiere="Cada cliente trae su ficha (el id). La libreta guarda los datos **por id**: `$sesiones[$ficha]['pedido']`. Así no se mezclan los clientes.",
              desafio="Guardá y leé el pedido de cada cliente según su ficha.",
              inicial='''
                  <?php
                  $sesiones = [];

                  function pedir(array &$sesiones, string $ficha, string $plato): void
                  {
                      $sesiones['pedido'] = $plato;
                  }

                  function servir(array $sesiones, string $ficha): string
                  {
                      return "Ficha $ficha: " . ($sesiones['pedido'] ?? 'sin pedido');
                  }

                  pedir($sesiones, 'A7', 'guiso');
                  pedir($sesiones, 'B2', 'empanadas');
                  echo servir($sesiones, 'A7') . "\\n";
                  echo servir($sesiones, 'B2') . "\\n";
                  echo servir($sesiones, 'C9') . "\\n";
              ''',
              solucion='''
                  <?php
                  $sesiones = [];

                  function pedir(array &$sesiones, string $ficha, string $plato): void
                  {
                      $sesiones[$ficha]['pedido'] = $plato;
                  }

                  function servir(array $sesiones, string $ficha): string
                  {
                      return "Ficha $ficha: " . ($sesiones[$ficha]['pedido'] ?? 'sin pedido');
                  }

                  pedir($sesiones, 'A7', 'guiso');
                  pedir($sesiones, 'B2', 'empanadas');
                  echo servir($sesiones, 'A7') . "\\n";
                  echo servir($sesiones, 'B2') . "\\n";
                  echo servir($sesiones, 'C9') . "\\n";
              ''',
              al_superar="A la mañana siguiente, Nilo entra a la torre y saluda: —¡Buen día, Elefa! —A la Capitana casi se le cae el bastón.",
              imagen=["La ventanilla de la fonda con un talonario de fichas numeradas con puntitos de colores y una galletita redonda con un sello estampado.",
                      IARA + " le da la galletita a Nilo.", NILO + " la mira como si fuera un tesoro.", ELEFA + " al fondo, en la puerta, sorprendida.", GHECO + " sobre el talonario."]),
            m(id="R03-N04-P3", titulo="El carrito que dura",
              lugar=FONDA, personajes="Nilo, Gheco",
              carta="Carrito | $_SESSION['carrito'][$producto] = ($_SESSION['carrito'][$producto] ?? 0) + $cantidad · dura entre páginas",
              recompensa="xp 15, oro 15",
              escena="""
                  En la fonda se puede ir sumando platos a la cuenta mientras se come. La cuenta de Nilo se borraba cada vez que el cliente pedía algo nuevo: solo quedaba el último plato.
              """,
              sugiere="Sumá al carrito sin pisar lo que había: `$carrito[$plato] = ($carrito[$plato] ?? 0) + $cantidad;`.",
              desafio="Sumá los platos a la cuenta y mostrala.",
              inicial='''
                  <?php
                  $sesion = ['carrito' => []];
                  $precios = ['guiso' => 12, 'pan' => 2, 'te' => 3];

                  foreach ([['guiso', 1], ['pan', 2], ['guiso', 1], ['te', 1]] as [$plato, $cantidad]) {
                      $sesion['carrito'] = [$plato => $cantidad];
                  }

                  $total = 0;
                  foreach ($sesion['carrito'] as $plato => $cantidad) {
                      echo "$plato x$cantidad\\n";
                      $total += $precios[$plato] * $cantidad;
                  }
                  echo "Total: $total sellos\\n";
              ''',
              solucion='''
                  <?php
                  $sesion = ['carrito' => []];
                  $precios = ['guiso' => 12, 'pan' => 2, 'te' => 3];

                  foreach ([['guiso', 1], ['pan', 2], ['guiso', 1], ['te', 1]] as [$plato, $cantidad]) {
                      $sesion['carrito'][$plato] = ($sesion['carrito'][$plato] ?? 0) + $cantidad;
                  }

                  $total = 0;
                  foreach ($sesion['carrito'] as $plato => $cantidad) {
                      echo "$plato x$cantidad\\n";
                      $total += $precios[$plato] * $cantidad;
                  }
                  echo "Total: $total sellos\\n";
              ''',
              al_superar="Dos guisos, dos panes y un té: 31 sellos. El cliente paga, satisfecho y lleno.",
              imagen=["Una mesa de la fonda con dos platos de guiso, pan y una taza de té, y una cuenta de papel al lado.",
                      NILO + " sirve el té.", GHECO + " sobre la cuenta."]),
            m(id="R03-N04-P4", titulo="El mensaje de una sola vez",
              lugar=FONDA, personajes="Nilo, Gheco",
              carta="Flash | se guarda en la sesión al redirigir · se muestra una vez · se borra al leerlo",
              recompensa="xp 10, oro 10",
              escena="""
                  Después de pagar, el cliente ve «¡Gracias por su visita!». Pero el cartel no se borra: lo ve el siguiente cliente, y el siguiente, y uno que todavía no comió nada.
              """,
              sugiere="Leer el mensaje y **borrarlo** en el mismo paso: guardalo en una variable y hacé `unset($sesion['flash'])`.",
              desafio="Hacé que el mensaje se muestre una sola vez.",
              inicial='''
                  <?php
                  $sesion = ['flash' => '¡Gracias por su visita!'];

                  function pagina(array &$sesion): string
                  {
                      return $sesion['flash'] ?? '(sin mensajes)';
                  }

                  echo pagina($sesion) . "\\n";
                  echo pagina($sesion) . "\\n";
              ''',
              solucion='''
                  <?php
                  $sesion = ['flash' => '¡Gracias por su visita!'];

                  function pagina(array &$sesion): string
                  {
                      $mensaje = $sesion['flash'] ?? '(sin mensajes)';
                      unset($sesion['flash']);
                      return $mensaje;
                  }

                  echo pagina($sesion) . "\\n";
                  echo pagina($sesion) . "\\n";
              ''',
              al_superar="El cartel aparece una vez y se va. El cliente que no comió nada ya no se siente agradecido por error.",
              imagen=["Un cartel de madera con un corazón pintado, colgado en la puerta de la fonda, que se desvanece en humo.",
                      NILO + " saluda a un cliente que se va.", GHECO + " sobre el marco de la puerta."]),
        ],
    },
    {
        "titulo": "R03-N05 · Seguridad: XSS, CSRF y validación del lado del servidor",
        "misiones": [
            m(id="R03-N05-P1", titulo="Envíos gratis",
              lugar=TABLERO, personajes="Nilo, Elefa, Gheco",
              criatura="troll",
              carta="XSS | todo lo que viene de afuera se escapa al mostrarlo · htmlspecialchars($x) convierte < > \" ' & en texto · nunca echo $_POST directo",
              recompensa="xp 15, oro 15",
              escena="""
                  Una mañana, el tablero de avisos amaneció diciendo *«¡Todos los envíos gratis hoy!»*. Nadie lo había escrito: alguien dejó un aviso con un truco escondido (`<script>`), y el tablero lo ejecutó en lugar de mostrarlo. Elefa cierra la puerta con llave.
              """,
              sugiere="`htmlspecialchars($aviso)` convierte los `<` y `>` en texto: el truco se ve, pero ya no se ejecuta.",
              desafio="Escapá cada aviso antes de mostrarlo en el tablero.",
              inicial='''
                  <?php
                  $avisos = ['Llega el ferry a las 8', '<script>envios("gratis")</script>'];
                  foreach ($avisos as $a) {
                      echo "<p>$a</p>\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $avisos = ['Llega el ferry a las 8', '<script>envios("gratis")</script>'];
                  foreach ($avisos as $a) {
                      echo "<p>" . htmlspecialchars($a) . "</p>\\n";
                  }
              ''',
              al_superar="El aviso tramposo queda en el tablero, pero desarmado: se lee el truco y no pasa nada. Elefa: —Todo lo que llega de afuera es sospechoso.",
              imagen=["Un tablero de avisos de corcho con papelitos clavados, uno de ellos con un dibujo de una calavera tachada.",
                      ELEFA + " cierra una puerta con una llave grande.", NILO + " clava un papel en el tablero.", "Un troll escondido detrás del tablero.", GHECO + " sobre una chinche."]),
            m(id="R03-N05-P2", titulo="El formulario robado",
              lugar=TABLERO, personajes="Nilo, Pico, Gheco",
              carta="CSRF | cada formulario lleva un token secreto guardado en la sesión · al recibirlo se compara con hash_equals · sin token, se rechaza",
              recompensa="xp 15, oro 15",
              escena="""
                  Pico entra por la ventana con un formulario robado en el pico: un pedido de «transferir 100 sellos» con la firma de la tesorera… que ella nunca mandó. El programa lo aceptó porque la firma parecía buena.
              """,
              sugiere="El token se guarda en la sesión al mostrar el formulario. Al recibirlo, `hash_equals($sesion['token'], $post['token'] ?? '')`: si no coincide, se rechaza.",
              desafio="Rechazá el pedido que no trae el token correcto.",
              inicial='''
                  <?php
                  $sesion = ['token' => bin2hex(random_bytes(16))];
                  $formularioBueno = ['monto' => 20, 'token' => $sesion['token']];
                  $formularioDePico = ['monto' => 100, 'token' => 'cualquiera'];

                  foreach ([$formularioBueno, $formularioDePico] as $post) {
                      echo "Transferidos {$post['monto']} sellos\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $sesion = ['token' => bin2hex(random_bytes(16))];
                  $formularioBueno = ['monto' => 20, 'token' => $sesion['token']];
                  $formularioDePico = ['monto' => 100, 'token' => 'cualquiera'];

                  foreach ([$formularioBueno, $formularioDePico] as $post) {
                      if (!hash_equals($sesion['token'], $post['token'] ?? '')) {
                          echo "Rechazado: el formulario no es nuestro\\n";
                          continue;
                      }
                      echo "Transferidos {$post['monto']} sellos\\n";
                  }
              ''',
              al_superar="El formulario de Pico rebota. Pico lo suelta y se va a buscar algo más fácil de robar. Nilo jura que no lo hizo a propósito.",
              imagen=["Una ventana abierta de la oficina de correos de noche, con un papel con sello cayendo hacia el piso.",
                      PICO + " suelta el papel, con cara de inocente.", NILO + " atrapa el papel.", GHECO + " sobre el marco de la ventana."]),
            m(id="R03-N05-P3", titulo="El navegador no manda",
              lugar=TABLERO, personajes="Nilo, Gheco",
              criatura="goblin",
              carta="Validar en el servidor | el maxlength, el required y el min del HTML los saltea cualquiera · el servidor revisa todo de nuevo",
              recompensa="xp 10, oro 10",
              escena="""
                  El formulario de reservas dice en el HTML que la cantidad va de 1 a 10. Un **goblin** mandó el pedido a mano, sin navegador: 500 lugares. El servidor confió en el HTML.
              """,
              sugiere="Validá en el servidor: `filter_var($cantidad, FILTER_VALIDATE_INT, ['options' => ['min_range' => 1, 'max_range' => 10]])` da `false` si no está en el rango.",
              desafio="Rechazá las cantidades fuera del rango.",
              inicial='''
                  <?php
                  foreach (['3', '500', 'cinco'] as $cantidad) {
                      echo "Reservados $cantidad lugares\\n";
                  }
              ''',
              solucion='''
                  <?php
                  foreach (['3', '500', 'cinco'] as $cantidad) {
                      $n = filter_var($cantidad, FILTER_VALIDATE_INT, ['options' => ['min_range' => 1, 'max_range' => 10]]);
                      if ($n === false) {
                          echo "Cantidad invalida: $cantidad\\n";
                      } else {
                          echo "Reservados $n lugares\\n";
                      }
                  }
              ''',
              al_superar="Los 500 lugares del goblin no se reservan. El ferry sale con lugar para todos.",
              imagen=["Un ferry en el muelle con una fila de pasajeros normales y un goblin que intenta colar una carretilla llena de boletos.",
                      NILO + " le cierra el paso con el brazo.", GHECO + " sobre la baranda del ferry."]),
            m(id="R03-N05-P4", titulo="La redirección abierta",
              lugar=TABLERO, personajes="Nilo, Elefa, Gheco",
              carta="Redirecciones | ?volver=… no se usa tal cual · solo direcciones del mismo sitio: empiezan con / y no con // · si no, al inicio",
              recompensa="xp 15, oro 15",
              escena="""
                  Después del login, la página vuelve a donde dice `?volver=`. Alguien armó un enlace con `?volver=//puerto-falso.ar` y mandó a los clientes a un sitio igualito al de Elefa, pero falso.
              """,
              sugiere="Aceptá solo direcciones que empiezan con `/` y **no** con `//`. Todo lo demás vuelve a `/inicio`.",
              desafio="Escribí la función que decide a dónde volver.",
              inicial='''
                  <?php
                  function volverA(string $pedido): string
                  {
                      return $pedido;
                  }

                  foreach (['/mis-envios', '//puerto-falso.ar', 'https://otro.ar'] as $p) {
                      echo volverA($p) . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function volverA(string $pedido): string
                  {
                      if (str_starts_with($pedido, '/') && !str_starts_with($pedido, '//')) {
                          return $pedido;
                      }
                      return '/inicio';
                  }

                  foreach (['/mis-envios', '//puerto-falso.ar', 'https://otro.ar'] as $p) {
                      echo volverA($p) . "\\n";
                  }
              ''',
              al_superar="Los clientes vuelven a donde tienen que volver. El puerto falso se queda sin visitas. Elefa sella la puerta otra vez.",
              imagen=["Dos puertas iguales una al lado de la otra en un pasillo de la torre, una con un sello de lacre violeta y otra sin sello.",
                      ELEFA + " señala la puerta con el sello.", NILO + " con la mano en el picaporte de la otra.", GHECO + " sobre el sello."]),
        ],
    },
    {
        "titulo": "R03-N06 · Login con contraseñas",
        "misiones": [
            m(id="R03-N06-P1", titulo="La huella de la contraseña",
              lugar=ARCHIVOS, personajes="Nilo, Iara, Pico, Gheco",
              carta="password_hash | se guarda la huella, nunca la contraseña · password_verify($escrita, $huella) dice si coincide · cada huella es distinta aunque la clave sea igual",
              recompensa="xp 15, oro 15",
              escena="""
                  Antes, el guardia de la sala de archivos tenía las contraseñas escritas en un papel. Pico se robó el papel, y con él, todas las contraseñas. Nilo anota la suya nueva en la palma de la mano. Iara se la borra con saliva.
              """,
              sugiere="Guardá `password_hash($clave, PASSWORD_DEFAULT)` y, para entrar, compará con `password_verify($escrita, $huella)`. La huella no se puede volver a convertir en la clave.",
              desafio="Guardá la huella en lugar de la contraseña y comprobá los dos intentos.",
              inicial='''
                  <?php
                  $guardada = 'faro2026';

                  foreach (['faro2026', 'gaviota'] as $intento) {
                      echo $intento === $guardada ? "Pasa\\n" : "No pasa\\n";
                  }
                  echo "En el papel dice: $guardada\\n";
              ''',
              solucion='''
                  <?php
                  $huella = password_hash('faro2026', PASSWORD_DEFAULT);

                  foreach (['faro2026', 'gaviota'] as $intento) {
                      echo password_verify($intento, $huella) ? "Pasa\\n" : "No pasa\\n";
                  }
                  echo "En el papel dice: " . (str_starts_with($huella, '$2y$') ? "una huella" : "la clave") . "\\n";
              ''',
              al_superar="Aunque Pico se robe el papel nuevo, no le sirve: tiene huellas, no contraseñas. Nilo se mira la palma limpia, un poco triste.",
              imagen=["Una puerta de una sala de archivos con un guardia y una lista en la pared llena de sellos de lacre deformados, sin letras.",
                      PICO + " mira la lista, decepcionado.", IARA + " le limpia la mano a Nilo con un pañuelo.", NILO + " con la palma estirada.", GHECO + " sobre la lista."]),
            m(id="R03-N06-P2", titulo="Solo para los de adentro",
              lugar=ARCHIVOS, personajes="Nilo, Gheco",
              carta="Proteger páginas | al principio: si no hay usuario en la sesión, a /login y exit · se revisa en CADA página privada",
              recompensa="xp 10, oro 10",
              escena="""
                  La sala de archivos tiene tres puertas, y Nilo puso guardia solo en la principal. Por la de atrás entra cualquiera.
              """,
              sugiere="Una función `exigirLogin(array $sesion): ?string` que devuelve la redirección si no hay usuario. Se llama al principio de **cada** página privada.",
              desafio="Escribí la guardia y ponela en las tres páginas.",
              inicial='''
                  <?php
                  function pagina(string $nombre, array $sesion): string
                  {
                      return "Mostrando $nombre";
                  }

                  $visitante = [];
                  foreach (['archivos', 'balances', 'claves'] as $p) {
                      echo pagina($p, $visitante) . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function exigirLogin(array $sesion): ?string
                  {
                      return isset($sesion['usuario']) ? null : 'Redirige a /login';
                  }

                  function pagina(string $nombre, array $sesion): string
                  {
                      return exigirLogin($sesion) ?? "Mostrando $nombre";
                  }

                  $visitante = [];
                  $iara = ['usuario' => 'iara'];
                  foreach (['archivos', 'balances', 'claves'] as $p) {
                      echo pagina($p, $visitante) . "\\n";
                  }
                  echo pagina('archivos', $iara) . "\\n";
              ''',
              al_superar="Las tres puertas tienen guardia. Iara entra por la de atrás y el guardia le pide la ficha igual. Iara aprueba.",
              imagen=["Un pasillo con tres puertas de la sala de archivos, cada una con un guardia chiquito con farol.",
                      NILO + " pone el último guardia en la puerta de atrás.", GHECO + " sobre un farol."]),
            m(id="R03-N06-P3", titulo="Tres intentos",
              lugar=ARCHIVOS, personajes="Nilo, Gheco",
              criatura="goblin",
              carta="Limitar intentos | contar los fallos por usuario · después de 3, bloquear un rato · avisar sin decir si el usuario existe",
              recompensa="xp 15, oro 15",
              escena="""
                  Un **goblin** prueba contraseñas en la puerta de los archivos: una, otra, otra, cien. Nadie lo frena.
              """,
              sugiere="Contá los fallos en `$intentos[$usuario]`. Si ya son 3, se bloquea sin siquiera probar la clave.",
              desafio="Bloqueá al usuario después de 3 intentos fallidos.",
              inicial='''
                  <?php
                  $huella = password_hash('faro2026', PASSWORD_DEFAULT);
                  $intentos = [];

                  foreach (['a', 'b', 'c', 'd', 'faro2026'] as $clave) {
                      echo password_verify($clave, $huella) ? "Adentro\\n" : "Clave incorrecta\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $huella = password_hash('faro2026', PASSWORD_DEFAULT);
                  $intentos = [];
                  $usuario = 'fermin';

                  foreach (['a', 'b', 'c', 'd', 'faro2026'] as $clave) {
                      if (($intentos[$usuario] ?? 0) >= 3) {
                          echo "Bloqueado: proba mas tarde\\n";
                          continue;
                      }
                      if (password_verify($clave, $huella)) {
                          echo "Adentro\\n";
                      } else {
                          $intentos[$usuario] = ($intentos[$usuario] ?? 0) + 1;
                          echo "Clave incorrecta\\n";
                      }
                  }
              ''',
              al_superar="Al cuarto intento, la puerta deja de escuchar. El goblin se sienta en el escalón a esperar. Va a esperar un buen rato.",
              imagen=["La puerta de la sala de archivos con un candado de bronce enorme y tres marcas rayadas al lado.",
                      "Un goblin sentado en el escalón, aburrido.", NILO + " cierra el candado.", GHECO + " sobre el candado."]),
            m(id="R03-N06-P4", titulo="Una clave como la gente",
              lugar=ARCHIVOS, personajes="Nilo, Iara, Gheco",
              carta="Registrar | la clave: largo mínimo, no igual al usuario · se juntan los problemas y se muestran todos juntos",
              recompensa="xp 10, oro 10",
              escena="""
                  Para registrarse en la Oficina, Nilo propone de contraseña «nilo». Iara le dice que una clave igual al nombre la adivina hasta Pico.
              """,
              sugiere="Juntá los problemas en una lista: menos de 8 caracteres, igual al usuario. Si la lista está vacía, la clave sirve.",
              desafio="Revisá las dos claves y mostrá todos los problemas de cada una.",
              inicial='''
                  <?php
                  function problemas(string $usuario, string $clave): array
                  {
                      return [];
                  }

                  foreach (['nilo' => 'nilo', 'iara' => 'cuaderno-azul-12'] as $usuario => $clave) {
                      $p = problemas($usuario, $clave);
                      echo "$usuario: " . ($p === [] ? 'clave aceptada' : implode('; ', $p)) . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function problemas(string $usuario, string $clave): array
                  {
                      $p = [];
                      if (mb_strlen($clave) < 8) {
                          $p[] = 'muy corta';
                      }
                      if (strtolower($clave) === strtolower($usuario)) {
                          $p[] = 'igual al usuario';
                      }
                      return $p;
                  }

                  foreach (['nilo' => 'nilo', 'iara' => 'cuaderno-azul-12'] as $usuario => $clave) {
                      $p = problemas($usuario, $clave);
                      echo "$usuario: " . ($p === [] ? 'clave aceptada' : implode('; ', $p)) . "\\n";
                  }
              ''',
              al_superar="Nilo elige una clave nueva, larga, que no se parece a su nombre. Al rato se la olvida. Por suerte, eso tiene arreglo.",
              imagen=["Un formulario de registro sobre un mostrador, con dos casilleros, uno con una cruz roja y otro con un tilde verde, sin letras.",
                      IARA + " señala la cruz.", NILO + " se rasca la gorra.", GHECO + " sobre el tilde."]),
        ],
    },
    {
        "titulo": "R03-N07 · Subir archivos y guardar en JSON",
        "misiones": [
            m(id="R03-N07-P1", titulo="El retrato que era una trampa",
              lugar=REVISOR, personajes="Nilo, Gheco",
              criatura="troll",
              carta="Tipo real | el nombre y lo que dice el navegador se pueden falsificar · se mira el contenido: un PNG empieza con \\x89PNG, un JPEG con \\xFF\\xD8 · y el tamaño",
              recompensa="xp 15, oro 15",
              escena="""
                  Un día alguien mandó un «retrato.png» que en realidad tenía código adentro, y casi incendia el archivo. Desde entonces, un revisor mira **qué hay de verdad** dentro de cada paquete antes de guardarlo.
              """,
              sugiere="Mirá los primeros bytes del contenido: una imagen PNG empieza con `\"\\x89PNG\"` y una JPEG con `\"\\xFF\\xD8\"`. El nombre no importa.",
              desafio="Aceptá solo los archivos que de verdad son PNG o JPEG.",
              inicial='''
                  <?php
                  $subidos = [
                      'retrato.png' => "\\x89PNG\\r\\n\\x1a\\n...",
                      'foto.jpg' => "\\xFF\\xD8\\xFF\\xE0...",
                      'gatito.png' => "<?php system('...');",
                  ];
                  foreach ($subidos as $nombre => $contenido) {
                      echo str_ends_with($nombre, '.png') || str_ends_with($nombre, '.jpg') ? "Guardado: $nombre\\n" : "Rechazado: $nombre\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function tipoReal(string $contenido): ?string
                  {
                      if (str_starts_with($contenido, "\\x89PNG")) {
                          return 'png';
                      }
                      if (str_starts_with($contenido, "\\xFF\\xD8")) {
                          return 'jpg';
                      }
                      return null;
                  }

                  $subidos = [
                      'retrato.png' => "\\x89PNG\\r\\n\\x1a\\n...",
                      'foto.jpg' => "\\xFF\\xD8\\xFF\\xE0...",
                      'gatito.png' => "<?php system('...');",
                  ];
                  foreach ($subidos as $nombre => $contenido) {
                      echo tipoReal($contenido) !== null ? "Guardado: $nombre\\n" : "Rechazado: $nombre\\n";
                  }
              ''',
              al_superar="El «gatito.png» queda afuera: adentro no había ningún gato. El troll que venía escondido en él se va con las manos vacías.",
              imagen=["Una mesa de revisión con tres paquetes abiertos: dos con cuadros adentro y uno con humo violeta saliendo.",
                      NILO + " cierra el paquete del humo con cara de susto.", "Un troll chiquito asoma del humo.", GHECO + " sobre un cuadro."]),
            m(id="R03-N07-P2", titulo="El registro de los robos",
              lugar=REVISOR, personajes="Nilo, Elefa, Gheco",
              carta="JSON | json_encode($datos, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) · file_put_contents · json_decode($texto, true) da un array",
              recompensa="xp 15, oro 15",
              escena="""
                  Mientras no haya bodega, los registros se guardan en archivos JSON. Revisando el registro de robos de hace veinte años, Nilo encuentra una línea: *«paquete para quien llegue, robado del Albatros por un ladrón de techos»*.
              """,
              sugiere="Guardá los registros con `json_encode` en un archivo y leelos con `json_decode($texto, true)`. Después buscá el que dice «para quien llegue».",
              desafio="Guardá el registro, volvé a leerlo y encontrá la línea del robo.",
              inicial='''
                  <?php
                  $robos = [
                      ['anio' => 2003, 'que' => 'un barril de aceite', 'barco' => 'Tortuga'],
                      ['anio' => 2006, 'que' => 'paquete para quien llegue', 'barco' => 'Albatros'],
                  ];
                  echo "Robos guardados: 0\\n";
              ''',
              solucion='''
                  <?php
                  $robos = [
                      ['anio' => 2003, 'que' => 'un barril de aceite', 'barco' => 'Tortuga'],
                      ['anio' => 2006, 'que' => 'paquete para quien llegue', 'barco' => 'Albatros'],
                  ];
                  file_put_contents('robos.json', json_encode($robos, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

                  $leidos = json_decode(file_get_contents('robos.json'), true);
                  echo "Robos guardados: " . count($leidos) . "\\n";
                  foreach ($leidos as $r) {
                      if (str_contains($r['que'], 'quien llegue')) {
                          echo "{$r['anio']}: {$r['que']}, del {$r['barco']}\\n";
                      }
                  }
              ''',
              al_superar="—Eran dos envíos —dice Elefa, sin levantar la vista—. Uno se lo llevó él. El otro lo guardé yo. —Y no dice nada más.",
              imagen=["Un archivo de la oficina de correos con cajones abiertos y un papel viejo amarillento con un dibujo de un tejado y una figura saltando.",
                      NILO + " lee el papel a la luz de un farol.", ELEFA + " de espaldas, mirando por la ventana.", GHECO + " sobre el cajón."]),
            m(id="R03-N07-P3", titulo="Un nombre nuestro",
              lugar=REVISOR, personajes="Nilo, Iara, Gheco",
              carta="Guardar con nombre propio | el nombre del cliente puede traer ../ o ser repetido · se genera uno: número de registro + extensión según el tipo real",
              recompensa="xp 10, oro 10",
              escena="""
                  Un cliente subió un archivo llamado `../../tablero.png`, y el revisor casi lo guarda **encima** del tablero de avisos. Iara propone que cada archivo se guarde con un número de registro.
              """,
              sugiere="Ignorá el nombre que trae: armá uno con el número de registro y la extensión del tipo real, como `envio-0007.png`.",
              desafio="Generá el nombre con el número y la extensión.",
              inicial='''
                  <?php
                  $subidas = [['../../tablero.png', 'png'], ['mi foto (1).JPG', 'jpg']];
                  $numero = 7;
                  foreach ($subidas as [$nombreOriginal, $tipo]) {
                      echo "Guardo como: $nombreOriginal\\n";
                      $numero++;
                  }
              ''',
              solucion='''
                  <?php
                  $subidas = [['../../tablero.png', 'png'], ['mi foto (1).JPG', 'jpg']];
                  $numero = 7;
                  foreach ($subidas as [$nombreOriginal, $tipo]) {
                      $nombre = sprintf('envio-%04d.%s', $numero, $tipo);
                      echo "Guardo como: $nombre\\n";
                      $numero++;
                  }
              ''',
              al_superar="El tablero de avisos se salva. Iara anota el número siete y el ocho en la libreta, en orden.",
              imagen=["Un estante con cajitas numeradas con puntitos de colores, una con un paquete adentro.",
                      IARA + " pone una etiqueta en una cajita.", NILO + " le alcanza el paquete.", GHECO + " sobre el estante."]),
        ],
    },
    {
        "titulo": "R03-N08 · Plantillas y organización",
        "misiones": [
            m(id="R03-N08-P1", titulo="Un molde de cartel",
              lugar=CARTELES, personajes="Nilo, Elefa, Gheco",
              carta="Layout | una función arma el encabezado y el pie · cada página solo pasa su parte · si cambia el horario, cambia una vez",
              recompensa="xp 10, oro 10",
              escena="""
                  La Oficina ya tiene veinte ventanillas, cada una con su cartel pintado a mano. Cuando cambió el horario, Nilo tuvo que repintar los veinte, y en tres se olvidó del domingo. Elefa mandó hacer un **molde de cartel**.
              """,
              sugiere="Una función `cartel(string $ventanilla): string` que devuelve el marco común con el horario, y en el medio, lo de cada ventanilla.",
              desafio="Escribí el molde y usalo para las tres ventanillas.",
              inicial='''
                  <?php
                  echo "[Puerto | Envios | Lun a Sab]\\n";
                  echo "[Puerto | Consultas | Lun a Sab]\\n";
                  echo "[Puerto | Encomiendas | Lun a Vie]\\n";
              ''',
              solucion='''
                  <?php
                  const HORARIO = 'Lun a Dom';

                  function cartel(string $ventanilla): string
                  {
                      return "[Puerto | $ventanilla | " . HORARIO . "]";
                  }

                  foreach (['Envios', 'Consultas', 'Encomiendas'] as $v) {
                      echo cartel($v) . "\\n";
                  }
              ''',
              al_superar="El domingo aparece en las tres ventanillas a la vez. Los pintores del Puerto se quedan sin trabajo; Elefa los manda al Astillero.",
              imagen=["Una fila de ventanillas iguales con carteles con el mismo marco y el mismo sello, cada uno con un dibujito distinto en el medio.",
                      ELEFA + " mira la fila satisfecha.", NILO + " cuelga el último cartel.", GHECO + " sobre un cartel."]),
            m(id="R03-N08-P2", titulo="La función vista()",
              lugar=CARTELES, personajes="Nilo, Gheco",
              carta="vista() | extract($datos) convierte claves en variables · ob_start() junta lo que se imprime · ob_get_clean() lo devuelve como texto",
              recompensa="xp 15, oro 15",
              escena="""
                  Las páginas de Nilo mezclan todo: cuentas, consultas y HTML en el mismo archivo. Gheco le muestra cómo separar: la página decide **qué** mostrar y la vista, **cómo**.
              """,
              sugiere="La vista es un archivo con HTML y `<?= ?>`. La función `vista()` hace `extract($datos)`, `ob_start()`, `require` del archivo y devuelve `ob_get_clean()`.",
              desafio="Completá `vista()` para que arme la página con la plantilla.",
              inicial='''
                  <?php
                  file_put_contents('saludo.php', '<h1>Hola, <?= htmlspecialchars($nombre) ?></h1><p>Tenes <?= $envios ?> envios.</p>');

                  function vista(string $archivo, array $datos): string
                  {
                      return '';
                  }

                  echo vista('saludo.php', ['nombre' => 'Iara', 'envios' => 3]) . "\\n";
              ''',
              solucion='''
                  <?php
                  file_put_contents('saludo.php', '<h1>Hola, <?= htmlspecialchars($nombre) ?></h1><p>Tenes <?= $envios ?> envios.</p>');

                  function vista(string $archivo, array $datos): string
                  {
                      extract($datos);
                      ob_start();
                      require $archivo;
                      return ob_get_clean();
                  }

                  echo vista('saludo.php', ['nombre' => 'Iara', 'envios' => 3]) . "\\n";
              ''',
              al_superar="La página de Iara sale armada con la plantilla. Si mañana cambia el diseño, se toca un solo archivo.",
              imagen=["Una mesa de imprenta con un molde de página vacío y letras de plomo al lado, sin letras legibles.",
                      NILO + " pone el molde en la prensa.", GHECO + " sobre la prensa."]),
            m(id="R03-N08-P3", titulo="Un pedacito que se repite",
              lugar=CARTELES, personajes="Nilo, Iara, Gheco",
              carta="Parciales | un pedacito (la tarjeta de un barco) en su propia función o archivo · se usa en el listado, en el detalle y en el buscador",
              recompensa="xp 10, oro 10",
              escena="""
                  La tarjeta de un barco aparece en tres páginas, y en cada una Nilo la escribió distinta. Iara le muestra las tres juntas: una tiene el calado, otra no, y la otra lo tiene mal.
              """,
              sugiere="Una función `tarjeta(array $barco): string` que arme siempre lo mismo, y las tres páginas la usan.",
              desafio="Escribí la tarjeta una vez y usala en las dos listas.",
              inicial='''
                  <?php
                  $barcos = [['nombre' => 'Gaviota', 'calado' => 3], ['nombre' => 'Albatros', 'calado' => 8]];

                  echo "Listado:\\n";
                  foreach ($barcos as $b) {
                      echo "- {$b['nombre']}\\n";
                  }
                  echo "Buscador:\\n";
                  echo "- {$barcos[1]['nombre']} (calado ?)\\n";
              ''',
              solucion='''
                  <?php
                  $barcos = [['nombre' => 'Gaviota', 'calado' => 3], ['nombre' => 'Albatros', 'calado' => 8]];

                  function tarjeta(array $b): string
                  {
                      return "- {$b['nombre']} (calado {$b['calado']} m)";
                  }

                  echo "Listado:\\n";
                  foreach ($barcos as $b) {
                      echo tarjeta($b) . "\\n";
                  }
                  echo "Buscador:\\n";
                  echo tarjeta($barcos[1]) . "\\n";
              ''',
              al_superar="Las tres páginas muestran la misma tarjeta. Iara las pone una al lado de la otra: idénticas. Asiente.",
              imagen=["Tres tarjetas de cartón iguales con el dibujo de un barco y una línea de agua, sobre un mostrador.",
                      IARA + " las compara.", NILO + " sostiene el sello con que las imprimió.", GHECO + " sobre una tarjeta."]),
        ],
    },
    {
        "titulo": "R03-N09 · Jefe: la Gorgona de los Formularios",
        "misiones": [
            m(id="R03-N09-P1", titulo="Los cabellos sin validar",
              lugar=ULTIMO_PISO, personajes="Nilo, Gheco",
              criatura="dragon",
              carta="Validar todo | una función por formulario · devuelve los errores por campo · email con filter_var(FILTER_VALIDATE_EMAIL) · números con rango",
              recompensa="xp 15, oro 15",
              escena="""
                  En el último piso vive la **Gorgona de los Formularios**: sus cabellos son cintas de papel sin validar que se retuercen. Un email sin arroba, un precio negativo. Quien la mira sin validar, queda de piedra.
              """,
              sugiere="Validá el email con `filter_var($email, FILTER_VALIDATE_EMAIL)` y el precio como entero positivo. Devolvé los errores por campo.",
              desafio="Escribí `validarPedido` y probala con el pedido de la Gorgona.",
              inicial='''
                  <?php
                  function validarPedido(array $p): array
                  {
                      return [];
                  }

                  $deLaGorgona = ['email' => 'gorgona.sin.arroba', 'precio' => '-50'];
                  $errores = validarPedido($deLaGorgona);
                  echo $errores === [] ? "Pedido aceptado\\n" : implode("\\n", $errores) . "\\n";
              ''',
              solucion='''
                  <?php
                  function validarPedido(array $p): array
                  {
                      $errores = [];
                      if (filter_var($p['email'] ?? '', FILTER_VALIDATE_EMAIL) === false) {
                          $errores['email'] = 'email: no es valido';
                      }
                      if (filter_var($p['precio'] ?? '', FILTER_VALIDATE_INT, ['options' => ['min_range' => 1]]) === false) {
                          $errores['precio'] = 'precio: tiene que ser un entero positivo';
                      }
                      return $errores;
                  }

                  $deLaGorgona = ['email' => 'gorgona.sin.arroba', 'precio' => '-50'];
                  $errores = validarPedido($deLaGorgona);
                  echo $errores === [] ? "Pedido aceptado\\n" : implode("\\n", $errores) . "\\n";
              ''',
              al_superar="Dos cabellos de papel se quedan quietos, desarmados. La Gorgona sisea, molesta.",
              imagen=["El último piso de la oficina de correos, oscuro, con papeles volando.",
                      GORGONA + " con dos cintas de papel caídas.", NILO + " con un escudo pulido como espejo.", GHECO + " detrás del escudo."]),
            m(id="R03-N09-P2", titulo="El escudo espejo",
              lugar=ULTIMO_PISO, personajes="Nilo, Elefa, Gheco",
              criatura="dragon",
              carta="Escapar según el lugar | htmlspecialchars en HTML y atributos · urlencode en direcciones · json_encode en JSON · nunca el dato crudo",
              recompensa="xp 15, oro 15",
              escena="""
                  Elefa le da a Nilo un escudo pulido como espejo. —No se la enfrenta de frente. —La Gorgona le lanza un nombre con trampa para que lo muestre en tres lugares: en la página, en un enlace y en un JSON.
              """,
              sugiere="Cada lugar tiene su forma de escapar: `htmlspecialchars` para el HTML, `urlencode` para la dirección y `json_encode` para el JSON.",
              desafio="Escapá el nombre en los tres lugares.",
              inicial='''
                  <?php
                  $nombre = '<b>Gorgona</b> & "amigas"';
                  echo "<p>$nombre</p>\\n";
                  echo "/buscar?q=$nombre\\n";
                  echo '{"nombre":"' . $nombre . '"}' . "\\n";
              ''',
              solucion='''
                  <?php
                  $nombre = '<b>Gorgona</b> & "amigas"';
                  echo "<p>" . htmlspecialchars($nombre) . "</p>\\n";
                  echo "/buscar?q=" . urlencode($nombre) . "\\n";
                  echo json_encode(['nombre' => $nombre]) . "\\n";
              ''',
              al_superar="El nombre tramposo aparece tres veces, desarmado en las tres. La Gorgona se ve reflejada en el escudo y se le endurece una mano.",
              imagen=["Un escudo de bronce pulido como espejo que refleja a una criatura con pelo de papel.",
                      NILO + " sostiene el escudo con las dos manos.", ELEFA + " detrás de él, con el bastón en alto.", GHECO + " sobre el borde del escudo."]),
            m(id="R03-N09-P3", titulo="La Gorgona de piedra",
              lugar=ULTIMO_PISO, personajes="Nilo, Iara, Elefa, Gheco",
              criatura="dragon",
              carta="Todo junto | login con huella · token en cada formulario · validar en el servidor · escapar al mostrar · lo que no pasa, se rechaza con su motivo",
              recompensa="xp 25, oro 30", item="Bolso Remendado",
              escena="""
                  La Gorgona manda su último ataque: tres pedidos a la vez. Uno sin sesión, uno sin token y uno con un comentario tramposo. El sitio de Nilo tiene que atender los tres sin dejarse engañar por ninguno.
              """,
              sugiere="Una función `atender()` que revisa en orden: ¿hay usuario?, ¿el token coincide?, ¿el comentario es válido? Si todo está bien, muestra el comentario escapado.",
              desafio="Completá `atender` con las tres defensas.",
              inicial='''
                  <?php
                  function atender(array $sesion, array $post): string
                  {
                      return "Publicado: " . $post['comentario'];
                  }

                  $sesion = ['usuario' => 'nilo', 'token' => 'abc123'];
                  $pedidos = [
                      [[], ['token' => 'abc123', 'comentario' => 'Hola']],
                      [$sesion, ['token' => 'falso', 'comentario' => 'Hola']],
                      [$sesion, ['token' => 'abc123', 'comentario' => '<script>piedra()</script>']],
                  ];
                  foreach ($pedidos as [$s, $p]) {
                      echo atender($s, $p) . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function atender(array $sesion, array $post): string
                  {
                      if (!isset($sesion['usuario'])) {
                          return "Rechazado: primero hay que entrar";
                      }
                      if (!hash_equals($sesion['token'] ?? '', $post['token'] ?? '')) {
                          return "Rechazado: el formulario no es nuestro";
                      }
                      $comentario = trim($post['comentario'] ?? '');
                      if ($comentario === '' || mb_strlen($comentario) > 200) {
                          return "Rechazado: comentario vacio o muy largo";
                      }
                      return "Publicado: " . htmlspecialchars($comentario);
                  }

                  $sesion = ['usuario' => 'nilo', 'token' => 'abc123'];
                  $pedidos = [
                      [[], ['token' => 'abc123', 'comentario' => 'Hola']],
                      [$sesion, ['token' => 'falso', 'comentario' => 'Hola']],
                      [$sesion, ['token' => 'abc123', 'comentario' => '<script>piedra()</script>']],
                  ];
                  foreach ($pedidos as [$s, $p]) {
                      echo atender($s, $p) . "\\n";
                  }
              ''',
              al_superar="Los tres ataques rebotan. La Gorgona se ve reflejada en el escudo y se queda de piedra ella. Mientras tanto, Iara le cose el bolso a Nilo: un bolsillo nuevo con su nombre bordado, para lo que tiene que recordar. Es **el Bolso Remendado**. Elefa hace sonar la campana tres veces.",
              imagen=["El último piso de la oficina de correos con una estatua de piedra gris de una mujer-serpiente con el pelo de papel petrificado.",
                      IARA + " cose un parche en el bolso de Nilo con hilo turquesa.", NILO + " con el escudo apoyado en el piso.", ELEFA + " hace sonar una campana.", GHECO + " sobre la estatua."]),
        ],
    },
]
