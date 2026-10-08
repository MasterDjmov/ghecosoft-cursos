from genjava import m

# S03 (el Arcade) y S04 (el Puerto de Spring). El Arcade sin ventana: el estado del juego, el bucle con un dt
# fijo, las teclas apretadas, Rectangle.intersects y el azar con semilla. El Puerto imita JPA con Java puro:
# entidades con id generado, un repositorio genérico, consultas derivadas, relaciones y el problema N+1.

NODOS = [
    {
        "titulo": "S03-N01 · El lienzo y el bucle de juego",
        "misiones": [
            m(id="S03-N01-P1", titulo="El estado y el dibujo",
              lugar="El Arcade Imperial", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Estado separado del dibujo | una clase con los DATOS del juego (posición, puntos) · el dibujo solo los lee · así se prueba sin pantalla",
              recompensa="xp 10, oro 10",
              escena="""
                  En el Arcade Imperial, las máquinas brillan con figuras que se mueven solas. Gheco abre una por atrás: adentro no hay dibujos, hay **números**. —El juego es su estado —dice—. El dibujo solo lo muestra.
              """,
              sugiere="El **estado** del juego (dónde está la nave, cuántos puntos hay) va en una clase propia, sin nada de Swing. El método que dibuja solo lo lee. Así se puede probar el juego imprimiendo el estado.",
              desafio="Completá el método que mueve la nave: suma la velocidad a la posición.",
              inicial='''
                  public class Lienzo {
                      static class Estado {
                          int x = 10;
                          int velocidad = 4;
                          int puntos = 0;

                          void actualizar() {
                              ___;
                              puntos++;
                          }

                          String describir() {
                              return "nave en x=" + x + ", puntos=" + puntos;
                          }
                      }

                      public static void main(String[] args) {
                          Estado estado = new Estado();
                          for (int cuadro = 1; cuadro <= 3; cuadro++) {
                              estado.actualizar();
                              System.out.println("Cuadro " + cuadro + ": " + estado.describir());
                          }
                      }
                  }
              ''',
              solucion='''
                  public class Lienzo {
                      static class Estado {
                          int x = 10;
                          int velocidad = 4;
                          int puntos = 0;

                          void actualizar() {
                              x += velocidad;
                              puntos++;
                          }

                          String describir() {
                              return "nave en x=" + x + ", puntos=" + puntos;
                          }
                      }

                      public static void main(String[] args) {
                          Estado estado = new Estado();
                          for (int cuadro = 1; cuadro <= 3; cuadro++) {
                              estado.actualizar();
                              System.out.println("Cuadro " + cuadro + ": " + estado.describir());
                          }
                      }
                  }
              ''',
              al_superar="Tres cuadros, la nave avanza y suma puntos. Ninguna ventana se abrió: el juego vive en los números.",
              imagen=["El Arcade Imperial: una sala oscura llena de máquinas con pantallas que brillan.",
                      "Gheco abriendo una máquina por atrás: adentro hay números flotando en vez de dibujos."]),
            m(id="S03-N01-P2", titulo="El bucle de juego",
              lugar="El Arcade Imperial", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Bucle de juego | cada vuelta: actualizar el estado y redibujar · con un javax.swing.Timer cada N milisegundos · acá, un for de cuadros",
              recompensa="xp 10, oro 10",
              escena="""
                  Las máquinas del Arcade repiten lo mismo sesenta veces por segundo: **actualizar** y **dibujar**. Zed arma el bucle de una pelota que rebota en los bordes.
              """,
              sugiere="En cada cuadro, la pelota avanza con su velocidad; si pasa un borde, la velocidad cambia de signo (`vx = -vx`). En Swing esto lo dispara un `Timer`; para probarlo alcanza un `for` de cuadros.",
              desafio="Completá el rebote: si se pasa del borde derecho (100) o del izquierdo (0), la velocidad se invierte.",
              inicial='''
                  public class Rebote {
                      public static void main(String[] args) {
                          int x = 80;
                          int vx = 15;
                          StringBuilder recorrido = new StringBuilder();
                          for (int cuadro = 0; cuadro < 8; cuadro++) {
                              x += vx;
                              if (x > 100 || x < 0) {
                                  ___;
                                  x += vx;
                              }
                              recorrido.append(x).append(" ");
                          }
                          System.out.println("Posiciones: " + recorrido.toString().trim());
                      }
                  }
              ''',
              solucion='''
                  public class Rebote {
                      public static void main(String[] args) {
                          int x = 80;
                          int vx = 15;
                          StringBuilder recorrido = new StringBuilder();
                          for (int cuadro = 0; cuadro < 8; cuadro++) {
                              x += vx;
                              if (x > 100 || x < 0) {
                                  vx = -vx;
                                  x += vx;
                              }
                              recorrido.append(x).append(" ");
                          }
                          System.out.println("Posiciones: " + recorrido.toString().trim());
                      }
                  }
              ''',
              al_superar="La pelota llega al borde y vuelve. Nadia mira las posiciones y entiende el juego sin haberlo visto.",
              imagen=["Una pantalla de máquina con una pelota de luz rebotando en el borde, dejando una estela.",
                      "Nadia leyendo la lista de posiciones en un papel."]),
            m(id="S03-N01-P3", titulo="Igual en cualquier máquina",
              lugar="El Arcade Imperial", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Paso de tiempo (dt) | moverse con velocidad × dt (en segundos) · el juego avanza igual en una máquina rápida o en una lenta",
              recompensa="xp 15, oro 15",
              escena="""
                  En una máquina vieja, la nave anda lenta; en una nueva, vuela. —Si avanzás «un poco por cuadro» —dice Kaffa—, el juego depende de la máquina. Avanzá según el **tiempo** que pasó.
              """,
              sugiere="La posición avanza `velocidad * dt`, donde `dt` es el tiempo del cuadro en segundos. Con más cuadros por segundo, cada `dt` es más chico, y en un segundo la nave recorre lo mismo.",
              desafio="Completá el avance: la velocidad por el tiempo del cuadro.",
              inicial='''
                  public class TiempoFijo {
                      static double recorrer(int cuadrosPorSegundo, double velocidad) {
                          double dt = 1.0 / cuadrosPorSegundo;
                          double x = 0;
                          for (int i = 0; i < cuadrosPorSegundo; i++) {
                              x += ___;
                          }
                          return x;
                      }

                      public static void main(String[] args) {
                          for (int fps : new int[] {30, 60, 120}) {
                              System.out.printf(java.util.Locale.US, "%d cuadros por segundo: %.1f píxeles en un segundo%n", fps, recorrer(fps, 200));
                          }
                      }
                  }
              ''',
              solucion='''
                  public class TiempoFijo {
                      static double recorrer(int cuadrosPorSegundo, double velocidad) {
                          double dt = 1.0 / cuadrosPorSegundo;
                          double x = 0;
                          for (int i = 0; i < cuadrosPorSegundo; i++) {
                              x += velocidad * dt;
                          }
                          return x;
                      }

                      public static void main(String[] args) {
                          for (int fps : new int[] {30, 60, 120}) {
                              System.out.printf(java.util.Locale.US, "%d cuadros por segundo: %.1f píxeles en un segundo%n", fps, recorrer(fps, 200));
                          }
                      }
                  }
              ''',
              al_superar="""
                  Doscientos píxeles en un segundo, en las tres máquinas. El dueño del Arcade le regala a Zed una ficha.
                  En la máquina del fondo, un cartel titila: «JUGADOR 1: APRETÁ UNA TECLA».
              """,
              imagen=["Tres máquinas del Arcade, una vieja, una media y una nueva, con la misma nave en el mismo lugar.",
                      "El dueño del Arcade dándole una ficha a Zed; al fondo, una máquina con un cartel titilando."]),
        ],
    },
    {
        "titulo": "S03-N02 · Teclado, movimiento y estados",
        "misiones": [
            m(id="S03-N02-P1", titulo="Las teclas apretadas",
              lugar="La máquina del fondo del Arcade", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Teclas apretadas | un Set con las teclas que están abajo · al apretar se agrega, al soltar se saca · cada cuadro se mueve según lo que hay",
              recompensa="xp 10, oro 10",
              escena="""
                  En la máquina del fondo, Zed aprieta la flecha derecha y la mantiene. La nave tiene que moverse **mientras** esté apretada, no una vez por cada toque.
              """,
              sugiere="Se guarda qué teclas están apretadas en un `Set`: al apretar, `add`; al soltar, `remove`. En cada cuadro, si el conjunto tiene la derecha, la nave avanza.",
              desafio="Completá la condición del movimiento a la derecha.",
              inicial='''
                  import java.util.HashSet;
                  import java.util.Set;

                  public class Teclas {
                      public static void main(String[] args) {
                          Set<String> apretadas = new HashSet<>();
                          int x = 50;
                          String[][] eventos = {{"apreta", "DERECHA"}, {}, {}, {"suelta", "DERECHA"}, {}};
                          for (int cuadro = 0; cuadro < eventos.length; cuadro++) {
                              String[] e = eventos[cuadro];
                              if (e.length == 2 && e[0].equals("apreta")) apretadas.add(e[1]);
                              if (e.length == 2 && e[0].equals("suelta")) apretadas.remove(e[1]);
                              if (___) {
                                  x += 5;
                              }
                              System.out.println("Cuadro " + cuadro + ": x=" + x + " teclas=" + apretadas);
                          }
                      }
                  }
              ''',
              solucion='''
                  import java.util.HashSet;
                  import java.util.Set;

                  public class Teclas {
                      public static void main(String[] args) {
                          Set<String> apretadas = new HashSet<>();
                          int x = 50;
                          String[][] eventos = {{"apreta", "DERECHA"}, {}, {}, {"suelta", "DERECHA"}, {}};
                          for (int cuadro = 0; cuadro < eventos.length; cuadro++) {
                              String[] e = eventos[cuadro];
                              if (e.length == 2 && e[0].equals("apreta")) apretadas.add(e[1]);
                              if (e.length == 2 && e[0].equals("suelta")) apretadas.remove(e[1]);
                              if (apretadas.contains("DERECHA")) {
                                  x += 5;
                              }
                              System.out.println("Cuadro " + cuadro + ": x=" + x + " teclas=" + apretadas);
                          }
                      }
                  }
              ''',
              al_superar="Mientras la flecha está abajo, la nave avanza; cuando la suelta, se queda. —Igual que con las cerraduras —dice Zed—: importa cuánto tiempo apretás.",
              imagen=["Una mano apretando una flecha luminosa en el tablero de la máquina; en la pantalla, la nave avanzando.",
                      "Zed concentrado frente a la máquina del fondo."]),
            m(id="S03-N02-P2", titulo="Los bordes de la pantalla",
              lugar="La máquina del fondo del Arcade", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Límites | la posición se encierra entre 0 y el ancho menos el tamaño · Math.max(min, Math.min(max, x))",
              recompensa="xp 10, oro 10",
              escena="""
                  Zed mantiene apretada la flecha y la nave se sale de la pantalla. Desaparece. —Encerrala —dice Gheco.
              """,
              sugiere="Para que la nave no se salga: `x = Math.max(0, Math.min(ANCHO - TAM, x))`. Si se pasa por un lado o por el otro, queda pegada al borde.",
              desafio="Completá el encierro de la posición entre 0 y `ANCHO - TAM`.",
              inicial='''
                  public class Bordes {
                      static final int ANCHO = 200;
                      static final int TAM = 20;

                      public static void main(String[] args) {
                          int x = 150;
                          for (int cuadro = 0; cuadro < 5; cuadro++) {
                              x += 12;
                              x = ___;
                              System.out.println("Cuadro " + cuadro + ": x=" + x);
                          }
                      }
                  }
              ''',
              solucion='''
                  public class Bordes {
                      static final int ANCHO = 200;
                      static final int TAM = 20;

                      public static void main(String[] args) {
                          int x = 150;
                          for (int cuadro = 0; cuadro < 5; cuadro++) {
                              x += 12;
                              x = Math.max(0, Math.min(ANCHO - TAM, x));
                              System.out.println("Cuadro " + cuadro + ": x=" + x);
                          }
                      }
                  }
              ''',
              al_superar="La nave se queda pegada en 180, justo antes del borde. Ni un píxel afuera.",
              imagen=["Una nave de luz pegada al borde derecho de la pantalla, sin poder seguir.",
                      "Gheco con un cartel de «PROHIBIDO SALIR»."]),
            m(id="S03-N02-P3", titulo="Menú, jugando, pausa, fin",
              lugar="La máquina del fondo del Arcade", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Estados con enum | enum Estado { MENU, JUGANDO, PAUSA, FIN } · cada tecla hace algo distinto según el estado · switch",
              recompensa="xp 15, oro 15",
              escena="""
                  La máquina tiene momentos: el **menú** espera, **jugando** se mueve, la **pausa** congela y el **fin** muestra el puntaje. La misma tecla hace cosas distintas en cada uno.
              """,
              sugiere="Los estados van en un `enum`. Al apretar una tecla, un `switch` sobre el estado actual decide el siguiente: desde el menú, ENTER empieza; jugando, P pausa; en pausa, P sigue.",
              desafio="Completá la transición de la pausa: con P, vuelve a JUGANDO.",
              inicial='''
                  public class Estados {
                      enum Estado { MENU, JUGANDO, PAUSA, FIN }

                      static Estado tecla(Estado actual, String tecla) {
                          return switch (actual) {
                              case MENU -> tecla.equals("ENTER") ? Estado.JUGANDO : actual;
                              case JUGANDO -> tecla.equals("P") ? Estado.PAUSA : tecla.equals("X") ? Estado.FIN : actual;
                              case PAUSA -> tecla.equals("P") ? ___ : actual;
                              case FIN -> tecla.equals("ENTER") ? Estado.MENU : actual;
                          };
                      }

                      public static void main(String[] args) {
                          Estado e = Estado.MENU;
                          for (String t : new String[] {"P", "ENTER", "P", "X", "P", "X", "ENTER"}) {
                              e = tecla(e, t);
                              System.out.println(t + " -> " + e);
                          }
                      }
                  }
              ''',
              solucion='''
                  public class Estados {
                      enum Estado { MENU, JUGANDO, PAUSA, FIN }

                      static Estado tecla(Estado actual, String tecla) {
                          return switch (actual) {
                              case MENU -> tecla.equals("ENTER") ? Estado.JUGANDO : actual;
                              case JUGANDO -> tecla.equals("P") ? Estado.PAUSA : tecla.equals("X") ? Estado.FIN : actual;
                              case PAUSA -> tecla.equals("P") ? Estado.JUGANDO : actual;
                              case FIN -> tecla.equals("ENTER") ? Estado.MENU : actual;
                          };
                      }

                      public static void main(String[] args) {
                          Estado e = Estado.MENU;
                          for (String t : new String[] {"P", "ENTER", "P", "X", "P", "X", "ENTER"}) {
                              e = tecla(e, t);
                              System.out.println(t + " -> " + e);
                          }
                      }
                  }
              ''',
              al_superar="""
                  La máquina responde a cada tecla según el momento. En la pausa, la X no hace nada: el juego está congelado.
                  —Ya se mueve —dice Gheco—. Ahora tiene que **chocar**.
              """,
              imagen=["Cuatro pantallas de la misma máquina: menú, jugando, pausa y fin, unidas por flechas con letras.",
                      "Gheco señalando la pantalla de pausa."]),
        ],
    },
    {
        "titulo": "S03-N03 · Sprites, colisiones y animación",
        "misiones": [
            m(id="S03-N03-P1", titulo="Cuando dos rectángulos se tocan",
              lugar="La máquina de las monedas", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Colisiones | cada cosa tiene un Rectangle (x, y, ancho, alto) · a.intersects(b) dice si se tocan",
              recompensa="xp 10, oro 10",
              escena="""
                  En la máquina de las monedas, la nave tiene que juntar monedas que caen. ¿Cómo sabe el juego que la tocó? —Cada cosa es una **caja** —dice Gheco—. Si las cajas se cruzan, chocaron.
              """,
              sugiere="`java.awt.Rectangle` guarda una caja con `x`, `y`, ancho y alto. `nave.intersects(moneda)` devuelve `true` si se superponen.",
              desafio="Completá la pregunta: ¿la nave toca esta moneda?",
              inicial='''
                  import java.awt.Rectangle;

                  public class Choques {
                      public static void main(String[] args) {
                          Rectangle nave = new Rectangle(100, 200, 30, 20);
                          Rectangle[] monedas = {new Rectangle(110, 195, 10, 10), new Rectangle(160, 200, 10, 10), new Rectangle(125, 215, 10, 10)};
                          for (int i = 0; i < monedas.length; i++) {
                              boolean toca = ___;
                              System.out.println("Moneda " + (i + 1) + ": " + (toca ? "¡atrapada!" : "pasa de largo"));
                          }
                      }
                  }
              ''',
              solucion='''
                  import java.awt.Rectangle;

                  public class Choques {
                      public static void main(String[] args) {
                          Rectangle nave = new Rectangle(100, 200, 30, 20);
                          Rectangle[] monedas = {new Rectangle(110, 195, 10, 10), new Rectangle(160, 200, 10, 10), new Rectangle(125, 215, 10, 10)};
                          for (int i = 0; i < monedas.length; i++) {
                              boolean toca = nave.intersects(monedas[i]);
                              System.out.println("Moneda " + (i + 1) + ": " + (toca ? "¡atrapada!" : "pasa de largo"));
                          }
                      }
                  }
              ''',
              al_superar="Dos atrapadas, una que se escapa. —Cajas invisibles alrededor de todo —dice Nadia—. Como los cajones de la Aduana.",
              imagen=["Una nave y tres monedas en la pantalla, con sus cajas dibujadas en líneas finas; dos se superponen.",
                      "Nadia señalando las cajas."]),
            m(id="S03-N03-P2", titulo="Juntar sin tropezar",
              lugar="La máquina de las monedas", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="orco",
              carta="Quitar durante el juego | borrar de la lista mientras se la recorre con for-each da ConcurrentModificationException · removeIf o un Iterator",
              recompensa="xp 15, oro 15",
              escena="""
                  Zed borra cada moneda atrapada de la lista en el mismo for-each que la recorre, y el juego se corta con un **orco**: *ConcurrentModificationException*.
              """,
              sugiere="No se puede sacar de una lista mientras se la recorre con for-each. `monedas.removeIf(m -> nave.intersects(m))` saca todas las atrapadas de una vez, sin tropezar.",
              desafio="Ejecutalo, mirá el error y reemplazá el for-each por un `removeIf`.",
              inicial='''
                  import java.awt.Rectangle;
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Juntar {
                      public static void main(String[] args) {
                          Rectangle nave = new Rectangle(100, 200, 30, 20);
                          List<Rectangle> monedas = new ArrayList<>(List.of(new Rectangle(110, 195, 10, 10),
                                  new Rectangle(160, 200, 10, 10), new Rectangle(125, 215, 10, 10)));
                          for (Rectangle m : monedas) {
                              if (nave.intersects(m)) {
                                  monedas.remove(m);
                              }
                          }
                          System.out.println("Monedas en pantalla: " + monedas.size());
                      }
                  }
              ''',
              solucion='''
                  import java.awt.Rectangle;
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Juntar {
                      public static void main(String[] args) {
                          Rectangle nave = new Rectangle(100, 200, 30, 20);
                          List<Rectangle> monedas = new ArrayList<>(List.of(new Rectangle(110, 195, 10, 10),
                                  new Rectangle(160, 200, 10, 10), new Rectangle(125, 215, 10, 10)));
                          monedas.removeIf(m -> nave.intersects(m));
                          System.out.println("Monedas en pantalla: " + monedas.size());
                      }
                  }
              ''',
              al_superar="Queda una moneda, la que se escapó, y el juego sigue. El orco se va masticando una ficha.",
              imagen=["Un orco saliendo de la pantalla con un cartel «ConcurrentModificationException».",
                      "La nave con dos monedas guardadas y una tercera cayendo lejos."]),
            m(id="S03-N03-P3", titulo="El azar que se repite",
              lugar="La máquina de las monedas", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Azar con semilla y animación | new Random(42): las monedas caen siempre igual (sirve para probar) · el cuadro del sprite: (tick / velocidad) % cuadros",
              recompensa="xp 15, oro 20",
              escena="""
                  Zed sospecha de la máquina, como del tahúr de la Aduana: las monedas caen siempre en los mismos lugares. —Tiene semilla —confirma Gheco—. Para probar un juego, el azar tiene que repetirse.
              """,
              sugiere="Con `new Random(42)`, la secuencia es siempre la misma. Cada moneda sale en `r.nextInt(ANCHO)`. Para animar, el cuadro del sprite cambia cada pocos ticks: `(tick / 3) % 4`.",
              desafio="Completá el cálculo del cuadro de la animación: cambia cada 3 ticks, entre 4 cuadros.",
              inicial='''
                  import java.util.Random;

                  public class Azar {
                      public static void main(String[] args) {
                          Random r = new Random(42);
                          StringBuilder lugares = new StringBuilder();
                          for (int i = 0; i < 5; i++) {
                              lugares.append(r.nextInt(200)).append(" ");
                          }
                          System.out.println("Monedas en x: " + lugares.toString().trim());
                          StringBuilder cuadros = new StringBuilder();
                          for (int tick = 0; tick < 12; tick++) {
                              int cuadro = ___;
                              cuadros.append(cuadro);
                          }
                          System.out.println("Cuadros del sprite: " + cuadros);
                      }
                  }
              ''',
              solucion='''
                  import java.util.Random;

                  public class Azar {
                      public static void main(String[] args) {
                          Random r = new Random(42);
                          StringBuilder lugares = new StringBuilder();
                          for (int i = 0; i < 5; i++) {
                              lugares.append(r.nextInt(200)).append(" ");
                          }
                          System.out.println("Monedas en x: " + lugares.toString().trim());
                          StringBuilder cuadros = new StringBuilder();
                          for (int tick = 0; tick < 12; tick++) {
                              int cuadro = (tick / 3) % 4;
                              cuadros.append(cuadro);
                          }
                          System.out.println("Cuadros del sprite: " + cuadros);
                      }
                  }
              ''',
              al_superar="""
                  Las monedas caen siempre igual y el sprite gira en cuatro cuadros. Zed, que conoce las trampas, aprueba la máquina: para probar, el azar tiene que ser honesto **y** repetible.
                  En el centro del Arcade se enciende la máquina más grande. Adentro hay alguien: **el Guardián de la Máquina**.
              """,
              imagen=["Una tira de cuatro cuadros de una moneda girando, como un rollo de película.",
                      "La máquina gigante del centro del Arcade encendiéndose, con una silueta adentro."]),
        ],
    },
    {
        "titulo": "S03-N04 · Jefe del Arcade: el Guardián de la Máquina",
        "misiones": [
            m(id="S03-N04-P1", titulo="El mundo del juego",
              lugar="La máquina gigante del Arcade", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="dragon",
              carta="Mundo y entidades | una clase Mundo con la lista de entidades · cada Entidad sabe actualizarse · el mundo las recorre",
              recompensa="xp 20, oro 20",
              escena="""
                  El **Guardián de la Máquina** desafía a Zed: un juego entero, ordenado en clases, o no sale del Arcade. —Primero el **mundo** —dice Kaffa—: la lista de todo lo que se mueve.
              """,
              sugiere="Cada `Entidad` tiene posición y velocidad y sabe `actualizar()`. El `Mundo` las guarda en una lista y en cada tick llama a `actualizar()` de todas: polimorfismo en el juego.",
              desafio="Completá el tick del mundo: que cada entidad se actualice.",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Mundo1 {
                      static class Entidad {
                          final String nombre;
                          int y;
                          final int vy;

                          Entidad(String nombre, int y, int vy) {
                              this.nombre = nombre;
                              this.y = y;
                              this.vy = vy;
                          }

                          void actualizar() { y += vy; }
                      }

                      static class Mundo {
                          final List<Entidad> entidades = new ArrayList<>();

                          void tick() {
                              for (Entidad e : entidades) {
                                  ___;
                              }
                          }
                      }

                      public static void main(String[] args) {
                          Mundo mundo = new Mundo();
                          mundo.entidades.add(new Entidad("roca", 0, 5));
                          mundo.entidades.add(new Entidad("moneda", 10, 3));
                          for (int t = 1; t <= 2; t++) {
                              mundo.tick();
                              StringBuilder linea = new StringBuilder("Tick " + t + ":");
                              mundo.entidades.forEach(e -> linea.append(" ").append(e.nombre).append(" y=").append(e.y));
                              System.out.println(linea);
                          }
                      }
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Mundo1 {
                      static class Entidad {
                          final String nombre;
                          int y;
                          final int vy;

                          Entidad(String nombre, int y, int vy) {
                              this.nombre = nombre;
                              this.y = y;
                              this.vy = vy;
                          }

                          void actualizar() { y += vy; }
                      }

                      static class Mundo {
                          final List<Entidad> entidades = new ArrayList<>();

                          void tick() {
                              for (Entidad e : entidades) {
                                  e.actualizar();
                              }
                          }
                      }

                      public static void main(String[] args) {
                          Mundo mundo = new Mundo();
                          mundo.entidades.add(new Entidad("roca", 0, 5));
                          mundo.entidades.add(new Entidad("moneda", 10, 3));
                          for (int t = 1; t <= 2; t++) {
                              mundo.tick();
                              StringBuilder linea = new StringBuilder("Tick " + t + ":");
                              mundo.entidades.forEach(e -> linea.append(" ").append(e.nombre).append(" y=").append(e.y));
                              System.out.println(linea);
                          }
                      }
                  }
              ''',
              al_superar="El mundo late: rocas y monedas caen a su ritmo. El Guardián, adentro de la máquina, levanta una ceja de píxeles.",
              imagen=["El Guardián de la Máquina: un robot de arcade hecho de botones y pantallas, con una cara de píxeles, adentro de la máquina gigante.",
                      "En la pantalla, rocas y monedas cayendo."]),
            m(id="S03-N04-P2", titulo="Puntaje y vidas",
              lugar="La máquina gigante del Arcade", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Reglas del juego | moneda: +10 puntos · roca: −1 vida · sin vidas: FIN · las reglas en un solo método",
              recompensa="xp 20, oro 25",
              escena="""
                  El Guardián dicta las reglas: cada moneda suma 10, cada roca quita una vida, y con cero vidas se termina. Zed juega una partida grabada y tiene que anotar todo bien.
              """,
              sugiere="Las reglas van en un solo lugar: según qué tocó la nave, se suman puntos o se resta una vida. Con cero vidas, el juego pasa a FIN y no cuenta nada más.",
              desafio="Completá la regla de la roca: resta una vida.",
              inicial='''
                  public class Reglas {
                      static int puntos = 0;
                      static int vidas = 2;
                      static boolean fin = false;

                      static void toco(String cosa) {
                          if (fin) {
                              return;
                          }
                          if (cosa.equals("moneda")) {
                              puntos += 10;
                          } else if (cosa.equals("roca")) {
                              ___;
                              if (vidas == 0) {
                                  fin = true;
                              }
                          }
                      }

                      public static void main(String[] args) {
                          for (String c : new String[] {"moneda", "moneda", "roca", "moneda", "roca", "moneda"}) {
                              toco(c);
                              System.out.println(c + ": puntos=" + puntos + " vidas=" + vidas + (fin ? " FIN" : ""));
                          }
                      }
                  }
              ''',
              solucion='''
                  public class Reglas {
                      static int puntos = 0;
                      static int vidas = 2;
                      static boolean fin = false;

                      static void toco(String cosa) {
                          if (fin) {
                              return;
                          }
                          if (cosa.equals("moneda")) {
                              puntos += 10;
                          } else if (cosa.equals("roca")) {
                              vidas--;
                              if (vidas == 0) {
                                  fin = true;
                              }
                          }
                      }

                      public static void main(String[] args) {
                          for (String c : new String[] {"moneda", "moneda", "roca", "moneda", "roca", "moneda"}) {
                              toco(c);
                              System.out.println(c + ": puntos=" + puntos + " vidas=" + vidas + (fin ? " FIN" : ""));
                          }
                      }
                  }
              ''',
              al_superar="Treinta puntos y fin. La última moneda ya no cuenta: el juego terminó. El Guardián asiente: las reglas están en su lugar.",
              imagen=["Un tablero de puntaje del Arcade con «30» y dos corazones apagados; la palabra FIN titilando.",
                      "El Guardián asintiendo con su cara de píxeles."]),
            m(id="S03-N04-P3", titulo="El mejor puntaje",
              lugar="La máquina gigante del Arcade", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Guardar el récord | se lee el mejor puntaje de un archivo · si el nuevo es mayor, se reemplaza · Files.writeString / readString",
              recompensa="xp 25, oro 30",
              escena="""
                  La última prueba del Guardián: que la máquina **recuerde** el mejor puntaje entre partidas. Hasta hoy, el récord lo tenía el Guardián mismo: 120 puntos.
              """,
              sugiere="El récord se guarda en un archivo. Se lee con `Files.readString`, se compara con el puntaje nuevo y, si es mayor, se escribe con `Files.writeString`. Al terminar se borra el archivo de prueba.",
              desafio="Completá la condición: si el puntaje nuevo supera al récord.",
              inicial='''
                  import java.nio.file.Files;
                  import java.nio.file.Path;

                  public class Record {
                      public static void main(String[] args) throws Exception {
                          Path archivo = Files.createTempFile("record", ".txt");
                          Files.writeString(archivo, "120");
                          for (int puntaje : new int[] {90, 150, 130}) {
                              int record = Integer.parseInt(Files.readString(archivo).trim());
                              if (___) {
                                  Files.writeString(archivo, String.valueOf(puntaje));
                                  System.out.println(puntaje + ": ¡nuevo récord!");
                              } else {
                                  System.out.println(puntaje + ": el récord sigue en " + record);
                              }
                          }
                          System.out.println("Récord guardado: " + Files.readString(archivo));
                          Files.delete(archivo);
                      }
                  }
              ''',
              solucion='''
                  import java.nio.file.Files;
                  import java.nio.file.Path;

                  public class Record {
                      public static void main(String[] args) throws Exception {
                          Path archivo = Files.createTempFile("record", ".txt");
                          Files.writeString(archivo, "120");
                          for (int puntaje : new int[] {90, 150, 130}) {
                              int record = Integer.parseInt(Files.readString(archivo).trim());
                              if (puntaje > record) {
                                  Files.writeString(archivo, String.valueOf(puntaje));
                                  System.out.println(puntaje + ": ¡nuevo récord!");
                              } else {
                                  System.out.println(puntaje + ": el récord sigue en " + record);
                              }
                          }
                          System.out.println("Récord guardado: " + Files.readString(archivo));
                          Files.delete(archivo);
                      }
                  }
              ''',
              al_superar="""
                  Ciento cincuenta: récord nuevo, con las iniciales de Zed. El Guardián de la Máquina se inclina, la pantalla gigante muestra «ZED 150» y la máquina le devuelve todas las fichas.
                  Nadia, que nunca había jugado, pide una partida.
              """,
              imagen=["La pantalla gigante del Arcade con la tabla de récords: «ZED 150» arriba de todo.",
                      "El Guardián de la Máquina inclinándose; Nadia con una ficha en la mano, lista para jugar."]),
        ],
    },
    {
        "titulo": "S04-N01 · JPA: la bóveda del Puerto",
        "misiones": [
            m(id="S04-N01-P1", titulo="Los espíritus que anotan",
              lugar="La bóveda del Puerto", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Entidad e id generado | @Entity: una clase = una tabla · @Id @GeneratedValue: el id lo pone la base al guardar · save() devuelve la entidad con su id",
              recompensa="xp 10, oro 10",
              escena="""
                  Debajo del Puerto hay una bóveda sin escribas: cuando un capitán guarda un cargamento, unos **espíritus** lo anotan solos y le ponen número. Gheco arma un repositorio de juguete para ver qué hacen.
              """,
              sugiere="En JPA, `save(entidad)` guarda y, si la entidad no tiene id, la base le asigna uno (`@GeneratedValue`). Acá un mapa hace de tabla y un contador de secuencia pone los ids.",
              desafio="Completá el `save`: si el cargamento no tiene id, asignale el siguiente de la secuencia.",
              inicial='''
                  import java.util.LinkedHashMap;
                  import java.util.Map;

                  public class Espiritus {
                      static class Cargamento {
                          Long id;
                          final String descripcion;

                          Cargamento(String descripcion) { this.descripcion = descripcion; }
                      }

                      static class CargamentoRepository {
                          private final Map<Long, Cargamento> tabla = new LinkedHashMap<>();
                          private long secuencia = 0;

                          Cargamento save(Cargamento c) {
                              if (c.id == null) {
                                  ___;
                              }
                              tabla.put(c.id, c);
                              return c;
                          }

                          long count() { return tabla.size(); }
                      }

                      public static void main(String[] args) {
                          CargamentoRepository repo = new CargamentoRepository();
                          Cargamento a = repo.save(new Cargamento("café de Kaffa"));
                          Cargamento b = repo.save(new Cargamento("vidrios de colores"));
                          System.out.println(a.id + ": " + a.descripcion);
                          System.out.println(b.id + ": " + b.descripcion);
                          System.out.println("En la tabla: " + repo.count());
                      }
                  }
              ''',
              solucion='''
                  import java.util.LinkedHashMap;
                  import java.util.Map;

                  public class Espiritus {
                      static class Cargamento {
                          Long id;
                          final String descripcion;

                          Cargamento(String descripcion) { this.descripcion = descripcion; }
                      }

                      static class CargamentoRepository {
                          private final Map<Long, Cargamento> tabla = new LinkedHashMap<>();
                          private long secuencia = 0;

                          Cargamento save(Cargamento c) {
                              if (c.id == null) {
                                  c.id = ++secuencia;
                              }
                              tabla.put(c.id, c);
                              return c;
                          }

                          long count() { return tabla.size(); }
                      }

                      public static void main(String[] args) {
                          CargamentoRepository repo = new CargamentoRepository();
                          Cargamento a = repo.save(new Cargamento("café de Kaffa"));
                          Cargamento b = repo.save(new Cargamento("vidrios de colores"));
                          System.out.println(a.id + ": " + a.descripcion);
                          System.out.println(b.id + ": " + b.descripcion);
                          System.out.println("En la tabla: " + repo.count());
                      }
                  }
              ''',
              al_superar="Cada cargamento sale con su número. —En la Bóveda escribías cada INSERT a mano —dice Kaffa—. Acá lo hacen los espíritus. Pero ojo: hacen lo que les pedís, no lo que querías pedir.",
              imagen=["La bóveda debajo del Puerto: estantes de piedra y espíritus de luz anotando en libros flotantes.",
                      "Un espíritu poniéndole un número de bronce a un cargamento."]),
            m(id="S04-N01-P2", titulo="La consulta que se escribe sola",
              lugar="La bóveda del Puerto", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Consultas derivadas | findByPuerto(\"Puerto\") · Spring arma la consulta a partir del NOMBRE del método · acá la escribimos con un stream",
              recompensa="xp 10, oro 10",
              escena="""
                  Zed le pide a un espíritu «todos los cargamentos que van al Puerto». El espíritu no necesita SQL: lee el **nombre** del pedido, `findByDestino`, y arma la consulta solo.
              """,
              sugiere="En Spring Data, declarar `List<Cargamento> findByDestino(String destino)` alcanza: la consulta sale del nombre. Por dentro hace lo que acá escribimos con un stream: filtrar por ese campo.",
              desafio="Completá el filtro de `findByDestino`.",
              inicial='''
                  import java.util.List;

                  public class Derivadas {
                      record Cargamento(Long id, String descripcion, String destino) { }

                      static final List<Cargamento> TABLA = List.of(new Cargamento(1L, "café", "Puerto"),
                              new Cargamento(2L, "vidrios", "Torre"), new Cargamento(3L, "sal", "Puerto"));

                      static List<Cargamento> findByDestino(String destino) {
                          return TABLA.stream().filter(c -> ___).toList();
                      }

                      public static void main(String[] args) {
                          findByDestino("Puerto").forEach(c -> System.out.println(c.id() + " " + c.descripcion()));
                          System.out.println("A la Torre: " + findByDestino("Torre").size());
                      }
                  }
              ''',
              solucion='''
                  import java.util.List;

                  public class Derivadas {
                      record Cargamento(Long id, String descripcion, String destino) { }

                      static final List<Cargamento> TABLA = List.of(new Cargamento(1L, "café", "Puerto"),
                              new Cargamento(2L, "vidrios", "Torre"), new Cargamento(3L, "sal", "Puerto"));

                      static List<Cargamento> findByDestino(String destino) {
                          return TABLA.stream().filter(c -> c.destino().equals(destino)).toList();
                      }

                      public static void main(String[] args) {
                          findByDestino("Puerto").forEach(c -> System.out.println(c.id() + " " + c.descripcion()));
                          System.out.println("A la Torre: " + findByDestino("Torre").size());
                      }
                  }
              ''',
              al_superar="Café y sal al Puerto, vidrios a la Torre. —Un método con buen nombre ya es una consulta —dice Gheco—. Por eso los nombres importan.",
              imagen=["Un espíritu leyendo un pergamino con «findByDestino» y señalando dos cajas.",
                      "Zed mirando cómo los cargamentos se ordenan solos."]),
            m(id="S04-N01-P3", titulo="Un barco, muchos cargamentos",
              lugar="La bóveda del Puerto", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Relaciones | @ManyToOne: cada cargamento tiene UN barco · @OneToMany: un barco tiene MUCHOS cargamentos · los dos lados se mantienen juntos",
              recompensa="xp 15, oro 20",
              escena="""
                  Cada cargamento viaja en un barco, y un barco lleva muchos cargamentos. Si se anota de un solo lado, el otro no se entera y los espíritus se confunden.
              """,
              sugiere="En una relación de dos lados, al agregar un cargamento al barco hay que actualizar **los dos**: la lista del barco (`@OneToMany`) y el barco del cargamento (`@ManyToOne`). Un método `agregar` en el barco hace las dos cosas.",
              desafio="Completá el método `agregar`: además de sumarlo a la lista, el cargamento tiene que saber en qué barco va.",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Relaciones {
                      static class Barco {
                          final String nombre;
                          final List<Cargamento> cargamentos = new ArrayList<>();

                          Barco(String nombre) { this.nombre = nombre; }

                          void agregar(Cargamento c) {
                              cargamentos.add(c);
                              ___;
                          }
                      }

                      static class Cargamento {
                          final String descripcion;
                          Barco barco;

                          Cargamento(String descripcion) { this.descripcion = descripcion; }
                      }

                      public static void main(String[] args) {
                          Barco garza = new Barco("Garza");
                          Cargamento cafe = new Cargamento("café");
                          Cargamento sal = new Cargamento("sal");
                          garza.agregar(cafe);
                          garza.agregar(sal);
                          System.out.println(garza.nombre + " lleva " + garza.cargamentos.size() + " cargamentos");
                          System.out.println("El café va en: " + cafe.barco.nombre);
                      }
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Relaciones {
                      static class Barco {
                          final String nombre;
                          final List<Cargamento> cargamentos = new ArrayList<>();

                          Barco(String nombre) { this.nombre = nombre; }

                          void agregar(Cargamento c) {
                              cargamentos.add(c);
                              c.barco = this;
                          }
                      }

                      static class Cargamento {
                          final String descripcion;
                          Barco barco;

                          Cargamento(String descripcion) { this.descripcion = descripcion; }
                      }

                      public static void main(String[] args) {
                          Barco garza = new Barco("Garza");
                          Cargamento cafe = new Cargamento("café");
                          Cargamento sal = new Cargamento("sal");
                          garza.agregar(cafe);
                          garza.agregar(sal);
                          System.out.println(garza.nombre + " lleva " + garza.cargamentos.size() + " cargamentos");
                          System.out.println("El café va en: " + cafe.barco.nombre);
                      }
                  }
              ''',
              al_superar="""
                  Los dos lados saben lo mismo. Los espíritus anotan tranquilos.
                  Pero en la boca del Puerto, el agua se agita: el **Kraken de los Servicios** pide miles de cargamentos por segundo.
              """,
              imagen=["Un barco, la Garza, con dos cajas a bordo unidas por hilos de luz de ida y vuelta.",
                      "En la boca del Puerto, un tentáculo enorme asomando del agua."]),
        ],
    },
    {
        "titulo": "S04-N02 · Jefe del Puerto: el Kraken de los Servicios",
        "misiones": [
            m(id="S04-N02-P1", titulo="Los mil pedidos del Kraken",
              lugar="La boca del Puerto", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="dragon",
              carta="El problema N+1 | 1 consulta para los barcos + 1 por cada barco para sus cargamentos · con un JOIN FETCH (o una sola consulta agrupada), son 1",
              recompensa="xp 20, oro 20",
              escena="""
                  El **Kraken de los Servicios** pide el listado de barcos con sus cargamentos. Zed lo arma como venía y los espíritus hacen **una consulta por barco**: con cien barcos, ciento una. El Kraken se ríe con cien bocas.
              """,
              sugiere="Pedir los barcos y después, por cada uno, sus cargamentos son N+1 consultas. Si se piden **todos** los cargamentos juntos y se agrupan por barco (en JPA, un `JOIN FETCH`), es una sola.",
              desafio="Completá la versión de una consulta: agrupá todos los cargamentos por barco.",
              inicial='''
                  import java.util.List;
                  import java.util.Map;
                  import java.util.TreeMap;
                  import java.util.stream.Collectors;

                  public class Kraken1 {
                      record Cargamento(String barco, String descripcion) { }

                      static int consultas = 0;
                      static final List<Cargamento> TABLA = List.of(new Cargamento("Garza", "café"), new Cargamento("Bagre", "sal"),
                              new Cargamento("Garza", "vidrios"), new Cargamento("Junco", "seda"));

                      static List<Cargamento> cargamentosDe(String barco) {
                          consultas++;
                          return TABLA.stream().filter(c -> c.barco().equals(barco)).toList();
                      }

                      static List<Cargamento> todos() {
                          consultas++;
                          return TABLA;
                      }

                      public static void main(String[] args) {
                          List<String> barcos = List.of("Bagre", "Garza", "Junco");
                          consultas = 1;
                          barcos.forEach(Kraken1::cargamentosDe);
                          System.out.println("Una por barco: " + consultas + " consultas");

                          consultas = 0;
                          Map<String, List<String>> porBarco = todos().stream().collect(Collectors.groupingBy(Cargamento::barco, TreeMap::new,
                                  Collectors.mapping(Cargamento::descripcion, Collectors.___())));
                          System.out.println("Todo junto: " + consultas + " consulta");
                          System.out.println(porBarco);
                      }
                  }
              ''',
              solucion='''
                  import java.util.List;
                  import java.util.Map;
                  import java.util.TreeMap;
                  import java.util.stream.Collectors;

                  public class Kraken1 {
                      record Cargamento(String barco, String descripcion) { }

                      static int consultas = 0;
                      static final List<Cargamento> TABLA = List.of(new Cargamento("Garza", "café"), new Cargamento("Bagre", "sal"),
                              new Cargamento("Garza", "vidrios"), new Cargamento("Junco", "seda"));

                      static List<Cargamento> cargamentosDe(String barco) {
                          consultas++;
                          return TABLA.stream().filter(c -> c.barco().equals(barco)).toList();
                      }

                      static List<Cargamento> todos() {
                          consultas++;
                          return TABLA;
                      }

                      public static void main(String[] args) {
                          List<String> barcos = List.of("Bagre", "Garza", "Junco");
                          consultas = 1;
                          barcos.forEach(Kraken1::cargamentosDe);
                          System.out.println("Una por barco: " + consultas + " consultas");

                          consultas = 0;
                          Map<String, List<String>> porBarco = todos().stream().collect(Collectors.groupingBy(Cargamento::barco, TreeMap::new,
                                  Collectors.mapping(Cargamento::descripcion, Collectors.toList())));
                          System.out.println("Todo junto: " + consultas + " consulta");
                          System.out.println(porBarco);
                      }
                  }
              ''',
              al_superar="De cuatro consultas a una. Con cien barcos, de ciento una a una. Al Kraken se le cierran noventa y nueve bocas.",
              imagen=["El Kraken de los Servicios: un pulpo gigante hecho de cables y mensajes, con muchas bocas pidiendo datos, en la boca del Puerto.",
                      "Zed frente a él con una sola caja grande en lugar de cien chicas."]),
            m(id="S04-N02-P2", titulo="Todo o nada",
              lugar="La boca del Puerto", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="@Transactional | todos los cambios de un servicio se guardan juntos o ninguno · si algo falla en el medio, se deshace lo anterior",
              recompensa="xp 20, oro 25",
              escena="""
                  El Kraken arranca un tentáculo a mitad de una transferencia de mercadería: la caja ya salió de un barco pero todavía no llegó al otro. Desapareció. —Todo o nada —dice Kaffa—: una **transacción**.
              """,
              sugiere="En una transacción, si algo falla, se vuelve atrás lo que se había hecho. Acá se imita: se guarda una copia del estado antes y, si salta una excepción, se restaura. En Spring alcanza con `@Transactional` en el servicio.",
              desafio="Completá el `catch`: restaurá el estado guardado antes de empezar.",
              inicial='''
                  import java.util.HashMap;
                  import java.util.Map;

                  public class Kraken2 {
                      static Map<String, Integer> stock = new HashMap<>(Map.of("Garza", 10, "Bagre", 0));

                      static void transferir(String desde, String hasta, int cajas, boolean kraken) {
                          Map<String, Integer> antes = new HashMap<>(stock);
                          try {
                              stock.put(desde, stock.get(desde) - cajas);
                              if (kraken) {
                                  throw new IllegalStateException("el Kraken cortó la transferencia");
                              }
                              stock.put(hasta, stock.get(hasta) + cajas);
                              System.out.println("Transferidas " + cajas + " cajas");
                          } catch (IllegalStateException e) {
                              ___;
                              System.out.println("Se deshizo: " + e.getMessage());
                          }
                      }

                      public static void main(String[] args) {
                          transferir("Garza", "Bagre", 4, false);
                          transferir("Garza", "Bagre", 3, true);
                          System.out.println("Garza: " + stock.get("Garza") + ", Bagre: " + stock.get("Bagre"));
                      }
                  }
              ''',
              solucion='''
                  import java.util.HashMap;
                  import java.util.Map;

                  public class Kraken2 {
                      static Map<String, Integer> stock = new HashMap<>(Map.of("Garza", 10, "Bagre", 0));

                      static void transferir(String desde, String hasta, int cajas, boolean kraken) {
                          Map<String, Integer> antes = new HashMap<>(stock);
                          try {
                              stock.put(desde, stock.get(desde) - cajas);
                              if (kraken) {
                                  throw new IllegalStateException("el Kraken cortó la transferencia");
                              }
                              stock.put(hasta, stock.get(hasta) + cajas);
                              System.out.println("Transferidas " + cajas + " cajas");
                          } catch (IllegalStateException e) {
                              stock = antes;
                              System.out.println("Se deshizo: " + e.getMessage());
                          }
                      }

                      public static void main(String[] args) {
                          transferir("Garza", "Bagre", 4, false);
                          transferir("Garza", "Bagre", 3, true);
                          System.out.println("Garza: " + stock.get("Garza") + ", Bagre: " + stock.get("Bagre"));
                      }
                  }
              ''',
              al_superar="La transferencia cortada se deshace y no se pierde ni una caja: 6 en la Garza, 4 en el Bagre. El Kraken suelta el tentáculo.",
              imagen=["Una caja volviendo sola al barco del que salió, mientras un tentáculo del Kraken se retira.",
                      "Kaffa con la taza en alto: «todo o nada»."]),
            m(id="S04-N02-P3", titulo="El servicio que el Kraken no rompe",
              lugar="La boca del Puerto", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Capas de punta a punta | controlador → servicio → repositorio · DTO en los bordes · validar y responder errores claros",
              recompensa="xp 25, oro 30",
              escena="""
                  El último ataque del Kraken es una lluvia de pedidos: buenos, vacíos y para barcos que no existen. El servicio de Zed tiene que responder **todos**, cada uno con su código.
              """,
              sugiere="El controlador recibe el pedido, el servicio valida y busca en el repositorio, y la respuesta es un texto con el código: 201 si se registró, 400 si el pedido es inválido, 404 si el barco no existe.",
              desafio="Completá el caso del barco que no existe: 404.",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.List;
                  import java.util.Map;

                  public class Kraken3 {
                      record CargaPedido(String barco, String descripcion) { }

                      static final Map<String, List<String>> REPO = Map.of("Garza", new ArrayList<>(), "Bagre", new ArrayList<>());

                      static String registrar(CargaPedido p) {
                          if (p.descripcion() == null || p.descripcion().isBlank()) {
                              return "400 la descripción es obligatoria";
                          }
                          List<String> bodega = REPO.get(p.barco());
                          if (bodega == null) {
                              return ___;
                          }
                          bodega.add(p.descripcion());
                          return "201 " + p.descripcion() + " a bordo del " + p.barco() + " (" + bodega.size() + ")";
                      }

                      public static void main(String[] args) {
                          List<CargaPedido> lluvia = List.of(new CargaPedido("Garza", "café"), new CargaPedido("Garza", " "),
                                  new CargaPedido("Ceibo", "vitral"), new CargaPedido("Bagre", "sal"));
                          lluvia.forEach(p -> System.out.println(registrar(p)));
                      }
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.List;
                  import java.util.Map;

                  public class Kraken3 {
                      record CargaPedido(String barco, String descripcion) { }

                      static final Map<String, List<String>> REPO = Map.of("Garza", new ArrayList<>(), "Bagre", new ArrayList<>());

                      static String registrar(CargaPedido p) {
                          if (p.descripcion() == null || p.descripcion().isBlank()) {
                              return "400 la descripción es obligatoria";
                          }
                          List<String> bodega = REPO.get(p.barco());
                          if (bodega == null) {
                              return "404 no existe el barco " + p.barco();
                          }
                          bodega.add(p.descripcion());
                          return "201 " + p.descripcion() + " a bordo del " + p.barco() + " (" + bodega.size() + ")";
                      }

                      public static void main(String[] args) {
                          List<CargaPedido> lluvia = List.of(new CargaPedido("Garza", "café"), new CargaPedido("Garza", " "),
                                  new CargaPedido("Ceibo", "vitral"), new CargaPedido("Bagre", "sal"));
                          lluvia.forEach(p -> System.out.println(registrar(p)));
                      }
                  }
              ''',
              al_superar="""
                  Cada pedido con su respuesta, y el servicio sigue en pie. El Kraken se hunde despacio en la boca del Puerto.
                  «404 no existe el barco Ceibo.» Zed sonríe: en el Puerto nadie sabe que el Ceibo está encallado en la Represa, con un vitral que ya está donde tenía que estar.
              """,
              imagen=["El Kraken hundiéndose en la boca del Puerto, con los tentáculos relajados.",
                      "Zed en el muelle de su Puerto natal, ahora construyendo; a lo lejos, la Torre del Arquitecto."]),
        ],
    },
]
