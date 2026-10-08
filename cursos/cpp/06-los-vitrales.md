# RAMA R06 · Los Vitrales: aplicaciones de escritorio con Qt

```meta
tipo: tronco
posicion: 6
```

## R06-N01 · Los Vitrales: ventanas, señales y slots

```meta
tipo: tema
padre: R05-N06
precio: 10
criatura: slime
ejecutable: no
temas: gui.qt, gui.eventos, gui.componentes, gui.layouts
usa: cal.build
```

### Crónica

Desde el Laberinto, una escalera sube al **Taller de los Vitrales**, en lo más alto de la Ciudadela. Acá no se hacen juegos: se hacen **ventanas** para que cualquiera, aunque no sepa programar, use las máquinas. Cada vitral tiene palancas, perillas y carteles.

Bron aprieta todos los botones de un vitral a la vez, para ver qué pasa. Suenan todas las campanas del taller juntas. La Maestra Artífice levanta la vista de la tableta y Bron saca las manos del vitral.

—En el Laberinto, vos llevabas el ritmo con tu bucle —dice {mentor}—. Acá es al revés: el vitral **espera**. Cuando alguien toca una palanca, suena una campana, y tu código responde. Se llaman **señales y slots**.

### Objetivos

- Instalar Qt 6 y compilar una aplicación con CMake.
- Entender el modelo **dirigido por eventos**: `QApplication` y su bucle.
- Armar ventanas con widgets (`QPushButton`, `QLabel`, `QSpinBox`…) y **layouts**.
- Conectar **señales** con **slots** (funciones o lambdas) y crear señales propias con `Q_OBJECT`.

### Antes de empezar

Todo el camino principal, en especial clases, herencia, lambdas y `std::function` (ramas 2 a 4).

### Explicación

#### Instalar Qt y compilar

Qt es un **framework** enorme: ventanas, botones, archivos, red, bases de datos. Se instala una vez:

- **Linux** (Ubuntu, Debian, Mint):
  ```bash
  sudo apt install qt6-base-dev cmake qtcreator
  ```
- **Windows**: bajá el **Qt Online Installer** de qt.io (sección *Download Qt for open source use*; pide crear una cuenta gratuita). En la lista de componentes elegí la versión de **Qt 6** más nueva con **MinGW 64-bit**, y dejá tildados **Qt Creator**, **CMake** y **Ninja** (en *Build Tools*). Instala todo junto, compilador incluido.

**Con Qt Creator** (lo que usa la UTN, en Linux y en Windows): *Archivo → Abrir archivo o proyecto* y elegí el `CMakeLists.txt`. La primera vez pide un *kit*: elegí el de Qt 6 (en Windows, el de MinGW). Después, el triángulo verde de abajo a la izquierda (o `Ctrl+R`) compila y ejecuta. Para un proyecto nuevo, *Archivo → Nuevo proyecto → Application (Qt) → Qt Widgets Application*, con CMake como sistema de compilación.

**Con VS Code**: instalá las extensiones *C/C++* y *CMake Tools*, abrí la carpeta del proyecto y elegí el kit (en Windows, el compilador MinGW que trajo Qt). La barra de abajo tiene *Build* y el botón de ejecutar. Si no encuentra Qt, agregá en `.vscode/settings.json` la ruta de Qt: `"cmake.configureSettings": { "CMAKE_PREFIX_PATH": "C:/Qt/6.8.0/mingw_64" }` (con tu versión).

Los programas de Qt se compilan con CMake:
```cmake
cmake_minimum_required(VERSION 3.16)
project(vitrales CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_AUTOMOC ON)                            # ver "moc", más abajo
find_package(Qt6 REQUIRED COMPONENTS Widgets)
add_executable(vitrales main.cpp)
target_link_libraries(vitrales PRIVATE Qt6::Widgets)
```
Desde la terminal (Linux, o la terminal de Qt en Windows: *Inicio → Qt 6 (MinGW)*):
```bash
cmake -B build && cmake --build build && ./build/vitrales      # Linux
cmake -B build -G Ninja && cmake --build build && build\vitrales.exe   # Windows
```
Estos programas abren ventanas: se prueban en tu compu y se entregan como `.zip` con el código y el `CMakeLists.txt`.

#### Otra forma de programar: eventos
En un juego, tu `while` corre sin parar. En una aplicación de escritorio, la ventana está casi siempre **quieta, esperando**. Qt tiene su propio bucle (`app.exec()`) que espera eventos (un clic, una tecla, un temporizador) y llama a **tus** funciones cuando pasan.
```cpp
int main(int argc, char* argv[])
{
    QApplication app(argc, argv);    // uno solo, antes de crear cualquier widget
    QWidget ventana;
    ventana.show();
    return app.exec();               // el bucle de eventos: termina al cerrar la última ventana
}
```

#### Widgets y layouts
Cada cosa en pantalla es un **widget**: `QLabel` (texto), `QPushButton`, `QLineEdit` (una línea de texto), `QSpinBox` y `QDoubleSpinBox` (números), `QSlider`, `QProgressBar`… No se ubican con coordenadas: se ponen en **layouts** que los acomodan solos al cambiar el tamaño:
- `QVBoxLayout` (uno abajo del otro), `QHBoxLayout` (uno al lado del otro);
- `QGridLayout` (grilla: `addWidget(w, fila, columna)`), `QFormLayout` (etiqueta y campo).

**¿Y los `new` sin `delete`?** En Qt, cada widget tiene un **padre**. Cuando se destruye el padre, destruye a todos sus hijos. Al poner un widget en un layout, el widget de ese layout pasa a ser su padre. Por eso se escribe `new QPushButton(...)` sin `delete`: es la forma de RAII de Qt (el dueño es el padre). Lo que **no** tiene padre (la ventana principal) se crea como variable normal en `main`.

#### Señales y slots
Un widget **emite señales** cuando le pasa algo (`clicked`, `valueChanged`, `textChanged`). Con `connect` se dice qué hacer:
```cpp
QObject::connect(boton, &QPushButton::clicked, &ventana, [&] { contador++; });   // con una lambda
QObject::connect(caldera, &Caldera::presionCambio, barra, &QProgressBar::setValue);   // con un método
```
`connect(emisor, &Clase::señal, contexto, qué_hacer)`. El tercer parámetro (contexto) hace que la conexión se corte sola si ese objeto se destruye. Una señal puede tener muchos receptores y un receptor escuchar muchas señales: es el **bus de eventos** de la rama 4, hecho parte del framework.

#### Señales propias: `Q_OBJECT` y moc
Una clase propia puede declarar señales si hereda de `QObject` y lleva la macro `Q_OBJECT`:
```cpp
class Caldera : public QObject {
    Q_OBJECT
public slots:
    void calentar(int grados);
signals:
    void presionCambio(int nueva);     // no se implementa: la escribe moc
};
... emit presionCambio(presion_);      // "tocar la campana"
```
**moc** (*meta-object compiler*) es un programa de Qt que lee las clases con `Q_OBJECT` y genera el código de sus señales. `set(CMAKE_AUTOMOC ON)` lo corre solo. Si la clase está en un `.cpp` (y no en un `.h`), al final del archivo va `#include "main.moc"`.

#### El `QTimer`
Un `QTimer` emite `timeout()` cada tantos milisegundos: es la forma de hacer algo periódico sin bucle propio.

#### Evitar el rebote
Si dos campos se actualizan entre sí (Celsius ↔ Fahrenheit), cambiar uno emite su señal, que cambia el otro, que emite… Un `QSignalBlocker` silencia las señales de un widget mientras dura su bloque.

### Código de ejemplo

```cpp
/*
 * R06-N01 - Ventanas, senales y slots: la caldera del Taller.
 * Con CMake: find_package(Qt6 REQUIRED COMPONENTS Widgets) y set(CMAKE_AUTOMOC ON).
 */
#include <QApplication>
#include <QHBoxLayout>
#include <QLabel>
#include <QProgressBar>
#include <QPushButton>
#include <QTimer>
#include <QVBoxLayout>
#include <QWidget>

// Un objeto de Qt con SENALES propias: avisa cuando cambia, sin saber quien escucha.
class Caldera : public QObject {
    Q_OBJECT

public:
    int presion() const { return presion_; }

public slots:
    void calentar(int grados)
    {
        presion_ = qMin(100, presion_ + grados);
        emit presionCambio(presion_);          // "tocar la campana"
        if (presion_ == 100) {
            emit exploto();
        }
    }
    void purgar()
    {
        presion_ = 0;
        emit presionCambio(presion_);
    }

signals:
    void presionCambio(int nueva);
    void exploto();

private:
    int presion_ = 0;
};

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);                   // uno solo, antes de cualquier widget

    QWidget ventana;
    ventana.setWindowTitle("La caldera del Taller");
    auto* columna = new QVBoxLayout(&ventana);      // los widgets hijos se liberan con su padre
    auto* barra = new QProgressBar;
    barra->setRange(0, 100);
    auto* estado = new QLabel("Presión: 0");
    auto* fila = new QHBoxLayout;
    auto* calentar = new QPushButton("Calentar +15");
    auto* purgar = new QPushButton("Purgar");
    fila->addWidget(calentar);
    fila->addWidget(purgar);
    columna->addWidget(barra);
    columna->addWidget(estado);
    columna->addLayout(fila);

    Caldera caldera;
    // connect(emisor, senal, receptor, slot): cuando pasa la senal, se llama al slot.
    QObject::connect(calentar, &QPushButton::clicked, &caldera, [&caldera] { caldera.calentar(15); });
    QObject::connect(purgar, &QPushButton::clicked, &caldera, &Caldera::purgar);
    QObject::connect(&caldera, &Caldera::presionCambio, barra, &QProgressBar::setValue);
    QObject::connect(&caldera, &Caldera::presionCambio, estado, [estado](int p) {
        estado->setText(QString("Presión: %1").arg(p));
    });
    QObject::connect(&caldera, &Caldera::exploto, estado, [estado] { estado->setText("¡BUM! Purgá la caldera."); });

    // Un QTimer emite timeout() cada tanto: la caldera se calienta sola.
    QTimer reloj;
    QObject::connect(&reloj, &QTimer::timeout, &caldera, [&caldera] { caldera.calentar(1); });
    reloj.start(500);

    ventana.resize(360, 150);
    ventana.show();
    return app.exec();                               // el bucle de eventos: Qt llama a tus funciones
}

#include "main.moc"   // el codigo que genera moc para las clases con Q_OBJECT de este archivo
```

### ¿Para qué sirve?

Qt es el framework de C++ más usado para aplicaciones de escritorio: con él se hicieron programas como VLC, OBS Studio, VirtualBox, Autodesk Maya, las pantallas de muchos autos y la interfaz de KDE. En el mundo de los juegos se usa para las **herramientas**: editores de niveles, lanzadores, visores de recursos y paneles de configuración.

### Errores habituales

**Esqueleto: falta moc.** Una clase con `Q_OBJECT` sin `CMAKE_AUTOMOC` (o sin `#include "main.moc"` si está en el `.cpp`):
```
undefined reference to `vtable for Caldera'
```

**Esqueleto: el header de Qt que falta.** `QLabel` sin `#include <QLabel>`: "incomplete type" o "was not declared".

**Troll: un widget sin padre que nadie borra.** Si creás con `new` un widget que no ponés en ningún layout ni le das padre, nadie lo libera. Y al revés: un widget **con** padre no se borra con `delete` a mano (lo borraría dos veces).

**Ogro: el rebote infinito.** Dos campos que se actualizan mutuamente sin `QSignalBlocker` cuelgan el programa.

**Ogro: trabar el bucle de eventos.** Un cálculo largo (o un `sleep`) dentro de un slot congela la ventana: mientras tu función corre, Qt no puede redibujar ni atender clics.

### Misión R06-N01-M1 · El conversor de temperaturas

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, cpp, h, txt
```

#### Consigna

Hacé una ventana con dos campos numéricos (`QDoubleSpinBox`), Celsius y Fahrenheit, en un `QFormLayout`. Cambiar cualquiera de los dos actualiza el otro (sin rebote infinito: `QSignalBlocker`). Debajo, un cartel avisa "Se congela el agua" bajo 0 °C y "Hierve el agua" desde 100 °C.

#### Criterio de aprobación

- Los dos campos se actualizan mutuamente sin colgarse.
- Usa lambdas conectadas a `valueChanged`.
- Compila con CMake sin advertencias.

#### Solución de referencia

```cpp
// R06-N01-M1 - El conversor de temperaturas: dos campos que se actualizan entre si.
#include <QApplication>
#include <QDoubleSpinBox>
#include <QFormLayout>
#include <QLabel>
#include <QSignalBlocker>
#include <QWidget>

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    QWidget ventana;
    ventana.setWindowTitle("Conversor de temperaturas");
    auto* formulario = new QFormLayout(&ventana);
    auto* celsius = new QDoubleSpinBox;
    auto* fahrenheit = new QDoubleSpinBox;
    for (auto* campo : {celsius, fahrenheit}) {
        campo->setRange(-500, 1000);
        campo->setDecimals(1);
    }
    auto* aviso = new QLabel;
    formulario->addRow("Celsius", celsius);
    formulario->addRow("Fahrenheit", fahrenheit);
    formulario->addRow(aviso);

    auto avisar = [aviso](double c) {
        aviso->setText(c < 0 ? "Se congela el agua" : c >= 100 ? "Hierve el agua" : "");
    };
    // Cada campo actualiza al otro. QSignalBlocker evita que el cambio "rebote" para siempre.
    QObject::connect(celsius, &QDoubleSpinBox::valueChanged, fahrenheit, [=](double c) {
        QSignalBlocker bloqueo(fahrenheit);
        fahrenheit->setValue(c * 9 / 5 + 32);
        avisar(c);
    });
    QObject::connect(fahrenheit, &QDoubleSpinBox::valueChanged, celsius, [=](double f) {
        QSignalBlocker bloqueo(celsius);
        celsius->setValue((f - 32) * 5 / 9);
        avisar(celsius->value());
    });
    celsius->setValue(20);
    ventana.show();
    return app.exec();
}
```

### Misión R06-N01-M2 · El contador de aforo

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, cpp, h, txt
```

#### Consigna

Un contador para la puerta de una sala: un número grande, botones "Entra", "Sale" y "Reiniciar", y un `QSpinBox` con la capacidad. El número se pone **rojo** si se supera la capacidad (con `setStyleSheet`), el título dice "Aforo: N de M" (o avisa que se excedió) y el botón "Sale" se desactiva con la sala vacía. Toda la actualización está en **una** función `refrescar` que llaman todos.

#### Criterio de aprobación

- Los botones y el campo de capacidad llaman a la misma función de refresco.
- "Sale" se desactiva con `setEnabled(false)` cuando no hay nadie.

#### Solución de referencia

```cpp
// R06-N01-M2 - El contador de aforo de la sala.
#include <QApplication>
#include <QGridLayout>
#include <QLabel>
#include <QPushButton>
#include <QSpinBox>
#include <QWidget>

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    QWidget ventana;
    auto* grilla = new QGridLayout(&ventana);
    auto* numero = new QLabel("0");
    numero->setAlignment(Qt::AlignCenter);
    auto* entra = new QPushButton("Entra (+1)");
    auto* sale = new QPushButton("Sale (-1)");
    auto* reiniciar = new QPushButton("Reiniciar");
    auto* capacidad = new QSpinBox;
    capacidad->setRange(1, 500);
    capacidad->setValue(30);
    capacidad->setPrefix("Capacidad: ");
    grilla->addWidget(numero, 0, 0, 1, 3);
    grilla->addWidget(entra, 1, 0);
    grilla->addWidget(sale, 1, 1);
    grilla->addWidget(reiniciar, 1, 2);
    grilla->addWidget(capacidad, 2, 0, 1, 3);

    int adentro = 0;
    auto refrescar = [&] {
        bool lleno = adentro > capacidad->value();
        numero->setText(QString::number(adentro));
        numero->setStyleSheet(QString("font-size: 64px; color: %1;").arg(lleno ? "#d33" : "#2a2"));
        ventana.setWindowTitle(lleno ? "¡Sala excedida!" : QString("Aforo: %1 de %2").arg(adentro).arg(capacidad->value()));
        sale->setEnabled(adentro > 0);
    };
    QObject::connect(entra, &QPushButton::clicked, &ventana, [&] { adentro++; refrescar(); });
    QObject::connect(sale, &QPushButton::clicked, &ventana, [&] { adentro--; refrescar(); });
    QObject::connect(reiniciar, &QPushButton::clicked, &ventana, [&] { adentro = 0; refrescar(); });
    QObject::connect(capacidad, &QSpinBox::valueChanged, &ventana, [&] { refrescar(); });
    refrescar();
    ventana.show();
    return app.exec();
}
```

### Encargo R06-N01-E1 · Las propinas del bar

```meta
entrega: archivo
entorno: local
monedas: 1
xp: 20
extensiones: zip, cpp, h, txt
```

#### Consigna

El bar de la esquina quiere una calculadora de propinas: el monto de la cuenta, un deslizador (`QSlider`) para el porcentaje (0 a 30%), la cantidad de personas, y los resultados: la propina, el total y cuánto paga cada uno, con 2 decimales (`QString::arg(valor, 0, 'f', 2)`). Todo se recalcula al cambiar cualquier dato.

#### Criterio de aprobación

- Se recalcula con cualquier cambio.
- Los montos se muestran con 2 decimales.

#### Solución de referencia

```cpp
// R06-N01-E1 - La calculadora de propinas del bar de la esquina.
#include <QApplication>
#include <QDoubleSpinBox>
#include <QFormLayout>
#include <QLabel>
#include <QSlider>
#include <QSpinBox>
#include <QWidget>

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    QWidget ventana;
    ventana.setWindowTitle("Propinas");
    auto* f = new QFormLayout(&ventana);
    auto* cuenta = new QDoubleSpinBox;
    cuenta->setRange(0, 1000000);
    cuenta->setPrefix("$ ");
    cuenta->setValue(25000);
    auto* porcentaje = new QSlider(Qt::Horizontal);
    porcentaje->setRange(0, 30);
    porcentaje->setValue(10);
    auto* etiqueta_pct = new QLabel;
    auto* personas = new QSpinBox;
    personas->setRange(1, 30);
    personas->setValue(2);
    auto* propina = new QLabel;
    auto* total = new QLabel;
    auto* cada_uno = new QLabel;
    f->addRow("Cuenta", cuenta);
    f->addRow("Propina", porcentaje);
    f->addRow("", etiqueta_pct);
    f->addRow("Personas", personas);
    f->addRow("Propina", propina);
    f->addRow("Total", total);
    f->addRow("Cada uno", cada_uno);

    auto calcular = [=] {
        double p = cuenta->value() * porcentaje->value() / 100.0;
        double t = cuenta->value() + p;
        etiqueta_pct->setText(QString("%1 %").arg(porcentaje->value()));
        propina->setText(QString("$ %1").arg(p, 0, 'f', 2));
        total->setText(QString("$ %1").arg(t, 0, 'f', 2));
        cada_uno->setText(QString("$ %1").arg(t / personas->value(), 0, 'f', 2));
    };
    QObject::connect(cuenta, &QDoubleSpinBox::valueChanged, &ventana, calcular);
    QObject::connect(porcentaje, &QSlider::valueChanged, &ventana, calcular);
    QObject::connect(personas, &QSpinBox::valueChanged, &ventana, calcular);
    calcular();
    ventana.show();
    return app.exec();
}
```

