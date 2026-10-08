from gencpp import m

PORTON = "El portón de engranajes"
ALMACEN = "El almacén de piezas"
VENTANILLA = "La ventanilla de pedidos"
CANAL = "Las compuertas del canal"
CINTA = "La sala de la cinta transportadora"
HERRAMIENTAS = "El banco de herramientas de Lima"
EJECUTAR = "Tocá **Ejecutar**: C++ se compila acá mismo, en tu navegador (la primera vez baja el compilador y tarda un poco)."
BRON = "Bron (mecánico grandote de 24 años, pelo castaño corto peinado hacia arriba, remera táctica negra, cinturón de herramientas, rodilleras con luz ámbar, llave inglesa cian al hombro)"
TESLA = "Tesla (muchacho delgado de pelo negro azulado en punta, visor cian, traje azul ajustado con líneas de luz cian y engranajes de bronce en los hombros)"
LIMA = "Lima (aprendiz de relojera de 16, chiquita, dos rodetes castaños con un lápiz clavado, lupa de relojero en un ojo, delantal azul petróleo, una lima en la mano)"
LYN = "Lyn (mensajera de 19, alta, pecas, trenza rubia oscura, ropa de corredora azul y blanca, botas con resortes de bronce, cronómetro de bolsillo)"
OTO = "Oto (cocinero grandote, bigote enorme de manubrio, cabeza afeitada, gorro alto con un engranaje bordado, delantal con manchas violetas, cucharón de bronce)"
GHECO = "Gheco (gecko de luz con antiparras)"

