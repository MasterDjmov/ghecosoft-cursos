# RAMA R05 · La Prueba del Temple: calidad y proyectos

```meta
tipo: tronco
posicion: 5
```

## R05-N01 · Depuración

```meta
tipo: tema
padre: R04-N06
precio: 10
criatura: ogro
```

### Crónica

Para ser maestro de la Forja hay que pasar la **Prueba del Temple**. La primera sala está a oscuras y llena de piezas que parecen perfectas… pero algunas se quiebran al primer golpe.

—Una espada que se ve bien no es una espada que anda, {heroe} —dice {mentor}, y te da una lupa de cristal—. Esta es la **lupa del depurador**. Con ella se mira adentro del metal mientras trabaja, golpe por golpe.

### Objetivos

- Seguir la ejecución de un programa con `gdb`: puntos de parada, avanzar línea por línea, ver variables y la pila de llamadas.
- Detectar errores de memoria y de **comportamiento indefinido** con los sanitizadores y `valgrind`.
- Tener un método: reproducir, aislar, entender, corregir y volver a probar.

### Antes de empezar

- Funciones y recursión (08), punteros (13) y memoria dinámica (R03-N01).
- Compilar con advertencias (01).

### Explicación

#### Primero, un método

1. **Reproducir**: encontrar una entrada con la que el error aparece siempre.
2. **Aislar**: achicar el problema (¿qué función? ¿qué línea?).
3. **Entender** por qué pasa, antes de tocar nada.
4. **Corregir** y **volver a probar** con la misma entrada… y con otras.

Mostrar variables con `printf` sirve, pero ensucia el código y hay que borrarlo después. El depurador hace lo mismo sin tocar el programa.

#### `gdb` en cinco comandos

Se compila con información de depuración (`-g`) y sin optimizar (`-O0`):

```bash
gcc -std=c11 -Wall -Wextra -g -O0 -o programa main.c
gdb ./programa
```

| Comando | Qué hace |
|---|---|
| `break poder` (o `b main.c:17`) | frenar al entrar a `poder` (o en esa línea) |
| `run` (`r`) | ejecutar hasta el próximo punto de parada |
| `next` (`n`) / `step` (`s`) | ejecutar una línea; `step` además **entra** a las funciones |
| `print e->vida` (`p`) | mostrar una variable o expresión |
| `backtrace` (`bt`) | ver la pila: qué función llamó a cuál, con qué argumentos |
| `continue` (`c`) / `quit` (`q`) | seguir hasta la próxima parada / salir |

Una sesión con el ejemplo:

```
(gdb) break poder
(gdb) run
Breakpoint 1, poder (e=0x7ffc...) at main.c:17
17	    int p = e->vida + e->ataque * 3;
(gdb) print *e
$1 = {nombre = 0x55... "Goblin", vida = 22, ataque = 7}
(gdb) next
18	    return p;
(gdb) print p
$2 = 43
(gdb) backtrace
#0  poder (e=0x7ffc...) at main.c:18
#1  main () at main.c:37
```

Si el programa se corta (`Segmentation fault`), ejecutalo dentro de `gdb`: se frena justo en la línea del problema, y `bt` muestra cómo se llegó ahí.

#### Los sanitizadores

```bash
gcc -g -fsanitize=address,undefined -o programa main.c
```

- **`address`**: accesos fuera de un array, uso después de liberar, fugas.
- **`undefined`**: comportamiento indefinido, como el desbordamiento de un `int` con signo o un desplazamiento de bits inválido.

`valgrind ./programa` encuentra problemas parecidos sin recompilar (más lento).

#### Comportamiento indefinido

C no promete nada en algunos casos: el programa puede andar, dar cualquier cosa o cortarse, y puede cambiar con otro compilador u otra optimización. Los más comunes:

- usar una variable local **sin inicializar**;
- leer o escribir **fuera de un array**;
- **desbordar** un entero con signo (`INT_MAX + 1`);
- desreferenciar `NULL` o un puntero liberado;
- modificar la misma variable dos veces en una expresión (`x++ + x++`).

"En mi compu anda" no alcanza: hay que compilar con `-Wall -Wextra` y los sanitizadores.

### Código de ejemplo

```c
/*
 * 26 - Depuracion: un programa correcto para practicar con gdb.
 *   gcc -std=c11 -Wall -Wextra -g -O0 -o programa main.c
 *   gdb ./programa
 */
#include <stdio.h>

typedef struct {
    const char *nombre;
    int vida;
    int ataque;
} Enemigo;

int poder(const Enemigo *e)
{
    int p = e->vida + e->ataque * 3;      /* un buen lugar para un "break poder" */
    return p;
}

const Enemigo *mas_fuerte(const Enemigo *v, int n)
{
    const Enemigo *mejor = &v[0];
    for (int i = 1; i < n; i++) {
        if (poder(&v[i]) > poder(mejor)) {
            mejor = &v[i];
        }
    }
    return mejor;
}

int main(void)
{
    Enemigo horda[] = { { "Goblin", 22, 7 }, { "Orco", 40, 12 }, { "Troll", 70, 9 }, { "Ogro", 55, 14 } };
    int n = sizeof(horda) / sizeof(horda[0]);
    for (int i = 0; i < n; i++) {
        printf("%-7s poder %3d\n", horda[i].nombre, poder(&horda[i]));
    }
    const Enemigo *jefe = mas_fuerte(horda, n);
    printf("El más fuerte es %s\n", jefe->nombre);
    return 0;
}
```

### Salida esperada

```
Goblin  poder  43
Orco    poder  76
Troll   poder  97
Ogro    poder  97
El más fuerte es Troll
```

### ¿Para qué sirve?

Depurar es buena parte del trabajo de cualquier programador: se estima que se pasa más tiempo encontrando y corrigiendo errores que escribiendo código nuevo. `gdb` y los sanitizadores se usan en el desarrollo de sistemas operativos, navegadores y motores de juegos; y el comportamiento indefinido es el origen de muchas fallas de seguridad famosas, por eso las empresas grandes compilan sus pruebas con sanitizadores todos los días.

### Errores habituales

**Ogro: el error que "desaparece".** Agregás un `printf` y el programa anda: casi siempre es comportamiento indefinido (una variable sin inicializar, un acceso fuera del array) que cambió de lugar. No está arreglado: compilá con sanitizadores.

**Ogro: depurar sin `-g`.** `gdb` muestra direcciones en lugar de líneas y no ve las variables.

**Ogro: depurar con `-O2`.** El optimizador reordena y elimina variables: `print x` dice `<optimized out>`. Para depurar, `-O0`.

**Troll: arreglar el síntoma.** Poner un `if` para que no se corte, sin entender por qué el valor estaba mal: el error sigue ahí y aparece en otro lado.

Un informe típico de `-fsanitize=undefined`:

```
main.c:9:11: runtime error: signed integer overflow: 479001600 * 13 cannot be represented in type 'int'
```

### Misión R05-N01-M1 · El promedio que miente

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El código inicial calcula el promedio de cinco temperaturas y cuántas lo superan, pero tiene **dos** errores.

1. Compilalo con `-g -fsanitize=address` y ejecutalo: uno de los errores aparece enseguida.
2. Con `gdb` (o mirando el valor que devuelve `promedio`), encontrá el otro: el promedio está mal aunque no se corte nada.
3. Corregí los dos y explicá cada uno en un comentario al principio.

#### Criterio de aprobación

- El bucle ya no lee fuera del array.
- La división se hace con decimales (`(double) suma / n`).
- Explica los dos errores; sin avisos del sanitizador.

#### Código inicial

```c
/* Este programa deberia mostrar el promedio de las temperaturas y cuantas lo superan. Tiene dos errores. */
#include <stdio.h>

double promedio(const int *v, int n)
{
    int suma = 0;
    for (int i = 0; i <= n; i++) {
        suma += v[i];
    }
    return suma / n;
}

int main(void)
{
    int temperaturas[] = { 870, 905, 1210, 640, 1500 };
    int n = 5;
    double p = promedio(temperaturas, n);
    int arriba = 0;
    for (int i = 0; i < n; i++) {
        if (temperaturas[i] > p) {
            arriba++;
        }
    }
    printf("Promedio: %.2f\n", p);
    printf("Superan el promedio: %d\n", arriba);
    return 0;
}
```

#### Salida esperada

```
Promedio: 1025.00
Superan el promedio: 2
```

#### Solución de referencia

```c
/*
 * Mision 1 - El promedio que miente, corregido.
 *  1. El for iba hasta i <= n: leia temperaturas[5], fuera del array (-fsanitize=address lo marca).
 *  2. suma / n dividia dos enteros: se perdian los decimales. Se convierte a double antes.
 */
#include <stdio.h>

double promedio(const int *v, int n)
{
    int suma = 0;
    for (int i = 0; i < n; i++) {
        suma += v[i];
    }
    return (double) suma / n;
}

int main(void)
{
    int temperaturas[] = { 870, 905, 1210, 640, 1500 };
    int n = 5;
    double p = promedio(temperaturas, n);
    int arriba = 0;
    for (int i = 0; i < n; i++) {
        if (temperaturas[i] > p) {
            arriba++;
        }
    }
    printf("Promedio: %.2f\n", p);
    printf("Superan el promedio: %d\n", arriba);
    return 0;
}
```

### Misión R05-N01-M2 · Lo que no está definido

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El código inicial tiene **tres** comportamientos indefinidos y, según la compu, puede parecer que anda. Compilalo con `-Wall -Wextra -g -fsanitize=address,undefined`, leé las advertencias y los informes, y corregí los tres. En un comentario, explicá cada uno: por qué es indefinido y cómo lo arreglaste.

#### Criterio de aprobación

- Inicializa `total`.
- Usa `long long` para el factorial (13! no entra en `int`).
- Separa `x++ + x++` en pasos.
- Sin advertencias ni informes del sanitizador.

#### Código inicial

```c
/* Tiene tres comportamientos indefinidos. En tu compu puede "andar". Encontralos. */
#include <stdio.h>

int factorial(int n)
{
    int r = 1;
    for (int i = 2; i <= n; i++) {
        r *= i;
    }
    return r;
}

int main(void)
{
    int total;
    for (int i = 1; i <= 3; i++) {
        total += i;
    }
    printf("1 + 2 + 3 = %d\n", total);
    printf("13! = %d\n", factorial(13));
    int x = 5;
    int y = x++ + x++;
    printf("y = %d\n", y);
    return 0;
}
```

#### Salida esperada

```
1 + 2 + 3 = 6
13! = 6227020800
y = 11
```

#### Solución de referencia

```c
/*
 * Mision 2 - Lo que no esta definido, corregido.
 *  1. total no tenia valor inicial: empezaba con basura. (-Wall lo avisa: "may be used uninitialized")
 *  2. 13! no entra en un int: el desbordamiento con signo es indefinido (-fsanitize=undefined lo marca). Va long long.
 *  3. x++ + x++ modifica x dos veces en la misma expresion: indefinido. Se separa en pasos.
 */
#include <stdio.h>

long long factorial(int n)
{
    long long r = 1;
    for (int i = 2; i <= n; i++) {
        r *= i;
    }
    return r;
}

int main(void)
{
    int total = 0;
    for (int i = 1; i <= 3; i++) {
        total += i;
    }
    printf("1 + 2 + 3 = %d\n", total);
    printf("13! = %lld\n", factorial(13));
    int x = 5;
    int a = x++;
    int b = x++;
    int y = a + b;
    printf("y = %d\n", y);
    return 0;
}
```

### Misión R05-N01-M3 · La escalera sin fin

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El código inicial calcula con recursión la suma `n + (n - 2) + (n - 4) + …`. Con 4 anda, pero con 5 se corta con `Segmentation fault`.

1. Ejecutalo dentro de `gdb` (`run`) y, cuando se corte, usá `backtrace` (`bt`). ¿Qué ves en los valores de `n`?
2. Explicá por qué la recursión no termina y corregí el caso base.

#### Criterio de aprobación

- Usa `gdb` y `backtrace` para diagnosticar (lo explica en un comentario).
- Corrige el caso base para que atrape los valores menores o iguales a 0.
- Muestra los dos resultados.

#### Código inicial

```c
/* Se corta con "Segmentation fault". Usa gdb y "backtrace" para ver por que. */
#include <stdio.h>

int escalones(int n)
{
    if (n == 0) {
        return 0;
    }
    return n + escalones(n - 2);
}

int main(void)
{
    printf("Escalones de 4: %d\n", escalones(4));
    printf("Escalones de 5: %d\n", escalones(5));
    return 0;
}
```

#### Salida esperada

```
Escalones de 4: 6
Escalones de 5: 9
```

#### Solución de referencia

```c
/*
 * Mision 3 - La escalera sin fin, corregida.
 * Con n impar, n - 2 salta el 0 (5, 3, 1, -1, -3...) y la recursion no termina:
 * la pila se llena y el programa se corta. En gdb, "bt" muestra miles de
 * llamadas a escalones con n negativo. El caso base tiene que atrapar n <= 0.
 */
#include <stdio.h>

int escalones(int n)
{
    if (n <= 0) {
        return 0;
    }
    return n + escalones(n - 2);
}

int main(void)
{
    printf("Escalones de 4: %d\n", escalones(4));
    printf("Escalones de 5: %d\n", escalones(5));
    return 0;
}
```

