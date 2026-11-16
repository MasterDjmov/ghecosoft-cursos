# RAMA S03 · Senda del Puerto: dos ventanillas que se hablan

```meta
tipo: senda
posicion: 9
```

## S03-N01 · Pedirle al Puerto

```meta
tipo: tema
padre: R05-N07
precio: 3
moneda: comodin
criatura: esqueleto
temas: web.http, web.api-rest
usa: conc.async, arch.json, poo.records
```

### Crónica

Una paloma con un sello de lacre violeta entra por la ventanilla del Conservatorio y se posa sobre el mostrador. La carta es de **Elefa**, la Capitana del Puerto de los Mensajeros:

*«Ceci: me contaron que abriste una ventanilla. Nosotros tenemos la nuestra hace veinte años: la **API del Puerto**, que escribió Nilo en PHP. Ahí está todo: qué barcos llegaron, qué traen, los mensajes para cada región. Tu Conservatorio espera cuerdas y violines. No los esperes mirando el mar: **preguntale a mi ventanilla desde la tuya**.»*

Abajo, con otra letra, más apurada: *«¡Y cuidado con Pico! — Nilo.»*

—Una ventanilla que le habla a otra —dice {mentor}, leyendo por encima del hombro de Ceci—. Así se arma casi todo lo que anda por ahí.

### Objetivos

- Pedirle datos a otra API con un `HttpClient`.
- Traer el texto crudo con `GetStringAsync`.
- Traer el JSON ya convertido en un `record` con `GetFromJsonAsync`.
- Pedir una lista entera y un elemento por su número.

### Antes de empezar

- `async` y `await` (R05-N01), JSON (R04-N06) y la ventanilla (R05-N07).

### Explicación

#### Del otro lado del mostrador

En la ventanilla, vos **atendías** pedidos. Ahora vas a **hacerlos**. El que pide es un `HttpClient`: le decís a qué dirección y él trae la respuesta.

En una compu de verdad, se crea con la dirección del Puerto:

```csharp
HttpClient puerto = new HttpClient { BaseAddress = new Uri("https://puerto.codexia/") };
```

En el navegador no hay red, así que el curso trae una **copia del Puerto** que contesta igual que el de verdad. Se pide así, y todo lo demás es idéntico:

```csharp
HttpClient puerto = Puerto.CreateClient();
```

#### Texto crudo o un objeto

Cada pedido tarda (el mensaje tiene que ir y volver), por eso todos son `async` y llevan `await`:

```csharp
string crudo = await puerto.GetStringAsync("hola");
// {"mensaje":"¡Hola, Ceci! …","de":"Elefa"}

Saludo? s = await puerto.GetFromJsonAsync<Saludo>("hola");
Console.WriteLine(s!.Mensaje);

record Saludo(string Mensaje, string De);
```

`GetFromJsonAsync<Saludo>` pide, espera y convierte el JSON en un `Saludo`, todo junto. Entiende los nombres en minúscula (`mensaje` llena `Mensaje`), como las APIs de verdad. El `?` es porque podría llegar vacío; el `!` le promete a C# que no.

#### Una lista, o uno solo

La dirección dice qué querés: `barcos` es la lista entera, y `barcos/2` es el barco número 2.

```csharp
List<Barco>? todos = await puerto.GetFromJsonAsync<List<Barco>>("barcos");
Barco? uno = await puerto.GetFromJsonAsync<Barco>($"barcos/{id}");
```

### Código de ejemplo

```csharp
HttpClient puerto = Puerto.CreateClient();

string crudo = await puerto.GetStringAsync("hola");
Console.WriteLine(crudo);

Saludo? s = await puerto.GetFromJsonAsync<Saludo>("hola");
Console.WriteLine($"{s!.De} dice: {s.Mensaje}");

List<Barco>? barcos = await puerto.GetFromJsonAsync<List<Barco>>("barcos");
foreach (Barco b in barcos!)
{
    Console.WriteLine($"{b.Id}. {b.Nombre}: {b.Carga}");
}

record Saludo(string Mensaje, string De);
record Barco(int Id, string Nombre, string Carga);
```

### Salida esperada

```
{"mensaje":"¡Hola, Ceci! Te escribe Elefa desde el Puerto.","de":"Elefa"}
Elefa dice: ¡Hola, Ceci! Te escribe Elefa desde el Puerto.
1. La Gaviota: violines
2. El Ancla Azul: cuerdas
3. La Marea: sal
4. El Faro Viejo: partituras
```

### ¿Para qué sirve?

Las apps del clima, los mapas, los pagos y los juegos en línea son, por dentro, un programa que le pide datos a la API de otro. `HttpClient` es como C# lo hace, en una consola, en una página o en un servidor.

### Errores habituales

- **Olvidarse el `await`:** sin él, tenés la promesa de una respuesta (`Task<string>`), no la respuesta.
- **Pedir un objeto cuando llega una lista:** `GetFromJsonAsync<Barco>("barcos")` se rompe, porque el JSON empieza con `[`.
- **Un nombre en el `record` que no está en el JSON:** queda vacío, sin avisar. Es el **esqueleto** de los nombres que no existen.

### Micro-misión S03-N01-P1 · El primer mensaje

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Gheco
carta: await | string t = await puerto.GetStringAsync("hola"); · sin await: Task<string>, no el texto
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Ceci le escribe por primera vez al Puerto. Pero el programa no compila: quiere guardar la respuesta en un `string` antes de esperarla.

#### Gheco sugiere
Un pedido devuelve un `Task<string>`: la **promesa** de un texto. `await` espera a que llegue y te da el texto:

```csharp
string notas = await archivo.LeerAsync();   // sin await, sería un Task<string>
```

#### Desafío
Agregá `await` antes de `puerto.GetStringAsync("hola")`.

#### Pasos
1. Cambiá `= puerto.GetStringAsync("hola");` por `= await puerto.GetStringAsync("hola");`.
2. Tocá **Ejecutar** y compará.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();
string crudo = puerto.GetStringAsync("hola");
Console.WriteLine(crudo);
```

#### Salida esperada
```
{"mensaje":"¡Hola, Ceci! Te escribe Elefa desde el Puerto.","de":"Elefa"}
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
string crudo = await puerto.GetStringAsync("hola");
Console.WriteLine(crudo);
```

#### Al superarla
En la pantalla aparece el saludo de Elefa, con llaves y comillas. Ceci se ríe. —Es como leer una carta con el sobre puesto.

#### Imagen
- El mostrador de madera de la Ventanilla de Pedidos del Conservatorio, con una campanilla y una paloma blanca con un sello de lacre violeta en la pata, sin letras.
- Ceci, con su violín a la espalda, lee un papel; Gheco, un gecko de luz cian con antiparras, MINÚSCULO, sentado sobre la campanilla.

### Micro-misión S03-N01-P2 · Sacar la carta del sobre

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Clave
carta: GetFromJsonAsync | Saludo? s = await puerto.GetFromJsonAsync<Saludo>("hola"); · pide y convierte · mensaje llena Mensaje
recompensa: xp 15, oro 15
```

#### Escena
El saludo llega con las llaves y las comillas del JSON. Clave quiere leer solo lo que dice Elefa, sin el sobre.

#### Gheco sugiere
`GetFromJsonAsync<T>` pide y convierte el JSON en un objeto del tipo que digas:

```csharp
Clima? c = await servicio.GetFromJsonAsync<Clima>("clima");
Console.WriteLine(c!.Temperatura);
```

#### Desafío
Cambiá la línea de `crudo` por `Saludo? s = await puerto.GetFromJsonAsync<Saludo>("hola");` y mostrá `s!.Mensaje` en vez de `crudo`.

#### Pasos
1. Cambiá la línea de `crudo` por `Saludo? s = await puerto.GetFromJsonAsync<Saludo>("hola");`.
2. En el `WriteLine`, cambiá `{crudo}` por `{s!.Mensaje}`.
3. Tocá **Ejecutar** y compará.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();
string crudo = await puerto.GetStringAsync("hola");
Console.WriteLine($"Elefa dice: {crudo}");

record Saludo(string Mensaje, string De);
```

#### Salida esperada
```
Elefa dice: ¡Hola, Ceci! Te escribe Elefa desde el Puerto.
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
Saludo? s = await puerto.GetFromJsonAsync<Saludo>("hola");
Console.WriteLine($"Elefa dice: {s!.Mensaje}");

record Saludo(string Mensaje, string De);
```

#### Al superarla
—Mejor —dice Clave—. Las llaves son para la máquina. Las palabras, para nosotras.

#### Imagen
- Una carta abierta con un sello de lacre violeta roto, sobre el mostrador de la ventanilla, junto a su sobre vacío, sin letras legibles.
- Clave, con su capa y la mecha blanca en el rodete, lee la carta con los anteojos en la punta de la nariz; Ceci sostiene el sobre.

### Micro-misión S03-N01-P3 · Todos los barcos

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Bemol
carta: Lista | GetFromJsonAsync<List<Barco>>("barcos") · el JSON empieza con [ · una lista, no un objeto
recompensa: xp 15, oro 15
```

