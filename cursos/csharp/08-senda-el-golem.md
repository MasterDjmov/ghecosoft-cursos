# RAMA S02 · Senda del Gólem: lo que hay debajo de C#

```meta
tipo: senda
posicion: 8
```

## S02-N01 · Cajones de tamaño fijo

```meta
tipo: tema
padre: R02-N05
precio: 3
moneda: comodin
criatura: goblin
temas: prog.variables, maq.registros
usa: prog.enums, prog.operadores
```

### Crónica

Una noche, los tubos del órgano del Conservatorio se encienden solos con una luz cian. La luz baja por los tubos, cruza el piso y toma forma: una chica que flota, con el pelo dorado moviéndose como en el agua.

—Soy **Nova** —dice—. Vivo adentro de **Axón**, el Gólem de Bronce, debajo de las Forjas. Los tubos de tu órgano llegan hasta mis chimeneas, y por ahí escuché que en tu lengua cada número vive en un **cajón de tamaño fijo**. ¡Como mis palancas! —Se pone seria—. Cuando una palanca se pasa de su tope, **da la vuelta** y vuelve a cero, y Axón da un paso de más y se tropieza. ¿Me ayudás a entender qué pasa ahí abajo?

Ceci mira a Clave. Clave ya está buscando la capa. —Vamos —dice {mentor}—. Lo que hay debajo de C# es lo mismo que hay debajo de todo.

### Objetivos

- Conocer los tipos enteros de tamaño fijo: `byte`, `ushort`, `int` y `long`.
- Ver qué pasa cuando un número **se pasa** de su tipo: da la vuelta.
- Pedirle a C# que avise en vez de dar la vuelta, con `checked`.

### Antes de empezar

- Variables y tipos (R01) y `struct` y `enum` (R02-N05). Un `enum` ya es un número por dentro: hoy vas a ver de qué tamaño.

### Explicación

#### Cada tipo es un cajón con un tope

Un `int` no guarda cualquier número: guarda los que entran en **32 interruptores** (bits). Cada tipo entero tiene su cantidad de bits, y eso le pone un mínimo y un máximo:

| Tipo | Bits | Desde | Hasta |
|---|---|---|---|
| `byte` | 8 | 0 | 255 |
| `ushort` | 16 | 0 | 65 535 |
| `int` | 32 | −2 147 483 648 | 2 147 483 647 |
| `long` | 64 | muchísimo | muchísimo |

Las palancas de Axón son de **16 bits**, sin signo: como un `ushort`. No hace falta acordarse los números: cada tipo los tiene guardados.

```csharp
Console.WriteLine(byte.MaxValue);     // 255
Console.WriteLine(ushort.MaxValue);   // 65535
```

#### Pasarse: el número da la vuelta

Si un cajón está lleno y le sumás uno, no hay error: **vuelve a cero**, como el cuentakilómetros de un auto viejo.

```csharp
byte luz = 255;
luz++;
Console.WriteLine(luz);   // 0
```

#### Las cuentas se hacen en `int`

C# hace las cuentas entre `byte` o `ushort` **en `int`**, para no perder nada. Por eso esto no compila:

```csharp
byte a = 200;
byte b = 100;
byte c = a + b;          // error: a + b es un int (300)
byte d = (byte)(a + b);  // así sí: 300 da la vuelta y queda 44
```

Con el `(byte)` le decís «ya sé que puede no entrar; guardá lo que entre».

#### `checked`: que avise en vez de dar la vuelta

A veces dar la vuelta es justo lo que querés (un reloj, un contador). Otras veces es un error que nadie ve. Con `checked`, C# **corta el programa** con un `OverflowException` cuando un número no entra:

```csharp
int pasos = checked(a + b);              // con int entra: 300
ushort ax = checked((ushort)(65535 + 1)); // no entra: OverflowException
```

Y como cualquier excepción, se atrapa con `try`/`catch` (lo vas a ver a fondo en el Acto IV; por ahora alcanza con copiar la forma).

### Código de ejemplo

```csharp
ushort ax = 65535;
ax++;
Console.WriteLine($"AX después de 65535: {ax}");

byte luz = 250;
luz = (byte)(luz + 10);
Console.WriteLine($"Luz: {luz}");

Console.WriteLine($"Un ushort va de {ushort.MinValue} a {ushort.MaxValue}");

try
{
    ushort bx = 65535;
    bx = checked((ushort)(bx + 1));
    Console.WriteLine($"BX: {bx}");
}
catch (OverflowException)
{
    Console.WriteLine("checked: ¡BX se pasó!");
}
```

### Salida esperada

```
AX después de 65535: 0
Luz: 4
Un ushort va de 0 a 65535
checked: ¡BX se pasó!
```

### ¿Para qué sirve?

Los tipos de tamaño fijo están en todos lados: un color es un `byte` por canal (rojo, verde y azul, de 0 a 255), un archivo se lee como `byte`, y un juego que cuenta puntos en un tipo chico puede dar la vuelta y mostrar cero. Saber dónde está el tope te salva de esos errores, y `checked` los hace visibles.

### Errores habituales

- **Guardar una cuenta de `byte` en un `byte` sin cast:** `byte c = a + b;` no compila, porque la cuenta es `int`. Es el **goblin** de los tipos.
- **Creer que pasarse da error:** sin `checked`, el número da la vuelta en silencio.
- **Recorrer con un `byte` hasta 255:** `i <= 255` siempre es verdad para un `byte`, y el bucle no termina nunca.

### Micro-misión S02-N01-P1 · La palanca de 16 bits

