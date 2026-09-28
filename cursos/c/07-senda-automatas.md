# RAMA S02 · Senda de los Autómatas: Arduino

```meta
tipo: senda
posicion: 7
```

## S02-N01 · Los Autómatas: el primer autómata

```meta
tipo: tema
padre: R05-N05
precio: 3
moneda: comodin
criatura: slime
ejecutable: no
```

### Crónica

Por el otro camino de la Encrucijada se llega al **Taller de los Autómatas**. En las mesas hay figuras de latón con ojos de vidrio que se prenden y se apagan, brazos que se mueven solos y campanas que suenan cuando alguien pasa.

—Hasta ahora tu magia vivía adentro de una pantalla, {heroe} —dice {mentor}—. Acá sale al mundo: prende luces, lee botones, mueve cosas. Y la lengua sigue siendo la misma.

### Objetivos

- Compilar y subir un programa (*sketch*) a una placa Arduino.
- Entender `setup()` y `loop()`, y prender y apagar un pin.
- Hacer varias cosas "a la vez" con `millis()` en lugar de `delay()`.
- Mandar mensajes a la compu por el puerto serie.

### Antes de empezar

Todo el camino principal. El lenguaje de Arduino es **C++**, pero para esta Senda alcanza con lo que ya sabés de C.

### Explicación

#### Las herramientas

Hace falta una placa **Arduino Uno o Nano**, un cable USB y el programa **arduino-cli** (o el IDE de Arduino):

```bash
arduino-cli core install arduino:avr                              # una sola vez
arduino-cli compile --fqbn arduino:avr:uno MiSketch               # compilar (la carpeta y el .ino se llaman igual)
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno MiSketch   # subir a la placa
arduino-cli monitor -p /dev/ttyACM0 -c baudrate=115200            # ver lo que manda por el puerto serie
```

En Linux, para usar el puerto hay que estar en el grupo `dialout` (`sudo usermod -aG dialout $USER` y volver a iniciar sesión). Las misiones con la placa se entregan como `.zip` con la carpeta del sketch.

#### `setup()` y `loop()`

Un sketch no tiene `main`: tiene dos funciones. `setup()` corre **una vez** al encender la placa; `loop()` corre **para siempre** después. Es el bucle de juego, pero en la placa.

```cpp
void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);     // el pin del LED de la placa, como salida
  Serial.begin(115200);             // el puerto serie, a 115200 baudios
}

void loop()
{
  digitalWrite(LED_BUILTIN, HIGH);  // prender (5 voltios)
  delay(500);                       // esperar medio segundo
  digitalWrite(LED_BUILTIN, LOW);   // apagar
  delay(500);
}
```

#### El problema de `delay()`

Mientras hace `delay(500)`, la placa **no hace nada más**: no lee botones ni sensores. La solución es la misma idea del *delta time*: mirar el reloj y actuar cuando pasó el tiempo.

```cpp
if (millis() - ultimoCambio >= 400) {   // millis(): milisegundos desde que se encendió
  ultimoCambio = millis();
  // ...cambiar el LED
}
```

`millis()` devuelve un `unsigned long`. La resta `millis() - ultimoCambio` funciona bien incluso cuando el contador da la vuelta (a los 49 días).

#### El puerto serie

`Serial.print` y `Serial.println` mandan texto por el cable USB. Del otro lado, el monitor serie (o un programa tuyo) lo lee. Las dos puntas tienen que usar la **misma velocidad**: 115200.

### Código de ejemplo

```cpp
/*
 * S02-N01 - El primer automata: parpadear sin detener la placa.
 * delay() congela todo; con millis() la placa puede hacer varias cosas "a la vez".
 */
const int LED = LED_BUILTIN;              // pin 13 en el Uno
const unsigned long MEDIO_PERIODO = 400;  // milisegundos

unsigned long ultimoCambio = 0;
bool encendido = false;
unsigned long parpadeos = 0;

void setup()
{
  pinMode(LED, OUTPUT);
  Serial.begin(115200);                  // la misma velocidad que el monitor serie
  Serial.println("Automata listo");
}

void loop()
{
  unsigned long ahora = millis();         // milisegundos desde que se encendio la placa
  if (ahora - ultimoCambio >= MEDIO_PERIODO) {
    ultimoCambio = ahora;
    encendido = !encendido;
    digitalWrite(LED, encendido ? HIGH : LOW);
    if (encendido) {
      parpadeos++;
      Serial.print("parpadeo #");
      Serial.println(parpadeos);
    }
  }
  // aca la placa esta libre para leer botones, sensores, etc.
}
```

### ¿Para qué sirve?

Arduino y placas parecidas están en impresoras 3D, estaciones meteorológicas caseras, sistemas de riego, alarmas, robots educativos y prototipos de productos que después se fabrican. Las máquinas de estados con `millis()` (como el semáforo del encargo) son la forma en que se programan los controladores de ascensores, lavarropas y semáforos de verdad.

### Errores habituales

**Slime: el sketch mal nombrado.** El archivo `.ino` tiene que llamarse igual que su carpeta: `Blink/Blink.ino`.

**Ogro: el monitor mudo o con basura.** Distinta velocidad en `Serial.begin` y en el monitor: aparecen caracteres raros o nada.

**Troll: el puerto ocupado.** No se puede subir el sketch mientras el monitor serie tiene el puerto abierto (`Device or resource busy`).

**Ogro: `delay` que traba todo.** Con `delay`, un botón apretado durante la espera no se detecta.

**Goblin: `millis()` en un `int`.** Un `int` del Uno tiene 16 bits: a los 32 segundos se desborda. Siempre `unsigned long`.

### Misión S02-N01-M1 · SOS en Morse

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, ino
```

#### Consigna

Hacé que el LED de la placa transmita **SOS** en código Morse, una y otra vez: tres señales cortas, tres largas y tres cortas. Con una unidad de 200 ms: el punto dura 1 unidad y la raya 3; entre señales hay 1 unidad de silencio, entre letras 3 y entre palabras 7. Escribí funciones `senal(unidades)` y `letra(codigo)` (por ejemplo, `letra("...")`). Mandá `... --- ...` por el puerto serie en cada vuelta.

#### Criterio de aprobación

- Respeta los tiempos del Morse con una unidad de 200 ms.
- Usa funciones para la señal y la letra.
- Manda el mensaje por el puerto serie.

#### Solución de referencia

```cpp
/* S02-N01 Mision 1 - SOS en Morse: tres cortos, tres largos, tres cortos, con una pausa. */
const int LED = LED_BUILTIN;
const int PUNTO = 200;                    // la unidad de tiempo del Morse, en ms

void senal(int unidades)
{
  digitalWrite(LED, HIGH);
  delay(PUNTO * unidades);
  digitalWrite(LED, LOW);
  delay(PUNTO);                           // silencio de una unidad entre senales
}

