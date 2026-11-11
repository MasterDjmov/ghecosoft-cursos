# RAMA R04 · El Archivo Mudo: errores y archivos

```meta
tipo: tronco
posicion: 4
```

## R04-N01 · try y catch: que el concierto siga

```meta
tipo: tema
padre: R03-N10
precio: 10
criatura: goblin
temas: err.excepciones
usa: prog.variables, prog.bucles
```

### Crónica

En plena función, a un violinista se le corta una cuerda. El público ni se entera: un suplente sube desde el foso con otro violín y la obra sigue. Ceci mira la escena con la boca abierta.

—El mal concierto no es el que tiene un problema —dice {mentor}—. Es el que **se detiene** por él. Hasta ahora, cada vez que algo fallaba, tus programas se morían en el medio. Hoy aprendés a tener un suplente preparado.

Abajo, en el sótano, se oye un ruido de cajones. Nadie baja ahí desde hace años: es el **Archivo Mudo**.

### Objetivos

- Entender qué es una **excepción**: el error que aparece mientras el programa corre.
- Atraparla con `try` y `catch` para que el programa siga.
- Atrapar distintos errores con distintos `catch`.
- Usar `finally` para lo que tiene que pasar siempre.

### Antes de empezar

- Convertir texto a número con `int.Parse` (Acto I) y los arreglos (R01-N11).

### Explicación

#### Una excepción

Ya las viste: cuando `int.Parse("abc")` no puede convertir, o cuando pedís una posición que no existe, el programa se corta y muestra un mensaje que empieza con `Unhandled exception` («excepción sin atrapar»). Una **excepción** es eso: un error que aparece **mientras el programa corre**, no al compilar.

#### Atraparla: `try` y `catch`

```csharp
try
{
    int n = int.Parse("abc");      // acá falla
    Console.WriteLine(n);          // esto se saltea
}
catch (FormatException)
{
    Console.WriteLine("No es un número");
}
Console.WriteLine("Sigo");
```

- En el `try` («intentá») va el código que puede fallar.
- Si falla, el resto del `try` **se saltea** y corre el `catch` («atrapá») de ese error.
- Después, el programa **sigue** como si nada.
- Si no falla, el `catch` no corre.

`FormatException` es el error de `int.Parse` cuando el texto no es un número. Cada error tiene su nombre:

| Excepción | Cuándo |
|---|---|
| `FormatException` | `int.Parse("abc")` |
| `DivideByZeroException` | dividir un entero por cero |
| `IndexOutOfRangeException` | una posición que no existe en un arreglo |
| `NullReferenceException` | usar algo que vale `null` |
| `KeyNotFoundException` | una clave que no está en un diccionario |

#### Atrapar cualquiera

`catch (Exception e)` atrapa **cualquier** error, y lo guarda en `e`. `e.GetType().Name` da su nombre:

```csharp
catch (Exception e)
{
    Console.WriteLine(e.GetType().Name);   // IndexOutOfRangeException
}
```

#### `finally`: pase lo que pase

```csharp
try { … }
catch (FormatException) { … }
finally
{
    Console.WriteLine("esto corre siempre");
}
```

### Código de ejemplo

```csharp
string[] entradas = { "12", "doce", "7" };
int total = 0;
foreach (string e in entradas)
{
    try
    {
        total += int.Parse(e);
        Console.WriteLine($"Sumé {e}");
    }
    catch (FormatException)
    {
        Console.WriteLine($"'{e}' no es un número");
    }
}
Console.WriteLine($"Total: {total}");
```

### Salida esperada

```
Sumé 12
'doce' no es un número
Sumé 7
Total: 19
```

### ¿Para qué sirve?

Para que un dato malo no tire abajo todo. Un juego no se cierra porque un archivo de configuración tiene un error; una app no se cae porque el usuario escribió letras donde iba un número.

### Errores habituales

- **El `catch` vacío:** `catch { }` hace desaparecer el error sin avisar. El programa sigue haciendo cualquier cosa y no queda rastro. Siempre mostrá o hacé algo en el `catch`.
- **Atrapar otro error:** un `catch (FormatException)` no atrapa una `DivideByZeroException`. Si el error es otro, el programa se corta igual.
- **Creer que el resto del `try` corre:** después del error, lo que queda en el `try` se saltea.

### Micro-misión R04-N01-P1 · La cuerda que se corta

```meta
lugar: El Escenario Grande
personajes: Ceci, Clave
carta: try y catch | try { lo que puede fallar } · catch (FormatException) { el suplente } · después, sigue
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
El programa del concierto lee cuántos compases tiene la obra, pero alguien escribió `tres` con letras. Hoy el concierto se corta en el medio. Clave quiere que siga.

#### Gheco sugiere
`int.Parse("tres")` no puede convertir y lanza una **excepción**: un error mientras el programa corre. Si nadie la atrapa, el programa se muere ahí.

Para atraparla, el código que puede fallar va adentro de un `try`, y lo que hay que hacer si falla, en un `catch`:

```csharp
try
{
    int n = int.Parse("hola");
    Console.WriteLine(n);
}
catch (FormatException)
{
    Console.WriteLine("No es un número");
}
```

`FormatException` es el nombre del error de `int.Parse` cuando el texto no es un número.

#### Desafío
Envolvé las dos líneas del medio en un `try`, y agregá un `catch (FormatException)` que muestre `No es un número`.

#### Código inicial
```csharp
Console.WriteLine("Empieza el concierto");
string compases = "tres";

int n = int.Parse(compases);
Console.WriteLine($"Compases: {n}");

Console.WriteLine("El concierto sigue");
```

#### Salida esperada
```
Empieza el concierto
No es un número
El concierto sigue
```

#### Solución
```csharp
Console.WriteLine("Empieza el concierto");
string compases = "tres";

try
{
    int n = int.Parse(compases);
    Console.WriteLine($"Compases: {n}");
}
catch (FormatException)
{
    Console.WriteLine("No es un número");
}

Console.WriteLine("El concierto sigue");
```

#### Al superarla
—¿Ves? —dice Clave—. Se cortó una cuerda y nadie se fue a su casa.

#### Imagen
- Un escenario de teatro gótico con velas, con un violinista de espaldas que levanta un violín con una cuerda cortada, sin letras.
- Ceci, en primer plano, sigue tocando su violín; Clave la mira desde un costado y asiente.

### Micro-misión R04-N01-P2 · Lo que queda se saltea

```meta
lugar: El Escenario Grande
personajes: Ceci, Bemol
carta: Se saltea | si falla una línea del try · las de abajo NO corren · lo que va siempre, afuera del try
recompensa: xp 15, oro 15
```

#### Escena
Bemol armó la rutina de la noche: afinar, contar las cuerdas y saludar al público. Pero cuando falla el conteo, nadie saluda.

#### Gheco sugiere
Cuando una línea del `try` falla, **todo lo que queda abajo en el `try` se saltea** y se salta directo al `catch`. Lo que tiene que pasar sí o sí no puede quedar adentro del `try`: va **después** del `catch`.

```csharp
try
{
    Console.WriteLine("uno");
    int x = int.Parse("dos");   // falla acá
    Console.WriteLine("tres");  // no se muestra
}
catch (FormatException)
{
    Console.WriteLine("falló");
}
Console.WriteLine("cuatro");    // esta sí
```

#### Desafío
Sacá el `Console.WriteLine("Saludo al público");` del `try` y ponelo después del `catch`, para que se salude siempre.

#### Código inicial
```csharp
try
{
    Console.WriteLine("Afino el violín");
    int cuerdas = int.Parse("cuatro");
    Console.WriteLine($"Cuerdas: {cuerdas}");
    Console.WriteLine("Saludo al público");
}
catch (FormatException)
{
    Console.WriteLine("Esa cuerda no sirve");
}
```

#### Salida esperada
```
Afino el violín
Esa cuerda no sirve
Saludo al público
```

#### Solución
```csharp
try
{
    Console.WriteLine("Afino el violín");
    int cuerdas = int.Parse("cuatro");
    Console.WriteLine($"Cuerdas: {cuerdas}");
}
catch (FormatException)
{
    Console.WriteLine("Esa cuerda no sirve");
}
Console.WriteLine("Saludo al público");
```

#### Al superarla
Bemol hace una reverencia tan exagerada que casi se le cae el tambor.

#### Imagen
- Un escenario gótico con velas y un telón de terciopelo bordó abierto, con butacas vacías al fondo, sin letras.
- Bemol hace una reverencia exagerada con el tambor colgando; Ceci se tapa la boca para no reírse.

### Micro-misión R04-N01-P3 · ¿Qué se rompió?

```meta
lugar: El Foso de la Orquesta
personajes: Ceci, Don Cedro
carta: catch (Exception e) | atrapa cualquier error · e.GetType().Name → su nombre
recompensa: xp 15, oro 15
```

#### Escena
En el foso de la orquesta algo se rompió, pero nadie sabe qué. Don Cedro quiere saber **qué tipo de error** fue antes de arreglarlo.

#### Gheco sugiere
Un `catch (FormatException)` solo atrapa ese error. `catch (Exception e)` atrapa **cualquiera**, y lo guarda en una variable (acá, `e`) para que puedas mirarlo.

`e.GetType().Name` da el **nombre** del tipo de error:

```csharp
catch (Exception e)
{
    Console.WriteLine(e.GetType().Name);
}
```

Acá el error es pedir la posición `5` de un arreglo de `3`: eso es una `IndexOutOfRangeException`, no una `FormatException`.

#### Desafío
Cambiá el `catch` para que atrape cualquier error y muestre `Se rompió: ` seguido del nombre del error.

#### Código inicial
```csharp
int[] atriles = new int[3];
try
{
    atriles[5] = 1;
    Console.WriteLine("Atril ocupado");
}
catch (FormatException)
{
    Console.WriteLine("Se rompió algo");
}
```

#### Salida esperada
```
Se rompió: IndexOutOfRangeException
```

#### Solución
```csharp
int[] atriles = new int[3];
try
{
    atriles[5] = 1;
    Console.WriteLine("Atril ocupado");
}
catch (Exception e)
{
    Console.WriteLine($"Se rompió: {e.GetType().Name}");
}
```

#### Al superarla
—Un atril que no existe —dice Don Cedro, y se acomoda los anteojos—. Eso no se arregla con cola: se arregla contando bien.

#### Imagen
- El foso de una orquesta de teatro, iluminado con velas, con tres atriles de madera y un hueco vacío donde faltaría un cuarto, sin letras.
- Don Cedro se rasca la barba mirando el hueco; Ceci le señala los tres atriles.

### Micro-misión R04-N01-P4 · Pase lo que pase

```meta
lugar: El Escenario Grande
personajes: Ceci, Clave
carta: finally | try { … } catch { … } finally { corre SIEMPRE } · haya error o no
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Clave marca el compás con la batuta. Haya nota buena o rota, después de cada una el compás tiene que pasar.

#### Gheco sugiere
Después de los `catch` se puede agregar un `finally` («al final»). Lo que va adentro corre **siempre**: si no hubo error, si hubo y se atrapó, y hasta si hubo uno que nadie atrapó.

```csharp
try
{
    Console.WriteLine(int.Parse("8"));
}
catch (FormatException)
{
    Console.WriteLine("mal");
}
finally
{
    Console.WriteLine("listo");
}
```

#### Desafío
Agregale un `finally` que muestre `Pasa el compás`.

#### Código inicial
```csharp
string[] notas = { "4", "x", "2" };
foreach (string t in notas)
{
    try
    {
        Console.WriteLine($"Nota {int.Parse(t)}");
    }
    catch (FormatException)
    {
        Console.WriteLine("Nota rota");
    }
}
```

#### Salida esperada
```
Nota 4
Pasa el compás
Nota rota
Pasa el compás
Nota 2
Pasa el compás
```

#### Solución
```csharp
string[] notas = { "4", "x", "2" };
foreach (string t in notas)
{
    try
    {
        Console.WriteLine($"Nota {int.Parse(t)}");
    }
    catch (FormatException)
    {
        Console.WriteLine("Nota rota");
    }
    finally
    {
        Console.WriteLine("Pasa el compás");
    }
}
```

#### Al superarla
La batuta sube y baja, sube y baja. Ni una nota rota la frena.

#### Imagen
- Un escenario gótico con velas, con una batuta clara que deja una estela dorada en el aire marcando un ritmo regular, sin letras.
- Clave dirige con firmeza; Ceci toca a su lado con los ojos cerrados.

### Micro-misión R04-N01-P5 · El goblin del cero

```meta
lugar: El Foso de la Orquesta
personajes: Ceci, Gheco
criatura: goblin
carta: Goblin | un catch por cada error · FormatException: texto que no es número · DivideByZeroException: dividir por cero
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un goblin reparte 24 caramelos entre los músicos de cada fila, pero le pasaron una fila con letras y otra con cero músicos. Con la primera ya lo atrapa un `catch`; con la segunda, el programa explota.

#### Gheco sugiere
Dividir un entero por `0` lanza otro error: `DivideByZeroException`. El `catch (FormatException)` no lo atrapa, porque es de otro tipo.

Se pueden poner **varios `catch` seguidos**, uno por cada error; se prueba el primero, después el segundo:

```csharp
catch (FormatException) { … }
catch (DivideByZeroException) { … }
```

#### Desafío
Agregá un segundo `catch` para `DivideByZeroException` que muestre `No se divide por cero`.

#### Código inicial
```csharp
string[] filas = { "8", "ocho", "0" };
foreach (string f in filas)
{
    try
    {
        int musicos = int.Parse(f);
        Console.WriteLine(24 / musicos);
    }
    catch (FormatException)
    {
        Console.WriteLine($"'{f}' no es un número");
    }
}
```

#### Salida esperada
```
3
'ocho' no es un número
No se divide por cero
```

#### Solución
```csharp
string[] filas = { "8", "ocho", "0" };
foreach (string f in filas)
{
    try
    {
        int musicos = int.Parse(f);
        Console.WriteLine(24 / musicos);
    }
    catch (FormatException)
    {
        Console.WriteLine($"'{f}' no es un número");
    }
    catch (DivideByZeroException)
    {
        Console.WriteLine("No se divide por cero");
    }
}
```

#### Al superarla
El goblin se guarda los caramelos que sobraron y se va, convencido de que salió ganando.

#### Imagen
- Un goblin chico de orejas puntiagudas con una bolsa de caramelos de colores, parado frente a una fila de sillas vacías en el foso de una orquesta con velas, sin letras.
- Gheco, sobre una silla, lo mira con las antiparras puestas y los brazos cruzados.

### Encargo R04-N01-E1 · Las butacas del Teatro

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Hilván, el hermano de Ceci, cuenta las butacas que vendió cada función del Teatro de la Feria. Pero algunos anotan con letras. Escribí un programa que lea cantidades, una por línea, hasta una línea vacía. Cada una se convierte con `int.Parse` adentro de un `try`: si es un número, se suma; si no, se muestra `Inválida: ` y el texto. Al final, mostrá el total de butacas y cuántas inválidas hubo.

Con esta entrada:

```
3
dos
5

