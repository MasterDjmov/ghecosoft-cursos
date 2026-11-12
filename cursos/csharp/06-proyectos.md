# RAMA R06 · Proyectos: la Arena y el Libro Mayor

```meta
tipo: tronco
posicion: 6
```

## R06-N01 · Proyecto: la Arena, las piezas

```meta
tipo: tema
padre: R05-N08
precio: 10
criatura: ogro
temas: juegos.turnos
usa: poo.herencia, poo.abstractas, poo.polimorfismo, poo.encapsulamiento, col.mapas
```

### Crónica

Con la ventanilla en silencio, {mentor} lleva a Ceci al fondo del Conservatorio, donde nunca la dejaron pasar: una **arena redonda** de piedra, con gradas de madera y atriles alrededor, como un teatro para pelear.

—Acá se rinde el último examen —dice—. No es una partitura: es un **juego entero**. Un héroe, una oleada de monstruos y, al final, el que se despierta cuando alguien entra a la Arena: **el Dragón del Conservatorio**. Escupe fuego cada tres compases.

Bemol se sienta en la primera grada con una bolsa de garrapiñadas. —Yo vine a mirar.

—Un juego grande no se escribe de un tirón —sigue {mentor}—. Se arma **por piezas**, y cada pieza se ensaya sola. Empezamos por los que pelean.

### Objetivos

- Armar un programa grande **por piezas**, cada una con su responsabilidad.
- Usar una **clase abstracta** como molde común de héroes y monstruos.
- Proteger los datos con `private set` y cuidar los **bordes** con `Math.Min` y `Math.Max`.
- Cambiar el comportamiento de cada monstruo con `virtual` y `override`.

### Antes de empezar

- Clases, propiedades y constructores (Acto II), herencia, `abstract` y polimorfismo (R02-N07 y R02-N08), `Dictionary` (R03-N01).

### Explicación

#### Un programa grande, hecho de piezas chicas

En este proyecto vas a armar **la Arena**: un juego por turnos donde Ceci pelea contra una oleada de monstruos. Es el programa más largo del curso, pero no tiene nada que no sepas: son las piezas de los actos anteriores, **juntas**.

Las piezas de este nodo son **los que pelean**:

```
Entidad (abstracta)      lo que tienen todos: nombre, vida, ataque, recibir daño, curarse, la barra
 ├─ Heroe                 Ceci: además, maná y una mochila
 └─ Monstruo (abstracta)  además, cuánto oro deja y cómo elige su golpe
     ├─ Goblin             el más simple: no cambia nada
     ├─ Ogro               su piel absorbe 2 de cada golpe
     └─ Dragon             cada tres turnos, escupe fuego (pega el doble)
```

En el nodo que sigue llegan las **acciones** (espada, fuego, poción) y la **partida**, que los hace pelear por turnos.

#### El molde común: una clase abstracta

`Entidad` es **abstracta**: no existe "una entidad" suelta, existen héroes y monstruos. Pero todos tienen vida y reciben daño, así que eso se escribe **una sola vez**, en el molde:

```csharp
abstract class Entidad
{
    public string Nombre { get; }
    public int VidaMaxima { get; }
    public int Vida { get; private set; }
    public bool EstaViva => Vida > 0;
    ...
}
```

- `{ get; }`: se lee desde afuera, y solo se escribe en el constructor.
- `{ get; private set; }`: se lee desde afuera, pero **solo la propia clase** la cambia. Nadie puede escribir `goblin.Vida = 1000` desde el programa: para cambiar la vida hay que pasar por `RecibirDanio` o `Curar`, que cuidan las reglas.
- `EstaViva => Vida > 0`: una propiedad **calculada**. No se guarda: se averigua cada vez que se pregunta.

#### Los bordes

Los errores más comunes de un juego están en los **bordes**: la vida que baja de cero, la poción que cura más que el máximo, la barra que se pasa de largo. Dos herramientas los cuidan:

| Quiero… | Uso | Ejemplo |
|---|---|---|
| que no pase de un máximo | `Math.Min(valor, maximo)` | `Math.Min(70 + 40, 100)` da `100` |
| que no baje de un mínimo | `Math.Max(valor, minimo)` | `Math.Max(1 - 2, 1)` da `1` |

`Math.Min` devuelve **el más chico** de los dos, y `Math.Max`, **el más grande**. Parece al revés, pero pensalo así: para que algo **no pase** de 100, me quedo con el más chico entre el valor y 100.

#### Cada monstruo, con su voz

`RecibirDanio` está escrito en `Entidad` con `virtual`: quiere decir "esta es la forma normal, pero una clase hija la puede cambiar". El ogro la cambia con `override`, y adentro llama a la normal con `base`:

```csharp
class Ogro : Monstruo
{
    public Ogro() : base("Ogro", 60, 9, 25) { }

    public override int RecibirDanio(int cantidad) => base.RecibirDanio(Math.Max(cantidad - 2, 1));
}
```

Lo bueno: el resto del programa **no sabe** qué monstruo tiene adelante. Le dice `enemigo.RecibirDanio(10)` a cualquiera, y cada uno responde a su manera. Eso es el **polimorfismo**: agregar un monstruo nuevo no obliga a tocar el combate.

#### La barra de vida

Para dibujar la vida se usan dos trucos de texto:

- `new string('#', 12)` arma un texto con 12 numerales: `############`.
- `{Nombre,-8}` adentro de un `$"…"` ocupa **8 lugares**, alineado a la izquierda (con `8` sin el menos, a la derecha). Así las barras quedan una debajo de la otra.

Y una cuenta: la barra tiene 20 lugares, entonces los llenos son `Vida * 20 / VidaMaxima` (una regla de tres, con división entera).

### Código de ejemplo

```csharp
List<Entidad> arena = [new Heroe("Ceci"), new Goblin(), new Ogro(), new Dragon()];

foreach (Entidad e in arena)
{
    e.RecibirDanio(10);
    Console.WriteLine(e.Barra());
}

abstract class Entidad
{
    public string Nombre { get; }
    public int VidaMaxima { get; }
    public int Vida { get; private set; }
    public int Ataque { get; }
    public bool EstaViva => Vida > 0;

    protected Entidad(string nombre, int vida, int ataque)
    {
        Nombre = nombre;
        VidaMaxima = vida;
        Vida = vida;
        Ataque = ataque;
    }

    public virtual int RecibirDanio(int cantidad)
    {
        int real = Math.Min(cantidad, Vida);
        Vida -= real;
        return real;
    }

    public void Curar(int cantidad)
    {
        Vida = Math.Min(Vida + cantidad, VidaMaxima);
    }

    public string Barra()
    {
        int llenos = Vida * 20 / VidaMaxima;
        return $"{Nombre,-8}[{new string('#', llenos),-20}] {Vida}/{VidaMaxima}";
    }
}

class Heroe : Entidad
{
    public int Mana { get; private set; } = 30;

    public Heroe(string nombre) : base(nombre, 100, 12) { }
}

abstract class Monstruo : Entidad
{
    public int Recompensa { get; }

    protected Monstruo(string nombre, int vida, int ataque, int recompensa) : base(nombre, vida, ataque)
    {
        Recompensa = recompensa;
    }

    public virtual int ElegirGolpe(int turno) => Ataque;
}

class Goblin : Monstruo
{
    public Goblin() : base("Goblin", 30, 5, 10) { }
}

class Ogro : Monstruo
{
    public Ogro() : base("Ogro", 60, 9, 25) { }

    public override int RecibirDanio(int cantidad) => base.RecibirDanio(Math.Max(cantidad - 2, 1));
}

class Dragon : Monstruo
{
    public Dragon() : base("Dragón", 90, 10, 100) { }

    public override int ElegirGolpe(int turno) => turno % 3 == 0 ? Ataque * 2 : Ataque;
}
```

### Salida esperada

```
Ceci    [##################  ] 90/100
Goblin  [#############       ] 20/30
Ogro    [#################   ] 52/60
Dragón  [#################   ] 80/90
```

### ¿Para qué sirve?

Así se arma cualquier juego, en consola o en **Unity** y **Godot**: una clase base para todo lo que tiene vida, y una hija por cada enemigo, cada una con su comportamiento. Agregar el enemigo número cincuenta es escribir una clase más, sin tocar las otras cuarenta y nueve.

### Errores habituales

- **Cambiar la vida desde afuera:** `goblin.Vida = 0;` no compila (CS0272) por el `private set`. Es a propósito: para cambiarla, `RecibirDanio` o `Curar`.
- **Olvidar el `override`:** si el ogro escribe `public int RecibirDanio(...)` sin `override`, C# avisa (CS0114) y, cuando el combate lo trate como `Entidad`, se usa la versión común. La piel no absorbe nada.
- **Los bordes:** una poción que cura más que el máximo, una barra con más de 20 `#`. Por eso `Math.Min`.
- **`new Entidad(...)`:** no compila (CS0144): una clase abstracta no se puede crear. Se crea un `Heroe` o un `Goblin`.

### Micro-misión R06-N01-P1 · La barra de vida

```meta
lugar: La Arena del Conservatorio
personajes: Ceci, Clave
carta: La barra | llenos = Vida * 20 / VidaMaxima · new string('#', n) repite · {Nombre,-8} ocupa 8 lugares
recompensa: xp 20, oro 20, monedas 4
```

#### Escena
En el pizarrón de la Arena, la barra del goblin se sale del cuadro: tiene 30 numerales, y el cuadro es de 20.

#### Gheco sugiere
La barra tiene **20 lugares**, pero el goblin tiene 30 de vida. Si ponés un `#` por cada punto de vida, no entra. Hay que hacer una **regla de tres**: si la vida máxima llena los 20 lugares, la vida actual llena

```csharp
int llenos = Vida * 20 / VidaMaxima;
```

Con 30 de 30, da 20; con 18 de 30, da 12. Primero se multiplica y después se divide: al revés, `18 / 30` da 0 (división entera) y la barra quedaría vacía.

#### Desafío
Cambiá la cuenta de `llenos` para que la barra nunca pase de 20 lugares.

#### Código inicial
```csharp
Goblin goblin = new Goblin();
Console.WriteLine(goblin.Barra());
goblin.RecibirDanio(12);
Console.WriteLine(goblin.Barra());
goblin.RecibirDanio(50);
Console.WriteLine(goblin.Barra());

abstract class Entidad
{
    public string Nombre { get; }
    public int VidaMaxima { get; }
    public int Vida { get; private set; }

    protected Entidad(string nombre, int vida)
    {
        Nombre = nombre;
        VidaMaxima = vida;
        Vida = vida;
    }

    public int RecibirDanio(int cantidad)
    {
        int real = Math.Min(cantidad, Vida);
        Vida -= real;
        return real;
    }

    public string Barra()
    {
        int llenos = Vida;
        return $"{Nombre,-8}[{new string('#', llenos),-20}] {Vida}/{VidaMaxima}";
    }
}

class Goblin : Entidad
{
    public Goblin() : base("Goblin", 30) { }
}
```

#### Salida esperada
```
Goblin  [####################] 30/30
Goblin  [############        ] 18/30
Goblin  [                    ] 0/30
```

#### Solución
```csharp
Goblin goblin = new Goblin();
Console.WriteLine(goblin.Barra());
goblin.RecibirDanio(12);
Console.WriteLine(goblin.Barra());
goblin.RecibirDanio(50);
Console.WriteLine(goblin.Barra());

abstract class Entidad
{
    public string Nombre { get; }
    public int VidaMaxima { get; }
    public int Vida { get; private set; }

    protected Entidad(string nombre, int vida)
    {
        Nombre = nombre;
        VidaMaxima = vida;
        Vida = vida;
    }

    public int RecibirDanio(int cantidad)
    {
        int real = Math.Min(cantidad, Vida);
        Vida -= real;
        return real;
    }

    public string Barra()
    {
        int llenos = Vida * 20 / VidaMaxima;
        return $"{Nombre,-8}[{new string('#', llenos),-20}] {Vida}/{VidaMaxima}";
    }
}

class Goblin : Entidad
{
    public Goblin() : base("Goblin", 30) { }
}
```

#### Al superarla
La barra entra justo en el cuadro. —Veinte lugares —dice {mentor}—. Ni uno más. Los bordes son donde se esconden los ogros.

#### Imagen
- Una arena redonda de piedra con gradas de madera y atriles alrededor, de noche, con faroles; en el centro, un pizarrón grande con una barra horizontal dividida en cuadraditos iguales, sin letras ni números.
- Clave señala el pizarrón con la batuta; Ceci, con su violín en la espalda, mira la barra.

### Micro-misión R06-N01-P2 · Curar sin pasarse

```meta
lugar: La Arena del Conservatorio
personajes: Ceci, Bemol
carta: Math.Min | Math.Min(a, b) da el más chico · Vida = Math.Min(Vida + cantidad, VidaMaxima) · nunca pasa del máximo
recompensa: xp 20, oro 20
```

#### Escena
Bemol prueba la poción de la Arena con Ceci herida, y Ceci queda con 110 de vida sobre 100. Su barra se sale del cuadro.

#### Gheco sugiere
`Curar` suma sin mirar el techo. Para que la vida **no pase** de `VidaMaxima`, quedate con el más chico entre la vida curada y el máximo:

```csharp
Vida = Math.Min(Vida + cantidad, VidaMaxima);
```

Si Ceci tiene 70 y la poción cura 40: `Math.Min(110, 100)` da `100`. Si tiene 30: `Math.Min(70, 100)` da `70`. En los dos casos, lo justo.

#### Desafío
Usá `Math.Min` en `Curar` para que la vida nunca pase de la máxima.

#### Código inicial
```csharp
Heroe ceci = new Heroe("Ceci");
ceci.RecibirDanio(30);
Console.WriteLine(ceci.Barra());
ceci.Curar(40);
Console.WriteLine(ceci.Barra());
ceci.RecibirDanio(70);
ceci.Curar(40);
Console.WriteLine(ceci.Barra());

abstract class Entidad
{
    public string Nombre { get; }
    public int VidaMaxima { get; }
    public int Vida { get; private set; }

    protected Entidad(string nombre, int vida)
    {
        Nombre = nombre;
        VidaMaxima = vida;
        Vida = vida;
    }

    public int RecibirDanio(int cantidad)
    {
        int real = Math.Min(cantidad, Vida);
        Vida -= real;
        return real;
    }

    public void Curar(int cantidad)
    {
        Vida = Vida + cantidad;
    }

    public string Barra()
    {
        int llenos = Vida * 20 / VidaMaxima;
        return $"{Nombre,-8}[{new string('#', llenos),-20}] {Vida}/{VidaMaxima}";
    }
}

class Heroe : Entidad
{
    public Heroe(string nombre) : base(nombre, 100) { }
}
```

#### Salida esperada
```
Ceci    [##############      ] 70/100
Ceci    [####################] 100/100
Ceci    [##############      ] 70/100
```

#### Solución
```csharp
Heroe ceci = new Heroe("Ceci");
ceci.RecibirDanio(30);
Console.WriteLine(ceci.Barra());
ceci.Curar(40);
Console.WriteLine(ceci.Barra());
ceci.RecibirDanio(70);
ceci.Curar(40);
Console.WriteLine(ceci.Barra());

abstract class Entidad
{
    public string Nombre { get; }
    public int VidaMaxima { get; }
    public int Vida { get; private set; }

    protected Entidad(string nombre, int vida)
    {
        Nombre = nombre;
        VidaMaxima = vida;
        Vida = vida;
    }

    public int RecibirDanio(int cantidad)
    {
        int real = Math.Min(cantidad, Vida);
        Vida -= real;
        return real;
    }

    public void Curar(int cantidad)
    {
        Vida = Math.Min(Vida + cantidad, VidaMaxima);
    }

    public string Barra()
    {
        int llenos = Vida * 20 / VidaMaxima;
        return $"{Nombre,-8}[{new string('#', llenos),-20}] {Vida}/{VidaMaxima}";
    }
}

class Heroe : Entidad
{
    public Heroe(string nombre) : base(nombre, 100) { }
}
```

#### Al superarla
—Cien sobre cien —dice Bemol, y prueba otra poción por las dudas. Sigue en cien—. Qué aburrido. Qué bien.

#### Imagen
- Las gradas de madera de una arena de piedra con faroles, sin letras.
- Bemol, gordito y con panza, levanta un frasquito de poción roja contra la luz; Ceci, a su lado, se ríe.

### Micro-misión R06-N01-P3 · La piel del ogro

```meta
lugar: La Arena del Conservatorio
personajes: Ceci, Clave
carta: override | public override int RecibirDanio(int cantidad) · base.RecibirDanio(…) llama a la común · cada monstruo con su voz
recompensa: xp 20, oro 20
```

#### Escena
Al ogro de la Arena le entran los golpes igual que al goblin, y eso no puede ser: tiene la piel gruesa.

#### Gheco sugiere
`RecibirDanio` está marcado `virtual` en `Entidad`: es la forma común, pero una hija la puede cambiar. Escribila de nuevo en `Ogro`, con `override`, y adentro llamá a la común con `base`, pero con 2 menos:

```csharp
public override int RecibirDanio(int cantidad) => base.RecibirDanio(Math.Max(cantidad - 2, 1));
```

El `Math.Max(…, 1)` es el borde de abajo: un golpe de 1 no puede curar al ogro (daría `-1`), así que siempre entra **por lo menos 1**.

Fijate que el `foreach` recorre una lista de `Entidad`, y aun así el ogro usa **su** versión. Eso es el polimorfismo.

#### Desafío
Agregale a `Ogro` el `override` de `RecibirDanio` que le quita 2 a cada golpe, sin bajar de 1.

#### Código inicial
```csharp
List<Entidad> grupo = [new Goblin(), new Ogro()];

foreach (int golpe in new[] { 10, 1 })
{
    foreach (Entidad e in grupo)
    {
        int real = e.RecibirDanio(golpe);
        Console.WriteLine($"{e.Nombre} recibe {real}: le quedan {e.Vida}");
    }
}

abstract class Entidad
{
    public string Nombre { get; }
    public int Vida { get; private set; }

    protected Entidad(string nombre, int vida)
    {
        Nombre = nombre;
        Vida = vida;
    }

    public virtual int RecibirDanio(int cantidad)
    {
        int real = Math.Min(cantidad, Vida);
        Vida -= real;
        return real;
    }
}

class Goblin : Entidad
{
    public Goblin() : base("Goblin", 30) { }
}

class Ogro : Entidad
{
    public Ogro() : base("Ogro", 60) { }
}
```

#### Salida esperada
```
Goblin recibe 10: le quedan 20
Ogro recibe 8: le quedan 52
Goblin recibe 1: le quedan 19
Ogro recibe 1: le quedan 51
```

