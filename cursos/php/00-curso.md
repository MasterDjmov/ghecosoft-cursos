# CURSO

```meta
slug: php
titulo: PHP: El Puerto de los Mensajeros
lenguaje: php
nivel: desde_cero
descripcion_corta: PHP desde cero: páginas web, formularios, sesiones y sistemas con MySQL y MariaDB.
precio_raiz: 10
dias_abono: 30
destacado: si
proximamente: no
publicado: si
```

### Descripción

Aprendé **PHP desde cero**. No hace falta saber programar: cada tema se explica antes de usarse. El curso llega hasta sistemas web completos, con formularios, usuarios, base de datos **MySQL/MariaDB**, una API en JSON y pruebas automáticas, listos para subir a un hosting.

PHP es la lengua de los servidores: responde los pedidos que llegan desde el navegador. Con PHP funcionan WordPress, Wikipedia, buena parte de las tiendas online y la mayoría de los sistemas de gestión de los hostings compartidos. En el Puerto **cada pedido recibe su respuesta**: llega un mensaje, se lo lee con cuidado, se busca lo que pide y se lo despacha.

Cada tema es un **nodo** del árbol. En cada uno leés la explicación, corrés el ejemplo en tu compu y resolvés las **misiones**: al aprobarlas ganás sellos para abrir el siguiente. Cada rama termina con un **jefe**, un proyecto que junta todo lo que aprendiste.

Al final del camino principal llegás a la **Encrucijada de los Sellos**, de donde salen tres Sendas optativas: un **RPG por turnos**, lo esencial del framework **Laravel** y una **aplicación web con JavaScript** que habla con tu API. Y apenas terminás la primera rama se abre otra Senda optativa, la del **Escaparate**: HTML y CSS para armar páginas que se vean bien en cualquier pantalla.

> Qué hace falta: una compu con **PHP 8.2 o más nuevo** y, desde la cuarta rama, **MariaDB o MySQL**. En Windows lo más simple es instalar **XAMPP** (trae PHP, MariaDB y phpMyAdmin juntos); en Linux, `sudo apt install php-cli php-mysql php-mbstring mariadb-server`. Los programas se prueban en tu compu y se entregan pegando el código o subiendo un archivo.

### Temario

- Variables, tipos, textos, entrada por teclado, decisiones, bucles, arrays y funciones
- Clases y objetos: encapsulamiento, herencia, interfaces, traits, enums y excepciones
- Namespaces, autoload y Composer
- La web: HTTP, formularios, validación, seguridad (XSS y CSRF), sesiones, login y subida de archivos
- MySQL y MariaDB: tablas, consultas, relaciones y `JOIN`
- PDO: consultas preparadas, un ABM web completo, transacciones y paginación
- MVC sin framework, una API REST en JSON, pruebas con PHPUnit y subir a un hosting
- Sendas optativas: HTML y CSS, un RPG por turnos, Laravel y JavaScript con `fetch`

# DICCIONARIO

