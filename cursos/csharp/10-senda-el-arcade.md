# RAMA S04 · Senda del Arcade: un juego a la manera de Unity y Godot

```meta
tipo: senda
posicion: 10
```

## S04-N01 · El bucle del juego

```meta
tipo: tema
padre: R06-N02
precio: 3
moneda: comodin
criatura: ogro
temas: juegos.bucle, juegos.entrada
usa: prog.bucles, prog.matematica-azar
```

### Crónica

Después de la Arena, Bemol no duerme. Se pasa las noches dibujando en un cuaderno: una nave chiquita, meteoros, un marcador de puntos. —Quiero hacer un **arcade** para la Feria —le dice a Ceci, con los ojos brillando—. Una máquina con una pantalla, donde la gente juegue. Como los juegos que se hacen con **Unity** y **Godot**.

—La Arena era por turnos —dice Ceci—. Un arcade no espera a nadie.

—Por eso. Tiene que moverse **solo**. —Bemol abre el cuaderno en una página llena de flechas—. Dicen que todos los juegos, por dentro, son la misma vuelta que se repite. Mil veces. Muy rápido.

### Objetivos

- Entender el **bucle del juego**: leer la entrada, actualizar y dibujar, en cada cuadro.
- Mover las cosas según el **tiempo** que pasó (`dt`), no según los cuadros.
- Dibujar la pantalla en texto, cuadro por cuadro, y no dejar que la nave se salga.
- Leer las teclas de una lista fija, para que el juego siempre haga lo mismo y se pueda comprobar.

### Antes de empezar

- La Arena (R06-N01 y N02): `Math.Min`, `Math.Max` y la partida.

### Explicación

#### La vuelta que se repite

Un juego por turnos espera. Un arcade no: muestra un **cuadro** (una foto de la pantalla) tras otro, muchas veces por segundo, y en cada uno hace siempre lo mismo:

1. **Entrada:** qué teclas están apretadas.
2. **Actualizar:** mover todo según el tiempo que pasó.
3. **Dibujar:** mostrar cómo quedó.

En **Unity** eso es el método `Update()`, y en **Godot**, `_process(delta)`: el motor lo llama en cada cuadro.

#### El tiempo de cada cuadro: `dt`

Cada cuadro dura un poquito. Ese tiempo se llama `dt` (*delta time*, «cuánto pasó»). La velocidad se dice en **casillas por segundo**, y lo que se mueve en un cuadro es velocidad × tiempo:

```csharp
double velocidad = 4;   // casillas por segundo
double dt = 0.25;       // cada cuadro dura un cuarto de segundo
x += velocidad * dt;    // en cada cuadro avanza 1 casilla
```

Así, el juego va igual de rápido en una compu lenta (pocos cuadros largos) que en una rápida (muchos cuadros cortos). En Unity se escribe `Time.deltaTime`.

#### Dibujar en texto

Acá la pantalla es una fila de puntos, y la nave es una `@`. La posición es un `double` (puede estar entre dos casillas), así que se **redondea** para dibujarla:

```csharp
char[] fila = new string('.', ancho).ToCharArray();
fila[(int)Math.Round(x)] = '@';
Console.WriteLine(new string(fila));
```

#### Que no se salga

`Math.Clamp(valor, mínimo, máximo)` deja el valor adentro de los bordes, en una sola línea (es `Math.Min` y `Math.Max` juntos):

```csharp
x = Math.Clamp(x, 0, ancho - 1);
```

#### Las teclas, de una lista

En la Feria, la gente aprieta botones. Acá, para que el juego siempre dé lo mismo, las teclas vienen en un texto: una letra por cuadro (`D` derecha, `I` izquierda, espacio quieto).

### Código de ejemplo

```csharp
int ancho = 10;
double x = 0;
double dt = 0.25;
string teclas = "DDDII";

foreach (char tecla in teclas)
{
    double velocidad = tecla switch { 'D' => 4, 'I' => -4, _ => 0 };
    x = Math.Clamp(x + velocidad * dt, 0, ancho - 1);
    Dibujar(x);
}

void Dibujar(double posicion)
{
    char[] fila = new string('.', ancho).ToCharArray();
    fila[(int)Math.Round(posicion)] = '@';
    Console.WriteLine(new string(fila));
}
```

### Salida esperada

```
.@........
..@.......
...@......
..@.......
.@........
```

### ¿Para qué sirve?

Es el corazón de todo videojuego, desde el arcade más viejo hasta los de Unity y Godot. Y la idea de actualizar según el tiempo que pasó también está en las animaciones de una página, en las simulaciones y en los robots.

### Errores habituales

- **Mover por cuadro y no por tiempo:** en una compu rápida, el juego va al doble.
- **Dibujar sin redondear:** una posición `double` no sirve como lugar en un arreglo.
- **Olvidarse los bordes:** la nave se sale de la pantalla y el programa se rompe (el orco de las posiciones).
- **Dibujar antes de actualizar:** la pantalla muestra siempre el cuadro anterior. Es el **ogro** del bucle.

### Micro-misión S04-N01-P1 · El primer cuadro

```meta
lugar: El taller de Bemol
personajes: Bemol, Ceci
carta: Dibujar | char[] fila = new string('.', ancho).ToCharArray(); · fila[3] = '@'; · new string(fila)
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Bemol armó la pantalla del arcade: una fila de diez lucecitas. Pero la nave no aparece: la función que dibuja hace la fila y se olvida de ponerla.

#### Gheco sugiere
Un `string` no se puede cambiar letra por letra. Por eso se pasa a un `char[]`, se cambia la casilla, y se vuelve a armar el texto:

```csharp
char[] palabra = "gato".ToCharArray();
palabra[0] = 'p';
Console.WriteLine(new string(palabra));   // pato
```

#### Desafío
Donde dice `// poné la nave`, escribí `fila[(int)Math.Round(posicion)] = '@';`.

#### Pasos
1. Cambiá `// poné la nave` por `fila[(int)Math.Round(posicion)] = '@';`.
2. Tocá **Ejecutar**. Tiene que salir `...@......`.

#### Código inicial
```csharp
int ancho = 10;
Dibujar(3);

void Dibujar(double posicion)
{
    char[] fila = new string('.', ancho).ToCharArray();
    // poné la nave
    Console.WriteLine(new string(fila));
}
```

#### Salida esperada
```
...@......
```

#### Solución
```csharp
int ancho = 10;
Dibujar(3);

void Dibujar(double posicion)
{
    char[] fila = new string('.', ancho).ToCharArray();
    fila[(int)Math.Round(posicion)] = '@';
    Console.WriteLine(new string(fila));
}
```

#### Al superarla
Una lucecita se enciende en la cuarta casilla. Bemol aplaude como si hubiera ganado la Feria entera. —¡Mi nave!

#### Imagen
- Un taller de madera desordenado con una máquina de arcade a medio armar, con una pantalla de diez lucecitas en fila y una sola encendida, sin letras.
- Bemol, MUY GORDITO con panza, aplaude delante de la pantalla; Ceci, con su violín a la espalda, sostiene un destornillador.

### Micro-misión S04-N01-P2 · Cuatro casillas por segundo

```meta
lugar: El taller de Bemol
personajes: Bemol, Ceci, Gheco
carta: dt | x += velocidad * dt; · velocidad en casillas por segundo · dt: lo que dura el cuadro
recompensa: xp 15, oro 15
```

#### Escena
Bemol quiere que la nave avance cuatro casillas por segundo. Pero su programa le suma la velocidad entera en cada cuadro, y como hay cuatro cuadros por segundo, la nave sale disparada y se estrella contra el borde.

#### Gheco sugiere
Lo que se mueve en un cuadro es la velocidad **por** lo que dura el cuadro:

```csharp
double metrosPorSegundo = 10;
double cuadro = 0.1;
distancia += metrosPorSegundo * cuadro;   // 1 metro por cuadro
```

#### Desafío
Cambiá `x += velocidad;` por `x += velocidad * dt;`.

#### Pasos
1. Cambiá `x += velocidad;` por `x += velocidad * dt;`.
2. Tocá **Ejecutar**. La nave avanza de a una casilla.

#### Código inicial
```csharp
int ancho = 10;
double x = 0;
double velocidad = 4;
double dt = 0.25;

for (int cuadro = 1; cuadro <= 4; cuadro++)
{
    x += velocidad;
    Dibujar(x);
}

void Dibujar(double posicion)
{
    char[] fila = new string('.', ancho).ToCharArray();
    fila[(int)Math.Round(posicion)] = '@';
    Console.WriteLine(new string(fila));
}
```

#### Salida esperada
```
.@........
..@.......
...@......
....@.....
```

#### Solución
```csharp
int ancho = 10;
double x = 0;
double velocidad = 4;
double dt = 0.25;

for (int cuadro = 1; cuadro <= 4; cuadro++)
{
    x += velocidad * dt;
    Dibujar(x);
}

void Dibujar(double posicion)
{
    char[] fila = new string('.', ancho).ToCharArray();
    fila[(int)Math.Round(posicion)] = '@';
    Console.WriteLine(new string(fila));
}
```

