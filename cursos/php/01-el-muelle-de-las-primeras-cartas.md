# RAMA R01 · El Muelle de las Primeras Cartas: los fundamentos

```meta
tipo: tronco
posicion: 1
```

## R01-N01 · Variables, tipos y conversiones

```meta
tipo: tema
padre: R00-N01
precio: 10
criatura: goblin
temas: prog.variables
```

### Crónica

En el primer muelle hay una fila de cajones de madera, cada uno con una etiqueta pintada a mano: *peso*, *destino*, *¿frágil?*. Un estibador mete en el cajón *peso* una bolsa que dice "12 kilos y medio".

—En el Puerto los cajones no tienen tipo fijo —explica {mentor}—. Podés guardar un número, un texto o un "sí/no" en cualquiera. Es cómodo, {heroe}, pero hay que saber **qué hay adentro** de cada cajón. PHP a veces convierte las cosas solo, y ahí nacen los goblins.

### Objetivos

- Crear variables y cambiar su valor.
- Conocer los tipos básicos: `int`, `float`, `string`, `bool` y `null`.
- Ver el tipo y el valor de una variable con `var_dump` y `gettype`.
- Declarar constantes con `const` y `define`.
- Convertir entre tipos a propósito (*casting*) y entender las conversiones automáticas.

### Antes de empezar

- Escribir y ejecutar un programa con `echo` (Clase 0).

### Explicación

#### Crear una variable
Una **variable** es un cajón con nombre donde se guarda un valor. En PHP el
nombre empieza con **`$`** y se crea la primera vez que le asignás algo:
```php
$vidas = 3;              // un entero
$precio = 1250.75;       // un decimal
$tieneLlave = true;      // verdadero o falso
$nombre = "Kira";        // un texto
$sinDueno = null;        // "nada": todavía no tiene valor
```
Después se puede cambiar el valor, y hasta el tipo:
```php
$vidas = $vidas - 1;     // ahora vale 2
$vidas = "muchas";       // ahora es un texto (se puede, pero no conviene)
```
Los nombres van en *camelCase* (`$puntosDeVida`), empiezan con letra o `_` y
**distinguen mayúsculas**: `$nombre` y `$Nombre` son dos variables distintas.

#### Los tipos básicos
| Tipo | Guarda | Ejemplo |
|---|---|---|
| `int` | enteros | `42`, `-7`, `1_000_000` |
| `float` | decimales | `3.14`, `1.5e3` (1500.0) |
| `string` | textos | `"Kira"`, `'hola'` |
| `bool` | verdadero o falso | `true`, `false` |
| `null` | la ausencia de valor | `null` |

Más adelante vas a usar `array` (listas y diccionarios) y objetos.

#### Ver qué hay en el cajón
`echo` muestra el valor, pero no el tipo. Para depurar se usa **`var_dump`**, que
muestra las dos cosas:
```php
var_dump(42);          // int(42)
var_dump(12.5);        // float(12.5)
var_dump("Kira");      // string(4) "Kira"   ← 4 es la cantidad de bytes
var_dump(true);        // bool(true)
var_dump(null);        // NULL
echo gettype(12.5);    // double  (el nombre histórico de float)
```
Ojo con `echo` y los booleanos: `echo true` muestra `1` y `echo false` **no
muestra nada**. Por eso para ver un `bool` se usa `var_dump`.

#### Constantes
Un valor que no cambia en todo el programa se declara como **constante**, sin `$`
y en mayúsculas:
```php
const IVA = 0.21;
define('PUERTO', 'Mensajeros');   // otra forma, útil dentro de un if
echo IVA;                        // 0.21
```
Si intentás reasignar una constante, PHP da un error.

#### Conversiones automáticas
PHP es de **tipado dinámico y débil**: cuando una operación necesita otro tipo,
intenta convertir solo.
```php
echo 5 + "3";        // 8: el texto "3" se convierte en número
echo 5 . 3;          // 53: el punto une textos, así que 5 y 3 se vuelven "5" y "3"
echo 7 / 2;          // 3.5: la división siempre puede dar decimal
echo "10" * "2";     // 20
```
Si el texto no es un número, PHP 8 se enoja:
```php
echo 5 + "3 manzanas";   // 8, pero con "Warning: A non-numeric value encountered"
echo 5 + "manzanas";     // TypeError: Unsupported operand types: int + string
```
Esas conversiones silenciosas son el terreno de los **goblins**: si un dato llega
como texto, conviene convertirlo a propósito.

#### Casting: convertir a propósito
```php
$kilos = (int) "12.75";      // 12   (corta los decimales)
$precio = (float) "1250.5";  // 1250.5
$texto = (string) 42;        // "42"
$activo = (bool) 0;          // false
$n = intval("0042");         // 42
```
Para `bool`, son **falsos**: `0`, `0.0`, `""`, `"0"`, `null` y el array vacío. Todo
lo demás es verdadero (¡incluso `"false"` y `" "`!).

#### El tipo de una variable, de verdad
Para preguntar el tipo hay funciones `is_*`:
```php
is_int(5);          // true
is_string("5");     // true
is_numeric("5.2");  // true: "parece un número"
is_numeric("5a");   // false
```

#### Los decimales no son exactos
Los `float` se guardan en binario y algunos decimales no tienen representación
exacta:
```php
var_dump(0.1 + 0.2);             // float(0.30000000000000004)
echo round(0.1 + 0.2, 2);        // 0.3
```
Para mostrar dinero se redondea (`round`, `number_format`), y para cálculos
exactos de plata se trabaja en **centavos** con enteros.

> **Si venís de un lenguaje con tipos (Java, C).** En PHP no se declara el tipo de
> una variable; sí se puede declarar el tipo de los parámetros de una función,
> como vas a ver en el nodo de funciones.

### Código de ejemplo

```php
<?php
/*
 * El cajón del muelle: variables, tipos y conversiones.
 */
const CAPACIDAD_KG = 500;

$barco = "La Gaviota";
$cajones = 12;
$pesoPorCajon = 37.5;
$fragil = true;
$destino = null;

echo "Barco: ", $barco, "\n";
echo "Carga total: ", $cajones * $pesoPorCajon, " kg de ", CAPACIDAD_KG, "\n";

// var_dump muestra tipo y valor
var_dump($cajones);
var_dump($pesoPorCajon);
var_dump($barco);
var_dump($fragil);
var_dump($destino);
echo "gettype de 37.5: ", gettype($pesoPorCajon), "\n";

// Conversiones automáticas
echo "5 + \"3\" = ", 5 + "3", "\n";
echo "5 . 3 = ", 5 . 3, "\n";
echo "7 / 2 = ", 7 / 2, "\n";

// Casting
$leido = "12.75";
echo "(int) \"12.75\" = ", (int) $leido, "\n";
echo "(float) \"12.75\" = ", (float) $leido, "\n";
var_dump((bool) "0");
var_dump((bool) "false");

// Los decimales no son exactos
var_dump(0.1 + 0.2);
echo "redondeado: ", round(0.1 + 0.2, 2), "\n";
```

### Salida esperada

```
Barco: La Gaviota
Carga total: 450 kg de 500
int(12)
float(37.5)
string(10) "La Gaviota"
bool(true)
NULL
gettype de 37.5: double
5 + "3" = 8
5 . 3 = 53
7 / 2 = 3.5
(int) "12.75" = 12
(float) "12.75" = 12.75
bool(false)
bool(true)
float(0.30000000000000004)
redondeado: 0.3
```

### ¿Para qué sirve?

Todo lo que llega a un programa PHP desde afuera —un formulario, una URL, un archivo— llega como **texto**. Saber qué tipo tiene cada dato y convertirlo a propósito es lo que separa un sistema que funciona de uno que suma `"10"` + `"10"` y a veces da `20`, a veces `1010`, y a veces se rompe.

### Errores habituales

**Esqueleto: la variable mal escrita.**
```
PHP Warning:  Undefined variable $Barco in carga.php on line 6
```
PHP distingue mayúsculas en las variables: `$barco` no es `$Barco`. Además sigue
ejecutando con `null`, así que el error aparece más abajo.

**Slime: falta el `$`.** `barco = "La Gaviota";` da `Parse error: syntax error,
unexpected token "="`. Todas las variables llevan `$`.

**Goblin: un texto que no es un número.**
```
PHP Fatal error:  Uncaught TypeError: Unsupported operand types: int + string
```
Aparece al operar con un texto como `"manzanas"`. Convertí o validá antes.

**Ogro: `echo` de un booleano.** `echo false;` no muestra nada y `echo true;`
muestra `1`. Para depurar, `var_dump`.

**Goblin: `(int)` corta, no redondea.** `(int) 12.99` es `12`. Si querés el entero
más cercano, `round(12.99)` (que da `13.0`, un float) o `(int) round(12.99)`.

### Misión R01-N01-M1 · El manifiesto de carga

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Declará variables para describir la carga de un barco: el nombre del barco
(texto), la cantidad de cajones (entero), el peso de cada cajón (decimal) y si
lleva carga frágil (booleano). Declará también una constante con la capacidad
máxima del barco en kilos. Mostrá el manifiesto con `echo` y, al final, el
`var_dump` de las cuatro variables.

#### Criterio de aprobación

- Usa una variable para cada dato y una constante para la capacidad.
- El peso total se calcula con las variables.
- La salida coincide con la esperada.

#### Salida esperada

```
MANIFIESTO DE CARGA
Barco: El Albatros
Cajones: 15
Peso por cajón: 42.5 kg
Peso total: 637.5 kg de 800
string(11) "El Albatros"
int(15)
float(42.5)
bool(false)
```

#### Solución de referencia

```php
<?php
// Mision 1 - El manifiesto de carga: variables, tipos y una constante.
const CAPACIDAD = 800;

$barco = "El Albatros";
$cajones = 15;
$pesoCajon = 42.5;
$fragil = false;

echo "MANIFIESTO DE CARGA\n";
echo "Barco: ", $barco, "\n";
echo "Cajones: ", $cajones, "\n";
echo "Peso por cajón: ", $pesoCajon, " kg\n";
echo "Peso total: ", $cajones * $pesoCajon, " kg de ", CAPACIDAD, "\n";
var_dump($barco, $cajones, $pesoCajon, $fragil);
```

### Misión R01-N01-M2 · Los papeles del aduanero

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El aduanero recibe todos los datos como **texto**, porque vienen escritos en un
papel: `"15"` cajones, `"42.5"` kilos cada uno y `"3.99"` monedas de impuesto por
kilo. Convertí cada uno al tipo correcto con *casting* y mostrá:

1. El `var_dump` de cada valor ya convertido.
2. El peso total.
3. El impuesto total redondeado a 2 decimales con `round`.
4. El impuesto total truncado a entero con `(int)`.

#### Criterio de aprobación

- Convierte con `(int)` y `(float)`, no escribe los números a mano.
- Usa `round` para los dos decimales.
- La salida coincide con la esperada.

#### Salida esperada

```
int(15)
float(42.5)
float(3.99)
Peso total: 637.5 kg
Impuesto: 2543.63
Impuesto truncado: 2543
```

#### Solución de referencia

```php
<?php
// Mision 2 - Los papeles del aduanero: casting de textos a números.
$papelCajones = "15";
$papelKilos = "42.5";
$papelImpuesto = "3.99";

$cajones = (int) $papelCajones;
$kilos = (float) $papelKilos;
$impuestoPorKilo = (float) $papelImpuesto;

var_dump($cajones, $kilos, $impuestoPorKilo);

$pesoTotal = $cajones * $kilos;
$impuesto = $pesoTotal * $impuestoPorKilo;
echo "Peso total: ", $pesoTotal, " kg\n";
echo "Impuesto: ", round($impuesto, 2), "\n";
echo "Impuesto truncado: ", (int) $impuesto, "\n";
```

### Misión R01-N01-M3 · ¿Verdadero o falso?

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La Capitana tiene una lista de valores y quiere saber cuáles PHP considera
**verdaderos** y cuáles **falsos**. Para cada uno de estos valores, mostrá su
`var_dump` y después el `var_dump` de convertirlo a `bool`:

`0`, `1`, `-1`, `""`, `" "`, `"0"`, `"0.0"`, `"false"`, `null`, `0.0`.

Usá una línea por valor con el formato del ejemplo (`var_dump` acepta varios
valores separados por coma).

#### Criterio de aprobación

- Muestra los diez valores y su conversión a `bool`.
- La salida coincide con la esperada.

#### Salida esperada

```
int(0)
bool(false)
int(1)
bool(true)
int(-1)
bool(true)
string(0) ""
bool(false)
string(1) " "
bool(true)
string(1) "0"
bool(false)
string(3) "0.0"
bool(true)
string(5) "false"
bool(true)
NULL
bool(false)
float(0)
bool(false)
```

#### Solución de referencia

```php
<?php
// Mision 3 - ¿Verdadero o falso?: la conversión a bool de cada valor.
var_dump(0, (bool) 0);
var_dump(1, (bool) 1);
var_dump(-1, (bool) -1);
var_dump("", (bool) "");
var_dump(" ", (bool) " ");
var_dump("0", (bool) "0");
var_dump("0.0", (bool) "0.0");
var_dump("false", (bool) "false");
var_dump(null, (bool) null);
var_dump(0.0, (bool) 0.0);
```

### Encargo R01-N01-E1 · El vuelto en centavos

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una despensa del puerto cobra con decimales y a veces el vuelto sale raro. Una
clienta compra por **$1234.56** y paga con **$2000**. Calculá el vuelto de dos
maneras y mostrá las dos con `var_dump`:

1. Con `float`: `2000 - 1234.56`.
2. En **centavos** con enteros: `200000 - 123456`, y después pasalo a pesos
   dividiendo por 100.

Al final, mostrá el vuelto con `number_format($vuelto, 2, ',', '.')`, que es como
se escribe en Argentina.

#### Criterio de aprobación

- Calcula el vuelto con `float` y con centavos enteros.
- Muestra el resultado formateado con coma decimal.

#### Salida esperada

```
float(765.44)
int(76544)
float(765.44)
Vuelto: $765,44
```

#### Solución de referencia

```php
<?php
// Encargo - El vuelto en centavos: float vs enteros para la plata.
$conFloat = 2000 - 1234.56;
var_dump($conFloat);

$centavos = 200000 - 123456;
var_dump($centavos);
$vuelto = $centavos / 100;
var_dump($vuelto);

echo "Vuelto: $", number_format($vuelto, 2, ',', '.'), "\n";
```

### Prueba del sello

#### ¿Con qué empieza el nombre de toda variable en PHP?

Con el signo `$`, por ejemplo `$nombre`.

#### ¿Qué muestra `var_dump("Kira")`?

`string(4) "Kira"`: el tipo, el largo en bytes y el valor.

#### ¿Cuánto da `(int) "12.75"`?

`12`: el casting a entero corta los decimales, no redondea.

#### ¿`"0"` es verdadero o falso para PHP?

Falso. Son falsos `0`, `0.0`, `""`, `"0"`, `null` y el array vacío; todo lo demás es verdadero.

#### ¿Por qué conviene trabajar la plata en centavos enteros?

Porque los `float` no guardan exacto algunos decimales (`0.1 + 0.2` no da justo `0.3`); con enteros las cuentas son exactas.

### Soluciones (docente)

Sale de `21-PHP/02-Tipos`, reescrito desde cero. Se evita `declare(strict_types=1)` hasta el nodo de funciones, donde tiene sentido. El `echo 5 + "3 manzanas"` de la explicación da `8` con un `Warning: A non-numeric value` en PHP 8 (es un "leading-numeric string"); no está en el código de ejemplo para que el ejemplo corra sin avisos.

## R01-N02 · Operadores y expresiones

```meta
tipo: tema
padre: R01-N01
precio: 10
criatura: ogre
temas: prog.operadores
```

### Crónica

En la oficina de pesaje del segundo muelle, un empleado hace cuentas en un pizarrón: kilos por cajón, cajones por bodega, cuánto sobra. Al lado, una balanza de dos platos compara dos bolsas.

—Las cuentas se hacen con **operadores** —dice {mentor}—. Sumar, comparar, decidir si algo es cierto. Cuidado con la balanza, {heroe}: en el Puerto hay dos maneras de preguntar si dos cosas son iguales, y solo una no miente.

### Objetivos

- Usar los operadores aritméticos, incluidos el resto `%` y la potencia `**`.
- Usar la asignación compuesta y el incremento.
- Comparar con `===` y `!==`, y entender por qué `==` es peligroso.
- Combinar condiciones con `&&`, `||` y `!`.
- Usar el operador ternario, `??` y la nave espacial `<=>`.
- Unir textos con el punto `.`.

### Antes de empezar

- Variables y tipos (R01-N01).

### Explicación

#### Aritméticos
| Operador | Qué hace | Ejemplo | Resultado |
|---|---|---|---|
| `+` `-` `*` | suma, resta, multiplicación | `7 * 3` | `21` |
| `/` | división (puede dar decimal) | `7 / 2` | `3.5` |
| `intdiv()` | división entera | `intdiv(7, 2)` | `3` |
| `%` | resto de la división | `7 % 2` | `1` |
| `**` | potencia | `2 ** 10` | `1024` |

El resto sirve para saber si un número es par (`$n % 2 === 0`) o para "dar la
vuelta" (las horas de un reloj: `($hora + 5) % 24`).

#### Asignación compuesta, incremento y decremento
```php
$oro = 100;
$oro += 25;    // $oro = $oro + 25   → 125
$oro -= 5;     // 120
$oro *= 2;     // 240
$oro /= 4;     // 60 (puede quedar float)
$nombre = "Kira";
$nombre .= " Valdez";   // une texto: "Kira Valdez"
$barcos = 3;
$barcos++;     // 4
$barcos--;     // 3
```

#### Comparación
| Operador | Pregunta |
|---|---|
| `===` | ¿son iguales **y del mismo tipo**? |
| `!==` | ¿son distintos (en valor o en tipo)? |
| `<` `>` `<=` `>=` | menor, mayor… |
| `==` `!=` | ¿son iguales "después de convertir"? |

**Usá siempre `===` y `!==`.** El `==` convierte antes de comparar y da sorpresas:
```php
var_dump(1 == "1");        // true
var_dump(1 === "1");       // false: int contra string
var_dump("1" == "01");     // true  (los dos "parecen" el número 1)
var_dump("1" === "01");    // false
var_dump(null == false);   // true
var_dump(0 == "");         // false en PHP 8 (true en PHP 7: ¡cambió!)
```
El `==` es el truco favorito del **ogro**: el programa corre, pero la comparación
dice que dos cosas distintas son iguales.

#### Lógicos
| Operador | Significa | Es verdadero cuando… |
|---|---|---|
| `&&` | Y | las dos condiciones son verdaderas |
| `\|\|` | O | al menos una es verdadera |
| `!` | NO | la condición es falsa |

```php
$edad = 17;
$conPermiso = true;
$puedeViajar = $edad >= 18 || $conPermiso;   // true
```
PHP evalúa "en cortocircuito": en `A && B`, si `A` es falso ni mira `B`.

#### El ternario y `??`
```php
$estado = $puntos >= 60 ? "aprobado" : "a recuperar";
$apodo = $apodo ?? "sin apodo";   // si $apodo es null (o no existe), usa "sin apodo"
$apodo ??= "sin apodo";           // lo mismo, abreviado
```
`??` (*null coalescing*) es clave en la web: `$_GET['pagina'] ?? 1` usa `1` si el
dato no vino.

#### La nave espacial `<=>`
Compara y devuelve `-1`, `0` o `1`:
```php
echo 3 <=> 5;     // -1 (menor)
echo 5 <=> 5;     //  0 (igual)
echo 7 <=> 5;     //  1 (mayor)
```
La vas a usar para ordenar listas.

#### Unir textos: el punto
```php
echo "Total: " . (2 + 3) . " barcos";   // Total: 5 barcos
```
En PHP el `+` **siempre suma** números y el `.` **siempre une** textos. Por eso
`"2" + "3"` da `5` y `"2" . "3"` da `"23"`.

#### Precedencia
Como en matemática: primero `**`, después `*` `/` `%`, después `+` `-` y **recién
después** el `.`. Por eso en PHP 8 `"Total: " . 2 + 3` da `"Total: 5"` (en PHP 7
daba `3` y un aviso: cambió). Ante la duda, **paréntesis**: `"Total: " . (2 + 3)`
se lee igual en cualquier versión.

### Código de ejemplo

```php
<?php
/*
 * La oficina de pesaje: operadores aritméticos, de comparación y lógicos.
 */
$kilos = 1250;
$porCajon = 40;

echo "Cajones llenos: ", intdiv($kilos, $porCajon), "\n";
echo "Kilos sueltos: ", $kilos % $porCajon, "\n";
echo "División con decimales: ", $kilos / $porCajon, "\n";
echo "2 elevado a 10: ", 2 ** 10, "\n";

$bodega = 0;
$bodega += 300;
$bodega += 450;
$bodega -= 100;
echo "En la bodega: $bodega kg\n";

// === contra ==
var_dump(1 == "1", 1 === "1");
var_dump("1" == "01", "1" === "01");

// Lógicos
$edad = 17;
$conPermiso = true;
$puedeEmbarcar = $edad >= 18 || $conPermiso;
var_dump($puedeEmbarcar);

// Ternario y ??
$peso = 620;
echo "El barco va ", $peso > 500 ? "cargado" : "liviano", "\n";
$capitan = null;
echo "Capitán: ", $capitan ?? "a designar", "\n";

// La nave espacial
echo "3 <=> 5: ", 3 <=> 5, "\n";
echo "Total: " . ($bodega + 50) . " kg\n";
```

### Salida esperada

```
Cajones llenos: 31
Kilos sueltos: 10
División con decimales: 31.25
2 elevado a 10: 1024
En la bodega: 650 kg
bool(true)
bool(false)
bool(true)
bool(false)
bool(true)
El barco va cargado
Capitán: a designar
3 <=> 5: -1
Total: 700 kg
```