```

se muestra:

```
Inválida: dos
Butacas: 8
Inválidas: 1
```

#### Criterio de aprobación

- Usa `try` y `catch (FormatException)` con `int.Parse`.
- Deja de leer con la línea vacía y no se corta con un dato malo.

#### Entrada de ejemplo

```
3
dos
5

```

#### Salida esperada

```
Inválida: dos
Butacas: 8
Inválidas: 1
```

#### Solución de referencia

```csharp
int total = 0;
int invalidas = 0;
string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    try
    {
        total += int.Parse(linea);
    }
    catch (FormatException)
    {
        Console.WriteLine($"Inválida: {linea}");
        invalidas++;
    }
    linea = Console.ReadLine();
}
Console.WriteLine($"Butacas: {total}");
Console.WriteLine($"Inválidas: {invalidas}");
```

## R04-N02 · throw: avisar que algo anda mal

```meta
tipo: tema
padre: R04-N01
precio: 10
criatura: slime
temas: err.excepciones
usa: poo.herencia, prog.funciones
```

### Crónica

Ceci baja la escalera del sótano con un farol. El **Archivo Mudo** está lleno de cajones que nadie abre hace años, y en el fondo, algo respira. Las velas se apagan solas cuando pasa cerca.

—Hasta ahora atrapaste errores que lanzaba C# —dice {mentor}, que bajó detrás de ella—. Ahora vas a lanzar los tuyos. Cuando un método recibe algo que no tiene sentido, no tiene que hacer como si nada: tiene que **avisar**, fuerte, para que alguien arriba decida.

### Objetivos

- Lanzar un error con `throw`.
- Entender que un error sin atrapar **sube** al método que llamó.
- Crear tu propia excepción heredando de `Exception`.
- Atrapar solo cuando se cumple algo, con `when`.
- Ordenar los `catch` del más específico al más general.

### Antes de empezar

- `try` y `catch` (R04-N01), métodos (Acto I) y herencia (Acto II).

### Explicación

#### Lanzar: `throw`

```csharp
static void Afinar(int tension)
{
    if (tension < 0)
    {
        throw new ArgumentException("la tensión no puede ser negativa");
    }
    Console.WriteLine("Afinado");
}
```

`throw` («lanzá») corta el método en ese mismo momento y lanza el error. El texto que le pasás queda en `e.Message`, para quien lo atrape:

```csharp
catch (ArgumentException e)
{
    Console.WriteLine(e.Message);   // la tensión no puede ser negativa
}
```

Las que más vas a lanzar: `ArgumentException` (te pasaron un dato que no sirve) e `InvalidOperationException` (ahora no se puede hacer eso).

#### El error sube

Si el método donde ocurre el error no lo atrapa, **sube** al que lo llamó; si ese tampoco, sube otra vez, hasta arriba de todo. Si nadie lo atrapa, el programa se corta. Por eso el `try` se pone donde se sabe **qué hacer** con el error.

#### Tu propia excepción

Una excepción es una clase. Para crear la tuya, heredás de `Exception` y le pasás el mensaje a `base`:

```csharp
class CuerdaRotaException : Exception
{
    public int Cuerda { get; }

    public CuerdaRotaException(int cuerda) : base($"se cortó la cuerda {cuerda}")
    {
        Cuerda = cuerda;
    }
}
```

Por costumbre, el nombre termina en `Exception`. Puede guardar datos (acá, `Cuerda`) para quien la atrape.

#### `when`: solo si…

```csharp
catch (CuerdaRotaException e) when (e.Cuerda == 1)
{
    Console.WriteLine("Hay repuesto");
}
catch (CuerdaRotaException e)
{
    Console.WriteLine("Hay que ir al taller");
}
```

El primero atrapa solo si la condición del `when` da `true`; si no, se prueba el siguiente.

#### El orden de los `catch`

Se prueban de arriba para abajo. `Exception` atrapa todo, así que va **último**: si va primero, los de abajo nunca llegarían, y el compilador no te deja (`CS0160`).

### Código de ejemplo

```csharp
try
{
    Afinar(-3);
}
catch (ArgumentException e)
{
    Console.WriteLine($"No se pudo: {e.Message}");
}

try
{
    throw new CuerdaRotaException(2);
}
catch (CuerdaRotaException e) when (e.Cuerda == 1)
{
    Console.WriteLine("Se cortó la primera: hay repuesto");
}
catch (CuerdaRotaException e)
{
    Console.WriteLine($"Se cortó la cuerda {e.Cuerda}");
}

static void Afinar(int tension)
{
    if (tension < 0)
    {
        throw new ArgumentException("la tensión no puede ser negativa");
    }
    Console.WriteLine("Afinado");
}

class CuerdaRotaException : Exception
{
    public int Cuerda { get; }

    public CuerdaRotaException(int cuerda) : base($"se cortó la cuerda {cuerda}")
    {
        Cuerda = cuerda;
    }
}
```

### Salida esperada

```
No se pudo: la tensión no puede ser negativa
Se cortó la cuerda 2
```

### ¿Para qué sirve?

Para que tus métodos no sigan trabajando con datos imposibles. Un banco no transfiere un monto negativo: lanza un error, y la pantalla de arriba le avisa al usuario.

### Errores habituales

- **Devolver un valor raro en vez de lanzar:** un método que devuelve `-1` cuando algo falla obliga a todos a acordarse de revisar. Un error lanzado no se puede ignorar sin querer.
- **El `catch (Exception)` primero:** los de abajo no llegarían nunca (`CS0160`). Del más específico al más general.
- **Usar excepciones para lo normal:** si es esperable que el usuario escriba cualquier cosa, alcanza con un `if` o con `int.TryParse`. Las excepciones son para lo que **no debería pasar**.

### Micro-misión R04-N02-P1 · Un violín sin cuerdas

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: throw | throw new ArgumentException("mensaje"); · corta el método · e.Message → el mensaje
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Don Cedro calcula el precio de un violín por sus cuerdas. Un cliente pidió uno de **cero** cuerdas, y el método contestó `0` como si nada.

#### Gheco sugiere
Un método puede **lanzar** su propio error con `throw`. Corta el método en ese momento:

```csharp
if (edad < 0)
{
    throw new ArgumentException("la edad no puede ser negativa");
}
```

`ArgumentException` es el error de «me pasaron un dato que no sirve». El texto entre comillas es el **mensaje**: quien lo atrape lo lee con `e.Message`. Acá el `catch` ya está escrito.

#### Desafío
En `Precio`, si `cuerdas` es `0` o menos, lanzá una `ArgumentException` con el mensaje `un violín necesita cuerdas`.

#### Código inicial
```csharp
try
{
    Console.WriteLine(Precio(4));
    Console.WriteLine(Precio(0));
}
catch (ArgumentException e)
{
    Console.WriteLine($"Error: {e.Message}");
}

static int Precio(int cuerdas)
{
    return cuerdas * 50;
}
```

#### Salida esperada
```
200
Error: un violín necesita cuerdas
```

#### Solución
```csharp
try
{
    Console.WriteLine(Precio(4));
    Console.WriteLine(Precio(0));
}
catch (ArgumentException e)
{
    Console.WriteLine($"Error: {e.Message}");
}

static int Precio(int cuerdas)
{
    if (cuerdas <= 0)
    {
        throw new ArgumentException("un violín necesita cuerdas");
    }
    return cuerdas * 50;
}
```

#### Al superarla
—Eso —dice Don Cedro—. Si el pedido no tiene sentido, se dice. No se cobra cero y se manda una caja vacía.

#### Imagen
- Un taller de luthier de madera con un violín sin cuerdas sobre la mesa de trabajo y un rollo de cuerdas al lado, con velas, sin letras.
- Don Cedro levanta el violín vacío con cara de «¿y esto?»; Ceci se ríe.

### Micro-misión R04-N02-P2 · Sube hasta quien sabe

```meta
lugar: El Archivo Mudo
personajes: Ceci, Clave
carta: El error sube | si nadie lo atrapa en el método · sube al que lo llamó · el try va donde se sabe qué hacer
recompensa: xp 15, oro 15
```

#### Escena
`Obra` lanza un error porque falta el pentagrama. `Concierto` no lo atrapa. Nadie lo atrapa, y la noche termina de golpe.

#### Gheco sugiere
Si un método lanza un error y **no lo atrapa**, el error **sube** al que lo llamó, y se corta también ahí. Si ese tampoco lo atrapa, sigue subiendo. Así, un solo `try` arriba de todo puede atrapar lo que pase en cualquier método de abajo.

`InvalidOperationException` es el error de «ahora no se puede hacer eso».

#### Desafío
En el programa principal, envolvé `Concierto();` en un `try`, con un `catch (InvalidOperationException e)` que muestre `Arriba: ` y el mensaje. Fijate que `Concierto: cierra` no se muestra: el error cortó también a `Concierto`.

#### Código inicial
```csharp
Console.WriteLine("Empieza");
Concierto();
Console.WriteLine("Fin de la noche");

static void Concierto()
{
    Console.WriteLine("Concierto: abre");
    Obra();
    Console.WriteLine("Concierto: cierra");
}

static void Obra()
{
    throw new InvalidOperationException("falta el pentagrama");
}
```

#### Salida esperada
```
Empieza
Concierto: abre
Arriba: falta el pentagrama
Fin de la noche
```

#### Solución
```csharp
Console.WriteLine("Empieza");
try
{
    Concierto();
}
catch (InvalidOperationException e)
{
    Console.WriteLine($"Arriba: {e.Message}");
}
Console.WriteLine("Fin de la noche");

static void Concierto()
{
    Console.WriteLine("Concierto: abre");
    Obra();
    Console.WriteLine("Concierto: cierra");
}

static void Obra()
{
    throw new InvalidOperationException("falta el pentagrama");
}
```

#### Al superarla
—El error subió dos escalones hasta encontrar a alguien que supiera qué hacer —dice Clave—. Esa persona sos vos.

#### Imagen
- Una escalera de piedra que baja a un sótano oscuro con cajones polvorientos, con una lucecita roja que sube por los escalones, de noche, sin letras.
- Clave, arriba de la escalera, atrapa la lucecita en la mano; Ceci la mira desde abajo con un farol.

### Micro-misión R04-N02-P3 · Tu propia maldición

```meta
lugar: El Archivo Mudo
personajes: Ceci, Bemol
carta: Excepción propia | class XException : Exception · el constructor llama a : base("mensaje") · puede guardar datos
recompensa: xp 15, oro 15
```

#### Escena
Bemol quiere un error que diga exactamente qué pasó: qué cuerda está desafinada y por cuánto. Ninguno de los de C# dice eso.

#### Gheco sugiere
Una excepción es una **clase**. La tuya hereda de `Exception` (con `:`, como en el Acto II) y le pasa el mensaje al constructor de arriba con `: base(…)`:

```csharp
class Tarde : Exception
{
    public Tarde(string nombre) : base($"{nombre} llegó tarde")
    {
    }
}
```

Lo que le pasás a `base` es lo que después se lee en `e.Message`. Por costumbre, el nombre termina en `Exception`.

#### Desafío
Completá la clase `DesafinadaException`: que herede de `Exception` y que su constructor le pase a `base` el mensaje `La cuerda X está desafinada`, con el nombre de la cuerda en lugar de `X`.

#### Código inicial
```csharp
try
{
    Afinar("la", 3);
}
catch (DesafinadaException e)
{
    Console.WriteLine($"{e.Message} (por {e.Diferencia})");
}

static void Afinar(string cuerda, int diferencia)
{
    if (diferencia != 0)
    {
        throw new DesafinadaException(cuerda, diferencia);
    }
    Console.WriteLine($"{cuerda} afinada");
}

class DesafinadaException
{
    public int Diferencia { get; }

    public DesafinadaException(string cuerda, int diferencia)
    {
        Diferencia = diferencia;
    }
}
```

#### Salida esperada
```
La cuerda la está desafinada (por 3)
```

#### Solución
```csharp
try
{
    Afinar("la", 3);
}
catch (DesafinadaException e)
{
    Console.WriteLine($"{e.Message} (por {e.Diferencia})");
}

static void Afinar(string cuerda, int diferencia)
{
    if (diferencia != 0)
    {
        throw new DesafinadaException(cuerda, diferencia);
    }
    Console.WriteLine($"{cuerda} afinada");
}

class DesafinadaException : Exception
{
    public int Diferencia { get; }

    public DesafinadaException(string cuerda, int diferencia) : base($"La cuerda {cuerda} está desafinada")
    {
        Diferencia = diferencia;
    }
}
```

#### Al superarla
—Ahora el error habla —dice Bemol—. Dice qué cuerda y cuánto. Eso es casi un afinador.

#### Imagen
- Un sótano de piedra con cajones polvorientos y un violín sobre un cajón, con una cuerda que vibra brillando en rojo suave, con faroles azules, sin letras.
- Bemol apoya la oreja cerca del violín; Ceci gira una clavija con cuidado.

### Micro-misión R04-N02-P4 · Solo si falta poco

```meta
lugar: El Archivo Mudo
personajes: Ceci, Don Cedro
carta: when | catch (X e) when (condición) { … } · atrapa solo si la condición da true · si no, prueba el siguiente
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Don Cedro dice que si una cuerda está desafinada por poco, se arregla con la clavija; si está muy desafinada, hay que cambiarla. El programa hoy dice «cambiar» para todas.

