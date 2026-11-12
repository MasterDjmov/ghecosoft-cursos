# RAMA R05 · La Bóveda y la ventanilla: el mundo real

```meta
tipo: tronco
posicion: 5
```

## R05-N01 · async y await: esperar sin trabar

```meta
tipo: tema
padre: R04-N07
precio: 10
criatura: ogro
temas: conc.async
usa: prog.funciones
```

### Crónica

Con el Archivo despierto, el Conservatorio abre una **Ventanilla de Pedidos**: Nilo trae cartas del Puerto, Nima manda flechas de luz desde la Feria, y todos quieren partituras. Bemol atiende el primer día. Pide una partitura al depósito y se queda parado, mirando la puerta, hasta que llega. Detrás de él, la fila da vuelta la manzana.

—Así atiende un programa que espera **trabado** —dice {mentor}—. Pedí, y mientras llega, seguí con lo tuyo. Cuando esté, te avisan.

En la ventanilla suena una campanilla, aunque nadie la tocó.

### Objetivos

- Entender qué es una **tarea** (`Task`): un trabajo que termina más tarde.
- Esperarla sin trabar el programa con `await`.
- Escribir métodos que esperan, con `async Task` y `async Task<T>`.
- Saber cuándo esperar enseguida y cuándo arrancar algo y esperarlo después.

### Antes de empezar

- Métodos (R01-N13) y excepciones (R04-N01).

### Explicación

#### Lo que tarda

Muchas cosas **tardan**: traer algo por la red, leer un archivo grande, preguntarle a una base de datos. Si el programa se queda quieto esperando, no puede hacer nada más; en una aplicación con ventanas, la ventana se congela.

En este acto, lo que tarda lo simulamos con `Task.Delay(200)`: una espera de 200 milisegundos (un quinto de segundo).

#### `await`: esperá, pero sin trabar

```csharp
Console.WriteLine("Pido la partitura");
await Task.Delay(200);
Console.WriteLine("Llegó");
```

`await` quiere decir: **esperá a que esto termine, y mientras tanto dejá que el resto siga**. Cuando termina, el programa sigue en la línea de abajo.

#### Métodos que esperan: `async Task`

Un método que usa `await` adentro se marca con `async`, y en vez de `void` devuelve `Task` (una **tarea**: un trabajo que termina más tarde):

```csharp
async Task AfinarAsync()
{
    await Task.Delay(200);
    Console.WriteLine("Afinado");
}

await AfinarAsync();
```

Si al terminar tiene que **devolver** algo, devuelve `Task<T>`, y adentro se escribe `return` como siempre:

```csharp
async Task<int> ContarCuerdasAsync()
{
    await Task.Delay(200);
    return 4;
}

int cuerdas = await ContarCuerdasAsync();
```

`ContarCuerdasAsync()` devuelve un `Task<int>`: algo así como un **recibo** que promete un `int`. El `await` cambia el recibo por el número cuando llega. Por costumbre, esos métodos terminan en `Async`.

#### Arrancar ahora, esperar después

Llamar a un método `async` **sin** `await` lo arranca y sigue de largo. Se guarda la tarea y se la espera más tarde:

```csharp
Task afinar = AfinarAsync();          // arranca
Console.WriteLine("Mientras, leo");   // esto pasa mientras espera
await afinar;                         // y acá sí, espero a que termine
```

#### Un error adentro de una tarea

Si algo falla adentro de un método `async`, el error salta **en el `await`**. Por eso el `try` va alrededor del `await`.

### Código de ejemplo

```csharp
async Task<string> PedirPartituraAsync(string obra)
{
    Console.WriteLine($"Pido {obra}");
    await Task.Delay(200);
    return $"{obra} (8 páginas)";
}

Task<string> pedido = PedirPartituraAsync("Canon");
Console.WriteLine("Mientras, atiendo al siguiente");
string partitura = await pedido;
Console.WriteLine($"Llegó: {partitura}");
```

### Salida esperada

```
Pido Canon
Mientras, atiendo al siguiente
Llegó: Canon (8 páginas)
```

### ¿Para qué sirve?

Todo lo que habla con el mundo de afuera (internet, archivos, bases de datos) en C# se hace con `async` y `await`. Un juego sigue dibujando mientras carga un nivel; una app sigue respondiendo mientras baja una foto.

### Errores habituales

- **Olvidar el `await`:** `string p = PedirPartituraAsync("Canon");` no compila (CS0029): lo que devuelve es el recibo (`Task<string>`), no la partitura.
- **`await` en un método sin `async`:** CS4032. Si adentro hay un `await`, el método lleva `async` y devuelve `Task` o `Task<T>`.
- **`Thread.Sleep` en vez de `Task.Delay`:** `Thread.Sleep` traba todo el programa mientras espera. En el navegador, ni siquiera anda.

### Micro-misión R05-N01-P1 · El recibo de la partitura

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Bemol
carta: await | Metodo() devuelve un Task<string> · un recibo · await lo cambia por lo que promete
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Bemol pide el Bolero al depósito y quiere guardar la partitura en una variable, pero el ensayo general no lo deja pasar.

#### Gheco sugiere
`PedirAsync("Bolero")` no devuelve la partitura: devuelve un `Task<string>`, un **recibo** que promete un texto para más tarde. Para cambiar el recibo por el texto se escribe `await` adelante:

```csharp
int cuerdas = await ContarCuerdasAsync();
```

Sin el `await`, C# protesta con `CS0029`: no se puede guardar un recibo en una variable de texto.

#### Desafío
Agregá `await` donde se pide la partitura.

#### Código inicial
```csharp
async Task<string> PedirAsync(string obra)
{
    await Task.Delay(200);
    return $"{obra}, para orquesta";
}

string partitura = PedirAsync("Bolero");
Console.WriteLine($"Llegó: {partitura}");
```

#### Salida esperada
```
Llegó: Bolero, para orquesta
```

#### Solución
```csharp
async Task<string> PedirAsync(string obra)
{
    await Task.Delay(200);
    return $"{obra}, para orquesta";
}

string partitura = await PedirAsync("Bolero");
Console.WriteLine($"Llegó: {partitura}");
```

#### Al superarla
—Ah, era un recibo —dice Bemol, y lo da vuelta como si atrás hubiera algo escrito.

#### Imagen
- La ventanilla de madera de un conservatorio gótico, con una campanilla de bronce y un papelito de recibo liso en el mostrador, sin letras.
- Bemol mira el recibo con cara de confundido; Ceci, al lado, le señala la puerta del depósito.

### Micro-misión R05-N01-P2 · Un método que espera

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: async Task<T> | si adentro hay await · el método lleva async · y devuelve Task<int>, no int
recompensa: xp 15, oro 15
```

#### Escena
Don Cedro escribió un método que tarda en afinar cada instrumento, pero no compila: le falta decir que espera.

#### Gheco sugiere
Un método que tiene un `await` adentro se marca con `async`, y lo que devuelve se envuelve en un `Task`:

| Sin esperas | Con un `await` adentro |
|---|---|
| `void Hacer()` | `async Task HacerAsync()` |
| `int Contar()` | `async Task<int> ContarAsync()` |

El `return` adentro sigue igual: se devuelve el `int`, y C# lo envuelve solo. Si falta el `async`, aparece el error `CS4032`.

#### Desafío
Cambiá `int AfinarAsync` por `async Task<int> AfinarAsync`.

#### Código inicial
```csharp
int AfinarAsync(int cuerdas)
{
    await Task.Delay(100 * cuerdas);
    return cuerdas * 2;
}

int vueltas = await AfinarAsync(4);
Console.WriteLine($"Vueltas de clavija: {vueltas}");
```

#### Salida esperada
```
Vueltas de clavija: 8
```

#### Solución
```csharp
async Task<int> AfinarAsync(int cuerdas)
{
    await Task.Delay(100 * cuerdas);
    return cuerdas * 2;
}

int vueltas = await AfinarAsync(4);
Console.WriteLine($"Vueltas de clavija: {vueltas}");
```

#### Al superarla
—Ocho vueltas —dice Don Cedro—. Y mientras doy la última, ya estoy pensando en la viola.

#### Imagen
- Un taller de luthier de madera cálida con velas, con un violín sobre la mesa de trabajo y un reloj de arena chico al lado, sin letras.
- Don Cedro gira una clavija del violín; Ceci da vuelta el reloj de arena.

### Micro-misión R05-N01-P3 · Mientras tanto

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Bemol
carta: Arrancar y esperar después | Task t = HacerAsync(); · algo mientras tanto · await t;
recompensa: xp 15, oro 15
```

#### Escena
Bemol pide una partitura y se queda mirando la puerta. Ceci le muestra que, mientras tanto, podría ir anotando al siguiente de la fila.

#### Gheco sugiere
Si llamás al método **sin** `await`, la tarea arranca y el programa sigue de largo. La guardás en una variable de tipo `Task` y la esperás más tarde:

```csharp
Task afinar = AfinarAsync();         // arranca
Console.WriteLine("Mientras, leo");  // mientras tanto
await afinar;                        // ahora sí espero
```

#### Desafío
Guardá la tarea en `Task pedido = PedirAsync("Canon");`, mostrá `Mientras, anoto al siguiente` y recién después hacé `await pedido;`.

#### Código inicial
```csharp
async Task PedirAsync(string obra)
{
    Console.WriteLine($"Pido {obra}");
    await Task.Delay(200);
    Console.WriteLine($"Llegó {obra}");
}

await PedirAsync("Canon");
Console.WriteLine("Mientras, anoto al siguiente");
```

#### Salida esperada
```
Pido Canon
Mientras, anoto al siguiente
Llegó Canon
```

#### Solución
```csharp
async Task PedirAsync(string obra)
{
    Console.WriteLine($"Pido {obra}");
    await Task.Delay(200);
    Console.WriteLine($"Llegó {obra}");
}

Task pedido = PedirAsync("Canon");
Console.WriteLine("Mientras, anoto al siguiente");
await pedido;
```

#### Al superarla
La fila avanza. Por primera vez en el día, alguien de la fila sonríe.

#### Imagen
- La ventanilla de madera de un conservatorio gótico con una fila de gente de espaldas esperando, con faroles, sin letras.
- Bemol anota en una libreta lisa; Ceci le alcanza una partitura enrollada por la ventanilla.

### Micro-misión R05-N01-P4 · El error llega con el await

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Clave
carta: Errores en tareas | el error de adentro · salta en el await · try { await … } catch { … }
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Piden una partitura que no existe, y el depósito contesta con un error. La ventanilla entera se cierra de golpe.

#### Gheco sugiere
Si algo falla adentro de un método `async`, el error queda guardado en la tarea y **salta en el `await`**. Se atrapa como siempre, con el `try` alrededor del `await`:

```csharp
try
{
    await CargarAsync();
}
catch (InvalidOperationException e)
{
    Console.WriteLine(e.Message);
}
```

`e.Message` es el mensaje que se puso al lanzar el error.

#### Desafío
Envolvé el `await` en un `try`, y en un `catch (InvalidOperationException e)` mostrá `No hay: ` seguido de `e.Message`.

#### Código inicial
```csharp
async Task<string> PedirAsync(string obra)
{
    await Task.Delay(100);
    if (obra == "Sinfonía 11")
    {
        throw new InvalidOperationException("esa obra no está en el depósito");
    }
    return obra;
}

string p = await PedirAsync("Sinfonía 11");
Console.WriteLine($"Llegó: {p}");
Console.WriteLine("La ventanilla sigue abierta");
```

#### Salida esperada
```
No hay: esa obra no está en el depósito
La ventanilla sigue abierta
```

#### Solución
```csharp
async Task<string> PedirAsync(string obra)
{
    await Task.Delay(100);
    if (obra == "Sinfonía 11")
    {
        throw new InvalidOperationException("esa obra no está en el depósito");
    }
    return obra;
}

try
{
    string p = await PedirAsync("Sinfonía 11");
    Console.WriteLine($"Llegó: {p}");
}
catch (InvalidOperationException e)
{
    Console.WriteLine($"No hay: {e.Message}");
}
Console.WriteLine("La ventanilla sigue abierta");
```

#### Al superarla
—Una partitura que no existe no es motivo para cerrar —dice Clave—. Es motivo para avisar.

#### Imagen
- La ventanilla de madera de un conservatorio gótico con la persiana a medio bajar y un farol encendido, sin letras.
- Clave sostiene la persiana para que no se cierre; Ceci, del otro lado, asiente.

### Micro-misión R05-N01-P5 · El ogro que abrió antes de tiempo

```meta
lugar: El Escenario Grande
personajes: Ceci, Gheco
criatura: ogro
carta: Ogro | si lo que sigue necesita la tarea terminada · await ANTES de seguir
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un ogro de la Feria ayuda a preparar el escenario. Arranca a acomodar las sillas y, sin esperar, abre la puerta al público. La gente entra y no tiene dónde sentarse.

#### Gheco sugiere
Arrancar una tarea y esperarla después sirve cuando lo de «mientras tanto» **no la necesita**. Si lo que sigue necesita que la tarea haya terminado, el `await` va **antes**:

```csharp
await AfinarAsync();                 // primero termina
Console.WriteLine("Empieza el concierto");
```

El programa corre sin error, pero en otro orden: es un error de **lógica**.

#### Desafío
Hacé que el escenario esté listo antes de abrir la puerta: `await PrepararAsync();` y recién después, `Abro la puerta`.

#### Código inicial
```csharp
async Task PrepararAsync()
{
    await Task.Delay(200);
    Console.WriteLine("Sillas acomodadas");
}

Task preparar = PrepararAsync();
Console.WriteLine("Abro la puerta");
await preparar;
```

#### Salida esperada
```
Sillas acomodadas
Abro la puerta
```

#### Solución
```csharp
async Task PrepararAsync()
{
    await Task.Delay(200);
    Console.WriteLine("Sillas acomodadas");
}

await PrepararAsync();
Console.WriteLine("Abro la puerta");
```

#### Al superarla
El ogro espera con la mano en el picaporte hasta que la última silla está en su lugar. Después abre, orgulloso, como si hubiera sido idea suya.

#### Imagen
- Un escenario gótico con velas y filas de sillas de madera a medio acomodar, con una puerta grande de madera al fondo, sin letras.
- El ogro grandote, con la mano en el picaporte, espera; Gheco, parado solo sobre una silla, le hace señas de que todavía no.

### Encargo R05-N01-E1 · Las cartas del Puerto

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Nilo trae cartas del Puerto, y cada una hay que **sellarla** antes de responder: sellar tarda. Escribí un método `async Task<int> SellarAsync(string carta)` que espere 50 milisegundos con `Task.Delay` y devuelva la cantidad de letras de la carta. Leé cartas, una por línea, hasta una línea vacía; para cada una, esperá a que se selle y mostrá `Sellada: ` con la carta y las letras entre paréntesis. Al final, el total de letras.

Con esta entrada:

```
Hola
Partitura nueva

```

se muestra:

```
Sellada: Hola (4)
Sellada: Partitura nueva (15)
Total: 19
```

#### Criterio de aprobación

- `SellarAsync` es `async Task<int>`, espera con `await Task.Delay(50)` y devuelve la cantidad de letras.
- Cada carta se espera con `await` antes de mostrarla.

#### Entrada de ejemplo

```
Hola
Partitura nueva

```

#### Salida esperada

```
Sellada: Hola (4)
Sellada: Partitura nueva (15)
Total: 19
```

#### Solución de referencia

```csharp
async Task<int> SellarAsync(string carta)
{
    await Task.Delay(50);
    return carta.Length;
}

int total = 0;
string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    int letras = await SellarAsync(linea);
    Console.WriteLine($"Sellada: {linea} ({letras})");
    total += letras;
    linea = Console.ReadLine();
}
Console.WriteLine($"Total: {total}");
```

## R05-N02 · Todas juntas: WhenAll, WhenAny y cancelar

```meta
tipo: tema
padre: R05-N01
precio: 10
criatura: troll
temas: conc.async
usa: prog.funciones, col.arrays
```

### Crónica

La orquesta tiene que afinar antes del concierto: el violín, la viola y el chelo. Bemol los afina de a uno, y cuando termina con el chelo, el público ya se fue.

—¿Y si afinan **los tres a la vez**? —pregunta Ceci.

—Eso —dice {mentor}—. Cada uno espera lo suyo, y vos esperás a que terminen todos. Y si alguno tarda demasiado, aprendé a decirle basta.

En la ventanilla, la campanilla vuelve a sonar sola. Esta vez, dos veces seguidas.

### Objetivos

- Arrancar varias tareas a la vez y esperar a todas con `Task.WhenAll`.
- Juntar lo que devuelve cada una.
- Quedarse con la primera que termina, con `Task.WhenAny`.
- Cancelar lo que tarda demasiado con `CancellationTokenSource`.

### Antes de empezar

- `async` y `await` (R05-N01).

### Explicación

#### De a una, o todas juntas

```csharp
await AfinarAsync("violín");   // 300 ms
await AfinarAsync("viola");    // 300 ms más
await AfinarAsync("chelo");    // 300 ms más: casi un segundo
```

Así, cada una empieza cuando termina la anterior: **en serie**. Pero afinar el violín no tiene nada que ver con afinar el chelo. Se pueden arrancar las tres y esperar a todas juntas:

```csharp
Task a = AfinarAsync("violín");
Task b = AfinarAsync("viola");
Task c = AfinarAsync("chelo");
await Task.WhenAll(a, b, c);   // tarda lo que la más lenta: 300 ms
```

`Task.WhenAll` («cuando todas») termina cuando terminaron **todas**.

#### Lo que devuelven

Si las tareas devuelven algo (`Task<int>`), `await Task.WhenAll(...)` da un **arreglo** con los resultados, **en el mismo orden** en que se las pasaste (no en el que terminaron):

```csharp
int[] cuerdas = await Task.WhenAll(ContarAsync("violín"), ContarAsync("guitarra"));
// cuerdas[0] es del violín, cuerdas[1] de la guitarra
```

#### La primera que llega

`Task.WhenAny` («cuando cualquiera») termina con la **primera** que termina, y te da esa tarea. Con otro `await` sacás su resultado:

```csharp
Task<string> primera = await Task.WhenAny(t1, t2, t3);
Console.WriteLine(await primera);
```

#### Medir cuánto tardó

`System.Diagnostics.Stopwatch` es un cronómetro:

```csharp
var reloj = System.Diagnostics.Stopwatch.StartNew();
// …
Console.WriteLine(reloj.ElapsedMilliseconds);   // milisegundos desde que arrancó
```

#### Decir basta: cancelar

Un `CancellationTokenSource` es el botón de «basta». Con `new CancellationTokenSource(500)` se aprieta solo a los 500 ms. Su `Token` se le pasa a quien espera; cuando se cancela, el `await` lanza una `OperationCanceledException`:

```csharp
var basta = new CancellationTokenSource(500);
try
{
    await Task.Delay(2000, basta.Token);
}
catch (OperationCanceledException)
{
    Console.WriteLine("Tardaba demasiado");
}
```

### Código de ejemplo

```csharp
async Task<int> AfinarAsync(string instrumento, int cuerdas)
{
    await Task.Delay(300);
    return cuerdas;
}

var reloj = System.Diagnostics.Stopwatch.StartNew();
int[] cuerdas = await Task.WhenAll(AfinarAsync("violín", 4), AfinarAsync("viola", 4), AfinarAsync("guitarra", 6));
Console.WriteLine($"Cuerdas afinadas: {cuerdas.Sum()}");
Console.WriteLine($"Menos de medio segundo: {reloj.ElapsedMilliseconds < 500}");
```

### Salida esperada

```
Cuerdas afinadas: 14
Menos de medio segundo: True
```

### ¿Para qué sirve?

Una página web pide a la vez las fotos, los comentarios y el perfil; un juego carga los sonidos y las texturas juntos. Pedir todo junto es mucho más rápido que de a uno. Y cancelar evita quedarse esperando para siempre algo que no va a llegar.

### Errores habituales

- **Esperar dentro del bucle:** `foreach (…) await AfinarAsync(…)` las hace de a una. Para que vayan juntas, juntá las tareas en una lista y esperá con `Task.WhenAll(lista)`.
- **Creer que el arreglo viene en el orden en que terminaron:** viene en el orden en que las pasaste.
- **Cancelar sin pasar el `Token`:** si no se lo das a `Task.Delay` (o a quien espere), nadie se entera de que apretaste «basta».

### Micro-misión R05-N02-P1 · Las tres juntas

```meta
lugar: El Escenario Grande
personajes: Ceci, Bemol
carta: Task.WhenAll | arrancá todas · await Task.WhenAll(a, b, c) · tarda lo que la más lenta
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Bemol afina el violín, la viola y el chelo de a uno. Tarda casi un segundo, y el público se impacienta.

