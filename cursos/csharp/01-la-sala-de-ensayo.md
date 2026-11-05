# RAMA R01 · La Sala de Ensayo: los fundamentos

```meta
tipo: tronco
posicion: 1
```

## R01-N01 · Variables: los atriles con nombre

```meta
tipo: tema
padre: R00-N01
precio: 10
criatura: esqueleto
temas: prog.variables, prog.salida
usa: prog.entorno
```

### Crónica

A las ocho en punto, Clave pone en fila diez atriles, cada uno con una etiqueta: *compases*, *obra*, *tempo*. Ceci quiere tocar ya.

—Antes de tocar, se anota —dice {mentor}—. Cada dato en su atril, y cada atril con su nombre. Así, cuando lo necesitás, lo llamás y está.

En ese momento entra **Nilo**, el mensajero del Puerto, con una carta para Clave. Mira los atriles y sonríe: —En el Puerto usamos cajones. Es lo mismo.

### Objetivos

- Entender qué es una variable.
- Guardar un número entero (`int`) y un texto (`string`).
- Cambiar lo que guarda una variable.
- Mostrar variables dentro de un texto con `$"..."`.

### Antes de empezar

- Mostrar texto con `Console.WriteLine` (Clase 0).

### Explicación

#### ¿Qué es una variable?

Una **variable** es un atril con nombre: un lugar donde el programa guarda un dato para usarlo después.

```csharp
int compases = 4;
```

Tiene tres partes:

- `int`: **qué tipo de dato** guarda. `int` es un número entero.
- `compases`: **el nombre** del atril.
- `4`: **el valor** que guarda.

El `=` no es el «igual» de matemática: quiere decir **«guardá esto acá»**.

#### Dos tipos para empezar

| Tipo | Guarda | Ejemplo |
|---|---|---|
| `int` | números enteros | `int compases = 4;` |
| `string` | texto, entre comillas | `string obra = "Vals";` |

#### Usar una variable

Para usarla, se escribe su nombre **sin comillas**:

```csharp
Console.WriteLine(compases);   // muestra 4
Console.WriteLine("compases"); // muestra la palabra compases
```

#### Cambiar el valor

Una variable se puede cambiar, sin repetir el tipo:

```csharp
compases = 8;
```

El valor de antes se pierde y queda el nuevo.

#### Texto con variables adentro

Si un texto empieza con `$`, lo que va entre llaves `{ }` se reemplaza por su valor:

```csharp
Console.WriteLine($"Son {compases} compases");
```

Muestra `Son 8 compases`.

### Código de ejemplo

```csharp
string obra = "Vals de la Feria";
int compases = 4;

Console.WriteLine(obra);
Console.WriteLine(compases);

compases = 8;
Console.WriteLine($"{obra}: {compases} compases");
```

### Salida esperada

```
Vals de la Feria
4
Vals de la Feria: 8 compases
```

### ¿Para qué sirve?

Los puntos de un jugador, el nombre de un usuario o el precio de una entrada: todo dato que un programa recuerda vive en una variable.

### Errores habituales

- **Escribir mal el nombre:** `Compases` y `compases` son dos nombres distintos.
- **Usar una variable antes de crearla:** el compilador avisa con `CS0103`.
- **Poner comillas de más:** `"compases"` es la palabra, no la variable.

### Micro-misión R01-N01-P1 · El atril de los compases

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Variable entera | int compases = 4; · int es un número entero · el = guarda el valor en la variable
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Clave le señala a Ceci el primer atril, que tiene una etiqueta y nada más. —Este atril se llama *vueltas*. Guardá ahí cuántas vueltas da la cajita.

#### Gheco sugiere
Una **variable** es un atril con nombre donde el programa guarda un dato. Se crea así:

```csharp
int edad = 12;
```

`int` quiere decir «número entero», `edad` es el nombre y `12` es lo que guarda. Después se usa por su nombre, sin comillas: `Console.WriteLine(edad);` muestra `12`.

#### Desafío
Creá una variable `int` llamada `vueltas` con el valor `3`. La orden que la muestra ya está escrita.

#### Código inicial
```csharp
// Creá la variable vueltas acá

Console.WriteLine(vueltas);
```

#### Salida esperada
```
3
```

#### Solución
```csharp
int vueltas = 3;
Console.WriteLine(vueltas);
```

#### Al superarla
En la etiqueta del atril aparece un 3. Ceci da tres vueltas a la cuerda de la cajita: suena igual de rara, pero ahora lo tiene anotado.

#### Imagen
- Una fila de atriles de madera con etiquetas lisas sin nada escrito, en una sala de ensayo con tubos de órgano al fondo.
- Clave señala un atril con la batuta; Ceci da cuerda a una cajita de música de madera.

### Micro-misión R01-N01-P2 · El atril del texto

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Variable de texto | string obra = "Vals"; · string guarda texto · el texto siempre va entre comillas
recompensa: xp 15, oro 15
```

#### Escena
—No todo es número —dice Bemol, y le muestra su atril—. El mío guarda el nombre de la obra que me toca. Yo siempre me olvido.

#### Gheco sugiere
Para guardar texto se usa el tipo `string`. El texto va entre comillas:

```csharp
string ciudad = "La Rioja";
Console.WriteLine(ciudad);
```

Muestra `La Rioja`. Las comillas van cuando **creás** el texto; cuando usás la variable, **no**.

#### Desafío
Creá una variable `string` llamada `obra` que guarde el texto `Vals de la Feria`.

#### Código inicial
```csharp
// Creá la variable obra acá

