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
temas: cal.depuracion
```

### Crónica

Para ser oficial de la Forja hay que pasar la **Prueba del Temple**. La primera sala está llena de piezas que parecen perfectas, pero algunas se quiebran al primer golpe. Kira, por costumbre, le grita a una espada que no anda.

Ferrum la aparta, golpea cada pieza con un martillito y **escucha** dónde suena hueca. —Una espada que se ve bien no es una espada que anda —dice {mentor}, y le da a Kira una lupa de cristal—. Con esta se mira adentro del metal **mientras trabaja**, golpe por golpe. No hace falta gritarle: hace falta **frenarla** en la línea justa.

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

**En Windows:** `gdb` viene con MSYS2 (`pacman -S mingw-w64-ucrt-x86_64-gdb`) y se usa igual: `gdb programa.exe`. Sin comandos, los IDE tienen el mismo depurador con botones:
- **ZinjaI** (Linux y Windows): clic en el margen de una línea para un punto de parada y **F5** para depurar; las variables se ven en el panel de inspecciones.
- **Code::Blocks**: **F5** pone el punto de parada, Depurar → Iniciar (**F8**), y Depurar → Ventanas → Variables.
- **VS Code**: con la extensión C/C++, **F9** pone el punto de parada y **F5** depura (la primera vez pide elegir `gcc` y crea `launch.json`).

#### Los sanitizadores

```bash
gcc -g -fsanitize=address,undefined -o programa main.c
```

- **`address`**: accesos fuera de un array, uso después de liberar, fugas.
- **`undefined`**: comportamiento indefinido, como el desbordamiento de un `int` con signo o un desplazamiento de bits inválido.

`valgrind ./programa` encuentra problemas parecidos sin recompilar (más lento).

**En Windows** (MinGW), `-fsanitize=address` no existe: queda `-fsanitize=undefined` con `-fsanitize-undefined-trap-on-error`, y para la memoria, **Dr. Memory** (`drmemory -- programa.exe`), que hace lo de `valgrind`. Otra opción es instalar **WSL** (un Linux dentro de Windows) y usar todo lo de arriba tal cual.

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

### Micro-misión R05-N01-P1 · La pieza que suena hueca

```meta
lugar: La Prueba del Temple
personajes: Kira, Gheco, Maese Ferrum
criatura: ogro
carta: Error de lógica | compila y corre, pero el resultado está mal · mirar los valores paso a paso · el depurador frena en la línea justa
recompensa: xp 10, oro 10
```

#### Escena
La primera sala está llena de piezas que parecen perfectas. Kira le grita a una espada que no anda. Ferrum la aparta, golpea cada pieza con un martillito y **escucha** dónde suena hueca.
—No hace falta gritarle —dice—. Hace falta frenarla en la línea justa.

#### Gheco sugiere
El promedio de 4 notas da 7 y no 7.5: la división se hace con dos enteros. Seguilo línea por línea (o con un `printf` de depuración): ¿qué valor tiene la división antes de guardarse?

#### Desafío
Arreglá el promedio sin cambiar las notas.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int notas[4] = { 8, 7, 9, 6 };
    int suma = 0;
    for (int i = 0; i < 4; i++) {
        suma += notas[i];
    }
    double promedio = suma / 4;
    printf("promedio: %.2f\n", promedio);
    return 0;
}
```

#### Salida esperada
```
promedio: 7.50
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int notas[4] = { 8, 7, 9, 6 };
    int suma = 0;
    for (int i = 0; i < 4; i++) {
        suma += notas[i];
    }
    double promedio = suma / 4.0;
    printf("promedio: %.2f\n", promedio);
    return 0;
}
```

#### Al superarla
7,50. La pieza suena maciza. Ferrum guarda el martillito sin decir nada; Kira entiende que eso es un elogio.

#### Imagen
- Una sala oscura llena de espadas colgadas; una tiene una grieta fina que brilla.
- Maese Ferrum (herrero humano enorme, NO es enano: mide unos dos metros, de piernas largas, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) golpea una espada con un martillito y escucha.

### Micro-misión R05-N01-P2 · El que nunca entra

```meta
lugar: La Prueba del Temple
personajes: Kira, Gheco, Tizón
criatura: ogro
carta: = contra == | if (x = 0) ASIGNA y da falso · if (x == 0) compara · -Wall avisa: «suggest parentheses»
recompensa: xp 10, oro 10
```

#### Escena
Tizón escribió un control que dice «stock agotado» cuando el stock es 0. Nunca lo dice. Y después de pasar por el control, el stock de todo queda en 0.

#### Gheco sugiere
`if (stock = 0)` **guarda** 0 en `stock` y la condición vale 0 (falso). Para comparar se usa `==`. El compilador lo avisa con `-Wall`: leé las advertencias.

#### Desafío
Corregí la comparación.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int stocks[3] = { 5, 0, 12 };
    for (int i = 0; i < 3; i++) {
        int stock = stocks[i];
        if (stock = 0) {
            printf("pieza %d: agotada\n", i);
        } else {
            printf("pieza %d: quedan %d\n", i, stock);
        }
    }
    return 0;
}
```

#### Salida esperada
```
pieza 0: quedan 5
pieza 1: agotada
pieza 2: quedan 12
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int stocks[3] = { 5, 0, 12 };
    for (int i = 0; i < 3; i++) {
        int stock = stocks[i];
        if (stock == 0) {
            printf("pieza %d: agotada\n", i);
        } else {
            printf("pieza %d: quedan %d\n", i, stock);
        }
    }
    return 0;
}
```

#### Al superarla
Ahora sí avisa, y el stock no desaparece. Tizón se promete leer **todas** las advertencias. Las anota en la libreta, para medirlas.

#### Imagen
- Un cartel de stock que muestra ceros en todas las filas, tachado.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) lee una advertencia amarilla del Horno.

### Micro-misión R05-N01-P3 · La variable sin valor

```meta
lugar: La Prueba del Temple
personajes: Kira, Gheco, Hulda
criatura: ogro
carta: Sin inicializar | una variable local empieza con basura · el acumulador va en 0 ANTES del bucle · -Wall a veces lo avisa
recompensa: xp 10, oro 10
```

#### Escena
Hulda suma las cargas del día con un programa que a veces da bien y a veces da cualquier cosa, según el día. —En mi compu anda —dice. Ferrum: —«En mi compu anda» no alcanza.

#### Gheco sugiere
Una variable local sin valor inicial tiene **basura**: lo que quedó en esa memoria. El acumulador tiene que arrancar en 0.

#### Desafío
Inicializá el acumulador.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int cargas[4] = { 120, 80, 200, 50 };
    int total___;
    for (int i = 0; i < 4; i++) {
        total += cargas[i];
    }
    printf("total del dia: %d kg\n", total);
    return 0;
}
```

#### Salida esperada
```
total del dia: 450 kg
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int cargas[4] = { 120, 80, 200, 50 };
    int total = 0;
    for (int i = 0; i < 4; i++) {
        total += cargas[i];
    }
    printf("total del dia: %d kg\n", total);
    return 0;
}
```

#### Al superarla
Cuatrocientos cincuenta, todos los días igual. Hulda le pone un cero bien grande al principio de la tablilla, para no olvidarse más.

#### Imagen
- Una tablilla de minera con un cero enorme escrito al principio.
- Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro) lo remarca con tiza.

### Micro-misión R05-N01-P4 · Uno de menos

```meta
lugar: La Prueba del Temple
personajes: Kira, Gheco, Tizón
criatura: ogro
carta: Off by one | contar desde 1 pide <= · contar desde 0 pide < · probá con el primero y el último a mano
recompensa: xp 15, oro 15
```

#### Escena
Tizón suma el carbón de los 7 días de la semana y le da de menos. Lo revisa tres veces con el calibre: el carbón está, el que falta es un **día**.

#### Gheco sugiere
Si el contador arranca en 1, para llegar al 7 la condición es `dia <= 7`. Con `< 7` se queda en el 6: le falta uno. Probá a mano la primera y la última vuelta.

#### Desafío
Corregí el límite para que se cuenten los 7 días.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int total = 0;
    int dias = 0;
    for (int dia = 1; dia < 7; dia++) {
        total += 10 * dia;
        dias++;
    }
    printf("%d dias, %d bolsas de carbon\n", dias, total);
    return 0;
}
```

#### Salida esperada
```
7 dias, 280 bolsas de carbon
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int total = 0;
    int dias = 0;
    for (int dia = 1; dia <= 7; dia++) {
        total += 10 * dia;
        dias++;
    }
    printf("%d dias, %d bolsas de carbon\n", dias, total);
    return 0;
}
```

#### Al superarla
Siete días, doscientas ochenta bolsas. Tizón le pone nombre al domingo en la libreta para no volver a perderlo.

#### Imagen
- Un calendario de piedra con siete días; el último estaba tapado con una tela.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) destapa el domingo, aliviado.

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
temas: cal.pruebas
```

### Crónica

La segunda sala de la Prueba está llena de martillos de prueba. Antes de entregar una espada, se golpea donde **suele** quebrarse: la punta, el filo, la unión con la empuñadura.

Tizón entra a la sala, ve los martillos y los calibres y se emociona hasta las lágrimas: por fin alguien le **pide** que mida todo. Prueba cada pieza tres veces. Después, por las dudas, una cuarta.

—No se prueba donde la espada es fuerte —dice {mentor}—. Se prueba en los bordes. Y se prueba **cada vez** que se toca el metal, no una sola.

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

### Micro-misión R05-N02-P1 · El martillo de prueba

```meta
lugar: La Prueba del Temple
personajes: Kira, Gheco, Tizón
carta: Un mini framework | una macro PROBAR(cond) cuenta y muestra la línea que falla · al final, cuántas pasaron
recompensa: xp 10, oro 10
```

#### Escena
La segunda sala está llena de martillos de prueba. Tizón entra, ve los martillos y los calibres, y se emociona hasta las lágrimas: por fin alguien le **pide** que mida todo.

#### Gheco sugiere
`PROBAR(cond)` suma 1 a las pruebas y, si `cond` es falsa, muestra la línea (`__LINE__`). Si es verdadera, suma 1 a las que pasaron.

#### Desafío
Completá la macro: si la condición se cumple, cuenta una que pasó.

#### Código inicial
```c
#include <stdio.h>

static int pruebas = 0, pasaron = 0;
#define PROBAR(cond) do { pruebas++; if (cond) { ___; } else { printf("falla en la linea %d\n", __LINE__); } } while (0)

int maximo(int a, int b)
{
    return a > b ? a : b;
}

int main(void)
{
    PROBAR(maximo(3, 7) == 7);
    PROBAR(maximo(7, 3) == 7);
    PROBAR(maximo(-2, -9) == -2);
    PROBAR(maximo(4, 4) == 4);
    printf("%d de %d pruebas pasaron\n", pasaron, pruebas);
    return 0;
}
```

#### Salida esperada
```
4 de 4 pruebas pasaron
```

#### Solución
```c
#include <stdio.h>

static int pruebas = 0, pasaron = 0;
#define PROBAR(cond) do { pruebas++; if (cond) { pasaron++; } else { printf("falla en la linea %d\n", __LINE__); } } while (0)

int maximo(int a, int b)
{
    return a > b ? a : b;
}

int main(void)
{
    PROBAR(maximo(3, 7) == 7);
    PROBAR(maximo(7, 3) == 7);
    PROBAR(maximo(-2, -9) == -2);
    PROBAR(maximo(4, 4) == 4);
    printf("%d de %d pruebas pasaron\n", pasaron, pruebas);
    return 0;
}
```

#### Al superarla
Cuatro de cuatro. Tizón prueba cada pieza tres veces. Después, por las dudas, una cuarta.