#### Solución
```csharp
List<Entidad> grupo = [new Goblin(), new Ogro()];

foreach (int golpe in new[] { 10, 1 })
{
    foreach (Entidad e in grupo)
    {
        int real = e.RecibirDanio(golpe);
        Console.WriteLine($"{e.Nombre} recibe {real}: le quedan {e.Vida}");
    }
}

abstract class Entidad
{
    public string Nombre { get; }
    public int Vida { get; private set; }

    protected Entidad(string nombre, int vida)
    {
        Nombre = nombre;
        Vida = vida;
    }

    public virtual int RecibirDanio(int cantidad)
    {
        int real = Math.Min(cantidad, Vida);
        Vida -= real;
        return real;
    }
}

class Goblin : Entidad
{
    public Goblin() : base("Goblin", 30) { }
}

class Ogro : Entidad
{
    public Ogro() : base("Ogro", 60) { }

    public override int RecibirDanio(int cantidad) => base.RecibirDanio(Math.Max(cantidad - 2, 1));
}
```

#### Al superarla
El ogro de práctica se golpea el pecho, satisfecho: ahora sí se siente un ogro. —Y la partida ni se enteró —dice {mentor}—. Le pegó a una lista de entidades. Cada uno contestó con su piel.

#### Imagen
- Una arena redonda de piedra con faroles, sin letras.
- un ogro de caricatura, grandote y simpático, de piel gris azulada, con chaleco de cuero cerrado, se golpea el pecho y le rebota una espada de madera; Ceci y Clave lo miran desde un costado.

### Micro-misión R06-N01-P4 · Fuego cada tres turnos

```meta
lugar: La Arena del Conservatorio
personajes: Ceci, Clave, Gheco
carta: El turno del fuego | turno % 3 == 0 en los turnos 3, 6, 9… · condición ? si : no · Ataque * 2
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
En el pizarrón, el dragón de práctica pega siempre lo mismo. Pero el de verdad, dicen, escupe fuego cada tres compases.

#### Gheco sugiere
`ElegirGolpe` es `virtual` en `Monstruo`: cada monstruo puede decidir cuánto pega. El dragón lo cambia con `override`. Para saber si es turno de fuego, usá el **resto** de dividir por 3: en los turnos 3, 6, 9… da `0`.

```csharp
public override int ElegirGolpe(int turno) => turno % 3 == 0 ? Ataque * 2 : Ataque;
```

Se lee así: "si el turno es múltiplo de 3, el doble del ataque; si no, el ataque". El `? :` es un `if` que devuelve un valor.

#### Desafío
Agregale a `Dragon` el `override` de `ElegirGolpe` que pega el doble en los turnos múltiplos de 3.

#### Código inicial
```csharp
Monstruo dragon = new Dragon();
for (int turno = 1; turno <= 6; turno++)
{
    Console.WriteLine($"Turno {turno}: {dragon.Nombre} pega {dragon.ElegirGolpe(turno)}");
}

abstract class Monstruo
{
    public string Nombre { get; }
    public int Ataque { get; }

    protected Monstruo(string nombre, int ataque)
    {
        Nombre = nombre;
        Ataque = ataque;
    }

    public virtual int ElegirGolpe(int turno) => Ataque;
}

class Dragon : Monstruo
{
    public Dragon() : base("Dragón", 10) { }
}
```

#### Salida esperada
```
Turno 1: Dragón pega 10
Turno 2: Dragón pega 10
Turno 3: Dragón pega 20
Turno 4: Dragón pega 10
Turno 5: Dragón pega 10
Turno 6: Dragón pega 20
```

#### Solución
```csharp
Monstruo dragon = new Dragon();
for (int turno = 1; turno <= 6; turno++)
{
    Console.WriteLine($"Turno {turno}: {dragon.Nombre} pega {dragon.ElegirGolpe(turno)}");
}

abstract class Monstruo
{
    public string Nombre { get; }
    public int Ataque { get; }

    protected Monstruo(string nombre, int ataque)
    {
        Nombre = nombre;
        Ataque = ataque;
    }

    public virtual int ElegirGolpe(int turno) => Ataque;
}

class Dragon : Monstruo
{
    public Dragon() : base("Dragón", 10) { }

    public override int ElegirGolpe(int turno) => turno % 3 == 0 ? Ataque * 2 : Ataque;
}
```

#### Al superarla
En el turno 3, el dibujo del dragón en el pizarrón echa una llamarada de tiza. Gheco se esconde detrás del borrador. —Es de práctica —le dice Ceci. Gheco no sale igual.

#### Imagen
- Un pizarrón grande en una arena de piedra con faroles, con un dragón dibujado con tiza que echa una llamarada de tiza naranja, sin letras ni números.
- Ceci se ríe; Gheco, un gecko de luz cian con antiparras, muy chiquito, más chico que el borrador, se asoma detrás de un borrador de madera apoyado en la repisa del pizarrón.

### Micro-misión R06-N01-P5 · La mochila de Ceci

```meta
lugar: La Arena del Conservatorio
personajes: Ceci, Bemol
carta: GetValueOrDefault | mochila.GetValueOrDefault("antídoto") da 0 si no está · revisar antes de restar · devolver bool: se pudo o no
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
Ceci busca un antídoto en la mochila y el programa explota: el antídoto no estaba. Antes, además, había tomado una poción que no tenía.

#### Gheco sugiere
`Mochila["antídoto"]` explota con `KeyNotFoundException` si esa clave no está en el diccionario. Y restar sin mirar deja pociones en `-1`. Revisá **antes** de restar, con `GetValueOrDefault`, que devuelve la cantidad o `0` si no está:

```csharp
if (Mochila.GetValueOrDefault(objeto) == 0)
{
    return false;      // no se pudo
}
Mochila[objeto]--;
return true;           // se pudo
```

`Usar` devuelve un `bool` para que quien lo llama sepa si se pudo o no, y decida qué mostrar.

#### Desafío
Agregá en `Usar` la comprobación con `GetValueOrDefault`, que devuelve `false` si no queda ninguno.

#### Código inicial
```csharp
Heroe ceci = new Heroe();
foreach (string objeto in new[] { "poción", "poción", "poción", "antídoto" })
{
    if (ceci.Usar(objeto))
    {
        Console.WriteLine($"Ceci usa {objeto}. Le quedan {ceci.Mochila[objeto]}.");
    }
    else
    {
        Console.WriteLine($"No le queda {objeto}.");
    }
}

class Heroe
{
    public Dictionary<string, int> Mochila { get; } = new() { ["poción"] = 2 };

    public bool Usar(string objeto)
    {
        Mochila[objeto]--;
        return true;
    }
}
```

#### Salida esperada
```
Ceci usa poción. Le quedan 1.
Ceci usa poción. Le quedan 0.
No le queda poción.
No le queda antídoto.
```

#### Solución
```csharp
Heroe ceci = new Heroe();
foreach (string objeto in new[] { "poción", "poción", "poción", "antídoto" })
{
    if (ceci.Usar(objeto))
    {
        Console.WriteLine($"Ceci usa {objeto}. Le quedan {ceci.Mochila[objeto]}.");
    }
    else
    {
        Console.WriteLine($"No le queda {objeto}.");
    }
}

class Heroe
{
    public Dictionary<string, int> Mochila { get; } = new() { ["poción"] = 2 };

    public bool Usar(string objeto)
    {
        if (Mochila.GetValueOrDefault(objeto) == 0)
        {
            return false;
        }
        Mochila[objeto]--;
        return true;
    }
}
```

#### Al superarla
—No tenés antídoto —dice Bemol, revolviendo la mochila—. Pero tenés garrapiñadas. —No son mías. —Ahora sí.

#### Imagen
- Las gradas de madera de una arena de piedra con faroles, sin letras.
- Ceci da vuelta una mochila de cuero de la que caen dos frasquitos de poción roja; Bemol, gordito y con panza, mete la mano en la mochila buscando algo más.

### Encargo R06-N01-E1 · Los blancos de la Feria

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Nima quiere un puesto de tiro nuevo para la Feria, con tres clases de blancos. Armá una clase abstracta `Blanco` con un `Nombre` y un método `virtual int Puntos(int distancia)` que dé `10` siempre. Después, tres hijas:

- `BlancoComun` ("Común"): no cambia nada.
- `BlancoMovil` ("Móvil"): da el doble si la distancia es mayor que 20.
- `BlancoDorado` ("Dorado"): da 50, pero solo si la distancia es 30 o más; si no, 0.

Leé tiros, uno por línea, con el formato `tipo,distancia` (`comun`, `movil` o `dorado`), hasta una línea vacía. Por cada tiro, mostrá el nombre del blanco y sus puntos; si el tipo no existe, `No hay blanco: …`. Al final, el total.

Con esta entrada:

```
comun,10
movil,25
dorado,15
dorado,35
cañón,5

```

se muestra:

```
Común: 10
Móvil: 20
Dorado: 0
Dorado: 50
No hay blanco: cañón
Total: 80
```

#### Criterio de aprobación

- `Blanco` es abstracta y cada hija cambia `Puntos` con `override` (la común puede no cambiarlo).
- El programa trata a todos los blancos como `Blanco`: no pregunta de qué clase es cada uno para sumar.

#### Entrada de ejemplo

```
comun,10
movil,25
dorado,15
dorado,35
cañón,5

```

#### Salida esperada

```
Común: 10
Móvil: 20
Dorado: 0
Dorado: 50
No hay blanco: cañón
Total: 80
```

#### Solución de referencia

```csharp
int total = 0;
string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    string[] partes = linea.Split(',');
    Blanco? blanco = partes[0] switch
    {
        "comun" => new BlancoComun(),
        "movil" => new BlancoMovil(),
        "dorado" => new BlancoDorado(),
        _ => null,
    };
    if (blanco is null)
    {
        Console.WriteLine($"No hay blanco: {partes[0]}");
    }
    else
    {
        int puntos = blanco.Puntos(int.Parse(partes[1]));
        Console.WriteLine($"{blanco.Nombre}: {puntos}");
        total += puntos;
    }
    linea = Console.ReadLine();
}
Console.WriteLine($"Total: {total}");

abstract class Blanco
{
    public string Nombre { get; }

    protected Blanco(string nombre)
    {
        Nombre = nombre;
    }

    public virtual int Puntos(int distancia) => 10;
}

class BlancoComun : Blanco
{
    public BlancoComun() : base("Común") { }
}

class BlancoMovil : Blanco
{
    public BlancoMovil() : base("Móvil") { }

    public override int Puntos(int distancia) => distancia > 20 ? base.Puntos(distancia) * 2 : base.Puntos(distancia);
}

class BlancoDorado : Blanco
{
    public BlancoDorado() : base("Dorado") { }

    public override int Puntos(int distancia) => distancia >= 30 ? 50 : 0;
}
```

## R06-N02 · Proyecto: la Arena, la partida

```meta
tipo: tema
padre: R06-N01
precio: 10
criatura: troll
temas: juegos.turnos, diseno.patrones
usa: poo.interfaces, col.pilas-colas, col.mapas, func.lambdas, prog.matematica-azar
```

### Crónica

Los que pelean ya están. Ahora falta **la pelea**. {mentor} dibuja en el pizarrón un menú: `1) Espada  2) Fuego  3) Poción  0) Huir`.

—Mañana alguien va a querer una acción nueva —dice—. Un escudo, una daga envenenada. Y pasado, otro monstruo. Si para cada cosa nueva hay que abrir el combate y meter la mano adentro, el combate se rompe. Así que lo armamos para que **no haya que tocarlo**.

Bemol levanta la mano. —¿Y yo qué hago? —Vos sos el público —dice {mentor}—. La partida te va a **avisar** lo que pasa. Vos decidís cómo contarlo.

### Objetivos

- Que cada acción del menú sea **una clase** que cumple una interfaz (`IAccion`).
- Guardar las acciones en un `Dictionary<string, IAccion>`, sin un `switch` gigante.
- Usar una `Queue` para la **oleada**: el primero que entra es el primero que pelea.
- Que la partida **avise** con un evento, en vez de escribir en la pantalla.
- Recibir el **azar** de afuera, con una semilla, para que la partida se pueda repetir.

### Antes de empezar

- La primera parte del proyecto (R06-N01), interfaces (R02-N09), `Queue` y `Dictionary` (R03-N01 a R03-N03), delegados y eventos (R03-N06 y R03-N07).

### Explicación

#### Las piezas de este nodo

```
IAccion (interfaz)      lo que promete cada acción: un Nombre y Ejecutar(...)
 ├─ GolpeDeEspada        12 más el dado; a veces, crítico
 ├─ BolaDeFuego          25 de daño, cuesta 10 de maná
 └─ BeberPocion          cura 40, si quedan pociones
Partida                 el bucle: saca monstruos de la oleada y los hace pelear por turnos
Program                 arma todo y muestra lo que la partida avisa
```

#### Cada acción, una clase

Todas las acciones prometen lo mismo, así que hay una **interfaz**:

```csharp
interface IAccion
{
    string Nombre { get; }
    bool Ejecutar(Heroe heroe, Monstruo enemigo, Random azar, Action<string> anotar);
}
```

`Ejecutar` devuelve un `bool`: `true` si la acción **se hizo** (y se gasta el turno), `false` si no se pudo (no alcanza el maná, no quedan pociones). Así, elegir algo imposible **no regala el turno** al monstruo.

`anotar` es un `Action<string>`: un método que recibe un texto. La acción no sabe si ese texto va a la pantalla, a un archivo o a una ventana: solo lo anota.

#### El menú es un diccionario

En vez de un `switch` con un caso por acción, las acciones se guardan en un diccionario, con la tecla como clave:

```csharp
Dictionary<string, IAccion> acciones = new()
{
    ["1"] = new GolpeDeEspada(),
    ["2"] = new BolaDeFuego(),
    ["3"] = new BeberPocion(),
};
```

Para ejecutar lo que eligió el jugador, se busca en el diccionario con `TryGetValue`, y se llama a `Ejecutar`. Agregar un escudo es escribir la clase `Escudo` y una línea `["4"] = new Escudo()`: el combate no se toca. A esta forma de armar las cosas se la llama **estrategia**: cada estrategia es un objeto que se puede cambiar.

#### La oleada es una fila

Los monstruos esperan su turno en una `Queue<Monstruo>`: `Dequeue()` saca **al primero que entró**, y `Count` dice cuántos quedan. Como la fila de una boletería.

#### La partida avisa, no escribe

`Partida` no usa `Console.WriteLine`. Tiene un **evento**:

```csharp
public event Action<string>? Mensaje;
...
Mensaje?.Invoke("¡Aparece Goblin!");
```

Y el programa se **suscribe**:

```csharp
partida.Mensaje += Console.WriteLine;
```

`Console.WriteLine` es un método que recibe un texto, así que sirve como suscriptor. Mañana, la misma `Partida` podría mostrarse en una ventana de Unity o de Godot, sin cambiarle nada: solo se suscribe otro método.

#### El azar, desde afuera

El dado sale de un `Random`, pero la partida no lo crea: lo **recibe**. Con `new Random(7)`, el dado tira siempre los mismos números, en el mismo orden: la partida se repite igual cada vez. Es ideal para buscar errores (y para que las micro-misiones se comprueben solas). En el juego de verdad, `new Random()` sin número tira distinto cada vez.

### Código de ejemplo

```csharp
Heroe ceci = new Heroe("Ceci");
Monstruo goblin = new Goblin();
Random azar = new Random(7);

Dictionary<string, IAccion> acciones = new()
{
    ["1"] = new GolpeDeEspada(),
    ["2"] = new BolaDeFuego(),
};

string menu = string.Join("  ", acciones.Select(a => $"{a.Key}) {a.Value.Nombre}"));
Console.WriteLine(menu);

foreach (string tecla in new[] { "2", "1" })
{
    acciones[tecla].Ejecutar(ceci, goblin, azar, Console.WriteLine);
}
Console.WriteLine($"Al goblin le quedan {goblin.Vida}");

interface IAccion
{
    string Nombre { get; }
    bool Ejecutar(Heroe heroe, Monstruo enemigo, Random azar, Action<string> anotar);
}

class GolpeDeEspada : IAccion
{
    public string Nombre => "Espada";

    public bool Ejecutar(Heroe heroe, Monstruo enemigo, Random azar, Action<string> anotar)
    {
        int real = enemigo.RecibirDanio(heroe.Ataque + azar.Next(0, 4));
        anotar($"{real} de daño.");
        return true;
    }
}

class BolaDeFuego : IAccion
{
    public string Nombre => "Fuego (10 maná)";

    public bool Ejecutar(Heroe heroe, Monstruo enemigo, Random azar, Action<string> anotar)
    {
        if (!heroe.GastarMana(10))
        {
            anotar("No alcanza el maná.");
            return false;
        }
        anotar($"La bola de fuego hace {enemigo.RecibirDanio(25)}.");
        return true;
    }
}

class Heroe
{
    public string Nombre { get; }
    public int Ataque => 12;
    public int Mana { get; private set; } = 30;

    public Heroe(string nombre)
    {
        Nombre = nombre;
    }

    public bool GastarMana(int costo)
    {
        if (costo > Mana)
        {
            return false;
        }
        Mana -= costo;
        return true;
    }
}

class Monstruo
{
    public int Vida { get; private set; }

    public Monstruo(int vida)
    {
        Vida = vida;
    }

    public int RecibirDanio(int cantidad)
    {
        int real = Math.Min(cantidad, Vida);
        Vida -= real;
        return real;
    }
}

class Goblin : Monstruo
{
    public Goblin() : base(60) { }
}
```

### Salida esperada

```
1) Espada  2) Fuego (10 maná)
La bola de fuego hace 25.
13 de daño.
Al goblin le quedan 22
```

### ¿Para qué sirve?

Las tres ideas de este nodo están en todos los juegos y en muchísimos programas: **estrategias** que se enchufan sin tocar el resto (los poderes de un personaje, los medios de pago de una tienda), **filas** de cosas por atender (pedidos, turnos, enemigos) y **eventos** para que la lógica no dependa de la pantalla (en Unity, los `UnityEvent`; en Godot, las señales).

### Errores habituales

- **El turno gratis:** si `Ejecutar` devuelve `true` aunque no se haya podido, el monstruo pega igual. Por eso `false` cuando no se pudo.
- **El muerto que pega:** después del golpe del héroe, hay que preguntar `enemigo.EstaViva` antes de que el monstruo conteste.
- **Olvidar suscribirse:** si nadie se suscribe al evento, la partida avisa y nadie escucha: la pantalla queda vacía. Por eso el `?.` en `Mensaje?.Invoke(...)`: si no hay nadie, no explota.
- **La entrada que se termina:** si `Console.ReadLine()` da `null` (no hay más entrada) y no se contempla, el bucle no termina nunca. Acá, `null` quiere decir "huir".

### Micro-misión R06-N02-P1 · El menú que se arma solo

```meta
lugar: La Arena del Conservatorio
personajes: Ceci, Clave
carta: El menú | string.Join("  ", acciones.Select(a => $"{a.Key}) {a.Value.Nombre}")) · cada par del diccionario: Key y Value
recompensa: xp 20, oro 20, monedas 4
```

