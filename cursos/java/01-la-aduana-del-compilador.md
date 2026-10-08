# RAMA R01 · La Aduana del Compilador: los fundamentos

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

Pasado el portón, un aduanero le pone a Zed delante una balanza con cajones etiquetados: *enteros*, *decimales*, *letras*, *verdadero o falso*. Zed intenta meter «un poco de todo» en el mismo cajón. Nada entra sin etiqueta.

—En el Imperio cada cosa se **declara** —explica {mentor}—. Si decís que un cajón guarda números enteros, la Aduana no te va a dejar meter medio kilo de harina. Parece rígido, Zed, pero así nadie se lleva sorpresas.

Nadia anota todo en su libreta. No le saca los ojos de encima.

### Objetivos

- Declarar variables con su tipo y darles un valor.
- Conocer los tipos primitivos (`int`, `long`, `double`, `boolean`, `char`) y el tipo `String`.
- Declarar constantes con `final`.
- Convertir entre tipos: conversiones automáticas y *casting*.
- Entender el desbordamiento de los enteros.

### Antes de empezar

- Escribir, compilar y ejecutar un programa (Clase 0).

### Explicación

#### Declarar una variable
Una **variable** es un cajón con nombre donde se guarda un valor. En Java se
declara con su **tipo** y, casi siempre, con un valor inicial:
```java
int vidas = 3;              // tipo, nombre, valor
double precio = 1250.75;
boolean tieneLlave = true;
char inicial = 'K';          // un solo carácter, entre comillas simples
String nombre = "Kira";      // un texto, entre comillas dobles
```
Después se puede cambiar el valor (sin repetir el tipo):
```java
vidas = vidas - 1;          // ahora vale 2
```
Los nombres van en *camelCase* (`puntosDeVida`), empiezan con letra y no pueden
ser palabras reservadas (`class`, `int`, `new`…).

#### Los tipos primitivos
| Tipo | Guarda | Ejemplo | Rango |
|---|---|---|---|
| `int` | enteros | `42` | ±2 147 483 647 (unos 2 mil millones) |
| `long` | enteros grandes | `9_000_000_000L` | ±9,2 × 10¹⁸ |
| `double` | decimales | `3.14` | unos 15 dígitos de precisión |
| `boolean` | verdadero o falso | `true`, `false` | — |
| `char` | un carácter | `'K'`, `'ñ'` | un carácter Unicode |

También existen `byte`, `short` y `float`, pero se usan poco: con `int`, `long`,
`double`, `boolean` y `char` se resuelve casi todo.

`String` **no es primitivo**: es una clase (por eso va con mayúscula). Lo vas a
ver a fondo en el nodo de textos.

Detalles de los literales:
- Un número con punto es `double` (`2.5`); sin punto es `int` (`2`).
- Un `long` grande lleva `L` al final: `3_000_000_000L`.
- El guion bajo separa miles para leer mejor: `1_000_000` es un millón.

#### Constantes: `final`
Un valor que no debe cambiar se declara `final`, y por convención su nombre va en
mayúsculas:
```java
final int VIDAS_MAXIMAS = 5;
final double IMPUESTO = 0.21;
VIDAS_MAXIMAS = 6;          // error de compilación: no se puede cambiar
```

#### `var`: que el compilador deduzca el tipo
Desde Java 10, en variables locales podés escribir `var` y el compilador deduce el
tipo del valor:
```java
var puntos = 100;           // int
var nombre = "Bron";        // String
```
El tipo sigue siendo fijo: `puntos = "mucho";` no compila. En este curso lo usamos
poco, para que los tipos se vean siempre.

#### Conversiones automáticas
Java convierte solo cuando **no se pierde información**: de `int` a `long`, de
`int` a `double`.
```java
int enteros = 7;
double comoDecimal = enteros;   // 7.0: entra sin problema
```
Al revés no: guardar un `double` en un `int` **no compila**, porque se perderían
los decimales:
```java
double peso = 3.9;
int kilos = peso;               // error: incompatible types: possible lossy conversion from double to int
```

#### Casting: convertir a propósito
Si querés perder los decimales a propósito, lo decís con un **casting**: el tipo
entre paréntesis.
```java
int kilos = (int) peso;          // 3: corta los decimales (no redondea)
double mitad = (double) 7 / 2;   // 3.5 (sin el casting daría 3)
char letra = (char) ('A' + 2);   // 'C': los char son números por dentro
int codigo = 'K';                // 75: el código Unicode de la K
```

#### Desbordamiento
Un `int` no puede pasar de 2 147 483 647. Si lo pasa, **da la vuelta** y queda
negativo, sin aviso:
```java
int oro = Integer.MAX_VALUE;     // 2147483647
oro = oro + 1;                   // -2147483648
```
Para cantidades grandes (dinero en centavos, poblaciones, milisegundos) usá `long`.

#### Los decimales no son exactos
Los `double` guardan una aproximación en binario:
```java
System.out.println(0.1 + 0.2);   // 0.30000000000000004
```
Para mostrar una cantidad fija de decimales vas a usar `printf` en el nodo de
textos. Para dinero exacto se usan centavos en un `long` (o la clase
`BigDecimal`, que se ve más adelante).

> **Si venís de C.** Los tamaños son fijos en todas las plataformas (`int` siempre
> es de 32 bits), no hay `unsigned`, `boolean` no es un número y una variable local
> sin inicializar **no compila** en vez de tener basura.
>
> **Si venís de Python.** El tipo se declara y no cambia. Los `int` tienen límite y
> se desbordan (en Python no), y `7 / 2` entre enteros da `3`.

### Código de ejemplo

```java
/*
 * Variables, tipos y conversiones: la ficha de una viajera en la Aduana.
 */
public class FichaAduana {
    public static void main(String[] args) {
        final double IMPUESTO = 0.21;          // constante: no cambia

        String nombre = "Kira";
        char inicial = nombre.charAt(0);       // el primer carácter
        int edad = 19;
        double pesoEquipaje = 12.75;
        boolean traeArmas = false;
        long pasosDesdeElValle = 3_450_000_000L;

        System.out.println("Viajera: " + nombre + " (" + inicial + ")");
        System.out.println("Edad: " + edad);
        System.out.println("Equipaje: " + pesoEquipaje + " kg");
        System.out.println("¿Trae armas? " + traeArmas);
        System.out.println("Pasos desde el Valle: " + pasosDesdeElValle);

        // Conversiones
        int kilosEnteros = (int) pesoEquipaje;             // casting: corta los decimales
        double tasa = kilosEnteros * 100 * IMPUESTO;       // int * int * double -> double
        System.out.println("Kilos que se cobran: " + kilosEnteros);
        System.out.println("Tasa: " + tasa);
        System.out.println("Promedio de 7 y 2: " + (7 + 2) / 2 + " (entero) y " + (7 + 2) / 2.0 + " (decimal)");

        // Desbordamiento
        int oro = Integer.MAX_VALUE;
        System.out.println("Oro máximo: " + oro);
        oro = oro + 1;
        System.out.println("Un denario más: " + oro);

        // char como número
        System.out.println("Código de la K: " + (int) inicial);
        System.out.println("Dos letras después: " + (char) (inicial + 2));
    }
}
```

### Salida esperada

```
Viajera: Kira (K)
Edad: 19
Equipaje: 12.75 kg
¿Trae armas? false
Pasos desde el Valle: 3450000000
Kilos que se cobran: 12
Tasa: 252.0
Promedio de 7 y 2: 4 (entero) y 4.5 (decimal)
Oro máximo: 2147483647
Un denario más: -2147483648
Código de la K: 75
Dos letras después: M
```

### ¿Para qué sirve?

Elegir bien el tipo es la primera decisión de cualquier programa: un sistema de ventas guarda precios, cantidades y códigos; un juego guarda vidas, posiciones y nombres. Usar `int` donde hacía falta `long` es el origen de errores famosos (contadores que se vuelven negativos), y confundir `int` con `double` es la causa más común de promedios mal calculados.

### Errores habituales

**Goblin: meter un decimal en un entero.**
```
Ficha.java:5: error: incompatible types: possible lossy conversion from double to int
        int kilos = 12.75;
                    ^
```
Si querés cortar los decimales, hacelo a propósito: `(int) 12.75`.

**Ogro: la división entera.** `int promedio = (7 + 2) / 2;` da `4`, no `4.5`.
Si querés decimales, al menos uno de los dos tiene que ser `double`: `/ 2.0`.

**Esqueleto: usar una variable sin valor.**
```
Ficha.java:6: error: variable vidas might not have been initialized
```
Toda variable local necesita un valor antes de usarse.

**Goblin: el `long` sin `L`.** `long pasos = 3450000000;` no compila (`integer
number too large`): el literal es `int` y no entra. Va `3450000000L`.

**Slime: comillas equivocadas.** `char c = "K";` o `String s = 'Kira';`: el `char`
va con comillas simples y el `String` con dobles.

### Micro-misión R01-N01-P1 · Cada cajón con su etiqueta

```meta
lugar: La Aduana del Compilador
personajes: Zed, Gheco, Nadia
carta: Variables y tipos | int edad = 18; · double peso = 2.5; · String nombre = "Zed"; · boolean libre = true;
recompensa: xp 10, oro 10
```

#### Escena
Pasado el portón hay una balanza con cajones etiquetados: *enteros*, *decimales*, *texto*, *verdadero o falso*. Zed quiere meter «un poco de todo» en el mismo cajón.
—Cada cajón guarda **un solo tipo** —dice Nadia—. Declaralo.

#### Gheco sugiere
Una variable se declara con su **tipo** y su nombre: `int` (enteros), `double` (decimales), `String` (texto, con mayúscula) y `boolean` (`true` o `false`).

#### Desafío
Completá el tipo de cada cajón.

#### Código inicial
```java
public class Cajones {
    public static void main(String[] args) {
        ___ barriles = 3;
        ___ peso = 12.5;
        ___ propietario = "Zed";
        ___ declarado = true;
        System.out.println(barriles + " barriles de " + peso + " kg, de " + propietario + ": " + declarado);
    }
}
```

#### Salida esperada
```
3 barriles de 12.5 kg, de Zed: true
```

#### Solución
```java
public class Cajones {
    public static void main(String[] args) {
        int barriles = 3;
        double peso = 12.5;
        String propietario = "Zed";
        boolean declarado = true;
        System.out.println(barriles + " barriles de " + peso + " kg, de " + propietario + ": " + declarado);
    }
}
```

#### Al superarla
La balanza se equilibra y cada cajón se cierra con un clic. Nadia tilda algo en la libreta.

#### Imagen
- Una balanza de bronce con cuatro cajones etiquetados: enteros, decimales, texto, verdadero o falso.
- Zed acomoda paquetes en cada cajón; Nadia controla con la libreta.

### Micro-misión R01-N01-P2 · Lo que no cambia

```meta
lugar: La Aduana del Compilador
personajes: Zed, Gheco, Nadia
carta: Constantes | final double PEAJE = 2.5; · no se puede reasignar · nombre en MAYÚSCULAS
recompensa: xp 10, oro 10
```

#### Escena
Zed «ajusta» el valor del peaje en su cuenta, para pagar menos. Nadia ni lo mira: —El peaje es **constante**. Escribilo así y el compilador no te va a dejar tocarlo.

#### Gheco sugiere
Con `final` una variable se vuelve **constante**: si alguien intenta cambiarla, no compila. Por costumbre se escribe en MAYÚSCULAS.

#### Desafío
Sacá la línea que intenta cambiar la constante, para que compile.

#### Código inicial
```java
public class Constante {
    public static void main(String[] args) {
        final int PEAJE = 5;
        int carros = 4;
        PEAJE = 1;
        System.out.println("Total: " + PEAJE * carros + " denarios");
    }
}
```

#### Salida esperada
```
Total: 20 denarios
```

#### Solución
```java
public class Constante {
    public static void main(String[] args) {
        final int PEAJE = 5;
        int carros = 4;
        System.out.println("Total: " + PEAJE * carros + " denarios");
    }
}
```

#### Al superarla
Veinte denarios. Zed paga, de mala gana. —Por lo menos es la misma regla para todos —murmura Gheco.

#### Imagen
- Un cartel de piedra tallada con el peaje: «5», con un candado de bronce.
- Zed pagando monedas de mala gana; Nadia extiende la mano.

### Micro-misión R01-N01-P3 · Medio kilo no entra

```meta
lugar: La Aduana del Compilador
personajes: Zed, Gheco, Nadia
criatura: goblin
carta: Casting | int n = (int) 3.99; → 3 (corta, no redondea) · de double a int hay que pedirlo
recompensa: xp 15, oro 15
```

#### Escena
Zed intenta guardar 7,8 kilos de harina en el cajón de los enteros. No compila, y de entre los sacos salta un **goblin**.
—Los goblins nacen de los tipos que no encajan —dice Gheco—. Si querés pasar un decimal a entero, **pedilo**.

#### Gheco sugiere
Un `double` no entra solo en un `int`: hay que **convertirlo** con `(int)`. Ojo: **corta** los decimales, no redondea. Para redondear está `Math.round`.

#### Desafío
Convertí el peso a entero (cortando) para el cajón de enteros.

#### Código inicial
```java
public class Casting {
    public static void main(String[] args) {
        double harina = 7.8;
        int cajon = harina;
        System.out.println("En el cajón entran " + cajon + " kg");
        System.out.println("Redondeado serían " + Math.round(harina));
    }
}
```

#### Salida esperada
```
En el cajón entran 7 kg
Redondeado serían 8
```

#### Solución
```java
public class Casting {
    public static void main(String[] args) {
        double harina = 7.8;
        int cajon = (int) harina;
        System.out.println("En el cajón entran " + cajon + " kg");
        System.out.println("Redondeado serían " + Math.round(harina));
    }
}
```

#### Al superarla
Siete kilos al cajón; los ochocientos gramos sobrantes se los queda el goblin y huye. Nadia anota: «pérdida: 0,8 kg».

#### Imagen
- Un goblin flaco huye con un saquito de harina entre los cajones.
- Un cajón de enteros con un 7 grabado; un 0,8 escapándose en el aire.

### Micro-misión R01-N01-P4 · El reparto que no da

```meta
lugar: La Aduana del Compilador
personajes: Zed, Gheco, Nadia
criatura: ogro
carta: División entera | 7 / 2 → 3 (dos int) · 7 / 2.0 → 3.5 · si uno es double, el resultado es double
recompensa: xp 15, oro 15
```

#### Escena
Hay que repartir 7 denarios de multa entre 2 viajeros. La cuenta da 3 cada uno… y se perdió un denario. Ningún error: es un **ogro**.

#### Gheco sugiere
Entre dos `int`, `/` da la **división entera**: tira los decimales. Si uno de los dos es `double` (por ejemplo `2.0`), el resultado tiene decimales.

#### Desafío
Hacé que el reparto dé con decimales.

#### Código inicial
```java
public class Reparto {
    public static void main(String[] args) {
        int multa = 7;
        System.out.println("Cada uno paga " + multa / 2);
    }
}
```

#### Salida esperada
```
Cada uno paga 3.5
```

#### Solución
```java
public class Reparto {
    public static void main(String[] args) {
        int multa = 7;
        System.out.println("Cada uno paga " + multa / 2.0);
    }
}
```

#### Al superarla
Tres y medio cada uno: el denario perdido aparece. —Ningún error y todo mal —dice Gheco—. Así son los ogros.

#### Imagen
- Siete monedas que se reparten en dos montones de tres y media; media moneda partida brilla en el medio.
- Un ogro chiquito que se escabulle detrás de la balanza.

### Misión R01-N01-M1 · El inventario del carro

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un mercader lleva en su carro 37 bolsas de harina de 2.5 kg cada una. Declará las
variables con el tipo adecuado (la cantidad de bolsas, el peso de cada bolsa y el
nombre del mercader) y mostrá:

1. El peso total, como `double`.
2. El peso total en kilos enteros, con casting.
3. Cuántas bolsas completas de 10 kg se podrían armar con esa harina (división entera).

#### Criterio de aprobación

- Usa `int`, `double` y `String` donde corresponde.
- Usa un casting `(int)` para los kilos enteros.
- La salida coincide con la esperada.

#### Salida esperada

```
Carro de Olmo
Peso total: 92.5 kg
En kilos enteros: 92
Bolsas completas de 10 kg: 9
```

#### Solución de referencia

```java
// Mision 1 - El inventario del carro: tipos, casting y division entera.
public class Inventario {
    public static void main(String[] args) {
        String mercader = "Olmo";
        int bolsas = 37;
        double kilosPorBolsa = 2.5;

        double total = bolsas * kilosPorBolsa;
        int totalEntero = (int) total;
        int bolsasDeDiez = totalEntero / 10;

        System.out.println("Carro de " + mercader);
        System.out.println("Peso total: " + total + " kg");
        System.out.println("En kilos enteros: " + totalEntero);
        System.out.println("Bolsas completas de 10 kg: " + bolsasDeDiez);
    }
}
```

### Misión R01-N01-M2 · El tesoro que dio la vuelta

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El tesoro del Imperio tiene 2 000 000 000 denarios y recibe un tributo de 500 000 000.
Mostrá qué pasa si lo guardás en un `int` y qué pasa si lo guardás en un `long`.
Después mostrá los valores máximos de los dos tipos (`Integer.MAX_VALUE` y
`Long.MAX_VALUE`).

#### Criterio de aprobación

- Muestra el desbordamiento del `int` (queda negativo).
- Con `long` el resultado es correcto.
- Muestra los dos máximos.

#### Salida esperada

```
Con int: -1794967296
Con long: 2500000000
Máximo de int: 2147483647
Máximo de long: 9223372036854775807
```

#### Solución de referencia

```java
// Mision 2 - El tesoro que dio la vuelta: desbordamiento de int y uso de long.
public class Tesoro {
    public static void main(String[] args) {
        int tesoroInt = 2_000_000_000;
        tesoroInt = tesoroInt + 500_000_000;
        System.out.println("Con int: " + tesoroInt);

        long tesoroLong = 2_000_000_000L;
        tesoroLong = tesoroLong + 500_000_000;
        System.out.println("Con long: " + tesoroLong);

        System.out.println("Máximo de int: " + Integer.MAX_VALUE);
        System.out.println("Máximo de long: " + Long.MAX_VALUE);
    }
}
```

### Misión R01-N01-M3 · Las notas de la academia

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Una estudiante de la Academia sacó 7, 9 y 8 en tres exámenes (guardalos en `int`).
Mostrá el promedio calculado **mal** (división entera) y **bien** (con casting a
`double`). Después mostrá la letra que va una posición después de la inicial de su
nombre, `'L'` de Lía, usando un casting a `char`.

#### Criterio de aprobación

- Las tres notas son `int`.
- El promedio correcto usa `(double)`.
- La letra siguiente se calcula con un casting a `char`, no se escribe a mano.

#### Salida esperada

```
Promedio con división entera: 8
Promedio con casting: 8.0
Letra siguiente a L: M
```

#### Solución de referencia

```java
// Mision 3 - Las notas de la academia: division entera vs casting.
public class Notas {
    public static void main(String[] args) {
        int nota1 = 7;
        int nota2 = 9;
        int nota3 = 8;
        char inicial = 'L';

        int promedioMal = (nota1 + nota2 + nota3) / 3;
        double promedioBien = (double) (nota1 + nota2 + nota3) / 3;

        System.out.println("Promedio con división entera: " + promedioMal);
        System.out.println("Promedio con casting: " + promedioBien);
        System.out.println("Letra siguiente a " + inicial + ": " + (char) (inicial + 1));
    }
}
```

### Encargo R01-N01-E1 · El cambio de monedas

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una casa de cambio guarda los montos en **centavos** (en un `long`) para no perder
precisión. Un cliente cambia 1 234 567 centavos. Mostrá el monto en pesos y centavos
por separado (`12345 pesos con 67 centavos`) usando división entera y resto (`%`),
y cuántos billetes de 1000 pesos entran.

#### Criterio de aprobación

- El monto se guarda en `long`.
- Usa `/` y `%` entre enteros.

#### Salida esperada

```
Monto: 12345 pesos con 67 centavos
Billetes de 1000: 12
```

#### Solución de referencia

```java
// Encargo - El cambio de monedas: centavos en long, / y %.
public class Cambio {
    public static void main(String[] args) {
        long centavos = 1_234_567L;
        long pesos = centavos / 100;
        long resto = centavos % 100;
        long billetesDeMil = pesos / 1000;

        System.out.println("Monto: " + pesos + " pesos con " + resto + " centavos");
        System.out.println("Billetes de 1000: " + billetesDeMil);
    }
}
```

### Prueba del sello

#### ¿Cuánto da `7 / 2`? ¿Y `7 / 2.0`?

`3` y `3.5`. Entre dos enteros la división es entera; si uno es `double`, el resultado es `double`.

#### ¿Por qué `int kilos = 12.75;` no compila?

Porque se perderían los decimales, y Java no hace esa conversión sola. Hay que pedirla con un casting: `(int) 12.75`.

#### ¿Qué pasa si a `Integer.MAX_VALUE` le sumás 1?

Da la vuelta y queda en el mínimo, `-2147483648`, sin ningún aviso. Para números grandes se usa `long`.

#### ¿Qué diferencia hay entre `'K'` y `"K"`?

`'K'` es un `char` (un carácter) y `"K"` es un `String` (un texto de un carácter).

#### ¿Para qué sirve `final`?

Para declarar una constante: una variable que no se puede volver a asignar.

### Soluciones (docente)

Sale de `18-Java/02-Variables-Tipos` (unidad 2). Se sumó `var` y el desbordamiento con `long`, y se corrigió la idea del capítulo viejo de que "los primitivos viven en la pila".

## R01-N02 · Operadores y expresiones

```meta
tipo: tema
padre: R01-N01
precio: 10
criatura: ogre
temas: prog.operadores
```

### Crónica

En el patio de la Aduana, dos guardias discuten a los gritos: uno calculó que la caravana paga 18 denarios y el otro, 12. Los dos usaron los mismos números.

—Tienen razón los dos —suspira {mentor}—, y los dos están mal. Uno sumó antes de multiplicar y el otro al revés. Las **expresiones** tienen reglas de orden, Zed. Si no las conocés, el ogro de la lógica se ríe de vos.

Zed, que en el Puerto contaba monedas ajenas a toda velocidad, descubre que acá el orden decide quién paga de más.

### Objetivos

- Usar los operadores aritméticos, incluido el resto `%`.
- Abreviar asignaciones con `+=`, `-=`, `++` y `--`.
- Comparar valores y combinar condiciones con `&&`, `||` y `!`.
- Usar el operador ternario.
- Conocer la precedencia y usar paréntesis para dejarla clara.

### Antes de empezar

- Variables, tipos y conversiones.

### Explicación

#### Aritméticos
| Operador | Qué hace | Ejemplo | Resultado |
|---|---|---|---|
| `+` | suma (y une textos) | `7 + 2` | `9` |
| `-` | resta | `7 - 2` | `5` |
| `*` | multiplicación | `7 * 2` | `14` |
| `/` | división (entera si los dos son enteros) | `7 / 2` | `3` |
| `%` | resto de la división entera | `7 % 2` | `1` |

El resto sirve para muchas cosas: `n % 2 == 0` dice si `n` es par, `n % 10` da el
último dígito y `segundos % 60` los segundos que sobran de los minutos.

#### Asignación compuesta, incremento y decremento
```java
int oro = 100;
oro += 25;      // oro = oro + 25  -> 125
oro -= 5;       // 120
oro *= 2;       // 240
oro /= 3;       // 80
oro %= 7;       // 3
int turno = 1;
turno++;        // turno = turno + 1 -> 2
turno--;        // 1
```
`x++` (después) y `++x` (antes) dan distinto **solo si se usan dentro de otra
expresión**. Para no confundirse, usalos solos en su propia línea.

#### Comparación
Devuelven un `boolean`: `==` (igual), `!=` (distinto), `<`, `<=`, `>`, `>=`.
```java
int vida = 12;
boolean enPeligro = vida < 20;     // true
```
Ojo: `=` asigna y `==` compara. Y para comparar **textos** no se usa `==` (lo vas a
ver en el nodo de textos).

#### Lógicos
| Operador | Significa | Da `true` si… |
|---|---|---|
| `a && b` | y | los dos son `true` |
| `a \|\| b` | o | al menos uno es `true` |
| `!a` | no | `a` es `false` |

```java
boolean puedePasar = tienePase && !traeArmas;
boolean descuento = edad < 12 || edad >= 65;
```
`&&` y `||` son de **cortocircuito**: si con el primer operando ya se sabe el
resultado, el segundo ni se evalúa. `x != 0 && 10 / x > 2` nunca divide por cero.

#### El operador ternario
Elige entre dos valores según una condición:
```java
String estado = vida > 0 ? "vivo" : "caído";
int mayor = a > b ? a : b;
```
Se lee: *¿condición? valor si es verdad : valor si es falso*.

#### Precedencia
Como en matemática, se multiplica y divide antes de sumar y restar:
```java
int total = 2 + 3 * 4;       // 14, no 20
int otro  = (2 + 3) * 4;     // 20
```
El orden, de mayor a menor: `!` y `++`/`--` → `*` `/` `%` → `+` `-` → comparaciones
→ `==` `!=` → `&&` → `||` → ternario → asignaciones. Cuando dudes, **poné
paréntesis**: no cuestan nada y hacen el código más claro.

#### El `+` con textos
Si alguno de los dos lados es un `String`, `+` **une**. Se evalúa de izquierda a
derecha:
```java
System.out.println("Total: " + 2 + 3);     // Total: 23  (une "2" y después "3")
System.out.println("Total: " + (2 + 3));   // Total: 5
System.out.println(2 + 3 + " denarios");   // 5 denarios (primero suma)
```

> **Si venís de Python.** `&&`, `||` y `!` reemplazan a `and`, `or` y `not`; el
> ternario es `c ? a : b` en lugar de `a if c else b`, y no hay `**`: la potencia es
> `Math.pow`.

### Código de ejemplo

```java
/*
 * Operadores: el cobro de una caravana en la Aduana.
 */
public class CobroCaravana {
    public static void main(String[] args) {
        int carros = 5;
        int caballos = 12;
        int tasaCarro = 3;
        int tasaCaballo = 1;

        int total = carros * tasaCarro + caballos * tasaCaballo;   // se multiplica antes de sumar
        System.out.println("Total a pagar: " + total + " denarios");

        // Resto: repartir los caballos en establos de 5
        System.out.println("Establos llenos: " + caballos / 5);
        System.out.println("Caballos sueltos: " + caballos % 5);

        // Asignación compuesta
        int oro = 100;
        oro -= total;
        oro += 10;           // propina del mercader
        System.out.println("Oro de la Aduana: " + oro);

        // Comparaciones y lógicos
        boolean tienePase = true;
        boolean traeArmas = false;
        boolean caravanaGrande = carros > 3 || caballos > 10;
        boolean puedePasar = tienePase && !traeArmas;
        System.out.println("¿Caravana grande? " + caravanaGrande);
        System.out.println("¿Puede pasar? " + puedePasar);

        // Ternario
        String trato = caravanaGrande ? "revisión completa" : "revisión rápida";
        System.out.println("Trato: " + trato);

        // El + con textos
        System.out.println("Sin paréntesis: " + carros + caballos);
        System.out.println("Con paréntesis: " + (carros + caballos));

        // Par o impar con %
        int numeroDeCaravana = 47;
        System.out.println("La caravana " + numeroDeCaravana + " es " + (numeroDeCaravana % 2 == 0 ? "par" : "impar"));
    }
}
```

### Salida esperada

```
Total a pagar: 27 denarios
Establos llenos: 2
Caballos sueltos: 2
Oro de la Aduana: 83
¿Caravana grande? true
¿Puede pasar? true
Trato: revisión completa
Sin paréntesis: 512
Con paréntesis: 17
La caravana 47 es impar
```

### ¿Para qué sirve?

Todo cálculo de un sistema real es una expresión: el total de una factura con impuestos, si un alumno aprueba (`nota >= 4 && asistencia >= 75`), si un año es bisiesto, cuántas páginas hacen falta para mostrar 53 resultados de a 10. El resto `%` aparece en todos lados: relojes, calendarios, turnos rotativos, validar dígitos verificadores.

### Errores habituales

**Ogro: la precedencia.** `double promedio = a + b / 2;` divide solo `b`. Va
`(a + b) / 2`.

**Ogro: el `+` que une en vez de sumar.** `"Total: " + 2 + 3` muestra `Total: 23`.
Encerrá la cuenta entre paréntesis.

**Slime: `=` en lugar de `==`.** `if (vida = 0)` no compila en Java
(`incompatible types: int cannot be converted to boolean`): para comparar va `==`.

**Ogro: `&` y `|` simples.** Existen, pero no hacen cortocircuito: evalúan los dos
lados siempre. Para condiciones usá `&&` y `||`.

**Orco: dividir por cero.** Entre enteros, `x / 0` corta el programa con
`ArithmeticException: / by zero`. Entre `double`, da `Infinity`.

### Micro-misión R01-N02-P1 · Cuántos carros completos

```meta
lugar: El patio de la Aduana
personajes: Zed, Gheco, Nadia
carta: / y % | 17 / 5 → 3 (cuántas veces entra) · 17 % 5 → 2 (lo que sobra)
recompensa: xp 10, oro 10
```

#### Escena
En el patio hay 17 barriles y los carros llevan 5 cada uno. Dos guardias discuten cuántos carros salen y cuántos barriles quedan. Nadia le pasa la cuenta a Zed.

#### Gheco sugiere
Con enteros, `/` dice **cuántas veces entra** y `%` (el resto) dice **lo que sobra**.

#### Desafío
Completá con el operador del resto.

#### Código inicial
```java
public class Carros {
    public static void main(String[] args) {
        int barriles = 17;
        int porCarro = 5;
        System.out.println("Carros llenos: " + barriles / porCarro);
        System.out.println("Sobran: " + barriles ___ porCarro);
    }
}
```