#### Al superarla
La nave avanza de a una casilla, suavecita, y en un segundo justo recorre cuatro. Bemol mira el reloj de la pared y la pantalla, el reloj y la pantalla. —Va a tiempo.

#### Imagen
- La pantalla del arcade con lucecitas en fila, varias encendidas en escalera como un rastro, sin letras.
- Bemol mira un reloj de pared con la boca abierta; Gheco, un gecko de luz cian con antiparras, MINÚSCULO, sentado arriba de la máquina, marca el tiempo con el dedo.

### Micro-misión S04-N01-P3 · Los bordes de la pantalla

```meta
lugar: El taller de Bemol
personajes: Bemol, Ceci
carta: Clamp | x = Math.Clamp(x, 0, ancho - 1); · nunca menos de 0 · nunca más del último lugar
recompensa: xp 15, oro 15
```

#### Escena
Ahora la nave va más rápido, y cuando llega al final de la pantalla, sigue de largo. El programa se rompe: quiere dibujarla en una casilla que no existe.

#### Gheco sugiere
`Math.Clamp` deja un número adentro de un rango. Si se pasa, lo pone en el borde:

```csharp
int volumen = Math.Clamp(15, 0, 10);   // 10
```

#### Desafío
Después de mover la nave, agregá `x = Math.Clamp(x, 0, ancho - 1);`.

#### Pasos
1. Debajo de `x += velocidad * dt;`, escribí `x = Math.Clamp(x, 0, ancho - 1);`.
2. Tocá **Ejecutar**. La nave se tiene que quedar en el borde.

#### Código inicial
```csharp
int ancho = 10;
double x = 0;
double velocidad = 8;
double dt = 0.25;

for (int cuadro = 1; cuadro <= 6; cuadro++)
{
    x += velocidad * dt;
    Dibujar(x);
}

void Dibujar(double posicion)
{
    char[] fila = new string('.', ancho).ToCharArray();
    fila[(int)Math.Round(posicion)] = '@';
    Console.WriteLine(new string(fila));
}
```

#### Salida esperada
```
..@.......
....@.....
......@...
........@.
.........@
.........@
```

#### Solución
```csharp
int ancho = 10;
double x = 0;
double velocidad = 8;
double dt = 0.25;

for (int cuadro = 1; cuadro <= 6; cuadro++)
{
    x += velocidad * dt;
    x = Math.Clamp(x, 0, ancho - 1);
    Dibujar(x);
}

void Dibujar(double posicion)
{
    char[] fila = new string('.', ancho).ToCharArray();
    fila[(int)Math.Round(posicion)] = '@';
    Console.WriteLine(new string(fila));
}
```

#### Al superarla
La nave llega al borde y se queda ahí, temblando contra el marco de la pantalla. Ceci le pone una almohadita al costado de la máquina, por las dudas.

#### Imagen
- La pantalla del arcade con la última lucecita de la fila encendida y brillando contra el marco, sin letras.
- Ceci apoya un almohadón contra el costado de la máquina; Bemol se ríe.

### Micro-misión S04-N01-P4 · Los botones

```meta
lugar: El taller de Bemol
personajes: Bemol, Ceci, Gheco
carta: Entrada | velocidad = tecla switch { 'D' => 4, 'I' => -4, _ => 0 }; · una tecla por cuadro
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol le puso a la máquina dos botones, uno a cada lado. Pero el programa no los mira: la nave va siempre para la derecha, apriete lo que apriete.

#### Gheco sugiere
En cada cuadro se lee la tecla y se decide la velocidad. Un `switch` de flechas lo hace en una línea:

```csharp
int paso = boton switch { 'A' => -1, 'B' => 1, _ => 0 };
```

#### Desafío
Adentro del `foreach`, cambiá `double velocidad = 4;` por `double velocidad = tecla switch { 'D' => 4, 'I' => -4, _ => 0 };`.

#### Pasos
1. Cambiá `double velocidad = 4;` por `double velocidad = tecla switch { 'D' => 4, 'I' => -4, _ => 0 };`.
2. Tocá **Ejecutar** y compará.

#### Código inicial
```csharp
int ancho = 10;
double x = 0;
double dt = 0.25;
string teclas = "DD II";

foreach (char tecla in teclas)
{
    double velocidad = 4;
    x = Math.Clamp(x + velocidad * dt, 0, ancho - 1);
    Dibujar(x);
}

void Dibujar(double posicion)
{
    char[] fila = new string('.', ancho).ToCharArray();
    fila[(int)Math.Round(posicion)] = '@';
    Console.WriteLine(new string(fila));
}
```

#### Salida esperada
```
.@........
..@.......
..@.......
.@........
@.........
```

#### Solución
```csharp
int ancho = 10;
double x = 0;
double dt = 0.25;
string teclas = "DD II";

foreach (char tecla in teclas)
{
    double velocidad = tecla switch { 'D' => 4, 'I' => -4, _ => 0 };
    x = Math.Clamp(x + velocidad * dt, 0, ancho - 1);
    Dibujar(x);
}

void Dibujar(double posicion)
{
    char[] fila = new string('.', ancho).ToCharArray();
    fila[(int)Math.Round(posicion)] = '@';
    Console.WriteLine(new string(fila));
}
```

#### Al superarla
La nave va, se queda quieta un cuadro y vuelve. Bemol aprieta los botones como loco, aunque el programa lee la lista. —¡Igual siento que la manejo yo!

#### Imagen
- El panel de una máquina de arcade de madera con dos botones grandes y redondos, uno de cada lado, sin letras.
- Bemol aprieta los dos botones con entusiasmo; Gheco, MINÚSCULO, sentado entre los botones, se tapa los oídos; Ceci mira la pantalla.

### Micro-misión S04-N01-P5 · El ogro que dibujaba antes

```meta
lugar: El taller de Bemol
personajes: Bemol, Ceci, Gheco
criatura: ogro
carta: Ogro | primero actualizar, después dibujar · al revés, la pantalla muestra el cuadro anterior
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un ogro de la Feria se ofreció a ayudar y dio vuelta el bucle: ahora la máquina dibuja primero y mueve después. La pantalla llega siempre un cuadro tarde, y la nave nunca se ve donde está de verdad.

#### Gheco sugiere
El orden del bucle importa: si se dibuja antes de actualizar, lo último que se movió no se ve nunca.

```csharp
foreach (var paso in pasos)
{
    Avanzar(paso);    // primero el mundo cambia
    Mostrar();        // después se muestra
}
```

#### Desafío
Poné la línea de `Dibujar(x);` **después** de la que mueve la nave.

#### Pasos
1. Borrá `Dibujar(x);` de arriba.
2. Escribilo debajo de la línea de `x = Math.Clamp(...)`.
3. Tocá **Ejecutar** y compará.

#### Código inicial
```csharp
int ancho = 10;
double x = 0;
double dt = 0.25;
string teclas = "DDD";

foreach (char tecla in teclas)
{
    Dibujar(x);
    double velocidad = tecla switch { 'D' => 4, 'I' => -4, _ => 0 };
    x = Math.Clamp(x + velocidad * dt, 0, ancho - 1);
}

void Dibujar(double posicion)
{
    char[] fila = new string('.', ancho).ToCharArray();
    fila[(int)Math.Round(posicion)] = '@';
    Console.WriteLine(new string(fila));
}
```

#### Salida esperada
```
.@........
..@.......
...@......
```

#### Solución
```csharp
int ancho = 10;
double x = 0;
double dt = 0.25;
string teclas = "DDD";

foreach (char tecla in teclas)
{
    double velocidad = tecla switch { 'D' => 4, 'I' => -4, _ => 0 };
    x = Math.Clamp(x + velocidad * dt, 0, ancho - 1);
    Dibujar(x);
}

void Dibujar(double posicion)
{
    char[] fila = new string('.', ancho).ToCharArray();
    fila[(int)Math.Round(posicion)] = '@';
    Console.WriteLine(new string(fila));
}
```

#### Al superarla
Ahora la nave se ve justo donde está. El ogro mira la pantalla un rato largo, convencido de que antes también andaba, y se va a buscar pochoclos.

#### Imagen
- La máquina de arcade de madera con su pantalla de lucecitas, en el taller desordenado, sin letras.
- El ogro grandote, con camisa cerrada, se rasca la cabeza frente a la pantalla; Gheco, MINÚSCULO, flota delante de él con una flecha de luz que da la vuelta; Bemol y Ceci se miran.

## S04-N02 · Vector2: posiciones con dos números

```meta
tipo: tema
padre: S04-N01
precio: 10
criatura: goblin
temas: poo.operadores, juegos.fisica
usa: poo.records, juegos.bucle
```

### Crónica

Una sola fila le queda chica a Bemol. —Los meteoros caen de **arriba**. La nave tiene que poder subir y bajar. —Ahora cada cosa del juego necesita **dos** números: dónde está a lo ancho y dónde a lo alto.

—En la Arena ya hiciste una posición así —le recuerda Ceci—, con la fila y la columna de las gemas.

—Pero ahora se mueven solas, y en diagonal. Unity y Godot tienen un tipo para esto. Se llama `Vector2`. —Bemol sonríe—. Hagamos el nuestro.

### Objetivos