#### Escena
Don Cedro le regaló a Ceci un escudo de madera, y ya está en el diccionario de acciones. Pero el menú del pizarrón no lo muestra: alguien lo escribió a mano.

#### Gheco sugiere
El menú está escrito **a mano**, así que cada acción nueva obliga a cambiarlo. Mejor armarlo **desde el diccionario**. Recorrer un diccionario da pares, con `Key` (la tecla) y `Value` (la acción). Con `Select` se convierte cada par en un texto, y con `string.Join` se pegan todos con dos espacios en el medio:

```csharp
string menu = string.Join("  ", acciones.Select(a => $"{a.Key}) {a.Value.Nombre}"));
```

#### Desafío
Reemplazá el menú escrito a mano por uno armado con `string.Join` y `Select` desde el diccionario.

#### Código inicial
```csharp
Dictionary<string, IAccion> acciones = new()
{
    ["1"] = new GolpeDeEspada(),
    ["2"] = new BolaDeFuego(),
    ["3"] = new Escudo(),
};

string menu = "1) Espada  2) Fuego (10 maná)";
Console.WriteLine($"{menu}  0) Huir");

interface IAccion
{
    string Nombre { get; }
}

class GolpeDeEspada : IAccion
{
    public string Nombre => "Espada";
}

class BolaDeFuego : IAccion
{
    public string Nombre => "Fuego (10 maná)";
}

class Escudo : IAccion
{
    public string Nombre => "Escudo";
}
```

#### Salida esperada
```
1) Espada  2) Fuego (10 maná)  3) Escudo  0) Huir
```

#### Solución
```csharp
Dictionary<string, IAccion> acciones = new()
{
    ["1"] = new GolpeDeEspada(),
    ["2"] = new BolaDeFuego(),
    ["3"] = new Escudo(),
};

string menu = string.Join("  ", acciones.Select(a => $"{a.Key}) {a.Value.Nombre}"));
Console.WriteLine($"{menu}  0) Huir");

interface IAccion
{
    string Nombre { get; }
}

class GolpeDeEspada : IAccion
{
    public string Nombre => "Espada";
}

class BolaDeFuego : IAccion
{
    public string Nombre => "Fuego (10 maná)";
}

class Escudo : IAccion
{
    public string Nombre => "Escudo";
}
```

#### Al superarla
El escudo aparece en el menú del pizarrón sin que nadie lo escriba. —La próxima acción que agregues —dice {mentor}— va a aparecer sola. Así se escribe una vez.

#### Imagen
- Un pizarrón grande en una arena de piedra con faroles, con tres dibujos de tiza en fila: una espada, una llamita y un escudo, sin letras ni números.
- Ceci apoya un escudo de madera redondo contra el pizarrón; Clave asiente con la batuta en la mano.

### Micro-misión R06-N02-P2 · El turno gratis

```meta
lugar: La Arena del Conservatorio
personajes: Ceci, Bemol
carta: Ejecutar devuelve bool | true: se hizo, se gasta el turno · false: no se pudo, elegí otra · el monstruo pega solo si se hizo
recompensa: xp 20, oro 20
```

#### Escena
Ceci elige fuego sin maná: no pasa nada, y el goblin le pega igual. Bemol grita desde la grada que eso es trampa.

#### Gheco sugiere
`BolaDeFuego` avisa que no alcanza el maná, pero devuelve `true`: dice "me hice" cuando no se hizo. Entonces el turno se gasta y el goblin pega. Cuando no se pudo, tiene que devolver `false`:

```csharp
if (!heroe.GastarMana(10))
{
    anotar("No alcanza el maná.");
    return false;      // no gasta el turno
}
```

Mirá el `do … while` del turno: repite **mientras** la acción no se haya hecho, y pasa a la siguiente tecla.

#### Desafío
Hacé que `BolaDeFuego` devuelva `false` cuando no alcanza el maná.

#### Código inicial
```csharp
Heroe ceci = new Heroe();
Queue<string> teclas = new(["2", "2", "1"]);
Dictionary<string, IAccion> acciones = new() { ["1"] = new GolpeDeEspada(), ["2"] = new BolaDeFuego() };

for (int turno = 1; turno <= 2; turno++)
{
    Console.WriteLine($"Turno {turno}, maná {ceci.Mana}");
    bool hecha;
    do
    {
        hecha = acciones[teclas.Dequeue()].Ejecutar(ceci, Console.WriteLine);
    } while (!hecha);
    Console.WriteLine("Goblin golpea: 6 de daño.");
}

interface IAccion
{
    bool Ejecutar(Heroe heroe, Action<string> anotar);
}

class GolpeDeEspada : IAccion
{
    public bool Ejecutar(Heroe heroe, Action<string> anotar)
    {
        anotar("Espada: 12 de daño.");
        return true;
    }
}

class BolaDeFuego : IAccion
{
    public bool Ejecutar(Heroe heroe, Action<string> anotar)
    {
        if (!heroe.GastarMana(10))
        {
            anotar("No alcanza el maná.");
            return true;
        }
        anotar("La bola de fuego hace 25.");
        return true;
    }
}

class Heroe
{
    public int Mana { get; private set; } = 10;

    public bool GastarMana(int costo)
    {
        if (costo > Mana)
        {
            return false;
        }
        Mana -= costo;
        return true;
    }
}
```

#### Salida esperada
```
Turno 1, maná 10
La bola de fuego hace 25.
Goblin golpea: 6 de daño.
Turno 2, maná 0
No alcanza el maná.
Espada: 12 de daño.
Goblin golpea: 6 de daño.
```

#### Solución
```csharp
Heroe ceci = new Heroe();
Queue<string> teclas = new(["2", "2", "1"]);
Dictionary<string, IAccion> acciones = new() { ["1"] = new GolpeDeEspada(), ["2"] = new BolaDeFuego() };

for (int turno = 1; turno <= 2; turno++)
{
    Console.WriteLine($"Turno {turno}, maná {ceci.Mana}");
    bool hecha;
    do
    {
        hecha = acciones[teclas.Dequeue()].Ejecutar(ceci, Console.WriteLine);
    } while (!hecha);
    Console.WriteLine("Goblin golpea: 6 de daño.");
}

interface IAccion
{
    bool Ejecutar(Heroe heroe, Action<string> anotar);
}

class GolpeDeEspada : IAccion
{
    public bool Ejecutar(Heroe heroe, Action<string> anotar)
    {
        anotar("Espada: 12 de daño.");
        return true;
    }
}

class BolaDeFuego : IAccion
{
    public bool Ejecutar(Heroe heroe, Action<string> anotar)
    {
        if (!heroe.GastarMana(10))
        {
            anotar("No alcanza el maná.");
            return false;
        }
        anotar("La bola de fuego hace 25.");
        return true;
    }
}

class Heroe
{
    public int Mana { get; private set; } = 10;

    public bool GastarMana(int costo)
    {
        if (costo > Mana)
        {
            return false;
        }
        Mana -= costo;
        return true;
    }
}
```

#### Al superarla
—¡Ahora sí! —grita Bemol, y tira garrapiñadas al aire—. Sin maná, se elige otra cosa. ¡Eso es justicia!

#### Imagen
- Las gradas de madera de una arena de piedra con faroles, sin letras.
- Bemol, gordito y con panza, festeja de pie con los brazos arriba, y le vuelan garrapiñadas de una bolsita de papel; abajo, en la arena, Ceci levanta una espada de madera.

### Micro-misión R06-N02-P3 · La oleada

```meta
lugar: La Arena del Conservatorio
personajes: Ceci, Clave
carta: Queue | new Queue<T>(lista) · Dequeue() saca al primero que entró · Count: cuántos quedan
recompensa: xp 20, oro 20
```

#### Escena
Los monstruos tenían que salir en orden: goblin, ogro y, al final, el dragón. Pero sale primero el dragón, y Ceci todavía no calentó.

#### Gheco sugiere
El programa saca **el último** de la lista: es una pila, no una fila. Para que salga primero el que entró primero, usá una `Queue`:

```csharp
Queue<string> oleada = new(["Goblin", "Ogro", "Dragón"]);
string enemigo = oleada.Dequeue();      // "Goblin"
```

`Dequeue()` saca y devuelve al primero, y `oleada.Count` dice cuántos quedan esperando.

#### Desafío
Cambiá la `List` por una `Queue`, y sacá a cada monstruo con `Dequeue()`.

#### Código inicial
```csharp
List<string> oleada = ["Goblin", "Ogro", "Dragón"];

while (oleada.Count > 0)
{
    string enemigo = oleada[oleada.Count - 1];
    oleada.RemoveAt(oleada.Count - 1);
    Console.WriteLine($"--- ¡Aparece {enemigo}! ({oleada.Count} más en camino) ---");
}
```

#### Salida esperada
```
--- ¡Aparece Goblin! (2 más en camino) ---
--- ¡Aparece Ogro! (1 más en camino) ---
--- ¡Aparece Dragón! (0 más en camino) ---
```

#### Solución
```csharp
Queue<string> oleada = new(["Goblin", "Ogro", "Dragón"]);

while (oleada.Count > 0)
{
    string enemigo = oleada.Dequeue();
    Console.WriteLine($"--- ¡Aparece {enemigo}! ({oleada.Count} más en camino) ---");
}
```

#### Al superarla
El goblin entra primero, frotándose las manos. El dragón espera al fondo, en la oscuridad, y solo se le ven los ojos. —Cada cosa a su tiempo —dice {mentor}.

#### Imagen
- La entrada de una arena de piedra con faroles, con una fila de monstruos de caricatura esperando: adelante un goblin chiquito y verde, detrás un ogro grandote, y al fondo, en la sombra, solo dos ojos naranjas brillantes, sin letras.
- Ceci, del otro lado de la arena, se acomoda la capa.

### Micro-misión R06-N02-P4 · La partida avisa

```meta
lugar: La Arena del Conservatorio
personajes: Ceci, Bemol, Gheco
carta: Suscribirse | partida.Mensaje += Console.WriteLine; · la partida avisa · quien se suscribe decide qué hacer
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
La partida corre, pero la pantalla queda vacía: solo el título y el final. Bemol se perdió toda la pelea.

#### Gheco sugiere
La partida **avisa** con su evento `Mensaje`, pero nadie lo está escuchando. Suscribite antes de jugar:

```csharp
partida.Mensaje += Console.WriteLine;
```

`+=` agrega un suscriptor. Como `Console.WriteLine` recibe un texto, cada aviso de la partida se muestra en la pantalla. Si después quisieras guardarlos en un archivo, te suscribirías con otro método, sin tocar `Partida`.

#### Desafío
Suscribí `Console.WriteLine` al evento `Mensaje` de la partida, antes de llamar a `Jugar`.

#### Código inicial
```csharp
Partida partida = new Partida(["Goblin", "Ogro"]);

Console.WriteLine("=== La Arena del Conservatorio ===");
partida.Jugar();
Console.WriteLine("Fin de la oleada.");

class Partida
{
    private readonly Queue<string> _oleada;

    public event Action<string>? Mensaje;

    public Partida(IEnumerable<string> oleada)
    {
        _oleada = new Queue<string>(oleada);
    }

    public void Jugar()
    {
        while (_oleada.Count > 0)
        {
            string enemigo = _oleada.Dequeue();
            Mensaje?.Invoke($"¡Aparece {enemigo}!");
            Mensaje?.Invoke($"{enemigo} cae.");
        }
    }
}
```

#### Salida esperada
```
=== La Arena del Conservatorio ===
¡Aparece Goblin!
Goblin cae.
¡Aparece Ogro!
Ogro cae.
Fin de la oleada.
```

#### Solución
```csharp
Partida partida = new Partida(["Goblin", "Ogro"]);
partida.Mensaje += Console.WriteLine;

Console.WriteLine("=== La Arena del Conservatorio ===");
partida.Jugar();
Console.WriteLine("Fin de la oleada.");

class Partida
{
    private readonly Queue<string> _oleada;

    public event Action<string>? Mensaje;

    public Partida(IEnumerable<string> oleada)
    {
        _oleada = new Queue<string>(oleada);
    }

    public void Jugar()
    {
        while (_oleada.Count > 0)
        {
            string enemigo = _oleada.Dequeue();
            Mensaje?.Invoke($"¡Aparece {enemigo}!");
            Mensaje?.Invoke($"{enemigo} cae.");
        }
    }
}
```

#### Al superarla
Ahora la pelea se cuenta entera, y Bemol la relata desde la grada como si fuera un partido. Gheco, sentado en su hombro, hace de hinchada.

#### Imagen
- Las gradas de madera de una arena de piedra con faroles, sin letras.
- Bemol, gordito y con panza, relata con un cucurucho de papel como megáfono; Gheco, un gecko de luz cian con antiparras, MINÚSCULO, sentado en el hombro de Bemol, más chico que su oreja, levanta los bracitos.

### Micro-misión R06-N02-P5 · El muerto que pega

```meta
lugar: La Arena del Conservatorio
personajes: Ceci, Clave
criatura: troll
carta: EstaViva | después del golpe del héroe · if (enemigo.EstaViva) contesta · un caído no pega
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
Ceci tumba al goblin con la segunda bola de fuego, y el goblin, desde el piso, le pega igual. Un troll se ríe escondido entre los atriles.

#### Gheco sugiere
En `Pelear`, el monstruo contesta **siempre**, aunque el golpe de Ceci lo haya tumbado. Hay que preguntar antes si sigue vivo:

```csharp
if (enemigo.EstaViva)
{
    int real = heroe.RecibirDanio(enemigo.ElegirGolpe(azar));
    Mensaje?.Invoke($"{enemigo.Nombre} golpea: {real} de daño.");
}
```

Esta partida lee las teclas de la entrada (`2` y `2`: dos bolas de fuego) y tira el dado con la semilla 7, así que da siempre lo mismo.

#### Desafío
Agregá en `Pelear` la pregunta `if (enemigo.EstaViva)` antes de que el monstruo golpee.

#### Entrada
```
2
2
```

#### Código inicial
```csharp
Partida partida = new Partida(new Heroe(), new Random(7));
partida.Mensaje += Console.WriteLine;
partida.Pelear(new Monstruo("Goblin", 30, 5));
Console.WriteLine($"Ceci termina con {partida.Heroe.Vida} de vida.");

class Partida
{
    public Heroe Heroe { get; }
    private readonly Random _azar;

    public event Action<string>? Mensaje;

    public Partida(Heroe heroe, Random azar)
    {
        Heroe = heroe;
        _azar = azar;
    }

    public void Pelear(Monstruo enemigo)
    {
        while (enemigo.EstaViva && Heroe.EstaViva)
        {
            string? tecla = Console.ReadLine();
            if (tecla is null)
            {
                Mensaje?.Invoke("Ceci se retira.");
                return;
            }
            int hecho = enemigo.RecibirDanio(25);
            Mensaje?.Invoke($"La bola de fuego hace {hecho}.");

            int real = Heroe.RecibirDanio(enemigo.ElegirGolpe(_azar));
            Mensaje?.Invoke($"{enemigo.Nombre} golpea: {real} de daño.");
        }
        Mensaje?.Invoke($"{enemigo.Nombre} cae.");
    }
}

class Heroe
{
    public int Vida { get; private set; } = 100;
    public bool EstaViva => Vida > 0;

    public int RecibirDanio(int cantidad)
    {
        int real = Math.Min(cantidad, Vida);
        Vida -= real;
        return real;
    }
}

class Monstruo
{
    public string Nombre { get; }
    public int Vida { get; private set; }
    public int Ataque { get; }
    public bool EstaViva => Vida > 0;

    public Monstruo(string nombre, int vida, int ataque)
    {
        Nombre = nombre;
        Vida = vida;
        Ataque = ataque;
    }

    public int RecibirDanio(int cantidad)
    {
        int real = Math.Min(cantidad, Vida);
        Vida -= real;
        return real;
    }

    public int ElegirGolpe(Random azar) => Ataque + azar.Next(0, 4);
}
```

#### Salida esperada
```
La bola de fuego hace 25.
Goblin golpea: 6 de daño.
La bola de fuego hace 5.
Goblin cae.
Ceci termina con 94 de vida.
```

#### Solución
```csharp
Partida partida = new Partida(new Heroe(), new Random(7));
partida.Mensaje += Console.WriteLine;
partida.Pelear(new Monstruo("Goblin", 30, 5));
Console.WriteLine($"Ceci termina con {partida.Heroe.Vida} de vida.");

class Partida
{
    public Heroe Heroe { get; }
    private readonly Random _azar;

    public event Action<string>? Mensaje;

    public Partida(Heroe heroe, Random azar)
    {
        Heroe = heroe;
        _azar = azar;
    }

    public void Pelear(Monstruo enemigo)
    {
        while (enemigo.EstaViva && Heroe.EstaViva)
        {
            string? tecla = Console.ReadLine();
            if (tecla is null)
            {
                Mensaje?.Invoke("Ceci se retira.");
                return;
            }
            int hecho = enemigo.RecibirDanio(25);
            Mensaje?.Invoke($"La bola de fuego hace {hecho}.");

            if (enemigo.EstaViva)
            {
                int real = Heroe.RecibirDanio(enemigo.ElegirGolpe(_azar));
                Mensaje?.Invoke($"{enemigo.Nombre} golpea: {real} de daño.");
            }
        }
        Mensaje?.Invoke($"{enemigo.Nombre} cae.");
    }
}

class Heroe
{
    public int Vida { get; private set; } = 100;
    public bool EstaViva => Vida > 0;

    public int RecibirDanio(int cantidad)
    {
        int real = Math.Min(cantidad, Vida);
        Vida -= real;
        return real;
    }
}

class Monstruo
{
    public string Nombre { get; }
    public int Vida { get; private set; }
    public int Ataque { get; }
    public bool EstaViva => Vida > 0;

    public Monstruo(string nombre, int vida, int ataque)
    {
        Nombre = nombre;
        Vida = vida;
        Ataque = ataque;
    }

    public int RecibirDanio(int cantidad)
    {
        int real = Math.Min(cantidad, Vida);
        Vida -= real;
        return real;
    }

    public int ElegirGolpe(Random azar) => Ataque + azar.Next(0, 4);
}
```

#### Al superarla
El goblin queda en el piso, quietito, con estrellitas dando vueltas. El troll de los atriles deja de reírse y se va en puntas de pie. —Los muertos no pegan —dice {mentor}—. Ni en la Arena ni en ningún programa.

#### Imagen
- Una arena redonda de piedra con faroles, sin letras.
- Un goblin chiquito y verde, de caricatura, tirado en el piso con estrellitas dando vueltas sobre la cabeza; Ceci baja la mano después de lanzar una bola de fuego; Clave mira desde un costado.

### Encargo R06-N02-E1 · El consultorio del pueblo

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

