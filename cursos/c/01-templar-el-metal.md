# RAMA R01 · Templar el metal: los fundamentos

```meta
tipo: tronco
posicion: 1
```

## R01-N01 · Variables y tipos

```meta
tipo: tema
criatura: goblin
padre: R00-N01
precio: 10
temas: prog.variables
```

### Crónica

En el depósito de la Forja, cada material va en su cajón: el carbón en uno, las gemas en otro, los clavos en uno chiquito que dice «255». Ferrum le encarga a Kira guardar los clavos de la mañana.

Kira mete el clavo 254, el 255… y el 256. El cajón hace *clic* y queda **vacío**. Tizón, que los había contado uno por uno, se agarra la cabeza.

—El tamaño del cajón lo elegís vos —le explica {mentor}—, y el metal no perdona: si no entra, no te avisa. Vuelve a cero. —Tizón ya está contando de nuevo, en voz alta, y le dedica a Kira una mirada larguísima.

### Objetivos

Declarar variables del tipo adecuado, saber cuánta memoria ocupa cada una y
hasta dónde llega, mostrarlas con `printf`, declarar constantes y convertir entre
tipos sabiendo qué se puede perder.

### Antes de empezar

- Compilar, ejecutar y `printf` (01).

### Explicación

#### Variables
Una variable es un **cajón con nombre** en la memoria. En C se declara con su
**tipo**, que dice qué se puede guardar y cuántos bytes ocupa:
```c
int nivel = 5;       /* tipo, nombre, valor inicial */
nivel = 6;           /* cambiar el valor */
```
- El tipo **no cambia nunca**.
- Nombres: letras, números y `_`, sin empezar con número. En C se usa
  `minusculas_con_guion`: `vida_maxima`.
- **Inicializá siempre**: una variable local sin valor inicial tiene **basura**
  (lo que había antes en esa memoria), no cero.

#### Los tipos
| Tipo | Guarda | Tamaño típico | `printf` |
|---|---|---|---|
| `char` | un carácter (y también un número chico) | 1 byte | `%c` (o `%d`) |
| `short` | entero chico | 2 bytes | `%d` |
| **`int`** | **entero habitual** | 4 bytes (±2 100 millones) | `%d` |
| `long` | entero grande | 8 bytes en Linux de 64 bits | `%ld` |
| `long long` | entero enorme | 8 bytes | `%lld` |
| `unsigned int` | entero **sin signo** (0 o más) | 4 bytes (0 a 4 294 millones) | `%u` |
| `float` | decimal (unas 7 cifras) | 4 bytes | `%f` |
| **`double`** | **decimal habitual** (unas 15 cifras) | 8 bytes | `%f` |
| `bool` | `true`/`false` (con `#include <stdbool.h>`) | 1 byte | `%d` (muestra 1/0) |

- **Los tamaños dependen de la máquina.** C solo garantiza mínimos. Para
  saberlo: `sizeof(tipo)` da los bytes (se muestra con `%zu`).
- Los límites están en `<limits.h>`: `INT_MAX`, `INT_MIN`, `UINT_MAX`…
- Los literales llevan sufijos: `125000L` (long), `8000000000LL` (long long),
  `350u` (unsigned), `2.5f` (float). Sin sufijo, `5` es `int` y `2.5` es
  `double`.
- `%.2f` muestra 2 decimales.

#### `stdint.h`: enteros de tamaño exacto
Cuando **importa** el tamaño (colores, archivos binarios, hardware), se usan los
tipos de `<stdint.h>`: `int8_t`, `int16_t`, `int32_t`, `int64_t` y sus
versiones sin signo `uint8_t`… `uint64_t`. Un `uint8_t` es **exactamente** 8
bits: de 0 a 255, justo un canal de color. SDL3 (cap. 06) los usa en todos
lados.

#### Constantes
```c
#define VIDA_MAXIMA 100          /* el preprocesador reemplaza el texto antes de compilar */
const int COSTO_POCION = 8;      /* una variable que no se puede cambiar */
```
- **`#define`** no es una variable: antes de compilar, el preprocesador
  reemplaza cada `VIDA_MAXIMA` por `100`. Sin `=` y **sin `;`**.
- **`const`** es una variable de verdad (tiene tipo), pero de solo lectura.
- Las dos se nombran en `MAYUSCULAS`. El preprocesador se ve a fondo en el 23.

#### Conversiones
**Automáticas.** Al asignar un tipo "chico" a uno "grande", C convierte solo:
`double d = 17;` guarda `17.0`.

**Cast (a mano).** Poniendo el tipo entre paréntesis:
```c
int golpe_entero = (int) 17.9;     /* 17: TRUNCA, no redondea */
double r = (double) 7 / 2;         /* 3.5: convierte el 7 ANTES de dividir */
```
Ojo: `7 / 2` entre enteros da `3` (división entera, se ve en el 03).

**Peligro:** C también convierte **solo** de grande a chico (`int x = 3.9;` guarda
3), muchas veces sin avisar. Por eso los casts se escriben explícitos: dejan
claro que la pérdida es intencional.

#### Desbordamiento
- **Sin signo (`unsigned`)**: si se pasa del máximo, **da la vuelta** a 0 (y
  si baja de 0, va al máximo). Está **definido**: siempre pasa lo mismo.
- **Con signo (`int`)**: pasarse de `INT_MAX` es **comportamiento indefinido**
  (*undefined behavior*): el estándar no dice qué pasa, y el compilador puede
  hacer cualquier cosa. Nunca lo hagas; los sanitizadores lo detectan (ver el
  bestiario).

#### `char` es un número
Un `char` guarda el **código** del carácter: `'A'` es 65. Por eso `'A' + 1` es
66, que con `%c` se muestra como `'B'`.

#### Los decimales no son exactos
`0.1 + 0.2` da `0.30000000000000004`: los decimales se guardan en binario y
0.1 no tiene representación exacta (como 1/3 en decimal). Nunca compares
decimales con `==` (03).

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo.
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`

### Código de ejemplo

```c
/*
 * 02 - Variables, tipos, constantes y conversiones.
 *
 *   make run
 */
#include <stdio.h>
#include <stdbool.h>   /* bool, true, false */
#include <limits.h>    /* INT_MAX, INT_MIN, UINT_MAX... */
#include <stdint.h>    /* int32_t, uint8_t...: enteros de tamanio exacto */

#define VIDA_MAXIMA 100          /* constante del preprocesador: se reemplaza el texto */

int main(void)
{
    /* --- Enteros --- */
    int      nivel       = 5;                /* el entero de todos los dias */
    short    flechas     = 120;              /* entero chico */
    long     experiencia = 125000L;          /* entero grande */
    long long habitantes = 8000000000LL;     /* entero enorme */
    unsigned int oro     = 350u;             /* sin signo: solo 0 o positivos */

    printf("nivel=%d flechas=%d experiencia=%ld\n", nivel, flechas, experiencia);
    printf("habitantes=%lld oro=%u\n", habitantes, oro);

    /* --- Decimales --- */
    float  velocidad = 2.5f;                 /* precision simple (unas 7 cifras) */
    double precision = 3.141592653589793;    /* precision doble (unas 15 cifras) */
    printf("velocidad=%.2f precisión=%.10f\n", velocidad, precision);

    /* --- Caracteres y booleanos --- */
    char inicial = 'K';                      /* UN caracter, comillas simples */
    bool viva    = true;
    printf("inicial=%c (código %d) viva=%d\n", inicial, inicial, viva);

    /* --- Tamanio en bytes (depende de la maquina; aca, Linux de 64 bits) --- */
    printf("\nTamaños en bytes:\n");
    printf("  char=%zu short=%zu int=%zu long=%zu long long=%zu\n",
           sizeof(char), sizeof(short), sizeof(int), sizeof(long), sizeof(long long));
    printf("  float=%zu double=%zu bool=%zu\n", sizeof(float), sizeof(double), sizeof(bool));

    /* --- Limites --- */
    printf("\nint va de %d a %d\n", INT_MIN, INT_MAX);
    printf("unsigned int va de 0 a %u\n", UINT_MAX);

    /* --- Enteros de tamanio exacto (stdint.h): los usa SDL para colores y pixeles --- */
    uint8_t rojo = 255;                      /* exactamente 8 bits sin signo: 0 a 255 */
    int32_t puntaje = -1500;                 /* exactamente 32 bits con signo */
    printf("\nrojo=%u (%zu byte) puntaje=%d (%zu bytes)\n",
           rojo, sizeof(rojo), puntaje, sizeof(puntaje));

    /* --- Constantes --- */
    const int COSTO_POCION = 8;              /* variable que no se puede cambiar */
    printf("\nvida máxima=%d poción=%d\n", VIDA_MAXIMA, COSTO_POCION);

    /* --- Conversiones --- */
    int danio_base = 17;
    double danio_exacto = danio_base;        /* int -> double: automatico, sin perdida */
    double golpe = 17.9;
    int golpe_entero = (int) golpe;          /* cast: TRUNCA (corta los decimales) */
    printf("\ndaño exacto=%.1f  (int) 17.9=%d\n", danio_exacto, golpe_entero);
    printf("7 / 2 = %d   (double) 7 / 2 = %.1f\n", 7 / 2, (double) 7 / 2);

    /* --- unsigned "da la vuelta": el resultado esta DEFINIDO --- */
    unsigned int cero = 0;
    unsigned int menos_uno = cero - 1;       /* no hay negativos: vuelve al maximo */
    uint8_t byte = 255;
    byte = byte + 1;                         /* 256 no entra en 8 bits: vuelve a 0 */
    printf("\n0u - 1 = %u   uint8_t 255 + 1 = %u\n", menos_uno, byte);

    /* --- char es un numero --- */
    char letra = 'A';
    printf("'A' + 1 = %d = '%c'\n", letra + 1, letra + 1);

    /* --- Los decimales no son exactos --- */
    printf("0.1 + 0.2 = %.17f\n", 0.1 + 0.2);

    return 0;
}
```

### Salida esperada

```
nivel=5 flechas=120 experiencia=125000
habitantes=8000000000 oro=350
velocidad=2.50 precisión=3.1415926536
inicial=K (código 75) viva=1

Tamaños en bytes:
  char=1 short=2 int=4 long=8 long long=8
  float=4 double=8 bool=1

int va de -2147483648 a 2147483647
unsigned int va de 0 a 4294967295

rojo=255 (1 byte) puntaje=-1500 (4 bytes)

vida máxima=100 poción=8

daño exacto=17.0  (int) 17.9=17
7 / 2 = 3   (double) 7 / 2 = 3.5

0u - 1 = 4294967295   uint8_t 255 + 1 = 0
'A' + 1 = 66 = 'B'
0.1 + 0.2 = 0.30000000000000004
```

### ¿Para qué sirve?

Elegir el tipo correcto es una decisión real de ingeniería: un sensor de temperatura manda valores en 12 bits, un color de pantalla ocupa 4 bytes (rojo, verde, azul y transparencia) y un contador de visitas de una página puede pasar los 2 000 millones que entran en un `int`. En 1996, el cohete Ariane 5 explotó a los 37 segundos de despegar por guardar un número de 64 bits en uno de 16: desbordamiento, el mismo goblin de esta unidad.

### Errores habituales

Mensajes reales de `gcc` 13 con `-Wall -Wextra`.

**Goblin: el formato de `printf` no coincide con el tipo.** Compila, pero
muestra basura. `gcc` avisa y sugiere el correcto:
```
e4.c:7:14: warning: format ‘%d’ expects argument of type ‘int’, but argument 2 has type ‘double’ [-Wformat=]
    7 |     printf("%d %f\n", oro, nivel);
      |             ~^        ~~~
      |              |        |
      |              int      double
      |             %f
```

**Goblin: un valor que no entra en el tipo.**
```
e5.c:8:14: warning: overflow in conversion from ‘int’ to ‘char’ changes value from ‘300’ to ‘44’ [-Woverflow]
    8 |     char c = 300;
      |              ^~~
```

**Slime: cambiar una constante.**
```
e6.c:7:9: error: assignment of read-only variable ‘MAX’
    7 |     MAX = 4;
      |         ^
```

**Goblin: mezclar con y sin signo.** `-1 < 5u` es **falso**: el `-1` se
convierte a `unsigned` (4 294 967 295). `gcc` avisa:
```
e5.c:7:14: warning: comparison of integer expressions of different signedness: ‘int’ and ‘unsigned int’ [-Wsign-compare]
```

**Autómata Desbordado: pasarse de `INT_MAX`.** Sin avisar, el resultado puede
ser cualquier cosa. Compilando con `-fsanitize=undefined` (o `make asan`) se ve:
```
o.c:6:9: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
```

**Ogros:**
- Usar una variable sin inicializar (tiene basura).
- `#define VIDA 100;` con punto y coma: el `;` también se pega donde se usa
  `VIDA`.
- Creer que `(int) 17.9` redondea.

### Micro-misión R01-N01-P1 · Cada cosa en su cajón

```meta
lugar: El depósito de la Forja
personajes: Kira, Gheco, Tizón
criatura: goblin
carta: Variables | tipo nombre = valor; · int para enteros · double para decimales · char para un carácter
recompensa: xp 10, oro 10
```

#### Escena
En el depósito cada material va en un cajón con etiqueta. Tizón le da a Kira tres cajones vacíos: uno para la cantidad de clavos, uno para el peso del lingote y uno para la letra del sello.

#### Gheco sugiere
Una variable se declara con su **tipo**: `int` (enteros), `double` (decimales) o `char` (un carácter, entre comillas simples: `'K'`). Se muestran con `%d`, `%.1f` y `%c`.

#### Desafío
Declará las tres variables con el tipo correcto.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    ___ clavos = 120;
    ___ peso = 2.5;
    ___ sello = 'K';
    printf("clavos: %d\n", clavos);
    printf("peso: %.1f kg\n", peso);
    printf("sello: %c\n", sello);
    return 0;
}
```

#### Salida esperada
```
clavos: 120
peso: 2.5 kg
sello: K
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int clavos = 120;
    double peso = 2.5;
    char sello = 'K';
    printf("clavos: %d\n", clavos);
    printf("peso: %.1f kg\n", peso);
    printf("sello: %c\n", sello);
    return 0;
}
```

#### Al superarla
Tres cajones, tres etiquetas. Tizón los mide uno por uno y los aprueba con un gruñido muy parecido al de Ferrum.

#### Imagen
- Un depósito de piedra con cajones de hierro etiquetados: clavos, peso, sello.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) guarda una letra K de bronce en un cajón chiquito.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) anota en su libreta.

### Micro-misión R01-N01-P2 · El clavo 256

```meta
lugar: El depósito de la Forja
personajes: Kira, Gheco, Tizón
criatura: ogro
carta: Desborde | unsigned char va de 0 a 255 · si se pasa, vuelve a 0 sin avisar · elegí un tipo con lugar de sobra
recompensa: xp 10, oro 10
```

#### Escena
Kira guarda clavos en el cajón chiquito: 254, 255… y el 256. El cajón hace *clic* y queda **vacío**.
—¡Los había contado uno por uno! —se agarra la cabeza Tizón.

#### Gheco sugiere
Un `unsigned char` guarda de 0 a 255: si se pasa, **vuelve a 0** sin avisar. Un `int` tiene lugar de sobra (más de dos mil millones).

#### Desafío
Cambiá el tipo del cajón para que entren 256 clavos.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    unsigned char cajon = 255;
    cajon = cajon + 1;
    printf("clavos en el cajon: %d\n", cajon);
    return 0;
}
```

#### Salida esperada
```
clavos en el cajon: 256
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int cajon = 255;
    cajon = cajon + 1;
    printf("clavos en el cajon: %d\n", cajon);
    return 0;
}
```

#### Al superarla
256 clavos, ni uno menos. Tizón le perdona a Kira el susto, pero le dedica una mirada larguísima.

#### Imagen
- Un cajón chiquito de hierro con un 255 grabado, que se vacía con un destello.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) se agarra la cabeza; Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) sostiene el clavo 256 con cara de culpa.

### Micro-misión R01-N01-P3 · Cuánto ocupa cada cajón

```meta
lugar: El depósito de la Forja
personajes: Kira, Gheco, Tizón
carta: sizeof | sizeof(tipo) dice cuántos bytes ocupa · se muestra con %zu · char 1, int 4, double 8
recompensa: xp 10, oro 10
```

#### Escena
Tizón quiere medir los cajones por dentro, pero el calibre no entra. Gheco le muestra una herramienta mejor.

#### Gheco sugiere
`sizeof(tipo)` devuelve cuántos **bytes** ocupa ese tipo. Su valor se muestra con `%zu`.

#### Desafío
Completá con `sizeof` para mostrar cuánto ocupa cada tipo.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    printf("char:   %zu byte\n", ___(char));
    printf("int:    %zu bytes\n", ___(int));
    printf("double: %zu bytes\n", ___(double));
    return 0;
}
```

#### Salida esperada
```
char:   1 byte
int:    4 bytes
double: 8 bytes
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    printf("char:   %zu byte\n", sizeof(char));
    printf("int:    %zu bytes\n", sizeof(int));
    printf("double: %zu bytes\n", sizeof(double));
    return 0;
}
```

#### Al superarla
Tizón copia los tres números en la tapa de la libreta, con letra grande. Es la primera vez que algo lo mide a él primero.

#### Imagen
- Tres cajones de distinto tamaño, con números luminosos 1, 4 y 8 encima.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) guarda el calibre, sorprendido.

### Micro-misión R01-N01-P4 · El precio con decimales

```meta
lugar: El depósito de la Forja
personajes: Kira, Gheco, Chispa
criatura: goblin
carta: Conversión | int / int da un entero · (double) convierte antes de dividir · el cast va delante del valor
recompensa: xp 15, oro 15
```

#### Escena
Chispa reparte el precio de 7 lingotes entre 2 compradores y le da **3** a cada uno. —Sobra uno, que me lo quedo yo —sonríe con el diente de oro.

#### Gheco sugiere
Si los dos números son `int`, la división **descarta** los decimales. Con `(double)` delante de uno, la cuenta se hace con decimales.

#### Desafío
Convertí la cuenta para que el reparto sea justo.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int lingotes = 7;
    int compradores = 2;
    double cada_uno = lingotes / compradores;
    printf("cada uno paga %.1f lingotes\n", cada_uno);
    return 0;
}
```

#### Salida esperada
```
cada uno paga 3.5 lingotes
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int lingotes = 7;
    int compradores = 2;
    double cada_uno = (double) lingotes / compradores;
    printf("cada uno paga %.1f lingotes\n", cada_uno);
    return 0;
}
```

#### Al superarla
3,5 cada uno. Chispa devuelve el lingote que «sobraba» con una sonrisa que no engaña a nadie.

#### Imagen
- Chispa (mercader alto y flaco, sombrero de ala corta, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro) reparte siete lingotes en dos pilas desparejas.
- Un goblin se escapa con medio lingote bajo el brazo.

### Misión R01-N01-M1 · Cada dato en su cajón

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Tizón tiene nivel 12, 3 500 millones de
experiencia, 15 % de probabilidad de crítico, rango `S`, escudo (sí) y 40
flechas. Elegí el tipo de cada variable y mostralas con el formato correcto.
¿Por qué la experiencia no entra en un `int`?

#### Criterio de aprobación

- Usa un tipo adecuado para cada dato (por ejemplo `long long` o `uint32_t` para la experiencia, `char` para el rango, `bool` para el escudo).
- Muestra cada valor con el formato correcto de `printf`.
- Explica en un comentario por qué 3 500 millones no entra en un `int`.

#### Salida esperada

```
Tizon | nivel 12 | exp 3500000000
crítico 0.15 | rango S | escudo 1 | flechas 40
```

#### Solución de referencia

```c
/*
 * Mision 1 - Cada dato en su caja: elegir el tipo de cada atributo de Tizon.
 */
#include <stdio.h>
#include <stdbool.h>

int main(void)
{
    int       nivel        = 12;            /* entero mediano */
    long long experiencia  = 3500000000LL;  /* mas de 2100 millones: no entra en int */
    double    prob_critico = 0.15;          /* decimal */
    char      rango        = 'S';           /* una letra */
    bool      tiene_escudo = true;          /* si / no */
    unsigned int flechas   = 40u;           /* nunca es negativo */

    printf("Tizon | nivel %d | exp %lld\n", nivel, experiencia);
    printf("crítico %.2f | rango %c | escudo %d | flechas %u\n",
           prob_critico, rango, tiene_escudo, flechas);
    return 0;
}
```

### Misión R01-N01-M2 · El cofre de 8 bits

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Guardá 255 monedas en un `uint8_t` y sumale una. ¿Qué
pasa? Arreglalo con un tipo más grande.

#### Criterio de aprobación

- Muestra que 255 + 1 en un `uint8_t` da 0.
- Lo arregla con un tipo más grande y muestra 256.

#### Salida esperada

```
Cofre lleno: 255
Entra una moneda más: 0
Con uint16_t: 256
```

#### Solución de referencia

```c
/*
 * Mision 2 - El cofre de 8 bits.
 * Un uint8_t guarda de 0 a 255. Si el cofre esta lleno y entra una moneda mas,
 * no hay error: vuelve a 0. Con unsigned ese comportamiento esta DEFINIDO.
 */
#include <stdio.h>
#include <stdint.h>

int main(void)
{
    uint8_t cofre = 255;
    printf("Cofre lleno: %u\n", cofre);
    cofre = cofre + 1;
    printf("Entra una moneda más: %u\n", cofre);

    uint16_t cofre_grande = 255;             /* 16 bits: hasta 65535 */
    cofre_grande = cofre_grande + 1;
    printf("Con uint16_t: %u\n", cofre_grande);
    return 0;
}
```

### Misión R01-N01-M3 · El inventario de la Forja

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Mostrá una tabla con el tamaño, el mínimo y el
máximo de `char`, `short`, `int`, `long` y `unsigned int`, usando
`sizeof` y `<limits.h>`.

#### Criterio de aprobación

- Muestra tamaño, mínimo y máximo de los cinco tipos.
- Usa `sizeof` y las constantes de `<limits.h>` (no números escritos a mano).
- Usa `%zu` para `sizeof`.

#### Salida esperada

```
tipo        bytes                 mínimo                 máximo
char            1                   -128                    127
short           2                 -32768                  32767
int             4            -2147483648             2147483647
long            8   -9223372036854775808    9223372036854775807
unsigned        4                      0             4294967295
```

#### Solución de referencia

```c
/*
 * Mision 3 - El inventario de la forja: cuanto ocupa cada tipo y hasta donde llega.
 */
#include <stdio.h>
#include <limits.h>

int main(void)
{
    /* "mínimo" y "máximo" tienen una letra con tilde, que en UTF-8 ocupa 2 bytes;
       printf cuenta BYTES, no letras, asi que se les da un lugar mas (23). */
    printf("%-10s %6s %23s %23s\n", "tipo", "bytes", "mínimo", "máximo");
    printf("%-10s %6zu %22d %22d\n", "char", sizeof(char), CHAR_MIN, CHAR_MAX);
    printf("%-10s %6zu %22d %22d\n", "short", sizeof(short), SHRT_MIN, SHRT_MAX);
    printf("%-10s %6zu %22d %22d\n", "int", sizeof(int), INT_MIN, INT_MAX);
    printf("%-10s %6zu %22ld %22ld\n", "long", sizeof(long), LONG_MIN, LONG_MAX);
    printf("%-10s %6zu %22d %22u\n", "unsigned", sizeof(unsigned int), 0, UINT_MAX);
    return 0;
}
```

### Encargo R01-N01-E1 · El termómetro del herrero

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El herrero anota la temperatura en Celsius y el cartel la muestra en Fahrenheit
(`F = C × 9 / 5 + 32`). Convertí 36,6 °C con `double` y mostralo con 2
decimales. Después hacé la cuenta con enteros, escribiendo `c * (9 / 5) + 32`: ¿por
qué da mal? Por último, mostrá la versión del cartel, sin decimales.

#### Criterio de aprobación

- Convierte 36,6 °C con `double` y muestra 97.88 °F.
- Muestra la cuenta con enteros y explica que `9 / 5` da 1.
- Muestra la versión del cartel sin decimales.

#### Salida esperada

```
36.6 °C = 97.88 °F
Con enteros y 9 / 5 primero: 68 °F (mal)
Con enteros bien ordenado:   96 °F
Cartel: 97 °F
```

#### Solución de referencia

```c
/*
 * Encargo del Gremio - El termometro de la herreria.
 * F = C * 9 / 5 + 32, con double para no perder decimales.
 */
#include <stdio.h>

int main(void)
{
    double celsius = 36.6;
    double fahrenheit = celsius * 9 / 5 + 32;
    printf("%.1f °C = %.2f °F\n", celsius, fahrenheit);

    /* Con enteros, 9 / 5 da 1 (division entera) y el resultado sale mal: */
    int c = 36;
    printf("Con enteros y 9 / 5 primero: %d °F (mal)\n", c * (9 / 5) + 32);
    printf("Con enteros bien ordenado:   %d °F\n", c * 9 / 5 + 32);

    int cartel = (int) fahrenheit;           /* el cartel no muestra decimales */
    printf("Cartel: %d °F\n", cartel);
    return 0;
}
```

### Prueba del sello

#### ¿Qué tipo usarías para: la vida de un personaje, el precio con centavos, la inicial de un nombre, "¿está vivo?", un canal de color de 0 a 255?

Vida: `int`; precio con centavos: `double` (o centavos en un entero); inicial: `char`; ¿está vivo?: `bool`; canal de color: `uint8_t` (o `unsigned char`).

#### ¿Qué muestra `printf("%zu", sizeof(int));` en tu máquina? ¿Es igual en todas?

Normalmente `4`. No: el estándar solo garantiza mínimos, depende de la máquina y del compilador.

#### ¿Qué diferencia hay entre `#define MAX 10` y `const int MAX = 10;`?

`#define` reemplaza el texto antes de compilar (no tiene tipo); `const int` es una variable de verdad, con tipo, que no se puede modificar.

#### ¿Cuánto da `(int) 9.99`? ¿Y `(double) 7 / 2`? ¿Y `(double) (7 / 2)`?

`9` (corta los decimales); `3.5` (convierte el 7 antes de dividir); `3.0` (divide enteros primero y da 3).

#### ¿Qué pasa si un `uint8_t` que vale 255 suma 1? ¿Y un `int` que vale `INT_MAX`?

El `uint8_t` da la vuelta y queda en 0. El `int` que pasa `INT_MAX` es **comportamiento indefinido**: puede pasar cualquier cosa.

#### ¿Qué tiene una variable local que no inicializaste?

Basura: lo que había en esa memoria. Hay que inicializarla siempre.

### Soluciones (docente)

Material original: `01-C/02-Variables` (soluciones completas en `soluciones/`, con sus archivos de entrada y salida).

## R01-N02 · Operadores

```meta
tipo: tema
criatura: ogro
padre: R01-N01
precio: 10
temas: prog.operadores
```

### Crónica

Chispa, el mercader de lingotes, llega a la Forja con su carretilla que se desarma sola y su sonrisa de diente de oro. Vende herraduras: por la mañana cobra **7 lingotes** por tres herraduras; a la tarde, por el mismo pedido, **3**.

Tizón le desarma la cuenta en el mostrador: Chispa había dividido antes de multiplicar, y en las Forjas `17 / 5` da **3**. Esta vez el estafado fue él mismo.

—Los enteros no se parten —dice {mentor}, sin levantar la vista del yunque—. Si querés los pedazos, pedí decimales. Y el orden de las cuentas decide quién paga de más. —Chispa anota todo en un papelito. Kira sospecha que no para mejorar.

### Objetivos

Usar los operadores de C (aritméticos, de asignación, de incremento, de
comparación, lógicos y el ternario) y saber en qué orden se evalúan.

### Antes de empezar

- Variables, tipos y casting (02).

### Explicación

#### Aritméticos
| Operador | Qué hace | `17 ? 5` |
|---|---|---|
| `+` `-` `*` | suma, resta, producto | `22`, `12`, `85` |
| `/` | división | `3` si **los dos** son enteros; `3.4` si alguno es decimal |
| `%` | resto (solo con enteros) | `2` |

**División entera:** `17 / 5` da `3`. Para tener decimales, al menos uno tiene
que ser decimal: `17.0 / 5` o `(double) a / b`. En cambio, `(double) (a / b)`
**no** sirve: primero divide entero (3) y después convierte (3.0).

La división entera **trunca hacia cero** (`-7 / 2` es `-3`) y el resto lleva
el signo del primero (`-7 % 2` es `-1`).

Usos típicos: `seg / 60` y `seg % 60` (minutos y segundos), `n % 2 == 0` (¿es
par?), `turno % 3 == 0` (cada 3 turnos).

#### Asignación compuesta e incremento
- `oro += 25` equivale a `oro = oro + 25`. Existen `+=`, `-=`, `*=`, `/=` y `%=`.
- `x++` suma 1 y `x--` resta 1. Solos en una línea, `x++` y `++x` hacen lo
  mismo. **Dentro** de otra expresión, `x++` usa el valor viejo y `++x` el
  nuevo. Consejo: usalos solos en su línea.

#### Comparación: dan 1 o 0
`==`, `!=`, `<`, `<=`, `>`, `>=`. En C **no hay un resultado "verdadero"
especial**: una comparación da el entero `1` si es verdadera y `0` si es falsa.
- **`=` asigna, `==` compara.** `if (vida = 0)` **compila** (asigna 0 y la
  condición es falsa). `gcc` avisa con `-Wall` (ver el bestiario).
- No se pueden encadenar: `30 <= vida <= 70` compila pero **no** significa lo
  que parece. Se escribe `vida >= 30 && vida <= 70`.
- No compares decimales con `==` (02).

#### Lógicos: `&&`, `||`, `!`
| Expresión | Da 1 cuando… |
|---|---|
| `a && b` | los dos son verdaderos ("y") |
| `a \|\| b` | al menos uno es verdadero ("o") |
| `!a` | `a` es falso ("no") |

En C, **cualquier número distinto de 0 es verdadero** y el 0 es falso. Por eso
`!5` da 0 y `5 && 3` da 1.

**Cortocircuito:** en `a && b`, si `a` es falso, `b` **no se evalúa**. En
`a || b`, si `a` es verdadero, tampoco. Sirve para proteger operaciones
peligrosas:
```c
int alcanza = companeros > 0 && 90 / companeros > 10;   /* nunca divide por 0 */
```

#### Ternario
```c
int danio = vida > 50 ? 10 : 20;
```
"¿`vida > 50`? Si sí, 10; si no, 20". Sirve para elegir entre dos valores.

#### Precedencia (de mayor a menor)
| Prioridad | Operadores |
|---|---|
| 1 | `( )` `x++` `x--` |
| 2 | `++x` `--x` `-x` `!` `(tipo)` `sizeof` |
| 3 | `*` `/` `%` |
| 4 | `+` `-` |
| 5 | `<` `<=` `>` `>=` |
| 6 | `==` `!=` |
| 7 | `&&` |
| 8 | `\|\|` |
| 9 | `? :` |
| 10 | `=` `+=` `-=` … |

(Los operadores de bits, que van entre medio, se ven en el 04.)

En el mismo nivel se evalúa **de izquierda a derecha**: `10 - 4 - 3` es `3`.
**Ante la duda, usá paréntesis.**

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo.
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`

### Código de ejemplo

```c
/*
 * 03 - Operadores: aritmeticos, asignacion, incremento, comparacion,
 * logicos, ternario y precedencia.
 *
 *   make run
 */
#include <stdio.h>

int main(void)
{
    /* --- Aritmeticos --- */
    int a = 17;
    int b = 5;
    printf("suma        %d\n", a + b);
    printf("resta       %d\n", a - b);
    printf("producto    %d\n", a * b);
    printf("división    %d   <- entre enteros: división ENTERA\n", a / b);
    printf("resto       %d\n", a % b);
    printf("17.0 / 5    %.1f\n", 17.0 / 5);
    printf("-7 / 2 = %d   -7 %% 2 = %d\n", -7 / 2, -7 % 2);

    int segundos = 135;
    printf("%d s = %d min %d s\n", segundos, segundos / 60, segundos % 60);

    /* --- Asignacion compuesta --- */
    int oro = 50;
    oro += 25;      /* oro = oro + 25 */
    oro -= 10;
    oro *= 2;
    oro /= 3;       /* entera */
    oro %= 40;
    printf("oro final: %d\n", oro);

    /* --- Incremento --- */
    int flechas = 5;
    int antes = flechas++;      /* POST: usa el valor viejo (5), despues suma */
    int despues = ++flechas;    /* PRE: suma primero (7), despues usa */
    printf("antes=%d despues=%d flechas=%d\n", antes, despues, flechas);

    /* --- Comparacion: en C dan 1 (verdadero) o 0 (falso), de tipo int --- */
    int vida = 35;
    printf("vida == 35 -> %d\n", vida == 35);
    printf("vida != 0  -> %d\n", vida != 0);
    printf("vida < 30  -> %d\n", vida < 30);
    printf("¿vida entre 30 y 70? %d\n", vida >= 30 && vida <= 70);

    /* --- Logicos: && (y), || (o), ! (no) --- */
    int tiene_llave = 1;
    int es_maga = 0;
    int maldita = 0;
    printf("abre la puerta: %d\n", (tiene_llave || es_maga) && !maldita);

    /* En C, CUALQUIER numero distinto de 0 cuenta como verdadero */
    printf("!5 = %d   !0 = %d   5 && 3 = %d\n", !5, !0, 5 && 3);

    /* Cortocircuito: si la izquierda ya decide, la derecha NI SE EVALUA */
    int companeros = 0;
    int alcanza = companeros > 0 && 90 / companeros > 10;   /* nunca divide por 0 */
    printf("¿alcanza para repartir? %d\n", alcanza);

    /* --- Ternario: condicion ? valor_si_verdadero : valor_si_falso --- */
    int danio = vida > 50 ? 10 : 20;
    printf("daño según la vida: %d\n", danio);

    /* --- Precedencia --- */
    printf("2 + 3 * 4   = %d\n", 2 + 3 * 4);
    printf("(2 + 3) * 4 = %d\n", (2 + 3) * 4);
    printf("10 - 4 - 3  = %d\n", 10 - 4 - 3);    /* de izquierda a derecha */

    /* Promedio: la division entera se "come" los decimales */
    int suma = 7;
    int cantidad = 2;
    printf("promedio mal:  %d\n", suma / cantidad);
    printf("promedio bien: %.1f\n", (double) suma / cantidad);

    int ataque = 20;
    int defensa = 6;
    int critico = 2;
    printf("daño: %d\n", (ataque - defensa / 2) * critico);
    return 0;
}
```

### Salida esperada

```
suma        22
resta       12
producto    85
división    3   <- entre enteros: división ENTERA
resto       2
17.0 / 5    3.4
-7 / 2 = -3   -7 % 2 = -1
135 s = 2 min 15 s
oro final: 3
antes=5 despues=7 flechas=7
vida == 35 -> 1
vida != 0  -> 1
vida < 30  -> 0
¿vida entre 30 y 70? 1
abre la puerta: 1
!5 = 0   !0 = 1   5 && 3 = 1
¿alcanza para repartir? 0
daño según la vida: 20
2 + 3 * 4   = 14
(2 + 3) * 4 = 20
10 - 4 - 3  = 3
promedio mal:  3
promedio bien: 3.5
daño: 34
```

### ¿Para qué sirve?

Los operadores son las reglas del negocio: "envío gratis si la compra supera $30 000 **o** es cliente premium", "descuento si es jubilado **y** paga en efectivo". Con `/` y `%` se pasan segundos a horas y minutos, se reparten turnos o se sabe si un número es par; y el cortocircuito de `&&` evita divisiones por cero en cualquier programa que haga cuentas con datos del usuario.

### Errores habituales

Mensajes reales de `gcc` 13 con `-Wall -Wextra`.

**Ogro: `=` en lugar de `==`.** Compila y hace otra cosa. Por suerte, `gcc` avisa:
```
e5.c:5:9: warning: suggest parentheses around assignment used as truth value [-Wparentheses]
    5 |     if (vida = 0) printf("muerto\n");
      |         ^~~~