- Escribir un `Vector2` propio, un `record struct` con dos `double`.
- Sumar vectores y multiplicarlos por un número con operadores (`+` y `*`).
- Mostrarlos lindo, con un `ToString` propio.
- Calcular la **magnitud** (el largo) y **normalizar** (dejar el largo en 1), para que la diagonal no sea más rápida.

### Antes de empezar

- El bucle del juego (S04-N01) y el `record struct` con `operator +` de Junta las Gemas (R06-N03).

### Explicación

#### Dos números que viajan juntos

```csharp
record struct Vector2(double X, double Y)
{
    public static Vector2 operator +(Vector2 a, Vector2 b) => new(a.X + b.X, a.Y + b.Y);
    public static Vector2 operator *(Vector2 v, double k) => new(v.X * k, v.Y * k);
}
```

Con los dos operadores, el movimiento se escribe igual que en una sola fila, pero en dos direcciones a la vez:

```csharp
pos = pos + velocidad * dt;
```

#### Un `ToString` a medida

Un `record struct` se muestra como `Vector2 { X = 2, Y = 1 }`. Se puede cambiar:

```csharp
public override string ToString() => $"({X}, {Y})";
```

#### El largo y la dirección

La **magnitud** de un vector es su largo, por Pitágoras: `√(X² + Y²)`. El vector `(3, 4)` mide 5.

```csharp
public double Magnitud => Math.Sqrt(X * X + Y * Y);
```

Ir en diagonal con `(1, 1)` mide 1,41: **más** que ir derecho con `(1, 0)`. En muchos juegos viejos, la diagonal era más rápida, y los jugadores la aprovechaban. Para que no pase, se **normaliza**: se divide por la magnitud, y queda una flecha de largo 1 que solo dice **hacia dónde**.

```csharp
public Vector2 Normalizado => Magnitud == 0 ? this : new(X / Magnitud, Y / Magnitud);
```

### Código de ejemplo

```csharp
Vector2 pos = new(0, 0);
Vector2 vel = new(4, 2);
double dt = 0.5;

pos = pos + vel * dt;
Console.WriteLine(pos);
Console.WriteLine(new Vector2(3, 4).Magnitud);

Vector2 diagonal = new(1, 1);
Console.WriteLine(Math.Round(diagonal.Magnitud, 2));
Console.WriteLine(Math.Round(diagonal.Normalizado.Magnitud, 2));

record struct Vector2(double X, double Y)
{
    public static Vector2 operator +(Vector2 a, Vector2 b) => new(a.X + b.X, a.Y + b.Y);
    public static Vector2 operator *(Vector2 v, double k) => new(v.X * k, v.Y * k);
    public double Magnitud => Math.Sqrt(X * X + Y * Y);
    public Vector2 Normalizado => Magnitud == 0 ? this : new(X / Magnitud, Y / Magnitud);
    public override string ToString() => $"({X}, {Y})";
}
```

### Salida esperada

```
(2, 1)
5
1,41
1
```

### ¿Para qué sirve?

Unity (`Vector2`, `Vector3`) y Godot (`Vector2`) usan exactamente esto para posiciones, velocidades y direcciones. Y los vectores están en la física, en los mapas, en los gráficos y en la inteligencia artificial.

### Errores habituales

- **Multiplicar sin el operador:** `vel * dt` no compila si el `Vector2` no sabe multiplicarse por un `double`.
- **Usar un `double` como lugar en un arreglo:** hay que redondear y convertir a `int`. Es el **goblin** de los tipos.
- **No normalizar la dirección:** la diagonal va más rápido que lo derecho.
- **Normalizar el `(0, 0)`:** dividir por cero da cualquier cosa; por eso el `Magnitud == 0 ? this`.

### Micro-misión S04-N02-P1 · Multiplicar por el tiempo

```meta
lugar: El taller de Bemol
personajes: Bemol, Ceci
carta: Operador * | public static Vector2 operator *(Vector2 v, double k) => new(v.X * k, v.Y * k);
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Bemol escribe `pos + vel * dt`, como en la fila, pero el programa no compila: su `Vector2` sabe sumarse con otro, pero no multiplicarse por un número.

#### Gheco sugiere
Un operador se define con `operator`, como un método `static`. Para multiplicar por un número, recibe un vector y un `double`:

```csharp
public static Color operator *(Color c, double brillo) => new(c.R * brillo, c.G * brillo, c.B * brillo);
```

#### Desafío
Agregale al `Vector2` el operador `*`: `public static Vector2 operator *(Vector2 v, double k) => new(v.X * k, v.Y * k);`.

#### Pasos
1. Debajo del `operator +`, escribí `public static Vector2 operator *(Vector2 v, double k) => new(v.X * k, v.Y * k);`.
2. Tocá **Ejecutar**. Tiene que salir `(2, 1)`.

#### Código inicial
```csharp
Vector2 pos = new(0, 0);
Vector2 vel = new(4, 2);
double dt = 0.5;
pos = pos + vel * dt;
Console.WriteLine(pos);

record struct Vector2(double X, double Y)
{
    public static Vector2 operator +(Vector2 a, Vector2 b) => new(a.X + b.X, a.Y + b.Y);
    public override string ToString() => $"({X}, {Y})";
}
```

#### Salida esperada
```
(2, 1)
```

#### Solución
```csharp
Vector2 pos = new(0, 0);
Vector2 vel = new(4, 2);
double dt = 0.5;
pos = pos + vel * dt;
Console.WriteLine(pos);

record struct Vector2(double X, double Y)
{
    public static Vector2 operator +(Vector2 a, Vector2 b) => new(a.X + b.X, a.Y + b.Y);
    public static Vector2 operator *(Vector2 v, double k) => new(v.X * k, v.Y * k);
    public override string ToString() => $"({X}, {Y})";
}
```

#### Al superarla
La nave se mueve en diagonal, dos casillas a la derecha y una para arriba. Bemol la sigue con el dedo por la pantalla nueva, que ahora es una grilla.

#### Imagen
- Una pantalla de arcade nueva con una grilla de lucecitas, varias filas y columnas, con una lucecita encendida en diagonal, sin letras.
- Bemol, MUY GORDITO con panza, sigue la lucecita con el dedo; Ceci escribe en un cuaderno.

### Micro-misión S04-N02-P2 · Mostrarlo lindo

```meta
lugar: El taller de Bemol
personajes: Bemol, Gheco
carta: ToString | public override string ToString() => $"({X}, {Y})"; · cambia cómo se muestra
recompensa: xp 15, oro 15
```

#### Escena
El marcador de Bemol muestra la posición de la nave como `Vector2 { X = 1, Y = 2 }`. No entra en la pantallita del costado.

#### Gheco sugiere
`ToString` decide cómo se muestra un objeto. Con `override`, el tuyo reemplaza al que viene:

```csharp
public override string ToString() => $"{Nombre} (nivel {Nivel})";
```

#### Desafío
Agregale al `Vector2` un `ToString` que devuelva `$"({X}, {Y})"`.

#### Pasos
1. Cambiá el `;` del final de `record struct Vector2(double X, double Y);` por unas llaves.
2. Adentro: `public override string ToString() => $"({X}, {Y})";`.
3. Tocá **Ejecutar**. Tiene que salir `Nave en (1, 2)`.

#### Código inicial
```csharp
Vector2 nave = new(1, 2);
Console.WriteLine($"Nave en {nave}");

record struct Vector2(double X, double Y);
```

#### Salida esperada
```
Nave en (1, 2)
```

#### Solución
```csharp
Vector2 nave = new(1, 2);
Console.WriteLine($"Nave en {nave}");

record struct Vector2(double X, double Y)
{
    public override string ToString() => $"({X}, {Y})";
}
```

#### Al superarla
Ahora entra justo en la pantallita: `(1, 2)`. Bemol le pone un marco dorado de cartón.

#### Imagen
- Una pantallita chica al costado de la máquina de arcade con un marco dorado de cartón, sin letras ni números.
- Bemol pega el marco con cinta; Gheco, MINÚSCULO, sentado arriba de la pantallita, sostiene la cinta.

### Micro-misión S04-N02-P3 · La distancia al meteoro

```meta
lugar: El taller de Bemol
personajes: Bemol, Ceci, Clave
carta: Magnitud | Math.Sqrt(X * X + Y * Y) · Pitágoras · (3, 4) mide 5
recompensa: xp 15, oro 15
```

#### Escena
Bemol quiere que la máquina avise cuando un meteoro está cerca. Pero calcula la distancia sumando `X + Y`, y le da 7 donde Clave, con una regla, mide 5.

#### Gheco sugiere
El largo de un vector sale de Pitágoras: la raíz de la suma de los cuadrados.

```csharp
double hipotenusa = Math.Sqrt(cateto1 * cateto1 + cateto2 * cateto2);
```

#### Desafío
Cambiá `Magnitud` para que sea `Math.Sqrt(X * X + Y * Y)`.

#### Pasos
1. Cambiá `X + Y` por `Math.Sqrt(X * X + Y * Y)`.
2. Tocá **Ejecutar**. Tiene que salir `Distancia al meteoro: 5`.

#### Código inicial
```csharp
Vector2 hastaElMeteoro = new(3, 4);
Console.WriteLine($"Distancia al meteoro: {hastaElMeteoro.Magnitud}");