```meta
lugar: La sala de las palancas
personajes: Ceci, Nova
carta: Tipos fijos | ushort: 16 bits, de 0 a 65535 · int: 32 bits · al pasarse, vuelve a 0
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Nova le muestra a Ceci la palanca AX, llena hasta el tope. Ceci la anotó en su programa como `int`, y el programa dice 65536. Pero Nova la empuja una vez más y la palanca vuelve a cero, de un golpe.

#### Gheco sugiere
Para que el programa se comporte como la palanca, la variable tiene que ser del **mismo tamaño**. Un `byte`, por ejemplo, es un cajón de 8 bits:

```csharp
byte vela = 255;
vela++;            // 0: un byte no llega a 256
```

#### Desafío
Cambiá el tipo de `ax` de `int` a `ushort`, para que haga lo mismo que la palanca de Axón.

#### Código inicial
```csharp
int ax = 65535;
ax++;
Console.WriteLine($"AX: {ax}");
```

#### Salida esperada
```
AX: 0
```

#### Solución
```csharp
ushort ax = 65535;
ax++;
Console.WriteLine($"AX: {ax}");
```

#### Al superarla
El programa y la palanca dicen lo mismo: cero. Nova aplaude, flotando un poco más alto. —¡Tu lengua tiene palancas como las mías!

#### Imagen
- Una sala de bronce enorme llena de palancas grandes con engranajes a la vista y luces cian, sin letras ni números.
- Nova, una chica de pelo dorado que flota, empuja una palanca que vuelve hacia abajo; Ceci, con su violín a la espalda, la mira con la boca abierta.

### Micro-misión S02-N01-P2 · Los topes de cada cajón

```meta
lugar: La sala de las palancas
personajes: Ceci, Nova, Gheco
carta: MaxValue | byte.MaxValue → 255 · ushort.MaxValue → 65535 · int.MaxValue → 2147483647
recompensa: xp 15, oro 15
```

#### Escena
Nova pegó carteles con el tope de cada cajón, pero los escribió de memoria y se equivocó en todos. Gheco propone no escribirlos a mano: cada tipo sabe su propio tope.

#### Gheco sugiere
Cada tipo entero tiene `MinValue` y `MaxValue`. Así no se escribe ningún número a mano:

```csharp
Console.WriteLine(long.MaxValue);   // el tope de un long
```

#### Desafío
Reemplazá cada número escrito a mano por el `MaxValue` de su tipo: `byte`, `ushort` e `int`.

#### Código inicial
```csharp
Console.WriteLine($"byte: {256}");
Console.WriteLine($"ushort: {65536}");
Console.WriteLine($"int: {2000000000}");
```

#### Salida esperada
```
byte: 255
ushort: 65535
int: 2147483647
```

#### Solución
```csharp
Console.WriteLine($"byte: {byte.MaxValue}");
Console.WriteLine($"ushort: {ushort.MaxValue}");
Console.WriteLine($"int: {int.MaxValue}");
```

#### Al superarla
Nova cambia los carteles. Ahora cada cajón dice su tope de verdad, y ninguno se equivoca, porque no lo escribió nadie.

#### Imagen
- Tres cajones de bronce de distinto tamaño, uno chico, uno mediano y uno enorme, en una pared con engranajes, sin letras ni números.
- Nova despega un cartel viejo; Gheco, un gecko de luz cian con antiparras, MINÚSCULO, sentado arriba del cajón chico, señala el más grande.

### Micro-misión S02-N01-P3 · La suma de dos bytes

```meta
lugar: La sala de las palancas
personajes: Ceci, Nova
carta: Cast | byte + byte → int · (byte)(a + b) guarda lo que entra · lo que sobra da la vuelta
recompensa: xp 15, oro 15
```

#### Escena
Dos interruptores de luz de Axón guardan un `byte` cada uno: 200 y 100. Ceci quiere sumarlos en un tercero, pero el programa ni siquiera arranca.

#### Gheco sugiere
La cuenta entre dos `byte` se hace en `int`, y un `int` no entra solo en un `byte`. Hay que pedir el cast, con paréntesis alrededor de **toda** la cuenta:

```csharp
ushort pasos = (ushort)(ax + bx);
```

#### Desafío
Agregá el cast `(byte)` a la suma para que el programa compile. Vas a ver que 300 no entra en un byte y da la vuelta.

#### Código inicial
```csharp
byte a = 200;
byte b = 100;
byte suma = a + b;
Console.WriteLine($"Suma: {suma}");
```

#### Salida esperada
```
Suma: 44
```

#### Solución
```csharp
byte a = 200;
byte b = 100;
byte suma = (byte)(a + b);
Console.WriteLine($"Suma: {suma}");
```

#### Al superarla
Compila, y da 44: lo que sobró de 256. Nova se rasca la cabeza. —Entonces el cast no arregla nada: solo me deja hacerlo. Ceci asiente. —Y te avisa que lo hacés a propósito.

#### Imagen
- Dos interruptores de bronce con luces, uno muy encendido y otro a medias, conectados a un tercero que chisporrotea, en una pared de engranajes, sin letras ni números.
- Ceci sostiene un cable entre dos interruptores; Nova, flotando, mira de cerca la chispa.

### Micro-misión S02-N01-P4 · Que avise

```meta
lugar: La sala de las palancas
personajes: Ceci, Nova, Clave
carta: checked | checked((ushort)(ax + 5)) · si no entra: OverflowException · se atrapa con catch
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Nova le suma 5 pasos a la palanca AX, que está casi llena, y Axón da un paso hacia atrás: la palanca dio la vuelta y quedó en 4. Clave dice que eso es peor que un error: es un error que **no se ve**.

#### Gheco sugiere
`checked` hace que la conversión **avise** con un `OverflowException` cuando el número no entra, en vez de dar la vuelta:

```csharp
byte vela = checked((byte)(200 + 100));   // OverflowException
```

El `catch` de abajo ya está listo para atraparlo.

#### Desafío
Envolvé la conversión en `checked(...)` para que el programa avise en vez de mostrar `AX: 4`.

#### Código inicial
```csharp
ushort ax = 65535;
try
{
    ax = (ushort)(ax + 5);
    Console.WriteLine($"AX: {ax}");
}
catch (OverflowException)
{
    Console.WriteLine("¡Alto! AX se pasa de 65535");
}
```

#### Salida esperada
```
¡Alto! AX se pasa de 65535
```

#### Solución
```csharp
ushort ax = 65535;
try
{
    ax = checked((ushort)(ax + 5));
    Console.WriteLine($"AX: {ax}");
}
catch (OverflowException)
{
    Console.WriteLine("¡Alto! AX se pasa de 65535");
}
```

#### Al superarla
La palanca se traba antes de dar la vuelta y una campanita suena en todo el Gólem. Axón se queda quieto, con un pie en el aire. —Gracias —retumba su voz—. Prefiero que me avisen.

#### Imagen
- Una palanca de bronce trabada a mitad de camino con una campanita sonando arriba, en una sala de engranajes, sin letras ni números.
- Clave, con su capa y la mecha blanca en el rodete, asiente con los brazos cruzados; Nova se tapa los oídos riendo.

### Micro-misión S02-N01-P5 · El ogro del contador eterno

```meta
lugar: La sala de las palancas
personajes: Ceci, Nova, Gheco
criatura: ogro
carta: Ogro | byte i <= 255 siempre es verdad · después de 255 vuelve a 0 · para contar hasta 256, int
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un ogro de las Forjas se ofreció a probar los 256 interruptores de un cajón, uno por uno. Usa un `byte` para contar. Lleva horas y no termina nunca: cuando llega a 255, vuelve a 0 y empieza otra vez.

#### Gheco sugiere
Un `byte` nunca llega a 256: después de 255 da la vuelta a 0. Entonces `i <= 255` es **siempre** verdad y el bucle no termina. Para contar más allá del tope, el contador tiene que ser de un tipo más grande:

```csharp
for (int nota = 0; nota < 300; nota++) { }   // un int llega a 300 sin problema
```

#### Desafío
Cambiá el tipo de `i` a `int` para que el ogro termine de probar los 256 interruptores.

#### Código inicial
```csharp
int probados = 0;
for (byte i = 0; i <= 255; i++)
{
    probados++;
}
Console.WriteLine($"Interruptores probados: {probados}");
```

#### Salida esperada
```
Interruptores probados: 256
```

#### Solución
```csharp
int probados = 0;
for (int i = 0; i <= 255; i++)
{
    probados++;
}
Console.WriteLine($"Interruptores probados: {probados}");
```

#### Al superarla
El ogro prueba el último interruptor, cuenta con los dedos y se va a dormir la siesta, satisfecho, en un rincón de la sala.

#### Imagen
- Una pared de bronce cubierta de interruptores chiquitos con luces, en filas, sin letras ni números.
- El ogro grandote, con camisa cerrada y cara de cansado, aprieta interruptores uno por uno; Gheco, MINÚSCULO, flota a su lado con un reloj de arena.

## S02-N02 · Binario y hexadecimal

```meta
tipo: tema
padre: S02-N01
precio: 10
criatura: goblin
temas: maq.numeracion, prog.bits
usa: prog.variables, prog.cadenas
```

### Crónica

En la frente de Axón hay un ojo redondo de cristal. Ahí aparecen los números de las palancas, pero no como los escribe Ceci: aparecen como `002A` o `00000101`. —Es que yo no pienso en diez —dice Nova—. Pienso en **interruptores**: prendido o apagado. Y para no escribir tantos, los junto de a cuatro.

Ceci frunce la nariz. —¿Y por qué el ojo escribe letras en los números?

### Objetivos

- Mostrar un número en **binario** (`{n:B8}`) y en **hexadecimal** (`{n:X4}`).
- Escribir números en binario y en hexadecimal dentro del código (`0b0101`, `0x2A`).
- Leer un texto en hexadecimal y convertirlo en número (`Convert.ToInt32(texto, 16)`).

### Antes de empezar

- Los tipos de tamaño fijo (S02-N01) y el formato de los textos con `{…}` (R01).

### Explicación

#### Binario: de a un interruptor

En **binario** cada cifra es un interruptor: `1` prendido, `0` apagado. Cada lugar vale el doble que el de su derecha: 1, 2, 4, 8, 16…

| Binario | Cuenta | Decimal |
|---|---|---|
| `0101` | 4 + 1 | 5 |
| `1010` | 8 + 2 | 10 |
| `1111` | 8 + 4 + 2 + 1 | 15 |

#### Hexadecimal: de a cuatro interruptores

Cuatro interruptores van de 0 a 15. El **hexadecimal** les da una sola cifra a cada grupo: del 0 al 9, y después **A** (10), **B** (11), **C** (12), **D** (13), **E** (14) y **F** (15). Por eso un `ushort` (16 bits) se escribe siempre con 4 cifras hexadecimales: `002A` es 42, y `FFFF` es 65535.

#### Mostrar en binario o en hexa

Dentro de las llaves, después de `:`, va el formato. `B` es binario y `X` es hexadecimal; el número dice cuántas cifras, con ceros adelante:

```csharp
int n = 42;
Console.WriteLine($"{n:B8}");   // 00101010
Console.WriteLine($"{n:X4}");   // 002A
Console.WriteLine($"{n:X}");    // 2A
```

#### Escribirlos en el código

Un número que empieza con `0b` está en binario, y uno que empieza con `0x`, en hexa. El `_` se puede usar para separar y no cambia nada:

```csharp
int a = 0b0010_1010;   // 42
int b = 0x2A;          // 42
```

#### Leer un texto en hexa

`int.Parse("2A")` se rompe, porque espera decimal. Para otra base, `Convert.ToInt32` recibe el texto y la base:

```csharp
int c = Convert.ToInt32("2A", 16);   // 42
int d = Convert.ToInt32("101", 2);   // 5
```

### Código de ejemplo

```csharp
ushort ax = 42;
Console.WriteLine($"Decimal: {ax}");
Console.WriteLine($"Binario: {ax:B16}");
Console.WriteLine($"Hexa: {ax:X4}");

