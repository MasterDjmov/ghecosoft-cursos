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

## R01-N05 · Textos: las letras de la partitura

```meta
tipo: tema
padre: R01-N04
precio: 10
criatura: orco
temas: prog.cadenas
usa: prog.variables, prog.salida
```

### Crónica

Clave abre un cajón lleno de partituras viejas. Las etiquetas están escritas de cualquier manera: unas en mayúsculas, otras con espacios de más, otras con el nombre de la obra pegado al del compositor.

—Una partitura empieza por su nombre —dice {mentor}—. Si el nombre está mal escrito, nadie la encuentra. Vamos a aprender a leer y arreglar textos, letra por letra.

### Objetivos

- Saber cuántas letras tiene un texto con `Length`.
- Tomar una letra por su posición: la primera es la `0`.
- Pasar a mayúsculas o minúsculas, y sacar los espacios de los costados.
- Buscar y reemplazar dentro de un texto.

### Antes de empezar

- Las variables `string` (R01-N01).

### Explicación

#### Un texto es una fila de letras

Cada letra tiene su lugar, y **el primer lugar es el 0**:

| Letra | `C` | `e` | `c` | `i` |
|---|---|---|---|---|
| Lugar | 0 | 1 | 2 | 3 |

```csharp
string nombre = "Ceci";
Console.WriteLine(nombre.Length);   // 4: cuántas letras tiene
Console.WriteLine(nombre[0]);       // C: la primera
Console.WriteLine(nombre[^1]);      // i: la última (^1 quiere decir «la primera desde el final»)
```

#### Los textos no cambian: dan uno nuevo

`ToUpper()` no cambia el texto que tenés: te **devuelve otro**, en mayúsculas. Si querés quedártelo, lo guardás.

| Método | Qué devuelve | Ejemplo |
|---|---|---|
| `ToUpper()` | todo en mayúsculas | `"la".ToUpper()` da `"LA"` |
| `ToLower()` | todo en minúsculas | `"LA".ToLower()` da `"la"` |
| `Trim()` | sin los espacios de los costados | `"  do  ".Trim()` da `"do"` |
| `Contains("x")` | `True` si lo tiene adentro | `"do re mi".Contains("re")` da `True` |
| `Replace("a", "b")` | cambia cada `a` por `b` | `"do re".Replace("re", "mi")` da `"do mi"` |

### Código de ejemplo

```csharp
string obra = "  la cajita  ";
string limpia = obra.Trim();

Console.WriteLine(limpia);
Console.WriteLine(limpia.Length);
Console.WriteLine(limpia.ToUpper());
Console.WriteLine(limpia[0]);
Console.WriteLine(limpia.Contains("ita"));
Console.WriteLine(limpia.Replace("cajita", "partitura"));
```

### Salida esperada

```
la cajita
9
LA CAJITA
l
True
la partitura
```

### ¿Para qué sirve?

Casi todo lo que escribe una persona llega como texto: nombres, contraseñas, búsquedas. Antes de usarlo hay que limpiarlo y compararlo bien: «Ceci», «ceci» y « Ceci » tienen que ser la misma alumna.

### Errores habituales

- **Contar desde 1:** la primera letra es `[0]`, y la última es `[Length - 1]` o `[^1]`.
- **Pedir una letra que no existe:** `"Ceci"[4]` corta el programa con `IndexOutOfRangeException` (el **orco** de las posiciones).
- **Creer que `ToUpper()` cambia la variable:** devuelve un texto nuevo; si no lo guardás, se pierde.

### Micro-misión R01-N05-P1 · Cuántas letras

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Length | texto.Length = cuántas letras tiene · los espacios también cuentan
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Clave quiere etiquetas que entren en el atril: ninguna puede tener más de 12 letras. Ceci tiene que contar las de «Serenata».

#### Gheco sugiere
`Length` te dice cuántas letras tiene un texto. Va **sin paréntesis**, pegado con un punto:

```csharp
string fruta = "manzana";
Console.WriteLine(fruta.Length);
```

Muestra `7`. Los espacios también cuentan como letras.

#### Desafío
Mostrá cuántas letras tiene `obra`.

#### Código inicial
```csharp
string obra = "Serenata";
Console.WriteLine(obra);
```

#### Salida esperada
```
8
```

#### Solución
```csharp
string obra = "Serenata";
Console.WriteLine(obra.Length);
```

#### Al superarla
—Ocho: entra de sobra —dice Clave, y le pasa la siguiente etiqueta.

#### Imagen
- Un atril de madera con una etiqueta de papel en blanco, y al lado un montón de partituras viejas atadas con cinta.
- Ceci cuenta con los dedos mientras Clave la mira con los brazos cruzados, en una sala de ensayo con velas.

### Micro-misión R01-N05-P2 · La primera letra

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Posición | texto[0] = la primera letra · texto[^1] = la última · se cuenta desde 0
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol ordena las partituras por la primera letra del compositor. Le pide a Ceci que le diga con qué letra empieza y con cuál termina «Vivaldi».

#### Gheco sugiere
Entre corchetes pedís la letra de un lugar. **El primer lugar es el 0**, y `^1` es el último:

```csharp
string animal = "gato";
Console.WriteLine(animal[0]);
Console.WriteLine(animal[^1]);
```

Muestra `g` y después `o`.

#### Desafío
Mostrá la primera letra de `autor` y, en la línea siguiente, la última.

#### Código inicial
```csharp
string autor = "Vivaldi";
Console.WriteLine(autor);
```

#### Salida esperada
```
V
i
```

#### Solución
```csharp
string autor = "Vivaldi";
Console.WriteLine(autor[0]);
Console.WriteLine(autor[^1]);
```

#### Al superarla
Bemol pone la partitura en la pila de la «V». —¿Y por qué se cuenta desde cero? —pregunta, como siempre.

#### Imagen
- Pilas de partituras sobre una mesa larga, cada pila con un separador de madera liso.
- Bemol, con su tambor colgado, sostiene una partitura y mira a Ceci, que señala la pila correcta.

### Micro-misión R01-N05-P3 · Limpiar la etiqueta

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
carta: Trim y ToUpper | Trim() saca los espacios de los costados · ToUpper() pasa a mayúsculas · devuelven un texto NUEVO
recompensa: xp 15, oro 15
```

#### Escena
Una etiqueta vieja dice «   minueto   », con espacios de más y en minúscula. Clave quiere las etiquetas limpias y en mayúsculas.

#### Gheco sugiere
Los métodos de texto se pueden **encadenar**: el resultado de uno pasa al siguiente.

```csharp
string saludo = "  hola  ";
Console.WriteLine(saludo.Trim().ToUpper());
```

Muestra `HOLA`: primero `Trim()` saca los espacios y después `ToUpper()` lo pasa a mayúsculas.

#### Desafío
Mostrá `etiqueta` sin los espacios de los costados y en mayúsculas.

#### Código inicial
```csharp
string etiqueta = "   minueto   ";
Console.WriteLine(etiqueta);
```

#### Salida esperada
```
MINUETO
```

#### Solución
```csharp
string etiqueta = "   minueto   ";
Console.WriteLine(etiqueta.Trim().ToUpper());
```

#### Al superarla
La etiqueta queda prolija. Gheco, sentado arriba del atril, aplaude con la cola.

#### Imagen
- Una etiqueta de papel pegada en el lomo de una carpeta de partituras, sin nada escrito a la vista.
- Gheco, sentado en el borde de un atril, mira cómo Ceci alisa la etiqueta con la mano.

### Micro-misión R01-N05-P4 · ¿Está en la partitura?

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Contains | texto.Contains("x") = True si x está adentro · distingue mayúsculas
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Clave busca una partitura que tenga la nota «sol». Ceci tiene la lista de notas de una obra y tiene que contestar sí o no.

#### Gheco sugiere
`Contains` pregunta si un texto está **adentro** de otro, y contesta `True` o `False`:

```csharp
string frase = "el gato duerme";
Console.WriteLine(frase.Contains("gato"));
Console.WriteLine(frase.Contains("perro"));
```

Muestra `True` y después `False`. Ojo: `"Gato"` con mayúscula no lo encontraría.

#### Desafío
Mostrá si `notas` tiene adentro la palabra `"sol"`.

#### Código inicial
```csharp
string notas = "do re mi fa sol la";
Console.WriteLine(notas);
```

#### Salida esperada
```
True
```

#### Solución
```csharp
string notas = "do re mi fa sol la";
Console.WriteLine(notas.Contains("sol"));
```

#### Al superarla
—Esa es —dice Clave, y la separa del resto.

#### Imagen
- Una partitura abierta sobre un atril, con pentagramas y notas dibujadas, sin letras.
- Clave, con sus anteojos redondos, sigue las notas con el dedo mientras Ceci espera la respuesta.

### Micro-misión R01-N05-P5 · El orco de la letra que no existe

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
criatura: orco
carta: Fuera de rango | texto[texto.Length] no existe · la última es texto[texto.Length - 1] · IndexOutOfRangeException
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un orco chiquito se metió en el cajón de las etiquetas. Cada vez que alguien pide una letra que no existe, rompe el programa. Esta vez alguien quiso mostrar la letra del lugar 5 de «Tango», que tiene 5 letras.

#### Gheco sugiere
Si un texto tiene 5 letras, sus lugares van del **0 al 4**. Pedir el lugar 5 corta el programa con `IndexOutOfRangeException`. La última letra está en `Length - 1`:

```csharp
string flor = "rosa";
Console.WriteLine(flor[flor.Length - 1]);
```

Muestra `a`, la última.

#### Desafío
Ejecutalo y mirá el error del orco. Después arreglalo para que muestre la última letra de `danza`, usando `Length - 1`.

#### Código inicial
```csharp
string danza = "Tango";
Console.WriteLine(danza[danza.Length]);
```

#### Salida esperada
```
o
```

#### Solución
```csharp
string danza = "Tango";
Console.WriteLine(danza[danza.Length - 1]);
```

#### Al superarla
El orco se queda sin letras para romper y sale corriendo por debajo de la puerta.

#### Imagen
- Un cajón de madera abierto, lleno de etiquetas de papel en blanco desparramadas.
- Un orco verde chiquito y gruñón sale corriendo del cajón mientras Gheco lo señala, sin sangre ni armas.

### Encargo R01-N05-E1 · El cartel de Baldo

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Baldo, el mercader del Valle, escribió el cartel de su puesto apurado: `"  frutas frescas  "`. Con ese texto en una variable, mostrá:

- el cartel limpio y en mayúsculas;
- cuántas letras tiene el cartel limpio;
- su primera letra;
- si dice `"frescas"`.

```
FRUTAS FRESCAS
14
f
True
```

#### Criterio de aprobación

- Usa `Trim()`, `ToUpper()`, `Length`, una posición con corchetes y `Contains`.
- El texto está en una variable.

#### Salida esperada

```
FRUTAS FRESCAS
14
f
True
```

#### Solución de referencia

```csharp
string cartel = "  frutas frescas  ";
string limpio = cartel.Trim();
Console.WriteLine(limpio.ToUpper());
Console.WriteLine(limpio.Length);
Console.WriteLine(limpio[0]);
Console.WriteLine(limpio.Contains("frescas"));
```

## R01-N06 · Cortar, partir y dar formato

```meta
tipo: tema
padre: R01-N05
precio: 10
criatura: goblin
temas: prog.cadenas, prog.salida
usa: prog.variables
```

### Crónica

En la última hoja de la partitura sin terminar hay una sola línea: *do-re-mi-fa-sol*. Clave dice que es el comienzo de la melodía de la cajita, y que hay que separar cada nota para ensayarlas de a una.

—Un texto largo se corta en pedazos —dice {mentor}—, y los pedazos se vuelven a juntar como uno quiera. Y cuando muestres números, que se vean prolijos.

### Objetivos

- Tomar un pedazo de un texto con `Substring`.
- Partir un texto en pedazos con `Split` y volver a unirlos con `string.Join`.
- Mostrar números con dos decimales o de un ancho fijo.
- Escribir comillas, tabulaciones y rutas dentro de un texto.

### Antes de empezar

- Las posiciones de un texto (R01-N05).

### Explicación

#### Cortar un pedazo

`Substring(desde, cuántas)` te da `cuántas` letras a partir del lugar `desde`:

```csharp
string obra = "Gran Serenata";
Console.WriteLine(obra.Substring(5, 8));   // Serenata
```

#### Partir y unir

`Split('-')` parte el texto cada vez que encuentra un `-`, y te da los pedazos en una **lista** (un arreglo, que vas a ver en detalle más adelante). `string.Join` hace lo contrario:

```csharp
string[] notas = "do-re-mi".Split('-');
Console.WriteLine(notas.Length);              // 3
Console.WriteLine(notas[1]);                  // re
Console.WriteLine(string.Join(" ", notas));   // do re mi
```

#### Formato dentro de `{ }`

En un texto con `$`, después del valor podés poner **dos puntos** y un formato:

| Formato | Qué hace | Ejemplo | Da |
|---|---|---|---|
| `{x:F2}` | dos decimales | `{7.5:F2}` | `7,50` |
| `{x:D3}` | rellena con ceros hasta 3 cifras | `{7:D3}` | `007` |
| `{x,6}` | ancho 6, a la derecha | `{42,6}` | `    42` |
| `{x,-6}` | ancho 6, a la izquierda | `{"do",-6}` | `do    ` |

Los decimales salen con **coma**, como en una compu de acá.

#### Caracteres especiales

| Escribís | Aparece |
|---|---|
| `\"` | una comilla dentro del texto |
| `\t` | un salto hasta la columna siguiente (tabulación) |
| `\n` | una línea nueva |

Con `@` adelante, la barra `\` se escribe tal cual: `@"C:\Partituras"`. Sirve para rutas de Windows.

### Código de ejemplo

```csharp
string linea = "do-re-mi-fa-sol";
string[] notas = linea.Split('-');

Console.WriteLine(notas.Length);
Console.WriteLine(notas[4]);
Console.WriteLine(string.Join(" ", notas));
Console.WriteLine(linea.Substring(0, 5));

double precio = 12.5;
Console.WriteLine($"Precio: {precio:F2}");
Console.WriteLine($"Partitura n.º {7:D3}");
Console.WriteLine("Ceci dijo: \"¡ya!\"");
```

### Salida esperada

```
5
sol
do re mi fa sol
do-re
Precio: 12,50
Partitura n.º 007
Ceci dijo: "¡ya!"
```

### ¿Para qué sirve?

Los datos viajan muchas veces en una sola línea separada por comas o guiones (una planilla, un mensaje). Partirla es lo primero que hace cualquier programa que la lee. Y un número con formato (`$ 12,50` y no `12,5`) es la diferencia entre un recibo prolijo y uno que confunde.

### Errores habituales

- **Pasarse en `Substring`:** si pedís más letras de las que hay, sale `ArgumentOutOfRangeException`.
- **Partir por el separador equivocado:** si la línea usa `-` y partís por `,`, te queda un solo pedazo.
- **Olvidar la `@` en una ruta:** sin ella, `"C:\nueva"` tiene un `\n` (línea nueva) escondido.

### Micro-misión R01-N06-P1 · Un pedazo de la obra

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Substring | texto.Substring(desde, cuántas) · desde se cuenta desde 0
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
La obra se llama «Nocturno en Do». Clave solo quiere la palabra «Nocturno» para el programa del concierto.

#### Gheco sugiere
`Substring(desde, cuántas)` corta un pedazo: arranca en el lugar `desde` (contando desde 0) y toma `cuántas` letras.

```csharp
string ciudad = "Buenos Aires";
Console.WriteLine(ciudad.Substring(7, 5));
```

Muestra `Aires`: arranca en el lugar 7 y toma 5 letras.

#### Desafío
Mostrá solo la palabra `Nocturno`, que son las primeras 8 letras de `obra`.

#### Código inicial
```csharp
string obra = "Nocturno en Do";
Console.WriteLine(obra);
```

#### Salida esperada
```
Nocturno
```

#### Solución
```csharp
string obra = "Nocturno en Do";
Console.WriteLine(obra.Substring(0, 8));
```

#### Al superarla
Clave anota «Nocturno» en el programa del concierto, con letra prolija.

#### Imagen
- Un programa de concierto doblado sobre un atril, en blanco, con un lápiz al lado.
- Clave escribe en el programa mientras Ceci le muestra la partitura.

### Micro-misión R01-N06-P2 · Separar las notas

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Split | texto.Split('-') parte en cada guion · da una lista · lista.Length = cuántos pedazos
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
La línea de la partitura sin terminar dice `do-re-mi-fa-sol`. Bemol quiere saber cuántas notas son y cuál es la tercera.

#### Gheco sugiere
`Split` parte un texto cada vez que encuentra el separador, y te da los pedazos. Se piden igual que las letras: el primero es el `[0]`.

```csharp
string[] frutas = "pera,uva,kiwi".Split(',');
Console.WriteLine(frutas.Length);
Console.WriteLine(frutas[0]);
```

Muestra `3` y después `pera`. El separador va entre comillas **simples**, porque es una sola letra.

#### Desafío
Partí `linea` por el `-` y mostrá cuántas notas hay y, en la línea siguiente, la tercera nota.

#### Código inicial
```csharp
string linea = "do-re-mi-fa-sol";
Console.WriteLine(linea);
```

#### Salida esperada
```
5
mi
```

#### Solución
```csharp
string linea = "do-re-mi-fa-sol";
string[] notas = linea.Split('-');
Console.WriteLine(notas.Length);
Console.WriteLine(notas[2]);
```

#### Al superarla
—Cinco notas, y la tercera es mi —repite Bemol—. ¿Y por qué la tercera es el dos?

#### Imagen
- Cinco tarjetas de cartón en fila sobre una mesa, cada una con una nota musical dibujada.
- Bemol, con su tambor colgado, señala la tercera tarjeta; Ceci lo mira divertida.

### Micro-misión R01-N06-P3 · Volver a unir

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: string.Join | string.Join(" ", lista) une los pedazos con lo que pongas en el medio
recompensa: xp 15, oro 15
```