#### Imagen
- Una sala con martillos de prueba colgados y una pizarra que dice 4/4.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) llorando de emoción con un calibre en cada mano.

### Micro-misión R05-N02-P2 · Probar en los bordes

```meta
lugar: La Prueba del Temple
personajes: Kira, Gheco, Maese Ferrum
criatura: ogro
carta: Casos límite | probar el 0, el máximo, el mínimo, el borde exacto · los errores viven en los bordes
recompensa: xp 15, oro 15
```

#### Escena
—No se prueba donde la espada es fuerte —dice Ferrum—. Se prueba en los bordes. —La función que clasifica la temperatura anda con 500 y con 1100… y falla justo en 800.

#### Gheco sugiere
Las pruebas del borde (800 exacto) muestran el error: «templada» empieza **en** 800, así que la comparación es `>=`.

#### Desafío
Corregí la función para que pasen las cinco pruebas.

#### Código inicial
```c
#include <stdio.h>
#include <string.h>

static int pruebas = 0, pasaron = 0;
#define PROBAR(cond) do { pruebas++; if (cond) { pasaron++; } else { printf("falla en la linea %d\n", __LINE__); } } while (0)

const char *estado(int grados)
{
    if (grados > 1200) {
        return "quemada";
    }
    if (grados > 800) {
        return "templada";
    }
    return "fria";
}

int main(void)
{
    PROBAR(strcmp(estado(500), "fria") == 0);
    PROBAR(strcmp(estado(799), "fria") == 0);
    PROBAR(strcmp(estado(800), "templada") == 0);
    PROBAR(strcmp(estado(1200), "templada") == 0);
    PROBAR(strcmp(estado(1201), "quemada") == 0);
    printf("%d de %d pruebas pasaron\n", pasaron, pruebas);
    return 0;
}
```

#### Salida esperada
```
5 de 5 pruebas pasaron
```

#### Solución
```c
#include <stdio.h>
#include <string.h>

static int pruebas = 0, pasaron = 0;
#define PROBAR(cond) do { pruebas++; if (cond) { pasaron++; } else { printf("falla en la linea %d\n", __LINE__); } } while (0)

const char *estado(int grados)
{
    if (grados > 1200) {
        return "quemada";
    }
    if (grados >= 800) {
        return "templada";
    }
    return "fria";
}

int main(void)
{
    PROBAR(strcmp(estado(500), "fria") == 0);
    PROBAR(strcmp(estado(799), "fria") == 0);
    PROBAR(strcmp(estado(800), "templada") == 0);
    PROBAR(strcmp(estado(1200), "templada") == 0);
    PROBAR(strcmp(estado(1201), "quemada") == 0);
    printf("%d de %d pruebas pasaron\n", pasaron, pruebas);
    return 0;
}
```

#### Al superarla
Cinco de cinco. Ferrum golpea el yunque dos veces. Kira, esta vez, sabe exactamente qué significa.

#### Imagen
- Un termómetro de cobre con una marca en 800 que brilla.
- Maese Ferrum (herrero humano enorme, NO es enano: mide unos dos metros, de piernas largas, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) golpea el yunque dos veces.

### Micro-misión R05-N02-P3 · Primero la prueba

```meta
lugar: La Prueba del Temple
personajes: Kira, Gheco, Tizón
carta: Primero la prueba | escribir las pruebas antes de la función · al principio fallan · se programa hasta que pasen
recompensa: xp 15, oro 15
```

#### Escena
Tizón propone algo raro: escribir las pruebas **antes** que la función. Las pruebas de `es_bisiesto` ya están; la función no.

#### Gheco sugiere
Un año es bisiesto si es divisible por 4, salvo los divisibles por 100, que solo lo son si también son divisibles por 400.

#### Desafío
Escribí `es_bisiesto` hasta que pasen las cinco pruebas.

#### Código inicial
```c
#include <stdio.h>
#include <stdbool.h>

static int pruebas = 0, pasaron = 0;
#define PROBAR(cond) do { pruebas++; if (cond) { pasaron++; } else { printf("falla en la linea %d\n", __LINE__); } } while (0)

bool es_bisiesto(int anio)
{
    ___
}

int main(void)
{
    PROBAR(es_bisiesto(2024));
    PROBAR(!es_bisiesto(2023));
    PROBAR(!es_bisiesto(1900));
    PROBAR(es_bisiesto(2000));
    PROBAR(es_bisiesto(2028));
    printf("%d de %d pruebas pasaron\n", pasaron, pruebas);
    return 0;
}
```

#### Salida esperada
```
5 de 5 pruebas pasaron
```

#### Solución
```c
#include <stdio.h>
#include <stdbool.h>

static int pruebas = 0, pasaron = 0;
#define PROBAR(cond) do { pruebas++; if (cond) { pasaron++; } else { printf("falla en la linea %d\n", __LINE__); } } while (0)

bool es_bisiesto(int anio)
{
    return (anio % 4 == 0 && anio % 100 != 0) || anio % 400 == 0;
}

int main(void)
{
    PROBAR(es_bisiesto(2024));
    PROBAR(!es_bisiesto(2023));
    PROBAR(!es_bisiesto(1900));
    PROBAR(es_bisiesto(2000));
    PROBAR(es_bisiesto(2028));
    printf("%d de %d pruebas pasaron\n", pasaron, pruebas);
    return 0;
}
```

#### Al superarla
Cinco de cinco, al tercer intento. Tizón anota la fecha y la hora exacta en que pasaron todas. Con minutos y segundos.

#### Imagen
- Una pizarra con cinco pruebas escritas antes que la función; las cinco con un tilde verde.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) anota la hora en la libreta.

### Micro-misión R05-N02-P4 · La prueba que encuentra al ogro

```meta
lugar: La Prueba del Temple
personajes: Kira, Gheco, Chispa
criatura: ogro
carta: Una prueba para cada error | cuando aparece un error, primero se escribe la prueba que lo muestra · después se arregla · así no vuelve
recompensa: xp 15, oro 15
```

#### Escena
Chispa encontró un error en la balanza del Gremio y, por primera vez en su vida, el error es **en contra suya**: con 1999 centavos y 10 % de descuento le cobran 1799 en vez de 1800. Antes de arreglarlo, Kira escribe la prueba que lo muestra.

#### Gheco sugiere
La regla del Gremio: el descuento es el 10 % del precio, en centavos enteros y **redondeado para abajo** (`centavos / 10`), y se resta. Con 1999, el descuento es 199 y se paga 1800. La cuenta `centavos * 9 / 10` redondea el precio final para abajo y da 1799.

#### Desafío
Arreglá la función para que pase la prueba nueva sin romper las otras.

#### Código inicial
```c
#include <stdio.h>

static int pruebas = 0, pasaron = 0;
#define PROBAR(cond) do { pruebas++; if (cond) { pasaron++; } else { printf("falla en la linea %d\n", __LINE__); } } while (0)

int con_descuento(int centavos)
{
    return centavos * 9 / 10;
}

int main(void)
{
    PROBAR(con_descuento(1000) == 900);
    PROBAR(con_descuento(500) == 450);
    PROBAR(con_descuento(1999) == 1800);
    printf("%d de %d pruebas pasaron\n", pasaron, pruebas);
    return 0;
}
```

#### Salida esperada
```
3 de 3 pruebas pasaron
```

#### Solución
```c
#include <stdio.h>

static int pruebas = 0, pasaron = 0;
#define PROBAR(cond) do { pruebas++; if (cond) { pasaron++; } else { printf("falla en la linea %d\n", __LINE__); } } while (0)

int con_descuento(int centavos)
{
    int descuento = centavos / 10;
    return centavos - descuento;
}

int main(void)
{
    PROBAR(con_descuento(1000) == 900);
    PROBAR(con_descuento(500) == 450);
    PROBAR(con_descuento(1999) == 1800);
    printf("%d de %d pruebas pasaron\n", pasaron, pruebas);
    return 0;
}
```

#### Al superarla
Tres de tres. Chispa recupera su centavo y lo festeja como un tesoro. Después calcula cuántos centavos ganó en toda su vida con los errores **a su favor** y prefiere no decirlo en voz alta.

#### Imagen
- Una balanza de bronce con un centavo de cobre que vuelve volando a la mano de un cliente.
- Chispa (mercader alto y flaco, sombrero de ala corta, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro) pálido, haciendo cuentas.

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

- `"kira"` → `"Kira"`; `"  tIZON   el   enano "` → `"Tizon El Enano"`; `"HULDA"` → `"Hulda"`;
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
    PROBAR("  tIZON   el   enano ", "Tizon El Enano");
    PROBAR("HULDA", "Hulda");
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
usa: arch.csv, alg.ordenamiento, mem.dinamica
```

### Crónica

Antes del último desafío, el Gremio le pide a Kira un favor sin nada de mágico: los comerciantes pierden los contactos de sus proveedores anotados en papelitos. Quieren una **agenda** que no se pierda, que busque rápido y que no acepte teléfonos con letras.

Chispa es el primero en probarla: intenta cargar su teléfono como «llamame». La agenda no lo acepta. Intenta «el de siempre». Tampoco. Al final lo carga bien, y es la primera vez que alguien en las Forjas tiene el teléfono de Chispa.

—No todo lo que se forja es una espada —dice {mentor}—. Las herramientas que usa la gente todos los días también se forjan. Y con el mismo cuidado.

### Objetivos

- Construir un programa útil fuera de los juegos, de punta a punta.
- Combinar memoria dinámica, textos, archivos CSV, búsqueda y orden con `qsort`.
- Validar los datos antes de guardarlos.

### Antes de empezar

- Strings (11), array dinámico (R03-N02), archivos de texto (R04-N01) y punteros a función (R03-N05).
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

### Micro-misión R05-N03-P1 · Un teléfono sin letras

```meta
lugar: La sede del Gremio
personajes: Kira, Gheco, Chispa
carta: Validar un texto | recorrer letra por letra · isdigit, el espacio y el + valen · al menos 6 dígitos
recompensa: xp 10, oro 10
```

#### Escena
Los comerciantes del Gremio pierden los teléfonos de sus proveedores. Chispa es el primero en probar la agenda: carga su teléfono como «llamame».

#### Gheco sugiere
Se recorre el texto: cada carácter tiene que ser un dígito, un espacio o un `+`, y tiene que haber al menos 6 dígitos.

#### Desafío
Completá la condición de carácter inválido.

#### Código inicial
```c
#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>

bool telefono_valido(const char *t)
{
    int digitos = 0;
    for (int i = 0; t[i] != '\0'; i++) {
        if (isdigit((unsigned char) t[i])) {
            digitos++;
        } else if (___) {
            return false;
        }
    }
    return digitos >= 6;
}

int main(void)
{
    const char *pruebas[4] = { "380 4223344", "llamame", "+54 380 1", "12345" };
    for (int i = 0; i < 4; i++) {
        printf("%-12s %s\n", pruebas[i], telefono_valido(pruebas[i]) ? "valido" : "invalido");
    }
    return 0;
}
```

#### Salida esperada
```
380 4223344  valido
llamame      invalido
+54 380 1    valido
12345        invalido
```

#### Solución
```c
#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>

bool telefono_valido(const char *t)
{
    int digitos = 0;
    for (int i = 0; t[i] != '\0'; i++) {
        if (isdigit((unsigned char) t[i])) {
            digitos++;
        } else if (t[i] != ' ' && t[i] != '+') {
            return false;
        }
    }
    return digitos >= 6;
}

