from genphp import m
from php_r01 import NILO, ELEFA, IARA, PICO, GHECO

CALLE = "La calle de las vidrieras"
FERRETERIA = "La vidriera de la ferretería"
VELAS = "La tienda de las velas"
CRUCEROS = "La temporada de cruceros"
REFLEJOS = "Los reflejos de las vidrieras"
BASTION = "El Bastión de Laravel"
SOTANO_B = "El sótano del Bastión"
TORRE_B = "La torre del Bastión"
FERMIN = "Fermín (anciano bajo y encorvado, barba blanca larga, anteojos redondos de bronce, guardapolvo gris, gorro de lana, farol cian)"
HIPOCAMPO = "el Hipocampo de las Vidrieras (caballito de mar del tamaño de un caballo, hecho de vidrio de colores rojo, ámbar, azul y verde unidos con plomo como un vitral)"
GRIFO = "el Grifo de los Registros (grifo de cabeza y alas de águila blancas y cuerpo de león dorado, con un monóculo de bronce y páginas en blanco entre las plumas)"
ARMA = "PHP arma el HTML que recibe el navegador: acá lo armás con `echo` y lo ves como texto."
IMITA = "En el navegador no hay Laravel: acá armamos la misma idea con PHP puro. En tu compu, las misiones usan Laravel de verdad."