#### Salida esperada
```
Carros llenos: 3
Sobran: 2
```

#### Solución
```java
public class Carros {
    public static void main(String[] args) {
        int barriles = 17;
        int porCarro = 5;
        System.out.println("Carros llenos: " + barriles / porCarro);
        System.out.println("Sobran: " + barriles % porCarro);
    }
}
```

#### Al superarla
Tres carros y dos barriles sueltos. Los guardias se callan. Uno le hace un gesto a Zed: no está mal, para un colado.

#### Imagen
- El patio de la Aduana: tres carros cargados y dos barriles sueltos.
- Dos guardias que dejan de discutir; Zed con los brazos cruzados, satisfecho.

### Micro-misión R01-N02-P2 · Sumar sobre lo que hay

```meta
lugar: El patio de la Aduana
personajes: Zed, Gheco, Nadia
carta: Asignación compuesta | x += 3 · x -= 2 · x *= 2 · x++ suma uno
recompensa: xp 10, oro 10
```

#### Escena
—Contá los carros que van pasando —dice Nadia—. Uno por uno. Y al final, cada carro paga el doble por ser feriado.

#### Gheco sugiere
`carros++` suma uno. `total += 5` es `total = total + 5`; también existen `-=`, `*=` y `/=`.

#### Desafío
Completá las tres cuentas con atajos.

#### Código inicial
```java
public class Conteo {
    public static void main(String[] args) {
        int carros = 0;
        carros___;
        carros___;
        carros___;
        int peaje = carros * 5;
        peaje ___ 2;
        System.out.println(carros + " carros pagan " + peaje);
    }
}
```

#### Salida esperada
```
3 carros pagan 30
```

#### Solución
```java
public class Conteo {
    public static void main(String[] args) {
        int carros = 0;
        carros++;
        carros++;
        carros++;
        int peaje = carros * 5;
        peaje *= 2;
        System.out.println(carros + " carros pagan " + peaje);
    }
}
```

#### Al superarla
Treinta denarios de feriado. Nadia los guarda en la caja fuerte… y mira a Zed para ver dónde tiene las manos.

#### Imagen
- Una caja fuerte de la Aduana con un contador de carros de bronce que marca 3.
- Nadia guardando monedas mientras vigila a Zed de reojo.

### Micro-misión R01-N02-P3 · ¿Puede pasar?

```meta
lugar: El patio de la Aduana
personajes: Zed, Gheco, Nadia
carta: Lógicos | && (y) · || (o) · ! (no) · dan true o false
recompensa: xp 10, oro 10
```

#### Escena
La regla del portón: pasa quien **tiene sello y pagó**, o quien es **guardia**. Zed tiene sello, no pagó y no es guardia, pero dice que debería pasar.

#### Gheco sugiere
`&&` es «y» (las dos cosas), `||` es «o» (alguna de las dos) y `!` niega. Combinadas dan `true` o `false`.

#### Desafío
Escribí la regla del portón con `&&` y `||`.

#### Código inicial
```java
public class Porton {
    public static void main(String[] args) {
        boolean tieneSello = true;
        boolean pago = false;
        boolean esGuardia = false;
        boolean pasa = ___;
        System.out.println("¿Zed pasa? " + pasa);
    }
}
```

#### Salida esperada
```
¿Zed pasa? false
```

#### Solución
```java
public class Porton {
    public static void main(String[] args) {
        boolean tieneSello = true;
        boolean pago = false;
        boolean esGuardia = false;
        boolean pasa = (tieneSello && pago) || esGuardia;
        System.out.println("¿Zed pasa? " + pasa);
    }
}
```

#### Al superarla
`false`. Zed paga, refunfuñando. —La regla no tiene otra puerta —dice Nadia, y por primera vez casi se ríe.

#### Imagen
- Un portón con dos candados de luz: «sello» encendido y «pago» apagado.
- Zed busca una rendija en el portón; Nadia, apoyada en la pared, casi sonríe.

### Micro-misión R01-N02-P4 · Primero lo que va primero

```meta
lugar: El patio de la Aduana
personajes: Zed, Gheco, Nadia
criatura: ogro
carta: Precedencia | * y / antes que + y - · los paréntesis mandan · 2 + 3 * 4 → 14
recompensa: xp 15, oro 15
```

#### Escena
Cada carro paga 3 denarios, más 10 de la caravana entera, y todo eso por 2 porque es feriado. Un guardia hizo la cuenta y le dio 16. Debería ser 32. No hay error: un **ogro**.

#### Gheco sugiere
Java multiplica y divide **antes** de sumar y restar. Si querés otro orden, usá **paréntesis**.

#### Desafío
Poné los paréntesis para que la cuenta dé lo que tiene que dar.

#### Código inicial
```java
public class Feriado {
    public static void main(String[] args) {
        int carros = 2;
        int total = carros * 3 + 10 * 2;
        System.out.println("La caravana paga " + total);
    }
}
```

#### Salida esperada
```
La caravana paga 32
```

#### Solución
```java
public class Feriado {
    public static void main(String[] args) {
        int carros = 2;
        int total = (carros * 3 + 10) * 2;
        System.out.println("La caravana paga " + total);
    }
}
```

#### Al superarla
Treinta y dos. Los dos guardias que discutían se dan la mano. —El orden decide quién paga de más —dice Zed, y Nadia lo anota en su libreta como si fuera una regla.

#### Imagen
- Una pizarra con la cuenta: los paréntesis brillan en verde.
- Dos guardias dándose la mano; Nadia anota en su libreta.

### Misión R01-N02-M1 · El reloj de la torre

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El reloj de la torre cuenta los segundos desde la medianoche: van **50 000**.
Mostrá la hora en formato `horas:minutos:segundos` usando `/` y `%`. Después mostrá
cuántos segundos faltan para la medianoche siguiente (un día tiene 86 400).

#### Criterio de aprobación

- Calcula horas, minutos y segundos con `/` y `%`, sin escribir los valores a mano.
- Muestra los segundos que faltan.

#### Salida esperada

```
Hora: 13:53:20
Faltan 36400 segundos para la medianoche
```

#### Solución de referencia

```java
// Mision 1 - El reloj de la torre: / y % para convertir segundos.
public class Reloj {
    public static void main(String[] args) {
        int segundosTotales = 50_000;
        int horas = segundosTotales / 3600;
        int minutos = segundosTotales % 3600 / 60;
        int segundos = segundosTotales % 60;

        System.out.println("Hora: " + horas + ":" + minutos + ":" + segundos);
        System.out.println("Faltan " + (86_400 - segundosTotales) + " segundos para la medianoche");
    }
}
```

### Misión R01-N02-M2 · El año bisiesto

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un año es bisiesto si es divisible por 4 y no por 100, **o** si es divisible por
400. Guardá en una variable `boolean` si cada uno de estos años es bisiesto y
mostralo: 2024, 1900, 2000 y 2026. Usá una sola expresión con `%`, `&&`, `||` y
`!=` (podés repetirla para cada año).

#### Criterio de aprobación

- La condición combina `%`, `&&` y `||` correctamente.
- Los cuatro resultados son correctos.

#### Salida esperada

```
2024 bisiesto: true
1900 bisiesto: false
2000 bisiesto: true
2026 bisiesto: false
```

#### Solución de referencia

```java
// Mision 2 - El anio bisiesto: condiciones con % && ||.
public class Bisiesto {
    public static void main(String[] args) {
        int a1 = 2024;
        int a2 = 1900;
        int a3 = 2000;
        int a4 = 2026;
        boolean b1 = (a1 % 4 == 0 && a1 % 100 != 0) || a1 % 400 == 0;
        boolean b2 = (a2 % 4 == 0 && a2 % 100 != 0) || a2 % 400 == 0;
        boolean b3 = (a3 % 4 == 0 && a3 % 100 != 0) || a3 % 400 == 0;
        boolean b4 = (a4 % 4 == 0 && a4 % 100 != 0) || a4 % 400 == 0;
        System.out.println(a1 + " bisiesto: " + b1);
        System.out.println(a2 + " bisiesto: " + b2);
        System.out.println(a3 + " bisiesto: " + b3);
        System.out.println(a4 + " bisiesto: " + b4);
    }
}
```

### Misión R01-N02-M3 · El golpe crítico

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Kira ataca con fuerza 14 a un enemigo con armadura 5 y 30 de vida. El daño es la
fuerza menos la armadura, pero si la fuerza es al menos el doble de la armadura es
un **golpe crítico** y el daño se duplica. Calculá con el ternario el daño final,
restáselo a la vida con `-=` y mostrá si el enemigo sigue en pie (`vida > 0`).

#### Criterio de aprobación

- Usa el operador ternario para el daño.
- Usa `-=` para la vida.
- La salida coincide con la esperada.

#### Salida esperada

```
¿Crítico? true
Daño: 18
Vida restante: 12
¿Sigue en pie? true
```

#### Solución de referencia

```java
// Mision 3 - El golpe critico: ternario y asignacion compuesta.
public class GolpeCritico {
    public static void main(String[] args) {
        int fuerza = 14;
        int armadura = 5;
        int vida = 30;

        boolean critico = fuerza >= armadura * 2;
        int danio = critico ? (fuerza - armadura) * 2 : fuerza - armadura;
        vida -= danio;

        System.out.println("¿Crítico? " + critico);
        System.out.println("Daño: " + danio);
        System.out.println("Vida restante: " + vida);
        System.out.println("¿Sigue en pie? " + (vida > 0));
    }
}
```

### Encargo R01-N02-E1 · Las páginas del catálogo

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una tienda online muestra 12 productos por página y tiene 53 productos. Calculá
cuántas páginas hacen falta (la última puede quedar incompleta) **sin usar `if`**:
con división entera, resto y el ternario. Mostrá también cuántos productos hay en
la última página.

#### Criterio de aprobación

- La cantidad de páginas es correcta aunque la división no sea exacta.
- No usa `if`.

#### Salida esperada

```
Páginas: 5
Productos en la última: 5
```

#### Solución de referencia

```java
// Encargo - Las paginas del catalogo: division entera, resto y ternario.
public class Paginas {
    public static void main(String[] args) {
        int productos = 53;
        int porPagina = 12;
        int completas = productos / porPagina;
        int sobran = productos % porPagina;
        int paginas = sobran == 0 ? completas : completas + 1;
        int enLaUltima = sobran == 0 ? porPagina : sobran;

        System.out.println("Páginas: " + paginas);
        System.out.println("Productos en la última: " + enLaUltima);
    }
}
```

### Prueba del sello

#### ¿Cuánto da `2 + 3 * 4`? ¿Por qué?

`14`: la multiplicación se hace antes que la suma.

#### ¿Qué muestra `System.out.println("A" + 1 + 2);`?

`A12`: como el primero es un texto, cada `+` une.

#### ¿Qué hace `x % 2 == 0`?

Dice si `x` es par: el resto de dividirlo por 2 es cero.

#### ¿Por qué `x != 0 && 10 / x > 1` nunca divide por cero?

Porque `&&` hace cortocircuito: si `x != 0` es `false`, el lado derecho no se evalúa.

#### ¿Qué devuelve `edad >= 18 ? "adulto" : "menor"` si `edad` vale 15?

`"menor"`.

### Soluciones (docente)

Sale de `18-Java/03-Operadores` (unidad 2).

## R01-N03 · Textos: String, equals y printf

```meta
tipo: tema
padre: R01-N02
precio: 10
criatura: ogre
temas: prog.cadenas, prog.salida
```

### Crónica

La oficina de sellos de la Aduana está tapada de pergaminos: nombres mal escritos, apellidos en mayúsculas, espacios de más. El Escriba Jefe mira a Zed con ojeras.

Zed piensa en copiar un sello y ahorrarse la fila. Lo copia perfecto, letra por letra… y la Aduana lo rechaza.

—Los textos son lo que más se rompe —dice {mentor}—. Y tienen una trampa que se cobró más víctimas que cualquier monstruo: en el Imperio, **dos textos iguales no siempre son el mismo texto**. Prestá atención, Zed.

### Objetivos

- Usar los métodos principales de `String`: largo, caracteres, partes, búsqueda, mayúsculas y reemplazos.
- Comparar textos correctamente con `equals` (y no con `==`).
- Armar textos largos con `StringBuilder`.
- Dar formato a la salida con `printf` y `String.format`.

### Antes de empezar

- Variables, tipos y operadores.

### Explicación

#### Un `String` es un objeto
`String` es una **clase**: cada texto es un objeto con **métodos** que se llaman con
un punto. Los caracteres se numeran desde **0**.
```java
String nombre = "Kira Valdez";
nombre.length();              // 11
nombre.charAt(0);             // 'K'
nombre.charAt(nombre.length() - 1);   // 'z', el último
```

#### Los métodos más usados
| Método | Qué devuelve | Ejemplo con `"Kira Valdez"` |
|---|---|---|
| `length()` | la cantidad de caracteres | `11` |
| `charAt(i)` | el carácter en la posición `i` | `charAt(5)` → `'V'` |
| `substring(a, b)` | de la posición `a` hasta `b` (sin incluir `b`) | `substring(0, 4)` → `"Kira"` |
| `substring(a)` | desde `a` hasta el final | `substring(5)` → `"Valdez"` |
| `indexOf(texto)` | dónde aparece por primera vez (o `-1`) | `indexOf(" ")` → `4` |
| `contains(texto)` | si aparece | `contains("Val")` → `true` |
| `startsWith` / `endsWith` | si empieza / termina así | `endsWith("ez")` → `true` |
| `toUpperCase()` / `toLowerCase()` | en mayúsculas / minúsculas | `"KIRA VALDEZ"` |
| `trim()` / `strip()` | sin espacios al principio y al final | `"  hola "` → `"hola"` |
| `replace(a, b)` | cambia todas las apariciones de `a` por `b` | `replace("a", "4")` |
| `isEmpty()` / `isBlank()` | si está vacío / si solo tiene espacios | |
| `split(sep)` | lo corta en partes (un array) | `split(" ")` → `["Kira", "Valdez"]` |
| `repeat(n)` | repetido `n` veces | `"-".repeat(5)` → `"-----"` |

Los `String` son **inmutables**: ningún método cambia el texto original, todos
devuelven uno nuevo. Por eso hay que guardar el resultado:
```java
nombre.toUpperCase();              // no cambia nada
nombre = nombre.toUpperCase();     // ahora sí
```

#### La trampa: `==` contra `equals`
`==` entre objetos compara si son **el mismo objeto** en memoria, no si tienen el
mismo contenido. Dos textos iguales pueden ser objetos distintos:
```java
String a = "kira";
String b = new String("kira");
System.out.println(a == b);              // false: son dos objetos distintos
System.out.println(a.equals(b));         // true: tienen el mismo contenido
System.out.println(a.equalsIgnoreCase("KIRA"));   // true: sin mirar mayúsculas
```
A veces `==` da `true` por casualidad (Java reutiliza los textos literales), y eso
lo hace más peligroso: el programa anda en tus pruebas y falla con datos que vienen
del teclado. **Los textos se comparan siempre con `equals`.**

Para ordenar alfabéticamente, `a.compareTo(b)` devuelve un número negativo si `a` va
antes, 0 si son iguales y positivo si va después.

#### `StringBuilder`: armar textos de a pedazos
Como un `String` no cambia, cada `+` crea uno nuevo. Para armar un texto largo en
muchos pasos se usa `StringBuilder`, que sí se modifica:
```java
StringBuilder sb = new StringBuilder();
sb.append("Kira").append(" · ").append(30).append(" de vida");
sb.insert(0, "> ");
sb.reverse();                  // también invierte
String resultado = sb.toString();
```

#### `printf`: formato
`System.out.printf` muestra un texto con **huecos** que se completan con valores:
```java
System.out.printf("%s tiene %d de vida y %.2f de oro%n", "Kira", 30, 12.5);
```
| Hueco | Para | Ejemplo | Resultado |
|---|---|---|---|
| `%s` | textos (y cualquier cosa) | `"%s", "Kira"` | `Kira` |
| `%d` | enteros | `"%d", 30` | `30` |
| `%.2f` | decimales con 2 cifras | `"%.2f", 12.5` | `12.50` |
| `%5d` / `%-10s` | ancho mínimo (derecha / izquierda) | `"%5d", 42` | `   42` |
| `%05d` | rellenar con ceros | `"%05d", 42` | `00042` |
| `%n` | salto de línea | | |

`String.format` hace lo mismo pero **devuelve** el texto en vez de mostrarlo:
```java
String linea = String.format("%-10s %5d", "Kira", 30);
```

#### El punto decimal y la configuración regional
`printf` y `String.format` usan la **configuración regional** de la compu. En una
compu configurada en español de Argentina, `%.2f` muestra `12,50` con coma; en una en
inglés, `12.50` con punto. Para que un programa muestre lo mismo en cualquier compu,
en este curso escribimos esta línea al principio del `main` de los programas que
muestran o leen decimales:
```java
Locale.setDefault(Locale.US);   // punto decimal en printf y Scanner (import java.util.Locale;)
```
`import java.util.Locale;` va arriba de todo, antes de la clase: le avisa al
compilador en qué **paquete** está la clase `Locale` (los paquetes se ven más
adelante). `String` y `System` no necesitan `import` porque están en `java.lang`,
que se importa solo.

> **Si venís de C.** Un `String` no es un array de `char` terminado en `\0`: es un
> objeto con su largo y sus métodos. `printf` es casi igual al de C (con `%n` en
> lugar de `\n`).

### Código de ejemplo

```java
/*
 * Textos: la oficina de sellos de la Aduana.
 */
import java.util.Locale;

public class OficinaSellos {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);                     // punto decimal en cualquier compu

        String entrada = "   kira VALDEZ   ";
        String limpio = entrada.trim();
        System.out.println("Limpio: [" + limpio + "]");

        int espacio = limpio.indexOf(" ");
        String nombre = limpio.substring(0, espacio);
        String apellido = limpio.substring(espacio + 1);
        String prolijo = nombre.substring(0, 1).toUpperCase() + nombre.substring(1).toLowerCase()
                + " " + apellido.charAt(0) + apellido.substring(1).toLowerCase();
        System.out.println("Prolijo: " + prolijo);
        System.out.println("Letras: " + prolijo.length() + ", iniciales: " + prolijo.charAt(0) + prolijo.charAt(espacio + 1));

        // == contra equals
        String buscado = "Kira Valdez";
        String armado = new String(prolijo);              // un objeto nuevo, con el mismo contenido
        System.out.println("¿Mismo objeto (==)? " + (armado == buscado));
        System.out.println("¿Mismo texto (equals)? " + armado.equals(buscado));
        System.out.println("¿Igual sin mayúsculas? " + "KIRA VALDEZ".equalsIgnoreCase(buscado));

        // split y StringBuilder
        String equipaje = "espada,mapa,brújula";
        String[] cosas = equipaje.split(",");
        StringBuilder lista = new StringBuilder();
        lista.append(cosas.length).append(" cosas: ");
        lista.append(cosas[0]).append(" / ").append(cosas[1]).append(" / ").append(cosas[2]);
        System.out.println(lista.toString());

        // printf y String.format
        System.out.println("=".repeat(28));
        System.out.printf("%-12s %6s %8s%n", "Viajero", "Días", "Tasa");
        System.out.printf("%-12s %6d %8.2f%n", "Kira", 7, 12.5);
        System.out.printf("%-12s %6d %8.2f%n", "Bron", 12, 101.25);
        String sello = String.format("SELLO-%05d", 42);
        System.out.println(sello);
    }
}
```

### Salida esperada

```
Limpio: [kira VALDEZ]
Prolijo: Kira Valdez
Letras: 11, iniciales: KV
¿Mismo objeto (==)? false
¿Mismo texto (equals)? true
¿Igual sin mayúsculas? true
3 cosas: espada / mapa / brújula
============================
Viajero        Días     Tasa
Kira              7    12.50
Bron             12   101.25
SELLO-00042
```

### ¿Para qué sirve?

Casi todos los datos que entran a un sistema son textos: nombres, direcciones, códigos, líneas de un archivo. Limpiarlos (`trim`, mayúsculas), partirlos (`split`, `substring`) y compararlos bien (`equals`) es trabajo diario en cualquier empresa. Y `printf` arma los reportes, tickets y tablas que la gente lee.

### Errores habituales

**Ogro: comparar textos con `==`.** `if (respuesta == "si")` puede dar `false`
aunque la persona haya escrito `si`. Va `respuesta.equals("si")`.

**Orco: posición fuera del texto.**
```
Exception in thread "main" java.lang.StringIndexOutOfBoundsException: index 11, length 11
        at java.base/java.lang.String.charAt(String.java:1555)
        at Oficina.main(Oficina.java:6)
```
Las posiciones van de `0` a `length() - 1`.

**Ogro: olvidarse de guardar el resultado.** `nombre.trim();` sola no hace nada:
los `String` no cambian. Va `nombre = nombre.trim();`.

**Goblin: el hueco equivocado en `printf`.** `printf("%d", 12.5)` corta el programa
con `IllegalFormatConversionException: d != java.lang.Double`. `%d` es para enteros
y `%f` para decimales.

**Ogro: coma en lugar de punto.** Sin `Locale.setDefault(Locale.US)`, en una compu en
español `%.2f` muestra `12,50`.

### Micro-misión R01-N03-P1 · Los nombres torcidos

```meta
lugar: La oficina de sellos de la Aduana
personajes: Zed, Gheco, Nadia, el Escriba Jefe
carta: Métodos de String | .trim() saca espacios · .toUpperCase() · .length() · .charAt(0)
recompensa: xp 10, oro 10
```

#### Escena
En la oficina de sellos, el Escriba Jefe tiene los ojos rojos de copiar nombres con espacios de más y en minúsculas. —Arreglámelos —le pide a Zed—, que yo ya no veo.

#### Gheco sugiere
Un `String` sabe hacer cosas: `.trim()` saca los espacios de los costados, `.toUpperCase()` lo pasa a mayúsculas y `.length()` dice cuántas letras tiene.

#### Desafío
Limpiá el nombre y pasalo a mayúsculas.

#### Código inicial
```java
public class Nombres {
    public static void main(String[] args) {
        String crudo = "   nadia   ";
        String limpio = crudo.___.___;
        System.out.println("[" + limpio + "] tiene " + limpio.length() + " letras");
    }
}
```

#### Salida esperada
```
[NADIA] tiene 5 letras
```

#### Solución
```java
public class Nombres {
    public static void main(String[] args) {
        String crudo = "   nadia   ";
        String limpio = crudo.trim().toUpperCase();
        System.out.println("[" + limpio + "] tiene " + limpio.length() + " letras");
    }
}
```

#### Al superarla
«NADIA», sin un espacio de más. Nadia, que miraba por encima del hombro, carraspea. —Está bien escrito. Por una vez.

#### Imagen
- Una oficina tapada de pergaminos; el Escriba Jefe, ojeroso, con anteojos en la punta de la nariz.
- Un pergamino donde «   nadia   » se convierte en «NADIA».

### Micro-misión R01-N03-P2 · El sello falsificado

```meta
lugar: La oficina de sellos de la Aduana
personajes: Zed, Gheco, Nadia, el Escriba Jefe
criatura: ogro
carta: == contra equals | == pregunta si es el MISMO objeto · .equals() compara el texto · para textos, siempre equals
recompensa: xp 15, oro 15
```

#### Escena
Zed copia un sello que dice exactamente lo mismo que el original: «APROBADO». La Aduana lo compara… y dice que **no** es igual.
—Dos textos iguales no siempre son **el mismo** texto —dice Gheco—. Ese es el ogro preferido del Imperio.

#### Gheco sugiere
Con textos, `==` pregunta si son **el mismo objeto**, no si dicen lo mismo, y a veces da `false` aunque el texto sea igual. Para comparar el contenido se usa `.equals()`.

#### Desafío
Compará el contenido de los dos sellos.

#### Código inicial
```java
public class Sello {
    public static void main(String[] args) {
        String original = "APROBADO";
        String copia = new String("APROBADO");
        System.out.println("¿Mismo objeto? " + (original == copia));
        System.out.println("¿Mismo texto? " + ___);
    }
}
```

#### Salida esperada
```
¿Mismo objeto? false
¿Mismo texto? true
```

#### Solución
```java
public class Sello {
    public static void main(String[] args) {
        String original = "APROBADO";
        String copia = new String("APROBADO");
        System.out.println("¿Mismo objeto? " + (original == copia));
        System.out.println("¿Mismo texto? " + original.equals(copia));
    }
}
```

#### Al superarla
«Mismo objeto: false. Mismo texto: true.» El Escriba Jefe se ríe. —¡Así me engañaron cien veces! —Zed no dice que él también pensaba engañarlo.

#### Imagen
- Dos sellos idénticos «APROBADO» sobre la mesa; entre ellos, un `==` tachado y un `.equals()` brillando.
- El Escriba Jefe riéndose; Zed silba mirando al techo.

### Micro-misión R01-N03-P3 · La lista de una sola tirada

```meta
lugar: La oficina de sellos de la Aduana
personajes: Zed, Gheco, Nadia, el Escriba Jefe
carta: StringBuilder | sb.append("…") agrega · sb.toString() da el texto · para armar textos de a pedazos
recompensa: xp 10, oro 10
```

#### Escena
El Escriba Jefe quiere la lista de los viajeros de hoy en una sola línea, separados por guiones. Pegar pedazos con `+` lo vuelve loco: cada `+` arma un texto nuevo.

#### Gheco sugiere
`StringBuilder` arma un texto de a pedazos: `append` agrega al final y `toString()` devuelve el texto armado.

#### Desafío
Agregá a Nadia y al mercader con `append`, como está hecho con Zed.

#### Código inicial
```java
public class Lista {
    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder();
        sb.append("Zed").append(" - ");
        sb.___("Nadia").___(" - ");
        sb.___("un mercader");
        System.out.println(sb.toString());
    }
}
```

#### Salida esperada
```
Zed - Nadia - un mercader
```

#### Solución
```java
public class Lista {
    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder();
        sb.append("Zed").append(" - ");
        sb.append("Nadia").append(" - ");
        sb.append("un mercader");
        System.out.println(sb.toString());
    }
}
```

#### Al superarla
La lista sale de un tirón. —Nadia no es una viajera —protesta ella. —Hoy sí —dice Zed—: viaja conmigo.

#### Imagen
- Una tira de pergamino que se arma sola, nombre por nombre, con guiones de luz.
- Nadia, ofendida, con los brazos en jarra; Zed sonriendo torcido.

### Micro-misión R01-N03-P4 · La tabla de tarifas

```meta
lugar: La oficina de sellos de la Aduana
personajes: Zed, Gheco, Nadia, el Escriba Jefe
carta: printf | System.out.printf(Locale.US, "%-8s %6.2f%n", nombre, precio) · %s texto · %d entero · %.2f decimales · %n salto
recompensa: xp 15, oro 15
```

#### Escena
—La tabla de tarifas tiene que quedar **prolija** —pide el Escriba—: el nombre a la izquierda y el precio con dos decimales, alineado.

#### Gheco sugiere
`printf` usa un **formato**: `%s` para textos, `%d` para enteros, `%.2f` para decimales con 2 cifras, `%n` para saltar de línea. Un número antes (`%-8s`, `%6.2f`) fija el ancho. Con `Locale.US`, el decimal es un punto en cualquier compu.

#### Desafío
Completá el formato del precio: ancho 6 y 2 decimales.

#### Código inicial
```java
import java.util.Locale;

public class Tarifas {
    public static void main(String[] args) {
        String formato = "%-8s ___%n";
        System.out.printf(Locale.US, formato, "Barril", 2.5);
        System.out.printf(Locale.US, formato, "Caballo", 12.0);
        System.out.printf(Locale.US, formato, "Carta", 0.75);
    }
}
```

#### Salida esperada
```
Barril     2.50
Caballo   12.00
Carta      0.75
```

#### Solución
```java
import java.util.Locale;

public class Tarifas {
    public static void main(String[] args) {
        String formato = "%-8s %6.2f%n";
        System.out.printf(Locale.US, formato, "Barril", 2.5);
        System.out.printf(Locale.US, formato, "Caballo", 12.0);
        System.out.printf(Locale.US, formato, "Carta", 0.75);
    }
}
```

#### Al superarla
La tabla queda perfecta, con los números alineados como soldados. El Escriba Jefe la cuelga en la puerta. En la ventanilla de al lado, alguien empieza a hacer preguntas.

#### Imagen
- Una tabla de tarifas tallada en bronce, con precios perfectamente alineados.
- El Escriba Jefe la cuelga en la puerta de la oficina.

### Misión R01-N03-M1 · El registro del escriba

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El escriba recibió el nombre `"  lía   FERRARI "` (con espacios de más). Guardalo en
una variable y mostrá:

1. El nombre sin espacios al principio ni al final, entre corchetes.
2. El nombre en mayúsculas.
3. La cantidad de letras del nombre de pila (hasta el primer espacio).
4. Si contiene `"FERR"`.
5. El nombre con cada `A` reemplazada por `@`.

#### Criterio de aprobación

- Usa `trim`, `toUpperCase`, `indexOf`, `contains` y `replace`.
- Guarda los resultados (no llama a los métodos sin usar lo que devuelven).

#### Salida esperada

```
[lía   FERRARI]
LÍA   FERRARI
Letras del nombre: 3
¿Contiene FERR? true
LÍ@   FERR@RI
```

#### Solución de referencia

```java
// Mision 1 - El registro del escriba: metodos de String.
public class Escriba {
    public static void main(String[] args) {
        String crudo = "  lía   FERRARI ";
        String limpio = crudo.trim();
        String mayus = limpio.toUpperCase();
        int espacio = limpio.indexOf(" ");

        System.out.println("[" + limpio + "]");
        System.out.println(mayus);
        System.out.println("Letras del nombre: " + limpio.substring(0, espacio).length());
        System.out.println("¿Contiene FERR? " + limpio.contains("FERR"));
        System.out.println(mayus.replace("A", "@"));
    }
}
```

