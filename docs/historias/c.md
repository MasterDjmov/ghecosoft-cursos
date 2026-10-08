# C · El arco de Kira (borrador 1, a revisar)

El curso de C, **«Las Forjas de Hierro»**, con Kira como protagonista fija (JUEGO.md § 1) y Maese Ferrum como mentor. Lo que manda en los contenidos es el **apunte de cátedra de Programación I de la UNLaR** (Camargo, 2008), adaptado a C moderno: el apunte usa Turbo C (`conio.h`, `clrscr()`, `getch()`, `void main`, `randomize()`, `fflush(stdin)`) y el curso enseña C estándar (`int main`, sin `conio.h`), que compila igual en Linux y en Windows. Las páginas de clases y C++ del apunte (pp. 70–88) van al curso de C++.

**Linux y Windows siempre:** el docente trabaja en Linux y los alumnos, en Windows. Cada «Cómo compilarlo», cada instalación y cada comando se da en las dos versiones.

---

## 1. El arco

Kira es una **aprendiz de espadachina** de un pueblo común. Una noche cruza un **vitral** que se enciende como un portal y despierta en la boca de las Forjas, con la espada en la mano. Quiere resolver todo **con fuerza y rápido**: en las Forjas aprende que **cada byte se cuenta** y que el metal no perdona, pero tampoco miente.

**Las criaturas** son los errores de C:
- **slimes** por la sintaxis (`expected ';'`);
- **goblins** por los tipos y los formatos que no coinciden (`%d` para un `double`, el `&` que falta en `scanf`, el desborde);
- **esqueletos** por los nombres que no existen (`undeclared`, `undefined reference`);
- **orcos** por los índices fuera de rango y los textos sin lugar para su `'\0'`;
- **ogros** por la lógica y el comportamiento indefinido;
- **trolls** por la memoria mal manejada (fugas, punteros colgantes, doble `free`).

**El objeto que cambia con ella** es su **espada de aprendiz** (como la ganzúa de Zed):
- **en la Clase 0**, la espada se **raja** contra el portón de la Forja: Kira golpeó sin medir;
- **al vencer al Gólem** (R01), Ferrum se la reforja por primera vez, y le dice que la próxima la forja ella;
- **al final**, Kira forja su propia hoja, **la Hoja Templada**, midiendo cada grado y cada golpe.

**El hilo del portal:** según Ferrum (`story.portal_piece`), el Vidriero le encargó **el plomo para un vitral enorme**, pagó por adelantado y nunca dijo para qué era. En las Forjas, Kira sigue ese encargo:
- en el depósito hay un **pedido de plomo** firmado con un vitral;
- en las Minas, la veta de donde salió ese plomo;
- en el Archivo, el **libro de registros** con las medidas del marco;
- bajo la Montaña, la fragua donde se fundió y **la matriz del marco** que dejó el Vidriero.

Es el mismo marco vacío que Zed ve en la Torre del Arquitecto (Java) y el mismo plomo que Tesela reconoce en los Talleres (HTML). Los hilos se cruzan, pero los protagonistas **no viajan juntos** (solo se anticipan).

### El tono: que sea divertido

Como en el Valle y en el Imperio, cada crónica tiene **un chiste o una escena cómica** antes de la lección, y los errores dan risa antes de dar miedo. Los chistes que vuelven a lo largo del curso:

- **Kira golpea primero.** Cada vez que algo no anda, su primer impulso es darle un espadazo. Ferrum lleva la cuenta en la pared con tiza: «Espadazos: 37. Problemas resueltos a espadazos: 0».
- **Tizón mide todo.** La sopa («le faltan 3 mililitros»), la puerta, la sombra de Kira, la paciencia de Ferrum. Cuando por fin acierta algo sin medir, se asusta.
- **El aplauso de Ferrum** son dos golpes en el yunque. Kira tarda medio curso en entender que es un elogio; la primera vez que recibe tres, no sabe qué hacer.
- **La balanza de Chispa** siempre pesa un poquito a su favor; en cada visita, Tizón la desarma y encuentra el truco (un desborde, un redondeo, un `%d` para un `double`).
- **Las vagonetas de Hulda:** quien no devuelve lo que pidió paga «intereses» en chistes malos que Hulda le obliga a contar en voz alta frente a toda la mina.
- **Las cartas de Bron** llegan siempre quemadas en una esquina, porque Ferrum las lee demasiado cerca del horno.

### Los personajes

Las fichas completas están en [PERSONAJES.md](PERSONAJES.md) (§ Las Forjas de Hierro); las que dicen *(falta la imagen)* aparecen en *Admin → Historia → Personajes* para generarlas.