#### Gheco sugiere
Después del `catch` se puede poner un `when` («cuando») con una condición. Ese `catch` atrapa **solo si la condición da `true`**; si no, el error sigue al `catch` de abajo:

```csharp
catch (DesafinadaException e) when (e.Diferencia > 10)
{
    Console.WriteLine("muy desafinada");
}
catch (DesafinadaException e)
{
    Console.WriteLine("un poco desafinada");
}
```

#### Desafío
Agregá, **antes** del `catch` que ya está, otro `catch (DesafinadaException e) when (e.Diferencia <= 2)` que muestre `Se arregla con la clavija`.

#### Código inicial
```csharp
int[] diferencias = { 1, 5 };
foreach (int d in diferencias)
{
    try
    {
        throw new DesafinadaException("mi", d);
    }
    catch (DesafinadaException)
    {
        Console.WriteLine("Hay que cambiar la cuerda");
    }
}

class DesafinadaException : Exception
{
    public int Diferencia { get; }

    public DesafinadaException(string cuerda, int diferencia) : base($"La cuerda {cuerda} está desafinada")
    {
        Diferencia = diferencia;
    }
}
```

#### Salida esperada
```
Se arregla con la clavija
Hay que cambiar la cuerda
```

#### Solución
```csharp
int[] diferencias = { 1, 5 };
foreach (int d in diferencias)
{
    try
    {
        throw new DesafinadaException("mi", d);
    }
    catch (DesafinadaException e) when (e.Diferencia <= 2)
    {
        Console.WriteLine("Se arregla con la clavija");
    }
    catch (DesafinadaException)
    {
        Console.WriteLine("Hay que cambiar la cuerda");
    }
}

class DesafinadaException : Exception
{
    public int Diferencia { get; }

    public DesafinadaException(string cuerda, int diferencia) : base($"La cuerda {cuerda} está desafinada")
    {
        Diferencia = diferencia;
    }
}
```

#### Al superarla
Don Cedro gira la clavija un cuarto de vuelta. La primera cuerda suena perfecta. La segunda, la tira al canasto sin dudar.

#### Imagen
- Una mesa de luthier en un sótano de piedra con faroles azules, con un violín, una clavija de madera y una cuerda nueva enrollada al lado, sin letras.
- Don Cedro gira una clavija con dos dedos; Ceci sostiene la cuerda nueva, lista.

### Micro-misión R04-N02-P5 · El slime de los catch

```meta
lugar: El Archivo Mudo
personajes: Ceci, Gheco
criatura: slime
carta: Slime | CS0160 · catch (Exception) atrapa todo · va ÚLTIMO · del más específico al más general
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un slime acomodó los `catch` al revés, y la partitura ni siquiera pasa el ensayo: el compilador la rechaza.

#### Gheco sugiere
Los `catch` se prueban **de arriba para abajo**. `catch (Exception)` atrapa todo, así que si va primero, el de `FormatException` nunca llegaría. El compilador lo ve y no te deja:

```
error CS0160: Una cláusula catch previa ya detecta todas las excepciones de este tipo o de tipo superior
```

La regla: del más específico (el que atrapa un error concreto) al más general.

#### Desafío
Ensayá, mirá el error y dalos vuelta: primero el `catch (FormatException)`, después el `catch (Exception)`.

#### Código inicial
```csharp
string[] datos = { "7", "siete" };
foreach (string d in datos)
{
    try
    {
        Console.WriteLine(int.Parse(d) * 2);
    }
    catch (Exception)
    {
        Console.WriteLine("Algo falló");
    }
    catch (FormatException)
    {
        Console.WriteLine($"'{d}' no es un número");
    }
}
```

#### Salida esperada
```
14
'siete' no es un número
```

#### Solución
```csharp
string[] datos = { "7", "siete" };
foreach (string d in datos)
{
    try
    {
        Console.WriteLine(int.Parse(d) * 2);
    }
    catch (FormatException)
    {
        Console.WriteLine($"'{d}' no es un número");
    }
    catch (Exception)
    {
        Console.WriteLine("Algo falló");
    }
}
```

#### Al superarla
El slime se da vuelta a sí mismo, como un guante, y se va rodando escaleras arriba.

#### Imagen
- Un slime verde gelatinoso de caricatura dándose vuelta como un guante sobre el piso de piedra de un sótano con cajones y faroles azules, sin letras.
- Gheco, sobre un cajón, lo mira con las antiparras puestas, divertido.

### Encargo R04-N02-E1 · La caja fuerte de Elefa

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Elefa guarda las monedas del Puerto en una caja fuerte. Escribí un método `Depositar(int monto)` que, si el monto es `0` o menos, lance una `ArgumentException` con el mensaje `monto inválido: ` y el monto. El programa lee montos, uno por línea, hasta una línea vacía: por cada uno intenta depositar y muestra `Depositado ` y el monto, o `Error: ` y el mensaje. Al final, el saldo.

Con esta entrada:

```
100
-5
40

```

se muestra:

```
Depositado 100
Error: monto inválido: -5
Depositado 40
Saldo: 140
```

#### Criterio de aprobación

- `Depositar` lanza una `ArgumentException` con `throw`.
- El programa atrapa el error y sigue con el siguiente monto.

#### Entrada de ejemplo

```
100
-5
40

```

#### Salida esperada

```
Depositado 100
Error: monto inválido: -5
Depositado 40
Saldo: 140
```

#### Solución de referencia

```csharp
int saldo = 0;
string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    int monto = int.Parse(linea);
    try
    {
        saldo += Depositar(monto);
        Console.WriteLine($"Depositado {monto}");
    }
    catch (ArgumentException e)
    {
        Console.WriteLine($"Error: {e.Message}");
    }
    linea = Console.ReadLine();
}
Console.WriteLine($"Saldo: {saldo}");

static int Depositar(int monto)
{
    if (monto <= 0)
    {
        throw new ArgumentException($"monto inválido: {monto}");
    }
    return monto;
}
```

## R04-N03 · Archivos de texto: que el Archivo recuerde

```meta
tipo: tema
padre: R04-N02
precio: 10
criatura: orco
temas: arch.texto
usa: err.excepciones, prog.cadenas
```

### Crónica

En el fondo del Archivo Mudo, entre cajones vacíos, Ceci lo ve por fin: el **Liche del Archivo Mudo**, alto y flaco, con una túnica hecha de páginas en blanco y un apagavelas en la mano. Cada vela que apaga se lleva lo que alguien ensayó ese día.

—Todo lo que guardás en una variable desaparece cuando el programa termina —dice {mentor}—. Es como una vela que se apaga. El Liche vive de eso. Para vencerlo, lo importante hay que **escribirlo**: en un archivo, lo que se escribe queda.

### Objetivos

- Escribir un archivo de texto con `File.WriteAllText` y agregarle líneas con `File.AppendAllText`.
- Leerlo entero con `File.ReadAllText` o línea por línea con `File.ReadAllLines`.
- Preguntar si existe con `File.Exists` y borrarlo con `File.Delete`.

### Antes de empezar

- Textos y arreglos (Acto I), y `try`/`catch` (R04-N01).

### Explicación

#### Una carpeta de mentira

Acá, en el navegador, tus programas tienen una **carpeta propia que empieza vacía cada vez que ejecutás**: lo que escribís dura hasta que termina el programa. En tu compu, con .NET instalado, el archivo queda guardado en la carpeta donde ejecutás, y lo podés abrir con el Bloc de notas (Windows) o con cualquier editor de texto (Linux).

#### Todo de una vez: `File`

| Método | Qué hace |
|---|---|
| `File.WriteAllText(ruta, texto)` | crea el archivo, o lo **reemplaza** si ya existía |
| `File.AppendAllText(ruta, texto)` | agrega el texto **al final** |
| `File.ReadAllText(ruta)` | devuelve todo el contenido en un `string` |
| `File.WriteAllLines(ruta, lineas)` | escribe un arreglo, una línea por elemento |
| `File.ReadAllLines(ruta)` | devuelve un arreglo con las líneas |
| `File.Exists(ruta)` | `true` si existe |
| `File.Delete(ruta)` | lo borra |

La **ruta** es el nombre del archivo, por ejemplo `"diario.txt"`. `\n` dentro de un texto es un **salto de línea**: lo que hace `WriteLine` al final.

### Código de ejemplo

```csharp
File.WriteAllText("diario.txt", "Primer ensayo\n");
File.AppendAllText("diario.txt", "Segundo ensayo\n");
Console.Write(File.ReadAllText("diario.txt"));

string[] lineas = File.ReadAllLines("diario.txt");
Console.WriteLine(lineas.Length);
Console.WriteLine(File.Exists("diario.txt"));
Console.WriteLine(File.Exists("otro.txt"));
```

### Salida esperada

```
Primer ensayo
Segundo ensayo
2
True
False
```

### ¿Para qué sirve?

Para que tus programas **recuerden**: un récord, la configuración, la lista de tareas, un registro de lo que pasó. Sin archivos (o una base de datos), cada vez que se cierra el programa empieza de cero.

### Errores habituales

- **`WriteAllText` para agregar:** reemplaza todo lo que había. Para sumar al final, `AppendAllText`.
- **Leer un archivo que no existe:** `FileNotFoundException`. Preguntá antes con `File.Exists`.
- **Olvidar el `\n`:** con `AppendAllText`, si no ponés el salto de línea, todo queda pegado en la misma línea.

### Micro-misión R04-N03-P1 · La primera página

```meta
lugar: El Archivo Mudo
personajes: Ceci, Clave
carta: Escribir y leer | File.WriteAllText("a.txt", "texto"); · File.ReadAllText("a.txt") → el texto
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Clave le da a Ceci un cuaderno en blanco. Lo primero que hay que anotar es que llegó al Archivo, antes de que el Liche apague la vela.

#### Gheco sugiere
`File` es la herramienta de C# para trabajar con archivos. `File.WriteAllText` crea un archivo con un nombre y le escribe un texto. `File.ReadAllText` lo lee entero y te lo devuelve como `string`:

```csharp
File.WriteAllText("saludo.txt", "Hola");
string leido = File.ReadAllText("saludo.txt");
Console.WriteLine(leido);   // Hola
```

Acá, en el navegador, la carpeta empieza vacía cada vez que ejecutás; en tu compu, el archivo queda guardado.

#### Desafío
Antes de la línea que lee, escribí en `memoria.txt` el texto `Ceci llegó al Archivo`.

#### Código inicial
```csharp
// escribí el archivo acá

Console.WriteLine(File.ReadAllText("memoria.txt"));
```

#### Salida esperada
```
Ceci llegó al Archivo
```

#### Solución
```csharp
File.WriteAllText("memoria.txt", "Ceci llegó al Archivo");

Console.WriteLine(File.ReadAllText("memoria.txt"));
```

#### Al superarla
La vela tiembla, pero no se apaga. Lo escrito, escrito está.

#### Imagen
- Un sótano de piedra con cajones polvorientos y faroles azules, con un cuaderno abierto de páginas lisas sobre un cajón y una vela encendida al lado, sin letras.
- Ceci escribe en el cuaderno con una pluma; Clave le sostiene el farol.

### Micro-misión R04-N03-P2 · Una línea más

```meta
lugar: El Archivo Mudo
personajes: Ceci, Bemol
carta: Agregar | WriteAllText REEMPLAZA · AppendAllText AGREGA al final · \n = salto de línea
recompensa: xp 15, oro 15
```

#### Escena
Bemol anota los ensayos de la semana, pero cada vez que escribe uno, desaparece el anterior. El Liche se ríe en la oscuridad.

#### Gheco sugiere
`WriteAllText` **reemplaza** todo lo que había en el archivo. Para **agregar** al final sin borrar, se usa `File.AppendAllText`:

```csharp
File.WriteAllText("a.txt", "uno\n");
File.AppendAllText("a.txt", "dos\n");   // queda: uno, dos
```

`\n` es un salto de línea: sin él, todo quedaría pegado.

#### Desafío
Cambiá el segundo `WriteAllText` por `AppendAllText`.

#### Código inicial
```csharp
File.WriteAllText("ensayos.txt", "Lunes: escalas\n");
File.WriteAllText("ensayos.txt", "Martes: arpegios\n");
Console.Write(File.ReadAllText("ensayos.txt"));
```

#### Salida esperada
```
Lunes: escalas
Martes: arpegios
```

#### Solución
```csharp
File.WriteAllText("ensayos.txt", "Lunes: escalas\n");
File.AppendAllText("ensayos.txt", "Martes: arpegios\n");
Console.Write(File.ReadAllText("ensayos.txt"));
```

#### Al superarla
—Ahora el lunes se queda —dice Bemol, y le saca la lengua a la oscuridad.

#### Imagen
- Un cuaderno abierto de páginas lisas sobre un cajón de piedra, con dos marcadores de cinta de colores entre las hojas, en un sótano con faroles azules, sin letras.
- Bemol señala orgulloso el cuaderno; Ceci aplaude bajito.

### Micro-misión R04-N03-P3 · Línea por línea

```meta
lugar: El Archivo Mudo
personajes: Ceci, Clave
carta: Líneas | File.WriteAllLines("a.txt", arreglo); · File.ReadAllLines("a.txt") → string[] · una línea por elemento
recompensa: xp 15, oro 15
```

#### Escena
En un cajón hay una lista de obras guardada. Clave quiere verlas numeradas, una por línea.

#### Gheco sugiere
`File.WriteAllLines` escribe un arreglo de textos, **uno por línea**. `File.ReadAllLines` hace lo contrario: lee el archivo y te da un `string[]` con una línea en cada posición.

```csharp
string[] lineas = File.ReadAllLines("lista.txt");
for (int i = 0; i < lineas.Length; i++)
{
    Console.WriteLine($"{i + 1}. {lineas[i]}");
}
```

`new[] { "a", "b" }` crea un arreglo ahí mismo, sin nombre: C# se da cuenta solo de que es de `string`.

