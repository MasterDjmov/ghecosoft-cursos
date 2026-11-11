# RAMA R02 · El Taller de Instrumentos: los objetos

```meta
tipo: tronco
posicion: 2
```

## R02-N01 · Clases y objetos: el plano del violín

```meta
tipo: tema
padre: R01-N15
precio: 10
criatura: goblin
temas: poo.clases
usa: prog.variables, prog.funciones
```

### Crónica

Al otro lado del patio, detrás de una puerta que huele a madera y a cola, está el **Taller de Instrumentos**. Lo atiende **Don Cedro**, el luthier: bajito, de barba blanca, con un lápiz detrás de la oreja. En la pared cuelga un solo plano de violín, y sobre la mesa hay veinte violines distintos: uno rojo, otro desafinado, otro partido al medio.

—El plano es la **clase** —le explica {mentor} a Ceci—. Cada violín es un **objeto**. Un solo plano, muchos instrumentos, y cada uno con su propio estado.

—Primero el plano, después la madera —agrega Don Cedro, sin levantar la vista del barniz.

### Objetivos

- Escribir una **clase** con datos (campos) y acciones (métodos).
- Crear **objetos** con `new` y usarlos con el punto.
- Entender que cada objeto tiene sus propios datos.

### Antes de empezar

- Los métodos (R01-N13) y todo lo de la Sala de Ensayo.

### Explicación

#### El plano y los instrumentos

Una **clase** es un molde: dice **qué datos** tiene algo y **qué sabe hacer**. Un **objeto** es una cosa concreta hecha con ese molde.

```csharp
class Violin
{
    public string color = "natural";   // un campo: un dato del objeto
    public int cuerdas = 4;
}
```

En nuestros programas, las clases se escriben **abajo de todo**, después de las órdenes y de los métodos sueltos.

#### `new`: hacer un objeto

```csharp
Violin rojo = new Violin();   // new fabrica un violín nuevo con el plano
rojo.color = "rojo";          // el punto entra a sus datos
Console.WriteLine(rojo.color);    // rojo
```

`Violin` es el **tipo** de la variable, igual que `int` o `string`: ahora los tipos los podés inventar vos.

#### Cada objeto tiene lo suyo

```csharp
Violin a = new Violin();
Violin b = new Violin();
a.color = "rojo";
Console.WriteLine(b.color);   // natural: b no cambió
```

Dos objetos del mismo plano son **dos instrumentos distintos**: lo que le hacés a uno no le pasa al otro.

#### `public`

`public` quiere decir que el dato se puede usar desde afuera de la clase. Si no lo ponés, queda **privado** y el compilador no te deja tocarlo desde afuera. En el R02-N03 vas a ver por qué, muchas veces, eso es lo mejor.

### Código de ejemplo

```csharp
Violin rojo = new Violin();
rojo.color = "rojo";

Violin viejo = new Violin();
viejo.cuerdas = 3;

Console.WriteLine($"Rojo: {rojo.color}, {rojo.cuerdas} cuerdas");
Console.WriteLine($"Viejo: {viejo.color}, {viejo.cuerdas} cuerdas");

class Violin
{
    public string color = "natural";
    public int cuerdas = 4;
}
```

### Salida esperada

```
Rojo: rojo, 4 cuerdas
Viejo: natural, 3 cuerdas
```

### ¿Para qué sirve?

En un juego, cada enemigo, cada ítem y cada jugador es un objeto. En una tienda, cada producto y cada pedido. Una clase bien hecha te deja crear mil objetos sin repetir código, y cada uno guarda lo suyo.

### Errores habituales

- **Olvidar el `new`:** `Violin v;` solo declara el nombre; sin `new` no hay ningún violín.
- **Escribir la clase arriba:** en un programa como los nuestros, las órdenes van primero y las clases al final.
- **Olvidar el `public`:** el **goblin** de `CS0122` aparece cuando tocás un dato privado desde afuera.

### Micro-misión R02-N01-P1 · El primer violín del plano

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: Objeto | Clase nombre = new Clase(); · nombre.dato = valor; · la clase va abajo de todo
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Don Cedro le pasa a Ceci el plano del violín y un trozo de madera. —Fabricá uno —dice—. Y pintalo de azul.

#### Gheco sugiere
Para fabricar un objeto se usa `new`, y para tocar sus datos, el punto:

```csharp
Tambor t = new Tambor();
t.tamanio = "grande";
Console.WriteLine(t.tamanio);   // grande

class Tambor
{
    public string tamanio = "chico";
}
```

#### Desafío
Creá un `Violin` llamado `nuevo`, cambiale el color a `azul` y mostralo.

#### Código inicial
```csharp
// Fabricá el violín acá


class Violin
{
    public string color = "natural";
}
```

#### Salida esperada
```
azul
```

#### Solución
```csharp
Violin nuevo = new Violin();
nuevo.color = "azul";
Console.WriteLine(nuevo.color);

class Violin
{
    public string color = "natural";
}
```

#### Al superarla
Don Cedro levanta el violín azul contra la luz, le da vuelta y gruñe algo que suena a aprobación. —Lindo color. Ahora, que suene.

#### Imagen
- Un taller de luthier de madera con instrumentos colgados, virutas en el piso y un plano de violín en la pared, sin letras.
- Ceci sostiene un violín azul recién pintado y Don Cedro lo mira por encima de sus anteojos redondos.

### Micro-misión R02-N01-P2 · Dos violines, dos colores

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Bemol, Don Cedro
carta: Cada objeto es otro | a.color = "rojo" no cambia b.color · un plano, muchos objetos
recompensa: xp 15, oro 15
```

#### Escena
Bemol no se convence: —Si los dos salen del mismo plano, ¿no son el mismo violín?

#### Gheco sugiere
Cada `new` fabrica un objeto **distinto**. Cambiar uno no cambia al otro:

```csharp
Tambor a = new Tambor();
Tambor b = new Tambor();
a.tamanio = "grande";
Console.WriteLine(b.tamanio);   // chico
```

#### Desafío
Fabricá un segundo violín, `segundo`, y pintalo de `verde`. El primero tiene que seguir `rojo`.

#### Código inicial
```csharp
Violin primero = new Violin();
primero.color = "rojo";

// el segundo violín


Console.WriteLine(primero.color);
Console.WriteLine(segundo.color);

class Violin
{
    public string color = "natural";
}
```

#### Salida esperada
```
rojo
verde
```

#### Solución
```csharp
Violin primero = new Violin();
primero.color = "rojo";

Violin segundo = new Violin();
segundo.color = "verde";

Console.WriteLine(primero.color);
Console.WriteLine(segundo.color);

class Violin
{
    public string color = "natural";
}
```

#### Al superarla
—Ah —dice Bemol, y se acomoda los anteojos—. Un plano, muchos violines. Cada uno con su color.

#### Imagen
- Dos violines iguales sobre una mesa de trabajo de madera, uno rojo y otro verde, con un plano de violín clavado en la pared, sin letras.
- Bemol los mira de cerca con la nariz casi pegada; Ceci se ríe detrás.

### Micro-misión R02-N01-P3 · Un dato más en el plano

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: Campo | public tipo nombre = valor; · dentro de la clase · cada objeto trae el suyo
recompensa: xp 15, oro 15
```

#### Escena
Don Cedro anota algo en el plano: cada violín, además de color, tiene un **dueño**. Si nadie lo compró todavía, el dueño es «el taller».

#### Gheco sugiere
Un **campo** se declara dentro de la clase, con `public`, su tipo y un valor inicial:

```csharp
class Tambor
{
    public string tamanio = "chico";
    public int golpes = 0;
}
```

#### Desafío
Agregale al plano un campo `public string duenio = "el taller";`. El programa ya lo muestra.

#### Código inicial
```csharp
Violin v = new Violin();
Console.WriteLine($"{v.color}, de {v.duenio}");

class Violin
{
    public string color = "natural";
}
```

#### Salida esperada
```
natural, de el taller
```

#### Solución
```csharp
Violin v = new Violin();
Console.WriteLine($"{v.color}, de {v.duenio}");

class Violin
{
    public string color = "natural";
    public string duenio = "el taller";
}
```

#### Al superarla
—Todos los violines nuevos nacen del taller —dice Don Cedro—. Después, cada uno elige su casa.

#### Imagen
- Un plano grande de violín clavado en una pared de madera, con un lápiz de carpintero apoyado al lado, sin letras.
- Don Cedro dibuja una línea más en el plano; Ceci mira por encima de su hombro.

### Micro-misión R02-N01-P4 · El violín que sabe sonar

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro, Clave
carta: Método de la clase | public void Tocar() { … } · v.Tocar() · usa los datos de su objeto
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
—Un plano de violín que no dice cómo suena está incompleto —dice Clave—. Los objetos no solo **tienen** datos: también **saben hacer** cosas.

#### Gheco sugiere
Un método escrito **dentro** de la clase es algo que cada objeto sabe hacer. Usa los datos del objeto que lo ejecuta, sin `static`:

```csharp
Tambor t = new Tambor();
t.Golpear();     // Pum (chico)

class Tambor
{
    public string tamanio = "chico";

    public void Golpear()
    {
        Console.WriteLine($"Pum ({tamanio})");
    }
}
```

#### Desafío
Escribí en la clase el método `public void Tocar()`, que muestre `El violín <color> suena`, y llamalo para los dos violines.

#### Código inicial
```csharp
Violin rojo = new Violin();
rojo.color = "rojo";
Violin azul = new Violin();
azul.color = "azul";

rojo.Tocar();
azul.Tocar();

class Violin
{
    public string color = "natural";

    // el método Tocar
}
```

#### Salida esperada
```
El violín rojo suena
El violín azul suena
```

#### Solución
```csharp
Violin rojo = new Violin();
rojo.color = "rojo";
Violin azul = new Violin();
azul.color = "azul";

rojo.Tocar();
azul.Tocar();

class Violin
{
    public string color = "natural";

    public void Tocar()
    {
        Console.WriteLine($"El violín {color} suena");
    }
}
```

#### Al superarla
Los dos violines suenan, cada uno con su voz. Don Cedro deja el pincel por primera vez en la tarde. —Ahora sí: un plano completo.

#### Imagen
- Dos violines, uno rojo y uno azul, sobre un banco de trabajo, con notas musicales doradas flotando sobre cada uno, sin letras.
- Ceci toca el rojo; Clave escucha con los brazos cruzados y Don Cedro sonríe en el fondo.

### Micro-misión R02-N01-P5 · El goblin del cajón cerrado

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Gheco
criatura: goblin
carta: Goblin | CS0122: no es accesible · el campo sin public es privado · agregale public
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un goblin se metió en el plano y le borró una palabra a un campo. Ahora el programa no compila y el goblin se ríe desde un cajón.

#### Gheco sugiere
Si un campo no dice `public`, es **privado**: solo se puede usar adentro de la clase. Desde afuera aparece:

```
error CS0122: 'Violin.precio' no es accesible debido a su nivel de protección
```

Para usarlo desde afuera, agregale `public` adelante.

#### Desafío
Ensayá, leé el error y arreglá el campo para que el programa muestre el precio.

#### Código inicial
```csharp
Violin v = new Violin();
Console.WriteLine($"Precio: {v.precio}");

class Violin
{
    int precio = 120;
}
```

#### Salida esperada
```
Precio: 120
```

#### Solución
```csharp
Violin v = new Violin();
Console.WriteLine($"Precio: {v.precio}");

class Violin
{
    public int precio = 120;
}
```

#### Al superarla
El goblin sale del cajón, ve que el precio está a la vista de todos y se va refunfuñando por la ventana.

#### Imagen
- Un cajón de madera de un taller de luthier abierto, con un goblin chico de orejas puntiagudas saliendo de un salto hacia una ventana.
- Gheco, sobre el borde de la mesa, lo mira irse con cara de triunfo.

### Encargo R02-N01-E1 · Los faroles de Lucio

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Lucio, el farolero de la Feria, quiere llevar la cuenta de sus faroles. Escribí una clase `Farol` con un campo `calle` (texto), un campo `prendido` (`bool`, empieza en `false`) y un método `Mostrar()` que muestre `Farol de <calle>: prendido` o `Farol de <calle>: apagado`.

Creá dos faroles, uno en `la avenida` (prendido) y otro en `la calesita` (apagado), y mostralos:

```
Farol de la avenida: prendido
Farol de la calesita: apagado
```

#### Criterio de aprobación

- Hay una clase `Farol` con los dos campos y el método `Mostrar`.
- Los faroles se crean con `new` y se muestran llamando a `Mostrar()`.

#### Salida esperada

```
Farol de la avenida: prendido
Farol de la calesita: apagado
```

#### Solución de referencia

```csharp
Farol a = new Farol();
a.calle = "la avenida";
a.prendido = true;

Farol b = new Farol();
b.calle = "la calesita";

a.Mostrar();
b.Mostrar();

class Farol
{
    public string calle = "";
    public bool prendido = false;

    public void Mostrar()
    {
        string estado = prendido ? "prendido" : "apagado";
        Console.WriteLine($"Farol de {calle}: {estado}");
    }
}
```

## R02-N02 · Objetos que trabajan juntos (y la sobrecarga)

```meta
tipo: tema
padre: R02-N01
precio: 10
criatura: esqueleto
temas: poo.clases, prog.funciones
usa: col.arrays, prog.bucles
```

### Crónica

Don Cedro tiene un problema: los violines llegan al taller desafinados, y él tiene que afinarlos de a uno. —Si un objeto sabe hacer cosas —pregunta Ceci—, ¿puede hacerle cosas a **otro** objeto?

—Puede —dice {mentor}—. Un afinador afina violines. Un violín le pasa la nota a otro. Los objetos trabajan juntos, se guardan en arreglos y se pasan a los métodos como cualquier dato.

### Objetivos

- Pasar un objeto a un método y que el método lo cambie.
- Guardar objetos en un arreglo y recorrerlos.
- Usar `this` y métodos que devuelven un resultado.
- **Sobrecargar** un método: el mismo nombre con distintos parámetros.

### Antes de empezar

- Clases y objetos (R02-N01), arreglos (R01-N11).

### Explicación

#### Un objeto que recibe a otro

Un método puede recibir un objeto como parámetro, y cambiarlo:

```csharp
class Afinador
{
    public void Afinar(Violin v)
    {
        v.afinado = true;
    }
}
```

```csharp
Afinador a = new Afinador();
a.Afinar(rojo);      // ahora rojo.afinado es true
```

#### Un arreglo de objetos

```csharp
Violin[] estante = { new Violin(), new Violin(), new Violin() };
foreach (Violin v in estante)
{
    a.Afinar(v);
}
```

#### `this`: el objeto que está trabajando

Adentro de un método, `this` es **el objeto que lo ejecuta**. Casi siempre se puede omitir, pero ayuda cuando un parámetro se llama igual que un campo:

```csharp
public void CambiarColor(string color)
{
    this.color = color;     // el campo = el parámetro
}
```

#### Sobrecarga

Dentro de una clase, **varios métodos pueden llamarse igual** si reciben parámetros distintos. C# elige cuál usar mirando lo que le pasás:

```csharp
class Afinador
{
    public void Afinar(Violin v) { v.afinado = true; }
    public void Afinar(Violin[] varios)
    {
        foreach (Violin v in varios) Afinar(v);
    }
}
```

Eso es lo que en la Sala de Ensayo no se podía: ahora, adentro de una clase, sí.

### Código de ejemplo

```csharp
Violin[] estante = { new Violin(), new Violin() };
estante[0].color = "rojo";
estante[1].color = "azul";

Afinador afinador = new Afinador();
afinador.Afinar(estante[0]);

foreach (Violin v in estante)
{
    Console.WriteLine(v.Estado());
}

afinador.Afinar(estante);
Console.WriteLine(estante[1].Estado());

class Violin
{
    public string color = "natural";
    public bool afinado = false;

    public string Estado()
    {
        return afinado ? $"{color}: afinado" : $"{color}: desafinado";
    }
}

class Afinador
{
    public void Afinar(Violin v)
    {
        v.afinado = true;
    }

    public void Afinar(Violin[] varios)
    {
        foreach (Violin v in varios) Afinar(v);
    }
}
```

### Salida esperada

```
rojo: afinado
azul: desafinado
azul: afinado
```

### ¿Para qué sirve?

Un programa de verdad es una orquesta de objetos: el carrito usa los productos, el héroe ataca al ogro, el afinador afina violines. Y la sobrecarga es lo que te deja escribir `Console.WriteLine` con un número, un texto o nada: son varios métodos con el mismo nombre.

### Errores habituales

- **Usar un lugar del arreglo vacío:** `new Violin[3]` hace el estante, pero **sin violines adentro**. Cada lugar hay que llenarlo con `new Violin()`.
- **Dos métodos iguales de verdad:** la sobrecarga necesita parámetros **distintos**; con los mismos, no compila (`CS0111`).
- **Llamar a un método que no existe:** el **esqueleto** de `CS1061` dice que el objeto no tiene ese método. Fijate el nombre y las mayúsculas.

### Micro-misión R02-N02-P1 · El afinador

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: Objeto como parámetro | public void Afinar(Violin v) · v.afinado = true · cambia al objeto que recibe
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Don Cedro le presta a Ceci su afinador de bronce. —Le das un violín, y te lo devuelve afinado. Siempre.

#### Gheco sugiere
Un método puede recibir un objeto y cambiarle los datos:

```csharp
class Pintor
{
    public void Pintar(Tambor t)
    {
        t.color = "rojo";
    }
}
```

#### Desafío
Completá el método `Afinar` para que ponga en `true` el campo `afinado` del violín que recibe.

#### Código inicial
```csharp
Violin v = new Violin();
Afinador a = new Afinador();
a.Afinar(v);
Console.WriteLine($"¿Afinado? {v.afinado}");

class Violin
{
    public bool afinado = false;
}

class Afinador
{
    public void Afinar(Violin v)
    {
        // afinalo
    }
}
```

#### Salida esperada
```
¿Afinado? True
```

#### Solución
```csharp
Violin v = new Violin();
Afinador a = new Afinador();
a.Afinar(v);
Console.WriteLine($"¿Afinado? {v.afinado}");

class Violin
{
    public bool afinado = false;
}

class Afinador
{
    public void Afinar(Violin v)
    {
        v.afinado = true;
    }
}
```

#### Al superarla
El afinador zumba, la cuerda se tensa y el La suena limpio. —¿Ves? —dice Don Cedro—. Le diste el violín, y el violín volvió distinto.

#### Imagen
- Un afinador de bronce antiguo con forma de horquilla apoyado sobre las cuerdas de un violín, con una nota dorada saliendo, sin letras.
- Ceci gira una clavija con cuidado; Don Cedro le sostiene el violín.

### Micro-misión R02-N02-P2 · El estante de violines

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Bemol
carta: Arreglo de objetos | Violin[] e = { new Violin(), … } · foreach (Violin v in e) · cada lugar, un objeto
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
En el estante hay tres violines esperando. Bemol propone afinarlos de a uno, a mano. Ceci prefiere un bucle.

#### Gheco sugiere
Los objetos se guardan en arreglos como cualquier dato, y se recorren con `foreach`:

```csharp
Tambor[] banda = { new Tambor(), new Tambor() };
foreach (Tambor t in banda)
{
    t.Golpear();
}
```

#### Desafío
Recorré el estante con un `foreach` y afiná cada violín con el afinador. El programa después cuenta los afinados.

#### Código inicial
```csharp
Violin[] estante = { new Violin(), new Violin(), new Violin() };
Afinador a = new Afinador();

// afiná todos


int listos = 0;
foreach (Violin v in estante)
{
    if (v.afinado) listos++;
}
Console.WriteLine($"Afinados: {listos} de {estante.Length}");

class Violin
{
    public bool afinado = false;
}

class Afinador
{
    public void Afinar(Violin v)
    {
        v.afinado = true;
    }
}
```

#### Salida esperada
```
Afinados: 3 de 3
```

#### Solución
```csharp
Violin[] estante = { new Violin(), new Violin(), new Violin() };
Afinador a = new Afinador();

foreach (Violin v in estante)
{
    a.Afinar(v);
}

int listos = 0;
foreach (Violin v in estante)
{
    if (v.afinado) listos++;
}
Console.WriteLine($"Afinados: {listos} de {estante.Length}");

class Violin
{
    public bool afinado = false;
}

class Afinador
{
    public void Afinar(Violin v)
    {
        v.afinado = true;
    }
}
```

#### Al superarla
Tres zumbidos seguidos y el estante entero queda afinado. Bemol aplaude con los palillos del tambor.

