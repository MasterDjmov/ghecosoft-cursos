# RAMA R05 · La Torre del Arquitecto: diseño, Spring y el examen

```meta
tipo: tronco
posicion: 5
```

## R05-N01 · Eficiencia: Big O y medir tiempos

```meta
tipo: tema
padre: R04-N06
precio: 10
criatura: ogre
temas: alg.complejidad
usa: col.listas, col.mapas, col.conjuntos
```

### Crónica

Con el vitral del viajero envuelto en lona, Zed sube a la **Torre del Arquitecto**, donde {mentor} dibuja los planos del Imperio. En el primer piso, la **sala de las balanzas del tiempo**, dos aprendices discuten a los gritos cuál de sus algoritmos es más rápido. Cada uno jura que el suyo.

—No discutan: **midan** —dice {mentor}, y les deja un reloj sobre la mesa—. Y después piensen **cómo crece**: con diez datos cualquier cosa anda. La pregunta es qué pasa con un millón. Vos también, Zed: ya no alcanza con que funcione.

### Objetivos

- Medir el tiempo de un programa con `System.nanoTime()` y conocer sus trampas.
- Contar las operaciones de un algoritmo y expresar cómo crecen con la notación **O grande**.
- Reconocer O(1), O(log n), O(n), O(n log n) y O(n²) en código de verdad.
- Elegir la colección adecuada por el costo de sus operaciones (`ArrayList`, `HashMap`, `HashSet`, `TreeMap`).

### Antes de empezar

- Listas, mapas y conjuntos (rama 3).
- Streams y concurrencia (rama 4).

### Explicación

#### Medir con el reloj
`System.nanoTime()` da un instante en nanosegundos. Restando dos, sabés cuánto tardó algo:
```java
long inicio = System.nanoTime();
ordenar(datos);
long ms = (System.nanoTime() - inicio) / 1_000_000;
System.out.println("Tardó " + ms + " ms");
```
Tres trampas: la primera vez Java es más lento (está compilando el código caliente), cada medición
varía según lo que haga la compu en ese momento, y con pocos datos no se ve nada. Medí varias veces,
con datos grandes, y mirá la **tendencia**, no un número suelto.

#### Contar pasos: la notación O grande
Como el tiempo depende de la máquina, los algoritmos se comparan **contando operaciones** en función
de la cantidad de datos, *n*. La **O grande** dice cómo crece esa cuenta cuando *n* crece, sin
importar las constantes:

| Orden | Nombre | Ejemplo | Con n = 1.000.000 |
|---|---|---|---|
| O(1) | constante | `lista.get(i)`, `mapa.get(k)`, `set.contains(x)` | 1 paso |
| O(log n) | logarítmico | búsqueda binaria en un array ordenado, `TreeMap.get` | unos 20 pasos |
| O(n) | lineal | recorrer una lista, `lista.contains(x)` | un millón |
| O(n log n) | casi lineal | `Collections.sort`, `Arrays.sort` | unos 20 millones |
| O(n²) | cuadrático | dos bucles anidados sobre los mismos datos | un billón |

#### Cómo se lee en el código
```java
for (int i = 0; i < n; i++) { … }                      // un bucle: O(n)
for (int i = 0; i < n; i++)                            // dos bucles anidados: O(n²)
    for (int j = i + 1; j < n; j++) { … }
while (desde <= hasta) { medio = …; /* descarta la mitad */ }   // partir a la mitad: O(log n)
```
Lo que manda es el término que **más crece**: un O(n) seguido de un O(n²) es O(n²).

#### El costo de las colecciones
| Operación | `ArrayList` | `HashMap` / `HashSet` | `TreeMap` / `TreeSet` |
|---|---|---|---|
| buscar por posición | O(1) | — | — |
| ¿está? / buscar por clave | O(n) | O(1) | O(log n) |
| agregar al final | O(1) | O(1) | O(log n) |
| recorrer en orden | sí | sin orden | ordenado |

Por eso, **para buscar por código** se usa un `HashMap`, y **para detectar repetidos** en una sola
pasada, un `HashSet`: con dos bucles es O(n²); con el conjunto, O(n). En el examen final se pide
exactamente eso: depurar duplicados «en una sola pasada».

### Código de ejemplo

```java
/*
 * Eficiencia: contar pasos en lugar de adivinar. Búsqueda lineal contra binaria y
 * duplicados con dos bucles contra un HashSet.
 */
import java.util.HashSet;
import java.util.Set;

public class Balanzas {
    static int pasos;

    static int lineal(int[] datos, int buscado) {
        for (int i = 0; i < datos.length; i++) {
            pasos++;
            if (datos[i] == buscado) {
                return i;
            }
        }
        return -1;
    }

    static int binaria(int[] ordenados, int buscado) {
        int desde = 0;
        int hasta = ordenados.length - 1;
        while (desde <= hasta) {
            pasos++;
            int medio = (desde + hasta) / 2;
            if (ordenados[medio] == buscado) {
                return medio;
            } else if (ordenados[medio] < buscado) {
                desde = medio + 1;
            } else {
                hasta = medio - 1;
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        for (int n : new int[] {1_000, 1_000_000}) {
            int[] datos = new int[n];
            for (int i = 0; i < n; i++) {
                datos[i] = i * 2;
            }
            int buscado = datos[n - 1];
            pasos = 0;
            lineal(datos, buscado);
            int pasosLineal = pasos;
            pasos = 0;
            binaria(datos, buscado);
            System.out.printf("n = %d: lineal %d pasos, binaria %d pasos%n", n, pasosLineal, pasos);
        }

        String[] pasaportes = {"A1", "B2", "A1", "C3", "B2", "D4"};
        long comparaciones = 0;
        for (int i = 0; i < pasaportes.length; i++) {
            for (int j = i + 1; j < pasaportes.length; j++) {
                comparaciones++;
            }
        }
        Set<String> vistos = new HashSet<>();
        int repetidos = 0;
        for (String p : pasaportes) {
            if (!vistos.add(p)) {
                repetidos++;
            }
        }
        System.out.println("Duplicados con dos bucles: " + comparaciones + " comparaciones");
        System.out.println("Duplicados con HashSet: " + pasaportes.length + " pasos, " + repetidos + " repetidos");
    }
}
```

### Salida esperada

```
n = 1000: lineal 1000 pasos, binaria 10 pasos
n = 1000000: lineal 1000000 pasos, binaria 20 pasos
Duplicados con dos bucles: 15 comparaciones
Duplicados con HashSet: 6 pasos, 2 repetidos
```

### ¿Para qué sirve?

Con los datos de una clase práctica, cualquier algoritmo anda. Con los de una empresa (millones de clientes, de ventas, de registros), un O(n²) tarda horas y un O(n) segundos. Saber leer la O grande te deja elegir la colección correcta, explicar por qué tu solución escala y responder la pregunta que aparece en todas las entrevistas y en el examen: «¿cuál es la complejidad de tu solución?».

### Errores habituales

**Ogro: el `contains` adentro de un bucle.** `lista.contains(x)` recorre la lista entera: adentro
de un `for` sobre la misma lista, el programa es O(n²) aunque se vea un solo bucle. Con un
`HashSet` es O(1).

**Goblin: medir una sola vez.** Un número suelto de `nanoTime` no dice nada: la primera ejecución
es más lenta y cada una varía. Medí varias veces con datos grandes.

**Troll: la búsqueda binaria en datos desordenados.** Solo funciona si el array está ordenado; si
no, devuelve cualquier cosa sin dar error.

**Slime: optimizar antes de tiempo.** Primero que funcione y sea claro; después medí y mejorá
lo que de verdad tarda.

### Micro-misión R05-N01-P1 · No discutan: cuenten

```meta
lugar: La sala de las balanzas del tiempo
personajes: Zed, Gheco, Nadia, Kaffa
carta: Contar pasos | un contador adentro del bucle · cuántas vueltas da según n · eso es lo que mide la O grande
recompensa: xp 10, oro 10
```

#### Escena
En el primer piso de la Torre, dos aprendices discuten cuál de sus algoritmos es más rápido. Kaffa deja un reloj sobre la mesa, pero Gheco tiene una idea mejor: **contar** cuántos pasos da cada uno.

#### Gheco sugiere
Para comparar algoritmos sin depender de la compu, se cuentan los pasos: una variable `pasos` que suma 1 en cada vuelta. Una búsqueda lineal en el peor caso mira **todos** los elementos.

#### Desafío
Sumá un paso en cada vuelta del bucle.

#### Código inicial
```java
public class Balanza {
    public static void main(String[] args) {
        for (int n : new int[] {10, 100, 1000}) {
            int pasos = 0;
            for (int i = 0; i < n; i++) {
                ___;
            }
            System.out.println("n = " + n + ": " + pasos + " pasos");
        }
    }
}
```

#### Salida esperada
```
n = 10: 10 pasos
n = 100: 100 pasos
n = 1000: 1000 pasos
```

#### Solución
```java
public class Balanza {
    public static void main(String[] args) {
        for (int n : new int[] {10, 100, 1000}) {
            int pasos = 0;
            for (int i = 0; i < n; i++) {
                pasos++;
            }
            System.out.println("n = " + n + ": " + pasos + " pasos");
        }
    }
}
```

#### Al superarla
Diez veces más datos, diez veces más pasos. —Eso es **O(n)** —dice Gheco—: crece igual que los datos. Los aprendices dejan de gritar y se ponen a contar.

#### Imagen
- La sala de las balanzas del tiempo: balanzas de bronce con relojes de arena en vez de pesas.
- Dos aprendices discutiendo; Gheco con un ábaco de luz contando pasos.

### Micro-misión R05-N01-P2 · Dos bucles, n al cuadrado

```meta
lugar: La sala de las balanzas del tiempo
personajes: Zed, Gheco, Nadia, Kaffa
criatura: ogro
carta: O(n²) | un bucle adentro de otro sobre los mismos datos · con el doble de datos, cuatro veces más pasos
recompensa: xp 10, oro 10
```

#### Escena
El segundo aprendiz compara cada pasaporte con todos los demás. Con pocos anda; con muchos, la Aduana entera espera. Un **ogro** sonríe: el programa funciona, pero no termina nunca.

#### Gheco sugiere
Dos bucles anidados que comparan cada par: `for i … for j = i + 1 …`. Los pasos crecen como **n²**: con 10 veces más datos, unas 100 veces más pasos.

#### Desafío
Completá el inicio del bucle de adentro: compara cada uno con los que vienen **después**.

#### Código inicial
```java
public class Cuadrado {
    public static void main(String[] args) {
        for (int n : new int[] {10, 100, 1000}) {
            long pasos = 0;
            for (int i = 0; i < n; i++) {
                for (int j = ___; j < n; j++) {
                    pasos++;
                }
            }
            System.out.println("n = " + n + ": " + pasos + " comparaciones");
        }
    }
}
```

#### Salida esperada
```
n = 10: 45 comparaciones
n = 100: 4950 comparaciones
n = 1000: 499500 comparaciones
```

#### Solución
```java
public class Cuadrado {
    public static void main(String[] args) {
        for (int n : new int[] {10, 100, 1000}) {
            long pasos = 0;
            for (int i = 0; i < n; i++) {
                for (int j = i + 1; j < n; j++) {
                    pasos++;
                }
            }
            System.out.println("n = " + n + ": " + pasos + " comparaciones");
        }
    }
}
```

#### Al superarla
De 45 a casi medio millón. —Con los pasaportes de un día de feria —calcula Nadia—, esto tarda hasta mañana. El ogro aplaude.

#### Imagen
- Una balanza con un plato que se hunde bajo una montaña de comparaciones.
- Nadia haciendo cuentas en su libreta, alarmada; un ogro aplaudiendo.

### Micro-misión R05-N01-P3 · Una sola pasada

```meta
lugar: La sala de las balanzas del tiempo
personajes: Zed, Gheco, Nadia, Kaffa
carta: HashSet en una pasada | vistos.add(p) devuelve false si ya estaba · O(1) cada uno · O(n) en total
recompensa: xp 15, oro 15
```

#### Escena
—Los pasaportes repetidos se encuentran en **una sola pasada** —dice Kaffa—. Es lo que te van a pedir en el examen. Con lo que aprendiste en los Archivos alcanza.

#### Gheco sugiere
Con un `HashSet` de vistos, cada `add` dice en un paso si el pasaporte ya había aparecido (devuelve `false`). Así se recorre la lista **una sola vez**.

#### Desafío
Completá la condición: si no se pudo agregar, es un repetido.

#### Código inicial
```java
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public class UnaPasada {
    public static void main(String[] args) {
        List<String> pasaportes = List.of("AR-101", "UY-202", "AR-101", "CL-303", "UY-202");
        Set<String> vistos = new HashSet<>();
        Set<String> repetidos = new LinkedHashSet<>();
        int pasos = 0;
        for (String p : pasaportes) {
            pasos++;
            if (___) {
                repetidos.add(p);
            }
        }
        System.out.println("Repetidos: " + repetidos);
        System.out.println("Pasos: " + pasos);
    }
}
```

#### Salida esperada
```
Repetidos: [AR-101, UY-202]
Pasos: 5
```

#### Solución
```java
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public class UnaPasada {
    public static void main(String[] args) {
        List<String> pasaportes = List.of("AR-101", "UY-202", "AR-101", "CL-303", "UY-202");
        Set<String> vistos = new HashSet<>();
        Set<String> repetidos = new LinkedHashSet<>();
        int pasos = 0;
        for (String p : pasaportes) {
            pasos++;
            if (!vistos.add(p)) {
                repetidos.add(p);
            }
        }
        System.out.println("Repetidos: " + repetidos);
        System.out.println("Pasos: " + pasos);
    }
}
```

#### Al superarla
Cinco pasaportes, cinco pasos. —«¿Cuál es la complejidad de tu solución?» —pregunta Kaffa, imitando a un profesor. —O(n) —contesta Zed, sin pensarlo.

#### Imagen
- Una fila de pasaportes pasando una sola vez por un arco; dos de ellos se encienden en rojo al pasar.
- Kaffa con anteojos de profesor, sonriendo.

### Micro-misión R05-N01-P4 · Partir a la mitad

```meta
lugar: La sala de las balanzas del tiempo
personajes: Zed, Gheco, Nadia, Kaffa
carta: O(log n) | la búsqueda binaria descarta la mitad en cada paso · un millón de datos, unos 20 pasos · solo con datos ORDENADOS
recompensa: xp 15, oro 20
```

#### Escena
El último aprendiz busca un registro en el archivo ordenado de la Torre: un millón de fichas. No las mira de a una: abre por la mitad, ve si se pasó, y descarta media pila.

#### Gheco sugiere
En la búsqueda binaria, si lo del medio es menor que lo buscado, lo buscado está en la mitad de **arriba**: `desde = medio + 1`. Si es mayor, en la de abajo: `hasta = medio - 1`.

#### Desafío
Completá qué pasa cuando lo del medio es menor que lo buscado.

#### Código inicial
```java
public class Mitad {
    public static void main(String[] args) {
        int n = 1_000_000;
        int[] fichas = new int[n];
        for (int i = 0; i < n; i++) {
            fichas[i] = i * 2;
        }
        int buscado = 1_234_566;
        int desde = 0;
        int hasta = n - 1;
        int pasos = 0;
        int encontrada = -1;
        while (desde <= hasta) {
            pasos++;
            int medio = (desde + hasta) / 2;
            if (fichas[medio] == buscado) {
                encontrada = medio;
                break;
            } else if (fichas[medio] < buscado) {
                ___;
            } else {
                hasta = medio - 1;
            }
        }
        System.out.println("Ficha en la posición " + encontrada + ", en " + pasos + " pasos");
    }
}
```

#### Salida esperada
```
Ficha en la posición 617283, en 20 pasos
```

#### Solución
```java
public class Mitad {
    public static void main(String[] args) {
        int n = 1_000_000;
        int[] fichas = new int[n];
        for (int i = 0; i < n; i++) {
            fichas[i] = i * 2;
        }
        int buscado = 1_234_566;
        int desde = 0;
        int hasta = n - 1;
        int pasos = 0;
        int encontrada = -1;
        while (desde <= hasta) {
            pasos++;
            int medio = (desde + hasta) / 2;
            if (fichas[medio] == buscado) {
                encontrada = medio;
                break;
            } else if (fichas[medio] < buscado) {
                desde = medio + 1;
            } else {
                hasta = medio - 1;
            }
        }
        System.out.println("Ficha en la posición " + encontrada + ", en " + pasos + " pasos");
    }
}
```

#### Al superarla
Un millón de fichas y la encuentra en menos de veinte pasos. Los aprendices se dan la mano.
En el segundo piso, Kaffa abre un plano viejo tan enredado que cambiar una puerta tira una pared.

#### Imagen
- Una pila gigante de fichas que se parte por la mitad una y otra vez hasta dejar una sola brillando.
- Al fondo, una escalera que sube al segundo piso, con planos enrollados en los escalones.

### Misión R05-N01-M1 · Contar pasos

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí la búsqueda **lineal** y la **binaria** sobre un array de `int` ordenado, y contá los
pasos de cada una en una variable `static int pasos` (un paso por cada elemento que miran).
Para *n* = 10, 100, 1.000, 10.000 y 100.000, llená el array con `i * 3` y buscá un valor que
**no está** (`-1`), que es el peor caso. Mostrá la tabla con `printf("%6d %8d %8d%n", …)`.

#### Criterio de aprobación

- La búsqueda binaria descarta la mitad en cada paso (`desde`, `hasta`, `medio`).
- Los pasos se cuentan, no se miden con el reloj: la salida es siempre la misma.
- La salida coincide con la esperada.

#### Salida esperada

```
     n   lineal  binaria
    10       10        3
   100      100        6
  1000     1000        9
 10000    10000       13
100000   100000       16
```

#### Solución de referencia

```java
// Mision 1 - Contar pasos: búsqueda lineal y binaria.
public class ContarPasos {
    static int pasos;

    static int lineal(int[] datos, int buscado) {
        for (int i = 0; i < datos.length; i++) {
            pasos++;
            if (datos[i] == buscado) {
                return i;
            }
        }
        return -1;
    }

    static int binaria(int[] ordenados, int buscado) {
        int desde = 0;
        int hasta = ordenados.length - 1;
        while (desde <= hasta) {
            pasos++;
            int medio = (desde + hasta) / 2;
            if (ordenados[medio] == buscado) {
                return medio;
            } else if (ordenados[medio] < buscado) {
                desde = medio + 1;
            } else {
                hasta = medio - 1;
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        System.out.println("     n   lineal  binaria");
        for (int n : new int[] {10, 100, 1_000, 10_000, 100_000}) {
            int[] datos = new int[n];
            for (int i = 0; i < n; i++) {
                datos[i] = i * 3;
            }
            pasos = 0;
            lineal(datos, -1);
            int l = pasos;
            pasos = 0;
            binaria(datos, -1);
            System.out.printf("%6d %8d %8d%n", n, l, pasos);
        }
    }
}
```

### Misión R05-N01-M2 · Los pasaportes duplicados

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La Aduana recibe la lista de pasaportes del día con repetidos:
`AR-101, UY-202, AR-101, CL-303, UY-202, AR-101, PY-404`. Encontrá los duplicados **de dos
formas** y compará:

1. Con dos bucles anidados, contando las comparaciones.
2. Con un `HashSet` de vistos y un `LinkedHashSet` de duplicados, **en una sola pasada**.

Mostrá los duplicados de cada forma, cuántos pasos hizo cada una y cuántos pasaportes únicos hay.

#### Criterio de aprobación

- La segunda forma recorre la lista una sola vez y usa `add` del conjunto para saber si ya estaba.
- Las dos formas encuentran los mismos duplicados.
- La salida coincide con la esperada.

#### Salida esperada

```
Con dos bucles: [AR-101, UY-202] en 21 comparaciones
Con HashSet: [AR-101, UY-202] en 7 pasos
Únicos: 4
```

#### Solución de referencia

```java
// Mision 2 - Los pasaportes duplicados: O(n²) contra O(n).
import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public class PasaportesDuplicados {
    public static void main(String[] args) {
        List<String> pasaportes = List.of("AR-101", "UY-202", "AR-101", "CL-303", "UY-202", "AR-101", "PY-404");

        long comparaciones = 0;
        List<String> duplicadosLentos = new ArrayList<>();
        for (int i = 0; i < pasaportes.size(); i++) {
            for (int j = i + 1; j < pasaportes.size(); j++) {
                comparaciones++;
                String p = pasaportes.get(i);
                if (p.equals(pasaportes.get(j)) && !duplicadosLentos.contains(p)) {
                    duplicadosLentos.add(p);
                }
            }
        }

        Set<String> vistos = new HashSet<>();
        Set<String> duplicados = new LinkedHashSet<>();
        for (String p : pasaportes) {
            if (!vistos.add(p)) {
                duplicados.add(p);
            }
        }

        System.out.println("Con dos bucles: " + duplicadosLentos + " en " + comparaciones + " comparaciones");
        System.out.println("Con HashSet: " + duplicados + " en " + pasaportes.size() + " pasos");
        System.out.println("Únicos: " + vistos.size());
    }
}
```

### Misión R05-N01-M3 · Buscar por código

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Cargá 50.000 mercancías (`record Mercancia(String codigo, String descripcion)`, con códigos
`M0` a `M49999`) en una **lista** y en un **mapa** por código. Buscá `M10`, `M49999` y `X1`
de las dos formas: en la lista recorriendo (contá los pasos) y en el mapa con `get` (un paso
cada una). Mostrá qué encontraste, comprobá que las dos formas coinciden y mostrá los pasos
totales de cada una.

#### Criterio de aprobación

- La búsqueda en la lista corta con `break` al encontrar.
- El mapa se usa con `get`, sin recorrerlo.
- La salida coincide con la esperada.

#### Salida esperada

```
M10: bulto 10
M49999: bulto 49999
X1: no está
Pasos con la lista: 100011
Pasos con el mapa: 3
```

#### Solución de referencia

```java
// Mision 3 - Buscar por código: lista contra mapa.
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class BuscarPorCodigo {
    record Mercancia(String codigo, String descripcion) { }

    public static void main(String[] args) {
        int n = 50_000;
        List<Mercancia> lista = new ArrayList<>();
        Map<String, Mercancia> mapa = new HashMap<>();
        for (int i = 0; i < n; i++) {
            Mercancia m = new Mercancia("M" + i, "bulto " + i);
            lista.add(m);
            mapa.put(m.codigo(), m);
        }

        String[] buscados = {"M10", "M49999", "X1"};
        long pasosLista = 0;
        for (String codigo : buscados) {
            Mercancia encontrada = null;
            for (Mercancia m : lista) {
                pasosLista++;
                if (m.codigo().equals(codigo)) {
                    encontrada = m;
                    break;
                }
            }
            Mercancia porMapa = mapa.get(codigo);
            System.out.println(codigo + ": " + (porMapa == null ? "no está" : porMapa.descripcion())
                    + (encontrada == porMapa ? "" : " (¡no coinciden!)"));
        }
        System.out.println("Pasos con la lista: " + pasosLista);
        System.out.println("Pasos con el mapa: " + buscados.length);
    }
}
```

### Encargo R05-N01-E1 · Cómo crecen

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Mostrá una tabla con *n*, log₂ *n* (redondeado), *n* log *n* y *n²* para *n* = 10, 100,
1.000, 10.000 y 100.000 (usá `long` para que no se desborde). Al final, mostrá cuántas veces
más grande es *n²* que *n* log *n* con *n* = 100.000, tomando log *n* = 17.

#### Criterio de aprobación

- Usa `long` para los productos grandes.
- La salida coincide con la esperada.

#### Salida esperada

```
       n    log n      n log n            n²
      10        3           30           100
     100        7          700         10000
    1000       10        10000       1000000
   10000       13       130000     100000000
  100000       17      1700000   10000000000
Con n = 100.000, n² es 5882 veces n log n
```

#### Solución de referencia

```java
// Encargo 1 - Cómo crecen: la tabla de las funciones.
public class ComoCrecen {
    public static void main(String[] args) {
        System.out.println("       n    log n      n log n            n²");
        for (int n : new int[] {10, 100, 1_000, 10_000, 100_000}) {
            int log = (int) Math.round(Math.log(n) / Math.log(2));
            System.out.printf("%8d %8d %12d %13d%n", n, log, (long) n * log, (long) n * n);
        }
        System.out.println("Con n = 100.000, n² es " + (100_000L * 100_000L) / (100_000L * 17) + " veces n log n");
    }
}
```

### Prueba del sello

#### ¿Por qué los algoritmos se comparan contando operaciones y no con el reloj?

Porque el tiempo depende de la máquina y de lo que esté haciendo en ese momento; la cantidad de operaciones depende solo del algoritmo y de *n*.

#### ¿Qué complejidad tienen dos bucles anidados que recorren la misma lista?

O(n²): por cada elemento se recorren los demás.

#### ¿Por qué la búsqueda binaria es O(log n)?

Porque en cada paso descarta la mitad de lo que queda: con un millón de datos alcanza con unos 20 pasos.

#### ¿Qué colección usás para saber si un pasaporte ya apareció, y con qué costo?

Un `HashSet`: `add` y `contains` son O(1), y toda la lista se revisa en una sola pasada, O(n).

#### ¿Qué trampas tiene medir con `System.nanoTime()`?

La primera ejecución es más lenta, cada medición varía y con pocos datos no se ve la diferencia: hay que medir varias veces y con datos grandes.


### Soluciones (docente)

Nodo nuevo (D96): el programa de la cátedra pide eficiencia y Big O en la unidad 3, y el examen pide depurar duplicados «en una sola pasada». Las misiones cuentan pasos en lugar de medir tiempos, para que la salida sea verificable; en clase conviene mostrar además una medición con `nanoTime` y comentar por qué varía.

## R05-N02 · Principios SOLID

```meta
tipo: tema
padre: R05-N01
precio: 10
criatura: troll
temas: diseno.solid
usa: poo.interfaces, diseno.patrones
```

### Crónica

En el segundo piso de la Torre están los **planos viejos**: uno tan enredado que cambiar una puerta tira una pared, otro donde la cocina también es la armería y el dormitorio. Nadie se anima a tocarlos. Zed, que entraba a las casas por cualquier lado, ve por primera vez el problema desde adentro.

—Hay cinco reglas para que un plano dure —dice {mentor}, y las anota en la pizarra con tiza—. Se llaman **SOLID**. La última es la más importante: **no fabriques lo que usás; pedilo**. Arriba, en el piso del contenedor, vas a ver por qué.

### Objetivos

- Conocer los cinco principios SOLID y reconocer cuándo se rompen.
- Separar responsabilidades: una clase, una razón para cambiar.
- Extender sin modificar con interfaces (y Strategy).
- Diseñar subtipos que cumplen lo que prometen y interfaces chicas.
- Depender de abstracciones y recibir las dependencias por el constructor.

### Antes de empezar

- Interfaces y polimorfismo (rama 2).
- Patrones de diseño (rama 4).
- Eficiencia: Big O y medir tiempos.

### Explicación

#### S: responsabilidad única
Una clase tiene **una sola razón para cambiar**. Si `Informe` calcula los totales, arma el texto y
lo guarda en un archivo, cualquier cambio en cualquiera de las tres cosas la toca. Separada en
`CalculadoraVentas`, `FormateadorInforme` y un guardador, cada cambio toca una sola clase.

#### O: abierta a la extensión, cerrada a la modificación
Agregar un comportamiento nuevo **no debería obligar a editar** lo que ya anda. Un `switch` con cada
tipo de descuento crece para siempre; una interfaz `Descuento` con una clase por descuento (una
Strategy) se extiende **agregando** una clase:
```java
interface Descuento { double aplicar(double precio); }
record Peregrino() implements Descuento { public double aplicar(double p) { return p * 0.5; } }
// mañana: record Gremio() implements Descuento { … }  — cobrar(...) no se toca
```

#### L: sustitución de Liskov
Donde se usa un tipo, tiene que poder ir **cualquier subtipo** sin sorpresas. El ejemplo clásico:
si `Cuadrado extends Rectangulo` y `setAncho` también cambia el alto, un método que espera un
rectángulo se rompe. Si un hijo no puede cumplir lo que promete el padre, la herencia está mal.

#### I: segregación de interfaces
Mejor **varias interfaces chicas** que una gorda. Una impresora común no debería verse obligada a
implementar `escanear()` y `enviarFax()` para cumplir un contrato: `Imprime` y `Escanea` por
separado, y la multifunción firma las dos.

#### D: inversión de dependencias
Las clases importantes dependen de **interfaces**, no de clases concretas, y **reciben** sus piezas
en lugar de crearlas:
```java
class ServicioReservas {
    private final Avisador avisador;                       // una interfaz
    ServicioReservas(Avisador avisador) {                  // se la pasan de afuera
        this.avisador = avisador;
    }
}
new ServicioReservas(new AvisadorPorMail());               // en producción
new ServicioReservas(new AvisadorDePrueba());              // en las pruebas
```
Es exactamente lo que hace **Spring** en el piso de arriba: el contenedor crea las piezas y se las
pasa al constructor de cada servicio (con Lombok, `@RequiredArgsConstructor`).

### Código de ejemplo

```java
/*
 * SOLID en un servicio chico: cada clase una responsabilidad, el cálculo abierto a extensiones,
 * interfaces chicas y el servicio que recibe sus piezas por el constructor.
 */
import java.util.ArrayList;
import java.util.List;

public class PlanosQueDuran {
    public static void main(String[] args) {
        Repositorio repo = new RepositorioEnMemoria();
        ServicioDeclaraciones servicio = new ServicioDeclaraciones(repo, new TarifaComun());
        servicio.declarar(new Declaracion("Baldo", 200));
        servicio.declarar(new Declaracion("Nadia", 50));
        servicio.setTarifa(new TarifaFeria());
        servicio.declarar(new Declaracion("Zed", 200));
        new Informe().imprimir(repo.todas());
    }
}

record Declaracion(String viajero, double valor) { }

record Liquidacion(String viajero, double impuesto) { }

interface Tarifa {                                    // O: se agregan tarifas sin tocar el servicio
    double impuesto(double valor);
}

class TarifaComun implements Tarifa {
    public double impuesto(double valor) { return valor * 0.10; }
}

class TarifaFeria implements Tarifa {
    public double impuesto(double valor) { return valor * 0.05; }
}

interface Repositorio {                               // I y D: una interfaz chica, de la que depende el servicio
    void guardar(Liquidacion l);

    List<Liquidacion> todas();
}

class RepositorioEnMemoria implements Repositorio {
    private final List<Liquidacion> datos = new ArrayList<>();

    public void guardar(Liquidacion l) { datos.add(l); }

    public List<Liquidacion> todas() { return List.copyOf(datos); }
}

class ServicioDeclaraciones {                         // S: solo liquida
    private final Repositorio repositorio;
    private Tarifa tarifa;

    ServicioDeclaraciones(Repositorio repositorio, Tarifa tarifa) {   // D: recibe sus piezas
        this.repositorio = repositorio;
        this.tarifa = tarifa;
    }

    void setTarifa(Tarifa tarifa) { this.tarifa = tarifa; }

    void declarar(Declaracion d) {
        repositorio.guardar(new Liquidacion(d.viajero(), tarifa.impuesto(d.valor())));
    }
}

class Informe {                                       // S: solo muestra
    void imprimir(List<Liquidacion> liquidaciones) {
        liquidaciones.forEach(l -> System.out.println(l.viajero() + ": " + l.impuesto() + " denarios"));
    }
}
```

