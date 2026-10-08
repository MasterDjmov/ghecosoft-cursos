from gencpp import m
from cpp_r01 import BRON, TESLA, LIMA, LYN, OTO, GHECO

BIBLIOTECA = "La Gran Biblioteca"
ESTANTES = "Los estantes de la Gran Biblioteca"
DEPOSITO = "El depósito de la Biblioteca"
INDICE = "El índice de la Gran Biblioteca"
HERRAMIENTAS = "El ala de las herramientas"
CONTROL = "La sala de control de la Biblioteca"
LECTURA = "La sala de lectura"
TALLER = "El taller de la Biblioteca"
SOTANOS = "Los sótanos inundados de la Gran Biblioteca"
KRAKEN = "el Kraken de los Contenedores (pulpo gigante de piel azul oscura con ventosas que brillan, que lleva cajas, estantes y libros enganchados en los tentáculos)"

NODOS = [
    {
        "titulo": "R04-N01 · Plantillas",
        "misiones": [
            m(id="R04-N01-P1", titulo="Un molde para cualquier tipo",
              lugar=BIBLIOTECA, personajes="Bron, Lima, Tesla",
              carta="Plantilla de función | template <typename T> T mayor(T a, T b) · el compilador arma una versión por cada tipo con que la llames",
              recompensa="xp 10, oro 10",
              escena="""
                  En la puerta de la Gran Biblioteca, Tesla explica que adentro no hay un plano por pieza, sino **moldes**. A Lima se le cae la lupa del ojo. Bron, en cambio, tiene una función `mayor` que solo sabe de enteros, y con decimales se come la coma.
              """,
              sugiere="Convertila en plantilla: `template <typename T>` arriba, y `T` en lugar de `int` en los parámetros y en lo que devuelve.",
              desafio="Hacé que `mayor` sirva para cualquier tipo.",
              inicial='''
                  #include <iostream>
                  #include <string>

                  int mayor(int a, int b)
                  {
                      return a > b ? a : b;
                  }

                  int main()
                  {
                      std::cout << "mayor: " << mayor(3, 9) << "\\n";
                      std::cout << "mayor: " << mayor(2.5, 1.5) << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  template <typename T>
                  T mayor(T a, T b)
                  {
                      return a > b ? a : b;
                  }

                  int main()
                  {
                      std::cout << "mayor: " << mayor(3, 9) << "\\n";
                      std::cout << "mayor: " << mayor(2.5, 1.5) << "\\n";
                      std::cout << "mayor: " << mayor(std::string("lima"), std::string("bron")) << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Nueve, dos y medio, y «lima» (que va después de «bron» en el diccionario). Lima se pone colorada.",
              imagen=["La puerta enorme de la Gran Biblioteca, con moldes de bronce colgados como llaves.",
                      LIMA + " recoge su lupa del piso.", TESLA + " señala un molde."]),
            m(id="R04-N01-P2", titulo="La caja de cualquier cosa",
              lugar=BIBLIOTECA, personajes="Bron, Oto",
              carta="Plantilla de clase | template <typename T> class Caja { T dentro_; }; · Caja<int>, Caja<std::string> · una clase, muchas cajas",
              recompensa="xp 15, oro 15",
              escena="""
                  Bron hizo una caja para guardar tuercas (enteros). Oto quiere una igual para guardar una receta (texto), y la caja de Bron no la acepta.
              """,
              sugiere="Hacé la clase plantilla: `template <typename T>` arriba de la clase y `T` en lugar de `int`. Después se usa `Caja<int>` y `Caja<std::string>`.",
              desafio="Convertí la caja en una plantilla.",
              inicial='''
                  #include <iostream>
                  #include <string>

                  class Caja {
                  public:
                      explicit Caja(int x) : dentro_(x) {}
                      const int& abrir() const { return dentro_; }

                  private:
                      int dentro_;
                  };

                  int main()
                  {
                      Caja tuercas(40);
                      Caja receta(std::string("guiso violeta"));
                      std::cout << tuercas.abrir() << "\\n";
                      std::cout << receta.abrir() << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  template <typename T>
                  class Caja {
                  public:
                      explicit Caja(T x) : dentro_(x) {}
                      const T& abrir() const { return dentro_; }

                  private:
                      T dentro_;
                  };

                  int main()
                  {
                      Caja<int> tuercas(40);
                      Caja<std::string> receta(std::string("guiso violeta"));
                      std::cout << tuercas.abrir() << "\\n";
                      std::cout << receta.abrir() << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Cuarenta tuercas en una caja, el guiso violeta en otra, con el mismo plano. Oto pide una tercera para el cucharón.",
              imagen=["Dos cajas de bronce iguales: una con tuercas y otra con una receta enrollada.",
                      OTO + " guarda la receta.", BRON + " cierra la caja de tuercas."]),
            m(id="R04-N01-P3", titulo="Solo enteros, por favor",
              lugar=BIBLIOTECA, personajes="Lima, Tesla",
              carta="Concepto | template <std::integral T> acepta solo tipos enteros (#include <concepts>) · si no cumple, el error lo dice claro",
              recompensa="xp 15, oro 15",
              escena="""
                  La función `es_par` solo tiene sentido con enteros. Lima la limitó con un **concepto**, pero eligió el equivocado: `std::floating_point` (los decimales), y ahora no acepta los enteros que le pasa Tesla.
              """,
              sugiere="El concepto de los enteros es `std::integral`.",
              desafio="Elegí el concepto correcto.",
              inicial='''
                  #include <concepts>
                  #include <iostream>

                  template <std::floating_point T>
                  bool es_par(T x)
                  {
                      return x % 2 == 0;
                  }

                  int main()
                  {
                      std::cout << "4: " << (es_par(4) ? "par" : "impar") << "\\n";
                      std::cout << "7: " << (es_par(7L) ? "par" : "impar") << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <concepts>
                  #include <iostream>

                  template <std::integral T>
                  bool es_par(T x)
                  {
                      return x % 2 == 0;
                  }

                  int main()
                  {
                      std::cout << "4: " << (es_par(4) ? "par" : "impar") << "\\n";
                      std::cout << "7: " << (es_par(7L) ? "par" : "impar") << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Cuatro par, siete impar. Tesla prueba con 2.5, para ver qué pasa: el error dice clarito que no es un entero.",
              imagen=["Una puerta de biblioteca con un cartel que dice «solo enteros».",
                      LIMA + " cambia el cartel.", TESLA + " intenta pasar con un 2.5 en la mano."]),
        ],
    },
    {
        "titulo": "R04-N02 · Iteradores",
        "misiones": [
            m(id="R04-N02-P1", titulo="El estante al revés",
              lugar=ESTANTES, personajes="Bron, Lima",
              carta="Al revés | rbegin() y rend() recorren de atrás para adelante · for (auto it = v.rbegin(); it != v.rend(); ++it)",
              recompensa="xp 10, oro 10",
              escena="""
                  Los bibliotecarios recorren los estantes con un dedo de bronce. Lima quiere leer el estante de los libros nuevos de atrás para adelante (el último que llegó, primero), y el dedo de Bron va hacia adelante.
              """,
              sugiere="Usá `rbegin()` y `rend()`: el dedo arranca en el último y avanza hacia el primero con el mismo `++`.",
              desafio="Recorré el estante al revés.",
              inicial='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::string> nuevos = {"Poleas", "Vapor", "Relojes", "Vitrales"};
                      for (auto it = nuevos.begin(); it != nuevos.end(); ++it) {
                          std::cout << *it << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::string> nuevos = {"Poleas", "Vapor", "Relojes", "Vitrales"};
                      for (auto it = nuevos.rbegin(); it != nuevos.rend(); ++it) {
                          std::cout << *it << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="«Vitrales» primero. Lima lo saca del estante antes que nadie.",
              imagen=["Un estante de libros con un dedo de bronce que apunta al último.",
                      LIMA + " saca el libro de los vitrales.", BRON + " sostiene el dedo de bronce."]),
            m(id="R04-N02-P2", titulo="¿En qué lugar estaba?",
              lugar=ESTANTES, personajes="Bron, Tesla",
              carta="distance | std::find devuelve un iterador · std::distance(v.begin(), it) dice en qué posición quedó",
              recompensa="xp 10, oro 10",
              escena="""
                  Tesla le pide a Bron que encuentre el libro de los relojes y le diga **en qué lugar** del estante está. Bron lo encuentra, pero le contesta el título: ya lo sabía.
              """,
              sugiere="`std::distance(estante.begin(), it)` cuenta cuántos pasos hay desde el principio hasta el iterador.",
              desafio="Mostrá la posición, no el título.",
              inicial='''
                  #include <algorithm>
                  #include <iostream>
                  #include <iterator>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::string> estante = {"Poleas", "Vapor", "Relojes", "Vitrales"};
                      auto it = std::find(estante.begin(), estante.end(), "Relojes");
                      std::cout << "Relojes esta en el lugar " << *it << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <algorithm>
                  #include <iostream>
                  #include <iterator>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::string> estante = {"Poleas", "Vapor", "Relojes", "Vitrales"};
                      auto it = std::find(estante.begin(), estante.end(), "Relojes");
                      std::cout << "Relojes esta en el lugar " << std::distance(estante.begin(), it) << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Lugar 2 (contando desde 0, como todo en la Ciudadela).",
              imagen=["Un estante con cuatro libros numerados del 0 al 3 y una flecha sobre el 2.",
                      TESLA + " cuenta con el compás.", BRON + " señala el libro."]),
            m(id="R04-N02-P3", titulo="Copiar a una caja que crece",
              lugar=ESTANTES, personajes="Lima, Bron",
              carta="back_inserter | std::copy_if(..., std::back_inserter(salida), cond) hace push_back por cada uno · la salida empieza VACÍA",
              recompensa="xp 15, oro 15",
              escena="""
                  Lima quiere copiar a otra caja solo los libros gruesos (más de 300 páginas). Bron preparó una caja del tamaño del estante entero, y quedan lugares vacíos al final, llenos de ceros.
              """,
              sugiere="Empezá con la caja vacía y copiá con `std::back_inserter(gruesos)`: agrega uno por cada libro que cumple, ni uno más.",
              desafio="Copiá a una caja que crece sola.",
              inicial='''
                  #include <algorithm>
                  #include <iostream>
                  #include <iterator>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> paginas = {120, 450, 80, 610, 300, 350};
                      std::vector<int> gruesos(paginas.size());
                      std::copy_if(paginas.begin(), paginas.end(), gruesos.begin(), [](int p) { return p > 300; });
                      std::cout << "Gruesos (" << gruesos.size() << "):";
                      for (int p : gruesos) {
                          std::cout << " " << p;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <algorithm>
                  #include <iostream>
                  #include <iterator>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> paginas = {120, 450, 80, 610, 300, 350};
                      std::vector<int> gruesos;
                      std::copy_if(paginas.begin(), paginas.end(), std::back_inserter(gruesos), [](int p) { return p > 300; });
                      std::cout << "Gruesos (" << gruesos.size() << "):";
                      for (int p : gruesos) {
                          std::cout << " " << p;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres libros gruesos y ningún lugar vacío. El de 300 páginas justas se queda en el estante, por poco.",
              imagen=["Una caja con tres libros gruesos, al lado de un estante.",
                      LIMA + " mide un libro con el calibre.", BRON + " mete los libros en la caja."]),
        ],
    },
    {
        "titulo": "R04-N03 · Pilas, colas y otras secuencias",
        "misiones": [
            m(id="R04-N03-P1", titulo="La torre de platos",
              lugar="El comedor de los artífices", personajes="Oto, Bron",
              carta="stack | std::stack: push pone arriba · top mira el de arriba · pop lo saca · el ÚLTIMO que entra es el PRIMERO que sale",
              recompensa="xp 10, oro 10",
              escena="""
                  Oto apila los platos del comedor y siempre saca el de arriba. Bron modeló la torre con una **cola**, y en su programa Oto saca el plato de abajo de todo. La torre se viene abajo.
              """,
              sugiere="Una torre de platos es una **pila**: cambiá `std::queue` por `std::stack` (y `front()` por `top()`).",
              desafio="Modelá la torre de platos con una pila.",
              inicial='''
                  #include <iostream>
                  #include <queue>
                  #include <stack>
                  #include <string>

                  int main()
                  {
                      std::queue<std::string> platos;
                      for (std::string p : {"plato hondo", "plato playo", "plato de postre"}) {
                          platos.push(p);
                      }
                      while (!platos.empty()) {
                          std::cout << "Oto saca: " << platos.front() << "\\n";
                          platos.pop();
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <queue>
                  #include <stack>
                  #include <string>

                  int main()
                  {
                      std::stack<std::string> platos;
                      for (std::string p : {"plato hondo", "plato playo", "plato de postre"}) {
                          platos.push(p);
                      }
                      while (!platos.empty()) {
                          std::cout << "Oto saca: " << platos.top() << "\\n";
                          platos.pop();
                      }
                      return 0;
                  }
              ''',
              al_superar="El de postre primero, como corresponde. La torre de platos sigue en pie.",
              imagen=["Una torre alta de platos sobre una mesada, con el de arriba levantándose.",
                      OTO + " saca el plato de arriba.", BRON + " sostiene la torre, nervioso."]),
            m(id="R04-N03-P2", titulo="Lo más urgente primero",
              lugar=DEPOSITO, personajes="Bron, Tesla",
              carta="priority_queue | top() es siempre el MAYOR · con std::greater<int> pasa a ser el menor · se usa para «lo más urgente primero»",
              recompensa="xp 10, oro 10",
              escena="""
                  Los pedidos de reparación llegan con una urgencia del 1 al 10, y hay que atender primero el más urgente. Bron armó la cola de prioridad al revés, con `std::greater`, y está atendiendo los que pueden esperar.
              """,
              sugiere="Por defecto, `std::priority_queue<int>` saca siempre el **mayor**. Sacale el comparador.",
              desafio="Atendé primero lo más urgente.",
              inicial='''
                  #include <functional>
                  #include <iostream>
                  #include <queue>
                  #include <vector>

                  int main()
                  {
                      std::priority_queue<int, std::vector<int>, std::greater<int>> urgencias;
                      for (int u : {3, 9, 1, 7, 5}) {
                          urgencias.push(u);
                      }
                      std::cout << "Orden:";
                      while (!urgencias.empty()) {
                          std::cout << " " << urgencias.top();
                          urgencias.pop();
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <functional>
                  #include <iostream>
                  #include <queue>
                  #include <vector>

                  int main()
                  {
                      std::priority_queue<int> urgencias;
                      for (int u : {3, 9, 1, 7, 5}) {
                          urgencias.push(u);
                      }
                      std::cout << "Orden:";
                      while (!urgencias.empty()) {
                          std::cout << " " << urgencias.top();
                          urgencias.pop();
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Nueve, siete, cinco, tres, uno. La caldera de urgencia nueve se arregla a tiempo.",
              imagen=["Un tablero de pedidos con tarjetas numeradas por urgencia; la 9 en rojo arriba.",
                      TESLA + " toma la tarjeta 9.", BRON + " reordena el tablero."]),
            m(id="R04-N03-P3", titulo="La cadena de cajas",
              lugar=DEPOSITO, personajes="Lima, Bron",
              carta="forward_list | cada caja conoce solo la siguiente · insert_after(it, x) mete DESPUÉS de it · before_begin() para el principio",
              recompensa="xp 15, oro 15",
              escena="""
                  En el depósito hay una cadena de cajas donde cada una sabe cuál es la siguiente, y nada más. Lima quiere meter la caja 2 **después** de la 1, y Bron la metió antes que todas.
              """,
              sugiere="`insert_after(f.before_begin(), x)` mete al principio. Para meterla después de la primera caja: `insert_after(f.begin(), x)`.",
              desafio="Meté la caja en su lugar.",
              inicial='''
                  #include <forward_list>
                  #include <iostream>

                  int main()
                  {
                      std::forward_list<int> cajas = {1, 3, 4};
                      cajas.insert_after(cajas.before_begin(), 2);
                      std::cout << "Cadena:";
                      for (int c : cajas) {
                          std::cout << " " << c;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <forward_list>
                  #include <iostream>

                  int main()
                  {
                      std::forward_list<int> cajas = {1, 3, 4};
                      cajas.insert_after(cajas.begin(), 2);
                      std::cout << "Cadena:";
                      for (int c : cajas) {
                          std::cout << " " << c;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Uno, dos, tres, cuatro. Lima dice que es como la lista enlazada que en las Forjas se arma a mano; Bron dice que prefiere esta.",
              imagen=["Una cadena de cajas de madera unidas por eslabones, numeradas del 1 al 4.",
                      LIMA + " engancha la caja 2.", BRON + " sostiene la cadena."]),
        ],
    },
    {
        "titulo": "R04-N04 · Mapas y conjuntos a fondo",
        "misiones": [
            m(id="R04-N04-P1", titulo="Un tema, muchos libros",
              lugar=INDICE, personajes="Bron, Lima",
              carta="multimap | guarda la misma clave varias veces · equal_range(clave) da el rango de TODAS las que tienen esa clave",
              recompensa="xp 10, oro 10",
              escena="""
                  En el índice, el tema «mapas» aparece en varios libros. Bron lo busca con `find` y le da uno solo: el primero.
              """,
              sugiere="`auto [desde, hasta] = indice.equal_range(\"mapas\");` y recorré de `desde` a `hasta`.",
              desafio="Mostrá todos los libros del tema.",
              inicial='''
                  #include <iostream>
                  #include <map>
                  #include <string>

                  int main()
                  {
                      std::multimap<std::string, std::string> indice = {
                          {"mapas", "Atlas de las torres"}, {"vapor", "Calderas"}, {"mapas", "Caminos del canal"}, {"mapas", "La plaza"}};
                      auto it = indice.find("mapas");
                      std::cout << "mapas: " << it->second << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <map>
                  #include <string>

                  int main()
                  {
                      std::multimap<std::string, std::string> indice = {
                          {"mapas", "Atlas de las torres"}, {"vapor", "Calderas"}, {"mapas", "Caminos del canal"}, {"mapas", "La plaza"}};
                      auto [desde, hasta] = indice.equal_range("mapas");
                      for (auto it = desde; it != hasta; ++it) {
                          std::cout << "mapas: " << it->second << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Tres libros de mapas, en el orden en que llegaron al índice. Lima los apila para Lyn, que siempre se pierde.",
              imagen=["Un fichero del índice con tres tarjetas bajo la palabra «mapas».",
                      LIMA + " apila tres libros.", BRON + " revisa las tarjetas."]),
            m(id="R04-N04-P2", titulo="De la L a la P",
              lugar=INDICE, personajes="Lyn, Lima",
              carta="Rangos | lower_bound(x): el primero >= x · upper_bound(x): el primero > x · las palabras que empiezan con P son mayores que \"P\"",
              recompensa="xp 15, oro 15",
              escena="""
                  Lyn busca «todo lo de la L a la P» y, entre los resultados, aparece Lima. Lyn se la quiere llevar de regalo; Lima no se deja. Pero el rango de Bron se olvida de «Poleas»: corta en `upper_bound("P")`, y «Poleas» es mayor que «P».
              """,
              sugiere="Las palabras que empiezan con P son todas menores que «Q». Cortá en `lower_bound(\"Q\")`.",
              desafio="Incluí las palabras que empiezan con P.",
              inicial='''
                  #include <iostream>
                  #include <set>
                  #include <string>

                  int main()
                  {
                      std::set<std::string> nombres = {"Bron", "Lima", "Lyn", "Oto", "Poleas", "Quimera", "Tesla"};
                      auto desde = nombres.lower_bound("L");
                      auto hasta = nombres.upper_bound("P");
                      std::cout << "De la L a la P:";
                      for (auto it = desde; it != hasta; ++it) {
                          std::cout << " " << *it;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <set>
                  #include <string>

                  int main()
                  {
                      std::set<std::string> nombres = {"Bron", "Lima", "Lyn", "Oto", "Poleas", "Quimera", "Tesla"};
                      auto desde = nombres.lower_bound("L");
                      auto hasta = nombres.lower_bound("Q");
                      std::cout << "De la L a la P:";
                      for (auto it = desde; it != hasta; ++it) {
                          std::cout << " " << *it;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Lima, Lyn, Oto y Poleas. Lyn se lleva el libro de las poleas, que es lo único que se deja llevar.",
              imagen=["Un fichero con separadores de letras, de la L a la P resaltados.",
                      LYN + " tira de un libro.", LIMA + " se cruza de brazos."]),
            m(id="R04-N04-P3", titulo="¿Ya estaba?",
              lugar=INDICE, personajes="Bron, Tesla",
              carta="insert devuelve un par | auto [it, nuevo] = s.insert(x); · nuevo es false si ya estaba · sirve para avisar repetidos sin buscar antes",
              recompensa="xp 10, oro 10",
              escena="""
                  Tesla registra visitantes en la Biblioteca y quiere avisar cuando alguien ya había venido. Bron busca antes de insertar, pero la condición está al revés y avisa con los nuevos.
              """,
              sugiere="Usá lo que devuelve `insert`: el segundo elemento del par es `true` si lo agregó (era nuevo) y `false` si ya estaba.",
              desafio="Avisá con los repetidos usando lo que devuelve `insert`.",
              entrada="Lyn Bron Lyn Oto Bron\n",
              inicial='''
                  #include <iostream>
                  #include <set>
                  #include <string>

                  int main()
                  {
                      std::set<std::string> visitas;
                      std::string nombre;
                      while (std::cin >> nombre) {
                          visitas.insert(nombre);
                          std::cout << nombre << ": " << (visitas.contains(nombre) ? "ya habia venido" : "primera vez") << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <set>
                  #include <string>

                  int main()
                  {
                      std::set<std::string> visitas;
                      std::string nombre;
                      while (std::cin >> nombre) {
                          auto [it, nuevo] = visitas.insert(nombre);
                          std::cout << *it << ": " << (nuevo ? "primera vez" : "ya habia venido") << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Lyn y Bron vinieron dos veces. Oto, una sola: dice que los libros no se comen.",
              imagen=["Un libro de visitas con nombres repetidos marcados con una estrella.",
                      TESLA + " firma el libro.", BRON + " pone una estrella."]),
        ],
    },
    {
        "titulo": "R04-N05 · Los algoritmos de la biblioteca",
        "misiones": [
            m(id="R04-N05-P1", titulo="El tipo de accumulate",
              lugar=HERRAMIENTAS, personajes="Bron, Tesla",
              carta="accumulate | std::accumulate(v.begin(), v.end(), 0.0) (#include <numeric>) · el TIPO del valor inicial es el tipo de la suma: con 0 suma enteros",
              recompensa="xp 10, oro 10",
              escena="""
                  Bron estaba escribiendo un bucle de veinte líneas para sumar una columna. Tesla le alcanza una herramienta: `accumulate`. Bron la usa y la suma de los pesos le da **entera**: perdió los decimales.
              """,
              sugiere="El valor inicial decide el tipo de la suma. Con `0` suma `int` (y trunca); con `0.0`, `double`.",
              desafio="Sumá los pesos con decimales.",
              inicial='''
                  #include <iostream>
                  #include <numeric>
                  #include <vector>

                  int main()
                  {
                      std::vector<double> pesos = {1.5, 2.25, 3.5, 0.75};
                      double total = std::accumulate(pesos.begin(), pesos.end(), 0);
                      std::cout << "Peso total: " << total << " kg\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <numeric>
                  #include <vector>

                  int main()
                  {
                      std::vector<double> pesos = {1.5, 2.25, 3.5, 0.75};
                      double total = std::accumulate(pesos.begin(), pesos.end(), 0.0);
                      std::cout << "Peso total: " << total << " kg\\n";
                      return 0;
                  }
              ''',
              al_superar="Ocho kilos justos, no seis. Bron le pregunta a Lima si puede guardar el bucle de recuerdo. Lima ya tiene la lima en la mano.",
              imagen=["Una pared con más de cien herramientas colgadas, una de ellas iluminada.",
                      TESLA + " le alcanza la herramienta.", BRON + " esconde una hoja con un bucle larguísimo."]),
            m(id="R04-N05-P2", titulo="Correr y después borrar",
              lugar=HERRAMIENTAS, personajes="Lima, Bron",
              carta="erase-remove | std::remove_if NO borra: corre adelante los que quedan y devuelve dónde empieza lo que sobra · v.erase(eso, v.end()) borra",
              recompensa="xp 15, oro 15",
              escena="""
                  Lima le pide a Bron que saque de la lista los libros dañados (los que tienen menos de 100 páginas). Bron usa `std::remove_if`… y la lista sigue teniendo el mismo tamaño, con cosas raras al final.
              """,
              sugiere="`remove_if` solo corre lo que se queda hacia adelante. Para borrar el resto: `libros.erase(std::remove_if(...), libros.end());`.",
              desafio="Completá el *erase-remove*.",
              inicial='''
                  #include <algorithm>
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> libros = {120, 40, 300, 95, 210, 15};
                      std::remove_if(libros.begin(), libros.end(), [](int p) { return p < 100; });
                      std::cout << "Quedan " << libros.size() << " libros\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <algorithm>
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> libros = {120, 40, 300, 95, 210, 15};
                      libros.erase(std::remove_if(libros.begin(), libros.end(), [](int p) { return p < 100; }), libros.end());
                      std::cout << "Quedan " << libros.size() << " libros:";
                      for (int p : libros) {
                          std::cout << " " << p;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres libros sanos, y nada raro al final. Lima le cuenta que desde C++20 está `std::erase_if`, que hace las dos cosas; Bron dice que ahora ya sabe por qué.",
              imagen=["Un carrito con tres libros sanos y, al costado, una pila de libros rotos.",
                      LIMA + " revisa la pila.", BRON + " empuja el carrito."]),
            m(id="R04-N05-P3", titulo="Repetidos que no están juntos",
              lugar=HERRAMIENTAS, personajes="Bron, Tesla",
              carta="unique | quita repetidos CONSECUTIVOS · por eso primero se ordena · y como remove, después hace falta el erase",
              recompensa="xp 15, oro 15",
              escena="""
                  La lista de temas pedidos tiene repetidos. Bron usa `unique` y siguen apareciendo: los repetidos no estaban uno al lado del otro.
              """,
              sugiere="Ordená primero con `std::sort`, así los repetidos quedan juntos, y después `erase` + `unique`.",
              desafio="Ordená antes de quitar repetidos.",
              inicial='''
                  #include <algorithm>
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::string> temas = {"vapor", "mapas", "vapor", "relojes", "mapas", "vapor"};
                      temas.erase(std::unique(temas.begin(), temas.end()), temas.end());
                      std::cout << "Temas:";
                      for (const auto& t : temas) {
                          std::cout << " " << t;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <algorithm>
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::string> temas = {"vapor", "mapas", "vapor", "relojes", "mapas", "vapor"};
                      std::sort(temas.begin(), temas.end());
                      temas.erase(std::unique(temas.begin(), temas.end()), temas.end());
                      std::cout << "Temas:";
                      for (const auto& t : temas) {
                          std::cout << " " << t;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Mapas, relojes, vapor: tres temas, en orden. Tesla dice que así se arma un índice.",
              imagen=["Un pizarrón con una lista de temas tachados y tres que quedan.",
                      TESLA + " escribe «índice».", BRON + " tacha repetidos."]),
        ],
    },
    {
        "titulo": "R04-N06 · Functores y std::function",
        "misiones": [
            m(id="R04-N06-P1", titulo="El contador que se queda",
              lugar=CONTROL, personajes="Bron, Lima",
              carta="Functor | un objeto con operator() que guarda estado · for_each trabaja con una COPIA y la devuelve: usá lo que devuelve",
              recompensa="xp 15, oro 15",
              escena="""
                  Bron escribió un functor que cuenta cuántas palancas están arriba. Se lo pasa a `for_each` y después mira su contador: cero. Lima le explica que `for_each` contó con una copia, y la devolvió.
              """,
              sugiere="Guardá lo que devuelve `for_each`: `Contador resultado = std::for_each(..., Contador{});` y mostrá `resultado.arriba`.",
              desafio="Usá el functor que devuelve `for_each`.",
              inicial='''
                  #include <algorithm>
                  #include <iostream>
                  #include <vector>

                  struct Contador {
                      int arriba = 0;
                      void operator()(bool palanca) { if (palanca) arriba++; }
                  };

                  int main()
                  {
                      std::vector<bool> palancas = {true, false, true, true, false};
                      Contador c;
                      std::for_each(palancas.begin(), palancas.end(), c);
                      std::cout << "Palancas arriba: " << c.arriba << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <algorithm>
                  #include <iostream>
                  #include <vector>

                  struct Contador {
                      int arriba = 0;
                      void operator()(bool palanca) { if (palanca) arriba++; }
                  };

                  int main()
                  {
                      std::vector<bool> palancas = {true, false, true, true, false};
                      Contador c = std::for_each(palancas.begin(), palancas.end(), Contador{});
                      std::cout << "Palancas arriba: " << c.arriba << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres palancas arriba. Lima anota que el contador de verdad es el que vuelve.",
              imagen=["Un tablero con cinco palancas, tres arriba.",
                      LIMA + " señala un contador de bronce.", BRON + " baja una palanca."]),
            m(id="R04-N06-P2", titulo="Las tarjetas de las palancas",
              lugar=CONTROL, personajes="Bron, Oto",
              carta="std::function | std::map<std::string, std::function<void()>> guarda acciones con nombre · comandos[\"campana\"]() la ejecuta",
              recompensa="xp 10, oro 10",
              escena="""
                  Cada palanca del tablero tiene una tarjeta con su acción. Bron cambió la tarjeta de la campana por «servir el guiso»… pero se olvidó de colgarla en la tabla, y la palanca dice «orden desconocida».
              """,
              sugiere="Agregá la entrada `\"campana\"` a la tabla, con una lambda que muestre `Oto sirve el guiso`.",
              desafio="Colgá la tarjeta que falta.",
              entrada="caldera campana compuerta\n",
              inicial='''
                  #include <functional>
                  #include <iostream>
                  #include <map>
                  #include <string>

                  int main()
                  {
                      std::map<std::string, std::function<void()>> palancas = {
                          {"caldera", [] { std::cout << "se enciende la caldera\\n"; }},
                          {"compuerta", [] { std::cout << "se abre la compuerta\\n"; }},
                      };
                      std::string orden;
                      while (std::cin >> orden) {
                          if (palancas.contains(orden)) {
                              palancas[orden]();
                          } else {
                              std::cout << "orden desconocida: " << orden << "\\n";
                          }
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <functional>
                  #include <iostream>
                  #include <map>
                  #include <string>

                  int main()
                  {
                      std::map<std::string, std::function<void()>> palancas = {
                          {"caldera", [] { std::cout << "se enciende la caldera\\n"; }},
                          {"campana", [] { std::cout << "Oto sirve el guiso\\n"; }},
                          {"compuerta", [] { std::cout << "se abre la compuerta\\n"; }},
                      };
                      std::string orden;
                      while (std::cin >> orden) {
                          if (palancas.contains(orden)) {
                              palancas[orden]();
                          } else {
                              std::cout << "orden desconocida: " << orden << "\\n";
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="Desde ese día, a las doce suena la palanca y Oto sirve el guiso. Nadie se quejó.",
              imagen=["Un tablero de palancas con tarjetas colgadas; una dice «servir el guiso».",
                      OTO + " sirve guiso a la hora exacta.", BRON + " baja la palanca."]),
            m(id="R04-N06-P3", titulo="Todas las reglas",
              lugar=CONTROL, personajes="Bron, Tesla",
              carta="Lista de reglas | std::vector<std::function<bool(int)>> · una presión vale si cumple TODAS: std::all_of sobre las reglas",
              recompensa="xp 15, oro 15",
              escena="""
                  La presión de la caldera tiene tres reglas: ser positiva, no pasar de 100 y ser par (la caldera es rara). La validación de Bron acepta la presión si cumple **alguna**.
              """,
              sugiere="Cambiá `std::any_of` por `std::all_of`: tiene que cumplir todas.",
              desafio="Exigí todas las reglas.",
              inicial='''
                  #include <algorithm>
                  #include <functional>
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::function<bool(int)>> reglas = {
                          [](int p) { return p > 0; },
                          [](int p) { return p <= 100; },
                          [](int p) { return p % 2 == 0; },
                      };
                      for (int presion : {40, 130, 33, -2}) {
                          bool ok = std::any_of(reglas.begin(), reglas.end(), [presion](const auto& r) { return r(presion); });
                          std::cout << presion << ": " << (ok ? "aceptada" : "rechazada") << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <algorithm>
                  #include <functional>
                  #include <iostream>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::function<bool(int)>> reglas = {
                          [](int p) { return p > 0; },
                          [](int p) { return p <= 100; },
                          [](int p) { return p % 2 == 0; },
                      };
                      for (int presion : {40, 130, 33, -2}) {
                          bool ok = std::all_of(reglas.begin(), reglas.end(), [presion](const auto& r) { return r(presion); });
                          std::cout << presion << ": " << (ok ? "aceptada" : "rechazada") << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Solo el 40 pasa las tres reglas. Tesla agrega una cuarta regla en el pizarrón, sin tocar el código: la lista crece sola.",
              imagen=["Un pizarrón con tres reglas escritas y una cuarta a medio escribir.",
                      TESLA + " escribe la cuarta regla.", BRON + " revisa la caldera."]),
        ],
    },
    {
        "titulo": "R04-N07 · Vistas y ranges",
        "misiones": [
            m(id="R04-N07-P1", titulo="Primero filtrar, después mirar",
              lugar=LECTURA, personajes="Bron, Lima",
              carta="Views | v | std::views::filter(cond) | std::views::transform(f) · se aplican EN ORDEN, sin copiar nada · el orden cambia el resultado",
              recompensa="xp 15, oro 15",
              escena="""
                  En la sala de lectura se encadenan lentes: uno que deja ver solo los capítulos pares, otro que duplica el número de página. Bron los puso al revés: primero duplica y después filtra, y todos los números le quedan pares.
              """,
              sugiere="Poné primero el `filter` (quedarse con los pares) y después el `transform` (duplicar).",
              desafio="Ordená los lentes.",
              inicial='''
                  #include <iostream>
                  #include <ranges>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> capitulos = {1, 2, 3, 4, 5, 6};
                      auto lente = capitulos | std::views::transform([](int c) { return c * 2; })
                                             | std::views::filter([](int c) { return c % 2 == 0; });
                      std::cout << "Paginas:";
                      for (int p : lente) {
                          std::cout << " " << p;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <ranges>
                  #include <vector>

                  int main()
                  {
                      std::vector<int> capitulos = {1, 2, 3, 4, 5, 6};
                      auto lente = capitulos | std::views::filter([](int c) { return c % 2 == 0; })
                                             | std::views::transform([](int c) { return c * 2; });
                      std::cout << "Paginas:";
                      for (int p : lente) {
                          std::cout << " " << p;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Cuatro, ocho, doce: solo los pares, duplicados. Lima dice que es exactamente lo que tenía que ver.",
              imagen=["Tres lentes de bronce encadenados frente a un libro abierto.",
                      BRON + " mira a través de los lentes.", LIMA + " cambia el orden de dos lentes."]),
            m(id="R04-N07-P2", titulo="Los tres mejores",
              lugar=LECTURA, personajes="Lyn, Bron",
              carta="ranges::sort con proyección | std::ranges::sort(v, std::greater{}, &Marca::puntos) ordena por ese campo · std::views::take(3) mira los tres primeros",
              recompensa="xp 15, oro 15",
              escena="""
                  Lyn quiere el podio de la carrera: los tres con más puntos. Bron ordena por puntos, pero de menor a mayor, y en el podio quedan los últimos.
              """,
              sugiere="Pasale `std::greater{}` como comparador a `std::ranges::sort`, antes de la proyección `&Marca::puntos`.",
              desafio="Ordená de mayor a menor.",
              inicial='''
                  #include <algorithm>
                  #include <functional>
                  #include <iostream>
                  #include <ranges>
                  #include <string>
                  #include <vector>

                  struct Marca {
                      std::string nombre;
                      int puntos;
                  };

                  int main()
                  {
                      std::vector<Marca> tabla = {{"Bron", 120}, {"Lyn", 340}, {"Lima", 210}, {"Oto", 95}, {"Tesla", 300}};
                      std::ranges::sort(tabla, std::less{}, &Marca::puntos);
                      for (const Marca& m : tabla | std::views::take(3)) {
                          std::cout << m.nombre << " " << m.puntos << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <algorithm>
                  #include <functional>
                  #include <iostream>
                  #include <ranges>
                  #include <string>
                  #include <vector>

                  struct Marca {
                      std::string nombre;
                      int puntos;
                  };

                  int main()
                  {
                      std::vector<Marca> tabla = {{"Bron", 120}, {"Lyn", 340}, {"Lima", 210}, {"Oto", 95}, {"Tesla", 300}};
                      std::ranges::sort(tabla, std::greater{}, &Marca::puntos);
                      for (const Marca& m : tabla | std::views::take(3)) {
                          std::cout << m.nombre << " " << m.puntos << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Lyn, Tesla y Lima en el podio. Tesla dice que corrió en contra de su voluntad.",
              imagen=["Un podio de tres escalones de bronce.",
                      LYN + " en el escalón más alto.", BRON + " aplaude desde abajo."]),
            m(id="R04-N07-P3", titulo="La cuenta regresiva",
              lugar=LECTURA, personajes="Bron, Tesla",
              carta="iota | std::views::iota(1, 6) da 1, 2, 3, 4, 5 (el 6 no entra) · | std::views::reverse los da vuelta",
              recompensa="xp 10, oro 10",
              escena="""
                  Para cerrar la sala de lectura, la campana da una cuenta regresiva del 5 al 1. La de Bron arranca en 4: `iota(1, 5)` no incluye el 5.
              """,
              sugiere="`iota(desde, hasta)` no incluye `hasta`. Para llegar al 5, el tope es 6.",
              desafio="Hacé que la cuenta arranque en 5.",
              inicial='''
                  #include <iostream>
                  #include <ranges>

                  int main()
                  {
                      std::cout << "Cierre:";
                      for (int n : std::views::iota(1, 5) | std::views::reverse) {
                          std::cout << " " << n;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <ranges>

                  int main()
                  {
                      std::cout << "Cierre:";
                      for (int n : std::views::iota(1, 6) | std::views::reverse) {
                          std::cout << " " << n;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Cinco, cuatro, tres, dos, uno: la sala se cierra a tiempo. Lyn llega corriendo al «uno», como siempre.",
              imagen=["Una campana sobre la puerta de la sala de lectura y un cartel con números del 5 al 1.",
                      TESLA + " tira de la cuerda de la campana.", BRON + " cierra la puerta."]),
        ],
    },
    {
        "titulo": "R04-N08 · Un contenedor propio",
        "misiones": [
            m(id="R04-N08-P1", titulo="El estante que se deja recorrer",
              lugar=TALLER, personajes="Bron, Lima",
              carta="begin y end | un contenedor propio con begin() y end() funciona con el for de rango y con los algoritmos · se pueden prestar los iteradores del vector de adentro",
              recompensa="xp 10, oro 10",
              escena="""
                  Bron hizo una clase `Estante` y quiere recorrerla con un `for` de rango. El Taller no lo deja: el estante tiene `begin()`, pero le falta `end()`.
              """,
              sugiere="Agregá `auto end() const { return libros_.end(); }`, como el `begin()` que ya está.",
              desafio="Completá lo que necesita el `for` de rango.",
              inicial='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  class Estante {
                  public:
                      void poner(const std::string& libro) { libros_.push_back(libro); }
                      auto begin() const { return libros_.begin(); }

                  private:
                      std::vector<std::string> libros_;
                  };

                  int main()
                  {
                      Estante e;
                      e.poner("Poleas");
                      e.poner("Vapor");
                      for (const auto& libro : e) {
                          std::cout << libro << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  class Estante {
                  public:
                      void poner(const std::string& libro) { libros_.push_back(libro); }
                      auto begin() const { return libros_.begin(); }
                      auto end() const { return libros_.end(); }

                  private:
                      std::vector<std::string> libros_;
                  };

                  int main()
                  {
                      Estante e;
                      e.poner("Poleas");
                      e.poner("Vapor");
                      for (const auto& libro : e) {
                          std::cout << libro << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="El estante se deja recorrer, y de yapa funciona con todos los algoritmos de la Biblioteca. Gratis.",
              imagen=["Un estante de madera con dos libros y un dedo de bronce apoyado en el primero.",
                      BRON + " acomoda los libros.", LIMA + " prueba el dedo de bronce."]),
            m(id="R04-N08-P2", titulo="Las últimas lecturas",
              lugar=TALLER, personajes="Lima, Bron",
              carta="Plantilla con número | template <std::size_t N> class Ultimas · guarda solo las últimas N (con deque: push_back y, si sobra, pop_front)",
              recompensa="xp 15, oro 15",
              escena="""
                  Lima fabricó un estante raro: cuando llega una lectura nueva y no hay lugar, la más vieja se cae. Así guarda siempre las últimas N lecturas de la caldera. El de Bron nunca tira nada.
              """,
              sugiere="Después de agregar, si el `deque` tiene más de `N`, sacá la más vieja con `pop_front()`.",
              desafio="Hacé que el estante guarde solo las últimas `N`.",
              inicial='''
                  #include <deque>
                  #include <iostream>

                  template <std::size_t N>
                  class Ultimas {
                  public:
                      void agregar(int x)
                      {
                          datos_.push_back(x);
                      }
                      auto begin() const { return datos_.begin(); }
                      auto end() const { return datos_.end(); }

                  private:
                      std::deque<int> datos_;
                  };

                  int main()
                  {
                      Ultimas<3> caldera;
                      for (int lectura : {80, 85, 90, 95, 70}) {
                          caldera.agregar(lectura);
                      }
                      std::cout << "Ultimas lecturas:";
                      for (int x : caldera) {
                          std::cout << " " << x;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <deque>
                  #include <iostream>

                  template <std::size_t N>
                  class Ultimas {
                  public:
                      void agregar(int x)
                      {
                          datos_.push_back(x);
                          if (datos_.size() > N) {
                              datos_.pop_front();
                          }
                      }
                      auto begin() const { return datos_.begin(); }
                      auto end() const { return datos_.end(); }

                  private:
                      std::deque<int> datos_;
                  };

                  int main()
                  {
                      Ultimas<3> caldera;
                      for (int lectura : {80, 85, 90, 95, 70}) {
                          caldera.agregar(lectura);
                      }
                      std::cout << "Ultimas lecturas:";
                      for (int x : caldera) {
                          std::cout << " " << x;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Noventa, noventa y cinco, setenta: las tres últimas. Bron le pregunta para qué sirve un estante que tira libros, y se contesta solo antes de que Lima abra la boca.",
              imagen=["Un estante circular de bronce con tres lugares y un libro cayéndose por el borde.",
                      LIMA + " ajusta el estante.", BRON + " ataja el libro que cae."]),
            m(id="R04-N08-P3", titulo="El dedo de bronce propio",
              lugar=TALLER, personajes="Bron, Tesla",
              carta="Iterador mínimo | operator* da el valor · operator++ avanza · operator!= compara con el final · con eso anda el for de rango",
              recompensa="xp 15, oro 15",
              escena="""
                  Tesla le pide a Bron un contenedor que no guarda nada: cuenta del 1 al N. Para eso hace falta un dedo de bronce propio. El de Bron avanza, pero cuando le preguntan dónde está, contesta siempre 0.
              """,
              sugiere="`operator*` tiene que devolver el número actual del iterador, `actual_`.",
              desafio="Hacé que el iterador diga su valor.",
              inicial='''
                  #include <iostream>

                  class Cuenta {
                  public:
                      explicit Cuenta(int n) : n_(n) {}

                      struct Iter {
                          int actual_;
                          int operator*() const { return 0; }
                          Iter& operator++() { ++actual_; return *this; }
                          bool operator!=(const Iter& otro) const { return actual_ != otro.actual_; }
                      };

                      Iter begin() const { return Iter{1}; }
                      Iter end() const { return Iter{n_ + 1}; }

                  private:
                      int n_;
                  };

                  int main()
                  {
                      std::cout << "Cuenta:";
                      for (int x : Cuenta(5)) {
                          std::cout << " " << x;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  class Cuenta {
                  public:
                      explicit Cuenta(int n) : n_(n) {}

                      struct Iter {
                          int actual_;
                          int operator*() const { return actual_; }
                          Iter& operator++() { ++actual_; return *this; }
                          bool operator!=(const Iter& otro) const { return actual_ != otro.actual_; }
                      };

                      Iter begin() const { return Iter{1}; }
                      Iter end() const { return Iter{n_ + 1}; }

                  private:
                      int n_;
                  };

                  int main()
                  {
                      std::cout << "Cuenta:";
                      for (int x : Cuenta(5)) {
                          std::cout << " " << x;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Uno, dos, tres, cuatro, cinco, sin guardar ni un número. Tesla dice que eso es lo que hace `views::iota` por dentro.",
              imagen=["Un dedo de bronce hecho a mano, con un engranaje chiquito en la punta que cuenta.",
                      TESLA + " lo prueba.", BRON + " le da cuerda."]),
        ],
    },
    {
        "titulo": "R04-N09 · Jefe: el Kraken de los Contenedores",
        "misiones": [
            m(id="R04-N09-P1", titulo="El tentáculo más fuerte",
              lugar=SOTANOS, personajes="Bron, Lima",
              criatura="dragon",
              carta="priority_queue de pares | std::priority_queue<std::pair<int, std::string>> ordena por el primero (la fuerza) · top() es el más fuerte",
              recompensa="xp 15, oro 15",
              escena="""
                  En los sótanos inundados vive el **Kraken de los Contenedores**, que saca un tentáculo por cada pasillo. Lima no sabe nadar y se queda en la escalera, dando indicaciones. Bron tiene que atacar primero el tentáculo más fuerte, pero su cola los guarda por nombre.
              """,
              sugiere="Poné la fuerza **primero** en el par: `{fuerza, nombre}`. La cola de prioridad compara por el primero.",
              desafio="Ordená los tentáculos por fuerza.",
              entrada="norte 30\nsur 75\neste 50\noeste 10\n",
              inicial='''
                  #include <iostream>
                  #include <queue>
                  #include <string>
                  #include <utility>

                  int main()
                  {
                      std::priority_queue<std::pair<std::string, int>> tentaculos;
                      std::string pasillo;
                      int fuerza = 0;
                      while (std::cin >> pasillo >> fuerza) {
                          tentaculos.push({pasillo, fuerza});
                      }
                      while (!tentaculos.empty()) {
                          auto [p, f] = tentaculos.top();
                          std::cout << "Tentaculo del " << p << " (fuerza " << f << ")\\n";
                          tentaculos.pop();
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <queue>
                  #include <string>
                  #include <utility>

                  int main()
                  {
                      std::priority_queue<std::pair<int, std::string>> tentaculos;
                      std::string pasillo;
                      int fuerza = 0;
                      while (std::cin >> pasillo >> fuerza) {
                          tentaculos.push({fuerza, pasillo});
                      }
                      while (!tentaculos.empty()) {
                          auto [f, p] = tentaculos.top();
                          std::cout << "Tentaculo del " << p << " (fuerza " << f << ")\\n";
                          tentaculos.pop();
                      }
                      return 0;
                  }
              ''',
              al_superar="Sur, este, norte, oeste: Bron los suelta en ese orden y el Kraken retrocede hacia el fondo.",
              imagen=["Un sótano inundado con estanterías medio hundidas y " + KRAKEN + ".",
                      BRON + " con el agua hasta el pecho, sosteniendo su llave.", LIMA + " en la escalera, con la lima en alto."]),
            m(id="R04-N09-P2", titulo="Cada libro a su estante",
              lugar=SOTANOS, personajes="Bron, Tesla",
              criatura="dragon",
              carta="map de vectores | std::map<std::string, std::vector<std::string>> · estantes[tema].push_back(libro) agrupa por tema",
              recompensa="xp 15, oro 15",
              escena="""
                  El Kraken desordenó todo: los libros flotan mezclados. Para que no tenga dónde esconderse, cada libro tiene que volver al estante de su tema. Bron los pone todos en el mismo estante.
              """,
              sugiere="Agrupalos con `estantes[tema].push_back(titulo);` y después recorré el mapa.",
              desafio="Agrupá los libros por tema.",
              entrada="mapas Atlas\nvapor Calderas\nmapas Caminos\nrelojes Pendulos\nvapor Valvulas\n",
              inicial='''
                  #include <iostream>
                  #include <map>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::map<std::string, std::vector<std::string>> estantes;
                      std::string tema, titulo;
                      while (std::cin >> tema >> titulo) {
                          estantes["todo"].push_back(titulo);
                      }
                      for (const auto& [t, libros] : estantes) {
                          std::cout << t << ":";
                          for (const auto& l : libros) {
                              std::cout << " " << l;
                          }
                          std::cout << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <map>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::map<std::string, std::vector<std::string>> estantes;
                      std::string tema, titulo;
                      while (std::cin >> tema >> titulo) {
                          estantes[tema].push_back(titulo);
                      }
                      for (const auto& [t, libros] : estantes) {
                          std::cout << t << ":";
                          for (const auto& l : libros) {
                              std::cout << " " << l;
                          }
                          std::cout << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Mapas, relojes y vapor, cada uno en su estante. El Kraken busca un hueco donde meterse y no encuentra ninguno.",
              imagen=["Estanterías ordenadas que emergen del agua, cada una con un cartel de tema.",
                      BRON + " pone un libro en su estante.", TESLA + " lee los carteles desde una pasarela."]),
            m(id="R04-N09-P3", titulo="Avisar sin mirar",
              lugar=SOTANOS, personajes="Lima, Bron",
              criatura="dragon",
              carta="Eventos | std::vector<std::function<void(const std::string&)>> oyentes · al pasar algo se llama a todos · nadie tiene que estar mirando",
              recompensa="xp 15, oro 15",
              escena="""
                  Cuando el Kraken saca un tentáculo, todos tienen que enterarse: Lima desde la escalera, Bron desde el agua. Bron armó la lista de oyentes, pero cuando suena la alarma no le avisa a nadie.
              """,
              sugiere="En `avisar`, recorré `oyentes_` y llamá a cada uno con el pasillo: `o(pasillo);`.",
              desafio="Hacé que la alarma avise a todos los oyentes.",
              inicial='''
                  #include <functional>
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  class Alarma {
                  public:
                      void escuchar(std::function<void(const std::string&)> f) { oyentes_.push_back(f); }
                      void avisar(const std::string& pasillo)
                      {
                          std::cout << "ALARMA en el pasillo " << pasillo << "\\n";
                      }

                  private:
                      std::vector<std::function<void(const std::string&)>> oyentes_;
                  };

                  int main()
                  {
                      Alarma alarma;
                      alarma.escuchar([](const std::string& p) { std::cout << "  Lima grita: cuidado en el " << p << "!\\n"; });
                      alarma.escuchar([](const std::string& p) { std::cout << "  Bron nada hacia el " << p << "\\n"; });
                      alarma.avisar("norte");
                      alarma.avisar("sur");
                      return 0;
                  }
              ''',
              solucion='''
                  #include <functional>
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  class Alarma {
                  public:
                      void escuchar(std::function<void(const std::string&)> f) { oyentes_.push_back(f); }
                      void avisar(const std::string& pasillo)
                      {
                          std::cout << "ALARMA en el pasillo " << pasillo << "\\n";
                          for (const auto& o : oyentes_) {
                              o(pasillo);
                          }
                      }

                  private:
                      std::vector<std::function<void(const std::string&)>> oyentes_;
                  };

                  int main()
                  {
                      Alarma alarma;
                      alarma.escuchar([](const std::string& p) { std::cout << "  Lima grita: cuidado en el " << p << "!\\n"; });
                      alarma.escuchar([](const std::string& p) { std::cout << "  Bron nada hacia el " << p << "\\n"; });
                      alarma.avisar("norte");
                      alarma.avisar("sur");
                      return 0;
                  }
              ''',
              al_superar="Cada vez que asoma un tentáculo, Lima grita y Bron ya está nadando hacia ahí. El Kraken no sorprende a nadie.",
              imagen=["Una campana de alarma colgada sobre el agua del sótano, sonando.",
                      LIMA + " grita desde la escalera.", BRON + " nada hacia un tentáculo."]),
            m(id="R04-N09-P4", titulo="El catálogo de plantillas",
              lugar=SOTANOS, personajes="Bron, Tesla, Lima",
              criatura="dragon",
              carta="Plantilla + optional | template <typename C> std::optional<...> buscar(const C& cont, ...) sirve para cualquier contenedor",
              recompensa="xp 25, oro 30",
              item="Catálogo de Plantillas",
              escena="""
                  El último tentáculo del Kraken suelta su estante, y cae al agua un libro de tapas de bronce: un **catálogo**. Para encontrar en él la página de las bisagras del Vidriero, Bron escribió un buscador que solo sirve para vectores, y el catálogo es una lista.
              """,
              sugiere="Hacé `buscar` plantilla: `template <typename Contenedor>` y recibí `const Contenedor& c`. El resto del código ya funciona con cualquier contenedor que se pueda recorrer.",
              desafio="Convertí el buscador en una plantilla.",
              inicial='''
                  #include <iostream>
                  #include <list>
                  #include <optional>
                  #include <string>
                  #include <vector>

                  std::optional<int> buscar(const std::vector<std::string>& c, const std::string& buscado)
                  {
                      int pagina = 1;
                      for (const auto& x : c) {
                          if (x == buscado) {
                              return pagina;
                          }
                          pagina++;
                      }
                      return std::nullopt;
                  }

                  int main()
                  {
                      std::vector<std::string> estante = {"poleas", "bisagras"};
                      std::list<std::string> catalogo = {"engranajes", "resortes", "valvulas", "bisagras"};
                      for (const auto& r : {buscar(estante, "bisagras"), buscar(catalogo, "bisagras")}) {
                          if (r) {
                              std::cout << "Bisagras en la pagina " << *r << "\\n";
                          } else {
                              std::cout << "No hay bisagras\\n";
                          }
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <list>
                  #include <optional>
                  #include <string>
                  #include <vector>

                  template <typename Contenedor>
                  std::optional<int> buscar(const Contenedor& c, const std::string& buscado)
                  {
                      int pagina = 1;
                      for (const auto& x : c) {
                          if (x == buscado) {
                              return pagina;
                          }
                          pagina++;
                      }
                      return std::nullopt;
                  }

                  int main()
                  {
                      std::vector<std::string> estante = {"poleas", "bisagras"};
                      std::list<std::string> catalogo = {"engranajes", "resortes", "valvulas", "bisagras"};
                      for (const auto& r : {buscar(estante, "bisagras"), buscar(catalogo, "bisagras")}) {
                          if (r) {
                              std::cout << "Bisagras en la pagina " << *r << "\\n";
                          } else {
                              std::cout << "No hay bisagras\\n";
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="Página 4 del **Catálogo de Plantillas**: las bisagras del Vidriero, catalogadas como **plantilla**, «para cualquier marco». Tesla las mira un largo rato. Lima, desde la escalera, pregunta si ya puede bajar.",
              imagen=["Un libro de tapas de bronce abierto sobre el agua, en la página de dos bisagras.",
                      BRON + " sostiene el libro con cuidado.", TESLA + " mira la página; " + LIMA + " espera en la escalera."]),
        ],
    },
]