#### Gheco sugiere
Si cada tarea es independiente, se pueden arrancar todas y esperar a que terminen juntas:

```csharp
Task a = LavarAsync("taza");
Task b = LavarAsync("plato");
await Task.WhenAll(a, b);
```

Así tardan lo que la más lenta, no la suma de todas.

#### Desafío
Arrancá las tres afinaciones sin `await` (guardalas en tres variables `Task`) y esperalas juntas con `await Task.WhenAll(...)`.

#### Código inicial
```csharp
async Task AfinarAsync(string instrumento)
{
    await Task.Delay(300);
}

var reloj = System.Diagnostics.Stopwatch.StartNew();
await AfinarAsync("violín");
await AfinarAsync("viola");
await AfinarAsync("chelo");
Console.WriteLine("Orquesta afinada");
Console.WriteLine($"Menos de medio segundo: {reloj.ElapsedMilliseconds < 500}");
```

#### Salida esperada
```
Orquesta afinada
Menos de medio segundo: True
```

#### Solución
```csharp
async Task AfinarAsync(string instrumento)
{
    await Task.Delay(300);
}

var reloj = System.Diagnostics.Stopwatch.StartNew();
Task a = AfinarAsync("violín");
Task b = AfinarAsync("viola");
Task c = AfinarAsync("chelo");
await Task.WhenAll(a, b, c);
Console.WriteLine("Orquesta afinada");
Console.WriteLine($"Menos de medio segundo: {reloj.ElapsedMilliseconds < 500}");
```

#### Al superarla
Tres instrumentos suenan a la vez, cada uno buscando su nota, y de golpe, los tres la encuentran.

#### Imagen
- Un escenario gótico con velas, con un violín, una viola y un chelo apoyados en atriles, cada uno con un brillo dorado suave, sin letras.
- Bemol, con el tambor colgando, señala los tres instrumentos; Ceci sonríe con el violín bajo el brazo.

### Micro-misión R05-N02-P2 · Juntar los resultados

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: Resultados de WhenAll | int[] r = await Task.WhenAll(…) · en el orden en que las pasaste
recompensa: xp 15, oro 15
```

#### Escena
Don Cedro cuenta a la vez las cuerdas de tres instrumentos, pero el total le da cero: espera las tareas y se olvida de mirar qué devolvieron.

#### Gheco sugiere
Cuando las tareas devuelven algo (`Task<int>`), `await Task.WhenAll(...)` da un **arreglo** con lo que devolvió cada una, en el orden en que se las pasaste:

```csharp
string[] nombres = await Task.WhenAll(BuscarAsync(1), BuscarAsync(2));
Console.WriteLine(nombres[0]);
```

Para sumar un arreglo de números, `Sum()`.

#### Desafío
Guardá lo que devuelve `Task.WhenAll` en un `int[] cuerdas` y mostrá su suma.

#### Código inicial
```csharp
async Task<int> ContarCuerdasAsync(string instrumento)
{
    await Task.Delay(200);
    return instrumento == "guitarra" ? 6 : 4;
}

await Task.WhenAll(ContarCuerdasAsync("violín"), ContarCuerdasAsync("guitarra"), ContarCuerdasAsync("viola"));
int total = 0;
Console.WriteLine($"Cuerdas en el taller: {total}");
```

#### Salida esperada
```
Cuerdas en el taller: 14
```

#### Solución
```csharp
async Task<int> ContarCuerdasAsync(string instrumento)
{
    await Task.Delay(200);
    return instrumento == "guitarra" ? 6 : 4;
}

int[] cuerdas = await Task.WhenAll(ContarCuerdasAsync("violín"), ContarCuerdasAsync("guitarra"), ContarCuerdasAsync("viola"));
int total = cuerdas.Sum();
Console.WriteLine($"Cuerdas en el taller: {total}");
```

#### Al superarla
—Catorce —dice Don Cedro—. Y ninguna rota, por una vez.

#### Imagen
- Un taller de luthier de madera cálida con velas, con un violín, una viola y una guitarra colgados en fila en la pared, sin letras.
- Don Cedro cuenta con los dedos; Ceci le alcanza un rollo de cuerdas nuevas.

### Micro-misión R05-N02-P3 · La primera que llega

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Bemol
carta: Task.WhenAny | await Task.WhenAny(…) → la PRIMERA tarea que terminó · await esa → su resultado
recompensa: xp 15, oro 15
```

#### Escena
Para llevar una partitura urgente al Puerto, Bemol llama a tres mensajeros a la vez: el que llegue primero, la lleva. Pero siempre elige al primero de la lista, aunque sea el más lento.

#### Gheco sugiere
`Task.WhenAny` termina cuando termina **cualquiera**, y te da esa tarea (la primera que terminó). Con otro `await` sacás lo que devolvió:

```csharp
Task<string> ganadora = await Task.WhenAny(t1, t2);
string nombre = await ganadora;
```

`Task.WhenAll`, en cambio, espera a todas y te da los resultados en el orden de la lista.

#### Desafío
Usá `Task.WhenAny` en vez de `Task.WhenAll`, y mostrá el resultado de la tarea que llegó primero.

#### Código inicial
```csharp
async Task<string> LlegarAsync(string mensajero, int ms)
{
    await Task.Delay(ms);
    return mensajero;
}

string[] todos = await Task.WhenAll(LlegarAsync("la paloma", 300), LlegarAsync("Nilo", 100), LlegarAsync("el carro", 200));
Console.WriteLine($"La lleva {todos[0]}");
```

#### Salida esperada
```
La lleva Nilo
```

#### Solución
```csharp
async Task<string> LlegarAsync(string mensajero, int ms)
{
    await Task.Delay(ms);
    return mensajero;
}

Task<string> primera = await Task.WhenAny(LlegarAsync("la paloma", 300), LlegarAsync("Nilo", 100), LlegarAsync("el carro", 200));
Console.WriteLine($"La lleva {await primera}");
```

#### Al superarla
Nilo llega corriendo, con la gorra torcida, y se lleva la partitura antes de que la paloma termine de desperezarse.

#### Imagen
- La ventanilla de madera de un conservatorio gótico de noche, con una partitura enrollada atada con cinta bordó sobre el mostrador y una paloma dormida en el alféizar, sin letras.
- Bemol entrega la partitura por la ventanilla; Ceci mira hacia la calle.

### Micro-misión R05-N02-P4 · Basta de esperar

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Clave
carta: Cancelar | var basta = new CancellationTokenSource(ms) · Task.Delay(…, basta.Token) · catch (OperationCanceledException)
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un pedido al depósito no vuelve nunca. Clave no quiere que la ventanilla espere para siempre: si en un rato no llegó, que avise.

#### Gheco sugiere
`new CancellationTokenSource(300)` es un botón de «basta» que se aprieta solo a los 300 ms. Su `Token` se le pasa a lo que espera (acá, como segundo dato de `Task.Delay`). Cuando se aprieta, el `await` lanza una `OperationCanceledException`:

```csharp
var basta = new CancellationTokenSource(300);
try
{
    await Task.Delay(5000, basta.Token);
}
catch (OperationCanceledException)
{
    Console.WriteLine("Cancelado");
}
```

#### Desafío
Creá `var basta = new CancellationTokenSource(300);`, pasale `basta.Token` a `EsperarAsync`, y atrapá la `OperationCanceledException` mostrando `Tardaba demasiado`.

#### Código inicial
```csharp
async Task<string> EsperarAsync(CancellationToken token)
{
    await Task.Delay(1500, token);
    return "Llegó la respuesta";
}

string r = await EsperarAsync(CancellationToken.None);
Console.WriteLine(r);
Console.WriteLine("Siguiente pedido");
```

#### Salida esperada
```
Tardaba demasiado
Siguiente pedido
```

#### Solución
```csharp
async Task<string> EsperarAsync(CancellationToken token)
{
    await Task.Delay(1500, token);
    return "Llegó la respuesta";
}

var basta = new CancellationTokenSource(300);
try
{
    string r = await EsperarAsync(basta.Token);
    Console.WriteLine(r);
}
catch (OperationCanceledException)
{
    Console.WriteLine("Tardaba demasiado");
}
Console.WriteLine("Siguiente pedido");
```

#### Al superarla
—Esperar tiene un límite —dice Clave—. Después de eso, es perder el tiempo de todos.

#### Imagen
- Un reloj de arena grande de bronce sobre el mostrador de una ventanilla de madera, con la arena casi terminada, con faroles, sin letras.
- Clave levanta la mano en señal de «basta»; Ceci mira el reloj de arena.

### Micro-misión R05-N02-P5 · El troll que se durmió

```meta
lugar: El Escenario Grande
personajes: Ceci, Gheco
criatura: troll
carta: Troll | si una tarea de WhenAll falla · el error salta en el await · try alrededor de await Task.WhenAll(…)
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un troll chiquito tenía que tocar el oboe con los demás, pero se quedó dormido. Cuando falla él, se cae toda la orquesta.

#### Gheco sugiere
Si una de las tareas de `Task.WhenAll` lanza un error, ese error salta en el `await Task.WhenAll(...)`. Se atrapa con un `try` alrededor de ese `await`, igual que con una sola tarea.

#### Desafío
Envolvé el `await Task.WhenAll(...)` en un `try` y atrapá la `InvalidOperationException` mostrando `Alguien no tocó: ` seguido del mensaje.

#### Código inicial
```csharp
async Task TocarAsync(string quien)
{
    await Task.Delay(100);
    if (quien == "el troll")
    {
        throw new InvalidOperationException("se quedó dormido");
    }
}

await Task.WhenAll(TocarAsync("Ceci"), TocarAsync("el troll"), TocarAsync("Bemol"));
Console.WriteLine("Concierto completo");
Console.WriteLine("Saludo final");
```

#### Salida esperada
```
Alguien no tocó: se quedó dormido
Saludo final
```

#### Solución
```csharp
async Task TocarAsync(string quien)
{
    await Task.Delay(100);
    if (quien == "el troll")
    {
        throw new InvalidOperationException("se quedó dormido");
    }
}

try
{
    await Task.WhenAll(TocarAsync("Ceci"), TocarAsync("el troll"), TocarAsync("Bemol"));
    Console.WriteLine("Concierto completo");
}
catch (InvalidOperationException e)
{
    Console.WriteLine($"Alguien no tocó: {e.Message}");
}
Console.WriteLine("Saludo final");
```

#### Al superarla
El troll se despierta con el aplauso final, se levanta de un salto y saluda como si hubiera tocado toda la noche.

#### Imagen
- Un escenario gótico con velas y atriles, con un oboe tirado en el piso, sin letras.
- El troll chiquito duerme sentado en una silla con la boca abierta; Gheco, parado solo sobre el atril, lo mira con las antiparras puestas.

### Encargo R05-N02-E1 · Los afinadores de la Feria

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Hilván contrató afinadores para los instrumentos del Teatro. Escribí un método `async Task AfinarAsync(string instrumento, int ms)` que espere `ms` milisegundos y después muestre `Afinado: ` con el instrumento. Leé líneas como `instrumento,ms` hasta una línea vacía, **arrancá todas las afinaciones a la vez** (guardalas en una `List<Task>`) y esperalas con `Task.WhenAll`. Al final, mostrá `Todos listos`. Como van juntas, terminan en el orden de sus tiempos, no en el de la lista.

Con esta entrada:

```
chelo,300
violín,100
viola,200

```

se muestra:

```
Afinado: violín
Afinado: viola
Afinado: chelo
Todos listos
```

#### Criterio de aprobación

- Arranca todas las tareas antes de esperar (no hay `await` adentro del bucle de lectura).
- Las espera con `await Task.WhenAll(...)`.

#### Entrada de ejemplo

```
chelo,300
violín,100
viola,200

```

#### Salida esperada

```
Afinado: violín
Afinado: viola
Afinado: chelo
Todos listos
```

#### Solución de referencia

```csharp
async Task AfinarAsync(string instrumento, int ms)
{
    await Task.Delay(ms);
    Console.WriteLine($"Afinado: {instrumento}");
}

List<Task> tareas = new List<Task>();
string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    string[] partes = linea.Split(',');
    tareas.Add(AfinarAsync(partes[0], int.Parse(partes[1])));
    linea = Console.ReadLine();
}
await Task.WhenAll(tareas);
Console.WriteLine("Todos listos");
```

## R05-N03 · La carrera y el candado

```meta
tipo: tema
padre: R05-N02
precio: 10
criatura: troll
temas: conc.sincronizacion
usa: conc.async
```

### Crónica

Al final del concierto, diez aprendices anotan los aplausos en la misma pizarra. Cada uno lee el número, suma uno y lo vuelve a escribir. Aplaudieron mil veces, pero la pizarra dice cien.

—Dos leyeron el mismo número a la vez —dice {mentor}—, y los dos escribieron lo mismo. Uno de los aplausos se perdió. Cuando varias tareas tocan la misma cosa, hace falta un **candado**: una pizarra, una tiza, y de a uno por vez.

### Objetivos

- Ver por qué se pierden datos cuando varias tareas cambian la misma variable.
- Achicar el hueco entre leer y escribir.
- Usar un candado (`SemaphoreSlim`) para que pasen de a una.
- Evitar el problema dándole a cada tarea lo suyo.
- Soltar el candado siempre, con `finally`.

### Antes de empezar

- `async`, `await` y `Task.WhenAll` (R05-N01 y R05-N02); `finally` (R04-N01).

### Explicación

#### La carrera

```csharp
int v = aplausos;      // 1. leo
await Task.Yield();    // 2. me distraigo un instante
aplausos = v + 1;      // 3. escribo
```

Si diez tareas hacen esto a la vez, varias leen **el mismo número** antes de que alguna escriba. Todas escriben `v + 1` con el mismo `v`, y los aplausos se pierden. Eso se llama una **condición de carrera**: el resultado depende de quién llega primero.

`await Task.Yield()` hace que la tarea ceda el turno un instante, como si se distrajera. En una compu de verdad, con varios **hilos** trabajando al mismo tiempo, esto pasa aunque no esperes nada: alcanza con que dos hilos lean a la vez. En el navegador hay un solo hilo, así que lo mostramos con `Task.Yield()`.

#### Achicar el hueco

Si leer y escribir pasan juntos, sin un `await` en el medio, nadie puede meterse entre las dos cosas:

```csharp
await Task.Yield();
aplausos++;            // leer y escribir, sin hueco
```

#### El candado: `SemaphoreSlim`

A veces hay que esperar algo entre leer y escribir. Entonces se usa un candado que deja pasar **de a uno**:

```csharp
var candado = new SemaphoreSlim(1);   // 1 = de a uno

await candado.WaitAsync();            // espero mi turno
try
{
    int v = aplausos;
    await Task.Yield();
    aplausos = v + 1;
}
finally
{
    candado.Release();                // libero el turno, pase lo que pase
}
```

`Release()` va en el `finally`: si algo falla adentro y nadie lo suelta, el candado queda cerrado y los demás esperan **para siempre**.

#### Mejor todavía: que cada una tenga lo suyo

Lo más seguro es no compartir: cada tarea cuenta lo suyo, lo devuelve, y al final se suma:

```csharp
int[] partes = await Task.WhenAll(ContarAsync(), ContarAsync());
int total = partes.Sum();
```

#### En una compu de verdad

Con hilos de verdad hay más herramientas: `lock (objeto) { … }` para código sin `await`, e `Interlocked.Increment(ref aplausos)`, que suma uno sin hueco. Se nombran acá para que las reconozcas: el problema y la idea son los mismos.

### Código de ejemplo

```csharp
var candado = new SemaphoreSlim(1);
int aplausos = 0;

async Task AplaudirAsync()
{
    for (int i = 0; i < 100; i++)
    {
        await candado.WaitAsync();
        try
        {
            int v = aplausos;
            await Task.Yield();
            aplausos = v + 1;
        }
        finally
        {
            candado.Release();
        }
    }
}

List<Task> aprendices = new List<Task>();
for (int i = 0; i < 10; i++)
{
    aprendices.Add(AplaudirAsync());
}
await Task.WhenAll(aprendices);
Console.WriteLine($"Aplausos: {aplausos}");
```

### Salida esperada

```
Aplausos: 1000
```

### ¿Para qué sirve?

Un servidor atiende a muchos a la vez: dos personas compran la última entrada, dos jugadores agarran el mismo cofre. Sin candado, se vende dos veces lo mismo. Los errores de carrera son de los más difíciles de encontrar, porque a veces pasan y a veces no.

### Errores habituales

- **El hueco entre leer y escribir:** cualquier `await` entre `int v = x;` y `x = v + 1;` es una puerta abierta para que otra tarea se meta.
- **`Release()` afuera del `finally`:** si salta un error, el candado no se suelta y el programa se queda esperando para siempre.
- **`WaitAsync()` sin `await`:** no espera nada, y el candado no cuida a nadie.

### Micro-misión R05-N03-P1 · Los aplausos perdidos

```meta
lugar: El Escenario Grande
personajes: Ceci, Bemol
carta: La carrera | leer · hueco (await) · escribir → se pierden datos · sin hueco: x++
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Diez aprendices anotan los aplausos en la misma pizarra. Aplaudieron mil veces, pero la pizarra dice cien.

#### Gheco sugiere
Cada aprendiz lee el número (`int v = aplausos;`), se distrae un instante (`await Task.Yield();`) y escribe `v + 1`. Mientras uno se distrae, los otros leen el **mismo** número, y todos escriben lo mismo: los aplausos se pierden.

Si se distraen **antes** de leer, y leer y sumar pasan juntos, nadie puede meterse en el medio:

```csharp
await Task.Yield();
contador++;
```

#### Desafío
Dejá el `await Task.Yield();` al principio de la vuelta y reemplazá las otras dos líneas por `aplausos++;`.

#### Código inicial
```csharp
int aplausos = 0;

async Task AplaudirAsync()
{
    for (int i = 0; i < 100; i++)
    {
        int v = aplausos;
        await Task.Yield();
        aplausos = v + 1;
    }
}

List<Task> aprendices = new List<Task>();
for (int i = 0; i < 10; i++)
{
    aprendices.Add(AplaudirAsync());
}
await Task.WhenAll(aprendices);
Console.WriteLine($"Aplausos: {aplausos}");
```

#### Salida esperada
```
Aplausos: 1000
```

#### Solución
```csharp
int aplausos = 0;

async Task AplaudirAsync()
{
    for (int i = 0; i < 100; i++)
    {
        await Task.Yield();
        aplausos++;
    }
}

List<Task> aprendices = new List<Task>();
for (int i = 0; i < 10; i++)
{
    aprendices.Add(AplaudirAsync());
}
await Task.WhenAll(aprendices);
Console.WriteLine($"Aplausos: {aplausos}");
```

#### Al superarla
La pizarra marca mil. Bemol aplaude una vez más, nada más que para ver el número cambiar.

#### Imagen
- Una pizarra de madera con marco dorado en un costado de un escenario gótico con velas, con muchas rayitas de tiza agrupadas, sin letras ni números.
- Bemol aplaude con entusiasmo; Ceci, con una tiza en la mano, mira la pizarra.

### Micro-misión R05-N03-P2 · El candado

```meta
lugar: El Escenario Grande
personajes: Ceci, Clave
carta: SemaphoreSlim | await candado.WaitAsync() · try { … } · finally { candado.Release(); }
recompensa: xp 15, oro 15
```

#### Escena
Ahora cada aprendiz tiene que mirar la pizarra con la lupa antes de anotar, y eso tarda. El hueco entre leer y escribir no se puede sacar: hace falta un candado.

#### Gheco sugiere
`new SemaphoreSlim(1)` es un candado que deja pasar **de a uno**. Antes de tocar lo compartido se espera el turno con `await candado.WaitAsync();`, y al terminar se suelta con `candado.Release();`, en un `finally`:

```csharp
await candado.WaitAsync();
try
{
    // tocar lo compartido
}
finally
{
    candado.Release();
}
```

