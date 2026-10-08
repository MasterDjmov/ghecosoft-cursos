# RAMA R04 · Las Corrientes del Imperio: Java moderno, patrones y concurrencia

```meta
tipo: tronco
posicion: 4
```

## R04-N01 · Streams: datos que fluyen

```meta
tipo: tema
padre: R03-N08
criatura: slime
temas: func.streams
usa: func.lambdas
precio: 10
```

### Crónica

Desde las ventanas de los Archivos se oye el **río que cruza la capital**. Zed baja a la orilla siguiendo la pista del viajero: algo mandado por el río que nunca llegó. Por el agua bajan miles de barcazas, cada una con un dato, y en la orilla unos molinos las procesan sin detener la corriente: uno deja pasar solo las rojas, otro les cambia la carga, otro las cuenta.

—Hasta ahora recorrías tus listas con bucles, uno por uno, anotando todo a mano —dice {mentor}—. En el Java moderno, los datos **fluyen**: describís **qué** querés (filtrar, transformar, sumar) y el río se encarga del **cómo**. Eso es un *stream*, Zed.

### Objetivos

- Crear streams a partir de colecciones, arrays y rangos.
- Encadenar operaciones intermedias: `filter`, `map`, `sorted`, `distinct`, `limit`.
- Terminar un stream con `toList`, `count`, `forEach`, `anyMatch`, `reduce` y los de números (`sum`, `average`, `max`).
- Entender que un stream es perezoso y se usa una sola vez.

### Antes de empezar

- Lambdas y referencias a métodos (rama 3), `record` y colecciones.

### Explicación

#### Qué es un stream
Un **stream** es una secuencia de datos que se procesa con una **cadena de
operaciones**. No guarda datos: los toma de una fuente (una lista, un array, un rango),
los pasa por las operaciones y produce un resultado.
```java
List<String> nombres = heroes.stream()          // 1. la fuente
        .filter(h -> h.vida() > 20)             // 2. operaciones intermedias
        .map(Heroe::nombre)
        .sorted()
        .toList();                              // 3. una operación terminal
```
Lo mismo con un bucle ocupa diez líneas, una lista auxiliar y un `if`. Con el stream se
lee como la frase: "de los héroes, los que tienen más de 20 de vida, su nombre,
ordenados, en una lista".

#### Crear un stream
```java
lista.stream()                           // de una colección
Arrays.stream(array)                     // de un array
Stream.of("a", "b", "c")                 // de valores sueltos
IntStream.range(0, 10)                   // 0..9 (rangeClosed incluye el 10)
"hola".chars()                           // los caracteres de un texto (como números)
```

#### Operaciones intermedias (devuelven otro stream)
| Operación | Hace |
|---|---|
| `filter(predicado)` | deja pasar los que cumplen |
| `map(función)` | transforma cada elemento |
| `mapToInt(función)` | transforma a `int` (para sumar, promediar) |
| `sorted()` / `sorted(comparador)` | ordena |
| `distinct()` | saca repetidos |
| `limit(n)` / `skip(n)` | los primeros `n` / saltea `n` |
| `peek(acción)` | mira cada elemento sin cambiarlo (para depurar) |

#### Operaciones terminales (producen el resultado)
| Operación | Devuelve |
|---|---|
| `toList()` | una lista (inmutable) |
| `count()` | cuántos hay (`long`) |
| `forEach(acción)` | nada: hace algo con cada uno |
| `anyMatch` / `allMatch` / `noneMatch` | `boolean` |
| `findFirst()` | el primero, en un `Optional` (nodo siguiente) |
| `reduce(inicial, operación)` | combina todos en uno |
| `sum()`, `average()`, `max()`, `min()` | en `IntStream` / `DoubleStream` |

`average()` devuelve un `OptionalDouble` (puede no haber elementos): se lee con
`.orElse(0)`.

#### Perezoso y de un solo uso
Las operaciones intermedias **no hacen nada** hasta que llega una terminal: el stream
es perezoso. Y un stream se consume **una sola vez**: usarlo dos veces lanza
`IllegalStateException: stream has already been operated upon or closed`. Si necesitás
dos resultados, creá dos streams (o guardá una lista).

#### Sin efectos secundarios
Dentro de un `map` o un `filter`, no modifiques variables de afuera ni la lista que
recorrés: el resultado se obtiene de la operación terminal. Si te encontrás sumando en
una variable dentro de un `forEach`, seguramente buscabas `sum()` o `reduce`.

> **Si venís de Python.** Un stream se parece a encadenar `filter`, `map` y
> comprensiones de listas: `[h.nombre for h in heroes if h.vida > 20]`.

### Código de ejemplo

```java
/*
 * Streams: los molinos del Río de las Corrientes.
 */
import java.util.List;
import java.util.stream.IntStream;

public class Corrientes {
    record Heroe(String nombre, String clase, int nivel, int vida) { }

    public static void main(String[] args) {
        List<Heroe> heroes = List.of(
                new Heroe("Kira", "arquera", 7, 30), new Heroe("Bron", "guerrero", 9, 45),
                new Heroe("Lía", "maga", 5, 18), new Heroe("Nara", "paladina", 8, 40),
                new Heroe("Pip", "arquero", 2, 12), new Heroe("Olmo", "mago", 6, 22));

        // filter + map + sorted + toList
        List<String> fuertes = heroes.stream()
                .filter(h -> h.vida() > 20)
                .map(Heroe::nombre)
                .sorted()
                .toList();
        System.out.println("Con más de 20 de vida: " + fuertes);

        // count, anyMatch, allMatch
        long magos = heroes.stream().filter(h -> h.clase().startsWith("mag")).count();
        System.out.println("Magos: " + magos);
        System.out.println("¿Alguno de nivel 9? " + heroes.stream().anyMatch(h -> h.nivel() == 9));
        System.out.println("¿Todos con vida? " + heroes.stream().allMatch(h -> h.vida() > 0));

        // mapToInt + sum / average / max
        int vidaTotal = heroes.stream().mapToInt(Heroe::vida).sum();
        double nivelPromedio = heroes.stream().mapToInt(Heroe::nivel).average().orElse(0);
        int nivelMaximo = heroes.stream().mapToInt(Heroe::nivel).max().orElse(0);
        System.out.println("Vida total: " + vidaTotal + ", nivel promedio: " + nivelPromedio + ", máximo: " + nivelMaximo);

        // sorted con comparador + limit: el podio por nivel
        List<String> podio = heroes.stream()
                .sorted((a, b) -> Integer.compare(b.nivel(), a.nivel()))
                .limit(3)
                .map(h -> h.nombre() + " (" + h.nivel() + ")")
                .toList();
        System.out.println("Podio: " + podio);

        // distinct: las clases sin repetir, en mayúsculas
        List<String> clases = heroes.stream().map(h -> h.clase().replace("arquero", "arquera")).distinct().map(String::toUpperCase).toList();
        System.out.println("Clases: " + clases);

        // reduce: combinar todos en uno
        String iniciales = heroes.stream().map(h -> h.nombre().substring(0, 1)).reduce("", String::concat);
        System.out.println("Iniciales: " + iniciales);

        // IntStream: números sin lista
        int sumaDeCuadrados = IntStream.rangeClosed(1, 10).map(n -> n * n).sum();
        List<Integer> multiplosDe7 = IntStream.range(1, 60).filter(n -> n % 7 == 0).boxed().toList();
        System.out.println("Suma de cuadrados del 1 al 10: " + sumaDeCuadrados);
        System.out.println("Múltiplos de 7 menores a 60: " + multiplosDe7);
    }
}
```

### Salida esperada

```
Con más de 20 de vida: [Bron, Kira, Nara, Olmo]
Magos: 2
¿Alguno de nivel 9? true
¿Todos con vida? true
Vida total: 167, nivel promedio: 6.166666666666667, máximo: 9
Podio: [Bron (9), Nara (8), Kira (7)]
Clases: [ARQUERA, GUERRERO, MAGA, PALADINA, MAGO]
Iniciales: KBLNPO
Suma de cuadrados del 1 al 10: 385
Múltiplos de 7 menores a 60: [7, 14, 21, 28, 35, 42, 49, 56]
```

### ¿Para qué sirve?

Los streams están en todo el Java moderno: filtrar los pedidos de un cliente, calcular el total de una factura, armar un reporte, transformar los datos que llegan de una API. En Spring (la tercera Senda) y en cualquier empresa que use Java 8 o más nuevo, vas a leer y escribir streams todos los días.

### Errores habituales

**Ogro: el stream reutilizado.** Guardar un `Stream` en una variable y usarlo dos
veces: `IllegalStateException: stream has already been operated upon or closed`.

**Ogro: el stream que no hace nada.** `heroes.stream().filter(...).map(...);` sin una
operación terminal no ejecuta nada.

**Troll: modificar afuera desde adentro.** Sumar en una variable externa dentro de un
`forEach` o de un `map` no compila (la variable tiene que ser efectivamente final) o da
resultados raros con streams paralelos. Usá `sum`, `count` o `reduce`.

**Goblin: la lista inmutable.** `toList()` devuelve una lista que no se puede modificar:
`add` lanza `UnsupportedOperationException`. Si la necesitás modificable:
`new ArrayList<>(stream.toList())` o `collect(Collectors.toList())`.

**Esqueleto: `average()` no es un `double`.** Devuelve `OptionalDouble`: hay que usar
`.orElse(0)` o `.getAsDouble()`.

### Micro-misión R04-N01-P1 · El molino que filtra

```meta
lugar: La orilla del río de la capital
personajes: Zed, Gheco, Nadia, Kaffa
carta: filter | lista.stream().filter(b -> b.carga() > 50).toList() · deja pasar solo lo que cumple la condición
recompensa: xp 10, oro 10
```

#### Escena
Por el río bajan barcazas sin parar. En la orilla, un molino deja pasar solo las **cargadas**, sin detener el agua. Zed, que está acostumbrado a recorrer todo con un for, mira el molino un buen rato.

#### Gheco sugiere
Un **stream** es una corriente de datos: `barcazas.stream()`. `filter(b -> condición)` deja pasar solo los que cumplen, y `toList()` junta lo que llegó al final en una lista.

#### Desafío
Completá la condición del filtro: las barcazas con más de 50 de carga.

#### Código inicial
```java
import java.util.List;

public class Molino {
    public static void main(String[] args) {
        List<Barcaza> rio = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20),
                new Barcaza("Bagre", 120), new Barcaza("Junco", 50));
        List<Barcaza> cargadas = rio.stream()
                .filter(b -> ___)
                .toList();
        System.out.println("Pasan el molino: " + cargadas);
    }
}

record Barcaza(String nombre, int carga) {
}
```

#### Salida esperada
```
Pasan el molino: [Barcaza[nombre=Garza, carga=80], Barcaza[nombre=Bagre, carga=120]]
```

#### Solución
```java
import java.util.List;

public class Molino {
    public static void main(String[] args) {
        List<Barcaza> rio = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20),
                new Barcaza("Bagre", 120), new Barcaza("Junco", 50));
        List<Barcaza> cargadas = rio.stream()
                .filter(b -> b.carga() > 50)
                .toList();
        System.out.println("Pasan el molino: " + cargadas);
    }
}

record Barcaza(String nombre, int carga) {
}
```

#### Al superarla
La Garza y el Bagre pasan; el Junco, con 50 justos, se queda. El molino no paró ni un segundo. —Describís **qué** querés —dice Kaffa— y el río se ocupa del cómo.

#### Imagen
- El río de la capital al atardecer, lleno de barcazas; en la orilla, un molino de bronce que desvía solo las barcazas cargadas.
- Zed sentado en la orilla mirando el molino; Kaffa con su taza al lado.

### Micro-misión R04-N01-P2 · El molino que transforma

```meta
lugar: La orilla del río de la capital
personajes: Zed, Gheco, Nadia, Kaffa
carta: map y sorted | .map(Barcaza::nombre) cambia cada elemento por otro · .sorted() los ordena · se encadenan
recompensa: xp 10, oro 10
```

#### Escena
Un segundo molino no filtra: **transforma**. A cada barcaza le saca el nombre y lo pinta en mayúsculas en un cartel, y los carteles salen ordenados.

#### Gheco sugiere
`map(f)` cambia cada elemento por el resultado de `f`: `.map(Barcaza::nombre)` deja solo los nombres. Las operaciones se **encadenan**: `.map(...).map(String::toUpperCase).sorted()`.

#### Desafío
Completá el `map` que pasa cada nombre a mayúsculas.

#### Código inicial
```java
import java.util.List;

public class Carteles {
    public static void main(String[] args) {
        List<Barcaza> rio = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20), new Barcaza("Bagre", 120));
        List<String> carteles = rio.stream()
                .map(Barcaza::nombre)
                .map(___)
                .sorted()
                .toList();
        System.out.println(carteles);
    }
}

record Barcaza(String nombre, int carga) {
}
```

#### Salida esperada
```
[BAGRE, GARZA, SAUCE]
```

#### Solución
```java
import java.util.List;

public class Carteles {
    public static void main(String[] args) {
        List<Barcaza> rio = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20), new Barcaza("Bagre", 120));
        List<String> carteles = rio.stream()
                .map(Barcaza::nombre)
                .map(String::toUpperCase)
                .sorted()
                .toList();
        System.out.println(carteles);
    }
}

record Barcaza(String nombre, int carga) {
}
```

#### Al superarla
BAGRE, GARZA, SAUCE: tres carteles en orden, sin un solo for. Nadia los copia en su libreta y, por primera vez, no corrige nada.

#### Imagen
- Un molino que convierte barcazas en carteles de madera con nombres en mayúsculas.
- Nadia copiando los carteles en su libreta.

### Micro-misión R04-N01-P3 · El que cuenta y suma

```meta
lugar: La orilla del río de la capital
personajes: Zed, Gheco, Nadia, Kaffa
carta: Terminales | count() cuántos · mapToInt(Barcaza::carga).sum() suma · max(), average() · el stream termina ahí
recompensa: xp 15, oro 15
```

#### Escena
El tercer molino solo **cuenta**: cuántas barcazas pasaron hoy y cuánta carga trajeron entre todas. Es el último de la orilla: después de él, la corriente termina en un número.

#### Gheco sugiere
Una operación **terminal** termina el stream y da un resultado: `count()`. Para sumar números, primero se pasa a un stream de `int` con `mapToInt(Barcaza::carga)` y después `sum()`.

#### Desafío
Completá el `mapToInt` con la carga de cada barcaza.

#### Código inicial
```java
import java.util.List;

public class Cuenta {
    public static void main(String[] args) {
        List<Barcaza> rio = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20),
                new Barcaza("Bagre", 120), new Barcaza("Junco", 50));
        long cuantas = rio.stream().count();
        int total = rio.stream().mapToInt(___).sum();
        System.out.println("Barcazas: " + cuantas);
        System.out.println("Carga total: " + total);
    }
}

record Barcaza(String nombre, int carga) {
}
```

#### Salida esperada
```
Barcazas: 4
Carga total: 270
```

#### Solución
```java
import java.util.List;

public class Cuenta {
    public static void main(String[] args) {
        List<Barcaza> rio = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20),
                new Barcaza("Bagre", 120), new Barcaza("Junco", 50));
        long cuantas = rio.stream().count();
        int total = rio.stream().mapToInt(Barcaza::carga).sum();
        System.out.println("Barcazas: " + cuantas);
        System.out.println("Carga total: " + total);
    }
}

record Barcaza(String nombre, int carga) {
}
```

#### Al superarla
Cuatro barcazas, 270 de carga. El molinero lo talla en la puerta del molino, como cada día desde hace cien años.

#### Imagen
- Un molino con un contador de bronce que marca «4» y «270».
- El molinero tallando los números en la puerta.

### Micro-misión R04-N01-P4 · El agua no vuelve

```meta
lugar: La orilla del río de la capital
personajes: Zed, Gheco, Nadia, Kaffa
criatura: slime
carta: De un solo uso | un stream se recorre UNA vez · reusarlo da IllegalStateException · para otra pasada, otro .stream()
recompensa: xp 15, oro 15
```

#### Escena
Zed guarda una corriente en una variable y quiere usarla dos veces: una para contar y otra para sumar. La segunda vez, del agua sale un **slime**: *stream has already been operated upon or closed*.

#### Gheco sugiere
Un stream es como el agua del río: pasa **una vez**. Si lo guardás en una variable y lo usás dos veces, la segunda falla. Para otra pasada, pedí un stream nuevo a la lista: `rio.stream()`.

#### Desafío
Ejecutalo, leé el error y hacé que la suma use un stream nuevo.

#### Código inicial
```java
import java.util.List;
import java.util.stream.Stream;

public class AguaQueNoVuelve {
    public static void main(String[] args) {
        List<Integer> cargas = List.of(80, 20, 120, 50);
        Stream<Integer> corriente = cargas.stream();
        System.out.println("Pasaron: " + corriente.count());
        System.out.println("Carga: " + corriente.mapToInt(c -> c).sum());
    }
}
```

#### Salida esperada
```
Pasaron: 4
Carga: 270
```

#### Solución
```java
import java.util.List;
import java.util.stream.Stream;

public class AguaQueNoVuelve {
    public static void main(String[] args) {
        List<Integer> cargas = List.of(80, 20, 120, 50);
        Stream<Integer> corriente = cargas.stream();
        System.out.println("Pasaron: " + corriente.count());
        System.out.println("Carga: " + cargas.stream().mapToInt(c -> c).sum());
    }
}
```

#### Al superarla
Dos corrientes, dos resultados. El slime se disuelve en el agua.
Río abajo, en los muelles, los recaudadores no cuentan de a una: juntan todo en **cajas** por puerto.

#### Imagen
- Un slime saliendo del agua del río con un cartel de «IllegalStateException».
- Al fondo, los muelles con recaudadores juntando cajas por puerto.

### Misión R04-N01-M1 · El inventario que fluye

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con una lista de 8 productos (`record Producto(String nombre, String rubro, double
precio, int stock)`), resolvé **sin bucles**, cada punto con un stream:

1. Los nombres de los productos sin stock.
2. Cuántos productos cuestan más de 5000.
3. El valor total del inventario (precio × stock).
4. Los tres productos más caros, de mayor a menor.
5. Si hay algún producto del rubro "limpieza" con stock menor a 5.
6. Los rubros distintos, ordenados.

Mostrá los montos con 2 decimales.

#### Criterio de aprobación

- No hay `for` ni `while`: todo son streams.
- Cada punto usa la operación adecuada (`filter`, `count`, `mapToDouble`/`sum`, `sorted`+`limit`, `anyMatch`, `distinct`).

#### Salida esperada

```
Sin stock: [Aceite, Jamón]
Más de 5000: 2
Valor del inventario: 203610.00
Los más caros: [Jamón, Queso, Yerba]
¿Limpieza con poco stock? true
Rubros: [almacén, fiambrería, limpieza]
```

#### Solución de referencia

```java
// Mision 1 - El inventario que fluye: seis preguntas, seis streams.
import java.util.Comparator;
import java.util.List;
import java.util.Locale;

public class InventarioStreams {
    record Producto(String nombre, String rubro, double precio, int stock) { }

    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        List<Producto> productos = List.of(
                new Producto("Yerba", "almacén", 4200.5, 20), new Producto("Lavandina", "limpieza", 900, 3),
                new Producto("Aceite", "almacén", 2890, 0), new Producto("Detergente", "limpieza", 1600, 12),
                new Producto("Queso", "fiambrería", 9800, 4), new Producto("Jamón", "fiambrería", 12500, 0),
                new Producto("Arroz", "almacén", 1450, 30), new Producto("Esponja", "limpieza", 600, 25));

        System.out.println("Sin stock: " + productos.stream().filter(p -> p.stock() == 0).map(Producto::nombre).toList());
        System.out.println("Más de 5000: " + productos.stream().filter(p -> p.precio() > 5000).count());
        System.out.printf("Valor del inventario: %.2f%n", productos.stream().mapToDouble(p -> p.precio() * p.stock()).sum());
        System.out.println("Los más caros: " + productos.stream()
                .sorted(Comparator.comparingDouble(Producto::precio).reversed())
                .limit(3).map(Producto::nombre).toList());
        System.out.println("¿Limpieza con poco stock? " + productos.stream()
                .anyMatch(p -> p.rubro().equals("limpieza") && p.stock() < 5));
        System.out.println("Rubros: " + productos.stream().map(Producto::rubro).distinct().sorted().toList());
    }
}
```

### Misión R04-N01-M2 · Los números del oráculo

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con `IntStream` y sin bucles:

1. La suma de los números del 1 al 100 que son múltiplos de 3 o de 5.
2. Los primeros 10 números primos (escribí un método `esPrimo` y usá `iterate` o `range`
   con `filter` y `limit`).
3. El factorial de 15 con `LongStream.rangeClosed` y `reduce`.
4. Las palabras de una frase con más de 4 letras, en mayúsculas y sin repetir (con
   `Arrays.stream(frase.split(" "))`).
5. Cuántas vocales tiene la frase (con `chars()`).

#### Criterio de aprobación

- Usa `IntStream`/`LongStream`, `filter`, `limit`, `reduce` y `chars`.
- No hay bucles.

#### Salida esperada

```
Suma de múltiplos de 3 o 5: 2418
Primeros 10 primos: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
15! = 1307674368000
Palabras largas: [ORACULO, SIEMPRE, ENCUENTRA, CAMINO]
Vocales: 42
```

#### Solución de referencia

```java
// Mision 2 - Los numeros del oraculo: IntStream, LongStream y chars.
import java.util.Arrays;
import java.util.stream.IntStream;
import java.util.stream.LongStream;

public class NumerosOraculo {
    public static void main(String[] args) {
        int suma = IntStream.rangeClosed(1, 100).filter(n -> n % 3 == 0 || n % 5 == 0).sum();
        System.out.println("Suma de múltiplos de 3 o 5: " + suma);

        System.out.println("Primeros 10 primos: " + IntStream.iterate(2, n -> n + 1).filter(NumerosOraculo::esPrimo).limit(10).boxed().toList());

        long factorial = LongStream.rangeClosed(1, 15).reduce(1, (a, b) -> a * b);
        System.out.println("15! = " + factorial);

        String frase = "el oraculo del rio sabe que el agua siempre encuentra su camino y el camino siempre encuentra al agua";
        System.out.println("Palabras largas: " + Arrays.stream(frase.split(" ")).filter(p -> p.length() > 4)
                .map(String::toUpperCase).distinct().toList());
        long vocales = frase.chars().filter(c -> "aeiou".indexOf(c) >= 0).count();
        System.out.println("Vocales: " + vocales);
    }

    static boolean esPrimo(int n) {
        return n > 1 && IntStream.rangeClosed(2, (int) Math.sqrt(n)).noneMatch(d -> n % d == 0);
    }
}
```

### Misión R04-N01-M3 · Del bucle al stream

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Este método calcula, con bucles, el promedio de las notas aprobadas (4 o más) de los
alumnos de una comisión, redondeado a 2 decimales, y la lista de nombres de los que
tienen alguna nota de 10. Reescribí **los dos cálculos** con streams (debe dar
exactamente lo mismo) y mostrá los dos resultados, el viejo y el nuevo.

```java
static double promedioAprobadas(List<Alumno> alumnos, String comision) {
    double suma = 0;
    int cantidad = 0;
    for (Alumno a : alumnos) {
        if (a.comision().equals(comision)) {
            for (int nota : a.notas()) {
                if (nota >= 4) {
                    suma += nota;
                    cantidad++;
                }
            }
        }
    }
    return cantidad == 0 ? 0 : Math.round(suma / cantidad * 100) / 100.0;
}
```

#### Criterio de aprobación

- Los dos cálculos con streams dan lo mismo que con bucles.
- Usa `flatMapToInt` (o `flatMap`) para aplanar las listas de notas.

#### Salida esperada

```
Promedio (bucles): 7.38
Promedio (streams): 7.38
Con algún 10 (bucles): [Kira, Lía, Nara]
Con algún 10 (streams): [Kira, Lía, Nara]
```

#### Solución de referencia

```java
// Mision 3 - Del bucle al stream: el mismo calculo, dos formas.
import java.util.ArrayList;
import java.util.List;

public class BucleAStream {
    record Alumno(String nombre, String comision, List<Integer> notas) { }

    public static void main(String[] args) {
        List<Alumno> alumnos = List.of(
                new Alumno("Kira", "A", List.of(9, 10, 7)), new Alumno("Bron", "A", List.of(3, 6, 4)),
                new Alumno("Lía", "B", List.of(10, 8)), new Alumno("Pip", "A", List.of(2, 3)),
                new Alumno("Nara", "A", List.of(8, 10, 5)));

        System.out.println("Promedio (bucles): " + promedioConBucles(alumnos, "A"));
        System.out.println("Promedio (streams): " + promedioConStreams(alumnos, "A"));
        System.out.println("Con algún 10 (bucles): " + conDiezBucles(alumnos));
        System.out.println("Con algún 10 (streams): " + alumnos.stream().filter(a -> a.notas().contains(10)).map(Alumno::nombre).toList());
    }

    static double promedioConBucles(List<Alumno> alumnos, String comision) {
        double suma = 0;
        int cantidad = 0;
        for (Alumno a : alumnos) {
            if (a.comision().equals(comision)) {
                for (int nota : a.notas()) {
                    if (nota >= 4) {
                        suma += nota;
                        cantidad++;
                    }
                }
            }
        }
        return cantidad == 0 ? 0 : Math.round(suma / cantidad * 100) / 100.0;
    }

    static double promedioConStreams(List<Alumno> alumnos, String comision) {
        double promedio = alumnos.stream()
                .filter(a -> a.comision().equals(comision))
                .flatMapToInt(a -> a.notas().stream().mapToInt(Integer::intValue))
                .filter(n -> n >= 4)
                .average()
                .orElse(0);
        return Math.round(promedio * 100) / 100.0;
    }

    static List<String> conDiezBucles(List<Alumno> alumnos) {
        List<String> nombres = new ArrayList<>();
        for (Alumno a : alumnos) {
            if (a.notas().contains(10)) {
                nombres.add(a.nombre());
            }
        }
        return nombres;
    }
}
```