Console.WriteLine(obra);
```

#### Salida esperada
```
Vals de la Feria
```

#### Solución
```csharp
string obra = "Vals de la Feria";
Console.WriteLine(obra);
```

#### Al superarla
—Ese vals lo tocamos con Hilván todas las noches —dice Ceci—. Ahora quedó anotado, y no me lo voy a olvidar.

#### Imagen
- Bemol con su tambor y Ceci con su violín, parados frente a un atril de madera con una hoja en blanco, en una sala de ensayo.

### Micro-misión R01-N01-P3 · Cambiar lo que hay en el atril

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave, Gheco
carta: Cambiar el valor | compases = 8; · no se repite el tipo · el valor de antes se pierde
recompensa: xp 15, oro 15
```

#### Escena
—Cambió el programa del concierto —avisa Clave—. Eran cuatro compases, ahora son ocho. No hace falta otro atril: se borra y se anota de nuevo.

#### Gheco sugiere
Para cambiar lo que guarda una variable, se escribe su nombre, `=` y el valor nuevo. **No se repite el tipo**:

```csharp
int puntos = 10;
puntos = 25;
Console.WriteLine(puntos);
```

Muestra `25`: el 10 ya no está. Las órdenes se hacen en orden, así que importa **dónde** cambiás el valor.

#### Desafío
Agregá una línea, en el lugar marcado, para que `compases` pase a valer `8`.

#### Código inicial
```csharp
int compases = 4;
Console.WriteLine(compases);
// Cambiá compases a 8 acá

Console.WriteLine(compases);
```

#### Salida esperada
```
4
8
```

#### Solución
```csharp
int compases = 4;
Console.WriteLine(compases);
compases = 8;
Console.WriteLine(compases);
```

#### Al superarla
Ceci borra el 4 con el dedo y anota un 8. Gheco aplaude con la colita: la misma variable, otro valor.

#### Imagen
- Ceci frente a un atril borra algo de una pizarrita con el dedo; Clave observa con los brazos cruzados y la batuta en la mano.
- Gheco sobre el atril mueve la colita, contento. La pizarrita se ve lisa, sin nada escrito.

### Micro-misión R01-N01-P4 · La carta del Puerto

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Nilo
carta: Texto con valores | $"Hola, {nombre}" · el $ va antes de las comillas · lo que está entre { } se reemplaza por su valor
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Nilo deja una carta sobre el atril. —De parte de Elefa. Necesita saber la obra y los compases, los dos en un renglón. Ceci mira las dos variables y no sabe cómo juntarlas.

#### Gheco sugiere
Si ponés un `$` antes de las comillas, podés meter variables adentro del texto, entre llaves:

```csharp
string nombre = "Ana";
int edad = 12;
Console.WriteLine($"{nombre} tiene {edad} años");
```

Muestra `Ana tiene 12 años`. Sin el `$`, se vería `{nombre}` tal cual.

#### Desafío
Completá el texto para que muestre `Vals: 8 compases`, usando las dos variables. No escribas el nombre ni el número a mano.

#### Código inicial
```csharp
string obra = "Vals";
int compases = 8;
Console.WriteLine($"");
```

#### Salida esperada
```
Vals: 8 compases
```

#### Solución
```csharp
string obra = "Vals";
int compases = 8;
Console.WriteLine($"{obra}: {compases} compases");
```

#### Al superarla
Nilo guarda la respuesta en su bolso y sale corriendo. —¡Elefa contesta todo el mismo día! ¡Ustedes también!

#### Imagen
- Nilo, el mensajero, deja un sobre con sello de lacre violeta sobre un atril de madera, sonriendo.
- Ceci, con el violín en la mano, mira el sobre.

### Micro-misión R01-N01-P5 · El esqueleto del atril vacío

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
criatura: esqueleto
carta: Nombres | CS0103: ese nombre no existe · revisá cómo se escribió · Tempo y tempo son nombres distintos
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Detrás de un atril aparece un esqueletito con una batuta rota. Lo llaman y no contesta: es un nombre sin nadie adentro. —Se llama *Tempo*, con mayúscula —dice Gheco—. Pero acá alguien lo llamó con minúscula.

#### Gheco sugiere
C# distingue mayúsculas de minúsculas: `nota` y `Nota` son dos nombres distintos. Si usás un nombre que no existe, aparece este error:

```
Programa.cs(2,19): error CS0103: El nombre 'Nota' no existe en el contexto actual
```

Hay que comparar cómo se creó la variable y cómo se usa: tienen que estar escritas **exactamente igual**.

#### Desafío
Tocá *Ejecutar* y leé el error. Después corregí el nombre en la segunda línea para que el programa funcione.

#### Código inicial
```csharp
int tempo = 90;
Console.WriteLine(Tempo);
```

#### Salida esperada
```
90
```

#### Solución
```csharp
int tempo = 90;
Console.WriteLine(tempo);
```

#### Al superarla
El esqueletito se deshace en un montón de huesitos y un silbido desafinado. Ceci ya no se asusta: lee el mensaje, busca la línea y lo arregla.

#### Imagen
- Un esqueleto chiquito y simpático, del alto de un nene de seis años, sin armas, con una batuta rota, asoma detrás de un atril en una sala de ensayo.
- Ceci lo señala riéndose; Gheco en su hombro.

### Encargo R01-N01-E1 · La carga del barco

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Elefa, la Capitana del Puerto, le pide al Conservatorio una ficha para su registro. Creá tres variables: `barco` (`Gaviota`), `carga` (`violines`) y `cajones` (`12`). Mostrá con ellas este renglón:

```
Gaviota lleva 12 cajones de violines
```

#### Criterio de aprobación

- Usa las tres variables, con el tipo correcto.
- El renglón se arma con `$"..."`.

#### Salida esperada

```
Gaviota lleva 12 cajones de violines
```

#### Solución de referencia