#### Escena
Clave prefiere las notas separadas por un espacio, no por guiones. Ceci ya las tiene partidas en una lista.

#### Gheco sugiere
`string.Join(separador, lista)` es lo contrario de `Split`: junta los pedazos poniendo el separador entre cada uno.

```csharp
string[] dias = { "lunes", "martes" };
Console.WriteLine(string.Join(" y ", dias));
```

Muestra `lunes y martes`.

#### Desafío
Mostrá las notas unidas con un espacio entre cada una.

#### Código inicial
```csharp
string[] notas = "do-re-mi-fa-sol".Split('-');
Console.WriteLine(notas[0]);
```

#### Salida esperada
```
do re mi fa sol
```

#### Solución
```csharp
string[] notas = "do-re-mi-fa-sol".Split('-');
Console.WriteLine(string.Join(" ", notas));
```

#### Al superarla
Clave copia la línea en un papel nuevo. —Así se lee mucho mejor.

#### Imagen
- Una hoja de pentagrama nueva sobre un atril, con cinco notas dibujadas en fila, sin letras.
- Clave sostiene la hoja con una sonrisa leve y Ceci la mira desde el costado.

### Micro-misión R01-N06-P4 · El precio prolijo

```meta
lugar: El puesto de Baldo
personajes: Ceci, Gheco
carta: Formato | {x:F2} = dos decimales · {x:D3} = rellena con ceros · los decimales salen con coma
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Baldo vende cuerdas de violín a 3,5 monedas, pero su cartel dice «3,5» y él quiere que diga «3,50», como los precios de verdad.

#### Gheco sugiere
Adentro de `{ }`, después del valor, poné `:F2` para mostrar siempre **dos decimales**:

```csharp
double altura = 1.8;
Console.WriteLine($"Mide {altura:F2} m");
```

Muestra `Mide 1,80 m`. Los decimales salen con coma, como en una compu de acá.

#### Desafío
Mostrá `Cuerda: 3,50` usando el formato de dos decimales con la variable `precio`.

#### Código inicial
```csharp
double precio = 3.5;
Console.WriteLine($"Cuerda: {precio}");
```

#### Salida esperada
```
Cuerda: 3,50
```

#### Solución
```csharp
double precio = 3.5;
Console.WriteLine($"Cuerda: {precio:F2}");
```

#### Al superarla
Baldo pega el cartel nuevo y saca pecho. —Ahora sí parece un puesto serio.

#### Imagen
- Un puesto de mercado con un toldo a rayas, rollos de cuerdas de violín y un cartel de madera liso, sin letras.
- Gheco, sobre el mostrador, mira a Ceci que pega el cartel.

### Micro-misión R01-N06-P5 · El goblin de las comillas

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
criatura: goblin
carta: Comillas adentro | \" = una comilla dentro del texto · sin la barra, el texto se corta
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un goblin cambió el cartel de la sala: quiere que diga *Clave dijo: "silencio"*, pero puso las comillas sin la barra y el programa no compila.

#### Gheco sugiere
Una comilla `"` **cierra** el texto. Para escribir una comilla adentro, poné una barra antes: `\"`.

```csharp
Console.WriteLine("Le dicen \"el Rápido\"");
```

Muestra `Le dicen "el Rápido"`.

#### Desafío
Ejecutalo y mirá el error del goblin. Después arreglalo con `\"` para que muestre las comillas.

#### Código inicial
```csharp
Console.WriteLine("Clave dijo: "silencio"");
```

#### Salida esperada
```
Clave dijo: "silencio"
```

#### Solución
```csharp
Console.WriteLine("Clave dijo: \"silencio\"");
```

#### Al superarla
El cartel queda bien, y el goblin, sin comillas para robar, se esconde atrás del órgano.

#### Imagen
- Un cartel de madera liso colgado de la puerta de una sala de ensayo, sin letras.
- Un goblin verde chiquito, con cara de travieso, espía detrás de los tubos dorados de un órgano; Gheco lo descubre.

### Encargo R01-N06-E1 · La lista del Puerto

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Nilo trae del Puerto una línea con los paquetes del día: `"violín,arco,resina"`. Mostrá:

- cuántos paquetes son;
- cada paquete en mayúsculas, unidos con ` / `;
- el precio total, `12.5`, con dos decimales.

```
Paquetes: 3
VIOLÍN / ARCO / RESINA
Total: 12,50
```

#### Criterio de aprobación

- Usa `Split` y `string.Join`.
- Muestra el total con el formato `F2`.

#### Salida esperada

```
Paquetes: 3
VIOLÍN / ARCO / RESINA
Total: 12,50
```

#### Solución de referencia

```csharp
string linea = "violín,arco,resina";
string[] paquetes = linea.ToUpper().Split(',');
double total = 12.5;
Console.WriteLine($"Paquetes: {paquetes.Length}");
Console.WriteLine(string.Join(" / ", paquetes));
Console.WriteLine($"Total: {total:F2}");
```

## R01-N07 · Leer y validar: lo que escribe el público

```meta
tipo: tema
padre: R01-N06
precio: 10
criatura: goblin
temas: prog.entrada
usa: prog.variables, prog.salida, prog.cadenas
```

### Crónica

Clave abre las puertas del ensayo abierto: el público puede pedir la obra que quiere escuchar. Algunos escriben bien el pedido, otros ponen cualquier cosa.

—Hasta ahora, los datos los escribías vos en el programa —dice {mentor}—. Ahora los va a escribir otro. Y el que escribe se equivoca: hay que preguntar, leer y **revisar** antes de usar.

### Objetivos

- Leer lo que se escribe con `Console.ReadLine()`.
- Hacer la pregunta en la misma línea con `Console.Write`.
- Convertir el texto leído en número con `int.Parse`.
- Revisar si se puede convertir, sin que el programa se rompa, con `int.TryParse`.

### Antes de empezar

- Los textos (R01-N05) y los tipos (R01-N02).

### Explicación

#### Leer una línea

`Console.ReadLine()` espera a que alguien escriba y toque Enter, y te da lo que escribió **como texto**. El `?? ""` del final quiere decir «y si no escribió nada, usá un texto vacío»: ponelo siempre, después lo vas a entender del todo.

```csharp
Console.Write("¿Cómo te llamás? ");
string nombre = Console.ReadLine() ?? "";
Console.WriteLine($"Hola, {nombre}");
```

`Console.Write` muestra la pregunta **sin** pasar a la línea siguiente. Acá, en el navegador, lo que se «tipea» sale de la caja **Entrada**, y no se ve en la salida: por eso la respuesta aparece pegada a la pregunta, como cuando la entrada viene de un archivo.

#### Lo leído es texto

Aunque escriban `15`, `ReadLine` te da el texto `"15"`. Para hacer cuentas, se convierte:

```csharp
int edad = int.Parse("15");     // 15, ahora sí un número
```

Si escriben `quince`, `int.Parse` rompe el programa con `FormatException` (el **goblin** de los tipos).

#### Revisar antes de convertir

`int.TryParse` **intenta** convertir y no se rompe nunca: contesta `True` si pudo y deja el número en la variable que pongas después de `out`.

```csharp
bool pudo = int.TryParse("quince", out int numero);
Console.WriteLine(pudo);      // False
Console.WriteLine(numero);    // 0
```

En el próximo nodo vas a decidir qué hacer en cada caso con `if`.

### Código de ejemplo

```csharp
Console.Write("¿Qué obra querés? ");
string obra = Console.ReadLine() ?? "";
Console.Write("¿Cuántas veces? ");
int veces = int.Parse(Console.ReadLine() ?? "");

Console.WriteLine($"Vamos a tocar {obra} {veces} veces.");

bool esNumero = int.TryParse("diez", out int n);
Console.WriteLine(esNumero);
```

### Entrada de ejemplo

```
Serenata
2
```

### Salida esperada

```
¿Qué obra querés? ¿Cuántas veces? Vamos a tocar Serenata 2 veces.
False
```

### ¿Para qué sirve?

Todo programa que se usa de verdad pregunta algo: un nombre, una cantidad, una opción del menú. Y la regla de oro es **no confiar** en lo que escriben: revisar antes de usar evita que el programa se caiga delante del público.

### Errores habituales

- **Hacer cuentas con el texto:** `"2" + 1` da `"21"`, no `3`. Primero convertí.
- **Usar `int.Parse` con algo que no es número:** el goblin de `FormatException` corta el programa. Si no estás seguro, usá `TryParse`.
- **Olvidar el `out`:** `int.TryParse(texto, numero)` no compila; va `out int numero`.

### Micro-misión R01-N07-P1 · El nombre del público

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: ReadLine | Console.ReadLine() ?? "" = lo que escribieron, como texto · espera el Enter
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
El primero en la fila del ensayo abierto dice su nombre. Ceci tiene que saludarlo por el nombre que escribió.

#### Gheco sugiere
`Console.ReadLine()` te da lo que se escribió. Acá, lo que se escribe sale de la caja **Entrada**.

```csharp
string color = Console.ReadLine() ?? "";
Console.WriteLine($"Te gusta el {color}");
```

Si en la Entrada dice `azul`, muestra `Te gusta el azul`.

#### Desafío
Leé el nombre con `ReadLine` y guardalo en `nombre`, en lugar del texto fijo. Así saluda a cualquiera.

#### Código inicial
```csharp
string nombre = "nadie";
Console.WriteLine($"¡Bienvenido, {nombre}!");
```

#### Entrada
```
Tano
```

#### Salida esperada
```
¡Bienvenido, Tano!
```

#### Solución
```csharp
string nombre = Console.ReadLine() ?? "";
Console.WriteLine($"¡Bienvenido, {nombre}!");
```

#### Al superarla
Don Tano, el organillero de la Feria, saluda con el sombrero. Vino a escuchar a Ceci.

#### Imagen
- La puerta de una sala de ensayo abierta, con una fila de público esperando a la luz de las velas.
- Ceci saluda con la mano a un abuelo de sombrero de copa y bigote blanco, mientras Clave mira desde atrás.

### Micro-misión R01-N07-P2 · La pregunta en la misma línea

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Write | Console.Write = muestra sin pasar de línea · ideal para preguntar
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol quiere que la pregunta quede escrita y que la respuesta aparezca al lado, como en un formulario.

#### Gheco sugiere
`Console.Write` muestra el texto **y se queda en la misma línea**. `WriteLine` pasa a la línea siguiente.

```csharp
Console.Write("Uno, ");
Console.WriteLine("dos.");
```

Muestra `Uno, dos.` en una sola línea. Lo que se lee de la Entrada no se ve en la salida.

#### Desafío
Cambiá el primer `WriteLine` por `Write`, para que la pregunta y la respuesta queden en la misma línea.

#### Código inicial
```csharp
Console.WriteLine("¿Instrumento? ");
string instrumento = Console.ReadLine() ?? "";
Console.WriteLine($"Elegiste {instrumento}");
```

#### Entrada
```
flauta
```

#### Salida esperada
```
¿Instrumento? Elegiste flauta
```

#### Solución
```csharp
Console.Write("¿Instrumento? ");
string instrumento = Console.ReadLine() ?? "";
Console.WriteLine($"Elegiste {instrumento}");
```

#### Al superarla
—¿Y por qué no se ve lo que escribí? —pregunta Bemol. —Porque lo escribiste vos, no el programa —le contesta Ceci.

#### Imagen
- Un formulario de papel en blanco sobre un atril, con una pluma al lado.
- Bemol se rasca la cabeza mirando el formulario; Ceci le explica con las manos.

