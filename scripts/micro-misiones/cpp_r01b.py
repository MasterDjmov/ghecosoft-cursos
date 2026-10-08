from gencpp import m
from cpp_r01 import BRON, TESLA, LIMA, LYN, OTO, GHECO

DEPOSITO = "El depósito de la Ciudadela"
TORRE = "La torre del reloj"
FERIA = "La rueda de feria de la plaza"
PATIO = "El patio de pruebas"
AUTOMATA = "el Autómata de Latón (autómata de tres metros de placas de latón remachadas, corazón de vapor visible por una ventanita del pecho, tarjeta perforada en la frente, ojos cian)"

NODOS = [
    {
        "titulo": "R01-N06 · Referencias",
        "misiones": [
            m(id="R01-N06-P1", titulo="La llave prestada",
              lugar=DEPOSITO, personajes="Bron, Oto",
              carta="Referencia | void ajustar(int& p) recibe EL ORIGINAL · sin &, recibe una copia y el cambio se pierde al salir",
              recompensa="xp 10, oro 10",
              escena="""
                  Oto le pide la llave a Bron para ajustar la presión de la olla grande. Bron, generoso, le hace una **copia** en el torno. Oto ajusta con la copia… y la olla sigue igual.
              """,
              sugiere="Sin `&`, la función recibe una copia de `presion`: la cambia y la copia se tira al salir. Con `int& p`, recibe **la** variable de `main`.",
              desafio="Hacé que la función ajuste la presión de verdad.",
              inicial='''
                  #include <iostream>

                  void ajustar(int p)
                  {
                      p = p - 15;
                  }

                  int main()
                  {
                      int presion = 90;
                      ajustar(presion);
                      std::cout << "Presion de la olla: " << presion << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  void ajustar(int& p)
                  {
                      p = p - 15;
                  }

                  int main()
                  {
                      int presion = 90;
                      ajustar(presion);
                      std::cout << "Presion de la olla: " << presion << "\\n";
                      return 0;
                  }
              ''',
              al_superar="La olla baja a 75 y deja de silbar. Oto devuelve la llave de verdad, con olor a guiso.",
              imagen=["Una olla gigante con un manómetro que baja de 90 a 75.",
                      OTO + " ajusta una válvula con una llave inglesa cian.", BRON + " mira, satisfecho."]),
            m(id="R01-N06-P2", titulo="Dos respuestas de una vez",
              lugar=DEPOSITO, personajes="Bron, Lima",
              carta="Varios resultados | una función devuelve uno con return · para devolver dos, recibe dos referencias y las llena",
              recompensa="xp 10, oro 10",
              escena="""
                  Lima quiere una función que, de una sola vez, diga cuántas tuercas van por caja **y** cuántas sobran. Bron escribió la función, pero los resultados nunca llegan a `main`.
              """,
              sugiere="`por_caja` y `sobran` tienen que llegar como referencias (`int&`) para que la función pueda escribir en las variables de `main`.",
              desafio="Hacé que los dos resultados lleguen a `main`.",
              inicial='''
                  #include <iostream>

                  void repartir(int tuercas, int cajas, int por_caja, int sobran)
                  {
                      por_caja = tuercas / cajas;
                      sobran = tuercas % cajas;
                  }

                  int main()
                  {
                      int por_caja = 0;
                      int sobran = 0;
                      repartir(47, 6, por_caja, sobran);
                      std::cout << "Por caja: " << por_caja << ", sobran: " << sobran << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  void repartir(int tuercas, int cajas, int& por_caja, int& sobran)
                  {
                      por_caja = tuercas / cajas;
                      sobran = tuercas % cajas;
                  }

                  int main()
                  {
                      int por_caja = 0;
                      int sobran = 0;
                      repartir(47, 6, por_caja, sobran);
                      std::cout << "Por caja: " << por_caja << ", sobran: " << sobran << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Siete por caja y sobran cinco. Lima anota los dos números con su letra de relojera.",
              imagen=["Seis cajas con siete tuercas cada una y cinco tuercas sueltas.",
                      LIMA + " escribe en un cuaderno.", BRON + " cierra las cajas."]),
            m(id="R01-N06-P3", titulo="El pedido de las bisagras",
              lugar=DEPOSITO, personajes="Bron, Lima, Tesla",
              carta="Intercambiar | void cambiar(std::string& a, std::string& b) { std::string t = a; a = b; b = t; } · hacen falta las dos referencias",
              recompensa="xp 15, oro 15",
              escena="""
                  Bron y Lima tienen que cambiar los turnos de guardia del depósito. Bron escribe una función para intercambiarlos, y los turnos quedan igual.
                  Mientras lo arregla, ve en un estante un pedido viejo y amarillento: **«Bisagras, dos. Que abran algo que no es una puerta»**, firmado con un vitral dibujado. Tesla lo mira y se pone serio un segundo.
              """,
              sugiere="Para intercambiar dos variables de `main`, la función tiene que recibir las **dos** por referencia.",
              desafio="Hacé que el intercambio llegue a `main`.",
              inicial='''
                  #include <iostream>
                  #include <string>

                  void cambiar(std::string a, std::string b)
                  {
                      std::string t = a;
                      a = b;
                      b = t;
                  }

                  int main()
                  {
                      std::string manana = "Bron";
                      std::string tarde = "Lima";
                      cambiar(manana, tarde);
                      std::cout << "Manana: " << manana << "\\n";
                      std::cout << "Tarde: " << tarde << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  void cambiar(std::string& a, std::string& b)
                  {
                      std::string t = a;
                      a = b;
                      b = t;
                  }

                  int main()
                  {
                      std::string manana = "Bron";
                      std::string tarde = "Lima";
                      cambiar(manana, tarde);
                      std::cout << "Manana: " << manana << "\\n";
                      std::cout << "Tarde: " << tarde << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Lima a la mañana, Bron a la tarde. El pedido de las bisagras queda en el bolsillo de Bron; Tesla no le pide que lo devuelva.",
              imagen=["Un estante del depósito con un pedido amarillento que tiene un vitral dibujado en lugar de firma.",
                      BRON + " lee el pedido.", TESLA + " mira por encima de su hombro, serio."]),
        ],
    },
    {
        "titulo": "R01-N07 · Vectores: listas que crecen",
        "misiones": [
            m(id="R01-N07-P1", titulo="El orco del lugar 10",
              lugar=TORRE, personajes="Bron, Lima",
              criatura="orco",
              carta="Vector | std::vector<int> v = {...}; · posiciones de 0 a v.size() - 1 · v.at(i) avisa si te pasás",
              recompensa="xp 10, oro 10",
              escena="""
                  En la torre del reloj, los engranajes cuelgan de una cadena numerada desde **cero**. Bron recorre la cadena hasta el lugar 10 de una cadena de 10, y en ese lugar encuentra un **orco** dormido. El programa revienta con un `out_of_range`.
              """,
              sugiere="Las posiciones van de `0` a `size() - 1`. El bucle tiene que seguir **mientras** `i < dientes.size()`. Como el código usa `.at(i)`, el orco avisa en lugar de morder en silencio.",
              desafio="Arreglá la condición del bucle.",
              inicial='''
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> dientes = {12, 40, 60, 24, 36};
                      int total = 0;
                      for (std::size_t i = 0; i <= dientes.size(); i++) {
                          total += dientes.at(i);
                      }
                      std::cout << "Dientes en la cadena: " << total << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> dientes = {12, 40, 60, 24, 36};
                      int total = 0;
                      for (std::size_t i = 0; i < dientes.size(); i++) {
                          total += dientes.at(i);
                      }
                      std::cout << "Dientes en la cadena: " << total << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Ciento setenta y dos dientes, y el orco sigue durmiendo. Lima le dice a Bron que los números empiezan en cero, como la paciencia de Tesla.",
              imagen=["Una cadena vertical de engranajes numerados del 0 al 4 en una torre de reloj; en el lugar 5, un orco dormido.",
                      BRON + " retrocede en puntas de pie.", LIMA + " le hace señas de silencio."]),
            m(id="R01-N07-P2", titulo="La tabla de carreras",
              lugar="La pista alrededor de las torres", personajes="Lyn, Bron",
              carta="push_back y sort | v.push_back(x) agrega al final · std::sort(v.begin(), v.end()) ordena de menor a mayor (#include <algorithm>)",
              recompensa="xp 10, oro 10",
              escena="""
                  Lyn corrió varias vueltas y anotó cada tiempo en segundos. Quiere verlos ordenados, del mejor al peor, y saber el mejor. Bron los guarda, pero nunca los ordena.
              """,
              sugiere="Los tiempos ya se guardan con `push_back`. Falta ordenarlos con `std::sort(tiempos.begin(), tiempos.end());` antes de mostrarlos: el mejor queda primero.",
              desafio="Ordená los tiempos antes de mostrarlos.",
              entrada="64 58 71 55 60\n",
              inicial='''
                  #include <algorithm>
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> tiempos;
                      int t = 0;
                      while (std::cin >> t) {
                          tiempos.push_back(t);
                      }
                      std::cout << "Tiempos:";
                      for (int x : tiempos) {
                          std::cout << " " << x;
                      }
                      std::cout << "\\nMejor: " << tiempos[0] << " segundos\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <algorithm>
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> tiempos;
                      int t = 0;
                      while (std::cin >> t) {
                          tiempos.push_back(t);
                      }
                      std::sort(tiempos.begin(), tiempos.end());
                      std::cout << "Tiempos:";
                      for (int x : tiempos) {
                          std::cout << " " << x;
                      }
                      std::cout << "\\nMejor: " << tiempos[0] << " segundos\\n";
                      return 0;
                  }
              ''',
              al_superar="Cincuenta y cinco segundos. Lyn lo grita desde lo alto de la torre del reloj, para que lo escuche toda la Ciudadela.",
              imagen=["Un pizarrón en la pista con cinco tiempos ordenados de menor a mayor.",
                      LYN + " grita desde lo alto de una torre.", BRON + " escribe el último tiempo con tiza."]),
            m(id="R01-N07-P3", titulo="El tablero de la torre",
              lugar=TORRE, personajes="Bron, Tesla",
              carta="Grilla | std::vector<std::vector<char>> g(3, std::vector<char>(4, '.')); · g[fila][columna]",
              recompensa="xp 15, oro 15",
              escena="""
                  El tablero de control de la torre es una grilla de 3 filas y 4 columnas. Tesla le pide a Bron que marque con una `X` el engranaje roto, en la fila 1, columna 2. Bron marca la fila 2, columna 1.
              """,
              sugiere="Primero va la **fila** y después la **columna**: `tablero[1][2]`. Las dos empiezan en 0.",
              desafio="Marcá el engranaje en el lugar correcto.",
              inicial='''
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::vector<char>> tablero(3, std::vector<char>(4, '.'));
                      tablero[2][1] = 'X';
                      for (const std::vector<char>& fila : tablero) {
                          for (char c : fila) {
                              std::cout << c;
                          }
                          std::cout << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::vector<char>> tablero(3, std::vector<char>(4, '.'));
                      tablero[1][2] = 'X';
                      for (const std::vector<char>& fila : tablero) {
                          for (char c : fila) {
                              std::cout << c;
                          }
                          std::cout << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="La X cae justo sobre el engranaje que chirriaba. Tesla lo cambia en un minuto.",
              imagen=["Un tablero de bronce con 3 filas y 4 columnas de lucecitas; una en rojo.",
                      TESLA + " cambia un engranaje en la pared de la torre.", BRON + " señala el tablero."]),
        ],
    },
    {
        "titulo": "R01-N08 · Azar y matemáticas",
        "misiones": [
            m(id="R01-N08-P1", titulo="La rueda de Lyn",
              lugar=FERIA, personajes="Lyn, Tesla",
              carta="Semilla | std::mt19937 gen(semilla); · gen() da el siguiente número · la misma semilla da SIEMPRE la misma secuencia",
              recompensa="xp 10, oro 10",
              escena="""
                  Lyn apuesta al número de la rueda de la feria y gana diez veces seguidas. Tesla desarma la rueda: alguien la arranca siempre desde la misma posición, la **semilla** 7.
                  —Que la semilla la elija el feriante cada mañana —dice Tesla.
              """,
              sugiere="La semilla ya no puede estar fija: leela de la entrada y pasásela al generador. `gen() % 6 + 1` da un número del 1 al 6 (acá se usa así para que dé igual en el navegador y en tu compu).",
              desafio="Leé la semilla de la entrada en lugar de usar siempre la 7.",
              entrada="2026\n",
              inicial='''
                  #include <iostream>
                  #include <random>

                  int main()
                  {
                      unsigned int semilla = 0;
                      std::cin >> semilla;
                      std::mt19937 gen(7);
                      for (int i = 0; i < 3; i++) {
                          std::cout << "Tirada: " << gen() % 6 + 1 << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <random>

                  int main()
                  {
                      unsigned int semilla = 0;
                      std::cin >> semilla;
                      std::mt19937 gen(semilla);
                      for (int i = 0; i < 3; i++) {
                          std::cout << "Tirada: " << gen() % 6 + 1 << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Con la semilla del día la rueda cambia, y Lyn pierde dos de tres. Devuelve los premios. Casi todos.",
              imagen=["Una rueda de feria con números del 1 al 6 y una palanca de bronce.",
                      LYN + " abraza una pila de premios.", TESLA + " tiene en la mano una pieza de la rueda desarmada."]),
            m(id="R01-N08-P2", titulo="La distancia más corta",
              lugar="La plaza de las torres", personajes="Bron, Lima",
              carta="cmath | std::hypot(dx, dy) da la distancia en línea recta · std::sqrt, std::pow · std::round redondea",
              recompensa="xp 10, oro 10",
              escena="""
                  Bron está en la esquina (1, 2) de la plaza y Lima en la (4, 6). Bron calcula cuánto tiene que caminar sumando los dos lados: 7. Lima cruza en diagonal y llega antes.
              """,
              sugiere="En línea recta la distancia es la hipotenusa: `std::hypot(dx, dy)`, con `dx` y `dy` las diferencias de cada coordenada.",
              desafio="Calculá la distancia en línea recta.",
              inicial='''
                  #include <cmath>
                  #include <iostream>

                  int main()
                  {
                      double x1 = 1, y1 = 2;
                      double x2 = 4, y2 = 6;
                      double dx = x2 - x1;
                      double dy = y2 - y1;
                      double distancia = dx + dy;
                      std::cout << "Distancia: " << distancia << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <cmath>
                  #include <iostream>

                  int main()
                  {
                      double x1 = 1, y1 = 2;
                      double x2 = 4, y2 = 6;
                      double dx = x2 - x1;
                      double dy = y2 - y1;
                      double distancia = std::hypot(dx, dy);
                      std::cout << "Distancia: " << distancia << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Cinco, no siete. Bron cruza en diagonal por primera vez y pisa una baldosa floja.",
              imagen=["Una plaza con baldosas en cuadrícula; un camino en L y una diagonal marcada con tiza.",
                      LIMA + " ya llegó por la diagonal.", BRON + " camina por la L."]),
            m(id="R01-N08-P3", titulo="La aguja del manómetro",
              lugar="La sala de calderas", personajes="Bron, Tesla",
              carta="clamp | std::clamp(x, min, max) deja x dentro del rango (#include <algorithm>) · std::min y std::max eligen entre dos",
              recompensa="xp 10, oro 10",
              escena="""
                  El manómetro de la caldera tiene una aguja que va de 0 a 100. Cuando la presión se pasa, la aguja da la vuelta entera y marca cualquier cosa. Tesla quiere que se quede quieta en el tope.
              """,
              sugiere="`std::clamp(presion, 0, 100)` devuelve la presión, pero nunca menos de 0 ni más de 100.",
              desafio="Limitá la aguja al rango del manómetro.",
              entrada="-10 45 130\n",
              inicial='''
                  #include <algorithm>
                  #include <iostream>

                  int main()
                  {
                      int presion = 0;
                      while (std::cin >> presion) {
                          int aguja = presion;
                          std::cout << "Presion " << presion << " -> aguja en " << aguja << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <algorithm>
                  #include <iostream>

                  int main()
                  {
                      int presion = 0;
                      while (std::cin >> presion) {
                          int aguja = std::clamp(presion, 0, 100);
                          std::cout << "Presion " << presion << " -> aguja en " << aguja << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Con 130 la aguja se queda en 100 y suena una alarma, como corresponde. Tesla baja la presión con una palanca.",
              imagen=["Un manómetro de bronce con la aguja clavada en el tope, junto a una caldera que echa vapor.",
                      TESLA + " baja una palanca.", BRON + " lee el manómetro."]),
        ],
    },
    {
        "titulo": "R01-N09 · Jefe: el Autómata de Latón",
        "misiones": [
            m(id="R01-N09-P1", titulo="La tarjeta perforada",
              lugar=PATIO, personajes="Bron, Tesla, Gheco",
              criatura="dragon",
              carta="Leer hasta un centinela | while (std::cin >> orden && orden != \"FIN\") { ... } · se cuenta lo que llega",
              recompensa="xp 15, oro 15",
              escena="""
                  En el patio de pruebas espera el **Autómata de Latón**, con una tarjeta perforada en la frente: «ORDEN: NO DEJAR PASAR A NADIE QUE NO DOMINE LOS CIMIENTOS». Bron saca la llave para desarmarlo tornillo por tornillo.
                  Tesla le saca la llave de la mano. —Con un plan. Primero, leé qué órdenes tiene grabadas.
              """,
              sugiere="Las órdenes llegan una por palabra hasta `FIN`. Contá las que dicen `girar` y las que dicen `golpear`; el bucle ya se detiene en `FIN`.",
              desafio="Contá cada tipo de orden.",
              entrada="girar golpear girar girar golpear FIN girar\n",
              inicial='''
                  #include <iostream>
                  #include <string>

                  int main()
                  {
                      std::string orden;
                      int giros = 0;
                      int golpes = 0;
                      while (std::cin >> orden && orden != "FIN") {
                      }
                      std::cout << "Giros: " << giros << ", golpes: " << golpes << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  int main()
                  {
                      std::string orden;
                      int giros = 0;
                      int golpes = 0;
                      while (std::cin >> orden && orden != "FIN") {
                          if (orden == "girar") {
                              giros++;
                          } else if (orden == "golpear") {
                              golpes++;
                          }
                      }
                      std::cout << "Giros: " << giros << ", golpes: " << golpes << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres giros y dos golpes: el Autómata siempre repite el mismo patrón. Gheco lo anota: ya se sabe qué va a hacer.",
              imagen=["Un patio de pruebas con " + AUTOMATA + ".",
                      BRON + " lee una tarjeta perforada.", TESLA + " le sostiene la llave, lejos de su alcance."]),
            m(id="R01-N09-P2", titulo="Las placas más fuertes",
              lugar=PATIO, personajes="Bron, Lima",
              criatura="dragon",
              carta="Función con referencias | void extremos(const std::vector<int>& v, int& menor, int& mayor) · const & para no copiar el vector",
              recompensa="xp 15, oro 15",
              escena="""
                  Las placas del Autómata tienen distinta dureza. Lima quiere saber cuál es la más blanda (por ahí se entra) y cuál la más dura (esa ni intentarla). La función de Bron solo encuentra la más dura.
              """,
              sugiere="Arrancá `menor` y `mayor` con el primer elemento, y en el recorrido actualizá los dos.",
              desafio="Completá la búsqueda de la placa más blanda.",
              entrada="34 12 58 9 41\n",
              inicial='''
                  #include <iostream>
                  #include <vector>

                  void extremos(const std::vector<int>& placas, int& menor, int& mayor)
                  {
                      menor = placas[0];
                      mayor = placas[0];
                      for (int p : placas) {
                          if (p > mayor) {
                              mayor = p;
                          }
                      }
                  }

                  int main()
                  {
                      std::vector<int> placas;
                      int p = 0;
                      while (std::cin >> p) {
                          placas.push_back(p);
                      }
                      int menor = 0;
                      int mayor = 0;
                      extremos(placas, menor, mayor);
                      std::cout << "Mas blanda: " << menor << ", mas dura: " << mayor << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <vector>

                  void extremos(const std::vector<int>& placas, int& menor, int& mayor)
                  {
                      menor = placas[0];
                      mayor = placas[0];
                      for (int p : placas) {
                          if (p > mayor) {
                              mayor = p;
                          }
                          if (p < menor) {
                              menor = p;
                          }
                      }
                  }

                  int main()
                  {
                      std::vector<int> placas;
                      int p = 0;
                      while (std::cin >> p) {
                          placas.push_back(p);
                      }
                      int menor = 0;
                      int mayor = 0;
                      extremos(placas, menor, mayor);
                      std::cout << "Mas blanda: " << menor << ", mas dura: " << mayor << "\\n";
                      return 0;
                  }
              ''',
              al_superar="La placa de dureza 9 está en la rodilla izquierda. Lima la marca con tiza.",
              imagen=["Las piernas de " + AUTOMATA + " con una placa marcada con tiza en la rodilla.",
                      LIMA + " marca la placa.", BRON + " sostiene la lista de durezas."]),
            m(id="R01-N09-P3", titulo="Las palancas con semilla",
              lugar=PATIO, personajes="Bron, Tesla",
              criatura="dragon",
              carta="Azar repetible | con la misma semilla el Autómata hace siempre lo mismo · probar con una semilla fija es probar siempre el mismo caso",
              recompensa="xp 15, oro 15",
              escena="""
                  El Autómata elige al azar qué brazo mover, pero Tesla lo construyó con una semilla fija: 47, el engranaje donde se melló la llave de Bron. Si Bron simula los primeros movimientos, sabe por dónde va a venir cada golpe.
              """,
              sugiere="`gen() % 2` da 0 o 1: 0 es el brazo izquierdo y 1 el derecho. La semilla tiene que ser la del Autómata, 47, y hay que mostrar cinco movimientos.",
              desafio="Usá la semilla del Autómata y simulá cinco movimientos.",
              inicial='''
                  #include <iostream>
                  #include <random>
                  #include <string>

                  int main()
                  {
                      std::mt19937 gen(1);
                      for (int i = 1; i <= 3; i++) {
                          std::string brazo = gen() % 2 == 0 ? "izquierdo" : "derecho";
                          std::cout << "Golpe " << i << ": brazo " << brazo << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <random>
                  #include <string>

                  int main()
                  {
                      std::mt19937 gen(47);
                      for (int i = 1; i <= 5; i++) {
                          std::string brazo = gen() % 2 == 0 ? "izquierdo" : "derecho";
                          std::cout << "Golpe " << i << ": brazo " << brazo << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Bron esquiva cinco golpes seguidos sin mirar. El Autómata silba vapor, confundido.",
              imagen=["El patio de pruebas: " + AUTOMATA + " lanza un puñetazo con un brazo.",
                      BRON + " lo esquiva con un paso al costado, mirando una hoja con anotaciones.", TESLA + " aplaude desde atrás."]),
            m(id="R01-N09-P4", titulo="El corazón de vapor",
              lugar=PATIO, personajes="Bron, Tesla, Lima",
              criatura="dragon",
              carta="Partir en funciones | cada función hace una cosa y se prueba sola · main solo las junta",
              recompensa="xp 25, oro 30",
              item="Engranaje de Latón",
              escena="""
                  Para detener al Autómata hay que llegar a su corazón de vapor con la secuencia justa: por cada placa, si su dureza es par se gira la llave, si es impar se golpea, y al final se cuenta cuántas veces se giró. Bron lo escribió todo en `main`, y se perdió.
                  —Partilo —dice Tesla—. Una función por cosa.
              """,
              sugiere="Completá `accion`: devuelve `\"girar\"` si la dureza es par y `\"golpear\"` si es impar. El resto del plan ya está armado.",
              desafio="Escribí la función que decide la acción de cada placa.",
              entrada="34 12 58 9 41\n",
              inicial='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  std::vector<int> leer_placas()
                  {
                      std::vector<int> placas;
                      int p = 0;
                      while (std::cin >> p) {
                          placas.push_back(p);
                      }
                      return placas;
                  }

                  std::string accion(int dureza)
                  {
                      return "esperar";
                  }

                  int main()
                  {
                      std::vector<int> placas = leer_placas();
                      int giros = 0;
                      for (int p : placas) {
                          std::string a = accion(p);
                          std::cout << p << ": " << a << "\\n";
                          if (a == "girar") {
                              giros++;
                          }
                      }
                      std::cout << "Giros: " << giros << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  std::vector<int> leer_placas()
                  {
                      std::vector<int> placas;
                      int p = 0;
                      while (std::cin >> p) {
                          placas.push_back(p);
                      }
                      return placas;
                  }

                  std::string accion(int dureza)
                  {
                      if (dureza % 2 == 0) {
                          return "girar";
                      }
                      return "golpear";
                  }

                  int main()
                  {
                      std::vector<int> placas = leer_placas();
                      int giros = 0;
                      for (int p : placas) {
                          std::string a = accion(p);
                          std::cout << p << ": " << a << "\\n";
                          if (a == "girar") {
                              giros++;
                          }
                      }
                      std::cout << "Giros: " << giros << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres giros y dos golpes después, el Autómata se detiene con un último silbido. De su pecho cae el **Engranaje de Latón**, todavía tibio. —Bien —dice Tesla—. Y no preguntes para qué te sirve.",
              imagen=[AUTOMATA + " detenido, con la ventanita del pecho abierta y sin vapor.",
                      BRON + " sostiene un engranaje de latón tibio.", TESLA + " y " + LIMA + " sonríen detrás."]),
        ],
    },
]