void letra(const char *codigo)
{
  for (int i = 0; codigo[i] != '\0'; i++) {
    senal(codigo[i] == '.' ? 1 : 3);      // punto: 1 unidad; raya: 3
  }
  delay(PUNTO * 2);                       // entre letras: 3 unidades en total
}

void setup()
{
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
}

void loop()
{
  Serial.println("... --- ...");
  letra("...");
  letra("---");
  letra("...");
  delay(PUNTO * 4);                       // entre palabras: 7 unidades en total
}
```

### Misión S02-N01-M2 · Dos ritmos a la vez

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, ino
```

#### Consigna

Conectá dos LEDs (con su resistencia de 220 Ω) a los pines 12 y 11. Hacé que uno cambie cada 250 ms y el otro cada 700 ms, **a la vez**, sin `delay`. Guardá los datos de cada parpadeo en un `struct` (pin, medio período, último cambio, estado) y actualizalos con una misma función.

#### Criterio de aprobación

- No usa `delay`: todo con `millis()`.
- Cada LED tiene su struct y se actualiza con la misma función.
- Los dos ritmos son independientes.

#### Solución de referencia

```cpp
/* S02-N01 Mision 2 - Dos ritmos a la vez: dos LEDs con periodos distintos, sin delay. */
const int LED_A = 12, LED_B = 11;

struct Parpadeo {
  int pin;
  unsigned long medioPeriodo;
  unsigned long ultimo;
  bool encendido;
};

Parpadeo leds[] = { { LED_A, 250, 0, false }, { LED_B, 700, 0, false } };

void actualizar(Parpadeo &p, unsigned long ahora)
{
  if (ahora - p.ultimo >= p.medioPeriodo) {
    p.ultimo = ahora;
    p.encendido = !p.encendido;
    digitalWrite(p.pin, p.encendido ? HIGH : LOW);
  }
}

void setup()
{
  for (auto &p : leds) {
    pinMode(p.pin, OUTPUT);
  }
  Serial.begin(115200);
}

void loop()
{
  unsigned long ahora = millis();
  for (auto &p : leds) {
    actualizar(p, ahora);
  }
}
```

### Encargo S02-N01-E1 · El semáforo del Gremio

```meta
entrega: archivo
entorno: local
monedas: 1
xp: 20
extensiones: zip, ino
```

#### Consigna

Con tres LEDs (rojo en el 10, amarillo en el 9, verde en el 8), programá un semáforo: rojo 5 s, verde 4 s, amarillo 1,5 s, y vuelta a empezar. Usá un `enum` para los estados, un array con la duración de cada uno y `millis()`. Avisá cada cambio por el puerto serie.

#### Criterio de aprobación

- Es una máquina de estados con `enum`.
- Las duraciones están en un array.
- No usa `delay`.

#### Solución de referencia

```cpp
/* S02-N01 Encargo - El semaforo del Gremio: una maquina de estados con millis(). */
const int ROJO = 10, AMARILLO = 9, VERDE = 8;

enum Estado { EN_ROJO, EN_VERDE, EN_AMARILLO };
const unsigned long DURACION[] = { 5000, 4000, 1500 };   // ms de cada estado
const char *NOMBRE[] = { "rojo", "verde", "amarillo" };

Estado estado = EN_ROJO;
unsigned long desde = 0;

void mostrar(Estado e)
{
  digitalWrite(ROJO, e == EN_ROJO ? HIGH : LOW);
  digitalWrite(VERDE, e == EN_VERDE ? HIGH : LOW);
  digitalWrite(AMARILLO, e == EN_AMARILLO ? HIGH : LOW);
  Serial.print("semaforo en ");
  Serial.println(NOMBRE[e]);
}

void setup()
{
  pinMode(ROJO, OUTPUT);
  pinMode(AMARILLO, OUTPUT);
  pinMode(VERDE, OUTPUT);
  Serial.begin(115200);
  mostrar(estado);
}

void loop()
{
  if (millis() - desde >= DURACION[estado]) {
    desde = millis();
    estado = estado == EN_ROJO ? EN_VERDE : estado == EN_VERDE ? EN_AMARILLO : EN_ROJO;
    mostrar(estado);
  }
}
```

### Prueba del sello

#### ¿Qué diferencia hay entre `setup()` y `loop()`?

`setup()` se ejecuta una vez al encender o resetear la placa; `loop()` se repite para siempre después.

#### ¿Por qué conviene `millis()` en lugar de `delay()`?

Porque `delay()` detiene la placa: mientras espera no puede leer botones ni sensores. Con `millis()` se revisa el tiempo sin frenar.

#### ¿Por qué `millis()` se guarda en un `unsigned long`?

Porque crece rápido: en un `int` de 16 bits se desbordaría a los 32 segundos.

#### ¿Qué tiene que coincidir entre la placa y el monitor serie?

La velocidad (los baudios), por ejemplo 115200.

### Soluciones (docente)

Senda basada en `FullCursos/15-Arduino` (01 a 07). Las entregas con placa son archivos; se prueban subiéndolos a un Uno.

## S02-N02 · Botones y perillas

```meta
tipo: tema
padre: S02-N01
precio: 10
criatura: ogro
ejecutable: no
```

### Crónica

Los autómatas del Taller no solo hablan: **escuchan**. Tienen palancas, botones y perillas que la gente toca, y responden a cada gesto.

—Un botón parece la cosa más simple del mundo, {heroe} —dice {mentor}—. Hasta que lo mirás de cerca y ves que rebota como una pelota.

### Objetivos

- Leer botones con `INPUT_PULLUP` y filtrar el **rebote**.
- Leer valores analógicos (una perilla, un sensor) con `analogRead` y convertirlos con `map`.
- Controlar el brillo de un LED con PWM (`analogWrite`).

### Antes de empezar

El primer autómata (S02-N01).

### Explicación

#### Botones con `INPUT_PULLUP`

Un pin sin conectar lee valores al azar. `INPUT_PULLUP` activa una resistencia interna que lo mantiene en `HIGH`; el botón lo conecta a tierra (`GND`) al apretarlo. Por eso la lógica queda **invertida**:

```cpp
pinMode(2, INPUT_PULLUP);                  // pin 2 ---[botón]--- GND, sin resistencia externa
bool apretado = digitalRead(2) == LOW;     // apretado = LOW
```

#### El rebote

Un botón mecánico, al cerrarse, **rebota**: durante uno o dos milisegundos se abre y se cierra varias veces. Si se cuenta cada cambio, una pulsación cuenta como cinco. La solución: aceptar un cambio solo si se mantuvo **estable** un tiempo (20 ms):

```cpp
if (leido != ultimoLeido) {                // cambió: todavía puede ser rebote
  ultimoLeido = leido;
  ultimoCambio = millis();
}
if (millis() - ultimoCambio > 20 && leido != estable) {
  estable = leido;                         // se mantuvo: es un cambio de verdad
}
```

#### Lo analógico