### Misión R01-N03-M2 · La contraseña del portón

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La contraseña del portón es `"cafe"`. Simulá tres intentos guardados en variables:
`"cafe"`, `"CAFE"` y un texto armado en el momento con `new String("ca") + "fe"`.
Para cada uno mostrá el resultado de compararlo con `==`, con `equals` y con
`equalsIgnoreCase`. Terminá con una línea que explique cuál hay que usar.

#### Criterio de aprobación

- Muestra las tres comparaciones para los tres intentos.
- Se ve que `==` falla con el texto armado aunque tenga el mismo contenido.

#### Salida esperada

```
intento1: == true, equals true, ignoreCase true
intento2: == false, equals false, ignoreCase true
intento3: == false, equals true, ignoreCase true
Los textos se comparan con equals, nunca con ==.
```

#### Solución de referencia

```java
// Mision 2 - La contrasenia del porton: == contra equals.
public class Porton {
    public static void main(String[] args) {
        String clave = "cafe";
        String intento1 = "cafe";
        String intento2 = "CAFE";
        String intento3 = new String("ca") + "fe";

        System.out.println("intento1: == " + (intento1 == clave) + ", equals " + intento1.equals(clave) + ", ignoreCase " + intento1.equalsIgnoreCase(clave));
        System.out.println("intento2: == " + (intento2 == clave) + ", equals " + intento2.equals(clave) + ", ignoreCase " + intento2.equalsIgnoreCase(clave));
        System.out.println("intento3: == " + (intento3 == clave) + ", equals " + intento3.equals(clave) + ", ignoreCase " + intento3.equalsIgnoreCase(clave));
        System.out.println("Los textos se comparan con equals, nunca con ==.");
    }
}
```

### Misión R01-N03-M3 · La tabla de tarifas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Mostrá con `printf` la tabla de tarifas de la Aduana: tres mercancías con su
cantidad y su precio unitario, alineadas en columnas (nombre a la izquierda en 10
lugares, cantidad a la derecha en 5, precio y subtotal a la derecha en 9 con 2
decimales), y al final el total. Recordá `Locale.setDefault(Locale.US)`.

Mercancías: sal (4 × 12.5), seda (2 × 310.0) y hierro (10 × 7.25).

#### Criterio de aprobación

- Usa `printf` con anchos y `%.2f`.
- Tiene `Locale.setDefault(Locale.US)` para que el punto decimal sea siempre punto.
- El total está bien calculado.

#### Salida esperada

```
Mercancía   Cant    Precio  Subtotal
sal            4     12.50     50.00
seda           2    310.00    620.00
hierro        10      7.25     72.50
TOTAL                         742.50
```

#### Solución de referencia

```java
// Mision 3 - La tabla de tarifas: printf con anchos y decimales.
import java.util.Locale;

public class Tarifas {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        double subSal = 4 * 12.5;
        double subSeda = 2 * 310.0;
        double subHierro = 10 * 7.25;

        System.out.printf("%-10s %5s %9s %9s%n", "Mercancía", "Cant", "Precio", "Subtotal");
        System.out.printf("%-10s %5d %9.2f %9.2f%n", "sal", 4, 12.5, subSal);
        System.out.printf("%-10s %5d %9.2f %9.2f%n", "seda", 2, 310.0, subSeda);
        System.out.printf("%-10s %5d %9.2f %9.2f%n", "hierro", 10, 7.25, subHierro);
        System.out.printf("%-26s %9.2f%n", "TOTAL", subSal + subSeda + subHierro);
    }
}
```

### Encargo R01-N03-E1 · El usuario del sistema

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un sistema arma el usuario de cada empleado con la inicial del nombre, el apellido
completo y los dos últimos dígitos del año de ingreso, todo en minúsculas. Para
`"Martina"`, `"Sosa"` y el año 2019 da `msosa19`. Armalo con `StringBuilder` y
mostralo. Mostrá también el usuario al revés (con `reverse`) y un código de legajo con
`String.format` y ceros a la izquierda (`LEG-00042` para el legajo 42).

#### Criterio de aprobación

- Arma el usuario con `StringBuilder`.
- Usa `String.format` con `%05d`.

#### Salida esperada

```
Usuario: msosa19
Al revés: 91asosm
Legajo: LEG-00042
```

#### Solución de referencia

```java
// Encargo - El usuario del sistema: StringBuilder y String.format.
public class Usuario {
    public static void main(String[] args) {
        String nombre = "Martina";
        String apellido = "Sosa";
        int anio = 2019;
        int legajo = 42;

        StringBuilder sb = new StringBuilder();
        sb.append(nombre.charAt(0)).append(apellido).append(anio % 100);
        String usuario = sb.toString().toLowerCase();

        System.out.println("Usuario: " + usuario);
        System.out.println("Al revés: " + new StringBuilder(usuario).reverse());
        System.out.println("Legajo: " + String.format("LEG-%05d", legajo));
    }
}
```

### Prueba del sello

#### ¿Por qué no hay que comparar textos con `==`?

Porque `==` compara si son el mismo objeto, no si tienen el mismo contenido. Dos textos iguales pueden ser objetos distintos. Se usa `equals`.

#### ¿Qué devuelve `"Imperio".substring(1, 4)`?

`"mpe"`: desde la posición 1 hasta la 4 sin incluirla.

#### ¿Por qué `nombre.trim();` sola no hace nada?

Porque los `String` son inmutables: `trim` devuelve un texto nuevo, y hay que guardarlo.

#### ¿Qué muestra `printf("%05d", 42)`?

`00042`.

#### ¿Para qué sirve `Locale.setDefault(Locale.US)` en este curso?

Para que `printf` y `Scanner` usen el punto como separador decimal en cualquier compu, y la salida sea siempre la misma.

### Soluciones (docente)

Sale de `18-Java/04-Strings` (unidad 2). La convención `Locale.setDefault(Locale.US)` es del curso: el súper test y las salidas esperadas se generan con esa línea y se comprueban con la compu en español y en inglés.

## R01-N04 · Leer del teclado: Scanner, Math y Random

```meta
tipo: tema
padre: R01-N03
precio: 10
criatura: goblin
temas: prog.entrada, prog.matematica-azar
```

### Crónica

En la ventanilla de la Aduana, Nadia ya no lee pergaminos: **pregunta**. Nombre, edad, cuánto oro trae cada viajero. Anota cada respuesta y hace cuentas con una tablilla de fórmulas. Cuando le toca a Zed, contesta «muchos» donde iba un número.

—Un programa que no escucha siempre dice lo mismo —dice {mentor}—. Enseñale a preguntar, Zed. Pero ojo: la gente responde cualquier cosa. Vos lo sabés mejor que nadie.

### Objetivos

- Leer textos y números del teclado con `Scanner`.
- Evitar la trampa de mezclar `nextInt` con `nextLine`.
- Convertir textos a números con `Integer.parseInt` y `Double.parseDouble`.
- Usar las funciones de `Math` y números al azar con `Random`.

### Antes de empezar

- Textos y `printf` (Textos: String, equals y printf).

### Explicación

#### `Scanner`: leer del teclado
`Scanner` es la clase que lee lo que se escribe en la terminal. Está en el paquete
`java.util`, así que va con `import`:
```java
import java.util.Scanner;

Scanner teclado = new Scanner(System.in);     // System.in es la entrada estándar
System.out.print("Nombre: ");
String nombre = teclado.nextLine();           // lee la línea entera
System.out.print("Edad: ");
int edad = teclado.nextInt();                 // lee un entero
double oro = teclado.nextDouble();            // lee un decimal
```
| Método | Lee |
|---|---|
| `nextLine()` | la línea completa (hasta el Enter), con espacios |
| `next()` | una palabra (hasta el próximo espacio) |
| `nextInt()` / `nextLong()` / `nextDouble()` | un número |
| `hasNextInt()` | si lo que viene es un entero (sin leerlo) |

`nextDouble` también depende de la configuración regional: en una compu en español
espera `12,5`. Con `Locale.setDefault(Locale.US)` **antes** de crear el `Scanner`,
espera `12.5` en cualquier compu.

#### La trampa de `nextInt` + `nextLine`
`nextInt()` lee el número pero **deja el Enter** pendiente. El `nextLine()` que
viene después encuentra ese Enter y devuelve una línea vacía:
```java
int edad = teclado.nextInt();       // escribís 19 y Enter: queda el Enter
String ciudad = teclado.nextLine(); // devuelve "" al instante
```
La forma más segura de evitarlo: **leer siempre líneas** y convertirlas:
```java
int edad = Integer.parseInt(teclado.nextLine().trim());
double oro = Double.parseDouble(teclado.nextLine().trim());
```
Así cada lectura consume su Enter. Es la forma que usamos en el curso.

#### Cuando no escriben un número
`Integer.parseInt("muchos")` corta el programa con `NumberFormatException`. Para
avisar en lugar de romperse hay dos caminos: preguntar antes con `hasNextInt()`, o
atrapar la excepción con `try`/`catch` (lo vas a ver en el nodo de excepciones). En
el nodo de bucles vas a aprender a **volver a preguntar** hasta que la respuesta sea
válida.

#### `Math`: la tablilla de fórmulas
`Math` tiene funciones `static` que se usan sin crear nada:
| Método | Qué hace | Ejemplo | Resultado |
|---|---|---|---|
| `Math.abs(x)` | valor absoluto | `Math.abs(-7)` | `7` |
| `Math.max(a, b)` / `Math.min(a, b)` | el mayor / el menor | `Math.max(3, 9)` | `9` |
| `Math.pow(b, e)` | potencia (devuelve `double`) | `Math.pow(2, 10)` | `1024.0` |
| `Math.sqrt(x)` | raíz cuadrada | `Math.sqrt(81)` | `9.0` |
| `Math.round(x)` | redondeo al entero más cercano (`long`) | `Math.round(2.5)` | `3` |
| `Math.floor(x)` / `Math.ceil(x)` | hacia abajo / hacia arriba | `Math.ceil(2.1)` | `3.0` |
| `Math.PI` | π | | `3.141592653589793` |

#### `Random`: el azar
```java
import java.util.Random;

Random dado = new Random(42);        // con semilla: siempre la misma secuencia
int tirada = dado.nextInt(6) + 1;    // entre 1 y 6
double chance = dado.nextDouble();   // entre 0.0 y 1.0 (sin incluir 1)
boolean moneda = dado.nextBoolean();
```
`nextInt(n)` da un entero entre `0` y `n - 1`. Con una **semilla** fija
(`new Random(42)`) la secuencia es siempre la misma, en cualquier compu: sirve para
probar y para que tu salida coincida con la esperada. Sin semilla
(`new Random()`) cada ejecución es distinta, como en un juego de verdad.

#### Probar un programa con entrada sin tipearla cada vez
```bash
java Ventanilla.java < entrada.txt
printf 'Kira\n19\n120.5\n' | java Ventanilla.java
```
Así funcionan las **entradas de ejemplo** de las misiones: lo que escribirías, línea
por línea. En la salida esperada no aparece lo que se tipea, solo lo que el programa
muestra.

> **Si venís de C.** `Scanner` reemplaza a `scanf` y `Integer.parseInt` a `atoi`,
> pero con una diferencia importante: si el texto no es un número, Java no devuelve
> 0 en silencio sino que lanza una excepción.

### Código de ejemplo

```java
/*
 * Scanner, Math y Random: la ventanilla de la Aduana.
 */
import java.util.Locale;
import java.util.Random;
import java.util.Scanner;

public class Ventanilla {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);                       // antes de crear el Scanner
        Scanner teclado = new Scanner(System.in);

        System.out.print("Nombre completo: ");
        String nombre = teclado.nextLine().trim();
        System.out.print("Edad: ");
        int edad = Integer.parseInt(teclado.nextLine().trim());
        System.out.print("Oro que trae: ");
        double oro = Double.parseDouble(teclado.nextLine().trim());
        System.out.println();

        System.out.println("Registro de " + nombre + " (" + edad + " años)");
        double tasa = Math.max(5, oro * 0.1);               // la tasa mínima es 5
        System.out.printf("Tasa: %.2f (redondeada: %d)%n", tasa, Math.round(tasa));
        System.out.printf("Años hasta los 100: %d%n", Math.abs(100 - edad));
        System.out.printf("Raíz del oro: %.3f%n", Math.sqrt(oro));

        Random dado = new Random(2026);                     // semilla fija: siempre la misma secuencia
        int tirada1 = dado.nextInt(6) + 1;
        int tirada2 = dado.nextInt(6) + 1;
        System.out.println("Dados de la suerte: " + tirada1 + " y " + tirada2);
        System.out.println("¿Revisión sorpresa? " + (dado.nextInt(100) < 30 ? "sí" : "no"));
    }
}
```

### Entrada de ejemplo

```
Kira Valdez
19
120.5
```

### Salida esperada

```
Nombre completo: Edad: Oro que trae: 
Registro de Kira Valdez (19 años)
Tasa: 12.05 (redondeada: 12)
Años hasta los 100: 81
Raíz del oro: 10.977
Dados de la suerte: 6 y 5
¿Revisión sorpresa? no
```

### ¿Para qué sirve?

Todo programa de consola que interactúa con alguien lee datos: un cajero, un formulario de inscripción, una calculadora, un menú. Convertir y validar lo que entra es lo que separa a un programa que funciona en la demo de uno que funciona con usuarios reales. `Math` aparece en cualquier cálculo (geometría, finanzas, juegos) y `Random` en simulaciones, juegos y pruebas.

### Errores habituales

**Ogro: el `nextLine` que no espera.** Después de `nextInt()`, un `nextLine()`
devuelve una línea vacía. Leé todo con `nextLine()` y convertí con `parseInt`.

**Goblin: letras donde iba un número.**
```
Exception in thread "main" java.lang.NumberFormatException: For input string: "muchos"
        at java.base/java.lang.Integer.parseInt(Integer.java:661)
        at Ventanilla.main(Ventanilla.java:15)
```

**Goblin: coma o punto decimal.** Sin `Locale.setDefault(Locale.US)`, en una compu en
español `nextDouble()` con `120.5` lanza `InputMismatchException`. Con
`Double.parseDouble` siempre se usa punto.

**Esqueleto: falta el `import`.**
```
Ventanilla.java:5: error: cannot find symbol
        Scanner teclado = new Scanner(System.in);
        ^
  symbol:   class Scanner
```
Va `import java.util.Scanner;` arriba de todo.

**Ogro: `nextInt(6)` da de 0 a 5.** Para un dado de 1 a 6, sumale 1.

### Micro-misión R01-N04-P1 · El interrogatorio

```meta
lugar: La ventanilla de la Aduana
personajes: Zed, Gheco, Nadia
carta: Scanner | Scanner sc = new Scanner(System.in); · sc.nextLine() lee una línea · import java.util.Scanner;
recompensa: xp 10, oro 10
```

#### Escena
En la ventanilla, Nadia ya no lee pergaminos: **pregunta**. —Ahora lo escribís vos —le dice a Zed—. Que el programa pregunte el nombre y salude.

#### Gheco sugiere
`Scanner` lee lo que se escribe en el teclado. Se crea con `new Scanner(System.in)` y `nextLine()` lee una línea entera. Hay que importarlo: `import java.util.Scanner;`. Acá la **Entrada** ya viene escrita: es lo que «tipearía» el viajero.

#### Desafío
Leé el nombre con `nextLine`.

#### Código inicial
```java
import java.util.Scanner;

public class Ventanilla {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Nombre: ");
        String nombre = sc.___;
        System.out.println();
        System.out.println("Bienvenido al Imperio, " + nombre);
    }
}
```

#### Entrada
```
Baldo
```

#### Salida esperada
```
Nombre: 
Bienvenido al Imperio, Baldo
```

#### Solución
```java
import java.util.Scanner;

public class Ventanilla {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Nombre: ");
        String nombre = sc.nextLine();
        System.out.println();
        System.out.println("Bienvenido al Imperio, " + nombre);
    }
}
```

#### Al superarla
«Bienvenido al Imperio, Baldo.» El mercader de la fila, un hombrecito de orejas puntiagudas, se va contento. —Ese no es de acá —murmura Gheco.

#### Imagen
- La ventanilla de la Aduana: Nadia del otro lado del vidrio con su libreta.
- Un mercader de orejas puntiagudas y antiparras (Baldo, de paso por el Imperio) recibe su sello contento.

### Micro-misión R01-N04-P2 · El salto de línea perdido

```meta
lugar: La ventanilla de la Aduana
personajes: Zed, Gheco, Nadia
criatura: esqueleto
carta: nextInt + nextLine | nextInt() deja el Enter en la fila · un sc.nextLine() de más lo saca
recompensa: xp 15, oro 15
```

#### Escena
Ahora la ventanilla pregunta la edad (un número) y después el oficio. Pero el oficio sale **vacío**, como si el viajero no hubiera dicho nada.

#### Gheco sugiere
`nextInt()` lee el número pero **deja el Enter** esperando. El `nextLine()` que sigue se lleva ese Enter vacío. Solución: un `sc.nextLine();` extra justo después de `nextInt()`.

#### Desafío
Agregá la línea que se lleva el Enter que quedó.

#### Código inicial
```java
import java.util.Scanner;

public class Edad {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int edad = sc.nextInt();
        String oficio = sc.nextLine();
        System.out.println("Edad: " + edad);
        System.out.println("Oficio: [" + oficio + "]");
    }
}
```

#### Entrada
```
18
ladrón de techos
```

#### Salida esperada
```
Edad: 18
Oficio: [ladrón de techos]
```

#### Solución
```java
import java.util.Scanner;

public class Edad {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int edad = sc.nextInt();
        sc.nextLine();
        String oficio = sc.nextLine();
        System.out.println("Edad: " + edad);
        System.out.println("Oficio: [" + oficio + "]");
    }
}
```

#### Al superarla
«Oficio: ladrón de techos.» Nadia levanta la vista. —¿Pusiste eso en un formulario oficial? —Es lo que dijo el viajero —responde Zed, inocente.

#### Imagen
- Un formulario donde el casillero «Oficio» pasa de vacío a lleno.
- Nadia, incrédula, mira el formulario; Zed sonríe torcido.

### Micro-misión R01-N04-P3 · La tablilla de fórmulas

```meta
lugar: La ventanilla de la Aduana
personajes: Zed, Gheco, Nadia
carta: Math | Math.max(a, b) · Math.pow(b, e) · Math.sqrt(x) · Math.abs(x) · Math.round(x)
recompensa: xp 10, oro 10
```

#### Escena
Para tasar un terreno del cuartel, Nadia usa una **tablilla de fórmulas**: el lado de un terreno cuadrado a partir de su superficie, y cuál de dos ofertas es mayor.

#### Gheco sugiere
`Math` ya trae fórmulas listas: `Math.sqrt(x)` (raíz cuadrada), `Math.pow(base, exponente)`, `Math.max(a, b)`, `Math.abs(x)`.

#### Desafío
Calculá el lado con la raíz cuadrada.

#### Código inicial
```java
public class Terreno {
    public static void main(String[] args) {
        double superficie = 144;
        double lado = ___;
        System.out.println("Lado: " + lado);
        System.out.println("Mejor oferta: " + Math.max(300, 450));
        System.out.println("2 a la 10: " + Math.pow(2, 10));
    }
}
```

#### Salida esperada
```
Lado: 12.0
Mejor oferta: 450
2 a la 10: 1024.0
```

#### Solución
```java
public class Terreno {
    public static void main(String[] args) {
        double superficie = 144;
        double lado = Math.sqrt(superficie);
        System.out.println("Lado: " + lado);
        System.out.println("Mejor oferta: " + Math.max(300, 450));
        System.out.println("2 a la 10: " + Math.pow(2, 10));
    }
}
```

#### Al superarla
Doce de lado. Nadia guarda la tablilla y, sin darse cuenta, le presta a Zed su pluma.

#### Imagen
- Una tablilla de bronce con fórmulas grabadas que se encienden: raíz, potencia, máximo.
- Nadia le pasa su pluma a Zed sin mirarlo.

### Micro-misión R01-N04-P4 · Los dados del tahúr

```meta
lugar: La ventanilla de la Aduana
personajes: Zed, Gheco, Nadia
carta: Random | Random r = new Random(semilla); · r.nextInt(6) + 1 → de 1 a 6 · con la misma semilla, siempre lo mismo
recompensa: xp 15, oro 15
```

#### Escena
Un tahúr en la fila le ofrece a Zed un juego de dados. Zed, que de trampas sabe, sospecha: los dados salen siempre igual.
—Es un azar con **semilla** —dice Gheco—. Misma semilla, mismos números. Los dados del tahúr están cargados.

#### Gheco sugiere
`new Random(42)` crea un generador con **semilla**: con la misma semilla da siempre la misma secuencia (sirve para probar). `r.nextInt(6)` da de 0 a 5; sumándole 1, de 1 a 6.

#### Desafío
Tirá tres dados de 1 a 6.

#### Código inicial
```java
import java.util.Random;

public class Dados {
    public static void main(String[] args) {
        Random r = new Random(42);
        int primera = ___;
        int segunda = ___;
        int tercera = ___;
        System.out.println("Tiradas: " + primera + ", " + segunda + " y " + tercera);
    }
}
```

#### Salida esperada
```
Tiradas: 3, 4 y 1
```

#### Solución
```java
import java.util.Random;

public class Dados {
    public static void main(String[] args) {
        Random r = new Random(42);
        int primera = r.nextInt(6) + 1;
        int segunda = r.nextInt(6) + 1;
        int tercera = r.nextInt(6) + 1;
        System.out.println("Tiradas: " + primera + ", " + segunda + " y " + tercera);
    }
}
```

#### Al superarla
Zed adivina cada tirada antes de que caiga. El tahúr se va de la fila, furioso. Nadia anota: «tahúr: denunciado». —Por una vez, una trampa sirvió para algo —le dice a Zed.

#### Imagen
- Tres dados de luz en el aire, cada uno con su número antes de caer.
- Un tahúr furioso que se va; Nadia anota en su libreta.

### Misión R01-N04-M1 · La ficha del viajero

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Pedí el nombre completo, la ciudad de origen y los días que se va a quedar (un
entero). Mostrá una ficha con el nombre en mayúsculas, la ciudad y el costo de la
estadía: 15 denarios por día, con un descuento del 10 % si se queda más de 7 días.
Mostrá el costo con 2 decimales.

#### Criterio de aprobación

- Lee todo con `nextLine()` y convierte los días con `Integer.parseInt`.
- Muestra el costo con `printf` y `%.2f`, con `Locale.setDefault(Locale.US)`.

#### Entrada de ejemplo

```
Bron Tallo
Ciudadela
9
```

#### Salida esperada

```
Nombre completo: Ciudad de origen: Días de estadía: 
Viajero: BRON TALLO
Viene de: Ciudadela
Costo de 9 días: 121.50 denarios
```

#### Solución de referencia

```java
// Mision 1 - La ficha del viajero: Scanner con nextLine y parseInt.
import java.util.Locale;
import java.util.Scanner;

public class FichaViajero {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Scanner teclado = new Scanner(System.in);
        System.out.print("Nombre completo: ");
        String nombre = teclado.nextLine().trim();
        System.out.print("Ciudad de origen: ");
        String ciudad = teclado.nextLine().trim();
        System.out.print("Días de estadía: ");
        int dias = Integer.parseInt(teclado.nextLine().trim());
        System.out.println();

        double costo = dias * 15.0;
        costo = dias > 7 ? costo * 0.9 : costo;

        System.out.println("Viajero: " + nombre.toUpperCase());
        System.out.println("Viene de: " + ciudad);
        System.out.printf("Costo de %d días: %.2f denarios%n", dias, costo);
    }
}
```

#### Pruebas

##### Justo 7 días (sin descuento)
```entrada
kira valdez
Frontera
7
```
```salida
Nombre completo: Ciudad de origen: Días de estadía:
Viajero: KIRA VALDEZ
Viene de: Frontera
Costo de 7 días: 105.00 denarios
```

##### Un día
```entrada
Lía
Puerto
1
```
```salida
Nombre completo: Ciudad de origen: Días de estadía:
Viajero: LÍA
Viene de: Puerto
Costo de 1 días: 15.00 denarios
```

### Misión R01-N04-M2 · El terreno del cuartel

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Pedí el ancho y el largo de un terreno (decimales). Mostrá con 2 decimales el área,
la diagonal (con `Math.sqrt` y `Math.pow`) y cuántas estacas hacen falta para el
perímetro si van cada 2 metros (redondeando **para arriba** con `Math.ceil`).

#### Criterio de aprobación

- Usa `Math.sqrt`, `Math.pow` y `Math.ceil`.
- Muestra los decimales con punto en cualquier compu.

#### Entrada de ejemplo

```
12.5
8
```

#### Salida esperada

```
Ancho: Largo: 
Área: 100.00 m2
Diagonal: 14.84 m
Estacas para el perímetro: 21
```

#### Solución de referencia

```java
// Mision 2 - El terreno del cuartel: Math.sqrt, Math.pow y Math.ceil.
import java.util.Locale;
import java.util.Scanner;

public class Terreno {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Scanner teclado = new Scanner(System.in);
        System.out.print("Ancho: ");
        double ancho = Double.parseDouble(teclado.nextLine().trim());
        System.out.print("Largo: ");
        double largo = Double.parseDouble(teclado.nextLine().trim());
        System.out.println();

        double area = ancho * largo;
        double diagonal = Math.sqrt(Math.pow(ancho, 2) + Math.pow(largo, 2));
        double perimetro = 2 * (ancho + largo);
        int estacas = (int) Math.ceil(perimetro / 2);

        System.out.printf("Área: %.2f m2%n", area);
        System.out.printf("Diagonal: %.2f m%n", diagonal);
        System.out.println("Estacas para el perímetro: " + estacas);
    }
}
```

#### Pruebas

##### Cuadrado
```entrada
2
2
```
```salida
Ancho: Largo:
Área: 4.00 m2
Diagonal: 2.83 m
Estacas para el perímetro: 4
```

##### Terreno chico
```entrada
0.5
0.5
```
```salida
Ancho: Largo:
Área: 0.25 m2
Diagonal: 0.71 m
Estacas para el perímetro: 1
```

### Misión R01-N04-M3 · Los dados del tahúr

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un tahúr de la frontera juega a los dados. Pedí la **semilla** de la partida (un
entero) y creá un `Random` con ella. Tirá tres dados de 6 caras, mostralos, mostrá la
suma, el mayor (con `Math.max` dos veces) y si salió un trío (los tres iguales).

#### Criterio de aprobación

- Crea el `Random` con la semilla leída.
- Cada dado da entre 1 y 6.
- Usa `Math.max` para el mayor.

#### Entrada de ejemplo

```
7
```

#### Salida esperada

```
Semilla: 
Dados: 5 3 4
Suma: 12
Mayor: 5
¿Trío? false
```

#### Solución de referencia

```java
// Mision 3 - Los dados del tahur: Random con semilla y Math.max.
import java.util.Random;
import java.util.Scanner;

public class Dados {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        System.out.print("Semilla: ");
        long semilla = Long.parseLong(teclado.nextLine().trim());
        System.out.println();

        Random random = new Random(semilla);
        int d1 = random.nextInt(6) + 1;
        int d2 = random.nextInt(6) + 1;
        int d3 = random.nextInt(6) + 1;
        int mayor = Math.max(d1, Math.max(d2, d3));
        boolean trio = d1 == d2 && d2 == d3;

        System.out.println("Dados: " + d1 + " " + d2 + " " + d3);
        System.out.println("Suma: " + (d1 + d2 + d3));
        System.out.println("Mayor: " + mayor);
        System.out.println("¿Trío? " + trio);
    }
}
```

#### Pruebas

##### Semilla 1
```entrada
1
```
```salida
Semilla:
Dados: 4 5 2
Suma: 11
Mayor: 5
¿Trío? false
```

##### Semilla 2026
```entrada
2026
```
```salida
Semilla:
Dados: 6 5 2
Suma: 13
Mayor: 6
¿Trío? false
```

### Encargo R01-N04-E1 · La cuota del préstamo

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un banco calcula la cuota mensual de un préstamo con la fórmula del sistema francés:
`cuota = monto * i / (1 - (1 + i)^(-n))`, donde `i` es la tasa mensual (la anual
dividida 12 y dividida 100) y `n` la cantidad de cuotas. Pedí el monto, la tasa anual
y las cuotas, y mostrá la cuota, el total a pagar y los intereses, con 2 decimales.

#### Criterio de aprobación

- Usa `Math.pow` con exponente negativo.
- Los resultados se muestran con 2 decimales y punto.

#### Entrada de ejemplo

```
100000
60
12
```

#### Salida esperada

```
Monto: Tasa anual (%): Cuotas: 
Cuota: 11282.54
Total a pagar: 135390.49
Intereses: 35390.49
```

#### Solución de referencia

```java
// Encargo - La cuota del prestamo: sistema frances con Math.pow.
import java.util.Locale;
import java.util.Scanner;

public class Prestamo {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Scanner teclado = new Scanner(System.in);
        System.out.print("Monto: ");
        double monto = Double.parseDouble(teclado.nextLine().trim());
        System.out.print("Tasa anual (%): ");
        double tasaAnual = Double.parseDouble(teclado.nextLine().trim());
        System.out.print("Cuotas: ");
        int cuotas = Integer.parseInt(teclado.nextLine().trim());
        System.out.println();

        double i = tasaAnual / 12 / 100;
        double cuota = monto * i / (1 - Math.pow(1 + i, -cuotas));
        double total = cuota * cuotas;

        System.out.printf("Cuota: %.2f%n", cuota);
        System.out.printf("Total a pagar: %.2f%n", total);
        System.out.printf("Intereses: %.2f%n", total - monto);
    }
}
```

#### Pruebas

##### Una cuota
```entrada
50000
24
1
```
```salida
Monto: Tasa anual (%): Cuotas:
Cuota: 51000.00
Total a pagar: 51000.00
Intereses: 1000.00
```