| clave | singular | plural | género | descripción | historia | ámbito |
|---|---|---|---|---|---|---|
| coin.course | sello | sellos | m | La moneda del Puerto: el sello de lacre que cierra cada mensaje despachado. Se gana aprobando misiones obligatorias y abre los nodos del curso. | | curso |
| mentor.name | Elefa | | f | La Capitana del Puerto: una elefanta que despacha los mensajes de todo el mundo y nunca olvida un pedido. | Elefa llegó al Puerto de los Mensajeros cuando era una oficina con un solo mostrador y una bolsa de cartas sin abrir. Hoy dirige muelles, correos y bodegas, y desde su torre ve llegar cada barco. Tiene una memoria de elefanta —nunca se olvida de un pedido— y una sola regla: **ningún mensaje se queda sin respuesta, y ninguna respuesta sale sin revisar**. Desconfía de todo lo que llega de afuera, hasta que lo comprueba. | curso |
| world.region | Puerto de los Mensajeros | | m | La región del mundo cuya lengua arcana es PHP. | | curso |
| story.course_intro | Bienvenida al Puerto | | f | | Llegás al **Puerto de los Mensajeros**, {heroe}. Hay barcos cargando y descargando, gaviotas, y una torre enorme donde no para de sonar una campana: cada campanada es un pedido nuevo que llega de algún lugar del mundo.<br><br>Soy {mentor}, la Capitana del Puerto. Acá hablamos **PHP**: la lengua de los servidores, los que reciben un pedido y despachan una respuesta. Vas a empezar en el Muelle, escribiendo tus primeras cartas, y vas a terminar dirigiendo tu propia oficina, con su bodega llena de registros.<br><br>Cada tema que domines te abre un muelle nuevo; cada misión aprobada te da sellos para abrir el siguiente. | curso |
| story.branch_completed | ¡Muelle despachado! | | m | | {mentor} hace sonar la campana de la torre tres veces, la señal de que un muelle entero funciona solo. —Esta parte del Puerto ya responde con tu código, {heroe}. | curso |
| story.course_completed | ¡Dominaste la lengua del Puerto! | | f | | {mentor} te entrega la llave de la torre y un sello de lacre con tu nombre grabado. —Ya sos capitana o capitán del Puerto, {heroe}. Desde la Encrucijada de los Sellos salen tres caminos: la Arena, la Ciudadela de Laravel y los Mensajes Veloces. Elegí el tuyo. | curso |
| story.portal_piece | Lo que guardó Elefa | | f | La pieza del misterio del portal que se lee al terminar este curso (Mis Crónicas). | Un día llegó al Puerto un mensaje sin remitente, sellado con un sello de vidrio de colores. Decía solamente: *para quien llegue*. Lo guardé veinte años. Creo que ahora es tuyo, {heroe}. | curso |
| beast.slime | slime | slimes | m | Nace de los errores de sintaxis: `Parse error`, y no se ejecuta nada. | Los slimes brotan de los punto y coma olvidados, las llaves sin cerrar, las comillas perdidas y el `$` que falta. PHP los detecta antes de ejecutar y avisa con `Parse error: syntax error, unexpected…`. Son débiles, pero hasta que no los eliminás el programa no arranca. | curso |
| beast.goblin | goblin | goblins | m | Nace de los tipos que no encajan: `TypeError` y las conversiones silenciosas. | Los goblins viven en las conversiones: PHP es generoso y convierte `"10 manzanas"` en `10` sin preguntar, o se niega con un `TypeError` cuando una función pide un `int` y le das un texto. Los más peligrosos son los que pasan en silencio. | curso |
| beast.skeleton | esqueleto | esqueletos | m | Nace de los nombres que no existen: `Undefined variable`, `Call to undefined function`. | Los esqueletos son nombres sin cuerpo: una variable mal escrita, una función que no está incluida, una clase que el autoload no encuentra. En PHP las variables distinguen mayúsculas: `$Nombre` no es `$nombre`. | curso |
| beast.orc | orco | orcos | m | Nace de las claves y posiciones que no existen: `Undefined array key`. | Los orcos atacan donde terminan los arrays: la posición 10 de una lista de 10, la clave `'email'` de un formulario que nadie completó. PHP avisa con un `Warning` y sigue con `null`, y ahí empiezan los problemas. | curso |
| beast.ogre | ogro | ogros | m | Nace de los errores de lógica, entre ellos comparar con `==` en vez de `===`. | El ogro es el más traicionero: el programa corre sin avisos… y el resultado está mal. Su truco favorito en el Puerto es `==`, que dice que `"abc" == 0` era cierto en PHP viejo y que `"1" == "01"`. Solo lo vence quien prueba y compara con `===`. | curso |
| beast.troll | troll | trolls | m | Nace de `null` y de las referencias: `on null`, valores que cambian desde otro lado. | El troll se esconde detrás de lo que no está: una consulta que no encontró nada y devolvió `false`, un objeto `null` al que le pedís una propiedad (`Attempt to read property "nombre" on null`), una variable pasada por referencia que alguien modificó. | curso |
| beast.dragon | dragón | dragones | m | Guardián de los jefes: un problema grande hecho de problemas chicos. | Un dragón no se vence de un golpe. Se lo divide en funciones, clases y páginas, se vence cada una y recién entonces cae. | curso |

## R00-N01 · Clase 0 · Hola, PHP

```meta
tipo: raiz
criatura: slime
temas: prog.entorno, prog.salida
```

### Crónica

La campana de la torre suena otra vez. Un mensajero baja corriendo por la escalera con un papel en la mano, lo deja en el mostrador y se va. En el papel dice solamente: *"¿Hay alguien?"*.

—Todos los días llegan miles así —dice {mentor}, acomodándose la gorra de capitana—. Alguien, en algún lugar del mundo, escribe una dirección en su navegador y nos manda un pedido. Nuestro trabajo es **contestar**. Para eso usamos PHP: escribimos las instrucciones y el servidor las sigue cada vez que llega un mensaje. Empecemos por lo más simple, {heroe}: contestar *"Sí, acá estamos"*.