int main(void)
{
    const char *pruebas[4] = { "380 4223344", "llamame", "+54 380 1", "12345" };
    for (int i = 0; i < 4; i++) {
        printf("%-12s %s\n", pruebas[i], telefono_valido(pruebas[i]) ? "valido" : "invalido");
    }
    return 0;
}
```

#### Al superarla
«llamame», inválido. Chispa intenta «el de siempre». También. Al final lo carga bien, y es la primera vez que alguien en las Forjas tiene el teléfono de Chispa.

#### Imagen
- Una agenda de cuero con renglones; uno dice «llamame» tachado en rojo.
- Chispa (mercader alto y flaco, sombrero de ala corta, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro) escribe su teléfono de verdad, a regañadientes.

### Micro-misión R05-N03-P2 · Buscar sin importar mayúsculas

```meta
lugar: La sede del Gremio
personajes: Kira, Gheco, Hulda
carta: Comparar sin mayúsculas | pasar las dos a minúsculas con tolower letra por letra · después strcmp · o comparar letra a letra
recompensa: xp 15, oro 15
```

#### Escena
Hulda busca en la agenda «HULDA», «hulda» y «Hulda», y solo la encuentra con la última. Grita fuerte. Kira tiene que hacer que la encuentre siempre.

#### Gheco sugiere
Se comparan letra por letra con `tolower`: si alguna difiere, no son iguales; si las dos terminan juntas, sí.

#### Desafío
Completá la comparación letra por letra.

#### Código inicial
```c
#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>

bool iguales_sin_mayusculas(const char *a, const char *b)
{
    int i = 0;
    while (a[i] != '\0' && b[i] != '\0') {
        if (___) {
            return false;
        }
        i++;
    }
    return a[i] == '\0' && b[i] == '\0';
}

int main(void)
{
    const char *buscados[3] = { "HULDA", "hulda", "Huldo" };
    for (int i = 0; i < 3; i++) {
        printf("%s: %s\n", buscados[i], iguales_sin_mayusculas("Hulda", buscados[i]) ? "encontrada" : "no esta");
    }
    return 0;
}
```

#### Salida esperada
```
HULDA: encontrada
hulda: encontrada
Huldo: no esta
```

#### Solución
```c
#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>

bool iguales_sin_mayusculas(const char *a, const char *b)
{
    int i = 0;
    while (a[i] != '\0' && b[i] != '\0') {
        if (tolower((unsigned char) a[i]) != tolower((unsigned char) b[i])) {
            return false;
        }
        i++;
    }
    return a[i] == '\0' && b[i] == '\0';
}

int main(void)
{
    const char *buscados[3] = { "HULDA", "hulda", "Huldo" };
    for (int i = 0; i < 3; i++) {
        printf("%s: %s\n", buscados[i], iguales_sin_mayusculas("Hulda", buscados[i]) ? "encontrada" : "no esta");
    }
    return 0;
}
```

#### Al superarla
Encontrada, encontrada. «Huldo», no. Hulda quiere saber quién es Huldo. Nadie sabe.

#### Imagen
- Una agenda abierta con el nombre Hulda resaltado tres veces.
- Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro) grita «¡HULDA!» con las manos en la boca.

### Micro-misión R05-N03-P3 · Campos con espacios

```meta
lugar: La sede del Gremio
personajes: Kira, Gheco, Tizón
carta: Leer campos separados | una línea «nombre;telefono;email» · %[^;] lee hasta el ; con espacios incluidos · validar cada campo
recompensa: xp 15, oro 15
```

#### Escena
Cada renglón que llega al Gremio dice «nombre;teléfono;email», y los nombres tienen espacios («Maese Ferrum»). Tizón quiere los tres campos bien separados.

#### Gheco sugiere
`sscanf(linea, "%29[^;];%19[^;];%39[^\n]", nombre, tel, mail)` lee los tres campos aunque tengan espacios. Si devuelve 3, están los tres.

#### Desafío
Completá el formato del `sscanf`.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    char linea[100], nombre[30], tel[20], mail[40];
    while (fgets(linea, sizeof linea, stdin) != NULL) {
        if (sscanf(linea, "___", nombre, tel, mail) == 3) {
            printf("[%s] [%s] [%s]\n", nombre, tel, mail);
        } else {
            printf("renglon incompleto\n");
        }
    }
    return 0;
}
```

#### Entrada
```
Maese Ferrum;380 4110000;ferrum@forjas.ar
Tizon;380 4229999
```

#### Salida esperada
```
[Maese Ferrum] [380 4110000] [ferrum@forjas.ar]
renglon incompleto
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    char linea[100], nombre[30], tel[20], mail[40];
    while (fgets(linea, sizeof linea, stdin) != NULL) {
        if (sscanf(linea, "%29[^;];%19[^;];%39[^\n]", nombre, tel, mail) == 3) {
            printf("[%s] [%s] [%s]\n", nombre, tel, mail);
        } else {
            printf("renglon incompleto\n");
        }
    }
    return 0;
}
```

#### Al superarla
Ferrum, completo; Tizón, sin email («no tengo», dice, «lo mido todo a mano»). La agenda los separa sin problema.

#### Imagen
- Un renglón de pergamino que se separa en tres casillas de luz.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) muestra que no tiene email, orgulloso.

### Micro-misión R05-N03-P4 · La agenda ordenada

```meta
lugar: La sede del Gremio
personajes: Kira, Gheco, Maese Ferrum
carta: El proyecto entero | array de structs + validación + qsort por nombre · cada función hace una cosa
recompensa: xp 15, oro 15
```

#### Escena
El Gremio quiere la agenda impresa, ordenada por nombre, para colgarla en la sede. Ferrum revisa que cada parte sea su propia función.

#### Gheco sugiere
`qsort` con una comparación que use `strcmp` de los nombres. Los contactos inválidos ni se agregan.

#### Desafío
Completá la comparación por nombre.

#### Código inicial
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char nombre[30];
    char telefono[20];
} Contacto;

int por_nombre(const void *a, const void *b)
{
    const Contacto *x = a;
    const Contacto *y = b;
    return ___;
}

int main(void)
{
    Contacto agenda[4] = {
        { "Tizon", "380 4229999" },
        { "Chispa", "380 4000001" },
        { "Hulda", "380 4335566" },
        { "Maese Ferrum", "380 4110000" },
    };
    qsort(agenda, 4, sizeof agenda[0], por_nombre);
    for (int i = 0; i < 4; i++) {
        printf("%-13s %s\n", agenda[i].nombre, agenda[i].telefono);
    }
    return 0;
}
```

#### Salida esperada
```
Chispa        380 4000001
Hulda         380 4335566
Maese Ferrum  380 4110000
Tizon         380 4229999
```

#### Solución
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char nombre[30];
    char telefono[20];
} Contacto;

int por_nombre(const void *a, const void *b)
{
    const Contacto *x = a;
    const Contacto *y = b;
    return strcmp(x->nombre, y->nombre);
}

int main(void)
{
    Contacto agenda[4] = {
        { "Tizon", "380 4229999" },
        { "Chispa", "380 4000001" },
        { "Hulda", "380 4335566" },
        { "Maese Ferrum", "380 4110000" },
    };
    qsort(agenda, 4, sizeof agenda[0], por_nombre);
    for (int i = 0; i < 4; i++) {
        printf("%-13s %s\n", agenda[i].nombre, agenda[i].telefono);
    }
    return 0;
}
```

#### Al superarla
La agenda cuelga en la sede del Gremio, ordenada. Chispa queda primero en la lista por primera vez en su vida. Lo festeja más que si hubiera ganado algo.

#### Imagen
- Una agenda grande clavada en la pared de la sede del Gremio, con cuatro nombres en orden.
- Chispa (mercader alto y flaco, sombrero de ala corta, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro) señala su nombre, primero, feliz.

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
agregar Tizon;380 4223344;tizon@forja.ar
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
> agregar Tizon;380 4223344;tizon@forja.ar
  Agregado.
> agregar sin datos
  Uso: agregar Nombre;Telefono;email
> listar
  Ana Paz          380 4556677    ana@correo.ar
  Ferrum           380 4001122    ferrum@forja.ar
  Tizon            380 4223344    tizon@forja.ar
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

#### Pruebas

##### Sin contactos
```entrada
listar
```
```salida
> listar
  (0 contactos)
Al volver a abrir: 0 contactos.
```

##### Un contacto
```entrada
agregar Hulda;380 1;hulda@mina.ar
listar
```
```salida
> agregar Hulda;380 1;hulda@mina.ar
  Agregado.
> listar
  Hulda            380 1          hulda@mina.ar
  (1 contactos)
Al volver a abrir: 1 contactos.
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
agregar Chispa;llamame;chispa@sombras.ar
agregar Hulda;380 4889900;hulda.mina
agregar Tizon;+54 380 4223344;tizon@forja.ar
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
> agregar Chispa;llamame;chispa@sombras.ar
  Teléfono inválido: llamame
> agregar Hulda;380 4889900;hulda.mina
  Email inválido: hulda.mina
> agregar Tizon;+54 380 4223344;tizon@forja.ar
  Agregado.
> buscar FORJA
  Ferrum           380 4001122    ferrum@forja.ar
  Tizon            +54 380 4223344 tizon@forja.ar
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
  Tizon            +54 380 4223344 tizon@forja.ar
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

#### Pruebas

##### Teléfonos al límite
```entrada
agregar A;12345;a@b.c
agregar B;123456;b@c.d
agregar C;+54-380;c@d.e
agregar D;54+380123;d@e.f
listar
```
```salida
> agregar A;12345;a@b.c
  Teléfono inválido: 12345
> agregar B;123456;b@c.d
  Agregado.
> agregar C;+54-380;c@d.e
  Teléfono inválido: +54-380
> agregar D;54+380123;d@e.f
  Teléfono inválido: 54+380123
> listar
  B                123456         b@c.d
  (1 contactos)
Al volver a abrir: 1 contactos.
```

##### Emails al límite
```entrada
agregar A;380 123456;@b.c
agregar B;380 123456;a@b
agregar C;380 123456;a@.c
agregar D;380 123456;a@b.c
listar
```
```salida
> agregar A;380 123456;@b.c
  Email inválido: @b.c
> agregar B;380 123456;a@b
  Email inválido: a@b
> agregar C;380 123456;a@.c
  Agregado.
> agregar D;380 123456;a@b.c
  Agregado.
> listar
  C                380 123456     a@.c
  D                380 123456     a@b.c
  (2 contactos)
Al volver a abrir: 2 contactos.
```

##### Buscar sin contactos
```entrada
buscar algo
borrar Nadie
```
```salida
> buscar algo
  No hay coincidencias para "algo".
> borrar Nadie
  No existe ese contacto.
Al volver a abrir: 0 contactos.
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
  Hulda R  hulda@mina.ar    mes  3
  Tizon    tizon@forja.ar   mes  7
  Ferrum   ferrum@forja.ar  mes 11
Por email:
  Ana Paz  ana@correo.ar    mes  3
  Ferrum   ferrum@forja.ar  mes 11
  Hulda R  hulda@mina.ar    mes  3
  Tizon    tizon@forja.ar   mes  7
No se puede ordenar por "telefono" (nombre, email o cumple)
Por nombre:
  Ana Paz  ana@correo.ar    mes  3
  Ferrum   ferrum@forja.ar  mes 11
  Hulda R  hulda@mina.ar    mes  3
  Tizon    tizon@forja.ar   mes  7
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
        { "Tizon", "380 4223344", "tizon@forja.ar", 7 },
        { "Hulda R", "380 4889900", "hulda@mina.ar", 3 },
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

#### Pruebas

##### Solo nombre
```entrada
nombre
```
```salida
Por nombre:
  Ana Paz  ana@correo.ar    mes  3
  Ferrum   ferrum@forja.ar  mes 11
  Hulda R  hulda@mina.ar    mes  3
  Tizon    tizon@forja.ar   mes  7
```