### ¿Para qué sirve?

Con estos operadores se hace **toda** la lógica de un sistema: calcular un total con IVA, decidir si un usuario puede entrar, repartir productos en cajas, ordenar una lista por precio. Y usar `===` en lugar de `==` evita una de las fallas de seguridad más conocidas de PHP (comparar contraseñas o códigos con `==`).

### Errores habituales

**Ogro: comparar con `==`.** `"1e3" == "1000"` da `true` porque los dos "parecen"
el mismo número. Con `===` da `false`, como corresponde.

**Ogro: `=` en lugar de `===`.** `if ($rol = "admin")` **asigna** `"admin"` y
siempre es verdadero. Para comparar, `===`.

**Goblin: `+` para unir textos.** `"Hola " + $nombre` da `TypeError: Unsupported
operand types: string + string`. Para unir se usa el punto: `"Hola " . $nombre`.

**Ogro: el punto y la suma sin paréntesis.** `echo "Total: " . 2 + 3;` da
`Total: 5` en PHP 8 pero `3` en PHP 7: el código cambia de significado según la
versión. Poné paréntesis: `"Total: " . (2 + 3)`.

**Goblin: división por cero.** `10 % 0` o `intdiv(10, 0)` cortan el programa con
`DivisionByZeroError`. Revisá el divisor antes.

### Misión R01-N02-M1 · El reloj de la torre

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El reloj de la torre del Puerto cuenta los **minutos** desde la medianoche. Hoy
marca `937`. Mostrá qué hora es (horas y minutos, con `intdiv` y `%`), y qué hora
va a ser dentro de **600 minutos** (cuando pasa de las 24 horas vuelve a empezar:
usá `% 24`). Mostrá los minutos siempre con dos cifras usando
`str_pad($minutos, 2, "0", STR_PAD_LEFT)`.

#### Criterio de aprobación

- Usa `intdiv` y `%` para horas y minutos.
- El cálculo de "dentro de 600 minutos" da la vuelta con `% 24`.
- La salida coincide con la esperada.

#### Salida esperada

```
Ahora son las 15:37
En 600 minutos: 1:37
```

#### Solución de referencia

```php
<?php
// Mision 1 - El reloj de la torre: intdiv y % para horas y minutos.
$minutosDelDia = 937;

$horas = intdiv($minutosDelDia, 60);
$minutos = $minutosDelDia % 60;
echo "Ahora son las ", $horas, ":", str_pad($minutos, 2, "0", STR_PAD_LEFT), "\n";

$despues = $minutosDelDia + 600;
$horasDespues = intdiv($despues, 60) % 24;
$minutosDespues = $despues % 60;
echo "En 600 minutos: ", $horasDespues, ":", str_pad($minutosDespues, 2, "0", STR_PAD_LEFT), "\n";
```

### Misión R01-N02-M2 · La balanza que miente

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un mercader tramposo le muestra a la Capitana estas comparaciones y dice que
todas son "iguales". Para cada par, mostrá con `var_dump` el resultado de `==` y el
de `===` (una línea por par, con los dos resultados):

`100` y `"100"` · `"1e2"` y `"100"` · `"abc"` y `0` · `null` y `false` ·
`"0"` y `false` · `" 1"` y `1`.

Al final, mostrá una línea que diga cuántos pares son **realmente** iguales (con
`===`), contándolos con una variable que sumás en cada comparación verdadera.

#### Criterio de aprobación

- Compara cada par con `==` y con `===`.
- Cuenta con una variable los pares iguales con `===`.
- La salida coincide con la esperada.

#### Salida esperada

```
bool(true)
bool(false)
bool(true)
bool(false)
bool(false)
bool(false)
bool(true)
bool(false)
bool(true)
bool(false)
bool(true)
bool(false)
Pares realmente iguales: 0
```

#### Solución de referencia

```php
<?php
// Mision 2 - La balanza que miente: == convierte, === no.
$iguales = 0;

var_dump(100 == "100", 100 === "100");
$iguales += (int) (100 === "100");
var_dump("1e2" == "100", "1e2" === "100");
$iguales += (int) ("1e2" === "100");
var_dump("abc" == 0, "abc" === 0);
$iguales += (int) ("abc" === 0);
var_dump(null == false, null === false);
$iguales += (int) (null === false);
var_dump("0" == false, "0" === false);
$iguales += (int) ("0" === false);
var_dump(" 1" == 1, " 1" === 1);
$iguales += (int) (" 1" === 1);

echo "Pares realmente iguales: ", $iguales, "\n";
```

### Misión R01-N02-M3 · ¿Puede zarpar?

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un barco puede zarpar si se cumplen **todas** estas reglas:

- el peso de la carga no supera la capacidad;
- tiene capitán (la variable no es `null`);
- y además, o el clima es "bueno", o el barco es "grande".

Con los datos del barco *La Tortuga* (carga 950 kg, capacidad 1000, capitán
`"Bron"`, clima `"tormenta"`, tamaño `"grande"`), mostrá cada regla con
`var_dump` y después una línea final con un **ternario**: `Puede zarpar` o
`Se queda en el muelle`. Mostrá también el nombre del capitán usando `??` con
"sin capitán" por si fuera `null`.

#### Criterio de aprobación

- Usa `&&`, `||` y `!==` (para el `null`).
- La decisión final sale de un ternario.
- La salida coincide con la esperada.

#### Salida esperada

```
bool(true)
bool(true)
bool(true)
Capitán: Bron
Puede zarpar
```

#### Solución de referencia

```php
<?php
// Mision 3 - ¿Puede zarpar?: operadores lógicos, ternario y ??.
$carga = 950;
$capacidad = 1000;
$capitan = "Bron";
$clima = "tormenta";
$tamano = "grande";

$pesoOk = $carga <= $capacidad;
$tieneCapitan = $capitan !== null;
$climaOk = $clima === "bueno" || $tamano === "grande";

var_dump($pesoOk, $tieneCapitan, $climaOk);
echo "Capitán: ", $capitan ?? "sin capitán", "\n";
echo $pesoOk && $tieneCapitan && $climaOk ? "Puede zarpar" : "Se queda en el muelle", "\n";
```

### Encargo R01-N02-E1 · La factura con IVA

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una ferretería del puerto vende 3 martillos de $8500 y 12 cajas de clavos de
$1250. Calculá y mostrá:

- el subtotal;
- el descuento: 10% si el subtotal supera $30000, si no 0 (con un ternario);
- el IVA (21%) sobre el subtotal menos el descuento;
- el total.

Usá una constante para el IVA y `.=` para ir armando un texto `$factura` con
todos los renglones, que mostrás con un solo `echo` al final.

#### Criterio de aprobación

- El IVA es una constante.
- El descuento sale de un ternario.
- La factura se arma con `.=` y se muestra con un solo `echo`.

#### Salida esperada

```
FERRETERÍA EL ANCLA
Subtotal: 40500
Descuento: 4050
IVA 21%: 7654.5
Total: 44104.5
```

#### Solución de referencia

```php
<?php
// Encargo - La factura con IVA: operadores, ternario y .= para armar el texto.
const IVA = 0.21;

$subtotal = 3 * 8500 + 12 * 1250;
$descuento = $subtotal > 30000 ? $subtotal * 0.10 : 0;
$neto = $subtotal - $descuento;
$iva = $neto * IVA;
$total = $neto + $iva;

$factura = "FERRETERÍA EL ANCLA\n";
$factura .= "Subtotal: " . $subtotal . "\n";
$factura .= "Descuento: " . $descuento . "\n";
$factura .= "IVA 21%: " . $iva . "\n";
$factura .= "Total: " . $total . "\n";
echo $factura;
```

### Prueba del sello

#### ¿Cuánto dan `7 / 2`, `intdiv(7, 2)` y `7 % 2`?

`3.5`, `3` y `1`.

#### ¿Qué diferencia hay entre `==` y `===`?

`==` convierte los tipos antes de comparar; `===` compara valor **y** tipo, sin convertir. Se usa siempre `===`.

#### ¿Qué hace `$x ?? "por defecto"`?

Devuelve `$x` si existe y no es `null`; si no, devuelve `"por defecto"`.

#### ¿Cómo se unen dos textos en PHP?

Con el punto: `"Hola " . $nombre`. El `+` solo suma números.

#### ¿Qué devuelve `5 <=> 3`?

`1`, porque 5 es mayor que 3 (devuelve `-1`, `0` o `1`).

### Soluciones (docente)

Sale de `21-PHP/02-Tipos` (la parte de `==` vs `===`) y `03-Control` (el `??`). En la misión 2, `"1e2" == "100"` es `true` (dos textos numéricos se comparan como números) y `"abc" == 0` es `false` desde PHP 8: vale la pena comentarlo en clase como ejemplo de por qué no confiar en `==`.

## R01-N03 · Textos: comillas, funciones y formato

```meta
tipo: tema
padre: R01-N02
precio: 10
criatura: skeleton
temas: prog.cadenas
```

### Crónica

En la oficina de correos del muelle hay una pared entera de casilleros, y un escribiente que pasa el día copiando direcciones: les saca los espacios de más, pone las mayúsculas donde van y arma las etiquetas de cada paquete.

—Casi todo lo que llega al Puerto es **texto** —dice {mentor}, señalando una montaña de sobres—. Nombres, direcciones, mensajes. Hay que saber cortarlo, buscar adentro, limpiarlo y darle formato. Y cuidado con las letras con tilde, {heroe}: ocupan más lugar del que parece.

### Objetivos

- Distinguir comillas simples y dobles, y usar la interpolación de variables.
- Escribir textos largos con *heredoc* y *nowdoc*.
- Usar las funciones de texto más comunes: largo, mayúsculas, buscar, cortar, reemplazar, partir y unir.
- Entender por qué las letras con tilde necesitan las funciones `mb_*`.
- Dar formato con `printf`, `sprintf` y `number_format`.

### Antes de empezar

- Variables y operadores, en especial el punto `.` para unir textos (R01-N02).

### Explicación

#### Comillas simples y dobles
```php
$nombre = "Kira";
echo "Hola, $nombre\n";      // Hola, Kira   → las dobles interpolan variables y \n
echo 'Hola, $nombre\n';      // Hola, $nombre\n   → las simples muestran todo literal
echo "Hola, {$nombre}s\n";   // Hola, Kiras  → las llaves marcan dónde termina la variable
```
Usá comillas **simples** para textos fijos y **dobles** cuando necesites meter
variables o `\n`. Dentro de las llaves se puede poner una posición de un array o
una propiedad: `"Barco: {$barco['nombre']}"`, pero **no** una cuenta: `"{$a + 1}"`
no funciona (calculalo antes en una variable).

#### Textos largos: heredoc y nowdoc
Para varios renglones, en vez de muchos `\n`:
```php
$carta = <<<TXT
    Querida {$nombre}:
    Tu paquete llegó al muelle 3.
    TXT;                       // se comporta como comillas dobles
$plantilla = <<<'TXT'
    Esto se muestra literal: $nombre
    TXT;                       // con comillas simples: como comillas simples
```
La sangría del cierre (`TXT;`) se le quita a todos los renglones.

#### Un texto es una fila de caracteres
Cada carácter tiene una posición, empezando en **0**:
```php
$barco = "Gaviota";
echo $barco[0];      // G
echo $barco[-1];     // a   (las negativas cuentan desde el final)
echo strlen($barco); // 7
```

#### Las funciones más usadas
| Función | Qué hace | Ejemplo → resultado |
|---|---|---|
| `strlen($t)` | largo en **bytes** | `strlen("Kira")` → `4` |
| `strtoupper`, `strtolower` | mayúsculas, minúsculas | `strtoupper("kira")` → `"KIRA"` |
| `ucfirst`, `ucwords` | primera letra, o la de cada palabra | `ucwords("kira valdez")` → `"Kira Valdez"` |
| `trim($t)` | saca espacios y saltos de los extremos | `trim("  hola ")` → `"hola"` |
| `str_contains($t, $x)` | ¿contiene? | `str_contains("Gaviota", "vio")` → `true` |
| `str_starts_with`, `str_ends_with` | ¿empieza / termina con? | `str_ends_with("carta.pdf", ".pdf")` → `true` |
| `strpos($t, $x)` | posición de la primera aparición (o `false`) | `strpos("Kira", "r")` → `2` |
| `substr($t, $desde, $largo)` | un pedazo | `substr("Kira Valdez", 5)` → `"Valdez"` |
| `str_replace($a, $b, $t)` | reemplaza todas las apariciones | `str_replace("a", "4", "Kira")` → `"Kir4"` |
| `explode($sep, $t)` | parte en un array | `explode(",", "a,b,c")` → `["a","b","c"]` |
| `implode($sep, $arr)` | une un array en un texto | `implode(" / ", ["a","b"])` → `"a / b"` |
| `str_repeat($t, $n)` | repite | `str_repeat("=", 5)` → `"====="` |
| `str_pad($t, $n, $c, STR_PAD_LEFT)` | rellena hasta un largo | `str_pad("7", 3, "0", STR_PAD_LEFT)` → `"007"` |
| `strrev($t)` | invierte | `strrev("puerto")` → `"otreup"` |

Ojo con `strpos`: si lo buscado está en la posición 0 devuelve `0`, que es "falso".
Por eso se compara con `!== false`, nunca con `if (strpos(...))`. Para preguntar
si está, mejor `str_contains`.

#### Las letras con tilde: las funciones `mb_*`
Los textos se guardan en **UTF-8**, donde la `ñ` y las vocales con tilde ocupan
**2 bytes**. Las funciones comunes cuentan bytes, no letras:
```php
strlen("ñandú");          // 7  (¡no 5!)
mb_strlen("ñandú");       // 5
strtoupper("ñandú");      // "ñANDú"  (no sabe pasar la ñ ni la ú)
mb_strtoupper("ñandú");   // "ÑANDÚ"
mb_substr("ñandú", 0, 2); // "ña"
```
Regla del Puerto: **con textos que escribe una persona, usá `mb_strlen`,
`mb_substr`, `mb_strtoupper` y `mb_strtolower`**. Hace falta la extensión
`mbstring` (viene en XAMPP; en Linux, `php-mbstring`).

#### Formato: `printf`, `sprintf` y `number_format`
`printf` muestra un texto con **huecos** que se completan con valores;
`sprintf` hace lo mismo pero **devuelve** el texto en lugar de mostrarlo:
```php
printf("%s tiene %d cajones y %.2f kg\n", "Gaviota", 12, 450.5);
$linea = sprintf("%-10s|%5d", "Kira", 42);   // "Kira      |   42"
```
| Hueco | Para | Ejemplo |
|---|---|---|
| `%s` | textos | `"Kira"` |
| `%d` | enteros | `42` |
| `%.2f` | decimales con 2 cifras | `3.14` |
| `%5d` / `%-10s` | ancho mínimo (derecha / izquierda) | `"   42"`, `"Kira      "` |
| `%05d` | rellenar con ceros | `"00042"` |
| `%%` | un signo `%` | `"%"` |

Para plata, **`number_format($n, 2, ',', '.')`** escribe `1.234.567,89`, como en
Argentina (decimales con coma, miles con punto).

Un detalle: el ancho de `%-10s` también se cuenta en **bytes**, así que un nombre
con tilde queda un lugar más corto y la tabla se desalinea. Cuando pase, rellená
con `str_repeat(" ", $ancho - mb_strlen($texto))`.

> **Si venís de otro lenguaje.** En PHP los textos no son objetos: no hay
> `$texto.length()` ni `$texto.upper()`, sino funciones que reciben el texto:
> `strlen($texto)`, `strtoupper($texto)`.

### Código de ejemplo

```php
<?php
/*
 * El escribiente del correo: limpiar, buscar, cortar y dar formato.
 */
$crudo = "   kira VALDEZ   ";
$nombre = ucwords(strtolower(trim($crudo)));
echo "Nombre limpio: [$nombre]\n";
echo "Iniciales: {$nombre[0]}", substr($nombre, strpos($nombre, " ") + 1, 1), "\n";

$direccion = "Muelle 3, casillero 42, Puerto de los Mensajeros";
$partes = explode(", ", $direccion);
echo "Muelle: ", $partes[0], "\n";
echo "Casillero: ", substr($partes[1], strlen("casillero ")), "\n";
echo "¿Es del Puerto? ", str_contains($direccion, "Puerto") ? "sí" : "no", "\n";
echo "Etiqueta: ", implode(" | ", $partes), "\n";

// Letras con tilde
$ave = "ñandú";
echo "strlen: ", strlen($ave), " / mb_strlen: ", mb_strlen($ave), "\n";
echo "Mayúsculas: ", mb_strtoupper($ave), "\n";

// Heredoc
$paquetes = 3;
echo <<<TXT
    Querida {$nombre}:
    Llegaron {$paquetes} paquetes a tu casillero.
    TXT;
echo "\n";

// Formato
printf("%-10s|%6s|%8s\n", "Paquete", "Kilos", "Precio");
printf("%-10s|%6.1f|%8.2f\n", "Cartas", 1.5, 1200);
printf("%-10s|%6.1f|%8.2f\n", "Especias", 12.4, 15999.9);
echo "Seguro: $", number_format(1234567.891, 2, ',', '.'), "\n";
echo "Código: ", sprintf("%05d", 42), "\n";
```

### Salida esperada

```
Nombre limpio: [Kira Valdez]
Iniciales: KV
Muelle: Muelle 3
Casillero: 42
¿Es del Puerto? sí
Etiqueta: Muelle 3 | casillero 42 | Puerto de los Mensajeros
strlen: 7 / mb_strlen: 5
Mayúsculas: ÑANDÚ
Querida Kira Valdez:
Llegaron 3 paquetes a tu casillero.
Paquete   | Kilos|  Precio
Cartas    |   1.5| 1200.00
Especias  |  12.4|15999.90
Seguro: $1.234.567,89
Código: 00042
```

### ¿Para qué sirve?

Cada formulario de la web devuelve textos: nombres con espacios de más, mails en mayúsculas, apellidos con tilde. Limpiarlos (`trim`, `mb_strtolower`), validarlos (`str_contains`, `strlen`) y mostrarlos bien formateados (`number_format`, `sprintf`) es trabajo de todos los días en cualquier sistema PHP.

### Errores habituales

**Ogro: `strpos` en un `if`.** `if (strpos($mail, "@"))` falla justo cuando el `@`
está en la posición 0 (porque `0` es falso). Usá `str_contains($mail, "@")` o
`strpos(...) !== false`.

**Ogro: `strlen` con tildes.** `strlen("José")` da `5`. Para contar letras,
`mb_strlen`.

**Esqueleto: la variable pegada al texto.** `"$barcos"` busca la variable
`$barcos`; si querías `$barco` seguido de una `s`, escribí `"{$barco}s"`.

**Esqueleto: la variable pegada a un símbolo.** En `"Peso: «$texto»"`, PHP toma la
`»` como parte del nombre (los nombres de variables admiten letras con tilde y
otros caracteres), busca `$texto»` y avisa `Undefined variable $texto»`. Con llaves
no hay duda: `"«{$texto}»"`.

**Orco: una posición que no existe.** `"Kira"[10]` da
`Warning: Uninitialized string offset 10`. Revisá el largo antes.

**Slime: el cierre del heredoc.** El `TXT;` de cierre tiene que estar solo en su
renglón (con sangría o sin ella, pero sin texto antes).

### Misión R01-N03-M1 · La etiqueta del paquete

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Llegó un paquete con los datos escritos a las apuradas:
`"  bron   de las FORJAS  "` (remitente) y `"  lía del valle  "` (destinataria).
Armá la etiqueta:

1. Limpiá los espacios de los extremos con `trim`.
2. Pasá cada nombre a "Tipo Título" con `ucwords(mb_strtolower(...))`.
3. Reemplazá los espacios dobles por uno solo (con `str_replace`, dos veces).
4. Mostrá la etiqueta con un recuadro de `*` tan ancho como el texto más largo
   más 4 (usá `mb_strlen` y `str_repeat`).

#### Criterio de aprobación

- Usa `trim`, `mb_strtolower`, `ucwords`, `str_replace`, `mb_strlen` y `str_repeat`.
- El ancho del recuadro se calcula, no se escribe a mano.
- La salida coincide con la esperada.

#### Salida esperada

```
**************************
* De: Bron De Las Forjas *
* Para: Lía Del Valle    *
**************************
```

#### Solución de referencia

```php
<?php
// Mision 1 - La etiqueta del paquete: limpiar textos y armar un recuadro.
$remitente = "  bron   de las FORJAS  ";
$destino = "  lía del valle  ";

$remitente = ucwords(mb_strtolower(trim($remitente)));
$remitente = str_replace("  ", " ", $remitente);
$remitente = str_replace("  ", " ", $remitente);
$destino = ucwords(mb_strtolower(trim($destino)));

$de = "De: $remitente";
$para = "Para: $destino";
$ancho = max(mb_strlen($de), mb_strlen($para)) + 4;

echo str_repeat("*", $ancho), "\n";
echo "* ", $de, str_repeat(" ", $ancho - mb_strlen($de) - 4), " *\n";
echo "* ", $para, str_repeat(" ", $ancho - mb_strlen($para) - 4), " *\n";
echo str_repeat("*", $ancho), "\n";
```

### Misión R01-N03-M2 · El mail del cliente

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La oficina de correos recibe la dirección de mail `"  Kira.Valdez@Puerto.COM.ar "`.
Mostrá:

1. El mail limpio y en minúsculas.
2. El usuario (lo que está antes del `@`) y el dominio (lo que está después),
   con `strpos` y `substr` (o con `explode`).
3. Si el dominio termina en `.ar` (con `str_ends_with`).
4. El mail "oculto" para mostrar en pantalla: la primera letra del usuario,
   asteriscos por el resto de las letras del usuario, y el dominio completo
   (`k**********@puerto.com.ar`).