#### Desafío
Leé `obras.txt` con `File.ReadAllLines` y mostrá cada obra numerada desde `1`, como `1. Canon`.

#### Código inicial
```csharp
File.WriteAllLines("obras.txt", new[] { "Canon", "Bolero", "Tango" });

// leé y mostrá numeradas

```

#### Salida esperada
```
1. Canon
2. Bolero
3. Tango
```

#### Solución
```csharp
File.WriteAllLines("obras.txt", new[] { "Canon", "Bolero", "Tango" });

string[] obras = File.ReadAllLines("obras.txt");
for (int i = 0; i < obras.Length; i++)
{
    Console.WriteLine($"{i + 1}. {obras[i]}");
}
```

#### Al superarla
—Tres obras, tres líneas —dice Clave—. Un archivo es eso: un cajón con renglones.

#### Imagen
- Tres partituras enrolladas atadas con cintas, saliendo de un cajón de madera abierto en un sótano de piedra con faroles azules, sin letras.
- Clave saca una partitura del cajón; Ceci las cuenta con los dedos.

### Micro-misión R04-N03-P4 · Borrar la página

```meta
lugar: El Archivo Mudo
personajes: Ceci, Don Cedro
carta: Existe y borrar | File.Exists("a.txt") → true o false · File.Delete("a.txt"); lo borra
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Don Cedro escribió un borrador del presupuesto que ya no sirve. Quiere borrarlo y comprobar que de verdad desapareció.

#### Gheco sugiere
`File.Exists("a.txt")` pregunta si el archivo está: devuelve `true` o `false`. `File.Delete("a.txt")` lo borra:

```csharp
File.WriteAllText("a.txt", "x");
Console.WriteLine(File.Exists("a.txt"));   // True
File.Delete("a.txt");
Console.WriteLine(File.Exists("a.txt"));   // False
```

#### Desafío
Entre las dos preguntas, borrá `borrador.txt`.

#### Código inicial
```csharp
File.WriteAllText("borrador.txt", "Presupuesto viejo");
Console.WriteLine($"¿Existe? {File.Exists("borrador.txt")}");

// borralo

Console.WriteLine($"¿Existe? {File.Exists("borrador.txt")}");
```

#### Salida esperada
```
¿Existe? True
¿Existe? False
```

#### Solución
```csharp
File.WriteAllText("borrador.txt", "Presupuesto viejo");
Console.WriteLine($"¿Existe? {File.Exists("borrador.txt")}");

File.Delete("borrador.txt");

Console.WriteLine($"¿Existe? {File.Exists("borrador.txt")}");
```

#### Al superarla
Don Cedro arruga una hoja imaginaria y la tira por arriba del hombro. —Al canasto.

#### Imagen
- Un canasto de mimbre con una hoja arrugada adentro, al lado de una mesa de luthier en un sótano de piedra con faroles azules, sin letras.
- Don Cedro tira una hoja arrugada por arriba del hombro; Ceci la ve caer adentro del canasto.

### Micro-misión R04-N03-P5 · El orco del archivo que no existe

```meta
lugar: El Archivo Mudo
personajes: Ceci, Gheco
criatura: orco
carta: Orco | FileNotFoundException · leer un archivo que no está · preguntá antes con File.Exists
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un orco quiere leer `partitura.txt` del cajón, pero el Liche ya la borró. El programa explota en la puerta.

#### Gheco sugiere
Leer un archivo que no existe lanza una `FileNotFoundException`. Antes de leer, preguntá con `File.Exists`:

```csharp
if (File.Exists("a.txt"))
{
    Console.WriteLine(File.ReadAllText("a.txt"));
}
else
{
    Console.WriteLine("no está");
}
```

#### Desafío
Si `partitura.txt` existe, mostrá su contenido; si no, mostrá `No hay partitura guardada`.

#### Código inicial
```csharp
string texto = File.ReadAllText("partitura.txt");
Console.WriteLine(texto);
```

#### Salida esperada
```
No hay partitura guardada
```

#### Solución
```csharp
if (File.Exists("partitura.txt"))
{
    string texto = File.ReadAllText("partitura.txt");
    Console.WriteLine(texto);
}
else
{
    Console.WriteLine("No hay partitura guardada");
}
```

#### Al superarla
El orco abre el cajón, lo encuentra vacío y, por primera vez, no rompe nada: lo cierra despacio y se va.

#### Imagen
- Un orco grandote de caricatura abriendo un cajón vacío de madera en un sótano de piedra con faroles azules, con cara de sorpresa.
- Gheco, sobre el cajón de al lado, le muestra un farol para que vea que no hay nada.

### Encargo R04-N03-E1 · El cuaderno de Tizón

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Tizón, el herrero de las Forjas, anota los metales que funde. Escribí un programa que lea metales, uno por línea, hasta una línea vacía, y que agregue cada uno a `forja.txt` con `File.AppendAllText`, numerado (`1: hierro`). Al final, leé el archivo con `File.ReadAllLines`, mostrá cada línea y la cantidad de líneas.

Con esta entrada:

```
hierro
cobre

```

se muestra:

```
1: hierro
2: cobre
Líneas: 2
```

#### Criterio de aprobación

- Escribe con `File.AppendAllText` y lee con `File.ReadAllLines`.
- La cantidad sale del archivo, no de un contador.

#### Entrada de ejemplo

```
hierro
cobre

```

#### Salida esperada

```
1: hierro
2: cobre
Líneas: 2
```

#### Solución de referencia

```csharp
int n = 0;
string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    n++;
    File.AppendAllText("forja.txt", $"{n}: {linea}\n");
    linea = Console.ReadLine();
}

string[] lineas = File.ReadAllLines("forja.txt");
foreach (string l in lineas)
{
    Console.WriteLine(l);
}
Console.WriteLine($"Líneas: {lineas.Length}");
```

## R04-N04 · using: abrir, escribir y cerrar

```meta
tipo: tema
padre: R04-N03
precio: 10
criatura: troll
temas: arch.texto
usa: err.excepciones, prog.bucles
```

### Crónica

El Liche tiene un truco: cuando alguien deja un cajón abierto, se mete adentro y se come lo que estaba escrito a medias. Don Cedro baja al sótano con una caja de herramientas y una regla de oro de luthier: *«Lo que se abre, se cierra»*.

—`File.WriteAllText` abre, escribe y cierra solo —dice {mentor}—. Pero cuando hay que escribir muchas líneas, una por una, conviene abrir el archivo **una vez**, escribir todo y cerrarlo. Y no olvidarse nunca de cerrarlo.

### Objetivos

- Escribir línea por línea con un `StreamWriter`.
- Leer línea por línea con un `StreamReader` hasta que no haya más.
- Cerrar los archivos sin olvidarse, con `using`.

### Antes de empezar

- Archivos de texto (R04-N03) y el bucle `while` (Acto I).

### Explicación

#### Un escritor y un lector

```csharp
StreamWriter escritor = new StreamWriter("a.txt");   // abre para escribir
escritor.WriteLine("hola");                          // como Console.WriteLine, pero al archivo
```

Un `StreamWriter` deja el archivo **abierto** hasta que se cierra. Si no se cierra, parte de lo escrito puede no llegar al archivo, y otro programa no lo puede abrir.

#### `using` lo cierra solo

```csharp
using (StreamWriter escritor = new StreamWriter("a.txt"))
{
    escritor.WriteLine("hola");
    escritor.WriteLine("chau");
}   // acá se cierra, aunque haya un error adentro
```

`using` («usando») crea el objeto, lo deja usar adentro de las llaves y lo **cierra solo** al salir. También hay una forma corta, que lo cierra al terminar el método donde está:

```csharp
using var escritor = new StreamWriter("a.txt");
```

#### Leer hasta el final

```csharp
using (StreamReader lector = new StreamReader("a.txt"))
{
    string? linea = lector.ReadLine();
    while (linea != null)
    {
        Console.WriteLine(linea);
        linea = lector.ReadLine();
    }
}
```

`ReadLine()` devuelve la línea siguiente, o `null` cuando **ya no quedan**. Es igual que `Console.ReadLine()`, pero leyendo del archivo.

### Código de ejemplo

```csharp
using (StreamWriter escritor = new StreamWriter("compases.txt"))
{
    for (int i = 1; i <= 3; i++)
    {
        escritor.WriteLine($"compás {i}");
    }
}

using (StreamReader lector = new StreamReader("compases.txt"))
{
    string? linea = lector.ReadLine();
    while (linea != null)
    {
        Console.WriteLine(linea);
        linea = lector.ReadLine();
    }
}
```

### Salida esperada

```
compás 1
compás 2
compás 3
```

### ¿Para qué sirve?

Para archivos grandes o que se escriben de a poco: un registro (*log*) que crece durante todo el programa, un archivo de millones de líneas que no entra entero en la memoria. Y `using` sirve para todo lo que se abre y se cierra: archivos, conexiones a una base de datos, a la red.

### Errores habituales

- **No cerrar:** sin `using`, lo escrito puede quedar a medias. El **troll** del archivo abierto se queda con las últimas líneas.
- **Seguir leyendo después del final:** `ReadLine()` devuelve `null`, y usarlo explota (`NullReferenceException`).
- **Abrir con `new StreamWriter` un archivo que ya existe:** lo reemplaza, como `WriteAllText`.

### Micro-misión R04-N04-P1 · El cuaderno abierto

```meta
lugar: El Archivo Mudo
personajes: Ceci, Don Cedro
carta: StreamWriter | using (StreamWriter e = new StreamWriter("a.txt")) { e.WriteLine("x"); } · al salir, se cierra solo
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Don Cedro abre el cuaderno de la escala. —Se abre, se escribe y se cierra —dice—. En ese orden, siempre.

#### Gheco sugiere
Un `StreamWriter` es un **escritor de archivos**: lo creás con el nombre del archivo y le escribís con `WriteLine`, igual que a la consola.

El `using (…) { }` lo crea, te deja usarlo adentro de las llaves y lo **cierra solo** al salir:

```csharp
using (StreamWriter escritor = new StreamWriter("a.txt"))
{
    escritor.WriteLine("primera");
}
```

#### Desafío
Adentro del `using`, escribí `do` y `re`, una por línea.

#### Código inicial
```csharp
using (StreamWriter escritor = new StreamWriter("escala.txt"))
{
    // escribí las dos notas

}

Console.Write(File.ReadAllText("escala.txt"));
```

#### Salida esperada
```
do
re
```

#### Solución
```csharp
using (StreamWriter escritor = new StreamWriter("escala.txt"))
{
    escritor.WriteLine("do");
    escritor.WriteLine("re");
}

Console.Write(File.ReadAllText("escala.txt"));
```

#### Al superarla
Don Cedro cierra el cuaderno con las dos manos, despacio, como quien cierra un estuche.

#### Imagen
- Un cuaderno de tapas de cuero que se cierra solo con una hebilla de bronce, sobre un cajón en un sótano de piedra con faroles azules, sin letras.
- Don Cedro aprieta la hebilla; Ceci sostiene la pluma con la que acaba de escribir.

### Micro-misión R04-N04-P2 · Muchas líneas sin reabrir

```meta
lugar: El Archivo Mudo
personajes: Ceci, Bemol
carta: Escribir en un bucle | el using afuera · el for adentro · se abre UNA vez, se escriben todas
recompensa: xp 15, oro 15
```

#### Escena
Bemol quiere guardar toda la escala, nota por nota, numerada. Abrir y cerrar el cuaderno siete veces le da sueño.

#### Gheco sugiere
El archivo se abre **una vez**, con el `using` afuera, y el bucle va **adentro**: cada vuelta escribe una línea más, sin volver a abrir.

```csharp
using (StreamWriter escritor = new StreamWriter("a.txt"))
{
    foreach (string x in lista)
    {
        escritor.WriteLine(x);
    }
}
```

#### Desafío
Adentro del `using`, recorré `notas` y escribí cada una con su número, desde `1`: `1 do`, `2 re`…

#### Código inicial
```csharp
string[] notas = { "do", "re", "mi", "fa" };

using (StreamWriter escritor = new StreamWriter("notas.txt"))
{
    // un for que escriba cada nota numerada

}

Console.Write(File.ReadAllText("notas.txt"));
```

#### Salida esperada
```
1 do
2 re
3 mi
4 fa
```

#### Solución
```csharp
string[] notas = { "do", "re", "mi", "fa" };

using (StreamWriter escritor = new StreamWriter("notas.txt"))
{
    for (int i = 0; i < notas.Length; i++)
    {
        escritor.WriteLine($"{i + 1} {notas[i]}");
    }
}

Console.Write(File.ReadAllText("notas.txt"));
```

#### Al superarla
—Una vez abierto, una vez cerrado —dice Bemol, y bosteza—. Igual me dio sueño.

#### Imagen
- Una escalera de notas musicales doradas que sube flotando desde un cuaderno abierto de páginas lisas, en un sótano de piedra con faroles azules, sin letras.
- Bemol bosteza con los palillos en la mano; Ceci sigue la escalera de notas con la vista.

### Micro-misión R04-N04-P3 · Leer de a una

```meta
lugar: El Archivo Mudo
personajes: Ceci, Clave
carta: StreamReader | string? l = lector.ReadLine(); · while (l != null) { … l = lector.ReadLine(); } · null = no hay más
recompensa: xp 15, oro 15
```

#### Escena
Clave encuentra un rollo de partituras viejo y lo lee renglón por renglón, sin apuro.

#### Gheco sugiere
Un `StreamReader` es un **lector de archivos**. `ReadLine()` te da la línea siguiente cada vez que la llamás, y `null` cuando ya no quedan (como `Console.ReadLine()` cuando se acaba la entrada):

```csharp
using (StreamReader lector = new StreamReader("a.txt"))
{
    string? linea = lector.ReadLine();
    while (linea != null)
    {
        Console.WriteLine(linea);
        linea = lector.ReadLine();
    }
}
```

#### Desafío
Leé `rollo.txt` con un `StreamReader`, mostrando cada línea con `> ` adelante, y al final `Leí ` y la cantidad de líneas.

#### Código inicial
```csharp
File.WriteAllLines("rollo.txt", new[] { "sol", "la", "si" });
int cuantas = 0;