##### Campo desconocido
```entrada
edad
```
```salida
No se puede ordenar por "edad" (nombre, email o cumple)
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
| Tizon          |
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
        { "Tizon", "Pasaje Enano 3", "Montaña Gris" },
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
insignia_descripcion: Venciste al Dragón bajo la Montaña: resolviste FundiciónExpress, el simulacro del parcial de C, con matrices, estructuras y archivos.
usa: col.matrices, col.registros, alg.ordenamiento, arch.binarios, err.validacion
```

### Crónica

Bajo las Forjas, más hondo que las Minas, en la fragua donde se fundió el plomo del Vidriero, duerme el **Dragón bajo la Montaña**. Ronca fuego. Donde pisa, el metal se derrite. En las escamas del lomo tiene grabados **tres encargos**, y solo deja pasar a quien los resuelve.

Kira llega con la espada reforjada en la vaina y la libreta de Tizón en el bolsillo. Esta vez no toma carrera. Se sienta, lee los tres encargos y empieza a **medir**.

—Es la última prueba —dice {mentor}, y por primera vez no le da ninguna herramienta—. Todo lo que necesitás ya lo forjaste vos. Tenés tres horas; si te pasás, terminala igual. —Tizón le pasa las medidas sin que se las pida. Ella las usa sin protestar.

### Objetivos

Resolver **FundiciónExpress**, un simulacro del parcial de Programación I (UNLaR y
UTN): tres ejercicios de C con **matrices**, **arreglos de estructuras** y un
**archivo binario de estructuras**, todo con funciones, validando la entrada,
pensado para **180 minutos**.

### Antes de empezar

- Todo el camino: matrices (R02-N01), estructuras y ordenar con desempate (R02-N03 y R02-N06), archivos binarios y baja lógica (R04-N02) y el menú que no se traba (R04-N05).

### Explicación

#### Cómo se enfrenta el parcial
Son **tres ejercicios independientes**: cada uno es un programa completo, en su
propio archivo `.c`. Un plan para las tres horas:

| Minutos | Qué |
|---|---|
| 10 | leer los tres enunciados enteros y anotar qué estructuras y funciones pide cada uno |
| 50 | ejercicio 1 (la matriz) |
| 60 | ejercicio 2 (las estructuras) |
| 50 | ejercicio 3 (el archivo binario) |
| 10 | probar todo de nuevo con los datos de ejemplo y con casos borde |

Si te pasás de las tres horas, **terminalo igual**: en el simulacro no se
descuentan puntos por el tiempo. Anotá al principio de cada archivo, en un
comentario, cuánto tardaste: así sabés cuánto te falta para el parcial de verdad.

Consejos que valen puntos:
- **Una función por requerimiento.** La consigna lo pide («todas las operaciones
  mediante funciones») y además te ordena.
- **Validar en un bucle**: leer con `fgets` y `sscanf`, y volver a pedir si el
  dato no sirve. Un `scanf` que se traba con una letra es un ejercicio perdido.
- **Primero que compile y ande con un caso**, después los informes. Un programa
  que no compila no se corrige.
- **Probar con los datos de ejemplo** redirigiendo la entrada:
  `./programa < entrada.txt` (Linux) o `programa.exe < entrada.txt` (Windows).

#### Los tres encargos del Dragón
1. **Las temperaturas de los hornos** (matriz): 7 días × 4 hornos de reales,
   validados entre 0.0 y 1500.0; la tabla; el promedio de cada horno y de cada
   día; el horno más caliente; el pico con su día y su horno; un vector de
   promedios ordenado de mayor a menor **sin perder de qué horno es cada uno**;
   y buscar si algún horno supera un límite.
2. **Los aprendices de la Forja** (arreglo de estructuras): hasta 50, con legajo,
   nombre, tres notas de temple, promedio y rango; validaciones; listados;
   porcentajes por rango; el mejor promedio; ordenar por promedio descendente y,
   si empatan, por nombre; y buscar por legajo.
3. **El depósito de lingotes** (archivo binario de estructuras con menú): alta,
   listar activos, buscar por código, actualizar stock, baja lógica e informes
   (el más caro, el promedio de precios y los de stock bajo).

#### La grilla de corrección
Cada ejercicio vale lo mismo. Dentro de cada uno se mira:

| Qué | Peso |
|---|---|
| Compila sin errores ni advertencias con `-Wall -Wextra` | obligatorio |
| Las estructuras de datos pedidas (la matriz, el struct, el archivo de structs) | 20 % |
| Las validaciones (rangos, datos que no son números) | 20 % |
| Cada requerimiento resuelto, en su función | 40 % |
| La salida clara y alineada, con los datos de ejemplo | 10 % |
| Código prolijo: nombres claros, sin repetir, comentarios donde hace falta | 10 % |

El tiempo **no resta puntos**: si se pasó de los 180 minutos, se corrige igual.

#### Cómo entregarlo
Tres archivos: `hornos.c`, `aprendices.c` y `deposito.c`. Cada uno se compila
solo, en Linux (`gcc -std=c11 -Wall -Wextra hornos.c -o hornos`) o en Windows
(`gcc -std=c11 -Wall -Wextra hornos.c -o hornos.exe`), o con F9 en ZinjaI o
Code::Blocks. Se entregan los tres juntos en un `.zip`.

### ¿Para qué sirve?

Para llegar al parcial sabiendo cómo se siente: tres enunciados largos, un reloj y ningún profe al lado. Los tres ejercicios son los clásicos de la cátedra (matrices, estructuras, archivos) y también son los programas de verdad de cualquier sistema de gestión chico: planillas de mediciones, padrones de alumnos y stocks de comercios.

### Errores habituales

**Ogro: no validar.** El enunciado dice «validando que cada valor esté entre 0.0 y 100.0»: si el programa acepta 5000, ese punto se pierde, aunque todo lo demás esté perfecto.

**Ogro: ordenar el vector de promedios y perder el horno.** Si se ordena un array suelto de `float`, ya no se sabe de qué horno era cada promedio. Se ordena un array de structs `{horno, promedio}` (o de índices).

**Goblin: `scanf("%d")` con una letra.** El programa queda leyendo la misma letra para siempre. En un parcial con menú, eso es un ejercicio entero. Siempre `fgets` + `sscanf`.

**Troll: escribir en el archivo sin volver.** Después de leer un registro, para reescribirlo hay que volver con `fseek(f, -(long) sizeof r, SEEK_CUR)`. Si no, se pisa el registro siguiente.

**Ogro: el desempate al revés.** «Promedio descendente y, si empatan, nombre ascendente»: dos criterios, dos sentidos. Probalo con dos que empaten.

**Esqueleto: todo en el `main`.** Compila y anda, pero la consigna pedía funciones: se pierde la mitad del puntaje de cada requerimiento.

### Micro-misión R05-N04-P1 · Primera escama: el valor que vale

```meta
lugar: La fragua bajo la Montaña
personajes: Kira, Gheco, Tizón
criatura: dragon
carta: Leer validando | fgets + sscanf · si no es un número o está fuera de rango, avisar y volver a pedir el MISMO dato
recompensa: xp 20, oro 20
```

#### Escena
El Dragón duerme sobre el plomo del Vidriero y ronca fuego. En la primera escama del lomo hay grabado un pedido: temperaturas entre 0 y 1500 grados, y ni una que no lo sea.
Kira se sienta, saca la libreta de Tizón y empieza por lo primero: leer **bien**.

#### Gheco sugiere
`leer_valor` lee una línea con `fgets`; si `sscanf` no da un número o el número está fuera de 0.0 a 1500.0, avisa y vuelve a leer. Recién cuando el dato sirve, lo devuelve.

#### Desafío
Completá la condición del dato válido.

#### Código inicial
```c
#include <stdio.h>

double leer_valor(void)
{
    char linea[50];
    double valor;
    while (fgets(linea, sizeof linea, stdin) != NULL) {
        if (___) {
            return valor;
        }
        printf("valor invalido, de nuevo\n");
    }
    return 0.0;
}

int main(void)
{
    double a = leer_valor();
    double b = leer_valor();
    printf("aceptados: %.1f y %.1f\n", a, b);
    return 0;
}
```

#### Entrada
```
900
5000
fuego
1200
```

#### Salida esperada
```
valor invalido, de nuevo
valor invalido, de nuevo
aceptados: 900.0 y 1200.0
```

#### Solución
```c
#include <stdio.h>

double leer_valor(void)
{
    char linea[50];
    double valor;
    while (fgets(linea, sizeof linea, stdin) != NULL) {
        if (sscanf(linea, "%lf", &valor) == 1 && valor >= 0.0 && valor <= 1500.0) {
            return valor;
        }
        printf("valor invalido, de nuevo\n");
    }
    return 0.0;
}

int main(void)
{
    double a = leer_valor();
    double b = leer_valor();
    printf("aceptados: %.1f y %.1f\n", a, b);
    return 0;
}
```

#### Al superarla
La primera escama se apaga. El Dragón abre un ojo, mira a Kira, y lo vuelve a cerrar. No parece preocupado. Todavía.

#### Imagen
- El Dragón bajo la Montaña (dragón de hierro negro con escamas como placas de forja, venas de lava, alas de chapa remachada y un horno encendido en el pecho) dormido sobre un lago de plomo fundido, con una escama del lomo apagándose.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) sentada con una libreta, mirándolo sin miedo.

### Micro-misión R05-N04-P2 · Segunda escama: el pico y dónde fue

```meta
lugar: La fragua bajo la Montaña
personajes: Kira, Gheco, Tizón
criatura: dragon
carta: El mayor de una matriz con su lugar | recorrer filas y columnas · guardar la fila y la columna, no solo el valor · devolverlas por puntero
recompensa: xp 20, oro 20
```

#### Escena
La segunda escama pide el día y el horno de la temperatura más alta de la semana. —El número solo no me sirve —dice Tizón—. Necesito saber **dónde** fue, para ir a medirlo.

#### Gheco sugiere
`pico(t, &dia, &horno)` arranca con `(0, 0)` y recorre la matriz: cuando encuentra uno mayor que `t[*dia][*horno]`, guarda esa fila y esa columna.

#### Desafío
Completá la comparación y lo que se guarda.

#### Código inicial
```c
#include <stdio.h>

#define DIAS 3
#define HORNOS 4

void pico(double t[DIAS][HORNOS], int *dia, int *horno)
{
    *dia = 0;
    *horno = 0;
    for (int d = 0; d < DIAS; d++) {
        for (int h = 0; h < HORNOS; h++) {
            if (___) {
                *dia = d;
                *horno = ___;
            }
        }
    }
}

int main(void)
{
    double t[DIAS][HORNOS] = {
        { 800, 950, 700, 1000 },
        { 820, 900, 720, 1100 },
        { 860, 1180, 680, 1060 },
    };
    int dia, horno;
    pico(t, &dia, &horno);
    printf("pico: %.1f, dia %d, horno %d\n", t[dia][horno], dia + 1, horno + 1);
    return 0;
}
```

#### Salida esperada
```
pico: 1180.0, dia 3, horno 2
```

#### Solución
```c
#include <stdio.h>

#define DIAS 3
#define HORNOS 4

void pico(double t[DIAS][HORNOS], int *dia, int *horno)
{
    *dia = 0;
    *horno = 0;
    for (int d = 0; d < DIAS; d++) {
        for (int h = 0; h < HORNOS; h++) {
            if (t[d][h] > t[*dia][*horno]) {
                *dia = d;
                *horno = h;
            }
        }
    }
}

int main(void)
{
    double t[DIAS][HORNOS] = {
        { 800, 950, 700, 1000 },
        { 820, 900, 720, 1100 },
        { 860, 1180, 680, 1060 },
    };
    int dia, horno;
    pico(t, &dia, &horno);
    printf("pico: %.1f, dia %d, horno %d\n", t[dia][horno], dia + 1, horno + 1);
    return 0;
}
```