NODOS = [
    {
        "titulo": "R00-N01 · Clase 0 · Hola, C++",
        "misiones": [
            m(id="R00-N01-P1", titulo="La primera orden",
              lugar=PORTON, personajes="Bron, Gheco, Tesla",
              carta="Mostrar texto | std::cout << \"texto\\n\"; · \\n salta de línea · cada instrucción termina con ;",
              recompensa="xp 10, oro 10",
              escena="""
                  Bron despierta al pie de la cuesta, junto a un vitral apagado. Arriba, el portón de la Ciudadela es una pared de engranajes trabados. Sobre su hombro aparece un gecko de luz con antiparras: **Gheco**.
                  —Acá las órdenes se escriben en C++ —le dice—. Antes de arreglar nada, presentate. Por escrito.
              """,
              sugiere="`std::cout << \"…\";` muestra el texto entre comillas, y `\\n` al final baja a la línea siguiente. " + EJECUTAR,
              desafio="Completá la instrucción para que Bron se presente.",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      ___ << "Soy Bron, mecanico. Arreglo todo a mano.\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      std::cout << "Soy Bron, mecanico. Arreglo todo a mano.\\n";
                      return 0;
                  }
              ''',
              al_superar="El portón no se abre, pero uno de los engranajes gira medio diente, como saludando. Gheco asiente.",
              imagen=["Al pie de una cuesta, de noche, un vitral apagado y arriba un portón enorme hecho de engranajes de bronce trabados.",
                      BRON + " mira el portón con la llave en la mano.", GHECO + " sobre su hombro."]),
            m(id="R00-N01-P2", titulo="Un slime en el portón",
              lugar=PORTON, personajes="Bron, Gheco",
              criatura="slime",
              carta="Error de sintaxis | expected ';' · el compilador no produce nada hasta que se arregla · se lee la PRIMERA línea del error",
              recompensa="xp 10, oro 10",
              escena="""
                  Entre los dientes del portón se asoma un **slime**: una gota de baba verde que se alimenta de los punto y coma olvidados. Bron le escribe una orden al portón, y el Taller ni la mira: devuelve un error.
              """,
              sugiere="Leé el primer error: dice la línea y que **esperaba** algo (`expected ';'`). Cada instrucción termina con `;`.",
              desafio="Encontrá lo que falta para que el programa compile.",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      std::cout << "Engranaje 1: listo\\n"
                      std::cout << "Engranaje 2: listo\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      std::cout << "Engranaje 1: listo\\n";
                      std::cout << "Engranaje 2: listo\\n";
                      return 0;
                  }
              ''',
              al_superar="El slime se resbala por el portón y desaparece en una grieta. Los dos primeros engranajes giran.",
              imagen=["Un portón de engranajes de bronce con un slime verde y brillante asomado entre dos dientes.",
                      BRON + " señala la línea del error en una pantalla flotante.", GHECO + " se tapa la nariz."]),
            m(id="R00-N01-P3", titulo="Las cuentas del portón",
              lugar=PORTON, personajes="Bron, Lima",
              carta="Números | std::cout << 200 - 47; muestra 153 · entre comillas es texto: \"200 - 47\" se muestra tal cual",
              recompensa="xp 10, oro 10",
              escena="""
                  Bron lleva 47 engranajes arreglados a mano. Una chica de delantal azul, con una lupa de relojero en el ojo y una lima en la mano, se le acerca: **Lima**.
                  —¿Cuántos te faltan? —Bron escribe la cuenta… y el Taller le muestra la cuenta, no el resultado.
              """,
              sugiere="Lo que va entre comillas se muestra **tal cual**. Para que C++ haga la cuenta, la cuenta va **afuera** de las comillas, con su propio `<<`.",
              desafio="Hacé que el programa muestre el resultado de la cuenta.",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      std::cout << "Faltan " << "200 - 47" << " engranajes\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      std::cout << "Faltan " << 200 - 47 << " engranajes\\n";
                      return 0;
                  }
              ''',
              al_superar="Ciento cincuenta y tres. Bron suspira. Lima se tapa la boca para no reírse.",
              imagen=["Frente al portón de engranajes, una pila de engranajes arreglados y una montaña más grande sin arreglar.",
                      BRON + " cuenta con los dedos, agotado.", LIMA + " lo mira con la lupa puesta, conteniendo la risa."]),
            m(id="R00-N01-P4", titulo="El plano del portón",
              lugar=PORTON, personajes="Bron, Tesla, Lima",
              carta="Varias líneas | cada \\n es un salto · sin \\n todo queda en un solo renglón · endl también salta",
              recompensa="xp 15, oro 15",
              item="Llave Mellada",
              escena="""
                  Al engranaje 47 la llave se traba en un diente, Bron hace fuerza y la llave sale **mellada**. Desde arriba baja por una polea un muchacho de traje azul y visor cian: **Tesla**, el Artífice Mayor.
                  —El portón tiene un plano —dice, y le muestra una hoja—. Escribilo bien, línea por línea, y el Taller arregla los doscientos de una vez.
              """,
              sugiere="Cada parte del plano tiene que ir en su renglón: falta el `\\n` al final de cada texto.",
              desafio="Hacé que cada paso del plano salga en su propia línea.",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      std::cout << "Plano del porton";
                      std::cout << "1. Alinear los 200 engranajes";
                      std::cout << "2. Girar la manivela";
                      std::cout << "3. Abrir";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      std::cout << "Plano del porton\\n";
                      std::cout << "1. Alinear los 200 engranajes\\n";
                      std::cout << "2. Girar la manivela\\n";
                      std::cout << "3. Abrir\\n";
                      return 0;
                  }
              ''',
              al_superar="Los doscientos engranajes giran a la vez y el portón se abre con un suspiro de vapor. Bron mira su llave mellada. —¿Y esto para qué me sirve? —pregunta. Tesla sonríe: es la primera vez, y no va a ser la última.",
              imagen=["El portón de engranajes abriéndose de par en par, con vapor y luz cian saliendo de adentro.",
                      TESLA + " sostiene un plano iluminado.", BRON + " mira su llave inglesa mellada."]),
        ],
    },
    {
        "titulo": "R01-N01 · Variables, tipos y operadores",
        "misiones": [
            m(id="R01-N01-P1", titulo="El goblin de los decimales",
              lugar=ALMACEN, personajes="Bron, Lima, Gheco",
              criatura="goblin",
              carta="Tipos | int guarda enteros · double guarda decimales · un double en un int pierde la parte decimal",
              recompensa="xp 10, oro 10",
              escena="""
                  Bron guarda tres kilos y tres cuartos de tornillos en el cajón de la etiqueta `int`. Al abrirlo, hay tres kilos. Los 750 gramos se los llevó un **goblin**, sin hacer ruido.
                  Lima se ríe por primera vez (y después disimula).
              """,
              sugiere="Un `int` solo guarda enteros. Para guardar `3.75`, el cajón tiene que ser `double`. Mirá también lo que dice el compilador del navegador: avisa que el valor cambia.",
              desafio="Cambiá el tipo del cajón para que no se pierdan los decimales.",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      int kilos = 3.75;
                      std::cout << "Tornillos: " << kilos << " kg\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      double kilos = 3.75;
                      std::cout << "Tornillos: " << kilos << " kg\\n";
                      return 0;
                  }
              ''',
              al_superar="Los tres kilos y tres cuartos vuelven al cajón. En un rincón, el goblin suelta los 750 gramos y sale corriendo.",
              imagen=["Un almacén de cajones con etiquetas: «int», «double», «char», «bool».",
                      "Un goblin escapa con una bolsita de tornillos.", BRON + " abre un cajón casi vacío; " + LIMA + " se ríe detrás."]),
            m(id="R01-N01-P2", titulo="Cajas y sobrantes",
              lugar=ALMACEN, personajes="Bron, Lima",
              carta="División entera | 17 / 5 da 3 (entre enteros, sin decimales) · 17 % 5 da 2 (el resto)",
              recompensa="xp 10, oro 10",
              escena="""
                  Hay 17 tuercas para repartir en 5 cajas iguales. Bron calcula cuántas van en cada caja y cuántas sobran, pero los sobrantes le dan cualquier cosa.
                  —Para el resto hay un operador —dice Lima, sin levantar la vista del reloj que arregla.
              """,
              sugiere="Entre enteros, `/` da el cociente y `%` da el **resto**: `17 % 5` es `2`.",
              desafio="Calculá lo que sobra con el operador del resto.",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      int tuercas = 17;
                      int cajas = 5;
                      int por_caja = tuercas / cajas;
                      int sobran = tuercas - cajas;
                      std::cout << "Por caja: " << por_caja << "\\n";
                      std::cout << "Sobran: " << sobran << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      int tuercas = 17;
                      int cajas = 5;
                      int por_caja = tuercas / cajas;
                      int sobran = tuercas % cajas;
                      std::cout << "Por caja: " << por_caja << "\\n";
                      std::cout << "Sobran: " << sobran << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres por caja y dos sueltas, que Lima se guarda en el bolsillo del delantal «para un reloj».",
              imagen=["Cinco cajas de madera con tres tuercas cada una y dos tuercas sueltas sobre la mesa.",
                      BRON + " reparte tuercas.", LIMA + " se guarda dos tuercas en el delantal."]),
            m(id="R01-N01-P3", titulo="El promedio de Lyn",
              lugar=ALMACEN, personajes="Lyn, Bron",
              carta="static_cast | static_cast<double>(x) convierte a propósito · si uno de los dos es double, la división tiene decimales",
              recompensa="xp 10, oro 10",
              escena="""
                  Lyn, la mensajera de la Ciudadela, corrió dos vueltas a las torres en 7 minutos en total. Quiere saber su promedio por vuelta, y el almacén le dice **3**.
                  —¡Es un robo! —grita Lyn—. Le apuesto lo que sea a que fueron tres y medio.
              """,
              sugiere="`7 / 2` entre enteros da `3`. Si convertís uno a `double` con `static_cast<double>(...)`, la división da `3.5`.",
              desafio="Convertí a propósito para que el promedio tenga decimales.",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      int minutos = 7;
                      int vueltas = 2;
                      double promedio = minutos / vueltas;
                      std::cout << "Promedio: " << promedio << " minutos por vuelta\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      int minutos = 7;
                      int vueltas = 2;
                      double promedio = static_cast<double>(minutos) / vueltas;
                      std::cout << "Promedio: " << promedio << " minutos por vuelta\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres y medio. Lyn gana la apuesta contra nadie y lo festeja igual.",
              imagen=["Un pizarrón con la cuenta 7 / 2 tachada y al lado 3.5.",
                      LYN + " levanta los brazos festejando.", BRON + " aplaude sin entender del todo."]),
        ],
    },
    {
        "titulo": "R01-N02 · Entrada y salida: cin y string",
        "misiones": [
            m(id="R01-N02-P1", titulo="La frase entera",
              lugar=VENTANILLA, personajes="Lyn, Bron, Gheco",
              carta="getline | std::cin >> lee UNA palabra · std::getline(std::cin, texto) lee la línea entera",
              recompensa="xp 10, oro 10",
              escena="""
                  Lyn llega corriendo a la ventanilla (siempre llega corriendo) y grita su pedido: **«Dos ruedas dentadas»**. El guardia mecánico anota… «Dos». Nada más.
                  Lyn le apuesta a Bron que el guardia está roto.
              """,
              sugiere="`std::cin >> pedido` corta en el primer espacio. Para leer la frase completa: `std::getline(std::cin, pedido);`.",
              desafio="Leé el pedido entero.",
              entrada="Dos ruedas dentadas\n",
              inicial='''
                  #include <iostream>
                  #include <string>

                  int main()
                  {
                      std::string pedido;
                      std::cin >> pedido;
                      std::cout << "Pedido: " << pedido << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  int main()
                  {
                      std::string pedido;
                      std::getline(std::cin, pedido);
                      std::cout << "Pedido: " << pedido << "\\n";
                      return 0;
                  }
              ''',
              al_superar="El guardia anota «Dos ruedas dentadas» y Lyn pierde la apuesta. Bron gana, pero no sabe bien por qué.",
              imagen=["Una ventanilla de bronce con un guardia mecánico que escribe en un libro enorme.",
                      LYN + " grita su pedido con las manos en la boca.", BRON + " espera con los brazos cruzados."]),
            m(id="R01-N02-P2", titulo="Cantidad por precio",
              lugar=VENTANILLA, personajes="Bron, Oto",
              carta="Leer números | std::cin >> a >> b; lee dos números separados por espacio · el tipo de la variable dice qué se lee",
              recompensa="xp 10, oro 10",
              escena="""
                  Oto, el cocinero del comedor, pide ollas nuevas: escribe en la ventanilla la cantidad y el precio de cada una. El guardia tiene que calcular el total, pero se olvida de leer el precio.
              """,
              sugiere="Se pueden leer varios valores seguidos: `std::cin >> cantidad >> precio;`.",
              desafio="Leé también el precio y mostrá el total.",
              entrada="3 250\n",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      int cantidad = 0;
                      int precio = 0;
                      std::cin >> cantidad;
                      std::cout << cantidad << " x " << precio << " = " << cantidad * precio << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      int cantidad = 0;
                      int precio = 0;
                      std::cin >> cantidad >> precio;
                      std::cout << cantidad << " x " << precio << " = " << cantidad * precio << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres ollas a 250: 750. Oto paga con monedas que huelen a guiso.",
              imagen=["La ventanilla de pedidos con un recibo que dice «3 x 250 = 750».",
                      OTO + " cuenta monedas con el cucharón bajo el brazo.", BRON + " sella el recibo."]),
            m(id="R01-N02-P3", titulo="El menú de Oto",
              lugar=VENTANILLA, personajes="Oto, Lima",
              carta="Formato | #include <iomanip> · std::setw(n) da ancho a la próxima cosa · std::left alinea a la izquierda · std::fixed << std::setprecision(2) muestra 2 decimales",
              recompensa="xp 15, oro 15",
              escena="""
                  Oto quiere colgar el menú del día en la ventanilla, con los precios en columna y siempre con dos decimales. Le sale todo amontonado.
                  Lima le mide las columnas con la lupa: —Así no se puede leer.
              """,
              sugiere="`std::left << std::setw(10) << nombre` ocupa 10 lugares con el nombre a la izquierda. `std::fixed << std::setprecision(2)` muestra siempre dos decimales (`8.00`).",
              desafio="Dale ancho a la columna de los nombres y dos decimales a los precios.",
              inicial='''
                  #include <iostream>
                  #include <iomanip>

                  int main()
                  {
                      std::cout << "Guiso" << 12.5 << "\\n";
                      std::cout << "Pan" << 3 << "\\n";
                      std::cout << "Sopa" << 8.75 << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <iomanip>

                  int main()
                  {
                      std::cout << std::fixed << std::setprecision(2);
                      std::cout << std::left << std::setw(10) << "Guiso" << 12.5 << "\\n";
                      std::cout << std::left << std::setw(10) << "Pan" << 3.0 << "\\n";
                      std::cout << std::left << std::setw(10) << "Sopa" << 8.75 << "\\n";
                      return 0;
                  }
              ''',
              al_superar="El menú queda prolijo como un reloj. Lima lo aprueba con un gesto, y Oto lo cuelga torcido.",
              imagen=["Un pizarrón de menú con tres platos en columna y sus precios alineados con dos decimales.",
                      OTO + " cuelga el pizarrón un poco torcido.", LIMA + " lo endereza con la punta de la lima."]),
        ],
    },
    {
        "titulo": "R01-N03 · Decisiones",
        "misiones": [
            m(id="R01-N03-P1", titulo="Las tres compuertas",
              lugar=CANAL, personajes="Bron, Oto, Tesla",
              carta="if / else if | se prueban en orden y entra en la PRIMERA que se cumple · la más exigente va primero",
              recompensa="xp 10, oro 10",
              escena="""
                  Las compuertas del canal se abren según cuánto llovió: más de 50 mm, tres; más de 20, dos; algo de lluvia, una; nada, ninguna. Bron programó la tabla y, con 35 mm, abrió una sola.
                  El comedor de Oto se inunda igual, porque Bron después abrió todas «por las dudas».
              """,
              sugiere="Con `else if`, entra en la **primera** condición que se cumple. Si `lluvia > 0` va primero, 35 entra ahí y nunca llega a las otras. Ordená de la más exigente a la menos.",
              desafio="Ordená las condiciones para que cada lluvia abra las compuertas que corresponden.",
              entrada="35\n",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      int lluvia = 0;
                      std::cin >> lluvia;
                      if (lluvia > 0) {
                          std::cout << "Abrir una compuerta\\n";
                      } else if (lluvia > 20) {
                          std::cout << "Abrir dos compuertas\\n";
                      } else if (lluvia > 50) {
                          std::cout << "Abrir tres compuertas\\n";
                      } else {
                          std::cout << "No abrir ninguna\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      int lluvia = 0;
                      std::cin >> lluvia;
                      if (lluvia > 50) {
                          std::cout << "Abrir tres compuertas\\n";
                      } else if (lluvia > 20) {
                          std::cout << "Abrir dos compuertas\\n";
                      } else if (lluvia > 0) {
                          std::cout << "Abrir una compuerta\\n";
                      } else {
                          std::cout << "No abrir ninguna\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Con 35 mm se abren dos compuertas, y el agua baja del comedor. Oto sale con la olla en alto: —¡Receta que se respeta, guiso que no falla!",
              imagen=["Un canal de piedra con tres compuertas de bronce; dos abiertas y una cerrada.",
                      OTO + " con el agua por las rodillas, levantando una olla.", BRON + " baja una palanca, avergonzado."]),
            m(id="R01-N03-P2", titulo="El punto del guiso",
              lugar="El comedor de los artífices", personajes="Oto, Bron",
              carta="&& y || | && pide que se cumplan LAS DOS · || alcanza con UNA · «entre 80 y 95» es t >= 80 && t <= 95",
              recompensa="xp 10, oro 10",
              escena="""
                  El guiso de Oto está listo entre 80 y 95 grados, ni uno más ni uno menos. Bron le armó un termómetro que dice «listo» con 120 grados, y el guiso sale violeta.
              """,
              sugiere="«Entre 80 y 95» son **dos** condiciones que se tienen que cumplir juntas: `&&`. Con `||` alcanza con que se cumpla una, y 120 es mayor que 80.",
              desafio="Corregí la condición del termómetro.",
              entrada="120\n",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      int grados = 0;
                      std::cin >> grados;
                      if (grados >= 80 || grados <= 95) {
                          std::cout << "El guiso esta listo\\n";
                      } else {
                          std::cout << "Todavia no\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      int grados = 0;
                      std::cin >> grados;
                      if (grados >= 80 && grados <= 95) {
                          std::cout << "El guiso esta listo\\n";
                      } else {
                          std::cout << "Todavia no\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Con 120 grados el termómetro dice «todavía no», y Oto baja el fuego. El guiso vuelve a ser marrón.",
              imagen=["Una olla enorme con un termómetro de bronce clavado que marca 120.",
                      OTO + " sopla el guiso, preocupado.", BRON + " ajusta el termómetro."]),
            m(id="R01-N03-P3", titulo="Las torres de Lyn",
              lugar="La plaza de las torres", personajes="Lyn, Lima",
              carta="switch | elige por un valor exacto (un entero o un char) · cada case termina con break · sin break sigue de largo",
              recompensa="xp 10, oro 10",
              escena="""
                  Lyn reparte cartas según la letra de la torre: `a`, la del reloj; `b`, la de las poleas; `c`, la de los vitrales. Con la letra `a`, el programa la manda a las tres torres. Lyn corre igual, pero llega agotada.
              """,
              sugiere="En un `switch`, cuando entra en un `case`, sigue de largo por los de abajo hasta encontrar un `break`.",
              desafio="Agregá lo que falta para que cada letra mande a una sola torre.",
              entrada="a\n",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      char torre = ' ';
                      std::cin >> torre;
                      switch (torre) {
                      case 'a':
                          std::cout << "Torre del reloj\\n";
                      case 'b':
                          std::cout << "Torre de las poleas\\n";
                      case 'c':
                          std::cout << "Torre de los vitrales\\n";
                          break;
                      default:
                          std::cout << "Esa torre no existe\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      char torre = ' ';
                      std::cin >> torre;
                      switch (torre) {
                      case 'a':
                          std::cout << "Torre del reloj\\n";
                          break;
                      case 'b':
                          std::cout << "Torre de las poleas\\n";
                          break;
                      case 'c':
                          std::cout << "Torre de los vitrales\\n";
                          break;
                      default:
                          std::cout << "Esa torre no existe\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Una carta, una torre. Lyn llega a la del reloj en un minuto y le sobra tiempo para apostar contra el reloj.",
              imagen=["Tres torres de la Ciudadela con letras a, b y c pintadas en la base.",
                      LYN + " corre con un bolso de cartas.", LIMA + " anota los tiempos con su lupa."]),
        ],
    },
    {
        "titulo": "R01-N04 · Bucles",
        "misiones": [
            m(id="R01-N04-P1", titulo="Diez tuercas, ni una más",
              lugar=CINTA, personajes="Bron, Lima",
              carta="for | for (int i = 0; i < 10; i++) da 10 vueltas · con <= da 11 · contá desde 0 con <",
              recompensa="xp 10, oro 10",
              escena="""
                  Bron prende la cinta para mandar diez tuercas al taller de Lima. Llegan once. Lima la para con la mano y saca la lima.
                  —¿Contaste las vueltas? —No. —Se nota.
              """,
              sugiere="Si `i` arranca en 0, `i <= 10` da once vueltas (de 0 a 10). Con `i < 10` da diez.",
              desafio="Hacé que la cinta mande exactamente diez tuercas.",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      int enviadas = 0;
                      for (int i = 0; i <= 10; i++) {
                          enviadas++;
                      }
                      std::cout << "Tuercas enviadas: " << enviadas << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      int enviadas = 0;
                      for (int i = 0; i < 10; i++) {
                          enviadas++;
                      }
                      std::cout << "Tuercas enviadas: " << enviadas << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Diez tuercas. Lima guarda la lima, por ahora.",
              imagen=["Una cinta transportadora de bronce con diez tuercas en fila.",
                      BRON + " frena la cinta con una palanca.", LIMA + " cuenta las tuercas con la lupa."]),
            m(id="R01-N04-P2", titulo="Las cajas crecientes",
              lugar=CINTA, personajes="Bron, Tesla",
              carta="Acumular | una variable que arranca en 0 y suma en cada vuelta: total += algo · se muestra DESPUÉS del bucle",
              recompensa="xp 10, oro 10",
              escena="""
                  La cinta lleva cajas: la primera con 2 tuercas, la segunda con 4, la tercera con 6… Tesla le pregunta a Bron cuántas tuercas hay en total en las primeras `n` cajas. Bron cuenta con los dedos y se le acaban.
              """,
              sugiere="La caja `i` tiene `2 * i` tuercas. Sumalas en `total` dentro del bucle (`total += 2 * i;`) y mostrá el total al final.",
              desafio="Completá la suma dentro del bucle.",
              entrada="5\n",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      int n = 0;
                      std::cin >> n;
                      int total = 0;
                      for (int i = 1; i <= n; i++) {
                          std::cout << "Caja " << i << ": " << 2 * i << " tuercas\\n";
                      }
                      std::cout << "Total: " << total << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      int n = 0;
                      std::cin >> n;
                      int total = 0;
                      for (int i = 1; i <= n; i++) {
                          std::cout << "Caja " << i << ": " << 2 * i << " tuercas\\n";
                          total += 2 * i;
                      }
                      std::cout << "Total: " << total << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Treinta tuercas en cinco cajas. Tesla asiente: —Ahora probalo con mil cajas, sin dedos.",
              imagen=["Cinco cajas en una cinta, cada una con más tuercas que la anterior.",
                      TESLA + " señala la cinta con el compás.", BRON + " se mira los dedos."]),
            m(id="R01-N04-P3", titulo="El cronómetro de Lyn",
              lugar="La pista alrededor de las torres", personajes="Lyn, Bron",
              carta="for de rango sobre un texto | for (char c : texto) recorre letra por letra · if (c == 'x') cuenta las x",
              recompensa="xp 10, oro 10",
              escena="""
                  El cronómetro de Lyn anota cada vuelta con una letra: `x` si fue buena, `o` si tropezó. Lyn quiere saber cuántas de cada una, y Bron le cuenta solo las buenas.
              """,
              sugiere="El `for` de rango ya recorre cada letra. Falta el contador de los tropiezos, y sumarle cuando la letra es `'o'`.",
              desafio="Contá también los tropiezos.",
              entrada="xxoxxxoo\n",
              inicial='''
                  #include <iostream>
                  #include <string>

                  int main()
                  {
                      std::string vueltas;
                      std::cin >> vueltas;
                      int buenas = 0;
                      int tropiezos = 0;
                      for (char c : vueltas) {
                          if (c == 'x') {
                              buenas++;
                          }
                      }
                      std::cout << "Buenas: " << buenas << ", tropiezos: " << tropiezos << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  int main()
                  {
                      std::string vueltas;
                      std::cin >> vueltas;
                      int buenas = 0;
                      int tropiezos = 0;
                      for (char c : vueltas) {
                          if (c == 'x') {
                              buenas++;
                          } else if (c == 'o') {
                              tropiezos++;
                          }
                      }
                      std::cout << "Buenas: " << buenas << ", tropiezos: " << tropiezos << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Cinco buenas y tres tropiezos. Lyn jura que los tropiezos fueron culpa de las botas.",
              imagen=["Un cronómetro de bolsillo abierto con una tira de papel que dice xxoxxxoo.",
                      LYN + " se ata las botas de resortes.", BRON + " lee la tira de papel."]),
        ],
    },
    {
        "titulo": "R01-N05 · Funciones",
        "misiones": [
            m(id="R01-N05-P1", titulo="Los relojes repetidos",
              lugar=HERRAMIENTAS, personajes="Bron, Lima",
              carta="Función | int dientes(int engranajes, int por_engranaje) { return ...; } · se escribe una vez y se llama muchas",
              recompensa="xp 10, oro 10",
              escena="""
                  Lima le encarga a Bron un tablero con relojes. Bron escribe la cuenta de los dientes de cada reloj, la copia, la copia otra vez… y, para ver qué pasa, una cuarta.
                  Lo que pasa es que Lima saca la lima. —¿Y si lo hacemos **una sola vez**?
              """,
              sugiere="La función recibe la cantidad de engranajes y los dientes de cada uno, y **devuelve** el total con `return`.",
              desafio="Completá el cuerpo de la función.",
              inicial='''
                  #include <iostream>

                  int dientes_totales(int engranajes, int por_engranaje)
                  {
                      return 0;
                  }

                  int main()
                  {
                      std::cout << "Reloj de pared: " << dientes_totales(3, 40) << " dientes\\n";
                      std::cout << "Reloj de torre: " << dientes_totales(12, 60) << " dientes\\n";
                      std::cout << "Reloj de bolsillo: " << dientes_totales(5, 12) << " dientes\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int dientes_totales(int engranajes, int por_engranaje)
                  {
                      return engranajes * por_engranaje;
                  }

                  int main()
                  {
                      std::cout << "Reloj de pared: " << dientes_totales(3, 40) << " dientes\\n";
                      std::cout << "Reloj de torre: " << dientes_totales(12, 60) << " dientes\\n";
                      std::cout << "Reloj de bolsillo: " << dientes_totales(5, 12) << " dientes\\n";
                      return 0;
                  }
              ''',
              al_superar="Una cuenta, tres relojes. Lima guarda la lima y Bron esconde detrás de la espalda la cuarta copia.",
              imagen=["Un banco de relojero con tres relojes de distinto tamaño abiertos.",
                      LIMA + " amenaza con la lima.", BRON + " esconde una hoja detrás de la espalda."]),
            m(id="R01-N05-P2", titulo="Tres formas de anunciar",
              lugar="La torre del reloj", personajes="Bron, Tesla",
              carta="Sobrecarga | varias funciones con el MISMO nombre y distintos parámetros · C++ elige la que encaja con lo que le pasás",
              recompensa="xp 15, oro 15",
              escena="""
                  El anunciador de la torre del reloj sabe anunciar números enteros y textos. Cuando Tesla le pasa la presión de la caldera, `2.5`, anuncia «entero 2». Tesla se cruza de brazos.
              """,
              sugiere="Cuando no hay una versión para `double`, C++ convierte el `2.5` a `int` y usa esa. Escribí una tercera `anunciar` que reciba un `double`.",
              desafio="Agregá la versión que falta.",
              inicial='''
                  #include <iostream>
                  #include <string>

                  void anunciar(int n)
                  {
                      std::cout << "entero " << n << "\\n";
                  }

                  void anunciar(const std::string& texto)
                  {
                      std::cout << "texto " << texto << "\\n";
                  }

                  int main()
                  {
                      anunciar(12);
                      anunciar("mediodia");
                      anunciar(2.5);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  void anunciar(int n)
                  {
                      std::cout << "entero " << n << "\\n";
                  }

                  void anunciar(const std::string& texto)
                  {
                      std::cout << "texto " << texto << "\\n";
                  }

                  void anunciar(double x)
                  {
                      std::cout << "decimal " << x << "\\n";
                  }

                  int main()
                  {
                      anunciar(12);
                      anunciar("mediodia");
                      anunciar(2.5);
                      return 0;
                  }
              ''',
              al_superar="«Decimal 2.5.» El anunciador suena tres veces con tres voces distintas. Tesla descruza los brazos.",
              imagen=["Una torre de reloj con un altavoz de bronce que tiene tres bocinas.",
                      TESLA + " escucha con el visor levantado.", BRON + " ajusta una de las bocinas."]),
            m(id="R01-N05-P3", titulo="La campana por defecto",
              lugar="La torre del reloj", personajes="Bron, Oto",
              carta="Parámetro por defecto | void tocar(int veces = 1) · tocar() usa 1 · tocar(3) usa 3 · el valor va en la declaración",
              recompensa="xp 10, oro 10",
              escena="""
                  La campana del comedor se toca una vez para avisar que hay guiso, y tres para los días de fiesta. Oto quiere poder escribir `tocar()` sin número, y el Taller no lo deja.
              """,
              sugiere="Un parámetro puede tener un valor **por defecto**: `void tocar(int veces = 1)`. Si no se lo pasás, usa ese.",
              desafio="Dale a `veces` el valor 1 por defecto.",
              inicial='''
                  #include <iostream>

                  void tocar(int veces)
                  {
                      for (int i = 0; i < veces; i++) {
                          std::cout << "Talan! ";
                      }
                      std::cout << "(" << veces << ")\\n";
                  }

                  int main()
                  {
                      tocar();
                      tocar(3);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  void tocar(int veces = 1)
                  {
                      for (int i = 0; i < veces; i++) {
                          std::cout << "Talan! ";
                      }
                      std::cout << "(" << veces << ")\\n";
                  }

                  int main()
                  {
                      tocar();
                      tocar(3);
                      return 0;
                  }
              ''',
              al_superar="Una campanada para el guiso de todos los días y tres para la fiesta. Oto toca las tres de nuevo, por las dudas.",
              imagen=["Una campana de bronce en el comedor de los artífices, con una cuerda larga.",
                      OTO + " tira de la cuerda con entusiasmo.", BRON + " se tapa los oídos."]),
        ],
    },
]