Mientras uno está adentro, los demás esperan en `WaitAsync`.

#### Desafío
Envolvé las tres líneas de adentro del `for` con el candado: `await candado.WaitAsync();`, un `try` con las tres líneas y un `finally` con `candado.Release();`.

#### Código inicial
```csharp
var candado = new SemaphoreSlim(1);
int aplausos = 0;

async Task AplaudirAsync()
{
    for (int i = 0; i < 100; i++)
    {
        int v = aplausos;
        await Task.Yield();
        aplausos = v + 1;
    }
}

List<Task> aprendices = new List<Task>();
for (int i = 0; i < 10; i++)
{
    aprendices.Add(AplaudirAsync());
}
await Task.WhenAll(aprendices);
Console.WriteLine($"Aplausos: {aplausos}");
```

#### Salida esperada
```
Aplausos: 1000
```

#### Solución
```csharp
var candado = new SemaphoreSlim(1);
int aplausos = 0;

async Task AplaudirAsync()
{
    for (int i = 0; i < 100; i++)
    {
        await candado.WaitAsync();
        try
        {
            int v = aplausos;
            await Task.Yield();
            aplausos = v + 1;
        }
        finally
        {
            candado.Release();
        }
    }
}

List<Task> aprendices = new List<Task>();
for (int i = 0; i < 10; i++)
{
    aprendices.Add(AplaudirAsync());
}
await Task.WhenAll(aprendices);
Console.WriteLine($"Aplausos: {aplausos}");
```

#### Al superarla
—Una pizarra, una tiza —dice Clave—, y de a uno por vez. Así se escribe la historia sin borrones.

#### Imagen
- Una pizarra de madera con un candado de bronce colgando de una cadena en el marco, en un escenario gótico con velas, sin letras.
- Clave sostiene la llave del candado; Ceci espera su turno con la tiza en la mano.

### Micro-misión R05-N03-P3 · Cada uno lo suyo

```meta
lugar: El Escenario Grande
personajes: Ceci, Bemol
carta: Sin compartir | cada tarea cuenta lo suyo y lo devuelve · int[] r = await Task.WhenAll(…) · r.Sum()
recompensa: xp 15, oro 15
```

#### Escena
Bemol tiene una idea: que cada aprendiz anote sus aplausos en su propio papelito, y al final se suman todos.

#### Gheco sugiere
Si cada tarea cuenta en **su propia** variable y la devuelve, no hay nada compartido y no hace falta candado. Al final se juntan los resultados con `Task.WhenAll` y se suman:

```csharp
async Task<int> ContarAsync()
{
    int mio = 0;
    // … mio++ …
    return mio;
}

int[] partes = await Task.WhenAll(ContarAsync(), ContarAsync());
Console.WriteLine(partes.Sum());
```

Para juntar las tareas en una lista: `List<Task<int>>`.

#### Desafío
Hacé que `AplaudirAsync` cuente en una variable propia (`int mios = 0;`) y la devuelva (`async Task<int>`). Juntá las tareas en una `List<Task<int>>` y mostrá la suma de lo que devuelve `Task.WhenAll`.

#### Código inicial
```csharp
int aplausos = 0;

async Task AplaudirAsync()
{
    for (int i = 0; i < 100; i++)
    {
        int v = aplausos;
        await Task.Yield();
        aplausos = v + 1;
    }
}

List<Task> aprendices = new List<Task>();
for (int i = 0; i < 10; i++)
{
    aprendices.Add(AplaudirAsync());
}
await Task.WhenAll(aprendices);
Console.WriteLine($"Aplausos: {aplausos}");
```

#### Salida esperada
```
Aplausos: 1000
```

#### Solución
```csharp
async Task<int> AplaudirAsync()
{
    int mios = 0;
    for (int i = 0; i < 100; i++)
    {
        int v = mios;
        await Task.Yield();
        mios = v + 1;
    }
    return mios;
}

List<Task<int>> aprendices = new List<Task<int>>();
for (int i = 0; i < 10; i++)
{
    aprendices.Add(AplaudirAsync());
}
int[] partes = await Task.WhenAll(aprendices);
Console.WriteLine($"Aplausos: {partes.Sum()}");
```

#### Al superarla
Diez papelitos, diez números, una suma. Bemol los apila con cuidado, como si fueran cartas de una baraja.

#### Imagen
- Una mesa de madera en un costado de un escenario gótico con velas, con diez papelitos lisos apilados en fila, sin letras ni números.
- Bemol apila los papelitos con cuidado; Ceci los cuenta con el dedo.

### Micro-misión R05-N03-P4 · La última butaca

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Bemol
carta: Mirar y tomar, juntos | si (libre) … await … tomar · entre mirar y tomar, otro se mete · candado alrededor de las dos
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Queda una sola butaca, la A1. Ceci y Bemol la piden a la vez por la ventanilla, y los dos se van contentos con la misma entrada.

#### Gheco sugiere
El programa **mira** si la butaca está libre, tarda un poco en anotarla, y después la **toma**. Mientras uno anota, el otro mira, la ve libre y también la toma.

El candado tiene que abrazar **las dos cosas**: mirar y tomar. Así, el segundo recién mira cuando el primero ya la tomó.

#### Desafío
Poné todo lo de adentro de `ReservarAsync` entre `await candado.WaitAsync();` y un `finally` con `candado.Release();`.

#### Código inicial
```csharp
var candado = new SemaphoreSlim(1);
List<string> vendidas = new List<string>();

async Task ReservarAsync(string quien, string butaca)
{
    if (!vendidas.Contains(butaca))
    {
        await Task.Delay(50);
        vendidas.Add(butaca);
        Console.WriteLine($"{quien} reservó {butaca}");
    }
    else
    {
        Console.WriteLine($"{quien}: {butaca} ya está vendida");
    }
}

await Task.WhenAll(ReservarAsync("Ceci", "A1"), ReservarAsync("Bemol", "A1"));
```

#### Salida esperada
```
Ceci reservó A1
Bemol: A1 ya está vendida
```

#### Solución
```csharp
var candado = new SemaphoreSlim(1);
List<string> vendidas = new List<string>();

async Task ReservarAsync(string quien, string butaca)
{
    await candado.WaitAsync();
    try
    {
        if (!vendidas.Contains(butaca))
        {
            await Task.Delay(50);
            vendidas.Add(butaca);
            Console.WriteLine($"{quien} reservó {butaca}");
        }
        else
        {
            Console.WriteLine($"{quien}: {butaca} ya está vendida");
        }
    }
    finally
    {
        candado.Release();
    }
}

await Task.WhenAll(ReservarAsync("Ceci", "A1"), ReservarAsync("Bemol", "A1"));
```

#### Al superarla
—Te la regalo —dice Bemol—. Total, yo toco el tambor desde el escenario.

#### Imagen
- La ventanilla de madera de un conservatorio gótico con dos entradas de papel liso iguales sobre el mostrador, con faroles, sin letras.
- Ceci y Bemol se miran sorprendidos, cada uno con la mano estirada hacia la misma entrada.

### Micro-misión R05-N03-P5 · El candado que nadie soltó

```meta
lugar: El Escenario Grande
personajes: Ceci, Gheco
criatura: troll
carta: Troll | Release() afuera del finally · si salta un error, el candado queda cerrado · y los demás esperan para siempre
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un troll chiquito entra a tocar, desafina, sale corriendo… y se lleva la llave del candado. Bemol se queda esperando su turno para siempre.

#### Gheco sugiere
`candado.Release();` está después de la parte que puede fallar. Cuando el troll desafina, salta el error, el `Release()` no corre y el candado **queda cerrado**: el siguiente se queda en `WaitAsync` esperando para siempre, y el programa se corta por tiempo.

Por eso el `Release()` va en un `finally`: corre **siempre**, haya error o no.

#### Desafío
Poné lo que está entre `WaitAsync` y `Release` en un `try`, y el `Release()` en un `finally`.

#### Código inicial
```csharp
var candado = new SemaphoreSlim(1);

async Task TocarAsync(string quien)
{
    await candado.WaitAsync();
    await Task.Delay(50);
    if (quien == "el troll")
    {
        throw new InvalidOperationException("desafinó");
    }
    Console.WriteLine($"{quien} toca");
    candado.Release();
}

foreach (string musico in new[] { "Ceci", "el troll", "Bemol" })
{
    try
    {
        await TocarAsync(musico);
    }
    catch (InvalidOperationException e)
    {
        Console.WriteLine($"{musico}: {e.Message}");
    }
}
```

#### Salida esperada
```
Ceci toca
el troll: desafinó
Bemol toca
```

#### Solución
```csharp
var candado = new SemaphoreSlim(1);

async Task TocarAsync(string quien)
{
    await candado.WaitAsync();
    try
    {
        await Task.Delay(50);
        if (quien == "el troll")
        {
            throw new InvalidOperationException("desafinó");
        }
        Console.WriteLine($"{quien} toca");
    }
    finally
    {
        candado.Release();
    }
}

foreach (string musico in new[] { "Ceci", "el troll", "Bemol" })
{
    try
    {
        await TocarAsync(musico);
    }
    catch (InvalidOperationException e)
    {
        Console.WriteLine($"{musico}: {e.Message}");
    }
}
```

#### Al superarla
El troll vuelve, colorado, y deja la llave sobre el atril. Bemol entra, toca, y sale silbando.

#### Imagen
- Una puerta de madera de un camarín gótico con un candado de bronce cerrado, con faroles, sin letras.
- El troll chiquito se escapa corriendo con una llave de bronce en la mano; Gheco, parado solo sobre un banquito, lo señala con la cola.

### Encargo R05-N03-E1 · El contador del Gremio

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

En el torneo del Gremio, varios jueces suman puntos al mismo marcador a la vez. Leé líneas como `juez,puntos` hasta una línea vacía. Por cada juez, arrancá una tarea que sume sus puntos **de a uno** al marcador compartido, con `await Task.Yield();` entre leer el marcador y escribirlo (como un juez que mira antes de anotar). Protegé el marcador con un `SemaphoreSlim`, esperá a todos los jueces con `Task.WhenAll` y mostrá el marcador.

Con esta entrada:

```
Kira,30
Zed,25
Tizón,45

```

se muestra:

```
Marcador: 100
```

#### Criterio de aprobación

- Cada juez es una tarea; se esperan todas con `Task.WhenAll`.
- Leer y escribir el marcador está protegido con `SemaphoreSlim`, con el `Release()` en un `finally`.

#### Entrada de ejemplo

```
Kira,30
Zed,25
Tizón,45

```

#### Salida esperada

```
Marcador: 100
```

#### Solución de referencia

```csharp
var candado = new SemaphoreSlim(1);
int marcador = 0;

async Task SumarAsync(int puntos)
{
    for (int i = 0; i < puntos; i++)
    {
        await candado.WaitAsync();
        try
        {
            int v = marcador;
            await Task.Yield();
            marcador = v + 1;
        }
        finally
        {
            candado.Release();
        }
    }
}

List<Task> jueces = new List<Task>();
string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    string[] partes = linea.Split(',');
    jueces.Add(SumarAsync(int.Parse(partes[1])));
    linea = Console.ReadLine();
}
await Task.WhenAll(jueces);
Console.WriteLine($"Marcador: {marcador}");
```

## R05-N04 · Ensayar con pruebas: xUnit

```meta
tipo: tema
padre: R05-N03
precio: 10
criatura: slime
temas: cal.pruebas
usa: poo.clases, err.excepciones
```

### Crónica

Don Cedro arregló el afinador mecánico del Conservatorio. Para saber si anda, lo prueba a mano: violín, cuatro cuerdas; guitarra, seis. Al día siguiente cambia una pieza y tiene que probar todo de nuevo. Y al otro, otra vez.

—Un músico no ensaya una vez y listo —dice {mentor}—. Ensaya **cada vez** que cambia algo. Tus programas también: escribí las pruebas una vez, y que se ensayen solas.

### Objetivos

- Escribir una **prueba automática** con `[Fact]` y `Assert.Equal`.
- Leer el resultado: en verde, pasó; en rojo, algo no da.
- Comprobar que algo lanza un error con `Assert.Throws`.
- Probar varios casos con una sola prueba: `[Theory]` e `[InlineData]`.

### Antes de empezar

- Clases y métodos (Acto II) y excepciones (R04-N01 y R04-N02).

### Explicación

#### Probar a mano o probar solo

Hasta ahora, para saber si un método andaba, lo llamabas y mirabas lo que mostraba. Una **prueba automática** es un método que llama a tu código y **compara** el resultado con lo que tiene que dar. Si da, pasa; si no, avisa. Se escribe una vez y se corre siempre.

En C#, la herramienta más usada para eso es **xUnit**:

```csharp
using Xunit;

public class Afinador
{
    public int Cuerdas(string instrumento) => instrumento == "guitarra" ? 6 : 4;
}

public class AfinadorTests
{
    [Fact]
    public void ViolinTieneCuatro()
    {
        Afinador a = new Afinador();
        Assert.Equal(4, a.Cuerdas("violín"));
    }
}
```

- `using Xunit;` trae las herramientas de prueba.
- `[Fact]` («hecho») marca un método como **prueba**. Sin eso, es un método común y nadie lo corre.
- `Assert.Equal(esperado, obtenido)`: primero lo que **tiene que dar**, después lo que **dio**. Si no son iguales, la prueba falla.
- Las pruebas van en otra clase, que por costumbre se llama como la que prueba más `Tests`.

#### El resultado

Si tu archivo tiene pruebas, al terminar el ensayo se corren todas:

```
Corriendo las pruebas…
  ✓ AfinadorTests.ViolinTieneCuatro
  ✗ AfinadorTests.GuitarraTieneSeis
      Assert.Equal() falló
      Esperado: 6
      Obtenido: 4

Pasaron 1 de 2 pruebas. ✗ Fallaron 1.
```

`✓` es una prueba en verde; `✗`, en rojo, con lo que esperaba y lo que obtuvo. Un archivo que solo tiene clases y pruebas, sin programa principal, también se ensaya: se corren las pruebas y listo.

#### Otras comprobaciones

| Assert | Pasa si… |
|---|---|
| `Assert.Equal(4, x)` | `x` vale 4 |
| `Assert.True(cond)` / `Assert.False(cond)` | la condición es verdadera / falsa |
| `Assert.Contains("do", texto)` | el texto tiene `do` adentro |
| `Assert.Null(x)` / `Assert.NotNull(x)` | `x` es / no es `null` |
| `Assert.Throws<ArgumentException>(() => …)` | lo de adentro lanza **ese** error |

#### Varios casos: `[Theory]`

Para probar lo mismo con distintos datos, en vez de copiar la prueba se usa `[Theory]` («teoría»), y cada `[InlineData]` es un caso. Los datos llegan como parámetros, en orden:

```csharp
[Theory]
[InlineData("violín", 4)]
[InlineData("guitarra", 6)]
public void CuentaCuerdas(string instrumento, int esperado)
{
    Assert.Equal(esperado, new Afinador().Cuerdas(instrumento));
}
```

#### En una compu de verdad

Las pruebas viven en un proyecto aparte. En Linux y en Windows es igual: `dotnet new xunit -o Pruebas` crea el proyecto, y `dotnet test` las corre todas y muestra cuántas pasaron.

### Código de ejemplo

```csharp
using Xunit;

public class Metronomo
{
    public int Pulsos(int compases, int tiempos) => compases * tiempos;
}

public class MetronomoTests
{
    [Fact]
    public void CuatroCompasesDeTres()
    {
        Assert.Equal(12, new Metronomo().Pulsos(4, 3));
    }

    [Theory]
    [InlineData(1, 4, 4)]
    [InlineData(2, 2, 4)]
    public void VariosCasos(int compases, int tiempos, int esperado)
    {
        Assert.Equal(esperado, new Metronomo().Pulsos(compases, tiempos));
    }
}
```

### Salida esperada

```
Corriendo las pruebas…
  ✓ MetronomoTests.CuatroCompasesDeTres
  ✓ MetronomoTests.VariosCasos(1, 4, 4)
  ✓ MetronomoTests.VariosCasos(2, 2, 4)

Pasaron 3 de 3 pruebas. ✓ Todo en verde.
```

### ¿Para qué sirve?

Los programas grandes cambian todos los días. Con pruebas, cada cambio se ensaya solo en segundos: si algo que andaba deja de andar, te enterás enseguida, y no cuando ya lo usa todo el mundo. Casi todos los equipos de programación trabajan así.

### Errores habituales

- **Olvidar el `[Fact]`:** el método no se corre, y parece que «no hay errores» cuando en realidad no se probó nada.
- **Dar vuelta el `Assert.Equal`:** primero lo esperado, después lo obtenido. Al revés también falla bien, pero el mensaje confunde.
- **Arreglar la prueba en vez del código:** si una prueba bien escrita está en rojo, lo que hay que arreglar es el programa.

### Micro-misión R05-N04-P1 · La primera prueba

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: [Fact] | marca un método como prueba · sin [Fact], nadie la corre
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Don Cedro escribió la prueba del afinador, pero cuando ensaya no pasa nada: ni verde, ni rojo. Nadie la está corriendo.

#### Gheco sugiere
Para que un método sea una **prueba**, lleva `[Fact]` justo arriba:

```csharp
[Fact]
public void DoEsLaPrimera()
{
    Assert.Equal("do", Escala.Primera());
}
```

Sin `[Fact]`, es un método común: nadie lo llama, y el ensayo no muestra nada.

#### Desafío
Agregale `[Fact]` arriba del método `ViolinTieneCuatro`.

#### Código inicial
```csharp
using Xunit;

public class Afinador
{
    public int Cuerdas(string instrumento) => instrumento == "guitarra" ? 6 : 4;
}

public class AfinadorTests
{
    public void ViolinTieneCuatro()
    {
        Afinador a = new Afinador();
        Assert.Equal(4, a.Cuerdas("violín"));
    }
}
```

#### Salida esperada
```
Corriendo las pruebas…
  ✓ AfinadorTests.ViolinTieneCuatro

Pasaron 1 de 1 pruebas. ✓ Todo en verde.
```

#### Solución
```csharp
using Xunit;

public class Afinador
{
    public int Cuerdas(string instrumento) => instrumento == "guitarra" ? 6 : 4;
}

public class AfinadorTests
{
    [Fact]
    public void ViolinTieneCuatro()
    {
        Afinador a = new Afinador();
        Assert.Equal(4, a.Cuerdas("violín"));
    }
}
```

#### Al superarla
—Verde —dice Don Cedro, y se lo dice al afinador, como si pudiera escucharlo.

#### Imagen
- Un taller de luthier de madera cálida con velas, con un afinador mecánico de bronce con agujas sobre la mesa y una lucecita verde encendida, sin letras.
- Don Cedro mira la lucecita verde por encima de los anteojos; Ceci aplaude bajito.

### Micro-misión R05-N04-P2 · Esperado y obtenido

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: Assert.Equal | Assert.Equal(lo que TIENE que dar, lo que dio) · si no son iguales, rojo
recompensa: xp 15, oro 15
```

#### Escena
La prueba de la guitarra sale en rojo. Don Cedro revisa el afinador y está perfecto: el error está en la prueba, que espera cuatro cuerdas para una guitarra.

#### Gheco sugiere
`Assert.Equal(esperado, obtenido)` compara dos cosas: primero lo que **tiene que dar**, después lo que **dio** tu código.

```csharp
Assert.Equal(7, Escala.Notas());   // la escala tiene 7 notas
```

Si la prueba espera algo equivocado, falla aunque el código esté bien. Leé el rojo: dice lo esperado y lo obtenido.

#### Desafío
Una guitarra tiene 6 cuerdas: corregí lo que espera la segunda prueba.

#### Código inicial
```csharp
using Xunit;

public class Afinador
{
    public int Cuerdas(string instrumento) => instrumento == "guitarra" ? 6 : 4;
}

public class AfinadorTests
{
    [Fact]
    public void ViolinTieneCuatro()
    {
        Assert.Equal(4, new Afinador().Cuerdas("violín"));
    }

    [Fact]
    public void GuitarraTieneSeis()
    {
        Assert.Equal(4, new Afinador().Cuerdas("guitarra"));
    }
}
```

#### Salida esperada
```
Corriendo las pruebas…
  ✓ AfinadorTests.ViolinTieneCuatro
  ✓ AfinadorTests.GuitarraTieneSeis

Pasaron 2 de 2 pruebas. ✓ Todo en verde.
```

