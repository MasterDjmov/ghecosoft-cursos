from genphp import m

FARO_OCULTO = "El Faro del Portal Oculto"
SENDERO = "El Sendero de las Cartas Perdidas"
MOSTRADOR = "El mostrador de la torre"
MUELLE = "El Muelle de las Primeras Cartas"
PESAJE = "La oficina de pesaje"
CASILLEROS = "Los casilleros del correo"
ENCOMIENDAS = "La ventanilla de encomiendas"
CRUCE = "El Cruce de los Tres Muelles"
EJECUTAR = "Tocá **Ejecutar**: PHP corre acá mismo, en tu navegador (la primera vez baja PHP y tarda un poco)."
NILO = "Nilo (muchacho de 17, gorra de mensajero azul noche, bufanda violeta larga, chaqueta azul noche con costuras cian, bolso cruzado de cuero marrón con sobres de lacre violeta)"
ELEFA = "Elefa (elefanta enorme erguida en dos patas, armadura gris y violeta, colmillos cian, bastón coronado por un sello de lacre violeta)"
IARA = "Iara (chica de 16, bajita, piel morena, cola baja de pelo negro con cinta turquesa, lápiz detrás de la oreja, chaleco azul petróleo con sobres, libreta atada a la muñeca)"
PICO = "Pico (gaviota regordeta blanca y gris con una mancha violeta en un ala)"
GHECO = "Gheco (gecko de luz cian con antiparras, chiquito)"