##### Tasa baja
```entrada
1000000
12
24
```
```salida
Monto: Tasa anual (%): Cuotas:
Cuota: 47073.47
Total a pagar: 1129763.33
Intereses: 129763.33
```

### Prueba del sello

#### ¿Por qué después de `nextInt()` un `nextLine()` devuelve una línea vacía?

Porque `nextInt()` lee el número pero deja el Enter pendiente, y `nextLine()` lee hasta ese Enter.

#### ¿Qué pasa con `Integer.parseInt("12a")`?

El programa se corta con `NumberFormatException`.

#### ¿Qué rango de valores da `random.nextInt(10)`?

De 0 a 9.

#### ¿Para qué sirve crear un `Random` con semilla?

Para que la secuencia de números sea siempre la misma: sirve para probar y repetir resultados.

#### ¿Qué devuelve `Math.round(2.5)` y de qué tipo es?

`3`, un `long`.

### Soluciones (docente)

Sale de `18-Java/05-Scanner-Math` (unidad 2). La validación en bucle, que el capítulo original tenía acá, pasó al nodo de bucles porque necesita `while`. `Random` con semilla da la misma secuencia en cualquier JVM (el algoritmo está definido en la especificación), así que las salidas esperadas con dados son estables.

## R01-N05 · Decisiones: if y switch

```meta
tipo: tema
padre: R01-N04
precio: 10
criatura: ogre
temas: prog.condicionales
```

### Crónica

Frente a la Aduana hay tres portones: uno para mercaderes, uno para soldados y uno para peregrinos. El guardia mira a cada viajero y lo manda a uno o a otro según lo que traiga. Esa tarde, Nadia le da a Zed el puesto del guardia.

—Un programa que siempre hace lo mismo es una carretilla —dice {mentor}—. Uno que **decide** es un guardia. Enseñale a tus programas a elegir el portón, Zed. Y fijate en qué orden preguntás.

### Objetivos

- Tomar decisiones con `if`, `else if` y `else`.
- Anidar decisiones sin perderse.
- Usar `switch` clásico (con `break`) y `switch` con flechas.
- Usar `switch` como expresión que devuelve un valor.

### Antes de empezar

- Operadores de comparación y lógicos (Operadores y expresiones).
- Leer del teclado (Leer del teclado: Scanner, Math y Random).

### Explicación

#### `if`, `else if`, `else`
```java
if (vida <= 0) {
    System.out.println("Caíste");
} else if (vida < 20) {
    System.out.println("Estás en peligro");
} else {
    System.out.println("Estás bien");
}
```
La condición va entre paréntesis y tiene que ser un `boolean`. Se evalúan **en
orden** y se ejecuta **solo el primer bloque** cuya condición sea verdadera. El
`else` final es opcional: es "en cualquier otro caso".

Las llaves son opcionales si el bloque tiene una sola instrucción, pero **ponelas
siempre**: evitan el error de agregar una segunda línea que parece estar adentro y
no lo está.

#### El orden importa
```java
if (nota >= 4) {            // con nota 9 entra acá...
    System.out.println("Aprobado");
} else if (nota >= 8) {     // ...y este nunca se evalúa
    System.out.println("Distinguido");
}
```
Con rangos, empezá por el más exigente (o el más chico).

#### Decisiones anidadas
Un `if` puede ir dentro de otro. Si se anidan demasiado, conviene combinar las
condiciones con `&&` o separar en métodos (lo vas a ver en el nodo de métodos).
```java
if (tienePase) {
    if (traeArmas) {
        System.out.println("A revisión");
    } else {
        System.out.println("Pase directo");
    }
} else {
    System.out.println("Vuelva con su pase");
}
```

#### `switch` clásico
Cuando una variable se compara contra varios valores fijos, `switch` es más claro
que una cadena de `else if`. Sirve para `int`, `char`, `String` y `enum`:
```java
switch (opcion) {
    case 1:
        System.out.println("Comprar");
        break;
    case 2:
    case 3:                              // dos casos con el mismo código
        System.out.println("Vender o cambiar");
        break;
    default:
        System.out.println("Opción inválida");
}
```
Cada `case` necesita su `break`. Sin él, el programa **sigue** con el código del caso
siguiente (se llama *fall-through*) y casi siempre es un error.

#### `switch` con flechas (Java 14+)
La forma moderna no necesita `break` y no se "cae" al caso siguiente:
```java
switch (portón) {
    case "mercader" -> System.out.println("Portón norte");
    case "soldado", "guardia" -> System.out.println("Portón del cuartel");
    default -> System.out.println("Portón de peregrinos");
}
```

#### `switch` como expresión
Con flechas, `switch` puede **devolver un valor** directamente:
```java
int tasa = switch (tipo) {
    case "mercader" -> 10;
    case "soldado" -> 0;
    default -> 3;
};                                   // ojo con el ; del final
```
Si un caso necesita varias líneas, se abre un bloque y el valor se devuelve con
`yield`:
```java
String trato = switch (dia) {
    case 6, 7 -> "fin de semana";
    default -> {
        String base = "día hábil";
        yield base.toUpperCase();
    }
};
```

> **Si venís de Python.** No hay `elif`: es `else if`. Los bloques van entre
> llaves, y la condición entre paréntesis. El `switch` con flechas se parece al
> `match` de Python 3.10.

### Código de ejemplo

```java
/*
 * Decisiones: el guardia de los tres portones.
 */
import java.util.Scanner;

public class Portones {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        System.out.print("Oficio: ");
        String oficio = teclado.nextLine().trim().toLowerCase();
        System.out.print("Carga (kg): ");
        int carga = Integer.parseInt(teclado.nextLine().trim());
        System.out.print("¿Trae armas? (s/n): ");
        boolean armas = teclado.nextLine().trim().equalsIgnoreCase("s");
        System.out.println();

        // switch con flechas como expresión
        String porton = switch (oficio) {
            case "mercader", "comerciante" -> "norte";
            case "soldado", "guardia" -> "del cuartel";
            default -> "de peregrinos";
        };
        System.out.println("Portón " + porton);

        // if / else if / else con rangos
        int tasa;
        if (carga == 0) {
            tasa = 0;
        } else if (carga <= 50) {
            tasa = 5;
        } else if (carga <= 200) {
            tasa = 12;
        } else {
            tasa = 30;
        }
        System.out.println("Tasa por carga: " + tasa);

        // decisiones anidadas
        if (armas) {
            if (oficio.equals("soldado")) {
                System.out.println("Armas permitidas: es soldado");
            } else {
                System.out.println("Armas a depósito hasta la salida");
            }
        } else {
            System.out.println("Sin armas: pase directo");
        }

        // switch clásico con fall-through a propósito
        int dia = 6;
        switch (dia) {
            case 6:
            case 7:
                System.out.println("Fin de semana: la Aduana cobra el doble");
                break;
            default:
                System.out.println("Día hábil");
        }
    }
}
```

### Entrada de ejemplo

```
Mercader
120
s
```

### Salida esperada

```
Oficio: Carga (kg): ¿Trae armas? (s/n): 
Portón norte
Tasa por carga: 12
Armas a depósito hasta la salida
Fin de semana: la Aduana cobra el doble
```

### ¿Para qué sirve?

Todas las reglas de un negocio son decisiones: el precio según la categoría del cliente, si una compra lleva envío gratis, qué menú mostrar según el rol del usuario, qué hacer con cada opción de un menú. Un sistema de facturación, un juego o una app de turnos es, en buena parte, un gran conjunto de `if` y `switch` bien ordenados.

### Errores habituales

**Ogro: el `break` que falta.** En un `switch` clásico, sin `break` se ejecuta
también el caso siguiente. Con flechas no pasa.

**Ogro: el orden de los rangos.** Si el primer `if` es el más amplio (`nota >= 4`),
los siguientes nunca se evalúan.

**Ogro: comparar textos con `==` en el `if`.** `if (oficio == "soldado")` puede dar
`false`. Va `oficio.equals("soldado")`. (El `switch` con `String` sí compara bien:
usa `equals` por dentro.)

**Slime: el punto y coma después del `if`.** `if (vida < 20);` termina el `if` ahí
mismo, y el bloque de abajo se ejecuta **siempre**.

**Esqueleto: variable que puede quedar sin valor.** Si declarás `int tasa;` y la
asignás solo en algunos `if` sin un `else`, el compilador dice `variable tasa might
not have been initialized`.

### Micro-misión R01-N05-P1 · Los tres portones

```meta
lugar: Los tres portones de la Aduana
personajes: Zed, Gheco, Nadia
carta: if / else if / else | se revisa en orden · entra al PRIMERO que se cumple · else: si ninguno
recompensa: xp 10, oro 10
```

#### Escena
Frente a la Aduana hay tres portones: mercaderes, soldados y peregrinos. Nadia le da a Zed el puesto del guardia: —Mandá a cada uno al suyo.

#### Gheco sugiere
`if (condición) { … } else if (otra) { … } else { … }` revisa **en orden** y entra solo en el primero que se cumple. El `else` es para todos los demás.

#### Desafío
Completá la condición del portón de los soldados (el que llega ahora es un soldado).

#### Código inicial
```java
public class Portones {
    public static void main(String[] args) {
        String v = "soldado";
        if (v.equals("mercader")) {
            System.out.println(v + ": portón del oro");
        } else if (___) {
            System.out.println(v + ": portón de hierro");
        } else {
            System.out.println(v + ": portón de piedra");
        }
    }
}
```

#### Salida esperada
```
soldado: portón de hierro
```

#### Solución
```java
public class Portones {
    public static void main(String[] args) {
        String v = "soldado";
        if (v.equals("mercader")) {
            System.out.println(v + ": portón del oro");
        } else if (v.equals("soldado")) {
            System.out.println(v + ": portón de hierro");
        } else {
            System.out.println(v + ": portón de piedra");
        }
    }
}
```

#### Al superarla
Cada viajero a su portón, sin una equivocación. —Un programa que decide es un guardia —dice Gheco—. Y vos sos un buen guardia, para ser ladrón.

#### Imagen
- Tres portones de la Aduana: uno dorado, uno de hierro y uno de piedra, cada uno con su fila.
- Zed en el puesto del guardia, señalando; Nadia lo observa con la libreta.

### Micro-misión R01-N05-P2 · El orden importa

```meta
lugar: Los tres portones de la Aduana
personajes: Zed, Gheco, Nadia
criatura: ogro
carta: El orden de los if | lo más exigente primero · si la primera condición es amplia, tapa a las demás
recompensa: xp 15, oro 15
```

#### Escena
El peaje depende de la carga: más de 100 kg paga 20, más de 50 paga 10, el resto 5. El guardia anterior lo escribió… y todos pagan 10. Un **ogro**.

#### Gheco sugiere
Los `else if` se revisan en orden: si la primera condición es la más **amplia** (`> 50`), atrapa también a los de 100 y nunca se llega a la otra. Lo más exigente va **primero**.

#### Desafío
Llega un carro de 120 kg y paga 10. Reordená las condiciones para que pague 20.

#### Código inicial
```java
public class Peso {
    public static void main(String[] args) {
        int kg = 120;
        int peaje;
        if (kg > 50) {
            peaje = 10;
        } else if (kg > 100) {
            peaje = 20;
        } else {
            peaje = 5;
        }
        System.out.println(kg + " kg: " + peaje);
    }
}
```

#### Salida esperada
```
120 kg: 20
```

#### Solución
```java
public class Peso {
    public static void main(String[] args) {
        int kg = 120;
        int peaje;
        if (kg > 100) {
            peaje = 20;
        } else if (kg > 50) {
            peaje = 10;
        } else {
            peaje = 5;
        }
        System.out.println(kg + " kg: " + peaje);
    }
}
```

#### Al superarla
El carro de 120 kg paga lo justo. Nadia anota la corrección y, por primera vez, le pone a Zed una tilde de aprobado.

#### Imagen
- Tres carros de distintos tamaños en una balanza gigante, cada uno con su peaje.
- La libreta de Nadia con una tilde verde junto al nombre de Zed.

### Micro-misión R01-N05-P3 · El menú de la posada

```meta
lugar: La posada junto a la Aduana
personajes: Zed, Gheco, Nadia
carta: switch | switch (op) { case 1 -> …; case 2 -> …; default -> …; } · compara un valor contra varios casos
recompensa: xp 10, oro 10
```

#### Escena
Al terminar el turno, Nadia lleva a Zed a la posada. El menú se pide por número, y el posadero se confunde siempre. —Escribile el menú —dice Nadia—, que yo invito.

#### Gheco sugiere
`switch` compara un valor contra varios casos. Con flechas (`case 1 -> …;`) no hace falta `break`. `default` atrapa todo lo que no coincide.

#### Desafío
Nadia pide el 2. Completá el caso 2: «Guiso del Imperio».

#### Código inicial
```java
public class Posada {
    public static void main(String[] args) {
        int op = 2;
        switch (op) {
            case 1 -> System.out.println("1: Pan y café");
            ___
            default -> System.out.println(op + ": eso no está en el menú");
        }
    }
}
```

#### Salida esperada
```
2: Guiso del Imperio
```

#### Solución
```java
public class Posada {
    public static void main(String[] args) {
        int op = 2;
        switch (op) {
            case 1 -> System.out.println("1: Pan y café");
            case 2 -> System.out.println("2: Guiso del Imperio");
            default -> System.out.println(op + ": eso no está en el menú");
        }
    }
}
```

#### Al superarla
Llega el guiso. Zed pide el siete «por las dudas» y el posadero se ríe: eso no está en el menú. Nadia paga, como prometió.

#### Imagen
- Una posada cálida con un menú de pizarra numerado.
- Zed y Nadia en una mesa; él señala el número 7 y el posadero se ríe.

### Micro-misión R01-N05-P4 · El switch que devuelve

```meta
lugar: La posada junto a la Aduana
personajes: Zed, Gheco, Nadia
carta: switch como expresión | String x = switch (v) { case "a" -> "…"; default -> "…"; }; · devuelve un valor
recompensa: xp 15, oro 15
```

#### Escena
En la posada, Nadia le cuenta a Zed cómo se clasifica a los viajeros. Él escribe la regla en una servilleta, más corta que la del reglamento.
—Así no está en el reglamento —dice ella. —Pero hace lo mismo —responde él.

#### Gheco sugiere
Un `switch` también puede **devolver** un valor: `String portón = switch (oficio) { case "mercader" -> "oro"; … default -> "piedra"; };`. Fijate el `;` del final.

#### Desafío
Escribí el `switch` que devuelve el portón de cada oficio.

#### Código inicial
```java
public class Servilleta {
    public static void main(String[] args) {
        String oficio = "mercader";
        String porton = ___;
        System.out.println(oficio + " -> " + porton);
    }
}
```

#### Salida esperada
```
mercader -> oro
```

#### Solución
```java
public class Servilleta {
    public static void main(String[] args) {
        String oficio = "mercader";
        String porton = switch (oficio) {
            case "mercader" -> "oro";
            case "soldado" -> "hierro";
            default -> "piedra";
        };
        System.out.println(oficio + " -> " + porton);
    }
}
```

#### Al superarla
Nadia lee la servilleta dos veces y se la guarda en el bolsillo. —Mañana se la muestro al Escriba Jefe.
Afuera, la Aduana cierra. Hay que contar todo lo que entró, carro por carro. Mañana, Zed va a aprender a **repetir**.

#### Imagen
- Una servilleta con un switch escrito a mano, sobre una mesa de la posada.
- Nadia guardándose la servilleta en el bolsillo de la chaqueta; Zed sonríe con la taza en la mano.
- Por la ventana, la Aduana cerrando y faroles encendiéndose.

### Misión R01-N05-M1 · La balanza del veredicto

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La Academia del Imperio pone notas de 1 a 10. Pedí una nota y mostrá el veredicto:
de 1 a 3 "Desaprobado", de 4 a 6 "Aprobado", de 7 a 9 "Muy bueno", 10 "Sobresaliente",
y cualquier otro número "Nota inválida". Usá `if` / `else if` / `else`.

#### Criterio de aprobación

- Los rangos están bien ordenados y no se superponen.
- Maneja las notas fuera de rango.

#### Entrada de ejemplo

```
7
```

#### Salida esperada

```
Nota: 
Muy bueno
```

#### Solución de referencia

```java
// Mision 1 - La balanza del veredicto: if / else if / else con rangos.
import java.util.Scanner;

public class Veredicto {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        System.out.print("Nota: ");
        int nota = Integer.parseInt(teclado.nextLine().trim());
        System.out.println();

        if (nota < 1 || nota > 10) {
            System.out.println("Nota inválida");
        } else if (nota <= 3) {
            System.out.println("Desaprobado");
        } else if (nota <= 6) {
            System.out.println("Aprobado");
        } else if (nota <= 9) {
            System.out.println("Muy bueno");
        } else {
            System.out.println("Sobresaliente");
        }
    }
}
```

#### Pruebas

##### Bordes
```entrada
1
```
```salida
Nota:
Desaprobado
```

##### Sobresaliente
```entrada
10
```
```salida
Nota:
Sobresaliente
```

##### Fuera de rango
```entrada
0
```
```salida
Nota:
Nota inválida
```

##### Aprobado justo
```entrada
4
```
```salida
Nota:
Aprobado
```

### Misión R01-N05-M2 · El menú de la posada

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Mostrá el menú de la posada (1 Guiso, 2 Pan, 3 Café, 4 Agua) y pedí una opción. Con
un **`switch` como expresión** obtené el precio (guiso 1200, pan 300, café 450,
agua 0) y el nombre del plato; para cualquier otra opción el precio es -1. Si el
precio es -1, avisá que la opción no existe; si no, mostrá qué se pidió y cuánto sale.

#### Criterio de aprobación

- Usa `switch` con flechas como expresión (al menos uno).
- Maneja la opción inexistente.

#### Entrada de ejemplo

```
3
```

#### Salida esperada

```
1 Guiso | 2 Pan | 3 Café | 4 Agua
Opción: 
Pediste café: 450 denarios
```

#### Solución de referencia

```java
// Mision 2 - El menu de la posada: switch con flechas como expresion.
import java.util.Scanner;

public class MenuPosada {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        System.out.println("1 Guiso | 2 Pan | 3 Café | 4 Agua");
        System.out.print("Opción: ");
        int opcion = Integer.parseInt(teclado.nextLine().trim());
        System.out.println();

        int precio = switch (opcion) {
            case 1 -> 1200;
            case 2 -> 300;
            case 3 -> 450;
            case 4 -> 0;
            default -> -1;
        };
        String plato = switch (opcion) {
            case 1 -> "guiso";
            case 2 -> "pan";
            case 3 -> "café";
            case 4 -> "agua";
            default -> "";
        };

        if (precio == -1) {
            System.out.println("Esa opción no existe");
        } else {
            System.out.println("Pediste " + plato + ": " + precio + " denarios");
        }
    }
}
```

#### Pruebas

##### Agua
```entrada
4
```
```salida
1 Guiso | 2 Pan | 3 Café | 4 Agua
Opción:
Pediste agua: 0 denarios
```

##### Opción inexistente
```entrada
9
```
```salida
1 Guiso | 2 Pan | 3 Café | 4 Agua
Opción:
Esa opción no existe
```

##### Guiso
```entrada
1
```
```salida
1 Guiso | 2 Pan | 3 Café | 4 Agua
Opción:
Pediste guiso: 1200 denarios
```

### Misión R01-N05-M3 · Piedra, papel o tijera

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Pedí la jugada de Kira (`piedra`, `papel` o `tijera`) y la semilla del guardia. El
guardia elige con `new Random(semilla).nextInt(3)`: 0 piedra, 1 papel, 2 tijera.
Mostrá las dos jugadas y el resultado: empate, gana Kira o gana el guardia. Si la
jugada de Kira no es válida, avisá.

#### Criterio de aprobación

- La jugada del guardia sale de un `switch`.
- Compara textos con `equals`.
- Cubre los empates y los seis casos con ganador.

#### Entrada de ejemplo

```
papel
5
```

#### Salida esperada

```
Tu jugada: Semilla del guardia: 
Kira: papel | Guardia: tijera
Gana el guardia
```

#### Solución de referencia

```java
// Mision 3 - Piedra, papel o tijera: switch, equals y condiciones combinadas.
import java.util.Random;
import java.util.Scanner;

public class PiedraPapelTijera {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        System.out.print("Tu jugada: ");
        String kira = teclado.nextLine().trim().toLowerCase();
        System.out.print("Semilla del guardia: ");
        long semilla = Long.parseLong(teclado.nextLine().trim());
        System.out.println();

        if (!kira.equals("piedra") && !kira.equals("papel") && !kira.equals("tijera")) {
            System.out.println("Jugada inválida");
            return;
        }
        String guardia = switch (new Random(semilla).nextInt(3)) {
            case 0 -> "piedra";
            case 1 -> "papel";
            default -> "tijera";
        };
        System.out.println("Kira: " + kira + " | Guardia: " + guardia);

        if (kira.equals(guardia)) {
            System.out.println("Empate");
        } else if ((kira.equals("piedra") && guardia.equals("tijera"))
                || (kira.equals("papel") && guardia.equals("piedra"))
                || (kira.equals("tijera") && guardia.equals("papel"))) {
            System.out.println("Gana Kira");
        } else {
            System.out.println("Gana el guardia");
        }
    }
}
```

#### Pruebas

##### Piedra
```entrada
piedra
1
```
```salida
Tu jugada: Semilla del guardia:
Kira: piedra | Guardia: piedra
Empate
```

##### Tijera
```entrada
tijera
2026
```
```salida
Tu jugada: Semilla del guardia:
Kira: tijera | Guardia: tijera
Empate
```

##### Jugada inválida
```entrada
lagarto
3
```
```salida
Tu jugada: Semilla del guardia:
Jugada inválida
```

### Encargo R01-N05-E1 · El envío de la tienda

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una tienda online cobra el envío según la zona (`CABA`, `GBA` o `INTERIOR`) y el
monto de la compra. Pedí las dos cosas y calculá el envío: CABA 2500, GBA 4000,
INTERIOR 7000 (con un `switch`); si la compra supera los 50 000 el envío es gratis en
CABA y GBA, y la mitad en el interior. Mostrá el envío y el total.

#### Criterio de aprobación

- Usa `switch` para la tarifa base y `if` para el descuento.
- Acepta la zona en mayúsculas o minúsculas.

#### Entrada de ejemplo

```
interior
62000
```

#### Salida esperada

```
Zona (CABA, GBA o INTERIOR): Monto de la compra: 
Envío: 3500
Total: 65500
```

#### Solución de referencia

```java
// Encargo - El envio de la tienda: switch para la tarifa, if para el descuento.
import java.util.Scanner;

public class Envio {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        System.out.print("Zona (CABA, GBA o INTERIOR): ");
        String zona = teclado.nextLine().trim().toUpperCase();
        System.out.print("Monto de la compra: ");
        int monto = Integer.parseInt(teclado.nextLine().trim());
        System.out.println();

        int envio = switch (zona) {
            case "CABA" -> 2500;
            case "GBA" -> 4000;
            case "INTERIOR" -> 7000;
            default -> -1;
        };
        if (envio == -1) {
            System.out.println("Zona desconocida");
            return;
        }
        if (monto > 50_000) {
            if (zona.equals("INTERIOR")) {
                envio = envio / 2;
            } else {
                envio = 0;
            }
        }
        System.out.println("Envío: " + envio);
        System.out.println("Total: " + (monto + envio));
    }
}
```

#### Pruebas

##### CABA con envío gratis
```entrada
CABA
50001
```
```salida
Zona (CABA, GBA o INTERIOR): Monto de la compra:
Envío: 0
Total: 50001
```

##### GBA justo en el límite
```entrada
gba
50000
```
```salida
Zona (CABA, GBA o INTERIOR): Monto de la compra:
Envío: 4000
Total: 54000
```

##### Interior sin descuento
```entrada
INTERIOR
100
```
```salida
Zona (CABA, GBA o INTERIOR): Monto de la compra:
Envío: 7000
Total: 7100
```

### Prueba del sello

#### Si la nota es 9 y el primer `if` pregunta `nota >= 4`, ¿qué pasa con un `else if (nota >= 8)` que viene después?

Nunca se evalúa: el primer `if` ya fue verdadero y se ejecuta solo ese bloque.

#### ¿Qué pasa si te olvidás el `break` en un `case` del `switch` clásico?

Se ejecuta también el código del caso siguiente (fall-through).

#### ¿Qué ventaja tiene el `switch` con flechas?

No necesita `break`, no se cae al caso siguiente y puede devolver un valor como expresión.

#### ¿Para qué sirve `yield`?

Para devolver el valor de un caso de un `switch` expresión que tiene un bloque de varias líneas.

#### ¿Qué hace `if (x > 3);` con el punto y coma?

Termina el `if` sin hacer nada; el bloque de abajo se ejecuta siempre.

### Soluciones (docente)

Sale de `18-Java/06-Control` (unidad 2), la parte de decisiones. El `switch` con flechas y como expresión es de Java 14+ (el curso pide Java 17).

## R01-N06 · Bucles: while, do y for

```meta
tipo: tema
padre: R01-N05
precio: 10
criatura: ogre
temas: prog.bucles, err.validacion
```

### Crónica

Al atardecer, la Aduana cierra y hay que contar todo lo que entró: carro por carro, bolsa por bolsa. El contador repite los mismos gestos cien veces sin equivocarse. Zed, que nunca contó nada que no fuera ajeno, se ofrece a ayudar.

—Las computadoras no se cansan de repetir —dice {mentor}—. Esa es su magia. Pero ojo, Zed: un bucle que no sabe cuándo parar es una maldición que no termina nunca. Y esta noche, la Aduana lo va a aprender por las malas.

### Objetivos

- Repetir con `while`, `do`/`while` y `for`.
- Usar contadores y acumuladores.
- Cortar un bucle con `break` y saltear una vuelta con `continue`.
- Validar la entrada volviendo a preguntar hasta que sea correcta.

### Antes de empezar

- Decisiones (Decisiones: if y switch).

### Explicación

#### `while`: mientras se cumpla
```java
int oro = 100;
while (oro >= 30) {          // se evalúa ANTES de cada vuelta
    oro -= 30;
    System.out.println("Pagaste 30, quedan " + oro);
}
```
Si la condición es falsa de entrada, el bloque no se ejecuta ni una vez. Algo
dentro del bucle tiene que acercarlo a terminar: si no, es un **bucle infinito**
(se corta con `Ctrl+C`).

#### `do`/`while`: al menos una vez
La condición se evalúa **después** de cada vuelta, así que el bloque se ejecuta por
lo menos una vez. Es ideal para menús y para pedir un dato:
```java
int opcion;
do {
    System.out.print("Opción (1-3): ");
    opcion = Integer.parseInt(teclado.nextLine().trim());
} while (opcion < 1 || opcion > 3);
```

#### `for`: una cantidad conocida de vueltas
```java
for (int i = 1; i <= 5; i++) {
    System.out.println("Vuelta " + i);
}
```
Tiene tres partes separadas por `;`: **inicio** (una vez), **condición** (antes de
cada vuelta) y **paso** (después de cada vuelta). La variable `i` existe solo dentro
del `for`. Se puede contar para atrás (`i--`) o de a varios (`i += 5`).

#### Contadores y acumuladores
```java
int cantidad = 0;       // contador: suma 1 cada vez que pasa algo
int total = 0;          // acumulador: suma valores
for (int i = 1; i <= 10; i++) {
    if (i % 3 == 0) {
        cantidad++;
        total += i;
    }
}
```
Se inicializan **antes** del bucle; si los declarás adentro, vuelven a cero en cada
vuelta.

#### `break` y `continue`
- `break` corta el bucle entero.
- `continue` saltea el resto de **esta** vuelta y pasa a la siguiente.
```java
for (int i = 1; i <= 10; i++) {
    if (i % 2 == 0) {
        continue;       // saltea los pares
    }
    if (i > 7) {
        break;          // termina todo
    }
    System.out.print(i + " ");     // 1 3 5 7
}
```

#### Validar la entrada en un bucle
Con `hasNextLine` y una conversión que puede fallar, el patrón para pedir un número
válido es:
```java
int edad = -1;
while (edad < 0) {
    System.out.print("Edad: ");
    String linea = teclado.nextLine().trim();
    if (linea.matches("\\d+")) {          // solo dígitos
        edad = Integer.parseInt(linea);
    } else {
        System.out.println("Eso no es un número. Probá de nuevo.");
    }
}
```
`linea.matches("\\d+")` dice si el texto son solo dígitos (es una *expresión
regular*: `\d` es "un dígito" y `+` es "uno o más"). En el nodo de excepciones vas a
ver otra forma, con `try`/`catch`.

#### Bucles anidados
Un bucle dentro de otro recorre combinaciones: filas y columnas, cada carro con cada
bolsa.
```java
for (int fila = 1; fila <= 3; fila++) {
    for (int col = 1; col <= fila; col++) {
        System.out.print("*");
    }
    System.out.println();
}
```

> **Si venís de Python.** No hay `for x in range(n)`: el `for` de Java tiene las
> tres partes. Para recorrer colecciones hay un *for-each* (`for (String s : lista)`)
> que vas a ver con los arrays.

### Código de ejemplo