El consultorio del pueblo atiende por orden de llegada, y quiere una pantalla en la sala de espera. Armá un `record Paciente(string Nombre, string Motivo)` y una clase `Consultorio` con:

- una `Queue<Paciente>` privada;
- un evento `public event Action<Paciente>? Llamado;`
- `Llegar(Paciente p)`, que lo pone en la fila;
- `LlamarSiguiente()`, que saca al primero y avisa con el evento; si no hay nadie, devuelve `false` (y si llamó a alguien, `true`).

El programa se suscribe al evento con una **pantalla** que muestra `Pantalla: <nombre>, pase al consultorio (<motivo>)`. Después lee órdenes, una por línea, hasta una línea vacía: `llega Nombre,Motivo` o `siguiente`. Si no hay nadie para llamar, mostrá `No hay nadie esperando`. Al final, `Quedan N en la sala`.

Con esta entrada:

```
llega Ana,dolor de muela
llega Teo,tos
siguiente
llega Lía,un raspón
siguiente
siguiente
siguiente

```

se muestra:

```
Pantalla: Ana, pase al consultorio (dolor de muela)
Pantalla: Teo, pase al consultorio (tos)
Pantalla: Lía, pase al consultorio (un raspón)
No hay nadie esperando
Quedan 0 en la sala
```

#### Criterio de aprobación

- La fila es una `Queue` y el consultorio avisa con un evento: no escribe en la pantalla.
- La pantalla es un suscriptor del evento.

#### Entrada de ejemplo

```
llega Ana,dolor de muela
llega Teo,tos
siguiente
llega Lía,un raspón
siguiente
siguiente
siguiente

```

#### Salida esperada

```
Pantalla: Ana, pase al consultorio (dolor de muela)
Pantalla: Teo, pase al consultorio (tos)
Pantalla: Lía, pase al consultorio (un raspón)
No hay nadie esperando
Quedan 0 en la sala
```

#### Solución de referencia

```csharp
Consultorio consultorio = new Consultorio();
consultorio.Llamado += p => Console.WriteLine($"Pantalla: {p.Nombre}, pase al consultorio ({p.Motivo})");

string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    if (linea.StartsWith("llega "))
    {
        string[] partes = linea.Substring(6).Split(',');
        consultorio.Llegar(new Paciente(partes[0], partes[1]));
    }
    else if (linea == "siguiente" && !consultorio.LlamarSiguiente())
    {
        Console.WriteLine("No hay nadie esperando");
    }
    linea = Console.ReadLine();
}
Console.WriteLine($"Quedan {consultorio.Esperando} en la sala");

record Paciente(string Nombre, string Motivo);

class Consultorio
{
    private readonly Queue<Paciente> _fila = new();

    public event Action<Paciente>? Llamado;

    public int Esperando => _fila.Count;

    public void Llegar(Paciente p)
    {
        _fila.Enqueue(p);
    }

    public bool LlamarSiguiente()
    {
        if (_fila.Count == 0)
        {
            return false;
        }
        Llamado?.Invoke(_fila.Dequeue());
        return true;
    }
}
```

## R06-N03 · Proyecto: Junta las Gemas

```meta
tipo: tema
padre: R06-N02
precio: 10
criatura: orco
temas: juegos.ia, juegos.guardado
usa: poo.records, poo.operadores, col.conjuntos, col.matrices, func.streams, arch.json, prog.enums
```

### Crónica

Entre pelea y pelea, Ceci encuentra detrás de la Arena un **jardín de setos** que nadie poda: un laberinto. Entre las hojas brillan **gemas de cristal** que suenan como campanitas cuando se las toca, y por los pasillos camina un **guardián de piedra**, lento, que siempre va hacia el que se mueve.

—Es el juego que me enseñó el Vidriero —dice {mentor}, mirando el laberinto desde arriba—. Junta las Gemas. Él lo armaba con vidrios de colores. Hacelo vos, pero en una partitura.

Bemol ya está adentro del laberinto, perdido. —¡Estoy bien! —grita—. ¡Creo!

### Objetivos

- Representar posiciones con un **`record struct`** y enseñarle a sumar con `operator +`.
- Guardar las gemas en un **`HashSet`**: buscar y sacar sin recorrer.
- Leer un mapa escrito como texto, con **fila y columna** en el orden justo.
- Darle al enemigo una inteligencia simple con **LINQ**.
- Separar la lógica de la pantalla y guardar el **récord** en un archivo JSON.

### Antes de empezar

- `struct`, `record` y `enum` (R02-N04 y R02-N05), operadores (R02-N03), matrices (R01-N12), `HashSet` (R03-N02), LINQ (R03-N08 y R03-N09), JSON y excepciones (Acto IV).

### Explicación

#### El nivel es un dato

El mapa se escribe como un arreglo de textos, una fila por renglón:

```
C = Ceci    * = gema    E = guardián    # = seto
```

```csharp
string[] nivel =
{
    "#######",
    "#C..*.#",
    "#.##..#",
    "#*...E#",
    "#######",
};
```

Para hacer otro nivel, no se toca el código: se escribe otro mapa. El borde es todo seto, así que nadie se sale.

#### Fila y columna

`nivel[y][x]` es la letra de la fila `y`, columna `x`: **primero la fila** (de arriba abajo) y después la columna (de izquierda a derecha). Es el error más común en una grilla: escribir `nivel[x][y]` da la letra equivocada, o se sale del mapa.

#### Una posición: `record struct`

```csharp
readonly record struct Vec2(int X, int Y)
{
    public static Vec2 operator +(Vec2 a, Vec2 b) => new(a.X + b.X, a.Y + b.Y);
    public int DistanciaA(Vec2 otro) => Math.Abs(X - otro.X) + Math.Abs(Y - otro.Y);
}
```

- **`record struct`**: se copia como un número (es un `struct`) y se compara **por contenido** (como un `record`): `new Vec2(1, 2) == new Vec2(1, 2)` da `true`. Y al mostrarlo, se ve lindo: `Vec2 { X = 1, Y = 2 }`.
- **`readonly`**: no se puede cambiar una parte (`ceci.X = 5` no compila). Para moverse, se crea otra posición.
- **`operator +`**: le enseña a sumar con `+`. Así, moverse es `ceci + derecha`. Es lo mismo que hace `Vector2` en Unity y en Godot.
- **`DistanciaA`**: la **distancia Manhattan**, la cantidad de pasos en una grilla sin diagonales: `|dx| + |dy|`.

#### Las gemas, en un `HashSet`

Un `HashSet<Vec2>` guarda posiciones **sin repetir** y responde enseguida si una está, sin recorrer nada. Y `Remove` hace dos cosas: la saca **y** dice si estaba:

```csharp
if (gemas.Remove(ceci))
{
    puntos += 10;    // había una gema justo ahí
}
```

#### La inteligencia del guardián

El guardián mira sus cuatro vecinos, se queda con los que no son seto y elige el que más lo acerca a Ceci:

```csharp
Vec2 siguiente = pasos
    .Select(p => actual + p)                 // los cuatro vecinos
    .Where(p => !EsSeto(p))                  // los que se pueden pisar
    .DefaultIfEmpty(actual)                  // si no hay ninguno, se queda
    .MinBy(p => p.DistanciaA(ceci));         // el que más se acerca
```

Eso es todo. Es una inteligencia **voraz**: siempre da el paso que más acerca, y por eso a veces se traba detrás de un seto. Ahí está la gracia del juego.

#### La lógica no dibuja

`Mundo` tiene el estado y las reglas, y su `Dibujar()` **devuelve** un texto, sin mostrarlo. El programa decide qué hacer con ese texto. Para armarlo se usa un **`StringBuilder`**, que va agregando letras sobre el mismo lugar, en vez de crear un texto nuevo en cada paso.

#### El récord, en un archivo

El mejor puntaje se guarda en `record.json`. Si el archivo no está, se arranca de cero; y si está **roto** (alguien lo editó a mano), también: se atrapa la `JsonException` y el juego sigue.

### Código de ejemplo

```csharp
string[] nivel =
{
    "#######",
    "#C..*.#",
    "#.##..#",
    "#*...E#",
    "#######",
};

Mundo mundo = new Mundo(nivel);
Console.Write(mundo.Dibujar());
Console.WriteLine($"Ceci está en {mundo.Ceci}, quedan {mundo.Gemas} gemas.");

readonly record struct Vec2(int X, int Y);

class Mundo
{
    private readonly string[] _mapa;
    private readonly HashSet<Vec2> _gemas = new();
    private Vec2 _guardian;

    public Vec2 Ceci { get; private set; }
    public int Gemas => _gemas.Count;

    public Mundo(string[] nivel)
    {
        _mapa = nivel;
        for (int y = 0; y < nivel.Length; y++)
        {
            for (int x = 0; x < nivel[y].Length; x++)
            {
                Vec2 p = new(x, y);
                switch (nivel[y][x])
                {
                    case 'C':
                        Ceci = p;
                        break;
                    case '*':
                        _gemas.Add(p);
                        break;
                    case 'E':
                        _guardian = p;
                        break;
                }
            }
        }
    }

    public string Dibujar()
    {
        System.Text.StringBuilder salida = new();
        for (int y = 0; y < _mapa.Length; y++)
        {
            for (int x = 0; x < _mapa[y].Length; x++)
            {
                Vec2 p = new(x, y);
                char c = _mapa[y][x] == '#' ? '#' : '.';
                if (_gemas.Contains(p)) c = '*';
                if (p == _guardian) c = 'E';
                if (p == Ceci) c = 'C';
                salida.Append(c);
            }
            salida.AppendLine();
        }
        return salida.ToString();
    }
}
```

### Salida esperada

```
#######
#C..*.#
#.##..#
#*...E#
#######
Ceci está en Vec2 { X = 1, Y = 1 }, quedan 2 gemas.
```

### ¿Para qué sirve?

Es la base de cualquier juego de grilla (laberintos, juegos de rol de casilleros, buscaminas) y de muchos motores de juego: posiciones que se suman como vectores, un mapa que es un dato, enemigos que deciden con una regla simple y un mundo que se puede probar sin abrir ninguna ventana.

### Errores habituales

- **Orco: salirse del mapa.** `_mapa[y][x]` con una posición fuera da `IndexOutOfRangeException`. Acá no pasa porque el borde es todo seto; si cambiás el nivel, cuidá eso.
- **Ogro: filas y columnas al revés.** `_mapa[p.X][p.Y]` lee otra casilla. Primero la fila: `_mapa[p.Y][p.X]`.
- **Goblin: cambiar un `readonly struct`.** `ceci.X = 5` no compila (CS8332). Se asigna otro: `ceci = destino`.
- **Una gema que se cobra dos veces:** con `Contains` se suma, pero la gema sigue ahí. `Remove` la saca y dice si estaba.

### Micro-misión R06-N03-P1 · Sumar posiciones

```meta
lugar: El Jardín de los Setos
personajes: Ceci, Clave
carta: operator + | public static Vec2 operator +(Vec2 a, Vec2 b) · => new(a.X + b.X, a.Y + b.Y) · moverse es ceci + paso
recompensa: xp 20, oro 20, monedas 4
```

#### Escena
Ceci quiere moverse por el laberinto sumando pasos, como se suman notas. Pero el ensayo general dice que dos posiciones no se pueden sumar.

#### Gheco sugiere
C# sabe sumar números, pero no sabe sumar **tus** tipos: `ceci + paso` da el error `CS0019`. Hay que enseñarle, con un **operador** adentro del `record struct`:

```csharp
public static Vec2 operator +(Vec2 a, Vec2 b) => new(a.X + b.X, a.Y + b.Y);
```

Se lee: "sumar dos `Vec2` es crear uno nuevo con las X sumadas y las Y sumadas". Va `static` porque no es de una posición en particular: recibe las dos.

#### Desafío
Agregale a `Vec2` el `operator +` que suma las dos posiciones.

#### Código inicial
```csharp
Vec2 ceci = new(1, 1);
Vec2 derecha = new(1, 0);
Vec2 abajo = new(0, 1);

ceci = ceci + derecha;
ceci = ceci + derecha;
ceci = ceci + abajo;
Console.WriteLine($"Ceci está en {ceci}");
Console.WriteLine(ceci == new Vec2(3, 2) ? "Llegó a la gema" : "Todavía no");

readonly record struct Vec2(int X, int Y)
{
}
```

#### Salida esperada
```
Ceci está en Vec2 { X = 3, Y = 2 }
Llegó a la gema
```

#### Solución
```csharp
Vec2 ceci = new(1, 1);
Vec2 derecha = new(1, 0);
Vec2 abajo = new(0, 1);

ceci = ceci + derecha;
ceci = ceci + derecha;
ceci = ceci + abajo;
Console.WriteLine($"Ceci está en {ceci}");
Console.WriteLine(ceci == new Vec2(3, 2) ? "Llegó a la gema" : "Todavía no");

readonly record struct Vec2(int X, int Y)
{
    public static Vec2 operator +(Vec2 a, Vec2 b) => new(a.X + b.X, a.Y + b.Y);
}
```

#### Al superarla
Ceci da dos pasos a la derecha y uno abajo, y la gema suena como una campanita cuando la toca. —Una posición más un paso —dice {mentor}—. Igual que una nota más un intervalo.

#### Imagen
- Un laberinto de setos verdes bien recortados, de noche, iluminado con faroles, con una gema de cristal celeste brillando entre las hojas, sin letras.
- Ceci, con el violín en la espalda, estira la mano hacia la gema; Clave mira desde una escalinata de piedra, arriba.

### Micro-misión R06-N03-P2 · La gema que se cobra dos veces

```meta
lugar: El Jardín de los Setos
personajes: Ceci, Bemol
carta: HashSet.Remove | gemas.Remove(p) la saca y dice si estaba · true: había gema · Contains solo pregunta
recompensa: xp 20, oro 20
```

#### Escena
Bemol pasa tres veces por la misma gema, y las tres veces le suman diez puntos. Está feliz. Clave, no.

#### Gheco sugiere
`Contains` solo **pregunta** si la gema está: suma los puntos, pero la gema sigue ahí, y al volver a pasar, suma otra vez. `Remove` hace las dos cosas juntas: la **saca**, y devuelve `true` si estaba:

```csharp
if (gemas.Remove(bemol))
{
    puntos += 10;
}
```

La segunda vez que pasa, ya no está: `Remove` devuelve `false` y no suma.

#### Desafío
Cambiá el `Contains` por un `Remove`, para que cada gema se cobre una sola vez.

#### Código inicial
```csharp
HashSet<Vec2> gemas = [new(2, 1), new(4, 1)];
Vec2[] camino = [new(1, 1), new(2, 1), new(3, 1), new(2, 1), new(3, 1), new(4, 1)];
int puntos = 0;

foreach (Vec2 bemol in camino)
{
    if (gemas.Contains(bemol))
    {
        puntos += 10;
        Console.WriteLine($"¡Gema en {bemol.X},{bemol.Y}! Puntos: {puntos}");
    }
}
Console.WriteLine($"Quedan {gemas.Count} gemas");

readonly record struct Vec2(int X, int Y);
```

#### Salida esperada
```
¡Gema en 2,1! Puntos: 10
¡Gema en 4,1! Puntos: 20
Quedan 0 gemas
```

#### Solución
```csharp
HashSet<Vec2> gemas = [new(2, 1), new(4, 1)];
Vec2[] camino = [new(1, 1), new(2, 1), new(3, 1), new(2, 1), new(3, 1), new(4, 1)];
int puntos = 0;

foreach (Vec2 bemol in camino)
{
    if (gemas.Remove(bemol))
    {
        puntos += 10;
        Console.WriteLine($"¡Gema en {bemol.X},{bemol.Y}! Puntos: {puntos}");
    }
}
Console.WriteLine($"Quedan {gemas.Count} gemas");

readonly record struct Vec2(int X, int Y);
```

#### Al superarla
—¿Cómo que veinte? —protesta Bemol—. ¡Pasé un montón de veces! —Por eso —dice Ceci, y le muestra el hueco entre las hojas donde estaba la gema.

#### Imagen
- Un pasillo de un laberinto de setos verdes con faroles, de noche, con un hueco vacío entre las hojas donde antes había algo, sin letras.
- Bemol, gordito y con panza, señala el hueco con cara de indignado; Ceci, al lado, sostiene una gema de cristal celeste y se ríe.

### Micro-misión R06-N03-P3 · Filas y columnas

```meta
lugar: El Jardín de los Setos
personajes: Ceci, Clave
criatura: ogro
carta: mapa[y][x] | primero la fila (y, de arriba abajo) · después la columna (x, de izquierda a derecha) · al revés lee otra casilla
recompensa: xp 20, oro 20
```

#### Escena
Ceci intenta caminar por el pasillo de arriba y choca contra un seto que no está. Después atraviesa uno que sí está. Un ogro, del otro lado, toca la nota equivocada perfecto.

#### Gheco sugiere
`EsSeto` lee `_mapa[p.X][p.Y]`: usa la columna como fila. En un mapa, el primer índice es **la fila** (`Y`, el renglón) y el segundo, **la columna** (`X`, la letra dentro del renglón):

```csharp
private bool EsSeto(Vec2 p) => _mapa[p.Y][p.X] == '#';
```

Pensalo como leer un libro: primero buscás el renglón y después la letra.

#### Desafío
Corregí `EsSeto` para que lea primero la fila (`p.Y`) y después la columna (`p.X`).

#### Código inicial
```csharp
string[] nivel =
{
    "######",
    "#C...#",
    "#.##.#",
    "######",
};
Mundo mundo = new Mundo(nivel, new Vec2(1, 1));

foreach (Vec2 paso in new Vec2[] { new(1, 0), new(1, 0), new(0, 1), new(1, 0), new(1, 0) })
{
    Console.WriteLine(mundo.Mover(paso) ? $"Camina a {mundo.Ceci.X},{mundo.Ceci.Y}" : "Hay un seto");
}

readonly record struct Vec2(int X, int Y)
{
    public static Vec2 operator +(Vec2 a, Vec2 b) => new(a.X + b.X, a.Y + b.Y);
}

class Mundo
{
    private readonly string[] _mapa;

    public Vec2 Ceci { get; private set; }

    public Mundo(string[] mapa, Vec2 inicio)
    {
        _mapa = mapa;
        Ceci = inicio;
    }

    private bool EsSeto(Vec2 p) => _mapa[p.X][p.Y] == '#';

    public bool Mover(Vec2 paso)
    {
        Vec2 destino = Ceci + paso;
        if (EsSeto(destino))
        {
            return false;
        }
        Ceci = destino;
        return true;
    }
}
```

#### Salida esperada
```
Camina a 2,1
Camina a 3,1
Hay un seto
Camina a 4,1
Hay un seto
```