### Salida esperada

```
Baldo: 20.0 denarios
Nadia: 5.0 denarios
Zed: 10.0 denarios
```

### ¿Para qué sirve?

SOLID es la diferencia entre un programa que se puede cambiar y uno que da miedo tocar. Es lo que se espera en las capas del examen final (controller, service, repositorio y DTO, cada uno con lo suyo), lo que piden las empresas en las entrevistas y lo que hace posible probar cada pieza por separado. Spring está construido sobre la D: si entendés la inversión de dependencias, entendés Spring.

### Errores habituales

**Troll: la clase que hace todo.** Un `Sistema` con quinientas líneas que lee, calcula, valida,
guarda y muestra. Cualquier cambio rompe algo lejos.

**Ogro: el `switch` que crece.** Cada tipo nuevo agrega un `case` en cinco lugares. Con una
interfaz, se agrega una clase.

**Goblin: el hijo que no cumple.** Un subtipo que tira `UnsupportedOperationException` en un
método del padre rompe Liskov: la jerarquía está mal.

**Esqueleto: el `new` escondido.** Un servicio que hace `new RepositorioMySQL()` adentro no se
puede probar sin la base: pedilo por el constructor.

### Micro-misión R05-N02-P1 · La cocina que también es armería

```meta
lugar: La sala de los planos viejos
personajes: Zed, Gheco, Nadia, Kaffa
criatura: troll
carta: S: responsabilidad única | una clase, una razón para cambiar · calcular, formatear y mostrar van en clases distintas
recompensa: xp 10, oro 10
```

#### Escena
En un plano viejo, la cocina también es la armería y el dormitorio. En el código del mismo arquitecto, una clase calcula, formatea y muestra. Un **troll** vive cómodo en ese desorden.

#### Gheco sugiere
Separá: una clase **calcula** y otra **formatea**. Así, si cambia el formato, no tocás la cuenta. El `main` solo conecta las piezas.

#### Desafío
Completá la llamada al formateador con el total calculado.

#### Código inicial
```java
public class Separar {
    public static void main(String[] args) {
        int[] tasas = {120, 80, 40};
        int total = new Calculadora().total(tasas);
        String texto = ___;
        System.out.println(texto);
    }
}

class Calculadora {
    int total(int[] montos) {
        int t = 0;
        for (int m : montos) {
            t += m;
        }
        return t;
    }
}

class Formateador {
    String formatear(int total) {
        return "Tasas del día: " + total + " denarios";
    }
}
```

#### Salida esperada
```
Tasas del día: 240 denarios
```

#### Solución
```java
public class Separar {
    public static void main(String[] args) {
        int[] tasas = {120, 80, 40};
        int total = new Calculadora().total(tasas);
        String texto = new Formateador().formatear(total);
        System.out.println(texto);
    }
}

class Calculadora {
    int total(int[] montos) {
        int t = 0;
        for (int m : montos) {
            t += m;
        }
        return t;
    }
}

class Formateador {
    String formatear(int total) {
        return "Tasas del día: " + total + " denarios";
    }
}
```

#### Al superarla
Cada clase en su habitación. El troll se queda sin rincón donde esconderse. —**S** —anota Kaffa en la pizarra.

#### Imagen
- Un plano viejo partido en tres habitaciones nuevas, cada una con su cartel: «calcular», «formatear», «mostrar».
- Kaffa escribiendo una S enorme en la pizarra.

### Micro-misión R05-N02-P2 · Agregar sin romper

```meta
lugar: La sala de los planos viejos
personajes: Zed, Gheco, Nadia, Kaffa
carta: O: abierto/cerrado | lo nuevo se AGREGA (una clase que implementa la interfaz) · lo que ya anda no se toca
recompensa: xp 15, oro 15
```

#### Escena
La Torre agrega un descuento nuevo cada semana. En el código viejo, cada uno era un `case` más en un `switch` gigante. Kaffa le pide a Zed que agregue el del **Gremio** sin tocar `cobrar`.

#### Gheco sugiere
Con una interfaz `Descuento`, cada descuento es una clase. Para agregar el del Gremio (15 menos) alcanza con **una clase nueva**; `cobrar` sigue igual.

#### Desafío
Completá el `aplicar` del descuento del Gremio: 15 denarios menos.

#### Código inicial
```java
public class Abierto {
    static double cobrar(double precio, Descuento d) {
        return d.aplicar(precio);
    }

    public static void main(String[] args) {
        System.out.println("Peregrino: " + cobrar(100, new Peregrino()));
        System.out.println("Gremio: " + cobrar(100, new Gremio()));
    }
}

interface Descuento {
    double aplicar(double precio);
}

class Peregrino implements Descuento {
    public double aplicar(double precio) { return precio * 0.5; }
}

class Gremio implements Descuento {
    public double aplicar(double precio) { return ___; }
}
```

#### Salida esperada
```
Peregrino: 50.0
Gremio: 85.0
```

#### Solución
```java
public class Abierto {
    static double cobrar(double precio, Descuento d) {
        return d.aplicar(precio);
    }

    public static void main(String[] args) {
        System.out.println("Peregrino: " + cobrar(100, new Peregrino()));
        System.out.println("Gremio: " + cobrar(100, new Gremio()));
    }
}

interface Descuento {
    double aplicar(double precio);
}

class Peregrino implements Descuento {
    public double aplicar(double precio) { return precio * 0.5; }
}

class Gremio implements Descuento {
    public double aplicar(double precio) { return precio - 15; }
}
```

#### Al superarla
Un descuento nuevo y `cobrar` no se enteró. —**O** —anota Kaffa—. Abierto para agregar, cerrado para tocar. Es la Strategy del astillero, con otro nombre.

#### Imagen
- Un plano con una habitación nueva agregada en el borde, sin tocar las demás.
- Zed con una regla y un lápiz, satisfecho.

### Micro-misión R05-N02-P3 · El hijo que no cumple

```meta
lugar: La sala de los planos viejos
personajes: Zed, Gheco, Nadia, Kaffa
criatura: goblin
carta: L: Liskov | donde va el padre, tiene que poder ir cualquier hijo sin sorpresas · si el hijo no puede cumplir, la herencia está mal
recompensa: xp 15, oro 15
```

#### Escena
En un plano viejo, el `Avestruz` hereda de `Ave`… y `volar()` tira un error. Cada vez que alguien hace volar a todas las aves, el programa explota. Un **goblin** se esconde en esa herencia.

#### Gheco sugiere
Si no todas las aves vuelan, `volar()` no va en `Ave`: va en una interfaz `Voladora` que firman solo las que pueden. Así, donde se espera una `Voladora`, ninguna falla.

#### Desafío
Completá el tipo de la lista: solo las que pueden volar.

#### Código inicial
```java
import java.util.List;

public class Liskov {
    public static void main(String[] args) {
        List<___> bandada = List.of(new Paloma(), new Grifo());
        for (Voladora v : bandada) {
            System.out.println(v.volar());
        }
        System.out.println(new Avestruz().correr());
    }
}

interface Voladora {
    String volar();
}

class Paloma implements Voladora {
    public String volar() { return "la paloma vuela bajo"; }
}

class Grifo implements Voladora {
    public String volar() { return "el grifo vuela en espiral"; }
}

class Avestruz {
    String correr() { return "el avestruz corre, no vuela"; }
}
```

#### Salida esperada
```
la paloma vuela bajo
el grifo vuela en espiral
el avestruz corre, no vuela
```

#### Solución
```java
import java.util.List;

public class Liskov {
    public static void main(String[] args) {
        List<Voladora> bandada = List.of(new Paloma(), new Grifo());
        for (Voladora v : bandada) {
            System.out.println(v.volar());
        }
        System.out.println(new Avestruz().correr());
    }
}

interface Voladora {
    String volar();
}

class Paloma implements Voladora {
    public String volar() { return "la paloma vuela bajo"; }
}

class Grifo implements Voladora {
    public String volar() { return "el grifo vuela en espiral"; }
}

class Avestruz {
    String correr() { return "el avestruz corre, no vuela"; }
}
```

#### Al superarla
Nadie le pide al avestruz que vuele, y nada explota. —**L** y, de paso, **I** —dice Kaffa—: interfaces chicas, que cada uno firme solo lo que puede cumplir.

#### Imagen
- Una paloma y un grifo volando; abajo, un avestruz corriendo feliz por el piso de la Torre.
- Un goblin escondido detrás de un plano tachado que decía «Avestruz extends Ave».

### Micro-misión R05-N02-P4 · No lo fabriques: pedilo

```meta
lugar: La sala de los planos viejos
personajes: Zed, Gheco, Nadia, Kaffa
carta: D: inversión de dependencias | la clase depende de una INTERFAZ y la RECIBE por el constructor · no hace new de lo que usa
recompensa: xp 15, oro 20
```

#### Escena
—La última regla es la más importante —dice Kaffa, y la subraya dos veces—: **no fabriques lo que usás; pedilo**. El servicio de reservas no crea su avisador: se lo dan. Así funciona con el de la Torre y con uno de prueba.

#### Gheco sugiere
El servicio guarda un `Avisador` (una interfaz) y lo recibe por el constructor: `new ServicioReservas(avisador)`. Así, el mismo servicio funciona con cualquier avisador, también con una lambda.

#### Desafío
Completá el constructor del servicio pasándole el avisador.

#### Código inicial
```java
public class Inversion {
    public static void main(String[] args) {
        Avisador torre = mensaje -> System.out.println("[Torre] " + mensaje);
        ServicioReservas servicio = ___;
        servicio.reservar("Zed", 2);
    }
}

interface Avisador {
    void avisar(String mensaje);
}

class ServicioReservas {
    private final Avisador avisador;

    ServicioReservas(Avisador avisador) {
        this.avisador = avisador;
    }

    void reservar(String viajero, int noches) {
        avisador.avisar(viajero + " reservó " + noches + " noches en la Torre");
    }
}
```

#### Salida esperada
```
[Torre] Zed reservó 2 noches en la Torre
```

#### Solución
```java
public class Inversion {
    public static void main(String[] args) {
        Avisador torre = mensaje -> System.out.println("[Torre] " + mensaje);
        ServicioReservas servicio = new ServicioReservas(torre);
        servicio.reservar("Zed", 2);
    }
}

interface Avisador {
    void avisar(String mensaje);
}

class ServicioReservas {
    private final Avisador avisador;

    ServicioReservas(Avisador avisador) {
        this.avisador = avisador;
    }

    void reservar(String viajero, int noches) {
        avisador.avisar(viajero + " reservó " + noches + " noches en la Torre");
    }
}
```

#### Al superarla
El servicio no sabe quién avisa, y no le hace falta. —**D** —termina Kaffa, y la pizarra queda llena: S, O, L, I, D.
—En el piso de arriba —agrega—, hay alguien que se dedica solo a eso: fabricar las piezas y pasárselas a cada uno.

#### Imagen
- La pizarra de la Torre con las cinco letras SOLID escritas con tiza, la D subrayada dos veces.
- Kaffa señalando hacia el techo, donde se oye el ruido de una grúa.

### Misión R05-N02-M1 · Una sola razón para cambiar

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

En la Torre hay una clase que calcula el total de las ventas, arma el texto del informe y lo
anuncia, todo junto. Separala en tres clases con **una responsabilidad cada una**:
`CalculadoraVentas` (`int total(List<Venta>)`), `FormateadorInforme`
(`String formatear(int cantidad, int total)`) y `Pregonero` (`void anunciar(String texto)`,
que muestra `[Torre] …`). Con las ventas `Capital 120`, `Puerto 80` y `Capital 40`, el `main`
usa las tres y anuncia el informe.

#### Criterio de aprobación

- Cada clase hace una sola cosa: ninguna calcula y muestra a la vez.
- El `main` solo conecta las piezas.
- La salida coincide con la esperada.

#### Salida esperada

```
[Torre] Ventas: 3 | Total: 240 denarios
```

#### Solución de referencia

```java
// Mision 1 - Una sola razón para cambiar (S).
import java.util.List;

public class UnaRazon {
    public static void main(String[] args) {
        List<Venta> ventas = List.of(new Venta("Capital", 120), new Venta("Puerto", 80), new Venta("Capital", 40));
        int total = new CalculadoraVentas().total(ventas);
        String texto = new FormateadorInforme().formatear(ventas.size(), total);
        new Pregonero().anunciar(texto);
    }
}

record Venta(String ciudad, int monto) { }

class CalculadoraVentas {
    int total(List<Venta> ventas) {
        return ventas.stream().mapToInt(Venta::monto).sum();
    }
}

class FormateadorInforme {
    String formatear(int cantidad, int total) {
        return "Ventas: " + cantidad + " | Total: " + total + " denarios";
    }
}

class Pregonero {
    void anunciar(String texto) {
        System.out.println("[Torre] " + texto);
    }
}
```

### Misión R05-N02-M2 · Abierto para agregar

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El cobro de la Torre tiene descuentos que no paran de aparecer. Declará la interfaz
`Descuento` con `double aplicar(double precio)` y tres implementaciones: `SinDescuento`, `Peregrino`
(paga la mitad) y `Gremio` (15 denarios menos). Un método `cobrar(double precio, Descuento d)`
aplica el descuento **sin ningún `if` ni `switch`**. Mostrá cuánto paga un precio de 100 con
cada descuento, con el nombre simple de la clase.

#### Criterio de aprobación

- Agregar un descuento nuevo es agregar una clase: `cobrar` no se toca.
- No hay `if`, `switch` ni `instanceof` sobre el tipo de descuento.
- La salida coincide con la esperada.

#### Salida esperada

```
SinDescuento: 100.0
Peregrino: 50.0
Gremio: 85.0
```

#### Solución de referencia

```java
// Mision 2 - Abierto para agregar, cerrado para tocar (O).
import java.util.List;

public class AbiertoCerrado {
    interface Descuento {
        double aplicar(double precio);
    }

    record SinDescuento() implements Descuento {
        public double aplicar(double precio) { return precio; }
    }

    record Peregrino() implements Descuento {
        public double aplicar(double precio) { return precio * 0.5; }
    }

    record Gremio() implements Descuento {
        public double aplicar(double precio) { return precio - 15; }
    }

    static double cobrar(double precio, Descuento d) {
        return d.aplicar(precio);
    }

    public static void main(String[] args) {
        for (Descuento d : List.of(new SinDescuento(), new Peregrino(), new Gremio())) {
            System.out.println(d.getClass().getSimpleName() + ": " + cobrar(100, d));
        }
    }
}
```

### Misión R05-N02-M3 · No fabriques lo que usás

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El `ServicioReservas` avisa cada reserva. Hacé que **dependa de una interfaz** `Avisador`
(`void avisar(String mensaje)`) recibida por el constructor, en lugar de crear él su forma de
avisar. Probalo con dos avisadores: uno de consola (una lambda que muestra `Consola: …`) y un
`AvisadorDePrueba` que **guarda** los avisos en una lista. Una reserva con 0 noches o menos se
rechaza con el aviso `reserva rechazada para …`. Reservá a Zed (3 noches) con el de consola, y a
Nadia (1) y a Baldo (0) con el de prueba, y mostrá lo que guardó.

#### Criterio de aprobación

- `ServicioReservas` no hace ningún `new` de un avisador: lo recibe.
- El mismo servicio funciona con los dos avisadores sin cambios.
- La salida coincide con la esperada.

#### Salida esperada

```
Consola: Zed reservó 3 noches
Avisos guardados en la prueba: [Nadia reservó 1 noche, reserva rechazada para Baldo]
```

#### Solución de referencia

```java
// Mision 3 - No fabriques lo que usás: pedilo (D).
import java.util.ArrayList;
import java.util.List;

public class Inversion {
    public static void main(String[] args) {
        Avisador deConsola = mensaje -> System.out.println("Consola: " + mensaje);
        AvisadorDePrueba dePrueba = new AvisadorDePrueba();

        new ServicioReservas(deConsola).reservar("Zed", 3);
        ServicioReservas paraProbar = new ServicioReservas(dePrueba);
        paraProbar.reservar("Nadia", 1);
        paraProbar.reservar("Baldo", 0);
        System.out.println("Avisos guardados en la prueba: " + dePrueba.avisos);
    }
}

interface Avisador {
    void avisar(String mensaje);
}

class AvisadorDePrueba implements Avisador {
    final List<String> avisos = new ArrayList<>();

    public void avisar(String mensaje) { avisos.add(mensaje); }
}

class ServicioReservas {
    private final Avisador avisador;

    ServicioReservas(Avisador avisador) {
        this.avisador = avisador;
    }

    void reservar(String viajero, int noches) {
        if (noches <= 0) {
            avisador.avisar("reserva rechazada para " + viajero);
            return;
        }
        avisador.avisar(viajero + " reservó " + noches + (noches == 1 ? " noche" : " noches"));
    }
}
```

### Encargo R05-N02-E1 · Interfaces chicas

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

En la oficina de la Torre hay impresoras comunes y multifunción. En lugar de una interfaz gorda
con `imprimir` y `escanear`, declará dos chicas: `Imprime` y `Escanea`. La `Impresora` firma solo
`Imprime`; la `Multifuncion`, las dos. Imprimí el «pasaporte de Zed» con una lista de `Imprime`
que tenga una de cada una, y escaneá el «vitral del Vidriero» con la multifunción vista como
`Escanea`.

#### Criterio de aprobación

- Ninguna clase implementa un método que no sabe hacer (nada de `UnsupportedOperationException`).
- La multifunción se usa donde se espera cualquiera de las dos interfaces.
- La salida coincide con la esperada.

#### Salida esperada

```
impreso: pasaporte de Zed
impreso en color: pasaporte de Zed
escaneado: vitral del Vidriero
```

#### Solución de referencia

```java
// Encargo 1 - Interfaces chicas y subtipos que cumplen (I y L).
import java.util.List;

public class Chicas {
    interface Imprime {
        String imprimir(String doc);
    }

    interface Escanea {
        String escanear(String doc);
    }

    static class Impresora implements Imprime {
        public String imprimir(String doc) { return "impreso: " + doc; }
    }

    static class Multifuncion implements Imprime, Escanea {
        public String imprimir(String doc) { return "impreso en color: " + doc; }

        public String escanear(String doc) { return "escaneado: " + doc; }
    }

    public static void main(String[] args) {
        List<Imprime> impresoras = List.of(new Impresora(), new Multifuncion());
        for (Imprime i : impresoras) {
            System.out.println(i.imprimir("pasaporte de Zed"));
        }
        Escanea escaner = new Multifuncion();
        System.out.println(escaner.escanear("vitral del Vidriero"));
    }
}
```

### Prueba del sello

#### ¿Qué dice el principio de responsabilidad única?

Que una clase tiene una sola razón para cambiar: si hace dos cosas que cambian por motivos distintos, hay que separarla.

#### ¿Cómo se agrega un comportamiento nuevo sin modificar el código que ya anda?

Con una interfaz y una clase nueva que la implementa (abierto/cerrado): el código que usa la interfaz no se toca.

#### Dá un ejemplo de algo que rompe el principio de Liskov.

Un `Cuadrado` que hereda de `Rectangulo` y cambia el alto al cambiar el ancho, o un hijo que tira `UnsupportedOperationException` en un método del padre.

#### ¿Por qué conviene recibir las dependencias por el constructor?

Porque la clase depende de una interfaz y no de una implementación: se puede usar con otra (por ejemplo, una de prueba) sin cambiarla. Es lo que hace Spring.

#### ¿Qué principio rompe una interfaz con diez métodos que casi nadie usa todos?

El de segregación de interfaces: conviene dividirla en interfaces chicas.


### Soluciones (docente)

Nodo nuevo (D96): el programa de la cátedra pide SOLID en la unidad 3, y el examen evalúa las capas y la Strategy. La M3 es la base de la inyección de dependencias del nodo siguiente; vale la pena mostrar en clase que `AvisadorDePrueba` es lo mismo que un *mock*.

## R05-N03 · Maven y el contenedor de Spring

```meta
tipo: tema
padre: R05-N02
criatura: slime
ejecutable: no
temas: fw.spring, diseno.inyeccion
usa: cal.build
precio: 10
```

### Crónica

En el tercer piso de la Torre hay un taller que arma solo: nadie fabrica sus propias piezas. Una grúa gigante, el **Contenedor**, sabe qué pieza va en cada lugar y la coloca. Los maestros solo dicen *"necesito un timonel y una brújula"*, y el Contenedor se los entrega armados. Por la ventana, lejos, se ve el Puerto: la casa de Zed.

—Hasta ahora hacías `new` de todo y conectabas las piezas vos —dice {mentor}—. En el Puerto, **Spring** crea los objetos y se los pasa a quien los necesita. Y **Maven** trae las bibliotecas del mundo sin que copies un solo `.jar`. Es la forma en que se hacen hoy la mayoría de los sistemas en Java, Zed.

### Objetivos

- Entender qué hace Maven: el `pom.xml`, las dependencias y la estructura de carpetas.
- Crear un proyecto de Spring Boot y correrlo.
- Entender la inversión de control y la inyección de dependencias por constructor.
- Usar `@Component`, `@Service`, `@Repository`, `@Value` y `application.properties`.
- Probar los componentes con JUnit, con y sin Spring.

### Antes de empezar

- Interfaces, paquetes, JUnit y el patrón DAO del tronco.
- Instalar un IDE con soporte de Maven (IntelliJ IDEA Community, VS Code con el
  *Extension Pack for Java* o NetBeans). Los proyectos traen el *Maven Wrapper*
  (`mvnw`), así que no hace falta instalar Maven aparte.

### Explicación

#### Maven: el que trae las bibliotecas
En la bóveda copiaste a mano el `.jar` del driver de PostgreSQL. Con diez bibliotecas,
cada una con sus propias dependencias, eso es imposible. **Maven** lo resuelve: en un
archivo `pom.xml` decís **qué** bibliotecas usás y Maven las baja (con todo lo que
ellas necesitan), compila, corre las pruebas y empaqueta.

Todo proyecto Maven tiene la misma forma:
```
mi-proyecto/
├── pom.xml                         ← qué es el proyecto y qué usa
├── mvnw, mvnw.cmd, .mvn/           ← el wrapper: trae Maven solo
└── src/
    ├── main/java/…                 ← el código
    ├── main/resources/             ← configuración (application.properties)
    └── test/java/…                 ← las pruebas
```
| Comando | Hace |
|---|---|
| `./mvnw compile` | compila |
| `./mvnw test` | compila y corre todas las pruebas |
| `./mvnw spring-boot:run` | arranca la aplicación |
| `./mvnw package` | arma un `.jar` ejecutable en `target/` |

En Windows es `mvnw.cmd` en lugar de `./mvnw`.

#### Crear el proyecto
La forma más simple es **start.spring.io** (*Spring Initializr*): elegís Maven, Java
17, el nombre del paquete y las dependencias, y bajás un zip listo. Todos los proyectos
de esta rama usan **Spring Boot 3.3** y un paquete que empieza con `imperio.`.

#### Inversión de control e inyección de dependencias
Sin Spring, cada clase crea lo que necesita:
```java
public class ServicioHeroes {
    private final RepositorioHeroes repositorio = new RepositorioHeroes();   // atado a esta clase concreta
}
```
Con Spring, la clase **pide** lo que necesita en el constructor, y el **contenedor**
(el `ApplicationContext`) crea los objetos y se los pasa:
```java
@Service
public class ServicioHeroes {
    private final RepositorioHeroes repositorio;
    private final Notificador notificador;

    public ServicioHeroes(RepositorioHeroes repositorio, Notificador notificador) {
        this.repositorio = repositorio;
        this.notificador = notificador;
    }
}
```
Eso es la **inversión de control**: ya no controlás vos cuándo se crean los objetos. Y
la **inyección de dependencias**: se las pasan desde afuera. Los objetos que maneja
Spring se llaman **beans**; por defecto hay **uno solo** de cada uno en toda la
aplicación.

| Anotación | Marca |
|---|---|
| `@SpringBootApplication` | la clase principal: arranca todo y busca beans en su paquete y los de abajo |
| `@Component` | un bean cualquiera |
| `@Service` | un bean de lógica de negocio |
| `@Repository` | un bean de acceso a datos |
| `@Value("${clave}")` | inyecta un valor de `application.properties` |
| `@Primary` | si hay dos beans del mismo tipo, cuál se elige |

La ventaja se ve en las pruebas: como el servicio recibe un `Notificador` (una
interfaz), en una prueba le pasás uno falso con `new` y probás el servicio **sin
Spring**, en milisegundos.

#### `application.properties`
La configuración va en `src/main/resources/application.properties`, no en el código:
```properties
spring.main.banner-mode=off
puerto.bienvenida=Bienvenida al Puerto de Spring
```

#### Pruebas con Spring
`@SpringBootTest` arranca el contenedor completo en la prueba y deja inyectar beans con
`@Autowired`. Es más lento que una prueba común, así que se usa para comprobar que todo
se conecta bien; la lógica se prueba con pruebas comunes.

> **Si venís de Python.** Maven hace lo que `pip` + `requirements.txt` + `pytest`, todo
> junto. Spring Boot se parece a Django o FastAPI: un marco que te da la estructura.

### Código de ejemplo

Un proyecto completo: un repositorio en memoria, un notificador (interfaz) y un
servicio que los recibe por constructor. Al arrancar, un `CommandLineRunner` registra
dos héroes. Descargá el esqueleto de start.spring.io (sin dependencias extra) y
reemplazá los archivos.

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>puerto</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
puerto.bienvenida=Bienvenida al Puerto de Spring
```

`src/main/java/imperio/puerto/PuertoApplication.java`

```java
package imperio.puerto;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class PuertoApplication {
    public static void main(String[] args) {
        SpringApplication.run(PuertoApplication.class, args);
    }

    // Se ejecuta una vez, cuando el contenedor terminó de armar todo.
    @Bean
    CommandLineRunner alArrancar(ServicioHeroes servicio) {
        return args -> {
            servicio.registrar("Nadia", 7);
            servicio.registrar("Baldo", 9);
            System.out.println("Héroes: " + servicio.todos());
        };
    }
}
```

`src/main/java/imperio/puerto/Heroe.java`

```java
package imperio.puerto;

public record Heroe(String nombre, int nivel) {
}
```

`src/main/java/imperio/puerto/RepositorioHeroes.java`

```java
package imperio.puerto;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Repository;

@Repository
public class RepositorioHeroes {
    private final List<Heroe> heroes = new ArrayList<>();

    public void guardar(Heroe heroe) {
        heroes.add(heroe);
    }

    public List<Heroe> todos() {
        return List.copyOf(heroes);
    }
}
```

`src/main/java/imperio/puerto/Notificador.java`

```java
package imperio.puerto;

public interface Notificador {
    void avisar(String mensaje);
}
```

`src/main/java/imperio/puerto/NotificadorConsola.java`

```java
package imperio.puerto;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class NotificadorConsola implements Notificador {
    private final String prefijo;

    public NotificadorConsola(@Value("${puerto.bienvenida}") String prefijo) {
        this.prefijo = prefijo;
    }

    @Override
    public void avisar(String mensaje) {
        System.out.println("[" + prefijo + "] " + mensaje);
    }
}
```

`src/main/java/imperio/puerto/ServicioHeroes.java`

```java
package imperio.puerto;

import java.util.List;

import org.springframework.stereotype.Service;

@Service
public class ServicioHeroes {
    private final RepositorioHeroes repositorio;
    private final Notificador notificador;

    // Un solo constructor: Spring lo usa para inyectar (no hace falta @Autowired).
    public ServicioHeroes(RepositorioHeroes repositorio, Notificador notificador) {
        this.repositorio = repositorio;
        this.notificador = notificador;
    }

    public Heroe registrar(String nombre, int nivel) {
        if (nombre == null || nombre.isBlank()) {
            throw new IllegalArgumentException("el héroe necesita un nombre");
        }
        Heroe heroe = new Heroe(nombre, nivel);
        repositorio.guardar(heroe);
        notificador.avisar("llegó " + nombre + " (nivel " + nivel + ")");
        return heroe;
    }

    public List<Heroe> todos() {
        return repositorio.todos();
    }
}
```

`src/test/java/imperio/puerto/ServicioHeroesTest.java`

```java
package imperio.puerto;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.Test;

// Prueba común, sin Spring: el servicio recibe un notificador falso por constructor.
class ServicioHeroesTest {
    private final List<String> avisos = new ArrayList<>();
    private final ServicioHeroes servicio = new ServicioHeroes(new RepositorioHeroes(), avisos::add);

    @Test
    void registrarGuardaYAvisa() {
        servicio.registrar("Lía", 5);
        assertEquals(List.of(new Heroe("Lía", 5)), servicio.todos());
        assertEquals(List.of("llegó Lía (nivel 5)"), avisos);
    }

    @Test
    void sinNombreNoSeRegistra() {
        assertThrows(IllegalArgumentException.class, () -> servicio.registrar(" ", 3));
        assertEquals(List.of(), avisos);
    }
}
```

`src/test/java/imperio/puerto/PuertoApplicationTest.java`

```java
package imperio.puerto;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

// Prueba con Spring: comprueba que el contenedor arma y conecta los beans.
@SpringBootTest
class PuertoApplicationTest {
    @Autowired
    private ServicioHeroes servicio;

    @Autowired
    private Notificador notificador;