// leé con un StreamReader

Console.WriteLine($"Leí {cuantas} líneas");
```

#### Salida esperada
```
> sol
> la
> si
Leí 3 líneas
```

#### Solución
```csharp
File.WriteAllLines("rollo.txt", new[] { "sol", "la", "si" });
int cuantas = 0;

using (StreamReader lector = new StreamReader("rollo.txt"))
{
    string? linea = lector.ReadLine();
    while (linea != null)
    {
        Console.WriteLine($"> {linea}");
        cuantas++;
        linea = lector.ReadLine();
    }
}

Console.WriteLine($"Leí {cuantas} líneas");
```

#### Al superarla
Clave enrolla la partitura otra vez. —Tres renglones. Y ni uno se lo llevó el Liche.

#### Imagen
- Una partitura larga desenrollada sobre una mesa de piedra, con un farol azul encima, en un sótano con cajones, sin letras.
- Clave recorre la partitura con el dedo; Ceci lee por encima de su hombro.

### Micro-misión R04-N04-P4 · La forma corta

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: using var | using var e = new StreamWriter("a.txt"); · se cierra al terminar el método · sin llaves
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Don Cedro tiene un método para guardar recibos. Le sobran llaves por todos lados y quiere algo más prolijo.

#### Gheco sugiere
Hay una forma corta del `using`, sin llaves: pone `using` adelante de la declaración y el archivo se cierra solo cuando **termina el método** donde está.

```csharp
static void Anotar(string texto)
{
    using var escritor = new StreamWriter("notas.txt");
    escritor.WriteLine(texto);
}   // acá se cierra
```

`var` le deja a C# adivinar el tipo (acá, `StreamWriter`).

#### Desafío
Completá `Guardar`: con un `using var`, abrí un `StreamWriter` sobre `ruta` y escribí `texto` con `WriteLine`.

#### Código inicial
```csharp
Guardar("recibo.txt", "Violín: 200 corcheas");
Console.Write(File.ReadAllText("recibo.txt"));

static void Guardar(string ruta, string texto)
{
    File.WriteAllText(ruta, "");
}
```

#### Salida esperada
```
Violín: 200 corcheas
```

#### Solución
```csharp
Guardar("recibo.txt", "Violín: 200 corcheas");
Console.Write(File.ReadAllText("recibo.txt"));

static void Guardar(string ruta, string texto)
{
    using var escritor = new StreamWriter(ruta);
    escritor.WriteLine(texto);
}
```

#### Al superarla
—Menos llaves, el mismo cuidado —dice Don Cedro, y guarda el recibo en un cajón con llave.

#### Imagen
- Un taller de luthier de madera cálida con un cajón con cerradura de bronce abierto, y adentro un recibo de papel liso, con velas, sin letras.
- Don Cedro guarda el recibo en el cajón; Ceci le alcanza la llave.

### Micro-misión R04-N04-P5 · El troll del final del archivo

```meta
lugar: El Archivo Mudo
personajes: Ceci, Gheco
criatura: troll
carta: Troll | ReadLine() da null al final · usar ese null explota · leé con while (linea != null)
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un troll lee el archivo del coro **tres** veces, porque cree que hay tres voces. Hay dos. En la tercera vuelta, `ReadLine()` le da `null` y el programa explota.

#### Gheco sugiere
Cuando no quedan líneas, `ReadLine()` devuelve `null`, y `null.ToUpper()` lanza una `NullReferenceException`. El `!` después de `linea` le promete a C# que no es `null`, pero acá la promesa es mentira.

No hay que adivinar cuántas líneas tiene: se lee **mientras** no sea `null`, como en la micro-misión de leer de a una.

#### Desafío
Cambiá el `for` por un `while` que lea hasta que `ReadLine()` dé `null`, y mostrá cada línea en mayúsculas.

#### Código inicial
```csharp
File.WriteAllLines("coro.txt", new[] { "soprano", "tenor" });

using (StreamReader lector = new StreamReader("coro.txt"))
{
    for (int i = 0; i < 3; i++)
    {
        string? linea = lector.ReadLine();
        Console.WriteLine(linea!.ToUpper());
    }
}
```

#### Salida esperada
```
SOPRANO
TENOR
```

#### Solución
```csharp
File.WriteAllLines("coro.txt", new[] { "soprano", "tenor" });

using (StreamReader lector = new StreamReader("coro.txt"))
{
    string? linea = lector.ReadLine();
    while (linea != null)
    {
        Console.WriteLine(linea.ToUpper());
        linea = lector.ReadLine();
    }
}
```

#### Al superarla
El troll busca la tercera voz por todo el sótano. No la encuentra, porque nunca existió.

#### Imagen
- Un troll chiquito de piel color musgo, pelo de paja y chaleco remendado, buscando con un farol en un cajón vacío de un sótano de piedra, con cara de confundido.
- Gheco, sobre un estante, lo mira con un ojo abierto.

### Encargo R04-N04-E1 · Los turnos de Zed

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Zed lleva los turnos de la biblioteca del Imperio. Escribí un programa que lea nombres, uno por línea, hasta una línea vacía, y los escriba en `turnos.txt` con un `StreamWriter` adentro de un `using`, como `Turno 1: Ana`. Después, leé el archivo con un `StreamReader` hasta que `ReadLine()` dé `null`, mostrá cada línea y al final `Turnos: ` y la cantidad.

Con esta entrada:

```
Ana
Luis
Sol

```

se muestra:

```
Turno 1: Ana
Turno 2: Luis
Turno 3: Sol
Turnos: 3
```

#### Criterio de aprobación

- Escribe con un `StreamWriter` y lee con un `StreamReader`, los dos con `using`.
- Lee hasta que `ReadLine()` devuelve `null`.

#### Entrada de ejemplo

```
Ana
Luis
Sol

```

#### Salida esperada

```
Turno 1: Ana
Turno 2: Luis
Turno 3: Sol
Turnos: 3
```

#### Solución de referencia

```csharp
using (StreamWriter escritor = new StreamWriter("turnos.txt"))
{
    int n = 0;
    string? nombre = Console.ReadLine();
    while (!string.IsNullOrEmpty(nombre))
    {
        n++;
        escritor.WriteLine($"Turno {n}: {nombre}");
        nombre = Console.ReadLine();
    }
}

int cuantos = 0;
using (StreamReader lector = new StreamReader("turnos.txt"))
{
    string? linea = lector.ReadLine();
    while (linea != null)
    {
        Console.WriteLine(linea);
        cuantos++;
        linea = lector.ReadLine();
    }
}
Console.WriteLine($"Turnos: {cuantos}");
```

## R04-N05 · CSV: planillas en texto

```meta
tipo: tema
padre: R04-N04
precio: 10
criatura: ogro
temas: arch.csv
usa: arch.texto, prog.cadenas, prog.variables
```

### Crónica

En un cajón del Archivo Mudo, Ceci encuentra el inventario del Conservatorio: cada instrumento en un renglón, con su nombre, su dueño y su precio, separados por comas. El Liche lo dejó a medias: los precios no suman lo que deberían.

—Es un **CSV** —dice {mentor}—. Lo entiende cualquier planilla. Pero cuidado con el punto de los decimales: es la trampa preferida del Liche.

### Objetivos

- Partir una línea de CSV con `Split(',')`.
- Saltear el encabezado.
- Sumar una columna convirtiendo cada valor.
- Escribir tu propio CSV.
- Leer decimales con punto sin errores, con `CultureInfo.InvariantCulture`.

### Antes de empezar

- Archivos de texto (R04-N03), `Split` (Acto I) y `List` (R03-N01).

### Explicación

#### Un CSV

```
nombre,instrumento,precio
Ceci,violín,1200.50
Bemol,tambor,800.25
```

CSV quiere decir «valores separados por comas». La primera línea suele ser el **encabezado**: el nombre de cada columna. Cada línea siguiente es una fila.

#### Partir una línea

```csharp
string[] partes = "Ceci,violín,1200.50".Split(',');
// partes[0] = "Ceci", partes[1] = "violín", partes[2] = "1200.50"
```

Cada parte es un **texto**: para sumarla hay que convertirla con `int.Parse` o `decimal.Parse`.

#### La trampa del punto

En un CSV los decimales van con **punto**. Pero en una compu configurada en español, el punto es el separador de miles: `decimal.Parse("1200.50")` da **`120050`**, sin ningún error. Para leer el punto como coma decimal, se le indica que no use la configuración de la compu:

```csharp
using System.Globalization;     // arriba de todo

decimal precio = decimal.Parse("1200.50", CultureInfo.InvariantCulture);   // 1200,50
```

`CultureInfo.InvariantCulture` es una configuración fija, igual en todas las compus, que usa punto para los decimales. El `using System.Globalization;` de arriba deja usar `CultureInfo` sin escribir el nombre completo; va antes de cualquier otra línea.

### Código de ejemplo

```csharp
using System.Globalization;

string[] lineas =
{
    "nombre,instrumento,precio",
    "Ceci,violín,1200.50",
    "Bemol,tambor,800.25",
};
File.WriteAllLines("instrumentos.csv", lineas);

decimal total = 0;
string[] filas = File.ReadAllLines("instrumentos.csv");
for (int i = 1; i < filas.Length; i++)
{
    string[] partes = filas[i].Split(',');
    Console.WriteLine($"{partes[0]} toca {partes[1]}");
    total += decimal.Parse(partes[2], CultureInfo.InvariantCulture);
}
Console.WriteLine($"Total: {total}");
```

### Salida esperada

```
Ceci toca violín
Bemol toca tambor
Total: 2000,75
```

### ¿Para qué sirve?

Para pasar datos de un programa a otro: exportar ventas a una planilla, importar una lista de alumnos, leer los datos de un sensor. Casi cualquier sistema sabe leer y escribir CSV.

### Errores habituales

- **El ogro del punto decimal:** sin `InvariantCulture`, `1200.50` se lee como `120050`. No da error: da un número equivocado. Es el ogro más peligroso de este acto.
- **Sumar el encabezado:** `int.Parse("puntos")` explota. Empezá desde la línea `1`.
- **Datos con comas adentro:** `"Pérez, Juan"` se parte en dos. Para CSV simples alcanza `Split`; para los complicados hay bibliotecas.

### Micro-misión R04-N05-P1 · Partir la línea

```meta
lugar: El Archivo Mudo
personajes: Ceci, Clave
carta: Split | "a,b,c".Split(',') → { "a", "b", "c" } · cada parte es un texto
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
El primer renglón del inventario dice `Ceci,violín,15`. Clave quiere ver cada dato por separado.

#### Gheco sugiere
Una línea de CSV tiene los datos separados por comas. `Split(',')` la parte en esas comas y devuelve un arreglo de textos:

```csharp
string[] partes = "pera,uva".Split(',');
Console.WriteLine(partes[0]);   // pera
Console.WriteLine(partes[1]);   // uva
```

#### Desafío
Partí `linea` y mostrá cada dato con su etiqueta.

#### Código inicial
```csharp
string linea = "Ceci,violín,15";

// partila

Console.WriteLine("Nombre: ");
Console.WriteLine("Instrumento: ");
Console.WriteLine("Edad: ");
```

#### Salida esperada
```
Nombre: Ceci
Instrumento: violín
Edad: 15
```

#### Solución
```csharp
string linea = "Ceci,violín,15";

string[] partes = linea.Split(',');

Console.WriteLine($"Nombre: {partes[0]}");
Console.WriteLine($"Instrumento: {partes[1]}");
Console.WriteLine($"Edad: {partes[2]}");
```

#### Al superarla
—Tres cajones en un renglón —dice Clave—. La coma es la pared entre uno y otro.

#### Imagen
- Una tira de papel lisa sobre un cajón de piedra, cortada en tres pedazos por una tijera de bronce, en un sótano con faroles azules, sin letras.
- Clave sostiene la tijera; Ceci acomoda los tres pedazos uno al lado del otro.

### Micro-misión R04-N05-P2 · Saltear el encabezado

```meta
lugar: El Archivo Mudo
personajes: Ceci, Bemol
carta: Encabezado | la línea 0 son los nombres de las columnas · los datos empiezan en la 1 · for (int i = 1; …)
recompensa: xp 15, oro 15
```

#### Escena
Bemol lista los músicos del CSV, pero entre ellos aparece uno que se llama «nombre».

#### Gheco sugiere
La primera línea del CSV (la `0`) es el **encabezado**: dice qué hay en cada columna, no es un dato. Para saltearla, el `for` empieza en `1`:

```csharp
for (int i = 1; i < filas.Length; i++)
```

#### Desafío
Cambiá el `for` para que empiece en la línea `1`.

#### Código inicial
```csharp
File.WriteAllLines("musicos.csv", new[] { "nombre,instrumento", "Ceci,violín", "Bemol,tambor" });

string[] filas = File.ReadAllLines("musicos.csv");
for (int i = 0; i < filas.Length; i++)
{
    string[] partes = filas[i].Split(',');
    Console.WriteLine(partes[0]);
}
```

#### Salida esperada
```
Ceci
Bemol
```

#### Solución
```csharp
File.WriteAllLines("musicos.csv", new[] { "nombre,instrumento", "Ceci,violín", "Bemol,tambor" });

string[] filas = File.ReadAllLines("musicos.csv");
for (int i = 1; i < filas.Length; i++)
{
    string[] partes = filas[i].Split(',');
    Console.WriteLine(partes[0]);
}
```

#### Al superarla
—«Nombre» no toca nada —dice Bemol—. Y encima, nunca viene a ensayar.

#### Imagen
- Una planilla de papel liso con renglones y una primera fila de color distinto, clavada en un estante de un sótano de piedra con faroles azules, sin letras.
- Bemol tapa la primera fila con la mano; Ceci señala la segunda.

### Micro-misión R04-N05-P3 · Sumar la columna

```meta
lugar: El Archivo Mudo
personajes: Ceci, Clave
carta: Sumar una columna | partes[1] es texto · int.Parse(partes[1]) · total += …
recompensa: xp 15, oro 15
```

#### Escena
Clave quiere saber cuántos puntos sumó el coro en el último concurso. Están en la segunda columna.

#### Gheco sugiere
Cada parte del `Split` es un **texto**. Para sumarla, primero hay que convertirla:

```csharp
string[] partes = "Lía,9".Split(',');
int puntos = int.Parse(partes[1]);
```

#### Desafío
Recorré las filas (sin el encabezado) y sumá los puntos en `total`.

#### Código inicial
```csharp
File.WriteAllLines("concurso.csv", new[] { "nombre,puntos", "Ceci,9", "Bemol,8", "Lía,10" });

