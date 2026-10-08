from genjava import m

# R04: las Corrientes del Imperio (el río de la capital). Todo determinista: la concurrencia se espera con
# join/get y se combina en orden, para que la salida sea siempre la misma.

NODOS = [
    {
        "titulo": "R04-N01 · Streams: datos que fluyen",
        "misiones": [
            m(id="R04-N01-P1", titulo="El molino que filtra",
              lugar="La orilla del río de la capital", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="filter | lista.stream().filter(b -> b.carga() > 50).toList() · deja pasar solo lo que cumple la condición",
              recompensa="xp 10, oro 10",
              escena="""
                  Por el río bajan barcazas sin parar. En la orilla, un molino deja pasar solo las **cargadas**, sin detener el agua. Zed, que está acostumbrado a recorrer todo con un for, mira el molino un buen rato.
              """,
              sugiere="Un **stream** es una corriente de datos: `barcazas.stream()`. `filter(b -> condición)` deja pasar solo los que cumplen, y `toList()` junta lo que llegó al final en una lista.",
              desafio="Completá la condición del filtro: las barcazas con más de 50 de carga.",
              inicial='''
                  import java.util.List;

                  public class Molino {
                      public static void main(String[] args) {
                          List<Barcaza> rio = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20),
                                  new Barcaza("Bagre", 120), new Barcaza("Junco", 50));
                          List<Barcaza> cargadas = rio.stream()
                                  .filter(b -> ___)
                                  .toList();
                          System.out.println("Pasan el molino: " + cargadas);
                      }
                  }

                  record Barcaza(String nombre, int carga) {
                  }
              ''',
              solucion='''
                  import java.util.List;

                  public class Molino {
                      public static void main(String[] args) {
                          List<Barcaza> rio = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20),
                                  new Barcaza("Bagre", 120), new Barcaza("Junco", 50));
                          List<Barcaza> cargadas = rio.stream()
                                  .filter(b -> b.carga() > 50)
                                  .toList();
                          System.out.println("Pasan el molino: " + cargadas);
                      }
                  }

                  record Barcaza(String nombre, int carga) {
                  }
              ''',
              al_superar="La Garza y el Bagre pasan; el Junco, con 50 justos, se queda. El molino no paró ni un segundo. —Describís **qué** querés —dice Kaffa— y el río se ocupa del cómo.",
              imagen=["El río de la capital al atardecer, lleno de barcazas; en la orilla, un molino de bronce que desvía solo las barcazas cargadas.",
                      "Zed sentado en la orilla mirando el molino; Kaffa con su taza al lado."]),
            m(id="R04-N01-P2", titulo="El molino que transforma",
              lugar="La orilla del río de la capital", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="map y sorted | .map(Barcaza::nombre) cambia cada elemento por otro · .sorted() los ordena · se encadenan",
              recompensa="xp 10, oro 10",
              escena="""
                  Un segundo molino no filtra: **transforma**. A cada barcaza le saca el nombre y lo pinta en mayúsculas en un cartel, y los carteles salen ordenados.
              """,
              sugiere="`map(f)` cambia cada elemento por el resultado de `f`: `.map(Barcaza::nombre)` deja solo los nombres. Las operaciones se **encadenan**: `.map(...).map(String::toUpperCase).sorted()`.",
              desafio="Completá el `map` que pasa cada nombre a mayúsculas.",
              inicial='''
                  import java.util.List;

                  public class Carteles {
                      public static void main(String[] args) {
                          List<Barcaza> rio = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20), new Barcaza("Bagre", 120));
                          List<String> carteles = rio.stream()
                                  .map(Barcaza::nombre)
                                  .map(___)
                                  .sorted()
                                  .toList();
                          System.out.println(carteles);
                      }
                  }

                  record Barcaza(String nombre, int carga) {
                  }
              ''',
              solucion='''
                  import java.util.List;

                  public class Carteles {
                      public static void main(String[] args) {
                          List<Barcaza> rio = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20), new Barcaza("Bagre", 120));
                          List<String> carteles = rio.stream()
                                  .map(Barcaza::nombre)
                                  .map(String::toUpperCase)
                                  .sorted()
                                  .toList();
                          System.out.println(carteles);
                      }
                  }

                  record Barcaza(String nombre, int carga) {
                  }
              ''',
              al_superar="BAGRE, GARZA, SAUCE: tres carteles en orden, sin un solo for. Nadia los copia en su libreta y, por primera vez, no corrige nada.",
              imagen=["Un molino que convierte barcazas en carteles de madera con nombres en mayúsculas.",
                      "Nadia copiando los carteles en su libreta."]),
            m(id="R04-N01-P3", titulo="El que cuenta y suma",
              lugar="La orilla del río de la capital", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Terminales | count() cuántos · mapToInt(Barcaza::carga).sum() suma · max(), average() · el stream termina ahí",
              recompensa="xp 15, oro 15",
              escena="""
                  El tercer molino solo **cuenta**: cuántas barcazas pasaron hoy y cuánta carga trajeron entre todas. Es el último de la orilla: después de él, la corriente termina en un número.
              """,
              sugiere="Una operación **terminal** termina el stream y da un resultado: `count()`. Para sumar números, primero se pasa a un stream de `int` con `mapToInt(Barcaza::carga)` y después `sum()`.",
              desafio="Completá el `mapToInt` con la carga de cada barcaza.",
              inicial='''
                  import java.util.List;

                  public class Cuenta {
                      public static void main(String[] args) {
                          List<Barcaza> rio = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20),
                                  new Barcaza("Bagre", 120), new Barcaza("Junco", 50));
                          long cuantas = rio.stream().count();
                          int total = rio.stream().mapToInt(___).sum();
                          System.out.println("Barcazas: " + cuantas);
                          System.out.println("Carga total: " + total);
                      }
                  }

                  record Barcaza(String nombre, int carga) {
                  }
              ''',
              solucion='''
                  import java.util.List;

                  public class Cuenta {
                      public static void main(String[] args) {
                          List<Barcaza> rio = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20),
                                  new Barcaza("Bagre", 120), new Barcaza("Junco", 50));
                          long cuantas = rio.stream().count();
                          int total = rio.stream().mapToInt(Barcaza::carga).sum();
                          System.out.println("Barcazas: " + cuantas);
                          System.out.println("Carga total: " + total);
                      }
                  }

                  record Barcaza(String nombre, int carga) {
                  }
              ''',
              al_superar="Cuatro barcazas, 270 de carga. El molinero lo talla en la puerta del molino, como cada día desde hace cien años.",
              imagen=["Un molino con un contador de bronce que marca «4» y «270».",
                      "El molinero tallando los números en la puerta."]),
            m(id="R04-N01-P4", titulo="El agua no vuelve",
              lugar="La orilla del río de la capital", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="slime",
              carta="De un solo uso | un stream se recorre UNA vez · reusarlo da IllegalStateException · para otra pasada, otro .stream()",
              recompensa="xp 15, oro 15",
              escena="""
                  Zed guarda una corriente en una variable y quiere usarla dos veces: una para contar y otra para sumar. La segunda vez, del agua sale un **slime**: *stream has already been operated upon or closed*.
              """,
              sugiere="Un stream es como el agua del río: pasa **una vez**. Si lo guardás en una variable y lo usás dos veces, la segunda falla. Para otra pasada, pedí un stream nuevo a la lista: `rio.stream()`.",
              desafio="Ejecutalo, leé el error y hacé que la suma use un stream nuevo.",
              inicial='''
                  import java.util.List;
                  import java.util.stream.Stream;

                  public class AguaQueNoVuelve {
                      public static void main(String[] args) {
                          List<Integer> cargas = List.of(80, 20, 120, 50);
                          Stream<Integer> corriente = cargas.stream();
                          System.out.println("Pasaron: " + corriente.count());
                          System.out.println("Carga: " + corriente.mapToInt(c -> c).sum());
                      }
                  }
              ''',
              solucion='''
                  import java.util.List;
                  import java.util.stream.Stream;

                  public class AguaQueNoVuelve {
                      public static void main(String[] args) {
                          List<Integer> cargas = List.of(80, 20, 120, 50);
                          Stream<Integer> corriente = cargas.stream();
                          System.out.println("Pasaron: " + corriente.count());
                          System.out.println("Carga: " + cargas.stream().mapToInt(c -> c).sum());
                      }
                  }
              ''',
              al_superar="""
                  Dos corrientes, dos resultados. El slime se disuelve en el agua.
                  Río abajo, en los muelles, los recaudadores no cuentan de a una: juntan todo en **cajas** por puerto.
              """,
              imagen=["Un slime saliendo del agua del río con un cartel de «IllegalStateException».",
                      "Al fondo, los muelles con recaudadores juntando cajas por puerto."]),
        ],
    },
    {
        "titulo": "R04-N02 · Collectors y Optional",
        "misiones": [
            m(id="R04-N02-P1", titulo="Las cajas de cada puerto",
              lugar="Los muelles del río", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="groupingBy | collect(Collectors.groupingBy(Barcaza::puerto, TreeMap::new, Collectors.counting())) · un mapa: grupo → resultado",
              recompensa="xp 10, oro 10",
              escena="""
                  En los muelles, los recaudadores juntan las barcazas en **cajas por puerto de destino** y escriben cuántas hay en cada una.
              """,
              sugiere="`collect(Collectors.groupingBy(clave, …))` arma un mapa: cada clave con lo que le tocó. Con `Collectors.counting()` como segundo paso, el valor es **cuántos** hay. `TreeMap::new` deja las claves ordenadas.",
              desafio="Completá el colector que cuenta cuántas barcazas hay por puerto.",
              inicial='''
                  import java.util.List;
                  import java.util.Map;
                  import java.util.TreeMap;
                  import java.util.stream.Collectors;

                  public class Cajas {
                      public static void main(String[] args) {
                          List<Barcaza> muelle = List.of(new Barcaza("Garza", "Capital", 80), new Barcaza("Sauce", "Puerto", 20),
                                  new Barcaza("Bagre", "Capital", 120), new Barcaza("Junco", "Torre", 50), new Barcaza("Ceibo", "Puerto", 40));
                          Map<String, Long> porPuerto = muelle.stream()
                                  .collect(Collectors.groupingBy(Barcaza::puerto, TreeMap::new, Collectors.___()));
                          System.out.println(porPuerto);
                      }
                  }

                  record Barcaza(String nombre, String puerto, int carga) {
                  }
              ''',
              solucion='''
                  import java.util.List;
                  import java.util.Map;
                  import java.util.TreeMap;
                  import java.util.stream.Collectors;

                  public class Cajas {
                      public static void main(String[] args) {
                          List<Barcaza> muelle = List.of(new Barcaza("Garza", "Capital", 80), new Barcaza("Sauce", "Puerto", 20),
                                  new Barcaza("Bagre", "Capital", 120), new Barcaza("Junco", "Torre", 50), new Barcaza("Ceibo", "Puerto", 40));
                          Map<String, Long> porPuerto = muelle.stream()
                                  .collect(Collectors.groupingBy(Barcaza::puerto, TreeMap::new, Collectors.counting()));
                          System.out.println(porPuerto);
                      }
                  }

                  record Barcaza(String nombre, String puerto, int carga) {
                  }
              ''',
              al_superar="Dos a la Capital, dos al Puerto y una a la Torre. —¿Una sola barcaza a la Torre? —pregunta Zed—. Para el lugar más importante del Imperio, es poco.",
              imagen=["Los muelles del río: recaudadores con cajas etiquetadas «Capital», «Puerto» y «Torre», con barquitos de madera adentro.",
                      "Zed mirando la caja «Torre», casi vacía."]),
            m(id="R04-N02-P2", titulo="La lista en una línea",
              lugar="Los muelles del río", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="joining | collect(Collectors.joining(\", \")) une textos con un separador · joining(\", \", \"[\", \"]\") con principio y final",
              recompensa="xp 10, oro 10",
              escena="""
                  El capitán del muelle quiere los nombres de las barcazas del día **en una sola línea**, separados por coma, para gritarlos desde la torreta.
              """,
              sugiere="`Collectors.joining(\", \")` une un stream de textos en uno solo, con el separador entre cada uno. Hay que pasar primero a textos: `.map(Barcaza::nombre)`.",
              desafio="Completá el colector que une los nombres con \", \".",
              inicial='''
                  import java.util.List;
                  import java.util.stream.Collectors;

                  public class Torreta {
                      public static void main(String[] args) {
                          List<Barcaza> muelle = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20), new Barcaza("Bagre", 120));
                          String grito = muelle.stream()
                                  .map(Barcaza::nombre)
                                  .collect(Collectors.___);
                          System.out.println("¡Hoy llegan " + grito + "!");
                      }
                  }

                  record Barcaza(String nombre, int carga) {
                  }
              ''',
              solucion='''
                  import java.util.List;
                  import java.util.stream.Collectors;

                  public class Torreta {
                      public static void main(String[] args) {
                          List<Barcaza> muelle = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20), new Barcaza("Bagre", 120));
                          String grito = muelle.stream()
                                  .map(Barcaza::nombre)
                                  .collect(Collectors.joining(", "));
                          System.out.println("¡Hoy llegan " + grito + "!");
                      }
                  }

                  record Barcaza(String nombre, int carga) {
                  }
              ''',
              al_superar="El capitán lo grita desde la torreta y el muelle entero lo escucha. Sin una coma de más al final.",
              imagen=["Un capitán gritando desde una torreta de madera, con un pergamino en la mano.",
                      "Las barcazas Garza, Sauce y Bagre amarrando abajo."]),
            m(id="R04-N02-P3", titulo="Livianas y pesadas",
              lugar="Los muelles del río", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="partitioningBy | collect(Collectors.partitioningBy(b -> b.carga() > 60)) · un mapa con dos grupos: true y false",
              recompensa="xp 15, oro 15",
              escena="""
                  Las barcazas pesadas van al muelle grande y las livianas al chico. Hay **dos** grupos y nada más: o pasa la condición, o no.
              """,
              sugiere="`partitioningBy(condición)` arma un mapa con dos claves: `true` (las que cumplen) y `false` (las demás). `get(true)` da la lista de las que cumplen.",
              desafio="Completá la condición: pesadas son las de más de 60.",
              inicial='''
                  import java.util.List;
                  import java.util.Map;
                  import java.util.stream.Collectors;

                  public class DosMuelles {
                      public static void main(String[] args) {
                          List<Barcaza> muelle = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20),
                                  new Barcaza("Bagre", 120), new Barcaza("Junco", 50));
                          Map<Boolean, List<Barcaza>> grupos = muelle.stream()
                                  .collect(Collectors.partitioningBy(b -> ___));
                          System.out.println("Muelle grande: " + grupos.get(true).stream().map(Barcaza::nombre).toList());
                          System.out.println("Muelle chico: " + grupos.get(false).stream().map(Barcaza::nombre).toList());
                      }
                  }

                  record Barcaza(String nombre, int carga) {
                  }
              ''',
              solucion='''
                  import java.util.List;
                  import java.util.Map;
                  import java.util.stream.Collectors;

                  public class DosMuelles {
                      public static void main(String[] args) {
                          List<Barcaza> muelle = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20),
                                  new Barcaza("Bagre", 120), new Barcaza("Junco", 50));
                          Map<Boolean, List<Barcaza>> grupos = muelle.stream()
                                  .collect(Collectors.partitioningBy(b -> b.carga() > 60));
                          System.out.println("Muelle grande: " + grupos.get(true).stream().map(Barcaza::nombre).toList());
                          System.out.println("Muelle chico: " + grupos.get(false).stream().map(Barcaza::nombre).toList());
                      }
                  }

                  record Barcaza(String nombre, int carga) {
                  }
              ''',
              al_superar="Garza y Bagre al grande, Sauce y Junco al chico. Ni una barcaza en el muelle equivocado.",
              imagen=["Un muelle grande con dos barcazas pesadas y uno chico con dos livianas.",
                      "Gheco señalando el cartel «> 60» en la bifurcación del canal."]),
            m(id="R04-N02-P4", titulo="La barcaza que nunca llegó",
              lugar="La capitanía de los muelles", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="troll",
              carta="Optional | findFirst() devuelve un Optional: una caja que puede estar vacía · .map(...) adentro · .orElse(\"…\") si no hay nada · nunca null",
              recompensa="xp 15, oro 20",
              escena="""
                  Zed revisa el registro del río buscando una barcaza que haya llevado **un vitral**. Un **troll** espera que la búsqueda devuelva `null`… pero en las Corrientes, lo que puede no existir viene en una **caja**: un `Optional`.
              """,
              sugiere="`findFirst()` devuelve un `Optional`: una caja con el primer resultado, o vacía. `.map(Registro::estado)` transforma lo de adentro si hay algo, y `.orElse(\"…\")` da un valor por defecto si la caja está vacía.",
              desafio="Completá el valor por defecto para cuando no hay ninguna barcaza: \"ninguna\".",
              inicial='''
                  import java.util.List;

                  public class Registro {
                      public static void main(String[] args) {
                          List<Viaje> rio = List.of(new Viaje("Garza", "sal", "llegó"), new Viaje("Ceibo", "un vitral", "nunca llegó"),
                                  new Viaje("Bagre", "café", "llegó"));
                          for (String carga : List.of("un vitral", "seda")) {
                              String estado = rio.stream()
                                      .filter(v -> v.carga().equals(carga))
                                      .findFirst()
                                      .map(v -> v.barcaza() + ", " + v.estado())
                                      .orElse(___);
                              System.out.println(carga + ": " + estado);
                          }
                      }
                  }

                  record Viaje(String barcaza, String carga, String estado) {
                  }
              ''',
              solucion='''
                  import java.util.List;

                  public class Registro {
                      public static void main(String[] args) {
                          List<Viaje> rio = List.of(new Viaje("Garza", "sal", "llegó"), new Viaje("Ceibo", "un vitral", "nunca llegó"),
                                  new Viaje("Bagre", "café", "llegó"));
                          for (String carga : List.of("un vitral", "seda")) {
                              String estado = rio.stream()
                                      .filter(v -> v.carga().equals(carga))
                                      .findFirst()
                                      .map(v -> v.barcaza() + ", " + v.estado())
                                      .orElse("ninguna");
                              System.out.println(carga + ": " + estado);
                          }
                      }
                  }

                  record Viaje(String barcaza, String carga, String estado) {
                  }
              ''',
              al_superar="""
                  «un vitral: Ceibo, nunca llegó.» La barcaza del Vidriero se llamaba **Ceibo**. El troll se queda sin su `null`.
                  En el delta, un cartógrafo ordena mapas de mil maneras. Tal vez sepa dónde se perdió el Ceibo.
              """,
              imagen=["Un registro del río abierto: una línea resaltada, «Ceibo · un vitral · nunca llegó».",
                      "Zed, serio, apoyando el dedo sobre la línea; un troll yéndose con las manos vacías."]),
        ],
    },
    {
        "titulo": "R04-N03 · Comparadores y el Java moderno",
        "misiones": [
            m(id="R04-N03-P1", titulo="Los mapas del cartógrafo",
              lugar="El delta del río", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Comparadores encadenados | Comparator.comparingInt(Mapa::anio).reversed().thenComparing(Mapa::region) · sin escribir compare a mano",
              recompensa="xp 10, oro 10",
              escena="""
                  El cartógrafo del delta ordena sus mapas de mil maneras. Zed le pide los más **nuevos primero** y, si son del mismo año, por región. —Armalo con piezas —le dice el viejo—, que yo ya no tengo pulso.
              """,
              sugiere="`Comparator.comparingInt(Mapa::anio)` ordena por año; `.reversed()` lo da vuelta (más nuevos primero). `.thenComparing(Mapa::region)` desempata. Ojo: `reversed()` invierte **todo** lo que está antes.",
              desafio="Completá el desempate por región.",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.Comparator;
                  import java.util.List;

                  public class Cartografo {
                      public static void main(String[] args) {
                          List<Mapa> mapas = new ArrayList<>(List.of(new Mapa("Delta", 1203), new Mapa("Capital", 1190),
                                  new Mapa("Aduana", 1203), new Mapa("Represa", 1201)));
                          mapas.sort(Comparator.comparingInt(Mapa::anio).reversed().___(Mapa::region));
                          mapas.forEach(m -> System.out.println(m.anio() + " " + m.region()));
                      }
                  }

                  record Mapa(String region, int anio) {
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.Comparator;
                  import java.util.List;

                  public class Cartografo {
                      public static void main(String[] args) {
                          List<Mapa> mapas = new ArrayList<>(List.of(new Mapa("Delta", 1203), new Mapa("Capital", 1190),
                                  new Mapa("Aduana", 1203), new Mapa("Represa", 1201)));
                          mapas.sort(Comparator.comparingInt(Mapa::anio).reversed().thenComparing(Mapa::region));
                          mapas.forEach(m -> System.out.println(m.anio() + " " + m.region()));
                      }
                  }

                  record Mapa(String region, int anio) {
                  }
              ''',
              al_superar="Los mapas del 1203 arriba, Aduana antes que Delta. El tercero, el de 1201, tiene algo marcado en rojo: **la Represa**.",
              imagen=["La mesa del cartógrafo del delta llena de mapas ordenados en pilas.",
                      "Un mapa con una X roja sobre la Represa."]),
            m(id="R04-N03-P2", titulo="El molde que se valida solo",
              lugar="El delta del río", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="goblin",
              carta="record con validación | record Carga(String que, int kilos) { Carga { if (kilos < 0) throw …; } } · constructor compacto: valida antes de guardar",
              recompensa="xp 15, oro 15",
              escena="""
                  En el delta, los moldes son más cortos que los de la Academia: son `record`. Pero un **goblin** anota cargas con kilos negativos y nadie lo frena.
              """,
              sugiere="Un `record` puede tener un **constructor compacto**: `Carga { … }`, sin paréntesis. Adentro se validan los parámetros; las asignaciones las hace Java solo, al final. Si algo no sirve, se lanza `IllegalArgumentException`.",
              desafio="Completá la condición que rechaza los kilos negativos.",
              inicial='''
                  public class Delta {
                      public static void main(String[] args) {
                          int[] pesos = {30, -5, 0};
                          for (int k : pesos) {
                              try {
                                  System.out.println("Anotada: " + new Carga("sal", k));
                              } catch (IllegalArgumentException e) {
                                  System.out.println("Rechazada: " + e.getMessage());
                              }
                          }
                      }
                  }

                  record Carga(String que, int kilos) {
                      Carga {
                          if (___) {
                              throw new IllegalArgumentException("kilos negativos: " + kilos);
                          }
                      }
                  }
              ''',
              solucion='''
                  public class Delta {
                      public static void main(String[] args) {
                          int[] pesos = {30, -5, 0};
                          for (int k : pesos) {
                              try {
                                  System.out.println("Anotada: " + new Carga("sal", k));
                              } catch (IllegalArgumentException e) {
                                  System.out.println("Rechazada: " + e.getMessage());
                              }
                          }
                      }
                  }

                  record Carga(String que, int kilos) {
                      Carga {
                          if (kilos < 0) {
                              throw new IllegalArgumentException("kilos negativos: " + kilos);
                          }
                      }
                  }
              ''',
              al_superar="Los −5 kilos rebotan en el molde. El goblin tira su pluma al río.",
              imagen=["Un molde de bronce corto, con la palabra «record», que rechaza una carga con «-5» escrito.",
                      "Un goblin enojado tirando una pluma al agua."]),
            m(id="R04-N03-P3", titulo="Las cajas selladas",
              lugar="El delta del río", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="sealed e instanceof con patrón | sealed interface Bulto permits Caja, Barril · if (b instanceof Caja c) pregunta y castea en un paso",
              recompensa="xp 15, oro 15",
              escena="""
                  En el delta hay cajas cerradas con un sello que dice exactamente qué puede haber adentro: **solo** cajas o barriles, nada más. Zed tiene que tratar distinto a cada uno.
              """,
              sugiere="Una interfaz `sealed … permits Caja, Barril` solo deja que la implementen esas clases. `if (b instanceof Caja c)` pregunta el tipo y, si es, ya te da la variable `c` de tipo `Caja`, sin casting aparte.",
              desafio="Completá el `instanceof` con patrón: si es un `Barril`, llamalo `barril`.",
              inicial='''
                  import java.util.List;

                  public class Sellados {
                      static String describir(Bulto b) {
                          if (b instanceof Caja c) {
                              return "caja de " + c.lado() + " cm";
                          } else if (b instanceof ___) {
                              return "barril de " + barril.litros() + " litros";
                          }
                          return "desconocido";
                      }

                      public static void main(String[] args) {
                          for (Bulto b : List.of(new Caja(40), new Barril(200), new Caja(15))) {
                              System.out.println(describir(b));
                          }
                      }
                  }

                  sealed interface Bulto permits Caja, Barril {
                  }

                  record Caja(int lado) implements Bulto {
                  }

                  record Barril(int litros) implements Bulto {
                  }
              ''',
              solucion='''
                  import java.util.List;

                  public class Sellados {
                      static String describir(Bulto b) {
                          if (b instanceof Caja c) {
                              return "caja de " + c.lado() + " cm";
                          } else if (b instanceof Barril barril) {
                              return "barril de " + barril.litros() + " litros";
                          }
                          return "desconocido";
                      }

                      public static void main(String[] args) {
                          for (Bulto b : List.of(new Caja(40), new Barril(200), new Caja(15))) {
                              System.out.println(describir(b));
                          }
                      }
                  }

                  sealed interface Bulto permits Caja, Barril {
                  }

                  record Caja(int lado) implements Bulto {
                  }

                  record Barril(int litros) implements Bulto {
                  }
              ''',
              al_superar="Dos cajas y un barril, cada uno descripto a su manera. El sello garantiza que no aparezca un bulto de otro tipo a la noche.",
              imagen=["Cajas y barriles sellados con un lacre dorado que dice «permits Caja, Barril».",
                      "Zed etiquetando cada bulto."]),
            m(id="R04-N03-P4", titulo="El informe en un bloque",
              lugar="El delta del río", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Bloque de texto y var | var x = 3; deduce el tipo · \"\"\" … \"\"\" un texto de varias líneas · .formatted(…) completa los %s y %d",
              recompensa="xp 15, oro 20",
              escena="""
                  El cartógrafo le dicta a Zed un informe de varias líneas para mandar a la Torre. Con comillas y `+` por todos lados, el informe queda ilegible. —En el Java nuevo —dice Kaffa—, el texto se escribe **como se ve**.
              """,
              sugiere="Un **bloque de texto** empieza y termina con tres comillas (`\"\"\"`) y respeta los saltos de línea. `.formatted(a, b)` reemplaza los `%s` y `%d` en orden. `var` deja que el compilador deduzca el tipo.",
              desafio="Completá el método que completa los `%s` y `%d` del bloque.",
              inicial='''
                  public class Informe {
                      public static void main(String[] args) {
                          var barcaza = "Ceibo";
                          var dias = 12;
                          var informe = """
                                  Informe del delta
                                  Barcaza perdida: %s
                                  Días sin noticias: %d
                                  Último lugar visto: la Represa""".___(barcaza, dias);
                          System.out.println(informe);
                      }
                  }
              ''',
              solucion='''
                  public class Informe {
                      public static void main(String[] args) {
                          var barcaza = "Ceibo";
                          var dias = 12;
                          var informe = """
                                  Informe del delta
                                  Barcaza perdida: %s
                                  Días sin noticias: %d
                                  Último lugar visto: la Represa""".formatted(barcaza, dias);
                          System.out.println(informe);
                      }
                  }
              ''',
              al_superar="""
                  El informe sale prolijo, como un pergamino. El Ceibo se vio por última vez en **la Represa**.
                  Camino a la Represa está el astillero, donde los maestros arman los barcos con recetas que se pasan de generación en generación.
              """,
              imagen=["Un pergamino prolijo con el informe del delta, con «la Represa» subrayado.",
                      "Al fondo, el astillero con barcos a medio armar."]),
        ],
    },
    {
        "titulo": "R04-N04 · Patrones de diseño: Singleton, Factory y Strategy",
        "misiones": [
            m(id="R04-N04-P1", titulo="Una sola capitanía",
              lugar="El astillero del río", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Singleton | constructor private · una instancia static final · static get() devuelve siempre la misma · nadie hace new",
              recompensa="xp 10, oro 10",
              escena="""
                  En el astillero hay una sola capitanía para todo el río. Zed, por las dudas, intenta armarse otra propia para registrar sus barcos sin pasar por la oficial. La Aduana del compilador lo frena en seco.
              """,
              sugiere="Un **Singleton** tiene el constructor `private`: nadie puede hacer `new` desde afuera. La única instancia se pide con `Capitania.get()`.",
              desafio="Ejecutalo, leé el error y cambiá el `new` por la capitanía oficial.",
              inicial='''
                  public class UnaSola {
                      public static void main(String[] args) {
                          Capitania oficial = Capitania.get();
                          Capitania deZed = new Capitania();
                          oficial.registrar("Barcaza 1");
                          deZed.registrar("Velero de Zed");
                          System.out.println("Registrados: " + Capitania.get().cantidad());
                          System.out.println("Misma capitanía: " + (oficial == deZed));
                      }
                  }

                  final class Capitania {
                      private static final Capitania INSTANCIA = new Capitania();
                      private int registrados;

                      private Capitania() { }

                      static Capitania get() { return INSTANCIA; }

                      void registrar(String barco) { registrados++; }

                      int cantidad() { return registrados; }
                  }
              ''',
              solucion='''
                  public class UnaSola {
                      public static void main(String[] args) {
                          Capitania oficial = Capitania.get();
                          Capitania deZed = Capitania.get();
                          oficial.registrar("Barcaza 1");
                          deZed.registrar("Velero de Zed");
                          System.out.println("Registrados: " + Capitania.get().cantidad());
                          System.out.println("Misma capitanía: " + (oficial == deZed));
                      }
                  }

                  final class Capitania {
                      private static final Capitania INSTANCIA = new Capitania();
                      private int registrados;

                      private Capitania() { }

                      static Capitania get() { return INSTANCIA; }

                      void registrar(String barco) { registrados++; }

                      int cantidad() { return registrados; }
                  }
              ''',
              al_superar="Dos registros en la misma capitanía. —Hace un mes te hubieras armado una paralela —dice Nadia. —Hace un mes no sabía que el constructor era privado —responde Zed.",
              imagen=["Una única capitanía de piedra sobre el astillero, con un solo libro de registros.",
                      "Zed con un sello improvisado roto en la mano; Nadia de brazos cruzados."]),
            m(id="R04-N04-P2", titulo="El barco del pedido",
              lugar="El astillero del río", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Factory | Fabrica.crear(\"carga\") devuelve un Barco · quien pide solo conoce la interfaz · las clases concretas, en un solo lugar",
              recompensa="xp 10, oro 10",
              escena="""
                  Al astillero llegan pedidos por tipo: «carga», «rápido», «pesca». El que pide no sabe armar barcos y no tiene por qué: la **fábrica** decide qué clase construir.
              """,
              sugiere="Una **Factory** es un método que recibe el pedido y devuelve el objeto, del tipo de la interfaz: `static Barco crear(String tipo)`. Adentro, un `switch` elige la clase.",
              desafio="Completá el caso que falta: el tipo \"pesca\" arma un `Pesquero`.",
              inicial='''
                  public class Pedidos {
                      public static void main(String[] args) {
                          for (String pedido : new String[] {"carga", "pesca", "rapido"}) {
                              System.out.println(pedido + " -> " + Fabrica.crear(pedido).descripcion());
                          }
                      }
                  }

                  interface Barco {
                      String descripcion();
                  }

                  class Barcaza implements Barco {
                      public String descripcion() { return "barcaza ancha"; }
                  }

                  class Velero implements Barco {
                      public String descripcion() { return "velero rápido"; }
                  }

                  class Pesquero implements Barco {
                      public String descripcion() { return "pesquero con redes"; }
                  }

                  class Fabrica {
                      static Barco crear(String tipo) {
                          return switch (tipo) {
                              case "carga" -> new Barcaza();
                              case "rapido" -> new Velero();
                              ___
                              default -> throw new IllegalArgumentException("no sé armar " + tipo);
                          };
                      }
                  }
              ''',
              solucion='''
                  public class Pedidos {
                      public static void main(String[] args) {
                          for (String pedido : new String[] {"carga", "pesca", "rapido"}) {
                              System.out.println(pedido + " -> " + Fabrica.crear(pedido).descripcion());
                          }
                      }
                  }

                  interface Barco {
                      String descripcion();
                  }

                  class Barcaza implements Barco {
                      public String descripcion() { return "barcaza ancha"; }
                  }

                  class Velero implements Barco {
                      public String descripcion() { return "velero rápido"; }
                  }

                  class Pesquero implements Barco {
                      public String descripcion() { return "pesquero con redes"; }
                  }

                  class Fabrica {
                      static Barco crear(String tipo) {
                          return switch (tipo) {
                              case "carga" -> new Barcaza();
                              case "rapido" -> new Velero();
                              case "pesca" -> new Pesquero();
                              default -> throw new IllegalArgumentException("no sé armar " + tipo);
                          };
                      }
                  }
              ''',
              al_superar="Tres pedidos, tres barcos, y el `main` no hizo un solo `new Barcaza()`. Si mañana hay un barco nuevo, cambia un solo lugar.",
              imagen=["La fábrica del astillero: una grúa de bronce armando un pesquero con redes según un pedido escrito.",
                      "Un maestro constructor leyendo la lista de pedidos."]),
            m(id="R04-N04-P3", titulo="La tarifa de feria",
              lugar="La capitanía del astillero", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Strategy | interface Recargo { int calcular(int dias); } · una clase por forma de calcular · la Aduana recibe la que toque y delega",
              recompensa="xp 15, oro 15",
              escena="""
                  Los barcos que se demoran en el astillero pagan un recargo, y la forma de calcularlo cambia según la época. En feria, los primeros 3 días son gratis. —Esto es lo que te van a pedir en el examen —le dice Kaffa a Zed, que no sabía que iba a haber un examen.
              """,
              sugiere="Cada forma de calcular es una clase que implementa `Recargo`. La `Aduana` no pregunta cuál es: llama a `recargo.calcular(dias)`. En feria: si los días son 3 o menos, 0; si no, 10 por cada día después del tercero.",
              desafio="Completá el `return` de `RecargoFeria`.",
              inicial='''
                  public class Feria {
                      public static void main(String[] args) {
                          Aduana aduana = new Aduana(new RecargoNormal());
                          System.out.println("Normal, 5 días: " + aduana.recargo(5));
                          aduana.setRecargo(new RecargoFeria());
                          System.out.println("Feria, 2 días: " + aduana.recargo(2));
                          System.out.println("Feria, 5 días: " + aduana.recargo(5));
                      }
                  }

                  interface Recargo {
                      int calcular(int dias);
                  }

                  class RecargoNormal implements Recargo {
                      public int calcular(int dias) { return dias * 10; }
                  }

                  class RecargoFeria implements Recargo {
                      public int calcular(int dias) {
                          return ___;
                      }
                  }

                  class Aduana {
                      private Recargo recargo;

                      Aduana(Recargo recargo) { this.recargo = recargo; }

                      void setRecargo(Recargo recargo) { this.recargo = recargo; }

                      int recargo(int dias) { return recargo.calcular(dias); }
                  }
              ''',
              solucion='''
                  public class Feria {
                      public static void main(String[] args) {
                          Aduana aduana = new Aduana(new RecargoNormal());
                          System.out.println("Normal, 5 días: " + aduana.recargo(5));
                          aduana.setRecargo(new RecargoFeria());
                          System.out.println("Feria, 2 días: " + aduana.recargo(2));
                          System.out.println("Feria, 5 días: " + aduana.recargo(5));
                      }
                  }

                  interface Recargo {
                      int calcular(int dias);
                  }

                  class RecargoNormal implements Recargo {
                      public int calcular(int dias) { return dias * 10; }
                  }

                  class RecargoFeria implements Recargo {
                      public int calcular(int dias) {
                          return dias <= 3 ? 0 : (dias - 3) * 10;
                      }
                  }

                  class Aduana {
                      private Recargo recargo;

                      Aduana(Recargo recargo) { this.recargo = recargo; }

                      void setRecargo(Recargo recargo) { this.recargo = recargo; }

                      int recargo(int dias) { return recargo.calcular(dias); }
                  }
              ''',
              al_superar="Cincuenta en época normal, veinte en feria, y la Aduana no tiene un solo `if` sobre la época. —¿Examen? —pregunta Zed. —Al final de la Torre —dice Kaffa, y no agrega nada.",
              imagen=["Dos tablillas de tarifas colgadas en la capitanía: «Normal» y «Feria», intercambiables en el mismo gancho.",
                      "Kaffa tomando café; Zed preocupado por la palabra «examen»."]),
            m(id="R04-N04-P4", titulo="La estrategia en una línea",
              lugar="La capitanía del astillero", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Strategy con lambda | si la interfaz tiene un solo método, la estrategia puede ser una lambda · aduana.setRecargo(dias -> dias * 5)",
              recompensa="xp 15, oro 20",
              escena="""
                  Para la noche de la crecida, la capitanía decide un recargo especial que se usa una sola vez: 5 por día. Escribir una clase entera para eso es demasiado. —`Recargo` tiene un solo método —dice Gheco—. Ya sabés qué significa.
              """,
              sugiere="Como `Recargo` tiene **un solo** método, cualquier lambda `dias -> …` sirve como estrategia. Es lo mismo que hacés con `Comparator` cuando ordenás.",
              desafio="Completá la lambda del recargo de la crecida: 5 por día.",
              inicial='''
                  public class Crecida {
                      public static void main(String[] args) {
                          Aduana aduana = new Aduana(dias -> dias * 10);
                          System.out.println("Normal, 4 días: " + aduana.recargo(4));
                          aduana.setRecargo(dias -> ___);
                          System.out.println("Crecida, 4 días: " + aduana.recargo(4));
                      }
                  }

                  interface Recargo {
                      int calcular(int dias);
                  }

                  class Aduana {
                      private Recargo recargo;

                      Aduana(Recargo recargo) { this.recargo = recargo; }

                      void setRecargo(Recargo recargo) { this.recargo = recargo; }

                      int recargo(int dias) { return recargo.calcular(dias); }
                  }
              ''',
              solucion='''
                  public class Crecida {
                      public static void main(String[] args) {
                          Aduana aduana = new Aduana(dias -> dias * 10);
                          System.out.println("Normal, 4 días: " + aduana.recargo(4));
                          aduana.setRecargo(dias -> dias * 5);
                          System.out.println("Crecida, 4 días: " + aduana.recargo(4));
                      }
                  }

                  interface Recargo {
                      int calcular(int dias);
                  }

                  class Aduana {
                      private Recargo recargo;

                      Aduana(Recargo recargo) { this.recargo = recargo; }

                      void setRecargo(Recargo recargo) { this.recargo = recargo; }

                      int recargo(int dias) { return recargo.calcular(dias); }
                  }
              ''',
              al_superar="""
                  Una estrategia de una línea, para una sola noche. Zed se da cuenta de que lleva semanas usando patrones sin saberlo: cada `Comparator` era una Strategy.
                  Río abajo, las esclusas no dan abasto: hay que abrir varias **a la vez**.
              """,
              imagen=["Una tablilla de tarifa escrita a mano, en una sola línea, colgada sobre las otras.",
                      "Al fondo, las esclusas del río con una fila larguísima de barcazas esperando."]),
        ],
    },
    {
        "titulo": "R04-N05 · Concurrencia: muchas corrientes a la vez",
        "misiones": [
            m(id="R04-N05-P1", titulo="Dos esclusas a la vez",
              lugar="Las esclusas del río", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Thread y join | new Thread(() -> …).start() arranca otra corriente · t.join() espera a que termine · sin join, el main no espera",
              recompensa="xp 10, oro 10",
              escena="""
                  Una sola esclusa no da abasto. Kaffa abre dos **a la vez**, cada una con su fila de barcazas. Zed, que siempre trabajó solo, tiene que aprender a **repartir el trabajo**… y a esperar que todos terminen antes de cantar el total.
              """,
              sugiere="Un `Thread` corre una tarea en paralelo: `new Thread(() -> …)` y `start()`. `join()` hace que el `main` **espere** a que ese hilo termine. Cada esclusa guarda su resultado en su propio lugar del array: no se pisan.",
              desafio="Completá el método que espera a que cada esclusa termine.",
              inicial='''
                  public class Esclusas {
                      public static void main(String[] args) throws InterruptedException {
                          int[][] filas = {{80, 20, 120}, {50, 40, 60, 30}};
                          int[] totales = new int[2];
                          Thread[] esclusas = new Thread[2];
                          for (int i = 0; i < 2; i++) {
                              int n = i;
                              esclusas[i] = new Thread(() -> {
                                  for (int carga : filas[n]) {
                                      totales[n] += carga;
                                  }
                              });
                              esclusas[i].start();
                          }
                          for (Thread t : esclusas) {
                              t.___();
                          }
                          System.out.println("Esclusa 1: " + totales[0]);
                          System.out.println("Esclusa 2: " + totales[1]);
                          System.out.println("Total del día: " + (totales[0] + totales[1]));
                      }
                  }
              ''',
              solucion='''
                  public class Esclusas {
                      public static void main(String[] args) throws InterruptedException {
                          int[][] filas = {{80, 20, 120}, {50, 40, 60, 30}};
                          int[] totales = new int[2];
                          Thread[] esclusas = new Thread[2];
                          for (int i = 0; i < 2; i++) {
                              int n = i;
                              esclusas[i] = new Thread(() -> {
                                  for (int carga : filas[n]) {
                                      totales[n] += carga;
                                  }
                              });
                              esclusas[i].start();
                          }
                          for (Thread t : esclusas) {
                              t.join();
                          }
                          System.out.println("Esclusa 1: " + totales[0]);
                          System.out.println("Esclusa 2: " + totales[1]);
                          System.out.println("Total del día: " + (totales[0] + totales[1]));
                      }
                  }
              ''',
              al_superar="Las dos esclusas terminan y recién ahí se canta el total: 400. —Si cantabas antes —dice Kaffa—, decías cualquier cosa. Esperar también es parte del trabajo.",
              imagen=["Dos esclusas de piedra abiertas a la vez, con dos filas de barcazas pasando.",
                      "Zed con un reloj de arena en la mano, esperando; Kaffa a su lado."]),
            m(id="R04-N05-P2", titulo="El capataz de las esclusas",
              lugar="Las esclusas del río", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="ExecutorService y Future | pool.submit(() -> valor) devuelve un Future · f.get() espera y da el resultado · pool.shutdown() al final",
              recompensa="xp 15, oro 15",
              escena="""
                  Crear un hilo para cada barcaza es un lío. El capataz de las esclusas tiene **dos ayudantes fijos** y les va pasando tareas; cada tarea le deja un **recibo** para retirar el resultado cuando esté listo.
              """,
              sugiere="Un `ExecutorService` es un capataz con hilos fijos: `Executors.newFixedThreadPool(2)`. `submit(() -> valor)` le pasa una tarea y devuelve un `Future` (el recibo). `f.get()` espera y devuelve el resultado. Al final, `shutdown()`.",
              desafio="Completá el método del recibo que espera y devuelve el resultado.",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.List;
                  import java.util.concurrent.ExecutorService;
                  import java.util.concurrent.Executors;
                  import java.util.concurrent.Future;

                  public class Capataz {
                      public static void main(String[] args) throws Exception {
                          ExecutorService pool = Executors.newFixedThreadPool(2);
                          List<Future<Integer>> recibos = new ArrayList<>();
                          for (int carga : new int[] {80, 20, 120}) {
                              recibos.add(pool.submit(() -> carga / 2));
                          }
                          int i = 1;
                          for (Future<Integer> f : recibos) {
                              System.out.println("Peaje de la barcaza " + i++ + ": " + f.___());
                          }
                          pool.shutdown();
                      }
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.List;
                  import java.util.concurrent.ExecutorService;
                  import java.util.concurrent.Executors;
                  import java.util.concurrent.Future;

                  public class Capataz {
                      public static void main(String[] args) throws Exception {
                          ExecutorService pool = Executors.newFixedThreadPool(2);
                          List<Future<Integer>> recibos = new ArrayList<>();
                          for (int carga : new int[] {80, 20, 120}) {
                              recibos.add(pool.submit(() -> carga / 2));
                          }
                          int i = 1;
                          for (Future<Integer> f : recibos) {
                              System.out.println("Peaje de la barcaza " + i++ + ": " + f.get());
                          }
                          pool.shutdown();
                      }
                  }
              ''',
              al_superar="Tres recibos, tres peajes, retirados en orden aunque los ayudantes hayan terminado en cualquier orden. El capataz cierra la ventanilla.",
              imagen=["Un capataz en una casilla de las esclusas entregando recibos de papel; dos ayudantes trabajando atrás.",
                      "Una pila de recibos con números."]),
            m(id="R04-N05-P3", titulo="El contador que pierde barcazas",
              lugar="Las esclusas del río", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="orco",
              carta="synchronized | dos hilos que hacen contador++ a la vez pierden cuentas (condición de carrera) · synchronized deja entrar de a uno",
              recompensa="xp 15, oro 15",
              escena="""
                  Las dos esclusas anotan en el **mismo** contador. Al final del día, faltan barcazas: cuando las dos suman a la vez, una cuenta se pisa con la otra. Un **orco** se ríe en la casilla: es la condición de carrera.
              """,
              sugiere="`total++` parece una sola cosa, pero son tres: leer, sumar y guardar. Si dos hilos lo hacen a la vez, se pierden sumas. Un método `synchronized` deja entrar **de a un hilo por vez**.",
              desafio="Completá la palabra que hace que `sumar` atienda de a un hilo por vez.",
              inicial='''
                  public class Contador {
                      public static void main(String[] args) throws InterruptedException {
                          Casilla casilla = new Casilla();
                          Runnable esclusa = () -> {
                              for (int i = 0; i < 100000; i++) {
                                  casilla.sumar();
                              }
                          };
                          Thread a = new Thread(esclusa);
                          Thread b = new Thread(esclusa);
                          a.start();
                          b.start();
                          a.join();
                          b.join();
                          System.out.println("Barcazas contadas: " + casilla.total());
                      }
                  }

                  class Casilla {
                      private int total;

                      ___ void sumar() {
                          total++;
                      }

                      int total() {
                          return total;
                      }
                  }
              ''',
              solucion='''
                  public class Contador {
                      public static void main(String[] args) throws InterruptedException {
                          Casilla casilla = new Casilla();
                          Runnable esclusa = () -> {
                              for (int i = 0; i < 100000; i++) {
                                  casilla.sumar();
                              }
                          };
                          Thread a = new Thread(esclusa);
                          Thread b = new Thread(esclusa);
                          a.start();
                          b.start();
                          a.join();
                          b.join();
                          System.out.println("Barcazas contadas: " + casilla.total());
                      }
                  }

                  class Casilla {
                      private int total;

                      synchronized void sumar() {
                          total++;
                      }

                      int total() {
                          return total;
                      }
                  }
              ''',
              al_superar="Doscientas mil, exactas. El orco sale de la casilla: con una puerta para uno, ya no puede meterse entre dos cuentas. —Lo compartido se cuida —dice Kaffa—. Es lo que más cuesta aprender.",
              imagen=["Una casilla con una puerta angosta por la que pasa un solo hilo de luz a la vez.",
                      "Un orco expulsado de la casilla, con un ábaco roto."]),
            m(id="R04-N05-P4", titulo="Dos presupuestos, una respuesta",
              lugar="Las esclusas del río", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="CompletableFuture | supplyAsync(() -> …) arranca una tarea · thenCombine(otra, Integer::sum) junta dos resultados · join() espera el final",
              recompensa="xp 15, oro 20",
              escena="""
                  Para reparar la esclusa grande hacen falta dos presupuestos: el de la madera y el de las piedras. Se piden **a la vez**, y cuando estén los dos, se suman.
              """,
              sugiere="`CompletableFuture.supplyAsync(() -> valor)` arranca una tarea en otro hilo. `a.thenCombine(b, Integer::sum)` arma una tarea que, cuando terminen `a` y `b`, suma sus resultados. `join()` espera el final.",
              desafio="Completá el método que combina los dos presupuestos.",
              inicial='''
                  import java.util.concurrent.CompletableFuture;

                  public class Presupuesto {
                      public static void main(String[] args) {
                          CompletableFuture<Integer> madera = CompletableFuture.supplyAsync(() -> 120);
                          CompletableFuture<Integer> piedras = CompletableFuture.supplyAsync(() -> 80);
                          int total = madera.___(piedras, Integer::sum).join();
                          System.out.println("Reparar la esclusa cuesta " + total + " denarios");
                      }
                  }
              ''',
              solucion='''
                  import java.util.concurrent.CompletableFuture;

                  public class Presupuesto {
                      public static void main(String[] args) {
                          CompletableFuture<Integer> madera = CompletableFuture.supplyAsync(() -> 120);
                          CompletableFuture<Integer> piedras = CompletableFuture.supplyAsync(() -> 80);
                          int total = madera.thenCombine(piedras, Integer::sum).join();
                          System.out.println("Reparar la esclusa cuesta " + total + " denarios");
                      }
                  }
              ''',
              al_superar="""
                  Doscientos denarios, sin esperar uno para pedir el otro. La esclusa se repara esa misma tarde.
                  A la noche, el agua de la Represa empieza a moverse sola. Algo enorme respira debajo.
              """,
              imagen=["Dos mensajeros llegando a la vez con presupuestos que se juntan en uno solo.",
                      "La Represa de noche, con el agua agitándose y una sombra enorme debajo."]),
        ],
    },
    {
        "titulo": "R04-N06 · Jefe de las Corrientes: el Leviatán de los Datos",
        "misiones": [
            m(id="R04-N06-P1", titulo="Ni una línea perdida",
              lugar="La Represa", personajes="Zed, Gheco, Nadia, Kaffa, el Leviatán de los Datos",
              criatura="dragon",
              carta="Clasificar sin perder | sealed interface Resultado permits Valido, Rechazado · cada línea termina en uno de los dos, con su motivo",
              recompensa="xp 20, oro 20",
              escena="""
                  En la Represa, el **Leviatán de los Datos** traga registros por miles, mezcla los buenos con los rotos y devuelve informes que nadie entiende. —No se lo vence con un bucle y cien `if` —dice Kaffa—. Primero: separá lo **válido** de lo **inválido**, sin perder ni una línea.
              """,
              sugiere="Cada línea se convierte en un `Resultado`: un `Valido` con la barcaza o un `Rechazado` con la línea y el **motivo**. Así ninguna se pierde. Una línea es inválida si no tiene dos partes separadas por `;`.",
              desafio="Completá el `Rechazado` con la línea y el motivo \"le falta el ;\".",
              inicial='''
                  import java.util.List;

                  public class Leviatan1 {
                      static Resultado leer(String linea) {
                          String[] partes = linea.split(";");
                          if (partes.length != 2) {
                              return ___;
                          }
                          return new Valido(new Barcaza(partes[0], Integer.parseInt(partes[1])));
                      }

                      public static void main(String[] args) {
                          for (String linea : List.of("Garza;80", "Ceibo", "Bagre;120")) {
                              System.out.println(leer(linea));
                          }
                      }
                  }

                  record Barcaza(String nombre, int carga) {
                  }

                  sealed interface Resultado permits Valido, Rechazado {
                  }

                  record Valido(Barcaza barcaza) implements Resultado {
                  }

                  record Rechazado(String linea, String motivo) implements Resultado {
                  }
              ''',
              solucion='''
                  import java.util.List;

                  public class Leviatan1 {
                      static Resultado leer(String linea) {
                          String[] partes = linea.split(";");
                          if (partes.length != 2) {
                              return new Rechazado(linea, "le falta el ;");
                          }
                          return new Valido(new Barcaza(partes[0], Integer.parseInt(partes[1])));
                      }

                      public static void main(String[] args) {
                          for (String linea : List.of("Garza;80", "Ceibo", "Bagre;120")) {
                              System.out.println(leer(linea));
                          }
                      }
                  }

                  record Barcaza(String nombre, int carga) {
                  }

                  sealed interface Resultado permits Valido, Rechazado {
                  }

                  record Valido(Barcaza barcaza) implements Resultado {
                  }

                  record Rechazado(String linea, String motivo) implements Resultado {
                  }
              ''',
              al_superar="Tres líneas, tres resultados, ninguna tragada. El Leviatán sacude la cola: por primera vez, alguien le pide cuentas por cada registro.",
              imagen=["El Leviatán de los Datos: una serpiente marina gigante hecha de registros y números que brillan, saliendo del agua de la Represa.",
                      "Zed frente a él, con dos canastos: «válido» y «rechazado»; Nadia, Gheco y Kaffa atrás."]),
            m(id="R04-N06-P2", titulo="El informe que se entiende",
              lugar="La Represa", personajes="Zed, Gheco, Nadia, Kaffa, el Leviatán de los Datos",
              carta="Resumir con Collectors | groupingBy(…, TreeMap::new, summingInt(…)) · un mapa ordenado: grupo → suma",
              recompensa="xp 20, oro 20",
              escena="""
                  El Leviatán devuelve informes que nadie entiende. Zed le contesta con uno que **sí**: la carga total que entró por cada puerto de origen.
              """,
              sugiere="`Collectors.groupingBy(Barcaza::origen, TreeMap::new, Collectors.summingInt(Barcaza::carga))` agrupa por origen y **suma** la carga de cada grupo, con los orígenes ordenados.",
              desafio="Completá el colector que suma la carga de cada grupo.",
              inicial='''
                  import java.util.List;
                  import java.util.Map;
                  import java.util.TreeMap;
                  import java.util.stream.Collectors;

                  public class Leviatan2 {
                      public static void main(String[] args) {
                          List<Barcaza> validas = List.of(new Barcaza("Garza", "Delta", 80), new Barcaza("Bagre", "Puerto", 120),
                                  new Barcaza("Junco", "Delta", 50), new Barcaza("Sauce", "Puerto", 20));
                          Map<String, Integer> porOrigen = validas.stream()
                                  .collect(Collectors.groupingBy(Barcaza::origen, TreeMap::new, Collectors.___(Barcaza::carga)));
                          porOrigen.forEach((origen, total) -> System.out.println(origen + ": " + total));
                      }
                  }

                  record Barcaza(String nombre, String origen, int carga) {
                  }
              ''',
              solucion='''
                  import java.util.List;
                  import java.util.Map;
                  import java.util.TreeMap;
                  import java.util.stream.Collectors;

                  public class Leviatan2 {
                      public static void main(String[] args) {
                          List<Barcaza> validas = List.of(new Barcaza("Garza", "Delta", 80), new Barcaza("Bagre", "Puerto", 120),
                                  new Barcaza("Junco", "Delta", 50), new Barcaza("Sauce", "Puerto", 20));
                          Map<String, Integer> porOrigen = validas.stream()
                                  .collect(Collectors.groupingBy(Barcaza::origen, TreeMap::new, Collectors.summingInt(Barcaza::carga)));
                          porOrigen.forEach((origen, total) -> System.out.println(origen + ": " + total));
                      }
                  }

                  record Barcaza(String nombre, String origen, int carga) {
                  }
              ''',
              al_superar="«Delta: 130. Puerto: 140.» Dos líneas que cualquiera entiende. El Leviatán pierde un anillo de registros, que se hunde en el agua.",
              imagen=["Un pergamino corto y claro flotando frente al Leviatán, con dos líneas de totales.",
                      "Un anillo de registros desprendiéndose del cuerpo del Leviatán."]),
            m(id="R04-N06-P3", titulo="La respuesta que puede no existir",
              lugar="La Represa", personajes="Zed, Gheco, Nadia, Kaffa, el Leviatán de los Datos",
              carta="max y Optional | stream().max(Comparator.comparingInt(…)) devuelve un Optional · .map(…).orElse(…) responde aunque no haya nada",
              recompensa="xp 20, oro 25",
              item="Remo de las Corrientes",
              escena="""
                  El Leviatán pregunta, con voz de agua: **¿cuál es la barcaza más cargada que entró desde la Torre?** Si Zed responde `null`, el Leviatán se lo traga. Desde la Torre no entró ninguna.
              """,
              sugiere="`max(comparador)` devuelve un `Optional`: puede estar vacío si no hay ninguna. `.map(Barcaza::nombre).orElse(\"ninguna\")` responde siempre, sin `null`.",
              desafio="Completá el comparador del `max`: por carga.",
              inicial='''
                  import java.util.Comparator;
                  import java.util.List;

                  public class Leviatan3 {
                      static String masCargada(List<Barcaza> barcazas, String origen) {
                          return barcazas.stream()
                                  .filter(b -> b.origen().equals(origen))
                                  .max(Comparator.comparingInt(___))
                                  .map(Barcaza::nombre)
                                  .orElse("ninguna");
                      }

                      public static void main(String[] args) {
                          List<Barcaza> validas = List.of(new Barcaza("Garza", "Delta", 80), new Barcaza("Bagre", "Puerto", 120),
                                  new Barcaza("Junco", "Delta", 50));
                          for (String origen : List.of("Delta", "Puerto", "Torre")) {
                              System.out.println(origen + ": " + masCargada(validas, origen));
                          }
                      }
                  }

                  record Barcaza(String nombre, String origen, int carga) {
                  }
              ''',
              solucion='''
                  import java.util.Comparator;
                  import java.util.List;

                  public class Leviatan3 {
                      static String masCargada(List<Barcaza> barcazas, String origen) {
                          return barcazas.stream()
                                  .filter(b -> b.origen().equals(origen))
                                  .max(Comparator.comparingInt(Barcaza::carga))
                                  .map(Barcaza::nombre)
                                  .orElse("ninguna");
                      }

                      public static void main(String[] args) {
                          List<Barcaza> validas = List.of(new Barcaza("Garza", "Delta", 80), new Barcaza("Bagre", "Puerto", 120),
                                  new Barcaza("Junco", "Delta", 50));
                          for (String origen : List.of("Delta", "Puerto", "Torre")) {
                              System.out.println(origen + ": " + masCargada(validas, origen));
                          }
                      }
                  }

                  record Barcaza(String nombre, String origen, int carga) {
                  }
              ''',
              al_superar="«Torre: ninguna.» Una respuesta, aunque sea vacía. El Leviatán se queda sin presa y suelta lo que tenía entre los dientes: un **remo** de madera clara que brilla con las corrientes. Zed lo agarra: el **Remo de las Corrientes**.",
              imagen=["El Leviatán abriendo la boca, sorprendido; un remo de madera clara cayendo al agua con líneas de luz como corrientes.",
                      "Zed atrapando el remo en el aire."]),
            m(id="R04-N06-P4", titulo="Dos corrientes, el mismo resultado",
              lugar="La Represa", personajes="Zed, Gheco, Nadia, Kaffa, el Leviatán de los Datos",
              carta="Concurrente y verificable | se reparte el trabajo en partes que NO comparten nada · cada parte da su resultado · se combinan · da igual que en secuencia",
              recompensa="xp 25, oro 30",
              item="Vitral del Viajero",
              escena="""
                  El último truco del Leviatán es la cantidad: millones de registros. Zed reparte el trabajo en **dos mitades**, cada una con su propio hilo y sin compartir nada, y después junta los resultados. —Y demostrá que da lo mismo que hacerlo de a uno —dice Kaffa—. Al Leviatán no se le cree nada sin comprobarlo.
              """,
              sugiere="Cada mitad se procesa en su tarea (`pool.submit`) y devuelve su suma; nadie toca una variable compartida. Al final se suman las dos partes con `get()` y se compara con el cálculo en secuencia.",
              desafio="Completá la suma de las dos mitades con sus recibos.",
              inicial='''
                  import java.util.List;
                  import java.util.concurrent.ExecutorService;
                  import java.util.concurrent.Executors;
                  import java.util.concurrent.Future;
                  import java.util.stream.IntStream;

                  public class Leviatan4 {
                      public static void main(String[] args) throws Exception {
                          List<Integer> cargas = IntStream.rangeClosed(1, 100000).map(i -> i % 97).boxed().toList();
                          int mitad = cargas.size() / 2;
                          ExecutorService pool = Executors.newFixedThreadPool(2);
                          Future<Integer> a = pool.submit(() -> cargas.subList(0, mitad).stream().mapToInt(c -> c).sum());
                          Future<Integer> b = pool.submit(() -> cargas.subList(mitad, cargas.size()).stream().mapToInt(c -> c).sum());
                          int enParalelo = ___;
                          pool.shutdown();
                          int enSecuencia = cargas.stream().mapToInt(c -> c).sum();
                          System.out.println("En paralelo: " + enParalelo);
                          System.out.println("En secuencia: " + enSecuencia);
                          System.out.println("Iguales: " + (enParalelo == enSecuencia));
                      }
                  }
              ''',
              solucion='''
                  import java.util.List;
                  import java.util.concurrent.ExecutorService;
                  import java.util.concurrent.Executors;
                  import java.util.concurrent.Future;
                  import java.util.stream.IntStream;

                  public class Leviatan4 {
                      public static void main(String[] args) throws Exception {
                          List<Integer> cargas = IntStream.rangeClosed(1, 100000).map(i -> i % 97).boxed().toList();
                          int mitad = cargas.size() / 2;
                          ExecutorService pool = Executors.newFixedThreadPool(2);
                          Future<Integer> a = pool.submit(() -> cargas.subList(0, mitad).stream().mapToInt(c -> c).sum());
                          Future<Integer> b = pool.submit(() -> cargas.subList(mitad, cargas.size()).stream().mapToInt(c -> c).sum());
                          int enParalelo = a.get() + b.get();
                          pool.shutdown();
                          int enSecuencia = cargas.stream().mapToInt(c -> c).sum();
                          System.out.println("En paralelo: " + enParalelo);
                          System.out.println("En secuencia: " + enSecuencia);
                          System.out.println("Iguales: " + (enParalelo == enSecuencia));
                      }
                  }
              ''',
              al_superar="""
                  «Iguales: true.» El Leviatán se deshace en millones de registros ordenados que el río se lleva mansamente.
                  Detrás de él, encallada en la Represa, está la barcaza **Ceibo**. Adentro, envuelto en lona, hay **un vitral**: el **Vitral del Viajero**. Tiene una etiqueta: «para la ventana más alta de la Torre del Arquitecto».
              """,
              imagen=["El Leviatán deshaciéndose en una lluvia de registros luminosos que el río se lleva.",
                      "La barcaza Ceibo encallada; Zed desenvolviendo un vitral de colores envuelto en lona, con una etiqueta atada.",
                      "Al fondo, la Torre del Arquitecto recortada contra el cielo."]),
        ],
    },
]
