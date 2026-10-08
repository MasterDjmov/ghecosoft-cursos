from genjava import m

# R02-N01 a N05: la Academia de los Moldes. En el modo de un solo archivo (`java Archivo.java`) la clase con el
# main va PRIMERO; las demás, sin public, debajo. Cada nodo usa solo lo que ya se enseñó.

NODOS = [
    {
        "titulo": "R02-N01 · Clases y objetos",
        "misiones": [
            m(id="R02-N01-P1", titulo="El primer molde",
              lugar="Los talleres de la Academia de los Moldes", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="Clase y objeto | class Viajero { String nombre; } es el molde · new Viajero() crea un objeto · v.nombre = \"Zed\"; le da un dato",
              recompensa="xp 10, oro 10",
              escena="""
                  Con el Sello de Entrada en el bolsillo, Zed llega a la **Academia de los Moldes**. La **Maestra de Moldes**, con el delantal lleno de virutas de bronce, le señala tres arrays sueltos en su pizarra: nombres, edades y oficios. —Así guardabas a tus viajeros. Desde hoy, cada viajero sale de un **molde**.
              """,
              sugiere="Una **clase** es el molde: dice qué datos tiene cada objeto (`String nombre; int edad;`). `new Viajero()` crea un **objeto** nuevo de ese molde, y con el punto le cargás sus datos: `v.nombre = \"Zed\";`.",
              desafio="Creá el objeto con `new`.",
              inicial='''
                  public class Molde {
                      public static void main(String[] args) {
                          Viajero v = ___;
                          v.nombre = "Zed";
                          v.edad = 19;
                          v.oficio = "ladrón retirado";
                          System.out.println(v.nombre + ", " + v.edad + " años, " + v.oficio);
                      }
                  }

                  class Viajero {
                      String nombre;
                      int edad;
                      String oficio;
                  }
              ''',
              solucion='''
                  public class Molde {
                      public static void main(String[] args) {
                          Viajero v = new Viajero();
                          v.nombre = "Zed";
                          v.edad = 19;
                          v.oficio = "ladrón retirado";
                          System.out.println(v.nombre + ", " + v.edad + " años, " + v.oficio);
                      }
                  }

                  class Viajero {
                      String nombre;
                      int edad;
                      String oficio;
                  }
              ''',
              al_superar="—«Retirado» —lee Nadia, y levanta una ceja. —Desde la semana pasada —dice Zed. La Maestra se ríe: es el primer viajero que sale entero de un molde, con todos sus datos juntos.",
              imagen=["Un taller enorme de la Academia de los Moldes, con moldes de bronce colgando del techo.",
                      "La Maestra de Moldes (delantal con virutas de bronce) señalando una pizarra con tres arrays tachados.",
                      "Zed (pelo blanco plateado, visor rojo) frente a un molde con forma de persona; Nadia y Gheco a su lado."]),
            m(id="R02-N01-P2", titulo="Un molde, muchos viajeros",
              lugar="Los talleres de la Academia de los Moldes", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="Cada objeto es otro | dos new = dos objetos · cada uno con sus propios datos · cambiar uno no cambia el otro",
              recompensa="xp 10, oro 10",
              escena="""
                  —Si cambio el nombre de este viajero —pregunta Zed—, ¿se cambia el de todos los que salieron del molde? La Maestra le pone dos viajeros enfrente. —Probalo.
              """,
              sugiere="Cada `new` fabrica un objeto **distinto**, con su propia copia de los atributos. `a.nombre` y `b.nombre` son dos cajones diferentes.",
              desafio="Creá el segundo viajero, `b`, con su propio `new`.",
              inicial='''
                  public class DosViajeros {
                      public static void main(String[] args) {
                          Viajero a = new Viajero();
                          Viajero b = ___;
                          a.nombre = "Zed";
                          b.nombre = "Nadia";
                          a.nombre = "Zed del Puerto";
                          System.out.println("a: " + a.nombre);
                          System.out.println("b: " + b.nombre);
                      }
                  }

                  class Viajero {
                      String nombre;
                  }
              ''',
              solucion='''
                  public class DosViajeros {
                      public static void main(String[] args) {
                          Viajero a = new Viajero();
                          Viajero b = new Viajero();
                          a.nombre = "Zed";
                          b.nombre = "Nadia";
                          a.nombre = "Zed del Puerto";
                          System.out.println("a: " + a.nombre);
                          System.out.println("b: " + b.nombre);
                      }
                  }

                  class Viajero {
                      String nombre;
                  }
              ''',
              al_superar="Zed cambió su nombre y el de Nadia siguió igual. —Por suerte —dice ella—. No quiero llamarme «del Puerto».",
              imagen=["Dos figuras recién salidas del mismo molde de bronce, cada una con una etiqueta distinta: «Zed del Puerto» y «Nadia».",
                      "Nadia cruzada de brazos; Zed sonriendo."]),
            m(id="R02-N01-P3", titulo="El molde que sabe hacer cosas",
              lugar="Los talleres de la Academia de los Moldes", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="Método de instancia | String saludo() { return \"Soy \" + nombre; } · usa los datos de SU objeto · v.saludo()",
              recompensa="xp 15, oro 15",
              escena="""
                  —Un molde no guarda solo datos —dice la Maestra—. También sabe **hacer** cosas. Cada viajero sabe presentarse, y se presenta con **su** nombre.
              """,
              sugiere="Un método **sin `static`** pertenece a cada objeto: adentro, `nombre` es el nombre de **ese** objeto. Se llama con el punto: `zed.saludo()`.",
              desafio="Completá el `return` del método `saludo`: «Soy <nombre>. Origen: <origen>».",
              inicial='''
                  public class Presentacion {
                      public static void main(String[] args) {
                          Viajero zed = new Viajero();
                          zed.nombre = "Zed";
                          zed.origen = "el Puerto";
                          Viajero nadia = new Viajero();
                          nadia.nombre = "Nadia";
                          nadia.origen = "la Aduana";
                          System.out.println(zed.saludo());
                          System.out.println(nadia.saludo());
                      }
                  }

                  class Viajero {
                      String nombre;
                      String origen;

                      String saludo() {
                          return ___;
                      }
                  }
              ''',
              solucion='''
                  public class Presentacion {
                      public static void main(String[] args) {
                          Viajero zed = new Viajero();
                          zed.nombre = "Zed";
                          zed.origen = "el Puerto";
                          Viajero nadia = new Viajero();
                          nadia.nombre = "Nadia";
                          nadia.origen = "la Aduana";
                          System.out.println(zed.saludo());
                          System.out.println(nadia.saludo());
                      }
                  }

                  class Viajero {
                      String nombre;
                      String origen;

                      String saludo() {
                          return "Soy " + nombre + ". Origen: " + origen;
                      }
                  }
              ''',
              al_superar="Un solo método y cada uno se presenta a su manera. —Es como los libritos de la Aduana —dice Zed—, pero cada viajero lleva el suyo en el bolsillo.",
              imagen=["Dos figuras de bronce con globos de diálogo distintos que salen del mismo libro abierto.",
                      "La Maestra de Moldes asintiendo; Gheco anotando en el aire con una pluma de luz."]),
            m(id="R02-N01-P4", titulo="El fantasma del molde",
              lugar="Los talleres de la Academia de los Moldes", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              criatura="esqueleto",
              carta="toString | public String toString() { return …; } · lo que se muestra al imprimir el objeto · sin él: Clase@1b6d3586",
              recompensa="xp 15, oro 15",
              escena="""
                  Zed imprime a su viajero directamente y en la consola aparece algo como `Viajero@1b6d3586`. Del molde sale un **esqueleto** que repite ese código como un nombre sin cuerpo.
                  —Java no sabe cómo querés que se vea tu objeto —dice Gheco—. Decíselo.
              """,
              sugiere="Al imprimir un objeto, Java llama a su método `toString()`. Si no lo escribiste, muestra la clase y un código raro. Escribilo vos: `public String toString() { return …; }`.",
              desafio="Completá el nombre del método para que `println(v)` muestre al viajero.",
              inicial='''
                  public class Fantasma {
                      public static void main(String[] args) {
                          Viajero v = new Viajero();
                          v.nombre = "Zed";
                          v.edad = 19;
                          System.out.println(v);
                      }
                  }

                  class Viajero {
                      String nombre;
                      int edad;

                      public String ___() {
                          return "Viajero[" + nombre + ", " + edad + "]";
                      }
                  }
              ''',
              solucion='''
                  public class Fantasma {
                      public static void main(String[] args) {
                          Viajero v = new Viajero();
                          v.nombre = "Zed";
                          v.edad = 19;
                          System.out.println(v);
                      }
                  }

                  class Viajero {
                      String nombre;
                      int edad;

                      public String toString() {
                          return "Viajero[" + nombre + ", " + edad + "]";
                      }
                  }
              ''',
              al_superar="«Viajero[Zed, 19]». El esqueleto se mira las manos, encuentra un nombre y se desarma tranquilo. Al lado, un soldado sale de un molde… sin espada.",
              imagen=["Un esqueleto con una etiqueta «Viajero@1b6d3586» desarmándose en paz.",
                      "Al fondo, un soldado de bronce recién salido de un molde, con la mano vacía donde debería ir la espada."]),
        ],
    },
    {
        "titulo": "R02-N02 · Constructores, this y sobrecarga",
        "misiones": [
            m(id="R02-N02-P1", titulo="La palanca del molde",
              lugar="El taller de los soldados", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="Constructor | Soldado(String nombre, String arma) { … } · se llama como la clase y no devuelve nada · new Soldado(\"Lía\", \"espada\")",
              recompensa="xp 10, oro 10",
              escena="""
                  Un aprendiz arma soldados a mano: primero el cuerpo, después el casco, después el nombre… y a la mitad se olvida la espada. La Maestra aprieta una palanca y el soldado sale **completo**. —Esa palanca es el **constructor**.
              """,
              sugiere="Un **constructor** se llama igual que la clase y no tiene tipo de retorno. Recibe los datos y los guarda en el objeto: `this.arma = arma;` (`this.arma` es el atributo; `arma`, el parámetro).",
              desafio="Completá la línea que guarda el arma en el objeto.",
              inicial='''
                  public class Palanca {
                      public static void main(String[] args) {
                          Soldado a = new Soldado("Lía", "espada");
                          Soldado b = new Soldado("Teo", "lanza");
                          System.out.println(a.nombre + " con " + a.arma);
                          System.out.println(b.nombre + " con " + b.arma);
                      }
                  }

                  class Soldado {
                      String nombre;
                      String arma;

                      Soldado(String nombre, String arma) {
                          this.nombre = nombre;
                          ___;
                      }
                  }
              ''',
              solucion='''
                  public class Palanca {
                      public static void main(String[] args) {
                          Soldado a = new Soldado("Lía", "espada");
                          Soldado b = new Soldado("Teo", "lanza");
                          System.out.println(a.nombre + " con " + a.arma);
                          System.out.println(b.nombre + " con " + b.arma);
                      }
                  }

                  class Soldado {
                      String nombre;
                      String arma;

                      Soldado(String nombre, String arma) {
                          this.nombre = nombre;
                          this.arma = arma;
                      }
                  }
              ''',
              al_superar="Los dos soldados salen armados. El aprendiz mira la palanca como si fuera magia. —No es magia —le dice Zed—. Es que el molde no te deja olvidarte.",
              imagen=["Una palanca de bronce bajando y un soldado completo saliendo del molde con su espada.",
                      "Un aprendiz con las piezas de un soldado desparramadas en la mesa, sorprendido."]),
            m(id="R02-N02-P2", titulo="Los soldados de nadie",
              lugar="El taller de los soldados", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              criatura="troll",
              carta="this | si el parámetro se llama igual que el atributo, nombre = nombre; no guarda nada · this.nombre = nombre; sí",
              recompensa="xp 15, oro 15",
              escena="""
                  El aprendiz escribió su propio constructor. Compila, corre… y todos los soldados salen llamándose `null`. Un **troll** asoma detrás de los moldes, encantado.
              """,
              sugiere="Adentro del constructor, `nombre` es el **parámetro**. `nombre = nombre;` lo copia sobre sí mismo y el atributo queda en `null`. Para hablar del atributo del objeto se usa `this.nombre`.",
              desafio="Ejecutalo, mirá los `null` y arreglá las dos asignaciones con `this`.",
              inicial='''
                  public class Nadie {
                      public static void main(String[] args) {
                          Soldado s = new Soldado("Lía", "arco");
                          System.out.println(s.nombre + " con " + s.arma);
                      }
                  }

                  class Soldado {
                      String nombre;
                      String arma;

                      Soldado(String nombre, String arma) {
                          nombre = nombre;
                          arma = arma;
                      }
                  }
              ''',
              solucion='''
                  public class Nadie {
                      public static void main(String[] args) {
                          Soldado s = new Soldado("Lía", "arco");
                          System.out.println(s.nombre + " con " + s.arma);
                      }
                  }

                  class Soldado {
                      String nombre;
                      String arma;

                      Soldado(String nombre, String arma) {
                          this.nombre = nombre;
                          this.arma = arma;
                      }
                  }
              ''',
              al_superar="«Lía con arco.» El troll se esconde de nuevo, decepcionado: sin `null`, no tiene de qué alimentarse.",
              imagen=["Una fila de soldados de bronce con etiquetas en blanco que dicen «null».",
                      "Un troll espiando detrás de los moldes, sonriendo; Zed señalando la palabra `this` en la pizarra."]),
            m(id="R02-N02-P3", titulo="Dos palancas",
              lugar="El taller de los soldados", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="Sobrecarga de constructores | Soldado(String nombre) { this(nombre, \"lanza\"); } · un constructor llama a otro con this(...) · va en la primera línea",
              recompensa="xp 15, oro 15",
              escena="""
                  La mayoría de los reclutas lleva lanza. La Maestra agrega una segunda palanca: si no decís el arma, sale con lanza. —Pero no copies el código del otro constructor —advierte—. **Llamalo**.
              """,
              sugiere="Se pueden tener varios constructores con distintos parámetros (sobrecarga). Uno puede llamar a otro con `this(...)`, en su **primera línea**: `this(nombre, \"lanza\");`.",
              desafio="Completá la llamada al otro constructor con el arma por defecto, \"lanza\".",
              inicial='''
                  public class DosPalancas {
                      public static void main(String[] args) {
                          Soldado a = new Soldado("Lía", "espada");
                          Soldado b = new Soldado("Teo");
                          System.out.println(a.nombre + " con " + a.arma);
                          System.out.println(b.nombre + " con " + b.arma);
                      }
                  }

                  class Soldado {
                      String nombre;
                      String arma;

                      Soldado(String nombre, String arma) {
                          this.nombre = nombre;
                          this.arma = arma;
                      }

                      Soldado(String nombre) {
                          ___;
                      }
                  }
              ''',
              solucion='''
                  public class DosPalancas {
                      public static void main(String[] args) {
                          Soldado a = new Soldado("Lía", "espada");
                          Soldado b = new Soldado("Teo");
                          System.out.println(a.nombre + " con " + a.arma);
                          System.out.println(b.nombre + " con " + b.arma);
                      }
                  }

                  class Soldado {
                      String nombre;
                      String arma;

                      Soldado(String nombre, String arma) {
                          this.nombre = nombre;
                          this.arma = arma;
                      }

                      Soldado(String nombre) {
                          this(nombre, "lanza");
                      }
                  }
              ''',
              al_superar="Teo sale con su lanza sin que nadie se la pida. —Una palanca usa la otra —dice Gheco—. Si mañana cambia cómo se arma un soldado, se cambia en un solo lugar.",
              imagen=["Dos palancas de bronce conectadas por un engranaje: la chica empuja a la grande.",
                      "Teo, un recluta joven, con una lanza recién salida del molde."]),
            m(id="R02-N02-P4", titulo="El constructor que desapareció",
              lugar="El taller de los soldados", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              criatura="goblin",
              carta="Constructor por defecto | si no escribís ninguno, Java pone uno vacío · si escribís uno, el vacío desaparece · new Soldado() deja de compilar",
              recompensa="xp 15, oro 15",
              escena="""
                  Un **goblin** se ríe en el taller: alguien escribió `new Soldado()` sin datos y el molde no lo acepta. —¡Antes andaba! —protesta el aprendiz. —Antes no había palancas —dice la Maestra.
              """,
              sugiere="Si una clase no tiene constructores, Java le pone uno **vacío**. Apenas escribís uno con parámetros, ese vacío **desaparece**. Si lo querés, escribilo vos: `Soldado() { this(\"recluta\", \"palo\"); }`.",
              desafio="Ejecutalo, leé el error y agregá un constructor sin parámetros que arme un \"recluta\" con un \"palo\".",
              inicial='''
                  public class Desaparecido {
                      public static void main(String[] args) {
                          Soldado s = new Soldado();
                          System.out.println(s.nombre + " con " + s.arma);
                      }
                  }

                  class Soldado {
                      String nombre;
                      String arma;

                      Soldado(String nombre, String arma) {
                          this.nombre = nombre;
                          this.arma = arma;
                      }
                  }
              ''',
              solucion='''
                  public class Desaparecido {
                      public static void main(String[] args) {
                          Soldado s = new Soldado();
                          System.out.println(s.nombre + " con " + s.arma);
                      }
                  }

                  class Soldado {
                      String nombre;
                      String arma;

                      Soldado() {
                          this("recluta", "palo");
                      }

                      Soldado(String nombre, String arma) {
                          this.nombre = nombre;
                          this.arma = arma;
                      }
                  }
              ''',
              al_superar="""
                  «recluta con palo.» El goblin se va refunfuñando. La Maestra los manda a la tesorería a buscar el pago del día. Zed va adelante: el cofre de la Academia está abierto, a la vista de todos.
              """,
              imagen=["Un goblin riéndose sobre un molde vacío que no se cierra.",
                      "Un recluta con un palo de madera, orgulloso igual."]),
        ],
    },
    {
        "titulo": "R02-N03 · Encapsulamiento y miembros static",
        "misiones": [
            m(id="R02-N03-P1", titulo="El cofre en negativo",
              lugar="La tesorería de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="private | private int saldo; · nadie de afuera lo toca · se cambia solo por los métodos del objeto, que validan",
              recompensa="xp 10, oro 15",
              escena="""
                  El cofre de la tesorería está abierto y Zed, por costumbre, mete la mano. Saca más de lo que hay y en la etiqueta queda escrito **«-500»**. La Maestra no lo reta: le da el molde del cofre. —Lo rompiste vos. Arreglalo vos: que **nadie**, ni vos, lo pueda dejar en negativo.
              """,
              sugiere="Con `private int saldo;` el saldo solo se toca desde **adentro** de la clase. Desde afuera se usa `retirar(monto)`, que puede negarse: si el monto es mayor que el saldo, devuelve `false` y no cambia nada.",
              desafio="Completá la condición: no se puede retirar más de lo que hay.",
              inicial='''
                  public class Tesoreria {
                      public static void main(String[] args) {
                          Cofre cofre = new Cofre(300);
                          System.out.println("Retiro 200: " + cofre.retirar(200));
                          System.out.println("Retiro 500: " + cofre.retirar(500));
                          System.out.println("Saldo: " + cofre.getSaldo());
                      }
                  }

                  class Cofre {
                      private int saldo;

                      Cofre(int saldoInicial) {
                          saldo = saldoInicial;
                      }

                      boolean retirar(int monto) {
                          if (___) {
                              return false;
                          }
                          saldo -= monto;
                          return true;
                      }

                      int getSaldo() {
                          return saldo;
                      }
                  }
              ''',
              solucion='''
                  public class Tesoreria {
                      public static void main(String[] args) {
                          Cofre cofre = new Cofre(300);
                          System.out.println("Retiro 200: " + cofre.retirar(200));
                          System.out.println("Retiro 500: " + cofre.retirar(500));
                          System.out.println("Saldo: " + cofre.getSaldo());
                      }
                  }

                  class Cofre {
                      private int saldo;

                      Cofre(int saldoInicial) {
                          saldo = saldoInicial;
                      }

                      boolean retirar(int monto) {
                          if (monto > saldo) {
                              return false;
                          }
                          saldo -= monto;
                          return true;
                      }

                      int getSaldo() {
                          return saldo;
                      }
                  }
              ''',
              al_superar="El segundo retiro rebota y el cofre queda en 100. Zed lo cierra él mismo. Es la primera vez que arregla algo que rompió, y no se siente mal: se siente raro.",
              imagen=["Un cofre de bronce cerrado con candado, con una etiqueta que dice «100» y otra vieja tachada que decía «-500».",
                      "Zed cerrando el cofre; la Maestra de Moldes mirándolo con los brazos cruzados, aprobando."]),
            m(id="R02-N03-P2", titulo="La ventanilla de lectura",
              lugar="La tesorería de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              criatura="troll",
              carta="Getter | int getSaldo() { return saldo; } · deja LEER sin dejar tocar · desde afuera: cofre.getSaldo(), nunca cofre.saldo",
              recompensa="xp 10, oro 10",
              escena="""
                  Nadia quiere anotar el saldo en su libreta y escribe `cofre.saldo`. La Aduana del compilador la frena: **`saldo has private access`**. —Hasta el reglamento me cierra la puerta —protesta.
              """,
              sugiere="Un atributo `private` no se lee desde otra clase. Para eso el objeto abre una **ventanilla de lectura**, un *getter*: `getSaldo()`. Desde afuera se usa siempre el método.",
              desafio="Ejecutalo, leé el error y cambiá `cofre.saldo` por el getter.",
              inicial='''
                  public class Ventanilla {
                      public static void main(String[] args) {
                          Cofre cofre = new Cofre(250);
                          System.out.println("Saldo para la libreta: " + cofre.saldo);
                      }
                  }

                  class Cofre {
                      private int saldo;

                      Cofre(int saldoInicial) {
                          saldo = saldoInicial;
                      }

                      int getSaldo() {
                          return saldo;
                      }
                  }
              ''',
              solucion='''
                  public class Ventanilla {
                      public static void main(String[] args) {
                          Cofre cofre = new Cofre(250);
                          System.out.println("Saldo para la libreta: " + cofre.getSaldo());
                      }
                  }

                  class Cofre {
                      private int saldo;

                      Cofre(int saldoInicial) {
                          saldo = saldoInicial;
                      }

                      int getSaldo() {
                          return saldo;
                      }
                  }
              ''',
              al_superar="Nadia anota «250» con letra prolija. —Así me gusta —dice—: una ventanilla, un reglamento, nadie metiendo la mano.",
              imagen=["Una ventanilla pequeña en el cofre de bronce por la que se ve un número, sin poder meter la mano.",
                      "Nadia escribiendo en su libreta, satisfecha."]),
            m(id="R02-N03-P3", titulo="La lista de inscriptos",
              lugar="La entrada de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="static | static int inscriptos; es UNO para toda la clase · lo comparten todos los objetos · se usa Alumno.inscriptos",
              recompensa="xp 15, oro 15",
              escena="""
                  En la entrada, la Maestra quiere saber cuántos alumnos se inscribieron hoy. Cada alumno tiene su nombre, pero el número de inscriptos no es de ninguno: es **de la Academia**.
              """,
              sugiere="Un atributo `static` es **de la clase**, no de cada objeto: hay uno solo, compartido. Si el constructor hace `inscriptos++`, cada `new` suma uno al mismo contador. Desde afuera se lee con el nombre de la clase: `Alumno.inscriptos`.",
              desafio="Completá la declaración para que el contador sea uno solo para toda la clase.",
              inicial='''
                  public class Inscripcion {
                      public static void main(String[] args) {
                          Alumno a = new Alumno("Zed");
                          Alumno b = new Alumno("Nadia");
                          Alumno c = new Alumno("Teo");
                          System.out.println(a.nombre + ", " + b.nombre + " y " + c.nombre);
                          System.out.println("Inscriptos: " + Alumno.inscriptos);
                      }
                  }

                  class Alumno {
                      ___ int inscriptos = 0;
                      String nombre;

                      Alumno(String nombre) {
                          this.nombre = nombre;
                          inscriptos++;
                      }
                  }
              ''',
              solucion='''
                  public class Inscripcion {
                      public static void main(String[] args) {
                          Alumno a = new Alumno("Zed");
                          Alumno b = new Alumno("Nadia");
                          Alumno c = new Alumno("Teo");
                          System.out.println(a.nombre + ", " + b.nombre + " y " + c.nombre);
                          System.out.println("Inscriptos: " + Alumno.inscriptos);
                      }
                  }

                  class Alumno {
                      static int inscriptos = 0;
                      String nombre;

                      Alumno(String nombre) {
                          this.nombre = nombre;
                          inscriptos++;
                      }
                  }
              ''',
              al_superar="«Inscriptos: 3.» —¿Nadia también se inscribió? —pregunta Zed. —Alguien tiene que vigilarte adentro —responde ella, sin mirarlo.",
              imagen=["Un libro de inscripción gigante en la entrada de la Academia, con un contador de bronce que marca 3.",
                      "Nadia firmando el libro; Zed sorprendido."]),
            m(id="R02-N03-P4", titulo="La tasa que no se toca",
              lugar="La tesorería de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="final | static final double TASA = 0.10; · una constante: no se puede cambiar · en mayúsculas por costumbre",
              recompensa="xp 15, oro 15",
              escena="""
                  La Academia cobra una tasa del 10 % sobre cada molde vendido. Zed, viejas mañas, intenta bajarla a escondidas desde el `main`. La Aduana del compilador lo atrapa en el acto.
              """,
              sugiere="Un atributo `final` no se puede volver a asignar: `static final double TASA = 0.10;` es una **constante**. Si alguien escribe `Tesoro.TASA = 0.01;`, no compila. La solución no es pelear con el compilador: es **sacar** esa línea.",
              desafio="Ejecutalo, leé el error y borrá la línea de la trampa.",
              inicial='''
                  public class Tasa {
                      public static void main(String[] args) {
                          Tesoro.TASA = 0.01;
                          double venta = 400;
                          System.out.println("Venta: " + venta);
                          System.out.println("Tasa: " + venta * Tesoro.TASA);
                      }
                  }

                  class Tesoro {
                      static final double TASA = 0.10;
                  }
              ''',
              solucion='''
                  public class Tasa {
                      public static void main(String[] args) {
                          double venta = 400;
                          System.out.println("Venta: " + venta);
                          System.out.println("Tasa: " + venta * Tesoro.TASA);
                      }
                  }

                  class Tesoro {
                      static final double TASA = 0.10;
                  }
              ''',
              al_superar="""
                  Cuarenta denarios de tasa, como dice el reglamento. —Ni lo intentes otra vez —dice Nadia, y por primera vez Zed no lo intenta.
                  En el depósito de la Academia, dos alumnos discuten frente a un escudo dorado abollado. Cada uno jura que no lo tocó.
              """,
              imagen=["Una placa de bronce atornillada en la pared de la tesorería: «TASA 10 %», con un candado.",
                      "Zed con las manos en los bolsillos; Nadia vigilándolo."]),
        ],
    },
    {
        "titulo": "R02-N04 · Referencias, null y equals",
        "misiones": [
            m(id="R02-N04-P1", titulo="El escudo abollado",
              lugar="El depósito de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              criatura="troll",
              carta="Referencia | Escudo b = a; NO copia el escudo: las dos variables señalan el MISMO objeto · para otro escudo, otro new",
              recompensa="xp 10, oro 10",
              escena="""
                  Dos alumnos tienen una tarjeta que dice «escudo dorado, estante 7». Uno lo lleva a pulir y lo abolla. El otro va al estante, lo ve abollado y no entiende nada. Un **troll** se ríe desde el estante.
                  —Las dos tarjetas señalaban **el mismo escudo** —dice Gheco.
              """,
              sugiere="Una variable de tipo clase guarda una **referencia**: la dirección del objeto, no el objeto. `Escudo b = a;` hace que `b` señale al mismo escudo que `a`. Para que cada uno tenga el suyo, `b` necesita su propio `new`.",
              desafio="Ejecutalo y fijate que se abollan los dos. Después hacé que `b` sea un escudo nuevo.",
              inicial='''
                  public class Escudos {
                      public static void main(String[] args) {
                          Escudo a = new Escudo();
                          Escudo b = a;
                          b.abollado = true;
                          System.out.println("Escudo de a abollado: " + a.abollado);
                          System.out.println("Escudo de b abollado: " + b.abollado);
                      }
                  }

                  class Escudo {
                      boolean abollado;
                  }
              ''',
              solucion='''
                  public class Escudos {
                      public static void main(String[] args) {
                          Escudo a = new Escudo();
                          Escudo b = new Escudo();
                          b.abollado = true;
                          System.out.println("Escudo de a abollado: " + a.abollado);
                          System.out.println("Escudo de b abollado: " + b.abollado);
                      }
                  }

                  class Escudo {
                      boolean abollado;
                  }
              ''',
              al_superar="Ahora hay dos escudos, y solo uno abollado. Los alumnos se dan la mano. El troll, aburrido, se mete en otro estante.",
              imagen=["Dos tarjetas con flechas de luz que apuntan al mismo escudo dorado abollado.",
                      "Un troll riéndose desde un estante alto; Zed con un escudo nuevo en la mano."]),
            m(id="R02-N04-P2", titulo="El viajero que no estaba",
              lugar="El registro de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              criatura="troll",
              carta="null | una referencia que no señala nada · v.metodo() con v null da NullPointerException · preguntá antes: if (v != null)",
              recompensa="xp 15, oro 15",
              escena="""
                  Zed busca en el registro a un viajero que llegó «con un vitral». La búsqueda no lo encuentra y devuelve `null`. Al usarlo, el programa se corta con un **NullPointerException** y el troll vuelve, feliz.
              """,
              sugiere="`null` significa «no hay objeto». Llamar un método sobre `null` corta el programa. Antes de usar una referencia que puede no estar, preguntá: `if (v != null) { … } else { … }`.",
              desafio="Completá la condición para usar al viajero solo si se encontró.",
              inicial='''
                  public class Registro {
                      static Viajero buscar(String nombre) {
                          if (nombre.equals("Zed")) {
                              Viajero v = new Viajero();
                              v.nombre = "Zed";
                              return v;
                          }
                          return null;
                      }

                      public static void main(String[] args) {
                          String[] pedidos = {"Zed", "el Vidriero"};
                          for (String p : pedidos) {
                              Viajero v = buscar(p);
                              if (___) {
                                  System.out.println("Encontrado: " + v.nombre.toUpperCase());
                              } else {
                                  System.out.println(p + ": no está en el registro");
                              }
                          }
                      }
                  }

                  class Viajero {
                      String nombre;
                  }
              ''',
              solucion='''
                  public class Registro {
                      static Viajero buscar(String nombre) {
                          if (nombre.equals("Zed")) {
                              Viajero v = new Viajero();
                              v.nombre = "Zed";
                              return v;
                          }
                          return null;
                      }

                      public static void main(String[] args) {
                          String[] pedidos = {"Zed", "el Vidriero"};
                          for (String p : pedidos) {
                              Viajero v = buscar(p);
                              if (v != null) {
                                  System.out.println("Encontrado: " + v.nombre.toUpperCase());
                              } else {
                                  System.out.println(p + ": no está en el registro");
                              }
                          }
                      }
                  }

                  class Viajero {
                      String nombre;
                  }
              ''',
              al_superar="«el Vidriero: no está en el registro.» Pero alguien lo buscó antes que Zed: en el margen hay una marca a lápiz. Nadia la mira y no dice nada.",
              imagen=["Un registro de la Academia abierto; un renglón vacío con una marca a lápiz en el margen.",
                      "El troll escondiéndose al ver el `if`; Nadia mirando la marca, pensativa."]),
            m(id="R02-N04-P3", titulo="Dos sellos iguales",
              lugar="El depósito de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="equals | == pregunta si es EL MISMO objeto · equals pregunta si son IGUALES · hay que escribirlo: public boolean equals(Object o)",
              recompensa="xp 15, oro 15",
              escena="""
                  Hay dos sellos con el mismo código, «A-7». Son dos objetos distintos, pero valen lo mismo. Con `==` dan `false`, y con `equals`… también, porque nadie le explicó al molde cuándo dos sellos son iguales.
              """,
              sugiere="`==` compara **identidad** (si es el mismo objeto). `equals` compara **igualdad**, pero hay que escribirlo: si el otro es un `Sello`, son iguales cuando tienen el mismo `codigo`. Los `String` se comparan con `equals`.",
              desafio="Completá el `return` de `equals`: iguales si tienen el mismo código.",
              inicial='''
                  public class Sellos {
                      public static void main(String[] args) {
                          Sello a = new Sello("A-7");
                          Sello b = new Sello("A-7");
                          Sello c = new Sello("B-2");
                          System.out.println("a == b: " + (a == b));
                          System.out.println("a.equals(b): " + a.equals(b));
                          System.out.println("a.equals(c): " + a.equals(c));
                      }
                  }

                  class Sello {
                      String codigo;

                      Sello(String codigo) {
                          this.codigo = codigo;
                      }

                      @Override
                      public boolean equals(Object o) {
                          if (!(o instanceof Sello)) {
                              return false;
                          }
                          Sello otro = (Sello) o;
                          return ___;
                      }
                  }
              ''',
              solucion='''
                  public class Sellos {
                      public static void main(String[] args) {
                          Sello a = new Sello("A-7");
                          Sello b = new Sello("A-7");
                          Sello c = new Sello("B-2");
                          System.out.println("a == b: " + (a == b));
                          System.out.println("a.equals(b): " + a.equals(b));
                          System.out.println("a.equals(c): " + a.equals(c));
                      }
                  }

                  class Sello {
                      String codigo;

                      Sello(String codigo) {
                          this.codigo = codigo;
                      }

                      @Override
                      public boolean equals(Object o) {
                          if (!(o instanceof Sello)) {
                              return false;
                          }
                          Sello otro = (Sello) o;
                          return codigo.equals(otro.codigo);
                      }
                  }
              ''',
              al_superar="«a == b: false. a.equals(b): true.» —Son dos sellos, pero valen lo mismo —resume Zed—. Como en la Aduana con los textos. —Exacto —dice Nadia—. Lo aprendiste allá y no te diste cuenta.",
              imagen=["Dos sellos de bronce idénticos con el código «A-7», uno al lado del otro, unidos por un signo igual de luz.",
                      "Un tercer sello «B-2» apartado."]),
            m(id="R02-N04-P4", titulo="La huella del sello",
              lugar="El depósito de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="hashCode | si dos objetos son equals, tienen que dar el mismo hashCode · return Objects.hash(codigo); · import java.util.Objects;",
              recompensa="xp 15, oro 15",
              escena="""
                  —Si escribís `equals`, escribí también `hashCode` —dice la Maestra—. Es la **huella** del objeto: dos sellos iguales tienen que dejar la misma huella. Los archivos del Imperio buscan por huella, y si no coincide, no los encuentran.
              """,
              sugiere="`hashCode()` devuelve un número que resume al objeto. La regla: si `a.equals(b)`, entonces `a.hashCode() == b.hashCode()`. Lo más simple: `return Objects.hash(codigo);` con los mismos campos que usa `equals`.",
              desafio="Completá el `hashCode` con el mismo campo que usa `equals`.",
              inicial='''
                  import java.util.Objects;

                  public class Huella {
                      public static void main(String[] args) {
                          Sello a = new Sello("A-7");
                          Sello b = new Sello("A-7");
                          System.out.println("Iguales: " + a.equals(b));
                          System.out.println("Misma huella: " + (a.hashCode() == b.hashCode()));
                      }
                  }

                  class Sello {
                      String codigo;

                      Sello(String codigo) {
                          this.codigo = codigo;
                      }

                      @Override
                      public boolean equals(Object o) {
                          if (!(o instanceof Sello)) {
                              return false;
                          }
                          return codigo.equals(((Sello) o).codigo);
                      }

                      @Override
                      public int hashCode() {
                          return ___;
                      }
                  }
              ''',
              solucion='''
                  import java.util.Objects;

                  public class Huella {
                      public static void main(String[] args) {
                          Sello a = new Sello("A-7");
                          Sello b = new Sello("A-7");
                          System.out.println("Iguales: " + a.equals(b));
                          System.out.println("Misma huella: " + (a.hashCode() == b.hashCode()));
                      }
                  }

                  class Sello {
                      String codigo;

                      Sello(String codigo) {
                          this.codigo = codigo;
                      }

                      @Override
                      public boolean equals(Object o) {
                          if (!(o instanceof Sello)) {
                              return false;
                          }
                          return codigo.equals(((Sello) o).codigo);
                      }

                      @Override
                      public int hashCode() {
                          return Objects.hash(codigo);
                      }
                  }
              ''',
              al_superar="""
                  Misma huella, iguales en todo. La Maestra guarda los sellos en su lugar.
                  En el ala oeste, cubierto de polvo, hay un molde viejísimo con una palabra grabada: **Personaje**. De él salieron todos los demás.
              """,
              imagen=["Dos sellos estampados en lacre que dejan exactamente la misma huella brillante.",
                      "Al fondo, en un pasillo oscuro, un molde viejo y enorme con la palabra «Personaje» grabada."]),
        ],
    },
    {
        "titulo": "R02-N05 · Herencia: extends y super",
        "misiones": [
            m(id="R02-N05-P1", titulo="El molde Personaje",
              lugar="El ala oeste de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="extends | class Guerrero extends Personaje · el hijo HEREDA los atributos y métodos del padre · agrega lo suyo",
              recompensa="xp 10, oro 10",
              escena="""
                  En el ala oeste, el molde **Personaje** tiene nombre, vida y un método para describirse. De él salen los demás. —No escribas dos veces lo que todos tienen —dice la Maestra—. El Guerrero **es** un Personaje: que lo herede.
              """,
              sugiere="`class Guerrero extends Personaje` hace que el Guerrero tenga todo lo del Personaje (`nombre`, `vida`, `describir()`) sin escribirlo de nuevo, y le suma lo suyo (`fuerza`).",
              desafio="Completá la palabra que hace que el Guerrero herede del Personaje.",
              inicial='''
                  public class AlaOeste {
                      public static void main(String[] args) {
                          Guerrero g = new Guerrero();
                          g.nombre = "Lía";
                          g.vida = 120;
                          g.fuerza = 9;
                          System.out.println(g.describir());
                          System.out.println("Fuerza: " + g.fuerza);
                      }
                  }

                  class Personaje {
                      String nombre;
                      int vida;

                      String describir() {
                          return nombre + " (" + vida + " de vida)";
                      }
                  }

                  class Guerrero ___ Personaje {
                      int fuerza;
                  }
              ''',
              solucion='''
                  public class AlaOeste {
                      public static void main(String[] args) {
                          Guerrero g = new Guerrero();
                          g.nombre = "Lía";
                          g.vida = 120;
                          g.fuerza = 9;
                          System.out.println(g.describir());
                          System.out.println("Fuerza: " + g.fuerza);
                      }
                  }

                  class Personaje {
                      String nombre;
                      int vida;

                      String describir() {
                          return nombre + " (" + vida + " de vida)";
                      }
                  }

                  class Guerrero extends Personaje {
                      int fuerza;
                  }
              ''',
              al_superar="Lía sale del molde Guerrero con nombre, vida y fuerza, y nadie escribió `describir` dos veces. —Es como heredar el oficio del padre —dice Zed—. Yo heredé el de ladrón. —Y lo estás sobrescribiendo —responde Nadia.",
              imagen=["El molde viejo «Personaje» en el centro y, saliendo de él con ramas de bronce, los moldes Guerrero, Arquero y Maga.",
                      "Lía, una guerrera joven, recién salida del molde Guerrero."]),
            m(id="R02-N05-P2", titulo="Primero el padre",
              lugar="El ala oeste de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="super(...) | el constructor del hijo llama al del padre con super(nombre, vida); · en la primera línea · el padre arma su parte",
              recompensa="xp 15, oro 15",
              escena="""
                  El molde Personaje ahora tiene constructor: pide nombre y vida. El molde Guerrero ya no compila. —El hijo tiene que dejar que el padre arme **su parte** primero —dice la Maestra.
              """,
              sugiere="Si el padre tiene un constructor con parámetros, el hijo lo llama con `super(…)` en la **primera línea** del suyo: `super(nombre, 120);`. Después, el hijo arma lo propio: `this.fuerza = fuerza;`.",
              desafio="Completá la llamada al constructor del padre: los guerreros arrancan con 120 de vida.",
              inicial='''
                  public class PrimeroElPadre {
                      public static void main(String[] args) {
                          Guerrero g = new Guerrero("Lía", 9);
                          System.out.println(g.describir() + ", fuerza " + g.fuerza);
                      }
                  }

                  class Personaje {
                      String nombre;
                      int vida;

                      Personaje(String nombre, int vida) {
                          this.nombre = nombre;
                          this.vida = vida;
                      }

                      String describir() {
                          return nombre + " (" + vida + " de vida)";
                      }
                  }

                  class Guerrero extends Personaje {
                      int fuerza;

                      Guerrero(String nombre, int fuerza) {
                          ___;
                          this.fuerza = fuerza;
                      }
                  }
              ''',
              solucion='''
                  public class PrimeroElPadre {
                      public static void main(String[] args) {
                          Guerrero g = new Guerrero("Lía", 9);
                          System.out.println(g.describir() + ", fuerza " + g.fuerza);
                      }
                  }

                  class Personaje {
                      String nombre;
                      int vida;

                      Personaje(String nombre, int vida) {
                          this.nombre = nombre;
                          this.vida = vida;
                      }

                      String describir() {
                          return nombre + " (" + vida + " de vida)";
                      }
                  }

                  class Guerrero extends Personaje {
                      int fuerza;

                      Guerrero(String nombre, int fuerza) {
                          super(nombre, 120);
                          this.fuerza = fuerza;
                      }
                  }
              ''',
              al_superar="El molde Guerrero vuelve a cerrar. Primero el padre pone nombre y vida, después el hijo pone la fuerza. —Orden —dice Gheco—. Como con el Centinela.",
              imagen=["Dos moldes encastrados: el grande (Personaje) se cierra primero y el chico (Guerrero) encaja encima.",
                      "La Maestra de Moldes ajustando una tuerca; Zed mirando con atención."]),
            m(id="R02-N05-P3", titulo="El arquero sin nombre",
              lugar="El ala oeste de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              criatura="esqueleto",
              carta="@Override | el hijo REEMPLAZA un método del padre con el mismo nombre y parámetros · @Override hace que el compilador lo controle",
              recompensa="xp 15, oro 15",
              escena="""
                  El Arquero quiere describirse a su manera, pero quien escribió su método se equivocó en una letra. Gracias a `@Override`, la Aduana del compilador lo frena: ese método no reemplaza a nada. Un **esqueleto** sale del molde, sin nombre que lo sostenga.
              """,
              sugiere="Para **sobrescribir** un método, el hijo lo escribe con el **mismo nombre y parámetros** que el padre. `@Override` le pide al compilador que lo controle: si el nombre está mal escrito, avisa.",
              desafio="Ejecutalo, leé el error y corregí el nombre del método del Arquero.",
              inicial='''
                  public class Arqueros {
                      public static void main(String[] args) {
                          Personaje p = new Personaje("Teo");
                          Arquero a = new Arquero("Mira");
                          System.out.println(p.describir());
                          System.out.println(a.describir());
                      }
                  }

                  class Personaje {
                      String nombre;

                      Personaje(String nombre) {
                          this.nombre = nombre;
                      }

                      String describir() {
                          return nombre + ", un personaje";
                      }
                  }

                  class Arquero extends Personaje {
                      Arquero(String nombre) {
                          super(nombre);
                      }

                      @Override
                      String descrbir() {
                          return nombre + ", arquera que nunca falla";
                      }
                  }
              ''',
              solucion='''
                  public class Arqueros {
                      public static void main(String[] args) {
                          Personaje p = new Personaje("Teo");
                          Arquero a = new Arquero("Mira");
                          System.out.println(p.describir());
                          System.out.println(a.describir());
                      }
                  }

                  class Personaje {
                      String nombre;

                      Personaje(String nombre) {
                          this.nombre = nombre;
                      }

                      String describir() {
                          return nombre + ", un personaje";
                      }
                  }

                  class Arquero extends Personaje {
                      Arquero(String nombre) {
                          super(nombre);
                      }

                      @Override
                      String describir() {
                          return nombre + ", arquera que nunca falla";
                      }
                  }
              ''',
              al_superar="Mira se presenta como arquera, no como «un personaje». El esqueleto encuentra su nombre en la etiqueta corregida y se desarma tranquilo.",
              imagen=["Una etiqueta de bronce con «descrbir» tachado y «describir» escrito encima.",
                      "Mira, una arquera de capa verde, con el arco tenso; un esqueleto desarmándose a sus pies."]),
            m(id="R02-N05-P4", titulo="Lo del padre, y algo más",
              lugar="El ala oeste de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="super.metodo() | el hijo usa lo que hacía el padre y le agrega lo suyo · return super.describir() + \" …\";",
              recompensa="xp 15, oro 15",
              escena="""
                  La Maga quiere describirse como cualquier personaje (nombre y vida), **más** su hechizo. —No copies lo del padre —dice la Maestra—. Pedíselo.
              """,
              sugiere="Adentro de un método sobrescrito, `super.describir()` llama a la versión del **padre**. Así el hijo reutiliza lo que ya existe y le agrega lo suyo.",
              desafio="Completá el `return`: lo que describe el padre, más \" y lanza rayos\".",
              inicial='''
                  public class Magas {
                      public static void main(String[] args) {
                          Maga m = new Maga("Sol", 80);
                          System.out.println(m.describir());
                      }
                  }

                  class Personaje {
                      String nombre;
                      int vida;

                      Personaje(String nombre, int vida) {
                          this.nombre = nombre;
                          this.vida = vida;
                      }

                      String describir() {
                          return nombre + " (" + vida + " de vida)";
                      }
                  }

                  class Maga extends Personaje {
                      Maga(String nombre, int vida) {
                          super(nombre, vida);
                      }

                      @Override
                      String describir() {
                          return ___;
                      }
                  }
              ''',
              solucion='''
                  public class Magas {
                      public static void main(String[] args) {
                          Maga m = new Maga("Sol", 80);
                          System.out.println(m.describir());
                      }
                  }

                  class Personaje {
                      String nombre;
                      int vida;

                      Personaje(String nombre, int vida) {
                          this.nombre = nombre;
                          this.vida = vida;
                      }

                      String describir() {
                          return nombre + " (" + vida + " de vida)";
                      }
                  }

                  class Maga extends Personaje {
                      Maga(String nombre, int vida) {
                          super(nombre, vida);
                      }

                      @Override
                      String describir() {
                          return super.describir() + " y lanza rayos";
                      }
                  }
              ''',
              al_superar="""
                  «Sol (80 de vida) y lanza rayos.» Guerrera, arquera y maga: tres moldes, un solo padre.
                  Desde el patio llega un grito: la Maestra reúne a todos los alumnos para un ejercicio con una sola orden.
              """,
              imagen=["Sol, una maga joven de túnica azul, con un rayo entre las manos.",
                      "Detrás, Lía y Mira; al fondo, el patio de armas de la Academia lleno de alumnos."]),
        ],
    },
]