    @Test
    void elContenedorInyectaLosBeans() {
        assertInstanceOf(NotificadorConsola.class, notificador);
        assertEquals(2, servicio.todos().size());      // los dos del CommandLineRunner
    }
}
```

Al correr `./mvnw spring-boot:run` se ve:

```
[Bienvenida al Puerto de Spring] llegó Nadia (nivel 7)
[Bienvenida al Puerto de Spring] llegó Baldo (nivel 9)
Héroes: [Heroe[nombre=Nadia, nivel=7], Heroe[nombre=Baldo, nivel=9]]
```

Y `./mvnw test` corre las tres pruebas.

### ¿Para qué sirve?

Casi todas las empresas que usan Java arman sus sistemas con Spring Boot y Maven (o Gradle). Saber leer un `pom.xml`, entender por qué las clases reciben todo por constructor y probarlas sin levantar el sistema entero es lo primero que se pide en un puesto de desarrollador Java.

### Errores habituales

**Ogro: el bean que no aparece.** `No qualifying bean of type…`: la clase no tiene
`@Component`/`@Service`/`@Repository`, o está en un paquete que no está **debajo** del
de la clase `@SpringBootApplication`.

**Troll: el `new` de un bean.** Hacer `new ServicioHeroes(...)` dentro de otro bean crea
un objeto que Spring no conoce (con otro repositorio). Pedilo por constructor.

**Goblin: dos candidatos.** Si hay dos clases que implementan `Notificador`, Spring no
sabe cuál inyectar (`expected single matching bean but found 2`). Marcá una con
`@Primary` o elegí con `@Qualifier`.

**Ogro: la clave mal escrita.** `@Value("${puerto.bienvenidas}")` con una clave que no
existe hace fallar el arranque: `Could not resolve placeholder`.

**Slime: inyección en el atributo.** `@Autowired private Repositorio r;` funciona, pero
el atributo no puede ser `final` y la clase no se puede probar sin Spring. Preferí el
constructor.

### Micro-misión R05-N03-P1 · El taller que arma solo

```meta
lugar: El taller del Contenedor
personajes: Zed, Gheco, Nadia, Kaffa
carta: El contenedor | alguien crea los objetos y se los entrega a quien los pide · en Spring, el ApplicationContext con sus @Component
recompensa: xp 10, oro 10
```

#### Escena
En el tercer piso, una grúa gigante, el **Contenedor**, sabe qué pieza va en cada lugar. Los maestros no fabrican nada: piden «un reloj» y la grúa se lo entrega armado. —Spring es esa grúa —dice Gheco—. Armemos una de juguete para entenderla.

#### Gheco sugiere
Un contenedor guarda las piezas por nombre en un mapa y las entrega cuando alguien las pide. En Spring, cada clase con `@Component` es una pieza, y el contenedor la crea **una sola vez**.

#### Desafío
Completá el método que entrega una pieza por su nombre.

#### Código inicial
```java
import java.util.HashMap;
import java.util.Map;

public class Grua {
    public static void main(String[] args) {
        Contenedor contenedor = new Contenedor();
        contenedor.registrar("reloj", new Reloj());
        Reloj a = (Reloj) contenedor.pedir("reloj");
        Reloj b = (Reloj) contenedor.pedir("reloj");
        System.out.println(a.hora());
        System.out.println("Es la misma pieza: " + (a == b));
    }
}

class Contenedor {
    private final Map<String, Object> piezas = new HashMap<>();

    void registrar(String nombre, Object pieza) {
        piezas.put(nombre, pieza);
    }

    Object pedir(String nombre) {
        return ___;
    }
}

class Reloj {
    String hora() {
        return "Son las 9 en la Torre";
    }
}
```

#### Salida esperada
```
Son las 9 en la Torre
Es la misma pieza: true
```

#### Solución
```java
import java.util.HashMap;
import java.util.Map;

public class Grua {
    public static void main(String[] args) {
        Contenedor contenedor = new Contenedor();
        contenedor.registrar("reloj", new Reloj());
        Reloj a = (Reloj) contenedor.pedir("reloj");
        Reloj b = (Reloj) contenedor.pedir("reloj");
        System.out.println(a.hora());
        System.out.println("Es la misma pieza: " + (a == b));
    }
}

class Contenedor {
    private final Map<String, Object> piezas = new HashMap<>();

    void registrar(String nombre, Object pieza) {
        piezas.put(nombre, pieza);
    }

    Object pedir(String nombre) {
        return piezas.get(nombre);
    }
}

class Reloj {
    String hora() {
        return "Son las 9 en la Torre";
    }
}
```

#### Al superarla
Dos pedidos, la misma pieza: el contenedor la creó una sola vez. —Como el Singleton del astillero —dice Zed—, pero sin `private` ni `get()`. —Exacto —dice Kaffa—: lo hace la grúa.

#### Imagen
- Una grúa de bronce enorme en el tercer piso de la Torre, entregando un reloj a un maestro.
- Zed mirando hacia arriba, entendiendo.

### Micro-misión R05-N03-P2 · La pieza que viene con piezas

```meta
lugar: El taller del Contenedor
personajes: Zed, Gheco, Nadia, Kaffa
carta: Inyección por constructor | la grúa crea primero lo que la pieza necesita y se lo pasa al construirla · en Spring: @RequiredArgsConstructor y final
recompensa: xp 15, oro 15
```

#### Escena
El `ServicioCampanas` necesita un `Reloj` para saber cuándo tocar. No lo fabrica: lo **pide en el constructor**, y la grúa se lo pasa al armarlo. Es la **D** de SOLID, hecha máquina.

#### Gheco sugiere
Cuando el contenedor arma una pieza que necesita otra, primero busca la que hace falta y la pasa al constructor: `new ServicioCampanas(reloj)`. En Spring se escribe el constructor (o se lo deja a Lombok con `@RequiredArgsConstructor`) y el contenedor hace el resto.

#### Desafío
Completá el armado del servicio con el reloj que ya está en el contenedor.

#### Código inicial
```java
import java.util.HashMap;
import java.util.Map;

public class Inyeccion {
    public static void main(String[] args) {
        Map<String, Object> contenedor = new HashMap<>();
        contenedor.put("reloj", new Reloj());
        Reloj reloj = (Reloj) contenedor.get("reloj");
        contenedor.put("campanas", ___);
        ServicioCampanas campanas = (ServicioCampanas) contenedor.get("campanas");
        System.out.println(campanas.tocar());
    }
}

class Reloj {
    int hora() { return 9; }
}

class ServicioCampanas {
    private final Reloj reloj;

    ServicioCampanas(Reloj reloj) {
        this.reloj = reloj;
    }

    String tocar() {
        return "Din don: son las " + reloj.hora();
    }
}
```

#### Salida esperada
```
Din don: son las 9
```

#### Solución
```java
import java.util.HashMap;
import java.util.Map;

public class Inyeccion {
    public static void main(String[] args) {
        Map<String, Object> contenedor = new HashMap<>();
        contenedor.put("reloj", new Reloj());
        Reloj reloj = (Reloj) contenedor.get("reloj");
        contenedor.put("campanas", new ServicioCampanas(reloj));
        ServicioCampanas campanas = (ServicioCampanas) contenedor.get("campanas");
        System.out.println(campanas.tocar());
    }
}

class Reloj {
    int hora() { return 9; }
}

class ServicioCampanas {
    private final Reloj reloj;

    ServicioCampanas(Reloj reloj) {
        this.reloj = reloj;
    }

    String tocar() {
        return "Din don: son las " + reloj.hora();
    }
}
```

#### Al superarla
Las campanas suenan a las 9. El servicio nunca hizo `new Reloj()`: se lo dieron armado. —Eso es **inyectar** —dice Kaffa—. Spring lo hace con cien piezas sin que escribas una línea de esto.

#### Imagen
- La grúa colocando un reloj adentro de un mecanismo de campanas.
- Las campanas de la Torre sonando.

### Micro-misión R05-N03-P3 · Dos piezas, una interfaz

```meta
lugar: El taller del Contenedor
personajes: Zed, Gheco, Nadia, Kaffa
carta: Elegir la implementación | el servicio pide una INTERFAZ · el contenedor decide cuál le da (en Spring, @Primary, @Qualifier o un perfil)
recompensa: xp 15, oro 15
```

#### Escena
En la Torre hay dos formas de avisar: por **campana** y por **mensajero**. El servicio de avisos no sabe cuál usa: pide «un notificador», y la configuración de la Torre decide.

#### Gheco sugiere
El servicio recibe un `Notificador` (la interfaz). Según la configuración (`modo`), el contenedor le pasa una implementación u otra. En Spring eso se elige con `@Primary`, `@Qualifier` o `application.properties`.

#### Desafío
Completá la elección: con el modo "mensajero", el contenedor da un `PorMensajero`.

#### Código inicial
```java
public class DosPiezas {
    static Notificador elegir(String modo) {
        return modo.equals("mensajero") ? ___ : new PorCampana();
    }

    public static void main(String[] args) {
        for (String modo : new String[] {"campana", "mensajero"}) {
            ServicioAvisos servicio = new ServicioAvisos(elegir(modo));
            System.out.println(servicio.avisar("el Dragón despertó"));
        }
    }
}

interface Notificador {
    String enviar(String texto);
}

class PorCampana implements Notificador {
    public String enviar(String texto) { return "Campana: " + texto; }
}

class PorMensajero implements Notificador {
    public String enviar(String texto) { return "Mensajero: " + texto; }
}

class ServicioAvisos {
    private final Notificador notificador;

    ServicioAvisos(Notificador notificador) { this.notificador = notificador; }

    String avisar(String texto) { return notificador.enviar(texto); }
}
```

#### Salida esperada
```
Campana: el Dragón despertó
Mensajero: el Dragón despertó
```

#### Solución
```java
public class DosPiezas {
    static Notificador elegir(String modo) {
        return modo.equals("mensajero") ? new PorMensajero() : new PorCampana();
    }

    public static void main(String[] args) {
        for (String modo : new String[] {"campana", "mensajero"}) {
            ServicioAvisos servicio = new ServicioAvisos(elegir(modo));
            System.out.println(servicio.avisar("el Dragón despertó"));
        }
    }
}

interface Notificador {
    String enviar(String texto);
}

class PorCampana implements Notificador {
    public String enviar(String texto) { return "Campana: " + texto; }
}

class PorMensajero implements Notificador {
    public String enviar(String texto) { return "Mensajero: " + texto; }
}

class ServicioAvisos {
    private final Notificador notificador;

    ServicioAvisos(Notificador notificador) { this.notificador = notificador; }

    String avisar(String texto) { return notificador.enviar(texto); }
}
```

#### Al superarla
«el Dragón despertó», por campana y por mensajero. Nadia y Zed se miran: el aviso de prueba sonó demasiado real.

#### Imagen
- Una campana y un mensajero con alas saliendo de la misma puerta del taller.
- Nadia y Zed mirando hacia arriba, inquietos.

### Micro-misión R05-N03-P4 · La configuración de la Torre

```meta
lugar: El taller del Contenedor
personajes: Zed, Gheco, Nadia, Kaffa
carta: application.properties | los valores que cambian (tasas, nombres, puertos) van afuera del código · en Spring: @Value("${clave}")
recompensa: xp 15, oro 20
```

#### Escena
La tasa de cambio del Puerto cambia cada mes. Si está escrita en el código, hay que recompilar todo. —Lo que cambia —dice Kaffa— va en la **configuración**, no en el código.

#### Gheco sugiere
Un archivo de propiedades guarda pares `clave=valor`. `Properties.load(...)` los lee y `getProperty("clave")` los devuelve como texto. En Spring es `application.properties` y se lee con `@Value("${clave}")`.

#### Desafío
Completá la lectura de la tasa desde las propiedades.

#### Código inicial
```java
import java.io.StringReader;
import java.util.Properties;

public class Configuracion {
    public static void main(String[] args) throws Exception {
        String archivo = """
                torre.nombre=Torre del Arquitecto
                cambio.tasa=0.85
                """;
        Properties props = new Properties();
        props.load(new StringReader(archivo));
        double tasa = Double.parseDouble(props.___("cambio.tasa"));
        System.out.println(props.getProperty("torre.nombre"));
        System.out.println("100 denarios son " + (100 * tasa) + " monedas del Puerto");
    }
}
```

#### Salida esperada
```
Torre del Arquitecto
100 denarios son 85.0 monedas del Puerto
```

#### Solución
```java
import java.io.StringReader;
import java.util.Properties;

public class Configuracion {
    public static void main(String[] args) throws Exception {
        String archivo = """
                torre.nombre=Torre del Arquitecto
                cambio.tasa=0.85
                """;
        Properties props = new Properties();
        props.load(new StringReader(archivo));
        double tasa = Double.parseDouble(props.getProperty("cambio.tasa"));
        System.out.println(props.getProperty("torre.nombre"));
        System.out.println("100 denarios son " + (100 * tasa) + " monedas del Puerto");
    }
}
```

#### Al superarla
Ochenta y cinco monedas del Puerto. Por la ventana del tercer piso, lejos, se ve el Puerto: la casa de Zed. —Arriba —dice Kaffa— vas a escribir la ventanilla que conecta la Torre con el Puerto.

#### Imagen
- Un pergamino de configuración clavado en la pared del taller, con «cambio.tasa=0.85».
- Zed mirando por la ventana hacia el Puerto lejano, con barcos y techos.

### Misión R05-N03-M1 · El reloj del puerto

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Creá un proyecto de Spring Boot con un servicio `ServicioTurnos` que asigna turnos de
carga a los barcos (`asignar(String barco)` devuelve un `record Turno(int numero, String
barco, String hora)`). La hora sale de un bean `Reloj` (una **interfaz** con un método
`String ahora()`): en la aplicación, un `@Component` `RelojDelSistema` que devuelve la
hora real con formato `HH:mm`. La cantidad máxima de turnos del día sale de
`application.properties` (`puerto.turnos-maximos=3`): pasado el máximo, `asignar` lanza
`IllegalStateException`.

Escribí pruebas **sin Spring** con un reloj falso que siempre devuelve `"08:30"`, y una
prueba con `@SpringBootTest` que compruebe que el máximo se leyó de la configuración.
Entregá el proyecto en un zip (sin la carpeta `target`).

#### Criterio de aprobación

- El servicio recibe el reloj y el máximo por constructor; nada hace `new` de un bean.
- Las pruebas con el reloj falso cubren la numeración y el máximo, y pasan con `./mvnw test`.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>turnos</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
puerto.turnos-maximos=3
```

`src/main/java/imperio/turnos/TurnosApplication.java`

```java
package imperio.turnos;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TurnosApplication {
    public static void main(String[] args) {
        SpringApplication.run(TurnosApplication.class, args);
    }
}
```

`src/main/java/imperio/turnos/Reloj.java`

```java
package imperio.turnos;

public interface Reloj {
    String ahora();
}
```

`src/main/java/imperio/turnos/RelojDelSistema.java`

```java
package imperio.turnos;

import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

import org.springframework.stereotype.Component;

@Component
public class RelojDelSistema implements Reloj {
    @Override
    public String ahora() {
        return LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm"));
    }
}
```

`src/main/java/imperio/turnos/Turno.java`

```java
package imperio.turnos;

public record Turno(int numero, String barco, String hora) {
}
```

`src/main/java/imperio/turnos/ServicioTurnos.java`

```java
package imperio.turnos;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class ServicioTurnos {
    private final Reloj reloj;
    private final int maximo;
    private int asignados;

    public ServicioTurnos(Reloj reloj, @Value("${puerto.turnos-maximos}") int maximo) {
        this.reloj = reloj;
        this.maximo = maximo;
    }

    public synchronized Turno asignar(String barco) {
        if (asignados >= maximo) {
            throw new IllegalStateException("no quedan turnos hoy (máximo " + maximo + ")");
        }
        asignados++;
        return new Turno(asignados, barco, reloj.ahora());
    }

    public int maximo() {
        return maximo;
    }
}
```

`src/test/java/imperio/turnos/ServicioTurnosTest.java`

```java
package imperio.turnos;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class ServicioTurnosTest {
    private final ServicioTurnos servicio = new ServicioTurnos(() -> "08:30", 2);

    @Test
    void losTurnosSeNumeranConLaHoraDelReloj() {
        assertEquals(new Turno(1, "Gaviota", "08:30"), servicio.asignar("Gaviota"));
        assertEquals(new Turno(2, "Albatros", "08:30"), servicio.asignar("Albatros"));
    }

    @Test
    void pasadoElMaximoNoHayMasTurnos() {
        servicio.asignar("Gaviota");
        servicio.asignar("Albatros");
        IllegalStateException e = assertThrows(IllegalStateException.class, () -> servicio.asignar("Petrel"));
        assertEquals("no quedan turnos hoy (máximo 2)", e.getMessage());
    }
}
```

`src/test/java/imperio/turnos/TurnosApplicationTest.java`

```java
package imperio.turnos;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class TurnosApplicationTest {
    @Autowired
    private ServicioTurnos servicio;

    @Test
    void elMaximoSaleDeLaConfiguracion() {
        assertEquals(3, servicio.maximo());
        assertTrue(servicio.asignar("Gaviota").hora().matches("\\d{2}:\\d{2}"));
    }
}
```

### Misión R05-N03-M2 · Dos notificadores

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Partiendo del ejemplo, agregá una segunda implementación de `Notificador`,
`NotificadorArchivo`, que **guarda** los avisos en una lista en memoria (simula un
archivo de registro) y los devuelve con `registrados()`. Hacé que Spring use
`NotificadorArchivo` por defecto con `@Primary`, y que un bean `ServicioAlertas` reciba
**específicamente** el de consola con `@Qualifier("notificadorConsola")`. Probá con
`@SpringBootTest` que el servicio de héroes avisa al de archivo y que las alertas van al
de consola.

#### Criterio de aprobación

- Usa `@Primary` y `@Qualifier` y la aplicación arranca sin el error de "dos candidatos".
- La prueba demuestra a qué notificador llega cada aviso.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>puerto</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
puerto.bienvenida=Puerto
```

`src/main/java/imperio/puerto/PuertoApplication.java`

```java
package imperio.puerto;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class PuertoApplication {
    public static void main(String[] args) {
        SpringApplication.run(PuertoApplication.class, args);
    }
}
```

`src/main/java/imperio/puerto/Heroe.java`

```java
package imperio.puerto;

public record Heroe(String nombre, int nivel) {
}
```

`src/main/java/imperio/puerto/RepositorioHeroes.java`

```java
package imperio.puerto;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Repository;

@Repository
public class RepositorioHeroes {
    private final List<Heroe> heroes = new ArrayList<>();

    public void guardar(Heroe heroe) {
        heroes.add(heroe);
    }

    public List<Heroe> todos() {
        return List.copyOf(heroes);
    }
}
```

`src/main/java/imperio/puerto/Notificador.java`

```java
package imperio.puerto;

public interface Notificador {
    void avisar(String mensaje);
}
```

`src/main/java/imperio/puerto/NotificadorConsola.java`

```java
package imperio.puerto;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class NotificadorConsola implements Notificador {
    private final String prefijo;
    private final List<String> mostrados = new ArrayList<>();

    public NotificadorConsola(@Value("${puerto.bienvenida}") String prefijo) {
        this.prefijo = prefijo;
    }

    @Override
    public void avisar(String mensaje) {
        String linea = "[" + prefijo + "] " + mensaje;
        mostrados.add(linea);
        System.out.println(linea);
    }

    public List<String> mostrados() {
        return List.copyOf(mostrados);
    }
}
```

`src/main/java/imperio/puerto/NotificadorArchivo.java`

```java
package imperio.puerto;

import java.util.ArrayList;
import java.util.List;

import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Component;

@Component
@Primary
public class NotificadorArchivo implements Notificador {
    private final List<String> registrados = new ArrayList<>();

    @Override
    public void avisar(String mensaje) {
        registrados.add(mensaje);
    }

    public List<String> registrados() {
        return List.copyOf(registrados);
    }
}
```

`src/main/java/imperio/puerto/ServicioHeroes.java`

```java
package imperio.puerto;

import java.util.List;

import org.springframework.stereotype.Service;

@Service
public class ServicioHeroes {
    private final RepositorioHeroes repositorio;
    private final Notificador notificador;

    public ServicioHeroes(RepositorioHeroes repositorio, Notificador notificador) {
        this.repositorio = repositorio;
        this.notificador = notificador;
    }

    public Heroe registrar(String nombre, int nivel) {
        Heroe heroe = new Heroe(nombre, nivel);
        repositorio.guardar(heroe);
        notificador.avisar("llegó " + nombre);
        return heroe;
    }

    public List<Heroe> todos() {
        return repositorio.todos();
    }
}
```

`src/main/java/imperio/puerto/ServicioAlertas.java`

```java
package imperio.puerto;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

@Service
public class ServicioAlertas {
    private final Notificador consola;

    public ServicioAlertas(@Qualifier("notificadorConsola") Notificador consola) {
        this.consola = consola;
    }

    public void alertar(String problema) {
        consola.avisar("ALERTA: " + problema);
    }
}
```

`src/test/java/imperio/puerto/NotificadoresTest.java`

```java
package imperio.puerto;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class NotificadoresTest {
    @Autowired
    private ServicioHeroes heroes;

    @Autowired
    private ServicioAlertas alertas;

    @Autowired
    private NotificadorArchivo archivo;

    @Autowired
    private NotificadorConsola consola;

    @Test
    void cadaAvisoVaAlNotificadorQueCorresponde() {
        heroes.registrar("Nadia", 7);
        alertas.alertar("marea alta");
        assertEquals(List.of("llegó Nadia"), archivo.registrados());
        assertEquals(List.of("[Puerto] ALERTA: marea alta"), consola.mostrados());
    }
}
```

### Misión R05-N03-M3 · El conversor configurable

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá un proyecto con un servicio `Conversor` que convierte montos entre pesos y otras
monedas. Las cotizaciones vienen de una interfaz `FuenteCotizaciones` (`double
cotizacion(String moneda)`); en la aplicación, un `@Component` las lee de
`application.properties` con `@Value` (`conversor.dolar=1250`, `conversor.euro=1370`,
`conversor.real=230`) y lanza `IllegalArgumentException` si la moneda no existe. El
conversor redondea a 2 decimales. Probalo con una fuente falsa (sin Spring) y con
`@SpringBootTest`.

#### Criterio de aprobación

- Las cotizaciones salen de la configuración, no del código.
- Hay pruebas sin Spring (con una fuente falsa) y con Spring, y pasan.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>conversor</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
conversor.dolar=1250
conversor.euro=1370
conversor.real=230
```

`src/main/java/imperio/conversor/ConversorApplication.java`

```java
package imperio.conversor;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ConversorApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConversorApplication.class, args);
    }
}
```

`src/main/java/imperio/conversor/FuenteCotizaciones.java`

```java
package imperio.conversor;

public interface FuenteCotizaciones {
    double cotizacion(String moneda);
}
```

`src/main/java/imperio/conversor/CotizacionesConfiguradas.java`

```java
package imperio.conversor;

import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class CotizacionesConfiguradas implements FuenteCotizaciones {
    private final Map<String, Double> cotizaciones;

    public CotizacionesConfiguradas(@Value("${conversor.dolar}") double dolar,
                                    @Value("${conversor.euro}") double euro,
                                    @Value("${conversor.real}") double real) {
        this.cotizaciones = Map.of("dolar", dolar, "euro", euro, "real", real);
    }

    @Override
    public double cotizacion(String moneda) {
        Double valor = cotizaciones.get(moneda);
        if (valor == null) {
            throw new IllegalArgumentException("moneda desconocida: " + moneda);
        }
        return valor;
    }
}
```

`src/main/java/imperio/conversor/Conversor.java`

```java
package imperio.conversor;

import org.springframework.stereotype.Service;

@Service
public class Conversor {
    private final FuenteCotizaciones fuente;

    public Conversor(FuenteCotizaciones fuente) {
        this.fuente = fuente;
    }

    public double aPesos(double monto, String moneda) {
        return redondear(monto * fuente.cotizacion(moneda));
    }

    public double desdePesos(double pesos, String moneda) {
        return redondear(pesos / fuente.cotizacion(moneda));
    }

    private static double redondear(double valor) {
        return Math.round(valor * 100) / 100.0;
    }
}
```

`src/test/java/imperio/conversor/ConversorTest.java`

```java
package imperio.conversor;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class ConversorTest {
    private final Conversor conversor = new Conversor(moneda -> {
        if (!moneda.equals("dolar")) {
            throw new IllegalArgumentException("moneda desconocida: " + moneda);
        }
        return 1000;
    });

    @Test
    void convierteYRedondea() {
        assertEquals(15000.0, conversor.aPesos(15, "dolar"));
        assertEquals(3.33, conversor.desdePesos(3333, "dolar"));
    }

    @Test
    void unaMonedaDesconocidaFalla() {
        assertThrows(IllegalArgumentException.class, () -> conversor.aPesos(1, "yen"));
    }
}
```

`src/test/java/imperio/conversor/ConversorApplicationTest.java`

```java
package imperio.conversor;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class ConversorApplicationTest {
    @Autowired
    private Conversor conversor;

    @Test
    void usaLasCotizacionesDeLaConfiguracion() {
        assertEquals(12500.0, conversor.aPesos(10, "dolar"));
        assertEquals(100.0, conversor.desdePesos(137000, "euro"));
        assertEquals(10.87, conversor.desdePesos(2500, "real"));
    }
}
```

### Encargo R05-N03-E1 · El despachante de pedidos

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Una distribuidora quiere un servicio `Despachante` que reciba un pedido (`record
Pedido(String cliente, double kilos, String zona)`) y le asigne un transporte: tiene una
**lista de beans** que implementan `Transporte` (`boolean puedeLlevar(Pedido)`,
`double costo(Pedido)`, `String nombre()`), por ejemplo `Moto` (hasta 10 kg, solo zona
"centro"), `Camioneta` (hasta 500 kg, solo en la ciudad: zonas "centro", "norte" y "sur") y `Camion` (cualquier peso, mínimo 100 kg). El
despachante elige el **más barato** que puede llevarlo (Spring le inyecta todos los
`Transporte` en un `List<Transporte>`) y devuelve un `Optional` vacío si ninguno puede.
Probalo con `@SpringBootTest`.

#### Criterio de aprobación

- El despachante recibe un `List<Transporte>` por constructor y no conoce las clases concretas.
- Agregar un transporte nuevo es agregar una clase, sin tocar el despachante.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>despacho</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/despacho/DespachoApplication.java`

```java
package imperio.despacho;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DespachoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DespachoApplication.class, args);
    }
}
```

`src/main/java/imperio/despacho/Pedido.java`

```java
package imperio.despacho;

public record Pedido(String cliente, double kilos, String zona) {
}
```

`src/main/java/imperio/despacho/Transporte.java`

```java
package imperio.despacho;

public interface Transporte {
    String nombre();

    boolean puedeLlevar(Pedido pedido);

    double costo(Pedido pedido);
}
```

`src/main/java/imperio/despacho/Moto.java`

```java
package imperio.despacho;

import org.springframework.stereotype.Component;

@Component
public class Moto implements Transporte {
    public String nombre() {
        return "moto";
    }

    public boolean puedeLlevar(Pedido p) {
        return p.kilos() <= 10 && p.zona().equals("centro");
    }

    public double costo(Pedido p) {
        return 1500;
    }
}
```

`src/main/java/imperio/despacho/Camioneta.java`

```java
package imperio.despacho;

import java.util.List;

import org.springframework.stereotype.Component;

@Component
public class Camioneta implements Transporte {
    public String nombre() {
        return "camioneta";
    }

    public boolean puedeLlevar(Pedido p) {
        return p.kilos() <= 500 && List.of("centro", "norte", "sur").contains(p.zona());
    }

    public double costo(Pedido p) {
        return 4000 + p.kilos() * 20;
    }
}
```

`src/main/java/imperio/despacho/Camion.java`

```java
package imperio.despacho;

import org.springframework.stereotype.Component;

@Component
public class Camion implements Transporte {
    public String nombre() {
        return "camión";
    }

    public boolean puedeLlevar(Pedido p) {
        return p.kilos() >= 100;
    }

    public double costo(Pedido p) {
        return 9000 + p.kilos() * 8;
    }
}
```

`src/main/java/imperio/despacho/Despachante.java`

```java
package imperio.despacho;

import java.util.Comparator;
import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;

@Service
public class Despachante {
    private final List<Transporte> transportes;

    public Despachante(List<Transporte> transportes) {
        this.transportes = transportes;
    }

    public Optional<Transporte> elegir(Pedido pedido) {
        return transportes.stream()
                .filter(t -> t.puedeLlevar(pedido))
                .min(Comparator.comparingDouble(t -> t.costo(pedido)));
    }
}
```

`src/test/java/imperio/despacho/DespachanteTest.java`

```java
package imperio.despacho;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class DespachanteTest {
    @Autowired
    private Despachante despachante;

    private String elegido(double kilos, String zona) {
        return despachante.elegir(new Pedido("Ana", kilos, zona)).map(Transporte::nombre).orElse("ninguno");
    }

    @Test
    void eligeElMasBaratoQuePuede() {
        assertEquals("moto", elegido(5, "centro"));
        assertEquals("camioneta", elegido(5, "norte"));
        assertEquals("camioneta", elegido(300, "norte"));
        assertEquals("camión", elegido(450, "sur"));
        assertEquals("camión", elegido(2000, "sur"));
    }

    @Test
    void sinTransportePosibleDevuelveVacio() {
        assertTrue(despachante.elegir(new Pedido("Ana", 50, "rural")).isEmpty());
        assertEquals("camión", elegido(150, "rural"));
    }
}
```

### Prueba del sello

#### ¿Para qué sirve el `pom.xml`?

Describe el proyecto y sus dependencias; Maven las baja y sabe cómo compilar, probar y empaquetar.

#### ¿Qué es la inversión de control?

Que no es tu código el que crea y conecta los objetos, sino el contenedor de Spring.

#### ¿Por qué conviene la inyección por constructor?

Porque las dependencias quedan explícitas, los atributos pueden ser `final` y la clase se puede probar sin Spring pasándole objetos falsos.

#### ¿Qué pasa si hay dos beans del mismo tipo?

Spring no sabe cuál inyectar y falla; se resuelve con `@Primary` o `@Qualifier`.

#### ¿Para qué sirve `application.properties`?

Para la configuración (puertos, claves, valores) fuera del código; se lee con `@Value`.

### Soluciones (docente)

Sale de `19-Java-Avanzado/12-Spring-Boot-IoC-DI`. Las soluciones se verifican con `mvn test` (Spring Boot 3.3.5, Java 17). Se corrige descomprimiendo el zip y corriendo `./mvnw test`.

## R05-N04 · Servicios REST

```meta
tipo: tema
padre: R05-N03
precio: 10
criatura: orc
ejecutable: no
temas: web.http, web.api-rest
usa: fw.spring
```

### Crónica

En el cuarto piso de la Torre está la **ventanilla de los mensajes**, que nunca cierra. Llegan pedidos de todo el Mundo del Código, escritos siempre igual: *«DAME el barco 7»*, *«AGREGÁ este cargamento»*, *«BORRÁ el turno 3»*. La ventanilla contesta con un número y un papel: *200, acá está*; *404, ese barco no existe*. Kaffa le encarga a Zed la que va a conectar la Torre con el Puerto, su casa.

—Así se hablan hoy los sistemas —dice {mentor}—: por **HTTP**, con verbos y códigos que todos entienden. Una app de celular, una página web, otro sistema: todos le piden datos a un **servicio REST**. Tu ventanilla va a ser un `@RestController`, Zed. Por primera vez vas a llegar al Puerto construyendo.

### Objetivos

- Entender HTTP: verbos, rutas, códigos de estado y JSON.
- Crear un `@RestController` con `@GetMapping`, `@PostMapping`, `@PutMapping` y `@DeleteMapping`.
- Recibir datos con `@PathVariable`, `@RequestParam` y `@RequestBody`.
- Responder con el código correcto usando `ResponseEntity`.
- Probar la API con `MockMvc`, sin levantar el servidor.

### Antes de empezar

- Maven y el contenedor de Spring.

### Explicación

#### HTTP en dos minutos
Un **pedido** HTTP tiene un **verbo**, una **ruta** y, a veces, un **cuerpo** (en JSON).
La **respuesta** trae un **código de estado** y, a veces, un cuerpo.
| Verbo | Para | Ejemplo |
|---|---|---|
| `GET` | leer | `GET /heroes`, `GET /heroes/3` |
| `POST` | crear | `POST /heroes` con el héroe en el cuerpo |
| `PUT` | reemplazar | `PUT /heroes/3` con el héroe completo |
| `PATCH` | modificar una parte | `PATCH /heroes/3/nivel` |
| `DELETE` | borrar | `DELETE /heroes/3` |

| Código | Significa |
|---|---|
| `200 OK` | salió bien, acá está |
| `201 Created` | se creó (con la ruta del nuevo en el encabezado `Location`) |
| `204 No Content` | salió bien, no hay nada que devolver |
| `400 Bad Request` | el pedido está mal armado |
| `404 Not Found` | eso no existe |
| `409 Conflict` | choca con algo que ya existe |

**REST** es una forma de ordenar las rutas: los **recursos** son sustantivos en plural
(`/heroes`), y el verbo dice qué se hace con ellos.

#### El controlador
Con `spring-boot-starter-web`, Spring Boot trae un servidor (Tomcat) adentro. Un
`@RestController` atiende pedidos; lo que devuelve cada método se convierte en JSON solo
(los `record` se convierten perfecto):
```java
@RestController
@RequestMapping("/heroes")
public class HeroeController {
    private final ServicioHeroes servicio;