#### Imagen
- Un estante de madera con tres violines en fila y un afinador de bronce, cada violín con una notita dorada encima, sin letras.
- Bemol aplaude con dos palillos de tambor; Ceci sostiene el afinador.

### Micro-misión R02-N02-P3 · `this`, el que está trabajando

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Clave
carta: this | this.color = color · el campo del objeto = el parámetro · cuando se llaman igual
recompensa: xp 15, oro 15
```

#### Escena
Ceci escribió un método para cambiar el color, pero el violín sigue `natural`. Clave señala la línea: —Le estás asignando el parámetro a sí mismo.

#### Gheco sugiere
Si el parámetro se llama igual que el campo, adentro del método gana el **parámetro**. Para hablar del campo del objeto se usa `this`:

```csharp
public void CambiarTamanio(string tamanio)
{
    this.tamanio = tamanio;
}
```

#### Desafío
Arreglá `CambiarColor` usando `this` para que el violín quede `dorado`.

#### Código inicial
```csharp
Violin v = new Violin();
v.CambiarColor("dorado");
Console.WriteLine(v.color);

class Violin
{
    public string color = "natural";

    public void CambiarColor(string color)
    {
        color = color;
    }
}
```

#### Salida esperada
```
dorado
```

#### Solución
```csharp
Violin v = new Violin();
v.CambiarColor("dorado");
Console.WriteLine(v.color);

class Violin
{
    public string color = "natural";

    public void CambiarColor(string color)
    {
        this.color = color;
    }
}
```

#### Al superarla
—`this` quiere decir «yo» —dice Clave—. El violín que está trabajando, no el que le pasaron.

#### Imagen
- Un violín dorado brillante sobre un atril de madera, con reflejos de velas, sin letras.
- Clave señala el violín con la batuta; Ceci lo mira sorprendida.

### Micro-misión R02-N02-P4 · Afinar uno o afinar todos

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro, Bemol
carta: Sobrecarga | dos métodos con el mismo nombre · distintos parámetros · C# elige por lo que le pasás
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
—Yo quiero decirle «afiná este» o «afiná todos» —dice Don Cedro—, con la misma palabra. Así hablo yo.

#### Gheco sugiere
Adentro de una clase, dos métodos pueden tener **el mismo nombre** si reciben parámetros distintos:

```csharp
class Pintor
{
    public void Pintar(Tambor t) { t.color = "rojo"; }
    public void Pintar(Tambor[] varios)
    {
        foreach (Tambor t in varios) Pintar(t);
    }
}
```

#### Desafío
Agregá al afinador un segundo `Afinar` que reciba un `Violin[]` y afine cada uno usando el primero. El programa ya lo llama con el estante.

#### Código inicial
```csharp
Violin solo = new Violin();
Violin[] estante = { new Violin(), new Violin() };
Afinador a = new Afinador();

a.Afinar(solo);
a.Afinar(estante);
Console.WriteLine($"{solo.afinado} {estante[0].afinado} {estante[1].afinado}");

class Violin
{
    public bool afinado = false;
}

class Afinador
{
    public void Afinar(Violin v)
    {
        v.afinado = true;
    }

    // el Afinar que recibe muchos
}
```

#### Salida esperada
```
True True True
```

#### Solución
```csharp
Violin solo = new Violin();
Violin[] estante = { new Violin(), new Violin() };
Afinador a = new Afinador();

a.Afinar(solo);
a.Afinar(estante);
Console.WriteLine($"{solo.afinado} {estante[0].afinado} {estante[1].afinado}");

class Violin
{
    public bool afinado = false;
}

class Afinador
{
    public void Afinar(Violin v)
    {
        v.afinado = true;
    }

    public void Afinar(Violin[] varios)
    {
        foreach (Violin v in varios) Afinar(v);
    }
}
```

#### Al superarla
—Así me gusta —dice Don Cedro—. Una palabra, y el afinador entiende si le hablás de uno o de muchos.

#### Imagen
- Un afinador de bronce flotando con ondas suaves que alcanzan a un violín solo y a un estante con dos violines, sin letras.
- Don Cedro, con su delantal de cuero, abre los brazos satisfecho; Bemol y Ceci se miran.

### Micro-misión R02-N02-P5 · El esqueleto del método perdido

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Gheco
criatura: esqueleto
carta: Esqueleto | CS1061: no contiene una definición · el método no existe con ese nombre · revisá mayúsculas
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un esqueleto llama a un método que nadie escribió. El compilador lo detiene en la puerta del taller.

#### Gheco sugiere
`CS1061` quiere decir: «este objeto no tiene un método (o un campo) con ese nombre».

```
error CS1061: "Violin" no contiene una definición para "tocar"
```

Casi siempre es una mayúscula: el método se llama `Tocar`, no `tocar`.

#### Desafío
Ensayá, leé el error y arreglá la llamada.

#### Código inicial
```csharp
Violin v = new Violin();
v.tocar();

class Violin
{
    public void Tocar()
    {
        Console.WriteLine("Suena el violín");
    }
}
```

#### Salida esperada
```
Suena el violín
```

#### Solución
```csharp
Violin v = new Violin();
v.Tocar();

class Violin
{
    public void Tocar()
    {
        Console.WriteLine("Suena el violín");
    }
}
```

#### Al superarla
El esqueleto oye el violín, se da cuenta de que no lo llamaban a él y se desarma de vergüenza en un montoncito de huesos.

#### Imagen
- Un esqueleto de caricatura desarmándose en un montoncito de huesos junto a la puerta de un taller de madera, sin sangre.
- Gheco, sobre un violín, lo mira con las antiparras levantadas.

### Encargo R02-N02-E1 · El palomar de Nilo

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Nilo reparte cartas del Puerto. Escribí una clase `Carta` con `destino` (texto) y `entregada` (`bool`), y una clase `Cartero` con dos métodos `Entregar`: uno que recibe **una** `Carta` y la marca entregada, y otro que recibe un `Carta[]` y entrega todas.

Creá tres cartas (`Feria`, `Forjas` y `Conservatorio`), entregá primero la de la Feria sola, mostrá cuántas quedan pendientes, después entregá todas juntas y volvé a mostrarlo:

```
Pendientes: 2
Pendientes: 0
```

#### Criterio de aprobación

- La clase `Cartero` tiene dos métodos `Entregar` (sobrecarga).
- Las pendientes se cuentan recorriendo el arreglo.

#### Salida esperada

```
Pendientes: 2
Pendientes: 0
```

#### Solución de referencia

```csharp
Carta[] bolsa = { new Carta(), new Carta(), new Carta() };
bolsa[0].destino = "Feria";
bolsa[1].destino = "Forjas";
bolsa[2].destino = "Conservatorio";

Cartero nilo = new Cartero();
nilo.Entregar(bolsa[0]);
Console.WriteLine($"Pendientes: {Pendientes(bolsa)}");
nilo.Entregar(bolsa);
Console.WriteLine($"Pendientes: {Pendientes(bolsa)}");

static int Pendientes(Carta[] cartas)
{
    int n = 0;
    foreach (Carta c in cartas)
    {
        if (!c.entregada) n++;
    }
    return n;
}

class Carta
{
    public string destino = "";
    public bool entregada = false;
}

class Cartero
{
    public void Entregar(Carta c)
    {
        c.entregada = true;
    }

    public void Entregar(Carta[] cartas)
    {
        foreach (Carta c in cartas) Entregar(c);
    }
}
```

## R02-N03 · Propiedades: el violín que se cuida solo

```meta
tipo: tema
padre: R02-N02
precio: 10
criatura: goblin
temas: poo.encapsulamiento
usa: poo.clases, prog.condicionales
```

### Crónica

Un goblin se coló en el taller de noche y le cambió las cuerdas a un violín: le puso **cuarenta**. Don Cedro amaneció furioso. —¡Un violín tiene cuatro cuerdas! ¿Cómo dejaron que alguien escribiera cuarenta?

—Porque el dato estaba a la vista —dice {mentor}—. Cualquiera podía escribir lo que quisiera. Hay que **cuidarlo**: esconderlo, y dejar pasar los cambios por una puerta que los revise.

### Objetivos

- Esconder un dato con `private`.
- Escribir una **propiedad** con `get` y `set` que revise lo que entra.
- Usar las propiedades automáticas, las de solo lectura y las calculadas.

### Antes de empezar

- Objetos que trabajan juntos (R02-N02).

### Explicación

#### El problema de lo público

Con `public int cuerdas`, cualquiera puede escribir `v.cuerdas = 40`. **Encapsular** es esconder el dato y dejar que los cambios pasen por un lugar que los controle.

| Palabra | Se puede usar desde… |
|---|---|
| `public` | cualquier lado |
| `private` | solo dentro de la clase (es lo que se usa si no ponés nada) |

#### Propiedades

Una **propiedad** se usa como un campo, pero por dentro tiene dos partes: `get` (cuando la leen) y `set` (cuando le asignan). En el `set`, `value` es lo que están asignando:

```csharp
class Violin
{
    private int _cuerdas = 4;     // el dato escondido

    public int Cuerdas
    {
        get { return _cuerdas; }
        set
        {
            if (value >= 1 && value <= 5) _cuerdas = value;
        }
    }
}
```

```csharp
v.Cuerdas = 40;                  // pasa por el set: se rechaza
Console.WriteLine(v.Cuerdas);    // 4
```

Costumbre de C#: lo público con **Mayúscula** (`Cuerdas`) y lo privado con guion bajo (`_cuerdas`).

#### Las formas cortas

| Escritura | Qué es |
|---|---|
| `public string Duenio { get; set; } = "";` | **automática**: C# crea el dato escondido |
| `public string Modelo { get; } = "clásico";` | **solo lectura**: no se puede cambiar desde afuera |
| `public int Arreglos { get; private set; }` | se lee afuera, pero se cambia solo adentro |
| `public bool EsViejo => Anios > 50;` | **calculada**: no guarda nada, se calcula al leerla |

### Código de ejemplo

```csharp
Violin v = new Violin();
v.Cuerdas = 40;
v.Anios = 80;
v.Reparar();
Console.WriteLine($"Cuerdas: {v.Cuerdas}");
Console.WriteLine($"¿Viejo? {v.EsViejo}");
Console.WriteLine($"Arreglos: {v.Arreglos}");

class Violin
{
    private int _cuerdas = 4;

    public int Cuerdas
    {
        get { return _cuerdas; }
        set
        {
            if (value >= 1 && value <= 5) _cuerdas = value;
        }
    }

    public int Anios { get; set; }
    public int Arreglos { get; private set; }
    public bool EsViejo => Anios > 50;

    public void Reparar()
    {
        Arreglos++;
    }
}
```

### Salida esperada

```
Cuerdas: 4
¿Viejo? True
Arreglos: 1
```

### ¿Para qué sirve?

Un saldo que no puede quedar negativo, una vida que no pasa de 100, una edad que no puede ser -3: las propiedades hacen que un objeto **nunca quede en un estado imposible**, sin importar quién lo use. En C#, todo dato público se escribe como propiedad.

### Errores habituales

- **El `set` que se llama a sí mismo:** si adentro de `Cuerdas` escribís `Cuerdas = value;`, se llama para siempre y el programa explota. Se asigna el dato escondido: `_cuerdas = value;`.
- **Olvidar el valor inicial de un texto:** `public string Duenio { get; set; }` sin `= ""` da un aviso, porque podría quedar sin nada.
- **Asignar algo de solo lectura:** el **goblin** de `CS0200` aparece cuando le asignás a una propiedad que solo tiene `get`.

### Micro-misión R02-N03-P1 · La puerta que revisa

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: Propiedad | get { return _dato; } · set { if (…) _dato = value; } · value es lo que asignan
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Don Cedro quiere que ningún violín acepte menos de 1 cuerda ni más de 5. Ceci tiene que escribir la puerta.

#### Gheco sugiere
En el `set`, revisá `value` antes de guardarlo. Si no pasa la prueba, no se guarda nada:

```csharp
public int Golpes
{
    get { return _golpes; }
    set
    {
        if (value >= 0) _golpes = value;
    }
}
```

`private` quiere decir que ese dato **solo se ve adentro de la clase**: desde afuera nadie lo puede tocar directo, solo a través de la propiedad. Por costumbre, los datos privados empiezan con `_`.

#### Desafío
Completá el `set` de `Cuerdas` para que solo guarde valores de `1` a `5`.

#### Código inicial
```csharp
Violin v = new Violin();
v.Cuerdas = 40;
Console.WriteLine(v.Cuerdas);
v.Cuerdas = 5;
Console.WriteLine(v.Cuerdas);

class Violin
{
    private int _cuerdas = 4;

    public int Cuerdas
    {
        get { return _cuerdas; }
        set
        {
            _cuerdas = value;
        }
    }
}
```

#### Salida esperada
```
4
5
```

#### Solución
```csharp
Violin v = new Violin();
v.Cuerdas = 40;
Console.WriteLine(v.Cuerdas);
v.Cuerdas = 5;
Console.WriteLine(v.Cuerdas);

class Violin
{
    private int _cuerdas = 4;

    public int Cuerdas
    {
        get { return _cuerdas; }
        set
        {
            if (value >= 1 && value <= 5) _cuerdas = value;
        }
    }
}
```

#### Al superarla
El violín rechaza las cuarenta cuerdas como quien escupe un carozo. Don Cedro asiente: —Así. Que se cuide solo.

#### Imagen
- Un violín sobre un banco de taller rodeado de muchas cuerdas sueltas enredadas que salen despedidas hacia afuera, sin letras.
- Don Cedro, con los brazos cruzados, sonríe satisfecho; Ceci sostiene una sola cuerda nueva.

### Micro-misión R02-N03-P2 · El nombre del dueño

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Bemol
carta: Automática | public string Duenio { get; set; } = ""; · C# crea el dato escondido
recompensa: xp 15, oro 15
```

#### Escena
Bemol quiere anotar el dueño de cada violín. —No necesito revisar nada —dice—, solo guardarlo.

#### Gheco sugiere
Si no hace falta revisar nada, alcanza con una **propiedad automática**:

```csharp
class Tambor
{
    public string Marca { get; set; } = "";
}
```

#### Desafío
Agregale a `Violin` una propiedad automática `Duenio`, de texto, que empiece vacía.

#### Código inicial
```csharp
Violin v = new Violin();
v.Duenio = "Ceci";
Console.WriteLine($"Violín de {v.Duenio}");

class Violin
{
    // la propiedad Duenio
}
```

#### Salida esperada
```
Violín de Ceci
```

#### Solución
```csharp
Violin v = new Violin();
v.Duenio = "Ceci";
Console.WriteLine($"Violín de {v.Duenio}");

class Violin
{
    public string Duenio { get; set; } = "";
}
```

#### Al superarla
Bemol escribe «Ceci» en una etiqueta de cartón y la ata al mango del violín. —Ahora no se pierde.

#### Imagen
- Un violín con una etiqueta de cartón lisa atada al mango con un hilo rojo, sobre una mesa de madera, sin letras en la etiqueta.
- Bemol termina el moño con la lengua afuera de concentración; Ceci espera con las manos juntas.

### Micro-misión R02-N03-P3 · Lo que se calcula solo

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: Calculada | public bool EsViejo => Anios > 50; · no guarda nada · se calcula al leerla
recompensa: xp 15, oro 15
```

#### Escena
—Un violín de más de cincuenta años es viejo —dice Don Cedro—, y un violín viejo se trata distinto. No lo anoten: **calcúlenlo**.

#### Gheco sugiere
Una propiedad **calculada** se escribe con `=>` y no guarda nada: cada vez que la leen, hace la cuenta:

```csharp
public int Golpes { get; set; }
public bool Cansado => Golpes > 100;
```

#### Desafío
Agregá la propiedad calculada `EsViejo`, que sea `true` si `Anios` es mayor que `50`.

#### Código inicial
```csharp
Violin a = new Violin();
a.Anios = 80;
Violin b = new Violin();
b.Anios = 3;
Console.WriteLine($"{a.EsViejo} {b.EsViejo}");

class Violin
{
    public int Anios { get; set; }

    // EsViejo
}
```

#### Salida esperada
```
True False
```

#### Solución
```csharp
Violin a = new Violin();
a.Anios = 80;
Violin b = new Violin();
b.Anios = 3;
Console.WriteLine($"{a.EsViejo} {b.EsViejo}");

class Violin
{
    public int Anios { get; set; }

    public bool EsViejo => Anios > 50;
}
```

#### Al superarla
—El de ochenta años lo hizo mi maestro —dice Don Cedro, y lo acaricia—. Ese se trata con guantes.

#### Imagen
- Dos violines sobre terciopelo bordó: uno antiguo de madera oscura y gastada, y otro nuevo de madera clara, sin letras.
- Don Cedro se pone unos guantes blancos de algodón para tocar el antiguo; Ceci mira con respeto.

### Micro-misión R02-N03-P4 · Se lee afuera, se cambia adentro

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro, Clave
carta: private set | public int Arreglos { get; private set; } · afuera solo se lee · adentro se cambia
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Cada violín lleva la cuenta de cuántas veces lo arreglaron. Clave quiere que esa cuenta solo suba cuando de verdad se arregla, nunca porque alguien la escriba.

#### Gheco sugiere
Con `private set`, la propiedad se **lee** desde cualquier lado, pero solo se **cambia** adentro de la clase, por ejemplo desde un método:

```csharp
public int Golpes { get; private set; }

public void Golpear()
{
    Golpes++;
}
```

#### Desafío
Completá el método `Reparar` para que sume uno a `Arreglos`. El programa lo llama dos veces.

#### Código inicial
```csharp
Violin v = new Violin();
v.Reparar();
v.Reparar();
Console.WriteLine($"Arreglos: {v.Arreglos}");

class Violin
{
    public int Arreglos { get; private set; }

    public void Reparar()
    {
        // sumá un arreglo
    }
}
```

#### Salida esperada
```
Arreglos: 2
```

#### Solución
```csharp
Violin v = new Violin();
v.Reparar();
v.Reparar();
Console.WriteLine($"Arreglos: {v.Arreglos}");

class Violin
{
    public int Arreglos { get; private set; }

    public void Reparar()
    {
        Arreglos++;
    }
}
```

#### Al superarla
—Ahora la cuenta no miente —dice Clave—. Solo sube cuando Don Cedro trabaja.

#### Imagen
- Un banco de luthier con herramientas chicas, cola y un violín abierto en reparación bajo una lámpara cálida, sin letras.
- Don Cedro pega una pieza con el pincel; Clave y Ceci miran desde atrás.

### Micro-misión R02-N03-P5 · El goblin de las cuarenta cuerdas

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Gheco
criatura: goblin
carta: Goblin | CS0200: es de solo lectura · solo tiene get · se asigna adentro, no afuera
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
El goblin vuelve a la carga: quiere cambiarle el modelo a un violín que ya salió del taller. Pero el modelo es de **solo lectura**.

#### Gheco sugiere
Una propiedad con solo `get` no se puede asignar desde afuera:

```
error CS0200: No se puede asignar a la propiedad o el indizador 'Violin.Modelo' porque es de solo lectura
```

Si el modelo no se puede cambiar, la línea que lo cambia **sobra**.

#### Desafío
Ensayá, leé el error y sacá la línea del goblin.

#### Código inicial
```csharp
Violin v = new Violin();
v.Modelo = "de juguete";
Console.WriteLine($"Modelo: {v.Modelo}");

class Violin
{
    public string Modelo { get; } = "clásico";
}
```

#### Salida esperada
```
Modelo: clásico
```

#### Solución
```csharp
Violin v = new Violin();
Console.WriteLine($"Modelo: {v.Modelo}");

class Violin
{
    public string Modelo { get; } = "clásico";
}
```

#### Al superarla
El goblin tira y tira de la etiqueta del modelo, pero no se mueve. Al final se cansa y se va a probar suerte a la Feria.

#### Imagen
- Un goblin chico de orejas puntiagudas tirando con todas sus fuerzas de una plaquita de bronce clavada en un estuche de violín, sin letras.
- Gheco, sentado en el estuche, bosteza.

### Encargo R02-N03-E1 · La alcancía de Bruno

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Bruno, el del puesto de tiro, junta fichas en una alcancía. Escribí una clase `Alcancia` con una propiedad `Fichas` que se lea desde afuera pero **no** se pueda asignar (`private set`), y dos métodos:

- `Meter(int cantidad)`: suma solo si la cantidad es mayor que `0`.
- `Sacar(int cantidad)`: resta solo si hay suficientes, y devuelve `true` si pudo.

Probala así: meté `10`, intentá meter `-5`, sacá `4`, intentá sacar `20`, y mostrá:

```
¿Sacó 4? True
¿Sacó 20? False
Quedan: 6
```

#### Criterio de aprobación

- `Fichas` tiene `private set`: desde afuera no se puede escribir.
- Los métodos revisan la cantidad antes de cambiar `Fichas`.

#### Salida esperada

```
¿Sacó 4? True
¿Sacó 20? False
Quedan: 6
```

#### Solución de referencia

```csharp
Alcancia a = new Alcancia();
a.Meter(10);
a.Meter(-5);
Console.WriteLine($"¿Sacó 4? {a.Sacar(4)}");
Console.WriteLine($"¿Sacó 20? {a.Sacar(20)}");
Console.WriteLine($"Quedan: {a.Fichas}");