#### Escena
Bemol quiere saber cuántos barcos hay en el muelle. El programa pide un solo `Barco`, pero el Puerto contesta una lista, y el programa se rompe.

#### Gheco sugiere
Si el JSON empieza con `[`, es una lista. El tipo que pedís tiene que ser una lista:

```csharp
List<Nota>? notas = await atril.GetFromJsonAsync<List<Nota>>("notas");
Console.WriteLine(notas!.Count);
```

#### Desafío
Pedí `List<Barco>` en vez de `Barco`, y mostrá `barcos!.Count`.

#### Pasos
1. Cambiá `GetFromJsonAsync<Barco>` por `GetFromJsonAsync<List<Barco>>`.
2. En el `WriteLine`, cambiá `{barcos}` por `{barcos!.Count}`.
3. Tocá **Ejecutar**. Tiene que salir `Barcos en el muelle: 4`.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();
var barcos = await puerto.GetFromJsonAsync<Barco>("barcos");
Console.WriteLine($"Barcos en el muelle: {barcos}");

record Barco(int Id, string Nombre, string Carga);
```

#### Salida esperada
```
Barcos en el muelle: 4
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
var barcos = await puerto.GetFromJsonAsync<List<Barco>>("barcos");
Console.WriteLine($"Barcos en el muelle: {barcos!.Count}");

record Barco(int Id, string Nombre, string Carga);
```

#### Al superarla
—¡Cuatro! —dice Bemol—. ¿Y si uno trae torta? Ceci le muestra la lista: violines, cuerdas, sal y partituras. Bemol suspira.

#### Imagen
- Por la ventana de la ventanilla se ve un muelle lejano con cuatro barcos de velas de colores, al atardecer, sin letras.
- Bemol, MUY GORDITO con panza, cuenta los barcos con los dedos pegado a la ventana; Ceci, a su lado, mira la pantalla.

### Micro-misión S03-N01-P4 · El barco número dos

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Gheco
carta: Uno por número | $"barcos/{id}" · sin el $, la dirección dice {id} literal · y el Puerto contesta 404
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Ceci quiere ver solo el barco número 2, el de las cuerdas. Pero la dirección sale escrita con `{id}`, tal cual, y el Puerto contesta que esa dirección no existe.

#### Gheco sugiere
Para que `{id}` se reemplace por su valor, el texto necesita el `$` adelante:

```csharp
string ruta = $"notas/{numero}";   // "notas/7", no "notas/{numero}"
```

#### Desafío
Agregá el `$` delante de `"barcos/{id}"`.

#### Pasos
1. Cambiá `("barcos/{id}")` por `($"barcos/{id}")`.
2. Tocá **Ejecutar**. Tiene que salir `El Ancla Azul`.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();
int id = 2;
Barco? b = await puerto.GetFromJsonAsync<Barco>("barcos/{id}");
Console.WriteLine($"Barco {b!.Id}: {b.Nombre} trae {b.Carga}");

record Barco(int Id, string Nombre, string Carga);
```

#### Salida esperada
```
Barco 2: El Ancla Azul trae cuerdas
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
int id = 2;
Barco? b = await puerto.GetFromJsonAsync<Barco>($"barcos/{id}");
Console.WriteLine($"Barco {b!.Id}: {b.Nombre} trae {b.Carga}");

record Barco(int Id, string Nombre, string Carga);
```

#### Al superarla
El Ancla Azul, con cuerdas para el Conservatorio. Ceci anota el nombre en su cuaderno, subrayado dos veces.

#### Imagen
- Un barco de vela azul con un ancla pintada en la proa, atracado en un muelle de madera con faroles violetas, sin letras.
- Gheco, MINÚSCULO, flota delante de una pantalla holográfica que muestra el barco; Ceci escribe en un cuaderno.

### Micro-misión S03-N01-P5 · El esqueleto del nombre equivocado

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Gheco
criatura: esqueleto
carta: Esqueleto | el record se llena por nombre · Cargamento no está en el JSON: queda vacío · tiene que llamarse Carga
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un esqueleto del Archivo Mudo le cambió el nombre a una propiedad del `record`: `Cargamento` en vez de `Carga`. Ahora el programa dice que El Faro Viejo no trae nada.

#### Gheco sugiere
El JSON se reparte en el `record` **por nombre**. Si el nombre no coincide, esa propiedad queda vacía, sin ningún error:

```json
{"titulo":"Vals"}
```
```csharp
record Obra(string Titulo);   // Titulo: sí · Nombre: quedaría vacío
```

#### Desafío
Cambiá `Cargamento` por `Carga`, en el `record` y en el `Console.WriteLine`.

#### Pasos
1. En el `WriteLine`, cambiá `b.Cargamento` por `b.Carga`.
2. En el `record`, cambiá `string Cargamento` por `string Carga`.
3. Tocá **Ejecutar** y compará.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();
Barco? b = await puerto.GetFromJsonAsync<Barco>("barcos/4");
Console.WriteLine($"{b!.Nombre} trae {b.Cargamento}");

record Barco(int Id, string Nombre, string Cargamento);
```

#### Salida esperada
```
El Faro Viejo trae partituras
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
Barco? b = await puerto.GetFromJsonAsync<Barco>("barcos/4");
Console.WriteLine($"{b!.Nombre} trae {b.Carga}");

record Barco(int Id, string Nombre, string Carga);
```

#### Al superarla
Partituras. El esqueleto, sin nombres que esconder, junta sus huesos y vuelve caminando al Archivo Mudo, con la cabeza bajo el brazo.

#### Imagen
- La Ventanilla de Pedidos con una pantalla holográfica que muestra un barco con un faro, sin letras.
- Un esqueleto de caricatura, flaco y torpe, se va caminando con su calavera bajo el brazo; Ceci lo mira irse; Gheco, MINÚSCULO, le hace adiós con la mano.

## S03-N02 · Mirar la respuesta

```meta
tipo: tema
padre: S03-N01
precio: 10
criatura: goblin
temas: web.http, err.excepciones
usa: web.api-rest, conc.async
```

### Crónica

Ceci ya le pregunta al Puerto todo el día. Hasta que pide el barco número 9 y el programa explota. —No hay barco 9 —dice Nilo, que vino de visita con su bolso lleno de cartas—. El Puerto te contestó, nomás que te contestó **que no**. Elefa nunca deja un pedido sin respuesta: a veces la respuesta es un 404.

En el techo, una gaviota regordeta, con una mancha violeta en el ala, mira el bolso de Nilo con mucho interés. Es **Pico**.

### Objetivos

- Pedir con `GetAsync` y mirar el **código de estado** antes de leer.
- Leer el cuerpo de la respuesta con `ReadFromJsonAsync`, sea un dato o un error.
- Mandar datos con `PostAsJsonAsync`.
- Cortar con `EnsureSuccessStatusCode` y atrapar `HttpRequestException` y `JsonException`.

### Antes de empezar

- Pedirle al Puerto (S03-N01) y los códigos de la ventanilla (R05-N07): 200, 201, 404, 422, 500.

### Explicación

#### La respuesta entera

`GetFromJsonAsync` es cómodo, pero si el Puerto contesta un error, se rompe. `GetAsync` trae la **respuesta entera**, sin leerla, para que la mires primero:

```csharp
HttpResponseMessage r = await puerto.GetAsync("barcos/9");
Console.WriteLine((int)r.StatusCode);      // 404
Console.WriteLine(r.StatusCode);           // NotFound
Console.WriteLine(r.IsSuccessStatusCode);  // False: solo los 2xx son éxito
```

Después se lee el cuerpo, con el tipo que corresponda: un barco si salió bien, el error si no.

```csharp
if (r.IsSuccessStatusCode)
{
    Barco? b = await r.Content.ReadFromJsonAsync<Barco>();
}
else
{
    Problema? p = await r.Content.ReadFromJsonAsync<Problema>();
}

record Problema(string Error);
```

#### Mandar algo

`PostAsJsonAsync` convierte el objeto en JSON y lo manda. Con un objeto anónimo (`new { ... }`) no hace falta un `record`:

```csharp
HttpResponseMessage c = await puerto.PostAsJsonAsync("mensajes", new { de = "Ceci", texto = "Gracias" });
Console.WriteLine(c.StatusCode);   // Created
```

#### Que corte si falló

`EnsureSuccessStatusCode()` no hace nada si salió bien, y lanza una `HttpRequestException` si no, con el código adentro (`ex.StatusCode`). Y si el JSON llega roto, `ReadFromJsonAsync` lanza una `JsonException` (está en `System.Text.Json`).

### Código de ejemplo

```csharp
HttpClient puerto = Puerto.CreateClient();