#### Criterio de aprobación

- Usa `trim` y `strtolower`, y encuentra el `@` con `strpos` o `explode`.
- Los asteriscos se calculan con `str_repeat` y el largo del usuario.
- La salida coincide con la esperada.

#### Salida esperada

```
Mail: kira.valdez@puerto.com.ar
Usuario: kira.valdez
Dominio: puerto.com.ar
¿Es de Argentina? sí
Oculto: k**********@puerto.com.ar
```

#### Solución de referencia

```php
<?php
// Mision 2 - El mail del cliente: buscar y cortar textos.
$mail = strtolower(trim("  Kira.Valdez@Puerto.COM.ar "));
$arroba = strpos($mail, "@");
$usuario = substr($mail, 0, $arroba);
$dominio = substr($mail, $arroba + 1);

echo "Mail: $mail\n";
echo "Usuario: $usuario\n";
echo "Dominio: $dominio\n";
echo "¿Es de Argentina? ", str_ends_with($dominio, ".ar") ? "sí" : "no", "\n";
echo "Oculto: ", $usuario[0], str_repeat("*", strlen($usuario) - 1), "@", $dominio, "\n";
```

### Misión R01-N03-M3 · La tabla de tarifas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Mostrá la tabla de tarifas del correo con `printf`: una columna de destino (10
caracteres, a la izquierda), una de peso máximo en kilos (6 caracteres, a la
derecha, un decimal) y una de precio (10 caracteres, a la derecha, dos
decimales). Los destinos son *Valle* (2.5 kg, 1800), *Forjas* (10 kg, 5250.5) e
*Imperio* (25 kg, 12999.99). Poné un título, un renglón de guiones y, al final,
el precio más caro escrito con `number_format` a la argentina.

#### Criterio de aprobación

- Usa `printf` con anchos (`%-10s`, `%6.1f`, `%10.2f`).
- El precio final usa `number_format` con coma decimal.
- La salida coincide con la esperada.

#### Salida esperada

```
Destino       Kg    Precio
--------------------------
Valle        2.5   1800.00
Forjas      10.0   5250.50
Imperio     25.0  12999.99
El envío más caro: $12.999,99
```

#### Solución de referencia

```php
<?php
// Mision 3 - La tabla de tarifas: printf con anchos y number_format.
printf("%-10s%6s%10s\n", "Destino", "Kg", "Precio");
echo str_repeat("-", 26), "\n";
printf("%-10s%6.1f%10.2f\n", "Valle", 2.5, 1800);
printf("%-10s%6.1f%10.2f\n", "Forjas", 10, 5250.5);
printf("%-10s%6.1f%10.2f\n", "Imperio", 25, 12999.99);
echo "El envío más caro: $", number_format(12999.99, 2, ',', '.'), "\n";
```

### Encargo R01-N03-E1 · La carta con plantilla

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una inmobiliaria del puerto manda la misma carta a muchos inquilinos. Con
variables para el nombre (`"Ana Pérez"`), el departamento (`"3B"`), el mes
(`"octubre"`) y el monto (`185000`), armá la carta con un **heredoc**:

- el saludo con el nombre;
- un párrafo que diga el departamento, el mes y el monto con `number_format` (el
  monto formateado guardalo antes en una variable, porque no se puede llamar a una
  función adentro del heredoc);
- una firma.

Después mostrá un renglón con la cantidad de **letras** del nombre (con
`mb_strlen`, sin contar el espacio: usá `str_replace`).

#### Criterio de aprobación

- La carta sale de un heredoc con variables interpoladas.
- El monto se formatea con `number_format` antes del heredoc.
- Cuenta las letras con `mb_strlen`.

#### Salida esperada

```
Estimada Ana Pérez:

Le recordamos que el alquiler del departamento 3B
correspondiente a octubre es de $185.000,00.

Saludos cordiales,
Inmobiliaria El Faro
Letras del nombre: 8
```

#### Solución de referencia

```php
<?php
// Encargo - La carta con plantilla: heredoc, number_format y mb_strlen.
$nombre = "Ana Pérez";
$depto = "3B";
$mes = "octubre";
$monto = number_format(185000, 2, ',', '.');

echo <<<CARTA
    Estimada {$nombre}:

    Le recordamos que el alquiler del departamento {$depto}
    correspondiente a {$mes} es de \${$monto}.

    Saludos cordiales,
    Inmobiliaria El Faro
    CARTA;
echo "\n";
echo "Letras del nombre: ", mb_strlen(str_replace(" ", "", $nombre)), "\n";
```

### Prueba del sello

#### ¿Qué muestra `echo 'Hola $nombre';`?

Muestra literalmente `Hola $nombre`: las comillas simples no interpolan variables.

#### ¿Por qué `strlen("ñandú")` da 7?

Porque cuenta bytes, y en UTF-8 la `ñ` y la `ú` ocupan 2 bytes cada una. Para contar letras se usa `mb_strlen`.

#### ¿Qué devuelve `explode(",", "a,b,c")`?

Un array con tres textos: `["a", "b", "c"]`.

#### ¿Qué diferencia hay entre `printf` y `sprintf`?

`printf` muestra el texto formateado; `sprintf` lo devuelve para guardarlo en una variable.

#### ¿Por qué `if (strpos($t, "x"))` es peligroso?

Porque si `"x"` está en la posición 0, `strpos` devuelve `0`, que se evalúa como falso. Hay que comparar con `!== false` o usar `str_contains`.

### Soluciones (docente)

Sale de `21-PHP/07-Strings`, ampliado con la tabla de funciones y las `mb_*` (clave en castellano). `mb_str_pad` no se usa porque es de PHP 8.3 y XAMPP trae 8.2. En la misión 2, el ocultado usa `strlen` porque el usuario del mail no tiene tildes; vale la pena preguntar qué pasaría si las tuviera.

## R01-N04 · Entrada por teclado y argumentos

```meta
tipo: tema
padre: R01-N03
precio: 10
criatura: goblin
temas: prog.entrada, prog.argumentos, err.validacion
```

### Crónica

En la ventanilla de encomiendas, un empleado le pregunta a cada cliente su nombre, el peso del paquete y el destino, y anota las respuestas en una planilla. Uno contesta "doce kilos" en vez de "12"; el empleado frunce el ceño y le pide que lo escriba de nuevo.

—Un programa que solo muestra cosas es como una ventanilla sin empleado —dice {mentor}—. Hay que **preguntar**. Pero lo que la gente contesta nunca es confiable, {heroe}: siempre llega como texto, a veces vacío, a veces con letras donde iban números. Se revisa antes de usar.

### Objetivos

- Leer renglones del teclado con `fgets(STDIN)` y limpiarlos con `trim`.
- Convertir lo leído a número y validarlo con `is_numeric` y `filter_var`.
- Leer varios datos de un mismo renglón con `explode`.
- Recibir argumentos desde la línea de comandos con `$argv` y `$argc`.
- Terminar el programa con un código de salida con `exit`.

### Antes de empezar

- Textos: `trim`, `explode` y `printf` (R01-N03).

### Explicación

#### Leer un renglón
En la terminal, PHP lee del teclado con **`fgets(STDIN)`**: espera a que la
persona escriba algo y apriete Enter, y devuelve ese renglón **como texto, con el
salto de línea incluido**:
```php
echo "¿Cómo te llamás? ";
$nombre = trim(fgets(STDIN));   // trim saca el "\n" del final (y los espacios)
echo "Hola, $nombre\n";
```
**Siempre `trim`**: sin él, `$nombre` vale `"Kira\n"` y el salto de línea aparece
donde no querés.

Si no hay nada más para leer (se terminó la entrada), `fgets` devuelve `false`.

> Algunas instalaciones tienen también `readline("¿Nombre? ")`, que es más
> cómoda, pero no siempre viene (en Windows muchas veces falta). `fgets(STDIN)`
> anda en todos lados.

#### De texto a número
Todo lo leído es texto. Para hacer cuentas, se convierte:
```php
echo "Peso del paquete (kg): ";
$peso = (float) trim(fgets(STDIN));
echo "Cajones: ";
$cajones = (int) trim(fgets(STDIN));
```
El problema: `(int) "doce"` da `0` sin quejarse, y `(int) "12abc"` da `12`. Para
**validar** antes de convertir:
```php
$texto = trim(fgets(STDIN));
if (is_numeric($texto)) {          // "12", "12.5", "-3", "1e3"
    $peso = (float) $texto;
}
$n = filter_var($texto, FILTER_VALIDATE_INT);   // int, o false si no es un entero válido
```
| `filter_var(…, FILTER_VALIDATE_INT)` con | Devuelve |
|---|---|
| `"42"` | `42` |
| `" 42 "` | `42` (ignora los espacios) |
| `"4.2"` | `false` |
| `"abc"` | `false` |

`FILTER_VALIDATE_FLOAT` hace lo mismo con decimales (pero con **punto**: `"3,5"`
da `false`). Y se le puede pedir un rango:
```php
$nota = filter_var($texto, FILTER_VALIDATE_INT, ['options' => ['min_range' => 1, 'max_range' => 10]]);
```
Esto de validar todo lo que llega vas a usarlo en cada formulario web.

#### Varios datos en un renglón
Si la persona escribe `12 37.5 Valle` en un solo renglón, se parte con `explode`:
```php
[$cajones, $kilos, $destino] = explode(" ", trim(fgets(STDIN)));
```
Esa forma de asignar a varias variables juntas se llama **desestructuración** (la
vas a ver mejor en arrays).

#### Argumentos de la línea de comandos
También se le pueden pasar datos al programa al ejecutarlo:
```bash
php etiqueta.php Kira 12
```
PHP los guarda en el array **`$argv`** (y la cantidad en **`$argc`**):
| Expresión | Vale |
|---|---|
| `$argv[0]` | `"etiqueta.php"` (el nombre del programa) |
| `$argv[1]` | `"Kira"` |
| `$argv[2]` | `"12"` (¡texto!) |
| `$argc` | `3` |

```php
$nombre = $argv[1] ?? "desconocido";   // ?? por si no lo pasaron
```

#### Probar con la entrada en un archivo
Escribir los mismos datos cada vez que probás cansa. Guardalos en un archivo
`entrada.txt` (un dato por renglón) y **redirigí** la entrada:
```bash
php ventanilla.php < entrada.txt
```
El programa lee de ese archivo como si alguien tipeara. Así se prueban las
misiones: por eso en las **salidas esperadas** no aparece lo que se escribe, y las
preguntas quedan todas en el mismo renglón (`Nombre: Peso: …`).

#### Terminar antes: `exit`
`exit("mensaje")` muestra el mensaje y corta el programa. `exit(1)` corta con un
**código de salida** distinto de 0, que en la terminal significa "terminó con
error" (0 es "todo bien"):
```php
if ($argc < 2) {
    echo "Uso: php etiqueta.php NOMBRE\n";
    exit(1);
}
```

### Código de ejemplo

```php
<?php
/*
 * La ventanilla de encomiendas: leer datos, validarlos y calcular.
 */
echo "Nombre del cliente: ";
$cliente = trim(fgets(STDIN));

echo "Peso del paquete (kg): ";
$textoPeso = trim(fgets(STDIN));
if (!is_numeric($textoPeso)) {
    echo "\n«{$textoPeso}» no es un número. Probá de nuevo.\n";
    exit(1);
}
$peso = (float) $textoPeso;

echo "Cantidad de paquetes: ";
$cantidad = filter_var(trim(fgets(STDIN)), FILTER_VALIDATE_INT, ['options' => ['min_range' => 1]]);
if ($cantidad === false) {
    echo "\nLa cantidad tiene que ser un entero mayor que 0.\n";
    exit(1);
}

echo "Destino y prioridad (ej.: Valle urgente): ";
[$destino, $prioridad] = explode(" ", trim(fgets(STDIN)));

$precio = $peso * $cantidad * 350;
if ($prioridad === "urgente") {
    $precio *= 1.5;
}

echo "\n";
echo "Cliente: ", ucwords($cliente), "\n";
printf("%d paquete(s) de %.1f kg a %s (%s)\n", $cantidad, $peso, $destino, $prioridad);
echo "Precio: $", number_format($precio, 2, ',', '.'), "\n";
```

### Entrada de ejemplo

```
kira valdez
2.5
3
Valle urgente
```

### Salida esperada

```
Nombre del cliente: Peso del paquete (kg): Cantidad de paquetes: Destino y prioridad (ej.: Valle urgente): 
Cliente: Kira Valdez
3 paquete(s) de 2.5 kg a Valle (urgente)
Precio: $3.937,50
```

### ¿Para qué sirve?

Leer datos, validarlos y recién después usarlos es **exactamente** lo que hace un formulario web, solo que en lugar de `fgets` los datos llegan en `$_POST`. Además, muchos programas de PHP corren en la terminal: tareas programadas, importadores de planillas, scripts de mantenimiento. Todos reciben argumentos con `$argv`.

### Errores habituales

**Ogro: olvidarse el `trim`.** Sin `trim`, `$nombre` termina en `"\n"` y
`"Hola, $nombre!"` muestra el `!` en el renglón de abajo. Además
`$respuesta === "si"` da falso porque en realidad vale `"si\n"`.

**Goblin: convertir sin validar.** `(int) "doce"` da `0` y el programa sigue como si
nada, con un peso de cero kilos. Validá con `is_numeric` o `filter_var`.

**Goblin: la coma decimal.** Una persona escribe `2,5`, pero `is_numeric("2,5")` es
`false` y `(float) "2,5"` da `2`. Si querés aceptar coma, reemplazala:
`str_replace(",", ".", $texto)`.

**Orco: el argumento que no vino.** `$argv[1]` cuando no pasaste argumentos da
`Warning: Undefined array key 1`. Usá `$argv[1] ?? "valor"` o revisá `$argc`.

**Orco: `explode` con menos partes.** Si la persona escribe solo `Valle`,
`[$destino, $prioridad] = explode(...)` da `Undefined array key 1`. Revisá con
`count()` cuántas partes vinieron.

### Misión R01-N04-M1 · El saludo del portero

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El portero del Puerto pregunta el nombre y la ciudad de cada visitante y lo
saluda. Leé los dos datos (limpiando espacios), y mostrá:

- `Bienvenida, NOMBRE de CIUDAD.` con el nombre en "Tipo Título";
- la cantidad de letras del nombre (con `mb_strlen`);
- el nombre al revés en mayúsculas (sin tildes en el ejemplo, así que `strrev` y
  `strtoupper` alcanzan).

#### Criterio de aprobación

- Lee con `fgets(STDIN)` y limpia con `trim`.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
   bron  
las Forjas
```

#### Salida esperada

```
Nombre: Ciudad: 
Bienvenida, Bron de las Forjas.
Tu nombre tiene 4 letras.
Al revés: NORB
```

#### Solución de referencia

```php
<?php
// Mision 1 - El saludo del portero: leer y limpiar textos.
echo "Nombre: ";
$nombre = ucwords(strtolower(trim(fgets(STDIN))));
echo "Ciudad: ";
$ciudad = trim(fgets(STDIN));

echo "\n";
echo "Bienvenida, $nombre de $ciudad.\n";
echo "Tu nombre tiene ", mb_strlen($nombre), " letras.\n";
echo "Al revés: ", strtoupper(strrev($nombre)), "\n";
```

### Misión R01-N04-M2 · La balanza de la aduana

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La balanza de la aduana pide el peso de **tres** paquetes, uno por renglón. Cada
peso puede venir con coma o con punto (`2,5` o `2.5`). Para cada uno:

- reemplazá la coma por punto;
- si no es un número (`is_numeric`), mostrá `Peso inválido: «TEXTO»` y contalo como 0;
- si es válido, sumalo.

Al final, mostrá el total con un decimal y cuántos pesos fueron inválidos.

#### Criterio de aprobación

- Acepta coma y punto.
- Los pesos inválidos se informan y no rompen el programa.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
2,5
doce
7.25
```

#### Salida esperada

```
Peso 1: Peso 2: Peso inválido: «doce»
Peso 3: 
Total: 9.8 kg (1 inválido/s)
```

#### Solución de referencia

```php
<?php
// Mision 2 - La balanza de la aduana: validar números con coma o punto.
$total = 0;
$invalidos = 0;

echo "Peso 1: ";
$texto = str_replace(",", ".", trim(fgets(STDIN)));
if (is_numeric($texto)) {
    $total += (float) $texto;
} else {
    echo "Peso inválido: «{$texto}»\n";
    $invalidos++;
}

echo "Peso 2: ";
$texto = str_replace(",", ".", trim(fgets(STDIN)));
if (is_numeric($texto)) {
    $total += (float) $texto;
} else {
    echo "Peso inválido: «{$texto}»\n";
    $invalidos++;
}

echo "Peso 3: ";
$texto = str_replace(",", ".", trim(fgets(STDIN)));
if (is_numeric($texto)) {
    $total += (float) $texto;
} else {
    echo "Peso inválido: «{$texto}»\n";
    $invalidos++;
}

printf("\nTotal: %.1f kg (%d inválido/s)\n", $total, $invalidos);
```

### Misión R01-N04-M3 · La etiqueta por argumentos

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `etiqueta.php`, que se ejecuta así:
```bash
php etiqueta.php Kira Valle 3
```
y recibe por argumentos el **destinatario**, el **destino** y la **cantidad de
paquetes** (opcional: si no se pasa, vale 1). Si faltan el destinatario o el
destino, mostrá `Uso: php etiqueta.php DESTINATARIO DESTINO [CANTIDAD]` y terminá
con `exit(1)`. Si la cantidad no es un entero válido mayor que 0 (usá
`filter_var` con `min_range`), mostrá `La cantidad tiene que ser un entero mayor
que 0.` y terminá con `exit(1)`.

Con los datos válidos, imprimí una etiqueta por paquete: `[1/3] Para: Kira — Valle`.

Para probar tu programa **sin** escribir los argumentos cada vez, la solución de
referencia arranca con una línea que simula los argumentos del ejemplo; en tu
entrega podés dejarla o sacarla.

#### Criterio de aprobación

- Usa `$argv` y `$argc` (o `??`) para los argumentos.
- Valida la cantidad con `filter_var` y sale con `exit(1)` si algo falta.
- Para los argumentos `Kira Valle 3`, la salida coincide con la esperada.

#### Salida esperada

```
[1/3] Para: Kira — Valle
[2/3] Para: Kira — Valle
[3/3] Para: Kira — Valle
```

#### Solución de referencia

```php
<?php
// Mision 3 - La etiqueta por argumentos: $argv, $argc, filter_var y exit.
// Para probar sin escribir los argumentos: se simulan si no vino ninguno.
if ($argc === 1) {
    $argv = ["etiqueta.php", "Kira", "Valle", "3"];
    $argc = count($argv);
}

if ($argc < 3) {
    echo "Uso: php etiqueta.php DESTINATARIO DESTINO [CANTIDAD]\n";
    exit(1);
}

$destinatario = $argv[1];
$destino = $argv[2];
$cantidad = filter_var($argv[3] ?? "1", FILTER_VALIDATE_INT, ['options' => ['min_range' => 1]]);
if ($cantidad === false) {
    echo "La cantidad tiene que ser un entero mayor que 0.\n";
    exit(1);
}

for ($i = 1; $i <= $cantidad; $i++) {
    echo "[$i/$cantidad] Para: $destinatario — $destino\n";
}
```

### Encargo R01-N04-E1 · El presupuesto de la pintura

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una pinturería le pide a sus clientes el **ancho** y el **alto** de la pared (en
metros, en un mismo renglón separados por espacio, con punto o coma) y la
**cantidad de manos**. Con esos datos:

- calculá los metros cuadrados (ancho × alto × manos);
- un litro de pintura cubre 10 m²: calculá los litros necesarios redondeando
  **hacia arriba** con `ceil`;
- las latas son de 4 litros: calculá cuántas latas comprar (también con `ceil`);
- cada lata cuesta $38500: mostrá el total con `number_format`.

Si el ancho o el alto no son números, mostrá un mensaje y terminá con `exit(1)`.

#### Criterio de aprobación

- Lee dos datos de un renglón con `explode` y acepta coma decimal.
- Usa `ceil` para litros y latas.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
4,5 2.6
2
```

#### Salida esperada

```
Ancho y alto (m): Manos: 
Superficie a pintar: 23.40 m²
Litros: 3
Latas de 4 l: 1
Total: $38.500,00
```

#### Solución de referencia

```php
<?php
// Encargo - El presupuesto de la pintura: leer, validar, ceil y number_format.
const COBERTURA = 10;     // m² por litro
const LITROS_LATA = 4;
const PRECIO_LATA = 38500;

echo "Ancho y alto (m): ";
$partes = explode(" ", str_replace(",", ".", trim(fgets(STDIN))));
if (count($partes) !== 2 || !is_numeric($partes[0]) || !is_numeric($partes[1])) {
    echo "\nHay que escribir dos números, por ejemplo: 4.5 2.6\n";
    exit(1);
}
[$ancho, $alto] = $partes;

echo "Manos: ";
$manos = (int) trim(fgets(STDIN));

$metros = $ancho * $alto * $manos;
$litros = ceil($metros / COBERTURA);
$latas = ceil($litros / LITROS_LATA);