class Alcancia
{
    public int Fichas { get; private set; }

    public void Meter(int cantidad)
    {
        if (cantidad > 0) Fichas += cantidad;
    }

    public bool Sacar(int cantidad)
    {
        if (cantidad > Fichas) return false;
        Fichas -= cantidad;
        return true;
    }
}
```

## R02-N04 · Constructores: el violín que nace listo

```meta
tipo: tema
padre: R02-N03
precio: 10
criatura: goblin
temas: poo.constructores, poo.static, poo.operadores
usa: poo.encapsulamiento
```

### Crónica

Un cliente se lleva un violín y vuelve a la hora, enojado: no tenía nombre de dueño, ni color, ni nada. Había salido del taller **a medio hacer**.

—Un violín no puede salir así —dice Don Cedro—. Tiene que **nacer** con lo que le hace falta.

—Para eso está el **constructor** —agrega {mentor}—: lo que se hace en el momento del `new`. Si un objeto necesita datos, se los pedís al nacer, y no puede existir sin ellos.

### Objetivos

- Escribir un **constructor** que pida los datos al crear el objeto.
- Usar los inicializadores `{ … }` al crear.
- Usar `static` para algo que comparten todos los objetos, y `const` para un valor fijo.
- Escribir `ToString` para mostrar un objeto.

### Antes de empezar

- Propiedades (R02-N03).

### Explicación

#### El constructor

Un **constructor** es un método que corre en el `new`. Se llama **igual que la clase** y no tiene tipo de retorno:

```csharp
class Violin
{
    public string Duenio { get; }
    public string Color { get; set; }

    public Violin(string duenio, string color)
    {
        Duenio = duenio;
        Color = color;
    }
}
```

```csharp
Violin v = new Violin("Ceci", "rojo");   // nace completo
```

Una propiedad con solo `get` se puede asignar **en el constructor**: así queda fija para siempre.

Ojo: si escribís un constructor con parámetros, **el `new Violin()` vacío deja de existir**. El violín ya no puede nacer sin dueño.

#### Inicializadores

Después del constructor, se pueden dar más datos entre llaves:

```csharp
Violin v = new Violin("Bemol", "negro") { Anios = 3 };
```

#### `static`: uno solo para todos

Un campo o una propiedad `static` es de la **clase**, no de cada objeto: hay **uno solo**, compartido. Se usa con el nombre de la clase:

```csharp
class Violin
{
    public static int Fabricados { get; private set; }

    public Violin(string duenio)
    {
        Fabricados++;      // cada violín nuevo suma al contador de todos
    }
}
// Violin.Fabricados
```

`const` es un valor fijo que no cambia nunca: `public const int CuerdasMaximas = 5;`, y se usa como `Violin.CuerdasMaximas`.

#### `ToString`: cómo se muestra

Cuando ponés un objeto en un `WriteLine`, C# llama a su `ToString()`. Si no lo escribís, muestra solo el nombre de la clase. Con `override`, le das tu versión:

```csharp
public override string ToString()
{
    return $"Violín {Color} de {Duenio}";
}
```

(`override` quiere decir «reemplazo la versión que viene de fábrica»; lo vas a ver a fondo en la herencia.)

### Código de ejemplo

```csharp
Violin a = new Violin("Ceci", "rojo");
Violin b = new Violin("Bemol", "negro") { Anios = 3 };

Console.WriteLine(a);
Console.WriteLine(b);
Console.WriteLine($"Fabricados: {Violin.Fabricados}");
Console.WriteLine($"Máximo de cuerdas: {Violin.CuerdasMaximas}");

class Violin
{
    public const int CuerdasMaximas = 5;
    public static int Fabricados { get; private set; }

    public string Duenio { get; }
    public string Color { get; set; }
    public int Anios { get; set; }

    public Violin(string duenio, string color)
    {
        Duenio = duenio;
        Color = color;
        Fabricados++;
    }

    public override string ToString()
    {
        return $"Violín {Color} de {Duenio} ({Anios} años)";
    }
}
```

### Salida esperada

```
Violín rojo de Ceci (0 años)
Violín negro de Bemol (3 años)
Fabricados: 2
Máximo de cuerdas: 5
```

### ¿Para qué sirve?

Un pedido sin cliente, un jugador sin nombre, una cuenta sin titular: el constructor hace que esos objetos **no puedan existir**. Y `static` sirve para lo que es de todos: cuántos se crearon, la configuración, una tabla de precios compartida.

### Errores habituales

- **El constructor vacío desapareció:** si escribiste uno con parámetros, `new Violin()` ya no compila. El **goblin** de `CS7036` te dice qué dato falta.
- **Poner tipo de retorno al constructor:** `public void Violin(…)` ya no es un constructor, es un método más.
- **Usar `static` para algo de cada objeto:** si el color fuera `static`, todos los violines tendrían el mismo.

### Micro-misión R02-N04-P1 · Nacer con dueño

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: Constructor | public Clase(tipo dato) { Prop = dato; } · se llama igual que la clase · corre en el new
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
—Desde hoy —dice Don Cedro—, ningún violín sale de acá sin el nombre de su dueño. Ni uno.

#### Gheco sugiere
El constructor se escribe adentro de la clase, con el nombre de la clase y sin tipo de retorno. Recibe los datos y los guarda:

```csharp
class Tambor
{
    public string Marca { get; }

    public Tambor(string marca)
    {
        Marca = marca;
    }
}
```

#### Desafío
Escribí el constructor de `Violin` que reciba `string duenio` y lo guarde en `Duenio`.

#### Código inicial
```csharp
Violin v = new Violin("Ceci");
Console.WriteLine($"Violín de {v.Duenio}");

class Violin
{
    public string Duenio { get; }

    // el constructor
}
```

#### Salida esperada
```
Violín de Ceci
```

#### Solución
```csharp
Violin v = new Violin("Ceci");
Console.WriteLine($"Violín de {v.Duenio}");

class Violin
{
    public string Duenio { get; }

    public Violin(string duenio)
    {
        Duenio = duenio;
    }
}
```

#### Al superarla
Don Cedro graba el nombre con una punta fina dentro de la caja del violín, donde nadie lo ve pero siempre está.

#### Imagen
- El interior de la caja de un violín visto por la abertura en forma de efe, con un punzón fino apoyado al lado, sin letras visibles.
- Don Cedro trabaja con la lupa puesta; Ceci espera con el estuche abierto.

### Micro-misión R02-N04-P2 · Dos datos al nacer

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Bemol
carta: Constructor con varios | public Violin(string duenio, string color) · new Violin("Bemol", "negro")
recompensa: xp 15, oro 15
```

#### Escena
Bemol encarga un violín negro. Esta vez el pedido trae dos datos: dueño y color.

#### Gheco sugiere
El constructor recibe tantos parámetros como haga falta, separados con coma, en el mismo orden en que los pasás al `new`:

```csharp
public Tambor(string marca, int tamanio)
{
    Marca = marca;
    Tamanio = tamanio;
}
// new Tambor("Redoble", 14)
```

#### Desafío
Completá el `new` del programa con los dos datos: `Bemol` y `negro`.

#### Código inicial
```csharp
Violin v = new Violin();
Console.WriteLine($"{v.Color}, de {v.Duenio}");

class Violin
{
    public string Duenio { get; }
    public string Color { get; }

    public Violin(string duenio, string color)
    {
        Duenio = duenio;
        Color = color;
    }
}
```

#### Salida esperada
```
negro, de Bemol
```

#### Solución
```csharp
Violin v = new Violin("Bemol", "negro");
Console.WriteLine($"{v.Color}, de {v.Duenio}");

class Violin
{
    public string Duenio { get; }
    public string Color { get; }

    public Violin(string duenio, string color)
    {
        Duenio = duenio;
        Color = color;
    }
}
```

#### Al superarla
—Negro, como mis zapatillas —dice Bemol, que tiene un solo par, y bien gastado.

#### Imagen
- Un violín negro brillante en un estuche abierto de terciopelo bordó, sin letras.
- Bemol lo mira con la boca abierta y los anteojos torcidos; Ceci le da una palmada en el hombro.

### Micro-misión R02-N04-P3 · El contador de todos

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: static | public static int Fabricados · uno solo, de la clase · Violin.Fabricados
recompensa: xp 15, oro 15
```

#### Escena
Don Cedro quiere saber cuántos violines salieron del taller en total. No uno por violín: **uno solo**, para todos.

#### Gheco sugiere
Lo `static` es de la clase y lo comparten todos los objetos. Se usa con el nombre de la clase:

```csharp
class Tambor
{
    public static int Hechos { get; private set; }

    public Tambor()
    {
        Hechos++;
    }
}
// Tambor.Hechos
```

#### Desafío
En el constructor, sumá uno a `Fabricados`. El programa fabrica tres violines.

#### Código inicial
```csharp
Violin a = new Violin("Ceci");
Violin b = new Violin("Bemol");
Violin c = new Violin("Clave");
Console.WriteLine($"Fabricados: {Violin.Fabricados}");

class Violin
{
    public static int Fabricados { get; private set; }
    public string Duenio { get; }

    public Violin(string duenio)
    {
        Duenio = duenio;
    }
}
```

#### Salida esperada
```
Fabricados: 3
```

#### Solución
```csharp
Violin a = new Violin("Ceci");
Violin b = new Violin("Bemol");
Violin c = new Violin("Clave");
Console.WriteLine($"Fabricados: {Violin.Fabricados}");

class Violin
{
    public static int Fabricados { get; private set; }
    public string Duenio { get; }

    public Violin(string duenio)
    {
        Duenio = duenio;
        Fabricados++;
    }
}
```

#### Al superarla
Don Cedro marca tres rayitas en la pared, junto a cientos de otras. —Tres más —dice—. Este taller no para.

#### Imagen
- Una pared de madera del taller llena de rayitas talladas en grupos, iluminada por una lámpara cálida, sin números ni letras.
- Don Cedro talla una rayita nueva con un formón; Ceci cuenta con el dedo.

### Micro-misión R02-N04-P4 · Cómo se presenta

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Clave
carta: ToString | public override string ToString() { return …; } · WriteLine(objeto) lo usa solo
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Ceci muestra un violín con `WriteLine` y aparece una palabra fea: `Violin`. —Así no se presenta un instrumento —dice Clave.

#### Gheco sugiere
Cuando ponés un objeto en un `WriteLine`, C# usa su `ToString()`. Escribí el tuyo con `override`:

```csharp
public override string ToString()
{
    return $"Tambor {Marca}";
}
```

#### Desafío
Escribí el `ToString` de `Violin` para que muestre `Violín de <Duenio>`.

#### Código inicial
```csharp
Violin v = new Violin("Ceci");
Console.WriteLine(v);

class Violin
{
    public string Duenio { get; }

    public Violin(string duenio)
    {
        Duenio = duenio;
    }

    // ToString
}
```

#### Salida esperada
```
Violín de Ceci
```

#### Solución
```csharp
Violin v = new Violin("Ceci");
Console.WriteLine(v);

class Violin
{
    public string Duenio { get; }

    public Violin(string duenio)
    {
        Duenio = duenio;
    }

    public override string ToString()
    {
        return $"Violín de {Duenio}";
    }
}
```

#### Al superarla
—Mucho mejor —dice Clave—. Un objeto que sabe presentarse se entiende al primer vistazo.

#### Imagen
- Un violín en un atril iluminado por un haz de luz, como en una presentación, con cortinas bordó a los costados, sin letras.
- Clave lo presenta con un gesto de la mano; Ceci hace una pequeña reverencia.

### Micro-misión R02-N04-P5 · El goblin del violín vacío

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Gheco, Don Cedro
criatura: goblin
carta: Goblin | CS7036: falta un argumento · el constructor pide datos · el new vacío ya no existe
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
El goblin quiere sacar del taller un violín sin dueño, con un `new` vacío. Pero el plano ya no lo permite.

#### Gheco sugiere
Si el constructor pide un dato, el `new` tiene que dárselo:

```
error CS7036: No se ha dado ningún argumento que corresponda al parámetro requerido "duenio" de "Violin.Violin(string)"
```

El error dice qué parámetro falta: `duenio`.

#### Desafío
Ensayá, leé el error y dale al violín el dueño `el taller`.

#### Código inicial
```csharp
Violin v = new Violin();
Console.WriteLine($"Violín de {v.Duenio}");

class Violin
{
    public string Duenio { get; }

    public Violin(string duenio)
    {
        Duenio = duenio;
    }
}
```

#### Salida esperada
```
Violín de el taller
```

#### Solución
```csharp
Violin v = new Violin("el taller");
Console.WriteLine($"Violín de {v.Duenio}");

class Violin
{
    public string Duenio { get; }

    public Violin(string duenio)
    {
        Duenio = duenio;
    }
}
```

#### Al superarla
El goblin intenta salir con el violín bajo el brazo, pero el violín ya tiene dueño: el taller. Don Cedro lo frena en la puerta con una sola mirada.

#### Imagen
- Un goblin chico con un violín bajo el brazo, frenado en seco en la puerta de un taller de madera.
- Don Cedro lo mira desde adentro, con los brazos cruzados y los anteojos en la punta de la nariz.

### Encargo R02-N04-E1 · Las entradas de la Feria

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

El Flaco Ruiz vende entradas numeradas. Escribí una clase `Entrada` con:

- un `static` que lleve la cuenta de las entradas vendidas,
- un constructor que reciba el nombre del comprador y le dé a cada entrada el número siguiente (la primera es la `1`),
- un `const` `Precio` de `250`,
- y un `ToString` que muestre `Entrada <numero>: <nombre>`.

Vendé tres entradas (`Nima`, `Ceci` y `Bruno`), mostralas y mostrá la recaudación:

```
Entrada 1: Nima
Entrada 2: Ceci
Entrada 3: Bruno
Recaudado: 750
```

#### Criterio de aprobación

- El número de cada entrada sale del contador `static`, no se escribe a mano.
- Las entradas se muestran con su `ToString`.

#### Salida esperada

```
Entrada 1: Nima
Entrada 2: Ceci
Entrada 3: Bruno
Recaudado: 750
```

#### Solución de referencia

```csharp
Entrada[] vendidas = { new Entrada("Nima"), new Entrada("Ceci"), new Entrada("Bruno") };
foreach (Entrada e in vendidas)
{
    Console.WriteLine(e);
}
Console.WriteLine($"Recaudado: {Entrada.Vendidas * Entrada.Precio}");

class Entrada
{
    public const int Precio = 250;
    public static int Vendidas { get; private set; }

    public int Numero { get; }
    public string Nombre { get; }

    public Entrada(string nombre)
    {
        Vendidas++;
        Numero = Vendidas;
        Nombre = nombre;
    }

    public override string ToString()
    {
        return $"Entrada {Numero}: {Nombre}";
    }
}
```

## R02-N05 · Valor o referencia: struct y enum

```meta
tipo: tema
padre: R02-N04
precio: 10
criatura: troll
temas: prog.referencias, prog.enums
usa: poo.clases
```

### Crónica

Ceci le presta su violín a Bemol «para que practique con uno igual». A la tarde, el violín de Ceci aparece con una cuerda rota. —¡Yo rompí el mío, no el tuyo! —dice Bemol. Pero era el mismo: nunca hubo dos.

—Una variable de una clase no guarda el violín —explica {mentor}—: guarda **dónde está**. Si le pasás esa dirección a otro, los dos miran el **mismo** violín. Hay tipos que sí se copian enteros, y otros que solo se copian de lugar. Hoy aprendés a distinguirlos.

### Objetivos

- Distinguir los tipos **por valor** (se copian) de los tipos **por referencia** (se comparten).
- Escribir un `struct` para datos chicos.
- Escribir un `enum` para una lista cerrada de opciones.

### Antes de empezar

- Constructores (R02-N04). En el R01-N12 ya viste que dos nombres pueden mirar el mismo arreglo.

### Explicación

#### Dos familias

| | Por **valor** | Por **referencia** |
|---|---|---|
| Ejemplos | `int`, `double`, `bool`, `struct`, `enum` | `class`, arreglos, `string` |
| La variable guarda… | el dato | **dónde está** el objeto |
| `b = a` | copia el dato | los dos miran **el mismo** objeto |

```csharp
Violin a = new Violin();
Violin b = a;          // b no es otro violín: es otro nombre para el mismo
b.Color = "verde";
Console.WriteLine(a.Color);   // verde
```

Para tener dos de verdad, hay que hacer otro `new`.

#### `struct`: un dato chico que se copia

Un `struct` se escribe como una clase, pero es **por valor**: al asignarlo, se copia entero. Sirve para datos chicos, como una posición en el escenario. (Unity usa `struct` para sus posiciones: `Vector2` y `Vector3`.)

```csharp
struct Lugar
{
    public int Fila;
    public int Butaca;
}
```

```csharp
Lugar a = new Lugar { Fila = 3, Butaca = 5 };
Lugar b = a;       // copia
b.Butaca = 9;
Console.WriteLine(a.Butaca);   // 5: a no cambió
```

#### `enum`: una lista cerrada

Cuando algo solo puede ser una de pocas opciones, un `enum` les pone nombre. Es mejor que un número o un texto que se puede escribir mal:

```csharp
enum Cuerda { Sol, Re, La, Mi }

Cuerda c = Cuerda.La;
Console.WriteLine(c);          // La
Console.WriteLine((int)c);     // 2: por dentro es un número, desde el 0
```

Combina muy bien con el `switch`:

```csharp
string tono = c switch
{
    Cuerda.Sol => "grave",
    Cuerda.Mi => "agudo",
    _ => "medio",
};
```

### Código de ejemplo

```csharp
Violin a = new Violin();
Violin b = a;
b.Color = "verde";
Console.WriteLine($"a: {a.Color}");

Lugar x = new Lugar { Fila = 3, Butaca = 5 };
Lugar y = x;
y.Butaca = 9;
Console.WriteLine($"x: fila {x.Fila}, butaca {x.Butaca}");

Cuerda c = Cuerda.Mi;
Console.WriteLine($"{c} es la número {(int)c}");

enum Cuerda { Sol, Re, La, Mi }

struct Lugar
{
    public int Fila;
    public int Butaca;
}

class Violin
{
    public string Color { get; set; } = "natural";
}
```

### Salida esperada

```
a: verde
x: fila 3, butaca 5
Mi es la número 3
```

### ¿Para qué sirve?

Saber si algo se copia o se comparte evita los errores más raros: «yo cambié el mío y se cambió el tuyo». Los `enum` aparecen en todos lados: el estado de un pedido, la dirección de un personaje, el día de la semana, la dificultad de un juego.

### Errores habituales

- **Creer que `b = a` copia un objeto de una clase:** solo copia la dirección. El **troll** de las referencias compartidas vive de esto.
- **Escribir el `enum` como texto:** `"La"` no es lo mismo que `Cuerda.La`, y un texto se puede escribir mal sin que nadie avise.
- **Hacer `struct` algo grande o que cambia mucho:** el `struct` es para datos chicos; para lo demás, una clase.

### Micro-misión R02-N05-P1 · Dos nombres, un violín

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Bemol
carta: Referencia | Violin b = a; → el mismo violín · para otro, new Violin()
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Ceci y Bemol quieren dos violines para practicar juntos. El programa dice que tienen dos, pero cuando Bemol lo pinta de verde, el de Ceci también cambia.

#### Gheco sugiere
`b = a` no fabrica nada: los dos nombres miran el mismo objeto. Para tener dos, hacen falta **dos `new`**:

```csharp
Tambor mio = new Tambor();
Tambor tuyo = new Tambor();   // otro tambor de verdad
```

#### Desafío
Cambiá la línea de `deBemol` para que sea un violín nuevo, así el de Ceci sigue `natural`.

#### Código inicial
```csharp
Violin deCeci = new Violin();
Violin deBemol = deCeci;
deBemol.Color = "verde";
Console.WriteLine($"Ceci: {deCeci.Color}");
Console.WriteLine($"Bemol: {deBemol.Color}");

