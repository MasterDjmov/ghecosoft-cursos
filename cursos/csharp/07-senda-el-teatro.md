# RAMA S01 · Senda del Teatro: el guion de los títeres

```meta
tipo: senda
posicion: 7
```

## S01-N01 · El títere y sus estados

```meta
tipo: tema
padre: R04-N06
precio: 3
moneda: comodin
criatura: ogro
temas: diseno.maquina-estados, prog.enums
usa: prog.condicionales, col.mapas
```

### Crónica

Una tarde, Hilván entra al Conservatorio con una caja de títeres bajo el brazo y los hilos dorados enredados hasta los codos. —Ceci, necesito a mi hermana.

En el Teatro de la Feria, Nima armó un **tablero en su lengua**, JavaScript, que mueve los títeres solo: lee un **guion** y, en cada segundo de la función, hace entrar, bailar o salir a cada uno. —El problema es el guion —dice Hilván—. Lo escribo a mano y me equivoco: Lola baila sin haber entrado, Pipo sale dos veces. El tablero no se da cuenta, y los hilos se enredan delante de todo el público.

Ceci mira a {mentor}. Clave levanta una ceja. —Antes de que un títere haga algo, hay que saber **en qué estado está**. Eso se programa.

### Objetivos

- Describir los estados de un títere con un `enum`.
- Escribir las **transiciones** (de qué estado a cuál, con qué acción) con un `switch` sobre una tupla.
- Lanzar una excepción cuando una acción no se puede hacer.
- Llevar el estado de varios títeres en un `Dictionary`.

### Antes de empezar

- `enum` y `switch` (Actos I y II), excepciones (R04-N01 y N02) y `Dictionary` (R03-N02).

### Explicación

#### Una máquina de estados

Un títere siempre está en **un** estado: guardado en la caja, en escena o bailando. Cada **acción** lo lleva de un estado a otro, pero no todas se pueden hacer siempre: no se puede bailar si estás guardado.

| Estado | Acción | Estado nuevo |
|---|---|---|
| `Guardado` | `Entra` | `EnEscena` |
| `EnEscena` | `Habla` | `EnEscena` |
| `EnEscena` | `Baila` | `Bailando` |
| `Bailando` | `Para` | `EnEscena` |
| `EnEscena` | `Sale` | `Guardado` |

Eso es una **máquina de estados**: los estados, las acciones y las flechas entre ellos. Lo que no está en la tabla, no se puede.

#### El `switch` sobre una tupla

Con una tupla `(estado, accion)`, un solo `switch` escribe la tabla entera:

```csharp
Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Baila) => Estado.Bailando,
    // ... una línea por fila de la tabla
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};
```

El `_` del final atrapa todo lo que no está en la tabla. Ahí, en vez de devolver algo, se **lanza** una excepción: un error a propósito, que dice qué pasó.

#### Varios títeres

Cada títere tiene su propio estado. Un `Dictionary<string, Estado>` los guarda por nombre:

```csharp
Dictionary<string, Estado> estados = new();
estados["Lola"] = Siguiente(estados.GetValueOrDefault("Lola"), Accion.Entra);
```

`GetValueOrDefault` devuelve el valor por defecto del `enum` si el títere todavía no está: el **primero** de la lista, `Guardado`. Por eso conviene que el estado inicial vaya primero.

### Código de ejemplo

```csharp
Estado lola = Estado.Guardado;
Accion[] acciones = [Accion.Entra, Accion.Baila, Accion.Para, Accion.Sale];

foreach (Accion a in acciones)
{
    lola = Siguiente(lola, a);
    Console.WriteLine($"{a} → {lola}");
}

try
{
    lola = Siguiente(lola, Accion.Baila);
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"No: {ex.Message}");
}

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Habla) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Baila) => Estado.Bailando,
    (Estado.Bailando, Accion.Para) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Sale) => Estado.Guardado,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

### Salida esperada

```
Entra → EnEscena
Baila → Bailando
Para → EnEscena
Sale → Guardado
No: Baila no se puede estando Guardado
```

### ¿Para qué sirve?

Las máquinas de estados están en todos lados: un semáforo, un pedido que pasa de «pagado» a «enviado», un personaje de videojuego que camina, salta o cae, la conexión de una app. Escribir la tabla de una vez evita los «esto no debería poder pasar» que aparecen cuando cada `if` decide por su cuenta.

### Errores habituales

- **Que el `_` devuelva algo en vez de lanzar:** el error pasa en silencio y el títere hace cualquier cosa. Es el **ogro** de las transiciones.
- **Un solo estado para todos:** si Lola y Pipo comparten la variable, lo que hace uno lo cambia para el otro.
- **Llamar a `Siguiente` sin guardar lo que devuelve:** el estado no cambia solo; hay que asignarlo.

### Micro-misión S01-N01-P1 · La primera flecha

```meta
lugar: El Teatro del Titiritero
personajes: Ceci, Hilván
carta: Tupla en switch | (e, a) switch { (Estado.Guardado, Accion.Entra) => Estado.EnEscena, ... } · una línea por flecha
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Hilván saca a Lola de la caja para que entre a escena, pero el programa de Ceci dice que no se puede. A la tabla le falta la primera flecha: de guardado a en escena.

#### Gheco sugiere
Cada fila de la tabla es una línea del `switch`, con la tupla `(estado, acción)` a la izquierda y el estado nuevo a la derecha:

```csharp
(Estado.Bailando, Accion.Para) => Estado.EnEscena,
```

#### Desafío
Agregá arriba de la flecha de `Baila` la que falta: `(Estado.Guardado, Accion.Entra) => Estado.EnEscena,`.

#### Código inicial
```csharp
Estado lola = Estado.Guardado;
try
{
    lola = Siguiente(lola, Accion.Entra);
    Console.WriteLine($"Lola: {lola}");
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"No: {ex.Message}");
}

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.EnEscena, Accion.Baila) => Estado.Bailando,
    (Estado.Bailando, Accion.Para) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Sale) => Estado.Guardado,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Salida esperada
```
Lola: EnEscena
```

#### Solución
```csharp
Estado lola = Estado.Guardado;
try
{
    lola = Siguiente(lola, Accion.Entra);
    Console.WriteLine($"Lola: {lola}");
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"No: {ex.Message}");
}

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Baila) => Estado.Bailando,
    (Estado.Bailando, Accion.Para) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Sale) => Estado.Guardado,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Al superarla
Lola sale de la caja y se para en el escenario, con los brazos en alto. Hilván suelta el aire. —Primera vez que entra a la primera.

#### Imagen
- Un teatrito de títeres de madera con telón rojo, en una carpa de feria iluminada con farolitos, sin letras.
- Hilván, joven y flaco, con chaleco violeta y hilos dorados en los dedos, hace entrar a una títere bailarina; Ceci, con su violín a la espalda, mira desde un costado.

### Micro-misión S01-N01-P2 · Lo que no se puede

```meta
lugar: El Teatro del Titiritero
personajes: Ceci, Hilván, Gheco
carta: throw en switch | _ => throw new InvalidOperationException(...) · lo que no está en la tabla, avisa
recompensa: xp 15, oro 15
```

#### Escena
El guion dice que Pipo sale, pero Pipo nunca entró. El programa de Ceci no dice nada: el `_` devuelve el mismo estado, y el error pasa en silencio hasta la función.

#### Gheco sugiere
En un `switch` de flechas, el `_` puede **lanzar** una excepción en vez de devolver un valor. Así, lo que no está en la tabla avisa:

```csharp
string Tono(int n) => n switch
{
    1 => "grave",
    _ => throw new ArgumentException($"No hay tono {n}"),
};
```

#### Desafío
Cambiá `_ => e,` por `_ => throw new InvalidOperationException($"{a} no se puede estando {e}"),`.

#### Código inicial
```csharp
Estado pipo = Estado.Guardado;
try
{
    pipo = Siguiente(pipo, Accion.Sale);
    Console.WriteLine($"Pipo: {pipo}");
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"No se puede: {ex.Message}");
}

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Sale) => Estado.Guardado,
    _ => e,
};

enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Salida esperada
```
No se puede: Sale no se puede estando Guardado
```

#### Solución
```csharp
Estado pipo = Estado.Guardado;
try
{
    pipo = Siguiente(pipo, Accion.Sale);
    Console.WriteLine($"Pipo: {pipo}");
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"No se puede: {ex.Message}");
}

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Sale) => Estado.Guardado,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Al superarla
El programa avisa, y Hilván tacha la línea del guion. —Pipo no puede salir de donde nunca entró. Tiene sentido, dicho así.