### Micro-misión R01-N07-P3 · De texto a número

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: int.Parse | int.Parse("15") = 15 · lo leído es texto: para hacer cuentas, convertí
recompensa: xp 15, oro 15
```

#### Escena
Una señora pide la obra «para mi nieta, que cumple 9». Clave quiere tocarla tantas veces como años cumple más uno, «para que crezca».

#### Gheco sugiere
`ReadLine` te da texto. Para sumar, convertí con `int.Parse`:

```csharp
int dulces = int.Parse(Console.ReadLine() ?? "");
Console.WriteLine(dulces * 2);
```

Si en la Entrada dice `4`, muestra `8`.

#### Desafío
Convertí lo leído con `int.Parse` para que la suma dé un número. Ahora pega el texto `"9"` con el `1`.

#### Código inicial
```csharp
string anios = Console.ReadLine() ?? "";
Console.WriteLine(anios + 1);
```

#### Entrada
```
9
```

#### Salida esperada
```
10
```

#### Solución
```csharp
int anios = int.Parse(Console.ReadLine() ?? "");
Console.WriteLine(anios + 1);
```

#### Al superarla
—Diez veces, entonces —dice Clave, y la señora aplaude como si ya hubiera terminado el concierto.

#### Imagen
- Un pastel de cumpleaños chiquito con velitas, sobre una mesa al costado de los atriles.
- Clave saluda a una señora mayor con un pañuelo en la cabeza; Ceci ya tiene el violín en el hombro.

### Micro-misión R01-N07-P4 · ¿Se puede convertir?

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
carta: TryParse | int.TryParse(texto, out int n) = True si pudo · deja el número en n · no se rompe
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Alguien del público escribió «muchas» donde iba la cantidad de veces. Antes de usarlo, Ceci quiere saber si es un número.

#### Gheco sugiere
`int.TryParse` **prueba** convertir y te contesta `True` o `False`, sin romperse. Si pudo, el número queda en la variable del `out`:

```csharp
bool ok = int.TryParse("8", out int cantidad);
Console.WriteLine(ok);
Console.WriteLine(cantidad);
```

Muestra `True` y `8`.

#### Desafío
Mostrá si `pedido` se puede convertir en número, usando `int.TryParse`.

#### Código inicial
```csharp
string pedido = Console.ReadLine() ?? "";
Console.WriteLine(pedido);
```

#### Entrada
```
muchas
```

#### Salida esperada
```
False
```

#### Solución
```csharp
string pedido = Console.ReadLine() ?? "";
bool esNumero = int.TryParse(pedido, out int veces);
Console.WriteLine(esNumero);
```

#### Al superarla
—«Muchas» no es un número —dice Ceci—, pero lo tomo como un cumplido.

#### Imagen
- Un papelito de pedido sobre un atril, con garabatos ilegibles, sin letras claras.
- Gheco, arriba del atril, mira el papelito con una lupa; Ceci se ríe.

### Micro-misión R01-N07-P5 · El goblin del número escrito

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
criatura: goblin
carta: FormatException | int.Parse("tres") rompe el programa · si puede venir cualquier cosa, TryParse
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
El goblin de los tipos escribió «tres» en la cantidad, para ver caer el programa. Con `int.Parse` cae. Con `TryParse`, no.

#### Gheco sugiere
`int.Parse` con algo que no es un número corta todo con `FormatException`. `TryParse` en cambio deja `0` en el número y sigue.

```csharp
int.TryParse("hola", out int n);
Console.WriteLine(n);
```

Muestra `0`, sin romperse.

#### Desafío
Ejecutalo y mirá el error del goblin. Después cambiá `int.Parse` por `int.TryParse` con `out int sillas`, para que el programa siga y muestre `Sillas: 0`.

#### Código inicial
```csharp
string texto = Console.ReadLine() ?? "";
int sillas = int.Parse(texto);
Console.WriteLine($"Sillas: {sillas}");
```

#### Entrada
```
tres
```

#### Salida esperada
```
Sillas: 0
```

#### Solución
```csharp
string texto = Console.ReadLine() ?? "";
int.TryParse(texto, out int sillas);
Console.WriteLine($"Sillas: {sillas}");
```

#### Al superarla
El programa sigue de pie, y el goblin, aburrido, se va a molestar a otra sala.

#### Imagen
- Una fila de sillas de madera vacías frente a un escenario chico, a la luz de faroles.
- Un goblin verde chiquito y travieso se aleja con los brazos cruzados; Gheco lo mira desde una silla.

### Encargo R01-N07-E1 · La ficha del Gremio

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

El Gremio quiere una ficha para cada músico que llega. Preguntá el nombre y la edad, en la misma línea que la pregunta, y mostrá la ficha con la edad que va a tener el año que viene. Con la Entrada `Ceci` y `15`:

```
Nombre: Edad: Ficha de Ceci: el año que viene cumple 16.
```

#### Criterio de aprobación

- Usa `Console.Write` para las preguntas y `ReadLine` para leer.
- Convierte la edad a número antes de sumar.

#### Entrada de ejemplo

```
Ceci
15
```

#### Salida esperada

```
Nombre: Edad: Ficha de Ceci: el año que viene cumple 16.
```

#### Solución de referencia

```csharp
Console.Write("Nombre: ");
string nombre = Console.ReadLine() ?? "";
Console.Write("Edad: ");
int edad = int.Parse(Console.ReadLine() ?? "");
Console.WriteLine($"Ficha de {nombre}: el año que viene cumple {edad + 1}.");
```

## R01-N08 · Math y el azar: la caja de herramientas

```meta
tipo: tema
padre: R01-N07
precio: 10
criatura: ogro
temas: prog.matematica-azar
usa: prog.operadores, prog.variables
```

### Crónica

En el fondo del Conservatorio hay una caja de herramientas que nadie abre: un metrónomo, una regla de afinar y un par de dados de marfil. Clave la abre por primera vez en años.

—No hace falta inventar todo —dice {mentor}—. C# trae una caja llena de cuentas ya hechas: raíces, potencias, redondeos. Y trae dados, para cuando el programa tiene que sorprender.

### Objetivos

- Usar las cuentas de `Math`: `Max`, `Min`, `Abs`, `Pow`, `Sqrt` y `Round`.
- Mantener un valor dentro de un rango con `Math.Clamp`.
- Tirar dados con `Random` y una semilla, para que el resultado se pueda repetir.

### Antes de empezar

- Las cuentas (R01-N03) y los tipos `int` y `double` (R01-N02).

### Explicación

#### `Math`: cuentas ya hechas

| Cuenta | Qué hace | Ejemplo | Da |
|---|---|---|---|
| `Math.Max(a, b)` | el mayor | `Math.Max(3, 9)` | `9` |
| `Math.Min(a, b)` | el menor | `Math.Min(3, 9)` | `3` |
| `Math.Abs(x)` | sin el signo menos | `Math.Abs(-8)` | `8` |
| `Math.Pow(a, b)` | `a` elevado a `b` | `Math.Pow(2, 10)` | `1024` |
| `Math.Sqrt(x)` | raíz cuadrada | `Math.Sqrt(81)` | `9` |
| `Math.Round(x, 2)` | redondea a 2 decimales | `Math.Round(2.567, 2)` | `2,57` |
| `Math.Clamp(x, min, max)` | lo mete entre `min` y `max` | `Math.Clamp(130, 0, 100)` | `100` |

#### Los dados: `Random`

```csharp
Random dado = new Random(42);
Console.WriteLine(dado.Next(1, 7));   // un número del 1 al 6
```

`Next(1, 7)` da un número **desde el 1 hasta el 6**: el último no entra. El `42` es la **semilla**: con la misma semilla, los dados salen siempre igual. Eso sirve para probar. Sin semilla (`new Random()`), cambian cada vez.

### Código de ejemplo

```csharp
Console.WriteLine(Math.Max(3, 9));
Console.WriteLine(Math.Abs(-8));
Console.WriteLine(Math.Pow(2, 10));
Console.WriteLine(Math.Sqrt(81));
Console.WriteLine(Math.Round(2.567, 2));
Console.WriteLine(Math.Clamp(130, 0, 100));

Random dado = new Random(42);
Console.WriteLine(dado.Next(1, 7));
Console.WriteLine(dado.Next(1, 7));
```

### Salida esperada

```
9
8
1024
9
2,57
100
5
1
```

### ¿Para qué sirve?

Los juegos viven de esto: la distancia entre dos personajes es una raíz, la vida nunca pasa de 100 (`Clamp`) y cada golpe tiene algo de azar. Y en cualquier programa, redondear un precio es una cuenta de todos los días.

### Errores habituales

- **Esperar que `Next(1, 6)` dé un 6:** el segundo número no entra. Para un dado de 6 caras, `Next(1, 7)`.
- **Guardar `Math.Pow` en un `int`:** devuelve `double`. Usá `double`, o convertí con `(int)`.
- **Probar con azar sin semilla:** cada vez sale otra cosa y no sabés si el programa anda. Para probar, poné una semilla.

### Micro-misión R01-N08-P1 · El más alto

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Max y Min | Math.Max(a, b) = el mayor · Math.Min(a, b) = el menor
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Ceci y Bemol compiten a ver quién toca la nota más larga. Ceci aguantó 14 segundos y Bemol 11. Clave quiere anotar el récord.

#### Gheco sugiere
`Math.Max` te da el mayor de dos números, sin tener que comparar vos:

```csharp
int a = 4, b = 10;
Console.WriteLine(Math.Max(a, b));
```

Muestra `10`.

#### Desafío
Mostrá el récord: el mayor entre `ceci` y `bemol`.

#### Código inicial
```csharp
int ceci = 14;
int bemol = 11;
Console.WriteLine(bemol);
```

#### Salida esperada
```
14
```

#### Solución
```csharp
int ceci = 14;
int bemol = 11;
Console.WriteLine(Math.Max(ceci, bemol));
```

#### Al superarla
Bemol se queda sin aire de la risa. —La próxima te gano, ¿eh?

#### Imagen
- Un reloj de arena sobre un atril y una pizarra lisa en la pared, sin nada escrito.
- Ceci toca el violín con los ojos cerrados y Bemol, rojo de aguantar, sostiene una nota en una flauta.

### Micro-misión R01-N08-P2 · La raíz del escenario

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Pow y Sqrt | Math.Pow(a, b) = a elevado a b · Math.Sqrt(x) = raíz cuadrada · dan double
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
El escenario nuevo es cuadrado y mide 64 metros cuadrados. Clave necesita saber cuánto mide cada lado para comprar la alfombra.

#### Gheco sugiere
La raíz cuadrada te da el lado de un cuadrado a partir de su superficie:

```csharp
Console.WriteLine(Math.Sqrt(25));
```

Muestra `5`, porque 5 × 5 = 25.

#### Desafío
Mostrá el lado del escenario: la raíz cuadrada de `superficie`.

#### Código inicial
```csharp
double superficie = 64;
Console.WriteLine(superficie);
```

#### Salida esperada
```
8
```

#### Solución
```csharp
double superficie = 64;
Console.WriteLine(Math.Sqrt(superficie));
```

#### Al superarla
—Ocho por ocho —dice Clave, y anota la medida para el alfombrero.

#### Imagen
- Un escenario de madera cuadrado y vacío, con una cinta métrica desenrollada en un borde.
- Clave mide un lado con un paso largo y Ceci sostiene la otra punta de la cinta.

### Micro-misión R01-N08-P3 · Redondear el precio

```meta
lugar: El puesto de Baldo
personajes: Ceci, Gheco
carta: Round | Math.Round(x, 2) = redondea a 2 decimales · 2,567 da 2,57
recompensa: xp 15, oro 15
```

#### Escena
Baldo dividió una caja de resina entre tres y le dio 4,6666… monedas cada parte. Quiere el precio redondeado a dos decimales.

#### Gheco sugiere
`Math.Round(número, decimales)` redondea:

```csharp
Console.WriteLine(Math.Round(3.14159, 2));
```

Muestra `3,14`.

#### Desafío
Mostrá `precio` redondeado a dos decimales.

#### Código inicial
```csharp
double precio = 14.0 / 3;
Console.WriteLine(precio);
```

#### Salida esperada
```
4,67
```

#### Solución
```csharp
double precio = 14.0 / 3;
Console.WriteLine(Math.Round(precio, 2));
```

#### Al superarla
—Cuatro con sesenta y siete —dice Baldo—. Ni un centavo más.

#### Imagen
- Tres panes de resina color ámbar sobre un mostrador de madera, al lado de una balanza de bronce.
- Gheco, sentado en el plato de la balanza, mira a Ceci contar monedas.

### Micro-misión R01-N08-P4 · Ni más de cien

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Clamp | Math.Clamp(x, min, max) mete x entre min y max · si se pasa, queda en el borde
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
El volumen del órgano va de 0 a 100. Bemol subió la perilla a 130 y casi rompe los vidrios. Hay que dejarlo dentro del rango.

#### Gheco sugiere
`Math.Clamp` pone un número entre un mínimo y un máximo. Si se pasa, lo deja en el borde:

```csharp
Console.WriteLine(Math.Clamp(-5, 0, 10));
Console.WriteLine(Math.Clamp(7, 0, 10));
```

Muestra `0` y después `7`.

#### Desafío
Mostrá `volumen` limitado entre `0` y `100`.

#### Código inicial
```csharp
int volumen = 130;
Console.WriteLine(volumen);
```

#### Salida esperada
```
100
```

#### Solución
```csharp
int volumen = 130;
Console.WriteLine(Math.Clamp(volumen, 0, 100));
```

#### Al superarla
Los vidrios dejan de temblar. Bemol esconde las manos en los bolsillos.

#### Imagen
- Los tubos dorados de un órgano y una perilla grande de bronce en el teclado, sin números.
- Bemol se tapa los oídos, asustado, y Ceci gira la perilla hacia abajo.

### Micro-misión R01-N08-P5 · El ogro del dado de cinco caras

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
criatura: ogro
carta: Random | new Random(semilla) · dado.Next(1, 7) = del 1 al 6 · el segundo número NO entra
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Para sortear quién toca primero tiran un dado. Pero un ogro escribió el programa: el dado nunca saca 6, y nadie entiende por qué.

#### Gheco sugiere
`Next(desde, hasta)` da un número desde `desde` hasta `hasta - 1`: **el segundo no entra**. Para que pueda salir el 6, el segundo número es 7.

```csharp
Random r = new Random(5);
Console.WriteLine(r.Next(1, 4));
```

Da un número del 1 al 3. Con la misma semilla (`5`), sale siempre el mismo.

#### Desafío
Arreglá el dado para que vaya del 1 al 6. Con la semilla `42`, el primer tiro sale `5`.

#### Código inicial
```csharp
Random dado = new Random(42);
int tiro = dado.Next(1, 6);
Console.WriteLine($"Salió {tiro}");
Console.WriteLine($"Puede salir 6: {6 < 6}");
```

#### Salida esperada
```
Salió 5
Puede salir 6: True
```

#### Solución
```csharp
Random dado = new Random(42);
int tiro = dado.Next(1, 7);
Console.WriteLine($"Salió {tiro}");
Console.WriteLine($"Puede salir 6: {6 < 7}");
```

#### Al superarla
El ogro mira el dado, cuenta las caras con los dedos y se va rascándose la cabeza.

#### Imagen
- Un dado grande de marfil sobre una mesa de madera, con los puntitos de las caras a la vista.
- Un ogro grandote y torpe, de cara confundida, se rasca la cabeza; Gheco lo mira desde el borde de la mesa.

### Encargo R01-N08-E1 · El golpe de Kira

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Kira, la espadachina de las Forjas, pide una calculadora de golpes. Con la semilla `7`, tirá un dado de 1 a 6 y multiplicá el tiro por la fuerza de Kira (`3,5`). Mostrá el golpe redondeado a un decimal, y la vida del ogro (`20`) menos el golpe, sin bajar nunca de `0` (con un golpe más fuerte, la vida quedaría en `0`):

```
Dado: 3
Golpe: 10,5
Vida del ogro: 9,5
```

#### Criterio de aprobación

- Usa `Random` con la semilla `7` y `Next(1, 7)`.
- Usa `Math.Round` y `Math.Max` (o `Math.Clamp`) para que la vida no sea negativa.

#### Salida esperada

```
Dado: 3
Golpe: 10,5
Vida del ogro: 9,5
```

#### Solución de referencia

```csharp
Random dado = new Random(7);
int tiro = dado.Next(1, 7);
double golpe = Math.Round(tiro * 3.5, 1);
double vida = Math.Max(20 - golpe, 0);
Console.WriteLine($"Dado: {tiro}");
Console.WriteLine($"Golpe: {golpe}");
Console.WriteLine($"Vida del ogro: {vida}");
```

## R01-N09 · Decidir: el programa elige el camino

```meta
tipo: tema
padre: R01-N08
precio: 10
criatura: ogro
temas: prog.condicionales
usa: prog.operadores, prog.entrada, prog.variables
```

### Crónica

La noche del ensayo, la cajita de música suena distinto según quién le da cuerda: con Ceci, alegre; con Bemol, lenta; con Clave, no suena. Clave anota cada caso en una hoja.

—Una partitura no siempre se toca igual —dice {mentor}—. Si llueve, más despacio; si el público aplaude, se repite el final. Un programa también elige: **si** pasa esto, hace aquello; **si no**, otra cosa.

### Objetivos

- Elegir entre dos caminos con `if` y `else`.
- Elegir entre varios con `else if`.
- Elegir según un valor exacto con `switch`.
- Validar la entrada con `TryParse` dentro de un `if`.

### Antes de empezar

- Las comparaciones (R01-N04) y `TryParse` (R01-N07).

### Explicación

#### `if` y `else`

```csharp
int edad = 14;
if (edad >= 13)
{
    Console.WriteLine("Puede entrar al coro.");
}
else
{
    Console.WriteLine("Todavía no.");
}
```

La condición va **entre paréntesis**, y lo que se hace va **entre llaves**. Si la condición da `True`, se hace lo del `if`; si no, lo del `else`. El `else` es opcional.

#### Varios caminos: `else if`

Se revisan **de arriba hacia abajo**, y se hace **solo el primero** que dé `True`:

```csharp
int nota = 7;
if (nota >= 9) Console.WriteLine("Excelente");
else if (nota >= 6) Console.WriteLine("Aprobado");
else Console.WriteLine("A ensayar");
```

Muestra `Aprobado`. Cuando hay una sola orden, se pueden omitir las llaves, pero con llaves nunca te equivocás.

#### `switch`: según un valor exacto

```csharp
string instrumento = "violín";
string familia = instrumento switch
{
    "violín" or "viola" => "cuerdas",
    "flauta" => "vientos",
    _ => "otra familia",
};
Console.WriteLine(familia);   // cuerdas
```

Es la **expresión `switch`**: compara el valor con cada caso y te da el resultado del primero que coincide. El `_` es «cualquier otro caso».

#### Validar con `if`

```csharp
if (int.TryParse(texto, out int n))
    Console.WriteLine($"Número: {n}");
else
    Console.WriteLine("Eso no es un número.");
```

### Código de ejemplo

```csharp
int aplausos = 85;

if (aplausos > 100)
{
    Console.WriteLine("¡Otra!");
}
else if (aplausos > 50)
{
    Console.WriteLine("Se repite el final.");
}
else
{
    Console.WriteLine("Saludo y a casa.");
}