int total = 0;
string[] filas = File.ReadAllLines("concurso.csv");

// sumá la segunda columna

Console.WriteLine($"Total: {total}");
```

#### Salida esperada
```
Total: 27
```

#### Solución
```csharp
File.WriteAllLines("concurso.csv", new[] { "nombre,puntos", "Ceci,9", "Bemol,8", "Lía,10" });

int total = 0;
string[] filas = File.ReadAllLines("concurso.csv");

for (int i = 1; i < filas.Length; i++)
{
    string[] partes = filas[i].Split(',');
    total += int.Parse(partes[1]);
}

Console.WriteLine($"Total: {total}");
```

#### Al superarla
—Veintisiete —dice Clave—. Nada mal, para un coro que hace un mes no sabía leer una partitura.

#### Imagen
- Una balanza de bronce sobre una mesa de piedra con tres montoncitos de monedas doradas en un platillo, en un sótano con faroles azules, sin letras.
- Clave mira la balanza; Ceci suma con los dedos.

### Micro-misión R04-N05-P4 · Escribir una planilla

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: Armar un CSV | List<string> lineas · Add("encabezado") · Add($"{a},{b}") · File.WriteAllLines(ruta, lineas)
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Don Cedro tiene sus precios en dos arreglos y quiere pasarlos a una planilla para el Gremio.

#### Gheco sugiere
Un CSV se arma como cualquier texto: primero el encabezado, después una línea por fila, con los datos separados por comas. Se juntan en una `List<string>` y `File.WriteAllLines` también acepta una lista:

```csharp
List<string> lineas = new List<string>();
lineas.Add("fruta,kilos");
lineas.Add($"{fruta},{kilos}");
File.WriteAllLines("frutas.csv", lineas);
```

#### Desafío
Agregá a `lineas` el encabezado `instrumento,precio` y una línea por cada instrumento, antes de escribir el archivo.

#### Código inicial
```csharp
string[] instrumentos = { "violín", "viola", "chelo" };
int[] precios = { 200, 250, 400 };

List<string> lineas = new List<string>();

// armá el CSV

File.WriteAllLines("precios.csv", lineas);
Console.Write(File.ReadAllText("precios.csv"));
```

#### Salida esperada
```
instrumento,precio
violín,200
viola,250
chelo,400
```

#### Solución
```csharp
string[] instrumentos = { "violín", "viola", "chelo" };
int[] precios = { 200, 250, 400 };

List<string> lineas = new List<string>();

lineas.Add("instrumento,precio");
for (int i = 0; i < instrumentos.Length; i++)
{
    lineas.Add($"{instrumentos[i]},{precios[i]}");
}

File.WriteAllLines("precios.csv", lineas);
Console.Write(File.ReadAllText("precios.csv"));
```

#### Al superarla
Don Cedro lee la planilla de arriba para abajo y asiente. —Hasta el Gremio la va a entender.

#### Imagen
- Un taller de luthier de madera cálida con un violín, una viola y un chelo colgados en fila, cada uno con una etiqueta de cartón lisa colgando, con velas, sin letras.
- Don Cedro cuelga la última etiqueta; Ceci sostiene la escalera.

### Micro-misión R04-N05-P5 · El ogro del punto decimal

```meta
lugar: El Archivo Mudo
personajes: Ceci, Gheco
criatura: ogro
carta: Ogro | decimal.Parse("1200.50") da 120050 · con CultureInfo.InvariantCulture da 1200,50 · using System.Globalization;
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un ogro sumó los precios del inventario y le dio un número enorme. No explotó nada: el programa da un resultado, pero está mal.

#### Gheco sugiere
En el CSV los decimales vienen con **punto**. En una compu en español, el punto es el separador de miles, y `decimal.Parse("1200.50")` da `120050`, sin avisar.

`CultureInfo.InvariantCulture` es una configuración fija que lee el punto como decimal. Se pasa como segundo dato de `decimal.Parse`:

```csharp
decimal p = decimal.Parse("3.75", CultureInfo.InvariantCulture);   // 3,75
```

El `using System.Globalization;` de arriba ya está: es lo que deja escribir `CultureInfo` sin su nombre completo.

#### Desafío
Agregale `CultureInfo.InvariantCulture` al `decimal.Parse`.

#### Código inicial
```csharp
using System.Globalization;

File.WriteAllLines("inventario.csv", new[] { "instrumento,precio", "violín,1200.50", "atril,79.50" });

decimal total = 0;
string[] filas = File.ReadAllLines("inventario.csv");
for (int i = 1; i < filas.Length; i++)
{
    string[] partes = filas[i].Split(',');
    total += decimal.Parse(partes[1]);
}
Console.WriteLine($"Total: {total}");
```

#### Salida esperada
```
Total: 1280,00
```

#### Solución
```csharp
using System.Globalization;

File.WriteAllLines("inventario.csv", new[] { "instrumento,precio", "violín,1200.50", "atril,79.50" });

decimal total = 0;
string[] filas = File.ReadAllLines("inventario.csv");
for (int i = 1; i < filas.Length; i++)
{
    string[] partes = filas[i].Split(',');
    total += decimal.Parse(partes[1], CultureInfo.InvariantCulture);
}
Console.WriteLine($"Total: {total}");
```

#### Al superarla
El ogro mira su número gigante, mira el nuevo, y se rasca la cabeza. Le parecía mucho más lindo el otro.

#### Imagen
- Un ogro grandote y simpático de piel gris azulada y pelo naranja, mirando con sorpresa una pila enorme de monedas doradas que se achica, en un sótano de piedra con faroles azules.
- Gheco, sobre un cajón, le muestra una sola moneda con las dos patitas.

### Encargo R04-N05-E1 · Las ventas de Baldo

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Baldo pasa las ventas del puesto en CSV: la primera línea es el encabezado `producto,cantidad,precio`, y después una venta por línea, hasta una línea vacía. Los precios vienen con punto. Escribí un programa que muestre cada venta con su subtotal (`cantidad x precio`) y al final el total.

Con esta entrada:

```
producto,cantidad,precio
miel,3,2.50
pan,2,1.25

```

se muestra:

```
miel: 7,50
pan: 2,50
Total: 10,00
```

#### Criterio de aprobación

- Saltea el encabezado y parte cada línea con `Split(',')`.
- Lee los precios con `CultureInfo.InvariantCulture`.

#### Entrada de ejemplo

```
producto,cantidad,precio
miel,3,2.50
pan,2,1.25

```

#### Salida esperada

```
miel: 7,50
pan: 2,50
Total: 10,00
```

#### Solución de referencia

```csharp
using System.Globalization;

decimal total = 0;
Console.ReadLine();
string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    string[] partes = linea.Split(',');
    int cantidad = int.Parse(partes[1]);
    decimal precio = decimal.Parse(partes[2], CultureInfo.InvariantCulture);
    decimal subtotal = cantidad * precio;
    Console.WriteLine($"{partes[0]}: {subtotal}");
    total += subtotal;
    linea = Console.ReadLine();
}
Console.WriteLine($"Total: {total}");
```

## R04-N06 · JSON: guardar objetos enteros

```meta
tipo: tema
padre: R04-N05
precio: 10
criatura: goblin
temas: arch.json
usa: arch.texto, poo.records, col.listas
```

### Crónica

El Liche ya no sabe qué hacer: cada cosa que borra, Ceci la escribe de nuevo. Pero hay algo que todavía no puede guardar: la **partida** de Bemol en el juego de la Feria, con su nombre, su nivel y todo lo que juntó. En un CSV no entra una lista adentro de otra.

—Para eso está el **JSON** —dice {mentor}—. Es la forma de escribir datos más usada del mundo. Guarda un objeto entero, con sus listas adentro, en un texto que entiende cualquier lenguaje.

### Objetivos

- Pasar un objeto a texto JSON con `JsonSerializer.Serialize`.
- Pasar un JSON a objeto con `JsonSerializer.Deserialize`.
- Escribirlo lindo, con sangría.
- Guardarlo en un archivo y cargarlo en la siguiente vuelta.
- Atrapar un JSON roto con `JsonException`.

### Antes de empezar

- `record` (Acto II), `List` (R03-N01), archivos (R04-N03) y `try`/`catch` (R04-N01).

### Explicación

#### Un JSON

```json
{"Nombre":"Ceci","Nivel":3,"Objetos":["arco","atril"]}
```

- Entre `{ }` va un **objeto**, con pares `"nombre":valor` separados por comas.
- Los textos van entre comillas; los números, no.
- Entre `[ ]` va una **lista**.

#### De objeto a texto, y de vuelta

```csharp
using System.Text.Json;     // arriba de todo

string json = JsonSerializer.Serialize(partida);                // objeto → texto
Partida p = JsonSerializer.Deserialize<Partida>(json)!;         // texto → objeto
```

`JsonSerializer` («el que pasa a JSON») es de C#; el `using System.Text.Json;` deja usarlo sin el nombre completo. Funciona con `record` y con clases de propiedades públicas, y con las listas que tengan adentro. `Deserialize<Partida>` dice **de qué tipo** es el objeto que tiene que armar; el `!` del final es porque podría devolver `null` (si el texto fuera `null`), y le prometés a C# que no.

#### Lindo para leer

```csharp
var opciones = new JsonSerializerOptions { WriteIndented = true };
string lindo = JsonSerializer.Serialize(partida, opciones);
```

`WriteIndented = true` pone un dato por línea, con sangría.

#### Un JSON roto

Si el texto no es un JSON válido, o un dato no tiene el tipo que esperaba (un texto donde va un número), `Deserialize` lanza una `JsonException`. Al leer un archivo que alguien pudo tocar a mano, hay que atraparla.

### Código de ejemplo

```csharp
using System.Text.Json;

Partida partida = new Partida("Ceci", 3, new List<string> { "arco", "atril" });
string json = JsonSerializer.Serialize(partida);
Console.WriteLine(json);

File.WriteAllText("partida.json", json);
Partida cargada = JsonSerializer.Deserialize<Partida>(File.ReadAllText("partida.json"))!;
Console.WriteLine($"{cargada.Nombre} está en el nivel {cargada.Nivel}");

record Partida(string Nombre, int Nivel, List<string> Objetos);
```

### Salida esperada

```
{"Nombre":"Ceci","Nivel":3,"Objetos":["arco","atril"]}
Ceci está en el nivel 3
```

### ¿Para qué sirve?

Para guardar partidas, configuraciones y cualquier dato con forma de objeto. Y es el idioma de las APIs de internet: cuando una app le pide datos a un servidor, casi siempre vienen en JSON (lo vas a ver en el Acto V).

### Errores habituales

- **Olvidar el tipo en `Deserialize`:** sin `<Partida>`, C# no sabe qué objeto armar.
- **Propiedades privadas o campos:** `JsonSerializer` guarda las **propiedades públicas**. Lo privado no se guarda.
- **No atrapar el JSON roto:** un archivo editado a mano puede tener cualquier cosa. El **goblin** del JSON roto pone un texto donde va un número.
- **Las letras con tilde:** en el JSON, `violín` puede aparecer como `violín`. Es lo mismo, escrito de otra forma; al leerlo de vuelta queda `violín`.

### Micro-misión R04-N06-P1 · De objeto a texto

```meta
lugar: El Archivo Mudo
personajes: Ceci, Clave
carta: Serialize | using System.Text.Json; · JsonSerializer.Serialize(objeto) → texto JSON
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Clave quiere guardar la ficha del violín de Ceci entera, de una sola vez, antes de que el Liche se la lleve.

#### Gheco sugiere
`JsonSerializer.Serialize(objeto)` convierte un objeto en un **texto JSON**: entre llaves, cada propiedad con su nombre entre comillas y su valor.

```csharp
string json = JsonSerializer.Serialize(new Nota("do", 4));
// {"Nombre":"do","Tiempos":4}
```

El `using System.Text.Json;` de arriba ya está: es lo que deja usar `JsonSerializer`.

#### Desafío
Pasá `violin` a JSON con `JsonSerializer.Serialize` y mostralo.

#### Código inicial
```csharp
using System.Text.Json;

Instrumento violin = new Instrumento("Violin", 4);
string json = "";

Console.WriteLine(json);

record Instrumento(string Nombre, int Cuerdas);
```

#### Salida esperada
```
{"Nombre":"Violin","Cuerdas":4}
```

#### Solución
```csharp
using System.Text.Json;

Instrumento violin = new Instrumento("Violin", 4);
string json = JsonSerializer.Serialize(violin);

Console.WriteLine(json);

record Instrumento(string Nombre, int Cuerdas);
```

#### Al superarla
—Todo el violín en un renglón —dice Clave—. El Liche puede apagar las velas que quiera.

#### Imagen
- Un violín sobre un cajón de piedra del que sale una cinta de luz dorada que se enrolla en un pergamino liso, en un sótano con faroles azules, sin letras.
- Clave enrolla el pergamino; Ceci mira cómo la luz sale del violín.

### Micro-misión R04-N06-P2 · De texto a objeto

```meta
lugar: El Archivo Mudo
personajes: Ceci, Bemol
carta: Deserialize | JsonSerializer.Deserialize<Tipo>(json)! → el objeto · <Tipo> dice qué armar
recompensa: xp 15, oro 15
```

#### Escena
Bemol encontró un pergamino con un JSON. Quiere saber qué instrumento describe, sin leer las llaves y las comillas.

#### Gheco sugiere
`JsonSerializer.Deserialize<Tipo>(json)` hace lo contrario: lee el texto JSON y **arma el objeto**. Entre `< >` va el tipo que tiene que armar.

```csharp
Nota n = JsonSerializer.Deserialize<Nota>("{\"Nombre\":\"do\",\"Tiempos\":4}")!;
Console.WriteLine(n.Nombre);   // do
```

El `!` del final es porque `Deserialize` podría devolver `null`; acá le prometés a C# que no. Las `\"` son comillas adentro de un texto.

