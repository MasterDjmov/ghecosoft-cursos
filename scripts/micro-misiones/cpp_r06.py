from gencpp import m
from cpp_r01 import BRON, TESLA, LIMA, LYN, OTO, GHECO
from cpp_r03 import MAESTRA

VITRALES = "El Taller de los Vitrales"
INSCRIPCIONES = "La oficina de inscripciones"
PATENTES = "La oficina de patentes"
VIDRIERO = "El fondo del Taller de los Vitrales"
GARGOLA_LUGAR = "Lo alto del Taller de los Vitrales"
GARGOLA = "la Gárgola de los Vitrales (gárgola de piedra gris con alas cortas, monóculo de vidrios de colores y una pluma de escribir en la garra)"
SIN_VENTANA = "Acá se prueba la lógica sin ventana (Qt no corre en el navegador): es lo mismo que pasa por dentro de Qt."

NODOS = [
    {
        "titulo": "R06-N01 · Los Vitrales: ventanas, señales y slots",
        "misiones": [
            m(id="R06-N01-P1", titulo="La campana de la palanca",
              lugar=VITRALES, personajes="Bron, Tesla",
              carta="Señal y slot | una señal es una lista de funciones conectadas · emitir = llamar a todas · en Qt: connect(boton, &QPushButton::clicked, ...)",
              recompensa="xp 10, oro 10",
              escena="""
                  En el Taller de los Vitrales las ventanas **esperan**: cuando alguien toca una palanca, suena una campana y el código responde. Bron armó su propio botón para entender cómo funciona, pero al tocarlo no responde nadie.
              """,
              sugiere="Cuando hacen clic, el botón tiene que **emitir** su señal: recorrer `conectados_` y llamar a cada función. " + SIN_VENTANA,
              desafio="Hacé que el clic llame a todo lo conectado.",
              inicial='''
                  #include <functional>
                  #include <iostream>
                  #include <vector>

                  class Boton {
                  public:
                      void conectar(std::function<void()> slot) { conectados_.push_back(slot); }
                      void click()
                      {
                          std::cout << "click!\\n";
                      }

                  private:
                      std::vector<std::function<void()>> conectados_;
                  };

                  int main()
                  {
                      Boton palanca;
                      int contador = 0;
                      palanca.conectar([&contador] { contador++; std::cout << "el contador sube a " << contador << "\\n"; });
                      palanca.conectar([] { std::cout << "suena la campana\\n"; });
                      palanca.click();
                      palanca.click();
                      return 0;
                  }
              ''',
              solucion='''
                  #include <functional>
                  #include <iostream>
                  #include <vector>

                  class Boton {
                  public:
                      void conectar(std::function<void()> slot) { conectados_.push_back(slot); }
                      void click()
                      {
                          std::cout << "click!\\n";
                          for (const auto& slot : conectados_) {
                              slot();
                          }
                      }

                  private:
                      std::vector<std::function<void()>> conectados_;
                  };

                  int main()
                  {
                      Boton palanca;
                      int contador = 0;
                      palanca.conectar([&contador] { contador++; std::cout << "el contador sube a " << contador << "\\n"; });
                      palanca.conectar([] { std::cout << "suena la campana\\n"; });
                      palanca.click();
                      palanca.click();
                      return 0;
                  }
              ''',
              al_superar="Cada clic sube el contador y suena la campana. Bron aprieta todos los botones de un vitral a la vez, para ver qué pasa, y suenan todas las campanas del taller.",
              imagen=["Un vitral con palancas y una campana de bronce que suena.",
                      BRON + " aprieta varias palancas a la vez.", TESLA + " se tapa los oídos."]),
            m(id="R06-N01-P2", titulo="Avisar solo si cambió",
              lugar=VITRALES, personajes="Lima, Bron",
              carta="valueChanged | un QSpinBox emite valueChanged(int) SOLO si el valor cambia · así nadie trabaja de más",
              recompensa="xp 10, oro 10",
              escena="""
                  El selector de presión de Lima avisa a la etiqueta cada vez que alguien lo toca, aunque ponga el mismo número. La etiqueta se redibuja de más, y Lima se impacienta: así no avisa un `QSpinBox`.
              """,
              sugiere="En `poner`, si el valor nuevo es igual al actual, no hagas nada. Si cambió, guardalo y avisá.",
              desafio="Avisá solo cuando el valor cambia.",
              inicial='''
                  #include <functional>
                  #include <iostream>

                  class Selector {
                  public:
                      std::function<void(int)> valor_cambiado;
                      void poner(int v)
                      {
                          valor_ = v;
                          if (valor_cambiado) {
                              valor_cambiado(valor_);
                          }
                      }

                  private:
                      int valor_ = 0;
                  };

                  int main()
                  {
                      Selector presion;
                      int avisos = 0;
                      presion.valor_cambiado = [&avisos](int v) { avisos++; std::cout << "etiqueta: " << v << "\\n"; };
                      for (int v : {40, 40, 55, 55, 55, 70}) {
                          presion.poner(v);
                      }
                      std::cout << "Avisos: " << avisos << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <functional>
                  #include <iostream>

                  class Selector {
                  public:
                      std::function<void(int)> valor_cambiado;
                      void poner(int v)
                      {
                          if (v == valor_) {
                              return;
                          }
                          valor_ = v;
                          if (valor_cambiado) {
                              valor_cambiado(valor_);
                          }
                      }

                  private:
                      int valor_ = 0;
                  };

                  int main()
                  {
                      Selector presion;
                      int avisos = 0;
                      presion.valor_cambiado = [&avisos](int v) { avisos++; std::cout << "etiqueta: " << v << "\\n"; };
                      for (int v : {40, 40, 55, 55, 55, 70}) {
                          presion.poner(v);
                      }
                      std::cout << "Avisos: " << avisos << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres avisos en vez de seis. La etiqueta descansa, y Lima también.",
              imagen=["Un selector giratorio de bronce conectado por un cable a una etiqueta luminosa.",
                      LIMA + " gira el selector.", BRON + " cuenta los destellos de la etiqueta."]),
            m(id="R06-N01-P3", titulo="Desconectar la campana",
              lugar=VITRALES, personajes="Bron, Oto",
              carta="Desconectar | connect devuelve un identificador · con él se desconecta (QObject::disconnect) · después de desconectar, ese slot no se llama más",
              recompensa="xp 15, oro 15",
              escena="""
                  La palanca del comedor toca la campana de Oto y prende la luz. De noche, Oto quiere que la palanca prenda la luz **sin** tocar la campana. Bron escribió `desconectar`, pero no saca nada.
              """,
              sugiere="Cada conexión tiene un número. En `desconectar(id)`, borrá del mapa la conexión con ese número: `conectados_.erase(id);`.",
              desafio="Hacé que `desconectar` saque la conexión.",
              inicial='''
                  #include <functional>
                  #include <iostream>
                  #include <map>

                  class Palanca {
                  public:
                      int conectar(std::function<void()> slot)
                      {
                          conectados_[siguiente_] = slot;
                          return siguiente_++;
                      }
                      void desconectar(int id)
                      {
                          std::cout << "(desconecto " << id << ")\\n";
                      }
                      void tirar()
                      {
                          for (const auto& [id, slot] : conectados_) {
                              slot();
                          }
                      }

                  private:
                      std::map<int, std::function<void()>> conectados_;
                      int siguiente_ = 1;
                  };

                  int main()
                  {
                      Palanca p;
                      int campana = p.conectar([] { std::cout << "tolon tolon\\n"; });
                      p.conectar([] { std::cout << "se prende la luz\\n"; });
                      p.tirar();
                      p.desconectar(campana);
                      p.tirar();
                      return 0;
                  }
              ''',
              solucion='''
                  #include <functional>
                  #include <iostream>
                  #include <map>

                  class Palanca {
                  public:
                      int conectar(std::function<void()> slot)
                      {
                          conectados_[siguiente_] = slot;
                          return siguiente_++;
                      }
                      void desconectar(int id)
                      {
                          std::cout << "(desconecto " << id << ")\\n";
                          conectados_.erase(id);
                      }
                      void tirar()
                      {
                          for (const auto& [id, slot] : conectados_) {
                              slot();
                          }
                      }

                  private:
                      std::map<int, std::function<void()>> conectados_;
                      int siguiente_ = 1;
                  };

                  int main()
                  {
                      Palanca p;
                      int campana = p.conectar([] { std::cout << "tolon tolon\\n"; });
                      p.conectar([] { std::cout << "se prende la luz\\n"; });
                      p.tirar();
                      p.desconectar(campana);
                      p.tirar();
                      return 0;
                  }
              ''',
              al_superar="De noche, la palanca prende la luz y la campana no suena. Oto duerme por primera vez en semanas.",
              imagen=["Una palanca con dos cables: uno a una campana (cortado) y otro a una lámpara encendida.",
                      OTO + " durmiendo con el gorro puesto.", BRON + " corta un cable con una pinza."]),
        ],
    },
    {
        "titulo": "R06-N02 · Formularios, menús y archivos",
        "misiones": [
            m(id="R06-N02-P1", titulo="Todos los errores juntos",
              lugar=INSCRIPCIONES, personajes="Lyn, Bron",
              carta="Validar | revisá TODO lo que escribió el usuario y juntá los errores en una lista · mostrarlos juntos (en Qt, un QMessageBox con la QStringList)",
              recompensa="xp 10, oro 10",
              escena="""
                  Lyn se inscribe en la carrera y el formulario le avisa un error. Lo corrige, y le avisa otro. Y otro. Lyn le apuesta a la ventanita que la próxima vez se acuerda de todo; pierde, porque la ventanita le muestra los errores de a uno.
              """,
              sugiere="En lugar de cortar con `return` en el primer error, agregá cada error a la lista `errores` y seguí revisando.",
              desafio="Juntá todos los errores antes de avisar.",
              inicial='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  std::vector<std::string> validar(const std::string& nombre, int edad, const std::string& torre)
                  {
                      std::vector<std::string> errores;
                      if (nombre.empty()) {
                          errores.push_back("falta el nombre");
                          return errores;
                      }
                      if (edad < 10 || edad > 99) {
                          errores.push_back("la edad tiene que estar entre 10 y 99");
                          return errores;
                      }
                      if (torre.empty()) {
                          errores.push_back("elegi una torre");
                      }
                      return errores;
                  }

                  int main()
                  {
                      std::vector<std::string> errores = validar("", 7, "");
                      std::cout << errores.size() << " errores:\\n";
                      for (const auto& e : errores) {
                          std::cout << "- " << e << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  std::vector<std::string> validar(const std::string& nombre, int edad, const std::string& torre)
                  {
                      std::vector<std::string> errores;
                      if (nombre.empty()) {
                          errores.push_back("falta el nombre");
                      }
                      if (edad < 10 || edad > 99) {
                          errores.push_back("la edad tiene que estar entre 10 y 99");
                      }
                      if (torre.empty()) {
                          errores.push_back("elegi una torre");
                      }
                      return errores;
                  }

                  int main()
                  {
                      std::vector<std::string> errores = validar("", 7, "");
                      std::cout << errores.size() << " errores:\\n";
                      for (const auto& e : errores) {
                          std::cout << "- " << e << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Tres errores de una vez. Lyn los corrige todos juntos y se inscribe primera, por supuesto.",
              imagen=["Una ventanita de aviso con tres renglones de errores.",
                      LYN + " completa el formulario a toda velocidad.", BRON + " sostiene el vitral."]),
            m(id="R06-N02-P2", titulo="Borrar de atrás para adelante",
              lugar=INSCRIPCIONES, personajes="Bron, Lima",
              carta="Borrar varios | al borrar el lugar i, los de atrás se corren uno · si se borra de adelante para atrás, se borra el equivocado · se recorre al revés",
              recompensa="xp 15, oro 15",
              escena="""
                  En la lista de inscriptos, Lima marcó dos para borrar: los lugares 1 y 3. Bron los borra en ese orden, y se va el que no era: al borrar el 1, todos los de atrás se corrieron un lugar.
              """,
              sugiere="Recorré los lugares marcados de **atrás para adelante** (el 3 primero, después el 1): así los que todavía faltan no se mueven.",
              desafio="Borrá en el orden que no corre a nadie.",
              inicial='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::string> inscriptos = {"Bron", "Lyn", "Oto", "Lima", "Tesla"};
                      std::vector<int> marcados = {1, 3};
                      for (std::size_t k = 0; k < marcados.size(); k++) {
                          inscriptos.erase(inscriptos.begin() + marcados[k]);
                      }
                      std::cout << "Quedan:";
                      for (const auto& n : inscriptos) {
                          std::cout << " " << n;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::string> inscriptos = {"Bron", "Lyn", "Oto", "Lima", "Tesla"};
                      std::vector<int> marcados = {1, 3};
                      for (auto it = marcados.rbegin(); it != marcados.rend(); ++it) {
                          inscriptos.erase(inscriptos.begin() + *it);
                      }
                      std::cout << "Quedan:";
                      for (const auto& n : inscriptos) {
                          std::cout << " " << n;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Se van Lyn y Lima, las marcadas (ya estaban inscriptas en otra carrera). Tesla sigue en la lista, que es lo que corresponde.",
              imagen=["Una lista de nombres en un vitral, con dos renglones tachados.",
                      LIMA + " marca dos nombres.", BRON + " tacha de abajo hacia arriba."]),
            m(id="R06-N02-P3", titulo="Nombres con espacios",
              lugar=INSCRIPCIONES, personajes="Bron, Oto",
              carta="Guardar un formulario | una línea por inscripto, con los campos separados por ; · al leer, getline(campos, texto, ';') respeta los espacios",
              recompensa="xp 15, oro 15",
              escena="""
                  El formulario guarda a cada inscripto en una línea: `nombre;edad;torre`. Oto se inscribe como «Oto el Grande», y al cargar el archivo, el programa de Bron lo parte en pedazos.
              """,
              sugiere="Leé cada línea con `std::getline` y partila por `;` con `std::getline(campos, nombre, ';')`, que no corta en los espacios.",
              desafio="Leé los campos respetando los espacios.",
              inicial='''
                  #include <fstream>
                  #include <iostream>
                  #include <sstream>
                  #include <string>

                  int main()
                  {
                      {
                          std::ofstream f("inscriptos.txt");
                          f << "Oto el Grande;40;comedor\\n";
                          f << "Lyn;19;torre del reloj\\n";
                      }
                      std::ifstream in("inscriptos.txt");
                      std::string nombre;
                      int n = 0;
                      while (in >> nombre) {
                          std::cout << ++n << ". " << nombre << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <fstream>
                  #include <iostream>
                  #include <sstream>
                  #include <string>

                  int main()
                  {
                      {
                          std::ofstream f("inscriptos.txt");
                          f << "Oto el Grande;40;comedor\\n";
                          f << "Lyn;19;torre del reloj\\n";
                      }
                      std::ifstream in("inscriptos.txt");
                      std::string linea;
                      int n = 0;
                      while (std::getline(in, linea)) {
                          std::istringstream campos(linea);
                          std::string nombre, edad, torre;
                          std::getline(campos, nombre, ';');
                          std::getline(campos, edad, ';');
                          std::getline(campos, torre);
                          std::cout << ++n << ". " << nombre << " (" << edad << ") - " << torre << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="«Oto el Grande», entero, y «torre del reloj» también. Oto pide que lo anoten así en todos lados.",
              imagen=["Un archivo de fichas con una que dice «Oto el Grande».",
                      OTO + " señala su ficha con el cucharón.", BRON + " la archiva."]),
        ],
    },
    {
        "titulo": "R06-N03 · Tu clase detrás de la ventana",
        "misiones": [
            m(id="R06-N03-P1", titulo="La fábrica de inventos",
              lugar=PATENTES, personajes="Bron, Tesla",
              carta="Fábrica | std::unique_ptr<Invento> crear(const std::string& tipo, ...) · el ÚNICO lugar que conoce todas las derivadas · un tipo nuevo se agrega ahí",
              recompensa="xp 10, oro 10",
              escena="""
                  En la oficina de patentes, el combo de la ventana ya ofrece «farol», pero la fábrica de Bron no lo conoce y devuelve nada. El empleado escribe «tipo desconocido» con cara de pena.
              """,
              sugiere="Agregá en `crear` el caso `\"farol\"`, que devuelva un `std::make_unique<Farol>(nombre)`.",
              desafio="Enseñale a la fábrica a crear faroles.",
              inicial='''
                  #include <iostream>
                  #include <memory>
                  #include <string>

                  class Invento {
                  public:
                      explicit Invento(std::string n) : nombre_(n) {}
                      virtual ~Invento() = default;
                      virtual std::string tipo() const = 0;
                      const std::string& nombre() const { return nombre_; }

                  private:
                      std::string nombre_;
                  };

                  class Reloj : public Invento {
                  public:
                      using Invento::Invento;
                      std::string tipo() const override { return "reloj"; }
                  };

                  class Farol : public Invento {
                  public:
                      using Invento::Invento;
                      std::string tipo() const override { return "farol"; }
                  };

                  std::unique_ptr<Invento> crear(const std::string& tipo, const std::string& nombre)
                  {
                      if (tipo == "reloj") {
                          return std::make_unique<Reloj>(nombre);
                      }
                      return nullptr;
                  }

                  int main()
                  {
                      for (auto [tipo, nombre] : {std::pair<std::string, std::string>{"reloj", "Cucu"}, {"farol", "Lucero"}, {"barco", "Ancla"}}) {
                          auto i = crear(tipo, nombre);
                          if (i) {
                              std::cout << "Registrado: " << i->tipo() << " " << i->nombre() << "\\n";
                          } else {
                              std::cout << "Tipo desconocido: " << tipo << "\\n";
                          }
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <memory>
                  #include <string>

                  class Invento {
                  public:
                      explicit Invento(std::string n) : nombre_(n) {}
                      virtual ~Invento() = default;
                      virtual std::string tipo() const = 0;
                      const std::string& nombre() const { return nombre_; }

                  private:
                      std::string nombre_;
                  };

                  class Reloj : public Invento {
                  public:
                      using Invento::Invento;
                      std::string tipo() const override { return "reloj"; }
                  };

                  class Farol : public Invento {
                  public:
                      using Invento::Invento;
                      std::string tipo() const override { return "farol"; }
                  };

                  std::unique_ptr<Invento> crear(const std::string& tipo, const std::string& nombre)
                  {
                      if (tipo == "reloj") {
                          return std::make_unique<Reloj>(nombre);
                      }
                      if (tipo == "farol") {
                          return std::make_unique<Farol>(nombre);
                      }
                      return nullptr;
                  }

                  int main()
                  {
                      for (auto [tipo, nombre] : {std::pair<std::string, std::string>{"reloj", "Cucu"}, {"farol", "Lucero"}, {"barco", "Ancla"}}) {
                          auto i = crear(tipo, nombre);
                          if (i) {
                              std::cout << "Registrado: " << i->tipo() << " " << i->nombre() << "\\n";
                          } else {
                              std::cout << "Tipo desconocido: " << tipo << "\\n";
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="El farol Lucero queda registrado. El barco no: en la Ciudadela no hay mar.",
              imagen=["Un mostrador de patentes con un farol, un reloj cucú y un barquito de juguete rechazado.",
                      TESLA + " sella una patente.", BRON + " sostiene el barquito."]),
            m(id="R06-N03-P2", titulo="Una sola verdad",
              lugar=PATENTES, personajes="Bron, la Maestra Artífice",
              carta="refrescar() | los datos viven SOLO en el modelo · la tabla se vuelve a llenar desde el modelo después de cada cambio · nunca dos copias",
              recompensa="xp 15, oro 15",
              escena="""
                  El empleado de patentes borra un invento de la tabla de la ventana… y el total sigue igual, porque en el registro el invento sigue estando. Dos verdades. La Maestra Artífice pasa y pregunta: —¿Y la prueba? —La prueba es el total, y no da.
              """,
              sugiere="Borrá del **modelo** (`registro.quitar(fila)`) y después rehacé la tabla con `refrescar`, en lugar de borrar solo de `tabla`.",
              desafio="Hacé que la tabla y el modelo digan lo mismo.",
              inicial='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  struct Invento {
                      std::string nombre;
                      int valor;
                  };

                  class Registro {
                  public:
                      void agregar(const Invento& i) { inventos_.push_back(i); }
                      void quitar(int fila) { inventos_.erase(inventos_.begin() + fila); }
                      const std::vector<Invento>& todos() const { return inventos_; }
                      int total() const
                      {
                          int t = 0;
                          for (const auto& i : inventos_) t += i.valor;
                          return t;
                      }

                  private:
                      std::vector<Invento> inventos_;
                  };

                  std::vector<std::string> refrescar(const Registro& r)
                  {
                      std::vector<std::string> tabla;
                      for (const auto& i : r.todos()) {
                          tabla.push_back(i.nombre + " $" + std::to_string(i.valor));
                      }
                      return tabla;
                  }

                  int main()
                  {
                      Registro registro;
                      registro.agregar({"Cucu", 124});
                      registro.agregar({"Pinza", 260});
                      registro.agregar({"Lucero", 125});
                      std::vector<std::string> tabla = refrescar(registro);
                      tabla.erase(tabla.begin() + 1);
                      for (const auto& fila : tabla) {
                          std::cout << fila << "\\n";
                      }
                      std::cout << "Total: $" << registro.total() << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  struct Invento {
                      std::string nombre;
                      int valor;
                  };

                  class Registro {
                  public:
                      void agregar(const Invento& i) { inventos_.push_back(i); }
                      void quitar(int fila) { inventos_.erase(inventos_.begin() + fila); }
                      const std::vector<Invento>& todos() const { return inventos_; }
                      int total() const
                      {
                          int t = 0;
                          for (const auto& i : inventos_) t += i.valor;
                          return t;
                      }

                  private:
                      std::vector<Invento> inventos_;
                  };

                  std::vector<std::string> refrescar(const Registro& r)
                  {
                      std::vector<std::string> tabla;
                      for (const auto& i : r.todos()) {
                          tabla.push_back(i.nombre + " $" + std::to_string(i.valor));
                      }
                      return tabla;
                  }

                  int main()
                  {
                      Registro registro;
                      registro.agregar({"Cucu", 124});
                      registro.agregar({"Pinza", 260});
                      registro.agregar({"Lucero", 125});
                      registro.quitar(1);
                      std::vector<std::string> tabla = refrescar(registro);
                      for (const auto& fila : tabla) {
                          std::cout << fila << "\\n";
                      }
                      std::cout << "Total: $" << registro.total() << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Doscientos cuarenta y nueve, en la tabla y en el registro. La Maestra Artífice tilda la oficina de patentes.",
              imagen=["Una tabla en un vitral y un libro de registro al lado, con los mismos renglones.",
                      MAESTRA + " compara la tabla con el libro.", BRON + " borra un renglón del libro."]),
            m(id="R06-N03-P3", titulo="Cuando no hay nada elegido",
              lugar=PATENTES, personajes="Bron, Lima",
              carta="currentRow() | devuelve -1 si no hay ninguna fila elegida · antes de usarla, se revisa fila < 0",
              recompensa="xp 10, oro 10",
              escena="""
                  El empleado aprieta «Quitar» sin elegir ninguna fila. La tabla le pasa −1, y el programa de Bron revienta buscando el invento número −1.
              """,
              sugiere="Revisá también que `fila` no sea negativa: si `fila < 0`, mostrá `Elegi un invento` y no hagas nada.",
              desafio="Cuidate del −1.",
              inicial='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  std::vector<std::string> inventos = {"Cucu", "Pinza", "Lucero"};

                  void quitar(int fila)
                  {
                      if (fila >= static_cast<int>(inventos.size())) {
                          std::cout << "No existe esa fila\\n";
                          return;
                      }
                      std::cout << "Quitado: " << inventos.at(fila) << "\\n";
                      inventos.erase(inventos.begin() + fila);
                  }

                  int main()
                  {
                      quitar(1);
                      quitar(-1);
                      quitar(5);
                      std::cout << "Quedan " << inventos.size() << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  std::vector<std::string> inventos = {"Cucu", "Pinza", "Lucero"};

                  void quitar(int fila)
                  {
                      if (fila < 0) {
                          std::cout << "Elegi un invento\\n";
                          return;
                      }
                      if (fila >= static_cast<int>(inventos.size())) {
                          std::cout << "No existe esa fila\\n";
                          return;
                      }
                      std::cout << "Quitado: " << inventos.at(fila) << "\\n";
                      inventos.erase(inventos.begin() + fila);
                  }

                  int main()
                  {
                      quitar(1);
                      quitar(-1);
                      quitar(5);
                      std::cout << "Quedan " << inventos.size() << "\\n";
                      return 0;
                  }
              ''',
              al_superar="El empleado aprieta «Quitar» sin elegir, y la ventana le pide que elija. Nadie revienta.",
              imagen=["Un vitral con una tabla sin ninguna fila elegida y un cartelito amable.",
                      LIMA + " señala el cartelito.", BRON + " aprieta el botón «Quitar»."]),
        ],
    },
    {
        "titulo": "R06-N04 · Dibujar, el mouse y el modelo-vista",
        "misiones": [
            m(id="R06-N04-P1", titulo="¿En qué baldosa hizo clic?",
              lugar=VIDRIERO, personajes="Bron, Lima",
              carta="Del mouse a la grilla | columna = x / tam · fila = y / tam (con enteros) · x es horizontal, y es vertical",
              recompensa="xp 10, oro 10",
              escena="""
                  El maestro vidriero pinta cada vitral a mano, baldosa por baldosa. Bron quiere saber en qué baldosa hizo clic, y confunde las coordenadas: pinta la fila donde iba la columna.
              """,
              sugiere="`x` es la posición horizontal (la columna) e `y` la vertical (la fila). Las baldosas miden `tam` píxeles.",
              desafio="Calculá bien la fila y la columna.",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      const int tam = 32;
                      int clics[][2] = {{40, 100}, {200, 10}, {0, 0}};
                      for (const auto& c : clics) {
                          int x = c[0];
                          int y = c[1];
                          int fila = x / tam;
                          int columna = y / tam;
                          std::cout << "clic (" << x << ", " << y << ") -> fila " << fila << ", columna " << columna << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      const int tam = 32;
                      int clics[][2] = {{40, 100}, {200, 10}, {0, 0}};
                      for (const auto& c : clics) {
                          int x = c[0];
                          int y = c[1];
                          int fila = y / tam;
                          int columna = x / tam;
                          std::cout << "clic (" << x << ", " << y << ") -> fila " << fila << ", columna " << columna << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Cada clic cae en su baldosa. Bron le pregunta al maestro vidriero si conoce al Vidriero. —Todos lo conocemos —se ríe—. Nadie lo vio nunca.",
              imagen=["Un vitral a medio pintar dividido en baldosas, con una iluminada donde cayó el clic.",
                      BRON + " sostiene un pincel de luz.", LIMA + " anota coordenadas."]),
            m(id="R06-N04-P2", titulo="El reloj de la torre",
              lugar=VIDRIERO, personajes="Tesla, Bron",
              carta="Animar con un timer | en Qt, un QTimer llama a un slot cada tantos milisegundos · el slot cambia el estado y pide update() · el ángulo vuelve a 0 con % 360",
              recompensa="xp 10, oro 10",
              escena="""
                  El reloj dibujado de la torre avanza la aguja 6 grados en cada tic del timer. Después de un minuto, la aguja de Bron marca 366 grados, y el dibujo se tuerce.
              """,
              sugiere="Después de sumar, quedate con el resto de dividir por 360: `angulo_ = (angulo_ + 6) % 360;`.",
              desafio="Hacé que la aguja dé la vuelta.",
              inicial='''
                  #include <iostream>

                  class Aguja {
                  public:
                      void tic() { angulo_ = angulo_ + 6; }
                      int angulo() const { return angulo_; }

                  private:
                      int angulo_ = 342;
                  };

                  int main()
                  {
                      Aguja a;
                      for (int i = 0; i < 5; i++) {
                          a.tic();
                          std::cout << "tic " << i + 1 << ": " << a.angulo() << " grados\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  class Aguja {
                  public:
                      void tic() { angulo_ = (angulo_ + 6) % 360; }
                      int angulo() const { return angulo_; }

                  private:
                      int angulo_ = 342;
                  };

                  int main()
                  {
                      Aguja a;
                      for (int i = 0; i < 5; i++) {
                          a.tic();
                          std::cout << "tic " << i + 1 << ": " << a.angulo() << " grados\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Trescientos cuarenta y ocho, trescientos cincuenta y cuatro, cero, seis, doce. La aguja da la vuelta, como un reloj de verdad.",
              imagen=["Un reloj pintado en un vitral, con la aguja pasando por las doce.",
                      TESLA + " mira el reloj con el compás.", BRON + " cuenta los tics."]),
            m(id="R06-N04-P3", titulo="La fila del filtro no es la del modelo",
              lugar=VIDRIERO, personajes="Lima, Bron",
              carta="mapToSource | con un filtro (QSortFilterProxyModel), la fila que se ve NO es la del modelo · se convierte antes de borrar",
              recompensa="xp 15, oro 15",
              escena="""
                  En la agenda, Lima filtra los contactos que tienen una «o» y elige el segundo que se ve. Bron borra la fila 1 del modelo… y se va otro contacto: la fila 1 de la vista no es la fila 1 del modelo.
              """,
              sugiere="El filtro guarda, para cada fila visible, cuál era en el modelo (`visibles`). Borrá `modelo[visibles[1]]`, no `modelo[1]`.",
              desafio="Convertí la fila de la vista a la del modelo antes de borrar.",
              inicial='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::string> modelo = {"Tesla", "Oto", "Lima", "Bron", "Lyn"};
                      std::vector<std::size_t> visibles;
                      for (std::size_t i = 0; i < modelo.size(); i++) {
                          if (modelo[i].find('o') != std::string::npos) {
                              visibles.push_back(i);
                          }
                      }
                      std::size_t elegida = 1;
                      std::cout << "Lima elige: " << modelo[visibles[elegida]] << "\\n";
                      modelo.erase(modelo.begin() + elegida);
                      std::cout << "Quedan:";
                      for (const auto& n : modelo) {
                          std::cout << " " << n;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  int main()
                  {
                      std::vector<std::string> modelo = {"Tesla", "Oto", "Lima", "Bron", "Lyn"};
                      std::vector<std::size_t> visibles;
                      for (std::size_t i = 0; i < modelo.size(); i++) {
                          if (modelo[i].find('o') != std::string::npos) {
                              visibles.push_back(i);
                          }
                      }
                      std::size_t elegida = 1;
                      std::cout << "Lima elige: " << modelo[visibles[elegida]] << "\\n";
                      modelo.erase(modelo.begin() + visibles[elegida]);
                      std::cout << "Quedan:";
                      for (const auto& n : modelo) {
                          std::cout << " " << n;
                      }
                      std::cout << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Se borra Bron (de la agenda, no de la Ciudadela). Bron protesta; Lima dice que fue un ejemplo.",
              imagen=["Una agenda en un vitral, con un filtro que deja ver dos nombres de cinco.",
                      LIMA + " elige un nombre.", BRON + " protesta, señalándose a sí mismo."]),
        ],
    },
    {
        "titulo": "R06-N05 · Jefe final: la Gárgola de los Vitrales",
        "misiones": [
            m(id="R06-N05-P1", titulo="Pregunta número uno: el costo",
              lugar=GARGOLA_LUGAR, personajes="Bron, Lima",
              criatura="dragon",
              carta="Método virtual puro | virtual int costo() const = 0; · cada máquina lo calcula a su manera · Grúa: horas * 8 + toneladas * 50",
              recompensa="xp 15, oro 15",
              escena="""
                  En lo alto del Taller espera la **Gárgola de los Vitrales**, con su monóculo de colores. —Pregunta número uno —dice, con voz de examinadora. Es **TallerExpress**. —Primero los planos —le susurra Lima a Bron—. Después el vitral.
                  A la grúa de Bron le falta su costo de mantenimiento, y el Taller no la deja construir: es abstracta.
              """,
              sugiere="Escribí `int costo() const override` en `Grua`: `horas() * 8 + toneladas_ * 50`.",
              desafio="Completá la grúa.",
              inicial='''
                  #include <iostream>
                  #include <memory>
                  #include <string>
                  #include <vector>

                  class Maquina {
                  public:
                      Maquina(std::string nombre, int horas) : nombre_(nombre), horas_(horas) {}
                      virtual ~Maquina() = default;
                      const std::string& nombre() const { return nombre_; }
                      int horas() const { return horas_; }
                      virtual int costo() const = 0;

                  private:
                      std::string nombre_;
                      int horas_;
                  };

                  class Automata : public Maquina {
                  public:
                      Automata(std::string n, int h, int bateria) : Maquina(n, h), bateria_(bateria) {}
                      int costo() const override { return horas() * 10 + (100 - bateria_) * 2; }

                  private:
                      int bateria_;
                  };

                  class Grua : public Maquina {
                  public:
                      Grua(std::string n, int h, int toneladas) : Maquina(n, h), toneladas_(toneladas) {}

                  private:
                      int toneladas_;
                  };

                  int main()
                  {
                      std::vector<std::unique_ptr<Maquina>> taller;
                      taller.push_back(std::make_unique<Automata>("Cuco", 40, 75));
                      taller.push_back(std::make_unique<Grua>("Brazo", 10, 2));
                      for (const auto& m : taller) {
                          std::cout << m->nombre() << ": $" << m->costo() << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <memory>
                  #include <string>
                  #include <vector>

                  class Maquina {
                  public:
                      Maquina(std::string nombre, int horas) : nombre_(nombre), horas_(horas) {}
                      virtual ~Maquina() = default;
                      const std::string& nombre() const { return nombre_; }
                      int horas() const { return horas_; }
                      virtual int costo() const = 0;

                  private:
                      std::string nombre_;
                      int horas_;
                  };

                  class Automata : public Maquina {
                  public:
                      Automata(std::string n, int h, int bateria) : Maquina(n, h), bateria_(bateria) {}
                      int costo() const override { return horas() * 10 + (100 - bateria_) * 2; }

                  private:
                      int bateria_;
                  };

                  class Grua : public Maquina {
                  public:
                      Grua(std::string n, int h, int toneladas) : Maquina(n, h), toneladas_(toneladas) {}
                      int costo() const override { return horas() * 8 + toneladas_ * 50; }

                  private:
                      int toneladas_;
                  };

                  int main()
                  {
                      std::vector<std::unique_ptr<Maquina>> taller;
                      taller.push_back(std::make_unique<Automata>("Cuco", 40, 75));
                      taller.push_back(std::make_unique<Grua>("Brazo", 10, 2));
                      for (const auto& m : taller) {
                          std::cout << m->nombre() << ": $" << m->costo() << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="—Correcto —dice la Gárgola, y anota algo con su pluma—. Pregunta número dos.",
              imagen=["Lo alto del Taller de los Vitrales con " + GARGOLA + ".",
                      BRON + " dibuja un plano en una hoja.", LIMA + " le susurra al oído."]),
            m(id="R06-N05-P2", titulo="Pregunta número dos: mostrarla",
              lugar=GARGOLA_LUGAR, personajes="Bron, Tesla",
              criatura="dragon",
              carta="friend operator<< | friend std::ostream& operator<<(std::ostream&, const Maquina&) · lee lo privado y llama a lo virtual: sirve para todas",
              recompensa="xp 15, oro 15",
              escena="""
                  —Muestre cualquier máquina con `<<` —pide la Gárgola—. Con el formato del libro: `[codigo] nombre - horas h - $costo`. El operador de Bron lee lo privado sin ser amigo, y el Taller no lo deja.
              """,
              sugiere="Declaralo **amigo** adentro de la clase: `friend std::ostream& operator<<(std::ostream& os, const Maquina& m);`.",
              desafio="Hacé que el operador pueda leer la máquina.",
              inicial='''
                  #include <iostream>
                  #include <string>

                  class Maquina {
                  public:
                      Maquina(int codigo, std::string nombre, int horas) : codigo_(codigo), nombre_(nombre), horas_(horas) {}
                      virtual ~Maquina() = default;
                      virtual int costo() const { return horas_ * 5; }

                  private:
                      int codigo_;
                      std::string nombre_;
                      int horas_;
                  };

                  std::ostream& operator<<(std::ostream& os, const Maquina& m)
                  {
                      return os << "[" << m.codigo_ << "] " << m.nombre_ << " - " << m.horas_ << " h - $" << m.costo();
                  }

                  int main()
                  {
                      Maquina rueca(205, "Rueca", 30);
                      std::cout << rueca << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  class Maquina {
                  public:
                      Maquina(int codigo, std::string nombre, int horas) : codigo_(codigo), nombre_(nombre), horas_(horas) {}
                      virtual ~Maquina() = default;
                      virtual int costo() const { return horas_ * 5; }
                      friend std::ostream& operator<<(std::ostream& os, const Maquina& m);

                  private:
                      int codigo_;
                      std::string nombre_;
                      int horas_;
                  };

                  std::ostream& operator<<(std::ostream& os, const Maquina& m)
                  {
                      return os << "[" << m.codigo_ << "] " << m.nombre_ << " - " << m.horas_ << " h - $" << m.costo();
                  }

                  int main()
                  {
                      Maquina rueca(205, "Rueca", 30);
                      std::cout << rueca << "\\n";
                      return 0;
                  }
              ''',
              al_superar="«[205] Rueca - 30 h - $150.» La Gárgola acomoda el monóculo. —Pregunta número tres.",
              imagen=["La pluma de la Gárgola escribiendo un renglón en un libro enorme.",
                      TESLA + " observa desde la escalera.", BRON + " mira a la Gárgola a los ojos."]),
            m(id="R06-N05-P3", titulo="Pregunta número tres: el desempate",
              lugar=GARGOLA_LUGAR, personajes="Bron, Lima",
              criatura="dragon",
              carta="Orden con desempate | de mayor a menor costo · si empatan, por código de menor a mayor · la lambda compara el costo y, si son iguales, el código",
              recompensa="xp 15, oro 15",
              escena="""
                  —Liste las máquinas de mayor a menor costo —pide la Gárgola—. Y si empatan… —deja la frase en el aire. Bron ordena solo por costo, y las empatadas salen en cualquier orden. La Gárgola carraspea.
              """,
              sugiere="En la lambda: si los costos son distintos, `return a.costo > b.costo;`; si son iguales, `return a.codigo < b.codigo;`.",
              desafio="Desempatá por código.",
              inicial='''
                  #include <algorithm>
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  struct Maquina {
                      int codigo;
                      std::string nombre;
                      int costo;
                  };

                  int main()
                  {
                      std::vector<Maquina> taller = {{310, "Brazo", 180}, {7, "Pluma", 50}, {101, "Cuco", 450}, {3, "Seda", 50}, {205, "Rueca", 180}};
                      std::sort(taller.begin(), taller.end(), [](const Maquina& a, const Maquina& b) { return a.costo > b.costo; });
                      for (const auto& m : taller) {
                          std::cout << "[" << m.codigo << "] " << m.nombre << " $" << m.costo << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <algorithm>
                  #include <iostream>
                  #include <string>
                  #include <vector>

                  struct Maquina {
                      int codigo;
                      std::string nombre;
                      int costo;
                  };

                  int main()
                  {
                      std::vector<Maquina> taller = {{310, "Brazo", 180}, {7, "Pluma", 50}, {101, "Cuco", 450}, {3, "Seda", 50}, {205, "Rueca", 180}};
                      std::sort(taller.begin(), taller.end(), [](const Maquina& a, const Maquina& b) {
                          if (a.costo != b.costo) {
                              return a.costo > b.costo;
                          }
                          return a.codigo < b.codigo;
                      });
                      for (const auto& m : taller) {
                          std::cout << "[" << m.codigo << "] " << m.nombre << " $" << m.costo << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Rueca antes que Brazo, Seda antes que Pluma. La Gárgola deja de carraspear. —Última pregunta.",
              imagen=["Un libro enorme con una lista ordenada y dos pares de renglones unidos por una llave.",
                      LIMA + " señala los empates.", BRON + " escribe la lambda."]),
            m(id="R06-N05-P4", titulo="Pregunta número cuatro: que nada se pierda",
              lugar=GARGOLA_LUGAR, personajes="Bron, Tesla, Lima",
              criatura="dragon",
              carta="Guardar y cargar | una línea por máquina, el tipo primero y los campos separados por ; · al cargar, la fábrica crea la clase que corresponde",
              recompensa="xp 25, oro 30",
              item="Llave Universal",
              escena="""
                  —Guarde el taller y vuélvalo a cargar —dice la Gárgola—. Si se pierde una sola fila, empezamos de nuevo. Bron guarda bien, pero al cargar lee el tipo y el resto en el orden equivocado.
              """,
              sugiere="Al cargar, cada línea es `tipo;codigo;nombre;horas`. Leé los cuatro campos **en ese orden** con `getline(campos, x, ';')`.",
              desafio="Cargá los campos en el orden en que se guardaron.",
              inicial='''
                  #include <fstream>
                  #include <iostream>
                  #include <sstream>
                  #include <string>
                  #include <vector>

                  struct Fila {
                      std::string tipo;
                      int codigo;
                      std::string nombre;
                      int horas;
                  };

                  int main()
                  {
                      std::vector<Fila> taller = {{"automata", 101, "Cuco", 40}, {"telar", 205, "Rueca", 30}, {"grua", 310, "Brazo", 10}};
                      {
                          std::ofstream f("maquinas.txt");
                          for (const Fila& m : taller) {
                              f << m.tipo << ';' << m.codigo << ';' << m.nombre << ';' << m.horas << '\\n';
                          }
                      }
                      std::ifstream in("maquinas.txt");
                      std::string linea;
                      int cargadas = 0;
                      while (std::getline(in, linea)) {
                          std::istringstream campos(linea);
                          std::string tipo, codigo, nombre, horas;
                          std::getline(campos, nombre, ';');
                          std::getline(campos, tipo, ';');
                          std::getline(campos, codigo, ';');
                          std::getline(campos, horas);
                          std::cout << "[" << codigo << "] " << tipo << " " << nombre << " - " << horas << " h\\n";
                          cargadas++;
                      }
                      std::cout << "Cargadas: " << cargadas << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <fstream>
                  #include <iostream>
                  #include <sstream>
                  #include <string>
                  #include <vector>

                  struct Fila {
                      std::string tipo;
                      int codigo;
                      std::string nombre;
                      int horas;
                  };

                  int main()
                  {
                      std::vector<Fila> taller = {{"automata", 101, "Cuco", 40}, {"telar", 205, "Rueca", 30}, {"grua", 310, "Brazo", 10}};
                      {
                          std::ofstream f("maquinas.txt");
                          for (const Fila& m : taller) {
                              f << m.tipo << ';' << m.codigo << ';' << m.nombre << ';' << m.horas << '\\n';
                          }
                      }
                      std::ifstream in("maquinas.txt");
                      std::string linea;
                      int cargadas = 0;
                      while (std::getline(in, linea)) {
                          std::istringstream campos(linea);
                          std::string tipo, codigo, nombre, horas;
                          std::getline(campos, tipo, ';');
                          std::getline(campos, codigo, ';');
                          std::getline(campos, nombre, ';');
                          std::getline(campos, horas);
                          std::cout << "[" << codigo << "] " << tipo << " " << nombre << " - " << horas << " h\\n";
                          cargadas++;
                      }
                      std::cout << "Cargadas: " << cargadas << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres de tres, idénticas. La Gárgola cierra el libro, satisfecha. Bron, que llegó arreglando doscientos engranajes a mano, dibuja en la misma hoja el plano de su propia llave, una que se ajusta a **cualquier** tuerca. Tesla la construye en el torno: **la Llave Universal**. Detrás de la Gárgola, el último vitral muestra un balcón con cuatro portales; uno es un engranaje, el que Bron tiene en el bolsillo.",
              imagen=["Un vitral enorme detrás de la Gárgola con un balcón y cuatro portales: una espiral, un engranaje, un vitral y un arco de fuego.",
                      BRON + " levanta una llave inglesa legendaria de bronce y cian.", TESLA + " y " + LIMA + " miran el vitral."]),
        ],
    },
    {
        "titulo": "S01-N01 · La Linterna Mágica: ventana y bucle",
        "misiones": [
            m(id="S01-N01-P1", titulo="Los milisegundos de la linterna",
              lugar="La sala de la Linterna Mágica", personajes="Bron, Tesla",
              carta="dt en segundos | SDL da el tiempo en milisegundos (enteros) · dt = (ahora - antes) / 1000.0 · con / 1000 entre enteros da 0",
              recompensa="xp 10, oro 10",
              escena="""
                  Detrás de la Encrucijada hay una sala oscura con una **linterna mágica** que proyecta figuras que se mueven. El reloj de la linterna da el tiempo en milisegundos, y el `dt` de Bron le da siempre cero: la figura no se mueve nunca.
              """,
              sugiere="Dividí por `1000.0` (con decimales): así `16 / 1000.0` da `0.016`. " + SIN_VENTANA.replace("Qt", "SDL"),
              desafio="Calculá el `dt` en segundos con decimales.",
              inicial='''
                  #include <cstdint>
                  #include <iostream>

                  int main()
                  {
                      std::uint64_t marcas[] = {1000, 1016, 1033, 1050};
                      double x = 0;
                      for (int i = 1; i < 4; i++) {
                          double dt = (marcas[i] - marcas[i - 1]) / 1000;
                          x += 300 * dt;
                          std::cout << "dt = " << dt << " s, x = " << x << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <cstdint>
                  #include <iostream>

                  int main()
                  {
                      std::uint64_t marcas[] = {1000, 1016, 1033, 1050};
                      double x = 0;
                      for (int i = 1; i < 4; i++) {
                          double dt = (marcas[i] - marcas[i - 1]) / 1000.0;
                          x += 300 * dt;
                          std::cout << "dt = " << dt << " s, x = " << x << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="La figura avanza quince píxeles en tres cuadros. Bron mete la mano delante de la lente y en la pared aparece una mano gigante.",
              imagen=["Una linterna mágica de bronce proyectando figuras en una pared oscura.",
                      BRON + " pone la mano delante de la lente.", TESLA + " ajusta el foco."]),
            m(id="S01-N01-P2", titulo="La pelota que rebota",
              lugar="La sala de la Linterna Mágica", personajes="Lyn, Bron",
              carta="Rebote | si la posición se pasa del borde, se la deja en el borde y se da vuelta la velocidad (vx = -vx)",
              recompensa="xp 10, oro 10",
              escena="""
                  Lyn hace rebotar una pelota de luz contra las paredes de la proyección (la pared derecha está en 100). La pelota de Bron se sale de la pared y se pierde en la oscuridad.
              """,
              sugiere="Si `x` pasa de 100, dejala en 100 y cambiá el signo de `vx`. Lo mismo con el borde izquierdo, en 0.",
              desafio="Hacé rebotar la pelota en los dos bordes.",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      double x = 80;
                      double vx = 50;
                      const double dt = 0.25;
                      for (int cuadro = 1; cuadro <= 4; cuadro++) {
                          x += vx * dt;
                          std::cout << "cuadro " << cuadro << ": x = " << x << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      double x = 80;
                      double vx = 50;
                      const double dt = 0.25;
                      for (int cuadro = 1; cuadro <= 4; cuadro++) {
                          x += vx * dt;
                          if (x > 100) {
                              x = 100;
                              vx = -vx;
                          } else if (x < 0) {
                              x = 0;
                              vx = -vx;
                          }
                          std::cout << "cuadro " << cuadro << ": x = " << x << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="La pelota toca la pared y vuelve. Lyn hace una sombra de conejo y le gana la carrera.",
              imagen=["Una pelota de luz rebotando en el borde de una proyección.",
                      LYN + " hace una sombra de conejo.", BRON + " sigue la pelota con la mirada."]),
            m(id="S01-N01-P3", titulo="La lente que se devuelve sola",
              lugar="La sala de la Linterna Mágica", personajes="Bron, Tesla",
              carta="RAII para SDL | una clase que pide el recurso en el constructor (SDL_CreateWindow) y lo devuelve en el destructor (SDL_DestroyWindow) · se libera al revés de como se pidió",
              recompensa="xp 15, oro 15",
              escena="""
                  La linterna usa tres recursos: la ventana, el pincel y una lente. Bron los pide y los devuelve a mano, y se olvidó de devolver la lente. Tesla le muestra cómo hacer que se devuelvan solos.
              """,
              sugiere="Creá los tres como objetos `Recurso` en orden (ventana, pincel, lente) y borrá las llamadas a mano: al terminar `main`, los destructores los devuelven al revés.",
              desafio="Usá objetos que se devuelvan solos.",
              inicial='''
                  #include <iostream>
                  #include <string>

                  void pedir(const std::string& r) { std::cout << "pido " << r << "\\n"; }
                  void devolver(const std::string& r) { std::cout << "devuelvo " << r << "\\n"; }

                  class Recurso {
                  public:
                      explicit Recurso(std::string n) : nombre_(n) { pedir(nombre_); }
                      ~Recurso() { devolver(nombre_); }
                      Recurso(const Recurso&) = delete;
                      Recurso& operator=(const Recurso&) = delete;

                  private:
                      std::string nombre_;
                  };

                  int main()
                  {
                      pedir("ventana");
                      pedir("pincel");
                      pedir("lente");
                      std::cout << "la linterna proyecta\\n";
                      devolver("pincel");
                      devolver("ventana");
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  void pedir(const std::string& r) { std::cout << "pido " << r << "\\n"; }
                  void devolver(const std::string& r) { std::cout << "devuelvo " << r << "\\n"; }

                  class Recurso {
                  public:
                      explicit Recurso(std::string n) : nombre_(n) { pedir(nombre_); }
                      ~Recurso() { devolver(nombre_); }
                      Recurso(const Recurso&) = delete;
                      Recurso& operator=(const Recurso&) = delete;

                  private:
                      std::string nombre_;
                  };

                  int main()
                  {
                      Recurso ventana("ventana");
                      Recurso pincel("pincel");
                      Recurso lente("lente");
                      std::cout << "la linterna proyecta\\n";
                      return 0;
                  }
              ''',
              al_superar="Lente, pincel, ventana: todo vuelve a su lugar, al revés y sin olvidos.",
              imagen=["Una linterna mágica desarmada sobre una mesa, con sus piezas en orden.",
                      TESLA + " guarda una lente.", BRON + " cierra la caja."]),
        ],
    },
    {
        "titulo": "S01-N02 · Teclado, sprites y animación",
        "misiones": [
            m(id="S01-N02-P1", titulo="La diagonal que no corre más",
              lugar="La sala de la Linterna Mágica", personajes="Bron, Lima",
              carta="Diagonal normalizada | si se aprietan dos flechas, el vector (1, 1) mide 1.41 · se divide por su largo (std::hypot) para que mida 1",
              recompensa="xp 10, oro 10",
              escena="""
                  La heroína de la linterna (la que tiene la cara de Lima) camina más rápido en diagonal que derecho. Lima dice que así no camina ella.
              """,
              sugiere="Si el vector de dirección no es cero, dividí `dx` y `dy` por su largo: `std::hypot(dx, dy)`.",
              desafio="Normalizá la dirección.",
              inicial='''
                  #include <cmath>
                  #include <iomanip>
                  #include <iostream>

                  int main()
                  {
                      int teclas[][2] = {{1, 0}, {1, 1}, {0, -1}};
                      std::cout << std::fixed << std::setprecision(2);
                      for (const auto& t : teclas) {
                          double dx = t[0];
                          double dy = t[1];
                          std::cout << "direccion (" << dx << ", " << dy << "), rapidez " << std::hypot(dx, dy) << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <cmath>
                  #include <iomanip>
                  #include <iostream>

                  int main()
                  {
                      int teclas[][2] = {{1, 0}, {1, 1}, {0, -1}};
                      std::cout << std::fixed << std::setprecision(2);
                      for (const auto& t : teclas) {
                          double dx = t[0];
                          double dy = t[1];
                          double largo = std::hypot(dx, dy);
                          if (largo > 0) {
                              dx /= largo;
                              dy /= largo;
                          }
                          std::cout << "direccion (" << dx << ", " << dy << "), rapidez " << std::hypot(dx, dy) << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Rapidez 1.00 en todas las direcciones. Lima dice que ahora sí camina como ella.",
              imagen=["Una figura proyectada caminando en diagonal con flechas de igual largo.",
                      LIMA + " mira la proyección, conforme.", BRON + " aprieta dos flechas."]),
            m(id="S01-N02-P2", titulo="Recién apretada",
              lugar="La sala de la Linterna Mágica", personajes="Bron, Tesla",
              carta="Tecla recién apretada | está apretada AHORA y NO lo estaba en el cuadro anterior · mantenerla apretada no repite el salto",
              recompensa="xp 15, oro 15",
              escena="""
                  La heroína salta cuando se aprieta la barra. Bron mantiene la barra apretada y la heroína salta en cada cuadro, como un resorte. Tesla le explica que el salto es para la tecla **recién** apretada.
              """,
              sugiere="Guardá cómo estaba la tecla en el cuadro anterior. Salta solo si `ahora && !antes`.",
              desafio="Saltá solo cuando la tecla se acaba de apretar.",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      bool barra[] = {false, true, true, true, false, true};
                      bool antes = false;
                      int saltos = 0;
                      for (int cuadro = 0; cuadro < 6; cuadro++) {
                          bool ahora = barra[cuadro];
                          if (ahora) {
                              saltos++;
                              std::cout << "cuadro " << cuadro << ": salta\\n";
                          }
                          antes = ahora;
                      }
                      std::cout << "Saltos: " << saltos << (antes ? " (la barra sigue apretada)" : "") << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      bool barra[] = {false, true, true, true, false, true};
                      bool antes = false;
                      int saltos = 0;
                      for (int cuadro = 0; cuadro < 6; cuadro++) {
                          bool ahora = barra[cuadro];
                          if (ahora && !antes) {
                              saltos++;
                              std::cout << "cuadro " << cuadro << ": salta\\n";
                          }
                          antes = ahora;
                      }
                      std::cout << "Saltos: " << saltos << (antes ? " (la barra sigue apretada)" : "") << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Dos saltos, no cuatro. La heroína deja de rebotar como un resorte.",
              imagen=["Una heroína proyectada en el aire, con una sola marca de salto.",
                      TESLA + " cuenta los cuadros.", BRON + " suelta la barra."]),
            m(id="S01-N02-P3", titulo="Los cuadros de la caminata",
              lugar="La sala de la Linterna Mágica", personajes="Lima, Bron",
              carta="Animación | cuadro = static_cast<int>(tiempo * fps) % cantidad · con el tiempo, no con las vueltas del bucle, para que vaya igual en cualquier compu",
              recompensa="xp 10, oro 10",
              escena="""
                  La heroína camina pasando cuatro placas de vidrio, a 8 cuadros por segundo. La animación de Bron se pasa del último cuadro y busca una placa 5 que no existe.
              """,
              sugiere="Usá el resto: `% 4`, así después del cuadro 3 vuelve al 0.",
              desafio="Hacé que la animación vuelva a empezar.",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      const double fps = 8;
                      for (double t : {0.0, 0.2, 0.4, 0.6, 0.8}) {
                          int cuadro = static_cast<int>(t * fps);
                          std::cout << "t = " << t << " s -> placa " << cuadro << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      const double fps = 8;
                      for (double t : {0.0, 0.2, 0.4, 0.6, 0.8}) {
                          int cuadro = static_cast<int>(t * fps) % 4;
                          std::cout << "t = " << t << " s -> placa " << cuadro << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="La heroína camina en un ciclo de cuatro placas, sin buscar la quinta. Lima reconoce su cara en la placa 2 y se la tapa.",
              imagen=["Cuatro placas de vidrio pintadas con una heroína en distintas poses.",
                      LIMA + " tapa una de las placas.", BRON + " las ordena."]),
        ],
    },
    {
        "titulo": "S01-N03 · Colisiones, cámara y escenas",
        "misiones": [
            m(id="S01-N03-P1", titulo="Los rectángulos que se tocan",
              lugar="El laberinto de la linterna", personajes="Bron, Tesla",
              carta="AABB | dos rectángulos se superponen si a.x < b.x + b.w y a.x + a.w > b.x, Y lo mismo en y · faltando una condición, choca con todo",
              recompensa="xp 10, oro 10",
              escena="""
                  La heroína tiene que frenar en las paredes del laberinto proyectado. La función de choque de Bron revisa solo el eje horizontal, y la heroína choca con paredes que están en otra fila.
              """,
              sugiere="Agregá las dos condiciones del eje vertical: `a.y < b.y + b.h && a.y + a.h > b.y`.",
              desafio="Revisá los dos ejes.",
              inicial='''
                  #include <iostream>

                  struct Rect {
                      int x, y, w, h;
                  };

                  bool chocan(const Rect& a, const Rect& b)
                  {
                      return a.x < b.x + b.w && a.x + a.w > b.x;
                  }

                  int main()
                  {
                      Rect heroina{10, 10, 16, 16};
                      Rect pared_cerca{20, 20, 32, 32};
                      Rect pared_abajo{10, 100, 32, 32};
                      std::cout << "Pared cerca: " << (chocan(heroina, pared_cerca) ? "choca" : "libre") << "\\n";
                      std::cout << "Pared abajo: " << (chocan(heroina, pared_abajo) ? "choca" : "libre") << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  struct Rect {
                      int x, y, w, h;
                  };

                  bool chocan(const Rect& a, const Rect& b)
                  {
                      return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
                  }

                  int main()
                  {
                      Rect heroina{10, 10, 16, 16};
                      Rect pared_cerca{20, 20, 32, 32};
                      Rect pared_abajo{10, 100, 32, 32};
                      std::cout << "Pared cerca: " << (chocan(heroina, pared_cerca) ? "choca" : "libre") << "\\n";
                      std::cout << "Pared abajo: " << (chocan(heroina, pared_abajo) ? "choca" : "libre") << "\\n";
                      return 0;
                  }
              ''',
              al_superar="La heroína frena en la pared de al lado y pasa libre por arriba de la de abajo.",
              imagen=["Dos rectángulos de luz superpuestos en una pared y uno lejos.",
                      TESLA + " dibuja los bordes con el compás.", BRON + " mueve la heroína."]),
            m(id="S01-N03-P2", titulo="La cámara que no se sale del mundo",
              lugar="El laberinto de la linterna", personajes="Lima, Bron",
              carta="Cámara | camara = jugador - mitad_de_pantalla, limitada con std::clamp entre 0 y mundo - pantalla · en pantalla: x - camara",
              recompensa="xp 15, oro 15",
              escena="""
                  El mundo de la linterna mide 1000 y la pared de la sala solo 320. La cámara sigue a la heroína, pero cerca de los bordes muestra el vacío negro de afuera del mundo.
              """,
              sugiere="Limitá la cámara: `std::clamp(jugador - 160, 0, 1000 - 320)`.",
              desafio="Que la cámara no muestre afuera del mundo.",
              inicial='''
                  #include <algorithm>
                  #include <iostream>

                  int main()
                  {
                      const int mundo = 1000;
                      const int pantalla = 320;
                      for (int jugador : {50, 500, 950}) {
                          int camara = jugador - pantalla / 2;
                          std::cout << "jugador en " << jugador << ": camara en " << camara << ", en pantalla en " << jugador - camara << "\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <algorithm>
                  #include <iostream>

                  int main()
                  {
                      const int mundo = 1000;
                      const int pantalla = 320;
                      for (int jugador : {50, 500, 950}) {
                          int camara = std::clamp(jugador - pantalla / 2, 0, mundo - pantalla);
                          std::cout << "jugador en " << jugador << ": camara en " << camara << ", en pantalla en " << jugador - camara << "\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="En los bordes, la cámara se queda quieta y la heroína camina por la pantalla. El vacío negro desaparece.",
              imagen=["Un riel con la lente de la linterna que se detiene en el tope.",
                      LIMA + " frena la lente con la mano.", BRON + " camina por la proyección."]),
            m(id="S01-N03-P3", titulo="Las escenas que se pasan la posta",
              lugar="La sala de la Linterna Mágica", personajes="Bron, Tesla",
              carta="Escenas | class Escena { virtual std::unique_ptr<Escena> siguiente(...) } · cada escena decide cuál sigue · el juego guarda la actual en un unique_ptr",
              recompensa="xp 15, oro 15",
              escena="""
                  La linterna tiene tres escenas: el título, el juego y el final. El título de Bron, cuando aprietan una tecla, vuelve a crear… el título.
              """,
              sugiere="En `Titulo::siguiente`, devolvé `std::make_unique<Juego>()`.",
              desafio="Que el título pase al juego.",
              inicial='''
                  #include <iostream>
                  #include <memory>
                  #include <string>

                  class Escena {
                  public:
                      virtual ~Escena() = default;
                      virtual std::string nombre() const = 0;
                      virtual std::unique_ptr<Escena> siguiente() const = 0;
                  };

                  class Final : public Escena {
                  public:
                      std::string nombre() const override { return "final"; }
                      std::unique_ptr<Escena> siguiente() const override { return nullptr; }
                  };

                  class Juego : public Escena {
                  public:
                      std::string nombre() const override { return "juego"; }
                      std::unique_ptr<Escena> siguiente() const override { return std::make_unique<Final>(); }
                  };

                  class Titulo : public Escena {
                  public:
                      std::string nombre() const override { return "titulo"; }
                      std::unique_ptr<Escena> siguiente() const override { return std::make_unique<Titulo>(); }
                  };

                  int main()
                  {
                      std::unique_ptr<Escena> actual = std::make_unique<Titulo>();
                      for (int i = 0; i < 4 && actual; i++) {
                          std::cout << "escena: " << actual->nombre() << "\\n";
                          actual = actual->siguiente();
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <memory>
                  #include <string>

                  class Escena {
                  public:
                      virtual ~Escena() = default;
                      virtual std::string nombre() const = 0;
                      virtual std::unique_ptr<Escena> siguiente() const = 0;
                  };

                  class Final : public Escena {
                  public:
                      std::string nombre() const override { return "final"; }
                      std::unique_ptr<Escena> siguiente() const override { return nullptr; }
                  };

                  class Juego : public Escena {
                  public:
                      std::string nombre() const override { return "juego"; }
                      std::unique_ptr<Escena> siguiente() const override { return std::make_unique<Final>(); }
                  };

                  class Titulo : public Escena {
                  public:
                      std::string nombre() const override { return "titulo"; }
                      std::unique_ptr<Escena> siguiente() const override { return std::make_unique<Juego>(); }
                  };

                  int main()
                  {
                      std::unique_ptr<Escena> actual = std::make_unique<Titulo>();
                      for (int i = 0; i < 4 && actual; i++) {
                          std::cout << "escena: " << actual->nombre() << "\\n";
                          actual = actual->siguiente();
                      }
                      return 0;
                  }
              ''',
              al_superar="Título, juego, final. La linterna cuenta una historia entera, y se apaga sola al terminar.",
              imagen=["Tres placas de vidrio en fila: un título, una escena de juego y un cartel de fin.",
                      TESLA + " cambia de placa.", BRON + " aplaude."]),
        ],
    },
    {
        "titulo": "S01-N04 · Jefe de la Linterna: el Espectro",
        "misiones": [
            m(id="S01-N04-P1", titulo="Las gemas de la linterna",
              lugar="El laberinto de los espectros", personajes="Bron, Lyn",
              criatura="dragon",
              carta="Juntar | si el jugador pisa la baldosa de una gema, la gema se borra del mapa y suma · se cuentan las que faltan",
              recompensa="xp 15, oro 15",
              escena="""
                  La linterna se apaga de golpe: el **Espectro de la Linterna** se escapó y se llevó las gemas que la hacen brillar. Lyn apuesta a que Bron no las junta antes del amanecer. Bron pasa por encima de las gemas, pero no las levanta.
              """,
              sugiere="Cuando la baldosa es `*`, cambiala por `.` y sumá una gema.",
              desafio="Juntá las gemas al pisarlas.",
              entrada="EEEEE\n",
              inicial='''
                  #include <iostream>
                  #include <string>

                  int main()
                  {
                      std::string fila = "B.*.**";
                      std::string camino;
                      std::cin >> camino;
                      int x = 0;
                      int gemas = 0;
                      for (char d : camino) {
                          if (d == 'E') x++;
                      }
                      std::cout << "Gemas: " << gemas << ", fila: " << fila << "\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>
                  #include <string>

                  int main()
                  {
                      std::string fila = "B.*.**";
                      std::string camino;
                      std::cin >> camino;
                      int x = 0;
                      int gemas = 0;
                      for (char d : camino) {
                          if (d == 'E') x++;
                          if (fila[x] == '*') {
                              fila[x] = '.';
                              gemas++;
                          }
                      }
                      std::cout << "Gemas: " << gemas << ", fila: " << fila << "\\n";
                      return 0;
                  }
              ''',
              al_superar="Tres gemas en el bolsillo y la fila queda limpia. Lyn mira el cielo: falta mucho para el amanecer.",
              imagen=["Un laberinto oscuro con gemas brillantes en el piso.",
                      BRON + " junta una gema.", LYN + " mira su cronómetro."]),
            m(id="S01-N04-P2", titulo="El espectro que no se cansa",
              lugar="El laberinto de los espectros", personajes="Bron, Tesla",
              criatura="dragon",
              carta="Perseguir | en cada paso, el espectro se acerca un lugar en cada eje: si está a la izquierda, x + 1; a la derecha, x - 1 (lo mismo en y)",
              recompensa="xp 15, oro 15",
              escena="""
                  Los espectros no tienen prisa, pero tampoco se cansan: en cada paso se acercan a Bron. El espectro de Bron solo se acerca en horizontal, y nunca lo alcanza en vertical.
              """,
              sugiere="Hacé lo mismo con `y`: si el espectro está arriba, `ey++`; si está abajo, `ey--`.",
              desafio="Que el espectro persiga en los dos ejes.",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      int bx = 5, by = 5;
                      int ex = 1, ey = 2;
                      for (int paso = 1; paso <= 4; paso++) {
                          if (ex < bx) ex++;
                          if (ex > bx) ex--;
                          std::cout << "paso " << paso << ": espectro en (" << ex << ", " << ey << ")\\n";
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      int bx = 5, by = 5;
                      int ex = 1, ey = 2;
                      for (int paso = 1; paso <= 4; paso++) {
                          if (ex < bx) ex++;
                          if (ex > bx) ex--;
                          if (ey < by) ey++;
                          if (ey > by) ey--;
                          std::cout << "paso " << paso << ": espectro en (" << ex << ", " << ey << ")\\n";
                      }
                      return 0;
                  }
              ''',
              al_superar="Al cuarto paso, el espectro está encima de Bron. Bron sale corriendo, y ahora sabe cuántos pasos tiene de ventaja.",
              imagen=["Un espectro de luz pixelado acercándose en diagonal por un laberinto.",
                      BRON + " retrocede.", TESLA + " cuenta los pasos."]),
            m(id="S01-N04-P3", titulo="La linterna se enciende",
              lugar="La sala de la Linterna Mágica", personajes="Bron, Tesla, Lyn",
              criatura="dragon",
              carta="Fin del juego | se gana cuando se juntaron TODAS las gemas · se pierde si un espectro toca al jugador · se revisa en cada cuadro, en orden",
              recompensa="xp 25, oro 30",
              escena="""
                  Bron vuelve con las gemas, perseguido por los espectros. El marcador de la linterna dice «ganaste» apenas junta la primera gema, y Lyn reclama: faltan dos.
              """,
              sugiere="Se gana cuando `gemas == total`, no con cualquier gema. Y el toque del espectro se revisa antes.",
              desafio="Corregí la condición de victoria.",
              inicial='''
                  #include <iostream>

                  int main()
                  {
                      const int total = 3;
                      int gemas = 0;
                      bool tocado = false;
                      int cuadros_con_gema[] = {2, 5, 7};
                      for (int cuadro = 1; cuadro <= 8; cuadro++) {
                          for (int c : cuadros_con_gema) {
                              if (c == cuadro) gemas++;
                          }
                          if (tocado) {
                              std::cout << "cuadro " << cuadro << ": perdiste\\n";
                              return 0;
                          }
                          if (gemas > 0) {
                              std::cout << "cuadro " << cuadro << ": ganaste con " << gemas << " gemas\\n";
                              return 0;
                          }
                      }
                      std::cout << "se acabo el tiempo\\n";
                      return 0;
                  }
              ''',
              solucion='''
                  #include <iostream>

                  int main()
                  {
                      const int total = 3;
                      int gemas = 0;
                      bool tocado = false;
                      int cuadros_con_gema[] = {2, 5, 7};
                      for (int cuadro = 1; cuadro <= 8; cuadro++) {
                          for (int c : cuadros_con_gema) {
                              if (c == cuadro) gemas++;
                          }
                          if (tocado) {
                              std::cout << "cuadro " << cuadro << ": perdiste\\n";
                              return 0;
                          }
                          if (gemas == total) {
                              std::cout << "cuadro " << cuadro << ": ganaste con " << gemas << " gemas\\n";
                              return 0;
                          }
                      }
                      std::cout << "se acabo el tiempo\\n";
                      return 0;
                  }
              ''',
              al_superar="En el cuadro 7, con las tres gemas, la linterna se enciende otra vez y el Espectro vuelve a sus placas de vidrio. Oto, que había apostado a favor de Bron, le sirve un guiso de festejo.",
              imagen=["La linterna mágica encendida otra vez, proyectando colores en toda la sala.",
                      BRON + " levanta tres gemas.", TESLA + " y " + LYN + " festejan; " + OTO + " trae una olla."]),
        ],
    },
]