### Prueba del sello

#### ¿Qué hace `app.exec()`?

Corre el bucle de eventos de Qt: espera eventos y llama a las funciones conectadas, hasta que se cierra la última ventana.

#### ¿Por qué en Qt se escribe `new QPushButton` sin `delete`?

Porque el botón tiene un padre (el widget del layout), y el padre destruye a sus hijos.

#### ¿Qué conecta `connect(boton, &QPushButton::clicked, &ventana, lambda)`?

La señal `clicked` del botón con la lambda; `ventana` es el contexto que corta la conexión si se destruye.

#### ¿Qué hace moc y cuándo hace falta?

Genera el código de las señales de las clases con `Q_OBJECT`. Hace falta cuando declarás señales o slots propios.

#### ¿Por qué un cálculo largo dentro de un slot congela la ventana?

Porque mientras corre, el bucle de eventos no puede redibujar ni atender otros eventos.

### Soluciones (docente)

Senda basada en `FullCursos/12-Qt-GUI` (01 a 07). Los programas se verificaron compilando con CMake + AUTOMOC contra Qt 6.4 y arrancando con `QT_QPA_PLATFORM=offscreen`.

## R06-N02 · Formularios, menús y archivos

```meta
tipo: tema
padre: R06-N01
precio: 10
criatura: goblin
ejecutable: no
temas: gui.componentes, gui.menus-dialogos
usa: gui.qt
```

### Crónica

El vitral de la oficina de inscripciones tiene de todo: campos para escribir, listas desplegables, casillas, un menú arriba y una barra abajo que avisa qué pasó. Lyn se inscribe en una carrera, se olvida de poner el nombre, y una ventanita le avisa. Lyn le apuesta a la ventanita que la próxima vez se acuerda. Pierde.

—Una aplicación de verdad no confía en nadie —dice {mentor}—. Revisa lo que le escriben, pregunta antes de borrar, y guarda en un archivo para que nada se pierda.

Oto pide un vitral para anotar sus recetas. Bron le promete hacérselo. Lima le recuerda a Bron que ya prometió cuatro.

### Objetivos

- Armar formularios con `QLineEdit`, `QComboBox`, `QCheckBox`, `QDateEdit` y listas (`QListWidget`).
- Usar una **ventana principal** (`QMainWindow`) con menús, atajos y barra de estado.
- Validar y avisar con diálogos (`QMessageBox`), elegir archivos (`QFileDialog`) y guardar y leer con `QFile` y `QTextStream`.
- Reaccionar al cierre de una ventana (`closeEvent`).

### Antes de empezar

Ventanas, señales y slots (nodo anterior). Archivos (rama 3).

### Explicación

#### Widgets de formulario
| Widget | Para | Señal útil |
|---|---|---|
| `QLineEdit` | una línea de texto (`text()`, `setPlaceholderText`) | `textChanged`, `returnPressed` |
| `QComboBox` | elegir de una lista (`addItems`, `currentText()`, `currentIndex()`) | `currentIndexChanged` |
| `QCheckBox` | sí o no (`isChecked()`) | `toggled` |
| `QDateEdit` | una fecha (`date()`, con `setCalendarPopup(true)`) | `dateChanged` |
| `QListWidget` | una lista de ítems (`addItem`, `count()`, `item(i)`, `takeItem(i)`) | `currentRowChanged` |

Los textos de Qt son `QString` (no `std::string`): tienen `trimmed()`, `isEmpty()`, `split()`, `contains()`, y `QString("%1 de %2").arg(a).arg(b)` para armar mensajes. Se convierten con `QString::fromStdString(s)` y `q.toStdString()`.

#### La ventana principal
`QMainWindow` trae un lugar para el **menú**, las **barras de herramientas**, la **barra de estado** y un **widget central**:
```cpp
QMenu* archivo = menuBar()->addMenu("&Archivo");     // la & marca la letra del atajo (Alt+A)
QAction* guardar = archivo->addAction("&Guardar...");
guardar->setShortcut(QKeySequence::Save);             // Ctrl+S (o Cmd+S en macOS)
connect(guardar, &QAction::triggered, this, &Registro::guardar);
statusBar()->showMessage("Guardado", 3000);           // desaparece a los 3 segundos
setCentralWidget(central);
```
Una ventana propia se escribe **heredando** de `QMainWindow` (o `QWidget`): los widgets son miembros y los slots son métodos.

#### Diálogos
```cpp
QMessageBox::warning(this, "Falta el nombre", "Escribí el nombre.");
if (QMessageBox::question(this, "Borrar", "¿Seguro?") == QMessageBox::Yes) { ... }
QString ruta = QFileDialog::getSaveFileName(this, "Guardar", "datos.txt", "Texto (*.txt)");
if (ruta.isEmpty()) return;          // el usuario canceló
```
Estos diálogos son **modales**: el programa espera la respuesta antes de seguir.

#### Archivos con Qt
Se puede usar `std::fstream`, pero con Qt es más cómodo `QFile` + `QTextStream` (que maneja bien los acentos):
```cpp
QFile f(ruta);
if (!f.open(QIODevice::WriteOnly | QIODevice::Text)) { /* error */ }
QTextStream salida(&f);
salida << "línea\n";                  // se cierra solo (RAII) al terminar el bloque
```
Para leer: `QIODevice::ReadOnly`, y `while (!in.atEnd()) { QString linea = in.readLine(); }`.

#### Al cerrar
Redefiniendo `closeEvent(QCloseEvent* e)` en tu ventana podés guardar antes de cerrar, o preguntar y cancelar el cierre con `e->ignore()`.

#### Validar
Revisá **todo** lo que escribe el usuario antes de usarlo, y decile **qué** está mal (juntá los errores en una `QStringList` y mostralos juntos). Botones que no tienen sentido en un momento (borrar sin nada elegido) se desactivan con `setEnabled(false)`.

#### Cómo compilarlo y ejecutarlo

Abre una ventana, así que se compila en tu compu con el `CMakeLists.txt` del primer nodo de la rama:
- **Qt Creator** (Linux y Windows): abrí el `CMakeLists.txt` y apretá **Ctrl+R**.
- **Terminal:** `cmake -B build && cmake --build build`, y después `./build/vitrales` (Linux) o `build\vitrales.exe` (Windows).

### Código de ejemplo

```cpp
/*
 * R06-N02 - Widgets, layouts y dialogos: el registro de artifices en una ventana principal.
 */
#include <QApplication>
#include <QCheckBox>
#include <QComboBox>
#include <QFile>
#include <QFileDialog>
#include <QFormLayout>
#include <QLineEdit>
#include <QListWidget>
#include <QMainWindow>
#include <QMenuBar>
#include <QMessageBox>
#include <QPushButton>
#include <QSpinBox>
#include <QStatusBar>
#include <QTextStream>
#include <QVBoxLayout>

class Registro : public QMainWindow {
public:
    Registro()
    {
        setWindowTitle("Registro de artífices");
        auto* central = new QWidget;
        auto* columna = new QVBoxLayout(central);
        auto* form = new QFormLayout;
        nombre_ = new QLineEdit;
        nombre_->setPlaceholderText("Nombre y apellido");
        edad_ = new QSpinBox;
        edad_->setRange(10, 99);
        taller_ = new QComboBox;
        taller_->addItems({"Relojes", "Vapor", "Faros", "Vitrales"});
        aprendiz_ = new QCheckBox("Es aprendiz");
        form->addRow("Nombre", nombre_);
        form->addRow("Edad", edad_);
        form->addRow("Taller", taller_);
        form->addRow("", aprendiz_);
        auto* agregar = new QPushButton("Agregar");
        lista_ = new QListWidget;
        columna->addLayout(form);
        columna->addWidget(agregar);
        columna->addWidget(lista_);
        setCentralWidget(central);

        // Menu Archivo
        QMenu* archivo = menuBar()->addMenu("&Archivo");
        QAction* guardar = archivo->addAction("&Guardar...");
        guardar->setShortcut(QKeySequence::Save);
        archivo->addSeparator();
        QAction* salir = archivo->addAction("&Salir");
        salir->setShortcut(QKeySequence::Quit);

        connect(agregar, &QPushButton::clicked, this, &Registro::agregar);
        connect(nombre_, &QLineEdit::returnPressed, this, &Registro::agregar);   // Enter tambien agrega
        connect(guardar, &QAction::triggered, this, &Registro::guardar);
        connect(salir, &QAction::triggered, this, &QWidget::close);
        statusBar()->showMessage("Listo");
    }

private:
    void agregar()
    {
        QString nombre = nombre_->text().trimmed();
        if (nombre.isEmpty()) {
            QMessageBox::warning(this, "Falta el nombre", "Escribí el nombre del artífice.");
            return;
        }
        lista_->addItem(QString("%1 (%2) - %3%4").arg(nombre).arg(edad_->value()).arg(taller_->currentText(),
                                                                                       aprendiz_->isChecked() ? ", aprendiz" : ""));
        nombre_->clear();
        nombre_->setFocus();
        statusBar()->showMessage(QString("%1 artífices").arg(lista_->count()));
    }

    void guardar()
    {
        QString ruta = QFileDialog::getSaveFileName(this, "Guardar registro", "artifices.txt", "Texto (*.txt)");
        if (ruta.isEmpty()) {
            return;                                   // el usuario cancelo
        }
        QFile archivo(ruta);
        if (!archivo.open(QIODevice::WriteOnly | QIODevice::Text)) {
            QMessageBox::critical(this, "Error", "No se pudo escribir " + ruta);
            return;
        }
        QTextStream salida(&archivo);
        for (int i = 0; i < lista_->count(); i++) {
            salida << lista_->item(i)->text() << "\n";
        }
        statusBar()->showMessage("Guardado en " + ruta, 3000);
    }

    QLineEdit* nombre_;
    QSpinBox* edad_;
    QComboBox* taller_;
    QCheckBox* aprendiz_;
    QListWidget* lista_;
};

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    Registro ventana;
    ventana.resize(420, 480);
    ventana.show();
    return app.exec();
}
```

### ¿Para qué sirve?

Formularios con validación, menús y archivos son el 90% de las aplicaciones de gestión: sistemas de turnos, inventarios, inscripciones, facturación, fichas de pacientes. Cualquier comercio o institución que necesita "un programita para cargar datos" necesita exactamente esto.

### Errores habituales

**Ogro: no revisar lo que devuelve un diálogo.** Si el usuario cancela, `getSaveFileName` devuelve un texto vacío: abrir un archivo con ese nombre falla (o peor, crea uno sin nombre).

**Ogro: no revisar `open`.** `QFile::open` devuelve `false` si no puede (sin permisos, carpeta inexistente): hay que avisar.

**Orco: borrar de una lista hacia adelante.** Al borrar el ítem `i`, los de atrás se corren: se saltea uno. Se recorre **de atrás para adelante**.

**Esqueleto: una variable local con el nombre de un método.** Dentro de una lambda, `agregar(...)` se refiere al botón local llamado `agregar`, no al método:
```
main.cpp:31:64: error: ‘agregar’ is not captured
```
Poné nombres distintos (`boton_agregar`).

**Goblin: mezclar `QString` y `std::string`.** No se convierten solos: `QString::fromStdString` y `toStdString`.

### Misión R06-N02-M1 · La inscripción al torneo

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, cpp, h, txt
```

#### Consigna

Un formulario de inscripción (nombre, correo, fecha de nacimiento con `QDateEdit`, categoría con `QComboBox`) con botones Aceptar y Reiniciar (`QDialogButtonBox`). Al aceptar, se **validan todos los campos a la vez** y se muestran los errores juntos en un `QMessageBox`: nombre de 3 letras o más, un correo con `@` y un punto después, y la categoría que corresponde a la edad (Infantil hasta 12, Juvenil de 13 a 17, Mayor desde 18). Si todo está bien, se agrega a una lista. Reiniciar pregunta antes de borrar la lista.

#### Criterio de aprobación

- Junta todos los errores y los muestra en un solo diálogo.
- Pregunta con `QMessageBox::question` antes de borrar.

#### Solución de referencia

```cpp
// R06-N02-M1 - La inscripcion al torneo: formulario con validacion y dialogos.
#include <QApplication>
#include <QComboBox>
#include <QDate>
#include <QDateEdit>
#include <QDialogButtonBox>
#include <QFormLayout>
#include <QLineEdit>
#include <QListWidget>
#include <QMessageBox>
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    QWidget ventana;
    ventana.setWindowTitle("Inscripción al torneo");
    auto* columna = new QVBoxLayout(&ventana);
    auto* form = new QFormLayout;
    auto* nombre = new QLineEdit;
    auto* correo = new QLineEdit;
    correo->setPlaceholderText("nombre@dominio.com");
    auto* nacimiento = new QDateEdit(QDate(2010, 1, 1));
    nacimiento->setCalendarPopup(true);
    auto* categoria = new QComboBox;
    categoria->addItems({"Infantil (hasta 12)", "Juvenil (13 a 17)", "Mayor (18 o más)"});
    form->addRow("Nombre *", nombre);
    form->addRow("Correo *", correo);
    form->addRow("Nacimiento", nacimiento);
    form->addRow("Categoría", categoria);
    auto* botones = new QDialogButtonBox(QDialogButtonBox::Ok | QDialogButtonBox::Reset);
    auto* inscriptos = new QListWidget;
    columna->addLayout(form);
    columna->addWidget(botones);
    columna->addWidget(inscriptos);

    auto errores = [=]() {
        QStringList e;
        if (nombre->text().trimmed().length() < 3) {
            e << "El nombre tiene que tener al menos 3 letras.";
        }
        QString c = correo->text().trimmed();
        int arroba = c.indexOf('@');
        if (arroba < 1 || c.indexOf('.', arroba) < arroba + 2 || c.endsWith('.')) {
            e << "El correo no parece válido.";
        }
        int edad = nacimiento->date().daysTo(QDate(2026, 12, 31)) / 365;
        int esperada = edad <= 12 ? 0 : edad <= 17 ? 1 : 2;
        if (categoria->currentIndex() != esperada) {
            e << QString("Con %1 años corresponde la categoría %2.").arg(edad).arg(categoria->itemText(esperada));
        }
        return e;
    };
    QObject::connect(botones, &QDialogButtonBox::accepted, &ventana, [=, &ventana] {
        QStringList e = errores();
        if (!e.isEmpty()) {
            QMessageBox::warning(&ventana, "Revisá los datos", e.join("\n"));
            return;
        }
        inscriptos->addItem(nombre->text().trimmed() + " - " + categoria->currentText());
        nombre->clear();
        correo->clear();
    });
    QObject::connect(botones->button(QDialogButtonBox::Reset), &QPushButton::clicked, &ventana, [=, &ventana] {
        if (QMessageBox::question(&ventana, "Borrar", "¿Borrar todas las inscripciones?") == QMessageBox::Yes) {
            inscriptos->clear();
        }
    });
    ventana.show();
    return app.exec();
}
```

### Misión R06-N02-M2 · Las tareas del taller

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, cpp, h, txt
```

#### Consigna

Una lista de tareas en una clase propia que hereda de `QWidget`: un `QLineEdit` (Enter o el botón agregan), un `QListWidget` con casillas para marcar las hechas y un botón "Borrar hechas". La lista se **guarda sola al cerrar** (`closeEvent`) en `tareas.txt` (una línea por tarea, con `x ` o `- ` adelante) y se **carga al abrir**.

#### Criterio de aprobación

- Guarda en `closeEvent` y carga en el constructor.
- Borra las hechas recorriendo de atrás para adelante.
- La primera vez, sin archivo, arranca vacía sin error.

#### Solución de referencia

```cpp
// R06-N02-M2 - La lista de tareas del taller: se guarda sola al cerrar y se carga al abrir.
#include <QApplication>
#include <QCloseEvent>
#include <QFile>
#include <QHBoxLayout>
#include <QLineEdit>
#include <QListWidget>
#include <QPushButton>
#include <QTextStream>
#include <QVBoxLayout>
#include <QWidget>

class Tareas : public QWidget {
public:
    Tareas()
    {
        setWindowTitle("Tareas del taller");
        auto* columna = new QVBoxLayout(this);
        auto* fila = new QHBoxLayout;
        texto_ = new QLineEdit;
        texto_->setPlaceholderText("Nueva tarea y Enter");
        auto* boton_agregar = new QPushButton("Agregar");
        auto* boton_borrar = new QPushButton("Borrar hechas");
        fila->addWidget(texto_);
        fila->addWidget(boton_agregar);
        lista_ = new QListWidget;
        columna->addLayout(fila);
        columna->addWidget(lista_);
        columna->addWidget(boton_borrar);
        connect(boton_agregar, &QPushButton::clicked, this, [this] { agregar(texto_->text(), false); texto_->clear(); });
        connect(texto_, &QLineEdit::returnPressed, this, [this] { agregar(texto_->text(), false); texto_->clear(); });
        connect(boton_borrar, &QPushButton::clicked, this, &Tareas::borrar_hechas);
        cargar();
    }

protected:
    void closeEvent(QCloseEvent* e) override       // se llama al cerrar la ventana
    {
        guardar();
        e->accept();
    }

private:
    void agregar(const QString& texto, bool hecha)
    {
        if (texto.trimmed().isEmpty()) {
            return;
        }
        auto* item = new QListWidgetItem(texto.trimmed(), lista_);
        item->setFlags(item->flags() | Qt::ItemIsUserCheckable);
        item->setCheckState(hecha ? Qt::Checked : Qt::Unchecked);
    }

    void borrar_hechas()
    {
        for (int i = lista_->count() - 1; i >= 0; i--) {        // de atras para adelante: los indices no se corren
            if (lista_->item(i)->checkState() == Qt::Checked) {
                delete lista_->takeItem(i);
            }
        }
    }

    void guardar() const
    {
        QFile f(RUTA);
        if (f.open(QIODevice::WriteOnly | QIODevice::Text)) {
            QTextStream out(&f);
            for (int i = 0; i < lista_->count(); i++) {
                out << (lista_->item(i)->checkState() == Qt::Checked ? "x " : "- ") << lista_->item(i)->text() << "\n";
            }
        }
    }

    void cargar()
    {
        QFile f(RUTA);
        if (!f.open(QIODevice::ReadOnly | QIODevice::Text)) {
            return;                                     // la primera vez no hay archivo
        }
        QTextStream in(&f);
        while (!in.atEnd()) {
            QString linea = in.readLine();
            if (linea.size() > 2) {
                agregar(linea.mid(2), linea.startsWith("x "));
            }
        }
    }

    inline static const QString RUTA = "tareas.txt";
    QLineEdit* texto_;
    QListWidget* lista_;
};

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    Tareas t;
    t.resize(380, 420);
    t.show();
    return app.exec();
}
```