- **Kira.**
- **Gheco**, que da las pistas (aparece sobre el hombro de Kira en la boca de la Forja).
- **Maese Ferrum:** el Forjador, herrero enano, el mentor. Fue maestro de Tesla y de Tesela (se los recuerda, no aparecen).
- **Tizón** *(nuevo, a confirmar)*: aprendiz enano de la Forja, de 16, con un **calibre** colgado del cuello y una libreta de medidas. Es el contrapunto de Kira: ella dice **«¡golpeá!»** y él **«¿lo mediste?»**. Los dos tienen razón a medias. Termina siendo su compañero.
- **Hulda** *(nueva, a confirmar)*: la **capataz de las Minas** (R03), dura, práctica, que cuenta cada vagoneta.
- **El Archivero de la Forja** *(nuevo, a confirmar)*: guarda los pedidos y los planos de todos los encargos (R04).
- **Bron, Mia y Zed no viajan con ella.** Solo se los anticipa: Ferrum recibe una carta de Bron desde la Ciudadela (es su viejo amigo), y un mercader cuenta que en el Imperio atraparon a un ladrón de techos en la Aduana.

**Los ejemplos y las prácticas** que hoy usan a Mia, Bron y Zed como compañía (≈ 300 menciones) pasan a gente de las Forjas, como se hizo en Java (Kira → Nadia, Bron → Baldo): **Mia → Tizón**, **Bron → Hulda**, **Zed → Chispa**, un mercader de lingotes que va y viene *(a confirmar)*. Las salidas se rehacen ejecutando el código.

**Las crónicas pasan a tercera persona con Kira** («Ferrum le explica a Kira…»), como las de Zed.

### Los jefes (todos tienen nombre; faltan sus fichas)

| Rama | Jefe | Ítem que deja |
|---|---|---|
| R01 | el Gólem de Escoria | **la Espada Reforjada** (arma rara) |
| R02 | la Araña de las Direcciones | **el Hilo de las Direcciones** (accesorio raro) |
| R03 | la Sanguijuela de las Minas | **la Lámpara del Minero** (épica) |
| R04 | el Guardián del Archivo | **el Libro de Registros de Plomo** (historia) y un épico |
| R05 | el Dragón bajo la Montaña | **la Hoja Templada** (legendaria) y **la Matriz del Marco** (historia) |
| S01 | la Salamandra del Horno | (Senda) |
| S02 | el Autómata Guardián | (Senda) |

**La segunda vida de las Forjas** (`Item::SECOND_LIFE`, como el Amuleto del Traceback y el de la Campana): **el Amuleto del Volcado**, que se gana en R02-N04 (punteros). Cuando un programa de C revienta, deja un *core dump*: el amuleto «guarda el volcado» y Kira vuelve a levantarse.

---

## 2. Los contenidos contra el apunte de la cátedra

El camino actual de C ya cubre casi todo el apunte. **Se mantiene el orden** (funciones temprano y punteros antes que archivos, porque `fopen` devuelve un `FILE*`), y se agrega lo que falta:

| Tema del apunte | Hoy | Qué se hace |
|---|---|---|
| Historia, niveles de lenguaje, compilador e intérprete, **del fuente al ejecutable** (preprocesador → compilador → enlazador) | Clase 0, breve | Ampliar la Clase 0 con el esquema del apunte (p. 6) |
| Tipos, modificadores, tabla de rangos | R01-N01 | Está (con `stdint.h` y rangos reales de hoy, no los de 16 bits del apunte) |
| **Especificadores de almacenamiento**: `const`, `static`, `extern`, `register`, `volatile` | `static` y alcance en R01-N07; `extern` en R04 | Completar R01-N07 con los cinco |
| Operadores, precedencia, `?:`, coma | R01-N02 | Está |
| Bits | R01-N03 | Está |
| **printf y scanf a fondo**: banderas `- + 0 #`, ancho, `.prec`, `*`, `%o %x %e %g` | sueltos | Sección nueva en R01-N04 con la tabla del apunte (p. 18) |
| **El preprocesador**: `#define` con parámetros y la trampa de los paréntesis (`CUBO(c+d)`), `#undef`, `#include` con `< >` y `" "`, `#error`, `#if`/`#ifdef`/`#ifndef`, macros contra funciones (`SWAP`) | `#define` simple y guardas | **Nodo nuevo** en R01, después de funciones |
| if, switch, while, do-while, for | R01-N05 y N06 | Está |
| Arrays 1D y 2D, centinela, array de contadores | R02-N01 | Está |
| Cadenas, `string.h`, `ctype.h` | R02-N02 | Está |
| Estructuras, anidadas, arrays de estructuras | R02-N03 y N06 | Está |
| **Uniones** y *little endian* | No está | Sumar a R02-N03 (structs, enum, typedef **y union**) |
| Funciones, prototipos, por valor y «por referencia» con punteros, arrays y structs como argumentos | R01-N07 y R02-N05 | Está |
| Recursividad | R01-N07 | Está |
| Archivos binarios y de texto, modos de `fopen` | R04-N01 y N02 | Está |
| Punteros, aritmética, arrays de punteros, puntero a puntero, errores típicos, `->`, `malloc` y `free` | R02-N04, N05 y R03-N01 | Está |
| **Listas**: inserción al frente, **inserción ordenada**, borrar, recorrido recursivo de ida y vuelta, **lista con arrays** (sin `malloc`) | al frente, al final y una práctica ordenada | Hacer de la ordenada un tema propio en R03-N03 y sumar la lista con arrays como encargo |

