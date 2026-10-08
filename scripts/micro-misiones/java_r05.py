from genjava import m

# R05: la Torre del Arquitecto. Spring se imita con Java puro (D96: el ejecutor corre un solo archivo, sin
# librerías): un contenedor chiquito, la inyección por constructor, un controlador que arma el JSON y un DTO
# validado. Spring, Lombok y Postman de verdad, en las prácticas que corrige el docente.

NODOS = [
    {
        "titulo": "R05-N01 · Eficiencia: Big O y medir tiempos",
        "misiones": [
            m(id="R05-N01-P1", titulo="No discutan: cuenten",
              lugar="La sala de las balanzas del tiempo", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Contar pasos | un contador adentro del bucle · cuántas vueltas da según n · eso es lo que mide la O grande",
              recompensa="xp 10, oro 10",
              escena="""
                  En el primer piso de la Torre, dos aprendices discuten cuál de sus algoritmos es más rápido. Kaffa deja un reloj sobre la mesa, pero Gheco tiene una idea mejor: **contar** cuántos pasos da cada uno.
              """,
              sugiere="Para comparar algoritmos sin depender de la compu, se cuentan los pasos: una variable `pasos` que suma 1 en cada vuelta. Una búsqueda lineal en el peor caso mira **todos** los elementos.",
              desafio="Sumá un paso en cada vuelta del bucle.",
              inicial='''
                  public class Balanza {
                      public static void main(String[] args) {
                          for (int n : new int[] {10, 100, 1000}) {
                              int pasos = 0;
                              for (int i = 0; i < n; i++) {
                                  ___;
                              }
                              System.out.println("n = " + n + ": " + pasos + " pasos");
                          }
                      }
                  }
              ''',
              solucion='''
                  public class Balanza {
                      public static void main(String[] args) {
                          for (int n : new int[] {10, 100, 1000}) {
                              int pasos = 0;
                              for (int i = 0; i < n; i++) {
                                  pasos++;
                              }
                              System.out.println("n = " + n + ": " + pasos + " pasos");
                          }
                      }
                  }
              ''',
              al_superar="Diez veces más datos, diez veces más pasos. —Eso es **O(n)** —dice Gheco—: crece igual que los datos. Los aprendices dejan de gritar y se ponen a contar.",
              imagen=["La sala de las balanzas del tiempo: balanzas de bronce con relojes de arena en vez de pesas.",
                      "Dos aprendices discutiendo; Gheco con un ábaco de luz contando pasos."]),
            m(id="R05-N01-P2", titulo="Dos bucles, n al cuadrado",
              lugar="La sala de las balanzas del tiempo", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="ogro",
              carta="O(n²) | un bucle adentro de otro sobre los mismos datos · con el doble de datos, cuatro veces más pasos",
              recompensa="xp 10, oro 10",
              escena="""
                  El segundo aprendiz compara cada pasaporte con todos los demás. Con pocos anda; con muchos, la Aduana entera espera. Un **ogro** sonríe: el programa funciona, pero no termina nunca.
              """,
              sugiere="Dos bucles anidados que comparan cada par: `for i … for j = i + 1 …`. Los pasos crecen como **n²**: con 10 veces más datos, unas 100 veces más pasos.",
              desafio="Completá el inicio del bucle de adentro: compara cada uno con los que vienen **después**.",
              inicial='''
                  public class Cuadrado {
                      public static void main(String[] args) {
                          for (int n : new int[] {10, 100, 1000}) {
                              long pasos = 0;
                              for (int i = 0; i < n; i++) {
                                  for (int j = ___; j < n; j++) {
                                      pasos++;
                                  }
                              }
                              System.out.println("n = " + n + ": " + pasos + " comparaciones");
                          }
                      }
                  }
              ''',
              solucion='''
                  public class Cuadrado {
                      public static void main(String[] args) {
                          for (int n : new int[] {10, 100, 1000}) {
                              long pasos = 0;
                              for (int i = 0; i < n; i++) {
                                  for (int j = i + 1; j < n; j++) {
                                      pasos++;
                                  }
                              }
                              System.out.println("n = " + n + ": " + pasos + " comparaciones");
                          }
                      }
                  }
              ''',
              al_superar="De 45 a casi medio millón. —Con los pasaportes de un día de feria —calcula Nadia—, esto tarda hasta mañana. El ogro aplaude.",
              imagen=["Una balanza con un plato que se hunde bajo una montaña de comparaciones.",
                      "Nadia haciendo cuentas en su libreta, alarmada; un ogro aplaudiendo."]),
            m(id="R05-N01-P3", titulo="Una sola pasada",
              lugar="La sala de las balanzas del tiempo", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="HashSet en una pasada | vistos.add(p) devuelve false si ya estaba · O(1) cada uno · O(n) en total",
              recompensa="xp 15, oro 15",
              escena="""
                  —Los pasaportes repetidos se encuentran en **una sola pasada** —dice Kaffa—. Es lo que te van a pedir en el examen. Con lo que aprendiste en los Archivos alcanza.
              """,
              sugiere="Con un `HashSet` de vistos, cada `add` dice en un paso si el pasaporte ya había aparecido (devuelve `false`). Así se recorre la lista **una sola vez**.",
              desafio="Completá la condición: si no se pudo agregar, es un repetido.",
              inicial='''
                  import java.util.HashSet;
                  import java.util.LinkedHashSet;
                  import java.util.List;
                  import java.util.Set;

                  public class UnaPasada {
                      public static void main(String[] args) {
                          List<String> pasaportes = List.of("AR-101", "UY-202", "AR-101", "CL-303", "UY-202");
                          Set<String> vistos = new HashSet<>();
                          Set<String> repetidos = new LinkedHashSet<>();
                          int pasos = 0;
                          for (String p : pasaportes) {
                              pasos++;
                              if (___) {
                                  repetidos.add(p);
                              }
                          }
                          System.out.println("Repetidos: " + repetidos);
                          System.out.println("Pasos: " + pasos);
                      }
                  }
              ''',
              solucion='''
                  import java.util.HashSet;
                  import java.util.LinkedHashSet;
                  import java.util.List;
                  import java.util.Set;

                  public class UnaPasada {
                      public static void main(String[] args) {
                          List<String> pasaportes = List.of("AR-101", "UY-202", "AR-101", "CL-303", "UY-202");
                          Set<String> vistos = new HashSet<>();
                          Set<String> repetidos = new LinkedHashSet<>();
                          int pasos = 0;
                          for (String p : pasaportes) {
                              pasos++;
                              if (!vistos.add(p)) {
                                  repetidos.add(p);
                              }
                          }
                          System.out.println("Repetidos: " + repetidos);
                          System.out.println("Pasos: " + pasos);
                      }
                  }
              ''',
              al_superar="Cinco pasaportes, cinco pasos. —«¿Cuál es la complejidad de tu solución?» —pregunta Kaffa, imitando a un profesor. —O(n) —contesta Zed, sin pensarlo.",
              imagen=["Una fila de pasaportes pasando una sola vez por un arco; dos de ellos se encienden en rojo al pasar.",
                      "Kaffa con anteojos de profesor, sonriendo."]),
            m(id="R05-N01-P4", titulo="Partir a la mitad",
              lugar="La sala de las balanzas del tiempo", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="O(log n) | la búsqueda binaria descarta la mitad en cada paso · un millón de datos, unos 20 pasos · solo con datos ORDENADOS",
              recompensa="xp 15, oro 20",
              escena="""
                  El último aprendiz busca un registro en el archivo ordenado de la Torre: un millón de fichas. No las mira de a una: abre por la mitad, ve si se pasó, y descarta media pila.
              """,
              sugiere="En la búsqueda binaria, si lo del medio es menor que lo buscado, lo buscado está en la mitad de **arriba**: `desde = medio + 1`. Si es mayor, en la de abajo: `hasta = medio - 1`.",
              desafio="Completá qué pasa cuando lo del medio es menor que lo buscado.",
              inicial='''
                  public class Mitad {
                      public static void main(String[] args) {
                          int n = 1_000_000;
                          int[] fichas = new int[n];
                          for (int i = 0; i < n; i++) {
                              fichas[i] = i * 2;
                          }
                          int buscado = 1_234_566;
                          int desde = 0;
                          int hasta = n - 1;
                          int pasos = 0;
                          int encontrada = -1;
                          while (desde <= hasta) {
                              pasos++;
                              int medio = (desde + hasta) / 2;
                              if (fichas[medio] == buscado) {
                                  encontrada = medio;
                                  break;
                              } else if (fichas[medio] < buscado) {
                                  ___;
                              } else {
                                  hasta = medio - 1;
                              }
                          }
                          System.out.println("Ficha en la posición " + encontrada + ", en " + pasos + " pasos");
                      }
                  }
              ''',
              solucion='''
                  public class Mitad {
                      public static void main(String[] args) {
                          int n = 1_000_000;
                          int[] fichas = new int[n];
                          for (int i = 0; i < n; i++) {
                              fichas[i] = i * 2;
                          }
                          int buscado = 1_234_566;
                          int desde = 0;
                          int hasta = n - 1;
                          int pasos = 0;
                          int encontrada = -1;
                          while (desde <= hasta) {
                              pasos++;
                              int medio = (desde + hasta) / 2;
                              if (fichas[medio] == buscado) {
                                  encontrada = medio;
                                  break;
                              } else if (fichas[medio] < buscado) {
                                  desde = medio + 1;
                              } else {
                                  hasta = medio - 1;
                              }
                          }
                          System.out.println("Ficha en la posición " + encontrada + ", en " + pasos + " pasos");
                      }
                  }
              ''',
              al_superar="""
                  Un millón de fichas y la encuentra en menos de veinte pasos. Los aprendices se dan la mano.
                  En el segundo piso, Kaffa abre un plano viejo tan enredado que cambiar una puerta tira una pared.
              """,
              imagen=["Una pila gigante de fichas que se parte por la mitad una y otra vez hasta dejar una sola brillando.",
                      "Al fondo, una escalera que sube al segundo piso, con planos enrollados en los escalones."]),
        ],
    },
    {
        "titulo": "R05-N02 · Principios SOLID",
        "misiones": [
            m(id="R05-N02-P1", titulo="La cocina que también es armería",
              lugar="La sala de los planos viejos", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="troll",
              carta="S: responsabilidad única | una clase, una razón para cambiar · calcular, formatear y mostrar van en clases distintas",
              recompensa="xp 10, oro 10",
              escena="""
                  En un plano viejo, la cocina también es la armería y el dormitorio. En el código del mismo arquitecto, una clase calcula, formatea y muestra. Un **troll** vive cómodo en ese desorden.
              """,
              sugiere="Separá: una clase **calcula** y otra **formatea**. Así, si cambia el formato, no tocás la cuenta. El `main` solo conecta las piezas.",
              desafio="Completá la llamada al formateador con el total calculado.",
              inicial='''
                  public class Separar {
                      public static void main(String[] args) {
                          int[] tasas = {120, 80, 40};
                          int total = new Calculadora().total(tasas);
                          String texto = ___;
                          System.out.println(texto);
                      }
                  }

                  class Calculadora {
                      int total(int[] montos) {
                          int t = 0;
                          for (int m : montos) {
                              t += m;
                          }
                          return t;
                      }
                  }

                  class Formateador {
                      String formatear(int total) {
                          return "Tasas del día: " + total + " denarios";
                      }
                  }
              ''',
              solucion='''
                  public class Separar {
                      public static void main(String[] args) {
                          int[] tasas = {120, 80, 40};
                          int total = new Calculadora().total(tasas);
                          String texto = new Formateador().formatear(total);
                          System.out.println(texto);
                      }
                  }

                  class Calculadora {
                      int total(int[] montos) {
                          int t = 0;
                          for (int m : montos) {
                              t += m;
                          }
                          return t;
                      }
                  }

                  class Formateador {
                      String formatear(int total) {
                          return "Tasas del día: " + total + " denarios";
                      }
                  }
              ''',
              al_superar="Cada clase en su habitación. El troll se queda sin rincón donde esconderse. —**S** —anota Kaffa en la pizarra.",
              imagen=["Un plano viejo partido en tres habitaciones nuevas, cada una con su cartel: «calcular», «formatear», «mostrar».",
                      "Kaffa escribiendo una S enorme en la pizarra."]),
            m(id="R05-N02-P2", titulo="Agregar sin romper",
              lugar="La sala de los planos viejos", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="O: abierto/cerrado | lo nuevo se AGREGA (una clase que implementa la interfaz) · lo que ya anda no se toca",
              recompensa="xp 15, oro 15",
              escena="""
                  La Torre agrega un descuento nuevo cada semana. En el código viejo, cada uno era un `case` más en un `switch` gigante. Kaffa le pide a Zed que agregue el del **Gremio** sin tocar `cobrar`.
              """,
              sugiere="Con una interfaz `Descuento`, cada descuento es una clase. Para agregar el del Gremio (15 menos) alcanza con **una clase nueva**; `cobrar` sigue igual.",
              desafio="Completá el `aplicar` del descuento del Gremio: 15 denarios menos.",
              inicial='''
                  public class Abierto {
                      static double cobrar(double precio, Descuento d) {
                          return d.aplicar(precio);
                      }

                      public static void main(String[] args) {
                          System.out.println("Peregrino: " + cobrar(100, new Peregrino()));
                          System.out.println("Gremio: " + cobrar(100, new Gremio()));
                      }
                  }

                  interface Descuento {
                      double aplicar(double precio);
                  }

                  class Peregrino implements Descuento {
                      public double aplicar(double precio) { return precio * 0.5; }
                  }

                  class Gremio implements Descuento {
                      public double aplicar(double precio) { return ___; }
                  }
              ''',
              solucion='''
                  public class Abierto {
                      static double cobrar(double precio, Descuento d) {
                          return d.aplicar(precio);
                      }

                      public static void main(String[] args) {
                          System.out.println("Peregrino: " + cobrar(100, new Peregrino()));
                          System.out.println("Gremio: " + cobrar(100, new Gremio()));
                      }
                  }

                  interface Descuento {
                      double aplicar(double precio);
                  }

                  class Peregrino implements Descuento {
                      public double aplicar(double precio) { return precio * 0.5; }
                  }

                  class Gremio implements Descuento {
                      public double aplicar(double precio) { return precio - 15; }
                  }
              ''',
              al_superar="Un descuento nuevo y `cobrar` no se enteró. —**O** —anota Kaffa—. Abierto para agregar, cerrado para tocar. Es la Strategy del astillero, con otro nombre.",
              imagen=["Un plano con una habitación nueva agregada en el borde, sin tocar las demás.",
                      "Zed con una regla y un lápiz, satisfecho."]),
            m(id="R05-N02-P3", titulo="El hijo que no cumple",
              lugar="La sala de los planos viejos", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="goblin",
              carta="L: Liskov | donde va el padre, tiene que poder ir cualquier hijo sin sorpresas · si el hijo no puede cumplir, la herencia está mal",
              recompensa="xp 15, oro 15",
              escena="""
                  En un plano viejo, el `Avestruz` hereda de `Ave`… y `volar()` tira un error. Cada vez que alguien hace volar a todas las aves, el programa explota. Un **goblin** se esconde en esa herencia.
              """,
              sugiere="Si no todas las aves vuelan, `volar()` no va en `Ave`: va en una interfaz `Voladora` que firman solo las que pueden. Así, donde se espera una `Voladora`, ninguna falla.",
              desafio="Completá el tipo de la lista: solo las que pueden volar.",
              inicial='''
                  import java.util.List;

                  public class Liskov {
                      public static void main(String[] args) {
                          List<___> bandada = List.of(new Paloma(), new Grifo());
                          for (Voladora v : bandada) {
                              System.out.println(v.volar());
                          }
                          System.out.println(new Avestruz().correr());
                      }
                  }

                  interface Voladora {
                      String volar();
                  }

                  class Paloma implements Voladora {
                      public String volar() { return "la paloma vuela bajo"; }
                  }

                  class Grifo implements Voladora {
                      public String volar() { return "el grifo vuela en espiral"; }
                  }

                  class Avestruz {
                      String correr() { return "el avestruz corre, no vuela"; }
                  }
              ''',
              solucion='''
                  import java.util.List;

                  public class Liskov {
                      public static void main(String[] args) {
                          List<Voladora> bandada = List.of(new Paloma(), new Grifo());
                          for (Voladora v : bandada) {
                              System.out.println(v.volar());
                          }
                          System.out.println(new Avestruz().correr());
                      }
                  }

                  interface Voladora {
                      String volar();
                  }

                  class Paloma implements Voladora {
                      public String volar() { return "la paloma vuela bajo"; }
                  }

                  class Grifo implements Voladora {
                      public String volar() { return "el grifo vuela en espiral"; }
                  }

                  class Avestruz {
                      String correr() { return "el avestruz corre, no vuela"; }
                  }
              ''',
              al_superar="Nadie le pide al avestruz que vuele, y nada explota. —**L** y, de paso, **I** —dice Kaffa—: interfaces chicas, que cada uno firme solo lo que puede cumplir.",
              imagen=["Una paloma y un grifo volando; abajo, un avestruz corriendo feliz por el piso de la Torre.",
                      "Un goblin escondido detrás de un plano tachado que decía «Avestruz extends Ave»."]),
            m(id="R05-N02-P4", titulo="No lo fabriques: pedilo",
              lugar="La sala de los planos viejos", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="D: inversión de dependencias | la clase depende de una INTERFAZ y la RECIBE por el constructor · no hace new de lo que usa",
              recompensa="xp 15, oro 20",
              escena="""
                  —La última regla es la más importante —dice Kaffa, y la subraya dos veces—: **no fabriques lo que usás; pedilo**. El servicio de reservas no crea su avisador: se lo dan. Así funciona con el de la Torre y con uno de prueba.
              """,
              sugiere="El servicio guarda un `Avisador` (una interfaz) y lo recibe por el constructor: `new ServicioReservas(avisador)`. Así, el mismo servicio funciona con cualquier avisador, también con una lambda.",
              desafio="Completá el constructor del servicio pasándole el avisador.",
              inicial='''
                  public class Inversion {
                      public static void main(String[] args) {
                          Avisador torre = mensaje -> System.out.println("[Torre] " + mensaje);
                          ServicioReservas servicio = ___;
                          servicio.reservar("Zed", 2);
                      }
                  }

                  interface Avisador {
                      void avisar(String mensaje);
                  }

                  class ServicioReservas {
                      private final Avisador avisador;

                      ServicioReservas(Avisador avisador) {
                          this.avisador = avisador;
                      }

                      void reservar(String viajero, int noches) {
                          avisador.avisar(viajero + " reservó " + noches + " noches en la Torre");
                      }
                  }
              ''',
              solucion='''
                  public class Inversion {
                      public static void main(String[] args) {
                          Avisador torre = mensaje -> System.out.println("[Torre] " + mensaje);
                          ServicioReservas servicio = new ServicioReservas(torre);
                          servicio.reservar("Zed", 2);
                      }
                  }

                  interface Avisador {
                      void avisar(String mensaje);
                  }

                  class ServicioReservas {
                      private final Avisador avisador;

                      ServicioReservas(Avisador avisador) {
                          this.avisador = avisador;
                      }

                      void reservar(String viajero, int noches) {
                          avisador.avisar(viajero + " reservó " + noches + " noches en la Torre");
                      }
                  }
              ''',
              al_superar="""
                  El servicio no sabe quién avisa, y no le hace falta. —**D** —termina Kaffa, y la pizarra queda llena: S, O, L, I, D.
                  —En el piso de arriba —agrega—, hay alguien que se dedica solo a eso: fabricar las piezas y pasárselas a cada uno.
              """,
              imagen=["La pizarra de la Torre con las cinco letras SOLID escritas con tiza, la D subrayada dos veces.",
                      "Kaffa señalando hacia el techo, donde se oye el ruido de una grúa."]),
        ],
    },
    {
        "titulo": "R05-N03 · Maven y el contenedor de Spring",
        "misiones": [
            m(id="R05-N03-P1", titulo="El taller que arma solo",
              lugar="El taller del Contenedor", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="El contenedor | alguien crea los objetos y se los entrega a quien los pide · en Spring, el ApplicationContext con sus @Component",
              recompensa="xp 10, oro 10",
              escena="""
                  En el tercer piso, una grúa gigante, el **Contenedor**, sabe qué pieza va en cada lugar. Los maestros no fabrican nada: piden «un reloj» y la grúa se lo entrega armado. —Spring es esa grúa —dice Gheco—. Armemos una de juguete para entenderla.
              """,
              sugiere="Un contenedor guarda las piezas por nombre en un mapa y las entrega cuando alguien las pide. En Spring, cada clase con `@Component` es una pieza, y el contenedor la crea **una sola vez**.",
              desafio="Completá el método que entrega una pieza por su nombre.",
              inicial='''
                  import java.util.HashMap;
                  import java.util.Map;

                  public class Grua {
                      public static void main(String[] args) {
                          Contenedor contenedor = new Contenedor();
                          contenedor.registrar("reloj", new Reloj());
                          Reloj a = (Reloj) contenedor.pedir("reloj");
                          Reloj b = (Reloj) contenedor.pedir("reloj");
                          System.out.println(a.hora());
                          System.out.println("Es la misma pieza: " + (a == b));
                      }
                  }

                  class Contenedor {
                      private final Map<String, Object> piezas = new HashMap<>();

                      void registrar(String nombre, Object pieza) {
                          piezas.put(nombre, pieza);
                      }

                      Object pedir(String nombre) {
                          return ___;
                      }
                  }

                  class Reloj {
                      String hora() {
                          return "Son las 9 en la Torre";
                      }
                  }
              ''',
              solucion='''
                  import java.util.HashMap;
                  import java.util.Map;

                  public class Grua {
                      public static void main(String[] args) {
                          Contenedor contenedor = new Contenedor();
                          contenedor.registrar("reloj", new Reloj());
                          Reloj a = (Reloj) contenedor.pedir("reloj");
                          Reloj b = (Reloj) contenedor.pedir("reloj");
                          System.out.println(a.hora());
                          System.out.println("Es la misma pieza: " + (a == b));
                      }
                  }

                  class Contenedor {
                      private final Map<String, Object> piezas = new HashMap<>();

                      void registrar(String nombre, Object pieza) {
                          piezas.put(nombre, pieza);
                      }

                      Object pedir(String nombre) {
                          return piezas.get(nombre);
                      }
                  }

                  class Reloj {
                      String hora() {
                          return "Son las 9 en la Torre";
                      }
                  }
              ''',
              al_superar="Dos pedidos, la misma pieza: el contenedor la creó una sola vez. —Como el Singleton del astillero —dice Zed—, pero sin `private` ni `get()`. —Exacto —dice Kaffa—: lo hace la grúa.",
              imagen=["Una grúa de bronce enorme en el tercer piso de la Torre, entregando un reloj a un maestro.",
                      "Zed mirando hacia arriba, entendiendo."]),
            m(id="R05-N03-P2", titulo="La pieza que viene con piezas",
              lugar="El taller del Contenedor", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Inyección por constructor | la grúa crea primero lo que la pieza necesita y se lo pasa al construirla · en Spring: @RequiredArgsConstructor y final",
              recompensa="xp 15, oro 15",
              escena="""
                  El `ServicioCampanas` necesita un `Reloj` para saber cuándo tocar. No lo fabrica: lo **pide en el constructor**, y la grúa se lo pasa al armarlo. Es la **D** de SOLID, hecha máquina.
              """,
              sugiere="Cuando el contenedor arma una pieza que necesita otra, primero busca la que hace falta y la pasa al constructor: `new ServicioCampanas(reloj)`. En Spring se escribe el constructor (o se lo deja a Lombok con `@RequiredArgsConstructor`) y el contenedor hace el resto.",
              desafio="Completá el armado del servicio con el reloj que ya está en el contenedor.",
              inicial='''
                  import java.util.HashMap;
                  import java.util.Map;

                  public class Inyeccion {
                      public static void main(String[] args) {
                          Map<String, Object> contenedor = new HashMap<>();
                          contenedor.put("reloj", new Reloj());
                          Reloj reloj = (Reloj) contenedor.get("reloj");
                          contenedor.put("campanas", ___);
                          ServicioCampanas campanas = (ServicioCampanas) contenedor.get("campanas");
                          System.out.println(campanas.tocar());
                      }
                  }

                  class Reloj {
                      int hora() { return 9; }
                  }

                  class ServicioCampanas {
                      private final Reloj reloj;

                      ServicioCampanas(Reloj reloj) {
                          this.reloj = reloj;
                      }

                      String tocar() {
                          return "Din don: son las " + reloj.hora();
                      }
                  }
              ''',
              solucion='''
                  import java.util.HashMap;
                  import java.util.Map;

                  public class Inyeccion {
                      public static void main(String[] args) {
                          Map<String, Object> contenedor = new HashMap<>();
                          contenedor.put("reloj", new Reloj());
                          Reloj reloj = (Reloj) contenedor.get("reloj");
                          contenedor.put("campanas", new ServicioCampanas(reloj));
                          ServicioCampanas campanas = (ServicioCampanas) contenedor.get("campanas");
                          System.out.println(campanas.tocar());
                      }
                  }

                  class Reloj {
                      int hora() { return 9; }
                  }

                  class ServicioCampanas {
                      private final Reloj reloj;

                      ServicioCampanas(Reloj reloj) {
                          this.reloj = reloj;
                      }

                      String tocar() {
                          return "Din don: son las " + reloj.hora();
                      }
                  }
              ''',
              al_superar="Las campanas suenan a las 9. El servicio nunca hizo `new Reloj()`: se lo dieron armado. —Eso es **inyectar** —dice Kaffa—. Spring lo hace con cien piezas sin que escribas una línea de esto.",
              imagen=["La grúa colocando un reloj adentro de un mecanismo de campanas.",
                      "Las campanas de la Torre sonando."]),
            m(id="R05-N03-P3", titulo="Dos piezas, una interfaz",
              lugar="El taller del Contenedor", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Elegir la implementación | el servicio pide una INTERFAZ · el contenedor decide cuál le da (en Spring, @Primary, @Qualifier o un perfil)",
              recompensa="xp 15, oro 15",
              escena="""
                  En la Torre hay dos formas de avisar: por **campana** y por **mensajero**. El servicio de avisos no sabe cuál usa: pide «un notificador», y la configuración de la Torre decide.
              """,
              sugiere="El servicio recibe un `Notificador` (la interfaz). Según la configuración (`modo`), el contenedor le pasa una implementación u otra. En Spring eso se elige con `@Primary`, `@Qualifier` o `application.properties`.",
              desafio="Completá la elección: con el modo \"mensajero\", el contenedor da un `PorMensajero`.",
              inicial='''
                  public class DosPiezas {
                      static Notificador elegir(String modo) {
                          return modo.equals("mensajero") ? ___ : new PorCampana();
                      }

                      public static void main(String[] args) {
                          for (String modo : new String[] {"campana", "mensajero"}) {
                              ServicioAvisos servicio = new ServicioAvisos(elegir(modo));
                              System.out.println(servicio.avisar("el Dragón despertó"));
                          }
                      }
                  }

                  interface Notificador {
                      String enviar(String texto);
                  }

                  class PorCampana implements Notificador {
                      public String enviar(String texto) { return "Campana: " + texto; }
                  }

                  class PorMensajero implements Notificador {
                      public String enviar(String texto) { return "Mensajero: " + texto; }
                  }

                  class ServicioAvisos {
                      private final Notificador notificador;

                      ServicioAvisos(Notificador notificador) { this.notificador = notificador; }

                      String avisar(String texto) { return notificador.enviar(texto); }
                  }
              ''',
              solucion='''
                  public class DosPiezas {
                      static Notificador elegir(String modo) {
                          return modo.equals("mensajero") ? new PorMensajero() : new PorCampana();
                      }

                      public static void main(String[] args) {
                          for (String modo : new String[] {"campana", "mensajero"}) {
                              ServicioAvisos servicio = new ServicioAvisos(elegir(modo));
                              System.out.println(servicio.avisar("el Dragón despertó"));
                          }
                      }
                  }

                  interface Notificador {
                      String enviar(String texto);
                  }

                  class PorCampana implements Notificador {
                      public String enviar(String texto) { return "Campana: " + texto; }
                  }

                  class PorMensajero implements Notificador {
                      public String enviar(String texto) { return "Mensajero: " + texto; }
                  }

                  class ServicioAvisos {
                      private final Notificador notificador;

                      ServicioAvisos(Notificador notificador) { this.notificador = notificador; }

                      String avisar(String texto) { return notificador.enviar(texto); }
                  }
              ''',
              al_superar="«el Dragón despertó», por campana y por mensajero. Nadia y Zed se miran: el aviso de prueba sonó demasiado real.",
              imagen=["Una campana y un mensajero con alas saliendo de la misma puerta del taller.",
                      "Nadia y Zed mirando hacia arriba, inquietos."]),
            m(id="R05-N03-P4", titulo="La configuración de la Torre",
              lugar="El taller del Contenedor", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="application.properties | los valores que cambian (tasas, nombres, puertos) van afuera del código · en Spring: @Value(\"${clave}\")",
              recompensa="xp 15, oro 20",
              escena="""
                  La tasa de cambio del Puerto cambia cada mes. Si está escrita en el código, hay que recompilar todo. —Lo que cambia —dice Kaffa— va en la **configuración**, no en el código.
              """,
              sugiere="Un archivo de propiedades guarda pares `clave=valor`. `Properties.load(...)` los lee y `getProperty(\"clave\")` los devuelve como texto. En Spring es `application.properties` y se lee con `@Value(\"${clave}\")`.",
              desafio="Completá la lectura de la tasa desde las propiedades.",
              inicial='''
                  import java.io.StringReader;
                  import java.util.Properties;

                  public class Configuracion {
                      public static void main(String[] args) throws Exception {
                          String archivo = """
                                  torre.nombre=Torre del Arquitecto
                                  cambio.tasa=0.85
                                  """;
                          Properties props = new Properties();
                          props.load(new StringReader(archivo));
                          double tasa = Double.parseDouble(props.___("cambio.tasa"));
                          System.out.println(props.getProperty("torre.nombre"));
                          System.out.println("100 denarios son " + (100 * tasa) + " monedas del Puerto");
                      }
                  }
              ''',
              solucion='''
                  import java.io.StringReader;
                  import java.util.Properties;

                  public class Configuracion {
                      public static void main(String[] args) throws Exception {
                          String archivo = """
                                  torre.nombre=Torre del Arquitecto
                                  cambio.tasa=0.85
                                  """;
                          Properties props = new Properties();
                          props.load(new StringReader(archivo));
                          double tasa = Double.parseDouble(props.getProperty("cambio.tasa"));
                          System.out.println(props.getProperty("torre.nombre"));
                          System.out.println("100 denarios son " + (100 * tasa) + " monedas del Puerto");
                      }
                  }
              ''',
              al_superar="""
                  Ochenta y cinco monedas del Puerto. Por la ventana del tercer piso, lejos, se ve el Puerto: la casa de Zed. —Arriba —dice Kaffa— vas a escribir la ventanilla que conecta la Torre con el Puerto.
              """,
              imagen=["Un pergamino de configuración clavado en la pared del taller, con «cambio.tasa=0.85».",
                      "Zed mirando por la ventana hacia el Puerto lejano, con barcos y techos."]),
        ],
    },
    {
        "titulo": "R05-N04 · Servicios REST",
        "misiones": [
            m(id="R05-N04-P1", titulo="La ventanilla de los mensajes",
              lugar="La ventanilla de la Torre", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Ruta y método | GET /api/barcos lee · POST /api/barcos crea · el controlador elige qué hacer según el método y la ruta",
              recompensa="xp 10, oro 10",
              escena="""
                  En el cuarto piso está la **ventanilla de los mensajes**: llegan pedidos de todo el Mundo del Código y cada uno dice **qué quiere** (el método) y **sobre qué** (la ruta). Gheco arma una ventanilla de juguete para ver cómo decide.
              """,
              sugiere="Un pedido HTTP tiene un **método** (`GET` para leer, `POST` para crear, `PUT` para cambiar, `DELETE` para borrar) y una **ruta**. El controlador los mira y decide. En Spring: `@GetMapping(\"/api/barcos\")`.",
              desafio="Completá el caso del pedido que crea un barco.",
              inicial='''
                  public class Ventanilla {
                      static String atender(String metodo, String ruta) {
                          return switch (metodo + " " + ruta) {
                              case "GET /api/barcos" -> "200: [Garza, Bagre]";
                              case ___ -> "201: barco creado";
                              default -> "404: no existe " + ruta;
                          };
                      }

                      public static void main(String[] args) {
                          System.out.println(atender("GET", "/api/barcos"));
                          System.out.println(atender("POST", "/api/barcos"));
                          System.out.println(atender("GET", "/api/dragones"));
                      }
                  }
              ''',
              solucion='''
                  public class Ventanilla {
                      static String atender(String metodo, String ruta) {
                          return switch (metodo + " " + ruta) {
                              case "GET /api/barcos" -> "200: [Garza, Bagre]";
                              case "POST /api/barcos" -> "201: barco creado";
                              default -> "404: no existe " + ruta;
                          };
                      }

                      public static void main(String[] args) {
                          System.out.println(atender("GET", "/api/barcos"));
                          System.out.println(atender("POST", "/api/barcos"));
                          System.out.println(atender("GET", "/api/dragones"));
                      }
                  }
              ''',
              al_superar="Leer, crear y un 404 para lo que no existe. —En Spring no escribís el `switch` —dice Kaffa—: ponés `@GetMapping` y `@PostMapping` y el framework elige.",
              imagen=["Una ventanilla de piedra en el cuarto piso de la Torre, con un cartel de rutas: GET, POST, PUT, DELETE.",
                      "Gheco atendiendo la ventanilla con una gorrita de empleado."]),
            m(id="R05-N04-P2", titulo="Responder en JSON",
              lugar="La ventanilla de la Torre", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="JSON | {\"nombre\": \"Garza\", \"carga\": 80} · texto entre comillas, números sin comillas · Spring convierte los objetos solo (Jackson)",
              recompensa="xp 10, oro 10",
              escena="""
                  El Puerto no lee pergaminos del Imperio: lee **JSON**. Zed tiene que responder cada barco en ese idioma.
              """,
              sugiere="Un objeto JSON va entre llaves, con `\"clave\": valor` separados por coma. Los textos llevan comillas (`\\\"Garza\\\"`) y los números no. En Spring, el controlador devuelve el objeto y Jackson lo convierte solo.",
              desafio="Completá el JSON con la carga del barco (un número, sin comillas).",
              inicial='''
                  public class Json {
                      record Barco(String nombre, int carga) {
                          String json() {
                              return "{\\"nombre\\": \\"" + nombre + "\\", \\"carga\\": " + ___ + "}";
                          }
                      }

                      public static void main(String[] args) {
                          System.out.println(new Barco("Garza", 80).json());
                          System.out.println(new Barco("Bagre", 120).json());
                      }
                  }
              ''',
              solucion='''
                  public class Json {
                      record Barco(String nombre, int carga) {
                          String json() {
                              return "{\\"nombre\\": \\"" + nombre + "\\", \\"carga\\": " + carga + "}";
                          }
                      }

                      public static void main(String[] args) {
                          System.out.println(new Barco("Garza", 80).json());
                          System.out.println(new Barco("Bagre", 120).json());
                      }
                  }
              ''',
              al_superar="Dos barcos en JSON, que el Puerto entiende. —Armarlo a mano es para entenderlo —dice Gheco—. En Spring, nunca más.",
              imagen=["Un pergamino con llaves y comillas, el JSON de un barco, viajando por un tubo hacia el Puerto.",
                      "Gheco con un diccionario «Imperio ↔ JSON»."]),
            m(id="R05-N04-P3", titulo="El código de la respuesta",
              lugar="La ventanilla de la Torre", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="orco",
              carta="Códigos de estado | 200 ok · 201 creado · 400 pedido inválido · 404 no existe · 409 conflicto · 500 error del servidor",
              recompensa="xp 15, oro 15",
              escena="""
                  Cuando alguien pide un barco que no existe, la ventanilla responde 200 con un cuerpo vacío y el cliente no entiende nada. Un **orco** festeja el silencio. Cada respuesta tiene que decir **cómo salió**.
              """,
              sugiere="Los códigos de estado dicen cómo salió el pedido: **200** encontrado, **404** no existe. En Spring, un `ResponseEntity.notFound()` o una excepción manejada en un `@RestControllerAdvice`.",
              desafio="Completá el código de estado para un barco que no existe.",
              inicial='''
                  import java.util.Map;

                  public class Estados {
                      static final Map<String, Integer> BARCOS = Map.of("Garza", 80, "Bagre", 120);

                      static String buscar(String nombre) {
                          Integer carga = BARCOS.get(nombre);
                          if (carga == null) {
                              return ___ + " no existe el barco " + nombre;
                          }
                          return 200 + " {\\"nombre\\": \\"" + nombre + "\\", \\"carga\\": " + carga + "}";
                      }

                      public static void main(String[] args) {
                          System.out.println(buscar("Garza"));
                          System.out.println(buscar("Ceibo"));
                      }
                  }
              ''',
              solucion='''
                  import java.util.Map;

                  public class Estados {
                      static final Map<String, Integer> BARCOS = Map.of("Garza", 80, "Bagre", 120);

                      static String buscar(String nombre) {
                          Integer carga = BARCOS.get(nombre);
                          if (carga == null) {
                              return 404 + " no existe el barco " + nombre;
                          }
                          return 200 + " {\\"nombre\\": \\"" + nombre + "\\", \\"carga\\": " + carga + "}";
                      }

                      public static void main(String[] args) {
                          System.out.println(buscar("Garza"));
                          System.out.println(buscar("Ceibo"));
                      }
                  }
              ''',
              al_superar="«404 no existe el barco Ceibo.» Claro y sin rodeos. El orco se va: ya nadie se confunde. —El Ceibo está encallado en la Represa —murmura Zed—. Pero eso la ventanilla no lo sabe.",
              imagen=["Un tablero de la ventanilla con números grandes: 200 en verde, 404 en naranja.",
                      "Un orco yéndose por la escalera, aburrido."]),
            m(id="R05-N04-P4", titulo="La primera ventanilla al Puerto",
              lugar="La ventanilla de la Torre", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Controlador y servicio | el controlador recibe el pedido y responde · el servicio tiene las reglas · el controlador NO calcula",
              recompensa="xp 15, oro 20",
              escena="""
                  Kaffa le encarga a Zed la ventanilla que conecta la Torre con **el Puerto**, su casa. Por primera vez, Zed va a llegar al Puerto **construyendo** algo, no robando.
              """,
              sugiere="El controlador solo traduce: recibe el pedido, le pide al **servicio** el resultado y arma la respuesta. Las reglas (cuánto cuesta un envío) están en el servicio. En Spring: `@RestController` que recibe un `@Service` por el constructor.",
              desafio="Completá el controlador: que le pida el costo al servicio.",
              inicial='''
                  public class AlPuerto {
                      public static void main(String[] args) {
                          ControladorEnvios controlador = new ControladorEnvios(new ServicioEnvios());
                          System.out.println(controlador.cotizar(30));
                          System.out.println(controlador.cotizar(120));
                      }
                  }

                  class ServicioEnvios {
                      int costo(int kilos) {
                          return kilos <= 50 ? 20 : 20 + (kilos - 50) / 10 * 5;
                      }
                  }

                  class ControladorEnvios {
                      private final ServicioEnvios servicio;

                      ControladorEnvios(ServicioEnvios servicio) {
                          this.servicio = servicio;
                      }

                      String cotizar(int kilos) {
                          int costo = ___;
                          return "200 {\\"kilos\\": " + kilos + ", \\"costo\\": " + costo + "}";
                      }
                  }
              ''',
              solucion='''
                  public class AlPuerto {
                      public static void main(String[] args) {
                          ControladorEnvios controlador = new ControladorEnvios(new ServicioEnvios());
                          System.out.println(controlador.cotizar(30));
                          System.out.println(controlador.cotizar(120));
                      }
                  }

                  class ServicioEnvios {
                      int costo(int kilos) {
                          return kilos <= 50 ? 20 : 20 + (kilos - 50) / 10 * 5;
                      }
                  }

                  class ControladorEnvios {
                      private final ServicioEnvios servicio;

                      ControladorEnvios(ServicioEnvios servicio) {
                          this.servicio = servicio;
                      }

                      String cotizar(int kilos) {
                          int costo = servicio.costo(kilos);
                          return "200 {\\"kilos\\": " + kilos + ", \\"costo\\": " + costo + "}";
                      }
                  }
              ''',
              al_superar="""
                  La primera cotización llega al Puerto y alguien allá la contesta: «¿Zed? ¿El de los techos?». Zed se ríe solo frente a la ventanilla.
                  Pero los mensajes del Puerto llegan con cualquier cosa adentro: kilos negativos, nombres vacíos, campos que sobran.
              """,
              imagen=["Un tubo de mensajes que une la Torre con el Puerto a lo lejos, con un pergamino JSON viajando.",
                      "Zed riéndose solo frente a la ventanilla, con una respuesta del Puerto en la mano."]),
        ],
    },
    {
        "titulo": "R05-N05 · DTO, validaciones y errores",
        "misiones": [
            m(id="R05-N05-P1", titulo="Lo que viaja no es lo que se guarda",
              lugar="Las cuatro salas de la Torre", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="DTO | un objeto solo para lo que entra o sale · el modelo guarda todo (también lo secreto) · la respuesta NUNCA es el modelo",
              recompensa="xp 10, oro 10",
              escena="""
                  En el quinto piso, Kaffa separa el servicio en salas que no se pisan. El modelo `Viajero` guarda el pasaporte y una **clave**; si se devuelve tal cual, la clave viaja al Puerto. —Lo que sale por la ventanilla es un **DTO** —dice—, nunca el modelo.
              """,
              sugiere="Un **DTO** es un objeto (casi siempre un `record`) con solo lo que tiene que viajar. Se arma desde el modelo con lo necesario: `new ViajeroRespuesta(v.nombre(), v.pasaporte())`. La clave se queda adentro.",
              desafio="Completá la respuesta con el nombre y el pasaporte, sin la clave.",
              inicial='''
                  public class Dto {
                      record Viajero(String nombre, String pasaporte, String clave) { }

                      record ViajeroRespuesta(String nombre, String pasaporte) { }

                      static ViajeroRespuesta aRespuesta(Viajero v) {
                          return ___;
                      }

                      public static void main(String[] args) {
                          Viajero zed = new Viajero("Zed", "PU-777", "techos123");
                          System.out.println("Se guarda: " + zed);
                          System.out.println("Viaja: " + aRespuesta(zed));
                      }
                  }
              ''',
              solucion='''
                  public class Dto {
                      record Viajero(String nombre, String pasaporte, String clave) { }

                      record ViajeroRespuesta(String nombre, String pasaporte) { }

                      static ViajeroRespuesta aRespuesta(Viajero v) {
                          return new ViajeroRespuesta(v.nombre(), v.pasaporte());
                      }

                      public static void main(String[] args) {
                          Viajero zed = new Viajero("Zed", "PU-777", "techos123");
                          System.out.println("Se guarda: " + zed);
                          System.out.println("Viaja: " + aRespuesta(zed));
                      }
                  }
              ''',
              al_superar="La clave «techos123» se queda en la Torre. —¿«techos123»? —pregunta Nadia. —Era una clave vieja —dice Zed, y la cambia esa misma noche.",
              imagen=["Dos salas de la Torre separadas por una ventanilla: adentro, una ficha completa con una clave; afuera, una tarjeta con solo nombre y pasaporte.",
                      "Nadia levantando una ceja; Zed rascándose la nuca."]),
            m(id="R05-N05-P2", titulo="Lo que entra se valida",
              lugar="Las cuatro salas de la Torre", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="goblin",
              carta="Validar la entrada | cada campo con su regla · se juntan TODOS los errores, no solo el primero · en Spring: @NotBlank, @Positive y @Valid",
              recompensa="xp 15, oro 15",
              escena="""
                  Del Puerto llega un pedido con el nombre vacío y los kilos en −3. Un **goblin** los mandó a propósito, para ver qué se rompe. La ventanilla tiene que rechazarlo y decir **todo** lo que está mal.
              """,
              sugiere="Se revisa cada campo y se **juntan** los errores en una lista: así el que mandó el pedido sabe todo lo que tiene que corregir. En Spring, las anotaciones `@NotBlank` y `@Positive` del DTO y `@Valid` en el controlador hacen esto solas.",
              desafio="Completá la regla de los kilos: tienen que ser mayores que cero.",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Validar {
                      record EnvioPedido(String destinatario, int kilos) { }

                      static List<String> validar(EnvioPedido p) {
                          List<String> errores = new ArrayList<>();
                          if (p.destinatario() == null || p.destinatario().isBlank()) {
                              errores.add("destinatario: no puede estar vacío");
                          }
                          if (___) {
                              errores.add("kilos: tiene que ser mayor que 0");
                          }
                          return errores;
                      }

                      public static void main(String[] args) {
                          System.out.println(validar(new EnvioPedido("Baldo", 30)));
                          System.out.println(validar(new EnvioPedido("", -3)));
                      }
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Validar {
                      record EnvioPedido(String destinatario, int kilos) { }

                      static List<String> validar(EnvioPedido p) {
                          List<String> errores = new ArrayList<>();
                          if (p.destinatario() == null || p.destinatario().isBlank()) {
                              errores.add("destinatario: no puede estar vacío");
                          }
                          if (p.kilos() <= 0) {
                              errores.add("kilos: tiene que ser mayor que 0");
                          }
                          return errores;
                      }

                      public static void main(String[] args) {
                          System.out.println(validar(new EnvioPedido("Baldo", 30)));
                          System.out.println(validar(new EnvioPedido("", -3)));
                      }
                  }
              ''',
              al_superar="El pedido de Baldo pasa limpio; el del goblin vuelve con sus dos errores anotados. El goblin, ofendido, corrige y lo manda bien.",
              imagen=["Una ventanilla devolviendo un pergamino con dos errores marcados en rojo.",
                      "Un goblin corrigiendo su pedido de mala gana."]),
            m(id="R05-N05-P3", titulo="Un error que se entiende",
              lugar="Las cuatro salas de la Torre", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Errores claros | una excepción propia por cada problema · un manejador central la convierte en la respuesta (código + detalle) · en Spring: @RestControllerAdvice y ProblemDetail",
              recompensa="xp 15, oro 15",
              escena="""
                  Cuando algo falla adentro, al Puerto le llega un «500» y un chorro de líneas en inglés. —Un error también es una respuesta —dice Kaffa—. Que diga **qué** pasó, con el código que corresponde.
              """,
              sugiere="El servicio lanza una excepción propia (`NoEncontrado`); un **manejador central** la atrapa y arma la respuesta: el código (404) y un detalle claro. En Spring, eso es un `@RestControllerAdvice` que devuelve un `ProblemDetail`.",
              desafio="Completá el manejador: atrapá la excepción `NoEncontrado`.",
              inicial='''
                  import java.util.Map;

                  public class Errores {
                      static class NoEncontrado extends RuntimeException {
                          NoEncontrado(String mensaje) { super(mensaje); }
                      }

                      static final Map<String, Integer> ENVIOS = Map.of("E1", 30);

                      static int buscar(String codigo) {
                          Integer kilos = ENVIOS.get(codigo);
                          if (kilos == null) {
                              throw new NoEncontrado("No existe el envío " + codigo);
                          }
                          return kilos;
                      }

                      static String atender(String codigo) {
                          try {
                              return "200 {\\"kilos\\": " + buscar(codigo) + "}";
                          } catch (___ e) {
                              return "404 {\\"detail\\": \\"" + e.getMessage() + "\\"}";
                          }
                      }

                      public static void main(String[] args) {
                          System.out.println(atender("E1"));
                          System.out.println(atender("E9"));
                      }
                  }
              ''',
              solucion='''
                  import java.util.Map;

                  public class Errores {
                      static class NoEncontrado extends RuntimeException {
                          NoEncontrado(String mensaje) { super(mensaje); }
                      }

                      static final Map<String, Integer> ENVIOS = Map.of("E1", 30);

                      static int buscar(String codigo) {
                          Integer kilos = ENVIOS.get(codigo);
                          if (kilos == null) {
                              throw new NoEncontrado("No existe el envío " + codigo);
                          }
                          return kilos;
                      }

                      static String atender(String codigo) {
                          try {
                              return "200 {\\"kilos\\": " + buscar(codigo) + "}";
                          } catch (NoEncontrado e) {
                              return "404 {\\"detail\\": \\"" + e.getMessage() + "\\"}";
                          }
                      }

                      public static void main(String[] args) {
                          System.out.println(atender("E1"));
                          System.out.println(atender("E9"));
                      }
                  }
              ''',
              al_superar="«404, no existe el envío E9.» El Puerto lo entiende a la primera. Las campanas de los Archivos, ahora con forma de respuesta HTTP.",
              imagen=["Una campana de los Archivos convertida en un cartel de respuesta: «404 · No existe el envío E9».",
                      "Kaffa asintiendo con la taza en la mano."]),
            m(id="R05-N05-P4", titulo="Lo que escribe Lombok",
              lugar="Las cuatro salas de la Torre", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Lombok | @Getter, @Setter, @RequiredArgsConstructor, @Builder escriben ese código al compilar · acá lo escribimos a mano para ver qué genera",
              recompensa="xp 15, oro 20",
              escena="""
                  Las clases del modelo que cambian no pueden ser `record` y necesitan constructores, getters y setters: cincuenta líneas iguales. **Lombok** las escribe solo con anotaciones. Gheco escribe a mano lo que genera un `@Builder`, para que Zed vea que no es magia.
              """,
              sugiere="Un **builder** arma el objeto paso a paso: `Envio.builder().destinatario(\"Baldo\").kilos(30).build()`. Cada método guarda un dato y devuelve el mismo builder (`return this;`), y `build()` crea el objeto. Con Lombok, `@Builder` escribe todo esto solo.",
              desafio="Completá el método del builder que guarda los kilos y devuelve el builder.",
              inicial='''
                  public class Lombok {
                      public static void main(String[] args) {
                          Envio e = Envio.builder().destinatario("Baldo").kilos(30).build();
                          System.out.println(e.getDestinatario() + ": " + e.getKilos() + " kg");
                      }
                  }

                  class Envio {
                      private final String destinatario;
                      private final int kilos;

                      private Envio(String destinatario, int kilos) {
                          this.destinatario = destinatario;
                          this.kilos = kilos;
                      }

                      String getDestinatario() { return destinatario; }

                      int getKilos() { return kilos; }

                      static Builder builder() { return new Builder(); }

                      static class Builder {
                          private String destinatario;
                          private int kilos;

                          Builder destinatario(String d) {
                              this.destinatario = d;
                              return this;
                          }

                          Builder kilos(int k) {
                              ___;
                          }

                          Envio build() { return new Envio(destinatario, kilos); }
                      }
                  }
              ''',
              solucion='''
                  public class Lombok {
                      public static void main(String[] args) {
                          Envio e = Envio.builder().destinatario("Baldo").kilos(30).build();
                          System.out.println(e.getDestinatario() + ": " + e.getKilos() + " kg");
                      }
                  }

                  class Envio {
                      private final String destinatario;
                      private final int kilos;

                      private Envio(String destinatario, int kilos) {
                          this.destinatario = destinatario;
                          this.kilos = kilos;
                      }

                      String getDestinatario() { return destinatario; }

                      int getKilos() { return kilos; }

                      static Builder builder() { return new Builder(); }

                      static class Builder {
                          private String destinatario;
                          private int kilos;

                          Builder destinatario(String d) {
                              this.destinatario = d;
                              return this;
                          }

                          Builder kilos(int k) {
                              this.kilos = k;
                              return this;
                          }

                          Envio build() { return new Envio(destinatario, kilos); }
                      }
                  }
              ''',
              al_superar="""
                  Treinta líneas para un builder… que Lombok escribe con **una** anotación. —Ahora que sabés lo que hace —dice Kaffa—, usalo sin culpa.
                  Zed, que entraba por cualquier lado, ahora **diseña las puertas** de su propio servicio. En la cima de la Torre, el Tribunal deja un pliego sobre la mesa.
              """,
              imagen=["Una pila de treinta líneas de código que se comprime en una sola etiqueta: «@Builder».",
                      "En la cima de la Torre, un pliego lacrado sobre una mesa de piedra, con la palabra «AduanaExpress»."]),
        ],
    },
    {
        "titulo": "R05-N06 · Jefe final: el Dragón del Imperio",
        "misiones": [
            m(id="R05-N06-P1", titulo="Primera pieza: el modelo",
              lugar="La cima de la Torre", personajes="Zed, Gheco, Nadia, Kaffa, el Dragón del Imperio",
              criatura="dragon",
              carta="El modelo del examen | Mercancia abstracta · Caja y Barril calculan su impuesto · nada de instanceof para calcular",
              recompensa="xp 20, oro 20",
              escena="""
                  El **Dragón del Imperio** despierta enroscado en la ventana más alta, hecho de todas las piezas que Zed juntó desde la Aduana. El pliego dice **AduanaExpress**. —Pieza por pieza —dice Kaffa—. Primero, el **modelo**: cada mercancía sabe cuánto paga.
              """,
              sugiere="`Mercancia` es abstracta y cada tipo escribe su `impuesto()`: la `Caja`, el 10 % del valor; el `Barril`, el 10 % más 0,5 por litro. Así el total se calcula con una sola línea, sin preguntar qué es cada una.",
              desafio="Completá el impuesto del barril: el 10 % del valor más 0,5 por litro.",
              inicial='''
                  import java.util.List;

                  public class Dragon1 {
                      public static void main(String[] args) {
                          List<Mercancia> carga = List.of(new Caja("C1", 1000), new Barril("B1", 500, 40));
                          double total = 0;
                          for (Mercancia m : carga) {
                              System.out.println(m.codigo + ": " + m.impuesto());
                              total += m.impuesto();
                          }
                          System.out.println("Impuestos: " + total);
                      }
                  }

                  abstract class Mercancia {
                      final String codigo;
                      final double valor;

                      Mercancia(String codigo, double valor) {
                          this.codigo = codigo;
                          this.valor = valor;
                      }

                      abstract double impuesto();
                  }

                  class Caja extends Mercancia {
                      Caja(String codigo, double valor) { super(codigo, valor); }

                      double impuesto() { return valor * 0.10; }
                  }

                  class Barril extends Mercancia {
                      final int litros;

                      Barril(String codigo, double valor, int litros) {
                          super(codigo, valor);
                          this.litros = litros;
                      }

                      double impuesto() { return ___; }
                  }
              ''',
              solucion='''
                  import java.util.List;

                  public class Dragon1 {
                      public static void main(String[] args) {
                          List<Mercancia> carga = List.of(new Caja("C1", 1000), new Barril("B1", 500, 40));
                          double total = 0;
                          for (Mercancia m : carga) {
                              System.out.println(m.codigo + ": " + m.impuesto());
                              total += m.impuesto();
                          }
                          System.out.println("Impuestos: " + total);
                      }
                  }

                  abstract class Mercancia {
                      final String codigo;
                      final double valor;

                      Mercancia(String codigo, double valor) {
                          this.codigo = codigo;
                          this.valor = valor;
                      }

                      abstract double impuesto();
                  }

                  class Caja extends Mercancia {
                      Caja(String codigo, double valor) { super(codigo, valor); }

                      double impuesto() { return valor * 0.10; }
                  }

                  class Barril extends Mercancia {
                      final int litros;

                      Barril(String codigo, double valor, int litros) {
                          super(codigo, valor);
                          this.litros = litros;
                      }

                      double impuesto() { return valor * 0.10 + litros * 0.5; }
                  }
              ''',
              al_superar="Ciento setenta denarios de impuestos, sin un `if`. Una escama del Dragón se apaga: la pieza de la Academia está en su lugar.",
              imagen=["El Dragón del Imperio: un dragón de bronce y vitrales hecho de piezas (moldes, campanas, corrientes), enroscado en la ventana más alta de la Torre.",
                      "Zed frente a él con el pliego «AduanaExpress»; Nadia y Gheco atrás; Kaffa sin su taza."]),
            m(id="R05-N06-P2", titulo="Segunda pieza: la estrategia activa",
              lugar="La cima de la Torre", personajes="Zed, Gheco, Nadia, Kaffa, el Dragón del Imperio",
              carta="Strategy por nombre | un mapa nombre → estrategia · la activa se cambia en tiempo de ejecución · en Spring, los @Component por nombre",
              recompensa="xp 20, oro 20",
              escena="""
                  El Dragón cambia de humor y, con él, el recargo por demora: normal, feria o nocturno. —Como en el astillero —dice Gheco—, pero eligiéndola por **nombre**, como hace Spring.
              """,
              sugiere="Las estrategias se guardan en un mapa por nombre. La activa es solo un nombre: `estrategias.get(activa).calcular(dias, valor)`. Cambiarla es cambiar ese nombre.",
              desafio="Completá el cálculo con la estrategia activa del mapa.",
              inicial='''
                  import java.util.LinkedHashMap;
                  import java.util.Map;

                  public class Dragon2 {
                      interface Recargo {
                          double calcular(int dias, double valor);
                      }

                      static final Map<String, Recargo> ESTRATEGIAS = new LinkedHashMap<>();
                      static String activa = "normal";

                      static {
                          ESTRATEGIAS.put("normal", (dias, valor) -> valor * 0.02 * dias);
                          ESTRATEGIAS.put("feria", (dias, valor) -> dias <= 3 ? 0 : valor * 0.01 * (dias - 3));
                          ESTRATEGIAS.put("nocturno", (dias, valor) -> dias == 0 ? 0 : valor * 0.05 + valor * 0.03 * dias);
                      }

                      static double recargo(int dias, double valor) {
                          return ___;
                      }

                      public static void main(String[] args) {
                          for (String nombre : ESTRATEGIAS.keySet()) {
                              activa = nombre;
                              System.out.println(nombre + ", 5 días sobre 1500: " + recargo(5, 1500));
                          }
                      }
                  }
              ''',
              solucion='''
                  import java.util.LinkedHashMap;
                  import java.util.Map;

                  public class Dragon2 {
                      interface Recargo {
                          double calcular(int dias, double valor);
                      }

                      static final Map<String, Recargo> ESTRATEGIAS = new LinkedHashMap<>();
                      static String activa = "normal";

                      static {
                          ESTRATEGIAS.put("normal", (dias, valor) -> valor * 0.02 * dias);
                          ESTRATEGIAS.put("feria", (dias, valor) -> dias <= 3 ? 0 : valor * 0.01 * (dias - 3));
                          ESTRATEGIAS.put("nocturno", (dias, valor) -> dias == 0 ? 0 : valor * 0.05 + valor * 0.03 * dias);
                      }

                      static double recargo(int dias, double valor) {
                          return ESTRATEGIAS.get(activa).calcular(dias, valor);
                      }

                      public static void main(String[] args) {
                          for (String nombre : ESTRATEGIAS.keySet()) {
                              activa = nombre;
                              System.out.println(nombre + ", 5 días sobre 1500: " + recargo(5, 1500));
                          }
                      }
                  }
              ''',
              al_superar="Tres humores, un solo cálculo. Otra escama se apaga: la del astillero.",
              imagen=["Tres esferas de colores (normal, feria, nocturno) orbitando alrededor de Zed; una se enciende.",
                      "El Dragón con una escama apagándose."]),
            m(id="R05-N06-P3", titulo="Tercera pieza: el peregrino y los pasaportes",
              lugar="La cima de la Torre", personajes="Zed, Gheco, Nadia, Kaffa, el Dragón del Imperio",
              carta="Herencia y una pasada | Peregrino paga la mitad del recargo (factorRecargo) · los pasaportes repetidos, en una pasada con HashSet",
              recompensa="xp 20, oro 25",
              escena="""
                  El Dragón escupe dos preguntas a la vez: cuánto recargo paga un **peregrino**, y cuáles de los pasaportes del día están **repetidos**. Las dos, sin perder tiempo.
              """,
              sugiere="Cada viajero dice qué parte del recargo paga: el mercader, `1.0`; el peregrino, `0.5`. Para los pasaportes, un `LinkedHashSet` de vistos y otro de duplicados, en una sola pasada.",
              desafio="Completá el factor del peregrino: paga la mitad.",
              inicial='''
                  import java.util.LinkedHashSet;
                  import java.util.List;
                  import java.util.Set;

                  public class Dragon3 {
                      public static void main(String[] args) {
                          double recargo = 30;
                          Viajero[] viajeros = {new Mercader("Baldo"), new Peregrino("Sor Ana")};
                          for (Viajero v : viajeros) {
                              System.out.println(v.nombre + " paga de recargo " + recargo * v.factorRecargo());
                          }

                          List<String> pasaportes = List.of("AR-101", "UY-202", "AR-101", "CL-303", "UY-202", "AR-101");
                          Set<String> vistos = new LinkedHashSet<>();
                          Set<String> duplicados = new LinkedHashSet<>();
                          for (String p : pasaportes) {
                              if (!vistos.add(p)) {
                                  duplicados.add(p);
                              }
                          }
                          System.out.println("Únicos: " + vistos);
                          System.out.println("Duplicados: " + duplicados);
                      }
                  }

                  abstract class Viajero {
                      final String nombre;

                      Viajero(String nombre) { this.nombre = nombre; }

                      abstract double factorRecargo();
                  }

                  class Mercader extends Viajero {
                      Mercader(String nombre) { super(nombre); }

                      double factorRecargo() { return 1.0; }
                  }

                  class Peregrino extends Viajero {
                      Peregrino(String nombre) { super(nombre); }

                      double factorRecargo() { return ___; }
                  }
              ''',
              solucion='''
                  import java.util.LinkedHashSet;
                  import java.util.List;
                  import java.util.Set;

                  public class Dragon3 {
                      public static void main(String[] args) {
                          double recargo = 30;
                          Viajero[] viajeros = {new Mercader("Baldo"), new Peregrino("Sor Ana")};
                          for (Viajero v : viajeros) {
                              System.out.println(v.nombre + " paga de recargo " + recargo * v.factorRecargo());
                          }

                          List<String> pasaportes = List.of("AR-101", "UY-202", "AR-101", "CL-303", "UY-202", "AR-101");
                          Set<String> vistos = new LinkedHashSet<>();
                          Set<String> duplicados = new LinkedHashSet<>();
                          for (String p : pasaportes) {
                              if (!vistos.add(p)) {
                                  duplicados.add(p);
                              }
                          }
                          System.out.println("Únicos: " + vistos);
                          System.out.println("Duplicados: " + duplicados);
                      }
                  }

                  abstract class Viajero {
                      final String nombre;

                      Viajero(String nombre) { this.nombre = nombre; }

                      abstract double factorRecargo();
                  }

                  class Mercader extends Viajero {
                      Mercader(String nombre) { super(nombre); }

                      double factorRecargo() { return 1.0; }
                  }

                  class Peregrino extends Viajero {
                      Peregrino(String nombre) { super(nombre); }

                      double factorRecargo() { return 0.5; }
                  }
              ''',
              al_superar="Quince para la peregrina, treinta para Baldo, y los repetidos en una pasada. Al Dragón le quedan pocas escamas encendidas.",
              imagen=["Sor Ana, una peregrina de capa clara, y Baldo con su sobretodo, frente a una balanza de recargos.",
                      "Una fila de pasaportes donde tres se iluminan en rojo; el Dragón con casi todas las escamas apagadas."]),
            m(id="R05-N06-P4", titulo="La declaración completa",
              lugar="La cima de la Torre", personajes="Zed, Gheco, Nadia, Kaffa, el Dragón del Imperio",
              carta="El servicio del examen | busca en el HashMap, suma impuestos, aplica la estrategia activa y el factor del viajero, responde un DTO · el controlador solo lo llama",
              recompensa="xp 25, oro 40",
              item="Llave Maestra",
              escena="""
                  La última pregunta del Dragón es la declaración completa: Baldo trae una caja y un barril, se demoró 5 días, y la estrategia activa es la normal. —Juntá todo en el **servicio** —dice Kaffa—, y que responda un DTO. Como en el examen.
              """,
              sugiere="El servicio busca cada mercancía en el `HashMap` por código, suma valores e impuestos, calcula el recargo con la estrategia activa por el factor del viajero y arma la respuesta. El total es impuestos más recargo.",
              desafio="Completá el total de la declaración.",
              inicial='''
                  import java.util.HashMap;
                  import java.util.List;
                  import java.util.Map;

                  public class Dragon4 {
                      record Mercancia(String codigo, double valor, double impuesto) { }

                      record DeclaracionRespuesta(String viajero, double impuestos, double recargo, double total) { }

                      static final Map<String, Mercancia> DEPOSITO = new HashMap<>();

                      static DeclaracionRespuesta declarar(String viajero, double factor, List<String> codigos, int dias) {
                          double valor = 0;
                          double impuestos = 0;
                          for (String c : codigos) {
                              Mercancia m = DEPOSITO.get(c);
                              valor += m.valor();
                              impuestos += m.impuesto();
                          }
                          double recargo = valor * 0.02 * dias * factor;
                          double total = ___;
                          return new DeclaracionRespuesta(viajero, impuestos, recargo, total);
                      }

                      public static void main(String[] args) {
                          DEPOSITO.put("C1", new Mercancia("C1", 1000, 100));
                          DEPOSITO.put("B1", new Mercancia("B1", 500, 70));
                          System.out.println(declarar("Baldo", 1.0, List.of("C1", "B1"), 5));
                          System.out.println(declarar("Sor Ana", 0.5, List.of("C1", "B1"), 5));
                      }
                  }
              ''',
              solucion='''
                  import java.util.HashMap;
                  import java.util.List;
                  import java.util.Map;

                  public class Dragon4 {
                      record Mercancia(String codigo, double valor, double impuesto) { }

                      record DeclaracionRespuesta(String viajero, double impuestos, double recargo, double total) { }

                      static final Map<String, Mercancia> DEPOSITO = new HashMap<>();

                      static DeclaracionRespuesta declarar(String viajero, double factor, List<String> codigos, int dias) {
                          double valor = 0;
                          double impuestos = 0;
                          for (String c : codigos) {
                              Mercancia m = DEPOSITO.get(c);
                              valor += m.valor();
                              impuestos += m.impuesto();
                          }
                          double recargo = valor * 0.02 * dias * factor;
                          double total = impuestos + recargo;
                          return new DeclaracionRespuesta(viajero, impuestos, recargo, total);
                      }

                      public static void main(String[] args) {
                          DEPOSITO.put("C1", new Mercancia("C1", 1000, 100));
                          DEPOSITO.put("B1", new Mercancia("B1", 500, 70));
                          System.out.println(declarar("Baldo", 1.0, List.of("C1", "B1"), 5));
                          System.out.println(declarar("Sor Ana", 0.5, List.of("C1", "B1"), 5));
                      }
                  }
              ''',
              al_superar="""
                  Trescientos veinte para Baldo, doscientos cuarenta y cinco para la peregrina. La última escama se apaga y el **Dragón del Imperio** se deshace en piezas que vuelven, una por una, a su lugar en la Torre.
                  En la mano de Zed, la ganzúa termina de transformarse: ya no es una ganzúa, es la **Llave Maestra**. Kaffa le estampa el sello de arquitecto en el pliego. Nadia, en la puerta, aplaude. Una sola vez, pero aplaude.
                  Detrás del Dragón, la ventana más alta tiene un marco vacío, esperando un vidrio.
              """,
              imagen=["El Dragón del Imperio deshaciéndose en piezas luminosas que vuelan a su lugar en la Torre.",
                      "La ganzúa de Zed transformándose en una llave maestra dorada con dientes de engranaje.",
                      "Kaffa estampando un sello en el pliego; Nadia aplaudiendo en la puerta; al fondo, una ventana con el marco vacío."]),
        ],
    },
]