```java
/*
 * Bucles: el recuento al cerrar la Aduana.
 */
import java.util.Scanner;

public class Recuento {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);

        // Validar: pedir la cantidad de carros hasta que sea un número entre 1 y 10
        int carros = 0;
        while (carros < 1 || carros > 10) {
            System.out.print("¿Cuántos carros entraron? (1-10): ");
            String linea = teclado.nextLine().trim();
            if (linea.matches("\\d+")) {
                carros = Integer.parseInt(linea);
                if (carros < 1 || carros > 10) {
                    System.out.println("Tiene que ser entre 1 y 10.");
                }
            } else {
                System.out.println("Eso no es un número.");
            }
        }

        // for con acumulador y contador
        int totalBolsas = 0;
        int carrosPesados = 0;
        for (int i = 1; i <= carros; i++) {
            System.out.print("Bolsas del carro " + i + ": ");
            int bolsas = Integer.parseInt(teclado.nextLine().trim());
            totalBolsas += bolsas;
            if (bolsas > 20) {
                carrosPesados++;
            }
        }
        System.out.println();
        System.out.println("Total de bolsas: " + totalBolsas);
        System.out.println("Carros pesados: " + carrosPesados);

        // while: pagar la tasa en cuotas de 30
        int deuda = totalBolsas * 2;
        int cuotas = 0;
        while (deuda > 0) {
            deuda -= 30;
            cuotas++;
        }
        System.out.println("Cuotas de 30 para pagar la tasa: " + cuotas);

        // break y continue
        System.out.print("Carros revisados (salteando los pares, hasta el 7): ");
        for (int i = 1; i <= 10; i++) {
            if (i % 2 == 0) {
                continue;
            }
            if (i > 7) {
                break;
            }
            System.out.print(i + " ");
        }
        System.out.println();

        // anidados: la pila de bolsas
        for (int fila = 1; fila <= 4; fila++) {
            System.out.println(" ".repeat(4 - fila) + "#".repeat(fila * 2 - 1));
        }
    }
}
```

### Entrada de ejemplo

```
muchos
15
3
12
25
8
```

### Salida esperada

```
¿Cuántos carros entraron? (1-10): Eso no es un número.
¿Cuántos carros entraron? (1-10): Tiene que ser entre 1 y 10.
¿Cuántos carros entraron? (1-10): Bolsas del carro 1: Bolsas del carro 2: Bolsas del carro 3: 
Total de bolsas: 45
Carros pesados: 1
Cuotas de 30 para pagar la tasa: 3
Carros revisados (salteando los pares, hasta el 7): 1 3 5 7 
   #
  ###
 #####
#######
```

### ¿Para qué sirve?

Todo lo que se hace "para cada cosa" es un bucle: sumar las ventas del día, mandar un mail a cada cliente, recorrer las líneas de un archivo, repetir el turno de un juego hasta que alguien gane. Y el bucle de validación está en cualquier formulario serio: no se sigue hasta que el dato sea correcto.

### Errores habituales

**Ogro: el bucle infinito.** Si nada dentro del bucle cambia la condición, no
termina nunca. En la terminal se corta con `Ctrl+C`.

**Ogro: una vuelta de más o de menos.** `for (int i = 0; i <= 5; i++)` da **6**
vueltas (0 a 5). Revisá si el límite va con `<` o con `<=`.

**Ogro: el acumulador adentro del bucle.** `int total = 0;` dentro del `for` vuelve a
cero en cada vuelta y al final vale solo el último valor.

**Esqueleto: usar la variable del `for` afuera.**
```
Recuento.java:20: error: cannot find symbol
  symbol:   variable i
```
La variable declarada en el `for` existe solo adentro.

**Slime: el `;` después del `while`.** `while (x > 0);` es un bucle vacío que no
termina nunca (la condición no cambia).

### Micro-misión R01-N06-P1 · La Aduana trabada

```meta
lugar: El cierre de la Aduana
personajes: Zed, Gheco, Nadia
criatura: ogro
carta: while | while (condición) { … } · repite mientras se cumpla · adentro, algo tiene que cambiar o no termina nunca
recompensa: xp 10, oro 10
```

#### Escena
Al cerrar la Aduana hay que contar los carros, uno por uno. Zed escribe su primer bucle, lo ejecuta… y el contador no para: «Carro 1, Carro 1, Carro 1». La Aduana queda trabada toda la noche y un **ogro** se sienta en la puerta a mirar.
—Tu bucle nunca cambia nada —dice Gheco—. Si `carro` vale siempre 1, la condición se cumple para siempre.

#### Gheco sugiere
`while (carro <= 4) { … }` repite mientras la condición se cumpla. Adentro, algo tiene que acercarla a ser falsa: `carro++;` le suma 1 a `carro` en cada vuelta.

#### Desafío
Completá la línea que falta para que el contador avance y el bucle termine.

#### Código inicial
```java
public class Cierre {
    public static void main(String[] args) {
        int carro = 1;
        while (carro <= 4) {
            System.out.println("Carro " + carro + ": contado");
            ___;
        }
        System.out.println("Aduana cerrada");
    }
}
```

#### Salida esperada
```
Carro 1: contado
Carro 2: contado
Carro 3: contado
Carro 4: contado
Aduana cerrada
```

#### Solución
```java
public class Cierre {
    public static void main(String[] args) {
        int carro = 1;
        while (carro <= 4) {
            System.out.println("Carro " + carro + ": contado");
            carro++;
        }
        System.out.println("Aduana cerrada");
    }
}
```

#### Al superarla
Cuatro carros y la Aduana se cierra. El ogro bosteza y se va. Nadia, que pasó la noche despierta por el bucle de Zed, no dice nada: le alcanza con mirarlo.

#### Imagen
- El portón de la Aduana de noche, trabado, con un contador de bronce que gira sin parar.
- Un ogro sentado en la puerta, aburrido; Zed (pelo blanco plateado, visor rojo) agarrándose la cabeza.
- Nadia (uniforme azul, rodete) con ojeras y los brazos cruzados.

### Micro-misión R01-N06-P2 · La recaudación de la semana

```meta
lugar: La tesorería de la Aduana
personajes: Zed, Gheco, Nadia
carta: for y acumulador | for (int i = 1; i <= 5; i++) { total += …; } · el acumulador se declara ANTES del bucle
recompensa: xp 10, oro 10
```

#### Escena
El tesorero quiere saber cuánto entró en la semana. Cada día se cobró diez denarios más que el anterior: 10, 20, 30… Zed se ofrece a sumarlo «de memoria» y Nadia le saca la pluma de la mano.
—Cuando sabés cuántas vueltas son, usá `for` —dice Gheco.

#### Gheco sugiere
`for (int dia = 1; dia <= 5; dia++)` da exactamente 5 vueltas. Para sumar, un **acumulador**: `int total = 0;` antes del bucle y `total += …;` adentro.

#### Desafío
Sumale al total lo que se cobró cada día (`dia * 10`).

#### Código inicial
```java
public class Recaudacion {
    public static void main(String[] args) {
        int total = 0;
        for (int dia = 1; dia <= 5; dia++) {
            total ___ dia * 10;
            System.out.println("Día " + dia + ": " + total);
        }
        System.out.println("Semana: " + total + " denarios");
    }
}
```

#### Salida esperada
```
Día 1: 10
Día 2: 30
Día 3: 60
Día 4: 100
Día 5: 150
Semana: 150 denarios
```

#### Solución
```java
public class Recaudacion {
    public static void main(String[] args) {
        int total = 0;
        for (int dia = 1; dia <= 5; dia++) {
            total += dia * 10;
            System.out.println("Día " + dia + ": " + total);
        }
        System.out.println("Semana: " + total + " denarios");
    }
}
```

#### Al superarla
Ciento cincuenta denarios, día por día. El tesorero lo anota sin discutir. —Si lo hubieras sumado de memoria —dice Nadia—, hoy faltarían diez. —¿Y vos cómo sabés? —Porque te conozco.

#### Imagen
- La tesorería de la Aduana: un mostrador con pilas de monedas que crecen día por día.
- Nadia sacándole la pluma de la mano a Zed; Gheco en el mostrador.

### Micro-misión R01-N06-P3 · El peso que no miente

```meta
lugar: La balanza de la Aduana
personajes: Zed, Gheco, Nadia
carta: do / while | do { … } while (condición); · da al menos una vuelta · sirve para volver a preguntar hasta que el dato sea válido
recompensa: xp 15, oro 15
```

#### Escena
Un mercader apurado declara pesos imposibles para no pagar: −3 kg, 0 kg… Nadia suspira. —Preguntale otra vez. Y otra. Hasta que diga algo que tenga sentido.

#### Gheco sugiere
`do { … } while (condición);` ejecuta el bloque **una vez** y después repite **mientras** la condición se cumpla. Para validar: repetí mientras el peso sea **inválido** (`peso <= 0`). Fijate el `;` del final.

#### Desafío
Completá la condición: se vuelve a preguntar mientras el peso no sea mayor que cero.

#### Código inicial
```java
import java.util.Scanner;

public class Balanza {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int peso;
        do {
            System.out.println("Peso del carro:");
            peso = sc.nextInt();
        } while (___);
        System.out.println("Aceptado: " + peso + " kg");
    }
}
```

#### Entrada
```
-3
0
25
```

#### Salida esperada
```
Peso del carro:
Peso del carro:
Peso del carro:
Aceptado: 25 kg
```

#### Solución
```java
import java.util.Scanner;

public class Balanza {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int peso;
        do {
            System.out.println("Peso del carro:");
            peso = sc.nextInt();
        } while (peso <= 0);
        System.out.println("Aceptado: " + peso + " kg");
    }
}
```

#### Al superarla
A la tercera, el mercader se rinde y declara 25 kg. —Con vos no se puede —le dice a Zed. Zed sonríe: hace una semana, el que mentía en la balanza era él.

#### Imagen
- Una balanza de bronce gigante con un carro encima y la aguja en 25.
- Un mercader de bigote, resignado; Zed sonriendo de costado y Nadia anotando.

### Micro-misión R01-N06-P4 · Los sellos falsos

```meta
lugar: La fila de los carros
personajes: Zed, Gheco, Nadia
carta: break y continue | continue: saltea el resto de ESTA vuelta · break: corta el bucle entero
recompensa: xp 15, oro 15
```

#### Escena
Último control del día. El carro 4 trae un sello falso: va al costado y se sigue con el próximo. Y cuando suena la campana del cierre, en el carro 7, no se revisa nada más.
—Hay dos formas de salir de una vuelta —dice Gheco—: saltearla o cortar todo.

#### Gheco sugiere
Adentro de un bucle, `continue;` saltea lo que queda de **esta** vuelta y pasa a la siguiente; `break;` termina el bucle **entero**.

#### Desafío
Completá las dos líneas: el carro 4 se saltea y en el 7 se corta todo.

#### Código inicial
```java
public class Control {
    public static void main(String[] args) {
        for (int carro = 1; carro <= 10; carro++) {
            if (carro == 4) {
                System.out.println("Carro 4: sello falso, al costado");
                ___;
            }
            if (carro == 7) {
                System.out.println("Carro 7: ¡campana del cierre!");
                ___;
            }
            System.out.println("Carro " + carro + ": pasa");
        }
    }
}
```

#### Salida esperada
```
Carro 1: pasa
Carro 2: pasa
Carro 3: pasa
Carro 4: sello falso, al costado
Carro 5: pasa
Carro 6: pasa
Carro 7: ¡campana del cierre!
```

#### Solución
```java
public class Control {
    public static void main(String[] args) {
        for (int carro = 1; carro <= 10; carro++) {
            if (carro == 4) {
                System.out.println("Carro 4: sello falso, al costado");
                continue;
            }
            if (carro == 7) {
                System.out.println("Carro 7: ¡campana del cierre!");
                break;
            }
            System.out.println("Carro " + carro + ": pasa");
        }
    }
}
```

#### Al superarla
El carro 4 queda al costado y la campana corta la fila justo a tiempo. Nadia cierra el portón con la llave grande.
—Mañana te toca el depósito —le dice a Zed—. Estantes numerados del cero al nueve. Y un mapa de la frontera, todo en cuadritos.

#### Imagen
- Una fila de carros: el cuarto apartado con un sello falso que se despega; una campana de bronce sonando sobre el séptimo.
- Nadia cerrando el portón con una llave enorme; Zed mirando hacia el depósito.

### Misión R01-N06-M1 · La tabla del tesorero

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Pedí un número del 1 al 10 (validá con un bucle: si no es un número o está fuera de
rango, volvé a preguntar) y mostrá su tabla de multiplicar del 1 al 10 con `printf`,
alineada. Al final mostrá la suma de todos los resultados.

#### Criterio de aprobación

- Vuelve a preguntar hasta que el dato sea válido.
- Usa un `for` para la tabla y un acumulador para la suma.

#### Entrada de ejemplo

```
doce
12
7
```

#### Salida esperada

```
Número (1-10): Tiene que ser un número del 1 al 10.
Número (1-10): Tiene que ser un número del 1 al 10.
Número (1-10): 
 7 x  1 =   7
 7 x  2 =  14
 7 x  3 =  21
 7 x  4 =  28
 7 x  5 =  35
 7 x  6 =  42
 7 x  7 =  49
 7 x  8 =  56
 7 x  9 =  63
 7 x 10 =  70
Suma de la tabla: 385
```

#### Solución de referencia

```java
// Mision 1 - La tabla del tesorero: validacion en bucle, for y acumulador.
import java.util.Scanner;

public class Tabla {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        int n = 0;
        while (n < 1 || n > 10) {
            System.out.print("Número (1-10): ");
            String linea = teclado.nextLine().trim();
            if (linea.matches("\\d+")) {
                n = Integer.parseInt(linea);
            }
            if (n < 1 || n > 10) {
                System.out.println("Tiene que ser un número del 1 al 10.");
            }
        }
        System.out.println();
        int suma = 0;
        for (int i = 1; i <= 10; i++) {
            System.out.printf("%2d x %2d = %3d%n", n, i, n * i);
            suma += n * i;
        }
        System.out.println("Suma de la tabla: " + suma);
    }
}
```

#### Pruebas

##### Bordes válidos
```entrada
1
```
```salida
Número (1-10):
 1 x  1 =   1
 1 x  2 =   2
 1 x  3 =   3
 1 x  4 =   4
 1 x  5 =   5
 1 x  6 =   6
 1 x  7 =   7
 1 x  8 =   8
 1 x  9 =   9
 1 x 10 =  10
Suma de la tabla: 55
```

##### Diez
```entrada
10
```
```salida
Número (1-10):
10 x  1 =  10
10 x  2 =  20
10 x  3 =  30
10 x  4 =  40
10 x  5 =  50
10 x  6 =  60
10 x  7 =  70
10 x  8 =  80
10 x  9 =  90
10 x 10 = 100
Suma de la tabla: 550
```

##### Muchos inválidos
```entrada
0
11
-3
x
5
```
```salida
Número (1-10): Tiene que ser un número del 1 al 10.
Número (1-10): Tiene que ser un número del 1 al 10.
Número (1-10): Tiene que ser un número del 1 al 10.
Número (1-10): Tiene que ser un número del 1 al 10.
Número (1-10):
 5 x  1 =   5
 5 x  2 =  10
 5 x  3 =  15
 5 x  4 =  20
 5 x  5 =  25
 5 x  6 =  30
 5 x  7 =  35
 5 x  8 =  40
 5 x  9 =  45
 5 x 10 =  50
Suma de la tabla: 275
```

### Misión R01-N06-M2 · El adivino de la frontera

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El adivino piensa un número del 1 al 100 con `new Random(semilla).nextInt(100) + 1`
(la semilla se pide al principio). Pedí intentos con un `do`/`while` hasta acertar;
en cada uno decí si el número es mayor o menor. Al final mostrá en cuántos intentos
acertó. Si en 7 intentos no acertó, cortá con `break` y revelá el número.

#### Criterio de aprobación

- Usa `do`/`while` y un contador de intentos.
- Corta con `break` al llegar a 7 intentos.

#### Entrada de ejemplo

```
42
50
25
37
31
```

#### Salida esperada

```
Semilla: Intento:   Es menor
Intento:   Es mayor
Intento:   Es menor
Intento: ¡Acertaste en 4 intentos!
```

#### Solución de referencia

```java
// Mision 2 - El adivino: do/while, contador y break.
import java.util.Random;
import java.util.Scanner;

public class Adivino {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        System.out.print("Semilla: ");
        long semilla = Long.parseLong(teclado.nextLine().trim());
        int secreto = new Random(semilla).nextInt(100) + 1;

        int intentos = 0;
        int intento;
        boolean acerto = false;
        do {
            System.out.print("Intento: ");
            intento = Integer.parseInt(teclado.nextLine().trim());
            intentos++;
            if (intento < secreto) {
                System.out.println("  Es mayor");
            } else if (intento > secreto) {
                System.out.println("  Es menor");
            } else {
                acerto = true;
            }
            if (!acerto && intentos == 7) {
                break;
            }
        } while (!acerto);

        if (acerto) {
            System.out.println("¡Acertaste en " + intentos + " intentos!");
        } else {
            System.out.println("Se acabaron los intentos. Era " + secreto);
        }
    }
}
```

#### Pruebas

##### Acierta al primero
```entrada
42
31
```
```salida
Semilla: Intento: ¡Acertaste en 1 intentos!
```

##### Se queda sin intentos
```entrada
42
1
2
3
4
5
6
7
```
```salida
Semilla: Intento:   Es mayor
Intento:   Es mayor
Intento:   Es mayor
Intento:   Es mayor
Intento:   Es mayor
Intento:   Es mayor
Intento:   Es mayor
Se acabaron los intentos. Era 31
```

### Misión R01-N06-M3 · La cosecha del granero

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Pedí las cosechas de un granero, una por línea, hasta que escriban `fin`. Ignorá con
`continue` las líneas vacías y los números negativos (avisando). Al final mostrá
cuántas cosechas válidas hubo, el total, la mayor y el promedio con un decimal.

#### Criterio de aprobación

- El bucle termina con `fin` (comparado con `equals`).
- Usa `continue` para las entradas inválidas.
- Muestra cantidad, total, mayor y promedio.

#### Entrada de ejemplo

```
120
-5
80

200
fin
```

#### Salida esperada

```
Cosecha (o fin): Cosecha (o fin):   Ignoro el negativo -5
Cosecha (o fin): Cosecha (o fin): Cosecha (o fin): Cosecha (o fin): 
Cosechas válidas: 3
Total: 400
Mayor: 200
Promedio: 133.3
```

#### Solución de referencia

```java
// Mision 3 - La cosecha del granero: bucle hasta "fin", continue, acumuladores.
import java.util.Locale;
import java.util.Scanner;

public class Cosecha {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Scanner teclado = new Scanner(System.in);
        int cantidad = 0;
        int total = 0;
        int mayor = 0;
        while (true) {
            System.out.print("Cosecha (o fin): ");
            String linea = teclado.nextLine().trim();
            if (linea.equals("fin")) {
                break;
            }
            if (linea.isEmpty()) {
                continue;
            }
            int valor = Integer.parseInt(linea);
            if (valor < 0) {
                System.out.println("  Ignoro el negativo " + valor);
                continue;
            }
            cantidad++;
            total += valor;
            mayor = Math.max(mayor, valor);
        }
        System.out.println();
        System.out.println("Cosechas válidas: " + cantidad);
        System.out.println("Total: " + total);
        System.out.println("Mayor: " + mayor);
        System.out.printf("Promedio: %.1f%n", cantidad == 0 ? 0.0 : (double) total / cantidad);
    }
}
```

#### Pruebas

##### Solo fin
```entrada
fin
```
```salida
Cosecha (o fin):
Cosechas válidas: 0
Total: 0
Mayor: 0
Promedio: 0.0
```

##### Todos negativos
```entrada
-1
-2
fin
```
```salida
Cosecha (o fin):   Ignoro el negativo -1
Cosecha (o fin):   Ignoro el negativo -2
Cosecha (o fin):
Cosechas válidas: 0
Total: 0
Mayor: 0
Promedio: 0.0
```

##### Una sola cosecha
```entrada
500
fin
```
```salida
Cosecha (o fin): Cosecha (o fin):
Cosechas válidas: 1
Total: 500
Mayor: 500
Promedio: 500.0
```

### Encargo R01-N06-E1 · El plan de ahorro

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una persona ahorra un monto fijo por mes y el banco le paga un interés mensual sobre
lo acumulado. Pedí el ahorro mensual, el interés mensual (en %) y la meta. Mostrá
mes por mes el saldo (con 2 decimales) hasta llegar a la meta, y cuántos meses tardó.
Si en 120 meses no llega, cortá y avisá.

#### Criterio de aprobación

- Usa un `while` que se detiene al llegar a la meta o a los 120 meses.
- Muestra el saldo de cada mes con 2 decimales.

#### Entrada de ejemplo

```
50000
2
300000
```

#### Salida esperada

```
Ahorro mensual: Interés mensual (%): Meta: 
Mes   1:     50000.00
Mes   2:    101000.00
Mes   3:    153020.00
Mes   4:    206080.40
Mes   5:    260202.01
Mes   6:    315406.05
Llegaste a la meta en 6 meses
```

#### Solución de referencia

```java
// Encargo - El plan de ahorro: while con dos condiciones de corte.
import java.util.Locale;
import java.util.Scanner;

public class Ahorro {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Scanner teclado = new Scanner(System.in);
        System.out.print("Ahorro mensual: ");
        double mensual = Double.parseDouble(teclado.nextLine().trim());
        System.out.print("Interés mensual (%): ");
        double interes = Double.parseDouble(teclado.nextLine().trim()) / 100;
        System.out.print("Meta: ");
        double meta = Double.parseDouble(teclado.nextLine().trim());
        System.out.println();

        double saldo = 0;
        int mes = 0;
        while (saldo < meta && mes < 120) {
            mes++;
            saldo = saldo * (1 + interes) + mensual;
            System.out.printf("Mes %3d: %12.2f%n", mes, saldo);
        }
        if (saldo >= meta) {
            System.out.println("Llegaste a la meta en " + mes + " meses");
        } else {
            System.out.println("En 120 meses no se llega a la meta");
        }
    }
}
```

#### Pruebas

##### No llega en 120 meses
```entrada
100
0
1000000
```
```salida
Ahorro mensual: Interés mensual (%): Meta:
Mes   1:       100.00
Mes   2:       200.00
Mes   3:       300.00
Mes   4:       400.00
Mes   5:       500.00
Mes   6:       600.00
Mes   7:       700.00
Mes   8:       800.00
Mes   9:       900.00
Mes  10:      1000.00
Mes  11:      1100.00
Mes  12:      1200.00
Mes  13:      1300.00
Mes  14:      1400.00
Mes  15:      1500.00
Mes  16:      1600.00
Mes  17:      1700.00
Mes  18:      1800.00
Mes  19:      1900.00
Mes  20:      2000.00
Mes  21:      2100.00
Mes  22:      2200.00
Mes  23:      2300.00
Mes  24:      2400.00
Mes  25:      2500.00
Mes  26:      2600.00
Mes  27:      2700.00
Mes  28:      2800.00
Mes  29:      2900.00
Mes  30:      3000.00
Mes  31:      3100.00
Mes  32:      3200.00
Mes  33:      3300.00
Mes  34:      3400.00
Mes  35:      3500.00
Mes  36:      3600.00
Mes  37:      3700.00
Mes  38:      3800.00
Mes  39:      3900.00
Mes  40:      4000.00
Mes  41:      4100.00
Mes  42:      4200.00
Mes  43:      4300.00
Mes  44:      4400.00
Mes  45:      4500.00
Mes  46:      4600.00
Mes  47:      4700.00
Mes  48:      4800.00
Mes  49:      4900.00
Mes  50:      5000.00
Mes  51:      5100.00
Mes  52:      5200.00
Mes  53:      5300.00
Mes  54:      5400.00
Mes  55:      5500.00
Mes  56:      5600.00
Mes  57:      5700.00
Mes  58:      5800.00
Mes  59:      5900.00
Mes  60:      6000.00
Mes  61:      6100.00
Mes  62:      6200.00
Mes  63:      6300.00
Mes  64:      6400.00
Mes  65:      6500.00
Mes  66:      6600.00
Mes  67:      6700.00
Mes  68:      6800.00
Mes  69:      6900.00
Mes  70:      7000.00
Mes  71:      7100.00
Mes  72:      7200.00
Mes  73:      7300.00
Mes  74:      7400.00
Mes  75:      7500.00
Mes  76:      7600.00
Mes  77:      7700.00
Mes  78:      7800.00
Mes  79:      7900.00
Mes  80:      8000.00
Mes  81:      8100.00
Mes  82:      8200.00
Mes  83:      8300.00
Mes  84:      8400.00
Mes  85:      8500.00
Mes  86:      8600.00
Mes  87:      8700.00
Mes  88:      8800.00
Mes  89:      8900.00
Mes  90:      9000.00
Mes  91:      9100.00
Mes  92:      9200.00
Mes  93:      9300.00
Mes  94:      9400.00
Mes  95:      9500.00
Mes  96:      9600.00
Mes  97:      9700.00
Mes  98:      9800.00
Mes  99:      9900.00
Mes 100:     10000.00
Mes 101:     10100.00
Mes 102:     10200.00
Mes 103:     10300.00
Mes 104:     10400.00
Mes 105:     10500.00
Mes 106:     10600.00
Mes 107:     10700.00
Mes 108:     10800.00
Mes 109:     10900.00
Mes 110:     11000.00
Mes 111:     11100.00
Mes 112:     11200.00
Mes 113:     11300.00
Mes 114:     11400.00
Mes 115:     11500.00
Mes 116:     11600.00
Mes 117:     11700.00
Mes 118:     11800.00
Mes 119:     11900.00
Mes 120:     12000.00
En 120 meses no se llega a la meta
```

##### Llega el primer mes
```entrada
1000
5
500
```
```salida
Ahorro mensual: Interés mensual (%): Meta:
Mes   1:      1000.00
Llegaste a la meta en 1 meses
```

### Prueba del sello

#### ¿Qué diferencia hay entre `while` y `do`/`while`?

`while` pregunta antes de cada vuelta (puede no ejecutarse nunca); `do`/`while` pregunta después (se ejecuta al menos una vez).

#### ¿Cuántas vueltas da `for (int i = 0; i < 5; i++)`?

Cinco: `i` vale 0, 1, 2, 3 y 4.

#### ¿Qué hace `continue`? ¿Y `break`?

`continue` saltea el resto de la vuelta actual y sigue con la próxima; `break` termina el bucle.

#### ¿Por qué el acumulador se declara antes del bucle?

Porque si se declara adentro vuelve a su valor inicial en cada vuelta.

#### ¿Qué hace `"123".matches("\\d+")`?

Devuelve `true`: el texto son solo dígitos (uno o más).

### Soluciones (docente)

Sale de `18-Java/06-Control` (unidad 2), la parte de bucles, con la validación de la entrada que el capítulo original tenía en el 05.

## R01-N07 · Arrays y matrices

```meta
tipo: tema
padre: R01-N06
precio: 10
criatura: orc
temas: col.arrays, col.matrices
```

### Crónica

En el depósito de la Aduana hay estantes numerados: el cajón 0, el 1, el 2… Cada uno guarda un solo paquete, y el depositario sabe exactamente dónde está cada cosa sin revolver. Al fondo, colgado en la pared, hay un mapa de la frontera dividido en cuadrículas. Y en el último estante, cubiertos de polvo, los registros más viejos del Imperio.

—Cuando tenés muchos datos del mismo tipo, no inventes cien variables —dice {mentor}—. Usá un **array**: una fila de cajones con número. Y si tenés filas y columnas, como ese mapa, una **matriz**. Cuidado con el último cajón, Zed: ahí esperan los orcos.

### Objetivos

- Crear arrays, recorrerlos y modificarlos.
- Usar el *for-each* y la propiedad `length`.
- Usar la clase `Arrays`: `toString`, `sort`, `fill`, `copyOf` y `equals`.
- Crear matrices (arrays de dos dimensiones) y recorrerlas por filas y columnas.

### Antes de empezar

- Bucles (Bucles: while, do y for).

### Explicación

#### Crear un array
Un **array** guarda una cantidad **fija** de valores del mismo tipo. Cada uno se
accede por su **índice**, que empieza en 0:
```java
int[] vidas = {30, 45, 12};          // con valores
double[] precios = new double[5];     // 5 lugares, todos en 0.0
String[] nombres = new String[3];     // 3 lugares, todos en null

vidas[0];               // 30, el primero
vidas[2] = 20;          // cambiar el tercero
vidas.length;           // 3 (es una propiedad, sin paréntesis)
vidas[vidas.length - 1]; // el último
```
Los valores iniciales con `new` son: `0` para números, `false` para `boolean` y
`null` para objetos como `String` (`null` significa "no apunta a nada").

El tamaño se fija al crearlo y **no cambia**. Para listas que crecen vas a usar
`ArrayList`, más adelante.

#### Recorrer
Con un `for` común, cuando necesitás el índice:
```java
for (int i = 0; i < vidas.length; i++) {
    System.out.println("Héroe " + i + ": " + vidas[i]);
}
```
Con el **for-each**, cuando solo necesitás cada valor:
```java
int total = 0;
for (int v : vidas) {       // "para cada v en vidas"
    total += v;
}
```
El for-each no sirve para **cambiar** los valores del array (la variable `v` es una
copia) ni cuando necesitás saber la posición.

#### La clase `Arrays`
Tiene métodos útiles (`import java.util.Arrays;`):
```java
Arrays.toString(vidas);           // "[30, 45, 20]" para mostrar
Arrays.sort(vidas);               // ordena de menor a mayor (modifica el array)
Arrays.fill(precios, 9.5);        // todos los lugares en 9.5
int[] copia = Arrays.copyOf(vidas, 5);   // copia con otro tamaño (los nuevos en 0)
Arrays.equals(vidas, copia);      // compara contenido
```
Ojo: `System.out.println(vidas)` no muestra los valores sino algo como
`[I@1b6d3586` (el tipo y un número interno). Usá `Arrays.toString`.

#### Asignar un array no lo copia
```java
int[] a = {1, 2, 3};
int[] b = a;          // b apunta AL MISMO array
b[0] = 99;
System.out.println(a[0]);    // 99
```
Un array es un objeto: la variable guarda una **referencia** (la dirección del
objeto). Para tener una copia independiente, `Arrays.copyOf(a, a.length)` o
`a.clone()`.