```

**Ogro: comparaciones encadenadas.** `1 < v < 3` es `(1 < v) < 3`, que siempre
es verdadero (0 o 1 siempre es menor que 3):
```
p.c:7:11: warning: comparisons like ‘X<=Y<=Z’ do not have their mathematical meaning [-Wparentheses]
    7 |     if (1 < v < 3) printf("a\n");
      |         ~~^~~
```

**Ogro: mezclar `&&` y `||` sin paréntesis.** `&&` va antes que `||`, y `gcc`
sugiere dejarlo explícito:
```
p.c:5:27: warning: suggest parentheses around ‘&&’ within ‘||’ [-Wparentheses]
    5 |     printf("%d\n", n >= 5 && l || m && !x);
      |                    ~~~~~~~^~~~
```

**Troll: dividir un entero por cero.** El programa muere:
```
Excepción de coma flotante   (`core' generado) ./programa
```
(en inglés: `Floating point exception (core dumped)`). Con constantes, `gcc` ya
avisa al compilar: `warning: division by zero [-Wdiv-by-zero]`.

**Ogro: promedio entero.** `suma / cantidad` con dos `int` pierde los
decimales: `(double) suma / cantidad`.

### Micro-misión R01-N02-P1 · Cajas completas y sobrantes

```meta
lugar: El mostrador de la Forja
personajes: Kira, Gheco, Chispa
carta: División entera y resto | 17 / 5 da 3 · 17 % 5 da 2 (lo que sobra) · solo con enteros
recompensa: xp 10, oro 10
```

#### Escena
Chispa trae 17 herraduras y las quiere vender en cajas de 5. —¿Cuántas cajas armo y cuántas me sobran para vender sueltas, que salen más caras?

#### Gheco sugiere
Con enteros, `/` da cuántas veces entra y `%` (el **resto**) da lo que sobra.

#### Desafío
Completá los dos operadores.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int herraduras = 17;
    int por_caja = 5;
    printf("cajas: %d\n", herraduras ___ por_caja);
    printf("sueltas: %d\n", herraduras ___ por_caja);
    return 0;
}
```

#### Salida esperada
```
cajas: 3
sueltas: 2
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int herraduras = 17;
    int por_caja = 5;
    printf("cajas: %d\n", herraduras / por_caja);
    printf("sueltas: %d\n", herraduras % por_caja);
    return 0;
}
```

#### Al superarla
Tres cajas y dos sueltas. Chispa le pone a las sueltas el doble de precio. Tizón lo anota, por las dudas.

#### Imagen
- Tres cajas con cinco herraduras cada una y dos herraduras sueltas sobre un mostrador.
- Chispa (mercader alto y flaco, sombrero de ala corta, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro) les pega una etiqueta de precio enorme a las sueltas.

### Micro-misión R01-N02-P2 · El orden de las cuentas

```meta
lugar: El mostrador de la Forja
personajes: Kira, Gheco, Chispa, Tizón
criatura: ogro
carta: Precedencia | * / % antes que + - · los paréntesis mandan · ante la duda, paréntesis
recompensa: xp 10, oro 10
```

#### Escena
Chispa cobra tres herraduras de 2 lingotes más 1 de envío. Le da **7**. Tizón hace la cuenta en la libreta: le da **9**.
—El envío es **por herradura** —dice Tizón—. Y la cuenta de Chispa lo cobra una sola vez.

#### Gheco sugiere
C hace `*` antes que `+`: `3 * 2 + 1` es 7. Para que la suma vaya primero, se encierra entre **paréntesis**.

#### Desafío
Agregá los paréntesis para que el envío se cobre por cada herradura.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int herraduras = 3;
    int precio = 2;
    int envio = 1;
    int total = herraduras * precio + envio;
    printf("total: %d lingotes\n", total);
    return 0;
}
```

#### Salida esperada
```
total: 9 lingotes
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int herraduras = 3;
    int precio = 2;
    int envio = 1;
    int total = herraduras * (precio + envio);
    printf("total: %d lingotes\n", total);
    return 0;
}
```

#### Al superarla
Nueve lingotes. Chispa, que esta vez se había cobrado de menos, mira a Tizón con respeto nuevo.

#### Imagen
- Una pizarra con dos cuentas: 3 * 2 + 1 tachada y 3 * (2 + 1) encerrada en un círculo.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) señala la pizarra; Chispa (mercader alto y flaco, sombrero de ala corta, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro) se rasca la cabeza.

### Micro-misión R01-N02-P3 · Un golpe más, un golpe menos

```meta
lugar: El yunque de la Forja
personajes: Kira, Gheco, Maese Ferrum
carta: Incremento y asignación compuesta | x++ suma 1 · x-- resta 1 · x += 5 es x = x + 5 · también -=, *=, /=
recompensa: xp 10, oro 10
```

#### Escena
Ferrum cuenta los martillazos de Kira en voz alta, de muy mal humor: uno, otro más, cinco de golpe en un ataque de impaciencia, y después se le cae el martillo y pierde la cuenta de dos.

#### Gheco sugiere
`golpes++` suma 1. `golpes += 5` suma 5. `golpes -= 2` resta 2. Son formas cortas de `golpes = golpes + …`.

#### Desafío
Completá con los operadores cortos para que la cuenta termine en 5.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int golpes = 0;
    golpes___;          /* uno */
    golpes___;          /* otro mas */
    golpes ___ 5;       /* cinco de golpe */
    golpes ___ 2;       /* se perdieron dos */
    printf("golpes contados: %d\n", golpes);
    return 0;
}
```

#### Salida esperada
```
golpes contados: 5
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int golpes = 0;
    golpes++;           /* uno */
    golpes++;           /* otro mas */
    golpes += 5;        /* cinco de golpe */
    golpes -= 2;        /* se perdieron dos */
    printf("golpes contados: %d\n", golpes);
    return 0;
}
```

#### Al superarla
Cinco golpes. Ferrum los anota en la pared, al lado de la cuenta de espadazos. Kira prefiere no mirar.

#### Imagen
- Maese Ferrum (herrero enorme, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) cuenta con los dedos al lado de un yunque.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) sostiene un martillo demasiado grande.

### Micro-misión R01-N02-P4 · ¿Alcanza el carbón?

```meta
lugar: El horno de la Forja
personajes: Kira, Gheco, Tizón
carta: Comparaciones | == != < > <= >= dan 1 (verdadero) o 0 (falso) · = guarda, == compara
recompensa: xp 15, oro 15
```

#### Escena
Para templar una espada hacen falta 12 bolsas de carbón. Hay 9 en el depósito. Tizón quiere la respuesta en números, como todo.

#### Gheco sugiere
Una comparación da **1** si es verdadera y **0** si es falsa. Ojo: `=` guarda un valor; `==` pregunta si son iguales.

#### Desafío
Completá las comparaciones.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int hay = 9;
    int hacen_falta = 12;
    printf("alcanza: %d\n", hay ___ hacen_falta);
    printf("faltan exactamente 3: %d\n", hacen_falta - hay ___ 3);
    return 0;
}
```

#### Salida esperada
```
alcanza: 0
faltan exactamente 3: 1
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int hay = 9;
    int hacen_falta = 12;
    printf("alcanza: %d\n", hay >= hacen_falta);
    printf("faltan exactamente 3: %d\n", hacen_falta - hay == 3);
    return 0;
}
```

#### Al superarla
No alcanza, y faltan justo tres. Tizón sale corriendo a buscar carbón. Vuelve con cuatro bolsas, «por si acaso».

#### Imagen
- Un horno apagado con nueve bolsas de carbón al lado y tres huecos marcados con tiza.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) carga bolsas de carbón.

### Misión R01-N02-M1 · El reloj de arena

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Pasá 4000 segundos a horas, minutos y segundos usando
solo `/` y `%`, y mostralo también como `01:06:40` (pista: `%02d` rellena
con ceros hasta 2 cifras; se ve a fondo en el 05).

#### Criterio de aprobación

- Usa solo `/` y `%` para separar horas, minutos y segundos.
- Muestra `4000 segundos = 1 h 6 min 40 s`.
- Muestra el formato reloj `01:06:40` con `%02d`.

#### Salida esperada

```
4000 s = 1 h 6 min 40 s
01:06:40
```

#### Solución de referencia

```c
/*
 * Mision 1 - El reloj de arena: 4000 segundos -> horas, minutos, segundos.
 * %02d rellena con ceros a la izquierda hasta 2 cifras (01, 06...).
 */
#include <stdio.h>

int main(void)
{
    int total = 4000;
    int horas = total / 3600;
    int minutos = total % 3600 / 60;
    int segundos = total % 60;

    printf("%d s = %d h %d min %d s\n", total, horas, minutos, segundos);
    printf("%02d:%02d:%02d\n", horas, minutos, segundos);
    return 0;
}
```

### Misión R01-N02-M2 · El Puente del Juicio

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Pasa quien tiene nivel 5 o más **y** (llave **o**
magia) **y no** está maldito. Evaluá a Kira (nivel 6, con llave), Hulda (nivel
5, minera, sin llave) y Chispa (nivel 8, con llave, maldito). Después probá la
regla **sin** los paréntesis de `(llave || magia)` con un aprendiz mago de
nivel 1 y explicá por qué cambia el resultado.

#### Criterio de aprobación

- Evalúa la regla con paréntesis para Kira (1), Hulda (1) y Chispa (0).
- Muestra que sin los paréntesis el aprendiz de nivel 1 pasa, y explica que `&&` se evalúa antes que `||`.

#### Salida esperada

```
Kira pasa: 1
Hulda pasa: 1
Chispa pasa: 0
Aprendiz, con paréntesis: 0
Aprendiz, sin paréntesis: 1
```

#### Solución de referencia

```c
/*
 * Mision 2 - El Puente del Juicio.
 * Pasa quien tiene nivel >= 5, Y (llave O magia), Y NO esta maldito.
 */
#include <stdio.h>

int main(void)
{
    /* Kira: nivel 6, con llave */
    int nivel = 6, llave = 1, magia = 0, maldito = 0;
    printf("Kira pasa: %d\n", nivel >= 5 && (llave || magia) && !maldito);

    /* Hulda: nivel 5, minera, sin llave */
    nivel = 5; llave = 0; magia = 1; maldito = 0;
    printf("Hulda pasa: %d\n", nivel >= 5 && (llave || magia) && !maldito);

    /* Chispa: nivel 8, con llave, maldito */
    nivel = 8; llave = 1; magia = 0; maldito = 1;
    printf("Chispa pasa: %d\n", nivel >= 5 && (llave || magia) && !maldito);

    /* Aprendiz: nivel 1, mago. Sin parentesis, && va ANTES que ||:
       (nivel >= 5 && llave) || (magia && !maldito)  -> 1 (¡y no deberia!) */
    nivel = 1; llave = 0; magia = 1; maldito = 0;
    printf("Aprendiz, con paréntesis: %d\n", nivel >= 5 && (llave || magia) && !maldito);
    printf("Aprendiz, sin paréntesis: %d\n", (nivel >= 5 && llave) || (magia && !maldito));
    return 0;
}
```

### Misión R01-N02-M3 · Predicción

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con `ataque = 20` y `defensa = 6`, anotá qué da cada línea
**antes** de ejecutarla: `ataque - defensa * 2`, `(ataque - defensa) * 2`,
`ataque / defensa + 1`, `ataque % defensa * 2`,
`!(ataque > 10) || defensa`, `ataque > 10 ? ataque : 0`,
`(double) ataque / defensa`.

#### Criterio de aprobación

- Deja anotada la predicción de cada expresión en un comentario.
- Muestra el resultado real de las siete expresiones.
- Usa `%.2f` para la división con `double`.

#### Salida esperada

```
8
28
4
4
1
20
3.33
```

#### Solución de referencia

```c
/*
 * Mision 3 - Prediccion: el resultado de cada linea esta anotado antes de ejecutar.
 */
#include <stdio.h>

int main(void)
{
    int ataque = 20;
    int defensa = 6;
    printf("%d\n", ataque - defensa * 2);        /* 20 - 12 = 8 */
    printf("%d\n", (ataque - defensa) * 2);      /* 14 * 2 = 28 */
    printf("%d\n", ataque / defensa + 1);        /* 3 + 1 = 4 (division entera) */
    printf("%d\n", ataque % defensa * 2);        /* 2 * 2 = 4 */
    printf("%d\n", !(ataque > 10) || defensa);   /* 0 || 6 -> 1 (6 es "verdadero") */
    printf("%d\n", ataque > 10 ? ataque : 0);    /* 20 */
    printf("%.2f\n", (double) ataque / defensa); /* 3.33 */
    return 0;
}
```

### Encargo R01-N02-E1 · El año bisiesto del escriba

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El escriba necesita saber si un año es **bisiesto**: lo es si es divisible por
4 y no por 100, **o** si es divisible por 400. Escribí la expresión y probala
con 1900, 2000, 2024 y 2026 (tiene que dar 0, 1, 1, 0).

#### Criterio de aprobación

- Escribe la regla en una sola expresión con `%`, `&&` y `||`.
- Muestra 0, 1, 1, 0 para 1900, 2000, 2024 y 2026.

#### Salida esperada

```
1900: 0
2000: 1
2024: 1
2026: 0
```

#### Solución de referencia

```c
/*
 * Encargo del Gremio - Los anios bisiestos del calendario del escriba.
 * Bisiesto: divisible por 4 y no por 100, O divisible por 400.
 */
#include <stdio.h>

int main(void)
{
    int anio = 1900;
    printf("%d: %d\n", anio, (anio % 4 == 0 && anio % 100 != 0) || anio % 400 == 0);
    anio = 2000;
    printf("%d: %d\n", anio, (anio % 4 == 0 && anio % 100 != 0) || anio % 400 == 0);
    anio = 2024;
    printf("%d: %d\n", anio, (anio % 4 == 0 && anio % 100 != 0) || anio % 400 == 0);
    anio = 2026;
    printf("%d: %d\n", anio, (anio % 4 == 0 && anio % 100 != 0) || anio % 400 == 0);
    return 0;
}
```

### Prueba del sello

#### ¿Qué dan `7 / 2`, `7.0 / 2`, `7 % 2` y `(double) (7 / 2)`?

`3`, `3.5`, `1` y `3.0`.

#### ¿Qué da `5 > 3` en C? ¿Y `!7`?

`1` (en C, verdadero es 1). `!7` da `0`: cualquier valor distinto de 0 es verdadero.

#### Si `x` vale 5, ¿cuánto valen `a` y `x` después de `int a = x++;`?

`a` vale 5 (se usa el valor antes de sumar) y `x` vale 6.

#### ¿Por qué `if (vida = 0)` compila? ¿Qué hace?

Porque `=` asigna: pone la vida en 0 y el `if` pregunta por ese 0 (falso). Con `-Wall` el compilador avisa; lo correcto es `==`.

#### ¿Por qué `n > 0 && 100 / n > 5` no falla cuando `n` es 0?

Por el **cortocircuito**: si `n > 0` es falso, `&&` ya sabe que todo es falso y no evalúa la división.

#### ¿Cuánto vale `2 + 3 * 4 % 5`?

`4`: primero `3 * 4 = 12`, después `12 % 5 = 2`, y por último `2 + 2`.

### Soluciones (docente)

Material original: `01-C/03-Operadores` (soluciones completas en `soluciones/`, con sus archivos de entrada y salida).

## R01-N03 · Operadores de bits

```meta
tipo: tema
criatura: goblin
padre: R01-N02
precio: 10
temas: prog.bits
```

### Crónica

La puerta del pañol de la Forja tiene una cerradura con **ocho palancas**: cada una arriba o abajo. Kira la intenta abrir a patadas (en la pared, la cuenta de espadazos suma una patada, «por las dudas»). La cerradura no se mueve.

Tizón la mira, anota algo en la libreta y mueve tres palancas a la vez con una **máscara**. *Clac*. —Ocho preguntas de sí o no caben en **un solo byte** —dice, colorado de orgullo.

—Fue suerte —dice Kira. {mentor} le pasa a ella el tablero de estados de los aprendices: envenenado, dormido, invisible, bendecido… —Entonces practicá la suerte —gruñe.

### Objetivos

Entender que un número son **bits**, leerlo en hexadecimal y usar los operadores
de bits para guardar varias banderas en un solo número y para separar las partes
de un valor (por ejemplo, los canales de un color).

### Antes de empezar

- `unsigned` y `uint8_t`/`uint32_t` (02).
- Operadores y precedencia (03).

### Explicación

#### Binario y hexadecimal
En la memoria todo son **bits** (0 o 1). Un `uint8_t` tiene 8: el número 42 se
guarda como `0010 1010` (32 + 8 + 2). Escribir en binario es largo, así que se
usa **hexadecimal** (base 16): cada cifra hexa (`0`–`9`, `a`–`f`) son
**exactamente 4 bits**.

| Decimal | Binario | Hexa |
|---|---|---|
| 10 | `1010` | `a` |
| 15 | `1111` | `f` |
| 42 | `0010 1010` | `2a` |
| 255 | `1111 1111` | `ff` |

- En C, un número que empieza con `0x` es hexa: `0x2A`. Con `0` adelante es
  **octal** (base 8): `0754`. ¡Ojo: `010` vale 8!
- `printf`: `%x` muestra en hexa, `%X` en mayúsculas, `%#x` agrega el `0x`,
  `%08X` rellena con ceros hasta 8 cifras y `%o` muestra en octal.
- El bit `k` de `x` se obtiene con `(x >> k) & 1`. El ejemplo muestra así los
  8 bits de 42.

#### Los operadores
| Operador | Nombre | Bit a bit | `1100 ? 1010` |
|---|---|---|---|
| `&` | Y | 1 si **los dos** son 1 | `1000` |
| `\|` | O | 1 si **alguno** es 1 | `1110` |
| `^` | O exclusivo (XOR) | 1 si son **distintos** | `0110` |
| `~` | NO | invierte cada bit | `~1100` → `…0011` |
| `<<` | desplazar a la izquierda | corre los bits; entran ceros | `1 << 4` = `10000` = 16 |
| `>>` | desplazar a la derecha | corre los bits hacia la derecha | `96 >> 3` = 12 |

- `x << k` equivale a multiplicar por 2ᵏ, y `x >> k` a dividir por 2ᵏ (con
  enteros sin signo).
- **No confundir** `&` con `&&` ni `|` con `||`. `&&` pregunta "¿los dos son
  verdaderos?" y da 1 o 0. `&` opera bit por bit: `6 & 1` da 0, pero `6 && 1`
  da 1.
- Usá operadores de bits con tipos **sin signo** (`unsigned`, `uint8_t`…). Con
  signo hay casos indefinidos.

#### Banderas (*flags*)
Cada bit es una pregunta de sí o no:
```c
#define ENVENENADO (1u << 0)   /* 0000 0001 */
#define DORMIDO    (1u << 1)   /* 0000 0010 */

uint8_t estado = 0;
estado |= ENVENENADO;               /* encender:  |=          */
estado &= ~ENVENENADO;              /* apagar:    &= con ~    */
estado ^= DORMIDO;                  /* invertir:  ^=          */
if (estado & DORMIDO) ...           /* preguntar: &  (≠ 0 = encendido) */
estado |= ENVENENADO | DORMIDO;     /* varias de una vez      */
```
Así se pasan opciones en muchas bibliotecas: `SDL_Init(SDL_INIT_VIDEO |
SDL_INIT_AUDIO)` le dice a SDL "video **y** audio" en un solo número.

#### Máscaras: sacar un pedazo de un número
Un color RGBA se guarda en 32 bits como `0xRRGGBBAA`. Para sacar el verde:
**desplazar** hasta que quede abajo de todo y **enmascarar** con `& 0xFF`,
que deja solo los 8 bits de abajo:
```c
unsigned int g = (color >> 16) & 0xFF;
```
Y para armar un color, al revés: cada parte a su lugar con `<<` y se juntan con
`|`.

#### Precedencia
Los operadores de bits tienen **menos** prioridad que las comparaciones:
`estado & DORMIDO == 0` se lee `estado & (DORMIDO == 0)`. **Siempre entre
paréntesis:** `(estado & DORMIDO) == 0`.

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo.
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`

### Código de ejemplo

```c
/*
 * 04 - Operadores de bits: & | ^ ~ << >>, banderas y mascaras.
 *
 *   make run
 */
#include <stdio.h>
#include <stdint.h>

/* Banderas: cada estado del personaje es UN bit de un byte. */
#define ENVENENADO  (1u << 0)   /* 0000 0001 */
#define DORMIDO     (1u << 1)   /* 0000 0010 */
#define INVISIBLE   (1u << 2)   /* 0000 0100 */
#define BENDECIDO   (1u << 3)   /* 0000 1000 */

int main(void)
{
    /* --- Hexadecimal: cada cifra son 4 bits --- */
    unsigned int n = 0x2A;                  /* 2A hexa = 42 decimal = 0010 1010 */
    printf("0x2A = %u (decimal) = %x (hexa) = %#x\n", n, n, n);

    /* Los 8 bits de un byte, del mas alto al mas bajo: (x >> k) & 1 da el bit k */
    uint8_t x = 42;
    printf("42 en binario: %u%u%u%u %u%u%u%u\n",
           (x >> 7) & 1u, (x >> 6) & 1u, (x >> 5) & 1u, (x >> 4) & 1u,
           (x >> 3) & 1u, (x >> 2) & 1u, (x >> 1) & 1u, x & 1u);

    /* --- Los operadores, bit a bit --- */
    uint8_t a = 0xC;   /* 1100 */
    uint8_t b = 0xA;   /* 1010 */
    printf("a & b  = %x   (1000: los dos en 1)\n", a & b);
    printf("a | b  = %x   (1110: alguno en 1)\n", a | b);
    printf("a ^ b  = %x   (0110: distintos)\n", a ^ b);
    printf("~a     = %x  (se invierten TODOS los bits del byte)\n", (uint8_t) ~a);
    printf("1 << 4 = %u  (desplazar a la izquierda = multiplicar por 2^4)\n", 1u << 4);
    printf("96 >> 3 = %u (desplazar a la derecha = dividir por 2^3)\n", 96u >> 3);

    /* --- Banderas: guardar varios si/no en un solo numero --- */
    uint8_t estado = 0;
    estado |= ENVENENADO;                   /* ENCENDER un bit: | */
    estado |= INVISIBLE;
    printf("\nestado = %#04x\n", estado);
    printf("¿envenenada? %d  ¿dormida? %d\n",
           (estado & ENVENENADO) != 0,      /* PREGUNTAR por un bit: & */
           (estado & DORMIDO) != 0);

    estado &= ~ENVENENADO;                  /* APAGAR un bit: & con el inverso */
    printf("toma un antídoto -> estado = %#04x, ¿envenenada? %d\n",
           estado, (estado & ENVENENADO) != 0);

    estado ^= INVISIBLE;                    /* INVERTIR un bit: ^ */
    printf("se quita la capa -> ¿invisible? %d\n", (estado & INVISIBLE) != 0);

    estado |= DORMIDO | BENDECIDO;          /* varias de una vez */
    printf("dormida y bendecida -> estado = %#04x\n", estado);

    /* --- Mascaras: sacar una parte de un numero ---
       Un color RGBA en 32 bits: 0xRRGGBBAA (asi lo guardan SDL y muchas bibliotecas) */
    uint32_t naranja = 0xFF8800FFu;
    unsigned int r = (naranja >> 24) & 0xFF;
    unsigned int g = (naranja >> 16) & 0xFF;
    unsigned int bl = (naranja >> 8) & 0xFF;
    unsigned int al = naranja & 0xFF;
    printf("\ncolor 0x%08X -> R=%u G=%u B=%u A=%u\n", naranja, r, g, bl, al);

    /* Armar un color a partir de sus partes */
    uint32_t violeta = (128u << 24) | (0u << 16) | (255u << 8) | 255u;
    printf("R=128 G=0 B=255 A=255 -> 0x%08X\n", violeta);
    return 0;
}
```

### Salida esperada

```
0x2A = 42 (decimal) = 2a (hexa) = 0x2a
42 en binario: 0010 1010
a & b  = 8   (1000: los dos en 1)
a | b  = e   (1110: alguno en 1)
a ^ b  = 6   (0110: distintos)
~a     = f3  (se invierten TODOS los bits del byte)
1 << 4 = 16  (desplazar a la izquierda = multiplicar por 2^4)
96 >> 3 = 12 (desplazar a la derecha = dividir por 2^3)

estado = 0x05
¿envenenada? 1  ¿dormida? 0
toma un antídoto -> estado = 0x04, ¿envenenada? 0
se quita la capa -> ¿invisible? 0
dormida y bendecida -> estado = 0x0a

color 0xFF8800FF -> R=255 G=136 B=0 A=255
R=128 G=0 B=255 A=255 -> 0x8000FFFF
```

### ¿Para qué sirve?

Los bits están en todos lados: los permisos de los archivos de Linux (`chmod 754`), los colores de una pantalla (`0xRRGGBBAA`), las banderas de configuración de bibliotecas como SDL u OpenGL, los registros de un microcontrolador (encender un LED es poner un bit en 1) y los protocolos de red, que empaquetan varios datos en pocos bytes para ahorrar espacio.

### Errores habituales

Mensajes reales de `gcc` 13 con `-Wall -Wextra`.

**Ogro: la precedencia de `&`.**
```
b.c:6:16: warning: suggest parentheses around comparison in operand of ‘&’ [-Wparentheses]
    6 |     if (estado & DORMIDO == 0) printf("despierta\n");
      |                ^
```

**Autómata Desbordado: desplazar de más.** Correr un `unsigned int` (32 bits) 32
lugares o más es comportamiento indefinido:
```
b.c:7:25: warning: left shift count >= width of type [-Wshift-count-overflow]
    7 |     unsigned int x = 1u << 32;
      |                         ^~
```

**Ogro: `&` por `&&`.** `if (tiene_llave & tiene_mapa)` con valores 2 y 1 da 0
(falso), aunque los dos sean "verdaderos".

**Ogro: el octal escondido.** `int dia = 09;` ni compila (9 no es una cifra
octal), y `010` vale 8.

**Ogro: apagar con `&=` sin `~`.** `estado &= ENVENENADO` no apaga ese bit: apaga
**todos los demás**.

### Micro-misión R01-N03-P1 · Las ocho palancas

```meta
lugar: El pañol de la Forja
personajes: Kira, Gheco, Tizón
carta: Hexadecimal | %x muestra en hexa · 0xFF = 255 = ocho bits en 1 · cada cifra hexa son 4 bits
recompensa: xp 10, oro 10
```

#### Escena
La cerradura del pañol tiene ocho palancas. Kira la intenta abrir a patadas; no se mueve. Tizón le muestra el número de la combinación, pero escrito raro: en **hexadecimal**.

#### Gheco sugiere
`%x` muestra un número en hexadecimal (base 16) y `%d`, en decimal. `0x` delante de un número dice que está escrito en hexa.

#### Desafío
Mostrá la combinación en hexadecimal y el número `0xFF` en decimal.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int combinacion = 173;
    printf("combinacion en hexa: %___\n", combinacion);
    printf("0xFF en decimal: %___\n", 0xFF);
    return 0;
}
```

#### Salida esperada
```
combinacion en hexa: ad
0xFF en decimal: 255
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int combinacion = 173;
    printf("combinacion en hexa: %x\n", combinacion);
    printf("0xFF en decimal: %d\n", 0xFF);
    return 0;
}
```

#### Al superarla
«ad». Tizón mueve las palancas siguiendo las dos cifras. *Clac*. Kira dice que fue suerte.

#### Imagen
- Una cerradura de hierro con ocho palancas, algunas arriba y otras abajo, y los caracteres 0xAD brillando encima.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) con el pie todavía levantado.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) con la mano en una palanca.

### Micro-misión R01-N03-P2 · Encender una bandera

```meta
lugar: El tablero de los aprendices
personajes: Kira, Gheco, Maese Ferrum
carta: OR de bits | estado | BANDERA enciende ese bit · los demás no cambian · 1 << n es el bit n
recompensa: xp 10, oro 10
```

#### Escena
En la pared hay un tablero con los estados de cada aprendiz: dormido, quemado, bendecido… Kira se quemó con el horno (otra vez). Ferrum le pide que lo anote **sin borrar** lo demás.

#### Gheco sugiere
Cada estado es un bit. `estado | QUEMADO` enciende ese bit y deja los otros como estaban. `1 << 2` es el bit 2 (vale 4).

#### Desafío
Encendé el bit de QUEMADO en el estado de Kira.

#### Código inicial
```c
#include <stdio.h>

#define DORMIDO   (1 << 0)
#define BENDECIDO (1 << 1)
#define QUEMADO   (1 << 2)

int main(void)
{
    int estado = BENDECIDO;
    estado = ___;
    printf("estado de Kira: %d\n", estado);
    printf("bendecida: %d, quemada: %d\n", (estado & BENDECIDO) != 0, (estado & QUEMADO) != 0);
    return 0;
}
```

#### Salida esperada
```
estado de Kira: 6
bendecida: 1, quemada: 1
```

#### Solución
```c
#include <stdio.h>

#define DORMIDO   (1 << 0)
#define BENDECIDO (1 << 1)
#define QUEMADO   (1 << 2)

int main(void)
{
    int estado = BENDECIDO;
    estado = estado | QUEMADO;
    printf("estado de Kira: %d\n", estado);
    printf("bendecida: %d, quemada: %d\n", (estado & BENDECIDO) != 0, (estado & QUEMADO) != 0);
    return 0;
}
```

#### Al superarla
Bendecida **y** quemada. Ferrum le pasa un ungüento. —Lo de bendecida no te salvó de nada, ¿no?

#### Imagen
- Un tablero de clavijas en la pared con tres luces: una apagada y dos encendidas.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) con una mano vendada.
- Maese Ferrum (herrero enorme, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) le pasa un frasco de ungüento.

### Micro-misión R01-N03-P3 · Apagar sin tocar lo demás

```meta
lugar: El tablero de los aprendices
personajes: Kira, Gheco, Tizón
carta: AND con NOT | estado & ~BANDERA apaga ese bit · ~ invierte todos los bits · & deja pasar solo los que están en 1 en los dos
recompensa: xp 10, oro 10
```

#### Escena
Tizón se pasó la noche durmiendo en la libreta. Hay que apagar su bit de DORMIDO, pero sin apagarle el de BENDECIDO, que le costó muchísimo conseguir.

#### Gheco sugiere
`~DORMIDO` tiene todos los bits en 1 **menos** el de DORMIDO. Con `estado & ~DORMIDO` se apaga solo ese.

#### Desafío
Apagá solo el bit DORMIDO.

#### Código inicial
```c
#include <stdio.h>

#define DORMIDO   (1 << 0)
#define BENDECIDO (1 << 1)

int main(void)
{
    int estado = DORMIDO | BENDECIDO;
    printf("antes: %d\n", estado);
    estado = estado & ___;
    printf("despues: %d\n", estado);
    return 0;
}
```

#### Salida esperada
```
antes: 3
despues: 2
```

#### Solución
```c
#include <stdio.h>

#define DORMIDO   (1 << 0)
#define BENDECIDO (1 << 1)

int main(void)
{
    int estado = DORMIDO | BENDECIDO;
    printf("antes: %d\n", estado);
    estado = estado & ~DORMIDO;
    printf("despues: %d\n", estado);
    return 0;
}
```

#### Al superarla
Tizón se despierta de un salto, bendecido y descansado, y mide el tablero para asegurarse de que no le tocaron nada más.

#### Imagen
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) dormido sobre la libreta abierta, con baba en una página llena de números.
- Una luz del tablero que se apaga mientras otra sigue encendida.

### Micro-misión R01-N03-P4 · Duplicar con un empujón

```meta
lugar: El horno de la Forja
personajes: Kira, Gheco, Tizón
carta: Desplazamientos | x << 1 duplica · x >> 1 divide por 2 (entero) · mueven los bits a la izquierda o a la derecha
recompensa: xp 15, oro 15
```