string dia = "sábado";
string ensayo = dia switch
{
    "sábado" or "domingo" => "ensayo general",
    _ => "ensayo de sección",
};
Console.WriteLine(ensayo);
```

### Salida esperada

```
Se repite el final.
ensayo general
```

### ¿Para qué sirve?

Casi todo programa decide: si la clave es correcta, entra; si no hay stock, avisa; si la vida llega a cero, termina el juego. Sin `if`, un programa haría siempre lo mismo.

### Errores habituales

- **Poner `;` después del paréntesis:** `if (x > 5);` termina el `if` ahí mismo, y lo de las llaves se hace siempre (un **ogro** de lógica).
- **Ordenar mal los `else if`:** si preguntás primero `nota >= 6` y después `nota >= 9`, el 9 nunca llega a «Excelente».
- **Olvidar el `_` en el `switch`:** si llega un valor que no está, el programa se rompe.

### Micro-misión R01-N09-P1 · ¿Entra al coro?

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: if / else | if (condición) { … } else { … } · se hace UNO de los dos
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Clave arma el coro de la noche: entran los que tienen 13 años o más. Una chica de 12 pregunta si puede.

#### Gheco sugiere
`if` hace algo solo si la condición da `True`; `else` hace otra cosa si no:

```csharp
int temperatura = 30;
if (temperatura > 25)
{
    Console.WriteLine("Hace calor");
}
else
{
    Console.WriteLine("Está fresco");
}
```

Muestra `Hace calor`.

#### Desafío
Completá: si `edad` es 13 o más, mostrá `Entra al coro`; si no, `Todavía no`.

#### Código inicial
```csharp
int edad = 12;
if (edad >= 13)
{
    Console.WriteLine("Entra al coro");
}
```

#### Salida esperada
```
Todavía no
```

#### Solución
```csharp
int edad = 12;
if (edad >= 13)
{
    Console.WriteLine("Entra al coro");
}
else
{
    Console.WriteLine("Todavía no");
}
```

#### Al superarla
La chica se pone triste, pero Clave le da una pandereta: —Para el año que viene, practicá con esto.

#### Imagen
- Una fila de chicos de coro con túnicas lisas cerradas, frente a una escalinata de piedra con velas.
- Clave le da una pandereta a una nena de pelo corto, y Ceci sonríe al costado.

### Micro-misión R01-N09-P2 · La nota del ensayo

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: else if | se revisan de arriba hacia abajo · se hace SOLO el primero que dé True
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Clave pone nota a cada ensayo. Con 9 o más, «Excelente»; con 6 o más, «Aprobado»; si no, «A ensayar». Bemol sacó un 6.

#### Gheco sugiere
Con `else if` encadenás varias preguntas. Se hace **solo la primera** que dé `True`:

```csharp
int velocidad = 70;
if (velocidad > 100) Console.WriteLine("Muy rápido");
else if (velocidad > 60) Console.WriteLine("Rápido");
else Console.WriteLine("Tranquilo");
```

Muestra `Rápido`.

#### Desafío
Agregá el caso del medio: con 6 o más, `Aprobado`.

#### Código inicial
```csharp
int nota = 6;
if (nota >= 9) Console.WriteLine("Excelente");
else Console.WriteLine("A ensayar");
```

#### Salida esperada
```
Aprobado
```

#### Solución
```csharp
int nota = 6;
if (nota >= 9) Console.WriteLine("Excelente");
else if (nota >= 6) Console.WriteLine("Aprobado");
else Console.WriteLine("A ensayar");
```

#### Al superarla
—¡Aprobado! —grita Bemol, y le da un golpe de festejo al tambor.

#### Imagen
- Un tablero de corcho con hojas de evaluación en blanco clavadas con chinches.
- Bemol festeja con los palillos en alto; Ceci aplaude a su lado.

### Micro-misión R01-N09-P3 · La familia del instrumento

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: switch | valor switch { "a" => …, "b" or "c" => …, _ => … } · _ = cualquier otro
recompensa: xp 15, oro 15
```

#### Escena
Los instrumentos nuevos llegaron en cajas sin etiqueta. Clave quiere saber a qué familia va cada uno: la flauta a vientos, el violín y la viola a cuerdas, y el resto a percusión.

#### Gheco sugiere
La **expresión `switch`** elige un resultado según el valor:

```csharp
string fruta = "limón";
string sabor = fruta switch
{
    "limón" => "ácido",
    "banana" => "dulce",
    _ => "no sé",
};
Console.WriteLine(sabor);
```

Muestra `ácido`. Con `or` juntás varios casos.

#### Desafío
Agregá el caso `"violín" or "viola"`, que da `"cuerdas"`.

#### Código inicial
```csharp
string instrumento = "viola";
string familia = instrumento switch
{
    "flauta" => "vientos",
    _ => "percusión",
};
Console.WriteLine(familia);
```

#### Salida esperada
```
cuerdas
```

#### Solución
```csharp
string instrumento = "viola";
string familia = instrumento switch
{
    "flauta" => "vientos",
    "violín" or "viola" => "cuerdas",
    _ => "percusión",
};
Console.WriteLine(familia);
```

#### Al superarla
Clave pone la viola en el estante de las cuerdas, al lado del violín de Ceci.

#### Imagen
- Tres estantes de madera: uno con violines y violas, otro con flautas y otro con tambores, todos sin carteles.
- Clave acomoda una viola en su estante mientras Ceci saca otra caja.

### Micro-misión R01-N09-P4 · El pedido revisado

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
carta: Validar | if (int.TryParse(texto, out int n)) { usar n } else { avisar }
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
En el ensayo abierto, alguien escribió la cantidad de repeticiones. Si es un número, Ceci lo repite; si no, le pide que lo escriba bien.

#### Gheco sugiere
`TryParse` da `True` o `False`, así que puede ir **directo** adentro del `if`:

```csharp
string texto = "12";
if (int.TryParse(texto, out int n))
    Console.WriteLine(n * 2);
else
    Console.WriteLine("No es un número");
```

Muestra `24`.

#### Desafío
Si `pedido` es un número, mostrá `Repito X veces`; si no, `Escribilo con números`.

#### Código inicial
```csharp
string pedido = Console.ReadLine() ?? "";
Console.WriteLine(pedido);
```

#### Entrada
```
cinco
```

#### Salida esperada
```
Escribilo con números
```

#### Solución
```csharp
string pedido = Console.ReadLine() ?? "";
if (int.TryParse(pedido, out int veces))
    Console.WriteLine($"Repito {veces} veces");
else
    Console.WriteLine("Escribilo con números");
```

#### Al superarla
Un nene del público tacha «cinco», escribe un 5 enorme, y Ceci lo toca cinco veces.

#### Imagen
- Un papelito de pedido con un número grande dibujado y un tachón, sin letras.
- Un nene del público levanta el papelito y Gheco, desde el atril, le hace un gesto de «bien».

### Micro-misión R01-N09-P5 · El ogro del punto y coma

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
criatura: ogro
carta: if (…); | un ; después del paréntesis termina el if · lo de las llaves se hace SIEMPRE
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
El ogro de la lógica escribió el programa de la alarma: tiene que sonar solo si entran más de 200 personas. Pero suena siempre, aunque haya 50.

#### Gheco sugiere
Un `;` justo después del `if (…)` lo termina ahí: el `if` no hace nada, y el bloque de llaves queda suelto y **se ejecuta siempre**. Va así, sin punto y coma:

```csharp
if (lluvia)
{
    Console.WriteLine("Llevá paraguas");
}
```

#### Desafío
Ejecutalo: suena la alarma con 50 personas. Sacá el `;` que sobra para que no muestre nada y solo muestre `Fin`.

#### Código inicial
```csharp
int personas = 50;
if (personas > 200);
{
    Console.WriteLine("¡Alarma!");
}
Console.WriteLine("Fin");
```

#### Salida esperada
```
Fin
```

#### Solución
```csharp
int personas = 50;
if (personas > 200)
{
    Console.WriteLine("¡Alarma!");
}
Console.WriteLine("Fin");
```

#### Al superarla
La alarma se calla. El ogro mira el punto y coma que sobró, lo levanta del piso y se lo lleva de recuerdo.

#### Imagen
- Una campana de bronce colgada en la entrada de la sala, quieta, a la luz de un farol.
- Un ogro grandote y torpe se tapa los oídos mientras Gheco, en la soga de la campana, la frena.

### Encargo R01-N09-E1 · La entrada de la Feria

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Bruno, del puesto de tiro de la Feria, quiere un programa para la entrada. Leé la edad. Si no es un número, mostrá `Edad inválida`. Si es menor de 6, `Entra gratis`; si es menor de 18, `Entrada de chico`; si no, `Entrada general`. Con la Entrada `12`:

```
Entrada de chico
```

#### Criterio de aprobación

- Valida con `int.TryParse` adentro de un `if`.
- Usa `else if` para los tres precios, de menor a mayor.

#### Entrada de ejemplo

```
12
```

#### Salida esperada

```
Entrada de chico
```

#### Pruebas

##### No es un número
```entrada
doce
```
```salida
Edad inválida
```

##### Un bebé
```entrada
3
```
```salida
Entra gratis
```

##### Adulto
```entrada
40
```
```salida
Entrada general
```

#### Solución de referencia

```csharp
string texto = Console.ReadLine() ?? "";
if (!int.TryParse(texto, out int edad))
    Console.WriteLine("Edad inválida");
else if (edad < 6)
    Console.WriteLine("Entra gratis");
else if (edad < 18)
    Console.WriteLine("Entrada de chico");
else
    Console.WriteLine("Entrada general");
```

## R01-N10 · Repetir: el ensayo hasta que salga

```meta
tipo: tema
padre: R01-N09
precio: 10
criatura: ogro
temas: prog.bucles, prog.menu
usa: prog.condicionales, prog.entrada
```

### Crónica

Ceci toca el mismo pasaje una vez, y otra, y otra. Le sale mejor cada vez. Clave cuenta en voz baja: —…ocho, nueve, diez. Ahora sí.

—Repetir es la base del ensayo —dice {mentor}—. Y un programa repite sin cansarse: cien veces, mil, o **hasta que** pase algo. Pero hay que decirle cuándo parar, o no para nunca.

### Objetivos

- Repetir mientras se cumpla una condición con `while`.
- Repetir una cantidad fija de veces con `for`.
- Sumar dentro de un bucle (un acumulador).
- Cortar con `break` y saltear con `continue`.
- Armar un menú que se repite hasta que eligen salir.

### Antes de empezar

- Las decisiones con `if` (R01-N09) y la lectura con `ReadLine` (R01-N07).

### Explicación

#### `while`: mientras se cumpla

```csharp
int ensayo = 1;
while (ensayo <= 3)
{
    Console.WriteLine($"Ensayo {ensayo}");
    ensayo++;          // suma 1: sin esto, no termina nunca
}
```

`ensayo++` es lo mismo que `ensayo = ensayo + 1`.

#### `for`: una cantidad fija de veces

Junta en una línea el **inicio**, la **condición** y el **paso**:

```csharp
for (int i = 1; i <= 3; i++)
{
    Console.WriteLine($"Compás {i}");
}
```

#### El acumulador

Una variable que arranca en `0` y suma en cada vuelta:

```csharp
int total = 0;
for (int i = 1; i <= 4; i++)
{
    total += i;        // total = total + i
}
Console.WriteLine(total);   // 10
```

#### `break` y `continue`

- `break` **corta** el bucle y sigue con lo que viene después.
- `continue` **saltea** el resto de esta vuelta y pasa a la siguiente.

#### El menú

Un `while (true)` que lee una opción y termina con `break` cuando eligen salir:

```csharp
while (true)
{
    string opcion = Console.ReadLine() ?? "";
    if (opcion == "0") break;
    Console.WriteLine($"Elegiste {opcion}");
}
```

### Código de ejemplo

```csharp
for (int i = 1; i <= 3; i++)
{
    Console.WriteLine($"Pasaje {i}");
}

int compases = 0;
int vuelta = 0;
while (compases < 20)
{
    compases += 8;
    vuelta++;
}
Console.WriteLine($"{vuelta} vueltas, {compases} compases");
```

### Salida esperada

```
Pasaje 1
Pasaje 2
Pasaje 3
3 vueltas, 24 compases
```

### ¿Para qué sirve?

Repetir es lo que mejor hace una compu: recorrer mil alumnos, sumar todas las ventas del día, mostrar un menú hasta que el usuario sale. Casi todos los programas tienen, en el centro, un bucle.

### Errores habituales

- **El bucle infinito:** si nunca cambia lo que pregunta la condición (olvidaste el `i++`), no termina. Acá el programa se corta a los 5 segundos (el **ogro** que no para).
- **Contar una vuelta de más o de menos:** `i < 3` da 3 vueltas desde 0; `i <= 3` da 4.
- **Acumulador adentro del bucle:** si ponés `int total = 0;` adentro, vuelve a 0 en cada vuelta.

### Micro-misión R01-N10-P1 · Contar hasta tres

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: for | for (int i = 1; i <= 3; i++) { … } · inicio; condición; paso
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Antes de cada obra, Clave cuenta hasta tres para que todos entren juntos. Quiere que el programa cuente con ella.

#### Gheco sugiere
`for` repite una cantidad fija de veces. La variable `i` cambia en cada vuelta:

```csharp
for (int i = 1; i <= 2; i++)
{
    Console.WriteLine($"Vuelta {i}");
}
```

Muestra `Vuelta 1` y `Vuelta 2`.

#### Desafío
Cambiá el `for` para que cuente de 1 a 3, en lugar de 1 a 5.

#### Código inicial
```csharp
for (int i = 1; i <= 5; i++)
{
    Console.WriteLine(i);
}
```

#### Salida esperada
```
1
2
3
```

#### Solución
```csharp
for (int i = 1; i <= 3; i++)
{
    Console.WriteLine(i);
}
```

#### Al superarla
—Uno, dos, tres… —y la orquesta entra toda junta, como un solo instrumento.

#### Imagen
- Una orquesta chica de alumnos con sus instrumentos listos, en semicírculo, a la luz de las velas.
- Clave levanta la batuta para marcar la entrada, y Ceci tiene el arco apoyado en las cuerdas.

### Micro-misión R01-N10-P2 · La suma de los aplausos

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Acumulador | total = 0 antes del bucle · total += x adentro · se muestra después
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol anotó los aplausos de cada noche de la semana: 1, 2, 3, 4 y 5 rondas, una más cada día. Quiere saber cuántas rondas hubo en total.

#### Gheco sugiere
Un **acumulador** arranca en `0` y suma en cada vuelta. Se muestra **después** del bucle:

```csharp
int puntos = 0;
for (int i = 1; i <= 3; i++)
{
    puntos += 10;
}
Console.WriteLine(puntos);
```

Muestra `30`.

#### Desafío
Sumá `i` al `total` en cada vuelta, para que muestre el total de rondas de los 5 días.

#### Código inicial
```csharp
int total = 0;
for (int i = 1; i <= 5; i++)
{
}
Console.WriteLine(total);
```

#### Salida esperada
```
15
```

#### Solución
```csharp
int total = 0;
for (int i = 1; i <= 5; i++)
{
    total += i;
}
Console.WriteLine(total);
```

#### Al superarla
—¡Quince rondas! —Bemol lo anota en el tambor con un lápiz.

#### Imagen
- Un tambor chico apoyado en una silla, con marcas de lápiz en el borde de madera, sin números.
- Bemol cuenta con los dedos y Ceci lo mira con el violín bajo el brazo.