#### Imagen
- Un payaso títere de madera con nariz roja, acostado dentro de una caja abierta, con los hilos flojos, sin letras.
- Hilván tacha algo en un papel; Gheco, un gecko de luz cian con antiparras, MINÚSCULO, sentado en el borde de la caja, señala al payaso.

### Micro-misión S01-N01-P3 · Guardar el estado nuevo

```meta
lugar: El Teatro del Titiritero
personajes: Ceci, Hilván
carta: Asignar | lola = Siguiente(lola, a); · Siguiente devuelve el estado nuevo · si no se guarda, se pierde
recompensa: xp 15, oro 15
```

#### Escena
Lola tiene que entrar y bailar. El programa llama a `Siguiente` en cada acción, pero Lola sigue guardada, y cuando le toca bailar, el programa dice que no puede.

#### Gheco sugiere
`Siguiente` no cambia nada: **devuelve** el estado nuevo. Si no lo guardás en la variable, se pierde:

```csharp
int nivel = 1;
nivel = Subir(nivel);   // sin el "nivel =", sigue en 1
```

#### Desafío
Adentro del `foreach`, cambiá `Siguiente(lola, a);` por `lola = Siguiente(lola, a);`.

#### Código inicial
```csharp
Estado lola = Estado.Guardado;
Accion[] acciones = [Accion.Entra, Accion.Baila];
try
{
    foreach (Accion a in acciones)
    {
        Siguiente(lola, a);
    }
    Console.WriteLine($"Lola termina: {lola}");
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"No: {ex.Message}");
}

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Baila) => Estado.Bailando,
    (Estado.Bailando, Accion.Para) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Sale) => Estado.Guardado,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Salida esperada
```
Lola termina: Bailando
```

#### Solución
```csharp
Estado lola = Estado.Guardado;
Accion[] acciones = [Accion.Entra, Accion.Baila];
try
{
    foreach (Accion a in acciones)
    {
        lola = Siguiente(lola, a);
    }
    Console.WriteLine($"Lola termina: {lola}");
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"No: {ex.Message}");
}

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Baila) => Estado.Bailando,
    (Estado.Bailando, Accion.Para) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Sale) => Estado.Guardado,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Al superarla
Lola entra y gira sobre una pierna, con los hilos dorados brillando. Ceci, sin pensarlo, le pone música con el violín.

#### Imagen
- El escenario del teatrito de títeres con una bailarina de madera girando en puntas, con hilos dorados que suben hasta arriba, sin letras.
- Ceci toca el violín al costado del teatrito; Hilván mueve los hilos desde arriba, concentrado.

### Micro-misión S01-N01-P4 · Cada uno con su estado

```meta
lugar: Detrás del telón
personajes: Ceci, Hilván, Clave
carta: Dictionary | estados["Pipo"] = Siguiente(estados["Pipo"], a) · un estado por títere
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Lola y Pipo entran juntos. Pero el programa usa una sola variable para los dos: cuando entra Pipo, el programa cree que ya está en escena, porque Lola entró antes.

#### Gheco sugiere
Cada títere necesita su propio estado. Un `Dictionary` los guarda por nombre, y cada acción lee y escribe el de **ese** títere:

```csharp
Dictionary<string, int> notas = new() { ["Ceci"] = 0, ["Bemol"] = 0 };
notas["Bemol"] = notas["Bemol"] + 1;
```

#### Desafío
Cambiá la línea de adentro del `foreach` para que use el estado de cada títere: `estados[t] = Siguiente(estados[t], a);`. Ya no hace falta la variable `estado`.

#### Código inicial
```csharp
Dictionary<string, Estado> estados = new() { ["Lola"] = Estado.Guardado, ["Pipo"] = Estado.Guardado };
(string, Accion)[] guion = [("Lola", Accion.Entra), ("Pipo", Accion.Entra), ("Lola", Accion.Baila)];

Estado estado = Estado.Guardado;
try
{
    foreach ((string t, Accion a) in guion)
    {
        estado = Siguiente(estado, a);
        estados[t] = estado;
    }
    Console.WriteLine($"Lola: {estados["Lola"]}, Pipo: {estados["Pipo"]}");
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"No: {ex.Message}");
}

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Baila) => Estado.Bailando,
    (Estado.Bailando, Accion.Para) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Sale) => Estado.Guardado,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Salida esperada
```
Lola: Bailando, Pipo: EnEscena
```

#### Solución
```csharp
Dictionary<string, Estado> estados = new() { ["Lola"] = Estado.Guardado, ["Pipo"] = Estado.Guardado };
(string, Accion)[] guion = [("Lola", Accion.Entra), ("Pipo", Accion.Entra), ("Lola", Accion.Baila)];

try
{
    foreach ((string t, Accion a) in guion)
    {
        estados[t] = Siguiente(estados[t], a);
    }
    Console.WriteLine($"Lola: {estados["Lola"]}, Pipo: {estados["Pipo"]}");
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"No: {ex.Message}");
}

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Baila) => Estado.Bailando,
    (Estado.Bailando, Accion.Para) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Sale) => Estado.Guardado,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Al superarla
Pipo entra haciendo una reverencia exagerada, y Lola baila a su alrededor. Clave, desde la última fila, anota algo en su libreta. Ceci no sabe si es bueno o malo.

#### Imagen
- Detrás de un telón rojo, una pasarela de madera con títeres colgados de ganchos, con farolitos, sin letras.
- Hilván maneja dos títeres a la vez, uno con cada mano; Clave, con su capa y la mecha blanca en el rodete, mira con los brazos cruzados; Ceci sostiene una lista.

### Micro-misión S01-N01-P5 · El orco de la títere nueva

```meta
lugar: Detrás del telón
personajes: Ceci, Hilván, Gheco
criatura: orco
carta: Orco | estados["Pepa"] sin Pepa → KeyNotFoundException · GetValueOrDefault("Pepa") → Guardado, el primero del enum
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Hilván suma a Pepa a la función, pero se olvidó de anotarla en el diccionario. Cuando le toca entrar, un orco chiquito salta de la caja de títeres y rompe el programa.

#### Gheco sugiere
`estados["Pepa"]` se rompe si Pepa no está. `GetValueOrDefault` devuelve el valor por defecto del `enum`, que es el **primero** de la lista: `Guardado`, justo lo que tiene una títere que todavía no entró.

```csharp
int veces = contador.GetValueOrDefault("Bemol");   // 0 si no está
```

#### Desafío
Cambiá `estados[t]` por `estados.GetValueOrDefault(t)` a la **derecha** del `=` (a la izquierda queda igual: asignar sí agrega la clave).

#### Código inicial
```csharp
Dictionary<string, Estado> estados = new() { ["Lola"] = Estado.Guardado };
(string, Accion)[] guion = [("Lola", Accion.Entra), ("Pepa", Accion.Entra)];

foreach ((string t, Accion a) in guion)
{
    estados[t] = Siguiente(estados[t], a);
}
Console.WriteLine($"Pepa: {estados["Pepa"]}");

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Sale) => Estado.Guardado,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Salida esperada
```
Pepa: EnEscena
```

#### Solución
```csharp
Dictionary<string, Estado> estados = new() { ["Lola"] = Estado.Guardado };
(string, Accion)[] guion = [("Lola", Accion.Entra), ("Pepa", Accion.Entra)];

foreach ((string t, Accion a) in guion)
{
    estados[t] = Siguiente(estados.GetValueOrDefault(t), a);
}
Console.WriteLine($"Pepa: {estados["Pepa"]}");

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Sale) => Estado.Guardado,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Al superarla
Pepa entra de la mano de Pipo. El orco, sin nada que romper, se acomoda en la primera fila y se queda a ver la función.

#### Imagen
- La pasarela detrás del telón, con una caja de títeres volcada, sin letras.
- Un orco verde chiquito y gruñón sale de la caja con un títere payaso en la mano, sin sangre ni armas; Hilván se agarra la cabeza; Gheco, MINÚSCULO, flota delante del orco con la mano levantada.

## S01-N02 · La línea de tiempo

```meta
tipo: tema
padre: S01-N01
precio: 10
criatura: ogro
temas: func.streams, prog.fechas
usa: poo.records, diseno.maquina-estados
```

### Crónica

Con la máquina de estados andando, Hilván desenrolla el guion de verdad: una tira larguísima de papel con avisos anotados en cualquier orden. «A los 12 segundos, Pipo entra.» «A los 3, Lola entra.» «A los 12, Lola baila.»

—El tablero de Nima los lee de arriba para abajo —dice Hilván—. Si el de los 12 está antes que el de los 3, Pipo entra antes que el telón se abra.

—Hay que ponerlos en orden —dice Ceci—. Y saber cuánto dura la función.

### Objetivos