#### Escena
Cada vez que Tizón sopla el fuelle, la temperatura del horno se duplica (eso dice él). Kira quiere comprobarlo sin multiplicar.

#### Gheco sugiere
`x << 1` corre todos los bits un lugar a la izquierda: es multiplicar por 2. `x >> 1` es dividir por 2 (sin decimales).

#### Desafío
Completá los desplazamientos.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int grados = 100;
    printf("un soplido: %d\n", grados ___ 1);
    printf("tres soplidos: %d\n", grados ___ 3);
    printf("se enfria a la mitad: %d\n", grados ___ 1);
    return 0;
}
```

#### Salida esperada
```
un soplido: 200
tres soplidos: 800
se enfria a la mitad: 50
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int grados = 100;
    printf("un soplido: %d\n", grados << 1);
    printf("tres soplidos: %d\n", grados << 3);
    printf("se enfria a la mitad: %d\n", grados >> 1);
    return 0;
}
```

#### Al superarla
800 grados con tres soplidos. Tizón, rojo de orgullo y de calor, se sienta a descansar lejos del horno.

#### Imagen
- Un horno con un termómetro de cobre que marca 100, 200, 800.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) sopla un fuelle con las mejillas infladas.

### Misión R01-N03-M1 · Las habilidades de la compañía

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Definí banderas `NADAR`, `TREPAR`,
`FORJAR`, `CURAR` y `SIGILO`. Kira nada y trepa, Tizón forja y trepa, y Hulda
cura. Hulda aprende a nadar y Tizón se lastima la mano (ya no trepa). Mostrá las
habilidades de todo el equipo juntas (`|`), las que Kira y Hulda tienen en común
(`&`) y si alguien tiene sigilo.

#### Criterio de aprobación

- Define cada habilidad como un bit distinto (`1 << n` o potencias de 2).
- Enciende con `|=`, apaga con `&= ~` y pregunta con `&`.
- Muestra las habilidades del equipo (`|`), las comunes entre Kira y Hulda (`&`) y si alguien tiene sigilo.

#### Salida esperada

```
Kira: 0x03  Tizon: 0x04  Hulda: 0x09
¿Tizon trepa? 0  ¿Hulda nada? 1
El equipo puede: 0x0f  Kira y Hulda en común: 0x01 (nadar)
¿Alguien tiene sigilo? 0
```

#### Solución de referencia

```c
/*
 * Mision 1 - Las habilidades de la compania, cada una en un bit.
 */
#include <stdio.h>
#include <stdint.h>

#define NADAR    (1u << 0)
#define TREPAR   (1u << 1)
#define FORJAR   (1u << 2)
#define CURAR    (1u << 3)
#define SIGILO   (1u << 4)

int main(void)
{
    uint8_t kira = NADAR | TREPAR;
    uint8_t tizon = FORJAR | TREPAR;
    uint8_t hulda  = CURAR;

    hulda |= NADAR;                 /* Hulda aprende a nadar */
    tizon &= ~TREPAR;              /* Tizon se lastima la mano: ya no trepa */

    printf("Kira: %#04x  Tizon: %#04x  Hulda: %#04x\n", kira, tizon, hulda);
    printf("¿Tizon trepa? %d  ¿Hulda nada? %d\n", (tizon & TREPAR) != 0, (hulda & NADAR) != 0);

    /* | junta las habilidades de todos; & las que tienen en comun */
    uint8_t equipo = kira | tizon | hulda;
    uint8_t en_comun = kira & hulda;
    printf("El equipo puede: %#04x  Kira y Hulda en común: %#04x (nadar)\n", equipo, en_comun);
    printf("¿Alguien tiene sigilo? %d\n", (equipo & SIGILO) != 0);
    return 0;
}
```

### Misión R01-N03-M2 · El tinte del herrero

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Separá el color `0x3366CCFF` en R, G, B y A.
Calculá el gris (el promedio de R, G y B) y armá el color gris conservando
el alfa.

#### Criterio de aprobación

- Separa R, G, B y A con `>>` y `& 0xFF`.
- Calcula el gris como promedio de R, G y B.
- Arma el color gris con `<<` y `|`, conservando el alfa.

#### Salida esperada

```
0x3366CCFF -> R=51 G=102 B=204 A=255
en gris (119): 0x777777FF
```

#### Solución de referencia

```c
/*
 * Mision 2 - El tinte del herrero: separar un color RGBA y pasarlo a gris.
 */
#include <stdio.h>
#include <stdint.h>

int main(void)
{
    uint32_t color = 0x3366CCFFu;
    unsigned int r = (color >> 24) & 0xFF;
    unsigned int g = (color >> 16) & 0xFF;
    unsigned int b = (color >> 8) & 0xFF;
    unsigned int a = color & 0xFF;
    printf("0x%08X -> R=%u G=%u B=%u A=%u\n", color, r, g, b, a);

    unsigned int gris = (r + g + b) / 3;
    uint32_t en_gris = (gris << 24) | (gris << 16) | (gris << 8) | a;
    printf("en gris (%u): 0x%08X\n", gris, en_gris);
    return 0;
}
```

### Misión R01-N03-M3 · Trucos de bits

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con `&` y `-`, averiguá si 37 es impar (`n & 1`) y si 64 y
96 son potencias de 2 (`n & (n - 1)` da 0 solo en las potencias de 2).
Multiplicá y dividí con `<<` y `>>`.

#### Criterio de aprobación

- Usa `n & 1` para saber si 37 es impar.
- Usa `n & (n - 1)` para decidir si 64 y 96 son potencias de 2.
- Multiplica y divide con `<<` y `>>`.

#### Salida esperada

```
37 es impar: 1
64 es potencia de 2: 1
96 es potencia de 2: 0
5 << 3 = 40 (5 * 8)
200 >> 2 = 50 (200 / 4)
```

#### Solución de referencia

```c
/*
 * Mision 3 - Trucos de bits de la Forja.
 *   n & 1          -> 1 si n es impar
 *   n & (n - 1)    -> 0 si n es potencia de 2 (tiene UN solo bit en 1)
 *   n << k         -> n * 2^k
 */
#include <stdio.h>

int main(void)
{
    unsigned int n = 37;
    printf("%u es impar: %u\n", n, n & 1u);
    n = 64;
    printf("%u es potencia de 2: %d\n", n, (n & (n - 1)) == 0);
    n = 96;
    printf("%u es potencia de 2: %d\n", n, (n & (n - 1)) == 0);
    printf("5 << 3 = %u (5 * 8)\n", 5u << 3);
    printf("200 >> 2 = %u (200 / 4)\n", 200u >> 2);
    return 0;
}
```

### Encargo R01-N03-E1 · Los permisos de Linux

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

En Linux, `chmod 754 archivo` fija los permisos con tres cifras **octales**: la
del dueño, la del grupo y la del resto. Cada cifra son 3 bits: leer (4),
escribir (2) y ejecutar (1). Con `0754`, separá las tres cifras (`>>` y `& 7`)
y mostralas como las muestra `ls -l`: `rwxr-xr--`.

#### Criterio de aprobación

- Separa las tres cifras de `0754` con `>>` y `& 7`.
- Muestra `rwxr-xr--`, eligiendo cada letra con `&`.

#### Salida esperada

```
permisos 754 -> dueño 7, grupo 5, resto 4
rwxr-xr--
¿el grupo puede escribir? 0
```

#### Solución de referencia

```c
/*
 * Encargo del Gremio - Los permisos de un archivo en Linux.
 * En "chmod 754", cada cifra (en octal) son 3 bits: r (4), w (2), x (1),
 * para el duenio, el grupo y el resto. 0754 en C es un numero OCTAL.
 */
#include <stdio.h>

int main(void)
{
    unsigned int permisos = 0754;
    unsigned int duenio = (permisos >> 6) & 7u;
    unsigned int grupo  = (permisos >> 3) & 7u;
    unsigned int resto  = permisos & 7u;

    printf("permisos %o -> dueño %u, grupo %u, resto %u\n", permisos, duenio, grupo, resto);
    printf("%c%c%c%c%c%c%c%c%c\n",
           duenio & 4u ? 'r' : '-', duenio & 2u ? 'w' : '-', duenio & 1u ? 'x' : '-',
           grupo & 4u ? 'r' : '-',  grupo & 2u ? 'w' : '-',  grupo & 1u ? 'x' : '-',
           resto & 4u ? 'r' : '-',  resto & 2u ? 'w' : '-',  resto & 1u ? 'x' : '-');
    printf("¿el grupo puede escribir? %d\n", (grupo & 2u) != 0);
    return 0;
}
```

### Prueba del sello

#### ¿Cuánto vale `0x1F` en decimal? ¿Y `0xFF`? ¿Cuántos bits representa cada cifra hexa?

`0x1F` = 31 y `0xFF` = 255. Cada cifra hexadecimal representa 4 bits.

#### ¿Qué dan `12 & 10`, `12 | 10` y `12 ^ 10`?

`8`, `14` y `6`.

#### ¿Cómo se enciende, se apaga y se pregunta por una bandera?

Encender: `x |= BANDERA`; apagar: `x &= ~BANDERA`; preguntar: `x & BANDERA` (distinto de 0 si está).

#### ¿Qué da `(0xAABBCCDD >> 8) & 0xFF`?

`0xCC` (204).

#### ¿Por qué `x & MASCARA == 0` está mal? ¿Cómo se escribe?

Porque `==` se evalúa antes que `&`: queda `x & (MASCARA == 0)`. Se escribe `(x & MASCARA) == 0`.

#### ¿Qué diferencia hay entre `6 & 1` y `6 && 1`?

`6 & 1` opera bit a bit y da 0 (6 es par); `6 && 1` es lógico y da 1 (los dos son verdaderos).

### Soluciones (docente)

Material original: `01-C/04-Bits` (soluciones completas en `soluciones/`, con sus archivos de entrada y salida).

## R01-N04 · Entrada y salida

```meta
tipo: tema
criatura: goblin
padre: R01-N03
precio: 10
temas: prog.salida, prog.entrada
```

### Crónica

En el mostrador de pedidos, Kira tiene que armar la tabla de precios de la Forja. La escribe rápido y la clava en la pared. Tizón llega con el calibre: —Esta columna está corrida un espacio. Esta otra, dos. Y este precio tiene un decimal de más.

Mientras tanto, en la ventanilla, el escriba le pregunta la edad a Chispa. —Diecinueve —contesta él, en letras. Le pide la altura: —Uno ochenta, con coma. El escriba anota lo que puede, y la ficha sale **cualquier cosa**. Del formulario se escapa el primer **goblin**, con un número robado bajo el brazo.

—El metal no adivina —dice {mentor}—. Lo que mostrás, alineado. Lo que te dan, revisado. Si no chequeás lo que entra, forjás basura.

### Objetivos

Mostrar datos con `printf` usando anchos, decimales y alineación; leer lo que
escribe el usuario con la **receta segura** (`fgets` + `sscanf`) y conocer las
trampas de `scanf`.

### Antes de empezar

- Tipos y formatos básicos de `printf` (02).
- Operadores (03).

### Explicación

#### `printf` a fondo
Cada `%` del texto es un lugar que se llena, en orden, con los valores que
siguen. Entre el `%` y la letra se puede indicar el formato:

| Marca | Para | Ejemplo con `7`, `1234.5`, `"Kira"` | Resultado |
|---|---|---|---|
| `%d` | entero | `%d` | `7` |
| `%5d` / `%-5d` | ancho 5, a la derecha / a la izquierda | | `    7` / `7    ` |
| `%05d` | ancho 5 con ceros | | `00007` |
| `%+d` | con signo siempre | | `+7` |
| `%.2f` | decimal con 2 decimales | | `1234.50` |
| `%10.2f` | ancho 10, 2 decimales | | `   1234.50` |
| `%e` | notación científica | | `1.234500e+03` |
| `%c` / `%s` | un carácter / un texto | | `K` / `Kira` |
| `%8s` / `%-8s` | texto en ancho 8 | | `    Kira` / `Kira    ` |
| `%x` / `%X` | hexa (04) | `255` | `ff` / `FF` |
| `%o` | octal | `255` | `377` |
| `%#x` / `%#o` | hexa con `0x` / octal con `0` adelante | `255` | `0xff` / `0377` |
| `%g` | el más corto entre `%f` y `%e` | `1234.5` | `1234.5` |
| `%+010.2f` | signo, ceros, ancho 10, 2 decimales | `3.7` | `+000003.70` |
| `%%` | un signo `%` | | `%` |

El ancho y la precisión también pueden venir **como argumentos**, con `*`:
`printf("%*.*f", 8, 2, 3.14159)` muestra `    3.14` (ancho 8, 2 decimales). Sirve
cuando el ancho de la tabla depende de los datos.

Los anchos sirven para armar **tablas alineadas**. Ojo: con tildes, `printf`
cuenta **bytes**, no letras (una letra con tilde ocupa 2 bytes en UTF-8), así que
la columna puede correrse un lugar. Se explica en el 11.

#### Dos salidas: `stdout` y `stderr`
`printf` escribe en la **salida estándar** (`stdout`). Hay otra, la **salida de
errores** (`stderr`), para los mensajes de error:
```c
fprintf(stderr, "No se pudo abrir el archivo\n");
```
En la terminal se ven las dos, pero se pueden separar: `./programa > salida.txt`
guarda solo `stdout` en el archivo y los errores siguen apareciendo en pantalla.

#### Leer del teclado: la receta segura
```c
char linea[100];                       /* un texto de hasta 99 letras (se ve en el 11) */
fgets(linea, sizeof(linea), stdin);    /* 1) leer la línea entera */
int edad = 0;
int leidos = sscanf(linea, "%d", &edad);  /* 2) sacar el número de esa línea */
```
1. **`fgets(texto, tamaño, stdin)`** lee **una línea completa**, con espacios,
   hasta el Enter. `stdin` es la entrada estándar (el teclado). **Nunca escribe
   más de `tamaño`**: no hay forma de desbordar el texto.
2. **`sscanf(linea, "%d", &edad)`** funciona como un `printf` al revés: busca
   en el texto lo que indica el formato y lo guarda en la variable. El `&`
   significa "la dirección de": `sscanf` necesita saber **dónde** guardar el
   valor (los punteros se ven en el 13; por ahora, **en `sscanf` las variables
   numéricas llevan `&`**).
3. **Devuelve cuántos datos pudo convertir**: 1 si leyó un número, 0 si no. Por
   ahora el ejemplo lo muestra; en el 06 se usa con un `if` para detectar
   errores y en el 07, con un bucle, para volver a preguntar.

Detalles:
- `fgets` deja el Enter (`\n`) al final del texto. Para sacarlo, la receta es
  `nombre[strcspn(nombre, "\n")] = '\0';` (con `#include <string.h>`; se
  entiende del todo en el 11).
- Para `double`, en `sscanf` va **`%lf`** (en `printf` alcanza con `%f`).
- Los decimales van con **punto**. C no usa el idioma del sistema salvo que se
  lo pidas.

#### Las trampas
**`sscanf` acepta a medias.** Con `"1,80"`, lee el `1`, se frena en la coma y
**dice que convirtió 1 dato**. La altura queda en `1.00` sin ningún aviso. (En el
07 se ve cómo exigir que no sobre nada.)

**`scanf` directo.** Existe `scanf("%d", &edad)`, que lee directamente del
teclado. Es cómodo pero traicionero:
- deja el Enter en la entrada, y un `fgets` posterior lee una línea **vacía**;
- si el usuario escribe letras, **las deja ahí**, y el próximo `scanf` vuelve a
  fallar con las mismas letras;
- `scanf("%s", nombre)` corta en el primer espacio y **no controla el tamaño**:
  un nombre largo desborda el texto.

Por eso en el curso se usa `fgets` + `sscanf`.

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo (la entrada de ejemplo ya está en la pestaña **Entrada**).
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**; las respuestas se escriben en la consola.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`
  - Con las respuestas en un archivo: `./programa < main.entrada.txt` (Linux) o `programa.exe < main.entrada.txt` (Windows).

El archivo `main.entrada.txt` tiene una respuesta por línea. Como las respuestas
no se muestran, en la salida las preguntas quedan pegadas.

### Código de ejemplo

```c
/*
 * 05 - Entrada y salida: printf a fondo, y leer del teclado de forma segura
 * con fgets + sscanf.
 *
 *   make run
 *   ./programa < main.entrada.txt     (las respuestas salen del archivo)
 */
#include <stdio.h>
#include <string.h>   /* strcspn, para sacar el Enter del final */

int main(void)
{
    /* --- printf a fondo --- */
    int nivel = 7;
    double oro = 1234.5;
    printf("[%d] [%5d] [%-5d] [%05d] [%+d]\n", nivel, nivel, nivel, nivel, nivel);
    printf("[%.2f] [%10.2f] [%-10.1f] [%e]\n", oro, oro, oro, oro);
    printf("[%c] [%s] [%8s] [%-8s] [%x] [%%]\n", 'K', "Kira", "Kira", "Kira", 255);

    /* --- Leer del teclado: la receta segura ---
       1) fgets lee la LINEA ENTERA (con espacios) en un texto;
       2) sscanf saca de ese texto el numero que necesitamos.
       char linea[100] es "un texto de hasta 99 letras" (se ve a fondo en el 11). */
    char linea[100];
    char nombre[32];

    printf("¿Cómo te llamás? ");
    fgets(nombre, sizeof(nombre), stdin);
    nombre[strcspn(nombre, "\n")] = '\0';    /* sacar el Enter que queda al final */

    printf("¿Cuántos años tenés? ");
    fgets(linea, sizeof(linea), stdin);
    int edad = 0;
    int leidos_edad = sscanf(linea, "%d", &edad);   /* devuelve CUANTOS datos convirtio */

    printf("¿Cuánto medís, en metros? ");
    fgets(linea, sizeof(linea), stdin);
    double altura = 0.0;
    int leidos_altura = sscanf(linea, "%lf", &altura); /* %lf para leer un double */

    printf("\n=== FICHA DE LA FORJA ===\n");
    printf("Nombre: %s\n", nombre);
    printf("Edad:   %d años (sscanf convirtió %d dato)\n", edad, leidos_edad);
    printf("Altura: %.2f m (sscanf convirtió %d dato)\n", altura, leidos_altura);
    printf("En 10 años vas a tener %d.\n", edad + 10);
    return 0;
}
```

### Entrada de ejemplo

```
Kira del Norte
19
1.68
```

### Salida esperada

```
[7] [    7] [7    ] [00007] [+7]
[1234.50] [   1234.50] [1234.5    ] [1.234500e+03]
[K] [Kira] [    Kira] [Kira    ] [ff] [%]
¿Cómo te llamás? ¿Cuántos años tenés? ¿Cuánto medís, en metros? 
=== FICHA DE LA FORJA ===
Nombre: Kira del Norte
Edad:   19 años (sscanf convirtió 1 dato)
Altura: 1.68 m (sscanf convirtió 1 dato)
En 10 años vas a tener 29.
```

### ¿Para qué sirve?

Todo programa habla con alguien: una terminal de autoservicio, una balanza de supermercado que imprime el ticket, un programa de consola que lee un archivo de configuración. Mostrar datos alineados (tickets, reportes, tablas) y, sobre todo, **no confiar** en lo que escribe el usuario son dos hábitos que separan un programa de juguete de uno que se puede usar de verdad.

### Errores habituales

Mensajes reales de `gcc` 13 con `-Wall -Wextra`.

**Goblin: olvidar el `&`.** `sscanf`/`scanf` recibe el **valor** en lugar de la
dirección y escribe quién sabe dónde:
```
e6.c:5:13: warning: format ‘%d’ expects argument of type ‘int *’, but argument 2 has type ‘int’ [-Wformat=]
    5 |     scanf("%d", edad);
      |            ~^   ~~~~
      |             |   |
      |             |   int
      |             int *
```

**Goblin: `%f` para un `double` al leer.**
```
s.c:5:13: warning: format ‘%f’ expects argument of type ‘float *’, but argument 2 has type ‘double *’ [-Wformat=]
      |            %lf
```

**Ogro: la coma decimal.** `1,80` se lee como `1`.

**Ogro: el Enter fantasma.** `scanf("%d")` seguido de `fgets` lee una línea
vacía.

**Ogro: el nombre con Enter.** Sin el `strcspn`, el `\n` queda dentro del nombre
y el texto que sigue aparece en la línea de abajo.

### Micro-misión R01-N04-P1 · La tabla torcida

```meta
lugar: El mostrador de pedidos
personajes: Kira, Gheco, Tizón
carta: Ancho en printf | %-8s texto a la izquierda en 8 lugares · %5d número a la derecha en 5 · %8.2f decimal en 8 con 2 decimales
recompensa: xp 10, oro 10
```

#### Escena
Kira clava la tabla de precios en la pared. Tizón llega con el calibre: —Esta columna está corrida. Y esta otra. Y este precio tiene un decimal de más.

#### Gheco sugiere
Entre el `%` y la letra va el **ancho**: `%-8s` ocupa 8 lugares alineado a la izquierda; `%5d` y `%8.2f`, a la derecha.

#### Desafío
Completá los formatos para que la tabla quede alineada.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    printf("%-8s %5s %8s\n", "pieza", "stock", "precio");
    printf("%___ %___ %___\n", "espada", 3, 45.5);
    printf("%___ %___ %___\n", "escudo", 12, 30.0);
    return 0;
}
```

#### Salida esperada
```
pieza    stock   precio
espada       3    45.50
escudo      12    30.00
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    printf("%-8s %5s %8s\n", "pieza", "stock", "precio");
    printf("%-8s %5d %8.2f\n", "espada", 3, 45.5);
    printf("%-8s %5d %8.2f\n", "escudo", 12, 30.0);
    return 0;
}
```

#### Al superarla
Tizón pasa el calibre por cada columna. Esta vez no encuentra nada. Se queda un rato mirando la tabla, casi decepcionado.

#### Imagen
- Una tabla de precios clavada en la pared, con columnas perfectamente alineadas.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) mide una columna con el calibre.

### Micro-misión R01-N04-P2 · La edad en números

```meta
lugar: La ventanilla de la Forja
personajes: Kira, Gheco, Chispa
criatura: goblin
carta: scanf | scanf("%d", &edad) lee un entero · el & dice DÓNDE guardarlo · sin &, el goblin se roba el número
recompensa: xp 10, oro 10
```

#### Escena
El escriba de la ventanilla le pregunta la edad a Chispa. El programa lee… y no guarda nada. Un **goblin** sale corriendo con el número bajo el brazo.
—Le faltó decirle **dónde** guardarlo —dice Gheco.

#### Gheco sugiere
`scanf("%d", &edad)` lee un entero y lo guarda **en** `edad`: el `&` es la dirección de la variable. Sin `&`, `scanf` no sabe dónde escribir.

#### Desafío
Completá el `scanf` para que lea la edad (la entrada ya está cargada).

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int edad = 0;
    scanf("%d", ___);
    printf("Edad de Chispa: %d\n", edad);
    return 0;
}
```

#### Entrada
```
30
```

#### Salida esperada
```
Edad de Chispa: 30
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int edad = 0;
    scanf("%d", &edad);
    printf("Edad de Chispa: %d\n", edad);
    return 0;
}
```

#### Al superarla
Treinta. —Treinta y pico —corrige Chispa, que nunca da un número exacto si puede evitarlo.

#### Imagen
- Una ventanilla de madera con un escriba enano detrás de una pila de fichas.
- Un goblin huye con un número 30 brillante.
- Chispa (mercader alto y flaco, sombrero de ala corta, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro) apoyado en la ventanilla.

### Micro-misión R01-N04-P3 · Dos datos en una línea

```meta
lugar: La ventanilla de la Forja
personajes: Kira, Gheco, Tizón
carta: scanf con varios | scanf("%d %lf", &a, &b) · %lf para leer un double · devuelve cuántos leyó
recompensa: xp 10, oro 10
```

#### Escena
Tizón trae los datos de un pedido en una sola línea: cantidad de piezas y peso de cada una. Kira tiene que calcular el peso total.

#### Gheco sugiere
Un `scanf` puede leer varios datos: `%d` para un `int` y `%lf` para un `double` (en `scanf`, **con l**). Cada variable con su `&`.

#### Desafío
Completá el formato y las direcciones.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int piezas;
    double peso;
    scanf("___", ___, ___);
    printf("%d piezas de %.1f kg: %.1f kg en total\n", piezas, peso, piezas * peso);
    return 0;
}
```

#### Entrada
```
4 2.5
```

#### Salida esperada
```
4 piezas de 2.5 kg: 10.0 kg en total
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int piezas;
    double peso;
    scanf("%d %lf", &piezas, &peso);
    printf("%d piezas de %.1f kg: %.1f kg en total\n", piezas, peso, piezas * peso);
    return 0;
}
```

#### Al superarla
Diez kilos. Tizón los pesa en la balanza de verdad, por las dudas: diez kilos y tres gramos. Se lo perdona.

#### Imagen
- Una balanza de bronce con cuatro piezas de hierro.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) compara la balanza con la libreta.

### Micro-misión R01-N04-P4 · La entrada que no es un número

```meta
lugar: La ventanilla de la Forja
personajes: Kira, Gheco, Chispa
criatura: goblin
carta: Leer seguro | fgets lee la línea entera · sscanf la interpreta · si devuelve 1, era un número
recompensa: xp 15, oro 15
```

#### Escena
Le piden a Chispa la altura y contesta «uno ochenta». El programa queda con cualquier cosa. Ferrum, desde lejos: —Si no revisás lo que te dan, forjás basura.

#### Gheco sugiere
La receta segura: `fgets` lee la línea entera y `sscanf` intenta sacar el número. `sscanf` devuelve cuántos datos pudo leer: si es 1, era un número.

#### Desafío
Completá la condición para avisar cuando lo que llega no es un número.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    char linea[50];
    int altura;
    fgets(linea, sizeof linea, stdin);
    if (sscanf(linea, "%d", &altura) ___) {
        printf("Eso no es una altura: %s", linea);
    } else {
        printf("Altura: %d cm\n", altura);
    }
    return 0;
}
```

#### Entrada
```
uno ochenta
```

#### Salida esperada
```
Eso no es una altura: uno ochenta
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    char linea[50];
    int altura;
    fgets(linea, sizeof linea, stdin);
    if (sscanf(linea, "%d", &altura) != 1) {
        printf("Eso no es una altura: %s", linea);
    } else {
        printf("Altura: %d cm\n", altura);
    }
    return 0;
}
```

#### Al superarla
La ventanilla rechaza el «uno ochenta». Chispa lo vuelve a intentar con «alto». Tampoco. Al final escribe 180, resignado.

#### Imagen
- Una ficha de papel con «uno ochenta» tachado en rojo.
- Chispa (mercader alto y flaco, sombrero de ala corta, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro) escribe en la ficha, resignado.

### Misión R01-N04-M1 · La calculadora de daño

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Pedí el ataque de Kira y la defensa del orco.
Mostrá el daño normal, el crítico (el doble), alineados con `%4d`, y cuántos
golpes hacen falta para vencer a un orco de 60 de vida (pista: redondear
hacia arriba con enteros es `(a + b - 1) / b`). Probalo con 23 y 9.

#### Criterio de aprobación

- Lee ataque y defensa con `fgets` + `sscanf`.
- Muestra el daño normal y el crítico alineados con `%4d`.
- Calcula los golpes para 60 de vida redondeando hacia arriba con enteros.

#### Entrada de ejemplo

```
23
9
```

#### Salida esperada

```
Ataque de Kira: Defensa del orco: 
Daño normal:    14
Daño crítico:   28
Golpes para vencer un orco de 60 de vida: 5
```

#### Solución de referencia

```c
/*
 * Mision 1 - La calculadora de danio.
 * Probar con:  ./sol < mision1_danio.entrada.txt
 */
#include <stdio.h>

int main(void)
{
    char linea[100];
    int ataque = 0, defensa = 0;

    printf("Ataque de Kira: ");
    fgets(linea, sizeof(linea), stdin);
    sscanf(linea, "%d", &ataque);

    printf("Defensa del orco: ");
    fgets(linea, sizeof(linea), stdin);
    sscanf(linea, "%d", &defensa);

    int danio = ataque - defensa;
    int critico = danio * 2;
    printf("\nDaño normal:  %4d\n", danio);
    printf("Daño crítico: %4d\n", critico);
    printf("Golpes para vencer un orco de 60 de vida: %d\n", (60 + danio - 1) / danio);
    return 0;
}
```

#### Pruebas

##### Defensa mayor que el ataque
```entrada
5
9
```
```salida
Ataque de Kira: Defensa del orco:
Daño normal:    -4
Daño crítico:   -8
Golpes para vencer un orco de 60 de vida: -13
```

##### Daño justo para un golpe
```entrada
69
9
```
```salida
Ataque de Kira: Defensa del orco:
Daño normal:    60
Daño crítico:  120
Golpes para vencer un orco de 60 de vida: 1
```

### Misión R01-N04-M2 · La tabla de la compañía

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Mostrá nombre, nivel, vida y precisión de Kira,
Tizón, Hulda y Chispa en columnas alineadas, y el oro del grupo con 8 cifras
(`00004250`).

#### Criterio de aprobación

- Muestra las cuatro filas en columnas alineadas con anchos fijos.
- Muestra el oro del grupo con 8 cifras (`00004250`).

#### Salida esperada

```
nombre   nivel  vida   prec
Kira         7   120   87.5
Tizon        9   160   72.2
Hulda        6    80   91.0
Chispa       8    95   99.9
Oro del grupo: 00004250
```

#### Solución de referencia

```c
/*
 * Mision 2 - La tabla de la compania, con anchos fijos.
 * %-8s: texto a la izquierda en 8 lugares; %5d: entero a la derecha en 5;
 * %6.1f: decimal en 6 lugares con 1 decimal.
 */
#include <stdio.h>

int main(void)
{
    printf("%-8s %5s %5s %6s\n", "nombre", "nivel", "vida", "prec");
    printf("%-8s %5d %5d %6.1f\n", "Kira", 7, 120, 87.5);
    printf("%-8s %5d %5d %6.1f\n", "Tizon", 9, 160, 72.25);   /* 72.25 -> "72.2": justo en el medio, printf redondea al par */
    printf("%-8s %5d %5d %6.1f\n", "Hulda", 6, 80, 91.0);
    printf("%-8s %5d %5d %6.1f\n", "Chispa", 8, 95, 99.9);
    printf("Oro del grupo: %08d\n", 4250);
    return 0;
}
```

### Misión R01-N04-M3 · La trampa de la coma

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé tres alturas: `1.80`, `1,80` y `uno ochenta`.
Para cada una, mostrá qué valor quedó y cuántos datos dijo `sscanf` que
convirtió. ¿Cuál es la más peligrosa?

#### Criterio de aprobación

- Lee las tres alturas y muestra el valor que quedó y lo que devolvió `sscanf` para cada una.
- Explica en un comentario que `1,80` es la más peligrosa: convierte 1 dato y queda 1.00 sin aviso.

#### Entrada de ejemplo

```
1.80
1,80
uno ochenta
```

#### Salida esperada

```
Altura con punto: -> leí 1.80 (convertidos: 1)
Altura con coma: -> leí 1.00 (convertidos: 1)  <- ¡se perdió el ,80!
Altura en palabras: -> altura sigue en -1.00 (convertidos: 0)
```

#### Solución de referencia

```c
/*
 * Mision 3 - La trampa de la coma.
 * En C (sin configurar el idioma) los decimales van con PUNTO. Con "1,80",
 * sscanf lee el 1, se frena en la coma y AUN ASI dice "converti 1 dato".
 * Probar con:  ./sol < mision3_trampa.entrada.txt
 */
#include <stdio.h>

int main(void)
{
    char linea[100];
    double altura = 0.0;

    printf("Altura con punto: ");
    fgets(linea, sizeof(linea), stdin);
    int n1 = sscanf(linea, "%lf", &altura);
    printf("-> leí %.2f (convertidos: %d)\n", altura, n1);

    printf("Altura con coma: ");
    fgets(linea, sizeof(linea), stdin);
    int n2 = sscanf(linea, "%lf", &altura);
    printf("-> leí %.2f (convertidos: %d)  <- ¡se perdió el ,80!\n", altura, n2);

    printf("Altura en palabras: ");
    fgets(linea, sizeof(linea), stdin);
    altura = -1.0;
    int n3 = sscanf(linea, "%lf", &altura);
    printf("-> altura sigue en %.2f (convertidos: %d)\n", altura, n3);
    return 0;
}
```

#### Pruebas

##### Otras alturas
```entrada
2.05
0,5
1.80 metros
```
```salida
Altura con punto: -> leí 2.05 (convertidos: 1)
Altura con coma: -> leí 0.00 (convertidos: 1)  <- ¡se perdió el ,80!
Altura en palabras: -> altura sigue en 1.80 (convertidos: 1)
```

### Encargo R01-N04-E1 · El recibo de la ferretería

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

La ferretería del Gremio necesita un **recibo**: pedí el producto (puede tener
espacios, como "Clavos de acero"), la cantidad y el precio unitario. Mostrá el
subtotal, el IVA (21 %) y el total, alineados con 2 decimales.

#### Criterio de aprobación

- Lee el producto con espacios usando `fgets` y le saca el `\n`.
- Muestra subtotal, IVA (21 %) y total alineados con 2 decimales.

#### Entrada de ejemplo

```
Clavos de acero
250
12.40
```

#### Salida esperada

```
Producto: Cantidad: Precio unitario: 
----------------------------------
Clavos de acero       250 x    12.40
Subtotal                       3100.00
IVA 21%                         651.00
TOTAL                          3751.00
----------------------------------
```

#### Solución de referencia

```c
/*
 * Encargo del Gremio - El recibo de la ferreteria.
 * El nombre del producto puede tener espacios: se lee con fgets.
 * Probar con:  ./sol < gremio_recibo.entrada.txt
 */
#include <stdio.h>
#include <string.h>