#### Solución
```csharp
using Xunit;

public class Afinador
{
    public int Cuerdas(string instrumento) => instrumento == "guitarra" ? 6 : 4;
}

public class AfinadorTests
{
    [Fact]
    public void ViolinTieneCuatro()
    {
        Assert.Equal(4, new Afinador().Cuerdas("violín"));
    }

    [Fact]
    public void GuitarraTieneSeis()
    {
        Assert.Equal(6, new Afinador().Cuerdas("guitarra"));
    }
}
```

#### Al superarla
—A veces el que desafina es el que escucha —dice Don Cedro, y se ríe solo de su chiste.

#### Imagen
- Un taller de luthier de madera cálida con velas, con una guitarra colgada en la pared al lado de un violín, sin letras.
- Don Cedro cuenta las cuerdas de la guitarra con el dedo; Ceci lo mira divertida.

### Micro-misión R05-N04-P3 · La prueba encontró algo

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Rojo = arreglar el código | si la prueba está bien escrita · y sale en rojo · el error está en el programa
recompensa: xp 15, oro 15
```

#### Escena
El metrónomo nuevo cuenta mal los pulsos: cuatro compases de tres tiempos le dan siete. La prueba lo descubrió.

#### Gheco sugiere
Esta vez la prueba está bien: cuatro compases de tres tiempos son doce pulsos (`4 * 3`). El rojo dice:

```
Esperado: 12
Obtenido: 7
```

Siete es `4 + 3`: el método **suma** en vez de **multiplicar**. Lo que hay que arreglar es el programa, no la prueba.

#### Desafío
Corregí el método `Pulsos` para que multiplique.

#### Código inicial
```csharp
using Xunit;

public class Metronomo
{
    public int Pulsos(int compases, int tiempos) => compases + tiempos;
}

public class MetronomoTests
{
    [Fact]
    public void CuatroCompasesDeTres()
    {
        Assert.Equal(12, new Metronomo().Pulsos(4, 3));
    }
}
```

#### Salida esperada
```
Corriendo las pruebas…
  ✓ MetronomoTests.CuatroCompasesDeTres

Pasaron 1 de 1 pruebas. ✓ Todo en verde.
```

#### Solución
```csharp
using Xunit;

public class Metronomo
{
    public int Pulsos(int compases, int tiempos) => compases * tiempos;
}

public class MetronomoTests
{
    [Fact]
    public void CuatroCompasesDeTres()
    {
        Assert.Equal(12, new Metronomo().Pulsos(4, 3));
    }
}
```

#### Al superarla
—Por eso se ensaya —dice Clave—. Mejor que lo descubra una prueba y no la orquesta, en medio del concierto.

#### Imagen
- Una sala de ensayo gótica con velas y atriles, con un metrónomo de madera con forma de pirámide sobre una mesa, con el péndulo en movimiento, sin letras.
- Clave señala el metrónomo con la batuta; Ceci lo mira con el ceño fruncido.

### Micro-misión R05-N04-P4 · Que falle cuando tiene que fallar

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: Assert.Throws | Assert.Throws<ArgumentException>(() => …) · pasa si lo de adentro LANZA ese error
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
El afinador no acepta frecuencias negativas: lanza un error, como debe. Pero la prueba que lo comprueba sale en rojo, porque el error la tira abajo a ella también.

#### Gheco sugiere
Si lo que querés probar es que algo **lanza** un error, no lo llames directamente: el error tumba la prueba. Se lo pasás a `Assert.Throws`, que lo llama, atrapa el error y comprueba que sea de ese tipo:

```csharp
Assert.Throws<FormatException>(() => int.Parse("hola"));
```

`() => …` es una lambda (R03-N06): el código que `Assert.Throws` va a correr.

#### Desafío
Cambiá la línea de la prueba por `Assert.Throws<ArgumentException>(() => new Afinador().Afinar(-1));`.

#### Código inicial
```csharp
using Xunit;

public class Afinador
{
    public string Afinar(int frecuencia)
    {
        if (frecuencia <= 0)
        {
            throw new ArgumentException("la frecuencia tiene que ser positiva");
        }
        return $"{frecuencia} Hz";
    }
}

public class AfinadorTests
{
    [Fact]
    public void FrecuenciaNegativaFalla()
    {
        new Afinador().Afinar(-1);
    }
}
```

#### Salida esperada
```
Corriendo las pruebas…
  ✓ AfinadorTests.FrecuenciaNegativaFalla

Pasaron 1 de 1 pruebas. ✓ Todo en verde.
```

#### Solución
```csharp
using Xunit;

public class Afinador
{
    public string Afinar(int frecuencia)
    {
        if (frecuencia <= 0)
        {
            throw new ArgumentException("la frecuencia tiene que ser positiva");
        }
        return $"{frecuencia} Hz";
    }
}

public class AfinadorTests
{
    [Fact]
    public void FrecuenciaNegativaFalla()
    {
        Assert.Throws<ArgumentException>(() => new Afinador().Afinar(-1));
    }
}
```

#### Al superarla
—Un afinador que se queja cuando tiene que quejarse —dice Don Cedro— es un buen afinador.

#### Imagen
- Un taller de luthier de madera cálida con velas, con el afinador mecánico de bronce sobre la mesa soltando una chispita roja, sin letras.
- Don Cedro se tapa un ojo, divertido; Ceci sostiene una pinza de luthier.

### Micro-misión R05-N04-P5 · El slime de las etiquetas

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
criatura: slime
carta: Slime | [Fact] no lleva datos · con datos: [Theory] · un [InlineData(…)] por caso
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un slime verde le pegó la etiqueta equivocada a una prueba: la que tenía que probar varios instrumentos dice `[Fact]`, y el ensayo no sabe con qué datos correrla.

#### Gheco sugiere
Un `[Fact]` no recibe datos. Si la prueba tiene parámetros, va `[Theory]`, y cada caso es un `[InlineData(...)]` con los datos en el mismo orden que los parámetros:

```csharp
[Theory]
[InlineData(2, 4)]
[InlineData(5, 10)]
public void Doble(int n, int esperado) => Assert.Equal(esperado, n * 2);
```

Cada `[InlineData]` es una prueba aparte en el resultado.

#### Desafío
Cambiá `[Fact]` por `[Theory]` y agregá tres casos: `("violín", 4)`, `("guitarra", 6)` y `("chelo", 4)`.

#### Código inicial
```csharp
using Xunit;

public class Afinador
{
    public int Cuerdas(string instrumento) => instrumento == "guitarra" ? 6 : 4;
}

public class AfinadorTests
{
    [Fact]
    public void CuentaCuerdas(string instrumento, int esperado)
    {
        Assert.Equal(esperado, new Afinador().Cuerdas(instrumento));
    }
}
```

#### Salida esperada
```
Corriendo las pruebas…
  ✓ AfinadorTests.CuentaCuerdas("violín", 4)
  ✓ AfinadorTests.CuentaCuerdas("guitarra", 6)
  ✓ AfinadorTests.CuentaCuerdas("chelo", 4)

Pasaron 3 de 3 pruebas. ✓ Todo en verde.
```

#### Solución
```csharp
using Xunit;

public class Afinador
{
    public int Cuerdas(string instrumento) => instrumento == "guitarra" ? 6 : 4;
}

public class AfinadorTests
{
    [Theory]
    [InlineData("violín", 4)]
    [InlineData("guitarra", 6)]
    [InlineData("chelo", 4)]
    public void CuentaCuerdas(string instrumento, int esperado)
    {
        Assert.Equal(esperado, new Afinador().Cuerdas(instrumento));
    }
}
```

#### Al superarla
El slime se despega de la prueba con un ¡plop!, rebota dos veces y se va a buscar otra etiqueta para pegar.

#### Imagen
- Una sala de ensayo gótica con velas, con tres atriles en fila, cada uno con una etiqueta de cartón lisa colgando, sin letras.
- El Slime Desafinado se pega a una de las etiquetas; Gheco, parado solo sobre un atril, tira de la etiqueta para despegarla.

### Encargo R05-N04-E1 · La boletería del Teatro

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Hilván necesita una boletería para el Teatro. Escribí la clase `Boleteria` con un método `int Precio(int edad)`: los menores de 12 pagan 500, los de 65 o más pagan 600, y el resto, 1000; una edad negativa lanza `ArgumentException`. Escribí la clase `BoleteriaTests` con:

- una `[Theory]` llamada `PrecioSegunEdad` con estos casos, en este orden: `(5, 500)`, `(12, 1000)`, `(40, 1000)` y `(70, 600)`;
- un `[Fact]` llamado `EdadNegativaFalla` que compruebe con `Assert.Throws` que `Precio(-1)` lanza `ArgumentException`.

Todas tienen que salir en verde:

```
Corriendo las pruebas…
  ✓ BoleteriaTests.PrecioSegunEdad(5, 500)
  ✓ BoleteriaTests.PrecioSegunEdad(12, 1000)
  ✓ BoleteriaTests.PrecioSegunEdad(40, 1000)
  ✓ BoleteriaTests.PrecioSegunEdad(70, 600)
  ✓ BoleteriaTests.EdadNegativaFalla

Pasaron 5 de 5 pruebas. ✓ Todo en verde.
```

#### Criterio de aprobación

- La `[Theory]` tiene los cuatro casos con `[InlineData]` y compara con `Assert.Equal`.
- El `[Fact]` usa `Assert.Throws<ArgumentException>`.

#### Salida esperada

```
Corriendo las pruebas…
  ✓ BoleteriaTests.PrecioSegunEdad(5, 500)
  ✓ BoleteriaTests.PrecioSegunEdad(12, 1000)
  ✓ BoleteriaTests.PrecioSegunEdad(40, 1000)
  ✓ BoleteriaTests.PrecioSegunEdad(70, 600)
  ✓ BoleteriaTests.EdadNegativaFalla

Pasaron 5 de 5 pruebas. ✓ Todo en verde.
```

#### Solución de referencia

```csharp
using Xunit;

public class Boleteria
{
    public int Precio(int edad)
    {
        if (edad < 0)
        {
            throw new ArgumentException("la edad no puede ser negativa");
        }
        if (edad < 12)
        {
            return 500;
        }
        if (edad >= 65)
        {
            return 600;
        }
        return 1000;
    }
}

public class BoleteriaTests
{
    [Theory]
    [InlineData(5, 500)]
    [InlineData(12, 1000)]
    [InlineData(40, 1000)]
    [InlineData(70, 600)]
    public void PrecioSegunEdad(int edad, int esperado)
    {
        Assert.Equal(esperado, new Boleteria().Precio(edad));
    }

    [Fact]
    public void EdadNegativaFalla()
    {
        Assert.Throws<ArgumentException>(() => new Boleteria().Precio(-1));
    }
}
```

## R05-N05 · La Bóveda: guardar en una base de datos

```meta
tipo: tema
padre: R05-N04
precio: 10
criatura: goblin
temas: sql.desde-codigo, sql.modelo
usa: prog.bucles, col.listas
```

### Crónica

Debajo del Archivo, más abajo todavía que el sótano del Liche, Clave abre una puerta redonda de metal. Adentro hay una sola mesa y un libro enorme, con columnas prolijas y renglones numerados.

—La **Bóveda** —dice {mentor}—. Los archivos de texto sirven para anotar. Pero cuando querés buscar una partitura entre diez mil, contarlas o cambiar una sin reescribir todo, hace falta una **base de datos**. Y le vas a hablar en su idioma: **SQL**.

### Objetivos

- Entender qué es una base de datos y una tabla.
- Conectarse a SQLite desde C# y crear una tabla.
- Guardar filas con `INSERT` y `ExecuteNonQuery`.
- Leer filas con `SELECT` y `ExecuteReader`.
- Pasar los datos con **parámetros**, nunca pegándolos en el texto del SQL.
- Pedir un solo valor con `ExecuteScalar`.

### Antes de empezar

- Bucles (Acto I) y `using` (R04-N04).

### Explicación

#### Una base de datos

Una **base de datos** guarda la información en **tablas**, como planillas: cada **columna** es un dato (título, páginas) y cada **fila**, una cosa guardada (una partitura). **SQLite** es una base de datos que vive en un solo archivo; no hay que instalar ningún servidor.

Se le habla en **SQL**, un idioma con pocas palabras:

| SQL | Qué hace |
|---|---|
| `CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, paginas INTEGER)` | crea la tabla con sus columnas |
| `INSERT INTO partituras (titulo, paginas) VALUES ('Canon', 8)` | agrega una fila |
| `SELECT titulo, paginas FROM partituras` | trae filas |
| `SELECT COUNT(*) FROM partituras` | cuenta las filas |

`INTEGER PRIMARY KEY` hace que el `id` se numere solo (1, 2, 3…); `TEXT` es texto; `NOT NULL`, que no puede quedar vacío.

#### Hablarle desde C#

```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();

var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, paginas INTEGER)";
comando.ExecuteNonQuery();
```

- `SqliteConnection` es la conexión con la base (`Data Source=` es el nombre del archivo). Hay que **abrirla** con `Open()` antes de usarla.
- `CreateCommand()` arma un **comando**; en `CommandText` va el SQL.
- `ExecuteNonQuery()` ejecuta un SQL que **no trae filas** (`CREATE`, `INSERT`…) y devuelve cuántas filas cambió.

#### Leer: `ExecuteReader`

```csharp
comando.CommandText = "SELECT titulo, paginas FROM partituras";
using var lector = comando.ExecuteReader();
while (lector.Read())
{
    Console.WriteLine($"{lector.GetString(0)}: {lector.GetInt32(1)}");
}
```

`Read()` avanza a la siguiente fila y devuelve `false` cuando no hay más. `GetString(0)` lee la primera columna como texto, `GetInt32(1)` la segunda como entero: el número es la **posición** de la columna en el `SELECT`.

#### Un solo valor: `ExecuteScalar`

`ExecuteScalar()` devuelve el primer valor de la primera fila, como `object`. SQLite guarda los enteros como `long`, así que se convierte con `Convert.ToInt32(...)`.

#### Parámetros: los datos van aparte

```csharp
comando.CommandText = "INSERT INTO partituras (titulo, paginas) VALUES ($titulo, $paginas)";
comando.Parameters.AddWithValue("$titulo", "Bolero");
comando.Parameters.AddWithValue("$paginas", 12);
comando.ExecuteNonQuery();
```

`$titulo` es un **lugar reservado**: el dato se pasa aparte con `AddWithValue`. **Nunca** se pega un dato adentro del texto del SQL: un título con una comilla (`El 'Bolero'`) rompe el SQL, y alguien malintencionado podría escribir SQL de más (eso se llama **inyección SQL**). `Parameters.Clear()` borra los parámetros para usar el comando otra vez.

#### En este curso y en una compu de verdad

Acá la Bóveda es un SQLite que corre en tu navegador, y **arranca vacía en cada ejecución**: por eso cada programa crea su tabla. En una compu, se agrega el paquete con `dotnet add package Microsoft.Data.Sqlite` (en Linux y en Windows es igual) y el archivo `boveda.db` queda guardado en la carpeta del proyecto.

### Código de ejemplo

```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();

var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, paginas INTEGER)";
comando.ExecuteNonQuery();

string[] titulos = { "Canon", "Bolero" };
int[] paginas = { 8, 12 };
comando.CommandText = "INSERT INTO partituras (titulo, paginas) VALUES ($titulo, $paginas)";
for (int i = 0; i < titulos.Length; i++)
{
    comando.Parameters.Clear();
    comando.Parameters.AddWithValue("$titulo", titulos[i]);
    comando.Parameters.AddWithValue("$paginas", paginas[i]);
    comando.ExecuteNonQuery();
}

comando.Parameters.Clear();
comando.CommandText = "SELECT id, titulo, paginas FROM partituras";
using var lector = comando.ExecuteReader();
while (lector.Read())
{
    Console.WriteLine($"{lector.GetInt32(0)}. {lector.GetString(1)} ({lector.GetInt32(2)} páginas)");
}
```

### Salida esperada

```
1. Canon (8 páginas)
2. Bolero (12 páginas)
```

### ¿Para qué sirve?

Casi todo lo que guarda datos usa una base de datos: los usuarios de una página, el inventario de un juego, las ventas de un negocio. SQLite está adentro de los celulares, de los navegadores y de muchísimos juegos.

### Errores habituales

- **Usar la conexión sin `Open()`:** salta una `InvalidOperationException` («can only be called when the connection is open»).
- **Pegar los datos en el SQL:** `"… VALUES ('" + titulo + "')"` se rompe con una comilla y deja la puerta abierta a la inyección SQL. Siempre parámetros.
- **`(int)comando.ExecuteScalar()`:** lo que vuelve es un `long` guardado en un `object`, y ese cambio de tipo falla. Usá `Convert.ToInt32(...)`.
- **Olvidar `Parameters.Clear()`:** al reusar el comando, quedan los parámetros de antes.

### Micro-misión R05-N05-P1 · Abrir la Bóveda

```meta
lugar: La Bóveda
personajes: Ceci, Clave
carta: Conexión | new SqliteConnection("Data Source=boveda.db") · Open() antes de usarla
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Ceci está frente a la puerta redonda de la Bóveda, con todo listo para guardar, pero la puerta sigue cerrada.

#### Gheco sugiere
La conexión con la base se crea con `new SqliteConnection("Data Source=archivo.db")`, pero empieza **cerrada**: antes de mandarle comandos, hay que abrirla.

```csharp
using var conexion = new SqliteConnection("Data Source=notas.db");
conexion.Open();
```

Si se usa sin abrir, salta una `InvalidOperationException`.

#### Desafío
Agregá `conexion.Open();` antes de crear el comando.

#### Código inicial
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");

var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, paginas INTEGER)";
comando.ExecuteNonQuery();
Console.WriteLine("La Bóveda está abierta");
```

#### Salida esperada
```
La Bóveda está abierta
```

#### Solución
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();

var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, paginas INTEGER)";
comando.ExecuteNonQuery();
Console.WriteLine("La Bóveda está abierta");
```

#### Al superarla
La puerta redonda gira con un ruido de engranajes y se abre. Adentro huele a papel y a metal.

#### Imagen
- Una puerta redonda de metal de bóveda, con engranajes de bronce, abriéndose en una pared de piedra iluminada por faroles azules, sin letras ni números.
- Clave gira la manija de la puerta; Ceci espera al lado con un farol.

### Micro-misión R05-N05-P2 · Guardar una partitura

```meta
lugar: La Bóveda
personajes: Ceci, Bemol
carta: INSERT | CommandText = "INSERT INTO … VALUES (…)" · ExecuteNonQuery() → cuántas filas cambió
recompensa: xp 15, oro 15
```

#### Escena
Bemol escribió el SQL para guardar el Canon, pero se olvidó de ejecutarlo. La Bóveda sigue vacía.

#### Gheco sugiere
Escribir el SQL en `CommandText` no hace nada todavía: hay que **ejecutarlo**. Para los que no traen filas (`CREATE`, `INSERT`), se usa `ExecuteNonQuery()`, que devuelve **cuántas filas cambió**:

```csharp
comando.CommandText = "INSERT INTO notas (nombre) VALUES ('do')";
int filas = comando.ExecuteNonQuery();   // 1
```

#### Desafío
Cambiá `int filas = 0;` por `int filas = comando.ExecuteNonQuery();`.

#### Código inicial
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, paginas INTEGER)";
comando.ExecuteNonQuery();

comando.CommandText = "INSERT INTO partituras (titulo, paginas) VALUES ('Canon', 8)";
int filas = 0;
Console.WriteLine($"Filas guardadas: {filas}");
```

#### Salida esperada
```
Filas guardadas: 1
```

#### Solución
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, paginas INTEGER)";
comando.ExecuteNonQuery();

comando.CommandText = "INSERT INTO partituras (titulo, paginas) VALUES ('Canon', 8)";
int filas = comando.ExecuteNonQuery();
Console.WriteLine($"Filas guardadas: {filas}");
```

#### Al superarla
En el libro enorme aparece un renglón nuevo, prolijo, como escrito por una mano invisible.

#### Imagen
- Una bóveda de piedra con faroles azules y una mesa con un libro enorme abierto de renglones lisos, sin letras.
- Bemol señala un renglón nuevo que brilla en dorado; Ceci se asoma por encima de su hombro.