### Encargo R04-N01-E1 · El resumen de la tarjeta

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un banco quiere el resumen de la tarjeta de un cliente a partir de sus movimientos
(`record Movimiento(String fecha, String comercio, String rubro, double monto)`, con
montos negativos para las devoluciones). Con streams: el total a pagar, la compra más
cara (comercio y monto), los comercios donde compró más de una vez, el gasto en el rubro
"supermercado" y los movimientos de más de 20 000 ordenados por fecha. Montos con 2
decimales.

#### Criterio de aprobación

- Todos los cálculos con streams.
- Las devoluciones se restan del total.

#### Salida esperada

```
Total a pagar: 185750.50
Compra más cara: Tienda Tech (125000.00)
Comercios repetidos: [Súper Día, Tienda Tech]
Supermercado: 48950.50
Más de 20000: [2026-09-05 Nafta YPF, 2026-09-15 Tienda Tech, 2026-09-21 Mercado Central]
```

#### Solución de referencia

```java
// Encargo - El resumen de la tarjeta: streams sobre movimientos.
import java.util.Comparator;
import java.util.List;
import java.util.Locale;

public class ResumenTarjeta {
    record Movimiento(String fecha, String comercio, String rubro, double monto) { }

    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        List<Movimiento> movimientos = List.of(
                new Movimiento("2026-09-02", "Súper Día", "supermercado", 18450.5), new Movimiento("2026-09-05", "Nafta YPF", "combustible", 32000),
                new Movimiento("2026-09-09", "Súper Día", "supermercado", 9200), new Movimiento("2026-09-12", "Librería Kaffa", "librería", 4800),
                new Movimiento("2026-09-15", "Tienda Tech", "electrónica", 125000), new Movimiento("2026-09-18", "Tienda Tech", "electrónica", -25000),
                new Movimiento("2026-09-21", "Mercado Central", "supermercado", 21300));

        System.out.printf("Total a pagar: %.2f%n", movimientos.stream().mapToDouble(Movimiento::monto).sum());
        Movimiento mayor = movimientos.stream().max(Comparator.comparingDouble(Movimiento::monto)).orElseThrow();
        System.out.printf("Compra más cara: %s (%.2f)%n", mayor.comercio(), mayor.monto());
        System.out.println("Comercios repetidos: " + movimientos.stream().map(Movimiento::comercio).distinct()
                .filter(c -> movimientos.stream().filter(m -> m.comercio().equals(c)).count() > 1).toList());
        System.out.printf("Supermercado: %.2f%n", movimientos.stream().filter(m -> m.rubro().equals("supermercado")).mapToDouble(Movimiento::monto).sum());
        System.out.println("Más de 20000: " + movimientos.stream().filter(m -> m.monto() > 20000)
                .sorted(Comparator.comparing(Movimiento::fecha)).map(m -> m.fecha() + " " + m.comercio()).toList());
    }
}
```

### Prueba del sello

#### ¿Qué diferencia hay entre una operación intermedia y una terminal?

La intermedia devuelve otro stream (y no ejecuta nada todavía); la terminal produce el resultado y dispara todo el procesamiento.

#### ¿Qué pasa si usás el mismo stream dos veces?

Se lanza `IllegalStateException`: un stream se consume una sola vez.

#### ¿Qué devuelve `average()` de un `IntStream`?

Un `OptionalDouble`, porque el stream puede estar vacío.

#### ¿Para qué sirve `mapToInt`?

Para pasar a un `IntStream` y poder usar `sum`, `average`, `max` y `min`.

#### ¿Qué hace `flatMap`?

Aplana: convierte cada elemento en un stream y los junta todos en uno.

### Soluciones (docente)

Sale de `19-Java-Avanzado/05-Iteradores-Stream-API`, reescrito para la Senda. `toList()` es de Java 16+ (el curso pide Java 17).

## R04-N02 · Collectors y Optional

```meta
tipo: tema
padre: R04-N01
precio: 10
criatura: troll
temas: func.streams, err.opcionales
```

### Crónica

Río abajo, las corrientes llegan a los **muelles** de clasificación. Las barcazas se agrupan por puerto de destino en dársenas distintas, se cuentan, se promedia su carga. En una de las dársenas, un cartel dice: *«Puede estar vacía»*. Y a veces lo está. Zed revisa el registro del río buscando una barcaza que haya llevado un vitral.

—Juntar lo que fluye es un arte —dice {mentor}—. Y a veces la respuesta es **nada**: no hay barcaza con esa carga, no hay nota más alta en una lista vacía. En lugar de devolver `null` y dejar que el troll aparezca, el Java moderno devuelve una **caja que puede estar vacía**: un `Optional`.

### Objetivos

- Agrupar con `Collectors.groupingBy` y contar, sumar o promediar por grupo.
- Separar en dos grupos con `partitioningBy` y armar mapas con `toMap`.
- Unir textos con `joining`.
- Usar `Optional` para los resultados que pueden no existir, sin `null`.

### Antes de empezar

- Streams: datos que fluyen.
- Mapas y el Espectro Nulo (rama 3).

### Explicación

#### `collect` y los `Collectors`
`collect` es la operación terminal que **junta** el stream en una estructura. La clase
`Collectors` trae los más usados (`import static java.util.stream.Collectors.*;` para
escribirlos cortos):
| Collector | Arma |
|---|---|
| `toList()`, `toSet()` | una lista / un conjunto |
| `joining(", ")` | un texto con los elementos unidos |
| `groupingBy(clave)` | un `Map<clave, List<elementos>>` |
| `groupingBy(clave, collectorDeAbajo)` | un mapa con otra cosa por grupo (cuenta, suma…) |
| `partitioningBy(predicado)` | un `Map<Boolean, List<…>>`: los que cumplen y los que no |
| `toMap(clave, valor)` | un mapa de clave a valor (falla si hay claves repetidas) |
| `counting()`, `summingInt(…)`, `averagingDouble(…)` | se usan dentro de `groupingBy` |

```java
Map<String, Long> porClase = heroes.stream()
        .collect(groupingBy(Heroe::clase, TreeMap::new, counting()));    // TreeMap: ordenado por clave
Map<Boolean, List<Heroe>> aprobados = alumnos.stream()
        .collect(partitioningBy(a -> a.nota() >= 4));
String nombres = heroes.stream().map(Heroe::nombre).collect(joining(", ", "[", "]"));
```
Por defecto `groupingBy` arma un `HashMap` (sin orden garantizado); pasale `TreeMap::new`
como segundo argumento para que las claves salgan ordenadas.

#### `Optional`: una caja que puede estar vacía
Algunas operaciones pueden no tener resultado: el máximo de una lista vacía, el primero
que cumple una condición. En lugar de `null`, devuelven un **`Optional<T>`**:
```java
Optional<Heroe> mejor = heroes.stream().max(Comparator.comparingInt(Heroe::nivel));
Optional<Heroe> mago = heroes.stream().filter(h -> h.clase().equals("mago")).findFirst();
```
Cómo sacar el valor, sin `NullPointerException`:
| Método | Hace |
|---|---|
| `isPresent()` / `isEmpty()` | pregunta si hay valor |
| `orElse(otro)` | el valor, o `otro` si está vacío |
| `orElseGet(() -> …)` | lo mismo, calculando el alternativo solo si hace falta |
| `orElseThrow()` | el valor, o una excepción si está vacío |
| `ifPresent(v -> …)` | hace algo solo si hay valor |
| `map(función)` | transforma el valor, si hay |

```java
String nombre = mago.map(Heroe::nombre).orElse("nadie");
```
Tus propios métodos pueden devolver `Optional` en lugar de `null` para decir "puede no
haber": `Optional<Heroe> buscar(String nombre)`. Así, quien lo llama **no puede
olvidarse** de que puede estar vacío.

No uses `Optional` para atributos ni parámetros: está pensado para lo que **devuelve**
un método.

> **Si venís de Python.** `groupingBy` hace lo que `itertools.groupby` o un
> `defaultdict(list)`; `Optional` no existe en Python, donde se usa `None`.

### Código de ejemplo

```java
/*
 * Collectors y Optional: el puerto de clasificación.
 */
import static java.util.stream.Collectors.averagingInt;
import static java.util.stream.Collectors.counting;
import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.mapping;
import static java.util.stream.Collectors.partitioningBy;
import static java.util.stream.Collectors.toList;
import static java.util.stream.Collectors.toMap;

import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import java.util.TreeMap;

public class PuertoClasificacion {
    record Viajero(String nombre, String ciudad, int edad, int oro) { }

    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        List<Viajero> viajeros = List.of(
                new Viajero("Kira", "Valle", 19, 120), new Viajero("Bron", "Forjas", 45, 30),
                new Viajero("Lía", "Valle", 16, 35), new Viajero("Tesla", "Ciudadela", 33, 980),
                new Viajero("Pip", "Forjas", 12, 5), new Viajero("Nara", "Ciudadela", 28, 210));

        Map<String, Long> porCiudad = viajeros.stream().collect(groupingBy(Viajero::ciudad, TreeMap::new, counting()));
        System.out.println("Viajeros por ciudad: " + porCiudad);

        Map<String, Double> edadPromedio = viajeros.stream().collect(groupingBy(Viajero::ciudad, TreeMap::new, averagingInt(Viajero::edad)));
        edadPromedio.forEach((ciudad, edad) -> System.out.printf("  edad promedio en %s: %.1f%n", ciudad, edad));

        Map<String, List<String>> nombresPorCiudad = viajeros.stream()
                .collect(groupingBy(Viajero::ciudad, TreeMap::new, mapping(Viajero::nombre, toList())));
        System.out.println("Nombres por ciudad: " + nombresPorCiudad);

        Map<Boolean, List<String>> mayores = viajeros.stream()
                .collect(partitioningBy(v -> v.edad() >= 18, mapping(Viajero::nombre, toList())));
        System.out.println("Mayores: " + mayores.get(true) + " | menores: " + mayores.get(false));

        Map<String, Integer> oroPorNombre = viajeros.stream().collect(toMap(Viajero::nombre, Viajero::oro, (a, b) -> a, TreeMap::new));
        System.out.println("Oro: " + oroPorNombre);

        System.out.println("Todos: " + viajeros.stream().map(Viajero::nombre).sorted().collect(joining(", ", "[", "]")));

        // Optional: resultados que pueden no existir
        Optional<Viajero> masRico = viajeros.stream().max(Comparator.comparingInt(Viajero::oro));
        System.out.println("El más rico: " + masRico.map(Viajero::nombre).orElse("nadie"));

        Optional<Viajero> dePuerto = viajeros.stream().filter(v -> v.ciudad().equals("Puerto")).findFirst();
        System.out.println("¿Hay alguien del Puerto? " + dePuerto.isPresent() + " -> " + dePuerto.map(Viajero::nombre).orElse("nadie"));

        buscar(viajeros, "Nara").ifPresent(v -> System.out.println("Encontrada: " + v.nombre() + " de " + v.ciudad()));
        System.out.println("Buscar a Olmo: " + buscar(viajeros, "Olmo").map(Viajero::ciudad).orElse("no está"));
        try {
            buscar(viajeros, "Olmo").orElseThrow(() -> new IllegalArgumentException("no existe Olmo"));
        } catch (IllegalArgumentException e) {
            System.out.println("orElseThrow: " + e.getMessage());
        }
    }

    static Optional<Viajero> buscar(List<Viajero> viajeros, String nombre) {
        return viajeros.stream().filter(v -> v.nombre().equals(nombre)).findFirst();
    }
}
```

### Salida esperada

```
Viajeros por ciudad: {Ciudadela=2, Forjas=2, Valle=2}
  edad promedio en Ciudadela: 30.5
  edad promedio en Forjas: 28.5
  edad promedio en Valle: 17.5
Nombres por ciudad: {Ciudadela=[Tesla, Nara], Forjas=[Bron, Pip], Valle=[Kira, Lía]}
Mayores: [Kira, Bron, Tesla, Nara] | menores: [Lía, Pip]
Oro: {Bron=30, Kira=120, Lía=35, Nara=210, Pip=5, Tesla=980}
Todos: [Bron, Kira, Lía, Nara, Pip, Tesla]
El más rico: Tesla
¿Hay alguien del Puerto? false -> nadie
Encontrada: Nara de Ciudadela
Buscar a Olmo: no está
orElseThrow: no existe Olmo
```

### ¿Para qué sirve?

Agrupar y resumir es lo que piden todos los reportes: ventas por vendedor, alumnos por comisión, gastos por rubro, turnos por día. Con `groupingBy` se hacen en una línea. Y `Optional` es la respuesta moderna al Espectro Nulo: las APIs de Java y de Spring lo devuelven cada vez que algo puede no existir (por ejemplo, `findById` en los repositorios de la tercera Senda).

### Errores habituales

**Troll: `Optional.get()` sin preguntar.** `get()` sobre un `Optional` vacío lanza
`NoSuchElementException`: es el mismo problema que el `null`. Usá `orElse`, `map` o
`orElseThrow` con un mensaje.

**Ogro: el orden que cambia.** `groupingBy` sin `TreeMap::new` arma un `HashMap`: el
orden de las claves no está garantizado.

**Goblin: la clave repetida en `toMap`.** `IllegalStateException: Duplicate key` si dos
elementos dan la misma clave. Pasale una función que resuelva el choque (`(a, b) -> a`).

**Ogro: `Optional` como atributo o parámetro.** Complica el código sin ganar nada: está
pensado para valores de retorno.

**Ogro: `Optional.of(null)`.** Lanza `NullPointerException`. Para un valor que puede ser
`null`, `Optional.ofNullable(x)`.

### Micro-misión R04-N02-P1 · Las cajas de cada puerto

```meta
lugar: Los muelles del río
personajes: Zed, Gheco, Nadia, Kaffa
carta: groupingBy | collect(Collectors.groupingBy(Barcaza::puerto, TreeMap::new, Collectors.counting())) · un mapa: grupo → resultado
recompensa: xp 10, oro 10
```

#### Escena
En los muelles, los recaudadores juntan las barcazas en **cajas por puerto de destino** y escriben cuántas hay en cada una.

#### Gheco sugiere
`collect(Collectors.groupingBy(clave, …))` arma un mapa: cada clave con lo que le tocó. Con `Collectors.counting()` como segundo paso, el valor es **cuántos** hay. `TreeMap::new` deja las claves ordenadas.

#### Desafío
Completá el colector que cuenta cuántas barcazas hay por puerto.

#### Código inicial
```java
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.stream.Collectors;

public class Cajas {
    public static void main(String[] args) {
        List<Barcaza> muelle = List.of(new Barcaza("Garza", "Capital", 80), new Barcaza("Sauce", "Puerto", 20),
                new Barcaza("Bagre", "Capital", 120), new Barcaza("Junco", "Torre", 50), new Barcaza("Ceibo", "Puerto", 40));
        Map<String, Long> porPuerto = muelle.stream()
                .collect(Collectors.groupingBy(Barcaza::puerto, TreeMap::new, Collectors.___()));
        System.out.println(porPuerto);
    }
}

record Barcaza(String nombre, String puerto, int carga) {
}
```

#### Salida esperada
```
{Capital=2, Puerto=2, Torre=1}
```

#### Solución
```java
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.stream.Collectors;

public class Cajas {
    public static void main(String[] args) {
        List<Barcaza> muelle = List.of(new Barcaza("Garza", "Capital", 80), new Barcaza("Sauce", "Puerto", 20),
                new Barcaza("Bagre", "Capital", 120), new Barcaza("Junco", "Torre", 50), new Barcaza("Ceibo", "Puerto", 40));
        Map<String, Long> porPuerto = muelle.stream()
                .collect(Collectors.groupingBy(Barcaza::puerto, TreeMap::new, Collectors.counting()));
        System.out.println(porPuerto);
    }
}

record Barcaza(String nombre, String puerto, int carga) {
}
```

#### Al superarla
Dos a la Capital, dos al Puerto y una a la Torre. —¿Una sola barcaza a la Torre? —pregunta Zed—. Para el lugar más importante del Imperio, es poco.

#### Imagen
- Los muelles del río: recaudadores con cajas etiquetadas «Capital», «Puerto» y «Torre», con barquitos de madera adentro.
- Zed mirando la caja «Torre», casi vacía.

### Micro-misión R04-N02-P2 · La lista en una línea

```meta
lugar: Los muelles del río
personajes: Zed, Gheco, Nadia, Kaffa
carta: joining | collect(Collectors.joining(", ")) une textos con un separador · joining(", ", "[", "]") con principio y final
recompensa: xp 10, oro 10
```

#### Escena
El capitán del muelle quiere los nombres de las barcazas del día **en una sola línea**, separados por coma, para gritarlos desde la torreta.

#### Gheco sugiere
`Collectors.joining(", ")` une un stream de textos en uno solo, con el separador entre cada uno. Hay que pasar primero a textos: `.map(Barcaza::nombre)`.

#### Desafío
Completá el colector que une los nombres con ", ".

#### Código inicial
```java
import java.util.List;
import java.util.stream.Collectors;

public class Torreta {
    public static void main(String[] args) {
        List<Barcaza> muelle = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20), new Barcaza("Bagre", 120));
        String grito = muelle.stream()
                .map(Barcaza::nombre)
                .collect(Collectors.___);
        System.out.println("¡Hoy llegan " + grito + "!");
    }
}

record Barcaza(String nombre, int carga) {
}
```

#### Salida esperada
```
¡Hoy llegan Garza, Sauce, Bagre!
```

#### Solución
```java
import java.util.List;
import java.util.stream.Collectors;

public class Torreta {
    public static void main(String[] args) {
        List<Barcaza> muelle = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20), new Barcaza("Bagre", 120));
        String grito = muelle.stream()
                .map(Barcaza::nombre)
                .collect(Collectors.joining(", "));
        System.out.println("¡Hoy llegan " + grito + "!");
    }
}

record Barcaza(String nombre, int carga) {
}
```

#### Al superarla
El capitán lo grita desde la torreta y el muelle entero lo escucha. Sin una coma de más al final.

#### Imagen
- Un capitán gritando desde una torreta de madera, con un pergamino en la mano.
- Las barcazas Garza, Sauce y Bagre amarrando abajo.

### Micro-misión R04-N02-P3 · Livianas y pesadas

```meta
lugar: Los muelles del río
personajes: Zed, Gheco, Nadia, Kaffa
carta: partitioningBy | collect(Collectors.partitioningBy(b -> b.carga() > 60)) · un mapa con dos grupos: true y false
recompensa: xp 15, oro 15
```

#### Escena
Las barcazas pesadas van al muelle grande y las livianas al chico. Hay **dos** grupos y nada más: o pasa la condición, o no.

#### Gheco sugiere
`partitioningBy(condición)` arma un mapa con dos claves: `true` (las que cumplen) y `false` (las demás). `get(true)` da la lista de las que cumplen.

#### Desafío
Completá la condición: pesadas son las de más de 60.

#### Código inicial
```java
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class DosMuelles {
    public static void main(String[] args) {
        List<Barcaza> muelle = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20),
                new Barcaza("Bagre", 120), new Barcaza("Junco", 50));
        Map<Boolean, List<Barcaza>> grupos = muelle.stream()
                .collect(Collectors.partitioningBy(b -> ___));
        System.out.println("Muelle grande: " + grupos.get(true).stream().map(Barcaza::nombre).toList());
        System.out.println("Muelle chico: " + grupos.get(false).stream().map(Barcaza::nombre).toList());
    }
}

record Barcaza(String nombre, int carga) {
}
```

#### Salida esperada
```
Muelle grande: [Garza, Bagre]
Muelle chico: [Sauce, Junco]
```

#### Solución
```java
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class DosMuelles {
    public static void main(String[] args) {
        List<Barcaza> muelle = List.of(new Barcaza("Garza", 80), new Barcaza("Sauce", 20),
                new Barcaza("Bagre", 120), new Barcaza("Junco", 50));
        Map<Boolean, List<Barcaza>> grupos = muelle.stream()
                .collect(Collectors.partitioningBy(b -> b.carga() > 60));
        System.out.println("Muelle grande: " + grupos.get(true).stream().map(Barcaza::nombre).toList());
        System.out.println("Muelle chico: " + grupos.get(false).stream().map(Barcaza::nombre).toList());
    }
}

record Barcaza(String nombre, int carga) {
}
```

#### Al superarla
Garza y Bagre al grande, Sauce y Junco al chico. Ni una barcaza en el muelle equivocado.

#### Imagen
- Un muelle grande con dos barcazas pesadas y uno chico con dos livianas.
- Gheco señalando el cartel «> 60» en la bifurcación del canal.

### Micro-misión R04-N02-P4 · La barcaza que nunca llegó

```meta
lugar: La capitanía de los muelles
personajes: Zed, Gheco, Nadia, Kaffa
criatura: troll
carta: Optional | findFirst() devuelve un Optional: una caja que puede estar vacía · .map(...) adentro · .orElse("…") si no hay nada · nunca null
recompensa: xp 15, oro 20
```

#### Escena
Zed revisa el registro del río buscando una barcaza que haya llevado **un vitral**. Un **troll** espera que la búsqueda devuelva `null`… pero en las Corrientes, lo que puede no existir viene en una **caja**: un `Optional`.

#### Gheco sugiere
`findFirst()` devuelve un `Optional`: una caja con el primer resultado, o vacía. `.map(Registro::estado)` transforma lo de adentro si hay algo, y `.orElse("…")` da un valor por defecto si la caja está vacía.

#### Desafío
Completá el valor por defecto para cuando no hay ninguna barcaza: "ninguna".

#### Código inicial
```java
import java.util.List;

public class Registro {
    public static void main(String[] args) {
        List<Viaje> rio = List.of(new Viaje("Garza", "sal", "llegó"), new Viaje("Ceibo", "un vitral", "nunca llegó"),
                new Viaje("Bagre", "café", "llegó"));
        for (String carga : List.of("un vitral", "seda")) {
            String estado = rio.stream()
                    .filter(v -> v.carga().equals(carga))
                    .findFirst()
                    .map(v -> v.barcaza() + ", " + v.estado())
                    .orElse(___);
            System.out.println(carga + ": " + estado);
        }
    }
}

record Viaje(String barcaza, String carga, String estado) {
}
```

#### Salida esperada
```
un vitral: Ceibo, nunca llegó
seda: ninguna
```

#### Solución
```java
import java.util.List;

public class Registro {
    public static void main(String[] args) {
        List<Viaje> rio = List.of(new Viaje("Garza", "sal", "llegó"), new Viaje("Ceibo", "un vitral", "nunca llegó"),
                new Viaje("Bagre", "café", "llegó"));
        for (String carga : List.of("un vitral", "seda")) {
            String estado = rio.stream()
                    .filter(v -> v.carga().equals(carga))
                    .findFirst()
                    .map(v -> v.barcaza() + ", " + v.estado())
                    .orElse("ninguna");
            System.out.println(carga + ": " + estado);
        }
    }
}

record Viaje(String barcaza, String carga, String estado) {
}
```

#### Al superarla
«un vitral: Ceibo, nunca llegó.» La barcaza del Vidriero se llamaba **Ceibo**. El troll se queda sin su `null`.
En el delta, un cartógrafo ordena mapas de mil maneras. Tal vez sepa dónde se perdió el Ceibo.

#### Imagen
- Un registro del río abierto: una línea resaltada, «Ceibo · un vitral · nunca llegó».
- Zed, serio, apoyando el dedo sobre la línea; un troll yéndose con las manos vacías.

### Misión R04-N02-M1 · El reporte de ventas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con una lista de ventas (`record Venta(String vendedor, String rubro, int mes, double
monto)`, al menos 10), armá con `Collectors` (claves ordenadas):

1. El total vendido por vendedor.
2. La cantidad de ventas por rubro.
3. El promedio por venta de cada mes (1 decimal).
4. Para cada vendedor, los rubros en los que vendió (sin repetir, en un `Set` ordenado).
5. Las ventas separadas en "grandes" (más de 50 000) y "chicas", mostrando cuántas hay en
   cada grupo.
6. El vendedor con el mayor total (con `Optional`).

#### Criterio de aprobación

- Usa `groupingBy` con collectors de abajo (`summingDouble`, `counting`, `averagingDouble`, `mapping`).
- Usa `partitioningBy` y un `Optional` para el mejor vendedor.

#### Salida esperada

```
Total por vendedor: {Ana=196800.0, Juan=151500.0, Marta=116500.0}
Ventas por rubro: {audio=4, hogar=4, jardín=2}
  mes 1: promedio 49333.3
  mes 2: promedio 67500.0
  mes 3: promedio 28575.0