HttpResponseMessage r = await puerto.GetAsync("barcos/9");
Console.WriteLine($"Código: {(int)r.StatusCode} ({r.StatusCode})");
if (!r.IsSuccessStatusCode)
{
    Problema? p = await r.Content.ReadFromJsonAsync<Problema>();
    Console.WriteLine($"El Puerto dice: {p!.Error}");
}

HttpResponseMessage c = await puerto.PostAsJsonAsync("mensajes", new { de = "Ceci", texto = "Gracias por las cuerdas" });
Mensaje? m = await c.Content.ReadFromJsonAsync<Mensaje>();
Console.WriteLine($"{(int)c.StatusCode}: mensaje {m!.Id} de {m.De}");

record Problema(string Error);
record Mensaje(int Id, string De, string Texto);
```

### Salida esperada

```
Código: 404 (NotFound)
El Puerto dice: No hay ningún barco con el número 9.
201: mensaje 3 de Ceci
```

### ¿Para qué sirve?

Del otro lado siempre puede pasar algo: lo que pediste no existe, te faltó un dato, el servidor se cayó. Un programa que mira el código antes de leer avisa bien en vez de romperse, y es lo que distingue una app que «se cuelga» de una que dice «no encontramos ese producto».

### Errores habituales

- **Leer sin mirar el código:** un 404 trae un error en el cuerpo, no un barco, y el barco queda vacío.
- **Mandar un nombre que el Puerto no espera:** `mensaje` en vez de `texto` y el Puerto contesta 422.
- **No atrapar el JSON roto:** es el **goblin** de los mensajes cortados. Va `catch (JsonException)`.

### Micro-misión S03-N02-P1 · El código de estado

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Nilo
carta: GetAsync | HttpResponseMessage r = await puerto.GetAsync(...) · (int)r.StatusCode → 404 · r.StatusCode → NotFound
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
Nilo le enseña a Ceci a leer el sello de cada respuesta antes de abrirla: un número que dice cómo salió el pedido. El programa de Ceci recibe la respuesta, pero no la mira.

#### Gheco sugiere
`StatusCode` es el código de la respuesta. Convertido a `int` es el número; sin convertir, su nombre:

```csharp
HttpResponseMessage r = await servicio.GetAsync("clima");
Console.WriteLine($"{(int)r.StatusCode} {r.StatusCode}");   // 200 OK
```

#### Desafío
En vez de `Llegó la respuesta`, mostrá `Código: ` con el número y, entre paréntesis, el nombre: `$"Código: {(int)r.StatusCode} ({r.StatusCode})"`.

#### Pasos
1. Cambiá `"Llegó la respuesta"` por `$"Código: {(int)r.StatusCode} ({r.StatusCode})"`.
2. Tocá **Ejecutar**. Tiene que salir `Código: 404 (NotFound)`.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();
HttpResponseMessage r = await puerto.GetAsync("barcos/9");
Console.WriteLine("Llegó la respuesta");
```

#### Salida esperada
```
Código: 404 (NotFound)
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
HttpResponseMessage r = await puerto.GetAsync("barcos/9");
Console.WriteLine($"Código: {(int)r.StatusCode} ({r.StatusCode})");
```

#### Al superarla
—404 —dice Nilo—. «No lo encontré.» El Puerto te contestó, y muy amable. El problema era la pregunta.

#### Imagen
- Un sobre con un sello de lacre violeta grande sobre el mostrador de la ventanilla, junto a una lupa, sin letras ni números.
- Nilo, con gorra de mensajero azul y bufanda violeta, señala el sello; Ceci mira con la lupa.

### Micro-misión S03-N02-P2 · Un barco o un error

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Nilo, Gheco
carta: Leer según el código | if (r.IsSuccessStatusCode) → ReadFromJsonAsync<Barco>() · si no → ReadFromJsonAsync<Problema>()
recompensa: xp 15, oro 15
```

#### Escena
El programa de Ceci lee la respuesta como un barco, aunque el Puerto haya contestado un error. Muestra un barco sin nombre y sin carga, como un fantasma.

#### Gheco sugiere
Primero se mira si salió bien. Si salió, se lee el dato; si no, se lee el error:

```csharp
if (r.IsSuccessStatusCode)
{
    Clima? c = await r.Content.ReadFromJsonAsync<Clima>();
}
else
{
    Problema? p = await r.Content.ReadFromJsonAsync<Problema>();
}
```

#### Desafío
Envolvé la lectura del barco en un `if (r.IsSuccessStatusCode)`. En el `else`, leé un `Problema` y mostrá `El Puerto dice: ` con `p!.Error`.

#### Pasos
1. Envolvé las dos líneas del barco en `if (r.IsSuccessStatusCode) { ... }`.
2. Después: `else` y, entre llaves, `Problema? p = await r.Content.ReadFromJsonAsync<Problema>();` y `Console.WriteLine($"El Puerto dice: {p!.Error}");`.
3. Tocá **Ejecutar** y compará.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();
HttpResponseMessage r = await puerto.GetAsync("barcos/9");

Barco? b = await r.Content.ReadFromJsonAsync<Barco>();
Console.WriteLine($"{b!.Nombre} trae {b.Carga}");

record Barco(int Id, string Nombre, string Carga);
record Problema(string Error);
```

#### Salida esperada
```
El Puerto dice: No hay ningún barco con el número 9.
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
HttpResponseMessage r = await puerto.GetAsync("barcos/9");

if (r.IsSuccessStatusCode)
{
    Barco? b = await r.Content.ReadFromJsonAsync<Barco>();
    Console.WriteLine($"{b!.Nombre} trae {b.Carga}");
}
else
{
    Problema? p = await r.Content.ReadFromJsonAsync<Problema>();
    Console.WriteLine($"El Puerto dice: {p!.Error}");
}

record Barco(int Id, string Nombre, string Carga);
record Problema(string Error);
```

#### Al superarla
El barco fantasma desaparece de la pantalla. En su lugar, la respuesta prolija de Elefa: no hay barco 9.

#### Imagen
- Un muelle de madera vacío con un poste numerado sin número y un farol violeta, de noche, sin letras.
- Nilo se encoge de hombros con las manos abiertas; Gheco, MINÚSCULO, sentado en el poste vacío; Ceci asiente.

### Micro-misión S03-N02-P3 · Escribirle al Puerto

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Elefa
carta: PostAsJsonAsync | puerto.PostAsJsonAsync("mensajes", new { de = "Ceci", texto = "..." }) · el Puerto espera texto · 201 Created
recompensa: xp 15, oro 15
```

#### Escena
Ceci quiere agradecerle a Elefa por las cuerdas. Manda el mensaje, pero el Puerto lo rechaza con un 422: el campo se llama `mensaje`, y el Puerto espera `texto`.

#### Gheco sugiere
`PostAsJsonAsync` convierte el objeto en JSON y lo manda. Los nombres tienen que ser los que espera la API:

```csharp
await servicio.PostAsJsonAsync("pedidos", new { producto = "resina", cantidad = 2 });
```

#### Desafío
En el objeto que se manda, cambiá `mensaje` por `texto`.

#### Pasos
1. En el objeto, cambiá `mensaje =` por `texto =`.
2. Tocá **Ejecutar**. Tiene que salir `201 Created`.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();
HttpResponseMessage c = await puerto.PostAsJsonAsync("mensajes", new { de = "Ceci", mensaje = "Gracias por las cuerdas" });
Mensaje? m = await c.Content.ReadFromJsonAsync<Mensaje>();
Console.WriteLine($"{(int)c.StatusCode} {c.StatusCode}: mensaje {m!.Id}");

record Mensaje(int Id, string De, string Texto);
```

#### Salida esperada
```
201 Created: mensaje 3
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
HttpResponseMessage c = await puerto.PostAsJsonAsync("mensajes", new { de = "Ceci", texto = "Gracias por las cuerdas" });
Mensaje? m = await c.Content.ReadFromJsonAsync<Mensaje>();
Console.WriteLine($"{(int)c.StatusCode} {c.StatusCode}: mensaje {m!.Id}");

record Mensaje(int Id, string De, string Texto);
```

#### Al superarla
Lejos, en la Torre de la Campana, suena la campana del Puerto: un mensaje nuevo. Elefa lo sella con su bastón y lo guarda. Nunca se olvida de nada.

#### Imagen
- Una torre de piedra con una campana de bronce grande y tubos de bronce, sobre un puerto de noche con faroles violetas, sin letras.
- Elefa, una elefanta enorme erguida con casco gris y violeta y armadura, sella una carta con un bastón coronado por un sello de lacre violeta.