#### Al superarla
Día 3, horno 2: 1180 grados. Tizón va a medirlo y vuelve con las cejas un poco más cortas, como Ferrum. Se siente un herrero de verdad.

#### Imagen
- Una tabla de temperaturas grabada en una escama de hierro, con una celda que brilla en rojo.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) vuelve con las cejas chamuscadas, orgulloso.

### Micro-misión R05-N04-P3 · Tercera escama: ordenar sin perder el horno

```meta
lugar: La fragua bajo la Montaña
personajes: Kira, Gheco, Maese Ferrum
criatura: dragon
carta: Ordenar con su referencia | un array de structs {horno, promedio} · se intercambia el struct entero · el número viaja con su promedio
recompensa: xp 20, oro 20
```

#### Escena
La tercera escama pide los promedios de los hornos de mayor a menor. Kira ordenó el array de promedios suelto y ya no sabe de qué horno es cada uno. Ferrum gruñe: —Que el número viaje con su promedio.

#### Gheco sugiere
Con `PromedioHorno v[4]`, la burbuja compara `v[i].promedio` pero intercambia **el struct entero**: el número de horno se mueve junto con su promedio.

#### Desafío
Completá la comparación (de mayor a menor) y el intercambio.

#### Código inicial
```c
#include <stdio.h>

typedef struct {
    int horno;
    double promedio;
} PromedioHorno;

int main(void)
{
    PromedioHorno v[4] = { { 1, 845.7 }, { 2, 930.0 }, { 3, 701.4 }, { 4, 1042.9 } };
    for (int pasada = 0; pasada < 3; pasada++) {
        for (int i = 0; i < 3 - pasada; i++) {
            if (___) {
                PromedioHorno aux = v[i];
                ___;
                v[i + 1] = aux;
            }
        }
    }
    for (int i = 0; i < 4; i++) {
        printf("horno %d: %.1f\n", v[i].horno, v[i].promedio);
    }
    return 0;
}
```

#### Salida esperada
```
horno 4: 1042.9
horno 2: 930.0
horno 1: 845.7
horno 3: 701.4
```

#### Solución
```c
#include <stdio.h>

typedef struct {
    int horno;
    double promedio;
} PromedioHorno;

int main(void)
{
    PromedioHorno v[4] = { { 1, 845.7 }, { 2, 930.0 }, { 3, 701.4 }, { 4, 1042.9 } };
    for (int pasada = 0; pasada < 3; pasada++) {
        for (int i = 0; i < 3 - pasada; i++) {
            if (v[i + 1].promedio > v[i].promedio) {
                PromedioHorno aux = v[i];
                v[i] = v[i + 1];
                v[i + 1] = aux;
            }
        }
    }
    for (int i = 0; i < 4; i++) {
        printf("horno %d: %.1f\n", v[i].horno, v[i].promedio);
    }
    return 0;
}
```

#### Al superarla
Horno 4, 2, 1 y 3, cada uno con su promedio. La tercera escama se apaga y el Dragón se despierta del todo. Se levanta. Es enorme.

#### Imagen
- El Dragón bajo la Montaña (dragón de hierro negro con escamas como placas de forja, venas de lava, alas de chapa remachada y un horno encendido en el pecho) despertándose, con tres escamas apagadas en el lomo.
- Maese Ferrum (herrero humano enorme, NO es enano: mide unos dos metros, de piernas largas, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) en la entrada de la fragua, sin intervenir.

### Micro-misión R05-N04-P4 · Cuarta escama: la hoja que se mide

```meta
lugar: La fragua bajo la Montaña
personajes: Kira, Gheco, Tizón, Maese Ferrum
criatura: dragon
carta: Clasificar con varias reglas | el orden de las condiciones importa · la más exigente primero · «ninguna nota menor a 7» es un && de las tres
recompensa: xp 25, oro 25
item: Hoja Templada
```

#### Escena
El Dragón ruge y escupe fuego sobre el yunque de la fragua. Es el momento: Kira mete en el fuego el acero que guardó toda la temporada y empieza a forjar **su propia hoja**. Cada golpe se mide; cada temple se clasifica.
Tizón le pasa las medidas sin que se las pida. Ella las usa sin protestar.

#### Gheco sugiere
Primero la regla más exigente: **templada** si el promedio es 8 o más y **ninguna** de las tres medidas es menor a 7. Si no, **usable** si el promedio es 6 o más. Si no, **de vuelta al fuego**.

#### Desafío
Completá las dos condiciones.

#### Código inicial
```c
#include <stdio.h>

const char *temple(int a, int b, int c)
{
    double promedio = (a + b + c) / 3.0;
    if (___) {
        return "templada";
    } else if (___) {
        return "usable";
    }
    return "de vuelta al fuego";
}

int main(void)
{
    int a, b, c;
    while (scanf("%d %d %d", &a, &b, &c) == 3) {
        printf("%d %d %d -> %s\n", a, b, c, temple(a, b, c));
    }
    return 0;
}
```

#### Entrada
```
9 8 9
10 8 6
5 6 4
```

#### Salida esperada
```
9 8 9 -> templada
10 8 6 -> usable
5 6 4 -> de vuelta al fuego
```

#### Solución
```c
#include <stdio.h>

const char *temple(int a, int b, int c)
{
    double promedio = (a + b + c) / 3.0;
    if (promedio >= 8 && a >= 7 && b >= 7 && c >= 7) {
        return "templada";
    } else if (promedio >= 6) {
        return "usable";
    }
    return "de vuelta al fuego";
}

int main(void)
{
    int a, b, c;
    while (scanf("%d %d %d", &a, &b, &c) == 3) {
        printf("%d %d %d -> %s\n", a, b, c, temple(a, b, c));
    }
    return 0;
}
```

#### Al superarla
La primera medida da «templada». Kira saca la hoja del agua: brilla con un filo cian, medida grado por grado. Es **la Hoja Templada**, forjada por ella misma, y va a tu mochila. Ferrum no dice nada. Golpea el yunque dos veces. Después, una tercera.

#### Imagen
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) saca del agua una espada que brilla con un filo cian, envuelta en vapor.
- El Dragón bajo la Montaña (dragón de hierro negro con escamas como placas de forja, venas de lava, alas de chapa remachada y un horno encendido en el pecho) retrocede ante el brillo.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) sostiene la libreta abierta con las medidas.
- Maese Ferrum (herrero humano enorme, NO es enano: mide unos dos metros, de piernas largas, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) golpea el yunque.

### Micro-misión R05-N04-P5 · La última escama

```meta
lugar: La fragua bajo la Montaña
personajes: Kira, Gheco, Tizón, Maese Ferrum
criatura: dragon
carta: El parcial entero | matriz + estructuras + archivo · validar, recorrer, ordenar, dar de baja · cada pieza en su función, y tres horas para todo
recompensa: xp 30, oro 40
item: Matriz del Marco
```

#### Escena
La última escama es la del corazón. Para apagarla hay que dar de baja, en el registro de la fragua, las piezas falsas que el Dragón fue tragando (las de temperatura imposible), sin borrar ninguna, y contar las que quedan.

#### Gheco sugiere
Se recorre el archivo con `"r+b"`: a cada pieza con temperatura mayor a 1500 se le pone `'B'`, se vuelve con `fseek` y se reescribe; entre escribir y leer de nuevo va un `fseek(f, 0, SEEK_CUR)`. Después se cuentan las activas.

#### Desafío
Completá la vuelta atrás y el conteo de activas.

#### Código inicial
```c
#include <stdio.h>

typedef struct {
    int codigo;
    double grados;
    char estado;
} Pieza;

int main(void)
{
    Pieza p[5] = { { 1, 900, 'A' }, { 2, 99999, 'A' }, { 3, 1200, 'A' }, { 4, 7000, 'A' }, { 5, 850, 'A' } };
    FILE *f = fopen("fragua.dat", "wb");
    if (f == NULL) {
        return 1;
    }
    fwrite(p, sizeof p[0], 5, f);
    fclose(f);

    f = fopen("fragua.dat", "r+b");
    if (f == NULL) {
        return 1;
    }
    Pieza x;
    while (fread(&x, sizeof x, 1, f) == 1) {
        if (x.grados > 1500 && x.estado == 'A') {
            x.estado = 'B';
            fseek(f, ___, SEEK_CUR);
            fwrite(&x, sizeof x, 1, f);
            fseek(f, 0, SEEK_CUR);
        }
    }
    rewind(f);
    int activas = 0;
    while (fread(&x, sizeof x, 1, f) == 1) {
        if (___) {
            activas++;
        }
    }
    fclose(f);
    printf("piezas activas: %d de 5\n", activas);
    if (activas == 3) {
        printf("la ultima escama se apaga\n");
    }
    return 0;
}
```

#### Salida esperada
```
piezas activas: 3 de 5
la ultima escama se apaga
```

#### Solución
```c
#include <stdio.h>

typedef struct {
    int codigo;
    double grados;
    char estado;
} Pieza;

int main(void)
{
    Pieza p[5] = { { 1, 900, 'A' }, { 2, 99999, 'A' }, { 3, 1200, 'A' }, { 4, 7000, 'A' }, { 5, 850, 'A' } };
    FILE *f = fopen("fragua.dat", "wb");
    if (f == NULL) {
        return 1;
    }
    fwrite(p, sizeof p[0], 5, f);
    fclose(f);

    f = fopen("fragua.dat", "r+b");
    if (f == NULL) {
        return 1;
    }
    Pieza x;
    while (fread(&x, sizeof x, 1, f) == 1) {
        if (x.grados > 1500 && x.estado == 'A') {
            x.estado = 'B';
            fseek(f, -(long) sizeof x, SEEK_CUR);
            fwrite(&x, sizeof x, 1, f);
            fseek(f, 0, SEEK_CUR);
        }
    }
    rewind(f);
    int activas = 0;
    while (fread(&x, sizeof x, 1, f) == 1) {
        if (x.estado == 'A') {
            activas++;
        }
    }
    fclose(f);
    printf("piezas activas: %d de 5\n", activas);
    if (activas == 3) {
        printf("la ultima escama se apaga\n");
    }
    return 0;
}
```

#### Al superarla
La última escama se apaga y el Dragón bajo la Montaña se echa, manso, a un costado del lago de plomo. Detrás de él hay un molde enorme: **la Matriz del Marco** que dejó el Vidriero, con la inscripción *«para quien llegue»*. Va a tu mochila. Ferrum la mira largo rato. —Este es el marco —dice—. El mismo que dicen que espera en la torre más alta del Imperio.

#### Imagen
- El Dragón bajo la Montaña (dragón de hierro negro con escamas como placas de forja, venas de lava, alas de chapa remachada y un horno encendido en el pecho) echado y manso junto a un lago de plomo, con todas las escamas apagadas.
- Un molde de plomo enorme con forma de marco de vitral y la inscripción «para quien llegue».
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) con la Hoja Templada en la mano, frente al molde.
- Maese Ferrum (herrero humano enorme, NO es enano: mide unos dos metros, de piernas largas, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) y Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) detrás, en silencio.

### Misión R05-N04-M1 · Encargo 1: las temperaturas de los hornos

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

La Forja registra durante **7 días** la temperatura de **4 hornos**. Escribí
`hornos.c`:

1. Declará una **matriz de reales** de 7 × 4.
2. Cargá las mediciones (día por día, horno por horno, una por línea) **validando**
   que cada valor esté entre 0.0 y 1500.0: si no lo está (o no es un número),
   avisá y volvé a pedir ese mismo valor.
3. Mostrá la matriz como tabla.
4. Informá: el promedio de cada horno; el promedio de cada día; el horno con
   mayor promedio semanal; y el día en que se registró la mayor temperatura,
   con su horno.
5. Generá un **vector** con los promedios semanales de los 4 hornos y ordenalo de
   mayor a menor **sin perder qué horno es cada uno**.
