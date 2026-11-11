# RAMA R03 · El Archivo y la batuta: colecciones y funciones

```meta
tipo: tronco
posicion: 3
```

## R03-N01 · List: el atril que crece

```meta
tipo: tema
padre: R02-N11
precio: 10
criatura: orco
temas: col.listas, poo.genericos
usa: col.arrays, prog.bucles
```

### Crónica

Detrás de la Sala de Ensayo hay una escalera de caracol que baja al **Archivo**: miles de partituras en cajones, estantes y carpetas. {mentor} le da a Ceci una tarea que parece simple: anotar los músicos de la orquesta de la noche.

Ceci arma un arreglo de cinco lugares. Llegan seis músicos. Después, uno se va. —Un arreglo tiene un largo fijo —dice {mentor}—. Una orquesta, no. Para eso está la **lista**: un atril que crece y se achica solo.

### Objetivos

- Crear una `List<T>` y agregarle elementos con `Add`.
- Recorrerla, contar con `Count` y usar posiciones como en un arreglo.
- Insertar, sacar y buscar con `Insert`, `Remove`, `RemoveAt` y `Contains`.
- Ordenarla con `Sort`.

### Antes de empezar

- Los arreglos (R01-N11) y las clases (Acto II).

### Explicación

#### Una lista

```csharp
List<string> orquesta = new List<string>();
orquesta.Add("Ceci");
orquesta.Add("Bemol");
```

`<string>` dice **qué tipo guarda**. Una `List<string>` solo acepta textos; una `List<int>`, solo enteros.

También se puede crear con datos adentro:

```csharp
List<string> orquesta = new List<string> { "Ceci", "Bemol" };
List<int> notas = [8, 7, 10];          // forma corta
```

#### Como un arreglo, pero que crece

```csharp
Console.WriteLine(orquesta[0]);     // Ceci
Console.WriteLine(orquesta.Count);  // 2 (en los arreglos era Length)
foreach (string m in orquesta) Console.WriteLine(m);
```

#### Agregar, sacar, buscar

| Método | Qué hace |
|---|---|
| `Add(x)` | agrega al final |
| `Insert(i, x)` | agrega en la posición `i` |
| `Remove(x)` | saca el primero que sea igual a `x` |
| `RemoveAt(i)` | saca el de la posición `i` |
| `Contains(x)` | `true` si está |
| `IndexOf(x)` | su posición, o `-1` si no está |
| `Sort()` | ordena de menor a mayor (o alfabético) |

### Código de ejemplo

```csharp
List<string> orquesta = new List<string> { "Ceci", "Bemol" };
orquesta.Add("Clave");
orquesta.Insert(0, "Don Cedro");
orquesta.Remove("Bemol");

Console.WriteLine($"Son {orquesta.Count}");
Console.WriteLine($"¿Está Ceci? {orquesta.Contains("Ceci")}");
orquesta.Sort();
foreach (string m in orquesta)
{
    Console.WriteLine(m);
}
```

### Salida esperada

```
Son 3
¿Está Ceci? True
Ceci
Clave
Don Cedro
```

### ¿Para qué sirve?

Es la colección que más vas a usar: los jugadores conectados, los productos del carrito, los mensajes de un chat. Casi nunca sabés de antemano cuántos van a ser.

### Errores habituales

- **Pedir una posición que no existe:** con 3 elementos, `orquesta[3]` explota. El **orco** de `ArgumentOutOfRangeException` vive al final de la lista.
- **Usar `Length`:** en las listas es `Count`.
- **Guardar otro tipo:** en una `List<int>` no entra un texto (`CS1503`).

### Micro-misión R03-N01-P1 · La lista de la noche

```meta
lugar: El Archivo
personajes: Ceci, Clave
carta: List | List<string> l = new List<string>(); · l.Add("x"); · crece sola
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Clave le pide a Ceci que anote quién toca esta noche. La lista empieza vacía.

#### Gheco sugiere
Una lista se crea vacía y se le agregan cosas con `Add`, una por una:

```csharp
List<string> frutas = new List<string>();
frutas.Add("pera");
frutas.Add("uva");
Console.WriteLine(frutas.Count);   // 2
```

#### Desafío
Agregá a la lista `Ceci`, `Bemol` y `Clave`, en ese orden.

#### Código inicial
```csharp
List<string> orquesta = new List<string>();

// agregá los tres


foreach (string m in orquesta)
{
    Console.WriteLine(m);
}
Console.WriteLine($"Total: {orquesta.Count}");
```

#### Salida esperada
```
Ceci
Bemol
Clave
Total: 3
```

#### Solución
```csharp
List<string> orquesta = new List<string>();

orquesta.Add("Ceci");
orquesta.Add("Bemol");
orquesta.Add("Clave");

foreach (string m in orquesta)
{
    Console.WriteLine(m);
}
Console.WriteLine($"Total: {orquesta.Count}");
```

#### Al superarla
—Tres —dice Clave—. Y si llega un cuarto, la lista se estira. No hay que rehacer nada.

#### Imagen
- Una sala de archivo subterránea de piedra con estantes altísimos llenos de carpetas de partituras y cajones, iluminada con faroles, sin letras.
- Clave dicta con la batuta en la mano; Ceci anota en una libreta de tapas lisas.

### Micro-misión R03-N01-P2 · El que llega tarde

```meta
lugar: El Archivo
personajes: Ceci, Bemol
carta: Insert | l.Insert(0, "x"); · agrega en esa posición · los demás se corren
recompensa: xp 15, oro 15
```

#### Escena
Bemol llega tarde, como siempre, pero es el que abre el concierto con el tambor: tiene que ir **primero** en la lista.

#### Gheco sugiere
`Insert` agrega en una posición; los que estaban se corren un lugar:

```csharp
List<string> fila = new List<string> { "Ana", "Luis" };
fila.Insert(0, "Sol");      // Sol, Ana, Luis
```

#### Desafío
Insertá a `Bemol` en la posición `0`.

#### Código inicial
```csharp
List<string> orquesta = new List<string> { "Ceci", "Clave" };

// Bemol primero


Console.WriteLine(string.Join(", ", orquesta));
```

#### Salida esperada
```
Bemol, Ceci, Clave
```

#### Solución
```csharp
List<string> orquesta = new List<string> { "Ceci", "Clave" };

orquesta.Insert(0, "Bemol");

Console.WriteLine(string.Join(", ", orquesta));
```

#### Al superarla
Bemol se acomoda al principio de la fila, sin aliento, con el tambor rebotándole en la panza.

#### Imagen
- Una escalera de caracol de piedra que baja a un archivo con faroles, de noche, sin letras.
- Bemol baja corriendo con el tambor rebotando; Ceci lo espera abajo, riéndose.

### Micro-misión R03-N01-P3 · El que se va

```meta
lugar: El Archivo
personajes: Ceci, Clave
carta: Remove | l.Remove("x"); saca por valor · l.RemoveAt(i); saca por posición
recompensa: xp 15, oro 15
```

#### Escena
Un flautista avisa que está resfriado y no viene. Hay que sacarlo de la lista.

#### Gheco sugiere
`Remove` saca un elemento por su **valor**. `RemoveAt` lo saca por su **posición**:

```csharp
List<string> fila = new List<string> { "Ana", "Luis", "Sol" };
fila.Remove("Luis");    // Ana, Sol
fila.RemoveAt(0);       // Sol
```

#### Desafío
Sacá a `Flautista` de la lista con `Remove`.

#### Código inicial
```csharp
List<string> orquesta = new List<string> { "Ceci", "Flautista", "Bemol" };

// sacalo


Console.WriteLine(string.Join(", ", orquesta));
Console.WriteLine($"Quedan {orquesta.Count}");
```

#### Salida esperada
```
Ceci, Bemol
Quedan 2
```

#### Solución
```csharp
List<string> orquesta = new List<string> { "Ceci", "Flautista", "Bemol" };

orquesta.Remove("Flautista");

Console.WriteLine(string.Join(", ", orquesta));
Console.WriteLine($"Quedan {orquesta.Count}");
```

#### Al superarla
—Que se mejore —dice Clave, y tacha el atril vacío con la mirada.

#### Imagen
- Una fila de atriles de madera en un archivo de piedra, con uno vacío en el medio y una flauta guardada en su estuche, sin letras.
- Clave mira el atril vacío; Ceci ordena las partituras de los demás.

### Micro-misión R03-N01-P4 · ¿Está o no está?

```meta
lugar: El Archivo
personajes: Ceci, Bemol
carta: Contains y Sort | l.Contains("x") → true o false · l.Sort(); ordena
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol no se acuerda si anotó a Don Cedro. Y después, Clave quiere la lista en orden alfabético.

#### Gheco sugiere
`Contains` dice si está. `Sort` ordena la lista (los textos, alfabéticamente):

```csharp
List<string> fila = new List<string> { "Sol", "Ana" };
Console.WriteLine(fila.Contains("Ana"));   // True
fila.Sort();                                // Ana, Sol
```

#### Desafío
Mostrá si `Don Cedro` está en la lista y después ordenala antes de mostrarla.

#### Código inicial
```csharp
List<string> orquesta = new List<string> { "Clave", "Bemol", "Ceci" };

Console.WriteLine($"¿Está Don Cedro? {false}");
// ordenala

Console.WriteLine(string.Join(", ", orquesta));
```

#### Salida esperada
```
¿Está Don Cedro? False
Bemol, Ceci, Clave
```

#### Solución
```csharp
List<string> orquesta = new List<string> { "Clave", "Bemol", "Ceci" };

Console.WriteLine($"¿Está Don Cedro? {orquesta.Contains("Don Cedro")}");
orquesta.Sort();

Console.WriteLine(string.Join(", ", orquesta));
```

#### Al superarla
—No está —dice Bemol—. Mejor, él no toca: arregla lo que rompemos.

#### Imagen
- Un estante de archivo con carpetas de partituras de lomos de colores ordenadas de a una, sin letras.
- Bemol pasa el dedo por los lomos buscando; Ceci sostiene una carpeta abierta de espaldas a nosotros.

### Micro-misión R03-N01-P5 · El orco del último atril

```meta
lugar: El Archivo
personajes: Ceci, Gheco
criatura: orco
carta: Orco | ArgumentOutOfRangeException · con Count 3, las posiciones van de 0 a 2 · el último es Count - 1
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un orco pidió el músico de la posición `3` en una lista de tres. El programa explota en la puerta del Archivo.

#### Gheco sugiere
Las posiciones empiezan en `0`. Con `Count` elementos, el último está en `Count - 1`:

```
Unhandled exception. System.ArgumentOutOfRangeException: Index was out of range.
```

#### Desafío
Ensayá, mirá cómo explota y arreglá la línea para mostrar el **último** de la lista, sea cual sea su largo.

#### Código inicial
```csharp
List<string> orquesta = new List<string> { "Ceci", "Bemol", "Clave" };
Console.WriteLine($"Cierra: {orquesta[orquesta.Count]}");
```

#### Salida esperada
```
Cierra: Clave
```

#### Solución
```csharp
List<string> orquesta = new List<string> { "Ceci", "Bemol", "Clave" };
Console.WriteLine($"Cierra: {orquesta[orquesta.Count - 1]}");
```

#### Al superarla
El orco busca el cuarto atril, se choca contra la pared del fondo y se va sobándose la frente.

#### Imagen
- Un orco grandote de caricatura sobándose la frente frente a una pared de piedra al final de una fila de tres atriles, en un archivo con faroles.
- Gheco, sobre el último atril, lo mira con las antiparras puestas.

### Encargo R03-N01-E1 · La lista de compras de Doña Mirta

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Doña Mirta anota lo que le falta para el puesto. Escribí un programa que lea productos, uno por línea, hasta una línea vacía, y los guarde en una `List<string>` **sin repetir** (si ya está, no lo agrega). Al final mostrá cuántos son y la lista ordenada, uno por línea.

Con esta entrada:

```
miel
harina
miel
leche

```

se muestra:

```
Productos: 3
harina
leche
miel
```

#### Criterio de aprobación

- Usa una `List<string>` con `Add`, `Contains` y `Sort`.
- Deja de leer con la línea vacía.

#### Entrada de ejemplo

```
miel
harina
miel
leche

```

#### Salida esperada

```
Productos: 3
harina
leche
miel
```

#### Solución de referencia

```csharp
List<string> compras = new List<string>();
string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    if (!compras.Contains(linea)) compras.Add(linea);
    linea = Console.ReadLine();
}
compras.Sort();
Console.WriteLine($"Productos: {compras.Count}");
foreach (string p in compras)
{
    Console.WriteLine(p);
}
```

## R03-N02 · Dictionary: buscar por nombre

```meta
tipo: tema
padre: R03-N01
precio: 10
criatura: orco
temas: col.mapas
usa: col.listas, prog.condicionales
```

### Crónica

En el Archivo, cada partitura tiene un **código** en el lomo. Clave nunca recorre los estantes uno por uno: dice el código y va directo al cajón. —Si tuviera que mirar mil carpetas cada vez —dice—, todavía estaría buscando la de ayer.

—Eso es un **diccionario** —explica {mentor}—: guarda pares **clave → valor**. Le das la clave, te devuelve el valor. Al instante, aunque tenga un millón.

### Objetivos

- Crear un `Dictionary<K, V>` y agregarle pares.
- Leer un valor por su clave y cambiarlo.
- Preguntar con `ContainsKey` y leer seguro con `TryGetValue`.
- Recorrerlo y usarlo para contar.

### Antes de empezar

- Las listas (R03-N01) y `out` (R01-N14).

### Explicación

#### Pares clave → valor

```csharp
Dictionary<string, int> compases = new Dictionary<string, int>();
compases["Vals"] = 48;          // agrega (o reemplaza si ya estaba)
compases["Marcha"] = 32;
Console.WriteLine(compases["Vals"]);   // 48
```

`<string, int>`: la clave es un texto y el valor, un entero. Las claves **no se repiten**.

También se puede crear con datos:

```csharp
var compases = new Dictionary<string, int> { ["Vals"] = 48, ["Marcha"] = 32 };
```

#### Leer sin explotar

Si pedís una clave que no está, el programa explota. Dos formas seguras:

```csharp
if (compases.ContainsKey("Tango")) { ... }

if (compases.TryGetValue("Tango", out int c))
{
    Console.WriteLine(c);
}
```

#### Recorrer

```csharp
foreach (var (obra, n) in compases)
{
    Console.WriteLine($"{obra}: {n}");
}
```

Un diccionario no promete ningún orden en particular.

#### Contar con un diccionario

```csharp
cuenta[nota] = cuenta.GetValueOrDefault(nota) + 1;
```

Si la nota todavía no estaba, `GetValueOrDefault` da `0`, y empieza a contar.

### Código de ejemplo

```csharp
var compases = new Dictionary<string, int> { ["Vals"] = 48, ["Marcha"] = 32 };
compases["Nocturno"] = 40;
compases["Vals"] = 50;

Console.WriteLine($"Vals: {compases["Vals"]}");
Console.WriteLine($"¿Hay tango? {compases.ContainsKey("Tango")}");
if (compases.TryGetValue("Marcha", out int m))
{
    Console.WriteLine($"Marcha: {m}");
}

var cuenta = new Dictionary<string, int>();
foreach (string nota in new[] { "La", "Mi", "La" })
{
    cuenta[nota] = cuenta.GetValueOrDefault(nota) + 1;
}
Console.WriteLine($"La aparece {cuenta["La"]} veces");
```

### Salida esperada

```
Vals: 50
¿Hay tango? False
Marcha: 32
La aparece 2 veces
```

### ¿Para qué sirve?

Los precios de una tienda por producto, los teléfonos por nombre, los puntos por jugador, las traducciones por palabra: cada vez que buscás algo **por su nombre**, va un diccionario.

### Errores habituales

- **Pedir una clave que no existe:** el **orco** de `KeyNotFoundException`. Preguntá antes o usá `TryGetValue`.
- **`Add` con una clave repetida:** `compases.Add("Vals", 1)` explota si ya estaba. Con `compases["Vals"] = 1` se reemplaza.
- **Esperar un orden:** si necesitás ordenado, ordená al mostrar.

### Micro-misión R03-N02-P1 · El cajón de cada obra

```meta
lugar: El Archivo
personajes: Ceci, Clave
carta: Dictionary | var d = new Dictionary<string, int>(); · d["clave"] = valor; · d["clave"] lo lee
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Clave le dicta a Ceci en qué cajón está cada obra: el Vals en el `12`, la Marcha en el `7`.

#### Gheco sugiere
Con los corchetes se guarda y se lee por clave:

```csharp
var edades = new Dictionary<string, int>();
edades["Ana"] = 12;
Console.WriteLine(edades["Ana"]);   // 12
```

#### Desafío
Guardá en el diccionario que el `Vals` está en el cajón `12` y la `Marcha` en el `7`.

#### Código inicial
```csharp
var cajones = new Dictionary<string, int>();

// guardá los dos


Console.WriteLine($"Vals: cajón {cajones["Vals"]}");
Console.WriteLine($"Marcha: cajón {cajones["Marcha"]}");
```

#### Salida esperada
```
Vals: cajón 12
Marcha: cajón 7
```

#### Solución
```csharp
var cajones = new Dictionary<string, int>();

cajones["Vals"] = 12;
cajones["Marcha"] = 7;

Console.WriteLine($"Vals: cajón {cajones["Vals"]}");
Console.WriteLine($"Marcha: cajón {cajones["Marcha"]}");
```

#### Al superarla
Ceci abre el cajón doce y ahí está el Vals, esperándola. —Sin buscar —dice, admirada.

#### Imagen
- Una pared de cajones de madera numerados solo con chapitas lisas de bronce, sin números, en un archivo de piedra con faroles; uno está abierto con una partitura enrollada adentro.
- Ceci saca la partitura del cajón abierto; Clave asiente detrás.

### Micro-misión R03-N02-P2 · Cambió de cajón

```meta
lugar: El Archivo
personajes: Ceci, Bemol
carta: Reemplazar | d["clave"] = nuevo; · si ya estaba, lo reemplaza · las claves no se repiten
recompensa: xp 15, oro 15
```