```csharp
string barco = "Gaviota";
string carga = "violines";
int cajones = 12;
Console.WriteLine($"{barco} lleva {cajones} cajones de {carga}");
```

## R01-N02 · Tipos: cada dato en su atril

```meta
tipo: tema
padre: R01-N01
precio: 10
criatura: goblin
temas: prog.variables
usa: prog.salida
```

### Crónica

Ceci quiere anotar el precio de una cuerda nueva: «dos con cincuenta». Lo intenta en un atril de enteros, y un goblin salta del estante.

—No podés tocar un violín con un tambor —dice {mentor}—. Cada dato tiene su tipo, y cada atril acepta uno solo. C# lo revisa antes de que suene nada. Por eso me lleva bien con Kaffa, allá en el Imperio: él también hace declarar todo.

### Objetivos

- Usar `double` para decimales y `decimal` para dinero.
- Usar `bool` para verdadero o falso.
- Reconocer el error de los tipos que no encajan.
- Convertir un decimal en entero con un cast.

### Antes de empezar

- Crear variables `int` y `string` (R01-N01).

### Explicación

#### Los tipos de este nodo

| Tipo | Guarda | Ejemplo |
|---|---|---|
| `double` | números con decimales | `double tempo = 7.5;` |
| `decimal` | dinero: decimales exactos | `decimal precio = 2.50m;` |
| `bool` | verdadero o falso | `bool afinado = true;` |

Dos detalles:

- En el código, los decimales se escriben con **punto**: `7.5`. Al mostrarlos, en Argentina se ven con **coma**: `7,5`.
- Un `decimal` lleva una **`m`** al final del número: `2.50m`.

#### ¿Por qué tantos tipos?

Porque así el compilador puede avisarte antes de ejecutar. Si guardás un texto donde va un número, no arranca:

```
Programa.cs(1,12): error CS0029: No se puede convertir implícitamente el tipo 'string' en 'int'
```

Ese es **el goblin**: un tipo que no encaja.

#### Convertir: el cast

Pasar de `int` a `double` es automático: no se pierde nada. Al revés, se pueden perder decimales, y C# te pide que lo digas a propósito, poniendo el tipo entre paréntesis:

```csharp
double precio = 9.99;
int entero = (int)precio;   // 9
```

Eso se llama **cast**. **Corta** los decimales, no redondea: da 9, no 10.

### Código de ejemplo

```csharp
double tempo = 7.5;
decimal cuerda = 2.50m;
bool afinado = true;

Console.WriteLine(tempo);
Console.WriteLine(cuerda);
Console.WriteLine(afinado);
Console.WriteLine((int)tempo);
```

### Salida esperada

```
7,5
2,50
True
7
```

### ¿Para qué sirve?

En un juego, la vida puede ser `int`, la velocidad `double` y «está vivo» `bool`. En una tienda, los precios van siempre en `decimal`, para que las cuentas den exactas.

### Errores habituales

- **Olvidarse la `m` del `decimal`:** `decimal p = 2.5;` no compila.
- **Escribir el decimal con coma en el código:** `7,5` no vale; va `7.5`.
- **Esperar que el cast redondee:** `(int)9.99` da 9.

### Micro-misión R01-N02-P1 · Medio compás

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Decimales | double tempo = 7.5; · en el código se escribe con punto · al mostrarlo se ve con coma
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
—Este compás dura un tiempo y medio —explica Bemol, y lo toca en el tambor—. Con `int` no me alcanza: necesito decimales.

#### Gheco sugiere
`int` solo guarda enteros. Para números con decimales está `double`:

```csharp
double altura = 1.65;
Console.WriteLine(altura);
```

Muestra `1,65`. Fijate bien: **en el código se escribe con punto**, y en pantalla se ve con coma, porque así se escriben los decimales en Argentina.

#### Desafío
Creá una variable `double` llamada `duracion` con el valor `1.5`.

#### Código inicial
```csharp
// Creá la variable duracion acá

Console.WriteLine(duracion);
```

#### Salida esperada
```
1,5
```

#### Solución
```csharp
double duracion = 1.5;
Console.WriteLine(duracion);
```

#### Al superarla
Bemol toca un golpe largo y uno corto. Ceci lo sigue con el violín y, por primera vez, entran juntos.

#### Imagen
- Bemol toca su tambor con los palillos en alto; Ceci lo acompaña con el violín, en una sala de ensayo con velas y tubos de órgano.

### Micro-misión R01-N02-P2 · Las cuentas de Baldo

```meta
lugar: El puesto de Baldo
personajes: Ceci, Gheco
carta: Dinero | decimal precio = 2.50m; · para dinero, decimal · lleva una m al final del número
recompensa: xp 15, oro 15
```

#### Escena
Baldo, el mercader ambulante, puso su puesto en la puerta del Conservatorio. Le vende a Ceci una cuerda de violín. —Dos con cincuenta, y sin redondear —le dice—. Con la plata, nada de «más o menos».

#### Gheco sugiere
Para el dinero se usa `decimal`, porque guarda los decimales **exactos**. El número lleva una `m` al final:

```csharp
decimal entrada = 150.75m;
Console.WriteLine(entrada);
```

Muestra `150,75`. Si te olvidás la `m`, el compilador se queja: cree que es un `double`.

#### Desafío
La variable `cuerda` no compila porque al número le falta algo. Agregáselo. El precio es `2.50`.

#### Código inicial
```csharp
decimal cuerda = 2.50;
Console.WriteLine(cuerda);
```

#### Salida esperada
```
2,50
```

#### Solución
```csharp
decimal cuerda = 2.50m;
Console.WriteLine(cuerda);
```

#### Al superarla
Ceci paga justo. Baldo cuenta las monedas dos veces, le guiña un ojo y le regala un poco de resina para el arco.

