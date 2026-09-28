# RAMA S02 · Senda de los Vitrales: aplicaciones de escritorio con Qt

```meta
tipo: senda
posicion: 7
```

## S02-N01 · Los Vitrales: ventanas, señales y slots

```meta
tipo: tema
padre: R05-N07
precio: 3
moneda: comodin
criatura: slime
ejecutable: no
```

### Crónica

Por el otro camino de la Encrucijada se llega al **Taller de los Vitrales**. Acá no se hacen juegos: se hacen **ventanas** para que cualquiera, aunque no sepa programar, use tus máquinas. Cada vitral tiene palancas, perillas y carteles.

—En la Linterna, vos llevabas el ritmo con tu bucle —dice {mentor}—. Acá es al revés: el vitral **espera**. Cuando alguien toca una palanca, suena una campana, y tu código responde. Se llaman señales y slots.

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
```bash
sudo apt install qt6-base-dev cmake        # Linux (Ubuntu 22.04 o más nuevo)
```
En Windows y macOS, el instalador de qt.io trae Qt y **Qt Creator**, un editor pensado para Qt (abre directamente un `CMakeLists.txt`).

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
```bash
cmake -B build && cmake --build build && ./build/vitrales
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
 * S02-N01 - Ventanas, senales y slots: la caldera del Taller.
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

### Misión S02-N01-M1 · El conversor de temperaturas

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
// S02-N01-M1 - El conversor de temperaturas: dos campos que se actualizan entre si.
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

### Misión S02-N01-M2 · El contador de aforo

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
// S02-N01-M2 - El contador de aforo de la sala.
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

### Encargo S02-N01-E1 · Las propinas del bar

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
// S02-N01-E1 - La calculadora de propinas del bar de la esquina.
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

## S02-N02 · Formularios, menús y archivos

```meta
tipo: tema
padre: S02-N01
precio: 10
criatura: goblin
ejecutable: no
```

### Crónica

El vitral de la oficina de inscripciones tiene de todo: campos para escribir, listas desplegables, casillas, un menú arriba y una barra abajo que avisa qué pasó. Y cuando alguien se olvida un dato, una ventanita le avisa.

—Una aplicación de verdad no confía en nadie —dice {mentor}—. Revisa lo que le escriben, pregunta antes de borrar, y guarda en un archivo para que nada se pierda.

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

### Código de ejemplo

```cpp
/*
 * S02-N02 - Widgets, layouts y dialogos: el registro de artifices en una ventana principal.
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

### Misión S02-N02-M1 · La inscripción al torneo

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
// S02-N02-M1 - La inscripcion al torneo: formulario con validacion y dialogos.
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

### Misión S02-N02-M2 · Las tareas del taller

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
// S02-N02-M2 - La lista de tareas del taller: se guarda sola al cerrar y se carga al abrir.
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

### Encargo S02-N02-E1 · El conversor del almacén

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
// S02-N02-E1 - El conversor de unidades del almacen.
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

## S02-N03 · Dibujar, el mouse y el modelo-vista

```meta
tipo: tema
padre: S02-N02
precio: 10
criatura: orco
ejecutable: no
```

### Crónica

En el fondo del Taller, un maestro vidriero no usa piezas hechas: pinta cada vitral a mano, con pinceles de luz. A su lado, un aprendiz lleva la lista de cada pieza en un cuaderno; cuando el maestro agrega un vidrio, el cuaderno se actualiza solo.

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

### Código de ejemplo

```cpp
/*
 * S02-N03 - Dibujar con QPainter, el mouse, QTimer y el modelo-vista.
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

### Misión S02-N03-M1 · El editor de baldosas

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
// S02-N03-M1 - El editor de baldosas: pintar una grilla arrastrando el mouse.
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

### Misión S02-N03-M2 · El reloj de la torre

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
// S02-N03-M2 - El reloj de la torre: QPainter con translate/rotate y un QTimer.
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

### Encargo S02-N03-E1 · La planilla de gastos

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
// S02-N03-E1 - La planilla de gastos del hogar: modelo-vista con una tabla editable.
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

## S02-N04 · Jefe de los Vitrales: la Gárgola del Editor

```meta
tipo: jefe
padre: S02-N03
precio: 10
criatura: dragon
ejecutable: no
insignia: Maestro Vidriero
insignia_descripcion: Venciste a la Gárgola de los Vitrales: construiste aplicaciones de escritorio completas con Qt.
```

### Crónica

En lo alto del Taller hay una gárgola de piedra que custodia los planos de los laberintos. Nadie puede dibujar uno nuevo sin su permiso, y la gárgola solo acepta planos **correctos**: con un inicio, con una salida, sin agujeros en las paredes.

—Hasta ahora los niveles del Laberinto se escribían a mano, letra por letra —dice {mentor}—. Construí una herramienta para dibujarlos, que los revise antes de guardarlos. Si la gárgola aprueba tus planos, el Taller es tuyo.

### Objetivos

Construir una aplicación de escritorio completa en varios archivos: un widget propio con señales, una ventana principal con menús, paleta y barra de estado, abrir, guardar y validar archivos, y no perder cambios al cerrar.

### Antes de empezar

Toda la Senda y el jefe final del camino principal (el formato de los niveles).

### Explicación

#### El proyecto: un editor de niveles para el Laberinto
| Archivo | Qué tiene |
|---|---|
| `EditorMapa.h` / `.cpp` | un widget propio (`Q_OBJECT`): dibuja las baldosas, se pinta con el mouse, valida el nivel y emite las señales `modificado()` y `cursor_en(columna, fila)` |
| `VentanaPrincipal.h` / `.cpp` | la `QMainWindow`: menús Archivo y Nivel, la paleta de piezas, la barra de estado, abrir, guardar, validar y la protección de cambios |
| `main.cpp` | crea la ventana y corre la aplicación |

El formato es **el mismo** que usa el Laberinto del Minotauro (`#`, `.`, `+`, `k`, `!`, `S`, `>`, `r`, `g`, `M`): los niveles que dibujes se pueden jugar.

#### Las ideas que junta
- **Señales propias**: el editor no conoce a la ventana; solo avisa que algo cambió. La ventana escucha y actualiza el título (con un `*` si hay cambios sin guardar) y la barra de estado.
- **`QActionGroup`**: las acciones de la paleta son `checkable` y el grupo garantiza que haya una sola elegida.
- **Proteger los cambios**: antes de "Nuevo", "Abrir" o cerrar, si hay cambios sin guardar, se pregunta Guardar / Descartar / Cancelar. Una sola función (`descartar_cambios`) lo resuelve para los tres casos.
- **Validar**: `problemas()` devuelve la lista de lo que impide jugar el nivel (vacía: todo bien). Es la misma validación que hace el `Mapa` del Laberinto, pero en vez de lanzar, informa.

### ¿Para qué sirve?

Los editores de niveles, de mapas y de diálogos son las herramientas más comunes en un estudio de videojuegos: los programadores los construyen para que los diseñadores trabajen sin tocar código. La misma estructura (documento, pinceles, abrir/guardar, cambios sin guardar) tienen los editores de texto, de imágenes y de planos.

### Errores habituales

**Esqueleto: el header con `Q_OBJECT` fuera de CMake.** Con `CMAKE_AUTOMOC`, moc encuentra los `.h` si están junto a los `.cpp` o listados en `add_executable`; si no, `undefined reference to vtable`.

**Ogro: perder cambios.** Cerrar, abrir o crear un nivel sin preguntar borra el trabajo del usuario.

**Ogro: guardar un nivel que no se puede jugar.** Validá (o al menos avisá) antes de guardar.

**Orco: pintar fuera de la grilla.** El mouse puede estar fuera del mapa: revisá los límites antes de tocar `filas_[f][c]`.

### Misión S02-N04-M1 · El editor de niveles

```meta
entrega: archivo
entorno: local
monedas: 8
xp: 40
extensiones: zip, cpp, h, txt
```

#### Consigna

Compilá el editor con CMake, dibujá un nivel, validalo y guardalo. Después agregale **tres** cosas:
1. **Deshacer** (`Ctrl+Z`): guardá el estado del mapa antes de cada trazo en una pila (`std::stack` o un `std::vector`) y volvé al anterior.
2. **Contadores** en la barra de estado: cuántos enemigos, pociones y llaves tiene el nivel.
3. **Validar al guardar**: si el nivel tiene problemas, preguntar si se guarda igual.

Entregá el proyecto completo en un `.zip`, junto con un nivel tuyo que se pueda jugar en el Laberinto del Minotauro.

#### Criterio de aprobación

- El proyecto compila con CMake sin advertencias.
- Deshacer vuelve atrás trazo por trazo.
- La barra de estado muestra los contadores.
- Al guardar un nivel inválido, pregunta.

#### Código inicial

```cpp
#include "VentanaPrincipal.h"

#include <QActionGroup>
#include <QCloseEvent>
#include <QFile>
#include <QFileDialog>
#include <QFileInfo>
#include <QInputDialog>
#include <QLabel>
#include <QMenuBar>
#include <QMessageBox>
#include <QScrollArea>
#include <QStatusBar>
#include <QTextStream>
#include <QToolBar>

#include <utility>
#include <vector>

#include "EditorMapa.h"

VentanaPrincipal::VentanaPrincipal()
{
    editor_ = new EditorMapa;
    auto* scroll = new QScrollArea;
    scroll->setWidget(editor_);
    setCentralWidget(scroll);
    info_ = new QLabel;
    statusBar()->addPermanentWidget(info_);
    crear_menus();
    crear_paleta();
    connect(editor_, &EditorMapa::modificado, this, [this] {
        modificado_ = true;
        actualizar_titulo();
    });
    connect(editor_, &EditorMapa::cursor_en, this, [this](int c, int f) { info_->setText(QString("columna %1, fila %2").arg(c).arg(f)); });
    modificado_ = false;
    actualizar_titulo();
}

void VentanaPrincipal::crear_menus()
{
    QMenu* archivo = menuBar()->addMenu("&Archivo");
    QAction* a = archivo->addAction("&Nuevo...");
    a->setShortcut(QKeySequence::New);
    connect(a, &QAction::triggered, this, &VentanaPrincipal::nuevo);
    a = archivo->addAction("&Abrir...");
    a->setShortcut(QKeySequence::Open);
    connect(a, &QAction::triggered, this, &VentanaPrincipal::abrir);
    a = archivo->addAction("&Guardar");
    a->setShortcut(QKeySequence::Save);
    connect(a, &QAction::triggered, this, &VentanaPrincipal::guardar);
    a = archivo->addAction("Guardar &como...");
    connect(a, &QAction::triggered, this, &VentanaPrincipal::guardar_como);
    archivo->addSeparator();
    a = archivo->addAction("&Salir");
    connect(a, &QAction::triggered, this, &QWidget::close);
    QMenu* nivel = menuBar()->addMenu("&Nivel");
    a = nivel->addAction("&Validar");
    a->setShortcut(Qt::Key_F5);
    connect(a, &QAction::triggered, this, &VentanaPrincipal::validar);
}

void VentanaPrincipal::crear_paleta()
{
    const std::vector<std::pair<QChar, QString>> PIEZAS = {{'#', "Pared"}, {'.', "Piso"}, {'+', "Puerta"}, {'k', "Llave"}, {'!', "Poción"},
                                                           {'S', "Inicio"}, {'>', "Salida"}, {'r', "Rata"}, {'g', "Goblin"}, {'M', "Minotauro"}};
    QToolBar* paleta = addToolBar("Paleta");
    auto* grupo = new QActionGroup(this);                  // solo un pincel elegido a la vez
    for (const auto& [letra, nombre] : PIEZAS) {
        QAction* a = paleta->addAction(QString("%1 %2").arg(letra).arg(nombre));
        a->setCheckable(true);
        a->setChecked(letra == '#');
        grupo->addAction(a);
        connect(a, &QAction::triggered, this, [this, letra] { editor_->set_pincel(letra); });
    }
}

void VentanaPrincipal::nuevo()
{
    if (!descartar_cambios()) {
        return;
    }
    bool ok = false;
    int columnas = QInputDialog::getInt(this, "Nuevo nivel", "Columnas:", 15, 5, 60, 1, &ok);
    if (!ok) {
        return;
    }
    int filas = QInputDialog::getInt(this, "Nuevo nivel", "Filas:", 7, 5, 40, 1, &ok);
    if (!ok) {
        return;
    }
    editor_->nuevo(columnas, filas);
    ruta_.clear();
    modificado_ = false;
    actualizar_titulo();
}

void VentanaPrincipal::abrir()
{
    if (!descartar_cambios()) {
        return;
    }
    QString ruta = QFileDialog::getOpenFileName(this, "Abrir nivel", "", "Niveles (*.txt)");
    if (ruta.isEmpty()) {
        return;
    }
    QFile f(ruta);
    if (!f.open(QIODevice::ReadOnly | QIODevice::Text)) {
        QMessageBox::critical(this, "Error", "No se pudo abrir " + ruta);
        return;
    }
    QStringList filas;
    QTextStream in(&f);
    while (!in.atEnd()) {
        QString linea = in.readLine();
        if (!linea.isEmpty()) {
            filas << linea;
        }
    }
    if (!editor_->cargar(filas)) {
        QMessageBox::critical(this, "Nivel inválido", "Las filas del archivo no miden todas lo mismo.");
        return;
    }
    ruta_ = ruta;
    modificado_ = false;
    actualizar_titulo();
}

bool VentanaPrincipal::guardar()
{
    if (ruta_.isEmpty()) {
        return guardar_como();
    }
    QFile f(ruta_);
    if (!f.open(QIODevice::WriteOnly | QIODevice::Text)) {
        QMessageBox::critical(this, "Error", "No se pudo escribir " + ruta_);
        return false;
    }
    QTextStream out(&f);
    for (const auto& fila : editor_->filas()) {
        out << fila << "\n";
    }
    modificado_ = false;
    actualizar_titulo();
    statusBar()->showMessage("Guardado", 2000);
    return true;
}

bool VentanaPrincipal::guardar_como()
{
    QString ruta = QFileDialog::getSaveFileName(this, "Guardar nivel", "nivel.txt", "Niveles (*.txt)");
    if (ruta.isEmpty()) {
        return false;
    }
    ruta_ = ruta;
    return guardar();
}

void VentanaPrincipal::validar()
{
    QStringList p = editor_->problemas();
    if (p.isEmpty()) {
        QMessageBox::information(this, "Validar", "El nivel se puede jugar.");
    } else {
        QMessageBox::warning(this, "Validar", "Problemas:\n- " + p.join("\n- "));
    }
}

bool VentanaPrincipal::descartar_cambios()
{
    if (!modificado_) {
        return true;
    }
    auto r = QMessageBox::question(this, "Cambios sin guardar", "¿Guardar los cambios del nivel?",
                                   QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel);
    if (r == QMessageBox::Save) {
        return guardar();
    }
    return r == QMessageBox::Discard;
}

void VentanaPrincipal::closeEvent(QCloseEvent* e)
{
    if (descartar_cambios()) {
        e->accept();
    } else {
        e->ignore();                        // el usuario cancelo: la ventana sigue abierta
    }
}

void VentanaPrincipal::actualizar_titulo()
{
    QString nombre = ruta_.isEmpty() ? "sin título" : QFileInfo(ruta_).fileName();
    setWindowTitle(QString("Editor de niveles - %1%2").arg(nombre, modificado_ ? " *" : ""));
}
```

#### Solución de referencia

```cpp
// ===== EditorMapa.h =====
#pragma once

#include <QStringList>
#include <QWidget>

// Un widget propio: muestra el mapa como baldosas y se pinta con el mouse.
// Usa el mismo formato de texto que el Laberinto del Minotauro.
class EditorMapa : public QWidget {
    Q_OBJECT

public:
    explicit EditorMapa(QWidget* padre = nullptr);

    void nuevo(int columnas, int filas);                 // borde de paredes, inicio y salida
    bool cargar(const QStringList& filas);               // false si las filas no miden lo mismo
    QStringList filas() const { return filas_; }
    QStringList problemas() const;                       // lo que impide jugar el nivel (vacio: todo bien)
    void set_pincel(QChar c) { pincel_ = c; }

signals:
    void modificado();
    void cursor_en(int columna, int fila);

protected:
    void paintEvent(QPaintEvent*) override;
    void mousePressEvent(QMouseEvent* e) override;
    void mouseMoveEvent(QMouseEvent* e) override;

private:
    void pintar(QPointF punto, bool borrar);
    void ajustar_tamano();

    static constexpr int LADO = 26;
    QStringList filas_;
    QChar pincel_ = '#';
};

// ===== EditorMapa.cpp =====
#include "EditorMapa.h"

#include <QMouseEvent>
#include <QPainter>

#include <map>

EditorMapa::EditorMapa(QWidget* padre) : QWidget(padre)
{
    setMouseTracking(true);                    // recibir movimientos aunque no haya botones apretados
    nuevo(15, 7);
}

void EditorMapa::nuevo(int columnas, int filas)
{
    filas_.clear();
    for (int f = 0; f < filas; f++) {
        bool borde = (f == 0 || f == filas - 1);
        filas_ << (borde ? QString(columnas, '#') : "#" + QString(columnas - 2, '.') + "#");
    }
    filas_[1][1] = 'S';
    filas_[filas - 2][columnas - 2] = '>';
    ajustar_tamano();
    emit modificado();
}

bool EditorMapa::cargar(const QStringList& filas)
{
    if (filas.isEmpty()) {
        return false;
    }
    for (const auto& f : filas) {
        if (f.size() != filas[0].size()) {
            return false;
        }
    }
    filas_ = filas;
    ajustar_tamano();
    return true;
}

QStringList EditorMapa::problemas() const
{
    QStringList p;
    int inicios = 0, salidas = 0;
    for (int f = 0; f < filas_.size(); f++) {
        for (int c = 0; c < filas_[f].size(); c++) {
            QChar ch = filas_[f][c];
            inicios += (ch == 'S');
            salidas += (ch == '>');
            bool borde = f == 0 || c == 0 || f == filas_.size() - 1 || c == filas_[f].size() - 1;
            if (borde && ch != '#' && ch != '>') {
                p << QString("La casilla (%1, %2) del borde no es pared: Kira se escaparía del mapa.").arg(c).arg(f);
            }
        }
    }
    if (inicios != 1) {
        p << QString("Tiene que haber exactamente un inicio (S); hay %1.").arg(inicios);
    }
    if (salidas == 0) {
        p << "Falta la salida (>).";
    }
    return p;
}

void EditorMapa::ajustar_tamano()
{
    setFixedSize(filas_[0].size() * LADO, filas_.size() * LADO);
    update();
}

void EditorMapa::paintEvent(QPaintEvent*)
{
    static const std::map<QChar, QColor> COLOR = {
        {'#', QColor(80, 70, 90)}, {'.', QColor(225, 220, 205)}, {'+', QColor(150, 90, 40)}, {'k', QColor(240, 200, 60)},
        {'!', QColor(220, 60, 90)}, {'>', QColor(60, 170, 90)}, {'S', QColor(60, 130, 220)}, {'r', QColor(150, 150, 150)},
        {'g', QColor(90, 150, 60)}, {'M', QColor(140, 30, 30)}};
    QPainter p(this);
    for (int f = 0; f < filas_.size(); f++) {
        for (int c = 0; c < filas_[f].size(); c++) {
            QChar ch = filas_[f][c];
            auto it = COLOR.find(ch);
            QRect r(c * LADO, f * LADO, LADO - 1, LADO - 1);
            p.fillRect(r, it != COLOR.end() ? it->second : QColor(255, 0, 255));
            if (ch != '#' && ch != '.') {
                p.setPen(Qt::white);
                p.drawText(r, Qt::AlignCenter, QString(ch));       // la letra, para reconocerla
            }
        }
    }
}

void EditorMapa::mousePressEvent(QMouseEvent* e)
{
    pintar(e->position(), e->button() == Qt::RightButton);
}

void EditorMapa::mouseMoveEvent(QMouseEvent* e)
{
    int c = static_cast<int>(e->position().x()) / LADO, f = static_cast<int>(e->position().y()) / LADO;
    emit cursor_en(c, f);
    if (e->buttons() & (Qt::LeftButton | Qt::RightButton)) {
        pintar(e->position(), e->buttons() & Qt::RightButton);
    }
}

void EditorMapa::pintar(QPointF punto, bool borrar)
{
    int c = static_cast<int>(punto.x()) / LADO, f = static_cast<int>(punto.y()) / LADO;
    if (f < 0 || f >= filas_.size() || c < 0 || c >= filas_[f].size()) {
        return;
    }
    QChar nuevo = borrar ? QChar('.') : pincel_;
    if (nuevo == 'S') {                                   // el inicio es unico: se mueve
        for (auto& fila : filas_) {
            fila.replace('S', '.');
        }
    }
    if (filas_[f][c] != nuevo) {
        filas_[f][c] = nuevo;
        update();
        emit modificado();
    }
}

// ===== VentanaPrincipal.h =====
#pragma once

#include <QMainWindow>
#include <QString>

class EditorMapa;
class QLabel;

class VentanaPrincipal : public QMainWindow {
    Q_OBJECT

public:
    VentanaPrincipal();

protected:
    void closeEvent(QCloseEvent* e) override;

private:
    void crear_menus();
    void crear_paleta();
    void nuevo();
    void abrir();
    bool guardar();
    bool guardar_como();
    void validar();
    bool descartar_cambios();              // pregunta si hay cambios sin guardar
    void actualizar_titulo();

    EditorMapa* editor_;
    QLabel* info_;
    QString ruta_;
    bool modificado_ = false;
};

// ===== VentanaPrincipal.cpp =====
#include "VentanaPrincipal.h"

#include <QActionGroup>
#include <QCloseEvent>
#include <QFile>
#include <QFileDialog>
#include <QFileInfo>
#include <QInputDialog>
#include <QLabel>
#include <QMenuBar>
#include <QMessageBox>
#include <QScrollArea>
#include <QStatusBar>
#include <QTextStream>
#include <QToolBar>

#include <utility>
#include <vector>

#include "EditorMapa.h"

VentanaPrincipal::VentanaPrincipal()
{
    editor_ = new EditorMapa;
    auto* scroll = new QScrollArea;
    scroll->setWidget(editor_);
    setCentralWidget(scroll);
    info_ = new QLabel;
    statusBar()->addPermanentWidget(info_);
    crear_menus();
    crear_paleta();
    connect(editor_, &EditorMapa::modificado, this, [this] {
        modificado_ = true;
        actualizar_titulo();
    });
    connect(editor_, &EditorMapa::cursor_en, this, [this](int c, int f) { info_->setText(QString("columna %1, fila %2").arg(c).arg(f)); });
    modificado_ = false;
    actualizar_titulo();
}

void VentanaPrincipal::crear_menus()
{
    QMenu* archivo = menuBar()->addMenu("&Archivo");
    QAction* a = archivo->addAction("&Nuevo...");
    a->setShortcut(QKeySequence::New);
    connect(a, &QAction::triggered, this, &VentanaPrincipal::nuevo);
    a = archivo->addAction("&Abrir...");
    a->setShortcut(QKeySequence::Open);
    connect(a, &QAction::triggered, this, &VentanaPrincipal::abrir);
    a = archivo->addAction("&Guardar");
    a->setShortcut(QKeySequence::Save);
    connect(a, &QAction::triggered, this, &VentanaPrincipal::guardar);
    a = archivo->addAction("Guardar &como...");
    connect(a, &QAction::triggered, this, &VentanaPrincipal::guardar_como);
    archivo->addSeparator();
    a = archivo->addAction("&Salir");
    connect(a, &QAction::triggered, this, &QWidget::close);
    QMenu* nivel = menuBar()->addMenu("&Nivel");
    a = nivel->addAction("&Validar");
    a->setShortcut(Qt::Key_F5);
    connect(a, &QAction::triggered, this, &VentanaPrincipal::validar);
}

void VentanaPrincipal::crear_paleta()
{
    const std::vector<std::pair<QChar, QString>> PIEZAS = {{'#', "Pared"}, {'.', "Piso"}, {'+', "Puerta"}, {'k', "Llave"}, {'!', "Poción"},
                                                           {'S', "Inicio"}, {'>', "Salida"}, {'r', "Rata"}, {'g', "Goblin"}, {'M', "Minotauro"}};
    QToolBar* paleta = addToolBar("Paleta");
    auto* grupo = new QActionGroup(this);                  // solo un pincel elegido a la vez
    for (const auto& [letra, nombre] : PIEZAS) {
        QAction* a = paleta->addAction(QString("%1 %2").arg(letra).arg(nombre));
        a->setCheckable(true);
        a->setChecked(letra == '#');
        grupo->addAction(a);
        connect(a, &QAction::triggered, this, [this, letra] { editor_->set_pincel(letra); });
    }
}

void VentanaPrincipal::nuevo()
{
    if (!descartar_cambios()) {
        return;
    }
    bool ok = false;
    int columnas = QInputDialog::getInt(this, "Nuevo nivel", "Columnas:", 15, 5, 60, 1, &ok);
    if (!ok) {
        return;
    }
    int filas = QInputDialog::getInt(this, "Nuevo nivel", "Filas:", 7, 5, 40, 1, &ok);
    if (!ok) {
        return;
    }
    editor_->nuevo(columnas, filas);
    ruta_.clear();
    modificado_ = false;
    actualizar_titulo();
}

void VentanaPrincipal::abrir()
{
    if (!descartar_cambios()) {
        return;
    }
    QString ruta = QFileDialog::getOpenFileName(this, "Abrir nivel", "", "Niveles (*.txt)");
    if (ruta.isEmpty()) {
        return;
    }
    QFile f(ruta);
    if (!f.open(QIODevice::ReadOnly | QIODevice::Text)) {
        QMessageBox::critical(this, "Error", "No se pudo abrir " + ruta);
        return;
    }
    QStringList filas;
    QTextStream in(&f);
    while (!in.atEnd()) {
        QString linea = in.readLine();
        if (!linea.isEmpty()) {
            filas << linea;
        }
    }
    if (!editor_->cargar(filas)) {
        QMessageBox::critical(this, "Nivel inválido", "Las filas del archivo no miden todas lo mismo.");
        return;
    }
    ruta_ = ruta;
    modificado_ = false;
    actualizar_titulo();
}

bool VentanaPrincipal::guardar()
{
    if (ruta_.isEmpty()) {
        return guardar_como();
    }
    QFile f(ruta_);
    if (!f.open(QIODevice::WriteOnly | QIODevice::Text)) {
        QMessageBox::critical(this, "Error", "No se pudo escribir " + ruta_);
        return false;
    }
    QTextStream out(&f);
    for (const auto& fila : editor_->filas()) {
        out << fila << "\n";
    }
    modificado_ = false;
    actualizar_titulo();
    statusBar()->showMessage("Guardado", 2000);
    return true;
}

bool VentanaPrincipal::guardar_como()
{
    QString ruta = QFileDialog::getSaveFileName(this, "Guardar nivel", "nivel.txt", "Niveles (*.txt)");
    if (ruta.isEmpty()) {
        return false;
    }
    ruta_ = ruta;
    return guardar();
}

void VentanaPrincipal::validar()
{
    QStringList p = editor_->problemas();
    if (p.isEmpty()) {
        QMessageBox::information(this, "Validar", "El nivel se puede jugar.");
    } else {
        QMessageBox::warning(this, "Validar", "Problemas:\n- " + p.join("\n- "));
    }
}

bool VentanaPrincipal::descartar_cambios()
{
    if (!modificado_) {
        return true;
    }
    auto r = QMessageBox::question(this, "Cambios sin guardar", "¿Guardar los cambios del nivel?",
                                   QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel);
    if (r == QMessageBox::Save) {
        return guardar();
    }
    return r == QMessageBox::Discard;
}

void VentanaPrincipal::closeEvent(QCloseEvent* e)
{
    if (descartar_cambios()) {
        e->accept();
    } else {
        e->ignore();                        // el usuario cancelo: la ventana sigue abierta
    }
}

void VentanaPrincipal::actualizar_titulo()
{
    QString nombre = ruta_.isEmpty() ? "sin título" : QFileInfo(ruta_).fileName();
    setWindowTitle(QString("Editor de niveles - %1%2").arg(nombre, modificado_ ? " *" : ""));
}

// ===== main.cpp =====
#include <QApplication>

#include "VentanaPrincipal.h"

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    VentanaPrincipal ventana;
    ventana.resize(760, 420);
    ventana.show();
    return app.exec();
}

// ===== CMakeLists.txt =====
cmake_minimum_required(VERSION 3.16)
project(editor_niveles CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)            # corre moc sobre las clases con Q_OBJECT
find_package(Qt6 REQUIRED COMPONENTS Widgets)
add_executable(editor main.cpp EditorMapa.cpp VentanaPrincipal.cpp EditorMapa.h VentanaPrincipal.h)
target_link_libraries(editor PRIVATE Qt6::Widgets)
target_compile_options(editor PRIVATE -Wall -Wextra)
```

### Misión S02-N04-M2 · El lanzador de la Ciudadela

```meta
entrega: archivo
entorno: local
monedas: 8
xp: 40
extensiones: zip, cpp, h, txt
```

#### Consigna

Hacé un lanzador: elige una carpeta (`QFileDialog::getExistingDirectory`), lista sus `.cpp` y, con un botón, los **compila con `g++`** y, si compiló, los **ejecuta**, mostrando toda la salida (y los errores) en un `QPlainTextEdit`. Usá `QProcess` **sin trabar la ventana**: conectá `readyReadStandardOutput`, `readyReadStandardError` y `finished`, y llevá una máquina de estados (`enum class Etapa { Nada, Compilando, Corriendo }`) para saber qué terminó.

#### Criterio de aprobación

- El proceso corre sin congelar la ventana (sin `waitForFinished`).
- Distingue compilar de correr con un `enum class`.
- Desactiva el botón mientras hay un proceso en marcha.

#### Solución de referencia

```cpp
// S02-N04-M2 - El lanzador de la Ciudadela: compilar y correr programas con QProcess.
#include <QApplication>
#include <QDir>
#include <QFileDialog>
#include <QHBoxLayout>
#include <QLabel>
#include <QListWidget>
#include <QPlainTextEdit>
#include <QProcess>
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>

class Lanzador : public QWidget {
public:
    Lanzador()
    {
        setWindowTitle("Lanzador de la Ciudadela");
        auto* columna = new QVBoxLayout(this);
        auto* arriba = new QHBoxLayout;
        carpeta_ = new QLabel(QDir::currentPath());
        auto* elegir = new QPushButton("Carpeta...");
        arriba->addWidget(carpeta_, 1);
        arriba->addWidget(elegir);
        lista_ = new QListWidget;
        auto* botones = new QHBoxLayout;
        compilar_ = new QPushButton("Compilar y correr");
        botones->addWidget(compilar_);
        salida_ = new QPlainTextEdit;
        salida_->setReadOnly(true);
        columna->addLayout(arriba);
        columna->addWidget(lista_);
        columna->addLayout(botones);
        columna->addWidget(salida_, 1);

        proceso_ = new QProcess(this);
        connect(elegir, &QPushButton::clicked, this, [this] {
            QString d = QFileDialog::getExistingDirectory(this, "Carpeta con programas", carpeta_->text());
            if (!d.isEmpty()) {
                carpeta_->setText(d);
                listar();
            }
        });
        connect(compilar_, &QPushButton::clicked, this, &Lanzador::compilar);
        // El proceso corre sin trabar la ventana: avisa con senales cuando hay salida y cuando termina.
        connect(proceso_, &QProcess::readyReadStandardOutput, this, [this] { salida_->appendPlainText(proceso_->readAllStandardOutput()); });
        connect(proceso_, &QProcess::readyReadStandardError, this, [this] { salida_->appendPlainText(proceso_->readAllStandardError()); });
        connect(proceso_, &QProcess::finished, this, &Lanzador::termino);
        listar();
    }

private:
    void listar()
    {
        lista_->clear();
        lista_->addItems(QDir(carpeta_->text()).entryList({"*.cpp"}, QDir::Files, QDir::Name));
    }

    void compilar()
    {
        if (!lista_->currentItem() || proceso_->state() != QProcess::NotRunning) {
            return;
        }
        etapa_ = Etapa::Compilando;
        compilar_->setEnabled(false);
        salida_->clear();
        salida_->appendPlainText("$ g++ -std=c++20 -Wall -Wextra " + lista_->currentItem()->text());
        proceso_->setWorkingDirectory(carpeta_->text());
        proceso_->start("g++", {"-std=c++20", "-Wall", "-Wextra", "-o", "programa_lanzado", lista_->currentItem()->text()});
    }

    void termino(int codigo, QProcess::ExitStatus)
    {
        if (etapa_ == Etapa::Compilando && codigo == 0) {
            etapa_ = Etapa::Corriendo;
            salida_->appendPlainText("--- compiló bien; ejecutando ---");
            proceso_->start(QDir(carpeta_->text()).filePath("programa_lanzado"), {});
            return;
        }
        salida_->appendPlainText(etapa_ == Etapa::Compilando ? "--- no compiló ---" : QString("--- terminó con código %1 ---").arg(codigo));
        etapa_ = Etapa::Nada;
        compilar_->setEnabled(true);
    }

    enum class Etapa { Nada, Compilando, Corriendo };
    Etapa etapa_ = Etapa::Nada;
    QLabel* carpeta_;
    QListWidget* lista_;
    QPushButton* compilar_;
    QPlainTextEdit* salida_;
    QProcess* proceso_;
};

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    Lanzador l;
    l.resize(560, 520);
    l.show();
    return app.exec();
}
```

### Encargo S02-N04-E1 · La agenda de contactos

```meta
entrega: archivo
entorno: local
monedas: 1
xp: 40
extensiones: zip, cpp, h, txt
```

#### Consigna

Una agenda de contactos (nombre, teléfono, correo) en una tabla editable y ordenable, con un campo de **búsqueda** que filtra por cualquier columna (`QSortFilterProxyModel`), botones para agregar y borrar (¡cuidado con el índice del proxy!) y guardado automático en `contactos.json` al salir (`QJsonDocument`, `QJsonArray`, `QJsonObject`). Si el archivo no existe, arranca con dos contactos de ejemplo.

#### Criterio de aprobación

- La búsqueda usa un proxy y no toca los datos.
- Borrar convierte el índice con `mapToSource`.
- Guarda y carga en JSON.

#### Solución de referencia

```cpp
// S02-N04-E1 - La agenda de contactos: tabla, busqueda con un proxy y guardado en JSON.
#include <QApplication>
#include <QFile>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QLineEdit>
#include <QPushButton>
#include <QSortFilterProxyModel>
#include <QStandardItemModel>
#include <QTableView>
#include <QVBoxLayout>
#include <QWidget>

const QString RUTA = "contactos.json";

void guardar(const QStandardItemModel& m)
{
    QJsonArray lista;
    for (int r = 0; r < m.rowCount(); r++) {
        lista.append(QJsonObject{{"nombre", m.item(r, 0)->text()}, {"telefono", m.item(r, 1)->text()}, {"email", m.item(r, 2)->text()}});
    }
    QFile f(RUTA);
    if (f.open(QIODevice::WriteOnly)) {
        f.write(QJsonDocument(lista).toJson());
    }
}

void cargar(QStandardItemModel& m)
{
    QFile f(RUTA);
    if (!f.open(QIODevice::ReadOnly)) {
        m.appendRow({new QStandardItem("Tesla"), new QStandardItem("3804-000001"), new QStandardItem("tesla@ciudadela.ar")});
        m.appendRow({new QStandardItem("Maese Ferrum"), new QStandardItem("3804-000002"), new QStandardItem("ferrum@forjas.ar")});
        return;
    }
    for (const QJsonValue& v : QJsonDocument::fromJson(f.readAll()).array()) {
        QJsonObject o = v.toObject();
        m.appendRow({new QStandardItem(o["nombre"].toString()), new QStandardItem(o["telefono"].toString()), new QStandardItem(o["email"].toString())});
    }
}

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    QWidget ventana;
    ventana.setWindowTitle("Agenda");
    QStandardItemModel modelo(0, 3);
    modelo.setHorizontalHeaderLabels({"Nombre", "Teléfono", "Correo"});
    cargar(modelo);

    QSortFilterProxyModel filtro;                         // un modelo "intermedio" que filtra y ordena
    filtro.setSourceModel(&modelo);
    filtro.setFilterCaseSensitivity(Qt::CaseInsensitive);
    filtro.setFilterKeyColumn(-1);                        // busca en todas las columnas

    auto* columna = new QVBoxLayout(&ventana);
    auto* buscar = new QLineEdit;
    buscar->setPlaceholderText("Buscar...");
    auto* tabla = new QTableView;
    tabla->setModel(&filtro);                             // la vista mira el filtro, no el modelo
    tabla->setSortingEnabled(true);
    tabla->horizontalHeader()->setStretchLastSection(true);
    auto* botones = new QHBoxLayout;
    auto* nuevo = new QPushButton("Nuevo");
    auto* borrar = new QPushButton("Borrar");
    botones->addWidget(nuevo);
    botones->addWidget(borrar);
    columna->addWidget(buscar);
    columna->addWidget(tabla);
    columna->addLayout(botones);

    QObject::connect(buscar, &QLineEdit::textChanged, &filtro, [&filtro](const QString& t) { filtro.setFilterFixedString(t); });
    QObject::connect(nuevo, &QPushButton::clicked, &ventana, [&] {
        modelo.appendRow({new QStandardItem("Nuevo contacto"), new QStandardItem(""), new QStandardItem("")});
        buscar->clear();
        tabla->edit(filtro.mapFromSource(modelo.index(modelo.rowCount() - 1, 0)));
    });
    QObject::connect(borrar, &QPushButton::clicked, &ventana, [&] {
        QModelIndex i = tabla->currentIndex();
        if (i.isValid()) {
            modelo.removeRow(filtro.mapToSource(i).row());   // el indice de la vista NO es el del modelo
        }
    });
    QObject::connect(&app, &QApplication::aboutToQuit, &ventana, [&modelo] { guardar(modelo); });
    ventana.resize(520, 380);
    ventana.show();
    return app.exec();
}
```

### Prueba del sello

#### ¿Por qué el editor avisa con una señal en vez de llamar a la ventana?

Para no depender de ella: cualquiera puede escuchar la señal, y el editor se puede usar en otra ventana.

#### ¿Para qué sirve el `*` en el título?

Para mostrar que hay cambios sin guardar.

#### ¿Por qué `QProcess` no traba la ventana?

Porque corre en paralelo y avisa con señales cuando hay salida o termina; el bucle de eventos sigue atendiendo.

#### ¿Qué comparte este editor con el Laberinto del Minotauro?

El formato del nivel y las reglas de validación (un inicio, una salida, bordes de pared).

### Soluciones (docente)

Jefe de la Senda, basado en `12-Qt-GUI/06-Launcher-QProcess` y `07-Editor-Niveles`. M1 parte del editor completo (las tres ampliaciones se corrigen probándolo). Todo compilado con CMake + AUTOMOC contra Qt 6.4.