### Encargo R06-N02-E1 · El conversor del almacén

```meta
entrega: archivo
entorno: local
monedas: 1
xp: 20
extensiones: zip, cpp, h, txt
```

#### Consigna

Un conversor de unidades para el almacén, con tres magnitudes (longitud, peso y volumen, cada una con sus unidades y un factor a la unidad base, guardadas en un `std::map<QString, std::vector<Unidad>>`). Al elegir la magnitud, los dos `QComboBox` de unidades se llenan con las de esa magnitud. El resultado se recalcula con cualquier cambio.

#### Criterio de aprobación

- Los datos de las unidades están en una estructura, no en `if`.
- Al cambiar de magnitud, se bloquean las señales mientras se llenan los combos.

#### Solución de referencia

```cpp
// R06-N02-E1 - El conversor de unidades del almacen.
#include <QApplication>
#include <QComboBox>
#include <QDoubleSpinBox>
#include <QGridLayout>
#include <QLabel>
#include <QWidget>

#include <map>
#include <vector>

struct Unidad {
    QString nombre;
    double factor;       // cuanto vale en la unidad base de su magnitud
};

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    const std::map<QString, std::vector<Unidad>> MAGNITUDES = {
        {"Longitud", {{"milímetros", 0.001}, {"centímetros", 0.01}, {"metros", 1}, {"kilómetros", 1000}, {"pulgadas", 0.0254}}},
        {"Peso", {{"gramos", 1}, {"kilos", 1000}, {"libras", 453.592}, {"onzas", 28.3495}}},
        {"Volumen", {{"mililitros", 1}, {"litros", 1000}, {"galones", 3785.41}, {"tazas", 250}}},
    };
    QWidget ventana;
    ventana.setWindowTitle("Conversor de unidades");
    auto* g = new QGridLayout(&ventana);
    auto* magnitud = new QComboBox;
    auto* desde = new QComboBox;
    auto* hasta = new QComboBox;
    auto* valor = new QDoubleSpinBox;
    valor->setRange(0, 1e9);
    valor->setDecimals(3);
    valor->setValue(1);
    auto* resultado = new QLabel;
    resultado->setStyleSheet("font-size: 20px;");
    for (const auto& [nombre, u] : MAGNITUDES) {
        magnitud->addItem(nombre);
    }
    g->addWidget(new QLabel("Magnitud"), 0, 0);
    g->addWidget(magnitud, 0, 1);
    g->addWidget(valor, 1, 0);
    g->addWidget(desde, 1, 1);
    g->addWidget(new QLabel("a"), 2, 0);
    g->addWidget(hasta, 2, 1);
    g->addWidget(resultado, 3, 0, 1, 2);

    auto convertir = [=, &MAGNITUDES] {
        const auto& unidades = MAGNITUDES.at(magnitud->currentText());
        if (desde->currentIndex() < 0 || hasta->currentIndex() < 0) {
            return;
        }
        double base = valor->value() * unidades[desde->currentIndex()].factor;
        double r = base / unidades[hasta->currentIndex()].factor;
        resultado->setText(QString("%1 %2 = %3 %4").arg(valor->value()).arg(desde->currentText()).arg(r, 0, 'g', 6).arg(hasta->currentText()));
    };
    auto cambiar_magnitud = [=, &MAGNITUDES] {
        desde->blockSignals(true);
        hasta->blockSignals(true);
        desde->clear();
        hasta->clear();
        for (const auto& u : MAGNITUDES.at(magnitud->currentText())) {
            desde->addItem(u.nombre);
            hasta->addItem(u.nombre);
        }
        hasta->setCurrentIndex(1);
        desde->blockSignals(false);
        hasta->blockSignals(false);
        convertir();
    };
    QObject::connect(magnitud, &QComboBox::currentIndexChanged, &ventana, cambiar_magnitud);
    QObject::connect(desde, &QComboBox::currentIndexChanged, &ventana, convertir);
    QObject::connect(hasta, &QComboBox::currentIndexChanged, &ventana, convertir);
    QObject::connect(valor, &QDoubleSpinBox::valueChanged, &ventana, convertir);
    cambiar_magnitud();
    ventana.show();
    return app.exec();
}
```

### Prueba del sello

#### ¿Qué partes trae un `QMainWindow`?

Menú, barras de herramientas, barra de estado y un widget central.

#### ¿Qué devuelve `QFileDialog::getSaveFileName` si el usuario cancela?

Un `QString` vacío.

#### ¿Por qué se borra de una lista recorriendo de atrás para adelante?

Porque al borrar un ítem los siguientes se corren, y hacia adelante se saltearía uno.

#### ¿Para qué sirve redefinir `closeEvent`?

Para hacer algo al cerrar la ventana (guardar, preguntar) y, si hace falta, cancelar el cierre con `ignore()`.

### Soluciones (docente)

Basado en `12-Qt-GUI/03-Widgets-Layouts` y en los mini proyectos de texto y utilidades de `Lab-Qt6`.

## R06-N03 · Tu clase detrás de la ventana

```meta
tipo: tema
padre: R06-N02
precio: 10
criatura: troll
ejecutable: no
temas: gui.tablas-arboles
usa: gui.qt, gui.componentes, poo.herencia, poo.polimorfismo, arch.texto
```

### Crónica

La oficina de patentes de la Ciudadela es un caos. Cada vez que alguien registra un invento, el empleado lo anota en la ventana… y nada más. Si se corta la luz, se pierde todo. Si alguien pregunta «¿cuánto vale todo lo registrado?», el empleado suma con los dedos.

Bron quiere arreglar la ventana. Tesla golpea el vidrio con el compás. —El problema no es la ventana: es que **la ventana es lo único que hay**. Primero va el plano: las clases, la herencia y el archivo, que funcionen solas en la consola. Después la ventana, que solo muestra lo que el plano sabe.

—¿Y la prueba? —pregunta la Maestra Artífice, que pasaba. —En la consola —contesta Bron, antes que Lima. La Maestra asiente. {mentor} se ríe.

### Objetivos

- Separar el **modelo** (tus clases de C++, sin nada de Qt) de la **vista** (la ventana).
- Mostrar una jerarquía de clases (herencia y polimorfismo) en una `QTableWidget`.
- Elegir qué clase derivada crear con un `QComboBox` y una función **fábrica**.
- Guardar y cargar los objetos en un archivo de texto, una línea por objeto.
- Convertir entre `QString` y `std::string`, y entre texto y números.

### Antes de empezar

Herencia y polimorfismo (rama 2), archivos y punteros inteligentes (rama 3) y los dos nodos anteriores.

### Explicación

#### Dos capas: el plano y la ventana
Un programa con ventanas tiene dos partes:
- **El modelo**: las clases que guardan los datos y hacen las cuentas (`Invento`, `Reloj`, `Registro`). Es C++ común: **no incluye nada de Qt**, y se puede probar en la consola con `cin` y `cout`.
- **La vista**: la ventana. Lee lo que escribe el usuario, se lo pasa al modelo y muestra lo que el modelo tiene.

¿Por qué separarlas?
- El modelo se prueba **sin hacer clic**: un `main` de consola alcanza.
- Si mañana cambia la ventana (otra tabla, otro diseño, una página web), las reglas no se tocan.
- En los parciales se corrige así: primero que las clases anden; después, la ventana.

#### La tabla: `QTableWidget`
```cpp
auto* tabla = new QTableWidget(0, 4);                    // 0 filas, 4 columnas
tabla->setHorizontalHeaderLabels({"Tipo", "Nombre", "Precio", "Valor"});
tabla->setEditTriggers(QAbstractItemView::NoEditTriggers);    // que no se escriba en las celdas
tabla->setSelectionBehavior(QAbstractItemView::SelectRows);   // un clic elige la fila entera
tabla->setRowCount(3);
tabla->setItem(0, 1, new QTableWidgetItem("Cucú"));      // fila 0, columna 1
int fila = tabla->currentRow();                          // la fila elegida, o -1 si no hay
```
Cada celda es un `QTableWidgetItem` creado con `new`: la tabla pasa a ser su dueña y lo borra cuando hace falta (como los widgets con padre).

#### Una sola verdad: `refrescar()`
El error más común es tener **dos copias** de los datos: el vector del modelo y las filas de la tabla, que se van separando. La solución: los datos viven **solo en el modelo**. Cada vez que algo cambia, una función `refrescar()` vuelve a llenar la tabla entera desde el modelo:
```cpp
void refrescar()
{
    const auto& inventos = registro_.todos();
    tabla_->setRowCount(static_cast<int>(inventos.size()));
    for (int f = 0; f < static_cast<int>(inventos.size()); f++) {
        tabla_->setItem(f, 1, new QTableWidgetItem(QString::fromStdString(inventos[f]->nombre())));
        // ... las otras columnas
    }
    total_->setText(QString("Valor total: %1").arg(registro_.total()));
}
```
Así, la fila `f` de la tabla es siempre el elemento `f` del vector: para quitar el invento elegido alcanza con `registro_.quitar(tabla_->currentRow())`.

#### La jerarquía en un vector
Los inventos son de distintas clases (`Reloj`, `Automata`), así que el registro guarda **punteros a la base**, y cada uno responde a su manera (polimorfismo):
```cpp
std::vector<std::unique_ptr<Invento>> inventos_;
inventos_.push_back(std::make_unique<Reloj>("Cucú", 100, 12));
int v = inventos_[0]->valor();          // llama a Reloj::valor()
```
`unique_ptr` es el dueño: al borrar el elemento del vector, el invento se destruye solo (por eso la base tiene **destructor virtual**).

#### La fábrica: de un texto, la clase que corresponde
El `QComboBox` da un texto (`"reloj"`), y el archivo también. Una función **fábrica** decide qué clase crear:
```cpp
std::unique_ptr<Invento> crear(const std::string& tipo, const std::string& nombre, int precio, int extra)
{
    if (tipo == "reloj") return std::make_unique<Reloj>(nombre, precio, extra);
    if (tipo == "automata") return std::make_unique<Automata>(nombre, precio, extra);
    return nullptr;                     // un tipo que no existe
}
```
Es el único lugar del programa que conoce **todas** las derivadas: para agregar una clase nueva se toca la jerarquía, la fábrica y el combo, y nada más.

#### Guardar y cargar objetos
Una línea por objeto, con los campos separados por `;` y **el tipo primero**, para saber qué clase crear al leer:
```
reloj;Cucu;100;12
automata;Pinza;120;20
```
Cada clase dice qué guardar con métodos virtuales (`tipo()`, `extra()`). Al leer, se parte la línea con `getline(campos, texto, ';')` y se le pasan los pedazos a la fábrica. El modelo usa `std::ofstream` y `std::ifstream`, así sigue sin depender de Qt; la ventana solo le pasa la ruta que eligió el usuario:
```cpp
QString ruta = QFileDialog::getSaveFileName(this, "Guardar", "inventos.txt", "Texto (*.txt)");
if (!ruta.isEmpty() && !registro_.guardar(ruta.toStdString())) { /* avisar */ }
```
Si un nombre puede tener `;`, rompe el archivo: validalo antes de agregarlo.

#### De texto a número
- `QString::number(42)` → `"42"`; `QString("%1 de %2").arg(a).arg(b)` arma frases.
- `texto.toInt(&ok)`: convierte y pone `ok` en `false` si el texto no era un número. Con un `QSpinBox` no hace falta: `value()` ya es un `int`.
- `std::stoi("42")` convierte un `std::string` (y lanza una excepción si no es un número).

### Código de ejemplo

```cpp
/*
 * R06-N03 - Tu clase detras de la ventana: el registro de inventos.
 * Arriba, el modelo (C++ puro, se prueba en consola); abajo, la ventana que lo muestra.
 */
#include <QApplication>
#include <QComboBox>
#include <QFileDialog>
#include <QFormLayout>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QLabel>
#include <QLineEdit>
#include <QMessageBox>
#include <QPushButton>
#include <QSpinBox>
#include <QTableWidget>
#include <QVBoxLayout>
#include <QWidget>

#include <fstream>
#include <memory>
#include <sstream>
#include <string>
#include <vector>

// ----- El modelo: no sabe nada de Qt -----

class Invento {
public:
    Invento(std::string nombre, int precio) : nombre_(std::move(nombre)), precio_(precio) {}
    virtual ~Invento() = default;
    const std::string& nombre() const { return nombre_; }
    int precio() const { return precio_; }
    virtual std::string tipo() const = 0;
    virtual int extra() const = 0;                       // las horas de cuerda o los pasos
    virtual int valor() const = 0;                       // cada clase lo calcula a su manera

private:
    std::string nombre_;
    int precio_;
};

class Reloj : public Invento {
public:
    Reloj(std::string nombre, int precio, int horas) : Invento(std::move(nombre), precio), horas_(horas) {}
    std::string tipo() const override { return "reloj"; }
    int extra() const override { return horas_; }
    int valor() const override { return precio() + horas_ * 2; }

private:
    int horas_;
};

class Automata : public Invento {
public:
    Automata(std::string nombre, int precio, int pasos) : Invento(std::move(nombre), precio), pasos_(pasos) {}
    std::string tipo() const override { return "automata"; }
    int extra() const override { return pasos_; }
    int valor() const override { return precio() * 2 + pasos_; }

private:
    int pasos_;
};

// La "fabrica": de la palabra del archivo, la clase que corresponde.
std::unique_ptr<Invento> crear(const std::string& tipo, const std::string& nombre, int precio, int extra)
{
    if (tipo == "reloj") {
        return std::make_unique<Reloj>(nombre, precio, extra);
    }
    if (tipo == "automata") {
        return std::make_unique<Automata>(nombre, precio, extra);
    }
    return nullptr;
}

class Registro {
public:
    void agregar(std::unique_ptr<Invento> i) { inventos_.push_back(std::move(i)); }
    void quitar(int fila) { inventos_.erase(inventos_.begin() + fila); }
    const std::vector<std::unique_ptr<Invento>>& todos() const { return inventos_; }

    int total() const
    {
        int t = 0;
        for (const auto& i : inventos_) {
            t += i->valor();
        }
        return t;
    }

    // Una linea por invento: tipo;nombre;precio;extra
    bool guardar(const std::string& ruta) const
    {
        std::ofstream f(ruta);
        if (!f) {
            return false;
        }
        for (const auto& i : inventos_) {
            f << i->tipo() << ';' << i->nombre() << ';' << i->precio() << ';' << i->extra() << '\n';
        }
        return true;
    }

    bool cargar(const std::string& ruta)
    {
        std::ifstream f(ruta);
        if (!f) {
            return false;
        }
        inventos_.clear();
        std::string linea;
        while (std::getline(f, linea)) {
            std::istringstream campos(linea);
            std::string tipo, nombre, precio, extra;
            std::getline(campos, tipo, ';');
            std::getline(campos, nombre, ';');
            std::getline(campos, precio, ';');
            std::getline(campos, extra);
            if (auto i = crear(tipo, nombre, std::stoi(precio), std::stoi(extra))) {
                agregar(std::move(i));
            }
        }
        return true;
    }

private:
    std::vector<std::unique_ptr<Invento>> inventos_;
};

// ----- La ventana: muestra el modelo y le pasa lo que hace el usuario -----

class VentanaRegistro : public QWidget {
public:
    VentanaRegistro()
    {
        setWindowTitle("Registro de inventos");
        tipo_ = new QComboBox;
        tipo_->addItems({"reloj", "automata"});
        nombre_ = new QLineEdit;
        precio_ = new QSpinBox;
        precio_->setRange(1, 9999);
        extra_ = new QSpinBox;
        extra_->setRange(0, 999);
        auto* form = new QFormLayout;
        form->addRow("Tipo", tipo_);
        form->addRow("Nombre", nombre_);
        form->addRow("Precio", precio_);
        form->addRow("Horas o pasos", extra_);

        tabla_ = new QTableWidget(0, 4);
        tabla_->setHorizontalHeaderLabels({"Tipo", "Nombre", "Precio", "Valor"});
        tabla_->setEditTriggers(QAbstractItemView::NoEditTriggers);   // se edita con el formulario, no en la tabla
        tabla_->setSelectionBehavior(QAbstractItemView::SelectRows);
        tabla_->horizontalHeader()->setStretchLastSection(true);
        total_ = new QLabel;

        auto* agregar = new QPushButton("Agregar");
        auto* quitar = new QPushButton("Quitar");
        auto* guardar = new QPushButton("Guardar...");
        auto* abrir = new QPushButton("Abrir...");
        auto* botones = new QHBoxLayout;
        for (auto* b : {agregar, quitar, guardar, abrir}) {
            botones->addWidget(b);
        }
        auto* columna = new QVBoxLayout(this);
        columna->addLayout(form);
        columna->addLayout(botones);
        columna->addWidget(tabla_);
        columna->addWidget(total_);

        connect(agregar, &QPushButton::clicked, this, &VentanaRegistro::agregar);
        connect(quitar, &QPushButton::clicked, this, &VentanaRegistro::quitar);
        connect(guardar, &QPushButton::clicked, this, &VentanaRegistro::guardar);
        connect(abrir, &QPushButton::clicked, this, &VentanaRegistro::abrir);
        refrescar();
    }

private:
    void agregar()
    {
        QString nombre = nombre_->text().trimmed();
        if (nombre.isEmpty()) {
            QMessageBox::warning(this, "Falta el nombre", "Escribí el nombre del invento.");
            return;
        }
        registro_.agregar(crear(tipo_->currentText().toStdString(), nombre.toStdString(), precio_->value(), extra_->value()));
        nombre_->clear();
        refrescar();
    }

    void quitar()
    {
        int fila = tabla_->currentRow();                 // -1 si no hay ninguna elegida
        if (fila < 0) {
            return;
        }
        registro_.quitar(fila);
        refrescar();
    }

    void guardar()
    {
        QString ruta = QFileDialog::getSaveFileName(this, "Guardar", "inventos.txt", "Texto (*.txt)");
        if (!ruta.isEmpty() && !registro_.guardar(ruta.toStdString())) {
            QMessageBox::critical(this, "Error", "No se pudo guardar en " + ruta);
        }
    }

    void abrir()
    {
        QString ruta = QFileDialog::getOpenFileName(this, "Abrir", "", "Texto (*.txt)");
        if (ruta.isEmpty()) {
            return;
        }
        if (!registro_.cargar(ruta.toStdString())) {
            QMessageBox::critical(this, "Error", "No se pudo abrir " + ruta);
        }
        refrescar();
    }

    // La tabla siempre se vuelve a llenar desde el modelo: nunca hay dos verdades.
    void refrescar()
    {
        const auto& inventos = registro_.todos();
        tabla_->setRowCount(static_cast<int>(inventos.size()));
        for (int f = 0; f < static_cast<int>(inventos.size()); f++) {
            const Invento& i = *inventos[f];
            tabla_->setItem(f, 0, new QTableWidgetItem(QString::fromStdString(i.tipo())));
            tabla_->setItem(f, 1, new QTableWidgetItem(QString::fromStdString(i.nombre())));
            tabla_->setItem(f, 2, new QTableWidgetItem(QString::number(i.precio())));
            tabla_->setItem(f, 3, new QTableWidgetItem(QString::number(i.valor())));
        }
        total_->setText(QString("Valor total: %1").arg(registro_.total()));
    }

    Registro registro_;
    QComboBox* tipo_;
    QLineEdit* nombre_;
    QSpinBox* precio_;
    QSpinBox* extra_;
    QTableWidget* tabla_;
    QLabel* total_;
};

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    VentanaRegistro ventana;
    ventana.resize(520, 480);
    ventana.show();
    return app.exec();
}
```