Rubros por vendedor: {Ana=[audio, hogar, jardín], Juan=[audio, hogar], Marta=[audio, hogar, jardín]}
Grandes: 4, chicas: 6
Mejor vendedor: Ana (196800.0)
```

#### Solución de referencia

```java
// Mision 1 - El reporte de ventas: groupingBy, partitioningBy y Optional.
import static java.util.stream.Collectors.averagingDouble;
import static java.util.stream.Collectors.counting;
import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.mapping;
import static java.util.stream.Collectors.partitioningBy;
import static java.util.stream.Collectors.summingDouble;
import static java.util.stream.Collectors.toCollection;

import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import java.util.TreeMap;
import java.util.TreeSet;

public class ReporteVentas {
    record Venta(String vendedor, String rubro, int mes, double monto) { }

    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        List<Venta> ventas = List.of(
                new Venta("Marta", "hogar", 1, 45000), new Venta("Juan", "audio", 1, 82000), new Venta("Marta", "audio", 1, 21000),
                new Venta("Ana", "hogar", 2, 67000), new Venta("Juan", "hogar", 2, 15500), new Venta("Ana", "audio", 2, 120000),
                new Venta("Marta", "hogar", 3, 38000), new Venta("Juan", "audio", 3, 54000), new Venta("Ana", "jardín", 3, 9800),
                new Venta("Marta", "jardín", 3, 12500));

        Map<String, Double> porVendedor = ventas.stream().collect(groupingBy(Venta::vendedor, TreeMap::new, summingDouble(Venta::monto)));
        System.out.println("Total por vendedor: " + porVendedor);
        System.out.println("Ventas por rubro: " + ventas.stream().collect(groupingBy(Venta::rubro, TreeMap::new, counting())));
        ventas.stream().collect(groupingBy(Venta::mes, TreeMap::new, averagingDouble(Venta::monto)))
                .forEach((mes, prom) -> System.out.printf("  mes %d: promedio %.1f%n", mes, prom));
        System.out.println("Rubros por vendedor: " + ventas.stream()
                .collect(groupingBy(Venta::vendedor, TreeMap::new, mapping(Venta::rubro, toCollection(TreeSet::new)))));
        Map<Boolean, Long> grandes = ventas.stream().collect(partitioningBy(v -> v.monto() > 50000, counting()));
        System.out.println("Grandes: " + grandes.get(true) + ", chicas: " + grandes.get(false));
        Optional<Map.Entry<String, Double>> mejor = porVendedor.entrySet().stream().max(Map.Entry.comparingByValue());
        System.out.println("Mejor vendedor: " + mejor.map(e -> e.getKey() + " (" + e.getValue() + ")").orElse("nadie"));
    }
}
```

### Misión R04-N02-M2 · El padrón sin nulls

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Padron` que guarda personas (`record Persona(String dni, String
nombre, String email)`, donde el email **puede ser `null`**) y tiene métodos que
**devuelven `Optional`**: `buscarPorDni(String)`, `emailDe(String dni)` (vacío si no
existe la persona **o** si no tiene email: usá `flatMap` o `map` + `ofNullable`) y
`masJoven()` (el DNI más alto suele ser el de la persona más joven). En el `main`,
probá los casos que existen y los que no, **sin** llamar nunca a `get()` ni comparar con
`null`.

#### Criterio de aprobación

- Los métodos devuelven `Optional` y usan `Optional.ofNullable` para el email.
- El `main` usa `map`, `orElse`, `ifPresentOrElse` u `orElseThrow`, nunca `get()`.

#### Salida esperada

```
Buscar 28999000: Juan Pérez
Buscar 11111111: no existe
Email de Marta: marta@correo.com
Email de Juan: sin email
Email de alguien inexistente: sin email
La persona más joven: Ana Ruiz
Padrón vacío: no hay más joven
```

#### Solución de referencia

```java
// Mision 2 - El padron sin nulls: metodos que devuelven Optional.
import java.util.Comparator;
import java.util.List;
import java.util.Optional;

public class PadronSinNulls {
    record Persona(String dni, String nombre, String email) { }

    public static void main(String[] args) {
        Padron p = new Padron(List.of(
                new Persona("30111222", "Marta Díaz", "marta@correo.com"),
                new Persona("28999000", "Juan Pérez", null),
                new Persona("41222333", "Ana Ruiz", "ana@correo.com")));

        System.out.println("Buscar 28999000: " + p.buscarPorDni("28999000").map(Persona::nombre).orElse("no existe"));
        System.out.println("Buscar 11111111: " + p.buscarPorDni("11111111").map(Persona::nombre).orElse("no existe"));
        System.out.println("Email de Marta: " + p.emailDe("30111222").orElse("sin email"));
        System.out.println("Email de Juan: " + p.emailDe("28999000").orElse("sin email"));
        System.out.println("Email de alguien inexistente: " + p.emailDe("99999999").orElse("sin email"));
        p.masJoven().ifPresentOrElse(x -> System.out.println("La persona más joven: " + x.nombre()),
                () -> System.out.println("Padrón vacío"));
        new Padron(List.of()).masJoven().ifPresentOrElse(x -> System.out.println(x.nombre()),
                () -> System.out.println("Padrón vacío: no hay más joven"));
    }

    static class Padron {
        private final List<Persona> personas;

        Padron(List<Persona> personas) {
            this.personas = personas;
        }

        Optional<Persona> buscarPorDni(String dni) {
            return personas.stream().filter(x -> x.dni().equals(dni)).findFirst();
        }

        Optional<String> emailDe(String dni) {
            return buscarPorDni(dni).flatMap(x -> Optional.ofNullable(x.email()));
        }

        Optional<Persona> masJoven() {
            return personas.stream().max(Comparator.comparing(Persona::dni));
        }
    }
}
```

### Misión R04-N02-M3 · Las palabras del libro

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Dado un texto largo (un párrafo de al menos 60 palabras en una constante), con streams y
`Collectors`:

1. La frecuencia de cada palabra (en minúsculas, sin signos de puntuación), mostrando
   las 5 más frecuentes y cuántas veces aparecen (desempate alfabético).
2. Las palabras agrupadas por su primera letra, solo las letras con 3 o más palabras
   distintas.
3. La palabra más larga (con `Optional`).
4. La longitud promedio de las palabras (1 decimal).

#### Criterio de aprobación

- Limpia el texto con `replaceAll` y `split("\\s+")`.
- Usa `groupingBy` + `counting` y ordena las entradas del mapa por valor.

#### Salida esperada

```
Las 5 más frecuentes:
  los: 6
  la: 5
  planos: 5
  y: 4
  a: 3
Por letra (3 o más distintas): {a=[a, acuerdo, arquitecta, así], c=[cada, ciudad, clase, clases, como, con, constructores, contrato, corrige, cosa, crece, creciendo, cuando], e=[el, en, existe], l=[la, las, levantan, los], p=[paciencia, paquete, pertenece, planos], s=[se, sigue, su, suelto]}
La más larga: constructores
Longitud promedio: 4.6
```

#### Solución de referencia

```java
// Mision 3 - Las palabras del libro: frecuencias con groupingBy y ordenar un mapa por valor.
import static java.util.stream.Collectors.counting;
import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.toCollection;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.TreeMap;
import java.util.TreeSet;

public class PalabrasLibro {
    static final String TEXTO = "En el Imperio de las Clases nada existe suelto. Cada cosa pertenece a una clase, "
            + "cada clase vive en su paquete y cada acuerdo se firma como un contrato. La arquitecta dibuja los planos, "
            + "los planos guían a los constructores y los constructores levantan la ciudad. Cuando la ciudad crece, "
            + "la arquitecta vuelve a los planos, corrige los planos y la ciudad sigue creciendo. Así crece el Imperio: "
            + "con planos, con clases y con paciencia.";

    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        List<String> palabras = Arrays.stream(TEXTO.toLowerCase().replaceAll("[^\\p{L} ]", "").split("\\s+")).toList();

        Map<String, Long> frecuencia = palabras.stream().collect(groupingBy(p -> p, counting()));
        System.out.println("Las 5 más frecuentes:");
        frecuencia.entrySet().stream()
                .sorted(Map.Entry.<String, Long>comparingByValue().reversed().thenComparing(Map.Entry.comparingByKey()))
                .limit(5)
                .forEach(e -> System.out.println("  " + e.getKey() + ": " + e.getValue()));

        Map<Character, TreeSet<String>> porLetra = palabras.stream()
                .collect(groupingBy(p -> p.charAt(0), TreeMap::new, toCollection(TreeSet::new)));
        porLetra.entrySet().removeIf(e -> e.getValue().size() < 3);
        System.out.println("Por letra (3 o más distintas): " + porLetra);

        System.out.println("La más larga: " + palabras.stream().max(Comparator.comparingInt(String::length).thenComparing(Comparator.reverseOrder())).orElse("-"));
        System.out.printf("Longitud promedio: %.1f%n", palabras.stream().mapToInt(String::length).average().orElse(0));
    }
}
```

### Encargo R04-N02-E1 · Las cuotas del club

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un club registra los pagos de cuotas (`record Pago(String socio, String categoria, int
mes, double monto)`). Con `Collectors`: lo recaudado por categoría y por mes (un mapa de
mapas, `groupingBy` dentro de `groupingBy`), los socios que pagaron los 3 meses
(agrupando por socio y contando), el socio que más pagó en total (`Optional`) y un texto
con todos los socios morosos (los que tienen menos de 3 pagos) separados por " · ".

#### Criterio de aprobación

- Usa un `groupingBy` anidado.
- Usa `joining` y un `Optional`.

#### Salida esperada

```
Recaudado por categoría y mes: {activo={1=24000.0, 2=24000.0, 3=25500.0}, cadete={1=6000.0, 3=6000.0}, vitalicio={2=3000.0}}
Pagaron los 3 meses: [Ana, Marta]
El que más pagó: Ana (37500.00)
Morosos: Juan · Leo
```

#### Solución de referencia

```java
// Encargo - Las cuotas del club: groupingBy anidado, joining y Optional.
import static java.util.stream.Collectors.counting;
import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.summingDouble;

import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.TreeMap;

public class CuotasClub {
    record Pago(String socio, String categoria, int mes, double monto) { }

    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        List<Pago> pagos = List.of(
                new Pago("Marta", "activo", 1, 12000), new Pago("Marta", "activo", 2, 12000), new Pago("Marta", "activo", 3, 12000),
                new Pago("Juan", "cadete", 1, 6000), new Pago("Juan", "cadete", 3, 6000),
                new Pago("Ana", "activo", 1, 12000), new Pago("Ana", "activo", 2, 12000), new Pago("Ana", "activo", 3, 13500),
                new Pago("Leo", "vitalicio", 2, 3000));

        Map<String, Map<Integer, Double>> recaudado = pagos.stream()
                .collect(groupingBy(Pago::categoria, TreeMap::new, groupingBy(Pago::mes, TreeMap::new, summingDouble(Pago::monto))));
        System.out.println("Recaudado por categoría y mes: " + recaudado);

        Map<String, Long> pagosPorSocio = pagos.stream().collect(groupingBy(Pago::socio, TreeMap::new, counting()));
        System.out.println("Pagaron los 3 meses: " + pagosPorSocio.entrySet().stream().filter(e -> e.getValue() == 3).map(Map.Entry::getKey).toList());

        pagos.stream().collect(groupingBy(Pago::socio, summingDouble(Pago::monto))).entrySet().stream()
                .max(Map.Entry.comparingByValue())
                .ifPresent(e -> System.out.printf("El que más pagó: %s (%.2f)%n", e.getKey(), e.getValue()));

        System.out.println("Morosos: " + pagosPorSocio.entrySet().stream().filter(e -> e.getValue() < 3).map(Map.Entry::getKey).collect(joining(" · ")));
    }
}
```

### Prueba del sello

#### ¿Qué devuelve `groupingBy(Heroe::clase)`?

Un `Map` de cada clase a la lista de héroes de esa clase.

#### ¿Cómo hacés que las claves de un `groupingBy` salgan ordenadas?

Pasándole `TreeMap::new` como fábrica del mapa.

#### ¿Qué problema resuelve `Optional`?

Representa un resultado que puede no existir sin usar `null`, obligando a quien lo recibe a pensar en el caso vacío.

#### ¿Por qué no conviene llamar a `get()` sobre un `Optional`?

Porque si está vacío lanza `NoSuchElementException`; es mejor `orElse`, `map`, `ifPresent` u `orElseThrow` con mensaje.

#### ¿Qué diferencia hay entre `Optional.of(x)` y `Optional.ofNullable(x)`?

`of` exige un valor no nulo (con `null` lanza excepción); `ofNullable` devuelve un `Optional` vacío si `x` es `null`.

### Soluciones (docente)

Sale de `19-Java-Avanzado/02-Collections-Framework` y `05-Iteradores-Stream-API`. Los `TreeMap::new` en los `groupingBy` son para que las salidas esperadas no dependan del orden de un `HashMap`.

## R04-N03 · Comparadores y el Java moderno

```meta
tipo: tema
padre: R04-N02
precio: 10
criatura: goblin
temas: poo.records
usa: func.lambdas
```

### Crónica

En el delta del río, las corrientes se dividen en brazos cada vez más finos. Un cartógrafo anciano ordena sus mapas de mil maneras: por región, después por fecha, después por nombre, al revés. En su mesa hay moldes nuevos, más cortos que los de la Academia, y cajas cerradas con un sello que dice exactamente qué puede haber adentro. Zed le pregunta por una barcaza llamada Ceibo.

—El Java que aprendiste en la Academia sigue vivo —dice {mentor}—, pero el lenguaje creció. Ahora hay formas más cortas y más seguras de decir lo mismo: comparadores que se encadenan, `record`s que se validan solos, jerarquías **selladas** y `switch` que devuelven valores. Es el Java que vas a leer en cualquier proyecto nuevo, Zed.

### Objetivos

- Armar comparadores con `Comparator.comparing`, `thenComparing`, `reversed` y `nullsLast`.
- Validar los datos de un `record` con un constructor compacto.
- Definir jerarquías cerradas con `sealed` y `permits`.
- Usar `instanceof` con patrón, `switch` como expresión, bloques de texto y `var`.

### Antes de empezar

- Collectors y Optional.
- Herencia, interfaces y `record` (rama 2).

### Explicación

#### Comparadores encadenados
`Comparator` tiene métodos que arman comparadores sin escribir `compare` a mano:
```java
Comparator<Heroe> orden = Comparator.comparing(Heroe::clase)        // primero por clase
        .thenComparing(Heroe::nivel, Comparator.reverseOrder())      // después nivel de mayor a menor
        .thenComparing(Heroe::nombre);                               // y a igual nivel, por nombre
lista.sort(orden);
```
| Método | Hace |
|---|---|
| `comparing(clave)` | compara por esa clave (que tiene que ser `Comparable`) |
| `comparingInt` / `comparingDouble` | lo mismo con números, sin *boxing* |
| `thenComparing(…)` | desempata con otro criterio |
| `reversed()` | invierte el orden **de todo lo anterior** |
| `nullsFirst(…)` / `nullsLast(…)` | dónde van los `null` |

Cuidado con `reversed()`: se aplica a toda la cadena hasta ese punto. Para invertir un
solo criterio, pasale `Comparator.reverseOrder()` a ese `thenComparing`.

#### `record` con validación
Un `record` puede tener un **constructor compacto**: sin parámetros ni asignaciones,
solo las validaciones (o normalizaciones) antes de guardar los valores.
```java
record Moneda(String codigo, double valor) {
    Moneda {
        if (valor < 0) throw new IllegalArgumentException("valor negativo: " + valor);
        codigo = codigo.toUpperCase();          // se puede normalizar el parámetro
    }
}
```
Los `record` también pueden tener métodos y métodos `static` (fábricas).

#### Jerarquías selladas
Una interfaz (o clase) `sealed` dice **exactamente** quiénes pueden implementarla:
```java
sealed interface Figura permits Circulo, Rectangulo, Triangulo { }
record Circulo(double radio) implements Figura { }
record Rectangulo(double ancho, double alto) implements Figura { }
record Triangulo(double base, double altura) implements Figura { }
```
Nadie más puede agregar una `Figura`. Las subclases tienen que ser `final` (los `record`
ya lo son), `sealed` o `non-sealed`. Sirve para modelar "una de estas opciones y
ninguna otra": los estados de un pedido, los tipos de movimiento de una cuenta.

#### `instanceof` con patrón
Antes había que preguntar y después castear. Ahora el `instanceof` declara la variable:
```java
if (figura instanceof Circulo c) {
    return Math.PI * c.radio() * c.radio();     // c ya es un Circulo
}
```

#### `switch` como expresión
El `switch` con flechas **devuelve un valor**, y el compilador exige cubrir todos los
casos (con un `enum`, todos sus valores; si no, un `default`). Si un caso necesita
varias líneas, termina con `yield`:
```java
int dias = switch (mes) {
    case 2 -> 28;
    case 4, 6, 9, 11 -> 30;
    default -> {
        if (mes < 1 || mes > 12) throw new IllegalArgumentException("mes inválido");
        yield 31;
    }
};
```

> **Java 21 y después.** En Java 21 el `switch` también acepta patrones de tipo
> (`case Circulo c -> …`) y, con una jerarquía sellada, el compilador verifica que no
> falte ningún caso. Este curso usa Java 17, así que para distinguir tipos usamos
> `instanceof` con patrón; si tenés Java 21, probá la versión con `switch`.

#### Bloques de texto y `var`
Un **bloque de texto** escribe texto de varias líneas sin `\n` ni `+`, ideal para SQL,
JSON o HTML:
```java
String sql = """
        SELECT nombre, nivel
        FROM heroe
        WHERE nivel > ?
        """;
```
`var` deja que el compilador deduzca el tipo de una variable local cuando es evidente:
`var heroes = new ArrayList<Heroe>();`. Sigue siendo tipado estático: la variable es un
`ArrayList<Heroe>` para siempre. Usalo cuando el tipo se ve en la misma línea; si hay
que adivinarlo, mejor escribirlo.

> **Si venís de Python.** El `switch` como expresión se parece al `match` de Python
> 3.10, y los bloques de texto a las comillas triples `"""`.

### Código de ejemplo

```java
/*
 * El Java moderno: comparadores, records validados, sealed, patrones y switch.
 */
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;

public class JavaModerno {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);

        // Comparadores encadenados
        var heroes = new ArrayList<>(List.of(
                new Heroe("Kira", "arquera", 7), new Heroe("Bron", "guerrero", 9),
                new Heroe("Lía", "maga", 7), new Heroe("Ada", "arquera", 9),
                new Heroe("Olmo", "guerrero", 4), new Heroe("Nara", "maga", 7)));
        heroes.sort(Comparator.comparing(Heroe::clase)
                .thenComparing(Heroe::nivel, Comparator.reverseOrder())
                .thenComparing(Heroe::nombre));
        System.out.println("Por clase, nivel (mayor primero) y nombre:");
        heroes.forEach(h -> System.out.println("  " + h));

        heroes.sort(Comparator.comparingInt(Heroe::nivel).thenComparing(Heroe::nombre).reversed());
        System.out.println("Todo al revés: " + heroes.stream().map(Heroe::nombre).toList());

        // record con constructor compacto
        System.out.println(new Moneda("ars", 1500));
        try {
            new Moneda("usd", -3);
        } catch (IllegalArgumentException e) {
            System.out.println("Rechazada: " + e.getMessage());
        }

        // sealed + instanceof con patrón
        List<Figura> figuras = List.of(new Circulo(1), new Rectangulo(3, 4), new Triangulo(6, 2));
        for (Figura f : figuras) {
            System.out.printf("%s -> área %.2f%n", f, area(f));
        }

        // switch como expresión, con yield
        for (int mes : new int[] {2, 7, 11}) {
            System.out.println("El mes " + mes + " tiene " + diasDelMes(mes) + " días");
        }

        // bloque de texto
        String consulta = """
                SELECT nombre, nivel
                FROM heroe
                WHERE nivel > 5
                ORDER BY nivel DESC;
                """;
        System.out.print(consulta);
    }

    static double area(Figura f) {
        if (f instanceof Circulo c) {
            return Math.PI * c.radio() * c.radio();
        } else if (f instanceof Rectangulo r) {
            return r.ancho() * r.alto();
        } else if (f instanceof Triangulo t) {
            return t.base() * t.altura() / 2;
        }
        throw new IllegalStateException("figura desconocida");
    }

    static int diasDelMes(int mes) {
        return switch (mes) {
            case 2 -> 28;
            case 4, 6, 9, 11 -> 30;
            default -> {
                if (mes < 1 || mes > 12) {
                    throw new IllegalArgumentException("mes inválido: " + mes);
                }
                yield 31;
            }
        };
    }

    record Heroe(String nombre, String clase, int nivel) {
        @Override
        public String toString() {
            return nombre + " (" + clase + ", " + nivel + ")";
        }
    }

    record Moneda(String codigo, double valor) {
        Moneda {
            if (valor < 0) {
                throw new IllegalArgumentException("valor negativo: " + valor);
            }
            codigo = codigo.toUpperCase();
        }
    }

    sealed interface Figura permits Circulo, Rectangulo, Triangulo { }

    record Circulo(double radio) implements Figura { }

    record Rectangulo(double ancho, double alto) implements Figura { }

    record Triangulo(double base, double altura) implements Figura { }
}
```

### Salida esperada

```
Por clase, nivel (mayor primero) y nombre:
  Ada (arquera, 9)
  Kira (arquera, 7)
  Bron (guerrero, 9)
  Olmo (guerrero, 4)
  Lía (maga, 7)
  Nara (maga, 7)
Todo al revés: [Bron, Ada, Nara, Lía, Kira, Olmo]
Moneda[codigo=ARS, valor=1500.0]
Rechazada: valor negativo: -3.0
Circulo[radio=1.0] -> área 3.14
Rectangulo[ancho=3.0, alto=4.0] -> área 12.00
Triangulo[base=6.0, altura=2.0] -> área 6.00
El mes 2 tiene 28 días
El mes 7 tiene 31 días
El mes 11 tiene 30 días
SELECT nombre, nivel
FROM heroe
WHERE nivel > 5
ORDER BY nivel DESC;
```

### ¿Para qué sirve?

Ordenar por varios criterios es de todos los días (un listado de alumnos por comisión y apellido, un ranking con desempates). Los `record` validados, las jerarquías selladas y el `switch` como expresión hacen el código más corto y hacen que el compilador encuentre errores que antes aparecían en producción: un caso olvidado, un dato inválido que se coló. Es lo que vas a ver en cualquier proyecto Java escrito en los últimos años.

### Errores habituales

**Goblin: el `reversed()` que invierte todo.** `comparing(A).thenComparing(B).reversed()`
invierte **los dos** criterios. Para invertir solo `B`:
`thenComparing(B, Comparator.reverseOrder())`.

**Ogro: el constructor compacto que asigna.** Dentro del constructor compacto no se
escribe `this.valor = valor`: no compila. Las asignaciones las hace Java al final; vos
solo validás o cambiás los parámetros.

**Troll: el `sealed` en otro archivo.** Las clases permitidas tienen que estar en el
mismo archivo (o en el mismo paquete o módulo). Si una no es `final`, `sealed` ni
`non-sealed`, no compila.

**Slime: el `switch` sin todos los casos.** Un `switch` como expresión tiene que cubrir
todos los valores posibles: con un `int` hace falta `default`.

**Ogro: `var` sin inicializar.** `var x;` o `var x = null;` no compila: el compilador
necesita ver el tipo.

### Micro-misión R04-N03-P1 · Los mapas del cartógrafo

```meta
lugar: El delta del río
personajes: Zed, Gheco, Nadia, Kaffa
carta: Comparadores encadenados | Comparator.comparingInt(Mapa::anio).reversed().thenComparing(Mapa::region) · sin escribir compare a mano
recompensa: xp 10, oro 10
```

#### Escena
El cartógrafo del delta ordena sus mapas de mil maneras. Zed le pide los más **nuevos primero** y, si son del mismo año, por región. —Armalo con piezas —le dice el viejo—, que yo ya no tengo pulso.

#### Gheco sugiere
`Comparator.comparingInt(Mapa::anio)` ordena por año; `.reversed()` lo da vuelta (más nuevos primero). `.thenComparing(Mapa::region)` desempata. Ojo: `reversed()` invierte **todo** lo que está antes.

#### Desafío
Completá el desempate por región.

#### Código inicial
```java
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Cartografo {
    public static void main(String[] args) {
        List<Mapa> mapas = new ArrayList<>(List.of(new Mapa("Delta", 1203), new Mapa("Capital", 1190),
                new Mapa("Aduana", 1203), new Mapa("Represa", 1201)));
        mapas.sort(Comparator.comparingInt(Mapa::anio).reversed().___(Mapa::region));
        mapas.forEach(m -> System.out.println(m.anio() + " " + m.region()));
    }
}

record Mapa(String region, int anio) {
}
```

#### Salida esperada
```
1203 Aduana
1203 Delta
1201 Represa
1190 Capital
```

#### Solución
```java
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Cartografo {
    public static void main(String[] args) {
        List<Mapa> mapas = new ArrayList<>(List.of(new Mapa("Delta", 1203), new Mapa("Capital", 1190),
                new Mapa("Aduana", 1203), new Mapa("Represa", 1201)));
        mapas.sort(Comparator.comparingInt(Mapa::anio).reversed().thenComparing(Mapa::region));
        mapas.forEach(m -> System.out.println(m.anio() + " " + m.region()));
    }
}

record Mapa(String region, int anio) {
}
```

