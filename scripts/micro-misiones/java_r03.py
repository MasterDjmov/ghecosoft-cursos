import textwrap

from genjava import m

# R03: los Archivos Imperiales. JUnit se imita con Java puro (el ejecutor corre un solo archivo, sin librerías);
# el Logger escribe en System.out con un formato fijo para que la salida se pueda comparar.

LOG_SETUP = '''
    static Logger diario() {
        Logger log = Logger.getLogger("archivos");
        log.setUseParentHandlers(false);
        Handler consola = new StreamHandler(System.out, new Formatter() {
            @Override
            public String format(LogRecord r) {
                return r.getLevel() + ": " + r.getMessage() + System.lineSeparator();
            }
        }) {
            @Override
            public synchronized void publish(LogRecord r) {
                super.publish(r);
                flush();
            }
        };
        consola.setLevel(Level.ALL);
        log.addHandler(consola);
        return log;
    }
'''
# Alineado con los métodos de la clase en los bloques de código (22 espacios antes del dedent).
LOG_SETUP = textwrap.indent(textwrap.dedent(LOG_SETUP).strip("\n"), " " * 22)[14:] + "\n"  # los 14 primeros ya están en el texto

NODOS = [
    {
        "titulo": "R03-N01 · Paquetes, import y archivos .jar",
        "misiones": [
            m(id="R03-N01-P1", titulo="La dirección que faltaba",
              lugar="Las salas de los Archivos Imperiales", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              criatura="esqueleto",
              carta="import | import java.util.Random; · trae una clase de otro paquete por su nombre corto · sin import: cannot find symbol",
              recompensa="xp 10, oro 10",
              escena="""
                  Los **Archivos Imperiales** ocupan un palacio entero: salas, pasillos, estantes con etiquetas. El **Archivista Mayor**, un hombre flaco con una lupa colgada del cuello, recibe a Zed. —Acá cada pergamino tiene su sala. Para pedir uno de otra sala, decí de dónde viene.
                  Zed pide un `Random` sin decir de dónde, y un **esqueleto** sale del estante: *cannot find symbol*.
              """,
              sugiere="`Random` vive en el paquete `java.util`. Para usarlo con su nombre corto, hay que **importarlo** arriba de todo: `import java.util.Random;`. Solo las clases de `java.lang` (`String`, `Math`, `Integer`…) vienen sin import.",
              desafio="Ejecutalo, leé el error y agregá el `import` que falta en la primera línea.",
              inicial='''
                  public class Sorteo {
                      public static void main(String[] args) {
                          Random r = new Random(7);
                          System.out.println("Sala sorteada: " + (r.nextInt(10) + 1));
                          System.out.println("Estante sorteado: " + (r.nextInt(20) + 1));
                      }
                  }
              ''',
              solucion='''
                  import java.util.Random;

                  public class Sorteo {
                      public static void main(String[] args) {
                          Random r = new Random(7);
                          System.out.println("Sala sorteada: " + (r.nextInt(10) + 1));
                          System.out.println("Estante sorteado: " + (r.nextInt(20) + 1));
                      }
                  }
              ''',
              al_superar="Con la dirección completa, el pergamino llega solo. El esqueleto vuelve a su estante, ahora con etiqueta.",
              imagen=["Un palacio de archivos con salas y pasillos etiquetados: «Modelo», «Servicios», «Pantallas».",
                      "El Archivista Mayor (flaco, lupa colgada del cuello, túnica gris con vivos dorados) recibiendo a Zed y Nadia.",
                      "Un esqueleto saliendo de un estante sin etiqueta."]),
            m(id="R03-N01-P2", titulo="La sala de cada clase",
              lugar="Las salas de los Archivos Imperiales", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              carta="package | package imperio.archivos; en la PRIMERA línea · el nombre completo de la clase es imperio.archivos.Pergamino",
              recompensa="xp 10, oro 10",
              escena="""
                  —Tu clase no puede andar suelta por el palacio —dice el Archivista—. Decí en qué sala vive. Y desde ese momento, su nombre completo incluye la sala.
              """,
              sugiere="`package imperio.archivos;` va en la **primera línea** del archivo: la clase pasa a vivir en ese paquete. Su nombre completo es `imperio.archivos.Pergamino`, y eso es lo que muestra `getClass().getName()`.",
              desafio="Completá la palabra que declara el paquete.",
              inicial='''
                  ___ imperio.archivos;

                  public class Pergamino {
                      public static void main(String[] args) {
                          Pergamino p = new Pergamino();
                          System.out.println("Nombre corto: " + p.getClass().getSimpleName());
                          System.out.println("Nombre completo: " + p.getClass().getName());
                      }
                  }
              ''',
              solucion='''
                  package imperio.archivos;

                  public class Pergamino {
                      public static void main(String[] args) {
                          Pergamino p = new Pergamino();
                          System.out.println("Nombre corto: " + p.getClass().getSimpleName());
                          System.out.println("Nombre completo: " + p.getClass().getName());
                      }
                  }
              ''',
              al_superar="«imperio.archivos.Pergamino.» El Archivista lo anota en el índice. En un proyecto de verdad, además, el archivo va en la carpeta `imperio/archivos/`.",
              imagen=["Un índice gigante del palacio con una entrada nueva: «imperio.archivos.Pergamino».",
                      "El Archivista anotando con una pluma larga; Gheco señalando la carpeta en un mapa del palacio."]),
            m(id="R03-N01-P3", titulo="La puerta de la sala",
              lugar="Las salas de los Archivos Imperiales", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              carta="Acceso de paquete | sin modificador: lo ven las clases del MISMO paquete · private: solo la propia clase · public: todos",
              recompensa="xp 15, oro 15",
              escena="""
                  El catálogo de la sala tiene un dato que tienen que leer **los archivistas de esa sala**, pero no los visitantes de otras. Alguien lo marcó `private` y ahora no lo lee nadie, ni siquiera la clase vecina.
              """,
              sugiere="Sin modificador, un atributo es **de paquete**: lo ven las clases del mismo paquete y nadie más. Es el punto medio entre `private` (solo la propia clase) y `public` (todos). Todas las clases de este archivo están en el mismo paquete.",
              desafio="Ejecutalo, leé el error y sacale el `private` al atributo `ubicacion` para que lo vean las clases de la misma sala.",
              inicial='''
                  public class Sala {
                      public static void main(String[] args) {
                          Catalogo c = new Catalogo();
                          System.out.println("Título: " + c.titulo);
                          System.out.println("Ubicación: " + c.ubicacion);
                      }
                  }

                  class Catalogo {
                      public String titulo = "Tratado de los moldes";
                      private String ubicacion = "estante 14, sala norte";
                  }
              ''',
              solucion='''
                  public class Sala {
                      public static void main(String[] args) {
                          Catalogo c = new Catalogo();
                          System.out.println("Título: " + c.titulo);
                          System.out.println("Ubicación: " + c.ubicacion);
                      }
                  }

                  class Catalogo {
                      public String titulo = "Tratado de los moldes";
                      String ubicacion = "estante 14, sala norte";
                  }
              ''',
              al_superar="""
                  «Estante 14, sala norte.» Allá va Zed. En el ala norte, el archivista de turno está desesperado: le dieron un estante con **diez** lugares fijos y ya tiene catorce pergaminos.
              """,
              imagen=["Una puerta de sala con tres cerraduras de distinto tamaño: una abierta para todos, una para los de la sala y una con candado.",
                      "Al fondo, un estante de diez lugares desbordado de pergaminos."]),
        ],
    },
    {
        "titulo": "R03-N02 · ArrayList y genéricos",
        "misiones": [
            m(id="R03-N02-P1", titulo="El estante que crece",
              lugar="El ala norte de los Archivos", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              carta="ArrayList | List<String> l = new ArrayList<>(); · add agrega · get(i) lee · size() cuántos hay · crece sola",
              recompensa="xp 10, oro 10",
              escena="""
                  El estante del ala norte tiene diez lugares fijos, como un array. Para agregar uno más, el archivista tiene que pedir un estante nuevo, copiar todo y tirar el viejo. —Para lo que crece —dice Gheco—, una **lista**.
              """,
              sugiere="Un `ArrayList` es un array que **crece solo**: `add(x)` agrega al final, `get(i)` lee la posición `i` y `size()` dice cuántos hay. Se declara con la interfaz: `List<String> estante = new ArrayList<>();`. `Collections.sort(estante)` la ordena.",
              desafio="Agregá el pergamino que falta, \"Mapa del sur\", con el método que agrega al final.",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.Collections;
                  import java.util.List;

                  public class AlaNorte {
                      public static void main(String[] args) {
                          List<String> estante = new ArrayList<>();
                          estante.add("Tratado de paz");
                          estante.add("Censo del Puerto");
                          estante.___("Mapa del sur");
                          System.out.println("Pergaminos: " + estante.size());
                          System.out.println("El segundo: " + estante.get(1));
                          Collections.sort(estante);
                          System.out.println("Ordenados: " + estante);
                      }
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.Collections;
                  import java.util.List;

                  public class AlaNorte {
                      public static void main(String[] args) {
                          List<String> estante = new ArrayList<>();
                          estante.add("Tratado de paz");
                          estante.add("Censo del Puerto");
                          estante.add("Mapa del sur");
                          System.out.println("Pergaminos: " + estante.size());
                          System.out.println("El segundo: " + estante.get(1));
                          Collections.sort(estante);
                          System.out.println("Ordenados: " + estante);
                      }
                  }
              ''',
              al_superar="El estante se estira solo para cada pergamino nuevo. El archivista lo mira como si fuera un milagro y le ofrece café a Zed.",
              imagen=["Un estante de madera mágico que se alarga a medida que le ponen pergaminos.",
                      "El archivista del ala norte, aliviado, ofreciéndole una taza a Zed."]),
            m(id="R03-N02-P2", titulo="Los primitivos no entran",
              lugar="El ala norte de los Archivos", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              carta="Envoltorios | List<Integer>, nunca List<int> · Integer envuelve a int, Double a double · autoboxing: add(90) lo envuelve solo",
              recompensa="xp 15, oro 15",
              escena="""
                  Zed quiere guardar los puntajes del torneo de los Archivos en una lista de `int`. La Aduana del compilador no lo deja: las listas solo guardan **objetos**.
              """,
              sugiere="Los genéricos solo aceptan clases. Para enteros se usa la clase **envoltorio** `Integer`: `List<Integer>`. Al hacer `add(90)`, Java envuelve el `int` solo (**autoboxing**), y al sumarlo lo desenvuelve.",
              desafio="Completá el tipo de la lista con la clase envoltorio de `int`.",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Puntajes {
                      public static void main(String[] args) {
                          List<___> puntajes = new ArrayList<>();
                          puntajes.add(90);
                          puntajes.add(75);
                          puntajes.add(88);
                          int total = 0;
                          for (int p : puntajes) {
                              total += p;
                          }
                          System.out.println("Puntajes: " + puntajes);
                          System.out.println("Total: " + total);
                      }
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Puntajes {
                      public static void main(String[] args) {
                          List<Integer> puntajes = new ArrayList<>();
                          puntajes.add(90);
                          puntajes.add(75);
                          puntajes.add(88);
                          int total = 0;
                          for (int p : puntajes) {
                              total += p;
                          }
                          System.out.println("Puntajes: " + puntajes);
                          System.out.println("Total: " + total);
                      }
                  }
              ''',
              al_superar="Doscientos cincuenta y tres puntos. Nadia ganó el torneo de los Archivos, por supuesto. Zed quedó segundo «porque no conocía el reglamento».",
              imagen=["Tres números envueltos en papel de regalo con la etiqueta «Integer», entrando en una lista.",
                      "Nadia con una medalla; Zed con una más chica, poniendo excusas."]),
            m(id="R03-N02-P3", titulo="El que se borró de más",
              lugar="El ala norte de los Archivos", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              criatura="ogro",
              carta="remove en List<Integer> | remove(2) borra la POSICIÓN 2 · remove(Integer.valueOf(2)) borra el VALOR 2",
              recompensa="xp 15, oro 15",
              escena="""
                  En la lista de salas para revisar hay que tachar la **sala 2**. Zed escribe `salas.remove(2)` y desaparece otra sala. El programa no se queja: un **ogro** de manual.
              """,
              sugiere="En una `List<Integer>`, `remove(2)` borra la **posición** 2. Para borrar el **valor** 2 hay que pasarle un objeto: `remove(Integer.valueOf(2))`.",
              desafio="Ejecutalo, mirá qué sala desaparece y arreglalo para borrar el valor 2.",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Salas {
                      public static void main(String[] args) {
                          List<Integer> salas = new ArrayList<>(List.of(5, 2, 9, 7));
                          salas.remove(2);
                          System.out.println("Quedan por revisar: " + salas);
                      }
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Salas {
                      public static void main(String[] args) {
                          List<Integer> salas = new ArrayList<>(List.of(5, 2, 9, 7));
                          salas.remove(Integer.valueOf(2));
                          System.out.println("Quedan por revisar: " + salas);
                      }
                  }
              ''',
              al_superar="Ahora sí se tacha la sala 2 y la 9 vuelve a la lista. El ogro se aleja, ofendido.",
              imagen=["Una lista de salas en un pergamino: la 2 tachada correctamente y la 9 restaurada con tinta fresca.",
                      "Un ogro alejándose con los brazos cruzados."]),
            m(id="R03-N02-P4", titulo="El cofre de cualquier cosa",
              lugar="El ala norte de los Archivos", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              carta="Clase genérica | class Cofre<T> { T contenido; } · T es un tipo que se elige al usarla · Cofre<String>, Cofre<Integer>",
              recompensa="xp 15, oro 15",
              escena="""
                  El Archivista quiere un cofre que guarde **una** cosa, de cualquier tipo, pero sin mezclar: un cofre de pergaminos solo acepta pergaminos. —Como las listas —dice Gheco—: con un **tipo entre `<>`**.
              """,
              sugiere="`class Cofre<T>` declara un **parámetro de tipo** `T`. Adentro se usa como cualquier tipo (`T contenido;`). Al crear el cofre se elige: `new Cofre<>(\"…\")` en un `Cofre<String>`.",
              desafio="Completá el parámetro de tipo de la clase.",
              inicial='''
                  public class Cofres {
                      public static void main(String[] args) {
                          Cofre<String> deTexto = new Cofre<>("Carta del Vidriero");
                          Cofre<Integer> deNumeros = new Cofre<>(1203);
                          System.out.println(deTexto.abrir().toUpperCase());
                          System.out.println(deNumeros.abrir() + 1);
                      }
                  }

                  class Cofre<___> {
                      private T contenido;

                      Cofre(T contenido) {
                          this.contenido = contenido;
                      }

                      T abrir() {
                          return contenido;
                      }
                  }
              ''',
              solucion='''
                  public class Cofres {
                      public static void main(String[] args) {
                          Cofre<String> deTexto = new Cofre<>("Carta del Vidriero");
                          Cofre<Integer> deNumeros = new Cofre<>(1203);
                          System.out.println(deTexto.abrir().toUpperCase());
                          System.out.println(deNumeros.abrir() + 1);
                      }
                  }

                  class Cofre<T> {
                      private T contenido;

                      Cofre(T contenido) {
                          this.contenido = contenido;
                      }

                      T abrir() {
                          return contenido;
                      }
                  }
              ''',
              al_superar="""
                  Uno guarda texto y el otro un número, y la Aduana del compilador sabe qué hay en cada uno. —«Carta del Vidriero» —lee Zed—. ¿Quién es el Vidriero?
                  —Preguntá en el ala sur —dice el Archivista—. Allá no hay estantes: hay **fichas**.
              """,
              imagen=["Dos cofres iguales con etiquetas distintas, «String» e «Integer», uno con una carta y otro con un número.",
                      "Zed leyendo la etiqueta «Carta del Vidriero», intrigado."]),
        ],
    },
    {
        "titulo": "R03-N03 · Mapas y conjuntos: HashMap y HashSet",
        "misiones": [
            m(id="R03-N03-P1", titulo="El censo de criaturas",
              lugar="El ala sur de los Archivos", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              carta="Contar con un mapa | Map<String, Integer> m = new TreeMap<>(); · m.put(k, m.getOrDefault(k, 0) + 1) · TreeMap ordena por clave",
              recompensa="xp 10, oro 10",
              escena="""
                  En el ala sur no hay estantes numerados: hay **fichas**, cada una con una etiqueta. El Archivista le pide a Zed el censo de las criaturas vistas en el Imperio este mes: cuántas de cada una.
              """,
              sugiere="Un **mapa** asocia cada clave con un valor. Para contar: `censo.put(c, censo.getOrDefault(c, 0) + 1)`: si la criatura no estaba, arranca en 0. Con `TreeMap`, las claves salen ordenadas.",
              desafio="Completá el valor por defecto del conteo: si todavía no estaba, cuenta desde cero.",
              inicial='''
                  import java.util.Map;
                  import java.util.TreeMap;

                  public class Censo {
                      public static void main(String[] args) {
                          String[] vistas = {"slime", "orco", "slime", "troll", "slime", "orco"};
                          Map<String, Integer> censo = new TreeMap<>();
                          for (String c : vistas) {
                              censo.put(c, censo.getOrDefault(c, ___) + 1);
                          }
                          System.out.println(censo);
                          System.out.println("Slimes: " + censo.get("slime"));
                      }
                  }
              ''',
              solucion='''
                  import java.util.Map;
                  import java.util.TreeMap;

                  public class Censo {
                      public static void main(String[] args) {
                          String[] vistas = {"slime", "orco", "slime", "troll", "slime", "orco"};
                          Map<String, Integer> censo = new TreeMap<>();
                          for (String c : vistas) {
                              censo.put(c, censo.getOrDefault(c, 0) + 1);
                          }
                          System.out.println(censo);
                          System.out.println("Slimes: " + censo.get("slime"));
                      }
                  }
              ''',
              al_superar="Tres slimes, dos orcos, un troll. El Archivista guarda el censo en la ficha «criaturas». —Ni un recuento a mano —dice, conmovido.",
              imagen=["El ala sur de los Archivos: paredes de cajoncitos con fichas etiquetadas.",
                      "Una ficha «criaturas» con los conteos: orco 2, slime 3, troll 1."]),
            m(id="R03-N03-P2", titulo="Recorrer las fichas",
              lugar="El ala sur de los Archivos", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              carta="Recorrer un mapa | for (Map.Entry<String, Integer> e : m.entrySet()) · e.getKey() la clave · e.getValue() el valor",
              recompensa="xp 10, oro 10",
              escena="""
                  El Archivista quiere el listado de las ciudades con su población, una por renglón, para colgarlo en la puerta del ala.
              """,
              sugiere="`mapa.entrySet()` devuelve todos los pares. Cada `Map.Entry` tiene `getKey()` (la clave) y `getValue()` (el valor).",
              desafio="Completá el método que lee el valor de cada par.",
              inicial='''
                  import java.util.Map;
                  import java.util.TreeMap;

                  public class Ciudades {
                      public static void main(String[] args) {
                          Map<String, Integer> poblacion = new TreeMap<>();
                          poblacion.put("Capital", 120000);
                          poblacion.put("Puerto", 45000);
                          poblacion.put("Aduana", 3000);
                          for (Map.Entry<String, Integer> e : poblacion.entrySet()) {
                              System.out.println(e.getKey() + ": " + e.___());
                          }
                      }
                  }
              ''',
              solucion='''
                  import java.util.Map;
                  import java.util.TreeMap;

                  public class Ciudades {
                      public static void main(String[] args) {
                          Map<String, Integer> poblacion = new TreeMap<>();
                          poblacion.put("Capital", 120000);
                          poblacion.put("Puerto", 45000);
                          poblacion.put("Aduana", 3000);
                          for (Map.Entry<String, Integer> e : poblacion.entrySet()) {
                              System.out.println(e.getKey() + ": " + e.getValue());
                          }
                      }
                  }
              ''',
              al_superar="Tres ciudades en orden alfabético. —El Puerto tiene cuarenta y cinco mil —dice Zed—, y yo conocía a la mitad. —A la mitad le debías algo —comenta Nadia.",
              imagen=["Un cartel en la puerta del ala sur con tres ciudades y su población.",
                      "Zed sonriendo con nostalgia; Nadia levantando una ceja."]),
            m(id="R03-N03-P3", titulo="Los invitados sin repetir",
              lugar="El ala sur de los Archivos", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              carta="Set | Set<String> s = new HashSet<>(); · no guarda repetidos · add devuelve false si ya estaba",
              recompensa="xp 15, oro 15",
              escena="""
                  Para la cena de los Archivos, cada sala mandó su lista de invitados y muchos se repiten. Al Archivista solo le importa **quién viene**, sin repetidos.
              """,
              sugiere="Un `Set` es un conjunto: no guarda repetidos. `invitados.add(n)` devuelve `true` si lo agregó y `false` si ya estaba. `size()` dice cuántos distintos hay.",
              desafio="Completá el método que agrega al conjunto (y devuelve si era nuevo).",
              inicial='''
                  import java.util.HashSet;
                  import java.util.Set;

                  public class Invitados {
                      public static void main(String[] args) {
                          String[] listas = {"Kaffa", "Nadia", "Zed", "Nadia", "la Maestra de Moldes", "Kaffa"};
                          Set<String> invitados = new HashSet<>();
                          for (String n : listas) {
                              if (!invitados.___(n)) {
                                  System.out.println(n + " ya estaba");
                              }
                          }
                          System.out.println("Vienen " + invitados.size() + " invitados");
                          System.out.println("¿Viene Zed? " + invitados.contains("Zed"));
                      }
                  }
              ''',
              solucion='''
                  import java.util.HashSet;
                  import java.util.Set;

                  public class Invitados {
                      public static void main(String[] args) {
                          String[] listas = {"Kaffa", "Nadia", "Zed", "Nadia", "la Maestra de Moldes", "Kaffa"};
                          Set<String> invitados = new HashSet<>();
                          for (String n : listas) {
                              if (!invitados.add(n)) {
                                  System.out.println(n + " ya estaba");
                              }
                          }
                          System.out.println("Vienen " + invitados.size() + " invitados");
                          System.out.println("¿Viene Zed? " + invitados.contains("Zed"));
                      }
                  }
              ''',
              al_superar="Cuatro invitados distintos. Zed figura en la lista oficial de una cena del Imperio. Hace un mes, hubiera entrado por la ventana.",
              imagen=["Una tarjeta de invitación con cuatro nombres, y dos repetidos tachados que se desvanecen.",
                      "Zed mirando su nombre en la lista, contento."]),
            m(id="R03-N03-P4", titulo="La ficha del Vidriero",
              lugar="El ala sur de los Archivos", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              criatura="troll",
              carta="containsKey | get(k) da null si la clave no está… o si está con valor null · containsKey(k) dice si la clave existe",
              recompensa="xp 15, oro 20",
              escena="""
                  Zed busca la ficha del viajero por su clave: **«el Vidriero»**. `get` devuelve `null`. ¿No existe? Nadia, que conoce el ala sur, no está tan segura. Un **troll** asoma detrás de los cajones.
              """,
              sugiere="`get(clave)` devuelve `null` en dos casos: si la clave **no está**, o si está **guardada con `null`**. Para distinguirlos, `containsKey(clave)`.",
              desafio="Completá el método que pregunta si la clave existe.",
              inicial='''
                  import java.util.HashMap;
                  import java.util.Map;

                  public class Fichas {
                      public static void main(String[] args) {
                          Map<String, String> fichas = new HashMap<>();
                          fichas.put("Baldo", "mercader ambulante");
                          fichas.put("el Vidriero", null);
                          String[] buscadas = {"Baldo", "el Vidriero", "el Fantasma"};
                          for (String k : buscadas) {
                              if (fichas.get(k) != null) {
                                  System.out.println(k + ": " + fichas.get(k));
                              } else if (fichas.___(k)) {
                                  System.out.println(k + ": la ficha existe, pero alguien la vació");
                              } else {
                                  System.out.println(k + ": no hay ficha");
                              }
                          }
                      }
                  }
              ''',
              solucion='''
                  import java.util.HashMap;
                  import java.util.Map;

                  public class Fichas {
                      public static void main(String[] args) {
                          Map<String, String> fichas = new HashMap<>();
                          fichas.put("Baldo", "mercader ambulante");
                          fichas.put("el Vidriero", null);
                          String[] buscadas = {"Baldo", "el Vidriero", "el Fantasma"};
                          for (String k : buscadas) {
                              if (fichas.get(k) != null) {
                                  System.out.println(k + ": " + fichas.get(k));
                              } else if (fichas.containsKey(k)) {
                                  System.out.println(k + ": la ficha existe, pero alguien la vació");
                              } else {
                                  System.out.println(k + ": no hay ficha");
                              }
                          }
                      }
                  }
              ''',
              al_superar="""
                  La ficha del Vidriero **existe**, pero alguien la vació. Zed y Nadia se miran.
                  Esa noche, el palacio entero se apaga: un archivista pidió un tomo que no existía y todo se cortó.
              """,
              imagen=["Un cajón del ala sur abierto con la etiqueta «el Vidriero» y la ficha en blanco adentro.",
                      "Zed y Nadia mirándose; un troll escondido detrás de los cajones; las luces del palacio apagándose al fondo."]),
        ],
    },
    {
        "titulo": "R03-N04 · Excepciones",
        "misiones": [
            m(id="R03-N04-P1", titulo="La primera campana",
              lugar="Las salas de los Archivos, de noche", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="goblin",
              carta="try / catch | try { lo que puede fallar } catch (NumberFormatException e) { qué hacer } · el programa sigue",
              recompensa="xp 10, oro 10",
              escena="""
                  A la mañana, Kaffa instala en cada sala una **campana**: si algo sale mal, suena, alguien la escucha y decide qué hacer, y el resto del palacio sigue funcionando. Zed, que toda su vida esquivó las alarmas, esta vez tiene que **escucharlas**.
                  El primer pedido del día dice «doce» en lugar de 12. Un **goblin** se frota las manos.
              """,
              sugiere="Lo que puede fallar va adentro de `try { … }`. Si falla, Java salta al `catch` de esa excepción: `catch (NumberFormatException e)`. `e.getMessage()` dice qué pasó. El programa no se corta.",
              desafio="Completá el tipo de excepción que se atrapa.",
              inicial='''
                  public class Campana {
                      public static void main(String[] args) {
                          String[] pedidos = {"12", "doce", "7"};
                          for (String p : pedidos) {
                              try {
                                  int tomo = Integer.parseInt(p);
                                  System.out.println("Tomo " + tomo + ": en camino");
                              } catch (___ e) {
                                  System.out.println("Campana: «" + p + "» no es un número de tomo");
                              }
                          }
                      }
                  }
              ''',
              solucion='''
                  public class Campana {
                      public static void main(String[] args) {
                          String[] pedidos = {"12", "doce", "7"};
                          for (String p : pedidos) {
                              try {
                                  int tomo = Integer.parseInt(p);
                                  System.out.println("Tomo " + tomo + ": en camino");
                              } catch (NumberFormatException e) {
                                  System.out.println("Campana: «" + p + "» no es un número de tomo");
                              }
                          }
                      }
                  }
              ''',
              al_superar="Suena la campana, alguien la escucha, y el tomo 7 llega igual. El palacio no se apaga. Kaffa le da a Zed una palmada en el hombro.",
              imagen=["Una campana de bronce sonando en una sala de los Archivos; un pergamino con «doce» escrito.",
                      "Kaffa instalando campanas; un goblin decepcionado."]),
            m(id="R03-N04-P2", titulo="Pase lo que pase",
              lugar="Las salas de los Archivos", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="finally | finally { … } se ejecuta SIEMPRE: si salió bien, si falló y si hubo return · para cerrar y ordenar",
              recompensa="xp 15, oro 15",
              escena="""
                  Cada vez que un archivista entra a buscar un tomo, tiene que **apagar la vela** al salir, lo haya encontrado o no. Si se olvida, se quema el ala.
              """,
              sugiere="El bloque `finally` va después del `try`/`catch` y se ejecuta **siempre**, haya fallado o no. Ahí va lo que no se puede olvidar: cerrar, apagar, ordenar.",
              desafio="Completá la palabra del bloque que se ejecuta siempre.",
              inicial='''
                  public class Vela {
                      static void buscar(String tomo) {
                          try {
                              System.out.println("Busco «" + tomo + "»: " + tomo.substring(0, 3));
                          } catch (StringIndexOutOfBoundsException e) {
                              System.out.println("«" + tomo + "» es demasiado corto");
                          } ___ {
                              System.out.println("Vela apagada");
                          }
                      }

                      public static void main(String[] args) {
                          buscar("Tratado");
                          buscar("Tu");
                      }
                  }
              ''',
              solucion='''
                  public class Vela {
                      static void buscar(String tomo) {
                          try {
                              System.out.println("Busco «" + tomo + "»: " + tomo.substring(0, 3));
                          } catch (StringIndexOutOfBoundsException e) {
                              System.out.println("«" + tomo + "» es demasiado corto");
                          } finally {
                              System.out.println("Vela apagada");
                          }
                      }

                      public static void main(String[] args) {
                          buscar("Tratado");
                          buscar("Tu");
                      }
                  }
              ''',
              al_superar="Dos búsquedas, dos velas apagadas. El ala sigue en pie.",
              imagen=["Un archivista apagando una vela al salir de una sala oscura.",
                      "Un cartel en la puerta: «Pase lo que pase, apagá la vela»."]),
            m(id="R03-N04-P3", titulo="La campana propia",
              lugar="La herrería de los Archivos", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="throw y excepción propia | class SinStockException extends Exception · throw new SinStockException(\"…\") · el método avisa con throws",
              recompensa="xp 15, oro 15",
              escena="""
                  La herrería de los Archivos fabrica ganchos para los estantes. Cuando se queda sin hierro, no puede devolver «-3 ganchos»: tiene que **hacer sonar su propia campana**.
              """,
              sugiere="Una excepción propia se declara extendiendo `Exception`. El método que la puede lanzar lo avisa con `throws SinStockException`, y la lanza con `throw new SinStockException(\"mensaje\")`. Quien lo llama tiene que atraparla.",
              desafio="Completá el `throw`: lanzá una `SinStockException` nueva con el mensaje armado.",
              inicial='''
                  public class Herreria {
                      static int stock = 5;

                      static void fabricar(int ganchos) throws SinStockException {
                          if (ganchos > stock) {
                              throw ___;
                          }
                          stock -= ganchos;
                          System.out.println("Fabricados " + ganchos + ", queda hierro para " + stock);
                      }

                      public static void main(String[] args) {
                          int[] pedidos = {3, 4, 2};
                          for (int p : pedidos) {
                              try {
                                  fabricar(p);
                              } catch (SinStockException e) {
                                  System.out.println("Campana de la herrería: " + e.getMessage());
                              }
                          }
                      }
                  }

                  class SinStockException extends Exception {
                      SinStockException(String mensaje) {
                          super(mensaje);
                      }
                  }
              ''',
              solucion='''
                  public class Herreria {
                      static int stock = 5;

                      static void fabricar(int ganchos) throws SinStockException {
                          if (ganchos > stock) {
                              throw new SinStockException("pidieron " + ganchos + " y hay hierro para " + stock);
                          }
                          stock -= ganchos;
                          System.out.println("Fabricados " + ganchos + ", queda hierro para " + stock);
                      }

                      public static void main(String[] args) {
                          int[] pedidos = {3, 4, 2};
                          for (int p : pedidos) {
                              try {
                                  fabricar(p);
                              } catch (SinStockException e) {
                                  System.out.println("Campana de la herrería: " + e.getMessage());
                              }
                          }
                      }
                  }

                  class SinStockException extends Exception {
                      SinStockException(String mensaje) {
                          super(mensaje);
                      }
                  }
              ''',
              al_superar="El pedido de 4 rebota con un mensaje claro y el de 2 sale igual. El herrero cuelga su campana nueva, con su nombre grabado.",
              imagen=["Una herrería pequeña con una campana nueva colgada, grabada «SinStock».",
                      "El herrero mostrando el último lingote de hierro; Zed tomando nota."]),
            m(id="R03-N04-P4", titulo="La campana que trae otra",
              lugar="Las salas de los Archivos", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="La causa | throw new RegistroException(\"…\", e) · la excepción nueva lleva adentro la original · e.getCause() la recupera (en el stack trace: Caused by)",
              recompensa="xp 15, oro 20",
              item="Amuleto de la Campana",
              escena="""
                  Zed intenta leer el registro del Vidriero y suena una campana que dice «no se pudo leer el registro». ¿Por qué? —Una campana grande suele traer una chica adentro —dice Kaffa—. **La causa**. Ahí está lo que pasó de verdad.
              """,
              sugiere="Al lanzar una excepción nueva por culpa de otra, pasale la original como **causa**: `new RegistroException(\"…\", e)`. Quien la atrapa la recupera con `getCause()`. En un stack trace aparece como `Caused by:`.",
              desafio="Completá el método que recupera la excepción original.",
              inicial='''
                  public class Causa {
                      static int leerAnio(String registro) throws RegistroException {
                          try {
                              return Integer.parseInt(registro.split(";")[1]);
                          } catch (NumberFormatException e) {
                              throw new RegistroException("No se pudo leer el registro «" + registro + "»", e);
                          }
                      }

                      public static void main(String[] args) {
                          try {
                              System.out.println("Año: " + leerAnio("Baldo;1203"));
                              System.out.println("Año: " + leerAnio("el Vidriero;???"));
                          } catch (RegistroException e) {
                              System.out.println(e.getMessage());
                              System.out.println("Causa: " + e.___().getMessage());
                          }
                      }
                  }

                  class RegistroException extends Exception {
                      RegistroException(String mensaje, Throwable causa) {
                          super(mensaje, causa);
                      }
                  }
              ''',
              solucion='''
                  public class Causa {
                      static int leerAnio(String registro) throws RegistroException {
                          try {
                              return Integer.parseInt(registro.split(";")[1]);
                          } catch (NumberFormatException e) {
                              throw new RegistroException("No se pudo leer el registro «" + registro + "»", e);
                          }
                      }

                      public static void main(String[] args) {
                          try {
                              System.out.println("Año: " + leerAnio("Baldo;1203"));
                              System.out.println("Año: " + leerAnio("el Vidriero;???"));
                          } catch (RegistroException e) {
                              System.out.println(e.getMessage());
                              System.out.println("Causa: " + e.getCause().getMessage());
                          }
                      }
                  }

                  class RegistroException extends Exception {
                      RegistroException(String mensaje, Throwable causa) {
                          super(mensaje, causa);
                      }
                  }
              ''',
              al_superar="""
                  «For input string: "???"». Alguien reemplazó el año del Vidriero por signos de pregunta. No fue un error: fue **a propósito**.
                  Kaffa le cuelga a Zed del cuello una campanita de bronce: el **Amuleto de la Campana**. —Para que la escuches siempre. En una pelea, te va a levantar una vez.
              """,
              imagen=["Una campana grande que, al sonar, deja ver una campanita más chica adentro.",
                      "Kaffa colgándole a Zed un amuleto con forma de campanita de bronce.",
                      "Un registro con «???» escrito en lugar del año."]),
        ],
    },
    {
        "titulo": "R03-N05 · Lambdas, clases anónimas y referencias a métodos",
        "misiones": [
            m(id="R03-N05-P1", titulo="La tarjetita",
              lugar="La oficina del Archivista Mayor", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              carta="Lambda | (a, b) -> Integer.compare(a.length(), b.length()) · un método sin nombre, en una línea · reemplaza a una clase anónima",
              recompensa="xp 10, oro 10",
              escena="""
                  El Archivista Mayor está cansado de dar instrucciones largas. Para ordenar los títulos por largo escribió una clase anónima de diez líneas. Una aprendiz le pasa una **tarjetita** con una sola línea. Él la mira, sonríe y la clava en la puerta.
              """,
              sugiere="Una **lambda** es un método sin nombre: `(a, b) -> …`. Si una interfaz tiene **un solo** método (como `Comparator`), en lugar de una clase anónima se pasa la lambda: `titulos.sort((a, b) -> Integer.compare(a.length(), b.length()));`.",
              desafio="Completá el cuerpo de la lambda: comparar por largo del título.",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Tarjetita {
                      public static void main(String[] args) {
                          List<String> titulos = new ArrayList<>(List.of("Tratado de paz", "Censo", "Mapa del sur", "Leyes"));
                          titulos.sort((a, b) -> ___);
                          System.out.println(titulos);
                      }
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Tarjetita {
                      public static void main(String[] args) {
                          List<String> titulos = new ArrayList<>(List.of("Tratado de paz", "Censo", "Mapa del sur", "Leyes"));
                          titulos.sort((a, b) -> Integer.compare(a.length(), b.length()));
                          System.out.println(titulos);
                      }
                  }
              ''',
              al_superar="Diez líneas en una. El Archivista clava la tarjetita en la puerta, al lado de la de la aprendiz.",
              imagen=["Una puerta de oficina con tarjetitas clavadas, cada una con una lambda escrita.",
                      "El Archivista Mayor sonriendo con la lupa en la mano."]),
            m(id="R03-N05-P2", titulo="Limpiar sin tropezar",
              lugar="El depósito de los Archivos", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              carta="removeIf | lista.removeIf(p -> p.contains(\"roto\")) · borra los que cumplen la condición · sin borrar adentro de un for-each",
              recompensa="xp 15, oro 15",
              escena="""
                  Hay que sacar del depósito todos los pergaminos rotos. Borrar mientras se recorre con un for-each hace tropezar al programa. —Decile **qué** borrar —dice Gheco— y que la lista se ocupe del cómo.
              """,
              sugiere="`removeIf` recibe una condición (un `Predicate`): una lambda que devuelve `true` para los que hay que borrar. `p -> p.contains(\"roto\")`.",
              desafio="Completá la condición: se borran los que contienen \"roto\".",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Limpieza {
                      public static void main(String[] args) {
                          List<String> deposito = new ArrayList<>(List.of("Mapa (roto)", "Censo", "Leyes (roto)", "Tratado"));
                          deposito.removeIf(p -> ___);
                          System.out.println("Quedan: " + deposito);
                      }
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Limpieza {
                      public static void main(String[] args) {
                          List<String> deposito = new ArrayList<>(List.of("Mapa (roto)", "Censo", "Leyes (roto)", "Tratado"));
                          deposito.removeIf(p -> p.contains("roto"));
                          System.out.println("Quedan: " + deposito);
                      }
                  }
              ''',
              al_superar="El depósito queda limpio sin un tropiezo. Nadia, que ordena su libreta del mismo modo, asiente con aprobación profesional.",
              imagen=["Pergaminos rotos saliendo volando del estante solos; los sanos quedan en su lugar.",
                      "Nadia asintiendo con la libreta abierta."]),
            m(id="R03-N05-P3", titulo="Decir solo el nombre",
              lugar="La oficina del Archivista Mayor", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              carta="Referencia a método | String::toUpperCase en lugar de s -> s.toUpperCase() · System.out::println en lugar de x -> System.out.println(x)",
              recompensa="xp 15, oro 15",
              escena="""
                  Las tarjetitas del Archivista se fueron achicando. Ahora algunas dicen solo **el nombre del método**: `String::toUpperCase`. —Si la lambda solo llama a un método —explica Gheco—, decí el nombre y listo.
              """,
              sugiere="Cuando una lambda solo llama a un método, se puede escribir como **referencia a método**: `Clase::metodo`. `replaceAll(String::toUpperCase)` pasa cada elemento a mayúsculas; `forEach(System.out::println)` imprime cada uno.",
              desafio="Completá la referencia al método que imprime.",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Referencias {
                      public static void main(String[] args) {
                          List<String> salas = new ArrayList<>(List.of("norte", "sur", "de los errores"));
                          salas.replaceAll(String::toUpperCase);
                          salas.forEach(System.out::___);
                      }
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Referencias {
                      public static void main(String[] args) {
                          List<String> salas = new ArrayList<>(List.of("norte", "sur", "de los errores"));
                          salas.replaceAll(String::toUpperCase);
                          salas.forEach(System.out::println);
                      }
                  }
              ''',
              al_superar="Tres salas en mayúsculas, una por renglón, con dos tarjetitas de una palabra. La tercera sala, la de los errores, queda subrayada en el plano.",
              imagen=["Tarjetitas cada vez más chicas clavadas en la puerta: la última dice solo «String::toUpperCase».",
                      "Un plano del palacio con «SALA DE LOS ERRORES» subrayada."]),
            m(id="R03-N05-P4", titulo="Ordenar por año y por título",
              lugar="La oficina del Archivista Mayor", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              carta="Comparator.comparing | Comparator.comparing(Pergamino::anio).thenComparing(Pergamino::titulo) · primero por año, si empatan por título",
              recompensa="xp 15, oro 20",
              escena="""
                  El Archivista quiere los pergaminos del Vidriero ordenados por año y, si dos son del mismo año, por título. —Sin escribir la comparación a mano —pide—. Armala con piezas.
              """,
              sugiere="`Comparator.comparing(Pergamino::anio)` arma un comparador por año. `.thenComparing(Pergamino::titulo)` desempata por título. Con un `record`, los métodos `anio()` y `titulo()` ya existen.",
              desafio="Completá el desempate por título.",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.Comparator;
                  import java.util.List;

                  public class PorAnio {
                      public static void main(String[] args) {
                          List<Pergamino> delVidriero = new ArrayList<>(List.of(
                              new Pergamino("Vitral del río", 1203),
                              new Pergamino("Carta a la Torre", 1190),
                              new Pergamino("Boceto de ventana", 1203)));
                          delVidriero.sort(Comparator.comparing(Pergamino::anio).___(Pergamino::titulo));
                          for (Pergamino p : delVidriero) {
                              System.out.println(p.anio() + " - " + p.titulo());
                          }
                      }
                  }

                  record Pergamino(String titulo, int anio) {
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.Comparator;
                  import java.util.List;

                  public class PorAnio {
                      public static void main(String[] args) {
                          List<Pergamino> delVidriero = new ArrayList<>(List.of(
                              new Pergamino("Vitral del río", 1203),
                              new Pergamino("Carta a la Torre", 1190),
                              new Pergamino("Boceto de ventana", 1203)));
                          delVidriero.sort(Comparator.comparing(Pergamino::anio).thenComparing(Pergamino::titulo));
                          for (Pergamino p : delVidriero) {
                              System.out.println(p.anio() + " - " + p.titulo());
                          }
                      }
                  }

                  record Pergamino(String titulo, int anio) {
                  }
              ''',
              al_superar="""
                  Una carta a la Torre, un boceto de ventana y un vitral para el río. Zed acomoda los tres pergaminos sobre la mesa: el Vidriero estaba **haciendo un vitral para una ventana de la Torre**.
                  Para estar seguros, Kaffa los manda al **Tribunal de las Pruebas**, junto a los Archivos.
              """,
              imagen=["Tres pergaminos ordenados sobre una mesa: «Carta a la Torre» (1190), «Boceto de ventana» y «Vitral del río» (1203).",
                      "Zed comparando el boceto de la ventana con su llave de vidrios de colores."]),
        ],
    },
    {
        "titulo": "R03-N06 · Pruebas con JUnit",
        "misiones": [
            m(id="R03-N06-P1", titulo="El primer juicio",
              lugar="El Tribunal de las Pruebas", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Una prueba | assertEquals(esperado, real) · primero lo que DEBERÍA dar, después lo que da · en JUnit, cada prueba es un método con @Test",
              recompensa="xp 10, oro 10",
              escena="""
                  En el Tribunal de las Pruebas, cada ley nueva se somete a un juicio antes de publicarse: los jueces le presentan casos —un mercader con 0 kilos, uno con 10, uno con 100— y la ley tiene que responder bien a todos.
              """,
              sugiere="Una prueba compara lo que **debería** dar con lo que **da**: `assertEquals(esperado, real)`. Acá lo imitamos con Java puro (en JUnit se escribe igual, dentro de métodos con `@Test`). El peaje es medio denario por kilo, redondeado para abajo.",
              desafio="Completá el valor esperado del caso «carga cero».",
              inicial='''
                  public class Tribunal {
                      static int peaje(int kg) {
                          return kg / 2;
                      }

                      static void assertEquals(int esperado, int real, String caso) {
                          if (esperado == real) {
                              System.out.println("OK " + caso);
                          } else {
                              System.out.println("FALLA " + caso + ": esperaba " + esperado + " y dio " + real);
                          }
                      }

                      public static void main(String[] args) {
                          assertEquals(___, peaje(0), "carga cero");
                          assertEquals(5, peaje(10), "diez kilos");
                          assertEquals(50, peaje(100), "cien kilos");
                          assertEquals(3, peaje(7), "siete kilos, para abajo");
                      }
                  }
              ''',
              solucion='''
                  public class Tribunal {
                      static int peaje(int kg) {
                          return kg / 2;
                      }

                      static void assertEquals(int esperado, int real, String caso) {
                          if (esperado == real) {
                              System.out.println("OK " + caso);
                          } else {
                              System.out.println("FALLA " + caso + ": esperaba " + esperado + " y dio " + real);
                          }
                      }

                      public static void main(String[] args) {
                          assertEquals(0, peaje(0), "carga cero");
                          assertEquals(5, peaje(10), "diez kilos");
                          assertEquals(50, peaje(100), "cien kilos");
                          assertEquals(3, peaje(7), "siete kilos, para abajo");
                      }
                  }
              ''',
              al_superar="Cuatro casos, cuatro OK. La ley del peaje queda publicada. —Y si mañana alguien la cambia —dice Kaffa—, los casos la vuelven a juzgar en un segundo.",
              imagen=["Un tribunal de piedra con tres jueces y una ley en pergamino en el centro, rodeada de casos de prueba con tildes verdes.",
                      "Kaffa con su taza, sentado en el banco del público."]),
            m(id="R03-N06-P2", titulo="El bug de los descuentos",
              lugar="El Tribunal de las Pruebas", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="ogro",
              carta="Regresión | las pruebas encuentran lo que se rompió sin querer · se arregla el CÓDIGO, nunca la prueba para que pase",
              recompensa="xp 15, oro 15",
              escena="""
                  La ley de descuentos dice: **desde** 100 kilos, 10 % menos. Alguien la «mejoró» y ahora un caso falla. Un **ogro** se esconde en el borde de la condición.
              """,
              sugiere="Cuando una prueba falla, leé el caso: qué esperaba y qué dio. «Desde 100» incluye al 100: la condición tiene que ser `>=`, no `>`. Se arregla la **ley**, no la prueba.",
              desafio="Ejecutalo, mirá qué caso falla y arreglá la condición del descuento.",
              inicial='''
                  public class Descuentos {
                      static int precio(int kg) {
                          int base = kg * 2;
                          if (kg > 100) {
                              return base - base / 10;
                          }
                          return base;
                      }

                      static void assertEquals(int esperado, int real, String caso) {
                          System.out.println((esperado == real ? "OK " : "FALLA ") + caso + (esperado == real ? "" : ": esperaba " + esperado + " y dio " + real));
                      }

                      public static void main(String[] args) {
                          assertEquals(100, precio(50), "50 kg, sin descuento");
                          assertEquals(180, precio(100), "100 kg, con descuento");
                          assertEquals(360, precio(200), "200 kg, con descuento");
                      }
                  }
              ''',
              solucion='''
                  public class Descuentos {
                      static int precio(int kg) {
                          int base = kg * 2;
                          if (kg >= 100) {
                              return base - base / 10;
                          }
                          return base;
                      }

                      static void assertEquals(int esperado, int real, String caso) {
                          System.out.println((esperado == real ? "OK " : "FALLA ") + caso + (esperado == real ? "" : ": esperaba " + esperado + " y dio " + real));
                      }

                      public static void main(String[] args) {
                          assertEquals(100, precio(50), "50 kg, sin descuento");
                          assertEquals(180, precio(100), "100 kg, con descuento");
                          assertEquals(360, precio(200), "200 kg, con descuento");
                      }
                  }
              ''',
              al_superar="Tres OK. El ogro de la regresión sale del tribunal escoltado. —Sin la prueba —dice Nadia—, ese mercader de cien kilos hubiera pagado de más durante meses.",
              imagen=["Un ogro escoltado por dos guardias fuera del tribunal.",
                      "Un pergamino con «>» tachado y «>=» escrito encima."]),
            m(id="R03-N06-P3", titulo="Cada juicio, desde cero",
              lugar="El Tribunal de las Pruebas", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Preparar antes de cada prueba | cada prueba arranca con objetos NUEVOS · en JUnit, @BeforeEach · si se comparten, una prueba ensucia a la otra",
              recompensa="xp 15, oro 15",
              escena="""
                  Dos juicios usan el mismo cofre. El primero retira 50 y el segundo, que esperaba encontrar 100, encuentra 50 y falla. —Cada juicio con **su** cofre —dice el juez—. Nuevo, como recién salido del molde.
              """,
              sugiere="Las pruebas no se tienen que pisar: cada una prepara sus propios objetos. En JUnit eso va en un método con `@BeforeEach`; acá, un método `nuevoCofre()` que cada prueba llama al empezar.",
              desafio="Ejecutalo, mirá qué prueba falla y hacé que la segunda use un cofre nuevo.",
              inicial='''
                  public class DesdeCero {
                      static Cofre nuevoCofre() {
                          return new Cofre(100);
                      }

                      static void assertEquals(int esperado, int real, String caso) {
                          System.out.println((esperado == real ? "OK " : "FALLA ") + caso + (esperado == real ? "" : ": esperaba " + esperado + " y dio " + real));
                      }

                      public static void main(String[] args) {
                          Cofre cofre = nuevoCofre();
                          cofre.retirar(50);
                          assertEquals(50, cofre.saldo, "retirar 50 deja 50");

                          cofre.depositar(20);
                          assertEquals(120, cofre.saldo, "depositar 20 en un cofre de 100");
                      }
                  }

                  class Cofre {
                      int saldo;

                      Cofre(int saldo) { this.saldo = saldo; }

                      void retirar(int m) { saldo -= m; }

                      void depositar(int m) { saldo += m; }
                  }
              ''',
              solucion='''
                  public class DesdeCero {
                      static Cofre nuevoCofre() {
                          return new Cofre(100);
                      }

                      static void assertEquals(int esperado, int real, String caso) {
                          System.out.println((esperado == real ? "OK " : "FALLA ") + caso + (esperado == real ? "" : ": esperaba " + esperado + " y dio " + real));
                      }

                      public static void main(String[] args) {
                          Cofre cofre = nuevoCofre();
                          cofre.retirar(50);
                          assertEquals(50, cofre.saldo, "retirar 50 deja 50");

                          cofre = nuevoCofre();
                          cofre.depositar(20);
                          assertEquals(120, cofre.saldo, "depositar 20 en un cofre de 100");
                      }
                  }

                  class Cofre {
                      int saldo;

                      Cofre(int saldo) { this.saldo = saldo; }

                      void retirar(int m) { saldo -= m; }

                      void depositar(int m) { saldo += m; }
                  }
              ''',
              al_superar="Cada juicio con su cofre nuevo, y los dos pasan. El juez golpea el martillo. —La ley estaba bien —dice—. La prueba estaba sucia.",
              imagen=["Dos cofres idénticos recién salidos del molde, uno para cada juicio.",
                      "El juez golpeando el martillo; Zed y Nadia en el estrado."]),
            m(id="R03-N06-P4", titulo="Primero la prueba",
              lugar="El Tribunal de las Pruebas", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="TDD | primero se escriben las pruebas (fallan) · después el código mínimo que las hace pasar · después se ordena",
              recompensa="xp 15, oro 20",
              escena="""
                  El Tribunal le encarga a Zed una ley nueva: qué años son **bisiestos** en el calendario del Imperio. Pero esta vez los jueces ya escribieron los casos **antes** de que exista la ley. —Hacelos pasar —dice Kaffa—. Ni más ni menos.
              """,
              sugiere="Un año es bisiesto si es divisible por 4, **salvo** que sea divisible por 100, **salvo** que también lo sea por 400. En Java: `(a % 4 == 0 && a % 100 != 0) || a % 400 == 0`.",
              desafio="Escribí el `return` de `esBisiesto` para que pasen todas las pruebas.",
              inicial='''
                  public class Bisiesto {
                      static boolean esBisiesto(int a) {
                          return ___;
                      }

                      static void assertEquals(boolean esperado, boolean real, String caso) {
                          System.out.println((esperado == real ? "OK " : "FALLA ") + caso);
                      }

                      public static void main(String[] args) {
                          assertEquals(true, esBisiesto(2024), "2024 es bisiesto");
                          assertEquals(false, esBisiesto(2023), "2023 no");
                          assertEquals(false, esBisiesto(1900), "1900 no (divisible por 100)");
                          assertEquals(true, esBisiesto(2000), "2000 sí (divisible por 400)");
                      }
                  }
              ''',
              solucion='''
                  public class Bisiesto {
                      static boolean esBisiesto(int a) {
                          return (a % 4 == 0 && a % 100 != 0) || a % 400 == 0;
                      }

                      static void assertEquals(boolean esperado, boolean real, String caso) {
                          System.out.println((esperado == real ? "OK " : "FALLA ") + caso);
                      }

                      public static void main(String[] args) {
                          assertEquals(true, esBisiesto(2024), "2024 es bisiesto");
                          assertEquals(false, esBisiesto(2023), "2023 no");
                          assertEquals(false, esBisiesto(1900), "1900 no (divisible por 100)");
                          assertEquals(true, esBisiesto(2000), "2000 sí (divisible por 400)");
                      }
                  }
              ''',
              al_superar="""
                  Cuatro OK y la ley queda publicada. Zed se da cuenta de que, por primera vez, sabía **antes** de ejecutar que iba a andar.
                  A la salida, una escriba del ala de los errores les hace señas: en su **diario** hay algo raro sobre el Vidriero.
              """,
              imagen=["Un calendario del Imperio con los años bisiestos marcados con sellos dorados.",
                      "Una escriba en la puerta del tribunal, con un diario grueso bajo el brazo, haciéndoles señas."]),
        ],
    },
    {
        "titulo": "R03-N07 · Depuración, logging y Javadoc",
        "misiones": [
            m(id="R03-N07-P1", titulo="El promedio que miente",
              lugar="El ala de los errores", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              criatura="ogro",
              carta="Depurar | el programa corre pero el resultado está mal · mirá los valores intermedios (println o el depurador) · encontrá la línea, no adivines",
              recompensa="xp 10, oro 10",
              escena="""
                  En el ala de los errores, un informe dice que los pergaminos pesan en promedio **2 kilos** y todos saben que es más. El programa no se queja: es un **ogro**. La escriba recorre el programa paso a paso, mirando cuánto vale cada variable.
              """,
              sugiere="Para cazar un ogro, mirá los valores intermedios: `suma`, `cantidad` y el resultado de la división. Si dividís dos `int`, el resultado es `int` y se pierden los decimales. Uno de los dos tiene que ser `double`.",
              desafio="Ejecutalo, fijate dónde se pierden los decimales y arreglá la división.",
              inicial='''
                  public class Promedio {
                      public static void main(String[] args) {
                          int[] pesos = {2, 3, 3, 2, 3};
                          int suma = 0;
                          for (int p : pesos) {
                              suma += p;
                          }
                          int cantidad = pesos.length;
                          double promedio = suma / cantidad;
                          System.out.println("Suma: " + suma + ", cantidad: " + cantidad);
                          System.out.println("Promedio: " + promedio);
                      }
                  }
              ''',
              solucion='''
                  public class Promedio {
                      public static void main(String[] args) {
                          int[] pesos = {2, 3, 3, 2, 3};
                          int suma = 0;
                          for (int p : pesos) {
                              suma += p;
                          }
                          int cantidad = pesos.length;
                          double promedio = (double) suma / cantidad;
                          System.out.println("Suma: " + suma + ", cantidad: " + cantidad);
                          System.out.println("Promedio: " + promedio);
                      }
                  }
              ''',
              al_superar="2.6 kilos. El informe se corrige y el ogro se queda sin escondite. —No adiviné —dice Zed—: miré.",
              imagen=["Una escriba recorriendo un programa escrito en un pergamino largo, con una lupa, línea por línea.",
                      "Un ogro escondido detrás de un «/» gigante."]),
            m(id="R03-N07-P2", titulo="El diario del ala",
              lugar="El ala de los errores", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              carta="Logger | log.info(…), log.warning(…), log.fine(…) · cada mensaje con su nivel · log.setLevel(Level.INFO) muestra INFO y más graves",
              recompensa="xp 15, oro 15",
              escena="""
                  La escriba no usa `println`: lleva un **diario** donde cada cosa tiene su gravedad. Los detalles finos solo los anota cuando está depurando; lo importante, siempre.
              """,
              sugiere="Un `Logger` anota mensajes con un **nivel**: `FINE` (detalle), `INFO` (normal), `WARNING` (algo raro), `SEVERE` (grave). `log.setLevel(Level.INFO)` muestra INFO y lo más grave, y esconde los `FINE`. El método `diario()` ya está armado para escribir en la consola.",
              desafio="Completá el nivel para que se vean INFO y WARNING, pero no los FINE.",
              inicial='''
                  import java.util.logging.*;

                  public class Diario {
              ''' + LOG_SETUP + '''
                      public static void main(String[] args) {
                          Logger log = diario();
                          log.setLevel(Level.___);
                          log.fine("abro el cajón 3");
                          log.info("Pedido del tomo 12");
                          log.fine("el tomo 12 pesa 2 kg");
                          log.warning("El tomo 13 no está en su estante");
                      }
                  }
              ''',
              solucion='''
                  import java.util.logging.*;

                  public class Diario {
              ''' + LOG_SETUP + '''
                      public static void main(String[] args) {
                          Logger log = diario();
                          log.setLevel(Level.INFO);
                          log.fine("abro el cajón 3");
                          log.info("Pedido del tomo 12");
                          log.fine("el tomo 12 pesa 2 kg");
                          log.warning("El tomo 13 no está en su estante");
                      }
                  }
              ''',
              al_superar="Dos renglones en el diario, los que importan. —Cuando algo se rompa —dice la escriba—, nadie va a adivinar: van a leer.",
              imagen=["Un diario abierto con renglones marcados por color: INFO en azul, WARNING en naranja.",
                      "La escriba del ala de los errores escribiendo con una pluma."]),
            m(id="R03-N07-P3", titulo="Quién borra los registros",
              lugar="El ala de los errores", personajes="Zed, Gheco, Nadia, el Archivista Mayor",
              carta="Registrar lo raro | log.warning(\"…\") donde pasa algo que no debería · con los datos que hacen falta para entenderlo después",
              recompensa="xp 15, oro 20",
              escena="""
                  Los registros del Vidriero siguen desapareciendo. Zed propone algo que antes no se le hubiera ocurrido: en lugar de esconderse a mirar, **anotar en el diario** cada vez que se borra un registro, y **dónde**.
              """,
              sugiere="Un `log.warning(...)` en el lugar exacto donde pasa lo raro, con los datos que importan (qué registro y en qué sala), deja la pista escrita.",
              desafio="Completá el mensaje de advertencia: «Borrado: <registro> en <sala>».",
              inicial='''
                  import java.util.logging.*;

                  public class QuienBorra {
              ''' + LOG_SETUP + '''
                      static Logger log;

                      static void borrar(String registro, String sala) {
                          log.warning(___);
                      }

                      public static void main(String[] args) {
                          log = diario();
                          log.info("Turno de noche");
                          borrar("Carta a la Torre", "la sala vacía");
                          borrar("Boceto de ventana", "la sala vacía");
                          log.info("Fin del turno");
                      }
                  }
              ''',
              solucion='''
                  import java.util.logging.*;

                  public class QuienBorra {
              ''' + LOG_SETUP + '''
                      static Logger log;

                      static void borrar(String registro, String sala) {
                          log.warning("Borrado: " + registro + " en " + sala);
                      }

                      public static void main(String[] args) {
                          log = diario();
                          log.info("Turno de noche");
                          borrar("Carta a la Torre", "la sala vacía");
                          borrar("Boceto de ventana", "la sala vacía");
                          log.info("Fin del turno");
                      }
                  }
              ''',
              al_superar="""
                  A la mañana, el diario lo dice claro: **todo** lo del Vidriero se borra en el mismo lugar, «la sala vacía», en lo más profundo de los Archivos. Allí donde los pergaminos desaparecen y el sistema grita *NullPointerException*.
              """,
              imagen=["Un diario abierto con dos renglones en naranja: «WARNING: Borrado: … en la sala vacía».",
                      "Zed, Nadia y Gheco mirando hacia un pasillo oscuro que baja a una sala vacía."]),
        ],
    },
    {
        "titulo": "R03-N08 · Jefe: el Espectro Nulo",
        "misiones": [
            m(id="R03-N08-P1", titulo="Vacía, nunca null",
              lugar="La sala vacía", personajes="Zed, Gheco, Nadia, Kaffa, el Espectro Nulo",
              criatura="dragon",
              carta="Colección vacía | un método que devuelve una lista NUNCA devuelve null · return new ArrayList<>(); (o List.of()) · quien la recorre no se cae",
              recompensa="xp 20, oro 20",
              escena="""
                  En lo más profundo de los Archivos, la sala está vacía. Zed pide los pergaminos de un autor que no tiene ninguno… y el sistema se congela con un grito: aparece el **Espectro Nulo**, justo donde alguien supuso que algo existía.
                  —No se lo vence corriendo detrás de cada `null` —dice Kaffa—. Se lo vence **diseñando** para que no tenga dónde aparecer. Primera regla: si no hay nada, devolvé **vacío**.
              """,
              sugiere="Si un método devuelve una lista y no encontró nada, que devuelva una lista **vacía** (`new ArrayList<>()`), nunca `null`. Así quien la recorre no tiene que preguntar: un for-each sobre una lista vacía simplemente no da vueltas.",
              desafio="Completá el `return` del caso «no encontré nada»: una lista vacía.",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class SalaVacia {
                      static List<String> delAutor(String autor) {
                          if (autor.equals("el Vidriero")) {
                              return new ArrayList<>(List.of("Carta a la Torre", "Boceto de ventana"));
                          }
                          return ___;
                      }

                      public static void main(String[] args) {
                          String[] autores = {"el Vidriero", "el Fantasma"};
                          for (String a : autores) {
                              List<String> obras = delAutor(a);
                              System.out.println(a + ": " + obras.size() + " pergaminos");
                              for (String o : obras) {
                                  System.out.println("  - " + o);
                              }
                          }
                      }
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class SalaVacia {
                      static List<String> delAutor(String autor) {
                          if (autor.equals("el Vidriero")) {
                              return new ArrayList<>(List.of("Carta a la Torre", "Boceto de ventana"));
                          }
                          return new ArrayList<>();
                      }

                      public static void main(String[] args) {
                          String[] autores = {"el Vidriero", "el Fantasma"};
                          for (String a : autores) {
                              List<String> obras = delAutor(a);
                              System.out.println(a + ": " + obras.size() + " pergaminos");
                              for (String o : obras) {
                                  System.out.println("  - " + o);
                              }
                          }
                      }
                  }
              ''',
              al_superar="«el Fantasma: 0 pergaminos», y el sistema sigue andando. El Espectro se estira buscando un `null` donde meterse… y no encuentra ninguno.",
              imagen=["El Espectro Nulo: una figura transparente hecha de pergaminos en blanco, con un hueco negro con forma de «null» en el pecho.",
                      "La sala vacía con estantes desnudos; Zed, Nadia, Gheco y Kaffa frente al Espectro."]),
            m(id="R03-N08-P2", titulo="Validar en la puerta",
              lugar="La sala vacía", personajes="Zed, Gheco, Nadia, Kaffa, el Espectro Nulo",
              carta="Validar en la entrada | el constructor rechaza lo inválido con IllegalArgumentException · un objeto que existe es un objeto válido",
              recompensa="xp 20, oro 20",
              escena="""
                  El Espectro intenta colarse por otro lado: un pergamino creado **sin título**. Si entra, va a explotar después, lejos, donde nadie entienda por qué. —Segunda regla —dice Kaffa—: lo inválido no entra. Se lo frena **en la puerta**.
              """,
              sugiere="El constructor revisa los datos y, si no sirven, lanza `IllegalArgumentException` con un mensaje claro. Un título es inválido si es `null` o está en blanco: `titulo == null || titulo.isBlank()`.",
              desafio="Completá la condición que rechaza el título inválido.",
              inicial='''
                  public class Puerta {
                      public static void main(String[] args) {
                          String[] titulos = {"Carta a la Torre", "", null};
                          for (String t : titulos) {
                              try {
                                  Pergamino p = new Pergamino(t);
                                  System.out.println("Archivado: " + p.titulo);
                              } catch (IllegalArgumentException e) {
                                  System.out.println("Rechazado: " + e.getMessage());
                              }
                          }
                      }
                  }

                  class Pergamino {
                      final String titulo;

                      Pergamino(String titulo) {
                          if (___) {
                              throw new IllegalArgumentException("un pergamino necesita título");
                          }
                          this.titulo = titulo;
                      }
                  }
              ''',
              solucion='''
                  public class Puerta {
                      public static void main(String[] args) {
                          String[] titulos = {"Carta a la Torre", "", null};
                          for (String t : titulos) {
                              try {
                                  Pergamino p = new Pergamino(t);
                                  System.out.println("Archivado: " + p.titulo);
                              } catch (IllegalArgumentException e) {
                                  System.out.println("Rechazado: " + e.getMessage());
                              }
                          }
                      }
                  }

                  class Pergamino {
                      final String titulo;

                      Pergamino(String titulo) {
                          if (titulo == null || titulo.isBlank()) {
                              throw new IllegalArgumentException("un pergamino necesita título");
                          }
                          this.titulo = titulo;
                      }
                  }
              ''',
              al_superar="Dos pergaminos rechazados en la puerta, con un mensaje que cualquiera entiende. El Espectro choca contra el marco y retrocede.",
              imagen=["Una puerta de la sala con un sello que rechaza dos pergaminos en blanco.",
                      "El Espectro Nulo rebotando contra el marco de la puerta."]),
            m(id="R03-N08-P3", titulo="Un error que diga qué pasó",
              lugar="La sala vacía", personajes="Zed, Gheco, Nadia, Kaffa, el Espectro Nulo",
              carta="Excepción con mensaje | en lugar de devolver null, lanzá una excepción propia que diga QUÉ faltó y CUÁL · el que la atrapa sabe qué hacer",
              recompensa="xp 20, oro 25",
              escena="""
                  El Espectro se esconde en `buscar(id)`: cuando el pergamino no está, devuelve `null` y el grito llega diez líneas después. —Tercera regla —dice Kaffa—: si algo tiene que estar y no está, **decilo** en ese momento, con nombre y apellido.
              """,
              sugiere="En lugar de devolver `null`, `buscar` lanza una `PergaminoNoEncontradoException` con un mensaje que diga **cuál** faltó: `\"no existe el pergamino \" + id`. El que llama la atrapa y decide.",
              desafio="Completá el mensaje de la excepción: «no existe el pergamino <id>».",
              inicial='''
                  import java.util.HashMap;
                  import java.util.Map;

                  public class Buscar {
                      static Map<Integer, String> archivo = new HashMap<>();

                      static String buscar(int id) throws PergaminoNoEncontradoException {
                          if (!archivo.containsKey(id)) {
                              throw new PergaminoNoEncontradoException(___);
                          }
                          return archivo.get(id);
                      }

                      public static void main(String[] args) {
                          archivo.put(1, "Carta a la Torre");
                          archivo.put(2, "Boceto de ventana");
                          int[] pedidos = {1, 7, 2};
                          for (int id : pedidos) {
                              try {
                                  System.out.println(id + ": " + buscar(id));
                              } catch (PergaminoNoEncontradoException e) {
                                  System.out.println(id + ": " + e.getMessage());
                              }
                          }
                      }
                  }

                  class PergaminoNoEncontradoException extends Exception {
                      PergaminoNoEncontradoException(String mensaje) {
                          super(mensaje);
                      }
                  }
              ''',
              solucion='''
                  import java.util.HashMap;
                  import java.util.Map;

                  public class Buscar {
                      static Map<Integer, String> archivo = new HashMap<>();

                      static String buscar(int id) throws PergaminoNoEncontradoException {
                          if (!archivo.containsKey(id)) {
                              throw new PergaminoNoEncontradoException("no existe el pergamino " + id);
                          }
                          return archivo.get(id);
                      }

                      public static void main(String[] args) {
                          archivo.put(1, "Carta a la Torre");
                          archivo.put(2, "Boceto de ventana");
                          int[] pedidos = {1, 7, 2};
                          for (int id : pedidos) {
                              try {
                                  System.out.println(id + ": " + buscar(id));
                              } catch (PergaminoNoEncontradoException e) {
                                  System.out.println(id + ": " + e.getMessage());
                              }
                          }
                      }
                  }

                  class PergaminoNoEncontradoException extends Exception {
                      PergaminoNoEncontradoException(String mensaje) {
                          super(mensaje);
                      }
                  }
              ''',
              al_superar="«7: no existe el pergamino 7.» Un error con nombre y apellido. El Espectro pierde la forma: ya no tiene dónde esconderse.",
              imagen=["Una campana sonando con un cartel claro: «no existe el pergamino 7».",
                      "El Espectro Nulo deshilachándose."]),
            m(id="R03-N08-P4", titulo="La ficha vuelve entera",
              lugar="La sala vacía", personajes="Zed, Gheco, Nadia, Kaffa, el Espectro Nulo",
              carta="Todo junto | validar en la entrada · vacío en lugar de null · errores con mensaje · un programa que no se cae con ningún pedido",
              recompensa="xp 25, oro 30",
              item="Linterna del Espectro",
              escena="""
                  Última regla: un programa que recibe pedidos **no se cae** con ninguno. Kaffa le pasa a Zed los pedidos de la noche, buenos y malos, para reconstruir la ficha del Vidriero sin que el Espectro meta la mano.
              """,
              sugiere="Cada pedido se procesa adentro de su propio `try`: si uno falla, se avisa y se sigue con el siguiente. `split(\" \", 2)` separa el comando del resto.",
              desafio="Completá el `catch`: atrapá la `IllegalArgumentException` de los pedidos inválidos.",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Ficha {
                      static List<String> ficha = new ArrayList<>();

                      static void procesar(String pedido) {
                          String[] partes = pedido.split(" ", 2);
                          if (partes.length < 2 || partes[1].isBlank()) {
                              throw new IllegalArgumentException("pedido incompleto: «" + pedido + "»");
                          }
                          if (!partes[0].equals("anotar")) {
                              throw new IllegalArgumentException("no conozco «" + partes[0] + "»");
                          }
                          ficha.add(partes[1]);
                      }

                      public static void main(String[] args) {
                          String[] pedidos = {"anotar el Vidriero hacía vitrales", "borrar todo", "anotar", "anotar mandó un vitral por el río hacia la Torre del Arquitecto"};
                          for (String p : pedidos) {
                              try {
                                  procesar(p);
                              } catch (___ e) {
                                  System.out.println("Ignorado: " + e.getMessage());
                              }
                          }
                          System.out.println("Ficha del Vidriero:");
                          ficha.forEach(linea -> System.out.println("- " + linea));
                      }
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Ficha {
                      static List<String> ficha = new ArrayList<>();

                      static void procesar(String pedido) {
                          String[] partes = pedido.split(" ", 2);
                          if (partes.length < 2 || partes[1].isBlank()) {
                              throw new IllegalArgumentException("pedido incompleto: «" + pedido + "»");
                          }
                          if (!partes[0].equals("anotar")) {
                              throw new IllegalArgumentException("no conozco «" + partes[0] + "»");
                          }
                          ficha.add(partes[1]);
                      }

                      public static void main(String[] args) {
                          String[] pedidos = {"anotar el Vidriero hacía vitrales", "borrar todo", "anotar", "anotar mandó un vitral por el río hacia la Torre del Arquitecto"};
                          for (String p : pedidos) {
                              try {
                                  procesar(p);
                              } catch (IllegalArgumentException e) {
                                  System.out.println("Ignorado: " + e.getMessage());
                              }
                          }
                          System.out.println("Ficha del Vidriero:");
                          ficha.forEach(linea -> System.out.println("- " + linea));
                      }
                  }
              ''',
              al_superar="""
                  El «borrar todo» rebota, el pedido vacío también, y la ficha **vuelve entera**: el Vidriero mandó un vitral por el río, hacia la Torre del Arquitecto, y nunca llegó.
                  El Espectro Nulo se apaga como una vela y deja en el piso una linterna de luz fría: la **Linterna del Espectro**. —Ilumina donde algo debería estar —dice Kaffa.
                  Desde las ventanas de los Archivos se oye el río que cruza la capital.
              """,
              imagen=["El Espectro Nulo apagándose como una vela en la sala vacía; en el piso queda una linterna de luz azul fría.",
                      "Zed levantando la linterna; en la pared se proyecta la ficha completa del Vidriero.",
                      "Por una ventana alta, el río de la capital brillando de noche."]),
        ],
    },
]