6. Leé un **límite** y buscá, con una función, si algún horno tiene promedio
   mayor a ese límite (mostrá el primero en el vector ordenado, o que ninguno).
7. Todo el procesamiento en **funciones**.

#### Criterio de aprobación

- Usa una matriz `float` (o `double`) de 7 × 4 y valida cada valor entre 0.0 y 1500.0, repitiendo el pedido.
- Muestra la tabla y los promedios por horno y por día, con dos decimales.
- Informa el horno más caliente y el pico con su día y su horno.
- Ordena un vector de structs (o de índices) sin perder el horno, de mayor a menor.
- La búsqueda por límite está en una función.
- Cada requerimiento está en su propia función.

#### Entrada de ejemplo

```
800
950
700
1000
820
900
5000
720
1100
860
910
680
1060
840
930
hola
710
990
870
940
690
1020
880
960
700
1080
850
920
-3
710
1050
950
```

#### Salida esperada

```
Dia 2, horno 3: valor invalido, de nuevo
Dia 4, horno 3: valor invalido, de nuevo
Dia 7, horno 3: valor invalido, de nuevo

Dia     Horno 1  Horno 2  Horno 3  Horno 4
1         800.0    950.0    700.0   1000.0
2         820.0    900.0    720.0   1100.0
3         860.0    910.0    680.0   1060.0
4         840.0    930.0    710.0    990.0
5         870.0    940.0    690.0   1020.0
6         880.0    960.0    700.0   1080.0
7         850.0    920.0    710.0   1050.0

Promedio por horno:
  horno 1: 845.71
  horno 2: 930.00
  horno 3: 701.43
  horno 4: 1042.86
Promedio por dia:
  dia 1: 862.50
  dia 2: 885.00
  dia 3: 877.50
  dia 4: 867.50
  dia 5: 880.00
  dia 6: 905.00
  dia 7: 882.50
Horno mas caliente: 4 (1042.86)
Pico: 1100.0, dia 2, horno 4
Promedios ordenados:
  horno 4: 1042.86
  horno 2: 930.00
  horno 1: 845.71
  horno 3: 701.43
Limite:
El horno 4 supera 950.0 (1042.86)
```

#### Solución de referencia

```c
/*
 * FundicionExpress - Encargo 1: las temperaturas de los hornos.
 * Matriz de 7 dias x 4 hornos, validada entre 0.0 y 1500.0.
 * Tiempo: anotar aca cuanto tardaste.
 */
#include <stdio.h>

#define DIAS 7
#define HORNOS 4
#define MINIMO 0.0
#define MAXIMO 1500.0

typedef struct {
    int horno;          /* 1 a 4 */
    double promedio;
} PromedioHorno;

double leer_valor(int dia, int horno)
{
    char linea[50];
    double valor;
    while (1) {
        if (fgets(linea, sizeof linea, stdin) == NULL) {
            return MINIMO;                       /* sin mas datos */
        }
        if (sscanf(linea, "%lf", &valor) == 1 && valor >= MINIMO && valor <= MAXIMO) {
            return valor;
        }
        printf("Dia %d, horno %d: valor invalido, de nuevo\n", dia, horno);
    }
}

void cargar(double t[DIAS][HORNOS])
{
    for (int d = 0; d < DIAS; d++) {
        for (int h = 0; h < HORNOS; h++) {
            t[d][h] = leer_valor(d + 1, h + 1);
        }
    }
}

void mostrar(double t[DIAS][HORNOS])
{
    printf("\n%-6s", "Dia");
    for (int h = 0; h < HORNOS; h++) {
        printf("  Horno %d", h + 1);
    }
    printf("\n");
    for (int d = 0; d < DIAS; d++) {
        printf("%-6d", d + 1);
        for (int h = 0; h < HORNOS; h++) {
            printf(" %8.1f", t[d][h]);
        }
        printf("\n");
    }
}

double promedio_horno(double t[DIAS][HORNOS], int h)
{
    double suma = 0;
    for (int d = 0; d < DIAS; d++) {
        suma += t[d][h];
    }
    return suma / DIAS;
}

double promedio_dia(double t[DIAS][HORNOS], int d)
{
    double suma = 0;
    for (int h = 0; h < HORNOS; h++) {
        suma += t[d][h];
    }
    return suma / HORNOS;
}

void pico(double t[DIAS][HORNOS], int *dia, int *horno)
{
    *dia = 0;
    *horno = 0;
    for (int d = 0; d < DIAS; d++) {
        for (int h = 0; h < HORNOS; h++) {
            if (t[d][h] > t[*dia][*horno]) {
                *dia = d;
                *horno = h;
            }
        }
    }
}

void ordenar_desc(PromedioHorno v[], int n)
{
    for (int pasada = 0; pasada < n - 1; pasada++) {
        for (int i = 0; i < n - 1 - pasada; i++) {
            if (v[i + 1].promedio > v[i].promedio) {
                PromedioHorno aux = v[i];
                v[i] = v[i + 1];
                v[i + 1] = aux;
            }
        }
    }
}

int buscar_mayor_a(const PromedioHorno v[], int n, double limite)
{
    for (int i = 0; i < n; i++) {
        if (v[i].promedio > limite) {
            return i;
        }
    }
    return -1;
}

int main(void)
{
    double t[DIAS][HORNOS];
    cargar(t);
    mostrar(t);

    PromedioHorno v[HORNOS];
    printf("\nPromedio por horno:\n");
    for (int h = 0; h < HORNOS; h++) {
        v[h].horno = h + 1;
        v[h].promedio = promedio_horno(t, h);
        printf("  horno %d: %.2f\n", h + 1, v[h].promedio);
    }
    printf("Promedio por dia:\n");
    for (int d = 0; d < DIAS; d++) {
        printf("  dia %d: %.2f\n", d + 1, promedio_dia(t, d));
    }

    ordenar_desc(v, HORNOS);
    printf("Horno mas caliente: %d (%.2f)\n", v[0].horno, v[0].promedio);
    int dia, horno;
    pico(t, &dia, &horno);
    printf("Pico: %.1f, dia %d, horno %d\n", t[dia][horno], dia + 1, horno + 1);

    printf("Promedios ordenados:\n");
    for (int i = 0; i < HORNOS; i++) {
        printf("  horno %d: %.2f\n", v[i].horno, v[i].promedio);
    }

    char linea[50];
    double limite;
    printf("Limite: ");
    if (fgets(linea, sizeof linea, stdin) != NULL && sscanf(linea, "%lf", &limite) == 1) {
        int i = buscar_mayor_a(v, HORNOS, limite);
        if (i == -1) {
            printf("\nNingun horno supera %.1f\n", limite);
        } else {
            printf("\nEl horno %d supera %.1f (%.2f)\n", v[i].horno, limite, v[i].promedio);
        }
    }
    return 0;
}
```

#### Pruebas

##### Ningún horno supera el límite
```entrada
100
100
100
100
200
200
200
200
300
300
300
300
400
400
400
400
500
500
500
500
600
600
600
600
700
700
700
700
1500
```
```salida
Dia     Horno 1  Horno 2  Horno 3  Horno 4
1         100.0    100.0    100.0    100.0
2         200.0    200.0    200.0    200.0
3         300.0    300.0    300.0    300.0
4         400.0    400.0    400.0    400.0
5         500.0    500.0    500.0    500.0
6         600.0    600.0    600.0    600.0
7         700.0    700.0    700.0    700.0

Promedio por horno:
  horno 1: 400.00
  horno 2: 400.00
  horno 3: 400.00
  horno 4: 400.00
Promedio por dia:
  dia 1: 100.00
  dia 2: 200.00
  dia 3: 300.00
  dia 4: 400.00
  dia 5: 500.00
  dia 6: 600.00
  dia 7: 700.00
Horno mas caliente: 1 (400.00)
Pico: 700.0, dia 7, horno 1
Promedios ordenados:
  horno 1: 400.00
  horno 2: 400.00
  horno 3: 400.00
  horno 4: 400.00
Limite:
Ningun horno supera 1500.0
```

### Misión R05-N04-M2 · Encargo 2: los aprendices de la Forja

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Escribí `aprendices.c` para registrar a los aprendices de la Forja con un
**arreglo de estructuras** (hasta **50**). Cada aprendiz tiene legajo, apellido y
nombre, tres notas de temple, promedio y **rango**.

1. Cargá primero la cantidad y después un aprendiz por línea:
   `legajo;nombre;nota1;nota2;nota3`.
2. **Validá**: legajo mayor que 0 y notas entre 0 y 10. Un renglón que no cumple
   se informa y se descarta.
3. Calculá el promedio de cada uno.
4. El rango: **oficial** si el promedio es 8 o más y ninguna nota es menor a 7;
   **aprendiz** si el promedio es 6 o más; **de vuelta al fuelle** si es menor a 6.
5. Mostrá: el listado completo; los oficiales; el de mayor promedio; y el
   porcentaje de aprendices en cada rango.
6. Ordená el arreglo por promedio **descendente** y, si empatan, por nombre
   **ascendente**, y mostralo.
7. Leé un legajo y buscalo con una función: mostrá todos sus datos o que no existe.

#### Criterio de aprobación

- Usa un arreglo de structs con tope 50 y una cantidad cargada.
- Valida el legajo y las notas, y descarta el renglón inválido con un aviso.
- Calcula el promedio y el rango con las reglas de la consigna.
- Muestra el listado, los oficiales, el mejor promedio y los porcentajes.
- Ordena con desempate por nombre y busca por legajo, cada cosa en su función.

#### Entrada de ejemplo

```
6
101;Kira;9;8;9
102;Tizon;10;8;6
0;Nadie;5;5;5
103;Hulda;8;9;9
104;Chispa;5;6;4
105;Brasa;7;6;6
103
```

#### Salida esperada

```
Renglon descartado: 0;Nadie;5;5;5
Listado:
   101 Kira      9  8  9   8.67  oficial
   102 Tizon    10  8  6   8.00  aprendiz
   103 Hulda     8  9  9   8.67  oficial
   104 Chispa    5  6  4   5.00  de vuelta al fuelle
   105 Brasa     7  6  6   6.33  aprendiz
Oficiales:
   101 Kira      9  8  9   8.67  oficial
   103 Hulda     8  9  9   8.67  oficial
Mejor promedio: Kira (8.67)
Porcentajes:
  oficial               40.0 %
  aprendiz              40.0 %
  de vuelta al fuelle   20.0 %
Ordenados:
   103 Hulda     8  9  9   8.67  oficial
   101 Kira      9  8  9   8.67  oficial
   102 Tizon    10  8  6   8.00  aprendiz
   105 Brasa     7  6  6   6.33  aprendiz
   104 Chispa    5  6  4   5.00  de vuelta al fuelle
Legajo 103:
   103 Hulda     8  9  9   8.67  oficial
```

#### Solución de referencia