#### Al superarla
Los mapas del 1203 arriba, Aduana antes que Delta. El tercero, el de 1201, tiene algo marcado en rojo: **la Represa**.

#### Imagen
- La mesa del cartógrafo del delta llena de mapas ordenados en pilas.
- Un mapa con una X roja sobre la Represa.

### Micro-misión R04-N03-P2 · El molde que se valida solo

```meta
lugar: El delta del río
personajes: Zed, Gheco, Nadia, Kaffa
criatura: goblin
carta: record con validación | record Carga(String que, int kilos) { Carga { if (kilos < 0) throw …; } } · constructor compacto: valida antes de guardar
recompensa: xp 15, oro 15
```

#### Escena
En el delta, los moldes son más cortos que los de la Academia: son `record`. Pero un **goblin** anota cargas con kilos negativos y nadie lo frena.

#### Gheco sugiere
Un `record` puede tener un **constructor compacto**: `Carga { … }`, sin paréntesis. Adentro se validan los parámetros; las asignaciones las hace Java solo, al final. Si algo no sirve, se lanza `IllegalArgumentException`.

#### Desafío
Completá la condición que rechaza los kilos negativos.

#### Código inicial
```java
public class Delta {
    public static void main(String[] args) {
        int[] pesos = {30, -5, 0};
        for (int k : pesos) {
            try {
                System.out.println("Anotada: " + new Carga("sal", k));
            } catch (IllegalArgumentException e) {
                System.out.println("Rechazada: " + e.getMessage());
            }
        }
    }
}

record Carga(String que, int kilos) {
    Carga {
        if (___) {
            throw new IllegalArgumentException("kilos negativos: " + kilos);
        }
    }
}
```

#### Salida esperada
```
Anotada: Carga[que=sal, kilos=30]
Rechazada: kilos negativos: -5
Anotada: Carga[que=sal, kilos=0]
```

#### Solución
```java
public class Delta {
    public static void main(String[] args) {
        int[] pesos = {30, -5, 0};
        for (int k : pesos) {
            try {
                System.out.println("Anotada: " + new Carga("sal", k));
            } catch (IllegalArgumentException e) {
                System.out.println("Rechazada: " + e.getMessage());
            }
        }
    }
}

record Carga(String que, int kilos) {
    Carga {
        if (kilos < 0) {
            throw new IllegalArgumentException("kilos negativos: " + kilos);
        }
    }
}
```

#### Al superarla
Los −5 kilos rebotan en el molde. El goblin tira su pluma al río.

#### Imagen
- Un molde de bronce corto, con la palabra «record», que rechaza una carga con «-5» escrito.
- Un goblin enojado tirando una pluma al agua.

### Micro-misión R04-N03-P3 · Las cajas selladas

```meta
lugar: El delta del río
personajes: Zed, Gheco, Nadia, Kaffa
carta: sealed e instanceof con patrón | sealed interface Bulto permits Caja, Barril · if (b instanceof Caja c) pregunta y castea en un paso
recompensa: xp 15, oro 15
```

#### Escena
En el delta hay cajas cerradas con un sello que dice exactamente qué puede haber adentro: **solo** cajas o barriles, nada más. Zed tiene que tratar distinto a cada uno.

#### Gheco sugiere
Una interfaz `sealed … permits Caja, Barril` solo deja que la implementen esas clases. `if (b instanceof Caja c)` pregunta el tipo y, si es, ya te da la variable `c` de tipo `Caja`, sin casting aparte.

#### Desafío
Completá el `instanceof` con patrón: si es un `Barril`, llamalo `barril`.

#### Código inicial
```java
import java.util.List;

public class Sellados {
    static String describir(Bulto b) {
        if (b instanceof Caja c) {
            return "caja de " + c.lado() + " cm";
        } else if (b instanceof ___) {
            return "barril de " + barril.litros() + " litros";
        }
        return "desconocido";
    }

    public static void main(String[] args) {
        for (Bulto b : List.of(new Caja(40), new Barril(200), new Caja(15))) {
            System.out.println(describir(b));
        }
    }
}

sealed interface Bulto permits Caja, Barril {
}

record Caja(int lado) implements Bulto {
}

record Barril(int litros) implements Bulto {
}
```

#### Salida esperada
```
caja de 40 cm
barril de 200 litros
caja de 15 cm
```

#### Solución
```java
import java.util.List;

public class Sellados {
    static String describir(Bulto b) {
        if (b instanceof Caja c) {
            return "caja de " + c.lado() + " cm";
        } else if (b instanceof Barril barril) {
            return "barril de " + barril.litros() + " litros";
        }
        return "desconocido";
    }

    public static void main(String[] args) {
        for (Bulto b : List.of(new Caja(40), new Barril(200), new Caja(15))) {
            System.out.println(describir(b));
        }
    }
}

sealed interface Bulto permits Caja, Barril {
}

record Caja(int lado) implements Bulto {
}

record Barril(int litros) implements Bulto {
}
```

#### Al superarla
Dos cajas y un barril, cada uno descripto a su manera. El sello garantiza que no aparezca un bulto de otro tipo a la noche.

#### Imagen
- Cajas y barriles sellados con un lacre dorado que dice «permits Caja, Barril».
- Zed etiquetando cada bulto.

### Micro-misión R04-N03-P4 · El informe en un bloque

```meta
lugar: El delta del río
personajes: Zed, Gheco, Nadia, Kaffa
carta: Bloque de texto y var | var x = 3; deduce el tipo · """ … """ un texto de varias líneas · .formatted(…) completa los %s y %d
recompensa: xp 15, oro 20
```

#### Escena
El cartógrafo le dicta a Zed un informe de varias líneas para mandar a la Torre. Con comillas y `+` por todos lados, el informe queda ilegible. —En el Java nuevo —dice Kaffa—, el texto se escribe **como se ve**.

#### Gheco sugiere
Un **bloque de texto** empieza y termina con tres comillas (`"""`) y respeta los saltos de línea. `.formatted(a, b)` reemplaza los `%s` y `%d` en orden. `var` deja que el compilador deduzca el tipo.

#### Desafío
Completá el método que completa los `%s` y `%d` del bloque.

#### Código inicial
```java
public class Informe {
    public static void main(String[] args) {
        var barcaza = "Ceibo";
        var dias = 12;
        var informe = """
                Informe del delta
                Barcaza perdida: %s
                Días sin noticias: %d
                Último lugar visto: la Represa""".___(barcaza, dias);
        System.out.println(informe);
    }
}
```

#### Salida esperada
```
Informe del delta
Barcaza perdida: Ceibo
Días sin noticias: 12
Último lugar visto: la Represa
```

#### Solución
```java
public class Informe {
    public static void main(String[] args) {
        var barcaza = "Ceibo";
        var dias = 12;
        var informe = """
                Informe del delta
                Barcaza perdida: %s
                Días sin noticias: %d
                Último lugar visto: la Represa""".formatted(barcaza, dias);
        System.out.println(informe);
    }
}
```

#### Al superarla
El informe sale prolijo, como un pergamino. El Ceibo se vio por última vez en **la Represa**.
Camino a la Represa está el astillero, donde los maestros arman los barcos con recetas que se pasan de generación en generación.

#### Imagen
- Un pergamino prolijo con el informe del delta, con «la Represa» subrayado.
- Al fondo, el astillero con barcos a medio armar.

### Misión R04-N03-M1 · El ranking con desempates

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un torneo guarda los resultados de los jugadores (`record Jugador(String nombre, String
equipo, int puntos, int goles, Integer edad)`, donde la edad **puede ser `null`**).
Ordená la lista de tres formas, **solo con comparadores encadenados** (sin escribir
`compare` a mano), y mostrá cada una:

1. El ranking: más puntos primero; a igual puntos, más goles; a igual goles, por nombre.
2. Por equipo alfabético, y dentro de cada equipo por nombre al revés.
3. Por edad de menor a mayor, con los que no tienen edad al final.

#### Criterio de aprobación

- Usa `comparing`, `thenComparing`, `reverseOrder` o `reversed` y `nullsLast`.
- No hay ningún `compare` escrito a mano.

#### Salida esperada

```
Ranking:
  Caro   Oeste   15 pts   7 goles  edad 25
  Sofi   Sur     15 pts   5 goles  edad ?
  Tomi   Sur     12 pts  10 goles  edad 17
  Ana    Norte   12 pts   8 goles  edad 22
  Lucas  Norte   12 pts   8 goles  edad 19
  Beto   Oeste    9 pts   2 goles  edad ?
Por equipo:
  Lucas  Norte   12 pts   8 goles  edad 19
  Ana    Norte   12 pts   8 goles  edad 22
  Caro   Oeste   15 pts   7 goles  edad 25
  Beto   Oeste    9 pts   2 goles  edad ?
  Tomi   Sur     12 pts  10 goles  edad 17
  Sofi   Sur     15 pts   5 goles  edad ?
Por edad:
  Tomi   Sur     12 pts  10 goles  edad 17
  Lucas  Norte   12 pts   8 goles  edad 19
  Ana    Norte   12 pts   8 goles  edad 22
  Caro   Oeste   15 pts   7 goles  edad 25
  Beto   Oeste    9 pts   2 goles  edad ?
  Sofi   Sur     15 pts   5 goles  edad ?
```

#### Solución de referencia

```java
// Mision 1 - El ranking con desempates: comparadores encadenados.
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class RankingDesempates {
    record Jugador(String nombre, String equipo, int puntos, int goles, Integer edad) { }

    public static void main(String[] args) {
        var jugadores = new ArrayList<>(List.of(
                new Jugador("Lucas", "Norte", 12, 8, 19), new Jugador("Sofi", "Sur", 15, 5, null),
                new Jugador("Ana", "Norte", 12, 8, 22), new Jugador("Tomi", "Sur", 12, 10, 17),
                new Jugador("Beto", "Oeste", 9, 2, null), new Jugador("Caro", "Oeste", 15, 7, 25)));

        jugadores.sort(Comparator.comparingInt(Jugador::puntos).reversed()
                .thenComparing(Jugador::goles, Comparator.reverseOrder())
                .thenComparing(Jugador::nombre));
        mostrar("Ranking", jugadores);

        jugadores.sort(Comparator.comparing(Jugador::equipo).thenComparing(Jugador::nombre, Comparator.reverseOrder()));
        mostrar("Por equipo", jugadores);

        jugadores.sort(Comparator.comparing(Jugador::edad, Comparator.nullsLast(Comparator.naturalOrder())));
        mostrar("Por edad", jugadores);
    }

    static void mostrar(String titulo, List<Jugador> jugadores) {
        System.out.println(titulo + ":");
        jugadores.forEach(j -> System.out.printf("  %-6s %-6s %3d pts %3d goles  edad %s%n",
                j.nombre(), j.equipo(), j.puntos(), j.goles(), j.edad() == null ? "?" : j.edad()));
    }
}
```

### Misión R04-N03-M2 · Los movimientos sellados

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Modelá los movimientos de una cuenta con una interfaz sellada `Movimiento` que solo
permite tres `record`: `Deposito(double monto)`, `Extraccion(double monto)` y
`Transferencia(String destino, double monto)`. Cada `record` valida en su constructor
compacto que el monto sea positivo (y la transferencia, que el destino no esté vacío).
Escribí un método `aplicar(double saldo, Movimiento m)` que use `instanceof` con patrón
y devuelva el saldo nuevo (la transferencia descuenta el monto más una comisión del
1 %), y un método `describir(Movimiento m)` que devuelva un texto para el resumen.
Aplicá una lista de movimientos desde un saldo de 10 000 y probá que un movimiento con
monto negativo se rechaza.

#### Criterio de aprobación

- La interfaz es `sealed` con `permits` y los `record` validan en el constructor compacto.
- Usa `instanceof` con patrón, sin casteos.

#### Salida esperada

```
Saldo inicial: 10000.00
Depósito de 2500.0               saldo:   12500.00
Extracción de 4000.0             saldo:    8500.00
Transferencia a Ana de 3000.0    saldo:    5470.00
Depósito de 800.0                saldo:    6270.00
Rechazado: la extracción tiene que ser positiva
Rechazado: la transferencia necesita un destino
```

#### Solución de referencia

```java
// Mision 2 - Los movimientos sellados: sealed, records validados e instanceof con patron.
import java.util.List;
import java.util.Locale;

public class MovimientosSellados {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        List<Movimiento> movimientos = List.of(new Deposito(2500), new Extraccion(4000),
                new Transferencia("Ana", 3000), new Deposito(800));
        double saldo = 10000;
        System.out.printf("Saldo inicial: %.2f%n", saldo);
        for (Movimiento m : movimientos) {
            saldo = aplicar(saldo, m);
            System.out.printf("%-32s saldo: %10.2f%n", describir(m), saldo);
        }
        try {
            new Extraccion(-50);
        } catch (IllegalArgumentException e) {
            System.out.println("Rechazado: " + e.getMessage());
        }
        try {
            new Transferencia(" ", 100);
        } catch (IllegalArgumentException e) {
            System.out.println("Rechazado: " + e.getMessage());
        }
    }

    static double aplicar(double saldo, Movimiento m) {
        if (m instanceof Deposito d) {
            return saldo + d.monto();
        } else if (m instanceof Extraccion e) {
            return saldo - e.monto();
        } else if (m instanceof Transferencia t) {
            return saldo - t.monto() * 1.01;
        }
        throw new IllegalStateException("movimiento desconocido");
    }

    static String describir(Movimiento m) {
        if (m instanceof Deposito d) {
            return "Depósito de " + d.monto();
        } else if (m instanceof Extraccion e) {
            return "Extracción de " + e.monto();
        } else if (m instanceof Transferencia t) {
            return "Transferencia a " + t.destino() + " de " + t.monto();
        }
        throw new IllegalStateException("movimiento desconocido");
    }

    sealed interface Movimiento permits Deposito, Extraccion, Transferencia { }

    record Deposito(double monto) implements Movimiento {
        Deposito {
            if (monto <= 0) {
                throw new IllegalArgumentException("el depósito tiene que ser positivo");
            }
        }
    }

    record Extraccion(double monto) implements Movimiento {
        Extraccion {
            if (monto <= 0) {
                throw new IllegalArgumentException("la extracción tiene que ser positiva");
            }
        }
    }

    record Transferencia(String destino, double monto) implements Movimiento {
        Transferencia {
            if (destino == null || destino.isBlank()) {
                throw new IllegalArgumentException("la transferencia necesita un destino");
            }
            if (monto <= 0) {
                throw new IllegalArgumentException("la transferencia tiene que ser positiva");
            }
        }
    }
}
```

### Misión R04-N03-M3 · El switch de la tarifa

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un estacionamiento cobra según el tipo de vehículo (un `enum` con `AUTO`, `MOTO`,
`CAMIONETA` y `BICI`) y las horas. Escribí `tarifa(Vehiculo v, int horas)` con un
`switch` **como expresión**, sin `default` (el compilador tiene que exigir los cuatro
casos): auto 1200 la hora, moto 600, camioneta 1800 la hora pero con un mínimo de 2
horas (usá un bloque con `yield`), bici gratis. Después generá el ticket de cada
vehículo de una lista con un **bloque de texto** y `formatted`.

#### Criterio de aprobación

- El `switch` devuelve el valor y no tiene `default`.
- Usa `yield` en el caso de la camioneta y un bloque de texto para el ticket.

#### Salida esperada

```
+----------------------+
| Patente: AB123CD     |
| AUTO         3 h     |
| Total: $3600         |
+----------------------+
+----------------------+
| Patente: A012BCD     |
| MOTO         5 h     |
| Total: $3000         |
+----------------------+
+----------------------+
| Patente: AC987ZZ     |
| CAMIONETA    1 h     |
| Total: $3600         |
+----------------------+
+----------------------+
| Patente: -           |
| BICI         8 h     |
| Total: $0            |
+----------------------+
```

#### Solución de referencia

```java
// Mision 3 - El switch de la tarifa: switch como expresion, yield y bloques de texto.
import java.util.List;

public class SwitchTarifa {
    enum Vehiculo { AUTO, MOTO, CAMIONETA, BICI }

    record Estadia(String patente, Vehiculo vehiculo, int horas) { }

    public static void main(String[] args) {
        List<Estadia> estadias = List.of(new Estadia("AB123CD", Vehiculo.AUTO, 3),
                new Estadia("A012BCD", Vehiculo.MOTO, 5), new Estadia("AC987ZZ", Vehiculo.CAMIONETA, 1),
                new Estadia("-", Vehiculo.BICI, 8));
        for (Estadia e : estadias) {
            System.out.print("""
                    +----------------------+
                    | Patente: %-11s |
                    | %-9s %4d h     |
                    | Total: $%-12d |
                    +----------------------+
                    """.formatted(e.patente(), e.vehiculo(), e.horas(), tarifa(e.vehiculo(), e.horas())));
        }
    }

    static int tarifa(Vehiculo v, int horas) {
        return switch (v) {
            case AUTO -> horas * 1200;
            case MOTO -> horas * 600;
            case CAMIONETA -> {
                int cobradas = Math.max(horas, 2);
                yield cobradas * 1800;
            }
            case BICI -> 0;
        };
    }
}
```

### Encargo R04-N03-E1 · Los pedidos de la rotisería

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una rotisería toma pedidos que pueden ser `ParaRetirar(String cliente, double total)`,
`Delivery(String cliente, String direccion, double total, int km)` o
`EnMesa(int mesa, double total, int comensales)`, todos `record` de una interfaz
sellada `Pedido`, con validaciones. Calculá lo que se cobra en cada caso con
`instanceof` con patrón (el delivery suma 500 por km, en mesa suma un cubierto de 800
por comensal) y listá los pedidos ordenados por monto a cobrar de mayor a menor, con un
comparador. Cada pedido sabe describirse (un método `etiqueta()` en la interfaz). Mostrá el total del
día.

#### Criterio de aprobación

- Jerarquía sellada con `record` validados.
- El cálculo usa `instanceof` con patrón y el orden un comparador.

#### Salida esperada

```
Mesa 4 (3 comensales)            23400.00
Delivery a Juan (3 km)           13500.00
Mesa 7 (2 comensales)            11400.00
Retira Marta                      8500.00
Delivery a Ana (1 km)             6900.00
Total del día: 63700.00
```

#### Solución de referencia

```java
// Encargo - Los pedidos de la rotiseria: sealed, records y comparadores.
import java.util.Comparator;
import java.util.List;
import java.util.Locale;

public class PedidosRotiseria {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        List<Pedido> pedidos = List.of(new ParaRetirar("Marta", 8500), new Delivery("Juan", "San Martín 450", 12000, 3),
                new EnMesa(4, 21000, 3), new Delivery("Ana", "Belgrano 12", 6400, 1), new EnMesa(7, 9800, 2));
        pedidos.stream()
                .sorted(Comparator.comparingDouble(PedidosRotiseria::aCobrar).reversed())
                .forEach(p -> System.out.printf("%-30s %10.2f%n", p.etiqueta(), aCobrar(p)));
        System.out.printf("Total del día: %.2f%n", pedidos.stream().mapToDouble(PedidosRotiseria::aCobrar).sum());
    }

    static double aCobrar(Pedido p) {
        if (p instanceof ParaRetirar r) {
            return r.total();
        } else if (p instanceof Delivery d) {
            return d.total() + d.km() * 500;
        } else if (p instanceof EnMesa m) {
            return m.total() + m.comensales() * 800;
        }
        throw new IllegalStateException("pedido desconocido");
    }

    sealed interface Pedido permits ParaRetirar, Delivery, EnMesa {
        String etiqueta();
    }

    record ParaRetirar(String cliente, double total) implements Pedido {
        ParaRetirar {
            if (total <= 0) {
                throw new IllegalArgumentException("total inválido");
            }
        }

        public String etiqueta() {
            return "Retira " + cliente;
        }
    }

    record Delivery(String cliente, String direccion, double total, int km) implements Pedido {
        Delivery {
            if (total <= 0 || km < 0) {
                throw new IllegalArgumentException("delivery inválido");
            }
        }

        public String etiqueta() {
            return "Delivery a " + cliente + " (" + km + " km)";
        }
    }

    record EnMesa(int mesa, double total, int comensales) implements Pedido {
        EnMesa {
            if (total <= 0 || comensales < 1) {
                throw new IllegalArgumentException("mesa inválida");
            }
        }

        public String etiqueta() {
            return "Mesa " + mesa + " (" + comensales + " comensales)";
        }
    }
}
```

### Prueba del sello

#### ¿Cómo ordenás por puntos de mayor a menor y, a igual puntos, por nombre?

`Comparator.comparingInt(Jugador::puntos).reversed().thenComparing(Jugador::nombre)`.

#### ¿Qué hace un constructor compacto de un `record`?

Valida o normaliza los parámetros antes de que Java los asigne a los campos.

#### ¿Para qué sirve una interfaz `sealed`?

Para limitar quiénes pueden implementarla: la jerarquía queda cerrada a las clases de `permits`.

#### ¿Qué ventaja tiene `if (x instanceof Circulo c)`?

Pregunta el tipo y declara la variable ya casteada en un solo paso.

#### ¿Cuándo hace falta `yield` en un `switch`?

Cuando un caso del `switch` como expresión es un bloque de varias líneas: `yield` indica el valor que devuelve.

### Soluciones (docente)

Los comparadores salen de `19-Java-Avanzado/06-Comparable-Comparator`; `sealed`, los patrones y los bloques de texto son nuevos de la Senda. Todo compila con Java 17: el `switch` con patrones de tipo es de Java 21 y se menciona como nota.

## R04-N04 · Patrones de diseño: Singleton, Factory y Strategy

```meta
tipo: tema
padre: R04-N03
precio: 10
criatura: ogre
temas: diseno.patrones
usa: poo.interfaces, func.lambdas
```

### Crónica

Río abajo, Zed llega al **astillero** de la capital. Los maestros constructores no inventan cada barco: usan **recetas probadas**, que se pasan de generación en generación. Hay una sola capitanía para todo el río, una fábrica que arma el barco justo según el pedido y una ruta que se cambia según el clima sin desarmar el barco.

—Vos siempre improvisabas, Zed —dice {mentor}—. Y estuvo bien: así sobreviviste. Pero los problemas que se repiten ya tienen nombre y solución. Se llaman **patrones de diseño**. Una receta conocida es otro tipo de atajo: el que todos entienden.

### Objetivos

- Entender qué es un patrón de diseño y cuándo conviene usarlo (y cuándo no).
- Asegurar una única instancia con **Singleton** y conocer sus riesgos.
- Crear objetos según un pedido con una **Factory**, sin que quien pide conozca las clases concretas.
- Cambiar un algoritmo en tiempo de ejecución con **Strategy**, con clases o con lambdas.

### Antes de empezar

- Interfaces y polimorfismo (rama 2).
- Lambdas (Lambdas, clases anónimas y referencias a métodos).
- Comparadores y el Java moderno.

### Explicación

#### Qué es un patrón
Un **patrón de diseño** es una solución conocida para un problema que aparece una y otra vez. No es una
librería ni un código para copiar: es una **forma de ordenar las clases** con un nombre que todos entienden.
Decir «acá va una Strategy» ahorra diez minutos de explicación. Los más usados en Java vienen del libro
*Design Patterns* (1994), y muchos ya están adentro del lenguaje y de los frameworks: `Comparator` es una
Strategy y Spring crea sus servicios como Singleton.

#### Singleton: uno solo
Cuando tiene que existir **una única instancia** de algo (una configuración, un registro central):
```java
final class Capitania {
    private static final Capitania INSTANCIA = new Capitania();   // se crea una sola vez

    private Capitania() { }                                       // nadie de afuera puede hacer new

    static Capitania get() {                                      // todos piden la misma
        return INSTANCIA;
    }
}
```
El constructor `private` impide el `new` desde afuera, y `get()` devuelve siempre el mismo objeto.
**Cuidado:** un Singleton es un dato global. Si guarda estado que cambia, cualquier parte del programa
lo puede tocar, y las pruebas se ensucian entre sí. Usalo poco. En Spring no se escribe así: el contenedor
crea una sola instancia de cada `@Service` y la entrega a quien la pida (lo vas a ver en la Torre).

#### Factory: que la fábrica decida
Cuando el **pedido** dice qué objeto hace falta, pero quien pide no tiene por qué conocer las clases
concretas:
```java
interface Barco { String descripcion(); }
class Barcaza implements Barco { public String descripcion() { return "barcaza de carga"; } }
class Velero implements Barco { public String descripcion() { return "velero rápido"; } }

class Fabrica {
    static Barco crear(String tipo) {
        return switch (tipo) {
            case "carga" -> new Barcaza();
            case "rapido" -> new Velero();
            default -> throw new IllegalArgumentException("no sé armar " + tipo);
        };
    }
}

Barco b = Fabrica.crear("carga");   // el que pide solo conoce la interfaz Barco
```
Si mañana se agrega un barco nuevo, cambia **un solo lugar**: la fábrica. El resto del programa sigue
hablando con `Barco`.

