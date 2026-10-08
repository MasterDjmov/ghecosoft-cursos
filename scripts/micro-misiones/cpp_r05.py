from gencpp import m
from cpp_r01 import BRON, TESLA, LIMA, LYN, OTO, GHECO
from cpp_r03 import MAESTRA

TALLER = "El Taller del Juego"
ANDAMIO = "Los andamios del Taller del Juego"
BANCO = "El Banco de Pruebas de la Maestra Artífice"
MESA = "La mesa del juego desarmado"
PENDULO = "El Gran Péndulo del Taller"
LABERINTO = "El Laberinto bajo el Taller"
MINOTAURO = "el Minotauro del Laberinto (toro gigante de hierro y bronce que camina en dos patas, cuernos de acero, ojos de brasa y un engranaje enorme colgado del cuello)"

NODOS = [
    {
        "titulo": "R05-N01 · Excepciones",
        "misiones": [
            m(id="R05-N01-P1", titulo="Tocar la alarma",
              lugar=TALLER, personajes="Bron, Tesla",
              carta="throw y catch | throw std::invalid_argument(\"...\") avisa · try { ... } catch (const std::exception& e) { e.what() } atrapa · sin catch, el programa termina",
              recompensa="xp 10, oro 10",
              escena="""
                  En el Taller del Juego se construyen máquinas que no pueden fallar en silencio. La que reparte engranajes entre los ayudantes **toca la alarma** si le piden repartir entre cero. Nadie la escucha, y el programa se corta de golpe.
              """,
              sugiere="Envolvé los repartos en un `try` y atrapá con `catch (const std::exception& e)`, mostrando `Alarma: ` y `e.what()`.",
              desafio="Atrapá la alarma para que el Taller siga andando.",
              inicial='''
                  #include <iostream>
                  #include <stdexcept>

                  int repartir(int engranajes, int ayudantes)
                  {
                      if (ayudantes == 0) {
                          throw std::invalid_argument("no hay ayudantes");
                      }
                      return engranajes / ayudantes;
                  }

                  int main()
                  {
                      std::cout << "A cada uno: " << repartir(20, 4) << "\\n";
                      std::cout << "A cada uno: " << repartir(20, 0) << "\\n";
                      std::cout << "El Taller sigue andando\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <stdexcept>

                  int repartir(int engranajes, int ayudantes)
                  {
                      if (ayudantes == 0) {
                          throw std::invalid_argument("no hay ayudantes");
                      }
                      return engranajes / ayudantes;
                  }

                  int main()
                  {
                      try {
                          std::cout << "A cada uno: " << repartir(20, 4) << "\\n";
                          std::cout << "A cada uno: " << repartir(20, 0) << "\\n";
                      } catch (const std::exception& e) {
                          std::cout << "Alarma: " << e.what() << "\\n";
                      }
                      std::cout << "El Taller sigue andando\\n";
                      return 0;
                  }
              ''',
              al_superar="La alarma suena, alguien la atrapa, y el Taller sigue andando. Tesla asiente: el que sabía qué hacer estaba más arriba.",
              imagen=["Una máquina repartidora de engranajes con una sirena encendida.",
                      TESLA + " atrapa la sirena con una mano.", BRON + " mira el contador en cero."]),
            m(id="R05-N01-P2", titulo="Primero lo más específico",
              lugar=TALLER, personajes="Bron, Lima",
              carta="Orden de los catch | se prueban de arriba hacia abajo · el de la base (std::exception) atrapa TODO · los específicos van primero",
              recompensa="xp 10, oro 10",
              escena="""
                  Cuando alguien pide una pieza que no existe, la máquina tiene que decir «no existe esa pieza»; para el resto de los errores, «falla general». Bron puso el `catch` general arriba, y todo le dice «falla general». El compilador ya le avisa.
              """,
              sugiere="Poné el `catch (const std::out_of_range&)` **antes** que el de `std::exception`.",
              desafio="Ordená los `catch`.",
              inicial='''
                  #include <iostream>
                  #include <stdexcept>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> piezas = {10, 20, 30};
                      for (int pedido : {1, 7}) {
                          try {
                              std::cout << "Pieza " << pedido << ": " << piezas.at(pedido) << "\\n";
                          } catch (const std::exception& e) {
                              std::cout << "Pieza " << pedido << ": falla general\\n";
                          } catch (const std::out_of_range& e) {
                              std::cout << "Pieza " << pedido << ": no existe esa pieza\\n";
                          }
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <stdexcept>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> piezas = {10, 20, 30};
                      for (int pedido : {1, 7}) {
                          try {
                              std::cout << "Pieza " << pedido << ": " << piezas.at(pedido) << "\\n";
                          } catch (const std::out_of_range&) {
                              std::cout << "Pieza " << pedido << ": no existe esa pieza\\n";
                          } catch (const std::exception&) {
                              std::cout << "Pieza " << pedido << ": falla general\\n";
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="«No existe esa pieza», con todas las letras. Lima lo anota: de lo más fino a lo más grueso, como las limas.",
              imagen=["Una pared con dos redes colgadas, una de malla fina arriba y una gruesa abajo.",
                      LIMA + " acomoda la red fina arriba.", BRON + " sostiene la gruesa."]),
            m(id="R05-N01-P3", titulo="La red del andamio",
              lugar=ANDAMIO, personajes="Bron, Tesla",
              carta="Excepción propia | class FallaDeAndamio : public std::runtime_error { using runtime_error::runtime_error; }; · se atrapa por su tipo",
              recompensa="xp 15, oro 15",
              item="Amuleto del Catch",
              escena="""
                  Bron se sube a un andamio para ver mejor; el andamio se rompe, y Bron cae… y lo ataja una **red**. El que la tendió sabía que podía romperse, aunque no cuándo.
                  Tesla quiere que la falla del andamio tenga su propio tipo, para atraparla sin confundirla con otras. Bron declaró la clase, pero sigue tirando un error genérico.
              """,
              sugiere="En `subir`, tirá la excepción propia: `throw FallaDeAndamio(\"se rompio el tablon \" + std::to_string(piso));`.",
              desafio="Tirá la falla con su propio tipo.",
              inicial='''
                  #include <iostream>
                  #include <stdexcept>
                  #include <string>

                  class FallaDeAndamio : public std::runtime_error {
                  public:
                      using std::runtime_error::runtime_error;
                  };

                  void subir(int piso)
                  {
                      if (piso == 3) {
                          throw std::runtime_error("algo paso");
                      }
                      std::cout << "Bron sube al piso " << piso << "\\n";
                  }

                  int main()
                  {
                      try {
                          for (int piso = 1; piso <= 4; piso++) {
                              subir(piso);
                          }
                      } catch (const FallaDeAndamio& e) {
                          std::cout << "La red ataja a Bron: " << e.what() << "\\n";
                      } catch (const std::exception& e) {
                          std::cout << "Error sin red: " << e.what() << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <stdexcept>
                  #include <string>

                  class FallaDeAndamio : public std::runtime_error {
                  public:
                      using std::runtime_error::runtime_error;
                  };

                  void subir(int piso)
                  {
                      if (piso == 3) {
                          throw FallaDeAndamio("se rompio el tablon " + std::to_string(piso));
                      }
                      std::cout << "Bron sube al piso " << piso << "\\n";
                  }

                  int main()
                  {
                      try {
                          for (int piso = 1; piso <= 4; piso++) {
                              subir(piso);
                          }
                      } catch (const FallaDeAndamio& e) {
                          std::cout << "La red ataja a Bron: " << e.what() << "\\n";
                      } catch (const std::exception& e) {
                          std::cout << "Error sin red: " << e.what() << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="La red ataja a Bron. Tesla le da un amuleto con forma de red: **el Amuleto del Catch**. —Para la próxima —dice—. Siempre hay una próxima.",
              imagen=["Un andamio de madera roto y una red de bronce tendida debajo, con alguien atajado.",
                      BRON + " cuelga de la red, aliviado.", TESLA + " le muestra un amuleto con forma de red."]),
        ],
    },
    {
        "titulo": "R05-N02 · Depuración y buenas prácticas",
        "misiones": [
            m(id="R05-N02-P1", titulo="La suposición que falla",
              lugar=TALLER, personajes="Bron, Tesla",
              carta="assert | assert(condicion) (#include <cassert>) corta el programa si la suposición es falsa · es para errores de PROGRAMACIÓN, no para validar al usuario",
              recompensa="xp 10, oro 10",
              escena="""
                  Un autómata camina en círculos. Tesla saca la lupa y un cuaderno: —Adivinar es lo más lento que hay. Bron escribió `promedio_ultimos(n)` con una suposición (`n` no puede ser más que la cantidad de pasos), y el `assert` corta el programa: alguien la está llamando mal.
              """,
              sugiere="El `assert` no está mal: avisa que `main` pide los últimos 5 pasos de una lista de 4. Pedí los que hay: `pasos.size()`.",
              desafio="Corregí la llamada para que la suposición se cumpla.",
              inicial='''
                  #include <cassert>
                  #include <iostream>
                  #include <vector>

                  double promedio_ultimos(const std::vector<int>& pasos, std::size_t n)
                  {
                      assert(n > 0 && n <= pasos.size());
                      double suma = 0;
                      for (std::size_t i = pasos.size() - n; i < pasos.size(); i++) {
                          suma += pasos[i];
                      }
                      return suma / n;
                  }

                  int main()
                  {
                      std::vector<int> pasos = {4, 6, 5, 7};
                      std::cout << "Promedio: " << promedio_ultimos(pasos, 5) << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <cassert>
                  #include <iostream>
                  #include <vector>

                  double promedio_ultimos(const std::vector<int>& pasos, std::size_t n)
                  {
                      assert(n > 0 && n <= pasos.size());
                      double suma = 0;
                      for (std::size_t i = pasos.size() - n; i < pasos.size(); i++) {
                          suma += pasos[i];
                      }
                      return suma / n;
                  }

                  int main()
                  {
                      std::vector<int> pasos = {4, 6, 5, 7};
                      std::cout << "Promedio: " << promedio_ultimos(pasos, pasos.size()) << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Cinco y medio. El `assert` encontró el error en un segundo; adivinando, Bron habría tardado una tarde.",
              imagen=["Un autómata caminando en círculos y un cuaderno con anotaciones.",
                      TESLA + " observa con una lupa.", BRON + " anota en el cuaderno."]),
            m(id="R05-N02-P2", titulo="La lectura de más",
              lugar=TALLER, personajes="Bron, Lima",
              carta="Leer en la condición | while (std::cin >> x) se detiene cuando la lectura falla · while (!std::cin.eof()) da una vuelta de más",
              recompensa="xp 10, oro 10",
              escena="""
                  Bron cuenta los pasos del autómata leyendo números hasta el final, con `while (!std::cin.eof())`. Hay tres números y cuenta cuatro: la última vuelta lee nada y la cuenta igual.
              """,
              sugiere="Leé **en la condición**: `while (std::cin >> paso)`. Si la lectura falla, el bucle termina antes de contar.",
              desafio="Leé en la condición del bucle.",
              entrada="4 6 5\n",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      int paso = 0;
                      int lecturas = 0;
                      int suma = 0;
                      while (!std::cin.eof()) {
                          std::cin >> paso;
                          lecturas++;
                          suma += paso;
                      }
                      std::cout << "Lecturas: " << lecturas << ", suma: " << suma << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      int paso = 0;
                      int lecturas = 0;
                      int suma = 0;
                      while (std::cin >> paso) {
                          lecturas++;
                          suma += paso;
                      }
                      std::cout << "Lecturas: " << lecturas << ", suma: " << suma << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres lecturas, quince pasos. Lima tacha `eof` de la lista de cosas que Bron puede usar.",
              imagen=["Una tira de papel con tres números y un cuarto casillero vacío.",
                      LIMA + " tacha una palabra en una lista.", BRON + " cuenta con los dedos."]),
            m(id="R05-N02-P3", titulo="La variable que tapa a otra",
              lugar=TALLER, personajes="Bron, Tesla",
              carta="Sombra | declarar otra variable con el MISMO nombre adentro de un bloque tapa a la de afuera · -Wshadow lo avisa · nombres claros",
              recompensa="xp 10, oro 10",
              escena="""
                  El contador de engranajes del Taller da siempre cero. Tesla mira el código y señala la línea: adentro del bucle, Bron escribió `int total = 0;` otra vez, y esa variable nueva tapa a la de afuera.
              """,
              sugiere="Adentro del bucle no declares otra `total`: sumá a la de afuera.",
              desafio="Sacá la variable que tapa a la otra.",
              inicial='''
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> cajas = {12, 7, 30};
                      int total = 0;
                      for (int c : cajas) {
                          int total = 0;
                          total += c;
                      }
                      std::cout << "Engranajes: " << total << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> cajas = {12, 7, 30};
                      int total = 0;
                      for (int c : cajas) {
                          total += c;
                      }
                      std::cout << "Engranajes: " << total << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Cuarenta y nueve. Tesla le recomienda compilar con `-Wshadow`: el Taller avisa estas cosas solo.",
              imagen=["Dos variables dibujadas como dos cajas con el mismo nombre, una tapando a la otra.",
                      TESLA + " levanta la caja de arriba.", BRON + " se tapa la cara."]),
        ],
    },
    {
        "titulo": "R05-N03 · Pruebas y medición",
        "misiones": [
            m(id="R05-N03-P1", titulo="¿Y la prueba?",
              lugar=BANCO, personajes="Bron, la Maestra Artífice",
              carta="Pruebas automáticas | una función comprobar(nombre, condición) que cuenta las que pasan · se corren todas cada vez que algo cambia",
              recompensa="xp 10, oro 10",
              escena="""
                  Bron dice que su función «ya anda». La Maestra Artífice no levanta la vista de la tableta: —¿Y la prueba?
                  Esta vez Bron tiene pruebas escritas: una de cada tres falla. La función que dice si un año es bisiesto se olvidó de la regla de los siglos.
              """,
              sugiere="Un año es bisiesto si es divisible por 4 y **no** por 100, salvo que sea divisible por 400.",
              desafio="Arreglá la función, no las pruebas.",
              inicial='''
                  #include <iostream>
                  #include <string>

                  bool bisiesto(int anio)
                  {
                      return anio % 4 == 0;
                  }

                  int pasan = 0;
                  int total = 0;

                  void comprobar(const std::string& nombre, bool ok)
                  {
                      total++;
                      if (ok) {
                          pasan++;
                      } else {
                          std::cout << "FALLA: " << nombre << "\\n";
                      }
                  }

                  int main()
                  {
                      comprobar("2024 es bisiesto", bisiesto(2024));
                      comprobar("1900 no es bisiesto", !bisiesto(1900));
                      comprobar("2000 es bisiesto", bisiesto(2000));
                      std::cout << pasan << " de " << total << " pruebas pasan\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  bool bisiesto(int anio)
                  {
                      return (anio % 4 == 0 && anio % 100 != 0) || anio % 400 == 0;
                  }

                  int pasan = 0;
                  int total = 0;

                  void comprobar(const std::string& nombre, bool ok)
                  {
                      total++;
                      if (ok) {
                          pasan++;
                      } else {
                          std::cout << "FALLA: " << nombre << "\\n";
                      }
                  }

                  int main()
                  {
                      comprobar("2024 es bisiesto", bisiesto(2024));
                      comprobar("1900 no es bisiesto", !bisiesto(1900));
                      comprobar("2000 es bisiesto", bisiesto(2000));
                      std::cout << pasan << " de " << total << " pruebas pasan\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres de tres, en verde. La Maestra Artífice sonríe **medio segundo**. Lima jura que fue un tic.",
              imagen=["Un banco de pruebas largo con tres lucecitas verdes encendidas.",
                      MAESTRA + " sonríe apenas.", BRON + " no lo puede creer."]),
            m(id="R05-N03-P2", titulo="El caso borde",
              lugar=BANCO, personajes="Lima, la Maestra Artífice",
              carta="Casos borde | lo vacío, el cero, uno solo, el máximo · ahí se esconden los errores · cada uno con su prueba",
              recompensa="xp 15, oro 15",
              escena="""
                  La función de Lima cuenta las palabras de un cartel. Con carteles normales anda. La Maestra Artífice agrega una prueba con el cartel **vacío**, y la función dice que tiene una palabra.
              """,
              sugiere="Contá las palabras leyéndolas con un `std::istringstream` (como en los Talleres): un texto vacío da cero.",
              desafio="Hacé que la función pase la prueba del cartel vacío.",
              inicial='''
                  #include <iostream>
                  #include <sstream>
                  #include <string>

                  int palabras(const std::string& cartel)
                  {
                      int n = 1;
                      for (char c : cartel) {
                          if (c == ' ') {
                              n++;
                          }
                      }
                      return n;
                  }

                  int main()
                  {
                      int pasan = 0;
                      pasan += palabras("abierto todo el dia") == 4;
                      pasan += palabras("cerrado") == 1;
                      pasan += palabras("") == 0;
                      std::cout << pasan << " de 3 pruebas pasan\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <sstream>
                  #include <string>

                  int palabras(const std::string& cartel)
                  {
                      std::istringstream ss(cartel);
                      std::string p;
                      int n = 0;
                      while (ss >> p) {
                          n++;
                      }
                      return n;
                  }

                  int main()
                  {
                      int pasan = 0;
                      pasan += palabras("abierto todo el dia") == 4;
                      pasan += palabras("cerrado") == 1;
                      pasan += palabras("") == 0;
                      std::cout << pasan << " de 3 pruebas pasan\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres de tres. La Maestra Artífice agrega una cuarta prueba: un cartel con espacios de más. También pasa.",
              imagen=["Un cartel en blanco colgado en el banco de pruebas, con una tilde verde.",
                      LIMA + " ajusta la función.", MAESTRA + " escribe otra prueba en la tableta."]),
            m(id="R05-N03-P3", titulo="La invariante bajo prueba",
              lugar=BANCO, personajes="Bron, la Maestra Artífice",
              carta="Probar una clase | se hacen muchas operaciones y después de CADA una se comprueba la invariante (0 <= presión <= 100)",
              recompensa="xp 15, oro 15",
              escena="""
                  La Maestra Artífice prueba la caldera de Bron con una secuencia de subidas y bajadas, y después de cada una revisa que la presión siga entre 0 y 100. `bajar` deja pasar presiones negativas.
              """,
              sugiere="`bajar` tiene que hacer lo mismo que `subir`: si el resultado se sale del rango, no cambia nada.",
              desafio="Hacé que `bajar` cuide la regla.",
              inicial='''
                  #include <iostream>

                  class Caldera {
                  public:
                      void subir(int n) { if (presion_ + n <= 100) presion_ += n; }
                      void bajar(int n) { presion_ -= n; }
                      int presion() const { return presion_; }

                  private:
                      int presion_ = 50;
                  };

                  int main()
                  {
                      Caldera c;
                      int pasos = 0;
                      int bien = 0;
                      for (int cambio : {30, -20, 40, -70, -50, 10}) {
                          if (cambio > 0) {
                              c.subir(cambio);
                          } else {
                              c.bajar(-cambio);
                          }
                          pasos++;
                          bien += c.presion() >= 0 && c.presion() <= 100;
                      }
                      std::cout << bien << " de " << pasos << " pasos cumplen la regla (presion final " << c.presion() << ")\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  class Caldera {
                  public:
                      void subir(int n) { if (presion_ + n <= 100) presion_ += n; }
                      void bajar(int n) { if (presion_ - n >= 0) presion_ -= n; }
                      int presion() const { return presion_; }

                  private:
                      int presion_ = 50;
                  };

                  int main()
                  {
                      Caldera c;
                      int pasos = 0;
                      int bien = 0;
                      for (int cambio : {30, -20, 40, -70, -50, 10}) {
                          if (cambio > 0) {
                              c.subir(cambio);
                          } else {
                              c.bajar(-cambio);
                          }
                          pasos++;
                          bien += c.presion() >= 0 && c.presion() <= 100;
                      }
                      std::cout << bien << " de " << pasos << " pasos cumplen la regla (presion final " << c.presion() << ")\\n";
                      return 0;
                  }
              ''',
              al_superar="Seis de seis. La Maestra Artífice tilda la caldera en su tableta: puede salir del Taller.",
              imagen=["Una caldera conectada a un banco de pruebas con cables y un manómetro.",
                      MAESTRA + " tilda la caldera en la tableta.", BRON + " desconecta los cables."]),
        ],
    },
    {
        "titulo": "R05-N04 · Las piezas de un juego",
        "misiones": [
            m(id="R05-N04-P1", titulo="La mochila que apila",
              lugar=MESA, personajes="Bron, Lima",
              carta="Inventario | std::map<std::string, int> mochila · agregar suma a lo que había · usar resta y borra si llega a 0",
              recompensa="xp 10, oro 10",
              escena="""
                  En la mesa hay un juego desarmado: una heroína de madera (Bron le puso la cara de Lima, «porque es la que más pelea»), enemigos de lata y una mochila. La mochila de Bron no apila: cada poción nueva pisa a las anteriores.
              """,
              sugiere="En `agregar`, sumá a lo que ya había: `items_[nombre] += cantidad;`.",
              desafio="Hacé que la mochila apile.",
              inicial='''
                  #include <iostream>
                  #include <map>
                  #include <string>

                  class Mochila {
                  public:
                      void agregar(const std::string& nombre, int cantidad) { items_[nombre] = cantidad; }
                      void mostrar() const
                      {
                          for (const auto& [n, c] : items_) {
                              std::cout << n << " x" << c << "\\n";
                          }
                      }

                  private:
                      std::map<std::string, int> items_;
                  };

                  int main()
                  {
                      Mochila m;
                      m.agregar("pocion", 2);
                      m.agregar("tuerca", 5);
                      m.agregar("pocion", 3);
                      m.mostrar();
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <map>
                  #include <string>

                  class Mochila {
                  public:
                      void agregar(const std::string& nombre, int cantidad) { items_[nombre] += cantidad; }
                      void mostrar() const
                      {
                          for (const auto& [n, c] : items_) {
                              std::cout << n << " x" << c << "\\n";
                          }
                      }

                  private:
                      std::map<std::string, int> items_;
                  };

                  int main()
                  {
                      Mochila m;
                      m.agregar("pocion", 2);
                      m.agregar("tuerca", 5);
                      m.agregar("pocion", 3);
                      m.mostrar();
                      return 0;
                  }
              ''',
              al_superar="Cinco pociones y cinco tuercas. Lima no sabe si ofenderse por la cara de la heroína; decide que no, por ahora.",
              imagen=["Una mesa con piezas de un juego: una heroína de madera con la cara de Lima, enemigos de lata y una mochila.",
                      BRON + " apila pociones.", LIMA + " mira la heroína con desconfianza."]),
            m(id="R05-N04-P2", titulo="La IA del enemigo de lata",
              lugar=MESA, personajes="Bron, Tesla",
              carta="IA simple | se decide en orden de prioridad: primero lo más urgente (huir si queda poca vida), después atacar si está cerca, si no patrullar",
              recompensa="xp 15, oro 15",
              escena="""
                  El enemigo de lata decide qué hacer en cada turno. El de Bron ataca aunque le quede casi nada de vida: la pregunta por la distancia va antes que la de la vida.
              """,
              sugiere="Primero preguntá si la vida es menor que 30 (huir), después si está cerca (atacar), y si no, patrullar.",
              desafio="Ordená las decisiones por prioridad.",
              inicial='''
                  #include <iostream>
                  #include <string>

                  std::string decidir(int vida, int distancia)
                  {
                      if (distancia <= 2) {
                          return "atacar";
                      } else if (vida < 30) {
                          return "huir";
                      }
                      return "patrullar";
                  }

                  int main()
                  {
                      std::cout << "vida 80, distancia 1: " << decidir(80, 1) << "\\n";
                      std::cout << "vida 20, distancia 1: " << decidir(20, 1) << "\\n";
                      std::cout << "vida 50, distancia 9: " << decidir(50, 9) << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  std::string decidir(int vida, int distancia)
                  {
                      if (vida < 30) {
                          return "huir";
                      } else if (distancia <= 2) {
                          return "atacar";
                      }
                      return "patrullar";
                  }

                  int main()
                  {
                      std::cout << "vida 80, distancia 1: " << decidir(80, 1) << "\\n";
                      std::cout << "vida 20, distancia 1: " << decidir(20, 1) << "\\n";
                      std::cout << "vida 50, distancia 9: " << decidir(50, 9) << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Con poca vida, el enemigo de lata huye. Oto pide que haya un enemigo que sea un guiso violeta; se lo agregan.",
              imagen=["Un enemigo de lata huyendo por la mesa del juego.",
                      TESLA + " mueve una ficha.", BRON + " se ríe."]),
            m(id="R05-N04-P3", titulo="El combate que se puede repetir",
              lugar=MESA, personajes="Bron, Lyn",
              carta="Azar reproducible | std::mt19937 gen(semilla) · el mismo combate con la misma semilla · daño = 5 + gen() % 6",
              recompensa="xp 15, oro 15",
              escena="""
                  Lyn apuesta a que la heroína le gana al guiso violeta en tres golpes. Para que nadie haga trampa, el combate usa una semilla fija: la 2026. El combate de Bron usa la semilla 1, y Lyn reclama.
              """,
              sugiere="Cambiá la semilla a 2026 y hacé que el combate siga hasta que la vida del guiso llegue a 0 o menos.",
              desafio="Usá la semilla acordada y peleá hasta el final.",
              inicial='''
                  #include <iostream>
                  #include <random>

                  int main()
                  {
                      std::mt19937 gen(1);
                      int vida = 25;
                      int golpe = 0;
                      for (int i = 0; i < 2; i++) {
                          int danio = 5 + static_cast<int>(gen() % 6);
                          vida -= danio;
                          golpe++;
                          std::cout << "Golpe " << golpe << ": " << danio << " de dano, le queda " << vida << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <random>

                  int main()
                  {
                      std::mt19937 gen(2026);
                      int vida = 25;
                      int golpe = 0;
                      while (vida > 0) {
                          int danio = 5 + static_cast<int>(gen() % 6);
                          vida -= danio;
                          golpe++;
                          std::cout << "Golpe " << golpe << ": " << danio << " de dano, le queda " << vida << "\\n";
                      }
                      std::cout << "El guiso violeta cae en " << golpe << " golpes\\n";
                      return 0;
                  }
              ''',
              al_superar="Con la semilla acordada, el combate es siempre el mismo. Lyn lo juega diez veces para estar segura.",
              imagen=["Una heroína de madera golpeando a un guiso violeta con ojos en la mesa del juego.",
                      LYN + " cuenta los golpes con su cronómetro.", BRON + " tira los dados."]),
        ],
    },
    {
        "titulo": "R05-N05 · Estados y el bucle de juego",
        "misiones": [
            m(id="R05-N05-P1", titulo="La velocidad que no depende de la compu",
              lugar=PENDULO, personajes="Bron, Tesla",
              carta="Delta time | x += velocidad * dt · dt es el tiempo de cada vuelta, en segundos · así se mueve igual en una compu rápida o lenta",
              recompensa="xp 10, oro 10",
              escena="""
                  En el Taller gira el Gran Péndulo, y con cada vaivén los autómatas se mueven un poquito. El autómata de Bron avanza 40 en cada vuelta, sin importar cuánto dura la vuelta: en una compu rápida cruza la sala en un segundo.
              """,
              sugiere="La velocidad es por segundo: en cada vuelta se avanza `velocidad * dt`.",
              desafio="Mové el autómata con el tiempo de cada vuelta.",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      double x = 0;
                      double velocidad = 40;
                      double tiempos[] = {0.5, 0.25, 0.25};
                      for (double dt : tiempos) {
                          x += velocidad;
                          std::cout << "dt " << dt << " -> x = " << x << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      double x = 0;
                      double velocidad = 40;
                      double tiempos[] = {0.5, 0.25, 0.25};
                      for (double dt : tiempos) {
                          x += velocidad * dt;
                          std::cout << "dt " << dt << " -> x = " << x << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Un segundo, cuarenta pasos, en cualquier compu. Tesla lo prueba con el péndulo más rápido y más lento: llega igual.",
              imagen=["El Gran Péndulo oscilando sobre una sala con autómatas en fila.",
                      TESLA + " mide el vaivén.", BRON + " empuja un autómata."]),
            m(id="R05-N05-P2", titulo="La pausa que vuelve",
              lugar=PENDULO, personajes="Lima, Bron",
              carta="Estados del juego | Menu, Jugando, Pausa, Fin · la misma tecla hace cosas distintas según el estado · cada estado sabe a cuál pasa",
              recompensa="xp 15, oro 15",
              escena="""
                  Lima prueba el juego: aprieta `p` para pausar y otra vez `p` para volver… y el juego se queda en pausa para siempre. A la pausa de Bron le falta el camino de vuelta.
              """,
              sugiere="En el estado `Pausa`, la tecla `p` tiene que volver a `Jugando`.",
              desafio="Hacé que la pausa vuelva al juego.",
              entrada="enter p p x q\n",
              inicial='''
                  #include <iostream>
                  #include <string>

                  enum class Estado { Menu, Jugando, Pausa, Fin };

                  std::string nombre(Estado e)
                  {
                      switch (e) {
                      case Estado::Menu: return "menu";
                      case Estado::Jugando: return "jugando";
                      case Estado::Pausa: return "pausa";
                      case Estado::Fin: return "fin";
                      }
                      return "?";
                  }

                  int main()
                  {
                      Estado e = Estado::Menu;
                      std::string tecla;
                      while (e != Estado::Fin && std::cin >> tecla) {
                          switch (e) {
                          case Estado::Menu:
                              if (tecla == "enter") e = Estado::Jugando;
                              break;
                          case Estado::Jugando:
                              if (tecla == "p") e = Estado::Pausa;
                              if (tecla == "q") e = Estado::Fin;
                              break;
                          case Estado::Pausa:
                              break;
                          case Estado::Fin:
                              break;
                          }
                          std::cout << tecla << " -> " << nombre(e) << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  enum class Estado { Menu, Jugando, Pausa, Fin };

                  std::string nombre(Estado e)
                  {
                      switch (e) {
                      case Estado::Menu: return "menu";
                      case Estado::Jugando: return "jugando";
                      case Estado::Pausa: return "pausa";
                      case Estado::Fin: return "fin";
                      }
                      return "?";
                  }

                  int main()
                  {
                      Estado e = Estado::Menu;
                      std::string tecla;
                      while (e != Estado::Fin && std::cin >> tecla) {
                          switch (e) {
                          case Estado::Menu:
                              if (tecla == "enter") e = Estado::Jugando;
                              break;
                          case Estado::Jugando:
                              if (tecla == "p") e = Estado::Pausa;
                              if (tecla == "q") e = Estado::Fin;
                              break;
                          case Estado::Pausa:
                              if (tecla == "p") e = Estado::Jugando;
                              break;
                          case Estado::Fin:
                              break;
                          }
                          std::cout << tecla << " -> " << nombre(e) << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Pausa, juego, fin. Lima sale de la pausa y gana la partida en dos minutos.",
              imagen=["Una pantalla de bronce con la palabra PAUSA tachada.",
                      LIMA + " aprieta una tecla con fuerza.", BRON + " mira el diagrama de estados."]),
            m(id="R05-N05-P3", titulo="Escuchar, actualizar, dibujar",
              lugar=PENDULO, personajes="Bron, Tesla",
              carta="El bucle de juego | cada vuelta: 1) entrada 2) actualizar 3) dibujar · si se dibuja antes de actualizar, la pantalla va un paso atrás",
              recompensa="xp 10, oro 10",
              escena="""
                  En cada vaivén del péndulo, los autómatas escuchan, se mueven y encienden sus luces. En el bucle de Bron, el autómata enciende las luces **antes** de moverse, y la pantalla siempre muestra dónde estaba, no dónde está.
              """,
              sugiere="Dentro del bucle, primero actualizá la posición y después dibujá.",
              desafio="Ordená las tres partes del bucle.",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      int x = 0;
                      for (int vuelta = 1; vuelta <= 3; vuelta++) {
                          int paso = 2;
                          std::cout << "vuelta " << vuelta << ": dibujo en x = " << x << "\\n";
                          x += paso;
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      int x = 0;
                      for (int vuelta = 1; vuelta <= 3; vuelta++) {
                          int paso = 2;
                          x += paso;
                          std::cout << "vuelta " << vuelta << ": dibujo en x = " << x << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Ahora la luz se enciende donde está el autómata. Tesla dice que así se ve por dentro cualquier juego.",
              imagen=["Una tira de tres cuadros, como una historieta, con un autómata avanzando.",
                      TESLA + " señala el orden de los cuadros.", BRON + " cambia de lugar dos cuadros."]),
        ],
    },
    {
        "titulo": "R05-N06 · Jefe: el Minotauro del Laberinto",
        "misiones": [
            m(id="R05-N06-P1", titulo="El plano del Laberinto",
              lugar=LABERINTO, personajes="Bron, Tesla",
              criatura="dragon",
              carta="Mapa de texto | std::vector<std::string> mapa; · mapa[fila][columna] es una baldosa · se busca un carácter recorriendo filas y columnas",
              recompensa="xp 15, oro 15",
              escena="""
                  Debajo del Taller está el **Laberinto**, y adentro el **Minotauro**: no persigue, **embiste**. Tesla le da a Bron una hoja con el laberinto dibujado: `#` son paredes, `B` es Bron y `M` el Minotauro. Antes de entrar, hay que saber dónde está cada uno. Bron solo encontró a Bron.
              """,
              sugiere="Recorré el mapa y, si la baldosa es `M`, guardá su fila y su columna.",
              desafio="Encontrá también al Minotauro.",
              inicial='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::string> mapa = {
                          "#########",
                          "#B..#...#",
                          "#.#.#.#.#",
                          "#.#...#M#",
                          "#########",
                      };
                      int bf = -1, bc = -1, mf = -1, mc = -1;
                      for (int f = 0; f < static_cast<int>(mapa.size()); f++) {
                          for (int c = 0; c < static_cast<int>(mapa[f].size()); c++) {
                              if (mapa[f][c] == 'B') {
                                  bf = f;
                                  bc = c;
                              }
                          }
                      }
                      std::cout << "Bron en (" << bf << ", " << bc << ")\\n";
                      std::cout << "Minotauro en (" << mf << ", " << mc << ")\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::string> mapa = {
                          "#########",
                          "#B..#...#",
                          "#.#.#.#.#",
                          "#.#...#M#",
                          "#########",
                      };
                      int bf = -1, bc = -1, mf = -1, mc = -1;
                      for (int f = 0; f < static_cast<int>(mapa.size()); f++) {
                          for (int c = 0; c < static_cast<int>(mapa[f].size()); c++) {
                              if (mapa[f][c] == 'B') {
                                  bf = f;
                                  bc = c;
                              } else if (mapa[f][c] == 'M') {
                                  mf = f;
                                  mc = c;
                              }
                          }
                      }
                      std::cout << "Bron en (" << bf << ", " << bc << ")\\n";
                      std::cout << "Minotauro en (" << mf << ", " << mc << ")\\n";
                      return 0;
                  }
              ''',
              al_superar="El Minotauro está en la esquina de abajo a la derecha. Bron dobla el plano y se lo guarda en el bolsillo de la llave.",
              imagen=["Un plano de laberinto dibujado a mano, con una B y una M marcadas.",
                      TESLA + " le entrega el plano.", BRON + " lo mira de cerca."]),
            m(id="R05-N06-P2", titulo="La línea recta",
              lugar=LABERINTO, personajes="Bron, Lima",
              criatura="dragon",
              carta="Línea de visión | el Minotauro embiste si están en la misma fila (o columna) y NO hay paredes entre los dos · se recorre el tramo del medio",
              recompensa="xp 15, oro 15",
              escena="""
                  El Minotauro embiste si ve a Bron en línea recta. La función de Bron dice que lo ve siempre que estén en la misma fila, aunque haya una pared en el medio. Lima, que esta vez bajó, se esconde detrás de esa pared por las dudas.
              """,
              sugiere="Además de estar en la misma fila, recorré las columnas entre los dos: si alguna es `#`, no lo ve.",
              desafio="Tené en cuenta las paredes.",
              inicial='''
                  #include <algorithm>
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  bool lo_ve(const std::vector<std::string>& mapa, int fila, int c1, int c2)
                  {
                      return fila >= 0;
                  }

                  int main()
                  {
                      std::vector<std::string> mapa = {
                          "#########",
                          "#B..#..M#",
                          "#.....M.#",
                          "#########",
                      };
                      std::cout << "Fila 1 (B en 1, M en 7): " << (lo_ve(mapa, 1, 1, 7) ? "embiste" : "no lo ve") << "\\n";
                      std::cout << "Fila 2 (B en 1, M en 6): " << (lo_ve(mapa, 2, 1, 6) ? "embiste" : "no lo ve") << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <algorithm>
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  bool lo_ve(const std::vector<std::string>& mapa, int fila, int c1, int c2)
                  {
                      for (int c = std::min(c1, c2) + 1; c < std::max(c1, c2); c++) {
                          if (mapa[fila][c] == '#') {
                              return false;
                          }
                      }
                      return true;
                  }

                  int main()
                  {
                      std::vector<std::string> mapa = {
                          "#########",
                          "#B..#..M#",
                          "#.....M.#",
                          "#########",
                      };
                      std::cout << "Fila 1 (B en 1, M en 7): " << (lo_ve(mapa, 1, 1, 7) ? "embiste" : "no lo ve") << "\\n";
                      std::cout << "Fila 2 (B en 1, M en 6): " << (lo_ve(mapa, 2, 1, 6) ? "embiste" : "no lo ve") << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Con la pared en el medio, el Minotauro no lo ve. En el pasillo abierto, sí: Bron sale de ahí corriendo.",
              imagen=["Un pasillo del laberinto con una pared en el medio y el Minotauro al fondo.",
                      LIMA + " escondida detrás de la pared.", BRON + " cruza el pasillo abierto a toda velocidad."]),
            m(id="R05-N06-P3", titulo="El mapa que no se puede jugar",
              lugar=LABERINTO, personajes="Bron, Tesla",
              criatura="dragon",
              carta="Validar con excepciones | un mapa sin B o sin M no se puede jugar · cargar() tira std::runtime_error con el problema · main lo atrapa y lo muestra",
              recompensa="xp 15, oro 15",
              escena="""
                  Tesla le pasa a Bron varios planos del Laberinto, y algunos están mal dibujados: uno no tiene Minotauro, otro tiene dos Bron. La función de Bron los carga igual.
              """,
              sugiere="En `validar`, contá las `B` y las `M`: si no hay exactamente una de cada una, tirá un `std::runtime_error` que diga cuál falta o sobra.",
              desafio="Validá el plano antes de jugarlo.",
              inicial='''
                  #include <iostream>
                  #include <stdexcept>
                  #include <string>
                  #include <vector>

                  void validar(const std::vector<std::string>& mapa)
                  {
                      int b = 0, m = 0;
                      for (const auto& fila : mapa) {
                          for (char c : fila) {
                              if (c == 'B') b++;
                              if (c == 'M') m++;
                          }
                      }
                  }

                  int main()
                  {
                      std::vector<std::vector<std::string>> planos = {
                          {"#####", "#B.M#", "#####"},
                          {"#####", "#B..#", "#####"},
                          {"#####", "#BBM#", "#####"},
                      };
                      for (std::size_t i = 0; i < planos.size(); i++) {
                          try {
                              validar(planos[i]);
                              std::cout << "Plano " << i + 1 << ": se puede jugar\\n";
                          } catch (const std::runtime_error& e) {
                              std::cout << "Plano " << i + 1 << ": " << e.what() << "\\n";
                          }
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <stdexcept>
                  #include <string>
                  #include <vector>

                  void validar(const std::vector<std::string>& mapa)
                  {
                      int b = 0, m = 0;
                      for (const auto& fila : mapa) {
                          for (char c : fila) {
                              if (c == 'B') b++;
                              if (c == 'M') m++;
                          }
                      }
                      if (b != 1) {
                          throw std::runtime_error("tiene " + std::to_string(b) + " Bron");
                      }
                      if (m != 1) {
                          throw std::runtime_error("tiene " + std::to_string(m) + " Minotauros");
                      }
                  }

                  int main()
                  {
                      std::vector<std::vector<std::string>> planos = {
                          {"#####", "#B.M#", "#####"},
                          {"#####", "#B..#", "#####"},
                          {"#####", "#BBM#", "#####"},
                      };
                      for (std::size_t i = 0; i < planos.size(); i++) {
                          try {
                              validar(planos[i]);
                              std::cout << "Plano " << i + 1 << ": se puede jugar\\n";
                          } catch (const std::runtime_error& e) {
                              std::cout << "Plano " << i + 1 << ": " << e.what() << "\\n";
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="Solo el primer plano se puede jugar. Tesla tira los otros dos al fuego, menos el de dos Bron, que se lo queda «de recuerdo».",
              imagen=["Tres planos de laberinto sobre una mesa; dos tachados con una cruz roja.",
                      TESLA + " se guarda uno de los planos tachados.", BRON + " sostiene el bueno."]),
            m(id="R05-N06-P4", titulo="El engranaje del cuello",
              lugar=LABERINTO, personajes="Bron, Tesla, Lima",
              criatura="dragon",
              carta="Recorrer un camino | cada letra mueve una baldosa (N, S, E, O) · si la siguiente es pared, el camino no sirve · se cuentan los pasos hasta la M",
              recompensa="xp 25, oro 30",
              item="Engranaje del Portal",
              escena="""
                  Bron no entra a los golpes: entra con el plano. Escribió el camino hasta el Minotauro letra por letra, para que se quede trabado en un pasillo en diagonal. Pero su recorrido no revisa las paredes, y lo mete adentro de una.
              """,
              sugiere="Antes de moverte, mirá la baldosa de destino: si es `#`, mostrá `Pared en el paso <n>` y cortá. Si llegás a la `M`, mostrá en cuántos pasos.",
              desafio="Revisá las paredes en cada paso del camino.",
              entrada="EESSEES\n",
              inicial='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::string> mapa = {
                          "#######",
                          "#B..#.#",
                          "#.#.#.#",
                          "#.#...#",
                          "#...#M#",
                          "#######",
                      };
                      std::string camino;
                      std::cin >> camino;
                      int f = 1, c = 1;
                      int pasos = 0;
                      for (char d : camino) {
                          int nf = f, nc = c;
                          if (d == 'N') nf--;
                          if (d == 'S') nf++;
                          if (d == 'E') nc++;
                          if (d == 'O') nc--;
                          f = nf;
                          c = nc;
                          pasos++;
                      }
                      std::cout << "Bron termina en (" << f << ", " << c << ") despues de " << pasos << " pasos\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::string> mapa = {
                          "#######",
                          "#B..#.#",
                          "#.#.#.#",
                          "#.#...#",
                          "#...#M#",
                          "#######",
                      };
                      std::string camino;
                      std::cin >> camino;
                      int f = 1, c = 1;
                      int pasos = 0;
                      for (char d : camino) {
                          int nf = f, nc = c;
                          if (d == 'N') nf--;
                          if (d == 'S') nf++;
                          if (d == 'E') nc++;
                          if (d == 'O') nc--;
                          pasos++;
                          if (mapa[nf][nc] == '#') {
                              std::cout << "Pared en el paso " << pasos << "\\n";
                              return 0;
                          }
                          f = nf;
                          c = nc;
                          if (mapa[f][c] == 'M') {
                              std::cout << "Bron llega al Minotauro en " << pasos << " pasos\\n";
                              return 0;
                          }
                      }
                      std::cout << "Bron termina en (" << f << ", " << c << ") despues de " << pasos << " pasos\\n";
                      return 0;
                  }
              ''',
              al_superar="El Minotauro embiste, se traba en el pasillo y el engranaje enorme se le suelta del cuello. Es **el Engranaje del Portal**: tiene los mismos dientes que las bisagras del Vidriero. Tesla lo mira y, por primera vez, no termina la frase de nadie.",
              imagen=["Un Minotauro de hierro trabado en un pasillo estrecho del laberinto, con la cadena del cuello rota.",
                      BRON + " sostiene un engranaje enorme de bronce oscuro.", TESLA + " lo mira en silencio; " + LIMA + " se asoma detrás."]),
        ],
    },
]