int puerta = 0xFF;
int luces = 0b0000_0101;
Console.WriteLine($"Puerta: {puerta}, luces: {luces}");

int leido = Convert.ToInt32("1F", 16);
Console.WriteLine($"1F en hexa es {leido}");
```

### Salida esperada

```
Decimal: 42
Binario: 0000000000101010
Hexa: 002A
Puerta: 255, luces: 5
1F en hexa es 31
```

### ¿Para qué sirve?

El hexadecimal está en los colores de una página (`#FF8800`), en los errores de Windows (`0x80070005`), en las direcciones de memoria y en los depuradores. Leerlo sin miedo es parte de entender lo que pasa por debajo de cualquier lenguaje.

### Errores habituales

- **Leer hexa con `int.Parse`:** `int.Parse("2A")` da `FormatException` (el **goblin**). Va `Convert.ToInt32(texto, 16)`.
- **Olvidarse de la cantidad de cifras:** `{n:X}` muestra `2A`, pero el ojo de Axón quiere `002A`: `{n:X4}`.
- **Confundir `10` en hexa con diez:** `0x10` es dieciséis.

### Micro-misión S02-N02-P1 · El número en el ojo

```meta
lugar: El ojo del Gólem
personajes: Ceci, Nova
carta: Hexa | {n:X4} → 002A · X es hexadecimal · el 4 pide cuatro cifras
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
El ojo de Axón quiere ver la palanca AX como la ve Nova: en hexadecimal y con cuatro cifras. El programa de Ceci la muestra en decimal.

#### Gheco sugiere
Después de `:`, dentro de las llaves, va el formato. `X` es hexadecimal, y el número es la cantidad de cifras:

```csharp
int bx = 255;
Console.WriteLine($"{bx:X2}");   // FF
```

#### Desafío
Mostrá `ax` en hexadecimal con cuatro cifras.

#### Código inicial
```csharp
ushort ax = 42;
Console.WriteLine($"AX={ax}");
```

#### Salida esperada
```
AX=002A
```

#### Solución
```csharp
ushort ax = 42;
Console.WriteLine($"AX={ax:X4}");
```

#### Al superarla
El ojo de Axón parpadea y muestra lo mismo que la pantalla de Ceci. Nova le da un golpecito al cristal, contenta.

#### Imagen
- Un enorme ojo redondo de cristal en una cara de bronce con remaches, brillando en cian, visto desde adentro del Gólem, sin letras ni números.
- Ceci y Nova miran el ojo desde una pasarela; Nova señala el cristal.

### Micro-misión S02-N02-P2 · Los ocho interruptores

```meta
lugar: La sala de los interruptores
personajes: Ceci, Nova
carta: Binario | {n:B8} → 00000101 · B es binario · cada cifra es un interruptor
recompensa: xp 15, oro 15
```

#### Escena
Una fila de ocho interruptores guarda un `byte`. Nova quiere que la pantalla los muestre uno por uno, prendidos y apagados, y no como un número suelto.

#### Gheco sugiere
`B` es binario. Con `B8` salen siempre ocho cifras, con ceros adelante, como ocho interruptores:

```csharp
int luces = 3;
Console.WriteLine($"{luces:B4}");   // 0011
```

#### Desafío
Mostrá `fila` en binario, con ocho cifras.

#### Código inicial
```csharp
byte fila = 5;
Console.WriteLine($"Interruptores: {fila}");
```

#### Salida esperada
```
Interruptores: 00000101
```

#### Solución
```csharp
byte fila = 5;
Console.WriteLine($"Interruptores: {fila:B8}");
```

#### Al superarla
La pantalla y la fila de interruptores coinciden: dos prendidos, seis apagados. Ceci cuenta: 4 y 1, cinco.

#### Imagen
- Una fila de ocho interruptores grandes de bronce en una pared, dos encendidos con luz cian y seis apagados, sin letras ni números.
- Nova, flotando, toca uno encendido; Ceci cuenta con los dedos.

### Micro-misión S02-N02-P3 · Las notas de Nova

```meta
lugar: La sala de las palancas
personajes: Ceci, Nova, Gheco
carta: Leer hexa | Convert.ToInt32("2A", 16) → 42 · el 16 es la base · int.Parse solo lee decimal
recompensa: xp 15, oro 15
```

#### Escena
Nova anota todo en hexa, en tiras de papel: `2A`, `FF`, `100`. El programa de Ceci las lee con `int.Parse` y se rompe en la primera.

#### Gheco sugiere
`int.Parse` solo entiende decimal. `Convert.ToInt32` recibe el texto **y la base**:

```csharp
int luces = Convert.ToInt32("1010", 2);   // 10, porque está en binario
```

#### Desafío
Cambiá `int.Parse(nota)` por `Convert.ToInt32(nota, 16)`.

#### Código inicial
```csharp
string[] notas = ["2A", "FF", "100"];
foreach (string nota in notas)
{
    int valor = int.Parse(nota);
    Console.WriteLine($"{nota} → {valor}");
}
```

#### Salida esperada
```
2A → 42
FF → 255
100 → 256
```

#### Solución
```csharp
string[] notas = ["2A", "FF", "100"];
foreach (string nota in notas)
{
    int valor = Convert.ToInt32(nota, 16);
    Console.WriteLine($"{nota} → {valor}");
}
```

#### Al superarla
Ceci lee las tiras en voz alta, en decimal. Nova se ríe del último: —¡Cien es doscientos cincuenta y seis!

#### Imagen
- Tiras de papel colgadas de un hilo con broches, sobre una pared de bronce, con garabatos ilegibles, sin letras ni números claros.
- Nova cuelga una tira más; Gheco, MINÚSCULO, sentado en el hilo, se balancea.

### Micro-misión S02-N02-P4 · NOVA en el ojo

```meta
lugar: El ojo del Gólem
personajes: Ceci, Nova
carta: Letras | (int)'A' → 65 · {(int)c:X2} → 41 · cada letra es un número
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Lo que Nova más quiere es ver su nombre en el ojo de Axón. Pero el ojo no entiende letras: solo números en hexa, uno por letra.

#### Gheco sugiere
Cada letra es un número por dentro: `(int)'A'` es 65. Y ese número se puede mostrar en hexa, con dos cifras:

```csharp
char letra = 'C';
Console.WriteLine($"{(int)letra:X2}");   // 43
```