#### Escena
Bemol movió la Marcha al cajón `9` porque el `7` tenía humedad. Hay que actualizar el diccionario.

#### Gheco sugiere
Asignar a una clave que ya existe **reemplaza** el valor viejo:

```csharp
edades["Ana"] = 13;   // ahora 13, no 12
```

#### Desafío
Cambiá el cajón de la `Marcha` a `9`.

#### Código inicial
```csharp
var cajones = new Dictionary<string, int> { ["Vals"] = 12, ["Marcha"] = 7 };

// la Marcha ahora está en el 9


Console.WriteLine($"Marcha: cajón {cajones["Marcha"]}");
Console.WriteLine($"Obras: {cajones.Count}");
```

#### Salida esperada
```
Marcha: cajón 9
Obras: 2
```

#### Solución
```csharp
var cajones = new Dictionary<string, int> { ["Vals"] = 12, ["Marcha"] = 7 };

cajones["Marcha"] = 9;

Console.WriteLine($"Marcha: cajón {cajones["Marcha"]}");
Console.WriteLine($"Obras: {cajones.Count}");
```

#### Al superarla
—Siguen siendo dos obras —dice Bemol—. Solo cambió dónde está una.

#### Imagen
- Un cajón de madera con manchas de humedad y otro seco al lado, con una partitura enrollada pasando de uno a otro, en un archivo de piedra, sin letras.
- Bemol carga la partitura con cuidado; Ceci le sostiene el cajón nuevo.

### Micro-misión R03-N02-P3 · ¿Está esa obra?

```meta
lugar: El Archivo
personajes: Ceci, Clave
carta: TryGetValue | if (d.TryGetValue("x", out int v)) { … } · no explota si no está
recompensa: xp 15, oro 15
```

#### Escena
Un músico pide un Tango. Nadie sabe si está en el Archivo, y Ceci no quiere que el programa explote si no está.

#### Gheco sugiere
`TryGetValue` devuelve `true` si encontró la clave, y deja el valor en la variable del `out`:

```csharp
if (edades.TryGetValue("Luis", out int e))
{
    Console.WriteLine(e);
}
else
{
    Console.WriteLine("no está");
}
```

#### Desafío
Completá `Buscar` con `TryGetValue`: si está, mostrá `<obra>: cajón <n>`; si no, `<obra>: no está`.

#### Código inicial
```csharp
var cajones = new Dictionary<string, int> { ["Vals"] = 12, ["Marcha"] = 9 };
Buscar(cajones, "Vals");
Buscar(cajones, "Tango");

static void Buscar(Dictionary<string, int> cajones, string obra)
{
    Console.WriteLine($"{obra}: cajón {cajones[obra]}");
}
```

#### Salida esperada
```
Vals: cajón 12
Tango: no está
```

#### Solución
```csharp
var cajones = new Dictionary<string, int> { ["Vals"] = 12, ["Marcha"] = 9 };
Buscar(cajones, "Vals");
Buscar(cajones, "Tango");

static void Buscar(Dictionary<string, int> cajones, string obra)
{
    if (cajones.TryGetValue(obra, out int n))
    {
        Console.WriteLine($"{obra}: cajón {n}");
    }
    else
    {
        Console.WriteLine($"{obra}: no está");
    }
}
```

#### Al superarla
—No hay tango —dice Clave—. Pero el programa sigue de pie. Eso es lo importante.

#### Imagen
- Una pared de cajones de archivo de madera, todos cerrados, con un farol iluminando una fila, sin letras ni números.
- Clave recorre la pared con la mirada; Ceci espera con una libreta cerrada.

### Micro-misión R03-N02-P4 · Contar las notas

```meta
lugar: El Archivo
personajes: Ceci, Bemol
carta: Contar | d[x] = d.GetValueOrDefault(x) + 1; · la primera vez cuenta desde 0
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol quiere saber cuántas veces aparece cada nota en una melodía. —Si llevo la cuenta a mano —dice—, me pierdo en la tercera.

#### Gheco sugiere
Para contar, sumá uno al valor de esa clave. `GetValueOrDefault` da `0` si todavía no estaba:

```csharp
var votos = new Dictionary<string, int>();
foreach (string v in new[] { "sí", "no", "sí" })
{
    votos[v] = votos.GetValueOrDefault(v) + 1;
}
// sí: 2, no: 1
```

#### Desafío
Completá el bucle para contar cada nota. El programa después muestra las cuentas.

#### Código inicial
```csharp
string[] melodia = { "Do", "Mi", "Do", "Sol", "Do", "Mi" };
var cuenta = new Dictionary<string, int>();

foreach (string nota in melodia)
{
    // contá
}

Console.WriteLine($"Do: {cuenta.GetValueOrDefault("Do")}");
Console.WriteLine($"Mi: {cuenta.GetValueOrDefault("Mi")}");
Console.WriteLine($"Sol: {cuenta.GetValueOrDefault("Sol")}");
```

#### Salida esperada
```
Do: 3
Mi: 2
Sol: 1
```

#### Solución
```csharp
string[] melodia = { "Do", "Mi", "Do", "Sol", "Do", "Mi" };
var cuenta = new Dictionary<string, int>();

foreach (string nota in melodia)
{
    cuenta[nota] = cuenta.GetValueOrDefault(nota) + 1;
}

Console.WriteLine($"Do: {cuenta.GetValueOrDefault("Do")}");
Console.WriteLine($"Mi: {cuenta.GetValueOrDefault("Mi")}");
Console.WriteLine($"Sol: {cuenta.GetValueOrDefault("Sol")}");
```

#### Al superarla
—Tres Do —dice Bemol—. Con razón me sonaba tan Do.

#### Imagen
- Tres montoncitos de notas musicales doradas sobre una mesa de archivo, uno alto, uno mediano y uno chico, sin letras.
- Bemol los mide con los palillos del tambor; Ceci se ríe.

### Micro-misión R03-N02-P5 · El orco de la clave perdida

```meta
lugar: El Archivo
personajes: Ceci, Gheco
criatura: orco
carta: Orco | KeyNotFoundException · la clave no está · ContainsKey o TryGetValue antes
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
El orco pidió el precio de la «Polka» y el programa explotó: esa obra no está en el diccionario.

#### Gheco sugiere
Pedir una clave que no existe tira:

```
Unhandled exception. System.Collections.Generic.KeyNotFoundException: The given key 'Polka' was not present in the dictionary.
```

`GetValueOrDefault` devuelve un valor por defecto si no está: `precios.GetValueOrDefault("Polka", 0)`.

#### Desafío
Ensayá, mirá cómo explota y arreglá la línea para que, si no está, el precio sea `0`.

#### Código inicial
```csharp
var precios = new Dictionary<string, int> { ["Vals"] = 300, ["Marcha"] = 250 };
int p = precios["Polka"];
Console.WriteLine($"Polka: {p}");
```

#### Salida esperada
```
Polka: 0
```

#### Solución
```csharp
var precios = new Dictionary<string, int> { ["Vals"] = 300, ["Marcha"] = 250 };
int p = precios.GetValueOrDefault("Polka", 0);
Console.WriteLine($"Polka: {p}");
```

#### Al superarla
El orco abre todos los cajones buscando la Polka, no la encuentra y se va a bailar solo al patio.

#### Imagen
- Un orco grandote de caricatura rodeado de cajones de archivo abiertos y vacíos, rascándose la cabeza, en un archivo de piedra con faroles.
- Gheco, sobre un cajón, sostiene una partitura enrollada que no es la que el orco busca.

### Encargo R03-N02-E1 · La agenda del Puerto

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Nilo guarda en qué muelle atraca cada barco. Escribí un programa que lea órdenes, una por línea, hasta `fin`:

- `poner <barco> <muelle>`: guarda (o cambia) el muelle de ese barco.
- `ver <barco>`: muestra `<barco>: muelle <n>` o `<barco>: no está`.
- `sacar <barco>`: lo saca del diccionario.

Usá un `Dictionary<string, int>` y `Split(' ')` para separar la orden.

Con esta entrada:

```
poner Gaviota 3
poner Delfin 5
ver Gaviota
poner Gaviota 4
ver Gaviota
sacar Delfin
ver Delfin
fin
```

se muestra:

```
Gaviota: muelle 3
Gaviota: muelle 4
Delfin: no está
```

#### Criterio de aprobación

- Usa un `Dictionary` para guardar los muelles.
- `ver` no explota si el barco no está.

#### Entrada de ejemplo

```
poner Gaviota 3
poner Delfin 5
ver Gaviota
poner Gaviota 4
ver Gaviota
sacar Delfin
ver Delfin
fin
```

#### Salida esperada

```
Gaviota: muelle 3
Gaviota: muelle 4
Delfin: no está
```

#### Solución de referencia

```csharp
var muelles = new Dictionary<string, int>();
string? linea = Console.ReadLine();
while (linea is not null && linea != "fin")
{
    string[] partes = linea.Split(' ');
    switch (partes[0])
    {
        case "poner":
            muelles[partes[1]] = int.Parse(partes[2]);
            break;
        case "ver":
            if (muelles.TryGetValue(partes[1], out int m))
            {
                Console.WriteLine($"{partes[1]}: muelle {m}");
            }
            else
            {
                Console.WriteLine($"{partes[1]}: no está");
            }
            break;
        case "sacar":
            muelles.Remove(partes[1]);
            break;
    }
    linea = Console.ReadLine();
}
```

## R03-N03 · HashSet, Queue y Stack: tres formas de guardar

```meta
tipo: tema
padre: R03-N02
precio: 10
criatura: troll
temas: col.conjuntos, col.pilas-colas
usa: col.listas
```

### Crónica

El Archivo tiene tres rincones raros. En uno hay una **caja de sellos**: cada sello está una sola vez, nunca dos iguales. En otro, una **fila** de músicos esperando para ensayar: el primero que llega es el primero que entra. Y en el tercero, una **pila** de partituras: la última que se apoyó arriba es la primera que se saca.

—Tres formas de guardar —dice {mentor}—, cada una para un trabajo distinto. Elegir bien la caja es la mitad del programa.

### Objetivos

- Usar un `HashSet<T>` para guardar sin repetidos.
- Usar una `Queue<T>` (cola): el primero que entra, sale primero.
- Usar una `Stack<T>` (pila): el último que entra, sale primero.

### Antes de empezar

- Listas y diccionarios (R03-N01 y R03-N02).

### Explicación

#### `HashSet<T>`: sin repetidos

```csharp
HashSet<string> sellos = new HashSet<string>();
sellos.Add("Sol");       // true: entró
sellos.Add("Sol");       // false: ya estaba
Console.WriteLine(sellos.Count);           // 1
Console.WriteLine(sellos.Contains("Sol")); // True, al instante
```

`Add` devuelve `bool`: te dice si entró o si ya estaba.

#### `Queue<T>`: la fila

```csharp
Queue<string> fila = new Queue<string>();
fila.Enqueue("Ceci");      // se pone en la fila
fila.Enqueue("Bemol");
string primero = fila.Dequeue();   // sale Ceci
string mira = fila.Peek();         // mira el siguiente sin sacarlo: Bemol
```

#### `Stack<T>`: la pila

```csharp
Stack<string> pila = new Stack<string>();
pila.Push("Vals");         // se apoya arriba
pila.Push("Marcha");
string arriba = pila.Pop();        // sale Marcha, la última
```

| Colección | Entra | Sale | Para qué |
|---|---|---|---|
| `HashSet` | `Add` | `Remove` | «¿está?» y sin repetidos |
| `Queue` | `Enqueue` | `Dequeue` | turnos, el primero primero |
| `Stack` | `Push` | `Pop` | deshacer, lo último primero |

### Código de ejemplo

```csharp
HashSet<string> sellos = new HashSet<string>();
Console.WriteLine(sellos.Add("Sol"));
Console.WriteLine(sellos.Add("Sol"));

Queue<string> fila = new Queue<string>();
fila.Enqueue("Ceci");
fila.Enqueue("Bemol");
Console.WriteLine($"Entra: {fila.Dequeue()}");

Stack<string> pila = new Stack<string>();
pila.Push("Vals");
pila.Push("Marcha");
Console.WriteLine($"Arriba: {pila.Pop()}");
Console.WriteLine($"Quedan: {fila.Count} en la fila, {pila.Count} en la pila");
```

### Salida esperada

```
True
False
Entra: Ceci
Arriba: Marcha
Quedan: 1 en la fila, 1 en la pila
```

### ¿Para qué sirve?

`HashSet`: los usuarios que ya votaron, las palabras distintas de un texto. `Queue`: los pedidos de una cocina, los turnos de una guardia. `Stack`: el botón «deshacer» de cualquier editor, o revisar que los paréntesis estén bien cerrados.

### Errores habituales

- **Sacar de una fila o una pila vacía:** `Dequeue` y `Pop` explotan si no hay nada (`InvalidOperationException`). Mirá `Count` antes.
- **Usar una lista para «¿está?» con miles de datos:** funciona, pero lenta. El `HashSet` responde al instante.
- **Cambiar una colección mientras la recorrés:** el **troll** de `Collection was modified` aparece si sacás elementos dentro de un `foreach` de la misma colección.

### Micro-misión R03-N03-P1 · La caja de sellos

```meta
lugar: El Archivo
personajes: Ceci, Clave
carta: HashSet | var s = new HashSet<string>(); · s.Add(x) devuelve false si ya estaba · sin repetidos
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Cada partitura del Archivo lleva un sello con la clave de su tono. Clave quiere saber cuántos tonos distintos hay, sin contar repetidos.

#### Gheco sugiere
Un `HashSet` no guarda repetidos: si agregás algo que ya está, lo ignora.

```csharp
var colores = new HashSet<string> { "rojo" };
colores.Add("rojo");
colores.Add("azul");
Console.WriteLine(colores.Count);   // 2
```

#### Desafío
Recorré los sellos y agregalos al `HashSet`. El programa muestra cuántos distintos hay.

#### Código inicial
```csharp
string[] sellos = { "Sol", "Re", "Sol", "La", "Re", "Sol" };
var distintos = new HashSet<string>();

// agregalos


Console.WriteLine($"Tonos distintos: {distintos.Count}");
```

#### Salida esperada
```
Tonos distintos: 3
```

#### Solución
```csharp
string[] sellos = { "Sol", "Re", "Sol", "La", "Re", "Sol" };
var distintos = new HashSet<string>();

foreach (string s in sellos)
{
    distintos.Add(s);
}

Console.WriteLine($"Tonos distintos: {distintos.Count}");
```

#### Al superarla
—Tres tonos —dice Clave—. Seis sellos, pero tres tonos. No confundas cuántos hay con cuántos distintos.

#### Imagen
- Una caja de madera abierta con sellos de lacre de tres colores distintos, algunos repetidos, sobre una mesa de archivo, sin letras.
- Clave separa los sellos con la punta de la batuta; Ceci los cuenta.

### Micro-misión R03-N03-P2 · La fila del ensayo

```meta
lugar: El Archivo
personajes: Ceci, Bemol
carta: Queue | q.Enqueue(x) entra al final · q.Dequeue() sale el primero · el primero que llega, primero
recompensa: xp 15, oro 15
```

#### Escena
Los músicos hacen fila para ensayar el solo. Bemol lleva el orden: el primero que llegó entra primero.

#### Gheco sugiere
Una `Queue` es una fila: `Enqueue` pone al final, `Dequeue` saca al primero:

```csharp
var fila = new Queue<string>();
fila.Enqueue("Ana");
fila.Enqueue("Luis");
Console.WriteLine(fila.Dequeue());   // Ana
```

#### Desafío
Mientras la fila tenga gente (`Count > 0`), sacá al primero con `Dequeue` y mostrá `Ensaya: <nombre>`.

#### Código inicial
```csharp
var fila = new Queue<string>();
fila.Enqueue("Ceci");
fila.Enqueue("Bemol");
fila.Enqueue("Clave");

// que pasen de a uno

```

#### Salida esperada
```
Ensaya: Ceci
Ensaya: Bemol
Ensaya: Clave
```

#### Solución
```csharp
var fila = new Queue<string>();
fila.Enqueue("Ceci");
fila.Enqueue("Bemol");
fila.Enqueue("Clave");

while (fila.Count > 0)
{
    Console.WriteLine($"Ensaya: {fila.Dequeue()}");
}
```

#### Al superarla
Uno por uno, en el orden en que llegaron. Nadie se cuela: la fila es justa.

#### Imagen
- Un pasillo de piedra del archivo con una fila de sillas de madera y una puerta de ensayo entreabierta con luz cálida, sin letras.
- Bemol, con el tambor, organiza la fila; Ceci entra primera por la puerta.

### Micro-misión R03-N03-P3 · La pila de partituras

```meta
lugar: El Archivo
personajes: Ceci, Don Cedro
carta: Stack | s.Push(x) apoya arriba · s.Pop() saca la de arriba · lo último que entra, sale primero
recompensa: xp 15, oro 15
```

#### Escena
Don Cedro bajó al Archivo con una pila de partituras para encuadernar. La última que apoyó es la que está arriba.

#### Gheco sugiere
Una `Stack` es una pila: `Push` apoya arriba, `Pop` saca la de arriba:

```csharp
var platos = new Stack<string>();
platos.Push("verde");
platos.Push("rojo");
Console.WriteLine(platos.Pop());   // rojo
```

#### Desafío
Apilá las tres obras en orden (`Vals`, `Marcha`, `Nocturno`) y después sacalas todas con `Pop`, mostrando cada una.

#### Código inicial
```csharp
var pila = new Stack<string>();

// apilá y sacá

```

#### Salida esperada
```
Nocturno
Marcha
Vals
```

#### Solución
```csharp
var pila = new Stack<string>();

pila.Push("Vals");
pila.Push("Marcha");
pila.Push("Nocturno");

while (pila.Count > 0)
{
    Console.WriteLine(pila.Pop());
}
```

#### Al superarla
—Al revés de como entraron —dice Don Cedro—. Como los platos de mi cocina: el de abajo no lo uso nunca.

#### Imagen
- Una pila alta de partituras atadas sobre una mesa del archivo, con una vela al lado, sin letras.
- Don Cedro saca la de arriba con cuidado; Ceci sostiene la pila para que no se caiga.

### Micro-misión R03-N03-P4 · Los paréntesis del Gremio

```meta
lugar: El Archivo
personajes: Ceci, Bemol
carta: Stack para revisar | cada ( se apila · cada ) saca uno · si falta o sobra, está mal
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Al Archivo llegan fórmulas del Gremio con paréntesis. Bemol quiere saber si cada uno que abre tiene su cierre.