int main(void)
{
    char linea[100];
    char producto[40];
    int cantidad = 0;
    double precio = 0.0;

    printf("Producto: ");
    fgets(producto, sizeof(producto), stdin);
    producto[strcspn(producto, "\n")] = '\0';

    printf("Cantidad: ");
    fgets(linea, sizeof(linea), stdin);
    sscanf(linea, "%d", &cantidad);

    printf("Precio unitario: ");
    fgets(linea, sizeof(linea), stdin);
    sscanf(linea, "%lf", &precio);

    double subtotal = cantidad * precio;
    double iva = subtotal * 0.21;
    printf("\n----------------------------------\n");
    printf("%-20s %4d x %8.2f\n", producto, cantidad, precio);
    printf("%-20s %17.2f\n", "Subtotal", subtotal);
    printf("%-20s %17.2f\n", "IVA 21%", iva);
    printf("%-20s %17.2f\n", "TOTAL", subtotal + iva);
    printf("----------------------------------\n");
    return 0;
}
```

#### Pruebas

##### Un solo producto barato
```entrada
Tornillo
1
0.10
```
```salida
Producto: Cantidad: Precio unitario:
----------------------------------
Tornillo                1 x     0.10
Subtotal                          0.10
IVA 21%                           0.02
TOTAL                             0.12
----------------------------------
```

##### Cantidad grande
```entrada
Chapa galvanizada
1000
3500.75
```
```salida
Producto: Cantidad: Precio unitario:
----------------------------------
Chapa galvanizada    1000 x  3500.75
Subtotal                    3500750.00
IVA 21%                      735157.50
TOTAL                       4235907.50
----------------------------------
```

### Prueba del sello

#### ¿Qué muestran `printf("[%-6s|%4d]", "Hulda", 42)` y `printf("%07.2f", 3.14159)`?

`[Hulda |  42]` y `0003.14`.

#### ¿Qué diferencia hay entre `stdout` y `stderr`?

`stdout` es la salida normal; `stderr`, la de errores. Se pueden separar: `./programa > salida.txt` guarda solo `stdout`.

#### ¿Por qué se prefiere `fgets` + `sscanf` en lugar de `scanf`?

Porque `fgets` lee la línea entera sin pasarse del tamaño, y `sscanf` convierte desde ese texto: no quedan restos en la entrada ni se desborda nada.

#### ¿Qué devuelve `sscanf`? ¿Qué devuelve con `"hola"` y `"%d"`?

Cuántos datos pudo convertir. Con `"hola"` y `"%d"` devuelve 0.

#### ¿Por qué `sscanf` necesita `&edad` y no `edad`?

Porque necesita saber **dónde** guardar el valor: `&edad` es la dirección de la variable. Con `edad` recibiría el valor y escribiría en cualquier lado.

#### ¿Qué pasa si el usuario escribe `1,80` y leés con `%lf`?

Lee el `1`, se frena en la coma y devuelve 1: queda 1.00 sin ningún aviso.

### Soluciones (docente)

Material original: `01-C/05-EntradaSalida` (soluciones completas en `soluciones/`, con sus archivos de entrada y salida).

## R01-N05 · Condicionales

```meta
tipo: tema
criatura: ogro
padre: R01-N04
precio: 10
temas: prog.condicionales, err.validacion
```

### Crónica

El horno grande tiene tres temperaturas: brasas para los aprendices, rojo para los oficiales y blanco para el maestro. Kira escribe la regla en la pizarra: «si hace calor, más fuego». Nada más.

Al rato el horno está blanco, después más blanco, y la pizarra empieza a humear. Faltaba decir **qué hacer si no**. Tizón llega con el balde de agua justo a tiempo; Ferrum, con las cejas un poco más cortas que a la mañana.

—Cada camino tiene que estar escrito —dice {mentor}, apagando la pizarra con el guante—. Y si alguien te contesta *hola* cuando le preguntás la experiencia, lo mandás a la puerta. Nada de adivinar.

### Objetivos

Hacer que el programa **decida**: `if`/`else if`/`else` para condiciones y
rangos, `switch` para comparar un valor contra casos fijos y el ternario para
elegir entre dos valores. Usar lo que devuelve `sscanf` para **detectar datos
inválidos**.

### Antes de empezar

- Operadores de comparación y lógicos; en C, 0 es falso y cualquier otro número
  es verdadero (03).
- `fgets` + `sscanf` y su valor de retorno (05).

### Explicación

#### Bloques
Las llaves `{ }` agrupan instrucciones en un **bloque**. Una variable declarada
dentro de un bloque solo existe ahí adentro (se ve a fondo en el 08).

#### `if` / `else if` / `else`
```c
if (experiencia < 100) {
    printf("Aprendiz\n");
} else if (experiencia < 500) {
    printf("Oficial\n");
} else {
    printf("Maestro\n");
}
```
- La condición va entre paréntesis. Vale cualquier expresión: si da distinto
  de 0, es verdadera.
- Se evalúan **en orden** y se ejecuta **solo la primera** que se cumple. Por
  eso, en los rangos alcanza con el límite de arriba: si llegó al segundo
  `else if`, ya se sabe que no era menor que 100.
- Con una sola instrucción las llaves son opcionales, pero **ponelas siempre**.

#### Detectar datos inválidos
```c
if (sscanf(linea, "%d", &experiencia) != 1) {
    fprintf(stderr, "Eso no es un número.\n");
    return 1;
}
```
Si `sscanf` no pudo convertir un número, se avisa por `stderr` y `main` termina
con `return 1` (código de error). Volver a preguntar en lugar de terminar
necesita un bucle (07).

Al correr `printf 'hola\n' | ./programa`, el mensaje de error puede aparecer
**antes** que la pregunta. No es un error: cuando la salida no va a la terminal,
`stdout` acumula el texto en un *buffer* y lo muestra después, mientras que
`stderr` sale al instante.

#### `switch`
Compara **un** valor entero (o un `char`) contra casos **fijos**:
```c
switch (piso) {
    case 0:
        printf("brasas\n");
        break;            /* ¡sin break sigue de largo al próximo case! */
    case 1:
    case 2:               /* varios casos, el mismo código */
        printf("yunques\n");
        break;
    default:              /* si no coincidió ninguno */
        printf("cámara del maestro\n");
        break;
}
```
- Sin `break`, la ejecución **cae** al caso siguiente. Eso sirve para agrupar
  casos vacíos (`case 1: case 2:`), pero olvidarlo en un caso con código es un
  error clásico. `gcc -Wextra` lo avisa.
- Solo funciona con enteros y `char` (un `char` es un número, 02): no con
  `double` ni con textos.
- Para rangos (`< 100`), `if`. Para valores exactos (1, 2, 3, `'a'`), `switch`.

#### Ternario
Para **elegir un valor**, no para ejecutar cosas:
```c
int bonus = experiencia % 2 == 0 ? 10 : 5;
printf("%s\n", experiencia % 2 == 0 ? "par" : "impar");
```

#### Leer una letra
`linea[0]` es la **primera letra** de lo que escribió el usuario (los textos se
indexan desde 0; se ve en el 10 y el 11). Con eso se puede hacer un `switch`
sobre la letra, aceptando mayúsculas y minúsculas con casos agrupados.

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo (la entrada de ejemplo ya está en la pestaña **Entrada**).
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**; las respuestas se escriben en la consola.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`
  - Con las respuestas en un archivo: `./programa < main.entrada.txt` (Linux) o `programa.exe < main.entrada.txt` (Windows).

### Código de ejemplo

```c
/*
 * 06 - Condicionales: if / else if / else, switch y ternario.
 *
 *   make run
 *   ./programa < main.entrada.txt
 */
#include <stdio.h>

int main(void)
{
    char linea[100];
    int experiencia = 0;

    printf("Experiencia del aprendiz: ");
    fgets(linea, sizeof(linea), stdin);

    /* sscanf devuelve cuantos datos convirtio: si no es 1, no era un numero */
    if (sscanf(linea, "%d", &experiencia) != 1) {
        fprintf(stderr, "Eso no es un número.\n");
        return 1;                              /* terminar con codigo de error */
    }

    /* --- if / else if / else: se ejecuta SOLO el primero que se cumple --- */
    if (experiencia < 0) {
        printf("La experiencia no puede ser negativa.\n");
        return 1;
    } else if (experiencia < 100) {
        printf("Rango: Aprendiz\n");
    } else if (experiencia < 500) {
        printf("Rango: Oficial\n");
    } else if (experiencia < 2000) {
        printf("Rango: Maestro herrero\n");
    } else {
        printf("Rango: Leyenda de la Forja\n");
    }

    /* --- Condiciones compuestas y anidadas --- */
    int tiene_martillo = 1;
    if (experiencia >= 500 && tiene_martillo) {
        printf("Puede forjar armas.\n");
        if (experiencia >= 1000) {
            printf("  ...incluso armas encantadas.\n");
        }
    }

    /* --- switch: UN valor contra varios casos exactos --- */
    int piso = experiencia / 250;              /* 0, 1, 2, 3... */
    switch (piso) {
        case 0:
            printf("Trabaja en el piso de las brasas.\n");
            break;
        case 1:
        case 2:                                /* 1 y 2 comparten el mismo codigo */
            printf("Trabaja en el piso de los yunques.\n");
            break;
        default:                               /* cualquier otro valor */
            printf("Trabaja en la cámara del maestro.\n");
            break;
    }

    /* switch con letras: un char es un numero, asi que tambien sirve */
    printf("Especialidad (a = armas, h = herraduras, j = joyas): ");
    fgets(linea, sizeof(linea), stdin);
    char especialidad = linea[0];              /* la primera letra de la linea */
    switch (especialidad) {
        case 'a':
        case 'A':
            printf("\nForja armas.\n");
            break;
        case 'h':
        case 'H':
            printf("\nForja herraduras.\n");
            break;
        case 'j':
        case 'J':
            printf("\nTalla joyas.\n");
            break;
        default:
            printf("\nEspecialidad desconocida: '%c'\n", especialidad);
            break;
    }

    /* --- Ternario: elegir entre dos VALORES --- */
    int bonus = experiencia % 2 == 0 ? 10 : 5;
    printf("Bonus del día: %d (experiencia %s)\n", bonus, experiencia % 2 == 0 ? "par" : "impar");
    return 0;
}
```

### Entrada de ejemplo

```
750
A
```

### Salida esperada

```
Experiencia del aprendiz: Rango: Maestro herrero
Puede forjar armas.
Trabaja en la cámara del maestro.
Especialidad (a = armas, h = herraduras, j = joyas): 
Forja armas.
Bonus del día: 10 (experiencia par)
```

### ¿Para qué sirve?

Cada decisión de un programa es un `if`: el cajero que no te deja sacar más de lo que tenés, la app que calcula el envío según la zona, el termostato que prende la calefacción. El `switch` aparece en los menús de opciones y en los intérpretes de comandos; y validar la entrada antes de decidir es lo que evita que un dato mal escrito termine en una cuenta equivocada.

### Errores habituales

Mensajes reales de `gcc` 13 con `-Wall -Wextra`.

**Ogro: el punto y coma asesino.** El `;` después del `if` es una instrucción
vacía: el `printf` se ejecuta **siempre**. `gcc` lo detecta dos veces:
```
c6.c:5:19: warning: suggest braces around empty body in an ‘if’ statement [-Wempty-body]
    5 |     if (vida < 10);
      |                   ^
c6.c:5:5: warning: this ‘if’ clause does not guard... [-Wmisleading-indentation]
```

**Ogro: el `switch` que cae.**
```
c6.c:10:26: warning: this statement may fall through [-Wimplicit-fallthrough=]
   10 |     switch (n) { case 1: printf("a\n"); case 2: printf("b\n"); break; }
      |                          ^~~~~~~~~~~~~
```

**Goblin: `switch` sobre un decimal.**
```
c6.c:8:13: error: switch quantity not an integer
    8 |     switch (d) { case 1: break; }
      |             ^
```

**Ogro: `=` en lugar de `==` en el `if`** (visto en el 03).

**Ogro: rangos en el orden equivocado.** Si el primer `if` es
`experiencia < 2000`, **todos** los menores de 2000 entran ahí y los rangos
de abajo nunca se alcanzan.

### Micro-misión R01-N05-P1 · El horno que se derrite

```meta
lugar: El horno de tres temperaturas
personajes: Kira, Gheco, Tizón
carta: if y else | if (condición) { … } else { … } · cada camino escrito · las llaves marcan qué va en cada uno
recompensa: xp 10, oro 10
```

#### Escena
Kira escribió «si hace calor, más fuego» y nada más. El horno está blanco y la pizarra humea. Tizón llega con un balde de agua.

#### Gheco sugiere
Con `if … else` hay **dos caminos**: uno si la condición es verdadera, el otro si no. Sin `else`, cuando la condición es falsa no pasa nada.

#### Desafío
Agregá el `else` para que, si el horno ya está muy caliente, se baje el fuego.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int grados = 1300;
    if (grados < 1000) {
        printf("mas fuego\n");
    } ___ {
        printf("bajar el fuego\n");
    }
    printf("horno a %d grados\n", grados);
    return 0;
}
```

#### Salida esperada
```
bajar el fuego
horno a 1300 grados
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int grados = 1300;
    if (grados < 1000) {
        printf("mas fuego\n");
    } else {
        printf("bajar el fuego\n");
    }
    printf("horno a %d grados\n", grados);
    return 0;
}
```

#### Al superarla
El horno baja a rojo. La pizarra deja de humear. Ferrum pasa, ve el balde de Tizón y no pregunta.

#### Imagen
- Un horno al blanco vivo y una pizarra que humea.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) corre con un balde de agua.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) con cara de culpa.

### Micro-misión R01-N05-P2 · El portero de los tres pisos

```meta
lugar: El horno de tres temperaturas
personajes: Kira, Gheco, Maese Ferrum
carta: else if | varios caminos en orden · se ejecuta el primero que se cumpla · el último else es «todo lo demás»
recompensa: xp 10, oro 10
```

#### Escena
La Forja tiene tres pisos: brasas para los aprendices (menos de 50 piezas), yunques para los oficiales (hasta 200) y la cámara del maestro para el resto.

#### Gheco sugiere
Con `else if` se encadenan condiciones: C prueba la primera, si no se cumple la segunda, y así. El `else` final atrapa todo lo que sobra.

#### Desafío
Completá las condiciones para mandar a Kira (140 piezas forjadas) a su piso.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int piezas = 140;
    if (piezas ___ 50) {
        printf("Piso de las brasas\n");
    } else if (piezas ___ 200) {
        printf("Piso de los yunques\n");
    } else {
        printf("Camara del maestro\n");
    }
    return 0;
}
```

#### Salida esperada
```
Piso de los yunques
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int piezas = 140;
    if (piezas < 50) {
        printf("Piso de las brasas\n");
    } else if (piezas <= 200) {
        printf("Piso de los yunques\n");
    } else {
        printf("Camara del maestro\n");
    }
    return 0;
}
```

#### Al superarla
Piso de los yunques. Kira esperaba la cámara del maestro. Ferrum: —Ciento cuarenta piezas y cuarenta y una a espadazos. Yunques.

#### Imagen
- Una escalera de piedra con tres pisos iluminados: brasas, yunques y una cámara dorada arriba.
- Maese Ferrum (herrero enorme, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) señala el piso del medio.

### Micro-misión R01-N05-P3 · Dos condiciones a la vez

```meta
lugar: El horno de tres temperaturas
personajes: Kira, Gheco, Tizón
carta: Lógicos | && (y) exige las dos · || (o) alcanza con una · ! niega
recompensa: xp 10, oro 10
```

#### Escena
Para templar, el horno tiene que estar entre 800 y 1000 grados **y** tiene que haber agua en el balde. Tizón revisa las dos cosas antes de dejar entrar a Kira.

#### Gheco sugiere
`a && b` es verdadero solo si **las dos** lo son. `a || b`, si **alguna** lo es. `!a` niega.

#### Desafío
Completá la condición: entre 800 y 1000 grados, y con agua.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int grados = 920;
    int hay_agua = 1;
    if (grados >= 800 ___ grados <= 1000 ___ hay_agua) {
        printf("Se puede templar\n");
    } else {
        printf("Todavia no\n");
    }
    return 0;
}
```

#### Salida esperada
```
Se puede templar
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int grados = 920;
    int hay_agua = 1;
    if (grados >= 800 && grados <= 1000 && hay_agua) {
        printf("Se puede templar\n");
    } else {
        printf("Todavia no\n");
    }
    return 0;
}
```

#### Al superarla
Se puede. Tizón le abre paso a Kira con una reverencia exagerada, y le recuerda que el agua es para el metal, no para él.

#### Imagen
- Un balde de agua junto a un horno con un termómetro que marca 920.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) hace una reverencia exagerada.

### Micro-misión R01-N05-P4 · El menú del herrero

```meta
lugar: El mostrador de pedidos
personajes: Kira, Gheco, Chispa
carta: switch | switch (opción) { case 1: … break; } · default para lo que no está · sin break, sigue de largo
recompensa: xp 15, oro 15
```

#### Escena
Chispa elige siempre la opción 2 del menú del herrero, y siempre le sale la 2 **y** la 3, y paga las dos. Sospecha de una estafa. Es un `break` que falta.

#### Gheco sugiere
En un `switch`, cada `case` necesita su `break;` al final: si no, sigue ejecutando el `case` de abajo.

#### Desafío
Agregá el `break` que falta para que Chispa pague solo lo que pidió.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int opcion = 2;
    switch (opcion) {
    case 1:
        printf("Afilar: 3 lingotes\n");
        break;
    case 2:
        printf("Templar: 5 lingotes\n");
    case 3:
        printf("Pulir: 2 lingotes\n");
        break;
    default:
        printf("Esa opcion no existe\n");
    }
    return 0;
}
```

#### Salida esperada
```
Templar: 5 lingotes
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int opcion = 2;
    switch (opcion) {
    case 1:
        printf("Afilar: 3 lingotes\n");
        break;
    case 2:
        printf("Templar: 5 lingotes\n");
        break;
    case 3:
        printf("Pulir: 2 lingotes\n");
        break;
    default:
        printf("Esa opcion no existe\n");
    }
    return 0;
}
```

#### Al superarla
Cinco lingotes, solo templar. Chispa reclama los pulidos que pagó de más en todas las visitas anteriores. Ferrum le contesta con el martillo en la mano.

#### Imagen
- Un cartel de madera con un menú: 1 Afilar, 2 Templar, 3 Pulir.
- Chispa (mercader alto y flaco, sombrero de ala corta, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro) reclama con una lista larguísima de recibos.
- Maese Ferrum (herrero enorme, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) con el martillo al hombro.

### Misión R01-N05-M1 · El color del metal

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Pedí la temperatura del hierro y mostrá su estado:
menos de 500 °C, frío; menos de 900, rojo oscuro (listo para doblar); menos
de 1200, naranja (ideal para forjar); hasta 1538, amarillo blanco; más,
fundido. Rechazá temperaturas negativas y lo que no sea un número.

#### Criterio de aprobación

- Usa `else if` en orden para los cinco estados del metal.
- Rechaza lo que no es un número (`sscanf` distinto de 1) y las temperaturas negativas.

#### Entrada de ejemplo

```
1000
```

#### Salida esperada

```
Temperatura del hierro (°C): 
Naranja: ideal para forjar.
```

#### Solución de referencia

```c
/*
 * Mision 1 - El color del metal.
 * Segun la temperatura, el herrero sabe si el hierro esta listo.
 * Probar con:  ./sol < mision1_temple.entrada.txt
 */
#include <stdio.h>

int main(void)
{
    char linea[100];
    int grados = 0;

    printf("Temperatura del hierro (°C): ");
    fgets(linea, sizeof(linea), stdin);
    if (sscanf(linea, "%d", &grados) != 1) {
        printf("\nEso no es una temperatura.\n");
        return 0;
    }

    printf("\n");
    if (grados < 0) {
        printf("Imposible: el hierro no se congela así.\n");
    } else if (grados < 500) {
        printf("Frío: todavía no se puede trabajar.\n");
    } else if (grados < 900) {
        printf("Rojo oscuro: listo para doblar.\n");
    } else if (grados < 1200) {
        printf("Naranja: ideal para forjar.\n");
    } else if (grados <= 1538) {
        printf("Amarillo blanco: cuidado, casi se funde.\n");
    } else {
        printf("¡Se fundió! (el hierro funde a 1538 °C)\n");
    }
    return 0;
}
```

#### Pruebas

##### Frío
```entrada
20
```
```salida
Temperatura del hierro (°C):
Frío: todavía no se puede trabajar.
```

##### Bordes
```entrada
1538
```
```salida
Temperatura del hierro (°C):
Amarillo blanco: cuidado, casi se funde.
```

##### Fundido
```entrada
2000
```
```salida
Temperatura del hierro (°C):
¡Se fundió! (el hierro funde a 1538 °C)
```

##### Negativa
```entrada
-10
```
```salida
Temperatura del hierro (°C):
Imposible: el hierro no se congela así.
```

##### No es un número
```entrada
caliente
```
```salida
Temperatura del hierro (°C):
Eso no es una temperatura.
```

### Misión R01-N05-M2 · La calculadora del mercader

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé una cuenta en una línea, como
`12.5 * 4`, con `sscanf(linea, "%lf %c %lf", &a, &op, &b)` (tiene que
convertir **3** datos) y resolvela con un `switch` sobre el operador.
Aceptá `x` como sinónimo de `*` y no dividas por cero.

#### Criterio de aprobación

- Lee la cuenta con `sscanf(linea, "%lf %c %lf", ...)` y exige que convierta 3 datos.
- Resuelve con `switch`, aceptando `x` como `*` (dos `case` juntos).
- No divide por cero: avisa.

#### Entrada de ejemplo

```
12.5 * 4
```

#### Salida esperada

```
Cuenta (por ejemplo 12.5 * 4): 
12.50 * 4.00 = 50.00
```

#### Solución de referencia

```c
/*
 * Mision 2 - La calculadora del mercader: "numero operador numero".
 * sscanf puede leer varios datos de una linea: "%lf %c %lf" -> 3 datos.
 * Probar con:  ./sol < mision2_calculadora.entrada.txt
 */
#include <stdio.h>

int main(void)
{
    char linea[100];
    double a = 0.0, b = 0.0;
    char op = ' ';

    printf("Cuenta (por ejemplo 12.5 * 4): ");
    fgets(linea, sizeof(linea), stdin);
    if (sscanf(linea, "%lf %c %lf", &a, &op, &b) != 3) {
        printf("\nFormato inválido: tiene que ser número, operador, número.\n");
        return 0;
    }

    printf("\n");
    switch (op) {
        case '+': printf("%.2f + %.2f = %.2f\n", a, b, a + b); break;
        case '-': printf("%.2f - %.2f = %.2f\n", a, b, a - b); break;
        case '*':
        case 'x': printf("%.2f * %.2f = %.2f\n", a, b, a * b); break;
        case '/':
            if (b == 0.0) {
                printf("No se puede dividir por cero.\n");
            } else {
                printf("%.2f / %.2f = %.2f\n", a, b, a / b);
            }
            break;
        default:
            printf("Operador desconocido: '%c'\n", op);
            break;
    }
    return 0;
}
```

#### Pruebas

##### División por cero
```entrada
7 / 0
```
```salida
Cuenta (por ejemplo 12.5 * 4):
No se puede dividir por cero.
```

##### Con x
```entrada
3 x 3
```
```salida
Cuenta (por ejemplo 12.5 * 4):
3.00 * 3.00 = 9.00
```

##### Operador desconocido
```entrada
2 ^ 8
```
```salida
Cuenta (por ejemplo 12.5 * 4):
Operador desconocido: '^'
```

##### Datos de menos
```entrada
5 +
```
```salida
Cuenta (por ejemplo 12.5 * 4):
Formato inválido: tiene que ser número, operador, número.
```

### Misión R01-N05-M3 · La tirada contra la dificultad

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé una tirada de d20 (de 1 a 20). Un 1
es pifia y un 20 es crítico; si no, acierta si `tirada + 3 >= 15`.

#### Criterio de aprobación

- Trata aparte el 1 (pifia) y el 20 (crítico).
- Si no, acierta con `tirada + 3 >= 15`.
- Rechaza tiradas fuera de 1 a 20.

#### Entrada de ejemplo

```
12
```

#### Salida esperada

```
Tirada del d20: 
Acierta (12 + 3 >= 15).
```

#### Solución de referencia

```c
/*
 * Mision 3 - La tirada contra la dificultad.
 * 1 = pifia (siempre falla), 20 = critico (siempre acierta);
 * si no, acierta si tirada + bonus >= dificultad.
 * Probar con:  ./sol < mision3_tirada.entrada.txt   (y cambiando el numero)
 */
#include <stdio.h>

int main(void)
{
    char linea[100];
    int dificultad = 15;
    int bonus = 3;
    int t = 0;

    printf("Tirada del d20: ");
    fgets(linea, sizeof(linea), stdin);
    if (sscanf(linea, "%d", &t) != 1 || t < 1 || t > 20) {
        printf("\nUn d20 da de 1 a 20.\n");
        return 0;
    }

    printf("\n");
    if (t == 1) {
        printf("Pifia: falla siempre.\n");
    } else if (t == 20) {
        printf("¡Crítico! Acierta siempre.\n");
    } else if (t + bonus >= dificultad) {
        printf("Acierta (%d + %d >= %d).\n", t, bonus, dificultad);
    } else {
        printf("Falla (%d + %d < %d).\n", t, bonus, dificultad);
    }
    return 0;
}
```

#### Pruebas

##### Pifia
```entrada
1
```
```salida
Tirada del d20:
Pifia: falla siempre.
```

##### Crítico
```entrada
20
```
```salida
Tirada del d20:
¡Crítico! Acierta siempre.
```

##### Falla por poco
```entrada
11
```
```salida
Tirada del d20:
Falla (11 + 3 < 15).
```

##### Fuera de rango
```entrada
21
```
```salida
Tirada del d20:
Un d20 da de 1 a 20.
```

### Encargo R01-N05-E1 · El correo del Gremio

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El correo del Gremio cobra el envío según la zona (1 ciudad: $800; 2 provincia:
$1500; 3 resto: $2500) más $300 por cada kilo después del primero. Las compras
de $50 000 o más tienen envío gratis. Pedí la zona, los kilos y el monto, y
mostrá el costo, rechazando zonas inválidas y paquetes de menos de 1 kilo.

#### Criterio de aprobación

- Calcula el costo por zona más $300 por kilo después del primero.
- Envío gratis desde $50 000.
- Rechaza zonas inválidas y paquetes de menos de 1 kilo.

#### Entrada de ejemplo

```
2
4
32000
```

#### Salida esperada

```
Zona (1-3): Kilos: Monto de la compra: 
Envío: $2400
```

#### Solución de referencia

```c
/*
 * Encargo del Gremio - El costo de envio del correo del Gremio.
 * Zona 1 (ciudad): 800. Zona 2 (provincia): 1500. Zona 3 (resto): 2500.
 * Mas 300 por cada kilo despues del primero. Envio gratis desde 50000 de compra.
 * Probar con:  ./sol < gremio_envio.entrada.txt
 */
#include <stdio.h>

int main(void)
{
    char linea[100];
    int zona = 0, kilos = 0;
    double compra = 0.0;

    printf("Zona (1-3): ");
    fgets(linea, sizeof(linea), stdin);
    sscanf(linea, "%d", &zona);
    printf("Kilos: ");
    fgets(linea, sizeof(linea), stdin);
    sscanf(linea, "%d", &kilos);
    printf("Monto de la compra: ");
    fgets(linea, sizeof(linea), stdin);
    sscanf(linea, "%lf", &compra);
    printf("\n");

    int base;
    switch (zona) {
        case 1: base = 800; break;
        case 2: base = 1500; break;
        case 3: base = 2500; break;
        default:
            printf("Zona inválida.\n");
            return 0;
    }
    if (kilos < 1) {
        printf("El paquete tiene que pesar al menos 1 kilo.\n");
        return 0;
    }

    int costo = base + (kilos - 1) * 300;
    if (compra >= 50000) {
        printf("Envío gratis (costaría $%d).\n", costo);
    } else {
        printf("Envío: $%d\n", costo);
    }
    return 0;
}
```

#### Pruebas

##### Envío gratis
```entrada
1
10
50000
```
```salida
Zona (1-3): Kilos: Monto de la compra:
Envío gratis (costaría $3500).
```

##### Zona inválida
```entrada
4
2
1000
```
```salida
Zona (1-3): Kilos: Monto de la compra:
Zona inválida.
```

##### Menos de un kilo
```entrada
3
0
1000
```
```salida
Zona (1-3): Kilos: Monto de la compra:
El paquete tiene que pesar al menos 1 kilo.
```

##### Resto del país con varios kilos
```entrada
3
3
49999
```
```salida
Zona (1-3): Kilos: Monto de la compra:
Envío: $3100
```

### Prueba del sello

#### ¿En qué orden se evalúan los `else if`? ¿Cuántos se ejecutan como máximo?

De arriba hacia abajo; se ejecuta como máximo uno: el primero que se cumple (o el `else`).

#### ¿Qué pasa en un `switch` si falta un `break`? ¿Cuándo se hace a propósito?

Sigue ejecutando el `case` de abajo (se "cae"). Se hace a propósito cuando varios casos comparten el mismo código, como `case 'x': case '*':`.

#### ¿Por qué `switch` no sirve para preguntar `experiencia < 100`?

Porque `switch` compara contra valores constantes, uno por uno; no evalúa condiciones como `<`.

#### ¿Qué hace `if (sscanf(linea, "%d", &n) != 1)`?

Pregunta si `sscanf` **no** pudo convertir un entero: si no es 1, el dato no es válido.

#### ¿Qué imprime `printf("%s", 7 > 3 ? "sí" : "no");`?

`sí`.

#### ¿Qué pasa con `if (x > 0); printf("positivo");`?

El `;` cierra el `if` con una instrucción vacía: el `printf` se ejecuta siempre.

### Soluciones (docente)

Material original: `01-C/06-Condicionales` (soluciones completas en `soluciones/`, con sus archivos de entrada y salida).

## R01-N06 · Bucles

```meta
tipo: tema
criatura: ogro
padre: R01-N05
precio: 10
temas: prog.bucles, err.validacion
```

### Crónica

Para que el hierro llegue a 900 °C, alguien tiene que soplar el fuelle **mientras** el horno no alcance la temperatura. Kira escribe la orden para el fuelle mecánico y se va a dormir, orgullosa.

A la mañana, la Forja tiene la temperatura de un volcán, el fuelle sigue soplando y Ferrum tiene las cejas chamuscadas. La orden decía «soplá mientras el horno no esté **frío**».

—La mitad de la vida de un herrero es repetir bien la misma cosa —dice {mentor}, con una paciencia que se le está terminando—. La otra mitad es saber **cuándo parar**. —Tizón agrega en la pared: «Fuelles que no paran: 1».

### Objetivos

Repetir código con `for`, `while` y `do-while`; cortar o saltear vueltas con
`break` y `continue`; y armar un menú que **valide** lo que escribe el usuario,
volviendo a preguntar en lugar de terminar.

### Antes de empezar

- Condicionales (06).
- `fgets` + `sscanf` (05).

### Explicación

#### `for`: cuando se sabe cuántas veces
```c
for (int i = 5; i >= 1; i--) {
    printf("%d ", i);
}
/*   inicio;     condición;  paso  */
```
1. El `inicio` se ejecuta una vez.
2. Si la `condición` es verdadera, ejecuta el cuerpo y después el `paso`.
3. Vuelve al punto 2.

La variable declarada en el `for` (`i`) **solo existe dentro del `for`**.

#### `while`: mientras se cumpla
```c
while (temperatura < 900) {
    temperatura += 250;
}
```
La condición se mira **antes** de cada vuelta. Si ya es falsa al empezar, el
cuerpo no se ejecuta nunca. Algo adentro tiene que hacer que deje de cumplirse;
si no, es un **bucle infinito** (se corta con Ctrl+C).

#### `do-while`: al menos una vez
```c
do {
    ...
} while (opcion != 0);      /* ¡lleva punto y coma! */
```
Primero ejecuta y **después** pregunta. Es ideal para menús.

#### `break` y `continue`
- `break`: **sale** del bucle (o del `switch`) en el acto.
- `continue`: **saltea el resto** de esta vuelta y pasa a la siguiente. En un
  `do-while` salta a la condición.
- `for (;;)` es un bucle sin condición (infinito). Se usa cuando la salida está
  en el medio, con `break`.

#### Bucles anidados
Un bucle dentro de otro: el de adentro da **todas** sus vueltas por cada vuelta
del de afuera. Así se recorren tablas (fila y columna).

#### Validar la entrada: volver a preguntar
```c
for (;;) {
    printf("Elegí una opción: ");
    if (fgets(linea, sizeof(linea), stdin) == NULL) {
        opcion = 0;           /* no hay más entrada */
        break;
    }
    char sobra;
    if (sscanf(linea, "%d %c", &opcion, &sobra) == 1) {
        break;                /* un número y NADA más: válido */
    }
    printf("  Tiene que ser un número.\n");
}
```
- El truco de `"%d %c"`: se pide un número **y después** un carácter. Si la
  línea es solo un número, `sscanf` convierte **1** dato (no encuentra el
  carácter). Si sobra algo (`3abc`, `1,80`), convierte **2**, y se rechaza. Así se
  arregla la trampa del 05.
- **`fgets` devuelve `NULL`** cuando ya no hay entrada: se terminó el archivo
  redirigido o el usuario apretó Ctrl+D. Hay que contemplarlo; si no, el
  programa pregunta para siempre. (`NULL` significa "nada"; se ve en el 13.)
- Además de ser un número, a veces tiene que estar en un rango (mayor que 0,
  entre 1 y 50…): eso se chequea en el mismo `if`.

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo (la entrada de ejemplo ya está en la pestaña **Entrada**).
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**; las respuestas se escriben en la consola.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`
  - Con las respuestas en un archivo: `./programa < main.entrada.txt` (Linux) o `programa.exe < main.entrada.txt` (Windows).

### Código de ejemplo

```c
/*
 * 07 - Bucles: for, while, do-while, break, continue, y un menu que
 * VALIDA lo que escribe el usuario.
 *
 *   make run
 *   ./programa < main.entrada.txt
 */