```c
/*
 * FundicionExpress - Encargo 2: los aprendices de la Forja.
 * Arreglo de estructuras con validacion, rango, porcentajes,
 * ordenamiento con desempate y busqueda por legajo.
 */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define TOPE 50

typedef struct {
    int legajo;
    char nombre[30];
    int notas[3];
    double promedio;
    char rango[20];
} Aprendiz;

bool leer_aprendiz(const char *linea, Aprendiz *a)
{
    if (sscanf(linea, "%d;%29[^;];%d;%d;%d", &a->legajo, a->nombre, &a->notas[0], &a->notas[1], &a->notas[2]) != 5) {
        return false;
    }
    if (a->legajo <= 0) {
        return false;
    }
    for (int i = 0; i < 3; i++) {
        if (a->notas[i] < 0 || a->notas[i] > 10) {
            return false;
        }
    }
    return true;
}

void calcular(Aprendiz *a)
{
    a->promedio = (a->notas[0] + a->notas[1] + a->notas[2]) / 3.0;
    bool alguna_baja = a->notas[0] < 7 || a->notas[1] < 7 || a->notas[2] < 7;
    if (a->promedio >= 8 && !alguna_baja) {
        strcpy(a->rango, "oficial");
    } else if (a->promedio >= 6) {
        strcpy(a->rango, "aprendiz");
    } else {
        strcpy(a->rango, "de vuelta al fuelle");
    }
}

void mostrar(const Aprendiz *a)
{
    printf("  %4d %-8s %2d %2d %2d  %5.2f  %s\n", a->legajo, a->nombre,
           a->notas[0], a->notas[1], a->notas[2], a->promedio, a->rango);
}

void listar(const Aprendiz v[], int n, const char *filtro)
{
    for (int i = 0; i < n; i++) {
        if (filtro == NULL || strcmp(v[i].rango, filtro) == 0) {
            mostrar(&v[i]);
        }
    }
}

int mejor(const Aprendiz v[], int n)
{
    int m = 0;
    for (int i = 1; i < n; i++) {
        if (v[i].promedio > v[m].promedio) {
            m = i;
        }
    }
    return m;
}

void porcentajes(const Aprendiz v[], int n)
{
    const char *rangos[3] = { "oficial", "aprendiz", "de vuelta al fuelle" };
    for (int r = 0; r < 3; r++) {
        int c = 0;
        for (int i = 0; i < n; i++) {
            if (strcmp(v[i].rango, rangos[r]) == 0) {
                c++;
            }
        }
        printf("  %-20s %5.1f %%\n", rangos[r], 100.0 * c / n);
    }
}

bool va_antes(const Aprendiz *a, const Aprendiz *b)
{
    if (a->promedio != b->promedio) {
        return a->promedio > b->promedio;
    }
    return strcmp(a->nombre, b->nombre) < 0;
}

void ordenar(Aprendiz v[], int n)
{
    for (int pasada = 0; pasada < n - 1; pasada++) {
        for (int i = 0; i < n - 1 - pasada; i++) {
            if (va_antes(&v[i + 1], &v[i])) {
                Aprendiz aux = v[i];
                v[i] = v[i + 1];
                v[i + 1] = aux;
            }
        }
    }
}

int buscar(const Aprendiz v[], int n, int legajo)
{
    for (int i = 0; i < n; i++) {
        if (v[i].legajo == legajo) {
            return i;
        }
    }
    return -1;
}

int main(void)
{
    Aprendiz v[TOPE];
    int n = 0, cantidad = 0;
    char linea[100];
    if (fgets(linea, sizeof linea, stdin) == NULL || sscanf(linea, "%d", &cantidad) != 1) {
        return 1;
    }
    for (int k = 0; k < cantidad && n < TOPE; k++) {
        if (fgets(linea, sizeof linea, stdin) == NULL) {
            break;
        }
        linea[strcspn(linea, "\n")] = '\0';
        if (leer_aprendiz(linea, &v[n])) {
            calcular(&v[n]);
            n++;
        } else {
            printf("Renglon descartado: %s\n", linea);
        }
    }
    if (n == 0) {
        printf("No hay aprendices.\n");
        return 0;
    }

    printf("Listado:\n");
    listar(v, n, NULL);
    printf("Oficiales:\n");
    listar(v, n, "oficial");
    int m = mejor(v, n);
    printf("Mejor promedio: %s (%.2f)\n", v[m].nombre, v[m].promedio);
    printf("Porcentajes:\n");
    porcentajes(v, n);

    ordenar(v, n);
    printf("Ordenados:\n");
    listar(v, n, NULL);

    int legajo;
    if (fgets(linea, sizeof linea, stdin) != NULL && sscanf(linea, "%d", &legajo) == 1) {
        int i = buscar(v, n, legajo);
        if (i == -1) {
            printf("Legajo %d: no existe\n", legajo);
        } else {
            printf("Legajo %d:\n", legajo);
            mostrar(&v[i]);
        }
    }
    return 0;
}
```

#### Pruebas

##### Empate y legajo que no existe
```entrada
3
7;Zoe;8;8;8
5;Ana;8;8;8
9;Ivo;3;4;2
4
```
```salida
Listado:
     7 Zoe       8  8  8   8.00  oficial
     5 Ana       8  8  8   8.00  oficial
     9 Ivo       3  4  2   3.00  de vuelta al fuelle
Oficiales:
     7 Zoe       8  8  8   8.00  oficial
     5 Ana       8  8  8   8.00  oficial
Mejor promedio: Zoe (8.00)
Porcentajes:
  oficial               66.7 %
  aprendiz               0.0 %
  de vuelta al fuelle   33.3 %
Ordenados:
     5 Ana       8  8  8   8.00  oficial
     7 Zoe       8  8  8   8.00  oficial
     9 Ivo       3  4  2   3.00  de vuelta al fuelle
Legajo 4: no existe
```

### Misión R05-N04-M3 · Encargo 3: el depósito de lingotes

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Escribí `deposito.c` para administrar un **archivo binario de estructuras**
(`lingotes.dat`). Cada lingote tiene código, descripción, precio, stock y
**estado** (`'A'` activo, `'B'` baja lógica). Con un **menú** de opciones:

1. Crear el archivo e ingresar lingotes (`codigo;descripcion;precio;stock`,
   uno por línea, hasta una línea con `fin`).
2. Listar los lingotes activos.
3. Buscar un lingote por código.
4. Actualizar el stock de un lingote (se suma la cantidad, que puede ser negativa).
5. Dar de **baja lógica** un lingote.
6. Mostrar: el lingote con mayor precio, el promedio de precios y cuántos tienen
   stock menor a 10 (solo los activos).
0. Salir.

El menú no se tiene que trabar si se escribe cualquier cosa.

#### Criterio de aprobación

- Usa un struct con estado y un archivo binario con `fwrite` y `fread`.
- Actualizar y dar de baja reescriben el registro en su lugar (`fseek`), sin rehacer el archivo.
- Los listados e informes muestran solo los activos.
- El menú lee con `fgets` + `sscanf` y no se traba con letras.
- Cada opción está en su propia función.

#### Entrada de ejemplo

```
1
7;Plomo;9.5;40
12;Hierro;5.0;8
3;Oro;40.0;2
21;Cobre;12.0;15
fin
2
4
12 5
5
3
2
6
3
21
9
0
```

#### Salida esperada

```
[1] crear [2] listar [3] buscar [4] stock [5] baja [6] informes [0] salir
Opcion:
4 lingotes cargados.

[1] crear [2] listar [3] buscar [4] stock [5] baja [6] informes [0] salir
Opcion:
Activos:
    7 Plomo       9.50   40
   12 Hierro      5.00    8
    3 Oro        40.00    2
   21 Cobre      12.00   15

[1] crear [2] listar [3] buscar [4] stock [5] baja [6] informes [0] salir
Opcion:
Codigo y cantidad:
Stock de Hierro: 13

[1] crear [2] listar [3] buscar [4] stock [5] baja [6] informes [0] salir
Opcion:
Codigo:
Oro dado de baja.

[1] crear [2] listar [3] buscar [4] stock [5] baja [6] informes [0] salir
Opcion:
Activos:
    7 Plomo       9.50   40
   12 Hierro      5.00   13
   21 Cobre      12.00   15

[1] crear [2] listar [3] buscar [4] stock [5] baja [6] informes [0] salir
Opcion:
Mas caro: Cobre (12.00)
Promedio de precios: 8.83
Con stock menor a 10: 0

[1] crear [2] listar [3] buscar [4] stock [5] baja [6] informes [0] salir
Opcion:
Codigo:
   21 Cobre      12.00   15

[1] crear [2] listar [3] buscar [4] stock [5] baja [6] informes [0] salir
Opcion:
La opcion 9 no existe.

[1] crear [2] listar [3] buscar [4] stock [5] baja [6] informes [0] salir
Opcion:
Hasta luego.
```

#### Solución de referencia

```c
/*
 * FundicionExpress - Encargo 3: el deposito de lingotes.
 * Archivo binario de estructuras con alta, listado, busqueda, actualizacion
 * de stock, baja logica e informes, con un menu que no se traba.
 */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define ARCHIVO "lingotes.dat"

typedef struct {
    int codigo;
    char descripcion[30];
    float precio;
    int stock;
    char estado;
} Lingote;

bool leer_linea(char *linea, int tam)
{
    if (fgets(linea, tam, stdin) == NULL) {
        return false;
    }
    linea[strcspn(linea, "\n")] = '\0';
    return true;
}

int leer_entero(void)
{
    char linea[50];
    int x;
    while (leer_linea(linea, sizeof linea)) {
        if (sscanf(linea, "%d", &x) == 1) {
            return x;
        }
        printf("Eso no es un numero.\n");
    }
    return 0;
}

void crear(void)
{
    FILE *f = fopen(ARCHIVO, "wb");
    if (f == NULL) {
        printf("No se pudo crear el archivo.\n");
        return;
    }
    char linea[80];
    int cargados = 0;
    while (leer_linea(linea, sizeof linea) && strcmp(linea, "fin") != 0) {
        Lingote l;
        if (sscanf(linea, "%d;%29[^;];%f;%d", &l.codigo, l.descripcion, &l.precio, &l.stock) == 4 && l.codigo > 0) {
            l.estado = 'A';
            fwrite(&l, sizeof l, 1, f);
            cargados++;
        } else {
            printf("Renglon invalido: %s\n", linea);
        }
    }
    fclose(f);
    printf("%d lingotes cargados.\n", cargados);
}

void mostrar(const Lingote *l)
{
    printf("  %3d %-8s %7.2f %4d\n", l->codigo, l->descripcion, l->precio, l->stock);
}

void listar(void)
{
    FILE *f = fopen(ARCHIVO, "rb");
    if (f == NULL) {
        printf("No hay archivo.\n");
        return;
    }
    Lingote l;
    printf("Activos:\n");
    while (fread(&l, sizeof l, 1, f) == 1) {
        if (l.estado == 'A') {
            mostrar(&l);
        }
    }
    fclose(f);
}

/* Deja el archivo posicionado al principio del registro encontrado. */
bool buscar_en(FILE *f, int codigo, Lingote *l)
{
    rewind(f);
    while (fread(l, sizeof *l, 1, f) == 1) {
        if (l->codigo == codigo && l->estado == 'A') {
            fseek(f, -(long) sizeof *l, SEEK_CUR);
            return true;
        }
    }
    return false;
}

void buscar(void)
{
    printf("Codigo: ");
    int codigo = leer_entero();
    FILE *f = fopen(ARCHIVO, "rb");
    Lingote l;
    if (f != NULL && buscar_en(f, codigo, &l)) {
        printf("\n");
        mostrar(&l);
    } else {
        printf("\nNo existe el codigo %d.\n", codigo);
    }
    if (f != NULL) {
        fclose(f);
    }
}

void actualizar_stock(void)
{
    printf("Codigo y cantidad: ");
    char linea[50];
    int codigo, cantidad;
    if (!leer_linea(linea, sizeof linea) || sscanf(linea, "%d %d", &codigo, &cantidad) != 2) {
        printf("\nDatos invalidos.\n");
        return;
    }
    FILE *f = fopen(ARCHIVO, "r+b");
    Lingote l;
    if (f != NULL && buscar_en(f, codigo, &l)) {
        l.stock += cantidad;
        fwrite(&l, sizeof l, 1, f);
        printf("\nStock de %s: %d\n", l.descripcion, l.stock);
    } else {
        printf("\nNo existe el codigo %d.\n", codigo);
    }
    if (f != NULL) {
        fclose(f);
    }
}

void baja(void)
{
    printf("Codigo: ");
    int codigo = leer_entero();
    FILE *f = fopen(ARCHIVO, "r+b");
    Lingote l;
    if (f != NULL && buscar_en(f, codigo, &l)) {
        l.estado = 'B';
        fwrite(&l, sizeof l, 1, f);
        printf("\n%s dado de baja.\n", l.descripcion);
    } else {
        printf("\nNo existe el codigo %d.\n", codigo);
    }
    if (f != NULL) {
        fclose(f);
    }
}

void informes(void)
{
    FILE *f = fopen(ARCHIVO, "rb");
    if (f == NULL) {
        printf("No hay archivo.\n");
        return;
    }
    Lingote l, caro;
    int n = 0, bajo_stock = 0;
    double suma = 0;
    while (fread(&l, sizeof l, 1, f) == 1) {
        if (l.estado != 'A') {
            continue;
        }
        if (n == 0 || l.precio > caro.precio) {
            caro = l;
        }
        suma += l.precio;
        n++;
        if (l.stock < 10) {
            bajo_stock++;
        }
    }
    fclose(f);
    if (n == 0) {
        printf("No hay lingotes activos.\n");
        return;
    }
    printf("Mas caro: %s (%.2f)\n", caro.descripcion, caro.precio);
    printf("Promedio de precios: %.2f\n", suma / n);
    printf("Con stock menor a 10: %d\n", bajo_stock);
}

int main(void)
{
    int opcion = -1;
    while (opcion != 0) {
        printf("\n[1] crear [2] listar [3] buscar [4] stock [5] baja [6] informes [0] salir\nOpcion: ");
        char linea[50];
        if (!leer_linea(linea, sizeof linea)) {
            break;
        }
        if (sscanf(linea, "%d", &opcion) != 1) {
            printf("\nEso no es una opcion.\n");
            opcion = -1;
            continue;
        }
        printf("\n");
        switch (opcion) {
        case 1: crear(); break;
        case 2: listar(); break;
        case 3: buscar(); break;
        case 4: actualizar_stock(); break;
        case 5: baja(); break;
        case 6: informes(); break;
        case 0: printf("Hasta luego.\n"); break;
        default: printf("La opcion %d no existe.\n", opcion);
        }
    }
    return 0;
}
```

