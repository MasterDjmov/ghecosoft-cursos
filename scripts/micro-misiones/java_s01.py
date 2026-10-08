from genjava import m

# S01: la Bóveda Imperial. Las de SQL (lenguaje="sql") corren con SQLite en el navegador: la sintaxis básica es la
# misma que en PostgreSQL; donde cambia (triggers, tipos), la pista lo avisa. Las de archivos, JDBC y DAO siguen
# en Java, con la conexión imitada (la base de verdad se usa en las prácticas que corrige el docente).

NODOS = [
    {
        "titulo": "S01-N01 · Archivos de texto, CSV y .properties",
        "misiones": [
            m(id="S01-N01-P1", titulo="Lo que queda escrito",
              lugar="El primer piso de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Files | Files.writeString(ruta, texto) escribe · Files.readAllLines(ruta) lee línea por línea · lo que queda en un archivo sobrevive",
              recompensa="xp 10, oro 10",
              escena="""
                  Debajo de los Archivos, una escalera de piedra baja a la **Bóveda Imperial**. En el primer piso, los escribas copian registros en libros. —Hasta ahora tus programas olvidaban todo al terminar —dice Kaffa—. Lo que queda en un **archivo** sobrevive.
              """,
              sugiere="`Files.writeString(ruta, texto)` escribe un archivo entero y `Files.readAllLines(ruta)` lo lee como una lista de líneas. Para probar, se usa un archivo temporal y se borra al final.",
              desafio="Leé las líneas del archivo.",
              inicial='''
                  import java.nio.file.Files;
                  import java.nio.file.Path;
                  import java.util.List;

                  public class Escribas {
                      public static void main(String[] args) throws Exception {
                          Path ruta = Files.createTempFile("registro", ".txt");
                          Files.writeString(ruta, "Zed;19\\nNadia;19\\nBaldo;55\\n");
                          List<String> lineas = ___;
                          System.out.println("Registros: " + lineas.size());
                          for (String l : lineas) {
                              System.out.println("- " + l.replace(";", ", ") + " años");
                          }
                          Files.delete(ruta);
                      }
                  }
              ''',
              solucion='''
                  import java.nio.file.Files;
                  import java.nio.file.Path;
                  import java.util.List;

                  public class Escribas {
                      public static void main(String[] args) throws Exception {
                          Path ruta = Files.createTempFile("registro", ".txt");
                          Files.writeString(ruta, "Zed;19\\nNadia;19\\nBaldo;55\\n");
                          List<String> lineas = Files.readAllLines(ruta);
                          System.out.println("Registros: " + lineas.size());
                          for (String l : lineas) {
                              System.out.println("- " + l.replace(";", ", ") + " años");
                          }
                          Files.delete(ruta);
                      }
                  }
              ''',
              al_superar="Tres registros, escritos y leídos. Los escribas de la Bóveda asienten: por fin alguien guarda las cosas.",
              imagen=["La escalera de piedra que baja a la Bóveda Imperial, con antorchas.",
                      "Escribas copiando registros en libros enormes; Zed con un pergamino en la mano."]),
            m(id="S01-N01-P2", titulo="El CSV con líneas rotas",
              lugar="El primer piso de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="goblin",
              carta="CSV | cada línea: datos separados por comas · se valida cada una: cantidad de partes y números que sean números · las rotas se reportan, no cortan todo",
              recompensa="xp 15, oro 15",
              escena="""
                  Un **goblin** metió líneas rotas en el inventario de la Bóveda: una sin cantidad, otra con letras donde van números. —Leé siempre como si alguien hubiera escrito mal —dice Kaffa.
              """,
              sugiere="Cada línea se corta con `split(\",\")`. Si no tiene 3 partes, o la cantidad no es un número, se reporta y se sigue con la próxima. `Integer.parseInt` lanza `NumberFormatException` si el texto no es un número.",
              desafio="Completá la condición de línea incompleta: no tiene 3 partes.",
              inicial='''
                  public class Inventario {
                      public static void main(String[] args) {
                          String[] csv = {"sal,30,Puerto", "café,abc,Capital", "seda,5", "vino,12,Torre"};
                          int total = 0;
                          for (String linea : csv) {
                              String[] p = linea.split(",");
                              if (___) {
                                  System.out.println("Incompleta: " + linea);
                                  continue;
                              }
                              try {
                                  total += Integer.parseInt(p[1]);
                              } catch (NumberFormatException e) {
                                  System.out.println("Cantidad inválida: " + linea);
                              }
                          }
                          System.out.println("Total válido: " + total);
                      }
                  }
              ''',
              solucion='''
                  public class Inventario {
                      public static void main(String[] args) {
                          String[] csv = {"sal,30,Puerto", "café,abc,Capital", "seda,5", "vino,12,Torre"};
                          int total = 0;
                          for (String linea : csv) {
                              String[] p = linea.split(",");
                              if (p.length != 3) {
                                  System.out.println("Incompleta: " + linea);
                                  continue;
                              }
                              try {
                                  total += Integer.parseInt(p[1]);
                              } catch (NumberFormatException e) {
                                  System.out.println("Cantidad inválida: " + linea);
                              }
                          }
                          System.out.println("Total válido: " + total);
                      }
                  }
              ''',
              al_superar="Dos líneas reportadas y cuarenta y dos unidades válidas. El goblin se va sin haber roto nada.",
              imagen=["Un libro de inventario con dos renglones marcados en rojo y el resto en verde.",
                      "Un goblin escapando con una pluma manchada."]),
            m(id="S01-N01-P3", titulo="La configuración de la Bóveda",
              lugar="El primer piso de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              carta=".properties | Properties: claves y valores · setProperty y store(…) guardan · load(…) lee · getProperty(clave, porDefecto)",
              recompensa="xp 15, oro 15",
              escena="""
                  La Bóveda tiene sus ajustes: cuántos escribas trabajan y a qué hora cierra. Los guarda en un archivo de configuración, para que no haya que tocar el programa.
              """,
              sugiere="`Properties` guarda pares `clave=valor`: `setProperty` los carga, `store` los escribe y `load` los lee. `getProperty(\"clave\", \"porDefecto\")` da un valor por defecto si la clave no está.",
              desafio="Leé la hora de cierre con un valor por defecto de \"20\".",
              inicial='''
                  import java.io.StringReader;
                  import java.io.StringWriter;
                  import java.util.Properties;

                  public class Ajustes {
                      public static void main(String[] args) throws Exception {
                          Properties guardar = new Properties();
                          guardar.setProperty("escribas", "4");
                          StringWriter archivo = new StringWriter();
                          guardar.store(archivo, null);

                          Properties leer = new Properties();
                          leer.load(new StringReader(archivo.toString()));
                          System.out.println("Escribas: " + leer.getProperty("escribas"));
                          System.out.println("Cierra a las: " + ___);
                      }
                  }
              ''',
              solucion='''
                  import java.io.StringReader;
                  import java.io.StringWriter;
                  import java.util.Properties;

                  public class Ajustes {
                      public static void main(String[] args) throws Exception {
                          Properties guardar = new Properties();
                          guardar.setProperty("escribas", "4");
                          StringWriter archivo = new StringWriter();
                          guardar.store(archivo, null);

                          Properties leer = new Properties();
                          leer.load(new StringReader(archivo.toString()));
                          System.out.println("Escribas: " + leer.getProperty("escribas"));
                          System.out.println("Cierra a las: " + leer.getProperty("cierre", "20"));
                      }
                  }
              ''',
              al_superar="""
                  Cuatro escribas y, como nadie configuró el cierre, a las 20. —Los archivos se corrompen y se llenan —dice Kaffa—. Para lo que importa de verdad, abajo hay **tablas**.
              """,
              imagen=["Un archivo de configuración colgado en la pared de la Bóveda: «escribas=4».",
                      "Kaffa señalando hacia una escalera que baja aún más."]),
        ],
    },
    {
        "titulo": "S01-N02 · SQL: tablas, restricciones y ABM",
        "misiones": [
            m(id="S01-N02-P1", titulo="La primera tabla",
              lugar="El segundo piso de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              lenguaje="sql",
              carta="CREATE TABLE e INSERT | CREATE TABLE viajero (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL) · INSERT INTO viajero (nombre) VALUES ('Zed') · SELECT * FROM viajero",
              recompensa="xp 10, oro 10",
              escena="""
                  En el segundo piso, los registros no están en libros: están en **tablas**, con columnas y filas. Zed escribe su primera tabla. —Esto corre en tu navegador —dice Gheco—, con SQLite. En el curso usás PostgreSQL, pero lo básico se escribe igual.
              """,
              sugiere="`CREATE TABLE` define las columnas y sus tipos. `INSERT INTO tabla (columnas) VALUES (…)` agrega una fila. `SELECT * FROM tabla` muestra todo. Cada sentencia termina con `;`.",
              desafio="Agregá a Baldo, de 55 años, con un `INSERT`.",
              inicial='''
                  CREATE TABLE viajero (
                      id INTEGER PRIMARY KEY,
                      nombre TEXT NOT NULL,
                      edad INTEGER
                  );
                  INSERT INTO viajero (nombre, edad) VALUES ('Zed', 19);
                  INSERT INTO viajero (nombre, edad) VALUES ('Nadia', 19);
                  ___;
                  SELECT * FROM viajero;
              ''',
              solucion='''
                  CREATE TABLE viajero (
                      id INTEGER PRIMARY KEY,
                      nombre TEXT NOT NULL,
                      edad INTEGER
                  );
                  INSERT INTO viajero (nombre, edad) VALUES ('Zed', 19);
                  INSERT INTO viajero (nombre, edad) VALUES ('Nadia', 19);
                  INSERT INTO viajero (nombre, edad) VALUES ('Baldo', 55);
                  SELECT * FROM viajero;
              ''',
              al_superar="Tres filas, cada una con su id puesto por la base. —Ni un escriba —dice Nadia—, y todo en orden.",
              imagen=["Una tabla de piedra con columnas talladas (id, nombre, edad) y tres filas encendidas.",
                      "Zed escribiendo SQL en una losa luminosa."]),
            m(id="S01-N02-P2", titulo="Lo que se pone solo",
              lugar="El segundo piso de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              lenguaje="sql",
              carta="Restricciones | PRIMARY KEY · NOT NULL · UNIQUE · CHECK (stock >= 0) · DEFAULT 'Puerto': el valor que va si no se dice",
              recompensa="xp 10, oro 10",
              escena="""
                  En la tabla de cargamentos, casi todo sale del Puerto. —Que la tabla lo ponga sola —dice Kaffa—. Y que no acepte stock negativo: las **restricciones** protegen los datos aunque alguien se equivoque.
              """,
              sugiere="`DEFAULT 'Puerto'` pone ese valor si el `INSERT` no dice el origen. `CHECK (stock >= 0)` rechaza los negativos. Las restricciones van en la definición de cada columna.",
              desafio="Completá el valor por defecto del origen: 'Puerto'.",
              inicial='''
                  CREATE TABLE cargamento (
                      id INTEGER PRIMARY KEY,
                      descripcion TEXT NOT NULL UNIQUE,
                      stock INTEGER NOT NULL CHECK (stock >= 0),
                      origen TEXT NOT NULL ___
                  );
                  INSERT INTO cargamento (descripcion, stock) VALUES ('sal', 30);
                  INSERT INTO cargamento (descripcion, stock, origen) VALUES ('vidrios', 4, 'Talleres');
                  SELECT descripcion, stock, origen FROM cargamento;
              ''',
              solucion='''
                  CREATE TABLE cargamento (
                      id INTEGER PRIMARY KEY,
                      descripcion TEXT NOT NULL UNIQUE,
                      stock INTEGER NOT NULL CHECK (stock >= 0),
                      origen TEXT NOT NULL DEFAULT 'Puerto'
                  );
                  INSERT INTO cargamento (descripcion, stock) VALUES ('sal', 30);
                  INSERT INTO cargamento (descripcion, stock, origen) VALUES ('vidrios', 4, 'Talleres');
                  SELECT descripcion, stock, origen FROM cargamento;
              ''',
              al_superar="La sal sale del Puerto sin que nadie lo escriba; los vidrios, de los Talleres. —¿Talleres? —pregunta Zed—. Ahí hacen vitrales. —Ahí los hacía el Vidriero —dice Kaffa, y no agrega nada.",
              imagen=["Una columna de la tabla con un sello que dice «DEFAULT Puerto».",
                      "Kaffa pensativo frente a la palabra «Talleres»."]),
            m(id="S01-N02-P3", titulo="Altas, bajas y modificaciones",
              lugar="El segundo piso de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              lenguaje="sql",
              criatura="ogro",
              carta="ABM | INSERT da de alta · UPDATE … SET … WHERE modifica · DELETE FROM … WHERE borra · sin WHERE, ¡todas las filas!",
              recompensa="xp 15, oro 15",
              escena="""
                  Llega mercadería nueva y se vende otra. Un **ogro** le sugiere a Zed un `UPDATE` sin `WHERE`, «más rápido». Kaffa lo frena: sin `WHERE`, cambia **todas** las filas.
              """,
              sugiere="`UPDATE cargamento SET stock = stock - 10 WHERE descripcion = 'sal'` cambia solo esa fila. `DELETE FROM cargamento WHERE stock = 0` borra solo las vacías. El `WHERE` es lo que importa.",
              desafio="Completá el `WHERE` del `UPDATE`: solo la sal.",
              inicial='''
                  CREATE TABLE cargamento (id INTEGER PRIMARY KEY, descripcion TEXT NOT NULL, stock INTEGER NOT NULL);
                  INSERT INTO cargamento (descripcion, stock) VALUES ('sal', 30), ('café', 0), ('seda', 8);
                  UPDATE cargamento SET stock = stock - 10 WHERE ___;
                  DELETE FROM cargamento WHERE stock = 0;
                  SELECT descripcion, stock FROM cargamento;
              ''',
              solucion='''
                  CREATE TABLE cargamento (id INTEGER PRIMARY KEY, descripcion TEXT NOT NULL, stock INTEGER NOT NULL);
                  INSERT INTO cargamento (descripcion, stock) VALUES ('sal', 30), ('café', 0), ('seda', 8);
                  UPDATE cargamento SET stock = stock - 10 WHERE descripcion = 'sal';
                  DELETE FROM cargamento WHERE stock = 0;
                  SELECT descripcion, stock FROM cargamento;
              ''',
              al_superar="La sal baja a 20, el café vacío desaparece y la seda queda intacta. El ogro se queda sin su desastre.",
              imagen=["Una tabla de piedra donde una fila se borra sola y otra cambia de número.",
                      "Un ogro con un `UPDATE` sin `WHERE` en la mano, frenado por Kaffa."]),
        ],
    },
    {
        "titulo": "S01-N03 · SQL: consultas, JOIN y vistas",
        "misiones": [
            m(id="S01-N03-P1", titulo="Buscar en la tabla",
              lugar="El tercer piso de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              lenguaje="sql",
              carta="SELECT con filtros | WHERE condición · ORDER BY columna DESC · LIMIT n · LIKE 'A%' para empezar con A",
              recompensa="xp 10, oro 10",
              escena="""
                  En el tercer piso, la Oráculo de las Tablas responde preguntas. Zed le pregunta por los tres viajeros más grandes que llegaron del Puerto.
              """,
              sugiere="`WHERE origen = 'Puerto'` filtra, `ORDER BY edad DESC` ordena de mayor a menor y `LIMIT 3` se queda con los primeros tres.",
              desafio="Completá el orden: de mayor a menor edad.",
              inicial='''
                  CREATE TABLE viajero (nombre TEXT, edad INTEGER, origen TEXT);
                  INSERT INTO viajero VALUES ('Zed', 19, 'Puerto'), ('Nadia', 19, 'Aduana'), ('Baldo', 55, 'Puerto'),
                      ('Teo', 17, 'Puerto'), ('Sor Ana', 62, 'Puerto'), ('Mira', 20, 'Academia');
                  SELECT nombre, edad FROM viajero
                  WHERE origen = 'Puerto'
                  ORDER BY ___
                  LIMIT 3;
              ''',
              solucion='''
                  CREATE TABLE viajero (nombre TEXT, edad INTEGER, origen TEXT);
                  INSERT INTO viajero VALUES ('Zed', 19, 'Puerto'), ('Nadia', 19, 'Aduana'), ('Baldo', 55, 'Puerto'),
                      ('Teo', 17, 'Puerto'), ('Sor Ana', 62, 'Puerto'), ('Mira', 20, 'Academia');
                  SELECT nombre, edad FROM viajero
                  WHERE origen = 'Puerto'
                  ORDER BY edad DESC
                  LIMIT 3;
              ''',
              al_superar="Sor Ana, Baldo y Zed. La Oráculo responde sin abrir un solo libro.",
              imagen=["El tercer piso de la Bóveda: una Oráculo de túnica gris frente a una tabla luminosa que responde.",
                      "Tres nombres brillando en orden: Sor Ana, Baldo, Zed."]),
            m(id="S01-N03-P2", titulo="Cuántos de cada uno",
              lugar="El tercer piso de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              lenguaje="sql",
              carta="GROUP BY y HAVING | COUNT(*), SUM(…), AVG(…) por grupo · HAVING filtra GRUPOS (WHERE filtra filas)",
              recompensa="xp 15, oro 15",
              escena="""
                  La Oráculo quiere saber de qué lugares llegó más de un viajero, y cuántos. —Agrupá —dice Gheco—, y después filtrá los grupos.
              """,
              sugiere="`GROUP BY origen` arma un grupo por lugar y `COUNT(*)` cuenta las filas de cada uno. Para quedarse con los grupos de más de uno, `HAVING COUNT(*) > 1` (el `WHERE` no sirve para eso: filtra filas, no grupos).",
              desafio="Completá el filtro de grupos: más de un viajero.",
              inicial='''
                  CREATE TABLE viajero (nombre TEXT, edad INTEGER, origen TEXT);
                  INSERT INTO viajero VALUES ('Zed', 19, 'Puerto'), ('Nadia', 19, 'Aduana'), ('Baldo', 55, 'Puerto'),
                      ('Teo', 17, 'Academia'), ('Sor Ana', 62, 'Puerto'), ('Mira', 20, 'Academia');
                  SELECT origen, COUNT(*) AS viajeros, MAX(edad) AS mayor
                  FROM viajero
                  GROUP BY origen
                  ___
                  ORDER BY viajeros DESC;
              ''',
              solucion='''
                  CREATE TABLE viajero (nombre TEXT, edad INTEGER, origen TEXT);
                  INSERT INTO viajero VALUES ('Zed', 19, 'Puerto'), ('Nadia', 19, 'Aduana'), ('Baldo', 55, 'Puerto'),
                      ('Teo', 17, 'Academia'), ('Sor Ana', 62, 'Puerto'), ('Mira', 20, 'Academia');
                  SELECT origen, COUNT(*) AS viajeros, MAX(edad) AS mayor
                  FROM viajero
                  GROUP BY origen
                  HAVING COUNT(*) > 1
                  ORDER BY viajeros DESC;
              ''',
              al_superar="Tres del Puerto, dos de la Academia. La Aduana queda afuera: solo llegó Nadia, y ella ya estaba.",
              imagen=["Viajeros de luz agrupándose por lugar de origen en tres círculos.",
                      "Nadia sola en su círculo, encogiéndose de hombros."]),
            m(id="S01-N03-P3", titulo="Cruzar dos tablas",
              lugar="El tercer piso de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              lenguaje="sql",
              carta="JOIN | SELECT … FROM barco b JOIN cargamento c ON c.barco_id = b.id · une cada cargamento con SU barco · LEFT JOIN conserva los que no tienen pareja",
              recompensa="xp 15, oro 20",
              escena="""
                  Los barcos están en una tabla y los cargamentos en otra. La Oráculo pide cada cargamento con el nombre de su barco. —Las tablas se cruzan por la **clave foránea** —dice Kaffa.
              """,
              sugiere="`JOIN cargamento c ON c.barco_id = b.id` une cada cargamento con el barco cuyo `id` coincide. Con `LEFT JOIN`, los barcos sin cargamentos también aparecen, con `NULL`.",
              desafio="Completá la condición del `JOIN`: el barco del cargamento.",
              inicial='''
                  CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT);
                  CREATE TABLE cargamento (id INTEGER PRIMARY KEY, descripcion TEXT, barco_id INTEGER REFERENCES barco(id));
                  INSERT INTO barco VALUES (1, 'Garza'), (2, 'Bagre'), (3, 'Ceibo');
                  INSERT INTO cargamento (descripcion, barco_id) VALUES ('café', 1), ('sal', 2), ('vidrios', 1);
                  SELECT b.nombre AS barco, c.descripcion AS carga
                  FROM barco b
                  LEFT JOIN cargamento c ON ___
                  ORDER BY b.id, c.id;
              ''',
              solucion='''
                  CREATE TABLE barco (id INTEGER PRIMARY KEY, nombre TEXT);
                  CREATE TABLE cargamento (id INTEGER PRIMARY KEY, descripcion TEXT, barco_id INTEGER REFERENCES barco(id));
                  INSERT INTO barco VALUES (1, 'Garza'), (2, 'Bagre'), (3, 'Ceibo');
                  INSERT INTO cargamento (descripcion, barco_id) VALUES ('café', 1), ('sal', 2), ('vidrios', 1);
                  SELECT b.nombre AS barco, c.descripcion AS carga
                  FROM barco b
                  LEFT JOIN cargamento c ON c.barco_id = b.id
                  ORDER BY b.id, c.id;
              ''',
              al_superar="""
                  La Garza lleva café y vidrios, el Bagre sal… y el Ceibo, nada: `NULL`. Zed sabe por qué: lo que llevaba era un vitral, y está en la Torre.
                  En el piso de abajo, la Bóveda tiene mecanismos que trabajan solos.
              """,
              imagen=["Dos tablas de piedra unidas por hilos de luz: barcos de un lado, cargamentos del otro; el Ceibo sin hilo.",
                      "Zed mirando la fila del Ceibo con un NULL brillando."]),
        ],
    },
    {
        "titulo": "S01-N04 · SQL: funciones, procedimientos, triggers y roles",
        "misiones": [
            m(id="S01-N04-P1", titulo="Las funciones de la base",
              lugar="El cuarto piso de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              lenguaje="sql",
              carta="Funciones | UPPER(texto) · LENGTH(texto) · ROUND(número, 2) · COALESCE(a, b): el primero que no es NULL",
              recompensa="xp 10, oro 10",
              escena="""
                  En el cuarto piso, la base trabaja sola: pasa nombres a mayúsculas, redondea precios y completa lo que falta. Zed quiere el listado de viajeros con el oficio, y donde no hay oficio, «sin oficio».
              """,
              sugiere="`COALESCE(oficio, 'sin oficio')` devuelve el oficio, o el texto por defecto si es `NULL`. `UPPER` pasa a mayúsculas. Estas funciones existen igual en PostgreSQL.",
              desafio="Completá el `COALESCE` para los que no tienen oficio.",
              inicial='''
                  CREATE TABLE viajero (nombre TEXT, oficio TEXT, deuda REAL);
                  INSERT INTO viajero VALUES ('Zed', NULL, 12.456), ('Nadia', 'aduanera', 0), ('Baldo', 'mercader', 99.999);
                  SELECT UPPER(nombre) AS nombre, ___ AS oficio, ROUND(deuda, 2) AS deuda
                  FROM viajero;
              ''',
              solucion='''
                  CREATE TABLE viajero (nombre TEXT, oficio TEXT, deuda REAL);
                  INSERT INTO viajero VALUES ('Zed', NULL, 12.456), ('Nadia', 'aduanera', 0), ('Baldo', 'mercader', 99.999);
                  SELECT UPPER(nombre) AS nombre, COALESCE(oficio, 'sin oficio') AS oficio, ROUND(deuda, 2) AS deuda
                  FROM viajero;
              ''',
              al_superar="ZED, sin oficio. —Por ahora —dice Zed—. Aprendiz no cuenta.",
              imagen=["Una tabla donde un NULL se transforma en «sin oficio» al pasar por un engranaje.",
                      "Zed leyendo su fila con resignación divertida."]),
            m(id="S01-N04-P2", titulo="Según el caso",
              lugar="El cuarto piso de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              lenguaje="sql",
              carta="CASE | CASE WHEN condición THEN valor … ELSE otro END · como un if adentro de la consulta",
              recompensa="xp 15, oro 15",
              escena="""
                  La Bóveda clasifica los cargamentos por peso: liviano, mediano o pesado, sin que nadie lo calcule a mano.
              """,
              sugiere="`CASE WHEN kilos > 100 THEN 'pesado' WHEN kilos > 30 THEN 'mediano' ELSE 'liviano' END` evalúa en orden, como los `else if`. Lo más exigente va primero.",
              desafio="Completá el caso mediano: más de 30 kilos.",
              inicial='''
                  CREATE TABLE cargamento (descripcion TEXT, kilos INTEGER);
                  INSERT INTO cargamento VALUES ('sal', 120), ('café', 40), ('vidrios', 8);
                  SELECT descripcion,
                         CASE WHEN kilos > 100 THEN 'pesado'
                              ___
                              ELSE 'liviano' END AS clase
                  FROM cargamento;
              ''',
              solucion='''
                  CREATE TABLE cargamento (descripcion TEXT, kilos INTEGER);
                  INSERT INTO cargamento VALUES ('sal', 120), ('café', 40), ('vidrios', 8);
                  SELECT descripcion,
                         CASE WHEN kilos > 100 THEN 'pesado'
                              WHEN kilos > 30 THEN 'mediano'
                              ELSE 'liviano' END AS clase
                  FROM cargamento;
              ''',
              al_superar="Pesado, mediano, liviano. —Es el orden de los portones de la Aduana —recuerda Nadia—. Lo más exigente primero.",
              imagen=["Tres cargamentos cayendo por tres rampas según su peso.",
                      "Nadia recordando los portones de la Aduana."]),
            m(id="S01-N04-P3", titulo="El mecanismo que reacciona",
              lugar="El cuarto piso de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              lenguaje="sql",
              carta="Trigger | CREATE TRIGGER … AFTER INSERT ON venta … BEGIN UPDATE … END · la base reacciona sola a un cambio",
              recompensa="xp 15, oro 20",
              escena="""
                  Cada vez que se vende algo, alguien tiene que acordarse de bajar el stock. En la Bóveda no hace falta: un **trigger** reacciona solo a cada venta.
              """,
              sugiere="Un trigger se dispara con un `INSERT`, `UPDATE` o `DELETE`. Adentro, `NEW` es la fila que acaba de entrar: `UPDATE producto SET stock = stock - NEW.cantidad WHERE id = NEW.producto_id`. En PostgreSQL se escribe distinto (una función PL/pgSQL y después el trigger), pero la idea es la misma.",
              desafio="Completá el `UPDATE` del trigger: restá la cantidad vendida.",
              inicial='''
                  CREATE TABLE producto (id INTEGER PRIMARY KEY, nombre TEXT, stock INTEGER);
                  CREATE TABLE venta (id INTEGER PRIMARY KEY, producto_id INTEGER, cantidad INTEGER);
                  CREATE TRIGGER bajar_stock AFTER INSERT ON venta
                  BEGIN
                      UPDATE producto SET stock = ___ WHERE id = NEW.producto_id;
                  END;
                  INSERT INTO producto VALUES (1, 'Café Fuerte', 20), (2, 'Capa de Viajero', 5);
                  INSERT INTO venta (producto_id, cantidad) VALUES (1, 3), (2, 1), (1, 2);
                  SELECT nombre, stock FROM producto;
              ''',
              solucion='''
                  CREATE TABLE producto (id INTEGER PRIMARY KEY, nombre TEXT, stock INTEGER);
                  CREATE TABLE venta (id INTEGER PRIMARY KEY, producto_id INTEGER, cantidad INTEGER);
                  CREATE TRIGGER bajar_stock AFTER INSERT ON venta
                  BEGIN
                      UPDATE producto SET stock = stock - NEW.cantidad WHERE id = NEW.producto_id;
                  END;
                  INSERT INTO producto VALUES (1, 'Café Fuerte', 20), (2, 'Capa de Viajero', 5);
                  INSERT INTO venta (producto_id, cantidad) VALUES (1, 3), (2, 1), (1, 2);
                  SELECT nombre, stock FROM producto;
              ''',
              al_superar="""
                  Quince cafés y cuatro capas, sin que nadie bajara el stock a mano. Baldo, que vende esos mismos productos, pide una copia del trigger.
                  En el piso de abajo, una puerta de hierro dice «JDBC»: por ahí entran los programas de Java.
              """,
              imagen=["Un mecanismo de engranajes que baja un contador de stock cada vez que pasa una venta.",
                      "Baldo pidiendo una copia con entusiasmo."]),
        ],
    },
    {
        "titulo": "S01-N05 · JDBC: conectarse y consultar",
        "misiones": [
            m(id="S01-N05-P1", titulo="La inyección del falsificador",
              lugar="La puerta de hierro de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="dragon",
              carta="Inyección SQL | armar SQL concatenando lo que escribe el usuario deja que cambie la consulta · ' OR '1'='1 abre todo · se usa PreparedStatement con ?",
              recompensa="xp 15, oro 15",
              escena="""
                  En la puerta de hierro, un falsificador escribe como nombre `' OR '1'='1`. El programa viejo arma la consulta pegando textos y, de golpe, el falsificador ve **todos** los registros. Zed conoce el truco: lo usaba en el Puerto.
              """,
              sugiere="Si se arma la consulta con `+`, lo que escribe el usuario pasa a ser parte del SQL. Con un `PreparedStatement`, la consulta lleva `?` y el valor se manda aparte: nunca se mezcla con el código.",
              desafio="Completá la consulta segura: el nombre va como un `?`.",
              inicial='''
                  public class Inyeccion {
                      public static void main(String[] args) {
                          String nombre = "' OR '1'='1";
                          String peligrosa = "SELECT * FROM viajero WHERE nombre = '" + nombre + "'";
                          String segura = "SELECT * FROM viajero WHERE nombre = ___";
                          System.out.println("Concatenando: " + peligrosa);
                          System.out.println("Con PreparedStatement: " + segura);
                          System.out.println("Y el valor va aparte: [" + nombre + "]");
                      }
                  }
              ''',
              solucion='''
                  public class Inyeccion {
                      public static void main(String[] args) {
                          String nombre = "' OR '1'='1";
                          String peligrosa = "SELECT * FROM viajero WHERE nombre = '" + nombre + "'";
                          String segura = "SELECT * FROM viajero WHERE nombre = ?";
                          System.out.println("Concatenando: " + peligrosa);
                          System.out.println("Con PreparedStatement: " + segura);
                          System.out.println("Y el valor va aparte: [" + nombre + "]");
                      }
                  }
              ''',
              al_superar="La primera consulta trae a todos: `OR '1'='1` siempre es verdad. La segunda busca a alguien que se llame, literalmente, `' OR '1'='1`. El falsificador se va con las manos vacías. —Yo hacía eso —confiesa Zed—. Ahora sé cerrarlo.",
              imagen=["Una puerta de hierro con una cerradura de signos de pregunta (?) que rechaza una llave falsa.",
                      "Un falsificador encapuchado retirándose; Zed con los brazos cruzados."]),
            m(id="S01-N05-P2", titulo="La conexión que siempre se cierra",
              lugar="La puerta de hierro de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="try con recursos | try (Connection c = …) { … } cierra la conexión al salir, aunque haya un error · con Connection, PreparedStatement y ResultSet",
              recompensa="xp 15, oro 15",
              escena="""
                  Las conexiones a la Bóveda son pocas. Si un programa abre una y no la cierra, la puerta se traba para todos. —Con `try` con recursos —dice Gheco—, se cierra sola, pase lo que pase.
              """,
              sugiere="Todo lo que se declara entre los paréntesis del `try (...)` se cierra al salir, en orden inverso, aunque salte una excepción. Acá una conexión de juguete muestra cuándo se abre y se cierra.",
              desafio="Declará la conexión adentro de los paréntesis del `try`.",
              inicial='''
                  public class SiempreCerrada {
                      static class Conexion implements AutoCloseable {
                          Conexion() { System.out.println("Conexión abierta"); }

                          void consultar(String sql) {
                              if (sql.contains("tabla_que_no_existe")) {
                                  throw new IllegalStateException("no existe la tabla");
                              }
                              System.out.println("Consulta hecha: " + sql);
                          }

                          @Override
                          public void close() { System.out.println("Conexión cerrada"); }
                      }

                      public static void main(String[] args) {
                          try (___) {
                              c.consultar("SELECT * FROM viajero");
                              c.consultar("SELECT * FROM tabla_que_no_existe");
                          } catch (IllegalStateException e) {
                              System.out.println("Error: " + e.getMessage());
                          }
                      }
                  }
              ''',
              solucion='''
                  public class SiempreCerrada {
                      static class Conexion implements AutoCloseable {
                          Conexion() { System.out.println("Conexión abierta"); }

                          void consultar(String sql) {
                              if (sql.contains("tabla_que_no_existe")) {
                                  throw new IllegalStateException("no existe la tabla");
                              }
                              System.out.println("Consulta hecha: " + sql);
                          }

                          @Override
                          public void close() { System.out.println("Conexión cerrada"); }
                      }

                      public static void main(String[] args) {
                          try (Conexion c = new Conexion()) {
                              c.consultar("SELECT * FROM viajero");
                              c.consultar("SELECT * FROM tabla_que_no_existe");
                          } catch (IllegalStateException e) {
                              System.out.println("Error: " + e.getMessage());
                          }
                      }
                  }
              ''',
              al_superar="La conexión se cierra **antes** de mostrar el error, aunque la consulta falló. La puerta de hierro queda libre para el próximo.",
              imagen=["Una puerta de hierro cerrándose sola detrás de un mensajero, aunque este tropezó.",
                      "Gheco con una llave colgada al cuello."]),
            m(id="S01-N05-P3", titulo="Lo que ve el ResultSet",
              lugar="La puerta de hierro de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              lenguaje="sql",
              carta="Alias y metadatos | AS da nombre a una columna del resultado · el ResultSet la lee por ese nombre (rs.getString(\"barco\")) · ResultSetMetaData los lista",
              recompensa="xp 15, oro 20",
              escena="""
                  El programa de Java lee el resultado de la consulta columna por columna, **por nombre**. Si la consulta no les pone nombres claros, el programa no sabe qué leer.
              """,
              sugiere="Con `AS` se le pone nombre a cada columna del resultado: `COUNT(*) AS cantidad`. Ese es el nombre que usa `rs.getInt(\"cantidad\")` en Java, y el que muestran los metadatos.",
              desafio="Poné el alias `cantidad` a la cuenta.",
              inicial='''
                  CREATE TABLE cargamento (descripcion TEXT, barco TEXT, kilos INTEGER);
                  INSERT INTO cargamento VALUES ('café', 'Garza', 40), ('vidrios', 'Garza', 8), ('sal', 'Bagre', 120);
                  SELECT barco, COUNT(*) ___, SUM(kilos) AS kilos_totales
                  FROM cargamento
                  GROUP BY barco
                  ORDER BY barco;
              ''',
              solucion='''
                  CREATE TABLE cargamento (descripcion TEXT, barco TEXT, kilos INTEGER);
                  INSERT INTO cargamento VALUES ('café', 'Garza', 40), ('vidrios', 'Garza', 8), ('sal', 'Bagre', 120);
                  SELECT barco, COUNT(*) AS cantidad, SUM(kilos) AS kilos_totales
                  FROM cargamento
                  GROUP BY barco
                  ORDER BY barco;
              ''',
              al_superar="""
                  Columnas con nombre: barco, cantidad, kilos_totales. El programa de Java ya sabe qué pedir.
                  Detrás de la puerta, cada tabla tiene un encargado propio: el **DAO**.
              """,
              imagen=["Un resultado de consulta con etiquetas claras arriba de cada columna.",
                      "Detrás de la puerta de hierro, encargados con delantal frente a cada tabla."]),
        ],
    },
    {
        "titulo": "S01-N06 · DAO: el ABM completo desde Java",
        "misiones": [
            m(id="S01-N06-P1", titulo="El encargado de cada tabla",
              lugar="Las salas de los DAO", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="DAO | una interfaz con las operaciones (listar, buscar, insertar…) · una implementación por base · el resto del programa no ve SQL",
              recompensa="xp 10, oro 10",
              escena="""
                  Cada tabla de la Bóveda tiene un encargado, el **DAO**: el resto del Imperio le pide cosas y nunca ve una línea de SQL. Gheco arma uno de práctica, en memoria.
              """,
              sugiere="El DAO es una **interfaz** (`ViajeroDAO`) con las operaciones. Una implementación habla con la base; otra, en memoria, sirve para probar. Al insertar, el DAO devuelve el **id generado**.",
              desafio="Completá el `insertar`: asigná el siguiente id, guardá y devolvé el id.",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Dao {
                      record Viajero(int id, String nombre) { }

                      interface ViajeroDAO {
                          int insertar(String nombre);

                          List<Viajero> listar();
                      }

                      static class ViajeroDAOMemoria implements ViajeroDAO {
                          private final List<Viajero> tabla = new ArrayList<>();
                          private int secuencia = 0;

                          public int insertar(String nombre) {
                              ___;
                          }

                          public List<Viajero> listar() { return List.copyOf(tabla); }
                      }

                      public static void main(String[] args) {
                          ViajeroDAO dao = new ViajeroDAOMemoria();
                          System.out.println("Id de Zed: " + dao.insertar("Zed"));
                          System.out.println("Id de Nadia: " + dao.insertar("Nadia"));
                          dao.listar().forEach(System.out::println);
                      }
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Dao {
                      record Viajero(int id, String nombre) { }

                      interface ViajeroDAO {
                          int insertar(String nombre);

                          List<Viajero> listar();
                      }

                      static class ViajeroDAOMemoria implements ViajeroDAO {
                          private final List<Viajero> tabla = new ArrayList<>();
                          private int secuencia = 0;

                          public int insertar(String nombre) {
                              int id = ++secuencia;
                              tabla.add(new Viajero(id, nombre));
                              return id;
                          }

                          public List<Viajero> listar() { return List.copyOf(tabla); }
                      }

                      public static void main(String[] args) {
                          ViajeroDAO dao = new ViajeroDAOMemoria();
                          System.out.println("Id de Zed: " + dao.insertar("Zed"));
                          System.out.println("Id de Nadia: " + dao.insertar("Nadia"));
                          dao.listar().forEach(System.out::println);
                      }
                  }
              ''',
              al_superar="Dos viajeros con su id, y el `main` nunca escribió SQL. —Mañana se cambia la memoria por PostgreSQL —dice Kaffa— y el resto del Imperio ni se entera.",
              imagen=["Una sala con un encargado de delantal frente a una tabla, recibiendo pedidos por una ventanilla.",
                      "Kaffa mostrando dos llaves intercambiables: «memoria» y «PostgreSQL»."]),
            m(id="S01-N06-P2", titulo="Buscar sin null",
              lugar="Las salas de los DAO", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="troll",
              carta="buscar con Optional | Optional<Viajero> buscar(int id) · vacío si no está · quien llama decide con orElse o ifPresentOrElse",
              recompensa="xp 15, oro 15",
              escena="""
                  El DAO viejo devolvía `null` cuando no encontraba a alguien, y el **troll** aparecía tres pantallas después. Zed escribe un `buscar` que devuelve una caja que puede estar vacía.
              """,
              sugiere="`buscar` devuelve `Optional<Viajero>`: con un stream, `filter(v -> v.id() == id).findFirst()`. Quien llama decide: `.map(Viajero::nombre).orElse(\"no existe\")`.",
              desafio="Completá el `buscar`: el primero con ese id.",
              inicial='''
                  import java.util.List;
                  import java.util.Optional;

                  public class Buscar {
                      record Viajero(int id, String nombre) { }

                      static final List<Viajero> TABLA = List.of(new Viajero(1, "Zed"), new Viajero(2, "Nadia"));

                      static Optional<Viajero> buscar(int id) {
                          return ___;
                      }

                      public static void main(String[] args) {
                          for (int id : new int[] {2, 9}) {
                              System.out.println(id + ": " + buscar(id).map(Viajero::nombre).orElse("no existe"));
                          }
                      }
                  }
              ''',
              solucion='''
                  import java.util.List;
                  import java.util.Optional;

                  public class Buscar {
                      record Viajero(int id, String nombre) { }

                      static final List<Viajero> TABLA = List.of(new Viajero(1, "Zed"), new Viajero(2, "Nadia"));

                      static Optional<Viajero> buscar(int id) {
                          return TABLA.stream().filter(v -> v.id() == id).findFirst();
                      }

                      public static void main(String[] args) {
                          for (int id : new int[] {2, 9}) {
                              System.out.println(id + ": " + buscar(id).map(Viajero::nombre).orElse("no existe"));
                          }
                      }
                  }
              ''',
              al_superar="«9: no existe», sin un solo `null`. El troll se queda mirando una caja vacía, desilusionado.",
              imagen=["Una caja de bronce abierta y vacía, con un cartel «no existe».",
                      "Un troll mirando la caja, desilusionado."]),
            m(id="S01-N06-P3", titulo="El error en idioma del Imperio",
              lugar="Las salas de los DAO", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Traducir excepciones | el DAO atrapa la SQLException y lanza una propia (DatoInvalidoException) con un mensaje que el sistema entiende · guarda la original como causa",
              recompensa="xp 15, oro 20",
              escena="""
                  Cuando la base rechaza algo, devuelve un mensaje en idioma de máquina: *duplicate key value violates unique constraint*. —El DAO lo traduce —dice Kaffa—. Al resto del Imperio le llega «ese pasaporte ya está registrado».
              """,
              sugiere="El DAO atrapa la `SQLException` y lanza una excepción **propia**, con un mensaje claro y la original como **causa**: `throw new DatoInvalidoException(\"…\", e)`. Así nadie fuera del DAO tiene que conocer SQL.",
              desafio="Completá el `throw`: una `DatoInvalidoException` con el mensaje y la causa.",
              inicial='''
                  import java.sql.SQLException;

                  public class Traducir {
                      static class DatoInvalidoException extends RuntimeException {
                          DatoInvalidoException(String mensaje, Throwable causa) { super(mensaje, causa); }
                      }

                      static void insertarEnLaBase(String pasaporte) throws SQLException {
                          if (pasaporte.equals("AR-101")) {
                              throw new SQLException("duplicate key value violates unique constraint", "23505");
                          }
                      }

                      static void registrar(String pasaporte) {
                          try {
                              insertarEnLaBase(pasaporte);
                              System.out.println(pasaporte + ": registrado");
                          } catch (SQLException e) {
                              throw ___;
                          }
                      }

                      public static void main(String[] args) {
                          for (String p : new String[] {"UY-202", "AR-101"}) {
                              try {
                                  registrar(p);
                              } catch (DatoInvalidoException e) {
                                  System.out.println(p + ": " + e.getMessage() + " (código " + ((SQLException) e.getCause()).getSQLState() + ")");
                              }
                          }
                      }
                  }
              ''',
              solucion='''
                  import java.sql.SQLException;

                  public class Traducir {
                      static class DatoInvalidoException extends RuntimeException {
                          DatoInvalidoException(String mensaje, Throwable causa) { super(mensaje, causa); }
                      }

                      static void insertarEnLaBase(String pasaporte) throws SQLException {
                          if (pasaporte.equals("AR-101")) {
                              throw new SQLException("duplicate key value violates unique constraint", "23505");
                          }
                      }

                      static void registrar(String pasaporte) {
                          try {
                              insertarEnLaBase(pasaporte);
                              System.out.println(pasaporte + ": registrado");
                          } catch (SQLException e) {
                              throw new DatoInvalidoException("ese pasaporte ya está registrado", e);
                          }
                      }

                      public static void main(String[] args) {
                          for (String p : new String[] {"UY-202", "AR-101"}) {
                              try {
                                  registrar(p);
                              } catch (DatoInvalidoException e) {
                                  System.out.println(p + ": " + e.getMessage() + " (código " + ((SQLException) e.getCause()).getSQLState() + ")");
                              }
                          }
                      }
                  }
              ''',
              al_superar="""
                  «ese pasaporte ya está registrado», en idioma del Imperio, y el código original guardado por si alguien lo necesita.
                  En el piso más bajo, hay operaciones que tienen que salir **todas juntas o ninguna**.
              """,
              imagen=["Un traductor de túnica convirtiendo un pergamino lleno de símbolos en una frase clara.",
                      "Al fondo, una escalera que baja al último piso de la Bóveda."]),
        ],
    },
    {
        "titulo": "S01-N07 · Transacciones y CallableStatement",
        "misiones": [
            m(id="S01-N07-P1", titulo="Todas juntas",
              lugar="El último piso de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              lenguaje="sql",
              carta="Transacción | BEGIN; … COMMIT; · las operaciones de adentro se guardan juntas · en JDBC: setAutoCommit(false) y commit()",
              recompensa="xp 10, oro 10",
              escena="""
                  Pasar denarios del cofre de Nadia al de Zed son dos operaciones: sacar de uno y poner en el otro. Si se hace una sola, desaparece plata. —**Todas juntas** —dice Kaffa—: una transacción.
              """,
              sugiere="Entre `BEGIN;` y `COMMIT;`, las operaciones forman una sola unidad: se confirman juntas. En JDBC es lo mismo con `setAutoCommit(false)` y `commit()`.",
              desafio="Confirmá la transacción al final.",
              inicial='''
                  CREATE TABLE cofre (dueno TEXT PRIMARY KEY, denarios INTEGER CHECK (denarios >= 0));
                  INSERT INTO cofre VALUES ('Nadia', 150), ('Zed', 20);
                  BEGIN;
                  UPDATE cofre SET denarios = denarios - 100 WHERE dueno = 'Nadia';
                  UPDATE cofre SET denarios = denarios + 100 WHERE dueno = 'Zed';
                  ___;
                  SELECT dueno, denarios FROM cofre ORDER BY dueno;
              ''',
              solucion='''
                  CREATE TABLE cofre (dueno TEXT PRIMARY KEY, denarios INTEGER CHECK (denarios >= 0));
                  INSERT INTO cofre VALUES ('Nadia', 150), ('Zed', 20);
                  BEGIN;
                  UPDATE cofre SET denarios = denarios - 100 WHERE dueno = 'Nadia';
                  UPDATE cofre SET denarios = denarios + 100 WHERE dueno = 'Zed';
                  COMMIT;
                  SELECT dueno, denarios FROM cofre ORDER BY dueno;
              ''',
              al_superar="Cien denarios cruzan de un cofre al otro y la suma sigue siendo la misma. —Me los vas a devolver —dice Nadia. —Con intereses —promete Zed.",
              imagen=["Dos cofres unidos por un puente de luz por el que cruzan cien denarios a la vez.",
                      "Nadia de brazos cruzados; Zed sonriendo con las monedas."]),
            m(id="S01-N07-P2", titulo="Ninguna",
              lugar="El último piso de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              lenguaje="sql",
              criatura="ogro",
              carta="ROLLBACK | deshace todo lo que se hizo desde el BEGIN · se usa cuando algo sale mal en el medio · en JDBC: rollback() en el catch",
              recompensa="xp 15, oro 15",
              escena="""
                  A mitad de una transferencia, Zed se da cuenta de que el monto estaba mal: ya sacó de un cofre, pero todavía no puso en el otro. Un **ogro** le dice que lo arregle a mano.
              """,
              sugiere="`ROLLBACK;` deshace todo lo hecho desde el `BEGIN`: los cofres vuelven a como estaban. En Java, va en el `catch`: `conexion.rollback()`.",
              desafio="Deshacé la transacción.",
              inicial='''
                  CREATE TABLE cofre (dueno TEXT PRIMARY KEY, denarios INTEGER);
                  INSERT INTO cofre VALUES ('Nadia', 50), ('Zed', 120);
                  BEGIN;
                  UPDATE cofre SET denarios = denarios - 500 WHERE dueno = 'Zed';
                  ___;
                  SELECT dueno, denarios FROM cofre ORDER BY dueno;
              ''',
              solucion='''
                  CREATE TABLE cofre (dueno TEXT PRIMARY KEY, denarios INTEGER);
                  INSERT INTO cofre VALUES ('Nadia', 50), ('Zed', 120);
                  BEGIN;
                  UPDATE cofre SET denarios = denarios - 500 WHERE dueno = 'Zed';
                  ROLLBACK;
                  SELECT dueno, denarios FROM cofre ORDER BY dueno;
              ''',
              al_superar="Como si nada hubiera pasado: 120 en el cofre de Zed. El ogro se queda con las ganas de un arreglo a mano.",
              imagen=["Un reloj de arena que se da vuelta solo y devuelve las monedas a su cofre.",
                      "Un ogro con un martillo, sin nada que arreglar."]),
            m(id="S01-N07-P3", titulo="El punto de guardado",
              lugar="El último piso de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              lenguaje="sql",
              carta="SAVEPOINT | SAVEPOINT nombre marca un punto · ROLLBACK TO nombre vuelve ahí sin perder lo anterior · en JDBC: setSavepoint()",
              recompensa="xp 15, oro 20",
              escena="""
                  En una carga larga, Baldo registra tres productos. El tercero estaba mal. No quiere perder los dos primeros: quiere volver **un paso atrás**, no al principio.
              """,
              sugiere="`SAVEPOINT antes_del_tercero;` marca un punto adentro de la transacción. `ROLLBACK TO antes_del_tercero;` deshace solo lo que vino después. Al final, `COMMIT` guarda el resto.",
              desafio="Volvé al punto de guardado, sin deshacer los dos primeros.",
              inicial='''
                  CREATE TABLE producto (nombre TEXT, precio INTEGER);
                  BEGIN;
                  INSERT INTO producto VALUES ('Café Fuerte', 30);
                  INSERT INTO producto VALUES ('Capa de Viajero', 100);
                  SAVEPOINT antes_del_tercero;
                  INSERT INTO producto VALUES ('Ganzúa de Oro', 999999);
                  ___;
                  COMMIT;
                  SELECT nombre, precio FROM producto;
              ''',
              solucion='''
                  CREATE TABLE producto (nombre TEXT, precio INTEGER);
                  BEGIN;
                  INSERT INTO producto VALUES ('Café Fuerte', 30);
                  INSERT INTO producto VALUES ('Capa de Viajero', 100);
                  SAVEPOINT antes_del_tercero;
                  INSERT INTO producto VALUES ('Ganzúa de Oro', 999999);
                  ROLLBACK TO antes_del_tercero;
                  COMMIT;
                  SELECT nombre, precio FROM producto;
              ''',
              al_superar="""
                  El café y la capa quedan; la «Ganzúa de Oro» a un millón, no. —Era un chiste —dice Baldo. Nadie le cree.
                  En el fondo del último piso, entre tablas abandonadas, algo se mueve: **el Liche de las Tablas Huérfanas**.
              """,
              imagen=["Una línea de tiempo con una bandera clavada en el medio y lo que vino después desvaneciéndose.",
                      "Baldo con una ganzúa dorada de mentira; al fondo, una sombra entre tablas rotas."]),
        ],
    },
    {
        "titulo": "S01-N08 · Jefe: el Liche de las Tablas Huérfanas",
        "misiones": [
            m(id="S01-N08-P1", titulo="Los registros sin dueño",
              lugar="El fondo de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              lenguaje="sql",
              criatura="dragon",
              carta="Huérfanos | LEFT JOIN … WHERE padre.id IS NULL encuentra filas que apuntan a algo que ya no existe",
              recompensa="xp 20, oro 20",
              escena="""
                  El **Liche de las Tablas Huérfanas** vive entre registros que apuntan a dueños que ya no existen. Alguien creó estas tablas sin claves foráneas, y el Liche se alimenta de cada fila suelta.
              """,
              sugiere="Con `LEFT JOIN viajero v ON v.id = c.viajero_id`, los cargamentos cuyo viajero no existe quedan con `v.id` en `NULL`. `WHERE v.id IS NULL` deja solo a los huérfanos.",
              desafio="Completá la condición que deja solo a los huérfanos.",
              inicial='''
                  CREATE TABLE viajero (id INTEGER PRIMARY KEY, nombre TEXT);
                  CREATE TABLE cargamento (id INTEGER PRIMARY KEY, descripcion TEXT, viajero_id INTEGER);
                  INSERT INTO viajero VALUES (1, 'Zed'), (2, 'Baldo');
                  INSERT INTO cargamento (descripcion, viajero_id) VALUES ('ganzúa', 1), ('sal', 2), ('vitral', 7), ('seda', 9);
                  SELECT c.descripcion AS huerfano, c.viajero_id AS dueno_perdido
                  FROM cargamento c
                  LEFT JOIN viajero v ON v.id = c.viajero_id
                  WHERE ___;
              ''',
              solucion='''
                  CREATE TABLE viajero (id INTEGER PRIMARY KEY, nombre TEXT);
                  CREATE TABLE cargamento (id INTEGER PRIMARY KEY, descripcion TEXT, viajero_id INTEGER);
                  INSERT INTO viajero VALUES (1, 'Zed'), (2, 'Baldo');
                  INSERT INTO cargamento (descripcion, viajero_id) VALUES ('ganzúa', 1), ('sal', 2), ('vitral', 7), ('seda', 9);
                  SELECT c.descripcion AS huerfano, c.viajero_id AS dueno_perdido
                  FROM cargamento c
                  LEFT JOIN viajero v ON v.id = c.viajero_id
                  WHERE v.id IS NULL;
              ''',
              al_superar="Dos huérfanos: un vitral cuyo dueño, el 7, ya no está en ningún registro… y una seda. El Liche se encoge cuando Zed los nombra.",
              imagen=["El Liche de las Tablas Huérfanas: un esqueleto coronado envuelto en hojas de cálculo rotas, flotando entre tablas abandonadas.",
                      "Dos filas sueltas brillando en el aire: «vitral · 7» y «seda · 9»."]),
            m(id="S01-N08-P2", titulo="La clave que protege",
              lugar="El fondo de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              lenguaje="sql",
              carta="Clave foránea con cascada | REFERENCES viajero(id) ON DELETE CASCADE · la base no deja crear huérfanos y, al borrar al dueño, borra lo suyo",
              recompensa="xp 20, oro 25",
              escena="""
                  Para que el Liche no vuelva, el esquema nuevo **no deja** crear huérfanos: cada cargamento tiene que apuntar a un viajero que exista, y si el viajero se va, sus cargamentos se van con él.
              """,
              sugiere="`viajero_id INTEGER REFERENCES viajero(id) ON DELETE CASCADE`: la base controla que el dueño exista y, al borrarlo, borra lo que dependía de él. (En SQLite hay que activar las claves foráneas; acá ya están activas.)",
              desafio="Completá la regla del borrado: en cascada.",
              inicial='''
                  CREATE TABLE viajero (id INTEGER PRIMARY KEY, nombre TEXT);
                  CREATE TABLE cargamento (
                      id INTEGER PRIMARY KEY,
                      descripcion TEXT,
                      viajero_id INTEGER NOT NULL REFERENCES viajero(id) ON DELETE ___
                  );
                  INSERT INTO viajero VALUES (1, 'Zed'), (2, 'Baldo');
                  INSERT INTO cargamento (descripcion, viajero_id) VALUES ('ganzúa', 1), ('sal', 2), ('pimienta', 2);
                  DELETE FROM viajero WHERE nombre = 'Baldo';
                  SELECT COUNT(*) AS cargamentos FROM cargamento;
              ''',
              solucion='''
                  CREATE TABLE viajero (id INTEGER PRIMARY KEY, nombre TEXT);
                  CREATE TABLE cargamento (
                      id INTEGER PRIMARY KEY,
                      descripcion TEXT,
                      viajero_id INTEGER NOT NULL REFERENCES viajero(id) ON DELETE CASCADE
                  );
                  INSERT INTO viajero VALUES (1, 'Zed'), (2, 'Baldo');
                  INSERT INTO cargamento (descripcion, viajero_id) VALUES ('ganzúa', 1), ('sal', 2), ('pimienta', 2);
                  DELETE FROM viajero WHERE nombre = 'Baldo';
                  SELECT COUNT(*) AS cargamentos FROM cargamento;
              ''',
              al_superar="Baldo se va de la tabla (de viaje, como siempre) y sus dos cargamentos con él. Queda uno: la ganzúa de Zed. No hay huérfanos posibles. El Liche pierde la corona.",
              imagen=["Una cadena de luz que une cada cargamento con su dueño; al irse Baldo, sus cajas se van con él.",
                      "El Liche sin corona, desvaneciéndose."]),
            m(id="S01-N08-P3", titulo="El informe de la Bóveda",
              lugar="El fondo de la Bóveda", personajes="Zed, Gheco, Nadia, Kaffa",
              lenguaje="sql",
              carta="Todo junto | esquema con restricciones · transacción · JOIN y GROUP BY · ni un dato roto",
              recompensa="xp 25, oro 30",
              escena="""
                  Para terminar con el Liche, Zed carga la mercadería del día **en una transacción** y saca el informe final: cuántos kilos tiene cada viajero, con su nombre.
              """,
              sugiere="La carga va entre `BEGIN` y `COMMIT`. El informe une las dos tablas con `JOIN` y suma con `SUM(c.kilos)` agrupando por viajero. `ORDER BY total DESC` deja primero al que más tiene.",
              desafio="Completá la suma de los kilos de cada viajero.",
              inicial='''
                  CREATE TABLE viajero (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL UNIQUE);
                  CREATE TABLE cargamento (
                      id INTEGER PRIMARY KEY,
                      kilos INTEGER NOT NULL CHECK (kilos > 0),
                      viajero_id INTEGER NOT NULL REFERENCES viajero(id) ON DELETE CASCADE
                  );
                  BEGIN;
                  INSERT INTO viajero (nombre) VALUES ('Zed'), ('Nadia'), ('Baldo');
                  INSERT INTO cargamento (kilos, viajero_id) VALUES (5, 1), (12, 2), (80, 3), (40, 3), (3, 1);
                  COMMIT;
                  SELECT v.nombre, COUNT(c.id) AS bultos, ___ AS total
                  FROM viajero v
                  JOIN cargamento c ON c.viajero_id = v.id
                  GROUP BY v.id
                  ORDER BY total DESC;
              ''',
              solucion='''
                  CREATE TABLE viajero (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL UNIQUE);
                  CREATE TABLE cargamento (
                      id INTEGER PRIMARY KEY,
                      kilos INTEGER NOT NULL CHECK (kilos > 0),
                      viajero_id INTEGER NOT NULL REFERENCES viajero(id) ON DELETE CASCADE
                  );
                  BEGIN;
                  INSERT INTO viajero (nombre) VALUES ('Zed'), ('Nadia'), ('Baldo');
                  INSERT INTO cargamento (kilos, viajero_id) VALUES (5, 1), (12, 2), (80, 3), (40, 3), (3, 1);
                  COMMIT;
                  SELECT v.nombre, COUNT(c.id) AS bultos, SUM(c.kilos) AS total
                  FROM viajero v
                  JOIN cargamento c ON c.viajero_id = v.id
                  GROUP BY v.id
                  ORDER BY total DESC;
              ''',
              al_superar="""
                  Baldo con 120 kilos (por supuesto), Nadia con 12, Zed con 8. Ni un huérfano, ni un dato roto. El Liche de las Tablas Huérfanas se deshace en polvo de registros viejos.
                  —La Bóveda es tuya —dice Kaffa—. Y lo que guardes acá, no se pierde.
              """,
              imagen=["El Liche deshaciéndose en polvo de registros viejos.",
                      "Un informe de piedra con tres renglones: Baldo 120, Nadia 12, Zed 8; Kaffa con la taza en alto."]),
        ],
    },
]
