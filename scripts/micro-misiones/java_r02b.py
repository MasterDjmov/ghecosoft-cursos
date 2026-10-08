from genjava import m

# R02-N06 a N11: el patio de armas, la sala de los pactos, el taller de armaduras, el archivo, la biblioteca y la
# Quimera. La clase con el main va primero; nada de colecciones ni excepciones (son de R03).

NODOS = [
    {
        "titulo": "R02-N06 · Polimorfismo y clases abstractas",
        "misiones": [
            m(id="R02-N06-P1", titulo="Una sola orden",
              lugar="El patio de armas de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="Polimorfismo | Personaje[] tropa = {new Guerrera(), new Arquera()} · un mismo mensaje (atacar) · cada objeto responde a su manera",
              recompensa="xp 10, oro 10",
              escena="""
                  En el patio de armas, la Maestra grita una sola orden: **¡Ataquen!** Y cada alumno ataca a su manera. Ella no necesita saber quién es quién: sabe que todos son personajes y que todos saben atacar.
              """,
              sugiere="Una variable (o un array) del tipo del **padre** puede guardar objetos de cualquier hijo: `Personaje[] tropa`. Al llamar `p.atacar()`, se ejecuta el método del objeto **real**: el de la guerrera, el de la arquera…",
              desafio="Completá el tipo del array para que entren los tres alumnos.",
              inicial='''
                  public class Patio {
                      public static void main(String[] args) {
                          ___[] tropa = {new Guerrera("Lía"), new Arquera("Mira"), new Maga("Sol")};
                          for (Personaje p : tropa) {
                              System.out.println(p.nombre + ": " + p.atacar());
                          }
                      }
                  }

                  class Personaje {
                      String nombre;

                      Personaje(String nombre) {
                          this.nombre = nombre;
                      }

                      String atacar() {
                          return "empuja";
                      }
                  }

                  class Guerrera extends Personaje {
                      Guerrera(String nombre) { super(nombre); }

                      @Override
                      String atacar() { return "golpe de espada"; }
                  }

                  class Arquera extends Personaje {
                      Arquera(String nombre) { super(nombre); }

                      @Override
                      String atacar() { return "flecha certera"; }
                  }

                  class Maga extends Personaje {
                      Maga(String nombre) { super(nombre); }

                      @Override
                      String atacar() { return "rayo"; }
                  }
              ''',
              solucion='''
                  public class Patio {
                      public static void main(String[] args) {
                          Personaje[] tropa = {new Guerrera("Lía"), new Arquera("Mira"), new Maga("Sol")};
                          for (Personaje p : tropa) {
                              System.out.println(p.nombre + ": " + p.atacar());
                          }
                      }
                  }

                  class Personaje {
                      String nombre;

                      Personaje(String nombre) {
                          this.nombre = nombre;
                      }

                      String atacar() {
                          return "empuja";
                      }
                  }

                  class Guerrera extends Personaje {
                      Guerrera(String nombre) { super(nombre); }

                      @Override
                      String atacar() { return "golpe de espada"; }
                  }

                  class Arquera extends Personaje {
                      Arquera(String nombre) { super(nombre); }

                      @Override
                      String atacar() { return "flecha certera"; }
                  }

                  class Maga extends Personaje {
                      Maga(String nombre) { super(nombre); }

                      @Override
                      String atacar() { return "rayo"; }
                  }
              ''',
              al_superar="Espada, flecha y rayo, con una sola orden. —Un mismo mensaje, muchas formas de responderlo —dice Gheco—. Eso es el **polimorfismo**.",
              imagen=["El patio de armas de la Academia: la Maestra de Moldes gritando una orden con el brazo en alto.",
                      "Lía con espada, Mira con arco y Sol con un rayo, atacando a la vez a muñecos de práctica."]),
            m(id="R02-N06-P2", titulo="Nadie es un personaje a secas",
              lugar="El patio de armas de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="Clase abstracta | abstract class Personaje · no se puede hacer new Personaje() · abstract String atacar(); obliga a cada hijo a escribirlo",
              recompensa="xp 15, oro 15",
              escena="""
                  —¿Y si alguien sale del molde Personaje, sin ser guerrero ni arquero ni nada? —pregunta Zed. —Sería un alumno que no sabe atacar —dice la Maestra—. Por eso ese molde es **abstracto**: existe para que los demás lo completen.
              """,
              sugiere="Una clase `abstract` no se puede instanciar: solo sirve de padre. Un método `abstract` no tiene cuerpo (`abstract String atacar();`) y **obliga** a cada hijo concreto a escribirlo. Si una clase tiene un método abstracto, la clase también tiene que ser `abstract`.",
              desafio="Completá la palabra que hace abstracta a la clase Personaje.",
              inicial='''
                  public class Abstracto {
                      public static void main(String[] args) {
                          Personaje[] tropa = {new Guerrera("Lía"), new Arquera("Mira")};
                          for (Personaje p : tropa) {
                              System.out.println(p.nombre + ": " + p.atacar());
                          }
                      }
                  }

                  ___ class Personaje {
                      String nombre;

                      Personaje(String nombre) {
                          this.nombre = nombre;
                      }

                      abstract String atacar();
                  }

                  class Guerrera extends Personaje {
                      Guerrera(String nombre) { super(nombre); }

                      @Override
                      String atacar() { return "golpe de espada"; }
                  }

                  class Arquera extends Personaje {
                      Arquera(String nombre) { super(nombre); }

                      @Override
                      String atacar() { return "flecha certera"; }
                  }
              ''',
              solucion='''
                  public class Abstracto {
                      public static void main(String[] args) {
                          Personaje[] tropa = {new Guerrera("Lía"), new Arquera("Mira")};
                          for (Personaje p : tropa) {
                              System.out.println(p.nombre + ": " + p.atacar());
                          }
                      }
                  }

                  abstract class Personaje {
                      String nombre;

                      Personaje(String nombre) {
                          this.nombre = nombre;
                      }

                      abstract String atacar();
                  }

                  class Guerrera extends Personaje {
                      Guerrera(String nombre) { super(nombre); }

                      @Override
                      String atacar() { return "golpe de espada"; }
                  }

                  class Arquera extends Personaje {
                      Arquera(String nombre) { super(nombre); }

                      @Override
                      String atacar() { return "flecha certera"; }
                  }
              ''',
              al_superar="El molde Personaje queda cerrado con un candado: de ahí ya no sale nadie a medio hacer. Solo sirve para que los otros moldes se apoyen en él.",
              imagen=["El molde viejo «Personaje» con un candado de bronce y la palabra «abstract» grabada.",
                      "Los moldes Guerrera y Arquera, abiertos y brillantes, apoyados en él."]),
            m(id="R02-N06-P3", titulo="La maga disfrazada",
              lugar="El patio de armas de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              criatura="goblin",
              carta="instanceof y casting | if (p instanceof Maga) { Maga m = (Maga) p; m.curar(); } · preguntá antes de convertir · sin preguntar: ClassCastException",
              recompensa="xp 15, oro 15",
              escena="""
                  En la tropa, Lía está herida. Solo una maga puede curar, pero en el array todas son `Personaje`, y un `Personaje` no sabe curar. Un **goblin** se ofrece a convertir a cualquiera en maga «a la fuerza».
              """,
              sugiere="Con una variable `Personaje` solo se ven los métodos de `Personaje`. Para usar uno de `Maga`, primero preguntá con `instanceof` y después convertí la referencia con un **casting**: `Maga m = (Maga) p;`. Convertir sin preguntar es lo que quiere el goblin.",
              desafio="Completá el casting para usar a la maga.",
              inicial='''
                  public class Disfraz {
                      public static void main(String[] args) {
                          Personaje[] tropa = {new Guerrera("Lía"), new Maga("Sol")};
                          for (Personaje p : tropa) {
                              if (p instanceof Maga) {
                                  Maga m = ___;
                                  System.out.println(m.nombre + " cura: " + m.curar());
                              } else {
                                  System.out.println(p.nombre + " no sabe curar");
                              }
                          }
                      }
                  }

                  class Personaje {
                      String nombre;

                      Personaje(String nombre) { this.nombre = nombre; }
                  }

                  class Guerrera extends Personaje {
                      Guerrera(String nombre) { super(nombre); }
                  }

                  class Maga extends Personaje {
                      Maga(String nombre) { super(nombre); }

                      int curar() { return 30; }
                  }
              ''',
              solucion='''
                  public class Disfraz {
                      public static void main(String[] args) {
                          Personaje[] tropa = {new Guerrera("Lía"), new Maga("Sol")};
                          for (Personaje p : tropa) {
                              if (p instanceof Maga) {
                                  Maga m = (Maga) p;
                                  System.out.println(m.nombre + " cura: " + m.curar());
                              } else {
                                  System.out.println(p.nombre + " no sabe curar");
                              }
                          }
                      }
                  }

                  class Personaje {
                      String nombre;

                      Personaje(String nombre) { this.nombre = nombre; }
                  }

                  class Guerrera extends Personaje {
                      Guerrera(String nombre) { super(nombre); }
                  }

                  class Maga extends Personaje {
                      Maga(String nombre) { super(nombre); }

                      int curar() { return 30; }
                  }
              ''',
              al_superar="Sol cura a Lía. El goblin se queda con las ganas: nadie se convirtió en lo que no era. —Igual —dice la Maestra—, si tenés que preguntar mucho «¿sos maga?», a lo mejor te falta un contrato.",
              imagen=["Sol curando a Lía con una luz verde.",
                      "Un goblin con un disfraz de maga en las manos, frustrado."]),
            m(id="R02-N06-P4", titulo="El turno de cada uno",
              lugar="El patio de armas de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="Lo común en el padre | la clase abstracta escribe lo que todos hacen igual (turno) · deja abstracto lo que cada uno hace distinto (atacar)",
              recompensa="xp 15, oro 15",
              escena="""
                  La Maestra escribe en el molde Personaje cómo es un **turno**: decir el nombre y atacar. Eso es igual para todos. Lo único distinto es **cómo** ataca cada uno. Falta el molde de la arquera.
              """,
              sugiere="Una clase abstracta puede tener métodos **con cuerpo** que usan los abstractos: `turno()` arma el texto y llama a `atacar()`, que cada hijo escribe a su manera.",
              desafio="Completá el `return` del `atacar` de la Arquera: \"flecha certera\".",
              inicial='''
                  public class Turnos {
                      public static void main(String[] args) {
                          Personaje[] tropa = {new Guerrera("Lía"), new Arquera("Mira")};
                          for (Personaje p : tropa) {
                              System.out.println(p.turno());
                          }
                      }
                  }

                  abstract class Personaje {
                      String nombre;

                      Personaje(String nombre) { this.nombre = nombre; }

                      abstract String atacar();

                      String turno() {
                          return "Turno de " + nombre + ": " + atacar();
                      }
                  }

                  class Guerrera extends Personaje {
                      Guerrera(String nombre) { super(nombre); }

                      @Override
                      String atacar() { return "golpe de espada"; }
                  }

                  class Arquera extends Personaje {
                      Arquera(String nombre) { super(nombre); }

                      @Override
                      String atacar() { return ___; }
                  }
              ''',
              solucion='''
                  public class Turnos {
                      public static void main(String[] args) {
                          Personaje[] tropa = {new Guerrera("Lía"), new Arquera("Mira")};
                          for (Personaje p : tropa) {
                              System.out.println(p.turno());
                          }
                      }
                  }

                  abstract class Personaje {
                      String nombre;

                      Personaje(String nombre) { this.nombre = nombre; }

                      abstract String atacar();

                      String turno() {
                          return "Turno de " + nombre + ": " + atacar();
                      }
                  }

                  class Guerrera extends Personaje {
                      Guerrera(String nombre) { super(nombre); }

                      @Override
                      String atacar() { return "golpe de espada"; }
                  }

                  class Arquera extends Personaje {
                      Arquera(String nombre) { super(nombre); }

                      @Override
                      String atacar() { return "flecha certera"; }
                  }
              ''',
              al_superar="""
                  Dos turnos, un solo método `turno`. Al terminar el ejercicio, Zed intenta abrir con su ganzúa la puerta de la sala de al lado, por costumbre. La ganzúa no entra. En el cartel dice: **Sala de los Pactos**.
              """,
              imagen=["Lía y Mira tomando turnos frente a un muñeco de práctica.",
                      "Zed con la ganzúa contra una cerradura que no tiene ojo: la puerta de la Sala de los Pactos."]),
        ],
    },
    {
        "titulo": "R02-N07 · Interfaces: contratos",
        "misiones": [
            m(id="R02-N07-P1", titulo="La puerta sin cerradura",
              lugar="La Sala de los Pactos", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="interface | interface Nadador { String nadar(); } · un contrato: QUÉ sabe hacer · class Barco implements Nadador lo firma y lo cumple",
              recompensa="xp 10, oro 10",
              escena="""
                  La puerta de la Sala de los Pactos no tiene cerradura: tiene un pergamino. **Kaffa** aparece con su taza de café. —En el Imperio, las puertas no se abren con ganzúa, Zed. Se abren con **contratos**. Adentro cuelgan muchos: «quien firme este se compromete a saber nadar».
              """,
              sugiere="Una **interfaz** dice qué métodos tiene que tener quien la firme, sin decir cómo. `class Barco implements Nadador` firma el contrato y **tiene** que escribir `nadar()`. Un barco y un grifo no se parecen, pero los dos pueden nadar.",
              desafio="Completá la palabra con la que el Barco firma el contrato `Nadador`.",
              inicial='''
                  public class Pactos {
                      public static void main(String[] args) {
                          Nadador[] nadadores = {new Grifo(), new Barco()};
                          for (Nadador n : nadadores) {
                              System.out.println(n.nadar());
                          }
                      }
                  }

                  interface Nadador {
                      String nadar();
                  }

                  class Grifo implements Nadador {
                      public String nadar() { return "El grifo nada con las alas plegadas"; }
                  }

                  class Barco ___ Nadador {
                      public String nadar() { return "El barco flota y avanza"; }
                  }
              ''',
              solucion='''
                  public class Pactos {
                      public static void main(String[] args) {
                          Nadador[] nadadores = {new Grifo(), new Barco()};
                          for (Nadador n : nadadores) {
                              System.out.println(n.nadar());
                          }
                      }
                  }

                  interface Nadador {
                      String nadar();
                  }

                  class Grifo implements Nadador {
                      public String nadar() { return "El grifo nada con las alas plegadas"; }
                  }

                  class Barco implements Nadador {
                      public String nadar() { return "El barco flota y avanza"; }
                  }
              ''',
              al_superar="Un grifo y un barco, en el mismo array, porque los dos cumplen el contrato. —La herencia dice qué **sos** —dice Kaffa—. Una interfaz dice qué **sabés hacer**.",
              imagen=["La Sala de los Pactos: pergaminos firmados colgando de las paredes, con sellos de cera.",
                      "Kaffa (el Arquitecto Imperial) con su taza de café; Zed mirando su ganzúa inútil.",
                      "Un grifo y un pequeño barco dibujados en el mismo pergamino «Nadador»."]),
            m(id="R02-N07-P2", titulo="Todos los contratos que quieras",
              lugar="La Sala de los Pactos", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Varias interfaces | class Grifo implements Volador, Nadador · se heredan de UNA clase, pero se firman muchas interfaces",
              recompensa="xp 15, oro 15",
              escena="""
                  El grifo firmó dos pergaminos: el de volar y el de nadar. —Moldes padre hay uno solo —dice Kaffa—. Contratos, todos los que puedas cumplir.
              """,
              sugiere="Una clase puede implementar **varias** interfaces, separadas por coma: `implements Volador, Nadador`. Tiene que escribir los métodos de todas.",
              desafio="Completá la segunda interfaz que firma el Grifo.",
              inicial='''
                  public class DosContratos {
                      public static void main(String[] args) {
                          Grifo g = new Grifo();
                          System.out.println(g.volar());
                          System.out.println(g.nadar());
                          Volador v = g;
                          Nadador n = g;
                          System.out.println("Vuela y nada: " + (v == n));
                      }
                  }

                  interface Volador {
                      String volar();
                  }

                  interface Nadador {
                      String nadar();
                  }

                  class Grifo implements Volador, ___ {
                      public String volar() { return "El grifo sube en espiral"; }

                      public String nadar() { return "El grifo nada con las alas plegadas"; }
                  }
              ''',
              solucion='''
                  public class DosContratos {
                      public static void main(String[] args) {
                          Grifo g = new Grifo();
                          System.out.println(g.volar());
                          System.out.println(g.nadar());
                          Volador v = g;
                          Nadador n = g;
                          System.out.println("Vuela y nada: " + (v == n));
                      }
                  }

                  interface Volador {
                      String volar();
                  }

                  interface Nadador {
                      String nadar();
                  }

                  class Grifo implements Volador, Nadador {
                      public String volar() { return "El grifo sube en espiral"; }

                      public String nadar() { return "El grifo nada con las alas plegadas"; }
                  }
              ''',
              al_superar="El mismo grifo, visto como Volador o como Nadador: `true`, es uno solo. Nadia anota en su libreta: «contratos: muchos. Padres: uno».",
              imagen=["Un grifo dorado con dos pergaminos firmados atados al cuello: «Volador» y «Nadador».",
                      "Nadia anotando en su libreta."]),
            m(id="R02-N07-P3", titulo="La cláusula por defecto",
              lugar="La Sala de los Pactos", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Método default | default String bucear() { … } en la interfaz · ya viene escrito · quien firma puede usarlo o sobrescribirlo",
              recompensa="xp 15, oro 15",
              escena="""
                  Al contrato de nadar le agregaron una cláusula nueva: **bucear**. Los que ya lo habían firmado no quieren reescribir nada. —Entonces la cláusula viene **con su respuesta por defecto** —dice Kaffa—. El que quiera, la cambia.
              """,
              sugiere="Un método `default` en una interfaz tiene cuerpo: todas las clases que la firman lo reciben hecho. Una clase puede sobrescribirlo si necesita otra cosa.",
              desafio="Completá la palabra que le da cuerpo a `bucear` dentro de la interfaz.",
              inicial='''
                  public class Clausula {
                      public static void main(String[] args) {
                          Nadador[] nadadores = {new Grifo(), new Submarino()};
                          for (Nadador n : nadadores) {
                              System.out.println(n.bucear());
                          }
                      }
                  }

                  interface Nadador {
                      String nadar();

                      ___ String bucear() {
                          return "se sumerge un poco y sube";
                      }
                  }

                  class Grifo implements Nadador {
                      public String nadar() { return "nada"; }
                  }

                  class Submarino implements Nadador {
                      public String nadar() { return "avanza"; }

                      @Override
                      public String bucear() { return "baja hasta el fondo del río"; }
                  }
              ''',
              solucion='''
                  public class Clausula {
                      public static void main(String[] args) {
                          Nadador[] nadadores = {new Grifo(), new Submarino()};
                          for (Nadador n : nadadores) {
                              System.out.println(n.bucear());
                          }
                      }
                  }

                  interface Nadador {
                      String nadar();

                      default String bucear() {
                          return "se sumerge un poco y sube";
                      }
                  }

                  class Grifo implements Nadador {
                      public String nadar() { return "nada"; }
                  }

                  class Submarino implements Nadador {
                      public String nadar() { return "avanza"; }

                      @Override
                      public String bucear() { return "baja hasta el fondo del río"; }
                  }
              ''',
              al_superar="El grifo bucea un poco y sube; el submarino llega al fondo. Nadie tuvo que reescribir el contrato viejo.",
              imagen=["Un pergamino de contrato con una cláusula nueva agregada abajo, brillando.",
                      "Un grifo sumergiéndose apenas en el río; a su lado, un submarino de bronce bajando al fondo."]),
            m(id="R02-N07-P4", titulo="La ganzúa echa dientes",
              lugar="La Sala de los Pactos", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Comparable | class Llave implements Comparable<Llave> · int compareTo(Llave otra) · Arrays.sort(llaves) usa ese orden",
              recompensa="xp 15, oro 20",
              escena="""
                  El último pergamino dice: «quien firme este se compromete a **poder ser comparado**». Kaffa le pide a Zed que ordene las llaves del Imperio por cantidad de dientes. Zed apoya su ganzúa en la mesa, al lado de las llaves, y le parece que se mueve.
              """,
              sugiere="`Comparable<Llave>` obliga a escribir `compareTo(Llave otra)`: negativo si esta va antes, positivo si va después, 0 si da igual. Para enteros: `Integer.compare(dientes, otra.dientes)`. Con eso, `Arrays.sort(llaves)` sabe ordenarlas.",
              desafio="Completá el `return` de `compareTo`: de menos dientes a más.",
              inicial='''
                  import java.util.Arrays;

                  public class Llaves {
                      public static void main(String[] args) {
                          Llave[] llaves = {new Llave("la del Archivo", 7), new Llave("la de la Torre", 12), new Llave("la ganzúa de Zed", 1), new Llave("la del Cofre", 4)};
                          Arrays.sort(llaves);
                          for (Llave l : llaves) {
                              System.out.println(l.dientes + " dientes: " + l.nombre);
                          }
                      }
                  }

                  class Llave implements Comparable<Llave> {
                      String nombre;
                      int dientes;

                      Llave(String nombre, int dientes) {
                          this.nombre = nombre;
                          this.dientes = dientes;
                      }

                      @Override
                      public int compareTo(Llave otra) {
                          return ___;
                      }
                  }
              ''',
              solucion='''
                  import java.util.Arrays;

                  public class Llaves {
                      public static void main(String[] args) {
                          Llave[] llaves = {new Llave("la del Archivo", 7), new Llave("la de la Torre", 12), new Llave("la ganzúa de Zed", 1), new Llave("la del Cofre", 4)};
                          Arrays.sort(llaves);
                          for (Llave l : llaves) {
                              System.out.println(l.dientes + " dientes: " + l.nombre);
                          }
                      }
                  }

                  class Llave implements Comparable<Llave> {
                      String nombre;
                      int dientes;

                      Llave(String nombre, int dientes) {
                          this.nombre = nombre;
                          this.dientes = dientes;
                      }

                      @Override
                      public int compareTo(Llave otra) {
                          return Integer.compare(dientes, otra.dientes);
                      }
                  }
              ''',
              al_superar="""
                  Las llaves quedan en fila. La ganzúa de Zed, primera, con un solo diente… y de repente, con un chasquido, le **crece un segundo diente**, como a una llave de verdad. Kaffa sonríe detrás de su taza. —Firmaste tu primer contrato.
                  En el taller de al lado, un aprendiz intenta que un caballero herede de una armadura, de una espada y de un caballo a la vez.
              """,
              imagen=["Cuatro llaves ordenadas sobre una mesa, de menos a más dientes; la ganzúa de Zed, primera, echando un segundo diente con un destello.",
                      "Kaffa sonriendo detrás de su taza; Zed mirando la ganzúa, asombrado."]),
        ],
    },
    {
        "titulo": "R02-N08 · Composición, agregación y delegación",
        "misiones": [
            m(id="R02-N08-P1", titulo="Un caballero no es una armadura",
              lugar="El taller de armaduras", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="Tiene un | class Caballero { Armadura armadura; } · un atributo que es otro objeto · «tiene un», no «es un»",
              recompensa="xp 10, oro 10",
              escena="""
                  En el taller de armaduras, un aprendiz intenta que `Caballero` herede de `Armadura`. —Un caballero no **es** una armadura —le dice la Maestra—. **Tiene** una.
              """,
              sugiere="Cuando algo **tiene** otra cosa, la parte va como **atributo**: `Armadura armadura;`. Para usarla, se pasa por el atributo: `armadura.defensa`.",
              desafio="Completá el tipo del atributo `armadura`.",
              inicial='''
                  public class Taller {
                      public static void main(String[] args) {
                          Caballero c = new Caballero("Teo", new Armadura("de placas", 8));
                          System.out.println(c.nombre + " lleva armadura " + c.armadura.tipo + " (defensa " + c.armadura.defensa + ")");
                      }
                  }

                  class Armadura {
                      String tipo;
                      int defensa;

                      Armadura(String tipo, int defensa) {
                          this.tipo = tipo;
                          this.defensa = defensa;
                      }
                  }

                  class Caballero {
                      String nombre;
                      ___ armadura;

                      Caballero(String nombre, Armadura armadura) {
                          this.nombre = nombre;
                          this.armadura = armadura;
                      }
                  }
              ''',
              solucion='''
                  public class Taller {
                      public static void main(String[] args) {
                          Caballero c = new Caballero("Teo", new Armadura("de placas", 8));
                          System.out.println(c.nombre + " lleva armadura " + c.armadura.tipo + " (defensa " + c.armadura.defensa + ")");
                      }
                  }

                  class Armadura {
                      String tipo;
                      int defensa;

                      Armadura(String tipo, int defensa) {
                          this.tipo = tipo;
                          this.defensa = defensa;
                      }
                  }

                  class Caballero {
                      String nombre;
                      Armadura armadura;

                      Caballero(String nombre, Armadura armadura) {
                          this.nombre = nombre;
                          this.armadura = armadura;
                      }
                  }
              ''',
              al_superar="Teo sale del taller con su armadura puesta, no convertido en una. —Ahora sí tiene sentido —dice el aprendiz, aliviado.",
              imagen=["El taller de armaduras: yunques, chispas y armaduras colgadas.",
                      "Teo (el recluta de la lanza) probándose una armadura de placas; la Maestra ajustándole una correa."]),
            m(id="R02-N08-P2", titulo="Nace y muere con él",
              lugar="El taller de armaduras", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="Composición | la parte se crea ADENTRO del todo (new en el constructor) · nace y muere con él · nadie más la tiene",
              recompensa="xp 15, oro 15",
              escena="""
                  Las armaduras del taller se forjan **a medida**: cada una se hace para un caballero y no le sirve a nadie más. Cuando el caballero se retira, su armadura se funde.
              """,
              sugiere="En la **composición**, el todo crea su parte: el constructor del `Caballero` hace `this.armadura = new Armadura(...)`. Nadie de afuera tiene esa armadura: vive y muere con el caballero.",
              desafio="Completá la línea que forja la armadura adentro del constructor, con la defensa que recibe.",
              inicial='''
                  public class AMedida {
                      public static void main(String[] args) {
                          Caballero a = new Caballero("Teo", 8);
                          Caballero b = new Caballero("Lía", 10);
                          System.out.println(a.nombre + ": defensa " + a.armadura.defensa);
                          System.out.println(b.nombre + ": defensa " + b.armadura.defensa);
                          System.out.println("¿Comparten armadura? " + (a.armadura == b.armadura));
                      }
                  }

                  class Armadura {
                      int defensa;

                      Armadura(int defensa) { this.defensa = defensa; }
                  }

                  class Caballero {
                      String nombre;
                      Armadura armadura;

                      Caballero(String nombre, int defensa) {
                          this.nombre = nombre;
                          ___;
                      }
                  }
              ''',
              solucion='''
                  public class AMedida {
                      public static void main(String[] args) {
                          Caballero a = new Caballero("Teo", 8);
                          Caballero b = new Caballero("Lía", 10);
                          System.out.println(a.nombre + ": defensa " + a.armadura.defensa);
                          System.out.println(b.nombre + ": defensa " + b.armadura.defensa);
                          System.out.println("¿Comparten armadura? " + (a.armadura == b.armadura));
                      }
                  }

                  class Armadura {
                      int defensa;

                      Armadura(int defensa) { this.defensa = defensa; }
                  }

                  class Caballero {
                      String nombre;
                      Armadura armadura;

                      Caballero(String nombre, int defensa) {
                          this.nombre = nombre;
                          this.armadura = new Armadura(defensa);
                      }
                  }
              ''',
              al_superar="Cada caballero con su armadura, forjada para él. «¿Comparten armadura? false.» —Como los sellos de la Aduana —dice Nadia—: cada uno, el suyo.",
              imagen=["Dos armaduras forjándose a la vez en dos yunques, cada una con el nombre grabado: «Teo» y «Lía».",
                      "Chispas doradas; Nadia observando con la libreta."]),
            m(id="R02-N08-P3", titulo="El caballo sigue",
              lugar="Las caballerizas de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              criatura="troll",
              carta="Agregación | la parte existe por su cuenta y se pasa al todo · si el caballero cae (null), el caballo sigue existiendo",
              recompensa="xp 15, oro 15",
              escena="""
                  En las caballerizas, el caballo **Rayo** ya existía antes de que Teo llegara. Teo lo monta, pero no es suyo para siempre. Un **troll** espera que, si Teo cae, Rayo desaparezca con él.
              """,
              sugiere="En la **agregación**, la parte se crea **afuera** y se le pasa al todo: `new Caballero(\"Teo\", rayo)`. Si después `teo = null`, el objeto caballo sigue vivo mientras alguien lo señale (la variable `rayo`).",
              desafio="Completá el `new Caballero` pasándole el caballo que ya existe.",
              inicial='''
                  public class Caballerizas {
                      public static void main(String[] args) {
                          Caballo rayo = new Caballo("Rayo");
                          Caballero teo = new Caballero("Teo", ___);
                          System.out.println(teo.nombre + " monta a " + teo.caballo.nombre);
                          teo = null;
                          System.out.println("Teo cayó. " + rayo.nombre + " sigue en las caballerizas");
                      }
                  }

                  class Caballo {
                      String nombre;

                      Caballo(String nombre) { this.nombre = nombre; }
                  }

                  class Caballero {
                      String nombre;
                      Caballo caballo;

                      Caballero(String nombre, Caballo caballo) {
                          this.nombre = nombre;
                          this.caballo = caballo;
                      }
                  }
              ''',
              solucion='''
                  public class Caballerizas {
                      public static void main(String[] args) {
                          Caballo rayo = new Caballo("Rayo");
                          Caballero teo = new Caballero("Teo", rayo);
                          System.out.println(teo.nombre + " monta a " + teo.caballo.nombre);
                          teo = null;
                          System.out.println("Teo cayó. " + rayo.nombre + " sigue en las caballerizas");
                      }
                  }

                  class Caballo {
                      String nombre;

                      Caballo(String nombre) { this.nombre = nombre; }
                  }

                  class Caballero {
                      String nombre;
                      Caballo caballo;

                      Caballero(String nombre, Caballo caballo) {
                          this.nombre = nombre;
                          this.caballo = caballo;
                      }
                  }
              ''',
              al_superar="Teo se cae del caballo en la práctica (de verdad), y Rayo sigue ahí, comiendo pasto. El troll se va sin nada.",
              imagen=["Rayo, un caballo gris, comiendo tranquilo en las caballerizas.",
                      "Teo sentado en el piso, riéndose; un troll yéndose decepcionado."]),
            m(id="R02-N08-P4", titulo="Que lo haga la armadura",
              lugar="El taller de armaduras", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="Delegación | el todo le pasa el trabajo a su parte · int recibir(int golpe) { return armadura.absorber(golpe); }",
              recompensa="xp 15, oro 15",
              escena="""
                  Cuando a un caballero le pegan, no es él quien frena el golpe: es su armadura. —El caballero **delega** —dice la Maestra—. No sabe de placas ni de remaches. Le pasa el golpe a quien sabe.
              """,
              sugiere="**Delegar** es que un método del todo llame a un método de la parte: `return armadura.absorber(golpe);`. El caballero no repite la cuenta: la hace la armadura.",
              desafio="Completá el `return` de `recibir`: que la armadura absorba el golpe.",
              inicial='''
                  public class Delegar {
                      public static void main(String[] args) {
                          Caballero teo = new Caballero("Teo", new Armadura(8));
                          System.out.println("Golpe de 20, daño: " + teo.recibir(20));
                          System.out.println("Golpe de 5, daño: " + teo.recibir(5));
                      }
                  }

                  class Armadura {
                      int defensa;

                      Armadura(int defensa) { this.defensa = defensa; }

                      int absorber(int golpe) {
                          return Math.max(0, golpe - defensa);
                      }
                  }

                  class Caballero {
                      String nombre;
                      Armadura armadura;

                      Caballero(String nombre, Armadura armadura) {
                          this.nombre = nombre;
                          this.armadura = armadura;
                      }

                      int recibir(int golpe) {
                          return ___;
                      }
                  }
              ''',
              solucion='''
                  public class Delegar {
                      public static void main(String[] args) {
                          Caballero teo = new Caballero("Teo", new Armadura(8));
                          System.out.println("Golpe de 20, daño: " + teo.recibir(20));
                          System.out.println("Golpe de 5, daño: " + teo.recibir(5));
                      }
                  }

                  class Armadura {
                      int defensa;

                      Armadura(int defensa) { this.defensa = defensa; }

                      int absorber(int golpe) {
                          return Math.max(0, golpe - defensa);
                      }
                  }

                  class Caballero {
                      String nombre;
                      Armadura armadura;

                      Caballero(String nombre, Armadura armadura) {
                          this.nombre = nombre;
                          this.armadura = armadura;
                      }

                      int recibir(int golpe) {
                          return armadura.absorber(golpe);
                      }
                  }
              ''',
              al_superar="""
                  Doce de daño en lugar de veinte, y el golpe chico ni se siente. Teo le agradece a su armadura con una palmadita.
                  En el archivo de la Academia, alguien escribió en la pizarra «arquero», «ARQERO» y «ARQUERO». Nadie sabe cuántos arqueros hay.
              """,
              imagen=["Una espada golpeando una armadura de placas: el golpe se frena en un destello.",
                      "Teo dándole una palmadita a su armadura."]),
        ],
    },
    {
        "titulo": "R02-N09 · enum y record",
        "misiones": [
            m(id="R02-N09-P1", titulo="Tres palabras para lo mismo",
              lugar="El archivo de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              criatura="goblin",
              carta="enum | enum Clase { INFANTE, ARQUERO, JINETE } · una lista cerrada de valores · Clase.values() los recorre",
              recompensa="xp 10, oro 10",
              escena="""
                  En la pizarra del archivo dice «arquero», «ARQERO» y «ARQUERO». Un **goblin** escribió el del medio. —Cuando los valores posibles son una lista cerrada —dice la Maestra—, no los escribas como texto. Declaralos.
              """,
              sugiere="Un `enum` es un tipo con una lista **cerrada** de valores: `enum Clase { INFANTE, ARQUERO, JINETE }`. No hay forma de escribir `ARQERO`: no compila. `Clase.values()` devuelve todos, en orden.",
              desafio="Recorré todos los valores del enum con el método que los devuelve.",
              inicial='''
                  public class Pizarra {
                      public static void main(String[] args) {
                          Clase deMira = Clase.ARQUERO;
                          System.out.println("Mira es " + deMira);
                          for (Clase c : Clase.___()) {
                              System.out.println("- " + c);
                          }
                      }
                  }

                  enum Clase {
                      INFANTE, ARQUERO, JINETE
                  }
              ''',
              solucion='''
                  public class Pizarra {
                      public static void main(String[] args) {
                          Clase deMira = Clase.ARQUERO;
                          System.out.println("Mira es " + deMira);
                          for (Clase c : Clase.values()) {
                              System.out.println("- " + c);
                          }
                      }
                  }

                  enum Clase {
                      INFANTE, ARQUERO, JINETE
                  }
              ''',
              al_superar="Tres clases, escritas una sola vez. La Maestra borra la pizarra entera y el goblin se queda sin tiza.",
              imagen=["Una pizarra con «arquero», «ARQERO» y «ARQUERO» tachados y, encima, un cartel de bronce: INFANTE · ARQUERO · JINETE.",
                      "Un goblin con una tiza rota en la mano."]),
            m(id="R02-N09-P2", titulo="La paga de cada clase",
              lugar="El archivo de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="enum con datos | INFANTE(10), ARQUERO(12) · un atributo final y un constructor · cada valor lleva lo suyo",
              recompensa="xp 15, oro 15",
              escena="""
                  Cada clase de soldado cobra distinto. En lugar de una tabla aparte, la Maestra quiere que **cada valor del enum lleve su paga**.
              """,
              sugiere="Un `enum` puede tener atributos, constructor y métodos: `INFANTE(10)` llama al constructor con 10. El constructor guarda el dato: `this.paga = paga;`.",
              desafio="Completá el constructor del enum: guardá la paga.",
              inicial='''
                  public class Paga {
                      public static void main(String[] args) {
                          for (Clase c : Clase.values()) {
                              System.out.println(c + ": " + c.getPaga() + " denarios");
                          }
                      }
                  }

                  enum Clase {
                      INFANTE(10), ARQUERO(12), JINETE(20);

                      private final int paga;

                      Clase(int paga) {
                          ___;
                      }

                      int getPaga() {
                          return paga;
                      }
                  }
              ''',
              solucion='''
                  public class Paga {
                      public static void main(String[] args) {
                          for (Clase c : Clase.values()) {
                              System.out.println(c + ": " + c.getPaga() + " denarios");
                          }
                      }
                  }

                  enum Clase {
                      INFANTE(10), ARQUERO(12), JINETE(20);

                      private final int paga;

                      Clase(int paga) {
                          this.paga = paga;
                      }

                      int getPaga() {
                          return paga;
                      }
                  }
              ''',
              al_superar="Cada clase con su paga, sin tablas sueltas. —Los jinetes cobran el doble —protesta Teo—. —Tienen que alimentar al caballo —le contesta Nadia.",
              imagen=["Tres placas de bronce: INFANTE 10, ARQUERO 12, JINETE 20, con monedas apiladas al lado.",
                      "Teo protestando; Nadia señalando a Rayo, el caballo."]),
            m(id="R02-N09-P3", titulo="Una orden para cada clase",
              lugar="El patio de armas de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="enum en switch | switch (c) { case INFANTE -> …; case ARQUERO -> …; } · sin escribir Clase. adelante · con los tres casos no hace falta default",
              recompensa="xp 15, oro 15",
              escena="""
                  En el patio, la Maestra da órdenes distintas según la clase. Zed le arma la tabla de órdenes con un `switch`.
              """,
              sugiere="Un `enum` va perfecto en un `switch`: cada `case` es un valor (`case ARQUERO ->`). Si el `switch` devuelve un valor y cubre **todos** los valores del enum, no hace falta `default`.",
              desafio="Completá el caso que falta: los arqueros «disparan».",
              inicial='''
                  public class Ordenes {
                      static String orden(Clase c) {
                          return switch (c) {
                              case INFANTE -> "avanzan";
                              case ___ -> "disparan";
                              case JINETE -> "flanquean";
                          };
                      }

                      public static void main(String[] args) {
                          for (Clase c : Clase.values()) {
                              System.out.println(c + ": " + orden(c));
                          }
                      }
                  }

                  enum Clase {
                      INFANTE, ARQUERO, JINETE
                  }
              ''',
              solucion='''
                  public class Ordenes {
                      static String orden(Clase c) {
                          return switch (c) {
                              case INFANTE -> "avanzan";
                              case ARQUERO -> "disparan";
                              case JINETE -> "flanquean";
                          };
                      }

                      public static void main(String[] args) {
                          for (Clase c : Clase.values()) {
                              System.out.println(c + ": " + orden(c));
                          }
                      }
                  }

                  enum Clase {
                      INFANTE, ARQUERO, JINETE
                  }
              ''',
              al_superar="Las tres órdenes, sin una sola palabra mal escrita. Si mañana se agrega una clase nueva, el compilador va a avisar que falta su caso.",
              imagen=["El patio de armas: infantes avanzando, arqueros disparando y jinetes rodeando por el costado.",
                      "La Maestra con un cartel de órdenes; Zed a su lado."]),
            m(id="R02-N09-P4", titulo="La ficha que no cambia",
              lugar="El archivo de la Academia", personajes="Zed, Gheco, Nadia, la Maestra de Moldes",
              carta="record | record Recluta(String nombre, Clase clase) {} · constructor, getters nombre(), equals y toString hechos · no se puede cambiar",
              recompensa="xp 15, oro 15",
              escena="""
                  Las fichas de los reclutas son solo datos: nombre y clase. Escribirlas como clase lleva cincuenta líneas. —Para un paquete de datos que no cambia —dice la Maestra—, un **record**.
              """,
              sugiere="`record Recluta(String nombre, Clase clase) {}` crea el constructor, un método para leer cada dato (`r.nombre()`, sin `get`), `equals` y `toString`, y no deja cambiar nada.",
              desafio="Completá el método que lee el nombre del recluta.",
              inicial='''
                  public class Fichas {
                      public static void main(String[] args) {
                          Recluta a = new Recluta("Mira", Clase.ARQUERO);
                          Recluta b = new Recluta("Mira", Clase.ARQUERO);
                          System.out.println(a);
                          System.out.println("Nombre: " + a.___());
                          System.out.println("Iguales: " + a.equals(b));
                      }
                  }

                  enum Clase {
                      INFANTE, ARQUERO, JINETE
                  }

                  record Recluta(String nombre, Clase clase) {
                  }
              ''',
              solucion='''
                  public class Fichas {
                      public static void main(String[] args) {
                          Recluta a = new Recluta("Mira", Clase.ARQUERO);
                          Recluta b = new Recluta("Mira", Clase.ARQUERO);
                          System.out.println(a);
                          System.out.println("Nombre: " + a.nombre());
                          System.out.println("Iguales: " + a.equals(b));
                      }
                  }

                  enum Clase {
                      INFANTE, ARQUERO, JINETE
                  }

                  record Recluta(String nombre, Clase clase) {
                  }
              ''',
              al_superar="""
                  Una línea en lugar de cincuenta, con `toString` y `equals` incluidos. La Maestra archiva las fichas.
                  Esa tarde, Kaffa los cita en la biblioteca. Desenrolla un plano lleno de cajas y flechas, sin una sola línea de código.
              """,
              imagen=["Una ficha de bronce que se escribe sola: «Recluta[nombre=Mira, clase=ARQUERO]».",
                      "Al fondo, la puerta de la biblioteca de la Academia, con Kaffa esperando con un plano enrollado."]),
        ],
    },
    {
        "titulo": "R02-N10 · Diagramas UML",
        "misiones": [
            m(id="R02-N10-P1", titulo="Leer una caja",
              lugar="La biblioteca de la Academia", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Clase en UML | caja con tres partes: nombre, atributos y métodos · - es private · + es public · nombre: Tipo",
              recompensa="xp 10, oro 10",
              escena="""
                  Kaffa señala la primera caja del plano:
                  `Viajero` / `- nombre: String` / `- edad: int` / `+ getNombre(): String`.
                  —Antes de levantar un edificio, lo dibujo —dice—. Este idioma lo lee cualquier arquitecta del Imperio. El **menos** es privado; el **más**, público.
              """,
              sugiere="En una caja de UML, `- nombre: String` es un atributo **private** de tipo `String`, y `+ getNombre(): String` es un método **public** que devuelve un `String`. Primero el nombre, después los dos puntos y el tipo.",
              desafio="Pasá la caja a código: completá la visibilidad de los dos atributos.",
              inicial='''
                  public class Caja {
                      public static void main(String[] args) {
                          Viajero v = new Viajero("Zed", 19);
                          System.out.println("Nombre: " + v.getNombre());
                      }
                  }

                  class Viajero {
                      ___ String nombre;
                      ___ int edad;

                      Viajero(String nombre, int edad) {
                          this.nombre = nombre;
                          this.edad = edad;
                      }

                      public String getNombre() {
                          return nombre;
                      }
                  }
              ''',
              solucion='''
                  public class Caja {
                      public static void main(String[] args) {
                          Viajero v = new Viajero("Zed", 19);
                          System.out.println("Nombre: " + v.getNombre());
                      }
                  }

                  class Viajero {
                      private String nombre;
                      private int edad;

                      Viajero(String nombre, int edad) {
                          this.nombre = nombre;
                          this.edad = edad;
                      }

                      public String getNombre() {
                          return nombre;
                      }
                  }
              ''',
              al_superar="La caja del plano y el código dicen lo mismo. —Ahora, al revés —dice Kaffa—: cuando leas código, imaginate la caja.",
              imagen=["Un plano de pergamino desenrollado sobre una mesa con una caja dibujada: «Viajero», sus atributos con «-» y su método con «+».",
                      "Kaffa señalando con una pluma; Zed y Nadia inclinados sobre el plano."]),
            m(id="R02-N10-P2", titulo="Las dos flechas huecas",
              lugar="La biblioteca de la Academia", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Herencia y realización | flecha llena con triángulo hueco: extends · flecha punteada con triángulo hueco: implements («interface»)",
              recompensa="xp 15, oro 15",
              escena="""
                  En el plano hay dos flechas con punta de triángulo hueco. Una, de línea **llena**: de `Arquero` a `Personaje`. La otra, **punteada**: de `Grifo` a `«interface» Volador`.
              """,
              sugiere="Triángulo hueco con línea llena: **herencia** (`extends`). Triángulo hueco con línea punteada: **realización**, una clase que implementa una interfaz (`implements`).",
              desafio="Completá las dos palabras según las flechas del plano.",
              inicial='''
                  public class Flechas {
                      public static void main(String[] args) {
                          Personaje p = new Arquero("Mira");
                          Volador v = new Grifo();
                          System.out.println(p.describir());
                          System.out.println(v.volar());
                      }
                  }

                  class Personaje {
                      String nombre;

                      Personaje(String nombre) { this.nombre = nombre; }

                      String describir() { return nombre + ", un personaje"; }
                  }

                  class Arquero ___ Personaje {
                      Arquero(String nombre) { super(nombre); }

                      @Override
                      String describir() { return nombre + ", arquera"; }
                  }

                  interface Volador {
                      String volar();
                  }

                  class Grifo ___ Volador {
                      public String volar() { return "El grifo vuela"; }
                  }
              ''',
              solucion='''
                  public class Flechas {
                      public static void main(String[] args) {
                          Personaje p = new Arquero("Mira");
                          Volador v = new Grifo();
                          System.out.println(p.describir());
                          System.out.println(v.volar());
                      }
                  }

                  class Personaje {
                      String nombre;

                      Personaje(String nombre) { this.nombre = nombre; }

                      String describir() { return nombre + ", un personaje"; }
                  }

                  class Arquero extends Personaje {
                      Arquero(String nombre) { super(nombre); }

                      @Override
                      String describir() { return nombre + ", arquera"; }
                  }

                  interface Volador {
                      String volar();
                  }

                  class Grifo implements Volador {
                      public String volar() { return "El grifo vuela"; }
                  }
              ''',
              al_superar="Las dos flechas, traducidas. —Línea llena, lo que sos; punteada, lo que prometiste —resume Nadia, y lo anota así en la libreta.",
              imagen=["Dos flechas dibujadas en el plano: una de línea llena con triángulo hueco y otra punteada, con el «interface» escrito arriba.",
                      "Nadia anotando el resumen en su libreta."]),
            m(id="R02-N10-P3", titulo="Rombo negro, rombo blanco",
              lugar="La biblioteca de la Academia", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="ogro",
              carta="Composición y agregación en UML | rombo negro (◆): composición, la parte se crea adentro · rombo blanco (◇): agregación, la parte viene de afuera",
              recompensa="xp 15, oro 15",
              escena="""
                  En el plano, `Caballero ◆—— Armadura` y `Caballero ◇—— Caballo`. Un aprendiz los pasó a código al revés: el caballo nace con el caballero y la armadura viene de afuera. Compila y corre… pero no es el diseño. Un **ogro** lo aplaude.
              """,
              sugiere="Rombo **negro** (composición): el caballero crea la armadura en su constructor (`new Armadura(...)`). Rombo **blanco** (agregación): el caballo existe antes y se pasa como parámetro.",
              desafio="Completá el constructor según el plano: la armadura se crea adentro y el caballo llega de afuera.",
              inicial='''
                  public class Rombos {
                      public static void main(String[] args) {
                          Caballo rayo = new Caballo("Rayo");
                          Caballero teo = new Caballero("Teo", 8, rayo);
                          System.out.println(teo.nombre + ": armadura " + teo.armadura.defensa + ", caballo " + teo.caballo.nombre);
                          System.out.println("Es el mismo caballo: " + (teo.caballo == rayo));
                      }
                  }

                  class Armadura {
                      int defensa;

                      Armadura(int defensa) { this.defensa = defensa; }
                  }

                  class Caballo {
                      String nombre;

                      Caballo(String nombre) { this.nombre = nombre; }
                  }

                  class Caballero {
                      String nombre;
                      Armadura armadura;
                      Caballo caballo;

                      Caballero(String nombre, int defensa, Caballo caballo) {
                          this.nombre = nombre;
                          this.armadura = ___;
                          this.caballo = ___;
                      }
                  }
              ''',
              solucion='''
                  public class Rombos {
                      public static void main(String[] args) {
                          Caballo rayo = new Caballo("Rayo");
                          Caballero teo = new Caballero("Teo", 8, rayo);
                          System.out.println(teo.nombre + ": armadura " + teo.armadura.defensa + ", caballo " + teo.caballo.nombre);
                          System.out.println("Es el mismo caballo: " + (teo.caballo == rayo));
                      }
                  }

                  class Armadura {
                      int defensa;

                      Armadura(int defensa) { this.defensa = defensa; }
                  }

                  class Caballo {
                      String nombre;

                      Caballo(String nombre) { this.nombre = nombre; }
                  }

                  class Caballero {
                      String nombre;
                      Armadura armadura;
                      Caballo caballo;

                      Caballero(String nombre, int defensa, Caballo caballo) {
                          this.nombre = nombre;
                          this.armadura = new Armadura(defensa);
                          this.caballo = caballo;
                      }
                  }
              ''',
              al_superar="El código y el plano coinciden: armadura a medida, Rayo prestado. El ogro deja de aplaudir: un programa que anda pero no respeta el diseño era su favorito.",
              imagen=["En el plano, un rombo negro hacia «Armadura» y un rombo blanco hacia «Caballo», con Teo dibujado en el centro.",
                      "Un ogro con las manos quietas, decepcionado."]),
            m(id="R02-N10-P4", titulo="Uno o más artesanos",
              lugar="La biblioteca de la Academia", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Multiplicidad | 1 exactamente uno · 0..1 uno o ninguno · * o 0..* muchos · 1..* al menos uno · en código, un array o una colección",
              recompensa="xp 15, oro 20",
              escena="""
                  Al pie del plano, `Gremio "1" ◇—— "1..*" Artesano`: cada gremio tiene **al menos un** artesano. —Los números de las puntas dicen **cuántos** —explica Kaffa—. Y un gremio vacío no es un gremio.
              """,
              sugiere="`1..*` del lado de `Artesano` significa que el gremio tiene **uno o más**: en código, un array `Artesano[] artesanos`. Para respetar el «al menos uno», el gremio pide un artesano al crearse.",
              desafio="Completá el método que cuenta los artesanos usando el largo del array.",
              inicial='''
                  public class Multiplicidad {
                      public static void main(String[] args) {
                          Artesano[] miembros = {new Artesano("la Maestra de Moldes"), new Artesano("Teo"), new Artesano("Zed")};
                          Gremio gremio = new Gremio("Gremio de los Moldes", miembros);
                          System.out.println(gremio.nombre + ": " + gremio.cantidad() + " artesanos");
                          System.out.println("El último en entrar: " + gremio.artesanos[gremio.cantidad() - 1].nombre);
                      }
                  }

                  class Artesano {
                      String nombre;

                      Artesano(String nombre) { this.nombre = nombre; }
                  }

                  class Gremio {
                      String nombre;
                      Artesano[] artesanos;

                      Gremio(String nombre, Artesano[] artesanos) {
                          this.nombre = nombre;
                          this.artesanos = artesanos;
                      }

                      int cantidad() {
                          return ___;
                      }
                  }
              ''',
              solucion='''
                  public class Multiplicidad {
                      public static void main(String[] args) {
                          Artesano[] miembros = {new Artesano("la Maestra de Moldes"), new Artesano("Teo"), new Artesano("Zed")};
                          Gremio gremio = new Gremio("Gremio de los Moldes", miembros);
                          System.out.println(gremio.nombre + ": " + gremio.cantidad() + " artesanos");
                          System.out.println("El último en entrar: " + gremio.artesanos[gremio.cantidad() - 1].nombre);
                      }
                  }

                  class Artesano {
                      String nombre;

                      Artesano(String nombre) { this.nombre = nombre; }
                  }

                  class Gremio {
                      String nombre;
                      Artesano[] artesanos;

                      Gremio(String nombre, Artesano[] artesanos) {
                          this.nombre = nombre;
                          this.artesanos = artesanos;
                      }

                      int cantidad() {
                          return artesanos.length;
                      }
                  }
              ''',
              al_superar="""
                  «El último en entrar: Zed.» Un ladrón en un gremio de artesanos. Kaffa enrolla el plano… y Zed ve, en una esquina, un molde que nadie terminó de dibujar, **firmado con el dibujo de un vitral**.
                  Desde el sótano de la Academia llega un rugido de tres voces distintas.
              """,
              imagen=["En la esquina del plano, una caja a medio dibujar con una firma pequeña: un vitral de colores.",
                      "Zed mirando la firma, con la llave del vitral en la otra mano; el piso de la biblioteca vibrando por un rugido."]),
        ],
    },
    {
        "titulo": "R02-N11 · Jefe: la Quimera de las Mil Herencias",
        "misiones": [
            m(id="R02-N11-P1", titulo="Qué es cada cabeza",
              lugar="El sótano de la Academia", personajes="Zed, Gheco, Nadia, Kaffa, la Maestra de Moldes",
              criatura="dragon",
              carta="Modelar lo que ES | una clase abstracta para lo común (Cabeza) · cada cabeza es un hijo que completa lo abstracto",
              recompensa="xp 20, oro 20",
              escena="""
                  En el sótano vive la **Quimera de las Mil Herencias**: alguien quiso que heredara de León, de Cabra y de Serpiente a la vez, y el molde se rompió. Ahora tiene tres cabezas, cada una con su elemento.
                  —No se la vence con un solo molde —dice Kaffa—. Se la vence **modelándola bien**: qué es, qué tiene, qué sabe hacer. Empezá por lo que **es**: cada cabeza es una Cabeza.
              """,
              sugiere="Lo que tienen todas las cabezas (nombre, vida y un ataque) va en la clase abstracta `Cabeza`. Cada cabeza concreta **extiende** a `Cabeza` y escribe su `atacar()`.",
              desafio="Completá el ataque de la cabeza de Serpiente: \"muerde con veneno\".",
              inicial='''
                  public class Quimera1 {
                      public static void main(String[] args) {
                          Cabeza[] cabezas = {new Leon(), new Cabra(), new Serpiente()};
                          for (Cabeza c : cabezas) {
                              System.out.println(c.nombre + " (" + c.vida + "): " + c.atacar());
                          }
                      }
                  }

                  abstract class Cabeza {
                      String nombre;
                      int vida;

                      Cabeza(String nombre, int vida) {
                          this.nombre = nombre;
                          this.vida = vida;
                      }

                      abstract String atacar();
                  }

                  class Leon extends Cabeza {
                      Leon() { super("León", 60); }

                      @Override
                      String atacar() { return "escupe fuego"; }
                  }

                  class Cabra extends Cabeza {
                      Cabra() { super("Cabra", 40); }

                      @Override
                      String atacar() { return "embiste con hielo"; }
                  }

                  class Serpiente extends Cabeza {
                      Serpiente() { super("Serpiente", 30); }

                      @Override
                      String atacar() { return ___; }
                  }
              ''',
              solucion='''
                  public class Quimera1 {
                      public static void main(String[] args) {
                          Cabeza[] cabezas = {new Leon(), new Cabra(), new Serpiente()};
                          for (Cabeza c : cabezas) {
                              System.out.println(c.nombre + " (" + c.vida + "): " + c.atacar());
                          }
                      }
                  }

                  abstract class Cabeza {
                      String nombre;
                      int vida;

                      Cabeza(String nombre, int vida) {
                          this.nombre = nombre;
                          this.vida = vida;
                      }

                      abstract String atacar();
                  }

                  class Leon extends Cabeza {
                      Leon() { super("León", 60); }

                      @Override
                      String atacar() { return "escupe fuego"; }
                  }

                  class Cabra extends Cabeza {
                      Cabra() { super("Cabra", 40); }

                      @Override
                      String atacar() { return "embiste con hielo"; }
                  }

                  class Serpiente extends Cabeza {
                      Serpiente() { super("Serpiente", 30); }

                      @Override
                      String atacar() { return "muerde con veneno"; }
                  }
              ''',
              al_superar="Fuego, hielo y veneno: tres cabezas, un solo molde abstracto. La Quimera ruge y cambia de forma, pero ahora Zed sabe qué es cada parte.",
              imagen=["La Quimera de las Mil Herencias: un cuerpo de bronce agrietado con tres cabezas, león de fuego, cabra de hielo y serpiente de veneno.",
                      "Zed, Nadia y Gheco frente a ella en un sótano lleno de moldes rotos; Kaffa y la Maestra atrás."]),
            m(id="R02-N11-P2", titulo="El golpe justo",
              lugar="El sótano de la Academia", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="enum y record juntos | enum Elemento { FUEGO, HIELO, VENENO } · record Golpe(int danio, Elemento elemento) · el switch decide",
              recompensa="xp 20, oro 20",
              escena="""
                  Cada cabeza es débil a un elemento: el León al hielo, la Cabra al fuego, la Serpiente al hielo también. Zed no puede improvisar los golpes: los tiene que **declarar**.
              """,
              sugiere="Los elementos son una lista cerrada: un `enum`. Un golpe es solo un paquete de datos: un `record`. La debilidad de cada cabeza se decide con un `switch` sobre el nombre.",
              desafio="Completá el caso de la Cabra: es débil al FUEGO.",
              inicial='''
                  public class Quimera2 {
                      static Elemento debilidad(String cabeza) {
                          return switch (cabeza) {
                              case "León" -> Elemento.HIELO;
                              case "Cabra" -> ___;
                              default -> Elemento.HIELO;
                          };
                      }

                      public static void main(String[] args) {
                          String[] cabezas = {"León", "Cabra", "Serpiente"};
                          for (String c : cabezas) {
                              Golpe g = new Golpe(25, debilidad(c));
                              System.out.println(c + ": " + g);
                          }
                      }
                  }

                  enum Elemento {
                      FUEGO, HIELO, VENENO
                  }

                  record Golpe(int danio, Elemento elemento) {
                  }
              ''',
              solucion='''
                  public class Quimera2 {
                      static Elemento debilidad(String cabeza) {
                          return switch (cabeza) {
                              case "León" -> Elemento.HIELO;
                              case "Cabra" -> Elemento.FUEGO;
                              default -> Elemento.HIELO;
                          };
                      }

                      public static void main(String[] args) {
                          String[] cabezas = {"León", "Cabra", "Serpiente"};
                          for (String c : cabezas) {
                              Golpe g = new Golpe(25, debilidad(c));
                              System.out.println(c + ": " + g);
                          }
                      }
                  }

                  enum Elemento {
                      FUEGO, HIELO, VENENO
                  }

                  record Golpe(int danio, Elemento elemento) {
                  }
              ''',
              al_superar="Tres golpes declarados, cada uno con su elemento. La Quimera retrocede: por primera vez, alguien la atacó con un plan.",
              imagen=["Tres esferas de luz flotando frente a Zed: dos de hielo (celestes) y una de fuego (naranja), cada una con una etiqueta.",
                      "La Quimera retrocediendo contra la pared del sótano."]),
            m(id="R02-N11-P3", titulo="Lo que tiene la Quimera",
              lugar="El sótano de la Academia", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Composición y delegación | la Quimera TIENE cabezas (un array) · su vida es la suma de las de sus cabezas · le delega a cada una",
              recompensa="xp 20, oro 25",
              escena="""
                  —La Quimera no **es** un león, ni una cabra, ni una serpiente —dice Kaffa—. **Tiene** tres cabezas. Ese fue el error del aprendiz. Su vida es la de sus cabezas, sumadas.
              """,
              sugiere="La `Quimera` tiene un array de `Cabeza` (composición). Para saber su vida total, recorre las cabezas y le **pregunta a cada una** su vida: `total += c.getVida();`.",
              desafio="Completá el acumulador: sumá la vida de cada cabeza.",
              inicial='''
                  public class Quimera3 {
                      public static void main(String[] args) {
                          Quimera q = new Quimera();
                          System.out.println("Vida de la Quimera: " + q.vidaTotal());
                          q.cabezas[2].recibir(30);
                          System.out.println("Después de golpear a la Serpiente: " + q.vidaTotal());
                      }
                  }

                  class Cabeza {
                      private String nombre;
                      private int vida;

                      Cabeza(String nombre, int vida) {
                          this.nombre = nombre;
                          this.vida = vida;
                      }

                      int getVida() { return vida; }

                      void recibir(int danio) { vida = Math.max(0, vida - danio); }
                  }

                  class Quimera {
                      Cabeza[] cabezas = {new Cabeza("León", 60), new Cabeza("Cabra", 40), new Cabeza("Serpiente", 30)};

                      int vidaTotal() {
                          int total = 0;
                          for (Cabeza c : cabezas) {
                              ___;
                          }
                          return total;
                      }
                  }
              ''',
              solucion='''
                  public class Quimera3 {
                      public static void main(String[] args) {
                          Quimera q = new Quimera();
                          System.out.println("Vida de la Quimera: " + q.vidaTotal());
                          q.cabezas[2].recibir(30);
                          System.out.println("Después de golpear a la Serpiente: " + q.vidaTotal());
                      }
                  }

                  class Cabeza {
                      private String nombre;
                      private int vida;

                      Cabeza(String nombre, int vida) {
                          this.nombre = nombre;
                          this.vida = vida;
                      }

                      int getVida() { return vida; }

                      void recibir(int danio) { vida = Math.max(0, vida - danio); }
                  }

                  class Quimera {
                      Cabeza[] cabezas = {new Cabeza("León", 60), new Cabeza("Cabra", 40), new Cabeza("Serpiente", 30)};

                      int vidaTotal() {
                          int total = 0;
                          for (Cabeza c : cabezas) {
                              total += c.getVida();
                          }
                          return total;
                      }
                  }
              ''',
              al_superar="De 130 a 100: la Serpiente cae y su cabeza se apaga. Quedan dos.",
              imagen=["La cabeza de serpiente de la Quimera apagándose, gris; las otras dos rugiendo.",
                      "Un contador de vida de bronce sobre la Quimera bajando de 130 a 100."]),
            m(id="R02-N11-P4", titulo="El combate se escribe solo",
              lugar="El sótano de la Academia", personajes="Zed, Gheco, Nadia, Kaffa, la Maestra de Moldes",
              carta="Todo junto | herencia, polimorfismo, composición, enum y record · si el diseño está bien, el combate es un bucle de cinco líneas",
              recompensa="xp 25, oro 30",
              item="Guantes del Artesano",
              escena="""
                  Quedan el León y la Cabra. —Si el diseño está bien —dice Kaffa—, el combate se escribe solo. Cada cabeza sabe su debilidad; vos solo tenés que **pegarle con lo que le duele**.
              """,
              sugiere="Cada `Cabeza` sabe su debilidad (`debilidad()`). Un golpe con ese elemento hace el **doble** de daño. En el bucle, armá el golpe con la debilidad de **esa** cabeza: `new Golpe(35, c.debilidad())`.",
              desafio="Completá el golpe: 35 de daño, con el elemento al que es débil cada cabeza.",
              inicial='''
                  public class Quimera4 {
                      public static void main(String[] args) {
                          Cabeza[] cabezas = {new Leon(), new Cabra()};
                          for (Cabeza c : cabezas) {
                              Golpe g = ___;
                              c.recibir(g);
                              System.out.println(c.nombre + " recibe " + g.elemento() + ": le queda " + c.vida);
                          }
                          System.out.println("La Quimera cae.");
                      }
                  }

                  enum Elemento {
                      FUEGO, HIELO, VENENO
                  }

                  record Golpe(int danio, Elemento elemento) {
                  }

                  abstract class Cabeza {
                      String nombre;
                      int vida;

                      Cabeza(String nombre, int vida) {
                          this.nombre = nombre;
                          this.vida = vida;
                      }

                      abstract Elemento debilidad();

                      void recibir(Golpe g) {
                          int danio = g.elemento() == debilidad() ? g.danio() * 2 : g.danio();
                          vida = Math.max(0, vida - danio);
                      }
                  }

                  class Leon extends Cabeza {
                      Leon() { super("León", 60); }

                      @Override
                      Elemento debilidad() { return Elemento.HIELO; }
                  }

                  class Cabra extends Cabeza {
                      Cabra() { super("Cabra", 40); }

                      @Override
                      Elemento debilidad() { return Elemento.FUEGO; }
                  }
              ''',
              solucion='''
                  public class Quimera4 {
                      public static void main(String[] args) {
                          Cabeza[] cabezas = {new Leon(), new Cabra()};
                          for (Cabeza c : cabezas) {
                              Golpe g = new Golpe(35, c.debilidad());
                              c.recibir(g);
                              System.out.println(c.nombre + " recibe " + g.elemento() + ": le queda " + c.vida);
                          }
                          System.out.println("La Quimera cae.");
                      }
                  }

                  enum Elemento {
                      FUEGO, HIELO, VENENO
                  }

                  record Golpe(int danio, Elemento elemento) {
                  }

                  abstract class Cabeza {
                      String nombre;
                      int vida;

                      Cabeza(String nombre, int vida) {
                          this.nombre = nombre;
                          this.vida = vida;
                      }

                      abstract Elemento debilidad();

                      void recibir(Golpe g) {
                          int danio = g.elemento() == debilidad() ? g.danio() * 2 : g.danio();
                          vida = Math.max(0, vida - danio);
                      }
                  }

                  class Leon extends Cabeza {
                      Leon() { super("León", 60); }

                      @Override
                      Elemento debilidad() { return Elemento.HIELO; }
                  }

                  class Cabra extends Cabeza {
                      Cabra() { super("Cabra", 40); }

                      @Override
                      Elemento debilidad() { return Elemento.FUEGO; }
                  }
              ''',
              al_superar="""
                  Hielo al León, fuego a la Cabra, y la Quimera cae. Del molde roto queda un par de **guantes de cuero y bronce**: la Maestra se los da a Zed. —Los **Guantes del Artesano**. Desde hoy sos aprendiz de la Academia.
                  Kaffa termina su café. —Los Archivos Imperiales guardan el registro de todos los que cruzaron. También el de alguien que llegó con un vitral.
              """,
              imagen=["La Quimera derrumbándose en el sótano entre moldes rotos, con las tres cabezas apagadas.",
                      "La Maestra de Moldes entregándole a Zed un par de guantes de cuero con remaches de bronce.",
                      "Kaffa con su taza; Nadia y Gheco celebrando atrás."]),
        ],
    },
]