#### Desafío
Mostrá cada letra de `nombre` en hexadecimal, con dos cifras, en vez de en decimal.

#### Código inicial
```csharp
string nombre = "NOVA";
foreach (char c in nombre)
{
    Console.Write($"{(int)c} ");
}
Console.WriteLine();
```

#### Salida esperada
```
4E 4F 56 41
```

#### Solución
```csharp
string nombre = "NOVA";
foreach (char c in nombre)
{
    Console.Write($"{(int)c:X2} ");
}
Console.WriteLine();
```

#### Al superarla
El ojo de Axón se enciende y, por primera vez, muestra un nombre. Nova se queda mirándolo un rato largo, sin decir nada.

#### Imagen
- Un ojo redondo de cristal enorme brillando en cian con cuatro destellos en fila, en una cara de bronce, sin letras ni números.
- Nova, emocionada, con las manos juntas en el pecho; Ceci, a su lado, sonríe.

### Micro-misión S02-N02-P5 · El goblin del color grande

```meta
lugar: La sala de los interruptores
personajes: Ceci, Gheco
criatura: goblin
carta: Goblin | 0x1FF no entra en un byte (tope 0xFF) · ushort llega a 0xFFFF
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un goblin cambió el color de una lámpara del Gólem por `0x1FF` y lo quiere guardar en un `byte`. El programa no compila, y el goblin se ríe desde arriba de la lámpara.

#### Gheco sugiere
Un `byte` llega hasta `0xFF` (255). `0x1FF` son tres cifras hexa: no entra. Hace falta un cajón más grande, como `ushort`, que llega a `0xFFFF`:

```csharp
ushort paso = 0x1234;   // entra: cuatro cifras hexa
```

#### Desafío
Cambiá el tipo de `color` a `ushort`.

#### Código inicial
```csharp
byte color = 0x1FF;
Console.WriteLine($"Color: {color:X4}");
```

#### Salida esperada
```
Color: 01FF
```

#### Solución
```csharp
ushort color = 0x1FF;
Console.WriteLine($"Color: {color:X4}");
```

#### Al superarla
La lámpara se prende de un color que no tiene nombre. El goblin, sin chiste para hacer, se descuelga y se va silbando.

#### Imagen
- Una lámpara de bronce colgada de una cadena, encendida de un color violeta raro, en una sala de engranajes, sin letras ni números.
- Un goblin verde chiquito se descuelga de la lámpara; Ceci lo mira con las manos en la cintura y Gheco, MINÚSCULO, le apunta con el dedo.

## S02-N03 · Interruptores con bits

```meta
tipo: tema
padre: S02-N02
precio: 10
criatura: ogro
temas: prog.bits, maq.banderas
usa: maq.numeracion, prog.enums
```

### Crónica

Debajo del ojo hay una caja de interruptores que Nova cuida más que a nada: las **banderas**. Una dice si la última cuenta dio cero, otra si se pasó, otra si dio negativo. Todas viven en un solo número.

—El problema es que cuando quiero prender una, apago las otras —dice Nova—. Y cuando quiero saber si una está prendida, el número me dice otra cosa.

Ceci mira la caja. —Es como afinar una cuerda sin tocar las demás.

### Objetivos

- Saber si un bit está prendido, con `&` (la máscara).
- Prender un bit con `|`, apagarlo con `& ~` e invertirlo con `^`.
- Correr bits con `<<` y `>>`, y separar las dos mitades de una palanca.
- Ponerle nombre a cada bit con un `enum` marcado con `[Flags]`.

### Antes de empezar

- Binario y hexadecimal (S02-N02) y los `enum` (R02-N05).

### Explicación

#### Las operaciones de a un bit

Estos operadores trabajan **bit por bit**, de a pares, como si se apoyaran dos filas de interruptores una sobre otra:

| Operador | Da 1 si… | Para qué sirve |
|---|---|---|
| `a & b` | los dos son 1 | **mirar** un bit (máscara) o apagar |
| `a \| b` | alguno es 1 | **prender** un bit |
| `a ^ b` | son distintos | **invertir** un bit |
| `~a` | `a` es 0 | dar vuelta todos |

```csharp
int banderas = 0b0110;
bool cero = (banderas & 0b0010) != 0;   // ¿está el segundo? sí
banderas |= 0b0001;                     // prende el primero: 0111
banderas &= ~0b0100;                    // apaga el tercero: 0011
banderas ^= 0b1000;                     // invierte el cuarto: 1011
```

La **máscara** es un número con un solo bit prendido: el que te interesa. Con `&`, todo lo demás queda en cero.

#### Correr bits

`<<` corre los bits a la izquierda (cada lugar multiplica por 2) y `>>` a la derecha (divide por 2). Sirve para separar las dos mitades de una palanca de 16 bits, como la parte alta (`AH`) y la baja (`AL`) de `AX`:

```csharp
ushort ax = 0x1234;
int ah = ax >> 8;      // 0x12: corre 8 lugares, se cae la mitad baja
int al = ax & 0xFF;    // 0x34: la máscara deja solo los 8 de abajo
```

#### Nombres para los bits: `[Flags]`

Escribir `0b0010` en todos lados confunde. Un `enum` con `[Flags]` le pone nombre a cada bit; los valores tienen que ser **potencias de 2** (1, 2, 4, 8…), un bit cada uno:

```csharp
[Flags]
enum Bandera { Ninguna = 0, Acarreo = 1, Cero = 2, Signo = 4, Desborde = 8 }

Bandera b = Bandera.Cero | Bandera.Signo;
Console.WriteLine(b);                         // Cero, Signo
Console.WriteLine(b.HasFlag(Bandera.Cero));   // True
```

(En el 8086 de verdad, las banderas están en otros lugares del registro; acá las pusimos juntas para que se vean mejor.)

### Código de ejemplo

```csharp
int banderas = 0b0000;
banderas |= 0b0010;
banderas |= 0b0100;
Console.WriteLine($"Prendidas: {banderas:B4}");

bool cero = (banderas & 0b0010) != 0;
Console.WriteLine($"¿Cero? {cero}");

banderas &= ~0b0010;
Console.WriteLine($"Después de apagar: {banderas:B4}");

ushort ax = 0xBEEF;
Console.WriteLine($"AH={ax >> 8:X2} AL={ax & 0xFF:X2}");

Bandera b = Bandera.Acarreo | Bandera.Desborde;
Console.WriteLine(b);

[Flags]
enum Bandera { Ninguna = 0, Acarreo = 1, Cero = 2, Signo = 4, Desborde = 8 }
```

### Salida esperada

```
Prendidas: 0110
¿Cero? True
Después de apagar: 0100
AH=BE AL=EF
Acarreo, Desborde
```

### ¿Para qué sirve?

Los permisos de un archivo, las opciones de una ventana, las teclas apretadas en un juego y las banderas de un procesador se guardan así: muchos sí o no en un solo número. C# mismo usa `[Flags]` en sus bibliotecas (por ejemplo, `FileAttributes`). Y separar un número en bytes es lo que hace cualquier programa que lee archivos o se comunica por red.

### Errores habituales

- **Preguntar con `==` en vez de con `&`:** `banderas == 0b0010` solo es verdad si es **la única** prendida. Es el **ogro** de las máscaras.
- **Prender con `=`:** `banderas = 0b0001` apaga todas las demás. Va `|=`.
- **Apagar restando:** `banderas -= 0b0010` funciona si estaba prendida, pero si estaba apagada rompe las otras. Va `&= ~`.
- **Un `[Flags]` con valores 1, 2, 3, 4:** el 3 son dos bits juntos (1 y 2), y los nombres se mezclan.

### Micro-misión S02-N03-P1 · ¿Está prendida?

```meta
lugar: La caja de las banderas
personajes: Ceci, Nova
carta: Máscara | (banderas & 0b0100) != 0 · & deja solo ese bit · != 0: está prendido
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
La bandera del signo está prendida, y Axón camina para atrás. Pero el programa de Ceci dice que no, porque también está prendida la del cero, y el `==` compara el número entero.