- Guardar cada aviso del guion en un `record`.
- Ordenarlos por segundo con `OrderBy`, y desempatar con `ThenBy`.
- Mostrar los segundos como un reloj (`1:05`) con `TimeSpan`.
- Filtrar los avisos de un títere y calcular cuánto dura la función.

### Antes de empezar

- `record` (Acto II), LINQ (R03-N08 y N09) y la máquina de estados (S01-N01).

### Explicación

#### Un aviso, un `record`

```csharp
record Aviso(int Segundo, string Titere, Accion Accion);
```

Un `record` es justo para esto: datos que viajan juntos y no cambian.

#### Ordenar y desempatar

`OrderBy` ordena por lo que le digas. Si dos avisos caen en el **mismo** segundo, `ThenBy` decide entre ellos:

```csharp
var enOrden = guion.OrderBy(a => a.Segundo).ThenBy(a => a.Titere);
```

Sin `ThenBy`, los empatados quedan en el orden en que venían.

#### Segundos como reloj

Un `TimeSpan` es una **duración**. `TimeSpan.FromSeconds(65)` es un minuto y cinco segundos, y con `ToString` se muestra como reloj:

```csharp
TimeSpan t = TimeSpan.FromSeconds(65);
Console.WriteLine(t.ToString(@"m\:ss"));   // 1:05
```

`m` son los minutos, `ss` los segundos con dos cifras, y el `\:` es un dos puntos escrito tal cual (la `@` delante deja escribir la barra sin duplicarla).

#### Preguntas al guion

```csharp
var deLola = guion.Where(a => a.Titere == "Lola");
int dura = guion.Max(a => a.Segundo);
```

### Código de ejemplo

```csharp
List<Aviso> guion =
[
    new(12, "Pipo", Accion.Entra),
    new(3, "Lola", Accion.Entra),
    new(65, "Lola", Accion.Sale),
    new(12, "Lola", Accion.Baila),
];

foreach (Aviso a in guion.OrderBy(a => a.Segundo).ThenBy(a => a.Titere))
{
    string reloj = TimeSpan.FromSeconds(a.Segundo).ToString(@"m\:ss");
    Console.WriteLine($"{reloj} {a.Titere} {a.Accion}");
}

Console.WriteLine($"Avisos de Lola: {guion.Count(a => a.Titere == "Lola")}");
Console.WriteLine($"Dura: {TimeSpan.FromSeconds(guion.Max(a => a.Segundo)).ToString(@"m\:ss")}");

record Aviso(int Segundo, string Titere, Accion Accion);
enum Accion { Entra, Habla, Baila, Para, Sale }
```

### Salida esperada

```
0:03 Lola Entra
0:12 Lola Baila
0:12 Pipo Entra
1:05 Lola Sale
Avisos de Lola: 3
Dura: 1:05
```

### ¿Para qué sirve?

Las líneas de tiempo están en los editores de video y de música, en las animaciones de un juego, en los subtítulos de una película y en los recordatorios de un calendario. Siempre es lo mismo: avisos con un momento, puestos en orden.

### Errores habituales

- **Confiar en el orden en que vienen:** un guion escrito a mano nunca está en orden. `OrderBy` antes de usarlo.
- **Olvidarse de desempatar:** dos avisos en el mismo segundo pueden salir en cualquier orden según cómo se escribieron.
- **Usar el último aviso como duración:** el último de la lista no es el último de la función, salvo que esté ordenada. Es el **ogro** del reloj. Va `Max`.
- **Escribir `"m:ss"` sin la barra:** `ToString` de un `TimeSpan` se rompe con un `:` suelto.

### Micro-misión S01-N02-P1 · En orden de reloj

```meta
lugar: El Teatro del Titiritero
personajes: Ceci, Hilván
carta: OrderBy | guion.OrderBy(a => a.Segundo) · de menor a mayor · no cambia la lista: devuelve otra
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
El tablero de Nima lee el guion de arriba para abajo, y Pipo entra antes de que se abra el telón. Hay que ordenar los avisos por segundo.

#### Gheco sugiere
`OrderBy` recibe **por qué** ordenar, con una lambda:

```csharp
var porNivel = jugadores.OrderBy(j => j.Nivel);
```

#### Desafío
Recorré `guion.OrderBy(a => a.Segundo)` en vez de `guion`.

#### Código inicial
```csharp
List<Aviso> guion =
[
    new(12, "Pipo", Accion.Entra),
    new(0, "Telon", Accion.Entra),
    new(3, "Lola", Accion.Entra),
];

foreach (Aviso a in guion)
{
    Console.WriteLine($"{a.Segundo}s {a.Titere} {a.Accion}");
}

record Aviso(int Segundo, string Titere, Accion Accion);
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Salida esperada
```
0s Telon Entra
3s Lola Entra
12s Pipo Entra
```

#### Solución
```csharp
List<Aviso> guion =
[
    new(12, "Pipo", Accion.Entra),
    new(0, "Telon", Accion.Entra),
    new(3, "Lola", Accion.Entra),
];

foreach (Aviso a in guion.OrderBy(a => a.Segundo))
{
    Console.WriteLine($"{a.Segundo}s {a.Titere} {a.Accion}");
}

record Aviso(int Segundo, string Titere, Accion Accion);
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Al superarla
Primero se abre el telón, después entra Lola, después Pipo. Hilván mira el orden y se ríe. —Ahora parece una función.

#### Imagen
- Una tira larga de papel desenrollada sobre el piso del teatro, con marcas y dibujitos sin letras, junto a un teatrito con el telón abriéndose.
- Ceci, arrodillada, acomoda pedazos de papel en fila; Hilván, de pie, sostiene la punta de la tira.

### Micro-misión S01-N02-P2 · Empate en el segundo doce

```meta
lugar: El Teatro del Titiritero
personajes: Ceci, Hilván, Gheco
carta: ThenBy | .OrderBy(a => a.Segundo).ThenBy(a => a.Titere) · ThenBy desempata a los iguales
recompensa: xp 15, oro 15
```

#### Escena
A los 12 segundos pasan dos cosas: entra Pipo y baila Lola. Hilván quiere que, cuando empatan, vayan por orden alfabético, así el tablero siempre hace lo mismo.

#### Gheco sugiere
`ThenBy` va **después** de un `OrderBy` y solo ordena a los que empataron:

```csharp
var tabla = jugadores.OrderBy(j => j.Nivel).ThenBy(j => j.Nombre);
```

#### Desafío
Agregá `.ThenBy(a => a.Titere)` después del `OrderBy`.

#### Código inicial
```csharp
List<Aviso> guion =
[
    new(12, "Pipo", Accion.Entra),
    new(3, "Lola", Accion.Entra),
    new(12, "Lola", Accion.Baila),
];

foreach (Aviso a in guion.OrderBy(a => a.Segundo))
{
    Console.WriteLine($"{a.Segundo}s {a.Titere} {a.Accion}");
}

record Aviso(int Segundo, string Titere, Accion Accion);
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Salida esperada
```
3s Lola Entra
12s Lola Baila
12s Pipo Entra
```

#### Solución
```csharp
List<Aviso> guion =
[
    new(12, "Pipo", Accion.Entra),
    new(3, "Lola", Accion.Entra),
    new(12, "Lola", Accion.Baila),
];

foreach (Aviso a in guion.OrderBy(a => a.Segundo).ThenBy(a => a.Titere))
{
    Console.WriteLine($"{a.Segundo}s {a.Titere} {a.Accion}");
}

record Aviso(int Segundo, string Titere, Accion Accion);
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Al superarla
El empate se resuelve siempre igual. Hilván lo prueba tres veces, cambiando el orden de las líneas, y el guion sale idéntico.

#### Imagen
- El teatrito con dos títeres en escena a la vez, una bailarina girando y un payaso entrando, sin letras.
- Hilván maneja los dos con cara de esfuerzo; Gheco, MINÚSCULO, sentado sobre el techo del teatrito, sostiene un relojito de arena.

### Micro-misión S01-N02-P3 · El reloj de la función

```meta
lugar: Detrás del telón
personajes: Ceci, Hilván
carta: TimeSpan | TimeSpan.FromSeconds(65).ToString(@"m\:ss") → 1:05 · \: es el dos puntos tal cual
recompensa: xp 15, oro 15
```

#### Escena
Detrás del telón hay un reloj grande, y Hilván se guía por él. Pero el guion de Ceci dice «65 s», y Hilván tiene que hacer la cuenta en la cabeza mientras maneja los hilos.

#### Gheco sugiere
`TimeSpan.FromSeconds` convierte segundos en una duración, y `ToString` la escribe como un reloj:

```csharp
string t = TimeSpan.FromSeconds(130).ToString(@"m\:ss");   // 2:10
```

#### Desafío
Mostrá el segundo de cada aviso como reloj: `TimeSpan.FromSeconds(a.Segundo).ToString(@"m\:ss")`.

#### Código inicial
```csharp
List<Aviso> guion = [new(3, "Lola", Accion.Entra), new(65, "Lola", Accion.Sale)];