#### Solución
```csharp
string[] nivel =
{
    "######",
    "#C...#",
    "#.##.#",
    "######",
};
Mundo mundo = new Mundo(nivel, new Vec2(1, 1));

foreach (Vec2 paso in new Vec2[] { new(1, 0), new(1, 0), new(0, 1), new(1, 0), new(1, 0) })
{
    Console.WriteLine(mundo.Mover(paso) ? $"Camina a {mundo.Ceci.X},{mundo.Ceci.Y}" : "Hay un seto");
}

readonly record struct Vec2(int X, int Y)
{
    public static Vec2 operator +(Vec2 a, Vec2 b) => new(a.X + b.X, a.Y + b.Y);
}

class Mundo
{
    private readonly string[] _mapa;

    public Vec2 Ceci { get; private set; }

    public Mundo(string[] mapa, Vec2 inicio)
    {
        _mapa = mapa;
        Ceci = inicio;
    }

    private bool EsSeto(Vec2 p) => _mapa[p.Y][p.X] == '#';

    public bool Mover(Vec2 paso)
    {
        Vec2 destino = Ceci + paso;
        if (EsSeto(destino))
        {
            return false;
        }
        Ceci = destino;
        return true;
    }
}
```

#### Al superarla
Ahora los setos están donde se ven. El ogro se rasca la cabeza, mira el mapa dado vuelta que tenía en la mano, lo endereza y se va. —Primero el renglón —dice {mentor}—. Siempre.

#### Imagen
- Un laberinto de setos verdes con faroles, de noche, sin letras.
- un ogro de caricatura, grandote y simpático, de piel gris azulada, con chaleco de cuero cerrado, mira confundido un plano de papel liso que tiene dado vuelta; Ceci camina tranquila por el pasillo de al lado; Clave, arriba en una escalinata, levanta una ceja.

### Micro-misión R06-N03-P4 · El guardián que se acerca

```meta
lugar: El Jardín de los Setos
personajes: Ceci, Clave, Gheco
carta: La inteligencia | Select: los 4 vecinos · Where: los que no son seto · DefaultIfEmpty: si no hay, se queda · MinBy: el más cerca
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
El guardián de piedra persigue a Ceci, pero camina derecho contra los setos y se queda incrustado entre las hojas, con los pies para afuera.

#### Gheco sugiere
La consulta elige el vecino más cercano a Ceci, pero **no mira si es seto**. Entre el `Select` y el `DefaultIfEmpty` falta un filtro que se quede solo con los que se pueden pisar:

```csharp
.Where(p => !EsSeto(p))
```

Leé la consulta de arriba abajo, como una receta: los cuatro vecinos, **los que no son seto**, si no queda ninguno me quedo donde estoy, y de esos, el que más me acerca.

#### Desafío
Agregá el `Where` que descarta los setos en la consulta del guardián.

#### Código inicial
```csharp
string[] nivel =
{
    "#######",
    "#.C...#",
    "###.#.#",
    "#....E#",
    "#######",
};
Mundo mundo = new Mundo(nivel, new Vec2(2, 1), new Vec2(5, 3));
for (int turno = 1; turno <= 4; turno++)
{
    mundo.MoverGuardian();
    Console.WriteLine($"Turno {turno}: el guardián está en {mundo.Guardian.X},{mundo.Guardian.Y}");
}

readonly record struct Vec2(int X, int Y)
{
    public static Vec2 operator +(Vec2 a, Vec2 b) => new(a.X + b.X, a.Y + b.Y);
    public int DistanciaA(Vec2 otro) => Math.Abs(X - otro.X) + Math.Abs(Y - otro.Y);
}

class Mundo
{
    private readonly string[] _mapa;
    private readonly Vec2 _ceci;

    public Vec2 Guardian { get; private set; }

    public Mundo(string[] mapa, Vec2 ceci, Vec2 guardian)
    {
        _mapa = mapa;
        _ceci = ceci;
        Guardian = guardian;
    }

    private bool EsSeto(Vec2 p) => _mapa[p.Y][p.X] == '#';

    public void MoverGuardian()
    {
        Vec2[] pasos = { new(1, 0), new(-1, 0), new(0, 1), new(0, -1) };
        Vec2 actual = Guardian;
        Guardian = pasos
            .Select(p => actual + p)
            .DefaultIfEmpty(actual)
            .MinBy(p => p.DistanciaA(_ceci));
    }
}
```

#### Salida esperada
```
Turno 1: el guardián está en 4,3
Turno 2: el guardián está en 3,3
Turno 3: el guardián está en 2,3
Turno 4: el guardián está en 3,3
```

#### Solución
```csharp
string[] nivel =
{
    "#######",
    "#.C...#",
    "###.#.#",
    "#....E#",
    "#######",
};
Mundo mundo = new Mundo(nivel, new Vec2(2, 1), new Vec2(5, 3));
for (int turno = 1; turno <= 4; turno++)
{
    mundo.MoverGuardian();
    Console.WriteLine($"Turno {turno}: el guardián está en {mundo.Guardian.X},{mundo.Guardian.Y}");
}

readonly record struct Vec2(int X, int Y)
{
    public static Vec2 operator +(Vec2 a, Vec2 b) => new(a.X + b.X, a.Y + b.Y);
    public int DistanciaA(Vec2 otro) => Math.Abs(X - otro.X) + Math.Abs(Y - otro.Y);
}

class Mundo
{
    private readonly string[] _mapa;
    private readonly Vec2 _ceci;

    public Vec2 Guardian { get; private set; }

    public Mundo(string[] mapa, Vec2 ceci, Vec2 guardian)
    {
        _mapa = mapa;
        _ceci = ceci;
        Guardian = guardian;
    }

    private bool EsSeto(Vec2 p) => _mapa[p.Y][p.X] == '#';

    public void MoverGuardian()
    {
        Vec2[] pasos = { new(1, 0), new(-1, 0), new(0, 1), new(0, -1) };
        Vec2 actual = Guardian;
        Guardian = pasos
            .Select(p => actual + p)
            .Where(p => !EsSeto(p))
            .DefaultIfEmpty(actual)
            .MinBy(p => p.DistanciaA(_ceci));
    }
}
```

#### Al superarla
El guardián ya no se mete en los setos: avanza por el pasillo de abajo, lento, siempre hacia Ceci. Pero cuando un seto le tapa el camino, se queda yendo y viniendo, sin saber rodearlo. Gheco, desde el hombro de Ceci, le saca la lengua. —No lo provoques —le dice ella—. Es lento, pero no se cansa. —Y ahí está la gracia del juego —dice {mentor}.

#### Imagen
- Un laberinto de setos verdes con faroles, de noche, sin letras.
- Un guardián de piedra gris, redondito y de caricatura, con ojos de luz celeste, camina despacio por el pasillo; al fondo, Ceci lo mira, y Gheco, un gecko de luz cian con antiparras, MINÚSCULO, sentado en el hombro de Ceci, más chico que su cabeza, le saca la lengua.

### Micro-misión R06-N03-P5 · El récord que no se rompe

```meta
lugar: El Jardín de los Setos
personajes: Ceci, Bemol
carta: El récord | JsonSerializer.Serialize / Deserialize<T> · try / catch (JsonException) · un archivo roto: se arranca de cero
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
Bemol abrió `record.json` "para mirar" y le borró la mitad. Ahora el juego explota apenas arranca.

#### Gheco sugiere
`JsonSerializer.Deserialize` lanza una `JsonException` si el texto no es un JSON válido. Un récord roto no debería romper el juego: atrapala y arrancá de cero.

```csharp
try
{
    return JsonSerializer.Deserialize<Puntaje>(File.ReadAllText(Ruta)) ?? new Puntaje("nadie", 0);
}
catch (JsonException)
{
    return new Puntaje("nadie", 0);
}
```

Fijate que se atrapa **solo** `JsonException`: el error que sabemos explicar. Cualquier otro, que se vea.

#### Desafío
Envolvé la lectura de `CargarRecord` en un `try` que atrape `JsonException` y devuelva `new Puntaje("nadie", 0)`.

#### Código inicial
```csharp
using System.Text.Json;

const string Ruta = "record.json";
File.WriteAllText(Ruta, "{\"Nombre\":\"Bem");

Puntaje mejor = CargarRecord();
Console.WriteLine($"Récord: {mejor.Nombre} con {mejor.Puntos}");

GuardarRecord(new Puntaje("Ceci", 40));
mejor = CargarRecord();
Console.WriteLine($"Récord: {mejor.Nombre} con {mejor.Puntos}");

Puntaje CargarRecord()
{
    if (!File.Exists(Ruta))
    {
        return new Puntaje("nadie", 0);
    }
    return JsonSerializer.Deserialize<Puntaje>(File.ReadAllText(Ruta)) ?? new Puntaje("nadie", 0);
}

void GuardarRecord(Puntaje puntaje)
{
    File.WriteAllText(Ruta, JsonSerializer.Serialize(puntaje));
}

record Puntaje(string Nombre, int Puntos);
```

#### Salida esperada
```
Récord: nadie con 0
Récord: Ceci con 40
```

#### Solución
```csharp
using System.Text.Json;

const string Ruta = "record.json";
File.WriteAllText(Ruta, "{\"Nombre\":\"Bem");

Puntaje mejor = CargarRecord();
Console.WriteLine($"Récord: {mejor.Nombre} con {mejor.Puntos}");

GuardarRecord(new Puntaje("Ceci", 40));
mejor = CargarRecord();
Console.WriteLine($"Récord: {mejor.Nombre} con {mejor.Puntos}");

Puntaje CargarRecord()
{
    if (!File.Exists(Ruta))
    {
        return new Puntaje("nadie", 0);
    }
    try
    {
        return JsonSerializer.Deserialize<Puntaje>(File.ReadAllText(Ruta)) ?? new Puntaje("nadie", 0);
    }
    catch (JsonException)
    {
        return new Puntaje("nadie", 0);
    }
}

void GuardarRecord(Puntaje puntaje)
{
    File.WriteAllText(Ruta, JsonSerializer.Serialize(puntaje));
}

record Puntaje(string Nombre, int Puntos);
```

#### Al superarla
El juego arranca de cero, Ceci junta cuatro gemas y el récord queda guardado con su nombre. Bemol mira el archivo de lejos, con las manos en los bolsillos. —Yo no toqué nada.

#### Imagen
- La entrada de un laberinto de setos con faroles, de noche, con un pergamino de papel liso clavado en un poste de madera, sin letras.
- Bemol, gordito y con panza, silba mirando para otro lado con las manos en los bolsillos; Ceci clava un pergamino nuevo en el poste.

### Encargo R06-N03-E1 · Las butacas del Teatro

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Hilván necesita un plano de butacas para el Teatro de la Feria: 3 filas y 5 columnas, todas libres al empezar. Guardalo en una matriz `char[,]` con `L` (libre) y `X` (ocupada).

Leé reservas, una por línea, con el formato `fila,columna` (contando desde 1), hasta una línea vacía. Por cada una, mostrá:

- `Reservada F,C` si estaba libre (y marcala con `X`);
- `Ocupada F,C` si ya estaba reservada;
- `No existe F,C` si se sale del plano.

Al final, dibujá el plano (una fila por renglón, sin espacios) y `Libres: N`.

Con esta entrada:

```
1,1
2,3
1,1
4,2
3,5

```

se muestra:

```
Reservada 1,1
Reservada 2,3
Ocupada 1,1
No existe 4,2
Reservada 3,5
XLLLL
LLXLL
LLLLX
Libres: 12
```

#### Criterio de aprobación

- Usa una matriz `char[,]` y revisa los límites **antes** de mirar la casilla (sin atrapar excepciones).
- Cuenta las libres recorriendo la matriz.

#### Entrada de ejemplo

```
1,1
2,3
1,1
4,2
3,5

```

#### Salida esperada

```
Reservada 1,1
Reservada 2,3
Ocupada 1,1
No existe 4,2
Reservada 3,5
XLLLL
LLXLL
LLLLX
Libres: 12
```

#### Solución de referencia

```csharp
char[,] butacas = new char[3, 5];
for (int f = 0; f < 3; f++)
{
    for (int c = 0; c < 5; c++)
    {
        butacas[f, c] = 'L';
    }
}

string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    string[] partes = linea.Split(',');
    int fila = int.Parse(partes[0]);
    int columna = int.Parse(partes[1]);
    if (fila < 1 || fila > 3 || columna < 1 || columna > 5)
    {
        Console.WriteLine($"No existe {fila},{columna}");
    }
    else if (butacas[fila - 1, columna - 1] == 'X')
    {
        Console.WriteLine($"Ocupada {fila},{columna}");
    }
    else
    {
        butacas[fila - 1, columna - 1] = 'X';
        Console.WriteLine($"Reservada {fila},{columna}");
    }
    linea = Console.ReadLine();
}

int libres = 0;
for (int f = 0; f < 3; f++)
{
    string renglon = "";
    for (int c = 0; c < 5; c++)
    {
        renglon += butacas[f, c];
        if (butacas[f, c] == 'L')
        {
            libres++;
        }
    }
    Console.WriteLine(renglon);
}
Console.WriteLine($"Libres: {libres}");
```

## R06-N04 · Proyecto: el Libro Mayor

```meta
tipo: tema
padre: R06-N03
precio: 10
criatura: goblin
temas: diseno.capas, diseno.inyeccion
usa: poo.records, poo.interfaces, err.excepciones, func.streams, cal.pruebas, col.listas
```

### Crónica

El taller de Don Cedro está lleno de papelitos: en la caja, en los cajones, pinchados en un clavo. Cada venta, un papelito. Cada mes, la cuenta no da.

—Los perdí otra vez —dice Don Cedro, revolviendo—. Vendí doce juegos de cuerdas, eso seguro. O diez.

{mentor} le pone a Ceci el **sello del Conservatorio** en la mano. —Lo que aprendiste no era solo para pelear dragones —dice—. Era para esto. Este programa no tiene monstruos: tiene **clientes**. —Mira a Don Cedro, que discute con uno por el precio de la resina—. Que son peores.

### Objetivos

- Dividir un programa en **capas**, cada una con un solo trabajo.
- Poner todas las **reglas** en un solo lugar, que falla con excepciones claras.
- Cambiar **dónde se guardan** los datos sin tocar las reglas, con una interfaz.
- Usar `record` y `with` para datos que no se cambian: se reemplazan.
- **Probar** las reglas con xUnit, sin archivos ni pantalla.

### Antes de empezar

- Interfaces (R02-N09), `record` (R02-N05), LINQ (R03-N08 y R03-N09), excepciones propias (R04-N02) y pruebas con xUnit (R05-N04).

### Explicación

#### Capas

```
Program        la consola: pide datos y muestra resultados
   |
Tienda         las REGLAS: no lee el teclado ni escribe en la pantalla
   |
IRepositorio   la promesa: "guardame esto, dame lo guardado"
   |
Repositorio…   el detalle: en memoria, en un archivo JSON o en SQLite
```

Cada capa **solo conoce a la de abajo**. Gracias a eso:

- se puede cambiar el JSON por SQLite escribiendo **otro** repositorio, sin tocar `Tienda`;
- se puede cambiar la consola por una ventanilla web (como la del Acto V), sin tocar `Tienda`;
- se puede **probar** `Tienda` con un repositorio de mentira, sin archivos.

#### La tienda recibe su repositorio

`Tienda` no crea su repositorio: lo **recibe** en el constructor.

```csharp
Tienda tienda = new Tienda(new RepositorioMemoria());
```

A esto se lo llama **inyección de dependencias**: la tienda depende de "algo que guarde", y quien la crea decide qué. Es lo mismo que la partida de la Arena recibiendo su `Random`.

#### Las reglas, en un solo lugar

Toda regla importante (no vender más de lo que hay, no repetir códigos, no cantidades negativas) está en `Tienda`, y si se rompe, **lanza una excepción** con un mensaje claro:

```csharp
if (cantidad > producto.Stock)
{
    throw new StockInsuficienteException(producto.Nombre, producto.Stock);
}
```

La consola atrapa **solo** las excepciones que sabe explicar, y muestra el mensaje. Un error de programación no se esconde: explota y se ve.

#### `record` y `with`

`Producto` es un `record`: sus datos no se cambian. Para bajar el stock, se crea un producto **nuevo**, igual al anterior salvo en lo que se indica, y reemplaza al viejo en la lista:

```csharp
_productos[i] = producto with { Stock = producto.Stock - cantidad };
```

Un `record` también puede tener propiedades calculadas: `public decimal ValorTotal => Precio * Stock;`.

#### Una lista que se mira y no se toca

```csharp
public IReadOnlyList<Producto> Productos => _productos;
```

Desde afuera se puede recorrer y leer, pero no agregar ni borrar. Protege la lista, como `private set` protege un dato.

#### El dinero, en `decimal`

Precios e importes van en `decimal`, nunca en `double`: `0.1 + 0.2` en `double` no da exactamente `0.3`, y en una caja eso es plata que falta.

### Código de ejemplo

```csharp
Tienda tienda = new Tienda(new RepositorioMemoria());
tienda.Alta("C1", "Cuerdas", 1500.50m, 10);
tienda.Alta("R1", "Resina", 800m, 4);

try
{
    Venta venta = tienda.Vender("C1", 3);
    Console.WriteLine($"Venta por {venta.Importe:F2}");
    tienda.Vender("R1", 9);
}
catch (StockInsuficienteException e)
{
    Console.WriteLine(e.Message);
}

foreach (Producto p in tienda.Productos)
{
    Console.WriteLine($"{p.Codigo,-4}{p.Nombre,-10}{p.Precio,10:F2}{p.Stock,4}");
}

record Producto(string Codigo, string Nombre, decimal Precio, int Stock);
record Venta(string Codigo, int Cantidad, decimal Importe);

class StockInsuficienteException : Exception
{
    public StockInsuficienteException(string nombre, int disponible) : base($"Solo quedan {disponible} de {nombre}") { }
}

interface IRepositorio
{
    List<Producto> Productos();
    List<Venta> Ventas();
    void Guardar(List<Producto> productos, List<Venta> ventas);
}

class RepositorioMemoria : IRepositorio
{
    private readonly List<Producto> _productos = new();
    private readonly List<Venta> _ventas = new();

    public List<Producto> Productos() => _productos;
    public List<Venta> Ventas() => _ventas;
    public void Guardar(List<Producto> productos, List<Venta> ventas) { }
}

class Tienda
{
    private readonly IRepositorio _repositorio;
    private readonly List<Producto> _productos;
    private readonly List<Venta> _ventas;

    public Tienda(IRepositorio repositorio)
    {
        _repositorio = repositorio;
        _productos = repositorio.Productos();
        _ventas = repositorio.Ventas();
    }

    public IReadOnlyList<Producto> Productos => _productos;

    public void Alta(string codigo, string nombre, decimal precio, int stock)
    {
        _productos.Add(new Producto(codigo, nombre, precio, stock));
        _repositorio.Guardar(_productos, _ventas);
    }

    public Venta Vender(string codigo, int cantidad)
    {
        int i = _productos.FindIndex(p => p.Codigo == codigo);
        Producto producto = _productos[i];
        if (cantidad > producto.Stock)
        {
            throw new StockInsuficienteException(producto.Nombre, producto.Stock);
        }
        _productos[i] = producto with { Stock = producto.Stock - cantidad };
        Venta venta = new(codigo, cantidad, cantidad * producto.Precio);
        _ventas.Add(venta);
        _repositorio.Guardar(_productos, _ventas);
        return venta;
    }
}
```