class Violin
{
    public string Color { get; set; } = "natural";
}
```

#### Salida esperada
```
Ceci: natural
Bemol: verde
```

#### Solución
```csharp
Violin deCeci = new Violin();
Violin deBemol = new Violin();
deBemol.Color = "verde";
Console.WriteLine($"Ceci: {deCeci.Color}");
Console.WriteLine($"Bemol: {deBemol.Color}");

class Violin
{
    public string Color { get; set; } = "natural";
}
```

#### Al superarla
Ahora hay dos violines de verdad. Bemol pinta el suyo de verde y Ceci respira aliviada.

#### Imagen
- Dos violines sobre una mesa de taller: uno de madera natural y otro recién pintado de verde, con un pincel apoyado, sin letras.
- Bemol pinta con cuidado; Ceci abraza el suyo, aliviada.

### Micro-misión R02-N05-P2 · La butaca copiada

```meta
lugar: El Escenario Grande
personajes: Ceci, Clave
carta: struct | struct Lugar { public int Fila; } · Lugar b = a; copia todo · cambiar b no cambia a
recompensa: xp 15, oro 15
```

#### Escena
Clave anota los lugares del concierto con un `struct`. Ceci copia el lugar de Clave para sentarse al lado, y cambia solo la butaca.

#### Gheco sugiere
Un `struct` se copia entero al asignarlo. Por eso, cambiar la copia no toca el original:

```csharp
Punto a = new Punto { X = 1 };
Punto b = a;
b.X = 7;      // a.X sigue en 1
```

#### Desafío
Hacé que `ceci` sea una copia de `clave` y cambiale la butaca a `6`. El lugar de Clave tiene que quedar igual.

#### Código inicial
```csharp
Lugar clave = new Lugar { Fila = 2, Butaca = 5 };
Lugar ceci = new Lugar();

// copiá y cambiá la butaca


Console.WriteLine($"Clave: fila {clave.Fila}, butaca {clave.Butaca}");
Console.WriteLine($"Ceci: fila {ceci.Fila}, butaca {ceci.Butaca}");

struct Lugar
{
    public int Fila;
    public int Butaca;
}
```

#### Salida esperada
```
Clave: fila 2, butaca 5
Ceci: fila 2, butaca 6
```

#### Solución
```csharp
Lugar clave = new Lugar { Fila = 2, Butaca = 5 };
Lugar ceci = new Lugar();

ceci = clave;
ceci.Butaca = 6;

Console.WriteLine($"Clave: fila {clave.Fila}, butaca {clave.Butaca}");
Console.WriteLine($"Ceci: fila {ceci.Fila}, butaca {ceci.Butaca}");

struct Lugar
{
    public int Fila;
    public int Butaca;
}
```

#### Al superarla
Ceci se sienta al lado de Clave, en la misma fila. Clave no la mira, pero corre un poco su capa para hacerle lugar.

#### Imagen
- Una fila de butacas de terciopelo bordó en un teatro gótico de piedra, con dos butacas vecinas iluminadas, sin números.
- Clave sentada muy derecha y Ceci sentándose a su lado con el violín en la falda.

### Micro-misión R02-N05-P3 · Las cuatro cuerdas con nombre

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: enum | enum Cuerda { Sol, Re, La, Mi } · Cuerda c = Cuerda.La; · (int)c da su número
recompensa: xp 15, oro 15
```

#### Escena
Don Cedro numera las cuerdas: 0, 1, 2, 3. Ceci prefiere llamarlas por su nombre.

#### Gheco sugiere
Un `enum` es una lista cerrada de nombres. Se escribe al final, como las clases, y se usa con el punto:

```csharp
enum Dia { Lunes, Martes, Miercoles }

Dia hoy = Dia.Martes;
Console.WriteLine(hoy);        // Martes
Console.WriteLine((int)hoy);   // 1
```

#### Desafío
Escribí el `enum Cuerda` con `Sol`, `Re`, `La` y `Mi`, en ese orden.

#### Código inicial
```csharp
Cuerda c = Cuerda.La;
Console.WriteLine($"{c} es la cuerda {(int)c}");

// el enum
```

#### Salida esperada
```
La es la cuerda 2
```

#### Solución
```csharp
Cuerda c = Cuerda.La;
Console.WriteLine($"{c} es la cuerda {(int)c}");

enum Cuerda { Sol, Re, La, Mi }
```

#### Al superarla
—La, la cuerda dos —repite Don Cedro—. Bueno, con nombre suena mejor. Lo admito.

#### Imagen
- El clavijero de un violín de cerca, con sus cuatro cuerdas brillando en cuatro colores suaves distintos, sin letras.
- Don Cedro las señala con la punta del lápiz; Ceci las cuenta con los dedos.

### Micro-misión R02-N05-P4 · Cada cuerda, su tono

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Bemol
carta: enum + switch | c switch { Cuerda.Sol => "grave", … , _ => "medio" }
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol quiere un método que diga si una cuerda suena grave, media o aguda. —Sol es la más grave y Mi la más aguda —dice—. Las otras dos, en el medio.

#### Gheco sugiere
La expresión `switch` elige un valor según el `enum`. El `_` es «cualquier otro»:

```csharp
string tipo = hoy switch
{
    Dia.Lunes => "empieza",
    _ => "sigue",
};
```

#### Desafío
Completá `Tono` con un `switch`: `Sol` es `grave`, `Mi` es `agudo` y las demás, `medio`.

#### Código inicial
```csharp
Console.WriteLine(Tono(Cuerda.Sol));
Console.WriteLine(Tono(Cuerda.Re));
Console.WriteLine(Tono(Cuerda.Mi));

static string Tono(Cuerda c)
{
    return "medio";
}

enum Cuerda { Sol, Re, La, Mi }
```

#### Salida esperada
```
grave
medio
agudo
```

#### Solución
```csharp
Console.WriteLine(Tono(Cuerda.Sol));
Console.WriteLine(Tono(Cuerda.Re));
Console.WriteLine(Tono(Cuerda.Mi));

static string Tono(Cuerda c)
{
    return c switch
    {
        Cuerda.Sol => "grave",
        Cuerda.Mi => "agudo",
        _ => "medio",
    };
}

enum Cuerda { Sol, Re, La, Mi }
```

#### Al superarla
Bemol toca las cuatro cuerdas del violín de Ceci, de la más grave a la más aguda, y dice el tono de cada una antes de que suene. Acierta las cuatro.

#### Imagen
- Cuatro notas musicales doradas flotando en escalera, de la más grande y baja a la más chica y alta, sobre un violín, sin letras.
- Bemol pulsa las cuerdas con un dedo; Ceci escucha con los ojos cerrados.

### Micro-misión R02-N05-P5 · El troll del violín prestado

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Gheco
criatura: troll
carta: Troll | un método recibe la dirección · si cambia el objeto, cambia el tuyo · prestá una copia
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un troll chiquito pide un violín «para mirarlo nomás», y lo devuelve pintado de violeta. El método `Prestar` le dio **el mismo** violín.

#### Gheco sugiere
Un objeto de una clase se pasa a un método **por referencia**: el método recibe la dirección y puede cambiar el original. Para que no lo toque, prestale una **copia**: un violín nuevo con los mismos datos.

```csharp
Tambor copia = new Tambor { Color = original.Color };
```

#### Desafío
Cambiá la llamada para que el troll reciba una copia del violín, no el original.

#### Código inicial
```csharp
Violin mio = new Violin { Color = "rojo" };

Prestar(mio);
Console.WriteLine($"Mi violín: {mio.Color}");

static void Prestar(Violin v)
{
    v.Color = "violeta";
}

class Violin
{
    public string Color { get; set; } = "natural";
}
```

#### Salida esperada
```
Mi violín: rojo
```

#### Solución
```csharp
Violin mio = new Violin { Color = "rojo" };

Prestar(new Violin { Color = mio.Color });
Console.WriteLine($"Mi violín: {mio.Color}");

static void Prestar(Violin v)
{
    v.Color = "violeta";
}

class Violin
{
    public string Color { get; set; } = "natural";
}
```

#### Al superarla
El troll devuelve la copia pintada de violeta, muy orgulloso. El violín rojo de Ceci nunca salió del estuche.

#### Imagen
- Un troll chiquito de piel color musgo, pelo de paja y chaleco remendado, sosteniendo orgulloso un violín pintado de violeta con un pincel en la otra mano.
- Ceci abraza su estuche cerrado; Gheco, en su hombro, guiña un ojo.

### Encargo R02-N05-E1 · El semáforo de la calesita

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

El guardia de la calesita usa tres luces para dejar subir a los chicos. Escribí un `enum Luz { Roja, Amarilla, Verde }` y un método `Siguiente(Luz actual)` que devuelva la luz que sigue (Verde → Amarilla → Roja → Verde) usando un `switch`. Empezando en `Verde`, mostrá cinco cambios con un bucle:

```
Verde
Amarilla
Roja
Verde
Amarilla
```

#### Criterio de aprobación

- Las luces son un `enum`, no textos.
- `Siguiente` usa un `switch` y el bucle la llama en cada vuelta.

#### Salida esperada

```
Verde
Amarilla
Roja
Verde
Amarilla
```

#### Solución de referencia

```csharp
Luz luz = Luz.Verde;
for (int i = 0; i < 5; i++)
{
    Console.WriteLine(luz);
    luz = Siguiente(luz);
}

static Luz Siguiente(Luz actual)
{
    return actual switch
    {
        Luz.Verde => Luz.Amarilla,
        Luz.Amarilla => Luz.Roja,
        _ => Luz.Verde,
    };
}

enum Luz { Roja, Amarilla, Verde }
```

## R02-N06 · record y null: lo que se compara y lo que falta

```meta
tipo: tema
padre: R02-N05
precio: 10
criatura: troll
temas: poo.records, err.opcionales
usa: poo.clases, prog.condicionales
```

### Crónica

En el fondo del taller hay un fichero con las fichas de todos los violines que pasaron por ahí. Algunas fichas dicen el **apodo** del violín («el Gruñón», «la Viejita»); otras, nada. Y cuando Ceci quiere mostrar un apodo que no existe, el programa explota.

—Eso es **`null`** —dice {mentor}—: «acá no hay nada». Es la trampa más famosa de todas. Hoy aprendés a esquivarla. Y para las fichas, que son solo datos, C# tiene algo mejor que una clase: el **`record`**.

### Objetivos

- Escribir un `record` en una línea y compararlo por su contenido.
- Copiar un `record` cambiando un dato con `with`.
- Marcar con `?` lo que puede faltar y usar `??` y `?.` para no explotar.

### Antes de empezar

- Valor y referencia (R02-N05).

### Explicación

#### `record`: una clase para datos

```csharp
record Ficha(string Nombre, int Anios);
```

En esa línea ya tenés: constructor, propiedades de solo lectura y un `ToString` que muestra todo.

```csharp
Ficha a = new Ficha("Violín rojo", 12);
Console.WriteLine(a);    // Ficha { Nombre = Violín rojo, Anios = 12 }
```

Y su `==` compara el **contenido**, no la dirección:

```csharp
Ficha b = new Ficha("Violín rojo", 12);
Console.WriteLine(a == b);   // True: tienen los mismos datos
```

#### `with`: copiar cambiando algo

```csharp
Ficha vieja = a with { Anios = 13 };   // a no cambia
```

#### `null`: «no hay nada»

Una variable de referencia puede no apuntar a ningún objeto: vale `null`. Si usás algo que es `null`, el programa explota con `NullReferenceException`.

C# te ayuda marcando en el tipo qué puede faltar:

- `string apodo`: **no** debería ser `null`.
- `string? apodo`: **puede** ser `null`, y el compilador te pide que lo revises.

| Escritura | Qué hace | Ejemplo |
|---|---|---|
| `a ?? b` | si `a` es `null`, usa `b` | `apodo ?? "sin apodo"` |
| `a?.B` | si `a` es `null`, da `null` sin explotar | `apodo?.Length` |
| `a is null` | pregunta si falta | `if (apodo is null)` |

### Código de ejemplo

```csharp
Ficha a = new Ficha("Violín rojo", 12, "el Gruñón");
Ficha b = new Ficha("Violín rojo", 12, "el Gruñón");
Ficha c = a with { Anios = 13, Apodo = null };

Console.WriteLine(a == b);
Console.WriteLine(c);
Console.WriteLine($"Apodo de c: {c.Apodo ?? "sin apodo"}");
Console.WriteLine($"Letras del apodo de a: {a.Apodo?.Length}");

record Ficha(string Nombre, int Anios, string? Apodo);
```

### Salida esperada

```
True
Ficha { Nombre = Violín rojo, Anios = 13, Apodo =  }
Apodo de c: sin apodo
Letras del apodo de a: 9
```

### ¿Para qué sirve?

Los `record` son perfectos para lo que viaja de un lado a otro: un pedido, un mensaje, un dato que llega de internet. Y `null` aparece en todos lados: un usuario sin teléfono, una búsqueda que no encontró nada. El que sabe esquivarlo no tiene sorpresas.

### Errores habituales

- **Usar algo que puede ser `null` sin revisarlo:** el **troll** de `NullReferenceException` aparece en el peor momento. Usá `??`, `?.` o un `if`.
- **Querer cambiar un dato de un `record`:** sus propiedades son de solo lectura. Para «cambiarlo», hacé una copia con `with`.
- **Comparar clases con `==`:** dos objetos de una clase con los mismos datos **no** son iguales con `==`; dos `record`, sí.

### Micro-misión R02-N06-P1 · La ficha en una línea

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: record | record Ficha(string Nombre, int Anios); · constructor, propiedades y ToString incluidos
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Don Cedro abre el fichero. —Cada ficha: nombre del violín y años. Nada más. No me hagas una clase de veinte líneas para eso.

#### Gheco sugiere
Un `record` declara todo en una línea. Se escribe al final, como las clases:

```csharp
record Nota(string Nombre, int Duracion);

Nota n = new Nota("La", 4);
Console.WriteLine(n);   // Nota { Nombre = La, Duracion = 4 }
```

#### Desafío
Escribí el `record Ficha` con `string Nombre` e `int Anios`.

#### Código inicial
```csharp
Ficha f = new Ficha("Violín rojo", 12);
Console.WriteLine(f);

// el record
```

#### Salida esperada
```
Ficha { Nombre = Violín rojo, Anios = 12 }
```

#### Solución
```csharp
Ficha f = new Ficha("Violín rojo", 12);
Console.WriteLine(f);

record Ficha(string Nombre, int Anios);
```

#### Al superarla
—Una línea —dice Don Cedro, contando con el dedo—. Así me gusta. Lo que es simple, que se escriba simple.

#### Imagen
- Un fichero de madera abierto con fichas de cartón lisas, sin escritura, sobre un escritorio del taller.
- Don Cedro saca una ficha con dos dedos; Ceci la recibe.

### Micro-misión R02-N06-P2 · Dos fichas iguales

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Bemol
carta: == en un record | compara el contenido · dos fichas con los mismos datos son iguales
recompensa: xp 15, oro 15
```

#### Escena
Bemol encontró dos fichas repetidas en el fichero y quiere saber si son de verdad iguales.

#### Gheco sugiere
Dos `record` con los mismos datos son iguales con `==`, aunque sean dos objetos distintos:

```csharp
Nota a = new Nota("La", 4);
Nota b = new Nota("La", 4);
Console.WriteLine(a == b);   // True
```

#### Desafío
Mostrá si `a` es igual a `b`, y si `a` es igual a `c`.

#### Código inicial
```csharp
Ficha a = new Ficha("Violín rojo", 12);
Ficha b = new Ficha("Violín rojo", 12);
Ficha c = new Ficha("Violín azul", 12);

// compará

record Ficha(string Nombre, int Anios);
```

#### Salida esperada
```
True
False
```

#### Solución
```csharp
Ficha a = new Ficha("Violín rojo", 12);
Ficha b = new Ficha("Violín rojo", 12);
Ficha c = new Ficha("Violín azul", 12);

Console.WriteLine(a == b);
Console.WriteLine(a == c);

record Ficha(string Nombre, int Anios);
```

#### Al superarla
Bemol tira la ficha repetida al canasto. —Una sola por violín. Si no, después no sabemos cuál es cuál.

#### Imagen
- Dos fichas de cartón lisas e idénticas lado a lado sobre una mesa, y un canasto de mimbre al costado, sin letras.
- Bemol compara las fichas con los anteojos en la frente; Ceci se ríe.

### Micro-misión R02-N06-P3 · Un año más

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: with | Ficha nueva = vieja with { Anios = 13 }; · copia cambiando un dato · la vieja no cambia
recompensa: xp 15, oro 15
```

#### Escena
Pasó un año. Don Cedro no tacha fichas: hace una nueva con un año más y guarda la vieja.

#### Gheco sugiere
Las propiedades de un `record` no se cambian: se hace una **copia** con `with`, cambiando lo que haga falta:

```csharp
Nota larga = n with { Duracion = 8 };
```

#### Desafío
Creá `nueva` como una copia de `vieja` con `Anios` en `13`.

#### Código inicial
```csharp
Ficha vieja = new Ficha("Violín rojo", 12);

// la ficha nueva


Console.WriteLine(vieja);
Console.WriteLine(nueva);

record Ficha(string Nombre, int Anios);
```

#### Salida esperada
```
Ficha { Nombre = Violín rojo, Anios = 12 }
Ficha { Nombre = Violín rojo, Anios = 13 }
```

#### Solución
```csharp
Ficha vieja = new Ficha("Violín rojo", 12);

Ficha nueva = vieja with { Anios = 13 };

Console.WriteLine(vieja);
Console.WriteLine(nueva);

record Ficha(string Nombre, int Anios);
```

#### Al superarla
—Las fichas viejas no se tiran —dice Don Cedro—. Cuentan la historia del violín.

#### Imagen
- Una pila ordenada de fichas de cartón lisas atadas con un hilo, al lado de una ficha nueva más blanca, sin letras.
- Don Cedro ata la pila con cariño; Ceci sostiene la ficha nueva.

### Micro-misión R02-N06-P4 · El apodo que falta

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Bemol, Don Cedro
carta: ?? | string? puede faltar · apodo ?? "sin apodo" · si es null, usa lo de la derecha
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Algunos violines tienen apodo y otros no. Bemol quiere que, si no tiene, diga `sin apodo`.

#### Gheco sugiere
`??` usa lo de la izquierda si tiene algo, y lo de la derecha si es `null`:

```csharp
string? sobrenombre = null;
Console.WriteLine(sobrenombre ?? "ninguno");   // ninguno
```

#### Desafío
Completá `Mostrar` para que use el apodo, o `sin apodo` si falta.

#### Código inicial
```csharp
Mostrar(new Ficha("Violín rojo", "el Gruñón"));
Mostrar(new Ficha("Violín azul", null));

static void Mostrar(Ficha f)
{
    Console.WriteLine($"{f.Nombre}: {f.Apodo}");
}

record Ficha(string Nombre, string? Apodo);
```

#### Salida esperada
```
Violín rojo: el Gruñón
Violín azul: sin apodo
```

#### Solución
```csharp
Mostrar(new Ficha("Violín rojo", "el Gruñón"));
Mostrar(new Ficha("Violín azul", null));

static void Mostrar(Ficha f)
{
    Console.WriteLine($"{f.Nombre}: {f.Apodo ?? "sin apodo"}");
}

record Ficha(string Nombre, string? Apodo);
```

#### Al superarla
—«El Gruñón» —lee Ceci—. ¿Por qué le dicen así? —Porque suena como yo a la mañana —contesta Don Cedro.

#### Imagen
- Un violín viejo de madera oscura con aspecto un poco malhumorado por sus vetas, sobre un paño bordó, sin letras.
- Don Cedro hace la misma cara que el violín; Ceci y Bemol se tientan de risa.

### Micro-misión R02-N06-P5 · El troll del atril vacío

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Gheco
criatura: troll
carta: Troll | NullReferenceException · usaste algo que es null · ?. o ?? antes de usarlo
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
El troll se escondió en el atril vacío: el programa pide el largo de un apodo que no existe, y explota.

#### Gheco sugiere
`?.` pregunta antes de entrar: si lo de la izquierda es `null`, da `null` sin explotar. Y con `??` le das un valor por si falta:

```csharp
string? s = null;
int largo = s?.Length ?? 0;   // 0, sin explotar
```

#### Desafío
Ensayá, mirá cómo explota y arreglá la línea para que, si no hay apodo, el largo sea `0`.