`analogRead(A0)` mide un voltaje entre 0 y 5 V y devuelve un número entre **0 y 1023**. Una perilla (potenciómetro) con los extremos a 5 V y GND y el medio en A0 da todo el rango. `map(valor, 0, 1023, 0, 100)` convierte a otra escala (una regla de tres entera).

#### PWM: medio encendido

Un pin digital solo puede estar prendido o apagado. `analogWrite(pin, 0..255)` lo prende y apaga muy rápido: con 128 está prendido la mitad del tiempo y el LED se ve a media luz. Solo funciona en los pines marcados con `~` (en el Uno: 3, 5, 6, 9, 10 y 11).

### Código de ejemplo

```cpp
/*
 * S02-N02 - Botones y perillas: un boton con INPUT_PULLUP y antirrebote,
 * y una perilla (potenciometro) leida con analogRead.
 *   boton:  pin 2 ---[ boton ]--- GND      (sin resistencia: la pone INPUT_PULLUP)
 *   perilla: extremos a 5V y GND, el medio a A0
 */
const int BOTON = 2, PERILLA = A0;
const unsigned long ANTIRREBOTE_MS = 20;

int estadoEstable = HIGH, ultimoLeido = HIGH;
unsigned long ultimoCambio = 0;
unsigned long ultimoEnvio = 0;

void setup()
{
  pinMode(BOTON, INPUT_PULLUP);           // suelto: HIGH; apretado: LOW (logica invertida)
  Serial.begin(115200);
}

void loop()
{
  int leido = digitalRead(BOTON);
  if (leido != ultimoLeido) {             // cambio: puede ser rebote, se espera
    ultimoLeido = leido;
    ultimoCambio = millis();
  }
  if (millis() - ultimoCambio > ANTIRREBOTE_MS && leido != estadoEstable) {
    estadoEstable = leido;                // estable el tiempo suficiente: es de verdad
    Serial.println(estadoEstable == LOW ? "BOTON apretado" : "BOTON suelto");
  }

  if (millis() - ultimoEnvio >= 250) {    // la perilla, cuatro veces por segundo
    ultimoEnvio = millis();
    int valor = analogRead(PERILLA);      // 0..1023
    int porcentaje = map(valor, 0, 1023, 0, 100);
    Serial.print("PERILLA ");
    Serial.print(valor);
    Serial.print(" (");
    Serial.print(porcentaje);
    Serial.println("%)");
  }
}
```

### ¿Para qué sirve?

El antirrebote está en todo aparato con botones: controles remotos, teclados, ascensores, microondas. La lectura analógica es la base de cualquier sensor (temperatura, luz, humedad del suelo, fuerza) y el PWM controla el brillo de las pantallas, la velocidad de los motores y la posición de los servos en robótica.

### Errores habituales

**Ogro: la lógica al revés.** Con `INPUT_PULLUP`, apretado es `LOW`. Si no se invierte, el programa cree que el botón está apretado todo el tiempo.

**Ogro: contar los rebotes.** Una pulsación cuenta varias veces.

**Ogro: contar mientras se mantiene.** Contar cada vez que se lee `LOW` en lugar del **flanco** (el momento en que pasa de suelto a apretado): mantenerlo apretado suma sin parar.

**Slime: PWM en un pin sin `~`.** `analogWrite` en un pin sin PWM solo prende o apaga.

**Goblin: la lectura que tiembla.** Las lecturas analógicas varían un poco aunque la perilla esté quieta: para avisar cambios hace falta un umbral.

### Misión S02-N02-M1 · El contador de golpes

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, ino
```

#### Consigna

Contá cuántas veces se aprieta un botón (en el pin 2, con `INPUT_PULLUP`), sin contar rebotes ni sumar mientras se mantiene apretado: se cuenta el **flanco** de suelto a apretado. Mostrá el total por el puerto serie en cada golpe. Si se mantiene apretado 2 segundos, el contador vuelve a cero (una sola vez por pulsación).

#### Criterio de aprobación

- Filtra el rebote con `millis()`.
- Cuenta el flanco, no el estado.
- El reinicio por pulsación larga ocurre una sola vez.

#### Solución de referencia

```cpp
/* S02-N02 Mision 1 - El contador de golpes: cuenta pulsaciones sin rebotes; mantenido 2 s, vuelve a cero. */
const int BOTON = 2;
const unsigned long ANTIRREBOTE_MS = 20, REINICIO_MS = 2000;

int estable = HIGH, ultimoLeido = HIGH;
unsigned long ultimoCambio = 0, apretadoDesde = 0;
unsigned int golpes = 0;
bool reiniciado = false;

void setup()
{
  pinMode(BOTON, INPUT_PULLUP);
  Serial.begin(115200);
  Serial.println("golpes: 0");
}

void loop()
{
  int leido = digitalRead(BOTON);
  if (leido != ultimoLeido) {
    ultimoLeido = leido;
    ultimoCambio = millis();
  }
  if (millis() - ultimoCambio > ANTIRREBOTE_MS && leido != estable) {
    estable = leido;
    if (estable == LOW) {                 // flanco de bajada: se apreto
      apretadoDesde = millis();
      reiniciado = false;
      golpes++;
      Serial.print("golpes: ");
      Serial.println(golpes);
    }
  }
  if (estable == LOW && !reiniciado && millis() - apretadoDesde >= REINICIO_MS) {
    golpes = 0;
    reiniciado = true;
    Serial.println("golpes: 0 (reinicio)");
  }
}
```

### Misión S02-N02-M2 · La perilla y el brillo

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, ino
```

#### Consigna

Con una perilla en A0 y un LED (con resistencia) en el pin 9, hacé que el brillo del LED siga a la perilla: leé con `analogRead`, convertí de 0–1023 a 0–255 con `map` y escribí con `analogWrite`. Mandá el brillo por el puerto serie solo cuando cambie en 5 o más.

#### Criterio de aprobación

- Convierte con `map` al rango de `analogWrite`.
- Usa un pin con PWM.
- Solo informa cambios mayores a un umbral.

#### Solución de referencia

```cpp
/* S02-N02 Mision 2 - La perilla y el brillo: analogRead -> map -> analogWrite (PWM), avisando solo los cambios. */
const int PERILLA = A0, LED = 9;          // el 9 tiene PWM en el Uno (marcado con ~)

int ultimoBrillo = -1;

void setup()
{
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
}

void loop()
{
  int valor = analogRead(PERILLA);        // 0..1023
  int brillo = map(valor, 0, 1023, 0, 255);
  analogWrite(LED, brillo);               // 0 apagado .. 255 al maximo
  if (abs(brillo - ultimoBrillo) >= 5) {  // umbral: la lectura analogica tiembla un poco
    ultimoBrillo = brillo;
    Serial.print("brillo ");
    Serial.println(brillo);
  }
  delay(10);
}
```

### Encargo S02-N02-E1 · El termómetro del horno