record struct Vector2(double X, double Y)
{
    public double Magnitud => X + Y;
}
```

#### Salida esperada
```
Distancia al meteoro: 5
```

#### Solución
```csharp
Vector2 hastaElMeteoro = new(3, 4);
Console.WriteLine($"Distancia al meteoro: {hastaElMeteoro.Magnitud}");

record struct Vector2(double X, double Y)
{
    public double Magnitud => Math.Sqrt(X * X + Y * Y);
}
```

#### Al superarla
Cinco. Clave guarda la regla. —Pitágoras tocaba la lira, ¿sabías? Le gustaban los números que suenan bien.

#### Imagen
- La grilla del arcade con dos lucecitas encendidas, una nave y un meteoro, unidas por una línea de luz en diagonal, sin letras ni números.
- Clave, con su capa y la mecha blanca en el rodete, mide la pantalla con una regla de madera; Bemol y Ceci miran.

### Micro-misión S04-N02-P4 · La diagonal tramposa

```meta
lugar: El taller de Bemol
personajes: Bemol, Ceci, Gheco
carta: Normalizar | direccion.Normalizado * velocidad · largo 1: solo dice hacia dónde · la diagonal deja de ser más rápida
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Ceci descubre una trampa en el juego de Bemol: si aprieta derecha y arriba a la vez, la nave va más rápido que derecho. Los chicos de la Feria la van a encontrar en dos minutos.

#### Gheco sugiere
Una dirección se **normaliza** antes de multiplicarla por la velocidad: así mide 1, vaya para donde vaya.

```csharp
Vector2 haciaElTesoro = new Vector2(6, 8).Normalizado;   // (0,6; 0,8): mide 1
```

#### Desafío
Cambiá `direccion * velocidad` por `direccion.Normalizado * velocidad`.

#### Pasos
1. Cambiá `direccion * velocidad` por `direccion.Normalizado * velocidad`.
2. Tocá **Ejecutar**. Tiene que salir `Rapidez en diagonal: 4`.

#### Código inicial
```csharp
Vector2 direccion = new(1, 1);
double velocidad = 4;
Vector2 vel = direccion * velocidad;
Console.WriteLine($"Rapidez en diagonal: {Math.Round(vel.Magnitud, 2)}");

record struct Vector2(double X, double Y)
{
    public static Vector2 operator *(Vector2 v, double k) => new(v.X * k, v.Y * k);
    public double Magnitud => Math.Sqrt(X * X + Y * Y);
    public Vector2 Normalizado => Magnitud == 0 ? this : new(X / Magnitud, Y / Magnitud);
}
```

#### Salida esperada
```
Rapidez en diagonal: 4
```

#### Solución
```csharp
Vector2 direccion = new(1, 1);
double velocidad = 4;
Vector2 vel = direccion.Normalizado * velocidad;
Console.WriteLine($"Rapidez en diagonal: {Math.Round(vel.Magnitud, 2)}");

record struct Vector2(double X, double Y)
{
    public static Vector2 operator *(Vector2 v, double k) => new(v.X * k, v.Y * k);
    public double Magnitud => Math.Sqrt(X * X + Y * Y);
    public Vector2 Normalizado => Magnitud == 0 ? this : new(X / Magnitud, Y / Magnitud);
}
```

#### Al superarla
Ahora la nave va igual de rápido para todos lados. Ceci prueba la trampa otra vez, y ya no anda. Bemol suspira, aliviado y un poco triste: le gustaba.

#### Imagen
- La grilla del arcade con una flecha de luz derecha y otra en diagonal del mismo largo, saliendo de la misma lucecita, sin letras.
- Ceci aprieta dos botones a la vez con cara de detective; Bemol se tapa la cara; Gheco, MINÚSCULO, sostiene una regla.

### Micro-misión S04-N02-P5 · El goblin de la casilla y media

```meta
lugar: El taller de Bemol
personajes: Bemol, Gheco
criatura: goblin
carta: Goblin | el lugar en un arreglo es int · pos.X es double · fila[(int)Math.Round(pos.X)]
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un goblin quiere dibujar la nave en la casilla 2,4. El programa no compila: un arreglo no tiene casilla 2,4, solo la 2 o la 3.

#### Gheco sugiere
Una posición `double` se redondea al entero más cercano y se convierte a `int` para usarla como lugar:

```csharp
double nivel = 6.7;
int escalon = (int)Math.Round(nivel);   // 7
```

#### Desafío
Cambiá `fila[pos.X]` por `fila[(int)Math.Round(pos.X)]`.

#### Pasos
1. Cambiá `fila[pos.X]` por `fila[(int)Math.Round(pos.X)]`.
2. Tocá **Ejecutar** y compará.

#### Código inicial
```csharp
Vector2 pos = new(2.4, 0);
char[] fila = new string('.', 10).ToCharArray();
fila[pos.X] = '@';
Console.WriteLine(new string(fila));

record struct Vector2(double X, double Y);
```

#### Salida esperada
```
..@.......
```

#### Solución
```csharp
Vector2 pos = new(2.4, 0);
char[] fila = new string('.', 10).ToCharArray();
fila[(int)Math.Round(pos.X)] = '@';
Console.WriteLine(new string(fila));

record struct Vector2(double X, double Y);
```

#### Al superarla
La nave aparece en la casilla 2, la más cercana. El goblin cuenta las casillas con los dedos, no encuentra la 2,4 y se va, confundido.

#### Imagen
- La pantalla del arcade con una lucecita encendida entre otras apagadas, sin letras ni números.
- Un goblin verde chiquito intenta meter el dedo entre dos lucecitas; Gheco, MINÚSCULO, le señala la lucecita correcta; Bemol mira de costado.

## S04-N03 · Componentes y señales

```meta
tipo: tema
padre: S04-N02
precio: 10
criatura: troll
temas: poo.composicion, juegos.colisiones
usa: poo.abstractas, poo.genericos, func.lambdas
```

### Crónica

El juego crece: una nave, meteoros, estrellas que dan puntos. Bemol empezó a escribir una clase para cada cosa, y se dio cuenta de que la nave y el meteoro se mueven **igual**, y que el meteoro y la estrella chocan **igual**. —Estoy copiando lo mismo en todos lados.

Clave mira el código por encima de los anteojos. —Una orquesta no tiene una clase para cada músico que sabe leer partituras. Cada músico **tiene** lo que sabe hacer.

—Así trabaja Unity —dice Ceci, que estuvo leyendo—: cada cosa del juego es un objeto vacío, y le vas **agregando** piezas. Se llaman **componentes**.

### Objetivos

- Armar una entidad del juego con **componentes** (composición), como un `GameObject` de Unity.
- Escribir un componente que mueve, a partir de una clase abstracta.
- Buscar un componente por su tipo con un método genérico, como `GetComponent<T>()`.
- Saber si dos cajas se tocan (colisión **AABB**).
- Avisar un choque con un **evento**, como las señales de Godot.

### Antes de empezar

- `Vector2` (S04-N02), clases abstractas (Acto II), genéricos (R03-N04) y eventos (R03-N07).

### Explicación

#### Una entidad con piezas

```csharp
abstract class Componente
{
    public abstract void Update(Entidad e, double dt);
}

class Movimiento : Componente
{
    public Vector2 Velocidad { get; set; }
    public Movimiento(Vector2 velocidad) { Velocidad = velocidad; }
    public override void Update(Entidad e, double dt) => e.Pos = e.Pos + Velocidad * dt;
}
```

La `Entidad` tiene una lista de componentes y, en cada cuadro, les pide a todos que se actualicen:

```csharp
public void Update(double dt)
{
    foreach (Componente c in componentes) c.Update(this, dt);
}
```

Una nave es una entidad con `Movimiento`; un meteoro, otra entidad con otro `Movimiento`. Nada se copia.

#### Buscar una pieza por su tipo

```csharp
public T? Get<T>() where T : Componente => componentes.OfType<T>().FirstOrDefault();
```

`OfType<T>()` deja solo los de ese tipo. Es lo mismo que `GetComponent<Movimiento>()` en Unity.

#### ¿Se tocan? AABB

Si cada cosa es una caja de 1×1, dos cajas se tocan si se pisan **a lo ancho y a lo alto**:

```csharp
bool chocan = a.X < b.X + 1 && a.X + 1 > b.X
           && a.Y < b.Y + 1 && a.Y + 1 > b.Y;
```

Se llama AABB (cajas alineadas con los ejes) y es la colisión más usada en los juegos 2D.

#### Señales: avisar sin saber a quién

La nave no tiene que saber quién cuenta los puntos o quién hace sonar la alarma. Solo **avisa** que chocó, con un evento. En Godot eso se llama **señal**:

```csharp
public event Action<string>? AlChocar;
public void Chocar(Entidad otra) => AlChocar?.Invoke(otra.Nombre);
```

Y quien quiere enterarse, se **suscribe**:

```csharp
nave.AlChocar += nombre => Console.WriteLine($"¡{nombre} chocó con la nave!");
```

### Código de ejemplo

```csharp
var nave = new Entidad("Nave", new Vector2(0, 0));
nave.Agregar(new Movimiento(new Vector2(4, 0)));
var meteoro = new Entidad("Meteoro", new Vector2(3, 0));