### Micro-misión R01-N10-P3 · Hasta que se apague la vela

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
carta: while | while (condición) { … } · algo adentro tiene que cambiar la condición
recompensa: xp 15, oro 15
```

#### Escena
La vela del atril mide 10 centímetros y cada ensayo gasta 3. Ceci quiere saber cuántos ensayos puede hacer antes de quedarse a oscuras.

#### Gheco sugiere
`while` repite **mientras** la condición dé `True`. Adentro, algo tiene que cambiar, si no, no termina nunca:

```csharp
int agua = 7;
while (agua > 0)
{
    agua -= 2;
}
Console.WriteLine(agua);
```

Muestra `-1`: la última vuelta pasó de 1 a -1.

#### Desafío
Completá el bucle: en cada vuelta, restale 3 a `vela` y sumale 1 a `ensayos`.

#### Código inicial
```csharp
int vela = 10;
int ensayos = 0;
while (vela >= 3)
{
}
Console.WriteLine($"Ensayos: {ensayos}");
```

#### Salida esperada
```
Ensayos: 3
```

#### Solución
```csharp
int vela = 10;
int ensayos = 0;
while (vela >= 3)
{
    vela -= 3;
    ensayos++;
}
Console.WriteLine($"Ensayos: {ensayos}");
```

#### Al superarla
Tres ensayos, y queda un pedacito de vela para guardar el violín sin tropezar.

#### Imagen
- Una vela casi consumida sobre el borde de un atril, con una gota de cera.
- Gheco, al lado de la vela, protege la llama con las manitos; Ceci guarda el violín.

### Micro-misión R01-N10-P4 · El menú del Conservatorio

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Menú | while (true) { leer opción; if (opcion == "0") break; … } · break corta el bucle
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol armó un menú para el público: escriben la obra que quieren escuchar, y el programa la anuncia. Con `0` se termina. Pero el menú no termina nunca.

#### Gheco sugiere
`break` corta el bucle en el momento. En un menú, se usa cuando eligen la opción de salir:

```csharp
while (true)
{
    string x = Console.ReadLine() ?? "";
    if (x == "fin") break;
    Console.WriteLine(x);
}
```

#### Desafío
Agregá, antes del `WriteLine`, la línea que corta el bucle cuando la opción es `"0"`. Después del bucle tiene que mostrar `Gracias por venir`.

#### Código inicial
```csharp
while (true)
{
    string opcion = Console.ReadLine() ?? "0";
    Console.WriteLine($"Ahora suena: {opcion}");
}
Console.WriteLine("Gracias por venir");
```

#### Entrada
```
Serenata
Minueto
0
```

#### Salida esperada
```
Ahora suena: Serenata
Ahora suena: Minueto
Gracias por venir
```

#### Solución
```csharp
while (true)
{
    string opcion = Console.ReadLine() ?? "0";
    if (opcion == "0") break;
    Console.WriteLine($"Ahora suena: {opcion}");
}
Console.WriteLine("Gracias por venir");
```

#### Al superarla
El público pide dos obras y se va contento. Bemol apaga las velas una por una.

#### Imagen
- Una pizarra de madera lisa en un caballete, al lado de la puerta de la sala, sin nada escrito.
- Bemol saluda al público que se va, y Ceci guarda el arco.

### Micro-misión R01-N10-P5 · El ogro que no para

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
criatura: ogro
carta: Bucle infinito | si nada cambia la condición, no termina · falta el i++ · se corta a los 5 s
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
El ogro de la lógica escribió un metrónomo que tenía que dar 4 golpes. Da golpes sin parar hasta que el programa se corta.

#### Gheco sugiere
Si nada dentro del `while` cambia lo que pregunta la condición, no termina nunca. Acá el programa se corta a los 5 segundos. Casi siempre, falta sumar 1:

```csharp
int i = 0;
while (i < 2)
{
    Console.WriteLine("tic");
    i++;
}
```

#### Desafío
Ejecutalo y mirá cómo se corta. Agregá `golpe++;` adentro del bucle para que dé solo 4 golpes.

#### Código inicial
```csharp
int golpe = 1;
while (golpe <= 4)
{
    Console.WriteLine($"Tac {golpe}");
}
```

#### Salida esperada
```
Tac 1
Tac 2
Tac 3
Tac 4
```

#### Solución
```csharp
int golpe = 1;
while (golpe <= 4)
{
    Console.WriteLine($"Tac {golpe}");
    golpe++;
}
```

#### Al superarla
El metrónomo da cuatro golpes y se queda quieto. El ogro, mareado, se sienta en el piso.

#### Imagen
- Un metrónomo de madera con la aguja quieta sobre una mesa, a la luz de un farol.
- Un ogro grandote y mareado sentado en el piso; Gheco, parado en el metrónomo, frena la aguja.

### Encargo R01-N10-E1 · La caja del puesto de pan

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Doña Mirta, la panadera de la Feria, quiere sumar las ventas del día. Leé precios, uno por línea, hasta que escriban `0`. Si una línea no es un número, salteala con `continue`. Al final, mostrá cuántas ventas hubo y el total. Con esta Entrada:

```
300
150
mucho
250
0
```

muestra:

```
Ventas: 3
Total: 700
```

#### Criterio de aprobación

- Usa un bucle con `break` para el `0` y `continue` para lo que no es un número.
- Usa acumuladores para la cantidad y el total.

#### Entrada de ejemplo

```
300
150
mucho
250
0
```

#### Salida esperada

```
Ventas: 3
Total: 700
```

#### Pruebas

##### Sin ventas
```entrada
0
```
```salida
Ventas: 0
Total: 0
```

#### Solución de referencia

```csharp
int ventas = 0;
int total = 0;
while (true)
{
    string linea = Console.ReadLine() ?? "0";
    if (!int.TryParse(linea, out int precio)) continue;
    if (precio == 0) break;
    ventas++;
    total += precio;
}
Console.WriteLine($"Ventas: {ventas}");
Console.WriteLine($"Total: {total}");
```

## R01-N11 · Arreglos: el estante de las partituras

```meta
tipo: tema
padre: R01-N10
precio: 10
criatura: orco
temas: col.arrays
usa: prog.bucles, prog.variables
```

### Crónica

Clave le muestra a Ceci un estante largo, con un casillero numerado para cada partitura del repertorio. —Si tuvieras que hacer una variable para cada obra, no te alcanzaría la noche.

—Un **arreglo** es un estante —dice {mentor}—: un solo nombre, muchos casilleros, y cada casillero con su número. El primero, como siempre, es el cero.

### Objetivos

- Guardar muchos valores bajo un solo nombre con un arreglo (`int[]`, `string[]`).
- Leer y cambiar un casillero por su posición.
- Recorrer un arreglo con `foreach` y con `for`.
- Ordenar y buscar con `Array.Sort` y `Array.IndexOf`.

### Antes de empezar

- Las posiciones de un texto (R01-N05) y los bucles (R01-N10).

### Explicación

#### Crear un arreglo

```csharp
int[] duraciones = { 3, 5, 2, 4 };        // con los valores
string[] obras = new string[3];           // 3 casilleros vacíos
obras[0] = "Serenata";
```

`duraciones.Length` dice cuántos casilleros tiene (4). El primero es `[0]` y el último `[Length - 1]`, igual que las letras de un texto.

#### Recorrer

- `foreach` cuando solo importa **el valor**:

```csharp
foreach (int d in duraciones)
{
    Console.WriteLine(d);
}
```

- `for` cuando también importa **la posición**:

```csharp
for (int i = 0; i < duraciones.Length; i++)
{
    Console.WriteLine($"{i}: {duraciones[i]}");
}
```

#### Herramientas de `Array`

| Orden | Qué hace |
|---|---|
| `Array.Sort(a)` | ordena de menor a mayor (cambia el arreglo) |
| `Array.Reverse(a)` | lo da vuelta |
| `Array.IndexOf(a, x)` | la posición de `x`, o `-1` si no está |

### Código de ejemplo

```csharp
string[] obras = { "Serenata", "Minueto", "Nocturno" };
int[] minutos = { 6, 3, 8 };

Console.WriteLine(obras.Length);
Console.WriteLine(obras[1]);

int total = 0;
foreach (int m in minutos)
{
    total += m;
}
Console.WriteLine($"Concierto: {total} minutos");

for (int i = 0; i < obras.Length; i++)
{
    Console.WriteLine($"{i + 1}. {obras[i]} ({minutos[i]} min)");
}

Array.Sort(minutos);
Console.WriteLine(string.Join(", ", minutos));
```

### Salida esperada

```
3
Minueto
Concierto: 17 minutos
1. Serenata (6 min)
2. Minueto (3 min)
3. Nocturno (8 min)
3, 6, 8
```

### ¿Para qué sirve?

Cada vez que hay «muchos de lo mismo» (las notas de un curso, los precios de una lista, los enemigos de un nivel) va un arreglo. Con un bucle, el mismo programa sirve para 3 o para 3000.

### Errores habituales

- **Recorrer con `i <= Length`:** la última vuelta pide un casillero que no existe y el **orco** de `IndexOutOfRangeException` corta todo. Va `i < Length`.
- **Querer agrandar el arreglo:** su tamaño es fijo desde que se crea. Para listas que crecen hay otra herramienta (`List`, en el Acto III).
- **Mostrarlo con `WriteLine(arreglo)`:** muestra `System.Int32[]`, no los valores. Usá `string.Join`.

### Micro-misión R01-N11-P1 · El tercer casillero

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Arreglo | int[] a = { 3, 5, 2 } · a[0] = el primero · a.Length = cuántos hay
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Clave tiene el repertorio de la noche en un estante: cuatro obras. Le pide a Ceci la tercera.

#### Gheco sugiere
Un arreglo guarda muchos valores con un solo nombre. Se piden por posición, desde el 0:

```csharp
string[] colores = { "rojo", "verde", "azul" };
Console.WriteLine(colores[1]);
```

Muestra `verde`.

#### Desafío
Mostrá la tercera obra del arreglo.

#### Código inicial
```csharp
string[] repertorio = { "Serenata", "Minueto", "Nocturno", "Vals" };
Console.WriteLine(repertorio.Length);
```

#### Salida esperada
```
Nocturno
```

#### Solución
```csharp
string[] repertorio = { "Serenata", "Minueto", "Nocturno", "Vals" };
Console.WriteLine(repertorio[2]);
```

#### Al superarla
Clave saca la partitura del tercer casillero y la pone en el atril de Ceci.

#### Imagen
- Un estante largo de madera con casilleros iguales, cada uno con una carpeta de partituras, sin números a la vista.
- Clave saca una carpeta del tercer casillero y se la da a Ceci.

### Micro-misión R01-N11-P2 · Todas las duraciones

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: foreach | foreach (int d in duraciones) { … } · pasa por cada valor, en orden
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol quiere saber cuánto dura el concierto entero: suma las duraciones de todas las obras.

#### Gheco sugiere
`foreach` pasa por cada valor del arreglo, uno por vuelta:

```csharp
int[] edades = { 10, 20 };
int suma = 0;
foreach (int e in edades)
{
    suma += e;
}
Console.WriteLine(suma);
```

Muestra `30`.

#### Desafío
Recorré `minutos` con `foreach` y sumá cada valor a `total`.

#### Código inicial
```csharp
int[] minutos = { 6, 3, 8, 4 };
int total = 0;
Console.WriteLine($"Total: {total} minutos");
```

#### Salida esperada
```
Total: 21 minutos
```

#### Solución
```csharp
int[] minutos = { 6, 3, 8, 4 };
int total = 0;
foreach (int m in minutos)
{
    total += m;
}
Console.WriteLine($"Total: {total} minutos");
```

#### Al superarla
—Veintiún minutos —dice Bemol—. Me da tiempo de comer algo antes.

#### Imagen
- Un reloj de pared antiguo en una sala de piedra, con las agujas a la vista y sin números.
- Bemol mira el reloj con la mano en la panza; Ceci repasa las partituras.

### Micro-misión R01-N11-P3 · El programa numerado

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: for con arreglo | for (int i = 0; i < a.Length; i++) · a[i] = el de esa vuelta
recompensa: xp 15, oro 15
```

#### Escena
Para el programa impreso del concierto, Clave quiere cada obra con su número: 1, 2, 3…

#### Gheco sugiere
Con `for` tenés la posición `i` en cada vuelta. Como empieza en 0, para numerar desde 1 se muestra `i + 1`:

```csharp
string[] pasos = { "afinar", "tocar" };
for (int i = 0; i < pasos.Length; i++)
{
    Console.WriteLine($"{i + 1}) {pasos[i]}");
}
```

Muestra `1) afinar` y `2) tocar`.

#### Desafío
Completá el `WriteLine` para que muestre cada obra con su número, desde 1.

#### Código inicial
```csharp
string[] obras = { "Serenata", "Minueto", "Nocturno" };
for (int i = 0; i < obras.Length; i++)
{
    Console.WriteLine(obras[0]);
}
```

#### Salida esperada
```
1. Serenata
2. Minueto
3. Nocturno
```

#### Solución
```csharp
string[] obras = { "Serenata", "Minueto", "Nocturno" };
for (int i = 0; i < obras.Length; i++)
{
    Console.WriteLine($"{i + 1}. {obras[i]}");
}
```

#### Al superarla
El programa queda listo para la imprenta. Clave lo dobla en tres.

#### Imagen
- Una pila de programas de concierto doblados, en blanco, atados con una cinta bordó.
- Clave dobla un programa con cuidado y Ceci acomoda la pila.

### Micro-misión R01-N11-P4 · Ordenar el repertorio

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
carta: Array.Sort | Array.Sort(a) ordena de menor a mayor · string.Join(", ", a) para mostrarlo
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Para que el concierto vaya de lo más tranquilo a lo más fuerte, Ceci quiere ordenar las obras por volumen, de menor a mayor.

#### Gheco sugiere
`Array.Sort` ordena el arreglo de menor a mayor. Para verlo entero, se une con `string.Join`:

```csharp
int[] puntajes = { 30, 10, 20 };
Array.Sort(puntajes);
Console.WriteLine(string.Join(" ", puntajes));
```

Muestra `10 20 30`.

#### Desafío
Ordená `volumenes` antes de mostrarlo.

#### Código inicial
```csharp
int[] volumenes = { 70, 20, 95, 40 };
Console.WriteLine(string.Join(", ", volumenes));
```

#### Salida esperada
```
20, 40, 70, 95
```

#### Solución
```csharp
int[] volumenes = { 70, 20, 95, 40 };
Array.Sort(volumenes);
Console.WriteLine(string.Join(", ", volumenes));
```

#### Al superarla
El concierto ya tiene forma: empieza en un susurro y termina con el órgano a todo lo que da.

#### Imagen
- Cuatro carpetas de partituras de alturas distintas, ordenadas de la más baja a la más alta sobre una mesa.
- Gheco salta de una carpeta a la siguiente, como por una escalera.

### Micro-misión R01-N11-P5 · El orco del casillero de más

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
criatura: orco
carta: i < Length | un arreglo de 3 tiene [0], [1] y [2] · i <= Length pide uno de más
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
El orco de las posiciones volvió: el programa muestra las tres obras y después se rompe pidiendo una cuarta que no existe.

#### Gheco sugiere
Un arreglo de 3 tiene los casilleros `0`, `1` y `2`. Si el `for` llega a `i <= Length`, la última vuelta pide el `3`, que no existe. Va **`<`**:

```csharp
for (int i = 0; i < nombres.Length; i++)
```

#### Desafío
Ejecutalo y mirá el error del orco. Arreglá la condición del `for`.

#### Código inicial
```csharp
string[] obras = { "Serenata", "Minueto", "Nocturno" };
for (int i = 0; i <= obras.Length; i++)
{
    Console.WriteLine(obras[i]);
}
```

#### Salida esperada
```
Serenata
Minueto
Nocturno
```

#### Solución
```csharp
string[] obras = { "Serenata", "Minueto", "Nocturno" };
for (int i = 0; i < obras.Length; i++)
{
    Console.WriteLine(obras[i]);
}
```

#### Al superarla
El orco busca el cuarto casillero, no lo encuentra, y se va a buscarlo a otro estante.

#### Imagen
- El final de un estante de madera: el último casillero lleno y, después, la pared lisa.
- Un orco verde chiquito tantea la pared buscando un casillero que no está; Gheco se ríe en el estante.

### Encargo R01-N11-E1 · Los blancos de Bruno

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Bruno anotó los puntos de los tiros de la noche en el puesto de tiro: `{ 40, 85, 10, 70, 55 }`. Mostrá:

- cuántos tiros hubo;
- el total de puntos;
- el promedio, con un decimal;
- los puntos ordenados de mayor a menor (ordená y después da vuelta).

```
Tiros: 5
Total: 260
Promedio: 52,0
De mayor a menor: 85, 70, 55, 40, 10
```

#### Criterio de aprobación

- Recorre el arreglo con `foreach` o `for` para sumar.
- Usa `Array.Sort` y `Array.Reverse`.

#### Salida esperada

```
Tiros: 5
Total: 260
Promedio: 52,0
De mayor a menor: 85, 70, 55, 40, 10
```

#### Solución de referencia

```csharp
int[] tiros = { 40, 85, 10, 70, 55 };
int total = 0;
foreach (int t in tiros)
{
    total += t;
}
double promedio = (double)total / tiros.Length;
Array.Sort(tiros);
Array.Reverse(tiros);
Console.WriteLine($"Tiros: {tiros.Length}");
Console.WriteLine($"Total: {total}");
Console.WriteLine($"Promedio: {promedio:F1}");
Console.WriteLine($"De mayor a menor: {string.Join(", ", tiros)}");
```

## R01-N12 · Matrices y referencias: el mapa del escenario

```meta
tipo: tema
padre: R01-N11
precio: 10
criatura: troll
temas: col.matrices, prog.referencias
usa: col.arrays, prog.bucles
```

### Crónica

Para el concierto grande, Clave dibuja el escenario en una cuadrícula: filas y columnas, y en cada cuadradito, un músico. Bemol copia el plano para ensayar su lugar… y cuando tacha algo en su copia, se tacha también en el de Clave.

—Dos cosas nuevas —dice {mentor}—. Una tabla tiene filas **y** columnas. Y un arreglo no se copia con `=`: con `=` le ponés **otro nombre** al mismo estante.

### Objetivos

- Guardar datos en filas y columnas con una matriz (`int[,]`).
- Recorrer una matriz con dos `for`, uno adentro del otro.
- Entender que `b = a` no copia un arreglo: los dos nombres apuntan al mismo.
- Copiar de verdad con `Clone()`.

### Antes de empezar

- Los arreglos (R01-N11).

### Explicación

#### Una matriz: filas y columnas

```csharp
char[,] escenario =
{
    { 'V', 'V', 'C' },
    { '.', 'F', '.' },
};
Console.WriteLine(escenario[0, 2]);            // C: fila 0, columna 2
Console.WriteLine(escenario.GetLength(0));     // 2 filas
Console.WriteLine(escenario.GetLength(1));     // 3 columnas
```

Se pide con **dos** números: primero la fila y después la columna, separados por coma.

#### Recorrer con dos `for`

```csharp
for (int f = 0; f < escenario.GetLength(0); f++)
{
    for (int c = 0; c < escenario.GetLength(1); c++)
    {
        Console.Write(escenario[f, c]);
    }
    Console.WriteLine();     // al terminar la fila, línea nueva
}
```