#### Strategy: el algoritmo que se cambia
Cuando hay **varias formas de hacer lo mismo** y se elige una en tiempo de ejecución. Cada forma es una
clase que implementa la misma interfaz, y el objeto que la usa la recibe de afuera:
```java
interface Recargo { int calcular(int dias); }
class RecargoNormal implements Recargo { public int calcular(int dias) { return dias * 10; } }
class RecargoFeria implements Recargo { public int calcular(int dias) { return dias <= 3 ? 0 : (dias - 3) * 10; } }

class Aduana {
    private Recargo recargo;                          // la estrategia activa
    Aduana(Recargo recargo) { this.recargo = recargo; }
    void setRecargo(Recargo recargo) { this.recargo = recargo; }
    int recargo(int dias) { return recargo.calcular(dias); }   // delega
}

Aduana aduana = new Aduana(new RecargoNormal());
aduana.setRecargo(new RecargoFeria());              // cambia el cálculo sin tocar Aduana
```
Como `Recargo` tiene un solo método, una estrategia también puede ser una **lambda**:
`aduana.setRecargo(dias -> dias * 5);`. `Comparator` es exactamente eso: la estrategia de orden que le
pasás a `sort`.

> **En el examen final** de la cátedra (BiblioExpress y sus variantes) se pide un cálculo que cambia según
> una configuración activa —un recargo, una tarifa, un descuento— y se espera una **Strategy**: una
> interfaz, una clase por variante y el servicio que recibe la estrategia.

#### Cuándo no usarlos
Un patrón resuelve un problema; si el problema no está, sobra. Una sola forma de calcular no necesita
Strategy, y una sola clase no necesita Factory. Primero escribí lo simple; cuando aparezca la segunda
variante, refactorizá hacia el patrón.

### Código de ejemplo

```java
/*
 * Patrones de diseño en el astillero: Singleton, Factory y Strategy.
 */
import java.util.List;

public class Astillero {
    public static void main(String[] args) {
        // Singleton: una sola capitanía para todo el río.
        Capitania.get().registrar("Barcaza 1");
        Capitania.get().registrar("Velero 2");
        System.out.println("Barcos registrados: " + Capitania.get().cantidad());
        System.out.println("¿Es la misma capitanía? " + (Capitania.get() == Capitania.get()));

        // Factory: el pedido dice qué barco; la fábrica sabe cómo armarlo.
        for (String pedido : List.of("carga", "rapido")) {
            Barco b = Fabrica.crear(pedido);
            System.out.println(pedido + " -> " + b.descripcion());
        }

        // Strategy: la ruta cambia según el clima, sin tocar el barco.
        Barco barcaza = Fabrica.crear("carga");
        barcaza.setRuta(km -> km / 10);
        System.out.println("Con buen tiempo, 120 km: " + barcaza.horas(120) + " h");
        barcaza.setRuta(km -> km / 6);
        System.out.println("Con tormenta, 120 km: " + barcaza.horas(120) + " h");
    }
}

final class Capitania {
    private static final Capitania INSTANCIA = new Capitania();
    private int registrados;

    private Capitania() { }

    static Capitania get() {
        return INSTANCIA;
    }

    void registrar(String barco) {
        registrados++;
    }

    int cantidad() {
        return registrados;
    }
}

interface Ruta {
    int horas(int km);
}

abstract class Barco {
    private Ruta ruta = km -> km / 8;

    abstract String descripcion();

    void setRuta(Ruta ruta) {
        this.ruta = ruta;
    }

    int horas(int km) {
        return ruta.horas(km);
    }
}

class Barcaza extends Barco {
    String descripcion() { return "barcaza de carga, lenta y ancha"; }
}

class Velero extends Barco {
    String descripcion() { return "velero rápido, para cartas y pasajeros"; }
}

class Fabrica {
    static Barco crear(String tipo) {
        return switch (tipo) {
            case "carga" -> new Barcaza();
            case "rapido" -> new Velero();
            default -> throw new IllegalArgumentException("no sé armar un barco de tipo " + tipo);
        };
    }
}
```

### Salida esperada

```
Barcos registrados: 2
¿Es la misma capitanía? true
carga -> barcaza de carga, lenta y ancha
rapido -> velero rápido, para cartas y pasajeros
Con buen tiempo, 120 km: 12 h
Con tormenta, 120 km: 20 h
```

### ¿Para qué sirve?

Los patrones son el vocabulario común del diseño orientado a objetos: aparecen en las entrevistas, en los exámenes y en cualquier proyecto grande. Strategy está en cada `Comparator` y en cada cálculo que cambia según una configuración; Factory, en los métodos `of` de Java (`List.of`, `Path.of`) y en los frameworks; Singleton, en los servicios de Spring. Reconocerlos te deja leer código ajeno más rápido y explicar el tuyo en una frase.

### Errores habituales

**Slime: el Singleton con constructor público.** Si el constructor no es `private`, cualquiera
hace `new` y ya hay dos. El patrón entero depende de esa palabra.

**Troll: el Singleton con estado compartido.** Un contador global en un Singleton hace que una
prueba ensucie a la siguiente y que dos partes del programa se pisen. Si tiene estado, que sea poco
y que haya una forma de reiniciarlo.

**Goblin: la Strategy con `instanceof`.** Si el que usa la estrategia pregunta
`if (recargo instanceof RecargoFeria)`, el patrón se rompió: tiene que llamar al método de la
interfaz y dejar que cada clase responda.

**Ogro: el patrón donde no hace falta.** Tres clases y una interfaz para una sola forma de
calcular es complicar por complicar. El patrón llega cuando aparece la segunda variante.

### Micro-misión R04-N04-P1 · Una sola capitanía

```meta
lugar: El astillero del río
personajes: Zed, Gheco, Nadia, Kaffa
carta: Singleton | constructor private · una instancia static final · static get() devuelve siempre la misma · nadie hace new
recompensa: xp 10, oro 10
```

#### Escena
En el astillero hay una sola capitanía para todo el río. Zed, por las dudas, intenta armarse otra propia para registrar sus barcos sin pasar por la oficial. La Aduana del compilador lo frena en seco.

#### Gheco sugiere
Un **Singleton** tiene el constructor `private`: nadie puede hacer `new` desde afuera. La única instancia se pide con `Capitania.get()`.

#### Desafío
Ejecutalo, leé el error y cambiá el `new` por la capitanía oficial.

#### Código inicial
```java
public class UnaSola {
    public static void main(String[] args) {
        Capitania oficial = Capitania.get();
        Capitania deZed = new Capitania();
        oficial.registrar("Barcaza 1");
        deZed.registrar("Velero de Zed");
        System.out.println("Registrados: " + Capitania.get().cantidad());
        System.out.println("Misma capitanía: " + (oficial == deZed));
    }
}

final class Capitania {
    private static final Capitania INSTANCIA = new Capitania();
    private int registrados;

    private Capitania() { }

    static Capitania get() { return INSTANCIA; }

    void registrar(String barco) { registrados++; }

    int cantidad() { return registrados; }
}
```

#### Salida esperada
```
Registrados: 2
Misma capitanía: true
```

#### Solución
```java
public class UnaSola {
    public static void main(String[] args) {
        Capitania oficial = Capitania.get();
        Capitania deZed = Capitania.get();
        oficial.registrar("Barcaza 1");
        deZed.registrar("Velero de Zed");
        System.out.println("Registrados: " + Capitania.get().cantidad());
        System.out.println("Misma capitanía: " + (oficial == deZed));
    }
}

final class Capitania {
    private static final Capitania INSTANCIA = new Capitania();
    private int registrados;

    private Capitania() { }

    static Capitania get() { return INSTANCIA; }

    void registrar(String barco) { registrados++; }

    int cantidad() { return registrados; }
}
```

#### Al superarla
Dos registros en la misma capitanía. —Hace un mes te hubieras armado una paralela —dice Nadia. —Hace un mes no sabía que el constructor era privado —responde Zed.

#### Imagen
- Una única capitanía de piedra sobre el astillero, con un solo libro de registros.
- Zed con un sello improvisado roto en la mano; Nadia de brazos cruzados.

### Micro-misión R04-N04-P2 · El barco del pedido

```meta
lugar: El astillero del río
personajes: Zed, Gheco, Nadia, Kaffa
carta: Factory | Fabrica.crear("carga") devuelve un Barco · quien pide solo conoce la interfaz · las clases concretas, en un solo lugar
recompensa: xp 10, oro 10
```

#### Escena
Al astillero llegan pedidos por tipo: «carga», «rápido», «pesca». El que pide no sabe armar barcos y no tiene por qué: la **fábrica** decide qué clase construir.

#### Gheco sugiere
Una **Factory** es un método que recibe el pedido y devuelve el objeto, del tipo de la interfaz: `static Barco crear(String tipo)`. Adentro, un `switch` elige la clase.

#### Desafío
Completá el caso que falta: el tipo "pesca" arma un `Pesquero`.

#### Código inicial
```java
public class Pedidos {
    public static void main(String[] args) {
        for (String pedido : new String[] {"carga", "pesca", "rapido"}) {
            System.out.println(pedido + " -> " + Fabrica.crear(pedido).descripcion());
        }
    }
}

interface Barco {
    String descripcion();
}

class Barcaza implements Barco {
    public String descripcion() { return "barcaza ancha"; }
}

class Velero implements Barco {
    public String descripcion() { return "velero rápido"; }
}

class Pesquero implements Barco {
    public String descripcion() { return "pesquero con redes"; }
}

class Fabrica {
    static Barco crear(String tipo) {
        return switch (tipo) {
            case "carga" -> new Barcaza();
            case "rapido" -> new Velero();
            ___
            default -> throw new IllegalArgumentException("no sé armar " + tipo);
        };
    }
}
```

#### Salida esperada
```
carga -> barcaza ancha
pesca -> pesquero con redes
rapido -> velero rápido
```

#### Solución
```java
public class Pedidos {
    public static void main(String[] args) {
        for (String pedido : new String[] {"carga", "pesca", "rapido"}) {
            System.out.println(pedido + " -> " + Fabrica.crear(pedido).descripcion());
        }
    }
}

interface Barco {
    String descripcion();
}

class Barcaza implements Barco {
    public String descripcion() { return "barcaza ancha"; }
}

class Velero implements Barco {
    public String descripcion() { return "velero rápido"; }
}

class Pesquero implements Barco {
    public String descripcion() { return "pesquero con redes"; }
}

class Fabrica {
    static Barco crear(String tipo) {
        return switch (tipo) {
            case "carga" -> new Barcaza();
            case "rapido" -> new Velero();
            case "pesca" -> new Pesquero();
            default -> throw new IllegalArgumentException("no sé armar " + tipo);
        };
    }
}
```

#### Al superarla
Tres pedidos, tres barcos, y el `main` no hizo un solo `new Barcaza()`. Si mañana hay un barco nuevo, cambia un solo lugar.

#### Imagen
- La fábrica del astillero: una grúa de bronce armando un pesquero con redes según un pedido escrito.
- Un maestro constructor leyendo la lista de pedidos.

### Micro-misión R04-N04-P3 · La tarifa de feria

```meta
lugar: La capitanía del astillero
personajes: Zed, Gheco, Nadia, Kaffa
carta: Strategy | interface Recargo { int calcular(int dias); } · una clase por forma de calcular · la Aduana recibe la que toque y delega
recompensa: xp 15, oro 15
```

#### Escena
Los barcos que se demoran en el astillero pagan un recargo, y la forma de calcularlo cambia según la época. En feria, los primeros 3 días son gratis. —Esto es lo que te van a pedir en el examen —le dice Kaffa a Zed, que no sabía que iba a haber un examen.

#### Gheco sugiere
Cada forma de calcular es una clase que implementa `Recargo`. La `Aduana` no pregunta cuál es: llama a `recargo.calcular(dias)`. En feria: si los días son 3 o menos, 0; si no, 10 por cada día después del tercero.

#### Desafío
Completá el `return` de `RecargoFeria`.

#### Código inicial
```java
public class Feria {
    public static void main(String[] args) {
        Aduana aduana = new Aduana(new RecargoNormal());
        System.out.println("Normal, 5 días: " + aduana.recargo(5));
        aduana.setRecargo(new RecargoFeria());
        System.out.println("Feria, 2 días: " + aduana.recargo(2));
        System.out.println("Feria, 5 días: " + aduana.recargo(5));
    }
}

interface Recargo {
    int calcular(int dias);
}

class RecargoNormal implements Recargo {
    public int calcular(int dias) { return dias * 10; }
}

class RecargoFeria implements Recargo {
    public int calcular(int dias) {
        return ___;
    }
}

class Aduana {
    private Recargo recargo;

    Aduana(Recargo recargo) { this.recargo = recargo; }

    void setRecargo(Recargo recargo) { this.recargo = recargo; }

    int recargo(int dias) { return recargo.calcular(dias); }
}
```

#### Salida esperada
```
Normal, 5 días: 50
Feria, 2 días: 0
Feria, 5 días: 20
```

#### Solución
```java
public class Feria {
    public static void main(String[] args) {
        Aduana aduana = new Aduana(new RecargoNormal());
        System.out.println("Normal, 5 días: " + aduana.recargo(5));
        aduana.setRecargo(new RecargoFeria());
        System.out.println("Feria, 2 días: " + aduana.recargo(2));
        System.out.println("Feria, 5 días: " + aduana.recargo(5));
    }
}

interface Recargo {
    int calcular(int dias);
}

class RecargoNormal implements Recargo {
    public int calcular(int dias) { return dias * 10; }
}

class RecargoFeria implements Recargo {
    public int calcular(int dias) {
        return dias <= 3 ? 0 : (dias - 3) * 10;
    }
}

class Aduana {
    private Recargo recargo;

    Aduana(Recargo recargo) { this.recargo = recargo; }

    void setRecargo(Recargo recargo) { this.recargo = recargo; }

    int recargo(int dias) { return recargo.calcular(dias); }
}
```

#### Al superarla
Cincuenta en época normal, veinte en feria, y la Aduana no tiene un solo `if` sobre la época. —¿Examen? —pregunta Zed. —Al final de la Torre —dice Kaffa, y no agrega nada.

#### Imagen
- Dos tablillas de tarifas colgadas en la capitanía: «Normal» y «Feria», intercambiables en el mismo gancho.
- Kaffa tomando café; Zed preocupado por la palabra «examen».

### Micro-misión R04-N04-P4 · La estrategia en una línea

```meta
lugar: La capitanía del astillero
personajes: Zed, Gheco, Nadia, Kaffa
carta: Strategy con lambda | si la interfaz tiene un solo método, la estrategia puede ser una lambda · aduana.setRecargo(dias -> dias * 5)
recompensa: xp 15, oro 20
```

#### Escena
Para la noche de la crecida, la capitanía decide un recargo especial que se usa una sola vez: 5 por día. Escribir una clase entera para eso es demasiado. —`Recargo` tiene un solo método —dice Gheco—. Ya sabés qué significa.

#### Gheco sugiere
Como `Recargo` tiene **un solo** método, cualquier lambda `dias -> …` sirve como estrategia. Es lo mismo que hacés con `Comparator` cuando ordenás.

#### Desafío
Completá la lambda del recargo de la crecida: 5 por día.

#### Código inicial
```java
public class Crecida {
    public static void main(String[] args) {
        Aduana aduana = new Aduana(dias -> dias * 10);
        System.out.println("Normal, 4 días: " + aduana.recargo(4));
        aduana.setRecargo(dias -> ___);
        System.out.println("Crecida, 4 días: " + aduana.recargo(4));
    }
}

interface Recargo {
    int calcular(int dias);
}

class Aduana {
    private Recargo recargo;

    Aduana(Recargo recargo) { this.recargo = recargo; }

    void setRecargo(Recargo recargo) { this.recargo = recargo; }

    int recargo(int dias) { return recargo.calcular(dias); }
}
```

#### Salida esperada
```
Normal, 4 días: 40
Crecida, 4 días: 20
```

#### Solución
```java
public class Crecida {
    public static void main(String[] args) {
        Aduana aduana = new Aduana(dias -> dias * 10);
        System.out.println("Normal, 4 días: " + aduana.recargo(4));
        aduana.setRecargo(dias -> dias * 5);
        System.out.println("Crecida, 4 días: " + aduana.recargo(4));
    }
}

interface Recargo {
    int calcular(int dias);
}

class Aduana {
    private Recargo recargo;

    Aduana(Recargo recargo) { this.recargo = recargo; }

    void setRecargo(Recargo recargo) { this.recargo = recargo; }

    int recargo(int dias) { return recargo.calcular(dias); }
}
```

#### Al superarla
Una estrategia de una línea, para una sola noche. Zed se da cuenta de que lleva semanas usando patrones sin saberlo: cada `Comparator` era una Strategy.
Río abajo, las esclusas no dan abasto: hay que abrir varias **a la vez**.

#### Imagen
- Una tablilla de tarifa escrita a mano, en una sola línea, colgada sobre las otras.
- Al fondo, las esclusas del río con una fila larguísima de barcazas esperando.

### Misión R04-N04-M1 · La capitanía única

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

En el río hay varios muelles, pero **una sola capitanía** que lleva la cuenta de todas las
zarpadas. Escribí la clase `Capitania` como **Singleton** (constructor privado, una instancia
`static final` y un método `get()`), con `registrar(String muelle, String barco)`,
`zarpadas()` y `ultima()`. Escribí también la clase `Muelle`: cada muelle tiene su nombre y su
método `zarpa(String barco)`, que avisa a la capitanía y muestra el mensaje.

En el `main`, creá los muelles **norte** y **sur**, hacé zarpar a `Barcaza 1` (norte),
`Velero 2` (sur) y `Barcaza 3` (norte), y mostrá las zarpadas, la última y si
`Capitania.get() == Capitania.get()`.

#### Criterio de aprobación

- `Capitania` tiene el constructor `private` y se obtiene solo con `get()`.
- Los muelles no reciben la capitanía por parámetro: la piden con `get()`.
- La salida coincide con la esperada.

#### Salida esperada

```
Barcaza 1 zarpa del muelle norte
Velero 2 zarpa del muelle sur
Barcaza 3 zarpa del muelle norte
Zarpadas en el río: 3
Última: Barcaza 3 desde el muelle norte
Misma capitanía: true
```

#### Solución de referencia

```java
// Mision 1 - La capitanía única: Singleton.
public class CapitaniaUnica {
    public static void main(String[] args) {
        Muelle norte = new Muelle("norte");
        Muelle sur = new Muelle("sur");
        norte.zarpa("Barcaza 1");
        sur.zarpa("Velero 2");
        norte.zarpa("Barcaza 3");
        System.out.println("Zarpadas en el río: " + Capitania.get().zarpadas());
        System.out.println("Última: " + Capitania.get().ultima());
        System.out.println("Misma capitanía: " + (Capitania.get() == Capitania.get()));
    }
}

final class Capitania {
    private static final Capitania INSTANCIA = new Capitania();
    private int zarpadas;
    private String ultima = "ninguna";

    private Capitania() { }

    static Capitania get() {
        return INSTANCIA;
    }

    void registrar(String muelle, String barco) {
        zarpadas++;
        ultima = barco + " desde el muelle " + muelle;
    }

    int zarpadas() { return zarpadas; }

    String ultima() { return ultima; }
}

class Muelle {
    private final String nombre;

    Muelle(String nombre) { this.nombre = nombre; }

    void zarpa(String barco) {
        Capitania.get().registrar(nombre, barco);
        System.out.println(barco + " zarpa del muelle " + nombre);
    }
}
```

### Misión R04-N04-M2 · La fábrica del astillero

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El astillero recibe pedidos por tipo: `carga`, `rapido`, `pesca`. Declará la interfaz `Barco`
(`nombre()` y `capacidad()`) y tres implementaciones: `Barcaza` (120), `Velero` (10) y
`Pesquero` (30). Pueden ser `record`. Escribí `Fabrica.crear(String tipo)`, que devuelve el barco
que corresponde y, para un tipo desconocido, lanza `IllegalArgumentException` con el mensaje
`el astillero no arma «tipo»`.

En el `main`, procesá los pedidos `carga`, `rapido`, `pesca` y `submarino` y mostrá cada
resultado con `printf("%-9s -> …")`, sin que el programa se corte con el último.

#### Criterio de aprobación

- El `main` solo conoce la interfaz `Barco` y la `Fabrica`: no hace `new Barcaza()` ni pregunta tipos.
- El tipo desconocido se maneja con la excepción, sin cortar el programa.
- La salida coincide con la esperada.

#### Salida esperada

```
carga     -> Barcaza (capacidad 120)
rapido    -> Velero (capacidad 10)
pesca     -> Pesquero (capacidad 30)
submarino -> el astillero no arma «submarino»
```

#### Solución de referencia

```java
// Mision 2 - La fábrica del astillero: Factory.
import java.util.List;

public class FabricaAstillero {
    public static void main(String[] args) {
        for (String pedido : List.of("carga", "rapido", "pesca", "submarino")) {
            try {
                Barco b = Fabrica.crear(pedido);
                System.out.printf("%-9s -> %s (capacidad %d)%n", pedido, b.nombre(), b.capacidad());
            } catch (IllegalArgumentException e) {
                System.out.printf("%-9s -> %s%n", pedido, e.getMessage());
            }
        }
    }
}

interface Barco {
    String nombre();

    int capacidad();
}

record Barcaza() implements Barco {
    public String nombre() { return "Barcaza"; }

    public int capacidad() { return 120; }
}

record Velero() implements Barco {
    public String nombre() { return "Velero"; }

    public int capacidad() { return 10; }
}

record Pesquero() implements Barco {
    public String nombre() { return "Pesquero"; }

    public int capacidad() { return 30; }
}

class Fabrica {
    static Barco crear(String tipo) {
        return switch (tipo) {
            case "carga" -> new Barcaza();
            case "rapido" -> new Velero();
            case "pesca" -> new Pesquero();
            default -> throw new IllegalArgumentException("el astillero no arma «" + tipo + "»");
        };
    }
}
```

### Misión R04-N04-M3 · El recargo por demora

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La Aduana cobra un recargo por cada día de demora, y la forma de calcularlo cambia según la época.
Declará la interfaz `Recargo` con `int calcular(int dias)` y tres estrategias:

- `RecargoNormal`: 10 denarios por día.
- `RecargoFeria`: los primeros 3 días son gratis; después, 10 por día.
- `RecargoNocturno`: 0 si no hay demora; si hay, 20 fijos más 15 por día.

La clase `Aduana` recibe la estrategia en el constructor, la puede cambiar con `setRecargo` y
calcula con `recargo(int dias)`. En el `main`, mostrá el recargo de 0, 3 y 10 días con cada
estrategia, cambiándola en la **misma** aduana.

#### Criterio de aprobación

- `Aduana` no tiene ningún `if` ni `switch` sobre el tipo de recargo: delega en la estrategia.
- Se usa una sola `Aduana` y se cambia la estrategia con `setRecargo`.
- La salida coincide con la esperada.

#### Salida esperada

```
Recargo normal:
   0 días -> 0 denarios
   3 días -> 30 denarios
  10 días -> 100 denarios
Recargo feria:
   0 días -> 0 denarios
   3 días -> 0 denarios
  10 días -> 70 denarios
Recargo nocturno:
   0 días -> 0 denarios
   3 días -> 65 denarios
  10 días -> 170 denarios
```

#### Solución de referencia

```java
// Mision 3 - El recargo por demora: Strategy.
public class RecargoDemora {
    public static void main(String[] args) {
        Aduana aduana = new Aduana(new RecargoNormal());
        mostrar(aduana, "normal");
        aduana.setRecargo(new RecargoFeria());
        mostrar(aduana, "feria");
        aduana.setRecargo(new RecargoNocturno());
        mostrar(aduana, "nocturno");
    }

    static void mostrar(Aduana aduana, String nombre) {
        System.out.println("Recargo " + nombre + ":");
        for (int dias : new int[] {0, 3, 10}) {
            System.out.printf("  %2d días -> %d denarios%n", dias, aduana.recargo(dias));
        }
    }
}

interface Recargo {
    int calcular(int dias);
}

class RecargoNormal implements Recargo {
    public int calcular(int dias) { return dias * 10; }
}

class RecargoFeria implements Recargo {
    public int calcular(int dias) { return dias <= 3 ? 0 : (dias - 3) * 10; }
}

class RecargoNocturno implements Recargo {
    public int calcular(int dias) { return dias == 0 ? 0 : 20 + dias * 15; }
}

class Aduana {
    private Recargo recargo;

    Aduana(Recargo recargo) { this.recargo = recargo; }

    void setRecargo(Recargo recargo) { this.recargo = recargo; }

    int recargo(int dias) { return recargo.calcular(dias); }
}
```

### Encargo R04-N04-E1 · La ruta según el clima

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Las rutas del río dependen del clima. Guardá las estrategias en un `Map<String, Ruta>`
(con `LinkedHashMap`), escritas como **lambdas**: con `sol`, `km / 10` horas; con `viento`,
`km / 8`; con `tormenta`, `km / 5 + 2`. Escribí `elegir(String clima)`, que devuelve la
estrategia o lanza `IllegalArgumentException("clima desconocido: …")`.

Mostrá cuántas horas lleva recorrer 120 km con `sol`, `viento`, `tormenta` y `niebla`.

#### Criterio de aprobación

- Las estrategias son lambdas guardadas en un mapa: agregar un clima es agregar una línea.
- El clima desconocido se maneja con la excepción.
- La salida coincide con la esperada.

#### Salida esperada

```
sol      120 km -> 12 h
viento   120 km -> 15 h
tormenta 120 km -> 26 h
niebla   clima desconocido: niebla
```