Compilalo con el mismo `CMakeLists.txt` de siempre (cambiá el nombre del ejecutable) y probá: agregá un reloj y un autómata, guardá, cerrá, volvé a abrir y cargá el archivo.

### ¿Para qué sirve?

Así están hechos los programas de gestión: un sistema de turnos, el inventario de un negocio, la ficha de los socios de un club. Las reglas viven en clases que se prueban solas, y la ventana es solo una forma de usarlas. Es también el examen típico de la UTN: un programa en Qt que maneja objetos de una jerarquía de clases y los guarda en un archivo.

### Errores habituales

**Troll: dos verdades.** Agregar una fila a la tabla **y** un objeto al vector por separado: tarde o temprano no coinciden (se borra de uno y no del otro). Cambiá solo el modelo y llamá a `refrescar()`.

**Orco: `currentRow()` vale -1.** Si no hay ninguna fila elegida, `quitar(-1)` borra fuera del vector. Revisá `fila < 0` antes.

**Troll: la base sin destructor virtual.** Con `unique_ptr<Invento>`, al destruir un `Reloj` se llama solo al destructor de `Invento` si no es `virtual`. El compilador avisa con `-Wall`:
```
warning: deleting object of abstract class type 'Invento' which has non-virtual destructor will cause undefined behavior
```

**Goblin: `QString` y `std::string` mezclados.** No se convierten solos:
```
error: no matching function for call to 'Registro::guardar(QString&)'
```
Usá `ruta.toStdString()` y `QString::fromStdString(texto)`.

**Ogro: el separador dentro de un dato.** Un nombre como `Reloj;de;pared` se lee como cuatro campos. Validá lo que escribe el usuario.

### Misión R06-N03-M1 · El plano sin ventana

```meta
entrega: codigo
entorno: local
monedas: 5
xp: 10
```

#### Consigna

Antes de la ventana, el modelo tiene que andar solo. Partí de las clases del ejemplo y agregá una tercera derivada: `Farol`, con su **luz** (un entero), que vale `precio + luz * 3`.

El programa lee de la entrada líneas `tipo nombre precio extra` (el nombre es una sola palabra) hasta que se terminen:
1. Crea cada invento con la fábrica. Si el tipo no existe, muestra `Tipo desconocido: <tipo>` y sigue.
2. Guarda todo en `inventos.txt` y muestra `Guardados: <cantidad>`.
3. Crea **otro** `Registro`, vacío, y lo carga desde `inventos.txt` (así se prueba que el archivo anda).
4. Muestra los inventos de esa copia ordenados por valor, de mayor a menor (a igual valor, por nombre), con el formato `tipo nombre: valor`, y al final `Valor total: <total>`.

#### Criterio de aprobación

- `Farol` hereda de `Invento` y redefine `tipo()`, `extra()` y `valor()`.
- La fábrica es el único lugar que conoce las tres derivadas.
- La lista sale del registro cargado desde el archivo, no del primero.
- Sin advertencias con `-Wall -Wextra`.

#### Entrada de ejemplo

```
reloj Cucu 100 12
automata Pinza 120 20
farol Lucero 80 15
barco Ancla 50 1
reloj Torre 236 12
```

#### Salida esperada

```
Tipo desconocido: barco
Guardados: 4
automata Pinza: 260
reloj Torre: 260
farol Lucero: 125
reloj Cucu: 124
Valor total: 769
```

#### Solución de referencia

```cpp
// R06-N03-M1 - El modelo sin ventana: la jerarquia de inventos, guardada y cargada de un archivo.
#include <algorithm>
#include <fstream>
#include <iostream>
#include <memory>
#include <sstream>
#include <string>
#include <vector>

class Invento {
public:
    Invento(std::string nombre, int precio) : nombre_(std::move(nombre)), precio_(precio) {}
    virtual ~Invento() = default;
    const std::string& nombre() const { return nombre_; }
    int precio() const { return precio_; }
    virtual std::string tipo() const = 0;
    virtual int extra() const = 0;
    virtual int valor() const = 0;

private:
    std::string nombre_;
    int precio_;
};

class Reloj : public Invento {
public:
    Reloj(std::string nombre, int precio, int horas) : Invento(std::move(nombre), precio), horas_(horas) {}
    std::string tipo() const override { return "reloj"; }
    int extra() const override { return horas_; }
    int valor() const override { return precio() + horas_ * 2; }

private:
    int horas_;
};

class Automata : public Invento {
public:
    Automata(std::string nombre, int precio, int pasos) : Invento(std::move(nombre), precio), pasos_(pasos) {}
    std::string tipo() const override { return "automata"; }
    int extra() const override { return pasos_; }
    int valor() const override { return precio() * 2 + pasos_; }

private:
    int pasos_;
};

class Farol : public Invento {
public:
    Farol(std::string nombre, int precio, int luz) : Invento(std::move(nombre), precio), luz_(luz) {}
    std::string tipo() const override { return "farol"; }
    int extra() const override { return luz_; }
    int valor() const override { return precio() + luz_ * 3; }

private:
    int luz_;
};

std::unique_ptr<Invento> crear(const std::string& tipo, const std::string& nombre, int precio, int extra)
{
    if (tipo == "reloj") {
        return std::make_unique<Reloj>(nombre, precio, extra);
    }
    if (tipo == "automata") {
        return std::make_unique<Automata>(nombre, precio, extra);
    }
    if (tipo == "farol") {
        return std::make_unique<Farol>(nombre, precio, extra);
    }
    return nullptr;
}

class Registro {
public:
    void agregar(std::unique_ptr<Invento> i) { inventos_.push_back(std::move(i)); }
    const std::vector<std::unique_ptr<Invento>>& todos() const { return inventos_; }

    int total() const
    {
        int t = 0;
        for (const auto& i : inventos_) {
            t += i->valor();
        }
        return t;
    }

    void ordenar()
    {
        std::sort(inventos_.begin(), inventos_.end(), [](const auto& a, const auto& b) {
            if (a->valor() != b->valor()) {
                return a->valor() > b->valor();
            }
            return a->nombre() < b->nombre();
        });
    }

    bool guardar(const std::string& ruta) const
    {
        std::ofstream f(ruta);
        if (!f) {
            return false;
        }
        for (const auto& i : inventos_) {
            f << i->tipo() << ';' << i->nombre() << ';' << i->precio() << ';' << i->extra() << '\n';
        }
        return true;
    }

    bool cargar(const std::string& ruta)
    {
        std::ifstream f(ruta);
        if (!f) {
            return false;
        }
        inventos_.clear();
        std::string linea;
        while (std::getline(f, linea)) {
            std::istringstream campos(linea);
            std::string tipo, nombre, precio, extra;
            std::getline(campos, tipo, ';');
            std::getline(campos, nombre, ';');
            std::getline(campos, precio, ';');
            std::getline(campos, extra);
            if (auto i = crear(tipo, nombre, std::stoi(precio), std::stoi(extra))) {
                agregar(std::move(i));
            }
        }
        return true;
    }

private:
    std::vector<std::unique_ptr<Invento>> inventos_;
};

int main()
{
    Registro taller;
    std::string tipo, nombre;
    int precio, extra;
    while (std::cin >> tipo >> nombre >> precio >> extra) {
        if (auto i = crear(tipo, nombre, precio, extra)) {
            taller.agregar(std::move(i));
        } else {
            std::cout << "Tipo desconocido: " << tipo << "\n";
        }
    }
    if (!taller.guardar("inventos.txt")) {
        std::cout << "No se pudo guardar\n";
        return 1;
    }
    std::cout << "Guardados: " << taller.todos().size() << "\n";

    Registro copia;                               // otro registro, solo con lo que quedo en el archivo
    copia.cargar("inventos.txt");
    copia.ordenar();
    for (const auto& i : copia.todos()) {
        std::cout << i->tipo() << " " << i->nombre() << ": " << i->valor() << "\n";
    }
    std::cout << "Valor total: " << copia.total() << "\n";
    return 0;
}
```

#### Pruebas

##### Un solo farol sin luz
```entrada
farol Uno 10 0
```
```salida
Guardados: 1
farol Uno: 10
Valor total: 10
```

##### Registro vacío
```entrada
```
```salida
Guardados: 0
Valor total: 0
```

##### Todos desconocidos
```entrada
barco Ancla 50 1
tren Rapido 9 9
```
```salida
Tipo desconocido: barco
Tipo desconocido: tren
Guardados: 0
Valor total: 0
```

### Misión R06-N03-M2 · La ventana del registro

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 10
extensiones: zip, cpp, h, txt
```

#### Consigna

Ahora sí, la ventana. Partí del código de ejemplo, con el modelo de la misión 1 (los tres tipos de invento), y agregale:
1. `farol` en el combo de tipos.
2. **Editar**: al elegir una fila, el formulario muestra ese invento; un botón «Guardar cambios» lo reemplaza por lo que dice el formulario (un método `reemplazar(fila, invento)` en `Registro`).
3. **No perder cambios**: si hay cambios sin guardar, al cerrar la ventana pregunta Guardar / Descartar / Cancelar (redefiní `closeEvent`).
4. Validar el nombre: ni vacío ni con `;`.

Entregá el proyecto en un `.zip` (el código y el `CMakeLists.txt`).

#### Criterio de aprobación

- La tabla se llena siempre desde el modelo (`refrescar()`), nunca a mano.
- Editar reemplaza el objeto, aunque cambie de tipo (un reloj que pasa a farol).
- Al cerrar con cambios pregunta, y «Cancelar» deja la ventana abierta.
- El modelo no incluye nada de Qt.

#### Solución de referencia

```cpp
// R06-N03-M2 - La ventana del registro: el modelo de la mision 1 con agregar, editar, quitar,
// guardar, abrir y la pregunta antes de cerrar con cambios sin guardar.
#include <QApplication>
#include <QCloseEvent>
#include <QComboBox>
#include <QFileDialog>
#include <QFormLayout>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QLabel>
#include <QLineEdit>
#include <QMessageBox>
#include <QPushButton>
#include <QSpinBox>
#include <QTableWidget>
#include <QVBoxLayout>
#include <QWidget>

#include <algorithm>
#include <fstream>
#include <memory>
#include <sstream>
#include <string>
#include <vector>

class Invento {
public:
    Invento(std::string nombre, int precio) : nombre_(std::move(nombre)), precio_(precio) {}
    virtual ~Invento() = default;
    const std::string& nombre() const { return nombre_; }
    int precio() const { return precio_; }
    virtual std::string tipo() const = 0;
    virtual int extra() const = 0;
    virtual int valor() const = 0;

private:
    std::string nombre_;
    int precio_;
};

class Reloj : public Invento {
public:
    Reloj(std::string nombre, int precio, int horas) : Invento(std::move(nombre), precio), horas_(horas) {}
    std::string tipo() const override { return "reloj"; }
    int extra() const override { return horas_; }
    int valor() const override { return precio() + horas_ * 2; }

private:
    int horas_;
};

class Automata : public Invento {
public:
    Automata(std::string nombre, int precio, int pasos) : Invento(std::move(nombre), precio), pasos_(pasos) {}
    std::string tipo() const override { return "automata"; }
    int extra() const override { return pasos_; }
    int valor() const override { return precio() * 2 + pasos_; }

private:
    int pasos_;
};

class Farol : public Invento {
public:
    Farol(std::string nombre, int precio, int luz) : Invento(std::move(nombre), precio), luz_(luz) {}
    std::string tipo() const override { return "farol"; }
    int extra() const override { return luz_; }
    int valor() const override { return precio() + luz_ * 3; }

private:
    int luz_;
};

std::unique_ptr<Invento> crear(const std::string& tipo, const std::string& nombre, int precio, int extra)
{
    if (tipo == "reloj") {
        return std::make_unique<Reloj>(nombre, precio, extra);
    }
    if (tipo == "automata") {
        return std::make_unique<Automata>(nombre, precio, extra);
    }
    if (tipo == "farol") {
        return std::make_unique<Farol>(nombre, precio, extra);
    }
    return nullptr;
}

class Registro {
public:
    void agregar(std::unique_ptr<Invento> i) { inventos_.push_back(std::move(i)); }
    void quitar(int fila) { inventos_.erase(inventos_.begin() + fila); }
    void reemplazar(int fila, std::unique_ptr<Invento> i) { inventos_[fila] = std::move(i); }
    const std::vector<std::unique_ptr<Invento>>& todos() const { return inventos_; }

    int total() const
    {
        int t = 0;
        for (const auto& i : inventos_) {
            t += i->valor();
        }
        return t;
    }

    void ordenar()
    {
        std::sort(inventos_.begin(), inventos_.end(), [](const auto& a, const auto& b) {
            if (a->valor() != b->valor()) {
                return a->valor() > b->valor();
            }
            return a->nombre() < b->nombre();
        });
    }

    bool guardar(const std::string& ruta) const
    {
        std::ofstream f(ruta);
        if (!f) {
            return false;
        }
        for (const auto& i : inventos_) {
            f << i->tipo() << ';' << i->nombre() << ';' << i->precio() << ';' << i->extra() << '\n';
        }
        return true;
    }

    bool cargar(const std::string& ruta)
    {
        std::ifstream f(ruta);
        if (!f) {
            return false;
        }
        inventos_.clear();
        std::string linea;
        while (std::getline(f, linea)) {
            std::istringstream campos(linea);
            std::string tipo, nombre, precio, extra;
            std::getline(campos, tipo, ';');
            std::getline(campos, nombre, ';');
            std::getline(campos, precio, ';');
            std::getline(campos, extra);
            if (auto i = crear(tipo, nombre, std::stoi(precio), std::stoi(extra))) {
                agregar(std::move(i));
            }
        }
        return true;
    }

private:
    std::vector<std::unique_ptr<Invento>> inventos_;
};

// ----- La ventana -----

class VentanaRegistro : public QWidget {
public:
    VentanaRegistro()
    {
        setWindowTitle("Registro de inventos");
        tipo_ = new QComboBox;
        tipo_->addItems({"reloj", "automata", "farol"});
        nombre_ = new QLineEdit;
        precio_ = new QSpinBox;
        precio_->setRange(1, 9999);
        extra_ = new QSpinBox;
        extra_->setRange(0, 999);
        auto* form = new QFormLayout;
        form->addRow("Tipo", tipo_);
        form->addRow("Nombre", nombre_);
        form->addRow("Precio", precio_);
        form->addRow("Horas, pasos o luz", extra_);

        tabla_ = new QTableWidget(0, 4);
        tabla_->setHorizontalHeaderLabels({"Tipo", "Nombre", "Precio", "Valor"});
        tabla_->setEditTriggers(QAbstractItemView::NoEditTriggers);   // se edita con el formulario, no en la tabla
        tabla_->setSelectionBehavior(QAbstractItemView::SelectRows);
        tabla_->horizontalHeader()->setStretchLastSection(true);
        total_ = new QLabel;

        auto* agregar = new QPushButton("Agregar");
        auto* editar = new QPushButton("Guardar cambios");
        auto* quitar = new QPushButton("Quitar");
        auto* guardar = new QPushButton("Guardar...");
        auto* abrir = new QPushButton("Abrir...");
        auto* botones = new QHBoxLayout;
        for (auto* b : {agregar, editar, quitar, guardar, abrir}) {
            botones->addWidget(b);
        }
        auto* columna = new QVBoxLayout(this);
        columna->addLayout(form);
        columna->addLayout(botones);
        columna->addWidget(tabla_);
        columna->addWidget(total_);

        connect(agregar, &QPushButton::clicked, this, &VentanaRegistro::agregar);
        connect(editar, &QPushButton::clicked, this, &VentanaRegistro::editar);
        connect(quitar, &QPushButton::clicked, this, &VentanaRegistro::quitar);
        connect(tabla_, &QTableWidget::currentCellChanged, this, &VentanaRegistro::elegir);
        connect(guardar, &QPushButton::clicked, this, [this] { this->guardar(); });   // "guardar" solo seria el boton local
        connect(abrir, &QPushButton::clicked, this, &VentanaRegistro::abrir);
        refrescar();
    }

protected:
    // Al cerrar con cambios sin guardar, se pregunta; "Cancelar" deja la ventana abierta.
    void closeEvent(QCloseEvent* e) override
    {
        if (!cambios_) {
            e->accept();
            return;
        }
        auto r = QMessageBox::question(this, "Cambios sin guardar", "¿Guardar antes de salir?",
                                       QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel);
        if (r == QMessageBox::Cancel || (r == QMessageBox::Save && !guardar())) {
            e->ignore();
            return;
        }
        e->accept();
    }

private:
    // Arma un invento con lo que dice el formulario (nullptr si falta el nombre).
    std::unique_ptr<Invento> del_formulario()
    {
        QString nombre = nombre_->text().trimmed();
        if (nombre.isEmpty() || nombre.contains(';')) {
            QMessageBox::warning(this, "Nombre inválido", "Escribí el nombre del invento (sin punto y coma).");
            return nullptr;
        }
        return crear(tipo_->currentText().toStdString(), nombre.toStdString(), precio_->value(), extra_->value());
    }

    void agregar()
    {
        if (auto i = del_formulario()) {
            registro_.agregar(std::move(i));
            nombre_->clear();
            cambios_ = true;
            refrescar();
        }
    }

    // Al elegir una fila, el formulario muestra ese invento para editarlo.
    void elegir(int fila)
    {
        if (fila < 0 || fila >= static_cast<int>(registro_.todos().size())) {
            return;
        }
        const Invento& i = *registro_.todos()[fila];
        tipo_->setCurrentText(QString::fromStdString(i.tipo()));
        nombre_->setText(QString::fromStdString(i.nombre()));
        precio_->setValue(i.precio());
        extra_->setValue(i.extra());
    }

    void editar()
    {
        int fila = tabla_->currentRow();
        if (fila < 0) {
            return;
        }
        if (auto i = del_formulario()) {
            registro_.reemplazar(fila, std::move(i));
            cambios_ = true;
            refrescar();
        }
    }

    void quitar()
    {
        int fila = tabla_->currentRow();                 // -1 si no hay ninguna elegida
        if (fila < 0) {
            return;
        }
        registro_.quitar(fila);
        cambios_ = true;
        refrescar();
    }