nave.AlChocar += nombre => Console.WriteLine($"¡{nombre} chocó con la nave!");

for (int cuadro = 1; cuadro <= 4; cuadro++)
{
    nave.Update(0.25);
    Console.WriteLine($"Cuadro {cuadro}: nave en {nave.Pos}");
    if (Chocan(nave, meteoro))
    {
        nave.Chocar(meteoro);
    }
}

bool Chocan(Entidad a, Entidad b) =>
    a.Pos.X < b.Pos.X + 1 && a.Pos.X + 1 > b.Pos.X &&
    a.Pos.Y < b.Pos.Y + 1 && a.Pos.Y + 1 > b.Pos.Y;

record struct Vector2(double X, double Y)
{
    public static Vector2 operator +(Vector2 a, Vector2 b) => new(a.X + b.X, a.Y + b.Y);
    public static Vector2 operator *(Vector2 v, double k) => new(v.X * k, v.Y * k);
    public override string ToString() => $"({X}, {Y})";
}

abstract class Componente
{
    public abstract void Update(Entidad e, double dt);
}

class Movimiento : Componente
{
    public Vector2 Velocidad { get; set; }
    public Movimiento(Vector2 velocidad) { Velocidad = velocidad; }
    public override void Update(Entidad e, double dt) => e.Pos = e.Pos + Velocidad * dt;
}

class Entidad
{
    private readonly List<Componente> componentes = new();
    public string Nombre { get; }
    public Vector2 Pos { get; set; }
    public event Action<string>? AlChocar;

    public Entidad(string nombre, Vector2 pos) { Nombre = nombre; Pos = pos; }
    public void Agregar(Componente c) => componentes.Add(c);
    public T? Get<T>() where T : Componente => componentes.OfType<T>().FirstOrDefault();
    public void Update(double dt)
    {
        foreach (Componente c in componentes)
        {
            c.Update(this, dt);
        }
    }
    public void Chocar(Entidad otra) => AlChocar?.Invoke(otra.Nombre);
}
```

### Salida esperada

```
Cuadro 1: nave en (1, 0)
Cuadro 2: nave en (2, 0)
Cuadro 3: nave en (3, 0)
¡Meteoro chocó con la nave!
Cuadro 4: nave en (4, 0)
```

### ¿Para qué sirve?

Unity está armado entero con componentes (`GameObject` + `GetComponent<T>()`) y Godot con nodos y señales. Y la idea de «armar con piezas en vez de heredar de todo» y «avisar sin saber a quién» sirve igual en cualquier programa grande, juego o no.

### Errores habituales

- **Una clase por cada cosa del juego:** se termina copiando el mismo código en todos lados.
- **Revisar el choque solo a lo ancho:** dos cosas en la misma columna pero en otra fila no se tocan.
- **Disparar el evento sin nadie suscripto:** si nadie escucha, el evento vale `null`. Es el **troll** de las señales. Va `?.Invoke`.

### Micro-misión S04-N03-P1 · La pieza que mueve

```meta
lugar: El taller de Bemol
personajes: Bemol, Ceci
carta: Componente | override void Update(Entidad e, double dt) => e.Pos = e.Pos + Velocidad * dt; · la pieza mueve a su dueño
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Bemol le agregó a la nave la pieza `Movimiento`, pero la nave no se mueve: el `Update` de la pieza está vacío.

#### Gheco sugiere
El componente recibe a su **dueño** (la entidad) y lo cambia. Así, la misma pieza sirve para cualquier entidad:

```csharp
public override void Update(Entidad e, double dt) => e.Brillo = e.Brillo * 0.9;
```

#### Desafío
Completá el `Update` de `Movimiento` para que haga `e.Pos = e.Pos + Velocidad * dt;`.

#### Pasos
1. Adentro del `Update` de `Movimiento`, escribí `e.Pos = e.Pos + Velocidad * dt;`.
2. Tocá **Ejecutar**. Tiene que salir `Nave en (4, 0)`.

#### Código inicial
```csharp
var nave = new Entidad(new Vector2(0, 0));
nave.Agregar(new Movimiento(new Vector2(4, 0)));
for (int cuadro = 1; cuadro <= 4; cuadro++)
{
    nave.Update(0.25);
}
Console.WriteLine($"Nave en {nave.Pos}");

record struct Vector2(double X, double Y)
{
    public static Vector2 operator +(Vector2 a, Vector2 b) => new(a.X + b.X, a.Y + b.Y);
    public static Vector2 operator *(Vector2 v, double k) => new(v.X * k, v.Y * k);
    public override string ToString() => $"({X}, {Y})";
}

abstract class Componente
{
    public abstract void Update(Entidad e, double dt);
}

class Movimiento : Componente
{
    public Vector2 Velocidad { get; set; }
    public Movimiento(Vector2 velocidad) { Velocidad = velocidad; }
    public override void Update(Entidad e, double dt)
    {
    }
}

class Entidad
{
    private readonly List<Componente> componentes = new();
    public Vector2 Pos { get; set; }
    public Entidad(Vector2 pos) { Pos = pos; }
    public void Agregar(Componente c) => componentes.Add(c);
    public void Update(double dt)
    {
        foreach (Componente c in componentes)
        {
            c.Update(this, dt);
        }
    }
}
```

#### Salida esperada
```
Nave en (4, 0)
```

#### Solución
```csharp
var nave = new Entidad(new Vector2(0, 0));
nave.Agregar(new Movimiento(new Vector2(4, 0)));
for (int cuadro = 1; cuadro <= 4; cuadro++)
{
    nave.Update(0.25);
}
Console.WriteLine($"Nave en {nave.Pos}");

record struct Vector2(double X, double Y)
{
    public static Vector2 operator +(Vector2 a, Vector2 b) => new(a.X + b.X, a.Y + b.Y);
    public static Vector2 operator *(Vector2 v, double k) => new(v.X * k, v.Y * k);
    public override string ToString() => $"({X}, {Y})";
}

abstract class Componente
{
    public abstract void Update(Entidad e, double dt);
}

class Movimiento : Componente
{
    public Vector2 Velocidad { get; set; }
    public Movimiento(Vector2 velocidad) { Velocidad = velocidad; }
    public override void Update(Entidad e, double dt)
    {
        e.Pos = e.Pos + Velocidad * dt;
    }
}

class Entidad
{
    private readonly List<Componente> componentes = new();
    public Vector2 Pos { get; set; }
    public Entidad(Vector2 pos) { Pos = pos; }
    public void Agregar(Componente c) => componentes.Add(c);
    public void Update(double dt)
    {
        foreach (Componente c in componentes)
        {
            c.Update(this, dt);
        }
    }
}
```

#### Al superarla
La nave arranca. Bemol le agrega la misma pieza a un meteoro, con otra velocidad, y también se mueve. —¡Sin copiar nada!

#### Imagen
- Una mesa de taller con piezas de arcade sueltas, engranajes y una nave de juguete con una pieza encastrada que brilla, sin letras.
- Bemol, MUY GORDITO con panza, encastra una pieza en un meteoro de juguete; Ceci sostiene la nave.

### Micro-misión S04-N03-P2 · Buscar la pieza

```meta
lugar: El taller de Bemol
personajes: Bemol, Ceci, Gheco
carta: Get<T> | componentes.OfType<T>().FirstOrDefault() · como GetComponent<T>() de Unity · null si no la tiene
recompensa: xp 15, oro 15
```

#### Escena
Bemol quiere mostrar en el marcador la velocidad de la nave. Para eso tiene que encontrar su pieza `Movimiento`, pero el método `Get` siempre contesta que no hay ninguna.

#### Gheco sugiere
`OfType<T>()` deja solo los elementos de ese tipo, y `FirstOrDefault()` toma el primero, o `null` si no hay:

```csharp
var cuerdas = instrumentos.OfType<Violin>().FirstOrDefault();
```

#### Desafío
Cambiá el cuerpo de `Get<T>` por `componentes.OfType<T>().FirstOrDefault()`.

#### Pasos
1. Cambiá `=> null;` por `=> componentes.OfType<T>().FirstOrDefault();`.
2. Tocá **Ejecutar**. Tiene que salir `Velocidad: (4, 0)`.

#### Código inicial
```csharp
var nave = new Entidad();
nave.Agregar(new Movimiento(new Vector2(4, 0)));

Movimiento? m = nave.Get<Movimiento>();
Console.WriteLine(m is null ? "Sin movimiento" : $"Velocidad: {m.Velocidad}");

record struct Vector2(double X, double Y)
{
    public override string ToString() => $"({X}, {Y})";
}

abstract class Componente { }

class Movimiento : Componente
{
    public Vector2 Velocidad { get; set; }
    public Movimiento(Vector2 velocidad) { Velocidad = velocidad; }
}

class Entidad
{
    private readonly List<Componente> componentes = new();
    public void Agregar(Componente c) => componentes.Add(c);
    public T? Get<T>() where T : Componente => null;
}
```

#### Salida esperada
```
Velocidad: (4, 0)
```