**Del Turbo C a C moderno** (en la teoría, sin nombrar a Turbo C): `int main(void)` y `return 0`; sin `conio.h` (ni `clrscr`, `getch`, `gotoxy`); `srand(time(NULL))` y `rand() % n` en lugar de `randomize()` y `random(n)`; limpiar la entrada leyendo hasta `'\n'` en lugar de `fflush(stdin)` (que en C estándar no está definido para entrada); `int` de 4 bytes y no de 2.

**Linux y Windows:** hoy solo la Clase 0 y R04 nombran Windows. Cada nodo que compila algo pasa a tener las dos formas: `gcc` en la terminal de Linux, y en Windows **MSYS2 (UCRT64) con `gcc`** en la terminal o un IDE *(a confirmar cuál usan los alumnos: Code::Blocks, Dev-C++, VS Code)*. Lo mismo para `make`, `gdb`, los sanitizadores (en Windows, `-fsanitize=address` no anda con MinGW: se avisa y se da la alternativa) y las rutas de archivos (`/` contra `\\`).

---

## 3. Los capítulos (crónicas y micro-misiones)

**Clase 0 · Hola, C** — *La boca de la Forja.* Kira despierta junto a un vitral apagado, en la boca de las Forjas. Intenta abrir el portón a espadazos y la espada **se raja**; el portón ni se entera (se abría tirando, no empujando). Ferrum la mira: «Acá nada se abre a golpes. Se abre **sabiendo cuánto pesa cada cosa**». Le da una receta: su primer programa, y el Horno (el compilador) que la convierte en una pieza. Consigue: cartas `main`, `printf`, compilar y ejecutar, del fuente al ejecutable. Gancho: Tizón aparece con su calibre: «¿Lo mediste?».

### Acto I — Templar el metal (R01)

- **N01 · Variables y tipos** — *El depósito de cajones.* Kira mete el clavo 256 en un cajón de 255 y el cajón **se vacía solo** y vuelve a cero. Tizón tiene que contar los 255 de nuevo. Consigue: cartas `int`, `char`, `double`, `sizeof`, desborde.
- **N02 · Operadores** — *La balanza del mostrador.* Chispa cobra la misma herradura 7 lingotes por la mañana y 3 a la tarde: la división entera y el orden de las operaciones deciden quién estafa a quién (esta vez, sin querer, Chispa se estafó a sí mismo).
- **N03 · Operadores de bits** — *La cerradura de las ocho palancas.* Kira intenta abrirla a patadas; Tizón la abre con una máscara de bits. Kira dice que fue suerte.
- **N04 · Entrada y salida** (+ printf a fondo) — *El mostrador de pedidos.* Kira escribe la tabla de precios y Tizón le mide cada columna con el calibre: «Esta está corrida un espacio». El `scanf` sin `&` es el primer goblin que se roba un número.
- **N05 · Condicionales** — *El horno de tres temperaturas.* Kira pone «si hace calor, más fuego» y el horno se derrite. Faltaba un `else`.
- **N06 · Bucles** — *El fuelle.* El primer bucle que no termina deja el fuelle soplando toda la noche; a la mañana, la Forja tiene la temperatura de un volcán y Ferrum, las cejas chamuscadas.
- **N07 · Funciones** (+ especificadores de almacenamiento) — *Los martillos de cada uno.* Cada herrero tiene su martillo y nadie le presta el suyo a nadie (el alcance). En el depósito, entre los pedidos, Kira encuentra **un pedido de plomo** firmado con un vitral.
- **N08 · El preprocesador y las macros** *(nuevo)* — *Los sellos de marcar.* Un sello que se copia en cada pieza antes de entrar al horno: rápido, pero Tizón talla `CUBO(a) a*a*a` sin paréntesis y le sale una partida de herraduras con forma de banana.
- **N09 · Bibliotecas estándar útiles** — *El estante de herramientas.* Kira descubre que lo que le llevó una semana ya estaba en el estante, en `string.h`. Ferrum: «Mirar el estante también es trabajar».
- **N10 · Jefe: el Gólem de Escoria** — *El portón de la Forja.* El gólem está hecho de toda la escoria de la Forja, **incluida la de la primera semana de Kira**. Ella lo vence partiendo el problema en funciones, no a espadazos (la cuenta de la pared queda en 41 a 0). Ferrum le reforja la espada: **la Espada Reforjada**. Gancho: «La próxima la forjás vos».