#### Gheco sugiere
Para mirar **un** bit, se hace `&` con una máscara que tiene solo ese bit, y se pregunta si quedó algo:

```csharp
int luces = 0b1010;
bool segunda = (luces & 0b0010) != 0;   // True, aunque haya otras prendidas
```

#### Desafío
Cambiá la pregunta para que use la máscara: `(banderas & 0b0100) != 0`.

#### Código inicial
```csharp
int banderas = 0b0110;
bool signo = banderas == 0b0100;
Console.WriteLine($"Signo: {(signo ? "sí" : "no")}");
```

#### Salida esperada
```
Signo: sí
```

#### Solución
```csharp
int banderas = 0b0110;
bool signo = (banderas & 0b0100) != 0;
Console.WriteLine($"Signo: {(signo ? "sí" : "no")}");
```

#### Al superarla
—¡Es eso! —dice Nova—. Por eso Axón camina para atrás: dio negativo. Ahora el programa lo ve.

#### Imagen
- Una caja de bronce con cuatro interruptores grandes en fila debajo de un ojo de cristal, dos encendidos en cian, sin letras ni números.
- Ceci apoya una plantilla de cartón con un solo agujero sobre la caja; Nova mira por el agujero.

### Micro-misión S02-N03-P2 · Prender sin apagar

```meta
lugar: La caja de las banderas
personajes: Ceci, Nova, Gheco
carta: Prender | banderas |= 0b0001 · | deja las otras como estaban · = las pisa todas
recompensa: xp 15, oro 15
```

#### Escena
Nova quiere prender la bandera del acarreo. Pero su programa usa `=`, y al prenderla apaga la del signo, que estaba prendida.

#### Gheco sugiere
`|` prende los bits de la máscara y deja los demás como estaban. Con `|=` se guarda en la misma variable:

```csharp
int luces = 0b1000;
luces |= 0b0010;   // 1010: la de antes sigue prendida
```

#### Desafío
Cambiá `banderas = 0b0001;` por `banderas |= 0b0001;`.

#### Código inicial
```csharp
int banderas = 0b0100;
banderas = 0b0001;
Console.WriteLine($"Banderas: {banderas:B4}");
```

#### Salida esperada
```
Banderas: 0101
```

#### Solución
```csharp
int banderas = 0b0100;
banderas |= 0b0001;
Console.WriteLine($"Banderas: {banderas:B4}");
```

#### Al superarla
Dos interruptores prendidos, como tenía que ser. Nova prende y apaga otros por las dudas, para ver que ninguno se mueve solo.

#### Imagen
- La caja de bronce con cuatro interruptores, el primero y el tercero encendidos en cian, sin letras ni números.
- Nova prende un interruptor con un dedo; Gheco, MINÚSCULO, sentado arriba de la caja, sostiene otro para que no se apague.

### Micro-misión S02-N03-P3 · Apagar sin restar

```meta
lugar: La caja de las banderas
personajes: Ceci, Nova
carta: Apagar | banderas &= ~0b0010 · ~ da vuelta la máscara · & apaga solo ese bit
recompensa: xp 15, oro 15
```

#### Escena
Nova apaga la bandera del cero restando 2. Pero la bandera ya estaba apagada, y la resta desordena las otras: ahora hay dos prendidas que no tenían que estar.

#### Gheco sugiere
`~` da vuelta la máscara (todo en 1 salvo ese bit), y `&` con eso apaga **solo** ese bit, esté como esté:

```csharp
int luces = 0b1111;
luces &= ~0b1000;   // 0111
luces &= ~0b1000;   // sigue 0111: apagar dos veces no rompe nada
```

#### Desafío
Cambiá `banderas -= 0b0010;` por `banderas &= ~0b0010;`.

#### Código inicial
```csharp
int banderas = 0b0101;
banderas -= 0b0010;
Console.WriteLine($"Banderas: {banderas:B4}");
```

#### Salida esperada
```
Banderas: 0101
```

#### Solución
```csharp
int banderas = 0b0101;
banderas &= ~0b0010;
Console.WriteLine($"Banderas: {banderas:B4}");
```

#### Al superarla
Las banderas quedan como estaban, porque la del cero ya estaba apagada. Ceci anota en su cuaderno: «apagar no es restar».

#### Imagen
- La caja de bronce con cuatro interruptores, con un trapito encima de uno apagado, sin letras ni números.
- Ceci escribe en un cuaderno apoyado en la rodilla; Nova, flotando, lee por encima de su hombro.

### Micro-misión S02-N03-P4 · Las dos mitades de AX

```meta
lugar: La sala de las palancas
personajes: Ceci, Nova, Clave
carta: Correr | ax >> 8 → la mitad alta · ax & 0xFF → la mitad baja · cada cifra hexa son 4 bits
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
La palanca AX tiene dos mitades: la de arriba, AH, y la de abajo, AL. Nova las quiere ver por separado. El programa de Ceci las calcula dividiendo por 100, y las mitades no dan.

#### Gheco sugiere
Las mitades de una palanca de 16 bits son de 8 bits cada una. Se corren con `>>` y se recortan con una máscara:

```csharp
ushort bx = 0xCAFE;
Console.WriteLine($"{bx >> 8:X2}");     // CA
Console.WriteLine($"{bx & 0xFF:X2}");   // FE
```

#### Desafío
Calculá `ah` con `ax >> 8` y `al` con `ax & 0xFF`.

#### Código inicial
```csharp
ushort ax = 0x1234;
int ah = ax / 100;
int al = ax % 100;
Console.WriteLine($"AH={ah:X2} AL={al:X2}");
```

#### Salida esperada
```
AH=12 AL=34
```

#### Solución
```csharp
ushort ax = 0x1234;
int ah = ax >> 8;
int al = ax & 0xFF;
Console.WriteLine($"AH={ah:X2} AL={al:X2}");
```

#### Al superarla
La palanca se abre en dos, como un estuche, y cada mitad muestra lo suyo. Clave asiente. —Ocho y ocho. Como dos compases.

#### Imagen
- Una palanca de bronce grande partida en dos mitades iguales que se abren como un estuche, con luces cian adentro, sin letras ni números.
- Clave, con su capa y la mecha blanca, sostiene una mitad; Ceci sostiene la otra; Nova flota en medio.

### Micro-misión S02-N03-P5 · El ogro de las banderas mezcladas

```meta
lugar: La caja de las banderas
personajes: Ceci, Nova, Gheco
criatura: ogro
carta: Ogro | [Flags]: 1, 2, 4, 8 · un bit cada uno · 3 son dos bits juntos
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un ogro rotuló las banderas con un `enum`, pero las numeró 1, 2, 3 y 4. Ahora, cuando se prenden el acarreo y el cero juntos, el programa dice «Signo», y Axón cree que dio negativo.

#### Gheco sugiere
En un `[Flags]` cada nombre tiene que ser **un solo bit**: potencias de 2. El 3 no sirve, porque es 1 + 2: dos bits juntos.

```csharp
[Flags]
enum Tecla { Ninguna = 0, Arriba = 1, Abajo = 2, Salto = 4, Fuego = 8 }
```

#### Desafío
Arreglá los valores del `enum`: `Signo` tiene que ser 4 y `Desborde`, 8.

#### Código inicial
```csharp
Bandera b = Bandera.Acarreo | Bandera.Cero;
Console.WriteLine(b);

[Flags]
enum Bandera { Ninguna = 0, Acarreo = 1, Cero = 2, Signo = 3, Desborde = 4 }
```

#### Salida esperada
```
Acarreo, Cero
```

#### Solución
```csharp
Bandera b = Bandera.Acarreo | Bandera.Cero;
Console.WriteLine(b);

[Flags]
enum Bandera { Ninguna = 0, Acarreo = 1, Cero = 2, Signo = 4, Desborde = 8 }
```

#### Al superarla
Axón deja de caminar para atrás. El ogro mira los rótulos nuevos, cuenta 1, 2, 4, 8 con los dedos y se va convencido de que fue idea suya.