    bool guardar()
    {
        QString ruta = QFileDialog::getSaveFileName(this, "Guardar", "inventos.txt", "Texto (*.txt)");
        if (ruta.isEmpty()) {
            return false;
        }
        if (!registro_.guardar(ruta.toStdString())) {
            QMessageBox::critical(this, "Error", "No se pudo guardar en " + ruta);
            return false;
        }
        cambios_ = false;
        return true;
    }

    void abrir()
    {
        QString ruta = QFileDialog::getOpenFileName(this, "Abrir", "", "Texto (*.txt)");
        if (ruta.isEmpty()) {
            return;
        }
        if (!registro_.cargar(ruta.toStdString())) {
            QMessageBox::critical(this, "Error", "No se pudo abrir " + ruta);
        }
        cambios_ = false;
        refrescar();
    }

    // La tabla siempre se vuelve a llenar desde el modelo: nunca hay dos verdades.
    void refrescar()
    {
        const auto& inventos = registro_.todos();
        tabla_->setRowCount(static_cast<int>(inventos.size()));
        for (int f = 0; f < static_cast<int>(inventos.size()); f++) {
            const Invento& i = *inventos[f];
            tabla_->setItem(f, 0, new QTableWidgetItem(QString::fromStdString(i.tipo())));
            tabla_->setItem(f, 1, new QTableWidgetItem(QString::fromStdString(i.nombre())));
            tabla_->setItem(f, 2, new QTableWidgetItem(QString::number(i.precio())));
            tabla_->setItem(f, 3, new QTableWidgetItem(QString::number(i.valor())));
        }
        total_->setText(QString("Valor total: %1").arg(registro_.total()));
    }

    Registro registro_;
    bool cambios_ = false;
    QComboBox* tipo_;
    QLineEdit* nombre_;
    QSpinBox* precio_;
    QSpinBox* extra_;
    QTableWidget* tabla_;
    QLabel* total_;
};

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    VentanaRegistro ventana;
    ventana.resize(520, 480);
    ventana.show();
    return app.exec();
}
```

### Encargo R06-N03-E1 · La agenda de la Ciudadela

```meta
entrega: archivo
entorno: local
monedas: 1
xp: 40
extensiones: zip, cpp, h, txt
```

#### Consigna

Una agenda de contactos (nombre, teléfono y correo):
- Un `struct Contacto` con un método `coincide(texto)` que diga si el texto aparece en alguno de los tres campos, sin importar mayúsculas.
- Una clase `Agenda` que guarda los contactos en un `std::vector` y los lee y escribe en `contactos.txt` (una línea por contacto, separada por `;`). Si el archivo no existe, arranca con dos contactos de ejemplo.
- Una ventana con un campo de **búsqueda** que esconde las filas que no coinciden (`setRowHidden`), sin borrar nada; un formulario para agregar; un botón para borrar el elegido (preguntando antes).
- Guarda al cerrar.

#### Criterio de aprobación

- La búsqueda esconde filas: no toca los datos.
- Borrar pregunta y quita el contacto del modelo, no solo de la tabla.
- Lo que se agrega sigue ahí al volver a abrir el programa.

#### Solución de referencia

```cpp
// R06-N03-E1 - La agenda de la Ciudadela: una clase Contacto, un archivo de texto y una tabla que se filtra.
#include <QApplication>
#include <QFormLayout>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QLineEdit>
#include <QMessageBox>
#include <QPushButton>
#include <QTableWidget>
#include <QVBoxLayout>
#include <QWidget>

#include <cctype>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

struct Contacto {
    std::string nombre;
    std::string telefono;
    std::string correo;

    // ¿Aparece el texto (ya en minusculas) en alguno de los tres campos?
    bool coincide(const std::string& buscado) const
    {
        for (std::string campo : {nombre, telefono, correo}) {
            for (char& c : campo) {
                c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
            }
            if (campo.find(buscado) != std::string::npos) {
                return true;
            }
        }
        return false;
    }
};

class Agenda {
public:
    explicit Agenda(std::string ruta) : ruta_(std::move(ruta)) {}

    void agregar(const Contacto& c) { contactos_.push_back(c); }
    void quitar(int i) { contactos_.erase(contactos_.begin() + i); }
    const std::vector<Contacto>& todos() const { return contactos_; }

    void cargar()
    {
        std::ifstream f(ruta_);
        if (!f) {                                        // la primera vez: dos de ejemplo
            agregar({"Tesla", "3804-000001", "tesla@ciudadela.ar"});
            agregar({"Maese Ferrum", "3804-000002", "ferrum@forjas.ar"});
            return;
        }
        std::string linea;
        while (std::getline(f, linea)) {
            std::istringstream campos(linea);
            Contacto c;
            std::getline(campos, c.nombre, ';');
            std::getline(campos, c.telefono, ';');
            std::getline(campos, c.correo);
            agregar(c);
        }
    }

    bool guardar() const
    {
        std::ofstream f(ruta_);
        for (const Contacto& c : contactos_) {
            f << c.nombre << ';' << c.telefono << ';' << c.correo << '\n';
        }
        return static_cast<bool>(f);
    }

private:
    std::string ruta_;
    std::vector<Contacto> contactos_;
};

class VentanaAgenda : public QWidget {
public:
    VentanaAgenda() : agenda_("contactos.txt")
    {
        setWindowTitle("Agenda de la Ciudadela");
        buscar_ = new QLineEdit;
        buscar_->setPlaceholderText("Buscar...");
        nombre_ = new QLineEdit;
        telefono_ = new QLineEdit;
        correo_ = new QLineEdit;
        auto* form = new QFormLayout;
        form->addRow("Nombre", nombre_);
        form->addRow("Teléfono", telefono_);
        form->addRow("Correo", correo_);
        auto* boton_agregar = new QPushButton("Agregar");
        auto* boton_borrar = new QPushButton("Borrar");
        auto* botones = new QHBoxLayout;
        botones->addWidget(boton_agregar);
        botones->addWidget(boton_borrar);
        tabla_ = new QTableWidget(0, 3);
        tabla_->setHorizontalHeaderLabels({"Nombre", "Teléfono", "Correo"});
        tabla_->setEditTriggers(QAbstractItemView::NoEditTriggers);
        tabla_->setSelectionBehavior(QAbstractItemView::SelectRows);
        tabla_->horizontalHeader()->setStretchLastSection(true);
        auto* columna = new QVBoxLayout(this);
        columna->addWidget(buscar_);
        columna->addLayout(form);
        columna->addLayout(botones);
        columna->addWidget(tabla_);

        connect(boton_agregar, &QPushButton::clicked, this, &VentanaAgenda::agregar);
        connect(boton_borrar, &QPushButton::clicked, this, &VentanaAgenda::borrar);
        connect(buscar_, &QLineEdit::textChanged, this, &VentanaAgenda::filtrar);
        agenda_.cargar();
        refrescar();
    }

    ~VentanaAgenda() override { agenda_.guardar(); }   // guarda al cerrar

private:
    void agregar()
    {
        Contacto c{nombre_->text().trimmed().toStdString(), telefono_->text().trimmed().toStdString(),
                   correo_->text().trimmed().toStdString()};
        if (c.nombre.empty() || c.nombre.find(';') != std::string::npos) {
            QMessageBox::warning(this, "Nombre inválido", "Escribí el nombre (sin punto y coma).");
            return;
        }
        agenda_.agregar(c);
        for (auto* campo : {nombre_, telefono_, correo_}) {
            campo->clear();
        }
        refrescar();
    }

    void borrar()
    {
        int fila = tabla_->currentRow();
        if (fila < 0 || tabla_->isRowHidden(fila)) {
            return;
        }
        if (QMessageBox::question(this, "Borrar", "¿Borrar el contacto?") == QMessageBox::Yes) {
            agenda_.quitar(fila);                        // la fila de la tabla es la del vector: no se reordena
            refrescar();
        }
    }

    // Filtrar no borra nada: solo esconde las filas que no coinciden.
    void filtrar()
    {
        std::string buscado = buscar_->text().trimmed().toLower().toStdString();
        for (int f = 0; f < tabla_->rowCount(); f++) {
            tabla_->setRowHidden(f, !agenda_.todos()[f].coincide(buscado));
        }
    }

    void refrescar()
    {
        const auto& todos = agenda_.todos();
        tabla_->setRowCount(static_cast<int>(todos.size()));
        for (int f = 0; f < static_cast<int>(todos.size()); f++) {
            tabla_->setItem(f, 0, new QTableWidgetItem(QString::fromStdString(todos[f].nombre)));
            tabla_->setItem(f, 1, new QTableWidgetItem(QString::fromStdString(todos[f].telefono)));
            tabla_->setItem(f, 2, new QTableWidgetItem(QString::fromStdString(todos[f].correo)));
        }
        filtrar();
    }

    Agenda agenda_;
    QLineEdit* buscar_;
    QLineEdit* nombre_;
    QLineEdit* telefono_;
    QLineEdit* correo_;
    QTableWidget* tabla_;
};

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    VentanaAgenda ventana;
    ventana.resize(560, 420);
    ventana.show();
    return app.exec();
}
```

### Prueba del sello

#### ¿Qué ventaja tiene que el modelo no incluya nada de Qt?

Se prueba en la consola, sin ventanas, y se puede usar con otra interfaz sin cambiarlo.

#### ¿Por qué la tabla se vuelve a llenar entera en vez de agregar una fila?

Para que los datos vivan en un solo lugar (el modelo) y la tabla nunca muestre algo distinto.

#### ¿Para qué sirve la función fábrica?

Para crear la clase derivada que corresponde a un texto (del combo o del archivo), en un solo lugar.

#### ¿Por qué el tipo va primero en cada línea del archivo?

Porque al leer hay que saber qué clase crear antes de interpretar el resto de los campos.

#### ¿Qué devuelve `currentRow()` si no hay nada elegido?

-1.

### Soluciones (docente)

Nodo nuevo (2026-10-08) para el examen típico de la UTN: Qt + una jerarquía de clases + archivo, sin bases de datos. M1 se corrige con las pruebas (el modelo solo, en consola); M2 y E1 compilando con CMake + AUTOMOC contra Qt 6 y probándolos.

## R06-N04 · Dibujar, el mouse y el modelo-vista

```meta
tipo: tema
padre: R06-N03
precio: 10
criatura: orco
ejecutable: no
temas: gui.dibujo, gui.modelo-vista
usa: gui.qt
```

### Crónica

En el fondo del Taller, un maestro vidriero no usa piezas hechas: pinta cada vitral a mano, con pinceles de luz. A su lado, Lima lleva la lista de cada pieza en un cuaderno; cuando el maestro agrega un vidrio, el cuaderno se actualiza solo.

Bron, que llegó a la Ciudadela arreglando doscientos engranajes a mano, descubre que hay cosas que **sí** se hacen a mano: dibujar. Le pregunta al maestro vidriero si conoce al Vidriero. El maestro se ríe: —Todos los vidrieros conocemos al Vidriero. Nadie lo vio nunca.

—Cuando los botones no alcanzan, se **dibuja** —dice {mentor}—. Y cuando los datos son muchos, se separan: los **datos** por un lado, y las **vistas** que los muestran, por otro.

### Objetivos

- Crear widgets propios que se dibujan con `QPainter` (`paintEvent`) y responden al mouse y al teclado.
- Animar con `QTimer` y `update()`.
- Separar los datos de su presentación con el **modelo-vista** de Qt (`QStringListModel`, `QStandardItemModel`, `QListView`, `QTableView`).

### Antes de empezar

Formularios, menús y archivos (nodo anterior). Herencia y métodos virtuales (rama 2).

### Explicación

#### Un widget que se dibuja solo
Se hereda de `QWidget` y se redefine `paintEvent`. Qt lo llama **cada vez que hace falta dibujar** (al mostrarse, al cambiar de tamaño, o cuando lo pedís con `update()`):
```cpp
class Vitral : public QWidget {
protected:
    void paintEvent(QPaintEvent*) override
    {
        QPainter p(this);                          // el pincel, para este widget
        p.setRenderHint(QPainter::Antialiasing);   // bordes suaves
        p.fillRect(rect(), QColor(20, 20, 35));
        p.setBrush(Qt::red);  p.setPen(QPen(Qt::black, 3));
        p.drawEllipse(QPointF(100, 100), 28, 28);
    }
};
```
Nunca se dibuja fuera de `paintEvent`: se cambian los datos y se llama a `update()`, que **pide** redibujar (Qt junta varios pedidos en uno).

`QPainter` sabe `drawLine`, `drawRect`, `fillRect`, `drawEllipse`, `drawText`, `drawPixmap`… y **transformar** el sistema de coordenadas: `translate` (mover el origen), `rotate` (girar, en grados), `scale`. Con `save()`/`restore()` se vuelve al estado anterior. Un reloj analógico es "trasladar al centro y rotar según la hora".

#### El mouse y el teclado
Se redefinen métodos virtuales:
- `mousePressEvent(QMouseEvent* e)`: `e->position()` (dónde), `e->button()` (qué botón).
- `mouseMoveEvent`: llega mientras hay un botón apretado (o siempre, con `setMouseTracking(true)`); `e->buttons()` dice cuáles están apretados.
- `keyPressEvent(QKeyEvent* e)`: `e->key()` (por ejemplo `Qt::Key_1`). Para recibir el teclado, el widget necesita el foco: `setFocusPolicy(Qt::StrongFocus)`.

#### Animar
Un `QTimer` que cada 30 ms cambia algo y llama a `update()`. No hay bucle propio: el temporizador es un evento más.

#### Modelo-vista
Cuando hay muchos datos, Qt separa:
- el **modelo**: los datos (`QStringListModel` para una lista de textos, `QStandardItemModel` para tablas);
- la **vista**: cómo se muestran (`QListView`, `QTableView`, `QTreeView`).

La vista se conecta con `vista->setModel(modelo)`. Cuando el **modelo** cambia (desde el código o porque el usuario editó una celda), **todas** las vistas se actualizan solas, y el modelo emite señales (`dataChanged`, `rowsInserted`, `rowsRemoved`) para que otras partes reaccionen (por ejemplo, recalcular un total). Es la misma idea que separar la lógica del dibujo en un juego.

Entre el modelo y la vista puede ir un **proxy**, como `QSortFilterProxyModel`, que filtra y ordena sin tocar los datos originales. Ojo: los índices de la vista son los del proxy; para llegar al modelo, `mapToSource`.

(`QListWidget` y `QTableWidget`, del nodo anterior, son versiones "todo en uno" con el modelo adentro: más simples, pero menos flexibles.)

#### Cómo compilarlo y ejecutarlo

Abre una ventana, así que se compila en tu compu con el `CMakeLists.txt` del primer nodo de la rama:
- **Qt Creator** (Linux y Windows): abrí el `CMakeLists.txt` y apretá **Ctrl+R**.
- **Terminal:** `cmake -B build && cmake --build build`, y después `./build/vitrales` (Linux) o `build\vitrales.exe` (Windows).

### Código de ejemplo

```cpp
/*
 * R06-N04 - Dibujar con QPainter, el mouse, QTimer y el modelo-vista.
 * Un vitral que se pinta con clics (widget propio) y la lista de piezas en una QListView.
 */
#include <QApplication>
#include <QHBoxLayout>
#include <QListView>
#include <QMouseEvent>
#include <QPainter>
#include <QStringListModel>
#include <QTimer>
#include <QWidget>

#include <algorithm>
#include <cmath>
#include <utility>
#include <vector>

class Vitral : public QWidget {
public:
    explicit Vitral(QStringListModel* piezas) : piezas_(piezas)
    {
        setMinimumSize(400, 400);
        auto* reloj = new QTimer(this);                  // el reloj es hijo del widget: se libera con el
        connect(reloj, &QTimer::timeout, this, [this] {
            angulo_ += 2;
            update();                                     // pide redibujar: Qt llamara a paintEvent
        });
        reloj->start(30);
    }

protected:
    // Qt llama a paintEvent cada vez que hay que dibujar el widget.
    void paintEvent(QPaintEvent*) override
    {
        QPainter p(this);
        p.setRenderHint(QPainter::Antialiasing);
        p.fillRect(rect(), QColor(20, 20, 35));
        for (const auto& [centro, color] : vidrios_) {
            p.setBrush(color);
            p.setPen(QPen(Qt::black, 3));
            p.drawEllipse(centro, 28, 28);
        }
        // Un rayo de luz que gira alrededor del centro
        p.save();
        p.translate(width() / 2.0, height() / 2.0);
        p.rotate(angulo_);
        p.setPen(QPen(QColor(255, 240, 180, 160), 6));
        p.drawLine(0, 0, 0, -std::min(width(), height()) / 2);
        p.restore();
    }

    void mousePressEvent(QMouseEvent* e) override
    {
        static const QColor COLORES[] = {QColor(200, 60, 60), QColor(60, 120, 220), QColor(240, 200, 60), QColor(60, 180, 90)};
        QColor c = COLORES[vidrios_.size() % 4];
        if (e->button() == Qt::RightButton && !vidrios_.empty()) {
            vidrios_.pop_back();                          // derecho: saca el ultimo
            piezas_->removeRows(piezas_->rowCount() - 1, 1);
        } else if (e->button() == Qt::LeftButton) {
            vidrios_.push_back({e->position(), c});
            piezas_->insertRows(piezas_->rowCount(), 1);  // el MODELO cambia; la vista se entera sola
            piezas_->setData(piezas_->index(piezas_->rowCount() - 1), QString("vidrio %1 en (%2, %3)")
                             .arg(vidrios_.size()).arg(e->position().x(), 0, 'f', 0).arg(e->position().y(), 0, 'f', 0));
        }
        update();
    }

private:
    QStringListModel* piezas_;
    std::vector<std::pair<QPointF, QColor>> vidrios_;
    double angulo_ = 0;
};

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    QWidget ventana;
    ventana.setWindowTitle("El vitral");
    auto* fila = new QHBoxLayout(&ventana);
    auto* modelo = new QStringListModel(&ventana);        // los DATOS
    auto* vista = new QListView;                          // una forma de MOSTRARLOS
    vista->setModel(modelo);
    vista->setMaximumWidth(220);
    fila->addWidget(new Vitral(modelo));
    fila->addWidget(vista);
    ventana.show();
    return app.exec();
}
```

### ¿Para qué sirve?

Los widgets dibujados a mano están en los editores gráficos, los gráficos de datos, los relojes y medidores, los editores de mapas y los visores de imágenes. El modelo-vista es la base de cualquier aplicación que muestra tablas grandes: planillas, administradores de archivos, clientes de correo, listas de productos con filtros.

### Errores habituales

**Ogro: dibujar fuera de `paintEvent`.** Un `QPainter` creado en un slot no muestra nada (o da advertencias). Cambiá los datos y llamá a `update()`.

**Ogro: olvidar `update()`.** Los datos cambian y la pantalla no: falta pedir el redibujo.

**Ogro: el teclado que no llega.** Un widget propio sin `setFocusPolicy` no recibe `keyPressEvent`.

**Ogro: `save()` sin `restore()`.** Las transformaciones se acumulan y todo lo que se dibuja después sale girado.

**Orco: usar el índice de la vista en el modelo.** Con un proxy de filtro, la fila 2 de la vista puede ser la fila 7 del modelo: siempre `mapToSource`.

### Misión R06-N04-M1 · El editor de baldosas

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, cpp, h, txt
```