#### Gheco sugiere
Una pila sirve para emparejar: cada `(` se apila, y cada `)` saca uno. Si al cerrar no hay nada para sacar, o si al final sobra algo, está mal.

```csharp
if (c == '(') pila.Push(c);
else if (c == ')')
{
    if (pila.Count == 0) return false;
    pila.Pop();
}
```

#### Desafío
Completá `Equilibrados` con una `Stack<char>`.

#### Código inicial
```csharp
Console.WriteLine(Equilibrados("(a(b)c)"));
Console.WriteLine(Equilibrados("(a))"));
Console.WriteLine(Equilibrados("((a)"));

static bool Equilibrados(string texto)
{
    var pila = new Stack<char>();
    foreach (char c in texto)
    {
        // apilá y sacá
    }
    return true;
}
```

#### Salida esperada
```
True
False
False
```

#### Solución
```csharp
Console.WriteLine(Equilibrados("(a(b)c)"));
Console.WriteLine(Equilibrados("(a))"));
Console.WriteLine(Equilibrados("((a)"));

static bool Equilibrados(string texto)
{
    var pila = new Stack<char>();
    foreach (char c in texto)
    {
        if (c == '(') pila.Push(c);
        else if (c == ')')
        {
            if (pila.Count == 0) return false;
            pila.Pop();
        }
    }
    return pila.Count == 0;
}
```

#### Al superarla
—Así revisa el compilador tus llaves —dice Bemol, impresionado—. ¡Con una pila!

#### Imagen
- Pares de arcos de luz dorada que se abren y se cierran en el aire como paréntesis gigantes, en un archivo de piedra, sin letras.
- Bemol los cuenta con los palillos; Ceci une dos con las manos.

### Micro-misión R03-N03-P5 · El troll que borraba mientras contaba

```meta
lugar: El Archivo
personajes: Ceci, Gheco
criatura: troll
carta: Troll | Collection was modified · no saques dentro del foreach de la misma lista · RemoveAll o una copia
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un troll recorre la lista de partituras y va sacando las rotas en el mismo `foreach`. El programa explota.

#### Gheco sugiere
No se puede cambiar una colección mientras un `foreach` la recorre:

```
Unhandled exception. System.InvalidOperationException: Collection was modified; enumeration operation may not execute.
```

Una salida: recorrer una **copia** (`new List<string>(lista)`) y sacar de la original.

#### Desafío
Ensayá, mirá cómo explota y hacé que el `foreach` recorra una copia de la lista.

#### Código inicial
```csharp
var partituras = new List<string> { "Vals", "rota", "Marcha", "rota" };
foreach (string p in partituras)
{
    if (p == "rota") partituras.Remove(p);
}
Console.WriteLine(string.Join(", ", partituras));
```

#### Salida esperada
```
Vals, Marcha
```

#### Solución
```csharp
var partituras = new List<string> { "Vals", "rota", "Marcha", "rota" };
foreach (string p in new List<string>(partituras))
{
    if (p == "rota") partituras.Remove(p);
}
Console.WriteLine(string.Join(", ", partituras));
```

#### Al superarla
El troll intenta borrar mientras cuenta, se marea y se sienta en el piso. Las partituras rotas ya no están; las buenas, sí.

#### Imagen
- Un troll chiquito de piel color musgo, pelo de paja y chaleco remendado, sentado en el piso del archivo, mareado, rodeado de hojas de partitura sin letras.
- Gheco, sobre una pila de carpetas, lo mira con las antiparras puestas.

### Encargo R03-N03-E1 · La cocina de la Posada

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

En la cocina de la Posada los pedidos se atienden en el orden en que llegan, y el cocinero puede **deshacer** el último plato que sirvió si salió mal. Leé órdenes hasta `fin`:

- `pedido <plato>`: entra a la fila de pedidos (`Queue`).
- `servir`: saca el primer pedido de la fila, lo muestra como `Sirve: <plato>` y lo apila en los servidos (`Stack`). Si no hay pedidos, muestra `Nada para servir`.
- `deshacer`: saca el último servido, muestra `Vuelve: <plato>` y lo pone de nuevo al final de la fila.

Con esta entrada:

```
pedido sopa
pedido guiso
servir
deshacer
servir
servir
servir
fin
```

se muestra:

```
Sirve: sopa
Vuelve: sopa
Sirve: guiso
Sirve: sopa
Nada para servir
```

#### Criterio de aprobación

- Los pedidos van en una `Queue` y los servidos en una `Stack`.
- No explota al servir con la fila vacía.

#### Entrada de ejemplo

```
pedido sopa
pedido guiso
servir
deshacer
servir
servir
servir
fin
```

#### Salida esperada

```
Sirve: sopa
Vuelve: sopa
Sirve: guiso
Sirve: sopa
Nada para servir
```

#### Solución de referencia

```csharp
var pedidos = new Queue<string>();
var servidos = new Stack<string>();
string? linea = Console.ReadLine();
while (linea is not null && linea != "fin")
{
    string[] partes = linea.Split(' ');
    if (partes[0] == "pedido")
    {
        pedidos.Enqueue(partes[1]);
    }
    else if (partes[0] == "servir")
    {
        if (pedidos.Count == 0)
        {
            Console.WriteLine("Nada para servir");
        }
        else
        {
            string plato = pedidos.Dequeue();
            Console.WriteLine($"Sirve: {plato}");
            servidos.Push(plato);
        }
    }
    else if (partes[0] == "deshacer" && servidos.Count > 0)
    {
        string plato = servidos.Pop();
        Console.WriteLine($"Vuelve: {plato}");
        pedidos.Enqueue(plato);
    }
    linea = Console.ReadLine();
}
```

## R03-N04 · Genéricos: la caja para cualquier cosa

```meta
tipo: tema
padre: R03-N03
precio: 10
criatura: goblin
temas: poo.genericos
usa: poo.clases, poo.interfaces
```

### Crónica

Don Cedro necesita estuches. Uno para violines, otro para arcos, otro para diapasones. Empieza a dibujar tres planos y se detiene. —Son iguales —protesta—. Cambia solo lo que va adentro.

—Entonces dibujá **uno solo**, con un hueco para el tipo —dice {mentor}—. Eso es un **genérico**: `List<T>` y `Dictionary<K, V>` ya lo eran. Ahora los escribís vos.

### Objetivos

- Escribir una clase genérica `Estuche<T>`.
- Escribir un método genérico que sirva para cualquier tipo.
- Usar `where` para pedirle algo al tipo.

### Antes de empezar

- Las colecciones (R03-N01 a R03-N03) y las interfaces (R02-N09).

### Explicación

#### Una clase con un hueco para el tipo

```csharp
class Estuche<T>
{
    public T Contenido { get; }

    public Estuche(T contenido)
    {
        Contenido = contenido;
    }
}
```

```csharp
Estuche<string> e1 = new Estuche<string>("violín");
Estuche<int> e2 = new Estuche<int>(440);
```

`T` es un **parámetro de tipo**: se completa al usar la clase. El compilador revisa todo: en un `Estuche<int>` no entra un texto.

#### Un método genérico

```csharp
static T Ultimo<T>(List<T> datos)
{
    return datos[datos.Count - 1];
}
// Ultimo(new List<int> { 1, 2, 3 }) → 3: C# deduce que T es int
```

#### `where`: pedirle algo al tipo

Si `T` puede ser cualquier cosa, solo podés hacer lo que sabe hacer cualquier cosa. Para comparar, hay que pedir que `T` sepa compararse:

```csharp
static T Mayor<T>(T a, T b) where T : IComparable<T>
{
    return a.CompareTo(b) > 0 ? a : b;
}
```

`CompareTo` devuelve un número: positivo si `a` va después, negativo si va antes, `0` si son iguales. `int`, `double` y `string` ya lo saben hacer.

### Código de ejemplo

```csharp
Estuche<string> violin = new Estuche<string>("violín");
Estuche<int> la = new Estuche<int>(440);
Console.WriteLine(violin);
Console.WriteLine(la);

Console.WriteLine(Ultimo(new List<string> { "Do", "Re", "Mi" }));
Console.WriteLine(Mayor(7, 12));
Console.WriteLine(Mayor("Vals", "Marcha"));

static T Ultimo<T>(List<T> datos) => datos[datos.Count - 1];

static T Mayor<T>(T a, T b) where T : IComparable<T>
{
    return a.CompareTo(b) > 0 ? a : b;
}

class Estuche<T>
{
    public T Contenido { get; }

    public Estuche(T contenido)
    {
        Contenido = contenido;
    }

    public override string ToString() => $"Estuche con {Contenido}";
}
```

### Salida esperada

```
Estuche con violín
Estuche con 440
Mi
12
Vals
```

### ¿Para qué sirve?

Las colecciones de C# son todas genéricas. Y en tus programas, un `Resultado<T>` que devuelve un dato o un error, un `Repositorio<T>` que guarda cualquier cosa, un `Par<A, B>`: una sola clase, escrita una vez, que sirve para todo.

### Errores habituales

- **Operar con `T` sin pedirlo:** `a > b` con dos `T` no compila (`CS0019`): no todo tipo sabe compararse. Pedilo con `where T : IComparable<T>`.
- **Usar `object` en lugar de un genérico:** compila, pero los errores aparecen recién al ejecutar.
- **Mezclar tipos:** el **goblin** de los genéricos aparece cuando metés un texto en un `Estuche<int>`.

### Micro-misión R03-N04-P1 · Un estuche para todo

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: Clase genérica | class Estuche<T> { public T Contenido … } · new Estuche<string>("x")
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Don Cedro tiene el plano del estuche, pero dice «violín» en todos lados. Ceci tiene que hacerlo para cualquier cosa.

#### Gheco sugiere
Poné `<T>` después del nombre de la clase y usá `T` donde iba el tipo fijo:

```csharp
class Bolsa<T>
{
    public T Cosa { get; }
    public Bolsa(T cosa) { Cosa = cosa; }
}
```

#### Desafío
Convertí `Estuche` en `Estuche<T>`: la propiedad y el parámetro del constructor tienen que ser de tipo `T`.

#### Código inicial
```csharp
Estuche<string> a = new Estuche<string>("arco");
Estuche<int> b = new Estuche<int>(440);
Console.WriteLine($"{a.Contenido} y {b.Contenido}");

class Estuche
{
    public string Contenido { get; }

    public Estuche(string contenido)
    {
        Contenido = contenido;
    }
}
```

#### Salida esperada
```
arco y 440
```

#### Solución
```csharp
Estuche<string> a = new Estuche<string>("arco");
Estuche<int> b = new Estuche<int>(440);
Console.WriteLine($"{a.Contenido} y {b.Contenido}");

class Estuche<T>
{
    public T Contenido { get; }

    public Estuche(T contenido)
    {
        Contenido = contenido;
    }
}
```

#### Al superarla
Don Cedro borra la palabra «violín» del plano y escribe una sola letra en su lugar. —Un plano, mil estuches.

#### Imagen
- Tres estuches de madera iguales abiertos sobre una mesa de taller: uno con un violín, otro con un arco y otro con un diapasón, sin letras.
- Don Cedro los muestra orgulloso; Ceci los mira de cerca.

### Micro-misión R03-N04-P2 · El último de cualquier lista

```meta
lugar: El Archivo
personajes: Ceci, Bemol
carta: Método genérico | static T Ultimo<T>(List<T> d) · C# deduce T · sirve con cualquier lista
recompensa: xp 15, oro 15
```

#### Escena
Bemol escribió un método para el último nombre de una lista de textos. Ahora lo necesita para una lista de números, y no quiere escribirlo otra vez.

#### Gheco sugiere
Un método también puede tener `<T>`: se pone después del nombre, y C# deduce el tipo según lo que le pasás:

```csharp
static T Primero<T>(List<T> datos) => datos[0];
```

#### Desafío
Convertí `Ultimo` en genérico para que sirva con las dos listas.

#### Código inicial
```csharp
Console.WriteLine(Ultimo(new List<string> { "Do", "Re", "Mi" }));
Console.WriteLine(Ultimo(new List<int> { 4, 8, 15 }));

static string Ultimo(List<string> datos)
{
    return datos[datos.Count - 1];
}
```

#### Salida esperada
```
Mi
15
```

#### Solución
```csharp
Console.WriteLine(Ultimo(new List<string> { "Do", "Re", "Mi" }));
Console.WriteLine(Ultimo(new List<int> { 4, 8, 15 }));

static T Ultimo<T>(List<T> datos)
{
    return datos[datos.Count - 1];
}
```

#### Al superarla
—Mi y quince —lee Bemol—. Mismo método, otra lista. Me ahorré la mitad del trabajo.

#### Imagen
- Dos columnas de cartas de archivo lisas, una con notitas musicales dibujadas y otra con puntitos, cada una con la última carta brillando, sin letras ni números.
- Bemol señala las dos últimas cartas a la vez; Ceci aplaude.

### Micro-misión R03-N04-P3 · El más grave

```meta
lugar: El Archivo
personajes: Ceci, Clave
carta: where | where T : IComparable<T> · a.CompareTo(b) > 0 → a va después · pide que T sepa compararse
recompensa: xp 15, oro 15
```

#### Escena
Clave quiere un método que devuelva el **menor** de dos valores, sean números o textos. Pero `T` no sabe compararse, y no compila.

#### Gheco sugiere
`where T : IComparable<T>` le pide al tipo que sepa compararse. Entonces se puede usar `CompareTo`:

```csharp
static T Mayor<T>(T a, T b) where T : IComparable<T>
{
    return a.CompareTo(b) > 0 ? a : b;
}
```

#### Desafío
Completá `Menor` con la restricción y `CompareTo`.

#### Código inicial
```csharp
Console.WriteLine(Menor(7, 3));
Console.WriteLine(Menor("Vals", "Marcha"));

static T Menor<T>(T a, T b)
{
    return a;
}
```

#### Salida esperada
```
3
Marcha
```

#### Solución
```csharp
Console.WriteLine(Menor(7, 3));
Console.WriteLine(Menor("Vals", "Marcha"));

static T Menor<T>(T a, T b) where T : IComparable<T>
{
    return a.CompareTo(b) < 0 ? a : b;
}
```

#### Al superarla
—Para ordenar hay que saber comparar —dice Clave—. Y no todo sabe.

#### Imagen
- Una balanza de bronce en una mesa de archivo, con una partitura en cada platillo, una más baja que la otra, sin letras.
- Clave observa la balanza; Ceci acomoda uno de los platillos.

### Micro-misión R03-N04-P4 · La pila del luthier

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: Genérico propio | class Pila<T> con una List<T> adentro · Apilar, Desapilar, Cantidad
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Don Cedro quiere su propia pila, para cualquier cosa, con nombres en castellano. Por dentro, una lista hace el trabajo.

#### Gheco sugiere
Una clase genérica puede tener adentro una `List<T>` con el mismo `T`:

```csharp
class Bolsa<T>
{
    private readonly List<T> _cosas = new List<T>();
    public void Meter(T x) => _cosas.Add(x);
}
```

#### Desafío
Completá `Desapilar`: tiene que devolver el último elemento y sacarlo de la lista.

#### Código inicial
```csharp
var pila = new Pila<string>();
pila.Apilar("cola");
pila.Apilar("barniz");
Console.WriteLine(pila.Desapilar());
Console.WriteLine($"Quedan: {pila.Cantidad}");

class Pila<T>
{
    private readonly List<T> _datos = new List<T>();

    public int Cantidad => _datos.Count;

    public void Apilar(T x) => _datos.Add(x);

    public T Desapilar()
    {
        return _datos[0];
    }
}
```

#### Salida esperada
```
barniz
Quedan: 1
```

#### Solución
```csharp
var pila = new Pila<string>();
pila.Apilar("cola");
pila.Apilar("barniz");
Console.WriteLine(pila.Desapilar());
Console.WriteLine($"Quedan: {pila.Cantidad}");

class Pila<T>
{
    private readonly List<T> _datos = new List<T>();

    public int Cantidad => _datos.Count;

    public void Apilar(T x) => _datos.Add(x);

    public T Desapilar()
    {
        T ultimo = _datos[_datos.Count - 1];
        _datos.RemoveAt(_datos.Count - 1);
        return ultimo;
    }
}
```

#### Al superarla
—Barniz arriba, cola abajo —dice Don Cedro—. Como debe ser: primero se pega, después se barniza.

#### Imagen
- Una repisa de taller con frascos de cola y de barniz apilados, sin etiquetas con letras.
- Don Cedro saca el frasco de arriba; Ceci sostiene el de abajo.

### Micro-misión R03-N04-P5 · El goblin que comparaba sin permiso

```meta
lugar: El Archivo
personajes: Ceci, Gheco
criatura: goblin
carta: Goblin | CS0019: el operador > no se puede aplicar a T · pedí where T : IComparable<T> y usá CompareTo
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un goblin escribió un método genérico que compara con `>`. No compila, y el goblin no entiende por qué: con números siempre anduvo.

#### Gheco sugiere
Con un `T` cualquiera no se puede usar `>`:

```
error CS0019: El operador '>' no se puede aplicar a operandos del tipo 'T' y 'T'
```

Pedí que `T` sepa compararse y usá `CompareTo`: `a.CompareTo(b) > 0` es «`a` es mayor».

#### Desafío
Ensayá, leé el error y arreglá `Mayor`.

#### Código inicial
```csharp
Console.WriteLine(Mayor(3, 9));

static T Mayor<T>(T a, T b)
{
    return a > b ? a : b;
}
```

#### Salida esperada
```
9
```

#### Solución
```csharp
Console.WriteLine(Mayor(3, 9));

static T Mayor<T>(T a, T b) where T : IComparable<T>
{
    return a.CompareTo(b) > 0 ? a : b;
}
```