### Micro-misión S03-N02-P4 · La grúa caída

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Nilo
carta: EnsureSuccessStatusCode | r.EnsureSuccessStatusCode(); · si no es 2xx, lanza HttpRequestException · ex.StatusCode tiene el código
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Se cayó una grúa en el muelle, y el Puerto contesta 500 a todo. El programa de Ceci intenta leer la lista de barcos igual, y se rompe de una forma que nadie entiende.

#### Gheco sugiere
`EnsureSuccessStatusCode()` corta enseguida si la respuesta no salió bien, con una `HttpRequestException` que trae el código:

```csharp
try
{
    r.EnsureSuccessStatusCode();
}
catch (HttpRequestException ex)
{
    Console.WriteLine((int?)ex.StatusCode);
}
```

#### Desafío
Adentro del `try`, antes de leer, agregá `r.EnsureSuccessStatusCode();`.

#### Pasos
1. Adentro del `try`, antes de leer, escribí `r.EnsureSuccessStatusCode();`.
2. Tocá **Ejecutar**. Tiene que salir `Falló el pedido: 500`.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();
HttpResponseMessage r = await puerto.GetAsync("error");
try
{
    List<Barco>? barcos = await r.Content.ReadFromJsonAsync<List<Barco>>();
    Console.WriteLine($"Barcos: {barcos!.Count}");
}
catch (HttpRequestException ex)
{
    Console.WriteLine($"Falló el pedido: {(int?)ex.StatusCode}");
}

record Barco(int Id, string Nombre, string Carga);
```

#### Salida esperada
```
Falló el pedido: 500
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
HttpResponseMessage r = await puerto.GetAsync("error");
try
{
    r.EnsureSuccessStatusCode();
    List<Barco>? barcos = await r.Content.ReadFromJsonAsync<List<Barco>>();
    Console.WriteLine($"Barcos: {barcos!.Count}");
}
catch (HttpRequestException ex)
{
    Console.WriteLine($"Falló el pedido: {(int?)ex.StatusCode}");
}