#include <stdio.h>

int main(void)
{
    /* --- for: cuando se sabe cuantas veces --- */
    printf("Cuenta regresiva: ");
    for (int i = 5; i >= 1; i--) {
        printf("%d ", i);
    }
    printf("¡a forjar!\n");

    /* --- while: MIENTRAS se cumpla la condicion --- */
    int temperatura = 20;
    int soplidos = 0;
    while (temperatura < 900) {
        temperatura += 250;              /* cada soplido del fuelle */
        soplidos++;
    }
    printf("El horno llegó a %d °C en %d soplidos.\n", temperatura, soplidos);

    /* --- break y continue --- */
    for (int sala = 1; sala <= 10; sala++) {
        if (sala % 3 == 0) {
            continue;                    /* salas 3, 6, 9: cerradas, a la siguiente */
        }
        if (sala == 8) {
            printf("Sala 8: ¡el jefe! Se corta la exploración.\n");
            break;                       /* sale del for */
        }
        printf("Explora la sala %d\n", sala);
    }

    /* --- Bucles anidados: tabla de golpes (fila = fuerza, columna = martillo) --- */
    for (int fuerza = 1; fuerza <= 3; fuerza++) {
        for (int martillo = 1; martillo <= 4; martillo++) {
            printf("%4d", fuerza * martillo * 5);
        }
        printf("\n");
    }

    /* --- do-while + validacion: el menu de la tienda --- */
    char linea[100];
    int oro = 20;
    int opcion;

    printf("\n=== TIENDA DE FERRUM ===\n");
    printf("1) Clavos (8 oro)   2) Herradura (3 oro)   0) Salir\n");
    do {
        /* Preguntar HASTA que escriba un numero y nada mas */
        for (;;) {                                        /* bucle "infinito": sale con break */
            printf("Elegí una opción: ");
            if (fgets(linea, sizeof(linea), stdin) == NULL) {
                opcion = 0;                               /* no hay mas entrada: salir */
                break;
            }
            char sobra;
            if (sscanf(linea, "%d %c", &opcion, &sobra) == 1) {
                break;                                    /* un numero y NADA mas: valido */
            }
            printf("  Tiene que ser un número.\n");
        }

        int precio;
        if (opcion == 1) {
            precio = 8;
        } else if (opcion == 2) {
            precio = 3;
        } else if (opcion == 0) {
            continue;                                     /* va directo a la condicion del do-while */
        } else {
            printf("  Esa opción no existe.\n");
            continue;
        }

        int cantidad = 0;
        while (cantidad <= 0) {                           /* hasta un entero positivo */
            printf("  ¿Cuántos? ");
            if (fgets(linea, sizeof(linea), stdin) == NULL) {
                break;
            }
            char sobra;
            if (sscanf(linea, "%d %c", &cantidad, &sobra) != 1 || cantidad <= 0) {
                printf("  Tiene que ser un entero mayor que cero.\n");
                cantidad = 0;
            }
        }
        if (cantidad <= 0) {
            break;                                        /* se termino la entrada */
        }

        int total = precio * cantidad;
        if (total > oro) {
            printf("  No te alcanza: cuesta %d y tenés %d.\n", total, oro);
        } else {
            oro -= total;
            printf("  Compraste %d. Te quedan %d de oro.\n", cantidad, oro);
        }
    } while (opcion != 0);

    printf("Saliste de la tienda con %d de oro.\n", oro);
    return 0;
}
```

### Entrada de ejemplo

```
1
dos
2
7
3abc
2
-1
2
0
```

### Salida esperada

```
Cuenta regresiva: 5 4 3 2 1 ¡a forjar!
El horno llegó a 1020 °C en 4 soplidos.
Explora la sala 1
Explora la sala 2
Explora la sala 4
Explora la sala 5
Explora la sala 7
Sala 8: ¡el jefe! Se corta la exploración.
   5  10  15  20
  10  20  30  40
  15  30  45  60

=== TIENDA DE FERRUM ===
1) Clavos (8 oro)   2) Herradura (3 oro)   0) Salir
Elegí una opción:   ¿Cuántos?   Tiene que ser un entero mayor que cero.
  ¿Cuántos?   Compraste 2. Te quedan 4 de oro.
Elegí una opción:   Esa opción no existe.
Elegí una opción:   Tiene que ser un número.
Elegí una opción:   ¿Cuántos?   Tiene que ser un entero mayor que cero.
  ¿Cuántos?   No te alcanza: cuesta 6 y tenés 4.
Elegí una opción: Saliste de la tienda con 4 de oro.
```

### ¿Para qué sirve?

Los bucles son lo que hace útil a una computadora: recorrer todos los productos de un inventario, calcular los intereses mes a mes, reintentar una conexión hasta que responda, pedir un dato hasta que sea válido. El juego que corre a 60 cuadros por segundo es un bucle, y también lo es el servidor que atiende pedidos todo el día.

### Errores habituales

Mensajes reales de `gcc` 13 con `-Wall -Wextra`.

**Ogro: el punto y coma después del `while`.** `while (n > 0);` repite una
instrucción vacía **para siempre**. `gcc` sospecha:
```
c7.c:5:5: warning: this ‘while’ clause does not guard... [-Wmisleading-indentation]
    5 |     while (n > 0);
      |     ^~~~~
```

**Esqueleto: usar la variable del `for` afuera.**
```
c7.c:10:20: error: ‘i’ undeclared (first use in this function)
   10 |     printf("%d\n", i);
      |                    ^
```

**Ogro: el bucle infinito.** Nada adentro cambia la condición (te olvidaste del
`i++`, o no contemplaste el `NULL` de `fgets`).

**Ogro: uno de más o de menos.** `for (int i = 0; i <= 10; i++)` da **11**
vueltas. Revisá siempre el primer y el último valor.

**Ogro: el `continue` que se saltea el avance.** En un `while`, si el `i++` está
después del `continue`, esa vuelta nunca avanza (en un `for` no pasa, porque el
paso se ejecuta igual).

### Micro-misión R01-N06-P1 · Cuarenta martillazos

```meta
lugar: El yunque de la Forja
personajes: Kira, Gheco, Maese Ferrum
carta: for | for (int i = 1; i <= n; i++) { … } · arranque; condición; paso · para repetir una cantidad sabida
recompensa: xp 10, oro 10
```

#### Escena
Una herradura lleva **exactamente** cuarenta martillazos. Ferrum quiere que Kira cuente de diez en diez, en voz alta, para que no se pase.

#### Gheco sugiere
`for (arranque; condición; paso)` repite mientras la condición se cumpla. Con `i += 10` el paso es de diez en diez.

#### Desafío
Completá el `for` para contar de 10 a 40 de diez en diez.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    for (int golpes = ___; golpes ___ 40; golpes ___) {
        printf("%d martillazos\n", golpes);
    }
    printf("herradura lista\n");
    return 0;
}
```

#### Salida esperada
```
10 martillazos
20 martillazos
30 martillazos
40 martillazos
herradura lista
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    for (int golpes = 10; golpes <= 40; golpes += 10) {
        printf("%d martillazos\n", golpes);
    }
    printf("herradura lista\n");
    return 0;
}
```

#### Al superarla
Cuarenta, ni uno más. Ferrum golpea el yunque dos veces. Kira no entiende si es un aplauso o un tic.

#### Imagen
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) martilla una herradura al rojo sobre un yunque.
- Maese Ferrum (herrero enorme, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) cuenta con los dedos.
- Números luminosos 10, 20, 30, 40 flotan sobre el yunque.

### Micro-misión R01-N06-P2 · El fuelle que no para

```meta
lugar: El horno de la Forja
personajes: Kira, Gheco, Maese Ferrum, Tizón
criatura: ogro
carta: while | while (condición) { … } · repite mientras se cumpla · algo adentro tiene que acercarlo al final
recompensa: xp 10, oro 10
```

#### Escena
El fuelle mecánico sopló toda la noche: la orden decía «soplá mientras el horno **no esté frío**». A la mañana, la Forja es un volcán y Ferrum tiene las cejas chamuscadas.
En la pared, Tizón agrega: «Fuelles que no paran: 1».

#### Gheco sugiere
`while (condición)` repite **mientras** la condición se cumpla. Tiene que decir cuándo **seguir**: mientras el horno no llegue a la temperatura.

#### Desafío
Corregí la condición: soplar mientras el horno esté por debajo de 900 grados.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int grados = 600;
    int soplidos = 0;
    while (grados > 2000) {
        grados += 75;
        soplidos++;
    }
    printf("%d soplidos: horno a %d grados\n", soplidos, grados);
    return 0;
}
```

#### Salida esperada
```
4 soplidos: horno a 900 grados
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int grados = 600;
    int soplidos = 0;
    while (grados < 900) {
        grados += 75;
        soplidos++;
    }
    printf("%d soplidos: horno a %d grados\n", soplidos, grados);
    return 0;
}
```

#### Al superarla
Cuatro soplidos y el horno queda justo en 900. Ferrum se mira las cejas en el reflejo de un escudo, suspira, y no dice nada.

#### Imagen
- Un fuelle mecánico de cobre soplando junto a un horno enorme.
- Maese Ferrum (herrero enorme, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) con las cejas chamuscadas.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) escribe en la pared con tiza.

### Micro-misión R01-N06-P3 · Preguntar hasta que conteste bien

```meta
lugar: La ventanilla de la Forja
personajes: Kira, Gheco, Chispa
carta: do-while | do { … } while (condición); · se ejecuta al menos una vez · ideal para validar lo que se pide
recompensa: xp 10, oro 10
```

#### Escena
Chispa tiene que elegir una cantidad de 1 a 10 herraduras. Contesta 0, después 15, después 4. La ventanilla tiene que seguir preguntando hasta que el número tenga sentido.

#### Gheco sugiere
`do { … } while (condición);` ejecuta el bloque **primero** y pregunta después: sirve para pedir un dato hasta que sea válido. Termina con `;`.

#### Desafío
Completá la condición para repetir mientras la cantidad no esté entre 1 y 10.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int cantidad;
    int intentos = 0;
    do {
        scanf("%d", &cantidad);
        intentos++;
    } while (___);
    printf("Chispa pide %d herraduras (al intento %d)\n", cantidad, intentos);
    return 0;
}
```

#### Entrada
```
0
15
4
```

#### Salida esperada
```
Chispa pide 4 herraduras (al intento 3)
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int cantidad;
    int intentos = 0;
    do {
        scanf("%d", &cantidad);
        intentos++;
    } while (cantidad < 1 || cantidad > 10);
    printf("Chispa pide %d herraduras (al intento %d)\n", cantidad, intentos);
    return 0;
}
```

#### Al superarla
Cuatro herraduras, al tercer intento. —Precio de amigo —dice Chispa—, porque sos vos. —Tizón revisa la balanza.

#### Imagen
- Una ventanilla con tres fichas: un 0 y un 15 tachados, y un 4 aprobado.
- Chispa (mercader alto y flaco, sombrero de ala corta, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro) sonriendo con el diente de oro.

### Micro-misión R01-N06-P4 · El acumulador del carbón

```meta
lugar: El depósito de la Forja
personajes: Kira, Gheco, Tizón
carta: Acumular y contar | total += valor en cada vuelta · contador++ para saber cuántos · inicializar ANTES del bucle
recompensa: xp 15, oro 15
```

#### Escena
Llegan bolsas de carbón de distinto peso, una por línea, y al final un 0. Tizón quiere el total y el promedio, «con los decimales que correspondan».

#### Gheco sugiere
Un **acumulador** (`total += peso`) y un **contador** (`bolsas++`) se inicializan en 0 antes del bucle. El promedio se calcula al final, con `(double)`.

#### Desafío
Completá el acumulador y el contador.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int peso;
    int total = 0;
    int bolsas = 0;
    scanf("%d", &peso);
    while (peso != 0) {
        ___;
        ___;
        scanf("%d", &peso);
    }
    printf("%d bolsas, %d kg, promedio %.2f kg\n", bolsas, total, (double) total / bolsas);
    return 0;
}
```

#### Entrada
```
12
8
15
5
0
```

#### Salida esperada
```
4 bolsas, 40 kg, promedio 10.00 kg
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int peso;
    int total = 0;
    int bolsas = 0;
    scanf("%d", &peso);
    while (peso != 0) {
        total += peso;
        bolsas++;
        scanf("%d", &peso);
    }
    printf("%d bolsas, %d kg, promedio %.2f kg\n", bolsas, total, (double) total / bolsas);
    return 0;
}
```

#### Al superarla
Cuatro bolsas, cuarenta kilos, diez de promedio. Tizón queda feliz: el promedio dio redondo.

#### Imagen
- Bolsas de carbón de distinto tamaño en fila, con números de peso.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) suma en la libreta con la lengua afuera.

### Misión R01-N06-M1 · El ritmo de la forja

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Del 1 al 30: si el número es múltiplo de 3,
"Martillo"; de 5, "Yunque"; de los dos, "MartilloYunque"; si no, el número.

#### Criterio de aprobación

- Recorre del 1 al 30 con un `for`.
- Pregunta primero por los múltiplos de 3 y 5 a la vez (o arma el texto por partes).
- Muestra "Martillo", "Yunque", "MartilloYunque" o el número.

#### Salida esperada

```
1
2
Martillo
4
Yunque
Martillo
7
8
Martillo
Yunque
11
Martillo
13
14
MartilloYunque
16
17
Martillo
19
Yunque
Martillo
22
23
Martillo
Yunque
26
Martillo
28
29
MartilloYunque
```

#### Solución de referencia

```c
/*
 * Mision 1 - El ritmo de la forja (FizzBuzz).
 * Multiplo de 3 -> "Martillo", de 5 -> "Yunque", de ambos -> "MartilloYunque".
 * El caso "de ambos" va primero.
 */
#include <stdio.h>

int main(void)
{
    for (int n = 1; n <= 30; n++) {
        if (n % 3 == 0 && n % 5 == 0) {
            printf("MartilloYunque\n");
        } else if (n % 3 == 0) {
            printf("Martillo\n");
        } else if (n % 5 == 0) {
            printf("Yunque\n");
        } else {
            printf("%d\n", n);
        }
    }
    return 0;
}
```

### Misión R01-N06-M2 · El cofre del aprendiz

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Kira guarda 50 de oro por semana y Ferrum le suma
un 5 % de lo ahorrado. ¿Cuántas semanas tarda en juntar 1000? Mostrá el
ahorro cada 4 semanas.

#### Criterio de aprobación

- Suma 50 por semana y el 5 % de lo ahorrado.
- Muestra el ahorro cada 4 semanas y cuántas semanas tarda en llegar a 1000.

#### Salida esperada

```
semana  4:  226.28
semana  8:  501.33
semana 12:  835.65
Lo logra en la semana 14, con 1028.93 de oro.
```

#### Solución de referencia

```c
/*
 * Mision 2 - El cofre del aprendiz.
 * Kira guarda 50 de oro por semana y Ferrum le suma un 5 % de lo ahorrado.
 * ¿Cuantas semanas hasta juntar 1000 para un martillo de maestro?
 */
#include <stdio.h>

int main(void)
{
    double ahorro = 0.0;
    int semana = 0;
    while (ahorro < 1000.0) {
        semana++;
        ahorro += 50.0;
        ahorro += ahorro * 0.05;
        if (semana % 4 == 0) {                 /* mostrar solo cada 4 semanas */
            printf("semana %2d: %7.2f\n", semana, ahorro);
        }
    }
    printf("Lo logra en la semana %d, con %.2f de oro.\n", semana, ahorro);
    return 0;
}
```

### Misión R01-N06-M3 · El oráculo

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El oráculo piensa el 37 y Kira tiene 6 intentos: respondé
"más alto" o "más bajo". Lo que no sea un número del 1 al 50 **no cuenta**
como intento. (En el 09 el número va a salir al azar.)

#### Criterio de aprobación

- El número secreto es 37 y hay 6 intentos.
- Responde "más alto" o "más bajo".
- Lo que no sea un número del 1 al 50 no gasta intento.

#### Entrada de ejemplo

```
veinte
25
60
40
3x
36
37
```

#### Salida esperada

```
Intento 1: tiene que ser un número del 1 al 50.
Intento 1: más alto
Intento 2: tiene que ser un número del 1 al 50.
Intento 2: más bajo
Intento 3: tiene que ser un número del 1 al 50.
Intento 3: más alto
Intento 4: ¡Correcto! Era 37. Lo lograste en 4 intentos.
```

#### Solución de referencia

```c
/*
 * Mision 3 - El oraculo de la Forja piensa un numero del 1 al 50 (hoy, el 37)
 * y Kira tiene 6 intentos. Lo que no sea un numero valido no cuenta.
 * Probar con:  ./sol < mision3_oraculo.entrada.txt
 */
#include <stdio.h>

int main(void)
{
    const int SECRETO = 37;              /* en el 09 se elige al azar con rand() */
    char linea[100];
    int intentos = 0;
    int adivino = 0;

    while (intentos < 6 && !adivino) {
        printf("Intento %d: ", intentos + 1);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            break;                       /* no hay mas entrada */
        }
        int n;
        char sobra;
        if (sscanf(linea, "%d %c", &n, &sobra) != 1 || n < 1 || n > 50) {
            printf("tiene que ser un número del 1 al 50.\n");
            continue;                    /* no cuenta como intento */
        }
        intentos++;
        if (n == SECRETO) {
            adivino = 1;
        } else if (n < SECRETO) {
            printf("más alto\n");
        } else {
            printf("más bajo\n");
        }
    }

    if (adivino) {
        printf("¡Correcto! Era %d. Lo lograste en %d intentos.\n", SECRETO, intentos);
    } else {
        printf("No lo adivinaste. Era %d.\n", SECRETO);
    }
    return 0;
}
```

#### Pruebas

##### Acierta al primero
```entrada
37
```
```salida
Intento 1: ¡Correcto! Era 37. Lo lograste en 1 intentos.
```

##### Se acaban los intentos
```entrada
10
20
30
40
45
50
```
```salida
Intento 1: más alto
Intento 2: más alto
Intento 3: más alto
Intento 4: más bajo
Intento 5: más bajo
Intento 6: más bajo
No lo adivinaste. Era 37.
```

##### Todo inválido
```entrada
cero
51
0
```
```salida
Intento 1: tiene que ser un número del 1 al 50.
Intento 1: tiene que ser un número del 1 al 50.
Intento 1: tiene que ser un número del 1 al 50.
Intento 1: No lo adivinaste. Era 37.
```

### Encargo R01-N06-E1 · El vuelto del cajero

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El cajero del mercado tiene que dar el vuelto de $10 000 por una compra de $3270
con la **menor cantidad de billetes** posible (de 1000, 500, 200, 100, 50, 20 y
10). Todavía sin arrays: el billete siguiente se puede calcular con un `switch`.

#### Criterio de aprobación

- Calcula el vuelto de $10 000 por $3270.
- Usa la menor cantidad de billetes, de mayor a menor.
- Pasa al billete siguiente con un `switch` (sin arrays).

#### Salida esperada

```
Vuelto: $6730
  6 x $1000
  1 x $500
  1 x $200
  1 x $20
  1 x $10
```

#### Solución de referencia

```c
/*
 * Encargo del Gremio - Dar el vuelto con la menor cantidad de billetes
 * (1000, 500, 200, 100, 50, 20 y 10). Sin arrays todavia: el billete
 * siguiente se calcula con un switch.
 */
#include <stdio.h>

int main(void)
{
    int precio = 3270;
    int pago = 10000;
    int vuelto = pago - precio;
    printf("Vuelto: $%d\n", vuelto);

    int billete = 1000;
    while (billete > 0) {
        int cantidad = vuelto / billete;
        if (cantidad > 0) {
            printf("  %d x $%d\n", cantidad, billete);
            vuelto %= billete;
        }
        switch (billete) {
            case 1000: billete = 500; break;
            case 500:  billete = 200; break;
            case 200:  billete = 100; break;
            case 100:  billete = 50;  break;
            case 50:   billete = 20;  break;
            case 20:   billete = 10;  break;
            default:   billete = 0;   break;    /* despues del de 10, no hay mas */
        }
    }
    if (vuelto > 0) {
        printf("  (quedan $%d en monedas)\n", vuelto);
    }
    return 0;
}
```

### Prueba del sello

#### ¿Cuántas veces se ejecuta `for (int i = 5; i < 20; i += 5)`? ¿Con qué valores?

Tres veces, con 5, 10 y 15.

#### ¿Qué diferencia hay entre `while` y `do-while`?

`while` pregunta antes de cada vuelta (puede no ejecutarse nunca); `do-while` pregunta después (se ejecuta al menos una vez).

#### ¿Qué diferencia hay entre `break` y `continue`?

`break` sale del bucle; `continue` saltea el resto de esta vuelta y pasa a la siguiente.

#### ¿Por qué `sscanf(linea, "%d %c", &n, &c) == 1` rechaza `3abc`?

Porque con `3abc` el `%c` también convierte (la `a`) y `sscanf` devuelve 2, no 1: sobra texto después del número.

#### ¿Qué devuelve `fgets` cuando no hay más entrada? ¿Qué pasa si no lo chequeás?

`NULL`. Si no lo chequeás, el bucle sigue para siempre usando la última línea (o datos sin cambiar).

#### ¿Cuántas veces se ejecuta el cuerpo de dos `for` anidados de 3 y 4 vueltas?

12 veces (3 × 4).

### Soluciones (docente)

Material original: `01-C/07-Bucles` (soluciones completas en `soluciones/`, con sus archivos de entrada y salida).

## R01-N07 · Funciones

```meta
tipo: tema
criatura: esqueleto
padre: R01-N06
precio: 10
temas: prog.funciones, prog.alcance, prog.recursion
```

### Crónica

En la Forja, cada herrero tiene su martillo y no se lo presta a nadie: el martillo de afilar, el de templar, el de calcular el daño. Si alguien necesita afilar, le pide a la que afila; no se pone a afilar él. Kira aprende a la fuerza: agarra el martillo de Hulda y le tuerce el mango.

{mentor} le muestra el libro de la Forja, donde cada técnica tiene su página con nombre, y una página rara que se remite **a sí misma**: «para contar hacia atrás desde 3, decí 3 y contá hacia atrás desde 2…».

Ordenando el depósito, entre los pedidos viejos, Kira encuentra uno distinto: un **pedido de plomo**, una cantidad enorme, pagado por adelantado. En lugar de firma, tiene dibujado **un vitral**. Igual al que estaba junto a ella cuando despertó.

### Objetivos

Partir un programa en **funciones** con nombre, parámetros y valor de retorno.
Entender el **paso por valor**, el **alcance** de las variables (local, global y
`static`) y la **recursión**.

### Antes de empezar

- Condicionales y bucles (06 y 07).

### Explicación

#### Para qué sirven
Una función es un bloque de código **con nombre** que se puede usar muchas
veces. Sirve para:
- **no repetir** código: una regla se escribe una vez;
- **dividir** un problema grande en pasos chicos con nombres que explican qué
  hacen (`main` queda como una receta);
- **probar** cada parte por separado (27).

Regla práctica: si un bloque se puede describir con un verbo ("calcular el
daño", "curar"), es candidato a función.

#### Anatomía
```c
int calcular_danio(int ataque, int defensa)    /* tipo que devuelve, nombre, parámetros */
{
    int danio = ataque - defensa;
    return danio;                               /* devuelve el valor y TERMINA */
}
```
- Se **llama** con los argumentos en el mismo orden:
  `int d = calcular_danio(20, 6);`.
- **`void`** como tipo: no devuelve nada. `(void)` en los parámetros: no recibe
  nada (`void saludar(void)`).
- **`return`** devuelve el valor y corta la función en ese momento. Una función
  que no es `void` tiene que devolver algo **por todos los caminos**.
- **`bool`** (con `<stdbool.h>`) es el tipo natural para las funciones que
  responden sí o no (`es_critico`).
- `const char *nombre` es un **texto** que la función recibe y no modifica.
  Por qué se escribe así se entiende en el 11 (strings) y el 13 (punteros).

#### Prototipos
C lee el archivo **de arriba hacia abajo**. Para usar una función **antes** de
definirla, hay que avisar que existe con un **prototipo**: la primera línea,
terminada en `;`.
```c
int calcular_danio(int ataque, int defensa);    /* prototipo, arriba de main */
```
Es la costumbre: prototipos arriba, `main` y después las definiciones. En el 23
los prototipos pasan a un archivo `.h`.

#### Paso por valor
C pasa **una copia** de cada argumento. Cambiar el parámetro adentro de la
función **no cambia** la variable de quien la llamó:
```c
void intentar_curar(int vida) { vida = vida + 30; }   /* cambia la copia */
...
intentar_curar(vida);           /* vida sigue igual */
vida = curar(vida, 30);         /* lo correcto: devolver el valor nuevo y guardarlo */
```
Para que una función **modifique** una variable de afuera, hay que pasarle su
**dirección** (un puntero): es lo que hace `sscanf` con `&edad`. Se ve en el 13.

#### Alcance: dónde existe cada variable
| Tipo de variable | Dónde se declara | Existe… | La ven… |
|---|---|---|---|
| **local** | dentro de una función o bloque | mientras se ejecuta ese bloque | solo ese bloque |
| **parámetro** | en los paréntesis | mientras se ejecuta la función | solo esa función |
| **global** | fuera de todas las funciones | todo el programa | todo el archivo |
| **`static` local** | dentro de una función, con `static` | todo el programa | solo esa función |

- Dos funciones pueden tener cada una su variable `danio`: son **distintas**.
- Las **globales** las puede cambiar cualquiera, y cuesta seguirles el rastro.
  Usalas poco: mejor pasar parámetros y devolver resultados.
- Una **`static` local** se inicializa **una sola vez** y **recuerda** su valor
  entre llamadas (el contador de `contar_golpe`). Es como una global, pero
  escondida adentro de la función.

#### Los especificadores de almacenamiento
Delante del tipo de una variable puede ir una palabra que cambia **dónde vive** o
**quién la puede tocar**:

| Palabra | Qué hace | Ejemplo |
|---|---|---|
| `auto` | la de siempre de una local (nadie la escribe) | `auto int i;` = `int i;` |
| `static` (local) | recuerda su valor entre llamadas | `static int contador = 0;` |
| `static` (global) | la global solo se ve en **este archivo** | `static int secreto;` |
| `extern` | «está declarada en otro archivo» (R04-N03) | `extern int golpes_totales;` |
| `const` | no se puede cambiar después de inicializarla | `const double PI = 3.14159;` |
| `register` | pide guardarla en un registro del procesador; hoy el compilador lo decide solo | `register int i;` |
| `volatile` | puede cambiar «por afuera» (un sensor, otro hilo): el compilador la lee siempre de nuevo | `volatile int boton;` (Arduino) |

En la práctica se usan `static`, `extern` y `const`; `register` quedó de los
compiladores viejos y `volatile` aparece en la electrónica (la Senda de los
Autómatas).

#### Recursión
Una función **recursiva** se llama a sí misma con un problema **más chico**.
Siempre tiene:
1. un **caso base**, que se resuelve sin volver a llamarse y corta;
2. un **caso recursivo**, que se acerca al caso base.
```c
long long factorial(int n)
{
    if (n <= 1) return 1;              /* caso base */
    return n * factorial(n - 1);       /* 5! = 5 * 4! */
}
```
Cada llamada ocupa lugar en la **pila** (*stack*) hasta que termina. Sin caso
base, la pila se llena y el programa muere (ver el bestiario). `factorial`
devuelve `long long` porque 13! ya no entra en un `int`.

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo.
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`

### Código de ejemplo

```c
/*
 * 08 - Funciones: prototipos, parametros, retorno, paso por valor,
 * alcance, variables static y recursion.
 *
 *   make run
 */
#include <stdio.h>
#include <stdbool.h>

#define VIDA_MAXIMA 100

/* --- Prototipos: le avisan al compilador que estas funciones existen.
       Asi main puede usarlas aunque esten definidas mas abajo. --- */
void saludar(void);
void presentar(const char *nombre, int nivel);
int  calcular_danio(int ataque, int defensa);
bool es_critico(int tirada);
void intentar_curar(int vida);
int  curar(int vida, int cantidad);
int  contar_golpe(void);
void cuenta_regresiva(int n);
long long factorial(int n);

/* Variable GLOBAL: la ve todo el archivo. Usar muy poco. */
int golpes_totales = 0;

int main(void)
{
    saludar();
    presentar("Kira", 7);
    presentar("Tizon", 9);

    int danio = calcular_danio(20, 6);              /* el resultado vuelve y se guarda */
    printf("daño: %d\n", danio);
    printf("daño contra un gólem: %d\n", calcular_danio(20, 50));
    printf("¿14 es crítico? %d   ¿20? %d\n", es_critico(14), es_critico(20));

    /* --- Paso por valor: la funcion recibe una COPIA --- */
    int vida = 40;
    intentar_curar(vida);
    printf("vida después de intentar_curar: %d  (no cambió)\n", vida);
    vida = curar(vida, 30);                         /* lo correcto: devolver el valor nuevo */
    printf("vida después de curar: %d\n", vida);
    vida = curar(vida, 50);
    printf("vida después de curar de nuevo: %d  (tope %d)\n", vida, VIDA_MAXIMA);

    /* --- static local: recuerda su valor entre llamadas --- */
    contar_golpe();
    contar_golpe();
    int n = contar_golpe();
    printf("golpes contados por la función: %d, globales: %d\n", n, golpes_totales);

    /* --- Recursion --- */
    cuenta_regresiva(3);
    printf("5! = %lld   20! = %lld\n", factorial(5), factorial(20));
    return 0;
}

/* --- Definiciones --- */

/* void: no devuelve nada. (void) entre parentesis: no recibe nada. */
void saludar(void)
{
    printf("¡Bienvenidos a la Forja!\n");
}

/* const char *nombre: un texto que la funcion no va a modificar (se ve en el 11) */
void presentar(const char *nombre, int nivel)
{
    printf("%s se presenta (nivel %d)\n", nombre, nivel);
}

int calcular_danio(int ataque, int defensa)
{
    int danio = ataque - defensa;                   /* variable LOCAL: solo existe aca */
    if (danio < 1) {
        return 1;                                   /* return corta la funcion en el acto */
    }
    return danio;
}

bool es_critico(int tirada)
{
    return tirada >= 20;
}

void intentar_curar(int vida)
{
    vida = vida + 30;                               /* cambia la COPIA... */
    printf("  (adentro de intentar_curar, la copia vale %d)\n", vida);
}                                                   /* ...que desaparece al terminar */

int curar(int vida, int cantidad)
{
    int nueva = vida + cantidad;
    return nueva > VIDA_MAXIMA ? VIDA_MAXIMA : nueva;
}

int contar_golpe(void)
{
    static int contador = 0;                        /* se inicializa UNA sola vez */
    contador++;
    golpes_totales++;
    return contador;
}

/* Recursion: la funcion se llama a si misma con un problema mas chico */
void cuenta_regresiva(int n)
{
    if (n == 0) {                                   /* caso base: corta */
        printf("¡ya!\n");
        return;
    }
    printf("%d... ", n);
    cuenta_regresiva(n - 1);                        /* caso recursivo */
}

long long factorial(int n)
{
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}
```

### Salida esperada

```
¡Bienvenidos a la Forja!
Kira se presenta (nivel 7)
Tizon se presenta (nivel 9)
daño: 14
daño contra un gólem: 1
¿14 es crítico? 0   ¿20? 1
  (adentro de intentar_curar, la copia vale 70)
vida después de intentar_curar: 40  (no cambió)
vida después de curar: 70
vida después de curar de nuevo: 100  (tope 100)
golpes contados por la función: 3, globales: 3
3... 2... 1... ¡ya!
5! = 120   20! = 2432902008176640000
```

### ¿Para qué sirve?

Las funciones son la forma de ordenar un programa grande: cada parte hace una cosa, tiene nombre y se puede probar sola. Las bibliotecas que usás (`printf`, `sqrt`) son funciones que escribió otra persona. La recursión aparece en problemas con forma de árbol: recorrer carpetas, resolver laberintos, calcular jugadas en un juego de estrategia.

### Errores habituales

Mensajes reales de `gcc` 13 con `-Wall -Wextra`.

**Esqueleto: usar una función sin prototipo.** Definida abajo de `main` y sin
prototipo arriba:
```
f8.c:4:13: warning: implicit declaration of function ‘doble’ [-Wimplicit-function-declaration]
    4 |     int x = doble(3);
      |             ^~~~~
```

**Esqueleto: prototipo sin definición.** Compila, pero falla el **enlazador**
(el mensaje sale en el idioma del sistema):
```
/usr/bin/ld: /tmp/cc4AZSjD.o: en la función `main':
f9.c:(.text+0x9): referencia a `saludar' sin definir
collect2: error: ld returned 1 exit status
```

**Slime: falta el `return`.**
```
e7.c:13:35: warning: control reaches end of non-void function [-Wreturn-type]
   13 | int doble(int n) { int r = n * 2; }
      |                                   ^
```

**Goblin: argumentos de más o de menos.**
```
e7.c:5:13: error: too many arguments to function ‘doble’
    5 |     int x = doble(1, 2);
      |             ^~~~~
```

**Troll: recursión sin salida.** Sin caso base, la pila se desborda:
```
Violación de segmento  (`core' generado) ./r
```
Con `make asan`, el informe dice qué pasó y dónde:
```
==945777==ERROR: AddressSanitizer: stack-overflow on address 0x7ffd0eb23ffc ...
    #0 0x5a2a2adca1d5 in f r.c:2
    #1 0x5a2a2adca1e4 in f r.c:2
    #2 0x5a2a2adca1e4 in f r.c:2
```
Esas líneas `#0`, `#1`… son el **pergamino de la maldición** de C: la pila de
llamadas, de la más reciente a la más vieja.

**Ogro: creer que la función cambió la variable.** `intentar_curar(vida)` no la
cambia: devolvé el valor y guardalo.

### Micro-misión R01-N07-P1 · El martillo de cada uno