#### Matrices
Una matriz es un array de arrays: filas y columnas.
```java
char[][] mapa = {
    {'.', '.', '#'},
    {'.', 'K', '.'},
};
mapa[1][1];               // 'K': fila 1, columna 1
mapa.length;              // 2 filas
mapa[0].length;           // 3 columnas
int[][] tablero = new int[8][8];   // 8x8 en cero
```
Se recorren con dos `for` anidados: el de afuera por filas y el de adentro por
columnas. `Arrays.deepToString(matriz)` la muestra entera.

> **Si venís de C.** Java **controla los índices**: salirse del array corta el
> programa con una excepción en lugar de leer memoria ajena. El largo viaja con el
> array (`length`), así que no hace falta pasarlo aparte.
>
> **Si venís de Python.** Un array no es una lista: tiene tamaño fijo y un solo
> tipo. No hay índices negativos ni *slicing*.

### Código de ejemplo

```java
/*
 * Arrays y matrices: el depósito y el mapa de la frontera.
 */
import java.util.Arrays;

public class Deposito {
    public static void main(String[] args) {
        String[] paquetes = {"sal", "seda", "hierro", "especias", "lana"};
        int[] pesos = {40, 5, 120, 8, 35};

        System.out.println("Paquetes: " + paquetes.length);
        for (int i = 0; i < paquetes.length; i++) {
            System.out.printf("  cajón %d: %-9s %4d kg%n", i, paquetes[i], pesos[i]);
        }

        // for-each con acumulador y máximo
        int total = 0;
        int maximo = pesos[0];
        for (int p : pesos) {
            total += p;
            maximo = Math.max(maximo, p);
        }
        System.out.println("Total: " + total + " kg, el más pesado: " + maximo + " kg");

        // Arrays: copiar, ordenar, mostrar
        int[] ordenados = Arrays.copyOf(pesos, pesos.length);
        Arrays.sort(ordenados);
        System.out.println("Original: " + Arrays.toString(pesos));
        System.out.println("Ordenado: " + Arrays.toString(ordenados));

        // La trampa: asignar no copia
        int[] alias = pesos;
        alias[0] = 0;
        System.out.println("Después de tocar el alias: " + Arrays.toString(pesos));

        // Matriz: el mapa de la frontera
        char[][] mapa = {
            {'.', '.', '#', '.', '.'},
            {'.', '#', '.', '.', 'T'},
            {'K', '.', '.', '#', '.'},
        };
        int muros = 0;
        for (int fila = 0; fila < mapa.length; fila++) {
            for (int col = 0; col < mapa[fila].length; col++) {
                System.out.print(mapa[fila][col] + " ");
                if (mapa[fila][col] == '#') {
                    muros++;
                }
            }
            System.out.println();
        }
        System.out.println("Muros: " + muros + ", Kira en fila 2 columna 0: " + mapa[2][0]);
    }
}
```

### Salida esperada

```
Paquetes: 5
  cajón 0: sal         40 kg
  cajón 1: seda         5 kg
  cajón 2: hierro     120 kg
  cajón 3: especias     8 kg
  cajón 4: lana        35 kg
Total: 208 kg, el más pesado: 120 kg
Original: [40, 5, 120, 8, 35]
Ordenado: [5, 8, 35, 40, 120]
Después de tocar el alias: [0, 5, 120, 8, 35]
. . # . . 
. # . . T 
K . . # . 
Muros: 3, Kira en fila 2 columna 0: K
```

### ¿Para qué sirve?

Las temperaturas de la semana, las notas de un curso, los precios de un catálogo, los píxeles de una imagen, el tablero de un juego: todo son arrays y matrices. Aunque en programas grandes vas a usar más las listas (`ArrayList`), los arrays son la base de todo y aparecen en `main(String[] args)`, en `split` y en cualquier cálculo numérico.

### Errores habituales

**Orco: salirse del array.**
```
Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 5
        at Deposito.main(Deposito.java:12)
```
Los índices van de `0` a `length - 1`. Revisá si el `for` va con `<` y no con `<=`.

**Troll: el alias.** `int[] b = a;` no copia: los dos nombres apuntan al mismo array
y cambiar uno cambia el otro.

**Ogro: mostrar el array con `println`.** Aparece `[I@1b6d3586`. Va
`Arrays.toString(array)`.

**Troll: el `null` de los arrays de objetos.** `new String[3]` tiene tres `null`:
`nombres[0].length()` corta con `NullPointerException` si no le pusiste un valor.

**Slime: `length` con paréntesis.** En arrays es `vidas.length`; en `String`,
`nombre.length()`.

### Micro-misión R01-N07-P1 · Los estantes numerados

```meta
lugar: El depósito de la Aduana
personajes: Zed, Gheco, Nadia
carta: Array | String[] e = {"sal", "seda"}; · e[0] es el primero · e.length es cuántos hay · el último es e[e.length - 1]
recompensa: xp 10, oro 10
```

#### Escena
El depósito es una fila de estantes numerados. Cada uno guarda un solo cajón y el depositario sabe dónde está cada cosa sin revolver.
—Empiezan en el **cero** —le avisa Nadia—. No en el uno. Todos se equivocan la primera vez.

#### Gheco sugiere
Un **array** es una fila de lugares numerados desde 0. `estantes[0]` es el primero y `estantes.length` dice cuántos hay. Como empieza en 0, el **último** está en `estantes.length - 1`.

#### Desafío
Mostrá el último estante usando `length`, sin escribir el número a mano.

#### Código inicial
```java
public class Deposito {
    public static void main(String[] args) {
        String[] estantes = {"sal", "seda", "café", "especias", "vino"};
        System.out.println("Estantes: " + estantes.length);
        System.out.println("Primero: " + estantes[0]);
        System.out.println("Último: " + estantes[___]);
    }
}
```

#### Salida esperada
```
Estantes: 5
Primero: sal
Último: vino
```

#### Solución
```java
public class Deposito {
    public static void main(String[] args) {
        String[] estantes = {"sal", "seda", "café", "especias", "vino"};
        System.out.println("Estantes: " + estantes.length);
        System.out.println("Primero: " + estantes[0]);
        System.out.println("Último: " + estantes[estantes.length - 1]);
    }
}
```

#### Al superarla
El vino está donde decía el registro: en el estante 4, que es el quinto. —Del cero —repite Nadia—. Ya lo vas a soñar.

#### Imagen
- Un depósito largo con estantes de madera numerados del 0 en adelante, cada uno con un cajón distinto (sal, seda, café, especias, vino).
- Nadia señalando el cartel con el 0; Zed contando con los dedos.

### Micro-misión R01-N07-P2 · El orco del último cajón

```meta
lugar: El depósito de la Aduana
personajes: Zed, Gheco, Nadia
criatura: orco
carta: Recorrer un array | for (int i = 0; i < a.length; i++) · con <, nunca <= · pedir a[a.length] da ArrayIndexOutOfBoundsException
recompensa: xp 15, oro 15
```

#### Escena
Zed recorre los cajones para sumar lo que pesan. Al llegar al final, sigue de largo: pide un cajón que no existe y de la oscuridad sale un **orco** gritando *ArrayIndexOutOfBoundsException*.
—Pediste uno de más —dice Gheco, escondido detrás de Nadia.

#### Gheco sugiere
Los índices van de `0` a `length - 1`. Si el bucle llega a `i <= pesos.length`, en la última vuelta pide `pesos[5]`, que no existe. La condición correcta es `i < pesos.length`.

#### Desafío
Ejecutalo, mirá el error y arreglá la condición del `for`.

#### Código inicial
```java
public class Pesos {
    public static void main(String[] args) {
        int[] pesos = {12, 30, 8, 25, 5};
        int total = 0;
        for (int i = 0; i <= pesos.length; i++) {
            total += pesos[i];
        }
        System.out.println("Cajones: " + pesos.length);
        System.out.println("Peso total: " + total + " kg");
    }
}
```

#### Salida esperada
```
Cajones: 5
Peso total: 80 kg
```

#### Solución
```java
public class Pesos {
    public static void main(String[] args) {
        int[] pesos = {12, 30, 8, 25, 5};
        int total = 0;
        for (int i = 0; i < pesos.length; i++) {
            total += pesos[i];
        }
        System.out.println("Cajones: " + pesos.length);
        System.out.println("Peso total: " + total + " kg");
    }
}
```

#### Al superarla
Con `<`, el bucle frena en el último cajón y el orco se queda sin nada que pedir. Se va arrastrando los pies. —Ese vuelve cada vez que alguien cuenta de más —dice Nadia.

#### Imagen
- El fondo oscuro del depósito: después del último estante, un hueco del que sale un orco gritando.
- Gheco escondido detrás de Nadia; Zed con un farol frente al orco.

### Micro-misión R01-N07-P3 · El registro más viejo

```meta
lugar: El archivo del depósito
personajes: Zed, Gheco, Nadia
carta: La clase Arrays | Arrays.sort(a) ordena · Arrays.toString(a) lo muestra entero · import java.util.Arrays;
recompensa: xp 15, oro 15
```

#### Escena
En el archivo del depósito hay registros de viajeros de todas las épocas, mezclados. Zed quiere encontrar el más viejo. Nadia se lo prohíbe… y después le alcanza la escalera.

#### Gheco sugiere
`Arrays.sort(anios)` ordena el array de menor a mayor (lo cambia ahí mismo). `Arrays.toString(anios)` lo devuelve como texto: `[987, 1120, …]`. Hace falta `import java.util.Arrays;`.

#### Desafío
Ordená los años para que el primero sea el más viejo.

#### Código inicial
```java
import java.util.Arrays;

public class Archivo {
    public static void main(String[] args) {
        int[] anios = {1203, 987, 1450, 1120, 1333};
        ___;
        System.out.println(Arrays.toString(anios));
        System.out.println("El más viejo: año " + anios[0]);
    }
}
```

#### Salida esperada
```
[987, 1120, 1203, 1333, 1450]
El más viejo: año 987
```

#### Solución
```java
import java.util.Arrays;

public class Archivo {
    public static void main(String[] args) {
        int[] anios = {1203, 987, 1450, 1120, 1333};
        Arrays.sort(anios);
        System.out.println(Arrays.toString(anios));
        System.out.println("El más viejo: año " + anios[0]);
    }
}
```

#### Al superarla
El registro del año 987 está en el último estante, cubierto de polvo. Un viajero sin nombre declaró una sola cosa: **«un vitral»**. Zed mira su llave de vidrios de colores y no dice nada.
Nadia sí lo nota. Anota algo en su libreta y la cierra rápido.

#### Imagen
- Un pergamino viejísimo bajo la luz de un farol: una sola línea escrita, «un vitral».
- Zed en lo alto de una escalera, con la llave del vitral brillando en la mano.
- Nadia abajo, cerrando su libreta.

### Micro-misión R01-N07-P4 · El mapa de la frontera

```meta
lugar: La pared del depósito
personajes: Zed, Gheco, Nadia
carta: Matriz | int[][] m = {{0, 1}, {1, 0}}; · m[fila][columna] · m.length filas · m[f].length columnas · dos for, uno adentro del otro
recompensa: xp 15, oro 15
```

#### Escena
Colgado en la pared del depósito hay un mapa de la frontera en cuadritos. Donde hay una torre de vigilancia, un 1; donde no, un 0. Nadia quiere saber dónde están todas.

#### Gheco sugiere
Una **matriz** es un array de filas. `mapa.length` es la cantidad de filas y `mapa[f].length` las columnas de la fila `f`. Se recorre con dos `for`: el de afuera por filas y el de adentro por columnas.

#### Desafío
Completá el límite del `for` de adentro: las columnas de esa fila.

#### Código inicial
```java
public class Mapa {
    public static void main(String[] args) {
        int[][] mapa = {
            {0, 1, 0, 0},
            {0, 0, 0, 1},
            {1, 0, 0, 0}
        };
        int torres = 0;
        for (int f = 0; f < mapa.length; f++) {
            for (int c = 0; c < ___; c++) {
                if (mapa[f][c] == 1) {
                    System.out.println("Torre en fila " + f + ", columna " + c);
                    torres++;
                }
            }
        }
        System.out.println("Torres: " + torres);
    }
}
```

#### Salida esperada
```
Torre en fila 0, columna 1
Torre en fila 1, columna 3
Torre en fila 2, columna 0
Torres: 3
```

#### Solución
```java
public class Mapa {
    public static void main(String[] args) {
        int[][] mapa = {
            {0, 1, 0, 0},
            {0, 0, 0, 1},
            {1, 0, 0, 0}
        };
        int torres = 0;
        for (int f = 0; f < mapa.length; f++) {
            for (int c = 0; c < mapa[f].length; c++) {
                if (mapa[f][c] == 1) {
                    System.out.println("Torre en fila " + f + ", columna " + c);
                    torres++;
                }
            }
        }
        System.out.println("Torres: " + torres);
    }
}
```

#### Al superarla
Tres torres, cada una en su cuadrito. Nadia las marca con alfileres. Al lado del mapa cuelga el reglamento de la Aduana: mil páginas.
—¿Alguien lo leyó entero? —pregunta Zed. —Nadie —dice Nadia—. Cada aduanero tiene su librito.

#### Imagen
- Un mapa de la frontera en cuadrícula colgado en la pared, con tres torres marcadas con alfileres rojos.
- Al lado, un reglamento gordísimo colgado de un clavo; Zed lo mira con espanto.

### Misión R01-N07-M1 · Las temperaturas de la semana

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Pedí las temperaturas máximas de los 7 días de la semana y guardalas en un array
de `double`. Mostrá el array con `Arrays.toString`, el promedio (con un decimal), la
máxima, la mínima y en qué día (número del 1 al 7) fue la máxima.

#### Criterio de aprobación

- Guarda los 7 valores en un array.
- Recorre el array para calcular promedio, máxima, mínima y el día.

#### Entrada de ejemplo

```
21.5
24
19.8
27.3
25
18.2
22
```

#### Salida esperada

```
Día 1: Día 2: Día 3: Día 4: Día 5: Día 6: Día 7: 
[21.5, 24.0, 19.8, 27.3, 25.0, 18.2, 22.0]
Promedio: 22.5
Máxima: 27.3 (día 4)
Mínima: 18.2
```

#### Solución de referencia

```java
// Mision 1 - Las temperaturas de la semana: cargar y recorrer un array.
import java.util.Arrays;
import java.util.Locale;
import java.util.Scanner;

public class Temperaturas {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Scanner teclado = new Scanner(System.in);
        double[] temps = new double[7];
        for (int i = 0; i < temps.length; i++) {
            System.out.print("Día " + (i + 1) + ": ");
            temps[i] = Double.parseDouble(teclado.nextLine().trim());
        }
        System.out.println();

        double suma = 0;
        double max = temps[0];
        double min = temps[0];
        int diaMax = 1;
        for (int i = 0; i < temps.length; i++) {
            suma += temps[i];
            if (temps[i] > max) {
                max = temps[i];
                diaMax = i + 1;
            }
            min = Math.min(min, temps[i]);
        }
        System.out.println(Arrays.toString(temps));
        System.out.printf("Promedio: %.1f%n", suma / temps.length);
        System.out.println("Máxima: " + max + " (día " + diaMax + ")");
        System.out.println("Mínima: " + min);
    }
}
```

#### Pruebas

##### Todas iguales
```entrada
20
20
20
20
20
20
20
```
```salida
Día 1: Día 2: Día 3: Día 4: Día 5: Día 6: Día 7:
[20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0]
Promedio: 20.0
Máxima: 20.0 (día 1)
Mínima: 20.0
```

##### Bajo cero
```entrada
-3
-1.5
0
2
-7.25
1
-2
```
```salida
Día 1: Día 2: Día 3: Día 4: Día 5: Día 6: Día 7:
[-3.0, -1.5, 0.0, 2.0, -7.25, 1.0, -2.0]
Promedio: -1.5
Máxima: 2.0 (día 4)
Mínima: -7.25
```

### Misión R01-N07-M2 · El ranking del torneo

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Guardá los puntajes `{340, 125, 980, 560, 125, 720}` en un array. Hacé una **copia**
con `Arrays.copyOf`, ordenala y mostrá el podio (los tres más altos, de mayor a
menor) recorriendo la copia desde el final. Mostrá el array original para demostrar
que no cambió, y usá `Arrays.equals` para comparar el original con la copia.

#### Criterio de aprobación

- Ordena una copia, no el original.
- Muestra el podio recorriendo el array al revés.

#### Salida esperada

```
Podio:
  1. 980
  2. 720
  3. 560
Original: [340, 125, 980, 560, 125, 720]
Ordenado: [125, 125, 340, 560, 720, 980]
¿Iguales? false
```

#### Solución de referencia

```java
// Mision 2 - El ranking del torneo: copiar, ordenar y recorrer al reves.
import java.util.Arrays;

public class Ranking {
    public static void main(String[] args) {
        int[] puntajes = {340, 125, 980, 560, 125, 720};
        int[] ordenados = Arrays.copyOf(puntajes, puntajes.length);
        Arrays.sort(ordenados);

        System.out.println("Podio:");
        int puesto = 1;
        for (int i = ordenados.length - 1; i >= ordenados.length - 3; i--) {
            System.out.println("  " + puesto + ". " + ordenados[i]);
            puesto++;
        }
        System.out.println("Original: " + Arrays.toString(puntajes));
        System.out.println("Ordenado: " + Arrays.toString(ordenados));
        System.out.println("¿Iguales? " + Arrays.equals(puntajes, ordenados));
    }
}
```

### Misión R01-N07-M3 · El mapa del tesoro

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Creá una matriz de `char` de 4 filas por 6 columnas llena de `'.'` (con dos `for` o
con `Arrays.fill` en cada fila). Pedí la fila y la columna del tesoro y marcalo con
`'X'`. Marcá también con `'#'` toda la columna 2 (un río). Mostrá el mapa y cuántas
casillas libres (`'.'`) quedan. Si la posición del tesoro está fuera del mapa,
avisá sin cortar el programa.

#### Criterio de aprobación

- Crea y recorre la matriz con bucles anidados.
- Valida la posición antes de usarla.

#### Entrada de ejemplo

```
1
4
```

#### Salida esperada

```
Fila del tesoro: Columna del tesoro: 
..#...
..#.X.
..#...
..#...
Casillas libres: 19
```

#### Solución de referencia

```java
// Mision 3 - El mapa del tesoro: matriz de char, validar indices.
import java.util.Arrays;
import java.util.Scanner;

public class MapaTesoro {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        char[][] mapa = new char[4][6];
        for (char[] fila : mapa) {
            Arrays.fill(fila, '.');
        }
        for (int f = 0; f < mapa.length; f++) {
            mapa[f][2] = '#';
        }

        System.out.print("Fila del tesoro: ");
        int fila = Integer.parseInt(teclado.nextLine().trim());
        System.out.print("Columna del tesoro: ");
        int col = Integer.parseInt(teclado.nextLine().trim());
        System.out.println();

        if (fila >= 0 && fila < mapa.length && col >= 0 && col < mapa[0].length) {
            mapa[fila][col] = 'X';
        } else {
            System.out.println("Esa posición está fuera del mapa");
        }

        int libres = 0;
        for (char[] f : mapa) {
            for (char c : f) {
                System.out.print(c);
                if (c == '.') {
                    libres++;
                }
            }
            System.out.println();
        }
        System.out.println("Casillas libres: " + libres);
    }
}
```

#### Pruebas

##### Tesoro sobre el río
```entrada
0
2
```
```salida
Fila del tesoro: Columna del tesoro:
..X...
..#...
..#...
..#...
Casillas libres: 20
```

##### Fuera del mapa
```entrada
4
6
```
```salida
Fila del tesoro: Columna del tesoro:
Esa posición está fuera del mapa
..#...
..#...
..#...
..#...
Casillas libres: 20
```

##### Esquina
```entrada
3
5
```
```salida
Fila del tesoro: Columna del tesoro:
..#...
..#...
..#...
..#..X
Casillas libres: 19
```

### Encargo R01-N07-E1 · Las ventas por sucursal

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una cadena de 3 sucursales registra las ventas de 4 meses en una matriz de `int`
(filas = sucursales, columnas = meses):
`{{120, 150, 90, 200}, {80, 95, 110, 105}, {300, 280, 310, 290}}`.
Mostrá la tabla con el total de cada sucursal (al final de cada fila) y el total de
cada mes (en una última fila), alineado con `printf`. Mostrá también qué sucursal
vendió más.

#### Criterio de aprobación

- Recorre la matriz por filas y por columnas.
- Los totales son correctos.

#### Salida esperada

```
Sucursal    Mes1  Mes2  Mes3  Mes4  Total
S1           120   150    90   200    560
S2            80    95   110   105    390
S3           300   280   310   290   1180
Total        500   525   510   595
La que más vendió: S3 (1180)
```

#### Solución de referencia

```java
// Encargo - Las ventas por sucursal: totales por fila y por columna de una matriz.
public class Ventas {
    public static void main(String[] args) {
        int[][] ventas = {{120, 150, 90, 200}, {80, 95, 110, 105}, {300, 280, 310, 290}};

        System.out.printf("%-10s", "Sucursal");
        for (int m = 0; m < ventas[0].length; m++) {
            System.out.printf("%6s", "Mes" + (m + 1));
        }
        System.out.printf("%7s%n", "Total");

        int mejor = 0;
        int mejorTotal = 0;
        for (int s = 0; s < ventas.length; s++) {
            System.out.printf("%-10s", "S" + (s + 1));
            int total = 0;
            for (int m = 0; m < ventas[s].length; m++) {
                System.out.printf("%6d", ventas[s][m]);
                total += ventas[s][m];
            }
            System.out.printf("%7d%n", total);
            if (total > mejorTotal) {
                mejorTotal = total;
                mejor = s;
            }
        }
        System.out.printf("%-10s", "Total");
        for (int m = 0; m < ventas[0].length; m++) {
            int totalMes = 0;
            for (int s = 0; s < ventas.length; s++) {
                totalMes += ventas[s][m];
            }
            System.out.printf("%6d", totalMes);
        }
        System.out.println();
        System.out.println("La que más vendió: S" + (mejor + 1) + " (" + mejorTotal + ")");
    }
}
```

### Prueba del sello

#### ¿Cuál es el índice del último elemento de un array `a`?

`a.length - 1`.

#### ¿Qué pasa si hacés `int[] b = a;` y después `b[0] = 5;`?

Cambia también `a[0]`: los dos nombres apuntan al mismo array.

#### ¿Qué muestra `System.out.println(new int[]{1, 2})`?

Algo como `[I@1b6d3586`, no los valores. Para ver los valores se usa `Arrays.toString`.

#### ¿Con qué valor empiezan los lugares de `new String[3]`?

Con `null`.

#### En `int[][] m = new int[3][5];`, ¿qué es `m.length` y qué es `m[0].length`?

`3` (las filas) y `5` (las columnas de la fila 0).

### Soluciones (docente)

Sale de `18-Java/07-Arrays-Matrices` (unidad 4 de la cátedra: estructuras de datos).

## R01-N08 · Métodos: dividir el trabajo

```meta
tipo: tema
padre: R01-N07
precio: 10
criatura: skeleton
temas: prog.funciones, prog.recursion
```

### Crónica

La Aduana tiene un reglamento de mil páginas, pero ningún aduanero lo lee entero: cada uno tiene su librito. Uno pesa, otro cobra, otro sella. Cuando algo cambia, se cambia un solo librito. Zed recorre los pasillos mirando por cada puerta: ninguno sabe hacer todo, y entre todos no se les escapa nada.

—Un programa de mil líneas en un solo `main` es un reglamento que nadie entiende —dice {mentor}—. Partilo en **métodos**: cada uno hace una cosa, tiene un nombre y se puede probar solo. Al final de estos pasillos hay alguien que solo se deja vencer así.

### Objetivos

- Declarar métodos `static` con parámetros y valor de retorno.
- Entender el paso por valor (y qué pasa cuando el parámetro es un array).
- Sobrecargar métodos: mismo nombre, distintos parámetros.
- Escribir métodos recursivos.

### Antes de empezar

- Arrays (Arrays y matrices).

### Explicación

#### Declarar y llamar un método
```java
public class Aduana {
    // tipo de retorno, nombre, parámetros
    static int calcularTasa(int kilos, boolean urgente) {
        int tasa = kilos * 2;
        if (urgente) {
            tasa += 10;
        }
        return tasa;               // devuelve el valor y termina el método
    }

    public static void main(String[] args) {
        int t = calcularTasa(30, true);     // se llama con valores (argumentos)
        System.out.println(t);              // 70
    }
}
```
- **`static`**: el método es de la clase y se llama sin crear objetos (lo vas a
  entender del todo con las clases). Por ahora, todos los métodos que se llaman desde
  `main` llevan `static`.
- **Tipo de retorno**: lo que devuelve (`int`, `double`, `String`, `int[]`…).
  `void` significa que no devuelve nada.
- **Parámetros**: las variables que recibe, con su tipo, separadas por comas.
- **`return`**: devuelve el valor. En un método `void` se puede usar `return;`
  solo, para terminar antes.

Los nombres de los métodos son verbos en *camelCase*: `calcularTasa`,
`mostrarMenu`, `esPar`.

#### Alcance: cada método tiene sus variables
Las variables declaradas dentro de un método (incluidos los parámetros) existen
**solo ahí**. Dos métodos pueden tener variables con el mismo nombre sin chocar.

#### Paso por valor
Java pasa **una copia del valor** de cada argumento. Si el método cambia su
parámetro, la variable original no cambia:
```java
static void duplicar(int x) {
    x = x * 2;            // cambia la copia
}
int n = 5;
duplicar(n);
System.out.println(n);    // 5
```
Con un **array** también se copia el valor... pero el valor es una **referencia**.
El método recibe otra variable que apunta **al mismo array**, así que si cambia sus
elementos, el cambio se ve afuera:
```java
static void vaciar(int[] datos) {
    datos[0] = 0;         // cambia el array original
}
```

#### Sobrecarga
Varios métodos pueden llamarse igual si tienen **distintos parámetros** (cantidad o
tipos). Java elige el que corresponde según los argumentos:
```java
static int mayor(int a, int b) { return a > b ? a : b; }
static int mayor(int a, int b, int c) { return mayor(mayor(a, b), c); }
static double mayor(double a, double b) { return a > b ? a : b; }
```
El tipo de retorno solo no alcanza para distinguirlos.

#### Recursión
Un método puede llamarse a sí mismo. Necesita un **caso base** que corte:
```java
static long factorial(int n) {
    if (n <= 1) {
        return 1;                      // caso base
    }
    return n * factorial(n - 1);       // caso recursivo: un problema más chico
}
```
Sin caso base, las llamadas no terminan y el programa se corta con
`StackOverflowError`.

#### Los argumentos del `main`
`String[] args` recibe lo que escribís después del nombre del programa:
`java Saludo.java Kira 3` da `args[0] = "Kira"` y `args[1] = "3"`.

> **Si venís de C.** No hacen falta prototipos: un método se puede usar antes de
> declararlo en el archivo. No hay punteros para "devolver" varios valores: se
> devuelve un objeto o un array.

### Código de ejemplo

```java
/*
 * Métodos: los libritos de la Aduana.
 */
import java.util.Arrays;

public class Libritos {
    public static void main(String[] args) {
        mostrarTitulo("Aduana del Imperio");

        int tasa = calcularTasa(30, true);
        System.out.println("Tasa de 30 kg urgente: " + tasa);
        System.out.println("Tasa de 12 kg normal: " + calcularTasa(12, false));

        // Sobrecarga
        System.out.println("Mayor de 3 y 8: " + mayor(3, 8));
        System.out.println("Mayor de 3, 8 y 5: " + mayor(3, 8, 5));
        System.out.println("Mayor de 2.5 y 1.5: " + mayor(2.5, 1.5));

        // Paso por valor
        int oro = 50;
        intentarDuplicar(oro);
        System.out.println("Oro después de intentarDuplicar: " + oro);
        oro = duplicado(oro);
        System.out.println("Oro después de duplicado: " + oro);

        // Un array se pasa por referencia al mismo objeto
        int[] cargas = {40, 5, 120};
        aplicarDescuento(cargas, 10);
        System.out.println("Cargas con descuento: " + Arrays.toString(cargas));
        System.out.println("Promedio: " + promedio(cargas));

        // Recursión
        System.out.println("Formas de ordenar 5 carros: " + factorial(5));
        System.out.println("¿El 47 es primo? " + esPrimo(47));
    }

    static void mostrarTitulo(String texto) {
        String linea = "=".repeat(texto.length() + 4);
        System.out.println(linea);
        System.out.println("  " + texto);
        System.out.println(linea);
    }

    static int calcularTasa(int kilos, boolean urgente) {
        int tasa = kilos * 2;
        if (urgente) {
            tasa += 10;
        }
        return tasa;
    }

    static int mayor(int a, int b) {
        return a > b ? a : b;
    }

    static int mayor(int a, int b, int c) {
        return mayor(mayor(a, b), c);
    }

    static double mayor(double a, double b) {
        return a > b ? a : b;
    }

    static void intentarDuplicar(int x) {
        x = x * 2;                  // cambia solo la copia
    }

    static int duplicado(int x) {
        return x * 2;               // devuelve el resultado: así sí
    }

    static void aplicarDescuento(int[] valores, int descuento) {
        for (int i = 0; i < valores.length; i++) {
            valores[i] = Math.max(0, valores[i] - descuento);
        }
    }

    static double promedio(int[] valores) {
        int suma = 0;
        for (int v : valores) {
            suma += v;
        }
        return (double) suma / valores.length;
    }

    static long factorial(int n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }

    static boolean esPrimo(int n) {
        if (n < 2) {
            return false;
        }
        for (int d = 2; d * d <= n; d++) {
            if (n % d == 0) {
                return false;
            }
        }
        return true;
    }
}
```

### Salida esperada

