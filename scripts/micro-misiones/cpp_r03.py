from gencpp import m
from cpp_r01 import BRON, TESLA, LIMA, LYN, OTO, GHECO

TALLERES = "Los Talleres Modernos"
ADUANA = "La oficina de la Aduana de la Ciudadela"
FICHERO = "El fichero del archivista"
CONTROL = "La sala de control"
CLASIFICADOR = "El clasificador de piezas"
ARCHIVO = "El Archivo de los registros"
DEPOSITO = "El depósito de autómatas"
SALA = "La sala de máquinas"
BESTIARIO = "El Bestiario de los Talleres"
MAESTRA = "la Maestra Artífice (mujer alta de 60, piel oscura, pelo blanco muy corto, antiparras verdes en la frente, delantal de cuero sobre una túnica verde con circuitos, tableta con tildes verdes)"
MIMICO = "el Mímico del Bestiario (criatura gris y blanda como cera, que imita a quien mira con algo mal copiado: una cola de más, un ojo en la rodilla)"

NODOS = [
    {
        "titulo": "R03-N01 · auto, array y el for de rango",
        "misiones": [
            m(id="R03-N01-P1", titulo="El goblin de la copia",
              lugar=TALLERES, personajes="Bron, Lima",
              criatura="goblin",
              carta="for de rango | for (auto x : v) trabaja con COPIAS · for (auto& x : v) cambia los originales · for (const auto& x : v) solo lee",
              recompensa="xp 10, oro 10",
              escena="""
                  En los Talleres Modernos, Bron escribe `auto` en todos lados, encantado. Quiere duplicar la carga de cada vagoneta, pero las vagonetas siguen igual: un **goblin** se esconde en cada copia que no quería hacer.
              """,
              sugiere="`auto x` es una copia: duplicarla no toca el vector. Para cambiar cada elemento, `auto& x`.",
              desafio="Hacé que el bucle cambie las vagonetas de verdad.",
              inicial='''
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> carga = {3, 7, 2, 5};
                      for (auto x : carga) {
                          x *= 2;
                      }
                      std::cout << "Cargas:";
                      for (const auto& x : carga) {
                          std::cout << " " << x;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> carga = {3, 7, 2, 5};
                      for (auto& x : carga) {
                          x *= 2;
                      }
                      std::cout << "Cargas:";
                      for (const auto& x : carga) {
                          std::cout << " " << x;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Las vagonetas salen con el doble. Lima le señala el `&` con la punta de la lima: —Ese chiquito hace todo.",
              imagen=["Cuatro vagonetas de bronce cargadas en un taller luminoso.",
                      "Un goblin escapa con una vagoneta de juguete (la copia).", BRON + " y " + LIMA + " lo miran irse."]),
            m(id="R03-N01-P2", titulo="Nombre y pisos, cada uno en su lugar",
              lugar=TALLERES, personajes="Bron, Tesla",
              carta="Structured bindings | for (const auto& [nombre, pisos] : torres) · separa un par o un struct en variables con nombre, en orden",
              recompensa="xp 10, oro 10",
              escena="""
                  Tesla le enseña a Bron a separar cada par en dos variables con nombre. Bron las nombró al revés, y la Ciudadela tiene ahora una torre llamada «12» con «Reloj» pisos.
              """,
              sugiere="Los nombres van en el **orden** de los campos del par: primero el `first` (el nombre), después el `second` (los pisos).",
              desafio="Poné los nombres en el orden correcto.",
              inicial='''
                  #include <iostream>
                  #include <string>
                  #include <utility>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::pair<std::string, int>> torres = {{"Reloj", 12}, {"Poleas", 8}};
                      for (const auto& [pisos, nombre] : torres) {
                          std::cout << "Torre " << nombre << ": " << pisos << " pisos\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>
                  #include <utility>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::pair<std::string, int>> torres = {{"Reloj", 12}, {"Poleas", 8}};
                      for (const auto& [nombre, pisos] : torres) {
                          std::cout << "Torre " << nombre << ": " << pisos << " pisos\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="La torre del Reloj recupera su nombre. Tesla dice que el código ahora se lee solo.",
              imagen=["Dos torres con carteles; uno de los carteles está al revés.",
                      TESLA + " da vuelta el cartel.", BRON + " se ríe de su error."]),
            m(id="R03-N01-P3", titulo="La semana del taller",
              lugar=TALLERES, personajes="Lima, Bron",
              carta="std::array | std::array<int, 7> horas = {...}; · tamaño fijo, lo sabe el compilador · horas.size() · si sobran valores, no compila",
              recompensa="xp 10, oro 10",
              escena="""
                  Lima anota las horas de trabajo de cada día de la semana en un `std::array`. Bron le hizo uno de seis lugares, y la semana tiene siete días: el Taller no lo deja compilar.
              """,
              sugiere="En `std::array<int, N>`, `N` es la cantidad de lugares. Una semana tiene 7.",
              desafio="Dale al array el tamaño de la semana.",
              inicial='''
                  #include <array>
                  #include <iostream>

                  int main()
                  {
                      std::array<int, 6> horas = {8, 7, 9, 8, 6, 4, 2};
                      int total = 0;
                      for (int h : horas) {
                          total += h;
                      }
                      std::cout << horas.size() << " dias, " << total << " horas\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <array>
                  #include <iostream>

                  int main()
                  {
                      std::array<int, 7> horas = {8, 7, 9, 8, 6, 4, 2};
                      int total = 0;
                      for (int h : horas) {
                          total += h;
                      }
                      std::cout << horas.size() << " dias, " << total << " horas\\n";
                      return 0;
                  }
              ''',
              al_superar="Siete días, cuarenta y cuatro horas. Lima subraya el domingo: dos horas, «solo para limar».",
              imagen=["Un calendario de bronce con siete casilleros y horas anotadas.",
                      LIMA + " subraya el domingo.", BRON + " bosteza."]),
        ],
    },
    {
        "titulo": "R03-N02 · Textos a fondo",
        "misiones": [
            m(id="R03-N02-P1", titulo="La planilla con punto y coma",
              lugar=ADUANA, personajes="Bron, Lima",
              carta="find y substr | t.find(';') da la posición del ; · t.substr(desde, cuantos) corta un pedazo · t.substr(desde) hasta el final",
              recompensa="xp 10, oro 10",
              escena="""
                  En la Aduana llegan planillas como «Lima;27;relojera». Bron corta el nombre, pero se lleva también el punto y coma, y el escriba anota a «Lima;».
              """,
              sugiere="Si el `;` está en la posición `p`, el nombre son los `p` caracteres desde el 0: `substr(0, p)`. Lo que sigue empieza en `p + 1`.",
              desafio="Cortá el nombre sin el punto y coma.",
              entrada="Lima;27;relojera\n",
              inicial='''
                  #include <iostream>
                  #include <string>

                  int main()
                  {
                      std::string linea;
                      std::getline(std::cin, linea);
                      std::size_t p = linea.find(';');
                      std::string nombre = linea.substr(0, p + 1);
                      std::string resto = linea.substr(p + 1);
                      std::cout << "Nombre: [" << nombre << "]\\n";
                      std::cout << "Resto: [" << resto << "]\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  int main()
                  {
                      std::string linea;
                      std::getline(std::cin, linea);
                      std::size_t p = linea.find(';');
                      std::string nombre = linea.substr(0, p);
                      std::string resto = linea.substr(p + 1);
                      std::cout << "Nombre: [" << nombre << "]\\n";
                      std::cout << "Resto: [" << resto << "]\\n";
                      return 0;
                  }
              ''',
              al_superar="«Lima», limpito. El escriba lo anota y le devuelve a Lima su punto y coma.",
              imagen=["Un escritorio de Aduana con planillas apiladas y una tijera de bronce.",
                      BRON + " corta una tira de papel.", LIMA + " revisa el corte con la lupa."]),
            m(id="R03-N02-P2", titulo="27120",
              lugar=ADUANA, personajes="Bron, Lima",
              carta="Texto a número | std::stoi(\"27\") da 27 · std::stod para decimales · std::to_string(27) al revés · \"27\" + \"120\" pega textos",
              recompensa="xp 10, oro 10",
              escena="""
                  Bron suma las edades de las planillas y le da **27120**. El escriba se desmaya. Lima lo abanica con la planilla: las edades eran texto, y sumar textos los pega.
              """,
              sugiere="Convertí cada edad con `std::stoi` antes de sumarla.",
              desafio="Sumá las edades como números.",
              entrada="27 120 19\n",
              inicial='''
                  #include <iostream>
                  #include <string>

                  int main()
                  {
                      std::string edad;
                      std::string suma;
                      while (std::cin >> edad) {
                          suma += edad;
                      }
                      std::cout << "Suma de edades: " << suma << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  int main()
                  {
                      std::string edad;
                      int suma = 0;
                      while (std::cin >> edad) {
                          suma += std::stoi(edad);
                      }
                      std::cout << "Suma de edades: " << suma << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Ciento sesenta y seis. El escriba se despierta, lo revisa, y se vuelve a desmayar porque alguien tiene 120.",
              imagen=["Un escriba desmayado en su silla con una planilla en la mano.",
                      LIMA + " lo abanica.", BRON + " mira el número 27120 escrito en la pizarra, avergonzado."]),
            m(id="R03-N02-P3", titulo="Las palabras de Oto",
              lugar=ADUANA, personajes="Oto, Bron",
              carta="istringstream | std::istringstream ss(linea); while (ss >> palabra) · lee palabra por palabra, salteando todos los espacios",
              recompensa="xp 15, oro 15",
              escena="""
                  Oto dicta su receta con espacios por todos lados, y el contador de palabras de Bron (que cuenta espacios) le da un número disparatado. Oto jura que dijo cuatro palabras.
              """,
              sugiere="Un `std::istringstream` sobre la línea lee con `>>` palabra por palabra y se saltea los espacios de más. Contá las vueltas.",
              desafio="Contá las palabras con un `istringstream`.",
              entrada="  Oto   cocina  guiso   violeta \n",
              inicial='''
                  #include <iostream>
                  #include <sstream>
                  #include <string>

                  int main()
                  {
                      std::string linea;
                      std::getline(std::cin, linea);
                      int palabras = 1;
                      for (char c : linea) {
                          if (c == ' ') {
                              palabras++;
                          }
                      }
                      std::cout << "Palabras: " << palabras << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <sstream>
                  #include <string>

                  int main()
                  {
                      std::string linea;
                      std::getline(std::cin, linea);
                      std::istringstream ss(linea);
                      std::string palabra;
                      int palabras = 0;
                      while (ss >> palabra) {
                          palabras++;
                      }
                      std::cout << "Palabras: " << palabras << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Cuatro, como dijo Oto. «Guiso violeta» queda anotado como receta oficial, para espanto de la Maestra Artífice.",
              imagen=["Una hoja de receta con palabras muy separadas entre sí.",
                      OTO + " dicta con el cucharón en alto.", BRON + " cuenta con los dedos."]),
        ],
    },
    {
        "titulo": "R03-N03 · Diccionarios y conjuntos",
        "misiones": [
            m(id="R03-N03-P1", titulo="El inventario que cuenta",
              lugar=FICHERO, personajes="Bron, Lima",
              carta="map para contar | std::map<std::string, int> conteo; conteo[pieza]++; · la primera vez arranca en 0 · se recorre ordenado por clave",
              recompensa="xp 10, oro 10",
              escena="""
                  El archivista quiere saber cuántas piezas de cada tipo llegaron. El fichero de Bron anota cada pieza, pero siempre con un 1: nunca suma.
              """,
              sugiere="`conteo[pieza]++` suma uno a lo que ya había (la primera vez, a 0).",
              desafio="Contá cuántas veces llega cada pieza.",
              entrada="engranaje resorte engranaje tuerca engranaje resorte\n",
              inicial='''
                  #include <iostream>
                  #include <map>
                  #include <string>

                  int main()
                  {
                      std::map<std::string, int> conteo;
                      std::string pieza;
                      while (std::cin >> pieza) {
                          conteo[pieza] = 1;
                      }
                      for (const auto& [nombre, cantidad] : conteo) {
                          std::cout << nombre << ": " << cantidad << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <map>
                  #include <string>

                  int main()
                  {
                      std::map<std::string, int> conteo;
                      std::string pieza;
                      while (std::cin >> pieza) {
                          conteo[pieza]++;
                      }
                      for (const auto& [nombre, cantidad] : conteo) {
                          std::cout << nombre << ": " << cantidad << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Tres engranajes, dos resortes, una tuerca, y en orden alfabético. El archivista no lo podía creer.",
              imagen=["Un fichero de madera con tarjetas: engranaje 3, resorte 2, tuerca 1.",
                      BRON + " pone tarjetas en el fichero.", LIMA + " las ordena."]),
            m(id="R03-N03-P2", titulo="Buscar sin inventar",
              lugar=FICHERO, personajes="Bron, Tesla",
              carta="Consultar sin crear | fichero[\"x\"] CREA la entrada si no está · fichero.find(\"x\") == fichero.end() o fichero.contains(\"x\") solo preguntan",
              recompensa="xp 15, oro 15",
              escena="""
                  Bron pregunta en el fichero dónde está la «palanca», que no existe. El fichero responde «cajón 0»… y desde ese momento la palanca existe, en el cajón 0, que está vacío. Tesla suspira.
              """,
              sugiere="Con `[]` preguntar crea la ficha. Usá `fichero.contains(\"palanca\")` (o `find`) para preguntar sin crear nada.",
              desafio="Preguntá sin agregar fichas falsas.",
              inicial='''
                  #include <iostream>
                  #include <map>
                  #include <string>

                  int main()
                  {
                      std::map<std::string, int> fichero = {{"reloj", 14}, {"polea", 3}, {"vitral", 9}};
                      for (std::string buscado : {"reloj", "palanca"}) {
                          if (fichero[buscado] != 0) {
                              std::cout << buscado << ": cajon " << fichero[buscado] << "\\n";
                          } else {
                              std::cout << buscado << ": no esta\\n";
                          }
                      }
                      std::cout << "Fichas: " << fichero.size() << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <map>
                  #include <string>

                  int main()
                  {
                      std::map<std::string, int> fichero = {{"reloj", 14}, {"polea", 3}, {"vitral", 9}};
                      for (std::string buscado : {"reloj", "palanca"}) {
                          if (fichero.contains(buscado)) {
                              std::cout << buscado << ": cajon " << fichero.at(buscado) << "\\n";
                          } else {
                              std::cout << buscado << ": no esta\\n";
                          }
                      }
                      std::cout << "Fichas: " << fichero.size() << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres fichas, como antes. La palanca sigue sin existir, que es lo que tiene que hacer.",
              imagen=["Un fichero con una tarjeta en blanco que dice «palanca» tachada.",
                      TESLA + " saca la tarjeta en blanco.", BRON + " se rasca la cabeza."]),
            m(id="R03-N03-P3", titulo="Los aprobados, una sola vez",
              lugar=FICHERO, personajes="Oto, Lima",
              carta="set | std::set<std::string> guarda cada cosa UNA vez y ordenada · insert de algo repetido no hace nada · .size()",
              recompensa="xp 10, oro 10",
              escena="""
                  En el libro de los aprobados nadie aparece dos veces. Oto quiere anotar su guiso dos veces «porque estaba muy bueno». El libro de Bron es un vector y lo deja.
              """,
              sugiere="Cambiá el vector por un `std::set`: `insert` de algo repetido no lo agrega. Y sale ordenado solo.",
              desafio="Usá un conjunto para que no haya repetidos.",
              entrada="guiso pan guiso sopa pan guiso\n",
              inicial='''
                  #include <iostream>
                  #include <set>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::string> aprobados;
                      std::string plato;
                      while (std::cin >> plato) {
                          aprobados.push_back(plato);
                      }
                      std::cout << "Aprobados (" << aprobados.size() << "):";
                      for (const auto& p : aprobados) {
                          std::cout << " " << p;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <set>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::set<std::string> aprobados;
                      std::string plato;
                      while (std::cin >> plato) {
                          aprobados.insert(plato);
                      }
                      std::cout << "Aprobados (" << aprobados.size() << "):";
                      for (const auto& p : aprobados) {
                          std::cout << " " << p;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres platos, una vez cada uno. Oto se ofende un poquito, y después se le pasa.",
              imagen=["Un libro de aprobados con tres renglones: guiso, pan, sopa.",
                      OTO + " intenta escribir «guiso» otra vez.", LIMA + " le saca la pluma."]),
        ],
    },
    {
        "titulo": "R03-N04 · Estados y valores que pueden faltar",
        "misiones": [
            m(id="R03-N04-P1", titulo="Las luces del tablero",
              lugar=CONTROL, personajes="Bron, Tesla",
              carta="enum class | enum class Estado { Apagado, Girando, Averiado }; · Estado::Girando · un switch lo pasa a texto",
              recompensa="xp 10, oro 10",
              escena="""
                  El tablero de control ya no usa números pintados a mano: cada máquina tiene un **estado** con nombre. Pero la función que lo pasa a texto se olvidó de las averiadas, y las muestra con un signo de pregunta.
              """,
              sugiere="Agregá el `case Estado::Averiado` que devuelva `\"averiado\"`.",
              desafio="Completá la conversión del estado a texto.",
              inicial='''
                  #include <iostream>
                  #include <string>

                  enum class Estado { Apagado, Girando, Averiado };

                  std::string texto(Estado e)
                  {
                      switch (e) {
                      case Estado::Apagado:
                          return "apagado";
                      case Estado::Girando:
                          return "girando";
                      default:
                          return "?";
                      }
                  }

                  int main()
                  {
                      Estado calderas[] = {Estado::Girando, Estado::Averiado, Estado::Apagado};
                      for (Estado e : calderas) {
                          std::cout << "Caldera: " << texto(e) << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  enum class Estado { Apagado, Girando, Averiado };

                  std::string texto(Estado e)
                  {
                      switch (e) {
                      case Estado::Apagado:
                          return "apagado";
                      case Estado::Girando:
                          return "girando";
                      case Estado::Averiado:
                          return "averiado";
                      default:
                          return "?";
                      }
                  }

                  int main()
                  {
                      Estado calderas[] = {Estado::Girando, Estado::Averiado, Estado::Apagado};
                      for (Estado e : calderas) {
                          std::cout << "Caldera: " << texto(e) << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="La segunda caldera dice «averiado» con todas las letras. Bron la apaga antes de que haga algo peor.",
              imagen=["Un tablero de control con tres luces: verde «girando», roja «averiado», gris «apagado».",
                      TESLA + " señala la luz roja.", BRON + " corre hacia una caldera."]),
            m(id="R03-N04-P2", titulo="Sin menos uno",
              lugar=CONTROL, personajes="Bron, Lima",
              carta="optional | std::optional<int> buscar(...) devuelve el valor o std::nullopt · if (r) pregunta si hay · *r lo saca",
              recompensa="xp 15, oro 15",
              escena="""
                  La función que busca una máquina en el tablero devuelve **−1** cuando no la encuentra, y el tablero muestra «cajón −1». El día que Bron leyó el −1 como un cajón, abrió la pared.
              """,
              sugiere="Que la función devuelva `std::optional<int>`: la posición si la encuentra, `std::nullopt` si no. En `main`, preguntá con `if (r)`.",
              desafio="Reemplazá el −1 por un `optional`.",
              inicial='''
                  #include <iostream>
                  #include <optional>
                  #include <string>
                  #include <vector>

                  int buscar(const std::vector<std::string>& maquinas, const std::string& nombre)
                  {
                      for (std::size_t i = 0; i < maquinas.size(); i++) {
                          if (maquinas[i] == nombre) {
                              return static_cast<int>(i);
                          }
                      }
                      return -1;
                  }

                  int main()
                  {
                      std::vector<std::string> maquinas = {"caldera", "telar", "grua"};
                      for (std::string n : {"telar", "molino"}) {
                          int r = buscar(maquinas, n);
                          std::cout << n << ": cajon " << r << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <optional>
                  #include <string>
                  #include <vector>

                  std::optional<int> buscar(const std::vector<std::string>& maquinas, const std::string& nombre)
                  {
                      for (std::size_t i = 0; i < maquinas.size(); i++) {
                          if (maquinas[i] == nombre) {
                              return static_cast<int>(i);
                          }
                      }
                      return std::nullopt;
                  }

                  int main()
                  {
                      std::vector<std::string> maquinas = {"caldera", "telar", "grua"};
                      for (std::string n : {"telar", "molino"}) {
                          std::optional<int> r = buscar(maquinas, n);
                          if (r) {
                              std::cout << n << ": cajon " << *r << "\\n";
                          } else {
                              std::cout << n << ": no esta\\n";
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="El molino «no está», y nadie abre la pared. Lima tacha el −1 de su cuaderno con dos rayas.",
              imagen=["Una pared de la sala de control con un agujero mal tapado.",
                      LIMA + " tacha un −1 en un cuaderno.", BRON + " tapa el agujero con un tablón."]),
            m(id="R03-N04-P3", titulo="La caldera que cambia de estado",
              lugar=CONTROL, personajes="Bron, Tesla",
              carta="Máquina de estados | según el estado actual y el evento, se pasa a otro estado · switch (estado) y adentro un if por evento",
              recompensa="xp 15, oro 15",
              escena="""
                  La caldera se prende, se avería y se arregla. Tesla dibuja el diagrama: apagada → (prender) → girando → (falla) → averiada → (arreglar) → apagada. A la máquina de Bron le falta la flecha de «arreglar».
              """,
              sugiere="En el `case Estado::Averiado`, si el evento es `arreglar`, el estado pasa a `Apagado`.",
              desafio="Agregá la transición que falta.",
              entrada="prender falla prender arreglar prender\n",
              inicial='''
                  #include <iostream>
                  #include <string>

                  enum class Estado { Apagado, Girando, Averiado };

                  std::string texto(Estado e)
                  {
                      switch (e) {
                      case Estado::Apagado: return "apagada";
                      case Estado::Girando: return "girando";
                      case Estado::Averiado: return "averiada";
                      }
                      return "?";
                  }

                  int main()
                  {
                      Estado e = Estado::Apagado;
                      std::string evento;
                      while (std::cin >> evento) {
                          switch (e) {
                          case Estado::Apagado:
                              if (evento == "prender") e = Estado::Girando;
                              break;
                          case Estado::Girando:
                              if (evento == "falla") e = Estado::Averiado;
                              break;
                          case Estado::Averiado:
                              break;
                          }
                          std::cout << evento << " -> " << texto(e) << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  enum class Estado { Apagado, Girando, Averiado };

                  std::string texto(Estado e)
                  {
                      switch (e) {
                      case Estado::Apagado: return "apagada";
                      case Estado::Girando: return "girando";
                      case Estado::Averiado: return "averiada";
                      }
                      return "?";
                  }

                  int main()
                  {
                      Estado e = Estado::Apagado;
                      std::string evento;
                      while (std::cin >> evento) {
                          switch (e) {
                          case Estado::Apagado:
                              if (evento == "prender") e = Estado::Girando;
                              break;
                          case Estado::Girando:
                              if (evento == "falla") e = Estado::Averiado;
                              break;
                          case Estado::Averiado:
                              if (evento == "arreglar") e = Estado::Apagado;
                              break;
                          }
                          std::cout << evento << " -> " << texto(e) << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Averiada, arreglada, girando otra vez. Tesla le agrega una flecha al diagrama con tiza: la que dibujó Bron.",
              imagen=["Un pizarrón con un diagrama de tres círculos unidos por flechas.",
                      TESLA + " dibuja una flecha.", BRON + " sostiene la tiza."]),
        ],
    },
    {
        "titulo": "R03-N05 · Lambdas",
        "misiones": [
            m(id="R03-N05-P1", titulo="La regla en la tarjeta",
              lugar=CLASIFICADOR, personajes="Bron, Lima",
              carta="Lambda | [](const Pieza& a, const Pieza& b) { return a.peso > b.peso; } · una función sin nombre, escrita donde se usa",
              recompensa="xp 10, oro 10",
              escena="""
                  El clasificador ordena piezas, pero no sabe **cómo**: hay que darle una tarjeta con la regla. Bron escribió la tarjeta al revés, y la más liviana sale primero.
              """,
              sugiere="Para que la más pesada vaya primero, la lambda devuelve `true` cuando `a` pesa **más** que `b`.",
              desafio="Corregí la regla de la tarjeta.",
              inicial='''
                  #include <algorithm>
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  struct Pieza {
                      std::string nombre;
                      int peso;
                  };

                  int main()
                  {
                      std::vector<Pieza> piezas = {{"tuerca", 2}, {"yunque", 90}, {"engranaje", 15}, {"resorte", 1}};
                      std::sort(piezas.begin(), piezas.end(), [](const Pieza& a, const Pieza& b) { return a.peso < b.peso; });
                      for (const Pieza& p : piezas) {
                          std::cout << p.nombre << " " << p.peso << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <algorithm>
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  struct Pieza {
                      std::string nombre;
                      int peso;
                  };

                  int main()
                  {
                      std::vector<Pieza> piezas = {{"tuerca", 2}, {"yunque", 90}, {"engranaje", 15}, {"resorte", 1}};
                      std::sort(piezas.begin(), piezas.end(), [](const Pieza& a, const Pieza& b) { return a.peso > b.peso; });
                      for (const Pieza& p : piezas) {
                          std::cout << p.nombre << " " << p.peso << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="El yunque primero, el resorte al final. Bron esconde detrás de la espalda la función con nombre que había escrito para esto.",
              imagen=["Una máquina clasificadora enorme con una ranura para tarjetas.",
                      BRON + " mete una tarjeta.", LIMA + " lo vigila con la lima en alto."]),
            m(id="R03-N05-P2", titulo="Las más pesadas que el límite",
              lugar=CLASIFICADOR, personajes="Bron, Tesla",
              carta="Captura | [limite](int p) { return p > limite; } copia limite adentro · [&] usa las de afuera por referencia · std::count_if cuenta las que cumplen",
              recompensa="xp 10, oro 10",
              escena="""
                  Tesla quiere saber cuántas piezas pasan el límite de la balanza, que se lee de la entrada. La lambda de Bron no puede usar `limite`: no lo capturó.
              """,
              sugiere="Para usar `limite` adentro de la lambda, ponelo entre los corchetes: `[limite]`.",
              desafio="Capturá el límite.",
              entrada="10\n",
              inicial='''
                  #include <algorithm>
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      int limite = 0;
                      std::cin >> limite;
                      std::vector<int> pesos = {2, 90, 15, 1, 12, 7};
                      auto pesadas = std::count_if(pesos.begin(), pesos.end(), [](int p) { return p > limite; });
                      std::cout << "Pasan de " << limite << ": " << pesadas << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <algorithm>
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      int limite = 0;
                      std::cin >> limite;
                      std::vector<int> pesos = {2, 90, 15, 1, 12, 7};
                      auto pesadas = std::count_if(pesos.begin(), pesos.end(), [limite](int p) { return p > limite; });
                      std::cout << "Pasan de " << limite << ": " << pesadas << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres piezas pasan de 10. Tesla pone el límite en 50 para probar, y queda solo el yunque.",
              imagen=["Una balanza de bronce con un yunque encima y una aguja en rojo.",
                      TESLA + " gira la perilla del límite.", BRON + " anota."]),
            m(id="R03-N05-P3", titulo="Fuera los defectuosos",
              lugar=CLASIFICADOR, personajes="Lima, Bron",
              carta="std::erase_if(v, lambda) | borra del vector todos los que cumplen la condición (C++20) · devuelve cuántos borró",
              recompensa="xp 15, oro 15",
              escena="""
                  Los engranajes con menos de 10 dientes están defectuosos. Lima quiere sacarlos todos de la caja de una vez, y Bron los está sacando de a uno, con un bucle que se saltea algunos.
              """,
              sugiere="`std::erase_if(dientes, [](int d) { return d < 10; });` borra todos los que cumplen la condición, sin saltear ninguno.",
              desafio="Borrá los defectuosos con `erase_if`.",
              inicial='''
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> dientes = {12, 8, 5, 40, 9, 24};
                      for (std::size_t i = 0; i < dientes.size(); i++) {
                          if (dientes[i] < 10) {
                              dientes.erase(dientes.begin() + i);
                          }
                      }
                      std::cout << "Quedan:";
                      for (int d : dientes) {
                          std::cout << " " << d;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> dientes = {12, 8, 5, 40, 9, 24};
                      auto borrados = std::erase_if(dientes, [](int d) { return d < 10; });
                      std::cout << "Borrados: " << borrados << "\\n";
                      std::cout << "Quedan:";
                      for (int d : dientes) {
                          std::cout << " " << d;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres afuera, tres adentro. El bucle de Bron se había salteado el 5, que estaba justo después del 8.",
              imagen=["Una caja de engranajes y, al lado, tres engranajes chiquitos descartados.",
                      LIMA + " tira los defectuosos a un balde.", BRON + " mira el balde."]),
        ],
    },
    {
        "titulo": "R03-N06 · Archivos y carpetas",
        "misiones": [
            m(id="R03-N06-P1", titulo="La bitácora que se cierra sola",
              lugar=ARCHIVO, personajes="Bron, Lima",
              carta="Cerrar al salir del bloque | un ofstream escribe en un buffer · al destruirse (fin de su bloque) se cierra y graba · leer antes de cerrar puede no encontrar nada",
              recompensa="xp 15, oro 15",
              escena="""
                  Bron escribe el inventario en un archivo y, enseguida, lo lee para controlarlo. El archivo aparece vacío. Lima le explica: lo escrito todavía está en el buffer del `ofstream`, que recién lo graba al cerrarse.
              """,
              sugiere="Poné la escritura en su propio bloque `{ ... }`: al terminar el bloque, el `ofstream` se destruye y se cierra (RAII), y después se puede leer.",
              desafio="Cerrá el archivo antes de leerlo, con un bloque.",
              inicial='''
                  #include <fstream>
                  #include <iostream>
                  #include <string>

                  int main()
                  {
                      std::ofstream out("inventario.txt");
                      out << "llave cian\\n";
                      out << "engranaje de laton\\n";
                      out << "pedido de bisagras\\n";

                      std::ifstream in("inventario.txt");
                      std::string linea;
                      int n = 0;
                      while (std::getline(in, linea)) {
                          std::cout << ++n << ". " << linea << "\\n";
                      }
                      std::cout << "Lineas: " << n << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <fstream>
                  #include <iostream>
                  #include <string>

                  int main()
                  {
                      {
                          std::ofstream out("inventario.txt");
                          out << "llave cian\\n";
                          out << "engranaje de laton\\n";
                          out << "pedido de bisagras\\n";
                      }

                      std::ifstream in("inventario.txt");
                      std::string linea;
                      int n = 0;
                      while (std::getline(in, linea)) {
                          std::cout << ++n << ". " << linea << "\\n";
                      }
                      std::cout << "Lineas: " << n << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres líneas, y la tercera es el pedido de bisagras. Bron no lo perdió esta vez.",
              imagen=["Un libro de registros abierto con tres renglones escritos y una pluma.",
                      BRON + " cierra el libro.", LIMA + " lee por encima."]),
            m(id="R03-N06-P2", titulo="Sumar, no pisar",
              lugar=ARCHIVO, personajes="Bron, Oto",
              carta="Agregar al final | std::ofstream f(ruta, std::ios::app) agrega · sin app, abrir para escribir BORRA lo que había",
              recompensa="xp 10, oro 10",
              escena="""
                  Oto anota en el archivo del comedor cada guiso que sirve. Bron abre el archivo cada vez para escribir, y el archivo siempre tiene un solo guiso: el último.
              """,
              sugiere="Abrí el archivo en modo agregar: `std::ofstream f(\"guisos.txt\", std::ios::app);`.",
              desafio="Hacé que cada guiso se sume al archivo.",
              inicial='''
                  #include <fstream>
                  #include <iostream>
                  #include <string>

                  void anotar(const std::string& guiso)
                  {
                      std::ofstream f("guisos.txt");
                      f << guiso << "\\n";
                  }

                  int main()
                  {
                      anotar("guiso de lunes");
                      anotar("guiso de martes");
                      anotar("guiso violeta");
                      std::ifstream in("guisos.txt");
                      std::string linea;
                      while (std::getline(in, linea)) {
                          std::cout << linea << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <fstream>
                  #include <iostream>
                  #include <string>

                  void anotar(const std::string& guiso)
                  {
                      std::ofstream f("guisos.txt", std::ios::app);
                      f << guiso << "\\n";
                  }

                  int main()
                  {
                      anotar("guiso de lunes");
                      anotar("guiso de martes");
                      anotar("guiso violeta");
                      std::ifstream in("guisos.txt");
                      std::string linea;
                      while (std::getline(in, linea)) {
                          std::cout << linea << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Los tres guisos de la semana, en orden. El violeta queda anotado para la historia.",
              imagen=["Un cuaderno de cocina con tres guisos anotados, el último en tinta violeta.",
                      OTO + " lee el cuaderno con orgullo.", BRON + " sostiene la pluma."]),
            m(id="R03-N06-P3", titulo="La columna del CSV",
              lugar=ARCHIVO, personajes="Bron, Lima",
              carta="CSV | std::getline(ss, campo, ',') corta por comas · la primera línea suele ser el encabezado · std::stoi para los números",
              recompensa="xp 15, oro 15",
              escena="""
                  El Archivo guarda el stock en un CSV: `pieza,cantidad`. Lima quiere el total de piezas. Bron suma también el encabezado, y el programa revienta al convertir «cantidad» en número.
              """,
              sugiere="Leé la primera línea (el encabezado) con un `getline` antes del bucle, y no la sumes.",
              desafio="Salteá el encabezado.",
              entrada="pieza,cantidad\nengranaje,40\nresorte,25\ntuerca,120\n",
              inicial='''
                  #include <iostream>
                  #include <sstream>
                  #include <string>

                  int main()
                  {
                      std::string linea;
                      int total = 0;
                      while (std::getline(std::cin, linea)) {
                          std::istringstream ss(linea);
                          std::string pieza, cantidad;
                          std::getline(ss, pieza, ',');
                          std::getline(ss, cantidad);
                          total += std::stoi(cantidad);
                      }
                      std::cout << "Total de piezas: " << total << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <sstream>
                  #include <string>

                  int main()
                  {
                      std::string linea;
                      std::getline(std::cin, linea);
                      int total = 0;
                      while (std::getline(std::cin, linea)) {
                          std::istringstream ss(linea);
                          std::string pieza, cantidad;
                          std::getline(ss, pieza, ',');
                          std::getline(ss, cantidad);
                          total += std::stoi(cantidad);
                      }
                      std::cout << "Total de piezas: " << total << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Ciento ochenta y cinco piezas. Lima lo anota y le recuerda a Bron que la primera línea casi nunca es un dato.",
              imagen=["Una planilla en la pared con tres columnas y un encabezado subrayado.",
                      LIMA + " subraya el encabezado.", BRON + " suma con un ábaco."]),
        ],
    },
    {
        "titulo": "R03-N07 · Punteros inteligentes",
        "misiones": [
            m(id="R03-N07-P1", titulo="Un solo dueño",
              lugar=DEPOSITO, personajes="Bron, Oto",
              carta="unique_ptr | un solo dueño · no se copia: se ENTREGA con std::move · el que entregó queda vacío (nullptr)",
              recompensa="xp 10, oro 10",
              escena="""
                  La batidora (el autómata que Bron armó con `new`) por fin tiene etiqueta de dueño. Bron se la quiere dar a Oto, y escribe una copia: el Taller no lo deja. Una máquina con un solo dueño se **entrega**.
              """,
              sugiere="`std::unique_ptr` no se copia. Para pasárselo a Oto: `std::move(de_bron)`. Después, `de_bron` queda vacío.",
              desafio="Entregale la batidora a Oto.",
              inicial='''
                  #include <iostream>
                  #include <memory>
                  #include <string>

                  struct Automata {
                      std::string nombre;
                  };

                  int main()
                  {
                      std::unique_ptr<Automata> de_bron = std::make_unique<Automata>(Automata{"Batidora"});
                      std::unique_ptr<Automata> de_oto = de_bron;
                      std::cout << "Oto tiene: " << de_oto->nombre << "\\n";
                      std::cout << "Bron tiene: " << (de_bron ? de_bron->nombre : "nada") << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <memory>
                  #include <string>
                  #include <utility>

                  struct Automata {
                      std::string nombre;
                  };

                  int main()
                  {
                      std::unique_ptr<Automata> de_bron = std::make_unique<Automata>(Automata{"Batidora"});
                      std::unique_ptr<Automata> de_oto = std::move(de_bron);
                      std::cout << "Oto tiene: " << de_oto->nombre << "\\n";
                      std::cout << "Bron tiene: " << (de_bron ? de_bron->nombre : "nada") << "\\n";
                      return 0;
                  }
              ''',
              al_superar="La batidora es de Oto, con etiqueta y todo. Por primera vez, se apaga sola cuando Oto cierra la cocina.",
              imagen=["Un autómata batidora con una etiqueta colgada que dice «Oto».",
                      BRON + " le entrega el autómata.", OTO + " lo recibe con el cucharón en la otra mano."]),
            m(id="R03-N07-P2", titulo="Dos dueños para el guiso",
              lugar="El comedor de los artífices", personajes="Oto, Bron",
              carta="shared_ptr | varios dueños comparten el objeto · use_count() dice cuántos · se destruye cuando se va el ÚLTIMO",
              recompensa="xp 15, oro 15",
              escena="""
                  El guiso grande es de Oto **y** de Bron: los dos lo cuidan. Bron quiere saber cuántos dueños tiene en cada momento, pero cuenta mal: imprime un número fijo.
              """,
              sugiere="`guiso.use_count()` dice cuántos `shared_ptr` comparten el objeto. Mostralo en lugar del número fijo.",
              desafio="Mostrá la cuenta real de dueños.",
              inicial='''
                  #include <iostream>
                  #include <memory>
                  #include <string>

                  int main()
                  {
                      auto de_oto = std::make_shared<std::string>("guiso grande");
                      std::cout << "Duenos: " << 1 << "\\n";
                      {
                          auto de_bron = de_oto;
                          std::cout << "Duenos: " << 1 << "\\n";
                      }
                      std::cout << "Duenos: " << 1 << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <memory>
                  #include <string>

                  int main()
                  {
                      auto de_oto = std::make_shared<std::string>("guiso grande");
                      std::cout << "Duenos: " << de_oto.use_count() << "\\n";
                      {
                          auto de_bron = de_oto;
                          std::cout << "Duenos: " << de_oto.use_count() << "\\n";
                      }
                      std::cout << "Duenos: " << de_oto.use_count() << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Uno, dos, uno. Cuando Bron se va, el guiso sigue: todavía tiene a Oto.",
              imagen=["Una olla grande con dos cucharones adentro.",
                      OTO + " y " + BRON + " sostienen cada uno un cucharón."]),
            m(id="R03-N07-P3", titulo="Mirar sin ser dueño",
              lugar=DEPOSITO, personajes="Lima, Bron",
              carta="weak_ptr | mira un objeto de un shared_ptr sin ser dueño · w.lock() devuelve un shared_ptr, o vacío si el objeto ya no existe",
              recompensa="xp 15, oro 15",
              escena="""
                  Lima lleva una lista de los autómatas del depósito, pero no es dueña de ninguno. Cuando uno vuelve a la fundición, su lista tiene que darse cuenta. La de Bron sigue diciendo que el autómata está.
              """,
              sugiere="Antes de usarlo, pedile al `weak_ptr` el objeto con `lock()`: si devuelve vacío, el autómata ya no existe.",
              desafio="Preguntá con `lock()` si el autómata sigue existiendo.",
              inicial='''
                  #include <iostream>
                  #include <memory>
                  #include <string>

                  int main()
                  {
                      auto dueno = std::make_shared<std::string>("Cucu");
                      std::weak_ptr<std::string> lista = dueno;
                      for (int dia = 1; dia <= 2; dia++) {
                          std::cout << "Dia " << dia << ": " << "sigue en el deposito" << "\\n";
                          dueno.reset();
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <memory>
                  #include <string>

                  int main()
                  {
                      auto dueno = std::make_shared<std::string>("Cucu");
                      std::weak_ptr<std::string> lista = dueno;
                      for (int dia = 1; dia <= 2; dia++) {
                          if (auto a = lista.lock()) {
                              std::cout << "Dia " << dia << ": " << *a << " sigue en el deposito\\n";
                          } else {
                              std::cout << "Dia " << dia << ": volvio a la fundicion\\n";
                          }
                          dueno.reset();
                      }
                      return 0;
                  }
              ''',
              al_superar="El segundo día, Cucú ya volvió a la fundición, y la lista de Lima lo sabe. Lima lo tacha con cariño.",
              imagen=["Una lista colgada en el depósito con un nombre tachado.",
                      LIMA + " tacha el nombre con cuidado.", BRON + " empuja un autómata hacia la fundición."]),
        ],
    },
    {
        "titulo": "R03-N08 · RAII, copias y movimientos",
        "misiones": [
            m(id="R03-N08-P1", titulo="La puerta que se destraba sola",
              lugar=SALA, personajes="Bron, la Maestra Artífice",
              carta="RAII | lo que se toma en el constructor se suelta en el destructor · así se suelta SIEMPRE, también en un return temprano",
              recompensa="xp 15, oro 15",
              escena="""
                  La puerta de la sala de máquinas se traba al entrar y hay que destrabarla al salir. La función de Bron se olvida de destrabarla cuando sale antes, por la caldera rota.
                  En la puerta aparece una mujer alta de pelo blanco y antiparras verdes, con una tableta llena de tildes: **la Maestra Artífice**. —¿Y la prueba? —pregunta. Bron no tiene la prueba.
              """,
              sugiere="Usá la clase `Traba`: en su constructor traba y en su destructor destraba. Creá una al principio de `revisar` y sacá los `destrabar` a mano: el destructor corre en cualquier salida.",
              desafio="Reemplazá el trabado a mano por un objeto `Traba`.",
              inicial='''
                  #include <iostream>

                  void trabar() { std::cout << "puerta trabada\\n"; }
                  void destrabar() { std::cout << "puerta destrabada\\n"; }

                  class Traba {
                  public:
                      Traba() { trabar(); }
                      ~Traba() { destrabar(); }
                  };

                  void revisar(bool caldera_rota)
                  {
                      trabar();
                      if (caldera_rota) {
                          std::cout << "caldera rota: salgo corriendo\\n";
                          return;
                      }
                      std::cout << "todo en orden\\n";
                      destrabar();
                  }

                  int main()
                  {
                      revisar(false);
                      revisar(true);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  void trabar() { std::cout << "puerta trabada\\n"; }
                  void destrabar() { std::cout << "puerta destrabada\\n"; }

                  class Traba {
                  public:
                      Traba() { trabar(); }
                      ~Traba() { destrabar(); }
                  };

                  void revisar(bool caldera_rota)
                  {
                      Traba traba;
                      if (caldera_rota) {
                          std::cout << "caldera rota: salgo corriendo\\n";
                          return;
                      }
                      std::cout << "todo en orden\\n";
                  }

                  int main()
                  {
                      revisar(false);
                      revisar(true);
                      return 0;
                  }
              ''',
              al_superar="La puerta se destraba sola, también cuando Bron sale corriendo. La Maestra Artífice tilda algo en su tableta, sin mirarlo.",
              imagen=["La puerta de hierro de la sala de máquinas, con un cerrojo que se abre solo.",
                      MAESTRA + " tilda algo en su tableta.", BRON + " sale corriendo, con hollín en la cara."]),
            m(id="R03-N08-P2", titulo="La llave maestra se entrega",
              lugar=SALA, personajes="Bron, Tesla",
              carta="= delete | LlaveMaestra(const LlaveMaestra&) = delete; prohíbe copiarla · se puede MOVER: LlaveMaestra b = std::move(a);",
              recompensa="xp 15, oro 15",
              escena="""
                  La llave maestra de la sala de máquinas no se puede copiar: Tesla le borró la copia al plano. Bron intenta hacerse una copia «por las dudas». El Taller no lo deja: una llave maestra se **entrega**.
              """,
              sugiere="En lugar de copiarla, movela: `LlaveMaestra de_bron = std::move(de_tesla);`.",
              desafio="Entregá la llave en lugar de copiarla.",
              inicial='''
                  #include <iostream>
                  #include <string>
                  #include <utility>

                  class LlaveMaestra {
                  public:
                      explicit LlaveMaestra(std::string sala) : sala_(sala) {}
                      LlaveMaestra(const LlaveMaestra&) = delete;
                      LlaveMaestra(LlaveMaestra&& otra) noexcept : sala_(std::move(otra.sala_)) { otra.sala_ = ""; }
                      bool abre() const { return !sala_.empty(); }

                  private:
                      std::string sala_;
                  };

                  int main()
                  {
                      LlaveMaestra de_tesla("sala de maquinas");
                      LlaveMaestra de_bron = de_tesla;
                      std::cout << "La de Tesla abre: " << (de_tesla.abre() ? "si" : "no") << "\\n";
                      std::cout << "La de Bron abre: " << (de_bron.abre() ? "si" : "no") << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>
                  #include <utility>

                  class LlaveMaestra {
                  public:
                      explicit LlaveMaestra(std::string sala) : sala_(sala) {}
                      LlaveMaestra(const LlaveMaestra&) = delete;
                      LlaveMaestra(LlaveMaestra&& otra) noexcept : sala_(std::move(otra.sala_)) { otra.sala_ = ""; }
                      bool abre() const { return !sala_.empty(); }

                  private:
                      std::string sala_;
                  };

                  int main()
                  {
                      LlaveMaestra de_tesla("sala de maquinas");
                      LlaveMaestra de_bron = std::move(de_tesla);
                      std::cout << "La de Tesla abre: " << (de_tesla.abre() ? "si" : "no") << "\\n";
                      std::cout << "La de Bron abre: " << (de_bron.abre() ? "si" : "no") << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Una sola llave, ahora en el bolsillo de Bron. Tesla se queda con las manos vacías y una sonrisa.",
              imagen=["Una llave maestra de bronce pasando de una mano a otra.",
                      TESLA + " la entrega.", BRON + " la recibe con las dos manos."]),
            m(id="R03-N08-P3", titulo="Mover en vez de copiar",
              lugar=SALA, personajes="Oto, Lima",
              carta="Mover | std::move(x) avisa que x ya no se usa · el vector «se lleva» los datos sin copiarlos · x queda válido pero vacío",
              recompensa="xp 10, oro 10",
              escena="""
                  Oto guarda su receta larguísima en el libro del comedor, y el libro hace una copia entera, letra por letra. Lima mide el tiempo con la lupa y se impacienta: la receta original ya no se va a usar.
              """,
              sugiere="Pasale la receta al vector con `std::move(receta)`: el vector se lleva las letras sin copiarlas, y `receta` queda vacía.",
              desafio="Mové la receta al libro.",
              inicial='''
                  #include <iostream>
                  #include <string>
                  #include <utility>
                  #include <vector>

                  int main()
                  {
                      std::string receta = "guiso: cebolla, zanahoria, papa, carne y una pizca de violeta";
                      std::vector<std::string> libro;
                      libro.push_back(receta);
                      std::cout << "En el libro: " << libro[0].size() << " letras\\n";
                      std::cout << "En la mano de Oto: " << receta.size() << " letras\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>
                  #include <utility>
                  #include <vector>

                  int main()
                  {
                      std::string receta = "guiso: cebolla, zanahoria, papa, carne y una pizca de violeta";
                      std::vector<std::string> libro;
                      libro.push_back(std::move(receta));
                      std::cout << "En el libro: " << libro[0].size() << " letras\\n";
                      std::cout << "En la mano de Oto: " << receta.size() << " letras\\n";
                      return 0;
                  }
              ''',
              al_superar="La receta está en el libro, y la hoja de Oto quedó en blanco. Oto la usa para anotar la próxima.",
              imagen=["Un libro de recetas abierto y una hoja en blanco al lado.",
                      OTO + " mira la hoja en blanco, sorprendido.", LIMA + " guarda la lupa."]),
        ],
    },
    {
        "titulo": "R03-N09 · Jefe: el Mímico del Bestiario",
        "misiones": [
            m(id="R03-N09-P1", titulo="Ordenar el Bestiario",
              lugar=BESTIARIO, personajes="Bron, Lima, Tesla",
              criatura="dragon",
              carta="map + optional | std::map<std::string, int> ordena por nombre · una búsqueda que puede fallar devuelve std::optional",
              recompensa="xp 15, oro 15",
              escena="""
                  Anoche alguien revolvió el **Bestiario**: hay fichas rotas, criaturas repetidas y una nueva, el **Mímico**, que copia a quien mira. —Para atraparlo, primero ordená el Bestiario —dice Tesla.
                  Bron guarda cada ficha en un `map` (nombre → peligro), pero las repetidas pisan a las anteriores y se pierde el peligro mayor.
              """,
              sugiere="Si la criatura ya está, quedate con el peligro **mayor**: `fichas[n] = std::max(fichas[n], peligro);` (si no estaba, arranca en 0).",
              desafio="Guardá el peligro mayor de cada criatura.",
              entrada="lobo 7\nslime 2\nlobo 3\ntroll 5\nslime 1\n",
              inicial='''
                  #include <algorithm>
                  #include <iostream>
                  #include <map>
                  #include <string>

                  int main()
                  {
                      std::map<std::string, int> fichas;
                      std::string nombre;
                      int peligro = 0;
                      while (std::cin >> nombre >> peligro) {
                          fichas[nombre] = peligro;
                      }
                      for (const auto& [n, p] : fichas) {
                          std::cout << n << ": peligro " << p << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <algorithm>
                  #include <iostream>
                  #include <map>
                  #include <string>

                  int main()
                  {
                      std::map<std::string, int> fichas;
                      std::string nombre;
                      int peligro = 0;
                      while (std::cin >> nombre >> peligro) {
                          fichas[nombre] = std::max(fichas[nombre], peligro);
                      }
                      for (const auto& [n, p] : fichas) {
                          std::cout << n << ": peligro " << p << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Lobo 7, slime 2, troll 5, en orden. El Bestiario queda prolijo, y en un rincón algo gris se esconde detrás de un estante.",
              imagen=["Un libro enorme de bestiario abierto sobre un atril, con fichas desparramadas alrededor.",
                      LIMA + " ordena fichas.", "Detrás de un estante asoma " + MIMICO + "."]),
            m(id="R03-N09-P2", titulo="La copia que es suya",
              lugar=BESTIARIO, personajes="Bron, Tesla",
              criatura="dragon",
              carta="clone() | virtual std::unique_ptr<Criatura> clone() const · copia polimórfica: cada clase devuelve una copia de SÍ MISMA",
              recompensa="xp 15, oro 15",
              escena="""
                  El Mímico copia a quien mira. Tesla le explica a Bron cómo lo hace: no **es** un lobo, **tiene** una copia de un lobo, y esa copia es suya. Para copiar algo sin saber qué es, cada criatura sabe copiarse a sí misma. Al troll le falta su `clone`.
              """,
              sugiere="Escribí `clone()` en `Troll` como en `Lobo`: `return std::make_unique<Troll>(*this);`.",
              desafio="Completá la copia del troll.",
              inicial='''
                  #include <iostream>
                  #include <memory>
                  #include <string>

                  class Criatura {
                  public:
                      virtual ~Criatura() = default;
                      virtual std::string sonido() const = 0;
                      virtual std::unique_ptr<Criatura> clone() const { return nullptr; }
                  };

                  class Lobo : public Criatura {
                  public:
                      std::string sonido() const override { return "auuu"; }
                      std::unique_ptr<Criatura> clone() const override { return std::make_unique<Lobo>(*this); }
                  };

                  class Troll : public Criatura {
                  public:
                      std::string sonido() const override { return "grrr"; }
                  };

                  int main()
                  {
                      Lobo lobo;
                      Troll troll;
                      for (const Criatura* original : {static_cast<const Criatura*>(&lobo), static_cast<const Criatura*>(&troll)}) {
                          std::unique_ptr<Criatura> copia = original->clone();
                          std::cout << "El Mimico hace: " << (copia ? copia->sonido() : "...nada") << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <memory>
                  #include <string>

                  class Criatura {
                  public:
                      virtual ~Criatura() = default;
                      virtual std::string sonido() const = 0;
                      virtual std::unique_ptr<Criatura> clone() const { return nullptr; }
                  };

                  class Lobo : public Criatura {
                  public:
                      std::string sonido() const override { return "auuu"; }
                      std::unique_ptr<Criatura> clone() const override { return std::make_unique<Lobo>(*this); }
                  };

                  class Troll : public Criatura {
                  public:
                      std::string sonido() const override { return "grrr"; }
                      std::unique_ptr<Criatura> clone() const override { return std::make_unique<Troll>(*this); }
                  };

                  int main()
                  {
                      Lobo lobo;
                      Troll troll;
                      for (const Criatura* original : {static_cast<const Criatura*>(&lobo), static_cast<const Criatura*>(&troll)}) {
                          std::unique_ptr<Criatura> copia = original->clone();
                          std::cout << "El Mimico hace: " << (copia ? copia->sonido() : "...nada") << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="«Auuu», «grrr». El Mímico copia al troll a la perfección, salvo por un ojo en la rodilla.",
              imagen=[MIMICO + " tomando la forma de un troll, con un ojo en la rodilla.",
                      BRON + " retrocede.", TESLA + " lo observa con el visor bajado."]),
            m(id="R03-N09-P3", titulo="La bisagra del Mímico",
              lugar=BESTIARIO, personajes="Bron, Lima",
              criatura="dragon",
              carta="Lambda + algoritmo | std::find_if(v.begin(), v.end(), [](const Objeto& o) { return ...; }) devuelve un iterador, o end() si no hay",
              recompensa="xp 15, oro 15",
              escena="""
                  El Mímico copió a Bron (con dos llaves) y a Lima (con tres rodetes). Y tiene en la mano una **bisagra**: copió la del Vidriero, pero no sabe abrir nada con ella. Para encontrarla entre todo lo que robó, Bron recorre la bolsa a mano y se pierde.
              """,
              sugiere="Buscá con `std::find_if` y una lambda que pregunte si el objeto es una `\"bisagra\"`. Si el iterador no es `end()`, la encontraste.",
              desafio="Encontrá la bisagra con `find_if`.",
              inicial='''
                  #include <algorithm>
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  struct Objeto {
                      std::string tipo;
                      std::string de_quien;
                  };

                  int main()
                  {
                      std::vector<Objeto> bolsa = {{"llave", "Bron"}, {"lima", "Lima"}, {"bisagra", "Vidriero"}, {"cucharon", "Oto"}};
                      auto it = bolsa.end();
                      if (it != bolsa.end()) {
                          std::cout << "La bisagra era del " << it->de_quien << "\\n";
                      } else {
                          std::cout << "No hay bisagra\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <algorithm>
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  struct Objeto {
                      std::string tipo;
                      std::string de_quien;
                  };

                  int main()
                  {
                      std::vector<Objeto> bolsa = {{"llave", "Bron"}, {"lima", "Lima"}, {"bisagra", "Vidriero"}, {"cucharon", "Oto"}};
                      auto it = std::find_if(bolsa.begin(), bolsa.end(), [](const Objeto& o) { return o.tipo == "bisagra"; });
                      if (it != bolsa.end()) {
                          std::cout << "La bisagra era del " << it->de_quien << "\\n";
                      } else {
                          std::cout << "No hay bisagra\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="La bisagra era del Vidriero, y el Mímico no sabe qué abre. Bron tampoco. Lima la dibuja en su cuaderno.",
              imagen=["Una bolsa de tela abierta con una llave, una lima, un cucharón y una bisagra rara.",
                      BRON + " levanta la bisagra.", LIMA + " la dibuja en su cuaderno."]),
            m(id="R03-N09-P4", titulo="El espejo del Mímico",
              lugar=BESTIARIO, personajes="Bron, Tesla, Lima",
              criatura="dragon",
              carta="Varios dueños, uno solo | map<string, unique_ptr<Criatura>> · el mapa es el dueño · mover una criatura al mapa con std::move",
              recompensa="xp 25, oro 30",
              item="Espejo del Mímico",
              escena="""
                  Para atrapar al Mímico, hay que guardar cada criatura del Bestiario en su lugar, con **un solo dueño**: el mapa. El Mímico se escapa por cada copia que queda suelta. Bron crea las criaturas pero no las mete en el mapa.
              """,
              sugiere="Movelas al mapa: `bestiario[nombre] = std::move(c);`. Al final, el Mímico no tiene ninguna copia suelta para esconderse.",
              desafio="Guardá cada criatura en el Bestiario, entregándola.",
              inicial='''
                  #include <iostream>
                  #include <map>
                  #include <memory>
                  #include <string>
                  #include <utility>

                  struct Criatura {
                      std::string sonido;
                  };

                  int main()
                  {
                      std::map<std::string, std::unique_ptr<Criatura>> bestiario;
                      int sueltas = 0;
                      for (auto [nombre, sonido] : {std::pair<std::string, std::string>{"lobo", "auuu"}, {"troll", "grrr"}, {"slime", "blub"}}) {
                          auto c = std::make_unique<Criatura>(Criatura{sonido});
                          if (c) {
                              sueltas++;
                          }
                      }
                      std::cout << "En el Bestiario: " << bestiario.size() << "\\n";
                      for (const auto& [nombre, c] : bestiario) {
                          std::cout << nombre << ": " << c->sonido << "\\n";
                      }
                      std::cout << "Copias sueltas para el Mimico: " << sueltas - static_cast<int>(bestiario.size()) << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <map>
                  #include <memory>
                  #include <string>
                  #include <utility>

                  struct Criatura {
                      std::string sonido;
                  };

                  int main()
                  {
                      std::map<std::string, std::unique_ptr<Criatura>> bestiario;
                      int sueltas = 0;
                      for (auto [nombre, sonido] : {std::pair<std::string, std::string>{"lobo", "auuu"}, {"troll", "grrr"}, {"slime", "blub"}}) {
                          auto c = std::make_unique<Criatura>(Criatura{sonido});
                          if (c) {
                              sueltas++;
                          }
                          bestiario[nombre] = std::move(c);
                      }
                      std::cout << "En el Bestiario: " << bestiario.size() << "\\n";
                      for (const auto& [nombre, c] : bestiario) {
                          std::cout << nombre << ": " << c->sonido << "\\n";
                      }
                      std::cout << "Copias sueltas para el Mimico: " << sueltas - static_cast<int>(bestiario.size()) << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Cero copias sueltas. El Mímico no tiene a quién imitar, se derrite como una vela, y deja en el piso **el Espejo del Mímico**: refleja lo que tenés, no lo que sos.",
              imagen=["Un charco de cera gris en el piso del Bestiario, con un espejo ovalado encima.",
                      BRON + " levanta el espejo.", TESLA + " y " + LIMA + " miran el reflejo, que es un poco distinto."]),
        ],
    },
]