```meta
entrega: archivo
entorno: local
monedas: 1
xp: 20
extensiones: zip, ino
```

#### Consigna

El herrero quiere saber la temperatura del taller. Con un sensor **LM35** en A0 (entrega 10 mV por grado), leé 10 veces, promediá, convertí la lectura a milivoltios (`lectura × 5000 / 1023`) y a grados, y mostrá la temperatura con un decimal cada segundo. (Sin sensor, se puede probar con la perilla).

#### Criterio de aprobación

- Promedia varias lecturas.
- Convierte bien de lectura a milivoltios y a grados.
- Muestra un valor por segundo con un decimal.

#### Solución de referencia

```cpp
/* S02-N02 Encargo - El termometro del horno: sensor LM35 en A0 (10 mV por grado), promedio de 10 lecturas. */
const int SENSOR = A0;
const int MUESTRAS = 10;

void setup()
{
  Serial.begin(115200);
}

void loop()
{
  long suma = 0;
  for (int i = 0; i < MUESTRAS; i++) {
    suma += analogRead(SENSOR);
    delay(5);
  }
  float lectura = suma / (float) MUESTRAS;
  float milivoltios = lectura * 5000.0 / 1023.0;   // 0..1023 -> 0..5000 mV
  float grados = milivoltios / 10.0;                // LM35: 10 mV por grado
  Serial.print("temperatura: ");
  Serial.print(grados, 1);
  Serial.println(" C");
  delay(1000);
}
```

### Prueba del sello

#### ¿Por qué con `INPUT_PULLUP` el botón apretado se lee `LOW`?

Porque la resistencia interna mantiene el pin en `HIGH` y el botón, al apretarse, lo conecta a tierra.

#### ¿Qué es el rebote de un botón y cómo se filtra?

Los cierres y aperturas rápidas del contacto al apretarlo. Se filtra aceptando un cambio solo si se mantuvo estable unos milisegundos.

#### ¿Qué rango devuelve `analogRead` y qué rango acepta `analogWrite`?

`analogRead` devuelve de 0 a 1023; `analogWrite` acepta de 0 a 255.

#### ¿Qué es contar el flanco en lugar del estado?

Contar el momento en que el botón pasa de suelto a apretado, una sola vez, en lugar de contar cada lectura en que está apretado.

### Soluciones (docente)

Basado en `15-Arduino` (02 Botones-Serie, 03 Joystick-Analógico).

## S02-N03 · Hablar con la compu

```meta
tipo: tema
padre: S02-N02
precio: 10
criatura: goblin
ejecutable: no
```

### Crónica

Los autómatas más viejos del Taller trabajan solos. Los nuevos **conversan**: le cuentan a una máquina más grande todo lo que sienten, y reciben órdenes de vuelta.

—Para conversar hace falta un idioma que los dos entiendan, {heroe} —dice {mentor}—. Uno simple, que no se rompa si se pierde una palabra.

### Objetivos

- Diseñar un **protocolo de línea** simple y robusto entre la placa y la compu.
- Recibir órdenes en la placa sin bloquear el `loop()`.
- Leer el puerto serie desde un programa de C en la compu (con `termios`).

### Antes de empezar

Botones y perillas (S02-N02). Del camino principal: archivos y `sscanf` (R04-N01) y argumentos (R04-N04).

### Explicación

#### Un protocolo de línea

Las reglas de un protocolo que no se rompe:

- **Texto**, una línea por mensaje, terminada en `\n`: se puede leer con el monitor serie y se interpreta con `sscanf`.
- La placa manda su estado **completo** en cada mensaje (`S 1 0 480 -2`: botón A, botón B, eje x, eje y), no "cambió el botón A". Si se pierde una línea, la siguiente corrige.
- Cada tipo de mensaje empieza con una letra distinta: `S` para el estado, `L` para el LED, `R` para vibrar.

#### Recibir sin bloquear, en la placa

```cpp
while (Serial.available() > 0) {       // solo lo que ya llegó: no espera
  char c = Serial.read();
  if (c == '\n') { /* la orden está completa: interpretarla */ }
  else if (largo < sizeof(orden) - 1) { orden[largo++] = c; }
}
```

#### Leer el puerto desde la compu

En Linux, el puerto serie es un **archivo** (`/dev/ttyACM0` o `/dev/ttyUSB0`). Se abre con `open` y se configura con `termios`: modo crudo (sin eco ni procesamiento) y la misma velocidad que la placa.

```c
int fd = open("/dev/ttyACM0", O_RDWR | O_NOCTTY);
struct termios tio;
tcgetattr(fd, &tio);
cfmakeraw(&tio);
cfsetispeed(&tio, B115200);
cfsetospeed(&tio, B115200);
tcsetattr(fd, TCSANOW, &tio);
```

Como es un archivo, se lee con `read` y se escribe con `write`. Los programas de esta Senda, si no reciben la ruta del puerto como argumento, leen la **entrada estándar**: así se prueban sin placa, con un archivo de líneas `S ...`.

#### Compilar el programa de la compu

```bash
gcc -std=c11 -Wall -Wextra -o lector lector.c
./lector /dev/ttyACM0          # con la placa
./lector < prueba.txt          # sin placa
```

### Código de ejemplo

```cpp
/*
 * S02-N03 - El protocolo: la placa manda su estado COMPLETO en una linea,
 *   S <A> <B> <x> <y>\n        (30 veces por segundo; 1 = apretado; ejes de -512 a 511)
 * y entiende ordenes de la compu:
 *   L1\n / L0\n                (prender o apagar el LED)
 */
const int PIN_A = 2, PIN_B = 3, EJE_X = A0, EJE_Y = A1, LED = LED_BUILTIN;

char orden[16];
byte largo = 0;
unsigned long ultimoEnvio = 0;

void setup()
{
  pinMode(PIN_A, INPUT_PULLUP);
  pinMode(PIN_B, INPUT_PULLUP);
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
}

void loop()
{
  // 1. recibir: se junta la linea de a un caracter, sin bloquear
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      orden[largo] = '\0';
      if (orden[0] == 'L') {
        digitalWrite(LED, orden[1] == '1' ? HIGH : LOW);
      }
      largo = 0;
    } else if (largo < sizeof(orden) - 1) {
      orden[largo++] = c;
    }
  }
  // 2. mandar el estado completo cada 33 ms (si se pierde una linea, la proxima corrige)
  if (millis() - ultimoEnvio >= 33) {
    ultimoEnvio = millis();
    Serial.print("S ");
    Serial.print(!digitalRead(PIN_A));
    Serial.print(' ');
    Serial.print(!digitalRead(PIN_B));
    Serial.print(' ');
    Serial.print(analogRead(EJE_X) - 512);
    Serial.print(' ');
    Serial.println(analogRead(EJE_Y) - 512);
  }
}
```

### ¿Para qué sirve?