foreach (Aviso a in guion)
{
    string reloj = $"{a.Segundo} s";
    Console.WriteLine($"{reloj} {a.Titere} {a.Accion}");
}

record Aviso(int Segundo, string Titere, Accion Accion);
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Salida esperada
```
0:03 Lola Entra
1:05 Lola Sale
```

#### Solución
```csharp
List<Aviso> guion = [new(3, "Lola", Accion.Entra), new(65, "Lola", Accion.Sale)];

foreach (Aviso a in guion)
{
    string reloj = TimeSpan.FromSeconds(a.Segundo).ToString(@"m\:ss");
    Console.WriteLine($"{reloj} {a.Titere} {a.Accion}");
}

record Aviso(int Segundo, string Titere, Accion Accion);
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Al superarla
Hilván pega el guion al lado del reloj. Ahora solo tiene que mirar las agujas.

#### Imagen
- Detrás del telón rojo, un reloj redondo grande de madera colgado en la pared, sin números ni letras, con una tira de papel pegada al lado.
- Hilván pega la tira con una chinche; Ceci le alcanza otra.

### Micro-misión S01-N02-P4 · Lo que hace Lola

```meta
lugar: El Teatro del Titiritero
personajes: Ceci, Hilván, Clave
carta: Where | guion.Where(a => a.Titere == "Lola") · solo los que cumplen · el orden se mantiene
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Lola es la títere más difícil de manejar: Hilván quiere practicar solo sus avisos, sin los de los demás. El programa le muestra el guion entero.

#### Gheco sugiere
`Where` deja pasar solo los elementos que cumplen la condición:

```csharp
var altos = jugadores.Where(j => j.Nivel >= 10);
```

#### Desafío
Recorré `guion.Where(a => a.Titere == "Lola")` en vez de `guion`.

#### Código inicial
```csharp
List<Aviso> guion =
[
    new(3, "Lola", Accion.Entra),
    new(5, "Pipo", Accion.Entra),
    new(12, "Lola", Accion.Baila),
    new(20, "Pipo", Accion.Habla),
    new(30, "Lola", Accion.Para),
];

foreach (Aviso a in guion)
{
    Console.WriteLine($"{a.Segundo}s {a.Accion}");
}

record Aviso(int Segundo, string Titere, Accion Accion);
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Salida esperada
```
3s Entra
12s Baila
30s Para
```

#### Solución
```csharp
List<Aviso> guion =
[
    new(3, "Lola", Accion.Entra),
    new(5, "Pipo", Accion.Entra),
    new(12, "Lola", Accion.Baila),
    new(20, "Pipo", Accion.Habla),
    new(30, "Lola", Accion.Para),
];

foreach (Aviso a in guion.Where(a => a.Titere == "Lola"))
{
    Console.WriteLine($"{a.Segundo}s {a.Accion}");
}

record Aviso(int Segundo, string Titere, Accion Accion);
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Al superarla
Hilván ensaya los tres avisos de Lola una y otra vez. Clave lo mira desde la puerta. —Así se estudia una parte difícil: sola, despacio, y después con todos.

#### Imagen
- El escenario del teatrito vacío salvo por una bailarina de madera, iluminada por un solo farol, sin letras.
- Hilván ensaya con la bailarina, concentrado; Clave, con su capa y la mecha blanca, mira apoyada en el marco de la puerta.

### Micro-misión S01-N02-P5 · El ogro del final adelantado

```meta
lugar: Detrás del telón
personajes: Ceci, Hilván, Gheco
criatura: ogro
carta: Ogro | Last() es el último de la lista, no de la función · Max(a => a.Segundo) mira todos
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un ogro de la Feria se ofreció a bajar el telón al final. Calcula cuánto dura la función mirando el **último** aviso de la lista, y baja el telón a los 12 segundos, en la mitad del baile de Lola.

#### Gheco sugiere
El último aviso de la lista no es el último de la función: el guion no está en orden. `Max` mira todos y devuelve el más grande:

```csharp
int record = puntajes.Max(p => p.Puntos);
```

#### Desafío
Cambiá `guion.Last().Segundo` por `guion.Max(a => a.Segundo)`.

#### Código inicial
```csharp
List<Aviso> guion =
[
    new(3, "Lola", Accion.Entra),
    new(65, "Lola", Accion.Sale),
    new(12, "Pipo", Accion.Entra),
];

int dura = guion.Last().Segundo;
Console.WriteLine($"El telón baja a los {TimeSpan.FromSeconds(dura).ToString(@"m\:ss")}");

record Aviso(int Segundo, string Titere, Accion Accion);
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Salida esperada
```
El telón baja a los 1:05
```

#### Solución
```csharp
List<Aviso> guion =
[
    new(3, "Lola", Accion.Entra),
    new(65, "Lola", Accion.Sale),
    new(12, "Pipo", Accion.Entra),
];

int dura = guion.Max(a => a.Segundo);
Console.WriteLine($"El telón baja a los {TimeSpan.FromSeconds(dura).ToString(@"m\:ss")}");

record Aviso(int Segundo, string Titere, Accion Accion);
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Al superarla
El ogro espera con la soga en la mano hasta que Lola sale. Recién ahí baja el telón, despacito, y el público aplaude más fuerte que nunca.

#### Imagen
- Un telón rojo de teatro de títeres bajando despacio, con una soga gruesa, sin letras.
- El ogro grandote, con camisa cerrada, sostiene la soga con cuidado exagerado; Gheco, MINÚSCULO, flota a su lado haciéndole señas de «todavía no».

## S01-N03 · El ensayo general

```meta
tipo: tema
padre: S01-N02
precio: 10
criatura: troll
temas: err.validacion, diseno.maquina-estados
usa: err.excepciones, func.streams
```

### Crónica

La noche antes del estreno, Hilván quiere un **ensayo general**: pasar el guion entero de principio a fin, con la máquina de estados, y anotar todo lo que esté mal. —Pero que no se pare en el primer error —pide—. Si hay cinco, quiero saber los cinco antes de dormirme.

Bemol aparece con un paquete de pochoclos. —Yo hago de público.

### Objetivos

- Pasar el guion **en orden** por la máquina de estados.
- Atrapar cada error **adentro** del bucle, anotarlo y seguir.
- Decir en qué segundo pasó cada problema.
- Revisar al final que ningún títere se haya quedado en escena.
- Preguntar por algo que puede no estar, con `?.` y `??`.

### Antes de empezar

- La máquina de estados (S01-N01), la línea de tiempo (S01-N02) y `null` (R02-N06).

### Explicación

#### Anotar y seguir

Un `try`/`catch` **afuera** del bucle corta todo en el primer error. **Adentro**, atrapa ese aviso, lo anota y el bucle sigue con el próximo:

```csharp
List<string> problemas = [];
foreach (Aviso a in enOrden)
{
    try
    {
        estados[a.Titere] = Siguiente(estados.GetValueOrDefault(a.Titere), a.Accion);
    }
    catch (InvalidOperationException ex)
    {
        problemas.Add($"{a.Segundo}s: {a.Titere}, {ex.Message}");
    }
}
```

Esto se llama **validar**: revisar todo antes de usarlo y juntar los errores en una lista.

#### Lo que quedó al final

Cuando termina el guion, todos los títeres tienen que estar guardados. Se pregunta al diccionario:

```csharp
foreach (var (titere, estado) in estados.Where(e => e.Value != Estado.Guardado))
{
    problemas.Add($"{titere} quedó en {estado}");
}
```

#### Algo que puede no estar

`FirstOrDefault` devuelve el primero que cumple, o `null` si no hay ninguno. Con `?.` se pide algo **solo si no es `null`**, y con `??` se da un valor para cuando sí lo es:

```csharp
Aviso? entrada = guion.FirstOrDefault(a => a.Titere == "Pepa");
string cuando = entrada?.Segundo.ToString() ?? "nunca";
```

### Código de ejemplo

```csharp
List<Aviso> guion =
[
    new(3, "Lola", Accion.Entra),
    new(8, "Pipo", Accion.Baila),
    new(12, "Lola", Accion.Baila),
    new(20, "Lola", Accion.Sale),
];

Dictionary<string, Estado> estados = new();
List<string> problemas = [];