### Acto II — Los pasillos numerados (R02)

- **N01 · Arrays y matrices** — *Los pasillos de estantes.* Diez estantes numerados del 0 al 9; Kira busca el estante 10 y encuentra un orco durmiendo ahí.
- **N02 · Strings** — *Las etiquetas de los lingotes.* Chispa escribe «ORO» en una etiqueta de tres lugares y no deja lugar para el `'\0'`: la etiqueta sigue leyendo en la de al lado y el lingote de hierro se vende como «OROHIERRO». El primer orco de los textos.
- **N03 · Structs, enum, typedef y union** — *Las fichas de los encargos.* La ficha del pedido de plomo tiene **dos formas de leerse** (union): leída como número dice un peso; leída por bytes, al revés (*little endian*), dice «PARA QUIEN LLEGUE».
- **N04 · Punteros** — *Los carteles que señalan.* Kira sigue un cartel que no apunta a ningún lado, se cae por un hueco y el programa revienta. Hulda la saca con una soga y le regala **el Amuleto del Volcado**: «Para la próxima que te caigas».
- **N05 · Punteros y structs** — *El mapa de los pasillos.* Tizón confunde `.` con `->` y manda una carta a la dirección de la carta.
- **N06 · Arrays de structs** — *El registro de toda la Forja.*
- **N07 · Jefe: la Araña de las Direcciones** — *El pasillo sin fin.* Teje direcciones falsas y cambia los carteles de lugar. Kira, por una vez, no da un espadazo: anota cada dirección, y la Araña se enreda en su propia tela. Consigue: **el Hilo de las Direcciones**. Gancho: el plomo del pedido vino de las Minas.

### Acto III — Las Minas (R03)

Hulda, la capataz, cuenta cada vagoneta. Las Minas son la memoria: lo que se pide se devuelve.

- **N01 · Memoria dinámica** — *Las vagonetas prestadas.* Kira pide diez vagonetas, devuelve nueve y Hulda la hace contar un chiste malo frente a toda la mina. El chiste es tan malo que nadie vuelve a olvidarse un `free`.
- **N02 · Un array que crece** — *La galería que se alarga.* Cada vez que la galería se llena, hay que cavar una más grande y mudar todo (`realloc`); Tizón calcula que conviene duplicarla y, por una vez, nadie le discute.
- **N03 · Listas enlazadas** (+ inserción ordenada y lista con arrays) — *Los vagones enganchados.* Kira engancha los vagones en cualquier orden y el tren de la mina sale al revés. Hay que engancharlos **ordenados por peso**. Al final de una vía muerta, la **veta del plomo** del Vidriero.
- **N04 · Punteros a función** — *Las palancas de las vías.* Una palanca que cambia qué tren sale; Chispa intenta poner una que manda todos los trenes a su puesto.
- **N05 · Jefe: la Sanguijuela de las Minas** — *La galería que se vacía.* Se come cada vagoneta que nadie devolvió y está gordísima (casi todas son de Chispa). Kira la vence liberando todo, y la Sanguijuela queda flaquita y avergonzada. Consigue: **la Lámpara del Minero**. Gancho: el registro de la veta está en el Archivo.

### Acto IV — El Archivo de la Forja (R04)