Los protocolos de línea de texto están en todos lados: los módems y los módulos GPS hablan con comandos de texto, las impresoras 3D reciben G-code línea por línea, y muchos sensores industriales mandan su estado así. Leer un puerto serie desde C es lo que hacen los programas que controlan máquinas, estaciones meteorológicas y robots desde una compu.

### Errores habituales

**Troll: el `loop()` bloqueado.** Esperar con `while (!Serial.available())` congela la placa hasta que llegue algo.

**Orco: la orden sin límite.** Juntar caracteres sin controlar el tamaño del array desborda la memoria (y en la placa hay muy poca).

**Goblin: el `\r` escondido.** Algunos monitores mandan `\r\n`: si no se descarta el `\r`, la orden `LED 1` no coincide.

**Ogro: mandar solo los cambios.** Si se pierde el mensaje "soltó el botón", la compu cree que sigue apretado para siempre.

**Troll: el puerto sin configurar.** Sin `termios`, el sistema procesa los bytes (eco, fin de línea) y los mensajes llegan mezclados.

### Misión S02-N03-M1 · La consola del Gremio

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, ino
```

#### Consigna

Programá la placa para que responda órdenes de texto por el puerto serie, sin importar mayúsculas y sin bloquear el `loop()`:

- `HOLA`: responde un saludo.
- `LED 1` / `LED 0`: prende o apaga el LED de la placa y lo confirma.
- `LEER`: responde el valor de A0.
- Cualquier otra cosa: `No entiendo: ...`.

Juntá cada orden hasta el `\n`, descartando el `\r` y sin pasarte de 40 caracteres.

#### Criterio de aprobación

- Junta la línea sin bloquear y sin desbordar.
- Ignora mayúsculas y el `\r`.
- Responde las cuatro órdenes y avisa las desconocidas.

#### Solución de referencia

```cpp
/* S02-N03 Encargo - La consola del Gremio: la placa responde ordenes de texto por el puerto serie. */
const int LED = LED_BUILTIN, SENSOR = A0;
String linea = "";

void responder(String orden)
{
  orden.trim();
  orden.toUpperCase();
  if (orden == "HOLA") {
    Serial.println("Hola, soy el automata del Gremio.");
  } else if (orden == "LED 1" || orden == "LED 0") {
    digitalWrite(LED, orden == "LED 1" ? HIGH : LOW);
    Serial.println(orden == "LED 1" ? "LED prendido" : "LED apagado");
  } else if (orden == "LEER") {
    Serial.print("A0 = ");
    Serial.println(analogRead(SENSOR));
  } else if (orden.length() > 0) {
    Serial.print("No entiendo: ");
    Serial.println(orden);
  }
}

void setup()
{
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
  Serial.println("Ordenes: HOLA, LED 1, LED 0, LEER");
}

void loop()
{
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      responder(linea);
      linea = "";
    } else if (c != '\r' && linea.length() < 40) {
      linea += c;
    }
  }
}
```

### Misión S02-N03-M2 · El lector de la compu

```meta
entrega: codigo
entorno: local
monedas: 5
xp: 20
```

#### Consigna

Escribí en C el programa de la compu que lee el estado del control (`S a b x y`, como manda el sketch del ejemplo). Si recibe la ruta del puerto como argumento, lo abre y lo configura con `termios`; si no, lee la entrada estándar.

Mostrá **solo los cambios**: `A apretado` / `A suelto`, lo mismo con B, y la dirección del joystick (`arriba`, `abajo izquierda`, `centro`…) usando una zona muerta de 60. Ignorá las líneas que no son de estado y, al final, mostrá cuántas líneas leíste y cuántas ignoraste.

#### Criterio de aprobación

- Con argumento abre y configura el puerto; sin argumento lee la entrada.
- Interpreta las líneas `S` con `sscanf` e ignora las demás.
- Muestra solo los cambios, con zona muerta.

#### Entrada de ejemplo

```
Arduino listo
S 0 0 3 -2
S 0 0 5 1
S 1 0 4 0
S 1 0 480 2
S 0 0 470 -350
basura
S 0 1 0 0
S 0 0 -2 510
```

#### Salida esperada

```
A apretado
joystick: derecha
A suelto
joystick: arriba derecha
B apretado
joystick: centro
B suelto
joystick: abajo
9 líneas leídas, 2 ignoradas
```

#### Solución de referencia

```c
/*
 * S02-N03 Mision 2 - El lector de la compu: lee el estado del control por el puerto serie
 * y avisa solo los cambios. Uso: ./lector /dev/ttyACM0   (o sin argumento: lee la entrada)
 */

#define _DEFAULT_SOURCE           /* para cfmakeraw y las velocidades de termios */
#include <errno.h>
#include <fcntl.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>

typedef struct {
    int a, b, x, y;
} Control;

/* Abre el puerto serie en modo crudo a 115200. Sin ruta, lee la entrada estandar (para probar sin placa). */
static int abrir_puerto(const char *ruta)
{
    if (ruta == NULL) {
        return STDIN_FILENO;
    }
    int fd = open(ruta, O_RDWR | O_NOCTTY);
    if (fd < 0) {
        perror(ruta);
        return -1;
    }
    if (isatty(fd)) {
        struct termios tio;
        tcgetattr(fd, &tio);
        cfmakeraw(&tio);                  /* sin eco ni procesamiento: byte a byte */
        cfsetispeed(&tio, B115200);
        cfsetospeed(&tio, B115200);
        tio.c_cflag |= CLOCAL | CREAD;
        tcsetattr(fd, TCSANOW, &tio);
    }
    return fd;
}

/* Lee una linea completa (sin el \n). Devuelve false al terminar la entrada. */
static bool leer_linea(int fd, char *linea, size_t tam)
{
    size_t n = 0;
    char c;
    for (;;) {
        ssize_t r = read(fd, &c, 1);
        if (r == 0 || (r < 0 && errno != EINTR)) {
            return n > 0 && (linea[n] = '\0', true);
        }
        if (r < 0) {
            continue;
        }
        if (c == '\n') {
            linea[n] = '\0';
            return true;
        }
        if (c != '\r' && n < tam - 1) {
            linea[n++] = c;
        }
    }
}

/* "S a b x y" -> Control. Las lineas que no son de estado se ignoran. */
static bool interpretar(const char *linea, Control *c)
{
    return sscanf(linea, "S %d %d %d %d", &c->a, &c->b, &c->x, &c->y) == 4;
}

#define ZONA_MUERTA 60              /* el joystick quieto no da exactamente 0 */

static int direccion(int eje)
{
    return eje > ZONA_MUERTA ? 1 : eje < -ZONA_MUERTA ? -1 : 0;
}