### Salida esperada

```
Venta por 4501,50
Solo quedan 4 de Resina
C1  Cuerdas      1500,50   7
R1  Resina        800,00   4
```

### ¿Para qué sirve?

Así está armado casi todo programa "de verdad": un sistema de ventas, una biblioteca, un turnero, un juego con partidas guardadas. Las reglas en el medio, protegidas y probadas; la pantalla y el guardado, en los bordes, para poder cambiarlos sin miedo.

### Errores habituales

- **Ogro: la regla en la consola.** Si la consola revisa el stock, la ventanilla web del futuro no lo va a revisar. Las reglas van en `Tienda`.
- **Goblin: el precio en `double`.** Para dinero, siempre `decimal` (con la `m` al final: `1500.50m`).
- **Cambiar un `record`:** `producto.Stock -= 3` no compila (CS8852). Se crea otro con `with`.
- **Atrapar `Exception`:** esconde los errores de programación. Se atrapan solo las que se saben explicar.

### Micro-misión R06-N04-P1 · El stock con with

```meta
lugar: El taller de Don Cedro
personajes: Ceci, Don Cedro
carta: with | producto with { Stock = producto.Stock - 3 } · crea uno nuevo igual, salvo en eso · y reemplaza al viejo en la lista
recompensa: xp 20, oro 20, monedas 4
```

#### Escena
Don Cedro vende tres juegos de cuerdas y quiere bajar el stock, pero el ensayo general no lo deja: el producto no se puede cambiar.

#### Gheco sugiere
`Producto` es un `record` con propiedades que solo se escriben al crearlo: `Stock -= 3` da el error `CS8852`. Para "cambiarlo", se crea uno **nuevo** con `with`, y se lo pone en el lugar del viejo:

```csharp
productos[0] = cuerdas with { Stock = cuerdas.Stock - 3 };
```

`with` copia todo el producto y cambia solo lo que está entre llaves. El viejo no se toca: por eso nadie que lo esté mirando se lleva una sorpresa.

#### Desafío
Reemplazá `cuerdas.Stock -= 3;` por una línea con `with` que ponga el producto nuevo en la lista.

#### Código inicial
```csharp
List<Producto> productos = [new Producto("C1", "Cuerdas", 1500.50m, 10)];

Producto cuerdas = productos[0];
cuerdas.Stock -= 3;

Console.WriteLine($"Antes: {cuerdas.Stock}");
Console.WriteLine($"Ahora: {productos[0].Stock}");
Console.WriteLine($"Valor del stock: {productos[0].ValorTotal:F2}");

record Producto(string Codigo, string Nombre, decimal Precio, int Stock)
{
    public decimal ValorTotal => Precio * Stock;
}
```

#### Salida esperada
```
Antes: 10
Ahora: 7
Valor del stock: 10503,50
```

#### Solución
```csharp
List<Producto> productos = [new Producto("C1", "Cuerdas", 1500.50m, 10)];

Producto cuerdas = productos[0];
productos[0] = cuerdas with { Stock = cuerdas.Stock - 3 };

Console.WriteLine($"Antes: {cuerdas.Stock}");
Console.WriteLine($"Ahora: {productos[0].Stock}");
Console.WriteLine($"Valor del stock: {productos[0].ValorTotal:F2}");

record Producto(string Codigo, string Nombre, decimal Precio, int Stock)
{
    public decimal ValorTotal => Precio * Stock;
}
```

#### Al superarla
—Antes diez, ahora siete —lee Don Cedro—. Y el papelito de antes sigue diciendo diez, pero ya no es el que manda. —Lo mira contento—. Esto se lo voy a contar a mi señora.

#### Imagen
- Un taller de luthier de madera cálida con velas, con papelitos pinchados en un clavo y violines colgados, sin letras.
- Don Cedro, con delantal de cuero, despincha un papelito del clavo; Ceci, al lado, le muestra un cuaderno nuevo de tapas oscuras.

### Micro-misión R06-N04-P2 · La regla vive en la tienda

```meta
lugar: El taller de Don Cedro
personajes: Ceci, Don Cedro
carta: Las reglas | la Tienda lanza: throw new StockInsuficienteException(…) · la consola atrapa y muestra · nunca stock negativo
recompensa: xp 20, oro 20
```

#### Escena
Un cliente pide ocho cajitas de resina y Don Cedro tiene tres. El programa se las vende igual, y el stock queda en menos cinco.

#### Gheco sugiere
`Vender` no revisa si alcanza. La regla tiene que estar **en la tienda**, para que valga desde la consola, desde la ventanilla y desde cualquier lado. Antes de bajar el stock:

```csharp
if (cantidad > producto.Stock)
{
    throw new StockInsuficienteException(producto.Nombre, producto.Stock);
}
```

El programa ya atrapa esa excepción y muestra su mensaje. Fijate que, si se lanza, el resto de `Vender` no se ejecuta: la venta no se registra a medias.

#### Desafío
Agregá en `Vender` la regla que lanza `StockInsuficienteException` si no alcanza el stock.

#### Código inicial
```csharp
Tienda tienda = new Tienda();
tienda.Alta("R1", "Resina", 800m, 3);

foreach (int cantidad in new[] { 8, 2 })
{
    try
    {
        Venta venta = tienda.Vender("R1", cantidad);
        Console.WriteLine($"Venta por {venta.Importe:F2}");
    }
    catch (StockInsuficienteException e)
    {
        Console.WriteLine(e.Message);
    }
}
Console.WriteLine($"Stock de resina: {tienda.Productos[0].Stock}");

record Producto(string Codigo, string Nombre, decimal Precio, int Stock);
record Venta(string Codigo, int Cantidad, decimal Importe);

class StockInsuficienteException : Exception
{
    public StockInsuficienteException(string nombre, int disponible) : base($"Solo quedan {disponible} de {nombre}") { }
}

class Tienda
{
    private readonly List<Producto> _productos = new();

    public IReadOnlyList<Producto> Productos => _productos;

    public void Alta(string codigo, string nombre, decimal precio, int stock)
    {
        _productos.Add(new Producto(codigo, nombre, precio, stock));
    }

    public Venta Vender(string codigo, int cantidad)
    {
        int i = _productos.FindIndex(p => p.Codigo == codigo);
        Producto producto = _productos[i];
        _productos[i] = producto with { Stock = producto.Stock - cantidad };
        return new Venta(codigo, cantidad, cantidad * producto.Precio);
    }
}
```

#### Salida esperada
```
Solo quedan 3 de Resina
Venta por 1600,00
Stock de resina: 1
```

#### Solución
```csharp
Tienda tienda = new Tienda();
tienda.Alta("R1", "Resina", 800m, 3);

foreach (int cantidad in new[] { 8, 2 })
{
    try
    {
        Venta venta = tienda.Vender("R1", cantidad);
        Console.WriteLine($"Venta por {venta.Importe:F2}");
    }
    catch (StockInsuficienteException e)
    {
        Console.WriteLine(e.Message);
    }
}
Console.WriteLine($"Stock de resina: {tienda.Productos[0].Stock}");

record Producto(string Codigo, string Nombre, decimal Precio, int Stock);
record Venta(string Codigo, int Cantidad, decimal Importe);

class StockInsuficienteException : Exception
{
    public StockInsuficienteException(string nombre, int disponible) : base($"Solo quedan {disponible} de {nombre}") { }
}

class Tienda
{
    private readonly List<Producto> _productos = new();

    public IReadOnlyList<Producto> Productos => _productos;

    public void Alta(string codigo, string nombre, decimal precio, int stock)
    {
        _productos.Add(new Producto(codigo, nombre, precio, stock));
    }

    public Venta Vender(string codigo, int cantidad)
    {
        int i = _productos.FindIndex(p => p.Codigo == codigo);
        Producto producto = _productos[i];
        if (cantidad > producto.Stock)
        {
            throw new StockInsuficienteException(producto.Nombre, producto.Stock);
        }
        _productos[i] = producto with { Stock = producto.Stock - cantidad };
        return new Venta(codigo, cantidad, cantidad * producto.Precio);
    }
}
```

#### Al superarla
—"Solo quedan 3 de Resina" —lee el cliente en voz alta, y se lleva dos. Don Cedro respira. —Ni un frasquito de más —dice—. Ni uno de menos.

#### Imagen
- El mostrador de madera de un taller de luthier con velas, con tres frasquitos de resina dorada en fila, sin letras.
- Don Cedro, con delantal de cuero, pone una mano sobre los frasquitos; Ceci, al lado, sonríe.

### Micro-misión R06-N04-P3 · Otro repositorio

```meta
lugar: El taller de Don Cedro
personajes: Ceci, Clave
carta: Implementar la interfaz | class RepositorioMemoria : IRepositorio · cumplir cada método · la Tienda no cambia
recompensa: xp 20, oro 20
```

#### Escena
Don Cedro quiere probar el programa sin arriesgar su cuaderno de verdad. {mentor} propone un repositorio de mentira, en memoria. Ceci lo empezó, pero quedó a medias.

#### Gheco sugiere
`RepositorioMemoria` promete cumplir `IRepositorio`, pero su `Guardar` todavía tira `NotImplementedException` (la excepción de "esto no está hecho"). Completalo: como los datos ya están en las listas de memoria, alcanza con **contar** cuántas veces se guardó:

```csharp
public void Guardar(List<Producto> productos, List<Venta> ventas)
{
    Guardados++;
}
```

Mirá que `Tienda` no cambia nada: recibe "algo que guarde", y le da igual si es memoria, un JSON o SQLite.

#### Desafío
Completá `Guardar` en `RepositorioMemoria` para que sume 1 a `Guardados`.

#### Código inicial
```csharp
RepositorioMemoria memoria = new RepositorioMemoria();
Tienda tienda = new Tienda(memoria);
tienda.Alta("C1", "Cuerdas", 1500.50m, 10);
tienda.Alta("A1", "Arco", 9000m, 2);
Console.WriteLine($"Productos: {memoria.Productos().Count}");
Console.WriteLine($"Guardados: {memoria.Guardados}");

record Producto(string Codigo, string Nombre, decimal Precio, int Stock);
record Venta(string Codigo, int Cantidad, decimal Importe);

interface IRepositorio
{
    List<Producto> Productos();
    List<Venta> Ventas();
    void Guardar(List<Producto> productos, List<Venta> ventas);
}

class RepositorioMemoria : IRepositorio
{
    private readonly List<Producto> _productos = new();
    private readonly List<Venta> _ventas = new();

    public int Guardados { get; private set; }

    public List<Producto> Productos() => _productos;
    public List<Venta> Ventas() => _ventas;

    public void Guardar(List<Producto> productos, List<Venta> ventas)
    {
        throw new NotImplementedException();
    }
}

class Tienda
{
    private readonly IRepositorio _repositorio;
    private readonly List<Producto> _productos;
    private readonly List<Venta> _ventas;

    public Tienda(IRepositorio repositorio)
    {
        _repositorio = repositorio;
        _productos = repositorio.Productos();
        _ventas = repositorio.Ventas();
    }

    public void Alta(string codigo, string nombre, decimal precio, int stock)
    {
        _productos.Add(new Producto(codigo, nombre, precio, stock));
        _repositorio.Guardar(_productos, _ventas);
    }
}
```

#### Salida esperada
```
Productos: 2
Guardados: 2
```

#### Solución
```csharp
RepositorioMemoria memoria = new RepositorioMemoria();
Tienda tienda = new Tienda(memoria);
tienda.Alta("C1", "Cuerdas", 1500.50m, 10);
tienda.Alta("A1", "Arco", 9000m, 2);
Console.WriteLine($"Productos: {memoria.Productos().Count}");
Console.WriteLine($"Guardados: {memoria.Guardados}");

record Producto(string Codigo, string Nombre, decimal Precio, int Stock);
record Venta(string Codigo, int Cantidad, decimal Importe);

interface IRepositorio
{
    List<Producto> Productos();
    List<Venta> Ventas();
    void Guardar(List<Producto> productos, List<Venta> ventas);
}

class RepositorioMemoria : IRepositorio
{
    private readonly List<Producto> _productos = new();
    private readonly List<Venta> _ventas = new();

    public int Guardados { get; private set; }

    public List<Producto> Productos() => _productos;
    public List<Venta> Ventas() => _ventas;

    public void Guardar(List<Producto> productos, List<Venta> ventas)
    {
        Guardados++;
    }
}

class Tienda
{
    private readonly IRepositorio _repositorio;
    private readonly List<Producto> _productos;
    private readonly List<Venta> _ventas;

    public Tienda(IRepositorio repositorio)
    {
        _repositorio = repositorio;
        _productos = repositorio.Productos();
        _ventas = repositorio.Ventas();
    }

    public void Alta(string codigo, string nombre, decimal precio, int stock)
    {
        _productos.Add(new Producto(codigo, nombre, precio, stock));
        _repositorio.Guardar(_productos, _ventas);
    }
}
```

#### Al superarla
—Dos productos, dos guardados —dice {mentor}—. Y la tienda no se enteró de que no hay ningún cuaderno. Mañana le das uno de verdad, y tampoco se va a enterar.

#### Imagen
- Un taller de luthier de madera cálida con velas, sin letras.
- Clave sostiene un cuaderno de tapas oscuras con una mano y uno de papel transparente, de luz, con la otra, como comparándolos; Ceci la mira atenta.

### Micro-misión R06-N04-P4 · El más vendido

```meta
lugar: El taller de Don Cedro
personajes: Ceci, Don Cedro
carta: Agrupar | GroupBy(v => v.Codigo) · OrderByDescending(g => g.Sum(v => v.Cantidad)) · Select(g => g.Key).FirstOrDefault()
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
El informe dice que lo más vendido es el arco. Don Cedro vendió un solo arco en todo el mes. Lo que más vendió fueron cuerdas.

#### Gheco sugiere
`MasVendido` devuelve el código de la **primera** venta, no del más vendido. Hay que **agrupar** las ventas por código, sumar las cantidades de cada grupo y quedarse con el que más suma:

```csharp
_ventas.GroupBy(v => v.Codigo)
    .OrderByDescending(g => g.Sum(v => v.Cantidad))
    .Select(g => g.Key)
    .FirstOrDefault();
```

Cada grupo tiene su `Key` (el código) y adentro, sus ventas. `FirstOrDefault` da `null` si no hubo ninguna venta.

#### Desafío
Escribí `MasVendido` con `GroupBy`, para que devuelva el código que más cantidad vendió.

#### Código inicial
```csharp
List<Venta> ventas =
[
    new("A1", 1, 9000m),
    new("C1", 3, 4501.50m),
    new("R1", 2, 1600m),
    new("C1", 4, 6002m),
];
Informe informe = new Informe(ventas);
Console.WriteLine($"Facturado: {informe.TotalFacturado():F2}");
Console.WriteLine($"Más vendido: {informe.MasVendido() ?? "(sin ventas)"}");

record Venta(string Codigo, int Cantidad, decimal Importe);

class Informe
{
    private readonly List<Venta> _ventas;

    public Informe(List<Venta> ventas)
    {
        _ventas = ventas;
    }

    public decimal TotalFacturado() => _ventas.Sum(v => v.Importe);

    public string? MasVendido() => _ventas.Select(v => v.Codigo).FirstOrDefault();
}
```

#### Salida esperada
```
Facturado: 21103,50
Más vendido: C1
```

#### Solución
```csharp
List<Venta> ventas =
[
    new("A1", 1, 9000m),
    new("C1", 3, 4501.50m),
    new("R1", 2, 1600m),
    new("C1", 4, 6002m),
];
Informe informe = new Informe(ventas);
Console.WriteLine($"Facturado: {informe.TotalFacturado():F2}");
Console.WriteLine($"Más vendido: {informe.MasVendido() ?? "(sin ventas)"}");

record Venta(string Codigo, int Cantidad, decimal Importe);

class Informe
{
    private readonly List<Venta> _ventas;

    public Informe(List<Venta> ventas)
    {
        _ventas = ventas;
    }

    public decimal TotalFacturado() => _ventas.Sum(v => v.Importe);

    public string? MasVendido() =>
        _ventas.GroupBy(v => v.Codigo)
            .OrderByDescending(g => g.Sum(v => v.Cantidad))
            .Select(g => g.Key)
            .FirstOrDefault();
}
```

#### Al superarla
—¡Cuerdas! —dice Don Cedro, y golpea el mostrador—. Lo sabía. Siempre se cortan. —Se queda pensando—. Voy a pedir el doble.

#### Imagen
- Un taller de luthier de madera cálida con velas, con muchos rollitos de cuerdas de violín colgados en una pared, sin letras.
- Don Cedro, con delantal de cuero, golpea el mostrador con la palma, contento; Ceci levanta un rollito de cuerdas.

### Micro-misión R06-N04-P5 · Las pruebas del Libro

```meta
lugar: El taller de Don Cedro
personajes: Ceci, Clave, Gheco
carta: Pruebas | [Fact] un caso · [Theory] + [InlineData] varios · una prueba en rojo: se arregla el programa
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
Antes de darle el programa a Don Cedro, {mentor} corre las pruebas. Pasan casi todas. Una, no: la tienda acepta vender cero cuerdas, y menos una.

#### Gheco sugiere
La prueba `Vender_CantidadInvalida` espera que vender `0` o `-1` lance `ArgumentOutOfRangeException`, pero `Vender` no revisa eso. No se borra la prueba: se arregla la tienda. Al principio de `Vender`:

```csharp
if (cantidad <= 0)
{
    throw new ArgumentOutOfRangeException(nameof(cantidad), "La cantidad tiene que ser positiva");
}
```

Mirá también cómo se prueba sin archivos: las pruebas le dan a la tienda un `RepositorioFalso`, en memoria. Y el constructor de la clase de pruebas prepara cada una, porque xUnit crea un objeto nuevo por prueba.

#### Desafío
Agregá en `Vender` la regla que rechaza las cantidades que no son positivas, para que pasen todas las pruebas.