#### Solución
```csharp
var nave = new Entidad();
nave.Agregar(new Movimiento(new Vector2(4, 0)));

Movimiento? m = nave.Get<Movimiento>();
Console.WriteLine(m is null ? "Sin movimiento" : $"Velocidad: {m.Velocidad}");

record struct Vector2(double X, double Y)
{
    public override string ToString() => $"({X}, {Y})";
}

abstract class Componente { }

class Movimiento : Componente
{
    public Vector2 Velocidad { get; set; }
    public Movimiento(Vector2 velocidad) { Velocidad = velocidad; }
}

class Entidad
{
    private readonly List<Componente> componentes = new();
    public void Agregar(Componente c) => componentes.Add(c);
    public T? Get<T>() where T : Componente => componentes.OfType<T>().FirstOrDefault();
}
```

#### Al superarla
El marcador muestra la velocidad. Bemol lee en voz alta, con voz de locutor: —¡Cuatro casillas por segundo!

#### Imagen
- La pantallita con marco dorado de cartón al costado del arcade, encendida, sin letras ni números.
- Bemol habla con un micrófono de juguete; Gheco, MINÚSCULO, sentado sobre la pantallita, sostiene una lupa; Ceci se ríe.

### Micro-misión S04-N03-P3 · Cajas que se tocan

```meta
lugar: El taller de Bemol
personajes: Bemol, Clave
carta: AABB | se pisan a lo ancho Y a lo alto · a.X < b.X + 1 && a.X + 1 > b.X && a.Y < b.Y + 1 && a.Y + 1 > b.Y
recompensa: xp 15, oro 15
```

#### Escena
En el juego de Bemol, la nave explota aunque el meteoro pase dos filas más arriba. El programa solo mira si están en la misma columna.

#### Gheco sugiere
Dos cajas se tocan si se pisan a lo ancho **y** a lo alto. La parte de lo alto es igual, cambiando `X` por `Y`:

```csharp
bool mismaHora = a.Inicio < b.Fin && a.Fin > b.Inicio;   // dos turnos que se pisan
```

#### Desafío
Agregale a `Chocan` la parte de lo alto: `&& a.Y < b.Y + 1 && a.Y + 1 > b.Y`.

#### Pasos
1. Al final de `Chocan`, antes del `;`, agregá `&& a.Y < b.Y + 1 && a.Y + 1 > b.Y`.
2. Tocá **Ejecutar**. Tiene que salir `¿Chocan? False`.

#### Código inicial
```csharp
Vector2 nave = new(3, 0);
Vector2 meteoro = new(3, 2);
Console.WriteLine($"¿Chocan? {Chocan(nave, meteoro)}");

bool Chocan(Vector2 a, Vector2 b) =>
    a.X < b.X + 1 && a.X + 1 > b.X;

record struct Vector2(double X, double Y);
```

#### Salida esperada
```
¿Chocan? False
```

#### Solución
```csharp
Vector2 nave = new(3, 0);
Vector2 meteoro = new(3, 2);
Console.WriteLine($"¿Chocan? {Chocan(nave, meteoro)}");

bool Chocan(Vector2 a, Vector2 b) =>
    a.X < b.X + 1 && a.X + 1 > b.X &&
    a.Y < b.Y + 1 && a.Y + 1 > b.Y;

record struct Vector2(double X, double Y);
```

#### Al superarla
El meteoro pasa por arriba, sin tocarla. Clave, que estaba probando el juego con cara seria, esquiva el siguiente sin querer, y sonríe.

#### Imagen
- La grilla del arcade con una lucecita abajo y otra dos filas más arriba en la misma columna, sin letras.
- Clave, con su capa y la mecha blanca en el rodete, juega en la máquina con cara concentrada; Bemol mira por encima de su hombro.

### Micro-misión S04-N03-P4 · La señal del choque

```meta
lugar: El taller de Bemol
personajes: Bemol, Ceci, Gheco
carta: Señal | nave.AlChocar += nombre => Console.WriteLine(...); · += suscribe · la nave avisa sin saber a quién
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
La nave choca con el meteoro y avisa con su señal `AlChocar`, pero no pasa nada: nadie está escuchando. Bemol quería que la pantalla mostrara el choque.

#### Gheco sugiere
Para enterarse de una señal, hay que **suscribirse** con `+=`, dándole lo que tiene que hacer:

```csharp
batuta.AlBajar += () => Console.WriteLine("¡Empieza!");
```

#### Desafío
Antes de `nave.Chocar(meteoro);`, suscribite: `nave.AlChocar += nombre => Console.WriteLine($"¡{nombre} chocó con la nave!");`.

#### Pasos
1. Arriba de `nave.Chocar(meteoro);`, escribí `nave.AlChocar += nombre => Console.WriteLine($"¡{nombre} chocó con la nave!");`.
2. Tocá **Ejecutar** y compará.

#### Código inicial
```csharp
var nave = new Entidad("Nave");
var meteoro = new Entidad("Meteoro");

nave.Chocar(meteoro);

class Entidad
{
    public string Nombre { get; }
    public event Action<string>? AlChocar;
    public Entidad(string nombre) { Nombre = nombre; }
    public void Chocar(Entidad otra) => AlChocar?.Invoke(otra.Nombre);
}
```

#### Salida esperada
```
¡Meteoro chocó con la nave!
```

#### Solución
```csharp
var nave = new Entidad("Nave");
var meteoro = new Entidad("Meteoro");

nave.AlChocar += nombre => Console.WriteLine($"¡{nombre} chocó con la nave!");
nave.Chocar(meteoro);

class Entidad
{
    public string Nombre { get; }
    public event Action<string>? AlChocar;
    public Entidad(string nombre) { Nombre = nombre; }
    public void Chocar(Entidad otra) => AlChocar?.Invoke(otra.Nombre);
}
```

#### Al superarla
La pantalla parpadea en rojo. Bemol suscribe otra cosa a la misma señal: un ruido de explosión que hace él con la boca. Ceci le pide que lo saque.

#### Imagen
- La pantalla del arcade parpadeando en rojo con una explosión de lucecitas, sin letras.
- Bemol hace un ruido de explosión con las manos en la boca; Ceci se tapa los oídos riendo; Gheco, MINÚSCULO, flota con los pelos de punta.

### Micro-misión S04-N03-P5 · El troll de la señal sin nadie

```meta
lugar: El taller de Bemol
personajes: Bemol, Gheco
criatura: troll
carta: Troll | sin suscriptos, el evento vale null · AlChocar(nombre) se rompe · AlChocar?.Invoke(nombre) no
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un troll escribió la señal de los meteoros llamándola directo: `AlChocar(otra.Nombre)`. Funciona mientras alguien escucha. Pero los meteoros chocan entre ellos sin que nadie se suscriba, y el juego se rompe.

#### Gheco sugiere
Un evento sin nadie suscripto vale `null`. Llamarlo directo rompe el programa. `?.Invoke` lo llama **solo si** hay alguien:

```csharp
AlTerminar?.Invoke();   // si nadie escucha, no pasa nada
```

#### Desafío
En `Chocar`, cambiá `AlChocar(otra.Nombre)` por `AlChocar?.Invoke(otra.Nombre)`.

#### Pasos
1. Cambiá `AlChocar(otra.Nombre)` por `AlChocar?.Invoke(otra.Nombre)`.
2. Tocá **Ejecutar** y compará.

#### Código inicial
```csharp
var uno = new Entidad("Meteoro chico");
var otro = new Entidad("Meteoro grande");

uno.Chocar(otro);
Console.WriteLine("Sin nadie escuchando, el juego sigue");

class Entidad
{
    public string Nombre { get; }
    public event Action<string>? AlChocar;
    public Entidad(string nombre) { Nombre = nombre; }
    public void Chocar(Entidad otra) => AlChocar(otra.Nombre);
}
```

#### Salida esperada
```
Sin nadie escuchando, el juego sigue
```

#### Solución
```csharp
var uno = new Entidad("Meteoro chico");
var otro = new Entidad("Meteoro grande");

uno.Chocar(otro);
Console.WriteLine("Sin nadie escuchando, el juego sigue");

class Entidad
{
    public string Nombre { get; }
    public event Action<string>? AlChocar;
    public Entidad(string nombre) { Nombre = nombre; }
    public void Chocar(Entidad otra) => AlChocar?.Invoke(otra.Nombre);
}
```

#### Al superarla
Los meteoros chocan entre ellos y siguen de largo, sin romper nada. El troll se sienta arriba de la máquina a mirar cómo pasan, hipnotizado.

#### Imagen
- La pantalla del arcade con dos lucecitas que se cruzan y siguen de largo, sin letras.
- Un troll gris chiquito sentado arriba de la máquina de arcade, mirando la pantalla con la boca abierta; Gheco, MINÚSCULO, le ofrece pochoclos; Bemol, al lado.

## S04-N04 · Jefe: el Glitch del Arcade

```meta
tipo: jefe
padre: S04-N03
precio: 10
criatura: dragon
insignia: Creadora del Arcade
insignia_descripcion: Venciste al Glitch del Arcade: tu juego tiene bucle con delta time, Vector2, componentes, colisiones y señales, una pantalla en dos dimensiones, azar con semilla, vidas y fin del juego.
temas: juegos.estados, juegos.ia
usa: juegos.bucle, juegos.colisiones, poo.composicion, prog.matematica-azar
```