int main(int argc, char *argv[])
{
    int fd = abrir_puerto(argc > 1 ? argv[1] : NULL);
    if (fd < 0) {
        return 1;
    }
    Control antes = { 0, 0, 0, 0 }, ahora;
    char linea[64];
    int lineas = 0, invalidas = 0;
    while (leer_linea(fd, linea, sizeof linea)) {
        lineas++;
        if (!interpretar(linea, &ahora)) {
            invalidas++;
            continue;
        }
        if (ahora.a != antes.a) printf("A %s\n", ahora.a ? "apretado" : "suelto");
        if (ahora.b != antes.b) printf("B %s\n", ahora.b ? "apretado" : "suelto");
        int dx = direccion(ahora.x), dy = direccion(ahora.y);
        if (dx != direccion(antes.x) || dy != direccion(antes.y)) {
            const char *vertical = dy < 0 ? "arriba" : dy > 0 ? "abajo" : "";
            const char *horizontal = dx < 0 ? "izquierda" : dx > 0 ? "derecha" : "";
            if (dx == 0 && dy == 0) {
                printf("joystick: centro\n");
            } else {
                printf("joystick: %s%s%s\n", vertical, dx != 0 && dy != 0 ? " " : "", horizontal);
            }
        }
        antes = ahora;
    }
    printf("%d líneas leídas, %d ignoradas\n", lineas, invalidas);
    if (fd != STDIN_FILENO) {
        close(fd);
    }
    return 0;
}
```

### Prueba del sello

#### ¿Por qué conviene que la placa mande su estado completo en cada línea?

Porque si se pierde una línea, la siguiente corrige: el estado nunca queda desactualizado.

#### ¿Cómo recibe órdenes la placa sin bloquear el `loop()`?

Leyendo solo lo que ya llegó (`Serial.available()`) y juntando los caracteres hasta el `\n`.

#### ¿Qué es `/dev/ttyACM0` para un programa de C?

Un archivo: se abre con `open`, se configura con `termios` y se lee y escribe con `read` y `write`.

#### ¿Para qué sirve que el programa de la compu lea la entrada estándar si no recibe el puerto?

Para probarlo sin placa, con un archivo de líneas de ejemplo.

### Soluciones (docente)

Basado en `15-Arduino` (04 PC-a-Placa, 05 Protocolo, 06 PC-LeerSerie, reescrito en C). La misión 2 es C de la compu: se corrige con la entrada de ejemplo.

## S02-N04 · Jefe de los Autómatas: el Autómata Guardián

```meta
tipo: jefe
padre: S02-N03
precio: 10
criatura: dragon
ejecutable: no
insignia: Artífice de Autómatas
insignia_descripcion: Venciste al Autómata Guardián: tu código mueve el mundo real desde una placa.
```

### Crónica

En el fondo del Taller espera el **Autómata Guardián**, el más grande de todos. No tiene espada: tiene un joystick de bronce y una fila de luces en el pecho. Te desafía a un juego: recorrer la mazmorra del Dragón… pero con **su** control.

—Es la prueba de todo artífice, {heroe} —dice {mentor}—. Que la placa y la compu trabajen juntas, cada una en lo suyo.

### Objetivos

- Usar la placa como **control** de un programa de la compu, en las dos direcciones.
- Convertir un estado continuo (el joystick) en acciones discretas (un paso por inclinación).
- Mostrar datos de la compu en el mundo físico (LEDs en binario).

### Antes de empezar

Toda la Senda de los Autómatas y la mazmorra del jefe final (R05-N04).

### Explicación

#### El reparto del trabajo

- **La placa**: lee botones y joystick y los manda (`S a b x y`), 30 veces por segundo. Obedece órdenes simples (`R150`: vibrar 150 ms; `P7`: mostrar 7 en los LEDs).
- **La compu**: tiene el juego (la mazmorra) y decide qué pasa.

Ninguna de las dos espera a la otra: cada una lee lo que hay y sigue.

#### De un eje a un paso

El joystick manda un valor continuo (de −512 a 511). Para moverse de a una casilla:

1. Se decide la dirección con un **umbral** (más de 300 hacia un lado).
2. Se da **un** paso solo cuando pasa de centrado a inclinado (el **flanco**, como con los botones). Mantenerlo inclinado no sigue avanzando.

#### Números en luces

Con 4 LEDs se muestra un número de 0 a 15 en **binario**: el LED del bit `k` se prende si `(n >> k) & 1`. Son los operadores de bits del principio del camino.

### Código de ejemplo

```cpp
/*
 * S02-N03 - El protocolo: la placa manda su estado COMPLETO en una linea,
 *   S <A> <B> <x> <y>\n        (30 veces por segundo; 1 = apretado; ejes de -512 a 511)
 * y entiende ordenes de la compu:
 *   L1\n / L0\n                (prender o apagar el LED)
 */
const int PIN_A = 2, PIN_B = 3, EJE_X = A0, EJE_Y = A1, LED = LED_BUILTIN;

char orden[16];
byte largo = 0;
unsigned long ultimoEnvio = 0;

void setup()
{
  pinMode(PIN_A, INPUT_PULLUP);
  pinMode(PIN_B, INPUT_PULLUP);
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
}

void loop()
{
  // 1. recibir: se junta la linea de a un caracter, sin bloquear
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      orden[largo] = '\0';
      if (orden[0] == 'L') {
        digitalWrite(LED, orden[1] == '1' ? HIGH : LOW);
      }
      largo = 0;
    } else if (largo < sizeof(orden) - 1) {
      orden[largo++] = c;
    }
  }
  // 2. mandar el estado completo cada 33 ms (si se pierde una linea, la proxima corrige)
  if (millis() - ultimoEnvio >= 33) {
    ultimoEnvio = millis();
    Serial.print("S ");
    Serial.print(!digitalRead(PIN_A));
    Serial.print(' ');
    Serial.print(!digitalRead(PIN_B));
    Serial.print(' ');
    Serial.print(analogRead(EJE_X) - 512);
    Serial.print(' ');
    Serial.println(analogRead(EJE_Y) - 512);
  }
}
```

### ¿Para qué sirve?

Es la arquitectura de los controles de videojuegos, los simuladores de manejo y las máquinas arcade (una placa lee los botones y le habla a la compu), y también la de los paneles de control industriales, donde un microcontrolador lee sensores y una compu toma las decisiones y muestra el estado.

### Errores habituales

El Guardián combina a las criaturas de la Senda:

- **Ogro**: un paso por cada línea recibida: mantener el joystick recorre media mazmorra de golpe. Hay que detectar el flanco.
- **Ogro**: sin umbral, el temblor del joystick centrado produce pasos fantasma.
- **Troll**: escribir al puerto sin revisar lo que devuelve `write`.
- **Orco**: mostrar en 4 LEDs un número mayor a 15 (se limita con `constrain`).
- **Goblin**: el `\r` al final de las órdenes.

### Misión S02-N04-M1 · La mazmorra con control

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Escribí en C la mazmorra de la exploración (el mapa del jefe final) movida por el control: el programa lee líneas `S a b x y` (del puerto si recibe su ruta, o de la entrada estándar).

- La dirección sale del eje con más inclinación, con un umbral de 300 (`y` negativa es arriba).
- Se da **un paso** solo al pasar de centrado a inclinado.
- Las paredes frenan (`Pared.`) y le piden a la placa que vibre mandando `R150\n` (sin placa, mostrá `(el control vibra)`); los tesoros suman 10 de oro; la `S` termina.
- Al final, mostrá si salió, los pasos y el oro.

#### Criterio de aprobación

- Un paso por inclinación (flanco), con umbral.
- Frena en las paredes y pide vibrar.
- Lee del puerto o de la entrada estándar.

#### Entrada de ejemplo

```
S 0 0 0 0
S 0 0 0 -500
S 0 0 0 0
S 0 0 500 0
S 0 0 0 0
S 0 0 500 0
S 0 0 0 0
S 0 0 0 500
S 0 0 0 0
S 0 0 0 500
S 0 0 0 0
S 0 0 500 0
S 0 0 0 0
S 0 0 500 0
S 0 0 0 0
S 0 0 0 -500
S 0 0 0 0
S 0 0 0 -500
S 0 0 0 0
S 0 0 500 0
S 0 0 0 0
S 0 0 500 0
S 0 0 0 0
S 0 0 500 0
S 0 0 0 0
S 0 0 500 0
S 0 0 0 0
S 0 0 500 0
S 0 0 0 0
S 0 0 500 0
S 0 0 0 0
S 0 0 0 500
S 0 0 0 0
S 0 0 0 500
S 0 0 0 0
S 0 0 0 500
S 0 0 0 0
S 0 0 0 500
S 0 0 0 0
```

#### Salida esperada

```
Pared.
  (el control vibra)