```meta
lugar: El taller de los martillos
personajes: Kira, Gheco, Hulda
carta: Función | tipo nombre(parámetros) { … return valor; } · se llama con sus argumentos · devuelve un resultado
recompensa: xp 10, oro 10
```

#### Escena
Kira agarra el martillo de Hulda para calcular el daño de un golpe… y le tuerce el mango. Hulda le explica, con la voz de capataz, que cada cuenta tiene su martillo: su **función**.

#### Gheco sugiere
Una función se escribe una vez y se usa muchas: `int danio(int ataque, int defensa) { return …; }` y se llama `danio(15, 4)`.

#### Desafío
Completá la función: el daño es el ataque menos la defensa.

#### Código inicial
```c
#include <stdio.h>

int danio(int ataque, int defensa)
{
    ___
}

int main(void)
{
    printf("Kira contra un goblin: %d\n", danio(15, 4));
    printf("Hulda contra un orco: %d\n", danio(22, 9));
    return 0;
}
```

#### Salida esperada
```
Kira contra un goblin: 11
Hulda contra un orco: 13
```

#### Solución
```c
#include <stdio.h>

int danio(int ataque, int defensa)
{
    return ataque - defensa;
}

int main(void)
{
    printf("Kira contra un goblin: %d\n", danio(15, 4));
    printf("Hulda contra un orco: %d\n", danio(22, 9));
    return 0;
}
```

#### Al superarla
Un martillo, dos golpes, dos resultados. Hulda le devuelve a Kira el martillo torcido para que lo enderece. Con su propia función.

#### Imagen
- Una pared con martillos colgados, cada uno con una etiqueta: afilar, templar, daño.
- Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro) sostiene un martillo con el mango torcido.

### Micro-misión R01-N07-P2 · La copia que no cura

```meta
lugar: El taller de los martillos
personajes: Kira, Gheco, Tizón
criatura: ogro
carta: Paso por valor | la función recibe una COPIA · cambiarla no cambia la de afuera · devolvé el valor nuevo y guardalo
recompensa: xp 10, oro 10
```

#### Escena
Tizón se lastimó la mano. Kira llama a la función `curar`… y la vida de Tizón sigue igual. —¿Me curaste o no? —pregunta, mirándose la mano.

#### Gheco sugiere
C pasa una **copia** del argumento: si la función la cambia, la variable de afuera no se entera. La función tiene que **devolver** la vida nueva y quien llama, guardarla.

#### Desafío
Hacé que `curar` devuelva la vida nueva y guardala.

#### Código inicial
```c
#include <stdio.h>

void curar(int vida)
{
    vida = vida + 30;
}

int main(void)
{
    int vida_tizon = 50;
    curar(vida_tizon);
    printf("vida de Tizon: %d\n", vida_tizon);
    return 0;
}
```

#### Salida esperada
```
vida de Tizon: 80
```

#### Solución
```c
#include <stdio.h>

int curar(int vida)
{
    return vida + 30;
}

int main(void)
{
    int vida_tizon = 50;
    vida_tizon = curar(vida_tizon);
    printf("vida de Tizon: %d\n", vida_tizon);
    return 0;
}
```

#### Al superarla
Ochenta. Tizón mueve los dedos, uno por uno, y anota en la libreta: «Curado: sí. Copia: no».

#### Imagen
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) con una mano vendada que brilla de verde.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) lee un pergamino con la función curar.

### Micro-misión R01-N07-P3 · El contador que recuerda

```meta
lugar: El taller de los martillos
personajes: Kira, Gheco, Maese Ferrum
carta: static local | static int n = 0; se inicializa UNA vez · recuerda su valor entre llamadas · solo la ve su función
recompensa: xp 10, oro 10
```

#### Escena
Ferrum quiere saber cuántos espadazos lleva Kira, pero cada vez que llama a `espadazo()` la cuenta vuelve a 1. La función se olvida de todo al terminar.

#### Gheco sugiere
Una variable local nace y muere con cada llamada. Con `static` delante se inicializa **una sola vez** y **recuerda** su valor.

#### Desafío
Hacé que la función recuerde la cuenta.

#### Código inicial
```c
#include <stdio.h>

int espadazo(void)
{
    int cuenta = 0;
    cuenta++;
    return cuenta;
}

int main(void)
{
    espadazo();
    espadazo();
    printf("Espadazos: %d\n", espadazo());
    return 0;
}
```

#### Salida esperada
```
Espadazos: 3
```

#### Solución
```c
#include <stdio.h>

int espadazo(void)
{
    static int cuenta = 0;
    cuenta++;
    return cuenta;
}

int main(void)
{
    espadazo();
    espadazo();
    printf("Espadazos: %d\n", espadazo());
    return 0;
}
```

#### Al superarla
Tres espadazos, contados. Ferrum los suma a la cuenta de la pared, que ya va por treinta y pico. Kira pide que no la sume en voz alta.

#### Imagen
- Una pared con una cuenta de tiza larguísima bajo el título «Espadazos».
- Maese Ferrum (herrero enorme, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) agrega tres palitos más.

### Micro-misión R01-N07-P4 · La página que se llama a sí misma

```meta
lugar: El libro de la Forja
personajes: Kira, Gheco, Tizón
carta: Recursión | una función que se llama con un problema más chico · caso base: cuándo parar · sin caso base, la pila se desborda
recompensa: xp 15, oro 15
```

#### Escena
En el libro de la Forja hay una página rara: «para contar los eslabones de una cadena, contá el primero y después contá los eslabones del resto». Tizón la lee tres veces y se marea.

#### Gheco sugiere
Una función **recursiva** se llama a sí misma con un caso más chico y tiene un **caso base** que corta. `eslabones(0)` es 0; `eslabones(n)` es 1 más `eslabones(n - 1)`.

#### Desafío
Completá el caso base y la llamada recursiva.

#### Código inicial
```c
#include <stdio.h>

int eslabones(int n)
{
    if (n == 0) {
        return ___;
    }
    return 1 + ___;
}

int main(void)
{
    printf("una cadena de 7: %d eslabones\n", eslabones(7));
    return 0;
}
```

#### Salida esperada
```
una cadena de 7: 7 eslabones
```

#### Solución
```c
#include <stdio.h>

int eslabones(int n)
{
    if (n == 0) {
        return 0;
    }
    return 1 + eslabones(n - 1);
}

int main(void)
{
    printf("una cadena de 7: %d eslabones\n", eslabones(7));
    return 0;
}
```

#### Al superarla
Siete. Entre las páginas del libro cae un papel viejo: un **pedido de plomo** enorme, pagado por adelantado, firmado con el dibujo de un vitral. Igual al que estaba junto a Kira cuando despertó.

#### Imagen
- Un libro enorme de la Forja abierto en una página con una cadena dibujada que se repite cada vez más chica.
- Un papel viejo que cae del libro: un pedido de plomo firmado con el dibujo de un vitral.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) lo levanta del piso, seria.

### Misión R01-N07-M1 · Las reglas del combate

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `es_critico(tirada)` (crítico con 15 o
más) y `danio_final(ataque, defensa, critico)` (mínimo 1; el doble si es
crítico). Todavía sin azar, la tirada de cada turno sale de
`tirada_del_turno(turno)`, que devuelve `turno * 7 % 20 + 1`. Simulá hasta 5
ataques de Kira (ataque 15) contra un orco (defensa 4, vida 60).

#### Criterio de aprobación

- Escribe `es_critico` y `danio_final` (mínimo 1, el doble si es crítico).
- La tirada sale de `tirada_del_turno(turno)`.
- Simula hasta 5 ataques contra el orco y muestra la vida que le queda.

#### Salida esperada

```
turno 1: tirada  8 -> daño 11, orco 49
turno 2: tirada 15 CRÍTICO -> daño 22, orco 27
turno 3: tirada  2 -> daño 11, orco 16
turno 4: tirada  9 -> daño 11, orco 5
turno 5: tirada 16 CRÍTICO -> daño 22, orco 0
el orco cayó
```

#### Solución de referencia

```c
/*
 * Mision 1 - Las reglas del combate, cada una en su funcion.
 * Todavia no hay azar (se ve en el 09): la tirada de cada turno sale de una
 * formula fija, asi el combate se puede repetir.
 */
#include <stdio.h>
#include <stdbool.h>

int  tirada_del_turno(int turno);
bool es_critico(int tirada);
int  danio_final(int ataque, int defensa, bool critico);

int main(void)
{
    int vida_orco = 60;
    for (int turno = 1; turno <= 5 && vida_orco > 0; turno++) {
        int tirada = tirada_del_turno(turno);
        bool critico = es_critico(tirada);
        int danio = danio_final(15, 4, critico);
        vida_orco -= danio;
        if (vida_orco < 0) {
            vida_orco = 0;
        }
        printf("turno %d: tirada %2d%s -> daño %2d, orco %d\n",
               turno, tirada, critico ? " CRÍTICO" : "", danio, vida_orco);
    }
    printf("%s\n", vida_orco == 0 ? "el orco cayó" : "el orco sigue en pie");
    return 0;
}

int tirada_del_turno(int turno)
{
    return turno * 7 % 20 + 1;          /* 8, 15, 2, 9, 16... entre 1 y 20 */
}

bool es_critico(int tirada)
{
    return tirada >= 15;
}

int danio_final(int ataque, int defensa, bool critico)
{
    int base = ataque - defensa;
    if (base < 1) {
        base = 1;
    }
    return critico ? base * 2 : base;
}
```

### Misión R01-N07-M2 · La caja de herramientas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `maximo`, `minimo`, `limitar(valor, min,
max)` (usando las dos anteriores) y `es_par`.

#### Criterio de aprobación

- Escribe `maximo`, `minimo`, `limitar` (que usa las dos anteriores) y `es_par`.
- Declara los prototipos antes de `main` (o define las funciones antes).
- Muestra pruebas de cada una.

#### Salida esperada

```
maximo(7, 12) = 12
minimo(7, 12) = 7
limitar(130, 0, 100) = 100
limitar(-5, 0, 100) = 0
limitar(42, 0, 100) = 42
es_par(10) = 1  es_par(7) = 0
```

#### Solución de referencia

```c
/*
 * Mision 2 - La caja de herramientas: funciones chicas que se reutilizan.
 */
#include <stdio.h>
#include <stdbool.h>

int  maximo(int a, int b);
int  minimo(int a, int b);
int  limitar(int valor, int min, int max);
bool es_par(int n);

int main(void)
{
    printf("maximo(7, 12) = %d\n", maximo(7, 12));
    printf("minimo(7, 12) = %d\n", minimo(7, 12));
    printf("limitar(130, 0, 100) = %d\n", limitar(130, 0, 100));
    printf("limitar(-5, 0, 100) = %d\n", limitar(-5, 0, 100));
    printf("limitar(42, 0, 100) = %d\n", limitar(42, 0, 100));
    printf("es_par(10) = %d  es_par(7) = %d\n", es_par(10), es_par(7));
    return 0;
}

int maximo(int a, int b)
{
    return a > b ? a : b;
}

int minimo(int a, int b)
{
    return a < b ? a : b;
}

/* Una funcion puede usar otras: limitar = no bajar de min, no pasar de max */
int limitar(int valor, int min, int max)
{
    return minimo(maximo(valor, min), max);
}

bool es_par(int n)
{
    return n % 2 == 0;
}
```

### Misión R01-N07-M3 · Dos hechizos recursivos

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

`potencia(base, exp)` sin usar `pow`
(`base^0 = 1`) y `suma_digitos(n)`
(`suma_digitos(2026) = 6 + suma_digitos(202)`).

#### Criterio de aprobación

- `potencia` y `suma_digitos` son recursivas, sin `pow` ni bucles.
- Cada una tiene su caso base.
- Muestra, por ejemplo, 2^10 = 1024 y la suma de dígitos de 2026 = 10.

#### Salida esperada

```
2^10 = 1024
3^4 = 81
suma de dígitos de 2026 = 10
suma de dígitos de 7 = 7
```

#### Solución de referencia

```c
/*
 * Mision 3 - Dos hechizos recursivos: cada uno con su CASO BASE.
 */
#include <stdio.h>

long long potencia(int base, int exp);
int suma_digitos(int n);

int main(void)
{
    printf("2^10 = %lld\n", potencia(2, 10));
    printf("3^4 = %lld\n", potencia(3, 4));
    printf("suma de dígitos de 2026 = %d\n", suma_digitos(2026));
    printf("suma de dígitos de 7 = %d\n", suma_digitos(7));
    return 0;
}

/* base^exp = base * base^(exp-1), y base^0 = 1 */
long long potencia(int base, int exp)
{
    if (exp == 0) {
        return 1;
    }
    return base * potencia(base, exp - 1);
}

/* suma_digitos(2026) = 6 + suma_digitos(202) */
int suma_digitos(int n)
{
    if (n < 10) {
        return n;
    }
    return n % 10 + suma_digitos(n / 10);
}
```

### Encargo R01-N07-E1 · El médico del Gremio

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El médico del Gremio calcula el **índice de masa corporal**:
`IMC = peso / (altura × altura)`. Escribí `calcular_imc`, una función
`categoria(imc)` que devuelva `"bajo peso"` (< 18,5), `"normal"` (< 25),
`"sobrepeso"` (< 30) u `"obesidad"`, y una función `informe` que muestre una
línea por paciente. Probalo con Ana (52 kg, 1,68 m), Beto (70 kg, 1,75 m) y Caro
(88 kg, 1,70 m).

#### Criterio de aprobación

- Escribe `calcular_imc`, `categoria` e `informe`.
- Muestra una línea por paciente con el IMC y su categoría.

#### Salida esperada

```
Ana   IMC  18.4 -> bajo peso
Beto  IMC  22.9 -> normal
Caro  IMC  30.4 -> obesidad
```

#### Solución de referencia

```c
/*
 * Encargo del Gremio - El medico del Gremio calcula el indice de masa corporal:
 * IMC = peso / (altura * altura). Una funcion calcula, otra clasifica.
 */
#include <stdio.h>

double calcular_imc(double peso_kg, double altura_m);
const char *categoria(double imc);
void informe(const char *nombre, double peso_kg, double altura_m);

int main(void)
{
    informe("Ana", 52.0, 1.68);
    informe("Beto", 70.0, 1.75);
    informe("Caro", 88.0, 1.70);
    return 0;
}

double calcular_imc(double peso_kg, double altura_m)
{
    return peso_kg / (altura_m * altura_m);
}

/* Devuelve un texto fijo segun el rango */
const char *categoria(double imc)
{
    if (imc < 18.5) {
        return "bajo peso";
    } else if (imc < 25.0) {
        return "normal";
    } else if (imc < 30.0) {
        return "sobrepeso";
    }
    return "obesidad";
}

void informe(const char *nombre, double peso_kg, double altura_m)
{
    double imc = calcular_imc(peso_kg, altura_m);
    printf("%-5s IMC %5.1f -> %s\n", nombre, imc, categoria(imc));
}
```

### Prueba del sello

#### ¿Para qué sirve un prototipo? ¿Qué pasa si falta?

Avisa al compilador cómo es la función (nombre, parámetros y retorno) antes de usarla. Sin él, llamarla antes de su definición es un error en C moderno.

#### Si `void f(int x) { x = 99; }`, ¿cuánto vale `a` después de `int a = 1; f(a);`?

`1`: la función recibe una **copia** del valor.

#### ¿Qué diferencia hay entre una variable local, una global y una `static` local?

La local vive solo dentro de su función; la global, en todo el programa; la `static` local es visible solo en su función pero conserva el valor entre llamadas.

#### ¿Qué muestra `contar_golpe()` si se la llama tres veces? ¿Y si se saca el `static`?

1, 2 y 3, porque la `static` recuerda el valor. Sin `static`, muestra 1 las tres veces.

#### ¿Qué dos partes tiene toda función recursiva?

El **caso base** (donde termina) y el **paso recursivo** (que se acerca al caso base).

#### ¿Por qué `factorial` devuelve `long long`?

Porque el factorial crece muy rápido: `13!` ya no entra en un `int`.

### Soluciones (docente)

Material original: `01-C/08-Funciones` (soluciones completas en `soluciones/`, con sus archivos de entrada y salida).

## R01-N08 · El preprocesador y las macros

```meta
tipo: tema
criatura: ogro
padre: R01-N07
precio: 10
temas: herr.preprocesador
usa: prog.funciones
```

### Crónica

En el taller de marcar, cada pieza recibe su sello antes de entrar al horno: el escudo de las Forjas, el peso, el nombre del herrero. Nadie lo graba a mano: hay **sellos de bronce** que se apoyan y listo.

Tizón talla su primer sello, uno que marca el **cubo** de un número: `a*a*a`. Lo prueba con 2 y sale 8. Feliz, lo prueba con `2+1`… y sale 7. Esa tarde, la partida entera de herraduras sale **con forma de banana**.

—El sello no piensa, Tizón —gruñe Ferrum, levantando una herradura torcida—. **Copia**. Si copiás sin paréntesis, copiás el error.

Kira se ríe tan fuerte que tiene que sentarse. En la pared, debajo de la cuenta de espadazos, alguien escribe con tiza: «Herraduras banana: 40».

### Objetivos

Entender qué hace el **preprocesador** antes de compilar, usar `#include` y
`#define` (constantes y macros con parámetros) sin caer en la trampa de los
paréntesis, elegir entre una macro y una función, y compilar partes del
programa solo cuando hace falta (`#if`, `#ifdef`, `#ifndef`, `#error`).

### Antes de empezar

- Funciones (R01-N07).

### Explicación

#### Del fuente al ejecutable
Cuando apretás **Compilar**, pasan tres cosas en orden:

1. el **preprocesador** lee las líneas que empiezan con `#` y **reemplaza texto**:
   pega los `#include`, cambia cada macro por su valor y saca lo que no se
   compila;
2. el **compilador** traduce ese C «limpio» a código de máquina (un archivo objeto);
3. el **enlazador** junta tu objeto con las bibliotecas (`printf` está ahí) y
   arma el ejecutable.

El preprocesador **no sabe C**: solo copia y pega texto. Para ver qué le entrega
al compilador: `gcc -E programa.c` (en Linux y en Windows con MSYS2).

#### `#include`: pegar otro archivo
```c
#include <stdio.h>      /* < >: lo busca en las carpetas del compilador */
#include "forja.h"      /* " ": primero en la carpeta de tu programa */
```
Las directivas van **una por línea**, empiezan con `#` y **no llevan `;`**.

#### `#define`: constantes con nombre
```c
#define TOPE 10
#define NOMBRE_FORJA "Forjas de Hierro"
int temperaturas[TOPE];         /* el preprocesador escribe int temperaturas[10]; */
```
Se escriben en **MAYÚSCULAS** por costumbre, para distinguirlas de las
variables. Si se cambia `TOPE`, cambia en todo el programa. La otra forma es
`const int tope = 10;`: tiene tipo y el depurador la ve; `#define` sirve
también para el tamaño de un array en cualquier compilador.

#### Macros con parámetros (y la trampa de los paréntesis)
```c
#define CUBO_MAL(a)  a*a*a
#define CUBO(a)      ((a) * (a) * (a))
```
`CUBO_MAL(2+1)` se copia como `2+1*2+1*2+1`, que vale **7**, no 27. La regla:
**un paréntesis alrededor de cada parámetro y otro alrededor de todo**.
`CUBO(2+1)` se copia como `((2+1) * (2+1) * (2+1))` = 27.

Otra trampa: la macro **repite** el argumento. `CUBO(i++)` incrementa `i` tres
veces. Con macros, pasá siempre valores simples.

Sin espacio entre el nombre y el paréntesis: `#define DOBLE (x) ...` define una
constante `DOBLE` que vale `(x) ...`, y no una macro.

#### ¿Macro o función?
| | Macro | Función |
|---|---|---|
| Qué es | texto que se copia | código que se llama |
| Tipos | no los revisa | los revisa |
| Velocidad | sin costo de llamada | un salto y una vuelta |
| Errores | raros y difíciles de ver | claros |

Una macro sirve para algo **muy corto** que se usa **muchas veces**, como el
`SWAP` del apunte, que intercambia dos variables de cualquier tipo:
```c
#define SWAP(tipo, a, b) do { tipo aux_ = (a); (a) = (b); (b) = aux_; } while (0)
```
El `do { … } while (0)` hace que la macro se comporte como **una sola**
instrucción (anda bien dentro de un `if` sin llaves). Para todo lo demás, una
función. En C moderno, una función `static inline` da la velocidad de la macro
con la seguridad de la función.

`#undef NOMBRE` borra una definición: desde esa línea, `NOMBRE` ya no existe.

#### Compilar solo una parte: `#if`, `#ifdef`, `#ifndef`
```c
#define NIVEL 2

#if NIVEL >= 2
    printf("modo forja\n");          /* esto se compila */
#elif NIVEL == 1
    printf("modo práctica\n");       /* esto no llega al compilador */
#else
    printf("modo aprendiz\n");
#endif

#ifdef DEPURAR                        /* = #if defined(DEPURAR) */
    printf("detalle para depurar\n");
#endif
```
- `#ifdef X` pregunta si `X` está definido; `#ifndef X`, si **no** lo está.
- Todo `#if` termina con su `#endif`.
- `#error mensaje` corta la compilación con ese mensaje: sirve para avisar que
  falta algo (`#ifndef NIVEL` → `#error Falta definir NIVEL`).
- Las **guardas** de los archivos `.h` (`#ifndef FORJA_H` … `#endif`) usan esto
  mismo; se ven en R04-N03.

Una macro se puede definir **al compilar**, sin tocar el código: `-DDEPURAR` o
`-DNIVEL=1`.
- En la terminal (Linux, o Windows con MSYS2): `gcc -DDEPURAR programa.c -o programa`.
- En **ZinjaI** y en **Code::Blocks**, en las opciones de compilación del proyecto
  hay un lugar para los *defines* (`DEPURAR`, `NIVEL=1`).
- En **VS Code**, se agrega `-DDEPURAR` a los argumentos de `gcc` en `tasks.json`.

#### Macros que ya vienen
`__LINE__` es el número de línea y `__FILE__`, el nombre del archivo: sirven para
mensajes de depuración. `__func__` (que no es una macro, pero se usa igual) es el
nombre de la función en la que estás.

#### Cómo compilarlo y ejecutarlo
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**
  (compilar y ejecutar).
- **VS Code**: en Windows, con el `gcc` de MSYS2; en Linux, con el del sistema.
  Desde la terminal integrada:
  - Linux: `gcc -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -Wall -Wextra main.c -o programa.exe` y `programa.exe`
- Para ver lo que hace el preprocesador: `gcc -E main.c | tail -40`
  (en Windows con MSYS2, igual).

### Código de ejemplo

```c
/*
 * R01-N08 - El preprocesador: constantes, macros con parametros (con y sin
 * parentesis), macro contra funcion, #undef y compilacion condicional.
 */
#include <stdio.h>

#define TOPE 5
#define NOMBRE_FORJA "Forjas de Hierro"

#define CUBO_MAL(a)  a*a*a                 /* sin parentesis: peligro */
#define CUBO(a)      ((a) * (a) * (a))     /* bien: cada parametro y todo */
#define MAYOR(a, b)  ((a) > (b) ? (a) : (b))
#define SWAP(tipo, a, b) do { tipo aux_ = (a); (a) = (b); (b) = aux_; } while (0)

#define NIVEL 2                            /* probá cambiarlo por 1 o 0 */

int cubo_funcion(int a)
{
    return a * a * a;
}

int main(void)
{
    int pesos[TOPE] = { 12, 7, 30, 18, 9 };
    printf("Bienvenidos a las %s (%d piezas)\n", NOMBRE_FORJA, TOPE);

    printf("CUBO_MAL(2+1) = %d   (se copio como 2+1*2+1*2+1)\n", CUBO_MAL(2+1));
    printf("CUBO(2+1)     = %d\n", CUBO(2+1));
    printf("cubo_funcion(2+1) = %d\n", cubo_funcion(2+1));

    int mayor = pesos[0];
    for (int i = 1; i < TOPE; i++) {
        mayor = MAYOR(mayor, pesos[i]);
    }
    printf("la pieza mas pesada: %d\n", mayor);

    int martillos = 3, yunques = 8;
    SWAP(int, martillos, yunques);
    printf("despues del SWAP: martillos %d, yunques %d\n", martillos, yunques);

    double frio = 20.5, caliente = 900.0;
    SWAP(double, frio, caliente);
    printf("tambien con double: %.1f y %.1f\n", frio, caliente);

#if NIVEL >= 2
    printf("modo forja: el horno al maximo\n");
#elif NIVEL == 1
    printf("modo practica: el horno a la mitad\n");
#else
    printf("modo aprendiz: el horno apagado\n");
#endif

#ifdef DEPURAR
    printf("[depurar] linea %d\n", __LINE__);
#endif

#undef TOPE
    /* desde aca, TOPE ya no existe: usarlo daria error */
    printf("fin del turno en la funcion %s\n", __func__);
    return 0;
}
```

### Salida esperada

```
Bienvenidos a las Forjas de Hierro (5 piezas)
CUBO_MAL(2+1) = 7   (se copio como 2+1*2+1*2+1)
CUBO(2+1)     = 27
cubo_funcion(2+1) = 27
la pieza mas pesada: 30
despues del SWAP: martillos 8, yunques 3
tambien con double: 900.0 y 20.5
modo forja: el horno al maximo
fin del turno en la funcion main
```

### ¿Para qué sirve?

Todo programa de C usa el preprocesador: cada `#include` es una directiva. Las constantes con `#define` son la forma clásica de los tamaños de los arrays y los valores fijos. La compilación condicional deja **un solo código** que se compila distinto en Linux y en Windows (`#ifdef _WIN32`), con o sin mensajes de depuración, o para una placa distinta en Arduino. Y las guardas (`#ifndef ... #endif`) están en cada archivo `.h` que vas a escribir.

### Errores habituales

Mensajes reales de `gcc` 13 con `-Wall -Wextra`.

**Ogro: la macro sin paréntesis.** Compila sin un solo aviso y da otro
resultado: `CUBO_MAL(2+1)` vale 7. Mirá lo que hace el preprocesador con
`gcc -E`.

**Slime: el `;` al final de un `#define`.** `#define TOPE 10;` copia también el
punto y coma:
```
e1.c:2:16: error: expected ‘]’ before ‘;’ token
    2 | #define TOPE 10;
      |                ^
e1.c:5:11: note: in expansion of macro ‘TOPE’
    5 |     int v[TOPE];
      |           ^~~~
```

**Esqueleto: el espacio antes del paréntesis.** `#define DOBLE (x) ((x) + (x))`
define una constante, no una macro, y aparece una `x` que no existe:
```
e4.c:2:16: error: ‘x’ undeclared (first use in this function)
    2 | #define DOBLE (x) ((x) + (x))
      |                ^
```

**Slime: un `#ifdef` sin su `#endif`.**
```
e2.c:3: error: unterminated #ifdef
    3 | #ifdef MODO_FORJA
      |
```

**El `#error` que pusiste vos.** No es un bug: es el aviso que escribiste para
cuando falta algo:
```
e3.c:3:2: error: #error Falta definir NIVEL: compila con -DNIVEL=1
```

**Ogro: el argumento con `++`.** `MAYOR(i++, j)` puede incrementar `i` dos
veces. Con macros, nada de `++` ni llamadas a funciones en los argumentos.

### Micro-misión R01-N08-P1 · El sello del tamaño

```meta
lugar: El taller de marcar
personajes: Kira, Gheco, Tizón
carta: #define | #define NOMBRE valor · el preprocesador lo reemplaza antes de compilar · en MAYUSCULAS y sin ;
recompensa: xp 10, oro 10
```

#### Escena
En el taller de marcar, cada caja dice cuántas piezas lleva. Tizón escribió el 12 en cinco lugares distintos de la receta, y ahora las cajas son de 10. Le toca buscar cada 12. Hay un sello mejor.

#### Gheco sugiere
`#define PIEZAS_POR_CAJA 10` define una constante: antes de compilar, el preprocesador cambia cada `PIEZAS_POR_CAJA` por `10`. Va sin `;`.

#### Desafío
Definí la constante para que todo el programa use 10.

#### Código inicial
```c
#include <stdio.h>

___

int main(void)
{
    int piezas = 47;
    printf("cajas llenas: %d\n", piezas / PIEZAS_POR_CAJA);
    printf("sueltas: %d\n", piezas % PIEZAS_POR_CAJA);
    return 0;
}
```

#### Salida esperada
```
cajas llenas: 4
sueltas: 7
```

#### Solución
```c
#include <stdio.h>

#define PIEZAS_POR_CAJA 10

int main(void)
{
    int piezas = 47;
    printf("cajas llenas: %d\n", piezas / PIEZAS_POR_CAJA);
    printf("sueltas: %d\n", piezas % PIEZAS_POR_CAJA);
    return 0;
}
```

#### Al superarla
Un solo lugar para cambiar el tamaño. Tizón tacha en la libreta «buscar cada 12» y escribe «nunca más».

#### Imagen
- Un sello de bronce que estampa «10» sobre muchas cajas a la vez.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) tacha una lista larguísima.

### Micro-misión R01-N08-P2 · La herradura banana

```meta
lugar: El taller de marcar
personajes: Kira, Gheco, Tizón, Maese Ferrum
criatura: ogro
carta: Macro con parámetros | #define CUBO(a) ((a) * (a) * (a)) · un paréntesis por parámetro y otro por todo · la macro copia texto, no piensa
recompensa: xp 10, oro 10
```

#### Escena
Tizón talló un sello que marca el **cubo** de un número: `a*a*a`. Con 2 da 8. Con `2+1`… da 7. Toda la partida sale **con forma de banana**.
—El sello no piensa —gruñe Ferrum—. **Copia**.

#### Gheco sugiere
`CUBO(2+1)` con `a*a*a` se copia como `2+1*2+1*2+1`, que es 7. Con paréntesis en cada `a` y en todo, se copia como `((2+1) * (2+1) * (2+1))`.

#### Desafío
Arreglá la macro para que `CUBO(2+1)` dé 27.

#### Código inicial
```c
#include <stdio.h>

#define CUBO(a) a*a*a

int main(void)
{
    printf("CUBO(2+1) = %d\n", CUBO(2+1));
    return 0;
}
```

#### Salida esperada
```
CUBO(2+1) = 27
```

#### Solución
```c
#include <stdio.h>

#define CUBO(a) ((a) * (a) * (a))

int main(void)
{
    printf("CUBO(2+1) = %d\n", CUBO(2+1));
    return 0;
}
```

#### Al superarla
Veintisiete, y ni una banana. En la pared, debajo de la cuenta de espadazos, alguien escribe: «Herraduras banana: 40». Tizón no quiere hablar del tema.

#### Imagen
- Una pila de herraduras torcidas con forma de banana.
- Maese Ferrum (herrero enorme, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) sostiene una con dos dedos, mirando a Tizón.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) llorando de risa.

### Micro-misión R01-N08-P3 · Cambiar sin una auxiliar a la vista

```meta
lugar: El taller de marcar
personajes: Kira, Gheco, Chispa
carta: Macro SWAP | intercambia dos variables de cualquier tipo · do { … } while (0) la vuelve una sola instrucción · el tipo va como parámetro
recompensa: xp 10, oro 10
```

#### Escena
Chispa cambió de lugar los precios de dos piezas «sin querer». Hay que volver a intercambiarlos, y después lo mismo con los pesos (que son decimales).

#### Gheco sugiere
`SWAP(tipo, a, b)` usa una variable auxiliar del tipo que le pases: `tipo aux = a; a = b; b = aux;`. Envuelto en `do { … } while (0)` se comporta como una sola instrucción.

#### Desafío
Usá la macro para intercambiar los precios y los pesos.

#### Código inicial
```c
#include <stdio.h>

#define SWAP(tipo, a, b) do { tipo aux_ = (a); (a) = (b); (b) = aux_; } while (0)

int main(void)
{
    int precio_espada = 12, precio_escudo = 45;
    double peso_espada = 6.5, peso_escudo = 2.0;
    ___;
    ___;
    printf("espada: %d lingotes, %.1f kg\n", precio_espada, peso_espada);
    printf("escudo: %d lingotes, %.1f kg\n", precio_escudo, peso_escudo);
    return 0;
}
```

#### Salida esperada
```
espada: 45 lingotes, 2.0 kg
escudo: 12 lingotes, 6.5 kg
```

#### Solución
```c
#include <stdio.h>

#define SWAP(tipo, a, b) do { tipo aux_ = (a); (a) = (b); (b) = aux_; } while (0)

int main(void)
{
    int precio_espada = 12, precio_escudo = 45;
    double peso_espada = 6.5, peso_escudo = 2.0;
    SWAP(int, precio_espada, precio_escudo);
    SWAP(double, peso_espada, peso_escudo);
    printf("espada: %d lingotes, %.1f kg\n", precio_espada, peso_espada);
    printf("escudo: %d lingotes, %.1f kg\n", precio_escudo, peso_escudo);
    return 0;
}
```

#### Al superarla
Todo en su lugar. Chispa jura que fue un error de imprenta. Tizón le muestra que las etiquetas las escribió él, a mano.

#### Imagen
- Dos etiquetas de precio que cambian de lugar en el aire.
- Chispa (mercader alto y flaco, sombrero de ala corta, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro) silba mirando para otro lado.

### Micro-misión R01-N08-P4 · Modo práctica

```meta
lugar: El taller de marcar
personajes: Kira, Gheco, Maese Ferrum
carta: Compilación condicional | #if / #elif / #else / #endif · #ifdef pregunta si algo está definido · lo que no se cumple ni llega al compilador
recompensa: xp 15, oro 15
```

#### Escena
Ferrum quiere una sola receta para el horno, que se compile en «modo práctica» para los aprendices y en «modo forja» para los oficiales. Kira es aprendiz. Por ahora.

#### Gheco sugiere
`#if MODO == 1` … `#else` … `#endif` elige qué líneas se compilan según el valor de `MODO`. Lo que no se cumple el compilador ni lo ve.

#### Desafío
Completá la condición para que con `MODO` en 1 se compile el modo práctica.