### Crónica

La noche antes de llevar el arcade a la Feria, la máquina se enciende sola. En la pantalla aparece una figura que no dibujó nadie: un **sprite roto**, de colores que no existen, que salta de un lugar a otro sin pasar por el medio. Es **el Glitch del Arcade**. Donde aterriza, las lucecitas se queman, los puntos se cuentan tres veces y las vidas no se terminan nunca.

—¡Mañana viene toda la Feria! —se desespera Bemol.

Ceci se arremanga. —Entonces lo atrapamos. Con todo lo que armaste.

### Objetivos

- Dibujar una pantalla en dos dimensiones con un `char[,]` (fila y columna).
- Hacer que el Glitch salte con azar, pero con **semilla**, para que el juego se pueda repetir.
- Suscribirse a una señal **una sola vez**.
- Contar las vidas y terminar el juego en el momento justo.
- Que el juego vaya igual con más o menos cuadros por segundo.

### Antes de empezar

- Toda la Senda del Arcade (S04-N01 a N03) y el azar con semilla de la Arena (R06-N02).

### Explicación

#### La pantalla en dos dimensiones

Una matriz `char[,]` es la pantalla: el primer número es la **fila** (lo alto, `Y`) y el segundo, la **columna** (lo ancho, `X`).

```csharp
char[,] pantalla = new char[3, 8];          // 3 filas, 8 columnas
pantalla[(int)pos.Y, (int)pos.X] = '@';     // primero Y, después X
```

Es el error más común de los juegos en grilla: poner `X` primero.

#### Azar que se repite

`new Random(7)` da siempre los mismos números, en el mismo orden. Para un juego de verdad se usa `new Random()`, pero para probarlo, y para que un error se pueda repetir, la semilla fija es oro.

#### Suscribirse una vez

Cada `+=` agrega **otro** suscriptor. Si se suscribe adentro del bucle, en el cuadro 10 hay diez, y un choque cuenta diez veces. Se suscribe **una vez**, antes del bucle (en Godot: conectar la señal en `_ready`, no en `_process`).

#### El fin del juego

Un juego también es una máquina de estados: jugando, ganaste, perdiste. Cuando las vidas llegan a **cero**, se corta el bucle con `break`.

### Código de ejemplo

```csharp
char[,] pantalla = new char[3, 8];
Random azar = new Random(7);
int vidas = 2;

for (int cuadro = 1; cuadro <= 3 && vidas > 0; cuadro++)
{
    for (int f = 0; f < 3; f++)
        for (int c = 0; c < 8; c++)
            pantalla[f, c] = '.';

    Vector2 nave = new(3, 1);
    Vector2 glitch = new(azar.Next(8), azar.Next(3));
    pantalla[(int)nave.Y, (int)nave.X] = '@';
    pantalla[(int)glitch.Y, (int)glitch.X] = 'G';
    if (nave == glitch) vidas--;

    Console.WriteLine($"Cuadro {cuadro} (vidas: {vidas})");
    for (int f = 0; f < 3; f++)
    {
        for (int c = 0; c < 8; c++) Console.Write(pantalla[f, c]);
        Console.WriteLine();
    }
}

record struct Vector2(double X, double Y);
```

### Salida esperada

```
Cuadro 1 (vidas: 2)
........
...@....
...G....
Cuadro 2 (vidas: 2)
.....G..
...@....
........
Cuadro 3 (vidas: 2)
........
...@....
..G.....
```

### ¿Para qué sirve?

Con esto ya tenés todas las piezas de un juego 2D de verdad: la pantalla en grilla de los juegos de baldosas, el azar con semilla de los juegos que generan mapas, las señales bien conectadas y un bucle que no depende de la compu. Es lo mismo que vas a encontrar en Unity y en Godot, con dibujos en vez de letras.

### Errores habituales

- **`pantalla[x, y]` en vez de `[y, x]`:** la fila va primero.
- **Suscribirse adentro del bucle:** cada cuadro suma otro suscriptor.
- **Terminar el juego con `vidas < 0`:** se juega un cuadro con cero vidas.
- **Mover por cuadro y no por tiempo:** con más cuadros por segundo, el Glitch va más rápido.

### Micro-misión S04-N04-P1 · Fila primero

```meta
lugar: La Feria de las Luces
personajes: Bemol, Ceci, Gheco
criatura: dragon
carta: Jefe | pantalla[fila, columna] · pantalla[(int)p.Y, (int)p.X] · la Y va primero
recompensa: xp 25, oro 25
```

#### Escena
El Glitch dio vuelta la pantalla: ahora el programa pone la `X` donde va la `Y`, y en cuanto la nave pasa la tercera columna, el programa se rompe.

#### Gheco sugiere
En una matriz, el primer número es la **fila** y el segundo la **columna**. La fila es lo alto (`Y`); la columna, lo ancho (`X`):

```csharp
char[,] tablero = new char[8, 8];
tablero[fila, columna] = 'R';
```

#### Desafío
En `Poner`, cambiá `pantalla[(int)p.X, (int)p.Y]` por `pantalla[(int)p.Y, (int)p.X]`.

#### Pasos
1. Cambiá `pantalla[(int)p.X, (int)p.Y]` por `pantalla[(int)p.Y, (int)p.X]`.
2. Tocá **Ejecutar** y compará la pantalla.

#### Código inicial
```csharp
char[,] pantalla = new char[3, 8];
for (int f = 0; f < 3; f++)
    for (int c = 0; c < 8; c++)
        pantalla[f, c] = '.';

Poner(new Vector2(5, 1), '@');
Poner(new Vector2(2, 0), 'G');

for (int f = 0; f < 3; f++)
{
    for (int c = 0; c < 8; c++) Console.Write(pantalla[f, c]);
    Console.WriteLine();
}

void Poner(Vector2 p, char letra) => pantalla[(int)p.X, (int)p.Y] = letra;

record struct Vector2(double X, double Y);
```

#### Salida esperada
```
..G.....
.....@..
........
```

#### Solución
```csharp
char[,] pantalla = new char[3, 8];
for (int f = 0; f < 3; f++)
    for (int c = 0; c < 8; c++)
        pantalla[f, c] = '.';

Poner(new Vector2(5, 1), '@');
Poner(new Vector2(2, 0), 'G');

for (int f = 0; f < 3; f++)
{
    for (int c = 0; c < 8; c++) Console.Write(pantalla[f, c]);
    Console.WriteLine();
}

void Poner(Vector2 p, char letra) => pantalla[(int)p.Y, (int)p.X] = letra;

record struct Vector2(double X, double Y);
```

#### Al superarla
La pantalla se endereza. Ahí está la nave, y ahí, en la primera fila, el Glitch: un manchón de colores raros que tiembla. Por primera vez, se lo ve quieto.

#### Imagen
- Una máquina de arcade de madera en un puesto de la Feria de las Luces de noche, con farolitos, con la pantalla de grilla encendida, sin letras.
- En la pantalla, un sprite roto de colores imposibles y bordes pixelados que tiembla; Bemol, MUY GORDITO con panza, y Ceci miran la pantalla; Gheco, MINÚSCULO, en el hombro de Ceci.

### Micro-misión S04-N04-P2 · El salto con semilla

```meta
lugar: La Feria de las Luces
personajes: Bemol, Ceci
criatura: dragon
carta: Jefe | new Random(7) · siempre los mismos saltos, en el mismo orden · así el error se puede repetir
recompensa: xp 25, oro 25
```

#### Escena
El Glitch salta a un lugar distinto cada vez que prueban, y Ceci no puede estudiar cómo se mueve. Necesita que salte **siempre igual** mientras lo investiga.

#### Gheco sugiere
Un `Random` con semilla da siempre la misma lista de números:

```csharp
Random dado = new Random(3);
Console.WriteLine(dado.Next(1, 7));   // siempre el mismo
```

#### Desafío
Cambiá `new Random()` por `new Random(7)`.

#### Pasos
1. Cambiá `new Random()` por `new Random(7)`.
2. Tocá **Ejecutar**. El Glitch tiene que aparecer siempre en los mismos lugares.

#### Código inicial
```csharp
Random azar = new Random();
for (int cuadro = 1; cuadro <= 3; cuadro++)
{
    Vector2 glitch = new(azar.Next(8), azar.Next(3));
    Console.WriteLine($"Cuadro {cuadro}: el Glitch aparece en {glitch}");
}

record struct Vector2(double X, double Y)
{
    public override string ToString() => $"({X}, {Y})";
}
```

#### Salida esperada
```
Cuadro 1: el Glitch aparece en (3, 2)
Cuadro 2: el Glitch aparece en (5, 0)
Cuadro 3: el Glitch aparece en (2, 2)
```

#### Solución
```csharp
Random azar = new Random(7);
for (int cuadro = 1; cuadro <= 3; cuadro++)
{
    Vector2 glitch = new(azar.Next(8), azar.Next(3));
    Console.WriteLine($"Cuadro {cuadro}: el Glitch aparece en {glitch}");
}

record struct Vector2(double X, double Y)
{
    public override string ToString() => $"({X}, {Y})";
}
```