### Encargo R05-N01-E1 · El cajero que redondea mal

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un cajero del Gremio sumaba diez centavos mil veces con `float` y el saldo no daba $100.00. Mostrá el problema: sumá `0.10f` mil veces en un `float` y 10 centavos mil veces en un entero (`long long`), y mostrá los dos resultados. Después convertí `19.99` a centavos redondeando bien, y mostrá qué pasa si no se redondea.

#### Criterio de aprobación

- Muestra el error acumulado del `float`.
- Lleva la plata en centavos enteros y la muestra con 2 decimales.
- Redondea al convertir a centavos.

#### Salida esperada

```
Con float:    99.999046
En centavos:  100.00
19.99 en centavos: 1999 (sin redondear: 1998)
```

#### Solución de referencia

```c
/*
 * Encargo - El cajero que redondea mal: con float, 0.10 sumado mil veces no da 100.
 * Solucion: la plata se guarda en centavos, con enteros.
 */
#include <stdio.h>

int main(void)
{
    float saldo_float = 0;
    long long saldo_centavos = 0;
    for (int i = 0; i < 1000; i++) {
        saldo_float += 0.10f;          /* diez centavos, mil veces */
        saldo_centavos += 10;
    }
    printf("Con float:    %.6f\n", saldo_float);
    printf("En centavos:  %lld.%02lld\n", saldo_centavos / 100, saldo_centavos % 100);

    double precio = 19.99;
    long long centavos = (long long) (precio * 100 + 0.5);   /* redondear al convertir */
    printf("19.99 en centavos: %lld (sin redondear: %lld)\n", centavos, (long long) (precio * 100));
    return 0;
}
```

### Prueba del sello

#### ¿Para qué sirve compilar con `-g`? ¿Y con `-O0`?

`-g` agrega la información para que el depurador muestre líneas y variables. `-O0` evita que el optimizador reordene o elimine variables.

#### ¿Qué diferencia hay entre `next` y `step` en `gdb`?

Los dos ejecutan una línea, pero `step` entra a las funciones que se llaman en esa línea y `next` las ejecuta de una.

#### El programa se corta con `Segmentation fault`. ¿Qué hacés primero?

Lo ejecuto dentro de `gdb` (o con `-fsanitize=address`) para ver en qué línea se corta y, con `backtrace`, cómo se llegó ahí.

#### ¿Qué es el comportamiento indefinido? Da dos ejemplos.

Casos en los que C no promete ningún resultado: el programa puede hacer cualquier cosa. Por ejemplo, una variable sin inicializar o desbordar un `int` con signo.

#### ¿Por qué "en mi compu anda" no alcanza?

Porque con comportamiento indefinido el resultado puede cambiar en otra máquina, con otro compilador o con otras opciones, aunque en la tuya justo dé bien.

### Soluciones (docente)

Unidad nueva (planificada como 26). Las misiones parten de programas con errores; se corrige con `-g -fsanitize=address,undefined`.

## R05-N02 · Tests

```meta
tipo: tema
padre: R05-N01
precio: 10
criatura: ogro
```

### Crónica

La segunda sala de la Prueba del Temple está llena de martillos de prueba. Antes de entregar una espada, el maestro la golpea en los lugares donde **suele** quebrarse: la punta, el filo, la unión con la empuñadura.

—No se prueba donde la espada es fuerte, {heroe} —dice {mentor}—. Se prueba en los bordes. Y se prueba **cada vez** que se toca el metal, no una sola.

### Objetivos

- Escribir **pruebas automáticas**: un programa que verifica que tus funciones hacen lo que deben.
- Usar `assert` para las precondiciones y un mini framework de pruebas con macros.
- Elegir los **casos límite** que hay que probar.

### Antes de empezar

- Funciones (08), strings (11) y el preprocesador con macros (R04-N03).
- Depuración (R05-N01).

### Explicación

#### Probar a mano no escala

Cada vez que cambiás una función, habría que volver a probar todo a mano. Una **prueba automática** es código que llama a tus funciones con datos conocidos y compara con el resultado esperado. Se ejecuta en un segundo, siempre igual, cada vez que tocás algo.

#### `assert`: lo que no puede pasar

```c
#include <assert.h>

int maximo(const int *v, int n)
{
    assert(v != NULL && n > 0);      /* si es falso, el programa se detiene acá */
    ...
}
```

Si la condición es falsa, el programa se corta con el archivo, la línea y la condición:

```
programa: main.c:36: maximo: Assertion `v != NULL && n > 0' failed.
Aborted (core dumped)
```

`assert` es para **errores de programación** (alguien llamó mal a la función), no para validar lo que escribe el usuario. Compilando con `-DNDEBUG`, todos los `assert` desaparecen.

#### Un mini framework

Con dos macros alcanza para contar pruebas y mostrar las que fallan:

```c
static int pruebas = 0, fallas = 0;

