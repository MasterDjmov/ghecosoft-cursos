from genphp import m
from php_r01 import NILO, ELEFA, IARA, PICO, GHECO

FILA = "La fila de barcos al amanecer"
BODEGA3 = "La bodega del tercer muelle"
OFICINAS = "Las oficinas de la torre"
ESTANTE = "El estante de los tomos"
ROCA = "La Roca de la Sirena"
SIRENA = "la Sirena de los Tipos Débiles (sirena de pelo largo de algas verdes, top de escamas y caracolas, cola de escamas violetas, un ojo cian y otro violeta, sentada en una roca con musgo entre burbujas)"

NODOS = [
    {
        "titulo": "R01-N06 · Bucles: while, do-while, for y foreach",
        "misiones": [
            m(id="R01-N06-P1", titulo="Descargar hasta vaciar",
              lugar=FILA, personajes="Nilo, Gheco",
              carta="while | while (cond) { … } repite mientras se cumpla · algo adentro tiene que cambiar la condición, o no termina",
              recompensa="xp 10, oro 10",
              escena="""
                  Al amanecer, un barco espera para descargar 4 cajones. Nilo baja cajones a toda velocidad… y cuando el barco queda vacío sigue bajando cajones que no existen, con los brazos en el aire.
              """,
              sugiere="Adentro del `while` falta **descontar** el cajón que se bajó: `$cajones--;`. Si nada cambia, la condición se cumple para siempre (y el navegador corta a los 5 segundos).",
              desafio="Hacé que el bucle termine cuando no quedan cajones.",
              inicial='''
                  <?php
                  $cajones = 4;
                  while ($cajones > 0) {
                      echo "Bajo un cajon. Quedan $cajones.\\n";
                  }
                  echo "Barco vacio.\\n";
              ''',
              solucion='''
                  <?php
                  $cajones = 4;
                  while ($cajones > 0) {
                      $cajones--;
                      echo "Bajo un cajon. Quedan $cajones.\\n";
                  }
                  echo "Barco vacio.\\n";
              ''',
              al_superar="El barco queda vacío y Nilo baja los brazos. Iara, que lo miraba desde el muelle, le pone la libreta delante: «parar cuando no hay más».",
              imagen=["Un barco de carga amarrado al amanecer, con la bodega vacía, y una pila de cuatro cajones en el muelle.",
                      NILO + " con los brazos en el aire como cargando un cajón que no existe.", GHECO + " sobre la pila de cajones."]),
            m(id="R01-N06-P2", titulo="Contar con for",
              lugar=FILA, personajes="Nilo, Gheco",
              carta="for | for ($i = 1; $i <= 5; $i++) { … } · empieza, condición, paso · ideal cuando se sabe cuántas veces",
              recompensa="xp 10, oro 10",
              escena="""
                  Hay cinco barcos en la fila y a cada uno le toca un número de amarre, del 1 al 5. Nilo escribió los cinco `echo` a mano y se salteó el 4.
              """,
              sugiere="Un `for` cuenta solo: `for ($i = 1; $i <= 5; $i++)` pasa por 1, 2, 3, 4 y 5.",
              desafio="Reemplazá los `echo` sueltos por un `for` que numere los cinco barcos.",
              inicial='''
                  <?php
                  echo "Barco 1: amarre listo\\n";
                  echo "Barco 2: amarre listo\\n";
                  echo "Barco 3: amarre listo\\n";
                  echo "Barco 5: amarre listo\\n";
              ''',
              solucion='''
                  <?php
                  for ($i = 1; $i <= 5; $i++) {
                      echo "Barco $i: amarre listo\\n";
                  }
              ''',
              al_superar="El barco 4, que esperaba sin amarre desde hacía una hora, por fin atraca. El capitán le tira un pescado a Nilo, que lo esquiva.",
              imagen=["Una fila de cinco barcos de vela violeta esperando entrar a un puerto al amanecer.",
                      NILO + " en el muelle, señalando los barcos uno por uno.", GHECO + " en la proa del primer barco."]),
            m(id="R01-N06-P3", titulo="El cajón roto",
              lugar=FILA, personajes="Nilo, Gheco",
              carta="continue y break | continue salta a la siguiente vuelta · break sale del bucle · útiles en un foreach",
              recompensa="xp 15, oro 15",
              escena="""
                  El jefe de estibadores aparta los cajones rotos y sigue con el próximo. Nilo, en cambio, los anota igual en la lista de carga, y la bodega termina llena de astillas.
              """,
              sugiere="Dentro del `foreach`, si el cajón está roto, `continue;` lo saltea y pasa al siguiente.",
              desafio="Salteá los cajones rotos y sumá solo los kilos de los sanos.",
              inicial='''
                  <?php
                  $cajones = [12, "roto", 8, 20, "roto", 5];
                  $total = 0;
                  foreach ($cajones as $kilos) {
                      echo "Cargo $kilos\\n";
                      $total += (int) $kilos;
                  }
                  echo "Total: $total kg\\n";
              ''',
              solucion='''
                  <?php
                  $cajones = [12, "roto", 8, 20, "roto", 5];
                  $total = 0;
                  foreach ($cajones as $kilos) {
                      if ($kilos === "roto") {
                          continue;
                      }
                      echo "Cargo $kilos\\n";
                      $total += $kilos;
                  }
                  echo "Total: $total kg\\n";
              ''',
              al_superar="La bodega queda limpia de astillas. El jefe de estibadores le da una palmada a Nilo que casi lo tira al agua.",
              imagen=["Un muelle con una fila de cajones de madera y dos cajones rotos, con astillas, apartados a un costado.",
                      NILO + " aparta un cajón roto con el pie.", GHECO + " sobre un cajón sano."]),
            m(id="R01-N06-P4", titulo="Leer hasta que no haya más",
              lugar=FILA, personajes="Nilo, Iara, Gheco",
              carta="Leer todo | while (($r = fgets(STDIN)) !== false) { … } · fgets da false cuando no hay más renglones",
              recompensa="xp 15, oro 15",
              escena="""
                  Iara le pasa a Nilo la lista de pesos de la mañana, uno por renglón. Nilo lee solo el primero y se va a almorzar. —¿Y los demás? —pregunta Iara.
              """,
              sugiere="`fgets(STDIN)` devuelve `false` cuando ya no quedan renglones. Un `while` que lee hasta `false` recorre la entrada entera.",
              desafio="Leé todos los pesos, mostralos y sumalos.",
              inicial='''
                  <?php
                  $total = 0;
                  $renglon = fgets(STDIN);
                  $peso = (int) trim($renglon);
                  echo "Peso: $peso\\n";
                  $total += $peso;
                  echo "Total: $total kg\\n";
              ''',
              entrada="12\n30\n7\n",
              solucion='''
                  <?php
                  $total = 0;
                  while (($renglon = fgets(STDIN)) !== false) {
                      $peso = (int) trim($renglon);
                      echo "Peso: $peso\\n";
                      $total += $peso;
                  }
                  echo "Total: $total kg\\n";
              ''',
              al_superar="Cuarenta y nueve kilos, todos anotados. Iara tacha la lista. Nilo se va a almorzar, esta vez con la conciencia tranquila.",
              imagen=["Una lista larga de papel que cae desde un mostrador hasta el piso del muelle, con marcas de tilde, sin letras.",
                      IARA + " sostiene la punta de la lista.", NILO + " la lee renglón por renglón.", GHECO + " sobre el mostrador."]),
        ],
    },
    {
        "titulo": "R01-N07 · Arrays: listas y diccionarios",
        "misiones": [
            m(id="R01-N07-P1", titulo="La etiqueta que se llevó Pico",
              lugar=BODEGA3, personajes="Nilo, Pico, Gheco",
              criatura="orco",
              carta="Diccionarios | $stock = ['sal' => 4]; · $stock['sal'] lee · isset($stock['x']) o ?? para lo que puede no estar",
              recompensa="xp 10, oro 10",
              escena="""
                  En la bodega del tercer muelle, cada cajón tiene una etiqueta con un nombre. Una gaviota regordeta con una mancha violeta en el ala arranca la etiqueta *sal* y se la lleva en el pico: es **Pico**, la gaviota ladrona del Puerto. Cuando Nilo busca la sal, aparece un **orco**: `Undefined array key`.
              """,
              sugiere="Para una clave que puede no estar, `$stock['sal'] ?? 0` da 0 en lugar del aviso.",
              desafio="Leé el stock sin que aparezca el orco: lo que no está, cuenta como 0.",
              inicial='''
                  <?php
                  $stock = ['harina' => 6, 'aceite' => 3];
                  echo "Harina: " . $stock['harina'] . "\\n";
                  echo "Sal: " . $stock['sal'] . "\\n";
              ''',
              solucion='''
                  <?php
                  $stock = ['harina' => 6, 'aceite' => 3];
                  echo "Harina: " . ($stock['harina'] ?? 0) . "\\n";
                  echo "Sal: " . ($stock['sal'] ?? 0) . "\\n";
              ''',
              al_superar="El orco se queda sin lugar donde atacar. —¡No le digan nada a Pico, que es buena! —grita Nilo, que adora a las gaviotas.",
              imagen=["Una bodega de estantes de madera con cajones etiquetados con dibujitos lisos (una espiga, un frasco, una gota), de noche.",
                      PICO + " vuela con una etiqueta en el pico.", NILO + " la mira encantado.", "Un orco verde asoma detrás de un estante vacío.", GHECO + " sobre un cajón."]),
            m(id="R01-N07-P2", titulo="Recorrer con clave y valor",
              lugar=BODEGA3, personajes="Nilo, Gheco",
              carta="foreach | foreach ($stock as $producto => $cantidad) { … } · recorre todo el diccionario, en orden",
              recompensa="xp 10, oro 10",
              escena="""
                  El bodeguero le pide a Nilo el inventario entero de la bodega. Nilo escribe un `echo` por producto y se olvida del aceite.
              """,
              sugiere="`foreach ($stock as $producto => $cantidad)` pasa por cada par del diccionario, sin olvidarse de ninguno.",
              desafio="Mostrá el inventario entero con un `foreach`.",
              inicial='''
                  <?php
                  $stock = ['harina' => 6, 'sal' => 2, 'aceite' => 3];
                  echo "harina: 6\\n";
                  echo "sal: 2\\n";
              ''',
              solucion='''
                  <?php
                  $stock = ['harina' => 6, 'sal' => 2, 'aceite' => 3];
                  foreach ($stock as $producto => $cantidad) {
                      echo "$producto: $cantidad\\n";
                  }
              ''',
              al_superar="Tres productos, tres renglones. El bodeguero lo firma sin contar: ya aprendió a confiar en los bucles.",
              imagen=["Una bodega con tres estantes llenos: bolsas de harina, bolsitas de sal y botellas de aceite.",
                      NILO + " recorre los estantes con una lista.", GHECO + " sobre una bolsa de harina."]),
            m(id="R01-N07-P3", titulo="La tabla de los barcos",
              lugar=BODEGA3, personajes="Nilo, Iara, Gheco",
              carta="Arrays de arrays | $barcos = [['nombre' => 'Gaviota', 'kilos' => 300], …] · foreach por fila · $b['kilos'] por columna",
              recompensa="xp 15, oro 15",
              escena="""
                  Iara lleva la tabla de los barcos del día: cada barco es una fila con su nombre y sus kilos. Le pide a Nilo que muestre solo los que pasan los 500 kilos, para mandarlos a la bodega grande.
              """,
              sugiere="Cada `$b` del `foreach` es una fila: `$b['nombre']` y `$b['kilos']`. Un `if` adentro elige cuáles mostrar.",
              desafio="Mostrá solo los barcos de más de 500 kilos.",
              inicial='''
                  <?php
                  $barcos = [
                      ['nombre' => 'Gaviota', 'kilos' => 300],
                      ['nombre' => 'Albatros', 'kilos' => 820],
                      ['nombre' => 'Tortuga', 'kilos' => 510],
                      ['nombre' => 'Triton', 'kilos' => 90],
                  ];
                  foreach ($barcos as $b) {
                      echo $b['nombre'] . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $barcos = [
                      ['nombre' => 'Gaviota', 'kilos' => 300],
                      ['nombre' => 'Albatros', 'kilos' => 820],
                      ['nombre' => 'Tortuga', 'kilos' => 510],
                      ['nombre' => 'Triton', 'kilos' => 90],
                  ];
                  foreach ($barcos as $b) {
                      if ($b['kilos'] > 500) {
                          echo $b['nombre'] . ": " . $b['kilos'] . " kg\\n";
                      }
                  }
              ''',
              al_superar="El Albatros y la Tortuga van a la bodega grande. Iara tilda la tabla con dos rayitas prolijas.",
              imagen=["Una tabla de madera colgada en una bodega con cuatro dibujos de barcos, dos marcados con un círculo violeta, sin letras.",
                      IARA + " marca la tabla con el lápiz.", NILO + " señala uno de los barcos.", GHECO + " sobre la tabla."]),
            m(id="R01-N07-P4", titulo="Ordenar y filtrar",
              lugar=BODEGA3, personajes="Nilo, Gheco",
              carta="Funciones de arrays | count · array_sum · max · sort ordena · array_filter($a, fn($x) => …) se queda con los que cumplen",
              recompensa="xp 15, oro 15",
              escena="""
                  Al final del día, el bodeguero pide un resumen de los pesos: cuántos cajones hubo, cuánto suman, el más pesado y la lista ordenada. Nilo saca la calculadora. Gheco le muestra que PHP ya trae todo eso.
              """,
              sugiere="`count`, `array_sum` y `max` resumen la lista; `sort($pesos)` la ordena de menor a mayor (cambia la lista misma) e `implode(\", \", $pesos)` la une en un texto.",
              desafio="Completá el resumen.",
              inicial='''
                  <?php
                  $pesos = [12, 40, 7, 25, 18];
                  echo "Cajones: ?\\n";
                  echo "Total: ?\\n";
                  echo "El mas pesado: ?\\n";
                  echo "Ordenados: ?\\n";
              ''',
              solucion='''
                  <?php
                  $pesos = [12, 40, 7, 25, 18];
                  echo "Cajones: " . count($pesos) . "\\n";
                  echo "Total: " . array_sum($pesos) . "\\n";
                  echo "El mas pesado: " . max($pesos) . "\\n";
                  sort($pesos);
                  echo "Ordenados: " . implode(", ", $pesos) . "\\n";
              ''',
              al_superar="El resumen sale en un segundo. Nilo guarda la calculadora en el bolso. Se cae por el agujero.",
              imagen=["Una pila de cajones de madera ordenados de menor a mayor como una escalera, en una bodega.",
                      NILO + " sube la escalera de cajones.", GHECO + " en el cajón más alto."]),
        ],
    },
    {
        "titulo": "R01-N08 · Funciones",
        "misiones": [
            m(id="R01-N08-P1", titulo="La oficina de tarifas",
              lugar=OFICINAS, personajes="Nilo, Gheco",
              carta="Funciones | function tarifa(float $kilos): float { return …; } · se escribe una vez · se usa mil",
              recompensa="xp 10, oro 10",
              escena="""
                  Nilo pasó la mañana explicándole a cada capitán cómo se calcula la tarifa de su carga. Al décimo ya no tiene voz. En la torre, cada tarea tiene su oficina: la de tarifas recibe los kilos y devuelve el precio.
              """,
              sugiere="Una función recibe datos y **devuelve** un resultado con `return`. La tarifa es 3 sellos por kilo, más 10 de despacho.",
              desafio="Escribí la función `tarifa` y usala para los tres barcos.",
              inicial='''
                  <?php
                  // Escribí la función tarifa acá

                  echo "Gaviota: " . tarifa(20) . " sellos\\n";
                  echo "Albatros: " . tarifa(150) . " sellos\\n";
                  echo "Tortuga: " . tarifa(4) . " sellos\\n";
              ''',
              solucion='''
                  <?php
                  function tarifa(float $kilos): float
                  {
                      return $kilos * 3 + 10;
                  }

                  echo "Gaviota: " . tarifa(20) . " sellos\\n";
                  echo "Albatros: " . tarifa(150) . " sellos\\n";
                  echo "Tortuga: " . tarifa(4) . " sellos\\n";
              ''',
              al_superar="Los capitanes hacen fila en la oficina de tarifas y Nilo recupera la voz. La usa para silbar.",
              imagen=["Un pasillo de una torre con puertas de oficinas, una con un dibujo de una balanza, y capitanes de barco haciendo fila.",
                      NILO + " silbando apoyado en la pared.", GHECO + " sobre la puerta de la oficina."]),
            m(id="R01-N08-P2", titulo="Con tipos estrictos",
              lugar=OFICINAS, personajes="Nilo, Elefa, Gheco",
              criatura="goblin",
              carta="strict_types | declare(strict_types=1); arriba de todo · la función rechaza un \"20\" donde pide int · TypeError en vez de convertir callado",
              recompensa="xp 15, oro 15",
              escena="""
                  Un **goblin** le pasaba a la oficina de tarifas el texto «20» y la oficina, generosa, lo convertía callada. Elefa le puso a la oficina `strict_types`: —En mi Puerto, si piden un número, es un número. —Ahora el pedido de Nilo rebota con un `TypeError`.
              """,
              sugiere="Con `strict_types` la función ya no convierte sola. Lo que llega como texto se convierte **a propósito**, a la vista, antes de pasarlo: `tarifa((int) $pedido)`.",
              desafio="Arreglá la llamada para que la oficina reciba un número.",
              inicial='''
                  <?php
                  declare(strict_types=1);

                  function tarifa(int $kilos): int
                  {
                      return $kilos * 3 + 10;
                  }

                  $pedido = "20";
                  echo "A pagar: " . tarifa($pedido) . "\\n";
              ''',
              solucion='''
                  <?php
                  declare(strict_types=1);

                  function tarifa(int $kilos): int
                  {
                      return $kilos * 3 + 10;
                  }

                  $pedido = "20";
                  echo "A pagar: " . tarifa((int) $pedido) . "\\n";
              ''',
              al_superar="La conversión ahora se ve, escrita, a propósito. El goblin ya no puede colarse. Elefa sella la oficina con su bastón.",
              imagen=["Una oficina de tarifas en una torre, con una balanza y un mostrador de bronce.",
                      ELEFA + " sella el mostrador con el bastón.", "Un goblin flaco se va corriendo con una bolsita.", NILO + " detrás del mostrador.", GHECO + " sobre la balanza."]),
            m(id="R01-N08-P3", titulo="Valor por defecto",
              lugar=OFICINAS, personajes="Nilo, Gheco",
              carta="Por defecto | function f($x, $urgente = false) · si no se pasa, usa el valor de la firma · argumentos con nombre: f(kilos: 5, urgente: true)",
              recompensa="xp 10, oro 10",
              escena="""
                  Casi todos los envíos son comunes, pero algunos son urgentes y pagan el doble. Nilo escribió dos funciones casi iguales, `tarifa` y `tarifaUrgente`, y en una se equivocó el número.
              """,
              sugiere="Una sola función con un parámetro opcional: `function tarifa(int $kilos, bool $urgente = false)`. Si `$urgente` es `true`, el precio se duplica.",
              desafio="Escribí una sola función `tarifa` con `$urgente` opcional.",
              inicial='''
                  <?php
                  function tarifa(int $kilos): int
                  {
                      return $kilos * 3 + 10;
                  }

                  function tarifaUrgente(int $kilos): int
                  {
                      return ($kilos * 3 + 10) * 3;
                  }

                  echo "Comun: " . tarifa(10) . "\\n";
                  echo "Urgente: " . tarifaUrgente(10) . "\\n";
              ''',
              solucion='''
                  <?php
                  function tarifa(int $kilos, bool $urgente = false): int
                  {
                      $precio = $kilos * 3 + 10;
                      return $urgente ? $precio * 2 : $precio;
                  }

                  echo "Comun: " . tarifa(10) . "\\n";
                  echo "Urgente: " . tarifa(10, urgente: true) . "\\n";
              ''',
              al_superar="Una oficina, dos precios, ningún error. La función copiada se jubila.",
              imagen=["Una oficina de tarifas con un sello de urgente (un rayo dibujado) sobre un paquete, sin letras.",
                      NILO + " le pone el sello del rayo a un paquete.", GHECO + " sobre el paquete."]),
            m(id="R01-N08-P4", titulo="La función que se llama a sí misma",
              lugar=OFICINAS, personajes="Nilo, Iara, Gheco",
              carta="Recursión | una función que se llama a sí misma con un problema más chico · siempre con un caso base que corta",
              recompensa="xp 15, oro 15",
              escena="""
                  Las cajas del Puerto vienen una dentro de otra, como mamushkas: la caja 3 tiene adentro la 2, que tiene adentro la 1. Iara quiere un programa que las abra todas, de afuera hacia adentro.
              """,
              sugiere="`abrir($n)` muestra que abre la caja `$n` y, si `$n` es mayor que 1, se llama a sí misma con `$n - 1`. La caja 1 es el caso base: no tiene nada adentro.",
              desafio="Completá la función recursiva.",
              inicial='''
                  <?php
                  function abrir(int $n): void
                  {
                      echo "Abro la caja $n\\n";
                  }

                  abrir(3);
                  echo "Adentro: una carta\\n";
              ''',
              solucion='''
                  <?php
                  function abrir(int $n): void
                  {
                      echo "Abro la caja $n\\n";
                      if ($n > 1) {
                          abrir($n - 1);
                      }
                  }

                  abrir(3);
                  echo "Adentro: una carta\\n";
              ''',
              al_superar="En la caja más chica hay una carta para Nilo. Está en blanco. Iara la anota igual.",
              imagen=["Tres cajas de madera una dentro de otra, abiertas, sobre una mesa, y en la más chica un sobre.",
                      IARA + " abre la caja más chica.", NILO + " mira por encima de su hombro.", GHECO + " sobre la caja grande."]),
        ],
    },
    {
        "titulo": "R01-N09 · Organizar el código: include y require",
        "misiones": [
            m(id="R01-N09-P1", titulo="El tomo de las tarifas",
              lugar=ESTANTE, personajes="Nilo, Gheco",
              carta="Un archivo que devuelve | tarifas.php: <?php return [...]; · $t = require 'tarifas.php'; · la configuración en su propio archivo",
              recompensa="xp 10, oro 10",
              escena="""
                  El libro de instrucciones del Puerto ya no entra en un solo tomo: ahora hay un estante, y el tomo de las tarifas es un archivo aparte. El programa de Nilo lo crea (como lo haría alguien que lo escribe a mano) y después tiene que **traerlo**.
              """,
              sugiere="Un archivo que termina con `return [...]` se puede traer con `$tarifas = require 'tarifas.php';`: la variable recibe lo que devuelve.",
              desafio="Traé el tomo de las tarifas con `require` y usalo.",
              inicial='''
                  <?php
                  file_put_contents('tarifas.php', '<?php return ["comun" => 3, "urgente" => 6];');

                  $tarifas = [];
                  echo "Comun: " . ($tarifas['comun'] ?? '?') . " por kilo\\n";
                  echo "Urgente: " . ($tarifas['urgente'] ?? '?') . " por kilo\\n";
              ''',
              solucion='''
                  <?php
                  file_put_contents('tarifas.php', '<?php return ["comun" => 3, "urgente" => 6];');

                  $tarifas = require 'tarifas.php';
                  echo "Comun: " . ($tarifas['comun'] ?? '?') . " por kilo\\n";
                  echo "Urgente: " . ($tarifas['urgente'] ?? '?') . " por kilo\\n";
              ''',
              al_superar="El tomo llega del estante a la mesa y las tarifas aparecen. Si mañana cambian, se cambian en un solo lugar.",
              imagen=["Un estante alto de madera con tomos gruesos cerrados de lomos de colores, con dibujitos de una balanza, un sobre y un barco.",
                      NILO + " saca un tomo del estante.", GHECO + " sobre el estante."]),
            m(id="R01-N09-P2", titulo="Una sola vez",
              lugar=ESTANTE, personajes="Nilo, Gheco",
              criatura="esqueleto",
              carta="require_once | trae el archivo una sola vez aunque se pida dos · sin _once, una función repetida da Fatal error",
              recompensa="xp 15, oro 15",
              escena="""
                  Nilo trae el tomo de las etiquetas dos veces, por las dudas, y la oficina se traba: PHP grita que la función `etiqueta` ya existe. Del estante cae un **esqueleto** de tanto alboroto.
              """,
              sugiere="`require_once` recuerda qué archivos ya trajo y no lo vuelve a cargar. Cambiá los dos `require` por `require_once`.",
              desafio="Hacé que el tomo se cargue una sola vez.",
              inicial='''
                  <?php
                  file_put_contents('etiquetas.php', '<?php function etiqueta(string $d): string { return "[" . strtoupper($d) . "]"; }');

                  require 'etiquetas.php';
                  require 'etiquetas.php';
                  echo etiqueta("faro") . "\\n";
              ''',
              solucion='''
                  <?php
                  file_put_contents('etiquetas.php', '<?php function etiqueta(string $d): string { return "[" . strtoupper($d) . "]"; }');

                  require_once 'etiquetas.php';
                  require_once 'etiquetas.php';
                  echo etiqueta("faro") . "\\n";
              ''',
              al_superar="La oficina se destraba y el esqueleto vuelve a su estante, ofendido.",
              imagen=["Un estante con dos tomos iguales, uno encima del otro, y un esqueleto caído en el piso entre libros cerrados.",
                      NILO + " sostiene los dos tomos iguales, confundido.", GHECO + " sobre el estante."]),
            m(id="R01-N09-P3", titulo="El libro de las cartas sin entregar",
              lugar=ESTANTE, personajes="Nilo, Iara, Elefa, Gheco",
              carta="Depurar | var_dump($x) muestra tipo y valor · print_r($a) muestra un array legible · se busca dónde cambia lo que no debía",
              recompensa="xp 15, oro 15",
              escena="""
                  Buscando el tomo de tarifas, Nilo encuentra uno viejísimo: el **libro de las cartas sin entregar**. Todas las líneas están tachadas menos una. El programa que las cuenta dice que no queda ninguna pendiente. Iara sospecha del programa.
              """,
              sugiere="Mirá con `var_dump` qué hay en `$entregada` de la carta que falta: no es `true` ni `false`. Compará con `=== false` para contar solo las que de verdad no se entregaron.",
              desafio="Arreglá el dato para que el programa encuentre la carta pendiente y muestre para quién es.",
              inicial='''
                  <?php
                  $cartas = [
                      ['para' => 'Olmo', 'entregada' => true],
                      ['para' => 'Lia', 'entregada' => true],
                      ['para' => 'quien llegue', 'entregada' => 0],
                  ];
                  $pendientes = 0;
                  foreach ($cartas as $c) {
                      if ($c['entregada'] === false) {
                          $pendientes++;
                      }
                  }
                  echo "Pendientes: $pendientes\\n";
              ''',
              solucion='''
                  <?php
                  $cartas = [
                      ['para' => 'Olmo', 'entregada' => true],
                      ['para' => 'Lia', 'entregada' => true],
                      ['para' => 'quien llegue', 'entregada' => false],
                  ];
                  $pendientes = 0;
                  foreach ($cartas as $c) {
                      if ($c['entregada'] === false) {
                          $pendientes++;
                          echo "Sin entregar: para " . $c['para'] . "\\n";
                      }
                  }
                  echo "Pendientes: $pendientes\\n";
              ''',
              al_superar="Una carta sin entregar, hace veinte años: *«1 mensaje, para quien llegue. Retenido por la Capitana»*. Iara lo anota. Elefa aparece en la puerta, le saca el libro de las manos y no dice nada.",
              imagen=["Un libro enorme y viejo abierto sobre un atril, con todas las líneas tachadas con tinta menos una que brilla en violeta, sin letras legibles.",
                      NILO + " señala la línea que brilla.", IARA + " anota en su libreta.", ELEFA + " en la puerta, en sombra.", GHECO + " sobre el atril."]),
        ],
    },
    {
        "titulo": "R01-N10 · Jefe: la Sirena de los Tipos Débiles",
        "misiones": [
            m(id="R01-N10-P1", titulo="«10» es 10",
              lugar=ROCA, personajes="Nilo, Gheco",
              criatura="goblin",
              carta="La mentira 1 | \"10\" es un texto · 10 es un número · is_numeric antes de convertir · (int) a propósito",
              recompensa="xp 15, oro 15",
              escena="""
                  Sobre una roca con algas, la **Sirena de los Tipos Débiles** canta: *«el texto “10” es el número 10…»*. Los barcos que le creen suman «10 cajas» más 5 y les da 15, sin quejarse. Nilo tiene que demostrarle la verdad.
              """,
              sugiere="Antes de sumar, revisá con `is_numeric` cada texto: «10 cajas» no es un número y no se suma.",
              desafio="Sumá solo los textos que de verdad son números y avisá los que no.",
              inicial='''
                  <?php
                  $cargas = ["10", "10 cajas", "5", "tres"];
                  $total = 0;
                  foreach ($cargas as $c) {
                      $total += (int) $c;
                  }
                  echo "Total: $total\\n";
              ''',
              solucion='''
                  <?php
                  $cargas = ["10", "10 cajas", "5", "tres"];
                  $total = 0;
                  foreach ($cargas as $c) {
                      if (is_numeric($c)) {
                          $total += (int) $c;
                      } else {
                          echo "No es un numero: $c\\n";
                      }
                  }
                  echo "Total: $total\\n";
              ''',
              al_superar="La Sirena desafina. Uno de sus versos se deshace en burbujas.",
              imagen=["Una roca con algas en la boca de un puerto de noche, con burbujas brillantes alrededor.",
                      SIRENA + " canta con los brazos abiertos.", NILO + " en un bote chico frente a la roca, con la gorra bien puesta.", GHECO + " en la proa del bote."]),
            m(id="R01-N10-P2", titulo="El cero no es nada",
              lugar=ROCA, personajes="Nilo, Gheco",
              criatura="ogro",
              carta="La mentira 2 | 0, \"\", \"0\", null y false parecen lo mismo con == · empty() dice true para todos · se pregunta lo que se quiere saber",
              recompensa="xp 15, oro 15",
              escena="""
                  *«El cero es lo mismo que nada…»*, canta la Sirena. Un barco con 0 kilos de carga y otro sin dato aparecen iguales en la lista de Nilo: los dos «vacíos». Un **ogro** se frota las manos.
              """,
              sugiere="`empty($x)` es verdadero para 0 **y** para `null`. Para saber si falta el dato, preguntá `$kilos === null`.",
              desafio="Distinguí el barco con 0 kilos del que no tiene el dato.",
              inicial='''
                  <?php
                  $barcos = ['Gaviota' => 0, 'Albatros' => null, 'Tortuga' => 30];
                  foreach ($barcos as $nombre => $kilos) {
                      if (empty($kilos)) {
                          echo "$nombre: vacio\\n";
                      } else {
                          echo "$nombre: $kilos kg\\n";
                      }
                  }
              ''',
              solucion='''
                  <?php
                  $barcos = ['Gaviota' => 0, 'Albatros' => null, 'Tortuga' => 30];
                  foreach ($barcos as $nombre => $kilos) {
                      if ($kilos === null) {
                          echo "$nombre: falta el dato\\n";
                      } else {
                          echo "$nombre: $kilos kg\\n";
                      }
                  }
              ''',
              al_superar="Cero kilos es cero kilos; sin dato es sin dato. El ogro se va a buscar otra lista que no sepa distinguir.",
              imagen=["Dos botes iguales junto a la roca: uno vacío, con la bodega abierta, y otro envuelto en niebla.",
                      SIRENA + " sonríe engañosa.", NILO + " los compara desde su bote.", GHECO + " sobre el remo."]),
            m(id="R01-N10-P3", titulo="Lo que falta sí importa",
              lugar=ROCA, personajes="Nilo, Gheco",
              criatura="orco",
              carta="La mentira 3 | una clave que no está da Warning y null · se pregunta con isset o ?? · y se avisa qué falta",
              recompensa="xp 15, oro 15",
              escena="""
                  *«Lo que falta no importa…»*, canta la Sirena. El formulario de un barco llega sin el campo *destino*, el programa sigue de largo y un **orco** se lo lleva al fondo del mar.
              """,
              sugiere="Revisá cada campo obligatorio con `isset($formulario[$campo])` y juntá los que faltan en una lista. Si la lista no está vacía, se avisa.",
              desafio="Avisá qué campos faltan en vez de seguir de largo.",
              inicial='''
                  <?php
                  $formulario = ['barco' => 'Tortuga', 'kilos' => 300];
                  echo "Despacho: " . $formulario['barco'] . " a " . $formulario['destino'] . "\\n";
              ''',
              solucion='''
                  <?php
                  $formulario = ['barco' => 'Tortuga', 'kilos' => 300];
                  $faltan = [];
                  foreach (['barco', 'destino', 'kilos'] as $campo) {
                      if (!isset($formulario[$campo])) {
                          $faltan[] = $campo;
                      }
                  }
                  if ($faltan !== []) {
                      echo "Faltan: " . implode(", ", $faltan) . "\\n";
                  } else {
                      echo "Despacho: " . $formulario['barco'] . " a " . $formulario['destino'] . "\\n";
                  }
              ''',
              al_superar="El orco no encuentra nada que robar. La Sirena, por primera vez, se queda callada un verso entero.",
              imagen=["Un formulario de papel flotando sobre el agua oscura junto a la roca, con un casillero vacío marcado con un círculo, sin letras.",
                      "Un orco asoma del agua intentando agarrar el papel.", NILO + " lo rescata desde el bote.", GHECO + " sobre el papel."]),
            m(id="R01-N10-P4", titulo="La canción verdadera",
              lugar=ROCA, personajes="Nilo, Elefa, Gheco",
              criatura="dragon",
              carta="Todo junto | declare(strict_types=1) · funciones con tipos · === siempre · validar lo que entra · avisar lo que falta",
              recompensa="xp 25, oro 30", item="Caracola de la Sirena",
              escena="""
                  La Sirena canta su última mentira, la más larga: un manifiesto de carga lleno de textos que parecen números, ceros que parecen nada y datos que faltan. Nilo tiene que contestarle con un programa que no se deje engañar.
              """,
              sugiere="Una función `kilosValidos(array $carga): ?int` que devuelva el peso si es un entero positivo y `null` si no. Con `strict_types` y `===`, ninguna conversión pasa callada.",
              desafio="Completá la función y sumá solo las cargas válidas, avisando cuáles se rechazan.",
              inicial='''
                  <?php
                  declare(strict_types=1);

                  function kilosValidos(array $carga): ?int
                  {
                      return (int) $carga['kilos'];
                  }

                  $manifiesto = [
                      ['barco' => 'Gaviota', 'kilos' => '120'],
                      ['barco' => 'Albatros', 'kilos' => '0'],
                      ['barco' => 'Tortuga'],
                      ['barco' => 'Triton', 'kilos' => 'muchos'],
                      ['barco' => 'Colonia', 'kilos' => '80'],
                  ];
                  $total = 0;
                  foreach ($manifiesto as $carga) {
                      $total += kilosValidos($carga);
                  }
                  echo "Total: $total kg\\n";
              ''',
              solucion='''
                  <?php
                  declare(strict_types=1);

                  function kilosValidos(array $carga): ?int
                  {
                      $kilos = $carga['kilos'] ?? null;
                      if ($kilos === null || !ctype_digit($kilos) || (int) $kilos === 0) {
                          return null;
                      }
                      return (int) $kilos;
                  }

                  $manifiesto = [
                      ['barco' => 'Gaviota', 'kilos' => '120'],
                      ['barco' => 'Albatros', 'kilos' => '0'],
                      ['barco' => 'Tortuga'],
                      ['barco' => 'Triton', 'kilos' => 'muchos'],
                      ['barco' => 'Colonia', 'kilos' => '80'],
                  ];
                  $total = 0;
                  foreach ($manifiesto as $carga) {
                      $kilos = kilosValidos($carga);
                      if ($kilos === null) {
                          echo "Rechazado: " . $carga['barco'] . "\\n";
                      } else {
                          $total += $kilos;
                      }
                  }
                  echo "Total: $total kg\\n";
              ''',
              al_superar="La Sirena deja de cantar. Se mira las manos, como si las viera por primera vez, y se zambulle. En la roca queda una caracola nacarada: **la Caracola de la Sirena**. Si la escuchás, te dice el tipo de verdad de cada cosa. Elefa hace sonar la campana tres veces.",
              imagen=["Una roca con algas de noche, con una caracola nacarada violeta y verde agua brillando sobre el musgo, y burbujas que se apagan.",
                      SIRENA + " se zambulle, con la cola fuera del agua.", NILO + " en su bote, estirando la mano hacia la caracola.", GHECO + " en la proa."]),
        ],
    },
]