¡Tesoro! Oro: 10
¡Saliste con el control! Pasos: 18. Oro: 10.
```

#### Solución de referencia

```c
/*
 * S02-N04 Mision 1 - La mazmorra con control: el heroe de la mazmorra del jefe final
 * se mueve con el joystick. Un paso por cada vez que se inclina (no uno por linea);
 * al chocar una pared, la compu le pide a la placa que vibre (R150).
 * Uso: ./mazmorra /dev/ttyACM0   (o sin argumento: lee la entrada)
 */

#define _DEFAULT_SOURCE           /* para cfmakeraw y las velocidades de termios */
#include <errno.h>
#include <fcntl.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>

typedef struct {
    int a, b, x, y;
} Control;

/* Abre el puerto serie en modo crudo a 115200. Sin ruta, lee la entrada estandar (para probar sin placa). */
static int abrir_puerto(const char *ruta)
{
    if (ruta == NULL) {
        return STDIN_FILENO;
    }
    int fd = open(ruta, O_RDWR | O_NOCTTY);
    if (fd < 0) {
        perror(ruta);
        return -1;
    }
    if (isatty(fd)) {
        struct termios tio;
        tcgetattr(fd, &tio);
        cfmakeraw(&tio);                  /* sin eco ni procesamiento: byte a byte */
        cfsetispeed(&tio, B115200);
        cfsetospeed(&tio, B115200);
        tio.c_cflag |= CLOCAL | CREAD;
        tcsetattr(fd, TCSANOW, &tio);
    }
    return fd;
}

/* Lee una linea completa (sin el \n). Devuelve false al terminar la entrada. */
static bool leer_linea(int fd, char *linea, size_t tam)
{
    size_t n = 0;
    char c;
    for (;;) {
        ssize_t r = read(fd, &c, 1);
        if (r == 0 || (r < 0 && errno != EINTR)) {
            return n > 0 && (linea[n] = '\0', true);
        }
        if (r < 0) {
            continue;
        }
        if (c == '\n') {
            linea[n] = '\0';
            return true;
        }
        if (c != '\r' && n < tam - 1) {
            linea[n++] = c;
        }
    }
}

/* "S a b x y" -> Control. Las lineas que no son de estado se ignoran. */
static bool interpretar(const char *linea, Control *c)
{
    return sscanf(linea, "S %d %d %d %d", &c->a, &c->b, &c->x, &c->y) == 4;
}

#include <stdlib.h>

#define FILAS 7
#define COLUMNAS 13
#define UMBRAL 300

static const char *MAPA[FILAS] = {
    "#############",
    "#@..#...$...#",
    "#.#.#.###.#.#",
    "#.#...#$..#.#",
    "#.###.#.###.#",
    "#$........#S#",
    "#############",
};

static int fd_puerto = -1;

static void vibrar(void)
{
    if (fd_puerto != STDIN_FILENO && fd_puerto >= 0) {
        if (write(fd_puerto, "R150\n", 5) != 5) {
            perror("vibrar");
        }
    } else {
        printf("  (el control vibra)\n");
    }
}

int main(int argc, char *argv[])
{
    fd_puerto = abrir_puerto(argc > 1 ? argv[1] : NULL);
    if (fd_puerto < 0) {
        return 1;
    }
    char mapa[FILAS][COLUMNAS + 1];
    int fila = 0, columna = 0, oro = 0, pasos = 0;
    for (int f = 0; f < FILAS; f++) {
        strcpy(mapa[f], MAPA[f]);
        char *arroba = strchr(mapa[f], '@');
        if (arroba != NULL) {
            fila = f;
            columna = (int) (arroba - mapa[f]);
            *arroba = '.';
        }
    }

    bool inclinado = false, salio = false;
    Control c;
    char linea[64];
    while (!salio && leer_linea(fd_puerto, linea, sizeof linea)) {
        if (!interpretar(linea, &c)) {
            continue;
        }
        int df = 0, dc = 0;
        if (abs(c.x) > abs(c.y)) {
            dc = c.x > UMBRAL ? 1 : c.x < -UMBRAL ? -1 : 0;
        } else {
            df = c.y > UMBRAL ? 1 : c.y < -UMBRAL ? -1 : 0;
        }
        bool ahora = df != 0 || dc != 0;
        if (ahora && !inclinado) {                 /* recien se inclino: un paso */
            char destino = mapa[fila + df][columna + dc];
            if (destino == '#') {
                printf("Pared.\n");
                vibrar();
            } else {
                fila += df;
                columna += dc;
                pasos++;
                if (destino == '$') {
                    oro += 10;
                    mapa[fila][columna] = '.';
                    printf("¡Tesoro! Oro: %d\n", oro);
                } else if (destino == 'S') {
                    salio = true;
                }
            }
        }
        inclinado = ahora;
    }
    printf("%s Pasos: %d. Oro: %d.\n", salio ? "¡Saliste con el control!" : "Se cortó la conexión.", pasos, oro);
    return 0;
}
```

### Misión S02-N04-M2 · El marcador de oro

```meta
entrega: archivo
entorno: local
monedas: 6
xp: 30
extensiones: zip, ino
```

#### Consigna

Programá la placa para que muestre un número de 0 a 15 en **binario** con 4 LEDs (pines 8 a 11, el bit 0 en el 8). La compu manda `P<n>\n` (por ejemplo `P7`): la placa lo limita a 0–15, prende los LEDs con los operadores de bits y confirma por el puerto serie mostrando el número y sus 4 bits (`marcador: 7 = 0111`).

#### Criterio de aprobación

- Junta la orden sin bloquear.
- Prende cada LED con `(n >> bit) & 1`.
- Limita el número a 0–15 y lo confirma en binario.

#### Solución de referencia

```cpp
/* S02-N04 Mision 2 - El marcador de oro: la compu manda "P<n>" y la placa muestra n (0 a 15) en binario con 4 LEDs. */
const int LEDS[4] = { 8, 9, 10, 11 };     // bit 0 en el 8 ... bit 3 en el 11
char orden[12];
byte largo = 0;