#### Desafío
Convertí `json` en un `Instrumento` y mostrá `Chelo: 4 cuerdas`.

#### Código inicial
```csharp
using System.Text.Json;

string json = "{\"Nombre\":\"Chelo\",\"Cuerdas\":4}";

// armá el objeto

Console.WriteLine(json);

record Instrumento(string Nombre, int Cuerdas);
```

#### Salida esperada
```
Chelo: 4 cuerdas
```

#### Solución
```csharp
using System.Text.Json;

string json = "{\"Nombre\":\"Chelo\",\"Cuerdas\":4}";

Instrumento chelo = JsonSerializer.Deserialize<Instrumento>(json)!;

Console.WriteLine($"{chelo.Nombre}: {chelo.Cuerdas} cuerdas");

record Instrumento(string Nombre, int Cuerdas);
```

#### Al superarla
—Un chelo —dice Bemol, decepcionado—. Yo esperaba un tambor.

#### Imagen
- Un pergamino abierto de papel liso que flota sobre un cajón y del que sale un chelo de luz dorada, en un sótano de piedra con faroles azules, sin letras.
- Bemol mira el chelo de luz con cara de decepción; Ceci se ríe.

### Micro-misión R04-N06-P3 · Lindo para leer

```meta
lugar: El Archivo Mudo
personajes: Ceci, Clave
carta: Con sangría | new JsonSerializerOptions { WriteIndented = true } · Serialize(objeto, opciones)
recompensa: xp 15, oro 15
```

#### Escena
Clave quiere que el JSON de la partida se pueda leer a ojo, renglón por renglón, como una partitura bien copiada.

#### Gheco sugiere
`Serialize` acepta un segundo dato con **opciones**. `WriteIndented = true` («escribí con sangría») pone cada dato en su propia línea:

```csharp
var opciones = new JsonSerializerOptions { WriteIndented = true };
string json = JsonSerializer.Serialize(objeto, opciones);
```

Las llaves `{ … }` después de `new JsonSerializerOptions` le dan valor a sus propiedades al crearlo.

#### Desafío
Creá las opciones con `WriteIndented = true` y pasáselas a `Serialize`.

#### Código inicial
```csharp
using System.Text.Json;

Partida p = new Partida("Ceci", 2);

string json = JsonSerializer.Serialize(p);
Console.WriteLine(json);

record Partida(string Nombre, int Nivel);
```

#### Salida esperada
```
{
  "Nombre": "Ceci",
  "Nivel": 2
}
```

#### Solución
```csharp
using System.Text.Json;

Partida p = new Partida("Ceci", 2);

var opciones = new JsonSerializerOptions { WriteIndented = true };
string json = JsonSerializer.Serialize(p, opciones);
Console.WriteLine(json);

record Partida(string Nombre, int Nivel);
```

#### Al superarla
—Así sí —dice Clave—. Un dato por renglón, como los atriles de una orquesta.

#### Imagen
- Un pergamino largo de papel liso colgando de un estante, con renglones de luz dorada bien alineados, en un sótano de piedra con faroles azules, sin letras.
- Clave lo revisa con los anteojos en la punta de la nariz; Ceci espera su aprobación.

### Micro-misión R04-N06-P4 · La partida que sube

```meta
lugar: El Archivo Mudo
personajes: Ceci, Bemol
carta: Guardar y cargar | si existe: Deserialize(File.ReadAllText) · si no: una nueva · sube · File.WriteAllText(Serialize)
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol juega tres veces seguidas. Cada vez que abre el juego, tiene que seguir desde el nivel donde quedó, no desde cero.

#### Gheco sugiere
Cada vuelta del `for` hace de cuenta que es una vez que se abre el juego:

1. Si existe `partida.json`, se carga con `Deserialize`. Si no, se arranca una nueva en el nivel `0`.
2. Se sube un nivel: como un `record` no se cambia, se crea uno nuevo con `with` (Acto II).
3. Se guarda con `Serialize` y `File.WriteAllText`.

```csharp
p = p with { Nivel = p.Nivel + 1 };
```

#### Desafío
Completá los pasos 1 y 3 adentro del `for`.

#### Código inicial
```csharp
using System.Text.Json;

for (int vez = 0; vez < 3; vez++)
{
    Partida p = new Partida("Bemol", 0);
    // 1. si existe "partida.json", cargala

    p = p with { Nivel = p.Nivel + 1 };
    Console.WriteLine($"Nivel {p.Nivel}");

    // 3. guardala

}

record Partida(string Nombre, int Nivel);
```

#### Salida esperada
```
Nivel 1
Nivel 2
Nivel 3
```

#### Solución
```csharp
using System.Text.Json;

for (int vez = 0; vez < 3; vez++)
{
    Partida p = new Partida("Bemol", 0);
    if (File.Exists("partida.json"))
    {
        p = JsonSerializer.Deserialize<Partida>(File.ReadAllText("partida.json"))!;
    }

    p = p with { Nivel = p.Nivel + 1 };
    Console.WriteLine($"Nivel {p.Nivel}");

    File.WriteAllText("partida.json", JsonSerializer.Serialize(p));
}

record Partida(string Nombre, int Nivel);
```

#### Al superarla
—¡Nivel tres! —grita Bemol—. Y sin empezar de cero ni una vez.

#### Imagen
- Una escalera de tres escalones de luz dorada que sube desde un cajón abierto, en un sótano de piedra con faroles azules, sin letras.
- Bemol sube los escalones de a saltos con el tambor colgando; Ceci lo aplaude desde abajo.

### Micro-misión R04-N06-P5 · El goblin del JSON roto

```meta
lugar: El Archivo Mudo
personajes: Ceci, Gheco
criatura: goblin
carta: Goblin | un texto donde va un número · Deserialize lanza JsonException · atrapala y seguí
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un goblin abrió `partida.json` a mano y le puso el nivel con letras: `"tres"`. Al cargarla, el programa explota.

#### Gheco sugiere
Si el JSON está roto, o un dato no es del tipo que espera (un texto donde va un número), `Deserialize` lanza una `JsonException`. Un archivo que alguien pudo tocar a mano hay que leerlo adentro de un `try`:

```csharp
try
{
    var p = JsonSerializer.Deserialize<Partida>(json)!;
}
catch (JsonException)
{
    Console.WriteLine("está roto");
}
```

#### Desafío
Envolvé la carga en un `try`, con un `catch (JsonException)` que muestre `La partida guardada está rota`.

#### Código inicial
```csharp
using System.Text.Json;

File.WriteAllText("partida.json", "{\"Nombre\":\"Ceci\",\"Nivel\":\"tres\"}");

Partida p = JsonSerializer.Deserialize<Partida>(File.ReadAllText("partida.json"))!;
Console.WriteLine($"Nivel {p.Nivel}");

Console.WriteLine("Empieza el juego");

record Partida(string Nombre, int Nivel);
```

#### Salida esperada
```
La partida guardada está rota
Empieza el juego
```

#### Solución
```csharp
using System.Text.Json;

File.WriteAllText("partida.json", "{\"Nombre\":\"Ceci\",\"Nivel\":\"tres\"}");

try
{
    Partida p = JsonSerializer.Deserialize<Partida>(File.ReadAllText("partida.json"))!;
    Console.WriteLine($"Nivel {p.Nivel}");
}
catch (JsonException)
{
    Console.WriteLine("La partida guardada está rota");
}

Console.WriteLine("Empieza el juego");

record Partida(string Nombre, int Nivel);
```

#### Al superarla
El goblin escribe `"tres"` otra vez, más grande, como si así fuera a funcionar. No funciona.

#### Imagen
- Un goblin chico de orejas puntiagudas escribiendo con un pincel gordo sobre un pergamino liso clavado en un cajón, en un sótano de piedra con faroles azules, sin letras.
- Gheco, sobre el cajón, le saca el pincel de la mano con la cola.

### Encargo R04-N06-E1 · Los faroles de Nima

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Nima vende faroles en la Feria y quiere guardar su catálogo en JSON. Escribí un programa que lea faroles como `nombre,precio` (el precio es entero), uno por línea, hasta una línea vacía, y los guarde en una `List<Farol>`. Guardá la lista entera en `faroles.json` con `JsonSerializer`, leela de vuelta del archivo en otra variable y, con esa, mostrá cuántos hay y cuál es el más caro.

Con esta entrada:

```
Farol rojo,20
Farol azul,35
Farol verde,15

```

se muestra:

```
Guardados: 3
El más caro: Farol azul (35)
```

#### Criterio de aprobación

- Guarda la lista con `JsonSerializer.Serialize` y la lee con `Deserialize<List<Farol>>`.
- Los resultados salen de la lista leída del archivo.

#### Entrada de ejemplo

```
Farol rojo,20
Farol azul,35
Farol verde,15

```

#### Salida esperada

```
Guardados: 3
El más caro: Farol azul (35)
```

#### Solución de referencia

```csharp
using System.Text.Json;

List<Farol> faroles = new List<Farol>();
string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    string[] partes = linea.Split(',');
    faroles.Add(new Farol(partes[0], int.Parse(partes[1])));
    linea = Console.ReadLine();
}

File.WriteAllText("faroles.json", JsonSerializer.Serialize(faroles));
List<Farol> leidos = JsonSerializer.Deserialize<List<Farol>>(File.ReadAllText("faroles.json"))!;

Farol caro = leidos.MaxBy(f => f.Precio)!;
Console.WriteLine($"Guardados: {leidos.Count}");
Console.WriteLine($"El más caro: {caro.Nombre} ({caro.Precio})");

record Farol(string Nombre, int Precio);
```

## R04-N07 · Jefe: el Liche del Archivo Mudo

```meta
tipo: jefe
padre: R04-N06
precio: 10
criatura: dragon
insignia: Guardiana de la Memoria
insignia_descripcion: Venciste al Liche del Archivo Mudo: tus programas no se caen con un error y recuerdan lo que hicieron, en texto, CSV o JSON.
usa: err.excepciones, arch.texto, arch.csv, arch.json
```

### Crónica

En el fondo del Archivo Mudo, el **Liche** espera con su apagavelas. Es alto y flaco, con una túnica larga hecha de páginas en blanco: todo lo que borró. Cada vez que apaga una vela, alguien del Conservatorio se olvida de algo que ensayó.

—No se lo vence a golpes —dice {mentor}—. Se lo vence **recordando**. Encendé cuatro velas: un programa que no se cae, uno que anota lo que pasa, una planilla bien leída y una memoria en JSON. Con la quinta, el Archivo vuelve a hablar.

### Objetivos

- Juntar en un programa excepciones, archivos de texto, CSV y JSON.
- Encontrar y arreglar los errores de a uno.

### Antes de empezar

- Todo el Archivo Mudo (R04-N01 a R04-N06).

### Explicación

#### Qué usar para qué

| Necesito… | Uso |
|---|---|
| que un dato malo no corte el programa | `try` / `catch` |
| avisar que algo no tiene sentido | `throw` |
| guardar texto, renglón por renglón | `File.AppendAllText`, `StreamWriter` |
| una planilla | CSV con `Split(',')` e `InvariantCulture` |
| un objeto entero, con listas adentro | JSON con `JsonSerializer` |
| no explotar con un archivo que no está | `File.Exists` |

#### Cómo encender una vela

1. Ensayá y leé el primer error: el compilador te dice la línea.
2. Si explota al correr, mirá el nombre de la excepción: te dice qué pasó.
3. Si no explota pero da otra cosa, seguí los datos paso a paso.

### Código de ejemplo

```csharp
using System.Text.Json;

string[] entradas = { "Canon", "", "Tango" };
List<string> tocadas = new List<string>();
foreach (string obra in entradas)
{
    try
    {
        if (obra == "")
        {
            throw new ArgumentException("obra sin nombre");
        }
        tocadas.Add(obra);
        File.AppendAllText("bitacora.txt", $"Tocada: {obra}\n");
    }
    catch (ArgumentException e)
    {
        File.AppendAllText("bitacora.txt", $"Error: {e.Message}\n");
    }
}

File.WriteAllText("tocadas.json", JsonSerializer.Serialize(tocadas));
Console.Write(File.ReadAllText("bitacora.txt"));
Console.WriteLine(File.ReadAllText("tocadas.json"));
```

### Salida esperada

```
Tocada: Canon
Error: obra sin nombre
Tocada: Tango
["Canon","Tango"]
```

### ¿Para qué sirve?

Así trabaja casi cualquier programa de verdad: lee datos que pueden venir mal, no se cae por eso, anota lo que pasó y guarda su estado para la próxima vez.

### Errores habituales

- **Arreglar todo junto:** un error por vez. El siguiente aparece recién cuando arreglás el anterior.
- **Atrapar con un `catch` vacío para que «ande»:** el programa sigue, pero sin avisar de nada. El Liche adora los `catch` vacíos.
- **Guardar y no volver a leer:** si no lo cargás la próxima vez, es como si no lo hubieras guardado.

### Micro-misión R04-N07-P1 · La primera vela

```meta
lugar: El Archivo Mudo
personajes: Ceci, Clave
criatura: dragon
carta: Vela 1 | un try adentro del bucle · el dato malo se cuenta · los buenos se suman
recompensa: xp 20, oro 20, monedas 4
```

#### Escena
El Liche ensució el registro de ensayos con datos rotos: una palabra donde iba un número y un renglón vacío. Con el primer dato malo, el programa se apaga.

#### Gheco sugiere
`int.Parse` lanza una `FormatException` tanto con `"cuatro"` como con un texto vacío (`""`). Si el `try` va **adentro** del `foreach`, cada línea tiene su propio suplente: la mala se cuenta y el bucle sigue con la siguiente.

#### Desafío
Envolvé la suma en un `try` adentro del `foreach`, y en el `catch (FormatException)` sumale uno a `rotas`.