```
======================
  Aduana del Imperio
======================
Tasa de 30 kg urgente: 70
Tasa de 12 kg normal: 24
Mayor de 3 y 8: 8
Mayor de 3, 8 y 5: 8
Mayor de 2.5 y 1.5: 2.5
Oro después de intentarDuplicar: 50
Oro después de duplicado: 100
Cargas con descuento: [30, 0, 110]
Promedio: 46.666666666666664
Formas de ordenar 5 carros: 120
¿El 47 es primo? true
```

### ¿Para qué sirve?

Los métodos son la herramienta principal para escribir programas que se entienden y se pueden mantener. Un método con buen nombre (`calcularIva`, `validarDni`) se lee como una frase, se prueba solo y se reutiliza en todo el sistema. Cuando una regla del negocio cambia, se cambia en un solo lugar.

### Errores habituales

**Esqueleto: llamar un método que no existe o con otro nombre.**
```
Libritos.java:8: error: cannot find symbol
        int tasa = calcularTaza(30, true);
                   ^
  symbol:   method calcularTaza(int,boolean)
```

**Goblin: argumentos de otro tipo o en otra cantidad.**
```
error: method calcularTasa in class Libritos cannot be applied to given types;
  required: int,boolean
  found:    int
```

**Slime: falta el `return`.** Un método que no es `void` tiene que devolver algo en
todos los caminos: `missing return statement`.

**Esqueleto: llamar un método no `static` desde `main`.** `non-static method
calcular(int) cannot be referenced from a static context`: agregale `static` (por
ahora).

**Ogro: esperar que el método cambie un `int`.** Los primitivos se copian: si el
método tiene que cambiar un valor, que lo **devuelva**.

**Ogro: recursión sin caso base.** `Exception in thread "main"
java.lang.StackOverflowError`.

### Micro-misión R01-N08-P1 · El librito del pesador

```meta
lugar: Los pasillos de los aduaneros
personajes: Zed, Gheco, Nadia
carta: Método con return | static double peaje(int kg) { return kg * 0.5; } · recibe datos, devuelve un resultado · se llama por su nombre
recompensa: xp 10, oro 10
```

#### Escena
En los pasillos de la Aduana, cada aduanero tiene su librito: uno pesa, otro cobra, otro sella. El pesador le muestra a Zed el suyo: una sola regla, «medio denario por kilo».
—Un **método** es eso —dice Gheco—: un librito con nombre. Le das los datos y te devuelve la respuesta.

#### Gheco sugiere
`static double peaje(int kg) { … }` declara un método que recibe un `int` y **devuelve** un `double`. Adentro, `return …;` dice qué devuelve. En `main` se usa como un valor: `peaje(10)`.

#### Desafío
Escribí el `return` del método: medio denario por kilo.

#### Código inicial
```java
public class Pesador {
    static double peaje(int kg) {
        ___;
    }

    public static void main(String[] args) {
        System.out.println("10 kg: " + peaje(10));
        System.out.println("40 kg: " + peaje(40));
        System.out.println("Los dos: " + (peaje(10) + peaje(40)));
    }
}
```

#### Salida esperada
```
10 kg: 5.0
40 kg: 20.0
Los dos: 25.0
```

#### Solución
```java
public class Pesador {
    static double peaje(int kg) {
        return kg * 0.5;
    }

    public static void main(String[] args) {
        System.out.println("10 kg: " + peaje(10));
        System.out.println("40 kg: " + peaje(40));
        System.out.println("Los dos: " + (peaje(10) + peaje(40)));
    }
}
```

#### Al superarla
El pesador asiente: el librito de Zed dice lo mismo que el suyo. —Cuando cambie la tarifa —le explica—, cambio una sola línea y todos los carros pagan lo nuevo.

#### Imagen
- Un pasillo de la Aduana con puertitas; en cada una, un aduanero con un librito distinto.
- El pesador, viejo y de delantal, mostrándole a Zed un librito con una sola regla.

### Micro-misión R01-N08-P2 · El librito del sellador

```meta
lugar: Los pasillos de los aduaneros
personajes: Zed, Gheco, Nadia
carta: Parámetros y tipo de retorno | static String sello(String nombre, boolean declarado) · varios parámetros separados por coma · void si no devuelve nada
recompensa: xp 10, oro 10
```

#### Escena
El sellador decide entre dos sellos: APROBADO si el viajero declaró todo, RETENIDO si no. Nadia le pide a Zed que escriba ese librito. —Y que devuelva el texto del sello, no que lo muestre: lo usa otro aduanero.

#### Gheco sugiere
Antes del nombre del método va el **tipo de lo que devuelve**: `String` si devuelve un texto, `int` si un número, `void` si no devuelve nada. Los parámetros van entre paréntesis, separados por coma.

#### Desafío
Completá el tipo de retorno del método.

#### Código inicial
```java
public class Sellador {
    static ___ sello(String nombre, boolean declarado) {
        if (declarado) {
            return "APROBADO: " + nombre;
        }
        return "RETENIDO: " + nombre;
    }

    public static void main(String[] args) {
        System.out.println(sello("Nadia", true));
        System.out.println(sello("un tahúr", false));
        String deZed = sello("Zed", true);
        System.out.println(deZed.toLowerCase());
    }
}
```

#### Salida esperada
```
APROBADO: Nadia
RETENIDO: un tahúr
aprobado: zed
```

#### Solución
```java
public class Sellador {
    static String sello(String nombre, boolean declarado) {
        if (declarado) {
            return "APROBADO: " + nombre;
        }
        return "RETENIDO: " + nombre;
    }

    public static void main(String[] args) {
        System.out.println(sello("Nadia", true));
        System.out.println(sello("un tahúr", false));
        String deZed = sello("Zed", true);
        System.out.println(deZed.toLowerCase());
    }
}
```

#### Al superarla
«aprobado: zed», en minúsculas, como un susurro. Zed se queda mirándolo. Es la primera vez que un papel dice que él puede estar acá.

#### Imagen
- Dos sellos de bronce sobre un escritorio: APROBADO en dorado y RETENIDO en rojo.
- Zed mirando un papel sellado con su nombre; Nadia lo observa de reojo.

### Micro-misión R01-N08-P3 · Dos formas de cobrar

```meta
lugar: La ventanilla del cobrador
personajes: Zed, Gheco, Nadia
carta: Sobrecarga | mismo nombre, distintos parámetros · cobrar(int kg) y cobrar(int kg, int carros) · Java elige por lo que le pasás
recompensa: xp 15, oro 15
```

#### Escena
El cobrador tiene dos tarifas con el mismo nombre: «cobrar». Si viene un carro solo, 2 denarios por kilo. Si vienen varios carros con la misma carga, se cobra por cada uno y se descuenta 5 por carro.
—¿Dos libritos con el mismo nombre? —pregunta Zed. —Mientras reciban cosas distintas, Java sabe cuál abrir —dice Gheco.

#### Gheco sugiere
**Sobrecarga**: dos métodos con el mismo nombre y distintos parámetros. `cobrar(30)` usa el de un parámetro y `cobrar(30, 3)` el de dos. Uno puede llamar al otro: `cobrar(kg) * carros`.

#### Desafío
Completá el `return` del segundo `cobrar`: lo de un carro por la cantidad de carros, menos 5 por carro.

#### Código inicial
```java
public class Cobrador {
    static int cobrar(int kg) {
        return kg * 2;
    }

    static int cobrar(int kg, int carros) {
        return ___;
    }

    public static void main(String[] args) {
        System.out.println("Un carro de 30 kg: " + cobrar(30));
        System.out.println("Tres carros de 30 kg: " + cobrar(30, 3));
    }
}
```

#### Salida esperada
```
Un carro de 30 kg: 60
Tres carros de 30 kg: 165
```

#### Solución
```java
public class Cobrador {
    static int cobrar(int kg) {
        return kg * 2;
    }

    static int cobrar(int kg, int carros) {
        return cobrar(kg) * carros - 5 * carros;
    }

    public static void main(String[] args) {
        System.out.println("Un carro de 30 kg: " + cobrar(30));
        System.out.println("Tres carros de 30 kg: " + cobrar(30, 3));
    }
}
```

#### Al superarla
El cobrador cobra 60 y 165 sin pensar. —El segundo librito usa el primero —le explica Gheco a Zed—: si cambia la tarifa por kilo, cambian los dos.

#### Imagen
- Una ventanilla con dos libritos de tapa igual, «cobrar», uno fino y uno más grueso.
- Una fila de tres carros iguales esperando; el cobrador contando monedas.

### Micro-misión R01-N08-P4 · La escalera sin fin

```meta
lugar: La escalera al último pasillo
personajes: Zed, Gheco, Nadia
criatura: esqueleto
carta: Recursión | un método que se llama a sí mismo · necesita un caso base que corte · sin él: StackOverflowError
recompensa: xp 15, oro 15
```

#### Escena
Para llegar al último pasillo hay una escalera de caracol. Zed escribe un librito para bajar escalón por escalón: «bajar un escalón y volver a bajar». Nunca llega abajo. Al fondo, un **esqueleto** que intentó lo mismo hace siglos todavía está bajando.

#### Gheco sugiere
Un método **recursivo** se llama a sí mismo con un problema más chico: `bajar(n - 1)`. Necesita un **caso base** que corte sin volver a llamarse: cuando `n == 0`, ya llegaste. Sin él, se llena la pila y aparece `StackOverflowError`.

#### Desafío
Completá la condición del caso base: cuando no quedan escalones.

#### Código inicial
```java
public class Escalera {
    static void bajar(int escalones) {
        if (___) {
            System.out.println("¡Abajo! Ahí está el último pasillo.");
            return;
        }
        System.out.println("Faltan " + escalones);
        bajar(escalones - 1);
    }

    public static void main(String[] args) {
        bajar(4);
    }
}
```

#### Salida esperada
```
Faltan 4
Faltan 3
Faltan 2
Faltan 1
¡Abajo! Ahí está el último pasillo.
```

#### Solución
```java
public class Escalera {
    static void bajar(int escalones) {
        if (escalones == 0) {
            System.out.println("¡Abajo! Ahí está el último pasillo.");
            return;
        }
        System.out.println("Faltan " + escalones);
        bajar(escalones - 1);
    }

    public static void main(String[] args) {
        bajar(4);
    }
}
```

#### Al superarla
Cuatro escalones y abajo. El esqueleto, que seguía bajando, se detiene y se sienta, aliviado.
Al final del último pasillo, sobre un trono de piedra, una armadura vacía sostiene un libro de registros. Gheco baja la voz: —El **Centinela**.

#### Imagen
- Una escalera de caracol de piedra que baja en espiral; un esqueleto sentado en un escalón, aliviado.
- Al fondo, la silueta de una armadura sentada en un trono de piedra, con un libro abierto en las rodillas.
- Gheco, el gecko cian, escondido en el hombro de Zed.

### Misión R01-N08-M1 · El conversor del cambista

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí tres métodos: `aDenarios(double pesos)` que convierte pesos a denarios (1
denario = 250 pesos), `aPesos(double denarios)` que hace lo contrario, y
`redondear(double valor, int decimales)` que redondea a esa cantidad de decimales
(con `Math.round` y `Math.pow`). Pedí un monto en pesos y mostrá cuántos denarios son,
redondeado a 2 decimales, y la vuelta a pesos.

#### Criterio de aprobación

- Los tres métodos son `static`, reciben parámetros y devuelven un valor.
- El `main` solo lee, llama a los métodos y muestra.

#### Entrada de ejemplo

```
12345
```

#### Salida esperada

```
Pesos: 
12345.0 pesos son 49.38 denarios
49.38 denarios son 12345.0 pesos
```

#### Solución de referencia

```java
// Mision 1 - El conversor del cambista: metodos con parametros y retorno.
import java.util.Scanner;

public class Cambista {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        System.out.print("Pesos: ");
        double pesos = Double.parseDouble(teclado.nextLine().trim());
        System.out.println();

        double denarios = redondear(aDenarios(pesos), 2);
        System.out.println(pesos + " pesos son " + denarios + " denarios");
        System.out.println(denarios + " denarios son " + redondear(aPesos(denarios), 2) + " pesos");
    }

    static double aDenarios(double pesos) {
        return pesos / 250;
    }

    static double aPesos(double denarios) {
        return denarios * 250;
    }

    static double redondear(double valor, int decimales) {
        double factor = Math.pow(10, decimales);
        return Math.round(valor * factor) / factor;
    }
}
```

#### Pruebas

##### Cero
```entrada
0
```
```salida
Pesos:
0.0 pesos son 0.0 denarios
0.0 denarios son 0.0 pesos
```

##### Monto chico
```entrada
1
```
```salida
Pesos:
1.0 pesos son 0.0 denarios
0.0 denarios son 0.0 pesos
```

##### Monto grande
```entrada
1000000
```
```salida
Pesos:
1000000.0 pesos son 4000.0 denarios
4000.0 denarios son 1000000.0 pesos
```

### Misión R01-N08-M2 · Las estadísticas del regimiento

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí métodos que reciban un `int[]`: `suma`, `maximo`, `contarMayoresA(int[]
datos, int limite)` y `normalizar(int[] datos)`, que cambia el array para que ningún
valor pase de 100 (los que pasan quedan en 100). En el `main`, con las fuerzas
`{85, 120, 60, 101, 95}`, mostrá la suma, el máximo, cuántos superan 90, y el array
antes y después de normalizar.

#### Criterio de aprobación

- `normalizar` es `void` y modifica el array recibido.
- Los demás métodos devuelven su resultado sin modificar el array.

#### Salida esperada

```
Suma: 461
Máximo: 120
Superan 90: 3
Antes: [85, 120, 60, 101, 95]
Después: [85, 100, 60, 100, 95]
```

#### Solución de referencia

```java
// Mision 2 - Las estadisticas del regimiento: metodos que reciben arrays.
import java.util.Arrays;

public class Regimiento {
    public static void main(String[] args) {
        int[] fuerzas = {85, 120, 60, 101, 95};
        System.out.println("Suma: " + suma(fuerzas));
        System.out.println("Máximo: " + maximo(fuerzas));
        System.out.println("Superan 90: " + contarMayoresA(fuerzas, 90));
        System.out.println("Antes: " + Arrays.toString(fuerzas));
        normalizar(fuerzas);
        System.out.println("Después: " + Arrays.toString(fuerzas));
    }

    static int suma(int[] datos) {
        int total = 0;
        for (int d : datos) {
            total += d;
        }
        return total;
    }

    static int maximo(int[] datos) {
        int max = datos[0];
        for (int d : datos) {
            max = Math.max(max, d);
        }
        return max;
    }

    static int contarMayoresA(int[] datos, int limite) {
        int cantidad = 0;
        for (int d : datos) {
            if (d > limite) {
                cantidad++;
            }
        }
        return cantidad;
    }

    static void normalizar(int[] datos) {
        for (int i = 0; i < datos.length; i++) {
            datos[i] = Math.min(datos[i], 100);
        }
    }
}
```

### Misión R01-N08-M3 · La escalera de la torre

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí dos métodos **recursivos**: `potencia(int base, int exp)` (sin usar
`Math.pow`) y `sumaDigitos(int n)`, que suma los dígitos de un número (la suma de
los dígitos de 4719 es 21). Escribí además un método **sobrecargado** `dibujar`:
`dibujar(int n)` muestra una escalera de `n` escalones con `#`, y `dibujar(int n,
char c)` hace lo mismo con otro carácter. Probá todos desde el `main`.

#### Criterio de aprobación

- `potencia` y `sumaDigitos` son recursivos, con caso base.
- `dibujar` está sobrecargado y una versión reutiliza a la otra o comparten lógica.

#### Salida esperada

```
2^10 = 1024
3^0 = 1
Suma de dígitos de 4719: 21
#
##
###
####
*
**
***
```

#### Solución de referencia

```java
// Mision 3 - La escalera de la torre: recursion y sobrecarga.
public class Escalera {
    public static void main(String[] args) {
        System.out.println("2^10 = " + potencia(2, 10));
        System.out.println("3^0 = " + potencia(3, 0));
        System.out.println("Suma de dígitos de 4719: " + sumaDigitos(4719));
        dibujar(4);
        dibujar(3, '*');
    }

    static long potencia(int base, int exp) {
        if (exp == 0) {
            return 1;
        }
        return base * potencia(base, exp - 1);
    }

    static int sumaDigitos(int n) {
        if (n < 10) {
            return n;
        }
        return n % 10 + sumaDigitos(n / 10);
    }

    static void dibujar(int n) {
        dibujar(n, '#');
    }

    static void dibujar(int n, char c) {
        for (int i = 1; i <= n; i++) {
            System.out.println(String.valueOf(c).repeat(i));
        }
    }
}
```

### Encargo R01-N08-E1 · El validador de CUIT

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un CUIT tiene 11 dígitos y el último es un **dígito verificador**: se multiplican los
10 primeros por `5, 4, 3, 2, 7, 6, 5, 4, 3, 2`, se suman, y el verificador es `11 -
(suma % 11)`; si da 11 es 0, y si da 10 el CUIT es inválido. Escribí un método
`boolean cuitValido(String cuit)` (acepta el formato con guiones `20-12345678-6`) y
probalo con los CUIT que se leen, uno por línea, hasta una línea vacía.

#### Criterio de aprobación

- La validación está en un método que devuelve `boolean`.
- Quita los guiones y rechaza lo que no tenga 11 dígitos.

#### Entrada de ejemplo

```
20-12345678-6
20-12345678-5
27-40111222-2
123

```

#### Salida esperada

```
20-12345678-6: válido
20-12345678-5: inválido
27-40111222-2: válido
123: inválido
```

#### Solución de referencia

```java
// Encargo - El validador de CUIT: un metodo que devuelve boolean.
import java.util.Scanner;

public class Cuit {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.isEmpty()) {
                break;
            }
            System.out.println(linea + ": " + (cuitValido(linea) ? "válido" : "inválido"));
        }
    }

    static boolean cuitValido(String cuit) {
        String digitos = cuit.replace("-", "");
        if (!digitos.matches("\\d{11}")) {
            return false;
        }
        int[] pesos = {5, 4, 3, 2, 7, 6, 5, 4, 3, 2};
        int suma = 0;
        for (int i = 0; i < 10; i++) {
            suma += (digitos.charAt(i) - '0') * pesos[i];
        }
        int verificador = 11 - suma % 11;
        if (verificador == 11) {
            verificador = 0;
        }
        if (verificador == 10) {
            return false;
        }
        return verificador == digitos.charAt(10) - '0';
    }
}
```

#### Pruebas

##### Verificador 0
```entrada
20-00000000-1
```
```salida
20-00000000-1: válido
```

##### Con letras y largo raro
```entrada
20-1234567A-6
2012345678
```
```salida
20-1234567A-6: inválido
2012345678: inválido
```

##### Sin guiones
```entrada
20123456786
```
```salida
20123456786: válido
```

### Prueba del sello

#### ¿Qué significa `void` en la declaración de un método?

Que el método no devuelve ningún valor.

#### Si un método recibe un `int` y le cambia el valor, ¿cambia la variable original?

No: Java pasa una copia del valor.

#### ¿Y si recibe un array y cambia `datos[0]`?

Sí se ve afuera: la copia es de la referencia, y apunta al mismo array.

#### ¿Qué es la sobrecarga?

Tener varios métodos con el mismo nombre y distintos parámetros; Java elige cuál llamar según los argumentos.

#### ¿Qué necesita todo método recursivo para no terminar en `StackOverflowError`?

Un caso base que no vuelva a llamarse, y que cada llamada se acerque a él.

### Soluciones (docente)

Sale de `18-Java/08-Metodos` (unidad 4). Los CUIT de la entrada del encargo están armados para que den un válido, un verificador equivocado, otro válido y uno con largo incorrecto.

## R01-N09 · Jefe: el Centinela de la Aduana

```meta
tipo: jefe
padre: R01-N08
precio: 10
criatura: dragon
insignia: Sello del Centinela
insignia_descripcion: Venciste al Centinela de la Aduana: dominás los fundamentos de Java.
usa: prog.funciones, col.arrays, err.validacion
```

### Crónica

Al final del último pasillo de la Aduana, sentado en un trono de piedra, está el **Centinela**: una armadura sin nadie adentro, con un libro de registros abierto sobre las rodillas. Hace siglos que nadie cruza sin que él lo apruebe. Zed estudia las juntas de la armadura, buscando por dónde colarse. No hay por dónde.

—No se lo vence con fuerza ni con trampas —le dice {mentor} en voz baja, con la taza de café en la mano—. Se lo vence con **orden**. Leé bien lo que pide, partí el problema en métodos, probá cada uno, y recién después juntalos. Si pasás por él, Zed, vas a estar declarado. Por primera vez en tu vida.

### Objetivos

- Integrar todo lo de la rama en programas completos: entrada validada, decisiones, bucles, arrays y métodos.
- Partir un problema grande en métodos chicos con nombres claros.
- Probar un programa con entradas preparadas.

### Antes de empezar

- Toda la rama: variables, operadores, textos, `Scanner`, decisiones, bucles, arrays y métodos.

### Explicación

#### Cómo se enfrenta a un jefe
Un jefe es un programa más largo que los de las misiones. No se escribe de un tirón:
se **parte**.
1. **Leé la consigna entera** y la salida esperada. Anotá qué datos entran, qué sale
   y qué reglas hay.