### Micro-misión R05-N05-P3 · Leer la Bóveda

```meta
lugar: La Bóveda
personajes: Ceci, Clave
carta: SELECT | ExecuteReader() · while (lector.Read()) · GetString(0), GetInt32(1): por posición
recompensa: xp 15, oro 15
```

#### Escena
La Bóveda ya tiene tres partituras. Clave quiere ver la lista, pero el programa muestra el título y nada más.

#### Gheco sugiere
Para un `SELECT`, que trae filas, se usa `ExecuteReader()`. El lector arranca **antes** de la primera fila: cada `Read()` avanza una y devuelve `false` cuando no hay más.

```csharp
using var lector = comando.ExecuteReader();
while (lector.Read())
{
    Console.WriteLine(lector.GetString(0));
}
```

`GetString(0)` lee la columna 0 del `SELECT` como texto; `GetInt32(1)`, la columna 1 como entero.

#### Desafío
Recorré el lector con `while (lector.Read())` y mostrá cada partitura como `Canon: 8 páginas`.

#### Código inicial
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, paginas INTEGER);"
    + "INSERT INTO partituras (titulo, paginas) VALUES ('Canon', 8), ('Bolero', 12), ('Tango', 5);";
comando.ExecuteNonQuery();

comando.CommandText = "SELECT titulo, paginas FROM partituras";
using var lector = comando.ExecuteReader();
Console.WriteLine("Partituras en la Bóveda:");
```

#### Salida esperada
```
Partituras en la Bóveda:
Canon: 8 páginas
Bolero: 12 páginas
Tango: 5 páginas
```

#### Solución
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, paginas INTEGER);"
    + "INSERT INTO partituras (titulo, paginas) VALUES ('Canon', 8), ('Bolero', 12), ('Tango', 5);";
comando.ExecuteNonQuery();

comando.CommandText = "SELECT titulo, paginas FROM partituras";
using var lector = comando.ExecuteReader();
Console.WriteLine("Partituras en la Bóveda:");
while (lector.Read())
{
    Console.WriteLine($"{lector.GetString(0)}: {lector.GetInt32(1)} páginas");
}
```

#### Al superarla
—Ni una se perdió —dice Clave, y pasa la mano por el lomo del libro, despacito.

#### Imagen
- Una bóveda de piedra con faroles azules y estantes con partituras enrolladas, ordenadas, atadas con cintas de colores, sin letras.
- Clave recorre los estantes con la mirada; Ceci sostiene una partitura enrollada.

### Micro-misión R05-N05-P4 · La comilla traicionera

```meta
lugar: La Bóveda
personajes: Ceci, Bemol
carta: Parámetros | "… VALUES ($titulo)" · Parameters.AddWithValue("$titulo", dato) · nunca pegar datos en el SQL
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol quiere guardar una obra que se llama `El 'Bolero'`, con comillas y todo. La pega en el SQL, y la Bóveda contesta con un error.

#### Gheco sugiere
En SQL, los textos van entre comillas simples: `'Canon'`. Si el dato **tiene** una comilla, el SQL se corta en el lugar equivocado y no se entiende. Peor: alguien podría escribir un dato que sea SQL y hacer que la base haga otra cosa (**inyección SQL**).

La solución es no pegar el dato: en el SQL va un **lugar reservado** con `$`, y el dato se pasa aparte:

```csharp
comando.CommandText = "INSERT INTO notas (nombre) VALUES ($nombre)";
comando.Parameters.AddWithValue("$nombre", "la 'buena'");
```

#### Desafío
Reemplazá el `'{titulo}'` del SQL por `$titulo`, y pasá el dato con `comando.Parameters.AddWithValue("$titulo", titulo);`.

#### Código inicial
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL)";
comando.ExecuteNonQuery();

string titulo = "El 'Bolero'";
comando.CommandText = $"INSERT INTO partituras (titulo) VALUES ('{titulo}')";
comando.ExecuteNonQuery();
Console.WriteLine($"Guardada: {titulo}");
```

#### Salida esperada
```
Guardada: El 'Bolero'
```

#### Solución
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL)";
comando.ExecuteNonQuery();

string titulo = "El 'Bolero'";
comando.CommandText = "INSERT INTO partituras (titulo) VALUES ($titulo)";
comando.Parameters.AddWithValue("$titulo", titulo);
comando.ExecuteNonQuery();
Console.WriteLine($"Guardada: {titulo}");
```

#### Al superarla
—Las comillas eran parte del nombre —dice Bemol—. El compositor era muy dramático.

#### Imagen
- Una mesa de piedra en una bóveda con faroles azules, con una partitura enrollada y un sobre lacrado aparte, al lado, sin letras.
- Bemol pone el sobre al lado de la partitura con cuidado; Ceci le señala que van separados.

### Micro-misión R05-N05-P5 · El goblin del long

```meta
lugar: La Bóveda
personajes: Ceci, Gheco
criatura: goblin
carta: Goblin | ExecuteScalar() → object con un long adentro · (int) falla · Convert.ToInt32(…)
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un goblin cuenta las partituras de la Bóveda con `COUNT(*)`, pero cuando quiere guardar el número en un `int`, todo explota.

#### Gheco sugiere
`ExecuteScalar()` devuelve el primer valor de la primera fila como `object`. SQLite guarda los enteros como `long` (enteros grandes), así que adentro del `object` hay un `long`. Y un `long` guardado en un `object` **no se puede** pasar a `int` con `(int)`: salta una `InvalidCastException`.

`Convert.ToInt32(...)` sí sabe convertirlo:

```csharp
object valor = 5L;                    // un long adentro de un object
int n = Convert.ToInt32(valor);       // 5
```

#### Desafío
Cambiá `(int)comando.ExecuteScalar()!` por `Convert.ToInt32(comando.ExecuteScalar())`.

#### Código inicial
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL);"
    + "INSERT INTO partituras (titulo) VALUES ('Canon'), ('Bolero'), ('Tango');";
comando.ExecuteNonQuery();

comando.CommandText = "SELECT COUNT(*) FROM partituras";
int total = (int)comando.ExecuteScalar()!;
Console.WriteLine($"Partituras: {total}");
```

#### Salida esperada
```
Partituras: 3
```

#### Solución
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL);"
    + "INSERT INTO partituras (titulo) VALUES ('Canon'), ('Bolero'), ('Tango');";
comando.ExecuteNonQuery();

comando.CommandText = "SELECT COUNT(*) FROM partituras";
int total = Convert.ToInt32(comando.ExecuteScalar());
Console.WriteLine($"Partituras: {total}");
```

#### Al superarla
El goblin cuenta de nuevo con los dedos, llega a tres, y se va contento a buscar algo más grande que contar.

#### Imagen
- Una bóveda de piedra con faroles azules, con tres partituras enrolladas sobre una mesa y una caja de madera grande abierta al lado, sin letras.
- Un goblin chico de orejas puntiagudas intenta meter una partitura en una cajita demasiado chica; Gheco, parado solo sobre la mesa, le señala la caja grande.

### Encargo R05-N05-E1 · El catálogo de Hulda

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Hulda, la de las Forjas, quiere el catálogo de sus herramientas en una base de datos. Creá la tabla `herramientas` (con `id INTEGER PRIMARY KEY`, `nombre TEXT NOT NULL` y `precio INTEGER`). Leé líneas como `nombre,precio` hasta una línea vacía y guardá cada una con un `INSERT` **con parámetros**. Después, mostrá todas con `SELECT nombre, precio FROM herramientas ORDER BY precio DESC` (`ORDER BY precio DESC` las ordena de la más cara a la más barata) y, al final, cuántas hay con `SELECT COUNT(*)` y `ExecuteScalar`.

Con esta entrada:

```
Martillo,1200
Tenaza,800
Yunque,9000

```

se muestra:

```
Yunque: $9000
Martillo: $1200
Tenaza: $800
Herramientas: 3
```

#### Criterio de aprobación

- Guarda con `INSERT` y parámetros (`$nombre`, `$precio`), sin pegar los datos en el SQL.
- Lee con `ExecuteReader` y cuenta con `ExecuteScalar`.

#### Entrada de ejemplo

```
Martillo,1200
Tenaza,800
Yunque,9000

```

#### Salida esperada

```
Yunque: $9000
Martillo: $1200
Tenaza: $800
Herramientas: 3
```

#### Solución de referencia

```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=forjas.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE herramientas (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, precio INTEGER)";
comando.ExecuteNonQuery();

comando.CommandText = "INSERT INTO herramientas (nombre, precio) VALUES ($nombre, $precio)";
string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    string[] partes = linea.Split(',');
    comando.Parameters.Clear();
    comando.Parameters.AddWithValue("$nombre", partes[0]);
    comando.Parameters.AddWithValue("$precio", int.Parse(partes[1]));
    comando.ExecuteNonQuery();
    linea = Console.ReadLine();
}

comando.Parameters.Clear();
comando.CommandText = "SELECT nombre, precio FROM herramientas ORDER BY precio DESC";
using (var lector = comando.ExecuteReader())
{
    while (lector.Read())
    {
        Console.WriteLine($"{lector.GetString(0)}: ${lector.GetInt32(1)}");
    }
}

comando.CommandText = "SELECT COUNT(*) FROM herramientas";
Console.WriteLine($"Herramientas: {Convert.ToInt32(comando.ExecuteScalar())}");
```

## R05-N06 · Buscar, cambiar, borrar: todo o nada

```meta
tipo: tema
padre: R05-N05
precio: 10
criatura: ogro
temas: sql.abm, sql.transacciones, sql.consultas
usa: sql.desde-codigo
```

### Crónica

En la Bóveda también se guardan las **corcheas** de cada alumno. Un día, Ceci le paga 30 a Bemol por unas cuerdas. Las corcheas salen de su cuenta… y nunca llegan a la de Bemol: alguien escribió mal su nombre. Treinta corcheas se evaporaron en el aire.

—Un pago tiene dos partes —dice {mentor}—: sacar de un lado y poner en el otro. O pasan **las dos**, o **ninguna**. Para eso, la Bóveda tiene transacciones.

### Objetivos

- Buscar filas con `WHERE` y un parámetro.
- Cambiar filas con `UPDATE` y borrarlas con `DELETE`, siempre con `WHERE`.
- Usar lo que devuelve `ExecuteNonQuery` para saber si encontró algo.
- Agrupar cambios en una **transacción**: `BeginTransaction`, `Commit` y `Rollback`.

### Antes de empezar

- La Bóveda (R05-N05) y excepciones (R04-N01 y R04-N02).

### Explicación

#### Buscar: `WHERE`

`WHERE` («donde») filtra las filas: solo vienen las que cumplen la condición.

```sql
SELECT titulo, paginas FROM partituras WHERE paginas >= $minimo
SELECT titulo FROM partituras WHERE titulo = $titulo
```

Las comparaciones son como en C#, salvo que «igual» es un solo `=` y «distinto» es `<>`. `ORDER BY titulo` las ordena.

#### Cambiar y borrar

```sql
UPDATE partituras SET paginas = $paginas WHERE id = $id
DELETE FROM partituras WHERE id = $id
```

`UPDATE … SET` cambia columnas; `DELETE` borra filas. **Sin `WHERE`, cambian o borran todas.**

Los dos se ejecutan con `ExecuteNonQuery()`, que devuelve **cuántas filas tocó**. Si devuelve `0`, no había ninguna que cumpliera el `WHERE`.

#### Todo o nada: transacciones

Un pago son dos `UPDATE`. Si el primero pasa y el segundo falla, el dinero desaparece. Una **transacción** agrupa varios cambios para que pasen todos juntos o ninguno:

```csharp
using var transaccion = conexion.BeginTransaction();
comando.Transaction = transaccion;
try
{
    // … varios ExecuteNonQuery …
    transaccion.Commit();      // confirmo: ahora sí queda todo
}
catch (InvalidOperationException)
{
    transaccion.Rollback();    // deshago todo lo de la transacción
}
```

- `BeginTransaction()` empieza la transacción; el comando la usa con `comando.Transaction = transaccion;`.
- `Commit()` confirma los cambios.
- `Rollback()` los deshace, como si nunca hubieran pasado.
- Si la transacción se cierra sin `Commit()`, se deshace sola.
- Cuando termina, el comando la suelta con `comando.Transaction = null;` para seguir usándolo.

### Código de ejemplo

```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, paginas INTEGER);"
    + "INSERT INTO partituras (titulo, paginas) VALUES ('Canon', 8), ('Bolero', 12), ('Tango', 5);";
comando.ExecuteNonQuery();

comando.CommandText = "UPDATE partituras SET paginas = $paginas WHERE titulo = $titulo";
comando.Parameters.AddWithValue("$paginas", 6);
comando.Parameters.AddWithValue("$titulo", "Tango");
Console.WriteLine($"Cambiadas: {comando.ExecuteNonQuery()}");

comando.Parameters.Clear();
comando.CommandText = "SELECT titulo, paginas FROM partituras WHERE paginas >= $minimo ORDER BY titulo";
comando.Parameters.AddWithValue("$minimo", 6);
using var lector = comando.ExecuteReader();
while (lector.Read())
{
    Console.WriteLine($"{lector.GetString(0)}: {lector.GetInt32(1)}");
}
```

### Salida esperada

```
Cambiadas: 1
Bolero: 12
Canon: 8
Tango: 6
```

### ¿Para qué sirve?

Así funcionan un banco, una tienda o el inventario de un juego: buscar un producto, cambiarle el precio, borrar lo que ya no está. Y cualquier cosa que tenga dos partes (pagar y cobrar, sacar de la mochila y poner en el cofre) va en una transacción, para que nunca quede a medias.

### Errores habituales

- **`UPDATE` o `DELETE` sin `WHERE`:** cambian o borran **toda** la tabla.
- **No mirar lo que devuelve `ExecuteNonQuery`:** si dio `0`, no se cambió nada, aunque no haya salido ningún error.
- **Olvidar el `Commit()`:** al cerrar la transacción sin confirmar, todo se deshace.
- **`=` contra `>=`:** «diez o más» es `>= 10`; `> 10` deja afuera al diez.

### Micro-misión R05-N06-P1 · Buscar una partitura

```meta
lugar: La Bóveda
personajes: Ceci, Clave
carta: WHERE | SELECT … FROM … WHERE titulo = $titulo · solo las filas que cumplen
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Clave pide el Bolero, y Ceci le trae la Bóveda entera.

#### Gheco sugiere
`WHERE` filtra las filas: solo vienen las que cumplen la condición. El dato que se busca va como parámetro:

```csharp
comando.CommandText = "SELECT nombre FROM notas WHERE octava = $octava";
comando.Parameters.AddWithValue("$octava", 4);
```

En SQL, «igual» se escribe con un solo `=`.

#### Desafío
Agregale al `SELECT` un `WHERE titulo = $titulo` y pasá `"Bolero"` como parámetro `$titulo`.

#### Código inicial
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, paginas INTEGER);"
    + "INSERT INTO partituras (titulo, paginas) VALUES ('Canon', 8), ('Bolero', 12), ('Tango', 5);";
comando.ExecuteNonQuery();

comando.CommandText = "SELECT id, titulo, paginas FROM partituras";
using var lector = comando.ExecuteReader();
while (lector.Read())
{
    Console.WriteLine($"{lector.GetInt32(0)}. {lector.GetString(1)} ({lector.GetInt32(2)} páginas)");
}
```

#### Salida esperada
```
2. Bolero (12 páginas)
```

#### Solución
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, paginas INTEGER);"
    + "INSERT INTO partituras (titulo, paginas) VALUES ('Canon', 8), ('Bolero', 12), ('Tango', 5);";
comando.ExecuteNonQuery();

comando.CommandText = "SELECT id, titulo, paginas FROM partituras WHERE titulo = $titulo";
comando.Parameters.AddWithValue("$titulo", "Bolero");
using var lector = comando.ExecuteReader();
while (lector.Read())
{
    Console.WriteLine($"{lector.GetInt32(0)}. {lector.GetString(1)} ({lector.GetInt32(2)} páginas)");
}
```

#### Al superarla
—Esa —dice Clave—. Una sola. No te pedí que me mudaras la Bóveda.

#### Imagen
- Una bóveda de piedra con faroles azules y estantes con partituras enrolladas, con una sola partitura que brilla en dorado en un estante, sin letras.
- Ceci saca la partitura que brilla; Clave espera con la mano extendida.

### Micro-misión R05-N06-P2 · Cambiar una, no todas

```meta
lugar: La Bóveda
personajes: Ceci, Bemol
carta: UPDATE | UPDATE … SET … WHERE id = $id · sin WHERE, cambian TODAS
recompensa: xp 15, oro 15
```

#### Escena
Bemol corrige las páginas del Tango: tiene 6, no 5. Pero después de su cambio, todas las partituras de la Bóveda tienen 6 páginas.

#### Gheco sugiere
`UPDATE … SET` cambia columnas de las filas… de **todas**, si no le decís cuáles. El `WHERE` elige las filas que se cambian:

```csharp
comando.CommandText = "UPDATE notas SET octava = $octava WHERE nombre = $nombre";
```

`ExecuteNonQuery()` devuelve cuántas filas cambió: acá tendría que ser una sola.

#### Desafío
Agregale al `UPDATE` un `WHERE titulo = $titulo` y pasá `"Tango"` como parámetro.

#### Código inicial
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, paginas INTEGER);"
    + "INSERT INTO partituras (titulo, paginas) VALUES ('Canon', 8), ('Bolero', 12), ('Tango', 5);";
comando.ExecuteNonQuery();

comando.CommandText = "UPDATE partituras SET paginas = $paginas";
comando.Parameters.AddWithValue("$paginas", 6);
Console.WriteLine($"Cambiadas: {comando.ExecuteNonQuery()}");

comando.Parameters.Clear();
comando.CommandText = "SELECT titulo, paginas FROM partituras";
using var lector = comando.ExecuteReader();
while (lector.Read())
{
    Console.WriteLine($"{lector.GetString(0)}: {lector.GetInt32(1)}");
}
```

#### Salida esperada
```
Cambiadas: 1
Canon: 8
Bolero: 12
Tango: 6
```

#### Solución
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, paginas INTEGER);"
    + "INSERT INTO partituras (titulo, paginas) VALUES ('Canon', 8), ('Bolero', 12), ('Tango', 5);";
comando.ExecuteNonQuery();

comando.CommandText = "UPDATE partituras SET paginas = $paginas WHERE titulo = $titulo";
comando.Parameters.AddWithValue("$paginas", 6);
comando.Parameters.AddWithValue("$titulo", "Tango");
Console.WriteLine($"Cambiadas: {comando.ExecuteNonQuery()}");

comando.Parameters.Clear();
comando.CommandText = "SELECT titulo, paginas FROM partituras";
using var lector = comando.ExecuteReader();
while (lector.Read())
{
    Console.WriteLine($"{lector.GetString(0)}: {lector.GetInt32(1)}");
}
```

#### Al superarla
Bemol respira aliviado. El Bolero sigue teniendo sus doce páginas, una por una.

#### Imagen
- Una bóveda de piedra con faroles azules y una mesa con tres partituras enrolladas de distinto grosor, sin letras.
- Bemol sostiene una goma de borrar gigante con cara de culpa; Ceci le señala una sola de las partituras.

### Micro-misión R05-N06-P3 · ¿Estaba o no estaba?

```meta
lugar: La Bóveda
personajes: Ceci, Don Cedro
carta: Filas tocadas | int filas = ExecuteNonQuery() · 0 → no había ninguna así
recompensa: xp 15, oro 15
```

#### Escena
Don Cedro borra de la Bóveda los instrumentos que ya vendió. Pero el programa dice «Borrado» incluso con uno que nunca estuvo.

#### Gheco sugiere
`DELETE FROM … WHERE …` borra las filas que cumplen el `WHERE`. Si no hay ninguna, no es un error: simplemente no borra nada, y `ExecuteNonQuery()` devuelve `0`.

```csharp
int filas = comando.ExecuteNonQuery();
if (filas == 0)
{
    Console.WriteLine("No había nada para borrar");
}
```

#### Desafío
Guardá lo que devuelve `ExecuteNonQuery()` en `int filas`, y mostrá `Borrado: ` o `No estaba: ` según si es mayor que cero.

#### Código inicial
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE instrumentos (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL);"
    + "INSERT INTO instrumentos (nombre) VALUES ('violín'), ('viola');";
comando.ExecuteNonQuery();

comando.CommandText = "DELETE FROM instrumentos WHERE nombre = $nombre";
foreach (string vendido in new[] { "viola", "arpa" })
{
    comando.Parameters.Clear();
    comando.Parameters.AddWithValue("$nombre", vendido);
    comando.ExecuteNonQuery();
    Console.WriteLine($"Borrado: {vendido}");
}
```