record Barco(int Id, string Nombre, string Carga);
```

#### Al superarla
—500: el problema es de ellos, no tuyo —dice Nilo—. Ahora tu programa lo sabe, en vez de tratar de leer una grúa como si fuera un barco.

#### Imagen
- Una grúa de madera del puerto caída sobre el muelle, con cajas desparramadas y faroles violetas, sin letras.
- Nilo, con su bufanda violeta, se rasca la cabeza mirando la grúa; Ceci, al lado, sostiene su cuaderno.

### Micro-misión S03-N02-P5 · El goblin del mensaje cortado

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Gheco
criatura: goblin
carta: Goblin | JSON cortado → JsonException · catch (JsonException) · using System.Text.Json; arriba de todo
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Un goblin se comió la mitad de un mensaje del Puerto. Llega `{"mensaje": "esto se cortó a la mit`, sin cerrar, y el programa de Ceci se rompe: solo sabe atrapar errores de pedido, no de JSON.

#### Gheco sugiere
Un JSON roto no es un error del pedido (el pedido salió bien): es una `JsonException`. Se atrapa con otro `catch`:

```csharp
catch (JsonException)
{
    Console.WriteLine("El archivo está roto");
}
```

El `using System.Text.Json;` de arriba ya está.

#### Desafío
Agregá un `catch (JsonException)` que muestre `El mensaje llegó cortado: un goblin se comió la mitad`.

#### Pasos
1. Después del último `catch`, escribí `catch (JsonException)`.
2. Entre llaves: `Console.WriteLine("El mensaje llegó cortado: un goblin se comió la mitad");`.
3. Tocá **Ejecutar** y compará.

#### Código inicial
```csharp
using System.Text.Json;

HttpClient puerto = Puerto.CreateClient();
try
{
    Saludo? s = await puerto.GetFromJsonAsync<Saludo>("roto");
    Console.WriteLine(s!.Mensaje);
}
catch (HttpRequestException)
{
    Console.WriteLine("El Puerto no contestó");
}

record Saludo(string Mensaje);
```

#### Salida esperada
```
El mensaje llegó cortado: un goblin se comió la mitad
```

#### Solución
```csharp
using System.Text.Json;

HttpClient puerto = Puerto.CreateClient();
try
{
    Saludo? s = await puerto.GetFromJsonAsync<Saludo>("roto");
    Console.WriteLine(s!.Mensaje);
}
catch (HttpRequestException)
{
    Console.WriteLine("El Puerto no contestó");
}
catch (JsonException)
{
    Console.WriteLine("El mensaje llegó cortado: un goblin se comió la mitad");
}

record Saludo(string Mensaje);
```

#### Al superarla
El goblin escupe el pedazo de papel que le quedaba y se va, con hipo. Ceci le pide a Elefa que mande el mensaje otra vez.

#### Imagen
- Un pedazo de papel roto por la mitad sobre el mostrador de la ventanilla, con la otra mitad mordida, sin letras.
- Un goblin verde chiquito mastica un papel con cara de culpa; Gheco, MINÚSCULO, le señala la boca; Ceci sostiene la mitad que quedó.

## S03-N03 · Paciencia y tormentas

```meta
tipo: tema
padre: S03-N02
precio: 10
criatura: troll
temas: web.http, err.validacion
usa: conc.async, func.streams
```

### Crónica

Llega el invierno y sopla el viento del sur. A veces el Puerto tarda en contestar, porque la marea está alta. A veces está **cerrado por tormenta**, y hay que volver a preguntar más tarde. Y Pico aprendió a meterse en las cajas: las cargas llegan revueltas, sin nombre o con cantidades negativas.

—Elefa desconfía de todo lo que llega de afuera hasta que lo comprueba —dice Nilo—. Tu ventanilla tendría que hacer lo mismo.

### Objetivos

- No esperar para siempre: `Timeout` del cliente y `CancellationTokenSource`.
- Volver a intentar cuando el Puerto está cerrado, con un **tope** de intentos.
- Esperar un poco entre un intento y otro.
- No confiar en lo que llega: descartar los datos que no tienen sentido.

### Antes de empezar

- Mirar la respuesta (S03-N02) y cancelar (R05-N02).

### Explicación

#### No esperar para siempre

Si el Puerto tarda, tu programa no puede quedarse colgado. Un cliente puede tener un **tope de espera**:

```csharp
puerto.Timeout = TimeSpan.FromSeconds(1);
try
{
    await puerto.GetAsync("lento");
}
catch (TaskCanceledException)
{
    Console.WriteLine("El Puerto tarda demasiado");
}
```

También se puede cortar un pedido solo, con un `CancellationTokenSource` como en el R05-N02:

```csharp
using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(1));
await puerto.GetAsync("lento", cts.Token);   // si pasa el segundo: OperationCanceledException
```

#### Volver a intentar, con tope

Algunos errores se arreglan solos: el 503 quiere decir «ahora no puedo, probá más tarde». Se reintenta, pero **siempre con un tope**, y esperando un poco más cada vez:

```csharp
for (int intento = 1; intento <= 3; intento++)
{
    HttpResponseMessage r = await puerto.GetAsync("tormenta");
    if (r.IsSuccessStatusCode) break;
    await Task.Delay(100 * intento);   // 100 ms, 200 ms, 300 ms
}
```

Sin tope, si el Puerto no vuelve nunca, tu programa pregunta para siempre.

#### No confiar en lo que llega

Que el JSON se haya podido leer no quiere decir que los datos tengan sentido. Se revisan con `Where` antes de usarlos:

```csharp
var buenas = cargas.Where(c => c.Nombre is not null && c.Cantidad > 0).ToList();
```

### Código de ejemplo

```csharp
HttpClient puerto = Puerto.CreateClient();
puerto.Timeout = TimeSpan.FromSeconds(1);

try
{
    await puerto.GetAsync("lento");
}
catch (TaskCanceledException)
{
    Console.WriteLine("El Puerto tarda demasiado");
}

for (int intento = 1; intento <= 3; intento++)
{
    HttpResponseMessage r = await puerto.GetAsync("tormenta");
    Console.WriteLine($"Intento {intento}: {(int)r.StatusCode}");
    if (r.IsSuccessStatusCode)
    {
        break;
    }
    await Task.Delay(100 * intento);
}

List<Carga> cargas = (await puerto.GetFromJsonAsync<List<Carga>>("cargas"))!;
var buenas = cargas.Where(c => c.Nombre is not null && c.Cantidad > 0).ToList();
Console.WriteLine($"Buenas: {buenas.Count}, descartadas: {cargas.Count - buenas.Count}");

record Carga(string? Nombre, int Cantidad);
```

### Salida esperada

```
El Puerto tarda demasiado
Intento 1: 503
Intento 2: 503
Intento 3: 200
Buenas: 2, descartadas: 2
```

### ¿Para qué sirve?

Internet falla todo el tiempo: el celular pierde señal, el servidor está ocupado, un dato viene mal cargado. Las apps que «aguantan» hacen esto: no esperan para siempre, reintentan con calma y con tope, y no se creen todo lo que llega.

### Errores habituales

- **Reintentar sin tope:** si el Puerto no vuelve, el programa no termina nunca.
- **Reintentar sin esperar:** se le cae encima al Puerto justo cuando está en problemas.
- **Reintentar un 404 o un 422:** esos no se arreglan solos. Se reintenta un 503 o un 500, no un error tuyo.
- **Usar los datos sin revisarlos:** una carga sin nombre rompe el programa. Es el **troll** de lo que vale `null`.

### Micro-misión S03-N03-P1 · La marea alta

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Nilo
carta: Timeout | puerto.Timeout = TimeSpan.FromSeconds(1); · si tarda más: TaskCanceledException
recompensa: xp 15, oro 15, monedas 4
```

#### Escena
La marea está alta y el Puerto tarda tres segundos en contestar. Mientras tanto, la ventanilla de Ceci se queda congelada, y la fila de gente llega hasta la calle.

#### Gheco sugiere
`Timeout` le pone un tope de espera a **cada** pedido del cliente. Si se pasa, el pedido se cancela con una `TaskCanceledException`:

```csharp
servicio.Timeout = TimeSpan.FromMilliseconds(500);
```

#### Desafío
Antes del `try`, poné `puerto.Timeout = TimeSpan.FromSeconds(1);`.

#### Pasos
1. Debajo de la primera línea, escribí `puerto.Timeout = TimeSpan.FromSeconds(1);`.
2. Tocá **Ejecutar** y compará.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();

try
{
    string t = await puerto.GetStringAsync("lento");
    Console.WriteLine(t);
}
catch (TaskCanceledException)
{
    Console.WriteLine("El Puerto tarda demasiado: probá más tarde");
}
```

#### Salida esperada
```
El Puerto tarda demasiado: probá más tarde
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
puerto.Timeout = TimeSpan.FromSeconds(1);

try
{
    string t = await puerto.GetStringAsync("lento");
    Console.WriteLine(t);
}
catch (TaskCanceledException)
{
    Console.WriteLine("El Puerto tarda demasiado: probá más tarde");
}
```

#### Al superarla
La ventanilla deja de congelarse: al segundo, avisa y sigue atendiendo. La fila avanza.

#### Imagen
- Un muelle con la marea muy alta, olas que pasan por encima de las tablas y faroles violetas que se mecen, sin letras.
- Nilo, empapado, con la gorra chorreando, sostiene una carta seca arriba de la cabeza; Ceci lo mira desde la ventanilla.

### Micro-misión S03-N03-P2 · Cerrado por tormenta

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Nilo, Gheco
carta: Reintentar | for (int intento = 1; intento <= 3; intento++) · break si salió bien · 503: probá más tarde
recompensa: xp 15, oro 15
```

#### Escena
El Puerto contesta 503: cerrado por tormenta. Ceci pregunta una vez y se rinde. Nilo se ríe. —Las tormentas de acá pasan rápido. Preguntá otra vez.

#### Gheco sugiere
Un `for` repite el pedido, y un `break` corta apenas sale bien:

```csharp
for (int vuelta = 1; vuelta <= 5; vuelta++)
{
    if (Probar()) break;
}
```

#### Desafío
Envolvé el pedido y su `Console.WriteLine` en un `for (int intento = 1; intento <= 3; intento++)`. Mostrá el número de `intento` en vez del `1`, y cortá con `break` si `codigo == 200`.

#### Pasos
1. Arriba del pedido: `for (int intento = 1; intento <= 3; intento++)` y abrí una llave.
2. Adentro, las tres líneas. En el `WriteLine`, cambiá `Intento 1` por `Intento {intento}`.
3. Debajo: `if (codigo == 200)` y, entre llaves, `break;`. Cerrá la llave del `for`.
4. Tocá **Ejecutar**. El intento 3 tiene que dar 200.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();
int codigo = 0;

HttpResponseMessage r = await puerto.GetAsync("tormenta");
codigo = (int)r.StatusCode;
Console.WriteLine($"Intento 1: {codigo}");

Console.WriteLine(codigo == 200 ? "Salen los barcos" : "El Puerto sigue cerrado");
```

#### Salida esperada
```
Intento 1: 503
Intento 2: 503
Intento 3: 200
Salen los barcos
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
int codigo = 0;

for (int intento = 1; intento <= 3; intento++)
{
    HttpResponseMessage r = await puerto.GetAsync("tormenta");
    codigo = (int)r.StatusCode;
    Console.WriteLine($"Intento {intento}: {codigo}");
    if (codigo == 200)
    {
        break;
    }
}

Console.WriteLine(codigo == 200 ? "Salen los barcos" : "El Puerto sigue cerrado");
```

#### Al superarla
A la tercera, el viento se calma. Los cuatro barcos levan anclas y uno, el Ancla Azul, pone proa al Conservatorio.

#### Imagen
- Un puerto bajo una tormenta que se abre, con nubes oscuras que dejan pasar un rayo de sol sobre barcos de vela, sin letras.
- Nilo señala el cielo que se despeja; Gheco, MINÚSCULO, sentado en la gorra de Nilo, festeja; Ceci sonríe.

### Micro-misión S03-N03-P3 · Saber rendirse

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Elefa
carta: Tope | un for con tope, no un while sin fin · al final: si nunca salió bien, avisar
recompensa: xp 15, oro 15
```

#### Escena
La grúa caída no se arregla en un rato. El programa de Ceci pregunta una y otra vez, sin parar, y el Puerto se llena de pedidos repetidos. Elefa le manda una paloma: *«Preguntá tres veces. Si no, esperá a mañana.»*

#### Gheco sugiere
Un `while` que espera el éxito no termina si el éxito no llega nunca. Un `for` con tope sí:

```csharp
bool listo = false;
for (int vuelta = 1; vuelta <= 3 && !listo; vuelta++)
{
    listo = Probar();
}
if (!listo) Console.WriteLine("Me rindo");
```

#### Desafío
Cambiá el `while (codigo != 200)` por un `for (int intento = 1; intento <= 3; intento++)` que corte con `break` si sale bien, y sacá el `intento++` de adentro. Al final, si `codigo != 200`, mostrá `Me rindo: el Puerto no contesta`.

#### Pasos
1. Borrá `int intento = 1;`.
2. Cambiá `while (codigo != 200)` por `for (int intento = 1; intento <= 3; intento++)`.
3. Cambiá `intento++;` por `if (codigo == 200)` con `break;` entre llaves.
4. Después del `for`: `if (codigo != 200)` y, entre llaves, `Console.WriteLine("Me rindo: el Puerto no contesta");`.
5. Tocá **Ejecutar** y compará.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();
int codigo = 0;
int intento = 1;

while (codigo != 200)
{
    HttpResponseMessage r = await puerto.GetAsync("error");
    codigo = (int)r.StatusCode;
    Console.WriteLine($"Intento {intento}: {codigo}");
    intento++;
}
```

#### Salida esperada
```
Intento 1: 500
Intento 2: 500
Intento 3: 500
Me rindo: el Puerto no contesta
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
int codigo = 0;

for (int intento = 1; intento <= 3; intento++)
{
    HttpResponseMessage r = await puerto.GetAsync("error");
    codigo = (int)r.StatusCode;
    Console.WriteLine($"Intento {intento}: {codigo}");
    if (codigo == 200)
    {
        break;
    }
}

if (codigo != 200)
{
    Console.WriteLine("Me rindo: el Puerto no contesta");
}
```

#### Al superarla
Tres intentos y a dormir. Elefa, en su torre, oye la campana sonar tres veces y nada más. Asiente: así se pregunta.

#### Imagen
- La Torre de la Campana del Puerto al anochecer, con la campana quieta y tres palomas que vuelven al palomar, sin letras.
- Elefa, la elefanta enorme con casco y armadura gris y violeta, mira por una ventana de la torre, tranquila.

### Micro-misión S03-N03-P4 · Un segundo para todo

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Clave
carta: CancellationTokenSource | using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(1)); · GetAsync(…, cts.Token) · OperationCanceledException
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Clave tiene un ensayo en un rato y le da a Ceci un segundo, ni uno más, para saber si llegaron las partituras. El programa no tiene `Timeout` y no puede cambiarlo: el cliente lo usan otros. Hay que cortar **este** pedido.

#### Gheco sugiere
Un `CancellationTokenSource` con tiempo se cancela solo. Se le pasa su `Token` al pedido:

```csharp
using var cts = new CancellationTokenSource(TimeSpan.FromMilliseconds(500));
await servicio.GetAsync("clima", cts.Token);
```

#### Desafío
Creá `using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(1));` antes del `try`, y pasale `cts.Token` a `GetStringAsync`.

#### Pasos
1. Debajo de la primera línea, escribí `using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(1));`.
2. Cambiá `GetStringAsync("lento")` por `GetStringAsync("lento", cts.Token)`.
3. Tocá **Ejecutar** y compará.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();

try
{
    string t = await puerto.GetStringAsync("lento");
    Console.WriteLine(t);
}
catch (OperationCanceledException)
{
    Console.WriteLine("Cancelado: se acabó el segundo de Clave");
}
```

#### Salida esperada
```
Cancelado: se acabó el segundo de Clave
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(1));

try
{
    string t = await puerto.GetStringAsync("lento", cts.Token);
    Console.WriteLine(t);
}
catch (OperationCanceledException)
{
    Console.WriteLine("Cancelado: se acabó el segundo de Clave");
}
```

#### Al superarla
Al segundo justo, el programa avisa. Clave ya está en la puerta, con la batuta. —Gracias. Las partituras pueden esperar al ensayo de mañana.

#### Imagen
- Un reloj de arena grande sobre el mostrador de la ventanilla, con la última arena cayendo, sin letras ni números.
- Clave, con su capa y la mecha blanca en el rodete, espera en la puerta con una batuta en la mano; Ceci mira el reloj de arena.

### Micro-misión S03-N03-P5 · El troll de las cajas revueltas

```meta
lugar: El muelle del Puerto
personajes: Ceci, Nilo, Gheco
criatura: troll
carta: Troll | Where(c => c.Nombre is not null && c.Cantidad > 0) · descartar lo que no tiene sentido antes de usarlo
recompensa: xp 15, oro 15, monedas 3
```

#### Escena
Pico revolvió las cajas de carga, y un troll del muelle las anotó como estaban: una sin nombre y otra con cantidad negativa. El programa de Ceci las muestra en mayúscula y, al llegar a la que no tiene nombre, se rompe.

#### Gheco sugiere
Antes de usar los datos, se descarta lo que no tiene sentido. `Where` deja pasar solo lo que cumple **todas** las condiciones:

```csharp
foreach (var p in pedidos.Where(p => p.Producto is not null && p.Precio >= 0))
{
    Console.WriteLine(p.Producto);
}
```

#### Desafío
Recorré `cargas.Where(c => c.Nombre is not null && c.Cantidad > 0)` en vez de `cargas`.

#### Pasos
1. Cambiá `in cargas)` por `in cargas.Where(c => c.Nombre is not null && c.Cantidad > 0))`.
2. Tocá **Ejecutar**. Tiene que salir `VIOLINES: 4` y `RESINA: 6`.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();
List<Carga> cargas = (await puerto.GetFromJsonAsync<List<Carga>>("cargas"))!;

foreach (Carga c in cargas)
{
    Console.WriteLine($"{c.Nombre!.ToUpper()}: {c.Cantidad}");
}

record Carga(string? Nombre, int Cantidad);
```

#### Salida esperada
```
VIOLINES: 4
RESINA: 6
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
List<Carga> cargas = (await puerto.GetFromJsonAsync<List<Carga>>("cargas"))!;

foreach (Carga c in cargas.Where(c => c.Nombre is not null && c.Cantidad > 0))
{
    Console.WriteLine($"{c.Nombre!.ToUpper()}: {c.Cantidad}");
}

record Carga(string? Nombre, int Cantidad);
```

#### Al superarla
Las dos cajas buenas suben al carro del Conservatorio. Las otras dos se quedan en el muelle, y el troll se sienta arriba a cuidarlas, contento de tener algo que hacer. Pico, desde un poste, grita «¡Kiá!» y se va volando, ofendido.

#### Imagen
- Un muelle de madera con cajas de carga, unas apiladas en orden y dos tiradas y abiertas, con faroles violetas, sin letras.
- Un troll gris chiquito sentado arriba de las cajas tiradas; una gaviota regordeta con una mancha violeta en el ala, en un poste, con un sobre en el pico; Nilo, con su bufanda violeta, y Ceci cargan una caja buena; Gheco, MINÚSCULO, flota arriba.

## S03-N04 · Jefe: la Gaviota de Mil Mensajes

```meta
tipo: jefe
padre: S03-N03
precio: 10
criatura: dragon
insignia: Ventanilla del Puerto
insignia_descripcion: Venciste a la Gaviota de Mil Mensajes: tu ventanilla le pregunta al Puerto, filtra lo que importa, avisa cuando el Puerto falla, no deja pasar cartas vacías y no repite mensajes.
temas: web.api-rest, web.http
usa: conc.async, err.validacion, col.conjuntos, func.streams
```

### Crónica

Una noche, el palomar de Pico se descontrola. Las palomas, las gaviotas y los sobres robados de veinte años se juntan en el cielo y forman una sola figura enorme: **la Gaviota de Mil Mensajes**, un remolino de papel con alas que chilla en todas las voces a la vez. Se posa sobre la Ventanilla del Conservatorio y empieza a escupir cartas: vacías, repetidas, mezcladas.

—¡Va a tapar el Puerto entero! —grita Nilo, que llegó corriendo—. Si todo eso llega a la ventanilla de Elefa, se cae.

Ceci respira hondo. Su ventanilla tiene que ser el **filtro**: preguntarle al Puerto solo lo que importa, avisar bien cuando el Puerto falla, y no dejar pasar ni una carta vacía ni una repetida.

### Objetivos

- Armar en tu ventanilla una ruta que **le pregunta al Puerto** y contesta con eso.
- Agregarle lo del Conservatorio: quedarse solo con lo que le sirve.
- Contestar **502** cuando el Puerto falla, en vez de pasar su error como si fuera un éxito.
- Validar antes de pasar un pedido (400) y no mandar repetidos, con un `HashSet`.

### Antes de empezar

- La ventanilla (R05-N07), `HashSet` (R03-N03) y toda la Senda del Puerto (S03-N01 a N03).

### Explicación

#### Una ruta que pregunta

El manejador de una ruta puede ser `async` y usar el cliente del Puerto adentro. Tu ventanilla pregunta, espera y contesta:

```csharp
HttpClient puerto = Puerto.CreateClient();
var app = WebApplication.CreateBuilder(args).Build();

app.MapGet("/llegadas", async () =>
{
    List<Barco> barcos = (await puerto.GetFromJsonAsync<List<Barco>>("barcos"))!;
    return Results.Ok(barcos.Select(b => b.Nombre));
});
```

Así trabajan casi todos los servidores: el tuyo le pregunta a otros, junta lo que importa y lo devuelve armado.

#### Cuando el de atrás falla: 502

Si el Puerto contesta 500, tu ventanilla no tiene la culpa, pero tampoco puede decir 200. Para eso está el **502 Bad Gateway**: «el de atrás me falló».

```csharp
return r.IsSuccessStatusCode ? Results.Ok(...) : Results.StatusCode(502);
```

#### El filtro

Antes de pasarle algo al Puerto, se revisa: una carta vacía se rechaza con un 400 **acá**, sin molestar al Puerto. Y un `HashSet` recuerda lo que ya se mandó: `Add` devuelve `false` si ya estaba.

```csharp
HashSet<string> enviadas = new();
if (!enviadas.Add(texto)) { /* repetida: no se manda */ }
```

### Código de ejemplo

```csharp
HttpClient puerto = Puerto.CreateClient();
var app = WebApplication.CreateBuilder(args).Build();
string[] instrumentos = ["violines", "cuerdas", "partituras"];

app.MapGet("/llegadas", async () =>
{
    List<Barco> barcos = (await puerto.GetFromJsonAsync<List<Barco>>("barcos"))!;
    return Results.Ok(barcos.Where(b => instrumentos.Contains(b.Carga)).Select(b => b.Nombre));
});

app.MapGet("/grua", async () =>
{
    HttpResponseMessage r = await puerto.GetAsync("error");
    return r.IsSuccessStatusCode ? Results.Ok() : Results.StatusCode(502);
});

HttpClient cliente = app.CreateClient();
Console.WriteLine(await cliente.GetStringAsync("/llegadas"));
Console.WriteLine((int)(await cliente.GetAsync("/grua")).StatusCode);

record Barco(int Id, string Nombre, string Carga);
```

### Salida esperada

```
["La Gaviota","El Ancla Azul","El Faro Viejo"]
502
```

### ¿Para qué sirve?

Una app de viajes le pregunta a las aerolíneas, a los hoteles y al clima, y te muestra todo junto: es una ventanilla que habla con otras. Esa forma de armar servidores (un intermediario que filtra, junta y protege a los de atrás) se usa en todos lados, y C# con ASP.NET es uno de los lenguajes favoritos para hacerla.