2. **Hacé la lista de métodos**: uno por cada tarea con nombre ("leer un entero
   válido", "calcular la tasa", "mostrar el informe"). Si un método no entra en la
   pantalla, partilo.
3. **Decidí qué recibe y qué devuelve cada uno.** Los datos entran por parámetros y
   salen por `return`; si un método tiene que llenar un array, lo recibe y lo
   modifica.
4. **Escribí y probá de a uno.** Compilá seguido: diez errores juntos asustan; uno
   solo se arregla en un minuto.
5. **Probá con la entrada de ejemplo** redirigida (`java Programa.java < entrada.txt`)
   y compará con la salida esperada.

#### Un método para leer datos válidos
Casi todos los programas del jefe piden números y tienen que aguantar respuestas
malas. En lugar de repetir el bucle de validación, se escribe **una vez** en un
método que se reutiliza:
```java
static int leerEntero(Scanner teclado, String pregunta, int min, int max) {
    while (true) {
        System.out.print(pregunta);
        String linea = teclado.nextLine().trim();
        if (linea.matches("-?\\d+")) {
            int valor = Integer.parseInt(linea);
            if (valor >= min && valor <= max) {
                return valor;
            }
        }
        System.out.println("  Tiene que ser un número entre " + min + " y " + max + ".");
    }
}
```
El `Scanner` se crea **una sola vez** en el `main` y se pasa como parámetro: crear
varios `Scanner` sobre `System.in` pierde datos.

#### Arrays paralelos
Sin clases (que vienen en la rama siguiente), para guardar varios datos de cada
viajero se usan **arrays paralelos**: `nombres[i]`, `cargas[i]` y `tasas[i]` son del
mismo viajero `i`. Funciona, pero es incómodo: en la próxima rama vas a ver que una
clase `Viajero` lo resuelve mucho mejor.

### Código de ejemplo

```java
/*
 * Jefe de la rama 1: el libro del Centinela.
 * Registra viajeros hasta "fin", valida los datos, calcula la tasa de cada uno
 * y muestra un informe ordenado con el total.
 */
import java.util.Locale;
import java.util.Scanner;

public class LibroCentinela {
    static final int MAX_VIAJEROS = 10;

    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Scanner teclado = new Scanner(System.in);

        String[] nombres = new String[MAX_VIAJEROS];
        int[] cargas = new int[MAX_VIAJEROS];
        double[] tasas = new double[MAX_VIAJEROS];
        int cantidad = 0;

        while (cantidad < MAX_VIAJEROS) {
            System.out.print("Nombre (o fin): ");
            String nombre = teclado.nextLine().trim();
            if (nombre.equalsIgnoreCase("fin")) {
                break;
            }
            if (nombre.isEmpty()) {
                System.out.println("  El nombre no puede estar vacío.");
                continue;
            }
            int carga = leerEntero(teclado, "Carga en kg: ", 0, 1000);
            boolean armas = leerSiNo(teclado, "¿Trae armas? (s/n): ");
            nombres[cantidad] = nombre;
            cargas[cantidad] = carga;
            tasas[cantidad] = calcularTasa(carga, armas);
            cantidad++;
        }

        ordenarPorTasa(nombres, cargas, tasas, cantidad);
        mostrarInforme(nombres, cargas, tasas, cantidad);
    }

    static int leerEntero(Scanner teclado, String pregunta, int min, int max) {
        while (true) {
            System.out.print(pregunta);
            String linea = teclado.nextLine().trim();
            if (linea.matches("-?\\d+")) {
                int valor = Integer.parseInt(linea);
                if (valor >= min && valor <= max) {
                    return valor;
                }
            }
            System.out.println("  Tiene que ser un número entre " + min + " y " + max + ".");
        }
    }

    static boolean leerSiNo(Scanner teclado, String pregunta) {
        while (true) {
            System.out.print(pregunta);
            String linea = teclado.nextLine().trim().toLowerCase();
            if (linea.equals("s") || linea.equals("n")) {
                return linea.equals("s");
            }
            System.out.println("  Respondé s o n.");
        }
    }

    static double calcularTasa(int carga, boolean armas) {
        double tasa;
        if (carga <= 50) {
            tasa = 5;
        } else if (carga <= 200) {
            tasa = 5 + (carga - 50) * 0.1;
        } else {
            tasa = 20 + (carga - 200) * 0.25;
        }
        return armas ? tasa * 1.5 : tasa;
    }

    // Ordena de mayor a menor tasa, moviendo juntos los tres arrays (burbuja).
    static void ordenarPorTasa(String[] nombres, int[] cargas, double[] tasas, int n) {
        for (int pasada = 0; pasada < n - 1; pasada++) {
            for (int i = 0; i < n - 1 - pasada; i++) {
                if (tasas[i] < tasas[i + 1]) {
                    String n1 = nombres[i];
                    nombres[i] = nombres[i + 1];
                    nombres[i + 1] = n1;
                    int c1 = cargas[i];
                    cargas[i] = cargas[i + 1];
                    cargas[i + 1] = c1;
                    double t1 = tasas[i];
                    tasas[i] = tasas[i + 1];
                    tasas[i + 1] = t1;
                }
            }
        }
    }

    static void mostrarInforme(String[] nombres, int[] cargas, double[] tasas, int n) {
        System.out.println();
        System.out.println("=== Libro del Centinela ===");
        double total = 0;
        for (int i = 0; i < n; i++) {
            System.out.printf("%-12s %5d kg %8.2f%n", nombres[i], cargas[i], tasas[i]);
            total += tasas[i];
        }
        System.out.printf("%d viajeros, total recaudado: %.2f denarios%n", n, total);
    }
}
```

### Entrada de ejemplo

```
Kira
30
n
Bron
300
s

Olmo
mucha
120
n
fin
```

### Salida esperada

```
Nombre (o fin): Carga en kg: ¿Trae armas? (s/n): Nombre (o fin): Carga en kg: ¿Trae armas? (s/n): Nombre (o fin):   El nombre no puede estar vacío.
Nombre (o fin): Carga en kg:   Tiene que ser un número entre 0 y 1000.
Carga en kg: ¿Trae armas? (s/n): Nombre (o fin): 
=== Libro del Centinela ===
Bron           300 kg    67.50
Olmo           120 kg    12.00
Kira            30 kg     5.00
3 viajeros, total recaudado: 84.50 denarios
```

### ¿Para qué sirve?

Así se escribe cualquier programa de verdad: un sistema de turnos, una caja registradora o una planilla de notas empiezan igual, con datos que entran, reglas que se aplican y un informe que sale. La costumbre de partir en métodos y probar cada pieza es la que vas a usar en todo el resto del curso.

### Errores habituales

**Dragón: escribir todo el `main` de un tirón.** Cuando algo falla, no sabés dónde.
Partí en métodos y probá cada uno.

**Ogro: crear un `Scanner` en cada método.** Varios `Scanner` sobre `System.in` se
roban los datos entre sí. Creá uno en el `main` y pasalo como parámetro.

**Orco: el array lleno.** Si cargás más elementos que el tamaño del array, corta con
`ArrayIndexOutOfBoundsException`. Llevá la cuenta y frená al llegar al máximo.

**Ogro: arrays paralelos desordenados.** Si ordenás un array y no los otros, los
datos quedan mezclados entre viajeros. Se mueven siempre juntos.

### Micro-misión R01-N09-P1 · La primera pregunta del Centinela

```meta
lugar: El trono del Centinela
personajes: Zed, Gheco, Nadia, Kaffa, el Centinela
carta: Leer un dato válido | static int leerEntero(Scanner sc, int min, int max) · repite hasta que esté en el rango · un solo Scanner, pasado como parámetro
recompensa: xp 20, oro 20
```

#### Escena
La armadura levanta la cabeza. Su voz suena a hierro: —**Cuántos días te quedás en el Imperio.** Entre 1 y 30. —Zed contesta «0», por probar. Después «45». La armadura no se mueve: vuelve a preguntar.
Kaffa aparece a su lado, con una taza de café. —No se lo engaña, Zed. Se lo vence con **orden**: un librito para cada cosa. Empezá por uno que lea un número válido.

#### Gheco sugiere
Un método `leerEntero(sc, min, max)` encierra el bucle de validación: pregunta, lee y repite **mientras** el número esté fuera del rango (`n < min || n > max`). Así se escribe una vez y se usa en todo el programa.

#### Desafío
Completá la condición del `while`: se repite mientras el número esté fuera del rango.

#### Código inicial
```java
import java.util.Scanner;

public class Centinela {
    static int leerEntero(Scanner sc, int min, int max) {
        System.out.println("Entre " + min + " y " + max + ":");
        int n = sc.nextInt();
        while (___) {
            System.out.println("Fuera de rango. Otra vez:");
            n = sc.nextInt();
        }
        return n;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int dias = leerEntero(sc, 1, 30);
        System.out.println("Registrado: " + dias + " días");
    }
}
```

#### Entrada
```
0
45
12
```

#### Salida esperada
```
Entre 1 y 30:
Fuera de rango. Otra vez:
Fuera de rango. Otra vez:
Registrado: 12 días
```

#### Solución
```java
import java.util.Scanner;

public class Centinela {
    static int leerEntero(Scanner sc, int min, int max) {
        System.out.println("Entre " + min + " y " + max + ":");
        int n = sc.nextInt();
        while (n < min || n > max) {
            System.out.println("Fuera de rango. Otra vez:");
            n = sc.nextInt();
        }
        return n;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int dias = leerEntero(sc, 1, 30);
        System.out.println("Registrado: " + dias + " días");
    }
}
```

#### Al superarla
«Doce días.» La armadura escribe en su libro, con una pluma que se mueve sola. Primera pregunta, superada. El libro pasa la página.

#### Imagen
- El Centinela: una armadura vacía de piedra y bronce sentada en un trono, con ojos de luz azul y un libro de registros abierto.
- Zed frente al trono; Kaffa a su lado con una taza de café; Nadia y Gheco atrás.

### Micro-misión R01-N09-P2 · Los registros del Centinela

```meta
lugar: El trono del Centinela
personajes: Zed, Gheco, Nadia, el Centinela
carta: Métodos con arrays | static double promedio(int[] datos) · el array entra por parámetro · recorrer, acumular y dividir
recompensa: xp 20, oro 20
```

#### Escena
—**Cuánto pesó, en promedio, lo que entró esta semana** —pregunta el Centinela, y del libro caen siete números. Zed empieza a sumar con los dedos. Nadia lo frena: —Un librito. Que reciba los pesos y devuelva el promedio.

#### Gheco sugiere
Un método puede recibir un **array**: `static double promedio(int[] datos)`. Adentro, recorrelo con un acumulador y devolvé `total / (double) datos.length` (el `(double)` evita que la división sea entera).

#### Desafío
Completá el `return`: el total dividido por la cantidad, con decimales.

#### Código inicial
```java
import java.util.Locale;

public class Registros {
    static double promedio(int[] datos) {
        int total = 0;
        for (int dato : datos) {
            total += dato;
        }
        return ___;
    }

    public static void main(String[] args) {
        int[] semana = {120, 80, 95, 60, 130, 75, 110};
        System.out.printf(Locale.US, "Promedio: %.2f kg%n", promedio(semana));
    }
}
```

#### Salida esperada
```
Promedio: 95.71 kg
```

#### Solución
```java
import java.util.Locale;

public class Registros {
    static double promedio(int[] datos) {
        int total = 0;
        for (int dato : datos) {
            total += dato;
        }
        return total / (double) datos.length;
    }

    public static void main(String[] args) {
        int[] semana = {120, 80, 95, 60, 130, 75, 110};
        System.out.printf(Locale.US, "Promedio: %.2f kg%n", promedio(semana));
    }
}
```

#### Al superarla
«95.71 kilos.» El Centinela lo comprueba en su libro. Exacto, con dos decimales. Una placa de su armadura se apaga.

#### Imagen
- Siete números de luz cayendo de un libro abierto y acomodándose en una fila.
- Una placa de la armadura del Centinela que se apaga; Zed concentrado.

### Micro-misión R01-N09-P3 · El veredicto

```meta
lugar: El trono del Centinela
personajes: Zed, Gheco, Nadia, el Centinela
carta: Partir el problema | un método por tarea · main solo los junta · arrays paralelos: el mismo índice en dos arrays es el mismo viajero
recompensa: xp 20, oro 25
```

#### Escena
—**Decidí por mí** —dice el Centinela, y le muestra la fila de viajeros de hoy: sus nombres en un registro y lo que cargan en otro—. Más de 100 kg, inspección. Si no, pasa.
Zed entiende el truco: el mismo número de renglón en los dos registros es el mismo viajero.

#### Gheco sugiere
Con **arrays paralelos**, `nombres[i]` y `cargas[i]` son del mismo viajero. El veredicto va en su propio método; en el bucle de `main`, solo hay que **llamarlo** con la carga de ese viajero: `veredicto(cargas[i])`.

#### Desafío
Completá la llamada al método `veredicto` con la carga del viajero `i`.

#### Código inicial
```java
public class Veredicto {
    static String veredicto(int kg) {
        if (kg > 100) {
            return "inspección";
        }
        return "pasa";
    }

    public static void main(String[] args) {
        String[] nombres = {"Baldo", "un tahúr", "la cocinera", "un soldado"};
        int[] cargas = {140, 20, 60, 101};
        for (int i = 0; i < nombres.length; i++) {
            System.out.println(nombres[i] + ": " + ___);
        }
    }
}
```

#### Salida esperada
```
Baldo: inspección
un tahúr: pasa
la cocinera: pasa
un soldado: inspección
```

#### Solución
```java
public class Veredicto {
    static String veredicto(int kg) {
        if (kg > 100) {
            return "inspección";
        }
        return "pasa";
    }

    public static void main(String[] args) {
        String[] nombres = {"Baldo", "un tahúr", "la cocinera", "un soldado"};
        int[] cargas = {140, 20, 60, 101};
        for (int i = 0; i < nombres.length; i++) {
            System.out.println(nombres[i] + ": " + veredicto(cargas[i]));
        }
    }
}
```

#### Al superarla
Baldo, a inspección (como siempre). El soldado, por un kilo. El Centinela cierra el libro despacio. Queda una sola pregunta, y es sobre Zed.

#### Imagen
- Dos registros abiertos lado a lado, unidos renglón por renglón con hilos de luz.
- Baldo, el mercader ambulante, resignado frente al cartel de «inspección».

### Micro-misión R01-N09-P4 · El Sello de Entrada

```meta
lugar: El trono del Centinela
personajes: Zed, Gheco, Nadia, Kaffa, el Centinela
carta: Un programa entero | leer, decidir, repetir y resumir · cada parte en su método · main cuenta la historia
recompensa: xp 25, oro 30
item: Sello de Entrada
```

#### Escena
—**Declarate** —dice el Centinela—. Todo lo que traés. Uno por uno. Y decime cuánto es.
Zed abre la bolsa. Hace una semana se hubiera guardado algo. Esta vez saca todo: la ganzúa, la capa, la llave de vidrio.

#### Gheco sugiere
Un programa completo se arma con los libritos que ya tenés: uno lee la cantidad, el bucle lee cada cosa y un acumulador suma el valor. `sc.next()` lee una palabra y `sc.nextInt()` un número.

#### Desafío
Completá el acumulador: sumá el valor de cada cosa al total.

#### Código inicial
```java
import java.util.Scanner;

public class Declaracion {
    static String resumen(int cosas, int total) {
        return cosas + " cosas declaradas, valor total " + total + " denarios";
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int cantidad = sc.nextInt();
        int total = 0;
        for (int i = 1; i <= cantidad; i++) {
            String cosa = sc.next();
            int valor = sc.nextInt();
            System.out.println(i + ". " + cosa + ": " + valor);
            ___;
        }
        System.out.println(resumen(cantidad, total));
    }
}
```

#### Entrada
```
3
ganzua 15
capa 40
llave 0
```

#### Salida esperada
```
1. ganzua: 15
2. capa: 40
3. llave: 0
3 cosas declaradas, valor total 55 denarios
```

#### Solución
```java
import java.util.Scanner;

public class Declaracion {
    static String resumen(int cosas, int total) {
        return cosas + " cosas declaradas, valor total " + total + " denarios";
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int cantidad = sc.nextInt();
        int total = 0;
        for (int i = 1; i <= cantidad; i++) {
            String cosa = sc.next();
            int valor = sc.nextInt();
            System.out.println(i + ". " + cosa + ": " + valor);
            total += valor;
        }
        System.out.println(resumen(cantidad, total));
    }
}
```

#### Al superarla
«Llave: 0 denarios.» El Centinela se queda mirando ese renglón mucho tiempo. Después se levanta, se hace a un lado y le entrega a Zed un sello de bronce: el **Sello de Entrada**. Ya no es un colado: está declarado.
Esa noche, la ganzúa de Zed amanece un poco distinta, como si quisiera ser otra cosa. Kaffa termina su café. —Ahora aprendé a hacer **moldes**.

#### Imagen
- El Centinela de pie, haciéndose a un lado del trono, entregándole a Zed un sello de bronce que brilla.
- Sobre una mesa, lo que Zed declaró: una ganzúa, una capa gastada y la llave de plomo y vidrios de colores.
- Kaffa con su taza de café; Nadia sonriendo apenas, por primera vez.

### Misión R01-N09-M1 · El duelo con el Centinela

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Escribí el duelo por turnos contra el Centinela. Kira empieza con 40 de vida y 3
pociones; el Centinela, con 60 de vida. Primero se pide la semilla del azar. En cada
turno se muestra el estado y se pide una acción, validada con un método:

1. **Atacar**: Kira hace entre 8 y 14 de daño (`random.nextInt(7) + 8`).
2. **Curarse**: si le quedan pociones, recupera 15 de vida (sin pasar de 40); si no,
   pierde el turno.
3. **Defender**: ese turno el Centinela le hace la mitad del daño.

Después de la acción de Kira, si el Centinela sigue en pie, ataca con entre 5 y 12
de daño (`random.nextInt(8) + 5`). El duelo termina cuando alguno queda en 0 o menos.
Mostrá quién ganó y en cuántos turnos.

#### Criterio de aprobación

- Usa un `Random` con la semilla leída, creado una sola vez.
- La acción se lee con un método que valida (1 a 3).
- Separa en métodos al menos: leer la acción, el turno de Kira y el ataque del Centinela.
- La salida coincide con la esperada.

#### Entrada de ejemplo

```
2026
1
1
3
2
1
1
1
1
1
```

#### Salida esperada

```
Semilla: 
Turno 1 | Kira 40 (pociones: 3) | Centinela 60
1 Atacar, 2 Curarse, 3 Defender: Kira ataca: 8 de daño
El Centinela golpea: 6 de daño

Turno 2 | Kira 34 (pociones: 3) | Centinela 52
1 Atacar, 2 Curarse, 3 Defender: Kira ataca: 14 de daño
El Centinela golpea: 6 de daño

Turno 3 | Kira 28 (pociones: 3) | Centinela 38
1 Atacar, 2 Curarse, 3 Defender: Kira se defiende
El Centinela golpea: 5 de daño

Turno 4 | Kira 23 (pociones: 3) | Centinela 38
1 Atacar, 2 Curarse, 3 Defender: Kira se cura 15
El Centinela golpea: 6 de daño

Turno 5 | Kira 32 (pociones: 2) | Centinela 38
1 Atacar, 2 Curarse, 3 Defender: Kira ataca: 11 de daño
El Centinela golpea: 9 de daño

Turno 6 | Kira 23 (pociones: 2) | Centinela 27
1 Atacar, 2 Curarse, 3 Defender: Kira ataca: 14 de daño
El Centinela golpea: 5 de daño

Turno 7 | Kira 18 (pociones: 2) | Centinela 13
1 Atacar, 2 Curarse, 3 Defender: Kira ataca: 11 de daño
El Centinela golpea: 11 de daño

Turno 8 | Kira 7 (pociones: 2) | Centinela 2
1 Atacar, 2 Curarse, 3 Defender: Kira ataca: 14 de daño

¡El Centinela cae en el turno 8! Kira queda con 7 de vida.
```

#### Solución de referencia

```java
// Jefe R01 - Mision 1: el duelo con el Centinela.
import java.util.Random;
import java.util.Scanner;

public class DueloCentinela {
    static final int VIDA_MAX = 40;

    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        System.out.print("Semilla: ");
        Random random = new Random(Long.parseLong(teclado.nextLine().trim()));

        int vidaKira = VIDA_MAX;
        int pociones = 3;
        int vidaCentinela = 60;
        int turno = 0;

        while (vidaKira > 0 && vidaCentinela > 0) {
            turno++;
            System.out.println();
            System.out.println("Turno " + turno + " | Kira " + vidaKira + " (pociones: " + pociones + ") | Centinela " + vidaCentinela);
            int accion = leerAccion(teclado);
            boolean defiende = accion == 3;

            if (accion == 1) {
                int danio = random.nextInt(7) + 8;
                vidaCentinela -= danio;
                System.out.println("Kira ataca: " + danio + " de daño");
            } else if (accion == 2) {
                if (pociones > 0) {
                    pociones--;
                    int antes = vidaKira;
                    vidaKira = Math.min(VIDA_MAX, vidaKira + 15);
                    System.out.println("Kira se cura " + (vidaKira - antes));
                } else {
                    System.out.println("No quedan pociones: Kira pierde el turno");
                }
            } else {
                System.out.println("Kira se defiende");
            }

            if (vidaCentinela > 0) {
                vidaKira -= ataqueCentinela(random, defiende);
            }
        }

        System.out.println();
        if (vidaCentinela <= 0) {
            System.out.println("¡El Centinela cae en el turno " + turno + "! Kira queda con " + vidaKira + " de vida.");
        } else {
            System.out.println("Kira cae en el turno " + turno + ". El Centinela queda con " + vidaCentinela + ".");
        }
    }

    static int leerAccion(Scanner teclado) {
        while (true) {
            System.out.print("1 Atacar, 2 Curarse, 3 Defender: ");
            String linea = teclado.nextLine().trim();
            if (linea.equals("1") || linea.equals("2") || linea.equals("3")) {
                return Integer.parseInt(linea);
            }
            System.out.println("  Elegí 1, 2 o 3.");
        }
    }

    static int ataqueCentinela(Random random, boolean defiende) {
        int danio = random.nextInt(8) + 5;
        if (defiende) {
            danio = danio / 2;
        }
        System.out.println("El Centinela golpea: " + danio + " de daño");
        return danio;
    }
}
```

#### Pruebas

##### Cura siempre
```entrada
5
2
2
2
2
1
1
1
1
1
1
1
1
1
1
```
```salida
Semilla:
Turno 1 | Kira 40 (pociones: 3) | Centinela 60
1 Atacar, 2 Curarse, 3 Defender: Kira se cura 0
El Centinela golpea: 10 de daño

Turno 2 | Kira 30 (pociones: 2) | Centinela 60
1 Atacar, 2 Curarse, 3 Defender: Kira se cura 10
El Centinela golpea: 6 de daño

Turno 3 | Kira 34 (pociones: 1) | Centinela 60
1 Atacar, 2 Curarse, 3 Defender: Kira se cura 6
El Centinela golpea: 5 de daño

Turno 4 | Kira 35 (pociones: 0) | Centinela 60
1 Atacar, 2 Curarse, 3 Defender: No quedan pociones: Kira pierde el turno
El Centinela golpea: 9 de daño

Turno 5 | Kira 26 (pociones: 0) | Centinela 60
1 Atacar, 2 Curarse, 3 Defender: Kira ataca: 12 de daño
El Centinela golpea: 12 de daño

Turno 6 | Kira 14 (pociones: 0) | Centinela 48
1 Atacar, 2 Curarse, 3 Defender: Kira ataca: 9 de daño
El Centinela golpea: 11 de daño

Turno 7 | Kira 3 (pociones: 0) | Centinela 39
1 Atacar, 2 Curarse, 3 Defender: Kira ataca: 13 de daño
El Centinela golpea: 8 de daño

Kira cae en el turno 7. El Centinela queda con 26.
```

##### Defiende siempre
```entrada
99
3
3
3
3
3
3
3
3
3
3
3
3
3
3
3
```
```salida
Semilla:
Turno 1 | Kira 40 (pociones: 3) | Centinela 60
1 Atacar, 2 Curarse, 3 Defender: Kira se defiende
El Centinela golpea: 5 de daño

Turno 2 | Kira 35 (pociones: 3) | Centinela 60
1 Atacar, 2 Curarse, 3 Defender: Kira se defiende
El Centinela golpea: 4 de daño

Turno 3 | Kira 31 (pociones: 3) | Centinela 60
1 Atacar, 2 Curarse, 3 Defender: Kira se defiende
El Centinela golpea: 3 de daño

Turno 4 | Kira 28 (pociones: 3) | Centinela 60
1 Atacar, 2 Curarse, 3 Defender: Kira se defiende
El Centinela golpea: 5 de daño

Turno 5 | Kira 23 (pociones: 3) | Centinela 60
1 Atacar, 2 Curarse, 3 Defender: Kira se defiende
El Centinela golpea: 5 de daño

Turno 6 | Kira 18 (pociones: 3) | Centinela 60
1 Atacar, 2 Curarse, 3 Defender: Kira se defiende
El Centinela golpea: 4 de daño

Turno 7 | Kira 14 (pociones: 3) | Centinela 60
1 Atacar, 2 Curarse, 3 Defender: Kira se defiende
El Centinela golpea: 5 de daño

Turno 8 | Kira 9 (pociones: 3) | Centinela 60
1 Atacar, 2 Curarse, 3 Defender: Kira se defiende
El Centinela golpea: 4 de daño

Turno 9 | Kira 5 (pociones: 3) | Centinela 60
1 Atacar, 2 Curarse, 3 Defender: Kira se defiende
El Centinela golpea: 5 de daño

Kira cae en el turno 9. El Centinela queda con 60.
```

### Misión R01-N09-M2 · Los registros del Centinela

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

El Centinela guarda sus registros en líneas con el formato `nombre;edad;oro`. Leé
líneas hasta una vacía (como máximo 20). Para cada una, con un método
`validarRegistro` que devuelve un mensaje de error o `""` si está bien, descartá las
que no tengan tres partes, tengan la edad fuera de 0 a 120 o el oro negativo (mostrá
por qué). Con los registros válidos, guardados en arrays paralelos, mostrá:

1. Una tabla con nombre, edad y oro (alineada con `printf`).
2. El promedio de edad (un decimal) y el oro total.
3. El nombre del más rico.
4. Cuántos son menores de 18.

#### Criterio de aprobación

- La validación está en un método.
- Usa `split(";")` y arrays paralelos.
- Las líneas inválidas se informan y no se cuentan.

#### Entrada de ejemplo

```
Kira;19;120
Bron;45;-3
Olmo;veinte;10
Lía;16;35
Tesla;33;980
Pip;12

```

#### Salida esperada

```
Descartado [Bron;45;-3]: el oro no puede ser negativo
Descartado [Olmo;veinte;10]: la edad no es un número
Descartado [Pip;12]: tiene que tener nombre;edad;oro

Nombre    Edad    Oro
Kira        19    120
Lía         16     35
Tesla       33    980
Promedio de edad: 22.7
Oro total: 1135
El más rico: Tesla
Menores de 18: 1
```

#### Solución de referencia

```java
// Jefe R01 - Mision 2: los registros del Centinela.
import java.util.Locale;
import java.util.Scanner;

public class RegistrosCentinela {
    static final int MAX = 20;

    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Scanner teclado = new Scanner(System.in);
        String[] nombres = new String[MAX];
        int[] edades = new int[MAX];
        int[] oros = new int[MAX];
        int n = 0;

        while (n < MAX && teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.isEmpty()) {
                break;
            }
            String error = validarRegistro(linea);
            if (!error.isEmpty()) {
                System.out.println("Descartado [" + linea + "]: " + error);
                continue;
            }
            String[] partes = linea.split(";");
            nombres[n] = partes[0];
            edades[n] = Integer.parseInt(partes[1]);
            oros[n] = Integer.parseInt(partes[2]);
            n++;
        }

        System.out.println();
        System.out.printf("%-8s %5s %6s%n", "Nombre", "Edad", "Oro");
        for (int i = 0; i < n; i++) {
            System.out.printf("%-8s %5d %6d%n", nombres[i], edades[i], oros[i]);
        }
        System.out.printf("Promedio de edad: %.1f%n", promedio(edades, n));
        System.out.println("Oro total: " + suma(oros, n));
        System.out.println("El más rico: " + nombres[indiceDelMayor(oros, n)]);
        System.out.println("Menores de 18: " + contarMenores(edades, n, 18));
    }

    static String validarRegistro(String linea) {
        String[] partes = linea.split(";");
        if (partes.length != 3) {
            return "tiene que tener nombre;edad;oro";
        }
        if (!partes[1].matches("\\d+")) {
            return "la edad no es un número";
        }
        if (!partes[2].matches("-?\\d+")) {
            return "el oro no es un número";
        }
        int edad = Integer.parseInt(partes[1]);
        if (edad > 120) {
            return "edad fuera de rango";
        }
        if (Integer.parseInt(partes[2]) < 0) {
            return "el oro no puede ser negativo";
        }
        return "";
    }

    static double promedio(int[] datos, int n) {
        return n == 0 ? 0 : (double) suma(datos, n) / n;
    }

    static int suma(int[] datos, int n) {
        int total = 0;
        for (int i = 0; i < n; i++) {
            total += datos[i];
        }
        return total;
    }

    static int indiceDelMayor(int[] datos, int n) {
        int mejor = 0;
        for (int i = 1; i < n; i++) {
            if (datos[i] > datos[mejor]) {
                mejor = i;
            }
        }
        return mejor;
    }

    static int contarMenores(int[] edades, int n, int limite) {
        int cantidad = 0;
        for (int i = 0; i < n; i++) {
            if (edades[i] < limite) {
                cantidad++;
            }
        }
        return cantidad;
    }
}
```

#### Pruebas

##### Todos válidos
```entrada
Ana;30;10
Beto;17;0
```
```salida
Nombre    Edad    Oro
Ana         30     10
Beto        17      0
Promedio de edad: 23.5
Oro total: 10
El más rico: Ana
Menores de 18: 1
```

##### Bordes de edad
```entrada
Uno;0;1
Dos;120;1
Tres;121;1
Cuatro;-1;1
```
```salida
Descartado [Tres;121;1]: edad fuera de rango
Descartado [Cuatro;-1;1]: la edad no es un número

Nombre    Edad    Oro
Uno          0      1
Dos        120      1
Promedio de edad: 60.0
Oro total: 2
El más rico: Uno
Menores de 18: 1
```

##### Ninguno válido
```entrada
a;b;c
x
```
```salida
Descartado [a;b;c]: la edad no es un número
Descartado [x]: tiene que tener nombre;edad;oro

Nombre    Edad    Oro
Promedio de edad: 0.0
Oro total: 0
El más rico: null
Menores de 18: 0
```

### Encargo R01-N09-E1 · El cajero automático

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 30
```

#### Consigna

Programá un cajero automático de consola. La cuenta empieza con 50 000 pesos y el
PIN es `4321`: el cajero pide el PIN y da **3 intentos**. Si entra, muestra un menú
hasta que se elija salir: 1 consultar saldo, 2 depositar, 3 extraer (no puede
dejar el saldo negativo ni extraer más de 30 000 por operación), 4 ver los últimos
movimientos (guardá hasta 10 en un array) y 5 salir. Cada operación en su método.

#### Criterio de aprobación

- El PIN se compara con `equals` y hay 3 intentos.
- El menú se repite con un bucle hasta la opción 5.
- Las extracciones respetan las dos reglas.
- Guarda los movimientos en un array.

#### Entrada de ejemplo

```
1111
4321
2
15000
3
40000
3
20000
1
4
5
```

#### Salida esperada

```
PIN: PIN incorrecto (2 intentos restantes)
PIN: Acceso correcto.

1 Saldo | 2 Depositar | 3 Extraer | 4 Movimientos | 5 Salir
Opción: Monto a depositar: Depositaste $15000

1 Saldo | 2 Depositar | 3 Extraer | 4 Movimientos | 5 Salir
Opción: Monto a extraer: El máximo por extracción es $30000

1 Saldo | 2 Depositar | 3 Extraer | 4 Movimientos | 5 Salir
Opción: Monto a extraer: Retirá $20000

1 Saldo | 2 Depositar | 3 Extraer | 4 Movimientos | 5 Salir
Opción: Saldo: $45000

1 Saldo | 2 Depositar | 3 Extraer | 4 Movimientos | 5 Salir
Opción:   Depósito +15000
  Extracción -20000

1 Saldo | 2 Depositar | 3 Extraer | 4 Movimientos | 5 Salir
Opción: Gracias por usar el cajero.
```

#### Solución de referencia

```java
// Jefe R01 - Encargo: el cajero automatico.
import java.util.Scanner;

public class Cajero {
    static final String PIN = "4321";
    static final int LIMITE_EXTRACCION = 30_000;
    static String[] movimientos = new String[10];
    static int cantMovimientos = 0;

    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        if (!login(teclado)) {
            System.out.println("Tarjeta retenida.");
            return;
        }
        int saldo = 50_000;
        int opcion;
        do {
            System.out.println();
            System.out.println("1 Saldo | 2 Depositar | 3 Extraer | 4 Movimientos | 5 Salir");
            opcion = leerEntero(teclado, "Opción: ");
            switch (opcion) {
                case 1 -> System.out.println("Saldo: $" + saldo);
                case 2 -> saldo = depositar(teclado, saldo);
                case 3 -> saldo = extraer(teclado, saldo);
                case 4 -> mostrarMovimientos();
                case 5 -> System.out.println("Gracias por usar el cajero.");
                default -> System.out.println("Opción inválida.");
            }
        } while (opcion != 5);
    }

    static boolean login(Scanner teclado) {
        for (int intento = 1; intento <= 3; intento++) {
            System.out.print("PIN: ");
            if (teclado.nextLine().trim().equals(PIN)) {
                System.out.println("Acceso correcto.");
                return true;
            }
            System.out.println("PIN incorrecto (" + (3 - intento) + " intentos restantes)");
        }
        return false;
    }

    static int leerEntero(Scanner teclado, String pregunta) {
        while (true) {
            System.out.print(pregunta);
            String linea = teclado.nextLine().trim();
            if (linea.matches("\\d+")) {
                return Integer.parseInt(linea);
            }
            System.out.println("  Ingresá un número.");
        }
    }

    static int depositar(Scanner teclado, int saldo) {
        int monto = leerEntero(teclado, "Monto a depositar: ");
        registrar("Depósito +" + monto);
        System.out.println("Depositaste $" + monto);
        return saldo + monto;
    }

    static int extraer(Scanner teclado, int saldo) {
        int monto = leerEntero(teclado, "Monto a extraer: ");
        if (monto > LIMITE_EXTRACCION) {
            System.out.println("El máximo por extracción es $" + LIMITE_EXTRACCION);
            return saldo;
        }
        if (monto > saldo) {
            System.out.println("Saldo insuficiente");
            return saldo;
        }
        registrar("Extracción -" + monto);
        System.out.println("Retirá $" + monto);
        return saldo - monto;
    }

    static void registrar(String movimiento) {
        if (cantMovimientos == movimientos.length) {
            for (int i = 1; i < movimientos.length; i++) {
                movimientos[i - 1] = movimientos[i];
            }
            cantMovimientos--;
        }
        movimientos[cantMovimientos] = movimiento;
        cantMovimientos++;
    }

    static void mostrarMovimientos() {
        if (cantMovimientos == 0) {
            System.out.println("Sin movimientos.");
        }
        for (int i = 0; i < cantMovimientos; i++) {
            System.out.println("  " + movimientos[i]);
        }
    }
}
```

#### Pruebas

##### Tres PIN incorrectos
```entrada
1
2
3
```
```salida
PIN: PIN incorrecto (2 intentos restantes)
PIN: PIN incorrecto (1 intentos restantes)
PIN: PIN incorrecto (0 intentos restantes)
Tarjeta retenida.
```

##### Depositar y ver movimientos
```entrada
4321
2
1000
2
2000
4
1
5
```
```salida
PIN: Acceso correcto.

1 Saldo | 2 Depositar | 3 Extraer | 4 Movimientos | 5 Salir
Opción: Monto a depositar: Depositaste $1000

1 Saldo | 2 Depositar | 3 Extraer | 4 Movimientos | 5 Salir
Opción: Monto a depositar: Depositaste $2000

1 Saldo | 2 Depositar | 3 Extraer | 4 Movimientos | 5 Salir
Opción:   Depósito +1000
  Depósito +2000

1 Saldo | 2 Depositar | 3 Extraer | 4 Movimientos | 5 Salir
Opción: Saldo: $53000

1 Saldo | 2 Depositar | 3 Extraer | 4 Movimientos | 5 Salir
Opción: Gracias por usar el cajero.
```

##### Extraer justo 30000
```entrada
4321
3
30000
3
30001
1
5
```
```salida
PIN: Acceso correcto.

1 Saldo | 2 Depositar | 3 Extraer | 4 Movimientos | 5 Salir
Opción: Monto a extraer: Retirá $30000

1 Saldo | 2 Depositar | 3 Extraer | 4 Movimientos | 5 Salir
Opción: Monto a extraer: El máximo por extracción es $30000

1 Saldo | 2 Depositar | 3 Extraer | 4 Movimientos | 5 Salir
Opción: Saldo: $20000

1 Saldo | 2 Depositar | 3 Extraer | 4 Movimientos | 5 Salir
Opción: Gracias por usar el cajero.
```

### Prueba del sello

#### ¿Por qué conviene un método `leerEntero` en vez de repetir el bucle de validación?

Porque la lógica se escribe y se prueba una vez, y si cambia (por ejemplo, el mensaje), se cambia en un solo lugar.

#### ¿Por qué se crea un solo `Scanner` y se pasa como parámetro?

Porque varios `Scanner` sobre `System.in` pueden quedarse con datos que le correspondían a otro.

#### ¿Qué son los arrays paralelos y cuál es su problema?

Varios arrays donde la misma posición corresponde al mismo elemento (`nombres[i]`, `edades[i]`). Hay que mover todos juntos al ordenar o borrar; las clases lo resuelven mejor.

#### ¿Cómo probás un programa que pide muchos datos sin tipearlos cada vez?

Guardando la entrada en un archivo y redirigiéndola: `java Programa.java < entrada.txt`.

### Soluciones (docente)

Jefe nuevo, integrador de la rama (el capítulo 18 no tenía uno para el bloque 1). Las entradas del duelo están armadas con la semilla 2026 para que se vean las tres acciones y la victoria de Kira; si se cambia la entrada, regenerar la salida esperada.