#### Imagen
- Un puesto ambulante de madera junto a la escalinata de un conservatorio de piedra oscura, de noche, con cuerdas de violín colgadas y faroles.
- Ceci paga con una moneda lisa; Gheco en su hombro mira las cuerdas.

### Micro-misión R01-N02-P3 · ¿Está afinado?

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Verdadero o falso | bool afinado = true; · solo vale true o false · van sin comillas
recompensa: xp 15, oro 15
```

#### Escena
Clave pulsa una cuerda del violín de Ceci y arruga la nariz. —Hay preguntas que solo tienen dos respuestas. ¿Está afinado? Sí o no.

#### Gheco sugiere
`bool` guarda una sola cosa: verdadero o falso. Se escribe `true` o `false`, en minúscula y **sin comillas**:

```csharp
bool abierto = true;
Console.WriteLine(abierto);
```

Muestra `True`. Al mostrarlo, sale con mayúscula; en el código va en minúscula.

#### Desafío
Creá una variable `bool` llamada `afinado` que valga `false`.

#### Código inicial
```csharp
// Creá la variable afinado acá

Console.WriteLine(afinado);
```

#### Salida esperada
```
False
```

#### Solución
```csharp
bool afinado = false;
Console.WriteLine(afinado);
```

#### Al superarla
Ceci gira la clavija hasta que Clave deja de arrugar la nariz. Nadie dice nada, pero en el atril podría decir `true`.

#### Imagen
- Clave, de pie, inclinada sobre el violín que sostiene Ceci, pulsa una cuerda con un dedo y arruga la nariz.
- Ceci la mira nerviosa, en una sala de ensayo.

### Micro-misión R01-N02-P4 · El goblin del tambor

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
criatura: goblin
carta: Tipos que no encajan | CS0029: el valor no es del tipo de la variable · los números van sin comillas
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un goblin le arrebata el tambor a Bemol y lo golpea con un arco de violín. No suena nada. —¡Eso no se toca así! —grita Bemol. Es lo que pasa cuando un dato no encaja en su atril.

#### Gheco sugiere
Una variable `int` solo acepta enteros. Con comillas, `"12"` no es un número: es un **texto** que tiene dos letras. Por eso esto no compila:

```csharp
int edad = "12";
```

```
Programa.cs(1,12): error CS0029: No se puede convertir implícitamente el tipo 'string' en 'int'
```

El mensaje te dice qué tipo le diste (`string`) y cuál hacía falta (`int`).

#### Desafío
Tocá *Ejecutar* y leé el error. Después arreglá la primera línea para que `compases` guarde un número de verdad.

#### Código inicial
```csharp
int compases = "12";
Console.WriteLine(compases);
```

#### Salida esperada
```
12
```

#### Solución
```csharp
int compases = 12;
Console.WriteLine(compases);
```

#### Al superarla
El goblin suelta el tambor y se va refunfuñando. Bemol lo recupera y prueba dos golpes: suena perfecto.

#### Imagen
- Un goblin chiquito, verde, sin armas, golpea un tambor con un arco de violín, con cara de enojado.
- Bemol estira las manos para recuperar su tambor; Ceci se ríe atrás.

### Micro-misión R01-N02-P5 · Cortar el decimal

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
carta: Cast | int n = (int)9.99; · el tipo entre paréntesis convierte a propósito · corta los decimales, no redondea
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Ceci tiene 7,8 monedas de plata, pero en la ventanilla del Conservatorio solo aceptan enteras. —Te las cuentan cortando —le avisa Gheco—. Pedilo vos a propósito.

#### Gheco sugiere
Si querés guardar un `double` en un `int`, se pueden perder los decimales, así que C# te pide que lo digas a propósito. Se pone el tipo entre paréntesis, adelante:

```csharp
double nota = 9.99;
int entera = (int)nota;
Console.WriteLine(entera);
```

Muestra `9`. Se llama **cast**, y **corta** los decimales: no redondea.

#### Desafío
Completá la segunda línea con un cast, para que `enteras` guarde la parte entera de `monedas`.

#### Código inicial
```csharp
double monedas = 7.8;
int enteras = monedas;
Console.WriteLine(enteras);
```

#### Salida esperada
```
7
```

#### Solución
```csharp
double monedas = 7.8;
int enteras = (int)monedas;
Console.WriteLine(enteras);
```

#### Al superarla
—Me perdí ocho décimas —protesta Ceci. —No te las perdiste —dice Gheco—: las cortaste vos, a propósito. Clave le deja otra corchea sobre el atril.

#### Imagen
- Una ventanilla de madera dentro de un conservatorio, con un mostrador y una lámpara; Ceci apoya unas monedas lisas de plata.
- Gheco, sobre el mostrador, señala una moneda partida al medio.

### Encargo R01-N02-E1 · La factura de Baldo

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Baldo quiere una línea de factura. Creá `producto` (`Cuerda`), `cantidad` (`3`) y `precio` (`2.50`, en `decimal`). Calculá el total multiplicando cantidad por precio, con `*`, y mostralo así:

```
3 x Cuerda: 7,50
```

#### Criterio de aprobación

- `precio` y el total son `decimal`.
- El total se calcula: no está escrito a mano.

#### Salida esperada

```
3 x Cuerda: 7,50
```

#### Solución de referencia

```csharp
string producto = "Cuerda";
int cantidad = 3;
decimal precio = 2.50m;
decimal total = cantidad * precio;
Console.WriteLine($"{cantidad} x {producto}: {total}");
```

## R01-N03 · Cuentas: el reparto de las notas

```meta
tipo: tema
padre: R01-N02
precio: 10
criatura: ogro
temas: prog.operadores
usa: prog.variables, prog.salida
```

### Crónica

Clave le da a Ceci una orquesta chica para organizar: hay que repartir partituras, contar compases y calcular cuánto dura la obra. Ceci lo hace de cabeza, y le sobran tres violines.

—El **ogro** no desafina —dice {mentor}—. Toca perfecto la nota equivocada. El programa corre y el resultado está mal. A ese no te lo avisa nadie: tenés que saber qué tiene que dar.

### Objetivos

- Hacer cuentas con `+`, `-`, `*` y `/`.
- Entender la división entera.
- Usar `%` para saber cuánto sobra.
- Usar paréntesis para decidir el orden.

### Antes de empezar

- Variables `int` y `double` (R01-N01 y R01-N02).

### Explicación

#### Las cuatro cuentas

| Símbolo | Cuenta | Ejemplo | Da |
|---|---|---|---|
| `+` | suma | `7 + 2` | `9` |
| `-` | resta | `7 - 2` | `5` |
| `*` | multiplicación | `7 * 2` | `14` |
| `/` | división | `7 / 2` | `3` (¡ojo!) |
| `%` | resto | `7 % 2` | `1` |

#### La trampa de la división

Si dividís **dos enteros**, el resultado es entero: se cortan los decimales.

```csharp
Console.WriteLine(7 / 2);    // 3
Console.WriteLine(7.0 / 2);  // 3,5
```

Si al menos uno de los dos tiene decimales, el resultado también los tiene.

#### El resto: cuánto sobra

`%` no tiene nada que ver con porcentajes: da **lo que sobra** de una división entera. Si repartís 17 partituras entre 5 músicos, a cada uno le tocan `17 / 5`, o sea 3, y sobran `17 % 5`, o sea 2.

#### El orden

Como en la escuela: primero `*`, `/` y `%`; después `+` y `-`. Con paréntesis decidís vos:

```csharp
Console.WriteLine(2 + 3 * 4);    // 14
Console.WriteLine((2 + 3) * 4);  // 20
```

### Código de ejemplo

```csharp
int partituras = 17;
int musicos = 5;