#### Al superarla
El goblin prueba con números, con textos, con fechas. Todo compara. Se va contento, como si hubiera sido idea suya.

#### Imagen
- Un goblin chico de orejas puntiagudas comparando dos cajas de distinto tamaño, una en cada mano, en un archivo de piedra con faroles, sin letras.
- Gheco, sobre un estante, le señala la caja más grande.

### Encargo R03-N04-E1 · El resultado de Hulda

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Hulda, la minera de las Forjas, busca minerales por código. A veces lo encuentra y a veces no, y quiere que el método diga **qué pasó** sin explotar. Escribí una clase genérica `Resultado<T>` con:

- `bool Exito`, `T? Valor` y `string Error`.
- Dos métodos `static`: `Bien(T valor)` y `Mal(string error)`, que devuelven un `Resultado<T>` armado.

Después, un método `Buscar(Dictionary<string, int> minas, string codigo)` que devuelva un `Resultado<int>` con la cantidad, o un error `No existe <codigo>`. Probalo con `HIE` (hay `40`) y con `ORO` (no está):

```
HIE: 40
Error: No existe ORO
```

#### Criterio de aprobación

- `Resultado<T>` es genérica y se arma con `Bien` o `Mal`.
- `Buscar` no explota cuando el código no existe.

#### Salida esperada

```
HIE: 40
Error: No existe ORO
```

#### Solución de referencia

```csharp
var minas = new Dictionary<string, int> { ["HIE"] = 40, ["COB"] = 12 };
Mostrar("HIE", Buscar(minas, "HIE"));
Mostrar("ORO", Buscar(minas, "ORO"));

static Resultado<int> Buscar(Dictionary<string, int> minas, string codigo)
{
    return minas.TryGetValue(codigo, out int n)
        ? Resultado<int>.Bien(n)
        : Resultado<int>.Mal($"No existe {codigo}");
}

static void Mostrar(string codigo, Resultado<int> r)
{
    Console.WriteLine(r.Exito ? $"{codigo}: {r.Valor}" : $"Error: {r.Error}");
}

class Resultado<T>
{
    public bool Exito { get; private set; }
    public T? Valor { get; private set; }
    public string Error { get; private set; } = "";

    public static Resultado<T> Bien(T valor) => new Resultado<T> { Exito = true, Valor = valor };
    public static Resultado<T> Mal(string error) => new Resultado<T> { Exito = false, Error = error };
}
```

## R03-N05 · yield: la partitura que se entrega de a una

```meta
tipo: tema
padre: R03-N04
precio: 10
criatura: ogro
temas: col.listas, poo.genericos
usa: poo.genericos, prog.bucles
```

### Crónica

Clave le pide a Ceci las escalas del Archivo: todas las notas, de a una, para practicarlas. Ceci empieza a copiarlas en una lista enorme. —No hace falta tenerlas todas juntas —la frena {mentor}—. Te las voy dando **de a una**, cuando me las pidas. Y si te cansás a la mitad, no copié las que sobraban.

### Objetivos

- Escribir un método que entrega valores de a uno con `yield return`.
- Recorrerlo con `foreach` como si fuera una colección.
- Entender que `yield` hace una pausa hasta que le piden el siguiente.

### Antes de empezar

- Los genéricos (R03-N04) y los bucles (R01-N10).

### Explicación

#### `IEnumerable<T>`: algo que se puede recorrer

Todo lo que se recorre con `foreach` (arreglos, listas, diccionarios) es un `IEnumerable<T>`: «se me puede recorrer, y entrego cosas de tipo `T`».

#### `yield return`: entregar de a uno

Un método que devuelve `IEnumerable<T>` puede entregar los valores de a uno con `yield return`:

```csharp
static IEnumerable<string> Escala()
{
    yield return "Do";
    yield return "Re";
    yield return "Mi";
}

foreach (string nota in Escala())
{
    Console.WriteLine(nota);
}
```

Cada `yield return` entrega un valor y **pausa** el método. Cuando el `foreach` pide el siguiente, sigue desde ahí. No arma ninguna lista.

#### Con un bucle adentro

```csharp
static IEnumerable<int> Compases(int desde, int hasta)
{
    for (int i = desde; i <= hasta; i++)
    {
        yield return i;
    }
}
```

`yield break` termina antes de tiempo.

### Código de ejemplo

```csharp
foreach (string nota in Escala())
{
    Console.Write(nota + " ");
}
Console.WriteLine();

foreach (int c in Pares(10))
{
    Console.Write(c + " ");
}
Console.WriteLine();

static IEnumerable<string> Escala()
{
    yield return "Do";
    yield return "Re";
    yield return "Mi";
}

static IEnumerable<int> Pares(int hasta)
{
    for (int i = 0; i <= hasta; i += 2)
    {
        yield return i;
    }
}
```

### Salida esperada

```
Do Re Mi 
0 2 4 6 8 10 
```

### ¿Para qué sirve?

Para recorrer cosas muy grandes o infinitas sin cargarlas en memoria: las líneas de un archivo enorme, los números de una serie, los resultados de una búsqueda. Y es la base de LINQ, que vas a ver en dos nodos.

### Errores habituales

- **Esperar que se ejecute al llamarlo:** `Escala()` solo no hace nada; empieza cuando lo recorrés.
- **Mezclar `return x;` con `yield return`:** en un método con `yield`, se termina con `yield break`, no con `return x;`.
- **Recorrerlo dos veces creyendo que guardó algo:** cada `foreach` lo ejecuta de nuevo. El **ogro** de las cuentas dobles vive de esto.

### Micro-misión R03-N05-P1 · La escala de a una

```meta
lugar: El Archivo
personajes: Ceci, Clave
carta: yield return | static IEnumerable<string> M() { yield return "x"; … } · foreach lo recorre
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Clave le va dando a Ceci las notas de la escala, de a una. Falta la última: `Sol`.

#### Gheco sugiere
Cada `yield return` entrega un valor más:

```csharp
static IEnumerable<string> Colores()
{
    yield return "rojo";
    yield return "azul";
}
```

#### Desafío
Agregá un `yield return` para que la escala termine en `Sol`.

#### Código inicial
```csharp
foreach (string nota in Escala())
{
    Console.WriteLine(nota);
}

static IEnumerable<string> Escala()
{
    yield return "Do";
    yield return "Re";
    yield return "Mi";
    yield return "Fa";
}
```

#### Salida esperada
```
Do
Re
Mi
Fa
Sol
```

#### Solución
```csharp
foreach (string nota in Escala())
{
    Console.WriteLine(nota);
}

static IEnumerable<string> Escala()
{
    yield return "Do";
    yield return "Re";
    yield return "Mi";
    yield return "Fa";
    yield return "Sol";
}
```

#### Al superarla
Do, re, mi, fa, sol. Ceci las toca en el violín a medida que Clave se las nombra, sin apuro.

#### Imagen
- Cinco notas musicales doradas que aparecen de a una en el aire, en fila ascendente, en un archivo de piedra con faroles, sin letras.
- Clave las va señalando con la batuta; Ceci las toca con el violín.

### Micro-misión R03-N05-P2 · Los compases del ensayo

```meta
lugar: El Archivo
personajes: Ceci, Bemol
carta: yield en un bucle | for (…) { yield return i; } · entrega uno por vuelta
recompensa: xp 15, oro 15
```

#### Escena
Bemol cuenta los compases del ensayo en voz alta, del que le digan al que le digan.

#### Gheco sugiere
Un `yield return` dentro de un `for` entrega un valor por vuelta:

```csharp
static IEnumerable<int> Cuenta(int hasta)
{
    for (int i = 1; i <= hasta; i++)
    {
        yield return i;
    }
}
```

#### Desafío
Completá `Compases` para que entregue los números de `desde` a `hasta`.

#### Código inicial
```csharp
foreach (int c in Compases(3, 6))
{
    Console.Write($"{c} ");
}
Console.WriteLine();

static IEnumerable<int> Compases(int desde, int hasta)
{
    yield break;
}
```

#### Salida esperada
```
3 4 5 6 
```

#### Solución
```csharp
foreach (int c in Compases(3, 6))
{
    Console.Write($"{c} ");
}
Console.WriteLine();

static IEnumerable<int> Compases(int desde, int hasta)
{
    for (int i = desde; i <= hasta; i++)
    {
        yield return i;
    }
}
```

#### Al superarla
—Tres, cuatro, cinco, seis —canta Bemol, golpeando el tambor en cada número.

#### Imagen
- Un tambor chico con sus palillos y cuatro círculos de sonido saliendo en ritmo, en un archivo de piedra, sin números.
- Bemol toca con energía; Ceci marca el compás con la cabeza.

### Micro-misión R03-N05-P3 · Solo las notas largas

```meta
lugar: El Archivo
personajes: Ceci, Clave
carta: Filtrar con yield | if (cumple) yield return x; · entrega solo las que sirven
recompensa: xp 15, oro 15
```

#### Escena
Clave quiere practicar solo las notas largas de una melodía: las que duran más de `2` tiempos.

#### Gheco sugiere
Un `yield return` dentro de un `if` entrega solo las que cumplen:

```csharp
static IEnumerable<int> Grandes(int[] datos)
{
    foreach (int d in datos)
    {
        if (d > 10) yield return d;
    }
}
```

#### Desafío
Completá `Largas` para que entregue solo las duraciones mayores que `2`.

#### Código inicial
```csharp
int[] duraciones = { 1, 4, 2, 3, 1, 8 };
foreach (int d in Largas(duraciones))
{
    Console.Write($"{d} ");
}
Console.WriteLine();

static IEnumerable<int> Largas(int[] datos)
{
    foreach (int d in datos)
    {
        yield return d;
    }
}
```

#### Salida esperada
```
4 3 8 
```

#### Solución
```csharp
int[] duraciones = { 1, 4, 2, 3, 1, 8 };
foreach (int d in Largas(duraciones))
{
    Console.Write($"{d} ");
}
Console.WriteLine();

static IEnumerable<int> Largas(int[] datos)
{
    foreach (int d in datos)
    {
        if (d > 2) yield return d;
    }
}
```

#### Al superarla
—Las largas son las que cansan el brazo —dice Clave—. Por eso se practican aparte.

#### Imagen
- Notas musicales doradas de distintos tamaños flotando, con las más grandes brillando más fuerte, en un archivo de piedra, sin letras.
- Clave sostiene un arco de violín largo; Ceci estira el brazo con una nota larga.

### Micro-misión R03-N05-P4 · La escala que no termina

```meta
lugar: El Archivo
personajes: Ceci, Bemol
carta: yield break | corta antes de tiempo · un while (true) con yield no se cuelga si alguien deja de pedir
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol inventó una escala que sube para siempre: cada nota duplica la anterior. Ceci quiere solo hasta que pase de `100`.

#### Gheco sugiere
Con `yield`, un `while (true)` no cuelga el programa: solo da valores cuando se los piden. Para terminar, `yield break`:

```csharp
static IEnumerable<int> Triples()
{
    int n = 1;
    while (true)
    {
        if (n > 50) yield break;
        yield return n;
        n *= 3;
    }
}
```

#### Desafío
Agregá un `yield break` para que la escala se corte cuando `n` pase de `100`.

#### Código inicial
```csharp
foreach (int n in Dobles())
{
    Console.Write($"{n} ");
    if (n > 1000) break;
}
Console.WriteLine();

static IEnumerable<int> Dobles()
{
    int n = 1;
    while (true)
    {
        yield return n;
        n *= 2;
    }
}
```

#### Salida esperada
```
1 2 4 8 16 32 64 
```

#### Solución
```csharp
foreach (int n in Dobles())
{
    Console.Write($"{n} ");
    if (n > 1000) break;
}
Console.WriteLine();

static IEnumerable<int> Dobles()
{
    int n = 1;
    while (true)
    {
        if (n > 100) yield break;
        yield return n;
        n *= 2;
    }
}
```

#### Al superarla
—Hasta sesenta y cuatro —dice Bemol—. La siguiente ya no la alcanza ningún violín.

#### Imagen
- Una escalera de notas doradas que sube en espiral hacia el techo de piedra del archivo y se corta con una pequeña barrera de luz, sin letras.
- Bemol mira hacia arriba con la boca abierta; Ceci le tira de la manga.

### Micro-misión R03-N05-P5 · El ogro que contaba dos veces

```meta
lugar: El Archivo
personajes: Ceci, Gheco
criatura: ogro
carta: Ogro | cada foreach vuelve a ejecutar el método con yield · si hace algo, lo hace dos veces · guardalo en una lista
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un ogro llama a un método que cobra una entrada cada vez que entrega un número. Lo recorre dos veces y cobra el doble.

#### Gheco sugiere
Un método con `yield` se ejecuta **de nuevo** en cada `foreach`. Si querés recorrerlo una sola vez y usarlo varias, guardalo en una lista: `var lista = new List<int>(Entradas());`.

#### Desafío
Guardá las entradas en una lista y recorré la lista dos veces, para que el cobro se muestre una sola vez por entrada.

#### Código inicial
```csharp
var entradas = Entradas();
foreach (int e in entradas) Console.WriteLine($"Entrada {e}");
foreach (int e in entradas) Console.WriteLine($"Revisada {e}");

static IEnumerable<int> Entradas()
{
    for (int i = 1; i <= 2; i++)
    {
        Console.WriteLine("Cobro");
        yield return i;
    }
}
```

#### Salida esperada
```
Cobro
Cobro
Entrada 1
Entrada 2
Revisada 1
Revisada 2
```

#### Solución
```csharp
var entradas = new List<int>(Entradas());
foreach (int e in entradas) Console.WriteLine($"Entrada {e}");
foreach (int e in entradas) Console.WriteLine($"Revisada {e}");

static IEnumerable<int> Entradas()
{
    for (int i = 1; i <= 2; i++)
    {
        Console.WriteLine("Cobro");
        yield return i;
    }
}
```

#### Al superarla
El ogro cuenta las monedas una vez, dos veces, tres. Siempre le da lo mismo. Se va desconfiado, pero sin haber cobrado de más.

#### Imagen
- Un ogro grandote y simpático de piel gris azulada y pelo naranja contando monedas doradas en la palma de la mano, en un archivo de piedra con faroles.
- Gheco, sobre una caja, lleva la cuenta con la cola.

### Encargo R03-N05-E1 · Las campanadas de la Torre

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

El Reloj de la Torre suena cada cuarto de hora. Escribí un método `static IEnumerable<string> Campanadas(int horaDesde, int horaHasta)` que entregue, con `yield return`, los horarios de cada cuarto con el formato `HH:MM` (`8:00`, `8:15`…), desde la `horaDesde` en punto hasta la `horaHasta` en punto incluida.

Leé las dos horas de la entrada (una por línea) y mostrá los horarios:

```
8:00
8:15
8:30
8:45
9:00
```

#### Criterio de aprobación

- `Campanadas` usa `yield return`, sin armar una lista.
- Los minutos se muestran con dos cifras.

#### Entrada de ejemplo

```
8
9
```

#### Salida esperada

```
8:00
8:15
8:30
8:45
9:00
```

#### Solución de referencia

```csharp
int desde = int.Parse(Console.ReadLine() ?? "0");
int hasta = int.Parse(Console.ReadLine() ?? "0");
foreach (string h in Campanadas(desde, hasta))
{
    Console.WriteLine(h);
}

static IEnumerable<string> Campanadas(int horaDesde, int horaHasta)
{
    for (int h = horaDesde; h <= horaHasta; h++)
    {
        for (int m = 0; m < 60; m += 15)
        {
            if (h == horaHasta && m > 0) yield break;
            yield return $"{h}:{m:00}";
        }
    }
}
```

## R03-N06 · Delegados y lambdas: la batuta en la mano

```meta
tipo: tema
padre: R03-N05
precio: 10
criatura: ogro
temas: func.lambdas, func.orden-superior
usa: col.listas, prog.funciones
```

### Crónica

Clave le presta a Ceci su batuta por primera vez. —La batuta no toca nada —le dice—. Le **dice a otro** qué hacer. Señalo a los violines: fuerte. A las flautas: suave. Yo elijo la orden, y la orquesta la ejecuta.

—En C# también se puede pasar una orden de un lado a otro —sigue {mentor}—: un método guardado en una variable. Se llama **delegado**, y la forma corta de escribirlo es una **lambda**.

### Objetivos

- Guardar un método en una variable con `Func` y `Action`.
- Escribir lambdas: `x => x * 2`.
- Pasarle una lambda a otro método para decirle **qué hacer**.
- Usar las lambdas con las listas: `Sort`, `Find`, `RemoveAll`.

### Antes de empezar

- Métodos (R01-N13) y listas (R03-N01).

### Explicación

#### Un método como dato

| Tipo | Qué guarda |
|---|---|
| `Func<int, int>` | recibe un `int`, devuelve un `int` (el **último** es lo que devuelve) |
| `Func<int, int, int>` | recibe dos `int`, devuelve un `int` |
| `Action<string>` | recibe un `string`, no devuelve nada |
| `Predicate<int>` | recibe un `int`, devuelve `bool` |

```csharp
Func<int, int> doble = Duplicar;     // sin paréntesis: se guarda, no se llama
Console.WriteLine(doble(5));         // ahora sí se llama: 10

static int Duplicar(int x) => x * 2;
```

#### Lambdas: métodos sin nombre

```csharp
Func<int, int> triple = x => x * 3;         // recibe x, devuelve x * 3
Func<int, int, int> suma = (a, b) => a + b;
Action saludar = () => Console.WriteLine("¡Hola!");
```

`=>` se lee «va a». A la izquierda, lo que recibe; a la derecha, lo que hace.

#### Pasar una orden a otro método

```csharp
static void Aplicar(int[] datos, Func<int, int> orden)
{
    foreach (int d in datos) Console.Write(orden(d) + " ");
}

Aplicar(notas, x => x + 1);   // a cada una, sumale 1
Aplicar(notas, x => x * x);   // a cada una, elevala al cuadrado
```

#### Las listas ya las usan

```csharp
lista.Sort((a, b) => a.Length.CompareTo(b.Length));   // ordenar por largo
string? hallado = lista.Find(m => m.StartsWith("C"));  // el primero que cumple
lista.RemoveAll(m => m == "rota");                     // sacar todos los que cumplen
```

`RemoveAll` es la forma segura de sacar elementos sin pelearse con el `foreach`.

### Código de ejemplo

```csharp
Func<int, int> doble = x => x * 2;
Func<int, int, int> suma = (a, b) => a + b;
Action<string> anunciar = obra => Console.WriteLine($"Suena: {obra}");