#### Solución de referencia

```java
// Encargo 1 - La ruta según el clima: Strategy con lambdas y un mapa de estrategias.
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class RutaClima {
    interface Ruta {
        int horas(int km);
    }

    static final Map<String, Ruta> RUTAS = new LinkedHashMap<>();

    static {
        RUTAS.put("sol", km -> km / 10);
        RUTAS.put("viento", km -> km / 8);
        RUTAS.put("tormenta", km -> km / 5 + 2);
    }

    static Ruta elegir(String clima) {
        Ruta r = RUTAS.get(clima);
        if (r == null) {
            throw new IllegalArgumentException("clima desconocido: " + clima);
        }
        return r;
    }

    public static void main(String[] args) {
        for (String clima : List.of("sol", "viento", "tormenta", "niebla")) {
            try {
                System.out.printf("%-8s 120 km -> %d h%n", clima, elegir(clima).horas(120));
            } catch (IllegalArgumentException e) {
                System.out.printf("%-8s %s%n", clima, e.getMessage());
            }
        }
    }
}
```

### Prueba del sello

#### ¿Qué es un patrón de diseño?

Una solución conocida, con nombre, para un problema de diseño que aparece una y otra vez. No es código para copiar: es una forma de ordenar las clases.

#### ¿Qué dos cosas hacen falta para que una clase sea un Singleton?

Un constructor `private` (nadie hace `new` desde afuera) y un método `static` que devuelve siempre la misma instancia.

#### ¿Qué gana el programa con una Factory?

Que quien pide un objeto solo conoce la interfaz: las clases concretas se eligen en un solo lugar, y agregar una nueva no cambia al resto.

#### ¿Cómo sabés que un problema pide una Strategy?

Cuando hay varias formas de calcular o hacer lo mismo y se elige una en tiempo de ejecución (por configuración, por época, por el usuario).

#### ¿Por qué `Comparator` es una Strategy?

Porque es una interfaz de un método que encapsula **cómo** comparar: `sort` la recibe de afuera y la usa sin saber cuál es.

### Soluciones (docente)

Nodo nuevo (D96): el programa de la cátedra pide patrones en la unidad 2 y el examen final usa Strategy. Las misiones corren con `java Archivo.java`; en la M3 conviene preguntar en clase por qué `Aduana` no tiene ningún `if`. Singleton se presenta con sus riesgos: en la Torre (Spring) los servicios ya son únicos sin escribir el patrón.

## R04-N05 · Concurrencia: muchas corrientes a la vez

```meta
tipo: tema
padre: R04-N04
precio: 10
criatura: orc
temas: conc.hilos, conc.sincronizacion
```

### Crónica

Río abajo están las **esclusas**: una sola no da abasto y la fila de barcazas llega hasta el astillero. Hay que abrir varias **a la vez** sin que las barcazas choquen, y hay un solo libro de registro para todas. Cuando dos esclusas anotan al mismo tiempo en el libro, los números no cierran.

—Tu computadora tiene varios núcleos, Zed, y hasta ahora usaste uno solo —dice {mentor}—. Con **hilos** podés hacer muchas cosas a la vez. Pero cuando varios tocan lo mismo, aparecen los errores más difíciles de encontrar. Vos siempre trabajaste solo; ahora toca **repartir el trabajo y compartir lo menos posible**.

### Objetivos

- Entender qué es un hilo y por qué la concurrencia es difícil.
- Repartir tareas con `ExecutorService` y recoger sus resultados con `Future`.
- Proteger datos compartidos con `synchronized` y las clases atómicas.
- Encadenar tareas asíncronas con `CompletableFuture`.

### Antes de empezar

- Comparadores y el Java moderno.

### Explicación

#### Hilos
Un **hilo** (*thread*) es una línea de ejecución. Un programa arranca con uno (el del
`main`) y puede crear más, que corren **a la vez** (en paralelo si hay varios núcleos).
El orden en que avanzan los hilos **no está garantizado**: dos ejecuciones del mismo
programa pueden mezclar sus pasos distinto.

Crear hilos a mano (`new Thread(...)`) se usa poco: se trabaja con un **pool** de hilos
que reparte las tareas.

#### `ExecutorService`: el capataz del puerto
```java
ExecutorService pool = Executors.newFixedThreadPool(4);       // 4 hilos trabajando
Future<Integer> f = pool.submit(() -> calcularAlgo());         // una tarea que devuelve algo
int resultado = f.get();                                       // espera y trae el resultado
pool.shutdown();                                               // no acepta más tareas
```
- `submit(Callable)` devuelve un **`Future`**: la promesa de un resultado. `get()` espera
  hasta que esté.
- `invokeAll(lista de tareas)` las lanza todas y devuelve los `Future` **en el mismo
  orden** en que las pasaste: aunque terminen desordenadas, los resultados se leen en
  orden.
- Siempre `shutdown()` al final (o usá el pool en un `try` con recursos en Java 19+),
  si no el programa no termina.

#### La condición de carrera
Si dos hilos hacen `contador++` sobre la misma variable, a veces se pierden sumas:
`contador++` son **tres pasos** (leer, sumar, escribir) y los hilos se pisan. Mil sumas
de cuatro hilos pueden dar 3 871 en lugar de 4 000, y otra vez 3 950. Es una
**condición de carrera**: el error aparece o no según el azar.

Soluciones, de la más simple a la más fina:
| Herramienta | Uso |
|---|---|
| no compartir | cada tarea calcula lo suyo y se suman los resultados al final |
| `AtomicInteger`, `AtomicLong` | contadores seguros: `incrementAndGet()`, `addAndGet(n)` |
| `synchronized` | un método o bloque que solo un hilo a la vez puede ejecutar |
| `ConcurrentHashMap` | un mapa que varios hilos pueden modificar (`merge`) |

#### `CompletableFuture`: tareas encadenadas
Para tareas que dependen unas de otras, sin bloquear esperando cada una:
```java
CompletableFuture<Double> precio = CompletableFuture.supplyAsync(() -> buscarPrecio("yerba"));
CompletableFuture<Double> cotizacion = CompletableFuture.supplyAsync(() -> buscarCotizacion());
double enDolares = precio.thenCombine(cotizacion, (p, c) -> p / c).join();
```
| Método | Hace |
|---|---|
| `supplyAsync(() -> …)` | arranca una tarea en otro hilo |
| `thenApply(f)` | transforma el resultado cuando esté |
| `thenCombine(otra, f)` | combina dos resultados |
| `exceptionally(e -> …)` | un valor alternativo si algo falló |
| `join()` | espera el resultado final |
| `allOf(…)` | espera a que terminen varias |

#### Streams paralelos
`lista.parallelStream()` reparte un stream entre varios hilos. Sirve para cálculos
grandes y sin efectos secundarios (sumar, contar, transformar); con operaciones que
tocan datos compartidos, trae las mismas carreras que los hilos a mano.

#### Hacer programas concurrentes verificables
Como el orden de los hilos cambia, un programa concurrente **no debe imprimir desde los
hilos** si su salida tiene que ser siempre la misma: los hilos calculan y devuelven, y el
`main` imprime en orden. Así lo hacen los ejemplos de este nodo.

> **Si venís de Python.** `ExecutorService` es el `concurrent.futures.ThreadPoolExecutor`
> de Python, y `CompletableFuture` se parece a `asyncio` con `await`. En Java los hilos
> sí corren en paralelo en varios núcleos.

### Código de ejemplo

```java
/*
 * Concurrencia: el puerto con muchos estibadores.
 * Los hilos calculan; el main imprime en orden (la salida es siempre la misma).
 */
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.Callable;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.LongStream;

public class PuertoConcurrente {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        Locale.setDefault(Locale.US);
        ExecutorService pool = Executors.newFixedThreadPool(4);

        // 1. Repartir: cada muelle cuenta los primos de su tramo, y se suman al final
        List<Callable<Long>> tramos = new ArrayList<>();
        for (int i = 0; i < 4; i++) {
            long desde = i * 50_000L + 1;
            long hasta = (i + 1) * 50_000L;
            tramos.add(() -> LongStream.rangeClosed(desde, hasta).filter(PuertoConcurrente::esPrimo).count());
        }
        List<Future<Long>> resultados = pool.invokeAll(tramos);
        long total = 0;
        for (int i = 0; i < resultados.size(); i++) {
            long primos = resultados.get(i).get();
            System.out.println("Muelle " + (i + 1) + ": " + primos + " primos");
            total += primos;
        }
        System.out.println("Primos hasta 200000: " + total);

        // 2. Un contador compartido, seguro con AtomicInteger
        AtomicInteger cajas = new AtomicInteger();
        List<Callable<Void>> estibadores = new ArrayList<>();
        for (int i = 0; i < 4; i++) {
            estibadores.add(() -> {
                for (int c = 0; c < 10_000; c++) {
                    cajas.incrementAndGet();
                }
                return null;
            });
        }
        pool.invokeAll(estibadores);
        System.out.println("Cajas descargadas (AtomicInteger): " + cajas.get());

        // 3. Lo mismo con un método synchronized
        Libro libro = new Libro();
        List<Callable<Void>> escribientes = new ArrayList<>();
        for (int i = 0; i < 4; i++) {
            escribientes.add(() -> {
                for (int c = 0; c < 10_000; c++) {
                    libro.anotar();
                }
                return null;
            });
        }
        pool.invokeAll(escribientes);
        System.out.println("Anotaciones en el libro (synchronized): " + libro.total());
        pool.shutdown();

        // 4. CompletableFuture: dos consultas a la vez, combinadas
        CompletableFuture<Double> precio = CompletableFuture.supplyAsync(() -> consultar("precio de la carga", 185_000.0));
        CompletableFuture<Double> cotizacion = CompletableFuture.supplyAsync(() -> consultar("cotización", 1_250.0));
        double enDolares = precio.thenCombine(cotizacion, (p, c) -> p / c).join();
        System.out.printf("La carga vale %.2f dólares%n", enDolares);

        CompletableFuture<Double> fallida = CompletableFuture
                .supplyAsync(() -> consultar("seguro", -1))
                .exceptionally(e -> 0.0);
        System.out.println("Seguro (con error): " + fallida.join());

        // 5. Stream paralelo: el mismo resultado, repartido
        System.out.println("Suma de cuadrados en paralelo: " + LongStream.rangeClosed(1, 1_000_000).parallel().map(n -> n * n).sum());
    }

    static boolean esPrimo(long n) {
        if (n < 2) {
            return false;
        }
        for (long d = 2; d * d <= n; d++) {
            if (n % d == 0) {
                return false;
            }
        }
        return true;
    }

    static double consultar(String que, double valor) {
        try {
            Thread.sleep(100);                  // simula la demora de una consulta
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        if (valor < 0) {
            throw new IllegalStateException("no se pudo consultar " + que);
        }
        return valor;
    }

    static class Libro {
        private int anotaciones;

        synchronized void anotar() {
            anotaciones++;
        }

        synchronized int total() {
            return anotaciones;
        }
    }
}
```

### Salida esperada

```
Muelle 1: 5133 primos
Muelle 2: 4459 primos
Muelle 3: 4256 primos
Muelle 4: 4136 primos
Primos hasta 200000: 17984
Cajas descargadas (AtomicInteger): 40000
Anotaciones en el libro (synchronized): 40000
La carga vale 148.00 dólares
Seguro (con error): 0.0
Suma de cuadrados en paralelo: 333333833333500000
```

### ¿Para qué sirve?

Un servidor web atiende a cientos de usuarios a la vez: cada pedido en su hilo (Spring lo hace por vos en la tercera Senda). Una aplicación consulta varias APIs y combina las respuestas; un proceso de datos reparte un archivo enorme entre los núcleos. Entender las carreras y cómo evitarlas es lo que separa un programa que "a veces falla" de uno confiable.

### Errores habituales

**Dragón: la condición de carrera.** Un `contador++` o un `lista.add` compartido entre
hilos sin protección. El programa anda "casi siempre" y falla en producción. Usá
atómicos, `synchronized` o, mejor, no compartas.

**Ogro: el pool sin `shutdown`.** El programa termina el `main` y queda colgado: los
hilos del pool siguen esperando tareas.

**Troll: `get()` dentro del bucle que lanza.** Lanzar una tarea y hacer `get()` enseguida,
una por una, las ejecuta de a una: no hay paralelismo. Primero lanzá todas, después
recogé los resultados.

**Goblin: imprimir desde los hilos.** Las líneas salen en un orden distinto cada vez. Que
los hilos devuelvan y el `main` imprima.

**Ogro: `ExecutionException` escondida.** Si una tarea lanza una excepción, `get()` la
envuelve en una `ExecutionException`: la causa real está en `e.getCause()`.

**Troll: el `ArrayList` compartido.** `ArrayList` y `HashMap` no son seguros entre hilos.
Usá `ConcurrentHashMap`, `Collections.synchronizedList` o, mejor, que cada tarea devuelva
su lista.

### Micro-misión R04-N05-P1 · Dos esclusas a la vez

```meta
lugar: Las esclusas del río
personajes: Zed, Gheco, Nadia, Kaffa
carta: Thread y join | new Thread(() -> …).start() arranca otra corriente · t.join() espera a que termine · sin join, el main no espera
recompensa: xp 10, oro 10
```

#### Escena
Una sola esclusa no da abasto. Kaffa abre dos **a la vez**, cada una con su fila de barcazas. Zed, que siempre trabajó solo, tiene que aprender a **repartir el trabajo**… y a esperar que todos terminen antes de cantar el total.

#### Gheco sugiere
Un `Thread` corre una tarea en paralelo: `new Thread(() -> …)` y `start()`. `join()` hace que el `main` **espere** a que ese hilo termine. Cada esclusa guarda su resultado en su propio lugar del array: no se pisan.

#### Desafío
Completá el método que espera a que cada esclusa termine.

#### Código inicial
```java
public class Esclusas {
    public static void main(String[] args) throws InterruptedException {
        int[][] filas = {{80, 20, 120}, {50, 40, 60, 30}};
        int[] totales = new int[2];
        Thread[] esclusas = new Thread[2];
        for (int i = 0; i < 2; i++) {
            int n = i;
            esclusas[i] = new Thread(() -> {
                for (int carga : filas[n]) {
                    totales[n] += carga;
                }
            });
            esclusas[i].start();
        }
        for (Thread t : esclusas) {
            t.___();
        }
        System.out.println("Esclusa 1: " + totales[0]);
        System.out.println("Esclusa 2: " + totales[1]);
        System.out.println("Total del día: " + (totales[0] + totales[1]));
    }
}
```

#### Salida esperada
```
Esclusa 1: 220
Esclusa 2: 180
Total del día: 400
```

#### Solución
```java
public class Esclusas {
    public static void main(String[] args) throws InterruptedException {
        int[][] filas = {{80, 20, 120}, {50, 40, 60, 30}};
        int[] totales = new int[2];
        Thread[] esclusas = new Thread[2];
        for (int i = 0; i < 2; i++) {
            int n = i;
            esclusas[i] = new Thread(() -> {
                for (int carga : filas[n]) {
                    totales[n] += carga;
                }
            });
            esclusas[i].start();
        }
        for (Thread t : esclusas) {
            t.join();
        }
        System.out.println("Esclusa 1: " + totales[0]);
        System.out.println("Esclusa 2: " + totales[1]);
        System.out.println("Total del día: " + (totales[0] + totales[1]));
    }
}
```

#### Al superarla
Las dos esclusas terminan y recién ahí se canta el total: 400. —Si cantabas antes —dice Kaffa—, decías cualquier cosa. Esperar también es parte del trabajo.

#### Imagen
- Dos esclusas de piedra abiertas a la vez, con dos filas de barcazas pasando.
- Zed con un reloj de arena en la mano, esperando; Kaffa a su lado.

### Micro-misión R04-N05-P2 · El capataz de las esclusas

```meta
lugar: Las esclusas del río
personajes: Zed, Gheco, Nadia, Kaffa
carta: ExecutorService y Future | pool.submit(() -> valor) devuelve un Future · f.get() espera y da el resultado · pool.shutdown() al final
recompensa: xp 15, oro 15
```

#### Escena
Crear un hilo para cada barcaza es un lío. El capataz de las esclusas tiene **dos ayudantes fijos** y les va pasando tareas; cada tarea le deja un **recibo** para retirar el resultado cuando esté listo.

#### Gheco sugiere
Un `ExecutorService` es un capataz con hilos fijos: `Executors.newFixedThreadPool(2)`. `submit(() -> valor)` le pasa una tarea y devuelve un `Future` (el recibo). `f.get()` espera y devuelve el resultado. Al final, `shutdown()`.

#### Desafío
Completá el método del recibo que espera y devuelve el resultado.

#### Código inicial
```java
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class Capataz {
    public static void main(String[] args) throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(2);
        List<Future<Integer>> recibos = new ArrayList<>();
        for (int carga : new int[] {80, 20, 120}) {
            recibos.add(pool.submit(() -> carga / 2));
        }
        int i = 1;
        for (Future<Integer> f : recibos) {
            System.out.println("Peaje de la barcaza " + i++ + ": " + f.___());
        }
        pool.shutdown();
    }
}
```

#### Salida esperada
```
Peaje de la barcaza 1: 40
Peaje de la barcaza 2: 10
Peaje de la barcaza 3: 60
```

#### Solución
```java
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class Capataz {
    public static void main(String[] args) throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(2);
        List<Future<Integer>> recibos = new ArrayList<>();
        for (int carga : new int[] {80, 20, 120}) {
            recibos.add(pool.submit(() -> carga / 2));
        }
        int i = 1;
        for (Future<Integer> f : recibos) {
            System.out.println("Peaje de la barcaza " + i++ + ": " + f.get());
        }
        pool.shutdown();
    }
}
```

#### Al superarla
Tres recibos, tres peajes, retirados en orden aunque los ayudantes hayan terminado en cualquier orden. El capataz cierra la ventanilla.

#### Imagen
- Un capataz en una casilla de las esclusas entregando recibos de papel; dos ayudantes trabajando atrás.
- Una pila de recibos con números.

### Micro-misión R04-N05-P3 · El contador que pierde barcazas

```meta
lugar: Las esclusas del río
personajes: Zed, Gheco, Nadia, Kaffa
criatura: orco
carta: synchronized | dos hilos que hacen contador++ a la vez pierden cuentas (condición de carrera) · synchronized deja entrar de a uno
recompensa: xp 15, oro 15
```

#### Escena
Las dos esclusas anotan en el **mismo** contador. Al final del día, faltan barcazas: cuando las dos suman a la vez, una cuenta se pisa con la otra. Un **orco** se ríe en la casilla: es la condición de carrera.

#### Gheco sugiere
`total++` parece una sola cosa, pero son tres: leer, sumar y guardar. Si dos hilos lo hacen a la vez, se pierden sumas. Un método `synchronized` deja entrar **de a un hilo por vez**.

#### Desafío
Completá la palabra que hace que `sumar` atienda de a un hilo por vez.

#### Código inicial
```java
public class Contador {
    public static void main(String[] args) throws InterruptedException {
        Casilla casilla = new Casilla();
        Runnable esclusa = () -> {
            for (int i = 0; i < 100000; i++) {
                casilla.sumar();
            }
        };
        Thread a = new Thread(esclusa);
        Thread b = new Thread(esclusa);
        a.start();
        b.start();
        a.join();
        b.join();
        System.out.println("Barcazas contadas: " + casilla.total());
    }
}

class Casilla {
    private int total;

    ___ void sumar() {
        total++;
    }

    int total() {
        return total;
    }
}
```

#### Salida esperada
```
Barcazas contadas: 200000
```

#### Solución
```java
public class Contador {
    public static void main(String[] args) throws InterruptedException {
        Casilla casilla = new Casilla();
        Runnable esclusa = () -> {
            for (int i = 0; i < 100000; i++) {
                casilla.sumar();
            }
        };
        Thread a = new Thread(esclusa);
        Thread b = new Thread(esclusa);
        a.start();
        b.start();
        a.join();
        b.join();
        System.out.println("Barcazas contadas: " + casilla.total());
    }
}

class Casilla {
    private int total;

    synchronized void sumar() {
        total++;
    }

    int total() {
        return total;
    }
}
```

#### Al superarla
Doscientas mil, exactas. El orco sale de la casilla: con una puerta para uno, ya no puede meterse entre dos cuentas. —Lo compartido se cuida —dice Kaffa—. Es lo que más cuesta aprender.

#### Imagen
- Una casilla con una puerta angosta por la que pasa un solo hilo de luz a la vez.
- Un orco expulsado de la casilla, con un ábaco roto.

### Micro-misión R04-N05-P4 · Dos presupuestos, una respuesta

```meta
lugar: Las esclusas del río
personajes: Zed, Gheco, Nadia, Kaffa
carta: CompletableFuture | supplyAsync(() -> …) arranca una tarea · thenCombine(otra, Integer::sum) junta dos resultados · join() espera el final
recompensa: xp 15, oro 20
```

#### Escena
Para reparar la esclusa grande hacen falta dos presupuestos: el de la madera y el de las piedras. Se piden **a la vez**, y cuando estén los dos, se suman.

#### Gheco sugiere
`CompletableFuture.supplyAsync(() -> valor)` arranca una tarea en otro hilo. `a.thenCombine(b, Integer::sum)` arma una tarea que, cuando terminen `a` y `b`, suma sus resultados. `join()` espera el final.

#### Desafío
Completá el método que combina los dos presupuestos.

#### Código inicial
```java
import java.util.concurrent.CompletableFuture;

public class Presupuesto {
    public static void main(String[] args) {
        CompletableFuture<Integer> madera = CompletableFuture.supplyAsync(() -> 120);
        CompletableFuture<Integer> piedras = CompletableFuture.supplyAsync(() -> 80);
        int total = madera.___(piedras, Integer::sum).join();
        System.out.println("Reparar la esclusa cuesta " + total + " denarios");
    }
}
```

#### Salida esperada
```
Reparar la esclusa cuesta 200 denarios
```

#### Solución
```java
import java.util.concurrent.CompletableFuture;

public class Presupuesto {
    public static void main(String[] args) {
        CompletableFuture<Integer> madera = CompletableFuture.supplyAsync(() -> 120);
        CompletableFuture<Integer> piedras = CompletableFuture.supplyAsync(() -> 80);
        int total = madera.thenCombine(piedras, Integer::sum).join();
        System.out.println("Reparar la esclusa cuesta " + total + " denarios");
    }
}
```

#### Al superarla
Doscientos denarios, sin esperar uno para pedir el otro. La esclusa se repara esa misma tarde.
A la noche, el agua de la Represa empieza a moverse sola. Algo enorme respira debajo.

#### Imagen
- Dos mensajeros llegando a la vez con presupuestos que se juntan en uno solo.
- La Represa de noche, con el agua agitándose y una sombra enorme debajo.

### Misión R04-N05-M1 · Los recaudadores

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Generá 200 000 ventas simuladas con un `Random(42)` (montos enteros entre 100 y 50 000,
cada una de una de 5 sucursales). Calculá el total por sucursal de dos formas:

1. Secuencial, con un bucle.
2. Concurrente: repartí las ventas en 4 partes con un `ExecutorService` de 4 hilos; cada
   tarea devuelve **su propio** mapa de totales parciales (sin compartir nada) y el
   `main` los junta.

Mostrá los dos resultados y si coinciden.

#### Criterio de aprobación

- Las tareas no comparten datos: cada una devuelve su resultado y se combinan al final.
- Los dos cálculos coinciden y el pool se cierra.

#### Salida esperada

```
Secuencial:  {Centro=1006497013, Este=1002544442, Norte=1004672922, Oeste=1009755622, Sur=986876697}
Concurrente: {Centro=1006497013, Este=1002544442, Norte=1004672922, Oeste=1009755622, Sur=986876697}
¿Coinciden? true
```

#### Solución de referencia

```java
// Mision 1 - Los recaudadores: repartir sin compartir, y juntar al final.
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.TreeMap;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class Recaudadores {
    record Venta(String sucursal, long monto) { }

    static final String[] SUCURSALES = {"Centro", "Norte", "Sur", "Este", "Oeste"};

    public static void main(String[] args) throws InterruptedException, ExecutionException {
        Random azar = new Random(42);
        List<Venta> ventas = new ArrayList<>();
        for (int i = 0; i < 200_000; i++) {
            ventas.add(new Venta(SUCURSALES[azar.nextInt(SUCURSALES.length)], 100 + azar.nextInt(49_901)));
        }

        Map<String, Long> secuencial = totales(ventas);
        System.out.println("Secuencial:  " + secuencial);

        ExecutorService pool = Executors.newFixedThreadPool(4);
        List<Callable<Map<String, Long>>> partes = new ArrayList<>();
        int tam = ventas.size() / 4;
        for (int i = 0; i < 4; i++) {
            List<Venta> parte = ventas.subList(i * tam, i == 3 ? ventas.size() : (i + 1) * tam);
            partes.add(() -> totales(parte));
        }
        Map<String, Long> concurrente = new TreeMap<>();
        for (Future<Map<String, Long>> f : pool.invokeAll(partes)) {
            f.get().forEach((sucursal, monto) -> concurrente.merge(sucursal, monto, Long::sum));
        }
        pool.shutdown();
        System.out.println("Concurrente: " + concurrente);
        System.out.println("¿Coinciden? " + secuencial.equals(concurrente));
    }

    static Map<String, Long> totales(List<Venta> ventas) {
        Map<String, Long> t = new TreeMap<>();
        for (Venta v : ventas) {
            t.merge(v.sucursal(), v.monto(), Long::sum);
        }
        return t;
    }
}
```