#### `=` no copia un arreglo

```csharp
int[] original = { 1, 2, 3 };
int[] otro = original;     // NO es una copia: es otro nombre para el mismo
otro[0] = 99;
Console.WriteLine(original[0]);   // 99: cambió también
```

Con un `int` suelto, `=` copia el número. Con un arreglo, copia **la dirección** del estante. Para una copia de verdad: `(int[])original.Clone()`.

### Código de ejemplo

```csharp
char[,] escenario =
{
    { 'V', 'V', 'C' },
    { '.', 'F', '.' },
};
for (int f = 0; f < escenario.GetLength(0); f++)
{
    for (int c = 0; c < escenario.GetLength(1); c++)
    {
        Console.Write(escenario[f, c]);
    }
    Console.WriteLine();
}

int[] plano = { 1, 2, 3 };
int[] mismo = plano;
int[] copia = (int[])plano.Clone();
mismo[0] = 9;
copia[1] = 7;
Console.WriteLine(string.Join(" ", plano));
```

### Salida esperada

```
VVC
.F.
9 2 3
```

### ¿Para qué sirve?

Las grillas están en todos lados: un tablero de ajedrez, el mapa de un juego, los asientos de un teatro, una planilla. Y entender que un arreglo se **comparte** evita uno de los errores más difíciles de encontrar: datos que cambian «solos».

### Errores habituales

- **Pedir `m[f][c]`:** en una matriz de C# va `m[f, c]`, con coma.
- **Usar `Length` para las filas:** en una matriz, `Length` es el total de casilleros. Las filas son `GetLength(0)` y las columnas `GetLength(1)`.
- **Creer que `b = a` copia:** el **troll** de las referencias compartidas cambia los dos. Usá `Clone()`.

### Micro-misión R01-N12-P1 · ¿Quién está en ese lugar?

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Matriz | int[,] m · m[fila, columna] · se cuenta desde 0 en las dos
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
En el plano del escenario, cada letra es un músico: V de violín, C de cello, F de flauta. Clave pregunta quién está en la fila 1, columna 2.

#### Gheco sugiere
Una matriz tiene filas y columnas. Se pide con dos números, separados por coma:

```csharp
int[,] tabla = { { 1, 2 }, { 3, 4 } };
Console.WriteLine(tabla[1, 0]);
```

Muestra `3`: fila 1, columna 0.

#### Desafío
Mostrá lo que hay en la fila `1`, columna `2`.

#### Código inicial
```csharp
char[,] escenario =
{
    { 'V', 'V', 'C' },
    { '.', 'V', 'F' },
};
Console.WriteLine(escenario[0, 0]);
```

#### Salida esperada
```
F
```

#### Solución
```csharp
char[,] escenario =
{
    { 'V', 'V', 'C' },
    { '.', 'V', 'F' },
};
Console.WriteLine(escenario[1, 2]);
```

#### Al superarla
—La flauta —dice Ceci—, al fondo a la derecha. —Clave asiente y marca el plano.

#### Imagen
- Un plano del escenario dibujado sobre papel, con cuadraditos y pequeños dibujos de instrumentos, sin letras.
- Clave señala un cuadradito con una batuta y Ceci se inclina a mirar.

### Micro-misión R01-N12-P2 · Dibujar el escenario

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Dos for | for filas { for columnas { Write } WriteLine } · GetLength(0) filas · GetLength(1) columnas
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol quiere ver el plano entero, fila por fila, como un dibujo.

#### Gheco sugiere
Con un `for` adentro de otro recorrés toda la matriz: el de afuera pasa por las filas y el de adentro por las columnas. `Write` deja todo en la misma línea, y el `WriteLine()` vacío pasa a la siguiente al terminar cada fila.

#### Desafío
Completá el `for` de adentro para que recorra las columnas y muestre cada lugar con `Console.Write`.

#### Código inicial
```csharp
char[,] escenario =
{
    { 'V', 'V', 'C' },
    { '.', 'F', '.' },
};
for (int f = 0; f < escenario.GetLength(0); f++)
{
    Console.WriteLine();
}
```

#### Salida esperada
```
VVC
.F.
```

#### Solución
```csharp
char[,] escenario =
{
    { 'V', 'V', 'C' },
    { '.', 'F', '.' },
};
for (int f = 0; f < escenario.GetLength(0); f++)
{
    for (int c = 0; c < escenario.GetLength(1); c++)
    {
        Console.Write(escenario[f, c]);
    }
    Console.WriteLine();
}
```

#### Al superarla
—¡Parece un tablero de ajedrez con instrumentos! —dice Bemol, y busca dónde le toca a él.

#### Imagen
- Un escenario visto desde arriba, con sillas en filas y columnas y los instrumentos apoyados, sin público.
- Bemol, de pie en un pasillo del escenario, mira hacia las sillas con el plano en la mano.

### Micro-misión R01-N12-P3 · Contar los violines

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Contar en matriz | dos for + if (m[f, c] == 'V') cuenta++ · comillas simples para un char
recompensa: xp 15, oro 15
```

#### Escena
Clave tiene que pedir resina para cada violín del escenario. ¿Cuántos son?

#### Gheco sugiere
Recorré la matriz con dos `for` y sumá 1 cada vez que encuentres lo que buscás. Un `char` va entre comillas **simples**: `'V'`.

```csharp
if (mapa[f, c] == 'X') cuenta++;
```

#### Desafío
Adentro del `for` de las columnas, sumá 1 a `violines` cada vez que el lugar sea `'V'`.

#### Código inicial
```csharp
char[,] escenario =
{
    { 'V', 'V', 'C' },
    { 'F', 'V', '.' },
};
int violines = 0;
for (int f = 0; f < escenario.GetLength(0); f++)
{
    for (int c = 0; c < escenario.GetLength(1); c++)
    {
    }
}
Console.WriteLine($"Violines: {violines}");
```

#### Salida esperada
```
Violines: 3
```

#### Solución
```csharp
char[,] escenario =
{
    { 'V', 'V', 'C' },
    { 'F', 'V', '.' },
};
int violines = 0;
for (int f = 0; f < escenario.GetLength(0); f++)
{
    for (int c = 0; c < escenario.GetLength(1); c++)
    {
        if (escenario[f, c] == 'V') violines++;
    }
}
Console.WriteLine($"Violines: {violines}");
```

#### Al superarla
—Tres panes de resina —anota Clave—. Uno más si Ceci sigue tocando tan fuerte.

#### Imagen
- Tres violines apoyados en sillas de un escenario, cada uno con su arco al lado.
- Clave cuenta los violines con la batuta y Ceci sostiene el suyo con una sonrisa culpable.

### Micro-misión R01-N12-P4 · La copia de verdad

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Clone | b = a NO copia: es el mismo arreglo · b = (int[])a.Clone() = una copia aparte
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol copió la lista de volúmenes para probar cambios. Cambió el primero de su copia… y se cambió también el de Clave.

#### Gheco sugiere
Con `=`, un arreglo no se copia: los dos nombres apuntan al mismo estante. Para una copia aparte, `Clone()`:

```csharp
int[] a = { 1, 2 };
int[] b = (int[])a.Clone();
b[0] = 50;
Console.WriteLine(a[0]);
```

Muestra `1`: el original no cambió.

#### Desafío
Cambiá la segunda línea para que `prueba` sea una copia de verdad. Así el original sigue empezando con `70`.

#### Código inicial
```csharp
int[] volumenes = { 70, 40, 90 };
int[] prueba = volumenes;
prueba[0] = 10;
Console.WriteLine(volumenes[0]);
```

#### Salida esperada
```
70
```

#### Solución
```csharp
int[] volumenes = { 70, 40, 90 };
int[] prueba = (int[])volumenes.Clone();
prueba[0] = 10;
Console.WriteLine(volumenes[0]);
```

#### Al superarla
Ahora Bemol puede probar lo que quiera en su copia. Clave respira aliviada.

#### Imagen
- Dos hojas iguales sobre una mesa, una al lado de la otra, una con tachones y la otra limpia, sin letras.
- Bemol muestra su hoja tachada con orgullo; Ceci protege la hoja limpia de Clave.

### Micro-misión R01-N12-P5 · El troll de las dos copias

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
criatura: troll
carta: Referencia compartida | dos nombres, un solo arreglo · lo que cambia uno, lo ve el otro
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
El troll de las referencias le dio a Ceci y a Bemol «sus propias» listas de afinación. Ceci afinó la suya, y la de Bemol amaneció cambiada.

#### Gheco sugiere
El troll usa `=` con arreglos para que dos nombres compartan el mismo estante. Si cada uno tiene que tener lo suyo, se copia con `Clone()` desde el principio.

#### Desafío
Ejecutalo: la lista de Bemol muestra `442`, aunque nadie la tocó. Arreglá la segunda línea con `Clone()` para que la de Bemol siga en `440`.

#### Código inicial
```csharp
int[] deCeci = { 440, 440 };
int[] deBemol = deCeci;
deCeci[0] = 442;
Console.WriteLine($"Ceci: {deCeci[0]}");
Console.WriteLine($"Bemol: {deBemol[0]}");
```

#### Salida esperada
```
Ceci: 442
Bemol: 440
```

#### Solución
```csharp
int[] deCeci = { 440, 440 };
int[] deBemol = (int[])deCeci.Clone();
deCeci[0] = 442;
Console.WriteLine($"Ceci: {deCeci[0]}");
Console.WriteLine($"Bemol: {deBemol[0]}");
```

#### Al superarla
El troll se rasca el pelo enredado. Sin estantes compartidos, no tiene nada que desordenar.

#### Imagen
- Dos diapasones de afinar sobre dos atriles distintos, iguales, brillando bajo un farol.
- Un troll chiquito y gruñón, sin armas, espía detrás de un atril; Gheco lo señala.

### Encargo R01-N12-E1 · Los asientos del teatro de Hilván

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Hilván, el titiritero de la Feria y hermano de Ceci, tiene el plano de las butacas de su teatro: `'X'` es ocupada y `'.'` es libre. Mostrá el plano fila por fila, y después cuántas butacas libres quedan.

```
XX.X
.X..
XXX.
Libres: 5
```

#### Criterio de aprobación

- Guarda el plano en una matriz `char[,]`.
- Lo recorre con dos `for` y `GetLength`.

#### Salida esperada

```
XX.X
.X..
XXX.
Libres: 5
```

#### Solución de referencia

```csharp
char[,] butacas =
{
    { 'X', 'X', '.', 'X' },
    { '.', 'X', '.', '.' },
    { 'X', 'X', 'X', '.' },
};
int libres = 0;
for (int f = 0; f < butacas.GetLength(0); f++)
{
    for (int c = 0; c < butacas.GetLength(1); c++)
    {
        Console.Write(butacas[f, c]);
        if (butacas[f, c] == '.') libres++;
    }
    Console.WriteLine();
}
Console.WriteLine($"Libres: {libres}");
```

## R01-N13 · Métodos: los movimientos de la obra

```meta
tipo: tema
padre: R01-N12
precio: 10
criatura: esqueleto
temas: prog.funciones
usa: prog.variables, prog.condicionales
```

### Crónica

La partitura sin terminar tiene una parte que se repite cinco veces: el estribillo. Clave no lo copió cinco veces: lo escribió una sola vez, al margen, con un nombre, y en cada lugar puso «acá va el estribillo».

—Eso es un **método** —dice {mentor}—. Escribís algo una vez, le ponés nombre, y lo llamás cuando lo necesitás. Si mañana cambia, lo cambiás en un solo lugar.

### Objetivos

- Escribir un método con `static` y llamarlo por su nombre.
- Pasarle datos con **parámetros**.
- Devolver un resultado con `return`.
- Dar un valor por defecto a un parámetro.

### Antes de empezar

- Las decisiones (R01-N09) y los bucles (R01-N10).

### Explicación

#### Definir y llamar

En un programa como los nuestros, los métodos se escriben **abajo**, después de lo que se ejecuta:

```csharp
Saludar();
Saludar();

static void Saludar()
{
    Console.WriteLine("¡Buenas noches!");
}
```

`void` quiere decir que **no devuelve** nada: solo hace algo.

#### Parámetros: los datos que recibe

```csharp
Saludar("Ceci");

static void Saludar(string nombre)
{
    Console.WriteLine($"¡Buenas noches, {nombre}!");
}
```

#### `return`: lo que devuelve

En lugar de `void`, se pone el **tipo** de lo que devuelve:

```csharp
int total = Sumar(3, 4);
Console.WriteLine(total);          // 7

static int Sumar(int a, int b)
{
    return a + b;
}
```

#### Valores por defecto

Un parámetro puede tener un valor por defecto, que se usa si no lo pasás:

```csharp
static void Tocar(string obra, int veces = 1)
{
    Console.WriteLine($"{obra} x{veces}");
}
// Tocar("Vals") muestra «Vals x1»; Tocar("Vals", 3) muestra «Vals x3»
```

En el Acto II, cuando los métodos vivan dentro de una **clase**, vas a poder tener varios con el mismo nombre y distintos parámetros (*sobrecarga*). En un programa suelto como estos, cada método tiene que tener un nombre distinto.

### Código de ejemplo

```csharp
Anunciar("Serenata");
Console.WriteLine(Duracion(4, 2));
Repetir("bravo");
Repetir("otra", 2);

static void Anunciar(string obra)
{
    Console.WriteLine($"Ahora suena: {obra}");
}

static int Duracion(int compases, int segundosPorCompas)
{
    return compases * segundosPorCompas;
}

static void Repetir(string palabra, int veces = 1)
{
    for (int i = 0; i < veces; i++) Console.WriteLine(palabra);
}
```

### Salida esperada

```
Ahora suena: Serenata
8
bravo
otra
otra
```

### ¿Para qué sirve?

Un programa de verdad tiene cientos de métodos, cada uno con un trabajo chico y un nombre claro: `CalcularPrecio`, `ValidarEdad`, `MostrarMenu`. Así se lee como una partitura bien escrita, y un error se arregla en un solo lugar.

### Errores habituales

- **Olvidar el `return`:** si dijiste que devuelve `int`, todos los caminos tienen que devolver algo (`CS0161`).
- **Llamarlo con otros datos:** si pide `(string, int)` y le pasás `(int)`, no compila.
- **Escribir el nombre distinto:** `saludar()` y `Saludar()` son dos nombres diferentes. El **esqueleto** de `CS0103` aparece cuando llamás a uno que no existe.

### Micro-misión R01-N13-P1 · El estribillo

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Método | static void Nombre() { … } · se escribe abajo · se llama con Nombre();
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
El estribillo de la partitura se toca dos veces. Clave ya lo escribió como un método: falta llamarlo la segunda vez.

#### Gheco sugiere
Un método se escribe una vez y se **llama** las veces que quieras, con su nombre y paréntesis:

```csharp
Aplaudir();
Aplaudir();

static void Aplaudir()
{
    Console.WriteLine("¡Clap!");
}
```

Muestra `¡Clap!` dos veces.

#### Desafío
Agregá una segunda llamada a `Estribillo()` después de la estrofa.

#### Código inicial
```csharp
Estribillo();
Console.WriteLine("Estrofa");

static void Estribillo()
{
    Console.WriteLine("La la la");
}
```

#### Salida esperada
```
La la la
Estrofa
La la la
```

#### Solución
```csharp
Estribillo();
Console.WriteLine("Estrofa");
Estribillo();

static void Estribillo()
{
    Console.WriteLine("La la la");
}
```

#### Al superarla
—Así se escribe una obra larga sin cansarse —dice Clave—: lo que se repite, se escribe una sola vez.

#### Imagen
- Una partitura grande en un atril, con un recuadro al margen y flechitas que lo señalan, sin letras.
- Clave señala el recuadro con la batuta y Ceci asiente con el violín al hombro.

### Micro-misión R01-N13-P2 · El anuncio con nombre

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Parámetro | static void Anunciar(string obra) · Anunciar("Vals") · el dato entra por los paréntesis
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Bemol anuncia cada obra antes de que suene. Escribió el método, pero siempre anuncia la misma.

#### Gheco sugiere
Un **parámetro** es un dato que el método recibe entre los paréntesis. Adentro se usa como una variable:

```csharp
Felicitar("Ana");

static void Felicitar(string quien)
{
    Console.WriteLine($"¡Feliz cumple, {quien}!");
}
```

#### Desafío
Agregale al método un parámetro `string obra` y usalo en el anuncio, en lugar de «algo».

#### Código inicial
```csharp
Anunciar("Minueto");
Anunciar("Vals");