Console.WriteLine($"A cada uno: {partituras / musicos}");
Console.WriteLine($"Sobran: {partituras % musicos}");
Console.WriteLine(7.0 / 2);
```

### Salida esperada

```
A cada uno: 3
Sobran: 2
3,5
```

### ¿Para qué sirve?

El daño de un golpe, el vuelto de una compra o el tiempo de una canción: casi todo programa hace cuentas. Y el `%` aparece siempre que hay que repartir, o saber si un número es par.

### Errores habituales

- **Esperar decimales de `7 / 2`:** da 3, porque los dos son enteros.
- **Olvidarse los paréntesis:** `2 + 3 * 4` no da 20.
- **Creer que `%` es un porcentaje:** es el resto.

### Micro-misión R01-N03-P1 · El total de la orquesta

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Cuentas | + suma · - resta · * multiplica · se pueden usar variables en las cuentas
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
—Somos 6 violines y 4 tambores —cuenta Bemol con los palillos—. ¿Cuántas sillas ponemos? Ceci empieza a contar con los dedos. —Dejá —le dice él—. Que lo cuente el programa.

#### Gheco sugiere
Con las variables se pueden hacer cuentas, y guardar el resultado en otra variable:

```csharp
int manzanas = 3;
int peras = 2;
int frutas = manzanas + peras;
Console.WriteLine(frutas);
```

Muestra `5`. Los símbolos son `+` para sumar, `-` para restar y `*` para multiplicar.

#### Desafío
Completá la tercera línea para que `sillas` guarde la suma de `violines` y `tambores`.

#### Código inicial
```csharp
int violines = 6;
int tambores = 4;
int sillas = 0;
Console.WriteLine(sillas);
```

#### Salida esperada
```
10
```

#### Solución
```csharp
int violines = 6;
int tambores = 4;
int sillas = violines + tambores;
Console.WriteLine(sillas);
```

#### Al superarla
Bemol pone las diez sillas en semicírculo. No sobra ninguna, y no falta ninguna.

#### Imagen
- Una sala de ensayo con diez sillas de madera en semicírculo y atriles.
- Bemol acomoda una silla; Ceci con el violín lo mira.

### Micro-misión R01-N03-P2 · El ogro de la división

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
criatura: ogro
carta: División | entre dos enteros, / corta los decimales · 7 / 2 da 3 · 7.0 / 2 da 3,5
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un ogro grandote y amable reparte 7 partituras entre 2 violines. A cada uno le da 3 y se guarda la que queda. —Tres y medio, le dije —protesta Ceci—. —Tres —contesta él, muy seguro. No hay ningún error rojo: el programa corrió bien, y el resultado está mal.

#### Gheco sugiere
Si dividís **dos enteros**, C# da un entero y corta los decimales:

```csharp
Console.WriteLine(9 / 2);
```

Muestra `4`, no 4,5. Para tener decimales, por lo menos uno de los dos números tiene que tenerlos:

```csharp
Console.WriteLine(9.0 / 2);
```

Muestra `4,5`.

#### Desafío
La cuenta da `3` y tendría que dar `3,5`. Cambiá **un solo número** para que dé con decimales.

#### Código inicial
```csharp
Console.WriteLine(7 / 2);
```

#### Salida esperada
```
3,5
```

#### Solución
```csharp
Console.WriteLine(7.0 / 2);
```

#### Al superarla
El ogro se rasca la cabeza, mira las hojas y le devuelve media partitura a cada violín. —Ah —dice—. Con coma.

#### Imagen
- Un ogro grandote y simpático de piel gris azulada, pelo naranja, nariz redonda, sin armas, sostiene una pila de hojas en blanco con cara de duda, en una sala de ensayo.
- Ceci le reclama con una mano en la cintura; Gheco en su hombro.

### Micro-misión R01-N03-P3 · Lo que sobra

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Resto | % da lo que sobra de una división entera · 17 % 5 da 2 · no es un porcentaje
recompensa: xp 15, oro 15
```