### Misión R04-N05-M2 · La boletería sin sobreventa

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un recital tiene 1000 entradas. Programá una clase `Boleteria` con un método
`boolean vender(int cantidad)` que vende solo si quedan entradas suficientes. Lanzá 8
hilos que intentan comprar, cada uno, 200 veces de a una entrada. Al final mostrá cuántas
se vendieron, cuántos pedidos fueron rechazados y que **nunca** se vendieron más de 1000.
Protegé la venta con `synchronized` (preguntar y descontar tiene que ser una sola
operación) y explicá en un comentario por qué un `AtomicInteger` solo para el contador
no alcanza si el "preguntar" y el "descontar" van separados.

#### Criterio de aprobación

- La venta es atómica: nunca se venden más de 1000 entradas.
- Vendidas + rechazadas = 1600 pedidos.

#### Salida esperada

```
Vendidas: 1000
Rechazadas: 600
Pedidos: 1600
¿Sobreventa? false
```

#### Solución de referencia

```java
// Mision 2 - La boleteria sin sobreventa: preguntar y descontar en una sola operacion.
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class BoleteriaSegura {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        Boleteria boleteria = new Boleteria(1000);
        ExecutorService pool = Executors.newFixedThreadPool(8);
        List<Callable<Integer>> compradores = new ArrayList<>();
        for (int i = 0; i < 8; i++) {
            compradores.add(() -> {
                int rechazos = 0;
                for (int intento = 0; intento < 200; intento++) {
                    if (!boleteria.vender(1)) {
                        rechazos++;
                    }
                }
                return rechazos;
            });
        }
        int rechazados = 0;
        for (Future<Integer> f : pool.invokeAll(compradores)) {
            rechazados += f.get();
        }
        pool.shutdown();
        System.out.println("Vendidas: " + boleteria.vendidas());
        System.out.println("Rechazadas: " + rechazados);
        System.out.println("Pedidos: " + (boleteria.vendidas() + rechazados));
        System.out.println("¿Sobreventa? " + (boleteria.vendidas() > 1000));
    }

    static class Boleteria {
        private int disponibles;
        private int vendidas;

        Boleteria(int disponibles) {
            this.disponibles = disponibles;
        }

        // Con un AtomicInteger, "if (disponibles.get() >= cantidad)" y luego
        // "disponibles.addAndGet(-cantidad)" son dos pasos: entre uno y otro otro hilo
        // puede vender la ultima entrada y se venderian de mas. synchronized hace que
        // preguntar y descontar sean una sola operacion.
        synchronized boolean vender(int cantidad) {
            if (disponibles < cantidad) {
                return false;
            }
            disponibles -= cantidad;
            vendidas += cantidad;
            return true;
        }

        synchronized int vendidas() {
            return vendidas;
        }
    }
}
```

### Misión R04-N05-M3 · El presupuesto combinado

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Para armar un presupuesto de viaje hay que consultar tres "servicios" lentos (simulados
con un método que duerme 300 ms y devuelve un valor fijo): el pasaje (95 000), el hotel
(28 000 por noche) y la cotización del dólar (1250). Con `CompletableFuture`:

1. Lanzá las tres consultas a la vez.
2. Calculá el hotel por 4 noches con `thenApply`.
3. Combiná pasaje y hotel con `thenCombine`, y el total con la cotización para tenerlo
   en dólares.
4. Si la consulta de un seguro opcional falla (lanza una excepción), usá
   `exceptionally` para tomarlo como 0.

Mostrá el presupuesto y medí el tiempo total: tiene que ser cercano a 300 ms y no a
1200 ms. Imprimí solo si tardó menos de un segundo (así la salida es siempre la misma).

#### Criterio de aprobación

- Las consultas corren a la vez (el tiempo total es el de la más lenta).
- Usa `thenApply`, `thenCombine` y `exceptionally`.

#### Salida esperada

```
Pasaje: 95000.00
Hotel (4 noches): 112000.00
Seguro: 0.00
Total: 207000.00 pesos = 165.60 dólares
Las consultas corrieron a la vez (menos de un segundo)
```

#### Solución de referencia

```java
// Mision 3 - El presupuesto combinado: CompletableFuture en paralelo.
import java.util.Locale;
import java.util.concurrent.CompletableFuture;

public class PresupuestoCombinado {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        long inicio = System.nanoTime();

        CompletableFuture<Double> pasaje = CompletableFuture.supplyAsync(() -> servicio("pasaje", 95_000));
        CompletableFuture<Double> hotel = CompletableFuture.supplyAsync(() -> servicio("hotel", 28_000)).thenApply(noche -> noche * 4);
        CompletableFuture<Double> dolar = CompletableFuture.supplyAsync(() -> servicio("dólar", 1_250));
        CompletableFuture<Double> seguro = CompletableFuture.supplyAsync(() -> servicio("seguro", -1)).exceptionally(e -> 0.0);

        CompletableFuture<Double> enPesos = pasaje.thenCombine(hotel, Double::sum).thenCombine(seguro, Double::sum);
        double total = enPesos.join();
        double enDolares = enPesos.thenCombine(dolar, (p, d) -> p / d).join();
        long ms = (System.nanoTime() - inicio) / 1_000_000;

        System.out.printf("Pasaje: %.2f%n", pasaje.join());
        System.out.printf("Hotel (4 noches): %.2f%n", hotel.join());
        System.out.printf("Seguro: %.2f%n", seguro.join());
        System.out.printf("Total: %.2f pesos = %.2f dólares%n", total, enDolares);
        System.out.println(ms < 1000 ? "Las consultas corrieron a la vez (menos de un segundo)" : "Tardó demasiado: ¿corrieron de a una?");
    }

    static double servicio(String nombre, double valor) {
        try {
            Thread.sleep(300);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        if (valor < 0) {
            throw new IllegalStateException("el servicio de " + nombre + " no responde");
        }
        return valor;
    }
}
```

### Encargo R04-N05-E1 · El contador de visitas

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un sitio registra visitas a sus páginas desde muchos hilos a la vez. Simulá 6 hilos que
registran, cada uno, 5000 visitas repartidas entre 4 páginas (`"/inicio"`, `"/cursos"`,
`"/precios"`, `"/contacto"`, en ciclo: la visita `i` va a la página `i % 4`). Guardá los
conteos en un `ConcurrentHashMap<String, Integer>` usando `merge`, y al final mostrá las
visitas por página ordenadas por nombre y el total. Explicá en un comentario por qué un
`HashMap` común con `put(pagina, get(pagina) + 1)` perdería visitas.

#### Criterio de aprobación

- Usa `ConcurrentHashMap.merge` y el total da exactamente 30 000.
- El comentario explica la carrera del `get` + `put`.

#### Salida esperada

```
/contacto: 7500
/cursos: 7500
/inicio: 7500
/precios: 7500
Total: 30000
```

#### Solución de referencia

```java
// Encargo - El contador de visitas: ConcurrentHashMap con merge.
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.concurrent.Callable;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ContadorVisitas {
    static final String[] PAGINAS = {"/inicio", "/cursos", "/precios", "/contacto"};

    public static void main(String[] args) throws InterruptedException {
        // Con un HashMap y put(p, get(p) + 1), dos hilos pueden leer el mismo valor,
        // sumarle 1 y escribir los dos el mismo resultado: se pierde una visita (y el
        // HashMap hasta puede romperse por dentro). merge en un ConcurrentHashMap hace
        // leer-sumar-escribir de forma atomica.
        Map<String, Integer> visitas = new ConcurrentHashMap<>();
        ExecutorService pool = Executors.newFixedThreadPool(6);
        List<Callable<Void>> hilos = new ArrayList<>();
        for (int h = 0; h < 6; h++) {
            hilos.add(() -> {
                for (int i = 0; i < 5000; i++) {
                    visitas.merge(PAGINAS[i % PAGINAS.length], 1, Integer::sum);
                }
                return null;
            });
        }
        pool.invokeAll(hilos);
        pool.shutdown();
        new TreeMap<>(visitas).forEach((pagina, n) -> System.out.println(pagina + ": " + n));
        System.out.println("Total: " + visitas.values().stream().mapToInt(Integer::intValue).sum());
    }
}
```

### Prueba del sello

#### ¿Qué es una condición de carrera?

Un error que aparece cuando varios hilos modifican el mismo dato a la vez y sus pasos se mezclan; el resultado depende del azar.

#### ¿Por qué `contador++` no es seguro entre hilos?

Porque son tres pasos (leer, sumar, escribir) y otro hilo puede meterse en el medio.

#### ¿Qué devuelve `submit` de un `ExecutorService`?

Un `Future`, del que se obtiene el resultado con `get()` cuando la tarea termina.

#### ¿Qué pasa si no llamás a `shutdown()`?

El programa no termina: los hilos del pool siguen esperando tareas.

#### ¿Cuál es la forma más segura de trabajar con varios hilos?

No compartir datos: que cada tarea calcule lo suyo y devuelva su resultado, y combinarlos al final.

### Soluciones (docente)

Sale de `19-Java-Avanzado/08-Concurrencia-Threads-Executors` (hilos, `ExecutorService`, sincronización). Todas las salidas son deterministas: los hilos no imprimen y los resultados se juntan en el `main`; la M3 solo informa si tardó menos de un segundo.

## R04-N06 · Jefe de las Corrientes: el Leviatán de los Datos

```meta
tipo: jefe
padre: R04-N05
precio: 10
criatura: dragon
insignia: Domador de Corrientes
insignia_descripcion: Venciste al Leviatán de los Datos: procesás miles de registros con streams, tipos sellados y concurrencia, sin un solo null.
usa: func.streams, conc.hilos
```

### Crónica

En la boca del río, donde las corrientes se juntan con el mar, algo enorme se mueve bajo el agua. Los pescadores lo llaman el **Leviatán de los Datos**: traga registros por miles, mezcla los buenos con los rotos y devuelve informes que nadie entiende.

—No se lo vence con un bucle y cien `if` —dice {mentor}—. Se lo vence separando lo que llega en **válido** e **inválido** sin perder ninguno, resumiendo con **streams**, repartiendo el trabajo entre **hilos** sin que se pisen, y respondiendo con un **`Optional`** cuando la respuesta puede no existir. Todo lo de las Corrientes, junto. Y con pruebas, Zed: al Leviatán no se le cree nada sin comprobarlo.

### Objetivos

- Leer registros de texto y clasificarlos con una jerarquía sellada (válido o rechazado con su motivo).
- Armar un informe con `Collectors`, comparadores y `Optional`.
- Repartir el procesamiento entre hilos sin compartir datos y obtener el mismo resultado que en secuencia.
- Probar el analizador con JUnit.

### Antes de empezar

- Toda la rama de las Corrientes.
- JUnit (rama 3).

### Explicación

#### La forma del analizador
```
líneas de texto  →  leer(línea)            →  Lectura (sealed): Valida(Registro) | Rechazada(línea, motivo)
                    registros válidos      →  informe con Collectors (por grupo, totales, ranking)
                    búsquedas              →  Optional<…>
                    muchas líneas          →  partes en un ExecutorService, se combinan al final
```

#### Nunca perder una línea
Un analizador serio **no descarta en silencio**: cada línea termina como válida o como
rechazada con su motivo. Con una interfaz sellada, el resultado de leer una línea es
"una de dos cosas", y el compilador lo sabe:
```java
sealed interface Lectura permits Valida, Rechazada { }
record Valida(Viaje viaje) implements Lectura { }
record Rechazada(int linea, String texto, String motivo) implements Lectura { }
```
Las validaciones viven en el constructor compacto del `record` del dato; leer la línea
es atrapar esa excepción y convertirla en una `Rechazada`.

#### Concurrente y verificable
Para repartir, cada tarea procesa **su parte** y devuelve su propio resultado parcial
(una lista o un mapa); el `main` los combina. El resultado tiene que ser **idéntico** al
secuencial: esa comparación es la mejor prueba de que no hay carreras.

### Código de ejemplo

El analizador de los viajes de una empresa de micros: lee las líneas, separa las
rechazadas, arma el informe y lo repite en paralelo para comprobar que da lo mismo.

```java
/*
 * Jefe de las Corrientes: el analizador de viajes.
 * Lectura sellada, informe con Collectors, Optional y procesamiento en paralelo.
 */
import static java.util.stream.Collectors.averagingInt;
import static java.util.stream.Collectors.counting;
import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.summingDouble;
import static java.util.stream.Collectors.summingLong;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import java.util.TreeMap;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class AnalizadorViajes {
    static final String DATOS = """
            2026-09-01;La Rioja;Chilecito;38;15500
            2026-09-01;La Rioja;Córdoba;41;32000
            2026-09-02;Chilecito;La Rioja;29;15500
            2026-09-02;La Rioja;Catamarca;;12800
            2026-09-03;La Rioja;Córdoba;44;32000
            2026-09-03;Córdoba;La Rioja;37;32000
            2026-09-04;La Rioja;Chilecito;52;15500
            2026-09-04;La Rioja;Aimogasta;12;-900
            2026-09-05;Catamarca;La Rioja;22;12800
            2026-09-05;La Rioja;La Rioja;10;5000
            2026-09-06;La Rioja;Córdoba;45;32000
            2026-09-06;Chilecito;La Rioja;31;15500
            fecha rota;La Rioja;Chilecito;30;15500
            2026-09-07;La Rioja;Catamarca;19;12800
            """;

    public static void main(String[] args) throws InterruptedException, ExecutionException {
        Locale.setDefault(Locale.US);
        List<String> lineas = DATOS.lines().toList();

        List<Lectura> lecturas = leerTodas(lineas, 0);
        List<Viaje> viajes = validos(lecturas);
        System.out.println("Líneas: " + lineas.size() + " | válidas: " + viajes.size() + " | rechazadas: " + (lineas.size() - viajes.size()));
        lecturas.stream().filter(l -> l instanceof Rechazada).map(l -> (Rechazada) l)
                .forEach(r -> System.out.println("  línea " + r.linea() + ": " + r.motivo()));

        System.out.println("Pasajeros por ruta:");
        Map<String, Long> pasajerosPorRuta = pasajerosPorRuta(viajes);
        pasajerosPorRuta.forEach((ruta, n) -> System.out.printf("  %-24s %4d%n", ruta, n));

        Map<String, Double> promedio = viajes.stream().collect(groupingBy(Viaje::origen, TreeMap::new, averagingInt(Viaje::pasajeros)));
        promedio.forEach((origen, p) -> System.out.printf("  promedio saliendo de %s: %.1f%n", origen, p));

        Map<String, Double> recaudado = viajes.stream().collect(groupingBy(Viaje::ruta, TreeMap::new, summingDouble(Viaje::recaudacion)));
        System.out.println("Las 2 rutas que más recaudan:");
        recaudado.entrySet().stream()
                .sorted(Map.Entry.<String, Double>comparingByValue().reversed().thenComparing(Map.Entry.comparingByKey()))
                .limit(2)
                .forEach(e -> System.out.printf("  %s: %.2f%n", e.getKey(), e.getValue()));

        System.out.println("Viaje más lleno: " + masLleno(viajes).map(Viaje::toString).orElse("ninguno"));
        System.out.println("Primer viaje a Mendoza: " + primeroA(viajes, "Mendoza").map(Viaje::fecha).orElse("no hay"));
        System.out.println("Viajes por día: " + viajes.stream().collect(groupingBy(Viaje::fecha, TreeMap::new, counting())));

        // En paralelo: 3 partes, cada una devuelve sus lecturas; se juntan en orden
        ExecutorService pool = Executors.newFixedThreadPool(3);
        List<Callable<List<Lectura>>> partes = new ArrayList<>();
        int tam = (lineas.size() + 2) / 3;
        for (int i = 0; i < lineas.size(); i += tam) {
            int desde = i;
            List<String> parte = lineas.subList(desde, Math.min(desde + tam, lineas.size()));
            partes.add(() -> leerTodas(parte, desde));
        }
        List<Lectura> enParalelo = new ArrayList<>();
        for (Future<List<Lectura>> f : pool.invokeAll(partes)) {
            enParalelo.addAll(f.get());
        }
        pool.shutdown();
        System.out.println("¿En paralelo da lo mismo? " + (enParalelo.equals(lecturas)
                && pasajerosPorRuta(validos(enParalelo)).equals(pasajerosPorRuta)));
    }

    static List<Lectura> leerTodas(List<String> lineas, int desplazamiento) {
        List<Lectura> lecturas = new ArrayList<>();
        for (int i = 0; i < lineas.size(); i++) {
            lecturas.add(leer(desplazamiento + i + 1, lineas.get(i)));
        }
        return lecturas;
    }

    static Lectura leer(int numero, String linea) {
        String[] c = linea.split(";", -1);
        try {
            if (c.length != 5) {
                throw new IllegalArgumentException("tiene " + c.length + " campos y no 5");
            }
            return new Valida(new Viaje(c[0], c[1], c[2], Integer.parseInt(c[3]), Double.parseDouble(c[4])));
        } catch (NumberFormatException e) {
            return new Rechazada(numero, linea, "número inválido (" + e.getMessage() + ")");
        } catch (IllegalArgumentException e) {
            return new Rechazada(numero, linea, e.getMessage());
        }
    }

    static List<Viaje> validos(List<Lectura> lecturas) {
        return lecturas.stream().filter(l -> l instanceof Valida).map(l -> ((Valida) l).viaje()).toList();
    }

    static Map<String, Long> pasajerosPorRuta(List<Viaje> viajes) {
        return viajes.stream().collect(groupingBy(Viaje::ruta, TreeMap::new, summingLong(Viaje::pasajeros)));
    }

    static Optional<Viaje> masLleno(List<Viaje> viajes) {
        return viajes.stream().max(Comparator.comparingInt(Viaje::pasajeros).thenComparing(Viaje::fecha, Comparator.reverseOrder()));
    }

    static Optional<Viaje> primeroA(List<Viaje> viajes, String destino) {
        return viajes.stream().filter(v -> v.destino().equals(destino)).findFirst();
    }

    sealed interface Lectura permits Valida, Rechazada { }

    record Valida(Viaje viaje) implements Lectura { }

    record Rechazada(int linea, String texto, String motivo) implements Lectura { }

    record Viaje(String fecha, String origen, String destino, int pasajeros, double tarifa) {
        Viaje {
            if (!fecha.matches("\\d{4}-\\d{2}-\\d{2}")) {
                throw new IllegalArgumentException("fecha inválida: " + fecha);
            }
            if (origen.equals(destino)) {
                throw new IllegalArgumentException("origen y destino iguales: " + origen);
            }
            if (pasajeros < 0 || tarifa <= 0) {
                throw new IllegalArgumentException("pasajeros o tarifa fuera de rango");
            }
        }

        String ruta() {
            return origen + " → " + destino;
        }

        double recaudacion() {
            return pasajeros * tarifa;
        }

        @Override
        public String toString() {
            return fecha + " " + ruta() + " (" + pasajeros + " pasajeros)";
        }
    }
}
```

### Salida esperada

```
Líneas: 14 | válidas: 10 | rechazadas: 4
  línea 4: número inválido (For input string: "")
  línea 8: pasajeros o tarifa fuera de rango
  línea 10: origen y destino iguales: La Rioja
  línea 13: fecha inválida: fecha rota
Pasajeros por ruta:
  Catamarca → La Rioja       22
  Chilecito → La Rioja       60
  Córdoba → La Rioja         37
  La Rioja → Catamarca       19
  La Rioja → Chilecito       90
  La Rioja → Córdoba        130
  promedio saliendo de Catamarca: 22.0
  promedio saliendo de Chilecito: 30.0
  promedio saliendo de Córdoba: 37.0
  promedio saliendo de La Rioja: 39.8
Las 2 rutas que más recaudan:
  La Rioja → Córdoba: 4160000.00
  La Rioja → Chilecito: 1395000.00
Viaje más lleno: 2026-09-04 La Rioja → Chilecito (52 pasajeros)
Primer viaje a Mendoza: no hay
Viajes por día: {2026-09-01=2, 2026-09-02=1, 2026-09-03=2, 2026-09-04=1, 2026-09-05=1, 2026-09-06=2, 2026-09-07=1}
¿En paralelo da lo mismo? true
```

### ¿Para qué sirve?

Así se procesan los archivos que llegan de otros sistemas: extractos bancarios, padrones, ventas de sucursales, lecturas de sensores. Siempre hay líneas rotas, y un buen programa las informa en vez de caerse o esconderlas. Repartir entre hilos y comparar con el resultado secuencial es cómo se procesan millones de registros con confianza.

### Errores habituales

**Dragón: la línea que desaparece.** Un `try`/`catch` vacío que saltea las líneas con
error: el informe da números que no cierran y nadie sabe por qué. Toda línea es válida o
rechazada con motivo.

**Ogro: el `split` que se come los vacíos.** `"a;;b;".split(";")` descarta los campos
vacíos del final. Con `split(";", -1)` se conservan y la cuenta de campos es correcta.

**Troll: el orden del `catch`.** `NumberFormatException` es hija de
`IllegalArgumentException`: si se atrapa primero la madre, la hija nunca llega a su
`catch` (y no compila).

**Goblin: el paralelo desordenado.** Juntar los resultados en el orden en que terminan
los hilos cambia el orden de las lecturas. `invokeAll` devuelve los `Future` en el orden
de las tareas: juntalos así.

**Ogro: el número de línea que se corre.** Al repartir en partes, cada parte tiene que
saber desde qué línea empieza para informar el número real.

### Micro-misión R04-N06-P1 · Ni una línea perdida

```meta
lugar: La Represa
personajes: Zed, Gheco, Nadia, Kaffa, el Leviatán de los Datos
criatura: dragon
carta: Clasificar sin perder | sealed interface Resultado permits Valido, Rechazado · cada línea termina en uno de los dos, con su motivo
recompensa: xp 20, oro 20
```

#### Escena
En la Represa, el **Leviatán de los Datos** traga registros por miles, mezcla los buenos con los rotos y devuelve informes que nadie entiende. —No se lo vence con un bucle y cien `if` —dice Kaffa—. Primero: separá lo **válido** de lo **inválido**, sin perder ni una línea.

#### Gheco sugiere
Cada línea se convierte en un `Resultado`: un `Valido` con la barcaza o un `Rechazado` con la línea y el **motivo**. Así ninguna se pierde. Una línea es inválida si no tiene dos partes separadas por `;`.

#### Desafío
Completá el `Rechazado` con la línea y el motivo "le falta el ;".

#### Código inicial
```java
import java.util.List;

public class Leviatan1 {
    static Resultado leer(String linea) {
        String[] partes = linea.split(";");
        if (partes.length != 2) {
            return ___;
        }
        return new Valido(new Barcaza(partes[0], Integer.parseInt(partes[1])));
    }

    public static void main(String[] args) {
        for (String linea : List.of("Garza;80", "Ceibo", "Bagre;120")) {
            System.out.println(leer(linea));
        }
    }
}

record Barcaza(String nombre, int carga) {
}

sealed interface Resultado permits Valido, Rechazado {
}

record Valido(Barcaza barcaza) implements Resultado {
}

record Rechazado(String linea, String motivo) implements Resultado {
}
```

#### Salida esperada
```
Valido[barcaza=Barcaza[nombre=Garza, carga=80]]
Rechazado[linea=Ceibo, motivo=le falta el ;]
Valido[barcaza=Barcaza[nombre=Bagre, carga=120]]
```

#### Solución
```java
import java.util.List;

public class Leviatan1 {
    static Resultado leer(String linea) {
        String[] partes = linea.split(";");
        if (partes.length != 2) {
            return new Rechazado(linea, "le falta el ;");
        }
        return new Valido(new Barcaza(partes[0], Integer.parseInt(partes[1])));
    }

    public static void main(String[] args) {
        for (String linea : List.of("Garza;80", "Ceibo", "Bagre;120")) {
            System.out.println(leer(linea));
        }
    }
}

record Barcaza(String nombre, int carga) {
}

sealed interface Resultado permits Valido, Rechazado {
}

record Valido(Barcaza barcaza) implements Resultado {
}

record Rechazado(String linea, String motivo) implements Resultado {
}
```

#### Al superarla
Tres líneas, tres resultados, ninguna tragada. El Leviatán sacude la cola: por primera vez, alguien le pide cuentas por cada registro.

#### Imagen
- El Leviatán de los Datos: una serpiente marina gigante hecha de registros y números que brillan, saliendo del agua de la Represa.
- Zed frente a él, con dos canastos: «válido» y «rechazado»; Nadia, Gheco y Kaffa atrás.

### Micro-misión R04-N06-P2 · El informe que se entiende

```meta
lugar: La Represa
personajes: Zed, Gheco, Nadia, Kaffa, el Leviatán de los Datos
carta: Resumir con Collectors | groupingBy(…, TreeMap::new, summingInt(…)) · un mapa ordenado: grupo → suma
recompensa: xp 20, oro 20
```

#### Escena
El Leviatán devuelve informes que nadie entiende. Zed le contesta con uno que **sí**: la carga total que entró por cada puerto de origen.