    public HeroeController(ServicioHeroes servicio) {
        this.servicio = servicio;
    }

    @GetMapping
    public List<Heroe> listar(@RequestParam(required = false) String clase) { … }

    @GetMapping("/{id}")
    public ResponseEntity<Heroe> buscar(@PathVariable long id) {
        return servicio.buscar(id)
                .map(ResponseEntity::ok)                       // 200 con el héroe
                .orElse(ResponseEntity.notFound().build());    // 404
    }

    @PostMapping
    public ResponseEntity<Heroe> crear(@RequestBody Heroe nuevo) {
        Heroe creado = servicio.crear(nuevo);
        return ResponseEntity.created(URI.create("/heroes/" + creado.id())).body(creado);   // 201
    }
}
```
| Anotación | Toma el dato de |
|---|---|
| `@PathVariable` | la ruta: `/heroes/{id}` |
| `@RequestParam` | la consulta: `/heroes?clase=maga` (`required = false` si es opcional) |
| `@RequestBody` | el cuerpo JSON del pedido |

El controlador **no tiene lógica**: recibe, llama al servicio y arma la respuesta. Las
reglas están en el servicio (que se prueba sin HTTP).

#### Probar con MockMvc
`MockMvc` simula pedidos HTTP sin abrir un puerto, y deja comprobar el código y el JSON
de la respuesta con `jsonPath`:
```java
mvc.perform(get("/heroes/1"))
   .andExpect(status().isOk())
   .andExpect(jsonPath("$.nombre").value("Nadia"));

mvc.perform(post("/heroes").contentType(MediaType.APPLICATION_JSON)
        .content("""
                {"nombre": "Lía", "clase": "maga", "nivel": 5}
                """))
   .andExpect(status().isCreated())
   .andExpect(header().string("Location", "/heroes/3"));
```
`$.nombre` es un campo del objeto; `$[0].nombre`, del primero de una lista;
`$.length()`, el tamaño.

#### Probar a mano
Con la aplicación corriendo (`./mvnw spring-boot:run`, puerto 8080), un `GET` se prueba
desde el navegador (`http://localhost:8080/heroes`). Para los demás verbos, `curl` o una
herramienta como Bruno o Postman:
```
curl -X POST localhost:8080/heroes -H "Content-Type: application/json" -d '{"nombre":"Lía","clase":"maga","nivel":5}'
```

> **Si venís de Python.** Es lo mismo que una ruta de Flask o FastAPI:
> `@app.get("/heroes/{id}")` en FastAPI es `@GetMapping("/{id}")` acá.

### Código de ejemplo

La ventanilla de los héroes: una API REST completa en memoria, con sus pruebas.

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>ventanilla</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/ventanilla/VentanillaApplication.java`

```java
package imperio.ventanilla;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class VentanillaApplication {
    public static void main(String[] args) {
        SpringApplication.run(VentanillaApplication.class, args);
    }
}
```

`src/main/java/imperio/ventanilla/Heroe.java`

```java
package imperio.ventanilla;

public record Heroe(Long id, String nombre, String clase, int nivel) {
    public Heroe conId(long nuevoId) {
        return new Heroe(nuevoId, nombre, clase, nivel);
    }
}
```

`src/main/java/imperio/ventanilla/ServicioHeroes.java`

```java
package imperio.ventanilla;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.stereotype.Service;

@Service
public class ServicioHeroes {
    private final Map<Long, Heroe> heroes = new ConcurrentHashMap<>();
    private final AtomicLong proximoId = new AtomicLong(1);

    public ServicioHeroes() {
        crear(new Heroe(null, "Nadia", "arquera", 7));
        crear(new Heroe(null, "Baldo", "guerrero", 9));
    }

    public List<Heroe> listar(String clase) {
        return heroes.values().stream()
                .filter(h -> clase == null || h.clase().equals(clase))
                .sorted((a, b) -> Long.compare(a.id(), b.id()))
                .toList();
    }

    public Optional<Heroe> buscar(long id) {
        return Optional.ofNullable(heroes.get(id));
    }

    public Heroe crear(Heroe nuevo) {
        Heroe conId = nuevo.conId(proximoId.getAndIncrement());
        heroes.put(conId.id(), conId);
        return conId;
    }

    public Optional<Heroe> reemplazar(long id, Heroe datos) {
        if (!heroes.containsKey(id)) {
            return Optional.empty();
        }
        Heroe nuevo = datos.conId(id);
        heroes.put(id, nuevo);
        return Optional.of(nuevo);
    }

    public boolean borrar(long id) {
        return heroes.remove(id) != null;
    }
}
```

`src/main/java/imperio/ventanilla/HeroeController.java`

```java
package imperio.ventanilla;

import java.net.URI;
import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/heroes")
public class HeroeController {
    private final ServicioHeroes servicio;

    public HeroeController(ServicioHeroes servicio) {
        this.servicio = servicio;
    }

