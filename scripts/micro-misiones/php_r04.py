from genphp import m
from php_r01 import NILO, ELEFA, IARA, PICO, GHECO

ESCALERA = "La escalera de piedra"
FICHAS = "Las estanterías de fichas"
DOS_ESTANTES = "Las dos estanterías"
MONTACARGAS = "El montacargas"
LIBRETA = "La libreta de consultas"
REPUESTOS = "El inventario de repuestos"
BANCO = "El banco del Puerto"
ENCARGADOS = "Los encargados de estantería"
SOTANO = "El Sótano Inundado"
FERMIN = "Fermín (anciano bajo y encorvado, barba blanca larga, anteojos redondos de bronce, guardapolvo gris, gorro de lana, farol de luz cian)"
SERPIENTE = "la Serpiente Marina de las Tablas (serpiente marina enorme de escamas azul oscuro, con placas rectangulares lisas en el lomo en filas y columnas que brillan cian, ojos amarillos)"
SQLITE = "Acá la bodega de práctica es SQLite en memoria (`new PDO('sqlite::memory:')`): el SQL es el mismo que vas a usar con MariaDB."

NODOS = [
    {
        "titulo": "R04-N01 · Bases de datos y MariaDB",
        "misiones": [
            m(id="R04-N01-P1", titulo="La primera estantería",
              lugar=ESCALERA, personajes="Nilo, Fermín, Gheco",
              carta="CREATE TABLE | CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, kilos INTEGER) · cada columna con su tipo · la clave identifica cada fila",
              recompensa="xp 10, oro 10",
              escena="""
                  Bajando una escalera de piedra, bajo la torre, está la **Bodega del Puerto**. Un anciano de barba blanca y farol cian, **Fermín, el Bodeguero**, encuentra cualquier ficha en segundos. —¿Cómo hace para acordarse de todo? —pregunta Nilo. —No me acuerdo —dice Fermín—. Lo anoto bien.
              """,
              sugiere="Primero se arma la estantería (`CREATE TABLE`), después se cargan las fichas (`INSERT`) y se leen (`SELECT`). " + SQLITE,
              desafio="Creá la tabla `barco` con su clave, cargá los dos barcos y mostralos.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

                  // Creá la tabla y cargá los barcos acá

                  foreach ($db->query('SELECT id, nombre, kilos FROM barco') as $fila) {
                      echo "{$fila['id']}. {$fila['nombre']}: {$fila['kilos']} kg\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, kilos INTEGER)');
                  $db->exec("INSERT INTO barco (nombre, kilos) VALUES ('Gaviota', 300), ('Albatros', 820)");

                  foreach ($db->query('SELECT id, nombre, kilos FROM barco') as $fila) {
                      echo "{$fila['id']}. {$fila['nombre']}: {$fila['kilos']} kg\\n";
                  }
              ''',
              al_superar="Dos fichas, cada una con su número. Fermín las mira por encima de los anteojos y asiente despacio.",
              imagen=["Una escalera de piedra que baja a una bodega con galerías de estanterías llenas de fichas ordenadas, iluminada por un farol cian.",
                      FERMIN + " al pie de la escalera con su farol.", NILO + " bajando los últimos escalones.", GHECO + " sobre la baranda."]),
            m(id="R04-N01-P2", titulo="La ficha mal completada",
              lugar=ESCALERA, personajes="Nilo, Fermín, Gheco",
              carta="Restricciones | NOT NULL no deja vacíos · UNIQUE no deja repetidos · CHECK (kilos > 0) · la base se defiende sola",
              recompensa="xp 15, oro 15",
              escena="""
                  Fermín nunca deja entrar una ficha mal completada. Nilo intenta guardar un barco sin nombre y otro con kilos negativos, y su estantería los acepta a los dos.
              """,
              sugiere="Agregale a la tabla `NOT NULL` en el nombre y `CHECK (kilos > 0)` en los kilos. La base rechaza lo que no cumple con una `PDOException`.",
              desafio="Agregá las restricciones para que la estantería rechace las fichas malas.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT, kilos INTEGER)');

                  foreach (["('Gaviota', 300)", "(NULL, 50)", "('Fantasma', -10)"] as $valores) {
                      try {
                          $db->exec("INSERT INTO barco (nombre, kilos) VALUES $valores");
                          echo "Guardada: $valores\\n";
                      } catch (PDOException $e) {
                          echo "Rechazada: $valores\\n";
                      }
                  }
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, kilos INTEGER CHECK (kilos > 0))');

                  foreach (["('Gaviota', 300)", "(NULL, 50)", "('Fantasma', -10)"] as $valores) {
                      try {
                          $db->exec("INSERT INTO barco (nombre, kilos) VALUES $valores");
                          echo "Guardada: $valores\\n";
                      } catch (PDOException $e) {
                          echo "Rechazada: $valores\\n";
                      }
                  }
              ''',
              al_superar="La estantería se defiende sola. Fermín: —Así me gusta. Que la bodega diga que no, aunque yo no esté.",
              imagen=["Una estantería de fichas con una ficha rota rechazada que cae al piso.",
                      FERMIN + " señala la ficha caída con el farol.", NILO + " la junta del piso.", GHECO + " sobre la estantería."]),
            m(id="R04-N01-P3", titulo="Un solo número por barco",
              lugar=ESCALERA, personajes="Nilo, Fermín, Gheco",
              criatura="ogro",
              carta="UNIQUE | UNIQUE en la matrícula: no puede haber dos iguales · la clave primaria también es única · la base avisa con un error de duplicado",
              recompensa="xp 10, oro 10",
              escena="""
                  En la bodega apareció dos veces el mismo barco, con la misma matrícula y distintos kilos. Nadie sabe cuál es el de verdad. Un **ogro** se ríe entre las estanterías.
              """,
              sugiere="Con `matricula TEXT UNIQUE`, la segunda ficha con la misma matrícula se rechaza.",
              desafio="Hacé que la matrícula no se pueda repetir.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, matricula TEXT, kilos INTEGER)');

                  foreach ([['PM-01', 300], ['PM-02', 80], ['PM-01', 999]] as [$mat, $kilos]) {
                      try {
                          $db->exec("INSERT INTO barco (matricula, kilos) VALUES ('$mat', $kilos)");
                          echo "Guardado $mat\\n";
                      } catch (PDOException $e) {
                          echo "Repetido: $mat\\n";
                      }
                  }
                  echo "Barcos: " . $db->query('SELECT COUNT(*) FROM barco')->fetchColumn() . "\\n";
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, matricula TEXT NOT NULL UNIQUE, kilos INTEGER)');

                  foreach ([['PM-01', 300], ['PM-02', 80], ['PM-01', 999]] as [$mat, $kilos]) {
                      try {
                          $db->exec("INSERT INTO barco (matricula, kilos) VALUES ('$mat', $kilos)");
                          echo "Guardado $mat\\n";
                      } catch (PDOException $e) {
                          echo "Repetido: $mat\\n";
                      }
                  }
                  echo "Barcos: " . $db->query('SELECT COUNT(*) FROM barco')->fetchColumn() . "\\n";
              ''',
              al_superar="Cada barco una vez. El ogro, sin confusión que aprovechar, se va a otra galería.",
              imagen=["Dos fichas iguales en una estantería, una brillando en verde y la otra tachada en rojo, sin letras.",
                      "Un ogro asoma entre los estantes.", NILO + " saca la ficha repetida.", GHECO + " sobre la estantería."]),
        ],
    },
    {
        "titulo": "R04-N02 · Consultas: filtrar, ordenar y agrupar",
        "misiones": [
            m(id="R04-N02-P1", titulo="Las preguntas de Fermín",
              lugar=FICHAS, personajes="Nilo, Fermín, Gheco",
              carta="WHERE y ORDER BY | SELECT … WHERE kilos > 500 ORDER BY kilos DESC · LIMIT n se queda con los primeros",
              recompensa="xp 10, oro 10",
              escena="""
                  A Fermín le preguntan: *«¿qué barcos de más de 500 kilos salieron, del más pesado al más liviano?»*. Nilo recorre las estanterías una por una. Vuelve a la tarde, con telarañas en la gorra.
              """,
              sugiere="`WHERE kilos > 500` elige las filas y `ORDER BY kilos DESC` las ordena de mayor a menor. " + SQLITE,
              desafio="Escribí la consulta que contesta la pregunta.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->exec('CREATE TABLE barco (nombre TEXT, kilos INTEGER)');
                  $db->exec("INSERT INTO barco VALUES ('Gaviota', 300), ('Albatros', 820), ('Tortuga', 510), ('Condor', 760)");

                  foreach ($db->query('SELECT nombre, kilos FROM barco') as $f) {
                      echo "{$f['nombre']}: {$f['kilos']}\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->exec('CREATE TABLE barco (nombre TEXT, kilos INTEGER)');
                  $db->exec("INSERT INTO barco VALUES ('Gaviota', 300), ('Albatros', 820), ('Tortuga', 510), ('Condor', 760)");

                  foreach ($db->query('SELECT nombre, kilos FROM barco WHERE kilos > 500 ORDER BY kilos DESC') as $f) {
                      echo "{$f['nombre']}: {$f['kilos']}\\n";
                  }
              ''',
              al_superar="La respuesta sale en un segundo. Nilo se saca las telarañas de la gorra y se las da a Pico, que no las quiere.",
              imagen=["Galerías largas de estanterías de fichas con telarañas en las esquinas.",
                      FERMIN + " escribe una pregunta en un papel.", NILO + " con telarañas en la gorra.", GHECO + " colgando de una telaraña."]),
            m(id="R04-N02-P2", titulo="¿Cuánto facturó cada muelle?",
              lugar=FICHAS, personajes="Nilo, Fermín, Gheco",
              carta="GROUP BY | SELECT muelle, SUM(sellos) FROM pago GROUP BY muelle · una fila por grupo · COUNT, SUM, AVG, MIN, MAX",
              recompensa="xp 15, oro 15",
              escena="""
                  La segunda pregunta del día: *«¿cuánto facturó cada muelle?»*. Nilo suma a mano los pagos del muelle 1, se marea, y empieza de nuevo.
              """,
              sugiere="`GROUP BY muelle` junta las filas de cada muelle y `SUM(sellos)` las suma.",
              desafio="Mostrá el total y la cantidad de pagos de cada muelle.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->exec('CREATE TABLE pago (muelle INTEGER, sellos INTEGER)');
                  $db->exec('INSERT INTO pago VALUES (1, 40), (2, 15), (1, 25), (3, 70), (2, 35), (1, 10)');

                  foreach ($db->query('SELECT muelle, sellos FROM pago') as $f) {
                      echo "Muelle {$f['muelle']}: {$f['sellos']}\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->exec('CREATE TABLE pago (muelle INTEGER, sellos INTEGER)');
                  $db->exec('INSERT INTO pago VALUES (1, 40), (2, 15), (1, 25), (3, 70), (2, 35), (1, 10)');

                  $sql = 'SELECT muelle, COUNT(*) AS pagos, SUM(sellos) AS total FROM pago GROUP BY muelle ORDER BY muelle';
                  foreach ($db->query($sql) as $f) {
                      echo "Muelle {$f['muelle']}: {$f['total']} sellos en {$f['pagos']} pagos\\n";
                  }
              ''',
              al_superar="Tres renglones, uno por muelle. El muelle 1 ganó, como siempre. Fermín lo sabía, pero lo anota igual.",
              imagen=["Tres pilas de sellos de lacre de distinto alto sobre una mesa de la bodega, cada una con un banderín de color.",
                      NILO + " pone el último sello en una pila.", FERMIN + " mira las pilas con el farol.", GHECO + " sobre la pila más alta."]),
            m(id="R04-N02-P3", titulo="Los que no retiraron",
              lugar=FICHAS, personajes="Nilo, Fermín, Gheco",
              carta="IS NULL y LIKE | WHERE retiro IS NULL (nunca = NULL) · WHERE producto LIKE 'yerba%' · % es cualquier cosa",
              recompensa="xp 15, oro 15",
              escena="""
                  *«¿Quién pidió yerba y no la retiró?»*. Nilo escribe `retiro = NULL` y la bodega no le devuelve a nadie, aunque hay tres paquetes juntando polvo.
              """,
              sugiere="`NULL` no es igual a nada, ni siquiera a sí mismo: se pregunta con `IS NULL`. Y `LIKE 'yerba%'` encuentra todo lo que empieza con «yerba».",
              desafio="Arreglá la consulta.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->exec('CREATE TABLE pedido (cliente TEXT, producto TEXT, retiro TEXT)');
                  $db->exec("INSERT INTO pedido VALUES ('Olmo', 'yerba mate', NULL), ('Lia', 'sal', NULL), ('Ana', 'yerba suave', '2026-10-02'), ('Beto', 'yerba mate', NULL)");

                  $sql = "SELECT cliente FROM pedido WHERE producto = 'yerba' AND retiro = NULL ORDER BY cliente";
                  $quienes = $db->query($sql)->fetchAll(PDO::FETCH_COLUMN);
                  echo "Sin retirar: " . (implode(', ', $quienes) ?: 'nadie') . "\\n";
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->exec('CREATE TABLE pedido (cliente TEXT, producto TEXT, retiro TEXT)');
                  $db->exec("INSERT INTO pedido VALUES ('Olmo', 'yerba mate', NULL), ('Lia', 'sal', NULL), ('Ana', 'yerba suave', '2026-10-02'), ('Beto', 'yerba mate', NULL)");

                  $sql = "SELECT cliente FROM pedido WHERE producto LIKE 'yerba%' AND retiro IS NULL ORDER BY cliente";
                  $quienes = $db->query($sql)->fetchAll(PDO::FETCH_COLUMN);
                  echo "Sin retirar: " . (implode(', ', $quienes) ?: 'nadie') . "\\n";
              ''',
              al_superar="Beto y Olmo. Fermín les manda un aviso. Pico se ofrece a llevarlo; nadie se lo da.",
              imagen=["Dos paquetes de yerba con polvo en un estante de la bodega, con una etiqueta lisa.",
                      NILO + " sopla el polvo de un paquete.", FERMIN + " anota en su libreta.", GHECO + " sobre un paquete."]),
            m(id="R04-N02-P4", titulo="Siempre con WHERE",
              lugar=FICHAS, personajes="Nilo, Fermín, Gheco",
              criatura="ogro",
              carta="UPDATE y DELETE | UPDATE barco SET kilos = 0 WHERE id = 3 · sin WHERE cambia TODAS las filas · antes de borrar, probar el WHERE con un SELECT",
              recompensa="xp 15, oro 15",
              escena="""
                  Fermín le pide a Nilo que descargue el barco número 3. Nilo escribe `UPDATE barco SET kilos = 0` y la bodega entera queda vacía. Un **ogro** aplaude.
              """,
              sugiere="El `WHERE id = 3` dice **qué** fila cambiar. Sin él, cambian todas.",
              desafio="Descargá solo el barco 3.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT, kilos INTEGER)');
                  $db->exec("INSERT INTO barco (nombre, kilos) VALUES ('Gaviota', 300), ('Albatros', 820), ('Tortuga', 510)");

                  $cambiadas = $db->exec('UPDATE barco SET kilos = 0');
                  echo "Filas cambiadas: $cambiadas\\n";
                  foreach ($db->query('SELECT nombre, kilos FROM barco') as $f) {
                      echo "{$f['nombre']}: {$f['kilos']}\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT, kilos INTEGER)');
                  $db->exec("INSERT INTO barco (nombre, kilos) VALUES ('Gaviota', 300), ('Albatros', 820), ('Tortuga', 510)");

                  $cambiadas = $db->exec('UPDATE barco SET kilos = 0 WHERE id = 3');
                  echo "Filas cambiadas: $cambiadas\\n";
                  foreach ($db->query('SELECT nombre, kilos FROM barco') as $f) {
                      echo "{$f['nombre']}: {$f['kilos']}\\n";
                  }
              ''',
              al_superar="Una sola fila cambiada: la Tortuga. Los demás barcos conservan su carga. El ogro deja de aplaudir.",
              imagen=["Tres barcos en el muelle, dos cargados de cajones y uno vacío.",
                      "Un ogro con las manos juntas, decepcionado.", NILO + " sobre el barco vacío.", GHECO + " sobre un cajón."]),
        ],
    },
    {
        "titulo": "R04-N03 · Relaciones y JOIN",
        "misiones": [
            m(id="R04-N03-P1", titulo="Las trescientas fichas de la Gaviota",
              lugar=DOS_ESTANTES, personajes="Nilo, Fermín, Gheco",
              carta="Relaciones | barco (id, nombre, telefono) · viaje (id, barco_id, destino) · cada dato una sola vez · los viajes guardan solo el número del barco",
              recompensa="xp 10, oro 10",
              escena="""
                  Cada ficha de viaje repetía todo el barco, teléfono del capitán incluido. Cuando el capitán de la *Gaviota* cambió de teléfono, Nilo tuvo que corregir trescientas fichas y se olvidó de cuarenta. Ahora hay dos estanterías: barcos y viajes.
              """,
              sugiere="Con `INNER JOIN barco ON barco.id = viaje.barco_id` cada viaje trae los datos de su barco, guardados una sola vez.",
              desafio="Uní los viajes con su barco para mostrar el teléfono.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT, telefono TEXT)');
                  $db->exec('CREATE TABLE viaje (id INTEGER PRIMARY KEY, barco_id INTEGER, destino TEXT)');
                  $db->exec("INSERT INTO barco VALUES (1, 'Gaviota', '3825-111'), (2, 'Albatros', '3825-222')");
                  $db->exec("INSERT INTO viaje (barco_id, destino) VALUES (1, 'Forjas'), (2, 'Valle'), (1, 'Ciudadela')");
                  $db->exec("UPDATE barco SET telefono = '3825-999' WHERE id = 1");

                  foreach ($db->query('SELECT destino, barco_id FROM viaje') as $f) {
                      echo "{$f['destino']}: barco {$f['barco_id']}\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT, telefono TEXT)');
                  $db->exec('CREATE TABLE viaje (id INTEGER PRIMARY KEY, barco_id INTEGER, destino TEXT)');
                  $db->exec("INSERT INTO barco VALUES (1, 'Gaviota', '3825-111'), (2, 'Albatros', '3825-222')");
                  $db->exec("INSERT INTO viaje (barco_id, destino) VALUES (1, 'Forjas'), (2, 'Valle'), (1, 'Ciudadela')");
                  $db->exec("UPDATE barco SET telefono = '3825-999' WHERE id = 1");

                  $sql = 'SELECT viaje.destino, barco.nombre, barco.telefono FROM viaje INNER JOIN barco ON barco.id = viaje.barco_id ORDER BY viaje.id';
                  foreach ($db->query($sql) as $f) {
                      echo "{$f['destino']}: {$f['nombre']} ({$f['telefono']})\\n";
                  }
              ''',
              al_superar="Un solo cambio y todos los viajes de la Gaviota muestran el teléfono nuevo. Las cuarenta fichas olvidadas ya no existen.",
              imagen=["Dos estanterías de fichas una frente a la otra, unidas por hilos de luz cian entre fichas.",
                      FERMIN + " tiende un hilo entre las estanterías.", NILO + " sostiene la otra punta.", GHECO + " caminando por un hilo."]),
            m(id="R04-N03-P2", titulo="Los barcos que no viajaron",
              lugar=DOS_ESTANTES, personajes="Nilo, Fermín, Gheco",
              carta="LEFT JOIN | trae todas las filas de la izquierda, aunque no tengan pareja · lo que falta viene en NULL · COUNT(viaje.id) cuenta solo los que hay",
              recompensa="xp 15, oro 15",
              escena="""
                  Fermín quiere saber cuántos viajes hizo cada barco, **incluidos** los que no hicieron ninguno. El `INNER JOIN` de Nilo deja afuera a la Tortuga, que no salió nunca.
              """,
              sugiere="Con `LEFT JOIN` los barcos sin viajes también aparecen, y `COUNT(viaje.id)` les da 0.",
              desafio="Contá los viajes de cada barco, sin dejar a ninguno afuera.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT)');
                  $db->exec('CREATE TABLE viaje (id INTEGER PRIMARY KEY, barco_id INTEGER)');
                  $db->exec("INSERT INTO barco VALUES (1, 'Gaviota'), (2, 'Albatros'), (3, 'Tortuga')");
                  $db->exec('INSERT INTO viaje (barco_id) VALUES (1), (2), (1), (1)');

                  $sql = 'SELECT barco.nombre, COUNT(viaje.id) AS viajes FROM barco INNER JOIN viaje ON viaje.barco_id = barco.id GROUP BY barco.id ORDER BY barco.id';
                  foreach ($db->query($sql) as $f) {
                      echo "{$f['nombre']}: {$f['viajes']}\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT)');
                  $db->exec('CREATE TABLE viaje (id INTEGER PRIMARY KEY, barco_id INTEGER)');
                  $db->exec("INSERT INTO barco VALUES (1, 'Gaviota'), (2, 'Albatros'), (3, 'Tortuga')");
                  $db->exec('INSERT INTO viaje (barco_id) VALUES (1), (2), (1), (1)');

                  $sql = 'SELECT barco.nombre, COUNT(viaje.id) AS viajes FROM barco LEFT JOIN viaje ON viaje.barco_id = barco.id GROUP BY barco.id ORDER BY barco.id';
                  foreach ($db->query($sql) as $f) {
                      echo "{$f['nombre']}: {$f['viajes']}\\n";
                  }
              ''',
              al_superar="La Tortuga aparece con 0 viajes. Fermín la anota para el próximo encargo: nadie se queda sin trabajo en su bodega.",
              imagen=["Tres barcos amarrados, dos con banderines de viajes colgando y uno, una tortuga de madera, sin ninguno.",
                      NILO + " le pone un banderín vacío a la Tortuga.", FERMIN + " lo mira con el farol.", GHECO + " sobre la Tortuga."]),
            m(id="R04-N03-P3", titulo="No se borra lo que tiene viajes",
              lugar=DOS_ESTANTES, personajes="Nilo, Fermín, Gheco",
              criatura="troll",
              carta="FOREIGN KEY | barco_id INTEGER REFERENCES barco(id) · la base no deja borrar un barco con viajes · en SQLite: PRAGMA foreign_keys = ON",
              recompensa="xp 15, oro 15",
              escena="""
                  Nilo borró la ficha del Albatros, que todavía tenía viajes, y esos viajes quedaron apuntando a la nada. Un **troll** se instaló en el hueco. —La bodega te tiene que frenar —dice Fermín.
              """,
              sugiere="Con `REFERENCES barco(id)` en la columna `barco_id`, la base no deja borrar un barco que tiene viajes. En la bodega de práctica (SQLite) hay que prender ese control con `PRAGMA foreign_keys = ON`; en MariaDB viene prendido.",
              desafio="Agregá la clave foránea para que la base frene el borrado.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                  $db->exec('PRAGMA foreign_keys = ON');
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT)');
                  $db->exec('CREATE TABLE viaje (id INTEGER PRIMARY KEY, barco_id INTEGER)');
                  $db->exec("INSERT INTO barco VALUES (1, 'Gaviota'), (2, 'Albatros')");
                  $db->exec('INSERT INTO viaje (barco_id) VALUES (2)');

                  try {
                      $db->exec('DELETE FROM barco WHERE id = 2');
                      echo "Albatros borrado\\n";
                  } catch (PDOException $e) {
                      echo "No se puede: el Albatros tiene viajes\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                  $db->exec('PRAGMA foreign_keys = ON');
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT)');
                  $db->exec('CREATE TABLE viaje (id INTEGER PRIMARY KEY, barco_id INTEGER NOT NULL REFERENCES barco(id))');
                  $db->exec("INSERT INTO barco VALUES (1, 'Gaviota'), (2, 'Albatros')");
                  $db->exec('INSERT INTO viaje (barco_id) VALUES (2)');

                  try {
                      $db->exec('DELETE FROM barco WHERE id = 2');
                      echo "Albatros borrado\\n";
                  } catch (PDOException $e) {
                      echo "No se puede: el Albatros tiene viajes\\n";
                  }
              ''',
              al_superar="La bodega frena el borrado. El troll se queda sin hueco y sube la escalera, rezongando.",
              imagen=["Una estantería de fichas con una ficha atada con una cadena de luz cian a otra estantería, que no se puede sacar.",
                      NILO + " tira de la ficha sin poder sacarla.", FERMIN + " sonríe.", "Un troll subiendo la escalera, enojado.", GHECO + " sobre la cadena."]),
            m(id="R04-N03-P4", titulo="Muchos a muchos",
              lugar=DOS_ESTANTES, personajes="Nilo, Iara, Gheco",
              carta="Tabla intermedia | un viaje lleva muchos pasajeros y un pasajero hace muchos viajes · pasaje (viaje_id, pasajero_id) · dos JOIN",
              recompensa="xp 15, oro 15",
              escena="""
                  Iara quiere saber quiénes viajaron a las Forjas. Un pasajero hace muchos viajes y un viaje lleva muchos pasajeros: no entra en una columna. Hace falta una tercera estantería: los pasajes.
              """,
              sugiere="La tabla `pasaje` une cada viaje con cada pasajero. Con dos `JOIN` se va del viaje al pasaje y del pasaje al pasajero.",
              desafio="Mostrá los pasajeros del viaje a las Forjas, en orden alfabético.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->exec('CREATE TABLE viaje (id INTEGER PRIMARY KEY, destino TEXT)');
                  $db->exec('CREATE TABLE pasajero (id INTEGER PRIMARY KEY, nombre TEXT)');
                  $db->exec('CREATE TABLE pasaje (viaje_id INTEGER, pasajero_id INTEGER)');
                  $db->exec("INSERT INTO viaje VALUES (1, 'Forjas'), (2, 'Valle')");
                  $db->exec("INSERT INTO pasajero VALUES (1, 'Olmo'), (2, 'Ana'), (3, 'Beto')");
                  $db->exec('INSERT INTO pasaje VALUES (1, 1), (1, 2), (2, 2), (2, 3)');

                  echo "A Forjas viajan: ?\\n";
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->exec('CREATE TABLE viaje (id INTEGER PRIMARY KEY, destino TEXT)');
                  $db->exec('CREATE TABLE pasajero (id INTEGER PRIMARY KEY, nombre TEXT)');
                  $db->exec('CREATE TABLE pasaje (viaje_id INTEGER, pasajero_id INTEGER)');
                  $db->exec("INSERT INTO viaje VALUES (1, 'Forjas'), (2, 'Valle')");
                  $db->exec("INSERT INTO pasajero VALUES (1, 'Olmo'), (2, 'Ana'), (3, 'Beto')");
                  $db->exec('INSERT INTO pasaje VALUES (1, 1), (1, 2), (2, 2), (2, 3)');

                  $sql = "SELECT pasajero.nombre FROM viaje
                          JOIN pasaje ON pasaje.viaje_id = viaje.id
                          JOIN pasajero ON pasajero.id = pasaje.pasajero_id
                          WHERE viaje.destino = 'Forjas' ORDER BY pasajero.nombre";
                  echo "A Forjas viajan: " . implode(', ', $db->query($sql)->fetchAll(PDO::FETCH_COLUMN)) . "\\n";
              ''',
              al_superar="Ana y Olmo. Iara arma la lista de embarque sin buscar en tres libretas.",
              imagen=["Tres estanterías de fichas en triángulo, unidas por hilos de luz cian en el medio.",
                      IARA + " sigue un hilo con el dedo.", NILO + " lee una ficha.", GHECO + " en el centro de los hilos."]),
        ],
    },
    {
        "titulo": "R04-N04 · PDO: conectarse desde PHP",
        "misiones": [
            m(id="R04-N04-P1", titulo="El montacargas",
              lugar=MONTACARGAS, personajes="Nilo, Iara, Fermín, Gheco",
              carta="PDO | new PDO($dsn, $usuario, $clave, $opciones) · ERRMODE_EXCEPTION para que avise fuerte · FETCH_ASSOC para filas con nombres",
              recompensa="xp 10, oro 10",
              escena="""
                  Entre la Oficina de Correos y la Bodega hay un montacargas que nadie usaba: Iara escribía arriba, Fermín abajo, y Nilo subía y bajaba la escalera cuarenta veces por día. Elefa tira de la cuerda y el montacargas empieza a andar.
              """,
              sugiere="Las opciones se pasan al crear el PDO: `PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION` y `PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC`. Con MariaDB el DSN sería `mysql:host=…;dbname=…;charset=utf8mb4`.",
              desafio="Creá la conexión con las opciones recomendadas y leé la fila.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->exec("CREATE TABLE aviso (texto TEXT)");
                  $db->exec("INSERT INTO aviso VALUES ('El montacargas anda')");

                  $fila = $db->query('SELECT texto FROM aviso')->fetch();
                  echo "Columnas: " . count($fila) . "\\n";
                  echo $fila['texto'] . "\\n";
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [
                      PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                      PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                  ]);
                  $db->exec("CREATE TABLE aviso (texto TEXT)");
                  $db->exec("INSERT INTO aviso VALUES ('El montacargas anda')");

                  $fila = $db->query('SELECT texto FROM aviso')->fetch();
                  echo "Columnas: " . count($fila) . "\\n";
                  echo $fila['texto'] . "\\n";
              ''',
              al_superar="El montacargas sube con la primera fila. Nilo se sienta en el último escalón, agradecido para siempre.",
              imagen=["Un montacargas de madera y bronce con una cuerda, entre un piso de oficinas arriba y una bodega de piedra abajo.",
                      IARA + " arriba, mandando un papel.", FERMIN + " abajo, recibiéndolo.", NILO + " sentado en un escalón, descansando.", GHECO + " sobre la cuerda."]),
            m(id="R04-N04-P2", titulo="fetch, fetchAll, fetchColumn",
              lugar=MONTACARGAS, personajes="Nilo, Fermín, Gheco",
              carta="Leer | fetch() una fila · fetchAll() todas · fetchColumn() el primer valor (ideal para COUNT) · exec() para lo que no devuelve filas",
              recompensa="xp 15, oro 15",
              escena="""
                  Fermín manda tres respuestas por el montacargas: un número, una fila y una lista. Nilo las abre todas igual, con `fetchAll`, y el número le llega envuelto en dos arrays.
              """,
              sugiere="Para un solo valor, `fetchColumn()`; para una fila, `fetch()`; para todas, `fetchAll()`.",
              desafio="Leé cada respuesta con la función que corresponde.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
                  $db->exec('CREATE TABLE barco (nombre TEXT, kilos INTEGER)');
                  $db->exec("INSERT INTO barco VALUES ('Gaviota', 300), ('Albatros', 820), ('Tortuga', 510)");

                  $cantidad = $db->query('SELECT COUNT(*) FROM barco')->fetchAll();
                  echo "Barcos: " . json_encode($cantidad) . "\\n";
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
                  $db->exec('CREATE TABLE barco (nombre TEXT, kilos INTEGER)');
                  $db->exec("INSERT INTO barco VALUES ('Gaviota', 300), ('Albatros', 820), ('Tortuga', 510)");

                  $cantidad = $db->query('SELECT COUNT(*) FROM barco')->fetchColumn();
                  echo "Barcos: $cantidad\\n";

                  $masPesado = $db->query('SELECT nombre, kilos FROM barco ORDER BY kilos DESC LIMIT 1')->fetch();
                  echo "El mas pesado: {$masPesado['nombre']}\\n";

                  $nombres = $db->query('SELECT nombre FROM barco ORDER BY nombre')->fetchAll(PDO::FETCH_COLUMN);
                  echo "Todos: " . implode(', ', $nombres) . "\\n";
              ''',
              al_superar="Un número, una fila y una lista, cada uno en su envase. Fermín manda una cuarta respuesta: un té.",
              imagen=["El montacargas abierto con tres paquetes de distinto tamaño adentro: uno chiquito, uno mediano y uno largo.",
                      NILO + " saca los paquetes.", GHECO + " sobre el más chiquito."]),
            m(id="R04-N04-P3", titulo="Cuando la bodega falla",
              lugar=MONTACARGAS, personajes="Nilo, Gheco",
              criatura="esqueleto",
              carta="PDOException | try { … } catch (PDOException $e) · al visitante, un mensaje amable · el detalle, al registro · nunca la clave ni el SQL en pantalla",
              recompensa="xp 10, oro 10",
              escena="""
                  Un día el montacargas pidió una tabla que no existía, y la página le mostró al visitante todo el error, con el SQL y la ruta de los archivos. Un **esqueleto** se asomó por el hueco.
              """,
              sugiere="Atrapá la `PDOException`: al visitante le mostrás un mensaje amable y el detalle lo guardás en una variable (o en un registro).",
              desafio="Mostrá un mensaje amable en vez del error crudo.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $filas = $db->query('SELECT * FROM barcos_fantasma')->fetchAll();
                  echo count($filas) . " barcos\\n";
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $registro = [];
                  try {
                      $filas = $db->query('SELECT * FROM barcos_fantasma')->fetchAll();
                      echo count($filas) . " barcos\\n";
                  } catch (PDOException $e) {
                      $registro[] = $e->getMessage();
                      echo "La bodega no responde. Proba en un rato.\\n";
                  }
                  echo "Errores registrados: " . count($registro) . "\\n";
              ''',
              al_superar="El visitante ve un mensaje amable; el detalle queda guardado para quien sabe arreglarlo. El esqueleto vuelve a su estante.",
              imagen=["El hueco oscuro de un montacargas con un esqueleto chiquito asomado.",
                      NILO + " le pone un cartel liso con un dibujo de una taza de té en la puerta.", GHECO + " sobre el cartel."]),
        ],
    },
    {
        "titulo": "R04-N05 · Consultas preparadas e inyección SQL",
        "misiones": [
            m(id="R04-N05-P1", titulo="Gaviota' OR '1'='1",
              lugar=LIBRETA, personajes="Nilo, Fermín, Gheco",
              criatura="troll",
              carta="Inyección SQL | nunca pegar un dato en el texto del SQL · prepare('… WHERE nombre = ?') · execute([$nombre]) · el dato nunca se vuelve código",
              recompensa="xp 15, oro 15",
              escena="""
                  Un día llegó al montacargas un pedido extraño. Donde iba el nombre de un barco decía: `Gaviota' OR '1'='1`. Fermín, que copiaba los pedidos tal cual en su libreta, leyó *«traeme los barcos que se llamen Gaviota… o cualquiera»*. Y subió toda la bodega.
              """,
              sugiere="Con `prepare` la consulta va con un hueco `?`, y el dato viaja aparte en `execute([$nombre])`: el truco queda como un nombre raro, no como SQL.",
              desafio="Cambiá la consulta pegada por una preparada.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
                  $db->exec('CREATE TABLE barco (nombre TEXT, capitan TEXT)');
                  $db->exec("INSERT INTO barco VALUES ('Gaviota', 'Marina'), ('Albatros', 'Ramos'), ('Tortuga', 'Quiroga')");

                  $pedido = "Gaviota' OR '1'='1";
                  $filas = $db->query("SELECT nombre FROM barco WHERE nombre = '$pedido'")->fetchAll();
                  echo "Encontrados: " . count($filas) . "\\n";
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
                  $db->exec('CREATE TABLE barco (nombre TEXT, capitan TEXT)');
                  $db->exec("INSERT INTO barco VALUES ('Gaviota', 'Marina'), ('Albatros', 'Ramos'), ('Tortuga', 'Quiroga')");

                  $pedido = "Gaviota' OR '1'='1";
                  $consulta = $db->prepare('SELECT nombre FROM barco WHERE nombre = ?');
                  $consulta->execute([$pedido]);
                  echo "Encontrados: " . count($consulta->fetchAll()) . "\\n";
              ''',
              al_superar="Cero barcos se llaman `Gaviota' OR '1'='1`. La bodega no se vacía. Desde ese día, Fermín mira cada pedido con los anteojos en la punta de la nariz.",
              imagen=["La libreta de consultas de Fermín abierta, con un papel pegado con un truco tachado, sin letras legibles.",
                      FERMIN + " mira el papel por encima de los anteojos.", NILO + " le muestra un sobre con un hueco recortado.", "Un troll asoma detrás de una estantería.", GHECO + " sobre la libreta."]),
            m(id="R04-N05-P2", titulo="Con nombre",
              lugar=LIBRETA, personajes="Nilo, Fermín, Gheco",
              carta="Parámetros con nombre | prepare('… WHERE kilos > :min AND destino = :destino') · execute(['min' => 100, 'destino' => 'Valle'])",
              recompensa="xp 10, oro 10",
              escena="""
                  La consulta de Fermín tiene cuatro huecos `?` y Nilo pasó los datos en otro orden: buscó barcos de «Valle» kilos al destino 100.
              """,
              sugiere="Con huecos con nombre (`:min`, `:destino`) el orden no importa: cada dato va a su hueco por nombre.",
              desafio="Usá parámetros con nombre.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
                  $db->exec('CREATE TABLE viaje (barco TEXT, destino TEXT, kilos INTEGER)');
                  $db->exec("INSERT INTO viaje VALUES ('Gaviota', 'Valle', 300), ('Albatros', 'Valle', 80), ('Tortuga', 'Forjas', 500)");

                  $c = $db->prepare('SELECT barco FROM viaje WHERE kilos > ? AND destino = ?');
                  $c->execute(['Valle', 100]);
                  echo "Barcos: " . implode(', ', $c->fetchAll(PDO::FETCH_COLUMN)) . "\\n";
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
                  $db->exec('CREATE TABLE viaje (barco TEXT, destino TEXT, kilos INTEGER)');
                  $db->exec("INSERT INTO viaje VALUES ('Gaviota', 'Valle', 300), ('Albatros', 'Valle', 80), ('Tortuga', 'Forjas', 500)");

                  $c = $db->prepare('SELECT barco FROM viaje WHERE kilos > :min AND destino = :destino');
                  $c->execute(['destino' => 'Valle', 'min' => 100]);
                  echo "Barcos: " . implode(', ', $c->fetchAll(PDO::FETCH_COLUMN)) . "\\n";
              ''',
              al_superar="La Gaviota, la única de más de 100 kilos al Valle. Cada dato en su hueco, sin importar el orden.",
              imagen=["Una hoja con huecos recortados con formas distintas (un círculo, un triángulo) y fichas que encajan en cada uno.",
                      NILO + " pone una ficha en su hueco.", FERMIN + " lo mira con aprobación.", GHECO + " dentro de un hueco."]),
            m(id="R04-N05-P3", titulo="El número que se acaba de crear",
              lugar=LIBRETA, personajes="Nilo, Gheco",
              carta="lastInsertId y rowCount | después de un INSERT, lastInsertId() da el id nuevo · después de UPDATE o DELETE, rowCount() dice cuántas filas tocó",
              recompensa="xp 15, oro 15",
              escena="""
                  Nilo da de alta un barco y quiere mostrarle al capitán su número de registro, pero no sabe cuál le tocó. Busca el más alto a mano y se equivoca porque justo entró otro.
              """,
              sugiere="`$db->lastInsertId()` da el id que se creó con **tu** `INSERT`. Y `$consulta->rowCount()` dice cuántas filas cambió un `UPDATE`.",
              desafio="Mostrá el número nuevo y cuántas filas cambió la actualización.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT, activo INTEGER DEFAULT 1)');
                  $db->exec("INSERT INTO barco (nombre) VALUES ('Gaviota'), ('Albatros')");

                  $alta = $db->prepare('INSERT INTO barco (nombre) VALUES (?)');
                  $alta->execute(['Delfin']);
                  echo "Registro nuevo: ?\\n";

                  $baja = $db->prepare('UPDATE barco SET activo = 0 WHERE id < ?');
                  $baja->execute([3]);
                  echo "Dados de baja: ?\\n";
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:');
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT, activo INTEGER DEFAULT 1)');
                  $db->exec("INSERT INTO barco (nombre) VALUES ('Gaviota'), ('Albatros')");

                  $alta = $db->prepare('INSERT INTO barco (nombre) VALUES (?)');
                  $alta->execute(['Delfin']);
                  echo "Registro nuevo: " . $db->lastInsertId() . "\\n";

                  $baja = $db->prepare('UPDATE barco SET activo = 0 WHERE id < ?');
                  $baja->execute([3]);
                  echo "Dados de baja: " . $baja->rowCount() . "\\n";
              ''',
              al_superar="El capitán del Delfín se va con su número 3 anotado. Nilo, por una vez, también.",
              imagen=["Un mostrador de la bodega con un talonario de registros y un capitán de barco recibiendo un papel con un sello.",
                      NILO + " le entrega el papel.", GHECO + " sobre el talonario."]),
            m(id="R04-N05-P4", titulo="El duplicado",
              lugar=LIBRETA, personajes="Nilo, Fermín, Gheco",
              carta="Errores de la base | un UNIQUE repetido da PDOException · se atrapa y se le avisa a la persona qué pasó · el código de error dice el motivo",
              recompensa="xp 15, oro 15",
              escena="""
                  Un capitán intenta registrar un barco con una matrícula que ya existe. La página de Nilo muestra una pantalla de error espantosa y el capitán se va asustado.
              """,
              sugiere="Atrapá la `PDOException` del `INSERT` y avisá «esa matrícula ya está registrada». La base es la que detecta el duplicado.",
              desafio="Avisá el duplicado con un mensaje claro.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE barco (matricula TEXT PRIMARY KEY, nombre TEXT)');
                  $alta = $db->prepare('INSERT INTO barco VALUES (?, ?)');

                  foreach ([['PM-01', 'Gaviota'], ['PM-01', 'Copia']] as $datos) {
                      $alta->execute($datos);
                      echo "Registrado: {$datos[1]}\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE barco (matricula TEXT PRIMARY KEY, nombre TEXT)');
                  $alta = $db->prepare('INSERT INTO barco VALUES (?, ?)');

                  foreach ([['PM-01', 'Gaviota'], ['PM-01', 'Copia']] as $datos) {
                      try {
                          $alta->execute($datos);
                          echo "Registrado: {$datos[1]}\\n";
                      } catch (PDOException $e) {
                          echo "La matricula {$datos[0]} ya esta registrada\\n";
                      }
                  }
              ''',
              al_superar="El capitán entiende qué pasó y vuelve con la matrícula correcta. Fermín le sirve un té.",
              imagen=["Un capitán de barco frente al mostrador de la bodega, aliviado, con una taza de té en la mano.",
                      FERMIN + " le sirve el té.", NILO + " le muestra un papel.", GHECO + " sobre la tetera."]),
        ],
    },
    {
        "titulo": "R04-N06 · Un ABM web",
        "misiones": [
            m(id="R04-N06-P1", titulo="Ver y agregar repuestos",
              lugar=REPUESTOS, personajes="Nilo, Pico, Gheco",
              carta="ABM | alta (INSERT), baja (DELETE), modificación (UPDATE) y listado (SELECT) · cada acción, una función con su consulta preparada",
              recompensa="xp 10, oro 10",
              escena="""
                  La Capitana le da a Nilo una llave de la Bodega: *Inventario de repuestos*. Hasta hoy lo llevaba Fermín en una planilla, y cada tanto Pico se llevaba una fila. Ahora tiene que vivir en la base.
              """,
              sugiere="Dos funciones: `alta(PDO $db, string $nombre, int $stock)` con un `INSERT` preparado, y `listado(PDO $db)` con un `SELECT` ordenado.",
              desafio="Escribí `alta` y `listado`.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
                  $db->exec('CREATE TABLE repuesto (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL UNIQUE, stock INTEGER NOT NULL)');

                  function alta(PDO $db, string $nombre, int $stock): void
                  {
                  }

                  function listado(PDO $db): array
                  {
                      return [];
                  }

                  alta($db, 'tornillo', 40);
                  alta($db, 'cadena', 3);
                  foreach (listado($db) as $r) {
                      echo "{$r['id']}. {$r['nombre']}: {$r['stock']}\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
                  $db->exec('CREATE TABLE repuesto (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL UNIQUE, stock INTEGER NOT NULL)');

                  function alta(PDO $db, string $nombre, int $stock): void
                  {
                      $db->prepare('INSERT INTO repuesto (nombre, stock) VALUES (?, ?)')->execute([$nombre, $stock]);
                  }

                  function listado(PDO $db): array
                  {
                      return $db->query('SELECT id, nombre, stock FROM repuesto ORDER BY nombre')->fetchAll();
                  }

                  alta($db, 'tornillo', 40);
                  alta($db, 'cadena', 3);
                  foreach (listado($db) as $r) {
                      echo "{$r['id']}. {$r['nombre']}: {$r['stock']}\\n";
                  }
              ''',
              al_superar="Los repuestos viven en la base. Pico revolotea alrededor de la pantalla, buscando una fila que robar. No hay.",
              imagen=["Una bodega de repuestos con cajones de tornillos y rollos de cadena, y una lista colgada.",
                      PICO + " picoteando el borde de la lista sin poder arrancarla.", NILO + " carga un cajón.", GHECO + " sobre un rollo de cadena."]),
            m(id="R04-N06-P2", titulo="Corregir sin romper",
              lugar=REPUESTOS, personajes="Nilo, Gheco",
              carta="Modificar | UPDATE … WHERE id = ? · si rowCount() da 0, el registro no existe: 404 · validar antes de guardar",
              recompensa="xp 15, oro 15",
              escena="""
                  Un empleado intentó corregir el stock del repuesto número 99, que no existe, y la página le dijo «guardado». Otro puso stock -5 y también.
              """,
              sugiere="Validá el stock (no negativo) y, después del `UPDATE`, mirá `rowCount()`: si es 0, el repuesto no existe.",
              desafio="Escribí `modificar` con sus dos controles.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE repuesto (id INTEGER PRIMARY KEY, nombre TEXT, stock INTEGER)');
                  $db->exec("INSERT INTO repuesto (nombre, stock) VALUES ('tornillo', 40), ('cadena', 3)");

                  function modificar(PDO $db, int $id, int $stock): string
                  {
                      $db->prepare('UPDATE repuesto SET stock = ? WHERE id = ?')->execute([$stock, $id]);
                      return "Guardado";
                  }

                  echo modificar($db, 2, 7) . "\\n";
                  echo modificar($db, 99, 10) . "\\n";
                  echo modificar($db, 1, -5) . "\\n";
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE repuesto (id INTEGER PRIMARY KEY, nombre TEXT, stock INTEGER)');
                  $db->exec("INSERT INTO repuesto (nombre, stock) VALUES ('tornillo', 40), ('cadena', 3)");

                  function modificar(PDO $db, int $id, int $stock): string
                  {
                      if ($stock < 0) {
                          return "Error: el stock no puede ser negativo";
                      }
                      $c = $db->prepare('UPDATE repuesto SET stock = ? WHERE id = ?');
                      $c->execute([$stock, $id]);
                      return $c->rowCount() === 0 ? "404: no existe el repuesto $id" : "Guardado";
                  }

                  echo modificar($db, 2, 7) . "\\n";
                  echo modificar($db, 99, 10) . "\\n";
                  echo modificar($db, 1, -5) . "\\n";
              ''',
              al_superar="Cada corrección dice lo que de verdad pasó. El repuesto 99 sigue sin existir, como debe ser.",
              imagen=["Un cajón de repuestos vacío con un número de puntitos y una telaraña, junto a otros cajones llenos.",
                      NILO + " revisa el cajón vacío con un farol.", GHECO + " en la telaraña."]),
            m(id="R04-N06-P3", titulo="La baja confirmada",
              lugar=REPUESTOS, personajes="Nilo, Iara, Gheco",
              criatura="troll",
              carta="Baja | por POST y con confirmación · DELETE … WHERE id = ? · si tiene movimientos, la base frena (o se marca inactivo)",
              recompensa="xp 15, oro 15",
              escena="""
                  Un enlace de «borrar» se podía abrir sin querer, y un repuesto con historia de movimientos desapareció. Un **troll** se quedó con los movimientos huérfanos. Iara propone dos reglas: confirmar y no borrar lo que tiene historia.
              """,
              sugiere="Si la confirmación no es «si», no se borra. Si el repuesto tiene movimientos, la clave foránea frena el `DELETE` y se avisa.",
              desafio="Escribí `baja` con las dos reglas.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('PRAGMA foreign_keys = ON');
                  $db->exec('CREATE TABLE repuesto (id INTEGER PRIMARY KEY, nombre TEXT)');
                  $db->exec('CREATE TABLE movimiento (id INTEGER PRIMARY KEY, repuesto_id INTEGER NOT NULL REFERENCES repuesto(id))');
                  $db->exec("INSERT INTO repuesto VALUES (1, 'tornillo'), (2, 'cadena'), (3, 'remache')");
                  $db->exec('INSERT INTO movimiento (repuesto_id) VALUES (1)');

                  function baja(PDO $db, int $id, string $confirma): string
                  {
                      $db->prepare('DELETE FROM repuesto WHERE id = ?')->execute([$id]);
                      return "Borrado $id";
                  }

                  echo baja($db, 2, 'no') . "\\n";
                  echo baja($db, 1, 'si') . "\\n";
                  echo baja($db, 3, 'si') . "\\n";
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('PRAGMA foreign_keys = ON');
                  $db->exec('CREATE TABLE repuesto (id INTEGER PRIMARY KEY, nombre TEXT)');
                  $db->exec('CREATE TABLE movimiento (id INTEGER PRIMARY KEY, repuesto_id INTEGER NOT NULL REFERENCES repuesto(id))');
                  $db->exec("INSERT INTO repuesto VALUES (1, 'tornillo'), (2, 'cadena'), (3, 'remache')");
                  $db->exec('INSERT INTO movimiento (repuesto_id) VALUES (1)');

                  function baja(PDO $db, int $id, string $confirma): string
                  {
                      if ($confirma !== 'si') {
                          return "Sin confirmar: no se borra $id";
                      }
                      try {
                          $db->prepare('DELETE FROM repuesto WHERE id = ?')->execute([$id]);
                          return "Borrado $id";
                      } catch (PDOException $e) {
                          return "No se puede borrar $id: tiene movimientos";
                      }
                  }

                  echo baja($db, 2, 'no') . "\\n";
                  echo baja($db, 1, 'si') . "\\n";
                  echo baja($db, 3, 'si') . "\\n";
              ''',
              al_superar="Solo se borra el remache, que no tenía historia y alguien confirmó. El troll se queda sin movimientos huérfanos.",
              imagen=["Un botón grande de palanca con una tapa de seguridad de bronce cerrada, en la pared de la bodega.",
                      IARA + " sostiene la tapa cerrada.", NILO + " con la mano cerca de la palanca.", "Un troll escondido detrás de unos cajones.", GHECO + " sobre la tapa."]),
        ],
    },
    {
        "titulo": "R04-N07 · Transacciones, índices y vistas",
        "misiones": [
            m(id="R04-N07-P1", titulo="La transferencia que se cortó",
              lugar=BANCO, personajes="Nilo, Fermín, Gheco",
              criatura="ogro",
              carta="Transacción | beginTransaction() · los dos UPDATE · commit() · si algo falla, rollBack() y no pasó nada · todo o nada",
              recompensa="xp 15, oro 15",
              escena="""
                  El sistema del banco del Puerto se cortó a mitad de una transferencia: los sellos salieron de la cuenta del Astillero y nunca llegaron a la de la fonda. Tres días tardaron en encontrar el error. Un **ogro** todavía se ríe.
              """,
              sugiere="Los dos `UPDATE` van adentro de una transacción. Si algo falla entre medio, `rollBack()` deshace el primero.",
              desafio="Envolvé la transferencia en una transacción.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE cuenta (nombre TEXT PRIMARY KEY, sellos INTEGER)');
                  $db->exec("INSERT INTO cuenta VALUES ('astillero', 500), ('fonda', 100)");

                  function transferir(PDO $db, string $de, string $a, int $monto, bool $seCorta): void
                  {
                      $db->prepare('UPDATE cuenta SET sellos = sellos - ? WHERE nombre = ?')->execute([$monto, $de]);
                      if ($seCorta) {
                          throw new RuntimeException('se corto la luz');
                      }
                      $db->prepare('UPDATE cuenta SET sellos = sellos + ? WHERE nombre = ?')->execute([$monto, $a]);
                  }

                  try {
                      transferir($db, 'astillero', 'fonda', 200, true);
                  } catch (RuntimeException $e) {
                      echo "Fallo: " . $e->getMessage() . "\\n";
                  }
                  foreach ($db->query('SELECT nombre, sellos FROM cuenta') as $f) {
                      echo "{$f['nombre']}: {$f['sellos']}\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE cuenta (nombre TEXT PRIMARY KEY, sellos INTEGER)');
                  $db->exec("INSERT INTO cuenta VALUES ('astillero', 500), ('fonda', 100)");

                  function transferir(PDO $db, string $de, string $a, int $monto, bool $seCorta): void
                  {
                      $db->beginTransaction();
                      try {
                          $db->prepare('UPDATE cuenta SET sellos = sellos - ? WHERE nombre = ?')->execute([$monto, $de]);
                          if ($seCorta) {
                              throw new RuntimeException('se corto la luz');
                          }
                          $db->prepare('UPDATE cuenta SET sellos = sellos + ? WHERE nombre = ?')->execute([$monto, $a]);
                          $db->commit();
                      } catch (Throwable $e) {
                          $db->rollBack();
                          throw $e;
                      }
                  }

                  try {
                      transferir($db, 'astillero', 'fonda', 200, true);
                  } catch (RuntimeException $e) {
                      echo "Fallo: " . $e->getMessage() . "\\n";
                  }
                  foreach ($db->query('SELECT nombre, sellos FROM cuenta') as $f) {
                      echo "{$f['nombre']}: {$f['sellos']}\\n";
                  }
              ''',
              al_superar="Aunque se corte la luz, los 500 sellos siguen en el Astillero. Nada a medias. El ogro se queda sin chiste.",
              imagen=["Dos cofres de sellos de lacre en el banco del puerto unidos por una cadena, con un farol que se apaga entre ellos.",
                      FERMIN + " sostiene el farol que parpadea.", NILO + " abraza un cofre.", "Un ogro riéndose en la sombra.", GHECO + " sobre la cadena."]),
            m(id="R04-N07-P2", titulo="La ficha de la noche de la tormenta",
              lugar=BANCO, personajes="Nilo, Fermín, Elefa, Gheco",
              carta="Índices | CREATE INDEX idx_fecha ON envio (fecha) · encuentra rápido entre millones · se crea en las columnas por las que se busca",
              recompensa="xp 15, oro 15", item="Ficha de la Noche de la Tormenta",
              escena="""
                  Buscando el error de la transferencia, Nilo y Fermín bajan a la estantería más vieja: millones de fichas sin orden por fecha. Buscar una noche de hace veinte años tarda lo que tarda el ferry en cruzar. Fermín propone un **índice**, como el de un libro.
              """,
              sugiere="`CREATE INDEX idx_fecha ON envio (fecha)` arma el índice. Con él, la consulta por fecha va directo. (El resultado es el mismo; lo que cambia es cuánto tarda.)",
              desafio="Creá el índice y buscá los envíos de la noche del 14/03/2006.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE envio (id INTEGER PRIMARY KEY, fecha TEXT, detalle TEXT)');
                  $db->exec("INSERT INTO envio (fecha, detalle) VALUES
                      ('2006-03-13', 'barril de aceite'),
                      ('2006-03-14', 'paquete sin remitente, lacre de vidrio, para quien llegue'),
                      ('2006-03-14', 'mensaje sin remitente, lacre de vidrio, para quien llegue'),
                      ('2006-03-14', 'esa noche se apago el Faro'),
                      ('2006-03-15', 'cajon de sal')");

                  $indices = $db->query("SELECT COUNT(*) FROM sqlite_master WHERE type = 'index' AND tbl_name = 'envio'")->fetchColumn();
                  echo "Indices: $indices\\n";
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE envio (id INTEGER PRIMARY KEY, fecha TEXT, detalle TEXT)');
                  $db->exec("INSERT INTO envio (fecha, detalle) VALUES
                      ('2006-03-13', 'barril de aceite'),
                      ('2006-03-14', 'paquete sin remitente, lacre de vidrio, para quien llegue'),
                      ('2006-03-14', 'mensaje sin remitente, lacre de vidrio, para quien llegue'),
                      ('2006-03-14', 'esa noche se apago el Faro'),
                      ('2006-03-15', 'cajon de sal')");
                  $db->exec('CREATE INDEX idx_fecha ON envio (fecha)');

                  $indices = $db->query("SELECT COUNT(*) FROM sqlite_master WHERE type = 'index' AND tbl_name = 'envio'")->fetchColumn();
                  echo "Indices: $indices\\n";

                  $c = $db->prepare('SELECT detalle FROM envio WHERE fecha = ? ORDER BY id');
                  $c->execute(['2006-03-14']);
                  foreach ($c->fetchAll(PDO::FETCH_COLUMN) as $detalle) {
                      echo "- $detalle\\n";
                  }
              ''',
              al_superar="La ficha de esa noche aparece al instante: **dos envíos sin remitente**, sellados con vidrio de colores, llegaron la misma noche en que se apagó el Faro. Nadie volvió a prenderlo. Elefa se queda mirando la ficha un rato largo.",
              imagen=["La estantería más vieja de la bodega, con polvo, y una ficha amarillenta iluminada por un farol, con el dibujo de dos sobres y un faro apagado.",
                      FERMIN + " sostiene el farol.", NILO + " sostiene la ficha.", ELEFA + " detrás, en silencio.", GHECO + " sobre la estantería."]),
            m(id="R04-N07-P3", titulo="La vista de los pendientes",
              lugar=BANCO, personajes="Nilo, Fermín, Gheco",
              carta="Vistas | CREATE VIEW pendientes AS SELECT … · una consulta guardada con nombre · se usa como una tabla: SELECT * FROM pendientes",
              recompensa="xp 10, oro 10",
              escena="""
                  Todas las mañanas, Fermín escribe la misma consulta larga para ver los envíos pendientes. Nilo se ofrece a escribirla él, y le sale distinta cada día.
              """,
              sugiere="`CREATE VIEW pendientes AS SELECT …` guarda la consulta con nombre. Después basta con `SELECT * FROM pendientes`.",
              desafio="Creá la vista y usala.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE envio (id INTEGER PRIMARY KEY, destino TEXT, entregado INTEGER)');
                  $db->exec("INSERT INTO envio (destino, entregado) VALUES ('Forjas', 1), ('Valle', 0), ('Ciudadela', 0)");

                  foreach ($db->query('SELECT destino FROM pendientes') as $f) {
                      echo "Pendiente: {$f['destino']}\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE envio (id INTEGER PRIMARY KEY, destino TEXT, entregado INTEGER)');
                  $db->exec("INSERT INTO envio (destino, entregado) VALUES ('Forjas', 1), ('Valle', 0), ('Ciudadela', 0)");
                  $db->exec('CREATE VIEW pendientes AS SELECT id, destino FROM envio WHERE entregado = 0 ORDER BY id');

                  foreach ($db->query('SELECT destino FROM pendientes') as $f) {
                      echo "Pendiente: {$f['destino']}\\n";
                  }
              ''',
              al_superar="La consulta queda guardada con su nombre. Fermín ya no la escribe todas las mañanas; ahora toma el té tranquilo.",
              imagen=["Una ventanita en la pared de la bodega por la que se ven solo algunas fichas, iluminadas.",
                      FERMIN + " toma té mirando por la ventanita.", NILO + " al lado.", GHECO + " en el marco de la ventanita."]),
        ],
    },
    {
        "titulo": "R04-N08 · Repositorios y login con base",
        "misiones": [
            m(id="R04-N08-P1", titulo="Ramiro, el encargado",
              lugar=ENCARGADOS, personajes="Nilo, Elefa, Gheco",
              carta="Repositorio | class BarcoRepo { __construct(private PDO $db) } · métodos del dominio: activos(), guardar() · el resto del sistema no escribe SQL",
              recompensa="xp 10, oro 10",
              escena="""
                  La Bodega tiene consultas desparramadas en cuarenta archivos. Cuando cambió el nombre de una columna, Nilo la buscó en todos. Elefa designa un encargado por estantería: *«las fichas de barcos las pide solo Ramiro»*.
              """,
              sugiere="Una clase `BarcoRepo` que recibe el PDO y tiene métodos con nombres del Puerto. El resto del programa le pide a ella.",
              desafio="Escribí el repositorio con `activos()`.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT, activo INTEGER)');
                  $db->exec("INSERT INTO barco (nombre, activo) VALUES ('Gaviota', 1), ('Tortuga', 0), ('Albatros', 1)");

                  class BarcoRepo
                  {
                  }

                  $ramiro = new BarcoRepo($db);
                  foreach ($ramiro->activos() as $nombre) {
                      echo "$nombre\\n";
                  }
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT, activo INTEGER)');
                  $db->exec("INSERT INTO barco (nombre, activo) VALUES ('Gaviota', 1), ('Tortuga', 0), ('Albatros', 1)");

                  class BarcoRepo
                  {
                      public function __construct(private PDO $db)
                      {
                      }

                      /** @return string[] */
                      public function activos(): array
                      {
                          return $this->db->query('SELECT nombre FROM barco WHERE activo = 1 ORDER BY nombre')->fetchAll(PDO::FETCH_COLUMN);
                      }
                  }

                  $ramiro = new BarcoRepo($db);
                  foreach ($ramiro->activos() as $nombre) {
                      echo "$nombre\\n";
                  }
              ''',
              al_superar="El SQL de los barcos vive en un solo lugar: el escritorio de Ramiro. Si mañana cambia una columna, se cambia ahí.",
              imagen=["Un escritorio de madera en la bodega con un cartel liso con el dibujo de un barco, frente a una estantería.",
                      ELEFA + " señala el escritorio con el bastón.", NILO + " deja una pila de papeles en el escritorio.", GHECO + " sobre el cartel."]),
            m(id="R04-N08-P2", titulo="De fila a objeto",
              lugar=ENCARGADOS, personajes="Nilo, Gheco",
              carta="Entidades | el repositorio convierte cada fila en un objeto Barco · el resto del programa trabaja con objetos, no con arrays sueltos",
              recompensa="xp 15, oro 15",
              escena="""
                  El repositorio devuelve arrays, y en cada página alguien escribe `$fila['nombre']` o `$fila['Nombre']` o `$fila['nombre_barco']`. Gheco propone que Ramiro devuelva barcos de verdad.
              """,
              sugiere="El repositorio arma un `new Barco($fila['nombre'], (int) $fila['kilos'])` por cada fila. El objeto sabe hacer sus cosas, como `pesado()`.",
              desafio="Hacé que `buscar()` devuelva un objeto `Barco` (o `null` si no existe).",
              inicial='''
                  <?php
                  final class Barco
                  {
                      public function __construct(public readonly string $nombre, public readonly int $kilos)
                      {
                      }

                      public function pesado(): bool
                      {
                          return $this->kilos > 500;
                      }
                  }

                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT, kilos INTEGER)');
                  $db->exec("INSERT INTO barco (nombre, kilos) VALUES ('Gaviota', 300), ('Albatros', 820)");

                  class BarcoRepo
                  {
                      public function __construct(private PDO $db)
                      {
                      }

                      public function buscar(int $id): array|false
                      {
                          $c = $this->db->prepare('SELECT nombre, kilos FROM barco WHERE id = ?');
                          $c->execute([$id]);
                          return $c->fetch();
                      }
                  }

                  $repo = new BarcoRepo($db);
                  foreach ([2, 7] as $id) {
                      $b = $repo->buscar($id);
                      echo $b instanceof Barco ? "{$b->nombre}: " . ($b->pesado() ? 'pesado' : 'liviano') . "\\n" : "No existe el $id\\n";
                  }
              ''',
              solucion='''
                  <?php
                  final class Barco
                  {
                      public function __construct(public readonly string $nombre, public readonly int $kilos)
                      {
                      }

                      public function pesado(): bool
                      {
                          return $this->kilos > 500;
                      }
                  }

                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
                  $db->exec('CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT, kilos INTEGER)');
                  $db->exec("INSERT INTO barco (nombre, kilos) VALUES ('Gaviota', 300), ('Albatros', 820)");

                  class BarcoRepo
                  {
                      public function __construct(private PDO $db)
                      {
                      }

                      public function buscar(int $id): ?Barco
                      {
                          $c = $this->db->prepare('SELECT nombre, kilos FROM barco WHERE id = ?');
                          $c->execute([$id]);
                          $fila = $c->fetch();
                          return $fila === false ? null : new Barco($fila['nombre'], (int) $fila['kilos']);
                      }
                  }

                  $repo = new BarcoRepo($db);
                  foreach ([2, 7] as $id) {
                      $b = $repo->buscar($id);
                      echo $b instanceof Barco ? "{$b->nombre}: " . ($b->pesado() ? 'pesado' : 'liviano') . "\\n" : "No existe el $id\\n";
                  }
              ''',
              al_superar="Ramiro entrega barcos, no papeles sueltos. Nadie más escribe `$fila['nombre_barco']`.",
              imagen=["Una ficha de cartón que se transforma en un barquito de madera de juguete sobre el escritorio de la bodega.",
                      NILO + " mira el barquito con asombro.", GHECO + " sobre el barquito."]),
            m(id="R04-N08-P3", titulo="El login en la bodega",
              lugar=ENCARGADOS, personajes="Nilo, Iara, Gheco",
              carta="Usuarios en la base | tabla usuario (nombre UNIQUE, huella, rol) · el repositorio busca por nombre · password_verify contra la huella guardada",
              recompensa="xp 15, oro 15",
              escena="""
                  Los usuarios de la Oficina estaban en un array escrito en el código. Iara quiere que vivan en la bodega, con su huella y su rol, y que el login le pregunte al repositorio.
              """,
              sugiere="Guardá la huella con `password_hash` al dar el alta. Para entrar, el repositorio trae la fila por nombre y se compara con `password_verify`.",
              desafio="Completá `entrar` para que use la base.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
                  $db->exec('CREATE TABLE usuario (nombre TEXT PRIMARY KEY, huella TEXT, rol TEXT)');
                  $db->prepare('INSERT INTO usuario VALUES (?, ?, ?)')->execute(['iara', password_hash('cuaderno-azul-12', PASSWORD_DEFAULT), 'escribiente']);

                  function entrar(PDO $db, string $nombre, string $clave): string
                  {
                      return "Bienvenida, $nombre";
                  }

                  echo entrar($db, 'iara', 'cuaderno-azul-12') . "\\n";
                  echo entrar($db, 'iara', 'gaviota') . "\\n";
                  echo entrar($db, 'pico', 'kia') . "\\n";
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
                  $db->exec('CREATE TABLE usuario (nombre TEXT PRIMARY KEY, huella TEXT, rol TEXT)');
                  $db->prepare('INSERT INTO usuario VALUES (?, ?, ?)')->execute(['iara', password_hash('cuaderno-azul-12', PASSWORD_DEFAULT), 'escribiente']);

                  function entrar(PDO $db, string $nombre, string $clave): string
                  {
                      $c = $db->prepare('SELECT huella, rol FROM usuario WHERE nombre = ?');
                      $c->execute([$nombre]);
                      $u = $c->fetch();
                      if ($u === false || !password_verify($clave, $u['huella'])) {
                          return "Usuario o clave incorrectos";
                      }
                      return "Bienvenida, $nombre ({$u['rol']})";
                  }

                  echo entrar($db, 'iara', 'cuaderno-azul-12') . "\\n";
                  echo entrar($db, 'iara', 'gaviota') . "\\n";
                  echo entrar($db, 'pico', 'kia') . "\\n";
              ''',
              al_superar="Iara entra con su rol de escribiente. Pico, que no tiene usuario, recibe el mismo mensaje que una clave mala: así no se entera de quién existe.",
              imagen=["La puerta de la bodega con una cerradura de bronce que tiene forma de huella dactilar.",
                      IARA + " apoya la mano en la cerradura.", NILO + " detrás, con el farol.", PICO + " en un estante, mirando.", GHECO + " sobre la cerradura."]),
        ],
    },
    {
        "titulo": "R04-N09 · Jefe: la Serpiente Marina de las Tablas",
        "misiones": [
            m(id="R04-N09-P1", titulo="El stock que se vende dos veces",
              lugar=SOTANO, personajes="Nilo, Fermín, Gheco",
              criatura="dragon",
              carta="Stock seguro | UPDATE producto SET stock = stock - ? WHERE id = ? AND stock >= ? · si rowCount() es 0, no alcanzaba · nada de leer y después restar",
              recompensa="xp 15, oro 15",
              escena="""
                  En lo más hondo de la Bodega vive la **Serpiente Marina de las Tablas**. Se alimenta del stock que se vende dos veces: dos clientes compraron la última cadena al mismo tiempo, y los dos se la llevaron. Fermín sube los pies a una silla.
              """,
              sugiere="En vez de leer el stock y después restar, que la misma consulta reste **solo si alcanza**: `… WHERE id = ? AND stock >= ?`. Si `rowCount()` da 0, no había.",
              desafio="Hacé que la venta no deje el stock en negativo.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE producto (id INTEGER PRIMARY KEY, nombre TEXT, stock INTEGER)');
                  $db->exec("INSERT INTO producto VALUES (1, 'cadena', 1)");

                  function vender(PDO $db, int $id, int $cantidad): string
                  {
                      $db->prepare('UPDATE producto SET stock = stock - ? WHERE id = ?')->execute([$cantidad, $id]);
                      return "Vendido";
                  }

                  echo vender($db, 1, 1) . "\\n";
                  echo vender($db, 1, 1) . "\\n";
                  echo "Stock: " . $db->query('SELECT stock FROM producto WHERE id = 1')->fetchColumn() . "\\n";
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE producto (id INTEGER PRIMARY KEY, nombre TEXT, stock INTEGER)');
                  $db->exec("INSERT INTO producto VALUES (1, 'cadena', 1)");

                  function vender(PDO $db, int $id, int $cantidad): string
                  {
                      $c = $db->prepare('UPDATE producto SET stock = stock - ? WHERE id = ? AND stock >= ?');
                      $c->execute([$cantidad, $id, $cantidad]);
                      return $c->rowCount() === 1 ? "Vendido" : "Sin stock";
                  }

                  echo vender($db, 1, 1) . "\\n";
                  echo vender($db, 1, 1) . "\\n";
                  echo "Stock: " . $db->query('SELECT stock FROM producto WHERE id = 1')->fetchColumn() . "\\n";
              ''',
              al_superar="La última cadena se vende una sola vez. La Serpiente pierde una escama del lomo, que brilla y se apaga.",
              imagen=["Un sótano de piedra inundado con agua oscura y estanterías de fichas a medio sumergir.",
                      SERPIENTE + " asoma del agua.", FERMIN + " parado sobre una silla.", NILO + " con un rollo de cadena en la mano.", GHECO + " sobre una estantería."]),
            m(id="R04-N09-P2", titulo="El precio de ese día",
              lugar=SOTANO, personajes="Nilo, Iara, Gheco",
              criatura="dragon",
              carta="Conservar la historia | el pedido guarda el precio del momento · si mañana cambia el precio, el pedido viejo no cambia · se copia, no se apunta",
              recompensa="xp 15, oro 15",
              escena="""
                  La Serpiente cambió el precio de la sal y, de golpe, todos los pedidos viejos de sal costaban otra cosa. Iara tiene los recibos de papel y no coinciden con la bodega.
              """,
              sugiere="El pedido guarda su propio `precio_unitario` al momento de comprar. El total se calcula con ese, no con el precio actual del producto.",
              desafio="Guardá el precio en el pedido y calculá con él.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE producto (id INTEGER PRIMARY KEY, nombre TEXT, precio INTEGER)');
                  $db->exec('CREATE TABLE pedido (id INTEGER PRIMARY KEY, producto_id INTEGER, cantidad INTEGER)');
                  $db->exec("INSERT INTO producto VALUES (1, 'sal', 10)");
                  $db->exec('INSERT INTO pedido (producto_id, cantidad) VALUES (1, 3)');
                  $db->exec('UPDATE producto SET precio = 25 WHERE id = 1');

                  $sql = 'SELECT pedido.cantidad * producto.precio FROM pedido JOIN producto ON producto.id = pedido.producto_id';
                  echo "Pedido 1: " . $db->query($sql)->fetchColumn() . " sellos\\n";
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE producto (id INTEGER PRIMARY KEY, nombre TEXT, precio INTEGER)');
                  $db->exec('CREATE TABLE pedido (id INTEGER PRIMARY KEY, producto_id INTEGER, cantidad INTEGER, precio_unitario INTEGER)');
                  $db->exec("INSERT INTO producto VALUES (1, 'sal', 10)");
                  $db->exec('INSERT INTO pedido (producto_id, cantidad, precio_unitario) SELECT id, 3, precio FROM producto WHERE id = 1');
                  $db->exec('UPDATE producto SET precio = 25 WHERE id = 1');

                  $sql = 'SELECT cantidad * precio_unitario FROM pedido WHERE id = 1';
                  echo "Pedido 1: " . $db->query($sql)->fetchColumn() . " sellos\\n";
              ''',
              al_superar="El recibo de Iara y la bodega dicen lo mismo: 30 sellos, como ese día. Otra escama de la Serpiente se apaga.",
              imagen=["Un recibo de papel viejo flotando en el agua del sótano, con un sello de lacre intacto.",
                      IARA + " rescata el recibo.", NILO + " le alumbra con el farol.", GHECO + " sobre el recibo."]),
            m(id="R04-N09-P3", titulo="Al fondo del mar",
              lugar=SOTANO, personajes="Nilo, Fermín, Elefa, Gheco",
              criatura="dragon",
              carta="Todo junto | tablas con claves y restricciones · consultas preparadas · transacción para la compra · stock que no se vende dos veces · precio copiado",
              recompensa="xp 25, oro 30", item="Llave de la Bodega",
              escena="""
                  La Serpiente se enrosca alrededor de los sistemas que Nilo armó en la Oficina: con muchos usuarios a la vez, los archivos JSON se pisan. Nilo tiene que llevarlos a la Bodega con todo lo que aprendió, en una sola compra que no pueda salir a medias.
              """,
              sugiere="`comprar()` hace todo en una transacción: resta el stock solo si alcanza, guarda el pedido con el precio del momento y, si algo falla, `rollBack()`.",
              desafio="Completá `comprar` y probala con las tres compras.",
              inicial='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE producto (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, precio INTEGER NOT NULL, stock INTEGER NOT NULL CHECK (stock >= 0))');
                  $db->exec('CREATE TABLE pedido (id INTEGER PRIMARY KEY, producto_id INTEGER NOT NULL REFERENCES producto(id), cantidad INTEGER NOT NULL, precio_unitario INTEGER NOT NULL)');
                  $db->exec("INSERT INTO producto VALUES (1, 'farol', 40, 2), (2, 'cadena', 15, 10)");

                  function comprar(PDO $db, int $producto, int $cantidad): string
                  {
                      return "?";
                  }

                  echo comprar($db, 1, 2) . "\\n";
                  echo comprar($db, 1, 1) . "\\n";
                  echo comprar($db, 2, 3) . "\\n";
                  echo "Pedidos: " . $db->query('SELECT COUNT(*) FROM pedido')->fetchColumn() . "\\n";
                  echo "Faroles: " . $db->query('SELECT stock FROM producto WHERE id = 1')->fetchColumn() . "\\n";
              ''',
              solucion='''
                  <?php
                  $db = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
                  $db->exec('CREATE TABLE producto (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, precio INTEGER NOT NULL, stock INTEGER NOT NULL CHECK (stock >= 0))');
                  $db->exec('CREATE TABLE pedido (id INTEGER PRIMARY KEY, producto_id INTEGER NOT NULL REFERENCES producto(id), cantidad INTEGER NOT NULL, precio_unitario INTEGER NOT NULL)');
                  $db->exec("INSERT INTO producto VALUES (1, 'farol', 40, 2), (2, 'cadena', 15, 10)");

                  function comprar(PDO $db, int $producto, int $cantidad): string
                  {
                      $db->beginTransaction();
                      try {
                          $resta = $db->prepare('UPDATE producto SET stock = stock - ? WHERE id = ? AND stock >= ?');
                          $resta->execute([$cantidad, $producto, $cantidad]);
                          if ($resta->rowCount() === 0) {
                              $db->rollBack();
                              return "Sin stock para el producto $producto";
                          }
                          $db->prepare('INSERT INTO pedido (producto_id, cantidad, precio_unitario) SELECT id, ?, precio FROM producto WHERE id = ?')
                              ->execute([$cantidad, $producto]);
                          $db->commit();
                          return "Pedido " . $db->lastInsertId() . " confirmado";
                      } catch (Throwable $e) {
                          $db->rollBack();
                          return "Fallo la compra";
                      }
                  }

                  echo comprar($db, 1, 2) . "\\n";
                  echo comprar($db, 1, 1) . "\\n";
                  echo comprar($db, 2, 3) . "\\n";
                  echo "Pedidos: " . $db->query('SELECT COUNT(*) FROM pedido')->fetchColumn() . "\\n";
                  echo "Faroles: " . $db->query('SELECT stock FROM producto WHERE id = 1')->fetchColumn() . "\\n";
              ''',
              al_superar="La Serpiente no encuentra por dónde entrar. Se desenrosca, se hunde y se va al fondo del mar, y en el agua queda flotando una llave de hierro: **la Llave de la Bodega**. Fermín baja los pies de la silla. Elefa hace sonar la campana tres veces.",
              imagen=["El sótano inundado con el agua quieta y una llave grande de hierro con la cabeza en forma de estantería flotando, con un brillo cian.",
                      NILO + " se estira para agarrar la llave.", FERMIN + " baja de la silla.", ELEFA + " en lo alto de la escalera.", GHECO + " sobre la llave."]),
        ],
    },
]