foreach (Aviso a in guion.OrderBy(a => a.Segundo))
{
    try
    {
        estados[a.Titere] = Siguiente(estados.GetValueOrDefault(a.Titere), a.Accion);
    }
    catch (InvalidOperationException ex)
    {
        problemas.Add($"{a.Segundo}s: {a.Titere}, {ex.Message}");
    }
}

foreach (var (titere, estado) in estados.Where(e => e.Value != Estado.Guardado))
{
    problemas.Add($"{titere} quedó en {estado}");
}

Console.WriteLine(problemas.Count == 0 ? "Ensayo sin problemas" : string.Join("\n", problemas));

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Habla) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Baila) => Estado.Bailando,
    (Estado.Bailando, Accion.Para) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Sale) => Estado.Guardado,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

record Aviso(int Segundo, string Titere, Accion Accion);
enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

### Salida esperada

```
8s: Pipo, Baila no se puede estando Guardado
20s: Lola, Sale no se puede estando Bailando
Lola quedó en Bailando
```

### ¿Para qué sirve?

Así validan los formularios (te muestran **todos** los campos mal, no de a uno), los compiladores (la lista de errores de C#) y los programas que importan datos. Juntar los problemas y mostrarlos al final es mucho más amable que cortar en el primero.

### Errores habituales

- **El `try` afuera del bucle:** se para en el primer problema, y los demás no se ven.
- **Ensayar el guion desordenado:** aparecen errores que no existen (Lola baila antes de entrar porque su entrada estaba más abajo).
- **Usar lo que devuelve `FirstOrDefault` sin mirar si es `null`:** es el **troll** de lo que no está.

### Micro-misión S01-N03-P1 · Ensayar en orden

```meta
lugar: El Teatro del Titiritero
personajes: Ceci, Hilván, Bemol
carta: Validar en orden | foreach (Aviso a in guion.OrderBy(a => a.Segundo)) · un guion escrito a mano nunca viene ordenado
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
El ensayo general dice que Lola baila sin haber entrado. Hilván jura que no: la entrada está en el guion, a los 3 segundos. Lo que pasa es que está escrita más abajo.

#### Gheco sugiere
Validar el guion en el orden en que está escrito da errores que no existen. Primero se ordena, después se ensaya:

```csharp
foreach (var p in pedidos.OrderBy(p => p.Hora)) { }
```

#### Desafío
Ensayá `guion.OrderBy(a => a.Segundo)` en vez de `guion`.

#### Código inicial
```csharp
List<Aviso> guion = [new(12, "Lola", Accion.Baila), new(3, "Lola", Accion.Entra)];
Dictionary<string, Estado> estados = new();
List<string> problemas = [];

foreach (Aviso a in guion)
{
    try
    {
        estados[a.Titere] = Siguiente(estados.GetValueOrDefault(a.Titere), a.Accion);
    }
    catch (InvalidOperationException ex)
    {
        problemas.Add($"{a.Segundo}s: {a.Titere}, {ex.Message}");
    }
}

Console.WriteLine(problemas.Count == 0 ? "Ensayo sin problemas" : string.Join("\n", problemas));

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Baila) => Estado.Bailando,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

record Aviso(int Segundo, string Titere, Accion Accion);
enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Salida esperada
```
Ensayo sin problemas
```

#### Solución
```csharp
List<Aviso> guion = [new(12, "Lola", Accion.Baila), new(3, "Lola", Accion.Entra)];
Dictionary<string, Estado> estados = new();
List<string> problemas = [];

foreach (Aviso a in guion.OrderBy(a => a.Segundo))
{
    try
    {
        estados[a.Titere] = Siguiente(estados.GetValueOrDefault(a.Titere), a.Accion);
    }
    catch (InvalidOperationException ex)
    {
        problemas.Add($"{a.Segundo}s: {a.Titere}, {ex.Message}");
    }
}

Console.WriteLine(problemas.Count == 0 ? "Ensayo sin problemas" : string.Join("\n", problemas));

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Baila) => Estado.Bailando,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

record Aviso(int Segundo, string Titere, Accion Accion);
enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Al superarla
—¿Ves? —dice Hilván—. Estaba bien. Bemol, desde la primera fila, aplaude con la boca llena de pochoclos.

#### Imagen
- Las butacas de madera de un teatro de títeres de feria, casi vacías, mirando a un teatrito con el telón abierto, sin letras.
- Bemol, MUY GORDITO con panza, sentado en la primera fila con un paquete de pochoclos; Hilván, en el escenario, con una títere bailarina; Ceci, al costado, con una lista.

### Micro-misión S01-N03-P2 · Anotar y seguir

```meta
lugar: El Teatro del Titiritero
personajes: Ceci, Hilván
carta: try adentro | el try va DENTRO del foreach · el catch anota en la lista · el bucle sigue
recompensa: xp 15, oro 15
```

#### Escena
El guion tiene dos errores, pero el ensayo se para en el primero. Hilván lo arregla, vuelve a ensayar y aparece el segundo. —Así no duermo nunca.

#### Gheco sugiere
Si el `try` está **afuera** del bucle, el primer error lo corta todo. Si está **adentro**, atrapa el error de ese paso y el bucle sigue:

```csharp
foreach (string linea in lineas)
{
    try { numeros.Add(int.Parse(linea)); }
    catch (FormatException) { malas++; }
}
```

#### Desafío
Mové el `try`/`catch` adentro del `foreach`, alrededor de la línea de `estados[...]`.

#### Código inicial
```csharp
List<Aviso> guion = [new(3, "Pipo", Accion.Sale), new(8, "Lola", Accion.Baila)];
Dictionary<string, Estado> estados = new();
List<string> problemas = [];

try
{
    foreach (Aviso a in guion.OrderBy(a => a.Segundo))
    {
        estados[a.Titere] = Siguiente(estados.GetValueOrDefault(a.Titere), a.Accion);
    }
}
catch (InvalidOperationException ex)
{
    problemas.Add(ex.Message);
}

Console.WriteLine(string.Join("\n", problemas));

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Baila) => Estado.Bailando,
    (Estado.EnEscena, Accion.Sale) => Estado.Guardado,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

record Aviso(int Segundo, string Titere, Accion Accion);
enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Salida esperada
```
Sale no se puede estando Guardado
Baila no se puede estando Guardado
```

#### Solución
```csharp
List<Aviso> guion = [new(3, "Pipo", Accion.Sale), new(8, "Lola", Accion.Baila)];
Dictionary<string, Estado> estados = new();
List<string> problemas = [];

foreach (Aviso a in guion.OrderBy(a => a.Segundo))
{
    try
    {
        estados[a.Titere] = Siguiente(estados.GetValueOrDefault(a.Titere), a.Accion);
    }
    catch (InvalidOperationException ex)
    {
        problemas.Add(ex.Message);
    }
}

Console.WriteLine(string.Join("\n", problemas));

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Baila) => Estado.Bailando,
    (Estado.EnEscena, Accion.Sale) => Estado.Guardado,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

record Aviso(int Segundo, string Titere, Accion Accion);
enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Al superarla
Los dos errores aparecen juntos. Hilván los arregla de una vez y se va a dormir temprano, por primera vez en una semana.

#### Imagen
- Un cuaderno abierto sobre una mesa de madera detrás del telón, con dos marcas rojas en la página sin letras legibles, iluminado por un farol.
- Hilván bosteza y estira los brazos; Ceci cierra el cuaderno.

### Micro-misión S01-N03-P3 · ¿En qué segundo?

```meta
lugar: Detrás del telón
personajes: Ceci, Hilván, Gheco
carta: Mensaje útil | $"{a.Segundo}s: {a.Titere}, {ex.Message}" · decí dónde pasó, no solo qué
recompensa: xp 15, oro 15
```

#### Escena
El ensayo dice «Baila no se puede estando Guardado», pero no dice **quién** ni **cuándo**. Hilván tiene cinco títeres y una función de dos minutos.

#### Gheco sugiere
Un buen mensaje de error dice qué pasó **y dónde**. El `catch` tiene a mano el aviso del bucle (`a`), así que puede sumarlo:

```csharp
errores.Add($"Línea {numero}: {ex.Message}");
```

#### Desafío
Cambiá `problemas.Add(ex.Message);` por `problemas.Add($"{a.Segundo}s: {a.Titere}, {ex.Message}");`.

#### Código inicial
```csharp
List<Aviso> guion = [new(3, "Lola", Accion.Entra), new(15, "Pipo", Accion.Baila)];
Dictionary<string, Estado> estados = new();
List<string> problemas = [];

foreach (Aviso a in guion.OrderBy(a => a.Segundo))
{
    try
    {
        estados[a.Titere] = Siguiente(estados.GetValueOrDefault(a.Titere), a.Accion);
    }
    catch (InvalidOperationException ex)
    {
        problemas.Add(ex.Message);
    }
}