NODOS = [
    {
        "titulo": "R00-N01 · Clase 0 · Hola, PHP",
        "misiones": [
            m(id="R00-N01-P1", titulo="¿Hay alguien?",
              lugar=FARO_OCULTO, personajes="Nilo, Gheco",
              carta="Mostrar texto | echo \"texto\\n\"; · <?php abre el modo PHP · \\n salta de línea · cada instrucción termina con ;",
              recompensa="xp 10, oro 10", item="Bolso Roto",
              escena="""
                  Nilo aparece en lo alto de un faro apagado, con la carta que perseguía en la mano: está en blanco. Sobre su hombro se enciende un gecko de luz con antiparras: **Gheco**.
                  —Acá las respuestas se escriben en PHP —le dice—. Si alguien pregunta «¿hay alguien?», se contesta. Probá.
              """,
              sugiere="`echo \"…\";` muestra el texto entre comillas, y `\\n` al final baja a la línea siguiente. " + EJECUTAR,
              desafio="Completá la instrucción para que Nilo conteste.",
              inicial='''
                  <?php
                  ___ "Si, aca estamos.\\n";
              ''',
              solucion='''
                  <?php
                  echo "Si, aca estamos.\\n";
              ''',
              al_superar="Abajo, en la bahía, una campana suena una vez, como si alguien hubiera recibido la respuesta. Nilo se da cuenta de que el bolso tiene la costura rota: es **el Bolso Roto**.",
              imagen=["En lo alto de un faro de piedra con la lámpara apagada, de noche y con tormenta, y abajo, lejos, un puerto iluminado con una torre.",
                      NILO + " sostiene un sobre en blanco y mira el puerto.", GHECO + " sobre su hombro."]),
            m(id="R00-N01-P2", titulo="Un slime en la escalera",
              lugar=FARO_OCULTO, personajes="Nilo, Gheco",
              criatura="slime",
              carta="Error de sintaxis | Parse error · PHP no ejecuta nada hasta que se arregla · el mensaje dice la línea · casi siempre falta un ;",
              recompensa="xp 10, oro 10",
              escena="""
                  Bajando la escalera de caracol del faro, Nilo pisa algo blando: un **slime**, una gota de baba verde que se alimenta de los punto y coma olvidados. Gheco le muestra el mensaje que dejó en la pared: `Parse error`.
              """,
              sugiere="Leé el error: dice en qué línea se dio cuenta PHP. Muchas veces el problema está en la línea **de arriba**: a cada instrucción le falta su `;`.",
              desafio="Encontrá lo que falta para que el programa ande.",
              inicial='''
                  <?php
                  echo "Escalon 1: listo\\n"
                  echo "Escalon 2: listo\\n";
              ''',
              solucion='''
                  <?php
                  echo "Escalon 1: listo\\n";
                  echo "Escalon 2: listo\\n";
              ''',
              al_superar="El slime se deshace en un charquito verde. —Leíste el error en lugar de adivinar —dice Gheco—. Eso es la mitad del oficio.",
              imagen=["Una escalera de caracol de piedra dentro de un faro, iluminada por la luz cian de un gecko.",
                      NILO + " baja con cuidado, mirando el escalón.", "Un slime verde y gelatinoso en un escalón, con cara de enojado.", GHECO + " flotando al lado."]),
            m(id="R00-N01-P3", titulo="Notas en el margen",
              lugar=SENDERO, personajes="Nilo, Gheco",
              carta="Comentarios | // una línea · # también · /* varias líneas */ · PHP los ignora: son para las personas",
              recompensa="xp 10, oro 10",
              escena="""
                  El Sendero de las Cartas Perdidas está lleno de sobres viejos enganchados en los arbustos. Nilo quiere anotar por dónde pasó, para no olvidarse, pero cada nota que escribe en el programa PHP la intenta ejecutar.
              """,
              sugiere="Lo que va después de `//` hasta el final del renglón es un **comentario**: PHP no lo ejecuta. Sirve para dejar notas.",
              desafio="Convertí la nota en un comentario para que el programa ande y muestre solo el recorrido.",
              inicial='''
                  <?php
                  Pase por el faro y despues por el sendero
                  echo "Faro\\n";
                  echo "Sendero\\n";
                  echo "Puerto\\n";
              ''',
              solucion='''
                  <?php
                  // Pase por el faro y despues por el sendero
                  echo "Faro\\n";
                  echo "Sendero\\n";
                  echo "Puerto\\n";
              ''',
              al_superar="La nota queda en el código, quieta, y el programa la saltea. —Es la primera vez que anoto algo —dice Nilo, orgulloso. Gheco no le cree.",
              imagen=["Un sendero de la costa de noche, con arbustos llenos de sobres viejos enganchados y el mar a un costado.",
                      NILO + " camina mirando los sobres de los arbustos.", GHECO + " sobre su gorra."]),
            m(id="R00-N01-P4", titulo="Tres renglones para la Capitana",
              lugar=MOSTRADOR, personajes="Nilo, Elefa, Gheco",
              carta="Saltos de línea | cada \\n baja un renglón · se pueden poner varios echo · o un solo echo con varios \\n",
              recompensa="xp 15, oro 15",
              escena="""
                  En el mostrador de la torre, la Capitana del Puerto, una elefanta enorme con armadura, le pide a Nilo que se presente en tres renglones: nombre, oficio y de dónde viene. Nilo lo escribe todo pegado.
              """,
              sugiere="Cada renglón termina con `\\n`. Si falta, el siguiente texto sigue en la misma línea.",
              desafio="Hacé que salgan tres renglones separados.",
              inicial='''
                  <?php
                  echo "Nilo";
                  echo "Mensajero";
                  echo "De la costa de los faros\\n";
              ''',
              solucion='''
                  <?php
                  echo "Nilo\\n";
                  echo "Mensajero\\n";
                  echo "De la costa de los faros\\n";
              ''',
              al_superar="—Elefa —dice la elefanta, y sella el papel con su bastón—. Me llamo Elefa. —Nilo asiente. Diez minutos después, le vuelve a preguntar cómo se llamaba.",
              imagen=["Un mostrador de madera en una torre con tubos de bronce que bajan del techo y una campana grande arriba.",
                      ELEFA + " sella un papel con el bastón.", NILO + " del otro lado del mostrador, rascándose la gorra.", GHECO + " sobre el mostrador."]),
        ],
    },
    {
        "titulo": "R01-N01 · Variables, tipos y conversiones",
        "misiones": [
            m(id="R01-N01-P1", titulo="El cajón del peso",
              lugar=MUELLE, personajes="Nilo, Gheco",
              carta="Variables | $nombre = valor; · empiezan con $ · se pueden cambiar · se muestran dentro de \"…\" o con .",
              recompensa="xp 10, oro 10",
              escena="""
                  En el primer muelle hay una fila de cajones con etiquetas pintadas a mano. A Nilo le toca anotar el barco, su carga y su peso. —Cada dato va en un cajón con nombre —le dice Gheco—. En PHP los cajones se llaman **variables** y su nombre empieza con `$`.
              """,
              sugiere="`$peso = 12.5;` guarda el valor en la variable. Dentro de comillas dobles, `\"Peso: $peso\"` muestra lo que tiene.",
              desafio="Creá las variables `$barco` (\"Gaviota\") y `$peso` (12.5) para que el programa las muestre.",
              inicial='''
                  <?php
                  // Creá $barco y $peso acá

                  echo "Barco: $barco\\n";
                  echo "Peso: $peso kg\\n";
              ''',
              solucion='''
                  <?php
                  $barco = "Gaviota";
                  $peso = 12.5;

                  echo "Barco: $barco\\n";
                  echo "Peso: $peso kg\\n";
              ''',
              al_superar="Los dos cajones quedan con su etiqueta y su contenido. Por primera vez, Nilo no tiene que acordarse de nada: está escrito.",
              imagen=["Un muelle de madera de noche, con cajones de madera en fila con etiquetas lisas pintadas a mano y faroles violetas.",
                      NILO + " pone una bolsa dentro de un cajón.", GHECO + " sobre un cajón, señalando la etiqueta."]),
            m(id="R01-N01-P2", titulo="¿Qué hay en el cajón?",
              lugar=MUELLE, personajes="Nilo, Gheco",
              carta="Tipos | int 12 · float 12.5 · string \"12\" · bool true/false · null · gettype($x) dice el tipo",
              recompensa="xp 10, oro 10",
              escena="""
                  Un estibador dejó cuatro cajones sin etiqueta de tipo. Nilo jura que en los cuatro hay «un doce». Gheco le pide que mire bien **qué tipo** de cosa hay en cada uno.
              """,
              sugiere="`gettype($x)` devuelve el nombre del tipo: `integer`, `double` (los decimales), `string`, `boolean` o `NULL`.",
              desafio="Mostrá el tipo de cada cajón con `gettype`.",
              inicial='''
                  <?php
                  $a = 12;
                  $b = 12.0;
                  $c = "12";
                  $d = true;

                  echo "a: " . ___ . "\\n";
                  echo "b: " . ___ . "\\n";
                  echo "c: " . ___ . "\\n";
                  echo "d: " . ___ . "\\n";
              ''',
              solucion='''
                  <?php
                  $a = 12;
                  $b = 12.0;
                  $c = "12";
                  $d = true;

                  echo "a: " . gettype($a) . "\\n";
                  echo "b: " . gettype($b) . "\\n";
                  echo "c: " . gettype($c) . "\\n";
                  echo "d: " . gettype($d) . "\\n";
              ''',
              al_superar="Cuatro doces, cuatro tipos distintos. Nilo se queda mirando el cajón del texto «12» como si lo hubiera engañado.",
              imagen=["Cuatro cajones de madera abiertos en un muelle, cada uno con algo distinto adentro: una pila de monedas, una balanza con medio peso, un papel enrollado y una luz que se prende.",
                      NILO + " mira los cajones rascándose la gorra.", GHECO + " sobre un cajón."]),
            m(id="R01-N01-P3", titulo="El medio kilo del goblin",
              lugar=MUELLE, personajes="Nilo, Gheco",
              criatura="goblin",
              carta="Casting | (int) corta los decimales · (float) los conserva · (int) \"12 kilos\" da 12 · convertir a propósito, nunca de casualidad",
              recompensa="xp 10, oro 10",
              escena="""
                  Un estibador mete en el cajón *peso* una bolsa que dice «12.5». Nilo la convierte a entero y el medio kilo desaparece: un **goblin** se va corriendo por el muelle con él bajo el brazo.
              """,
              sugiere="`(int)` corta los decimales; `(float)` los conserva. Para un peso con medio kilo hace falta un `float`.",
              desafio="Cambiá la conversión para que no se pierda el medio kilo.",
              inicial='''
                  <?php
                  $etiqueta = "12.5";
                  $peso = (int) $etiqueta;
                  echo "Peso: $peso kg\\n";
                  echo "Con el cajon: " . ($peso + 2) . " kg\\n";
              ''',
              solucion='''
                  <?php
                  $etiqueta = "12.5";
                  $peso = (float) $etiqueta;
                  echo "Peso: $peso kg\\n";
                  echo "Con el cajon: " . ($peso + 2) . " kg\\n";
              ''',
              al_superar="El goblin frena en seco, mira el medio kilo que ya no le pertenece y lo devuelve, de mala gana.",
              imagen=["Un muelle de madera de noche con cajones y una balanza.",
                      "Un goblin verde y flaco corre con una bolsita bajo el brazo.", NILO + " lo señala, sorprendido.", GHECO + " sobre la balanza."]),
            m(id="R01-N01-P4", titulo="Lo que no cambia",
              lugar=MUELLE, personajes="Nilo, Elefa, Gheco",
              carta="Constantes | const NOMBRE = valor; · sin $ · en MAYÚSCULAS · no se pueden cambiar después",
              recompensa="xp 15, oro 15",
              escena="""
                  Elefa le explica a Nilo que la tarifa del puerto es la misma para todos: 3 sellos por kilo. Nilo la guardó en una variable y, sin querer, más abajo la cambió por 30. Medio muelle pagó diez veces de más.
              """,
              sugiere="Lo que no tiene que cambiar nunca se declara con `const TARIFA = 3;` y se usa sin `$`: `TARIFA`. Si alguien intenta cambiarla, PHP no lo deja.",
              desafio="Convertí la tarifa en una constante y borrá la línea que la pisa.",
              inicial='''
                  <?php
                  $tarifa = 3;
                  $kilos = 12;
                  $tarifa = 30;
                  echo "Kilos: $kilos\\n";
                  echo "A pagar: " . ($kilos * $tarifa) . " sellos\\n";
              ''',
              solucion='''
                  <?php
                  const TARIFA = 3;
                  $kilos = 12;
                  echo "Kilos: $kilos\\n";
                  echo "A pagar: " . ($kilos * TARIFA) . " sellos\\n";
              ''',
              al_superar="Elefa sella la tarifa en el pizarrón de la entrada. —Lo que no cambia, se escribe una vez y se respeta —dice—. Como mi nombre. ¿Cómo me llamo? —Nilo no contesta.",
              imagen=["Un pizarrón grande en la entrada de un muelle, con un sello de lacre violeta en una esquina y un dibujo de una balanza, sin letras.",
                      ELEFA + " apoya el bastón en el pizarrón.", NILO + " mira para otro lado.", GHECO + " sobre el pizarrón."]),
        ],
    },
    {
        "titulo": "R01-N02 · Operadores y expresiones",
        "misiones": [
            m(id="R01-N02-P1", titulo="Cajones por bodega",
              lugar=PESAJE, personajes="Nilo, Gheco",
              carta="Aritméticos | + - * / · % es el resto · ** es la potencia · intdiv(a, b) divide sin decimales",
              recompensa="xp 10, oro 10",
              escena="""
                  En la oficina de pesaje, Nilo tiene que repartir 47 cajones en bodegas de a 6. Quiere saber cuántas bodegas llena y cuántos cajones le sobran. Lo hace con los dedos y se le acaban.
              """,
              sugiere="`intdiv(47, 6)` da cuántas veces entra el 6 en el 47, sin decimales; `47 % 6` da **lo que sobra**.",
              desafio="Completá las dos cuentas.",
              inicial='''
                  <?php
                  $cajones = 47;
                  $porBodega = 6;
                  $llenas = ___;
                  $sobran = ___;
                  echo "Bodegas llenas: $llenas\\n";
                  echo "Sobran: $sobran cajones\\n";
              ''',
              solucion='''
                  <?php
                  $cajones = 47;
                  $porBodega = 6;
                  $llenas = intdiv($cajones, $porBodega);
                  $sobran = $cajones % $porBodega;
                  echo "Bodegas llenas: $llenas\\n";
                  echo "Sobran: $sobran cajones\\n";
              ''',
              al_superar="Siete bodegas llenas y cinco cajones sueltos, que Nilo apila en un rincón. Le sobran los diez dedos.",
              imagen=["Una oficina de pesaje con una balanza grande de dos platos y pilas de cajones de madera ordenadas en grupos.",
                      NILO + " cuenta cajones con los dedos.", GHECO + " sobre una pila de cajones."]),
            m(id="R01-N02-P2", titulo="Tres iguales",
              lugar=PESAJE, personajes="Nilo, Elefa, Gheco",
              criatura="ogro",
              carta="Comparar | === igual valor Y tipo · !== distinto · == compara suelto y miente · siempre ===",
              recompensa="xp 10, oro 10",
              escena="""
                  Nilo entrega la carta del casillero «01» al señor del casillero 1. —Es lo mismo, ¿no? —dice, y compara con `==`. Abajo del muelle, un **ogro** se ríe. Elefa suspira: —Tres iguales, Nilo.
              """,
              sugiere="`==` convierte antes de comparar: para él \"01\" y \"1\" son iguales. `===` exige el mismo valor **y** el mismo tipo.",
              desafio="Cambiá la comparación para que la carta no se entregue al casillero equivocado.",
              inicial='''
                  <?php
                  $casilleroCarta = "01";
                  $casilleroCliente = "1";
                  if ($casilleroCarta == $casilleroCliente) {
                      echo "Entregada\\n";
                  } else {
                      echo "No es este casillero\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $casilleroCarta = "01";
                  $casilleroCliente = "1";
                  if ($casilleroCarta === $casilleroCliente) {
                      echo "Entregada\\n";
                  } else {
                      echo "No es este casillero\\n";
                  }
              ''',
              al_superar="La carta vuelve al bolso de Nilo… y se cae por el agujero. Pero al menos no la entregó mal.",
              imagen=["Una pared de casilleros de madera con números pintados que son solo puntitos de colores, en una oficina de correos de noche.",
                      NILO + " duda con una carta en la mano frente a dos casilleros.", ELEFA + " lo mira de brazos cruzados.", "Un ogro asoma la cabeza riéndose por debajo del muelle."]),
            m(id="R01-N02-P3", titulo="Lo que falta, con ??",
              lugar=PESAJE, personajes="Nilo, Gheco",
              criatura="troll",
              carta="?? y ternario | $a ?? \"otro\" usa $a si existe y no es null · $cond ? \"sí\" : \"no\" elige entre dos",
              recompensa="xp 15, oro 15",
              escena="""
                  A la oficina llega un cajón sin remitente: el campo está en `null`. Nilo tiene que imprimir la etiqueta igual, y en lugar del nombre sale un hueco. Un **troll** se esconde detrás de lo que no está.
              """,
              sugiere="`$remitente ?? \"Desconocido\"` usa el remitente si hay uno, y si es `null`, el texto de reserva. Para elegir entre dos textos según una condición: `$frágil ? \"si\" : \"no\"`.",
              desafio="Completá la etiqueta con `??` y con el ternario.",
              inicial='''
                  <?php
                  $remitente = null;
                  $fragil = true;
                  $nombre = $remitente;
                  $cuidado = $fragil;
                  echo "Remitente: $nombre\\n";
                  echo "Fragil: $cuidado\\n";
              ''',
              solucion='''
                  <?php
                  $remitente = null;
                  $fragil = true;
                  $nombre = $remitente ?? "Desconocido";
                  $cuidado = $fragil ? "si" : "no";
                  echo "Remitente: $nombre\\n";
                  echo "Fragil: $cuidado\\n";
              ''',
              al_superar="La etiqueta sale completa. El troll, que vivía en el hueco, se queda sin casa.",
              imagen=["Un cajón de madera con una etiqueta lisa en blanco sobre una mesa de pesaje, de noche.",
                      "Un troll grande y verdoso se esconde detrás del cajón.", NILO + " escribe la etiqueta.", GHECO + " sobre la mesa."]),
            m(id="R01-N02-P4", titulo="¿Cuál pesa más?",
              lugar=PESAJE, personajes="Nilo, Gheco",
              carta="Nave espacial | $a <=> $b da -1 si a es menor, 0 si son iguales, 1 si a es mayor · sirve para ordenar",
              recompensa="xp 10, oro 10",
              escena="""
                  La balanza de dos platos compara dos bolsas y una aguja marca para qué lado se inclina. Nilo quiere que el programa diga lo mismo con un solo número: -1, 0 o 1.
              """,
              sugiere="El operador `<=>` (la nave espacial) compara y devuelve -1, 0 o 1.",
              desafio="Completá las tres comparaciones con `<=>`.",
              inicial='''
                  <?php
                  echo "8 contra 12: " . (8 - 12) . "\\n";
                  echo "12 contra 12: " . (12 - 12) . "\\n";
                  echo "15 contra 12: " . (15 - 12) . "\\n";
              ''',
              solucion='''
                  <?php
                  echo "8 contra 12: " . (8 <=> 12) . "\\n";
                  echo "12 contra 12: " . (12 <=> 12) . "\\n";
                  echo "15 contra 12: " . (15 <=> 12) . "\\n";
              ''',
              al_superar="La aguja de la balanza y el programa dicen lo mismo. Nilo le pone nombre a la balanza: *Nave*.",
              imagen=["Una balanza antigua de dos platos de bronce con una aguja en el medio, con una bolsa en cada plato, en una oficina de pesaje.",
                      NILO + " compara las bolsas inclinado sobre la balanza.", GHECO + " colgado de la aguja."]),
        ],
    },
    {
        "titulo": "R01-N03 · Textos: comillas, funciones y formato",
        "misiones": [
            m(id="R01-N03-P1", titulo="La escribiente",
              lugar=CASILLEROS, personajes="Nilo, Iara, Gheco",
              carta="Limpiar textos | trim() saca espacios de las puntas · strtoupper() MAYÚSCULAS · ucfirst() la primera · ucwords() cada palabra",
              recompensa="xp 10, oro 10",
              escena="""
                  En los casilleros del correo, una chica de chaleco azul petróleo y lápiz detrás de la oreja limpia las direcciones que copió Nilo. Se llama **Iara** y es la escribiente de la Oficina. —¿Lo anotaste? —le pregunta. —Lo tengo acá —dice Nilo, tocándose la cabeza.
              """,
              sugiere="`trim($x)` saca los espacios de las puntas y `ucwords($x)` pone en mayúscula la primera letra de cada palabra. Se pueden combinar: `ucwords(trim($x))`.",
              desafio="Limpiá la dirección para que quede prolija.",
              inicial='''
                  <?php
                  $direccion = "   muelle tres, casillero doce   ";
                  echo "[" . $direccion . "]\\n";
              ''',
              solucion='''
                  <?php
                  $direccion = "   muelle tres, casillero doce   ";
                  echo "[" . ucwords(trim($direccion)) . "]\\n";
              ''',
              al_superar="Iara mira la dirección, después a Nilo, y anota algo en su libreta. Nilo no sabe si es un elogio.",
              imagen=["Una pared entera de casilleros de madera con sobres, en una oficina de correos con lámparas violetas.",
                      IARA + " limpia una etiqueta con el lápiz.", NILO + " le muestra un sobre.", GHECO + " sobre un casillero."]),
            m(id="R01-N03-P2", titulo="Comillas que hablan",
              lugar=CASILLEROS, personajes="Nilo, Iara, Gheco",
              carta="Comillas | \"…\" reemplaza $variables y \\n · '…' muestra todo tal cual · para mezclar, el punto .",
              recompensa="xp 10, oro 10",
              escena="""
                  Nilo escribió la etiqueta con comillas simples y salió literalmente `$destino` en lugar del destino. Iara levanta una ceja.
              """,
              sugiere="Dentro de comillas **dobles**, PHP reemplaza `$destino` por su valor y entiende `\\n`. En comillas **simples**, todo sale tal cual.",
              desafio="Arreglá la etiqueta para que muestre el destino y el salto de línea.",
              inicial='''
                  <?php
                  $destino = "Valle de la Serpiente";
                  echo 'Destino: $destino\\n';
              ''',
              solucion='''
                  <?php
                  $destino = "Valle de la Serpiente";
                  echo "Destino: $destino\\n";
              ''',
              al_superar="—Comillas dobles cuando hay algo adentro —anota Iara en voz alta. Esta vez Nilo también lo anota. En la mano.",
              imagen=["Una mesa de escribiente con sobres, sellos de lacre violeta y un tintero, en una oficina de correos.",
                      IARA + " señala un sobre con el lápiz.", NILO + " escribe en la palma de su mano.", GHECO + " sobre el tintero."]),
            m(id="R01-N03-P3", titulo="Letras con tilde",
              lugar=CASILLEROS, personajes="Nilo, Iara, Gheco",
              carta="mb_* | strlen cuenta bytes: una ñ o una tilde ocupan 2 · mb_strlen cuenta letras · mb_strtoupper con tildes",
              recompensa="xp 15, oro 15",
              escena="""
                  Las etiquetas de los casilleros tienen lugar para 10 letras. «Ñandú» entra de sobra, pero el programa de Nilo dice que tiene 7. Iara lo cuenta con el dedo: cinco.
              """,
              sugiere="`strlen` cuenta **bytes**, y en UTF-8 una letra con tilde o una ñ ocupa dos. `mb_strlen` cuenta letras de verdad. Lo mismo `mb_strtoupper` para las mayúsculas.",
              desafio="Usá las funciones `mb_` para contar y pasar a mayúsculas.",
              inicial='''
                  <?php
                  $nombre = "ñandú";
                  echo "Letras: " . strlen($nombre) . "\\n";
                  echo "Etiqueta: " . strtoupper($nombre) . "\\n";
              ''',
              solucion='''
                  <?php
                  $nombre = "ñandú";
                  echo "Letras: " . mb_strlen($nombre) . "\\n";
                  echo "Etiqueta: " . mb_strtoupper($nombre) . "\\n";
              ''',
              al_superar="Cinco letras, todas en mayúscula, con su tilde. Iara se guarda la cuenta en la libreta para cuando llegue el próximo «Ñandú».",
              imagen=["Una fila de etiquetas de casilleros, lisas, con dibujitos de un ñandú, en una oficina de correos.",
                      IARA + " cuenta con el dedo sobre la etiqueta.", NILO + " cuenta con los dedos y no le da.", GHECO + " sobre un casillero."]),
            m(id="R01-N03-P4", titulo="El recibo prolijo",
              lugar=CASILLEROS, personajes="Nilo, Iara, Gheco",
              carta="Formato | printf(\"%.2f\", $x) dos decimales · %d entero · %s texto · number_format($x, 2, ',', '.') estilo argentino",
              recompensa="xp 15, oro 15",
              escena="""
                  Iara le pide a Nilo un recibo por un envío de 1234.5 sellos. Nilo escribe «1234.5». —Con dos decimales y los miles separados —dice Iara—. Como se escribe acá: 1.234,50.
              """,
              sugiere="`number_format($monto, 2, ',', '.')` da dos decimales con coma y los miles con punto. `printf(\"%d\", $x)` muestra un entero.",
              desafio="Completá el recibo con el formato argentino.",
              inicial='''
                  <?php
                  $envios = 3;
                  $monto = 1234.5;
                  echo "Envios: $envios\\n";
                  echo "Total: $monto sellos\\n";
              ''',
              solucion='''
                  <?php
                  $envios = 3;
                  $monto = 1234.5;
                  printf("Envios: %d\\n", $envios);
                  echo "Total: " . number_format($monto, 2, ',', '.') . " sellos\\n";
              ''',
              al_superar="Iara firma el recibo y lo guarda en el casillero que corresponde. Nilo, por primera vez, ve que su trabajo queda guardado en algún lado.",
              imagen=["Un recibo de papel con un sello de lacre violeta, sin letras, sobre un mostrador de correos.",
                      IARA + " firma el recibo con el lápiz.", NILO + " sonríe orgulloso.", GHECO + " sobre el sello."]),
        ],
    },
    {
        "titulo": "R01-N04 · Entrada por teclado y argumentos",
        "misiones": [
            m(id="R01-N04-P1", titulo="La ventanilla pregunta",
              lugar=ENCOMIENDAS, personajes="Nilo, Gheco",
              carta="Leer un renglón | $x = trim(fgets(STDIN)); · fgets lee hasta el Enter · trim saca el salto de línea",
              recompensa="xp 10, oro 10",
              escena="""
                  En la ventanilla de encomiendas, Nilo le pregunta a cada cliente su nombre. El cliente contesta, pero el programa saluda siempre al mismo: «Hola, cliente».
              """,
              sugiere="`fgets(STDIN)` lee un renglón de lo que escribe la persona (acá, la **Entrada** de la misión). Trae el Enter al final: `trim` lo saca.",
              desafio="Leé el nombre de la entrada y saludá a quien escribió.",
              inicial='''
                  <?php
                  $nombre = "cliente";
                  echo "Hola, $nombre. Pase.\\n";
              ''',
              entrada="Rosaura\n",
              solucion='''
                  <?php
                  $nombre = trim(fgets(STDIN));
                  echo "Hola, $nombre. Pase.\\n";
              ''',
              al_superar="Rosaura pasa, contenta de que la llamen por su nombre. Nilo ya se olvidó de cómo se llamaba, pero el programa no.",
              imagen=["Una ventanilla de encomiendas con un mostrador de madera, una balanza y paquetes atados con soga, de noche.",
                      NILO + " atiende detrás de la ventanilla.", "Una clienta anciana con un paquete del otro lado.", GHECO + " sobre la balanza."]),
            m(id="R01-N04-P2", titulo="Doce kilos",
              lugar=ENCOMIENDAS, personajes="Nilo, Gheco",
              criatura="slime",
              carta="Validar números | is_numeric($x) dice si es un número · si no, se avisa y no se calcula · lo que se lee siempre es texto",
              recompensa="xp 15, oro 15",
              escena="""
                  Un cliente contesta «doce kilos» en vez de «12». Nilo lo usa en la cuenta igual, la balanza intenta multiplicar «doce kilos» por la tarifa y del platillo empiezan a brotar **slimes**.
              """,
              sugiere="`is_numeric($peso)` devuelve `true` si el texto es un número. Si no lo es, se avisa y no se calcula nada.",
              desafio="Validá el peso antes de calcular: si no es un número, mostrá «Peso invalido: escribilo con numeros.».",
              inicial='''
                  <?php
                  $peso = trim(fgets(STDIN));
                  $total = $peso * 3;
                  echo "A pagar: $total sellos\\n";
              ''',
              entrada="doce kilos\n",
              solucion='''
                  <?php
                  $peso = trim(fgets(STDIN));
                  if (is_numeric($peso)) {
                      $total = $peso * 3;
                      echo "A pagar: $total sellos\\n";
                  } else {
                      echo "Peso invalido: escribilo con numeros.\\n";
                  }
              ''',
              al_superar="La balanza no explota. El cliente se pone colorado y escribe «12». Los slimes, sin comida, se secan.",
              imagen=["Una balanza de encomiendas de la que brotan gotas de slime verde, sobre un mostrador.",
                      NILO + " tapa la balanza con las dos manos.", "Varios slimes verdes chiquitos saltando del platillo.", GHECO + " encima de un paquete."]),
            m(id="R01-N04-P3", titulo="Tres datos en un renglón",
              lugar=ENCOMIENDAS, personajes="Nilo, Iara, Gheco",
              carta="explode | explode(\",\", \"a,b,c\") da [\"a\", \"b\", \"c\"] · [$x, $y] = explode(...) los reparte en variables",
              recompensa="xp 15, oro 15",
              escena="""
                  Iara manda los pedidos en un solo renglón, separados por comas: nombre, destino y kilos. Nilo los lee enteros y no sabe dónde termina cada uno. —Se cortan por la coma —dice Iara.
              """,
              sugiere="`explode(\",\", $renglon)` corta el texto en cada coma y devuelve una lista. `[$a, $b, $c] = …` reparte las partes en tres variables.",
              desafio="Separá el renglón en sus tres datos.",
              inicial='''
                  <?php
                  $renglon = trim(fgets(STDIN));
                  echo "Pedido: $renglon\\n";
              ''',
              entrada="Olmo,Forjas,8\n",
              solucion='''
                  <?php
                  $renglon = trim(fgets(STDIN));
                  [$nombre, $destino, $kilos] = explode(",", $renglon);
                  echo "Cliente: $nombre\\n";
                  echo "Destino: $destino\\n";
                  echo "Kilos: $kilos\\n";
              ''',
              al_superar="Cada dato en su lugar. Iara asiente apenas; para ella, es un festejo.",
              imagen=["Una tira larga de papel con tres sellos de colores separados por cortes, sobre un mostrador.",
                      IARA + " corta la tira con una tijera.", NILO + " sostiene la otra punta.", GHECO + " sobre la tijera."]),
            m(id="R01-N04-P4", titulo="Dos números en un renglón",
              lugar=ENCOMIENDAS, personajes="Nilo, Gheco",
              carta="Convertir | (float) \"4.5\" da 4.5 · (int) \"3\" da 3 · se convierte después de cortar con explode",
              recompensa="xp 10, oro 10",
              escena="""
                  Un paquete mide 4.5 por 2 metros, y el cliente lo escribió en un solo renglón con un espacio en el medio. Nilo calcula la superficie y le da 0.
              """,
              sugiere="Cortá con `explode(\" \", …)` y convertí cada parte con `(float)` antes de multiplicar.",
              desafio="Calculá la superficie del paquete.",
              inicial='''
                  <?php
                  $renglon = trim(fgets(STDIN));
                  $superficie = 0;
                  echo "Superficie: $superficie m2\\n";
              ''',
              entrada="4.5 2\n",
              solucion='''
                  <?php
                  $renglon = trim(fgets(STDIN));
                  [$ancho, $alto] = explode(" ", $renglon);
                  $superficie = (float) $ancho * (float) $alto;
                  echo "Superficie: $superficie m2\\n";
              ''',
              al_superar="Nueve metros cuadrados: el paquete va en la bodega grande. Nilo lo lleva corriendo, silbando.",
              imagen=["Un paquete enorme y plano envuelto en papel madera, apoyado contra una pared en una ventanilla de encomiendas.",
                      NILO + " lo mide con los brazos abiertos.", GHECO + " sobre el paquete."]),
        ],
    },
    {
        "titulo": "R01-N05 · Decisiones: if, switch y match",
        "misiones": [
            m(id="R01-N05-P1", titulo="El farol del cruce",
              lugar=CRUCE, personajes="Nilo, Gheco",
              carta="if | if (cond) { … } elseif (otra) { … } else { … } · se prueba en orden y se hace solo el primero que se cumple",
              recompensa="xp 10, oro 10",
              escena="""
                  El guardia del cruce se fue a almorzar y le dejó el farol a Nilo. A cada carro le tiene que señalar un camino: el pescado a la izquierda, la madera al frente y las cartas a la torre. El primer carro de pescado sube derecho a la torre.
              """,
              sugiere="Con `if`, `elseif` y `else` se elige un camino según la carga. Se prueban en orden.",
              desafio="Completá las decisiones para que cada carga vaya a su camino.",
              inicial='''
                  <?php
                  $carga = trim(fgets(STDIN));
                  echo "A la torre\\n";
              ''',
              entrada="pescado\n",
              solucion='''
                  <?php
                  $carga = trim(fgets(STDIN));
                  if ($carga === "pescado") {
                      echo "A la izquierda\\n";
                  } elseif ($carga === "madera") {
                      echo "Al frente\\n";
                  } else {
                      echo "A la torre\\n";
                  }
              ''',
              al_superar="El carro de pescado dobla a la izquierda. La Oficina de Correos se salva del olor a merluza. Por ahora.",
              imagen=["Un cruce de tres muelles de madera de noche, con un farol de bronce en el medio y un carro cargado de pescado.",
                      NILO + " levanta el farol y señala a la izquierda.", GHECO + " sobre el farol."]),
            m(id="R01-N05-P2", titulo="La guardia en la puerta",
              lugar=CRUCE, personajes="Nilo, Gheco",
              carta="Cláusula de guarda | primero se descarta lo inválido · después, con el dato sano, se calcula · menos llaves anidadas",
              recompensa="xp 15, oro 15",
              escena="""
                  Al cruce llegan carros con pesos imposibles: negativos, cero, de diez mil kilos. Nilo los deja pasar a todos y la grúa se queja. Gheco le enseña el truco de la guardia: frenar lo malo en la puerta.
              """,
              sugiere="Primero los casos inválidos, cada uno con su mensaje. Si el peso es menor o igual a 0, o mayor a 1000, se avisa y no se sigue.",
              desafio="Agregá la guardia: «Peso imposible.» si el peso es menor o igual a 0 o mayor a 1000.",
              inicial='''
                  <?php
                  $peso = (float) trim(fgets(STDIN));
                  echo "Carro aceptado: $peso kg\\n";
              ''',
              entrada="-40\n",
              solucion='''
                  <?php
                  $peso = (float) trim(fgets(STDIN));
                  if ($peso <= 0 || $peso > 1000) {
                      echo "Peso imposible.\\n";
                  } else {
                      echo "Carro aceptado: $peso kg\\n";
                  }
              ''',
              al_superar="El carro de -40 kilos se da vuelta y se va por donde vino. La grúa deja de quejarse.",
              imagen=["Un cruce de muelles con una barrera de madera baja y un carro frenado delante.",
                      NILO + " baja la barrera con el farol en la otra mano.", GHECO + " sobre la barrera."]),
            m(id="R01-N05-P3", titulo="match, la forma moderna",
              lugar=CRUCE, personajes="Nilo, Elefa, Gheco",
              carta="match | $x = match ($dia) { 'lunes', 'martes' => 'abierto', default => 'cerrado' }; · compara con === · devuelve un valor",
              recompensa="xp 15, oro 15",
              escena="""
                  Elefa le pasa a Nilo la tabla de las dársenas: cada tipo de barco amarra en una distinta. Nilo la escribió con un `if` larguísimo que se le enreda. —Para elegir un valor según otro, está `match` —dice la Capitana.
              """,
              sugiere="`match` compara con `===` y devuelve el valor del primer caso que coincide. Si ninguno coincide, `default`.",
              desafio="Completá el `match` para cada barco: velero y bote a la dársena 1, remolcador a la 2, carguero a la 3 y cualquier otro a «revision».",
              inicial='''
                  <?php
                  $barco = trim(fgets(STDIN));
                  $darsena = match ($barco) {
                      default => "revision",
                  };
                  echo "Darsena: $darsena\\n";
              ''',
              entrada="remolcador\n",
              solucion='''
                  <?php
                  $barco = trim(fgets(STDIN));
                  $darsena = match ($barco) {
                      "velero", "bote" => "1",
                      "remolcador" => "2",
                      "carguero" => "3",
                      default => "revision",
                  };
                  echo "Darsena: $darsena\\n";
              ''',
              al_superar="El remolcador amarra donde tiene que amarrar. Elefa asiente con la trompa.",
              imagen=["Un puerto de noche con tres dársenas marcadas con banderines de colores lisos y un remolcador entrando.",
                      ELEFA + " señala una dársena con el bastón.", NILO + " sostiene el farol.", GHECO + " sobre un poste del muelle."]),
            m(id="R01-N05-P4", titulo="El carro raro",
              lugar=CRUCE, personajes="Nilo, Gheco",
              criatura="ogro",
              carta="switch | compara con == (suelto) · cada case termina con break · sin break, sigue al siguiente · para lo nuevo, mejor match",
              recompensa="xp 10, oro 10",
              escena="""
                  Un carro dice que su carga es «0». El `switch` de Nilo lo manda con el pescado, y el **ogro** del cruce se ríe a carcajadas: algo anda mal y nadie avisa.
              """,
              sugiere="Al `switch` le falta un `break` al final del primer caso: sin él, sigue de largo y ejecuta también el caso de abajo.",
              desafio="Agregá los `break` que faltan para que cada caso haga solo lo suyo.",
              inicial='''
                  <?php
                  $tipo = "madera";
                  switch ($tipo) {
                      case "madera":
                          echo "Al frente\\n";
                      case "pescado":
                          echo "A la izquierda\\n";
                      default:
                          echo "A la torre\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $tipo = "madera";
                  switch ($tipo) {
                      case "madera":
                          echo "Al frente\\n";
                          break;
                      case "pescado":
                          echo "A la izquierda\\n";
                          break;
                      default:
                          echo "A la torre\\n";
                  }
              ''',
              al_superar="El carro de madera sigue al frente, sin desviarse. El ogro deja de reírse y se va a buscar otro cruce.",
              imagen=["Un cruce de muelles con tres caminos y un carro de madera que intenta ir por los tres a la vez.",
                      "Un ogro grande riéndose apoyado en un poste.", NILO + " tira del caballo del carro.", GHECO + " sobre el farol."]),
        ],
    },
]