Console.WriteLine(doble(7));
Console.WriteLine(suma(3, 4));
anunciar("Vals");

var orquesta = new List<string> { "Clave", "Bemol", "Ceci", "Don Cedro" };
orquesta.Sort((a, b) => a.Length.CompareTo(b.Length));
Console.WriteLine(string.Join(", ", orquesta));
Console.WriteLine(orquesta.Find(m => m.StartsWith("B")));
orquesta.RemoveAll(m => m.Contains(' '));
Console.WriteLine(orquesta.Count);
```

### Salida esperada

```
14
7
Suena: Vals
Ceci, Clave, Bemol, Don Cedro
Bemol
3
```

### ¿Para qué sirve?

Para decirle a otro **cómo** hacer algo sin escribirlo adentro: cómo ordenar, qué filtrar, qué hacer al apretar un botón. Las lambdas están en todo C# moderno, y son la base de LINQ.

### Errores habituales

- **Poner paréntesis al guardar:** `Func<int, int> f = Duplicar();` llama al método; para guardarlo va sin paréntesis.
- **Confundir el orden de `Func`:** en `Func<string, int>`, recibe `string` y devuelve `int`. El último siempre es lo que devuelve.
- **La captura:** una lambda que usa una variable de afuera ve su valor **al ejecutarse**, no al crearse. El **ogro** de los valores cambiados vive de esto.

### Micro-misión R03-N06-P1 · La orden guardada

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Lambda | Func<int, int> f = x => x * 2; · f(5) la ejecuta · recibe => devuelve
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Clave quiere una orden guardada: «tocalo el doble de veces». Ceci tiene que escribirla como lambda.

#### Gheco sugiere
Una lambda se escribe `parámetro => resultado`, y se guarda en un `Func`:

```csharp
Func<int, int> mas10 = x => x + 10;
Console.WriteLine(mas10(5));   // 15
```

#### Desafío
Completá la lambda `doble` para que devuelva el doble de lo que recibe.

#### Código inicial
```csharp
Func<int, int> doble = x => x;
Console.WriteLine(doble(4));
Console.WriteLine(doble(15));
```

#### Salida esperada
```
8
30
```

#### Solución
```csharp
Func<int, int> doble = x => x * 2;
Console.WriteLine(doble(4));
Console.WriteLine(doble(15));
```

#### Al superarla
Clave le devuelve la batuta. —Una orden, guardada. Ahora la podés usar cuantas veces quieras.

#### Imagen
- Una batuta de director de madera clara flotando con una estela de luz dorada en una sala de ensayo gótica con velas, sin letras.
- Clave se la entrega a Ceci; Ceci la toma con las dos manos.

### Micro-misión R03-N06-P2 · Fuerte o suave

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Pasar una lambda | static void Aplicar(int[] d, Func<int, int> orden) · Aplicar(v, x => x + 1)
recompensa: xp 15, oro 15
```

#### Escena
Bemol tiene los volúmenes de cada músico. Ceci quiere un solo método que les aplique **cualquier** cambio: subir, bajar, duplicar.

#### Gheco sugiere
Un método puede recibir un `Func` como parámetro y usarlo con cada dato. Así la orden la decide quien lo llama:

```csharp
static void Mostrar(int[] d, Func<int, int> f)
{
    foreach (int x in d) Console.Write(f(x) + " ");
    Console.WriteLine();
}
```

#### Desafío
Llamá a `Aplicar` dos veces: una que sume `2` a cada volumen, y otra que lo multiplique por `3`.

#### Código inicial
```csharp
int[] volumenes = { 1, 4, 5 };

// las dos órdenes


static void Aplicar(int[] datos, Func<int, int> orden)
{
    foreach (int d in datos) Console.Write($"{orden(d)} ");
    Console.WriteLine();
}
```

#### Salida esperada
```
3 6 7 
3 12 15 
```

#### Solución
```csharp
int[] volumenes = { 1, 4, 5 };

Aplicar(volumenes, x => x + 2);
Aplicar(volumenes, x => x * 3);

static void Aplicar(int[] datos, Func<int, int> orden)
{
    foreach (int d in datos) Console.Write($"{orden(d)} ");
    Console.WriteLine();
}
```

#### Al superarla
Bemol sube el volumen, lo triplica, se tapa los oídos. —Bueno, bueno, entendí: la orden la elijo yo.

#### Imagen
- Una fila de atriles con círculos de sonido de distintos tamaños saliendo de cada uno, en una sala de ensayo gótica con velas, sin letras.
- Bemol se tapa los oídos riéndose; Ceci baja la batuta.

### Micro-misión R03-N06-P3 · Ordenar por largo

```meta
lugar: El Archivo
personajes: Ceci, Clave
carta: Sort con lambda | l.Sort((a, b) => a.Length.CompareTo(b.Length)); · vos decidís cómo comparar
recompensa: xp 15, oro 15
```

#### Escena
Clave quiere las obras ordenadas de la más corta a la más larga, según el largo de su nombre.

#### Gheco sugiere
`Sort` puede recibir una lambda que compara dos elementos. Devuelve negativo si `a` va antes, positivo si va después:

```csharp
numeros.Sort((a, b) => b.CompareTo(a));   // de mayor a menor
```

#### Desafío
Ordená la lista por el largo de cada nombre, de menor a mayor.

#### Código inicial
```csharp
var obras = new List<string> { "Nocturno", "Vals", "Marcha" };

// ordená por largo

Console.WriteLine(string.Join(", ", obras));
```

#### Salida esperada
```
Vals, Marcha, Nocturno
```

#### Solución
```csharp
var obras = new List<string> { "Nocturno", "Vals", "Marcha" };

obras.Sort((a, b) => a.Length.CompareTo(b.Length));

Console.WriteLine(string.Join(", ", obras));
```

#### Al superarla
—Las cortas primero —dice Clave—. Para calentar los dedos.

#### Imagen
- Tres partituras enrolladas de distinto largo, alineadas de la más corta a la más larga sobre un estante de archivo, sin letras.
- Clave las mide con la batuta; Ceci acomoda la más larga.

### Micro-misión R03-N06-P4 · Encontrar y sacar

```meta
lugar: El Archivo
personajes: Ceci, Bemol
carta: Find y RemoveAll | l.Find(x => cond) el primero que cumple · l.RemoveAll(x => cond) saca todos
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol busca la primera partitura en tono menor y después quiere sacar todas las que están rotas.

#### Gheco sugiere
`Find` devuelve el primero que cumple la condición (o `null` si no hay). `RemoveAll` saca todos los que cumplen:

```csharp
string? largo = palabras.Find(p => p.Length > 5);
palabras.RemoveAll(p => p.Length < 3);
```

#### Desafío
Mostrá la primera obra que termine en `menor` y después sacá todas las que contengan `rota`.

#### Código inicial
```csharp
var obras = new List<string> { "Vals mayor", "Marcha menor", "rota 1", "Nocturno menor", "rota 2" };

Console.WriteLine($"Primera en menor: {obras[0]}");
// sacá las rotas

Console.WriteLine(string.Join(", ", obras));
```

#### Salida esperada
```
Primera en menor: Marcha menor
Vals mayor, Marcha menor, Nocturno menor
```

#### Solución
```csharp
var obras = new List<string> { "Vals mayor", "Marcha menor", "rota 1", "Nocturno menor", "rota 2" };

Console.WriteLine($"Primera en menor: {obras.Find(o => o.EndsWith("menor"))}");
obras.RemoveAll(o => o.Contains("rota"));

Console.WriteLine(string.Join(", ", obras));
```

#### Al superarla
—Sin pelearme con el foreach —dice Bemol—. Le digo «sacá las rotas» y las saca.

#### Imagen
- Un canasto de mimbre con partituras arrugadas al lado de un estante ordenado de carpetas, en un archivo de piedra, sin letras.
- Bemol tira una partitura arrugada al canasto; Ceci sostiene una carpeta sana.

### Micro-misión R03-N06-P5 · El ogro de la variable que cambió

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
criatura: ogro
carta: Ogro | la lambda ve el valor al ejecutarse, no al crearse · si cambia la variable, cambia el resultado
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un ogro guarda una lambda que usa el precio de la entrada. Después sube el precio, y la lambda cobra el precio nuevo, aunque se creó con el viejo.

#### Gheco sugiere
Una lambda **no copia** las variables de afuera: las mira cuando se ejecuta. Si querés que use el valor de ese momento, guardalo antes en otra variable que no cambie:

```csharp
int fijo = precio;
Func<int, int> cobrar = n => n * fijo;
```

#### Desafío
Hacé que la lambda use el precio de `100` aunque después el precio cambie a `150`.

#### Código inicial
```csharp
int precio = 100;
Func<int, int> cobrar = n => n * precio;
precio = 150;
Console.WriteLine($"Tres entradas: {cobrar(3)}");
```

#### Salida esperada
```
Tres entradas: 300
```

#### Solución
```csharp
int precio = 100;
int fijo = precio;
Func<int, int> cobrar = n => n * fijo;
precio = 150;
Console.WriteLine($"Tres entradas: {cobrar(3)}");
```

#### Al superarla
El ogro quiere cobrar ciento cincuenta, pero la orden ya estaba escrita con cien. Refunfuña y devuelve el cambio.

#### Imagen
- Un ogro grandote y simpático de piel gris azulada y pelo naranja devolviendo monedas doradas por una ventanilla de boletería de madera.
- Gheco, sobre el mostrador, cuenta las monedas con la cola.

### Encargo R03-N06-E1 · La tabla de hechizos de Ofidia

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Ofidia, la maga del Valle, quiere una tabla de hechizos: cada nombre calcula el daño a partir del poder. Armá un `Dictionary<string, Func<int, int>>` con:

- `fuego`: el doble del poder.
- `hielo`: el poder más `5`.
- `rayo`: el poder al cuadrado.

Leé líneas `<hechizo> <poder>` hasta `fin` y mostrá `<hechizo>: <daño>`, o `<hechizo>: no existe` si no está en la tabla.

Con esta entrada:

```
fuego 6
rayo 4
viento 3
hielo 10
fin
```

se muestra:

```
fuego: 12
rayo: 16
viento: no existe
hielo: 15
```

#### Criterio de aprobación

- Los hechizos son lambdas guardadas en un `Dictionary`.
- No usa `if` ni `switch` para elegir el hechizo: lo busca en la tabla.

#### Entrada de ejemplo

```
fuego 6
rayo 4
viento 3
hielo 10
fin
```

#### Salida esperada

```
fuego: 12
rayo: 16
viento: no existe
hielo: 15
```

#### Solución de referencia

```csharp
var hechizos = new Dictionary<string, Func<int, int>>
{
    ["fuego"] = p => p * 2,
    ["hielo"] = p => p + 5,
    ["rayo"] = p => p * p,
};

string? linea = Console.ReadLine();
while (linea is not null && linea != "fin")
{
    string[] partes = linea.Split(' ');
    int poder = int.Parse(partes[1]);
    if (hechizos.TryGetValue(partes[0], out Func<int, int>? hechizo))
    {
        Console.WriteLine($"{partes[0]}: {hechizo(poder)}");
    }
    else
    {
        Console.WriteLine($"{partes[0]}: no existe");
    }
    linea = Console.ReadLine();
}
```

## R03-N07 · Eventos: cuando la batuta baja

```meta
tipo: tema
padre: R03-N06
precio: 10
criatura: troll
temas: func.lambdas, diseno.patrones
usa: poo.clases
```

### Crónica

En el concierto, nadie le dice a cada músico «ahora tocá vos». Clave **baja la batuta**, y cada uno de los que estaban atentos hace su parte: el tambor golpea, el violín entra, el que pasa las hojas da vuelta la página. Clave no sabe cuántos están mirando. Solo baja la batuta.

—Eso es un **evento** —dice {mentor}—: un aviso. El que avisa no conoce a los que escuchan. Los que escuchan se **suscriben**, y cuando pasa algo, todos se enteran.

### Objetivos

- Declarar un evento en una clase con `event`.
- Suscribir métodos y lambdas con `+=`, y darlos de baja con `-=`.
- Disparar el evento de forma segura con `?.Invoke`.

### Antes de empezar

- Delegados y lambdas (R03-N06).

### Explicación

#### Declarar y disparar

```csharp
class Batuta
{
    public event Action<int>? Compas;    // el aviso: lleva el número de compás

    public void Bajar(int numero)
    {
        Compas?.Invoke(numero);         // avisa a todos los suscriptos
    }
}
```

El `?` es porque, si nadie se suscribió, el evento vale `null`. `?.Invoke` avisa solo si hay alguien.

#### Suscribirse y darse de baja

```csharp
Batuta batuta = new Batuta();
batuta.Compas += n => Console.WriteLine($"Tambor: pum ({n})");
batuta.Compas += Violin;     // también un método con nombre
batuta.Bajar(1);             // avisa a los dos
batuta.Compas -= Violin;     // el violín deja de escuchar

static void Violin(int n) => Console.WriteLine($"Violín: la ({n})");
```

Desde afuera de la clase solo se puede usar `+=` y `-=`. **Disparar** el evento, solo la clase que lo tiene.

#### Para qué

La batuta no conoce al tambor ni al violín. Se pueden agregar músicos sin tocar la clase `Batuta`. Esto se llama patrón **Observador**, y es como funcionan los botones de una ventana y las señales de Godot y Unity.

### Código de ejemplo

```csharp
Batuta batuta = new Batuta();
batuta.Compas += n => Console.WriteLine($"Tambor: pum ({n})");
batuta.Compas += Violin;

batuta.Bajar(1);
batuta.Compas -= Violin;
batuta.Bajar(2);

static void Violin(int n) => Console.WriteLine($"Violín: la ({n})");

class Batuta
{
    public event Action<int>? Compas;

    public void Bajar(int numero)
    {
        Compas?.Invoke(numero);
    }
}
```

### Salida esperada

```
Tambor: pum (1)
Violín: la (1)
Tambor: pum (2)
```

### ¿Para qué sirve?

Un botón que avisa que lo apretaron, un juego que avisa que el jugador perdió vida, una tienda que avisa que se acabó un producto. El que avisa no sabe quién escucha, y por eso se puede agregar lo que quieras sin romper nada.

### Errores habituales

- **Disparar sin `?.`:** si nadie se suscribió, `Compas(1)` explota. El **troll** de `NullReferenceException` acecha ahí.
- **Disparar desde afuera:** solo la clase que declara el evento puede dispararlo (`CS0070`).
- **Olvidarse del `-=`:** el suscriptor sigue escuchando para siempre.

### Micro-misión R03-N07-P1 · El primer aviso

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: event | public event Action? Inicio; · Inicio?.Invoke(); avisa · afuera: obj.Inicio += …
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Clave tiene una batuta con un evento `Inicio`. Ceci quiere enterarse cuando empiece el concierto.

#### Gheco sugiere
Con `+=` te suscribís a un evento. Cuando la clase lo dispara, tu lambda se ejecuta:

```csharp
timbre.Suena += () => Console.WriteLine("¡Ring!");
timbre.Tocar();
```

Así se declara el evento en la clase: `public event Action? Inicio;`. `Action` es «una función que no recibe nada ni devuelve nada», y el `?` dice que puede no haber nadie suscripto. Para **dispararlo** se escribe `Inicio?.Invoke();`: llama a todos los suscriptos, y si no hay ninguno, no hace nada.

#### Desafío
Suscribí a `Inicio` una lambda que muestre `Ceci levanta el violín`.

#### Código inicial
```csharp
Batuta batuta = new Batuta();

// suscribite

batuta.Empezar();

class Batuta
{
    public event Action? Inicio;

    public void Empezar()
    {
        Console.WriteLine("Clave levanta la batuta");
        Inicio?.Invoke();
    }
}
```

#### Salida esperada
```
Clave levanta la batuta
Ceci levanta el violín
```

#### Solución
```csharp
Batuta batuta = new Batuta();

batuta.Inicio += () => Console.WriteLine("Ceci levanta el violín");

batuta.Empezar();

class Batuta
{
    public event Action? Inicio;

    public void Empezar()
    {
        Console.WriteLine("Clave levanta la batuta");
        Inicio?.Invoke();
    }
}
```

#### Al superarla
Clave levanta la batuta y, sin que nadie se lo diga, Ceci levanta el violín. Estaba atenta.

#### Imagen
- Una sala de ensayo gótica con velas, y una batuta en alto con un destello dorado en la punta, sin letras.
- Clave levanta la batuta; Ceci, enfrente, levanta el violín al mismo tiempo.

### Micro-misión R03-N07-P2 · Muchos atentos

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol, Clave
carta: Varios suscriptos | cada += suma uno más · el evento avisa a todos, en orden
recompensa: xp 15, oro 15
```

#### Escena
Ahora Bemol también quiere enterarse del compás. La batuta no cambia: solo se suma otro que escucha.

#### Gheco sugiere
Cada `+=` agrega otro suscriptor. Al disparar, se avisa a todos, en el orden en que se suscribieron:

```csharp
timbre.Suena += () => Console.WriteLine("Abro");
timbre.Suena += () => Console.WriteLine("Saludo");
```

#### Desafío
Suscribí a Bemol para que, en cada compás, muestre `Bemol: pum (<n>)`.

#### Código inicial
```csharp
Batuta batuta = new Batuta();
batuta.Compas += n => Console.WriteLine($"Ceci: la ({n})");

// Bemol también

batuta.Bajar(1);
batuta.Bajar(2);

class Batuta
{
    public event Action<int>? Compas;

    public void Bajar(int n) => Compas?.Invoke(n);
}
```

#### Salida esperada
```
Ceci: la (1)
Bemol: pum (1)
Ceci: la (2)
Bemol: pum (2)
```