echo "\n";
printf("Superficie a pintar: %.2f m²\n", $metros);
echo "Litros: $litros\n";
echo "Latas de ", LITROS_LATA, " l: $latas\n";
echo "Total: $", number_format($latas * PRECIO_LATA, 2, ',', '.'), "\n";
```

### Prueba del sello

#### ¿Por qué hay que usar `trim` después de `fgets(STDIN)`?

Porque `fgets` devuelve el renglón con el salto de línea del Enter al final (`"Kira\n"`); `trim` lo saca junto con los espacios.

#### ¿Qué devuelve `filter_var("4.2", FILTER_VALIDATE_INT)`?

`false`, porque `"4.2"` no es un entero válido.

#### ¿Qué hay en `$argv[0]`?

El nombre del programa que se ejecutó (por ejemplo, `"etiqueta.php"`). Los argumentos empiezan en `$argv[1]`.

#### ¿Qué significa `exit(1)`?

Termina el programa con código de salida 1, que para la terminal significa "terminó con error" (0 es "todo bien").

#### ¿Qué da `(int) "doce"` y por qué es peligroso?

Da `0` sin avisar: el programa sigue con un dato equivocado. Por eso se valida antes con `is_numeric` o `filter_var`.

### Soluciones (docente)

Nodo nuevo: el capítulo original no tenía entrada por teclado (usaba datos fijos). Se usa `fgets(STDIN)` porque `readline` no siempre está (falta en muchas instalaciones de Windows). La misión 3 simula `$argv` cuando no hay argumentos para que se pueda probar igual; conviene mostrar en clase cómo se ejecuta con argumentos reales y qué muestra `echo $?` (Linux) o `echo %ERRORLEVEL%` (Windows) después de un `exit(1)`.

## R01-N05 · Decisiones: if, switch y match

```meta
tipo: tema
padre: R01-N04
precio: 10
criatura: ogre
temas: prog.condicionales
```

### Crónica

En el cruce de los tres muelles hay un guardia con un farol. A cada carro que llega le mira la carga y le señala un camino: los de pescado, a la izquierda; los de madera, al frente; los que traen cartas, directo a la torre. Si trae algo raro, lo manda a revisar.

—Un programa también tiene que **elegir caminos** —dice {mentor}—. Según lo que llega, hace una cosa u otra. PHP tiene tres herramientas para eso, {heroe}, y una de ellas compara con trampa. Te voy a mostrar cuál.

### Objetivos

- Tomar decisiones con `if`, `elseif` y `else`.
- Anidar y combinar condiciones con `&&` y `||`.
- Elegir entre muchos casos con `switch` y entender su comparación suelta.
- Usar `match`, la forma moderna y estricta de elegir un valor.
- Validar datos de entrada antes de usarlos ("cláusulas de guarda").

### Antes de empezar

- Operadores de comparación y lógicos (R01-N02) y leer del teclado (R01-N04).

### Explicación

#### `if`, `elseif` y `else`
```php
if ($peso > 1000) {
    echo "Va a la bodega grande\n";
} elseif ($peso > 100) {
    echo "Va a la bodega chica\n";
} else {
    echo "Va como encomienda\n";
}
```
PHP evalúa de arriba abajo y entra **solo en el primer bloque** cuya condición sea
verdadera. El `else` es opcional. Las llaves se pueden omitir si el bloque tiene
una sola línea, pero en el Puerto **siempre se ponen**: evita errores cuando
alguien agrega una segunda línea.

#### Condiciones compuestas
```php
if ($edad >= 18 && $tienePasaje) { … }
if ($clima === "tormenta" || $olas > 3) { … }
if (!$autorizado) { … }
```

#### Cláusulas de guarda
En lugar de anidar muchos `if`, se descartan primero los casos malos:
```php
if ($peso <= 0) {
    echo "Peso inválido\n";
    exit(1);
}
if ($destino === "") {
    echo "Falta el destino\n";
    exit(1);
}
// acá los datos ya son válidos: el resto del programa queda sin sangrías
```

#### `switch`: muchos casos de un mismo valor
```php
switch ($muelle) {
    case 1:
        echo "Pescado\n";
        break;
    case 2:
    case 3:                 // 2 y 3 comparten el mismo código
        echo "Madera\n";
        break;
    default:
        echo "A revisar\n";
}
```
Dos trampas del `switch`:
1. **El `break`**: sin él, la ejecución "se cae" al caso siguiente y ejecuta
   también ese código.
2. **Compara con `==`**: `switch ("1")` entra en `case 1:` (texto contra
   número). Es el **ogro** escondido.

#### `match`: la forma moderna
Desde PHP 8, `match` elige un **valor** según otro, comparando con `===`:
```php
$bodega = match ($muelle) {
    1 => "Pescado",
    2, 3 => "Madera",
    default => "A revisar",
};
```
Diferencias con `switch`:
| | `switch` | `match` |
|---|---|---|
| compara con | `==` (suelto) | `===` (estricto) |
| devuelve un valor | no | sí |
| hace falta `break` | sí | no |
| sin caso que coincida | no pasa nada | error `UnhandledMatchError` |

Con `match (true)` se pueden poner condiciones en cada rama:
```php
$tarifa = match (true) {
    $peso > 1000 => "carga pesada",
    $peso > 100  => "carga",
    default      => "encomienda",
};
```
**En el Puerto se prefiere `match`**: es más corto y no compara con trampa.

#### El ternario, para lo chico
Para elegir entre dos valores en una línea, el ternario del nodo anterior:
```php
$texto = $cantidad === 1 ? "paquete" : "paquetes";
```

### Código de ejemplo

```php
<?php
/*
 * El guardia del cruce: if, switch y match.
 */
echo "Carga (pescado, madera, cartas, otra): ";
$carga = strtolower(trim(fgets(STDIN)));
echo "Peso (kg): ";
$peso = (float) trim(fgets(STDIN));
echo "\n";

// Cláusula de guarda
if ($peso <= 0) {
    echo "Un carro vacío no pasa.\n";
    exit(1);
}

// if / elseif / else
if ($peso > 1000) {
    $bodega = "grande";
} elseif ($peso > 100) {
    $bodega = "chica";
} else {
    $bodega = "de encomiendas";
}
echo "Bodega: $bodega\n";

// switch (compara con ==)
switch ($carga) {
    case "pescado":
        echo "Camino: muelle 1, a la izquierda\n";
        break;
    case "madera":
        echo "Camino: muelle 2, al frente\n";
        break;
    case "cartas":
        echo "Camino: directo a la torre\n";
        break;
    default:
        echo "Camino: a revisión\n";
}

// match (compara con === y devuelve un valor)
$impuesto = match ($carga) {
    "pescado" => 0.05,
    "madera" => 0.10,
    "cartas" => 0.0,
    default => 0.20,
};
printf("Impuesto: %.0f%% → $%s\n", $impuesto * 100, number_format($peso * 90 * $impuesto, 2, ',', '.'));

$prioridad = match (true) {
    $carga === "cartas" => "alta",
    $peso > 500 => "media",
    default => "baja",
};
echo "Prioridad: $prioridad\n";

// La trampa del switch: "1" entra en case 1
$muelle = "1";
switch ($muelle) {
    case 1:
        echo "switch: \"1\" entró en case 1\n";
        break;
}
try {
    echo match ($muelle) { 1 => "match: entró\n" };
} catch (\UnhandledMatchError $e) {
    echo "match: \"1\" no es 1 → ", $e->getMessage(), "\n";
}
```

### Entrada de ejemplo

```
Madera
640
```

### Salida esperada

```
Carga (pescado, madera, cartas, otra): Peso (kg): 
Bodega: chica
Camino: muelle 2, al frente
Impuesto: 10% → $5.760,00
Prioridad: media
switch: "1" entró en case 1
match: "1" no es 1 → Unhandled match case of type string
```

### ¿Para qué sirve?

Cada página de un sistema decide: si el usuario inició sesión, qué mostrarle; si el formulario tiene errores, volver a mostrarlo; según el rol, qué botones aparecen; según el método de pago, qué recargo aplicar. `match` hace esas decisiones cortas y seguras.

### Errores habituales

**Ogro: `=` en el `if`.** `if ($rol = "admin")` asigna y siempre entra. Para
comparar, `===`.

**Ogro: el `break` olvidado.** Sin `break`, el `switch` ejecuta también el caso de
abajo: el carro de pescado sale por el muelle 1 **y** por el 2.

**Ogro: el `switch` compara suelto.** `switch ("1")` entra en `case 1:` y `switch
(0)` podía entrar en `case "a":` en PHP 7. Con `match` no pasa.

**Goblin: `match` sin `default`.** Si ningún caso coincide:
```
PHP Fatal error:  Uncaught UnhandledMatchError: Unhandled match case of type string
```
Agregá un `default` o validá antes.

**Slime: el `;` después del `match`.** `match` es una expresión: cuando la asignás,
termina con `};`, a diferencia del `switch`.

### Misión R01-N05-M1 · La tarifa del ferry

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El ferry del Puerto cobra según la **edad** del pasajero:

- menores de 3 años: gratis;
- de 3 a 12: $2500;
- de 13 a 64: $5000;
- 65 o más: $2500.

Además, los **estudiantes** (se pregunta `si` o `no`) tienen 20% de descuento sobre
esa tarifa. Leé la edad y si es estudiante, validá que la edad sea un entero entre
0 y 120 (si no, mostrá `Edad inválida.` y terminá), y mostrá la categoría y el
precio final.

#### Criterio de aprobación

- Usa `if`/`elseif`/`else` o `match (true)` para la tarifa.
- Valida la edad con una cláusula de guarda.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
15
si
```

#### Salida esperada

```
Edad: ¿Estudiante? (si/no): 
Categoría: adulto (estudiante)
Pasaje: $4.000,00
```

#### Solución de referencia

```php
<?php
// Mision 1 - La tarifa del ferry: decisiones por rangos y una guarda.
echo "Edad: ";
$edad = filter_var(trim(fgets(STDIN)), FILTER_VALIDATE_INT, ['options' => ['min_range' => 0, 'max_range' => 120]]);
echo "¿Estudiante? (si/no): ";
$estudiante = strtolower(trim(fgets(STDIN))) === "si";
echo "\n";

if ($edad === false) {
    echo "Edad inválida.\n";
    exit(1);
}

if ($edad < 3) {
    $categoria = "bebé";
    $tarifa = 0;
} elseif ($edad <= 12) {
    $categoria = "niño";
    $tarifa = 2500;
} elseif ($edad <= 64) {
    $categoria = "adulto";
    $tarifa = 5000;
} else {
    $categoria = "jubilado";
    $tarifa = 2500;
}

if ($estudiante) {
    $tarifa *= 0.8;
}

echo "Categoría: $categoria", $estudiante ? " (estudiante)" : "", "\n";
echo "Pasaje: $", number_format($tarifa, 2, ',', '.'), "\n";
```

### Misión R01-N05-M2 · El semáforo del muelle

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El semáforo del muelle muestra un color y el capitán tiene que saber qué hacer.
Leé un color y, con **`match`**, mostrá la acción:

- `verde` → `Avanzar`
- `amarillo` → `Reducir la velocidad`
- `rojo` → `Detenerse`
- `azul` o `violeta` (luces de servicio) → `Ceder el paso a la guardia`
- cualquier otro → `Semáforo roto: llamar al capitán del puerto`

Aceptá el color con mayúsculas o espacios de más. Después, con un segundo
`match (true)`, mostrá la velocidad máxima según la acción: 20 si avanza, 5 si
reduce, 0 en cualquier otro caso.

#### Criterio de aprobación

- Usa `match` con varios valores en una rama (`"azul", "violeta" =>`).
- Tiene un `default`.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
  AMARILLO
```

#### Salida esperada

```
Color: 
Acción: Reducir la velocidad
Velocidad máxima: 5 nudos
```

#### Solución de referencia

```php
<?php
// Mision 2 - El semáforo del muelle: match con varios valores y match(true).
echo "Color: ";
$color = strtolower(trim(fgets(STDIN)));
echo "\n";

$accion = match ($color) {
    "verde" => "Avanzar",
    "amarillo" => "Reducir la velocidad",
    "rojo" => "Detenerse",
    "azul", "violeta" => "Ceder el paso a la guardia",
    default => "Semáforo roto: llamar al capitán del puerto",
};

$velocidad = match (true) {
    $accion === "Avanzar" => 20,
    $accion === "Reducir la velocidad" => 5,
    default => 0,
};

echo "Acción: $accion\n";
echo "Velocidad máxima: $velocidad nudos\n";
```

### Misión R01-N05-M3 · El año del faro

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El farero anota en su libro si cada año es **bisiesto**, porque ese año hay un día
más de guardia. Un año es bisiesto si es divisible por 4, **salvo** que sea
divisible por 100, **aunque** sí lo es si es divisible por 400. Leé tres años (uno
por renglón) y, para cada uno, mostrá si es bisiesto y cuántos días tiene. Escribí
la regla como **una sola** condición con `&&`, `||` y `%`.

#### Criterio de aprobación

- La regla es una sola expresión con `%`, `&&` y `||`.
- Para 1900, 2000 y 2028 da los resultados correctos.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
1900
2000
2028
```

#### Salida esperada

```
1900: común (365 días)
2000: bisiesto (366 días)
2028: bisiesto (366 días)
```

#### Solución de referencia

```php
<?php
// Mision 3 - El año del faro: una condición compuesta para los bisiestos.
for ($i = 1; $i <= 3; $i++) {
    $anio = (int) trim(fgets(STDIN));
    $bisiesto = ($anio % 4 === 0 && $anio % 100 !== 0) || $anio % 400 === 0;
    $dias = $bisiesto ? 366 : 365;
    echo $anio, ": ", $bisiesto ? "bisiesto" : "común", " ($dias días)\n";
}
```

### Encargo R01-N05-E1 · El envío de la tienda online

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una tienda online de La Rioja calcula el costo de envío así:

- según la **zona** (`capital`, `interior`, `otra provincia`): 1500, 3500 o 6000;
- si el paquete pesa más de 5 kg, se suman $400 por cada kilo (entero) que pase de
  5 (usá `ceil`);
- si la compra supera los $80000, el envío es **gratis** para `capital` e
  `interior`, y tiene 50% de descuento para `otra provincia`.

Leé la zona, el peso y el monto de la compra. Si la zona no es ninguna de las
tres, mostrá `Zona desconocida.` y terminá. Mostrá el detalle del cálculo.

#### Criterio de aprobación

- Usa `match` para el costo por zona (con un `default` que detecte la zona
  desconocida).
- Las reglas de peso y de compra grande se aplican con `if`.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
otra provincia
7.2
95000
```

#### Salida esperada

```
Zona: Peso (kg): Compra ($): 
Base (otra provincia): 6000
Extra por peso: 1200
Compra grande: 50% de descuento en el envío
Envío: $3.600,00
```

#### Solución de referencia

```php
<?php
// Encargo - El envío de la tienda online: match para la zona e if para las reglas.
echo "Zona: ";
$zona = strtolower(trim(fgets(STDIN)));
echo "Peso (kg): ";
$peso = (float) trim(fgets(STDIN));
echo "Compra ($): ";
$compra = (float) trim(fgets(STDIN));
echo "\n";

$base = match ($zona) {
    "capital" => 1500,
    "interior" => 3500,
    "otra provincia" => 6000,
    default => null,
};
if ($base === null) {
    echo "Zona desconocida.\n";
    exit(1);
}

$extraPeso = 0;
if ($peso > 5) {
    $extraPeso = ceil($peso - 5) * 400;
}
$envio = $base + $extraPeso;
echo "Base ($zona): $base\n";
echo "Extra por peso: $extraPeso\n";

if ($compra > 80000) {
    if ($zona === "otra provincia") {
        $envio *= 0.5;
        echo "Compra grande: 50% de descuento en el envío\n";
    } else {
        $envio = 0;
        echo "Compra grande: envío gratis\n";
    }
}
echo "Envío: $", number_format($envio, 2, ',', '.'), "\n";
```

### Prueba del sello

#### ¿Qué pasa si en un `switch` falta el `break`?

La ejecución sigue en el caso de abajo y ejecuta también su código ("se cae" al siguiente caso).

#### ¿Qué diferencia hay entre `switch` y `match` al comparar?

`switch` compara con `==` (convierte los tipos) y `match` con `===` (estricto).

#### ¿Qué pasa si ningún caso de un `match` coincide y no hay `default`?

Se produce un error `UnhandledMatchError` y el programa se corta.

#### ¿Para qué sirve `match (true)`?

Para poner una condición en cada rama: se elige la primera cuya condición sea verdadera.

#### ¿Qué es una cláusula de guarda?

Un `if` al principio que descarta los casos inválidos (y termina o devuelve) para que el resto del código trabaje con datos válidos, sin anidar.

### Soluciones (docente)

Sale de `21-PHP/03-Control`. Se insiste en `match` sobre `switch` por la comparación estricta. En la misión 3 conviene mostrar por qué 1900 no es bisiesto y 2000 sí (el caso que más se equivoca). En el encargo, `ceil(7.2 - 5)` da `3.0`: 3 kilos extra.

## R01-N06 · Bucles: while, do-while, for y foreach

```meta
tipo: tema
padre: R01-N05
precio: 10
criatura: orc
temas: prog.bucles
```

### Crónica

Al amanecer, una fila de barcos espera para descargar. El jefe de estibadores repite siempre lo mismo: bajar un cajón, anotarlo, bajar el siguiente, hasta que la bodega queda vacía. Cuando aparece un cajón roto, lo aparta y sigue con el próximo.

—**Repetir** es lo que mejor hace una máquina —dice {mentor}—. Una instrucción, mil veces, sin cansarse. Lo difícil es decirle cuándo parar, {heroe}. Un bucle que no termina nunca deja el muelle trabado para siempre.

### Objetivos

- Repetir con `while` mientras se cumpla una condición.
- Usar `do-while` cuando el bloque tiene que correr al menos una vez.
- Contar con `for`.
- Recorrer una lista con `foreach` (la presentación: en el nodo de arrays se profundiza).
- Controlar el bucle con `break` y `continue`, y salir de bucles anidados.
- Usar acumuladores y contadores.

### Antes de empezar

- Decisiones con `if` y `match` (R01-N05).

### Explicación

#### `while`: mientras se cumpla
```php
$cajones = 5;
while ($cajones > 0) {
    echo "Bajo un cajón, quedan ", $cajones - 1, "\n";
    $cajones--;
}
```
Se pregunta la condición **antes** de cada vuelta. Si al principio es falsa, el
bloque no se ejecuta nunca. Adentro tiene que cambiar algo que haga que la
condición termine siendo falsa; si no, es un **bucle infinito** (se corta con
`Ctrl+C`).

#### `do-while`: al menos una vez
```php
do {
    echo "Clave: ";
    $clave = trim(fgets(STDIN));
} while ($clave !== "ancla");
```
Se pregunta **después** de cada vuelta: sirve para "pedir hasta que sea válido".

#### `for`: contar
```php
for ($i = 1; $i <= 10; $i++) {
    echo "Campanada $i\n";
}
```
Las tres partes: **inicio** (`$i = 1`), **condición** para seguir (`$i <= 10`) y
**paso** (`$i++`). Se puede contar hacia atrás (`$i--`) o de a varios (`$i += 5`).

#### `foreach`: recorrer una lista
```php
$barcos = ["Gaviota", "Albatros", "Tortuga"];
foreach ($barcos as $barco) {
    echo "Llega: $barco\n";
}
foreach ($barcos as $posicion => $barco) {
    echo "$posicion. $barco\n";      // 0. Gaviota, 1. Albatros...
}
```
`range(1, 5)` arma la lista `[1, 2, 3, 4, 5]`, y `range(0, 100, 10)` cuenta de 10
en 10. Los arrays se ven a fondo en el próximo nodo.

#### `break` y `continue`
```php
for ($i = 1; $i <= 100; $i++) {
    if ($i % 2 === 0) {
        continue;        // saltea el resto de esta vuelta y pasa a la siguiente
    }
    if ($i > 9) {
        break;           // termina el bucle
    }
    echo $i, " ";        // 1 3 5 7 9
}
```
Con bucles **anidados**, `break 2` y `continue 2` salen o saltan también el bucle
de afuera.

#### Acumuladores y contadores
El patrón más usado: una variable que arranca en 0 **antes** del bucle y se va
sumando **adentro**:
```php
$total = 0;          // acumulador
$pesados = 0;        // contador
foreach ($pesos as $peso) {
    $total += $peso;
    if ($peso > 100) {
        $pesados++;
    }
}
```
Para buscar el máximo, se arranca con el primero (o con `PHP_INT_MIN`) y se
compara cada uno.

#### Leer hasta que no haya más
`fgets` devuelve `false` al terminar la entrada. Así se leen renglones sin saber
cuántos son:
```php
while (($linea = fgets(STDIN)) !== false) {
    $linea = trim($linea);
    // …
}
```

### Código de ejemplo

```php
<?php
/*
 * Los estibadores: while, do-while, for, foreach, break y continue.
 */
// while: descargar hasta vaciar
$enBodega = 4;
while ($enBodega > 0) {
    echo "Descargo un cajón (quedan ", --$enBodega, ")\n";
}

// for: las campanadas
echo "Campanadas:";
for ($i = 1; $i <= 6; $i++) {
    echo " $i";
}
echo "\n";

// foreach con acumulador, contador y máximo
$pesos = [120, 35, 0, 480, 75, 210];
$total = 0;
$pesados = 0;
$maximo = $pesos[0];
foreach ($pesos as $numero => $peso) {
    if ($peso === 0) {
        echo "Cajón $numero vacío: se aparta\n";
        continue;
    }
    $total += $peso;
    if ($peso > 100) {
        $pesados++;
    }
    if ($peso > $maximo) {
        $maximo = $peso;
    }
}
echo "Total: $total kg · pesados: $pesados · el más pesado: $maximo kg\n";

// break: el primer cajón que no entra en la grúa
foreach ($pesos as $numero => $peso) {
    if ($peso > 400) {
        echo "El cajón $numero ($peso kg) no entra en la grúa: se para\n";
        break;
    }
}

// Bucles anidados: la grilla de casilleros
for ($fila = 1; $fila <= 3; $fila++) {
    for ($col = 1; $col <= 4; $col++) {
        echo str_pad($fila * $col, 4, " ", STR_PAD_LEFT);
    }
    echo "\n";
}