### Objetivos

- Instalar PHP y comprobar que funciona.
- Escribir y ejecutar tu primer programa en PHP desde la terminal.
- Entender la etiqueta `<?php` y la instrucción `echo`.
- Mostrar texto con saltos de línea y escribir comentarios.
- Reconocer un error de sintaxis (`Parse error`) y leer su mensaje.

### Antes de empezar

Nada: este es el primer nodo. Solo necesitás una compu y ganas.

### Explicación

#### Qué es PHP
PHP es un lenguaje **interpretado**: escribís el programa en un archivo `.php`
(texto) y el intérprete `php` lo lee y lo ejecuta de arriba hacia abajo. No hay un
paso de compilación aparte.

PHP nació para la web: un **servidor** recibe un pedido del navegador, ejecuta un
programa PHP y le devuelve al navegador lo que ese programa "imprimió" (casi
siempre, una página HTML). Pero el mismo PHP también corre en la **terminal**, como
cualquier otro lenguaje. En las primeras ramas vas a usar la terminal, que es más
simple para aprender; en la tercera rama pasás a la web.

#### Instalar PHP
- **Windows**: instalá **XAMPP** (de *apachefriends.org*). Trae PHP, el servidor
  Apache, MariaDB y phpMyAdmin. PHP queda en `C:\xampp\php\php.exe`; para usarlo
  desde cualquier carpeta, agregá `C:\xampp\php` a la variable de entorno `PATH`.
- **Linux (Ubuntu, Debian)**: `sudo apt install php-cli php-mbstring`.
- **macOS**: con Homebrew, `brew install php`.

Después, en una terminal:
```bash
php -v
```
Si responde algo como `PHP 8.3.12 (cli)`, está listo. Este curso usa **PHP 8.2 o
más nuevo**.

#### Tu primer programa
Creá un archivo llamado **`hola.php`** con este contenido:
```php
<?php
echo "Sí, acá estamos\n";
```
Y ejecutalo desde la carpeta donde lo guardaste:
```bash
php hola.php
```
En la terminal aparece `Sí, acá estamos`.

#### La anatomía de un programa
| Parte | Qué significa |
|---|---|
| `<?php` | abre el **modo PHP**: desde acá, el intérprete lee instrucciones |
| `echo "…";` | una **instrucción**: muestra el texto |
| `"\n"` | un **salto de línea** dentro del texto |
| `;` | cada instrucción termina con punto y coma |

Todo lo que esté **fuera** de `<?php` se muestra tal cual, sin ejecutarse. Por eso
un archivo PHP puede mezclar texto (o HTML) con código: es lo que lo hace tan
cómodo para la web. Si el archivo es solo código, se abre con `<?php` en la
primera línea y **no se cierra** (no hace falta el `?>` final).

#### Mostrar texto
```php
echo "Con salto de línea al final\n";
echo "Sin salto... ";
echo "sigue en la misma línea\n";
echo "Comillas: \"así\" y barra: \\\n";
echo "\n";                          // una línea vacía
echo "Suma: ", 2 + 3, "\n";         // echo acepta varios valores separados por coma
```
`echo` **no** agrega un salto de línea: lo ponés vos con `\n`. Dentro de comillas
dobles, `\n` es un salto de línea, `\"` una comilla y `\\` una barra.

#### Comentarios
```php
// comentario de una línea
# también de una línea
/* comentario
   de varias líneas */
/** comentario de documentación: lo vas a usar más adelante */
```
El intérprete los ignora: son notas para las personas.

#### Cuando algo sale mal
Si escribís algo que PHP no entiende, no se ejecuta **nada** y aparece un
**error de sintaxis**:
```
PHP Parse error:  syntax error, unexpected token "echo", expecting "," or ";" in /home/kira/hola.php on line 3
```
Se lee así: **qué pasó** (`syntax error`: encontró `echo` donde esperaba una coma
o un punto y coma) y **dónde** (archivo `hola.php`, **línea 3**). Muchas veces el
error real está en la línea **anterior**: ahí faltaba el `;`.

Otros errores aparecen con el programa ya andando, como dividir por cero:
```
PHP Fatal error:  Uncaught DivisionByZeroError: Division by zero in /home/kira/cuenta.php:4
```
Siempre leé el mensaje entero: dice qué pasó, en qué archivo y en qué línea.