#### Solución
```csharp
Batuta batuta = new Batuta();
batuta.Compas += n => Console.WriteLine($"Ceci: la ({n})");

batuta.Compas += n => Console.WriteLine($"Bemol: pum ({n})");

batuta.Bajar(1);
batuta.Bajar(2);

class Batuta
{
    public event Action<int>? Compas;

    public void Bajar(int n) => Compas?.Invoke(n);
}
```

#### Al superarla
Violín y tambor, juntos en cada compás. Clave no tuvo que decirle nada a nadie: solo bajó la batuta.

#### Imagen
- Una sala de ensayo gótica con velas, con ondas doradas que salen de una batuta y llegan a la vez a un violín y a un tambor, sin letras.
- Clave dirige; Ceci toca el violín y Bemol el tambor, los dos mirando la batuta.

### Micro-misión R03-N07-P3 · El que se va del ensayo

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: -= | obj.Evento -= Metodo; · se da de baja · para eso, suscribite con un método con nombre
recompensa: xp 15, oro 15
```

#### Escena
Después del segundo compás, Bemol se va a buscar otro palillo. Tiene que dejar de escuchar.

#### Gheco sugiere
Para darse de baja con `-=` hace falta el **mismo** método que se suscribió. Por eso conviene usar un método con nombre:

```csharp
timbre.Suena += Abrir;
timbre.Suena -= Abrir;
```

#### Desafío
Después del compás `2`, dá de baja a `Bemol`.

#### Código inicial
```csharp
Batuta batuta = new Batuta();
batuta.Compas += Bemol;

batuta.Bajar(1);
batuta.Bajar(2);
// Bemol se va

batuta.Bajar(3);
Console.WriteLine("Fin");

static void Bemol(int n) => Console.WriteLine($"Bemol: pum ({n})");

class Batuta
{
    public event Action<int>? Compas;

    public void Bajar(int n) => Compas?.Invoke(n);
}
```

#### Salida esperada
```
Bemol: pum (1)
Bemol: pum (2)
Fin
```

#### Solución
```csharp
Batuta batuta = new Batuta();
batuta.Compas += Bemol;

batuta.Bajar(1);
batuta.Bajar(2);
batuta.Compas -= Bemol;

batuta.Bajar(3);
Console.WriteLine("Fin");

static void Bemol(int n) => Console.WriteLine($"Bemol: pum ({n})");

class Batuta
{
    public event Action<int>? Compas;

    public void Bajar(int n) => Compas?.Invoke(n);
}
```

#### Al superarla
El tercer compás suena sin tambor. Bemol vuelve corriendo con el palillo, justo a tiempo para el cuarto.

#### Imagen
- La puerta de una sala de ensayo gótica entreabierta, con un tambor chico olvidado en una silla, sin letras.
- Bemol sale corriendo por la puerta; Ceci sigue tocando el violín y lo mira de reojo.

### Micro-misión R03-N07-P4 · La barra de vida

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: El que avisa | la clase dispara el evento cuando cambia algo · los suscriptos deciden qué hacer
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Clave quiere que el metrónomo **avise** cuando el tempo baja de `60`, para que alguien lo note. El metrónomo no sabe quién va a escuchar.

#### Gheco sugiere
La clase dispara su evento **adentro**, cuando pasa lo que importa:

```csharp
public void Gastar(int n)
{
    Saldo -= n;
    if (Saldo < 10) Bajo?.Invoke(Saldo);
}
```

#### Desafío
En `CambiarTempo`, si el tempo nuevo es menor que `60`, disparar `Lento` con el tempo.

#### Código inicial
```csharp
Metronomo m = new Metronomo();
m.Lento += t => Console.WriteLine($"¡Cuidado! Tempo {t}");

m.CambiarTempo(80);
m.CambiarTempo(50);

class Metronomo
{
    public int Tempo { get; private set; } = 90;
    public event Action<int>? Lento;

    public void CambiarTempo(int nuevo)
    {
        Tempo = nuevo;
        Console.WriteLine($"Tempo: {Tempo}");
    }
}
```

#### Salida esperada
```
Tempo: 80
Tempo: 50
¡Cuidado! Tempo 50
```

#### Solución
```csharp
Metronomo m = new Metronomo();
m.Lento += t => Console.WriteLine($"¡Cuidado! Tempo {t}");

m.CambiarTempo(80);
m.CambiarTempo(50);

class Metronomo
{
    public int Tempo { get; private set; } = 90;
    public event Action<int>? Lento;

    public void CambiarTempo(int nuevo)
    {
        Tempo = nuevo;
        Console.WriteLine($"Tempo: {Tempo}");
        if (Tempo < 60) Lento?.Invoke(Tempo);
    }
}
```

#### Al superarla
—El metrónomo no sabe quién lo escucha —dice Clave—. Solo avisa. Y el que tiene que actuar, actúa.

#### Imagen
- Un metrónomo de madera con forma de pirámide oscilando lento, con una lucecita roja suave que se enciende en la punta, en una sala con velas, sin letras.
- Clave lo mira con atención; Ceci baja el arco.

### Micro-misión R03-N07-P5 · El troll del aviso sin nadie

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
criatura: troll
carta: Troll | NullReferenceException · nadie se suscribió y el evento vale null · Evento?.Invoke(…)
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un troll dispara el evento de la batuta en una sala vacía, sin nadie suscripto. El programa explota.

#### Gheco sugiere
Si nadie se suscribió, el evento es `null`, y llamarlo directamente explota. Con `?.Invoke` se avisa solo si hay alguien:

```csharp
Suena?.Invoke();
```

#### Desafío
Ensayá, mirá cómo explota y arreglá la línea que dispara el evento.

#### Código inicial
```csharp
Batuta batuta = new Batuta();
batuta.Bajar(1);
Console.WriteLine("La sala está vacía, pero no pasó nada malo");

class Batuta
{
    public event Action<int>? Compas;

    public void Bajar(int n) => Compas!(n);
}
```

#### Salida esperada
```
La sala está vacía, pero no pasó nada malo
```

#### Solución
```csharp
Batuta batuta = new Batuta();
batuta.Bajar(1);
Console.WriteLine("La sala está vacía, pero no pasó nada malo");

class Batuta
{
    public event Action<int>? Compas;

    public void Bajar(int n) => Compas?.Invoke(n);
}
```

#### Al superarla
El troll baja la batuta en la sala vacía. No pasa nada. Ni siquiera un eco. Se aburre y se va.

#### Imagen
- Una sala de ensayo gótica vacía, con sillas y atriles sin nadie, iluminada con velas, y un troll chiquito de piel color musgo, pelo de paja y chaleco remendado, sosteniendo una batuta con cara de aburrido.
- Gheco, sobre un atril, lo mira con un ojo abierto.

### Encargo R03-N07-E1 · La alarma del almacén de Baldo

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Baldo quiere enterarse cuando un producto se está acabando. Escribí una clase `Almacen` con un `Dictionary<string, int>` de stock, un método `Agregar(string producto, int cantidad)`, un método `Vender(string producto, int cantidad)` y un evento `StockBajo` (`Action<string, int>`) que se dispara cuando, después de vender, quedan menos de `5`.

Suscribí dos cosas al evento: una que muestre `¡Aviso! Quedan <n> de <producto>` y otra que agregue el producto a una lista de pedidos. Al final, mostrá `Pedir: <productos separados por coma>`.

Agregá `20` velas y `8` cuerdas; vendé `3` velas, `5` cuerdas y `14` velas:

```
¡Aviso! Quedan 3 de cuerdas
¡Aviso! Quedan 3 de velas
Pedir: cuerdas, velas
```

#### Criterio de aprobación

- `Almacen` dispara el evento sin conocer a los suscriptos.
- Hay dos suscriptos distintos.

#### Salida esperada

```
¡Aviso! Quedan 3 de cuerdas
¡Aviso! Quedan 3 de velas
Pedir: cuerdas, velas
```

#### Solución de referencia

```csharp
Almacen almacen = new Almacen();
var pedidos = new List<string>();
almacen.StockBajo += (p, n) => Console.WriteLine($"¡Aviso! Quedan {n} de {p}");
almacen.StockBajo += (p, n) => pedidos.Add(p);

almacen.Agregar("velas", 20);
almacen.Agregar("cuerdas", 8);
almacen.Vender("velas", 3);
almacen.Vender("cuerdas", 5);
almacen.Vender("velas", 14);
Console.WriteLine($"Pedir: {string.Join(", ", pedidos)}");

class Almacen
{
    private readonly Dictionary<string, int> _stock = new Dictionary<string, int>();

    public event Action<string, int>? StockBajo;

    public void Agregar(string producto, int cantidad)
    {
        _stock[producto] = _stock.GetValueOrDefault(producto) + cantidad;
    }

    public void Vender(string producto, int cantidad)
    {
        _stock[producto] -= cantidad;
        if (_stock[producto] < 5) StockBajo?.Invoke(producto, _stock[producto]);
    }
}
```

## R03-N08 · LINQ: preguntarle a la colección

```meta
tipo: tema
padre: R03-N07
precio: 10
criatura: esqueleto
temas: func.streams
usa: func.lambdas, col.listas
```

### Crónica

El Archivo tiene cientos de fichas de músicos: nombre, instrumento, años en la orquesta, puntaje del último examen. Clave quiere saber cosas: los mejores, los de cuerdas, el promedio. Ceci empieza a escribir un `foreach`, un `if`, una lista auxiliar…

—Hay una forma de **preguntarle** a la colección —dice {mentor}—: «dame los de cuerdas, ordenados por nombre, solo el nombre». Se escribe casi como se dice. Se llama **LINQ**.

### Objetivos

- Filtrar con `Where`, transformar con `Select` y ordenar con `OrderBy`.
- Encadenar varios en una sola consulta.
- Resumir con `Count`, `Sum`, `Average`, `Max` y `Min`.
- Preguntar con `Any` y `All`, y buscar con `First` y `FirstOrDefault`.

### Antes de empezar

- Las lambdas (R03-N06) y `record` (R02-N06).

### Explicación

#### Una frase que se lee de arriba abajo

```csharp
var buenos = orquesta
    .Where(m => m.Puntos >= 75)       // solo estos
    .OrderBy(m => m.Nombre)           // en este orden
    .Select(m => m.Nombre);           // de cada uno, esto
```

Cada método recibe una lambda. `m` es cada elemento: el nombre es libre.

#### Los más usados

| Método | Qué hace |
|---|---|
| `Where(cond)` | filtra |
| `Select(x => …)` | transforma cada uno |
| `OrderBy(x => …)` / `OrderByDescending(…)` | ordena (la lista original no cambia) |
| `Take(n)` / `Skip(n)` | los primeros `n` / saltea `n` |
| `Count()`, `Sum(…)`, `Average(…)`, `Max(…)`, `Min(…)` | un valor que resume |
| `Any(cond)` / `All(cond)` | ¿alguno cumple? / ¿todos cumplen? |
| `First(cond)` / `FirstOrDefault(cond)` | el primero; el segundo da `null` si no hay |
| `ToList()` | convierte el resultado en lista |

### Código de ejemplo

```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
    new Musico("Lía", "cuerdas", 93),
    new Musico("Tomi", "vientos", 64),
};

var cuerdas = orquesta.Where(m => m.Seccion == "cuerdas").Select(m => m.Nombre);
Console.WriteLine(string.Join(", ", cuerdas));

var ranking = orquesta.OrderByDescending(m => m.Puntos).Take(2).Select(m => m.Nombre);
Console.WriteLine(string.Join(", ", ranking));

Console.WriteLine(orquesta.Count(m => m.Puntos >= 70));
Console.WriteLine(orquesta.Average(m => m.Puntos));
Console.WriteLine(orquesta.Any(m => m.Seccion == "vientos"));
Console.WriteLine(orquesta.First(m => m.Puntos > 90).Nombre);

record Musico(string Nombre, string Seccion, int Puntos);
```

### Salida esperada

```
Ceci, Lía
Lía, Ceci
3
79
True
Lía
```

### ¿Para qué sirve?

Casi todo programa pregunta cosas a sus datos: los productos sin stock, los alumnos aprobados, el total de las ventas del mes. Con LINQ, cada pregunta es una línea que se lee como una frase.

### Errores habituales

- **Creer que `OrderBy` ordena la lista:** devuelve una secuencia **nueva**; la original queda igual.
- **`First` cuando puede no haber ninguno:** explota (`Sequence contains no elements`). Usá `FirstOrDefault`.
- **Pedir un dato que el elemento no tiene:** el **esqueleto** de `CS1061` aparece si escribís `m.Nombr` o le pedís `.Nombre` a un `int`.

### Micro-misión R03-N08-P1 · Solo las cuerdas

```meta
lugar: El Archivo
personajes: Ceci, Clave
carta: Where | lista.Where(m => cond) · se queda con los que cumplen
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Clave quiere ver solo las fichas de la sección de cuerdas.

#### Gheco sugiere
`Where` recibe una condición y se queda con los elementos que la cumplen:

```csharp
var pares = numeros.Where(n => n % 2 == 0);
```

#### Desafío
Filtrá la orquesta para quedarte con los de `cuerdas`.

#### Código inicial
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
    new Musico("Lía", "cuerdas", 93),
};

var cuerdas = orquesta;
foreach (Musico m in cuerdas) Console.WriteLine(m.Nombre);

record Musico(string Nombre, string Seccion, int Puntos);
```

#### Salida esperada
```
Ceci
Lía
```

#### Solución
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
    new Musico("Lía", "cuerdas", 93),
};

var cuerdas = orquesta.Where(m => m.Seccion == "cuerdas");
foreach (Musico m in cuerdas) Console.WriteLine(m.Nombre);

record Musico(string Nombre, string Seccion, int Puntos);
```

#### Al superarla
—Sin un solo `if` —dice Clave—. Le preguntaste a la lista, y la lista contestó.

#### Imagen
- Un fichero de archivo abierto con fichas de cartón lisas, algunas levantadas y brillando suavemente, sin letras.
- Clave señala las fichas que brillan; Ceci las saca con cuidado.

### Micro-misión R03-N08-P2 · De cada uno, el nombre

```meta
lugar: El Archivo
personajes: Ceci, Bemol
carta: Select | lista.Select(m => m.Nombre) · transforma cada elemento en otra cosa
recompensa: xp 15, oro 15
```

#### Escena
Bemol no quiere las fichas enteras: quiere solo los nombres, en mayúsculas, para el cartel del concierto.

#### Gheco sugiere
`Select` transforma cada elemento en otra cosa:

```csharp
var dobles = numeros.Select(n => n * 2);
var largos = palabras.Select(p => p.Length);
```

#### Desafío
Con `Select`, quedate con el nombre de cada músico en mayúsculas.

#### Código inicial
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
};

var nombres = new List<string>();
Console.WriteLine(string.Join(" · ", nombres));

record Musico(string Nombre, string Seccion, int Puntos);
```

#### Salida esperada
```
CECI · BEMOL
```

#### Solución
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
};

var nombres = orquesta.Select(m => m.Nombre.ToUpper());
Console.WriteLine(string.Join(" · ", nombres));

record Musico(string Nombre, string Seccion, int Puntos);
```

#### Al superarla
—En el cartel van grandes —dice Bemol—. Que se lean desde la última fila.

#### Imagen
- Un cartel de concierto en blanco, de tela lisa sin letras, colgado en la pared de piedra del archivo, con faroles a los costados.
- Bemol sube a una escalera con un pincel; Ceci le sostiene la escalera.

### Micro-misión R03-N08-P3 · Los dos mejores

```meta
lugar: El Archivo
personajes: Ceci, Clave
carta: Encadenar | .OrderByDescending(m => m.Puntos).Take(2).Select(m => m.Nombre) · se lee como una frase
recompensa: xp 15, oro 15
```

#### Escena
Clave elige a los dos solistas del concierto: los de mejor puntaje.

#### Gheco sugiere
Los métodos de LINQ se encadenan: cada uno trabaja sobre lo que dejó el anterior.

```csharp
var tresMayores = numeros.OrderByDescending(n => n).Take(3);
```

#### Desafío
Ordená de mayor a menor puntaje, tomá los dos primeros y quedate con el nombre.

#### Código inicial
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
    new Musico("Lía", "cuerdas", 93),
    new Musico("Tomi", "vientos", 64),
};

var solistas = orquesta.Select(m => m.Nombre);
Console.WriteLine(string.Join(", ", solistas));

record Musico(string Nombre, string Seccion, int Puntos);
```

#### Salida esperada
```
Lía, Ceci
```

#### Solución
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
    new Musico("Lía", "cuerdas", 93),
    new Musico("Tomi", "vientos", 64),
};

var solistas = orquesta.OrderByDescending(m => m.Puntos).Take(2).Select(m => m.Nombre);
Console.WriteLine(string.Join(", ", solistas));

record Musico(string Nombre, string Seccion, int Puntos);
```

#### Al superarla
Ceci se queda mirando su nombre en la lista de solistas. Segunda. Clave no la felicita, pero la sienta en la primera silla.

#### Imagen
- Dos sillas de solista de terciopelo bordó al frente de un escenario gótico con velas, sin letras.
- Clave señala una silla con la batuta; Ceci se sienta, emocionada.

### Micro-misión R03-N08-P4 · Cuántos, cuánto y alguno

```meta
lugar: El Archivo
personajes: Ceci, Bemol
carta: Resumir | Count(cond) · Average(m => …) · Max(m => …) · Any(cond)
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol tiene que pasarle a Clave un resumen: cuántos aprobaron (`70` o más), el puntaje más alto y si hay alguien de vientos.

#### Gheco sugiere
Hay métodos que resumen todo en un solo valor:

```csharp
int cuantos = numeros.Count(n => n > 5);
int mayor = numeros.Max();
bool hayCero = numeros.Any(n => n == 0);
```

#### Desafío
Completá las tres líneas con `Count`, `Max` y `Any`.

#### Código inicial
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
    new Musico("Tomi", "vientos", 64),
};

Console.WriteLine($"Aprobados: {0}");
Console.WriteLine($"Mejor puntaje: {0}");
Console.WriteLine($"¿Hay vientos? {false}");

record Musico(string Nombre, string Seccion, int Puntos);
```

#### Salida esperada
```
Aprobados: 2
Mejor puntaje: 88
¿Hay vientos? True
```