#### Pruebas

##### Opciones raras y archivo vacío
```entrada
hola
8
1
fin
2
6
0
```
```salida
[1] crear [2] listar [3] buscar [4] stock [5] baja [6] informes [0] salir
Opcion:
Eso no es una opcion.

[1] crear [2] listar [3] buscar [4] stock [5] baja [6] informes [0] salir
Opcion:
La opcion 8 no existe.

[1] crear [2] listar [3] buscar [4] stock [5] baja [6] informes [0] salir
Opcion:
0 lingotes cargados.

[1] crear [2] listar [3] buscar [4] stock [5] baja [6] informes [0] salir
Opcion:
Activos:

[1] crear [2] listar [3] buscar [4] stock [5] baja [6] informes [0] salir
Opcion:
No hay lingotes activos.

[1] crear [2] listar [3] buscar [4] stock [5] baja [6] informes [0] salir
Opcion:
Hasta luego.
```

### Encargo R05-N04-E1 · El simulacro de verdad, con reloj

```meta
entrega: archivo
entorno: local
monedas: 1
xp: 40
extensiones: zip
```

#### Consigna

Volvé a resolver **los tres encargos** de FundiciónExpress desde cero, en tu compu
(ZinjaI, Code::Blocks o VS Code, en Linux o en Windows), como en el parcial: con
un reloj, sin mirar tus soluciones anteriores y en una sola sentada. Al principio
de cada archivo, en un comentario, anotá a qué hora empezaste y a qué hora
terminaste ese ejercicio.

Entregá un `.zip` con `hornos.c`, `aprendices.c` y `deposito.c`.

#### Criterio de aprobación

- Los tres programas compilan con `-Wall -Wextra` sin advertencias.
- Cada uno anda con los datos de ejemplo de su misión.
- Cada archivo dice cuánto se tardó. El tiempo **no resta puntos**: sirve para saber cuánto falta para el parcial.

### Prueba del sello

#### ¿Cómo se ordena un vector de promedios sin perder de qué horno es cada uno?

Ordenando un array de structs `{horno, promedio}` (el número viaja con su promedio) o un array de índices, en lugar de un array suelto de promedios.

#### ¿Qué hace falta para ordenar «por promedio descendente y, si empatan, por nombre ascendente»?

Una función de comparación con dos criterios: primero el promedio (mayor primero); si son iguales, `strcmp` de los nombres (menor primero).

#### ¿Por qué la baja de un lingote es «lógica» y no se borra el registro?

Porque borrar del medio de un archivo binario obliga a reescribir todo lo que sigue. Se cambia el estado a `'B'`, se reescribe ese registro en su lugar, y los listados muestran solo los activos.

#### ¿Qué pasa si, después de leer un registro con `fread`, se escribe sin `fseek`?

Se pisa el registro **siguiente**: después del `fread`, el archivo quedó al final del registro leído. Hay que volver con `fseek(f, -(long) sizeof r, SEEK_CUR)`.

#### ¿Por qué el menú lee con `fgets` + `sscanf` y no con `scanf("%d")`?

Porque con una letra, `scanf("%d")` no la consume y el menú se traba leyéndola para siempre. Con `fgets` la línea se consume entera y `sscanf` dice si era un número.

#### Si te pasaste de los 180 minutos, ¿qué hacés?

Lo terminás igual: en el simulacro no se descuentan puntos por el tiempo. Se anota cuánto se tardó, para saber cuánto falta para el parcial.

### Soluciones (docente)

Simulacro del parcial de Programación I (2026-10-08), con el formato de los parciales de la UTN La Rioja (matrices, arreglos de estructuras y archivos binarios con menú) y de la UNLaR. Pensado para 180 minutos y sin penalizar si se pasa: el alumno anota cuánto tardó. Antes, este nodo era la mazmorra del Dragón (un juego con la matriz del mapa, los guardianes y la partida guardada en binario).
## R05-N05 · La Encrucijada del Yunque

```meta
tipo: ventana
padre: R05-N04
precio: 10
```

### Crónica

Kira sale de la fragua con **la Hoja Templada**, la espada que forjó ella misma midiendo cada grado, y con **la Matriz del Marco** que dejó el Vidriero: el molde de plomo de un vitral enorme, con la inscripción *«para quien llegue»*. El mismo marco que, dicen los mercaderes, espera vacío en la torre más alta del Imperio.

En la entrada de las Forjas hay un yunque viejo y de él salen dos caminos. {mentor} golpea el yunque **tres veces**. Kira no sabe qué hacer con las manos. En la pared, debajo de la cuenta de espadazos, Ferrum escribe con tiza: «Problemas resueltos midiendo: todos».

—Ya hablás la lengua de las Forjas. Lo que sigue no es obligatorio: es **tuyo**. Por un camino, la **Forja Viva**, donde el metal se mueve en una pantalla. Por el otro, el **Taller de los Autómatas**, donde el código mueve cosas de verdad. —Tizón, ahora oficial, la saluda desde el mostrador con el calibre en alto.

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

### Micro-misión R05-N05-P1 · La cuenta de la pared

```meta
lugar: La Encrucijada del Yunque
personajes: Kira, Gheco, Maese Ferrum, Tizón
carta: Mirar hacia atrás | todo lo que se forjó: tipos, bucles, funciones, punteros, memoria, archivos · cada pieza en su lugar
recompensa: xp 20, oro 20
```

#### Escena
En la entrada de las Forjas, la pared de la cuenta de espadazos está llena de palitos. Ferrum le da a Kira la tiza: falta la última línea.

#### Gheco sugiere
Un último programa para la pared: recorré los registros y mostrá cada uno alineado.

#### Desafío
Completá el `printf` para que la pared quede alineada (nombre a la izquierda en 30 lugares, número a la derecha en 3).

#### Código inicial
```c
#include <stdio.h>

typedef struct {
    const char *que;
    int cuantos;
} Registro;

int main(void)
{
    Registro pared[4] = {
        { "Espadazos", 41 },
        { "Problemas resueltos a espadazos", 0 },
        { "Herraduras banana", 40 },
        { "Problemas resueltos midiendo", 99 },
    };
    for (int i = 0; i < 4; i++) {
        printf("___\n", pared[i].que, pared[i].cuantos);
    }
    return 0;
}
```

#### Salida esperada
```
Espadazos                        41
Problemas resueltos a espadazos   0
Herraduras banana                40
Problemas resueltos midiendo     99
```

#### Solución
```c
#include <stdio.h>

typedef struct {
    const char *que;
    int cuantos;
} Registro;

int main(void)
{
    Registro pared[4] = {
        { "Espadazos", 41 },
        { "Problemas resueltos a espadazos", 0 },
        { "Herraduras banana", 40 },
        { "Problemas resueltos midiendo", 99 },
    };
    for (int i = 0; i < 4; i++) {
        printf("%-31s %3d\n", pared[i].que, pared[i].cuantos);
    }
    return 0;
}
```

#### Al superarla
Ferrum mira la pared, golpea el yunque **tres veces** y le saca la tiza de la mano a Kira. Tacha el 99 y escribe: «todos». Kira no sabe qué hacer con las manos. Tizón llora sin disimular.

#### Imagen
- Una pared de piedra llena de palitos de tiza bajo títulos como Espadazos y Herraduras banana.
- Maese Ferrum (herrero humano enorme, NO es enano: mide unos dos metros, de piernas largas, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) escribe «todos» con tiza.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) con la Hoja Templada a la espalda.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) llorando.

### Micro-misión R05-N05-P2 · Dos caminos

```meta
lugar: La Encrucijada del Yunque
personajes: Kira, Gheco, Maese Ferrum
carta: Elegir camino | la Forja Viva: juegos con SDL3 · el Taller de los Autómatas: Arduino · lo que sigue es tuyo
recompensa: xp 20, oro 20
```

#### Escena
Del yunque viejo salen dos caminos. Uno lleva a una puerta de vidrio negro donde el metal se mueve solo, sesenta veces por segundo. El otro, a un taller lleno de figuras de latón con ojos que se prenden y se apagan.

#### Gheco sugiere
Un último `switch`: según el camino elegido, se muestra adónde lleva.

#### Desafío
Completá los dos `case` con los caminos.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int camino;
    scanf("%d", &camino);
    switch (camino) {
    ___
        printf("La Forja Viva: el metal se mueve en una pantalla (SDL3)\n");
        break;
    ___
        printf("El Taller de los Automatas: el codigo mueve cosas de verdad (Arduino)\n");
        break;
    default:
        printf("Ese camino no existe (todavia)\n");
    }
    return 0;
}
```

#### Entrada
```
1
```

#### Salida esperada
```
La Forja Viva: el metal se mueve en una pantalla (SDL3)
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int camino;
    scanf("%d", &camino);
    switch (camino) {
    case 1:
        printf("La Forja Viva: el metal se mueve en una pantalla (SDL3)\n");
        break;
    case 2:
        printf("El Taller de los Automatas: el codigo mueve cosas de verdad (Arduino)\n");
        break;
    default:
        printf("Ese camino no existe (todavia)\n");
    }
    return 0;
}
```

#### Al superarla
Ferrum se apoya en el martillo. —Lo que sigue no es obligatorio. Es **tuyo**. —Kira mira los dos caminos. Por primera vez desde que llegó, no tiene apuro.

#### Imagen
- Un yunque viejo en una encrucijada, con dos caminos: uno hacia una puerta de vidrio negro y otro hacia un taller con autómatas de latón.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) de espaldas, mirando los dos caminos.
- Maese Ferrum (herrero humano enorme, NO es enano: mide unos dos metros, de piernas largas, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) apoyado en su martillo enorme.

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