NODOS = [
    {
        "titulo": "S04-N01 · HTML: la estructura de una página",
        "misiones": [
            m(id="S04-N01-P1", titulo="La vidriera tirada",
              lugar=CALLE, personajes="Nilo, Gheco",
              carta="Esqueleto | <!DOCTYPE html> · <html lang=\"es\"> · <head> con <meta charset> y <title> · <body> con lo que se ve",
              recompensa="xp 10, oro 10",
              escena="""
                  Frente al Muelle hay una calle de tiendas: el **Escaparate del Puerto**. Algunas vidrieras están tan bien armadas que la gente se para a mirar; otras son un montón de cosas tiradas, sin cartel, con la puerta escondida. Nilo entra a una buscando la puerta y sale por la ventana.
              """,
              sugiere="Toda página empieza igual: `<!DOCTYPE html>`, `<html lang=\"es\">`, un `<head>` con el `charset` y el `title`, y el `<body>`. " + ARMA,
              desafio="Completá el esqueleto de la página.",
              inicial='''
                  <?php
                  $titulo = 'Ferreteria del Puerto';
                  echo "<h1>$titulo</h1>\\n";
              ''',
              solucion='''
                  <?php
                  $titulo = 'Ferreteria del Puerto';
                  echo "<!DOCTYPE html>\\n";
                  echo "<html lang=\\"es\\">\\n";
                  echo "<head>\\n<meta charset=\\"utf-8\\">\\n<title>$titulo</title>\\n</head>\\n";
                  echo "<body>\\n<h1>$titulo</h1>\\n</body>\\n";
                  echo "</html>\\n";
              ''',
              al_superar="La vidriera ya tiene marco, cartel y puerta. Nilo entra por la puerta, esta vez.",
              imagen=["Una calle de tiendas del puerto de noche con vidrieras de marcos de madera iluminadas, unas ordenadas y otras desordenadas.",
                      NILO + " saliendo por la ventana de una vidriera desordenada.", GHECO + " sobre un marco."]),
            m(id="S04-N01-P2", titulo="Etiquetas con significado",
              lugar=CALLE, personajes="Nilo, Iara, Gheco",
              carta="Semántica | header · nav · main · article · footer · cada parte dice qué es, no solo cómo se ve · un solo h1 por página",
              recompensa="xp 15, oro 15",
              escena="""
                  La vidriera de la ferretería tiene todo metido en `<div>`: el cartel, el menú, los productos y el pie. Iara dice que así no se sabe qué es cada cosa.
              """,
              sugiere="Cada parte con su etiqueta: `<header>` el cartel, `<nav>` el menú, `<main>` lo principal y `<footer>` el pie.",
              desafio="Cambiá los `div` por las etiquetas con significado.",
              inicial='''
                  <?php
                  $partes = ['cartel' => 'Ferreteria', 'menu' => 'Inicio | Ofertas', 'principal' => 'Tornillos y cadenas', 'pie' => 'Muelle 3'];
                  foreach ($partes as $parte => $contenido) {
                      echo "<div>$contenido</div>\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $partes = ['cartel' => 'Ferreteria', 'menu' => 'Inicio | Ofertas', 'principal' => 'Tornillos y cadenas', 'pie' => 'Muelle 3'];
                  $etiquetas = ['cartel' => 'header', 'menu' => 'nav', 'principal' => 'main', 'pie' => 'footer'];
                  foreach ($partes as $parte => $contenido) {
                      $e = $etiquetas[$parte];
                      echo "<$e>$contenido</$e>\\n";
                  }
              ''',
              al_superar="Cada parte dice qué es. Iara ordena su escritorio con el mismo criterio. Nilo, no.",
              imagen=["Una vidriera de ferretería dividida en cuatro partes claras: un cartel arriba, un menú, los productos y un pie con el número del muelle.",
                      IARA + " señala cada parte.", NILO + " con un tornillo en la mano.", GHECO + " sobre el cartel."]),
            m(id="S04-N01-P3", titulo="La foto sin descripción",
              lugar=CALLE, personajes="Nilo, Gheco",
              criatura="esqueleto",
              carta="Enlaces e imágenes | <a href=\"ruta\">texto</a> · <img src=\"ruta\" alt=\"descripción\"> · rutas relativas · el alt lo leen quienes no ven la imagen",
              recompensa="xp 15, oro 15",
              escena="""
                  Las fotos de la vidriera no tienen descripción. Una clienta que no ve escucha a su lector de pantalla decir «imagen, imagen, imagen». Un **esqueleto** —un nombre sin cuerpo— se ríe desde el estante.
              """,
              sugiere="Cada `<img>` lleva su `alt` con lo que muestra. Armalas con un `foreach` sobre los productos, escapando el texto.",
              desafio="Armá las imágenes con su `alt`.",
              inicial='''
                  <?php
                  $productos = ['tornillo.png' => 'Caja de tornillos de bronce', 'cadena.png' => 'Rollo de cadena de 5 metros'];
                  foreach ($productos as $archivo => $descripcion) {
                      echo "<img src=\\"img/$archivo\\">\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $productos = ['tornillo.png' => 'Caja de tornillos de bronce', 'cadena.png' => 'Rollo de cadena de 5 metros'];
                  foreach ($productos as $archivo => $descripcion) {
                      echo "<img src=\\"img/$archivo\\" alt=\\"" . htmlspecialchars($descripcion) . "\\">\\n";
                  }
              ''',
              al_superar="El lector de pantalla dice «caja de tornillos de bronce». La clienta compra dos. El esqueleto se calla.",
              imagen=["Una vidriera con dos fotos enmarcadas de productos, cada una con una plaquita lisa debajo.",
                      NILO + " pega una plaquita.", "Un esqueleto chiquito en un estante.", GHECO + " sobre un marco."]),
        ],
    },
    {
        "titulo": "S04-N02 · Listas, tablas y formularios",
        "misiones": [
            m(id="S04-N02-P1", titulo="La tabla de precios",
              lugar=FERRETERIA, personajes="Nilo, Gheco",
              carta="Tablas | <table> · <thead> con <th scope=\"col\"> · <tbody> con las filas · <tfoot> para el total",
              recompensa="xp 10, oro 10",
              escena="""
                  En la vidriera de la ferretería todo está en orden: una tabla de precios con su encabezado. La de Nilo tiene los títulos de las columnas mezclados con los datos.
              """,
              sugiere="Los títulos van en `<thead>` con `<th scope=\"col\">`, los productos en `<tbody>` y el total en `<tfoot>`.",
              desafio="Armá la tabla con sus tres partes.",
              inicial='''
                  <?php
                  $precios = ['tornillo' => 2, 'cadena' => 15];
                  echo "<table>\\n";
                  foreach ($precios as $p => $precio) {
                      echo "<tr><td>$p</td><td>$precio</td></tr>\\n";
                  }
                  echo "</table>\\n";
              ''',
              solucion='''
                  <?php
                  $precios = ['tornillo' => 2, 'cadena' => 15];
                  echo "<table>\\n";
                  echo "<thead><tr><th scope=\\"col\\">Producto</th><th scope=\\"col\\">Precio</th></tr></thead>\\n";
                  echo "<tbody>\\n";
                  foreach ($precios as $p => $precio) {
                      echo "<tr><td>$p</td><td>$precio</td></tr>\\n";
                  }
                  echo "</tbody>\\n";
                  echo "<tfoot><tr><td>Total</td><td>" . array_sum($precios) . "</td></tr></tfoot>\\n";
                  echo "</table>\\n";
              ''',
              al_superar="La tabla se lee de un vistazo, con su encabezado y su total. El dueño dice que vende el doble.",
              imagen=["Una tabla de precios pintada en un cartel de madera con una fila de títulos más oscura arriba y una de total abajo, sin letras.",
                      NILO + " cuelga el cartel en la vidriera.", GHECO + " sobre el cartel."]),
            m(id="S04-N02-P2", titulo="La etiqueta de cada campo",
              lugar=FERRETERIA, personajes="Nilo, Iara, Gheco",
              carta="Formularios accesibles | <label for=\"id\"> y <input id=\"id\" name=\"…\"> · el name es lo que llega a PHP · required, type=\"number\", min",
              recompensa="xp 15, oro 15",
              escena="""
                  En la puerta de la ferretería hay un formulario para encargar lo que falta. Los campos no tienen etiquetas: nadie sabe qué va en cada uno, y a la Oficina de Correos los encargos llegan sin `name`, vacíos.
              """,
              sugiere="Cada campo con su `<label for>` y su `id` igual, y un `name` para que llegue a `$_POST`.",
              desafio="Armá los campos con su etiqueta, su id y su name.",
              inicial='''
                  <?php
                  $campos = ['producto' => 'Que necesitas', 'cantidad' => 'Cuantos'];
                  foreach ($campos as $nombre => $texto) {
                      echo "<input>\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $campos = ['producto' => 'Que necesitas', 'cantidad' => 'Cuantos'];
                  foreach ($campos as $nombre => $texto) {
                      $tipo = $nombre === 'cantidad' ? 'number' : 'text';
                      echo "<label for=\\"$nombre\\">$texto</label>\\n";
                      echo "<input id=\\"$nombre\\" name=\\"$nombre\\" type=\\"$tipo\\" required>\\n";
                  }
              ''',
              al_superar="Los encargos llegan completos a la Oficina. Iara le pide el formulario para copiarlo.",
              imagen=["Un formulario de papel en la puerta de la ferretería con dos casilleros, cada uno con su etiqueta de madera al lado.",
                      IARA + " copia el formulario en su libreta.", NILO + " sostiene la puerta.", GHECO + " sobre el formulario."]),
            m(id="S04-N02-P3", titulo="Listas dentro de listas",
              lugar=FERRETERIA, personajes="Nilo, Gheco",
              carta="Listas | <ul> sin orden · <ol> con orden · una lista dentro de un <li> para las categorías · se arma con dos foreach",
              recompensa="xp 15, oro 15",
              escena="""
                  La ferretería tiene categorías y, dentro de cada una, productos. Nilo los puso todos en una sola lista larga y nadie encuentra los clavos.
              """,
              sugiere="Un `<ul>` con un `<li>` por categoría, y adentro de cada `<li>` otro `<ul>` con sus productos.",
              desafio="Armá la lista anidada.",
              inicial='''
                  <?php
                  $catalogo = ['Herrajes' => ['tornillos', 'clavos'], 'Sogas' => ['cadena', 'cabo']];
                  echo "<ul>\\n";
                  foreach ($catalogo as $categoria => $productos) {
                      foreach ($productos as $p) {
                          echo "<li>$p</li>\\n";
                      }
                  }
                  echo "</ul>\\n";
              ''',
              solucion='''
                  <?php
                  $catalogo = ['Herrajes' => ['tornillos', 'clavos'], 'Sogas' => ['cadena', 'cabo']];
                  echo "<ul>\\n";
                  foreach ($catalogo as $categoria => $productos) {
                      echo "<li>$categoria\\n<ul>\\n";
                      foreach ($productos as $p) {
                          echo "<li>$p</li>\\n";
                      }
                      echo "</ul>\\n</li>\\n";
                  }
                  echo "</ul>\\n";
              ''',
              al_superar="Los clavos aparecen en Herrajes, donde tenían que estar. Un cliente que buscaba desde hace una hora se va feliz.",
              imagen=["Estantes de la ferretería con cajones agrupados por categoría, cada grupo con un cartel de madera liso arriba.",
                      NILO + " pone un cajón en su grupo.", GHECO + " sobre un cartel."]),
        ],
    },
    {
        "titulo": "S04-N03 · CSS: selectores, colores y cajas",
        "misiones": [
            m(id="S04-N03-P1", titulo="El letrero rojo",
              lugar=VELAS, personajes="Nilo, Gheco",
              carta="Reglas CSS | selector { propiedad: valor; } · las variables: :root { --rojo: #c0392b; } · color: var(--rojo) · se cambia en un solo lugar",
              recompensa="xp 10, oro 10",
              escena="""
                  En la tienda de las velas, un letrero rojo con letras claras hace que todos entren. Nilo quiere el mismo rojo en el letrero, los botones y los bordes, y lo escribió tres veces, cada una un poco distinta.
              """,
              sugiere="Una variable CSS en `:root` y las reglas la usan con `var(--rojo)`. Armá la hoja con PHP desde un array.",
              desafio="Generá la hoja de estilos usando la variable en las tres reglas.",
              inicial='''
                  <?php
                  echo ".letrero { color: #c0392b; }\\n";
                  echo ".boton { background: #c03a2b; }\\n";
                  echo ".marco { border-color: #b0392b; }\\n";
              ''',
              solucion='''
                  <?php
                  $rojo = '#c0392b';
                  echo ":root { --rojo: $rojo; }\\n";
                  $reglas = ['.letrero' => 'color', '.boton' => 'background', '.marco' => 'border-color'];
                  foreach ($reglas as $selector => $propiedad) {
                      echo "$selector { $propiedad: var(--rojo); }\\n";
                  }
              ''',
              al_superar="Un solo rojo, en un solo lugar. El día que cambie, cambia en toda la tienda.",
              imagen=["La vidriera de una tienda de velas con un letrero rojo brillante con un dibujo de una vela, y botones y marcos del mismo rojo.",
                      NILO + " pinta un marco con el mismo rojo.", GHECO + " sobre el letrero."]),
            m(id="S04-N03-P2", titulo="¿Qué regla gana?",
              lugar=VELAS, personajes="Nilo, Iara, Gheco",
              carta="Especificidad | id vale más que clase, clase más que etiqueta · (ids, clases, etiquetas) se comparan en orden · si empatan, gana la última",
              recompensa="xp 15, oro 15",
              escena="""
                  Nilo pintó el letrero de violeta con una regla, pero sigue rojo. Hay otra regla más «específica» que gana. Iara anota cuánto vale cada selector.
              """,
              sugiere="Contá ids (`#`), clases (`.`) y etiquetas de cada selector. Se compara primero ids, después clases, después etiquetas: `[ids, clases, etiquetas] <=> […]`.",
              desafio="Calculá la especificidad y decí qué regla gana.",
              inicial='''
                  <?php
                  function especificidad(string $selector): array
                  {
                      return [0, 0, 0];
                  }

                  $reglas = ['h1' => 'violeta', '.tienda h1' => 'rojo', 'h1.letrero' => 'azul'];
                  foreach ($reglas as $s => $color) {
                      echo "$s: " . implode(',', especificidad($s)) . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function especificidad(string $selector): array
                  {
                      $ids = substr_count($selector, '#');
                      $clases = substr_count($selector, '.');
                      $etiquetas = 0;
                      foreach (preg_split('/\\s+/', trim($selector)) as $parte) {
                          if (preg_match('/^[a-z]/', $parte)) {
                              $etiquetas++;
                          }
                      }
                      return [$ids, $clases, $etiquetas];
                  }

                  $reglas = ['h1' => 'violeta', '.tienda h1' => 'rojo', 'h1.letrero' => 'azul'];
                  $ganadora = null;
                  foreach ($reglas as $s => $color) {
                      $e = especificidad($s);
                      echo "$s: " . implode(',', $e) . "\\n";
                      if ($ganadora === null || $e >= especificidad($ganadora)) {
                          $ganadora = $s;
                      }
                  }
                  echo "Gana: $ganadora ({$reglas[$ganadora]})\\n";
              ''',
              al_superar="Empatan dos, y gana la última: el letrero queda azul. Nilo quería violeta. Iara le muestra cómo ganar sin pelear.",
              imagen=["Tres pinceles con pintura violeta, roja y azul apoyados frente a un letrero, uno de ellos brillando.",
                      IARA + " anota números en la libreta.", NILO + " con el pincel violeta, frustrado.", GHECO + " sobre el pincel azul."]),
            m(id="S04-N03-P3", titulo="La caja que se pasa",
              lugar=VELAS, personajes="Nilo, Gheco",
              criatura="orco",
              carta="Modelo de caja | ancho total = width + padding×2 + border×2 (con content-box) · box-sizing: border-box hace que width ya lo incluya todo",
              recompensa="xp 15, oro 15",
              escena="""
                  La vidriera mide 300 de ancho. Nilo puso una caja de 300 con relleno y borde, y se sale por el costado: un **orco** del desborde asoma del otro lado.
              """,
              sugiere="Con `content-box`, el ancho real es `width + 2×padding + 2×border`. Con `border-box`, es `width`.",
              desafio="Calculá el ancho real con los dos modos.",
              inicial='''
                  <?php
                  function anchoReal(int $width, int $padding, int $border, string $modo): int
                  {
                      return $width;
                  }

                  foreach (['content-box', 'border-box'] as $modo) {
                      $ancho = anchoReal(300, 20, 2, $modo);
                      echo "$modo: $ancho px" . ($ancho > 300 ? ' (se sale)' : '') . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function anchoReal(int $width, int $padding, int $border, string $modo): int
                  {
                      return $modo === 'border-box' ? $width : $width + 2 * $padding + 2 * $border;
                  }

                  foreach (['content-box', 'border-box'] as $modo) {
                      $ancho = anchoReal(300, 20, 2, $modo);
                      echo "$modo: $ancho px" . ($ancho > 300 ? ' (se sale)' : '') . "\\n";
                  }
              ''',
              al_superar="Con `border-box` la caja entra justo. El orco se queda del otro lado del vidrio.",
              imagen=["Una vidriera con una caja de madera que se sale por un costado del marco, y otra igual que entra justo.",
                      "Un orco asomado por el costado de la vidriera.", NILO + " empuja la caja para adentro.", GHECO + " sobre el marco."]),
        ],
    },
    {
        "titulo": "S04-N04 · Flexbox, grid y diseño adaptable",
        "misiones": [
            m(id="S04-N04-P1", titulo="Desde el celular",
              lugar=CRUCEROS, personajes="Nilo, Gheco",
              carta="Primero el celular | sin @media: una columna · @media (min-width: 700px) { … } agranda para pantallas anchas",
              recompensa="xp 10, oro 10",
              escena="""
                  Llega la temporada de cruceros y el Escaparate se llena de gente que mira las vidrieras desde el celular. Las tiendas que se ven bien en la pantalla grande se deforman: columnas aplastadas, textos cortados.
              """,
              sugiere="Una función `columnas($ancho)` que dé 1 en el celular y más en pantallas anchas, como lo haría una `@media` con `min-width`.",
              desafio="Decidí cuántas columnas mostrar según el ancho.",
              inicial='''
                  <?php
                  function columnas(int $ancho): int
                  {
                      return 4;
                  }

                  foreach ([360, 768, 1280] as $ancho) {
                      echo "$ancho px -> columnas: " . columnas($ancho) . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function columnas(int $ancho): int
                  {
                      if ($ancho >= 1000) {
                          return 4;
                      }
                      if ($ancho >= 700) {
                          return 2;
                      }
                      return 1;
                  }

                  foreach ([360, 768, 1280] as $ancho) {
                      echo "$ancho px -> columnas: " . columnas($ancho) . "\\n";
                  }
              ''',
              al_superar="En el celular, una columna cómoda; en la compu, cuatro. Los turistas compran sin entrecerrar los ojos.",
              imagen=["Turistas de un crucero mirando una vidriera a través de celulares que muestran la vidriera en una columna.",
                      NILO + " acomoda la vidriera en una sola fila vertical.", GHECO + " sobre un celular."]),
            m(id="S04-N04-P2", titulo="La grilla que se acomoda sola",
              lugar=CRUCEROS, personajes="Nilo, Iara, Gheco",
              carta="Grid automático | grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)) · entran tantas columnas de al menos 200 como quepan",
              recompensa="xp 15, oro 15",
              escena="""
                  Iara propone una grilla que no necesita preguntar el ancho: entran tantas columnas de al menos 200 como quepan. Nilo quiere saber cuántas son en cada pantalla, para creerle.
              """,
              sugiere="Con `auto-fill` y `minmax(200px, 1fr)` y un espacio entre columnas, entran `floor((ancho + espacio) / (200 + espacio))` columnas (al menos 1).",
              desafio="Calculá las columnas de la grilla y armá la regla CSS.",
              inicial='''
                  <?php
                  $minimo = 200;
                  $espacio = 16;
                  foreach ([360, 768, 1280] as $ancho) {
                      echo "$ancho px -> columnas: ?\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $minimo = 200;
                  $espacio = 16;
                  echo ".vidriera { display: grid; gap: {$espacio}px; grid-template-columns: repeat(auto-fill, minmax({$minimo}px, 1fr)); }\\n";
                  foreach ([360, 768, 1280] as $ancho) {
                      $columnas = max(1, intdiv($ancho + $espacio, $minimo + $espacio));
                      echo "$ancho px -> columnas: $columnas\\n";
                  }
              ''',
              al_superar="Una, tres y cinco columnas, sin escribir ni una `@media`. Nilo le cree a Iara. Como siempre.",
              imagen=["Una vidriera con productos en una grilla que se reacomoda en distintas cantidades de columnas en tres vidrios de distinto ancho.",
                      IARA + " señala los vidrios.", NILO + " cuenta las columnas.", GHECO + " sobre un producto."]),
            m(id="S04-N04-P3", titulo="La foto que se sale",
              lugar=CRUCEROS, personajes="Nilo, Gheco",
              criatura="orco",
              carta="Nada se sale | img { max-width: 100%; height: auto; } · los anchos fijos grandes rompen el celular · se usan %, rem y max-width",
              recompensa="xp 15, oro 15",
              escena="""
                  Una foto de 1200 de ancho rompe la vidriera en el celular: hay que mover la pantalla de costado para verla entera. Un **orco** del desborde asoma por el borde.
              """,
              sugiere="Con `max-width: 100%` la foto nunca es más ancha que su caja. Calculá el ancho que se ve: el menor entre la foto y la pantalla.",
              desafio="Calculá el ancho que se ve y armá la regla.",
              inicial='''
                  <?php
                  $foto = 1200;
                  foreach ([360, 1280] as $pantalla) {
                      echo "Pantalla $pantalla: la foto mide $foto px\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $foto = 1200;
                  echo "img { max-width: 100%; height: auto; }\\n";
                  foreach ([360, 1280] as $pantalla) {
                      $visible = min($foto, $pantalla);
                      echo "Pantalla $pantalla: la foto mide $visible px\\n";
                  }
              ''',
              al_superar="La foto se achica en el celular y en la compu se ve entera. El orco no encuentra un borde por donde asomarse.",
              imagen=["Un celular gigante en la vidriera mostrando una foto que entra justa en la pantalla.",
                      "Un orco intentando asomarse por el borde del celular.", NILO + " sostiene el celular.", GHECO + " sobre la foto."]),
        ],
    },
    {
        "titulo": "S04-N05 · Jefe del Escaparate: el Hipocampo de las Vidrieras",
        "misiones": [
            m(id="S04-N05-P1", titulo="Los enlaces rotos",
              lugar=REFLEJOS, personajes="Nilo, Gheco",
              criatura="dragon",
              carta="Revisar el sitio | cada enlace interno tiene que llevar a una página que existe · se buscan los href y se comparan con las páginas",
              recompensa="xp 15, oro 15",
              escena="""
                  Una mañana, todas las vidrieras amanecen revueltas: puertas que no llevan a ningún lado. En el reflejo de los vidrios se mueve el **Hipocampo de las Vidrieras**, que se alimenta de las páginas desordenadas.
              """,
              sugiere="Con `preg_match_all('/href=\"([^\"]+)\"/', $html, $m)` sacás los enlaces; los que no están en la lista de páginas están rotos.",
              desafio="Encontrá los enlaces rotos del menú.",
              inicial='''
                  <?php
                  $paginas = ['index.html', 'ofertas.html', 'contacto.html'];
                  $menu = '<a href="index.html">Inicio</a> <a href="ofertas.html">Ofertas</a> <a href="velas.html">Velas</a> <a href="contacto.htm">Contacto</a>';
                  echo "Enlaces rotos: 0\\n";
              ''',
              solucion='''
                  <?php
                  $paginas = ['index.html', 'ofertas.html', 'contacto.html'];
                  $menu = '<a href="index.html">Inicio</a> <a href="ofertas.html">Ofertas</a> <a href="velas.html">Velas</a> <a href="contacto.htm">Contacto</a>';
                  preg_match_all('/href="([^"]+)"/', $menu, $m);
                  $rotos = array_values(array_diff($m[1], $paginas));
                  foreach ($rotos as $r) {
                      echo "Roto: $r\\n";
                  }
                  echo "Enlaces rotos: " . count($rotos) . "\\n";
              ''',
              al_superar="Dos puertas que no llevaban a ningún lado, encontradas. El reflejo del Hipocampo tiembla.",
              imagen=["Una calle de vidrieras revueltas de noche, con puertas pintadas que no se abren y reflejos de colores en los vidrios.",
                      HIPOCAMPO + " reflejado en un vidrio.", NILO + " revisa una puerta con un farol.", GHECO + " sobre un picaporte."]),
            m(id="S04-N05-P2", titulo="Las imágenes sin alt",
              lugar=REFLEJOS, personajes="Nilo, Iara, Gheco",
              criatura="dragon",
              carta="Revisar imágenes | cada <img> con su alt · las decorativas con alt=\"\" (vacío a propósito) · las que no tienen alt, se marcan",
              recompensa="xp 15, oro 15",
              escena="""
                  El Hipocampo borró las descripciones de las fotos de media calle. Iara recorre las vidrieras con la libreta y marca las que quedaron sin `alt`.
              """,
              sugiere="Buscá cada `<img …>` con `preg_match_all` y fijate si tiene `alt=`. Las que no lo tienen se avisan.",
              desafio="Contá las imágenes sin `alt`.",
              inicial='''
                  <?php
                  $html = '<img src="a.png" alt="Velas rojas"><img src="b.png"><img src="borde.png" alt=""><img src="c.png">';
                  echo "Imagenes sin alt: 0\\n";
              ''',
              solucion='''
                  <?php
                  $html = '<img src="a.png" alt="Velas rojas"><img src="b.png"><img src="borde.png" alt=""><img src="c.png">';
                  preg_match_all('/<img\\b[^>]*>/', $html, $m);
                  $sinAlt = array_filter($m[0], fn ($img) => !str_contains($img, 'alt='));
                  foreach ($sinAlt as $img) {
                      preg_match('/src="([^"]+)"/', $img, $s);
                      echo "Sin alt: {$s[1]}\\n";
                  }
                  echo "Imagenes sin alt: " . count($sinAlt) . "\\n";
              ''',
              al_superar="Dos fotos sin descripción, encontradas. La decorativa, con su `alt` vacío a propósito, está bien. Iara tilda la libreta.",
              imagen=["Una fila de vidrieras con fotos enmarcadas, dos con un círculo rojo pintado en el vidrio.",
                      IARA + " pinta un círculo en el vidrio.", NILO + " le alumbra con el farol.", GHECO + " sobre un marco."]),
            m(id="S04-N05-P3", titulo="La vidriera de punta a punta",
              lugar=REFLEJOS, personajes="Nilo, Elefa, Gheco",
              criatura="dragon",
              carta="Todo junto | esqueleto completo · etiquetas con significado · un h1 · imágenes con alt · enlaces que andan · una sola hoja de estilos",
              recompensa="xp 25, oro 30",
              escena="""
                  El Hipocampo tiene una sola debilidad: las páginas que están bien de punta a punta. Nilo arma un revisor que mire todo a la vez, como lo haría un cliente exigente.
              """,
              sugiere="Una función que revisa la página y devuelve la lista de problemas: falta el `<!DOCTYPE`, más de un `<h1>`, falta el `<main>`, o hay imágenes sin `alt`.",
              desafio="Completá el revisor y probalo con las dos vidrieras.",
              inicial='''
                  <?php
                  function revisar(string $html): array
                  {
                      return [];
                  }

                  $revuelta = '<html><h1>Velas</h1><h1>Ofertas</h1><img src="x.png"></html>';
                  $ordenada = '<!DOCTYPE html><html lang="es"><body><header><h1>Velas</h1></header><main><img src="x.png" alt="Velas"></main></body></html>';
                  foreach (['revuelta' => $revuelta, 'ordenada' => $ordenada] as $nombre => $html) {
                      $p = revisar($html);
                      echo "$nombre: " . ($p === [] ? 'impecable' : implode('; ', $p)) . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function revisar(string $html): array
                  {
                      $problemas = [];
                      if (!str_starts_with(ltrim($html), '<!DOCTYPE html>')) {
                          $problemas[] = 'falta el DOCTYPE';
                      }
                      if (substr_count($html, '<h1') !== 1) {
                          $problemas[] = 'tiene que haber un solo h1';
                      }
                      if (!str_contains($html, '<main')) {
                          $problemas[] = 'falta el main';
                      }
                      preg_match_all('/<img\\b[^>]*>/', $html, $m);
                      foreach ($m[0] as $img) {
                          if (!str_contains($img, 'alt=')) {
                              $problemas[] = 'hay una imagen sin alt';
                          }
                      }
                      return $problemas;
                  }

                  $revuelta = '<html><h1>Velas</h1><h1>Ofertas</h1><img src="x.png"></html>';
                  $ordenada = '<!DOCTYPE html><html lang="es"><body><header><h1>Velas</h1></header><main><img src="x.png" alt="Velas"></main></body></html>';
                  foreach (['revuelta' => $revuelta, 'ordenada' => $ordenada] as $nombre => $html) {
                      $p = revisar($html);
                      echo "$nombre: " . ($p === [] ? 'impecable' : implode('; ', $p)) . "\\n";
                  }
              ''',
              al_superar="La vidriera ordenada sale impecable. El Hipocampo se mira en ella y no encuentra nada que comer: se va a buscar comida a otro puerto, dejando un reflejo de colores. Elefa: —Las vidrieras más lindas las hacen en los Talleres de Tesela. Este camino, si lo seguís, llega hasta allá.",
              imagen=["Una calle de vidrieras ordenadas e iluminadas al amanecer, y un caballito de mar de vidrio de colores alejándose por el reflejo de los vidrios.",
                      HIPOCAMPO + " alejándose.", ELEFA + " señala el horizonte con el bastón.", NILO + " frente a la vidriera ordenada.", GHECO + " sobre el cartel."]),
        ],
    },
    {
        "titulo": "S02-N01 · Rutas, controladores y vistas con Blade",
        "misiones": [
            m(id="S02-N01-P1", titulo="Las salas del Bastión",
              lugar=BASTION, personajes="Nilo, Pico, Gheco",
              carta="Rutas con nombre | Route::get('/barcos/{id}', …)->name('barcos.ver') · route('barcos.ver', 12) arma la dirección · si cambia la URL, los enlaces no se rompen",
              recompensa="xp 10, oro 10",
              escena="""
                  El segundo camino desde la Encrucijada sube a una fortaleza de piedra clara: el **Bastión de Laravel**. Adentro todo tiene su lugar. A Pico no lo dejan entrar; Nilo lo esconde en la gorra. Cada sala tiene un nombre, y para ir a una no hace falta saber el camino: alcanza con el nombre.
              """,
              sugiere="Un array de rutas con nombre y una función `route($nombre, $parametros)` que reemplace `{id}` por el valor. " + IMITA,
              desafio="Escribí `route()` para armar las direcciones por nombre.",
              inicial='''
                  <?php
                  $rutas = ['barcos.lista' => '/barcos', 'barcos.ver' => '/barcos/{id}', 'viajes.ver' => '/barcos/{barco}/viajes/{viaje}'];

                  function route(array $rutas, string $nombre, array $parametros = []): string
                  {
                      return $rutas[$nombre];
                  }

                  echo route($rutas, 'barcos.lista') . "\\n";
                  echo route($rutas, 'barcos.ver', ['id' => 12]) . "\\n";
                  echo route($rutas, 'viajes.ver', ['barco' => 12, 'viaje' => 3]) . "\\n";
              ''',
              solucion='''
                  <?php
                  $rutas = ['barcos.lista' => '/barcos', 'barcos.ver' => '/barcos/{id}', 'viajes.ver' => '/barcos/{barco}/viajes/{viaje}'];

                  function route(array $rutas, string $nombre, array $parametros = []): string
                  {
                      $url = $rutas[$nombre];
                      foreach ($parametros as $clave => $valor) {
                          $url = str_replace('{' . $clave . '}', rawurlencode((string) $valor), $url);
                      }
                      return $url;
                  }

                  echo route($rutas, 'barcos.lista') . "\\n";
                  echo route($rutas, 'barcos.ver', ['id' => 12]) . "\\n";
                  echo route($rutas, 'viajes.ver', ['barco' => 12, 'viaje' => 3]) . "\\n";
              ''',
              al_superar="Nilo llega a cada sala por su nombre. Pico, desde la gorra, no se pierde ninguna.",
              imagen=["El interior de una fortaleza de piedra clara con pasillos ordenados y puertas con plaquitas lisas de colores.",
                      NILO + " camina por un pasillo, con la gorra un poco abultada.", PICO + " asomando la cabeza por debajo de la gorra.", GHECO + " sobre una plaquita."]),
            m(id="S02-N01-P2", titulo="Llaves dobles",
              lugar=BASTION, personajes="Nilo, Gheco",
              criatura="troll",
              carta="Blade | {{ $x }} escapa (htmlspecialchars) · {!! $x !!} no escapa: solo para HTML que armaste vos · @foreach, @if, @empty",
              recompensa="xp 15, oro 15",
              escena="""
                  En el taller donde se dibujan las vistas, los guardias no dejan pasar un dato sin escapar. Nilo usó `{!! !!}` para todo «porque era más corto», y un **troll** se coló en la lista de barcos.
              """,
              sugiere="Imitá el trabajo de Blade: `{{ … }}` se reemplaza por el dato escapado con `htmlspecialchars`, `{!! … !!}` por el dato tal cual.",
              desafio="Completá el mini-Blade para que `{{ }}` escape.",
              inicial='''
                  <?php
                  function blade(string $plantilla, array $datos): string
                  {
                      return preg_replace_callback('/\\{\\{\\s*\\$(\\w+)\\s*\\}\\}|\\{!!\\s*\\$(\\w+)\\s*!!\\}/', function ($m) use ($datos) {
                          $clave = $m[1] !== '' ? $m[1] : $m[2];
                          return $datos[$clave];
                      }, $plantilla);
                  }

                  $datos = ['barco' => '<script>troll()</script>', 'icono' => '<b>*</b>'];
                  echo blade('<li>{{ $barco }} {!! $icono !!}</li>', $datos) . "\\n";
              ''',
              solucion='''
                  <?php
                  function blade(string $plantilla, array $datos): string
                  {
                      return preg_replace_callback('/\\{\\{\\s*\\$(\\w+)\\s*\\}\\}|\\{!!\\s*\\$(\\w+)\\s*!!\\}/', function ($m) use ($datos) {
                          if ($m[1] !== '') {
                              return htmlspecialchars((string) $datos[$m[1]]);
                          }
                          return (string) $datos[$m[2]];
                      }, $plantilla);
                  }

                  $datos = ['barco' => '<script>troll()</script>', 'icono' => '<b>*</b>'];
                  echo blade('<li>{{ $barco }} {!! $icono !!}</li>', $datos) . "\\n";
              ''',
              al_superar="El nombre tramposo sale desarmado; el ícono que armó Nilo, tal cual. El troll se queda afuera del taller.",
              imagen=["El taller de vistas del Bastión con mesas de dibujo y moldes de páginas, y un guardia en la puerta revisando papeles.",
                      "Un troll frenado en la puerta por el guardia.", NILO + " dibuja en una mesa.", GHECO + " sobre la mesa de dibujo."]),
            m(id="S02-N01-P3", titulo="Solo números",
              lugar=BASTION, personajes="Nilo, Gheco",
              carta="Restricciones de ruta | ->whereNumber('id') · /barcos/abc no entra al controlador: 404 · el controlador recibe siempre un número",
              recompensa="xp 15, oro 15",
              escena="""
                  Alguien pidió `/barcos/gaviota` y el controlador intentó buscar el barco número «gaviota». Laravel deja poner una condición a cada parámetro de la ruta, para que eso ni llegue.
              """,
              sugiere="Antes de llamar al controlador, comprobá que el parámetro cumpla su patrón (`ctype_digit`). Si no, 404.",
              desafio="Agregá la restricción de que el id sea un número.",
              inicial='''
                  <?php
                  function verBarco(int $id): string
                  {
                      return "200 Barco $id";
                  }

                  function despachar(string $url): string
                  {
                      if (preg_match('#^/barcos/([^/]+)$#', $url, $m)) {
                          return verBarco((int) $m[1]);
                      }
                      return "404";
                  }

                  foreach (['/barcos/12', '/barcos/gaviota'] as $u) {
                      echo "$u -> " . despachar($u) . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function verBarco(int $id): string
                  {
                      return "200 Barco $id";
                  }

                  function despachar(string $url): string
                  {
                      if (preg_match('#^/barcos/([^/]+)$#', $url, $m) && ctype_digit($m[1])) {
                          return verBarco((int) $m[1]);
                      }
                      return "404";
                  }

                  foreach (['/barcos/12', '/barcos/gaviota'] as $u) {
                      echo "$u -> " . despachar($u) . "\\n";
                  }
              ''',
              al_superar="«Gaviota» no es un número: 404 sin molestar al controlador. Pico, que se llama como varios barcos, se ofende un poco.",
              imagen=["La puerta de una sala del Bastión con una cerradura con forma de número, y un papel con una gaviota dibujada que no entra.",
                      NILO + " intenta meter el papel en la cerradura.", GHECO + " sobre la cerradura."]),
        ],
    },
    {
        "titulo": "S02-N02 · Migraciones, Eloquent y formularios con MariaDB",
        "misiones": [
            m(id="S02-N02-P1", titulo="Las reglas del guardia",
              lugar=SOTANO_B, personajes="Nilo, Fermín, Gheco",
              carta="Validación de Laravel | ['nombre' => 'required|max:30', 'kilos' => 'required|integer|min:1'] · cada regla con su mensaje en español · se devuelven todos los errores juntos",
              recompensa="xp 10, oro 10",
              escena="""
                  En el sótano del Bastión, un guardia revisa cada formulario antes de que toque la bodega, con una lista de reglas escrita en una sola línea. Fermín, que vino de visita, desconfía de una bodega que escribe sola, pero le gusta el guardia.
              """,
              sugiere="Partí cada regla con `explode('|', …)` y revisá `required`, `integer` y `min:N`. " + IMITA,
              desafio="Completá el validador de reglas.",
              inicial='''
                  <?php
                  function validar(array $datos, array $reglas): array
                  {
                      return [];
                  }

                  $reglas = ['nombre' => 'required', 'kilos' => 'required|integer|min:1'];
                  foreach ([['nombre' => '', 'kilos' => '0'], ['nombre' => 'Gaviota', 'kilos' => '300']] as $d) {
                      $e = validar($d, $reglas);
                      echo $e === [] ? "Valido\\n" : implode('; ', $e) . "\\n";
                  }
              ''',
              solucion='''
                  <?php
                  function validar(array $datos, array $reglas): array
                  {
                      $errores = [];
                      foreach ($reglas as $campo => $lista) {
                          $valor = trim((string) ($datos[$campo] ?? ''));
                          foreach (explode('|', $lista) as $regla) {
                              [$nombre, $parametro] = array_pad(explode(':', $regla, 2), 2, null);
                              $falla = match ($nombre) {
                                  'required' => $valor === '' ? "El campo $campo es obligatorio" : null,
                                  'integer' => $valor !== '' && !ctype_digit($valor) ? "El campo $campo tiene que ser un numero entero" : null,
                                  'min' => $valor !== '' && (int) $valor < (int) $parametro ? "El campo $campo tiene que ser al menos $parametro" : null,
                                  default => null,
                              };
                              if ($falla !== null) {
                                  $errores[] = $falla;
                                  break;
                              }
                          }
                      }
                      return $errores;
                  }

                  $reglas = ['nombre' => 'required', 'kilos' => 'required|integer|min:1'];
                  foreach ([['nombre' => '', 'kilos' => '0'], ['nombre' => 'Gaviota', 'kilos' => '300']] as $d) {
                      $e = validar($d, $reglas);
                      echo $e === [] ? "Valido\\n" : implode('; ', $e) . "\\n";
                  }
              ''',
              al_superar="El primer formulario vuelve con sus dos errores, en español; el segundo pasa. Fermín asiente: el guardia sabe lo suyo.",
              imagen=["La puerta del sótano del Bastión con un guardia que lee un formulario con una lupa y una lista de reglas colgada.",
                      FERMIN + " lo mira por encima de los anteojos.", NILO + " le entrega un formulario.", GHECO + " sobre la lista de reglas."]),
            m(id="S02-N02-P2", titulo="Un barco tiene muchos viajes",
              lugar=SOTANO_B, personajes="Nilo, Gheco",
              carta="Eloquent | class Barco extends Model · public function viajes() { return $this->hasMany(Viaje::class); } · $barco->viajes trae los suyos",
              recompensa="xp 15, oro 15",
              escena="""
                  En el Bastión cada registro se maneja como un objeto. Nilo quiere los viajes de un barco y escribe la consulta a mano otra vez. Gheco le muestra cómo lo haría el modelo: el barco ya sabe cuáles son sus viajes.
              """,
              sugiere="Una clase `Barco` con un método `viajes()` que filtra los viajes de **ese** barco. Es lo que hace `hasMany` por vos.",
              desafio="Escribí la relación `viajes()`.",
              inicial='''
                  <?php
                  $tablaViajes = [['barco_id' => 1, 'destino' => 'Forjas'], ['barco_id' => 2, 'destino' => 'Valle'], ['barco_id' => 1, 'destino' => 'Ciudadela']];

                  final class Barco
                  {
                      public function __construct(public readonly int $id, public readonly string $nombre)
                      {
                      }

                      public function viajes(array $tabla): array
                      {
                          return $tabla;
                      }
                  }

                  $gaviota = new Barco(1, 'Gaviota');
                  echo "{$gaviota->nombre}: " . implode(', ', array_column($gaviota->viajes($tablaViajes), 'destino')) . "\\n";
              ''',
              solucion='''
                  <?php
                  $tablaViajes = [['barco_id' => 1, 'destino' => 'Forjas'], ['barco_id' => 2, 'destino' => 'Valle'], ['barco_id' => 1, 'destino' => 'Ciudadela']];

                  final class Barco
                  {
                      public function __construct(public readonly int $id, public readonly string $nombre)
                      {
                      }

                      public function viajes(array $tabla): array
                      {
                          return array_values(array_filter($tabla, fn ($v) => $v['barco_id'] === $this->id));
                      }
                  }

                  $gaviota = new Barco(1, 'Gaviota');
                  echo "{$gaviota->nombre}: " . implode(', ', array_column($gaviota->viajes($tablaViajes), 'destino')) . "\\n";
              ''',
              al_superar="La Gaviota sabe sus viajes: Forjas y Ciudadela. Nilo deja de escribir la misma consulta por centésima vez.",
              imagen=["Un barco de juguete sobre una mesa del sótano del Bastión con dos hilos de luz que lo unen a dos fichas de viaje.",
                      NILO + " tira de un hilo.", GHECO + " caminando por el otro hilo."]),
            m(id="S02-N02-P3", titulo="Los pergaminos numerados",
              lugar=SOTANO_B, personajes="Nilo, Fermín, Gheco",
              carta="Migraciones | cada cambio de la base es un archivo numerado · se corren en orden y una sola vez · la tabla migrations recuerda cuáles ya corrieron",
              recompensa="xp 15, oro 15",
              escena="""
                  Las tablas del Bastión se describen en pergaminos numerados: las **migraciones**. Nilo corrió el pergamino 2 dos veces y la tabla se armó repetida. Fermín le muestra el libro donde se anota cuáles ya se leyeron.
              """,
              sugiere="Recorré las migraciones en orden y corré solo las que no están en `$hechas`; después de correr una, anotala.",
              desafio="Completá el corredor de migraciones.",
              inicial='''
                  <?php
                  $migraciones = [
                      '2026_10_01_crear_barcos' => 'CREATE TABLE barcos',
                      '2026_10_02_crear_viajes' => 'CREATE TABLE viajes',
                      '2026_10_05_agregar_calado' => 'ALTER TABLE barcos ADD calado',
                  ];
                  $hechas = ['2026_10_01_crear_barcos'];

                  foreach ($migraciones as $nombre => $sql) {
                      echo "Corriendo $nombre\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $migraciones = [
                      '2026_10_01_crear_barcos' => 'CREATE TABLE barcos',
                      '2026_10_02_crear_viajes' => 'CREATE TABLE viajes',
                      '2026_10_05_agregar_calado' => 'ALTER TABLE barcos ADD calado',
                  ];
                  $hechas = ['2026_10_01_crear_barcos'];

                  ksort($migraciones);
                  foreach ($migraciones as $nombre => $sql) {
                      if (in_array($nombre, $hechas, true)) {
                          continue;
                      }
                      echo "Corriendo $nombre: $sql\\n";
                      $hechas[] = $nombre;
                  }
                  echo "Hechas: " . count($hechas) . "\\n";
              ''',
              al_superar="Cada pergamino se lee una vez, en orden. Fermín anota el libro con la misma letra prolija de siempre.",
              imagen=["Una fila de pergaminos enrollados con sellos de números de puntitos, y un libro abierto con tildes al lado.",
                      FERMIN + " tilda el libro.", NILO + " desenrolla un pergamino.", GHECO + " sobre un sello."]),
        ],
    },
    {
        "titulo": "S02-N03 · Jefe del Bastión: el Grifo de los Registros",
        "misiones": [
            m(id="S02-N03-P1", titulo="Formato y reglas del negocio",
              lugar=TORRE_B, personajes="Nilo, Gheco",
              criatura="dragon",
              carta="Dos capas | la validación revisa el formato (¿es un número?) · la regla del negocio revisa lo que el sistema no puede permitir (¿dos barcos en el mismo muelle el mismo día?)",
              recompensa="xp 15, oro 15",
              escena="""
                  Sobre la torre más alta anida el **Grifo de los Registros**. Cada mañana revisa los libros y, si encuentra dos barcos en el mismo muelle el mismo día, arranca la página con el pico. El formulario de Nilo validaba el formato, pero dejaba pasar los choques.
              """,
              sugiere="Primero el formato (muelle numérico, fecha válida); después la regla: si ya hay un amarre en ese muelle y esa fecha, se rechaza con su motivo.",
              desafio="Agregá la regla del negocio después de la validación.",
              inicial='''
                  <?php
                  $amarres = [['muelle' => 2, 'fecha' => '2026-11-03']];

                  function amarrar(array &$amarres, array $pedido): string
                  {
                      if (!ctype_digit((string) $pedido['muelle'])) {
                          return "422 muelle invalido";
                      }
                      $amarres[] = $pedido;
                      return "201 amarrado";
                  }

                  echo amarrar($amarres, ['muelle' => 'dos', 'fecha' => '2026-11-03']) . "\\n";
                  echo amarrar($amarres, ['muelle' => 2, 'fecha' => '2026-11-03']) . "\\n";
                  echo amarrar($amarres, ['muelle' => 3, 'fecha' => '2026-11-03']) . "\\n";
              ''',
              solucion='''
                  <?php
                  $amarres = [['muelle' => 2, 'fecha' => '2026-11-03']];

                  function amarrar(array &$amarres, array $pedido): string
                  {
                      if (!ctype_digit((string) $pedido['muelle'])) {
                          return "422 muelle invalido";
                      }
                      foreach ($amarres as $a) {
                          if ($a['muelle'] === (int) $pedido['muelle'] && $a['fecha'] === $pedido['fecha']) {
                              return "409 el muelle {$a['muelle']} ya esta ocupado ese dia";
                          }
                      }
                      $amarres[] = ['muelle' => (int) $pedido['muelle'], 'fecha' => $pedido['fecha']];
                      return "201 amarrado";
                  }

                  echo amarrar($amarres, ['muelle' => 'dos', 'fecha' => '2026-11-03']) . "\\n";
                  echo amarrar($amarres, ['muelle' => 2, 'fecha' => '2026-11-03']) . "\\n";
                  echo amarrar($amarres, ['muelle' => 3, 'fecha' => '2026-11-03']) . "\\n";
              ''',
              al_superar="El choque se frena antes de llegar al libro. El Grifo baja, revisa y no encuentra nada que arrancar. Se rasca el monóculo, intrigado.",
              imagen=["La torre más alta del Bastión de noche, con un grifo enorme posado en la almena mirando un libro abierto con lupa.",
                      GRIFO + " revisando el libro con el monóculo.", NILO + " sostiene el libro abierto.", GHECO + " sobre una almena."]),
            m(id="S02-N03-P2", titulo="De a diez, con filtro",
              lugar=TORRE_B, personajes="Nilo, Iara, Gheco",
              criatura="dragon",
              carta="Filtrar y paginar | ->when($destino, fn ($q) => $q->where(…)) ->paginate(10) · la página trae sus datos y cuántas hay · el filtro sigue en los enlaces",
              recompensa="xp 15, oro 15",
              escena="""
                  El Grifo revisa cientos de registros por mañana. Iara propone mostrarle de a pocos, filtrados por destino, y que al pasar de página el filtro no se pierda.
              """,
              sugiere="Filtrá por destino solo si viene uno, después cortá la página con `array_slice` y armá el enlace a la siguiente con `http_build_query` conservando el filtro.",
              desafio="Completá el listado filtrado y paginado.",
              inicial='''
                  <?php
                  $registros = array_map(fn ($i) => ['id' => $i, 'destino' => $i % 3 === 0 ? 'Valle' : 'Forjas'], range(1, 12));

                  function pagina(array $registros, ?string $destino, int $pagina, int $porPagina): array
                  {
                      return ['items' => array_slice($registros, 0, $porPagina), 'siguiente' => '/registros?page=2'];
                  }

                  $p = pagina($registros, 'Valle', 1, 2);
                  echo "Ids: " . implode(', ', array_column($p['items'], 'id')) . "\\n";
                  echo "Siguiente: {$p['siguiente']}\\n";
              ''',
              solucion='''
                  <?php
                  $registros = array_map(fn ($i) => ['id' => $i, 'destino' => $i % 3 === 0 ? 'Valle' : 'Forjas'], range(1, 12));

                  function pagina(array $registros, ?string $destino, int $pagina, int $porPagina): array
                  {
                      if ($destino !== null) {
                          $registros = array_values(array_filter($registros, fn ($r) => $r['destino'] === $destino));
                      }
                      $ultima = max(1, (int) ceil(count($registros) / $porPagina));
                      $siguiente = $pagina < $ultima ? '/registros?' . http_build_query(['destino' => $destino, 'page' => $pagina + 1]) : null;
                      return ['items' => array_slice($registros, ($pagina - 1) * $porPagina, $porPagina), 'siguiente' => $siguiente ?? '(no hay mas)'];
                  }

                  $p = pagina($registros, 'Valle', 1, 2);
                  echo "Ids: " . implode(', ', array_column($p['items'], 'id')) . "\\n";
                  echo "Siguiente: {$p['siguiente']}\\n";
                  $q = pagina($registros, 'Valle', 2, 2);
                  echo "Ids: " . implode(', ', array_column($q['items'], 'id')) . "\\n";
                  echo "Siguiente: {$q['siguiente']}\\n";
              ''',
              al_superar="El Grifo revisa de a dos, solo los del Valle, y al pasar de página el filtro sigue ahí. Iara anota que le gustaría un grifo así para su escritorio.",
              imagen=["Pilas chicas de registros atadas con cintas sobre una almena, y un grifo revisando la primera pila.",
                      IARA + " ata una pila con una cinta.", NILO + " le alcanza otra pila al grifo.", GHECO + " sobre una cinta."]),
            m(id="S02-N03-P3", titulo="El guardián de los libros",
              lugar=TORRE_B, personajes="Nilo, Elefa, Gheco",
              criatura="dragon",
              carta="Todo el Bastión | rutas con nombre · validación en español · reglas del negocio · relaciones · filtros y páginas · mensajes de una sola vez · y una prueba para cada regla",
              recompensa="xp 25, oro 30",
              escena="""
                  El Grifo baja por última vez, dispuesto a arrancar la página que encuentre mal. Nilo tiene que mostrarle que el sistema tiene una **prueba para cada cosa** que el Grifo busca, y que todas pasan.
              """,
              sugiere="Una lista de reglas con su prueba (una función que devuelve `true` si se cumple). Corré todas y mostrá ok o FALLA; si todas pasan, el Grifo se queda.",
              desafio="Escribí las pruebas de las tres reglas del Grifo.",
              inicial='''
                  <?php
                  $amarres = [['muelle' => 1, 'fecha' => '2026-11-03'], ['muelle' => 2, 'fecha' => '2026-11-03']];
                  $barcos = [['nombre' => 'Gaviota', 'calado' => 4], ['nombre' => 'Delfin', 'calado' => 2]];

                  $pruebas = [];

                  $todas = true;
                  foreach ($pruebas as $regla => $prueba) {
                      $ok = $prueba();
                      $todas = $todas && $ok;
                      echo ($ok ? 'ok    ' : 'FALLA ') . $regla . "\\n";
                  }
                  echo count($pruebas) === 3 && $todas ? "El Grifo se queda a cuidar los libros\\n" : "El Grifo arranca una pagina\\n";
              ''',
              solucion='''
                  <?php
                  $amarres = [['muelle' => 1, 'fecha' => '2026-11-03'], ['muelle' => 2, 'fecha' => '2026-11-03']];
                  $barcos = [['nombre' => 'Gaviota', 'calado' => 4], ['nombre' => 'Delfin', 'calado' => 2]];

                  $pruebas = [
                      'ningun muelle con dos barcos el mismo dia' => fn () => count($amarres) === count(array_unique(array_map(fn ($a) => $a['muelle'] . '@' . $a['fecha'], $amarres))),
                      'ningun calado pasa de 12 m' => fn () => max(array_column($barcos, 'calado')) <= 12,
                      'todo amarre tiene fecha' => fn () => array_filter($amarres, fn ($a) => ($a['fecha'] ?? '') === '') === [],
                  ];

                  $todas = true;
                  foreach ($pruebas as $regla => $prueba) {
                      $ok = $prueba();
                      $todas = $todas && $ok;
                      echo ($ok ? 'ok    ' : 'FALLA ') . $regla . "\\n";
                  }
                  echo count($pruebas) === 3 && $todas ? "El Grifo se queda a cuidar los libros\\n" : "El Grifo arranca una pagina\\n";
              ''',
              al_superar="Tres reglas, tres pruebas en verde. El Grifo no encuentra nada que arrancar: pliega las alas, se acomoda el monóculo y se queda a cuidar los libros del Puerto. Elefa hace sonar la campana tres veces.",
              imagen=["La torre del Bastión al amanecer con un grifo enorme posado tranquilo sobre un libro cerrado, con las alas plegadas.",
                      GRIFO + " acomodándose el monóculo.", NILO + " con el libro de pruebas abierto.", ELEFA + " llegando a la torre con el bastón.", GHECO + " sobre el libro."]),
        ],
    },
]