#### Código inicial
```csharp
string? apodo = null;
int largo = apodo!.Length;
Console.WriteLine($"Letras: {largo}");
```

#### Salida esperada
```
Letras: 0
```

#### Solución
```csharp
string? apodo = null;
int largo = apodo?.Length ?? 0;
Console.WriteLine($"Letras: {largo}");
```

#### Al superarla
El troll sale del atril, ve que ya no hay nada que romper y se va a dormir debajo de una mesa.

#### Imagen
- Un atril de madera vacío en un rincón del taller, con un troll chiquito de piel color musgo saliendo de atrás, bostezando.
- Gheco, sobre el atril, le señala la puerta con la cola.

### Encargo R02-N06-E1 · Los pedidos de Elefa

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Elefa registra los pedidos del Puerto. Escribí un `record Pedido(int Numero, string Cliente, decimal Total, string? Nota)`.

1. Creá el pedido `1` de `Tizón` por `1500`, sin nota.
2. Creá una copia con `with` que tenga `Total` `1800` y la nota `urgente`.
3. Mostrá los dos pedidos en una línea cada uno, con la nota o `sin nota`, y si son iguales:

```
Pedido 1 de Tizón: 1500 (sin nota)
Pedido 1 de Tizón: 1800 (urgente)
¿Iguales? False
```

#### Criterio de aprobación

- El pedido es un `record` y la copia se hace con `with`.
- La nota que falta se muestra con `??`.

#### Salida esperada

```
Pedido 1 de Tizón: 1500 (sin nota)
Pedido 1 de Tizón: 1800 (urgente)
¿Iguales? False
```

#### Solución de referencia

```csharp
Pedido a = new Pedido(1, "Tizón", 1500, null);
Pedido b = a with { Total = 1800, Nota = "urgente" };

Mostrar(a);
Mostrar(b);
Console.WriteLine($"¿Iguales? {a == b}");

static void Mostrar(Pedido p)
{
    Console.WriteLine($"Pedido {p.Numero} de {p.Cliente}: {p.Total} ({p.Nota ?? "sin nota"})");
}

record Pedido(int Numero, string Cliente, decimal Total, string? Nota);
```

## R02-N07 · Herencia: la familia de las cuerdas

```meta
tipo: tema
padre: R02-N06
precio: 10
criatura: ogro
temas: poo.herencia
usa: poo.constructores, poo.encapsulamiento
```

### Crónica

Don Cedro no solo hace violines: también violas, chelos y contrabajos. —Son todos de la misma familia —dice—: madera, cuerdas, arco. Cambia el tamaño y la voz. No voy a dibujar cuatro planos desde cero.

—Entonces dibujá uno **general** —dice {mentor}— y que los otros **hereden** de él. Lo que tienen en común se escribe una vez; cada uno agrega lo suyo.

### Objetivos

- Escribir una clase que **hereda** de otra con `:`.
- Llamar al constructor de la base con `base(…)`.
- Usar `protected` para lo que comparten la base y sus derivadas.
- Cambiar un método de la base con `virtual` y `override`.

### Antes de empezar

- Constructores (R02-N04) y `record` (R02-N06).

### Explicación

#### Heredar

```csharp
class Cuerdas
{
    public string Nombre { get; }
    public int CantidadCuerdas { get; } = 4;

    public Cuerdas(string nombre)
    {
        Nombre = nombre;
    }
}

class Chelo : Cuerdas      // Chelo hereda de Cuerdas
{
    public Chelo() : base("chelo") { }
}
```

La clase **derivada** (`Chelo`) recibe todo lo de la **base** (`Cuerdas`) y puede agregar lo suyo. Se usa cuando se puede decir «**es un**»: un chelo *es un* instrumento de cuerdas. En C#, una clase hereda de **una sola**.

**El constructor:** la derivada tiene que llamar al de la base con `: base(…)`, pasándole lo que pide.

#### `protected`

Lo `private` no lo ve ni la derivada. Lo `protected` lo ven la base **y sus derivadas**, pero no los de afuera.

#### Cambiar un comportamiento: `virtual` y `override`

La base marca con `virtual` lo que las derivadas **pueden** cambiar, y la derivada lo cambia con `override`:

```csharp
class Cuerdas
{
    public virtual string Voz() => "media";
}

class Contrabajo : Cuerdas
{
    public override string Voz() => "muy grave";
}
```

Con `base.Voz()`, la derivada puede usar la versión de la base dentro de la suya.

### Código de ejemplo

```csharp
Cuerdas v = new Violin();
Chelo c = new Chelo();
Console.WriteLine($"{v.Nombre}: {v.Voz()}, {v.CantidadCuerdas} cuerdas");
Console.WriteLine($"{c.Nombre}: {c.Voz()}, {c.CantidadCuerdas} cuerdas");
c.Apoyar();

class Cuerdas
{
    public string Nombre { get; }
    public int CantidadCuerdas { get; } = 4;

    public Cuerdas(string nombre)
    {
        Nombre = nombre;
    }

    public virtual string Voz() => "media";
}

class Violin : Cuerdas
{
    public Violin() : base("violín") { }

    public override string Voz() => "aguda";
}

class Chelo : Cuerdas
{
    public Chelo() : base("chelo") { }

    public override string Voz() => "grave";

    public void Apoyar()
    {
        Console.WriteLine("El chelo se apoya en el piso");
    }
}
```

### Salida esperada

```
violín: aguda, 4 cuerdas
chelo: grave, 4 cuerdas
El chelo se apoya en el piso
```

### ¿Para qué sirve?

En un juego, un `Enemigo` general y de él heredan el `Ogro`, el `Goblin` y el `Dragon`. En una empresa, un `Empleado` y de él el `Gerente` y el `Cajero`. Lo común se escribe una sola vez; cada uno cambia lo que lo hace distinto.

### Errores habituales

- **Heredar cuando no «es un»:** un violín **tiene** cuerdas, pero no **es** una cuerda. Para «tiene un» está la composición (R02-N10).
- **Olvidar el `: base(…)`:** si la base pide datos en su constructor, la derivada tiene que pasárselos (`CS7036`).
- **Olvidar el `override`:** sin él, el método de la derivada no reemplaza al de la base, y el **ogro** hace sonar la versión equivocada sin que nada avise.

### Micro-misión R02-N07-P1 · La viola, hija de las cuerdas

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: Herencia | class Viola : Cuerdas · recibe todo lo de la base · public Viola() : base("viola") { }
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Don Cedro termina una viola: un poco más grande que el violín, un poco más grave. Ceci tiene que escribir su plano sin repetir nada.

#### Gheco sugiere
Una clase hereda con `:`, y su constructor le pasa a la base lo que pide con `: base(…)`:

```csharp
class Bombo : Tambor
{
    public Bombo() : base("bombo") { }
}
```

#### Desafío
Escribí la clase `Viola`, que herede de `Cuerdas` y le pase `viola` como nombre.

#### Código inicial
```csharp
Viola v = new Viola();
Console.WriteLine($"{v.Nombre}, {v.CantidadCuerdas} cuerdas");

class Cuerdas
{
    public string Nombre { get; }
    public int CantidadCuerdas { get; } = 4;

    public Cuerdas(string nombre)
    {
        Nombre = nombre;
    }
}

// la clase Viola
```

#### Salida esperada
```
viola, 4 cuerdas
```

#### Solución
```csharp
Viola v = new Viola();
Console.WriteLine($"{v.Nombre}, {v.CantidadCuerdas} cuerdas");

class Cuerdas
{
    public string Nombre { get; }
    public int CantidadCuerdas { get; } = 4;

    public Cuerdas(string nombre)
    {
        Nombre = nombre;
    }
}

class Viola : Cuerdas
{
    public Viola() : base("viola") { }
}
```

#### Al superarla
—Tres líneas —dice Don Cedro—. Y ya tiene cuerdas, nombre y todo lo de la familia.

#### Imagen
- Un violín, una viola y un chelo de madera parados uno al lado del otro, de menor a mayor, en un taller, sin letras.
- Don Cedro apoya la mano en la viola como quien presenta a una hija; Ceci la mira con admiración.

### Micro-misión R02-N07-P2 · Lo que solo sabe el chelo

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Bemol
carta: Agregar en la derivada | la derivada suma métodos propios · la base no los tiene
recompensa: xp 15, oro 15
```

#### Escena
—El chelo hace algo que el violín no —dice Bemol—: se toca sentado y se apoya en el piso.

#### Gheco sugiere
La derivada puede agregar métodos que la base no tiene:

```csharp
class Bombo : Tambor
{
    public Bombo() : base("bombo") { }

    public void Retumbar()
    {
        Console.WriteLine("¡BUM!");
    }
}
```

#### Desafío
Agregale a `Chelo` el método `Apoyar()`, que muestre `<Nombre> se apoya en el piso`.

#### Código inicial
```csharp
Chelo c = new Chelo();
c.Apoyar();

class Cuerdas
{
    public string Nombre { get; }

    public Cuerdas(string nombre)
    {
        Nombre = nombre;
    }
}

class Chelo : Cuerdas
{
    public Chelo() : base("chelo") { }

    // Apoyar
}
```

#### Salida esperada
```
chelo se apoya en el piso
```

#### Solución
```csharp
Chelo c = new Chelo();
c.Apoyar();

class Cuerdas
{
    public string Nombre { get; }

    public Cuerdas(string nombre)
    {
        Nombre = nombre;
    }
}

class Chelo : Cuerdas
{
    public Chelo() : base("chelo") { }

    public void Apoyar()
    {
        Console.WriteLine($"{Nombre} se apoya en el piso");
    }
}
```

#### Al superarla
Bemol se sienta y prueba el chelo. Le queda grande, pero la nota sale profunda y redonda.

#### Imagen
- Un chelo de madera apoyado en el piso de un taller, con su pica clavada en una tabla, sin letras.
- Bemol sentado en una banqueta abrazando el chelo, que le queda enorme; Ceci se ríe.

### Micro-misión R02-N07-P3 · Cada uno con su voz

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: virtual y override | la base: public virtual string Voz() · la derivada: public override string Voz()
recompensa: xp 15, oro 15
```

#### Escena
Todos los instrumentos de la familia dicen que su voz es «media». Don Cedro se tapa los oídos: el contrabajo, por lo menos, tiene que ser **muy grave**.

#### Gheco sugiere
La base marca con `virtual` lo que se puede cambiar, y la derivada lo reemplaza con `override`:

```csharp
class Tambor
{
    public virtual string Golpe() => "pum";
}

class Bombo : Tambor
{
    public override string Golpe() => "BUM";
}
```

#### Desafío
Hacé que `Contrabajo` reemplace `Voz()` para que devuelva `muy grave`.

#### Código inicial
```csharp
Cuerdas c = new Contrabajo();
Console.WriteLine($"{c.Nombre}: {c.Voz()}");

class Cuerdas
{
    public string Nombre { get; }

    public Cuerdas(string nombre)
    {
        Nombre = nombre;
    }

    public virtual string Voz() => "media";
}

class Contrabajo : Cuerdas
{
    public Contrabajo() : base("contrabajo") { }
}
```

#### Salida esperada
```
contrabajo: muy grave
```

#### Solución
```csharp
Cuerdas c = new Contrabajo();
Console.WriteLine($"{c.Nombre}: {c.Voz()}");

class Cuerdas
{
    public string Nombre { get; }

    public Cuerdas(string nombre)
    {
        Nombre = nombre;
    }

    public virtual string Voz() => "media";
}

class Contrabajo : Cuerdas
{
    public Contrabajo() : base("contrabajo") { }

    public override string Voz() => "muy grave";
}
```

#### Al superarla
El contrabajo suena tan grave que tiemblan las herramientas colgadas en la pared. Don Cedro sonríe: —Eso. Esa es su voz.

#### Imagen
- Un contrabajo enorme de madera oscura en un taller, con ondas de sonido que hacen temblar las herramientas colgadas de la pared, sin letras.
- Don Cedro, al lado, le llega apenas a la mitad del instrumento; Ceci se tapa una oreja riéndose.

### Micro-misión R02-N07-P4 · Lo que guarda la familia

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Clave
carta: protected | lo ven la base y sus derivadas · los de afuera, no
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Cada instrumento guarda un secreto de afinación que solo conoce la familia. Clave quiere que el violín lo pueda usar, pero que nadie de afuera lo vea.

#### Gheco sugiere
Lo `private` no lo ve ni la derivada. Para que la derivada lo use, va `protected`:

```csharp
class Tambor
{
    protected int tension = 3;
}

class Bombo : Tambor
{
    public int Doble() => tension * 2;   // la derivada lo ve
}
```

#### Desafío
El violín no puede usar `afinacion` porque es `private`. Cambialo a `protected`.

#### Código inicial
```csharp
Violin v = new Violin();
Console.WriteLine(v.Secreto());

class Cuerdas
{
    private int afinacion = 440;
}

class Violin : Cuerdas
{
    public string Secreto() => $"El La vibra {afinacion} veces por segundo";
}
```

#### Salida esperada
```
El La vibra 440 veces por segundo
```

#### Solución
```csharp
Violin v = new Violin();
Console.WriteLine(v.Secreto());

class Cuerdas
{
    protected int afinacion = 440;
}

class Violin : Cuerdas
{
    public string Secreto() => $"El La vibra {afinacion} veces por segundo";
}
```

#### Al superarla
—Cuatrocientas cuarenta veces por segundo —dice Clave—. Todos los instrumentos de la orquesta afinan con ese La. Es el secreto mejor guardado de la familia.

#### Imagen
- Un diapasón de acero vibrando sobre una mesa, con ondas de sonido suaves que llegan a un violín, una viola y un chelo alineados, sin letras.
- Clave sostiene el diapasón; Ceci se acerca para escuchar.

### Micro-misión R02-N07-P5 · El ogro del override olvidado

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Gheco
criatura: ogro
carta: Ogro | compila pero suena la versión equivocada · ¿la base dice virtual? ¿la derivada dice override?
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un ogro tocó el plano: ahora el violín dice que su voz es «media», como todos. No hay error: el programa corre, pero suena mal.

#### Gheco sugiere
Si la derivada escribe el método **sin `override`**, no reemplaza al de la base: cuando el objeto se usa como `Cuerdas`, suena la versión de la base. El compilador solo deja un aviso.

Para que la derivada reemplace de verdad, la base dice `virtual` y la derivada, `override`.

#### Desafío
Arreglá el plano para que el violín diga que su voz es `aguda`.

#### Código inicial
```csharp
Cuerdas v = new Violin();
Console.WriteLine($"Voz: {v.Voz()}");

class Cuerdas
{
    public string Voz() => "media";
}

class Violin : Cuerdas
{
    public new string Voz() => "aguda";
}
```

#### Salida esperada
```
Voz: aguda
```

#### Solución
```csharp
Cuerdas v = new Violin();
Console.WriteLine($"Voz: {v.Voz()}");

class Cuerdas
{
    public virtual string Voz() => "media";
}

class Violin : Cuerdas
{
    public override string Voz() => "aguda";
}
```

#### Al superarla
El violín vuelve a sonar agudo y claro. El ogro, que había tocado la nota equivocada con toda la seguridad del mundo, se rasca la cabeza y se va.

#### Imagen
- Un ogro grandote y simpático de piel gris azulada y pelo naranja, rascándose la cabeza confundido mientras sale por la puerta de un taller de madera.
- Gheco, en el hombro de Ceci, lo saluda con la patita.

### Encargo R02-N07-E1 · Los puestos de Doña Mirta

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Doña Mirta tiene varios puestos en la Feria. Escribí una clase base `Puesto` con `Nombre` (que recibe el constructor) y un método `virtual` `Precio()` que devuelve `100`. Después, dos derivadas:

- `PanConMiel`, con nombre `pan con miel`, que reemplace `Precio()` por `150`.
- `Limonada`, con nombre `limonada`, que use el precio de la base **más** `20` (con `base.Precio()`).

Mostrá los dos:

```
pan con miel: 150
limonada: 120
```

#### Criterio de aprobación

- Las dos clases heredan de `Puesto` y le pasan el nombre con `base(…)`.
- `Limonada` usa `base.Precio()`, sin escribir el `100` de nuevo.

#### Salida esperada

```
pan con miel: 150
limonada: 120
```

#### Solución de referencia

```csharp
Puesto[] puestos = { new PanConMiel(), new Limonada() };
foreach (Puesto p in puestos)
{
    Console.WriteLine($"{p.Nombre}: {p.Precio()}");
}

class Puesto
{
    public string Nombre { get; }

    public Puesto(string nombre)
    {
        Nombre = nombre;
    }

    public virtual int Precio() => 100;
}

class PanConMiel : Puesto
{
    public PanConMiel() : base("pan con miel") { }

    public override int Precio() => 150;
}

class Limonada : Puesto
{
    public Limonada() : base("limonada") { }

    public override int Precio() => base.Precio() + 20;
}
```

## R02-N08 · Polimorfismo: la orquesta entera

```meta
tipo: tema
padre: R02-N07
precio: 10
criatura: ogro
temas: poo.polimorfismo, poo.abstractas
usa: poo.herencia, col.arrays
```

### Crónica

Es el primer ensayo de la orquesta del Taller: un violín, una viola, un chelo y un tambor. Clave levanta la batuta y dice una sola palabra: «**Toquen**». Cada uno toca a su manera, y suena una sola música.

—Eso es el **polimorfismo** —dice {mentor}—: una sola orden, y cada objeto responde con su propia versión. Yo no le digo al chelo cómo tocar. Le digo «tocá», y él sabe.

### Objetivos

- Guardar objetos de distintas derivadas en un arreglo de la base.
- Llamar a un método y que cada objeto use su versión.
- Escribir una clase `abstract` que obliga a las derivadas a completar un método.
- Preguntar el tipo real con `is`.

### Antes de empezar

- Herencia (R02-N07).

### Explicación

#### Una orden, muchas respuestas

Una variable de la base puede guardar cualquier derivada. Al llamar a un método `virtual`, se usa la versión del **objeto real**:

```csharp
Instrumento[] orquesta = { new Violin(), new Chelo(), new Tambor() };
foreach (Instrumento i in orquesta)
{
    Console.WriteLine(i.Tocar());   // cada uno, su versión
}
```

Lo mejor: si mañana llega una `Flauta`, ese bucle **no cambia ni una línea**.

#### `abstract`: el plano incompleto

Una clase `abstract` es un molde a medio hacer: no se pueden crear objetos de ella, y sus métodos `abstract` **no tienen cuerpo**. Cada derivada **tiene que** escribirlos:

```csharp
abstract class Instrumento
{
    public abstract string Tocar();      // sin cuerpo: lo completa cada uno
}

class Tambor : Instrumento
{
    public override string Tocar() => "pum pum";
}
```

`virtual` dice «podés cambiarlo»; `abstract` dice «**tenés que** escribirlo».

#### Preguntar el tipo real: `is`

```csharp
if (i is Chelo chelo)
{
    chelo.Apoyar();      // adentro, chelo ya es un Chelo
}
```

Si te encontrás con muchos `is` seguidos, casi siempre falta un método `virtual`.

### Código de ejemplo

```csharp
Instrumento[] orquesta = { new Violin(), new Chelo(), new Tambor() };

foreach (Instrumento i in orquesta)
{
    Console.WriteLine($"{i.Nombre}: {i.Tocar()}");
}

foreach (Instrumento i in orquesta)
{
    if (i is Chelo chelo) chelo.Apoyar();
}

abstract class Instrumento
{
    public string Nombre { get; }

    protected Instrumento(string nombre)
    {
        Nombre = nombre;
    }

    public abstract string Tocar();
}

class Violin : Instrumento
{
    public Violin() : base("violín") { }
    public override string Tocar() => "la la la";
}

class Chelo : Instrumento
{
    public Chelo() : base("chelo") { }
    public override string Tocar() => "mmm mmm";
    public void Apoyar() => Console.WriteLine("El chelo se apoya en el piso");
}

class Tambor : Instrumento
{
    public Tambor() : base("tambor") { }
    public override string Tocar() => "pum pum";
}
```

### Salida esperada

```
violín: la la la
chelo: mmm mmm
tambor: pum pum
El chelo se apoya en el piso
```

### ¿Para qué sirve?

Es lo que hace que un programa grande se pueda agrandar sin romperse. Un juego recorre «todos los enemigos» y les dice «atacá»; una tienda recorre «todos los productos» y les pide «tu precio». Agregar un enemigo o un producto nuevo es escribir una clase, no tocar mil `if`.

### Errores habituales