#### Código inicial
```csharp
using Xunit;

public class TiendaTests
{
    private readonly Tienda _tienda;

    public TiendaTests()
    {
        _tienda = new Tienda(new RepositorioFalso());
        _tienda.Alta("C1", "Cuerdas", 100m, 10);
    }

    [Fact]
    public void Vender_DescuentaStock()
    {
        Venta venta = _tienda.Vender("C1", 3);
        Assert.Equal(300m, venta.Importe);
        Assert.Equal(7, _tienda.Productos[0].Stock);
    }

    [Fact]
    public void Vender_SinStock()
    {
        Assert.Throws<StockInsuficienteException>(() => _tienda.Vender("C1", 11));
        Assert.Equal(10, _tienda.Productos[0].Stock);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    public void Vender_CantidadInvalida(int cantidad)
    {
        Assert.Throws<ArgumentOutOfRangeException>(() => _tienda.Vender("C1", cantidad));
    }
}

public record Producto(string Codigo, string Nombre, decimal Precio, int Stock);
public record Venta(string Codigo, int Cantidad, decimal Importe);

public class StockInsuficienteException : Exception
{
    public StockInsuficienteException(string nombre, int disponible) : base($"Solo quedan {disponible} de {nombre}") { }
}

public interface IRepositorio
{
    List<Producto> Productos();
    List<Venta> Ventas();
    void Guardar(List<Producto> productos, List<Venta> ventas);
}

public class RepositorioFalso : IRepositorio
{
    private readonly List<Producto> _productos = new();
    private readonly List<Venta> _ventas = new();

    public List<Producto> Productos() => _productos;
    public List<Venta> Ventas() => _ventas;
    public void Guardar(List<Producto> productos, List<Venta> ventas) { }
}

public class Tienda
{
    private readonly IRepositorio _repositorio;
    private readonly List<Producto> _productos;
    private readonly List<Venta> _ventas;

    public Tienda(IRepositorio repositorio)
    {
        _repositorio = repositorio;
        _productos = repositorio.Productos();
        _ventas = repositorio.Ventas();
    }

    public IReadOnlyList<Producto> Productos => _productos;

    public void Alta(string codigo, string nombre, decimal precio, int stock)
    {
        _productos.Add(new Producto(codigo, nombre, precio, stock));
        _repositorio.Guardar(_productos, _ventas);
    }

    public Venta Vender(string codigo, int cantidad)
    {
        int i = _productos.FindIndex(p => p.Codigo == codigo);
        Producto producto = _productos[i];
        if (cantidad > producto.Stock)
        {
            throw new StockInsuficienteException(producto.Nombre, producto.Stock);
        }
        _productos[i] = producto with { Stock = producto.Stock - cantidad };
        Venta venta = new(codigo, cantidad, cantidad * producto.Precio);
        _ventas.Add(venta);
        _repositorio.Guardar(_productos, _ventas);
        return venta;
    }
}
```

#### Salida esperada
```
Corriendo las pruebas…
  ✓ TiendaTests.Vender_DescuentaStock
  ✓ TiendaTests.Vender_SinStock
  ✓ TiendaTests.Vender_CantidadInvalida(0)
  ✓ TiendaTests.Vender_CantidadInvalida(-1)

Pasaron 4 de 4 pruebas. ✓ Todo en verde.
```

#### Solución
```csharp
using Xunit;

public class TiendaTests
{
    private readonly Tienda _tienda;

    public TiendaTests()
    {
        _tienda = new Tienda(new RepositorioFalso());
        _tienda.Alta("C1", "Cuerdas", 100m, 10);
    }

    [Fact]
    public void Vender_DescuentaStock()
    {
        Venta venta = _tienda.Vender("C1", 3);
        Assert.Equal(300m, venta.Importe);
        Assert.Equal(7, _tienda.Productos[0].Stock);
    }

    [Fact]
    public void Vender_SinStock()
    {
        Assert.Throws<StockInsuficienteException>(() => _tienda.Vender("C1", 11));
        Assert.Equal(10, _tienda.Productos[0].Stock);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    public void Vender_CantidadInvalida(int cantidad)
    {
        Assert.Throws<ArgumentOutOfRangeException>(() => _tienda.Vender("C1", cantidad));
    }
}

public record Producto(string Codigo, string Nombre, decimal Precio, int Stock);
public record Venta(string Codigo, int Cantidad, decimal Importe);

public class StockInsuficienteException : Exception
{
    public StockInsuficienteException(string nombre, int disponible) : base($"Solo quedan {disponible} de {nombre}") { }
}

public interface IRepositorio
{
    List<Producto> Productos();
    List<Venta> Ventas();
    void Guardar(List<Producto> productos, List<Venta> ventas);
}

public class RepositorioFalso : IRepositorio
{
    private readonly List<Producto> _productos = new();
    private readonly List<Venta> _ventas = new();

    public List<Producto> Productos() => _productos;
    public List<Venta> Ventas() => _ventas;
    public void Guardar(List<Producto> productos, List<Venta> ventas) { }
}

public class Tienda
{
    private readonly IRepositorio _repositorio;
    private readonly List<Producto> _productos;
    private readonly List<Venta> _ventas;

    public Tienda(IRepositorio repositorio)
    {
        _repositorio = repositorio;
        _productos = repositorio.Productos();
        _ventas = repositorio.Ventas();
    }

    public IReadOnlyList<Producto> Productos => _productos;

    public void Alta(string codigo, string nombre, decimal precio, int stock)
    {
        _productos.Add(new Producto(codigo, nombre, precio, stock));
        _repositorio.Guardar(_productos, _ventas);
    }

    public Venta Vender(string codigo, int cantidad)
    {
        if (cantidad <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(cantidad), "La cantidad tiene que ser positiva");
        }
        int i = _productos.FindIndex(p => p.Codigo == codigo);
        Producto producto = _productos[i];
        if (cantidad > producto.Stock)
        {
            throw new StockInsuficienteException(producto.Nombre, producto.Stock);
        }
        _productos[i] = producto with { Stock = producto.Stock - cantidad };
        Venta venta = new(codigo, cantidad, cantidad * producto.Precio);
        _ventas.Add(venta);
        _repositorio.Guardar(_productos, _ventas);
        return venta;
    }
}
```

#### Al superarla
Todas en verde. {mentor} cierra el cuaderno de pruebas y se lo da a Don Cedro junto con el programa. —Cada vez que alguien lo toque —le dice—, que corra esto primero. Si algo se pone rojo, no se vende nada hasta arreglarlo.

#### Imagen
- Un taller de luthier de madera cálida con velas, con una fila de cuatro lucecitas verdes encendidas sobre el mostrador, sin letras.
- Clave le entrega a Don Cedro un cuaderno de tapas oscuras; Ceci sonríe; Gheco, un gecko de luz cian con antiparras, muy chiquito, más chico que una de las lucecitas, está sentado al lado de la fila de luces.

### Encargo R06-N04-E1 · El kiosco de Baldo

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Baldo vio el Libro Mayor de Don Cedro y quiere uno para su kiosco. Armalo con las mismas capas: `Producto` y `Venta` como `record`, una `Tienda` con las reglas (que recibe un `IRepositorio`) y un `RepositorioMemoria`.

Las reglas de la tienda: no se repiten códigos (`ArgumentException` con `Ya existe el código …`), no se vende un código que no existe (`ProductoNoEncontradoException` con `No existe el producto …`) ni más de lo que hay (`StockInsuficienteException` con `Solo quedan N de …`).

El programa lee órdenes, una por línea, hasta una línea vacía, con las partes separadas por `;`:

- `alta;código;nombre;precio;stock`: muestra `Producto agregado`;
- `vender;código;cantidad`: muestra `Venta por IMPORTE` (con dos decimales);
- `informe`: muestra `Facturado: …` (con dos decimales) y una línea `Reponer NOMBRE: quedan N` por cada producto con menos de 5, del que menos tiene al que más.

Si una orden rompe una regla, se muestra el mensaje de la excepción y se sigue.

Con esta entrada:

```
alta;A1;Alfajor;850;10
alta;G1;Gaseosa;1200;4
alta;A1;Otro;1;1
vender;A1;8
vender;G1;6
vender;ZZ;1
informe

```

se muestra:

```
Producto agregado
Producto agregado
Ya existe el código A1
Venta por 6800,00
Solo quedan 4 de Gaseosa
No existe el producto ZZ
Facturado: 6800,00
Reponer Alfajor: quedan 2
Reponer Gaseosa: quedan 4
```

#### Criterio de aprobación

- Las reglas están en `Tienda`, que no lee el teclado ni escribe en la pantalla.
- La consola atrapa solo las excepciones de las reglas, no `Exception`.
- El stock baja con `with`.

#### Entrada de ejemplo

```
alta;A1;Alfajor;850;10
alta;G1;Gaseosa;1200;4
alta;A1;Otro;1;1
vender;A1;8
vender;G1;6
vender;ZZ;1
informe

```

#### Salida esperada

```
Producto agregado
Producto agregado
Ya existe el código A1
Venta por 6800,00
Solo quedan 4 de Gaseosa
No existe el producto ZZ
Facturado: 6800,00
Reponer Alfajor: quedan 2
Reponer Gaseosa: quedan 4
```

#### Solución de referencia

```csharp
Tienda tienda = new Tienda(new RepositorioMemoria());

string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    string[] p = linea.Split(';');
    try
    {
        switch (p[0])
        {
            case "alta":
                tienda.Alta(p[1], p[2], decimal.Parse(p[3]), int.Parse(p[4]));
                Console.WriteLine("Producto agregado");
                break;
            case "vender":
                Venta venta = tienda.Vender(p[1], int.Parse(p[2]));
                Console.WriteLine($"Venta por {venta.Importe:F2}");
                break;
            case "informe":
                Console.WriteLine($"Facturado: {tienda.TotalFacturado():F2}");
                foreach (Producto producto in tienda.AReponer(5))
                {
                    Console.WriteLine($"Reponer {producto.Nombre}: quedan {producto.Stock}");
                }
                break;
        }
    }
    catch (ProductoNoEncontradoException e)
    {
        Console.WriteLine(e.Message);
    }
    catch (StockInsuficienteException e)
    {
        Console.WriteLine(e.Message);
    }
    catch (ArgumentException e)
    {
        Console.WriteLine(e.Message);
    }
    linea = Console.ReadLine();
}

record Producto(string Codigo, string Nombre, decimal Precio, int Stock);
record Venta(string Codigo, int Cantidad, decimal Importe);

class ProductoNoEncontradoException : Exception
{
    public ProductoNoEncontradoException(string codigo) : base($"No existe el producto {codigo}") { }
}

class StockInsuficienteException : Exception
{
    public StockInsuficienteException(string nombre, int disponible) : base($"Solo quedan {disponible} de {nombre}") { }
}

interface IRepositorio
{
    List<Producto> Productos();
    List<Venta> Ventas();
    void Guardar(List<Producto> productos, List<Venta> ventas);
}

class RepositorioMemoria : IRepositorio
{
    private readonly List<Producto> _productos = new();
    private readonly List<Venta> _ventas = new();

    public List<Producto> Productos() => _productos;
    public List<Venta> Ventas() => _ventas;
    public void Guardar(List<Producto> productos, List<Venta> ventas) { }
}

class Tienda
{
    private readonly IRepositorio _repositorio;
    private readonly List<Producto> _productos;
    private readonly List<Venta> _ventas;

    public Tienda(IRepositorio repositorio)
    {
        _repositorio = repositorio;
        _productos = repositorio.Productos();
        _ventas = repositorio.Ventas();
    }

    public void Alta(string codigo, string nombre, decimal precio, int stock)
    {
        if (_productos.Any(p => p.Codigo == codigo))
        {
            throw new ArgumentException($"Ya existe el código {codigo}");
        }
        _productos.Add(new Producto(codigo, nombre, precio, stock));
        _repositorio.Guardar(_productos, _ventas);
    }

    public Venta Vender(string codigo, int cantidad)
    {
        int i = _productos.FindIndex(p => p.Codigo == codigo);
        if (i < 0)
        {
            throw new ProductoNoEncontradoException(codigo);
        }
        Producto producto = _productos[i];
        if (cantidad > producto.Stock)
        {
            throw new StockInsuficienteException(producto.Nombre, producto.Stock);
        }
        _productos[i] = producto with { Stock = producto.Stock - cantidad };
        Venta venta = new(codigo, cantidad, cantidad * producto.Precio);
        _ventas.Add(venta);
        _repositorio.Guardar(_productos, _ventas);
        return venta;
    }

    public decimal TotalFacturado() => _ventas.Sum(v => v.Importe);

    public List<Producto> AReponer(int minimo) => _productos.Where(p => p.Stock < minimo).OrderBy(p => p.Stock).ToList();
}
```

## R06-N05 · Jefe final: el Dragón del Conservatorio

```meta
tipo: jefe
padre: R06-N04
precio: 10
criatura: dragon
insignia: Maestra del Conservatorio
insignia_descripcion: Venciste al Dragón del Conservatorio: armás programas grandes por piezas, con herencia, interfaces, colecciones, eventos, archivos y pruebas, y completaste la melodía del Vidriero.
usa: poo.polimorfismo, juegos.turnos, col.pilas-colas, func.streams, arch.json, cal.pruebas
```

### Crónica

La noche en que Ceci termina el Libro Mayor, la Arena se ilumina sola. Los faroles se prenden de a uno, las gradas crujen, y del fondo, donde siempre estuvo oscuro, sale **el Dragón del Conservatorio**: enorme, hecho de **partituras quemadas** que se pliegan como escamas, con ojos de brasa y un pecho que brilla como un horno. Cada tres compases, abre la boca y echa fuego. Y en el pecho, entre las escamas, brilla algo que no es fuego: **una escama de bronce con forma de sostenido**.

—Lo despertaron los papelitos de Don Cedro —dice {mentor}, sin moverse—. Se alimenta de lo que se escribe sin ensayar. Y esta vez, Ceci, no estoy yo para corregirte. Es tu concierto.

Bemol, en la grada, deja las garrapiñadas. Gheco se esconde en la capucha de Ceci. Ceci afina el violín.

—Cinco escamas —dice—. De a una.

### Objetivos

- Juntar en un solo programa todo el curso: clases, herencia, interfaces, colecciones, LINQ, archivos y pruebas.
- Encontrar y arreglar los errores **de a uno**.

### Antes de empezar

- Todos los proyectos: R06-N01 a R06-N04.

### Explicación

#### Qué usar para qué

| Necesito… | Uso |
|---|---|
| un molde común y cada hijo con su voz | clase `abstract`, `virtual` y `override` |
| cuidar los bordes | `Math.Min` y `Math.Max` |
| enchufar acciones sin tocar el resto | una interfaz y un `Dictionary` |
| atender en orden de llegada | `Queue`, con `Enqueue` y `Dequeue` |
| avisar sin escribir en la pantalla | un `event` y `+=` |
| ordenar y elegir los mejores | LINQ: `OrderByDescending`, `Take` |
| que algo se recuerde | JSON con `JsonSerializer` |
| saber que todo anda, siempre | pruebas con `[Fact]` y `[Theory]` |

#### Cómo se vence a un dragón

1. Ensayá y leé el **primer** error: línea y código (`CS…`).
2. Si explota, mirá el nombre de la excepción: te dice qué clase de monstruo es.
3. Si corre pero da otra cosa, compará tu salida con la esperada **renglón por renglón**: el primer renglón distinto te dice dónde mirar.
4. Una prueba en rojo no se borra: se lee, y se arregla el programa.

### Código de ejemplo

```csharp
List<Monstruo> oleada = [new Goblin(), new Dragon()];
Queue<Monstruo> fila = new(oleada);

while (fila.Count > 0)
{
    Monstruo m = fila.Dequeue();
    Console.WriteLine($"{m.Nombre}: turno 1 pega {m.ElegirGolpe(1)}, turno 3 pega {m.ElegirGolpe(3)}");
}

var mejores = new[] { ("Ceci", 135), ("Bemol", 20), ("Hilván", 60) }
    .OrderByDescending(j => j.Item2)
    .Take(2);
foreach (var (nombre, oro) in mejores)
{
    Console.WriteLine($"{nombre}: {oro}");
}

abstract class Monstruo
{
    public string Nombre { get; }
    public int Ataque { get; }

    protected Monstruo(string nombre, int ataque)
    {
        Nombre = nombre;
        Ataque = ataque;
    }

    public virtual int ElegirGolpe(int turno) => Ataque;
}

class Goblin : Monstruo
{
    public Goblin() : base("Goblin", 5) { }
}

class Dragon : Monstruo
{
    public Dragon() : base("Dragón", 10) { }

    public override int ElegirGolpe(int turno) => turno % 3 == 0 ? Ataque * 2 : Ataque;
}
```

### Salida esperada

```
Goblin: turno 1 pega 5, turno 3 pega 5
Dragón: turno 1 pega 10, turno 3 pega 20
Ceci: 135
Hilván: 60
```

### ¿Para qué sirve?

Un programa de verdad nunca es una sola idea: es todo junto. Y nunca sale bien la primera vez. Lo que hace a una programadora no es no equivocarse: es saber encontrar el error, arreglarlo y tener pruebas que avisen si vuelve.

### Errores habituales

- **Arreglar todo junto:** un error por vez. El siguiente aparece recién cuando arreglaste el anterior.
- **Cambiar la salida esperada en vez del programa:** la salida esperada es la partitura. Se toca lo que está escrito, no lo que tiene que sonar.
- **Borrar una prueba que falla:** la prueba avisa. Se arregla lo que avisa.

### Micro-misión R06-N05-P1 · Las escamas

```meta
lugar: La Arena del Conservatorio
personajes: Ceci, Clave
criatura: dragon
carta: Jefe | override de RecibirDanio · la mitad del golpe · Math.Max(…, 1): nunca 0
recompensa: xp 20, oro 20, monedas 4
```

#### Escena
Las escamas de partitura absorben la mitad de cada golpe. Pero cuando Ceci le pega flojito, con un golpe de 1, al dragón no le entra nada, y así la pelea no termina nunca.

#### Gheco sugiere
El `override` del dragón divide el golpe por 2. Con un golpe de 1, `1 / 2` da `0` (división entera): no le entra nada. Es un borde. Como con la piel del ogro, asegurá que entre **por lo menos 1**:

```csharp
public override int RecibirDanio(int cantidad) => base.RecibirDanio(Math.Max(cantidad / 2, 1));
```

#### Desafío
Usá `Math.Max` en el `override` del dragón para que cada golpe le saque por lo menos 1.

#### Código inicial
```csharp
Dragon dragon = new Dragon();
foreach (int golpe in new[] { 24, 9, 1, 1 })
{
    int real = dragon.RecibirDanio(golpe);
    Console.WriteLine($"Golpe de {golpe}: le entra {real}, le quedan {dragon.Vida}");
}

abstract class Entidad
{
    public string Nombre { get; }
    public int Vida { get; private set; }

    protected Entidad(string nombre, int vida)
    {
        Nombre = nombre;
        Vida = vida;
    }

    public virtual int RecibirDanio(int cantidad)
    {
        int real = Math.Min(cantidad, Vida);
        Vida -= real;
        return real;
    }
}

class Dragon : Entidad
{
    public Dragon() : base("Dragón", 90) { }

    public override int RecibirDanio(int cantidad) => base.RecibirDanio(cantidad / 2);
}
```