#### Gheco sugiere
`Collectors.groupingBy(Barcaza::origen, TreeMap::new, Collectors.summingInt(Barcaza::carga))` agrupa por origen y **suma** la carga de cada grupo, con los orígenes ordenados.

#### Desafío
Completá el colector que suma la carga de cada grupo.

#### Código inicial
```java
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.stream.Collectors;

public class Leviatan2 {
    public static void main(String[] args) {
        List<Barcaza> validas = List.of(new Barcaza("Garza", "Delta", 80), new Barcaza("Bagre", "Puerto", 120),
                new Barcaza("Junco", "Delta", 50), new Barcaza("Sauce", "Puerto", 20));
        Map<String, Integer> porOrigen = validas.stream()
                .collect(Collectors.groupingBy(Barcaza::origen, TreeMap::new, Collectors.___(Barcaza::carga)));
        porOrigen.forEach((origen, total) -> System.out.println(origen + ": " + total));
    }
}

record Barcaza(String nombre, String origen, int carga) {
}
```

#### Salida esperada
```
Delta: 130
Puerto: 140
```

#### Solución
```java
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.stream.Collectors;

public class Leviatan2 {
    public static void main(String[] args) {
        List<Barcaza> validas = List.of(new Barcaza("Garza", "Delta", 80), new Barcaza("Bagre", "Puerto", 120),
                new Barcaza("Junco", "Delta", 50), new Barcaza("Sauce", "Puerto", 20));
        Map<String, Integer> porOrigen = validas.stream()
                .collect(Collectors.groupingBy(Barcaza::origen, TreeMap::new, Collectors.summingInt(Barcaza::carga)));
        porOrigen.forEach((origen, total) -> System.out.println(origen + ": " + total));
    }
}

record Barcaza(String nombre, String origen, int carga) {
}
```

#### Al superarla
«Delta: 130. Puerto: 140.» Dos líneas que cualquiera entiende. El Leviatán pierde un anillo de registros, que se hunde en el agua.

#### Imagen
- Un pergamino corto y claro flotando frente al Leviatán, con dos líneas de totales.
- Un anillo de registros desprendiéndose del cuerpo del Leviatán.

### Micro-misión R04-N06-P3 · La respuesta que puede no existir

```meta
lugar: La Represa
personajes: Zed, Gheco, Nadia, Kaffa, el Leviatán de los Datos
carta: max y Optional | stream().max(Comparator.comparingInt(…)) devuelve un Optional · .map(…).orElse(…) responde aunque no haya nada
recompensa: xp 20, oro 25
item: Remo de las Corrientes
```

#### Escena
El Leviatán pregunta, con voz de agua: **¿cuál es la barcaza más cargada que entró desde la Torre?** Si Zed responde `null`, el Leviatán se lo traga. Desde la Torre no entró ninguna.

#### Gheco sugiere
`max(comparador)` devuelve un `Optional`: puede estar vacío si no hay ninguna. `.map(Barcaza::nombre).orElse("ninguna")` responde siempre, sin `null`.

#### Desafío
Completá el comparador del `max`: por carga.

#### Código inicial
```java
import java.util.Comparator;
import java.util.List;

public class Leviatan3 {
    static String masCargada(List<Barcaza> barcazas, String origen) {
        return barcazas.stream()
                .filter(b -> b.origen().equals(origen))
                .max(Comparator.comparingInt(___))
                .map(Barcaza::nombre)
                .orElse("ninguna");
    }

    public static void main(String[] args) {
        List<Barcaza> validas = List.of(new Barcaza("Garza", "Delta", 80), new Barcaza("Bagre", "Puerto", 120),
                new Barcaza("Junco", "Delta", 50));
        for (String origen : List.of("Delta", "Puerto", "Torre")) {
            System.out.println(origen + ": " + masCargada(validas, origen));
        }
    }
}

record Barcaza(String nombre, String origen, int carga) {
}
```

#### Salida esperada
```
Delta: Garza
Puerto: Bagre
Torre: ninguna
```

#### Solución
```java
import java.util.Comparator;
import java.util.List;

public class Leviatan3 {
    static String masCargada(List<Barcaza> barcazas, String origen) {
        return barcazas.stream()
                .filter(b -> b.origen().equals(origen))
                .max(Comparator.comparingInt(Barcaza::carga))
                .map(Barcaza::nombre)
                .orElse("ninguna");
    }

    public static void main(String[] args) {
        List<Barcaza> validas = List.of(new Barcaza("Garza", "Delta", 80), new Barcaza("Bagre", "Puerto", 120),
                new Barcaza("Junco", "Delta", 50));
        for (String origen : List.of("Delta", "Puerto", "Torre")) {
            System.out.println(origen + ": " + masCargada(validas, origen));
        }
    }
}

record Barcaza(String nombre, String origen, int carga) {
}
```

#### Al superarla
«Torre: ninguna.» Una respuesta, aunque sea vacía. El Leviatán se queda sin presa y suelta lo que tenía entre los dientes: un **remo** de madera clara que brilla con las corrientes. Zed lo agarra: el **Remo de las Corrientes**.

#### Imagen
- El Leviatán abriendo la boca, sorprendido; un remo de madera clara cayendo al agua con líneas de luz como corrientes.
- Zed atrapando el remo en el aire.

### Micro-misión R04-N06-P4 · Dos corrientes, el mismo resultado

```meta
lugar: La Represa
personajes: Zed, Gheco, Nadia, Kaffa, el Leviatán de los Datos
carta: Concurrente y verificable | se reparte el trabajo en partes que NO comparten nada · cada parte da su resultado · se combinan · da igual que en secuencia
recompensa: xp 25, oro 30
item: Vitral del Viajero
```

#### Escena
El último truco del Leviatán es la cantidad: millones de registros. Zed reparte el trabajo en **dos mitades**, cada una con su propio hilo y sin compartir nada, y después junta los resultados. —Y demostrá que da lo mismo que hacerlo de a uno —dice Kaffa—. Al Leviatán no se le cree nada sin comprobarlo.

#### Gheco sugiere
Cada mitad se procesa en su tarea (`pool.submit`) y devuelve su suma; nadie toca una variable compartida. Al final se suman las dos partes con `get()` y se compara con el cálculo en secuencia.

#### Desafío
Completá la suma de las dos mitades con sus recibos.

#### Código inicial
```java
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.stream.IntStream;

public class Leviatan4 {
    public static void main(String[] args) throws Exception {
        List<Integer> cargas = IntStream.rangeClosed(1, 100000).map(i -> i % 97).boxed().toList();
        int mitad = cargas.size() / 2;
        ExecutorService pool = Executors.newFixedThreadPool(2);
        Future<Integer> a = pool.submit(() -> cargas.subList(0, mitad).stream().mapToInt(c -> c).sum());
        Future<Integer> b = pool.submit(() -> cargas.subList(mitad, cargas.size()).stream().mapToInt(c -> c).sum());
        int enParalelo = ___;
        pool.shutdown();
        int enSecuencia = cargas.stream().mapToInt(c -> c).sum();
        System.out.println("En paralelo: " + enParalelo);
        System.out.println("En secuencia: " + enSecuencia);
        System.out.println("Iguales: " + (enParalelo == enSecuencia));
    }
}
```

#### Salida esperada
```
En paralelo: 4799775
En secuencia: 4799775
Iguales: true
```

#### Solución
```java
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.stream.IntStream;

public class Leviatan4 {
    public static void main(String[] args) throws Exception {
        List<Integer> cargas = IntStream.rangeClosed(1, 100000).map(i -> i % 97).boxed().toList();
        int mitad = cargas.size() / 2;
        ExecutorService pool = Executors.newFixedThreadPool(2);
        Future<Integer> a = pool.submit(() -> cargas.subList(0, mitad).stream().mapToInt(c -> c).sum());
        Future<Integer> b = pool.submit(() -> cargas.subList(mitad, cargas.size()).stream().mapToInt(c -> c).sum());
        int enParalelo = a.get() + b.get();
        pool.shutdown();
        int enSecuencia = cargas.stream().mapToInt(c -> c).sum();
        System.out.println("En paralelo: " + enParalelo);
        System.out.println("En secuencia: " + enSecuencia);
        System.out.println("Iguales: " + (enParalelo == enSecuencia));
    }
}
```

#### Al superarla
«Iguales: true.» El Leviatán se deshace en millones de registros ordenados que el río se lleva mansamente.
Detrás de él, encallada en la Represa, está la barcaza **Ceibo**. Adentro, envuelto en lona, hay **un vitral**: el **Vitral del Viajero**. Tiene una etiqueta: «para la ventana más alta de la Torre del Arquitecto».

#### Imagen
- El Leviatán deshaciéndose en una lluvia de registros luminosos que el río se lleva.
- La barcaza Ceibo encallada; Zed desenvolviendo un vitral de colores envuelto en lona, con una etiqueta atada.
- Al fondo, la Torre del Arquitecto recortada contra el cielo.

### Misión R04-N06-M1 · El informe del Leviatán

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Una cadena de farmacias manda sus ventas en líneas `fecha;sucursal;producto;cantidad;precio`
(en una constante con un bloque de texto, **al menos 15 líneas y al menos 3 inválidas**
por motivos distintos). Programá un analizador que:

1. Lea cada línea como una `Lectura` sellada: `Valida(Venta)` o `Rechazada(linea,
   motivo)`. `Venta` es un `record` que valida en su constructor compacto (cantidad
   positiva, precio positivo, sucursal no vacía).
2. Muestre las rechazadas con su número de línea y motivo.
3. Informe con `Collectors`: facturación por sucursal, unidades por producto, el producto
   más vendido (en unidades) y la sucursal con mayor ticket promedio.
4. Tenga dos búsquedas que devuelven `Optional`: la venta más cara de un producto dado y
   la primera venta de una sucursal en una fecha.
5. Procese las líneas en 3 partes con un `ExecutorService` y muestre que el resultado
   coincide con el secuencial.

#### Criterio de aprobación

- Ninguna línea se pierde: válidas + rechazadas = total.
- Usa la jerarquía sellada, `Collectors`, `Optional` y el pool; la versión en paralelo da lo mismo.
- Sin bucles donde alcanza un stream, sin `null` ni `Optional.get()`.

#### Salida esperada

```
Total: 16 | válidas: 12 | rechazadas: 4
  línea 6: cantidad no positiva: -1
  línea 9: sucursal vacía
  línea 13: número inválido: tres
  línea 16: faltan campos (3 de 5)
Facturación Centro: 50700.00
Facturación Norte: 33500.00
Facturación Sur: 45400.00
Unidades por producto: {alcohol en gel=12, ibuprofeno=11, protector solar=4, vitamina C=3}
Más vendido: alcohol en gel (12 unidades)
Mayor ticket promedio: Sur (15133.33)
Venta más cara de protector solar: 2026-09-11 Sur 2 x protector solar = 31600.00
Venta más cara de jarabe: no hay
Primera de Sur el 2026-09-11: alcohol en gel
Primera de Norte el 2026-09-13: no hay
¿En paralelo coincide? true
```

#### Solución de referencia

```java
// Jefe S02 - Mision 1: el informe de las farmacias.
import static java.util.stream.Collectors.averagingDouble;
import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.summingDouble;
import static java.util.stream.Collectors.summingInt;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import java.util.TreeMap;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class InformeFarmacias {
    static final String DATOS = """
            2026-09-10;Centro;ibuprofeno;3;2400
            2026-09-10;Centro;protector solar;1;15800
            2026-09-10;Norte;ibuprofeno;2;2400
            2026-09-10;Norte;alcohol en gel;4;1900
            2026-09-11;Centro;vitamina C;2;6200
            2026-09-11;Sur;ibuprofeno;-1;2400
            2026-09-11;Sur;alcohol en gel;6;1900
            2026-09-11;Sur;protector solar;2;15800
            2026-09-12;;ibuprofeno;1;2400
            2026-09-12;Norte;vitamina C;1;6200
            2026-09-12;Centro;alcohol en gel;2;1900
            2026-09-12;Norte;protector solar;1;14900
            2026-09-13;Sur;vitamina C;tres;6200
            2026-09-13;Centro;ibuprofeno;5;2300
            2026-09-13;Sur;ibuprofeno;1;2400
            2026-09-13;Norte;alcohol en gel
            """;

    public static void main(String[] args) throws InterruptedException, ExecutionException {
        Locale.setDefault(Locale.US);
        List<String> lineas = DATOS.lines().toList();
        List<Lectura> lecturas = leerTodas(lineas, 0);
        List<Venta> ventas = validas(lecturas);

        System.out.println("Total: " + lineas.size() + " | válidas: " + ventas.size() + " | rechazadas: " + (lineas.size() - ventas.size()));
        for (Lectura l : lecturas) {
            if (l instanceof Rechazada r) {
                System.out.println("  línea " + r.linea() + ": " + r.motivo());
            }
        }

        Map<String, Double> facturacion = ventas.stream().collect(groupingBy(Venta::sucursal, TreeMap::new, summingDouble(Venta::total)));
        facturacion.forEach((s, t) -> System.out.printf("Facturación %s: %.2f%n", s, t));
        Map<String, Integer> unidades = ventas.stream().collect(groupingBy(Venta::producto, TreeMap::new, summingInt(Venta::cantidad)));
        System.out.println("Unidades por producto: " + unidades);
        unidades.entrySet().stream().max(Map.Entry.comparingByValue())
                .ifPresent(e -> System.out.println("Más vendido: " + e.getKey() + " (" + e.getValue() + " unidades)"));
        ventas.stream().collect(groupingBy(Venta::sucursal, TreeMap::new, averagingDouble(Venta::total)))
                .entrySet().stream().max(Map.Entry.comparingByValue())
                .ifPresent(e -> System.out.printf("Mayor ticket promedio: %s (%.2f)%n", e.getKey(), e.getValue()));

        System.out.println("Venta más cara de protector solar: " + masCara(ventas, "protector solar").map(Venta::toString).orElse("no hay"));
        System.out.println("Venta más cara de jarabe: " + masCara(ventas, "jarabe").map(Venta::toString).orElse("no hay"));
        System.out.println("Primera de Sur el 2026-09-11: " + primera(ventas, "Sur", "2026-09-11").map(Venta::producto).orElse("no hay"));
        System.out.println("Primera de Norte el 2026-09-13: " + primera(ventas, "Norte", "2026-09-13").map(Venta::producto).orElse("no hay"));

        ExecutorService pool = Executors.newFixedThreadPool(3);
        List<Callable<List<Lectura>>> partes = new ArrayList<>();
        int tam = (lineas.size() + 2) / 3;
        for (int i = 0; i < lineas.size(); i += tam) {
            int desde = i;
            List<String> parte = lineas.subList(desde, Math.min(desde + tam, lineas.size()));
            partes.add(() -> leerTodas(parte, desde));
        }
        List<Lectura> enParalelo = new ArrayList<>();
        for (Future<List<Lectura>> f : pool.invokeAll(partes)) {
            enParalelo.addAll(f.get());
        }
        pool.shutdown();
        System.out.println("¿En paralelo coincide? " + enParalelo.equals(lecturas));
    }

    static List<Lectura> leerTodas(List<String> lineas, int desplazamiento) {
        List<Lectura> lecturas = new ArrayList<>();
        for (int i = 0; i < lineas.size(); i++) {
            lecturas.add(leer(desplazamiento + i + 1, lineas.get(i)));
        }
        return lecturas;
    }

    static Lectura leer(int numero, String linea) {
        String[] c = linea.split(";", -1);
        if (c.length != 5) {
            return new Rechazada(numero, "faltan campos (" + c.length + " de 5)");
        }
        try {
            return new Valida(new Venta(c[0], c[1], c[2], Integer.parseInt(c[3]), Double.parseDouble(c[4])));
        } catch (NumberFormatException e) {
            return new Rechazada(numero, "número inválido: " + c[3]);
        } catch (IllegalArgumentException e) {
            return new Rechazada(numero, e.getMessage());
        }
    }

    static List<Venta> validas(List<Lectura> lecturas) {
        List<Venta> ventas = new ArrayList<>();
        for (Lectura l : lecturas) {
            if (l instanceof Valida v) {
                ventas.add(v.venta());
            }
        }
        return ventas;
    }

    static Optional<Venta> masCara(List<Venta> ventas, String producto) {
        return ventas.stream().filter(v -> v.producto().equals(producto)).max(Comparator.comparingDouble(Venta::total));
    }

    static Optional<Venta> primera(List<Venta> ventas, String sucursal, String fecha) {
        return ventas.stream().filter(v -> v.sucursal().equals(sucursal) && v.fecha().equals(fecha)).findFirst();
    }

    sealed interface Lectura permits Valida, Rechazada { }

    record Valida(Venta venta) implements Lectura { }

    record Rechazada(int linea, String motivo) implements Lectura { }

    record Venta(String fecha, String sucursal, String producto, int cantidad, double precio) {
        Venta {
            if (sucursal.isBlank()) {
                throw new IllegalArgumentException("sucursal vacía");
            }
            if (cantidad <= 0) {
                throw new IllegalArgumentException("cantidad no positiva: " + cantidad);
            }
            if (precio <= 0) {
                throw new IllegalArgumentException("precio no positivo: " + precio);
            }
        }

        double total() {
            return cantidad * precio;
        }

        @Override
        public String toString() {
            return String.format("%s %s %d x %s = %.2f", fecha, sucursal, cantidad, producto, total());
        }
    }
}
```

### Misión R04-N06-M2 · Las pruebas del Leviatán

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Separá la lógica del analizador en una clase `Analizador` (sin `main`, sin imprimir) y
escribí **al menos 6 pruebas de JUnit** en `AnalizadorTest`:

1. Una línea correcta se lee como `Valida` con los datos bien cargados.
2. Una línea con campos de menos, una con un número inválido y una con cantidad negativa
   se leen como `Rechazada` con el motivo esperado.
3. Válidas + rechazadas = total de líneas.
4. La facturación por sucursal da los valores esperados.
5. Una búsqueda sin resultado devuelve un `Optional` vacío.
6. El procesamiento en paralelo da exactamente lo mismo que el secuencial.

Pegá las dos clases.

#### Criterio de aprobación

- La clase `Analizador` no imprime nada ni tiene `main`.
- Las pruebas cubren lecturas válidas e inválidas, el informe, el `Optional` vacío y el paralelo, y pasan.

#### Solución de referencia

`Analizador.java`

```java
// Jefe S02 - Mision 2: el analizador, sin main ni impresiones, listo para probar.
import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.summingDouble;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.TreeMap;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class Analizador {
    public sealed interface Lectura permits Valida, Rechazada { }

    public record Valida(Venta venta) implements Lectura { }

    public record Rechazada(int linea, String motivo) implements Lectura { }

    public record Venta(String fecha, String sucursal, String producto, int cantidad, double precio) {
        public Venta {
            if (sucursal.isBlank()) {
                throw new IllegalArgumentException("sucursal vacía");
            }
            if (cantidad <= 0) {
                throw new IllegalArgumentException("cantidad no positiva: " + cantidad);
            }
            if (precio <= 0) {
                throw new IllegalArgumentException("precio no positivo: " + precio);
            }
        }

        public double total() {
            return cantidad * precio;
        }
    }

    public static Lectura leer(int numero, String linea) {
        String[] c = linea.split(";", -1);
        if (c.length != 5) {
            return new Rechazada(numero, "faltan campos (" + c.length + " de 5)");
        }
        try {
            return new Valida(new Venta(c[0], c[1], c[2], Integer.parseInt(c[3]), Double.parseDouble(c[4])));
        } catch (NumberFormatException e) {
            return new Rechazada(numero, "número inválido: " + c[3]);
        } catch (IllegalArgumentException e) {
            return new Rechazada(numero, e.getMessage());
        }
    }

    public static List<Lectura> leerTodas(List<String> lineas, int desplazamiento) {
        List<Lectura> lecturas = new ArrayList<>();
        for (int i = 0; i < lineas.size(); i++) {
            lecturas.add(leer(desplazamiento + i + 1, lineas.get(i)));
        }
        return lecturas;
    }

    public static List<Lectura> leerEnParalelo(List<String> lineas, int hilos) throws InterruptedException, ExecutionException {
        ExecutorService pool = Executors.newFixedThreadPool(hilos);
        try {
            List<Callable<List<Lectura>>> partes = new ArrayList<>();
            int tam = Math.max(1, (lineas.size() + hilos - 1) / hilos);
            for (int i = 0; i < lineas.size(); i += tam) {
                int desde = i;
                List<String> parte = lineas.subList(desde, Math.min(desde + tam, lineas.size()));
                partes.add(() -> leerTodas(parte, desde));
            }
            List<Lectura> todas = new ArrayList<>();
            for (Future<List<Lectura>> f : pool.invokeAll(partes)) {
                todas.addAll(f.get());
            }
            return todas;
        } finally {
            pool.shutdown();
        }
    }

    public static List<Venta> validas(List<Lectura> lecturas) {
        return lecturas.stream().filter(l -> l instanceof Valida).map(l -> ((Valida) l).venta()).toList();
    }

    public static Map<String, Double> facturacionPorSucursal(List<Venta> ventas) {
        return ventas.stream().collect(groupingBy(Venta::sucursal, TreeMap::new, summingDouble(Venta::total)));
    }

    public static Optional<Venta> masCara(List<Venta> ventas, String producto) {
        return ventas.stream().filter(v -> v.producto().equals(producto)).max(Comparator.comparingDouble(Venta::total));
    }
}
```

`AnalizadorTest.java`

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.Test;

class AnalizadorTest {
    private static final List<String> LINEAS = List.of(
            "2026-09-10;Centro;ibuprofeno;3;2400",
            "2026-09-10;Norte;alcohol en gel;4;1900",
            "2026-09-11;Sur;ibuprofeno;-1;2400",
            "2026-09-11;Sur;protector solar;2;15800",
            "2026-09-12;Norte;vitamina C;tres;6200",
            "2026-09-12;Centro;alcohol en gel",
            "2026-09-13;Centro;vitamina C;1;6200");

    @Test
    void unaLineaCorrectaEsValida() {
        Analizador.Lectura l = Analizador.leer(1, LINEAS.get(0));
        Analizador.Valida v = assertInstanceOf(Analizador.Valida.class, l);
        assertEquals("Centro", v.venta().sucursal());
        assertEquals(3, v.venta().cantidad());
        assertEquals(7200, v.venta().total(), 0.001);
    }

    @Test
    void lasLineasRotasSeRechazanConSuMotivo() {
        assertEquals("cantidad no positiva: -1", assertInstanceOf(Analizador.Rechazada.class, Analizador.leer(3, LINEAS.get(2))).motivo());
        assertEquals("número inválido: tres", assertInstanceOf(Analizador.Rechazada.class, Analizador.leer(5, LINEAS.get(4))).motivo());
        assertEquals("faltan campos (3 de 5)", assertInstanceOf(Analizador.Rechazada.class, Analizador.leer(6, LINEAS.get(5))).motivo());
    }

    @Test
    void ningunaLineaSePierde() {
        List<Analizador.Lectura> lecturas = Analizador.leerTodas(LINEAS, 0);
        long rechazadas = lecturas.stream().filter(l -> l instanceof Analizador.Rechazada).count();
        assertEquals(LINEAS.size(), Analizador.validas(lecturas).size() + rechazadas);
        assertEquals(3, rechazadas);
    }

    @Test
    void laFacturacionPorSucursalEsCorrecta() {
        Map<String, Double> f = Analizador.facturacionPorSucursal(Analizador.validas(Analizador.leerTodas(LINEAS, 0)));
        assertEquals(Map.of("Centro", 13400.0, "Norte", 7600.0, "Sur", 31600.0), f);
    }

    @Test
    void unaBusquedaSinResultadoDevuelveVacio() {
        List<Analizador.Venta> ventas = Analizador.validas(Analizador.leerTodas(LINEAS, 0));
        assertTrue(Analizador.masCara(ventas, "jarabe").isEmpty());
        assertEquals("Sur", Analizador.masCara(ventas, "protector solar").map(Analizador.Venta::sucursal).orElse("-"));
    }

    @Test
    void enParaleloDaLoMismoQueEnSecuencia() throws Exception {
        assertEquals(Analizador.leerTodas(LINEAS, 0), Analizador.leerEnParalelo(LINEAS, 3));
        assertEquals(Analizador.leerTodas(LINEAS, 0), Analizador.leerEnParalelo(LINEAS, 5));
    }
}
```

### Prueba del sello

#### ¿Por qué conviene que leer una línea devuelva un tipo sellado en lugar de lanzar una excepción?

Porque cada línea termina como válida o rechazada con su motivo, ninguna se pierde, y el compilador sabe que solo hay esas dos opciones.

#### ¿Por qué `split(";", -1)`?

Para que no se descarten los campos vacíos del final y la cuenta de campos sea correcta.

#### ¿Cómo sabés que el procesamiento en paralelo no tiene carreras?

Porque cada tarea procesa su parte sin compartir datos y el resultado combinado es idéntico al secuencial (y hay una prueba que lo compara).

#### ¿Por qué las búsquedas devuelven `Optional`?

Porque puede no haber resultado; así quien las usa está obligado a decidir qué hacer en ese caso.

### Soluciones (docente)

Jefe de la Senda de las Corrientes. El ejemplo y la M1 imprimen todo desde el `main` (salida determinista); la M2 separa la lógica y la prueba con JUnit. Se corrige mirando que no se pierdan líneas, que no haya `get()` ni `null`, y corriendo las pruebas.