- **Hacer `new` de una clase `abstract`:** no se puede, es un plano incompleto (`CS0144`).
- **No completar un método `abstract`:** la derivada no compila hasta que lo escribe (`CS0534`).
- **Llenar el programa de `if (x is …)`:** es el **ogro** del polimorfismo. Si todos tienen que hacer algo distinto, que cada uno lo haga en su `override`.

### Micro-misión R02-N08-P1 · ¡Toquen!

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave, Bemol
carta: Polimorfismo | Instrumento[] orquesta = { … } · foreach: i.Tocar() · cada uno, su versión
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Clave levanta la batuta. La orquesta está lista en el arreglo; falta el bucle que les diga «toquen».

#### Gheco sugiere
Recorré el arreglo de la base y llamá al método: cada objeto usa su propia versión.

```csharp
foreach (Tambor t in banda)
{
    Console.WriteLine(t.Golpe());
}
```

#### Desafío
Recorré la orquesta y mostrá lo que toca cada instrumento.

#### Código inicial
```csharp
Instrumento[] orquesta = { new Violin(), new Tambor() };

// ¡toquen!

class Instrumento
{
    public virtual string Tocar() => "...";
}

class Violin : Instrumento
{
    public override string Tocar() => "la la la";
}

class Tambor : Instrumento
{
    public override string Tocar() => "pum pum";
}
```

#### Salida esperada
```
la la la
pum pum
```

#### Solución
```csharp
Instrumento[] orquesta = { new Violin(), new Tambor() };

foreach (Instrumento i in orquesta)
{
    Console.WriteLine(i.Tocar());
}

class Instrumento
{
    public virtual string Tocar() => "...";
}

class Violin : Instrumento
{
    public override string Tocar() => "la la la";
}

class Tambor : Instrumento
{
    public override string Tocar() => "pum pum";
}
```

#### Al superarla
El violín de Ceci y el tambor de Bemol suenan juntos por primera vez. Clave baja la batuta y, por un segundo, cierra los ojos.

#### Imagen
- Una sala de ensayo gótica iluminada con velas, con notas doradas y círculos de sonido saliendo de un violín y de un tambor a la vez, sin letras.
- Clave dirige con la batuta en alto; Ceci toca el violín y Bemol el tambor.

### Micro-misión R02-N08-P2 · Llega la flauta

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Agrandar sin tocar el bucle | una clase nueva que hereda · se suma al arreglo · el foreach no cambia
recompensa: xp 15, oro 15
```

#### Escena
Una alumna nueva llega con una flauta. Clave no toca el bucle de la orquesta: solo pide que la flauta tenga su clase.

#### Gheco sugiere
Para sumar un instrumento, alcanza con una clase nueva que herede y escriba su versión. El bucle sigue igual:

```csharp
class Bombo : Instrumento
{
    public override string Tocar() => "BUM";
}
```

#### Desafío
Escribí la clase `Flauta`, que toque `fiu fiu`. El arreglo ya la incluye.

#### Código inicial
```csharp
Instrumento[] orquesta = { new Violin(), new Flauta() };

foreach (Instrumento i in orquesta)
{
    Console.WriteLine(i.Tocar());
}

class Instrumento
{
    public virtual string Tocar() => "...";
}

class Violin : Instrumento
{
    public override string Tocar() => "la la la";
}

// la Flauta
```

#### Salida esperada
```
la la la
fiu fiu
```

#### Solución
```csharp
Instrumento[] orquesta = { new Violin(), new Flauta() };

foreach (Instrumento i in orquesta)
{
    Console.WriteLine(i.Tocar());
}

class Instrumento
{
    public virtual string Tocar() => "...";
}

class Violin : Instrumento
{
    public override string Tocar() => "la la la";
}

class Flauta : Instrumento
{
    public override string Tocar() => "fiu fiu";
}
```

#### Al superarla
—¿Ves? —dice Clave—. No toqué el bucle. La orquesta creció y nadie tuvo que aprender nada nuevo, salvo la flauta.

#### Imagen
- Una flauta traversa plateada brillando sobre un atril de madera, con notitas doradas saliendo de ella, en una sala de piedra con velas, sin letras.
- Clave asiente; Ceci aplaude con el arco en la mano.

### Micro-misión R02-N08-P3 · El plano incompleto

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: abstract | abstract class Instrumento · public abstract string Tocar(); · sin cuerpo · cada uno tiene que escribirlo
recompensa: xp 15, oro 15
```

#### Escena
Don Cedro se niega a fabricar «un instrumento» así, en general. —¿Qué instrumento? Un instrumento en general no existe. Existe un violín, un tambor.

#### Gheco sugiere
Una clase `abstract` no se puede crear con `new`, y su método `abstract` no tiene cuerpo: obliga a cada derivada a escribirlo.

```csharp
abstract class Forma
{
    public abstract int Lados();
}
```

#### Desafío
Al tambor le falta su `Tocar()` y nadie se dio cuenta: suena `...`. Convertí `Instrumento` en `abstract` y su `Tocar()` en un método `abstract`, sin cuerpo. Ensayá: el compilador te va a avisar que el tambor no lo escribió (`CS0534`). Escribiselo, que toque `pum pum`.

#### Código inicial
```csharp
Instrumento t = new Tambor();
Console.WriteLine(t.Tocar());

class Instrumento
{
    public virtual string Tocar() => "...";
}

class Tambor : Instrumento
{
}
```

#### Salida esperada
```
pum pum
```

#### Solución
```csharp
Instrumento t = new Tambor();
Console.WriteLine(t.Tocar());

abstract class Instrumento
{
    public abstract string Tocar();
}

class Tambor : Instrumento
{
    public override string Tocar() => "pum pum";
}
```

#### Al superarla
—Así —dice Don Cedro—. Ahora nadie se olvida de su parte. «Instrumento» es una idea. Lo que se fabrica es un tambor.

#### Imagen
- Un plano de instrumento a medio dibujar clavado en la pared, con un contorno vacío en el medio, y al lado un tambor terminado, sin letras.
- Don Cedro señala el contorno vacío con el lápiz; Ceci entiende.

### Micro-misión R02-N08-P4 · ¿Sos un chelo?

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: is | if (i is Chelo c) { c.Apoyar(); } · pregunta el tipo real · adentro ya es un Chelo
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Antes de empezar, Bemol tiene que acomodar los chelos: solo ellos se apoyan en el piso.

#### Gheco sugiere
`is` pregunta si un objeto es de cierta clase. Si lo es, le pone un nombre para usarlo como tal:

```csharp
if (t is Bombo b)
{
    b.Retumbar();
}
```

#### Desafío
Recorré la orquesta y, si el instrumento es un `Chelo`, llamá a `Apoyar()`.

#### Código inicial
```csharp
Instrumento[] orquesta = { new Violin(), new Chelo(), new Violin() };

// acomodá los chelos

class Instrumento { }

class Violin : Instrumento { }

class Chelo : Instrumento
{
    public void Apoyar() => Console.WriteLine("Chelo apoyado");
}
```

#### Salida esperada
```
Chelo apoyado
```

#### Solución
```csharp
Instrumento[] orquesta = { new Violin(), new Chelo(), new Violin() };

foreach (Instrumento i in orquesta)
{
    if (i is Chelo c) c.Apoyar();
}

class Instrumento { }

class Violin : Instrumento { }

class Chelo : Instrumento
{
    public void Apoyar() => Console.WriteLine("Chelo apoyado");
}
```

#### Al superarla
Bemol encuentra el único chelo entre los violines y lo apoya con cuidado. —Listo. Uno solo, pero pesado.

#### Imagen
- Una fila de sillas de ensayo con dos violines apoyados en dos sillas y un chelo parado en el medio, en una sala de piedra con velas, sin letras.
- Bemol apoya el chelo en el piso con esfuerzo; Ceci le alcanza el arco.

### Micro-misión R02-N08-P5 · El ogro de los mil if

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Bemol, Gheco
criatura: ogro
carta: Ogro | muchos if (x is …) para elegir qué hacer · mejor: cada clase con su override
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un ogro escribió el ensayo a su manera: un método enorme con un `if` para cada instrumento. Y se olvidó del tambor, que se quedó mudo.

#### Gheco sugiere
Si cada clase tiene que hacer algo distinto, que lo haga **ella**, en su `override`. Así nadie se olvida de nadie: la clase base lo pide con `abstract`.

```csharp
abstract class Instrumento
{
    public abstract string Tocar();
}
```

#### Desafío
Sacá el método del ogro y reemplazalo por un `Tocar()` en cada clase. El tambor toca `pum pum`.

#### Código inicial
```csharp
Instrumento[] orquesta = { new Violin(), new Tambor() };
foreach (Instrumento i in orquesta)
{
    Console.WriteLine(TocarComoOgro(i));
}

static string TocarComoOgro(Instrumento i)
{
    if (i is Violin) return "la la la";
    return "...";
}

class Instrumento { }

class Violin : Instrumento { }

class Tambor : Instrumento { }
```

#### Salida esperada
```
la la la
pum pum
```

#### Solución
```csharp
Instrumento[] orquesta = { new Violin(), new Tambor() };
foreach (Instrumento i in orquesta)
{
    Console.WriteLine(i.Tocar());
}

abstract class Instrumento
{
    public abstract string Tocar();
}

class Violin : Instrumento
{
    public override string Tocar() => "la la la";
}

class Tambor : Instrumento
{
    public override string Tocar() => "pum pum";
}
```

#### Al superarla
El tambor recupera la voz. El ogro mira su método enorme, ahora borrado, y se va con cara de no entender por qué era tan complicado.

#### Imagen
- Un ogro grandote y simpático de piel gris azulada y pelo naranja, con un rollo de papel larguísimo arrastrándose detrás, saliendo de un taller, sin letras en el papel.
- Bemol toca el tambor feliz; Gheco, sobre el tambor, salta con cada golpe.

### Encargo R02-N08-E1 · Los sueldos del Gremio

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

El Gremio paga a sus trabajadores de dos formas. Escribí una clase `abstract` `Empleado` con `Nombre` y un método `abstract` `int Sueldo()`, y dos derivadas:

- `Fijo`, que recibe un sueldo mensual y lo devuelve.
- `PorHora`, que recibe horas y valor por hora, y devuelve `horas * valor`.

Con un arreglo de `Empleado`, mostrá la lista y el total:

```
Ámbar: 90000
Fermín: 48000
Tati: 30000
Total: 168000
```

(Ámbar es fija con `90000`; Fermín trabaja `40` horas a `1200`; Tati, `25` horas a `1200`.)

#### Criterio de aprobación

- `Empleado` es `abstract` y cada derivada escribe su `Sueldo()`.
- El total se calcula recorriendo el arreglo, sin preguntar el tipo de cada uno.

#### Salida esperada

```
Ámbar: 90000
Fermín: 48000
Tati: 30000
Total: 168000
```

#### Solución de referencia

```csharp
Empleado[] nomina = { new Fijo("Ámbar", 90000), new PorHora("Fermín", 40, 1200), new PorHora("Tati", 25, 1200) };
int total = 0;
foreach (Empleado e in nomina)
{
    Console.WriteLine($"{e.Nombre}: {e.Sueldo()}");
    total += e.Sueldo();
}
Console.WriteLine($"Total: {total}");

abstract class Empleado
{
    public string Nombre { get; }

    protected Empleado(string nombre)
    {
        Nombre = nombre;
    }

    public abstract int Sueldo();
}

class Fijo : Empleado
{
    private readonly int _mensual;

    public Fijo(string nombre, int mensual) : base(nombre)
    {
        _mensual = mensual;
    }

    public override int Sueldo() => _mensual;
}

class PorHora : Empleado
{
    private readonly int _horas;
    private readonly int _valor;

    public PorHora(string nombre, int horas, int valor) : base(nombre)
    {
        _horas = horas;
        _valor = valor;
    }

    public override int Sueldo() => _horas * _valor;
}
```

## R02-N09 · Interfaces: lo que sabés hacer

```meta
tipo: tema
padre: R02-N08
precio: 10
criatura: goblin
temas: poo.interfaces
usa: poo.polimorfismo
```

### Crónica

Para el concierto hace falta alguien que marque el compás. Puede ser el metrónomo de Don Cedro, Bemol con su tambor o el péndulo de la torre. No son de la misma familia: uno es de madera, otro es un chico y otro es una torre.

—No me importa **qué son** —dice {mentor}—. Me importa que **sepan marcar el compás**. Eso es una **interface**: una promesa. «Yo sé hacer esto.» Cualquiera que la cumpla, me sirve.

### Objetivos

- Escribir una `interface` con lo que hay que saber hacer.
- Hacer que clases sin relación entre sí la **implementen**.
- Escribir métodos que pidan la interface, no una clase.
- Distinguir cuándo conviene una interface y cuándo una clase base.

### Antes de empezar

- Polimorfismo y clases abstractas (R02-N08).

### Explicación

#### Una promesa

```csharp
interface IMarcaCompas
{
    void Marcar();
}
```

- Por costumbre, el nombre empieza con **`I`**.
- No tiene datos ni código: solo dice **qué** hay que saber hacer.
- No se puede hacer `new` de una interface.

#### Cumplir la promesa

Una clase **implementa** la interface con `:` y escribe todo lo que pide, con `public`:

```csharp
class Metronomo : IMarcaCompas
{
    public void Marcar() => Console.WriteLine("tic tac");
}

class Tamborilero : IMarcaCompas
{
    public void Marcar() => Console.WriteLine("pum pum");
}
```

Una clase puede cumplir **varias** interfaces: `class Bemol : IMarcaCompas, ICanta`.

#### Pedir la promesa, no la clase

```csharp
static void Ensayar(IMarcaCompas quien)
{
    quien.Marcar();
}
```

`Ensayar` sirve con un metrónomo, con Bemol o con algo que se invente el año que viene.

#### ¿Interface o clase abstracta?

| | `interface` | `abstract class` |
|---|---|---|
| Cuántas puede tener una clase | **muchas** | **una** |
| Guarda datos | no | sí |
| Dice | «**sabe hacer**» | «**es un**» |

Ante la duda, empezá con una interface.

### Código de ejemplo

```csharp
IMarcaCompas[] marcadores = { new Metronomo(), new Tamborilero(), new Pendulo() };
foreach (IMarcaCompas m in marcadores)
{
    Ensayar(m);
}

static void Ensayar(IMarcaCompas quien)
{
    quien.Marcar();
}

interface IMarcaCompas
{
    void Marcar();
}

class Metronomo : IMarcaCompas
{
    public void Marcar() => Console.WriteLine("tic tac");
}

class Tamborilero : IMarcaCompas
{
    public void Marcar() => Console.WriteLine("pum pum");
}

class Pendulo : IMarcaCompas
{
    public void Marcar() => Console.WriteLine("bong");
}
```

### Salida esperada

```
tic tac
pum pum
bong
```

### ¿Para qué sirve?

Las interfaces están en todo C#: `IComparable` (sé compararme), `IDisposable` (tengo algo que cerrar), `IEnumerable` (se me puede recorrer). Los servicios de internet, los tests y casi todas las bibliotecas trabajan con interfaces: piden lo que necesitan saber hacer, no quién sos.

### Errores habituales

- **No escribir todo lo que pide:** si la interface pide `Marcar()` y la clase no lo tiene, el **goblin** de `CS0535` no te deja compilar.
- **Olvidar el `public`:** lo que cumple una interface tiene que ser público.
- **Querer guardar datos en la interface:** la interface promete acciones; los datos van en las clases.

### Micro-misión R02-N09-P1 · La promesa del compás

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: interface | interface IMarcaCompas { void Marcar(); } · solo dice qué · el nombre empieza con I
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Clave escribe en el pizarrón lo único que le pide a quien marque el compás. Ceci tiene que pasarlo al código.

#### Gheco sugiere
Una interface se escribe al final, como las clases, y solo lista lo que hay que saber hacer, sin cuerpo:

```csharp
interface ISaluda
{
    void Saludar();
}
```

#### Desafío
Escribí la interface `IMarcaCompas` con el método `void Marcar();`. El metrónomo ya la cumple.

#### Código inicial
```csharp
IMarcaCompas m = new Metronomo();
m.Marcar();

// la interface

class Metronomo : IMarcaCompas
{
    public void Marcar() => Console.WriteLine("tic tac");
}
```

#### Salida esperada
```
tic tac
```

#### Solución
```csharp
IMarcaCompas m = new Metronomo();
m.Marcar();

interface IMarcaCompas
{
    void Marcar();
}

class Metronomo : IMarcaCompas
{
    public void Marcar() => Console.WriteLine("tic tac");
}
```

#### Al superarla
El metrónomo empieza a oscilar: tic, tac, tic, tac. Clave borra el pizarrón. —Una promesa chica. Pero el que la cumple, entra a la orquesta.

#### Imagen
- Un metrónomo de madera con forma de pirámide oscilando sobre un piano, en una sala de piedra iluminada con velas, sin letras.
- Clave, con la tiza todavía en la mano, mira el metrónomo; Ceci lleva el ritmo con el pie.

### Micro-misión R02-N09-P2 · Bemol también marca

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Implementar | class Tamborilero : IMarcaCompas · escribe todo lo que pide, con public
recompensa: xp 15, oro 15
```

#### Escena
—Yo también sé marcar el compás —dice Bemol, ofendido—. Con el tambor, y mejor que el metrónomo.

#### Gheco sugiere
Una clase cumple la interface con `:` y escribe lo que pide, con `public`:

```csharp
class Loro : ISaluda
{
    public void Saludar() => Console.WriteLine("¡Hola!");
}
```

#### Desafío
Escribí la clase `Tamborilero`, que cumpla `IMarcaCompas` y marque `pum pum`.

#### Código inicial
```csharp
IMarcaCompas[] marcadores = { new Metronomo(), new Tamborilero() };
foreach (IMarcaCompas m in marcadores)
{
    m.Marcar();
}

interface IMarcaCompas
{
    void Marcar();
}

class Metronomo : IMarcaCompas
{
    public void Marcar() => Console.WriteLine("tic tac");
}

// el Tamborilero
```

#### Salida esperada
```
tic tac
pum pum
```

#### Solución
```csharp
IMarcaCompas[] marcadores = { new Metronomo(), new Tamborilero() };
foreach (IMarcaCompas m in marcadores)
{
    m.Marcar();
}

interface IMarcaCompas
{
    void Marcar();
}

class Metronomo : IMarcaCompas
{
    public void Marcar() => Console.WriteLine("tic tac");
}

class Tamborilero : IMarcaCompas
{
    public void Marcar() => Console.WriteLine("pum pum");
}
```

#### Al superarla
Bemol y el metrónomo marcan juntos. Van perfectos… durante tres compases. Después Bemol entra medio tiempo tarde, como siempre.

#### Imagen
- Un metrónomo de madera oscilando y un tambor chico con sus palillos, uno al lado del otro sobre el piso de una sala de ensayo, sin letras.
- Bemol toca el tambor muy concentrado; Ceci se tapa la boca para no reírse.

### Micro-misión R02-N09-P3 · El ensayo para cualquiera

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Pedir la interface | static void Ensayar(IMarcaCompas quien) · sirve con cualquiera que la cumpla
recompensa: xp 15, oro 15
```

#### Escena
Clave quiere un solo método de ensayo que sirva para cualquiera que marque el compás, sin importar quién sea.

#### Gheco sugiere
Un método puede pedir una **interface** como parámetro: le podés pasar cualquier objeto que la cumpla.

```csharp
static void Presentar(ISaluda alguien)
{
    alguien.Saludar();
}
```

#### Desafío
Completá `Ensayar` para que llame a `Marcar()` dos veces sobre lo que recibe.

#### Código inicial
```csharp
Ensayar(new Metronomo());
Ensayar(new Pendulo());

static void Ensayar(IMarcaCompas quien)
{
    // dos compases
}

interface IMarcaCompas
{
    void Marcar();
}

class Metronomo : IMarcaCompas
{
    public void Marcar() => Console.WriteLine("tic tac");
}

class Pendulo : IMarcaCompas
{
    public void Marcar() => Console.WriteLine("bong");
}
```

#### Salida esperada
```
tic tac
tic tac
bong
bong
```

#### Solución
```csharp
Ensayar(new Metronomo());
Ensayar(new Pendulo());

static void Ensayar(IMarcaCompas quien)
{
    quien.Marcar();
    quien.Marcar();
}

interface IMarcaCompas
{
    void Marcar();
}

class Metronomo : IMarcaCompas
{
    public void Marcar() => Console.WriteLine("tic tac");
}

class Pendulo : IMarcaCompas
{
    public void Marcar() => Console.WriteLine("bong");
}
```