Console.WriteLine(string.Join("\n", problemas));

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Baila) => Estado.Bailando,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

record Aviso(int Segundo, string Titere, Accion Accion);
enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Salida esperada
```
15s: Pipo, Baila no se puede estando Guardado
```

#### Solución
```csharp
List<Aviso> guion = [new(3, "Lola", Accion.Entra), new(15, "Pipo", Accion.Baila)];
Dictionary<string, Estado> estados = new();
List<string> problemas = [];

foreach (Aviso a in guion.OrderBy(a => a.Segundo))
{
    try
    {
        estados[a.Titere] = Siguiente(estados.GetValueOrDefault(a.Titere), a.Accion);
    }
    catch (InvalidOperationException ex)
    {
        problemas.Add($"{a.Segundo}s: {a.Titere}, {ex.Message}");
    }
}

Console.WriteLine(string.Join("\n", problemas));

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Baila) => Estado.Bailando,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

record Aviso(int Segundo, string Titere, Accion Accion);
enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Al superarla
—Quince segundos, Pipo —lee Hilván—. Claro: lo hice bailar antes de que entrara. Lo arregla con un solo trazo.

#### Imagen
- Detrás del telón, el reloj de madera grande sin números, con una aguja señalando un cuarto, sin letras.
- Hilván señala el reloj con un lápiz; Gheco, MINÚSCULO, sentado en la aguja del reloj, mira hacia abajo; un payaso títere cuelga a medio entrar.

### Micro-misión S01-N03-P4 · Nadie se queda en escena

```meta
lugar: El Teatro del Titiritero
personajes: Ceci, Hilván, Bemol
carta: Revisar al final | estados.Where(e => e.Value != Estado.Guardado) · los que no volvieron a la caja
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
El ensayo no encuentra errores, pero cuando baja el telón, Pipo queda colgado en el medio del escenario. Nadie lo hizo salir. Bemol se ríe tanto que se le caen los pochoclos.

#### Gheco sugiere
Al terminar el guion, todos tienen que estar guardados. `Where` sobre el diccionario encuentra a los que no:

```csharp
foreach (var (nombre, nivel) in niveles.Where(n => n.Value > 10))
{
    Console.WriteLine($"{nombre} pasó el nivel 10");
}
```

#### Desafío
Después del ensayo, recorré `estados.Where(e => e.Value != Estado.Guardado)` y agregá a `problemas` el texto `{titere} quedó en {estado}`.

#### Código inicial
```csharp
List<Aviso> guion = [new(3, "Lola", Accion.Entra), new(5, "Pipo", Accion.Entra), new(30, "Lola", Accion.Sale)];
Dictionary<string, Estado> estados = new();
List<string> problemas = [];

foreach (Aviso a in guion.OrderBy(a => a.Segundo))
{
    try
    {
        estados[a.Titere] = Siguiente(estados.GetValueOrDefault(a.Titere), a.Accion);
    }
    catch (InvalidOperationException ex)
    {
        problemas.Add($"{a.Segundo}s: {a.Titere}, {ex.Message}");
    }
}

// revisá quién quedó afuera de la caja


Console.WriteLine(problemas.Count == 0 ? "Ensayo sin problemas" : string.Join("\n", problemas));

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Sale) => Estado.Guardado,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

record Aviso(int Segundo, string Titere, Accion Accion);
enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Salida esperada
```
Pipo quedó en EnEscena
```

#### Solución
```csharp
List<Aviso> guion = [new(3, "Lola", Accion.Entra), new(5, "Pipo", Accion.Entra), new(30, "Lola", Accion.Sale)];
Dictionary<string, Estado> estados = new();
List<string> problemas = [];

foreach (Aviso a in guion.OrderBy(a => a.Segundo))
{
    try
    {
        estados[a.Titere] = Siguiente(estados.GetValueOrDefault(a.Titere), a.Accion);
    }
    catch (InvalidOperationException ex)
    {
        problemas.Add($"{a.Segundo}s: {a.Titere}, {ex.Message}");
    }
}

foreach (var (titere, estado) in estados.Where(e => e.Value != Estado.Guardado))
{
    problemas.Add($"{titere} quedó en {estado}");
}

Console.WriteLine(problemas.Count == 0 ? "Ensayo sin problemas" : string.Join("\n", problemas));

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Sale) => Estado.Guardado,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

record Aviso(int Segundo, string Titere, Accion Accion);
enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Al superarla
Hilván agrega «a los 40, Pipo sale», y en el próximo ensayo Pipo se despide con una reverencia antes de que baje el telón.

#### Imagen
- El telón rojo bajando y, delante, un payaso títere colgado solo en el medio del escenario, con los hilos flojos, sin letras.
- Bemol, MUY GORDITO con panza, se ríe con los pochoclos volando; Hilván se tapa la cara; Ceci contiene la risa.

### Micro-misión S01-N03-P5 · El troll de la títere que no viene

```meta
lugar: Detrás del telón
personajes: Ceci, Hilván, Gheco
criatura: troll
carta: Troll | FirstOrDefault puede dar null · entrada?.Segundo: solo si hay algo · ?? "nunca": para cuando no hay
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Hilván pregunta a qué segundo entra Pepa. Pero Pepa no está en el guion de esta noche: `FirstOrDefault` devuelve `null`, y un troll se sienta arriba del programa y lo rompe.

#### Gheco sugiere
`?.` pide algo **solo si** no es `null` (si es `null`, da `null` sin romper), y `??` pone un valor para ese caso:

```csharp
string titulo = obra?.Titulo ?? "sin título";
```

#### Desafío
Cambiá la línea de `cuando` por `string cuando = entrada?.Segundo.ToString() ?? "nunca";`.

#### Código inicial
```csharp
List<Aviso> guion = [new(3, "Lola", Accion.Entra), new(5, "Pipo", Accion.Entra)];

Aviso? entrada = guion.FirstOrDefault(a => a.Titere == "Pepa" && a.Accion == Accion.Entra);
string cuando = entrada!.Segundo.ToString();
Console.WriteLine($"Pepa entra: {cuando}");

record Aviso(int Segundo, string Titere, Accion Accion);
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Salida esperada
```
Pepa entra: nunca
```

#### Solución
```csharp
List<Aviso> guion = [new(3, "Lola", Accion.Entra), new(5, "Pipo", Accion.Entra)];

Aviso? entrada = guion.FirstOrDefault(a => a.Titere == "Pepa" && a.Accion == Accion.Entra);
string cuando = entrada?.Segundo.ToString() ?? "nunca";
Console.WriteLine($"Pepa entra: {cuando}");

record Aviso(int Segundo, string Titere, Accion Accion);
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Al superarla
—Nunca —lee Hilván—. Es verdad: Pepa descansa esta noche. El troll, sin nada donde sentarse, se acomoda en la caja de Pepa y se queda dormido.

#### Imagen
- Detrás del telón, una caja de títeres abierta y vacía, con un almohadón adentro, sin letras.
- Un troll gris chiquito se acomoda en la caja, bostezando; Hilván lo mira con una ceja levantada; Gheco, MINÚSCULO, le tapa la cabeza con un pañuelo.

## S01-N04 · Jefe: el Apuntador Fantasma

```meta
tipo: jefe
padre: S01-N03
precio: 10
criatura: dragon
insignia: Guionista del Teatro
insignia_descripcion: Venciste al Apuntador Fantasma: tus guiones tienen estados, línea de tiempo y ensayo general, y viajan en JSON al tablero de JavaScript del Teatro.
temas: arch.json, web.api-rest
usa: diseno.maquina-estados, err.validacion, func.streams, poo.records
```

### Crónica

La noche del estreno, el teatro está lleno. Nima, en la cabina, tiene el tablero de JavaScript listo: solo falta que le llegue el guion. Ceci lo manda en JSON, como le enseñaron en el Archivo Mudo.

Y el tablero no lo entiende. Los títeres se quedan quietos. En el agujero del apuntador, debajo del escenario, aparece una figura transparente con un libreto enorme: **el Apuntador Fantasma**, que lleva cien años soplando el guion **mal**. Cambia las mayúsculas, convierte las acciones en números y mete notas suyas donde no van.

—Mi tablero espera los nombres como los escribimos en JavaScript —grita Nima desde la cabina—: `segundo`, `titere`, `accion`. ¡Con minúscula!

### Objetivos

- Escribir el JSON con los nombres en **camelCase**, como en JavaScript (`JsonNamingPolicy.CamelCase`).
- Escribir los `enum` como texto, no como número (`JsonStringEnumConverter`).
- Leer un JSON que viene de JavaScript sin que importen las mayúsculas (`PropertyNameCaseInsensitive`).
- Dejar afuera del JSON lo que no tiene que viajar (`[JsonIgnore]`).
- No mandar nunca un guion que no pasó el ensayo.

### Antes de empezar

- JSON (R04-N06) y toda la Senda del Teatro (S01-N01 a N03).

### Explicación

#### Dos lenguajes, dos costumbres

C# escribe las propiedades con mayúscula (`Segundo`), y JavaScript, en **camelCase**: la primera palabra en minúscula (`segundo`, `nombreCompleto`). Para que los dos se entiendan, el JSON tiene que usar la costumbre del que lo lee. Las opciones de `JsonSerializer` lo arreglan sin tocar el `record`:

```csharp
using System.Text.Json;
using System.Text.Json.Serialization;