// do-while: pedir hasta que sea válido
do {
    echo "Muelle (1 a 3): ";
    $muelle = (int) trim(fgets(STDIN));
} while ($muelle < 1 || $muelle > 3);
echo "\nMuelle elegido: $muelle\n";
```

### Entrada de ejemplo

```
7
0
2
```

### Salida esperada

```
Descargo un cajón (quedan 3)
Descargo un cajón (quedan 2)
Descargo un cajón (quedan 1)
Descargo un cajón (quedan 0)
Campanadas: 1 2 3 4 5 6
Cajón 2 vacío: se aparta
Total: 920 kg · pesados: 3 · el más pesado: 480 kg
El cajón 3 (480 kg) no entra en la grúa: se para
   1   2   3   4
   2   4   6   8
   3   6   9  12
Muelle (1 a 3): Muelle (1 a 3): Muelle (1 a 3): 
Muelle elegido: 2
```

### ¿Para qué sirve?

Todo listado en una página web es un bucle: los productos de una tienda, los mensajes de un foro, las filas de una tabla que vino de la base de datos. Y los acumuladores están en cada total de un carrito, en cada promedio de un boletín, en cada reporte.

### Errores habituales

**Ogro: el bucle infinito.** `while ($cajones > 0) { echo "..."; }` sin `$cajones--`
nunca termina. Revisá que algo adentro acerque la condición al final. Se corta con
`Ctrl+C`.

**Orco: uno de más o de menos.** `for ($i = 0; $i <= count($lista); $i++)` recorre
una posición que no existe (`Undefined array key`). Con `<` alcanza, o mejor
`foreach`.

**Ogro: el acumulador adentro del bucle.** Si `$total = 0;` está **adentro**, se
reinicia en cada vuelta y al final solo queda el último valor.

**Ogro: `continue` en un `switch`.** Adentro de un `switch`, `continue` actúa como
`break` y PHP avisa: `"continue" targeting switch is equivalent to "break"`. Si
querías saltar la vuelta del bucle, `continue 2`.

**Ogro: el `;` después del `for`.** `for ($i = 0; $i < 5; $i++);` con punto y coma
repite **nada** cinco veces, y el bloque de abajo corre una sola vez.

### Misión R01-N06-M1 · La tabla del estibador

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El estibador tiene que saber cuánto pesan varios cajones iguales. Leé el peso de un
cajón y mostrá la tabla de 1 a 10 cajones con `for`, alineada con `printf`. Marcá
con ` <- excede` los renglones en los que el peso supera los 250 kg, y al final
mostrá cuántos cajones se pueden cargar como máximo sin pasar los 250 kg.

#### Criterio de aprobación

- Usa `for` de 1 a 10.
- Cuenta los renglones que no exceden con un contador.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
32.5
```

#### Salida esperada

```
Peso de un cajón (kg): 
 1 cajón/es:    32.5 kg
 2 cajón/es:    65.0 kg
 3 cajón/es:    97.5 kg
 4 cajón/es:   130.0 kg
 5 cajón/es:   162.5 kg
 6 cajón/es:   195.0 kg
 7 cajón/es:   227.5 kg
 8 cajón/es:   260.0 kg <- excede
 9 cajón/es:   292.5 kg <- excede
10 cajón/es:   325.0 kg <- excede
Máximo sin pasar 250 kg: 7 cajón/es
```

#### Solución de referencia

```php
<?php
// Mision 1 - La tabla del estibador: for, printf y un contador.
echo "Peso de un cajón (kg): ";
$peso = (float) trim(fgets(STDIN));
echo "\n";

$maximo = 0;
for ($i = 1; $i <= 10; $i++) {
    $total = $i * $peso;
    printf("%2d cajón/es: %7.1f kg%s\n", $i, $total, $total > 250 ? " <- excede" : "");
    if ($total <= 250) {
        $maximo++;
    }
}
echo "Máximo sin pasar 250 kg: $maximo cajón/es\n";
```

### Misión R01-N06-M2 · La clave del almacén

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El almacén del puerto se abre con la clave `ancla`. Pedí la clave con un
`do-while` hasta que sea correcta, pero con un máximo de **3 intentos**: si se
equivoca tres veces, mostrá `Almacén bloqueado.` y terminá con `exit(1)`. En cada
error mostrá cuántos intentos le quedan. Si acierta, mostrá en qué intento lo
logró.

#### Criterio de aprobación

- Usa `do-while` con un contador de intentos.
- Corta a los 3 intentos.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
timon
Ancla
ancla
```

#### Salida esperada

```
Clave: Incorrecta. Te quedan 2 intento/s.
Clave: Incorrecta. Te quedan 1 intento/s.
Clave: Adelante. Acertaste en el intento 3.
```

#### Solución de referencia

```php
<?php
// Mision 2 - La clave del almacén: do-while con un límite de intentos.
const CLAVE = "ancla";
const MAX_INTENTOS = 3;

$intentos = 0;
do {
    echo "Clave: ";
    $clave = trim(fgets(STDIN));
    $intentos++;
    $correcta = $clave === CLAVE;
    if (!$correcta && $intentos < MAX_INTENTOS) {
        echo "Incorrecta. Te quedan ", MAX_INTENTOS - $intentos, " intento/s.\n";
    }
} while (!$correcta && $intentos < MAX_INTENTOS);

if (!$correcta) {
    echo "Almacén bloqueado.\n";
    exit(1);
}
echo "Adelante. Acertaste en el intento $intentos.\n";
```

### Misión R01-N06-M3 · El registro de llegadas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El registro de llegadas se lee renglón por renglón **hasta que se termina la
entrada** (con `while` y `fgets` que devuelve `false`). Cada renglón tiene el
nombre del barco y la cantidad de pasajeros separados por `;`. Los renglones
vacíos se saltean (`continue`). Si un renglón dice `FIN`, se deja de leer
(`break`) aunque haya más. Mostrá cada barco y, al final, cuántos barcos llegaron,
el total de pasajeros, el promedio (dos decimales) y el barco con más pasajeros.

#### Criterio de aprobación

- Lee con `while (($linea = fgets(STDIN)) !== false)`.
- Usa `continue` para los vacíos y `break` para `FIN`.
- Calcula total, promedio y máximo con acumuladores.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
Gaviota;34

Albatros;120
Tortuga;18
FIN
Fantasma;999
```

#### Salida esperada

```
Llegó Gaviota con 34 pasajeros
Llegó Albatros con 120 pasajeros
Llegó Tortuga con 18 pasajeros
Barcos: 3
Pasajeros: 172
Promedio: 57.33
El más lleno: Albatros (120)
```

#### Solución de referencia

```php
<?php
// Mision 3 - El registro de llegadas: leer hasta el final, continue y break.
$barcos = 0;
$pasajeros = 0;
$mayor = "";
$maxPasajeros = -1;

while (($linea = fgets(STDIN)) !== false) {
    $linea = trim($linea);
    if ($linea === "") {
        continue;
    }
    if ($linea === "FIN") {
        break;
    }
    [$nombre, $cantidad] = explode(";", $linea);
    $cantidad = (int) $cantidad;
    echo "Llegó $nombre con $cantidad pasajeros\n";

    $barcos++;
    $pasajeros += $cantidad;
    if ($cantidad > $maxPasajeros) {
        $maxPasajeros = $cantidad;
        $mayor = $nombre;
    }
}

echo "Barcos: $barcos\n";
echo "Pasajeros: $pasajeros\n";
printf("Promedio: %.2f\n", $barcos > 0 ? $pasajeros / $barcos : 0);
echo "El más lleno: $mayor ($maxPasajeros)\n";
```

### Encargo R01-N06-E1 · El plan de cuotas

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una casa de electrodomésticos vende una heladera de **$950000** en **6 cuotas**
con un interés del **4% mensual** sobre el saldo que queda. Cada mes se paga una
cuota fija de capital (el precio dividido la cantidad de cuotas) más el interés
del saldo de ese mes. Mostrá una tabla con el número de cuota, el saldo al
empezar el mes, el interés, la cuota a pagar y el saldo que queda; y al final el
total pagado y cuánto se pagó de intereses. Los importes, con `number_format` a
la argentina.

#### Criterio de aprobación

- Usa un `for` y acumuladores para el total y los intereses.
- El saldo se actualiza en cada vuelta.
- La salida coincide con la esperada.

#### Salida esperada

```
Cuota           Saldo      Interés        A pagar          Queda
1          950.000,00    38.000,00     196.333,33     791.666,67
2          791.666,67    31.666,67     190.000,00     633.333,33
3          633.333,33    25.333,33     183.666,67     475.000,00
4          475.000,00    19.000,00     177.333,33     316.666,67
5          316.666,67    12.666,67     171.000,00     158.333,33
6          158.333,33     6.333,33     164.666,67           0,00
Total pagado: $1.083.000,00
Intereses: $133.000,00
```

#### Solución de referencia

```php
<?php
// Encargo - El plan de cuotas: for con saldo que baja y acumuladores.
const PRECIO = 950000;
const CUOTAS = 6;
const INTERES = 0.04;

$capital = PRECIO / CUOTAS;
$saldo = PRECIO;
$totalPagado = 0;
$totalIntereses = 0;

// "Interés" tiene tilde: ocupa un byte más, así que su ancho va con uno más (13).
printf("%-6s %14s %13s %14s %14s\n", "Cuota", "Saldo", "Interés", "A pagar", "Queda");
for ($n = 1; $n <= CUOTAS; $n++) {
    $interes = $saldo * INTERES;
    $cuota = $capital + $interes;
    $queda = $saldo - $capital;
    printf(
        "%-6d %14s %12s %14s %14s\n",
        $n,
        number_format($saldo, 2, ',', '.'),
        number_format($interes, 2, ',', '.'),
        number_format($cuota, 2, ',', '.'),
        number_format($queda, 2, ',', '.')
    );
    $totalPagado += $cuota;
    $totalIntereses += $interes;
    $saldo = $queda;
}
echo "Total pagado: $", number_format($totalPagado, 2, ',', '.'), "\n";
echo "Intereses: $", number_format($totalIntereses, 2, ',', '.'), "\n";
```

### Prueba del sello

#### ¿Qué diferencia hay entre `while` y `do-while`?

`while` pregunta la condición antes de cada vuelta (puede no ejecutarse nunca); `do-while` la pregunta después, así que el bloque corre al menos una vez.

#### ¿Qué hacen `break` y `continue`?

`break` termina el bucle; `continue` saltea lo que queda de la vuelta actual y pasa a la siguiente.

#### ¿Cómo se sale de dos bucles anidados a la vez?

Con `break 2` (y `continue 2` salta a la siguiente vuelta del bucle de afuera).

#### ¿Dónde se inicializa un acumulador y por qué?

Antes del bucle: si se inicializa adentro, se reinicia en cada vuelta y se pierde lo sumado.

#### ¿Cómo se leen renglones del teclado sin saber cuántos son?

Con `while (($linea = fgets(STDIN)) !== false)`, porque `fgets` devuelve `false` cuando se termina la entrada.

### Soluciones (docente)

Sale de `21-PHP/04-Bucles`, ampliado con acumuladores, lectura hasta el final de la entrada y el plan de cuotas (sistema alemán simplificado). En el ejemplo, `--$enBodega` decrementa antes de mostrar: vale la pena comparar con `$enBodega--` en clase. La misión 2 no muestra "te quedan 0 intentos": el último error va directo a "Almacén bloqueado." (en el ejemplo acierta en el tercero).

## R01-N07 · Arrays: listas y diccionarios

```meta
tipo: tema
padre: R01-N06
precio: 10
criatura: orc
temas: col.listas, col.mapas, col.matrices
```

### Crónica

La bodega del tercer muelle es un laberinto de estantes numerados. En algunos, los cajones van en fila: el primero, el segundo, el tercero. En otros, cada cajón tiene una etiqueta con un nombre: *harina*, *sal*, *aceite*. El bodeguero sabe encontrar cualquier cosa en segundos.

—En PHP, un solo tipo hace de fila y de estante con etiquetas: el **array** —dice {mentor}—. Es la herramienta que más vas a usar, {heroe}. Todo lo que llega de un formulario, de un archivo o de la base de datos llega en un array. Y los orcos acechan en las posiciones que no existen.

### Objetivos

- Crear arrays indexados (listas) y asociativos (diccionarios).
- Agregar, cambiar, sacar y preguntar si existe un elemento.
- Recorrer arrays con `foreach`, con clave y valor.
- Armar arrays de arrays (tablas) y recorrerlos.
- Usar las funciones más comunes: contar, sumar, buscar, ordenar, filtrar y transformar.
- Desestructurar un array en variables y combinar arrays con `...`.

### Antes de empezar

- Bucles, en especial `foreach` (R01-N06).

### Explicación

#### Listas: arrays indexados
```php
$barcos = ["Gaviota", "Albatros", "Tortuga"];
echo $barcos[0];          // Gaviota   (las posiciones empiezan en 0)
echo count($barcos);      // 3
$barcos[] = "Delfín";     // agrega al final
$barcos[1] = "Cóndor";    // cambia la posición 1
```

#### Diccionarios: arrays asociativos
Cada valor tiene una **clave** con nombre:
```php
$precios = ["pan" => 300, "guiso" => 1200, "mate" => 450];
echo $precios["guiso"];   // 1200
$precios["té"] = 400;     // agrega (o cambia, si ya existía)
unset($precios["pan"]);   // saca
```
En PHP **es el mismo tipo**: una lista es un array cuyas claves son `0, 1, 2…`.

#### ¿Existe?
Pedir una clave que no está da el aviso de los **orcos**:
```
PHP Warning:  Undefined array key "cafe"
```
Antes de leer, se pregunta:
```php
isset($precios["cafe"])            // ¿existe y no es null?
array_key_exists("cafe", $precios) // ¿existe la clave? (aunque valga null)
$precios["cafe"] ?? 0              // el valor, o 0 si no está
in_array("Gaviota", $barcos, true) // ¿está este VALOR? (true = compara con ===)
```

#### Recorrer
```php
foreach ($precios as $producto => $precio) {
    echo "$producto: $precio\n";
}
```

#### Arrays de arrays
Una tabla es una lista de filas, y cada fila es un diccionario:
```php
$pasajeros = [
    ["nombre" => "Kira", "edad" => 17, "destino" => "Valle"],
    ["nombre" => "Bron", "edad" => 45, "destino" => "Forjas"],
];
echo $pasajeros[1]["nombre"];      // Bron
foreach ($pasajeros as $p) {
    echo "{$p['nombre']} va a {$p['destino']}\n";
}
```
Así llegan los resultados de la base de datos en la cuarta rama.

#### Ver un array entero
`echo` no sirve para arrays (muestra `Array` y un aviso). Para depurar:
```php
print_r($precios);   // legible
var_dump($precios);  // con los tipos
```

#### Las funciones más usadas
| Función | Qué hace |
|---|---|
| `count($a)` | cantidad de elementos |
| `array_sum($a)`, `max($a)`, `min($a)` | suma, máximo, mínimo |
| `array_keys($a)`, `array_values($a)` | solo las claves, solo los valores |
| `array_search($v, $a, true)` | la clave de un valor (o `false`) |
| `array_slice($a, $desde, $cant)` | un pedazo |
| `array_merge($a, $b)` | une dos arrays |
| `array_unique($a)` | sin repetidos |
| `array_column($filas, "col")` | una columna de una tabla |
| `range(1, 5)` | `[1, 2, 3, 4, 5]` |
| `implode(", ", $a)` / `explode(",", $t)` | array ↔ texto |

#### Ordenar
Todas ordenan **el mismo array** (no devuelven uno nuevo):
| Función | Ordena por | Conserva las claves |
|---|---|---|
| `sort` / `rsort` | valor, de menor a mayor / al revés | no (renumera) |
| `asort` / `arsort` | valor | sí |
| `ksort` / `krsort` | clave | sí |
| `usort($a, fn($x, $y) => …)` | lo que diga tu función | no |

Con `usort` y la nave espacial `<=>` se ordena una tabla por cualquier columna:
```php
usort($pasajeros, fn($a, $b) => $a["edad"] <=> $b["edad"]);
```
(`fn` es una función corta: la vas a ver en el próximo nodo.)

#### Filtrar y transformar
```php
$caros = array_filter($precios, fn($p) => $p > 400);     // se queda con los que cumplen
$conIva = array_map(fn($p) => $p * 1.21, $precios);      // transforma cada uno
```
Ojo: `array_filter` **conserva las claves** originales. En una lista, después de
filtrar pueden quedar huecos (`[0, 1, 3]`); `array_values` la renumera.

#### Desestructurar y combinar
```php
[$primero, $segundo] = $barcos;                         // por posición
["nombre" => $nombre, "edad" => $edad] = $pasajeros[0]; // por clave
$todos = [...$barcos, ...["Ballena", "Foca"]];          // "desparrama" arrays
```

### Código de ejemplo

```php
<?php
/*
 * La bodega del muelle 3: listas, diccionarios y tablas.
 */
$estantes = ["harina", "sal", "aceite"];
$estantes[] = "yerba";
echo "Hay ", count($estantes), " estantes; el primero es de {$estantes[0]}\n";

$stock = ["harina" => 40, "sal" => 12, "aceite" => 0, "yerba" => 25];
$stock["azúcar"] = 18;
unset($stock["aceite"]);

foreach ($stock as $producto => $cantidad) {
    printf("%-8s %3d\n", $producto, $cantidad);   // "azúcar" sale corrida: la ú ocupa 2 bytes (R01-N03)
}
echo "Total de bolsas: ", array_sum($stock), "\n";
echo "¿Hay café? ", isset($stock["café"]) ? "sí" : "no", " (", $stock["café"] ?? 0, ")\n";

// Ordenar
arsort($stock);
echo "Más stock primero: ", implode(", ", array_keys($stock)), "\n";

// Filtrar y transformar
$poco = array_filter($stock, fn($c) => $c < 20);
echo "Poco stock: ", implode(", ", array_keys($poco)), "\n";
$pedido = array_map(fn($c) => 50 - $c, $poco);
print_r($pedido);

// Una tabla: lista de diccionarios
$barcos = [
    ["nombre" => "Gaviota", "carga" => 450, "origen" => "Valle"],
    ["nombre" => "Albatros", "carga" => 1200, "origen" => "Imperio"],
    ["nombre" => "Tortuga", "carga" => 80, "origen" => "Forjas"],
];
usort($barcos, fn($a, $b) => $b["carga"] <=> $a["carga"]);
foreach ($barcos as $i => $b) {
    echo $i + 1, ". {$b['nombre']} ({$b['origen']}): {$b['carga']} kg\n";
}
echo "Cargas: ", implode(" + ", array_column($barcos, "carga")), "\n";

// Desestructurar
["nombre" => $mayor, "carga" => $kilos] = $barcos[0];
echo "El más cargado: $mayor con $kilos kg\n";
```

### Salida esperada

```
Hay 4 estantes; el primero es de harina
harina    40
sal       12
yerba     25
azúcar   18
Total de bolsas: 95
¿Hay café? no (0)
Más stock primero: harina, yerba, azúcar, sal
Poco stock: azúcar, sal
Array
(
    [azúcar] => 32
    [sal] => 38
)
1. Albatros (Imperio): 1200 kg
2. Gaviota (Valle): 450 kg
3. Tortuga (Forjas): 80 kg
Cargas: 1200 + 450 + 80
El más cargado: Albatros con 1200 kg
```

### ¿Para qué sirve?

En PHP web **todo** es un array: `$_GET` y `$_POST` son diccionarios con lo que mandó el formulario, las filas que devuelve la base de datos son arrays, un carrito de compras es un array de productos, un JSON se convierte en un array. Saber recorrerlos, filtrarlos y ordenarlos es la mitad del trabajo.

### Errores habituales

**Orco: la clave que no existe.** `$_GET["pagina"]` cuando no vino da
`Warning: Undefined array key "pagina"`. Usá `?? valor` o `isset`.

**Orco: el hueco después de filtrar o de `unset`.** Después de
`unset($lista[1])`, la lista tiene las claves `0, 2, 3`: un `for` de `0` a
`count()` pide la `1` y falla. Usá `foreach` o `array_values`.

**Goblin: `echo` de un array.** `echo $stock;` muestra `Array` y el aviso
`Array to string conversion`. Usá `print_r`, `implode` o un `foreach`.

**Ogro: `in_array` sin `true`.** `in_array("1e1", ["10"])` da `true` porque compara
con `==`. Pasale `true` como tercer argumento.

**Ogro: esperar que `sort` devuelva el array.** `$ordenado = sort($lista);` guarda
`true`, no la lista: `sort` ordena la misma variable.

### Misión R01-N07-M1 · El inventario de la bodega

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La bodega tiene este stock: `harina` 40, `sal` 12, `yerba` 25, `aceite` 7,
`azúcar` 18. Con un array asociativo:

1. Mostrá el inventario ordenado **alfabéticamente** por producto (`ksort`).
2. Llegó un camión: sumale 30 a cada producto que tenga menos de 15 (con un
   `foreach` por referencia `&$cantidad`, o recorriendo las claves).
3. Mostrá el inventario actualizado ordenado de **mayor a menor** cantidad.
4. Mostrá el producto con más stock y el total.

#### Criterio de aprobación

- Usa un array asociativo y `ksort`/`arsort`.
- Calcula el máximo y el total con funciones de arrays.
- La salida coincide con la esperada.

#### Salida esperada

```
Inventario:
  aceite: 7
  azúcar: 18
  harina: 40
  sal: 12
  yerba: 25
Después del camión:
  sal: 42
  harina: 40
  aceite: 37
  yerba: 25
  azúcar: 18
Más stock: sal (42)
Total: 162
```

#### Solución de referencia