#### Consigna

Un widget propio con una grilla de 24 × 16 baldosas que se pintan con el mouse (se puede **arrastrar**; el botón derecho borra). Las teclas `1` a `4` eligen el pincel: piso, pared, agua, tesoro, cada uno con su color. El título muestra cuántos tesoros hay. Los datos están en un `std::vector<std::string>`, y `paintEvent` solo los dibuja.

#### Criterio de aprobación

- Pinta arrastrando con `mouseMoveEvent` y `buttons()`.
- Recibe el teclado (`setFocusPolicy`).
- Solo llama a `update()` si algo cambió.

#### Solución de referencia

```cpp
// R06-N04-M1 - El editor de baldosas: pintar una grilla arrastrando el mouse.
#include <QApplication>
#include <QKeyEvent>
#include <QMouseEvent>
#include <QPainter>
#include <QWidget>

#include <algorithm>
#include <map>
#include <string>
#include <vector>

class Grilla : public QWidget {
public:
    Grilla(int columnas, int filas) : columnas_(columnas), filas_(filas), celdas_(filas, std::string(columnas, '.'))
    {
        setFixedSize(columnas * LADO, filas * LADO + 24);
        setFocusPolicy(Qt::StrongFocus);                  // para recibir el teclado
        actualizar_titulo();
    }

protected:
    void paintEvent(QPaintEvent*) override
    {
        static const std::map<char, QColor> COLORES = {{'.', QColor(230, 225, 210)}, {'#', QColor(80, 70, 60)}, {'~', QColor(70, 130, 210)}, {'*', QColor(240, 200, 60)}};
        QPainter p(this);
        for (int f = 0; f < filas_; f++) {
            for (int c = 0; c < columnas_; c++) {
                p.fillRect(c * LADO, f * LADO, LADO - 1, LADO - 1, COLORES.at(celdas_[f][c]));
            }
        }
        p.setPen(Qt::black);
        p.drawText(4, filas_ * LADO + 17, QString("Pincel: %1   (1 piso, 2 pared, 3 agua, 4 tesoro; derecho borra)").arg(pincel_));
    }

    void mousePressEvent(QMouseEvent* e) override { pintar(e); }
    void mouseMoveEvent(QMouseEvent* e) override { pintar(e); }     // solo llega con un boton apretado

    void keyPressEvent(QKeyEvent* e) override
    {
        const std::string PINCELES = ".#~*";
        int n = e->key() - Qt::Key_1;
        if (n >= 0 && n < static_cast<int>(PINCELES.size())) {
            pincel_ = PINCELES[n];
            update();
        }
    }

private:
    void pintar(QMouseEvent* e)
    {
        int c = static_cast<int>(e->position().x()) / LADO;
        int f = static_cast<int>(e->position().y()) / LADO;
        if (c < 0 || c >= columnas_ || f < 0 || f >= filas_) {
            return;
        }
        char nuevo = (e->buttons() & Qt::RightButton) ? '.' : pincel_;
        if (celdas_[f][c] != nuevo) {
            celdas_[f][c] = nuevo;
            actualizar_titulo();
            update();
        }
    }

    void actualizar_titulo()
    {
        int tesoros = 0;
        for (const auto& fila : celdas_) {
            tesoros += static_cast<int>(std::count(fila.begin(), fila.end(), '*'));
        }
        setWindowTitle(QString("Editor de baldosas - %1 tesoros").arg(tesoros));
    }

    static constexpr int LADO = 24;
    int columnas_;
    int filas_;
    std::vector<std::string> celdas_;
    char pincel_ = '#';
};

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    Grilla g(24, 16);
    g.show();
    return app.exec();
}
```

### Misión R06-N04-M2 · El reloj de la torre

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, cpp, h, txt
```

#### Consigna

Un reloj analógico: la esfera, 60 marcas (largas cada 5) y tres agujas (horas, minutos y segundos, esta roja), dibujadas con `translate`, `rotate` y `save`/`restore`. Se escala según el tamaño de la ventana (dibujá en un "mundo" de 200 × 200 con `scale`). Un `QTimer` lo actualiza cada segundo. La hora sale de `QTime::currentTime()`.

#### Criterio de aprobación

- Usa transformaciones en vez de calcular senos y cosenos a mano.
- Se adapta al tamaño de la ventana.
- La aguja de las horas avanza también con los minutos.

#### Solución de referencia

```cpp
// R06-N04-M2 - El reloj de la torre: QPainter con translate/rotate y un QTimer.
#include <QApplication>
#include <QPainter>
#include <QTime>
#include <QTimer>
#include <QWidget>

#include <algorithm>

class Reloj : public QWidget {
public:
    Reloj()
    {
        setWindowTitle("El reloj de la torre");
        resize(360, 360);
        auto* t = new QTimer(this);
        connect(t, &QTimer::timeout, this, qOverload<>(&QWidget::update));
        t->start(1000);
    }

protected:
    void paintEvent(QPaintEvent*) override
    {
        QTime ahora = QTime::currentTime();
        int lado = std::min(width(), height());
        QPainter p(this);
        p.setRenderHint(QPainter::Antialiasing);
        p.translate(width() / 2.0, height() / 2.0);
        p.scale(lado / 200.0, lado / 200.0);               // dibujamos en un "mundo" de 200 x 200
        p.setBrush(QColor(245, 235, 210));
        p.setPen(QPen(QColor(90, 60, 30), 4));
        p.drawEllipse(QPointF(0, 0), 95, 95);
        for (int i = 0; i < 60; i++) {                     // marcas: largas cada 5 minutos
            p.drawLine(0, i % 5 == 0 ? -80 : -86, 0, -92);
            p.rotate(6);
        }
        auto aguja = [&p](double angulo, int largo, int grosor, QColor color) {
            p.save();
            p.rotate(angulo);
            p.setPen(QPen(color, grosor, Qt::SolidLine, Qt::RoundCap));
            p.drawLine(0, 12, 0, -largo);
            p.restore();
        };
        aguja(30.0 * (ahora.hour() % 12) + ahora.minute() / 2.0, 50, 7, QColor(40, 30, 20));
        aguja(6.0 * ahora.minute(), 75, 5, QColor(40, 30, 20));
        aguja(6.0 * ahora.second(), 82, 2, QColor(200, 40, 40));
    }
};

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    Reloj r;
    r.show();
    return app.exec();
}
```

### Encargo R06-N04-E1 · La planilla de gastos

```meta
entrega: archivo
entorno: local
monedas: 1
xp: 20
extensiones: zip, cpp, h, txt
```

#### Consigna

Una planilla de gastos del hogar con un `QStandardItemModel` (concepto, categoría, monto) y un `QTableView` editable y ordenable. Botones para agregar una fila y quitar la seleccionada. El total (y la cantidad de gastos) se recalcula **solo**, escuchando las señales del modelo, aunque el cambio venga de editar una celda a mano.

#### Criterio de aprobación

- El total se actualiza con las señales del modelo, no desde cada botón.
- El monto se guarda como número (`Qt::EditRole`), no como texto.

#### Solución de referencia

```cpp
// R06-N04-E1 - La planilla de gastos del hogar: modelo-vista con una tabla editable.
#include <QApplication>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QLabel>
#include <QPushButton>
#include <QStandardItemModel>
#include <QTableView>
#include <QVBoxLayout>
#include <QWidget>

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    QWidget ventana;
    ventana.setWindowTitle("Gastos del mes");
    auto* columna = new QVBoxLayout(&ventana);
    auto* modelo = new QStandardItemModel(0, 3, &ventana);
    modelo->setHorizontalHeaderLabels({"Concepto", "Categoría", "Monto"});
    auto agregar_fila = [modelo](const QString& concepto, const QString& categoria, double monto) {
        auto* m = new QStandardItem;
        m->setData(monto, Qt::EditRole);                 // un numero: el editor sera un campo numerico
        modelo->appendRow({new QStandardItem(concepto), new QStandardItem(categoria), m});
    };
    agregar_fila("Alquiler", "Casa", 350000);
    agregar_fila("Luz", "Servicios", 42000);
    agregar_fila("Supermercado", "Comida", 180000);

    auto* tabla = new QTableView;
    tabla->setModel(modelo);
    tabla->horizontalHeader()->setStretchLastSection(true);
    tabla->setSortingEnabled(true);
    auto* total = new QLabel;
    auto* fila = new QHBoxLayout;
    auto* nueva = new QPushButton("Nueva fila");
    auto* quitar = new QPushButton("Quitar seleccionada");
    fila->addWidget(nueva);
    fila->addWidget(quitar);
    columna->addWidget(tabla);
    columna->addLayout(fila);
    columna->addWidget(total);

    auto recalcular = [modelo, total] {
        double suma = 0;
        for (int r = 0; r < modelo->rowCount(); r++) {
            suma += modelo->item(r, 2)->data(Qt::EditRole).toDouble();
        }
        total->setText(QString("Total: $ %1  (%2 gastos)").arg(suma, 0, 'f', 2).arg(modelo->rowCount()));
    };
    // El modelo avisa cuando cambian sus datos: el total se recalcula solo, lo edite quien lo edite.
    QObject::connect(modelo, &QStandardItemModel::dataChanged, &ventana, recalcular);
    QObject::connect(modelo, &QStandardItemModel::rowsInserted, &ventana, recalcular);
    QObject::connect(modelo, &QStandardItemModel::rowsRemoved, &ventana, recalcular);
    QObject::connect(nueva, &QPushButton::clicked, &ventana, [=] { agregar_fila("Nuevo gasto", "Varios", 0); });
    QObject::connect(quitar, &QPushButton::clicked, &ventana, [=] {
        QModelIndex actual = tabla->currentIndex();
        if (actual.isValid()) {
            modelo->removeRow(actual.row());
        }
    });
    recalcular();
    ventana.resize(480, 360);
    ventana.show();
    return app.exec();
}
```

### Prueba del sello

#### ¿Cuándo llama Qt a `paintEvent`?

Cuando hace falta dibujar el widget: al mostrarse, al cambiar de tamaño o después de un `update()`.

#### ¿Qué hace `update()`?

Pide que el widget se redibuje; Qt llama a `paintEvent` cuando puede.

#### ¿Para qué sirven `save()` y `restore()` en `QPainter`?

Para guardar el estado (transformaciones, pinceles) y volver a él después.

#### ¿Qué ventaja tiene separar modelo y vista?

Varias vistas muestran los mismos datos y se actualizan solas cuando el modelo cambia.

#### ¿Qué hace un `QSortFilterProxyModel`?

Filtra y ordena los datos de otro modelo sin modificarlo.

### Soluciones (docente)

Basado en `12-Qt-GUI/04-QPainter-Tiles` y `05-Modelo-Vista`.

## R06-N05 · Jefe final: la Gárgola de los Vitrales

```meta
tipo: jefe
padre: R06-N04
precio: 10
criatura: dragon
ejecutable: no
insignia: Maestro Vidriero
insignia_descripcion: Venciste a la Gárgola de los Vitrales: armaste TallerExpress, con clases, herencia, un archivo y su ventana en Qt.
usa: gui.qt, gui.tablas-arboles, poo.herencia, poo.polimorfismo, poo.operadores, arch.texto
```

### Crónica

En lo alto del Taller de los Vitrales hay una **gárgola** de piedra con un monóculo de vidrios de colores. Custodia el libro del taller de reparaciones: qué máquina entró, cuántas horas trabajó y cuánto cuesta arreglarla. Nunca dejó pasar un programa con una sola fila mal sumada.

—Pregunta número uno —dice la Gárgola, con voz de examinadora. Es el examen de verdad, **TallerExpress**: unas clases con herencia, un archivo y una ventana en Qt. —Primero los planos —le susurra Lima—. Después el vitral.

Bron no saca la llave. Saca una hoja y dibuja el plano: la base, las tres derivadas, el taller, el archivo, la ventana. Cuando la Gárgola cierra el libro, satisfecha, Bron dibuja en la misma hoja el plano de su propia llave: una que se ajusta a **cualquier** tuerca de la Ciudadela. Tesla lo construye en el torno, y se la da: **la Llave Universal**. Detrás de la Gárgola, el último vitral muestra un balcón con cuatro portales: una espiral, **un engranaje**, un vitral y un arco de fuego. El engranaje es el que Bron tiene en el bolsillo.

### Objetivos

Resolver un examen completo de programación orientada a objetos con Qt: una jerarquía de clases con métodos virtuales y un `operator<<` amigo, un contenedor con altas, bajas, orden y totales, guardado y carga en un archivo de texto, y una ventana que lo usa todo.

### Antes de empezar

Todo el camino, en especial herencia, polimorfismo y operadores (rama 2), archivos (rama 3) y los nodos anteriores de esta rama.

### Explicación

#### El examen: TallerExpress
El taller de reparaciones de la Ciudadela registra **máquinas**. Todas tienen un **código** (único), un **nombre** y sus **horas de uso**, y hay tres clases:

| Clase | Dato propio | Costo de mantenimiento |
|---|---|---|
| `Automata` | batería (0 a 100) | `horas * 10 + (100 - bateria) * 2` |
| `Telar` | hilos | `horas * 5 + hilos` |
| `Grua` | toneladas | `horas * 8 + toneladas * 50` |

Se pide:
1. La jerarquía, con `Maquina` **abstracta** (`costo()` virtual pura) y un `operator<<` **amigo** que muestre cualquier máquina.
2. Una clase `Taller` que guarde las máquinas, sin códigos repetidos: alta, baja por código, listado de mayor a menor costo (a igual costo, por código), costo total, guardar y cargar en un archivo de texto.
3. Una ventana en Qt con el formulario, la tabla y los botones.

#### Cómo se encara (y cómo se corrige)
- **Primero el modelo, en consola** (misión 1): si las clases y el archivo andan, la mitad del examen está aprobada aunque la ventana no llegue a estar.
- **Después la ventana** (misión 2): la misma clase `Taller`, sin cambiarle una línea; la ventana solo la usa.
- **Cuidá el tiempo**: un examen así se piensa para unas tres horas. Dejá para el final lo lindo (colores, íconos) y asegurá lo que se corrige: que compile, que no pierda datos y que los números den.

#### Las ideas que junta
- **Polimorfismo**: el taller guarda `std::unique_ptr<Maquina>` y cada una calcula su costo a su manera.
- **`friend`**: el `operator<<` no es un método (a la izquierda está el `ostream`), pero puede leer lo privado de `Maquina`. Como llama a `tipo()` y `costo()`, que son virtuales, sirve para las tres clases.
- **Archivo con el tipo primero** y una **fábrica** que crea la clase que corresponde.
- **Orden con desempate**: un `std::sort` con una lambda que compara el costo y, si empatan, el código.
- **Una sola verdad**: la tabla siempre se llena desde el `Taller`.

### ¿Para qué sirve?

Además de aprobar: así es casi cualquier sistema de gestión chico (un taller mecánico, una biblioteca, el stock de un negocio). Las clases con las reglas, un archivo que guarda todo y una ventana para usarlo.

### Errores habituales

**Esqueleto: `operator<<` como método.** Si lo escribís dentro de la clase sin `friend`, C++ lo toma como un método con el objeto a la izquierda (`maquina << cout`) y `cout << maquina` no compila:
```
error: no match for ‘operator<<’ (operand types are ‘std::ostream’ and ‘Maquina’)
```

**Troll: la base sin destructor virtual.** Con `unique_ptr<Maquina>`, el destructor de la derivada no corre.

**Ogro: el código repetido.** Si el alta no revisa, dos máquinas con el mismo código rompen la baja (¿cuál se borra?).

**Ogro: el desempate.** Ordenar solo por costo deja las empatadas en cualquier orden: el corrector espera el orden por código.

**Orco: la fila de la tabla después de ordenar o filtrar.** Si la tabla muestra el modelo ordenado, la fila `f` es la máquina `f` **solo si** se llenó después de ordenar. Con filtro, leé el código de la celda y buscá por código.

### Misión R06-N05-M1 · Los planos de TallerExpress

```meta
entrega: codigo
entorno: local
monedas: 5
xp: 40
```

#### Consigna

El modelo de TallerExpress, en consola. Escribí la jerarquía (`Maquina` abstracta, `Automata`, `Telar` y `Grua`, con el `operator<<` amigo), la fábrica y la clase `Taller`. El programa lee órdenes de la entrada hasta que se terminen:

| Orden | Qué hace | Qué muestra |
|---|---|---|
| `alta tipo codigo nombre horas dato` | agrega una máquina | `Alta: 101`, `Codigo repetido: 101` o `Tipo desconocido: barco` |
| `baja codigo` | la quita | `Baja: 101` o `No existe: 101` |
| `listar` | ordena (costo de mayor a menor; a igual costo, por código) y muestra cada una con `<<` | `[101] automata Cuco - 40 h - $450` por línea y al final `Costo total: $930` |
| `guardar` | escribe `maquinas.txt` (una línea por máquina, el tipo primero, separada por `;`) | `Guardadas: 3` |
| `cargar` | reemplaza todo por lo de `maquinas.txt` | `Cargadas: 3` o `No hay archivo` |
| cualquier otra | nada | `Orden desconocida: volar` |

El nombre es una sola palabra.

#### Criterio de aprobación

- `Maquina` es abstracta, con destructor virtual, y las derivadas redefinen `tipo()`, `extra()` y `costo()`.
- El `operator<<` es amigo y sirve para las tres clases.
- `Taller` no acepta códigos repetidos, y lo que se guarda se vuelve a cargar igual.
- El listado respeta el desempate.
- Sin advertencias con `-Wall -Wextra`.

#### Entrada de ejemplo

```
alta automata 101 Cuco 40 75
alta telar 205 Rueca 30 150
alta grua 310 Brazo 10 2
alta grua 101 Doble 5 1
alta barco 400 Ancla 1 1
listar
guardar
baja 205
baja 999
listar
cargar
listar
```

#### Salida esperada

```
Alta: 101
Alta: 205
Alta: 310
Codigo repetido: 101
Tipo desconocido: barco
[101] automata Cuco - 40 h - $450
[205] telar Rueca - 30 h - $300
[310] grua Brazo - 10 h - $180
Costo total: $930
Guardadas: 3
Baja: 205
No existe: 999
[101] automata Cuco - 40 h - $450
[310] grua Brazo - 10 h - $180
Costo total: $630
Cargadas: 3
[101] automata Cuco - 40 h - $450
[205] telar Rueca - 30 h - $300
[310] grua Brazo - 10 h - $180
Costo total: $930
```

#### Solución de referencia

```cpp
// R06-N05-M1 - Los planos de TallerExpress: la jerarquia de maquinas, el taller y su archivo, en consola.
#include <algorithm>
#include <fstream>
#include <iostream>
#include <memory>
#include <sstream>
#include <string>
#include <vector>