#### Probar cosas sueltas
`php -a` abre el **modo interactivo**: escribís una instrucción, apretás Enter y
se ejecuta. Sirve para probar algo rápido (se sale con `exit`).

> **Si venís de otro lenguaje.** Las variables llevan `$` adelante (`$nombre`),
> no se declaran con tipo y el programa corre de arriba abajo, sin `main`. Para
> unir textos se usa el **punto** (`.`), no el `+`.

### Código de ejemplo

```php
<?php
/*
 * Clase 0 del Puerto: mostrar texto con echo.
 * Se ejecuta con: php hola.php
 */
echo "=== Puerto de los Mensajeros ===\n";
echo "Mensaje recibido: ¿Hay alguien?\n";
echo "Respuesta: ";
echo "Sí, acá estamos.\n";

// Secuencias de escape dentro de un texto
echo "Sello: \"DESPACHADO\"\n";
echo "Ruta: C:\\puerto\\muelle\n";
echo "Carga:\n  - una bolsa de cartas\n  - un mapa\n";

echo "\n";                                   // línea vacía
echo "Barcos en el muelle: ", 3 + 4, "\n";    // echo con varios valores
echo "Bienvenida al Puerto.\n";
```

### Salida esperada

```
=== Puerto de los Mensajeros ===
Mensaje recibido: ¿Hay alguien?
Respuesta: Sí, acá estamos.
Sello: "DESPACHADO"
Ruta: C:\puerto\muelle
Carga:
  - una bolsa de cartas
  - un mapa

Barcos en el muelle: 7
Bienvenida al Puerto.
```

### ¿Para qué sirve?

Todo programa PHP, del más chico al más grande, termina haciendo lo mismo que este: **mostrar algo**. En la web, lo que mostrás con `echo` es lo que ve el navegador. Y los mensajes de error son la primera herramienta para entender qué pasa: quien lee rápido un `Parse error` o un `Fatal error` ahorra horas.

### Errores habituales

**Slime: falta el punto y coma.**
```
PHP Parse error:  syntax error, unexpected token "echo", expecting "," or ";" in hola.php on line 3
```
Mirá la línea que dice el mensaje **y la anterior**, y agregá el `;`.

**Slime: comillas sin cerrar.** Si abrís una comilla y no la cerrás, PHP sigue
leyendo hasta el final del archivo:
```
PHP Parse error:  syntax error, unexpected end of file in hola.php on line 9
```

**Esqueleto: falta `<?php`.** Si el archivo no empieza con `<?php`, PHP no ejecuta
nada: **muestra el código** tal cual, como si fuera texto.

**Goblin: `php` no se reconoce.** `'php' no se reconoce como un comando interno o
externo` (Windows) o `php: command not found` (Linux): PHP no está instalado o su
carpeta no está en el `PATH`.

**Slime: el `\n` entre comillas simples.** `echo 'Hola\n';` muestra literalmente
`Hola\n`: los saltos de línea solo funcionan dentro de comillas **dobles**.

### Misión R00-N01-M1 · El aviso del muelle

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí un programa `aviso.php` que muestre el aviso de llegada de un barco,
exactamente así:

- Un título entre signos `=`.
- Tres renglones de datos: el nombre del barco, de dónde viene y qué trae.
- Una línea vacía.
- El sello final entre comillas dobles.

#### Criterio de aprobación

- Empieza con `<?php` y cada instrucción termina en `;`.
- Usa `\"` para las comillas y `\n` para los saltos de línea.
- La salida coincide con la esperada.

#### Salida esperada

```
==== AVISO DE LLEGADA ====
Barco: La Gaviota
Viene de: el Valle de la Serpiente
Trae: cartas y especias

Sello: "PUEDE AMARRAR"
```

#### Solución de referencia

```php
<?php
// Mision 1 - El aviso del muelle: mostrar texto con formato.
echo "==== AVISO DE LLEGADA ====\n";
echo "Barco: La Gaviota\n";
echo "Viene de: el Valle de la Serpiente\n";
echo "Trae: cartas y especias\n";
echo "\n";
echo "Sello: \"PUEDE AMARRAR\"\n";
```

### Misión R00-N01-M2 · La carta mojada

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Esta carta llegó mojada y tiene **tres errores**: PHP no la puede leer. Copiala,
ejecutala, leé cada mensaje y arreglala hasta que muestre la salida esperada. No
cambies los textos.