#### Imagen
- La caja de bronce con cuatro interruptores con rótulos de madera sin letras, uno colgando torcido, sin letras ni números.
- El ogro grandote, con camisa cerrada, se rasca la cabeza con un rótulo en la mano; Gheco, MINÚSCULO, flota delante de su nariz.

## S02-N04 · Jefe: el Bit Rebelde

```meta
tipo: jefe
padre: S02-N03
precio: 10
criatura: dragon
insignia: Domadora de Bits
insignia_descripcion: Venciste al Bit Rebelde: entendés lo que hay debajo de C# (tipos de tamaño fijo, binario, hexadecimal y bits) y armaste un intérprete chiquito para las órdenes de Axón.
temas: maq.saltos, maq.registros
usa: prog.bits, maq.numeracion, maq.banderas, prog.enums, prog.condicionales
```

### Crónica

Una mañana, Axón se despierta y hace cosas que nadie le ordenó: suma donde tenía que mover, salta donde tenía que seguir. En la caja de las banderas, un bichito de luz roja, del tamaño de una moneda, salta de interruptor en interruptor y los da vuelta a su gusto. Es **el Bit Rebelde**: un bit que se escapó de su palanca y ahora no quiere volver.

—Cada vez que Axón lee una orden, el Bit la desordena —dice Nova, desesperada—. No puedo probar nada sin que se caiga una pared.

Ceci tiene una idea. —Entonces armamos un **Axón de mentira**, en C#. Le damos las órdenes, vemos qué haría, y recién cuando está bien se las damos al de verdad. —Gheco ya está dibujando el plan en el aire: un programa que lee las órdenes una por una y mueve palancas que son solo números.

### Objetivos

- Partir una orden escrita (`MOV AX, 5`) en sus partes con `Split`.
- Guardar las palancas en un arreglo de `ushort` y elegir cuál con un `enum` (`Enum.Parse`).
- Hacer las cuentas en 16 bits y prender la bandera del cero cuando corresponde.
- Saltar con `JNZ` (salta si no dio cero) y frenar un programa que no termina nunca.

### Antes de empezar

- Toda la Senda (S02-N01 a N03), los arreglos (R01) y el `switch` (R01).

### Explicación

#### El plan: un intérprete

Un **intérprete** lee un programa escrito, orden por orden, y hace lo que cada una dice. Python, JavaScript y el tablero del curso de Ensamblador funcionan así. El de Ceci entiende cuatro órdenes:

| Orden | Qué hace |
|---|---|
| `MOV AX, 5` | pone 5 en la palanca AX |
| `ADD AX, 5` | le suma 5 (y prende la bandera del cero si da cero) |
| `DEC CX` | le resta 1 (y lo mismo con la bandera) |
| `JNZ 2` | si la bandera del cero está apagada, salta a la orden número 2 |

#### Partir la orden

```csharp
string[] p = "MOV AX, 5".Split([' ', ','], StringSplitOptions.RemoveEmptyEntries);
// p[0] = "MOV", p[1] = "AX", p[2] = "5"
```

Se parte por espacios **y** comas, y `RemoveEmptyEntries` saca los pedazos vacíos que quedan entre la coma y el espacio.

#### Las palancas: un arreglo y un `enum`

```csharp
enum Registro { AX, BX, CX, DX }

ushort[] reg = new ushort[4];
int cual = (int)Enum.Parse<Registro>("CX");   // 2
reg[cual] = 3;
```

`Enum.Parse` convierte el texto en el valor del `enum`, y el `enum` es un número: la posición en el arreglo.

#### El bucle del intérprete

`ip` dice qué orden sigue (como el `IP` del 8086). Después de cada orden, avanza uno, salvo que la orden sea un salto:

```csharp
int ip = 0;
while (ip < programa.Length)
{
    string[] p = programa[ip].Split([' ', ','], StringSplitOptions.RemoveEmptyEntries);
    switch (p[0])
    {
        case "MOV": /* ... */ break;
        case "JNZ":
            if ((banderas & Bandera.Cero) == 0)
            {
                ip = int.Parse(p[1]);
                continue;   // vuelve al while sin el ip++
            }
            break;
    }
    ip++;
}
```

### Código de ejemplo

```csharp
string[] programa = ["MOV CX, 3", "MOV AX, 0", "ADD AX, 5", "DEC CX", "JNZ 2"];

ushort[] reg = new ushort[4];
Bandera banderas = Bandera.Ninguna;
int ip = 0;

while (ip < programa.Length)
{
    string[] p = programa[ip].Split([' ', ','], StringSplitOptions.RemoveEmptyEntries);
    int d = p.Length > 1 && p[0] != "JNZ" ? (int)Enum.Parse<Registro>(p[1]) : 0;
    switch (p[0])
    {
        case "MOV":
            reg[d] = ushort.Parse(p[2]);
            break;
        case "ADD":
            reg[d] = (ushort)(reg[d] + ushort.Parse(p[2]));
            MarcarCero(reg[d]);
            break;
        case "DEC":
            reg[d]--;
            MarcarCero(reg[d]);
            break;
        case "JNZ":
            if ((banderas & Bandera.Cero) == 0)
            {
                ip = int.Parse(p[1]);
                continue;
            }
            break;
    }
    ip++;
}

Console.WriteLine($"AX={reg[(int)Registro.AX]:X4} CX={reg[(int)Registro.CX]:X4}");

void MarcarCero(ushort valor)
{
    if (valor == 0)
    {
        banderas |= Bandera.Cero;
    }
    else
    {
        banderas &= ~Bandera.Cero;
    }
}

enum Registro { AX, BX, CX, DX }

[Flags]
enum Bandera { Ninguna = 0, Acarreo = 1, Cero = 2, Signo = 4, Desborde = 8 }
```

### Salida esperada

```
AX=000F CX=0000
```

### ¿Para qué sirve?

Así funciona por dentro cualquier lenguaje que se interpreta, y también los emuladores de consolas viejas: leen una orden, la hacen, avanzan. Armar uno chiquito es la mejor forma de entender que un `while` o un `if` son, por debajo, una cuenta, una bandera y un salto.

### Errores habituales

- **Partir solo por espacios:** `"MOV AX, 5".Split(' ')` deja `"AX,"` con la coma pegada, y `Enum.Parse` se rompe.
- **Olvidarse del `continue` en el salto:** el `ip++` de abajo se suma igual y el programa salta una orden de más.
- **Dar vuelta la condición del salto:** `JNZ` salta cuando la bandera del cero está **apagada**.
- **Un programa que nunca termina:** si nada pone la bandera en cero, `JNZ` salta para siempre. Un intérprete serio cuenta los pasos y frena.

### Micro-misión S02-N04-P1 · Partir la orden

```meta
lugar: La caja de las banderas
personajes: Ceci, Nova, Gheco
criatura: dragon
carta: Jefe | Split([' ', ','], StringSplitOptions.RemoveEmptyEntries) · parte por espacios y comas · saca los vacíos
recompensa: xp 25, oro 25
```

#### Escena
El Bit Rebelde se esconde en las comas: cada vez que Ceci parte una orden solo por los espacios, la coma queda pegada al nombre de la palanca, y el Bit se ríe desde adentro de `"AX,"`.

#### Gheco sugiere
`Split` acepta varios separadores a la vez. Con `RemoveEmptyEntries` no quedan pedazos vacíos entre la coma y el espacio:

```csharp
string[] partes = "la, si; do".Split([',', ';', ' '], StringSplitOptions.RemoveEmptyEntries);
// "la", "si", "do"
```

#### Desafío
Partí `orden` por espacios **y** comas, sacando los vacíos.

#### Código inicial
```csharp
string orden = "MOV AX, 5";
string[] p = orden.Split(' ');
Console.WriteLine($"orden={p[0]} destino={p[1]} valor={p[2]}");
```

#### Salida esperada
```
orden=MOV destino=AX valor=5
```

#### Solución
```csharp
string orden = "MOV AX, 5";
string[] p = orden.Split([' ', ','], StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"orden={p[0]} destino={p[1]} valor={p[2]}");
```