class Maquina {
public:
    Maquina(int codigo, std::string nombre, int horas) : codigo_(codigo), nombre_(std::move(nombre)), horas_(horas) {}
    virtual ~Maquina() = default;
    int codigo() const { return codigo_; }
    const std::string& nombre() const { return nombre_; }
    int horas() const { return horas_; }
    virtual std::string tipo() const = 0;
    virtual int extra() const = 0;
    virtual int costo() const = 0;                       // el mantenimiento: cada maquina a su manera

    // Amiga: no es un metodo, pero puede leer lo privado. Llama a lo virtual, asi sirve para todas.
    friend std::ostream& operator<<(std::ostream& out, const Maquina& m)
    {
        return out << "[" << m.codigo_ << "] " << m.tipo() << " " << m.nombre_ << " - " << m.horas_ << " h - $" << m.costo();
    }

private:
    int codigo_;
    std::string nombre_;
    int horas_;
};

class Automata : public Maquina {
public:
    Automata(int codigo, std::string nombre, int horas, int bateria) : Maquina(codigo, std::move(nombre), horas), bateria_(bateria) {}
    std::string tipo() const override { return "automata"; }
    int extra() const override { return bateria_; }
    int costo() const override { return horas() * 10 + (100 - bateria_) * 2; }

private:
    int bateria_;                                        // de 0 a 100
};

class Telar : public Maquina {
public:
    Telar(int codigo, std::string nombre, int horas, int hilos) : Maquina(codigo, std::move(nombre), horas), hilos_(hilos) {}
    std::string tipo() const override { return "telar"; }
    int extra() const override { return hilos_; }
    int costo() const override { return horas() * 5 + hilos_; }

private:
    int hilos_;
};

class Grua : public Maquina {
public:
    Grua(int codigo, std::string nombre, int horas, int toneladas) : Maquina(codigo, std::move(nombre), horas), toneladas_(toneladas) {}
    std::string tipo() const override { return "grua"; }
    int extra() const override { return toneladas_; }
    int costo() const override { return horas() * 8 + toneladas_ * 50; }

private:
    int toneladas_;
};

std::unique_ptr<Maquina> crear(const std::string& tipo, int codigo, const std::string& nombre, int horas, int extra)
{
    if (tipo == "automata") {
        return std::make_unique<Automata>(codigo, nombre, horas, extra);
    }
    if (tipo == "telar") {
        return std::make_unique<Telar>(codigo, nombre, horas, extra);
    }
    if (tipo == "grua") {
        return std::make_unique<Grua>(codigo, nombre, horas, extra);
    }
    return nullptr;
}

class Taller {
public:
    bool existe(int codigo) const { return buscar(codigo) != maquinas_.end(); }

    bool alta(std::unique_ptr<Maquina> m)
    {
        if (existe(m->codigo())) {
            return false;
        }
        maquinas_.push_back(std::move(m));
        return true;
    }

    bool baja(int codigo)
    {
        auto it = buscar(codigo);
        if (it == maquinas_.end()) {
            return false;
        }
        maquinas_.erase(it);
        return true;
    }

    // De mayor a menor costo; a igual costo, por codigo.
    void ordenar()
    {
        std::sort(maquinas_.begin(), maquinas_.end(), [](const auto& a, const auto& b) {
            if (a->costo() != b->costo()) {
                return a->costo() > b->costo();
            }
            return a->codigo() < b->codigo();
        });
    }

    int total() const
    {
        int t = 0;
        for (const auto& m : maquinas_) {
            t += m->costo();
        }
        return t;
    }

    const std::vector<std::unique_ptr<Maquina>>& todas() const { return maquinas_; }

    int guardar(const std::string& ruta) const
    {
        std::ofstream f(ruta);
        for (const auto& m : maquinas_) {
            f << m->tipo() << ';' << m->codigo() << ';' << m->nombre() << ';' << m->horas() << ';' << m->extra() << '\n';
        }
        return f ? static_cast<int>(maquinas_.size()) : -1;
    }

    int cargar(const std::string& ruta)
    {
        std::ifstream f(ruta);
        if (!f) {
            return -1;
        }
        maquinas_.clear();
        std::string linea;
        while (std::getline(f, linea)) {
            std::istringstream campos(linea);
            std::string tipo, codigo, nombre, horas, extra;
            std::getline(campos, tipo, ';');
            std::getline(campos, codigo, ';');
            std::getline(campos, nombre, ';');
            std::getline(campos, horas, ';');
            std::getline(campos, extra);
            if (auto m = crear(tipo, std::stoi(codigo), nombre, std::stoi(horas), std::stoi(extra))) {
                alta(std::move(m));
            }
        }
        return static_cast<int>(maquinas_.size());
    }

private:
    std::vector<std::unique_ptr<Maquina>>::const_iterator buscar(int codigo) const
    {
        return std::find_if(maquinas_.begin(), maquinas_.end(), [codigo](const auto& m) { return m->codigo() == codigo; });
    }

    std::vector<std::unique_ptr<Maquina>> maquinas_;
};

int main()
{
    Taller taller;
    std::string orden;
    while (std::cin >> orden) {
        if (orden == "alta") {
            std::string tipo, nombre;
            int codigo, horas, extra;
            std::cin >> tipo >> codigo >> nombre >> horas >> extra;
            auto m = crear(tipo, codigo, nombre, horas, extra);
            if (!m) {
                std::cout << "Tipo desconocido: " << tipo << "\n";
            } else if (!taller.alta(std::move(m))) {
                std::cout << "Codigo repetido: " << codigo << "\n";
            } else {
                std::cout << "Alta: " << codigo << "\n";
            }
        } else if (orden == "baja") {
            int codigo;
            std::cin >> codigo;
            std::cout << (taller.baja(codigo) ? "Baja: " : "No existe: ") << codigo << "\n";
        } else if (orden == "listar") {
            taller.ordenar();
            for (const auto& m : taller.todas()) {
                std::cout << *m << "\n";
            }
            std::cout << "Costo total: $" << taller.total() << "\n";
        } else if (orden == "guardar") {
            std::cout << "Guardadas: " << taller.guardar("maquinas.txt") << "\n";
        } else if (orden == "cargar") {
            int n = taller.cargar("maquinas.txt");
            if (n < 0) {
                std::cout << "No hay archivo\n";
            } else {
                std::cout << "Cargadas: " << n << "\n";
            }
        } else {
            std::cout << "Orden desconocida: " << orden << "\n";
        }
    }
    return 0;
}
```

#### Pruebas

##### Taller vacío
```entrada
listar
```
```salida
Costo total: $0
```

##### Guardar, borrar y volver a cargar
```entrada
alta grua 9 Gancho 2 3
guardar
baja 9
listar
cargar
listar
```
```salida
Alta: 9
Guardadas: 1
Baja: 9
Costo total: $0
Cargadas: 1
[9] grua Gancho - 2 h - $166
Costo total: $166
```

##### Baja dos veces
```entrada
alta telar 1 A 0 0
alta automata 2 B 0 100
listar
baja 1
baja 1
listar
```
```salida
Alta: 1
Alta: 2
[1] telar A - 0 h - $0
[2] automata B - 0 h - $0
Costo total: $0
Baja: 1
No existe: 1
[2] automata B - 0 h - $0
Costo total: $0
```

##### Desempate por código y una orden desconocida
```entrada
alta grua 7 Pluma 0 1
alta telar 3 Seda 0 50
listar
volar
```
```salida
Alta: 7
Alta: 3
[3] telar Seda - 0 h - $50
[7] grua Pluma - 0 h - $50
Costo total: $100
Orden desconocida: volar
```

### Misión R06-N05-M2 · El vitral de TallerExpress

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 40
extensiones: zip, cpp, h, txt
```

#### Consigna

La ventana de TallerExpress, con el modelo de la misión 1 **sin cambios**:
- Un formulario: tipo (`QComboBox`), código, nombre, horas y el dato propio. La etiqueta del dato propio cambia con el tipo («Batería (%)», «Hilos» o «Toneladas»), y también su rango.
- Una tabla con código, tipo, nombre, horas y costo, ordenada como el listado.
- Botones **Alta** (avisa si el código está repetido o falta el nombre), **Baja** (pregunta antes), **Guardar...** y **Abrir...** (con `QFileDialog`).
- Abajo, la cantidad de máquinas, el costo total y la más cara.

Separá el proyecto en archivos si querés (`Maquina.h`, `Taller.h`, `VentanaTaller.h`…). Entregá un `.zip` con el código y el `CMakeLists.txt`.

#### Criterio de aprobación

- La ventana usa la clase `Taller` de la misión 1 sin cambiarla.
- La tabla se llena siempre desde el modelo, ya ordenado.
- Alta y baja validan y avisan con `QMessageBox`.
- Lo guardado se abre igual en la ventana y en el programa de consola.

#### Solución de referencia

```cpp
// R06-N05-M2 - El vitral de TallerExpress: la ventana sobre las clases de la mision 1.
#include <QApplication>
#include <QComboBox>
#include <QFileDialog>
#include <QFormLayout>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QLabel>
#include <QLineEdit>
#include <QMessageBox>
#include <QPushButton>
#include <QSpinBox>
#include <QTableWidget>
#include <QVBoxLayout>
#include <QWidget>

#include <algorithm>
#include <fstream>
#include <memory>
#include <sstream>
#include <string>
#include <vector>

// ----- El modelo: el mismo de la mision 1 -----

class Maquina {
public:
    Maquina(int codigo, std::string nombre, int horas) : codigo_(codigo), nombre_(std::move(nombre)), horas_(horas) {}
    virtual ~Maquina() = default;
    int codigo() const { return codigo_; }
    const std::string& nombre() const { return nombre_; }
    int horas() const { return horas_; }
    virtual std::string tipo() const = 0;
    virtual int extra() const = 0;
    virtual int costo() const = 0;                       // el mantenimiento: cada maquina a su manera

    // Amiga: no es un metodo, pero puede leer lo privado. Llama a lo virtual, asi sirve para todas.
    friend std::ostream& operator<<(std::ostream& out, const Maquina& m)
    {
        return out << "[" << m.codigo_ << "] " << m.tipo() << " " << m.nombre_ << " - " << m.horas_ << " h - $" << m.costo();
    }

private:
    int codigo_;
    std::string nombre_;
    int horas_;
};

class Automata : public Maquina {
public:
    Automata(int codigo, std::string nombre, int horas, int bateria) : Maquina(codigo, std::move(nombre), horas), bateria_(bateria) {}
    std::string tipo() const override { return "automata"; }
    int extra() const override { return bateria_; }
    int costo() const override { return horas() * 10 + (100 - bateria_) * 2; }

private:
    int bateria_;                                        // de 0 a 100
};

class Telar : public Maquina {
public:
    Telar(int codigo, std::string nombre, int horas, int hilos) : Maquina(codigo, std::move(nombre), horas), hilos_(hilos) {}
    std::string tipo() const override { return "telar"; }
    int extra() const override { return hilos_; }
    int costo() const override { return horas() * 5 + hilos_; }

private:
    int hilos_;
};

class Grua : public Maquina {
public:
    Grua(int codigo, std::string nombre, int horas, int toneladas) : Maquina(codigo, std::move(nombre), horas), toneladas_(toneladas) {}
    std::string tipo() const override { return "grua"; }
    int extra() const override { return toneladas_; }
    int costo() const override { return horas() * 8 + toneladas_ * 50; }

private:
    int toneladas_;
};

std::unique_ptr<Maquina> crear(const std::string& tipo, int codigo, const std::string& nombre, int horas, int extra)
{
    if (tipo == "automata") {
        return std::make_unique<Automata>(codigo, nombre, horas, extra);
    }
    if (tipo == "telar") {
        return std::make_unique<Telar>(codigo, nombre, horas, extra);
    }
    if (tipo == "grua") {
        return std::make_unique<Grua>(codigo, nombre, horas, extra);
    }
    return nullptr;
}

class Taller {
public:
    bool existe(int codigo) const { return buscar(codigo) != maquinas_.end(); }

    bool alta(std::unique_ptr<Maquina> m)
    {
        if (existe(m->codigo())) {
            return false;
        }
        maquinas_.push_back(std::move(m));
        return true;
    }

    bool baja(int codigo)
    {
        auto it = buscar(codigo);
        if (it == maquinas_.end()) {
            return false;
        }
        maquinas_.erase(it);
        return true;
    }

    // De mayor a menor costo; a igual costo, por codigo.
    void ordenar()
    {
        std::sort(maquinas_.begin(), maquinas_.end(), [](const auto& a, const auto& b) {
            if (a->costo() != b->costo()) {
                return a->costo() > b->costo();
            }
            return a->codigo() < b->codigo();
        });
    }

    int total() const
    {
        int t = 0;
        for (const auto& m : maquinas_) {
            t += m->costo();
        }
        return t;
    }

    const std::vector<std::unique_ptr<Maquina>>& todas() const { return maquinas_; }

    int guardar(const std::string& ruta) const
    {
        std::ofstream f(ruta);
        for (const auto& m : maquinas_) {
            f << m->tipo() << ';' << m->codigo() << ';' << m->nombre() << ';' << m->horas() << ';' << m->extra() << '\n';
        }
        return f ? static_cast<int>(maquinas_.size()) : -1;
    }

    int cargar(const std::string& ruta)
    {
        std::ifstream f(ruta);
        if (!f) {
            return -1;
        }
        maquinas_.clear();
        std::string linea;
        while (std::getline(f, linea)) {
            std::istringstream campos(linea);
            std::string tipo, codigo, nombre, horas, extra;
            std::getline(campos, tipo, ';');
            std::getline(campos, codigo, ';');
            std::getline(campos, nombre, ';');
            std::getline(campos, horas, ';');
            std::getline(campos, extra);
            if (auto m = crear(tipo, std::stoi(codigo), nombre, std::stoi(horas), std::stoi(extra))) {
                alta(std::move(m));
            }
        }
        return static_cast<int>(maquinas_.size());
    }

private:
    std::vector<std::unique_ptr<Maquina>>::const_iterator buscar(int codigo) const
    {
        return std::find_if(maquinas_.begin(), maquinas_.end(), [codigo](const auto& m) { return m->codigo() == codigo; });
    }

    std::vector<std::unique_ptr<Maquina>> maquinas_;
};

// ----- La ventana -----

class VentanaTaller : public QWidget {
public:
    VentanaTaller()
    {
        setWindowTitle("TallerExpress");
        tipo_ = new QComboBox;
        tipo_->addItems({"automata", "telar", "grua"});
        codigo_ = new QSpinBox;
        codigo_->setRange(1, 9999);
        nombre_ = new QLineEdit;
        horas_ = new QSpinBox;
        horas_->setRange(0, 10000);
        extra_ = new QSpinBox;
        extra_->setRange(0, 1000);
        etiqueta_extra_ = new QLabel;
        auto* form = new QFormLayout;
        form->addRow("Tipo", tipo_);
        form->addRow("Código", codigo_);
        form->addRow("Nombre", nombre_);
        form->addRow("Horas de uso", horas_);
        form->addRow(etiqueta_extra_, extra_);

        auto* boton_alta = new QPushButton("Alta");
        auto* boton_baja = new QPushButton("Baja");
        auto* boton_guardar = new QPushButton("Guardar...");
        auto* boton_abrir = new QPushButton("Abrir...");
        auto* botones = new QHBoxLayout;
        for (auto* b : {boton_alta, boton_baja, boton_guardar, boton_abrir}) {
            botones->addWidget(b);
        }
        tabla_ = new QTableWidget(0, 5);
        tabla_->setHorizontalHeaderLabels({"Código", "Tipo", "Nombre", "Horas", "Costo"});
        tabla_->setEditTriggers(QAbstractItemView::NoEditTriggers);
        tabla_->setSelectionBehavior(QAbstractItemView::SelectRows);
        tabla_->horizontalHeader()->setStretchLastSection(true);
        resumen_ = new QLabel;

        auto* columna = new QVBoxLayout(this);
        columna->addLayout(form);
        columna->addLayout(botones);
        columna->addWidget(tabla_);
        columna->addWidget(resumen_);

        connect(tipo_, &QComboBox::currentTextChanged, this, &VentanaTaller::cambiar_tipo);
        connect(boton_alta, &QPushButton::clicked, this, &VentanaTaller::alta);
        connect(boton_baja, &QPushButton::clicked, this, &VentanaTaller::baja);
        connect(boton_guardar, &QPushButton::clicked, this, &VentanaTaller::guardar);
        connect(boton_abrir, &QPushButton::clicked, this, &VentanaTaller::abrir);
        cambiar_tipo(tipo_->currentText());
        refrescar();
    }

private:
    // El ultimo dato depende del tipo: la etiqueta y el rango cambian con el combo.
    void cambiar_tipo(const QString& tipo)
    {
        if (tipo == "automata") {
            etiqueta_extra_->setText("Batería (%)");
            extra_->setRange(0, 100);
        } else if (tipo == "telar") {
            etiqueta_extra_->setText("Hilos");
            extra_->setRange(0, 1000);
        } else {
            etiqueta_extra_->setText("Toneladas");
            extra_->setRange(1, 100);
        }
    }

    void alta()
    {
        QString nombre = nombre_->text().trimmed();
        if (nombre.isEmpty() || nombre.contains(';')) {
            QMessageBox::warning(this, "Nombre inválido", "Escribí el nombre de la máquina (sin punto y coma).");
            return;
        }
        auto m = crear(tipo_->currentText().toStdString(), codigo_->value(), nombre.toStdString(), horas_->value(), extra_->value());
        if (!taller_.alta(std::move(m))) {
            QMessageBox::warning(this, "Código repetido", QString("Ya hay una máquina con el código %1.").arg(codigo_->value()));
            return;
        }
        nombre_->clear();
        refrescar();
    }

    void baja()
    {
        int fila = tabla_->currentRow();
        if (fila < 0) {
            QMessageBox::information(this, "Baja", "Elegí una máquina de la tabla.");
            return;
        }
        int codigo = taller_.todas()[fila]->codigo();
        if (QMessageBox::question(this, "Baja", QString("¿Dar de baja la máquina %1?").arg(codigo)) == QMessageBox::Yes) {
            taller_.baja(codigo);
            refrescar();
        }
    }

    void guardar()
    {
        QString ruta = QFileDialog::getSaveFileName(this, "Guardar", "maquinas.txt", "Texto (*.txt)");
        if (ruta.isEmpty()) {
            return;
        }
        if (taller_.guardar(ruta.toStdString()) < 0) {
            QMessageBox::critical(this, "Error", "No se pudo guardar en " + ruta);
        }
    }

    void abrir()
    {
        QString ruta = QFileDialog::getOpenFileName(this, "Abrir", "", "Texto (*.txt)");
        if (ruta.isEmpty()) {
            return;
        }
        if (taller_.cargar(ruta.toStdString()) < 0) {
            QMessageBox::critical(this, "Error", "No se pudo abrir " + ruta);
        }
        refrescar();
    }

    // Ordena el modelo y vuelve a llenar la tabla: la fila f es siempre la maquina f.
    void refrescar()
    {
        taller_.ordenar();
        const auto& todas = taller_.todas();
        tabla_->setRowCount(static_cast<int>(todas.size()));
        for (int f = 0; f < static_cast<int>(todas.size()); f++) {
            const Maquina& m = *todas[f];
            tabla_->setItem(f, 0, new QTableWidgetItem(QString::number(m.codigo())));
            tabla_->setItem(f, 1, new QTableWidgetItem(QString::fromStdString(m.tipo())));
            tabla_->setItem(f, 2, new QTableWidgetItem(QString::fromStdString(m.nombre())));
            tabla_->setItem(f, 3, new QTableWidgetItem(QString::number(m.horas())));
            tabla_->setItem(f, 4, new QTableWidgetItem(QString("$%1").arg(m.costo())));
        }
        QString cara = todas.empty() ? "ninguna" : QString::fromStdString(todas.front()->nombre());
        resumen_->setText(QString("Máquinas: %1 · Costo total: $%2 · La más cara: %3").arg(todas.size()).arg(taller_.total()).arg(cara));
    }

    Taller taller_;
    QComboBox* tipo_;
    QSpinBox* codigo_;
    QLineEdit* nombre_;
    QSpinBox* horas_;
    QSpinBox* extra_;
    QLabel* etiqueta_extra_;
    QTableWidget* tabla_;
    QLabel* resumen_;
};

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    VentanaTaller ventana;
    ventana.resize(600, 520);
    ventana.show();
    return app.exec();
}
```