#### Salida esperada
```
Borrado: viola
No estaba: arpa
```

#### Solución
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE instrumentos (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL);"
    + "INSERT INTO instrumentos (nombre) VALUES ('violín'), ('viola');";
comando.ExecuteNonQuery();

comando.CommandText = "DELETE FROM instrumentos WHERE nombre = $nombre";
foreach (string vendido in new[] { "viola", "arpa" })
{
    comando.Parameters.Clear();
    comando.Parameters.AddWithValue("$nombre", vendido);
    int filas = comando.ExecuteNonQuery();
    if (filas > 0)
    {
        Console.WriteLine($"Borrado: {vendido}");
    }
    else
    {
        Console.WriteLine($"No estaba: {vendido}");
    }
}
```

#### Al superarla
—¿Un arpa? —dice Don Cedro—. Nunca tuve un arpa. Aunque, pensándolo bien, me gustaría.

#### Imagen
- Un taller de luthier de madera cálida con velas y una pared con ganchos, uno con una viola colgada y otro vacío, sin letras.
- Don Cedro descuelga la viola; Ceci mira el gancho vacío con curiosidad.

### Micro-misión R05-N06-P4 · Todo o nada

```meta
lugar: La Bóveda
personajes: Ceci, Bemol
carta: Transacción | BeginTransaction() · comando.Transaction = t · Commit() si salió todo · Rollback() si algo falló
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Ceci le paga 30 corcheas a Bemol, pero en el pago alguien escribió `Bemoll`. Las corcheas salen de la cuenta de Ceci y no llegan a ningún lado.

#### Gheco sugiere
Un pago son dos cambios: restar y sumar. Si el segundo falla, el primero ya pasó. Una **transacción** los agrupa: o pasan los dos, o ninguno.

```csharp
using var transaccion = conexion.BeginTransaction();
comando.Transaction = transaccion;
try
{
    // … los cambios …
    transaccion.Commit();
}
catch (InvalidOperationException)
{
    transaccion.Rollback();
}
```

`Commit()` confirma todo; `Rollback()` deshace todo lo que se hizo desde `BeginTransaction()`.

#### Desafío
Empezá una transacción antes del `try` (`using var transaccion = conexion.BeginTransaction();` y `comando.Transaction = transaccion;`), confirmala con `transaccion.Commit();` al final del `try`, y deshacela con `transaccion.Rollback();` en el `catch`.

#### Código inicial
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE cuentas (nombre TEXT PRIMARY KEY, corcheas INTEGER);"
    + "INSERT INTO cuentas VALUES ('Ceci', 100), ('Bemol', 50);";
comando.ExecuteNonQuery();

try
{
    comando.CommandText = "UPDATE cuentas SET corcheas = corcheas - 30 WHERE nombre = 'Ceci'";
    comando.ExecuteNonQuery();
    comando.CommandText = "UPDATE cuentas SET corcheas = corcheas + 30 WHERE nombre = 'Bemoll'";
    if (comando.ExecuteNonQuery() == 0)
    {
        throw new InvalidOperationException("no existe la cuenta Bemoll");
    }
    Console.WriteLine("Pago hecho");
}
catch (InvalidOperationException e)
{
    Console.WriteLine($"Pago cancelado: {e.Message}");
}

comando.CommandText = "SELECT nombre, corcheas FROM cuentas ORDER BY nombre";
using var lector = comando.ExecuteReader();
while (lector.Read())
{
    Console.WriteLine($"{lector.GetString(0)}: {lector.GetInt32(1)}");
}
```

#### Salida esperada
```
Pago cancelado: no existe la cuenta Bemoll
Bemol: 50
Ceci: 100
```

#### Solución
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE cuentas (nombre TEXT PRIMARY KEY, corcheas INTEGER);"
    + "INSERT INTO cuentas VALUES ('Ceci', 100), ('Bemol', 50);";
comando.ExecuteNonQuery();

using var transaccion = conexion.BeginTransaction();
comando.Transaction = transaccion;
try
{
    comando.CommandText = "UPDATE cuentas SET corcheas = corcheas - 30 WHERE nombre = 'Ceci'";
    comando.ExecuteNonQuery();
    comando.CommandText = "UPDATE cuentas SET corcheas = corcheas + 30 WHERE nombre = 'Bemoll'";
    if (comando.ExecuteNonQuery() == 0)
    {
        throw new InvalidOperationException("no existe la cuenta Bemoll");
    }
    transaccion.Commit();
    Console.WriteLine("Pago hecho");
}
catch (InvalidOperationException e)
{
    transaccion.Rollback();
    Console.WriteLine($"Pago cancelado: {e.Message}");
}
comando.Transaction = null;

comando.CommandText = "SELECT nombre, corcheas FROM cuentas ORDER BY nombre";
using var lector = comando.ExecuteReader();
while (lector.Read())
{
    Console.WriteLine($"{lector.GetString(0)}: {lector.GetInt32(1)}");
}
```

#### Al superarla
Las treinta corcheas vuelven a la cuenta de Ceci como si nunca se hubieran ido. Bemol, igual, le pide que le pague de nuevo, «pero bien escrito».

#### Imagen
- Una bóveda de piedra con faroles azules y una balanza de bronce sobre la mesa con monedas doradas lisas volviendo por el aire a un platillo, sin letras ni números.
- Ceci mira cómo vuelven las monedas; Bemol se rasca la cabeza.

### Micro-misión R05-N06-P5 · El ogro del diez

```meta
lugar: La Bóveda
personajes: Ceci, Gheco
criatura: ogro
carta: Ogro | «10 o más» es >= 10 · > 10 deja afuera al diez
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un ogro tiene que llevar al escenario las partituras de **diez páginas o más**. Se lleva una sola: dejó la de diez en la Bóveda.

#### Gheco sugiere
En SQL, las comparaciones son como en C#: `>` es «mayor que», y `>=` es «mayor **o igual**». «Diez o más» incluye al diez, así que es `>= 10`.

El programa no tiene errores: corre y da otra cosa. Eso es un error de **lógica**.

#### Desafío
Cambiá el `>` del `WHERE` por `>=`.

#### Código inicial
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, paginas INTEGER);"
    + "INSERT INTO partituras (titulo, paginas) VALUES ('Canon', 8), ('Bolero', 12), ('Vals', 10);";
comando.ExecuteNonQuery();

comando.CommandText = "SELECT titulo FROM partituras WHERE paginas > $minimo ORDER BY titulo";
comando.Parameters.AddWithValue("$minimo", 10);
using var lector = comando.ExecuteReader();
while (lector.Read())
{
    Console.WriteLine($"Al escenario: {lector.GetString(0)}");
}
```

#### Salida esperada
```
Al escenario: Bolero
Al escenario: Vals
```

#### Solución
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE partituras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, paginas INTEGER);"
    + "INSERT INTO partituras (titulo, paginas) VALUES ('Canon', 8), ('Bolero', 12), ('Vals', 10);";
comando.ExecuteNonQuery();

comando.CommandText = "SELECT titulo FROM partituras WHERE paginas >= $minimo ORDER BY titulo";
comando.Parameters.AddWithValue("$minimo", 10);
using var lector = comando.ExecuteReader();
while (lector.Read())
{
    Console.WriteLine($"Al escenario: {lector.GetString(0)}");
}
```

#### Al superarla
El ogro vuelve por el Vals, lo lleva abrazado como si fuera un bebé y lo deja en el atril con muchísimo cuidado.

#### Imagen
- Una bóveda de piedra con faroles azules y un estante con partituras enrolladas, con un hueco donde falta una, sin letras.
- El ogro grandote lleva dos partituras abrazadas; Gheco, parado solo sobre el estante, le señala la que dejó.

### Encargo R05-N06-E1 · El banco del Gremio

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

El Gremio guarda las corcheas de sus miembros. Creá la tabla con `CREATE TABLE cuentas (nombre TEXT PRIMARY KEY, corcheas INTEGER CHECK (corcheas >= 0))` (el `CHECK` hace que la Bóveda rechace un saldo negativo con una `SqliteException`) y cargá a Ceci con 100, a Bemol con 50 y a Clave con 80.

Leé pagos como `de,a,monto` hasta una línea vacía. Cada pago va en **una transacción**: restale al que paga, sumale al que cobra, y si la cuenta que cobra no existe (`ExecuteNonQuery` devuelve `0`), lanzá una `InvalidOperationException`. Si sale bien, confirmá y mostrá `Hecho: de → a (monto)`; si falla cualquier cosa (atrapá `Exception`), deshacé y mostrá `Rechazado: de → a`. Al final, mostrá las cuentas ordenadas por nombre.

Con esta entrada:

```
Ceci,Bemol,30
Bemol,Clave,500
Clave,Nadie,10

```

se muestra:

```
Hecho: Ceci → Bemol (30)
Rechazado: Bemol → Clave
Rechazado: Clave → Nadie
Bemol: 80
Ceci: 70
Clave: 80
```

#### Criterio de aprobación

- Cada pago usa `BeginTransaction`, `Commit` si salió bien y `Rollback` si falló.
- Los datos van con parámetros; un pago rechazado no cambia ninguna cuenta.

#### Entrada de ejemplo

```
Ceci,Bemol,30
Bemol,Clave,500
Clave,Nadie,10

```

#### Salida esperada

```
Hecho: Ceci → Bemol (30)
Rechazado: Bemol → Clave
Rechazado: Clave → Nadie
Bemol: 80
Ceci: 70
Clave: 80
```

#### Solución de referencia

```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=gremio.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE cuentas (nombre TEXT PRIMARY KEY, corcheas INTEGER CHECK (corcheas >= 0));"
    + "INSERT INTO cuentas VALUES ('Ceci', 100), ('Bemol', 50), ('Clave', 80);";
comando.ExecuteNonQuery();

string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    string[] p = linea.Split(',');
    string de = p[0];
    string a = p[1];
    int monto = int.Parse(p[2]);

    using (var transaccion = conexion.BeginTransaction())
    {
        comando.Transaction = transaccion;
        try
        {
            comando.Parameters.Clear();
            comando.Parameters.AddWithValue("$nombre", de);
            comando.Parameters.AddWithValue("$monto", monto);
            comando.CommandText = "UPDATE cuentas SET corcheas = corcheas - $monto WHERE nombre = $nombre";
            comando.ExecuteNonQuery();

            comando.Parameters.Clear();
            comando.Parameters.AddWithValue("$nombre", a);
            comando.Parameters.AddWithValue("$monto", monto);
            comando.CommandText = "UPDATE cuentas SET corcheas = corcheas + $monto WHERE nombre = $nombre";
            if (comando.ExecuteNonQuery() == 0)
            {
                throw new InvalidOperationException($"no existe {a}");
            }

            transaccion.Commit();
            Console.WriteLine($"Hecho: {de} → {a} ({monto})");
        }
        catch (Exception)
        {
            transaccion.Rollback();
            Console.WriteLine($"Rechazado: {de} → {a}");
        }
    }
    comando.Transaction = null;
    linea = Console.ReadLine();
}

comando.Parameters.Clear();
comando.CommandText = "SELECT nombre, corcheas FROM cuentas ORDER BY nombre";
using var lector = comando.ExecuteReader();
while (lector.Read())
{
    Console.WriteLine($"{lector.GetString(0)}: {lector.GetInt32(1)}");
}
```

## R05-N07 · La ventanilla: una API web

```meta
tipo: tema
padre: R05-N06
precio: 10
criatura: goblin
temas: web.api-rest, web.http
usa: conc.async, col.listas, poo.records
```

### Crónica

Los pedidos ya no llegan solo en cartas. Nima quiere que el Teatro de la Feria le pregunte al Conservatorio, **solo**, qué partituras hay; Elefa, desde el Puerto, quiere encargarlas sin mandar a nadie. Programas que le hablan a otros programas.

—Entonces la ventanilla tiene que aprender a contestar sola —dice {mentor}—. Pedido que llega por una **ruta**, respuesta con un **código** y los datos en **JSON**. Eso es una **API**.

La campanilla de la ventanilla suena tres veces. Del otro lado del vidrio, algo se ríe.

### Objetivos

- Entender qué es una API web: pedidos, rutas, verbos y códigos de respuesta.
- Armar una ventanilla con `WebApplication` y atender rutas con `MapGet`.
- Devolver datos (que salen en JSON) y códigos como `404` con `Results`.
- Recibir datos con `MapPost` y validarlos.
- Hacerle pedidos con un `HttpClient`.

### Antes de empezar

- `async` y `await` (R05-N01), listas (R03-N01) y `record` (R02-N06).

### Explicación

#### Pedido y respuesta

Una **API web** es un programa que atiende **pedidos** de otros programas. Cada pedido tiene:

- un **verbo**: `GET` para pedir algo, `POST` para mandar algo nuevo (también hay `PUT` para cambiar y `DELETE` para borrar);
- una **ruta**: `/instrumentos`, `/instrumentos/2`;
- a veces, un **cuerpo** con datos (en `POST`).

Y cada respuesta tiene un **código** y, a veces, datos en **JSON**:

| Código | Quiere decir |
|---|---|
| `200` | bien, acá está |
| `201` | creado |
| `400` | el pedido vino mal |
| `404` | eso no existe |
| `405` | esa ruta existe, pero no con ese verbo |
| `500` | se rompió algo adentro de la API |

#### La ventanilla en C#

```csharp
var app = WebApplication.CreateBuilder(args).Build();

app.MapGet("/hola", () => "Hola desde el Conservatorio");
app.MapGet("/instrumentos", () => instrumentos);
```

`MapGet(ruta, qué hacer)` dice: cuando llegue un `GET` a esa ruta, corré esa lambda y contestá con lo que devuelve. Si devuelve un texto, va tal cual; si devuelve un objeto o una lista, sale **en JSON** con código `200`.

#### Partes de la ruta: `{id}`

```csharp
app.MapGet("/instrumentos/{id}", (int id) =>
{
    var i = instrumentos.FirstOrDefault(x => x.Id == id);
    return i is null ? Results.NotFound() : Results.Ok(i);
});
```

`{id}` es una parte que cambia: en `/instrumentos/2`, `id` vale `2`, y llega como parámetro de la lambda. `Results.Ok(…)` contesta `200` con datos; `Results.NotFound()`, `404`.

#### Recibir datos: `MapPost`

```csharp
app.MapPost("/pedidos", (Pedido p) =>
{
    if (p.Cantidad <= 0) return Results.BadRequest("La cantidad tiene que ser mayor que cero");
    pedidos.Add(p);
    return Results.Created($"/pedidos/{p.Id}", p);
});
```

El JSON que llega en el cuerpo se convierte solo en un `Pedido`. `Results.Created` contesta `201`; `Results.BadRequest`, `400`.

#### Hablarle: un `HttpClient`

En una compu, `app.Run();` abre la ventanilla en `http://localhost:5000` y se le puede hablar desde el navegador o desde otro programa. **En el navegador no hay red**, así que en este curso se le habla con `app.CreateClient()`: un `HttpClient` de verdad que le lleva los pedidos directo a la ventanilla (así se prueban las APIs en ASP.NET).

```csharp
var cliente = app.CreateClient();
var r = await cliente.GetAsync("/instrumentos/2");
Console.WriteLine((int)r.StatusCode);                    // 200
Console.WriteLine(await r.Content.ReadAsStringAsync());  // {"id":2,"nombre":"viola"}
```

- `GetAsync(ruta)` hace un `GET`; `PostAsJsonAsync(ruta, objeto)`, un `POST` con el objeto en JSON.
- `(int)r.StatusCode` es el código; `r.Content.ReadAsStringAsync()`, el cuerpo como texto.

En las micro-misiones, una función `PedirAsync` ya escrita hace el pedido y muestra la ruta, el código y el cuerpo.

#### En una compu de verdad

`dotnet new web -o Ventanilla` crea el proyecto (en Linux y en Windows es igual), y `dotnet run` la abre. Los nombres del JSON salen en minúscula (`"nombre"`), como se acostumbra en la web.

### Código de ejemplo

```csharp
var app = WebApplication.CreateBuilder(args).Build();
var instrumentos = new List<Instrumento> { new(1, "violín", 4), new(2, "viola", 4) };

app.MapGet("/instrumentos", () => instrumentos);
app.MapGet("/instrumentos/{id}", (int id) =>
{
    var i = instrumentos.FirstOrDefault(x => x.Id == id);
    return i is null ? Results.NotFound() : Results.Ok(i);
});

var cliente = app.CreateClient();
foreach (string ruta in new[] { "/instrumentos", "/instrumentos/2", "/instrumentos/9" })
{
    var r = await cliente.GetAsync(ruta);
    string cuerpo = await r.Content.ReadAsStringAsync();
    Console.WriteLine($"GET {ruta} → {(int)r.StatusCode} {cuerpo}".TrimEnd());
}

record Instrumento(int Id, string Nombre, int Cuerdas);
```

### Salida esperada

```
GET /instrumentos → 200 [{"id":1,"nombre":"violín","cuerdas":4},{"id":2,"nombre":"viola","cuerdas":4}]
GET /instrumentos/2 → 200 {"id":2,"nombre":"viola","cuerdas":4}
GET /instrumentos/9 → 404
```

### ¿Para qué sirve?

Casi todas las apps del celular le hablan a una API: el clima, los mensajes, las compras. Los juegos en línea guardan las partidas en una API; las páginas web traen sus datos de una API. Escribir una es escribir la parte del programa que **atiende** a todos los demás.

### Errores habituales

- **La ruta mal escrita:** `/instrumento` y `/instrumentos` son rutas distintas. Si no coincide, contesta `404`.
- **Devolver `null` en vez de `Results.NotFound()`:** el que pregunta recibe un `200` vacío y cree que salió bien.
- **No validar lo que llega:** cualquiera puede mandar cualquier cosa. Si el dato no sirve, `Results.BadRequest(...)`.
- **Atender con `MapGet` lo que llega con `POST`:** la ruta existe, pero con otro verbo: `405`.

### Micro-misión R05-N07-P1 · La primera ruta

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Clave
carta: MapGet | app.MapGet("/ruta", () => lo que contesta) · si nadie atiende esa ruta → 404
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Desde la Feria, el Teatro le pregunta a la ventanilla `/hola`. Nadie contesta: no hay ninguna ruta.

#### Gheco sugiere
`app.MapGet(ruta, lambda)` atiende los `GET` que llegan a esa ruta: corre la lambda y contesta con lo que devuelve.

```csharp
app.MapGet("/precio", () => "Mil corcheas");
```

Si llega un pedido a una ruta que nadie atiende, la ventanilla contesta `404`: no existe.

#### Desafío
Agregá una ruta `/hola` que conteste `Hola desde el Conservatorio`.

#### Código inicial
```csharp
var app = WebApplication.CreateBuilder(args).Build();

var cliente = app.CreateClient();
async Task PedirAsync(string ruta)
{
    var r = await cliente.GetAsync(ruta);
    string cuerpo = await r.Content.ReadAsStringAsync();
    Console.WriteLine($"GET {ruta} → {(int)r.StatusCode} {cuerpo}".TrimEnd());
}

await PedirAsync("/hola");
```

#### Salida esperada
```
GET /hola → 200 Hola desde el Conservatorio
```

#### Solución
```csharp
var app = WebApplication.CreateBuilder(args).Build();
app.MapGet("/hola", () => "Hola desde el Conservatorio");

var cliente = app.CreateClient();
async Task PedirAsync(string ruta)
{
    var r = await cliente.GetAsync(ruta);
    string cuerpo = await r.Content.ReadAsStringAsync();
    Console.WriteLine($"GET {ruta} → {(int)r.StatusCode} {cuerpo}".TrimEnd());
}

await PedirAsync("/hola");
```

#### Al superarla
—Contestó sola —dice Clave, y mira la ventanilla como si fuera la primera vez que la ve.