#### Al superarla
La coma cae sola al piso, y el Bit Rebelde, que estaba adentro, sale rodando. Se sacude, enojado, y salta a otra palanca.

#### Imagen
- La caja de bronce de los interruptores debajo del ojo de cristal, con chispas rojas saltando, sin letras ni números.
- Un bichito de luz roja del tamaño de una moneda, con forma de interruptor y patitas, sale rodando; Ceci lo señala; Nova flota detrás; Gheco, MINÚSCULO, en el hombro de Ceci.

### Micro-misión S02-N04-P2 · Cada palanca en su lugar

```meta
lugar: La sala de las palancas
personajes: Ceci, Nova
criatura: dragon
carta: Jefe | Enum.Parse<Registro>("BX") → Registro.BX · (int) lo vuelve posición · reg[posición]
recompensa: xp 25, oro 25
```

#### Escena
El Bit Rebelde cambió la orden `MOV`: ahora siempre escribe en la primera palanca, sin importar cuál diga la orden. `MOV BX, 7` termina en AX, y BX queda en cero.

#### Gheco sugiere
El nombre de la palanca viene como texto. `Enum.Parse` lo convierte en el `enum`, y el `enum` convertido a `int` es la posición en el arreglo:

```csharp
int donde = (int)Enum.Parse<Registro>("DX");   // 3
```

#### Desafío
En el `MOV`, cambiá `reg[0]` por `reg[(int)Enum.Parse<Registro>(p[1])]`.

#### Código inicial
```csharp
string[] programa = ["MOV AX, 5", "MOV BX, 7"];
ushort[] reg = new ushort[4];

foreach (string linea in programa)
{
    string[] p = linea.Split([' ', ','], StringSplitOptions.RemoveEmptyEntries);
    if (p[0] == "MOV")
    {
        reg[0] = ushort.Parse(p[2]);
    }
}

Console.WriteLine($"AX={reg[0]:X4} BX={reg[1]:X4}");

enum Registro { AX, BX, CX, DX }
```

#### Salida esperada
```
AX=0005 BX=0007
```

#### Solución
```csharp
string[] programa = ["MOV AX, 5", "MOV BX, 7"];
ushort[] reg = new ushort[4];

foreach (string linea in programa)
{
    string[] p = linea.Split([' ', ','], StringSplitOptions.RemoveEmptyEntries);
    if (p[0] == "MOV")
    {
        reg[(int)Enum.Parse<Registro>(p[1])] = ushort.Parse(p[2]);
    }
}

Console.WriteLine($"AX={reg[0]:X4} BX={reg[1]:X4}");

enum Registro { AX, BX, CX, DX }
```

#### Al superarla
Cada palanca baja hasta su número. El Bit Rebelde intenta empujar BX de vuelta a cero, pero ya no le alcanza la fuerza.

#### Imagen
- Cuatro palancas de bronce grandes en fila, dos bajadas a distinta altura con luces cian, sin letras ni números.
- El bichito de luz roja empuja una palanca con todo el cuerpo, sin moverla; Nova flota con las manos en la cintura; Ceci sonríe.

### Micro-misión S02-N04-P3 · La bandera que no se apaga

```meta
lugar: La caja de las banderas
personajes: Ceci, Nova, Gheco
criatura: dragon
carta: Jefe | si da 0: banderas |= Cero · si no: banderas &= ~Cero · la bandera siempre dice la última cuenta
recompensa: xp 25, oro 25
```

#### Escena
AX llega al tope, se le suma 1 y da la vuelta a cero: la bandera del cero se prende, bien. Pero después se le suma 2, y la bandera sigue prendida. El Bit Rebelde está sentado encima, y no la deja apagarse.

#### Gheco sugiere
La bandera tiene que contar la **última** cuenta. Si dio cero, se prende; si no, se apaga. Falta la otra mitad:

```csharp
if (nivel == 0) { avisos |= Aviso.Vacio; }
else { avisos &= ~Aviso.Vacio; }
```

#### Desafío
Agregale a `MarcarCero` un `else` que apague la bandera con `banderas &= ~Bandera.Cero;`.

#### Código inicial
```csharp
ushort ax = 65535;
Bandera banderas = Bandera.Ninguna;

ax = (ushort)(ax + 1);
MarcarCero(ax);
ax = (ushort)(ax + 2);
MarcarCero(ax);

int zf = (banderas & Bandera.Cero) != 0 ? 1 : 0;
Console.WriteLine($"AX={ax:X4} ZF={zf}");

void MarcarCero(ushort valor)
{
    if (valor == 0)
    {
        banderas |= Bandera.Cero;
    }
}

[Flags]
enum Bandera { Ninguna = 0, Acarreo = 1, Cero = 2, Signo = 4, Desborde = 8 }
```

#### Salida esperada
```
AX=0002 ZF=0
```

#### Solución
```csharp
ushort ax = 65535;
Bandera banderas = Bandera.Ninguna;

ax = (ushort)(ax + 1);
MarcarCero(ax);
ax = (ushort)(ax + 2);
MarcarCero(ax);

int zf = (banderas & Bandera.Cero) != 0 ? 1 : 0;
Console.WriteLine($"AX={ax:X4} ZF={zf}");

void MarcarCero(ushort valor)
{
    if (valor == 0)
    {
        banderas |= Bandera.Cero;
    }
    else
    {
        banderas &= ~Bandera.Cero;
    }
}

[Flags]
enum Bandera { Ninguna = 0, Acarreo = 1, Cero = 2, Signo = 4, Desborde = 8 }
```

#### Al superarla
La bandera se apaga de golpe y el Bit Rebelde sale despedido por el aire. Cae arriba de la caja, mareado, y se esconde detrás de un tornillo.

#### Imagen
- La caja de bronce de los interruptores, con uno que se apaga y una chispa roja que sale volando, sin letras ni números.
- El bichito de luz roja da vueltas en el aire, mareado; Nova se ríe tapándose la boca; Gheco, MINÚSCULO, festeja con los brazos arriba.

### Micro-misión S02-N04-P4 · El salto al revés

```meta
lugar: El núcleo del Gólem
personajes: Ceci, Nova, Clave
criatura: dragon
carta: Jefe | JNZ: salta si el cero está APAGADO · (banderas & Bandera.Cero) == 0 · continue: sin el ip++
recompensa: xp 25, oro 25, monedas 3
```

#### Escena
Nova quiere que Axón sume 5 tres veces, con un bucle: CX cuenta hacia abajo y `JNZ` vuelve atrás mientras CX no llegue a cero. Pero el Bit Rebelde dio vuelta la condición del salto: ahora salta solo cuando dio cero, y el bucle da una sola vuelta.

#### Gheco sugiere
`JNZ` quiere decir *Jump if Not Zero*: salta si la última cuenta **no** dio cero, o sea, si la bandera está **apagada**:

```csharp
bool apagada = (banderas & Bandera.Signo) == 0;   // == 0: el bit no está
```

#### Desafío
En el `JNZ`, cambiá `!= 0` por `== 0`.

#### Código inicial
```csharp
string[] programa = ["MOV CX, 3", "MOV AX, 0", "ADD AX, 5", "DEC CX", "JNZ 2"];

ushort[] reg = new ushort[4];
Bandera banderas = Bandera.Ninguna;
int ip = 0;

while (ip < programa.Length)
{
    string[] p = programa[ip].Split([' ', ','], StringSplitOptions.RemoveEmptyEntries);
    int d = p.Length > 1 && p[0] != "JNZ" ? (int)Enum.Parse<Registro>(p[1]) : 0;
    switch (p[0])
    {
        case "MOV":
            reg[d] = ushort.Parse(p[2]);
            break;
        case "ADD":
            reg[d] = (ushort)(reg[d] + ushort.Parse(p[2]));
            MarcarCero(reg[d]);
            break;
        case "DEC":
            reg[d]--;
            MarcarCero(reg[d]);
            break;
        case "JNZ":
            if ((banderas & Bandera.Cero) != 0)
            {
                ip = int.Parse(p[1]);
                continue;
            }
            break;
    }
    ip++;
}

Console.WriteLine($"AX={reg[(int)Registro.AX]:X4} CX={reg[(int)Registro.CX]:X4}");

void MarcarCero(ushort valor)
{
    if (valor == 0)
    {
        banderas |= Bandera.Cero;
    }
    else
    {
        banderas &= ~Bandera.Cero;
    }
}

enum Registro { AX, BX, CX, DX }

[Flags]
enum Bandera { Ninguna = 0, Acarreo = 1, Cero = 2, Signo = 4, Desborde = 8 }
```