void mostrar(int n)
{
  for (int bit = 0; bit < 4; bit++) {
    digitalWrite(LEDS[bit], (n >> bit) & 1 ? HIGH : LOW);   // los operadores de bits del camino principal
  }
  Serial.print("marcador: ");
  Serial.print(n);
  Serial.print(" = ");
  for (int bit = 3; bit >= 0; bit--) {
    Serial.print((n >> bit) & 1);
  }
  Serial.println();
}

void setup()
{
  for (int i = 0; i < 4; i++) {
    pinMode(LEDS[i], OUTPUT);
  }
  Serial.begin(115200);
  mostrar(0);
}

void loop()
{
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      orden[largo] = '\0';
      if (orden[0] == 'P') {
        int n = atoi(orden + 1);
        mostrar(constrain(n, 0, 15));
      }
      largo = 0;
    } else if (largo < sizeof(orden) - 1) {
      orden[largo++] = c;
    }
  }
}
```

### Encargo S02-N04-E1 · El registro de la sesión

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 30
```

#### Consigna

Para ver cómo se usa el control, escribí en C un programa que lea una sesión (líneas `S a b x y`, del puerto o de la entrada estándar) y muestre: cuántos estados llegaron (y cuántos segundos son, a 30 por segundo), cuántas veces se apretó cada botón (contando flancos) y el recorrido de cada eje (mínimo y máximo).

#### Criterio de aprobación

- Cuenta las pulsaciones por flanco.
- Calcula el recorrido de los ejes.
- Ignora las líneas que no son de estado.

#### Entrada de ejemplo

```
S 0 0 0 0
S 1 0 0 0
S 1 0 200 0
S 0 0 511 -12
S 1 0 300 -512
S 0 1 -490 0
S 0 1 -512 480
S 0 0 0 0
S 1 1 0 0
```

#### Salida esperada

```
Estados recibidos: 9 (unos 0.3 segundos a 30 por segundo)
Pulsaciones: A 3, B 2
Recorrido del joystick: x de -512 a 511, y de -512 a 480
```

#### Solución de referencia

```c
/* S02-N04 Encargo - El registro de la sesion: estadisticas de una partida con el control. */

#define _DEFAULT_SOURCE           /* para cfmakeraw y las velocidades de termios */
#include <errno.h>
#include <fcntl.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>

typedef struct {
    int a, b, x, y;
} Control;

/* Abre el puerto serie en modo crudo a 115200. Sin ruta, lee la entrada estandar (para probar sin placa). */
static int abrir_puerto(const char *ruta)
{
    if (ruta == NULL) {
        return STDIN_FILENO;
    }
    int fd = open(ruta, O_RDWR | O_NOCTTY);
    if (fd < 0) {
        perror(ruta);
        return -1;
    }
    if (isatty(fd)) {
        struct termios tio;
        tcgetattr(fd, &tio);
        cfmakeraw(&tio);                  /* sin eco ni procesamiento: byte a byte */
        cfsetispeed(&tio, B115200);
        cfsetospeed(&tio, B115200);
        tio.c_cflag |= CLOCAL | CREAD;
        tcsetattr(fd, TCSANOW, &tio);
    }
    return fd;
}

/* Lee una linea completa (sin el \n). Devuelve false al terminar la entrada. */
static bool leer_linea(int fd, char *linea, size_t tam)
{
    size_t n = 0;
    char c;
    for (;;) {
        ssize_t r = read(fd, &c, 1);
        if (r == 0 || (r < 0 && errno != EINTR)) {
            return n > 0 && (linea[n] = '\0', true);
        }
        if (r < 0) {
            continue;
        }
        if (c == '\n') {
            linea[n] = '\0';
            return true;
        }
        if (c != '\r' && n < tam - 1) {
            linea[n++] = c;
        }
    }
}

/* "S a b x y" -> Control. Las lineas que no son de estado se ignoran. */
static bool interpretar(const char *linea, Control *c)
{
    return sscanf(linea, "S %d %d %d %d", &c->a, &c->b, &c->x, &c->y) == 4;
}

int main(int argc, char *argv[])
{
    int fd = abrir_puerto(argc > 1 ? argv[1] : NULL);
    if (fd < 0) {
        return 1;
    }
    Control c, antes = { 0, 0, 0, 0 };
    int estados = 0, pulsaciones_a = 0, pulsaciones_b = 0, max_x = 0, min_x = 0, max_y = 0, min_y = 0;
    char linea[64];
    while (leer_linea(fd, linea, sizeof linea)) {
        if (!interpretar(linea, &c)) {
            continue;
        }
        estados++;
        pulsaciones_a += c.a && !antes.a;          /* se cuenta el flanco, no cada linea */
        pulsaciones_b += c.b && !antes.b;
        if (c.x > max_x) max_x = c.x;
        if (c.x < min_x) min_x = c.x;
        if (c.y > max_y) max_y = c.y;
        if (c.y < min_y) min_y = c.y;
        antes = c;
    }
    printf("Estados recibidos: %d (unos %.1f segundos a 30 por segundo)\n", estados, estados / 30.0);
    printf("Pulsaciones: A %d, B %d\n", pulsaciones_a, pulsaciones_b);
    printf("Recorrido del joystick: x de %d a %d, y de %d a %d\n", min_x, max_x, min_y, max_y);
    return 0;
}
```

### Prueba del sello

#### ¿Qué hace la placa y qué hace la compu en el proyecto?

La placa lee el control y obedece órdenes simples; la compu tiene el juego y decide qué pasa.

#### ¿Por qué se da un paso solo al pasar de centrado a inclinado?

Porque llegan 30 estados por segundo: si se diera un paso por línea, mantener el joystick avanzaría muchas casillas de golpe.

#### ¿Cómo se sabe si el LED del bit 2 va prendido para mostrar el 6?

Con `(6 >> 2) & 1`, que da 1: el 6 es `0110` en binario.

#### ¿Para qué sirve el umbral del joystick?

Para ignorar el pequeño temblor del joystick centrado y no dar pasos fantasma.

### Soluciones (docente)

Jefe basado en `15-Arduino/07-ControlArcade`, reescrito en C y conectado a la mazmorra del jefe final del camino principal.