#### Escena
Hay 17 partituras para 5 músicos. —A tres cada uno —calcula Bemol—. ¿Y las que quedan? Ahí está la pregunta que nadie hace.

#### Gheco sugiere
El símbolo `%` da **lo que sobra** de una división entera. Si tenés 10 caramelos y 3 amigos, a cada uno le tocan 3 y sobra 1:

```csharp
Console.WriteLine(10 / 3);
Console.WriteLine(10 % 3);
```

Muestra `3` y después `1`. No tiene nada que ver con los porcentajes: es solo que usa el mismo dibujito.

#### Desafío
Completá la cuenta de `sobran` para que guarde cuántas partituras quedan sin repartir.

#### Código inicial
```csharp
int partituras = 17;
int musicos = 5;
int sobran = 0;
Console.WriteLine($"Sobran {sobran}");
```

#### Salida esperada
```
Sobran 2
```

#### Solución
```csharp
int partituras = 17;
int musicos = 5;
int sobran = partituras % musicos;
Console.WriteLine($"Sobran {sobran}");
```

#### Al superarla
Bemol guarda las dos partituras de más en el estante. —Para cuando entre alguien tarde —dice—. O sea, para mí.

#### Imagen
- Cinco atriles de madera con hojas en blanco, y dos hojas de más en la mano de Bemol.
- Ceci cuenta con los dedos al lado de él, en una sala de ensayo.

### Micro-misión R01-N03-P4 · Primero lo primero

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: El orden de las cuentas | primero * / %, después + - · con paréntesis decidís vos · (2 + 3) * 4 da 20
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Clave escribe una cuenta en la pizarra y le da la tiza a Ceci. —Dos ensayos de tres compases, más cuatro de la entrada, por dos funciones. ¿Cuánto? Ceci contesta rápido, y mal.

#### Gheco sugiere
Como en la escuela, primero se hacen `*`, `/` y `%`, y después `+` y `-`:

```csharp
Console.WriteLine(1 + 2 * 3);
```

Muestra `7`, porque primero hace `2 * 3`. Si querés que sume primero, usá paréntesis:

```csharp
Console.WriteLine((1 + 2) * 3);
```

Muestra `9`.

#### Desafío
La cuenta tiene que sumar primero `3 + 4` y después multiplicar por `2`. Agregá los paréntesis para que dé `14`.

#### Código inicial
```csharp
Console.WriteLine(3 + 4 * 2);
```

#### Salida esperada
```
14
```

#### Solución
```csharp
Console.WriteLine((3 + 4) * 2);
```

#### Al superarla
Clave borra la pizarra sin decir nada. Ceci ya aprendió a leer esa cara: quiere decir *bien*.

#### Imagen
- Clave de pie, frente a una pizarra grande y limpia, le extiende una tiza a Ceci.
- Ceci, con el violín colgando a la espalda, duda con un dedo en la boca. La pizarra está sin nada escrito.

### Micro-misión R01-N03-P5 · Cuánto dura la obra

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol, Gheco
carta: Juntar todo | minutos = total / 60 · segundos = total % 60 · / y % juntos sirven para repartir
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
La cajita de música suena durante 130 segundos, y después se apaga. —¿Cuántos minutos son? —pregunta Bemol. Ceci se queda mirando la cajita: ya sabe cómo sacarlo.

#### Gheco sugiere
`/` y `%` juntos sirven para **repartir**. Si tenés 25 huevos y los ponés en cajas de 12:

```csharp
int huevos = 25;
Console.WriteLine(huevos / 12);
Console.WriteLine(huevos % 12);
```

Muestra `2` (cajas llenas) y `1` (huevo que sobra). Con los segundos es igual: un minuto son 60 segundos.

#### Desafío
Completá las dos cuentas para que el programa muestre cuántos minutos y cuántos segundos dura la cajita.

#### Código inicial
```csharp
int total = 130;
int minutos = 0;
int segundos = 0;
Console.WriteLine($"{minutos} minutos y {segundos} segundos");
```

#### Salida esperada
```
2 minutos y 10 segundos
```

#### Solución
```csharp
int total = 130;
int minutos = total / 60;
int segundos = total % 60;
Console.WriteLine($"{minutos} minutos y {segundos} segundos");
```

#### Al superarla
Dos minutos y diez segundos. Clave, que pasaba por ahí, se detiene en seco. —¿Cuánto dijiste? —Y por primera vez, le pide a Ceci que le muestre la cajita.

#### Imagen
- Una cajita de música de madera abierta sobre una mesa, con su cilindro dorado.
- Clave se detiene y la mira con atención, sorprendida; Ceci y Bemol la miran a ella; Gheco sobre la tapa.

### Encargo R01-N03-E1 · El reparto de las Forjas

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Tizón, desde las Forjas de Hierro, tiene que repartir `100` lingotes entre `7` carros. Mostrá cuántos lingotes le tocan a cada carro y cuántos sobran, con este formato:

```
Cada carro: 14
Sobran: 2
```

#### Criterio de aprobación

- Usa `/` y `%`.
- Los lingotes y los carros están en variables.

#### Salida esperada

```
Cada carro: 14
Sobran: 2
```

#### Solución de referencia

```csharp
int lingotes = 100;
int carros = 7;
Console.WriteLine($"Cada carro: {lingotes / carros}");
Console.WriteLine($"Sobran: {lingotes % carros}");
```