#### Código inicial
```csharp
File.WriteAllLines("registro.txt", new[] { "4", "cuatro", "6", "", "5" });

int suma = 0;
int rotas = 0;
foreach (string linea in File.ReadAllLines("registro.txt"))
{
    suma += int.Parse(linea);
}
Console.WriteLine($"Suma: {suma}");
Console.WriteLine($"Rotas: {rotas}");
```

#### Salida esperada
```
Suma: 15
Rotas: 2
```

#### Solución
```csharp
File.WriteAllLines("registro.txt", new[] { "4", "cuatro", "6", "", "5" });

int suma = 0;
int rotas = 0;
foreach (string linea in File.ReadAllLines("registro.txt"))
{
    try
    {
        suma += int.Parse(linea);
    }
    catch (FormatException)
    {
        rotas++;
    }
}
Console.WriteLine($"Suma: {suma}");
Console.WriteLine($"Rotas: {rotas}");
```

#### Al superarla
Se enciende la primera vela. El Liche levanta el apagavelas, pero la llama no se apaga: el programa ya no se cae.

#### Imagen
- Un liche de caricatura alto y flaco, con túnica larga y cerrada hecha de páginas en blanco y capucha, sosteniendo un apagavelas de bronce frente a una vela recién encendida, en un sótano de piedra con cajones y faroles azules, sin letras.
- Ceci enciende la vela con un fósforo; Clave, detrás, sostiene la batuta en alto.

### Micro-misión R04-N07-P2 · La segunda vela

```meta
lugar: El Archivo Mudo
personajes: Ceci, Bemol
criatura: dragon
carta: Vela 2 | throw para la obra sin nombre · AppendAllText para no borrar lo anterior · en el try y en el catch
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
La bitácora de la noche anota cada obra tocada y cada error. Pero el Liche hizo que cada renglón borre al anterior: al final solo queda el último.

#### Gheco sugiere
`File.WriteAllText` **reemplaza** el archivo entero. Si se usa en cada vuelta del bucle, solo sobrevive lo de la última. Para que la bitácora crezca, tiene que ser `File.AppendAllText`, tanto en el `try` como en el `catch`.

#### Desafío
Cambiá los dos `File.WriteAllText` por `File.AppendAllText`.

#### Código inicial
```csharp
string[] obras = { "Canon", "", "Tango" };
foreach (string o in obras)
{
    try
    {
        if (o == "")
        {
            throw new ArgumentException("obra sin nombre");
        }
        File.WriteAllText("bitacora.txt", $"Tocada: {o}\n");
    }
    catch (ArgumentException e)
    {
        File.WriteAllText("bitacora.txt", $"Error: {e.Message}\n");
    }
}
Console.Write(File.ReadAllText("bitacora.txt"));
```

#### Salida esperada
```
Tocada: Canon
Error: obra sin nombre
Tocada: Tango
```

#### Solución
```csharp
string[] obras = { "Canon", "", "Tango" };
foreach (string o in obras)
{
    try
    {
        if (o == "")
        {
            throw new ArgumentException("obra sin nombre");
        }
        File.AppendAllText("bitacora.txt", $"Tocada: {o}\n");
    }
    catch (ArgumentException e)
    {
        File.AppendAllText("bitacora.txt", $"Error: {e.Message}\n");
    }
}
Console.Write(File.ReadAllText("bitacora.txt"));
```

#### Al superarla
La segunda vela se enciende. Las páginas en blanco de la túnica del Liche empiezan a llenarse de renglones.

#### Imagen
- Un liche de caricatura alto y flaco, con túnica larga y cerrada de páginas en blanco, algunas ya con renglones dorados, retrocediendo frente a dos velas encendidas, en un sótano de piedra con faroles azules, sin letras.
- Bemol escribe en un cuaderno abierto; Ceci protege las velas con las manos.

### Micro-misión R04-N07-P3 · La tercera vela

```meta
lugar: El Archivo Mudo
personajes: Ceci, Don Cedro
criatura: dragon
carta: Vela 3 | el for empieza en 1 (sin encabezado) · decimal.Parse(x, CultureInfo.InvariantCulture)
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
Las notas del examen del Conservatorio están en una planilla. El Liche le dejó dos trampas: el programa intenta convertir el encabezado y lee mal el punto decimal.

#### Gheco sugiere
Dos cosas del nodo de los CSV:

- La línea `0` es el **encabezado** (`nombre,nota`): `decimal.Parse("nota")` explota. El `for` tiene que empezar en `1`.
- Las notas vienen con punto: sin `CultureInfo.InvariantCulture`, `8.50` se lee como `850`.

#### Desafío
Arreglá las dos trampas: que el `for` empiece en `1` y que el `decimal.Parse` use `CultureInfo.InvariantCulture`.

#### Código inicial
```csharp
using System.Globalization;

File.WriteAllLines("notas.csv", new[] { "nombre,nota", "Ceci,8.50", "Bemol,9.25", "Lía,7.25" });

string[] filas = File.ReadAllLines("notas.csv");
decimal total = 0;
decimal mejor = 0;
string quien = "";
for (int i = 0; i < filas.Length; i++)
{
    string[] partes = filas[i].Split(',');
    decimal nota = decimal.Parse(partes[1]);
    total += nota;
    if (nota > mejor)
    {
        mejor = nota;
        quien = partes[0];
    }
}
Console.WriteLine($"Total: {total}");
Console.WriteLine($"Mejor: {quien}");
```

#### Salida esperada
```
Total: 25,00
Mejor: Bemol
```

#### Solución
```csharp
using System.Globalization;

File.WriteAllLines("notas.csv", new[] { "nombre,nota", "Ceci,8.50", "Bemol,9.25", "Lía,7.25" });

string[] filas = File.ReadAllLines("notas.csv");
decimal total = 0;
decimal mejor = 0;
string quien = "";
for (int i = 1; i < filas.Length; i++)
{
    string[] partes = filas[i].Split(',');
    decimal nota = decimal.Parse(partes[1], CultureInfo.InvariantCulture);
    total += nota;
    if (nota > mejor)
    {
        mejor = nota;
        quien = partes[0];
    }
}
Console.WriteLine($"Total: {total}");
Console.WriteLine($"Mejor: {quien}");
```

#### Al superarla
—Bemol, la mejor nota —dice Don Cedro, sorprendido—. Habrá que revisar la planilla otra vez. —La revisamos —dice Ceci—. Está bien.

#### Imagen
- Un liche de caricatura alto y flaco, con túnica larga y cerrada de páginas en blanco, tapándose los ojos frente a tres velas encendidas, en un sótano de piedra con faroles azules, sin letras.
- Don Cedro sostiene una planilla de papel liso; Ceci enciende la tercera vela.

### Micro-misión R04-N07-P4 · La cuarta vela

```meta
lugar: El Archivo Mudo
personajes: Ceci, Clave
criatura: dragon
carta: Vela 4 | Serialize la lista → archivo · Deserialize<List<Musico>> del archivo · <List<Musico>> es el tipo entero
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
La orquesta ya está guardada en `orquesta.json`, pero nadie la vuelve a cargar: para el programa, los músicos no existen.

#### Gheco sugiere
`Deserialize` arma lo que le digas entre `< >`. Si en el archivo hay una **lista** de músicos, el tipo es la lista entera: `List<Musico>`.

```csharp
List<Musico> m = JsonSerializer.Deserialize<List<Musico>>(texto)!;
```

#### Desafío
En lugar de la lista vacía, cargá `cargados` leyendo `orquesta.json` y deserializándolo como `List<Musico>`.

#### Código inicial
```csharp
using System.Text.Json;

List<Musico> orquesta = new List<Musico>
{
    new Musico("Ceci", "violín"),
    new Musico("Bemol", "tambor"),
    new Musico("Clave", "batuta"),
};
File.WriteAllText("orquesta.json", JsonSerializer.Serialize(orquesta));

List<Musico> cargados = new List<Musico>();

Console.WriteLine($"Recordados: {cargados.Count}");
Console.WriteLine(string.Join(", ", cargados.Select(m => m.Nombre)));

record Musico(string Nombre, string Instrumento);
```

#### Salida esperada
```
Recordados: 3
Ceci, Bemol, Clave
```

#### Solución
```csharp
using System.Text.Json;

List<Musico> orquesta = new List<Musico>
{
    new Musico("Ceci", "violín"),
    new Musico("Bemol", "tambor"),
    new Musico("Clave", "batuta"),
};
File.WriteAllText("orquesta.json", JsonSerializer.Serialize(orquesta));

List<Musico> cargados = JsonSerializer.Deserialize<List<Musico>>(File.ReadAllText("orquesta.json"))!;

Console.WriteLine($"Recordados: {cargados.Count}");
Console.WriteLine(string.Join(", ", cargados.Select(m => m.Nombre)));

record Musico(string Nombre, string Instrumento);
```

#### Al superarla
Cuarta vela. El apagavelas del Liche se derrite como si fuera de cera.

#### Imagen
- Un liche de caricatura alto y flaco, con túnica larga y cerrada de páginas en blanco, mirando cómo su apagavelas de bronce se derrite, frente a cuatro velas encendidas en un sótano de piedra, sin letras.
- Clave señala las velas con la batuta; Ceci sostiene un pergamino liso enrollado.

### Micro-misión R04-N07-P5 · El Archivo recuerda

```meta
lugar: El Archivo Mudo
personajes: Ceci, Clave, Bemol, Gheco
criatura: dragon
carta: Jefe | un error por vez · CS1061: un nombre mal escrito · FileNotFoundException: File.Exists · y guardar después de cambiar
recompensa: xp 30, oro 30, monedas 3
item: Compás Perdido
```

#### Escena
La última vela es la memoria del Conservatorio: cada noche anota la obra tocada y recuerda las de antes. El Liche le dejó tres errores. Si la memoria funciona, el Archivo vuelve a hablar.

#### Gheco sugiere
De a uno:

1. Ensayá y leé el primer error: `CS1061` quiere decir que un dato **no existe** con ese nombre. Mirá cómo se llama de verdad en el `record`.
2. Después, al correr, explota con `FileNotFoundException`: la primera noche todavía no hay memoria guardada. Cargala **solo si** `File.Exists`.
3. Por último, corre pero no recuerda: la segunda noche no sabe nada de la primera. ¿Se guarda la memoria después de agregar la obra?

#### Desafío
Arreglá los tres errores para que cada noche recuerde las anteriores.

#### Código inicial
```csharp
using System.Text.Json;

string[] noches = { "Canon", "Bolero" };
foreach (string obra in noches)
{
    Memoria m = new Memoria(new List<string>());
    m = JsonSerializer.Deserialize<Memoria>(File.ReadAllText("memoria.json"))!;

    m.Obra.Add(obra);
    Console.WriteLine($"Noche {m.Obras.Count}: {string.Join(", ", m.Obras)}");
}

record Memoria(List<string> Obras);
```

#### Salida esperada
```
Noche 1: Canon
Noche 2: Canon, Bolero
```

#### Solución
```csharp
using System.Text.Json;

string[] noches = { "Canon", "Bolero" };
foreach (string obra in noches)
{
    Memoria m = new Memoria(new List<string>());
    if (File.Exists("memoria.json"))
    {
        m = JsonSerializer.Deserialize<Memoria>(File.ReadAllText("memoria.json"))!;
    }

    m.Obras.Add(obra);
    File.WriteAllText("memoria.json", JsonSerializer.Serialize(m));
    Console.WriteLine($"Noche {m.Obras.Count}: {string.Join(", ", m.Obras)}");
}

record Memoria(List<string> Obras);
```

#### Al superarla
La quinta vela se enciende y el Archivo entero se ilumina. Las páginas de la túnica del Liche se llenan de renglones, se despegan y vuelan a sus cajones, una por una. Donde estaba el Liche queda solo un papel dorado, doblado en cuatro: un **compás perdido** de la melodía del Vidriero.

—Lo tenía guardado bajo llave —dice {mentor}—. Lo único que nunca se animó a borrar.

#### Imagen
- Un sótano de piedra iluminado por cinco velas encendidas, con páginas en blanco que vuelan ordenadas hacia sus cajones, y en el centro un papel dorado brillante doblado en cuatro flotando, sin letras.
- Clave toma el papel dorado; Ceci, Bemol y Gheco miran asombrados.

### Encargo R04-N07-E1 · El ranking del Gremio

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

El Gremio guarda el ranking de su torneo. Escribí un programa que lea jugadores como `nombre,puntos`, uno por línea, hasta una línea vacía. Si los puntos no son un número, contala como inválida (con `try` y `catch`) y seguí. Guardá los jugadores válidos en `ranking.json` con `JsonSerializer`, leelos de vuelta del archivo y mostralos ordenados de mayor a menor, numerados. Al final, las inválidas.

Con esta entrada:

```
Ceci,25
Tomi,x
Bemol,30

```

se muestra:

```
1. Bemol 30
2. Ceci 25
Inválidas: 1
```

#### Criterio de aprobación

- Atrapa la `FormatException` y sigue con el siguiente jugador.
- Guarda y carga la lista en JSON; el ranking sale de la lista cargada.

#### Entrada de ejemplo

```
Ceci,25
Tomi,x
Bemol,30

```

#### Salida esperada

```
1. Bemol 30
2. Ceci 25
Inválidas: 1
```

#### Solución de referencia

```csharp
using System.Text.Json;

List<Jugador> jugadores = new List<Jugador>();
int invalidas = 0;
string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    string[] partes = linea.Split(',');
    try
    {
        jugadores.Add(new Jugador(partes[0], int.Parse(partes[1])));
    }
    catch (FormatException)
    {
        invalidas++;
    }
    linea = Console.ReadLine();
}

File.WriteAllText("ranking.json", JsonSerializer.Serialize(jugadores));
List<Jugador> cargados = JsonSerializer.Deserialize<List<Jugador>>(File.ReadAllText("ranking.json"))!;

int puesto = 1;
foreach (Jugador j in cargados.OrderByDescending(j => j.Puntos))
{
    Console.WriteLine($"{puesto}. {j.Nombre} {j.Puntos}");
    puesto++;
}
Console.WriteLine($"Inválidas: {invalidas}");

record Jugador(string Nombre, int Puntos);
```