#### Imagen
- La ventanilla de madera de un conservatorio gótico con un tubo de bronce que sale de la pared, por donde llega un sobre de papel liso volando, con faroles, sin letras.
- Clave recibe el sobre; Ceci se asoma por el tubo, curiosa.

### Micro-misión R05-N07-P2 · La lista en JSON

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Bemol
carta: Devolver datos | si la lambda devuelve una lista u objeto · sale en JSON · con código 200
recompensa: xp 15, oro 15
```

#### Escena
El Teatro pide la lista de instrumentos, pero la ventanilla contesta solo cuántos son: un `3`, y nada más.

#### Gheco sugiere
Lo que devuelve la lambda es lo que contesta la ventanilla. Si devuelve un número, contesta el número. Si devuelve una **lista** o un **objeto**, lo convierte a **JSON**:

```csharp
app.MapGet("/notas", () => new List<string> { "do", "re" });   // ["do","re"]
```

Los nombres de los datos salen en minúscula, como se acostumbra en la web.

#### Desafío
Hacé que `/instrumentos` devuelva la lista `instrumentos` entera, no su `Count`.

#### Código inicial
```csharp
var app = WebApplication.CreateBuilder(args).Build();
var instrumentos = new List<Instrumento> { new(1, "violín", 4), new(2, "viola", 4), new(3, "guitarra", 6) };
app.MapGet("/instrumentos", () => instrumentos.Count);

var cliente = app.CreateClient();
async Task PedirAsync(string ruta)
{
    var r = await cliente.GetAsync(ruta);
    string cuerpo = await r.Content.ReadAsStringAsync();
    Console.WriteLine($"GET {ruta} → {(int)r.StatusCode} {cuerpo}".TrimEnd());
}

await PedirAsync("/instrumentos");

record Instrumento(int Id, string Nombre, int Cuerdas);
```

#### Salida esperada
```
GET /instrumentos → 200 [{"id":1,"nombre":"violín","cuerdas":4},{"id":2,"nombre":"viola","cuerdas":4},{"id":3,"nombre":"guitarra","cuerdas":6}]
```

#### Solución
```csharp
var app = WebApplication.CreateBuilder(args).Build();
var instrumentos = new List<Instrumento> { new(1, "violín", 4), new(2, "viola", 4), new(3, "guitarra", 6) };
app.MapGet("/instrumentos", () => instrumentos);

var cliente = app.CreateClient();
async Task PedirAsync(string ruta)
{
    var r = await cliente.GetAsync(ruta);
    string cuerpo = await r.Content.ReadAsStringAsync();
    Console.WriteLine($"GET {ruta} → {(int)r.StatusCode} {cuerpo}".TrimEnd());
}

await PedirAsync("/instrumentos");

record Instrumento(int Id, string Nombre, int Cuerdas);
```

#### Al superarla
En la Feria, un cartel del Teatro se llena solo con los instrumentos del Conservatorio. Bemol jura que se le escucha el violín desde acá.

#### Imagen
- La ventanilla de madera de un conservatorio gótico con un rollo de papel liso que sale por el tubo de bronce, desenrollándose largo hasta el piso, con faroles, sin letras.
- Bemol sostiene la punta del rollo con los ojos muy abiertos; Ceci lo ayuda a enrollarlo.

### Micro-misión R05-N07-P3 · El que no existe

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Clave
carta: {id} y 404 | "/instrumentos/{id}" · (int id) => … · i is null ? Results.NotFound() : Results.Ok(i)
recompensa: xp 15, oro 15
```

#### Escena
Piden el instrumento número 9, que no existe. La ventanilla contesta `200`, «todo bien», con un sobre vacío.

#### Gheco sugiere
En la ruta, `{id}` es una parte que cambia: en `/instrumentos/9`, el parámetro `int id` de la lambda vale `9`.

Si no se encuentra, no hay que devolver `null`: hay que avisar con un **código**. `Results.NotFound()` contesta `404`, y `Results.Ok(dato)` contesta `200` con el dato:

```csharp
return nota is null ? Results.NotFound() : Results.Ok(nota);
```

#### Desafío
Si `i` es `null`, devolvé `Results.NotFound()`; si no, `Results.Ok(i)`.

#### Código inicial
```csharp
var app = WebApplication.CreateBuilder(args).Build();
var instrumentos = new List<Instrumento> { new(1, "violín", 4), new(2, "viola", 4) };
app.MapGet("/instrumentos/{id}", (int id) =>
{
    var i = instrumentos.FirstOrDefault(x => x.Id == id);
    return i;
});

var cliente = app.CreateClient();
async Task PedirAsync(string ruta)
{
    var r = await cliente.GetAsync(ruta);
    string cuerpo = await r.Content.ReadAsStringAsync();
    Console.WriteLine($"GET {ruta} → {(int)r.StatusCode} {cuerpo}".TrimEnd());
}

await PedirAsync("/instrumentos/2");
await PedirAsync("/instrumentos/9");

record Instrumento(int Id, string Nombre, int Cuerdas);
```

#### Salida esperada
```
GET /instrumentos/2 → 200 {"id":2,"nombre":"viola","cuerdas":4}
GET /instrumentos/9 → 404
```

#### Solución
```csharp
var app = WebApplication.CreateBuilder(args).Build();
var instrumentos = new List<Instrumento> { new(1, "violín", 4), new(2, "viola", 4) };
app.MapGet("/instrumentos/{id}", (int id) =>
{
    var i = instrumentos.FirstOrDefault(x => x.Id == id);
    return i is null ? Results.NotFound() : Results.Ok(i);
});

var cliente = app.CreateClient();
async Task PedirAsync(string ruta)
{
    var r = await cliente.GetAsync(ruta);
    string cuerpo = await r.Content.ReadAsStringAsync();
    Console.WriteLine($"GET {ruta} → {(int)r.StatusCode} {cuerpo}".TrimEnd());
}

await PedirAsync("/instrumentos/2");
await PedirAsync("/instrumentos/9");

record Instrumento(int Id, string Nombre, int Cuerdas);
```

#### Al superarla
—Un «no hay» a tiempo —dice Clave— vale más que un «todo bien» mentiroso.

#### Imagen
- La ventanilla de madera de un conservatorio gótico con un sobre de papel liso vacío y abierto sobre el mostrador, con faroles, sin letras.
- Clave da vuelta el sobre vacío; Ceci levanta un cartelito liso de color rojo.

### Micro-misión R05-N07-P4 · Un pedido nuevo

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Bemol
carta: MapPost | app.MapPost("/ruta", (Pedido p) => …) · el JSON del cuerpo llega como objeto · Results.Created(…) → 201
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Elefa, desde el Puerto, quiere **encargar** dos copias del Canon. Manda el pedido con `POST`, pero la ventanilla solo atiende `GET` en esa ruta y le contesta `405`.

#### Gheco sugiere
Para recibir algo nuevo se usa `POST`, y se atiende con `MapPost`. Los datos llegan en JSON en el cuerpo del pedido, y se convierten solos en el objeto que pide la lambda:

```csharp
app.MapPost("/notas", (Nota n) =>
{
    notas.Add(n);
    return Results.Created($"/notas/{n.Id}", n);
});
```

`Results.Created(ruta, dato)` contesta `201`: «creado, y queda en esta ruta».

#### Desafío
Agregá un `MapPost` en `/pedidos` que agregue el pedido a la lista y conteste con `Results.Created($"/pedidos/{p.Id}", p)`.

#### Código inicial
```csharp
var app = WebApplication.CreateBuilder(args).Build();
var pedidos = new List<Pedido>();
app.MapGet("/pedidos", () => pedidos);

var cliente = app.CreateClient();
var r = await cliente.PostAsJsonAsync("/pedidos", new Pedido(1, "Canon", 2));
Console.WriteLine($"POST /pedidos → {(int)r.StatusCode} {await r.Content.ReadAsStringAsync()}".TrimEnd());
r = await cliente.GetAsync("/pedidos");
Console.WriteLine($"GET /pedidos → {(int)r.StatusCode} {await r.Content.ReadAsStringAsync()}");

record Pedido(int Id, string Obra, int Cantidad);
```

#### Salida esperada
```
POST /pedidos → 201 {"id":1,"obra":"Canon","cantidad":2}
GET /pedidos → 200 [{"id":1,"obra":"Canon","cantidad":2}]
```

#### Solución
```csharp
var app = WebApplication.CreateBuilder(args).Build();
var pedidos = new List<Pedido>();
app.MapGet("/pedidos", () => pedidos);
app.MapPost("/pedidos", (Pedido p) =>
{
    pedidos.Add(p);
    return Results.Created($"/pedidos/{p.Id}", p);
});

var cliente = app.CreateClient();
var r = await cliente.PostAsJsonAsync("/pedidos", new Pedido(1, "Canon", 2));
Console.WriteLine($"POST /pedidos → {(int)r.StatusCode} {await r.Content.ReadAsStringAsync()}".TrimEnd());
r = await cliente.GetAsync("/pedidos");
Console.WriteLine($"GET /pedidos → {(int)r.StatusCode} {await r.Content.ReadAsStringAsync()}");

record Pedido(int Id, string Obra, int Cantidad);
```

#### Al superarla
En el Puerto, Elefa recibe un `201` y aplaude con la trompa. Bemol jura que eso también se escuchó desde acá.

#### Imagen
- La ventanilla de madera de un conservatorio gótico con una cinta transportadora de bronce que trae un paquete de partituras atado con cinta bordó, con faroles, sin letras.
- Bemol recibe el paquete con los brazos abiertos; Ceci anota en una libreta lisa.

### Micro-misión R05-N07-P5 · El goblin de los cero violines

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Gheco
criatura: goblin
carta: Goblin | validar lo que llega · if (no sirve) return Results.BadRequest("por qué") · 400
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un goblin encarga **cero** violines, y después **menos tres**. La ventanilla los acepta encantada, y el depósito no sabe qué preparar.

#### Gheco sugiere
Cualquiera puede mandarle cualquier cosa a una API. Antes de guardar, hay que **validar**: si el dato no sirve, se contesta `400` con `Results.BadRequest(...)`, y un mensaje que diga por qué.

```csharp
if (n.Octava < 0)
{
    return Results.BadRequest("La octava no puede ser negativa");
}
```

#### Desafío
Al principio del `MapPost`, si `p.Cantidad` es menor o igual que cero, devolvé `Results.BadRequest("La cantidad tiene que ser mayor que cero")`.

#### Código inicial
```csharp
var app = WebApplication.CreateBuilder(args).Build();
var pedidos = new List<Pedido>();
app.MapPost("/pedidos", (Pedido p) =>
{
    pedidos.Add(p);
    return Results.Created($"/pedidos/{p.Id}", p);
});

var cliente = app.CreateClient();
foreach (var p in new[] { new Pedido(1, "Canon", 2), new Pedido(2, "Bolero", 0), new Pedido(3, "Tango", -3) })
{
    var r = await cliente.PostAsJsonAsync("/pedidos", p);
    Console.WriteLine($"POST {p.Obra} → {(int)r.StatusCode} {await r.Content.ReadAsStringAsync()}");
}
Console.WriteLine($"Pedidos guardados: {pedidos.Count}");

record Pedido(int Id, string Obra, int Cantidad);
```

#### Salida esperada
```
POST Canon → 201 {"id":1,"obra":"Canon","cantidad":2}
POST Bolero → 400 "La cantidad tiene que ser mayor que cero"
POST Tango → 400 "La cantidad tiene que ser mayor que cero"
Pedidos guardados: 1
```

#### Solución
```csharp
var app = WebApplication.CreateBuilder(args).Build();
var pedidos = new List<Pedido>();
app.MapPost("/pedidos", (Pedido p) =>
{
    if (p.Cantidad <= 0)
    {
        return Results.BadRequest("La cantidad tiene que ser mayor que cero");
    }
    pedidos.Add(p);
    return Results.Created($"/pedidos/{p.Id}", p);
});

var cliente = app.CreateClient();
foreach (var p in new[] { new Pedido(1, "Canon", 2), new Pedido(2, "Bolero", 0), new Pedido(3, "Tango", -3) })
{
    var r = await cliente.PostAsJsonAsync("/pedidos", p);
    Console.WriteLine($"POST {p.Obra} → {(int)r.StatusCode} {await r.Content.ReadAsStringAsync()}");
}
Console.WriteLine($"Pedidos guardados: {pedidos.Count}");

record Pedido(int Id, string Obra, int Cantidad);
```

#### Al superarla
El goblin lee el `400`, se rasca la cabeza y encarga… un violín. Uno solo. Después se queda mirándolo, sin saber qué hacer con él.

#### Imagen
- La ventanilla de madera de un conservatorio gótico con faroles, con un sello de goma grande y un papel liso con una marca roja en el mostrador, sin letras.
- Un goblin chico de orejas puntiagudas, del otro lado de la ventanilla, estira un papel arrugado; Gheco, parado solo sobre el mostrador, le muestra el sello rojo.

### Encargo R05-N07-E1 · La cartelera de Nima

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Nima quiere que la Feria le pregunte al Conservatorio qué obras se tocan. Armá una ventanilla con la lista de obras `new(1, "Canon", 8)`, `new(2, "Bolero", 12)` y `new(3, "Tango", 5)` (un `record Obra(int Id, string Titulo, int Paginas)`), y dos rutas:

- `GET /obras`: la lista entera;
- `GET /obras/{id}`: la obra con ese `id` (`200`), o `404` si no existe.

Después, leé rutas, una por línea, hasta una línea vacía. Pedí cada una con `GetAsync` y mostrá `GET`, la ruta, una flecha, el código y el cuerpo (sin espacio al final si el cuerpo está vacío).

Con esta entrada:

```
/obras/2
/obras/7
/obras

```

se muestra:

```
GET /obras/2 → 200 {"id":2,"titulo":"Bolero","paginas":12}
GET /obras/7 → 404
GET /obras → 200 [{"id":1,"titulo":"Canon","paginas":8},{"id":2,"titulo":"Bolero","paginas":12},{"id":3,"titulo":"Tango","paginas":5}]
```

#### Criterio de aprobación

- Atiende las dos rutas con `MapGet`, con `Results.NotFound()` para la que no existe.
- Le habla a la ventanilla con el `HttpClient` de `app.CreateClient()`.

#### Entrada de ejemplo

```
/obras/2
/obras/7
/obras

```

#### Salida esperada

```
GET /obras/2 → 200 {"id":2,"titulo":"Bolero","paginas":12}
GET /obras/7 → 404
GET /obras → 200 [{"id":1,"titulo":"Canon","paginas":8},{"id":2,"titulo":"Bolero","paginas":12},{"id":3,"titulo":"Tango","paginas":5}]
```

#### Solución de referencia

```csharp
var app = WebApplication.CreateBuilder(args).Build();
var obras = new List<Obra> { new(1, "Canon", 8), new(2, "Bolero", 12), new(3, "Tango", 5) };

app.MapGet("/obras", () => obras);
app.MapGet("/obras/{id}", (int id) =>
{
    var o = obras.FirstOrDefault(x => x.Id == id);
    return o is null ? Results.NotFound() : Results.Ok(o);
});

var cliente = app.CreateClient();
string? ruta = Console.ReadLine();
while (!string.IsNullOrEmpty(ruta))
{
    var r = await cliente.GetAsync(ruta);
    string cuerpo = await r.Content.ReadAsStringAsync();
    Console.WriteLine($"GET {ruta} → {(int)r.StatusCode} {cuerpo}".TrimEnd());
    ruta = Console.ReadLine();
}

record Obra(int Id, string Titulo, int Paginas);
```

## R05-N08 · Jefe: el Duende de la Ventanilla

```meta
tipo: jefe
padre: R05-N07
precio: 10
criatura: dragon
insignia: Voz de la Ventanilla
insignia_descripcion: Venciste al Duende de la Ventanilla: tus programas esperan sin trabarse, no pierden datos, se ensayan solos, guardan en una base de datos y atienden pedidos como una API.
usa: conc.async, conc.sincronizacion, cal.pruebas, sql.desde-codigo, sql.transacciones, web.api-rest
```

### Crónica

La campanilla que sonaba sola tenía dueño. Del otro lado del vidrio de la ventanilla aparece **el Duende**: chiquito, hecho de sobres y cartas, con un sombrero de papel doblado y campanillas de bronce colgando por todos lados. Contesta antes de que le pregunten, mezcla los turnos, promete partituras que no existen y acepta pedidos de cero violines.

—No se lo calla gritándole —dice {mentor}—. Se lo calla **contestando bien**. Cinco campanillas: un programa que espera sin trabarse, uno que no pierde turnos, uno que se ensaya solo, una Bóveda que no pierde corcheas y una ventanilla que dice la verdad. Con la quinta, se queda sin nada que decir.

### Objetivos

- Juntar asincronía, candados, pruebas, base de datos y API.
- Encontrar y arreglar los errores de a uno.

### Antes de empezar

- Todo el acto: R05-N01 a R05-N07.

### Explicación

#### Qué usar para qué

| Necesito… | Uso |
|---|---|
| esperar algo sin trabar el programa | `await` en un método `async Task` |
| esperar varias cosas a la vez | `Task.WhenAll` |
| que varias tareas no pisen el mismo dato | `SemaphoreSlim`, con `Release()` en un `finally` |
| saber si mi código anda, siempre | pruebas con `[Fact]`, `[Theory]` y `Assert` |
| guardar y buscar datos | SQLite con parámetros |
| que un cambio de dos partes no quede a medias | una transacción: `Commit` o `Rollback` |
| atender pedidos de otros programas | `MapGet`, `MapPost` y `Results` |

#### Cómo tocar una campanilla

1. Ensayá y leé el **primer** error: el compilador te dice la línea y el código (`CS…`).
2. Si explota al correr, mirá el nombre de la excepción.
3. Si se queda esperando hasta cortarse, buscá un `await` que nunca termina: un candado que nadie soltó.
4. Si corre pero da otra cosa, seguí los datos paso a paso.

### Código de ejemplo

```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=conservatorio.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE obras (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL);"
    + "INSERT INTO obras (titulo) VALUES ('Canon'), ('Bolero');";
comando.ExecuteNonQuery();

var app = WebApplication.CreateBuilder(args).Build();
app.MapGet("/obras/{id}", (int id) =>
{
    var buscar = conexion.CreateCommand();
    buscar.CommandText = "SELECT titulo FROM obras WHERE id = $id";
    buscar.Parameters.AddWithValue("$id", id);
    object? titulo = buscar.ExecuteScalar();
    return titulo is null ? Results.NotFound() : Results.Ok(new { id, titulo });
});

var cliente = app.CreateClient();
foreach (string ruta in new[] { "/obras/1", "/obras/5" })
{
    var r = await cliente.GetAsync(ruta);
    Console.WriteLine($"GET {ruta} → {(int)r.StatusCode} {await r.Content.ReadAsStringAsync()}".TrimEnd());
}
```

### Salida esperada

```
GET /obras/1 → 200 {"id":1,"titulo":"Canon"}
GET /obras/5 → 404
```

### ¿Para qué sirve?

Así está armado casi cualquier programa que usás todos los días: una API que atiende muchos pedidos a la vez, guarda en una base de datos sin perder nada a medias, y tiene pruebas que se corren solas cada vez que alguien cambia algo.

### Errores habituales

- **Arreglar todo junto:** un error por vez. El siguiente aparece recién cuando arreglás el anterior.
- **Un aviso no es un error, pero avisa:** `CS4014` dice que llamaste a algo `async` sin `await`. El programa compila, pero no espera.
- **Una prueba en rojo no se borra:** se lee, y se arregla el programa (o la prueba, si estaba mal escrita).

### Micro-misión R05-N08-P1 · La primera campanilla

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Clave
criatura: dragon
carta: Campanilla 1 | CS0029: falta un await · de a una tarda la suma · Task.WhenAll → todas juntas
recompensa: xp 20, oro 20, monedas 4
```

#### Escena
El Duende le pidió al depósito tres partituras, y la ventanilla se quedó trabada. Hay que traerlas, y rápido.

#### Gheco sugiere
De a uno:

1. Ensayá: `CS0029` dice que no se puede guardar un `Task<string>` en un `string`. A una de las llamadas le falta el `await`.
2. Después corre, pero `Rápido` da `False`: las tres se traen **de a una**, y tardan la suma. Pedilas juntas con `Task.WhenAll`, que te da un `string[]` en el mismo orden, y mostralo con `string.Join(", ", …)`.

#### Desafío
Arreglá los dos errores para que traiga las tres partituras juntas.

#### Código inicial
```csharp
async Task<string> TraerAsync(string obra)
{
    await Task.Delay(300);
    return obra;
}