## R01-N04 · Comparar: ¿sí o no?

```meta
tipo: tema
padre: R01-N03
precio: 10
criatura: ogro
temas: prog.operadores, prog.condicionales
usa: prog.variables, prog.salida
```

### Crónica

Clave tiene la cajita en la mano, y no la suelta. —Esta melodía dura exactamente lo mismo que una partitura que tengo guardada. Y esa partitura no está terminada.

Antes de que Ceci pueda preguntar nada, una **flecha de luz amarilla** entra por la ventana y se clava en el atril. Trae un papelito atado, y Ceci reconoce la letra: es de **Nima**, la arquera de la Feria. —Ceci: Hilván me dijo adónde fuiste. Necesito tu ayuda con las reglas del puesto de tiro.

### Objetivos

- Comparar valores con `>`, `<`, `>=`, `<=`, `==` y `!=`.
- Guardar el resultado en un `bool`.
- Pedir dos condiciones juntas con `&&`.
- Pedir una u otra con `||`.

### Antes de empezar

- El tipo `bool` (R01-N02) y las cuentas (R01-N03).

### Explicación

#### Una comparación da `true` o `false`

| Símbolo | Pregunta | Ejemplo | Da |
|---|---|---|---|
| `>` | ¿es mayor? | `5 > 3` | `true` |
| `<` | ¿es menor? | `5 < 3` | `false` |
| `>=` | ¿es mayor o igual? | `5 >= 5` | `true` |
| `<=` | ¿es menor o igual? | `5 <= 3` | `false` |
| `==` | ¿son iguales? | `5 == 5` | `true` |
| `!=` | ¿son distintos? | `5 != 3` | `true` |

**Ojo:** `=` guarda un valor, y `==` pregunta si dos cosas son iguales. Son dos cosas muy distintas.

#### Juntar condiciones

- `&&` es **«y»**: da `true` solo si las dos partes son verdaderas.
- `||` es **«o»**: da `true` si por lo menos una es verdadera.

```csharp
int edad = 14;
bool tieneEntrada = true;
Console.WriteLine(edad >= 12 && tieneEntrada);  // True
```

### Código de ejemplo

```csharp
int nivel = 6;
bool tieneLlave = true;

Console.WriteLine(nivel > 5);
Console.WriteLine(nivel == 10);
Console.WriteLine(nivel > 5 && tieneLlave);
Console.WriteLine(nivel > 10 || tieneLlave);
```

### Salida esperada

```
True
False
True
True
```

### ¿Para qué sirve?

Toda decisión de un programa arranca con una pregunta así: ¿le alcanza la plata?, ¿todavía tiene vidas?, ¿la contraseña es correcta? En los próximos nodos, esas respuestas van a decidir qué hace el programa.

### Errores habituales

- **Usar `=` en vez de `==`:** `=` guarda, `==` compara.
- **Confundir `&&` con `||`:** «y» pide las dos; «o» se conforma con una.
- **Dejar un espacio en `> =`:** el símbolo es `>=`, todo junto.

### Micro-misión R01-N04-P1 · La flecha de Nima

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Nima
carta: Comparar | 5 > 3 da True · < menor · > mayor · el resultado es un bool
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Ceci desata el papelito de la flecha. Nima le pregunta: *«¿Le alcanza el puntaje a un tirador que hizo 80? Tiene que ser más de 50»*. Ceci mira la cuenta: es una pregunta de sí o no.

#### Gheco sugiere
Una **comparación** es una pregunta que la compu contesta con `True` o `False`:

```csharp
int edad = 14;
Console.WriteLine(edad > 18);
```

Muestra `False`, porque 14 no es mayor que 18. `>` quiere decir «mayor que» y `<`, «menor que».

#### Desafío
Completá la segunda línea para que pregunte si `puntaje` es mayor que `50`.

#### Código inicial
```csharp
int puntaje = 80;
Console.WriteLine(puntaje);
```

#### Salida esperada
```
True
```

#### Solución
```csharp
int puntaje = 80;
Console.WriteLine(puntaje > 50);
```

#### Al superarla
Ceci anota la respuesta en el papelito. Lo ata a la flecha y, sin que nadie la toque, la flecha sale volando por la ventana hacia la Feria.

#### Imagen
- Una flecha de luz amarilla clavada en un atril de madera, con un papelito en blanco atado.
- Ceci desata el papelito con cara de sorpresa, en una sala de ensayo; por la ventana se ve la noche con una aurora violeta.

### Micro-misión R01-N04-P2 · Igual no es guardar

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Igual y distinto | == pregunta si son iguales · != pregunta si son distintos · = guarda un valor
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol revisa las claves de las partituras. —Esta tiene que estar en do. ¿Lo está? Ceci escribe un `=` y se le cae todo. —Ese es el de guardar —se ríe Bemol—. Para preguntar, son dos.

#### Gheco sugiere
Un solo `=` **guarda** un valor. Dos, `==`, **preguntan** si son iguales. Y `!=` pregunta si son distintos:

```csharp
int a = 3;
Console.WriteLine(a == 3);
Console.WriteLine(a != 3);
```

Muestra `True` y después `False`. También sirven con textos: `"do" == "do"` da `True`.

#### Desafío
Completá la comparación para preguntar si `nota` es igual a `"do"`.

#### Código inicial
```csharp
string nota = "do";
Console.WriteLine(nota);
```

#### Salida esperada
```
True
```

#### Solución
```csharp
string nota = "do";
Console.WriteLine(nota == "do");
```

#### Al superarla
—Dos signos para preguntar, uno para guardar —repite Ceci, y se lo anota en la mano, por las dudas.