#### Solución
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
    new Musico("Tomi", "vientos", 64),
};

Console.WriteLine($"Aprobados: {orquesta.Count(m => m.Puntos >= 70)}");
Console.WriteLine($"Mejor puntaje: {orquesta.Max(m => m.Puntos)}");
Console.WriteLine($"¿Hay vientos? {orquesta.Any(m => m.Seccion == "vientos")}");

record Musico(string Nombre, string Seccion, int Puntos);
```

#### Al superarla
—Tres líneas —dice Bemol, y le entrega el papel a Clave—. El informe más corto de mi vida.

#### Imagen
- Una hoja de papel doblada lisa, sin escritura, pasando de una mano a otra sobre una mesa de archivo con faroles.
- Bemol le entrega el papel a Clave; Ceci mira por encima.

### Micro-misión R03-N08-P5 · El esqueleto del dato que no existe

```meta
lugar: El Archivo
personajes: Ceci, Gheco
criatura: esqueleto
carta: Esqueleto | CS1061: no contiene una definición · la lambda conoce el tipo del elemento · revisá el nombre
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un esqueleto escribió una consulta pidiendo `m.Puntaje`, pero las fichas dicen `Puntos`. No compila.

#### Gheco sugiere
Dentro de la lambda, `m` es una ficha de `Musico`, y el compilador sabe qué tiene:

```
error CS1061: "Musico" no contiene una definición para "Puntaje"
```

Mirá cómo se llama de verdad en el `record`.

#### Desafío
Ensayá, leé el error y arreglá el nombre del dato.

#### Código inicial
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
};

Console.WriteLine(orquesta.Sum(m => m.Puntaje));

record Musico(string Nombre, string Seccion, int Puntos);
```

#### Salida esperada
```
159
```

#### Solución
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
};

Console.WriteLine(orquesta.Sum(m => m.Puntos));

record Musico(string Nombre, string Seccion, int Puntos);
```

#### Al superarla
El esqueleto busca el «Puntaje» en todas las fichas, no lo encuentra en ninguna y se desarma de vergüenza entre los cajones.

#### Imagen
- Un esqueleto de caricatura desarmándose en un montoncito de huesos frente a un fichero de archivo abierto, sin sangre, con faroles.
- Gheco, sobre el fichero, sostiene una ficha de cartón lisa.

### Encargo R03-N08-E1 · Las notas de la Academia

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

La Maestra de Moldes, en el Imperio, quiere un resumen de sus alumnos. Leé líneas `nombre,nota` hasta `fin` y guardalas como `record Alumno(string Nombre, int Nota)` en una lista. Con LINQ, mostrá:

1. Cuántos aprobaron (nota `6` o más).
2. El promedio, con un decimal.
3. Los aprobados, ordenados de mayor a menor nota, con el formato `<nombre> (<nota>)`.

Con esta entrada:

```
Zed,7
Nadia,9
Tobi,4
Lu,6
fin
```

se muestra:

```
Aprobados: 3
Promedio: 6,5
Nadia (9)
Zed (7)
Lu (6)
```

#### Criterio de aprobación

- Usa `Count`, `Average`, `Where`, `OrderByDescending` y `Select`.
- No usa `foreach` con `if` para filtrar.

#### Entrada de ejemplo

```
Zed,7
Nadia,9
Tobi,4
Lu,6
fin
```

#### Salida esperada

```
Aprobados: 3
Promedio: 6,5
Nadia (9)
Zed (7)
Lu (6)
```

#### Solución de referencia

```csharp
var alumnos = new List<Alumno>();
string? linea = Console.ReadLine();
while (linea is not null && linea != "fin")
{
    string[] partes = linea.Split(',');
    alumnos.Add(new Alumno(partes[0], int.Parse(partes[1])));
    linea = Console.ReadLine();
}

Console.WriteLine($"Aprobados: {alumnos.Count(a => a.Nota >= 6)}");
Console.WriteLine($"Promedio: {alumnos.Average(a => a.Nota):F1}");
var lista = alumnos.Where(a => a.Nota >= 6)
    .OrderByDescending(a => a.Nota)
    .Select(a => $"{a.Nombre} ({a.Nota})");
foreach (string l in lista)
{
    Console.WriteLine(l);
}

record Alumno(string Nombre, int Nota);
```

## R03-N09 · Más LINQ: agrupar, el mejor y tus propias extensiones

```meta
tipo: tema
padre: R03-N08
precio: 10
criatura: ogro
temas: func.streams, func.orden-superior
usa: func.lambdas, col.mapas
```

### Crónica

Clave quiere el informe completo del Archivo: cuántos músicos hay **en cada sección**, quién es el mejor de cada una, y los nombres escritos todos con la primera letra en mayúscula. —Esta vez no te alcanza con filtrar —le dice a Ceci—. Hay que **agrupar**.

### Objetivos

- Agrupar con `GroupBy` y recorrer cada grupo con su `Key`.
- Encontrar **el elemento** con el mayor o menor valor con `MaxBy` y `MinBy`.
- Entender que una consulta se ejecuta recién al recorrerla, y guardarla con `ToList()`.
- Escribir un **método de extensión**.

### Antes de empezar

- LINQ (R03-N08) y `yield` (R03-N05).

### Explicación

#### `GroupBy`: un grupo por cada valor

```csharp
foreach (var grupo in orquesta.GroupBy(m => m.Seccion))
{
    Console.WriteLine($"{grupo.Key}: {grupo.Count()}");
}
```

Cada `grupo` tiene una `Key` (la sección) y adentro, los músicos de esa sección. Se le pueden hacer consultas como a cualquier colección.

#### `MaxBy` y `MinBy`: el elemento, no el número

```csharp
int mejorPuntaje = orquesta.Max(m => m.Puntos);       // un número: 93
Musico mejor = orquesta.MaxBy(m => m.Puntos)!;        // el músico entero
```

#### La consulta es una receta

```csharp
var altos = numeros.Where(n => n > 5);   // todavía no se ejecutó
numeros.Add(10);
Console.WriteLine(altos.Count());        // ahora sí: y cuenta el 10
```

Una consulta se ejecuta **cada vez** que se recorre, con los datos de ese momento. Para guardar el resultado de ahora: `.ToList()`. (Es lo mismo que pasaba con `yield`: LINQ está hecho así por dentro.)

#### Métodos de extensión

`orquesta.Where(…)` no es un método de `List`: es un **método de extensión**, un método `static` de otra clase que se usa como si fuera propio. Vos también podés escribirlos, con `this` en el primer parámetro:

```csharp
static class Extensiones
{
    public static string Capitalizar(this string s)
    {
        return char.ToUpper(s[0]) + s.Substring(1).ToLower();
    }
}
// "bEMOL".Capitalizar() → "Bemol"
```

### Código de ejemplo

```csharp
var orquesta = new List<Musico>
{
    new Musico("ceci", "cuerdas", 88),
    new Musico("bemol", "percusión", 71),
    new Musico("lía", "cuerdas", 93),
};

foreach (var grupo in orquesta.GroupBy(m => m.Seccion))
{
    Musico mejor = grupo.MaxBy(m => m.Puntos)!;
    Console.WriteLine($"{grupo.Key}: {grupo.Count()} (mejor: {mejor.Nombre.Capitalizar()})");
}

var altos = orquesta.Where(m => m.Puntos > 80);
orquesta.Add(new Musico("tomi", "vientos", 85));
Console.WriteLine(altos.Count());

record Musico(string Nombre, string Seccion, int Puntos);

static class Extensiones
{
    public static string Capitalizar(this string s)
    {
        return char.ToUpper(s[0]) + s.Substring(1).ToLower();
    }
}
```

### Salida esperada

```
cuerdas: 2 (mejor: Lía)
percusión: 1 (mejor: Bemol)
3
```

### ¿Para qué sirve?

Las ventas por mes, los alumnos por curso, los pedidos por cliente: agrupar es lo que hace cualquier informe. Y las extensiones te dejan sumar tus propias herramientas a tipos que no escribiste, como `string` o `List`.

### Errores habituales

- **Confundir `Max` con `MaxBy`:** `Max` da el número; `MaxBy`, el elemento que lo tiene.
- **Recorrer dos veces una consulta cara:** se ejecuta dos veces. Guardala con `ToList()`. El **ogro** de los resultados que cambian solos vive de esto.
- **Olvidar el `this` o el `static`:** sin ellos, no es una extensión y no se puede usar con el punto.

### Micro-misión R03-N09-P1 · Por sección

```meta
lugar: El Archivo
personajes: Ceci, Clave
carta: GroupBy | foreach (var g in lista.GroupBy(m => m.Seccion)) · g.Key · g.Count()
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Clave quiere saber cuántos músicos hay en cada sección.

#### Gheco sugiere
`GroupBy` arma un grupo por cada valor distinto. Cada grupo tiene su `Key`:

```csharp
foreach (var g in palabras.GroupBy(p => p.Length))
{
    Console.WriteLine($"{g.Key} letras: {g.Count()}");
}
```

#### Desafío
Agrupá la orquesta por sección y mostrá `<sección>: <cantidad>`.

#### Código inicial
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
    new Musico("Lía", "cuerdas", 93),
};

// agrupá


record Musico(string Nombre, string Seccion, int Puntos);
```

#### Salida esperada
```
cuerdas: 2
percusión: 1
```

#### Solución
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
    new Musico("Lía", "cuerdas", 93),
};

foreach (var grupo in orquesta.GroupBy(m => m.Seccion))
{
    Console.WriteLine($"{grupo.Key}: {grupo.Count()}");
}

record Musico(string Nombre, string Seccion, int Puntos);
```

#### Al superarla
—Dos cuerdas y un tambor —dice Clave—. Necesitamos más vientos.

#### Imagen
- Fichas de cartón lisas agrupadas en montoncitos sobre una mesa de archivo, cada montón atado con una cinta de distinto color, sin letras.
- Clave señala un montoncito; Ceci ata otro con una cinta.

### Micro-misión R03-N09-P2 · El mejor de todos

```meta
lugar: El Archivo
personajes: Ceci, Bemol
carta: MaxBy | lista.MaxBy(m => m.Puntos) devuelve el elemento · Max devuelve solo el número
recompensa: xp 15, oro 15
```

#### Escena
Bemol sabe que el mejor puntaje es `93`, pero no sabe **de quién** es.

#### Gheco sugiere
`Max` da el número; `MaxBy` da el elemento que tiene ese número:

```csharp
string larga = palabras.MaxBy(p => p.Length)!;
```

El `!` le dice al compilador que sabés que la lista no está vacía.

#### Desafío
Usá `MaxBy` para encontrar al músico con más puntos y mostrar su nombre.

#### Código inicial
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
    new Musico("Lía", "cuerdas", 93),
};

Console.WriteLine($"Mejor puntaje: {orquesta.Max(m => m.Puntos)}");
Console.WriteLine($"Es de: ?");

record Musico(string Nombre, string Seccion, int Puntos);
```

#### Salida esperada
```
Mejor puntaje: 93
Es de: Lía
```

#### Solución
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
    new Musico("Lía", "cuerdas", 93),
};

Console.WriteLine($"Mejor puntaje: {orquesta.Max(m => m.Puntos)}");
Console.WriteLine($"Es de: {orquesta.MaxBy(m => m.Puntos)!.Nombre}");

record Musico(string Nombre, string Seccion, int Puntos);
```

#### Al superarla
—Lía —dice Bemol—. Toca el violín desde los cuatro años. No es justo, pero es así.

#### Imagen
- Una ficha de cartón lisa que brilla más que las demás en un fichero de archivo, sin letras.
- Bemol la levanta resignado; Ceci aplaude a una compañera que no está en la escena, mirando hacia afuera.

### Micro-misión R03-N09-P3 · La receta que se ejecuta tarde

```meta
lugar: El Archivo
personajes: Ceci, Clave
carta: ToList | una consulta se ejecuta al recorrerla · .ToList() guarda el resultado de ese momento
recompensa: xp 15, oro 15
```

#### Escena
Clave contó los aprobados antes de que llegara un músico nuevo. Pero el número cambió solo después. Ceci quiere el número **de antes**.

#### Gheco sugiere
Una consulta de LINQ no guarda nada: se ejecuta cuando se recorre, con los datos de ese momento. Con `.ToList()`, el resultado queda guardado:

```csharp
var ahora = numeros.Where(n => n > 5).ToList();
```

#### Desafío
Agregale `.ToList()` a la consulta para que cuente los aprobados de antes de agregar a `Tomi`.

#### Código inicial
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
};

var aprobados = orquesta.Where(m => m.Puntos >= 70);
orquesta.Add(new Musico("Tomi", "vientos", 85));
Console.WriteLine($"Aprobados antes: {aprobados.Count()}");

record Musico(string Nombre, string Seccion, int Puntos);
```

#### Salida esperada
```
Aprobados antes: 2
```

#### Solución
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
};

var aprobados = orquesta.Where(m => m.Puntos >= 70).ToList();
orquesta.Add(new Musico("Tomi", "vientos", 85));
Console.WriteLine($"Aprobados antes: {aprobados.Count()}");

record Musico(string Nombre, string Seccion, int Puntos);
```

#### Al superarla
—Una consulta es una receta —dice Clave—. Si querés la torta de hoy, la tenés que hornear hoy.

#### Imagen
- Una libreta abierta de páginas lisas sin escritura y un reloj de arena al lado, sobre una mesa de archivo con faroles.
- Clave da vuelta el reloj de arena; Ceci cierra la libreta.

### Micro-misión R03-N09-P4 · Una herramienta propia

```meta
lugar: El Archivo
personajes: Ceci, Bemol
carta: Extensión | static class X { public static T M(this Tipo t) … } · se usa con el punto
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Los nombres del Archivo están escritos de cualquier manera: «bEMOL», «CECI». Bemol quiere poder escribir `nombre.Capitalizar()`.

#### Gheco sugiere
Un método de extensión es `static`, va en una clase `static`, y su primer parámetro lleva `this`:

```csharp
static class Ayuda
{
    public static int Doble(this int n) => n * 2;
}
// 5.Doble() → 10
```

#### Desafío
Completá `Capitalizar` para que devuelva la primera letra en mayúscula y el resto en minúscula.

#### Código inicial
```csharp
string[] nombres = { "bEMOL", "CECI", "clave" };
foreach (string n in nombres)
{
    Console.WriteLine(n.Capitalizar());
}

static class Extensiones
{
    public static string Capitalizar(this string s)
    {
        return s;
    }
}
```

#### Salida esperada
```
Bemol
Ceci
Clave
```

#### Solución
```csharp
string[] nombres = { "bEMOL", "CECI", "clave" };
foreach (string n in nombres)
{
    Console.WriteLine(n.Capitalizar());
}

static class Extensiones
{
    public static string Capitalizar(this string s)
    {
        return char.ToUpper(s[0]) + s.Substring(1).ToLower();
    }
}
```

#### Al superarla
—Ahora los textos saben capitalizarse —dice Bemol—. Les enseñé algo nuevo, y ni siquiera eran míos.

#### Imagen
- Una fila de carpetas de archivo con los lomos lisos, perfectamente alineadas y prolijas, sin letras.
- Bemol las acomoda con orgullo; Ceci aprueba con el pulgar arriba.

### Micro-misión R03-N09-P5 · El ogro del primero que no había

```meta
lugar: El Archivo
personajes: Ceci, Gheco
criatura: ogro
carta: Ogro | First explota si no hay ninguno · FirstOrDefault devuelve null · después, ?. y ??
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
El ogro busca al primer músico de arpa. No hay ninguno, y `First` explota.

#### Gheco sugiere
`First` explota si no encuentra nada:

```
Unhandled exception. System.InvalidOperationException: Sequence contains no matching element
```

`FirstOrDefault` devuelve `null` en ese caso, y con `?.` y `??` se muestra algo seguro.

#### Desafío
Ensayá, mirá cómo explota y cambiá la búsqueda para que muestre `nadie` si no hay arpa.

#### Código inicial
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
};

Musico arpa = orquesta.First(m => m.Seccion == "arpa");
Console.WriteLine($"Arpa: {arpa.Nombre}");

record Musico(string Nombre, string Seccion, int Puntos);
```

#### Salida esperada
```
Arpa: nadie
```

#### Solución
```csharp
var orquesta = new List<Musico>
{
    new Musico("Ceci", "cuerdas", 88),
    new Musico("Bemol", "percusión", 71),
};

Musico? arpa = orquesta.FirstOrDefault(m => m.Seccion == "arpa");
Console.WriteLine($"Arpa: {arpa?.Nombre ?? "nadie"}");

record Musico(string Nombre, string Seccion, int Puntos);
```

#### Al superarla
El ogro busca un arpista por todo el Archivo. No hay. Pero el programa sigue de pie, y el ogro se va a buscar arpas a otro lado.

#### Imagen
- Un ogro grandote y simpático de piel gris azulada y pelo naranja mirando debajo de una mesa de archivo con una vela en la mano.
- Gheco, sobre un arpa chiquita de juguete en un estante, lo mira divertido.

### Encargo R03-N09-E1 · Las ventas de la Feria

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

El Flaco Ruiz anota cada venta de la tienda de premios como `producto,cantidad,precio`. Leé ventas hasta `fin`, guardalas como `record Venta(string Producto, int Cantidad, decimal Precio)` y mostrá con LINQ:

1. El total facturado (cantidad × precio, sumado).
2. El producto más vendido (el que suma más **cantidad** entre todas sus ventas).
3. La facturación por producto, de mayor a menor, con el formato `<producto>: <total>`.

Con esta entrada:

```
osito,2,150
pelota,1,80
osito,1,150
silbato,5,20
fin
```

se muestra:

```
Total: 630
Más vendido: silbato
osito: 450
silbato: 100
pelota: 80
```

#### Criterio de aprobación

- Usa `GroupBy` para juntar las ventas de cada producto.
- Usa `MaxBy` o un orden para el más vendido.

#### Entrada de ejemplo

```
osito,2,150
pelota,1,80
osito,1,150
silbato,5,20
fin
```

#### Salida esperada

```
Total: 630
Más vendido: silbato
osito: 450
silbato: 100
pelota: 80
```