#### Al superarla
El péndulo de la torre suena tan fuerte que se oye en todo el Conservatorio: bong, bong. Clave ni se inmuta. —Sirve. Cualquiera que marque, sirve.

#### Imagen
- Una torre de piedra alta con un péndulo gigante de bronce oscilando adentro, con ondas de sonido que salen por las ventanas, de noche, sin letras.
- Clave y Ceci miran hacia arriba desde el patio.

### Micro-misión R02-N09-P4 · Dos promesas a la vez

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Varias interfaces | class Bemol : IMarcaCompas, ICanta · cumple las dos · una clase, muchas promesas
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol no solo marca el compás: también canta (mal, pero canta). Clave quiere que el programa lo sepa.

#### Gheco sugiere
Una clase puede cumplir varias interfaces, separadas con coma, y escribir lo que pide cada una:

```csharp
class Loro : ISaluda, IVuela
{
    public void Saludar() => Console.WriteLine("¡Hola!");
    public void Volar() => Console.WriteLine("flap");
}
```

#### Desafío
Hacé que `Tamborilero` cumpla también `ICanta`, cantando `la la la`.

#### Código inicial
```csharp
Tamborilero bemol = new Tamborilero();
bemol.Marcar();
bemol.Cantar();

interface IMarcaCompas
{
    void Marcar();
}

interface ICanta
{
    void Cantar();
}

class Tamborilero : IMarcaCompas
{
    public void Marcar() => Console.WriteLine("pum pum");
}
```

#### Salida esperada
```
pum pum
la la la
```

#### Solución
```csharp
Tamborilero bemol = new Tamborilero();
bemol.Marcar();
bemol.Cantar();

interface IMarcaCompas
{
    void Marcar();
}

interface ICanta
{
    void Cantar();
}

class Tamborilero : IMarcaCompas, ICanta
{
    public void Marcar() => Console.WriteLine("pum pum");
    public void Cantar() => Console.WriteLine("la la la");
}
```

#### Al superarla
Bemol toca y canta a la vez. Desafina un poco en el «la» del medio, pero nadie se lo dice.

#### Imagen
- Notas musicales doradas que salen de un tambor chico y de una boca abierta al mismo tiempo, en una sala de piedra con velas, sin letras.
- Bemol toca el tambor y canta con los ojos cerrados; Ceci aguanta la risa.

### Micro-misión R02-N09-P5 · El goblin de la promesa rota

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
criatura: goblin
carta: Goblin | CS0535: no implementa el miembro de interfaz · falta escribir lo que pide · con public
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un goblin dijo que sabía marcar el compás, firmó la promesa… y no escribió cómo. El compilador lo pescó.

#### Gheco sugiere
Si una clase dice que cumple una interface, tiene que escribir **todo** lo que pide:

```
error CS0535: "Goblin" no implementa el miembro de interfaz "IMarcaCompas.Marcar()"
```

#### Desafío
Ensayá, leé el error y escribile al `Goblin` su `Marcar()`, que muestre `tac… tac…`.

#### Código inicial
```csharp
IMarcaCompas g = new Goblin();
g.Marcar();

interface IMarcaCompas
{
    void Marcar();
}

class Goblin : IMarcaCompas
{
}
```

#### Salida esperada
```
tac… tac…
```

#### Solución
```csharp
IMarcaCompas g = new Goblin();
g.Marcar();

interface IMarcaCompas
{
    void Marcar();
}

class Goblin : IMarcaCompas
{
    public void Marcar() => Console.WriteLine("tac… tac…");
}
```

#### Al superarla
El goblin marca el compás, lento y desganado, pero lo marca. Una promesa es una promesa.

#### Imagen
- Un goblin chico de orejas puntiagudas sentado en un taburete golpeando el piso con un palito, con cara de aburrido, en una sala de ensayo.
- Gheco, al lado, marca el ritmo con la cola, mucho más animado.

### Encargo R02-N09-E1 · Las notificaciones del Puerto

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Elefa quiere avisarle a cada cliente cuando su pedido sale. Escribí una interface `INotificador` con `void Enviar(string mensaje)`, y dos clases que la cumplan:

- `Paloma`, que muestre `Paloma lleva: <mensaje>`.
- `Farol`, que muestre `Farol señala: <mensaje>`.

Después, una clase `Pedido` que reciba un `INotificador` en el constructor, y un método `Confirmar(string cliente)` que lo use para avisar `Salió el pedido de <cliente>`. Confirmá un pedido de `Nilo` con paloma y uno de `Nima` con farol:

```
Paloma lleva: Salió el pedido de Nilo
Farol señala: Salió el pedido de Nima
```

#### Criterio de aprobación

- `Pedido` recibe un `INotificador`, no una clase concreta.
- Para cambiar de paloma a farol no se toca la clase `Pedido`.

#### Salida esperada

```
Paloma lleva: Salió el pedido de Nilo
Farol señala: Salió el pedido de Nima
```

#### Solución de referencia

```csharp
new Pedido(new Paloma()).Confirmar("Nilo");
new Pedido(new Farol()).Confirmar("Nima");

interface INotificador
{
    void Enviar(string mensaje);
}

class Paloma : INotificador
{
    public void Enviar(string mensaje) => Console.WriteLine($"Paloma lleva: {mensaje}");
}

class Farol : INotificador
{
    public void Enviar(string mensaje) => Console.WriteLine($"Farol señala: {mensaje}");
}

class Pedido
{
    private readonly INotificador _aviso;

    public Pedido(INotificador aviso)
    {
        _aviso = aviso;
    }

    public void Confirmar(string cliente)
    {
        _aviso.Enviar($"Salió el pedido de {cliente}");
    }
}
```

## R02-N10 · Composición: el violín tiene cuerdas

```meta
tipo: tema
padre: R02-N09
precio: 10
criatura: troll
temas: poo.composicion, diseno.patrones
usa: poo.interfaces, err.opcionales
```

### Crónica

Ceci quiere que su violín suene distinto según la obra: dulce para las nanas, fuerte para las marchas. —¿Hago un `ViolinDulce` y un `ViolinFuerte` que hereden? —pregunta.

Don Cedro se ríe. —¿Vas a comprar un violín nuevo para cada obra? Lo que cambia no es el violín: es **cómo tocás**. Cambiá el arco.

—Eso es la **composición** —dice {mentor}—. Un violín no **es** un arco: **tiene** un arco. Y un arco se puede cambiar en medio del concierto.

### Objetivos

- Distinguir «**es un**» (herencia) de «**tiene un**» (composición).
- Armar un objeto con otros objetos adentro.
- Pasarle el trabajo a la parte (delegar).
- Cambiar la parte en pleno uso, usando una interface (el patrón **Estrategia**).

### Antes de empezar

- Interfaces (R02-N09) y `null` (R02-N06).

### Explicación

#### «Es un» o «tiene un»

| Pregunta | Relación | En código |
|---|---|---|
| ¿Un chelo **es un** instrumento de cuerdas? | herencia | `class Chelo : Cuerdas` |
| ¿Un violín **tiene un** arco? | composición | una propiedad `Arco` |

La herencia se elige una vez y no cambia. **Regla:** preferí la composición, y dejá la herencia para cuando el «es un» sea verdad de verdad.

#### Un objeto hecho de objetos

```csharp
class Violin
{
    public Estuche Estuche { get; } = new Estuche();   // nace con él
    public IArco Arco { get; set; } = new ArcoComun();
}
```

#### Delegar

El violín no sabe cómo suena cada arco: le **pasa el trabajo** al arco que tiene:

```csharp
public string Tocar(string nota) => Arco.Sonar(nota);
```

#### Estrategia: cambiar la parte

Si la parte es una **interface**, se puede cambiar en cualquier momento, sin `if` y sin tocar `Violin`:

```csharp
violin.Arco = new ArcoFuerte();
```

Crear un arco nuevo es escribir una clase nueva. Este es el patrón **Estrategia**, uno de los más usados.

#### Una parte que puede faltar

Si el violín puede no tener estuche, se marca con `?` y se usa con cuidado: `Estuche?.Color ?? "sin estuche"`.

### Código de ejemplo

```csharp
Violin v = new Violin();
Console.WriteLine(v.Tocar("La"));
v.Arco = new ArcoFuerte();
Console.WriteLine(v.Tocar("La"));
Console.WriteLine($"Estuche: {v.Estuche?.Color ?? "sin estuche"}");

interface IArco
{
    string Sonar(string nota);
}

class ArcoDulce : IArco
{
    public string Sonar(string nota) => $"{nota.ToLower()}…";
}

class ArcoFuerte : IArco
{
    public string Sonar(string nota) => $"¡{nota.ToUpper()}!";
}

class Estuche
{
    public string Color { get; set; } = "negro";
}

class Violin
{
    public IArco Arco { get; set; } = new ArcoDulce();
    public Estuche? Estuche { get; set; }

    public string Tocar(string nota) => Arco.Sonar(nota);
}
```

### Salida esperada

```
la…
¡LA!
Estuche: sin estuche
```

### ¿Para qué sirve?

Un personaje que cambia de arma, un carrito que cambia de descuento, un juego que cambia de dificultad: todo eso es composición. Es la forma en que se arman casi todos los programas grandes: piezas chicas que se combinan y se cambian, en lugar de árboles de herencia gigantes.

### Errores habituales

- **Heredar para todo:** si escribís `ViolinDulce`, `ViolinFuerte`, `ViolinDulceConEstuche`… el árbol explota. Lo que cambia, sacalo a una parte.
- **Usar una parte que no está:** si el estuche puede faltar y lo usás sin revisar, aparece el **troll** de `NullReferenceException`. Usá `?.` y `??`.
- **Preguntar con `if` qué parte tiene:** si escribís `if (arco is ArcoFuerte)`, falta delegar: que el arco haga su trabajo.

### Micro-misión R02-N10-P1 · El violín y su arco

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: Tiene un | public IArco Arco { get; set; } · el violín tiene un arco · no es un arco
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Don Cedro le da a Ceci un arco nuevo para su violín. El plano del violín todavía no tiene dónde guardarlo.

#### Gheco sugiere
Para que un objeto **tenga** otro, se le pone una propiedad de ese tipo:

```csharp
class Tambor
{
    public Palillos Palillos { get; set; } = new Palillos();
}
```

#### Desafío
Agregale a `Violin` una propiedad `Arco` de tipo `IArco`, que empiece con un `new ArcoDulce()`.

#### Código inicial
```csharp
Violin v = new Violin();
Console.WriteLine(v.Arco.Sonar("Mi"));

interface IArco
{
    string Sonar(string nota);
}

class ArcoDulce : IArco
{
    public string Sonar(string nota) => $"{nota.ToLower()}…";
}

class Violin
{
    // el arco
}
```

#### Salida esperada
```
mi…
```

#### Solución
```csharp
Violin v = new Violin();
Console.WriteLine(v.Arco.Sonar("Mi"));

interface IArco
{
    string Sonar(string nota);
}

class ArcoDulce : IArco
{
    public string Sonar(string nota) => $"{nota.ToLower()}…";
}

class Violin
{
    public IArco Arco { get; set; } = new ArcoDulce();
}
```

#### Al superarla
El arco nuevo apenas roza la cuerda y la nota sale suave, casi un susurro. —Para las nanas —dice Don Cedro.

#### Imagen
- Un arco de violín de madera clara apoyado suavemente sobre las cuerdas de un violín, con una nota dorada suave saliendo, sin letras.
- Don Cedro sostiene el violín; Ceci prueba el arco con delicadeza.

### Micro-misión R02-N10-P2 · Que toque el arco

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Bemol
carta: Delegar | public string Tocar(string nota) => Arco.Sonar(nota); · el violín le pasa el trabajo al arco
recompensa: xp 15, oro 15
```

#### Escena
Bemol quiere decir `violin.Tocar("La")` y no `violin.Arco.Sonar("La")`. —Al violín le pido que toque. Cómo lo hace, es cosa suya.

#### Gheco sugiere
**Delegar** es pasarle el trabajo a la parte que sabe hacerlo:

```csharp
public string Golpear() => Palillos.Pegar();
```

#### Desafío
Escribí en `Violin` el método `Tocar(string nota)` que devuelva lo que suena el arco.

#### Código inicial
```csharp
Violin v = new Violin();
Console.WriteLine(v.Tocar("La"));

interface IArco
{
    string Sonar(string nota);
}

class ArcoDulce : IArco
{
    public string Sonar(string nota) => $"{nota.ToLower()}…";
}

class Violin
{
    public IArco Arco { get; set; } = new ArcoDulce();

    // Tocar
}
```

#### Salida esperada
```
la…
```

#### Solución
```csharp
Violin v = new Violin();
Console.WriteLine(v.Tocar("La"));

interface IArco
{
    string Sonar(string nota);
}

class ArcoDulce : IArco
{
    public string Sonar(string nota) => $"{nota.ToLower()}…";
}

class Violin
{
    public IArco Arco { get; set; } = new ArcoDulce();

    public string Tocar(string nota) => Arco.Sonar(nota);
}
```

#### Al superarla
—Eso —dice Bemol—. Yo no le explico al tambor cómo vibrar. Le pego, y vibra.

#### Imagen
- Un violín con su arco apoyado, del que salen notas doradas suaves, sobre una mesa de taller de madera, sin letras.
- Bemol explica con un palillo de tambor en la mano; Ceci asiente.

### Micro-misión R02-N10-P3 · Cambiar de arco en pleno concierto

```meta
lugar: El Escenario Grande
personajes: Ceci, Clave
carta: Estrategia | v.Arco = new ArcoFuerte(); · cambia la parte · el violín no cambia
recompensa: xp 15, oro 15
```

#### Escena
La obra empieza con una nana y termina con una marcha. Ceci tiene que cambiar de arco en el medio, sin bajar del escenario.

#### Gheco sugiere
Como `Arco` es una interface, se le puede asignar cualquier arco en cualquier momento:

```csharp
tambor.Palillos = new Mazas();
```

#### Desafío
Escribí la clase `ArcoFuerte`, que suene `¡<NOTA en mayúsculas>!`, y cambiá el arco antes de la segunda nota.

#### Código inicial
```csharp
Violin v = new Violin();
Console.WriteLine(v.Tocar("Sol"));
// cambiá de arco
Console.WriteLine(v.Tocar("Sol"));

interface IArco
{
    string Sonar(string nota);
}

class ArcoDulce : IArco
{
    public string Sonar(string nota) => $"{nota.ToLower()}…";
}

// el ArcoFuerte

class Violin
{
    public IArco Arco { get; set; } = new ArcoDulce();

    public string Tocar(string nota) => Arco.Sonar(nota);
}
```

#### Salida esperada
```
sol…
¡SOL!
```

#### Solución
```csharp
Violin v = new Violin();
Console.WriteLine(v.Tocar("Sol"));
v.Arco = new ArcoFuerte();
Console.WriteLine(v.Tocar("Sol"));

interface IArco
{
    string Sonar(string nota);
}

class ArcoDulce : IArco
{
    public string Sonar(string nota) => $"{nota.ToLower()}…";
}

class ArcoFuerte : IArco
{
    public string Sonar(string nota) => $"¡{nota.ToUpper()}!";
}

class Violin
{
    public IArco Arco { get; set; } = new ArcoDulce();

    public string Tocar(string nota) => Arco.Sonar(nota);
}
```

#### Al superarla
La nana se apaga y, con un solo cambio de arco, entra la marcha. El público del ensayo se endereza en las sillas. Clave sonríe apenas.

#### Imagen
- Un escenario grande de teatro gótico con filas de sillas, y en el centro una violinista cambiando un arco claro por uno oscuro, con notas doradas fuertes saliendo, sin letras.
- Ceci en el escenario; Clave, en la primera fila, sonríe apenas.

### Micro-misión R02-N10-P4 · El arco que cuenta

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
carta: La parte guarda su estado | cada arco lleva su cuenta · el violín no se entera
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Don Cedro inventa un arco especial: cada tercera nota la toca con un acento. —El arco lleva la cuenta —dice—, no el violín.

#### Gheco sugiere
Una parte puede guardar sus propios datos. El violín no necesita saber nada:

```csharp
class Mazas : IPalillos
{
    private int _golpes = 0;

    public string Pegar()
    {
        _golpes++;
        return _golpes % 2 == 0 ? "PUM" : "pum";
    }
}
```

`nota.ToLower()` devuelve el texto **en minúsculas** (es lo contrario de `ToUpper()`, que lo pasa a mayúsculas).

#### Desafío
Completá `ArcoAcento`: que cuente las notas y, cada tres, devuelva la nota en mayúsculas con `!`; las demás, en minúsculas.

#### Código inicial
```csharp
Violin v = new Violin { Arco = new ArcoAcento() };
foreach (string nota in new[] { "Do", "Re", "Mi", "Fa", "Sol", "La" })
{
    Console.Write(v.Tocar(nota) + " ");
}
Console.WriteLine();

interface IArco
{
    string Sonar(string nota);
}

class ArcoAcento : IArco
{
    private int _notas = 0;

    public string Sonar(string nota)
    {
        return nota.ToLower();
    }
}

class Violin
{
    public IArco Arco { get; set; } = new ArcoAcento();

    public string Tocar(string nota) => Arco.Sonar(nota);
}
```

#### Salida esperada
```
do re MI! fa sol LA! 
```

#### Solución
```csharp
Violin v = new Violin { Arco = new ArcoAcento() };
foreach (string nota in new[] { "Do", "Re", "Mi", "Fa", "Sol", "La" })
{
    Console.Write(v.Tocar(nota) + " ");
}
Console.WriteLine();

interface IArco
{
    string Sonar(string nota);
}

class ArcoAcento : IArco
{
    private int _notas = 0;

    public string Sonar(string nota)
    {
        _notas++;
        return _notas % 3 == 0 ? nota.ToUpper() + "!" : nota.ToLower();
    }
}

class Violin
{
    public IArco Arco { get; set; } = new ArcoAcento();

    public string Tocar(string nota) => Arco.Sonar(nota);
}
```

#### Al superarla
Do, re, ¡MI!; fa, sol, ¡LA! El violín suena como un vals sin que nadie le haya enseñado a bailar. Don Cedro guiña un ojo: —El secreto está en el arco.

#### Imagen
- Un arco de violín oscuro con tres pequeñas muescas brillantes en la vara, apoyado sobre un violín, con notas doradas de distintos tamaños saliendo en ritmo, sin letras.
- Don Cedro guiña un ojo; Ceci toca con una sonrisa.

### Micro-misión R02-N10-P5 · El troll del estuche que no estaba

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Gheco
criatura: troll
carta: Troll | una parte que puede faltar (?) · v.Estuche?.Color ?? "sin estuche" · revisá antes de usar
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
El troll pregunta de qué color es el estuche de un violín que no tiene estuche. El programa explota.

#### Gheco sugiere
Si una parte puede faltar, está marcada con `?`. Antes de entrar, preguntá con `?.`, y dale un valor por si falta con `??`:

```csharp
string color = tambor.Funda?.Color ?? "sin funda";
```

#### Desafío
Ensayá, mirá cómo explota y arreglá la línea del color para que muestre `sin estuche`.

#### Código inicial
```csharp
Violin v = new Violin();
Console.WriteLine($"Estuche: {v.Estuche!.Color}");

class Estuche
{
    public string Color { get; set; } = "negro";
}

class Violin
{
    public Estuche? Estuche { get; set; }
}
```

#### Salida esperada
```
Estuche: sin estuche
```

#### Solución
```csharp
Violin v = new Violin();
Console.WriteLine($"Estuche: {v.Estuche?.Color ?? "sin estuche"}");

class Estuche
{
    public string Color { get; set; } = "negro";
}