### Encargo R06-N05-E1 · El simulacro, con reloj

```meta
entrega: archivo
entorno: local
monedas: 1
xp: 40
extensiones: zip, cpp, h, txt
```

#### Consigna

Un examen nuevo, para hacer **de corrido y con reloj** (unas tres horas: si te pasás, no pasa nada, pero anotá cuánto tardaste). No mires las soluciones de las misiones: es para medirte.

**La biblioteca de planos de la Ciudadela.** Cada plano tiene un código (único), un título, la cantidad de hojas y si está prestado. Hay tres clases:

| Clase | Dato propio | Costo de una copia |
|---|---|---|
| `PlanoTorre` | pisos | `hojas * 10 + pisos * 20` |
| `PlanoPuente` | metros | `hojas * 10 + metros` |
| `PlanoMaquina` | piezas | `hojas * 15 + piezas * 5` |

1. La jerarquía, con `Plano` abstracta.
2. Una clase `Biblioteca`: alta (sin códigos repetidos, y siempre ordenada por título), baja (**no** se puede dar de baja un plano prestado), buscar por código, cuántos están prestados, y guardar y cargar en `planos.txt`.
3. Una ventana en Qt: el formulario y los botones Alta, Baja y Prestar/devolver; un combo para **filtrar** la tabla (todos, cada tipo o solo los prestados); abajo, cuántos planos hay, cuántos están prestados y cuánto cuesta copiar los que se ven. Carga el archivo al abrir y lo guarda al cerrar.

Entregá un `.zip` con el código, el `CMakeLists.txt` y una línea en un `LEEME.txt` con cuánto tardaste.

#### Criterio de aprobación

- Las tres clases calculan bien su copia y la base es abstracta.
- Con el filtro puesto, Baja y Prestar actúan sobre el plano elegido (no sobre otro).
- No se puede dar de baja un plano prestado.
- Lo que se carga al cerrar sigue ahí al volver a abrir.

#### Solución de referencia

```cpp
// R06-N05-E1 - El simulacro, con reloj: la biblioteca de planos de la Ciudadela (Qt + clases + archivo).
#include <QApplication>
#include <QComboBox>
#include <QFormLayout>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QLabel>
#include <QLineEdit>
#include <QMessageBox>
#include <QPushButton>
#include <QSpinBox>
#include <QTableWidget>
#include <QVBoxLayout>
#include <QWidget>

#include <algorithm>
#include <fstream>
#include <memory>
#include <sstream>
#include <string>
#include <vector>

// ----- El modelo -----

class Plano {
public:
    Plano(int codigo, std::string titulo, int hojas, bool prestado)
        : codigo_(codigo), titulo_(std::move(titulo)), hojas_(hojas), prestado_(prestado) {}
    virtual ~Plano() = default;
    int codigo() const { return codigo_; }
    const std::string& titulo() const { return titulo_; }
    int hojas() const { return hojas_; }
    bool prestado() const { return prestado_; }
    void prestar(bool si) { prestado_ = si; }
    virtual std::string tipo() const = 0;
    virtual int extra() const = 0;
    virtual int copia() const = 0;                       // lo que cuesta sacarle una copia

private:
    int codigo_;
    std::string titulo_;
    int hojas_;
    bool prestado_;
};

class PlanoTorre : public Plano {
public:
    PlanoTorre(int codigo, std::string titulo, int hojas, bool prestado, int pisos)
        : Plano(codigo, std::move(titulo), hojas, prestado), pisos_(pisos) {}
    std::string tipo() const override { return "torre"; }
    int extra() const override { return pisos_; }
    int copia() const override { return hojas() * 10 + pisos_ * 20; }

private:
    int pisos_;
};

class PlanoPuente : public Plano {
public:
    PlanoPuente(int codigo, std::string titulo, int hojas, bool prestado, int metros)
        : Plano(codigo, std::move(titulo), hojas, prestado), metros_(metros) {}
    std::string tipo() const override { return "puente"; }
    int extra() const override { return metros_; }
    int copia() const override { return hojas() * 10 + metros_; }

private:
    int metros_;
};

class PlanoMaquina : public Plano {
public:
    PlanoMaquina(int codigo, std::string titulo, int hojas, bool prestado, int piezas)
        : Plano(codigo, std::move(titulo), hojas, prestado), piezas_(piezas) {}
    std::string tipo() const override { return "maquina"; }
    int extra() const override { return piezas_; }
    int copia() const override { return hojas() * 15 + piezas_ * 5; }

private:
    int piezas_;
};

std::unique_ptr<Plano> crear(const std::string& tipo, int codigo, const std::string& titulo, int hojas, bool prestado, int extra)
{
    if (tipo == "torre") {
        return std::make_unique<PlanoTorre>(codigo, titulo, hojas, prestado, extra);
    }
    if (tipo == "puente") {
        return std::make_unique<PlanoPuente>(codigo, titulo, hojas, prestado, extra);
    }
    if (tipo == "maquina") {
        return std::make_unique<PlanoMaquina>(codigo, titulo, hojas, prestado, extra);
    }
    return nullptr;
}

class Biblioteca {
public:
    explicit Biblioteca(std::string ruta) : ruta_(std::move(ruta)) {}

    bool alta(std::unique_ptr<Plano> p)
    {
        if (buscar(p->codigo())) {
            return false;
        }
        planos_.push_back(std::move(p));
        std::sort(planos_.begin(), planos_.end(), [](const auto& a, const auto& b) { return a->titulo() < b->titulo(); });
        return true;
    }

    void baja(int codigo)
    {
        std::erase_if(planos_, [codigo](const auto& p) { return p->codigo() == codigo; });
    }

    Plano* buscar(int codigo) const
    {
        for (const auto& p : planos_) {
            if (p->codigo() == codigo) {
                return p.get();
            }
        }
        return nullptr;
    }

    const std::vector<std::unique_ptr<Plano>>& todos() const { return planos_; }

    int prestados() const
    {
        return static_cast<int>(std::count_if(planos_.begin(), planos_.end(), [](const auto& p) { return p->prestado(); }));
    }

    void cargar()
    {
        std::ifstream f(ruta_);
        std::string linea;
        while (std::getline(f, linea)) {
            std::istringstream campos(linea);
            std::string tipo, codigo, titulo, hojas, prestado, extra;
            std::getline(campos, tipo, ';');
            std::getline(campos, codigo, ';');
            std::getline(campos, titulo, ';');
            std::getline(campos, hojas, ';');
            std::getline(campos, prestado, ';');
            std::getline(campos, extra);
            if (auto p = crear(tipo, std::stoi(codigo), titulo, std::stoi(hojas), prestado == "1", std::stoi(extra))) {
                alta(std::move(p));
            }
        }
    }

    bool guardar() const
    {
        std::ofstream f(ruta_);
        for (const auto& p : planos_) {
            f << p->tipo() << ';' << p->codigo() << ';' << p->titulo() << ';' << p->hojas() << ';' << (p->prestado() ? 1 : 0)
              << ';' << p->extra() << '\n';
        }
        return static_cast<bool>(f);
    }

private:
    std::string ruta_;
    std::vector<std::unique_ptr<Plano>> planos_;
};

// ----- La ventana -----

class VentanaBiblioteca : public QWidget {
public:
    VentanaBiblioteca() : biblioteca_("planos.txt")
    {
        setWindowTitle("Biblioteca de planos");
        tipo_ = new QComboBox;
        tipo_->addItems({"torre", "puente", "maquina"});
        codigo_ = new QSpinBox;
        codigo_->setRange(1, 9999);
        titulo_ = new QLineEdit;
        hojas_ = new QSpinBox;
        hojas_->setRange(1, 500);
        extra_ = new QSpinBox;
        extra_->setRange(0, 5000);
        auto* form = new QFormLayout;
        form->addRow("Tipo", tipo_);
        form->addRow("Código", codigo_);
        form->addRow("Título", titulo_);
        form->addRow("Hojas", hojas_);
        form->addRow("Pisos, metros o piezas", extra_);

        auto* boton_alta = new QPushButton("Alta");
        auto* boton_baja = new QPushButton("Baja");
        auto* boton_prestar = new QPushButton("Prestar / devolver");
        auto* botones = new QHBoxLayout;
        for (auto* b : {boton_alta, boton_baja, boton_prestar}) {
            botones->addWidget(b);
        }
        filtro_ = new QComboBox;
        filtro_->addItems({"todos", "torre", "puente", "maquina", "prestados"});
        tabla_ = new QTableWidget(0, 5);
        tabla_->setHorizontalHeaderLabels({"Código", "Tipo", "Título", "Copia", "Estado"});
        tabla_->setEditTriggers(QAbstractItemView::NoEditTriggers);
        tabla_->setSelectionBehavior(QAbstractItemView::SelectRows);
        tabla_->horizontalHeader()->setStretchLastSection(true);
        resumen_ = new QLabel;

        auto* columna = new QVBoxLayout(this);
        columna->addLayout(form);
        columna->addLayout(botones);
        columna->addWidget(filtro_);
        columna->addWidget(tabla_);
        columna->addWidget(resumen_);

        connect(boton_alta, &QPushButton::clicked, this, &VentanaBiblioteca::alta);
        connect(boton_baja, &QPushButton::clicked, this, &VentanaBiblioteca::baja);
        connect(boton_prestar, &QPushButton::clicked, this, &VentanaBiblioteca::prestar);
        connect(filtro_, &QComboBox::currentTextChanged, this, &VentanaBiblioteca::refrescar);
        biblioteca_.cargar();
        refrescar();
    }

    ~VentanaBiblioteca() override { biblioteca_.guardar(); }

private:
    // El codigo del plano de la fila elegida (0 si no hay): con filtro, la fila ya no es el indice del vector.
    int elegido() const
    {
        int fila = tabla_->currentRow();
        return fila < 0 ? 0 : tabla_->item(fila, 0)->text().toInt();
    }

    void alta()
    {
        QString titulo = titulo_->text().trimmed();
        if (titulo.isEmpty() || titulo.contains(';')) {
            QMessageBox::warning(this, "Título inválido", "Escribí el título (sin punto y coma).");
            return;
        }
        auto p = crear(tipo_->currentText().toStdString(), codigo_->value(), titulo.toStdString(), hojas_->value(), false, extra_->value());
        if (!biblioteca_.alta(std::move(p))) {
            QMessageBox::warning(this, "Código repetido", QString("Ya hay un plano con el código %1.").arg(codigo_->value()));
            return;
        }
        titulo_->clear();
        refrescar();
    }

    void baja()
    {
        int codigo = elegido();
        Plano* p = biblioteca_.buscar(codigo);
        if (!p) {
            return;
        }
        if (p->prestado()) {
            QMessageBox::warning(this, "Baja", "No se puede dar de baja un plano prestado.");
            return;
        }
        biblioteca_.baja(codigo);
        refrescar();
    }

    void prestar()
    {
        if (Plano* p = biblioteca_.buscar(elegido())) {
            p->prestar(!p->prestado());
            refrescar();
        }
    }

    void refrescar()
    {
        QString filtro = filtro_->currentText();
        tabla_->setRowCount(0);
        int copias = 0;
        for (const auto& p : biblioteca_.todos()) {
            bool entra = filtro == "todos" || (filtro == "prestados" ? p->prestado() : QString::fromStdString(p->tipo()) == filtro);
            if (!entra) {
                continue;
            }
            int f = tabla_->rowCount();
            tabla_->insertRow(f);
            tabla_->setItem(f, 0, new QTableWidgetItem(QString::number(p->codigo())));
            tabla_->setItem(f, 1, new QTableWidgetItem(QString::fromStdString(p->tipo())));
            tabla_->setItem(f, 2, new QTableWidgetItem(QString::fromStdString(p->titulo())));
            tabla_->setItem(f, 3, new QTableWidgetItem(QString("$%1").arg(p->copia())));
            tabla_->setItem(f, 4, new QTableWidgetItem(p->prestado() ? "prestado" : "en el estante"));
            copias += p->copia();
        }
        resumen_->setText(QString("Planos: %1 · Prestados: %2 · Copiar los que se ven: $%3")
                              .arg(biblioteca_.todos().size()).arg(biblioteca_.prestados()).arg(copias));
    }

    Biblioteca biblioteca_;
    QComboBox* tipo_;
    QSpinBox* codigo_;
    QLineEdit* titulo_;
    QSpinBox* hojas_;
    QSpinBox* extra_;
    QComboBox* filtro_;
    QTableWidget* tabla_;
    QLabel* resumen_;
};

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    VentanaBiblioteca ventana;
    ventana.resize(620, 560);
    ventana.show();
    return app.exec();
}
```

### Prueba del sello

#### ¿Por qué `operator<<` se escribe como función amiga y no como método?

Porque a la izquierda va el `ostream` (`cout << m`): un método tendría el objeto a la izquierda. `friend` le permite leer lo privado igual.

#### ¿Qué pasa si `Maquina` no tiene destructor virtual?

Al destruir una máquina desde un `unique_ptr<Maquina>`, no corre el destructor de la derivada (comportamiento indefinido).

#### ¿Por qué conviene resolver primero el modelo en consola?

Porque se prueba solo, sin ventanas, y es la parte que más se corrige: si anda, la ventana es solo mostrarlo.

#### Con la tabla filtrada, ¿por qué no sirve la fila elegida como índice del vector?

Porque la fila 0 de la tabla puede ser el plano 5 del vector. Se lee el código de la celda y se busca por código.

### Soluciones (docente)

Jefe final del camino (2026-10-08): el simulacro del examen de la UTN, que pide «un programa con Qt y clases» sin bases de datos. M1 se corrige con las pruebas (el modelo en consola); M2 y E1, compilando con CMake + AUTOMOC contra Qt 6 y probándolos. El editor de niveles y el lanzador con `QProcess` (el jefe viejo de la Senda) quedaron fuera del camino; están en `12-Qt-GUI/06-Launcher-QProcess` y `07-Editor-Niveles` de FullCursos.

## R06-N06 · La Encrucijada de los Engranajes

```meta
tipo: ventana
padre: R06-N05
precio: 10
```

### Crónica

En la plaza de la Ciudadela hay un engranaje gigante tallado en el piso, y de sus dientes salen caminos. {mentor} espera a Bron sentado en el borde, con el compás de bronce entre las manos. Lima, Lyn y Oto están ahí; la Maestra Artífice también, de brazos cruzados.

Un aprendiz nuevo, recién llegado, con una llave en la mano, mira el plano que le dieron y le pregunta a Bron: —¿Y esto para qué me sirve? —Bron contesta sin pensar, y le explica, y se da cuenta en la mitad de que está hablando como Tesla. Lima se tapa la boca para no reírse.

—Ya hablás la lengua de la Ciudadela, Bron —dice {mentor}—. Lo que sigue no es obligatorio: es **tuyo**. Por ese camino se llega a la **Linterna Mágica**, donde los planos se mueven en una pantalla. Pero antes, mirá hacia atrás. ¿Qué te llevás de este viaje?

### Objetivos

- Repasar todo el camino principal y reconocer lo que aprendiste.
- Conocer la Senda optativa que sale de acá.

### Explicación

#### Lo que ya sabés hacer

- **Los Cimientos**: compilar, tipos, entrada y salida, decisiones, bucles, funciones, referencias, vectores y azar.
- **Los Planos**: clases, constructores, encapsulamiento, operadores, composición, herencia, polimorfismo y proyectos de varios archivos con CMake.
- **Los Talleres Modernos**: `auto`, textos, mapas y conjuntos, `enum class`, `optional`, lambdas, archivos, punteros inteligentes y RAII.
- **La Gran Biblioteca**: plantillas, iteradores, todos los contenedores, algoritmos, `std::function`, vistas y ranges, y contenedores propios.
- **El Taller del Juego**: excepciones, depuración, pruebas, y un juego completo por turnos.
- **Los Vitrales**: aplicaciones de escritorio con Qt: ventanas, señales y slots, formularios, tus clases detrás de una tabla, dibujo y modelo-vista, y TallerExpress, el simulacro del examen.

Con eso ya podés escribir programas completos en C++ y leer código de otros. Lo que sigue son **especializaciones**.

#### La Senda

Una Senda es un camino optativo: no hace falta para completar el curso, y su entrada se paga con **comodines** (los que ganaste con los encargos del Gremio). Adentro, los nodos se pagan con engranajes, como siempre.

- **Senda de la Linterna Mágica**: videojuegos 2D con **SDL3**. Ventanas, el bucle de juego en tiempo real, teclado, sprites, animación, colisiones y cámara, hasta un juego completo. Se resuelve en tu compu.

### Misión R06-N06-M1 · Mirá hacia atrás

```meta
entrega: ninguna
entorno: navegador
monedas: 0
xp: 20
```

#### Consigna

Antes de seguir, tomate cinco minutos:

1. ¿Cuál fue el tema que más te costó? ¿Qué te ayudó a entenderlo?
2. ¿Qué programa de todo el camino te dio más orgullo?
3. ¿Qué te gustaría construir ahora con C++?

Charlalo con el profe en la próxima clase (o escribíselo). Cuando lo tengas, marcá la misión como completada.

#### Criterio de aprobación

- Respondió las tres preguntas (en clase o por escrito).

### Soluciones (docente)

Nodo Ventana: cierra el camino principal (completarlo completa el curso) y de acá brota la Senda S01 (SDL3). Qt pasó al camino obligatorio (R06) el 2026-10-08. La misión es de reflexión, sin entrega.