### Errores habituales

- **Olvidarse el `async` en el manejador:** sin él, no se puede usar `await` adentro.
- **Pasar el error del Puerto como un 200:** quien te pregunta cree que salió bien.
- **Dejar que el Puerto valide todo:** cada carta vacía es un viaje de ida y vuelta al Puerto. Se rechaza antes.
- **No recordar lo que ya se mandó:** los repetidos llenan el Puerto de lo mismo.

### Micro-misión S03-N04-P1 · La ruta que pregunta

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Nilo, Gheco
criatura: dragon
carta: Jefe | app.MapGet("/llegadas", async () => { … await puerto.GetFromJsonAsync<…>(…) … }) · el manejador puede preguntar
recompensa: xp 25, oro 25
```

#### Escena
La Gaviota tapa la ventana con sus alas de papel, y la gente de la Feria no ve qué barcos llegaron. La ruta `/llegadas` de la ventanilla de Ceci contesta una lista vacía: todavía no le pregunta nada al Puerto.

#### Gheco sugiere
Un manejador `async` puede pedirle algo al Puerto y contestar con eso:

```csharp
app.MapGet("/clima", async () =>
{
    Clima? c = await servicio.GetFromJsonAsync<Clima>("clima");
    return Results.Ok(c);
});
```

#### Desafío
Cambiá el manejador de `/llegadas` por uno `async` que pida `List<Barco>` al Puerto y conteste `Results.Ok(barcos.Select(b => b.Nombre))`.

#### Pasos
1. Cambiá la ruta por `app.MapGet("/llegadas", async () =>` y abrí una llave.
2. Adentro: `List<Barco> barcos = (await puerto.GetFromJsonAsync<List<Barco>>("barcos"))!;`.
3. Y: `return Results.Ok(barcos.Select(b => b.Nombre));`. Cerrá con `});`.
4. Tocá **Ejecutar** y compará.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();
var app = WebApplication.CreateBuilder(args).Build();

app.MapGet("/llegadas", () => Results.Ok(new List<string>()));

HttpClient cliente = app.CreateClient();
Console.WriteLine(await cliente.GetStringAsync("/llegadas"));

record Barco(int Id, string Nombre, string Carga);
```

#### Salida esperada
```
["La Gaviota","El Ancla Azul","La Marea","El Faro Viejo"]
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
var app = WebApplication.CreateBuilder(args).Build();

app.MapGet("/llegadas", async () =>
{
    List<Barco> barcos = (await puerto.GetFromJsonAsync<List<Barco>>("barcos"))!;
    return Results.Ok(barcos.Select(b => b.Nombre));
});

HttpClient cliente = app.CreateClient();
Console.WriteLine(await cliente.GetStringAsync("/llegadas"));

record Barco(int Id, string Nombre, string Carga);
```

#### Al superarla
Los nombres de los cuatro barcos aparecen en la pizarra de la ventanilla. La Gaviota chilla, enojada, y se le vuelan unas cuantas cartas de las alas.

#### Imagen
- La Ventanilla de Pedidos de noche, con un remolino enorme de cartas y sobres con forma de gaviota posado sobre el techo, sin letras.
- La Gaviota de Mil Mensajes, una gaviota gigante hecha de papeles y sobres arremolinados, con ojos de lacre violeta, abre las alas; Ceci, abajo, escribe en su pantalla; Nilo sostiene su gorra; Gheco, MINÚSCULO, en el hombro de Ceci.