```php
<?php
// Mision 1 - El inventario de la bodega: array asociativo, ordenar y actualizar.
$stock = ["harina" => 40, "sal" => 12, "yerba" => 25, "aceite" => 7, "azúcar" => 18];

ksort($stock);
echo "Inventario:\n";
foreach ($stock as $producto => $cantidad) {
    echo "  $producto: $cantidad\n";
}

foreach ($stock as $producto => $cantidad) {
    if ($cantidad < 15) {
        $stock[$producto] += 30;
    }
}

arsort($stock);
echo "Después del camión:\n";
foreach ($stock as $producto => $cantidad) {
    echo "  $producto: $cantidad\n";
}
echo "Más stock: ", array_key_first($stock), " (", max($stock), ")\n";
echo "Total: ", array_sum($stock), "\n";
```

### Misión R01-N07-M2 · Las notas de la escuela náutica

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La escuela náutica tiene sus alumnos en una tabla (una lista de diccionarios) con
nombre y tres notas:

- Kira: 8, 9, 7
- Bron: 5, 6, 4
- Ivo: 10, 9, 10
- Olmo: 6, 7, 6

Para cada alumno calculá el promedio (con `array_sum` y `count`) y guardalo en su
fila. Después:

1. Ordená la tabla por promedio de mayor a menor con `usort`.
2. Mostrá cada alumno con su promedio (un decimal) y `aprobado` si es 6 o más.
3. Mostrá, con `array_filter`, los nombres de los que desaprobaron.

#### Criterio de aprobación

- Guarda los datos en una lista de arrays asociativos.
- Ordena con `usort` y `<=>`, y filtra con `array_filter`.
- La salida coincide con la esperada.

#### Salida esperada

```
Ivo    9.7 aprobado
Kira   8.0 aprobado
Olmo   6.3 aprobado
Bron   5.0 a recuperar
A recuperar: Bron
```

#### Solución de referencia

```php
<?php
// Mision 2 - Las notas de la escuela náutica: tabla, usort y array_filter.
$alumnos = [
    ["nombre" => "Kira", "notas" => [8, 9, 7]],
    ["nombre" => "Bron", "notas" => [5, 6, 4]],
    ["nombre" => "Ivo", "notas" => [10, 9, 10]],
    ["nombre" => "Olmo", "notas" => [6, 7, 6]],
];

foreach ($alumnos as $i => $alumno) {
    $alumnos[$i]["promedio"] = array_sum($alumno["notas"]) / count($alumno["notas"]);
}

usort($alumnos, fn($a, $b) => $b["promedio"] <=> $a["promedio"]);

foreach ($alumnos as $a) {
    printf("%-5s %4.1f %s\n", $a["nombre"], $a["promedio"], $a["promedio"] >= 6 ? "aprobado" : "a recuperar");
}

$desaprobados = array_filter($alumnos, fn($a) => $a["promedio"] < 6);
echo "A recuperar: ", implode(", ", array_column($desaprobados, "nombre")), "\n";
```

### Misión R01-N07-M3 · El contador de palabras

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La Capitana quiere saber qué palabras se repiten más en los mensajes que llegan.
Leé renglones hasta el final de la entrada, pasá todo a minúsculas
(`mb_strtolower`), sacá los signos `.` `,` `¡` `!` `¿` `?` (con `str_replace`
y un array de signos) y partí cada renglón en palabras. Contá cuántas veces
aparece cada palabra en un array asociativo `palabra => cantidad` e ignorá las
palabras de menos de 3 letras. Mostrá las **5** más frecuentes (con `arsort` y
`array_slice`); si empatan, en el orden en que aparecieron.

#### Criterio de aprobación

- Cuenta con un array asociativo (`$cuenta[$palabra] = ($cuenta[$palabra] ?? 0) + 1`).
- Usa `arsort` y `array_slice` para las 5 primeras.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
¡El barco llegó! El barco trae cartas.
Las cartas son para el faro, y el faro espera.
¿Llegó el barco del Valle? Sí, el barco llegó.
```

#### Salida esperada

```
barco: 4
llegó: 3
cartas: 2
faro: 2
trae: 1
```

#### Solución de referencia

```php
<?php
// Mision 3 - El contador de palabras: contar con un array asociativo.
$signos = [".", ",", "¡", "!", "¿", "?"];
$cuenta = [];

while (($linea = fgets(STDIN)) !== false) {
    $limpia = str_replace($signos, "", mb_strtolower(trim($linea)));
    foreach (explode(" ", $limpia) as $palabra) {
        if (mb_strlen($palabra) < 3) {
            continue;
        }
        $cuenta[$palabra] = ($cuenta[$palabra] ?? 0) + 1;
    }
}

arsort($cuenta);
foreach (array_slice($cuenta, 0, 5) as $palabra => $veces) {
    echo "$palabra: $veces\n";
}
```

### Encargo R01-N07-E1 · El carrito de la despensa

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

La despensa del puerto tiene una lista de precios (`yerba` 4200, `azúcar` 1500,
`fideos` 1100, `aceite` 3800, `galletitas` 1600). Un cliente escribe su pedido,
un producto por renglón con la cantidad (`yerba 2`), hasta el final de la
entrada. Armá el carrito:

- si el producto no está en la lista, mostrá `No tenemos: PRODUCTO` y seguí;
- si el producto se repite, sumá las cantidades;
- al final mostrá el ticket ordenado por producto, con cantidad, precio unitario y
  subtotal, y el total. Si el total supera $15000, 10% de descuento.

#### Criterio de aprobación

- La lista de precios y el carrito son arrays asociativos.
- Suma cantidades de productos repetidos.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
yerba 2
fideos 3
chocolate 1
yerba 1
aceite 1
```

#### Salida esperada

```
No tenemos: chocolate
aceite     x1     3800     3800
fideos     x3     1100     3300
yerba      x3     4200    12600
Descuento 10%: -1970
TOTAL: 17730
```

#### Solución de referencia

```php
<?php
// Encargo - El carrito de la despensa: diccionarios de precios y de carrito.
$precios = ["yerba" => 4200, "azúcar" => 1500, "fideos" => 1100, "aceite" => 3800, "galletitas" => 1600];
$carrito = [];

while (($linea = fgets(STDIN)) !== false) {
    $linea = trim($linea);
    if ($linea === "") {
        continue;
    }
    [$producto, $cantidad] = explode(" ", $linea);
    if (!isset($precios[$producto])) {
        echo "No tenemos: $producto\n";
        continue;
    }
    $carrito[$producto] = ($carrito[$producto] ?? 0) + (int) $cantidad;
}

ksort($carrito);
$total = 0;
foreach ($carrito as $producto => $cantidad) {
    $subtotal = $cantidad * $precios[$producto];
    $total += $subtotal;
    printf("%-10s x%-3d %6d %8d\n", $producto, $cantidad, $precios[$producto], $subtotal);
}
if ($total > 15000) {
    echo "Descuento 10%: -", $total * 0.10, "\n";
    $total *= 0.90;
}
echo "TOTAL: ", $total, "\n";
```

### Prueba del sello

#### ¿Qué diferencia hay entre un array indexado y uno asociativo?

En el indexado las claves son posiciones `0, 1, 2…`; en el asociativo son nombres (`"pan" => 300`). En PHP son el mismo tipo.

#### ¿Cómo se agrega un elemento al final de una lista?

Con `$lista[] = $valor;`.

#### ¿Cómo evitás el aviso `Undefined array key`?

Preguntando antes con `isset`/`array_key_exists`, o leyendo con `$a["clave"] ?? valorPorDefecto`.

#### ¿Qué diferencia hay entre `sort` y `asort`?

Las dos ordenan por valor, pero `sort` renumera las claves y `asort` las conserva (sirve para diccionarios).

#### ¿Qué pasa con las claves después de `array_filter`?

Se conservan las originales, así que en una lista pueden quedar huecos; `array_values` la renumera.

### Soluciones (docente)

Sale de `21-PHP/05-Arrays`, ampliado con tablas (listas de diccionarios), `usort`, `array_column` y el conteo con diccionarios, que se usan mucho después con la base de datos. En la misión 3, `arsort` es estable desde PHP 8, así que los empates quedan en el orden de aparición. En el encargo, `azúcar` no aparece en el pedido; se puede pedir como variante que el cliente escriba productos con mayúsculas.

## R01-N08 · Funciones

```meta
tipo: tema
padre: R01-N07
precio: 10
criatura: skeleton
temas: prog.funciones, prog.alcance, cal.tipos
```

### Crónica

En la torre del Puerto, cada tarea tiene su oficina: una pesa, otra calcula tarifas, otra escribe etiquetas. Cuando un barco necesita algo, no se lo explican de nuevo a nadie: se le pide a la oficina que corresponde, se le dan los datos y ella devuelve el resultado.

—Eso es una **función** —dice {mentor}—. Un pedazo de código con nombre, que recibe datos y devuelve una respuesta. La escribís una vez y la usás mil. Y cuando algo falla, {heroe}, sabés exactamente en qué oficina buscar.

### Objetivos

- Definir funciones con parámetros y valor de retorno.
- Declarar los tipos de los parámetros y del retorno, y activar `strict_types`.
- Usar valores por defecto, argumentos con nombre y parámetros variádicos.
- Entender el alcance de las variables y el paso por referencia.
- Escribir funciones anónimas y flechas (`fn`), y usarlas con `array_map` y `usort`.
- Escribir funciones recursivas.

### Antes de empezar

- Arrays y sus funciones (R01-N07).

### Explicación

#### Definir y llamar
```php
function saludar(string $nombre): string
{
    return "Hola, $nombre";
}

echo saludar("Kira");   // Hola, Kira
```
- `string $nombre` es un **parámetro** con su tipo.
- `: string` es el tipo de lo que **devuelve**.
- `return` termina la función y devuelve el valor.
- Una función que no devuelve nada se declara `: void`.

Las funciones se pueden llamar antes o después de definirlas en el archivo.

#### Tipos en la firma y `strict_types`
Sin más, PHP **convierte** los argumentos si puede: `cajones("1000")` convierte el
texto `"1000"` en el entero `1000`. Con esta línea al principio del archivo:
```php
<?php
declare(strict_types=1);
```
PHP no convierte: si la función pide `int` y le das un texto, da un error claro:
```
cajones(): Argument #1 ($kilos) must be of type int, string given, called in carga.php on line 16
```
Es la forma de tener a los **goblins** bajo control. Desde acá, los programas del
Puerto usan `strict_types`.

Tipos que se pueden declarar: `int`, `float`, `string`, `bool`, `array`, `void`,
`mixed` (cualquiera), `?int` (un `int` o `null`) e `int|string` (uno u otro).

#### Valores por defecto y argumentos con nombre
```php
function cajones(int $kilos, int $porCajon = 40): int
{
    return intdiv($kilos, $porCajon);
}
cajones(1000);                          // 25   (usa 40)
cajones(1000, 50);                      // 20
cajones(porCajon: 50, kilos: 1000);     // 20   (con nombre, en cualquier orden)
```

#### Variádicas: cualquier cantidad de argumentos
```php
function sumar(int ...$numeros): int
{
    return array_sum($numeros);   // $numeros es un array
}
sumar(1, 2, 3);   // 6
```

#### Alcance: cada función tiene sus variables
Una función **no ve** las variables de afuera, y las de adentro desaparecen al
terminar:
```php
$iva = 0.21;
function conIva(float $precio): float
{
    return $precio * (1 + $iva);   // Warning: Undefined variable $iva
}
```
Lo que la función necesita, se lo pasás **por parámetro** (o es una constante).
Existe `global $iva;`, pero en el Puerto **no se usa**: hace el código difícil de
seguir.

#### Por valor y por referencia
Los parámetros se reciben **por valor**: la función trabaja con una copia. Con `&`
se recibe **por referencia** y los cambios se ven afuera:
```php
function agregar(array &$lista, string $item): void
{
    $lista[] = $item;
}
$carga = [];
agregar($carga, "cartas");   // ahora $carga tiene 1 elemento
```
Se usa poco: devolver un valor nuevo suele ser más claro.

#### Funciones anónimas y flechas
Una función sin nombre se puede guardar en una variable o pasar a otra función:
```php
$doble = fn(int $x): int => $x * 2;         // flecha: una sola expresión
echo $doble(4);                             // 8

$factor = 3;
$triple = function (int $x) use ($factor): int {   // use: trae $factor de afuera
    return $x * $factor;
};
```
Las `fn` ven automáticamente las variables de afuera; las `function` anónimas
necesitan `use`. Son las que le pasás a `array_map`, `array_filter` y `usort`.

#### Recursión
Una función que se llama a sí misma, con un caso que corta:
```php
function factorial(int $n): int
{
    return $n <= 1 ? 1 : $n * factorial($n - 1);
}
```

#### Cómo escribir buenas funciones
- Un nombre que diga qué hace: `calcularEnvio`, `esBisiesto`, `formatearPrecio`.
- Hace **una** cosa. Si hace tres, son tres funciones.
- Recibe todo por parámetro y **devuelve** el resultado: no muestra con `echo`
  adentro (así se puede usar en la terminal y en una página web).
- Documentala con un comentario `/** … */` arriba.

### Código de ejemplo

```php
<?php
declare(strict_types=1);
/*
 * Las oficinas de la torre: funciones con tipos, valores por defecto y flechas.
 */

/** Cuántos cajones llenos salen de tantos kilos. */
function cajones(int $kilos, int $porCajon = 40): int
{
    return intdiv($kilos, $porCajon);
}

/** El precio con IVA, redondeado a 2 decimales. */
function conIva(float $precio, float $iva = 0.21): float
{
    return round($precio * (1 + $iva), 2);
}

/** Un precio escrito a la argentina. */
function pesos(float $monto): string
{
    return "$" . number_format($monto, 2, ',', '.');
}

/** ¿El año es bisiesto? */
function esBisiesto(int $anio): bool
{
    return ($anio % 4 === 0 && $anio % 100 !== 0) || $anio % 400 === 0;
}

/** Suma cualquier cantidad de pesos. */
function pesoTotal(float ...$pesos): float
{
    return array_sum($pesos);
}

/** Rellena a la derecha contando letras (no bytes), para tablas con tildes. */
function rellenar(string $texto, int $ancho): string
{
    return $texto . str_repeat(" ", max(0, $ancho - mb_strlen($texto)));
}

/** Suma de 1 a n, con recursión. */
function sumaHasta(int $n): int
{
    return $n <= 0 ? 0 : $n + sumaHasta($n - 1);
}

echo "Cajones: ", cajones(1000), " de 40 / ", cajones(porCajon: 50, kilos: 1000), " de 50\n";
echo "Con IVA: ", pesos(conIva(15000)), "\n";
echo "Con IVA reducido: ", pesos(conIva(15000, iva: 0.105)), "\n";
echo "2024 es bisiesto: ", esBisiesto(2024) ? "sí" : "no", "\n";
echo "Peso total: ", pesoTotal(12.5, 30, 7.25), " kg\n";
echo "Suma de 1 a 10: ", sumaHasta(10), "\n";

// Flechas con funciones de arrays
$precios = ["mate" => 450, "té" => 400, "café" => 900];
$conIva = array_map(fn(int $p): float => conIva($p), $precios);
foreach ($conIva as $producto => $precio) {
    echo rellenar($producto, 6), "|", pesos($precio), "\n";
}

// strict_types: un texto donde va un int (try/catch se ve en el nodo de excepciones)
try {
    cajones("1000");
} catch (TypeError $e) {
    echo "Error: ", explode(", called", $e->getMessage())[0], "\n";
}
```

### Salida esperada

```
Cajones: 25 de 40 / 20 de 50
Con IVA: $18.150,00
Con IVA reducido: $16.575,00
2024 es bisiesto: sí
Peso total: 49.75 kg
Suma de 1 a 10: 55
mate  |$544,50
té    |$484,00
café  |$1.089,00
Error: cajones(): Argument #1 ($kilos) must be of type int, string given
```

### ¿Para qué sirve?

Un sistema real tiene cientos de funciones: `calcularTotal`, `validarEmail`, `formatearFecha`, `enviarMail`. Separar el código en funciones chicas y con tipos es lo que permite probarlo, reusarlo entre la terminal y la web, y encontrar los errores rápido. Todos los frameworks, empezando por Laravel, están hechos de funciones y métodos así.

### Errores habituales

**Esqueleto: la función que no existe.**
```
PHP Fatal error:  Uncaught Error: Call to undefined function saludar()
```
El nombre está mal escrito o la función está en otro archivo que no incluiste.

**Esqueleto: la variable de afuera.** Adentro de la función, `$iva` no existe si no
la pasaste por parámetro: `Warning: Undefined variable $iva`.

**Goblin: el tipo equivocado con `strict_types`.**
`Argument #1 ($kilos) must be of type int, string given`: convertí el dato antes de
llamar (o validalo).

**Ogro: `echo` en lugar de `return`.** Si la función muestra el resultado en lugar de
devolverlo, `$total = calcular(…)` queda en `null`.

**Ogro: la recursión sin final.** Si falta el caso que corta, la función se llama
para siempre hasta `Maximum function nesting level` o `Allowed memory size
exhausted`.

### Misión R01-N08-M1 · Las oficinas de la torre

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí estas funciones, con tipos en los parámetros y en el retorno, y
`strict_types`:

1. `areaRectangulo(float $ancho, float $alto): float`.
2. `precioFinal(float $precio, float $descuento = 0): float` — el descuento es un
   porcentaje (`10` es 10%).
3. `esPar(int $n): bool`.
4. `iniciales(string $nombreCompleto): string` — `"kira valdez"` → `"K.V."`
   (usá `explode`, `mb_substr` y `mb_strtoupper`).
5. `promedio(float ...$numeros): float` — si no hay números, devuelve `0`.

Mostrá el resultado de llamar a cada una con los datos del ejemplo.

#### Criterio de aprobación

- Las cinco funciones tienen tipos y `return` (no hacen `echo` adentro).
- Usa un valor por defecto y un parámetro variádico.
- La salida coincide con la esperada.

#### Salida esperada

```
Área: 9
Precio sin descuento: 12000
Precio con 15%: 10200
¿7 es par? no
Iniciales: K.V. / É.D.L.F.
Promedio: 8.17
Promedio vacío: 0
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 1 - Las oficinas de la torre: cinco funciones con tipos.

function areaRectangulo(float $ancho, float $alto): float
{
    return $ancho * $alto;
}

function precioFinal(float $precio, float $descuento = 0): float
{
    return $precio * (1 - $descuento / 100);
}

function esPar(int $n): bool
{
    return $n % 2 === 0;
}

function iniciales(string $nombreCompleto): string
{
    $resultado = "";
    foreach (explode(" ", trim($nombreCompleto)) as $parte) {
        if ($parte !== "") {
            $resultado .= mb_strtoupper(mb_substr($parte, 0, 1)) . ".";
        }
    }
    return $resultado;
}

function promedio(float ...$numeros): float
{
    return count($numeros) === 0 ? 0 : array_sum($numeros) / count($numeros);
}

echo "Área: ", areaRectangulo(4.5, 2), "\n";
echo "Precio sin descuento: ", precioFinal(12000), "\n";
echo "Precio con 15%: ", precioFinal(12000, 15), "\n";
echo "¿7 es par? ", esPar(7) ? "sí" : "no", "\n";
echo "Iniciales: ", iniciales("kira valdez"), " / ", iniciales("émile  de las forjas"), "\n";
echo "Promedio: ", round(promedio(8, 9.5, 7), 2), "\n";
echo "Promedio vacío: ", promedio(), "\n";
```

### Misión R01-N08-M2 · El conversor del cambista

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El cambista del puerto convierte entre monedas del mundo. Guardá las
cotizaciones en una constante con un array (`const COTIZACIONES = ["denario" =>
1250.0, …]`: cuántos pesos vale cada moneda): `denario` 1250, `lingote` 3400,
`escama` 820, `engranaje` 2100.

Escribí:

- `aPesos(float $cantidad, string $moneda): float` — si la moneda no existe,
  devuelve `-1`;
- `convertir(float $cantidad, string $de, string $a): float` — usa `aPesos` y
  divide por la cotización de destino; redondea a 2 decimales;
- `mostrarCambio(float $cantidad, string $de, string $a): string` — devuelve el
  texto `"10 denarios = 3,68 lingotes"` (con `number_format` y una `s` si la
  cantidad no es 1).

Mostrá tres cambios del ejemplo y un intento con una moneda que no existe
(`"perla"`), que tiene que mostrar `Moneda desconocida: perla`.

#### Criterio de aprobación

- Las cotizaciones son una constante array.
- `convertir` reusa `aPesos`.
- Ninguna función hace `echo` salvo el programa principal.
- La salida coincide con la esperada.

#### Salida esperada

```
10 denarios = 3,68 lingotes
1 lingote = 4,15 escamas
250 escamas = 97,62 engranajes
Moneda desconocida: perla
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 2 - El conversor del cambista: funciones que se llaman entre sí.
const COTIZACIONES = ["denario" => 1250.0, "lingote" => 3400.0, "escama" => 820.0, "engranaje" => 2100.0];

function aPesos(float $cantidad, string $moneda): float
{
    if (!isset(COTIZACIONES[$moneda])) {
        return -1;
    }
    return $cantidad * COTIZACIONES[$moneda];
}

function convertir(float $cantidad, string $de, string $a): float
{
    $pesos = aPesos($cantidad, $de);
    if ($pesos < 0 || !isset(COTIZACIONES[$a])) {
        return -1;
    }
    return round($pesos / COTIZACIONES[$a], 2);
}

function nombreMoneda(string $moneda, float $cantidad): string
{
    return $cantidad == 1 ? $moneda : $moneda . "s";
}

function mostrarCambio(float $cantidad, string $de, string $a): string
{
    $resultado = convertir($cantidad, $de, $a);
    if ($resultado < 0) {
        $desconocida = isset(COTIZACIONES[$de]) ? $a : $de;
        return "Moneda desconocida: $desconocida";
    }
    return number_format($cantidad, 0, ',', '.') . " " . nombreMoneda($de, $cantidad)
        . " = " . number_format($resultado, 2, ',', '.') . " " . nombreMoneda($a, $resultado);
}

echo mostrarCambio(10, "denario", "lingote"), "\n";
echo mostrarCambio(1, "lingote", "escama"), "\n";
echo mostrarCambio(250, "escama", "engranaje"), "\n";
echo mostrarCambio(5, "perla", "denario"), "\n";
```