var opciones = new JsonSerializerOptions
{
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,   // Segundo → segundo
    Converters = { new JsonStringEnumConverter() },      // Accion.Entra → "Entra", no 0
};
string json = JsonSerializer.Serialize(guion, opciones);
```

`JsonStringEnumConverter` está en `System.Text.Json.Serialization`: por eso el segundo `using`.

#### Leer lo que manda JavaScript

Al leer, `Deserialize` busca los nombres **exactos**: `aplausos` no es `Aplausos`, y la propiedad queda vacía sin avisar. Con `PropertyNameCaseInsensitive = true`, no importan las mayúsculas:

```csharp
var leer = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
Respuesta r = JsonSerializer.Deserialize<Respuesta>(texto, leer)!;
```

#### Lo que no viaja

`[JsonIgnore]` arriba de una propiedad la deja afuera del JSON:

```csharp
record Aviso(int Segundo, string Titere, Accion Accion)
{
    [JsonIgnore]
    public string? Nota { get; init; }
}
```

### Código de ejemplo

```csharp
using System.Text.Json;
using System.Text.Json.Serialization;

List<Aviso> guion = [new(3, "Lola", Accion.Entra), new(12, "Lola", Accion.Baila)];

var opciones = new JsonSerializerOptions
{
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
    Converters = { new JsonStringEnumConverter() },
};
Console.WriteLine(JsonSerializer.Serialize(guion, opciones));

string delTeatro = """{"funcion":"La Bailarina","aplausos":42}""";
var leer = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
Respuesta r = JsonSerializer.Deserialize<Respuesta>(delTeatro, leer)!;
Console.WriteLine($"{r.Funcion}: {r.Aplausos} aplausos");

record Aviso(int Segundo, string Titere, Accion Accion);
record Respuesta(string Funcion, int Aplausos);
enum Accion { Entra, Habla, Baila, Para, Sale }
```

### Salida esperada

```
[{"segundo":3,"titere":"Lola","accion":"Entra"},{"segundo":12,"titere":"Lola","accion":"Baila"}]
La Bailarina: 42 aplausos
```

### ¿Para qué sirve?

Casi todo programa de C# de verdad habla con otro escrito en otro lenguaje: una página en JavaScript, una app de celular, un servidor en PHP. El JSON es el idioma en común, y estas opciones son las que se tocan siempre. ASP.NET, la ventanilla de verdad, las usa así por defecto.

### Errores habituales

- **Mandar los nombres con mayúscula a JavaScript:** el tablero busca `segundo` y no lo encuentra.
- **Mandar los `enum` como número:** `"accion":0` no le dice nada a quien lee del otro lado.
- **Leer sin `PropertyNameCaseInsensitive`:** las propiedades quedan en `null` o `0`, sin error.
- **Olvidarse el `using System.Text.Json.Serialization;`:** `JsonStringEnumConverter` y `JsonIgnore` viven ahí.

### Micro-misión S01-N04-P1 · Con minúscula

```meta
lugar: El Teatro del Titiritero
personajes: Ceci, Hilván, Nima
criatura: dragon
carta: Jefe | PropertyNamingPolicy = JsonNamingPolicy.CamelCase · Segundo → segundo · como en JavaScript
recompensa: xp 25, oro 25
```

#### Escena
El Apuntador Fantasma sopla los nombres con mayúscula, y el tablero de Nima busca `segundo`, `titere` y `accion` sin encontrarlos. Los títeres se quedan quietos frente al público.

#### Gheco sugiere
`PropertyNamingPolicy = JsonNamingPolicy.CamelCase` escribe cada propiedad con la primera letra en minúscula, sin cambiar el `record`:

```csharp
var opciones = new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase };
// NombreCompleto → nombreCompleto
```

#### Desafío
Agregale a `opciones` la línea `PropertyNamingPolicy = JsonNamingPolicy.CamelCase,`.

#### Código inicial
```csharp
using System.Text.Json;

List<Aviso> guion = [new(3, "Lola", "Entra")];

var opciones = new JsonSerializerOptions
{
};
Console.WriteLine(JsonSerializer.Serialize(guion, opciones));

record Aviso(int Segundo, string Titere, string Accion);
```

#### Salida esperada
```
[{"segundo":3,"titere":"Lola","accion":"Entra"}]
```

#### Solución
```csharp
using System.Text.Json;

List<Aviso> guion = [new(3, "Lola", "Entra")];

var opciones = new JsonSerializerOptions
{
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
};
Console.WriteLine(JsonSerializer.Serialize(guion, opciones));

record Aviso(int Segundo, string Titere, string Accion);
```

#### Al superarla
El tablero lee el primer aviso y Lola entra al escenario. Debajo, el Apuntador Fantasma cierra el libreto de un golpe, enojado.

#### Imagen
- Un teatro de títeres de feria lleno de público en penumbra, con el escenario iluminado y un agujero de apuntador con forma de concha en el borde, sin letras.
- Una figura fantasmal transparente y celeste, con un libreto enorme, asoma enojada desde el agujero; Nima, arquera de trenza, en una cabina al fondo; Hilván maneja una bailarina; Ceci mira desde un costado.

### Micro-misión S01-N04-P2 · Acciones con nombre

```meta
lugar: El Teatro del Titiritero
personajes: Ceci, Nima, Gheco
criatura: dragon
carta: Jefe | Converters = { new JsonStringEnumConverter() } · Accion.Baila → "Baila", no 2 · using System.Text.Json.Serialization
recompensa: xp 25, oro 25
```

#### Escena
Ahora el Apuntador sopla las acciones como números: `"accion":2`. El tablero no sabe si 2 es bailar, entrar o salir, y Lola se queda dudando en el medio del escenario.

#### Gheco sugiere
Un `enum` se guarda como número salvo que se agregue un convertidor que lo escriba como texto:

```csharp
var opciones = new JsonSerializerOptions { Converters = { new JsonStringEnumConverter() } };
// Dificultad.Dificil → "Dificil"
```

#### Desafío
Agregale a `opciones` la línea `Converters = { new JsonStringEnumConverter() },`. El `using` que hace falta ya está.

#### Código inicial
```csharp
using System.Text.Json;
using System.Text.Json.Serialization;

List<Aviso> guion = [new(12, "Lola", Accion.Baila)];

var opciones = new JsonSerializerOptions
{
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
};
Console.WriteLine(JsonSerializer.Serialize(guion, opciones));

record Aviso(int Segundo, string Titere, Accion Accion);
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Salida esperada
```
[{"segundo":12,"titere":"Lola","accion":"Baila"}]
```

#### Solución
```csharp
using System.Text.Json;
using System.Text.Json.Serialization;

List<Aviso> guion = [new(12, "Lola", Accion.Baila)];

var opciones = new JsonSerializerOptions
{
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
    Converters = { new JsonStringEnumConverter() },
};
Console.WriteLine(JsonSerializer.Serialize(guion, opciones));

record Aviso(int Segundo, string Titere, Accion Accion);
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Al superarla
Lola gira, porque ahora sabe que le toca bailar. El público aplaude, y el Apuntador Fantasma se hunde un poco en su agujero.

#### Imagen
- El escenario del teatro de títeres con una bailarina de madera girando bajo un foco, sin letras.
- El fantasma transparente con su libreto, hundido hasta el pecho en el agujero del apuntador; Nima, en la cabina, levanta el pulgar; Gheco, MINÚSCULO, sentado en el borde del escenario.

### Micro-misión S01-N04-P3 · La respuesta del Teatro

```meta
lugar: El Teatro del Titiritero
personajes: Ceci, Hilván, Nima
criatura: dragon
carta: Jefe | PropertyNameCaseInsensitive = true · "aplausos" llena Aplausos · sin eso, queda en 0 sin avisar
recompensa: xp 25, oro 25
```

#### Escena
Al terminar el primer acto, el tablero de Nima le devuelve a Ceci un JSON con los aplausos. El programa de Ceci lo lee y dice cero. El Apuntador se ríe: los nombres vienen en minúscula, y C# los buscó con mayúscula.

#### Gheco sugiere
`Deserialize` busca los nombres exactos. Con `PropertyNameCaseInsensitive = true`, `aplausos` llena `Aplausos`:

```csharp
var leer = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
```

#### Desafío
Agregale a `leer` la línea `PropertyNameCaseInsensitive = true,`.

#### Código inicial
```csharp
using System.Text.Json;