#### Código inicial
```c
#include <stdio.h>

#define MODO 1

int main(void)
{
___
    printf("modo practica: horno a 600 grados\n");
#else
    printf("modo forja: horno a 1200 grados\n");
#endif
    return 0;
}
```

#### Salida esperada
```
modo practica: horno a 600 grados
```

#### Solución
```c
#include <stdio.h>

#define MODO 1

int main(void)
{
#if MODO == 1
    printf("modo practica: horno a 600 grados\n");
#else
    printf("modo forja: horno a 1200 grados\n");
#endif
    return 0;
}
```

#### Al superarla
Seiscientos grados. Kira cambia el 1 por un 2 «para ver qué pasa». Ferrum se lo vuelve a cambiar sin decir una palabra.

#### Imagen
- Un horno con una perilla de dos posiciones: práctica y forja.
- Maese Ferrum (herrero enorme, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) gira la perilla de vuelta a práctica.

### Misión R01-N08-M1 · Los sellos de la Forja

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Definí con `#define` la constante `LINGOTES_POR_CAJA` (12) y las macros
`AREA(base, altura)`, `MENOR(a, b)` y `EN_RANGO(x, min, max)` (vale 1 si `x`
está entre `min` y `max`, incluidos), **con todos los paréntesis**. Probalas con
`AREA(3+1, 2)`, `MENOR(7, 4)`, `EN_RANGO(850, 800, 1200)` y
`EN_RANGO(1300, 800, 1200)`, y calculá cuántas cajas completas salen de 100
lingotes y cuántos sobran.

#### Criterio de aprobación

- Usa `#define` para la constante y las tres macros, con un paréntesis en cada parámetro y otro alrededor de todo.
- `AREA(3+1, 2)` da 8 (sin paréntesis daría 5).
- Muestra las cajas completas y los lingotes que sobran.

#### Salida esperada

```
AREA(3+1, 2) = 8
MENOR(7, 4) = 4
EN_RANGO(850, 800, 1200) = 1
EN_RANGO(1300, 800, 1200) = 0
100 lingotes: 8 cajas de 12 y sobran 4
```

#### Solución de referencia

```c
/*
 * Mision 1 - Los sellos de la Forja: una constante y tres macros con todos
 * los parentesis.
 */
#include <stdio.h>

#define LINGOTES_POR_CAJA 12
#define AREA(base, altura)   ((base) * (altura))
#define MENOR(a, b)          ((a) < (b) ? (a) : (b))
#define EN_RANGO(x, min, max) ((x) >= (min) && (x) <= (max))

int main(void)
{
    printf("AREA(3+1, 2) = %d\n", AREA(3+1, 2));
    printf("MENOR(7, 4) = %d\n", MENOR(7, 4));
    printf("EN_RANGO(850, 800, 1200) = %d\n", EN_RANGO(850, 800, 1200));
    printf("EN_RANGO(1300, 800, 1200) = %d\n", EN_RANGO(1300, 800, 1200));

    int lingotes = 100;
    printf("%d lingotes: %d cajas de %d y sobran %d\n", lingotes,
           lingotes / LINGOTES_POR_CAJA, LINGOTES_POR_CAJA, lingotes % LINGOTES_POR_CAJA);
    return 0;
}
```

### Misión R01-N08-M2 · Las herraduras banana

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Tizón dejó estas macros en el taller:
```c
#define CUBO(a)   a*a*a
#define DOBLE(x)  x+x
#define MITAD(x)  x/2
```
Arreglalas y mostrá, para cada una, el resultado con un argumento que
**rompía** la versión vieja: `CUBO(2+1)`, `DOBLE(3)*2` y `MITAD(10+4)`. Al
lado, el valor que daba la versión rota (calculalo a mano: el preprocesador
solo copia texto).

#### Criterio de aprobación

- Las tres macros tienen un paréntesis en cada parámetro y otro alrededor de todo.
- `CUBO(2+1)` da 27, `DOBLE(3)*2` da 12 y `MITAD(10+4)` da 7.
- Muestra también el valor que daba la versión rota (7, 9 y 12).

#### Salida esperada

```
CUBO(2+1)   = 27  (la rota daba 7)
DOBLE(3)*2  = 12  (la rota daba 9)
MITAD(10+4) =  7  (la rota daba 12)
Ninguna herradura banana.
```

#### Solución de referencia

```c
/*
 * Mision 2 - Las herraduras banana: macros sin parentesis, arregladas.
 * La version rota copia el texto tal cual:
 *   CUBO(2+1)   -> 2+1*2+1*2+1 = 7
 *   DOBLE(3)*2  -> 3+3*2       = 9
 *   MITAD(10+4) -> 10+4/2      = 12
 */
#include <stdio.h>

#define CUBO(a)   ((a) * (a) * (a))
#define DOBLE(x)  ((x) + (x))
#define MITAD(x)  ((x) / 2)

int main(void)
{
    printf("CUBO(2+1)   = %2d  (la rota daba 7)\n", CUBO(2+1));
    printf("DOBLE(3)*2  = %2d  (la rota daba 9)\n", DOBLE(3)*2);
    printf("MITAD(10+4) = %2d  (la rota daba 12)\n", MITAD(10+4));
    printf("Ninguna herradura banana.\n");
    return 0;
}
```

### Misión R01-N08-M3 · Modo práctica y modo forja

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí un programa que muestre la temperatura del horno según `NIVEL`:
- si `NIVEL` no está definido, que **no compile** y avise con `#error`;
- con `NIVEL` 0, «horno apagado»; con 1, «horno a 600 grados»; con 2 o más,
  «horno a 1200 grados»;
- si además está definido `DEPURAR`, que muestre también la línea del programa
  con `__LINE__`.

Definí `NIVEL` en 1 arriba del programa y entregalo así. Probá en tu compu los
otros valores y `-DDEPURAR`.

#### Criterio de aprobación

- Usa `#ifndef` con `#error` cuando falta `NIVEL`.
- Usa `#if`, `#elif`, `#else` y `#endif` para los tres niveles.
- Usa `#ifdef DEPURAR` para el detalle de depuración.

#### Salida esperada

```
horno a 600 grados
nivel elegido: 1
```

#### Solución de referencia

```c
/*
 * Mision 3 - Modo practica y modo forja: compilacion condicional.
 * Probar con: gcc -DDEPURAR main.c -o programa
 */
#include <stdio.h>

#define NIVEL 1

#ifndef NIVEL
#error Falta definir NIVEL (0, 1 o 2)
#endif

int main(void)
{
#if NIVEL >= 2
    printf("horno a 1200 grados\n");
#elif NIVEL == 1
    printf("horno a 600 grados\n");
#else
    printf("horno apagado\n");
#endif

#ifdef DEPURAR
    printf("[depurar] esto salio de la linea %d\n", __LINE__);
#endif
    printf("nivel elegido: %d\n", NIVEL);
    return 0;
}
```

### Encargo R01-N08-E1 · La tabla de conversión del mercader

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Chispa vende en las Forjas y en el Valle, y nunca sabe cuánto es cada cosa.
Escribí las macros `C_A_F(c)` (de grados Celsius a Fahrenheit: `c * 9 / 5 + 32`)
y `KG_A_LIBRAS(kg)` (`kg * 2.20462`), con todos los paréntesis, y mostrá una
tabla de 0 a 1200 grados de 300 en 300 y otra con 1, 5 y 12.5 kilos. Usá
`double` y dos decimales.

#### Criterio de aprobación

- Escribe `C_A_F` y `KG_A_LIBRAS` con todos los paréntesis.
- Muestra las dos tablas alineadas, con dos decimales.

#### Salida esperada

```
Celsius  Fahrenheit
      0       32.00
    300      572.00
    600     1112.00
    900     1652.00
   1200     2192.00

Kilos   Libras
  1.0     2.20
  5.0    11.02
 12.5    27.56
```

#### Solución de referencia

```c
/*
 * Encargo - La tabla de conversion del mercader: macros con parametros
 * para convertir temperaturas y pesos.
 */
#include <stdio.h>

#define C_A_F(c)        ((c) * 9.0 / 5.0 + 32.0)
#define KG_A_LIBRAS(kg) ((kg) * 2.20462)

int main(void)
{
    printf("Celsius  Fahrenheit\n");
    for (int c = 0; c <= 1200; c += 300) {
        printf("%7d  %10.2f\n", c, C_A_F(c));
    }
    double kilos[] = { 1.0, 5.0, 12.5 };
    printf("\nKilos   Libras\n");
    for (int i = 0; i < 3; i++) {
        printf("%5.1f  %7.2f\n", kilos[i], KG_A_LIBRAS(kilos[i]));
    }
    return 0;
}
```

### Prueba del sello

#### ¿Qué hace el preprocesador y cuándo lo hace?

Reemplaza texto **antes** de compilar: pega los `#include`, cambia cada macro por su valor y saca lo que no se compila (`#if`). No sabe C: solo copia y pega.

#### ¿Cuánto vale `CUBO(1+1)` si `#define CUBO(a) a*a*a`? ¿Y bien escrita?

`1+1*1+1*1+1` = 4. Bien escrita, `((a) * (a) * (a))`, vale 8.

#### ¿Qué diferencia hay entre `#include <stdio.h>` y `#include "forja.h"`?

Con `< >` el archivo se busca en las carpetas del compilador; con `" "`, primero en la carpeta de tu programa.

#### ¿Por qué `#define TOPE 10;` da un error raro?

Porque el `;` también se copia: `int v[TOPE];` queda `int v[10;];`.

#### ¿Cuándo conviene una macro y cuándo una función?

Una macro, para algo muy corto que se usa muchas veces (y no revisa tipos); una función, para todo lo demás, porque revisa los tipos y sus errores son claros.

#### ¿Para qué sirven `#ifdef DEPURAR` y `-DDEPURAR`?

Para compilar los mensajes de depuración solo cuando se pide: `-DDEPURAR` define `DEPURAR` al compilar, sin tocar el código.

### Soluciones (docente)

Nodo nuevo (2026-10-08), del apunte de Programación I de la UNLaR (Camargo), «El preprocesador del C» (pp. 19–21) y «Velocidad de ejecución de las funciones» (p. 49), en C estándar.

## R01-N09 · Bibliotecas estándar útiles

```meta
tipo: tema
criatura: esqueleto
padre: R01-N08
precio: 10
temas: prog.matematica-azar
```

### Crónica

Kira se pasa una semana entera fabricando su propio martillo para medir textos: cuenta las letras una por una, las compara, las copia. Queda orgullosa. Ferrum abre un armario al fondo de la Forja y le muestra un estante lleno de herramientas que **ya estaban hechas**, con etiquetas: `string.h`, `math.h`, `ctype.h`, `stdlib.h`.

Kira se queda mirando el estante un rato largo. Tizón le da una palmadita en la espalda.

—No hace falta forjar cada martillo —dice {mentor}—. **Mirar el estante también es trabajar**. Eso sí: al Horno hay que avisarle qué cajón vas a usar. Y los dados de hueso de la taberna también están ahí, pero nunca caen dos veces igual en dos Forjas distintas.

### Objetivos

Usar tres cajones de la biblioteca estándar de C: `math.h` (matemática),
`rand`/`srand` de `stdlib.h` (números al azar) y `ctype.h` (preguntas sobre un
carácter). Entender por qué `math.h` necesita `-lm` al compilar.

### Antes de empezar

- Funciones: llamar, pasar argumentos, usar lo que devuelven (08).
- `#include` y los pasos de `gcc`: preprocesar, compilar, enlazar (01).

### Explicación

#### Cada cajón tiene su `#include`
| Cabecera | Trae |
|---|---|
| `<stdio.h>` | `printf`, `fgets`, `sscanf`, `getchar`, `putchar`… |
| `<math.h>` | `pow`, `sqrt`, `fabs`, `floor`, `ceil`, `round`, `hypot`, `sin`, `cos`… |
| `<stdlib.h>` | `rand`, `srand`, `abs`, `exit`… (y `malloc`, en el 17) |
| `<time.h>` | `time` |
| `<ctype.h>` | `isdigit`, `isalpha`, `isupper`, `isspace`, `toupper`, `tolower`… |

El `#include` trae solo los **prototipos**. El código de las funciones ya está
compilado en la biblioteca, y lo agrega el **enlazador**.

#### `math.h` y `-lm`
Las funciones de `math.h` reciben y devuelven **`double`**:

| Función | Qué hace | Ejemplo |
|---|---|---|
| `pow(b, e)` | potencia | `pow(2, 10)` → `1024.0` |
| `sqrt(x)` | raíz cuadrada | `sqrt(81)` → `9.0` |
| `hypot(dx, dy)` | distancia: √(dx² + dy²) | `hypot(3, 4)` → `5.0` |
| `fabs(x)` | valor absoluto de un `double` (`abs` es para `int`, en `stdlib.h`) | `fabs(-2.5)` → `2.5` |
| `floor(x)` / `ceil(x)` | redondeo hacia abajo / hacia arriba | `17.0` / `18.0` |
| `round(x)` | al más cercano (el .5 se aleja del cero) | `round(17.5)` → `18.0` |
| `fmin(a, b)` / `fmax(a, b)` | el menor / el mayor | |

En Linux, el código de `math.h` está en una biblioteca aparte, **libm**, y hay
que pedírsela al enlazador con **`-lm`**, al **final** del comando:
```bash
gcc -Wall -Wextra -std=c11 -o programa main.c -lm
```
(El `Makefile` de cada ejemplo ya lo agrega.)

**π no viene incluido:** `M_PI` es una extensión y con `-std=c11` no existe. Se
puede calcular: `const double PI = acos(-1.0);`.

#### Números al azar: `rand` y `srand`
```c
srand(42);                       /* elige la SEMILLA: el punto de partida */
int d6 = rand() % 6 + 1;         /* rand() % 6 da de 0 a 5; +1 → de 1 a 6 */
int entre = 10 + rand() % 11;    /* de 10 a 20: son 11 valores posibles */
double p = (double) rand() / RAND_MAX;   /* de 0.0 a 1.0 */
```
- `rand()` devuelve un entero de 0 a `RAND_MAX`. No es azar de verdad: es una
  **secuencia calculada** (pseudoaleatoria) que parte de la semilla.
- **Misma semilla, misma secuencia.** Sirve para probar y para repetir una
  partida. La secuencia depende de la biblioteca de C: con la misma semilla,
  **Linux, Windows y el botón Ejecutar de esta página dan números distintos**.
  Las salidas de ejemplo con `rand()` salieron de Linux: si en tu compu dan
  otros números, no está mal; fijate que estén en el rango correcto.
- En el juego real se siembra con la hora: `srand(time(NULL));`,
  **una sola vez**, al principio de `main`. `time(NULL)` devuelve los segundos
  que pasaron desde 1970.
- Sin `srand`, cada ejecución da **siempre** los mismos números.
- Patrón para un rango: `minimo + rand() % (maximo - minimo + 1)`. (Con `%` hay
  un sesgo muy chico hacia los números bajos; para juegos no importa.)

#### `ctype.h`: preguntas sobre un carácter
| Función | Pregunta | Devuelve |
|---|---|---|
| `isalpha(c)` | ¿es una letra? | distinto de 0 si es verdad |
| `isdigit(c)` | ¿es un dígito? | |
| `isupper(c)` / `islower(c)` | ¿mayúscula / minúscula? | |
| `isspace(c)` | ¿es un espacio, tab o salto de línea? | |
| `toupper(c)` / `tolower(c)` | la letra en mayúscula / minúscula | el carácter convertido |

- Devuelven "distinto de 0" (no necesariamente 1) cuando es verdad. Por eso el
  ejemplo escribe `!= 0` para mostrar 1 o 0.
- **Pasales un `unsigned char`**: `isdigit((unsigned char) c)`. Si `char` es con
  signo y la letra tiene tilde, el valor queda negativo y es comportamiento
  indefinido.
- Solo entienden letras **sin** tilde: `isalpha('ñ')` no funciona (UTF-8 usa 2
  bytes para la ñ; se ve en el 11).
- El valor de un dígito: `'7' - '0'` da `7`, porque los dígitos tienen códigos
  seguidos.

#### Leer y escribir de a un carácter
`getchar()` lee **un** carácter de la entrada y `putchar(c)` muestra uno.
`getchar` devuelve un `int` (no un `char`) porque, además de los caracteres,
puede devolver `EOF` ("no hay más entrada"):
```c
int c;
while ((c = getchar()) != EOF && c != '\n') { ... }
```

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo.
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`

### Código de ejemplo

```c
/*
 * 09 - Bibliotecas estandar utiles: math.h, stdlib.h (rand) y ctype.h.
 *
 *   make run          (el Makefile ya agrega -lm para math.h)
 */
#include <stdio.h>
#include <math.h>      /* pow, sqrt, fabs, floor, ceil, round, hypot... */
#include <stdlib.h>    /* rand, srand, abs */
#include <time.h>      /* time: la hora, para sembrar rand */
#include <ctype.h>     /* isdigit, isalpha, toupper... */

int main(void)
{
    /* --- math.h: trabaja con double --- */
    const double PI = acos(-1.0);                  /* M_PI no es parte de C estandar */
    printf("pow(2, 10)   = %.0f\n", pow(2, 10));
    printf("sqrt(81)     = %.1f\n", sqrt(81));
    printf("hypot(3, 4)  = %.1f   (distancia: raíz de 3*3 + 4*4)\n", hypot(3, 4));
    printf("fabs(-2.5)   = %.1f   abs(-7) = %d\n", fabs(-2.5), abs(-7));
    printf("floor(17.6)  = %.1f   ceil(17.2) = %.1f   round(17.5) = %.1f\n",
           floor(17.6), ceil(17.2), round(17.5));
    printf("fmin/fmax    = %.1f / %.1f\n", fmin(3.5, 8.0), fmax(3.5, 8.0));
    printf("PI           = %.6f\n", PI);
    printf("área de un escudo de radio 30 cm = %.1f cm²\n", PI * pow(30, 2));

    /* --- rand: numeros "al azar" (pseudoaleatorios) ---
       srand(semilla) elige el punto de partida de la secuencia. Con una semilla
       FIJA, la secuencia se repite (sirve para probar). En un juego se usa
       srand(time(NULL)): la hora cambia, asi que cambia la secuencia. */
    srand(42);
    int d6a = rand() % 6 + 1;                      /* rand() % 6 da 0..5 -> +1 da 1..6 */
    int d6b = rand() % 6 + 1;
    int d6c = rand() % 6 + 1;
    printf("\n3d6 (semilla 42): %d + %d + %d = %d\n", d6a, d6b, d6c, d6a + d6b + d6c);

    int d20 = rand() % 20 + 1;
    int entre = 10 + rand() % 11;                  /* de 10 a 20: 11 valores posibles */
    double suerte = (double) rand() / RAND_MAX;    /* de 0.0 a 1.0 */
    printf("d20: %d   oro del cofre (10 a 20): %d   suerte: %.3f\n", d20, entre, suerte);

    long ahora = (long) time(NULL);                /* segundos desde 1970: cambia siempre */
    printf("time(NULL) es un número que cambia: %s\n", ahora > 0 ? "sí" : "no");

    /* --- ctype.h: preguntas sobre UN caracter --- */
    char c = 'k';
    printf("\n'%c': letra=%d dígito=%d mayúscula=%d -> toupper = '%c'\n",
           c, isalpha((unsigned char) c) != 0, isdigit((unsigned char) c) != 0,
           isupper((unsigned char) c) != 0, toupper((unsigned char) c));
    char d = '7';
    printf("'%c': dígito=%d, su valor numérico es %d\n",
           d, isdigit((unsigned char) d) != 0, d - '0');
    printf("' ' es espacio: %d\n", isspace((unsigned char) ' ') != 0);
    return 0;
}
```

### Salida esperada

```
pow(2, 10)   = 1024
sqrt(81)     = 9.0
hypot(3, 4)  = 5.0   (distancia: raíz de 3*3 + 4*4)
fabs(-2.5)   = 2.5   abs(-7) = 7
floor(17.6)  = 17.0   ceil(17.2) = 18.0   round(17.5) = 18.0
fmin/fmax    = 3.5 / 8.0
PI           = 3.141593
área de un escudo de radio 30 cm = 2827.4 cm²

3d6 (semilla 42): 1 + 1 + 6 = 8
d20: 2   oro del cofre (10 a 20): 19   suerte: 0.250
time(NULL) es un número que cambia: sí

'k': letra=1 dígito=0 mayúscula=0 -> toupper = 'K'
'7': dígito=1, su valor numérico es 7
' ' es espacio: 1
```

### ¿Para qué sirve?

Nadie programa todo desde cero: `math.h` resuelve cálculos de física y finanzas, `rand` da el azar de los juegos y de las simulaciones, `ctype.h` valida lo que escribe el usuario. Saber qué hay en la biblioteca estándar (y cómo enlazarla, como `-lm`) ahorra horas y evita errores: las funciones de la biblioteca ya están probadas por millones de programas.

### Errores habituales

**Esqueleto: falta el `#include <math.h>`.**
```
e8.c:4:13: warning: implicit declaration of function ‘sqrt’ [-Wimplicit-function-declaration]
e8.c:2:1: note: include ‘<math.h>’ or provide a declaration of ‘sqrt’
```

**Esqueleto: falta `-lm`.** Compila, pero el enlazador no encuentra el código
(mensaje en el idioma del sistema):
```
/usr/bin/ld: /tmp/ccVFtxEg.o: en la función `main':
m.c:(.text+0x4c): referencia a `sqrt' sin definir
collect2: error: ld returned 1 exit status
```
A veces compila igual sin `-lm`: si los números son constantes (`sqrt(16.0)`),
`gcc` calcula el resultado al compilar. Con un valor que viene del usuario, falla.

**Esqueleto: `M_PI` con `-std=c11`.**
```
pi.c:3:32: error: ‘M_PI’ undeclared (first use in this function)
```

**Ogro: el azar que siempre sale igual.** Falta el `srand(time(NULL))`, o se
llama **dentro del bucle**: como la hora cambia una vez por segundo, se repite
el mismo número muchas veces seguidas.

**Ogro: el dado que nunca saca 6.** `rand() % 6` da de 0 a 5: falta el `+ 1`.

**Ogro: `abs` con decimales.** `abs(-2.5)` convierte a entero y da 2. Para
`double`, `fabs`.

### Micro-misión R01-N09-P1 · Cajas que no se parten

```meta
lugar: El estante de herramientas
personajes: Kira, Gheco, Tizón
carta: ceil y floor | ceil redondea hacia arriba · floor hacia abajo · devuelven double · están en math.h
recompensa: xp 10, oro 10
```

#### Escena
Kira se pasó una semana fabricando un redondeador casero. Ferrum abre el armario del fondo: en un estante que dice `math.h` ya estaba todo hecho. Hay que mandar 47 clavos en cajas de 10.

#### Gheco sugiere
Con `#include <math.h>`: `ceil(x)` redondea **hacia arriba** (las cajas que hacen falta) y `floor(x)`, **hacia abajo** (las que se llenan). Las dos devuelven `double`: se muestran con `%.0f`.

#### Desafío
Usá `ceil` y `floor`.

#### Código inicial
```c
#include <stdio.h>
#include <math.h>

int main(void)
{
    double clavos = 47.0;
    printf("cajas necesarias: %.0f\n", ___(clavos / 10));
    printf("cajas llenas: %.0f\n", ___(clavos / 10));
    return 0;
}
```

#### Salida esperada
```
cajas necesarias: 5
cajas llenas: 4
```

#### Solución
```c
#include <stdio.h>
#include <math.h>

int main(void)
{
    double clavos = 47.0;
    printf("cajas necesarias: %.0f\n", ceil(clavos / 10));
    printf("cajas llenas: %.0f\n", floor(clavos / 10));
    return 0;
}
```

#### Al superarla
Cinco cajas, cuatro llenas. Kira guarda su redondeador casero en un cajón, sin hacer comentarios. Tizón le da una palmadita en la espalda.

#### Imagen
- Un armario abierto con estantes etiquetados: math.h, ctype.h, stdlib.h.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) esconde un artefacto casero detrás de la espalda.

### Micro-misión R01-N09-P2 · La cuenta del alambre

```meta
lugar: El estante de herramientas
personajes: Kira, Gheco, Tizón
carta: math.h | sqrt raíz · pow potencia · fabs valor absoluto · en la terminal se compila con -lm
recompensa: xp 10, oro 10
```

#### Escena
Hay que cortar el alambre para la diagonal de un marco de 3 por 4. Tizón lo quiere medir con el calibre; Kira quiere usar el estante.

#### Gheco sugiere
Con `#include <math.h>`: `sqrt(x)` es la raíz cuadrada y `pow(b, e)` es b elevado a e. La diagonal es `sqrt(ancho² + alto²)`.

#### Desafío
Calculá la diagonal con `sqrt` y `pow`.

#### Código inicial
```c
#include <stdio.h>
#include <math.h>

int main(void)
{
    double ancho = 3.0, alto = 4.0;
    double diagonal = ___;
    printf("diagonal: %.1f\n", diagonal);
    return 0;
}
```

#### Salida esperada
```
diagonal: 5.0
```

#### Solución
```c
#include <stdio.h>
#include <math.h>

int main(void)
{
    double ancho = 3.0, alto = 4.0;
    double diagonal = sqrt(pow(ancho, 2) + pow(alto, 2));
    printf("diagonal: %.1f\n", diagonal);
    return 0;
}
```

#### Al superarla
Cinco. Tizón lo mide con el calibre para comprobar: cinco, exacto. Se queda en silencio, muy impresionado.

#### Imagen
- Un marco de hierro de 3 por 4 con un alambre cruzado en diagonal.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) mide la diagonal, boquiabierto.

### Micro-misión R01-N09-P3 · Letras al derecho

```meta
lugar: El estante de herramientas
personajes: Kira, Gheco, Chispa
carta: ctype.h y getchar | getchar lee un carácter · toupper devuelve la mayúscula · isdigit pregunta si es un dígito · putchar lo muestra
recompensa: xp 10, oro 10
```

#### Escena
Chispa escribió el cartel de su puesto en minúsculas «para ahorrar tinta». Kira lo quiere en mayúsculas, y quiere saber cuántos números tiene.

#### Gheco sugiere
`getchar()` lee **un** carácter (devuelve un `int`). Con `#include <ctype.h>`, `toupper(c)` da su mayúscula e `isdigit(c)` dice si es un dígito. `putchar(c)` lo muestra.

#### Desafío
Completá el bucle que lee el cartel de a un carácter hasta el fin de la línea.

#### Código inicial
```c
#include <stdio.h>
#include <ctype.h>

int main(void)
{
    int c;
    int digitos = 0;
    while ((c = getchar()) != '\n' && c != EOF) {
        if (___(c)) {
            digitos++;
        }
        putchar(___(c));
    }
    printf(" (%d numeros)\n", digitos);
    return 0;
}
```

#### Entrada
```
lingotes a 3 por 5
```

#### Salida esperada
```
LINGOTES A 3 POR 5 (2 numeros)
```

#### Solución
```c
#include <stdio.h>
#include <ctype.h>

int main(void)
{
    int c;
    int digitos = 0;
    while ((c = getchar()) != '\n' && c != EOF) {
        if (isdigit(c)) {
            digitos++;
        }
        putchar(toupper(c));
    }
    printf(" (%d numeros)\n", digitos);
    return 0;
}
```

#### Al superarla
LINGOTES A 3 POR 5. Chispa se queja del gasto de tinta. Después ve que vende el doble y se calla.

#### Imagen
- Un cartel de madera de un puesto de mercado con letras grandes en mayúscula.
- Chispa (mercader alto y flaco, sombrero de ala corta, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro) cuenta monedas detrás del puesto.

### Micro-misión R01-N09-P4 · Los dados de Tizón

```meta
lugar: La taberna de la Forja
personajes: Kira, Gheco, Tizón
carta: Pseudoazar a mano | un número semilla y una cuenta que lo cambia · misma semilla, misma secuencia · rand() hace algo parecido
recompensa: xp 15, oro 15
```

#### Escena
Tizón no confía en los dados de hueso de la taberna («nunca caen igual en dos Forjas distintas»). Inventó su propio dado: un número que se transforma con una cuenta cada vez que se tira.

#### Gheco sugiere
Un generador simple: `semilla = (semilla * 17 + 5) % 101` en cada tirada, y el dado es `semilla % 6 + 1` (de 1 a 6). Así sale **siempre** la misma secuencia, en cualquier compu. `rand()` hace algo parecido, pero su cuenta cambia según el sistema.

#### Desafío
Completá la tirada del dado.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int semilla = 7;
    for (int tirada = 1; tirada <= 5; tirada++) {
        semilla = (semilla * 17 + 5) % 101;
        int dado = ___;
        printf("tirada %d: %d\n", tirada, dado);
    }
    return 0;
}
```

#### Salida esperada
```
tirada 1: 6
tirada 2: 4
tirada 3: 6
tirada 4: 1
tirada 5: 6
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int semilla = 7;
    for (int tirada = 1; tirada <= 5; tirada++) {
        semilla = (semilla * 17 + 5) % 101;
        int dado = semilla % 6 + 1;
        printf("tirada %d: %d\n", tirada, dado);
    }
    return 0;
}
```

#### Al superarla
Cinco tiradas que salen igual en cualquier Forja del mundo. Los de la taberna dicen que el dado de Tizón está cargado. Tizón dice que está **medido**.

#### Imagen
- Una mesa de taberna con un dado de bronce tallado a mano.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) anota cada tirada en la libreta; alrededor, aprendices desconfiados.

### Misión R01-N09-M1 · Combate con pociones

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Kira (30 de vida, 2 pociones) contra un orco (40
de vida), con `srand(4)`. Kira pega de 5 a 10 y el orco de 4 a 9 (escribí
una función `tirar(minimo, maximo)`). Si en su turno Kira tiene menos de 10
de vida y le quedan pociones, toma una (+15) en lugar de atacar.

> El azar depende de la biblioteca de C: la salida esperada es la de Linux (glibc). En otro sistema los números pueden cambiar.

#### Criterio de aprobación

- Usa `srand(4)` y una función `tirar(minimo, maximo)`.
- Kira toma poción (+15) si tiene menos de 10 de vida y le quedan.
- Muestra cada turno y quién gana.

#### Salida esperada

```
T1: Kira pega 6 -> orco 34
    el orco pega 9 -> Kira 21
T2: Kira pega 9 -> orco 25
    el orco pega 6 -> Kira 15
T3: Kira pega 6 -> orco 19
    el orco pega 5 -> Kira 10
T4: Kira pega 8 -> orco 11
    el orco pega 5 -> Kira 5
T5: Kira toma una poción -> vida 20 (quedan 1)
    el orco pega 6 -> Kira 14
T6: Kira pega 10 -> orco 1
    el orco pega 6 -> Kira 8
T7: Kira toma una poción -> vida 23 (quedan 0)
    el orco pega 4 -> Kira 19
T8: Kira pega 9 -> orco 0
¡Ganó Kira!
```

#### Solución de referencia

```c
/*
 * Mision 1 - Combate con pociones.
 * Kira (30 de vida, 2 pociones) contra un orco (40). Si en su turno Kira tiene
 * menos de 10 y le quedan pociones, toma una (+15) en vez de atacar.
 * Kira pega de 5 a 10; el orco, de 4 a 9. Semilla fija para poder repetirlo.
 */
#include <stdio.h>
#include <stdlib.h>

int tirar(int minimo, int maximo);

int main(void)
{
    srand(4);
    int vida_kira = 30, pociones = 2, vida_orco = 40, turno = 0;

    while (vida_kira > 0 && vida_orco > 0) {
        turno++;
        if (vida_kira < 10 && pociones > 0) {
            pociones--;
            vida_kira += 15;
            printf("T%d: Kira toma una poción -> vida %d (quedan %d)\n", turno, vida_kira, pociones);
        } else {
            int golpe = tirar(5, 10);
            vida_orco = vida_orco - golpe < 0 ? 0 : vida_orco - golpe;
            printf("T%d: Kira pega %d -> orco %d\n", turno, golpe, vida_orco);
        }
        if (vida_orco > 0) {
            int golpe = tirar(4, 9);
            vida_kira = vida_kira - golpe < 0 ? 0 : vida_kira - golpe;
            printf("    el orco pega %d -> Kira %d\n", golpe, vida_kira);
        }
    }
    printf("%s\n", vida_kira > 0 ? "¡Ganó Kira!" : "Ganó el orco...");
    return 0;
}