- **N01 · Archivos de texto** — *Los libros de pedidos.* El Archivero busca sus anteojos durante toda la crónica (los tiene puestos); mientras, Kira aprende a abrir, leer y **cerrar** un libro.
- **N02 · Archivos binarios** — *Las cajas de fichas selladas.* Tizón abre una caja binaria con un editor de texto y ve jeroglíficos; jura que es un idioma antiguo.
- **N03 · Programas en varios archivos** — *Los talleres separados* (con `extern`, guardas y `make`, en Linux y en Windows). Cada taller hace su pieza; si dos talleres hacen la misma, el enlazador grita «¡ya hay una!».
- **N04 · Argumentos de la línea de comandos** — *Los pedidos por ventanilla.* Chispa hace pedidos gritando desde la puerta, todo junto y sin comas.
- **N05 · El menú de consola** — *El mostrador del Archivero.*
- **N06 · Jefe: el Guardián del Archivo** — *La bóveda de los registros.* Solo deja pasar a quien abre y **cierra** cada archivo; Kira se olvida de cerrar uno y el Guardián le cierra el cajón en los dedos. Al segundo intento pasa. Consigue: **el Libro de Registros de Plomo**, con las medidas del marco: el mismo marco que hay en la Torre del Imperio. Gancho: el plomo se fundió bajo la Montaña.

### Acto V — La Prueba del Temple (R05)

- **N01 · Depuración** — *El martillo que escucha* (`gdb` en Linux y en Windows con MSYS2). Ferrum golpea cada pieza y escucha dónde suena hueca; Kira aprende a frenar el programa en una línea en lugar de gritarle.
- **N02 · Tests** — *La prueba de cada pieza.* Tizón, feliz: por fin alguien le paga por medir todo.
- **N03 · Proyecto: la agenda del Gremio** — *El encargo completo.*
- **N04 · Jefe final: el Dragón bajo la Montaña** — *La fragua más honda.* El dragón duerme sobre el plomo del Vidriero y ronca fuego. Kira, que llegó a las Forjas rompiendo la espada contra un portón, forja su propia hoja midiendo cada grado (Tizón le pasa las medidas sin que se las pida, y ella las usa sin protestar): **la Hoja Templada**. Detrás del dragón, **la Matriz del Marco** que dejó el Vidriero.
- **N05 · La Encrucijada del Yunque** — Ferrum golpea el yunque **tres veces** (Kira no sabe qué hacer) y cuenta su pieza del portal. En la pared, debajo de la cuenta de espadazos, Ferrum escribe: «Problemas resueltos midiendo: todos». Tizón se queda de oficial en la Forja. Gheco señala las Sendas: **la Forja Viva** (SDL3) y **los Autómatas** (Arduino).

---

## 4. Lo que hay que construir

1. **Ejecutar C para el alumno en las micro-misiones (D98):** el mismo Clang en WebAssembly que usa el docente al corregir (D66, `public/toolchains/cpp/`), ahora también para el alumno, solo en las micro-misiones y en su navegador (nunca en el servidor). Cambia la regla de CLAUDE.md. Entrada por `stdin` cuando la micro-misión la pida.
2. **Generador de micro-misiones de C** (`scripts/micro-misiones/genc.py`): cada solución se compila y se ejecuta con `gcc -std=c17 -Wall -Wextra`; la salida esperada nunca se escribe a mano, y el código inicial no puede dar ya la salida. Una prueba en Chrome con el Clang del navegador, como las 16 de SQL.
3. **Kira jugable** en `config('game.protagonists.c')`: sus 6 aspectos (ya están las imágenes), el mapa de expediciones de las Forjas, la tienda y las recetas del taller.
4. **Las fichas en PERSONAJES.md** de Maese Ferrum, Tizón, Hulda, Chispa, el Archivero y los siete jefes: **hechas** (2026-10-08). Las que faltan generar están en *Admin → Historia → Personajes* con «Solo sin imagen».
5. **El nodo nuevo** (el preprocesador) y las secciones nuevas (printf a fondo, almacenamiento, union, listas ordenadas), con sus prácticas y la Prueba del sello.
6. **Linux y Windows** en todos los nodos que compilan.
7. **Las crónicas en tercera persona** y los ejemplos con la gente de las Forjas, con las salidas rehechas ejecutando (`app:course-tests`).

## 5. Preguntas abiertas

- **Tizón, Hulda, Chispa y el Archivero**: ¿van esos nombres y esos papeles? (Sus fichas ya están para generar las imágenes; si cambia un nombre, se cambia en la ficha.)
- **¿Qué usan los alumnos en Windows** para compilar C: Code::Blocks, Dev-C++, VS Code con MSYS2?
- **El nodo nuevo cambia la numeración de R01** (el Gólem pasa de N09 a N10). Si hay alumnos con progreso en C en producción, va una migración como la de Java (D96); si no, se renumera directo.
- **¿Hay un examen final de Programación I** con un formato conocido (como BiblioExpress en Java)? Si lo hay, el Dragón puede ser su simulacro.