string delTeatro = """{"funcion":"La Bailarina","aplausos":42}""";

var leer = new JsonSerializerOptions
{
};
Respuesta r = JsonSerializer.Deserialize<Respuesta>(delTeatro, leer)!;
Console.WriteLine($"{r.Funcion ?? "?"}: {r.Aplausos} aplausos");

record Respuesta(string? Funcion, int Aplausos);
```

#### Salida esperada
```
La Bailarina: 42 aplausos
```

#### Solución
```csharp
using System.Text.Json;

string delTeatro = """{"funcion":"La Bailarina","aplausos":42}""";

var leer = new JsonSerializerOptions
{
    PropertyNameCaseInsensitive = true,
};
Respuesta r = JsonSerializer.Deserialize<Respuesta>(delTeatro, leer)!;
Console.WriteLine($"{r.Funcion ?? "?"}: {r.Aplausos} aplausos");

record Respuesta(string? Funcion, int Aplausos);
```

#### Al superarla
Cuarenta y dos aplausos. Hilván los cuenta dos veces, porque no lo puede creer. El Apuntador Fantasma tira su libreto al piso.

#### Imagen
- Público de feria aplaudiendo en las butacas de un teatro de títeres, en penumbra, sin letras.
- Hilván, con los hilos dorados en la mano, sonríe sin poder creerlo; Ceci lo abraza de costado; Nima saluda desde la cabina.

### Micro-misión S01-N04-P4 · Las notas del Apuntador

```meta
lugar: El Teatro del Titiritero
personajes: Ceci, Hilván, Gheco
criatura: dragon
carta: Jefe | [JsonIgnore] arriba de la propiedad · no viaja en el JSON · sigue en el objeto
recompensa: xp 25, oro 25, monedas 3
```

#### Escena
El Apuntador mete sus notas en el guion: «acá Pipo se cae», «acá Lola se olvida el paso». Las notas viajan en el JSON al tablero, y el tablero las muestra en la pantalla del teatro, delante de todos.

#### Gheco sugiere
`[JsonIgnore]` arriba de una propiedad la deja afuera del JSON. En el programa, la nota sigue estando; solo no viaja:

```csharp
record Jugador(string Nombre)
{
    [JsonIgnore]
    public string? Clave { get; init; }
}
```

#### Desafío
Poné `[JsonIgnore]` arriba de la propiedad `Nota`.

#### Código inicial
```csharp
using System.Text.Json;
using System.Text.Json.Serialization;

Aviso aviso = new(20, "Pipo", "Entra") { Nota = "aca Pipo se cae" };

var opciones = new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase };
Console.WriteLine(JsonSerializer.Serialize(aviso, opciones));

record Aviso(int Segundo, string Titere, string Accion)
{
    public string? Nota { get; init; }
}
```

#### Salida esperada
```
{"segundo":20,"titere":"Pipo","accion":"Entra"}
```

#### Solución
```csharp
using System.Text.Json;
using System.Text.Json.Serialization;

Aviso aviso = new(20, "Pipo", "Entra") { Nota = "aca Pipo se cae" };

var opciones = new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase };
Console.WriteLine(JsonSerializer.Serialize(aviso, opciones));

record Aviso(int Segundo, string Titere, string Accion)
{
    [JsonIgnore]
    public string? Nota { get; init; }
}
```

#### Al superarla
Las notas se quedan en el papel. Pipo entra y no se cae. Debajo del escenario, el Apuntador Fantasma busca su libreto y lo encuentra en blanco.

#### Imagen
- El agujero del apuntador en el borde del escenario, con hojas de papel en blanco volando alrededor, sin letras.
- El fantasma transparente hojea su libreto vacío, desconcertado; Gheco, MINÚSCULO, sentado en el borde, se ríe; Hilván, arriba, maneja al payaso títere.

### Micro-misión S01-N04-P5 · Solo lo que pasó el ensayo

```meta
lugar: El Teatro del Titiritero
personajes: Ceci, Hilván, Clave, Nima
criatura: dragon
carta: Jefe | ensayar primero · si hay problemas: mostrarlos y NO mandar · si no: mandar el JSON
recompensa: xp 30, oro 30, monedas 3
```

#### Escena
Su última trampa: el Apuntador mete en el guion un aviso que Pipo no puede cumplir, bailar sin haber entrado. El programa de Ceci lo ensaya, encuentra el problema… y manda el guion igual.

#### Gheco sugiere
Validar sirve si lo que no pasó **no sigue**. Un `if`/`else` decide: con problemas, se muestran; sin problemas, se manda:

```csharp
if (errores.Count > 0)
{
    Console.WriteLine("No se guarda");
}
else
{
    Guardar();
}
```

#### Desafío
Mandá el JSON **solo** si no hubo problemas: poné el `Console.WriteLine` del JSON en el `else` de un `if (problemas.Count > 0)` que muestre `No se estrena:` y después cada problema.

#### Código inicial
```csharp
using System.Text.Json;
using System.Text.Json.Serialization;

List<Aviso> guion = [new(3, "Lola", Accion.Entra), new(8, "Pipo", Accion.Baila)];
Dictionary<string, Estado> estados = new();
List<string> problemas = [];

foreach (Aviso a in guion.OrderBy(a => a.Segundo))
{
    try
    {
        estados[a.Titere] = Siguiente(estados.GetValueOrDefault(a.Titere), a.Accion);
    }
    catch (InvalidOperationException ex)
    {
        problemas.Add($"{a.Segundo}s: {a.Titere}, {ex.Message}");
    }
}

var opciones = new JsonSerializerOptions
{
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
    Converters = { new JsonStringEnumConverter() },
};
Console.WriteLine(JsonSerializer.Serialize(guion, opciones));

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Baila) => Estado.Bailando,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

record Aviso(int Segundo, string Titere, Accion Accion);
enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Salida esperada
```
No se estrena:
8s: Pipo, Baila no se puede estando Guardado
```

#### Solución
```csharp
using System.Text.Json;
using System.Text.Json.Serialization;

List<Aviso> guion = [new(3, "Lola", Accion.Entra), new(8, "Pipo", Accion.Baila)];
Dictionary<string, Estado> estados = new();
List<string> problemas = [];

foreach (Aviso a in guion.OrderBy(a => a.Segundo))
{
    try
    {
        estados[a.Titere] = Siguiente(estados.GetValueOrDefault(a.Titere), a.Accion);
    }
    catch (InvalidOperationException ex)
    {
        problemas.Add($"{a.Segundo}s: {a.Titere}, {ex.Message}");
    }
}

if (problemas.Count > 0)
{
    Console.WriteLine("No se estrena:");
    foreach (string p in problemas)
    {
        Console.WriteLine(p);
    }
}
else
{
    var opciones = new JsonSerializerOptions
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        Converters = { new JsonStringEnumConverter() },
    };
    Console.WriteLine(JsonSerializer.Serialize(guion, opciones));
}

Estado Siguiente(Estado e, Accion a) => (e, a) switch
{
    (Estado.Guardado, Accion.Entra) => Estado.EnEscena,
    (Estado.EnEscena, Accion.Baila) => Estado.Bailando,
    _ => throw new InvalidOperationException($"{a} no se puede estando {e}"),
};

record Aviso(int Segundo, string Titere, Accion Accion);
enum Estado { Guardado, EnEscena, Bailando }
enum Accion { Entra, Habla, Baila, Para, Sale }
```

#### Al superarla
El guion no sale. Hilván corrige la línea de Pipo («a los 6, entra»), Ceci lo ensaya otra vez, y recién entonces lo manda. La función sigue sin un solo hilo enredado. Cuando baja el telón, el Apuntador Fantasma sale de su agujero, aplaude despacito y se desvanece, contento por primera vez en cien años: alguien, por fin, ensayó. Clave le apoya una mano a Ceci en el hombro. No dice nada. No hace falta.

#### Imagen
- El teatro de títeres de feria con el telón bajando y el público de pie aplaudiendo, con farolitos, sin letras.
- El fantasma transparente, ya sonriente, aplaude y se desvanece en chispas celestes; Clave, con su capa y la mecha blanca, apoya la mano en el hombro de Ceci; Hilván y Nima festejan al fondo; Gheco, MINÚSCULO, en el hombro de Ceci.
