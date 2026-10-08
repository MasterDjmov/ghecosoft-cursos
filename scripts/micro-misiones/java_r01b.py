from genjava import m

# R01-N06 a N09: el cierre de la Aduana, el depósito, los libritos de los aduaneros y el Centinela.
# Cada nodo usa solo lo que ya se vio: N06 sin arrays, N07 sin métodos propios.

NODOS = [
    {
        "titulo": "R01-N06 · Bucles: while, do y for",
        "misiones": [
            m(id="R01-N06-P1", titulo="La Aduana trabada",
              lugar="El cierre de la Aduana", personajes="Zed, Gheco, Nadia",
              criatura="ogro",
              carta="while | while (condición) { … } · repite mientras se cumpla · adentro, algo tiene que cambiar o no termina nunca",
              recompensa="xp 10, oro 10",
              escena="""
                  Al cerrar la Aduana hay que contar los carros, uno por uno. Zed escribe su primer bucle, lo ejecuta… y el contador no para: «Carro 1, Carro 1, Carro 1». La Aduana queda trabada toda la noche y un **ogro** se sienta en la puerta a mirar.
                  —Tu bucle nunca cambia nada —dice Gheco—. Si `carro` vale siempre 1, la condición se cumple para siempre.
              """,
              sugiere="`while (carro <= 4) { … }` repite mientras la condición se cumpla. Adentro, algo tiene que acercarla a ser falsa: `carro++;` le suma 1 a `carro` en cada vuelta.",
              desafio="Completá la línea que falta para que el contador avance y el bucle termine.",
              inicial='''
                  public class Cierre {
                      public static void main(String[] args) {
                          int carro = 1;
                          while (carro <= 4) {
                              System.out.println("Carro " + carro + ": contado");
                              ___;
                          }
                          System.out.println("Aduana cerrada");
                      }
                  }
              ''',
              solucion='''
                  public class Cierre {
                      public static void main(String[] args) {
                          int carro = 1;
                          while (carro <= 4) {
                              System.out.println("Carro " + carro + ": contado");
                              carro++;
                          }
                          System.out.println("Aduana cerrada");
                      }
                  }
              ''',
              al_superar="Cuatro carros y la Aduana se cierra. El ogro bosteza y se va. Nadia, que pasó la noche despierta por el bucle de Zed, no dice nada: le alcanza con mirarlo.",
              imagen=["El portón de la Aduana de noche, trabado, con un contador de bronce que gira sin parar.",
                      "Un ogro sentado en la puerta, aburrido; Zed (pelo blanco plateado, visor rojo) agarrándose la cabeza.",
                      "Nadia (uniforme azul, rodete) con ojeras y los brazos cruzados."]),
            m(id="R01-N06-P2", titulo="La recaudación de la semana",
              lugar="La tesorería de la Aduana", personajes="Zed, Gheco, Nadia",
              carta="for y acumulador | for (int i = 1; i <= 5; i++) { total += …; } · el acumulador se declara ANTES del bucle",
              recompensa="xp 10, oro 10",
              escena="""
                  El tesorero quiere saber cuánto entró en la semana. Cada día se cobró diez denarios más que el anterior: 10, 20, 30… Zed se ofrece a sumarlo «de memoria» y Nadia le saca la pluma de la mano.
                  —Cuando sabés cuántas vueltas son, usá `for` —dice Gheco.
              """,
              sugiere="`for (int dia = 1; dia <= 5; dia++)` da exactamente 5 vueltas. Para sumar, un **acumulador**: `int total = 0;` antes del bucle y `total += …;` adentro.",
              desafio="Sumale al total lo que se cobró cada día (`dia * 10`).",
              inicial='''
                  public class Recaudacion {
                      public static void main(String[] args) {
                          int total = 0;
                          for (int dia = 1; dia <= 5; dia++) {
                              total ___ dia * 10;
                              System.out.println("Día " + dia + ": " + total);
                          }
                          System.out.println("Semana: " + total + " denarios");
                      }
                  }
              ''',
              solucion='''
                  public class Recaudacion {
                      public static void main(String[] args) {
                          int total = 0;
                          for (int dia = 1; dia <= 5; dia++) {
                              total += dia * 10;
                              System.out.println("Día " + dia + ": " + total);
                          }
                          System.out.println("Semana: " + total + " denarios");
                      }
                  }
              ''',
              al_superar="Ciento cincuenta denarios, día por día. El tesorero lo anota sin discutir. —Si lo hubieras sumado de memoria —dice Nadia—, hoy faltarían diez. —¿Y vos cómo sabés? —Porque te conozco.",
              imagen=["La tesorería de la Aduana: un mostrador con pilas de monedas que crecen día por día.",
                      "Nadia sacándole la pluma de la mano a Zed; Gheco en el mostrador."]),
            m(id="R01-N06-P3", titulo="El peso que no miente",
              lugar="La balanza de la Aduana", personajes="Zed, Gheco, Nadia",
              carta="do / while | do { … } while (condición); · da al menos una vuelta · sirve para volver a preguntar hasta que el dato sea válido",
              recompensa="xp 15, oro 15",
              escena="""
                  Un mercader apurado declara pesos imposibles para no pagar: −3 kg, 0 kg… Nadia suspira. —Preguntale otra vez. Y otra. Hasta que diga algo que tenga sentido.
              """,
              sugiere="`do { … } while (condición);` ejecuta el bloque **una vez** y después repite **mientras** la condición se cumpla. Para validar: repetí mientras el peso sea **inválido** (`peso <= 0`). Fijate el `;` del final.",
              desafio="Completá la condición: se vuelve a preguntar mientras el peso no sea mayor que cero.",
              entrada="-3\n0\n25",
              inicial='''
                  import java.util.Scanner;

                  public class Balanza {
                      public static void main(String[] args) {
                          Scanner sc = new Scanner(System.in);
                          int peso;
                          do {
                              System.out.println("Peso del carro:");
                              peso = sc.nextInt();
                          } while (___);
                          System.out.println("Aceptado: " + peso + " kg");
                      }
                  }
              ''',
              solucion='''
                  import java.util.Scanner;

                  public class Balanza {
                      public static void main(String[] args) {
                          Scanner sc = new Scanner(System.in);
                          int peso;
                          do {
                              System.out.println("Peso del carro:");
                              peso = sc.nextInt();
                          } while (peso <= 0);
                          System.out.println("Aceptado: " + peso + " kg");
                      }
                  }
              ''',
              al_superar="A la tercera, el mercader se rinde y declara 25 kg. —Con vos no se puede —le dice a Zed. Zed sonríe: hace una semana, el que mentía en la balanza era él.",
              imagen=["Una balanza de bronce gigante con un carro encima y la aguja en 25.",
                      "Un mercader de bigote, resignado; Zed sonriendo de costado y Nadia anotando."]),
            m(id="R01-N06-P4", titulo="Los sellos falsos",
              lugar="La fila de los carros", personajes="Zed, Gheco, Nadia",
              carta="break y continue | continue: saltea el resto de ESTA vuelta · break: corta el bucle entero",
              recompensa="xp 15, oro 15",
              escena="""
                  Último control del día. El carro 4 trae un sello falso: va al costado y se sigue con el próximo. Y cuando suena la campana del cierre, en el carro 7, no se revisa nada más.
                  —Hay dos formas de salir de una vuelta —dice Gheco—: saltearla o cortar todo.
              """,
              sugiere="Adentro de un bucle, `continue;` saltea lo que queda de **esta** vuelta y pasa a la siguiente; `break;` termina el bucle **entero**.",
              desafio="Completá las dos líneas: el carro 4 se saltea y en el 7 se corta todo.",
              inicial='''
                  public class Control {
                      public static void main(String[] args) {
                          for (int carro = 1; carro <= 10; carro++) {
                              if (carro == 4) {
                                  System.out.println("Carro 4: sello falso, al costado");
                                  ___;
                              }
                              if (carro == 7) {
                                  System.out.println("Carro 7: ¡campana del cierre!");
                                  ___;
                              }
                              System.out.println("Carro " + carro + ": pasa");
                          }
                      }
                  }
              ''',
              solucion='''
                  public class Control {
                      public static void main(String[] args) {
                          for (int carro = 1; carro <= 10; carro++) {
                              if (carro == 4) {
                                  System.out.println("Carro 4: sello falso, al costado");
                                  continue;
                              }
                              if (carro == 7) {
                                  System.out.println("Carro 7: ¡campana del cierre!");
                                  break;
                              }
                              System.out.println("Carro " + carro + ": pasa");
                          }
                      }
                  }
              ''',
              al_superar="""
                  El carro 4 queda al costado y la campana corta la fila justo a tiempo. Nadia cierra el portón con la llave grande.
                  —Mañana te toca el depósito —le dice a Zed—. Estantes numerados del cero al nueve. Y un mapa de la frontera, todo en cuadritos.
              """,
              imagen=["Una fila de carros: el cuarto apartado con un sello falso que se despega; una campana de bronce sonando sobre el séptimo.",
                      "Nadia cerrando el portón con una llave enorme; Zed mirando hacia el depósito."]),
        ],
    },
    {
        "titulo": "R01-N07 · Arrays y matrices",
        "misiones": [
            m(id="R01-N07-P1", titulo="Los estantes numerados",
              lugar="El depósito de la Aduana", personajes="Zed, Gheco, Nadia",
              carta="Array | String[] e = {\"sal\", \"seda\"}; · e[0] es el primero · e.length es cuántos hay · el último es e[e.length - 1]",
              recompensa="xp 10, oro 10",
              escena="""
                  El depósito es una fila de estantes numerados. Cada uno guarda un solo cajón y el depositario sabe dónde está cada cosa sin revolver.
                  —Empiezan en el **cero** —le avisa Nadia—. No en el uno. Todos se equivocan la primera vez.
              """,
              sugiere="Un **array** es una fila de lugares numerados desde 0. `estantes[0]` es el primero y `estantes.length` dice cuántos hay. Como empieza en 0, el **último** está en `estantes.length - 1`.",
              desafio="Mostrá el último estante usando `length`, sin escribir el número a mano.",
              inicial='''
                  public class Deposito {
                      public static void main(String[] args) {
                          String[] estantes = {"sal", "seda", "café", "especias", "vino"};
                          System.out.println("Estantes: " + estantes.length);
                          System.out.println("Primero: " + estantes[0]);
                          System.out.println("Último: " + estantes[___]);
                      }
                  }
              ''',
              solucion='''
                  public class Deposito {
                      public static void main(String[] args) {
                          String[] estantes = {"sal", "seda", "café", "especias", "vino"};
                          System.out.println("Estantes: " + estantes.length);
                          System.out.println("Primero: " + estantes[0]);
                          System.out.println("Último: " + estantes[estantes.length - 1]);
                      }
                  }
              ''',
              al_superar="El vino está donde decía el registro: en el estante 4, que es el quinto. —Del cero —repite Nadia—. Ya lo vas a soñar.",
              imagen=["Un depósito largo con estantes de madera numerados del 0 en adelante, cada uno con un cajón distinto (sal, seda, café, especias, vino).",
                      "Nadia señalando el cartel con el 0; Zed contando con los dedos."]),
            m(id="R01-N07-P2", titulo="El orco del último cajón",
              lugar="El depósito de la Aduana", personajes="Zed, Gheco, Nadia",
              criatura="orco",
              carta="Recorrer un array | for (int i = 0; i < a.length; i++) · con <, nunca <= · pedir a[a.length] da ArrayIndexOutOfBoundsException",
              recompensa="xp 15, oro 15",
              escena="""
                  Zed recorre los cajones para sumar lo que pesan. Al llegar al final, sigue de largo: pide un cajón que no existe y de la oscuridad sale un **orco** gritando *ArrayIndexOutOfBoundsException*.
                  —Pediste uno de más —dice Gheco, escondido detrás de Nadia.
              """,
              sugiere="Los índices van de `0` a `length - 1`. Si el bucle llega a `i <= pesos.length`, en la última vuelta pide `pesos[5]`, que no existe. La condición correcta es `i < pesos.length`.",
              desafio="Ejecutalo, mirá el error y arreglá la condición del `for`.",
              inicial='''
                  public class Pesos {
                      public static void main(String[] args) {
                          int[] pesos = {12, 30, 8, 25, 5};
                          int total = 0;
                          for (int i = 0; i <= pesos.length; i++) {
                              total += pesos[i];
                          }
                          System.out.println("Cajones: " + pesos.length);
                          System.out.println("Peso total: " + total + " kg");
                      }
                  }
              ''',
              solucion='''
                  public class Pesos {
                      public static void main(String[] args) {
                          int[] pesos = {12, 30, 8, 25, 5};
                          int total = 0;
                          for (int i = 0; i < pesos.length; i++) {
                              total += pesos[i];
                          }
                          System.out.println("Cajones: " + pesos.length);
                          System.out.println("Peso total: " + total + " kg");
                      }
                  }
              ''',
              al_superar="Con `<`, el bucle frena en el último cajón y el orco se queda sin nada que pedir. Se va arrastrando los pies. —Ese vuelve cada vez que alguien cuenta de más —dice Nadia.",
              imagen=["El fondo oscuro del depósito: después del último estante, un hueco del que sale un orco gritando.",
                      "Gheco escondido detrás de Nadia; Zed con un farol frente al orco."]),
            m(id="R01-N07-P3", titulo="El registro más viejo",
              lugar="El archivo del depósito", personajes="Zed, Gheco, Nadia",
              carta="La clase Arrays | Arrays.sort(a) ordena · Arrays.toString(a) lo muestra entero · import java.util.Arrays;",
              recompensa="xp 15, oro 15",
              escena="""
                  En el archivo del depósito hay registros de viajeros de todas las épocas, mezclados. Zed quiere encontrar el más viejo. Nadia se lo prohíbe… y después le alcanza la escalera.
              """,
              sugiere="`Arrays.sort(anios)` ordena el array de menor a mayor (lo cambia ahí mismo). `Arrays.toString(anios)` lo devuelve como texto: `[987, 1120, …]`. Hace falta `import java.util.Arrays;`.",
              desafio="Ordená los años para que el primero sea el más viejo.",
              inicial='''
                  import java.util.Arrays;

                  public class Archivo {
                      public static void main(String[] args) {
                          int[] anios = {1203, 987, 1450, 1120, 1333};
                          ___;
                          System.out.println(Arrays.toString(anios));
                          System.out.println("El más viejo: año " + anios[0]);
                      }
                  }
              ''',
              solucion='''
                  import java.util.Arrays;

                  public class Archivo {
                      public static void main(String[] args) {
                          int[] anios = {1203, 987, 1450, 1120, 1333};
                          Arrays.sort(anios);
                          System.out.println(Arrays.toString(anios));
                          System.out.println("El más viejo: año " + anios[0]);
                      }
                  }
              ''',
              al_superar="""
                  El registro del año 987 está en el último estante, cubierto de polvo. Un viajero sin nombre declaró una sola cosa: **«un vitral»**. Zed mira su llave de vidrios de colores y no dice nada.
                  Nadia sí lo nota. Anota algo en su libreta y la cierra rápido.
              """,
              imagen=["Un pergamino viejísimo bajo la luz de un farol: una sola línea escrita, «un vitral».",
                      "Zed en lo alto de una escalera, con la llave del vitral brillando en la mano.",
                      "Nadia abajo, cerrando su libreta."]),
            m(id="R01-N07-P4", titulo="El mapa de la frontera",
              lugar="La pared del depósito", personajes="Zed, Gheco, Nadia",
              carta="Matriz | int[][] m = {{0, 1}, {1, 0}}; · m[fila][columna] · m.length filas · m[f].length columnas · dos for, uno adentro del otro",
              recompensa="xp 15, oro 15",
              escena="""
                  Colgado en la pared del depósito hay un mapa de la frontera en cuadritos. Donde hay una torre de vigilancia, un 1; donde no, un 0. Nadia quiere saber dónde están todas.
              """,
              sugiere="Una **matriz** es un array de filas. `mapa.length` es la cantidad de filas y `mapa[f].length` las columnas de la fila `f`. Se recorre con dos `for`: el de afuera por filas y el de adentro por columnas.",
              desafio="Completá el límite del `for` de adentro: las columnas de esa fila.",
              inicial='''
                  public class Mapa {
                      public static void main(String[] args) {
                          int[][] mapa = {
                              {0, 1, 0, 0},
                              {0, 0, 0, 1},
                              {1, 0, 0, 0}
                          };
                          int torres = 0;
                          for (int f = 0; f < mapa.length; f++) {
                              for (int c = 0; c < ___; c++) {
                                  if (mapa[f][c] == 1) {
                                      System.out.println("Torre en fila " + f + ", columna " + c);
                                      torres++;
                                  }
                              }
                          }
                          System.out.println("Torres: " + torres);
                      }
                  }
              ''',
              solucion='''
                  public class Mapa {
                      public static void main(String[] args) {
                          int[][] mapa = {
                              {0, 1, 0, 0},
                              {0, 0, 0, 1},
                              {1, 0, 0, 0}
                          };
                          int torres = 0;
                          for (int f = 0; f < mapa.length; f++) {
                              for (int c = 0; c < mapa[f].length; c++) {
                                  if (mapa[f][c] == 1) {
                                      System.out.println("Torre en fila " + f + ", columna " + c);
                                      torres++;
                                  }
                              }
                          }
                          System.out.println("Torres: " + torres);
                      }
                  }
              ''',
              al_superar="""
                  Tres torres, cada una en su cuadrito. Nadia las marca con alfileres. Al lado del mapa cuelga el reglamento de la Aduana: mil páginas.
                  —¿Alguien lo leyó entero? —pregunta Zed. —Nadie —dice Nadia—. Cada aduanero tiene su librito.
              """,
              imagen=["Un mapa de la frontera en cuadrícula colgado en la pared, con tres torres marcadas con alfileres rojos.",
                      "Al lado, un reglamento gordísimo colgado de un clavo; Zed lo mira con espanto."]),
        ],
    },
    {
        "titulo": "R01-N08 · Métodos: dividir el trabajo",
        "misiones": [
            m(id="R01-N08-P1", titulo="El librito del pesador",
              lugar="Los pasillos de los aduaneros", personajes="Zed, Gheco, Nadia",
              carta="Método con return | static double peaje(int kg) { return kg * 0.5; } · recibe datos, devuelve un resultado · se llama por su nombre",
              recompensa="xp 10, oro 10",
              escena="""
                  En los pasillos de la Aduana, cada aduanero tiene su librito: uno pesa, otro cobra, otro sella. El pesador le muestra a Zed el suyo: una sola regla, «medio denario por kilo».
                  —Un **método** es eso —dice Gheco—: un librito con nombre. Le das los datos y te devuelve la respuesta.
              """,
              sugiere="`static double peaje(int kg) { … }` declara un método que recibe un `int` y **devuelve** un `double`. Adentro, `return …;` dice qué devuelve. En `main` se usa como un valor: `peaje(10)`.",
              desafio="Escribí el `return` del método: medio denario por kilo.",
              inicial='''
                  public class Pesador {
                      static double peaje(int kg) {
                          ___;
                      }

                      public static void main(String[] args) {
                          System.out.println("10 kg: " + peaje(10));
                          System.out.println("40 kg: " + peaje(40));
                          System.out.println("Los dos: " + (peaje(10) + peaje(40)));
                      }
                  }
              ''',
              solucion='''
                  public class Pesador {
                      static double peaje(int kg) {
                          return kg * 0.5;
                      }

                      public static void main(String[] args) {
                          System.out.println("10 kg: " + peaje(10));
                          System.out.println("40 kg: " + peaje(40));
                          System.out.println("Los dos: " + (peaje(10) + peaje(40)));
                      }
                  }
              ''',
              al_superar="El pesador asiente: el librito de Zed dice lo mismo que el suyo. —Cuando cambie la tarifa —le explica—, cambio una sola línea y todos los carros pagan lo nuevo.",
              imagen=["Un pasillo de la Aduana con puertitas; en cada una, un aduanero con un librito distinto.",
                      "El pesador, viejo y de delantal, mostrándole a Zed un librito con una sola regla."]),
            m(id="R01-N08-P2", titulo="El librito del sellador",
              lugar="Los pasillos de los aduaneros", personajes="Zed, Gheco, Nadia",
              carta="Parámetros y tipo de retorno | static String sello(String nombre, boolean declarado) · varios parámetros separados por coma · void si no devuelve nada",
              recompensa="xp 10, oro 10",
              escena="""
                  El sellador decide entre dos sellos: APROBADO si el viajero declaró todo, RETENIDO si no. Nadia le pide a Zed que escriba ese librito. —Y que devuelva el texto del sello, no que lo muestre: lo usa otro aduanero.
              """,
              sugiere="Antes del nombre del método va el **tipo de lo que devuelve**: `String` si devuelve un texto, `int` si un número, `void` si no devuelve nada. Los parámetros van entre paréntesis, separados por coma.",
              desafio="Completá el tipo de retorno del método.",
              inicial='''
                  public class Sellador {
                      static ___ sello(String nombre, boolean declarado) {
                          if (declarado) {
                              return "APROBADO: " + nombre;
                          }
                          return "RETENIDO: " + nombre;
                      }

                      public static void main(String[] args) {
                          System.out.println(sello("Nadia", true));
                          System.out.println(sello("un tahúr", false));
                          String deZed = sello("Zed", true);
                          System.out.println(deZed.toLowerCase());
                      }
                  }
              ''',
              solucion='''
                  public class Sellador {
                      static String sello(String nombre, boolean declarado) {
                          if (declarado) {
                              return "APROBADO: " + nombre;
                          }
                          return "RETENIDO: " + nombre;
                      }

                      public static void main(String[] args) {
                          System.out.println(sello("Nadia", true));
                          System.out.println(sello("un tahúr", false));
                          String deZed = sello("Zed", true);
                          System.out.println(deZed.toLowerCase());
                      }
                  }
              ''',
              al_superar="«aprobado: zed», en minúsculas, como un susurro. Zed se queda mirándolo. Es la primera vez que un papel dice que él puede estar acá.",
              imagen=["Dos sellos de bronce sobre un escritorio: APROBADO en dorado y RETENIDO en rojo.",
                      "Zed mirando un papel sellado con su nombre; Nadia lo observa de reojo."]),
            m(id="R01-N08-P3", titulo="Dos formas de cobrar",
              lugar="La ventanilla del cobrador", personajes="Zed, Gheco, Nadia",
              carta="Sobrecarga | mismo nombre, distintos parámetros · cobrar(int kg) y cobrar(int kg, int carros) · Java elige por lo que le pasás",
              recompensa="xp 15, oro 15",
              escena="""
                  El cobrador tiene dos tarifas con el mismo nombre: «cobrar». Si viene un carro solo, 2 denarios por kilo. Si vienen varios carros con la misma carga, se cobra por cada uno y se descuenta 5 por carro.
                  —¿Dos libritos con el mismo nombre? —pregunta Zed. —Mientras reciban cosas distintas, Java sabe cuál abrir —dice Gheco.
              """,
              sugiere="**Sobrecarga**: dos métodos con el mismo nombre y distintos parámetros. `cobrar(30)` usa el de un parámetro y `cobrar(30, 3)` el de dos. Uno puede llamar al otro: `cobrar(kg) * carros`.",
              desafio="Completá el `return` del segundo `cobrar`: lo de un carro por la cantidad de carros, menos 5 por carro.",
              inicial='''
                  public class Cobrador {
                      static int cobrar(int kg) {
                          return kg * 2;
                      }

                      static int cobrar(int kg, int carros) {
                          return ___;
                      }

                      public static void main(String[] args) {
                          System.out.println("Un carro de 30 kg: " + cobrar(30));
                          System.out.println("Tres carros de 30 kg: " + cobrar(30, 3));
                      }
                  }
              ''',
              solucion='''
                  public class Cobrador {
                      static int cobrar(int kg) {
                          return kg * 2;
                      }

                      static int cobrar(int kg, int carros) {
                          return cobrar(kg) * carros - 5 * carros;
                      }

                      public static void main(String[] args) {
                          System.out.println("Un carro de 30 kg: " + cobrar(30));
                          System.out.println("Tres carros de 30 kg: " + cobrar(30, 3));
                      }
                  }
              ''',
              al_superar="El cobrador cobra 60 y 165 sin pensar. —El segundo librito usa el primero —le explica Gheco a Zed—: si cambia la tarifa por kilo, cambian los dos.",
              imagen=["Una ventanilla con dos libritos de tapa igual, «cobrar», uno fino y uno más grueso.",
                      "Una fila de tres carros iguales esperando; el cobrador contando monedas."]),
            m(id="R01-N08-P4", titulo="La escalera sin fin",
              lugar="La escalera al último pasillo", personajes="Zed, Gheco, Nadia",
              criatura="esqueleto",
              carta="Recursión | un método que se llama a sí mismo · necesita un caso base que corte · sin él: StackOverflowError",
              recompensa="xp 15, oro 15",
              escena="""
                  Para llegar al último pasillo hay una escalera de caracol. Zed escribe un librito para bajar escalón por escalón: «bajar un escalón y volver a bajar». Nunca llega abajo. Al fondo, un **esqueleto** que intentó lo mismo hace siglos todavía está bajando.
              """,
              sugiere="Un método **recursivo** se llama a sí mismo con un problema más chico: `bajar(n - 1)`. Necesita un **caso base** que corte sin volver a llamarse: cuando `n == 0`, ya llegaste. Sin él, se llena la pila y aparece `StackOverflowError`.",
              desafio="Completá la condición del caso base: cuando no quedan escalones.",
              inicial='''
                  public class Escalera {
                      static void bajar(int escalones) {
                          if (___) {
                              System.out.println("¡Abajo! Ahí está el último pasillo.");
                              return;
                          }
                          System.out.println("Faltan " + escalones);
                          bajar(escalones - 1);
                      }

                      public static void main(String[] args) {
                          bajar(4);
                      }
                  }
              ''',
              solucion='''
                  public class Escalera {
                      static void bajar(int escalones) {
                          if (escalones == 0) {
                              System.out.println("¡Abajo! Ahí está el último pasillo.");
                              return;
                          }
                          System.out.println("Faltan " + escalones);
                          bajar(escalones - 1);
                      }

                      public static void main(String[] args) {
                          bajar(4);
                      }
                  }
              ''',
              al_superar="""
                  Cuatro escalones y abajo. El esqueleto, que seguía bajando, se detiene y se sienta, aliviado.
                  Al final del último pasillo, sobre un trono de piedra, una armadura vacía sostiene un libro de registros. Gheco baja la voz: —El **Centinela**.
              """,
              imagen=["Una escalera de caracol de piedra que baja en espiral; un esqueleto sentado en un escalón, aliviado.",
                      "Al fondo, la silueta de una armadura sentada en un trono de piedra, con un libro abierto en las rodillas.",
                      "Gheco, el gecko cian, escondido en el hombro de Zed."]),
        ],
    },
    {
        "titulo": "R01-N09 · Jefe: el Centinela de la Aduana",
        "misiones": [
            m(id="R01-N09-P1", titulo="La primera pregunta del Centinela",
              lugar="El trono del Centinela", personajes="Zed, Gheco, Nadia, Kaffa, el Centinela",
              carta="Leer un dato válido | static int leerEntero(Scanner sc, int min, int max) · repite hasta que esté en el rango · un solo Scanner, pasado como parámetro",
              recompensa="xp 20, oro 20",
              escena="""
                  La armadura levanta la cabeza. Su voz suena a hierro: —**Cuántos días te quedás en el Imperio.** Entre 1 y 30. —Zed contesta «0», por probar. Después «45». La armadura no se mueve: vuelve a preguntar.
                  Kaffa aparece a su lado, con una taza de café. —No se lo engaña, Zed. Se lo vence con **orden**: un librito para cada cosa. Empezá por uno que lea un número válido.
              """,
              sugiere="Un método `leerEntero(sc, min, max)` encierra el bucle de validación: pregunta, lee y repite **mientras** el número esté fuera del rango (`n < min || n > max`). Así se escribe una vez y se usa en todo el programa.",
              desafio="Completá la condición del `while`: se repite mientras el número esté fuera del rango.",
              entrada="0\n45\n12",
              inicial='''
                  import java.util.Scanner;

                  public class Centinela {
                      static int leerEntero(Scanner sc, int min, int max) {
                          System.out.println("Entre " + min + " y " + max + ":");
                          int n = sc.nextInt();
                          while (___) {
                              System.out.println("Fuera de rango. Otra vez:");
                              n = sc.nextInt();
                          }
                          return n;
                      }

                      public static void main(String[] args) {
                          Scanner sc = new Scanner(System.in);
                          int dias = leerEntero(sc, 1, 30);
                          System.out.println("Registrado: " + dias + " días");
                      }
                  }
              ''',
              solucion='''
                  import java.util.Scanner;

                  public class Centinela {
                      static int leerEntero(Scanner sc, int min, int max) {
                          System.out.println("Entre " + min + " y " + max + ":");
                          int n = sc.nextInt();
                          while (n < min || n > max) {
                              System.out.println("Fuera de rango. Otra vez:");
                              n = sc.nextInt();
                          }
                          return n;
                      }

                      public static void main(String[] args) {
                          Scanner sc = new Scanner(System.in);
                          int dias = leerEntero(sc, 1, 30);
                          System.out.println("Registrado: " + dias + " días");
                      }
                  }
              ''',
              al_superar="«Doce días.» La armadura escribe en su libro, con una pluma que se mueve sola. Primera pregunta, superada. El libro pasa la página.",
              imagen=["El Centinela: una armadura vacía de piedra y bronce sentada en un trono, con ojos de luz azul y un libro de registros abierto.",
                      "Zed frente al trono; Kaffa a su lado con una taza de café; Nadia y Gheco atrás."]),
            m(id="R01-N09-P2", titulo="Los registros del Centinela",
              lugar="El trono del Centinela", personajes="Zed, Gheco, Nadia, el Centinela",
              carta="Métodos con arrays | static double promedio(int[] datos) · el array entra por parámetro · recorrer, acumular y dividir",
              recompensa="xp 20, oro 20",
              escena="""
                  —**Cuánto pesó, en promedio, lo que entró esta semana** —pregunta el Centinela, y del libro caen siete números. Zed empieza a sumar con los dedos. Nadia lo frena: —Un librito. Que reciba los pesos y devuelva el promedio.
              """,
              sugiere="Un método puede recibir un **array**: `static double promedio(int[] datos)`. Adentro, recorrelo con un acumulador y devolvé `total / (double) datos.length` (el `(double)` evita que la división sea entera).",
              desafio="Completá el `return`: el total dividido por la cantidad, con decimales.",
              inicial='''
                  import java.util.Locale;

                  public class Registros {
                      static double promedio(int[] datos) {
                          int total = 0;
                          for (int dato : datos) {
                              total += dato;
                          }
                          return ___;
                      }

                      public static void main(String[] args) {
                          int[] semana = {120, 80, 95, 60, 130, 75, 110};
                          System.out.printf(Locale.US, "Promedio: %.2f kg%n", promedio(semana));
                      }
                  }
              ''',
              solucion='''
                  import java.util.Locale;

                  public class Registros {
                      static double promedio(int[] datos) {
                          int total = 0;
                          for (int dato : datos) {
                              total += dato;
                          }
                          return total / (double) datos.length;
                      }

                      public static void main(String[] args) {
                          int[] semana = {120, 80, 95, 60, 130, 75, 110};
                          System.out.printf(Locale.US, "Promedio: %.2f kg%n", promedio(semana));
                      }
                  }
              ''',
              al_superar="«95.71 kilos.» El Centinela lo comprueba en su libro. Exacto, con dos decimales. Una placa de su armadura se apaga.",
              imagen=["Siete números de luz cayendo de un libro abierto y acomodándose en una fila.",
                      "Una placa de la armadura del Centinela que se apaga; Zed concentrado."]),
            m(id="R01-N09-P3", titulo="El veredicto",
              lugar="El trono del Centinela", personajes="Zed, Gheco, Nadia, el Centinela",
              carta="Partir el problema | un método por tarea · main solo los junta · arrays paralelos: el mismo índice en dos arrays es el mismo viajero",
              recompensa="xp 20, oro 25",
              escena="""
                  —**Decidí por mí** —dice el Centinela, y le muestra la fila de viajeros de hoy: sus nombres en un registro y lo que cargan en otro—. Más de 100 kg, inspección. Si no, pasa.
                  Zed entiende el truco: el mismo número de renglón en los dos registros es el mismo viajero.
              """,
              sugiere="Con **arrays paralelos**, `nombres[i]` y `cargas[i]` son del mismo viajero. El veredicto va en su propio método; en el bucle de `main`, solo hay que **llamarlo** con la carga de ese viajero: `veredicto(cargas[i])`.",
              desafio="Completá la llamada al método `veredicto` con la carga del viajero `i`.",
              inicial='''
                  public class Veredicto {
                      static String veredicto(int kg) {
                          if (kg > 100) {
                              return "inspección";
                          }
                          return "pasa";
                      }

                      public static void main(String[] args) {
                          String[] nombres = {"Baldo", "un tahúr", "la cocinera", "un soldado"};
                          int[] cargas = {140, 20, 60, 101};
                          for (int i = 0; i < nombres.length; i++) {
                              System.out.println(nombres[i] + ": " + ___);
                          }
                      }
                  }
              ''',
              solucion='''
                  public class Veredicto {
                      static String veredicto(int kg) {
                          if (kg > 100) {
                              return "inspección";
                          }
                          return "pasa";
                      }

                      public static void main(String[] args) {
                          String[] nombres = {"Baldo", "un tahúr", "la cocinera", "un soldado"};
                          int[] cargas = {140, 20, 60, 101};
                          for (int i = 0; i < nombres.length; i++) {
                              System.out.println(nombres[i] + ": " + veredicto(cargas[i]));
                          }
                      }
                  }
              ''',
              al_superar="Baldo, a inspección (como siempre). El soldado, por un kilo. El Centinela cierra el libro despacio. Queda una sola pregunta, y es sobre Zed.",
              imagen=["Dos registros abiertos lado a lado, unidos renglón por renglón con hilos de luz.",
                      "Baldo, el mercader ambulante, resignado frente al cartel de «inspección»."]),
            m(id="R01-N09-P4", titulo="El Sello de Entrada",
              lugar="El trono del Centinela", personajes="Zed, Gheco, Nadia, Kaffa, el Centinela",
              carta="Un programa entero | leer, decidir, repetir y resumir · cada parte en su método · main cuenta la historia",
              recompensa="xp 25, oro 30",
              item="Sello de Entrada",
              escena="""
                  —**Declarate** —dice el Centinela—. Todo lo que traés. Uno por uno. Y decime cuánto es.
                  Zed abre la bolsa. Hace una semana se hubiera guardado algo. Esta vez saca todo: la ganzúa, la capa, la llave de vidrio.
              """,
              sugiere="Un programa completo se arma con los libritos que ya tenés: uno lee la cantidad, el bucle lee cada cosa y un acumulador suma el valor. `sc.next()` lee una palabra y `sc.nextInt()` un número.",
              desafio="Completá el acumulador: sumá el valor de cada cosa al total.",
              entrada="3\nganzua 15\ncapa 40\nllave 0",
              inicial='''
                  import java.util.Scanner;

                  public class Declaracion {
                      static String resumen(int cosas, int total) {
                          return cosas + " cosas declaradas, valor total " + total + " denarios";
                      }

                      public static void main(String[] args) {
                          Scanner sc = new Scanner(System.in);
                          int cantidad = sc.nextInt();
                          int total = 0;
                          for (int i = 1; i <= cantidad; i++) {
                              String cosa = sc.next();
                              int valor = sc.nextInt();
                              System.out.println(i + ". " + cosa + ": " + valor);
                              ___;
                          }
                          System.out.println(resumen(cantidad, total));
                      }
                  }
              ''',
              solucion='''
                  import java.util.Scanner;

                  public class Declaracion {
                      static String resumen(int cosas, int total) {
                          return cosas + " cosas declaradas, valor total " + total + " denarios";
                      }

                      public static void main(String[] args) {
                          Scanner sc = new Scanner(System.in);
                          int cantidad = sc.nextInt();
                          int total = 0;
                          for (int i = 1; i <= cantidad; i++) {
                              String cosa = sc.next();
                              int valor = sc.nextInt();
                              System.out.println(i + ". " + cosa + ": " + valor);
                              total += valor;
                          }
                          System.out.println(resumen(cantidad, total));
                      }
                  }
              ''',
              al_superar="""
                  «Llave: 0 denarios.» El Centinela se queda mirando ese renglón mucho tiempo. Después se levanta, se hace a un lado y le entrega a Zed un sello de bronce: el **Sello de Entrada**. Ya no es un colado: está declarado.
                  Esa noche, la ganzúa de Zed amanece un poco distinta, como si quisiera ser otra cosa. Kaffa termina su café. —Ahora aprendé a hacer **moldes**.
              """,
              imagen=["El Centinela de pie, haciéndose a un lado del trono, entregándole a Zed un sello de bronce que brilla.",
                      "Sobre una mesa, lo que Zed declaró: una ganzúa, una capa gastada y la llave de plomo y vidrios de colores.",
                      "Kaffa con su taza de café; Nadia sonriendo apenas, por primera vez."]),
        ],
    },
]