#### Imagen
- Bemol sostiene una partitura en blanco y le señala algo a Ceci con un palillo; ella se ríe, en una sala de ensayo con velas.

### Micro-misión R01-N04-P3 · Mayor o igual

```meta
lugar: La Feria de las Luces
personajes: Ceci, Nima
carta: Mayor o igual | >= mayor o igual · <= menor o igual · van juntos, sin espacio
recompensa: xp 15, oro 15
```

#### Escena
La flecha vuelve con otra pregunta. *«Se puede entrar al puesto de tiro desde los 12 años. ¿Entra Bruno, que tiene justo 12?»* Con `>` diría que no, y Bruno se enojaría mucho.

#### Gheco sugiere
`>` no incluye al número: `12 > 12` es `False`. Para incluirlo está `>=`, «mayor o igual»:

```csharp
int altura = 150;
Console.WriteLine(altura >= 150);
```

Muestra `True`. También existe `<=`, «menor o igual». Se escriben juntos, sin espacio en el medio.

#### Desafío
La comparación da `False`, porque usa `>`. Cambiala para que `12` también pueda entrar.

#### Código inicial
```csharp
int edad = 12;
Console.WriteLine(edad > 12);
```

#### Salida esperada
```
True
```

#### Solución
```csharp
int edad = 12;
Console.WriteLine(edad >= 12);
```

#### Al superarla
En el puesto de tiro, Nima sonríe y le da a Bruno su arquito de feria. Él ya estaba protestando, y se queda sin nada que decir.

#### Imagen
- Un puesto de tiro de feria de noche, con blancos redondos de colores lisos, guirnaldas y faroles.
- Nima le entrega un arco chico a Bruno (gorra negra al revés, chaleco rojo inflado), que sonríe.

### Micro-misión R01-N04-P4 · Las dos cosas

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Y | && da True solo si las dos partes son verdaderas · edad >= 12 && tieneEntrada
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
—Para entrar al concierto —dice Clave—: tener la partitura **y** estar afinado. Las dos cosas. Una sola no alcanza, y a mí no me discutan.

#### Gheco sugiere
`&&` quiere decir **«y»**: junta dos condiciones y da `True` solo si **las dos** son verdaderas.

```csharp
bool tieneTicket = true;
bool esMayor = false;
Console.WriteLine(tieneTicket && esMayor);
```

Muestra `False`, porque una de las dos es falsa.

#### Desafío
Reemplazá el `false` de la última línea por la pregunta: si `partitura` **y** `afinado` son verdaderas las dos.

#### Código inicial
```csharp
bool partitura = true;
bool afinado = true;
Console.WriteLine(false);
```

#### Salida esperada
```
True
```

#### Solución
```csharp
bool partitura = true;
bool afinado = true;
Console.WriteLine(partitura && afinado);
```

#### Al superarla
Ceci muestra la partitura y pulsa una cuerda: suena limpia. Clave corre un paso al costado y le deja pasar a la sala del concierto.

#### Imagen
- Clave, de pie, frente a una puerta alta de madera de un conservatorio gótico, con la batuta en la mano.
- Ceci le muestra una hoja en blanco y su violín.

### Micro-misión R01-N04-P5 · Una o la otra

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol, Gheco
carta: O | || da True si por lo menos una parte es verdadera · nivel > 5 || tieneLlave
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
El depósito de Clave, donde está la partitura sin terminar, se abre con una llave **o** con el permiso de la Directora. Bemol tiene el permiso, firmado esta mañana. —Con una alcanza —dice, muy contento.

#### Gheco sugiere
`||` quiere decir **«o»**: da `True` si **por lo menos una** de las dos condiciones es verdadera. Solo da `False` si las dos son falsas.

```csharp
bool lluvia = false;
bool frio = true;
Console.WriteLine(lluvia || frio);
```

Muestra `True`. El símbolo `|` se escribe dos veces. Según el teclado, sale con la tecla a la izquierda del 1 o con AltGr y el 1.

#### Desafío
Completá la línea para preguntar si tiene `llave` **o** `permiso`.

#### Código inicial
```csharp
bool llave = false;
bool permiso = true;
Console.WriteLine(llave);
```

#### Salida esperada
```
True
```

#### Solución
```csharp
bool llave = false;
bool permiso = true;
Console.WriteLine(llave || permiso);
```

#### Al superarla
La puerta del depósito se abre. Adentro, sobre un atril solo, hay una partitura vieja con una etiqueta: *«para quien llegue»*. Es la misma letra que la de la cajita. Ceci la toma con las dos manos, y le tiemblan.

#### Imagen
- Un depósito oscuro de piedra lisa, con un solo atril iluminado por un farol y, encima, una partitura vieja cerrada con una cinta.
- Ceci y Bemol miran desde la puerta abierta, asombrados; Gheco sobre el hombro de Bemol.

### Encargo R01-N04-E1 · Las reglas del puesto de tiro

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Nima quiere las reglas de su puesto de tiro en un programa. Con `edad` (`14`), `tieneFicha` (`true`) y `puntaje` (`35`), mostrá:

- si puede jugar: tiene `12` años o más **y** tiene ficha;
- si gana un premio: su puntaje es mayor que `30` **o** tiene exactamente `100`.

```
Puede jugar: True
Gana premio: True
```

#### Criterio de aprobación

- Usa `&&` en la primera regla y `||` en la segunda.
- Los datos están en variables.

#### Salida esperada

```
Puede jugar: True
Gana premio: True
```

#### Solución de referencia

```csharp
int edad = 14;
bool tieneFicha = true;
int puntaje = 35;
Console.WriteLine($"Puede jugar: {edad >= 12 && tieneFicha}");
Console.WriteLine($"Gana premio: {puntaje > 30 || puntaje == 100}");
```