#define VERIFICAR(condicion)                                               \
    do {                                                                   \
        pruebas++;                                                         \
        if (!(condicion)) {                                                \
            fallas++;                                                      \
            printf("  FALLA %s:%d: %s\n", __FILE__, __LINE__, #condicion); \
        }                                                                  \
    } while (0)
```

- `#condicion` convierte la condición en texto: el mensaje muestra **qué** falló.
- `__FILE__` y `__LINE__` dicen **dónde**.
- El `do { ... } while (0)` hace que la macro se comporte como una sola instrucción (se puede usar dentro de un `if` sin llaves).
- El programa de pruebas devuelve 0 si todo pasó y 1 si no: un script (o `make test`) sabe si hubo fallas.

#### Qué probar: los bordes

Los errores viven en los **casos límite**:

- el vacío (array de 0 elementos, texto `""`), un solo elemento, el máximo;
- el cero, los negativos, el primero y el último;
- lo que **parece** cumplir y no cumple (91 parece primo: es 7 × 13).

#### Primero la prueba

Una forma de trabajar muy usada: escribir las pruebas **antes** que la función. Primero fallan todas; después se escribe el código hasta que pasan. Así la prueba describe exactamente lo que querés que haga.

### Código de ejemplo

```c
/*
 * 27 - Tests: el programa prueba sus propias funciones.
 */
#include <stdio.h>
#include <stdbool.h>
#include <assert.h>

/* Un mini framework de tests: cuenta las pruebas y muestra las que fallan con su linea. */
static int pruebas = 0, fallas = 0;

#define VERIFICAR(condicion)                                                   \
    do {                                                                       \
        pruebas++;                                                             \
        if (!(condicion)) {                                                    \
            fallas++;                                                          \
            printf("  FALLA %s:%d: %s\n", __FILE__, __LINE__, #condicion);     \
        }                                                                      \
    } while (0)

#define RESUMEN()                                                              \
    (printf("%d pruebas: %d bien, %d mal\n", pruebas, pruebas - fallas, fallas), fallas == 0 ? 0 : 1)

bool es_primo(int n)
{
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

int maximo(const int *v, int n)
{
    assert(v != NULL && n > 0);      /* precondicion: si se rompe, el programa se detiene aca */
    int m = v[0];
    for (int i = 1; i < n; i++) {
        if (v[i] > m) {
            m = v[i];
        }
    }
    return m;
}

int main(void)
{
    printf("es_primo:\n");
    VERIFICAR(!es_primo(-7));        /* casos limite: negativos, 0, 1 y 2 */
    VERIFICAR(!es_primo(0));
    VERIFICAR(!es_primo(1));
    VERIFICAR(es_primo(2));
    VERIFICAR(es_primo(97));
    VERIFICAR(!es_primo(91));        /* 7 x 13: parece primo */

    printf("maximo:\n");
    int uno[] = { 5 };
    int negativos[] = { -8, -3, -12 };
    int al_final[] = { 1, 2, 3, 99 };
    VERIFICAR(maximo(uno, 1) == 5);
    VERIFICAR(maximo(negativos, 3) == -3);
    VERIFICAR(maximo(al_final, 4) == 99);
    VERIFICAR(maximo(al_final, 4) == 3);  /* esta prueba esta mal a proposito: mira como se informa */

    return RESUMEN();
}
```

### Salida esperada

```
es_primo:
maximo:
  FALLA main.c:65: maximo(al_final, 4) == 3
10 pruebas: 9 bien, 1 mal
```

### ¿Para qué sirve?

Todo software serio tiene pruebas automáticas: los bancos prueban cada regla de sus cuentas, los navegadores tienen decenas de miles de pruebas, y servicios como GitHub las ejecutan solos cada vez que alguien sube un cambio (integración continua). Las pruebas permiten animarse a cambiar código viejo sin miedo a romper algo, y documentan cómo tiene que comportarse cada función.

### Errores habituales

**Ogro: probar solo el caso fácil.** `es_primo(7)` pasa… y `es_primo(1)` o `es_primo(91)` fallan sin que nadie se entere.

**Ogro: la prueba que siempre pasa.** `VERIFICAR(maximo(v, 4) == maximo(v, 4))` no prueba nada: hay que comparar con un valor **conocido**.

**Troll: `assert` con efectos.** `assert(depositar(&c, 100));`: con `-DNDEBUG` el `assert` desaparece… y el depósito también.

**Slime: la macro sin `do while (0)`.** Una macro de varias instrucciones dentro de un `if` sin llaves solo ejecuta la primera.

**Goblin: comparar `double` con `==`.** `VERIFICAR(promedio == 0.3)` puede fallar por el error de redondeo: se compara con una tolerancia, `fabs(promedio - 0.3) < 1e-9`.

### Misión R05-N02-M1 · Probar el bisiesto

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con el mini framework (`VERIFICAR` y `RESUMEN`), escribí las pruebas de `es_bisiesto`. Elegí casos que cubran **cada parte** de la regla: divisible por 4, no divisible por 4, divisible por 100 pero no por 400 (dos casos) y divisible por 400 (dos casos). El programa devuelve 0 si pasan todas.

#### Criterio de aprobación

- Cubre las cuatro partes de la regla, con casos límite como 1900, 2000 y 2100.
- Usa el mini framework y muestra el resumen.
- Devuelve 0 si todo pasa.

#### Salida esperada

```
6 pruebas: 6 bien, 0 mal
```

#### Solución de referencia

```c
/* Mision 1 - Probar el bisiesto con los casos que importan. */
#include <stdio.h>
#include <stdbool.h>

/* Un mini framework de tests: cuenta las pruebas y muestra las que fallan con su linea. */
static int pruebas = 0, fallas = 0;

#define VERIFICAR(condicion)                                                   \
    do {                                                                       \
        pruebas++;                                                             \
        if (!(condicion)) {                                                    \
            fallas++;                                                          \
            printf("  FALLA %s:%d: %s\n", __FILE__, __LINE__, #condicion);     \
        }                                                                      \
    } while (0)

#define RESUMEN()                                                              \
    (printf("%d pruebas: %d bien, %d mal\n", pruebas, pruebas - fallas, fallas), fallas == 0 ? 0 : 1)

bool es_bisiesto(int anio)
{
    return (anio % 4 == 0 && anio % 100 != 0) || anio % 400 == 0;
}

int main(void)
{
    VERIFICAR(es_bisiesto(2024));      /* divisible por 4 */
    VERIFICAR(!es_bisiesto(2026));     /* no divisible por 4 */
    VERIFICAR(!es_bisiesto(1900));     /* por 100 pero no por 400 */
    VERIFICAR(!es_bisiesto(2100));
    VERIFICAR(es_bisiesto(2000));      /* por 400 */
    VERIFICAR(es_bisiesto(2400));
    return RESUMEN();
}
```

### Misión R05-N02-M2 · Encontrar el bug con pruebas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La función `contar_palabras` del código inicial parece andar con `"hola mundo"`. Escribí pruebas para los casos límite: texto vacío, una palabra, espacios de más (al principio, al final y dobles), tabulaciones y saltos de línea, y un texto solo con espacios. Ejecutalas, mirá cuáles fallan y **después** corregí la función hasta que pasen todas.

#### Criterio de aprobación

- Tiene al menos 6 pruebas con casos límite.
- La función corregida pasa todas.
- Explica en un comentario qué fallaba.

#### Código inicial

```c
/* contar_palabras tiene errores. Escribi pruebas que los muestren y despues arreglala. */
#include <stdio.h>
#include <ctype.h>

int contar_palabras(const char *texto)
{
    int palabras = 0;
    for (int i = 0; texto[i] != '\0'; i++) {
        if (texto[i] == ' ') {
            palabras++;
        }
    }
    return palabras + 1;
}

int main(void)
{
    printf("%d\n", contar_palabras("hola mundo"));
    return 0;
}
```

#### Salida esperada

```
6 pruebas: 6 bien, 0 mal
```

#### Solución de referencia

```c
/*
 * Mision 2 - Encontrar el bug con pruebas.
 * La version original contaba espacios + 1: fallaba con el texto vacio (daba 1),
 * con espacios de mas (al principio, al final o dobles) y con tabulaciones.
 */
#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>

/* Un mini framework de tests: cuenta las pruebas y muestra las que fallan con su linea. */
static int pruebas = 0, fallas = 0;

#define VERIFICAR(condicion)                                                   \
    do {                                                                       \
        pruebas++;                                                             \
        if (!(condicion)) {                                                    \
            fallas++;                                                          \
            printf("  FALLA %s:%d: %s\n", __FILE__, __LINE__, #condicion);     \
        }                                                                      \
    } while (0)

#define RESUMEN()                                                              \
    (printf("%d pruebas: %d bien, %d mal\n", pruebas, pruebas - fallas, fallas), fallas == 0 ? 0 : 1)

int contar_palabras(const char *texto)
{
    int palabras = 0;
    bool en_palabra = false;
    for (int i = 0; texto[i] != '\0'; i++) {
        if (isspace((unsigned char) texto[i])) {
            en_palabra = false;
        } else if (!en_palabra) {
            en_palabra = true;
            palabras++;
        }
    }
    return palabras;
}

int main(void)
{
    VERIFICAR(contar_palabras("hola mundo") == 2);
    VERIFICAR(contar_palabras("") == 0);
    VERIFICAR(contar_palabras("forja") == 1);
    VERIFICAR(contar_palabras("  espacios   de  mas  ") == 3);
    VERIFICAR(contar_palabras("con\ttab\ny enter") == 4);
    VERIFICAR(contar_palabras("   ") == 0);
    return RESUMEN();
}
```

### Misión R05-N02-M3 · Primero la prueba

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí **primero** las pruebas y **después** la función `bool normalizar(const char *nombre, char *salida, size_t tam)`, que deja el nombre sin espacios de más y con Mayúscula Inicial en cada palabra, sin pasarse de `tam` (si no entra, devuelve `false`):

- `"kira"` → `"Kira"`; `"  bRON   el   enano "` → `"Bron El Enano"`; `"MIA"` → `"Mia"`;
- `""` y `"   "` → `""`;
- `"Maese Ferrum"` en un array de 5 → `false`.

Una macro `PROBAR(entrada, esperado)` ayuda a no repetir código.

#### Criterio de aprobación

- Las pruebas cubren los casos de la consigna.
- `normalizar` nunca se pasa de `tam` y devuelve `false` si no entra.
- Pasan todas las pruebas.

#### Salida esperada

```
6 pruebas: 6 bien, 0 mal
```

#### Solución de referencia

```c
/* Mision 3 - Primero las pruebas: normalizar un nombre (sin espacios de mas, Mayuscula Inicial). */
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

/* Un mini framework de tests: cuenta las pruebas y muestra las que fallan con su linea. */
static int pruebas = 0, fallas = 0;

#define VERIFICAR(condicion)                                                   \
    do {                                                                       \
        pruebas++;                                                             \
        if (!(condicion)) {                                                    \
            fallas++;                                                          \
            printf("  FALLA %s:%d: %s\n", __FILE__, __LINE__, #condicion);     \
        }                                                                      \
    } while (0)

#define RESUMEN()                                                              \
    (printf("%d pruebas: %d bien, %d mal\n", pruebas, pruebas - fallas, fallas), fallas == 0 ? 0 : 1)

/* Escribe en salida el nombre normalizado. Devuelve false si no entra en tam. */
bool normalizar(const char *nombre, char *salida, size_t tam)
{
    size_t k = 0;
    bool inicio = true;
    for (size_t i = 0; nombre[i] != '\0'; i++) {
        unsigned char c = (unsigned char) nombre[i];
        if (isspace(c)) {
            inicio = true;
            continue;
        }
        if (inicio && k > 0) {
            if (k + 1 >= tam) {
                return false;
            }
            salida[k++] = ' ';
        }
        if (k + 1 >= tam) {
            return false;
        }
        salida[k++] = (char) (inicio ? toupper(c) : tolower(c));
        inicio = false;
    }
    salida[k] = '\0';
    return true;
}

#define PROBAR(entrada, esperado)                                              \
    do {                                                                       \
        char s[32];                                                            \
        VERIFICAR(normalizar(entrada, s, sizeof s) && strcmp(s, esperado) == 0); \
    } while (0)

int main(void)
{
    PROBAR("kira", "Kira");
    PROBAR("  bRON   el   enano ", "Bron El Enano");
    PROBAR("MIA", "Mia");
    PROBAR("", "");
    PROBAR("   ", "");
    char chico[5];
    VERIFICAR(!normalizar("Maese Ferrum", chico, sizeof chico));   /* no entra: avisa */
    return RESUMEN();
}
```

### Encargo R05-N02-E1 · Las pruebas del cajero

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El banco del Gremio no confía en un cajero sin pruebas. Con una `Cuenta` en **centavos** (`long long`) y la cantidad de movimientos, escribí `depositar`, `extraer` y `transferir` (solo deposita si pudo extraer) y una prueba por cada regla: montos no positivos, saldo insuficiente (que no cambie nada), extraer justo todo, transferir sin saldo (que el destino no reciba) y la cuenta de movimientos.

#### Criterio de aprobación

- Una prueba por regla, incluidos los casos que deben fallar.
- Verifica que un intento fallido no cambie nada.
- Pasan todas.

#### Salida esperada

```
7 pruebas: 7 bien, 0 mal
```

#### Solución de referencia

```c
/* Encargo - Las pruebas del cajero: cada regla del negocio, una prueba. */
#include <stdio.h>
#include <stdbool.h>

/* Un mini framework de tests: cuenta las pruebas y muestra las que fallan con su linea. */
static int pruebas = 0, fallas = 0;

#define VERIFICAR(condicion)                                                   \
    do {                                                                       \
        pruebas++;                                                             \
        if (!(condicion)) {                                                    \
            fallas++;                                                          \
            printf("  FALLA %s:%d: %s\n", __FILE__, __LINE__, #condicion);     \
        }                                                                      \
    } while (0)

#define RESUMEN()                                                              \
    (printf("%d pruebas: %d bien, %d mal\n", pruebas, pruebas - fallas, fallas), fallas == 0 ? 0 : 1)

typedef struct {
    long long centavos;
    int movimientos;
} Cuenta;

bool depositar(Cuenta *c, long long monto)
{
    if (monto <= 0) {
        return false;
    }
    c->centavos += monto;
    c->movimientos++;
    return true;
}

bool extraer(Cuenta *c, long long monto)
{
    if (monto <= 0 || monto > c->centavos) {
        return false;
    }
    c->centavos -= monto;
    c->movimientos++;
    return true;
}

bool transferir(Cuenta *origen, Cuenta *destino, long long monto)
{
    return extraer(origen, monto) && depositar(destino, monto);
}

int main(void)
{
    Cuenta a = { 100000, 0 }, b = { 0, 0 };
    VERIFICAR(depositar(&a, 5000) && a.centavos == 105000);
    VERIFICAR(!depositar(&a, 0) && !depositar(&a, -10));
    VERIFICAR(!extraer(&a, 200000) && a.centavos == 105000);     /* no alcanza: no cambia nada */
    VERIFICAR(extraer(&a, 105000) && a.centavos == 0);           /* justo todo */
    VERIFICAR(!transferir(&a, &b, 1) && b.centavos == 0);        /* sin saldo: el destino no recibe */
    depositar(&a, 3000);
    VERIFICAR(transferir(&a, &b, 3000) && a.centavos == 0 && b.centavos == 3000);
    VERIFICAR(a.movimientos == 4 && b.movimientos == 1);
    return RESUMEN();
}
```

### Prueba del sello

#### ¿Qué ventaja tiene una prueba automática sobre probar a mano?

Se ejecuta en segundos y siempre igual, cada vez que se cambia el código: detecta enseguida si algo que andaba se rompió.

#### ¿Cuándo se usa `assert` y cuándo una validación con `if`?

`assert` para lo que nunca debería pasar si el programa está bien escrito (errores de programación). Lo que viene del usuario o de un archivo se valida con `if`.

#### ¿Qué hace `#condicion` dentro de una macro?

Convierte el argumento en un texto: sirve para mostrar qué condición falló.

#### Nombrá cuatro casos límite para una función que busca el máximo de un array.

Un solo elemento, todos negativos, el máximo en la primera posición y el máximo en la última (y el array vacío, que debería rechazarse).

#### ¿Por qué `assert(depositar(&c, 100));` es un error?

Porque con `-DNDEBUG` los `assert` se eliminan, y con ellos el depósito.

### Soluciones (docente)

Unidad nueva (planificada como 27). El ejemplo tiene una prueba que falla a propósito: su salida lo muestra.

## R05-N03 · Proyecto: la agenda del Gremio

```meta
tipo: tema
padre: R05-N02
precio: 10
criatura: orco
```

### Crónica

Antes del último desafío, el Gremio te pide un favor que no tiene nada de mágico: sus comerciantes pierden los contactos de proveedores anotados en papelitos. Quieren una **agenda** que no se pierda, que busque rápido y que no acepte teléfonos con letras.

—No todo lo que se forja es una espada, {heroe} —dice {mentor}—. Las herramientas que usa la gente todos los días también se forjan. Y se forjan con el mismo cuidado.

### Objetivos

- Construir un programa útil fuera de los juegos, de punta a punta.
- Combinar memoria dinámica, textos, archivos CSV, búsqueda y orden con `qsort`.
- Validar los datos antes de guardarlos.

### Antes de empezar

- Strings (11), array dinámico (R03-N02), archivos de texto (R04-N01) y punteros a función (R03-N04).
- Tests (R05-N02), para probar las validaciones.

### Explicación

#### El plan

La agenda es un **array dinámico** de `Contacto` (nombre, teléfono, email). Se maneja con órdenes, una por línea:

```
agregar Ana Paz;380 4556677;ana@correo.ar
listar
buscar ana
borrar Ana Paz
guardar
```

Al empezar, se carga `agenda.csv` (si existe); con `guardar` (y al salir) se escribe. Así los contactos sobreviven entre ejecuciones.

#### Leer campos con espacios

El nombre puede tener espacios (`Ana Paz`), así que no sirve `%s`. Con el separador `;`:

```c
sscanf(texto, "%39[^;];%19[^;];%49s", c.nombre, c.telefono, c.email)
```

#### Buscar sin importar mayúsculas

`strstr` busca un texto dentro de otro, pero distingue mayúsculas. Para que `ana` encuentre a `Ana Paz`, se compara carácter por carácter con `tolower`.

#### Validar antes de guardar

Un dato mal cargado es peor que un dato que falta. Reglas simples, cada una en su función (y fáciles de probar con el mini framework del nodo anterior):

- **Teléfono**: solo dígitos, espacios o guiones (y un `+` al principio), con al menos 6 dígitos.
- **Email**: exactamente una `@`, algo antes, y un punto después de la `@`.
- **Nombre**: que no se repita.

### Código de ejemplo

```c
/*
 * 29 - La agenda del Gremio: contactos en memoria dinamica, ordenes por linea
 * y un archivo CSV para que no se pierdan.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

#define RUTA "agenda.csv"

typedef struct {
    char nombre[40];
    char telefono[20];
    char email[50];
} Contacto;

typedef struct {
    Contacto *datos;
    int cantidad, capacidad;
} Agenda;

static bool agregar(Agenda *a, const Contacto *c)
{
    if (a->cantidad == a->capacidad) {
        int nueva = a->capacidad ? a->capacidad * 2 : 4;
        Contacto *tmp = realloc(a->datos, nueva * sizeof *tmp);
        if (tmp == NULL) {
            return false;
        }
        a->datos = tmp;
        a->capacidad = nueva;
    }
    a->datos[a->cantidad++] = *c;
    return true;
}

static int por_nombre(const void *x, const void *y)
{
    return strcmp(((const Contacto *) x)->nombre, ((const Contacto *) y)->nombre);
}

static void listar(Agenda *a)
{
    qsort(a->datos, a->cantidad, sizeof a->datos[0], por_nombre);
    for (int i = 0; i < a->cantidad; i++) {
        printf("  %-16s %-14s %s\n", a->datos[i].nombre, a->datos[i].telefono, a->datos[i].email);
    }
    printf("  (%d contactos)\n", a->cantidad);
}

static bool guardar(const Agenda *a)
{
    FILE *f = fopen(RUTA, "w");
    if (f == NULL) {
        return false;
    }
    for (int i = 0; i < a->cantidad; i++) {
        fprintf(f, "%s;%s;%s\n", a->datos[i].nombre, a->datos[i].telefono, a->datos[i].email);
    }
    return fclose(f) == 0;
}

static void cargar(Agenda *a)
{
    FILE *f = fopen(RUTA, "r");
    if (f == NULL) {
        return;                                  /* primera vez: agenda vacia */
    }
    char linea[150];
    Contacto c;
    while (fgets(linea, sizeof(linea), f) != NULL) {
        if (sscanf(linea, "%39[^;];%19[^;];%49[^\n]", c.nombre, c.telefono, c.email) == 3) {
            agregar(a, &c);
        }
    }
    fclose(f);
}

int main(void)
{
    Agenda agenda = { NULL, 0, 0 };
    remove(RUTA);                                /* para que la prueba arranque igual */
    cargar(&agenda);

    char linea[150];
    while (fgets(linea, sizeof(linea), stdin) != NULL) {
        linea[strcspn(linea, "\n")] = '\0';
        printf("> %s\n", linea);
        Contacto c;
        if (strncmp(linea, "agregar ", 8) == 0) {
            if (sscanf(linea + 8, "%39[^;];%19[^;];%49s", c.nombre, c.telefono, c.email) == 3) {
                printf("  %s\n", agregar(&agenda, &c) ? "Agregado." : "Sin memoria.");
            } else {
                printf("  Uso: agregar Nombre;Telefono;email\n");
            }
        } else if (strcmp(linea, "listar") == 0) {
            listar(&agenda);
        } else if (strcmp(linea, "guardar") == 0) {
            printf("  %s\n", guardar(&agenda) ? "Guardado." : "No se pudo guardar.");
        } else {
            printf("  Órdenes: agregar, listar, guardar\n");
        }
    }

    /* Se guarda, se libera todo y se vuelve a cargar: la agenda sobrevive. */
    guardar(&agenda);
    free(agenda.datos);
    Agenda otra = { NULL, 0, 0 };
    cargar(&otra);
    printf("Al volver a abrir: %d contactos.\n", otra.cantidad);
    free(otra.datos);
    remove(RUTA);
    return 0;
}
```

### Entrada de ejemplo

```
agregar Ferrum;380 4001122;ferrum@forja.ar
agregar Ana Paz;380 4556677;ana@correo.ar
agregar incompleto
listar
guardar
```

### Salida esperada

```
> agregar Ferrum;380 4001122;ferrum@forja.ar
  Agregado.
> agregar Ana Paz;380 4556677;ana@correo.ar
  Agregado.
> agregar incompleto
  Uso: agregar Nombre;Telefono;email
> listar
  Ana Paz          380 4556677    ana@correo.ar
  Ferrum           380 4001122    ferrum@forja.ar
  (2 contactos)
> guardar
  Guardado.
Al volver a abrir: 2 contactos.
```

### ¿Para qué sirve?

Es el tipo de programa que se escribe en cualquier trabajo: un registro de clientes, una lista de socios, un padrón de alumnos, el control de turnos de un consultorio. La combinación de datos en memoria, un archivo para guardarlos, búsqueda y validación es la base de los sistemas de gestión, y la misma idea escala a las bases de datos que usan los sistemas grandes.

### Errores habituales

- **Goblin**: `%s` para el nombre corta en el primer espacio: `Ana Paz` queda como `Ana` y el resto se mezcla con el teléfono.
- **Orco**: sin ancho en `%[^;]`, un nombre larguísimo desborda el array.
- **Ogro**: buscar con `strcmp` en lugar de "contiene": `buscar ana` no encuentra a `Ana Paz`.
- **Ogro**: `borrar` que no corre los contactos de atrás: queda un hueco con datos viejos.
- **Troll**: olvidar liberar el array al salir.
- **Ogro**: aceptar `hola` como teléfono porque "después se corrige".

### Misión R05-N03-M1 · La agenda que no se pierde

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí la agenda base: un array dinámico de `Contacto` y las órdenes `agregar Nombre;Telefono;email`, `listar` (ordenada por nombre con `qsort`, con la cantidad) y `guardar` (a `agenda.csv`). Mostrá cada orden con `> ` antes de procesarla y avisá las órdenes mal escritas. Al terminar la entrada, guardá, liberá todo, volvé a cargar el archivo en otra agenda y mostrá cuántos contactos tiene (así se comprueba que sobreviven).

#### Criterio de aprobación

- Array dinámico que crece; los nombres pueden tener espacios.
- Lista ordenada por nombre con `qsort`.
- Guarda y carga `agenda.csv`; libera la memoria.

#### Entrada de ejemplo

```
agregar Ferrum;380 4001122;ferrum@forja.ar
agregar Ana Paz;380 4556677;ana@correo.ar
agregar Bron;380 4223344;bron@forja.ar
agregar sin datos
listar
guardar
hola
```

#### Salida esperada

```
> agregar Ferrum;380 4001122;ferrum@forja.ar
  Agregado.
> agregar Ana Paz;380 4556677;ana@correo.ar
  Agregado.
> agregar Bron;380 4223344;bron@forja.ar
  Agregado.
> agregar sin datos
  Uso: agregar Nombre;Telefono;email
> listar
  Ana Paz          380 4556677    ana@correo.ar
  Bron             380 4223344    bron@forja.ar
  Ferrum           380 4001122    ferrum@forja.ar
  (3 contactos)
> guardar
  Guardado.
> hola
  Órdenes: agregar, listar, guardar
Al volver a abrir: 3 contactos.
```

#### Solución de referencia

```c
/*
 * 29 - La agenda del Gremio: contactos en memoria dinamica, ordenes por linea
 * y un archivo CSV para que no se pierdan.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

#define RUTA "agenda.csv"

typedef struct {
    char nombre[40];
    char telefono[20];
    char email[50];
} Contacto;

typedef struct {
    Contacto *datos;
    int cantidad, capacidad;
} Agenda;

static bool agregar(Agenda *a, const Contacto *c)
{
    if (a->cantidad == a->capacidad) {
        int nueva = a->capacidad ? a->capacidad * 2 : 4;
        Contacto *tmp = realloc(a->datos, nueva * sizeof *tmp);
        if (tmp == NULL) {
            return false;
        }
        a->datos = tmp;
        a->capacidad = nueva;
    }
    a->datos[a->cantidad++] = *c;
    return true;
}

static int por_nombre(const void *x, const void *y)
{
    return strcmp(((const Contacto *) x)->nombre, ((const Contacto *) y)->nombre);
}

static void listar(Agenda *a)
{
    qsort(a->datos, a->cantidad, sizeof a->datos[0], por_nombre);
    for (int i = 0; i < a->cantidad; i++) {
        printf("  %-16s %-14s %s\n", a->datos[i].nombre, a->datos[i].telefono, a->datos[i].email);
    }
    printf("  (%d contactos)\n", a->cantidad);
}

static bool guardar(const Agenda *a)
{
    FILE *f = fopen(RUTA, "w");
    if (f == NULL) {
        return false;
    }
    for (int i = 0; i < a->cantidad; i++) {
        fprintf(f, "%s;%s;%s\n", a->datos[i].nombre, a->datos[i].telefono, a->datos[i].email);
    }
    return fclose(f) == 0;
}

static void cargar(Agenda *a)
{
    FILE *f = fopen(RUTA, "r");
    if (f == NULL) {
        return;                                  /* primera vez: agenda vacia */
    }
    char linea[150];
    Contacto c;
    while (fgets(linea, sizeof(linea), f) != NULL) {
        if (sscanf(linea, "%39[^;];%19[^;];%49[^\n]", c.nombre, c.telefono, c.email) == 3) {
            agregar(a, &c);
        }
    }
    fclose(f);
}

int main(void)
{
    Agenda agenda = { NULL, 0, 0 };
    remove(RUTA);                                /* para que la prueba arranque igual */
    cargar(&agenda);

    char linea[150];
    while (fgets(linea, sizeof(linea), stdin) != NULL) {
        linea[strcspn(linea, "\n")] = '\0';
        printf("> %s\n", linea);
        Contacto c;
        if (strncmp(linea, "agregar ", 8) == 0) {
            if (sscanf(linea + 8, "%39[^;];%19[^;];%49s", c.nombre, c.telefono, c.email) == 3) {
                printf("  %s\n", agregar(&agenda, &c) ? "Agregado." : "Sin memoria.");
            } else {
                printf("  Uso: agregar Nombre;Telefono;email\n");
            }
        } else if (strcmp(linea, "listar") == 0) {
            listar(&agenda);
        } else if (strcmp(linea, "guardar") == 0) {
            printf("  %s\n", guardar(&agenda) ? "Guardado." : "No se pudo guardar.");
        } else {
            printf("  Órdenes: agregar, listar, guardar\n");
        }
    }

    /* Se guarda, se libera todo y se vuelve a cargar: la agenda sobrevive. */
    guardar(&agenda);
    free(agenda.datos);
    Agenda otra = { NULL, 0, 0 };
    cargar(&otra);
    printf("Al volver a abrir: %d contactos.\n", otra.cantidad);
    free(otra.datos);
    remove(RUTA);
    return 0;
}
```

### Misión R05-N03-M2 · Buscar, borrar y validar

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Agregale a la agenda:

- `buscar texto`: muestra los contactos cuyo nombre **o** email contiene el texto, sin importar mayúsculas (o avisa que no hay).
- `borrar Nombre`: borra el contacto con ese nombre exacto (o avisa que no existe).
- Validaciones al agregar: nombre repetido, teléfono (solo dígitos, espacios, guiones y un `+` inicial; al menos 6 dígitos) y email (una `@` con algo antes y un punto después).

#### Criterio de aprobación

- Busca sin importar mayúsculas, en nombre y email.
- Borra corriendo los de atrás.
- Rechaza nombres repetidos, teléfonos y emails inválidos con un mensaje claro.

#### Código inicial

```c
/*
 * 29 - La agenda del Gremio: contactos en memoria dinamica, ordenes por linea
 * y un archivo CSV para que no se pierdan.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

#define RUTA "agenda.csv"

typedef struct {
    char nombre[40];
    char telefono[20];
    char email[50];
} Contacto;

typedef struct {
    Contacto *datos;
    int cantidad, capacidad;
} Agenda;

static bool agregar(Agenda *a, const Contacto *c)
{
    if (a->cantidad == a->capacidad) {
        int nueva = a->capacidad ? a->capacidad * 2 : 4;
        Contacto *tmp = realloc(a->datos, nueva * sizeof *tmp);
        if (tmp == NULL) {
            return false;
        }
        a->datos = tmp;
        a->capacidad = nueva;
    }
    a->datos[a->cantidad++] = *c;
    return true;
}

static int por_nombre(const void *x, const void *y)
{
    return strcmp(((const Contacto *) x)->nombre, ((const Contacto *) y)->nombre);
}

static void listar(Agenda *a)
{
    qsort(a->datos, a->cantidad, sizeof a->datos[0], por_nombre);
    for (int i = 0; i < a->cantidad; i++) {
        printf("  %-16s %-14s %s\n", a->datos[i].nombre, a->datos[i].telefono, a->datos[i].email);
    }
    printf("  (%d contactos)\n", a->cantidad);
}

static bool guardar(const Agenda *a)
{
    FILE *f = fopen(RUTA, "w");
    if (f == NULL) {
        return false;
    }
    for (int i = 0; i < a->cantidad; i++) {
        fprintf(f, "%s;%s;%s\n", a->datos[i].nombre, a->datos[i].telefono, a->datos[i].email);
    }
    return fclose(f) == 0;
}

static void cargar(Agenda *a)
{
    FILE *f = fopen(RUTA, "r");
    if (f == NULL) {
        return;                                  /* primera vez: agenda vacia */
    }
    char linea[150];
    Contacto c;
    while (fgets(linea, sizeof(linea), f) != NULL) {
        if (sscanf(linea, "%39[^;];%19[^;];%49[^\n]", c.nombre, c.telefono, c.email) == 3) {
            agregar(a, &c);
        }
    }
    fclose(f);
}

int main(void)
{
    Agenda agenda = { NULL, 0, 0 };
    remove(RUTA);                                /* para que la prueba arranque igual */
    cargar(&agenda);

    char linea[150];
    while (fgets(linea, sizeof(linea), stdin) != NULL) {
        linea[strcspn(linea, "\n")] = '\0';
        printf("> %s\n", linea);
        Contacto c;
        if (strncmp(linea, "agregar ", 8) == 0) {
            if (sscanf(linea + 8, "%39[^;];%19[^;];%49s", c.nombre, c.telefono, c.email) == 3) {
                printf("  %s\n", agregar(&agenda, &c) ? "Agregado." : "Sin memoria.");
            } else {
                printf("  Uso: agregar Nombre;Telefono;email\n");
            }
        } else if (strcmp(linea, "listar") == 0) {
            listar(&agenda);
        } else if (strcmp(linea, "guardar") == 0) {
            printf("  %s\n", guardar(&agenda) ? "Guardado." : "No se pudo guardar.");
        } else {
            printf("  Órdenes: agregar, listar, guardar\n");
        }
    }

    /* Se guarda, se libera todo y se vuelve a cargar: la agenda sobrevive. */
    guardar(&agenda);
    free(agenda.datos);
    Agenda otra = { NULL, 0, 0 };
    cargar(&otra);
    printf("Al volver a abrir: %d contactos.\n", otra.cantidad);
    free(otra.datos);
    remove(RUTA);
    return 0;
}
```

#### Entrada de ejemplo

```
agregar Ferrum;380 4001122;ferrum@forja.ar
agregar Ana Paz;380 4556677;ana@correo.ar
agregar Ana Paz;380 111222;otra@correo.ar
agregar Zed;llamame;zed@sombras.ar
agregar Mia;380 4889900;mia.torre
agregar Bron;+54 380 4223344;bron@forja.ar
buscar FORJA
buscar ana
buscar dragon
borrar Ferrum
borrar Ferrum
listar
```

#### Salida esperada

```
> agregar Ferrum;380 4001122;ferrum@forja.ar
  Agregado.
> agregar Ana Paz;380 4556677;ana@correo.ar
  Agregado.
> agregar Ana Paz;380 111222;otra@correo.ar
  Ya hay un contacto llamado Ana Paz.
> agregar Zed;llamame;zed@sombras.ar
  Teléfono inválido: llamame
> agregar Mia;380 4889900;mia.torre
  Email inválido: mia.torre
> agregar Bron;+54 380 4223344;bron@forja.ar
  Agregado.
> buscar FORJA
  Ferrum           380 4001122    ferrum@forja.ar
  Bron             +54 380 4223344 bron@forja.ar
> buscar ana
  Ana Paz          380 4556677    ana@correo.ar
> buscar dragon
  No hay coincidencias para "dragon".
> borrar Ferrum
  Borrado.
> borrar Ferrum
  No existe ese contacto.
> listar
  Ana Paz          380 4556677    ana@correo.ar
  Bron             +54 380 4223344 bron@forja.ar
  (2 contactos)
Al volver a abrir: 2 contactos.
```

#### Solución de referencia

```c
/*
 * Mision 2 - Buscar, borrar y validar: la agenda ya no acepta cualquier cosa.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

#define RUTA "agenda.csv"

typedef struct {
    char nombre[40];
    char telefono[20];
    char email[50];
} Contacto;

typedef struct {
    Contacto *datos;
    int cantidad, capacidad;
} Agenda;

static bool agregar(Agenda *a, const Contacto *c)
{
    if (a->cantidad == a->capacidad) {
        int nueva = a->capacidad ? a->capacidad * 2 : 4;
        Contacto *tmp = realloc(a->datos, nueva * sizeof *tmp);
        if (tmp == NULL) {
            return false;
        }
        a->datos = tmp;
        a->capacidad = nueva;
    }
    a->datos[a->cantidad++] = *c;
    return true;
}

/* Busqueda sin importar mayusculas: devuelve true si "parte" aparece dentro de "texto". */
static bool contiene_sin_mayusculas(const char *texto, const char *parte)
{
    size_t n = strlen(texto), m = strlen(parte);
    for (size_t i = 0; i + m <= n; i++) {
        size_t k = 0;
        while (k < m && tolower((unsigned char) texto[i + k]) == tolower((unsigned char) parte[k])) {
            k++;
        }
        if (k == m) {
            return true;
        }
    }
    return false;
}

static int buscar_nombre(const Agenda *a, const char *nombre)
{
    for (int i = 0; i < a->cantidad; i++) {
        if (strcmp(a->datos[i].nombre, nombre) == 0) {
            return i;
        }
    }
    return -1;
}

static void buscar(const Agenda *a, const char *parte)
{
    int encontrados = 0;
    for (int i = 0; i < a->cantidad; i++) {
        if (contiene_sin_mayusculas(a->datos[i].nombre, parte) || contiene_sin_mayusculas(a->datos[i].email, parte)) {
            printf("  %-16s %-14s %s\n", a->datos[i].nombre, a->datos[i].telefono, a->datos[i].email);
            encontrados++;
        }
    }
    if (encontrados == 0) {
        printf("  No hay coincidencias para \"%s\".\n", parte);
    }
}

static bool borrar(Agenda *a, const char *nombre)
{
    int i = buscar_nombre(a, nombre);
    if (i < 0) {
        return false;
    }
    for (int k = i; k < a->cantidad - 1; k++) {
        a->datos[k] = a->datos[k + 1];
    }
    a->cantidad--;
    return true;
}

/* Telefono: solo digitos, espacios, guiones o + al principio; al menos 6 digitos. Email: algo@algo.algo */
static bool telefono_valido(const char *t)
{
    int digitos = 0;
    for (int i = 0; t[i]; i++) {
        if (isdigit((unsigned char) t[i])) {
            digitos++;
        } else if (!(t[i] == ' ' || t[i] == '-' || (t[i] == '+' && i == 0))) {
            return false;
        }
    }
    return digitos >= 6;
}

static bool email_valido(const char *e)
{
    const char *arroba = strchr(e, '@');
    return arroba != NULL && arroba != e && strchr(arroba + 1, '@') == NULL && strchr(arroba + 1, '.') != NULL
           && e[strlen(e) - 1] != '.';
}

static int por_nombre(const void *x, const void *y)
{
    return strcmp(((const Contacto *) x)->nombre, ((const Contacto *) y)->nombre);
}

static void listar(Agenda *a)
{
    qsort(a->datos, a->cantidad, sizeof a->datos[0], por_nombre);
    for (int i = 0; i < a->cantidad; i++) {
        printf("  %-16s %-14s %s\n", a->datos[i].nombre, a->datos[i].telefono, a->datos[i].email);
    }
    printf("  (%d contactos)\n", a->cantidad);
}

static bool guardar(const Agenda *a)
{
    FILE *f = fopen(RUTA, "w");
    if (f == NULL) {
        return false;
    }
    for (int i = 0; i < a->cantidad; i++) {
        fprintf(f, "%s;%s;%s\n", a->datos[i].nombre, a->datos[i].telefono, a->datos[i].email);
    }
    return fclose(f) == 0;
}

static void cargar(Agenda *a)
{
    FILE *f = fopen(RUTA, "r");
    if (f == NULL) {
        return;                                  /* primera vez: agenda vacia */
    }
    char linea[150];
    Contacto c;
    while (fgets(linea, sizeof(linea), f) != NULL) {
        if (sscanf(linea, "%39[^;];%19[^;];%49[^\n]", c.nombre, c.telefono, c.email) == 3) {
            agregar(a, &c);
        }
    }
    fclose(f);
}

int main(void)
{
    Agenda agenda = { NULL, 0, 0 };
    remove(RUTA);                                /* para que la prueba arranque igual */
    cargar(&agenda);

    char linea[150];
    while (fgets(linea, sizeof(linea), stdin) != NULL) {
        linea[strcspn(linea, "\n")] = '\0';
        printf("> %s\n", linea);
        Contacto c;
        if (strncmp(linea, "agregar ", 8) == 0) {
            if (sscanf(linea + 8, "%39[^;];%19[^;];%49s", c.nombre, c.telefono, c.email) != 3) {
                printf("  Uso: agregar Nombre;Telefono;email\n");
            } else if (buscar_nombre(&agenda, c.nombre) >= 0) {
                printf("  Ya hay un contacto llamado %s.\n", c.nombre);
            } else if (!telefono_valido(c.telefono)) {
                printf("  Teléfono inválido: %s\n", c.telefono);
            } else if (!email_valido(c.email)) {
                printf("  Email inválido: %s\n", c.email);
            } else {
                printf("  %s\n", agregar(&agenda, &c) ? "Agregado." : "Sin memoria.");
            }
        } else if (strncmp(linea, "buscar ", 7) == 0) {
            buscar(&agenda, linea + 7);
        } else if (strncmp(linea, "borrar ", 7) == 0) {
            printf("  %s\n", borrar(&agenda, linea + 7) ? "Borrado." : "No existe ese contacto.");
        } else if (strcmp(linea, "listar") == 0) {
            listar(&agenda);
        } else if (strcmp(linea, "guardar") == 0) {
            printf("  %s\n", guardar(&agenda) ? "Guardado." : "No se pudo guardar.");
        } else {
            printf("  Órdenes: agregar, buscar, borrar, listar, guardar\n");
        }
    }

    guardar(&agenda);
    free(agenda.datos);
    Agenda otra = { NULL, 0, 0 };
    cargar(&otra);
    printf("Al volver a abrir: %d contactos.\n", otra.cantidad);
    free(otra.datos);
    remove(RUTA);
    return 0;
}
```

### Misión R05-N03-M3 · Ordenar por cualquier campo

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con cuatro contactos que además tienen el mes de cumpleaños, escribí tres comparadores (por nombre, por email y por mes de cumpleaños, desempatando por nombre) en una **tabla** `{ campo, función }`. Por cada línea de la entrada (`nombre`, `email`, `cumple`), ordená con el comparador de ese campo y mostrá la lista; si el campo no existe, avisá.

#### Criterio de aprobación

- Tabla de comparadores elegidos por nombre de campo.
- El orden por cumpleaños desempata por nombre.
- Avisa los campos que no existen.

#### Entrada de ejemplo

```
cumple
email
telefono
nombre
```

#### Salida esperada

```
Por cumple:
  Ana Paz  ana@correo.ar    mes  3
  Mia Luz  mia@torre.ar     mes  3
  Bron     bron@forja.ar    mes  7
  Ferrum   ferrum@forja.ar  mes 11
Por email:
  Ana Paz  ana@correo.ar    mes  3
  Bron     bron@forja.ar    mes  7
  Ferrum   ferrum@forja.ar  mes 11
  Mia Luz  mia@torre.ar     mes  3
No se puede ordenar por "telefono" (nombre, email o cumple)
Por nombre:
  Ana Paz  ana@correo.ar    mes  3
  Bron     bron@forja.ar    mes  7
  Ferrum   ferrum@forja.ar  mes 11
  Mia Luz  mia@torre.ar     mes  3
```

#### Solución de referencia

```c
/* Mision 3 - Ordenar por cualquier campo: una tabla de comparadores elegida por nombre. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char nombre[40];
    char telefono[20];
    char email[50];
    int cumple_mes;
} Contacto;

static int por_nombre(const void *a, const void *b) { return strcmp(((const Contacto *) a)->nombre, ((const Contacto *) b)->nombre); }
static int por_email(const void *a, const void *b) { return strcmp(((const Contacto *) a)->email, ((const Contacto *) b)->email); }
static int por_cumple(const void *a, const void *b)
{
    const Contacto *x = a, *y = b;
    int d = x->cumple_mes - y->cumple_mes;
    return d != 0 ? d : strcmp(x->nombre, y->nombre);      /* desempate por nombre */
}

typedef struct {
    const char *campo;
    int (*comparar)(const void *, const void *);
} Orden;

static const Orden ORDENES[] = { { "nombre", por_nombre }, { "email", por_email }, { "cumple", por_cumple } };

int main(void)
{
    Contacto agenda[] = {
        { "Ferrum", "380 4001122", "ferrum@forja.ar", 11 },
        { "Ana Paz", "380 4556677", "ana@correo.ar", 3 },
        { "Bron", "380 4223344", "bron@forja.ar", 7 },
        { "Mia Luz", "380 4889900", "mia@torre.ar", 3 },
    };
    int n = sizeof(agenda) / sizeof(agenda[0]);
    char linea[40];
    while (fgets(linea, sizeof(linea), stdin) != NULL) {
        linea[strcspn(linea, "\n")] = '\0';
        const Orden *o = NULL;
        for (size_t i = 0; i < sizeof(ORDENES) / sizeof(ORDENES[0]); i++) {
            if (strcmp(ORDENES[i].campo, linea) == 0) {
                o = &ORDENES[i];
            }
        }
        if (o == NULL) {
            printf("No se puede ordenar por \"%s\" (nombre, email o cumple)\n", linea);
            continue;
        }
        qsort(agenda, n, sizeof agenda[0], o->comparar);
        printf("Por %s:\n", o->campo);
        for (int i = 0; i < n; i++) {
            printf("  %-8s %-16s mes %2d\n", agenda[i].nombre, agenda[i].email, agenda[i].cumple_mes);
        }
    }
    return 0;
}
```

### Encargo R05-N03-E1 · Las etiquetas del correo

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Para mandar cartas, el Gremio necesita etiquetas: cada destinatario (nombre, calle, ciudad) dentro de un recuadro de `+`, `-` y `|` que se ajusta al renglón más largo. Usá `%-*s` para que el ancho salga de una variable.

#### Criterio de aprobación

- El recuadro se ajusta al renglón más largo de cada etiqueta.
- Usa `%-*s` con el ancho calculado.

#### Salida esperada

```
+---------------------+
| Maese Ferrum        |
| Calle del Yunque 12 |
| Forjas de Hierro    |
+---------------------+
+----------------+
| Bron           |
| Pasaje Enano 3 |
| Montaña Gris  |
+----------------+
```

#### Solución de referencia

```c
/* Encargo - Las etiquetas del correo: cada contacto en un recuadro que se ajusta al texto mas largo. */
#include <stdio.h>
#include <string.h>

typedef struct {
    const char *nombre;
    const char *calle;
    const char *ciudad;
} Destinatario;

static void linea_horizontal(int ancho)
{
    putchar('+');
    for (int i = 0; i < ancho + 2; i++) {
        putchar('-');
    }
    printf("+\n");
}

static void etiqueta(const Destinatario *d)
{
    const char *renglones[] = { d->nombre, d->calle, d->ciudad };
    int ancho = 0;
    for (int i = 0; i < 3; i++) {
        int largo = (int) strlen(renglones[i]);
        if (largo > ancho) {
            ancho = largo;
        }
    }
    linea_horizontal(ancho);
    for (int i = 0; i < 3; i++) {
        printf("| %-*s |\n", ancho, renglones[i]);      /* el * toma el ancho de un argumento */
    }
    linea_horizontal(ancho);
}

int main(void)
{
    Destinatario lista[] = {
        { "Maese Ferrum", "Calle del Yunque 12", "Forjas de Hierro" },
        { "Bron", "Pasaje Enano 3", "Montaña Gris" },
    };
    for (int i = 0; i < 2; i++) {
        etiqueta(&lista[i]);
    }
    return 0;
}
```

### Prueba del sello

#### ¿Por qué la agenda se carga al empezar y se guarda al terminar?

Porque la memoria se pierde al cerrar el programa: el archivo es lo que hace que los contactos sobrevivan entre ejecuciones.

#### ¿Qué lee `%39[^;]` y por qué el 39?

Hasta 39 caracteres que no sean `;` (acepta espacios). El 39 deja lugar para el `'\0'` en un array de 40.

#### ¿Cómo se busca "ana" dentro de "Ana Paz" sin importar mayúsculas?

Comparando carácter por carácter con `tolower` desde cada posición posible del texto.

#### ¿Por qué conviene validar el teléfono en una función aparte?

Porque queda en un solo lugar, se puede probar sola con casos límite y se reutiliza.

#### Al borrar el contacto 2 de 5, ¿qué pasa con los contactos 3 y 4?

Se corren un lugar hacia adelante (al 2 y al 3) y la cantidad baja a 4.

### Soluciones (docente)

Proyecto nuevo, fuera de los juegos (en `02-C-Intermedio` estaba planificado como 29-ProyectoAgenda). Se trabaja con órdenes por la entrada en lugar de `argv` para poder probarlo con un archivo.

## R05-N04 · Jefe final: el Dragón bajo la Montaña

```meta
tipo: jefe
padre: R05-N03
precio: 10
criatura: dragon
insignia: Sello del Dragón de Hierro
insignia_descripcion: Venciste al Dragón bajo la Montaña: dominás C, de la primera línea a un programa completo.
```

### Crónica

Bajo las Forjas, más hondo que las Minas, duerme el **Dragón de Hierro**. Nadie baja a su mazmorra sin un mapa, sin fuerzas para los guardianes y sin una forma de volver si algo sale mal.

—Es la última prueba, {heroe} —dice {mentor}, y por primera vez no te da ninguna herramienta—. Todo lo que necesitás ya lo forjaste vos. Mapa, memoria, combate, archivos. Bajá.

### Objetivos

- Escribir un juego completo de consola, armado de a partes.
- Representar un mundo con una matriz de caracteres y el estado del juego en un struct.
- Sumar combate con azar controlado y guardado de la partida en binario.

### Antes de empezar

Todo el camino principal. Es el **proyecto final**: no hay teoría nueva.

### Explicación

#### El mundo es una matriz

```
#############      #  pared
#@..#...$...#      @  el héroe
#.#.#.###.#.#      $  tesoro
#.#...#$..#.#      S  salida
#.###.#.###.#      .  piso
#$........#S#
#############
```

Se guarda en `char mapa[FILAS][COLUMNAS + 1]` (el `+ 1` es para el `'\0'` de cada fila). La posición del héroe va **aparte** (fila y columna), así moverse no borra nada del mapa: se dibuja el `@` encima.

Como el borde es todo pared, antes de moverse alcanza con mirar la casilla de destino: nunca se sale de la matriz.

#### Todo el estado en un struct

```c
typedef struct {
    char mapa[FILAS][COLUMNAS + 1];
    int fila, columna, vida, oro, pasos;
    bool salio;
    Enemigo enemigos[MAX_ENEMIGOS];
    int cantidad_enemigos;
} Partida;
```

Si **todo** lo que cambia está en la `Partida`, guardar el juego es escribir un solo struct con `fwrite` (no tiene punteros: se puede guardar en binario tal cual).

#### Las tres misiones son una sola historia

Cada misión parte del código de la anterior:

1. **Explorar**: moverse, paredes, tesoros y salida.
2. **Los guardianes**: enemigos y combate por turnos.
3. **Guardar la partida**: `g` y `c`.

Probá cada una con un archivo de movimientos: `./programa < movimientos.txt`.

### ¿Para qué sirve?

Los *roguelikes* (juegos de mazmorras en una grilla) nacieron exactamente así, en la terminal y en C: *Rogue* (1980) y *NetHack* todavía se juegan. La misma estructura (un mundo en una matriz, entidades en arrays, un bucle de turnos y el estado en un struct que se guarda) es la base de los juegos de estrategia, los simuladores y los editores de mapas, y el algoritmo del encargo (búsqueda en anchura) es el que usan los GPS y los enemigos de los juegos para encontrar caminos.

### Errores habituales

El Dragón usa a todas las criaturas del camino:

- **Orco**: mirar `mapa[f][c]` sin controlar los límites (si el borde no fuera pared).
- **Ogro**: mover al héroe antes de ver si hay pared, o dejarlo avanzar después de perder un combate.
- **Troll**: guardar en binario un struct con punteros.
- **Ogro**: cargar pisando la partida antes de verificar la marca y la versión.
- **Goblin**: `int` y `char` mezclados al comparar casillas (`'#'` es un carácter, `"#"` es un texto).
- **Ogro**: un bucle que no termina cuando se acaba la entrada.

### Misión R05-N04-M1 · Explorar la mazmorra

```meta
entrega: codigo
entorno: local
monedas: 8
xp: 40
```

#### Consigna

Con el mapa de la explicación, escribí la exploración:

1. `iniciar` copia el mapa, busca el `@`, guarda su posición y deja un `.` en su lugar.
2. `dibujar` muestra el mapa con el `@` encima.
3. `mover(Partida *p, char comando)` mueve con `w`/`a`/`s`/`d`: las paredes frenan (`Pared.`), los tesoros suman 10 de oro y se borran del mapa, y la `S` termina la partida. Otro comando: `Usá w, a, s o d.`.
4. El bucle lee un comando por línea hasta salir o que se termine la entrada. Al final, dibujá el mapa y mostrá pasos y oro.

#### Criterio de aprobación

- El mapa es una matriz de caracteres y la posición del héroe va aparte.
- Las paredes frenan, los tesoros se juntan una sola vez.
- Termina al salir o cuando se acaba la entrada.

#### Entrada de ejemplo

```
w
d
d
s
s
d
d
x
w
w
d
d
d
d
d
d
s
s
s
s
```

#### Salida esperada

```
#############
#@..#...$...#
#.#.#.###.#.#
#.#...#$..#.#
#.###.#.###.#
#$........#S#
#############
  Pared.
  Usá w, a, s o d.
  ¡Tesoro! Oro: 10
#############
#...#.......#
#.#.#.###.#.#
#.#...#$..#.#
#.###.#.###.#
#$........#@#
#############
¡Encontraste la salida! Pasos: 18. Oro: 10.
```

#### Solución de referencia

```c
/*
 * Jefe final - Mision 1: explorar la mazmorra.
 * Mapa en una matriz de caracteres; w/a/s/d mueven; las paredes frenan,
 * los tesoros se juntan y la S es la salida.
 */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define FILAS 7
#define COLUMNAS 13

static const char *MAPA_INICIAL[FILAS] = {
    "#############",
    "#@..#...$...#",
    "#.#.#.###.#.#",
    "#.#...#$..#.#",
    "#.###.#.###.#",
    "#$........#S#",
    "#############",
};

typedef struct {
    char mapa[FILAS][COLUMNAS + 1];
    int fila, columna;          /* donde esta el heroe */
    int oro, pasos;
    bool salio;
} Partida;

void iniciar(Partida *p)
{
    for (int f = 0; f < FILAS; f++) {
        strcpy(p->mapa[f], MAPA_INICIAL[f]);
        char *arroba = strchr(p->mapa[f], '@');
        if (arroba != NULL) {
            p->fila = f;
            p->columna = (int) (arroba - p->mapa[f]);
            *arroba = '.';                          /* el heroe no es parte del mapa */
        }
    }
    p->oro = p->pasos = 0;
    p->salio = false;
}

void dibujar(const Partida *p)
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            putchar(f == p->fila && c == p->columna ? '@' : p->mapa[f][c]);
        }
        putchar('\n');
    }
}

/* Mueve si se puede. Devuelve false si el comando no es un movimiento. */
bool mover(Partida *p, char comando)
{
    int df = 0, dc = 0;
    switch (comando) {
    case 'w': df = -1; break;
    case 's': df = 1; break;
    case 'a': dc = -1; break;
    case 'd': dc = 1; break;
    default: return false;
    }
    char destino = p->mapa[p->fila + df][p->columna + dc];   /* el borde es pared: nunca se sale */
    if (destino == '#') {
        printf("  Pared.\n");
        return true;
    }
    p->fila += df;
    p->columna += dc;
    p->pasos++;
    if (destino == '$') {
        p->oro += 10;
        p->mapa[p->fila][p->columna] = '.';
        printf("  ¡Tesoro! Oro: %d\n", p->oro);
    } else if (destino == 'S') {
        p->salio = true;
    }
    return true;
}

int main(void)
{
    Partida p;
    iniciar(&p);
    dibujar(&p);
    char linea[20];
    while (!p.salio && fgets(linea, sizeof(linea), stdin) != NULL) {
        if (!mover(&p, linea[0])) {
            printf("  Usá w, a, s o d.\n");
        }
    }
    dibujar(&p);
    printf("%s Pasos: %d. Oro: %d.\n", p.salio ? "¡Encontraste la salida!" : "Te quedaste en la oscuridad.", p.pasos, p.oro);
    return 0;
}
```

### Misión R05-N04-M2 · Los guardianes

```meta
entrega: codigo
entorno: local
monedas: 8
xp: 40
```

#### Consigna

Partiendo de la misión anterior, agregá los guardianes:

1. Un `Enemigo` (nombre, fila, columna, vida, ataque) y un array de enemigos en la `Partida`: un Goblin en (3, 4) con 14 de vida y 4 de ataque, y el **Dragón** en (1, 11) con 30 de vida y 7 de ataque. Se dibujan como `E`.
2. El héroe empieza con 40 de vida. Entrar en la casilla de un enemigo vivo empieza un **combate por rondas** (`srand(30)`): el héroe pega de 5 a 10; si el enemigo sigue vivo, pega entre su ataque − 2 y su ataque + 2.
3. Si el héroe gana, avanza; si pierde, la partida termina.

#### Criterio de aprobación

- Los enemigos están en un array dentro de la `Partida`.
- El combate es una función con rondas y azar con semilla fija.
- El héroe no avanza si pierde; los enemigos caídos no se dibujan.

#### Código inicial

```c
/*
 * Jefe final - Mision 1: explorar la mazmorra.
 * Mapa en una matriz de caracteres; w/a/s/d mueven; las paredes frenan,
 * los tesoros se juntan y la S es la salida.
 */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define FILAS 7
#define COLUMNAS 13

static const char *MAPA_INICIAL[FILAS] = {
    "#############",
    "#@..#...$...#",
    "#.#.#.###.#.#",
    "#.#...#$..#.#",
    "#.###.#.###.#",
    "#$........#S#",
    "#############",
};

typedef struct {
    char mapa[FILAS][COLUMNAS + 1];
    int fila, columna;          /* donde esta el heroe */
    int oro, pasos;
    bool salio;
} Partida;

void iniciar(Partida *p)
{
    for (int f = 0; f < FILAS; f++) {
        strcpy(p->mapa[f], MAPA_INICIAL[f]);
        char *arroba = strchr(p->mapa[f], '@');
        if (arroba != NULL) {
            p->fila = f;
            p->columna = (int) (arroba - p->mapa[f]);
            *arroba = '.';                          /* el heroe no es parte del mapa */
        }
    }
    p->oro = p->pasos = 0;
    p->salio = false;
}

void dibujar(const Partida *p)
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            putchar(f == p->fila && c == p->columna ? '@' : p->mapa[f][c]);
        }
        putchar('\n');
    }
}

/* Mueve si se puede. Devuelve false si el comando no es un movimiento. */
bool mover(Partida *p, char comando)
{
    int df = 0, dc = 0;
    switch (comando) {
    case 'w': df = -1; break;
    case 's': df = 1; break;
    case 'a': dc = -1; break;
    case 'd': dc = 1; break;
    default: return false;
    }
    char destino = p->mapa[p->fila + df][p->columna + dc];   /* el borde es pared: nunca se sale */
    if (destino == '#') {
        printf("  Pared.\n");
        return true;
    }
    p->fila += df;
    p->columna += dc;
    p->pasos++;
    if (destino == '$') {
        p->oro += 10;
        p->mapa[p->fila][p->columna] = '.';
        printf("  ¡Tesoro! Oro: %d\n", p->oro);
    } else if (destino == 'S') {
        p->salio = true;
    }
    return true;
}

int main(void)
{
    Partida p;
    iniciar(&p);
    dibujar(&p);
    char linea[20];
    while (!p.salio && fgets(linea, sizeof(linea), stdin) != NULL) {
        if (!mover(&p, linea[0])) {
            printf("  Usá w, a, s o d.\n");
        }
    }
    dibujar(&p);
    printf("%s Pasos: %d. Oro: %d.\n", p.salio ? "¡Encontraste la salida!" : "Te quedaste en la oscuridad.", p.pasos, p.oro);
    return 0;
}
```

#### Entrada de ejemplo

```
w
d
d
s
s
d
d
x
w
w
d
d
d
d
d
d
s
s
s
s
```

#### Salida esperada

```
#############
#@..#...$..E#
#.#.#.###.#.#
#.#.E.#$..#.#
#.###.#.###.#
#$........#S#
#############
  Pared.
  ¡Goblin (vida 14) te cierra el paso!
  Ronda 1: le pegás 6, te pega 3. Tu vida: 37
  Ronda 2: le pegás 7, te pega 3. Tu vida: 34
  Ronda 3: le pegás 9. ¡Goblin cae!
  Usá w, a, s o d.
  ¡Tesoro! Oro: 10
  ¡Dragón (vida 30) te cierra el paso!
  Ronda 1: le pegás 5, te pega 9. Tu vida: 25
  Ronda 2: le pegás 5, te pega 7. Tu vida: 18
  Ronda 3: le pegás 10, te pega 8. Tu vida: 10
  Ronda 4: le pegás 6, te pega 5. Tu vida: 5
  Ronda 5: le pegás 9. ¡Dragón cae!
#############
#...#.......#
#.#.#.###.#.#
#.#...#$..#.#
#.###.#.###.#
#$........#@#
#############
¡Venciste al Dragón y saliste! Vida: 5. Pasos: 18. Oro: 10.
```

#### Solución de referencia

```c
/*
 * Jefe final - Mision 2: los guardianes.
 * Los enemigos viven en un array aparte; entrar en su casilla empieza un combate por turnos.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define FILAS 7
#define COLUMNAS 13
#define MAX_ENEMIGOS 4

static const char *MAPA_INICIAL[FILAS] = {
    "#############",
    "#@..#...$...#",
    "#.#.#.###.#.#",
    "#.#...#$..#.#",
    "#.###.#.###.#",
    "#$........#S#",
    "#############",
};

typedef struct {
    char nombre[12];
    int fila, columna;
    int vida, ataque;
} Enemigo;

typedef struct {
    char mapa[FILAS][COLUMNAS + 1];
    int fila, columna;
    int vida, oro, pasos;
    bool salio;
    Enemigo enemigos[MAX_ENEMIGOS];
    int cantidad_enemigos;
} Partida;

void iniciar(Partida *p)
{
    for (int f = 0; f < FILAS; f++) {
        strcpy(p->mapa[f], MAPA_INICIAL[f]);
        char *arroba = strchr(p->mapa[f], '@');
        if (arroba != NULL) {
            p->fila = f;
            p->columna = (int) (arroba - p->mapa[f]);
            *arroba = '.';
        }
    }
    p->vida = 40;
    p->oro = p->pasos = 0;
    p->salio = false;
    Enemigo iniciales[] = { { "Goblin", 3, 4, 14, 4 }, { "Dragón", 1, 11, 30, 7 } };
    p->cantidad_enemigos = 2;
    memcpy(p->enemigos, iniciales, sizeof iniciales);
}

Enemigo *enemigo_en(Partida *p, int fila, int columna)
{
    for (int i = 0; i < p->cantidad_enemigos; i++) {
        if (p->enemigos[i].vida > 0 && p->enemigos[i].fila == fila && p->enemigos[i].columna == columna) {
            return &p->enemigos[i];
        }
    }
    return NULL;
}

void dibujar(Partida *p)
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            if (f == p->fila && c == p->columna) {
                putchar('@');
            } else if (enemigo_en(p, f, c) != NULL) {
                putchar('E');
            } else {
                putchar(p->mapa[f][c]);
            }
        }
        putchar('\n');
    }
}

int tirar(int minimo, int maximo)
{
    return minimo + rand() % (maximo - minimo + 1);
}

/* Pelea hasta que alguien cae. Devuelve true si gano el heroe. */
bool combatir(Partida *p, Enemigo *e)
{
    printf("  ¡%s (vida %d) te cierra el paso!\n", e->nombre, e->vida);
    for (int ronda = 1; p->vida > 0 && e->vida > 0; ronda++) {
        int golpe = tirar(5, 10);
        e->vida -= golpe;
        if (e->vida <= 0) {
            printf("  Ronda %d: le pegás %d. ¡%s cae!\n", ronda, golpe, e->nombre);
            return true;
        }
        int recibe = tirar(e->ataque - 2, e->ataque + 2);
        p->vida -= recibe;
        printf("  Ronda %d: le pegás %d, te pega %d. Tu vida: %d\n", ronda, golpe, recibe, p->vida > 0 ? p->vida : 0);
    }
    return false;
}

bool mover(Partida *p, char comando)
{
    int df = 0, dc = 0;
    switch (comando) {
    case 'w': df = -1; break;
    case 's': df = 1; break;
    case 'a': dc = -1; break;
    case 'd': dc = 1; break;
    default: return false;
    }
    int f = p->fila + df, c = p->columna + dc;
    if (p->mapa[f][c] == '#') {
        printf("  Pared.\n");
        return true;
    }
    Enemigo *e = enemigo_en(p, f, c);
    if (e != NULL && !combatir(p, e)) {
        return true;                                /* el heroe cayo: no avanza */
    }
    p->fila = f;
    p->columna = c;
    p->pasos++;
    if (p->mapa[f][c] == '$') {
        p->oro += 10;
        p->mapa[f][c] = '.';
        printf("  ¡Tesoro! Oro: %d\n", p->oro);
    } else if (p->mapa[f][c] == 'S') {
        p->salio = true;
    }
    return true;
}

int main(void)
{
    srand(30);                 /* fija para probar; para jugar: srand(time(NULL)) */
    Partida p;
    iniciar(&p);
    dibujar(&p);
    char linea[20];
    while (!p.salio && p.vida > 0 && fgets(linea, sizeof(linea), stdin) != NULL) {
        if (!mover(&p, linea[0])) {
            printf("  Usá w, a, s o d.\n");
        }
    }
    dibujar(&p);
    if (p.vida <= 0) {
        printf("Caíste bajo la montaña. Pasos: %d. Oro: %d.\n", p.pasos, p.oro);
    } else {
        printf("%s Vida: %d. Pasos: %d. Oro: %d.\n", p.salio ? "¡Venciste al Dragón y saliste!" : "Te quedaste en la oscuridad.", p.vida, p.pasos, p.oro);
    }
    return 0;
}
```

### Misión R05-N04-M3 · Guardar la partida

```meta
entrega: codigo
entorno: local
monedas: 8
xp: 40
```

#### Consigna

Agregá dos comandos:

- `g` guarda la `Partida` completa en `mazmorra.sav`, en binario, con un encabezado (marca `"MAZ"` y versión 1).
- `c` carga la partida guardada. Lee en una **copia** y solo reemplaza la actual si la marca, la versión y el registro están bien; si no hay partida guardada, lo avisa.

Si el héroe cae, ya no puede moverse: solo puede cargar (`Caíste: solo podés cargar la partida (c).`).

Probalo cargando antes de guardar, guardando justo antes del Dragón, venciéndolo y volviendo a cargar: el Dragón tiene que volver a estar ahí, y la vida, el oro y los pasos, como en el momento del guardado.

#### Criterio de aprobación

- Guarda y carga el struct completo con encabezado.
- Cargar no pisa la partida si el archivo no está o no es válido.
- Después de cargar, el mapa, los enemigos y el estado vuelven al momento del guardado.
- Si el héroe cae, solo se puede cargar.

#### Código inicial

```c
/*
 * Jefe final - Mision 2: los guardianes.
 * Los enemigos viven en un array aparte; entrar en su casilla empieza un combate por turnos.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define FILAS 7
#define COLUMNAS 13
#define MAX_ENEMIGOS 4

static const char *MAPA_INICIAL[FILAS] = {
    "#############",
    "#@..#...$...#",
    "#.#.#.###.#.#",
    "#.#...#$..#.#",
    "#.###.#.###.#",
    "#$........#S#",
    "#############",
};

typedef struct {
    char nombre[12];
    int fila, columna;
    int vida, ataque;
} Enemigo;

typedef struct {
    char mapa[FILAS][COLUMNAS + 1];
    int fila, columna;
    int vida, oro, pasos;
    bool salio;
    Enemigo enemigos[MAX_ENEMIGOS];
    int cantidad_enemigos;
} Partida;

void iniciar(Partida *p)
{
    for (int f = 0; f < FILAS; f++) {
        strcpy(p->mapa[f], MAPA_INICIAL[f]);
        char *arroba = strchr(p->mapa[f], '@');
        if (arroba != NULL) {
            p->fila = f;
            p->columna = (int) (arroba - p->mapa[f]);
            *arroba = '.';
        }
    }
    p->vida = 40;
    p->oro = p->pasos = 0;
    p->salio = false;
    Enemigo iniciales[] = { { "Goblin", 3, 4, 14, 4 }, { "Dragón", 1, 11, 30, 7 } };
    p->cantidad_enemigos = 2;
    memcpy(p->enemigos, iniciales, sizeof iniciales);
}

Enemigo *enemigo_en(Partida *p, int fila, int columna)
{
    for (int i = 0; i < p->cantidad_enemigos; i++) {
        if (p->enemigos[i].vida > 0 && p->enemigos[i].fila == fila && p->enemigos[i].columna == columna) {
            return &p->enemigos[i];
        }
    }
    return NULL;
}

void dibujar(Partida *p)
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            if (f == p->fila && c == p->columna) {
                putchar('@');
            } else if (enemigo_en(p, f, c) != NULL) {
                putchar('E');
            } else {
                putchar(p->mapa[f][c]);
            }
        }
        putchar('\n');
    }
}

int tirar(int minimo, int maximo)
{
    return minimo + rand() % (maximo - minimo + 1);
}

/* Pelea hasta que alguien cae. Devuelve true si gano el heroe. */
bool combatir(Partida *p, Enemigo *e)
{
    printf("  ¡%s (vida %d) te cierra el paso!\n", e->nombre, e->vida);
    for (int ronda = 1; p->vida > 0 && e->vida > 0; ronda++) {
        int golpe = tirar(5, 10);
        e->vida -= golpe;
        if (e->vida <= 0) {
            printf("  Ronda %d: le pegás %d. ¡%s cae!\n", ronda, golpe, e->nombre);
            return true;
        }
        int recibe = tirar(e->ataque - 2, e->ataque + 2);
        p->vida -= recibe;
        printf("  Ronda %d: le pegás %d, te pega %d. Tu vida: %d\n", ronda, golpe, recibe, p->vida > 0 ? p->vida : 0);
    }
    return false;
}

bool mover(Partida *p, char comando)
{
    int df = 0, dc = 0;
    switch (comando) {
    case 'w': df = -1; break;
    case 's': df = 1; break;
    case 'a': dc = -1; break;
    case 'd': dc = 1; break;
    default: return false;
    }
    int f = p->fila + df, c = p->columna + dc;
    if (p->mapa[f][c] == '#') {
        printf("  Pared.\n");
        return true;
    }
    Enemigo *e = enemigo_en(p, f, c);
    if (e != NULL && !combatir(p, e)) {
        return true;                                /* el heroe cayo: no avanza */
    }
    p->fila = f;
    p->columna = c;
    p->pasos++;
    if (p->mapa[f][c] == '$') {
        p->oro += 10;
        p->mapa[f][c] = '.';
        printf("  ¡Tesoro! Oro: %d\n", p->oro);
    } else if (p->mapa[f][c] == 'S') {
        p->salio = true;
    }
    return true;
}

int main(void)
{
    srand(30);                 /* fija para probar; para jugar: srand(time(NULL)) */
    Partida p;
    iniciar(&p);
    dibujar(&p);
    char linea[20];
    while (!p.salio && p.vida > 0 && fgets(linea, sizeof(linea), stdin) != NULL) {
        if (!mover(&p, linea[0])) {
            printf("  Usá w, a, s o d.\n");
        }
    }
    dibujar(&p);
    if (p.vida <= 0) {
        printf("Caíste bajo la montaña. Pasos: %d. Oro: %d.\n", p.pasos, p.oro);
    } else {
        printf("%s Vida: %d. Pasos: %d. Oro: %d.\n", p.salio ? "¡Venciste al Dragón y saliste!" : "Te quedaste en la oscuridad.", p.vida, p.pasos, p.oro);
    }
    return 0;
}
```

#### Entrada de ejemplo

```
c
d
d
s
s
d
d
w
w
d
d
d
d
d
g
d
s
c
d
s
s
s
s
```

#### Salida esperada

```
#############
#@..#...$..E#
#.#.#.###.#.#
#.#.E.#$..#.#
#.###.#.###.#
#$........#S#
#############
  No hay partida guardada.
  ¡Goblin (vida 14) te cierra el paso!
  Ronda 1: le pegás 6, te pega 3. Tu vida: 37
  Ronda 2: le pegás 7, te pega 3. Tu vida: 34
  Ronda 3: le pegás 9. ¡Goblin cae!
  ¡Tesoro! Oro: 10
  Partida guardada.
  ¡Dragón (vida 30) te cierra el paso!
  Ronda 1: le pegás 5, te pega 9. Tu vida: 25
  Ronda 2: le pegás 5, te pega 7. Tu vida: 18
  Ronda 3: le pegás 10, te pega 8. Tu vida: 10
  Ronda 4: le pegás 6, te pega 5. Tu vida: 5
  Ronda 5: le pegás 9. ¡Dragón cae!
  Partida cargada (vida 34, oro 10, pasos 13).
  ¡Dragón (vida 30) te cierra el paso!
  Ronda 1: le pegás 7, te pega 5. Tu vida: 29
  Ronda 2: le pegás 10, te pega 7. Tu vida: 22
  Ronda 3: le pegás 6, te pega 7. Tu vida: 15
  Ronda 4: le pegás 6, te pega 7. Tu vida: 8
  Ronda 5: le pegás 6. ¡Dragón cae!
#############
#...#.......#
#.#.#.###.#.#
#.#...#$..#.#
#.###.#.###.#
#$........#@#
#############
¡Venciste al Dragón y saliste! Vida: 8. Pasos: 18. Oro: 10.
```

#### Solución de referencia

```c
/*
 * Jefe final - Mision 3: guardar la partida.
 * g guarda y c carga, en binario con marca y version. Todo el estado esta en el struct Partida.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define FILAS 7
#define COLUMNAS 13
#define MAX_ENEMIGOS 4
#define RUTA "mazmorra.sav"
#define VERSION 1

static const char *MAPA_INICIAL[FILAS] = {
    "#############",
    "#@..#...$...#",
    "#.#.#.###.#.#",
    "#.#...#$..#.#",
    "#.###.#.###.#",
    "#$........#S#",
    "#############",
};

typedef struct {
    char nombre[12];
    int fila, columna;
    int vida, ataque;
} Enemigo;

typedef struct {
    char mapa[FILAS][COLUMNAS + 1];
    int fila, columna;
    int vida, oro, pasos;
    bool salio;
    Enemigo enemigos[MAX_ENEMIGOS];
    int cantidad_enemigos;
} Partida;

void iniciar(Partida *p)
{
    for (int f = 0; f < FILAS; f++) {
        strcpy(p->mapa[f], MAPA_INICIAL[f]);
        char *arroba = strchr(p->mapa[f], '@');
        if (arroba != NULL) {
            p->fila = f;
            p->columna = (int) (arroba - p->mapa[f]);
            *arroba = '.';
        }
    }
    p->vida = 40;
    p->oro = p->pasos = 0;
    p->salio = false;
    Enemigo iniciales[] = { { "Goblin", 3, 4, 14, 4 }, { "Dragón", 1, 11, 30, 7 } };
    p->cantidad_enemigos = 2;
    memcpy(p->enemigos, iniciales, sizeof iniciales);
}

Enemigo *enemigo_en(Partida *p, int fila, int columna)
{
    for (int i = 0; i < p->cantidad_enemigos; i++) {
        if (p->enemigos[i].vida > 0 && p->enemigos[i].fila == fila && p->enemigos[i].columna == columna) {
            return &p->enemigos[i];
        }
    }
    return NULL;
}

void dibujar(Partida *p)
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            if (f == p->fila && c == p->columna) {
                putchar('@');
            } else if (enemigo_en(p, f, c) != NULL) {
                putchar('E');
            } else {
                putchar(p->mapa[f][c]);
            }
        }
        putchar('\n');
    }
}

int tirar(int minimo, int maximo)
{
    return minimo + rand() % (maximo - minimo + 1);
}

/* Pelea hasta que alguien cae. Devuelve true si gano el heroe. */
bool combatir(Partida *p, Enemigo *e)
{
    printf("  ¡%s (vida %d) te cierra el paso!\n", e->nombre, e->vida);
    for (int ronda = 1; p->vida > 0 && e->vida > 0; ronda++) {
        int golpe = tirar(5, 10);
        e->vida -= golpe;
        if (e->vida <= 0) {
            printf("  Ronda %d: le pegás %d. ¡%s cae!\n", ronda, golpe, e->nombre);
            return true;
        }
        int recibe = tirar(e->ataque - 2, e->ataque + 2);
        p->vida -= recibe;
        printf("  Ronda %d: le pegás %d, te pega %d. Tu vida: %d\n", ronda, golpe, recibe, p->vida > 0 ? p->vida : 0);
    }
    return false;
}

bool mover(Partida *p, char comando)
{
    int df = 0, dc = 0;
    switch (comando) {
    case 'w': df = -1; break;
    case 's': df = 1; break;
    case 'a': dc = -1; break;
    case 'd': dc = 1; break;
    default: return false;
    }
    int f = p->fila + df, c = p->columna + dc;
    if (p->mapa[f][c] == '#') {
        printf("  Pared.\n");
        return true;
    }
    Enemigo *e = enemigo_en(p, f, c);
    if (e != NULL && !combatir(p, e)) {
        return true;                                /* el heroe cayo: no avanza */
    }
    p->fila = f;
    p->columna = c;
    p->pasos++;
    if (p->mapa[f][c] == '$') {
        p->oro += 10;
        p->mapa[f][c] = '.';
        printf("  ¡Tesoro! Oro: %d\n", p->oro);
    } else if (p->mapa[f][c] == 'S') {
        p->salio = true;
    }
    return true;
}

typedef struct {
    char marca[4];              /* "MAZ" */
    int version;
} Encabezado;

bool guardar(const Partida *p)
{
    FILE *f = fopen(RUTA, "wb");
    if (f == NULL) {
        return false;
    }
    Encabezado e = { "MAZ", VERSION };
    bool ok = fwrite(&e, sizeof e, 1, f) == 1 && fwrite(p, sizeof *p, 1, f) == 1;
    return fclose(f) == 0 && ok;
}

/* Lee en una copia y recien si salio todo bien reemplaza la partida. */
bool cargar(Partida *p)
{
    FILE *f = fopen(RUTA, "rb");
    if (f == NULL) {
        return false;
    }
    Encabezado e;
    Partida leida;
    bool ok = fread(&e, sizeof e, 1, f) == 1 && memcmp(e.marca, "MAZ", 4) == 0 && e.version == VERSION
              && fread(&leida, sizeof leida, 1, f) == 1;
    fclose(f);
    if (ok) {
        *p = leida;
    }
    return ok;
}

int main(void)
{
    srand(30);                 /* fija para probar; para jugar: srand(time(NULL)) */
    remove(RUTA);              /* para que la prueba arranque igual */
    Partida p;
    iniciar(&p);
    dibujar(&p);
    char linea[20];
    while (!p.salio && fgets(linea, sizeof(linea), stdin) != NULL) {
        if (p.vida <= 0 && linea[0] != 'c') {
            printf("  Caíste: solo podés cargar la partida (c).\n");
        } else if (linea[0] == 'g') {
            printf("  %s\n", guardar(&p) ? "Partida guardada." : "No se pudo guardar.");
        } else if (linea[0] == 'c') {
            if (cargar(&p)) {
                printf("  Partida cargada (vida %d, oro %d, pasos %d).\n", p.vida, p.oro, p.pasos);
            } else {
                printf("  No hay partida guardada.\n");
            }
        } else if (!mover(&p, linea[0])) {
            printf("  Usá w, a, s, d, g (guardar) o c (cargar).\n");
        }
    }
    dibujar(&p);
    if (p.vida <= 0) {
        printf("Caíste bajo la montaña. Pasos: %d. Oro: %d.\n", p.pasos, p.oro);
    } else {
        printf("%s Vida: %d. Pasos: %d. Oro: %d.\n", p.salio ? "¡Venciste al Dragón y saliste!" : "Te quedaste en la oscuridad.", p.vida, p.pasos, p.oro);
    }
    remove(RUTA);
    return 0;
}
```

### Encargo R05-N04-E1 · El cartógrafo

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 40
```

#### Consigna

Antes de bajar, el cartógrafo del Gremio revisa los mapas. Escribí `revisar`, que para un mapa (un array de textos) verifica que todas las filas tengan el mismo largo, que el borde sea todo pared y que haya exactamente un `@` y una `S`, y cuenta los tesoros.

Si es válido, calculá con una **búsqueda en anchura** (BFS, con una cola en un array) la menor cantidad de pasos del `@` a la `S`, o avisá que no se puede alcanzar. Probalo con la mazmorra, con una cámara donde la salida está encerrada y con un mapa roto.

#### Criterio de aprobación

- Valida largo de filas, borde, inicio y salida.
- Usa BFS con una cola para la distancia mínima.
- Distingue mapa inválido de salida inalcanzable.

#### Salida esperada

```
== La mazmorra ==
  Válido: 3 tesoros, salida a 18 pasos como mínimo.
== La cámara sellada ==
  La salida no se puede alcanzar.
== El mapa roto ==
  Hueco en el borde en (1, 6).
  La fila 2 no tiene 7 columnas.
  Mapa inválido.
```

#### Solución de referencia

```c
/*
 * Jefe final - Encargo: el cartografo. Valida un mapa y comprueba con una
 * busqueda en anchura (BFS) que la salida se puede alcanzar desde el inicio.
 */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAX 20

typedef struct {
    int fila, columna;
} Punto;

/* Devuelve la cantidad de pasos minima hasta la S, o -1 si no se llega. */
int distancia_a_la_salida(char mapa[][MAX + 1], int filas, int columnas, Punto inicio)
{
    int dist[MAX][MAX];
    for (int f = 0; f < filas; f++) {
        for (int c = 0; c < columnas; c++) {
            dist[f][c] = -1;
        }
    }
    Punto cola[MAX * MAX];
    int primero = 0, ultimo = 0;
    cola[ultimo++] = inicio;
    dist[inicio.fila][inicio.columna] = 0;
    const int df[] = { -1, 1, 0, 0 }, dc[] = { 0, 0, -1, 1 };
    while (primero < ultimo) {
        Punto p = cola[primero++];
        if (mapa[p.fila][p.columna] == 'S') {
            return dist[p.fila][p.columna];
        }
        for (int k = 0; k < 4; k++) {
            int f = p.fila + df[k], c = p.columna + dc[k];
            if (f >= 0 && f < filas && c >= 0 && c < columnas && mapa[f][c] != '#' && dist[f][c] < 0) {
                dist[f][c] = dist[p.fila][p.columna] + 1;
                cola[ultimo++] = (Punto) { f, c };
            }
        }
    }
    return -1;
}

void revisar(const char *titulo, const char *filas_texto[], int filas)
{
    char mapa[MAX][MAX + 1];
    int columnas = (int) strlen(filas_texto[0]);
    int inicios = 0, salidas = 0, tesoros = 0;
    Punto inicio = { 0, 0 };
    bool ok = true;
    printf("== %s ==\n", titulo);
    for (int f = 0; f < filas; f++) {
        if ((int) strlen(filas_texto[f]) != columnas) {
            printf("  La fila %d no tiene %d columnas.\n", f, columnas);
            ok = false;
            continue;
        }
        strcpy(mapa[f], filas_texto[f]);
        for (int c = 0; c < columnas; c++) {
            char x = mapa[f][c];
            bool borde = f == 0 || f == filas - 1 || c == 0 || c == columnas - 1;
            if (borde && x != '#') {
                printf("  Hueco en el borde en (%d, %d).\n", f, c);
                ok = false;
            }
            if (x == '@') {
                inicios++;
                inicio = (Punto) { f, c };
            } else if (x == 'S') {
                salidas++;
            } else if (x == '$') {
                tesoros++;
            }
        }
    }
    if (inicios != 1 || salidas != 1) {
        printf("  Tiene que haber un inicio y una salida (hay %d y %d).\n", inicios, salidas);
        ok = false;
    }
    if (!ok) {
        printf("  Mapa inválido.\n");
        return;
    }
    int d = distancia_a_la_salida(mapa, filas, columnas, inicio);
    if (d < 0) {
        printf("  La salida no se puede alcanzar.\n");
    } else {
        printf("  Válido: %d tesoros, salida a %d pasos como mínimo.\n", tesoros, d);
    }
}

int main(void)
{
    const char *bueno[] = { "#############", "#@..#...$...#", "#.#.#.###.#.#", "#.#...#$..#.#",
                            "#.###.#.###.#", "#$........#S#", "#############" };
    const char *encerrado[] = { "#########", "#@..#..S#", "#...#...#", "#########" };
    const char *roto[] = { "#######", "#@...S.", "#####" };
    revisar("La mazmorra", bueno, 7);
    revisar("La cámara sellada", encerrado, 4);
    revisar("El mapa roto", roto, 3);
    return 0;
}
```

### Prueba del sello

#### ¿Por qué la posición del héroe va aparte del mapa?

Para no borrar lo que hay debajo al moverse: el mapa guarda el mundo y la posición se dibuja encima.

#### ¿Por qué no hace falta controlar los límites de la matriz al moverse?

Porque el borde es todo pared: antes de salir de la matriz siempre se encuentra un `#` y el movimiento se frena.

#### ¿Por qué se puede guardar la `Partida` con un solo `fwrite`?

Porque todo el estado está en el struct y no tiene punteros: sus bytes son todo lo que hace falta.

#### ¿Por qué `cargar` lee en una copia?

Para no perder la partida actual si el archivo no existe, es de otra versión o está cortado.

#### ¿Qué garantiza la búsqueda en anchura?

Que la primera vez que llega a la salida lo hace por el camino más corto, porque explora por capas de distancia.

### Soluciones (docente)

Proyecto final nuevo (en `02-C-Intermedio` estaba planificado como 30-ProyectoMazmorra). Las misiones 2 y 3 parten del código de la anterior; las salidas dependen del `rand` de glibc.

## R05-N05 · La Encrucijada del Yunque

```meta
tipo: ventana
padre: R05-N04
precio: 10
```

### Crónica

Salís de la mazmorra con el sello del Dragón en la mano. En la entrada de las Forjas hay un yunque viejo, y de él salen varios caminos. {mentor} se apoya en el martillo y te mira con algo parecido al orgullo.

—Ya hablás la lengua de las Forjas, {heroe}. Lo que sigue no es obligatorio: es **tuyo**. Por un camino se llega a la **Forja Viva**, donde el metal se mueve en una pantalla. Por el otro, al **Taller de los Autómatas**, donde el código mueve cosas de verdad.

—Antes de elegir, mirá hacia atrás. ¿Qué te llevás de este viaje?

### Objetivos

- Repasar todo el camino principal y reconocer lo que aprendiste.
- Conocer las Sendas optativas que salen de acá.

### Explicación

#### Lo que ya sabés hacer

- **Templar el metal**: compilar, tipos, operadores, bits, entrada y salida, decisiones, bucles, funciones y la biblioteca estándar.
- **Los pasillos numerados**: arrays, textos, structs y punteros.
- **Las Minas**: memoria dinámica, arrays que crecen, listas enlazadas y punteros a función.
- **El Archivo**: archivos de texto y binarios, programas en varios archivos, argumentos y menús.
- **La Prueba del Temple**: depuración, tests y programas completos.

Con eso ya podés escribir programas completos en C y leer código de otros. Lo que sigue son **especializaciones**.

#### Las Sendas

Cada Senda es un camino optativo: no hace falta para completar el curso, y su entrada se paga con **comodines** (los que ganaste con los encargos del Gremio). Adentro, los nodos se pagan con lingotes, como siempre.

- **Senda de la Forja Viva**: videojuegos 2D con **SDL3**. Ventanas, el bucle de juego, teclado, movimiento con tiempo real y colisiones, hasta un juego completo. Se resuelve en tu compu.
- **Senda de los Autómatas**: **Arduino**. Programar una placa en C, leer botones y sensores, hablar con la compu por el puerto serie y usar la placa como control de un juego.

### Misión R05-N05-M1 · Mirá hacia atrás

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
3. ¿Qué te gustaría construir ahora con C?

Charlalo con el profe en la próxima clase (o escribíselo). Cuando lo tengas, marcá la misión como completada.

#### Criterio de aprobación

- Respondió las tres preguntas (en clase o por escrito).

### Soluciones (docente)

Nodo Ventana: cierra el camino principal (completarlo completa el curso) y de acá brotan las Sendas S01 y S02. La misión es de reflexión, sin entrega.