#### Salida esperada
```
Golpe de 24: le entra 12, le quedan 78
Golpe de 9: le entra 4, le quedan 74
Golpe de 1: le entra 1, le quedan 73
Golpe de 1: le entra 1, le quedan 72
```

#### Solución
```csharp
Dragon dragon = new Dragon();
foreach (int golpe in new[] { 24, 9, 1, 1 })
{
    int real = dragon.RecibirDanio(golpe);
    Console.WriteLine($"Golpe de {golpe}: le entra {real}, le quedan {dragon.Vida}");
}

abstract class Entidad
{
    public string Nombre { get; }
    public int Vida { get; private set; }

    protected Entidad(string nombre, int vida)
    {
        Nombre = nombre;
        Vida = vida;
    }

    public virtual int RecibirDanio(int cantidad)
    {
        int real = Math.Min(cantidad, Vida);
        Vida -= real;
        return real;
    }
}

class Dragon : Entidad
{
    public Dragon() : base("Dragón", 90) { }

    public override int RecibirDanio(int cantidad) => base.RecibirDanio(Math.Max(cantidad / 2, 1));
}
```

#### Al superarla
La primera escama de partitura se suelta del pecho del dragón y cae flotando, como una hoja. El dragón ruge, y las gradas tiemblan. —Una —dice Ceci.

#### Imagen
- Una arena redonda de piedra con gradas de madera y faroles, de noche; en el centro, un dragón enorme de caricatura hecho de partituras quemadas plegadas como escamas, sin letras ni notas escritas, con ojos de brasa naranja y el pecho brillando como un horno; una escama de papel se suelta y cae flotando.
- Ceci, con el violín en la mano y la capa al viento, lo enfrenta; Clave mira desde el borde de la arena.

### Micro-misión R06-N05-P2 · El fuego cada tres compases

```meta
lugar: La Arena del Conservatorio
personajes: Ceci, Bemol
criatura: dragon
carta: Jefe | el turno se cuenta antes de pegar · turno++ al principio · fuego en el 3 y en el 6, no en el 1
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
El dragón tenía que echar fuego en los compases 3 y 6. Pero lo echa en el primero, sin aviso, y Ceci apenas llega a cubrirse.

#### Gheco sugiere
El turno se suma **al final** de la vuelta, así que el primer golpe se hace con `turno` en `0`, y `0 % 3` da `0`: fuego. El turno se tiene que contar **antes** de pegar. Mové el `turno++` al principio del bucle:

```csharp
while (turno < 6)
{
    turno++;
    int golpe = dragon.ElegirGolpe(turno);
    ...
}
```

Así, el primer golpe es el del turno 1.

#### Desafío
Mové `turno++` al principio del bucle, antes de que el dragón elija su golpe.

#### Código inicial
```csharp
Dragon dragon = new Dragon();
int turno = 0;
while (turno < 6)
{
    int golpe = dragon.ElegirGolpe(turno);
    Console.WriteLine(golpe > dragon.Ataque ? $"Compás {turno}: ¡FUEGO! {golpe}" : $"Compás {turno}: zarpazo {golpe}");
    turno++;
}

class Dragon
{
    public int Ataque => 10;

    public int ElegirGolpe(int turno) => turno % 3 == 0 ? Ataque * 2 : Ataque;
}
```

#### Salida esperada
```
Compás 1: zarpazo 10
Compás 2: zarpazo 10
Compás 3: ¡FUEGO! 20
Compás 4: zarpazo 10
Compás 5: zarpazo 10
Compás 6: ¡FUEGO! 20
```

#### Solución
```csharp
Dragon dragon = new Dragon();
int turno = 0;
while (turno < 6)
{
    turno++;
    int golpe = dragon.ElegirGolpe(turno);
    Console.WriteLine(golpe > dragon.Ataque ? $"Compás {turno}: ¡FUEGO! {golpe}" : $"Compás {turno}: zarpazo {golpe}");
}

class Dragon
{
    public int Ataque => 10;

    public int ElegirGolpe(int turno) => turno % 3 == 0 ? Ataque * 2 : Ataque;
}
```

#### Al superarla
Ahora Ceci cuenta con el dragón: uno, dos… y en el tres se agacha, y la llamarada le pasa por arriba. La segunda escama se suelta. —¡Uno, dos, AGACHATE! —grita Bemol desde la grada, que ya lo aprendió.

#### Imagen
- Una arena redonda de piedra con faroles, de noche, con un dragón enorme de caricatura hecho de partituras quemadas que echa una llamarada naranja hacia arriba, sin letras ni notas escritas.
- Ceci se agacha y la llamarada le pasa por encima; en la grada, Bemol, gordito y con panza, hace bocina con las manos.

### Micro-misión R06-N05-P3 · La tabla de campeones

```meta
lugar: La Arena del Conservatorio
personajes: Ceci, Bemol, Don Cedro
criatura: dragon
carta: Jefe | OrderByDescending: del más grande al más chico · Take(3): los tres primeros · OrderBy los ordena al revés
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
En la pared de la Arena hay una tabla de campeones, guardada en un archivo. El dragón la dio vuelta: arriba aparecen los que menos oro juntaron.

#### Gheco sugiere
`OrderBy` ordena de **menor a mayor**: los tres primeros son los peores. Para los mejores, de mayor a menor, se usa `OrderByDescending`:

```csharp
List<Puntaje> mejores = tabla.OrderByDescending(p => p.Oro).Take(3).ToList();
```

`Take(3)` se queda con los tres primeros de lo que ya está ordenado.

#### Desafío
Cambiá `OrderBy` por `OrderByDescending` para que la tabla muestre a los tres que más oro juntaron.

#### Código inicial
```csharp
using System.Text.Json;

List<Puntaje> tabla =
[
    new("Bemol", 20),
    new("Ceci", 135),
    new("Hilván", 60),
    new("Don Cedro", 90),
    new("Nima", 110),
];
File.WriteAllText("campeones.json", JsonSerializer.Serialize(tabla));

List<Puntaje> leida = JsonSerializer.Deserialize<List<Puntaje>>(File.ReadAllText("campeones.json")) ?? [];
List<Puntaje> mejores = leida.OrderBy(p => p.Oro).Take(3).ToList();

Console.WriteLine("=== Campeones de la Arena ===");
for (int i = 0; i < mejores.Count; i++)
{
    Console.WriteLine($"{i + 1}. {mejores[i].Nombre,-10}{mejores[i].Oro,5}");
}

record Puntaje(string Nombre, int Oro);
```

#### Salida esperada
```
=== Campeones de la Arena ===
1. Ceci        135
2. Nima        110
3. Don Cedro    90
```

#### Solución
```csharp
using System.Text.Json;

List<Puntaje> tabla =
[
    new("Bemol", 20),
    new("Ceci", 135),
    new("Hilván", 60),
    new("Don Cedro", 90),
    new("Nima", 110),
];
File.WriteAllText("campeones.json", JsonSerializer.Serialize(tabla));

List<Puntaje> leida = JsonSerializer.Deserialize<List<Puntaje>>(File.ReadAllText("campeones.json")) ?? [];
List<Puntaje> mejores = leida.OrderByDescending(p => p.Oro).Take(3).ToList();

Console.WriteLine("=== Campeones de la Arena ===");
for (int i = 0; i < mejores.Count; i++)
{
    Console.WriteLine($"{i + 1}. {mejores[i].Nombre,-10}{mejores[i].Oro,5}");
}

record Puntaje(string Nombre, int Oro);
```

#### Al superarla
La tabla se endereza en la pared, y la tercera escama cae. Bemol busca su nombre y no lo encuentra. —Estoy cuarto —dice Don Cedro, ofendido—. Y eso que pago las cuerdas.

#### Imagen
- La pared de piedra de una arena con faroles, con una tabla de madera con tres medallas doradas colgadas en escalera, sin letras ni números.
- Bemol, gordito y con panza, y Don Cedro, con delantal de cuero, miran la tabla con los brazos cruzados; Ceci, más atrás, se ríe.

### Micro-misión R06-N05-P4 · Las pruebas del dragón

```meta
lugar: La Arena del Conservatorio
personajes: Ceci, Clave, Gheco
criatura: dragon
carta: Jefe | [Theory] con varios [InlineData] · la prueba dice qué tenía que dar · se arregla el programa, no la prueba
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
Ceci escribió pruebas para el dragón, para no tener que pelear cada vez que cambia algo. Pero cuatro se ponen rojas: el dragón echa fuego en los compases 1 y 4, y en el 3 y el 6 no.

#### Gheco sugiere
Las pruebas dicen, compás por compás, cuánto tiene que pegar. La primera prueba en rojo (`ElegirGolpe(1)`, que tenía que dar `10`) apunta a la condición: `turno % 3 == 1` es verdadera en los compases 1, 4, 7… El fuego va en los múltiplos de 3, donde el resto da **0**:

```csharp
public int ElegirGolpe(int turno) => turno % 3 == 0 ? Ataque * 2 : Ataque;
```

Fijate que no se toca ninguna prueba: dicen lo que **tiene que pasar**.

#### Desafío
Corregí la condición de `ElegirGolpe` para que pasen todas las pruebas.

#### Código inicial
```csharp
using Xunit;

public class DragonTests
{
    private readonly Dragon _dragon = new();

    [Theory]
    [InlineData(1, 10)]
    [InlineData(2, 10)]
    [InlineData(3, 20)]
    [InlineData(4, 10)]
    [InlineData(6, 20)]
    public void ElegirGolpe_FuegoCadaTres(int turno, int esperado)
    {
        Assert.Equal(esperado, _dragon.ElegirGolpe(turno));
    }

    [Fact]
    public void ElDragonEmpiezaConNoventa()
    {
        Assert.Equal(90, _dragon.Vida);
    }
}

public class Dragon
{
    public int Vida { get; } = 90;
    public int Ataque => 10;

    public int ElegirGolpe(int turno) => turno % 3 == 1 ? Ataque * 2 : Ataque;
}
```

#### Salida esperada
```
Corriendo las pruebas…
  ✓ DragonTests.ElegirGolpe_FuegoCadaTres(1, 10)
  ✓ DragonTests.ElegirGolpe_FuegoCadaTres(2, 10)
  ✓ DragonTests.ElegirGolpe_FuegoCadaTres(3, 20)
  ✓ DragonTests.ElegirGolpe_FuegoCadaTres(4, 10)
  ✓ DragonTests.ElegirGolpe_FuegoCadaTres(6, 20)
  ✓ DragonTests.ElDragonEmpiezaConNoventa

Pasaron 6 de 6 pruebas. ✓ Todo en verde.
```

#### Solución
```csharp
using Xunit;

public class DragonTests
{
    private readonly Dragon _dragon = new();

    [Theory]
    [InlineData(1, 10)]
    [InlineData(2, 10)]
    [InlineData(3, 20)]
    [InlineData(4, 10)]
    [InlineData(6, 20)]
    public void ElegirGolpe_FuegoCadaTres(int turno, int esperado)
    {
        Assert.Equal(esperado, _dragon.ElegirGolpe(turno));
    }

    [Fact]
    public void ElDragonEmpiezaConNoventa()
    {
        Assert.Equal(90, _dragon.Vida);
    }
}

public class Dragon
{
    public int Vida { get; } = 90;
    public int Ataque => 10;

    public int ElegirGolpe(int turno) => turno % 3 == 0 ? Ataque * 2 : Ataque;
}
```

#### Al superarla
Seis luces verdes se prenden en el borde de la Arena, una por prueba. La cuarta escama se suelta, y el dragón, por primera vez, retrocede. Gheco asoma la cabeza de la capucha de Ceci.

#### Imagen
- El borde de piedra de una arena con faroles, de noche, con seis lucecitas verdes encendidas en fila, sin letras; al fondo, un dragón enorme de caricatura hecho de partituras quemadas retrocede.
- Ceci con el violín en alto; Clave, a un costado; Gheco, un gecko de luz cian con antiparras, MINÚSCULO, asoma la cabeza desde la capucha de Ceci, más chico que la cabeza de ella.

### Micro-misión R06-N05-P5 · La melodía completa

```meta
lugar: La Arena del Conservatorio
personajes: Ceci, Clave, Bemol, Gheco
criatura: dragon
carta: Jefe | Dequeue() saca y avanza · Peek() solo mira el primero · cada hueco, la nota siguiente
recompensa: xp 30, oro 30, monedas 3
item: Escama de Do Sostenido
```

#### Escena
La quinta escama es la de bronce, la del pecho. Para soltarla, Ceci tiene que tocar la partitura sin terminar del Vidriero, rellenando cada hueco con las notas de la cajita de música, en orden. Pero su programa rellena todos los huecos con la misma nota, y el dragón se ríe con una carcajada de humo.

#### Gheco sugiere
`Peek()` **mira** la primera nota de la fila, pero no la saca: por eso siempre da la misma. `Dequeue()` la mira **y la saca**, y la próxima vez da la siguiente:

```csharp
partitura[i] = cajita.Dequeue();
```

Al final, si la fila quedó vacía, se usaron todas las notas de la cajita: la partitura está completa.

#### Desafío
Cambiá `Peek()` por `Dequeue()` para rellenar cada hueco con la nota siguiente.

#### Código inicial
```csharp
Queue<string> cajita = new(["Mi", "Sol", "Do#", "La"]);
string[] partitura = ["Do#", "_", "Re", "_", "Fa#", "_", "Si", "_"];

for (int i = 0; i < partitura.Length; i++)
{
    if (partitura[i] == "_")
    {
        partitura[i] = cajita.Peek();
    }
}

Console.WriteLine(string.Join(" ", partitura));
Console.WriteLine(cajita.Count == 0 ? "La partitura está completa." : $"Sobran {cajita.Count} notas.");
```

#### Salida esperada
```
Do# Mi Re Sol Fa# Do# Si La
La partitura está completa.
```

#### Solución
```csharp
Queue<string> cajita = new(["Mi", "Sol", "Do#", "La"]);
string[] partitura = ["Do#", "_", "Re", "_", "Fa#", "_", "Si", "_"];

for (int i = 0; i < partitura.Length; i++)
{
    if (partitura[i] == "_")
    {
        partitura[i] = cajita.Dequeue();
    }
}

Console.WriteLine(string.Join(" ", partitura));
Console.WriteLine(cajita.Count == 0 ? "La partitura está completa." : $"Sobran {cajita.Count} notas.");
```

#### Al superarla
Ceci toca. Las ocho notas suenan en la Arena, la cajita de música y el violín juntos, y por primera vez la melodía del Vidriero se oye **entera**. El dragón se queda quieto, escuchando. Las partituras quemadas de su cuerpo se alisan, una por una, y se vuelven hojas en blanco que salen volando por encima de las gradas como pájaros. Donde estaba el dragón, sobre la arena, queda una sola cosa: la **Escama de Do Sostenido**, de bronce, tibia todavía.

{mentor} la levanta y se la pone a Ceci en la mano. —No era un monstruo —dice—. Eran todas las partituras que alguien escribió sin ensayar. Les faltaba eso: que alguien las tocara bien una vez.

Bemol aplaude solo en la grada. Después se suman los faroles, que parpadean. Gheco sale de la capucha y se para en la cabeza de Ceci, con los bracitos en alto.

#### Imagen
- Una arena redonda de piedra con gradas de madera y faroles, de noche, con cientos de hojas de papel en blanco volando hacia el cielo como pájaros, y en el centro, sobre la arena, una escama de bronce con forma de sostenido que brilla dorada, sin letras ni notas escritas.
- Ceci toca el violín con los ojos cerrados, con una cajita de música abierta a sus pies; Clave la mira con una sonrisa chiquita; Bemol, gordito y con panza, aplaude en la grada; Gheco, un gecko de luz cian con antiparras, MINÚSCULO, parado en la cabeza de Ceci, más chico que su mano, levanta los bracitos.

### Encargo R06-N05-E1 · El torneo del Gremio

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

El Gremio quiere repetir la Arena como torneo, con todas las regiones. Leé resultados, uno por línea, con el formato `nombre,oro`, hasta una línea vacía. Un mismo jugador puede pelear varias veces: su oro se **suma**. Si el oro no es un número entero, mostrá `Resultado inválido: …` y seguí.

Al final:

1. Mostrá `=== Torneo del Gremio ===` y el podio: los tres que más oro juntaron, de mayor a menor, con el formato `1. Nombre: oro`.
2. Guardá la tabla completa (todos los jugadores, de mayor a menor) en `torneo.json` como una lista de `record Puntaje(string Nombre, int Oro)`.
3. Leé el archivo de vuelta y mostrá `Guardados: N jugadores`.

Con esta entrada:

```
Ceci,90
Nilo,40
Nima,70
Ceci,45
Tizón,abc
Zed,60
Nilo,35

```

se muestra:

```
Resultado inválido: Tizón,abc
=== Torneo del Gremio ===
1. Ceci: 135
2. Nilo: 75
3. Nima: 70
Guardados: 4 jugadores
```

#### Criterio de aprobación

- Suma el oro de cada jugador con un `Dictionary<string, int>` y valida con `int.TryParse`.
- Ordena con LINQ y guarda y lee el JSON con `JsonSerializer`.

#### Entrada de ejemplo

```
Ceci,90
Nilo,40
Nima,70
Ceci,45
Tizón,abc
Zed,60
Nilo,35

```

#### Salida esperada

```
Resultado inválido: Tizón,abc
=== Torneo del Gremio ===
1. Ceci: 135
2. Nilo: 75
3. Nima: 70
Guardados: 4 jugadores
```

#### Solución de referencia

```csharp
using System.Text.Json;

Dictionary<string, int> oro = new();
string? linea = Console.ReadLine();
while (!string.IsNullOrEmpty(linea))
{
    string[] partes = linea.Split(',');
    if (partes.Length != 2 || !int.TryParse(partes[1], out int cantidad))
    {
        Console.WriteLine($"Resultado inválido: {linea}");
    }
    else
    {
        oro[partes[0]] = oro.GetValueOrDefault(partes[0]) + cantidad;
    }
    linea = Console.ReadLine();
}

List<Puntaje> tabla = oro.Select(par => new Puntaje(par.Key, par.Value))
    .OrderByDescending(p => p.Oro)
    .ToList();

Console.WriteLine("=== Torneo del Gremio ===");
int puesto = 1;
foreach (Puntaje p in tabla.Take(3))
{
    Console.WriteLine($"{puesto}. {p.Nombre}: {p.Oro}");
    puesto++;
}

File.WriteAllText("torneo.json", JsonSerializer.Serialize(tabla));
List<Puntaje> leida = JsonSerializer.Deserialize<List<Puntaje>>(File.ReadAllText("torneo.json")) ?? [];
Console.WriteLine($"Guardados: {leida.Count} jugadores");

record Puntaje(string Nombre, int Oro);
```