#### Criterio de aprobación

- Se ejecuta sin errores.
- La salida coincide con la esperada.

#### Código inicial

```php
echo "La carta dice:\n"
echo "  Quien lee los errores,\n";
echo '  despacha antes.\n";
Echo "  Firmado: la Capitana\n";
```

#### Salida esperada

```
La carta dice:
  Quien lee los errores,
  despacha antes.
  Firmado: la Capitana
```

#### Solución de referencia

```php
<?php
// Mision 2 - La carta mojada: faltaba <?php, faltaba un ; y una comilla
// simple no cerraba con la doble. (Echo con mayúscula funciona, porque las
// palabras del lenguaje no distinguen mayúsculas, pero se escriben en minúscula.)
echo "La carta dice:\n";
echo "  Quien lee los errores,\n";
echo "  despacha antes.\n";
echo "  Firmado: la Capitana\n";
```

### Misión R00-N01-M3 · El cartel de la fonda

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La fonda del puerto necesita un cartel. Mostralo usando **un solo** `echo` con
saltos de línea `\n` para el menú, y después otro `echo` con el total calculado
dentro del programa: un guiso (1200) más un pan (300) más un mate cocido (450).

#### Criterio de aprobación

- El menú sale de un único `echo` con `\n`.
- El total se calcula con `+`, no se escribe a mano.

#### Salida esperada

```
FONDA LA TROMPA ALEGRE
----------------------
Guiso ........ 1200
Pan .......... 300
Mate cocido .. 450
Total: 1950
```

#### Solución de referencia

```php
<?php
// Mision 3 - El cartel de la fonda: \n dentro de un texto y un total calculado.
echo "FONDA LA TROMPA ALEGRE\n----------------------\nGuiso ........ 1200\nPan .......... 300\nMate cocido .. 450\n";
echo "Total: ", 1200 + 300 + 450, "\n";
```

### Encargo R00-N01-E1 · El recibo del kiosco

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El kiosco del muelle quiere imprimir un recibo en su impresora de tickets.
Mostrá el nombre del kiosco, la fecha, tres productos con su precio, una línea
separadora y el total (calculado con `+`). Agregá un comentario arriba de cada
parte del recibo.

#### Criterio de aprobación

- Tiene comentarios que explican cada parte.
- El total se calcula dentro del programa.

#### Salida esperada

```
KIOSCO EL AMARRE
Fecha: 29/09/2026
Alfajor ........ 900
Agua ........... 1100
Chicles ........ 450
---------------------
TOTAL .......... 2450
```

#### Solución de referencia

```php
<?php
// Encargo - El recibo del kiosco.

// Encabezado
echo "KIOSCO EL AMARRE\n";
echo "Fecha: 29/09/2026\n";
// Productos
echo "Alfajor ........ 900\n";
echo "Agua ........... 1100\n";
echo "Chicles ........ 450\n";
// Total
echo "---------------------\n";
echo "TOTAL .......... ", 900 + 1100 + 450, "\n";
```

### Prueba del sello

#### ¿Qué hace el comando `php hola.php`?

Le pide al intérprete de PHP que lea el archivo `hola.php` y ejecute sus instrucciones de arriba hacia abajo.

#### ¿Para qué sirve `<?php`?

Abre el modo PHP: lo que viene después se ejecuta como código. Lo que está fuera de `<?php … ?>` se muestra tal cual.

#### ¿`echo` agrega un salto de línea al final?

No. El salto de línea se escribe con `\n` dentro de comillas dobles.

#### ¿Qué diferencia hay entre `"Hola\n"` y `'Hola\n'`?

Con comillas dobles, `\n` es un salto de línea; con comillas simples se muestra literalmente la barra y la `n`.

#### En un `Parse error`, ¿dónde conviene buscar el problema?

En la línea que indica el mensaje y en la anterior: muchas veces falta un `;` o una comilla en la línea de arriba.

### Soluciones (docente)

Sale de `21-PHP/01-Hola-PHP`, reescrito para empezar de cero (el capítulo original compara con JavaScript). Se trabaja por terminal (`php archivo.php`) hasta la rama 3, donde se pasa a la web con `php -S`. La misión 2 tiene tres errores: falta `<?php`, falta el `;` de la primera línea y la comilla simple que abre `'  despacha antes.\n"` no cierra. `Echo` en mayúscula es una trampa: funciona, pero se corrige por estilo (la solución lo aclara).