static void Anunciar()
{
    Console.WriteLine("Ahora suena: algo");
}
```

#### Salida esperada
```
Ahora suena: Minueto
Ahora suena: Vals
```

#### Solución
```csharp
Anunciar("Minueto");
Anunciar("Vals");

static void Anunciar(string obra)
{
    Console.WriteLine($"Ahora suena: {obra}");
}
```

#### Al superarla
Bemol anuncia cada obra con voz de locutor, y el público se ríe.

#### Imagen
- Un escenario con el telón a medio abrir y un banquito vacío en el centro, a la luz de faroles.
- Bemol, de pie al borde del escenario, anuncia con los brazos abiertos; Ceci espera detrás del telón.

### Micro-misión R01-N13-P3 · Cuánto dura

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: return | static int Nombre(…) { return valor; } · el tipo de adelante es el de lo que devuelve
recompensa: xp 15, oro 15
```

#### Escena
Clave quiere un método que calcule la duración de una obra: los compases por los segundos que dura cada uno.

#### Gheco sugiere
Un método que **devuelve** algo dice el tipo adelante y usa `return`:

```csharp
int area = Area(3, 4);
Console.WriteLine(area);

static int Area(int ancho, int alto)
{
    return ancho * alto;
}
```

Muestra `12`.

#### Desafío
Completá el método para que devuelva `compases * segundos`.

#### Código inicial
```csharp
Console.WriteLine(Duracion(32, 3));

static int Duracion(int compases, int segundos)
{
    return 0;
}
```

#### Salida esperada
```
96
```

#### Solución
```csharp
Console.WriteLine(Duracion(32, 3));

static int Duracion(int compases, int segundos)
{
    return compases * segundos;
}
```

#### Al superarla
—Noventa y seis segundos: un minuto y medio largo —calcula Ceci de cabeza.

#### Imagen
- Un metrónomo y un reloj de arena sobre una mesa de madera, al lado de una partitura cerrada.
- Clave mira el reloj de arena con atención mientras Ceci cuenta compases con el dedo.

### Micro-misión R01-N13-P4 · Una vez o varias

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Por defecto | static void Tocar(string obra, int veces = 1) · si no lo pasás, vale 1
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Casi siempre cada obra se toca una vez. Pero cuando el público pide «¡otra!», se repite. Bemol quiere un solo método para los dos casos.

#### Gheco sugiere
Un parámetro puede tener un **valor por defecto**: si al llamarlo no lo pasás, usa ese.

```csharp
Saludar("Ana");
Saludar("Leo", "¡Hola");

static void Saludar(string nombre, string saludo = "Buen día")
{
    Console.WriteLine($"{saludo}, {nombre}");
}
```

Muestra `Buen día, Ana` y `¡Hola, Leo`.

#### Desafío
Dale a `veces` el valor por defecto `1`, para que `Tocar("Vals")` compile y toque una sola vez.

#### Código inicial
```csharp
Tocar("Vals");
Tocar("Bis", 2);

static void Tocar(string obra, int veces)
{
    for (int i = 0; i < veces; i++) Console.WriteLine(obra);
}
```

#### Salida esperada
```
Vals
Bis
Bis
```

#### Solución
```csharp
Tocar("Vals");
Tocar("Bis", 2);

static void Tocar(string obra, int veces = 1)
{
    for (int i = 0; i < veces; i++) Console.WriteLine(obra);
}
```

#### Al superarla
El público grita «¡otra!», y esta vez el programa ya sabe qué hacer.

#### Imagen
- Flores tiradas sobre el borde de un escenario de madera, a la luz de las velas.
- Ceci hace una reverencia con el violín y Bemol, al costado, toca el tambor de festejo.

### Micro-misión R01-N13-P5 · El esqueleto del nombre equivocado

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
criatura: esqueleto
carta: CS0103 | llamar a un método que no existe · Afinar y afinar son nombres distintos
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un esqueleto chiquito, que vive de los nombres que no existen, cambió una letra en la llamada. El programa ya no compila.

#### Gheco sugiere
C# distingue mayúsculas de minúsculas: `Afinar` y `afinar` son dos nombres distintos. Si llamás a uno que no está escrito, el compilador avisa `CS0103: El nombre no existe en el contexto actual`.

#### Desafío
Ejecutalo y leé el error del esqueleto. Arreglá la llamada para que use el nombre exacto del método.

#### Código inicial
```csharp
afinar();

static void Afinar()
{
    Console.WriteLine("La 440");
}
```

#### Salida esperada
```
La 440
```

#### Solución
```csharp
Afinar();

static void Afinar()
{
    Console.WriteLine("La 440");
}
```

#### Al superarla
El esqueleto busca su nombre en la partitura, no lo encuentra, y se desarma en una pila de huesitos que se va rodando.

#### Imagen
- Una pila de huesitos de caricatura rodando por el piso de piedra de una sala de ensayo, sin sangre.
- Gheco, sorprendido, mira rodar los huesitos desde el borde de un atril.

### Encargo R01-N13-E1 · La calculadora de Elefa

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Elefa, la jefa del Puerto, cobra los envíos por peso: `50` monedas fijas más `12` por kilo. Escribí un método `Costo(int kilos)` que devuelva el precio, y otro `Mostrar(string destino, int kilos)` que muestre la línea del recibo usando `Costo`. Mostrá tres envíos:

```
Feria (2 kg): 74
Conservatorio (5 kg): 110
Forjas (0 kg): 50
```

#### Criterio de aprobación

- Tiene un método que devuelve con `return` y otro `void` que lo llama.
- Los envíos se muestran llamando al método, no con cuentas sueltas.

#### Salida esperada

```
Feria (2 kg): 74
Conservatorio (5 kg): 110
Forjas (0 kg): 50
```

#### Solución de referencia

```csharp
Mostrar("Feria", 2);
Mostrar("Conservatorio", 5);
Mostrar("Forjas", 0);

static int Costo(int kilos)
{
    return 50 + 12 * kilos;
}

static void Mostrar(string destino, int kilos)
{
    Console.WriteLine($"{destino} ({kilos} kg): {Costo(kilos)}");
}
```

## R01-N14 · Más de un resultado y la obra que se llama a sí misma

```meta
tipo: tema
padre: R01-N13
precio: 10
criatura: troll
temas: prog.funciones, prog.recursion, col.registros
usa: prog.referencias, prog.condicionales
```

### Crónica

Clave le da a Ceci un método que devuelve el compás más largo de la partitura. —¿Y si quiero también el más corto? —pregunta Ceci. —Entonces el método tiene que devolver **dos cosas**.

En la última página, la melodía de la cajita tiene una marca rara: «repetir, cada vez un poco más corto, hasta que no quede nada». Clave sonríe. —Una música que se llama a sí misma.

### Objetivos

- Entender que un método recibe **copias** de los números.
- Devolver dos o más resultados con una **tupla**: `(int, int)`.
- Saber qué hacen `ref` y `out`.
- Escribir un método recursivo, con su caso que termina.

### Antes de empezar

- Los métodos (R01-N13).

### Explicación

#### Un método recibe copias

```csharp
int volumen = 5;
Subir(volumen);
Console.WriteLine(volumen);   // 5: no cambió

static void Subir(int v) { v += 10; }
```

`Subir` cambia **su copia**, no la variable de afuera. Lo normal es **devolver** el valor nuevo: `volumen = Subir(volumen);`.

#### Devolver dos cosas: una tupla

```csharp
var (menor, mayor) = Extremos(4, 9, 2);
Console.WriteLine($"{menor} {mayor}");   // 2 9

static (int, int) Extremos(int a, int b, int c)
{
    return (Math.Min(a, Math.Min(b, c)), Math.Max(a, Math.Max(b, c)));
}
```

El tipo `(int, int)` es una tupla: dos valores que viajan juntos. Con `var (x, y) = …` se separan en dos variables.

#### `ref` y `out`

- `ref` le pasa **la variable misma**, no una copia: lo que cambie el método, cambia afuera. Se escribe al definir **y** al llamar: `Subir(ref volumen)`.
- `out` es para variables que el método tiene que **llenar**. Ya lo usaste: `int.TryParse(texto, out int n)`.

Se usan poco: casi siempre, una tupla es más clara.

#### Recursión: un método que se llama a sí mismo

```csharp
static void Eco(int veces)
{
    if (veces == 0) return;      // el caso que corta
    Console.WriteLine("eco");
    Eco(veces - 1);              // se llama con un problema más chico
}
```

Siempre necesita **un caso que corte**. Sin él, se llama para siempre hasta que se rompe (`StackOverflowException`, el **troll** de la pila infinita).

### Código de ejemplo

```csharp
var (menor, mayor) = Extremos(new int[] { 7, 3, 9, 5 });
Console.WriteLine($"Más corto: {menor}, más largo: {mayor}");

int volumen = 5;
SubirVolumen(ref volumen);
Console.WriteLine(volumen);

Cuenta(3);

static (int, int) Extremos(int[] compases)
{
    int menor = compases[0];
    int mayor = compases[0];
    foreach (int c in compases)
    {
        menor = Math.Min(menor, c);
        mayor = Math.Max(mayor, c);
    }
    return (menor, mayor);
}

static void SubirVolumen(ref int v)
{
    v += 10;
}

static void Cuenta(int n)
{
    if (n == 0)
    {
        Console.WriteLine("¡Ya!");
        return;
    }
    Console.WriteLine(n);
    Cuenta(n - 1);
}
```

### Salida esperada

```
Más corto: 3, más largo: 9
15
3
2
1
¡Ya!
```

### ¿Para qué sirve?

Muchas preguntas tienen dos respuestas: el mínimo y el máximo, el cociente y el resto, si salió bien y el resultado. La tupla las devuelve juntas sin inventar nada raro. Y la recursión resuelve con muy poco código los problemas que se parecen a sí mismos: las carpetas dentro de carpetas, los árboles, los laberintos.

### Errores habituales

- **Esperar que el método cambie tu variable:** recibe una copia. Devolvé el valor nuevo, o usá `ref` si de verdad hace falta.
- **Olvidar `ref` al llamar:** si el método lo pide, la llamada también lo lleva: `Subir(ref x)`.
- **Recursión sin caso que corte:** se llama para siempre y el **troll** de `StackOverflowException` corta el programa.

### Micro-misión R01-N14-P1 · La copia que no vuelve

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
carta: Copias | un método recibe COPIAS de los números · para cambiar afuera: x = Metodo(x)
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Bemol escribió un método para subir el tempo, pero el tempo no sube: sigue en 60.

#### Gheco sugiere
El método trabaja con una **copia** del número. Para que el cambio llegue afuera, el método lo **devuelve** y lo guardás:

```csharp
int precio = 100;
precio = ConDescuento(precio);
Console.WriteLine(precio);

static int ConDescuento(int p) => p - 10;
```

Muestra `90`.

#### Desafío
Guardá lo que devuelve `Acelerar` en `tempo`, para que muestre `80`.

#### Código inicial
```csharp
int tempo = 60;
Acelerar(tempo);
Console.WriteLine(tempo);

static int Acelerar(int t)
{
    return t + 20;
}
```

#### Salida esperada
```
80
```

#### Solución
```csharp
int tempo = 60;
tempo = Acelerar(tempo);
Console.WriteLine(tempo);

static int Acelerar(int t)
{
    return t + 20;
}
```

#### Al superarla
El metrónomo se acelera, y Bemol tiene que correr detrás con el tambor.

#### Imagen
- Un metrónomo de madera con la aguja moviéndose rápido, con líneas de movimiento.
- Bemol toca el tambor a toda velocidad, despeinado, y Ceci se ríe.

### Micro-misión R01-N14-P2 · El más corto y el más largo

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Tupla | static (int, int) M() { return (a, b); } · var (x, y) = M(); · dos valores juntos
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Clave quiere el compás más corto y el más largo de la partitura, de una sola vez.

#### Gheco sugiere
Una **tupla** devuelve varios valores juntos, entre paréntesis. Al recibirla, `var (x, y)` los separa:

```csharp
var (cociente, resto) = Dividir(17, 5);
Console.WriteLine($"{cociente} y sobran {resto}");

static (int, int) Dividir(int a, int b) => (a / b, a % b);
```

Muestra `3 y sobran 2`.

#### Desafío
Hacé que el método devuelva `(menor, mayor)` en lugar de `(0, 0)`.

#### Código inicial
```csharp
var (corto, largo) = Extremos(4, 9);
Console.WriteLine($"{corto} y {largo}");

static (int, int) Extremos(int a, int b)
{
    int menor = Math.Min(a, b);
    int mayor = Math.Max(a, b);
    return (0, 0);
}
```

#### Salida esperada
```
4 y 9
```

#### Solución
```csharp
var (corto, largo) = Extremos(4, 9);
Console.WriteLine($"{corto} y {largo}");

static (int, int) Extremos(int a, int b)
{
    int menor = Math.Min(a, b);
    int mayor = Math.Max(a, b);
    return (menor, mayor);
}
```

#### Al superarla
Clave marca los dos compases en la partitura con un lápiz suave.

#### Imagen
- Una partitura abierta con dos compases rodeados con un círculo de lápiz, sin letras.
- Clave sostiene el lápiz y Ceci mira por encima de su hombro.

### Micro-misión R01-N14-P3 · La variable de verdad

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
carta: ref | static void M(ref int x) · M(ref volumen) · el método cambia la variable de afuera
recompensa: xp 15, oro 15
```

#### Escena
El órgano tiene una perilla y Ceci quiere un método que la gire de verdad, sin devolver nada.

#### Gheco sugiere
Con `ref`, el método recibe **la variable misma** y no una copia. Va en los dos lados: al escribir el método y al llamarlo.

```csharp
int vidas = 3;
Perder(ref vidas);
Console.WriteLine(vidas);

static void Perder(ref int v) { v--; }
```

Muestra `2`.

#### Desafío
Agregá `ref` en el parámetro del método y en la llamada, para que `perilla` quede en `50`.

#### Código inicial
```csharp
int perilla = 30;
Girar(perilla);
Console.WriteLine(perilla);

static void Girar(int p)
{
    p += 20;
}
```

#### Salida esperada
```
50
```

#### Solución
```csharp
int perilla = 30;
Girar(ref perilla);
Console.WriteLine(perilla);

static void Girar(ref int p)
{
    p += 20;
}
```

#### Al superarla
El órgano suena un poco más fuerte, y Gheco se agarra del atril para no volar.

#### Imagen
- La perilla grande de bronce de un órgano, girada, con los tubos dorados detrás.
- Gheco se agarra fuerte del borde de un atril, despeinado por el sonido; Ceci gira la perilla.

### Micro-misión R01-N14-P4 · La cuenta regresiva

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Recursión | el método se llama a sí mismo con algo más chico · necesita un caso que corte
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Antes del concierto, Clave cuenta hacia atrás desde 3 y dice «¡Arriba el telón!». Ceci quiere hacerlo con un método que se llama a sí mismo.

#### Gheco sugiere
Un método **recursivo** se llama a sí mismo con un problema más chico, hasta llegar a un caso que corta:

```csharp
Bajar(2);

static void Bajar(int n)
{
    if (n == 0) return;
    Console.WriteLine(n);
    Bajar(n - 1);
}
```

Muestra `2` y `1`.

#### Desafío
Completá el caso que corta: cuando `n` es `0`, mostrá `¡Arriba el telón!` y terminá con `return`.

#### Código inicial
```csharp
Cuenta(3);

static void Cuenta(int n)
{
    Console.WriteLine(n);
    Cuenta(n - 1);
}
```

#### Salida esperada
```
3
2
1
¡Arriba el telón!
```

#### Solución
```csharp
Cuenta(3);

static void Cuenta(int n)
{
    if (n == 0)
    {
        Console.WriteLine("¡Arriba el telón!");
        return;
    }
    Console.WriteLine(n);
    Cuenta(n - 1);
}
```

#### Al superarla
El telón sube justo cuando Clave dice «¡Arriba!». Del otro lado, el público aplaude.

#### Imagen
- Un telón de terciopelo bordó levantándose sobre un escenario iluminado, con público en penumbra.
- Clave, de espaldas al público, levanta la batuta; Ceci está lista con el violín.

### Micro-misión R01-N14-P5 · El troll de la pila infinita

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
criatura: troll
carta: StackOverflow | recursión que nunca corta · el caso base tiene que llegar · n - 1, no n + 1
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
El troll escribió una melodía recursiva que «se achica en cada vuelta»… pero en vez de achicarse, crece. Nunca llega al final.

#### Gheco sugiere
Para que la recursión termine, cada llamada tiene que **acercarse** al caso que corta. Si va al revés, se llama para siempre y el programa se rompe con `StackOverflowException`.

#### Desafío
Ejecutalo y mirá cómo se rompe. Arreglá la llamada para que `n` baje en lugar de subir.

#### Código inicial
```csharp
Nota(4);