var reloj = System.Diagnostics.Stopwatch.StartNew();
string a = TraerAsync("Canon");
string b = await TraerAsync("Bolero");
string c = await TraerAsync("Tango");
Console.WriteLine($"{a}, {b}, {c}");
Console.WriteLine($"Rápido: {reloj.ElapsedMilliseconds < 500}");
```

#### Salida esperada
```
Canon, Bolero, Tango
Rápido: True
```

#### Solución
```csharp
async Task<string> TraerAsync(string obra)
{
    await Task.Delay(300);
    return obra;
}

var reloj = System.Diagnostics.Stopwatch.StartNew();
string[] obras = await Task.WhenAll(TraerAsync("Canon"), TraerAsync("Bolero"), TraerAsync("Tango"));
Console.WriteLine(string.Join(", ", obras));
Console.WriteLine($"Rápido: {reloj.ElapsedMilliseconds < 500}");
```

#### Al superarla
Una de las campanillas del Duende se apaga con un «tlin» chiquito. El Duende la mira, ofendido.

#### Imagen
- La ventanilla de madera de un conservatorio gótico con faroles, con tres partituras enrolladas llegando juntas por el tubo de bronce, sin letras.
- El Duende de la Ventanilla, del otro lado del vidrio, se tapa una campanilla apagada; Ceci recibe las partituras y Clave asiente.

### Micro-misión R05-N08-P2 · La segunda campanilla

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Bemol
criatura: dragon
carta: Campanilla 2 | CS4014: WaitAsync sin await · el candado no cuida a nadie · Release() en un finally
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
El Duende mezcla los turnos: atiende a cinco personas de la fila, pero el contador dice que atendió a una sola. Y uno de los pedidos llegó vacío.

#### Gheco sugiere
De a uno:

1. El ensayo avisa `CS4014`: `candado.WaitAsync()` se llama sin `await`, así que no espera el turno y todos pasan a la vez. Ponele `await`.
2. Ahora el programa se queda esperando hasta cortarse: cuando llega el pedido vacío, salta el error antes del `Release()`, y el candado queda cerrado. Poné lo de adentro en un `try` y el `Release()` en un `finally`.

#### Desafío
Arreglá los dos errores para que cuente bien a los atendidos y no se trabe con el pedido vacío.

#### Código inicial
```csharp
var candado = new SemaphoreSlim(1);
int atendidos = 0;

async Task AtenderAsync(string quien)
{
    candado.WaitAsync();
    if (quien == "")
    {
        throw new ArgumentException("pedido vacío");
    }
    int v = atendidos;
    await Task.Yield();
    atendidos = v + 1;
    candado.Release();
}

List<Task> tareas = new List<Task>();
foreach (string quien in new[] { "Nilo", "Nima", "", "Elefa", "Kira" })
{
    tareas.Add(AtenderAsync(quien));
}
try
{
    await Task.WhenAll(tareas);
}
catch (ArgumentException e)
{
    Console.WriteLine($"Rechazado: {e.Message}");
}
Console.WriteLine($"Atendidos: {atendidos}");
```

#### Salida esperada
```
Rechazado: pedido vacío
Atendidos: 4
```

#### Solución
```csharp
var candado = new SemaphoreSlim(1);
int atendidos = 0;

async Task AtenderAsync(string quien)
{
    await candado.WaitAsync();
    try
    {
        if (quien == "")
        {
            throw new ArgumentException("pedido vacío");
        }
        int v = atendidos;
        await Task.Yield();
        atendidos = v + 1;
    }
    finally
    {
        candado.Release();
    }
}

List<Task> tareas = new List<Task>();
foreach (string quien in new[] { "Nilo", "Nima", "", "Elefa", "Kira" })
{
    tareas.Add(AtenderAsync(quien));
}
try
{
    await Task.WhenAll(tareas);
}
catch (ArgumentException e)
{
    Console.WriteLine($"Rechazado: {e.Message}");
}
Console.WriteLine($"Atendidos: {atendidos}");
```

#### Al superarla
La fila avanza de a uno, ordenada. La segunda campanilla del Duende se apaga, y él empieza a contar con los dedos cuántas le quedan.

#### Imagen
- La ventanilla de madera de un conservatorio gótico con faroles y una fila ordenada de gente de espaldas, con un candado de bronce abierto en el mostrador, sin letras.
- El Duende de la Ventanilla cuenta sus campanillas con cara de preocupado; Bemol hace pasar a la fila de a uno, y Ceci sostiene la llave del candado.

### Micro-misión R05-N08-P3 · La tercera campanilla

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Don Cedro
criatura: dragon
carta: Campanilla 3 | leé cada rojo · el código suma en vez de multiplicar · falta un [Fact] · y una espera negativa tiene que lanzar ArgumentException
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
El Duende le dice a la fila cualquier cosa sobre cuánto van a esperar. Don Cedro escribió un cálculo de la espera, con sus pruebas, pero las pruebas están en rojo.

#### Gheco sugiere
Cada persona adelante son **3 minutos** de espera. Leé cada rojo, de a uno:

1. `SinNadieNoSeEspera` espera `0` y obtiene `3`: el método **suma** 3 en vez de **multiplicar** por 3.
2. `NegativoFalla` dice que no saltó ninguna excepción: si `personas` es negativo, `Espera` tiene que lanzar una `ArgumentException`.
3. Ya en verde, contá: son tres pruebas y pasan dos. A una le falta el `[Fact]`.

#### Desafío
Arreglá los tres errores para que pasen las tres pruebas.

#### Código inicial
```csharp
using Xunit;

public class Ventanilla
{
    public int Espera(int personas)
    {
        return personas + 3;
    }
}

public class VentanillaTests
{
    [Fact]
    public void SinNadieNoSeEspera() => Assert.Equal(0, new Ventanilla().Espera(0));

    public void CuatroPersonas() => Assert.Equal(12, new Ventanilla().Espera(4));

    [Fact]
    public void NegativoFalla() => Assert.Throws<ArgumentException>(() => new Ventanilla().Espera(-1));
}
```

#### Salida esperada
```
Corriendo las pruebas…
  ✓ VentanillaTests.SinNadieNoSeEspera
  ✓ VentanillaTests.CuatroPersonas
  ✓ VentanillaTests.NegativoFalla

Pasaron 3 de 3 pruebas. ✓ Todo en verde.
```

#### Solución
```csharp
using Xunit;

public class Ventanilla
{
    public int Espera(int personas)
    {
        if (personas < 0)
        {
            throw new ArgumentException("no puede haber personas negativas");
        }
        return personas * 3;
    }
}

public class VentanillaTests
{
    [Fact]
    public void SinNadieNoSeEspera() => Assert.Equal(0, new Ventanilla().Espera(0));

    [Fact]
    public void CuatroPersonas() => Assert.Equal(12, new Ventanilla().Espera(4));

    [Fact]
    public void NegativoFalla() => Assert.Throws<ArgumentException>(() => new Ventanilla().Espera(-1));
}
```

#### Al superarla
Tres lucecitas verdes en el afinador de Don Cedro. La tercera campanilla del Duende se apaga, y él se cruza de brazos.

#### Imagen
- Una sala de ensayo gótica con velas y el afinador mecánico de bronce sobre una mesa, con tres lucecitas verdes encendidas, sin letras.
- El Duende de la Ventanilla, sentado en un atril, se cruza de brazos enojado; Don Cedro señala las luces verdes y Ceci sonríe.

### Micro-misión R05-N08-P4 · La cuarta campanilla

```meta
lugar: La Bóveda
personajes: Ceci, Bemol
criatura: dragon
carta: Campanilla 4 | SqliteException: el SQL mal escrito · un pago de dos partes · en una transacción: Commit o Rollback
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
El Duende metió un pago falso en la Bóveda: Ceci le paga 40 corcheas a Clave, que todavía no tiene cuenta. Las corcheas desaparecen.

#### Gheco sugiere
De a uno:

1. Explota con una `SqliteException` y un `syntax error`: una de las palabras del SQL está mal escrita. Mirala de cerca.
2. Ahora dice «Pago rechazado», pero Ceci quedó con 60: la primera parte del pago pasó y la segunda no. Poné las dos en una **transacción**: `BeginTransaction()` antes del `try` (y `comando.Transaction = transaccion;`), `Commit()` al final del `try`, `Rollback()` en el `catch`, y `comando.Transaction = null;` al terminar.

#### Desafío
Arreglá los dos errores para que un pago rechazado no cambie ninguna cuenta.

#### Código inicial
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE cuentas (nombre TEXT PRIMARY KEY, corcheas INTEGER);"
    + "INSERT INTO cuentas VALUES ('Ceci', 100), ('Bemol', 50);";
comando.ExecuteNonQuery();

try
{
    comando.CommandText = "UPDATE cuentas SET corcheas = corcheas - 40 WHERE nombre = 'Ceci'";
    comando.ExecuteNonQuery();
    comando.CommandText = "UPDTE cuentas SET corcheas = corcheas + 40 WHERE nombre = 'Clave'";
    if (comando.ExecuteNonQuery() == 0)
    {
        throw new InvalidOperationException("no existe la cuenta de Clave");
    }
    Console.WriteLine("Pago hecho");
}
catch (InvalidOperationException e)
{
    Console.WriteLine($"Pago rechazado: {e.Message}");
}

comando.CommandText = "SELECT nombre, corcheas FROM cuentas ORDER BY nombre";
using var lector = comando.ExecuteReader();
while (lector.Read())
{
    Console.WriteLine($"{lector.GetString(0)}: {lector.GetInt32(1)}");
}
```

#### Salida esperada
```
Pago rechazado: no existe la cuenta de Clave
Bemol: 50
Ceci: 100
```

#### Solución
```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=boveda.db");
conexion.Open();
var comando = conexion.CreateCommand();
comando.CommandText = "CREATE TABLE cuentas (nombre TEXT PRIMARY KEY, corcheas INTEGER);"
    + "INSERT INTO cuentas VALUES ('Ceci', 100), ('Bemol', 50);";
comando.ExecuteNonQuery();

using var transaccion = conexion.BeginTransaction();
comando.Transaction = transaccion;
try
{
    comando.CommandText = "UPDATE cuentas SET corcheas = corcheas - 40 WHERE nombre = 'Ceci'";
    comando.ExecuteNonQuery();
    comando.CommandText = "UPDATE cuentas SET corcheas = corcheas + 40 WHERE nombre = 'Clave'";
    if (comando.ExecuteNonQuery() == 0)
    {
        throw new InvalidOperationException("no existe la cuenta de Clave");
    }
    transaccion.Commit();
    Console.WriteLine("Pago hecho");
}
catch (InvalidOperationException e)
{
    transaccion.Rollback();
    Console.WriteLine($"Pago rechazado: {e.Message}");
}
comando.Transaction = null;

comando.CommandText = "SELECT nombre, corcheas FROM cuentas ORDER BY nombre";
using var lector = comando.ExecuteReader();
while (lector.Read())
{
    Console.WriteLine($"{lector.GetString(0)}: {lector.GetInt32(1)}");
}
```

#### Al superarla
Las cuarenta corcheas vuelven a su lugar con un tintineo. La cuarta campanilla del Duende se apaga, y al Duende le tiembla el sombrero.

#### Imagen
- Una bóveda de piedra con faroles azules y una balanza de bronce equilibrada sobre la mesa, con monedas doradas lisas, sin letras ni números.
- El Duende de la Ventanilla, colgado del borde de la mesa, mira la balanza con fastidio; Bemol y Ceci chocan los cinco.

### Micro-misión R05-N08-P5 · La voz de la ventanilla

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Clave, Bemol, Gheco
criatura: dragon
carta: Jefe | un error por vez · 404 en todo: la ruta no coincide · 200 vacío: Results.NotFound() · 201 con cero: Results.BadRequest(…)
recompensa: xp 30, oro 30, monedas 3
item: Campanilla Afinada
```

#### Escena
La última campanilla es la ventanilla misma. El Duende la dejó contestando mentiras: no encuentra nada, dice «todo bien» cuando no hay nada, y acepta pedidos de cero partituras. Si la ventanilla dice la verdad, el Duende se queda sin voz.

#### Gheco sugiere
De a uno, mirando los códigos:

1. Las dos primeras dan `404`: los pedidos van a `/obras/…`, pero la ruta está escrita distinto. Tienen que coincidir letra por letra.
2. La obra 9 da `200` vacío: si no está, devolvé `Results.NotFound()`, y si está, `Results.Ok(o)`.
3. El pedido de 0 copias da `201`: validá la cantidad y contestá `Results.BadRequest("La cantidad tiene que ser mayor que cero")`.

#### Desafío
Arreglá los tres errores para que la ventanilla diga la verdad.

#### Código inicial
```csharp
var app = WebApplication.CreateBuilder(args).Build();
var obras = new List<Obra> { new(1, "Canon"), new(2, "Bolero") };
var pedidos = new List<Pedido>();

app.MapGet("/obra/{id}", (int id) =>
{
    var o = obras.FirstOrDefault(x => x.Id == id);
    return o;
});
app.MapPost("/pedidos", (Pedido p) =>
{
    pedidos.Add(p);
    return Results.Created($"/pedidos/{p.Id}", p);
});

var cliente = app.CreateClient();
foreach (string ruta in new[] { "/obras/2", "/obras/9" })
{
    var r = await cliente.GetAsync(ruta);
    Console.WriteLine($"GET {ruta} → {(int)r.StatusCode} {await r.Content.ReadAsStringAsync()}".TrimEnd());
}
var post = await cliente.PostAsJsonAsync("/pedidos", new Pedido(1, "Canon", 0));
Console.WriteLine($"POST /pedidos → {(int)post.StatusCode} {await post.Content.ReadAsStringAsync()}");

record Obra(int Id, string Titulo);
record Pedido(int Id, string Obra, int Cantidad);
```

#### Salida esperada
```
GET /obras/2 → 200 {"id":2,"titulo":"Bolero"}
GET /obras/9 → 404
POST /pedidos → 400 "La cantidad tiene que ser mayor que cero"
```

#### Solución
```csharp
var app = WebApplication.CreateBuilder(args).Build();
var obras = new List<Obra> { new(1, "Canon"), new(2, "Bolero") };
var pedidos = new List<Pedido>();

app.MapGet("/obras/{id}", (int id) =>
{
    var o = obras.FirstOrDefault(x => x.Id == id);
    return o is null ? Results.NotFound() : Results.Ok(o);
});
app.MapPost("/pedidos", (Pedido p) =>
{
    if (p.Cantidad <= 0)
    {
        return Results.BadRequest("La cantidad tiene que ser mayor que cero");
    }
    pedidos.Add(p);
    return Results.Created($"/pedidos/{p.Id}", p);
});

var cliente = app.CreateClient();
foreach (string ruta in new[] { "/obras/2", "/obras/9" })
{
    var r = await cliente.GetAsync(ruta);
    Console.WriteLine($"GET {ruta} → {(int)r.StatusCode} {await r.Content.ReadAsStringAsync()}".TrimEnd());
}
var post = await cliente.PostAsJsonAsync("/pedidos", new Pedido(1, "Canon", 0));
Console.WriteLine($"POST /pedidos → {(int)post.StatusCode} {await post.Content.ReadAsStringAsync()}");

record Obra(int Id, string Titulo);
record Pedido(int Id, string Obra, int Cantidad);
```

#### Al superarla
La quinta campanilla se apaga y la ventanilla queda en silencio. El Duende abre la boca para decir algo… y no le sale nada: todo lo que iba a inventar, la ventanilla ya lo contestó bien. Se dobla como una carta, más chico, más chico, hasta desaparecer. En el mostrador queda una sola campanilla de vidrio: la **Campanilla Afinada**. Cuando Ceci la toca, suena con la nota que le faltaba a la melodía del Vidriero.

—La tenía colgada del cuello —dice {mentor}—. Era la única que nunca se animó a hacer sonar.

#### Imagen
- La ventanilla de madera de un conservatorio gótico con faroles, con una campanilla de vidrio brillante sobre el mostrador y sobres de papel liso cayendo despacio como hojas, sin letras.
- Clave levanta la campanilla de vidrio; Ceci, Bemol y Gheco la miran asombrados.

### Encargo R05-N08-E1 · La API del Gremio

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

El Gremio quiere su ranking en una API que guarde en la Bóveda. Creá en SQLite la tabla `jugadores` (`nombre TEXT PRIMARY KEY`, `puntos INTEGER`). Armá una ventanilla con:

- `POST /jugadores`: recibe un `record Jugador(string Nombre, int Puntos)`. Si los puntos son negativos, contesta `Results.BadRequest("Puntos negativos")`; si no, lo guarda con un `INSERT` con parámetros y contesta `Results.Created($"/jugadores/{j.Nombre}", j)`.
- `GET /ranking`: los jugadores de la tabla, ordenados por puntos de mayor a menor, como lista de `Jugador`.

Después, leé jugadores como `nombre,puntos` hasta una línea vacía y mandá cada uno con `PostAsJsonAsync`: si contesta `201`, mostrá `Guardado: ` y el nombre; si no, `Rechazado: ` y el nombre. Al final, pedí `/ranking` y mostrá `GET /ranking → `, el código y el cuerpo.

Con esta entrada:

```
Ceci,25
Tomi,-5
Bemol,30

```

se muestra:

```
Guardado: Ceci
Rechazado: Tomi
Guardado: Bemol
GET /ranking → 200 [{"nombre":"Bemol","puntos":30},{"nombre":"Ceci","puntos":25}]
```

#### Criterio de aprobación

- Guarda y lee con SQLite y parámetros; el ranking sale de un `SELECT … ORDER BY puntos DESC`.
- Valida los puntos con `Results.BadRequest` y le habla a la ventanilla con el `HttpClient` de `app.CreateClient()`.

#### Entrada de ejemplo

```
Ceci,25
Tomi,-5
Bemol,30

```

#### Salida esperada

```
Guardado: Ceci
Rechazado: Tomi
Guardado: Bemol
GET /ranking → 200 [{"nombre":"Bemol","puntos":30},{"nombre":"Ceci","puntos":25}]
```

#### Solución de referencia

```csharp
using Microsoft.Data.Sqlite;

using var conexion = new SqliteConnection("Data Source=gremio.db");
conexion.Open();
var crear = conexion.CreateCommand();
crear.CommandText = "CREATE TABLE jugadores (nombre TEXT PRIMARY KEY, puntos INTEGER)";
crear.ExecuteNonQuery();

var app = WebApplication.CreateBuilder(args).Build();
app.MapPost("/jugadores", (Jugador j) =>
{
    if (j.Puntos < 0)
    {
        return Results.BadRequest("Puntos negativos");
    }
    var insertar = conexion.CreateCommand();
    insertar.CommandText = "INSERT INTO jugadores (nombre, puntos) VALUES ($nombre, $puntos)";
    insertar.Parameters.AddWithValue("$nombre", j.Nombre);
    insertar.Parameters.AddWithValue("$puntos", j.Puntos);
    insertar.ExecuteNonQuery();
    return Results.Created($"/jugadores/{j.Nombre}", j);
});
app.MapGet("/ranking", () =>
{
    var leer = conexion.CreateCommand();
    leer.CommandText = "SELECT nombre, puntos FROM jugadores ORDER BY puntos DESC";
    var lista = new List<Jugador>();
    using var lector = leer.ExecuteReader();
    while (lector.Read())
    {
        lista.Add(new Jugador(lector.GetString(0), lector.GetInt32(1)));
    }
    return lista;
});

var cliente = app.CreateClient();
string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    string[] partes = linea.Split(',');
    var r = await cliente.PostAsJsonAsync("/jugadores", new Jugador(partes[0], int.Parse(partes[1])));
    Console.WriteLine((int)r.StatusCode == 201 ? $"Guardado: {partes[0]}" : $"Rechazado: {partes[0]}");
    linea = Console.ReadLine();
}
var ranking = await cliente.GetAsync("/ranking");
Console.WriteLine($"GET /ranking → {(int)ranking.StatusCode} {await ranking.Content.ReadAsStringAsync()}");

record Jugador(string Nombre, int Puntos);
```