/* Un numero al azar entre minimo y maximo, ambos incluidos */
int tirar(int minimo, int maximo)
{
    return minimo + rand() % (maximo - minimo + 1);
}
```

### Misión R01-N09-M2 · El oráculo al azar

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El oráculo del 07, ahora con `rand() % 50 + 1`.
Dejá la semilla fija (`srand(2026)`) para poder probarlo con un archivo de
respuestas y comentá cómo sería con `time(NULL)`.

#### Criterio de aprobación

- Usa `rand() % 50 + 1` con `srand(2026)`.
- Reutiliza las reglas del oráculo del 07.
- Comenta cómo sería con `time(NULL)`.

#### Entrada de ejemplo

```
veinte
25
60
40
37
38
```

#### Salida esperada

```
Intento 1: tiene que ser un número del 1 al 50.
Intento 1: más alto
Intento 2: tiene que ser un número del 1 al 50.
Intento 2: más bajo
Intento 3: más alto
Intento 4: ¡Correcto! Lo lograste en 4 intentos.
```

#### Solución de referencia

```c
/*
 * Mision 2 - El oraculo, ahora con un numero al azar del 1 al 50.
 * Para jugar de verdad: srand(time(NULL)). Aca se deja fija para poder probarlo.
 * Probar con:  ./sol < mision2_oraculo.entrada.txt
 */
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    srand(2026);                              /* jugando: srand(time(NULL)); */
    int secreto = rand() % 50 + 1;
    char linea[100];
    int intentos = 0, adivino = 0;

    while (intentos < 6 && !adivino) {
        printf("Intento %d: ", intentos + 1);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            break;
        }
        int n;
        char sobra;
        if (sscanf(linea, "%d %c", &n, &sobra) != 1 || n < 1 || n > 50) {
            printf("tiene que ser un número del 1 al 50.\n");
            continue;
        }
        intentos++;
        if (n == secreto) {
            adivino = 1;
        } else {
            printf("%s\n", n < secreto ? "más alto" : "más bajo");
        }
    }
    if (adivino) {
        printf("¡Correcto! Lo lograste en %d intentos.\n", intentos);
    } else {
        printf("No lo adivinaste. Era %d.\n", secreto);
    }
    return 0;
}
```

#### Pruebas

##### Se termina la entrada
```entrada
1
```
```salida
Intento 1: más alto
Intento 2: No lo adivinaste. Era 38.
```

##### Siempre lo mismo
```entrada
25
25
25
25
25
25
```
```salida
Intento 1: más alto
Intento 2: más alto
Intento 3: más alto
Intento 4: más alto
Intento 5: más alto
Intento 6: más alto
No lo adivinaste. Era 38.
```

### Misión R01-N09-M3 · El sello de la Forja

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé una línea carácter por carácter con
`getchar`. Mostrá las letras en mayúscula, los dígitos tal cual, los espacios
como `_` y el resto como `?`, y al final cuántos hubo de cada tipo.

#### Criterio de aprobación

- Lee carácter por carácter con `getchar` hasta el Enter o el fin de la entrada.
- Usa `toupper`, `isdigit`, `isspace` de `ctype.h`.
- Muestra al final cuántos hubo de cada tipo.

#### Entrada de ejemplo

```
Kira tiene 3 martillos!
```

#### Salida esperada

```
Escribí una línea: KIRA_TIENE_3_MARTILLOS?
letras 18, dígitos 1, espacios 3, otros 1
```

#### Solución de referencia

```c
/*
 * Mision 3 - El sello de la Forja: clasificar cada letra de una linea
 * con ctype.h. (Todavia sin strings: se recorre letra por letra con getchar.)
 * Probar con:  ./sol < mision3_letras.entrada.txt
 */
#include <stdio.h>
#include <ctype.h>

int main(void)
{
    int letras = 0, digitos = 0, espacios = 0, otros = 0;
    int c;
    printf("Escribí una línea: ");
    while ((c = getchar()) != EOF && c != '\n') {   /* getchar: UN caracter por vez */
        if (isalpha(c)) {
            letras++;
            putchar(toupper(c));                    /* putchar: muestra UN caracter */
        } else if (isdigit(c)) {
            digitos++;
            putchar(c);
        } else if (isspace(c)) {
            espacios++;
            putchar('_');
        } else {
            otros++;
            putchar('?');
        }
    }
    printf("\nletras %d, dígitos %d, espacios %d, otros %d\n", letras, digitos, espacios, otros);
    return 0;
}
```

#### Pruebas

##### Solo dígitos
```entrada
2026 99
```
```salida
Escribí una línea: 2026_99
letras 0, dígitos 6, espacios 1, otros 0
```

##### Mayúsculas y símbolos
```entrada
¡HOLA, Kira!
```
```salida
Escribí una línea: ??HOLA?_KIRA?
letras 8, dígitos 0, espacios 1, otros 4
```

##### Línea vacía
```entrada
```
```salida
Escribí una línea:
letras 0, dígitos 0, espacios 0, otros 0
```

### Encargo R01-N09-E1 · El préstamo del banco

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El banco del Gremio presta $500 000 a una tasa anual del 60 %. La cuota fija
mensual es `cuota = P × i / (1 − (1 + i)^(−n))`, donde `i` es el interés
**mensual** (`tasa / 12 / 100`) y `n` la cantidad de cuotas. Escribí una función
`cuota` y mostrá una tabla con la cuota y el total a pagar en 6, 12 y 24 meses.

#### Criterio de aprobación

- Escribe la función `cuota` con `pow`.
- Muestra cuota y total para 6, 12 y 24 meses.
- Compila con `-lm`.

#### Salida esperada

```
Préstamo de $500000.00
 meses     tasa          cuota          total
     6    60.0%       98508.73      591052.40
    12    60.0%       56412.71      676952.46
    24    60.0%       36235.45      869650.81
```

#### Solución de referencia

```c
/*
 * Encargo del Gremio - La cuota de un prestamo del banco del Gremio.
 * Cuota fija (sistema frances):  cuota = P * i / (1 - (1 + i)^(-n))
 *   P = monto, i = interes MENSUAL (anual / 12 / 100), n = cantidad de cuotas.
 */
#include <stdio.h>
#include <math.h>

double cuota(double monto, double tasa_anual, int meses);

void mostrar_plan(double monto, double tasa_anual, int meses);

int main(void)
{
    double monto = 500000.0;
    printf("Préstamo de $%.2f\n", monto);
    printf("%6s %8s %14s %14s\n", "meses", "tasa", "cuota", "total");
    mostrar_plan(monto, 60.0, 6);
    mostrar_plan(monto, 60.0, 12);
    mostrar_plan(monto, 60.0, 24);
    return 0;
}

void mostrar_plan(double monto, double tasa_anual, int meses)
{
    double c = cuota(monto, tasa_anual, meses);
    printf("%6d %7.1f%% %14.2f %14.2f\n", meses, tasa_anual, c, c * meses);
}

double cuota(double monto, double tasa_anual, int meses)
{
    double i = tasa_anual / 12.0 / 100.0;
    return monto * i / (1.0 - pow(1.0 + i, -meses));
}
```

### Prueba del sello

#### ¿Qué hace `#include <math.h>`? ¿Y `-lm`? ¿Por qué hacen falta los dos?

`#include <math.h>` declara las funciones (el compilador sabe cómo son); `-lm` enlaza la biblioteca que las tiene. Sin el primero no compila bien; sin el segundo, falla al enlazar.

#### ¿Qué rango de valores da `rand() % 20 + 1`? ¿Y `5 + rand() % 6`?

`rand() % 20 + 1` da de 1 a 20; `5 + rand() % 6`, de 5 a 10.

#### ¿Por qué se llama a `srand` una sola vez? ¿Para qué sirve una semilla fija?

Porque `srand` fija el punto de partida de la secuencia: si se llama en cada tirada con la misma semilla, se repiten los números. Una semilla fija sirve para probar: siempre sale lo mismo.

#### ¿Qué diferencia hay entre `round(2.5)`, `floor(2.5)`, `ceil(2.5)` y `(int) 2.5`?

`3`, `2`, `3` y `2`.

#### ¿Cuánto da `'9' - '0'`?

`9`: los dígitos están seguidos en la tabla de caracteres.

#### ¿Por qué `getchar` devuelve `int`?

Porque además de cualquier carácter puede devolver `EOF` (fin de la entrada), que no es un carácter.

### Soluciones (docente)

Material original: `01-C/09-Bibliotecas` (soluciones completas en `soluciones/`, con sus archivos de entrada y salida).

## R01-N10 · Jefe: el Gólem de Escoria

```meta
tipo: jefe
padre: R01-N09
precio: 10
criatura: dragon
insignia: Sello del Gólem
insignia_descripcion: Venciste al Gólem de Escoria: dominás los fundamentos de C.
usa: prog.funciones, err.validacion
```

### Crónica

En el patio, toda la escoria de la Forja se junta y se levanta: el **Gólem de Escoria**, negro, con grietas de lava y puntos y coma incrustados en el pecho. Kira reconoce algunos pedazos: son **suyos**, de la primera semana.

Ella levanta la espada rajada por costumbre. Ferrum le pone la mano en el hombro. En la pared, la cuenta de espadazos dice 41 a 0.

—No lo vas a vencer de un golpe —dice {mentor}—. Lo vas a vencer con todo lo que templaste: tipos, cuentas, decisiones, bucles y funciones, cada cosa en su lugar. Y validando todo lo que te digan. —Tizón le pasa la libreta con las medidas, por si acaso.

### Objetivos

- Resolver un problema completo combinando todo lo de la rama.
- Dividir el programa en funciones chicas, cada una con una sola tarea.
- Validar la entrada para que el programa nunca se corte ni se trabe.

### Antes de empezar

Todos los nodos de *Templar el metal*. Es un **proyecto integrador**: no hay teoría nueva.

### Explicación

#### Cómo se enfrenta a un jefe

Un problema grande asusta; varios problemas chicos, no. Antes de escribir código:

1. **Leé la consigna entera** y anotá qué datos hay y de qué tipo es cada uno (¿entero? ¿`double`? ¿una bandera?).
2. **Partí el problema en funciones**: una para leer un dato válido, otra para calcular, otra para mostrar. Cada una recibe lo que necesita y **devuelve** el resultado.
3. **Armá el bucle principal** al final: pide, decide qué función llamar y muestra.
4. **Compilá seguido** con `-Wall -Wextra` y probá de a poco. Para no tipear cada vez, guardá las respuestas en un archivo y ejecutá `./programa < entrada.txt`.

#### La receta de lectura, una vez más

Casi todos los programas de este jefe leen números. Conviene escribir **una** función y usarla siempre:

```c
bool pedir_entero(const char *pregunta, int minimo, int maximo, int *resultado)
{
    char linea[100];
    for (;;) {
        printf("%s", pregunta);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;                 /* se terminó la entrada */
        }
        int n;
        char sobra;
        if (sscanf(linea, "%d %c", &n, &sobra) == 1 && n >= minimo && n <= maximo) {
            *resultado = n;
            return true;
        }
        printf("\n  Escribí un número del %d al %d.\n", minimo, maximo);
    }
}
```

(El `int *resultado` es un puntero: se ve a fondo en la rama siguiente. Por ahora alcanza con saber que así la función puede dejar el número en tu variable, igual que `sscanf` con `&`.)

### ¿Para qué sirve?

Es el esqueleto de muchísimos programas reales: la caja registradora de un comercio, el menú de un cajero automático, una calculadora de conversiones, el panel de control de una máquina. Leer datos, validarlos, decidir, repetir y mostrar un resultado claro es lo que hace cualquier programa que atiende a una persona.

### Errores habituales

El Gólem combina a todas las criaturas de la rama:

- **Goblin**: usar `%d` para un `double` (o `%f` para leerlo, en lugar de `%lf`).
- **Ogro**: descontar antes de revisar, o sumar el descuento en lugar de restarlo.
- **Ogro**: el `if (armadura & zona == 0)` sin paréntesis: `==` se evalúa antes que `&`.
- **Slime**: el `;` que falta, la llave que no cierra.
- **Esqueleto**: usar una función antes de declararla (sin prototipo).
- **Ogro**: un bucle que no revisa si `fgets` devolvió `NULL` y se queda preguntando para siempre cuando termina la entrada.

### Micro-misión R01-N10-P1 · La escoria se levanta

```meta
lugar: El patio de la Forja
personajes: Kira, Gheco, Maese Ferrum
criatura: dragon
carta: Partir el problema | cada paso en su función · main queda como una receta que se lee
recompensa: xp 15, oro 15
```

#### Escena
En el patio, toda la escoria de la Forja se junta y se levanta: el **Gólem de Escoria**, negro, con grietas de lava y puntos y coma incrustados en el pecho. Algunos pedazos son de la primera semana de Kira.
—No lo vas a vencer de un golpe —dice Ferrum—. Partilo.

#### Gheco sugiere
Cada parte del combate en su función: `vida_restante(vida, golpe)` devuelve la vida que queda (nunca menos de 0).

#### Desafío
Completá la función: si el golpe es mayor que la vida, la vida queda en 0.

#### Código inicial
```c
#include <stdio.h>

int vida_restante(int vida, int golpe)
{
    ___
}

int main(void)
{
    int golem = 50;
    golem = vida_restante(golem, 18);
    printf("el golem resiste: %d\n", golem);
    golem = vida_restante(golem, 40);
    printf("el golem resiste: %d\n", golem);
    return 0;
}
```

#### Salida esperada
```
el golem resiste: 32
el golem resiste: 0
```

#### Solución
```c
#include <stdio.h>

int vida_restante(int vida, int golpe)
{
    if (golpe >= vida) {
        return 0;
    }
    return vida - golpe;
}

int main(void)
{
    int golem = 50;
    golem = vida_restante(golem, 18);
    printf("el golem resiste: %d\n", golem);
    golem = vida_restante(golem, 40);
    printf("el golem resiste: %d\n", golem);
    return 0;
}
```

#### Al superarla
El gólem tambalea, pero se vuelve a juntar. En la pared, la cuenta de espadazos sigue en 41 a 0. Kira, por primera vez, no levanta la espada.

#### Imagen
- El Gólem de Escoria: un gigante de escoria negra y roca fundida con grietas de lava naranja y puntos y coma incrustados en el pecho.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) frente a él, con la espada rajada en la vaina.
- Maese Ferrum (herrero enorme, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) a un costado, con los brazos cruzados.

### Micro-misión R01-N10-P2 · Validar lo que dice el gólem

```meta
lugar: El patio de la Forja
personajes: Kira, Gheco, Tizón
criatura: goblin
carta: Validar en un bucle | leer con fgets · sscanf devuelve 1 si era un número · repetir hasta que el dato sirva
recompensa: xp 15, oro 15
```

#### Escena
El gólem grita números falsos para confundir: «¡mil!», «¡nada!», «¡-5!». Tizón le pasa a Kira una regla: solo valen los golpes entre 1 y 99.

#### Gheco sugiere
Se lee la línea con `fgets` y se interpreta con `sscanf`. Si `sscanf` no devuelve 1 o el número está fuera de rango, se ignora y se lee la siguiente.

#### Desafío
Completá la condición para aceptar solo números entre 1 y 99.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    char linea[50];
    int golpe = 0;
    int ignorados = 0;
    while (fgets(linea, sizeof linea, stdin) != NULL) {
        if (___) {
            break;
        }
        ignorados++;
    }
    printf("golpe valido: %d (ignorados: %d)\n", golpe, ignorados);
    return 0;
}
```

#### Entrada
```
mil
nada
-5
42
```

#### Salida esperada
```
golpe valido: 42 (ignorados: 3)
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    char linea[50];
    int golpe = 0;
    int ignorados = 0;
    while (fgets(linea, sizeof linea, stdin) != NULL) {
        if (sscanf(linea, "%d", &golpe) == 1 && golpe >= 1 && golpe <= 99) {
            break;
        }
        ignorados++;
    }
    printf("golpe valido: %d (ignorados: %d)\n", golpe, ignorados);
    return 0;
}
```

#### Al superarla
Tres gritos ignorados y un golpe de verdad: cuarenta y dos. El gólem se queda sin trucos. Tizón le guiña un ojo a Kira desde la tribuna.

#### Imagen
- El Gólem de Escoria grita números que salen de su boca como chispas.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) sostiene un cartel con «1 a 99».

### Micro-misión R01-N10-P3 · Las placas del pecho

```meta
lugar: El patio de la Forja
personajes: Kira, Gheco, Maese Ferrum
carta: Bucle y decisión | leer en un for · contar las que cumplen · guardar el mayor en la misma vuelta
recompensa: xp 15, oro 15
```

#### Escena
El gólem tiene en el pecho ocho placas con números de temple, que Tizón le va dictando a Kira. Solo las placas con temple mayor a 600 resisten; las demás se pueden romper. Kira tiene que saber cuántas son y cuál es la más dura.

#### Gheco sugiere
Un `for` lee las ocho placas con `scanf`; en cada vuelta, un `if` cuenta las blandas y otro guarda la más dura (la primera placa arranca como la más dura).

#### Desafío
Completá las dos condiciones.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    int placa;
    int blandas = 0;
    int mas_dura = 0;
    for (int i = 1; i <= 8; i++) {
        scanf("%d", &placa);
        if (___) {
            blandas++;
        }
        if (i == 1 || ___) {
            mas_dura = placa;
        }
    }
    printf("placas para romper: %d\n", blandas);
    printf("la mas dura: %d\n", mas_dura);
    return 0;
}
```

#### Entrada
```
450 720 300 980 610 550 120 800
```

#### Salida esperada
```
placas para romper: 4
la mas dura: 980
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    int placa;
    int blandas = 0;
    int mas_dura = 0;
    for (int i = 1; i <= 8; i++) {
        scanf("%d", &placa);
        if (placa <= 600) {
            blandas++;
        }
        if (i == 1 || placa > mas_dura) {
            mas_dura = placa;
        }
    }
    printf("placas para romper: %d\n", blandas);
    printf("la mas dura: %d\n", mas_dura);
    return 0;
}
```

#### Al superarla
Cuatro placas blandas. Kira las rompe una por una con un martillo chico, sin apuro, sin espadazos. Ferrum anota algo en la pared que Kira no alcanza a leer.

#### Imagen
- El pecho del Gólem de Escoria con ocho placas numeradas; cuatro se resquebrajan.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) golpea con un martillo chico, concentrada.

### Micro-misión R01-N10-P4 · El gólem cae

```meta
lugar: El patio de la Forja
personajes: Kira, Gheco, Maese Ferrum, Tizón
criatura: dragon
carta: Todo junto | funciones + bucle + decisiones · main se lee como una historia · cada pieza en su lugar
recompensa: xp 25, oro 30
item: Espada Reforjada
```

#### Escena
Solo queda el corazón del gólem: una piedra de lava con 60 de vida. Kira tiene tres golpes medidos: 15, 25 y 30. Si los aplica en orden, con la función de antes, el gólem cae.
—Medí antes de pegar —le dice Tizón, y le pasa la libreta.

#### Gheco sugiere
Un bucle lee cada golpe, lo aplica con `vida_restante` y corta (`break`) cuando la vida llega a 0.

#### Desafío
Completá el bucle y el corte.

#### Código inicial
```c
#include <stdio.h>

int vida_restante(int vida, int golpe)
{
    return golpe >= vida ? 0 : vida - golpe;
}

int main(void)
{
    int corazon = 60;
    int golpe;
    for (int i = 0; i < 3; i++) {
        scanf("%d", &golpe);
        corazon = ___;
        printf("golpe de %d: le quedan %d\n", golpe, corazon);
        if (___) {
            printf("el golem de escoria cae\n");
            break;
        }
    }
    return 0;
}
```

#### Entrada
```
15 25 30
```

#### Salida esperada
```
golpe de 15: le quedan 45
golpe de 25: le quedan 20
golpe de 30: le quedan 0
el golem de escoria cae
```

#### Solución
```c
#include <stdio.h>

int vida_restante(int vida, int golpe)
{
    return golpe >= vida ? 0 : vida - golpe;
}

int main(void)
{
    int corazon = 60;
    int golpe;
    for (int i = 0; i < 3; i++) {
        scanf("%d", &golpe);
        corazon = vida_restante(corazon, golpe);
        printf("golpe de %d: le quedan %d\n", golpe, corazon);
        if (corazon == 0) {
            printf("el golem de escoria cae\n");
            break;
        }
    }
    return 0;
}
```

#### Al superarla
El Gólem de Escoria se desarma en una montaña de piedras tibias. Ferrum toma la espada rajada de Kira, la mete al horno y la **reforja** delante de todos. —La próxima —le dice, devolviéndosela— la forjás vos. —La **Espada Reforjada** va a tu mochila. En la pared, la cuenta queda: «Espadazos: 41. Problemas resueltos a espadazos: 0. Gólems: 1».

#### Imagen
- El Gólem de Escoria se desarma en una montaña de piedras tibias.
- Maese Ferrum (herrero enorme, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) saca del horno la espada de Kira, reforjada y brillante.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) la recibe con las dos manos.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) aplaude en la tribuna.

### Misión R01-N10-M1 · La caja de la Forja

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Escribí la caja registradora de la Forja:

1. Mostrá la lista de productos: `1` Espada ($120), `2` Escudo ($80), `3` Herradura ($15), `4` Clavo de acero ($4.50) y `0` para cobrar.
2. En un bucle, pedí el código y la cantidad (de 1 a 99) con una función que valide. Lo que no sea válido se vuelve a preguntar.
3. Por cada pedido, mostrá una línea alineada con la cantidad, el nombre y el subtotal.
4. Al cobrar, mostrá la cantidad de productos, el subtotal, el descuento (10 % si el subtotal llega a $500) y el total, con 2 decimales.

Usá funciones `precio(codigo)` y `nombre(codigo)` con `switch`.

#### Criterio de aprobación

- Valida código y cantidad con una función que vuelve a preguntar.
- Usa `precio` y `nombre` con `switch`.
- Muestra el ticket alineado y aplica el 10 % solo desde $500.
- Termina bien con `0` o si se termina la entrada.

#### Entrada de ejemplo

```
1
4
7
3
dos
2
4
12
0
```

#### Salida esperada

```
=== CAJA DE LA FORJA ===
1 Espada $120 | 2 Escudo $80 | 3 Herradura $15 | 4 Clavo $4.50 | 0 Cobrar
Producto: Cantidad: 
   4 x Espada             480.00
Producto: 
  Escribí un número del 0 al 4.
Producto: Cantidad: 
  Escribí un número del 1 al 99.
Cantidad: 
   2 x Herradura           30.00
Producto: Cantidad: 
  12 x Clavo de acero      54.00
Producto: 
--------------------------------
Productos: 18
Subtotal:      564.00
Descuento:      56.40
TOTAL:         507.60
```

#### Solución de referencia

```c
/*
 * Jefe R01 - Mision 1: la caja de la Forja.
 * Pedidos por codigo hasta el 0; ticket alineado; 10 % de descuento desde $500.
 */
#include <stdio.h>
#include <stdbool.h>

#define DESCUENTO_DESDE 500.0

double precio(int codigo)
{
    switch (codigo) {
    case 1: return 120.0;   /* espada */
    case 2: return 80.0;    /* escudo */
    case 3: return 15.0;    /* herradura */
    case 4: return 4.5;     /* clavo de acero */
    default: return -1.0;
    }
}

const char *nombre(int codigo)
{
    switch (codigo) {
    case 1: return "Espada";
    case 2: return "Escudo";
    case 3: return "Herradura";
    case 4: return "Clavo de acero";
    default: return "?";
    }
}

/* Lee un entero entre minimo y maximo; false si se termino la entrada. */
bool pedir_entero(const char *pregunta, int minimo, int maximo, int *resultado)
{
    char linea[100];
    for (;;) {
        printf("%s", pregunta);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        int n;
        char sobra;
        if (sscanf(linea, "%d %c", &n, &sobra) == 1 && n >= minimo && n <= maximo) {
            *resultado = n;
            return true;
        }
        printf("\n  Escribí un número del %d al %d.\n", minimo, maximo);
    }
}

int main(void)
{
    double total = 0.0;
    int items = 0;

    printf("=== CAJA DE LA FORJA ===\n");
    printf("1 Espada $120 | 2 Escudo $80 | 3 Herradura $15 | 4 Clavo $4.50 | 0 Cobrar\n");

    for (;;) {
        int codigo, cantidad;
        if (!pedir_entero("Producto: ", 0, 4, &codigo) || codigo == 0) {
            break;
        }
        if (!pedir_entero("Cantidad: ", 1, 99, &cantidad)) {
            break;
        }
        double subtotal = precio(codigo) * cantidad;
        printf("\n  %2d x %-15s %9.2f\n", cantidad, nombre(codigo), subtotal);
        total += subtotal;
        items += cantidad;
    }

    printf("\n--------------------------------\n");
    printf("Productos: %d\n", items);
    printf("Subtotal:  %10.2f\n", total);
    double descuento = total >= DESCUENTO_DESDE ? total * 0.10 : 0.0;
    printf("Descuento: %10.2f\n", descuento);
    printf("TOTAL:     %10.2f\n", total - descuento);
    return 0;
}
```

#### Pruebas

##### Cobra sin comprar
```entrada
0
```
```salida
=== CAJA DE LA FORJA ===
1 Espada $120 | 2 Escudo $80 | 3 Herradura $15 | 4 Clavo $4.50 | 0 Cobrar
Producto:
--------------------------------
Productos: 0
Subtotal:        0.00
Descuento:       0.00
TOTAL:           0.00
```

##### Descuento justo en 500
```entrada
2
5
3
4
0
```
```salida
=== CAJA DE LA FORJA ===
1 Espada $120 | 2 Escudo $80 | 3 Herradura $15 | 4 Clavo $4.50 | 0 Cobrar
Producto: Cantidad:
   5 x Escudo             400.00
Producto: Cantidad:
   4 x Herradura           60.00
Producto:
--------------------------------
Productos: 9
Subtotal:      460.00
Descuento:       0.00
TOTAL:         460.00
```

##### Se termina la entrada
```entrada
1
2
```
```salida
=== CAJA DE LA FORJA ===
1 Espada $120 | 2 Escudo $80 | 3 Herradura $15 | 4 Clavo $4.50 | 0 Cobrar
Producto: Cantidad:
   2 x Espada             240.00
Producto:
--------------------------------
Productos: 2
Subtotal:      240.00
Descuento:       0.00
TOTAL:         240.00
```

### Misión R01-N10-M2 · Las placas del Gólem

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Simulá el combate contra el Gólem de Escoria:

1. El Gólem tiene 40 de vida y tres placas de armadura: cabeza, pecho y piernas. Guardalas como **banderas** en un solo `unsigned`.
2. Con `srand(13)`, cada turno elegí la zona al azar (`1u << tirar(0, 2)`) y el daño (de 4 a 9) con una función `tirar(minimo, maximo)`.
3. Si la zona tiene su placa, el golpe **rompe la placa** (apagá el bit) y no hace daño. Si no, resta el daño (la vida no baja de 0).
4. Mostrá cada turno con la zona, el resultado, la armadura como `[CPI]` (con `-` en las placas rotas) y la vida.
5. El combate termina cuando el Gólem cae o a los 30 turnos.

#### Criterio de aprobación

- Guarda la armadura como banderas y las apaga con `&= ~`.
- Usa `srand(13)` y una función `tirar`.
- Muestra cada turno y el resultado final.

#### Salida esperada

```
El Gólem de Escoria se levanta: 40 de vida, armadura [CPI]
Turno  1: golpe a la cabeza    -> se rompe la placa [-PI] vida 40
Turno  2: golpe a la cabeza    -> 5 de daño      [-PI] vida 35
Turno  3: golpe al pecho       -> se rompe la placa [--I] vida 35
Turno  4: golpe a las piernas  -> se rompe la placa [---] vida 35
Turno  5: golpe a las piernas  -> 9 de daño      [---] vida 26
Turno  6: golpe al pecho       -> 5 de daño      [---] vida 21
Turno  7: golpe al pecho       -> 4 de daño      [---] vida 17
Turno  8: golpe a las piernas  -> 5 de daño      [---] vida 12
Turno  9: golpe a la cabeza    -> 8 de daño      [---] vida  4
Turno 10: golpe a las piernas  -> 4 de daño      [---] vida  0
¡El Gólem cae en el turno 10!
```

#### Solución de referencia

```c
/*
 * Jefe R01 - Mision 2: el combate contra el Golem de Escoria.
 * La armadura son tres bits: cada golpe en una zona protegida rompe la placa
 * en lugar de hacer dano.
 */
#include <stdio.h>
#include <stdlib.h>

#define CABEZA  (1u << 0)
#define PECHO   (1u << 1)
#define PIERNAS (1u << 2)

int tirar(int minimo, int maximo)
{
    return minimo + rand() % (maximo - minimo + 1);
}

const char *zona_nombre(unsigned zona)
{
    switch (zona) {
    case CABEZA: return "a la cabeza";
    case PECHO: return "al pecho";
    default: return "a las piernas";
    }
}

void mostrar_armadura(unsigned armadura)
{
    printf("[%c%c%c]", armadura & CABEZA ? 'C' : '-', armadura & PECHO ? 'P' : '-', armadura & PIERNAS ? 'I' : '-');
}

int main(void)
{
    srand(13);
    unsigned armadura = CABEZA | PECHO | PIERNAS;
    int vida = 40;
    int turno = 0;

    printf("El Gólem de Escoria se levanta: 40 de vida, armadura ");
    mostrar_armadura(armadura);
    printf("\n");

    while (vida > 0 && turno < 30) {
        turno++;
        unsigned zona = 1u << tirar(0, 2);
        int danio = tirar(4, 9);
        printf("Turno %2d: golpe %-14s ", turno, zona_nombre(zona));
        if (armadura & zona) {
            armadura &= ~zona;
            printf("-> se rompe la placa ");
        } else {
            vida -= danio;
            if (vida < 0) {
                vida = 0;
            }
            printf("-> %d de daño      ", danio);
        }
        mostrar_armadura(armadura);
        printf(" vida %2d\n", vida);
    }

    if (vida == 0) {
        printf("¡El Gólem cae en el turno %d!\n", turno);
    } else {
        printf("El Gólem resiste. Hay que volver con más fuerza.\n");
    }
    return 0;
}
```

### Encargo R01-N10-E1 · El conversor del Gremio

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 30
```

#### Consigna

El Gremio quiere un conversor para el mostrador. En un menú que se repite hasta elegir `0`:

1. °C a °F.
2. Kilómetros a millas (1 km = 0.621371 millas).
3. Pesos a dólares, a $1200 por dólar (un monto negativo no se acepta).

Cada conversión es una función. Todo lo que no sea un número se vuelve a preguntar, y una opción que no existe se avisa.

#### Criterio de aprobación

- Una función por conversión.
- Valida la opción y el valor.
- Termina con `0` o cuando se acaba la entrada.

#### Entrada de ejemplo

```
1
36.6
2
42.195
3
-5
9
hola
3
60000
0
```

#### Salida esperada

```
1) °C a °F  2) km a millas  3) pesos a dólares  0) salir
Opción: Valor: 
36.6 °C = 97.9 °F

1) °C a °F  2) km a millas  3) pesos a dólares  0) salir
Opción: Valor: 
42.20 km = 26.22 millas

1) °C a °F  2) km a millas  3) pesos a dólares  0) salir
Opción: Valor: 
Un monto no puede ser negativo.

1) °C a °F  2) km a millas  3) pesos a dólares  0) salir
Opción: 
Opción inválida.

1) °C a °F  2) km a millas  3) pesos a dólares  0) salir
Opción: 
  Eso no es un número (usá punto para los decimales).
Opción: Valor: 
$60000.00 = US$50.00

1) °C a °F  2) km a millas  3) pesos a dólares  0) salir
Opción: 
¡Hasta la próxima!
```

#### Solución de referencia

```c
/*
 * Jefe R01 - Encargo: el conversor del Gremio.
 * Menu en bucle con validacion; cada conversion es una funcion.
 */
#include <stdio.h>
#include <stdbool.h>

#define PESOS_POR_DOLAR 1200.0

double a_fahrenheit(double c) { return c * 9.0 / 5.0 + 32.0; }
double a_millas(double km) { return km * 0.621371; }
double a_dolares(double pesos) { return pesos / PESOS_POR_DOLAR; }

bool pedir_numero(const char *pregunta, double *resultado)
{
    char linea[100];
    for (;;) {
        printf("%s", pregunta);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        double x;
        char sobra;
        if (sscanf(linea, "%lf %c", &x, &sobra) == 1) {
            *resultado = x;
            return true;
        }
        printf("\n  Eso no es un número (usá punto para los decimales).\n");
    }
}

int main(void)
{
    for (;;) {
        printf("\n1) °C a °F  2) km a millas  3) pesos a dólares  0) salir\n");
        double opcion, valor;
        if (!pedir_numero("Opción: ", &opcion) || opcion == 0) {
            break;
        }
        if (opcion != 1 && opcion != 2 && opcion != 3) {
            printf("\nOpción inválida.\n");
            continue;
        }
        if (!pedir_numero("Valor: ", &valor)) {
            break;
        }
        if (opcion == 1) {
            printf("\n%.1f °C = %.1f °F\n", valor, a_fahrenheit(valor));
        } else if (opcion == 2) {
            printf("\n%.2f km = %.2f millas\n", valor, a_millas(valor));
        } else if (valor < 0) {
            printf("\nUn monto no puede ser negativo.\n");
        } else {
            printf("\n$%.2f = US$%.2f\n", valor, a_dolares(valor));
        }
    }
    printf("\n¡Hasta la próxima!\n");
    return 0;
}
```

#### Pruebas

##### Sale enseguida
```entrada
0
```
```salida
1) °C a °F  2) km a millas  3) pesos a dólares  0) salir
Opción:
¡Hasta la próxima!
```

##### Bajo cero y cero
```entrada
1
-40
3
0
0
```
```salida
1) °C a °F  2) km a millas  3) pesos a dólares  0) salir
Opción: Valor:
-40.0 °C = -40.0 °F

1) °C a °F  2) km a millas  3) pesos a dólares  0) salir
Opción: Valor:
$0.00 = US$0.00

1) °C a °F  2) km a millas  3) pesos a dólares  0) salir
Opción:
¡Hasta la próxima!
```

##### Se termina la entrada
```entrada
2
```
```salida
1) °C a °F  2) km a millas  3) pesos a dólares  0) salir
Opción: Valor:
¡Hasta la próxima!
```

### Prueba del sello

#### ¿Por qué conviene escribir una sola función para leer números en lugar de repetir `fgets` y `sscanf` en cada lugar?

Porque la validación queda en un solo lugar: si hay que corregirla, se corrige una vez, y el resto del programa queda más corto y claro.

#### En el combate, ¿qué hace `armadura &= ~zona;`?

Apaga el bit de esa zona: rompe la placa. `~zona` tiene todos los bits en 1 menos ese.

#### ¿Por qué el combate da siempre lo mismo? ¿Cómo lo harías distinto cada vez?

Porque la semilla es fija (`srand(13)`). Con `srand(time(NULL))` cambia en cada ejecución.

#### ¿Qué pasa si la entrada se termina en medio de un pedido?

`pedir_entero` devuelve `false` y el bucle termina: el programa cobra lo que había y sale, sin quedarse preguntando.

#### ¿Dónde está el descuento: en la función `precio` o en `main`? ¿Por qué?

En `main`, porque depende del total del pedido, no de cada producto. Cada función tiene una sola tarea.

### Soluciones (docente)

Proyecto nuevo (no está en FullCursos). Las salidas esperadas salen de compilar con gcc en Linux: la de la misión 2 depende del `rand` de glibc.