class Violin
{
    public Estuche? Estuche { get; set; }
}
```

#### Al superarla
El troll busca el estuche por todo el taller, no lo encuentra y, como no explotó nada, se aburre y se va.

#### Imagen
- Un troll chiquito de piel color musgo, pelo de paja y chaleco remendado, buscando debajo de una mesa de taller con una vela, con cara de confundido.
- Gheco lo mira desde arriba de un violín sin estuche.

### Encargo R02-N10-E1 · Los descuentos de Baldo

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Baldo quiere cambiar el descuento de su puesto según el día, sin tocar el código del carrito. Escribí una interface `IDescuento` con `decimal Aplicar(decimal total)` y tres clases:

- `SinDescuento`: devuelve el total igual.
- `Porcentaje`: recibe un porcentaje en el constructor y lo descuenta.
- `Fijo`: recibe un monto y lo resta, sin bajar de `0`.

Después, una clase `Carrito` con una propiedad `Descuento` (`IDescuento`, empieza en `SinDescuento`), un método `Agregar(decimal precio)` y un método `Cobrar()` que devuelva el total con el descuento aplicado. Con `300` y `200` en el carrito, cobrá con los tres descuentos (`10`% y `150` fijos):

```
Sin descuento: 500
Con 10%: 450
Con 150 menos: 350
```

#### Criterio de aprobación

- `Carrito` tiene un `IDescuento` y le delega la cuenta.
- Para cambiar el descuento se asigna otro objeto; `Carrito` no usa `if` para elegirlo.

#### Salida esperada

```
Sin descuento: 500
Con 10%: 450
Con 150 menos: 350
```

#### Solución de referencia

```csharp
Carrito c = new Carrito();
c.Agregar(300);
c.Agregar(200);
Console.WriteLine($"Sin descuento: {c.Cobrar()}");
c.Descuento = new Porcentaje(10);
Console.WriteLine($"Con 10%: {c.Cobrar()}");
c.Descuento = new Fijo(150);
Console.WriteLine($"Con 150 menos: {c.Cobrar()}");

interface IDescuento
{
    decimal Aplicar(decimal total);
}

class SinDescuento : IDescuento
{
    public decimal Aplicar(decimal total) => total;
}

class Porcentaje : IDescuento
{
    private readonly decimal _porcentaje;

    public Porcentaje(decimal porcentaje)
    {
        _porcentaje = porcentaje;
    }

    public decimal Aplicar(decimal total) => total - total * _porcentaje / 100;
}

class Fijo : IDescuento
{
    private readonly decimal _monto;

    public Fijo(decimal monto)
    {
        _monto = monto;
    }

    public decimal Aplicar(decimal total) => Math.Max(0, total - _monto);
}

class Carrito
{
    private decimal _total = 0;

    public IDescuento Descuento { get; set; } = new SinDescuento();

    public void Agregar(decimal precio)
    {
        _total += precio;
    }

    public decimal Cobrar() => Descuento.Aplicar(_total);
}
```

## R02-N11 · Jefe: la Quimera de las Mil Partituras

```meta
tipo: jefe
padre: R02-N10
precio: 10
criatura: dragon
insignia: Maestro Luthier
insignia_descripcion: Venciste a la Quimera de las Mil Partituras: sabés armar programas con clases, herencia, interfaces y composición.
usa: poo.clases, poo.encapsulamiento, poo.constructores, poo.herencia, poo.polimorfismo, poo.interfaces, poo.composicion
```

### Crónica

Una noche, el Taller de Instrumentos amanece revuelto. Alguien juntó las partituras de todos los planos en una sola pila, y de la pila se levantó una criatura: la **Quimera de las Mil Partituras**. Tiene cabeza de león hecha de bronce de trompeta, cuerpo de hojas de partitura, alas como abanicos de papel y una cola de cuerdas de violín. Cada parte viene de un plano distinto, y ninguna encaja con las otras.

—Mezcló todo —dice Don Cedro, con el formón en la mano—. Planos que heredan de lo que no son, promesas sin cumplir, datos a la vista de cualquiera.

—Entonces la desarmamos plano por plano —dice {mentor}—. Ceci, usá todo lo que aprendiste en el Taller.

### Objetivos

- Juntar en un programa todo lo del Taller: clases, propiedades, constructores, herencia, polimorfismo, interfaces y composición.
- Encontrar qué parte de un diseño está mal y arreglarla sin romper el resto.

### Antes de empezar

- Todos los nodos del Taller de Instrumentos (R02-N01 a R02-N10).

### Explicación

#### Cómo se desarma una quimera

Cuando un programa con muchas clases no anda, revisá de a una pieza:

1. **¿Compila?** Leé el primer error: ¿falta un `public`, un `override`, algo que pide una interface, un dato del constructor?
2. **¿Cada dato se cuida solo?** Lo que no puede valer cualquier cosa va en una propiedad que lo revise.
3. **¿Cada uno hace su parte?** Si hay `if` preguntando el tipo, falta un `override`.
4. **¿«Es un» o «tiene un»?** Si una clase hereda de algo que no es, cambialo por una parte.

#### Lo que ya sabés

| Pieza | Para qué |
|---|---|
| `class` + `new` | el plano y los objetos |
| propiedades | datos que se cuidan solos |
| constructor | nacer completo |
| `: Base` + `override` | familias con su propia voz |
| `abstract` | obligar a completar |
| `interface` | prometer lo que se sabe hacer |
| composición | tener partes que se cambian |

### Código de ejemplo

```csharp
Musico[] orquesta =
{
    new Musico("Ceci", new Violin()),
    new Musico("Bemol", new Tambor()),
};

foreach (Musico m in orquesta)
{
    Console.WriteLine(m.Tocar());
}
orquesta[1].Instrumento = new Violin();
Console.WriteLine(orquesta[1].Tocar());

interface IInstrumento
{
    string Sonido();
}

class Violin : IInstrumento
{
    public string Sonido() => "la la la";
}

class Tambor : IInstrumento
{
    public string Sonido() => "pum pum";
}

class Musico
{
    public string Nombre { get; }
    public IInstrumento Instrumento { get; set; }

    public Musico(string nombre, IInstrumento instrumento)
    {
        Nombre = nombre;
        Instrumento = instrumento;
    }

    public string Tocar() => $"{Nombre}: {Instrumento.Sonido()}";
}
```

### Salida esperada

```
Ceci: la la la
Bemol: pum pum
Bemol: la la la
```

### ¿Para qué sirve?

Así se escriben los programas de verdad: muchas piezas chicas, cada una con un trabajo claro, que se combinan. Unity y Godot funcionan así: cada objeto del juego tiene partes (su dibujo, su física, su sonido) que se agregan y se cambian.

### Errores habituales

- **Arreglar todo a la vez:** de a una pieza, y ensayando entre una y otra.
- **Tapar un error con un `if`:** si un objeto hace algo mal, arreglalo **en su clase**.
- **Heredar para tener algo:** «tiene un» es composición.

### Micro-misión R02-N11-P1 · La garra a la vista

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Don Cedro
criatura: dragon
carta: Jefe 1 | un dato que no puede valer cualquier cosa · private + propiedad que revisa · value
recompensa: xp 20, oro 20, monedas 4
```

#### Escena
La primera garra de la Quimera es un violín con el volumen a la vista: cualquiera le escribe `-30` y la cuerda se rompe. Hay que cuidarlo.

#### Gheco sugiere
Escondé el dato y dejalo pasar por una propiedad que revise. Si el valor no sirve, se ignora:

```csharp
private int _vida = 10;
public int Vida
{
    get => _vida;
    set { if (value >= 0) _vida = value; }
}
```

#### Desafío
Convertí `volumen` en una propiedad `Volumen` que solo acepte valores de `0` a `10` (empieza en `5`).

#### Código inicial
```csharp
Violin v = new Violin();
v.volumen = -30;
Console.WriteLine($"Volumen: {v.volumen}");
v.volumen = 8;
Console.WriteLine($"Volumen: {v.volumen}");

class Violin
{
    public int volumen = 5;
}
```

#### Salida esperada
```
Volumen: 5
Volumen: 8
```

#### Solución
```csharp
Violin v = new Violin();
v.Volumen = -30;
Console.WriteLine($"Volumen: {v.Volumen}");
v.Volumen = 8;
Console.WriteLine($"Volumen: {v.Volumen}");

class Violin
{
    private int _volumen = 5;

    public int Volumen
    {
        get => _volumen;
        set
        {
            if (value >= 0 && value <= 10) _volumen = value;
        }
    }
}
```

#### Al superarla
La garra de violín se suelta de la Quimera y cae al piso, entera y afinada. La criatura ruge con un acorde roto.

#### Imagen
- Una criatura quimera hecha de partes de instrumentos: cabeza de león de bronce de trompeta, cuerpo de hojas de partitura sin letras, alas de abanico de papel y cola de cuerdas de violín, perdiendo una garra con forma de violín.
- Ceci, con su violín, la enfrenta; Don Cedro sostiene un formón detrás de ella.

### Micro-misión R02-N11-P2 · El ala que nació vacía

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Bemol
criatura: dragon
carta: Jefe 2 | un objeto que nace sin lo que necesita · constructor que lo pide · se asigna adentro
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
Un ala de la Quimera está hecha de partituras sin título: nacieron vacías y nadie les puso nombre después.

#### Gheco sugiere
Un constructor obliga a dar los datos al nacer. Con una propiedad de solo lectura, queda fija:

```csharp
public string Titulo { get; }

public Obra(string titulo)
{
    Titulo = titulo;
}
```

#### Desafío
Escribí un constructor en `Partitura` que reciba el título y lo guarde. Después, cambiá los `new` del programa para que cada partitura nazca con su título: `Nana` y `Marcha`.

#### Código inicial
```csharp
Partitura a = new Partitura();
Partitura b = new Partitura();
Console.WriteLine(a.Titulo);
Console.WriteLine(b.Titulo);

class Partitura
{
    public string Titulo { get; } = "";
}
```

#### Salida esperada
```
Nana
Marcha
```

#### Solución
```csharp
Partitura a = new Partitura("Nana");
Partitura b = new Partitura("Marcha");
Console.WriteLine(a.Titulo);
Console.WriteLine(b.Titulo);

class Partitura
{
    public string Titulo { get; }

    public Partitura(string titulo)
    {
        Titulo = titulo;
    }
}
```

#### Al superarla
Las hojas del ala se ordenan, cada una con su título, y se van volando hacia el estante. A la Quimera le queda una sola ala.

#### Imagen
- La quimera de partes de instrumentos con un ala de papel deshaciéndose en hojas de partitura sin letras que vuelan ordenadas hacia un estante.
- Bemol atrapa algunas hojas en el aire; Ceci apunta con el arco.

### Micro-misión R02-N11-P3 · La cola que no sabe su voz

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Clave
criatura: dragon
carta: Jefe 3 | todos suenan igual · abstract en la base · override en cada uno
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
La cola de la Quimera está hecha de instrumentos que suenan todos igual: «...». Nadie les escribió su voz, y la base no se lo exigió.

#### Gheco sugiere
Con `abstract`, la base obliga a cada derivada a escribir su versión. Si alguna no lo hace, el compilador avisa:

```csharp
abstract class Ave
{
    public abstract string Canto();
}
```

#### Desafío
Convertí `Instrumento` en `abstract` con `Sonido()` abstracto, y escribí el `Sonido()` de cada uno: el arpa hace `tlin tlin` y la trompeta `tururú`.

#### Código inicial
```csharp
Instrumento[] cola = { new Arpa(), new Trompeta() };
foreach (Instrumento i in cola)
{
    Console.WriteLine(i.Sonido());
}

class Instrumento
{
    public virtual string Sonido() => "...";
}

class Arpa : Instrumento { }

class Trompeta : Instrumento { }
```

#### Salida esperada
```
tlin tlin
tururú
```

#### Solución
```csharp
Instrumento[] cola = { new Arpa(), new Trompeta() };
foreach (Instrumento i in cola)
{
    Console.WriteLine(i.Sonido());
}

abstract class Instrumento
{
    public abstract string Sonido();
}

class Arpa : Instrumento
{
    public override string Sonido() => "tlin tlin";
}

class Trompeta : Instrumento
{
    public override string Sonido() => "tururú";
}
```

#### Al superarla
La cola suena: tlin tlin, tururú. Cada instrumento con su voz. La Quimera se sacude, confundida: ya no es un solo ruido, es una orquesta.

#### Imagen
- La quimera de partes de instrumentos con la cola de cuerdas convertida en un arpa y una trompeta que suenan, con notas doradas saliendo, sin letras.
- Clave dirige con la batuta; Ceci toca a su lado.

### Micro-misión R02-N11-P4 · La cabeza que heredó de más

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Bemol, Don Cedro
criatura: dragon
carta: Jefe 4 | «es un» o «tiene un» · un músico no es un violín · tiene un instrumento
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
La cabeza de la Quimera es un músico que **hereda** de violín. Por eso no puede cambiar de instrumento: quedó pegado al violín para siempre.

#### Gheco sugiere
Si algo **tiene** otra cosa, va como una parte, no como herencia. Una parte se puede cambiar:

```csharp
class Jinete
{
    public ICaballo Caballo { get; set; }
}
```

#### Desafío
Cambiá `Musico` para que **no** herede de `Violin` y en cambio **tenga** un `IInstrumento` (que empiece con un `Violin`). Su `Tocar()` usa el sonido del instrumento. El programa después le da un tambor.

#### Código inicial
```csharp
Musico bemol = new Musico();
Console.WriteLine(bemol.Tocar());
bemol.Instrumento = new Tambor();
Console.WriteLine(bemol.Tocar());

interface IInstrumento
{
    string Sonido();
}

class Violin : IInstrumento
{
    public string Sonido() => "la la la";
}

class Tambor : IInstrumento
{
    public string Sonido() => "pum pum";
}

class Musico : Violin
{
    public string Tocar() => Sonido();
}
```

#### Salida esperada
```
la la la
pum pum
```

#### Solución
```csharp
Musico bemol = new Musico();
Console.WriteLine(bemol.Tocar());
bemol.Instrumento = new Tambor();
Console.WriteLine(bemol.Tocar());

interface IInstrumento
{
    string Sonido();
}

class Violin : IInstrumento
{
    public string Sonido() => "la la la";
}

class Tambor : IInstrumento
{
    public string Sonido() => "pum pum";
}

class Musico
{
    public IInstrumento Instrumento { get; set; } = new Violin();

    public string Tocar() => Instrumento.Sonido();
}
```

#### Al superarla
La cabeza de bronce se despega del cuerpo con un *clang*. Lo que queda de la Quimera tiembla: ya casi no tiene de dónde agarrarse.

#### Imagen
- La cabeza de león de bronce de trompeta de la quimera cayendo y rebotando en el piso de madera del taller, sin letras.
- Don Cedro aplaude con el formón en la mano; Bemol, a su lado, levanta un tambor como trofeo.

### Micro-misión R02-N11-P5 · La orquesta del Taller

```meta
lugar: El Taller de Instrumentos
personajes: Ceci, Clave, Bemol, Don Cedro, Gheco
criatura: dragon
carta: Jefe | interface + constructor + composición + polimorfismo · un error a la vez · al final, que suene
recompensa: xp 30, oro 30, monedas 3
item: Cuerda de la Quimera
```

#### Escena
Es el último plano de la Quimera: la orquesta del Taller entera. Tiene tres errores: un músico que no cumple su promesa, un `new` sin el dato que pide el constructor y un método llamado con otra mayúscula. Si compila y suena, la Quimera se deshace en partituras ordenadas.

#### Gheco sugiere
De a uno. Ensayá, leé el **primer** error, arreglalo y volvé a ensayar. Los códigos que vas a ver: `CS0535` (falta lo que pide la interface), `CS7036` (falta un dato del constructor) y `CS1061` (ese método no existe con ese nombre).

#### Desafío
Arreglá los tres errores para que la orquesta toque completa. La flauta hace `fiu fiu`, y el tercer músico es `Clave`.

#### Código inicial
```csharp
Musico[] orquesta =
{
    new Musico("Ceci", new Violin()),
    new Musico("Bemol", new Flauta()),
    new Musico(new Violin()),
};

foreach (Musico m in orquesta)
{
    Console.WriteLine(m.tocar());
}

interface IInstrumento
{
    string Sonido();
}

class Violin : IInstrumento
{
    public string Sonido() => "la la la";
}

class Flauta : IInstrumento
{
}

class Musico
{
    public string Nombre { get; }
    public IInstrumento Instrumento { get; set; }

    public Musico(string nombre, IInstrumento instrumento)
    {
        Nombre = nombre;
        Instrumento = instrumento;
    }

    public string Tocar() => $"{Nombre}: {Instrumento.Sonido()}";
}
```

#### Salida esperada
```
Ceci: la la la
Bemol: fiu fiu
Clave: la la la
```

#### Solución
```csharp
Musico[] orquesta =
{
    new Musico("Ceci", new Violin()),
    new Musico("Bemol", new Flauta()),
    new Musico("Clave", new Violin()),
};

foreach (Musico m in orquesta)
{
    Console.WriteLine(m.Tocar());
}

interface IInstrumento
{
    string Sonido();
}

class Violin : IInstrumento
{
    public string Sonido() => "la la la";
}

class Flauta : IInstrumento
{
    public string Sonido() => "fiu fiu";
}

class Musico
{
    public string Nombre { get; }
    public IInstrumento Instrumento { get; set; }

    public Musico(string nombre, IInstrumento instrumento)
    {
        Nombre = nombre;
        Instrumento = instrumento;
    }

    public string Tocar() => $"{Nombre}: {Instrumento.Sonido()}";
}
```

#### Al superarla
La orquesta suena entera, y la Quimera de las Mil Partituras se deshace en una lluvia de hojas que caen, una por una, cada una en su estante. En el piso queda una cuerda de violín dorada, enroscada como una cola: **la Cuerda de la Quimera**.

Don Cedro la levanta y se la da a Ceci. —Un plano bien hecho no se rompe —dice—. Y vos ya sabés hacerlos.

{mentor} guarda la batuta. —El Taller está en orden. Mañana, el Archivo: ahí no se guarda un violín, se guardan mil.

#### Imagen
- Un taller de luthier de madera lleno de hojas de partitura sin letras que caen ordenadas hacia los estantes, con una cuerda de violín dorada enroscada brillando en el piso.
- Don Cedro le da la cuerda a Ceci; Clave, Bemol y Gheco miran sonriendo.

### Encargo R02-N11-E1 · El tablero de Kira

```meta
entrega: codigo
entorno: navegador
monedas: 2
xp: 30
```

#### Consigna

Kira entrena en el campo de las Forjas con muñecos de práctica. Escribí:

1. Una interface `IGolpeable` con `string Nombre { get; }`, `int Vida { get; }` y `void Recibir(int danio)`.
2. Una clase `abstract` `Muneco : IGolpeable` con un constructor que reciba el nombre y la vida, y una `Vida` que nunca baje de `0`. Su `Recibir` es `virtual` y resta el daño.
3. Dos derivadas: `MunecoDePaja` (vida `20`) y `MunecoDeHierro` (vida `40`), que en su `Recibir` usa solo la **mitad** del daño (con `base.Recibir`).
4. Una interface `IArma` con `int Danio()`, y dos armas: `Espada` (`8`) y `Martillo` (`12`).
5. Una clase `Kira` que **tiene** un `IArma` (empieza con espada) y un método `Atacar(IGolpeable blanco)`.

Kira ataca al de paja con espada, cambia al martillo y ataca a los dos. Mostrá la vida de cada muñeco al final:

```
paja: 0
hierro: 34
```

#### Criterio de aprobación

- `Kira` tiene su arma como una parte (`IArma`) y la cambia sin `if`.
- `MunecoDeHierro` usa `override` y `base.Recibir`.
- La vida no baja de `0`.

#### Salida esperada

```
paja: 0
hierro: 34
```

#### Solución de referencia

```csharp
IGolpeable[] blancos = { new MunecoDePaja(), new MunecoDeHierro() };
Kira kira = new Kira();
kira.Atacar(blancos[0]);
kira.Arma = new Martillo();
foreach (IGolpeable b in blancos)
{
    kira.Atacar(b);
}
foreach (IGolpeable b in blancos)
{
    Console.WriteLine($"{b.Nombre}: {b.Vida}");
}

interface IGolpeable
{
    string Nombre { get; }
    int Vida { get; }
    void Recibir(int danio);
}

abstract class Muneco : IGolpeable
{
    private int _vida;

    public string Nombre { get; }
    public int Vida => _vida;

    protected Muneco(string nombre, int vida)
    {
        Nombre = nombre;
        _vida = vida;
    }

    public virtual void Recibir(int danio)
    {
        _vida = Math.Max(0, _vida - danio);
    }
}

class MunecoDePaja : Muneco
{
    public MunecoDePaja() : base("paja", 20) { }
}

class MunecoDeHierro : Muneco
{
    public MunecoDeHierro() : base("hierro", 40) { }

    public override void Recibir(int danio)
    {
        base.Recibir(danio / 2);
    }
}

interface IArma
{
    int Danio();
}

class Espada : IArma
{
    public int Danio() => 8;
}

class Martillo : IArma
{
    public int Danio() => 12;
}

class Kira
{
    public IArma Arma { get; set; } = new Espada();

    public void Atacar(IGolpeable blanco)
    {
        blanco.Recibir(Arma.Danio());
    }
}
```
