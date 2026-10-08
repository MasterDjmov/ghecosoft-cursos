from gencpp import m
from cpp_r01 import BRON, TESLA, LIMA, LYN, OTO, GHECO

PLANOS = "La Sala de los Planos"
ENSAMBLAJE = "La línea de ensamblaje de autómatas"
CALDERA = "La sala de la caldera principal"
CARTOGRAFO = "La mesa del cartógrafo"
RELOJ = "El Gran Reloj de la plaza"
ARCHIVO = "El archivo de planos"
PATIO = "El patio de los autómatas"
ARENA = "La Arena bajo la Ciudadela"
QUIMERA = "la Quimera de la Arena (cabeza de león, cuerpo de cabra y cola de serpiente, hecha de piezas de bronce y cobre que se reacomodan con juntas cian)"

NODOS = [
    {
        "titulo": "R02-N01 · Structs y clases",
        "misiones": [
            m(id="R02-N01-P1", titulo="Un plano, tres torres",
              lugar=PLANOS, personajes="Bron, Tesla",
              carta="struct | struct Torre { std::string nombre; int pisos = 0; }; · t.pisos lee un campo · un vector de structs guarda muchas",
              recompensa="xp 10, oro 10",
              escena="""
                  —¿Y esto para qué me sirve? —pregunta Bron frente a miles de planos colgados. Tesla lo lleva a la ventana: tres torres, hechas con el mismo plano. Le pide que sume los pisos de las tres, y Bron cuenta las torres.
              """,
              sugiere="Cada torre del vector tiene su campo `pisos`. En el recorrido, sumá `t.pisos` en lugar de contar torres.",
              desafio="Sumá los pisos de todas las torres.",
              inicial='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  struct Torre {
                      std::string nombre;
                      int pisos = 0;
                  };

                  int main()
                  {
                      std::vector<Torre> torres = {{"Reloj", 12}, {"Poleas", 8}, {"Vitrales", 15}};
                      int total = 0;
                      for (const Torre& t : torres) {
                          std::cout << t.nombre << ": " << t.pisos << " pisos\\n";
                          total += 1;
                      }
                      std::cout << "Pisos en total: " << total << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  struct Torre {
                      std::string nombre;
                      int pisos = 0;
                  };

                  int main()
                  {
                      std::vector<Torre> torres = {{"Reloj", 12}, {"Poleas", 8}, {"Vitrales", 15}};
                      int total = 0;
                      for (const Torre& t : torres) {
                          std::cout << t.nombre << ": " << t.pisos << " pisos\\n";
                          total += t.pisos;
                      }
                      std::cout << "Pisos en total: " << total << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Treinta y cinco pisos de un solo plano. Bron se queda un rato largo mirando por la ventana.",
              imagen=["Una ventana alta de la Sala de los Planos con tres torres distintas afuera.",
                      TESLA + " señala las torres con el compás.", BRON + " mira con la boca abierta."]),
            m(id="R02-N01-P2", titulo="Lo que sabe hacer un plano",
              lugar=PLANOS, personajes="Bron, Lima",
              carta="Método | int altura() const { return pisos * 3; } · va DENTRO del struct · se llama t.altura() · const: no cambia el objeto",
              recompensa="xp 10, oro 10",
              escena="""
                  Un plano no solo dice qué datos tiene una torre: también qué sabe hacer. Lima le agregó a la torre un método que calcula su altura (tres metros por piso), pero lo dejó sin terminar.
              """,
              sugiere="Adentro del método se usan los campos del objeto directamente: `return pisos * 3;`.",
              desafio="Completá el método `altura`.",
              inicial='''
                  #include <iostream>
                  #include <string>

                  struct Torre {
                      std::string nombre;
                      int pisos = 0;

                      int altura() const
                      {
                          return 0;
                      }
                  };

                  int main()
                  {
                      Torre reloj{"Reloj", 12};
                      Torre vitrales{"Vitrales", 15};
                      std::cout << reloj.nombre << ": " << reloj.altura() << " metros\\n";
                      std::cout << vitrales.nombre << ": " << vitrales.altura() << " metros\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  struct Torre {
                      std::string nombre;
                      int pisos = 0;

                      int altura() const
                      {
                          return pisos * 3;
                      }
                  };

                  int main()
                  {
                      Torre reloj{"Reloj", 12};
                      Torre vitrales{"Vitrales", 15};
                      std::cout << reloj.nombre << ": " << reloj.altura() << " metros\\n";
                      std::cout << vitrales.nombre << ": " << vitrales.altura() << " metros\\n";
                      return 0;
                  }
              ''',
              al_superar="Treinta y seis y cuarenta y cinco metros. Lima lo anota y Bron pregunta si puede subir a la de los vitrales.",
              imagen=["Un plano de torre con la altura anotada al costado.",
                      LIMA + " mide el plano con un calibre.", BRON + " mira hacia arriba."]),
            m(id="R02-N01-P3", titulo="El reloj que no se toca",
              lugar=PLANOS, personajes="Bron, Tesla",
              carta="class | los datos van private · afuera solo se usan los métodos public · el compilador impide tocar lo privado",
              recompensa="xp 15, oro 15",
              escena="""
                  El reloj de la sala marca las 23. Bron quiere adelantarlo dos horas y escribe `r.hora_ = 25`. El Taller no lo deja: la hora es **privada**. Y está bien, porque las 25 no existen.
              """,
              sugiere="Desde afuera solo se puede usar lo `public`. El reloj tiene `avanzar(horas)`, que da la vuelta a las 24 con `%`.",
              desafio="Adelantá el reloj con el método, no tocando el dato.",
              inicial='''
                  #include <iostream>

                  class Reloj {
                  public:
                      void avanzar(int horas) { hora_ = (hora_ + horas) % 24; }
                      int hora() const { return hora_; }

                  private:
                      int hora_ = 23;
                  };

                  int main()
                  {
                      Reloj r;
                      r.hora_ = 25;
                      std::cout << "Hora: " << r.hora() << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  class Reloj {
                  public:
                      void avanzar(int horas) { hora_ = (hora_ + horas) % 24; }
                      int hora() const { return hora_; }

                  private:
                      int hora_ = 23;
                  };

                  int main()
                  {
                      Reloj r;
                      r.avanzar(2);
                      std::cout << "Hora: " << r.hora() << "\\n";
                      return 0;
                  }
              ''',
              al_superar="La una de la mañana, como corresponde. Tesla asiente: el reloj se cuida solo.",
              imagen=["Un reloj de pared de bronce que marca la una, con la tapa cerrada con candado.",
                      BRON + " sostiene una llave que no entra en el candado.", TESLA + " sonríe."]),
        ],
    },
    {
        "titulo": "R02-N02 · Constructores y destructores",
        "misiones": [
            m(id="R02-N02-P1", titulo="Nacer completo",
              lugar=ENSAMBLAJE, personajes="Bron, Tesla",
              carta="Constructor | Automata(std::string n, int b) : nombre_(n), bateria_(b) {} · la lista de inicialización llena cada dato al nacer",
              recompensa="xp 10, oro 10",
              escena="""
                  En la línea de ensamblaje cada autómata sale con su nombre y la batería cargada. El que armó Bron sale sin nombre y con la batería en cero: el constructor recibe los datos y no los guarda.
              """,
              sugiere="Usá la lista de inicialización: después de los parámetros, `: nombre_(n), bateria_(b)`.",
              desafio="Hacé que el constructor guarde lo que recibe.",
              inicial='''
                  #include <iostream>
                  #include <string>

                  class Automata {
                  public:
                      Automata(std::string n, int b) {}
                      void mostrar() const { std::cout << "[" << nombre_ << "] bateria " << bateria_ << "%\\n"; }

                  private:
                      std::string nombre_;
                      int bateria_ = 0;
                  };

                  int main()
                  {
                      Automata a("Cucu", 80);
                      a.mostrar();
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  class Automata {
                  public:
                      Automata(std::string n, int b) : nombre_(n), bateria_(b) {}
                      void mostrar() const { std::cout << "[" << nombre_ << "] bateria " << bateria_ << "%\\n"; }

                  private:
                      std::string nombre_;
                      int bateria_ = 0;
                  };

                  int main()
                  {
                      Automata a("Cucu", 80);
                      a.mostrar();
                      return 0;
                  }
              ''',
              al_superar="Cucú sale de la máquina con su nombre grabado y la batería al 80. Saluda con la cabeza.",
              imagen=["Una línea de ensamblaje de la que sale un autómata pequeño de bronce con un nombre grabado en el pecho.",
                      BRON + " ajusta el último tornillo.", TESLA + " mira el medidor de batería."]),
            m(id="R02-N02-P2", titulo="El orden de la despedida",
              lugar=ENSAMBLAJE, personajes="Bron, Lima",
              carta="Destructor | ~Automata() corre solo cuando el objeto deja de existir · en un bloque, se destruyen AL REVÉS de como nacieron",
              recompensa="xp 10, oro 10",
              escena="""
                  Al final del turno, los autómatas se apagan solos. Lima quiere ver en qué orden, pero el destructor que escribió Bron no dice nada.
              """,
              sugiere="El destructor se llama `~Automata()` y no recibe nada. Hacé que muestre `se apaga` y el nombre.",
              desafio="Completá el destructor.",
              inicial='''
                  #include <iostream>
                  #include <string>

                  class Automata {
                  public:
                      explicit Automata(std::string n) : nombre_(n) { std::cout << "nace " << nombre_ << "\\n"; }
                      ~Automata() {}

                  private:
                      std::string nombre_;
                  };

                  int main()
                  {
                      Automata a("Cucu");
                      Automata b("Pinza");
                      Automata c("Rueca");
                      std::cout << "fin del turno\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  class Automata {
                  public:
                      explicit Automata(std::string n) : nombre_(n) { std::cout << "nace " << nombre_ << "\\n"; }
                      ~Automata() { std::cout << "se apaga " << nombre_ << "\\n"; }

                  private:
                      std::string nombre_;
                  };

                  int main()
                  {
                      Automata a("Cucu");
                      Automata b("Pinza");
                      Automata c("Rueca");
                      std::cout << "fin del turno\\n";
                      return 0;
                  }
              ''',
              al_superar="Rueca, Pinza, Cucú: el último en nacer es el primero en irse. Lima lo anota como un reloj que va para atrás.",
              imagen=["Tres autómatas pequeños apagándose uno tras otro, de derecha a izquierda.",
                      LIMA + " anota el orden.", BRON + " apaga la luz del taller."]),
            m(id="R02-N02-P3", titulo="La batidora de Oto",
              lugar="El comedor de los artífices", personajes="Bron, Oto",
              carta="new y delete | Automata* a = new Automata(...) vive hasta el delete · a->metodo() · sin delete, el destructor nunca corre",
              recompensa="xp 15, oro 15",
              escena="""
                  Bron armó un autómata con `new`, «para que dure más». A la noche sigue dando vueltas por el taller, porque nadie le hizo `delete`. Oto lo usa de batidora. Funciona bastante bien, pero hay que apagarlo alguna vez.
              """,
              sugiere="Lo que se crea con `new` se despide con `delete a;`. Ahí corre el destructor.",
              desafio="Apagá el autómata al final del turno.",
              inicial='''
                  #include <iostream>
                  #include <string>

                  class Automata {
                  public:
                      explicit Automata(std::string n) : nombre_(n) { std::cout << "nace " << nombre_ << "\\n"; }
                      ~Automata() { std::cout << "se apaga " << nombre_ << "\\n"; }
                      void trabajar() const { std::cout << nombre_ << " bate el guiso\\n"; }

                  private:
                      std::string nombre_;
                  };

                  int main()
                  {
                      Automata* a = new Automata("Batidora");
                      a->trabajar();
                      std::cout << "fin del turno\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  class Automata {
                  public:
                      explicit Automata(std::string n) : nombre_(n) { std::cout << "nace " << nombre_ << "\\n"; }
                      ~Automata() { std::cout << "se apaga " << nombre_ << "\\n"; }
                      void trabajar() const { std::cout << nombre_ << " bate el guiso\\n"; }

                  private:
                      std::string nombre_;
                  };

                  int main()
                  {
                      Automata* a = new Automata("Batidora");
                      a->trabajar();
                      std::cout << "fin del turno\\n";
                      delete a;
                      return 0;
                  }
              ''',
              al_superar="La batidora se apaga a la hora justa. Oto le pide a Bron que mañana la vuelva a prender.",
              imagen=["Un autómata pequeño con brazos de batidora dentro de una olla enorme.",
                      OTO + " sostiene la olla.", BRON + " aprieta el botón de apagado."]),
        ],
    },
    {
        "titulo": "R02-N03 · Encapsulamiento",
        "misiones": [
            m(id="R02-N03-P1", titulo="La caldera que no explota",
              lugar=CALDERA, personajes="Bron, Tesla, Lyn",
              carta="Invariante | una regla que SIEMPRE se cumple (0 <= presión <= 100) · el método que cambia el dato la cuida",
              recompensa="xp 10, oro 10",
              escena="""
                  La presión de la caldera nunca puede pasar de 100. El método `subir` que escribió Bron no revisa nada, y la aguja llega a 130. Lyn apuesta a que explota.
              """,
              sugiere="Si la subida pasaría de 100, `subir` no la hace y avisa `No se puede: pasaria de 100`.",
              desafio="Hacé que `subir` cuide la regla de la caldera.",
              inicial='''
                  #include <iostream>

                  class Caldera {
                  public:
                      void subir(int n)
                      {
                          presion_ += n;
                      }
                      int presion() const { return presion_; }

                  private:
                      int presion_ = 60;
                  };

                  int main()
                  {
                      Caldera c;
                      c.subir(30);
                      c.subir(40);
                      std::cout << "Presion: " << c.presion() << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  class Caldera {
                  public:
                      void subir(int n)
                      {
                          if (presion_ + n > 100) {
                              std::cout << "No se puede: pasaria de 100\\n";
                              return;
                          }
                          presion_ += n;
                      }
                      int presion() const { return presion_; }

                  private:
                      int presion_ = 60;
                  };

                  int main()
                  {
                      Caldera c;
                      c.subir(30);
                      c.subir(40);
                      std::cout << "Presion: " << c.presion() << "\\n";
                      return 0;
                  }
              ''',
              al_superar="La caldera se queda en 90 y deja de silbar. Lyn pierde la apuesta y le paga a Oto, que ni había apostado.",
              imagen=["Una caldera gigante con un manómetro en 90 y una palanca bloqueada.",
                      LYN + " le da una moneda a alguien fuera de cuadro.", TESLA + " revisa la palanca."]),
            m(id="R02-N03-P2", titulo="Avisar lo que no se pudo",
              lugar="El depósito de la Ciudadela", personajes="Bron, Lima",
              carta="bool | un método que puede fallar devuelve true o false · quien lo llama decide qué hacer",
              recompensa="xp 10, oro 10",
              escena="""
                  El stock de resortes nunca puede quedar negativo. El método `sacar` de Bron saca igual, aunque no alcance, y el depósito termina debiendo resortes.
              """,
              sugiere="`sacar` tiene que devolver `false` (sin tocar nada) si no alcanza, y `true` si pudo.",
              desafio="Hacé que `sacar` no deje el stock en negativo.",
              inicial='''
                  #include <iostream>

                  class Stock {
                  public:
                      bool sacar(int n)
                      {
                          cantidad_ -= n;
                          return true;
                      }
                      int cantidad() const { return cantidad_; }

                  private:
                      int cantidad_ = 10;
                  };

                  int main()
                  {
                      Stock resortes;
                      for (int pedido : {4, 5, 3}) {
                          if (resortes.sacar(pedido)) {
                              std::cout << "Saque " << pedido << ", quedan " << resortes.cantidad() << "\\n";
                          } else {
                              std::cout << "No alcanza para " << pedido << "\\n";
                          }
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  class Stock {
                  public:
                      bool sacar(int n)
                      {
                          if (n > cantidad_) {
                              return false;
                          }
                          cantidad_ -= n;
                          return true;
                      }
                      int cantidad() const { return cantidad_; }

                  private:
                      int cantidad_ = 10;
                  };

                  int main()
                  {
                      Stock resortes;
                      for (int pedido : {4, 5, 3}) {
                          if (resortes.sacar(pedido)) {
                              std::cout << "Saque " << pedido << ", quedan " << resortes.cantidad() << "\\n";
                          } else {
                              std::cout << "No alcanza para " << pedido << "\\n";
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="Queda un resorte y el pedido de tres espera. Lima marca en su cuaderno: «pedir resortes».",
              imagen=["Un cajón de resortes con uno solo adentro.",
                      LIMA + " escribe «pedir resortes».", BRON + " mira el cajón vacío."]),
            m(id="R02-N03-P3", titulo="Los minutos que se pasan",
              lugar="La torre del reloj", personajes="Lima, Bron",
              carta="Helper privado | una función private que solo usa la clase · ordena el estado después de cada cambio",
              recompensa="xp 15, oro 15",
              escena="""
                  El reloj de Lima guarda horas y minutos, y los minutos tienen que quedar siempre entre 0 y 59. Su método privado `normalizar` acomoda los minutos que se pasan… pero se olvida de sumarlos a las horas.
              """,
              sugiere="Por cada 60 minutos, una hora más: `horas_ += minutos_ / 60;` antes de quedarse con el resto. Y las horas dan la vuelta a las 24.",
              desafio="Completá `normalizar`.",
              inicial='''
                  #include <iostream>

                  class Reloj {
                  public:
                      void avanzar(int minutos)
                      {
                          minutos_ += minutos;
                          normalizar();
                      }
                      void mostrar() const { std::cout << horas_ << ":" << (minutos_ < 10 ? "0" : "") << minutos_ << "\\n"; }

                  private:
                      void normalizar()
                      {
                          minutos_ = minutos_ % 60;
                      }

                      int horas_ = 22;
                      int minutos_ = 50;
                  };

                  int main()
                  {
                      Reloj r;
                      r.avanzar(15);
                      r.mostrar();
                      r.avanzar(125);
                      r.mostrar();
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  class Reloj {
                  public:
                      void avanzar(int minutos)
                      {
                          minutos_ += minutos;
                          normalizar();
                      }
                      void mostrar() const { std::cout << horas_ << ":" << (minutos_ < 10 ? "0" : "") << minutos_ << "\\n"; }

                  private:
                      void normalizar()
                      {
                          horas_ = (horas_ + minutos_ / 60) % 24;
                          minutos_ = minutos_ % 60;
                      }

                      int horas_ = 22;
                      int minutos_ = 50;
                  };

                  int main()
                  {
                      Reloj r;
                      r.avanzar(15);
                      r.mostrar();
                      r.avanzar(125);
                      r.mostrar();
                      return 0;
                  }
              ''',
              al_superar="23:05 y después 1:10. El reloj de Lima nunca atrasa, y ahora tampoco se olvida de las horas.",
              imagen=["Un reloj de relojera abierto con las agujas en la una y diez.",
                      LIMA + " ajusta un engranaje mínimo con pinzas.", BRON + " sostiene la lupa."]),
        ],
    },
    {
        "titulo": "R02-N04 · Operadores para tus clases",
        "misiones": [
            m(id="R02-N04-P1", titulo="Tramos que se suman",
              lugar=CARTOGRAFO, personajes="Bron, Lima",
              carta="operator+ | Vec2 operator+(const Vec2& a, const Vec2& b) { return {a.x + b.x, a.y + b.y}; } · a + b llama a esa función",
              recompensa="xp 10, oro 10",
              escena="""
                  En la mesa del cartógrafo los tramos se suman: un tramo más otro tramo. El `+` que escribió Bron devuelve siempre el primero, y los mapas quedan cortos.
              """,
              sugiere="El resultado tiene que sumar las `x` y las `y` de los dos tramos.",
              desafio="Corregí `operator+`.",
              inicial='''
                  #include <iostream>

                  struct Vec2 {
                      int x = 0;
                      int y = 0;
                  };

                  Vec2 operator+(const Vec2& a, const Vec2& b)
                  {
                      return a;
                  }

                  int main()
                  {
                      Vec2 tramo1{3, 1};
                      Vec2 tramo2{2, 4};
                      Vec2 tramo3{-1, 2};
                      Vec2 total = tramo1 + tramo2 + tramo3;
                      std::cout << "Camino total: (" << total.x << ", " << total.y << ")\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  struct Vec2 {
                      int x = 0;
                      int y = 0;
                  };

                  Vec2 operator+(const Vec2& a, const Vec2& b)
                  {
                      return {a.x + b.x, a.y + b.y};
                  }

                  int main()
                  {
                      Vec2 tramo1{3, 1};
                      Vec2 tramo2{2, 4};
                      Vec2 tramo3{-1, 2};
                      Vec2 total = tramo1 + tramo2 + tramo3;
                      std::cout << "Camino total: (" << total.x << ", " << total.y << ")\\n";
                      return 0;
                  }
              ''',
              al_superar="Cuatro para un lado y siete para el otro. Bron pregunta para qué le sirve; Lima le contesta antes que nadie: para no perderse.",
              imagen=["Una mesa de cartógrafo con tres flechas de cobre encadenadas sobre un mapa.",
                      LIMA + " mide la flecha final.", BRON + " sostiene la segunda flecha."]),
            m(id="R02-N04-P2", titulo="Los mejores primero",
              lugar="La pista alrededor de las torres", personajes="Lyn, Bron",
              carta="operator< | bool operator<(const Marca& o) const · std::sort usa < · para «más puntos primero», < compara al revés",
              recompensa="xp 10, oro 10",
              escena="""
                  Lyn quiere la tabla de la carrera con los mejores **primero**. El `operator<` de Bron ordena de menor a mayor, y Lyn queda última con el puntaje más alto.
              """,
              sugiere="`std::sort` pone primero lo que es «menor». Si «menor» significa «más puntos», el operador devuelve `puntos > otra.puntos`.",
              desafio="Hacé que la tabla empiece por el puntaje más alto.",
              inicial='''
                  #include <algorithm>
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  struct Marca {
                      std::string nombre;
                      int puntos = 0;
                      bool operator<(const Marca& otra) const { return puntos < otra.puntos; }
                  };

                  int main()
                  {
                      std::vector<Marca> tabla = {{"Bron", 120}, {"Lyn", 340}, {"Lima", 210}, {"Oto", 95}};
                      std::sort(tabla.begin(), tabla.end());
                      for (const Marca& m : tabla) {
                          std::cout << m.nombre << " " << m.puntos << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <algorithm>
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  struct Marca {
                      std::string nombre;
                      int puntos = 0;
                      bool operator<(const Marca& otra) const { return puntos > otra.puntos; }
                  };

                  int main()
                  {
                      std::vector<Marca> tabla = {{"Bron", 120}, {"Lyn", 340}, {"Lima", 210}, {"Oto", 95}};
                      std::sort(tabla.begin(), tabla.end());
                      for (const Marca& m : tabla) {
                          std::cout << m.nombre << " " << m.puntos << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Lyn primera, con 340. Lo grita desde la torre del reloj, otra vez.",
              imagen=["Una tabla de posiciones en un pizarrón con Lyn arriba de todo.",
                      LYN + " festeja en el podio.", BRON + " escribe los puntajes con tiza."]),
            m(id="R02-N04-P3", titulo="La caja fuerte del cartógrafo",
              lugar=CARTOGRAFO, personajes="Lyn, Lima",
              carta="friend | friend std::ostream& operator<<(std::ostream&, const Mapa&); · la clase le da permiso para leer lo privado · la amistad la da la clase",
              recompensa="xp 15, oro 15",
              escena="""
                  Los mapas del cartógrafo guardan sus coordenadas en privado. Bron escribió un `<<` para mostrarlos, pero el Taller no lo deja leer lo privado. Lyn quiere ser amiga de la caja fuerte; la caja no la deja.
                  —La amistad la da la clase —dice Lima, muy seria—. No la pide la función.
              """,
              sugiere="Adentro de la clase, declará el operador como amigo: `friend std::ostream& operator<<(std::ostream& os, const Mapa& m);`.",
              desafio="Hacé que la clase le dé permiso al operador.",
              inicial='''
                  #include <iostream>
                  #include <string>

                  class Mapa {
                  public:
                      Mapa(std::string lugar, int x, int y) : lugar_(lugar), x_(x), y_(y) {}

                  private:
                      std::string lugar_;
                      int x_;
                      int y_;
                  };

                  std::ostream& operator<<(std::ostream& os, const Mapa& m)
                  {
                      return os << m.lugar_ << " en (" << m.x_ << ", " << m.y_ << ")";
                  }

                  int main()
                  {
                      Mapa a("Torre del reloj", 4, 7);
                      Mapa b("Comedor", 1, 2);
                      std::cout << a << "\\n" << b << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  class Mapa {
                  public:
                      Mapa(std::string lugar, int x, int y) : lugar_(lugar), x_(x), y_(y) {}
                      friend std::ostream& operator<<(std::ostream& os, const Mapa& m);

                  private:
                      std::string lugar_;
                      int x_;
                      int y_;
                  };

                  std::ostream& operator<<(std::ostream& os, const Mapa& m)
                  {
                      return os << m.lugar_ << " en (" << m.x_ << ", " << m.y_ << ")";
                  }

                  int main()
                  {
                      Mapa a("Torre del reloj", 4, 7);
                      Mapa b("Comedor", 1, 2);
                      std::cout << a << "\\n" << b << "\\n";
                      return 0;
                  }
              ''',
              al_superar="El operador ve los mapas; Lyn, no. Dice que es injusto. La caja sigue cerrada.",
              imagen=["Una caja fuerte de bronce con mapas enrollados adentro y una rendija por donde sale una tira de papel con coordenadas.",
                      LYN + " intenta espiar por la rendija.", LIMA + " la aparta de un tirón."]),
        ],
    },
    {
        "titulo": "R02-N05 · Composición",
        "misiones": [
            m(id="R02-N05-P1", titulo="El reloj que delega",
              lugar=RELOJ, personajes="Bron, Tesla",
              carta="Composición | class Reloj { Pendulo pendulo_; }; · el reloj TIENE un péndulo · Reloj::tic() le pide el trabajo a pendulo_",
              recompensa="xp 10, oro 10",
              escena="""
                  El Gran Reloj **tiene** un péndulo. Cada `tic` del reloj tendría que hacer oscilar el péndulo, pero el `tic` de Bron solo hace ruido: el péndulo nunca se entera.
              """,
              sugiere="El reloj no oscila: le pide al péndulo que oscile. Adentro de `tic`, llamá a `pendulo_.oscilar()`.",
              desafio="Hacé que el reloj delegue en su péndulo.",
              inicial='''
                  #include <iostream>

                  class Pendulo {
                  public:
                      void oscilar() { oscilaciones_++; }
                      int oscilaciones() const { return oscilaciones_; }

                  private:
                      int oscilaciones_ = 0;
                  };

                  class Reloj {
                  public:
                      void tic()
                      {
                          std::cout << "[tic]";
                      }
                      int oscilaciones() const { return pendulo_.oscilaciones(); }

                  private:
                      Pendulo pendulo_;
                  };

                  int main()
                  {
                      Reloj r;
                      for (int i = 0; i < 4; i++) {
                          r.tic();
                      }
                      std::cout << "\\nOscilaciones: " << r.oscilaciones() << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  class Pendulo {
                  public:
                      void oscilar() { oscilaciones_++; }
                      int oscilaciones() const { return oscilaciones_; }

                  private:
                      int oscilaciones_ = 0;
                  };

                  class Reloj {
                  public:
                      void tic()
                      {
                          std::cout << "[tic]";
                          pendulo_.oscilar();
                      }
                      int oscilaciones() const { return pendulo_.oscilaciones(); }

                  private:
                      Pendulo pendulo_;
                  };

                  int main()
                  {
                      Reloj r;
                      for (int i = 0; i < 4; i++) {
                          r.tic();
                      }
                      std::cout << "\\nOscilaciones: " << r.oscilaciones() << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Cuatro tics, cuatro oscilaciones. El Gran Reloj de la plaza vuelve a dar la hora.",
              imagen=["El Gran Reloj de la plaza visto por dentro, con un péndulo enorme oscilando.",
                      TESLA + " escucha el tic con los ojos cerrados.", BRON + " empuja el péndulo."]),
            m(id="R02-N05-P2", titulo="Primero la caja",
              lugar=RELOJ, personajes="Lima, Bron",
              carta="Orden de construcción | los miembros se construyen en el orden en que están DECLARADOS en la clase · se destruyen al revés",
              recompensa="xp 10, oro 10",
              escena="""
                  Al armar el reloj, Lima quiere que primero se arme la caja y después el péndulo (si no, ¿dónde se cuelga?). En la clase de Bron, el péndulo está declarado arriba, y se arma primero.
              """,
              sugiere="Los miembros nacen en el orden en que están escritos en la clase, no en el de la lista de inicialización. Cambiá el orden de las declaraciones.",
              desafio="Hacé que la caja se arme antes que el péndulo.",
              inicial='''
                  #include <iostream>

                  struct Caja {
                      Caja() { std::cout << "se arma la caja\\n"; }
                  };

                  struct Pendulo {
                      Pendulo() { std::cout << "se cuelga el pendulo\\n"; }
                  };

                  class Reloj {
                  public:
                      Reloj() { std::cout << "reloj listo\\n"; }

                  private:
                      Pendulo pendulo_;
                      Caja caja_;
                  };

                  int main()
                  {
                      Reloj r;
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  struct Caja {
                      Caja() { std::cout << "se arma la caja\\n"; }
                  };

                  struct Pendulo {
                      Pendulo() { std::cout << "se cuelga el pendulo\\n"; }
                  };

                  class Reloj {
                  public:
                      Reloj() { std::cout << "reloj listo\\n"; }

                  private:
                      Caja caja_;
                      Pendulo pendulo_;
                  };

                  int main()
                  {
                      Reloj r;
                      return 0;
                  }
              ''',
              al_superar="Caja, péndulo, reloj listo. El péndulo por fin tiene de dónde colgarse.",
              imagen=["Un reloj de pie a medio armar: la caja de madera lista y el péndulo esperando en el piso.",
                      LIMA + " cuelga el péndulo.", BRON + " sostiene la caja."]),
            m(id="R02-N05-P3", titulo="El tablero de relojes",
              lugar=RELOJ, personajes="Bron, Tesla",
              carta="Tener muchos | class Tablero { std::vector<Reloj> relojes_; }; · el tablero recorre sus partes y suma lo de cada una",
              recompensa="xp 15, oro 15",
              escena="""
                  El tablero de la plaza **tiene** varios relojes, y Tesla le pide a Bron el total de dientes de todo el tablero. El método `dientes` del tablero devuelve solo los del primer reloj.
              """,
              sugiere="Recorré `relojes_` y sumá lo que devuelve `dientes()` de cada uno.",
              desafio="Completá el total del tablero.",
              inicial='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  class Reloj {
                  public:
                      Reloj(std::string nombre, int engranajes, int por_engranaje)
                          : nombre_(nombre), engranajes_(engranajes), por_engranaje_(por_engranaje) {}
                      int dientes() const { return engranajes_ * por_engranaje_; }

                  private:
                      std::string nombre_;
                      int engranajes_;
                      int por_engranaje_;
                  };

                  class Tablero {
                  public:
                      void agregar(const Reloj& r) { relojes_.push_back(r); }
                      int dientes() const
                      {
                          return relojes_[0].dientes();
                      }

                  private:
                      std::vector<Reloj> relojes_;
                  };

                  int main()
                  {
                      Tablero t;
                      t.agregar(Reloj("Pared", 3, 40));
                      t.agregar(Reloj("Torre", 12, 60));
                      t.agregar(Reloj("Bolsillo", 5, 12));
                      std::cout << "Dientes del tablero: " << t.dientes() << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  class Reloj {
                  public:
                      Reloj(std::string nombre, int engranajes, int por_engranaje)
                          : nombre_(nombre), engranajes_(engranajes), por_engranaje_(por_engranaje) {}
                      int dientes() const { return engranajes_ * por_engranaje_; }

                  private:
                      std::string nombre_;
                      int engranajes_;
                      int por_engranaje_;
                  };

                  class Tablero {
                  public:
                      void agregar(const Reloj& r) { relojes_.push_back(r); }
                      int dientes() const
                      {
                          int total = 0;
                          for (const Reloj& r : relojes_) {
                              total += r.dientes();
                          }
                          return total;
                      }

                  private:
                      std::vector<Reloj> relojes_;
                  };

                  int main()
                  {
                      Tablero t;
                      t.agregar(Reloj("Pared", 3, 40));
                      t.agregar(Reloj("Torre", 12, 60));
                      t.agregar(Reloj("Bolsillo", 5, 12));
                      std::cout << "Dientes del tablero: " << t.dientes() << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Novecientos dientes. Tesla le muestra a Bron que no hizo falta abrir ningún reloj: cada uno sabía lo suyo.",
              imagen=["Un tablero de bronce en la plaza con tres relojes de distinto tamaño.",
                      TESLA + " suma con el compás en el aire.", BRON + " mira el tablero."]),
        ],
    },
    {
        "titulo": "R02-N06 · Herencia",
        "misiones": [
            m(id="R02-N06-P1", titulo="Primero el esqueleto",
              lugar=ARCHIVO, personajes="Bron, Tesla",
              carta="Constructor de la base | AutomataCarga(std::string n) : Automata(n, 100) {} · la base se construye primero, en la lista de inicialización",
              recompensa="xp 10, oro 10",
              escena="""
                  El autómata de carga **es un** autómata, con brazos más fuertes. Bron escribió la clase derivada, pero el Taller se queja: el autómata base no tiene constructor sin datos, y nadie le pasa el nombre ni la batería.
              """,
              sugiere="La derivada llama al constructor de la base en su lista de inicialización: `: Automata(n, 100)`.",
              desafio="Construí la parte de `Automata` dentro del de carga.",
              inicial='''
                  #include <iostream>
                  #include <string>

                  class Automata {
                  public:
                      Automata(std::string n, int b) : nombre_(n), bateria_(b) {}
                      void mostrar() const { std::cout << nombre_ << " (bateria " << bateria_ << "%)\\n"; }

                  private:
                      std::string nombre_;
                      int bateria_;
                  };

                  class AutomataCarga : public Automata {
                  public:
                      explicit AutomataCarga(std::string n) : kilos_(500) {}
                      void levantar() const { std::cout << "Levanta " << kilos_ << " kg\\n"; }

                  private:
                      int kilos_;
                  };

                  int main()
                  {
                      AutomataCarga grua("Grua");
                      grua.mostrar();
                      grua.levantar();
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  class Automata {
                  public:
                      Automata(std::string n, int b) : nombre_(n), bateria_(b) {}
                      void mostrar() const { std::cout << nombre_ << " (bateria " << bateria_ << "%)\\n"; }

                  private:
                      std::string nombre_;
                      int bateria_;
                  };

                  class AutomataCarga : public Automata {
                  public:
                      explicit AutomataCarga(std::string n) : Automata(n, 100), kilos_(500) {}
                      void levantar() const { std::cout << "Levanta " << kilos_ << " kg\\n"; }

                  private:
                      int kilos_;
                  };

                  int main()
                  {
                      AutomataCarga grua("Grua");
                      grua.mostrar();
                      grua.levantar();
                      return 0;
                  }
              ''',
              al_superar="La grúa nace con su nombre, la batería llena y los brazos fuertes. Usa `mostrar` sin haberlo escrito: lo heredó.",
              imagen=["Un archivo de carpetas con la etiqueta «Autómata» y adentro una más fina «de carga».",
                      "Un autómata grúa de bronce levantando un cajón.", BRON + " le pasa a " + TESLA + " la carpeta."]),
            m(id="R02-N06-P2", titulo="Lo que hacía la base, y algo más",
              lugar=ARCHIVO, personajes="Bron, Lima",
              carta="Redefinir | la derivada escribe un método con el mismo nombre · Base::metodo() llama a la versión de la base",
              recompensa="xp 10, oro 10",
              escena="""
                  El autómata guardián muestra su ficha, pero solo dice su turno: se perdió el nombre y la batería, que mostraba el autómata base. Lima quiere las dos cosas.
              """,
              sugiere="Adentro de `Guardian::mostrar`, primero llamá a `Automata::mostrar();` y después agregá lo propio.",
              desafio="Reutilizá la ficha de la base.",
              inicial='''
                  #include <iostream>
                  #include <string>

                  class Automata {
                  public:
                      Automata(std::string n, int b) : nombre_(n), bateria_(b) {}
                      void mostrar() const { std::cout << nombre_ << " (bateria " << bateria_ << "%)"; }

                  private:
                      std::string nombre_;
                      int bateria_;
                  };

                  class Guardian : public Automata {
                  public:
                      Guardian(std::string n, std::string turno) : Automata(n, 90), turno_(turno) {}
                      void mostrar() const
                      {
                          std::cout << " - turno " << turno_ << "\\n";
                      }

                  private:
                      std::string turno_;
                  };

                  int main()
                  {
                      Guardian g("Centinela", "noche");
                      g.mostrar();
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  class Automata {
                  public:
                      Automata(std::string n, int b) : nombre_(n), bateria_(b) {}
                      void mostrar() const { std::cout << nombre_ << " (bateria " << bateria_ << "%)"; }

                  private:
                      std::string nombre_;
                      int bateria_;
                  };

                  class Guardian : public Automata {
                  public:
                      Guardian(std::string n, std::string turno) : Automata(n, 90), turno_(turno) {}
                      void mostrar() const
                      {
                          Automata::mostrar();
                          std::cout << " - turno " << turno_ << "\\n";
                      }

                  private:
                      std::string turno_;
                  };

                  int main()
                  {
                      Guardian g("Centinela", "noche");
                      g.mostrar();
                      return 0;
                  }
              ''',
              al_superar="«Centinela (batería 90%) - turno noche.» Lima archiva la ficha completa.",
              imagen=["Un autómata guardián de bronce con una lámpara en la mano, de noche.",
                      LIMA + " archiva una ficha.", BRON + " le da cuerda al guardián."]),
            m(id="R02-N06-P3", titulo="Lo que ve la derivada",
              lugar=ARCHIVO, personajes="Bron, Tesla",
              carta="protected | private: solo la clase · protected: la clase y sus derivadas · public: todos · lo private de la base nunca lo ve la derivada",
              recompensa="xp 15, oro 15",
              escena="""
                  El autómata jardinero tiene que gastar energía cada vez que riega, y la energía está en la clase base. Bron la declaró `private`, y el jardinero no puede tocarla. Tesla le muestra la tabla de accesos del archivo.
              """,
              sugiere="Para que una derivada pueda usar un dato de la base (y los de afuera no), ese dato va en `protected`.",
              desafio="Cambiá el acceso del dato para que el jardinero lo pueda usar.",
              inicial='''
                  #include <iostream>

                  class Automata {
                  public:
                      int energia() const { return energia_; }

                  private:
                      int energia_ = 50;
                  };

                  class Jardinero : public Automata {
                  public:
                      void regar()
                      {
                          energia_ -= 15;
                          std::cout << "Riega las macetas (energia " << energia_ << ")\\n";
                      }
                  };

                  int main()
                  {
                      Jardinero j;
                      j.regar();
                      j.regar();
                      std::cout << "Le queda " << j.energia() << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  class Automata {
                  public:
                      int energia() const { return energia_; }

                  protected:
                      int energia_ = 50;
                  };

                  class Jardinero : public Automata {
                  public:
                      void regar()
                      {
                          energia_ -= 15;
                          std::cout << "Riega las macetas (energia " << energia_ << ")\\n";
                      }
                  };

                  int main()
                  {
                      Jardinero j;
                      j.regar();
                      j.regar();
                      std::cout << "Le queda " << j.energia() << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Dos riegos y le queda energía para uno más. Desde afuera, nadie puede tocarla: solo leerla.",
              imagen=["Un autómata jardinero de bronce regando macetas en una terraza de la Ciudadela.",
                      TESLA + " señala una tabla de accesos colgada en la pared.", BRON + " la copia en un papel."]),
        ],
    },
    {
        "titulo": "R02-N07 · Polimorfismo",
        "misiones": [
            m(id="R02-N07-P1", titulo="Una orden, muchas respuestas",
              lugar=PATIO, personajes="Bron, Tesla",
              carta="virtual | virtual void trabajar() const en la base · override en las derivadas · con un puntero o referencia a la base, se ejecuta la del tipo REAL",
              recompensa="xp 10, oro 10",
              escena="""
                  Tesla le da la misma orden a varios autómatas: «¡Trabajá!». Todos responden lo mismo: «trabaja un autómata». El método de la base no es `virtual`, y C++ elige la versión por el tipo del puntero, no del objeto.
              """,
              sugiere="Poné `virtual` en el método de la base, y `override` en los de las derivadas.",
              desafio="Hacé que cada autómata trabaje a su manera.",
              inicial='''
                  #include <iostream>
                  #include <memory>
                  #include <vector>

                  class Automata {
                  public:
                      virtual ~Automata() = default;
                      void trabajar() const { std::cout << "trabaja un automata\\n"; }
                  };

                  class Carga : public Automata {
                  public:
                      void trabajar() const { std::cout << "levanta cajas\\n"; }
                  };

                  class Soldador : public Automata {
                  public:
                      void trabajar() const { std::cout << "enciende una chispa\\n"; }
                  };

                  int main()
                  {
                      std::vector<std::unique_ptr<Automata>> patio;
                      patio.push_back(std::make_unique<Carga>());
                      patio.push_back(std::make_unique<Soldador>());
                      for (const auto& a : patio) {
                          a->trabajar();
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <memory>
                  #include <vector>

                  class Automata {
                  public:
                      virtual ~Automata() = default;
                      virtual void trabajar() const { std::cout << "trabaja un automata\\n"; }
                  };

                  class Carga : public Automata {
                  public:
                      void trabajar() const override { std::cout << "levanta cajas\\n"; }
                  };

                  class Soldador : public Automata {
                  public:
                      void trabajar() const override { std::cout << "enciende una chispa\\n"; }
                  };

                  int main()
                  {
                      std::vector<std::unique_ptr<Automata>> patio;
                      patio.push_back(std::make_unique<Carga>());
                      patio.push_back(std::make_unique<Soldador>());
                      for (const auto& a : patio) {
                          a->trabajar();
                      }
                      return 0;
                  }
              ''',
              al_superar="Uno levanta cajas, otro enciende una chispa. —Una orden, muchas respuestas —sonríe Tesla.",
              imagen=["Un patio con autómatas distintos: uno levanta cajas, otro suelda con chispas.",
                      TESLA + " levanta la mano dando la orden.", BRON + " observa."]),
            m(id="R02-N07-P2", titulo="El autómata rebanado",
              lugar=PATIO, personajes="Bron, Lima",
              carta="Rebanado | guardar un derivado en un vector<Base> copia SOLO la parte de la base · para muchas clases juntas: vector<unique_ptr<Base>>",
              recompensa="xp 15, oro 15",
              escena="""
                  Bron guardó la batidora de Oto en un `std::vector<Automata>`, y la batidora dejó de batir: el vector guardó solo la parte de autómata. Lima dice que la «rebanaron».
              """,
              sugiere="Un `std::vector<Automata>` guarda copias de la base. Para guardar el objeto entero, guardá punteros dueños: `std::vector<std::unique_ptr<Automata>>` y `std::make_unique<Batidora>()`.",
              desafio="Guardá la batidora sin rebanarla.",
              inicial='''
                  #include <iostream>
                  #include <memory>
                  #include <vector>

                  class Automata {
                  public:
                      virtual ~Automata() = default;
                      virtual void trabajar() const { std::cout << "trabaja un automata\\n"; }
                  };

                  class Batidora : public Automata {
                  public:
                      void trabajar() const override { std::cout << "bate el guiso de Oto\\n"; }
                  };

                  int main()
                  {
                      std::vector<Automata> cocina;
                      cocina.push_back(Batidora());
                      for (const Automata& a : cocina) {
                          a.trabajar();
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <memory>
                  #include <vector>

                  class Automata {
                  public:
                      virtual ~Automata() = default;
                      virtual void trabajar() const { std::cout << "trabaja un automata\\n"; }
                  };

                  class Batidora : public Automata {
                  public:
                      void trabajar() const override { std::cout << "bate el guiso de Oto\\n"; }
                  };

                  int main()
                  {
                      std::vector<std::unique_ptr<Automata>> cocina;
                      cocina.push_back(std::make_unique<Batidora>());
                      for (const auto& a : cocina) {
                          a->trabajar();
                      }
                      return 0;
                  }
              ''',
              al_superar="La batidora vuelve a batir. Oto no sabe qué pasó, pero el guiso salió espumoso.",
              imagen=["Una batidora-autómata cortada al medio con una línea de puntos, al lado de otra entera.",
                      LIMA + " señala la línea de puntos.", BRON + " se rasca la cabeza."]),
            m(id="R02-N07-P3", titulo="El override que no era",
              lugar=PATIO, personajes="Bron, Tesla",
              carta="override | si la firma no es IDÉNTICA (hasta el const), no redefine: esconde · override hace que el compilador lo avise",
              recompensa="xp 15, oro 15",
              escena="""
                  El autómata jardinero sigue diciendo «trabaja un automata». Bron jura que redefinió `trabajar`. Tesla mira el código: en la base es `const`; en el jardinero, no. Son **dos** métodos distintos.
              """,
              sugiere="Agregale `const` al método del jardinero, para que tenga la misma firma que el de la base. Y `override`: si algún día no coincide, el compilador avisa.",
              desafio="Hacé que el jardinero redefina de verdad el método.",
              inicial='''
                  #include <iostream>
                  #include <memory>

                  class Automata {
                  public:
                      virtual ~Automata() = default;
                      virtual void trabajar() const { std::cout << "trabaja un automata\\n"; }
                  };

                  class Jardinero : public Automata {
                  public:
                      void trabajar() { std::cout << "riega las macetas\\n"; }
                  };

                  int main()
                  {
                      std::unique_ptr<Automata> a = std::make_unique<Jardinero>();
                      a->trabajar();
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <memory>

                  class Automata {
                  public:
                      virtual ~Automata() = default;
                      virtual void trabajar() const { std::cout << "trabaja un automata\\n"; }
                  };

                  class Jardinero : public Automata {
                  public:
                      void trabajar() const override { std::cout << "riega las macetas\\n"; }
                  };

                  int main()
                  {
                      std::unique_ptr<Automata> a = std::make_unique<Jardinero>();
                      a->trabajar();
                      return 0;
                  }
              ''',
              al_superar="El jardinero riega. Bron agrega `override` en todos lados, por las dudas; Tesla lo aprueba.",
              imagen=["Un autómata jardinero regando, con una palabra «const» flotando sobre su cabeza.",
                      TESLA + " señala la palabra.", BRON + " escribe «override» en un cartel."]),
        ],
    },
    {
        "titulo": "R02-N08 · Programas en varios archivos",
        "misiones": [
            m(id="R02-N08-P1", titulo="La ficha y el detalle",
              lugar=PLANOS, personajes="Bron, Lima",
              carta="Declarar y definir | en la clase se DECLARA int pisos() const; · afuera se DEFINE int Torre::pisos() const { ... } · Torre:: dice de quién es",
              recompensa="xp 10, oro 10",
              escena="""
                  En la Sala de los Planos, la **ficha** de cada máquina va en un cajón y el **detalle** en otro. Bron escribió el detalle del método afuera de la clase, pero se olvidó de decir de qué clase es, y el Taller cree que es una función suelta.
              """,
              sugiere="Afuera de la clase, el nombre del método lleva adelante el nombre de la clase: `int Torre::altura() const`.",
              desafio="Decí de qué clase es el método.",
              inicial='''
                  #include <iostream>

                  // La ficha (iria en Torre.h)
                  class Torre {
                  public:
                      explicit Torre(int pisos) : pisos_(pisos) {}
                      int altura() const;

                  private:
                      int pisos_;
                  };

                  // El detalle (iria en Torre.cpp)
                  int altura() const
                  {
                      return pisos_ * 3;
                  }

                  int main()
                  {
                      Torre t(12);
                      std::cout << "Altura: " << t.altura() << " metros\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  // La ficha (iria en Torre.h)
                  class Torre {
                  public:
                      explicit Torre(int pisos) : pisos_(pisos) {}
                      int altura() const;

                  private:
                      int pisos_;
                  };

                  // El detalle (iria en Torre.cpp)
                  int Torre::altura() const
                  {
                      return pisos_ * 3;
                  }

                  int main()
                  {
                      Torre t(12);
                      std::cout << "Altura: " << t.altura() << " metros\\n";
                      return 0;
                  }
              ''',
              al_superar="Treinta y seis metros. Lima guarda la ficha en un cajón y el detalle en otro, con etiquetas.",
              imagen=["Dos cajones de un archivo: uno dice «ficha» y otro «detalle».",
                      LIMA + " guarda papeles con etiquetas.", BRON + " sostiene un plano."]),
            m(id="R02-N08-P2", titulo="El esqueleto del enlazador",
              lugar=PLANOS, personajes="Bron, Gheco",
              criatura="esqueleto",
              carta="undefined reference | un método DECLARADO que nadie DEFINIÓ · compila, pero el enlazador no encuentra el cuerpo",
              recompensa="xp 10, oro 10",
              escena="""
                  Del cajón de los detalles sale un **esqueleto** que grita «undefined reference». La ficha de la torre promete un método `pisos()`, pero nadie escribió su detalle. Gheco señala la línea del error: no tiene número de línea, tiene un nombre.
              """,
              sugiere="Escribí la definición que falta: `int Torre::pisos() const { return pisos_; }`.",
              desafio="Escribí el detalle que prometió la ficha.",
              inicial='''
                  #include <iostream>

                  class Torre {
                  public:
                      explicit Torre(int pisos) : pisos_(pisos) {}
                      int pisos() const;
                      int altura() const;

                  private:
                      int pisos_;
                  };

                  int Torre::altura() const
                  {
                      return pisos_ * 3;
                  }

                  int main()
                  {
                      Torre t(15);
                      std::cout << t.pisos() << " pisos, " << t.altura() << " metros\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  class Torre {
                  public:
                      explicit Torre(int pisos) : pisos_(pisos) {}
                      int pisos() const;
                      int altura() const;

                  private:
                      int pisos_;
                  };

                  int Torre::pisos() const
                  {
                      return pisos_;
                  }

                  int Torre::altura() const
                  {
                      return pisos_ * 3;
                  }

                  int main()
                  {
                      Torre t(15);
                      std::cout << t.pisos() << " pisos, " << t.altura() << " metros\\n";
                      return 0;
                  }
              ''',
              al_superar="El esqueleto encuentra su cuerpo y se va caminando, contento. Gheco anota: «undefined reference: falta un detalle».",
              imagen=["Un esqueleto saliendo de un cajón de archivo con un cartel «undefined reference».",
                      BRON + " escribe en una hoja de detalle.", GHECO + " señala el cartel."]),
            m(id="R02-N08-P3", titulo="La ficha que se pegó dos veces",
              lugar=PLANOS, personajes="Bron, Tesla",
              carta="Guardas | #ifndef TORRE_H · #define TORRE_H · ... · #endif (o #pragma once) · si el header se incluye dos veces, la segunda no pega nada",
              recompensa="xp 15, oro 15",
              escena="""
                  Cuando un `.cpp` incluye dos headers que a su vez incluyen `Torre.h`, la ficha se pega **dos veces** y el Taller grita «redefinition». Tesla le muestra a Bron lo que pasa, pegando la ficha dos veces a mano.
              """,
              sugiere="Envolvé la ficha con guardas: `#ifndef TORRE_H`, `#define TORRE_H` al principio y `#endif` al final. Hacelo en **las dos** copias (son el mismo archivo pegado dos veces): la segunda vez, `TORRE_H` ya está definido y se saltea.",
              desafio="Poné las guardas para que la segunda copia no pegue nada.",
              inicial='''
                  #include <iostream>

                  // Torre.h, pegado por el primer #include
                  class Torre {
                  public:
                      int pisos = 12;
                  };

                  // Torre.h otra vez, pegado por un segundo #include
                  class Torre {
                  public:
                      int pisos = 12;
                  };

                  int main()
                  {
                      Torre t;
                      std::cout << "La torre tiene " << t.pisos << " pisos\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  // Torre.h, pegado por el primer #include
                  #ifndef TORRE_H
                  #define TORRE_H
                  class Torre {
                  public:
                      int pisos = 12;
                  };
                  #endif

                  // Torre.h otra vez, pegado por un segundo #include
                  #ifndef TORRE_H
                  #define TORRE_H
                  class Torre {
                  public:
                      int pisos = 12;
                  };
                  #endif

                  int main()
                  {
                      Torre t;
                      std::cout << "La torre tiene " << t.pisos << " pisos\\n";
                      return 0;
                  }
              ''',
              al_superar="La segunda copia se saltea sola. Mientras ordena los cajones, Bron encuentra el **plano de las bisagras** del Vidriero, dibujado por Tesla. Las medidas no cierran con ninguna puerta. Tesla lo guarda sin decir nada.",
              imagen=["Dos hojas iguales de una ficha de torre, la segunda tachada con una línea suave.",
                      BRON + " sostiene un plano de bisagras con medidas raras.", TESLA + " se lo saca de la mano con cuidado."]),
        ],
    },
    {
        "titulo": "R02-N09 · Jefe: la Quimera de la Arena",
        "misiones": [
            m(id="R02-N09-P1", titulo="Cada forma resiste algo",
              lugar=ARENA, personajes="Bron, Lima, Tesla",
              criatura="dragon",
              carta="Clase abstracta | virtual int danio(const std::string& golpe) const = 0; · cada forma de la Quimera lo calcula a su manera",
              recompensa="xp 15, oro 15",
              escena="""
                  En la jaula del fondo de la Arena espera la **Quimera**: cabeza de león, cuerpo de cabra y cola de serpiente. Cada forma resiste un golpe distinto. Bron escribió las formas, pero la serpiente todavía no sabe qué la lastima.
              """,
              sugiere="La serpiente recibe el daño entero de un golpe de `\"llave\"` (20) y la mitad de cualquier otro (10). Escribí su `danio` como los otros.",
              desafio="Completá la forma de serpiente.",
              inicial='''
                  #include <iostream>
                  #include <memory>
                  #include <string>
                  #include <vector>

                  class Forma {
                  public:
                      virtual ~Forma() = default;
                      virtual std::string nombre() const = 0;
                      virtual int danio(const std::string& golpe) const = 0;
                  };

                  class Leon : public Forma {
                  public:
                      std::string nombre() const override { return "leon"; }
                      int danio(const std::string& golpe) const override { return golpe == "red" ? 20 : 5; }
                  };

                  class Cabra : public Forma {
                  public:
                      std::string nombre() const override { return "cabra"; }
                      int danio(const std::string& golpe) const override { return golpe == "palanca" ? 20 : 5; }
                  };

                  class Serpiente : public Forma {
                  public:
                      std::string nombre() const override { return "serpiente"; }
                  };

                  int main()
                  {
                      std::vector<std::unique_ptr<Forma>> formas;
                      formas.push_back(std::make_unique<Leon>());
                      formas.push_back(std::make_unique<Cabra>());
                      formas.push_back(std::make_unique<Serpiente>());
                      for (const auto& f : formas) {
                          std::cout << f->nombre() << ": llave " << f->danio("llave") << ", red " << f->danio("red") << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <memory>
                  #include <string>
                  #include <vector>

                  class Forma {
                  public:
                      virtual ~Forma() = default;
                      virtual std::string nombre() const = 0;
                      virtual int danio(const std::string& golpe) const = 0;
                  };

                  class Leon : public Forma {
                  public:
                      std::string nombre() const override { return "leon"; }
                      int danio(const std::string& golpe) const override { return golpe == "red" ? 20 : 5; }
                  };

                  class Cabra : public Forma {
                  public:
                      std::string nombre() const override { return "cabra"; }
                      int danio(const std::string& golpe) const override { return golpe == "palanca" ? 20 : 5; }
                  };

                  class Serpiente : public Forma {
                  public:
                      std::string nombre() const override { return "serpiente"; }
                      int danio(const std::string& golpe) const override { return golpe == "llave" ? 20 : 10; }
                  };

                  int main()
                  {
                      std::vector<std::unique_ptr<Forma>> formas;
                      formas.push_back(std::make_unique<Leon>());
                      formas.push_back(std::make_unique<Cabra>());
                      formas.push_back(std::make_unique<Serpiente>());
                      for (const auto& f : formas) {
                          std::cout << f->nombre() << ": llave " << f->danio("llave") << ", red " << f->danio("red") << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="León: la red. Cabra: la palanca. Serpiente: la llave. Lima lo escribe en un cartel y lo cuelga en la tribuna.",
              imagen=["La Arena bajo la Ciudadela con una jaula al fondo y " + QUIMERA + ".",
                      BRON + " sostiene una red, una palanca y su llave.", LIMA + " cuelga un cartel en la tribuna."]),
            m(id="R02-N09-P2", titulo="La forma de cada turno",
              lugar=ARENA, personajes="Bron, Lima",
              criatura="dragon",
              carta="Composición + polimorfismo | la Quimera TIENE tres formas (vector<unique_ptr<Forma>>) · la forma del turno t es formas_[t % 3]",
              recompensa="xp 15, oro 15",
              escena="""
                  La Quimera cambia de forma en cada turno, siempre en el mismo orden: león, cabra, serpiente, león… Bron le pregunta qué es antes de cada golpe, y la Quimera cambia mientras él pregunta.
                  —¡No le preguntes! —grita Lima desde la tribuna—. ¡Sabé cuál toca!
              """,
              sugiere="La forma del turno `t` (empezando en 0) es `formas_[t % formas_.size()]`. Completá `forma_del_turno`.",
              desafio="Elegí la forma de cada turno con el resto.",
              inicial='''
                  #include <iostream>
                  #include <memory>
                  #include <string>
                  #include <vector>

                  class Forma {
                  public:
                      explicit Forma(std::string n) : nombre_(n) {}
                      const std::string& nombre() const { return nombre_; }

                  private:
                      std::string nombre_;
                  };

                  class Quimera {
                  public:
                      Quimera()
                      {
                          formas_.push_back(std::make_unique<Forma>("leon"));
                          formas_.push_back(std::make_unique<Forma>("cabra"));
                          formas_.push_back(std::make_unique<Forma>("serpiente"));
                      }
                      const Forma& forma_del_turno(int t) const
                      {
                          return *formas_[0];
                      }

                  private:
                      std::vector<std::unique_ptr<Forma>> formas_;
                  };

                  int main()
                  {
                      Quimera q;
                      for (int t = 0; t < 5; t++) {
                          std::cout << "Turno " << t + 1 << ": " << q.forma_del_turno(t).nombre() << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <memory>
                  #include <string>
                  #include <vector>

                  class Forma {
                  public:
                      explicit Forma(std::string n) : nombre_(n) {}
                      const std::string& nombre() const { return nombre_; }

                  private:
                      std::string nombre_;
                  };

                  class Quimera {
                  public:
                      Quimera()
                      {
                          formas_.push_back(std::make_unique<Forma>("leon"));
                          formas_.push_back(std::make_unique<Forma>("cabra"));
                          formas_.push_back(std::make_unique<Forma>("serpiente"));
                      }
                      const Forma& forma_del_turno(int t) const
                      {
                          return *formas_[t % formas_.size()];
                      }

                  private:
                      std::vector<std::unique_ptr<Forma>> formas_;
                  };

                  int main()
                  {
                      Quimera q;
                      for (int t = 0; t < 5; t++) {
                          std::cout << "Turno " << t + 1 << ": " << q.forma_del_turno(t).nombre() << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="León, cabra, serpiente, león, cabra. Bron ya sabe qué va a ser antes de que la Quimera lo sepa.",
              imagen=[QUIMERA + " a mitad de un cambio de forma, con las piezas en el aire.",
                      BRON + " cuenta los turnos con los dedos.", LIMA + " grita desde la tribuna."]),
            m(id="R02-N09-P3", titulo="El golpe justo",
              lugar=ARENA, personajes="Bron, Tesla",
              criatura="dragon",
              carta="Elegir sin preguntar | cada forma sabe qué la lastima (virtual mejor_golpe()) · el combate no pregunta el tipo: le pide a la forma",
              recompensa="xp 15, oro 15",
              escena="""
                  Bron sigue preguntando «¿sos león?», «¿sos cabra?» con una cadena de `if`. Tesla le borra los `if`: —Que cada forma **responda** cuál es su punto débil.
              """,
              sugiere="Cada forma ya tiene `mejor_golpe()`. En el combate, usá `f.mejor_golpe()` en lugar de preguntar el nombre. La vida baja 20 por golpe justo.",
              desafio="Usá el método de cada forma en lugar de la cadena de `if`.",
              inicial='''
                  #include <iostream>
                  #include <memory>
                  #include <string>
                  #include <vector>

                  class Forma {
                  public:
                      virtual ~Forma() = default;
                      virtual std::string nombre() const = 0;
                      virtual std::string mejor_golpe() const = 0;
                  };

                  class Leon : public Forma {
                  public:
                      std::string nombre() const override { return "leon"; }
                      std::string mejor_golpe() const override { return "red"; }
                  };

                  class Cabra : public Forma {
                  public:
                      std::string nombre() const override { return "cabra"; }
                      std::string mejor_golpe() const override { return "palanca"; }
                  };

                  class Serpiente : public Forma {
                  public:
                      std::string nombre() const override { return "serpiente"; }
                      std::string mejor_golpe() const override { return "llave"; }
                  };

                  int main()
                  {
                      std::vector<std::unique_ptr<Forma>> formas;
                      formas.push_back(std::make_unique<Leon>());
                      formas.push_back(std::make_unique<Cabra>());
                      formas.push_back(std::make_unique<Serpiente>());
                      int vida = 60;
                      for (int t = 0; vida > 0; t++) {
                          const Forma& f = *formas[t % formas.size()];
                          std::string golpe = "llave";
                          if (f.nombre() == "leon") {
                              golpe = "llave";
                          }
                          vida -= 20;
                          std::cout << f.nombre() << " recibe " << golpe << ", le queda " << vida << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <memory>
                  #include <string>
                  #include <vector>

                  class Forma {
                  public:
                      virtual ~Forma() = default;
                      virtual std::string nombre() const = 0;
                      virtual std::string mejor_golpe() const = 0;
                  };

                  class Leon : public Forma {
                  public:
                      std::string nombre() const override { return "leon"; }
                      std::string mejor_golpe() const override { return "red"; }
                  };

                  class Cabra : public Forma {
                  public:
                      std::string nombre() const override { return "cabra"; }
                      std::string mejor_golpe() const override { return "palanca"; }
                  };

                  class Serpiente : public Forma {
                  public:
                      std::string nombre() const override { return "serpiente"; }
                      std::string mejor_golpe() const override { return "llave"; }
                  };

                  int main()
                  {
                      std::vector<std::unique_ptr<Forma>> formas;
                      formas.push_back(std::make_unique<Leon>());
                      formas.push_back(std::make_unique<Cabra>());
                      formas.push_back(std::make_unique<Serpiente>());
                      int vida = 60;
                      for (int t = 0; vida > 0; t++) {
                          const Forma& f = *formas[t % formas.size()];
                          std::string golpe = f.mejor_golpe();
                          vida -= 20;
                          std::cout << f.nombre() << " recibe " << golpe << ", le queda " << vida << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Red al león, palanca a la cabra, llave a la serpiente. La Quimera se tambalea.",
              imagen=[QUIMERA + " tambaleándose en la Arena.",
                      BRON + " golpea con la llave a la cola de serpiente.", TESLA + " mira desde la tribuna, con el visor bajado."]),
            m(id="R02-N09-P4", titulo="La llave que se ajusta",
              lugar=ARENA, personajes="Bron, Tesla, Lima",
              criatura="dragon",
              carta="Constructor con parámetros | Llave(int medida) · una sola clase, muchas llaves · lo que cambia entra por el constructor",
              recompensa="xp 25, oro 30",
              item="Llave Ajustable",
              escena="""
                  La Quimera cae, y las piezas de bronce quedan quietas en la arena. Tesla le pide a Bron la llave mellada, le agrega una tuerca que se corre, y se la devuelve. —Una llave que sirve para muchas tuercas. Como un buen constructor.
                  Para probarla, Bron escribe la clase: pero el constructor ignora la medida y todas las llaves salen de 10.
              """,
              sugiere="El constructor tiene que guardar la medida que recibe: `: medida_(medida)`.",
              desafio="Hacé que cada llave tenga la medida que se le pide.",
              inicial='''
                  #include <iostream>
                  #include <vector>

                  class Llave {
                  public:
                      explicit Llave(int medida) : medida_(10) {}
                      bool encaja(int tuerca) const { return tuerca == medida_; }
                      int medida() const { return medida_; }

                  private:
                      int medida_;
                  };

                  int main()
                  {
                      std::vector<int> tuercas = {8, 13, 10, 19};
                      for (int t : tuercas) {
                          Llave ajustada(t);
                          std::cout << "Tuerca " << t << ": llave de " << ajustada.medida()
                                    << (ajustada.encaja(t) ? ", encaja" : ", no encaja") << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <vector>

                  class Llave {
                  public:
                      explicit Llave(int medida) : medida_(medida) {}
                      bool encaja(int tuerca) const { return tuerca == medida_; }
                      int medida() const { return medida_; }

                  private:
                      int medida_;
                  };

                  int main()
                  {
                      std::vector<int> tuercas = {8, 13, 10, 19};
                      for (int t : tuercas) {
                          Llave ajustada(t);
                          std::cout << "Tuerca " << t << ": llave de " << ajustada.medida()
                                    << (ajustada.encaja(t) ? ", encaja" : ", no encaja") << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Cuatro tuercas, cuatro medidas, una sola llave: **la Llave Ajustable**. Bron la levanta como un trofeo. Para algunos aprendices de la Ciudadela, el camino de las clases termina acá; Bron sigue subiendo.",
              imagen=["Las piezas de bronce de la Quimera quietas en la arena.",
                      BRON + " levanta una llave inglesa cian con una tuerca de bronce que se corre.", TESLA + " y " + LIMA + " aplauden."]),
        ],
    },
]