#### Salida esperada
```
AX=000F CX=0000
```

#### Solución
```csharp
string[] programa = ["MOV CX, 3", "MOV AX, 0", "ADD AX, 5", "DEC CX", "JNZ 2"];

ushort[] reg = new ushort[4];
Bandera banderas = Bandera.Ninguna;
int ip = 0;

while (ip < programa.Length)
{
    string[] p = programa[ip].Split([' ', ','], StringSplitOptions.RemoveEmptyEntries);
    int d = p.Length > 1 && p[0] != "JNZ" ? (int)Enum.Parse<Registro>(p[1]) : 0;
    switch (p[0])
    {
        case "MOV":
            reg[d] = ushort.Parse(p[2]);
            break;
        case "ADD":
            reg[d] = (ushort)(reg[d] + ushort.Parse(p[2]));
            MarcarCero(reg[d]);
            break;
        case "DEC":
            reg[d]--;
            MarcarCero(reg[d]);
            break;
        case "JNZ":
            if ((banderas & Bandera.Cero) == 0)
            {
                ip = int.Parse(p[1]);
                continue;
            }
            break;
    }
    ip++;
}

Console.WriteLine($"AX={reg[(int)Registro.AX]:X4} CX={reg[(int)Registro.CX]:X4}");

void MarcarCero(ushort valor)
{
    if (valor == 0)
    {
        banderas |= Bandera.Cero;
    }
    else
    {
        banderas &= ~Bandera.Cero;
    }
}

enum Registro { AX, BX, CX, DX }

[Flags]
enum Bandera { Ninguna = 0, Acarreo = 1, Cero = 2, Signo = 4, Desborde = 8 }
```

#### Al superarla
El Axón de mentira suma tres veces y frena justo en quince. Nova le da el mismo programa al de verdad: Axón levanta el brazo tres veces, despacio, y lo baja. Clave aplaude una sola vez, que en ella es mucho.

#### Imagen
- El núcleo del Gólem, una cámara redonda de bronce con un corazón de luz cian en el centro y engranajes alrededor, sin letras ni números.
- Nova flota frente al núcleo con los brazos abiertos; Clave, con su capa y la mecha blanca, aplaude; el bichito de luz roja huye por un engranaje.

### Micro-misión S02-N04-P5 · El bucle sin fin

```meta
lugar: El núcleo del Gólem
personajes: Ceci, Nova, Gheco
criatura: dragon
carta: Jefe | contar los pasos · si pasa el tope, frenar con break · un intérprete nunca se cuelga
recompensa: xp 30, oro 30, monedas 3
```

#### Escena
Su última trampa: el Bit Rebelde le da a Axón un programa que salta para siempre, porque nada pone la bandera del cero. Si el intérprete no frena, la pantalla de Ceci se cuelga, y Axón caminaría hasta chocar contra la montaña.

#### Gheco sugiere
Un intérprete serio **cuenta los pasos** y, si pasa un tope, frena con un aviso. El tablero de Ensamblador hace lo mismo:

```csharp
int vueltas = 0;
while (true)
{
    vueltas++;
    if (vueltas > 100) { Console.WriteLine("Basta."); break; }
}
```

#### Desafío
Adentro del `while`, antes de partir la orden, sumá 1 a `pasos`. Si `pasos` pasa de `1000`, mostrá `¡Alto! El Bit Rebelde metió un bucle sin fin` y cortá con `break`.

#### Código inicial
```csharp
string[] programa = ["MOV AX, 1", "ADD AX, 1", "JNZ 1"];

ushort[] reg = new ushort[4];
Bandera banderas = Bandera.Ninguna;
int ip = 0;
int pasos = 0;

while (ip < programa.Length)
{
    // contá el paso y frená si pasa de 1000

    string[] p = programa[ip].Split([' ', ','], StringSplitOptions.RemoveEmptyEntries);
    int d = p.Length > 1 && p[0] != "JNZ" ? (int)Enum.Parse<Registro>(p[1]) : 0;
    switch (p[0])
    {
        case "MOV":
            reg[d] = ushort.Parse(p[2]);
            break;
        case "ADD":
            reg[d] = (ushort)(reg[d] + ushort.Parse(p[2]));
            MarcarCero(reg[d]);
            break;
        case "JNZ":
            if ((banderas & Bandera.Cero) == 0)
            {
                ip = int.Parse(p[1]);
                continue;
            }
            break;
    }
    ip++;
}

Console.WriteLine($"AX={reg[(int)Registro.AX]:X4}");

void MarcarCero(ushort valor)
{
    if (valor == 0)
    {
        banderas |= Bandera.Cero;
    }
    else
    {
        banderas &= ~Bandera.Cero;
    }
}

enum Registro { AX, BX, CX, DX }

[Flags]
enum Bandera { Ninguna = 0, Acarreo = 1, Cero = 2, Signo = 4, Desborde = 8 }
```

#### Salida esperada
```
¡Alto! El Bit Rebelde metió un bucle sin fin
AX=01F5
```

#### Solución
```csharp
string[] programa = ["MOV AX, 1", "ADD AX, 1", "JNZ 1"];

ushort[] reg = new ushort[4];
Bandera banderas = Bandera.Ninguna;
int ip = 0;
int pasos = 0;

while (ip < programa.Length)
{
    pasos++;
    if (pasos > 1000)
    {
        Console.WriteLine("¡Alto! El Bit Rebelde metió un bucle sin fin");
        break;
    }

    string[] p = programa[ip].Split([' ', ','], StringSplitOptions.RemoveEmptyEntries);
    int d = p.Length > 1 && p[0] != "JNZ" ? (int)Enum.Parse<Registro>(p[1]) : 0;
    switch (p[0])
    {
        case "MOV":
            reg[d] = ushort.Parse(p[2]);
            break;
        case "ADD":
            reg[d] = (ushort)(reg[d] + ushort.Parse(p[2]));
            MarcarCero(reg[d]);
            break;
        case "JNZ":
            if ((banderas & Bandera.Cero) == 0)
            {
                ip = int.Parse(p[1]);
                continue;
            }
            break;
    }
    ip++;
}

Console.WriteLine($"AX={reg[(int)Registro.AX]:X4}");

void MarcarCero(ushort valor)
{
    if (valor == 0)
    {
        banderas |= Bandera.Cero;
    }
    else
    {
        banderas &= ~Bandera.Cero;
    }
}

enum Registro { AX, BX, CX, DX }

[Flags]
enum Bandera { Ninguna = 0, Acarreo = 1, Cero = 2, Signo = 4, Desborde = 8 }
```

#### Al superarla
El intérprete frena en el paso mil y muestra el aviso. El Bit Rebelde, sin bucle donde esconderse, se queda quieto en el medio del núcleo, chiquito y colorado. Nova lo junta con las dos manos y lo devuelve a su palanca, donde encaja con un clic. Axón da un paso, uno solo, perfecto. —Lo hiciste vos —le dice Nova a Ceci—. Bueno: lo hicimos.

#### Imagen
- El núcleo del Gólem con su corazón de luz cian, ahora tranquilo, y una palanca con un clic de luz roja que encaja en su lugar, sin letras ni números.
- Nova sostiene con las dos manos el bichito de luz roja, ya manso; Ceci sonríe con el violín al hombro; Gheco, MINÚSCULO, en el hombro de Ceci, levanta el pulgar.