static void Nota(int n)
{
    if (n == 0) return;
    Console.WriteLine($"Nota de {n} tiempos");
    Nota(n + 1);
}
```

#### Salida esperada
```
Nota de 4 tiempos
Nota de 3 tiempos
Nota de 2 tiempos
Nota de 1 tiempos
```

#### Solución
```csharp
Nota(4);

static void Nota(int n)
{
    if (n == 0) return;
    Console.WriteLine($"Nota de {n} tiempos");
    Nota(n - 1);
}
```

#### Al superarla
La melodía baja, nota por nota, hasta el silencio. El troll, que esperaba un concierto infinito, se queda dormido.

#### Imagen
- Una escalera de notas musicales que baja, cada vez más chicas, sobre una pared de piedra iluminada.
- Un troll chiquito y gruñón, sin armas, dormido sentado contra la pared; Gheco le pone una manta.

### Encargo R01-N14-E1 · Las cuentas de Tizón

```meta
entrega: codigo
entorno: navegador
monedas: 1
xp: 15
```

#### Consigna

Tizón, el herrero de las Forjas, reparte lingotes. Escribí un método `Repartir(int lingotes, int herreros)` que devuelva una tupla con cuántos le tocan a cada uno y cuántos sobran. Y un método **recursivo** `Potencia(int n)` que devuelva cuántos lingotes salen si cada horno duplica lo del anterior, `n` veces, empezando en 1 (`Potencia(0)` es `1`). Mostrá:

```
Cada herrero: 4, sobran: 2
Con 5 hornos: 32 lingotes
```

#### Criterio de aprobación

- `Repartir` devuelve una tupla `(int, int)`.
- `Potencia` es recursivo y tiene su caso que corta.

#### Salida esperada

```
Cada herrero: 4, sobran: 2
Con 5 hornos: 32 lingotes
```

#### Solución de referencia

```csharp
var (cada, sobran) = Repartir(26, 6);
Console.WriteLine($"Cada herrero: {cada}, sobran: {sobran}");
Console.WriteLine($"Con 5 hornos: {Potencia(5)} lingotes");

static (int, int) Repartir(int lingotes, int herreros)
{
    return (lingotes / herreros, lingotes % herreros);
}

static int Potencia(int n)
{
    if (n == 0) return 1;
    return 2 * Potencia(n - 1);
}
```

## R01-N15 · Jefe: el Slime Desafinado

```meta
tipo: jefe
padre: R01-N14
precio: 10
criatura: slime
insignia: Oído Afinado
insignia_descripcion: Venciste al Slime Desafinado: dominás los fundamentos de C# y sabés leer los errores del ensayo general.
usa: prog.variables, prog.cadenas, prog.entrada, prog.condicionales, prog.bucles, col.arrays, prog.funciones
```

### Crónica

La noche del concierto, la Sala de Ensayo amanece pegajosa. Un **slime verde y gelatinoso** se trepó al atril grande y se comió los signos de la partitura: faltan puntos y comas, llaves, comillas. Cuando Ceci intenta tocar, el compilador no la deja pasar del ensayo general.

—Es el **Slime Desafinado** —dice {mentor}—. Vive de los errores de escritura. No se lo vence tocando más fuerte: se lo vence **leyendo** lo que dice el compilador, arreglando de a uno, y ensayando de nuevo. Usá todo lo que aprendiste en la Sala.

### Objetivos

- Leer un error de compilación: el archivo, la **línea**, la columna y el código (`CS1002`, `CS1513`…).
- Arreglar los errores de a uno, empezando por el **primero**.
- Juntar en un programa todo lo de la Sala: textos, lectura, decisiones, bucles, arreglos y métodos.

### Antes de empezar

- Todos los nodos de la Sala de Ensayo (R01-N01 a R01-N14).

### Explicación

#### Cómo se lee un error

```
Programa.cs(3,30): error CS1002: Se esperaba ;
```

- `(3,30)`: **línea 3**, columna 30. Ahí, o justo antes, está el problema.
- `CS1002`: el código del error. Cada uno tiene su significado.
- `Se esperaba ;`: lo que el compilador no encontró.

#### Los signos que se come el Slime

| Error | Qué falta | Cómo se ve |
|---|---|---|
| `CS1002` | un `;` al final de una orden | `int x = 5` |
| `CS1513` | una `}` que cierre | un `if` o un método sin cerrar |
| `CS1026` | un `)` | `Console.WriteLine("hola"` |
| `CS1010` | una comilla que cierre el texto | `"hola` |

#### Cómo vencer a un jefe

1. **Ensayá** (ejecutá) y leé **solo el primer error**. A veces uno solo causa varios.
2. Andá a esa línea, arreglalo y ensayá otra vez.
3. Cuando compila, revisá que **haga lo que tiene que hacer**: ahí empiezan los ogros.

### Código de ejemplo

```csharp
string[] obras = { "Serenata", "Minueto", "Nocturno" };
int total = 0;

for (int i = 0; i < obras.Length; i++)
{
    int duracion = Duracion(obras[i]);
    total += duracion;
    Console.WriteLine($"{i + 1}. {obras[i].ToUpper(),-10}{duracion,3} min");
}
Console.WriteLine($"Total: {total} min");

static int Duracion(string obra)
{
    return obra.Length switch
    {
        <= 7 => 4,
        <= 8 => 6,
        _ => 8,
    };
}
```

### Salida esperada

```
1. SERENATA    6 min
2. MINUETO     4 min
3. NOCTURNO    6 min
Total: 16 min
```

### ¿Para qué sirve?

Todo programador, todos los días, lee errores del compilador. El que sabe leerlos arregla en un minuto lo que a otro le lleva una tarde. Y después de vencer al Slime, ya sabés escribir programas completos: leen, deciden, repiten y se ordenan en métodos.

### Errores habituales

- **Arreglar el último error primero:** muchas veces desaparecen solos cuando arreglás el primero.
- **Buscar en otra línea:** el número que da el compilador es el mejor lugar para empezar a mirar.
- **Creer que compilar es terminar:** un programa que compila todavía puede dar otra cosa.

### Micro-misión R01-N15-P1 · El punto y coma que se comió

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Gheco
criatura: slime
carta: CS1002 | Se esperaba ; · cada orden termina con punto y coma · mirá la línea que dice el error
recompensa: xp 20, oro 20, monedas 4
```

#### Escena
El Slime se comió los puntos y comas de las dos primeras líneas. El compilador avisa en qué línea falta cada uno.

#### Gheco sugiere
El error dice la línea entre paréntesis: `(1,21)` es la línea 1. Cada orden termina con `;`.

#### Desafío
Ejecutalo, leé las líneas del error y poné los `;` que faltan.

#### Código inicial
```csharp
string obra = "Vals"
int compases = 24
Console.WriteLine($"{obra}: {compases} compases");
```

#### Salida esperada
```
Vals: 24 compases
```

#### Solución
```csharp
string obra = "Vals";
int compases = 24;
Console.WriteLine($"{obra}: {compases} compases");
```

#### Al superarla
Un pedazo de slime se despega del atril y cae al piso con un *plop*.

#### Imagen
- Un slime verde brillante y gelatinoso, enorme, trepado a un atril grande; adentro flotan puntitos y comas, sin letras.
- Ceci, con el violín en la mano, se acerca decidida; Gheco, en su hombro, señala el atril.

### Micro-misión R01-N15-P2 · La llave que no cierra

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
criatura: slime
carta: CS1513 | Se esperaba } · cada { tiene su } · contá las llaves de un if o de un bucle
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
El Slime se comió la llave que cerraba el `for` del repertorio. El compilador se queja al final del archivo, porque ahí se dio cuenta de que faltaba.

#### Gheco sugiere
Cada `{` tiene que tener su `}`. Cuando falta una, el error aparece **al final**, aunque el problema esté antes: contá las llaves de cada bloque.

#### Desafío
Agregá la llave que cierra el `for`, antes de mostrar el total.

#### Código inicial
```csharp
int[] minutos = { 6, 4, 6 };
int total = 0;
for (int i = 0; i < minutos.Length; i++)
{
    total += minutos[i];
Console.WriteLine($"Total: {total} min");
```

#### Salida esperada
```
Total: 16 min
```

#### Solución
```csharp
int[] minutos = { 6, 4, 6 };
int total = 0;
for (int i = 0; i < minutos.Length; i++)
{
    total += minutos[i];
}
Console.WriteLine($"Total: {total} min");
```

#### Al superarla
—Así se lee un error —dice Clave—: no dónde se queja, sino dónde empezó.

#### Imagen
- Un slime verde que se encoge un poco sobre el atril, con gotas cayendo al piso de piedra.
- Clave, de brazos cruzados, observa a Ceci que escribe en una partitura con un lápiz.

### Micro-misión R01-N15-P3 · Las comillas abiertas

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Bemol
criatura: slime
carta: CS1010 | texto sin cerrar · cada " de apertura tiene su " de cierre · también el ) del WriteLine
recompensa: xp 20, oro 20
```

#### Escena
Ahora el Slime se comió una comilla y un paréntesis del anuncio del concierto. Bemol ve tres errores, pero son dos cosas.

#### Gheco sugiere
Un texto sin su comilla de cierre confunde al compilador por el resto de la línea, y puede dar varios errores. Arreglá el primero y ensayá otra vez.

#### Desafío
Cerrá el texto con su comilla y el `WriteLine` con su paréntesis.

#### Código inicial
```csharp
string sala = "Conservatorio";
Console.WriteLine($"Esta noche, concierto en el {sala}!);
```

#### Salida esperada
```
Esta noche, concierto en el Conservatorio!
```

#### Solución
```csharp
string sala = "Conservatorio";
Console.WriteLine($"Esta noche, concierto en el {sala}!");
```

#### Al superarla
—¿Y por qué daba tres errores si eran dos cosas? —pregunta Bemol. —Porque una comilla abierta lo confunde todo —le contesta Ceci.

#### Imagen
- Un cartel de concierto liso pegado en una puerta de madera, con una mancha verde de slime que se escurre.
- Bemol se rasca la cabeza frente al cartel y Ceci limpia la mancha con un pañuelo.

### Micro-misión R01-N15-P4 · El programa del público

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave
carta: Todo junto | ReadLine + TryParse + if + bucle · arreglá el error y revisá que haga lo que pide
recompensa: xp 20, oro 20, monedas 3
```

#### Escena
El Slime escondió un error en el programa que cuenta cuántas obras pide el público, y dejó un ogro adentro: cuenta mal. Hay que arreglar los dos.

#### Gheco sugiere
Primero que compile. Después, que dé lo correcto: el programa lee pedidos hasta que escriben `fin`, y cuenta solo los que son números del 1 al 3 (las obras que hay).

#### Desafío
Arreglá el error de compilación (falta un `;`) y la condición del `if`, que también cuenta el `4`, que no es una obra.

#### Código inicial
```csharp
int validos = 0
while (true)
{
    string linea = Console.ReadLine() ?? "fin";
    if (linea == "fin") break;
    if (int.TryParse(linea, out int obra) && obra >= 1 && obra <= 4)
    {
        validos++;
    }
}
Console.WriteLine($"Pedidos válidos: {validos}");
```

#### Entrada
```
1
3
4
dos
2
fin
```

#### Salida esperada
```
Pedidos válidos: 3
```

#### Solución
```csharp
int validos = 0;
while (true)
{
    string linea = Console.ReadLine() ?? "fin";
    if (linea == "fin") break;
    if (int.TryParse(linea, out int obra) && obra >= 1 && obra <= 3)
    {
        validos++;
    }
}
Console.WriteLine($"Pedidos válidos: {validos}");
```

#### Al superarla
El slime se achica hasta quedar del tamaño de una pelota. Todavía le queda fuerza para el último golpe.

#### Imagen
- Un slime verde, ahora chico como una pelota, rebotando nervioso sobre una mesa con papelitos de pedidos.
- Clave sostiene una pila de papelitos y Ceci cuenta los buenos.

### Micro-misión R01-N15-P5 · El concierto completo

```meta
lugar: La Sala de Ensayo
personajes: Ceci, Clave, Bemol, Gheco
criatura: slime
carta: Jefe | métodos + arreglo + bucle + formato · un error a la vez · al final, que suene bien
recompensa: xp 30, oro 30, monedas 3
item: Diapasón Verde
```

#### Escena
Es el último truco del Slime: el programa del concierto entero, con un método que se llama mal y un número con formato roto. Si compila y suena, el Slime se disuelve para siempre.

#### Gheco sugiere
Hay dos errores. Leé el primero, arreglalo y ensayá: el segundo aparece cuando el primero desaparece. El método se llama `Anunciar`, con mayúscula, y el formato de dos decimales es `:F2`.

#### Desafío
Arreglá la llamada al método y el formato del precio, para que el concierto salga completo.

#### Código inicial
```csharp
string[] obras = { "Serenata", "Minueto", "Nocturno" };
double entrada = 7.5;

for (int i = 0; i < obras.Length; i++)
{
    anunciar(i + 1, obras[i]);
}
Console.WriteLine($"Entrada: {entrada:F2");

static void Anunciar(int numero, string obra)
{
    Console.WriteLine($"{numero}. {obra}");
}
```

#### Salida esperada
```
1. Serenata
2. Minueto
3. Nocturno
Entrada: 7,50
```

#### Solución
```csharp
string[] obras = { "Serenata", "Minueto", "Nocturno" };
double entrada = 7.5;

for (int i = 0; i < obras.Length; i++)
{
    Anunciar(i + 1, obras[i]);
}
Console.WriteLine($"Entrada: {entrada:F2}");

static void Anunciar(int numero, string obra)
{
    Console.WriteLine($"{numero}. {obra}");
}
```

#### Al superarla
El programa compila, y el concierto suena de punta a punta. El Slime Desafinado se disuelve en un charquito verde que se evapora con el último acorde. En el piso queda un diapasón de cristal verde que todavía zumba bajito: **el Diapasón Verde**. Clave guarda la partitura sin terminar y mira a Ceci: —Ahora sí sabés escribir antes de tocar. Mañana te espera el Taller de Instrumentos.

#### Imagen
- La sala de ensayo iluminada con velas, el atril grande limpio y brillante, y un charquito verde evaporándose en el piso.
- Ceci toca el violín con los ojos cerrados; Clave, Bemol con su tambor y Gheco la escuchan sonriendo.

### Encargo R01-N15-E1 · La boletería del Conservatorio

```meta
entrega: codigo
entorno: navegador
monedas: 2
xp: 30
```

#### Consigna

El Conservatorio abre la boletería. Escribí un programa con métodos que:

1. Lea pedidos, uno por línea, con el formato `nombre,cantidad` (por ejemplo `Ana,2`), hasta que escriban `fin`.
2. Saltee las líneas mal escritas: sin coma, o con una cantidad que no es un número mayor que 0.
3. Cobre `7,5` por entrada, con un método `Precio(int cantidad)` que devuelva el total de ese pedido.
4. Muestre cada pedido válido con el nombre en mayúsculas y el precio con dos decimales, y al final cuántas entradas se vendieron y la recaudación.

Con esta Entrada:

```
Ana,2
Bruno
Leo,x
Mirta,3
fin
```

muestra:

```
ANA: 15,00
MIRTA: 22,50
Entradas: 5
Recaudación: 37,50
```

#### Criterio de aprobación

- Usa `Split`, `TryParse`, un bucle con `break` y al menos un método que devuelve un valor.
- Saltea las líneas mal escritas sin romperse.
- Muestra los importes con dos decimales.

#### Entrada de ejemplo

```
Ana,2
Bruno
Leo,x
Mirta,3
fin
```

#### Salida esperada

```
ANA: 15,00
MIRTA: 22,50
Entradas: 5
Recaudación: 37,50
```

#### Pruebas

##### Nada vendido
```entrada
fin
```
```salida
Entradas: 0
Recaudación: 0,00
```

##### Cantidad en cero
```entrada
Leo,0
Ana,1
fin
```
```salida
ANA: 7,50
Entradas: 1
Recaudación: 7,50
```

#### Solución de referencia

```csharp
int entradas = 0;
double recaudacion = 0;

while (true)
{
    string linea = Console.ReadLine() ?? "fin";
    if (linea == "fin") break;
    string[] partes = linea.Split(',');
    if (partes.Length != 2) continue;
    if (!int.TryParse(partes[1], out int cantidad) || cantidad <= 0) continue;

    double total = Precio(cantidad);
    Console.WriteLine($"{partes[0].Trim().ToUpper()}: {total:F2}");
    entradas += cantidad;
    recaudacion += total;
}
Console.WriteLine($"Entradas: {entradas}");
Console.WriteLine($"Recaudación: {recaudacion:F2}");

static double Precio(int cantidad)
{
    return cantidad * 7.5;
}
```