#### Solución de referencia

```csharp
var ventas = new List<Venta>();
string? linea = Console.ReadLine();
while (linea is not null && linea != "fin")
{
    string[] p = linea.Split(',');
    ventas.Add(new Venta(p[0], int.Parse(p[1]), decimal.Parse(p[2])));
    linea = Console.ReadLine();
}

Console.WriteLine($"Total: {ventas.Sum(v => v.Cantidad * v.Precio)}");
var porProducto = ventas.GroupBy(v => v.Producto).ToList();
Console.WriteLine($"Más vendido: {porProducto.MaxBy(g => g.Sum(v => v.Cantidad))!.Key}");
foreach (var g in porProducto.OrderByDescending(g => g.Sum(v => v.Cantidad * v.Precio)))
{
    Console.WriteLine($"{g.Key}: {g.Sum(v => v.Cantidad * v.Precio)}");
}

record Venta(string Producto, int Cantidad, decimal Precio);
```

## R03-N10 · Jefe: la Hidra del Coro

```meta
tipo: jefe
padre: R03-N09
precio: 10
criatura: dragon
insignia: Directora del Archivo
insignia_descripcion: Venciste a la Hidra del Coro: sabés guardar, ordenar y preguntarle a tus datos con colecciones, genéricos, lambdas, eventos y LINQ.
usa: col.listas, col.mapas, col.conjuntos, col.pilas-colas, poo.genericos, func.lambdas, func.streams
```

### Crónica

La noche del gran ensayo coral, del fondo del Archivo sube un canto desafinado. Es la **Hidra del Coro**: un cuerpo de tubos de órgano y varias cabezas de cuello largo, cada una cantando una parte distinta, todas a destiempo. Cada cabeza se comió una colección del Archivo: una se tragó la lista de coristas, otra mezcló el diccionario de voces, otra desordenó la fila de entrada.

—Una hidra no se vence de un golpe —dice {mentor}—. Se le calla una cabeza por vez. Usá todo lo del Archivo.

### Objetivos

- Juntar en un programa listas, diccionarios, conjuntos, colas, genéricos, lambdas, eventos y LINQ.
- Elegir la colección correcta para cada problema.

### Antes de empezar

- Todo el Archivo y la batuta (R03-N01 a R03-N09).

### Explicación

#### Qué colección para qué

| Necesito… | Uso |
|---|---|
| una lista que crece, en orden | `List<T>` |
| buscar por nombre | `Dictionary<K, V>` |
| no repetir y preguntar «¿está?» | `HashSet<T>` |
| atender en orden de llegada | `Queue<T>` |
| deshacer lo último | `Stack<T>` |
| filtrar, ordenar, resumir | LINQ |
| avisar a otros | un `event` |

#### Cómo callar a una hidra

1. Mirá qué hace cada parte del programa, de a una.
2. ¿La colección es la correcta? ¿Se repite algo que no debería? ¿Explota con una clave que no está?
3. ¿La consulta pregunta lo que de verdad querés?

### Código de ejemplo

```csharp
var coro = new List<Corista>
{
    new Corista("Ceci", "soprano", 9),
    new Corista("Bemol", "bajo", 6),
    new Corista("Lía", "soprano", 8),
    new Corista("Tomi", "tenor", 7),
};

var porVoz = coro.GroupBy(c => c.Voz).ToDictionary(g => g.Key, g => g.Count());
foreach (var (voz, n) in porVoz.OrderBy(p => p.Key))
{
    Console.WriteLine($"{voz}: {n}");
}

var fila = new Queue<string>(coro.OrderByDescending(c => c.Afinacion).Select(c => c.Nombre));
Console.WriteLine($"Entra primero: {fila.Dequeue()}");

record Corista(string Nombre, string Voz, int Afinacion);
```

### Salida esperada

```
bajo: 1
soprano: 2
tenor: 1
Entra primero: Ceci
```

### ¿Para qué sirve?

Un programa de verdad casi nunca usa una sola colección: lee datos en una lista, los indexa en un diccionario, los resume con LINQ y avisa con eventos cuando algo cambia. Después de la Hidra, sabés elegir la herramienta para cada parte.

### Errores habituales

- **Usar una lista para todo:** funciona, pero se repiten datos y se busca lento.
- **Olvidar que una clave puede no estar:** `TryGetValue` o `GetValueOrDefault`.
- **Ordenar y creer que la lista cambió:** `OrderBy` devuelve otra secuencia.

### Micro-misión R03-N10-P1 · La cabeza que repetía

```meta
lugar: El Archivo
personajes: Ceci, Clave
criatura: dragon
carta: Jefe 1 | un nombre repetido en la lista · HashSet no repite · Add devuelve false si ya estaba
recompensa: xp 20, oro 20, monedas 4
```

#### Escena
La primera cabeza de la Hidra anota a los coristas en una lista, y repite a todos los que se anotan dos veces. El coro parece el doble de grande.

#### Gheco sugiere
Un `HashSet` no guarda repetidos. Y su `Add` te dice si entró:

```csharp
var vistos = new HashSet<string>();
if (vistos.Add("Ana")) Console.WriteLine("nueva");
```

#### Desafío
Cambiá la `List<string>` por un `HashSet<string>` para que cada corista se cuente una sola vez.

#### Código inicial
```csharp
string[] anotados = { "Ceci", "Bemol", "Ceci", "Lía", "Bemol" };
var coro = new List<string>();
foreach (string n in anotados)
{
    coro.Add(n);
}
Console.WriteLine($"Coristas: {coro.Count}");
```

#### Salida esperada
```
Coristas: 3
```

#### Solución
```csharp
string[] anotados = { "Ceci", "Bemol", "Ceci", "Lía", "Bemol" };
var coro = new HashSet<string>();
foreach (string n in anotados)
{
    coro.Add(n);
}
Console.WriteLine($"Coristas: {coro.Count}");
```

#### Al superarla
La primera cabeza de la Hidra se queda sin eco: ya no puede repetir a nadie. Se calla, y se enrosca sobre sí misma.

#### Imagen
- Una criatura hidra de caricatura hecha de tubos dorados de órgano, con varias cabezas de cuello largo cantando con la boca abierta, una de ellas callándose y enroscándose, en un archivo de piedra con faroles, sin letras.
- Ceci la enfrenta con el violín en alto; Clave, detrás, sostiene la batuta.

### Micro-misión R03-N10-P2 · La cabeza de la voz perdida

```meta
lugar: El Archivo
personajes: Ceci, Bemol
criatura: dragon
carta: Jefe 2 | una clave que no está explota · GetValueOrDefault o TryGetValue
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
La segunda cabeza pregunta la voz de un corista que no está en el diccionario. El ensayo explota.

#### Gheco sugiere
`GetValueOrDefault(clave, otro)` devuelve `otro` si la clave no está, sin explotar.

#### Desafío
Arreglá `Voz` para que devuelva `sin voz` si el nombre no está.

#### Código inicial
```csharp
var voces = new Dictionary<string, string> { ["Ceci"] = "soprano", ["Bemol"] = "bajo" };
Console.WriteLine(Voz(voces, "Ceci"));
Console.WriteLine(Voz(voces, "Gheco"));

static string Voz(Dictionary<string, string> voces, string nombre)
{
    return voces[nombre];
}
```

#### Salida esperada
```
soprano
sin voz
```

#### Solución
```csharp
var voces = new Dictionary<string, string> { ["Ceci"] = "soprano", ["Bemol"] = "bajo" };
Console.WriteLine(Voz(voces, "Ceci"));
Console.WriteLine(Voz(voces, "Gheco"));

static string Voz(Dictionary<string, string> voces, string nombre)
{
    return voces.GetValueOrDefault(nombre, "sin voz");
}
```

#### Al superarla
La segunda cabeza busca una voz que no existe, no explota, y se queda muda. Bemol le hace «shhh» con el dedo.

#### Imagen
- La hidra de tubos dorados de órgano con dos cabezas ya calladas y enroscadas, y las demás todavía cantando, en un archivo de piedra, sin letras.
- Bemol le hace «shhh» a una cabeza con el dedo en los labios; Ceci se ríe.

### Micro-misión R03-N10-P3 · La cabeza que desordenaba la fila

```meta
lugar: El Archivo
personajes: Ceci, Clave
criatura: dragon
carta: Jefe 3 | entran por orden de llegada · Queue: Enqueue y Dequeue · no una Stack
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
La tercera cabeza hace entrar a los coristas al revés: el último que llegó entra primero. Usó una pila donde iba una fila.

#### Gheco sugiere
Para «el primero que llega entra primero», va una `Queue`: `Enqueue` para entrar en la fila y `Dequeue` para salir.

#### Desafío
Cambiá la `Stack` por una `Queue` (y sus métodos) para que entren en orden de llegada.

#### Código inicial
```csharp
var fila = new Stack<string>();
fila.Push("Ceci");
fila.Push("Bemol");
fila.Push("Lía");
while (fila.Count > 0)
{
    Console.WriteLine($"Entra: {fila.Pop()}");
}
```

#### Salida esperada
```
Entra: Ceci
Entra: Bemol
Entra: Lía
```

#### Solución
```csharp
var fila = new Queue<string>();
fila.Enqueue("Ceci");
fila.Enqueue("Bemol");
fila.Enqueue("Lía");
while (fila.Count > 0)
{
    Console.WriteLine($"Entra: {fila.Dequeue()}");
}
```

#### Al superarla
Los coristas entran en orden, y la tercera cabeza, mareada, se enrosca con las otras dos.

#### Imagen
- La hidra de tubos dorados de órgano con tres cabezas enroscadas y dormidas, y una fila ordenada de sombras de coristas entrando por una puerta de piedra, sin letras.
- Clave dirige la fila con la batuta; Ceci cuenta a los que pasan.

### Micro-misión R03-N10-P4 · La cabeza que no avisaba

```meta
lugar: El Archivo
personajes: Ceci, Bemol
criatura: dragon
carta: Jefe 4 | el que avisa dispara su evento · los demás se suscriben con += · ?.Invoke
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
La cuarta cabeza tiene el evento del compás, pero nunca lo dispara: nadie sabe cuándo entrar.

#### Gheco sugiere
La clase que tiene el evento lo dispara adentro con `?.Invoke(…)`, en el momento justo. Los demás se suscriben con `+=`.

#### Desafío
Hacé que `Bajar` dispare el evento `Compas` con el número, y suscribí a Bemol para que muestre `Bemol entra en el <n>`.

#### Código inicial
```csharp
Batuta batuta = new Batuta();

batuta.Bajar(1);
batuta.Bajar(2);

class Batuta
{
    public event Action<int>? Compas;

    public void Bajar(int n)
    {
    }
}
```

#### Salida esperada
```
Bemol entra en el 1
Bemol entra en el 2
```

#### Solución
```csharp
Batuta batuta = new Batuta();
batuta.Compas += n => Console.WriteLine($"Bemol entra en el {n}");

batuta.Bajar(1);
batuta.Bajar(2);

class Batuta
{
    public event Action<int>? Compas;

    public void Bajar(int n)
    {
        Compas?.Invoke(n);
    }
}
```

#### Al superarla
El tambor de Bemol marca el compás, y la cuarta cabeza, sin poder desafinar a destiempo, se calla.

#### Imagen
- La hidra de tubos dorados de órgano con cuatro cabezas calladas y una sola todavía cantando, en un archivo de piedra con faroles, sin letras.
- Bemol toca el tambor con fuerza; Ceci levanta el arco listo para el último golpe.

### Micro-misión R03-N10-P5 · El coro completo

```meta
lugar: El Archivo
personajes: Ceci, Clave, Bemol, Gheco
criatura: dragon
carta: Jefe | List + GroupBy + OrderBy + Select · un error a la vez · al final, que cante afinado
recompensa: xp 30, oro 30, monedas 3
item: Partitura del Coro
```

#### Escena
La última cabeza guarda el informe del coro. Tiene tres errores: una consulta que no ordena, un nombre de dato mal escrito y un `First` que explota. Si el informe sale bien, la Hidra se calla para siempre.

#### Gheco sugiere
De a uno. Ensayá y leé el primer error (`CS1061`: un dato que no existe). Después mirá qué sale mal: ¿están ordenadas las voces? ¿Explota buscando a alguien que no está?

`OrderBy(x => …)` ordena **de menor a mayor** (de la A a la Z en textos); es lo contrario de `OrderByDescending`.

#### Desafío
Arreglá el informe: las voces ordenadas alfabéticamente con su cantidad, la mejor afinación y el primer contralto (o `nadie`).

#### Código inicial
```csharp
var coro = new List<Corista>
{
    new Corista("Ceci", "soprano", 9),
    new Corista("Bemol", "bajo", 6),
    new Corista("Lía", "soprano", 8),
    new Corista("Tomi", "tenor", 7),
};

foreach (var g in coro.GroupBy(c => c.Voz))
{
    Console.WriteLine($"{g.Key}: {g.Count()}");
}
Console.WriteLine($"Mejor: {coro.MaxBy(c => c.Afinado)!.Nombre}");
Console.WriteLine($"Contralto: {coro.First(c => c.Voz == "contralto").Nombre}");

record Corista(string Nombre, string Voz, int Afinacion);
```

#### Salida esperada
```
bajo: 1
soprano: 2
tenor: 1
Mejor: Ceci
Contralto: nadie
```

#### Solución
```csharp
var coro = new List<Corista>
{
    new Corista("Ceci", "soprano", 9),
    new Corista("Bemol", "bajo", 6),
    new Corista("Lía", "soprano", 8),
    new Corista("Tomi", "tenor", 7),
};

foreach (var g in coro.GroupBy(c => c.Voz).OrderBy(g => g.Key))
{
    Console.WriteLine($"{g.Key}: {g.Count()}");
}
Console.WriteLine($"Mejor: {coro.MaxBy(c => c.Afinacion)!.Nombre}");
Console.WriteLine($"Contralto: {coro.FirstOrDefault(c => c.Voz == "contralto")?.Nombre ?? "nadie"}");

record Corista(string Nombre, string Voz, int Afinacion);
```

#### Al superarla
El informe sale perfecto, y la última cabeza de la Hidra, por primera vez, canta afinada. Una sola nota, larga y limpia. Después se deshace en una lluvia de hojas que vuelven solas a sus cajones. Entre las hojas queda una partitura dorada que nadie había visto: **la Partitura del Coro**.

{mentor} la levanta y la mira contra la luz. —Esto lo escribió el Vidriero —dice en voz baja—. Es otra parte de la melodía de la cajita.

#### Imagen
- Un archivo de piedra con faroles, lleno de hojas de partitura sin letras que vuelan ordenadas hacia sus cajones, y en el centro una partitura dorada brillante flotando.
- Clave toma la partitura dorada; Ceci, Bemol y Gheco miran asombrados.

### Encargo R03-N10-E1 · El torneo del Gremio

```meta
entrega: codigo
entorno: navegador
monedas: 2
xp: 30
```

#### Consigna

El Gremio organiza un torneo de preguntas entre regiones. Escribí un programa que lea resultados `jugador,region,puntos` hasta `fin` y:

1. Guarde cada resultado como `record Resultado(string Jugador, string Region, int Puntos)` en una `List`.
2. Lleve en un `HashSet` las regiones que participaron.
3. Tenga una clase `Marcador` con un evento `NuevoRecord` (`Action<string, int>`), que se dispara cuando alguien supera el mejor puntaje visto hasta ese momento; suscribí una lambda que muestre `¡Récord! <jugador> con <puntos>`.
4. Al final, con LINQ, muestre los puntos totales por región, de mayor a menor (`<región>: <total>`), y cuántas regiones participaron.

Con esta entrada:

```
Nima,Feria,40
Zed,Imperio,55
Kira,Forjas,30
Nilo,Puerto,55
Ceci,Conservatorio,60
Bruno,Feria,25
fin
```

se muestra:

```
¡Récord! Nima con 40
¡Récord! Zed con 55
¡Récord! Ceci con 60
Feria: 65
Conservatorio: 60
Imperio: 55
Puerto: 55
Forjas: 30
Regiones: 5
```

(Si dos regiones empatan, van en orden alfabético.)

#### Criterio de aprobación

- Usa `List`, `HashSet`, un `event` y LINQ (`GroupBy`, `OrderByDescending`, `ThenBy`).
- `Marcador` avisa sin saber quién escucha.

#### Entrada de ejemplo

```
Nima,Feria,40
Zed,Imperio,55
Kira,Forjas,30
Nilo,Puerto,55
Ceci,Conservatorio,60
Bruno,Feria,25
fin
```

#### Salida esperada

```
¡Récord! Nima con 40
¡Récord! Zed con 55
¡Récord! Ceci con 60
Feria: 65
Conservatorio: 60
Imperio: 55
Puerto: 55
Forjas: 30
Regiones: 5
```

#### Solución de referencia

```csharp
var resultados = new List<Resultado>();
var regiones = new HashSet<string>();
Marcador marcador = new Marcador();
marcador.NuevoRecord += (j, p) => Console.WriteLine($"¡Récord! {j} con {p}");

string? linea = Console.ReadLine();
while (linea is not null && linea != "fin")
{
    string[] x = linea.Split(',');
    var r = new Resultado(x[0], x[1], int.Parse(x[2]));
    resultados.Add(r);
    regiones.Add(r.Region);
    marcador.Anotar(r.Jugador, r.Puntos);
    linea = Console.ReadLine();
}

var totales = resultados.GroupBy(r => r.Region)
    .Select(g => new { Region = g.Key, Total = g.Sum(r => r.Puntos) })
    .OrderByDescending(t => t.Total)
    .ThenBy(t => t.Region);
foreach (var t in totales)
{
    Console.WriteLine($"{t.Region}: {t.Total}");
}
Console.WriteLine($"Regiones: {regiones.Count}");

record Resultado(string Jugador, string Region, int Puntos);

class Marcador
{
    private int _mejor = 0;

    public event Action<string, int>? NuevoRecord;

    public void Anotar(string jugador, int puntos)
    {
        if (puntos > _mejor)
        {
            _mejor = puntos;
            NuevoRecord?.Invoke(jugador, puntos);
        }
    }
}
```