    @GetMapping
    public List<Heroe> listar(@RequestParam(required = false) String clase) {
        return servicio.listar(clase);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Heroe> buscar(@PathVariable long id) {
        return servicio.buscar(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Heroe> crear(@RequestBody Heroe nuevo) {
        Heroe creado = servicio.crear(nuevo);
        return ResponseEntity.created(URI.create("/heroes/" + creado.id())).body(creado);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Heroe> reemplazar(@PathVariable long id, @RequestBody Heroe datos) {
        return servicio.reemplazar(id, datos).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> borrar(@PathVariable long id) {
        return servicio.borrar(id) ? ResponseEntity.noContent().build() : ResponseEntity.notFound().build();
    }
}
```

`src/test/java/imperio/ventanilla/HeroeControllerTest.java`

```java
package imperio.ventanilla;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)   // cada prueba arranca con los datos iniciales
class HeroeControllerTest {
    @Autowired
    private MockMvc mvc;

    @Test
    void listaTodosYFiltraPorClase() throws Exception {
        mvc.perform(get("/heroes"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(2))
                .andExpect(jsonPath("$[0].nombre").value("Nadia"));
        mvc.perform(get("/heroes").param("clase", "guerrero"))
                .andExpect(jsonPath("$.length()").value(1))
                .andExpect(jsonPath("$[0].nombre").value("Baldo"));
    }

    @Test
    void buscaUnoOContesta404() throws Exception {
        mvc.perform(get("/heroes/2")).andExpect(status().isOk()).andExpect(jsonPath("$.nivel").value(9));
        mvc.perform(get("/heroes/99")).andExpect(status().isNotFound());
    }

    @Test
    void creaConCodigo201YLocation() throws Exception {
        mvc.perform(post("/heroes").contentType(MediaType.APPLICATION_JSON).content("""
                        {"nombre": "Lía", "clase": "maga", "nivel": 5}
                        """))
                .andExpect(status().isCreated())
                .andExpect(header().string("Location", "/heroes/3"))
                .andExpect(jsonPath("$.id").value(3));
        mvc.perform(get("/heroes")).andExpect(jsonPath("$.length()").value(3));
    }

    @Test
    void reemplazaYBorra() throws Exception {
        mvc.perform(put("/heroes/1").contentType(MediaType.APPLICATION_JSON).content("""
                        {"nombre": "Nadia", "clase": "arquera", "nivel": 8}
                        """))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.nivel").value(8));
        mvc.perform(delete("/heroes/1")).andExpect(status().isNoContent());
        mvc.perform(delete("/heroes/1")).andExpect(status().isNotFound());
    }
}
```

Con la aplicación corriendo:

```
$ curl localhost:8080/heroes
[{"id":1,"nombre":"Nadia","clase":"arquera","nivel":7},{"id":2,"nombre":"Baldo","clase":"guerrero","nivel":9}]
$ curl -i localhost:8080/heroes/99
HTTP/1.1 404
```

### ¿Para qué sirve?

Todas las apps que usás le piden datos a un servicio REST: el home banking, la app del colectivo, una tienda online. El *backend* que las atiende muy a menudo está hecho con Spring Boot. Con lo de este nodo ya podés hacer el servidor de una app de celular o de una página hecha en JavaScript.

### Errores habituales

**Ogro: todo devuelve 200.** Devolver `null` (que da un 200 vacío) cuando algo no existe,
o 200 al crear. Usá `ResponseEntity` con el código que corresponde: 404, 201, 204.

**Troll: la lógica en el controlador.** Validar, calcular y guardar dentro del
controlador: queda imposible de probar sin HTTP y se repite. El controlador solo recibe y
responde; la lógica va en el servicio.

**Goblin: el `Content-Type` olvidado.** Un `POST` con JSON sin
`Content-Type: application/json` da `415 Unsupported Media Type`.

**Ogro: el `HashMap` compartido.** El servidor atiende muchos pedidos a la vez, en hilos
distintos: los datos en memoria van en un `ConcurrentHashMap` y los contadores en un
`AtomicLong` (lo viste en las Corrientes).

**Slime: el puerto ocupado.** `Port 8080 was already in use`: quedó otra aplicación
corriendo. Cerrala o cambiá `server.port` en `application.properties`.

### Micro-misión R05-N04-P1 · La ventanilla de los mensajes

```meta
lugar: La ventanilla de la Torre
personajes: Zed, Gheco, Nadia, Kaffa
carta: Ruta y método | GET /api/barcos lee · POST /api/barcos crea · el controlador elige qué hacer según el método y la ruta
recompensa: xp 10, oro 10
```

#### Escena
En el cuarto piso está la **ventanilla de los mensajes**: llegan pedidos de todo el Mundo del Código y cada uno dice **qué quiere** (el método) y **sobre qué** (la ruta). Gheco arma una ventanilla de juguete para ver cómo decide.

#### Gheco sugiere
Un pedido HTTP tiene un **método** (`GET` para leer, `POST` para crear, `PUT` para cambiar, `DELETE` para borrar) y una **ruta**. El controlador los mira y decide. En Spring: `@GetMapping("/api/barcos")`.

#### Desafío
Completá el caso del pedido que crea un barco.

#### Código inicial
```java
public class Ventanilla {
    static String atender(String metodo, String ruta) {
        return switch (metodo + " " + ruta) {
            case "GET /api/barcos" -> "200: [Garza, Bagre]";
            case ___ -> "201: barco creado";
            default -> "404: no existe " + ruta;
        };
    }

    public static void main(String[] args) {
        System.out.println(atender("GET", "/api/barcos"));
        System.out.println(atender("POST", "/api/barcos"));
        System.out.println(atender("GET", "/api/dragones"));
    }
}
```

#### Salida esperada
```
200: [Garza, Bagre]
201: barco creado
404: no existe /api/dragones
```

#### Solución
```java
public class Ventanilla {
    static String atender(String metodo, String ruta) {
        return switch (metodo + " " + ruta) {
            case "GET /api/barcos" -> "200: [Garza, Bagre]";
            case "POST /api/barcos" -> "201: barco creado";
            default -> "404: no existe " + ruta;
        };
    }

    public static void main(String[] args) {
        System.out.println(atender("GET", "/api/barcos"));
        System.out.println(atender("POST", "/api/barcos"));
        System.out.println(atender("GET", "/api/dragones"));
    }
}
```

#### Al superarla
Leer, crear y un 404 para lo que no existe. —En Spring no escribís el `switch` —dice Kaffa—: ponés `@GetMapping` y `@PostMapping` y el framework elige.

#### Imagen
- Una ventanilla de piedra en el cuarto piso de la Torre, con un cartel de rutas: GET, POST, PUT, DELETE.
- Gheco atendiendo la ventanilla con una gorrita de empleado.

### Micro-misión R05-N04-P2 · Responder en JSON

```meta
lugar: La ventanilla de la Torre
personajes: Zed, Gheco, Nadia, Kaffa
carta: JSON | {"nombre": "Garza", "carga": 80} · texto entre comillas, números sin comillas · Spring convierte los objetos solo (Jackson)
recompensa: xp 10, oro 10
```

#### Escena
El Puerto no lee pergaminos del Imperio: lee **JSON**. Zed tiene que responder cada barco en ese idioma.

#### Gheco sugiere
Un objeto JSON va entre llaves, con `"clave": valor` separados por coma. Los textos llevan comillas (`\"Garza\"`) y los números no. En Spring, el controlador devuelve el objeto y Jackson lo convierte solo.

#### Desafío
Completá el JSON con la carga del barco (un número, sin comillas).

#### Código inicial
```java
public class Json {
    record Barco(String nombre, int carga) {
        String json() {
            return "{\"nombre\": \"" + nombre + "\", \"carga\": " + ___ + "}";
        }
    }

    public static void main(String[] args) {
        System.out.println(new Barco("Garza", 80).json());
        System.out.println(new Barco("Bagre", 120).json());
    }
}
```

#### Salida esperada
```
{"nombre": "Garza", "carga": 80}
{"nombre": "Bagre", "carga": 120}
```

#### Solución
```java
public class Json {
    record Barco(String nombre, int carga) {
        String json() {
            return "{\"nombre\": \"" + nombre + "\", \"carga\": " + carga + "}";
        }
    }

    public static void main(String[] args) {
        System.out.println(new Barco("Garza", 80).json());
        System.out.println(new Barco("Bagre", 120).json());
    }
}
```

#### Al superarla
Dos barcos en JSON, que el Puerto entiende. —Armarlo a mano es para entenderlo —dice Gheco—. En Spring, nunca más.

#### Imagen
- Un pergamino con llaves y comillas, el JSON de un barco, viajando por un tubo hacia el Puerto.
- Gheco con un diccionario «Imperio ↔ JSON».

### Micro-misión R05-N04-P3 · El código de la respuesta

```meta
lugar: La ventanilla de la Torre
personajes: Zed, Gheco, Nadia, Kaffa
criatura: orco
carta: Códigos de estado | 200 ok · 201 creado · 400 pedido inválido · 404 no existe · 409 conflicto · 500 error del servidor
recompensa: xp 15, oro 15
```

#### Escena
Cuando alguien pide un barco que no existe, la ventanilla responde 200 con un cuerpo vacío y el cliente no entiende nada. Un **orco** festeja el silencio. Cada respuesta tiene que decir **cómo salió**.

#### Gheco sugiere
Los códigos de estado dicen cómo salió el pedido: **200** encontrado, **404** no existe. En Spring, un `ResponseEntity.notFound()` o una excepción manejada en un `@RestControllerAdvice`.

#### Desafío
Completá el código de estado para un barco que no existe.

#### Código inicial
```java
import java.util.Map;

public class Estados {
    static final Map<String, Integer> BARCOS = Map.of("Garza", 80, "Bagre", 120);

    static String buscar(String nombre) {
        Integer carga = BARCOS.get(nombre);
        if (carga == null) {
            return ___ + " no existe el barco " + nombre;
        }
        return 200 + " {\"nombre\": \"" + nombre + "\", \"carga\": " + carga + "}";
    }

    public static void main(String[] args) {
        System.out.println(buscar("Garza"));
        System.out.println(buscar("Ceibo"));
    }
}
```

#### Salida esperada
```
200 {"nombre": "Garza", "carga": 80}
404 no existe el barco Ceibo
```

#### Solución
```java
import java.util.Map;

public class Estados {
    static final Map<String, Integer> BARCOS = Map.of("Garza", 80, "Bagre", 120);

    static String buscar(String nombre) {
        Integer carga = BARCOS.get(nombre);
        if (carga == null) {
            return 404 + " no existe el barco " + nombre;
        }
        return 200 + " {\"nombre\": \"" + nombre + "\", \"carga\": " + carga + "}";
    }

    public static void main(String[] args) {
        System.out.println(buscar("Garza"));
        System.out.println(buscar("Ceibo"));
    }
}
```

#### Al superarla
«404 no existe el barco Ceibo.» Claro y sin rodeos. El orco se va: ya nadie se confunde. —El Ceibo está encallado en la Represa —murmura Zed—. Pero eso la ventanilla no lo sabe.

#### Imagen
- Un tablero de la ventanilla con números grandes: 200 en verde, 404 en naranja.
- Un orco yéndose por la escalera, aburrido.

### Micro-misión R05-N04-P4 · La primera ventanilla al Puerto

```meta
lugar: La ventanilla de la Torre
personajes: Zed, Gheco, Nadia, Kaffa
carta: Controlador y servicio | el controlador recibe el pedido y responde · el servicio tiene las reglas · el controlador NO calcula
recompensa: xp 15, oro 20
```

#### Escena
Kaffa le encarga a Zed la ventanilla que conecta la Torre con **el Puerto**, su casa. Por primera vez, Zed va a llegar al Puerto **construyendo** algo, no robando.

#### Gheco sugiere
El controlador solo traduce: recibe el pedido, le pide al **servicio** el resultado y arma la respuesta. Las reglas (cuánto cuesta un envío) están en el servicio. En Spring: `@RestController` que recibe un `@Service` por el constructor.

#### Desafío
Completá el controlador: que le pida el costo al servicio.

#### Código inicial
```java
public class AlPuerto {
    public static void main(String[] args) {
        ControladorEnvios controlador = new ControladorEnvios(new ServicioEnvios());
        System.out.println(controlador.cotizar(30));
        System.out.println(controlador.cotizar(120));
    }
}

class ServicioEnvios {
    int costo(int kilos) {
        return kilos <= 50 ? 20 : 20 + (kilos - 50) / 10 * 5;
    }
}

class ControladorEnvios {
    private final ServicioEnvios servicio;

    ControladorEnvios(ServicioEnvios servicio) {
        this.servicio = servicio;
    }

    String cotizar(int kilos) {
        int costo = ___;
        return "200 {\"kilos\": " + kilos + ", \"costo\": " + costo + "}";
    }
}
```

#### Salida esperada
```
200 {"kilos": 30, "costo": 20}
200 {"kilos": 120, "costo": 55}
```

#### Solución
```java
public class AlPuerto {
    public static void main(String[] args) {
        ControladorEnvios controlador = new ControladorEnvios(new ServicioEnvios());
        System.out.println(controlador.cotizar(30));
        System.out.println(controlador.cotizar(120));
    }
}

class ServicioEnvios {
    int costo(int kilos) {
        return kilos <= 50 ? 20 : 20 + (kilos - 50) / 10 * 5;
    }
}

class ControladorEnvios {
    private final ServicioEnvios servicio;

    ControladorEnvios(ServicioEnvios servicio) {
        this.servicio = servicio;
    }

    String cotizar(int kilos) {
        int costo = servicio.costo(kilos);
        return "200 {\"kilos\": " + kilos + ", \"costo\": " + costo + "}";
    }
}
```

#### Al superarla
La primera cotización llega al Puerto y alguien allá la contesta: «¿Zed? ¿El de los techos?». Zed se ríe solo frente a la ventanilla.
Pero los mensajes del Puerto llegan con cualquier cosa adentro: kilos negativos, nombres vacíos, campos que sobran.

#### Imagen
- Un tubo de mensajes que une la Torre con el Puerto a lo lejos, con un pergamino JSON viajando.
- Zed riéndose solo frente a la ventanilla, con una respuesta del Puerto en la mano.

### Misión R05-N04-M1 · La API de la biblioteca

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Hacé una API REST para los libros de una biblioteca (`record Libro(Long id, String
titulo, String autor, int anio, boolean prestado)`), en memoria, con tres libros
cargados al arrancar:

- `GET /libros` — todos, ordenados por id.
- `GET /libros/{id}` — uno, o 404.
- `POST /libros` — crea (siempre sin prestar), 201 con `Location`.
- `POST /libros/{id}/prestamo` — lo marca prestado; 404 si no existe, **409** si ya estaba
  prestado.
- `DELETE /libros/{id}/prestamo` — lo devuelve (204); 409 si no estaba prestado.

Probá cada ruta con `MockMvc`, incluidos los 404 y 409.

#### Criterio de aprobación

- Cada ruta responde el código correcto (200, 201, 204, 404, 409).
- La lógica está en el servicio y las pruebas pasan.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>biblioteca</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/biblioteca/BibliotecaApplication.java`

```java
package imperio.biblioteca;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class BibliotecaApplication {
    public static void main(String[] args) {
        SpringApplication.run(BibliotecaApplication.class, args);
    }
}
```

`src/main/java/imperio/biblioteca/Libro.java`

```java
package imperio.biblioteca;

public record Libro(Long id, String titulo, String autor, int anio, boolean prestado) {
    public Libro conId(long nuevoId) {
        return new Libro(nuevoId, titulo, autor, anio, false);
    }

    public Libro conPrestado(boolean valor) {
        return new Libro(id, titulo, autor, anio, valor);
    }
}
```

`src/main/java/imperio/biblioteca/Resultado.java`

```java
package imperio.biblioteca;

// Lo que puede pasar al prestar o devolver.
public enum Resultado { HECHO, NO_EXISTE, CONFLICTO }
```

`src/main/java/imperio/biblioteca/ServicioLibros.java`

```java
package imperio.biblioteca;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.stereotype.Service;

@Service
public class ServicioLibros {
    private final Map<Long, Libro> libros = new ConcurrentHashMap<>();
    private final AtomicLong proximoId = new AtomicLong(1);

    public ServicioLibros() {
        crear(new Libro(null, "Rayuela", "Julio Cortázar", 1963, false));
        crear(new Libro(null, "Ficciones", "Jorge Luis Borges", 1944, false));
        crear(new Libro(null, "El túnel", "Ernesto Sabato", 1948, false));
    }

    public List<Libro> todos() {
        return libros.values().stream().sorted(Comparator.comparing(Libro::id)).toList();
    }

    public Optional<Libro> buscar(long id) {
        return Optional.ofNullable(libros.get(id));
    }

    public Libro crear(Libro nuevo) {
        Libro libro = nuevo.conId(proximoId.getAndIncrement());
        libros.put(libro.id(), libro);
        return libro;
    }

    public synchronized Resultado cambiarPrestamo(long id, boolean prestar) {
        Libro libro = libros.get(id);
        if (libro == null) {
            return Resultado.NO_EXISTE;
        }
        if (libro.prestado() == prestar) {
            return Resultado.CONFLICTO;
        }
        libros.put(id, libro.conPrestado(prestar));
        return Resultado.HECHO;
    }
}
```

`src/main/java/imperio/biblioteca/LibroController.java`

```java
package imperio.biblioteca;

import java.net.URI;
import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/libros")
public class LibroController {
    private final ServicioLibros servicio;

    public LibroController(ServicioLibros servicio) {
        this.servicio = servicio;
    }

    @GetMapping
    public List<Libro> todos() {
        return servicio.todos();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Libro> buscar(@PathVariable long id) {
        return servicio.buscar(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Libro> crear(@RequestBody Libro nuevo) {
        Libro creado = servicio.crear(nuevo);
        return ResponseEntity.created(URI.create("/libros/" + creado.id())).body(creado);
    }

    @PostMapping("/{id}/prestamo")
    public ResponseEntity<Void> prestar(@PathVariable long id) {
        return responder(servicio.cambiarPrestamo(id, true));
    }

    @DeleteMapping("/{id}/prestamo")
    public ResponseEntity<Void> devolver(@PathVariable long id) {
        return responder(servicio.cambiarPrestamo(id, false));
    }

    private ResponseEntity<Void> responder(Resultado r) {
        return switch (r) {
            case HECHO -> ResponseEntity.noContent().build();
            case NO_EXISTE -> ResponseEntity.notFound().build();
            case CONFLICTO -> ResponseEntity.status(HttpStatus.CONFLICT).build();
        };
    }
}
```

`src/test/java/imperio/biblioteca/LibroControllerTest.java`

```java
package imperio.biblioteca;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class LibroControllerTest {
    @Autowired
    private MockMvc mvc;

    @Test
    void listaYBusca() throws Exception {
        mvc.perform(get("/libros")).andExpect(status().isOk()).andExpect(jsonPath("$.length()").value(3))
                .andExpect(jsonPath("$[1].autor").value("Jorge Luis Borges"));
        mvc.perform(get("/libros/3")).andExpect(jsonPath("$.titulo").value("El túnel"));
        mvc.perform(get("/libros/40")).andExpect(status().isNotFound());
    }

    @Test
    void creaSinPrestar() throws Exception {
        mvc.perform(post("/libros").contentType(MediaType.APPLICATION_JSON).content("""
                        {"titulo": "Zama", "autor": "Antonio Di Benedetto", "anio": 1956, "prestado": true}
                        """))
                .andExpect(status().isCreated())
                .andExpect(header().string("Location", "/libros/4"))
                .andExpect(jsonPath("$.prestado").value(false));
    }

    @Test
    void prestaYDevuelveConSusConflictos() throws Exception {
        mvc.perform(post("/libros/1/prestamo")).andExpect(status().isNoContent());
        mvc.perform(get("/libros/1")).andExpect(jsonPath("$.prestado").value(true));
        mvc.perform(post("/libros/1/prestamo")).andExpect(status().isConflict());
        mvc.perform(delete("/libros/1/prestamo")).andExpect(status().isNoContent());
        mvc.perform(delete("/libros/1/prestamo")).andExpect(status().isConflict());
        mvc.perform(post("/libros/99/prestamo")).andExpect(status().isNotFound());
    }
}
```

### Misión R05-N04-M2 · El catálogo con filtros

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Hacé `GET /productos` para el catálogo de una tienda (al menos 8 productos en memoria:
`record Producto(long id, String nombre, String rubro, double precio, int stock)`),
con parámetros **opcionales** que se combinan:

- `rubro` — solo ese rubro.
- `max` — precio máximo.
- `conStock` — `true` para dejar solo los que tienen stock.
- `orden` — `precio` (de menor a mayor) o `nombre` (por defecto, `id`).

Además, `GET /productos/resumen` devuelve un objeto con la cantidad de productos, el
precio promedio y los rubros distintos (un `record Resumen`). Probá varias combinaciones
de filtros con `MockMvc`.

#### Criterio de aprobación

- Los filtros son opcionales y se combinan (`@RequestParam(required = false)` o con `defaultValue`).
- El filtrado usa streams en el servicio y las pruebas cubren al menos 4 combinaciones.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>catalogo</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/catalogo/CatalogoApplication.java`

```java
package imperio.catalogo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class CatalogoApplication {
    public static void main(String[] args) {
        SpringApplication.run(CatalogoApplication.class, args);
    }
}
```

`src/main/java/imperio/catalogo/Producto.java`

```java
package imperio.catalogo;

public record Producto(long id, String nombre, String rubro, double precio, int stock) {
}
```

`src/main/java/imperio/catalogo/Resumen.java`

```java
package imperio.catalogo;

import java.util.List;

public record Resumen(int cantidad, double precioPromedio, List<String> rubros) {
}
```

`src/main/java/imperio/catalogo/ServicioCatalogo.java`

```java
package imperio.catalogo;

import java.util.Comparator;
import java.util.List;

import org.springframework.stereotype.Service;

@Service
public class ServicioCatalogo {
    private final List<Producto> productos = List.of(
            new Producto(1, "Yerba", "almacén", 4200, 20), new Producto(2, "Lavandina", "limpieza", 900, 3),
            new Producto(3, "Aceite", "almacén", 2890, 0), new Producto(4, "Detergente", "limpieza", 1600, 12),
            new Producto(5, "Queso", "fiambrería", 9800, 4), new Producto(6, "Jamón", "fiambrería", 12500, 0),
            new Producto(7, "Arroz", "almacén", 1450, 30), new Producto(8, "Esponja", "limpieza", 600, 25));

    public List<Producto> buscar(String rubro, Double max, boolean conStock, String orden) {
        Comparator<Producto> comparador = switch (orden) {
            case "precio" -> Comparator.comparingDouble(Producto::precio);
            case "nombre" -> Comparator.comparing(Producto::nombre);
            default -> Comparator.comparingLong(Producto::id);
        };
        return productos.stream()
                .filter(p -> rubro == null || p.rubro().equals(rubro))
                .filter(p -> max == null || p.precio() <= max)
                .filter(p -> !conStock || p.stock() > 0)
                .sorted(comparador)
                .toList();
    }

    public Resumen resumen() {
        double promedio = productos.stream().mapToDouble(Producto::precio).average().orElse(0);
        List<String> rubros = productos.stream().map(Producto::rubro).distinct().sorted().toList();
        return new Resumen(productos.size(), Math.round(promedio * 100) / 100.0, rubros);
    }
}
```

`src/main/java/imperio/catalogo/ProductoController.java`

```java
package imperio.catalogo;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/productos")
public class ProductoController {
    private final ServicioCatalogo servicio;

    public ProductoController(ServicioCatalogo servicio) {
        this.servicio = servicio;
    }

    @GetMapping
    public List<Producto> buscar(@RequestParam(required = false) String rubro,
                                 @RequestParam(required = false) Double max,
                                 @RequestParam(defaultValue = "false") boolean conStock,
                                 @RequestParam(defaultValue = "id") String orden) {
        return servicio.buscar(rubro, max, conStock, orden);
    }

    @GetMapping("/resumen")
    public Resumen resumen() {
        return servicio.resumen();
    }
}
```

`src/test/java/imperio/catalogo/ProductoControllerTest.java`

```java
package imperio.catalogo;

import static org.hamcrest.Matchers.contains;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class ProductoControllerTest {
    @Autowired
    private MockMvc mvc;

    @Test
    void sinFiltrosTraeTodosPorId() throws Exception {
        mvc.perform(get("/productos")).andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(8))
                .andExpect(jsonPath("$[0].nombre").value("Yerba"));
    }

    @Test
    void filtraPorRubroYOrdenaPorPrecio() throws Exception {
        mvc.perform(get("/productos").param("rubro", "limpieza").param("orden", "precio"))
                .andExpect(jsonPath("$[*].nombre", contains("Esponja", "Lavandina", "Detergente")));
    }

    @Test
    void combinaPrecioMaximoYStock() throws Exception {
        mvc.perform(get("/productos").param("max", "3000").param("conStock", "true").param("orden", "nombre"))
                .andExpect(jsonPath("$[*].nombre", contains("Arroz", "Detergente", "Esponja", "Lavandina")));
    }

    @Test
    void fiambreriaBarataNoHay() throws Exception {
        mvc.perform(get("/productos").param("rubro", "fiambrería").param("max", "9000"))
                .andExpect(jsonPath("$.length()").value(0));
    }

    @Test
    void elResumen() throws Exception {
        mvc.perform(get("/productos/resumen"))
                .andExpect(jsonPath("$.cantidad").value(8))
                .andExpect(jsonPath("$.precioPromedio").value(4242.5))
                .andExpect(jsonPath("$.rubros", contains("almacén", "fiambrería", "limpieza")));
    }
}
```

### Misión R05-N04-M3 · Las tareas del taller

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Un taller mecánico quiere una API para sus órdenes de trabajo (`record Orden(Long id,
String patente, String trabajo, String estado)`, con estado `PENDIENTE`, `EN_CURSO` o
`TERMINADA` como `enum`). Rutas:

- `POST /ordenes` — crea una orden `PENDIENTE` (201).
- `GET /ordenes?estado=…` — lista, filtrando por estado si viene.
- `PATCH /ordenes/{id}/avanzar` — pasa al estado siguiente (`PENDIENTE` → `EN_CURSO` →
  `TERMINADA`); 409 si ya estaba terminada; 404 si no existe.
- `PUT /ordenes/{id}` — cambia patente y trabajo (no el estado); 409 si está terminada.

Probalo con `MockMvc`.

#### Criterio de aprobación

- El estado es un `enum` y el avance se decide en el servicio con un `switch`.
- Las pruebas recorren el ciclo completo de una orden y los 404/409.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>taller</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/taller/TallerApplication.java`

```java
package imperio.taller;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TallerApplication {
    public static void main(String[] args) {
        SpringApplication.run(TallerApplication.class, args);
    }
}
```

`src/main/java/imperio/taller/Estado.java`

```java
package imperio.taller;

public enum Estado { PENDIENTE, EN_CURSO, TERMINADA }
```

`src/main/java/imperio/taller/Orden.java`

```java
package imperio.taller;

public record Orden(Long id, String patente, String trabajo, Estado estado) {
    public Orden con(Estado nuevo) {
        return new Orden(id, patente, trabajo, nuevo);
    }
}
```

`src/main/java/imperio/taller/Conflicto.java`

```java
package imperio.taller;

public class Conflicto extends RuntimeException {
    public Conflicto(String mensaje) {
        super(mensaje);
    }
}
```

`src/main/java/imperio/taller/ServicioOrdenes.java`

```java
package imperio.taller;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.stereotype.Service;

@Service
public class ServicioOrdenes {
    private final Map<Long, Orden> ordenes = new ConcurrentHashMap<>();
    private final AtomicLong proximoId = new AtomicLong(1);

    public Orden crear(String patente, String trabajo) {
        Orden orden = new Orden(proximoId.getAndIncrement(), patente, trabajo, Estado.PENDIENTE);
        ordenes.put(orden.id(), orden);
        return orden;
    }

    public List<Orden> listar(Estado estado) {
        return ordenes.values().stream()
                .filter(o -> estado == null || o.estado() == estado)
                .sorted(Comparator.comparing(Orden::id))
                .toList();
    }

    public synchronized Optional<Orden> avanzar(long id) {
        return Optional.ofNullable(ordenes.get(id)).map(o -> {
            Estado siguiente = switch (o.estado()) {
                case PENDIENTE -> Estado.EN_CURSO;
                case EN_CURSO -> Estado.TERMINADA;
                case TERMINADA -> throw new Conflicto("la orden " + id + " ya está terminada");
            };
            Orden nueva = o.con(siguiente);
            ordenes.put(id, nueva);
            return nueva;
        });
    }

    public synchronized Optional<Orden> modificar(long id, String patente, String trabajo) {
        return Optional.ofNullable(ordenes.get(id)).map(o -> {
            if (o.estado() == Estado.TERMINADA) {
                throw new Conflicto("no se modifica una orden terminada");
            }
            Orden nueva = new Orden(id, patente, trabajo, o.estado());
            ordenes.put(id, nueva);
            return nueva;
        });
    }
}
```

`src/main/java/imperio/taller/OrdenController.java`

```java
package imperio.taller;

import java.net.URI;
import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/ordenes")
public class OrdenController {
    private final ServicioOrdenes servicio;

    public OrdenController(ServicioOrdenes servicio) {
        this.servicio = servicio;
    }

    @PostMapping
    public ResponseEntity<Orden> crear(@RequestBody Orden datos) {
        Orden creada = servicio.crear(datos.patente(), datos.trabajo());
        return ResponseEntity.created(URI.create("/ordenes/" + creada.id())).body(creada);
    }

    @GetMapping
    public List<Orden> listar(@RequestParam(required = false) Estado estado) {
        return servicio.listar(estado);
    }

    @PatchMapping("/{id}/avanzar")
    public ResponseEntity<Orden> avanzar(@PathVariable long id) {
        return servicio.avanzar(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PutMapping("/{id}")
    public ResponseEntity<Orden> modificar(@PathVariable long id, @RequestBody Orden datos) {
        return servicio.modificar(id, datos.patente(), datos.trabajo()).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    // Una excepción del servicio se convierte en un 409.
    @ExceptionHandler(Conflicto.class)
    public ResponseEntity<String> conflicto(Conflicto e) {
        return ResponseEntity.status(HttpStatus.CONFLICT).body(e.getMessage());
    }
}
```

`src/test/java/imperio/taller/OrdenControllerTest.java`

```java
package imperio.taller;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class OrdenControllerTest {
    @Autowired
    private MockMvc mvc;

    private void crear(String patente, String trabajo) throws Exception {
        mvc.perform(post("/ordenes").contentType(MediaType.APPLICATION_JSON)
                        .content("{\"patente\": \"" + patente + "\", \"trabajo\": \"" + trabajo + "\"}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.estado").value("PENDIENTE"));
    }

    @Test
    void elCicloCompletoDeUnaOrden() throws Exception {
        crear("AB123CD", "cambio de aceite");
        mvc.perform(patch("/ordenes/1/avanzar")).andExpect(jsonPath("$.estado").value("EN_CURSO"));
        mvc.perform(put("/ordenes/1").contentType(MediaType.APPLICATION_JSON).content("""
                        {"patente": "AB123CD", "trabajo": "aceite y filtros"}
                        """))
                .andExpect(jsonPath("$.trabajo").value("aceite y filtros"))
                .andExpect(jsonPath("$.estado").value("EN_CURSO"));
        mvc.perform(patch("/ordenes/1/avanzar")).andExpect(jsonPath("$.estado").value("TERMINADA"));
        mvc.perform(patch("/ordenes/1/avanzar")).andExpect(status().isConflict())
                .andExpect(content().string("la orden 1 ya está terminada"));
        mvc.perform(put("/ordenes/1").contentType(MediaType.APPLICATION_JSON).content("""
                        {"patente": "ZZ999ZZ", "trabajo": "otro"}
                        """))
                .andExpect(status().isConflict());
    }

    @Test
    void filtraPorEstadoYContesta404() throws Exception {
        crear("AA111AA", "frenos");
        crear("BB222BB", "embrague");
        mvc.perform(patch("/ordenes/2/avanzar"));
        mvc.perform(get("/ordenes").param("estado", "PENDIENTE"))
                .andExpect(jsonPath("$.length()").value(1))
                .andExpect(jsonPath("$[0].patente").value("AA111AA"));
        mvc.perform(get("/ordenes")).andExpect(jsonPath("$.length()").value(2));
        mvc.perform(patch("/ordenes/7/avanzar")).andExpect(status().isNotFound());
    }
}
```

### Encargo R05-N04-E1 · El turnero del consultorio

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Un consultorio atiende de 9 a 12, con turnos cada 30 minutos (`09:00`, `09:30`, …,
`11:30`). Hacé la API:

- `GET /turnos/{fecha}/libres` — los horarios libres de ese día (fecha `AAAA-MM-DD`).
- `POST /turnos` con `{"fecha", "hora", "paciente"}` — reserva: 201; **409** si el horario
  ya está tomado; **400** si la hora no es uno de los horarios del consultorio.
- `DELETE /turnos/{fecha}/{hora}` — cancela: 204, o 404 si no había turno.

Guardá los turnos en un `ConcurrentHashMap` (la clave puede ser `fecha + " " + hora`) y
usá `putIfAbsent` para que dos pedidos simultáneos no reserven el mismo horario.
Probalo con `MockMvc`.

#### Criterio de aprobación

- La reserva usa una operación atómica (`putIfAbsent`) y responde 201, 400 o 409.
- Las pruebas cubren reservar, el horario tomado, la hora inválida, los libres y cancelar.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>turnero</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/turnero/TurneroApplication.java`

```java
package imperio.turnero;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TurneroApplication {
    public static void main(String[] args) {
        SpringApplication.run(TurneroApplication.class, args);
    }
}
```

`src/main/java/imperio/turnero/Turno.java`

```java
package imperio.turnero;

public record Turno(String fecha, String hora, String paciente) {
}
```

`src/main/java/imperio/turnero/ServicioTurnos.java`

```java
package imperio.turnero;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.stereotype.Service;

@Service
public class ServicioTurnos {
    public static final List<String> HORARIOS = List.of("09:00", "09:30", "10:00", "10:30", "11:00", "11:30");

    public enum Reserva { HECHA, HORA_INVALIDA, OCUPADO }

    private final Map<String, Turno> turnos = new ConcurrentHashMap<>();

    public List<String> libres(String fecha) {
        return HORARIOS.stream().filter(h -> !turnos.containsKey(fecha + " " + h)).toList();
    }

    public Reserva reservar(Turno turno) {
        if (!HORARIOS.contains(turno.hora())) {
            return Reserva.HORA_INVALIDA;
        }
        return turnos.putIfAbsent(turno.fecha() + " " + turno.hora(), turno) == null ? Reserva.HECHA : Reserva.OCUPADO;
    }

    public boolean cancelar(String fecha, String hora) {
        return turnos.remove(fecha + " " + hora) != null;
    }
}
```

`src/main/java/imperio/turnero/TurnoController.java`

```java
package imperio.turnero;

import java.net.URI;
import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/turnos")
public class TurnoController {
    private final ServicioTurnos servicio;

    public TurnoController(ServicioTurnos servicio) {
        this.servicio = servicio;
    }

    @GetMapping("/{fecha}/libres")
    public List<String> libres(@PathVariable String fecha) {
        return servicio.libres(fecha);
    }

    @PostMapping
    public ResponseEntity<Turno> reservar(@RequestBody Turno turno) {
        return switch (servicio.reservar(turno)) {
            case HECHA -> ResponseEntity.created(URI.create("/turnos/" + turno.fecha() + "/" + turno.hora())).body(turno);
            case HORA_INVALIDA -> ResponseEntity.badRequest().build();
            case OCUPADO -> ResponseEntity.status(HttpStatus.CONFLICT).build();
        };
    }

    @DeleteMapping("/{fecha}/{hora}")
    public ResponseEntity<Void> cancelar(@PathVariable String fecha, @PathVariable String hora) {
        return servicio.cancelar(fecha, hora) ? ResponseEntity.noContent().build() : ResponseEntity.notFound().build();
    }
}
```

`src/test/java/imperio/turnero/TurnoControllerTest.java`

```java
package imperio.turnero;

import static org.hamcrest.Matchers.contains;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class TurnoControllerTest {
    @Autowired
    private MockMvc mvc;

    private ResultActions reservar(String hora, String paciente) throws Exception {
        return mvc.perform(post("/turnos").contentType(MediaType.APPLICATION_JSON)
                .content("{\"fecha\": \"2026-10-05\", \"hora\": \"" + hora + "\", \"paciente\": \"" + paciente + "\"}"));
    }

    @Test
    void reservaYElHorarioQuedaTomado() throws Exception {
        reservar("09:30", "Ana").andExpect(status().isCreated());
        reservar("09:30", "Leo").andExpect(status().isConflict());
        reservar("11:00", "Leo").andExpect(status().isCreated());
        mvc.perform(get("/turnos/2026-10-05/libres"))
                .andExpect(jsonPath("$", contains("09:00", "10:00", "10:30", "11:30")));
        mvc.perform(get("/turnos/2026-10-06/libres")).andExpect(jsonPath("$.length()").value(6));
    }

    @Test
    void unaHoraFueraDelHorarioEs400() throws Exception {
        reservar("13:00", "Ana").andExpect(status().isBadRequest());
        reservar("09:15", "Ana").andExpect(status().isBadRequest());
    }

    @Test
    void cancelaYLiberaElHorario() throws Exception {
        reservar("10:00", "Ana");
        mvc.perform(delete("/turnos/2026-10-05/10:00")).andExpect(status().isNoContent());
        mvc.perform(delete("/turnos/2026-10-05/10:00")).andExpect(status().isNotFound());
        reservar("10:00", "Leo").andExpect(status().isCreated());
    }
}
```

### Prueba del sello

#### ¿Qué verbo HTTP usás para crear y qué código devolvés?

`POST`, y `201 Created` con la ruta del nuevo en `Location`.

#### ¿Qué diferencia hay entre `@PathVariable` y `@RequestParam`?

`@PathVariable` toma un dato de la ruta (`/heroes/3`); `@RequestParam`, de la consulta (`/heroes?clase=maga`).

#### ¿Para qué sirve `ResponseEntity`?

Para elegir el código de estado y los encabezados de la respuesta, además del cuerpo.

#### ¿Por qué el controlador no debería tener lógica?

Para que las reglas estén en el servicio, se prueben sin HTTP y no se repitan.

#### ¿Qué hace `MockMvc`?

Simula pedidos HTTP a la aplicación sin abrir un puerto, y deja comprobar el código y el JSON de la respuesta.

### Soluciones (docente)

Sale de `19-Java-Avanzado/09-Spring-MVC-REST`. Las pruebas usan `@DirtiesContext` para que cada una arranque con los datos iniciales (los servicios guardan en memoria). Se corrige con `./mvnw test` y probando un par de rutas con `curl`.

## R05-N05 · DTO, validaciones y errores

```meta
tipo: tema
padre: R05-N04
precio: 10
criatura: troll
ejecutable: no
temas: web.api-rest, err.validacion
usa: fw.spring
```

### Crónica

La ventanilla al Puerto empezó a recibir cualquier cosa: pedidos sin nombre, cargamentos de peso negativo, correos sin arroba. Y cuando algo fallaba, devolvía un papel con trescientas líneas de error en idioma de máquina. En el quinto piso, {mentor} separa el servicio en **cuatro salas** que no se pisan.

—Una buena ventanilla **controla lo que entra** y **explica lo que sale** —dice—. Lo que recibe se revisa antes de tocar nada, lo que devuelve muestra solo lo necesario, y cada error dice qué pasó en palabras que se entienden. Y de paso, vamos a dejar de escribir *getters* a mano. Vos, que entrabas por cualquier lado, Zed, ahora vas a **diseñar las puertas**.

### Objetivos

- Separar lo que entra y sale de la API (DTO) del modelo interno.
- Validar los datos de entrada con Bean Validation (`@NotBlank`, `@Email`, `@Min`, `@Size`, `@Valid`).
- Centralizar el manejo de errores con `@RestControllerAdvice` y responder con `ProblemDetail`.
- Reducir código repetido con Lombok.

### Antes de empezar

- Servicios REST.

### Explicación

#### DTO: lo que viaja no es lo que se guarda
Un **DTO** (*Data Transfer Object*) es un objeto pensado solo para entrar o salir por la
API. ¿Por qué no devolver directamente el modelo?
- El modelo puede tener datos que **no** tienen que salir (la clave de un usuario, un
  costo interno).
- Lo que se pide al crear no es lo mismo que lo que se devuelve (el `id` lo pone el
  sistema, no el cliente).
- Si cambia el modelo, la API no tiene que cambiar.

```java
public record AlumnoPedido(String nombre, String email, int edad) { }           // lo que entra
public record AlumnoRespuesta(long id, String nombre, String comision) { }      // lo que sale
```
Los `record` son perfectos para los DTO. El servicio convierte de uno a otro.

#### Validar lo que entra
Con `spring-boot-starter-validation`, los DTO se anotan con reglas y el controlador las
hace cumplir con `@Valid`:
```java
public record AlumnoPedido(
        @NotBlank(message = "el nombre es obligatorio") String nombre,
        @NotBlank @Email(message = "el email no es válido") String email,
        @Min(value = 16, message = "la edad mínima es 16") int edad) { }

@PostMapping
public ResponseEntity<AlumnoRespuesta> inscribir(@Valid @RequestBody AlumnoPedido pedido) { … }
```
Si algo no cumple, Spring **no llama** al método y responde `400 Bad Request`.

| Anotación | Exige |
|---|---|
| `@NotNull` | que no sea `null` |
| `@NotBlank` | texto no vacío (ni solo espacios) |
| `@Size(min, max)` | largo de un texto o de una lista |
| `@Min`, `@Max`, `@Positive` | rangos de números |
| `@Email`, `@Pattern(regexp)` | formato |
| `@Past`, `@Future` | fechas |
| `@AssertTrue` | que un método `boolean` dé `true` (reglas entre campos) |

#### Errores claros con `@RestControllerAdvice`
Un `@RestControllerAdvice` atrapa las excepciones de **todos** los controladores y las
convierte en respuestas. Spring trae `ProblemDetail`, un formato estándar para errores
(RFC 9457):
```java
@RestControllerAdvice
public class ManejoDeErrores {
    @ExceptionHandler(NoEncontrado.class)
    public ProblemDetail noEncontrado(NoEncontrado e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail invalido(MethodArgumentNotValidException e) {
        ProblemDetail p = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "datos inválidos");
        Map<String, String> campos = new TreeMap<>();
        e.getBindingResult().getFieldErrors().forEach(f -> campos.put(f.getField(), f.getDefaultMessage()));
        p.setProperty("campos", campos);
        return p;
    }
}
```
La respuesta queda así:
```json
{"type": "about:blank", "title": "Bad Request", "status": 400, "detail": "datos inválidos",
 "instance": "/alumnos", "campos": {"edad": "la edad mínima es 16", "nombre": "el nombre es obligatorio"}}
```
El servicio lanza excepciones propias (`NoEncontrado`, `Conflicto`) y ya no se ocupa de
HTTP; el *advice* decide el código.

#### Lombok: menos código repetido
Las clases del modelo (que no pueden ser `record` porque cambian, como las entidades del
próximo nodo) necesitan constructores, *getters* y *setters*. **Lombok** los genera al
compilar a partir de anotaciones:
| Anotación | Genera |
|---|---|
| `@Getter`, `@Setter` | los *getters* y *setters* |
| `@NoArgsConstructor`, `@AllArgsConstructor` | constructores |
| `@RequiredArgsConstructor` | un constructor con los atributos `final` (ideal para inyectar) |
| `@ToString`, `@EqualsAndHashCode` | esos métodos |
| `@Builder` | un constructor paso a paso: `Alumno.builder().nombre("Ana").edad(20).build()` |

```java
@Service
@RequiredArgsConstructor
public class ServicioAlumnos {
    private final RepositorioAlumnos repositorio;      // Lombok arma el constructor
}
```
Lombok necesita la dependencia en el `pom.xml` y, en el IDE, el plugin de Lombok (IntelliJ
ya lo trae). Desde Java 23 hay que declararlo también como procesador de anotaciones del
compilador: los `pom.xml` de este nodo ya lo hacen.

> **Si venís de Python.** Los DTO con validación se parecen a los modelos de Pydantic en
> FastAPI, y Lombok a los `@dataclass`.

### Código de ejemplo

La inscripción a las comisiones: DTO de entrada y salida, validación, errores con
`ProblemDetail` y el modelo con Lombok.

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>inscripciones</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                            <version>${lombok.version}</version>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/inscripciones/InscripcionesApplication.java`

```java
package imperio.inscripciones;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class InscripcionesApplication {
    public static void main(String[] args) {
        SpringApplication.run(InscripcionesApplication.class, args);
    }
}
```

`src/main/java/imperio/inscripciones/Alumno.java`

```java
package imperio.inscripciones;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

// El modelo interno: tiene el DNI, que nunca sale por la API.
@Getter
@Setter
@AllArgsConstructor
public class Alumno {
    private long id;
    private String nombre;
    private String email;
    private String dni;
    private String comision;
}
```

`src/main/java/imperio/inscripciones/AlumnoPedido.java`

```java
package imperio.inscripciones;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;

public record AlumnoPedido(
        @NotBlank(message = "el nombre es obligatorio") String nombre,
        @NotBlank(message = "el email es obligatorio") @Email(message = "el email no es válido") String email,
        @Pattern(regexp = "\\d{7,8}", message = "el DNI tiene que tener 7 u 8 dígitos") String dni,
        @Pattern(regexp = "[A-C]", message = "la comisión es A, B o C") String comision) {
}
```

`src/main/java/imperio/inscripciones/AlumnoRespuesta.java`

```java
package imperio.inscripciones;

public record AlumnoRespuesta(long id, String nombre, String email, String comision) {
    static AlumnoRespuesta de(Alumno a) {
        return new AlumnoRespuesta(a.getId(), a.getNombre(), a.getEmail(), a.getComision());
    }
}
```

`src/main/java/imperio/inscripciones/NoEncontrado.java`

```java
package imperio.inscripciones;

public class NoEncontrado extends RuntimeException {
    public NoEncontrado(String mensaje) {
        super(mensaje);
    }
}
```

`src/main/java/imperio/inscripciones/Conflicto.java`

```java
package imperio.inscripciones;

public class Conflicto extends RuntimeException {
    public Conflicto(String mensaje) {
        super(mensaje);
    }
}
```

`src/main/java/imperio/inscripciones/ServicioInscripciones.java`

```java
package imperio.inscripciones;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.stereotype.Service;

@Service
public class ServicioInscripciones {
    private final Map<Long, Alumno> alumnos = new ConcurrentHashMap<>();
    private final AtomicLong proximoId = new AtomicLong(1);

    public synchronized Alumno inscribir(AlumnoPedido pedido) {
        boolean repetido = alumnos.values().stream().anyMatch(a -> a.getDni().equals(pedido.dni()));
        if (repetido) {
            throw new Conflicto("ya hay un alumno con el DNI " + pedido.dni());
        }
        Alumno alumno = new Alumno(proximoId.getAndIncrement(), pedido.nombre(), pedido.email(), pedido.dni(), pedido.comision());
        alumnos.put(alumno.getId(), alumno);
        return alumno;
    }

    public Alumno buscar(long id) {
        Alumno a = alumnos.get(id);
        if (a == null) {
            throw new NoEncontrado("no existe el alumno " + id);
        }
        return a;
    }
}
```

`src/main/java/imperio/inscripciones/AlumnoController.java`

```java
package imperio.inscripciones;

import java.net.URI;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/alumnos")
@RequiredArgsConstructor
public class AlumnoController {
    private final ServicioInscripciones servicio;

    @PostMapping
    public ResponseEntity<AlumnoRespuesta> inscribir(@Valid @RequestBody AlumnoPedido pedido) {
        Alumno a = servicio.inscribir(pedido);
        return ResponseEntity.created(URI.create("/alumnos/" + a.getId())).body(AlumnoRespuesta.de(a));
    }

    @GetMapping("/{id}")
    public AlumnoRespuesta buscar(@PathVariable long id) {
        return AlumnoRespuesta.de(servicio.buscar(id));
    }
}
```

`src/main/java/imperio/inscripciones/ManejoDeErrores.java`

```java
package imperio.inscripciones;

import java.util.Map;
import java.util.TreeMap;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ManejoDeErrores {
    @ExceptionHandler(NoEncontrado.class)
    public ProblemDetail noEncontrado(NoEncontrado e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
    }

    @ExceptionHandler(Conflicto.class)
    public ProblemDetail conflicto(Conflicto e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail invalido(MethodArgumentNotValidException e) {
        ProblemDetail p = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "datos inválidos");
        Map<String, String> campos = new TreeMap<>();
        e.getBindingResult().getFieldErrors().forEach(f -> campos.putIfAbsent(f.getField(), f.getDefaultMessage()));
        p.setProperty("campos", campos);
        return p;
    }
}
```

`src/test/java/imperio/inscripciones/AlumnoControllerTest.java`

```java
package imperio.inscripciones;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class AlumnoControllerTest {
    @Autowired
    private MockMvc mvc;

    private ResultActions inscribir(String json) throws Exception {
        return mvc.perform(post("/alumnos").contentType(MediaType.APPLICATION_JSON).content(json));
    }

    @Test
    void inscribeYNoDevuelveElDni() throws Exception {
        inscribir("""
                {"nombre": "Ana Ruiz", "email": "ana@correo.com", "dni": "41222333", "comision": "B"}
                """)
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.comision").value("B"))
                .andExpect(jsonPath("$.dni").doesNotExist());
    }

    @Test
    void losDatosInvalidosDan400ConCadaCampo() throws Exception {
        inscribir("""
                {"nombre": " ", "email": "ana-correo", "dni": "123", "comision": "Z"}
                """)
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.detail").value("datos inválidos"))
                .andExpect(jsonPath("$.campos.nombre").value("el nombre es obligatorio"))
                .andExpect(jsonPath("$.campos.email").value("el email no es válido"))
                .andExpect(jsonPath("$.campos.dni").value("el DNI tiene que tener 7 u 8 dígitos"))
                .andExpect(jsonPath("$.campos.comision").value("la comisión es A, B o C"));
    }

    @Test
    void elDniRepetidoEs409YElInexistente404() throws Exception {
        String ana = """
                {"nombre": "Ana Ruiz", "email": "ana@correo.com", "dni": "41222333", "comision": "B"}
                """;
        inscribir(ana).andExpect(status().isCreated());
        inscribir(ana).andExpect(status().isConflict())
                .andExpect(jsonPath("$.detail").value("ya hay un alumno con el DNI 41222333"));
        mvc.perform(get("/alumnos/9")).andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status").value(404));
    }
}
```

Un pedido inválido contesta:

```
$ curl -s localhost:8080/alumnos -H "Content-Type: application/json" -d '{"nombre":"","email":"x","dni":"1","comision":"A"}'
{"type":"about:blank","title":"Bad Request","status":400,"detail":"datos inválidos","instance":"/alumnos",
 "campos":{"dni":"el DNI tiene que tener 7 u 8 dígitos","email":"el email no es válido","nombre":"el nombre es obligatorio"}}
```

### ¿Para qué sirve?

Una API pública recibe datos de cualquiera: validar en la entrada evita basura en la base y agujeros de seguridad. Los errores claros y uniformes le ahorran horas al equipo que arma la app o la página que usa tu API. Y los DTO evitan el clásico error de filtrar datos privados (claves, documentos) en una respuesta.

### Errores habituales

**Troll: el `@Valid` olvidado.** Las anotaciones del DTO no hacen nada si el parámetro no
tiene `@Valid`: los datos inválidos entran igual.

**Ogro: devolver la entidad.** Devolver el modelo interno expone todos sus campos
(claves, DNI, costos). Devolvé un DTO de respuesta.

**Goblin: el `@NotNull` en un `int`.** Un `int` nunca es `null`: si falta en el JSON vale
`0`. Para exigir que venga, usá `Integer` con `@NotNull`, o un `@Min`.

**Ogro: el `try`/`catch` en cada controlador.** Repetir el manejo de errores en cada
método. Lanzá excepciones propias desde el servicio y convertilas en un solo
`@RestControllerAdvice`.

**Slime: Lombok que no genera nada.** `cannot find symbol: method getNombre()`: falta el
plugin de Lombok en el IDE, o (desde Java 23) el procesador de anotaciones en el
`pom.xml`.

### Micro-misión R05-N05-P1 · Lo que viaja no es lo que se guarda

```meta
lugar: Las cuatro salas de la Torre
personajes: Zed, Gheco, Nadia, Kaffa
carta: DTO | un objeto solo para lo que entra o sale · el modelo guarda todo (también lo secreto) · la respuesta NUNCA es el modelo
recompensa: xp 10, oro 10
```

#### Escena
En el quinto piso, Kaffa separa el servicio en salas que no se pisan. El modelo `Viajero` guarda el pasaporte y una **clave**; si se devuelve tal cual, la clave viaja al Puerto. —Lo que sale por la ventanilla es un **DTO** —dice—, nunca el modelo.

#### Gheco sugiere
Un **DTO** es un objeto (casi siempre un `record`) con solo lo que tiene que viajar. Se arma desde el modelo con lo necesario: `new ViajeroRespuesta(v.nombre(), v.pasaporte())`. La clave se queda adentro.

#### Desafío
Completá la respuesta con el nombre y el pasaporte, sin la clave.

#### Código inicial
```java
public class Dto {
    record Viajero(String nombre, String pasaporte, String clave) { }

    record ViajeroRespuesta(String nombre, String pasaporte) { }

    static ViajeroRespuesta aRespuesta(Viajero v) {
        return ___;
    }

    public static void main(String[] args) {
        Viajero zed = new Viajero("Zed", "PU-777", "techos123");
        System.out.println("Se guarda: " + zed);
        System.out.println("Viaja: " + aRespuesta(zed));
    }
}
```

#### Salida esperada
```
Se guarda: Viajero[nombre=Zed, pasaporte=PU-777, clave=techos123]
Viaja: ViajeroRespuesta[nombre=Zed, pasaporte=PU-777]
```

#### Solución
```java
public class Dto {
    record Viajero(String nombre, String pasaporte, String clave) { }

    record ViajeroRespuesta(String nombre, String pasaporte) { }

    static ViajeroRespuesta aRespuesta(Viajero v) {
        return new ViajeroRespuesta(v.nombre(), v.pasaporte());
    }

    public static void main(String[] args) {
        Viajero zed = new Viajero("Zed", "PU-777", "techos123");
        System.out.println("Se guarda: " + zed);
        System.out.println("Viaja: " + aRespuesta(zed));
    }
}
```

#### Al superarla
La clave «techos123» se queda en la Torre. —¿«techos123»? —pregunta Nadia. —Era una clave vieja —dice Zed, y la cambia esa misma noche.

#### Imagen
- Dos salas de la Torre separadas por una ventanilla: adentro, una ficha completa con una clave; afuera, una tarjeta con solo nombre y pasaporte.
- Nadia levantando una ceja; Zed rascándose la nuca.

### Micro-misión R05-N05-P2 · Lo que entra se valida

```meta
lugar: Las cuatro salas de la Torre
personajes: Zed, Gheco, Nadia, Kaffa
criatura: goblin
carta: Validar la entrada | cada campo con su regla · se juntan TODOS los errores, no solo el primero · en Spring: @NotBlank, @Positive y @Valid
recompensa: xp 15, oro 15
```

#### Escena
Del Puerto llega un pedido con el nombre vacío y los kilos en −3. Un **goblin** los mandó a propósito, para ver qué se rompe. La ventanilla tiene que rechazarlo y decir **todo** lo que está mal.

#### Gheco sugiere
Se revisa cada campo y se **juntan** los errores en una lista: así el que mandó el pedido sabe todo lo que tiene que corregir. En Spring, las anotaciones `@NotBlank` y `@Positive` del DTO y `@Valid` en el controlador hacen esto solas.

#### Desafío
Completá la regla de los kilos: tienen que ser mayores que cero.

#### Código inicial
```java
import java.util.ArrayList;
import java.util.List;

public class Validar {
    record EnvioPedido(String destinatario, int kilos) { }

    static List<String> validar(EnvioPedido p) {
        List<String> errores = new ArrayList<>();
        if (p.destinatario() == null || p.destinatario().isBlank()) {
            errores.add("destinatario: no puede estar vacío");
        }
        if (___) {
            errores.add("kilos: tiene que ser mayor que 0");
        }
        return errores;
    }

    public static void main(String[] args) {
        System.out.println(validar(new EnvioPedido("Baldo", 30)));
        System.out.println(validar(new EnvioPedido("", -3)));
    }
}
```

#### Salida esperada
```
[]
[destinatario: no puede estar vacío, kilos: tiene que ser mayor que 0]
```

#### Solución
```java
import java.util.ArrayList;
import java.util.List;

public class Validar {
    record EnvioPedido(String destinatario, int kilos) { }

    static List<String> validar(EnvioPedido p) {
        List<String> errores = new ArrayList<>();
        if (p.destinatario() == null || p.destinatario().isBlank()) {
            errores.add("destinatario: no puede estar vacío");
        }
        if (p.kilos() <= 0) {
            errores.add("kilos: tiene que ser mayor que 0");
        }
        return errores;
    }

    public static void main(String[] args) {
        System.out.println(validar(new EnvioPedido("Baldo", 30)));
        System.out.println(validar(new EnvioPedido("", -3)));
    }
}
```

#### Al superarla
El pedido de Baldo pasa limpio; el del goblin vuelve con sus dos errores anotados. El goblin, ofendido, corrige y lo manda bien.

#### Imagen
- Una ventanilla devolviendo un pergamino con dos errores marcados en rojo.
- Un goblin corrigiendo su pedido de mala gana.

### Micro-misión R05-N05-P3 · Un error que se entiende

```meta
lugar: Las cuatro salas de la Torre
personajes: Zed, Gheco, Nadia, Kaffa
carta: Errores claros | una excepción propia por cada problema · un manejador central la convierte en la respuesta (código + detalle) · en Spring: @RestControllerAdvice y ProblemDetail
recompensa: xp 15, oro 15
```

#### Escena
Cuando algo falla adentro, al Puerto le llega un «500» y un chorro de líneas en inglés. —Un error también es una respuesta —dice Kaffa—. Que diga **qué** pasó, con el código que corresponde.

#### Gheco sugiere
El servicio lanza una excepción propia (`NoEncontrado`); un **manejador central** la atrapa y arma la respuesta: el código (404) y un detalle claro. En Spring, eso es un `@RestControllerAdvice` que devuelve un `ProblemDetail`.

#### Desafío
Completá el manejador: atrapá la excepción `NoEncontrado`.

#### Código inicial
```java
import java.util.Map;

public class Errores {
    static class NoEncontrado extends RuntimeException {
        NoEncontrado(String mensaje) { super(mensaje); }
    }

    static final Map<String, Integer> ENVIOS = Map.of("E1", 30);

    static int buscar(String codigo) {
        Integer kilos = ENVIOS.get(codigo);
        if (kilos == null) {
            throw new NoEncontrado("No existe el envío " + codigo);
        }
        return kilos;
    }

    static String atender(String codigo) {
        try {
            return "200 {\"kilos\": " + buscar(codigo) + "}";
        } catch (___ e) {
            return "404 {\"detail\": \"" + e.getMessage() + "\"}";
        }
    }

    public static void main(String[] args) {
        System.out.println(atender("E1"));
        System.out.println(atender("E9"));
    }
}
```

#### Salida esperada
```
200 {"kilos": 30}
404 {"detail": "No existe el envío E9"}
```

#### Solución
```java
import java.util.Map;

public class Errores {
    static class NoEncontrado extends RuntimeException {
        NoEncontrado(String mensaje) { super(mensaje); }
    }

    static final Map<String, Integer> ENVIOS = Map.of("E1", 30);

    static int buscar(String codigo) {
        Integer kilos = ENVIOS.get(codigo);
        if (kilos == null) {
            throw new NoEncontrado("No existe el envío " + codigo);
        }
        return kilos;
    }

    static String atender(String codigo) {
        try {
            return "200 {\"kilos\": " + buscar(codigo) + "}";
        } catch (NoEncontrado e) {
            return "404 {\"detail\": \"" + e.getMessage() + "\"}";
        }
    }

    public static void main(String[] args) {
        System.out.println(atender("E1"));
        System.out.println(atender("E9"));
    }
}
```

#### Al superarla
«404, no existe el envío E9.» El Puerto lo entiende a la primera. Las campanas de los Archivos, ahora con forma de respuesta HTTP.

#### Imagen
- Una campana de los Archivos convertida en un cartel de respuesta: «404 · No existe el envío E9».
- Kaffa asintiendo con la taza en la mano.

### Micro-misión R05-N05-P4 · Lo que escribe Lombok

```meta
lugar: Las cuatro salas de la Torre
personajes: Zed, Gheco, Nadia, Kaffa
carta: Lombok | @Getter, @Setter, @RequiredArgsConstructor, @Builder escriben ese código al compilar · acá lo escribimos a mano para ver qué genera
recompensa: xp 15, oro 20
```

#### Escena
Las clases del modelo que cambian no pueden ser `record` y necesitan constructores, getters y setters: cincuenta líneas iguales. **Lombok** las escribe solo con anotaciones. Gheco escribe a mano lo que genera un `@Builder`, para que Zed vea que no es magia.

#### Gheco sugiere
Un **builder** arma el objeto paso a paso: `Envio.builder().destinatario("Baldo").kilos(30).build()`. Cada método guarda un dato y devuelve el mismo builder (`return this;`), y `build()` crea el objeto. Con Lombok, `@Builder` escribe todo esto solo.

#### Desafío
Completá el método del builder que guarda los kilos y devuelve el builder.

#### Código inicial
```java
public class Lombok {
    public static void main(String[] args) {
        Envio e = Envio.builder().destinatario("Baldo").kilos(30).build();
        System.out.println(e.getDestinatario() + ": " + e.getKilos() + " kg");
    }
}

class Envio {
    private final String destinatario;
    private final int kilos;

    private Envio(String destinatario, int kilos) {
        this.destinatario = destinatario;
        this.kilos = kilos;
    }

    String getDestinatario() { return destinatario; }

    int getKilos() { return kilos; }

    static Builder builder() { return new Builder(); }

    static class Builder {
        private String destinatario;
        private int kilos;

        Builder destinatario(String d) {
            this.destinatario = d;
            return this;
        }

        Builder kilos(int k) {
            ___;
        }

        Envio build() { return new Envio(destinatario, kilos); }
    }
}
```

#### Salida esperada
```
Baldo: 30 kg
```

#### Solución
```java
public class Lombok {
    public static void main(String[] args) {
        Envio e = Envio.builder().destinatario("Baldo").kilos(30).build();
        System.out.println(e.getDestinatario() + ": " + e.getKilos() + " kg");
    }
}

class Envio {
    private final String destinatario;
    private final int kilos;

    private Envio(String destinatario, int kilos) {
        this.destinatario = destinatario;
        this.kilos = kilos;
    }

    String getDestinatario() { return destinatario; }

    int getKilos() { return kilos; }

    static Builder builder() { return new Builder(); }

    static class Builder {
        private String destinatario;
        private int kilos;

        Builder destinatario(String d) {
            this.destinatario = d;
            return this;
        }

        Builder kilos(int k) {
            this.kilos = k;
            return this;
        }

        Envio build() { return new Envio(destinatario, kilos); }
    }
}
```

#### Al superarla
Treinta líneas para un builder… que Lombok escribe con **una** anotación. —Ahora que sabés lo que hace —dice Kaffa—, usalo sin culpa.
Zed, que entraba por cualquier lado, ahora **diseña las puertas** de su propio servicio. En la cima de la Torre, el Tribunal deja un pliego sobre la mesa.

#### Imagen
- Una pila de treinta líneas de código que se comprime en una sola etiqueta: «@Builder».
- En la cima de la Torre, un pliego lacrado sobre una mesa de piedra, con la palabra «AduanaExpress».

### Misión R05-N05-M1 · El registro de usuarios

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Hacé `POST /usuarios` para registrar usuarios con un DTO `RegistroPedido`: `usuario`
(3 a 20 letras, números o guion bajo), `email` (válido), `clave` (al menos 8
caracteres) y `fechaNacimiento` (`LocalDate`, en el pasado). La respuesta es un
`UsuarioRespuesta` **sin la clave**. El servicio guarda la clave **cifrada** (para esta
misión alcanza con el SHA-256 en hexadecimal) en el modelo `Usuario` hecho con Lombok, y
lanza un conflicto si el usuario o el email ya existen. Los errores salen como
`ProblemDetail` con los campos inválidos. `GET /usuarios/{usuario}` devuelve el usuario o
404.

#### Criterio de aprobación

- Validaciones con Bean Validation y `@Valid`; la clave nunca aparece en una respuesta.
- Errores 400 (con campos), 404 y 409 desde un `@RestControllerAdvice`.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>usuarios</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                            <version>${lombok.version}</version>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/usuarios/UsuariosApplication.java`

```java
package imperio.usuarios;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class UsuariosApplication {
    public static void main(String[] args) {
        SpringApplication.run(UsuariosApplication.class, args);
    }
}
```

`src/main/java/imperio/usuarios/Usuario.java`

```java
package imperio.usuarios;

import java.time.LocalDate;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class Usuario {
    private final String usuario;
    private final String email;
    private final String claveCifrada;
    private final LocalDate fechaNacimiento;
}
```

`src/main/java/imperio/usuarios/RegistroPedido.java`

```java
package imperio.usuarios;

import java.time.LocalDate;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Past;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

public record RegistroPedido(
        @NotNull(message = "el usuario es obligatorio")
        @Pattern(regexp = "\\w{3,20}", message = "el usuario lleva de 3 a 20 letras, números o _") String usuario,
        @NotBlank(message = "el email es obligatorio") @Email(message = "el email no es válido") String email,
        @NotNull(message = "la clave es obligatoria") @Size(min = 8, message = "la clave necesita al menos 8 caracteres") String clave,
        @NotNull(message = "la fecha de nacimiento es obligatoria") @Past(message = "la fecha de nacimiento tiene que ser pasada") LocalDate fechaNacimiento) {
}
```

`src/main/java/imperio/usuarios/UsuarioRespuesta.java`

```java
package imperio.usuarios;

import java.time.LocalDate;

public record UsuarioRespuesta(String usuario, String email, LocalDate fechaNacimiento) {
    static UsuarioRespuesta de(Usuario u) {
        return new UsuarioRespuesta(u.getUsuario(), u.getEmail(), u.getFechaNacimiento());
    }
}
```

`src/main/java/imperio/usuarios/NoEncontrado.java`

```java
package imperio.usuarios;

public class NoEncontrado extends RuntimeException {
    public NoEncontrado(String mensaje) {
        super(mensaje);
    }
}
```

`src/main/java/imperio/usuarios/Conflicto.java`

```java
package imperio.usuarios;

public class Conflicto extends RuntimeException {
    public Conflicto(String mensaje) {
        super(mensaje);
    }
}
```

`src/main/java/imperio/usuarios/ServicioUsuarios.java`

```java
package imperio.usuarios;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.stereotype.Service;

@Service
public class ServicioUsuarios {
    private final Map<String, Usuario> usuarios = new ConcurrentHashMap<>();

    public synchronized Usuario registrar(RegistroPedido p) {
        if (usuarios.containsKey(p.usuario())) {
            throw new Conflicto("el usuario " + p.usuario() + " ya existe");
        }
        if (usuarios.values().stream().anyMatch(u -> u.getEmail().equalsIgnoreCase(p.email()))) {
            throw new Conflicto("el email ya está registrado");
        }
        Usuario u = new Usuario(p.usuario(), p.email(), sha256(p.clave()), p.fechaNacimiento());
        usuarios.put(u.getUsuario(), u);
        return u;
    }

    public Usuario buscar(String usuario) {
        Usuario u = usuarios.get(usuario);
        if (u == null) {
            throw new NoEncontrado("no existe el usuario " + usuario);
        }
        return u;
    }

    static String sha256(String texto) {
        try {
            byte[] hash = MessageDigest.getInstance("SHA-256").digest(texto.getBytes(StandardCharsets.UTF_8));
            return HexFormat.of().formatHex(hash);
        } catch (NoSuchAlgorithmException e) {
            throw new IllegalStateException(e);
        }
    }
}
```

`src/main/java/imperio/usuarios/UsuarioController.java`

```java
package imperio.usuarios;

import java.net.URI;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/usuarios")
@RequiredArgsConstructor
public class UsuarioController {
    private final ServicioUsuarios servicio;

    @PostMapping
    public ResponseEntity<UsuarioRespuesta> registrar(@Valid @RequestBody RegistroPedido pedido) {
        Usuario u = servicio.registrar(pedido);
        return ResponseEntity.created(URI.create("/usuarios/" + u.getUsuario())).body(UsuarioRespuesta.de(u));
    }

    @GetMapping("/{usuario}")
    public UsuarioRespuesta buscar(@PathVariable String usuario) {
        return UsuarioRespuesta.de(servicio.buscar(usuario));
    }
}
```

`src/main/java/imperio/usuarios/ManejoDeErrores.java`

```java
package imperio.usuarios;

import java.util.Map;
import java.util.TreeMap;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ManejoDeErrores {
    @ExceptionHandler(NoEncontrado.class)
    public ProblemDetail noEncontrado(NoEncontrado e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
    }

    @ExceptionHandler(Conflicto.class)
    public ProblemDetail conflicto(Conflicto e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail invalido(MethodArgumentNotValidException e) {
        ProblemDetail p = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "datos inválidos");
        Map<String, String> campos = new TreeMap<>();
        e.getBindingResult().getFieldErrors().forEach(f -> campos.putIfAbsent(f.getField(), f.getDefaultMessage()));
        p.setProperty("campos", campos);
        return p;
    }
}
```

`src/test/java/imperio/usuarios/UsuarioControllerTest.java`

```java
package imperio.usuarios;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class UsuarioControllerTest {
    @Autowired
    private MockMvc mvc;

    @Autowired
    private ServicioUsuarios servicio;

    private ResultActions registrar(String json) throws Exception {
        return mvc.perform(post("/usuarios").contentType(MediaType.APPLICATION_JSON).content(json));
    }

    private static final String NADIA = """
            {"usuario": "nadia_07", "email": "nadia@correo.com", "clave": "flechas123", "fechaNacimiento": "2004-05-17"}
            """;

    @Test
    void registraSinDevolverLaClaveYLaGuardaCifrada() throws Exception {
        registrar(NADIA).andExpect(status().isCreated())
                .andExpect(jsonPath("$.usuario").value("nadia_07"))
                .andExpect(jsonPath("$.clave").doesNotExist())
                .andExpect(jsonPath("$.claveCifrada").doesNotExist());
        assertEquals(64, servicio.buscar("nadia_07").getClaveCifrada().length());
        mvc.perform(get("/usuarios/nadia_07")).andExpect(jsonPath("$.fechaNacimiento").value("2004-05-17"));
    }

    @Test
    void validaCadaCampo() throws Exception {
        registrar("""
                {"usuario": "k!", "email": "nadia", "clave": "corta", "fechaNacimiento": "2999-01-01"}
                """)
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.usuario").value("el usuario lleva de 3 a 20 letras, números o _"))
                .andExpect(jsonPath("$.campos.email").value("el email no es válido"))
                .andExpect(jsonPath("$.campos.clave").value("la clave necesita al menos 8 caracteres"))
                .andExpect(jsonPath("$.campos.fechaNacimiento").value("la fecha de nacimiento tiene que ser pasada"));
    }

    @Test
    void usuarioOEmailRepetidosDan409() throws Exception {
        registrar(NADIA).andExpect(status().isCreated());
        registrar(NADIA).andExpect(status().isConflict()).andExpect(jsonPath("$.detail").value("el usuario nadia_07 ya existe"));
        registrar("""
                {"usuario": "otra", "email": "NADIA@correo.com", "clave": "flechas123", "fechaNacimiento": "2004-05-17"}
                """).andExpect(status().isConflict()).andExpect(jsonPath("$.detail").value("el email ya está registrado"));
        mvc.perform(get("/usuarios/nadie")).andExpect(status().isNotFound());
    }
}
```

### Misión R05-N05-M2 · El presupuesto con Lombok

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Un corralón arma presupuestos. Modelá con Lombok un `Presupuesto` (con `@Builder`,
`@Getter` y `@ToString`) que tiene cliente, una lista de `Item` (también con Lombok:
material, cantidad, precio unitario) y un descuento en porcentaje, con un método
`total()`. Hacé `POST /presupuestos` que recibe un DTO con validaciones **anidadas**: el
cliente es obligatorio, la lista de ítems no puede estar vacía (`@NotEmpty`) y **cada**
ítem se valida (`@Valid` en la lista: cantidad positiva, precio positivo); el descuento
va de 0 a 30. La respuesta trae el total calculado. Los errores de los ítems tienen que
indicar cuál (por ejemplo `items[1].cantidad`).

#### Criterio de aprobación

- El modelo usa Lombok (`@Builder`, `@Getter`) y el servicio `@RequiredArgsConstructor` o nada que inyectar.
- La validación anidada informa el ítem y el campo que fallan.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>corralon</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                            <version>${lombok.version}</version>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/corralon/CorralonApplication.java`

```java
package imperio.corralon;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class CorralonApplication {
    public static void main(String[] args) {
        SpringApplication.run(CorralonApplication.class, args);
    }
}
```

`src/main/java/imperio/corralon/Item.java`

```java
package imperio.corralon;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.ToString;

@Getter
@AllArgsConstructor
@ToString
public class Item {
    private final String material;
    private final int cantidad;
    private final double precioUnitario;

    public double subtotal() {
        return cantidad * precioUnitario;
    }
}
```

`src/main/java/imperio/corralon/Presupuesto.java`

```java
package imperio.corralon;

import java.util.List;

import lombok.Builder;
import lombok.Getter;
import lombok.Singular;
import lombok.ToString;

@Getter
@Builder
@ToString
public class Presupuesto {
    private final String cliente;
    @Singular
    private final List<Item> items;
    private final int descuento;

    public double total() {
        double bruto = items.stream().mapToDouble(Item::subtotal).sum();
        return Math.round(bruto * (100 - descuento)) / 100.0;
    }
}
```

`src/main/java/imperio/corralon/PresupuestoPedido.java`

```java
package imperio.corralon;

import java.util.List;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Positive;

public record PresupuestoPedido(
        @NotBlank(message = "el cliente es obligatorio") String cliente,
        @NotEmpty(message = "el presupuesto necesita al menos un ítem") List<@Valid ItemPedido> items,
        @Min(value = 0, message = "el descuento va de 0 a 30") @Max(value = 30, message = "el descuento va de 0 a 30") int descuento) {

    public record ItemPedido(
            @NotBlank(message = "falta el material") String material,
            @Positive(message = "la cantidad tiene que ser positiva") int cantidad,
            @Positive(message = "el precio tiene que ser positivo") double precioUnitario) {
    }
}
```

`src/main/java/imperio/corralon/PresupuestoRespuesta.java`

```java
package imperio.corralon;

public record PresupuestoRespuesta(String cliente, int items, int descuento, double total) {
    static PresupuestoRespuesta de(Presupuesto p) {
        return new PresupuestoRespuesta(p.getCliente(), p.getItems().size(), p.getDescuento(), p.total());
    }
}
```

`src/main/java/imperio/corralon/PresupuestoController.java`

```java
package imperio.corralon;

import java.util.Map;
import java.util.TreeMap;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/presupuestos")
public class PresupuestoController {
    @PostMapping
    public PresupuestoRespuesta armar(@Valid @RequestBody PresupuestoPedido pedido) {
        Presupuesto.PresupuestoBuilder b = Presupuesto.builder().cliente(pedido.cliente()).descuento(pedido.descuento());
        pedido.items().forEach(i -> b.item(new Item(i.material(), i.cantidad(), i.precioUnitario())));
        return PresupuestoRespuesta.de(b.build());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail invalido(MethodArgumentNotValidException e) {
        ProblemDetail p = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "datos inválidos");
        Map<String, String> campos = new TreeMap<>();
        e.getBindingResult().getFieldErrors().forEach(f -> campos.putIfAbsent(f.getField(), f.getDefaultMessage()));
        p.setProperty("campos", campos);
        return p;
    }
}
```

`src/test/java/imperio/corralon/PresupuestoTest.java`

```java
package imperio.corralon;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class PresupuestoTest {
    @Autowired
    private MockMvc mvc;

    @Test
    void elBuilderYElTotal() {
        Presupuesto p = Presupuesto.builder().cliente("Obra Ruiz").descuento(10)
                .item(new Item("cemento", 10, 9500)).item(new Item("arena m3", 2, 30000)).build();
        assertEquals(139500.0, p.total());
    }

    @Test
    void armaElPresupuesto() throws Exception {
        mvc.perform(post("/presupuestos").contentType(MediaType.APPLICATION_JSON).content("""
                        {"cliente": "Obra Ruiz", "descuento": 10, "items": [
                          {"material": "cemento", "cantidad": 10, "precioUnitario": 9500},
                          {"material": "arena m3", "cantidad": 2, "precioUnitario": 30000}]}
                        """))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.items").value(2))
                .andExpect(jsonPath("$.total").value(139500.0));
    }

    @Test
    void validaCadaItemYDiceCual() throws Exception {
        mvc.perform(post("/presupuestos").contentType(MediaType.APPLICATION_JSON).content("""
                        {"cliente": "", "descuento": 45, "items": [
                          {"material": "cemento", "cantidad": 10, "precioUnitario": 9500},
                          {"material": "", "cantidad": 0, "precioUnitario": 30000}]}
                        """))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.cliente").value("el cliente es obligatorio"))
                .andExpect(jsonPath("$.campos.descuento").value("el descuento va de 0 a 30"))
                .andExpect(jsonPath("$.campos['items[1].cantidad']").value("la cantidad tiene que ser positiva"))
                .andExpect(jsonPath("$.campos['items[1].material']").value("falta el material"));
    }

    @Test
    void sinItemsNoHayPresupuesto() throws Exception {
        mvc.perform(post("/presupuestos").contentType(MediaType.APPLICATION_JSON).content("""
                        {"cliente": "Obra Ruiz", "descuento": 0, "items": []}
                        """))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.items").value("el presupuesto necesita al menos un ítem"));
    }
}
```

### Misión R05-N05-M3 · Las reservas del hotel

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Hacé `POST /reservas` para un hotel con un DTO que tiene `huesped`, `habitacion` (1 a
20), `entrada` y `salida` (`LocalDate`) y `personas` (1 a 4). Además de las validaciones
de cada campo, hay reglas **entre campos**: la salida tiene que ser posterior a la
entrada y la estadía no puede pasar de 14 noches (usá métodos `@AssertTrue` en el
`record`). El servicio rechaza con 409 una reserva que se superpone con otra de la misma
habitación. La respuesta trae el id, las noches y el total (18 000 por noche por
persona, con 10 % de descuento desde 7 noches).

#### Criterio de aprobación

- Las reglas entre campos se validan con `@AssertTrue` y aparecen en los errores.
- La superposición se detecta en el servicio y responde 409.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>hotel</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/hotel/HotelApplication.java`

```java
package imperio.hotel;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class HotelApplication {
    public static void main(String[] args) {
        SpringApplication.run(HotelApplication.class, args);
    }
}
```

`src/main/java/imperio/hotel/ReservaPedido.java`

```java
package imperio.hotel;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.validation.constraints.AssertTrue;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record ReservaPedido(
        @NotBlank(message = "falta el huésped") String huesped,
        @Min(value = 1, message = "las habitaciones van del 1 al 20") @Max(value = 20, message = "las habitaciones van del 1 al 20") int habitacion,
        @NotNull(message = "falta la entrada") LocalDate entrada,
        @NotNull(message = "falta la salida") LocalDate salida,
        @Min(value = 1, message = "de 1 a 4 personas") @Max(value = 4, message = "de 1 a 4 personas") int personas) {

    @JsonIgnore
    @AssertTrue(message = "la salida tiene que ser posterior a la entrada")
    public boolean isFechasEnOrden() {
        return entrada == null || salida == null || salida.isAfter(entrada);
    }

    @JsonIgnore
    @AssertTrue(message = "la estadía máxima es de 14 noches")
    public boolean isEstadiaPermitida() {
        return entrada == null || salida == null || noches() <= 14;
    }

    public long noches() {
        return ChronoUnit.DAYS.between(entrada, salida);
    }
}
```

`src/main/java/imperio/hotel/Reserva.java`

```java
package imperio.hotel;

import java.time.LocalDate;

public record Reserva(long id, String huesped, int habitacion, LocalDate entrada, LocalDate salida, long noches, double total) {
    boolean seSuperponeCon(int otraHabitacion, LocalDate otraEntrada, LocalDate otraSalida) {
        return habitacion == otraHabitacion && otraEntrada.isBefore(salida) && entrada.isBefore(otraSalida);
    }
}
```

`src/main/java/imperio/hotel/Conflicto.java`

```java
package imperio.hotel;

public class Conflicto extends RuntimeException {
    public Conflicto(String mensaje) {
        super(mensaje);
    }
}
```

`src/main/java/imperio/hotel/ServicioReservas.java`

```java
package imperio.hotel;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

@Service
public class ServicioReservas {
    static final double POR_NOCHE_Y_PERSONA = 18000;

    private final List<Reserva> reservas = new ArrayList<>();

    public synchronized Reserva reservar(ReservaPedido p) {
        boolean ocupada = reservas.stream().anyMatch(r -> r.seSuperponeCon(p.habitacion(), p.entrada(), p.salida()));
        if (ocupada) {
            throw new Conflicto("la habitación " + p.habitacion() + " está ocupada en esas fechas");
        }
        long noches = p.noches();
        double total = noches * p.personas() * POR_NOCHE_Y_PERSONA * (noches >= 7 ? 0.9 : 1);
        Reserva r = new Reserva(reservas.size() + 1, p.huesped(), p.habitacion(), p.entrada(), p.salida(), noches, total);
        reservas.add(r);
        return r;
    }
}
```

`src/main/java/imperio/hotel/ReservaController.java`

```java
package imperio.hotel;

import java.util.Map;
import java.util.TreeMap;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/reservas")
public class ReservaController {
    private final ServicioReservas servicio;

    public ReservaController(ServicioReservas servicio) {
        this.servicio = servicio;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Reserva reservar(@Valid @RequestBody ReservaPedido pedido) {
        return servicio.reservar(pedido);
    }

    @ExceptionHandler(Conflicto.class)
    public ProblemDetail conflicto(Conflicto e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail invalido(MethodArgumentNotValidException e) {
        ProblemDetail p = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "datos inválidos");
        Map<String, String> campos = new TreeMap<>();
        e.getBindingResult().getFieldErrors().forEach(f -> campos.putIfAbsent(f.getField(), f.getDefaultMessage()));
        p.setProperty("campos", campos);
        return p;
    }
}
```

`src/test/java/imperio/hotel/ReservaControllerTest.java`

```java
package imperio.hotel;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class ReservaControllerTest {
    @Autowired
    private MockMvc mvc;

    private ResultActions reservar(int habitacion, String entrada, String salida, int personas) throws Exception {
        return mvc.perform(post("/reservas").contentType(MediaType.APPLICATION_JSON).content(
                "{\"huesped\": \"Ana\", \"habitacion\": " + habitacion + ", \"entrada\": \"" + entrada
                        + "\", \"salida\": \"" + salida + "\", \"personas\": " + personas + "}"));
    }

    @Test
    void calculaNochesYTotal() throws Exception {
        reservar(5, "2026-12-20", "2026-12-23", 2).andExpect(status().isCreated())
                .andExpect(jsonPath("$.noches").value(3))
                .andExpect(jsonPath("$.total").value(108000.0));
        reservar(6, "2027-01-02", "2027-01-09", 1).andExpect(jsonPath("$.total").value(113400.0));
    }

    @Test
    void lasReglasEntreCamposSeValidan() throws Exception {
        reservar(5, "2026-12-20", "2026-12-18", 2).andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.fechasEnOrden").value("la salida tiene que ser posterior a la entrada"));
        reservar(5, "2026-12-01", "2026-12-20", 2).andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.estadiaPermitida").value("la estadía máxima es de 14 noches"));
        reservar(25, "2026-12-01", "2026-12-02", 6).andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.habitacion").value("las habitaciones van del 1 al 20"))
                .andExpect(jsonPath("$.campos.personas").value("de 1 a 4 personas"));
    }

    @Test
    void laSuperposicionEs409() throws Exception {
        reservar(5, "2026-12-20", "2026-12-23", 2).andExpect(status().isCreated());
        reservar(5, "2026-12-22", "2026-12-25", 1).andExpect(status().isConflict())
                .andExpect(jsonPath("$.detail").value("la habitación 5 está ocupada en esas fechas"));
        reservar(5, "2026-12-23", "2026-12-25", 1).andExpect(status().isCreated());
        reservar(6, "2026-12-21", "2026-12-22", 1).andExpect(status().isCreated());
    }
}
```

### Encargo R05-N05-E1 · La mesa de ayuda

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Una mesa de ayuda recibe tickets. Hacé la API con DTO y validaciones:

- `POST /tickets` — `titulo` (5 a 80 caracteres), `descripcion` (obligatoria),
  `prioridad` (`BAJA`, `MEDIA` o `ALTA`, un `enum`: un valor inválido da 400) y `email` del
  solicitante. Se crea `ABIERTO`.
- `GET /tickets/{id}` — el ticket (sin el email del solicitante), o 404 con
  `ProblemDetail`.
- `POST /tickets/{id}/respuestas` — agrega una respuesta (`texto` obligatorio); 409 si el
  ticket está cerrado.
- `POST /tickets/{id}/cierre` — lo cierra; 409 si no tiene ninguna respuesta.

El modelo usa Lombok y los errores salen de un `@RestControllerAdvice`.

#### Criterio de aprobación

- DTO de entrada y de salida separados; el email no sale en las respuestas.
- Todos los errores (400, 404, 409) tienen formato `ProblemDetail`, incluido el de la prioridad inválida.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>ayuda</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                            <version>${lombok.version}</version>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/ayuda/AyudaApplication.java`

```java
package imperio.ayuda;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class AyudaApplication {
    public static void main(String[] args) {
        SpringApplication.run(AyudaApplication.class, args);
    }
}
```

`src/main/java/imperio/ayuda/Ticket.java`

```java
package imperio.ayuda;

import java.util.ArrayList;
import java.util.List;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;

@Getter
@RequiredArgsConstructor
public class Ticket {
    public enum Prioridad { BAJA, MEDIA, ALTA }

    public enum Estado { ABIERTO, CERRADO }

    private final long id;
    private final String titulo;
    private final String descripcion;
    private final Prioridad prioridad;
    private final String email;
    private final List<String> respuestas = new ArrayList<>();
    @Setter
    private Estado estado = Estado.ABIERTO;
}
```

`src/main/java/imperio/ayuda/TicketPedido.java`

```java
package imperio.ayuda;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record TicketPedido(
        @NotNull(message = "falta el título") @Size(min = 5, max = 80, message = "el título va de 5 a 80 caracteres") String titulo,
        @NotBlank(message = "falta la descripción") String descripcion,
        @NotNull(message = "falta la prioridad") Ticket.Prioridad prioridad,
        @NotBlank(message = "falta el email") @Email(message = "el email no es válido") String email) {
}
```

`src/main/java/imperio/ayuda/RespuestaPedido.java`

```java
package imperio.ayuda;

import jakarta.validation.constraints.NotBlank;

public record RespuestaPedido(@NotBlank(message = "la respuesta no puede estar vacía") String texto) {
}
```

`src/main/java/imperio/ayuda/TicketVista.java`

```java
package imperio.ayuda;

import java.util.List;

public record TicketVista(long id, String titulo, String descripcion, Ticket.Prioridad prioridad, Ticket.Estado estado, List<String> respuestas) {
    static TicketVista de(Ticket t) {
        return new TicketVista(t.getId(), t.getTitulo(), t.getDescripcion(), t.getPrioridad(), t.getEstado(), List.copyOf(t.getRespuestas()));
    }
}
```

`src/main/java/imperio/ayuda/Errores.java`

```java
package imperio.ayuda;

public final class Errores {
    private Errores() {
    }

    public static class NoEncontrado extends RuntimeException {
        public NoEncontrado(String mensaje) {
            super(mensaje);
        }
    }

    public static class Conflicto extends RuntimeException {
        public Conflicto(String mensaje) {
            super(mensaje);
        }
    }
}
```

`src/main/java/imperio/ayuda/ServicioTickets.java`

```java
package imperio.ayuda;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.stereotype.Service;

@Service
public class ServicioTickets {
    private final Map<Long, Ticket> tickets = new ConcurrentHashMap<>();
    private final AtomicLong proximoId = new AtomicLong(1);

    public Ticket abrir(TicketPedido p) {
        Ticket t = new Ticket(proximoId.getAndIncrement(), p.titulo(), p.descripcion(), p.prioridad(), p.email());
        tickets.put(t.getId(), t);
        return t;
    }

    public Ticket buscar(long id) {
        Ticket t = tickets.get(id);
        if (t == null) {
            throw new Errores.NoEncontrado("no existe el ticket " + id);
        }
        return t;
    }

    public synchronized Ticket responder(long id, String texto) {
        Ticket t = buscar(id);
        if (t.getEstado() == Ticket.Estado.CERRADO) {
            throw new Errores.Conflicto("el ticket " + id + " está cerrado");
        }
        t.getRespuestas().add(texto);
        return t;
    }

    public synchronized Ticket cerrar(long id) {
        Ticket t = buscar(id);
        if (t.getRespuestas().isEmpty()) {
            throw new Errores.Conflicto("no se cierra un ticket sin respuestas");
        }
        t.setEstado(Ticket.Estado.CERRADO);
        return t;
    }
}
```

`src/main/java/imperio/ayuda/TicketController.java`

```java
package imperio.ayuda;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/tickets")
@RequiredArgsConstructor
public class TicketController {
    private final ServicioTickets servicio;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public TicketVista abrir(@Valid @RequestBody TicketPedido pedido) {
        return TicketVista.de(servicio.abrir(pedido));
    }

    @GetMapping("/{id}")
    public TicketVista ver(@PathVariable long id) {
        return TicketVista.de(servicio.buscar(id));
    }

    @PostMapping("/{id}/respuestas")
    public TicketVista responder(@PathVariable long id, @Valid @RequestBody RespuestaPedido pedido) {
        return TicketVista.de(servicio.responder(id, pedido.texto()));
    }

    @PostMapping("/{id}/cierre")
    public TicketVista cerrar(@PathVariable long id) {
        return TicketVista.de(servicio.cerrar(id));
    }
}
```

`src/main/java/imperio/ayuda/ManejoDeErrores.java`

```java
package imperio.ayuda;

import java.util.Map;
import java.util.TreeMap;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ManejoDeErrores {
    @ExceptionHandler(Errores.NoEncontrado.class)
    public ProblemDetail noEncontrado(Errores.NoEncontrado e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
    }

    @ExceptionHandler(Errores.Conflicto.class)
    public ProblemDetail conflicto(Errores.Conflicto e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail invalido(MethodArgumentNotValidException e) {
        ProblemDetail p = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "datos inválidos");
        Map<String, String> campos = new TreeMap<>();
        e.getBindingResult().getFieldErrors().forEach(f -> campos.putIfAbsent(f.getField(), f.getDefaultMessage()));
        p.setProperty("campos", campos);
        return p;
    }

    // Un JSON que no se puede leer (por ejemplo, una prioridad que no está en el enum).
    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ProblemDetail ilegible(HttpMessageNotReadableException e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "el pedido tiene un valor que no se entiende");
    }
}
```

`src/test/java/imperio/ayuda/TicketControllerTest.java`

```java
package imperio.ayuda;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class TicketControllerTest {
    @Autowired
    private MockMvc mvc;

    private ResultActions enviar(String ruta, String json) throws Exception {
        return mvc.perform(post(ruta).contentType(MediaType.APPLICATION_JSON).content(json));
    }

    private static final String TICKET = """
            {"titulo": "No anda la impresora", "descripcion": "Sale la hoja en blanco", "prioridad": "ALTA", "email": "leo@oficina.com"}
            """;

    @Test
    void abreYNoMuestraElEmail() throws Exception {
        enviar("/tickets", TICKET).andExpect(status().isCreated())
                .andExpect(jsonPath("$.estado").value("ABIERTO"))
                .andExpect(jsonPath("$.email").doesNotExist());
        mvc.perform(get("/tickets/1")).andExpect(jsonPath("$.prioridad").value("ALTA"));
        mvc.perform(get("/tickets/5")).andExpect(status().isNotFound()).andExpect(jsonPath("$.detail").value("no existe el ticket 5"));
    }

    @Test
    void validaYRechazaUnaPrioridadInexistente() throws Exception {
        enviar("/tickets", """
                {"titulo": "Uy", "descripcion": "", "prioridad": "BAJA", "email": "leo"}
                """).andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.titulo").value("el título va de 5 a 80 caracteres"))
                .andExpect(jsonPath("$.campos.descripcion").value("falta la descripción"))
                .andExpect(jsonPath("$.campos.email").value("el email no es válido"));
        enviar("/tickets", TICKET.replace("ALTA", "URGENTE")).andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.detail").value("el pedido tiene un valor que no se entiende"));
    }

    @Test
    void responderYCerrarConSusReglas() throws Exception {
        enviar("/tickets", TICKET);
        mvc.perform(post("/tickets/1/cierre")).andExpect(status().isConflict())
                .andExpect(jsonPath("$.detail").value("no se cierra un ticket sin respuestas"));
        enviar("/tickets/1/respuestas", "{\"texto\": \" \"}").andExpect(status().isBadRequest());
        enviar("/tickets/1/respuestas", "{\"texto\": \"Cambiamos el tóner\"}")
                .andExpect(jsonPath("$.respuestas[0]").value("Cambiamos el tóner"));
        mvc.perform(post("/tickets/1/cierre")).andExpect(jsonPath("$.estado").value("CERRADO"));
        enviar("/tickets/1/respuestas", "{\"texto\": \"¿Anduvo?\"}").andExpect(status().isConflict());
    }
}
```

### Prueba del sello

#### ¿Qué es un DTO y para qué sirve?

Un objeto pensado solo para entrar o salir por la API; separa lo que viaja del modelo interno y evita exponer datos privados.

#### ¿Qué hace `@Valid` en un parámetro del controlador?

Hace cumplir las validaciones del DTO; si alguna falla, Spring no llama al método y responde 400.

#### ¿Cómo validás una regla que involucra dos campos?

Con un método `boolean` anotado con `@AssertTrue` en el DTO (o con una validación propia).

#### ¿Qué ventaja tiene un `@RestControllerAdvice`?

Centraliza el manejo de errores de todos los controladores: el servicio lanza excepciones y el *advice* decide el código y el formato.

#### ¿Qué genera `@RequiredArgsConstructor` de Lombok?

Un constructor con todos los atributos `final`, ideal para la inyección de dependencias.

### Soluciones (docente)

Nodo nuevo de la Senda (`19-Java-Avanzado` no tiene validaciones ni Lombok). Los `pom.xml` con Lombok declaran el procesador de anotaciones para que compilen también con Java 23 o más nuevo.

## R05-N06 · Jefe final: el Dragón del Imperio

```meta
tipo: jefe
padre: R05-N05
precio: 10
criatura: dragon
ejecutable: no
insignia: Sello del Arquitecto
insignia_descripcion: Venciste al Dragón del Imperio: construiste un servicio en capas con Spring Boot, como el del examen final.
usa: fw.spring, diseno.capas, diseno.patrones, col.mapas, col.conjuntos
```

### Crónica

En la cima de la Torre del Arquitecto, enroscado alrededor de la ventana más alta, duerme el **Dragón del Imperio**: está hecho de todas las piezas que Zed fue juntando desde la Aduana. Sobre la mesa del Tribunal hay un solo pliego, lacrado: **AduanaExpress**. Es el examen que el Imperio le toma a cada arquitecto antes de darle su sello, y se resuelve en tres horas.

—No hay truco nuevo —dice {mentor}, y por primera vez deja la taza de café a un costado—. Leé todo el pliego antes de escribir una línea. Armá las capas, poné cada regla donde va, probá cada pieza y dejá las evidencias. Pieza por pieza, Zed. Así cae un dragón. Nadia, en la puerta, cruza los dedos sin que nadie la vea.

### Objetivos

- Resolver en unas tres horas (180 minutos) un caso completo con el formato del examen final de la cátedra.
- Organizar un servicio Spring Boot en capas: controller, service, repository, model y dto.
- Combinar herencia, Strategy, `HashMap`, `HashSet`, validaciones, Lombok y manejo de errores.
- Entregar como en el examen: GitHub con commits, colección de Postman y `EVIDENCIAS.md`.

### Antes de empezar

- Toda la Torre: Big O, SOLID, el contenedor de Spring, REST y DTO con validaciones y Lombok.
- Patrones de diseño (rama 4) y colecciones (rama 3).

### Explicación

#### Cómo se enfrenta el examen
El simulacro está pensado para **180 minutos**. Una forma de repartirlos:
1. **Leé todo el pliego** (10 minutos) y subrayá los números: porcentajes, días, códigos de estado.
2. **Creá el proyecto** (10 minutos) con Spring Initializr (Web, Validation, Lombok) y hacé el primer commit.
3. **Modelo primero** (30 minutos): las clases abstractas y sus tipos. Commit.
4. **Strategy y repositorio** (30 minutos): la interfaz, las estrategias como `@Component` y el `HashMap`. Commit.
5. **Servicio y DTO** (40 minutos): las reglas van en el servicio; el controlador solo traduce. Commit.
6. **Controlador y errores** (30 minutos): las rutas y el `@RestControllerAdvice`. Commit.
7. **Postman y evidencias** (30 minutos): un pedido por ruta, incluidos los de error, y las capturas.
Si algo no sale, **dejalo andando a medias y seguí**: se corrige por partes. Y si te pasás de las tres horas, **terminalo igual**: en el simulacro no se descuentan puntos por el tiempo. Anotá en el `README.md` cuánto tardaste, así sabés cuánto te falta para el examen.

#### La forma del proyecto
```
imperio.aduana
├── controller   AduanaController         ← traduce HTTP ↔ DTO, nada de reglas
├── service      AduanaServicio           ← las reglas: liquidar, depurar, activar la estrategia
├── repository   MercanciaRepositorio     ← HashMap en memoria
├── model        Mercancia, Caja, Barril, Viajero, Mercader, Peregrino
├── dto          …Pedido y …Respuesta (record con validaciones)
├── strategy     RecargoStrategy y sus tres implementaciones
└── exception    ManejadorErrores y las excepciones propias
```

#### Elegir la estrategia por nombre
Si cada estrategia es un `@Component` con nombre, Spring las junta solo en un mapa, y el servicio
elige la activa sin `if` ni `switch`:
```java
@Component("feria")
public class RecargoFeria implements RecargoStrategy { … }

@Service
@RequiredArgsConstructor
public class AduanaServicio {
    private final Map<String, RecargoStrategy> estrategias;   // "normal", "feria", "nocturno"
    private String estrategiaActiva = "normal";
}
```

#### Las evidencias
El `EVIDENCIAS.md` tiene una sección por pedido: qué se mandó, qué respondió (código y cuerpo) y la
captura de Postman. Exportá la colección (*Export → Collection v2.1*) y subila al repositorio. Los
commits tienen que mostrar el avance: uno solo al final se nota.

### Código de ejemplo

El esqueleto de la Strategy elegida por nombre, que se usa en el examen:

```java
public interface RecargoStrategy {
    double calcular(int dias, double valor);
}

@Component("normal")
public class RecargoNormal implements RecargoStrategy {
    @Override
    public double calcular(int dias, double valor) {
        return valor * 0.02 * dias;
    }
}

@Service
@RequiredArgsConstructor
public class AduanaServicio {
    private final Map<String, RecargoStrategy> estrategias;
    private String estrategiaActiva = "normal";

    public void activar(String nombre) {
        if (!estrategias.containsKey(nombre)) {
            throw new IllegalArgumentException("Estrategia desconocida: " + nombre);
        }
        estrategiaActiva = nombre;
    }

    public double recargo(int dias, double valor, Viajero viajero) {
        return estrategias.get(estrategiaActiva).calcular(dias, valor) * viajero.factorRecargo();
    }
}
```

### ¿Para qué sirve?

Es el ensayo general del examen final de *Paradigmas y Lenguajes III*: el mismo formato y las mismas piezas (capas, herencia, Strategy, `HashMap`, `HashSet`, validaciones, Lombok, GitHub y Postman). Y es la forma en que se arma un servicio web en cualquier empresa que use Java.

### Errores habituales

**Dragón: empezar por el controlador.** Sin modelo ni servicio, el controlador se llena de reglas
y después no hay tiempo de ordenarlo. Modelo, servicio y recién después la API.

**Ogro: devolver el modelo.** Si la respuesta es la entidad, se filtran datos y cualquier cambio
interno rompe a los clientes: siempre un DTO.

**Goblin: la estrategia con `switch`.** Un `switch (estrategiaActiva)` en el servicio no es una
Strategy: cada cálculo va en su clase.

**Troll: el `null` de un `get`.** `mapa.get(codigo)` puede dar `null`: convertilo en un 404 con
una excepción propia.

**Slime: un solo commit al final.** El historial de GitHub es parte de la nota.

### Micro-misión R05-N06-P1 · Primera pieza: el modelo

```meta
lugar: La cima de la Torre
personajes: Zed, Gheco, Nadia, Kaffa, el Dragón del Imperio
criatura: dragon
carta: El modelo del examen | Mercancia abstracta · Caja y Barril calculan su impuesto · nada de instanceof para calcular
recompensa: xp 20, oro 20
```

#### Escena
El **Dragón del Imperio** despierta enroscado en la ventana más alta, hecho de todas las piezas que Zed juntó desde la Aduana. El pliego dice **AduanaExpress**. —Pieza por pieza —dice Kaffa—. Primero, el **modelo**: cada mercancía sabe cuánto paga.

#### Gheco sugiere
`Mercancia` es abstracta y cada tipo escribe su `impuesto()`: la `Caja`, el 10 % del valor; el `Barril`, el 10 % más 0,5 por litro. Así el total se calcula con una sola línea, sin preguntar qué es cada una.

#### Desafío
Completá el impuesto del barril: el 10 % del valor más 0,5 por litro.

#### Código inicial
```java
import java.util.List;

public class Dragon1 {
    public static void main(String[] args) {
        List<Mercancia> carga = List.of(new Caja("C1", 1000), new Barril("B1", 500, 40));
        double total = 0;
        for (Mercancia m : carga) {
            System.out.println(m.codigo + ": " + m.impuesto());
            total += m.impuesto();
        }
        System.out.println("Impuestos: " + total);
    }
}

abstract class Mercancia {
    final String codigo;
    final double valor;

    Mercancia(String codigo, double valor) {
        this.codigo = codigo;
        this.valor = valor;
    }

    abstract double impuesto();
}

class Caja extends Mercancia {
    Caja(String codigo, double valor) { super(codigo, valor); }

    double impuesto() { return valor * 0.10; }
}

class Barril extends Mercancia {
    final int litros;

    Barril(String codigo, double valor, int litros) {
        super(codigo, valor);
        this.litros = litros;
    }

    double impuesto() { return ___; }
}
```

#### Salida esperada
```
C1: 100.0
B1: 70.0
Impuestos: 170.0
```

#### Solución
```java
import java.util.List;

public class Dragon1 {
    public static void main(String[] args) {
        List<Mercancia> carga = List.of(new Caja("C1", 1000), new Barril("B1", 500, 40));
        double total = 0;
        for (Mercancia m : carga) {
            System.out.println(m.codigo + ": " + m.impuesto());
            total += m.impuesto();
        }
        System.out.println("Impuestos: " + total);
    }
}

abstract class Mercancia {
    final String codigo;
    final double valor;

    Mercancia(String codigo, double valor) {
        this.codigo = codigo;
        this.valor = valor;
    }

    abstract double impuesto();
}

class Caja extends Mercancia {
    Caja(String codigo, double valor) { super(codigo, valor); }

    double impuesto() { return valor * 0.10; }
}

class Barril extends Mercancia {
    final int litros;

    Barril(String codigo, double valor, int litros) {
        super(codigo, valor);
        this.litros = litros;
    }

    double impuesto() { return valor * 0.10 + litros * 0.5; }
}
```

#### Al superarla
Ciento setenta denarios de impuestos, sin un `if`. Una escama del Dragón se apaga: la pieza de la Academia está en su lugar.

#### Imagen
- El Dragón del Imperio: un dragón de bronce y vitrales hecho de piezas (moldes, campanas, corrientes), enroscado en la ventana más alta de la Torre.
- Zed frente a él con el pliego «AduanaExpress»; Nadia y Gheco atrás; Kaffa sin su taza.

### Micro-misión R05-N06-P2 · Segunda pieza: la estrategia activa

```meta
lugar: La cima de la Torre
personajes: Zed, Gheco, Nadia, Kaffa, el Dragón del Imperio
carta: Strategy por nombre | un mapa nombre → estrategia · la activa se cambia en tiempo de ejecución · en Spring, los @Component por nombre
recompensa: xp 20, oro 20
```

#### Escena
El Dragón cambia de humor y, con él, el recargo por demora: normal, feria o nocturno. —Como en el astillero —dice Gheco—, pero eligiéndola por **nombre**, como hace Spring.

#### Gheco sugiere
Las estrategias se guardan en un mapa por nombre. La activa es solo un nombre: `estrategias.get(activa).calcular(dias, valor)`. Cambiarla es cambiar ese nombre.

#### Desafío
Completá el cálculo con la estrategia activa del mapa.

#### Código inicial
```java
import java.util.LinkedHashMap;
import java.util.Map;

public class Dragon2 {
    interface Recargo {
        double calcular(int dias, double valor);
    }

    static final Map<String, Recargo> ESTRATEGIAS = new LinkedHashMap<>();
    static String activa = "normal";

    static {
        ESTRATEGIAS.put("normal", (dias, valor) -> valor * 0.02 * dias);
        ESTRATEGIAS.put("feria", (dias, valor) -> dias <= 3 ? 0 : valor * 0.01 * (dias - 3));
        ESTRATEGIAS.put("nocturno", (dias, valor) -> dias == 0 ? 0 : valor * 0.05 + valor * 0.03 * dias);
    }

    static double recargo(int dias, double valor) {
        return ___;
    }

    public static void main(String[] args) {
        for (String nombre : ESTRATEGIAS.keySet()) {
            activa = nombre;
            System.out.println(nombre + ", 5 días sobre 1500: " + recargo(5, 1500));
        }
    }
}
```

#### Salida esperada
```
normal, 5 días sobre 1500: 150.0
feria, 5 días sobre 1500: 30.0
nocturno, 5 días sobre 1500: 300.0
```

#### Solución
```java
import java.util.LinkedHashMap;
import java.util.Map;

public class Dragon2 {
    interface Recargo {
        double calcular(int dias, double valor);
    }

    static final Map<String, Recargo> ESTRATEGIAS = new LinkedHashMap<>();
    static String activa = "normal";

    static {
        ESTRATEGIAS.put("normal", (dias, valor) -> valor * 0.02 * dias);
        ESTRATEGIAS.put("feria", (dias, valor) -> dias <= 3 ? 0 : valor * 0.01 * (dias - 3));
        ESTRATEGIAS.put("nocturno", (dias, valor) -> dias == 0 ? 0 : valor * 0.05 + valor * 0.03 * dias);
    }

    static double recargo(int dias, double valor) {
        return ESTRATEGIAS.get(activa).calcular(dias, valor);
    }

    public static void main(String[] args) {
        for (String nombre : ESTRATEGIAS.keySet()) {
            activa = nombre;
            System.out.println(nombre + ", 5 días sobre 1500: " + recargo(5, 1500));
        }
    }
}
```

#### Al superarla
Tres humores, un solo cálculo. Otra escama se apaga: la del astillero.

#### Imagen
- Tres esferas de colores (normal, feria, nocturno) orbitando alrededor de Zed; una se enciende.
- El Dragón con una escama apagándose.

### Micro-misión R05-N06-P3 · Tercera pieza: el peregrino y los pasaportes

```meta
lugar: La cima de la Torre
personajes: Zed, Gheco, Nadia, Kaffa, el Dragón del Imperio
carta: Herencia y una pasada | Peregrino paga la mitad del recargo (factorRecargo) · los pasaportes repetidos, en una pasada con HashSet
recompensa: xp 20, oro 25
```

#### Escena
El Dragón escupe dos preguntas a la vez: cuánto recargo paga un **peregrino**, y cuáles de los pasaportes del día están **repetidos**. Las dos, sin perder tiempo.

#### Gheco sugiere
Cada viajero dice qué parte del recargo paga: el mercader, `1.0`; el peregrino, `0.5`. Para los pasaportes, un `LinkedHashSet` de vistos y otro de duplicados, en una sola pasada.

#### Desafío
Completá el factor del peregrino: paga la mitad.

#### Código inicial
```java
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public class Dragon3 {
    public static void main(String[] args) {
        double recargo = 30;
        Viajero[] viajeros = {new Mercader("Baldo"), new Peregrino("Sor Ana")};
        for (Viajero v : viajeros) {
            System.out.println(v.nombre + " paga de recargo " + recargo * v.factorRecargo());
        }

        List<String> pasaportes = List.of("AR-101", "UY-202", "AR-101", "CL-303", "UY-202", "AR-101");
        Set<String> vistos = new LinkedHashSet<>();
        Set<String> duplicados = new LinkedHashSet<>();
        for (String p : pasaportes) {
            if (!vistos.add(p)) {
                duplicados.add(p);
            }
        }
        System.out.println("Únicos: " + vistos);
        System.out.println("Duplicados: " + duplicados);
    }
}

abstract class Viajero {
    final String nombre;

    Viajero(String nombre) { this.nombre = nombre; }

    abstract double factorRecargo();
}

class Mercader extends Viajero {
    Mercader(String nombre) { super(nombre); }

    double factorRecargo() { return 1.0; }
}

class Peregrino extends Viajero {
    Peregrino(String nombre) { super(nombre); }

    double factorRecargo() { return ___; }
}
```

#### Salida esperada
```
Baldo paga de recargo 30.0
Sor Ana paga de recargo 15.0
Únicos: [AR-101, UY-202, CL-303]
Duplicados: [AR-101, UY-202]
```

#### Solución
```java
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public class Dragon3 {
    public static void main(String[] args) {
        double recargo = 30;
        Viajero[] viajeros = {new Mercader("Baldo"), new Peregrino("Sor Ana")};
        for (Viajero v : viajeros) {
            System.out.println(v.nombre + " paga de recargo " + recargo * v.factorRecargo());
        }

        List<String> pasaportes = List.of("AR-101", "UY-202", "AR-101", "CL-303", "UY-202", "AR-101");
        Set<String> vistos = new LinkedHashSet<>();
        Set<String> duplicados = new LinkedHashSet<>();
        for (String p : pasaportes) {
            if (!vistos.add(p)) {
                duplicados.add(p);
            }
        }
        System.out.println("Únicos: " + vistos);
        System.out.println("Duplicados: " + duplicados);
    }
}

abstract class Viajero {
    final String nombre;

    Viajero(String nombre) { this.nombre = nombre; }

    abstract double factorRecargo();
}

class Mercader extends Viajero {
    Mercader(String nombre) { super(nombre); }

    double factorRecargo() { return 1.0; }
}

class Peregrino extends Viajero {
    Peregrino(String nombre) { super(nombre); }

    double factorRecargo() { return 0.5; }
}
```

#### Al superarla
Quince para la peregrina, treinta para Baldo, y los repetidos en una pasada. Al Dragón le quedan pocas escamas encendidas.

#### Imagen
- Sor Ana, una peregrina de capa clara, y Baldo con su sobretodo, frente a una balanza de recargos.
- Una fila de pasaportes donde tres se iluminan en rojo; el Dragón con casi todas las escamas apagadas.

### Micro-misión R05-N06-P4 · La declaración completa

```meta
lugar: La cima de la Torre
personajes: Zed, Gheco, Nadia, Kaffa, el Dragón del Imperio
carta: El servicio del examen | busca en el HashMap, suma impuestos, aplica la estrategia activa y el factor del viajero, responde un DTO · el controlador solo lo llama
recompensa: xp 25, oro 40
item: Llave Maestra
```

#### Escena
La última pregunta del Dragón es la declaración completa: Baldo trae una caja y un barril, se demoró 5 días, y la estrategia activa es la normal. —Juntá todo en el **servicio** —dice Kaffa—, y que responda un DTO. Como en el examen.

#### Gheco sugiere
El servicio busca cada mercancía en el `HashMap` por código, suma valores e impuestos, calcula el recargo con la estrategia activa por el factor del viajero y arma la respuesta. El total es impuestos más recargo.

#### Desafío
Completá el total de la declaración.

#### Código inicial
```java
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Dragon4 {
    record Mercancia(String codigo, double valor, double impuesto) { }

    record DeclaracionRespuesta(String viajero, double impuestos, double recargo, double total) { }

    static final Map<String, Mercancia> DEPOSITO = new HashMap<>();

    static DeclaracionRespuesta declarar(String viajero, double factor, List<String> codigos, int dias) {
        double valor = 0;
        double impuestos = 0;
        for (String c : codigos) {
            Mercancia m = DEPOSITO.get(c);
            valor += m.valor();
            impuestos += m.impuesto();
        }
        double recargo = valor * 0.02 * dias * factor;
        double total = ___;
        return new DeclaracionRespuesta(viajero, impuestos, recargo, total);
    }

    public static void main(String[] args) {
        DEPOSITO.put("C1", new Mercancia("C1", 1000, 100));
        DEPOSITO.put("B1", new Mercancia("B1", 500, 70));
        System.out.println(declarar("Baldo", 1.0, List.of("C1", "B1"), 5));
        System.out.println(declarar("Sor Ana", 0.5, List.of("C1", "B1"), 5));
    }
}
```

#### Salida esperada
```
DeclaracionRespuesta[viajero=Baldo, impuestos=170.0, recargo=150.0, total=320.0]
DeclaracionRespuesta[viajero=Sor Ana, impuestos=170.0, recargo=75.0, total=245.0]
```

#### Solución
```java
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Dragon4 {
    record Mercancia(String codigo, double valor, double impuesto) { }

    record DeclaracionRespuesta(String viajero, double impuestos, double recargo, double total) { }

    static final Map<String, Mercancia> DEPOSITO = new HashMap<>();

    static DeclaracionRespuesta declarar(String viajero, double factor, List<String> codigos, int dias) {
        double valor = 0;
        double impuestos = 0;
        for (String c : codigos) {
            Mercancia m = DEPOSITO.get(c);
            valor += m.valor();
            impuestos += m.impuesto();
        }
        double recargo = valor * 0.02 * dias * factor;
        double total = impuestos + recargo;
        return new DeclaracionRespuesta(viajero, impuestos, recargo, total);
    }

    public static void main(String[] args) {
        DEPOSITO.put("C1", new Mercancia("C1", 1000, 100));
        DEPOSITO.put("B1", new Mercancia("B1", 500, 70));
        System.out.println(declarar("Baldo", 1.0, List.of("C1", "B1"), 5));
        System.out.println(declarar("Sor Ana", 0.5, List.of("C1", "B1"), 5));
    }
}
```

#### Al superarla
Trescientos veinte para Baldo, doscientos cuarenta y cinco para la peregrina. La última escama se apaga y el **Dragón del Imperio** se deshace en piezas que vuelven, una por una, a su lugar en la Torre.
En la mano de Zed, la ganzúa termina de transformarse: ya no es una ganzúa, es la **Llave Maestra**. Kaffa le estampa el sello de arquitecto en el pliego. Nadia, en la puerta, aplaude. Una sola vez, pero aplaude.
Detrás del Dragón, la ventana más alta tiene un marco vacío, esperando un vidrio.

#### Imagen
- El Dragón del Imperio deshaciéndose en piezas luminosas que vuelan a su lugar en la Torre.
- La ganzúa de Zed transformándose en una llave maestra dorada con dientes de engranaje.
- Kaffa estampando un sello en el pliego; Nadia aplaudiendo en la puerta; al fondo, una ventana con el marco vacío.

### Misión R05-N06-M1 · El pliego del Tribunal: AduanaExpress

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 30
```

#### Consigna

**Simulacro del examen final · 180 minutos · AduanaExpress.** Leé todo antes de empezar. Si te pasás del tiempo, terminalo igual: no se descuentan puntos; anotá en el `README.md` cuánto tardaste.

La Aduana del Imperio quiere un servicio web para registrar mercancías, liquidar declaraciones y
depurar pasaportes. Hacelo con **Java 17 o 21, Spring Boot 3, Maven y Lombok**, con los datos
**en memoria** (sin base de datos) y las capas **controller – service – repository – model – dto**.

**1. Modelo (20 puntos).** Una `Mercancia` abstracta (`codigo`, `descripcion`, `valorDeclarado`)
con dos tipos que calculan su impuesto: `Caja` (10 % del valor) y `Barril` (10 % del valor más
0,5 por litro). Un `Viajero` abstracto (`nombre`, `pasaporte`) con `Mercader` (paga el recargo
entero) y `Peregrino` (paga la **mitad** del recargo). Usá Lombok para los getters y constructores.

**2. Recargo por demora con Strategy (20 puntos).** Una interfaz `RecargoStrategy` con
`double calcular(int dias, double valor)` y tres estrategias: **normal** (2 % del valor por día),
**feria** (los primeros 3 días gratis, después 1 % por día) y **nocturno** (si hay demora, 5 %
fijo más 3 % por día). Hay una estrategia **activa** (al empezar, normal) que se cambia en
tiempo de ejecución.

**3. Colecciones (15 puntos).** El repositorio guarda las mercancías en un **`HashMap`** por
código. La depuración de pasaportes encuentra los duplicados **en una sola pasada** con un
**`HashSet`**, conservando el orden de llegada.

**4. API REST (25 puntos).**

| Método | Ruta | Hace |
|---|---|---|
| POST | `/api/mercancias` | registra (`tipo` CAJA o BARRIL); 201, o 409 si el código ya existe |
| GET | `/api/mercancias` | lista, ordenada por código |
| GET | `/api/mercancias/{codigo}` | una mercancía con su impuesto; 404 si no existe |
| GET | `/api/recargo` | la estrategia activa |
| PUT | `/api/recargo/{nombre}` | activa otra; 400 si no existe |
| POST | `/api/declaraciones` | liquida: impuestos + recargo (por el valor total y el tipo de viajero) |
| POST | `/api/pasaportes/depurar` | recibe una lista y devuelve `unicos` y `duplicados` |

Lo que entra y sale son **DTO** (nunca el modelo), redondeados a dos decimales.

**5. Validaciones y errores (10 puntos).** `@Valid` con Bean Validation: textos no vacíos, valor
positivo, litros y días no negativos, al menos un código, tipos válidos. Los errores salen como
`ProblemDetail` desde un `@RestControllerAdvice`: 400 con los campos inválidos, 404 y 409.

**6. Entrega y evidencias (10 puntos).** Un repositorio en **GitHub** con commits a medida que
avanzás, un `README.md` (cómo se ejecuta), la **colección de Postman** exportada y un
`EVIDENCIAS.md` con una captura de cada pedido de la tabla (incluidos los de error). Entregá
acá un `.zip` del proyecto (sin `target/`) con el enlace al repositorio en el `README.md`.

#### Criterio de aprobación

- **Modelo (20):** herencia con clases abstractas y el cálculo en cada subtipo, sin `instanceof` ni `switch` sobre el tipo fuera de la creación.
- **Strategy (20):** una clase por estrategia y el servicio delega en la activa; cambiarla no toca el cálculo.
- **Colecciones (15):** `HashMap` por código y depuración en una pasada con `HashSet`.
- **API (25):** las 7 rutas con sus códigos de estado; DTO en la entrada y la salida.
- **Validaciones y errores (10):** `@Valid` y `ProblemDetail` con 400, 404 y 409.
- **Entrega (10):** GitHub con commits, README, colección de Postman y `EVIDENCIAS.md`.
- Se aprueba con 60 puntos. Un proyecto que no compila no se corrige.
- El tiempo no resta puntos: si se pasó de los 180 minutos, se corrige igual (el `README.md` dice cuánto tardó).

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>aduana-express</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                            <version>${lombok.version}</version>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/aduana/AduanaExpressApplication.java`

```java
package imperio.aduana;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class AduanaExpressApplication {
    public static void main(String[] args) {
        SpringApplication.run(AduanaExpressApplication.class, args);
    }
}
```

`src/main/java/imperio/aduana/model/Mercancia.java`

```java
package imperio.aduana.model;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

/** Lo común de toda mercancía. Cada tipo calcula su impuesto. */
@Getter
@RequiredArgsConstructor
public abstract class Mercancia {
    private final String codigo;
    private final String descripcion;
    private final double valorDeclarado;

    public abstract String getTipo();

    public abstract double impuesto();
}
```

`src/main/java/imperio/aduana/model/Caja.java`

```java
package imperio.aduana.model;

/** Una caja paga el 10 % de su valor. */
public class Caja extends Mercancia {
    public Caja(String codigo, String descripcion, double valorDeclarado) {
        super(codigo, descripcion, valorDeclarado);
    }

    @Override
    public String getTipo() {
        return "CAJA";
    }

    @Override
    public double impuesto() {
        return getValorDeclarado() * 0.10;
    }
}
```

`src/main/java/imperio/aduana/model/Barril.java`

```java
package imperio.aduana.model;

import lombok.Getter;

/** Un barril paga el 10 % de su valor más medio denario por litro. */
@Getter
public class Barril extends Mercancia {
    private final int litros;

    public Barril(String codigo, String descripcion, double valorDeclarado, int litros) {
        super(codigo, descripcion, valorDeclarado);
        this.litros = litros;
    }

    @Override
    public String getTipo() {
        return "BARRIL";
    }

    @Override
    public double impuesto() {
        return getValorDeclarado() * 0.10 + litros * 0.5;
    }
}
```

`src/main/java/imperio/aduana/model/Viajero.java`

```java
package imperio.aduana.model;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

/** Quien declara. Cada tipo de viajero paga una parte distinta del recargo. */
@Getter
@RequiredArgsConstructor
public abstract class Viajero {
    private final String nombre;
    private final String pasaporte;

    public abstract double factorRecargo();
}
```

`src/main/java/imperio/aduana/model/Mercader.java`

```java
package imperio.aduana.model;

public class Mercader extends Viajero {
    public Mercader(String nombre, String pasaporte) {
        super(nombre, pasaporte);
    }

    @Override
    public double factorRecargo() {
        return 1.0;
    }
}
```

`src/main/java/imperio/aduana/model/Peregrino.java`

```java
package imperio.aduana.model;

/** Los peregrinos pagan la mitad de los recargos. */
public class Peregrino extends Viajero {
    public Peregrino(String nombre, String pasaporte) {
        super(nombre, pasaporte);
    }

    @Override
    public double factorRecargo() {
        return 0.5;
    }
}
```

`src/main/java/imperio/aduana/strategy/RecargoStrategy.java`

```java
package imperio.aduana.strategy;

/** Cómo se calcula el recargo por demora (Strategy). */
public interface RecargoStrategy {
    double calcular(int dias, double valor);
}
```

`src/main/java/imperio/aduana/strategy/RecargoNormal.java`

```java
package imperio.aduana.strategy;

import org.springframework.stereotype.Component;

/** 2 % del valor por cada día de demora. */
@Component("normal")
public class RecargoNormal implements RecargoStrategy {
    @Override
    public double calcular(int dias, double valor) {
        return valor * 0.02 * dias;
    }
}
```

`src/main/java/imperio/aduana/strategy/RecargoFeria.java`

```java
package imperio.aduana.strategy;

import org.springframework.stereotype.Component;

/** En feria, los primeros 3 días no pagan; después, 1 % por día. */
@Component("feria")
public class RecargoFeria implements RecargoStrategy {
    @Override
    public double calcular(int dias, double valor) {
        return dias <= 3 ? 0 : valor * 0.01 * (dias - 3);
    }
}
```

`src/main/java/imperio/aduana/strategy/RecargoNocturno.java`

```java
package imperio.aduana.strategy;

import org.springframework.stereotype.Component;

/** De noche: si hay demora, 5 % fijo más 3 % por día. */
@Component("nocturno")
public class RecargoNocturno implements RecargoStrategy {
    @Override
    public double calcular(int dias, double valor) {
        return dias == 0 ? 0 : valor * 0.05 + valor * 0.03 * dias;
    }
}
```

`src/main/java/imperio/aduana/dto/MercanciaPedido.java`

```java
package imperio.aduana.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.PositiveOrZero;

public record MercanciaPedido(
        @NotBlank @Pattern(regexp = "CAJA|BARRIL", message = "debe ser CAJA o BARRIL") String tipo,
        @NotBlank String codigo,
        @NotBlank String descripcion,
        @Positive double valorDeclarado,
        @PositiveOrZero int litros) {
}
```

`src/main/java/imperio/aduana/dto/MercanciaRespuesta.java`

```java
package imperio.aduana.dto;

import imperio.aduana.model.Mercancia;

public record MercanciaRespuesta(String codigo, String tipo, String descripcion, double valorDeclarado, double impuesto) {
    public static MercanciaRespuesta de(Mercancia m) {
        return new MercanciaRespuesta(m.getCodigo(), m.getTipo(), m.getDescripcion(), m.getValorDeclarado(), m.impuesto());
    }
}
```

`src/main/java/imperio/aduana/dto/DeclaracionPedido.java`

```java
package imperio.aduana.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.PositiveOrZero;
import java.util.List;

public record DeclaracionPedido(
        @NotBlank String viajero,
        @NotBlank String pasaporte,
        @NotBlank @Pattern(regexp = "MERCADER|PEREGRINO", message = "debe ser MERCADER o PEREGRINO") String tipoViajero,
        @NotEmpty List<@NotBlank String> codigos,
        @PositiveOrZero int diasDemora) {
}
```

`src/main/java/imperio/aduana/dto/DeclaracionRespuesta.java`

```java
package imperio.aduana.dto;

public record DeclaracionRespuesta(String viajero, int mercancias, double impuestos, double recargo, double total, String estrategia) {
}
```

`src/main/java/imperio/aduana/dto/DepuracionRespuesta.java`

```java
package imperio.aduana.dto;

import java.util.Set;

public record DepuracionRespuesta(Set<String> unicos, Set<String> duplicados) {
}
```

`src/main/java/imperio/aduana/repository/MercanciaRepositorio.java`

```java
package imperio.aduana.repository;

import imperio.aduana.model.Mercancia;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.springframework.stereotype.Repository;

/** En memoria: un HashMap por código (buscar es O(1)). */
@Repository
public class MercanciaRepositorio {
    private final Map<String, Mercancia> porCodigo = new HashMap<>();

    public boolean existe(String codigo) {
        return porCodigo.containsKey(codigo);
    }

    public void guardar(Mercancia m) {
        porCodigo.put(m.getCodigo(), m);
    }

    public Optional<Mercancia> buscar(String codigo) {
        return Optional.ofNullable(porCodigo.get(codigo));
    }

    public List<Mercancia> todas() {
        List<Mercancia> lista = new ArrayList<>(porCodigo.values());
        lista.sort(Comparator.comparing(Mercancia::getCodigo));
        return lista;
    }
}
```

`src/main/java/imperio/aduana/service/AduanaServicio.java`

```java
package imperio.aduana.service;

import imperio.aduana.dto.DeclaracionPedido;
import imperio.aduana.dto.DeclaracionRespuesta;
import imperio.aduana.dto.DepuracionRespuesta;
import imperio.aduana.dto.MercanciaPedido;
import imperio.aduana.exception.ConflictoException;
import imperio.aduana.exception.NoEncontradoException;
import imperio.aduana.model.Barril;
import imperio.aduana.model.Caja;
import imperio.aduana.model.Mercader;
import imperio.aduana.model.Mercancia;
import imperio.aduana.model.Peregrino;
import imperio.aduana.model.Viajero;
import imperio.aduana.repository.MercanciaRepositorio;
import imperio.aduana.strategy.RecargoStrategy;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AduanaServicio {
    private final MercanciaRepositorio repositorio;
    private final Map<String, RecargoStrategy> estrategias;   // Spring junta los @Component por nombre
    private String estrategiaActiva = "normal";

    public Mercancia registrar(MercanciaPedido p) {
        if (repositorio.existe(p.codigo())) {
            throw new ConflictoException("Ya existe la mercancía " + p.codigo());
        }
        Mercancia m = switch (p.tipo()) {
            case "CAJA" -> new Caja(p.codigo(), p.descripcion(), p.valorDeclarado());
            case "BARRIL" -> new Barril(p.codigo(), p.descripcion(), p.valorDeclarado(), p.litros());
            default -> throw new IllegalArgumentException("Tipo desconocido: " + p.tipo());
        };
        repositorio.guardar(m);
        return m;
    }

    public Mercancia buscar(String codigo) {
        return repositorio.buscar(codigo).orElseThrow(() -> new NoEncontradoException("No existe la mercancía " + codigo));
    }

    public List<Mercancia> todas() {
        return repositorio.todas();
    }

    public String getEstrategiaActiva() {
        return estrategiaActiva;
    }

    public void activar(String nombre) {
        if (!estrategias.containsKey(nombre)) {
            throw new IllegalArgumentException("Estrategia desconocida: " + nombre + ". Opciones: " + new java.util.TreeSet<>(estrategias.keySet()));
        }
        estrategiaActiva = nombre;
    }

    public DeclaracionRespuesta declarar(DeclaracionPedido p) {
        Viajero viajero = p.tipoViajero().equals("PEREGRINO")
                ? new Peregrino(p.viajero(), p.pasaporte())
                : new Mercader(p.viajero(), p.pasaporte());
        List<Mercancia> mercancias = p.codigos().stream().map(this::buscar).toList();
        double valor = mercancias.stream().mapToDouble(Mercancia::getValorDeclarado).sum();
        double impuestos = mercancias.stream().mapToDouble(Mercancia::impuesto).sum();
        double recargo = estrategias.get(estrategiaActiva).calcular(p.diasDemora(), valor) * viajero.factorRecargo();
        return new DeclaracionRespuesta(viajero.getNombre(), mercancias.size(), redondear(impuestos), redondear(recargo),
                redondear(impuestos + recargo), estrategiaActiva);
    }

    /** Una sola pasada: el HashSet dice en O(1) si el pasaporte ya apareció. */
    public DepuracionRespuesta depurar(List<String> pasaportes) {
        Set<String> vistos = new LinkedHashSet<>();
        Set<String> duplicados = new LinkedHashSet<>();
        for (String p : pasaportes) {
            if (!vistos.add(p)) {
                duplicados.add(p);
            }
        }
        return new DepuracionRespuesta(vistos, duplicados);
    }

    private static double redondear(double x) {
        return Math.round(x * 100) / 100.0;
    }
}
```

`src/main/java/imperio/aduana/controller/AduanaController.java`

```java
package imperio.aduana.controller;

import imperio.aduana.dto.DeclaracionPedido;
import imperio.aduana.dto.DeclaracionRespuesta;
import imperio.aduana.dto.DepuracionRespuesta;
import imperio.aduana.dto.MercanciaPedido;
import imperio.aduana.dto.MercanciaRespuesta;
import imperio.aduana.service.AduanaServicio;
import jakarta.validation.Valid;
import java.util.List;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
public class AduanaController {
    private final AduanaServicio servicio;

    @PostMapping("/mercancias")
    @ResponseStatus(HttpStatus.CREATED)
    public MercanciaRespuesta registrar(@Valid @RequestBody MercanciaPedido pedido) {
        return MercanciaRespuesta.de(servicio.registrar(pedido));
    }

    @GetMapping("/mercancias")
    public List<MercanciaRespuesta> todas() {
        return servicio.todas().stream().map(MercanciaRespuesta::de).toList();
    }

    @GetMapping("/mercancias/{codigo}")
    public MercanciaRespuesta buscar(@PathVariable String codigo) {
        return MercanciaRespuesta.de(servicio.buscar(codigo));
    }

    @GetMapping("/recargo")
    public Map<String, String> estrategia() {
        return Map.of("estrategia", servicio.getEstrategiaActiva());
    }

    @PutMapping("/recargo/{nombre}")
    public Map<String, String> activar(@PathVariable String nombre) {
        servicio.activar(nombre);
        return Map.of("estrategia", servicio.getEstrategiaActiva());
    }

    @PostMapping("/declaraciones")
    public DeclaracionRespuesta declarar(@Valid @RequestBody DeclaracionPedido pedido) {
        return servicio.declarar(pedido);
    }

    @PostMapping("/pasaportes/depurar")
    public DepuracionRespuesta depurar(@RequestBody List<String> pasaportes) {
        return servicio.depurar(pasaportes);
    }
}
```

`src/main/java/imperio/aduana/exception/NoEncontradoException.java`

```java
package imperio.aduana.exception;

public class NoEncontradoException extends RuntimeException {
    public NoEncontradoException(String mensaje) {
        super(mensaje);
    }
}
```

`src/main/java/imperio/aduana/exception/ConflictoException.java`

```java
package imperio.aduana.exception;

public class ConflictoException extends RuntimeException {
    public ConflictoException(String mensaje) {
        super(mensaje);
    }
}
```

`src/main/java/imperio/aduana/exception/ManejadorErrores.java`

```java
package imperio.aduana.exception;

import java.util.Map;
import java.util.TreeMap;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ManejadorErrores {
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail invalido(MethodArgumentNotValidException e) {
        Map<String, String> campos = new TreeMap<>();
        e.getBindingResult().getFieldErrors().forEach(f -> campos.put(f.getField(), f.getDefaultMessage()));
        ProblemDetail p = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "Datos inválidos");
        p.setProperty("campos", campos);
        return p;
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ProblemDetail argumento(IllegalArgumentException e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, e.getMessage());
    }

    @ExceptionHandler(NoEncontradoException.class)
    public ProblemDetail noEncontrado(NoEncontradoException e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
    }

    @ExceptionHandler(ConflictoException.class)
    public ProblemDetail conflicto(ConflictoException e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, e.getMessage());
    }
}
```

### Misión R05-N06-M2 · Las pruebas del Dragón

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 30
```

#### Consigna

Probá AduanaExpress con **JUnit y MockMvc** (`@SpringBootTest` y `@AutoConfigureMockMvc`), sin
levantar el servidor a mano. Las pruebas tienen que cubrir, como mínimo:

1. Registrar una caja y un barril (201, con su impuesto), buscar uno (200), uno que no existe (404),
   un código repetido (409) y un pedido inválido (400 con los campos).
2. Una declaración con la estrategia **normal** y un mercader, y otra con **feria** y un
   **peregrino**, comprobando impuestos, recargo y total; una estrategia que no existe (400).
3. La depuración de pasaportes: cuántos únicos y cuáles duplicados, en orden.

Cada prueba arranca con la aplicación limpia (`@DirtiesContext`), porque los datos están en
memoria. Entregá el `.zip` del proyecto con las pruebas pasando (`./mvnw test`).

#### Criterio de aprobación

- Las pruebas cubren los tres grupos y comprueban códigos de estado **y** valores del JSON.
- Cada prueba es independiente: no depende del orden ni de lo que dejó otra.
- `./mvnw test` pasa sin errores.

#### Solución de referencia

`src/test/java/imperio/aduana/AduanaExpressTest.java`

```java
package imperio.aduana;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.BEFORE_EACH_TEST_METHOD)
class AduanaExpressTest {
    @Autowired
    MockMvc mvc;

    void cargar() throws Exception {
        mvc.perform(post("/api/mercancias").contentType(MediaType.APPLICATION_JSON)
                .content("{\"tipo\":\"CAJA\",\"codigo\":\"C1\",\"descripcion\":\"sal\",\"valorDeclarado\":1000,\"litros\":0}"))
                .andExpect(status().isCreated()).andExpect(jsonPath("$.impuesto").value(100.0));
        mvc.perform(post("/api/mercancias").contentType(MediaType.APPLICATION_JSON)
                .content("{\"tipo\":\"BARRIL\",\"codigo\":\"B1\",\"descripcion\":\"vino\",\"valorDeclarado\":500,\"litros\":40}"))
                .andExpect(status().isCreated()).andExpect(jsonPath("$.impuesto").value(70.0));
    }

    @Test
    void registraBuscaYRechaza() throws Exception {
        cargar();
        mvc.perform(get("/api/mercancias/B1")).andExpect(status().isOk()).andExpect(jsonPath("$.tipo").value("BARRIL"));
        mvc.perform(get("/api/mercancias/X9")).andExpect(status().isNotFound());
        mvc.perform(post("/api/mercancias").contentType(MediaType.APPLICATION_JSON)
                .content("{\"tipo\":\"CAJA\",\"codigo\":\"C1\",\"descripcion\":\"otra\",\"valorDeclarado\":10,\"litros\":0}"))
                .andExpect(status().isConflict());
        mvc.perform(post("/api/mercancias").contentType(MediaType.APPLICATION_JSON)
                .content("{\"tipo\":\"BOLSA\",\"codigo\":\"\",\"descripcion\":\"x\",\"valorDeclarado\":-5,\"litros\":0}"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.tipo").exists())
                .andExpect(jsonPath("$.campos.codigo").exists())
                .andExpect(jsonPath("$.campos.valorDeclarado").exists());
    }

    @Test
    void declaraConLaEstrategiaActivaYElDescuentoDelPeregrino() throws Exception {
        cargar();
        String mercader = "{\"viajero\":\"Baldo\",\"pasaporte\":\"AR-101\",\"tipoViajero\":\"MERCADER\",\"codigos\":[\"C1\",\"B1\"],\"diasDemora\":5}";
        mvc.perform(post("/api/declaraciones").contentType(MediaType.APPLICATION_JSON).content(mercader))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.impuestos").value(170.0))
                .andExpect(jsonPath("$.recargo").value(150.0))
                .andExpect(jsonPath("$.total").value(320.0))
                .andExpect(jsonPath("$.estrategia").value("normal"));

        mvc.perform(put("/api/recargo/feria")).andExpect(status().isOk()).andExpect(jsonPath("$.estrategia").value("feria"));
        String peregrino = mercader.replace("MERCADER", "PEREGRINO");
        mvc.perform(post("/api/declaraciones").contentType(MediaType.APPLICATION_JSON).content(peregrino))
                .andExpect(jsonPath("$.recargo").value(15.0))
                .andExpect(jsonPath("$.total").value(185.0));

        mvc.perform(put("/api/recargo/lunar")).andExpect(status().isBadRequest());
        mvc.perform(post("/api/declaraciones").contentType(MediaType.APPLICATION_JSON)
                .content(mercader.replace("\"B1\"", "\"X9\""))).andExpect(status().isNotFound());
    }

    @Test
    void depuraLosPasaportesEnUnaPasada() throws Exception {
        mvc.perform(post("/api/pasaportes/depurar").contentType(MediaType.APPLICATION_JSON)
                .content("[\"AR-101\",\"UY-202\",\"AR-101\",\"CL-303\",\"UY-202\",\"AR-101\"]"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.unicos.length()").value(3))
                .andExpect(jsonPath("$.duplicados[0]").value("AR-101"))
                .andExpect(jsonPath("$.duplicados[1]").value("UY-202"));
    }
}
```

### Prueba del sello

#### ¿En qué capa va la regla «el peregrino paga la mitad del recargo»?

En el modelo (`factorRecargo()` de cada viajero) o en el servicio, nunca en el controlador: el controlador solo traduce entre HTTP y los DTO.

#### ¿Cómo se cambia la estrategia de recargo sin tocar el cálculo?

Cada estrategia es una clase que implementa `RecargoStrategy`; el servicio guarda cuál está activa y le delega el cálculo. Cambiarla es cambiar esa referencia.

#### ¿Por qué un `HashMap` para las mercancías y un `HashSet` para los pasaportes?

Porque buscar por código en un `HashMap` y preguntar si ya está en un `HashSet` es O(1): todo se resuelve en una sola pasada.

#### ¿Qué devuelve la API cuando el código no existe, y desde dónde?

Un 404 con un `ProblemDetail`, armado por el `@RestControllerAdvice` a partir de una excepción propia que lanza el servicio.

#### ¿Qué tiene que tener la entrega además del código?

El repositorio de GitHub con commits a medida que se avanza, el `README.md`, la colección de Postman exportada y el `EVIDENCIAS.md` con una captura de cada pedido.


### Soluciones (docente)

Nodo nuevo (D96): el simulacro del examen final, con el formato del último (BiblioExpress) ambientado en el Imperio. La solución de referencia compila con Spring Boot 3.3.5 y Java 17 y sus pruebas de la M2 pasan con `./mvnw test`. Está pensado para 180 minutos, pero pasarse no se penaliza: el alumno anota en el `README.md` cuánto tardó, y eso sirve para ver cuánto le falta para el examen. Se corrige con la grilla del criterio.

## R05-N07 · La Encrucijada de los Denarios

```meta
tipo: ventana
padre: R05-N06
precio: 10
```

### Crónica

En lo más alto de la Torre hay una ventana que nunca se abrió, con un marco vacío. Zed desenvuelve el vitral del viajero y lo coloca; la Llave del Vitral entra justo. El vidrio se enciende y muestra, por un instante, un balcón con cuatro portales y una frase grabada en el marco: *«para quien llegue»*.

Abajo, en la plaza central del Imperio, hay una fuente con forma de denario gigante, y de ella salen cuatro avenidas: una baja a la Bóveda, otra al Palacio de las Ventanas, otra a una sala de juegos llena de luces y la última al Puerto. Nadia vuelve a la Aduana, ahora como jefa de turno. Gheco señala las avenidas.

{mentor} espera a Zed sentado en el borde de la fuente, con una taza de café. —Ya hablás la lengua del Imperio. Lo que sigue no es obligatorio: es **tuyo**. Pero antes de elegir, mirá hacia atrás. ¿Qué te llevás de este viaje?

### Objetivos

- Repasar todo el camino principal y reconocer lo que aprendiste.
- Conocer las Sendas optativas que salen de acá.

### Explicación

#### Lo que ya sabés hacer

- **La Aduana del Compilador**: compilar y ejecutar, tipos, operadores, textos, entrada por teclado, decisiones, bucles, arrays y métodos.
- **La Academia de los Moldes**: clases y objetos, constructores, encapsulamiento, referencias, herencia, polimorfismo, interfaces, composición, `enum`, `record` y diagramas UML.
- **Los Archivos Imperiales**: paquetes y `.jar`, listas con envoltorios y autoboxing, mapas y conjuntos, excepciones, lambdas, pruebas con JUnit y depuración.
- **Las Corrientes del Imperio**: *streams*, `Collectors` y `Optional`, comparadores y Java moderno, patrones de diseño y concurrencia.
- **La Torre del Arquitecto**: Spring Boot con su contenedor e inyección de dependencias, servicios REST, capas con DTO, validaciones y Lombok.

Con eso podés construir un servicio web en capas como el del examen final de *Paradigmas y Lenguajes III* y leer el código Java de otros. Lo que sigue son **especializaciones**.

#### Las Sendas

Cada Senda es un camino optativo: no hace falta para completar el curso, y su entrada se paga con **comodines** (los que ganaste con los encargos). Adentro, los nodos se pagan con denarios, como siempre.

- **Senda de la Bóveda Imperial**: archivos, **SQL con PostgreSQL** (tablas, consultas, procedimientos, triggers y roles), JDBC, DAO y transacciones.
- **Senda del Palacio de las Ventanas**: **aplicaciones de escritorio** con Swing: layouts, componentes, tablas y árboles, MDI, `SwingWorker` y el MVC de la cátedra, hasta un sistema de actas completo (pide la Bóveda).
- **Senda del Arcade Imperial**: un **juego 2D** con Swing y Java2D: dibujar en un lienzo, el bucle de juego con un `Timer`, teclado, sprites, colisiones y un juego completo.
- **Senda del Puerto de Spring**: **persistencia con JPA** en PostgreSQL y el Kraken de los Servicios (pide lo básico de SQL de la Bóveda).

### Misión R05-N07-M1 · Mirá hacia atrás

```meta
entrega: ninguna
entorno: navegador
monedas: 0
xp: 20
```

#### Consigna

Antes de elegir tu Senda, tomate cinco minutos:

1. ¿Cuál fue el tema que más te costó? ¿Qué te ayudó a entenderlo?
2. ¿Qué programa de todo el camino te dio más orgullo?
3. ¿Qué te gustaría construir ahora con Java?

Charlalo con el profe en la próxima clase (o escribíselo). Cuando lo tengas, marcá la misión como completada.

#### Criterio de aprobación

- Pensaste las tres preguntas y lo charlaste con el profe.

### Prueba del sello

#### ¿Cuántas Sendas salen de la Encrucijada y con qué se paga su entrada?

Tres (el Arcade Imperial, las Corrientes y el Puerto de Spring), y la entrada se paga con comodines.

#### ¿Hace falta completar una Senda para terminar el curso?

No: las Sendas son optativas.

### Soluciones (docente)

Nodo de cierre del tronco (tipo `ventana`), como la Encrucijada de los otros cursos. La misión es de reflexión y no se entrega.
