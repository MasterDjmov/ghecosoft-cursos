from genjava import m

ADUANA = "La Aduana del Compilador"
EJECUTAR = "Para ejecutarlo: con el **Ejecutor de Java** abierto en tu compu (*Herramientas → Ejecutor de Java*), tocá **Ejecutar**. Si no lo tenés, corrélo en tu compu o tu IDE y pegá la salida abajo."

NODOS = [
    {
        "titulo": "R00-N01 · Clase 0 · Hola, Java",
        "misiones": [
            m(id="R00-N01-P1", titulo="Declarar en la frontera",
              lugar="La fila de la Aduana del Compilador", personajes="Zed, Gheco, Nadia",
              carta="Mostrar texto | System.out.println(\"texto\"); · muestra y salta de línea · cada instrucción termina con ;",
              recompensa="xp 10",
              escena=f"""
                  Zed despierta en una fila larguísima frente a una muralla con vitrales dorados, con una llave de vidrio en la mano. Una aduanera de uniforme azul y rodete tirante le corta el paso: **Nadia**.
                  —Nombre y procedencia. Por escrito. En el Imperio, lo que no está declarado no existe.
                  Sobre el hombro de Zed aparece un gecko de luz con antiparras: **Gheco**. —Escribilo en el pergamino. Acá los pergaminos se **ejecutan**.
              """,
              sugiere="`System.out.println(\"…\");` muestra el texto entre comillas y salta a la línea siguiente. " + EJECUTAR,
              desafio="Completá la instrucción para declarar quién sos.",
              inicial='''
                  public class Declaracion {
                      public static void main(String[] args) {
                          System.out.___("Me llamo Zed y vengo del Puerto.");
                      }
                  }
              ''',
              solucion='''
                  public class Declaracion {
                      public static void main(String[] args) {
                          System.out.println("Me llamo Zed y vengo del Puerto.");
                      }
                  }
              ''',
              al_superar="Nadia lee la declaración, la sella y anota algo en su libreta. —Del Puerto. Ajá. —No suena a cumplido.",
              imagen=["La muralla del Imperio de las Clases de noche, con vitrales dorados encendidos y una fila de viajeros.",
                      "Nadia (uniforme azul de cuello alto, botones de bronce, rodete tirante, guantes blancos) le corta el paso a Zed.",
                      "Zed (pelo blanco plateado, visor rojo, campera negra con vivos rojos) sostiene una llave de plomo y vidrios de colores.",
                      "Gheco, gecko cian con antiparras, aparece sobre su hombro."]),
            m(id="R00-N01-P2", titulo="Todo en una línea",
              lugar="La fila de la Aduana del Compilador", personajes="Zed, Gheco, Nadia",
              carta="print o println | print no salta de línea · println sí · se pueden combinar",
              recompensa="xp 10",
              escena="—El formulario va en **una sola línea** —dice Nadia—: nombre, guion, oficio. Y la fecha abajo.",
              sugiere="`System.out.print(…)` muestra **sin** saltar de línea: lo siguiente sigue pegado. `println` salta al final.",
              desafio="Usá `print` para que nombre y oficio queden en la misma línea.",
              inicial='''
                  public class Formulario {
                      public static void main(String[] args) {
                          System.out.println("Zed");
                          System.out.println(" - ladrón de techos");
                          System.out.println("Llegada: hoy");
                      }
                  }
              ''',
              solucion='''
                  public class Formulario {
                      public static void main(String[] args) {
                          System.out.print("Zed");
                          System.out.println(" - ladrón de techos");
                          System.out.println("Llegada: hoy");
                      }
                  }
              ''',
              al_superar="Nadia levanta una ceja. —¿«Ladrón de techos»? Por lo menos es honesto. —Y lo anota igual.",
              imagen=["Un formulario de pergamino con tres renglones luminosos: los dos primeros unidos en uno.",
                      "Nadia, con la pluma en alto, mira a Zed con una ceja levantada."]),
            m(id="R00-N01-P3", titulo="El punto y coma olvidado",
              lugar="La fila de la Aduana del Compilador", personajes="Zed, Gheco, Nadia",
              criatura="slime",
              carta="Error de compilación | el compilador (javac) revisa ANTES de ejecutar · ';' expected: falta un punto y coma",
              recompensa="xp 10",
              escena="""
                  Delante de Zed, un mercader entrega su pergamino y se lo devuelven con una marca roja. Del pergamino gotea un **slime**.
                  —La Aduana es el **compilador** —dice Gheco—. Revisa todo antes de dejarlo pasar. Si falta un signo, no se ejecuta nada.
              """,
              sugiere="Un **error de compilación** aparece antes de ejecutar: el programa ni arranca. `';' expected` quiere decir que falta un punto y coma en esa línea.",
              desafio="Arreglá el pergamino del mercader para que la Aduana lo deje pasar.",
              inicial='''
                  public class Mercader {
                      public static void main(String[] args) {
                          System.out.println("Traigo tres barriles")
                          System.out.println("y ninguna mala intención");
                      }
                  }
              ''',
              solucion='''
                  public class Mercader {
                      public static void main(String[] args) {
                          System.out.println("Traigo tres barriles");
                          System.out.println("y ninguna mala intención");
                      }
                  }
              ''',
              al_superar="El slime se evapora. El mercader, agradecido, le guiña un ojo a Zed. Nadia, en cambio, no le saca los ojos de encima.",
              imagen=["Un pergamino con una marca roja en la línea 3, del que gotea un slime verde que se evapora.",
                      "Un mercader agradecido; Zed con el pergamino corregido."]),
            m(id="R00-N01-P4", titulo="Lo que explota adentro",
              lugar="La fila de la Aduana del Compilador", personajes="Zed, Gheco, Nadia",
              criatura="ogro",
              carta="Error de ejecución | compila, pero falla al correr · el stack trace dice la línea · dividir enteros por 0: ArithmeticException",
              recompensa="xp 10",
              escena="""
                  Zed intenta repartir el peaje entre los viajeros de su fila… que son cero. El pergamino **compila**, pero al ejecutarse explota con un mensaje largo.
                  —Eso es un **error de ejecución** —dice Gheco—. La Aduana no lo vio venir. Leé la línea que te marca.
              """,
              sugiere="Un **error de ejecución** pasa con el programa ya andando. El *stack trace* dice qué pasó (`ArithmeticException: / by zero`) y en qué línea. Dividir un entero por 0 lo provoca.",
              desafio="Que el peaje se reparta entre los 4 viajeros de la fila.",
              inicial='''
                  public class Peaje {
                      public static void main(String[] args) {
                          int peaje = 20;
                          int viajeros = 0;
                          System.out.println("Cada uno paga " + peaje / viajeros);
                      }
                  }
              ''',
              solucion='''
                  public class Peaje {
                      public static void main(String[] args) {
                          int peaje = 20;
                          int viajeros = 4;
                          System.out.println("Cada uno paga " + peaje / viajeros);
                      }
                  }
              ''',
              al_superar="Cinco denarios cada uno. La fila avanza y Zed ya está frente al portón.",
              imagen=["Un pergamino que explota en chispas rojas con el texto `/ by zero`.",
                      "Zed retrocede de un salto; Gheco se tapa los ojos."]),
            m(id="R00-N01-P5", titulo="Nada existe suelto",
              lugar="El portón de la Aduana", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="La anatomía | public class Nombre { … } · public static void main(String[] args) { … } · en Java todo vive en una clase",
              recompensa="xp 15",
              item="Llave del Vitral",
              escena="""
                  En el portón, un hombre alto con una taza de café mira el pergamino de Zed: **Kaffa**, el Arquitecto Imperial. Al pergamino le falta el comienzo.
                  —En el Imperio **nada existe suelto** —dice—. Cada instrucción vive en un método, y cada método, en una clase.
              """,
              sugiere="Todo programa de Java tiene una **clase** (`public class Nombre { … }`) y adentro el método **`main`**, donde empieza a ejecutarse. Las llaves `{ }` marcan dónde empieza y termina cada uno.",
              desafio="Escribí la línea que abre el método `main`.",
              inicial='''
                  public class Porton {
                      ___
                          System.out.println("Zed, del Puerto");
                          System.out.println("Declara: una llave de vidrio");
                      }
                  }
              ''',
              solucion='''
                  public class Porton {
                      public static void main(String[] args) {
                          System.out.println("Zed, del Puerto");
                          System.out.println("Declara: una llave de vidrio");
                      }
                  }
              ''',
              al_superar="""
                  Kaffa toma la llave de vidrio, la mira contra la luz de los vitrales y se la devuelve, muy despacio.
                  —Pasás la Aduana como todos, Zed: **declarando**. Nadia te va a acompañar. —Ella no parece contenta. Él tampoco.
                  La **Llave del Vitral** va a tu mochila.
              """,
              imagen=["Kaffa (alto, de túnica de arquitecto, con una taza de café) mira una llave de plomo y vidrios de colores contra la luz de un vitral dorado.",
                      "Zed y Nadia, uno al lado del otro, mirándose de reojo.",
                      "El portón de la Aduana empieza a abrirse."]),
        ],
    },
    {
        "titulo": "R01-N01 · Variables, tipos y conversiones",
        "misiones": [
            m(id="R01-N01-P1", titulo="Cada cajón con su etiqueta",
              lugar=ADUANA, personajes="Zed, Gheco, Nadia",
              carta="Variables y tipos | int edad = 18; · double peso = 2.5; · String nombre = \"Zed\"; · boolean libre = true;",
              recompensa="xp 10, oro 10",
              escena="""
                  Pasado el portón hay una balanza con cajones etiquetados: *enteros*, *decimales*, *texto*, *verdadero o falso*. Zed quiere meter «un poco de todo» en el mismo cajón.
                  —Cada cajón guarda **un solo tipo** —dice Nadia—. Declaralo.
              """,
              sugiere="Una variable se declara con su **tipo** y su nombre: `int` (enteros), `double` (decimales), `String` (texto, con mayúscula) y `boolean` (`true` o `false`).",
              desafio="Completá el tipo de cada cajón.",
              inicial='''
                  public class Cajones {
                      public static void main(String[] args) {
                          ___ barriles = 3;
                          ___ peso = 12.5;
                          ___ propietario = "Zed";
                          ___ declarado = true;
                          System.out.println(barriles + " barriles de " + peso + " kg, de " + propietario + ": " + declarado);
                      }
                  }
              ''',
              solucion='''
                  public class Cajones {
                      public static void main(String[] args) {
                          int barriles = 3;
                          double peso = 12.5;
                          String propietario = "Zed";
                          boolean declarado = true;
                          System.out.println(barriles + " barriles de " + peso + " kg, de " + propietario + ": " + declarado);
                      }
                  }
              ''',
              al_superar="La balanza se equilibra y cada cajón se cierra con un clic. Nadia tilda algo en la libreta.",
              imagen=["Una balanza de bronce con cuatro cajones etiquetados: enteros, decimales, texto, verdadero o falso.",
                      "Zed acomoda paquetes en cada cajón; Nadia controla con la libreta."]),
            m(id="R01-N01-P2", titulo="Lo que no cambia",
              lugar=ADUANA, personajes="Zed, Gheco, Nadia",
              carta="Constantes | final double PEAJE = 2.5; · no se puede reasignar · nombre en MAYÚSCULAS",
              recompensa="xp 10, oro 10",
              escena="Zed «ajusta» el valor del peaje en su cuenta, para pagar menos. Nadia ni lo mira: —El peaje es **constante**. Escribilo así y el compilador no te va a dejar tocarlo.",
              sugiere="Con `final` una variable se vuelve **constante**: si alguien intenta cambiarla, no compila. Por costumbre se escribe en MAYÚSCULAS.",
              desafio="Sacá la línea que intenta cambiar la constante, para que compile.",
              inicial='''
                  public class Constante {
                      public static void main(String[] args) {
                          final int PEAJE = 5;
                          int carros = 4;
                          PEAJE = 1;
                          System.out.println("Total: " + PEAJE * carros + " denarios");
                      }
                  }
              ''',
              solucion='''
                  public class Constante {
                      public static void main(String[] args) {
                          final int PEAJE = 5;
                          int carros = 4;
                          System.out.println("Total: " + PEAJE * carros + " denarios");
                      }
                  }
              ''',
              al_superar="Veinte denarios. Zed paga, de mala gana. —Por lo menos es la misma regla para todos —murmura Gheco.",
              imagen=["Un cartel de piedra tallada con el peaje: «5», con un candado de bronce.",
                      "Zed pagando monedas de mala gana; Nadia extiende la mano."]),
            m(id="R01-N01-P3", titulo="Medio kilo no entra",
              lugar=ADUANA, personajes="Zed, Gheco, Nadia",
              criatura="goblin",
              carta="Casting | int n = (int) 3.99; → 3 (corta, no redondea) · de double a int hay que pedirlo",
              recompensa="xp 15, oro 15",
              escena="""
                  Zed intenta guardar 7,8 kilos de harina en el cajón de los enteros. No compila, y de entre los sacos salta un **goblin**.
                  —Los goblins nacen de los tipos que no encajan —dice Gheco—. Si querés pasar un decimal a entero, **pedilo**.
              """,
              sugiere="Un `double` no entra solo en un `int`: hay que **convertirlo** con `(int)`. Ojo: **corta** los decimales, no redondea. Para redondear está `Math.round`.",
              desafio="Convertí el peso a entero (cortando) para el cajón de enteros.",
              inicial='''
                  public class Casting {
                      public static void main(String[] args) {
                          double harina = 7.8;
                          int cajon = harina;
                          System.out.println("En el cajón entran " + cajon + " kg");
                          System.out.println("Redondeado serían " + Math.round(harina));
                      }
                  }
              ''',
              solucion='''
                  public class Casting {
                      public static void main(String[] args) {
                          double harina = 7.8;
                          int cajon = (int) harina;
                          System.out.println("En el cajón entran " + cajon + " kg");
                          System.out.println("Redondeado serían " + Math.round(harina));
                      }
                  }
              ''',
              al_superar="Siete kilos al cajón; los ochocientos gramos sobrantes se los queda el goblin y huye. Nadia anota: «pérdida: 0,8 kg».",
              imagen=["Un goblin flaco huye con un saquito de harina entre los cajones.",
                      "Un cajón de enteros con un 7 grabado; un 0,8 escapándose en el aire."]),
            m(id="R01-N01-P4", titulo="El reparto que no da",
              lugar=ADUANA, personajes="Zed, Gheco, Nadia",
              criatura="ogro",
              carta="División entera | 7 / 2 → 3 (dos int) · 7 / 2.0 → 3.5 · si uno es double, el resultado es double",
              recompensa="xp 15, oro 15",
              escena="Hay que repartir 7 denarios de multa entre 2 viajeros. La cuenta da 3 cada uno… y se perdió un denario. Ningún error: es un **ogro**.",
              sugiere="Entre dos `int`, `/` da la **división entera**: tira los decimales. Si uno de los dos es `double` (por ejemplo `2.0`), el resultado tiene decimales.",
              desafio="Hacé que el reparto dé con decimales.",
              inicial='''
                  public class Reparto {
                      public static void main(String[] args) {
                          int multa = 7;
                          System.out.println("Cada uno paga " + multa / 2);
                      }
                  }
              ''',
              solucion='''
                  public class Reparto {
                      public static void main(String[] args) {
                          int multa = 7;
                          System.out.println("Cada uno paga " + multa / 2.0);
                      }
                  }
              ''',
              al_superar="Tres y medio cada uno: el denario perdido aparece. —Ningún error y todo mal —dice Gheco—. Así son los ogros.",
              imagen=["Siete monedas que se reparten en dos montones de tres y media; media moneda partida brilla en el medio.",
                      "Un ogro chiquito que se escabulle detrás de la balanza."]),
        ],
    },
    {
        "titulo": "R01-N02 · Operadores y expresiones",
        "misiones": [
            m(id="R01-N02-P1", titulo="Cuántos carros completos",
              lugar="El patio de la Aduana", personajes="Zed, Gheco, Nadia",
              carta="/ y % | 17 / 5 → 3 (cuántas veces entra) · 17 % 5 → 2 (lo que sobra)",
              recompensa="xp 10, oro 10",
              escena="En el patio hay 17 barriles y los carros llevan 5 cada uno. Dos guardias discuten cuántos carros salen y cuántos barriles quedan. Nadia le pasa la cuenta a Zed.",
              sugiere="Con enteros, `/` dice **cuántas veces entra** y `%` (el resto) dice **lo que sobra**.",
              desafio="Completá con el operador del resto.",
              inicial='''
                  public class Carros {
                      public static void main(String[] args) {
                          int barriles = 17;
                          int porCarro = 5;
                          System.out.println("Carros llenos: " + barriles / porCarro);
                          System.out.println("Sobran: " + barriles ___ porCarro);
                      }
                  }
              ''',
              solucion='''
                  public class Carros {
                      public static void main(String[] args) {
                          int barriles = 17;
                          int porCarro = 5;
                          System.out.println("Carros llenos: " + barriles / porCarro);
                          System.out.println("Sobran: " + barriles % porCarro);
                      }
                  }
              ''',
              al_superar="Tres carros y dos barriles sueltos. Los guardias se callan. Uno le hace un gesto a Zed: no está mal, para un colado.",
              imagen=["El patio de la Aduana: tres carros cargados y dos barriles sueltos.",
                      "Dos guardias que dejan de discutir; Zed con los brazos cruzados, satisfecho."]),
            m(id="R01-N02-P2", titulo="Sumar sobre lo que hay",
              lugar="El patio de la Aduana", personajes="Zed, Gheco, Nadia",
              carta="Asignación compuesta | x += 3 · x -= 2 · x *= 2 · x++ suma uno",
              recompensa="xp 10, oro 10",
              escena="—Contá los carros que van pasando —dice Nadia—. Uno por uno. Y al final, cada carro paga el doble por ser feriado.",
              sugiere="`carros++` suma uno. `total += 5` es `total = total + 5`; también existen `-=`, `*=` y `/=`.",
              desafio="Completá las tres cuentas con atajos.",
              inicial='''
                  public class Conteo {
                      public static void main(String[] args) {
                          int carros = 0;
                          carros___;
                          carros___;
                          carros___;
                          int peaje = carros * 5;
                          peaje ___ 2;
                          System.out.println(carros + " carros pagan " + peaje);
                      }
                  }
              ''',
              solucion='''
                  public class Conteo {
                      public static void main(String[] args) {
                          int carros = 0;
                          carros++;
                          carros++;
                          carros++;
                          int peaje = carros * 5;
                          peaje *= 2;
                          System.out.println(carros + " carros pagan " + peaje);
                      }
                  }
              ''',
              al_superar="Treinta denarios de feriado. Nadia los guarda en la caja fuerte… y mira a Zed para ver dónde tiene las manos.",
              imagen=["Una caja fuerte de la Aduana con un contador de carros de bronce que marca 3.",
                      "Nadia guardando monedas mientras vigila a Zed de reojo."]),
            m(id="R01-N02-P3", titulo="¿Puede pasar?",
              lugar="El patio de la Aduana", personajes="Zed, Gheco, Nadia",
              carta="Lógicos | && (y) · || (o) · ! (no) · dan true o false",
              recompensa="xp 10, oro 10",
              escena="La regla del portón: pasa quien **tiene sello y pagó**, o quien es **guardia**. Zed tiene sello, no pagó y no es guardia, pero dice que debería pasar.",
              sugiere="`&&` es «y» (las dos cosas), `||` es «o» (alguna de las dos) y `!` niega. Combinadas dan `true` o `false`.",
              desafio="Escribí la regla del portón con `&&` y `||`.",
              inicial='''
                  public class Porton {
                      public static void main(String[] args) {
                          boolean tieneSello = true;
                          boolean pago = false;
                          boolean esGuardia = false;
                          boolean pasa = ___;
                          System.out.println("¿Zed pasa? " + pasa);
                      }
                  }
              ''',
              solucion='''
                  public class Porton {
                      public static void main(String[] args) {
                          boolean tieneSello = true;
                          boolean pago = false;
                          boolean esGuardia = false;
                          boolean pasa = (tieneSello && pago) || esGuardia;
                          System.out.println("¿Zed pasa? " + pasa);
                      }
                  }
              ''',
              al_superar="`false`. Zed paga, refunfuñando. —La regla no tiene otra puerta —dice Nadia, y por primera vez casi se ríe.",
              imagen=["Un portón con dos candados de luz: «sello» encendido y «pago» apagado.",
                      "Zed busca una rendija en el portón; Nadia, apoyada en la pared, casi sonríe."]),
            m(id="R01-N02-P4", titulo="Primero lo que va primero",
              lugar="El patio de la Aduana", personajes="Zed, Gheco, Nadia",
              criatura="ogro",
              carta="Precedencia | * y / antes que + y - · los paréntesis mandan · 2 + 3 * 4 → 14",
              recompensa="xp 15, oro 15",
              escena="Cada carro paga 3 denarios, más 10 de la caravana entera, y todo eso por 2 porque es feriado. Un guardia hizo la cuenta y le dio 16. Debería ser 32. No hay error: un **ogro**.",
              sugiere="Java multiplica y divide **antes** de sumar y restar. Si querés otro orden, usá **paréntesis**.",
              desafio="Poné los paréntesis para que la cuenta dé lo que tiene que dar.",
              inicial='''
                  public class Feriado {
                      public static void main(String[] args) {
                          int carros = 2;
                          int total = carros * 3 + 10 * 2;
                          System.out.println("La caravana paga " + total);
                      }
                  }
              ''',
              solucion='''
                  public class Feriado {
                      public static void main(String[] args) {
                          int carros = 2;
                          int total = (carros * 3 + 10) * 2;
                          System.out.println("La caravana paga " + total);
                      }
                  }
              ''',
              al_superar="Treinta y dos. Los dos guardias que discutían se dan la mano. —El orden decide quién paga de más —dice Zed, y Nadia lo anota en su libreta como si fuera una regla.",
              imagen=["Una pizarra con la cuenta: los paréntesis brillan en verde.",
                      "Dos guardias dándose la mano; Nadia anota en su libreta."]),
        ],
    },
    {
        "titulo": "R01-N03 · Textos: String, equals y printf",
        "misiones": [
            m(id="R01-N03-P1", titulo="Los nombres torcidos",
              lugar="La oficina de sellos de la Aduana", personajes="Zed, Gheco, Nadia, el Escriba Jefe",
              carta="Métodos de String | .trim() saca espacios · .toUpperCase() · .length() · .charAt(0)",
              recompensa="xp 10, oro 10",
              escena="En la oficina de sellos, el Escriba Jefe tiene los ojos rojos de copiar nombres con espacios de más y en minúsculas. —Arreglámelos —le pide a Zed—, que yo ya no veo.",
              sugiere="Un `String` sabe hacer cosas: `.trim()` saca los espacios de los costados, `.toUpperCase()` lo pasa a mayúsculas y `.length()` dice cuántas letras tiene.",
              desafio="Limpiá el nombre y pasalo a mayúsculas.",
              inicial='''
                  public class Nombres {
                      public static void main(String[] args) {
                          String crudo = "   nadia   ";
                          String limpio = crudo.___.___;
                          System.out.println("[" + limpio + "] tiene " + limpio.length() + " letras");
                      }
                  }
              ''',
              solucion='''
                  public class Nombres {
                      public static void main(String[] args) {
                          String crudo = "   nadia   ";
                          String limpio = crudo.trim().toUpperCase();
                          System.out.println("[" + limpio + "] tiene " + limpio.length() + " letras");
                      }
                  }
              ''',
              al_superar="«NADIA», sin un espacio de más. Nadia, que miraba por encima del hombro, carraspea. —Está bien escrito. Por una vez.",
              imagen=["Una oficina tapada de pergaminos; el Escriba Jefe, ojeroso, con anteojos en la punta de la nariz.",
                      "Un pergamino donde «   nadia   » se convierte en «NADIA»."]),
            m(id="R01-N03-P2", titulo="El sello falsificado",
              lugar="La oficina de sellos de la Aduana", personajes="Zed, Gheco, Nadia, el Escriba Jefe",
              criatura="ogro",
              carta="== contra equals | == pregunta si es el MISMO objeto · .equals() compara el texto · para textos, siempre equals",
              recompensa="xp 15, oro 15",
              escena="""
                  Zed copia un sello que dice exactamente lo mismo que el original: «APROBADO». La Aduana lo compara… y dice que **no** es igual.
                  —Dos textos iguales no siempre son **el mismo** texto —dice Gheco—. Ese es el ogro preferido del Imperio.
              """,
              sugiere="Con textos, `==` pregunta si son **el mismo objeto**, no si dicen lo mismo, y a veces da `false` aunque el texto sea igual. Para comparar el contenido se usa `.equals()`.",
              desafio="Compará el contenido de los dos sellos.",
              inicial='''
                  public class Sello {
                      public static void main(String[] args) {
                          String original = "APROBADO";
                          String copia = new String("APROBADO");
                          System.out.println("¿Mismo objeto? " + (original == copia));
                          System.out.println("¿Mismo texto? " + ___);
                      }
                  }
              ''',
              solucion='''
                  public class Sello {
                      public static void main(String[] args) {
                          String original = "APROBADO";
                          String copia = new String("APROBADO");
                          System.out.println("¿Mismo objeto? " + (original == copia));
                          System.out.println("¿Mismo texto? " + original.equals(copia));
                      }
                  }
              ''',
              al_superar="«Mismo objeto: false. Mismo texto: true.» El Escriba Jefe se ríe. —¡Así me engañaron cien veces! —Zed no dice que él también pensaba engañarlo.",
              imagen=["Dos sellos idénticos «APROBADO» sobre la mesa; entre ellos, un `==` tachado y un `.equals()` brillando.",
                      "El Escriba Jefe riéndose; Zed silba mirando al techo."]),
            m(id="R01-N03-P3", titulo="La lista de una sola tirada",
              lugar="La oficina de sellos de la Aduana", personajes="Zed, Gheco, Nadia, el Escriba Jefe",
              carta="StringBuilder | sb.append(\"…\") agrega · sb.toString() da el texto · para armar textos de a pedazos",
              recompensa="xp 10, oro 10",
              escena="El Escriba Jefe quiere la lista de los viajeros de hoy en una sola línea, separados por guiones. Pegar pedazos con `+` lo vuelve loco: cada `+` arma un texto nuevo.",
              sugiere="`StringBuilder` arma un texto de a pedazos: `append` agrega al final y `toString()` devuelve el texto armado.",
              desafio="Agregá a Nadia y al mercader con `append`, como está hecho con Zed.",
              inicial='''
                  public class Lista {
                      public static void main(String[] args) {
                          StringBuilder sb = new StringBuilder();
                          sb.append("Zed").append(" - ");
                          sb.___("Nadia").___(" - ");
                          sb.___("un mercader");
                          System.out.println(sb.toString());
                      }
                  }
              ''',
              solucion='''
                  public class Lista {
                      public static void main(String[] args) {
                          StringBuilder sb = new StringBuilder();
                          sb.append("Zed").append(" - ");
                          sb.append("Nadia").append(" - ");
                          sb.append("un mercader");
                          System.out.println(sb.toString());
                      }
                  }
              ''',
              al_superar="La lista sale de un tirón. —Nadia no es una viajera —protesta ella. —Hoy sí —dice Zed—: viaja conmigo.",
              imagen=["Una tira de pergamino que se arma sola, nombre por nombre, con guiones de luz.",
                      "Nadia, ofendida, con los brazos en jarra; Zed sonriendo torcido."]),
            m(id="R01-N03-P4", titulo="La tabla de tarifas",
              lugar="La oficina de sellos de la Aduana", personajes="Zed, Gheco, Nadia, el Escriba Jefe",
              carta="printf | System.out.printf(Locale.US, \"%-8s %6.2f%n\", nombre, precio) · %s texto · %d entero · %.2f decimales · %n salto",
              recompensa="xp 15, oro 15",
              escena="—La tabla de tarifas tiene que quedar **prolija** —pide el Escriba—: el nombre a la izquierda y el precio con dos decimales, alineado.",
              sugiere="`printf` usa un **formato**: `%s` para textos, `%d` para enteros, `%.2f` para decimales con 2 cifras, `%n` para saltar de línea. Un número antes (`%-8s`, `%6.2f`) fija el ancho. Con `Locale.US`, el decimal es un punto en cualquier compu.",
              desafio="Completá el formato del precio: ancho 6 y 2 decimales.",
              inicial='''
                  import java.util.Locale;

                  public class Tarifas {
                      public static void main(String[] args) {
                          String formato = "%-8s ___%n";
                          System.out.printf(Locale.US, formato, "Barril", 2.5);
                          System.out.printf(Locale.US, formato, "Caballo", 12.0);
                          System.out.printf(Locale.US, formato, "Carta", 0.75);
                      }
                  }
              ''',
              solucion='''
                  import java.util.Locale;

                  public class Tarifas {
                      public static void main(String[] args) {
                          String formato = "%-8s %6.2f%n";
                          System.out.printf(Locale.US, formato, "Barril", 2.5);
                          System.out.printf(Locale.US, formato, "Caballo", 12.0);
                          System.out.printf(Locale.US, formato, "Carta", 0.75);
                      }
                  }
              ''',
              al_superar="La tabla queda perfecta, con los números alineados como soldados. El Escriba Jefe la cuelga en la puerta. En la ventanilla de al lado, alguien empieza a hacer preguntas.",
              imagen=["Una tabla de tarifas tallada en bronce, con precios perfectamente alineados.",
                      "El Escriba Jefe la cuelga en la puerta de la oficina."]),
        ],
    },
    {
        "titulo": "R01-N04 · Leer del teclado: Scanner, Math y Random",
        "misiones": [
            m(id="R01-N04-P1", titulo="El interrogatorio",
              lugar="La ventanilla de la Aduana", personajes="Zed, Gheco, Nadia",
              carta="Scanner | Scanner sc = new Scanner(System.in); · sc.nextLine() lee una línea · import java.util.Scanner;",
              recompensa="xp 10, oro 10",
              escena="En la ventanilla, Nadia ya no lee pergaminos: **pregunta**. —Ahora lo escribís vos —le dice a Zed—. Que el programa pregunte el nombre y salude.",
              sugiere="`Scanner` lee lo que se escribe en el teclado. Se crea con `new Scanner(System.in)` y `nextLine()` lee una línea entera. Hay que importarlo: `import java.util.Scanner;`. Acá la **Entrada** ya viene escrita: es lo que «tipearía» el viajero.",
              desafio="Leé el nombre con `nextLine`.",
              inicial='''
                  import java.util.Scanner;

                  public class Ventanilla {
                      public static void main(String[] args) {
                          Scanner sc = new Scanner(System.in);
                          System.out.print("Nombre: ");
                          String nombre = sc.___;
                          System.out.println();
                          System.out.println("Bienvenido al Imperio, " + nombre);
                      }
                  }
              ''',
              solucion='''
                  import java.util.Scanner;

                  public class Ventanilla {
                      public static void main(String[] args) {
                          Scanner sc = new Scanner(System.in);
                          System.out.print("Nombre: ");
                          String nombre = sc.nextLine();
                          System.out.println();
                          System.out.println("Bienvenido al Imperio, " + nombre);
                      }
                  }
              ''',
              entrada="Baldo\n",
              al_superar="«Bienvenido al Imperio, Baldo.» El mercader de la fila, un hombrecito de orejas puntiagudas, se va contento. —Ese no es de acá —murmura Gheco.",
              imagen=["La ventanilla de la Aduana: Nadia del otro lado del vidrio con su libreta.",
                      "Un mercader de orejas puntiagudas y antiparras (Baldo, de paso por el Imperio) recibe su sello contento."]),
            m(id="R01-N04-P2", titulo="El salto de línea perdido",
              lugar="La ventanilla de la Aduana", personajes="Zed, Gheco, Nadia",
              criatura="esqueleto",
              carta="nextInt + nextLine | nextInt() deja el Enter en la fila · un sc.nextLine() de más lo saca",
              recompensa="xp 15, oro 15",
              escena="Ahora la ventanilla pregunta la edad (un número) y después el oficio. Pero el oficio sale **vacío**, como si el viajero no hubiera dicho nada.",
              sugiere="`nextInt()` lee el número pero **deja el Enter** esperando. El `nextLine()` que sigue se lleva ese Enter vacío. Solución: un `sc.nextLine();` extra justo después de `nextInt()`.",
              desafio="Agregá la línea que se lleva el Enter que quedó.",
              inicial='''
                  import java.util.Scanner;

                  public class Edad {
                      public static void main(String[] args) {
                          Scanner sc = new Scanner(System.in);
                          int edad = sc.nextInt();
                          String oficio = sc.nextLine();
                          System.out.println("Edad: " + edad);
                          System.out.println("Oficio: [" + oficio + "]");
                      }
                  }
              ''',
              solucion='''
                  import java.util.Scanner;

                  public class Edad {
                      public static void main(String[] args) {
                          Scanner sc = new Scanner(System.in);
                          int edad = sc.nextInt();
                          sc.nextLine();
                          String oficio = sc.nextLine();
                          System.out.println("Edad: " + edad);
                          System.out.println("Oficio: [" + oficio + "]");
                      }
                  }
              ''',
              entrada="18\nladrón de techos\n",
              al_superar="«Oficio: ladrón de techos.» Nadia levanta la vista. —¿Pusiste eso en un formulario oficial? —Es lo que dijo el viajero —responde Zed, inocente.",
              imagen=["Un formulario donde el casillero «Oficio» pasa de vacío a lleno.",
                      "Nadia, incrédula, mira el formulario; Zed sonríe torcido."]),
            m(id="R01-N04-P3", titulo="La tablilla de fórmulas",
              lugar="La ventanilla de la Aduana", personajes="Zed, Gheco, Nadia",
              carta="Math | Math.max(a, b) · Math.pow(b, e) · Math.sqrt(x) · Math.abs(x) · Math.round(x)",
              recompensa="xp 10, oro 10",
              escena="Para tasar un terreno del cuartel, Nadia usa una **tablilla de fórmulas**: el lado de un terreno cuadrado a partir de su superficie, y cuál de dos ofertas es mayor.",
              sugiere="`Math` ya trae fórmulas listas: `Math.sqrt(x)` (raíz cuadrada), `Math.pow(base, exponente)`, `Math.max(a, b)`, `Math.abs(x)`.",
              desafio="Calculá el lado con la raíz cuadrada.",
              inicial='''
                  public class Terreno {
                      public static void main(String[] args) {
                          double superficie = 144;
                          double lado = ___;
                          System.out.println("Lado: " + lado);
                          System.out.println("Mejor oferta: " + Math.max(300, 450));
                          System.out.println("2 a la 10: " + Math.pow(2, 10));
                      }
                  }
              ''',
              solucion='''
                  public class Terreno {
                      public static void main(String[] args) {
                          double superficie = 144;
                          double lado = Math.sqrt(superficie);
                          System.out.println("Lado: " + lado);
                          System.out.println("Mejor oferta: " + Math.max(300, 450));
                          System.out.println("2 a la 10: " + Math.pow(2, 10));
                      }
                  }
              ''',
              al_superar="Doce de lado. Nadia guarda la tablilla y, sin darse cuenta, le presta a Zed su pluma.",
              imagen=["Una tablilla de bronce con fórmulas grabadas que se encienden: raíz, potencia, máximo.",
                      "Nadia le pasa su pluma a Zed sin mirarlo."]),
            m(id="R01-N04-P4", titulo="Los dados del tahúr",
              lugar="La ventanilla de la Aduana", personajes="Zed, Gheco, Nadia",
              carta="Random | Random r = new Random(semilla); · r.nextInt(6) + 1 → de 1 a 6 · con la misma semilla, siempre lo mismo",
              recompensa="xp 15, oro 15",
              escena="""
                  Un tahúr en la fila le ofrece a Zed un juego de dados. Zed, que de trampas sabe, sospecha: los dados salen siempre igual.
                  —Es un azar con **semilla** —dice Gheco—. Misma semilla, mismos números. Los dados del tahúr están cargados.
              """,
              sugiere="`new Random(42)` crea un generador con **semilla**: con la misma semilla da siempre la misma secuencia (sirve para probar). `r.nextInt(6)` da de 0 a 5; sumándole 1, de 1 a 6.",
              desafio="Tirá tres dados de 1 a 6.",
              inicial='''
                  import java.util.Random;

                  public class Dados {
                      public static void main(String[] args) {
                          Random r = new Random(42);
                          int primera = ___;
                          int segunda = ___;
                          int tercera = ___;
                          System.out.println("Tiradas: " + primera + ", " + segunda + " y " + tercera);
                      }
                  }
              ''',
              solucion='''
                  import java.util.Random;

                  public class Dados {
                      public static void main(String[] args) {
                          Random r = new Random(42);
                          int primera = r.nextInt(6) + 1;
                          int segunda = r.nextInt(6) + 1;
                          int tercera = r.nextInt(6) + 1;
                          System.out.println("Tiradas: " + primera + ", " + segunda + " y " + tercera);
                      }
                  }
              ''',
              al_superar="Zed adivina cada tirada antes de que caiga. El tahúr se va de la fila, furioso. Nadia anota: «tahúr: denunciado». —Por una vez, una trampa sirvió para algo —le dice a Zed.",
              imagen=["Tres dados de luz en el aire, cada uno con su número antes de caer.",
                      "Un tahúr furioso que se va; Nadia anota en su libreta."]),
        ],
    },
    {
        "titulo": "R01-N05 · Decisiones: if y switch",
        "misiones": [
            m(id="R01-N05-P1", titulo="Los tres portones",
              lugar="Los tres portones de la Aduana", personajes="Zed, Gheco, Nadia",
              carta="if / else if / else | se revisa en orden · entra al PRIMERO que se cumple · else: si ninguno",
              recompensa="xp 10, oro 10",
              escena="Frente a la Aduana hay tres portones: mercaderes, soldados y peregrinos. Nadia le da a Zed el puesto del guardia: —Mandá a cada uno al suyo.",
              sugiere="`if (condición) { … } else if (otra) { … } else { … }` revisa **en orden** y entra solo en el primero que se cumple. El `else` es para todos los demás.",
              desafio="Completá la condición del portón de los soldados (el que llega ahora es un soldado).",
              inicial='''
                  public class Portones {
                      public static void main(String[] args) {
                          String v = "soldado";
                          if (v.equals("mercader")) {
                              System.out.println(v + ": portón del oro");
                          } else if (___) {
                              System.out.println(v + ": portón de hierro");
                          } else {
                              System.out.println(v + ": portón de piedra");
                          }
                      }
                  }
              ''',
              solucion='''
                  public class Portones {
                      public static void main(String[] args) {
                          String v = "soldado";
                          if (v.equals("mercader")) {
                              System.out.println(v + ": portón del oro");
                          } else if (v.equals("soldado")) {
                              System.out.println(v + ": portón de hierro");
                          } else {
                              System.out.println(v + ": portón de piedra");
                          }
                      }
                  }
              ''',
              al_superar="Cada viajero a su portón, sin una equivocación. —Un programa que decide es un guardia —dice Gheco—. Y vos sos un buen guardia, para ser ladrón.",
              imagen=["Tres portones de la Aduana: uno dorado, uno de hierro y uno de piedra, cada uno con su fila.",
                      "Zed en el puesto del guardia, señalando; Nadia lo observa con la libreta."]),
            m(id="R01-N05-P2", titulo="El orden importa",
              lugar="Los tres portones de la Aduana", personajes="Zed, Gheco, Nadia",
              criatura="ogro",
              carta="El orden de los if | lo más exigente primero · si la primera condición es amplia, tapa a las demás",
              recompensa="xp 15, oro 15",
              escena="El peaje depende de la carga: más de 100 kg paga 20, más de 50 paga 10, el resto 5. El guardia anterior lo escribió… y todos pagan 10. Un **ogro**.",
              sugiere="Los `else if` se revisan en orden: si la primera condición es la más **amplia** (`> 50`), atrapa también a los de 100 y nunca se llega a la otra. Lo más exigente va **primero**.",
              desafio="Llega un carro de 120 kg y paga 10. Reordená las condiciones para que pague 20.",
              inicial='''
                  public class Peso {
                      public static void main(String[] args) {
                          int kg = 120;
                          int peaje;
                          if (kg > 50) {
                              peaje = 10;
                          } else if (kg > 100) {
                              peaje = 20;
                          } else {
                              peaje = 5;
                          }
                          System.out.println(kg + " kg: " + peaje);
                      }
                  }
              ''',
              solucion='''
                  public class Peso {
                      public static void main(String[] args) {
                          int kg = 120;
                          int peaje;
                          if (kg > 100) {
                              peaje = 20;
                          } else if (kg > 50) {
                              peaje = 10;
                          } else {
                              peaje = 5;
                          }
                          System.out.println(kg + " kg: " + peaje);
                      }
                  }
              ''',
              al_superar="El carro de 120 kg paga lo justo. Nadia anota la corrección y, por primera vez, le pone a Zed una tilde de aprobado.",
              imagen=["Tres carros de distintos tamaños en una balanza gigante, cada uno con su peaje.",
                      "La libreta de Nadia con una tilde verde junto al nombre de Zed."]),
            m(id="R01-N05-P3", titulo="El menú de la posada",
              lugar="La posada junto a la Aduana", personajes="Zed, Gheco, Nadia",
              carta="switch | switch (op) { case 1 -> …; case 2 -> …; default -> …; } · compara un valor contra varios casos",
              recompensa="xp 10, oro 10",
              escena="Al terminar el turno, Nadia lleva a Zed a la posada. El menú se pide por número, y el posadero se confunde siempre. —Escribile el menú —dice Nadia—, que yo invito.",
              sugiere="`switch` compara un valor contra varios casos. Con flechas (`case 1 -> …;`) no hace falta `break`. `default` atrapa todo lo que no coincide.",
              desafio="Nadia pide el 2. Completá el caso 2: «Guiso del Imperio».",
              inicial='''
                  public class Posada {
                      public static void main(String[] args) {
                          int op = 2;
                          switch (op) {
                              case 1 -> System.out.println("1: Pan y café");
                              ___
                              default -> System.out.println(op + ": eso no está en el menú");
                          }
                      }
                  }
              ''',
              solucion='''
                  public class Posada {
                      public static void main(String[] args) {
                          int op = 2;
                          switch (op) {
                              case 1 -> System.out.println("1: Pan y café");
                              case 2 -> System.out.println("2: Guiso del Imperio");
                              default -> System.out.println(op + ": eso no está en el menú");
                          }
                      }
                  }
              ''',
              al_superar="Llega el guiso. Zed pide el siete «por las dudas» y el posadero se ríe: eso no está en el menú. Nadia paga, como prometió.",
              imagen=["Una posada cálida con un menú de pizarra numerado.",
                      "Zed y Nadia en una mesa; él señala el número 7 y el posadero se ríe."]),
            m(id="R01-N05-P4", titulo="El switch que devuelve",
              lugar="La posada junto a la Aduana", personajes="Zed, Gheco, Nadia",
              carta="switch como expresión | String x = switch (v) { case \"a\" -> \"…\"; default -> \"…\"; }; · devuelve un valor",
              recompensa="xp 15, oro 15",
              escena="""
                  En la posada, Nadia le cuenta a Zed cómo se clasifica a los viajeros. Él escribe la regla en una servilleta, más corta que la del reglamento.
                  —Así no está en el reglamento —dice ella. —Pero hace lo mismo —responde él.
              """,
              sugiere="Un `switch` también puede **devolver** un valor: `String portón = switch (oficio) { case \"mercader\" -> \"oro\"; … default -> \"piedra\"; };`. Fijate el `;` del final.",
              desafio="Escribí el `switch` que devuelve el portón de cada oficio.",
              inicial='''
                  public class Servilleta {
                      public static void main(String[] args) {
                          String oficio = "mercader";
                          String porton = ___;
                          System.out.println(oficio + " -> " + porton);
                      }
                  }
              ''',
              solucion='''
                  public class Servilleta {
                      public static void main(String[] args) {
                          String oficio = "mercader";
                          String porton = switch (oficio) {
                              case "mercader" -> "oro";
                              case "soldado" -> "hierro";
                              default -> "piedra";
                          };
                          System.out.println(oficio + " -> " + porton);
                      }
                  }
              ''',
              al_superar="""
                  Nadia lee la servilleta dos veces y se la guarda en el bolsillo. —Mañana se la muestro al Escriba Jefe.
                  Afuera, la Aduana cierra. Hay que contar todo lo que entró, carro por carro. Mañana, Zed va a aprender a **repetir**.
              """,
              imagen=["Una servilleta con un switch escrito a mano, sobre una mesa de la posada.",
                      "Nadia guardándose la servilleta en el bolsillo de la chaqueta; Zed sonríe con la taza en la mano.",
                      "Por la ventana, la Aduana cerrando y faroles encendiéndose."]),
        ],
    },
]