### Micro-misión S03-N04-P2 · Solo lo del Conservatorio

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Bemol
criatura: dragon
carta: Jefe | barcos.Where(b => instrumentos.Contains(b.Carga)) · tu ventanilla junta lo que le sirve
recompensa: xp 25, oro 25
```

#### Escena
La Gaviota mezcla en la pizarra barcos que no le importan a nadie en el Conservatorio: uno trae sal. Bemol pregunta si la sal se toca con arco. Hay que dejar solo los barcos que traen instrumentos.

#### Gheco sugiere
`Contains` dice si un arreglo tiene un elemento. Con `Where`, quedan solo los que están en la lista:

```csharp
string[] permitidos = ["do", "re", "mi"];
var notas = todas.Where(n => permitidos.Contains(n));
```

#### Desafío
Antes del `Select`, agregá `.Where(b => instrumentos.Contains(b.Carga))`.

#### Pasos
1. Cambiá `barcos.Select(` por `barcos.Where(b => instrumentos.Contains(b.Carga)).Select(`.
2. Tocá **Ejecutar**. La Marea no tiene que aparecer.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();
var app = WebApplication.CreateBuilder(args).Build();
string[] instrumentos = ["violines", "cuerdas", "partituras"];

app.MapGet("/llegadas", async () =>
{
    List<Barco> barcos = (await puerto.GetFromJsonAsync<List<Barco>>("barcos"))!;
    return Results.Ok(barcos.Select(b => b.Nombre));
});

HttpClient cliente = app.CreateClient();
Console.WriteLine(await cliente.GetStringAsync("/llegadas"));

record Barco(int Id, string Nombre, string Carga);
```

#### Salida esperada
```
["La Gaviota","El Ancla Azul","El Faro Viejo"]
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
var app = WebApplication.CreateBuilder(args).Build();
string[] instrumentos = ["violines", "cuerdas", "partituras"];

app.MapGet("/llegadas", async () =>
{
    List<Barco> barcos = (await puerto.GetFromJsonAsync<List<Barco>>("barcos"))!;
    return Results.Ok(barcos.Where(b => instrumentos.Contains(b.Carga)).Select(b => b.Nombre));
});

HttpClient cliente = app.CreateClient();
Console.WriteLine(await cliente.GetStringAsync("/llegadas"));

record Barco(int Id, string Nombre, string Carga);
```

#### Al superarla
La Marea, con su sal, desaparece de la pizarra. Bemol se queda un poco triste: tenía hambre de algo salado.

#### Imagen
- Una pizarra de la ventanilla con tres dibujitos de barcos con instrumentos y uno tachado con un salero, sin letras.
- Bemol, MUY GORDITO con panza, mira el barco tachado con cara de pena; Ceci, al lado, señala la pizarra; detrás, por la ventana, se ven alas de papel.

### Micro-misión S03-N04-P3 · El de atrás falló

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Nilo, Gheco
criatura: dragon
carta: Jefe | si el Puerto no contesta bien → Results.StatusCode(502) · 502 Bad Gateway: «el de atrás me falló»
recompensa: xp 25, oro 25
```

#### Escena
La Gaviota tiró la grúa del muelle y el Puerto contesta 500. La ruta `/grua` de Ceci le pasa a la gente el texto del error con un 200, como si todo estuviera bien. La gente de la Feria espera barcos que no van a llegar.

#### Gheco sugiere
Si el que está atrás falla, tu ventanilla contesta **502**: no es culpa tuya, pero tampoco salió bien.

```csharp
return respuesta.IsSuccessStatusCode ? Results.Ok() : Results.StatusCode(502);
```

#### Desafío
Cambiá el `return` de `/grua` por `return r.IsSuccessStatusCode ? Results.Ok() : Results.StatusCode(502);`.

#### Pasos
1. Cambiá el `return` por `return r.IsSuccessStatusCode ? Results.Ok() : Results.StatusCode(502);`.
2. Tocá **Ejecutar**. Tiene que salir `Código: 502`.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();
var app = WebApplication.CreateBuilder(args).Build();

app.MapGet("/grua", async () =>
{
    HttpResponseMessage r = await puerto.GetAsync("error");
    return Results.Ok(await r.Content.ReadAsStringAsync());
});

HttpClient cliente = app.CreateClient();
HttpResponseMessage respuesta = await cliente.GetAsync("/grua");
Console.WriteLine($"Código: {(int)respuesta.StatusCode}");
```

#### Salida esperada
```
Código: 502
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
var app = WebApplication.CreateBuilder(args).Build();

app.MapGet("/grua", async () =>
{
    HttpResponseMessage r = await puerto.GetAsync("error");
    return r.IsSuccessStatusCode ? Results.Ok() : Results.StatusCode(502);
});

HttpClient cliente = app.CreateClient();
HttpResponseMessage respuesta = await cliente.GetAsync("/grua");
Console.WriteLine($"Código: {(int)respuesta.StatusCode}");
```

#### Al superarla
La pizarra muestra la verdad: el Puerto tiene problemas. La gente se va a su casa a esperar tranquila, en vez de quedarse mirando el mar. La Gaviota pierde otra nube de cartas.

#### Imagen
- La grúa de madera del muelle caída, vista de lejos por la ventana de la ventanilla, con cartas volando, sin letras.
- Nilo explica algo a un grupo de gente de la Feria con las manos; Ceci cuelga un cartel sin letras en la ventanilla; Gheco, MINÚSCULO, ayuda a sostenerlo.

### Micro-misión S03-N04-P4 · Ni una carta vacía

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Elefa
criatura: dragon
carta: Jefe | if (string.IsNullOrWhiteSpace(c.Texto)) return Results.BadRequest(…); · se rechaza acá, sin molestar al Puerto
recompensa: xp 25, oro 25, monedas 3
```

#### Escena
La Gaviota escupe cartas vacías por cientos, y la ventanilla de Ceci se las pasa todas al Puerto. Elefa tiene que revisarlas una por una para rechazarlas. —Lo que se puede revisar acá —le escribe— no tiene que viajar hasta acá.

#### Gheco sugiere
La ventanilla revisa **antes** de pasar el pedido. Si la carta está vacía, contesta 400 ella misma:

```csharp
if (string.IsNullOrWhiteSpace(pedido.Producto))
{
    return Results.BadRequest(new { error = "Falta el producto." });
}
```

#### Desafío
Al principio del manejador de `/cartas`, si `c.Texto` está vacío, devolvé `Results.BadRequest(new { error = "La carta está vacía." })`.

#### Pasos
1. Al principio del manejador: `if (string.IsNullOrWhiteSpace(c.Texto))`.
2. Entre llaves: `return Results.BadRequest(new { error = "La carta está vacía." });`.
3. Tocá **Ejecutar**. Tiene que salir `Carta vacía: 400`.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();
var app = WebApplication.CreateBuilder(args).Build();

app.MapPost("/cartas", async (Carta c) =>
{
    HttpResponseMessage r = await puerto.PostAsJsonAsync("mensajes", new { de = "Conservatorio", texto = c.Texto });
    return Results.StatusCode((int)r.StatusCode);
});

HttpClient cliente = app.CreateClient();
Console.WriteLine($"Carta vacía: {(int)(await cliente.PostAsJsonAsync("/cartas", new Carta(""))).StatusCode}");
Console.WriteLine($"Carta con texto: {(int)(await cliente.PostAsJsonAsync("/cartas", new Carta("Llegaron las cuerdas"))).StatusCode}");

record Carta(string Texto);
```

#### Salida esperada
```
Carta vacía: 400
Carta con texto: 201
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
var app = WebApplication.CreateBuilder(args).Build();

app.MapPost("/cartas", async (Carta c) =>
{
    if (string.IsNullOrWhiteSpace(c.Texto))
    {
        return Results.BadRequest(new { error = "La carta está vacía." });
    }
    HttpResponseMessage r = await puerto.PostAsJsonAsync("mensajes", new { de = "Conservatorio", texto = c.Texto });
    return Results.StatusCode((int)r.StatusCode);
});

HttpClient cliente = app.CreateClient();
Console.WriteLine($"Carta vacía: {(int)(await cliente.PostAsJsonAsync("/cartas", new Carta(""))).StatusCode}");
Console.WriteLine($"Carta con texto: {(int)(await cliente.PostAsJsonAsync("/cartas", new Carta("Llegaron las cuerdas"))).StatusCode}");

record Carta(string Texto);
```

#### Al superarla
Las cartas vacías se apilan en la ventanilla de Ceci y no llegan al Puerto. En la Torre de la Campana, Elefa deja el bastón del sello apoyado y, por primera vez en toda la noche, se sienta.

#### Imagen
- Una pila de sobres vacíos en el piso de la Ventanilla de Pedidos, con un tacho de papeles al lado, sin letras.
- Elefa, la elefanta enorme con casco y armadura gris y violeta, sentada en su torre con el bastón apoyado, aliviada.

### Micro-misión S03-N04-P5 · Mil mensajes, uno de cada uno

```meta
lugar: La Ventanilla de Pedidos
personajes: Ceci, Nilo, Clave, Gheco
criatura: dragon
carta: Jefe | HashSet<string> enviadas · if (!enviadas.Add(texto)) → repetida, no se manda · Add da false si ya estaba
recompensa: xp 30, oro 30, monedas 3
```

#### Escena
Su último truco: la Gaviota repite cada mensaje una y otra vez, con mil voces. «¡Llegaron las cuerdas!» «¡Llegaron las cuerdas!» «¡Llegaron las cuerdas!» Si la ventanilla de Ceci las pasa todas, el Puerto se llena de lo mismo y nadie encuentra nada.

#### Gheco sugiere
Un `HashSet` recuerda lo que ya vio. `Add` lo agrega y devuelve `true`; si ya estaba, no lo agrega y devuelve `false`:

```csharp
HashSet<string> vistos = new();
if (!vistos.Add(nombre))
{
    Console.WriteLine($"{nombre} ya estaba");
}
```

#### Desafío
Creá `HashSet<string> enviadas = new();` antes de las rutas. En `/cartas`, si `!enviadas.Add(c.Texto)`, devolvé `Results.Ok(new { repetida = true })` sin mandarla al Puerto.

#### Pasos
1. Debajo de `var app = ...`, escribí `HashSet<string> enviadas = new();`.
2. Al principio de `/cartas`: `if (!enviadas.Add(c.Texto))` y, entre llaves, `return Results.Ok(new { repetida = true });`.
3. Tocá **Ejecutar**. Tiene que salir `Mensajes en el Puerto: 5`.

#### Código inicial
```csharp
HttpClient puerto = Puerto.CreateClient();
var app = WebApplication.CreateBuilder(args).Build();

app.MapPost("/cartas", async (Carta c) =>
{
    HttpResponseMessage r = await puerto.PostAsJsonAsync("mensajes", new { de = "Conservatorio", texto = c.Texto });
    return Results.StatusCode((int)r.StatusCode);
});

HttpClient cliente = app.CreateClient();
string[] gaviota = ["Llegaron las cuerdas", "Llegaron las cuerdas", "Zarpó la Gaviota", "Llegaron las cuerdas", "Zarpó la Gaviota", "Ensayo a las ocho"];
foreach (string texto in gaviota)
{
    await cliente.PostAsJsonAsync("/cartas", new Carta(texto));
}

List<Mensaje> mensajes = (await puerto.GetFromJsonAsync<List<Mensaje>>("mensajes"))!;
Console.WriteLine($"Mensajes en el Puerto: {mensajes.Count}");

record Carta(string Texto);
record Mensaje(int Id, string De, string Texto);
```

#### Salida esperada
```
Mensajes en el Puerto: 5
```

#### Solución
```csharp
HttpClient puerto = Puerto.CreateClient();
var app = WebApplication.CreateBuilder(args).Build();
HashSet<string> enviadas = new();

app.MapPost("/cartas", async (Carta c) =>
{
    if (!enviadas.Add(c.Texto))
    {
        return Results.Ok(new { repetida = true });
    }
    HttpResponseMessage r = await puerto.PostAsJsonAsync("mensajes", new { de = "Conservatorio", texto = c.Texto });
    return Results.StatusCode((int)r.StatusCode);
});

HttpClient cliente = app.CreateClient();
string[] gaviota = ["Llegaron las cuerdas", "Llegaron las cuerdas", "Zarpó la Gaviota", "Llegaron las cuerdas", "Zarpó la Gaviota", "Ensayo a las ocho"];
foreach (string texto in gaviota)
{
    await cliente.PostAsJsonAsync("/cartas", new Carta(texto));
}

List<Mensaje> mensajes = (await puerto.GetFromJsonAsync<List<Mensaje>>("mensajes"))!;
Console.WriteLine($"Mensajes en el Puerto: {mensajes.Count}");

record Carta(string Texto);
record Mensaje(int Id, string De, string Texto);
```

#### Al superarla
Los dos de antes y tres nuevos: cinco mensajes, uno de cada uno. Sin repetidos que la alimenten, la Gaviota de Mil Mensajes se deshace en el aire, y los sobres caen despacio sobre la Feria como copos de nieve. Las palomas vuelven al palomar. Pico, solo otra vez, se posa en la ventanilla con un sobre en el pico y se lo deja a Ceci: es una carta de Elefa, sellada con lacre violeta. *«Ningún mensaje se queda sin respuesta, y ninguna respuesta sale sin revisar. Ahora tu ventanilla también lo sabe.»* Clave lee por encima del hombro de Ceci y, por una vez, sonríe sin disimular.

#### Imagen
- La Feria de las Luces de noche, con cientos de sobres cayendo despacio del cielo como copos de nieve y palomas volviendo a un palomar, sin letras.
- Una gaviota regordeta con una mancha violeta en el ala deja un sobre con sello violeta sobre la ventanilla; Ceci lo recibe; Clave, con su capa y la mecha blanca, sonríe detrás; Nilo festeja con la gorra en alto; Gheco, MINÚSCULO, en el hombro de Ceci.