### Misión R01-N08-M3 · La escalera del faro

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La escalera del faro tiene `n` escalones y el farero puede subir **de a 1 o de a
2**. ¿De cuántas maneras distintas puede llegar arriba? Para 1 escalón hay 1
manera, para 2 hay 2, y para `n` es la suma de las maneras para `n - 1` y para
`n - 2`.

1. Escribí `maneras(int $n): int` **recursiva**.
2. Esa versión se pone lentísima con `n` grande porque calcula lo mismo muchas
   veces. Escribí `manerasRapido(int $n): int` que guarde lo ya calculado en un
   array `static $memoria = [];` adentro de la función (una variable `static`
   conserva su valor entre llamadas).
3. Mostrá las maneras para 1, 2, 3, 10 y 20 escalones con las dos, y para 80
   escalones solo con la rápida.

#### Criterio de aprobación

- `maneras` es recursiva, con los casos base.
- `manerasRapido` usa un array `static` como memoria.
- La salida coincide con la esperada.

#### Salida esperada

```
 1 escalones: 1 / 1
 2 escalones: 2 / 2
 3 escalones: 3 / 3
10 escalones: 89 / 89
20 escalones: 10946 / 10946
80 escalones: 37889062373143906
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - La escalera del faro: recursión y memoria con static.

function maneras(int $n): int
{
    if ($n <= 2) {
        return $n;
    }
    return maneras($n - 1) + maneras($n - 2);
}

function manerasRapido(int $n): int
{
    static $memoria = [];
    if ($n <= 2) {
        return $n;
    }
    if (!isset($memoria[$n])) {
        $memoria[$n] = manerasRapido($n - 1) + manerasRapido($n - 2);
    }
    return $memoria[$n];
}

foreach ([1, 2, 3, 10, 20] as $escalones) {
    printf("%2d escalones: %d / %d\n", $escalones, maneras($escalones), manerasRapido($escalones));
}
echo "80 escalones: ", manerasRapido(80), "\n";
```

### Encargo R01-N08-E1 · La validación del CUIT

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Todo sistema de facturación argentino valida el **CUIT** antes de guardarlo. Un
CUIT tiene 11 dígitos (se escribe `20-12345678-6`) y el último es un **dígito
verificador** que se calcula así:

1. Se multiplican los primeros 10 dígitos por `5, 4, 3, 2, 7, 6, 5, 4, 3, 2`
   (en ese orden) y se suman los productos.
2. Se calcula `11 - (suma % 11)`. Si da 11, el verificador es 0; si da 10, el
   CUIT es inválido; si no, ese es el verificador.

Escribí:

- `limpiarCuit(string $cuit): string` — saca guiones y espacios;
- `digitoVerificador(string $diez): int` — devuelve el verificador de los primeros
  10 dígitos (o `-1` si da 10);
- `cuitValido(string $cuit): bool` — limpia, revisa que tenga 11 dígitos (con
  `ctype_digit`) y compara el verificador;
- `formatearCuit(string $cuit): string` — `"20123456786"` → `"20-12345678-6"`.

Leé CUITs de la entrada (uno por renglón, hasta el final) y mostrá cada uno
formateado con `válido` o `inválido`.

#### Criterio de aprobación

- Cada paso es una función con tipos, sin `echo` adentro.
- Usa `strict_types`.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
20-12345678-6
27 25123456 3
30-71234567-1
2012345678
20-1234567A-6
```

#### Salida esperada

```
20-12345678-6  válido
27-25123456-3  inválido
30-71234567-1  válido
2012345678     inválido
20-1234567A-6  inválido
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Encargo - La validación del CUIT: dígito verificador con funciones.
const PESOS_CUIT = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2];

function limpiarCuit(string $cuit): string
{
    return str_replace(["-", " "], "", trim($cuit));
}

function digitoVerificador(string $diez): int
{
    $suma = 0;
    for ($i = 0; $i < 10; $i++) {
        $suma += (int) $diez[$i] * PESOS_CUIT[$i];
    }
    $resultado = 11 - ($suma % 11);
    return match ($resultado) {
        11 => 0,
        10 => -1,
        default => $resultado,
    };
}

function cuitValido(string $cuit): bool
{
    $limpio = limpiarCuit($cuit);
    if (strlen($limpio) !== 11 || !ctype_digit($limpio)) {
        return false;
    }
    return digitoVerificador(substr($limpio, 0, 10)) === (int) $limpio[10];
}

function formatearCuit(string $cuit): string
{
    $limpio = limpiarCuit($cuit);
    if (strlen($limpio) !== 11) {
        return $limpio;
    }
    return substr($limpio, 0, 2) . "-" . substr($limpio, 2, 8) . "-" . substr($limpio, 10);
}

while (($linea = fgets(STDIN)) !== false) {
    if (trim($linea) === "") {
        continue;
    }
    printf("%-14s %s\n", formatearCuit($linea), cuitValido($linea) ? "válido" : "inválido");
}
```

### Prueba del sello

#### ¿Qué hace `declare(strict_types=1)`?

Hace que PHP no convierta los argumentos: si una función pide `int` y recibe un texto, da un `TypeError` en lugar de convertir.

#### ¿Una función ve las variables definidas afuera de ella?

No. Lo que necesita se le pasa por parámetro (o es una constante).

#### ¿Qué significa `?int` como tipo de retorno?

Que la función devuelve un `int` o `null`.

#### ¿Qué diferencia hay entre una `fn` y una `function` anónima?

La `fn` es de una sola expresión y ve sola las variables de afuera; la `function` anónima puede tener varias líneas y necesita `use` para traer variables de afuera.

#### ¿Por qué conviene que una función devuelva con `return` en lugar de mostrar con `echo`?

Porque así el resultado se puede guardar, combinar y usar en cualquier lugar (la terminal o una página web); la función que muestra solo sirve para mostrar.

### Soluciones (docente)

Sale de `21-PHP/06-Funciones` y `14-Closures-Funcional` (la parte básica; closures y generadores vuelven en R05-N02). Desde este nodo se usa `strict_types`. La función `rellenar` del ejemplo resuelve el problema de las tildes en tablas (R01-N03) sin `mb_str_pad`, que es de PHP 8.3. En el encargo, `30-71234567-1` da válido por el cálculo aunque no sea de una empresa real (el verificador solo detecta errores de tipeo), y `27-25123456-3` muestra un verificador que no coincide.

## R01-N09 · Organizar el código: include y require

```meta
tipo: tema
padre: R01-N08
precio: 10
criatura: skeleton
temas: prog.modulos
```

### Crónica

La oficina de despacho del Puerto creció tanto que el libro de instrucciones ya no entra en un solo tomo. Ahora hay un estante: un tomo para las tarifas, otro para las etiquetas, otro con los datos de cada muelle. Cuando un empleado necesita algo, saca el tomo que corresponde.

—Un programa grande tampoco entra en un solo archivo —dice {mentor}—. Se reparte en varios, cada uno con lo suyo, y se los junta con `require`. Pero ojo, {heroe}: si pedís un tomo que no está en el estante, o traés el mismo dos veces, la oficina se traba.

### Objetivos

- Repartir un programa en varios archivos y juntarlos con `require` e `include`.
- Usar `require_once` para no cargar dos veces lo mismo.
- Armar las rutas con `__DIR__` para que funcionen desde cualquier carpeta.
- Guardar la configuración en un archivo que devuelve un array.
- Organizar un proyecto chico en carpetas.
- Depurar con `var_dump`, `print_r` y los mensajes de error.

### Antes de empezar

- Funciones con tipos (R01-N08).

### Explicación

#### Juntar archivos
`require 'archivo.php';` ejecuta ese archivo **en ese lugar**, como si su código
estuviera escrito ahí. Así se separan las funciones del programa principal:

`lib/tarifas.php`
```php
<?php
declare(strict_types=1);

function tarifa(float $kilos): float
{
    return $kilos * 350;
}
```

`main.php`
```php
<?php
declare(strict_types=1);
require __DIR__ . '/lib/tarifas.php';

echo tarifa(10), "\n";    // 3500
```

#### `require`, `include` y sus versiones `_once`
| Instrucción | Si el archivo no existe | Si ya se cargó antes |
|---|---|---|
| `require` | error fatal: el programa se corta | lo vuelve a cargar |
| `include` | un aviso, y sigue | lo vuelve a cargar |
| `require_once` | error fatal | no lo carga de nuevo |
| `include_once` | un aviso, y sigue | no lo carga de nuevo |

Para funciones y clases se usa **`require_once`**: cargar dos veces un archivo
con funciones da `Cannot redeclare f()`. `include` se usa para piezas opcionales
(en la web, por ejemplo, un pedacito de página).

#### Rutas con `__DIR__`
`require 'lib/tarifas.php'` busca a partir de la carpeta **desde donde ejecutaste**
el programa, no la del archivo. Si corrés `php proyecto/main.php` desde otra
carpeta, falla. **`__DIR__`** es la carpeta del archivo actual, así que
`__DIR__ . '/lib/tarifas.php'` funciona siempre.

Otras "constantes mágicas" útiles para depurar: `__FILE__` (el archivo actual) y
`__LINE__` (la línea actual).

#### Un archivo que devuelve algo
Un archivo incluido puede terminar con `return`, y `require` devuelve ese valor.
Es la forma clásica de guardar la **configuración**:

`config.php`
```php
<?php
return [
    'puerto' => 'Mensajeros',
    'iva' => 0.21,
    'tarifa_kg' => 350,
];
```
```php
$config = require __DIR__ . '/config.php';
echo $config['iva'];      // 0.21
```
Así la configuración (claves, datos de la base, precios) queda en un solo lugar y
no se mezcla con el código.

#### Cómo repartir un proyecto
Una estructura chica y ordenada:
```
despacho/
├── main.php            ← el programa: lee, llama funciones y muestra
├── config.php          ← los datos que cambian (precios, nombres)
└── lib/
    ├── tarifas.php     ← funciones de cálculo
    └── formato.php     ← funciones para mostrar (pesos, tablas)
```
Regla: **los archivos de `lib/` solo definen funciones**; no muestran nada ni leen
del teclado. Todo eso lo hace `main.php`.

#### Depurar: encontrar dónde está el problema
- `var_dump($x)` en el lugar sospechoso: muestra tipo y valor.
- `print_r($array)`: un array legible.
- `var_dump($x); exit;`: mirá el valor y cortá ahí.
- Leé **siempre** el mensaje de error completo: archivo y línea.
- Para ver todos los avisos (en tu compu, no en un servidor público), al
  principio del programa: `error_reporting(E_ALL); ini_set('display_errors', '1');`

### Código de ejemplo

`config.php`
```php
<?php
// Los datos que cambian: precios y nombres.
return [
    'oficina' => 'Despacho del Muelle 3',
    'tarifa_kg' => 350,
    'recargo_urgente' => 0.5,
];
```

`lib/tarifas.php`
```php
<?php
declare(strict_types=1);
// Funciones de cálculo: no muestran nada.

function costoEnvio(float $kilos, bool $urgente, array $config): float
{
    $costo = $kilos * $config['tarifa_kg'];
    return $urgente ? $costo * (1 + $config['recargo_urgente']) : $costo;
}
```

`lib/formato.php`
```php
<?php
declare(strict_types=1);
// Funciones para mostrar.

function pesos(float $monto): string
{
    return '$' . number_format($monto, 2, ',', '.');
}

function renglon(string $texto, string $valor, int $ancho = 24): string
{
    return $texto . str_repeat('.', max(1, $ancho - mb_strlen($texto) - mb_strlen($valor))) . $valor;
}
```

`main.php`
```php
<?php
declare(strict_types=1);
require_once __DIR__ . '/lib/tarifas.php';
require_once __DIR__ . '/lib/formato.php';
require_once __DIR__ . '/lib/formato.php';     // _once: no pasa nada si se repite

$config = require __DIR__ . '/config.php';

$envios = [
    ['destino' => 'Valle', 'kilos' => 2.5, 'urgente' => false],
    ['destino' => 'Forjas', 'kilos' => 12.0, 'urgente' => true],
    ['destino' => 'Imperio', 'kilos' => 0.8, 'urgente' => false],
];

echo $config['oficina'], "\n";
$total = 0;
foreach ($envios as $envio) {
    $costo = costoEnvio($envio['kilos'], $envio['urgente'], $config);
    $total += $costo;
    echo renglon($envio['destino'] . ($envio['urgente'] ? ' (urgente)' : ''), pesos($costo)), "\n";
}
echo renglon('TOTAL', pesos($total)), "\n";
echo "(generado por ", basename(__FILE__), ")\n";
```

### Salida esperada

```
Despacho del Muelle 3
Valle............$875,00
Forjas (urgente).$6.300,00
Imperio..........$280,00
TOTAL..........$7.455,00
(generado por main.php)
```

### ¿Para qué sirve?

Ningún sistema real es un solo archivo: WordPress tiene miles, y Laravel, decenas de carpetas. Separar la configuración, las funciones y el programa principal es el primer paso hacia esa organización; en la rama de objetos vas a ver cómo PHP carga los archivos solo (*autoload*) y cómo se usan bibliotecas de otros con Composer.

### Errores habituales

**Esqueleto: el archivo que no está.**
```
PHP Warning:  require(lib/tarifas.php): Failed to open stream: No such file or directory in main.php on line 3
PHP Fatal error:  Uncaught Error: Failed opening required 'lib/tarifas.php'
```
Revisá el nombre y usá `__DIR__` en la ruta.

**Slime: cargar dos veces.**
```
PHP Fatal error:  Cannot redeclare costoEnvio() (previously declared in lib/tarifas.php:5)
```
Usá `require_once` para los archivos con funciones.

**Ogro: la ruta relativa.** Funciona cuando ejecutás desde la carpeta del proyecto
y falla desde otra. Siempre `__DIR__ . '/…'`.

**Ogro: el `echo` escondido en la biblioteca.** Si `lib/tarifas.php` muestra algo al
cargarse, aparece texto de más en cualquier programa que lo use (y en la web rompe
las páginas). Las bibliotecas solo definen funciones.

**Goblin: olvidarse el `return` de la configuración.** Si `config.php` no termina con
`return [...]`, `require` devuelve `1` y `$config['iva']` da
`Trying to access array offset on value of type int`.

### Misión R01-N09-M1 · La biblioteca de medidas

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá un proyecto con esta estructura y entregalo comprimido en `.zip`:

```
medidas/
├── main.php
└── lib/
    ├── longitudes.php   ← millasAKm, kmAMillas, piesAMetros
    └── pesos.php        ← librasAKg, kgALibras
```

(1 milla náutica = 1.852 km; 1 pie = 0.3048 m; 1 libra = 0.4536 kg.) Todas las
funciones con tipos y `strict_types`, redondeando a 2 decimales. `main.php` carga
las bibliotecas con `require_once` y `__DIR__` y muestra la tabla de conversiones
del ejemplo.

#### Criterio de aprobación

- Las funciones están en `lib/` y no muestran nada.
- `main.php` usa `require_once __DIR__ . …`.
- La salida coincide con la esperada.

#### Salida esperada

```
120 millas = 222.24 km
500 km = 269.98 millas
35 pies = 10.67 m
220 libras = 99.79 kg
75 kg = 165.34 libras
```

#### Solución de referencia

`lib/longitudes.php`
```php
<?php
declare(strict_types=1);

const KM_POR_MILLA = 1.852;
const METROS_POR_PIE = 0.3048;

function millasAKm(float $millas): float
{
    return round($millas * KM_POR_MILLA, 2);
}

function kmAMillas(float $km): float
{
    return round($km / KM_POR_MILLA, 2);
}

function piesAMetros(float $pies): float
{
    return round($pies * METROS_POR_PIE, 2);
}
```

`lib/pesos.php`
```php
<?php
declare(strict_types=1);

const KG_POR_LIBRA = 0.4536;

function librasAKg(float $libras): float
{
    return round($libras * KG_POR_LIBRA, 2);
}

function kgALibras(float $kg): float
{
    return round($kg / KG_POR_LIBRA, 2);
}
```

`main.php`
```php
<?php
declare(strict_types=1);
// Mision 1 - La biblioteca de medidas: funciones repartidas en archivos.
require_once __DIR__ . '/lib/longitudes.php';
require_once __DIR__ . '/lib/pesos.php';

echo "120 millas = ", millasAKm(120), " km\n";
echo "500 km = ", kmAMillas(500), " millas\n";
echo "35 pies = ", piesAMetros(35), " m\n";
echo "220 libras = ", librasAKg(220), " kg\n";
echo "75 kg = ", kgALibras(75), " libras\n";
```

### Misión R01-N09-M2 · La configuración del faro

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

El faro enciende su luz según una configuración. Armá:

- `config.php`, que devuelve un array con: `nombre` (`"Faro del Cabo"`),
  `hora_encendido` (19), `hora_apagado` (7), `destellos_por_minuto` (12) y
  `alcance_millas` (18);
- `lib/faro.php`, con `estaEncendido(int $hora, array $config): bool` (ojo: el
  horario **cruza la medianoche**: de 19 a 7) y
  `destellos(int $minutos, array $config): int`;
- `main.php`, que carga todo y muestra, para las horas 6, 7, 12, 19 y 23, si el
  faro está encendido, y cuántos destellos hace en una noche completa (de 19 a 7).

#### Criterio de aprobación

- `config.php` termina con `return [...]` y `main.php` lo recibe con `$config = require …`.
- `estaEncendido` resuelve el horario que cruza la medianoche.
- La salida coincide con la esperada.

#### Salida esperada

```
Faro del Cabo (alcance: 18 millas)
06:00 → encendido
07:00 → apagado
12:00 → apagado
19:00 → encendido
23:00 → encendido
Destellos por noche: 8640
```

#### Solución de referencia

`config.php`
```php
<?php
return [
    'nombre' => 'Faro del Cabo',
    'hora_encendido' => 19,
    'hora_apagado' => 7,
    'destellos_por_minuto' => 12,
    'alcance_millas' => 18,
];
```

`lib/faro.php`
```php
<?php
declare(strict_types=1);

function estaEncendido(int $hora, array $config): bool
{
    $desde = $config['hora_encendido'];
    $hasta = $config['hora_apagado'];
    if ($desde < $hasta) {
        return $hora >= $desde && $hora < $hasta;
    }
    return $hora >= $desde || $hora < $hasta;   // cruza la medianoche
}

function destellos(int $minutos, array $config): int
{
    return $minutos * $config['destellos_por_minuto'];
}
```

`main.php`
```php
<?php
declare(strict_types=1);
// Mision 2 - La configuración del faro: un archivo que devuelve un array.
require_once __DIR__ . '/lib/faro.php';
$config = require __DIR__ . '/config.php';

echo $config['nombre'], " (alcance: ", $config['alcance_millas'], " millas)\n";
foreach ([6, 7, 12, 19, 23] as $hora) {
    echo str_pad((string) $hora, 2, "0", STR_PAD_LEFT), ":00 → ", estaEncendido($hora, $config) ? "encendido" : "apagado", "\n";
}
$horasDeNoche = (24 - $config['hora_encendido']) + $config['hora_apagado'];
echo "Destellos por noche: ", destellos($horasDeNoche * 60, $config), "\n";
```

### Misión R01-N09-M3 · La caza del esqueleto

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Este programa tiene **cuatro errores** que lo hacen fallar o mostrar resultados
equivocados (no hace falta separarlo en archivos). Ejecutalo, leé cada mensaje,
usá `var_dump` donde haga falta y corregilo hasta que muestre la salida esperada.
En tu entrega, agregá un comentario arriba de cada corrección explicando qué
estaba mal.

#### Criterio de aprobación

- Corrige los cuatro errores sin cambiar los textos.
- Cada corrección tiene un comentario que explica qué estaba mal.
- La salida coincide con la esperada.

#### Código inicial

```php
<?php
declare(strict_types=1);

function promedioDeCargas(array $cargas): float
{
    $total = 0;
    foreach ($cargas as $carga) {
        $total = $carga;
    }
    return $total / count($carga);
}

$barcos = ["Gaviota" => 450, "Albatros" => 1200, "Tortuga" => 80];
echo "Promedio: ", promedioDeCarga($barcos), " kg\n";
echo "El Albatros lleva: ", $barcos["albatros"], " kg\n";
```

#### Salida esperada

```
Promedio: 576.67 kg
El Albatros lleva: 1200 kg
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Mision 3 - La caza del esqueleto: cuatro errores corregidos.

function promedioDeCargas(array $cargas): float
{
    $total = 0;
    foreach ($cargas as $carga) {
        // 1. Era $total = $carga: pisaba el total en cada vuelta en lugar de sumar.
        $total += $carga;
    }
    // 2. Era count($carga) (una sola carga): hay que contar el array $cargas.
    return $total / count($cargas);
}