#### Al superarla
Ceci corre el programa diez veces y el Glitch salta diez veces igual. Anota los tres lugares en su cuaderno. El Glitch, en la pantalla, parece ponerse nervioso.

#### Imagen
- La pantalla del arcade con tres marcas de luz donde aterrizó el sprite roto, unidas por líneas punteadas, sin letras ni números.
- Ceci anota en su cuaderno; Bemol señala la pantalla; el sprite roto tiembla, nervioso.

### Micro-misión S04-N04-P3 · Una sola vez

```meta
lugar: La Feria de las Luces
personajes: Bemol, Ceci, Gheco
criatura: dragon
carta: Jefe | += afuera del bucle · adentro, cada cuadro suma otro suscriptor · un choque cuenta muchas veces
recompensa: xp 25, oro 25
```

#### Escena
Ceci atrapa al Glitch una vez y el marcador suma tres puntos. El Glitch se ríe con un chirrido: alguien escribió la suscripción adentro del bucle, y en cada cuadro se suma otro que cuenta.

#### Gheco sugiere
Cada `+=` agrega un suscriptor **más**. Se suscribe una sola vez, **antes** del bucle:

```csharp
batuta.AlBajar += Aplaudir;        // una vez
foreach (var compas in obra) { }   // y después, el bucle
```

#### Desafío
Sacá la línea `jugador.Atrapo += () => puntos++;` de adentro del `for` y ponela antes.

#### Pasos
1. Borrá `jugador.Atrapo += () => puntos++;` de adentro del `for`.
2. Escribilo arriba del `for`.
3. Tocá **Ejecutar**. Tiene que salir `Puntos: 1`.

#### Código inicial
```csharp
int puntos = 0;
var jugador = new Jugador();
Vector2[] glitch = [new(1, 0), new(4, 0), new(2, 0)];

for (int cuadro = 0; cuadro < 3; cuadro++)
{
    jugador.Atrapo += () => puntos++;
    if (jugador.Pos == glitch[cuadro])
    {
        jugador.Atrapar();
    }
}
Console.WriteLine($"Puntos: {puntos}");

record struct Vector2(double X, double Y);

class Jugador
{
    public Vector2 Pos { get; set; } = new(2, 0);
    public event Action? Atrapo;
    public void Atrapar() => Atrapo?.Invoke();
}
```

#### Salida esperada
```
Puntos: 1
```

#### Solución
```csharp
int puntos = 0;
var jugador = new Jugador();
Vector2[] glitch = [new(1, 0), new(4, 0), new(2, 0)];

jugador.Atrapo += () => puntos++;
for (int cuadro = 0; cuadro < 3; cuadro++)
{
    if (jugador.Pos == glitch[cuadro])
    {
        jugador.Atrapar();
    }
}
Console.WriteLine($"Puntos: {puntos}");

record struct Vector2(double X, double Y);

class Jugador
{
    public Vector2 Pos { get; set; } = new(2, 0);
    public event Action? Atrapo;
    public void Atrapar() => Atrapo?.Invoke();
}
```

#### Al superarla
Un punto por atrapada, como tiene que ser. El Glitch pierde un pedazo de colores raros, que cae al piso de la pantalla y se apaga.

#### Imagen
- La pantalla del arcade con un marcador de puntos de lucecitas, sin números, y un pedazo del sprite roto que cae y se apaga, sin letras.
- Ceci festeja con el puño; Gheco, MINÚSCULO, sentado en el marcador; Bemol abraza la máquina.

### Micro-misión S04-N04-P4 · Las vidas que no se terminan

```meta
lugar: La Feria de las Luces
personajes: Bemol, Ceci, Clave
criatura: dragon
carta: Jefe | el juego termina cuando las vidas llegan a 0 · vidas <= 0, no vidas < 0 · break corta el bucle
recompensa: xp 25, oro 25, monedas 3
```

#### Escena
El Glitch tocó la regla del fin del juego: ahora la partida sigue con cero vidas, y la nave juega un cuadro más como un fantasma. Clave dice que un concierto termina en la última nota, no en la siguiente.

#### Gheco sugiere
Si el juego termina «cuando no quedan vidas», la condición es `<= 0`: con cero, ya no queda ninguna.

```csharp
if (energia <= 0)
{
    Console.WriteLine("Sin energía");
    break;
}
```

#### Desafío
Cambiá `vidas < 0` por `vidas <= 0`.

#### Pasos
1. Cambiá `vidas < 0` por `vidas <= 0`.
2. Tocá **Ejecutar**. Tiene que salir `Fin del juego`.

#### Código inicial
```csharp
int vidas = 3;
int[] golpes = [1, 1, 0, 1, 1];

for (int cuadro = 0; cuadro < golpes.Length; cuadro++)
{
    vidas -= golpes[cuadro];
    Console.WriteLine($"Cuadro {cuadro + 1}: {vidas} vidas");
    if (vidas < 0)
    {
        Console.WriteLine("Fin del juego");
        break;
    }
}
```

#### Salida esperada
```
Cuadro 1: 2 vidas
Cuadro 2: 1 vidas
Cuadro 3: 1 vidas
Cuadro 4: 0 vidas
Fin del juego
```

#### Solución
```csharp
int vidas = 3;
int[] golpes = [1, 1, 0, 1, 1];

for (int cuadro = 0; cuadro < golpes.Length; cuadro++)
{
    vidas -= golpes[cuadro];
    Console.WriteLine($"Cuadro {cuadro + 1}: {vidas} vidas");
    if (vidas <= 0)
    {
        Console.WriteLine("Fin del juego");
        break;
    }
}
```

#### Al superarla
La partida termina justo en la última vida. Clave asiente: —La última nota. Ni una más. El Glitch se encoge un poco más.

#### Imagen
- La pantalla del arcade con tres corazones de lucecitas, todos apagados, sin letras ni números.
- Clave, con su capa y la mecha blanca en el rodete, juega con cara seria; Ceci y Bemol miran detrás.

### Micro-misión S04-N04-P5 · Igual en cualquier máquina

```meta
lugar: La Feria de las Luces
personajes: Bemol, Ceci, Clave, Gheco
criatura: dragon
carta: Jefe | x += velocidad * dt · dt = 1.0 / cuadrosPorSegundo · el mismo segundo de juego en cualquier compu
recompensa: xp 30, oro 30, monedas 3
```

#### Escena
Su último truco: el Glitch se esconde en la velocidad. En la máquina rápida de la Feria, que dibuja el doble de cuadros, todo se mueve el doble de rápido, y el Glitch se escapa siempre. Alguien sumó la velocidad por cuadro, sin el `dt`.

#### Gheco sugiere
Si cada cuadro dura `1.0 / cuadrosPorSegundo`, y se mueve `velocidad * dt`, en un segundo se recorre lo mismo con 2 cuadros que con 4:

```csharp
double dt = 1.0 / 60;            // 60 cuadros por segundo
posicion += rapidez * dt;
```

#### Desafío
En `Simular`, cambiá `x += velocidad;` por `x += velocidad * dt;`.

#### Pasos
1. En `Simular`, cambiá `x += velocidad;` por `x += velocidad * dt;`.
2. Tocá **Ejecutar**. Los dos tienen que dar 4.

#### Código inicial
```csharp
Console.WriteLine($"A 2 cuadros por segundo: {Simular(2)}");
Console.WriteLine($"A 4 cuadros por segundo: {Simular(4)}");

double Simular(int cuadrosPorSegundo)
{
    double x = 0;
    double velocidad = 4;
    double dt = 1.0 / cuadrosPorSegundo;
    for (int i = 0; i < cuadrosPorSegundo; i++)
    {
        x += velocidad;
    }
    return x;
}
```

#### Salida esperada
```
A 2 cuadros por segundo: 4
A 4 cuadros por segundo: 4
```

#### Solución
```csharp
Console.WriteLine($"A 2 cuadros por segundo: {Simular(2)}");
Console.WriteLine($"A 4 cuadros por segundo: {Simular(4)}");

double Simular(int cuadrosPorSegundo)
{
    double x = 0;
    double velocidad = 4;
    double dt = 1.0 / cuadrosPorSegundo;
    for (int i = 0; i < cuadrosPorSegundo; i++)
    {
        x += velocidad * dt;
    }
    return x;
}
```

#### Al superarla
En las dos máquinas, el mismo segundo, el mismo lugar. El Glitch no tiene dónde esconderse. Ceci lo atrapa en el medio de la pantalla y, en vez de explotar, el sprite roto se ordena: los colores imposibles se vuelven cuatro colores de verdad, los bordes se alisan, y queda una figurita simpática que saluda con la mano. Bemol la deja en el juego, de mascota. Al otro día, la Feria entera hace fila para jugar. Clave, que dijo que no iba a venir, juega tres partidas seguidas.

#### Imagen
- El puesto del arcade en la Feria de las Luces de día, con una fila larga de gente de la Feria esperando, farolitos y banderines, sin letras.
- En la pantalla, una figurita pixelada simpática de cuatro colores que saluda; Bemol, MUY GORDITO con panza, atiende orgulloso; Clave, con su capa y la mecha blanca, juega; Ceci sonríe al lado; Gheco, MINÚSCULO, en el hombro de Ceci.