$barcos = ["Gaviota" => 450, "Albatros" => 1200, "Tortuga" => 80];
// 3. La función se llama promedioDeCargas (con s): Call to undefined function.
echo "Promedio: ", round(promedioDeCargas($barcos), 2), " kg\n";
// 4. Las claves distinguen mayúsculas: "albatros" no existe, es "Albatros".
echo "El Albatros lleva: ", $barcos["Albatros"], " kg\n";
```

### Encargo R01-N09-E1 · El sistema de turnos del consultorio

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Un consultorio del barrio necesita un sistema de turnos por terminal. Armá un
proyecto en varios archivos:

- `config.php`: el nombre del consultorio, la duración de cada turno (20 minutos),
  la hora de inicio (`"09:00"`) y la cantidad de turnos por día (8);
- `lib/horarios.php`: `horaDelTurno(int $numero, array $config): string` (el turno
  1 es a las 09:00, el 2 a las 09:20…; usá minutos, `intdiv` y `%`);
- `lib/turnos.php`: `reservar(array $turnos, int $numero, string $paciente, array
  $config): array` que devuelve el array actualizado, o el mismo si el turno no
  existe o ya está ocupado (y muestra el motivo en `main.php`, no adentro);
- `main.php`: lee pedidos del teclado con el formato `NUMERO;PACIENTE` hasta el
  final de la entrada, reserva y al final muestra la agenda completa del día con
  `libre` en los turnos sin reservar.

#### Criterio de aprobación

- El proyecto está repartido en archivos con `require_once __DIR__`.
- Las funciones de `lib/` no muestran nada y devuelven valores.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
3;Ana Pérez
1;Bruno Díaz
3;Carla Gómez
12;Diego Ruiz
8;Elena Sosa
```

#### Salida esperada

```
Reservado: turno 3 (09:40) para Ana Pérez.
Reservado: turno 1 (09:00) para Bruno Díaz.
El turno 3 ya es de Ana Pérez.
El turno 12 no existe.
Reservado: turno 8 (11:20) para Elena Sosa.

Consultorio Dra. Molina
09:00  Bruno Díaz
09:20  libre
09:40  Ana Pérez
10:00  libre
10:20  libre
10:40  libre
11:00  libre
11:20  Elena Sosa
```

#### Solución de referencia

`config.php`
```php
<?php
return [
    'consultorio' => 'Consultorio Dra. Molina',
    'duracion' => 20,
    'inicio' => '09:00',
    'turnos_por_dia' => 8,
];
```

`lib/horarios.php`
```php
<?php
declare(strict_types=1);

function horaDelTurno(int $numero, array $config): string
{
    [$h, $m] = explode(':', $config['inicio']);
    $minutos = (int) $h * 60 + (int) $m + ($numero - 1) * $config['duracion'];
    return sprintf('%02d:%02d', intdiv($minutos, 60), $minutos % 60);
}
```

`lib/turnos.php`
```php
<?php
declare(strict_types=1);

function turnoExiste(int $numero, array $config): bool
{
    return $numero >= 1 && $numero <= $config['turnos_por_dia'];
}

function reservar(array $turnos, int $numero, string $paciente, array $config): array
{
    if (!turnoExiste($numero, $config) || isset($turnos[$numero])) {
        return $turnos;
    }
    $turnos[$numero] = $paciente;
    return $turnos;
}
```

`main.php`
```php
<?php
declare(strict_types=1);
// Encargo - El sistema de turnos del consultorio: un proyecto en varios archivos.
require_once __DIR__ . '/lib/horarios.php';
require_once __DIR__ . '/lib/turnos.php';
$config = require __DIR__ . '/config.php';

$turnos = [];
while (($linea = fgets(STDIN)) !== false) {
    if (trim($linea) === '') {
        continue;
    }
    [$numero, $paciente] = explode(';', trim($linea));
    $numero = (int) $numero;
    if (!turnoExiste($numero, $config)) {
        echo "El turno $numero no existe.\n";
        continue;
    }
    if (isset($turnos[$numero])) {
        echo "El turno $numero ya es de {$turnos[$numero]}.\n";
        continue;
    }
    $turnos = reservar($turnos, $numero, $paciente, $config);
    echo "Reservado: turno $numero (", horaDelTurno($numero, $config), ") para $paciente.\n";
}

echo "\n", $config['consultorio'], "\n";
for ($n = 1; $n <= $config['turnos_por_dia']; $n++) {
    echo horaDelTurno($n, $config), "  ", $turnos[$n] ?? 'libre', "\n";
}
```

### Prueba del sello

#### ¿Qué diferencia hay entre `require` e `include` cuando el archivo no existe?

`require` corta el programa con un error fatal; `include` muestra un aviso y sigue.

#### ¿Para qué sirve `require_once`?

Para cargar un archivo una sola vez: si ya se cargó, no lo vuelve a cargar (evita `Cannot redeclare`).

#### ¿Por qué se escribe `__DIR__ . '/lib/archivo.php'`?

Porque `__DIR__` es la carpeta del archivo actual, así la ruta funciona sin importar desde qué carpeta se ejecute el programa.

#### ¿Cómo se lee un archivo de configuración que termina con `return [...]`?

Guardando lo que devuelve `require`: `$config = require __DIR__ . '/config.php';`.

#### ¿Por qué las bibliotecas no deberían tener `echo`?

Porque se ejecutan al cargarse y agregarían texto de más en cualquier programa (o página web) que las use: solo deberían definir funciones.

### Soluciones (docente)

Sale de `21-PHP/08-Includes-Organizacion`, ampliado con la configuración que devuelve un array (el patrón que después usan PDO y Laravel) y una sección de depuración. Las misiones 1, 2 y el encargo se entregan en `.zip`. En la misión 3, los cuatro errores son: `=` en lugar de `+=`, `count($carga)`, el nombre `promedioDeCarga` y la clave `"albatros"`.

## R01-N10 · Jefe: la Sirena de los Tipos Débiles

```meta
tipo: jefe
padre: R01-N09
precio: 10
criatura: dragon
insignia: Sello de la Sirena
insignia_descripcion: Venciste a la Sirena de los Tipos Débiles: dominás los fundamentos de PHP.
usa: prog.funciones, col.mapas, err.validacion
```

### Crónica

Al final del Muelle de las Primeras Cartas, sobre una roca cubierta de algas, canta la **Sirena de los Tipos Débiles**. Su canción es dulce y engañosa: *"el texto «10» es el número 10… el cero es lo mismo que nada… lo que falta no importa…"*. Los barcos que le creen terminan contra las rocas, con las cuentas mal hechas y los registros perdidos.

—No le tapes los oídos —dice {mentor}—. Escuchala y demostrale que sabés la verdad: qué tipo tiene cada dato, cuándo `==` miente, qué pasa con una clave que no existe. Con todo lo que aprendiste en este muelle, {heroe}, podés construir algo que ella no pueda engañar.

### Objetivos

- Integrar todo lo de la rama: variables, textos, entrada, decisiones, bucles, arrays y funciones.
- Validar datos de entrada sin dejar pasar conversiones silenciosas.
- Organizar un programa mediano en funciones y archivos.

### Antes de empezar

- Todos los nodos del Muelle de las Primeras Cartas (R01-N01 a R01-N09).

### Explicación

#### Cómo encarar un proyecto
1. **Leé la consigna entera** y anotá qué entra (los datos) y qué sale (lo que se
   muestra).
2. **Separá en funciones** chicas: una lee, otra valida, otra calcula, otra
   formatea. Cada una con tipos.
3. **Empezá por lo más simple**: que lea un renglón y lo muestre. Después agregá
   de a una función y probá en cada paso.
4. **Probá con la entrada de ejemplo** redirigida (`php main.php < entrada.txt`) y
   compará con la salida esperada.
5. **Probá los casos raros**: un renglón vacío, un número con letras, una clave que
   no está. La Sirena ataca por ahí.

#### Las mentiras de la Sirena (y la verdad)
| La Sirena canta… | La verdad |
|---|---|
| "«10» es 10" | es un texto; convertilo a propósito, después de validarlo |
| "`==` alcanza" | `===` compara tipo y valor |
| "`(int) \"12abc\"` es 12, ¡perfecto!" | es un dato inválido que pasó en silencio: validá con `filter_var` |
| "si la clave no está, da igual" | `Undefined array key`: usá `??` o `isset` |
| "`\"0\"` es un valor" | para `if` es falso: compará con `=== ""` si querés saber si está vacío |

### Misión R01-N10-M1 · El libro de bitácora

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

La Sirena mezcló los registros del libro de bitácora del Puerto. Cada renglón de
la entrada tiene `BARCO;FECHA;KILOS;PASAJEROS`, pero hay renglones mal escritos.
Escribí un programa (en un solo archivo, con `strict_types` y funciones con tipos)
que:

1. Lea todos los renglones hasta el final de la entrada.
2. Valide cada uno con una función `validarRegistro(string $linea): array` que
   devuelva `['ok' => true, 'datos' => [...]]` o `['ok' => false, 'error' =>
   'motivo']`. Un registro es válido si:
   - tiene exactamente 4 campos;
   - el barco no está vacío;
   - la fecha tiene el formato `DD/MM/AAAA` (dos dígitos, dos dígitos, cuatro
     dígitos; usá `explode` y `ctype_digit`) con mes de 1 a 12;
   - los kilos son un número **entero** mayor o igual a 0 (`filter_var`: `"12abc"`
     y `"3.5"` no valen);
   - los pasajeros son un entero entre 0 y 500.
3. Muestre los inválidos con su número de renglón y el motivo.
4. Con los válidos, muestre un resumen por barco (ordenado por nombre): cuántos
   viajes, total de kilos y promedio de pasajeros con un decimal.
5. Muestre el barco que más kilos llevó en total.

#### Criterio de aprobación

- La validación está en una función que no muestra nada.
- `"12abc"`, `"3.5"` y el `"0"` como texto se tratan bien (el `0` es válido).
- El resumen usa un array asociativo por barco.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
Gaviota;01/10/2026;450;34
Albatros;01/10/2026;1200;120
Gaviota;03/10/2026;12abc;30
Tortuga;04/13/2026;80;5
Albatros;05/10/2026;900;0
;06/10/2026;100;10
Gaviota;07/10/2026;0;41
Delfín;07/10/2026;300
Tortuga;08/10/2026;95;600
Tortuga;09/10/2026;120;8
```

#### Salida esperada

```
Registros con errores:
  renglón 3: kilos inválidos: 12abc
  renglón 4: fecha inválida: 04/13/2026
  renglón 6: falta el barco
  renglón 8: tiene 3 campos (van 4)
  renglón 9: pasajeros inválidos: 600

Resumen por barco:
  Albatros  2 viaje/s   2100 kg   60.0 pasajeros
  Gaviota   2 viaje/s    450 kg   37.5 pasajeros
  Tortuga   1 viaje/s    120 kg    8.0 pasajeros

Más carga: Albatros (2100 kg)
```

#### Solución de referencia

```php
<?php
declare(strict_types=1);
// Jefe R01 - El libro de bitácora: validar, agrupar y resumir.

function fechaValida(string $fecha): bool
{
    $partes = explode('/', $fecha);
    if (count($partes) !== 3) {
        return false;
    }
    [$dia, $mes, $anio] = $partes;
    if (strlen($dia) !== 2 || strlen($mes) !== 2 || strlen($anio) !== 4) {
        return false;
    }
    if (!ctype_digit($dia . $mes . $anio)) {
        return false;
    }
    return (int) $mes >= 1 && (int) $mes <= 12 && (int) $dia >= 1 && (int) $dia <= 31;
}

function validarRegistro(string $linea): array
{
    $campos = explode(';', trim($linea));
    if (count($campos) !== 4) {
        return ['ok' => false, 'error' => 'tiene ' . count($campos) . ' campos (van 4)'];
    }
    [$barco, $fecha, $kilos, $pasajeros] = array_map('trim', $campos);
    if ($barco === '') {
        return ['ok' => false, 'error' => 'falta el barco'];
    }
    if (!fechaValida($fecha)) {
        return ['ok' => false, 'error' => "fecha inválida: $fecha"];
    }
    $kilosOk = filter_var($kilos, FILTER_VALIDATE_INT, ['options' => ['min_range' => 0]]);
    if ($kilosOk === false) {
        return ['ok' => false, 'error' => "kilos inválidos: $kilos"];
    }
    $pasajerosOk = filter_var($pasajeros, FILTER_VALIDATE_INT, ['options' => ['min_range' => 0, 'max_range' => 500]]);
    if ($pasajerosOk === false) {
        return ['ok' => false, 'error' => "pasajeros inválidos: $pasajeros"];
    }
    return ['ok' => true, 'datos' => ['barco' => $barco, 'fecha' => $fecha, 'kilos' => $kilosOk, 'pasajeros' => $pasajerosOk]];
}

function agregarAlResumen(array $resumen, array $datos): array
{
    $barco = $datos['barco'];
    $resumen[$barco] ??= ['viajes' => 0, 'kilos' => 0, 'pasajeros' => 0];
    $resumen[$barco]['viajes']++;
    $resumen[$barco]['kilos'] += $datos['kilos'];
    $resumen[$barco]['pasajeros'] += $datos['pasajeros'];
    return $resumen;
}

$resumen = [];
$numero = 0;
echo "Registros con errores:\n";
while (($linea = fgets(STDIN)) !== false) {
    $numero++;
    if (trim($linea) === '') {
        continue;
    }
    $resultado = validarRegistro($linea);
    if (!$resultado['ok']) {
        echo "  renglón $numero: {$resultado['error']}\n";
        continue;
    }
    $resumen = agregarAlResumen($resumen, $resultado['datos']);
}

ksort($resumen);
echo "\nResumen por barco:\n";
$masKilos = '';
foreach ($resumen as $barco => $r) {
    printf("  %-9s %d viaje/s  %5d kg  %5.1f pasajeros\n", $barco, $r['viajes'], $r['kilos'], $r['pasajeros'] / $r['viajes']);
    if ($masKilos === '' || $r['kilos'] > $resumen[$masKilos]['kilos']) {
        $masKilos = $barco;
    }
}
echo "\nMás carga: $masKilos ({$resumen[$masKilos]['kilos']} kg)\n";
```

### Misión R01-N10-M2 · La oficina de encomiendas

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 30
```

#### Consigna

Armá el sistema de la **oficina de encomiendas** del Puerto, repartido en
archivos:

```
encomiendas/
├── main.php
├── config.php         ← tarifas por destino, recargo urgente, IVA
└── lib/
    ├── validacion.php ← leer y validar datos
    ├── calculo.php    ← costos
    └── formato.php    ← pesos, renglones del ticket
```

El programa lee **comandos** de la entrada, uno por renglón, hasta `SALIR` o el
final:

- `ALTA;DESTINO;KILOS;URGENTE` — agrega una encomienda (URGENTE es `si` o `no`).
  Destinos y tarifa por kilo en `config.php`: `valle` 300, `forjas` 450,
  `imperio` 600, `ciudadela` 520. Si algo es inválido, muestra el motivo y no la
  agrega. Si sale bien, muestra el número de encomienda asignado (1, 2, 3…).
- `BAJA;NUMERO` — saca una encomienda (si no existe, lo avisa).
- `LISTA` — muestra las encomiendas cargadas con su costo.
- `TOTAL` — muestra el subtotal, el IVA (21%) y el total.
- cualquier otro comando — `Comando desconocido: …`.

El costo es kilos × tarifa, más 50% si es urgente, y un mínimo de $1000 por
encomienda.

#### Criterio de aprobación

- Está repartido en los archivos pedidos, con `require_once __DIR__` y la
  configuración en `config.php`.
- Las funciones tienen tipos y `strict_types`; solo `main.php` muestra y lee.
- Los comandos inválidos o con datos malos no rompen el programa.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
ALTA;valle;2;no
ALTA;imperio;10;si
ALTA;luna;3;no
ALTA;forjas;tres;no
ALTA;ciudadela;1.5;no
LISTA
BAJA;2
BAJA;7
VOLAR
TOTAL
SALIR
ALTA;valle;5;no
```

#### Salida esperada

```
Encomienda 1 cargada.
Encomienda 2 cargada.
No se cargó: destino desconocido: luna
No se cargó: kilos inválidos: tres
Encomienda 3 cargada.
#1 valle 2 kg............$1.000,00
#2 imperio 10 kg URG.....$9.000,00
#3 ciudadela 1.5 kg......$1.000,00
Encomienda 2 dada de baja.
No existe la encomienda 7.
Comando desconocido: VOLAR
Subtotal.................$2.000,00
IVA........................$420,00
TOTAL....................$2.420,00
Oficina cerrada.
```

#### Solución de referencia

`config.php`
```php
<?php
return [
    'tarifas' => ['valle' => 300, 'forjas' => 450, 'imperio' => 600, 'ciudadela' => 520],
    'recargo_urgente' => 0.5,
    'minimo' => 1000,
    'iva' => 0.21,
];
```

`lib/validacion.php`
```php
<?php
declare(strict_types=1);

/** Valida un ALTA; devuelve ['ok' => bool, 'error' => string, 'datos' => array]. */
function validarAlta(array $campos, array $config): array
{
    if (count($campos) !== 4) {
        return ['ok' => false, 'error' => 'ALTA lleva DESTINO;KILOS;URGENTE'];
    }
    [, $destino, $kilos, $urgente] = $campos;
    $destino = mb_strtolower(trim($destino));
    if (!isset($config['tarifas'][$destino])) {
        return ['ok' => false, 'error' => "destino desconocido: $destino"];
    }
    $kilos = str_replace(',', '.', trim($kilos));
    if (!is_numeric($kilos) || (float) $kilos <= 0) {
        return ['ok' => false, 'error' => "kilos inválidos: $kilos"];
    }
    $urgente = mb_strtolower(trim($urgente));
    if ($urgente !== 'si' && $urgente !== 'no') {
        return ['ok' => false, 'error' => "urgente es si o no: $urgente"];
    }
    return ['ok' => true, 'error' => '', 'datos' => ['destino' => $destino, 'kilos' => (float) $kilos, 'urgente' => $urgente === 'si']];
}
```

`lib/calculo.php`
```php
<?php
declare(strict_types=1);

function costo(array $encomienda, array $config): float
{
    $costo = $encomienda['kilos'] * $config['tarifas'][$encomienda['destino']];
    if ($encomienda['urgente']) {
        $costo *= 1 + $config['recargo_urgente'];
    }
    return max($costo, $config['minimo']);
}

function subtotal(array $encomiendas, array $config): float
{
    return array_sum(array_map(fn(array $e): float => costo($e, $config), $encomiendas));
}
```

`lib/formato.php`
```php
<?php
declare(strict_types=1);

function pesos(float $monto): string
{
    return '$' . number_format($monto, 2, ',', '.');
}

function renglon(string $texto, string $valor, int $ancho = 34): string
{
    return $texto . str_repeat('.', max(1, $ancho - mb_strlen($texto) - mb_strlen($valor))) . $valor;
}
```

`main.php`
```php
<?php
declare(strict_types=1);
// Jefe R01 - La oficina de encomiendas: comandos, validación y cálculo en varios archivos.
require_once __DIR__ . '/lib/validacion.php';
require_once __DIR__ . '/lib/calculo.php';
require_once __DIR__ . '/lib/formato.php';
$config = require __DIR__ . '/config.php';

$encomiendas = [];
$proximo = 1;

while (($linea = fgets(STDIN)) !== false) {
    $linea = trim($linea);
    if ($linea === '') {
        continue;
    }
    $campos = explode(';', $linea);
    $comando = strtoupper($campos[0]);
    if ($comando === 'SALIR') {
        break;
    }

    switch ($comando) {
        case 'ALTA':
            $resultado = validarAlta($campos, $config);
            if (!$resultado['ok']) {
                echo "No se cargó: {$resultado['error']}\n";
                break;
            }
            $encomiendas[$proximo] = $resultado['datos'];
            echo "Encomienda $proximo cargada.\n";
            $proximo++;
            break;
        case 'BAJA':
            $numero = (int) ($campos[1] ?? 0);
            if (!isset($encomiendas[$numero])) {
                echo "No existe la encomienda $numero.\n";
                break;
            }
            unset($encomiendas[$numero]);
            echo "Encomienda $numero dada de baja.\n";
            break;
        case 'LISTA':
            foreach ($encomiendas as $numero => $e) {
                $texto = "#$numero {$e['destino']} {$e['kilos']} kg" . ($e['urgente'] ? ' URG' : '');
                echo renglon($texto, pesos(costo($e, $config))), "\n";
            }
            break;
        case 'TOTAL':
            $sub = subtotal($encomiendas, $config);
            echo renglon('Subtotal', pesos($sub)), "\n";
            echo renglon('IVA', pesos($sub * $config['iva'])), "\n";
            echo renglon('TOTAL', pesos($sub * (1 + $config['iva']))), "\n";
            break;
        default:
            echo "Comando desconocido: {$campos[0]}\n";
    }
}
echo "Oficina cerrada.\n";
```

### Prueba del sello

#### ¿Por qué `filter_var("12abc", FILTER_VALIDATE_INT)` es mejor que `(int) "12abc"` para validar?

Porque `filter_var` devuelve `false` y te enterás de que el dato está mal; `(int)` devuelve `12` en silencio.

#### Si un campo vale `"0"`, ¿`if ($campo)` lo toma como vacío?

Sí: `"0"` es falso para PHP. Para saber si está vacío hay que comparar con `=== ""`.

#### ¿Qué conviene que devuelva una función de validación?

Un resultado que diga si está bien y, si no, el motivo (por ejemplo, un array con `ok` y `error`), sin mostrar nada: quien la llama decide qué hacer.

#### ¿Por qué se usa `??=` en `$resumen[$barco] ??= [...]`?

Para crear la entrada del barco solo si todavía no existe, sin pisar lo que ya tenía.

#### ¿Cómo se prueba un programa que lee del teclado sin escribir los datos cada vez?

Guardando la entrada en un archivo y redirigiéndola: `php main.php < entrada.txt`.

### Soluciones (docente)

Jefe de la rama 1: integra todo el Muelle. La misión 1 junta validación estricta (`filter_var` contra `(int)`), arrays asociativos y funciones; la 2 es un proyecto repartido en archivos con comandos (anticipa el `switch`/`match` de un router web). El capítulo original no tenía jefe en este punto: se escribió desde cero. Al corregir, mirar que las funciones de `lib/` no hagan `echo` y que la configuración esté en `config.php`.
