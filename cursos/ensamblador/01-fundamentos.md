# RAMA R01 · Fundamentos: Nova aprende a hablar y a guardar

```meta
tipo: tronco
posicion: 1
```

## R01-N01 · La voz del Gólem: mostrar textos

```meta
tipo: tema
criatura: orc
padre: R00-N01
precio: 0
temas: prog.salida, maq.interrupciones, maq.direcciones
```

### Crónica

Nova ya mueve palancas, pero nadie se entera: el Gólem sigue mudo. En su cara hay un **ojo** redondo de cristal, apagado.

—Ese ojo es mi pantalla —dice {mentor}—. Lo enciendo cuando me pedís una **interrupción**: una llamada a DOS, el viejo guardián que sabe escribir en él.

Gheco se cuelga del borde del ojo. —El número mágico es **21h** —dice—. Ponés el pedido en AH, los datos donde corresponda, y decís `int 21h`. Es como llamar a una función que ya viene hecha.

### Objetivos

Mostrar texto en pantalla con `INT 21h`: un carácter con la función **02h** y una cadena con la **09h**.
Entender la diferencia entre la **dirección** de un texto (`offset`) y el texto mismo, el **`'$'`** que marca
dónde termina y los códigos **13 y 10** que bajan de renglón. Al final, mostrar un **dígito** sumándole `'0'`.

### Antes de empezar

- La Clase 0: registros, `mov`, hexadecimal, AH y AL.

### Explicación

#### Interrupciones: pedirle algo a DOS
El Gólem no sabe dibujar letras solo: le pide ayuda a **DOS** con la orden `int 21h` («interrupción 21h»).
Antes de llamarla, en **AH** va el **número de pedido** (qué querés que haga) y en otros registros, los datos.

> **Puente con otras lenguas.** `int 21h` es lo que hay debajo de un `print()` de Python o un `printf` de C:
> una llamada a una rutina que ya viene hecha, que sabe escribir en la pantalla.

#### Un carácter: la función 02h
```asm
mov dl, 'N'      ; DL = el carácter a mostrar (su código ASCII)
mov ah, 02h      ; pedido 02h: «mostrá el carácter de DL»
int 21h          ; ¡llamada!
```
`'N'` entre comillas simples es el **código ASCII** de la letra N (78, o 4Eh). Para el Gólem, las letras
son números.

#### Una cadena: la función 09h
Un texto se guarda en los cajones, en la sección `.data`, con un **nombre**:
```asm
.data
saludo db 'Hola, soy Nova$'
```
`db` quiere decir *define byte*: guarda un byte por cada letra, una al lado de la otra. El **`'$'`** del final
marca dónde termina el texto: la función 09h escribe letras **hasta encontrar un `$`**.

Para mostrarlo, la función 09h necesita saber **dónde empieza** el texto: su **dirección**, que se consigue con
`offset`:
```asm
mov dx, offset saludo   ; DX = la DIRECCIÓN de saludo (dónde está el primer cajón)
mov ah, 09h             ; pedido 09h: «mostrá la cadena que empieza en DX, hasta el $»
int 21h
```

#### Dirección y contenido
Es la idea más importante del ensamblador, y la vas a ver en todos los nodos:
- `offset saludo` es **dónde está** el texto (un número de cajón).
- `saludo` solo es **lo que hay** en ese cajón (la letra `H`).

La función 09h quiere el **dónde**. Si te olvidás del `offset`, DOS va a escribir desde un cajón cualquiera
y sale basura.

> **Puente con otras lenguas.** Es la misma idea que los **punteros** de C: `char *p` guarda una dirección y
> `*p` lo que hay ahí. En Python no se ve, pero pasa igual por debajo.

#### Bajar de renglón: 13 y 10
Para empezar un renglón nuevo se usan dos códigos: **13** (volver al principio del renglón) y **10** (bajar
uno). Van en el texto, separados por comas:
```asm
dos_lineas db 'Primera', 13, 10, 'Segunda$'
```

#### Mostrar un dígito: sumar `'0'`
Si DL vale 3, la función 02h muestra el carácter de código 3, que no es el **3** que vemos. El carácter `'3'`
tiene el código 51. El truco: los dígitos están seguidos en la tabla ASCII (`'0'` = 48, `'1'` = 49…), así que
**sumando `'0'`** el número se convierte en su dígito:
```asm
mov dl, 3
add dl, '0'      ; DL = 3 + 48 = 51 = '3'
mov ah, 02h
int 21h          ; muestra 3
```
`add` suma: `add destino, valor` es como `destino = destino + valor`. Solo sirve para un dígito (0 a 9); los
números más grandes vienen más adelante.

> **Puente con otras lenguas.** Es lo que hace `str(3)` en Python o `%d` en el `printf` de C: convertir un
> número en los caracteres que lo representan.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
saludo db 'Hola, soy Nova', 13, 10, '$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov dx, offset saludo   ; dónde empieza el texto
    mov ah, 09h             ; mostrar cadena
    int 21h

    mov dl, 'N'             ; un carácter
    mov ah, 02h
    int 21h

    mov dl, 7               ; un dígito: 7 + '0' = '7'
    add dl, '0'
    mov ah, 02h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

### Salida esperada

```
Hola, soy Nova
N7
```

### ¿Para qué sirve?

Mostrar resultados es lo primero que hace cualquier programa. Además, la idea de **dirección y contenido**
es la base de los punteros de C, de los arreglos en todas las lenguas y de cómo se pasan datos grandes a una
función sin copiarlos.

### Errores habituales

**Orco: el texto sin `$`.** Si falta el `'$'`, DOS sigue escribiendo cajones de más hasta toparse con uno
por casualidad: sale basura, o el Gólem se detiene: `INT 21h/09h: la cadena no termina en '$'`.

**Ogro: el `offset` que falta.** `mov dx, saludo` → para el ensamblador, `saludo` es un **byte** (la H) y DX
es de 16 bits: aparece un goblin, `Operands must be the same size: 2 - 1`. Lo que se quería era la
**dirección**: `mov dx, offset saludo`.

**Ogro: el dígito sin `'0'`.** `mov dl, 5` y función 02h muestra un símbolo raro (el carácter de código 5),
no un 5.

### Micro-misión R01-N01-P1 · El ojo se enciende

```meta
lugar: El ojo del Gólem
personajes: Nova, Gheco, Axón
carta: INT 21h, 02h | DL = el carácter · AH = 02h · int 21h · como print() de un solo carácter
recompensa: xp 10, oro 10
```

#### Escena
Nova junta coraje y le pide al Gólem que muestre su inicial en el ojo. —Una sola letra —dice—. La **N**.

#### Gheco sugiere
En `DL` va el carácter entre comillas simples, en `AH` el pedido `02h`, y después `int 21h`.

#### Desafío
Completá la orden que falta para que el ojo muestre la letra **N**.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov dl, ___
    mov ah, 02h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
N
```

#### Solución
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov dl, 'N'
    mov ah, 02h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El ojo del Gólem se enciende con una **N** verde, temblorosa. Nova se queda mirándola un rato largo. —Es mi nombre. Bueno, el principio.

#### Imagen
- La cara de un gólem de bronce gigante con un único ojo redondo de cristal que brilla con una letra N verde.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) mira el ojo desde adentro, con las manos juntas.
- Gheco (gecko de luz cian con antiparras, chiquito) colgado del borde del ojo.

### Micro-misión R01-N01-P2 · Una frase entera

```meta
lugar: El ojo del Gólem
personajes: Nova, Gheco
carta: INT 21h, 09h | DX = offset texto · AH = 09h · int 21h · escribe hasta el $
recompensa: xp 10, oro 10
```

#### Escena
Letra por letra tarda una eternidad. —¿No puedo mostrar una frase de una vez? —pregunta Nova.

#### Gheco sugiere
La función `09h` muestra un texto entero. Necesita en `DX` la **dirección** donde empieza: `mov dx, offset saludo`.

#### Desafío
El texto ya está guardado en `saludo`. Completá la orden para que DX tenga **su dirección** y el ojo muestre la frase.

#### Código inicial
```asm
.model small
.stack 100h
.data
saludo db 'Hola, soy Nova$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov dx, ___
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
Hola, soy Nova
```

#### Solución
```asm
.model small
.stack 100h
.data
saludo db 'Hola, soy Nova$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov dx, offset saludo
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
«Hola, soy Nova» aparece en el ojo, de una sola vez. Desde arriba, en las Forjas, alguien deja caer un martillo. —¿El Gólem… habló? —se oye a lo lejos.

#### Imagen
- El ojo redondo de cristal de un gólem de bronce, encendido con una línea de luz verde, vista desde adentro de la cabeza.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) saluda con la mano hacia el ojo.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre su hombro.

### Micro-misión R01-N01-P3 · El orco del dólar

```meta
lugar: La pared de los cajones
personajes: Nova, Gheco
criatura: orc
carta: El $ final | La función 09h escribe hasta encontrar un $ · sin $, sigue de largo
recompensa: xp 10, oro 10
```

#### Escena
Nova guarda una frase nueva, pero el ojo se llena de símbolos raros y el Gólem se frena. Detrás de los cajones gruñe un **orco**.

#### Gheco sugiere
La función 09h escribe **hasta el `$`**. Si falta, sigue leyendo los cajones de al lado. Agregalo al final del texto, adentro de las comillas.

#### Desafío
Arreglá el texto para que el ojo muestre solo **Despierta** y nada más.

#### Código inicial
```asm
.model small
.stack 100h
.data
grito db 'Despierta'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov dx, offset grito
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
Despierta
```

#### Solución
```asm
.model small
.stack 100h
.data
grito db 'Despierta$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov dx, offset grito
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El orco se queda sin cajones que revolver y se va refunfuñando. Nova anota en su memoria: *todo texto termina en `$`*.

#### Imagen
- Una pared enorme de cajoncitos de bronce, algunos abiertos y desordenados.
- Un orco verde y gruñón revuelve los cajones.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) le cierra un cajón en la cara, decidida.
- Gheco (gecko de luz cian con antiparras, chiquito) sostiene una moneda de bronce lisa.

### Micro-misión R01-N01-P4 · Dos renglones

```meta
lugar: El ojo del Gólem
personajes: Nova, Gheco
carta: 13, 10 | 13 vuelve al principio del renglón · 10 baja uno · como el \n de Python y C
recompensa: xp 10, oro 10
```

#### Escena
Nova quiere escribir su nombre y abajo el del Gólem, pero los dos le salen pegados en el mismo renglón.

#### Gheco sugiere
Para bajar de renglón se ponen los códigos **13** y **10** dentro del texto, separados por comas: `'uno', 13, 10, 'dos$'`.

#### Desafío
Completá el texto para que **Nova** quede en un renglón y **Axón** en el siguiente.

#### Código inicial
```asm
.model small
.stack 100h
.data
nombres db 'Nova', ___, ___, 'Axon$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov dx, offset nombres
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
Nova
Axon
```

#### Solución
```asm
.model small
.stack 100h
.data
nombres db 'Nova', 13, 10, 'Axon$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov dx, offset nombres
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Dos renglones, prolijos. —Así se escribe una lista —dice Nova—. Ahora puedo presentarnos a los dos.

#### Imagen
- El ojo de cristal de un gólem de bronce con dos líneas de luz verde, una debajo de la otra.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) señala la línea de abajo.
- Gheco (gecko de luz cian con antiparras, chiquito) baja por una escalerita de luz entre las dos líneas.

### Micro-misión R01-N01-P5 · El número que no era número

```meta
lugar: El ojo del Gólem
personajes: Nova, Gheco, Axón
criatura: ogre
carta: Dígito | add dl, '0' · convierte 0..9 en '0'..'9' · como str(n) en Python
recompensa: xp 15, oro 15
```

#### Escena
Nova quiere mostrar cuántas palancas aprendió: **4**. Pero el ojo muestra un símbolo con forma de diamante. —Yo te pedí un 4 —dice. —Y yo te mostré el carácter número 4 —responde {mentor}—. Exactamente lo que me ordenaste.

#### Gheco sugiere
El carácter `'4'` no tiene el código 4 sino el 52. Sumando `'0'` (48) se pasa del número al dígito: `add dl, '0'`.

#### Desafío
Agregá la orden que falta para que el ojo muestre el dígito **4**.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov dl, 4
    ___
    mov ah, 02h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
4
```

#### Solución
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov dl, 4
    add dl, '0'
    mov ah, 02h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El diamante se convierte en un **4** limpito. Un ogro que espiaba desde la torre se va, aburrido: con Nova atenta no tiene nada que hacer.

#### Imagen
- El ojo de cristal de un gólem de bronce que muestra un diamante de luz transformándose en un dígito brillante.
- Un ogro grandote y verde espía desde un costado, con cara de fastidio.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) sonríe con un dedo levantado.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre el borde del ojo.

### Micro-misión R01-N01-P6 · La presentación de Nova

```meta
lugar: El ojo del Gólem
personajes: Nova, Gheco, Axón
carta: 09h y 02h juntas | Primero la cadena con 09h, después el dígito con 02h · cada int 21h pisa AL
recompensa: xp 20, oro 20
```

#### Escena
Ahora sí: Nova quiere presentarse completa. Un texto y, al final, un número.

#### Gheco sugiere
Juntá lo que aprendiste: la cadena con la función `09h` y el dígito con `add dl, '0'` y la función `02h`. Ojo: antes de cada `int 21h`, AH tiene que tener el pedido correcto.

#### Desafío
Completá el programa para que el ojo muestre **Palancas: 5** (el texto ya termina con el espacio después de los dos puntos).

#### Código inicial
```asm
.model small
.stack 100h
.data
etiqueta db 'Palancas: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov dx, offset etiqueta
    mov ah, ___
    int 21h

    mov dl, 5
    add dl, '0'
    mov ah, ___
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
Palancas: 5
```

#### Solución
```asm
.model small
.stack 100h
.data
etiqueta db 'Palancas: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov dx, offset etiqueta
    mov ah, 09h
    int 21h

    mov dl, 5
    add dl, '0'
    mov ah, 02h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
«Palancas: 5». Desde las Forjas baja corriendo una chica con un visor cian: **Kira**. Mira el ojo encendido, mira al Gólem y dice despacito: —Te escucho.

#### Imagen
- La cara de un gólem de bronce gigante con su ojo de cristal encendido con una línea de luz verde.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) mira el ojo desde abajo, asombrada.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se asoma por la grieta del pecho del gólem.
- Gheco (gecko de luz cian con antiparras, chiquito) en el hombro de Kira.

### Prueba del sello

#### ¿Qué va en AH antes de `int 21h` para mostrar un carácter? ¿Y para mostrar una cadena?
02h para un carácter (en DL) y 09h para una cadena (con su dirección en DX).

#### ¿Qué diferencia hay entre `offset saludo` y `saludo`?
`offset saludo` es la dirección donde empieza el texto; `saludo` es lo que hay en ese cajón (la primera letra).

#### ¿Para qué sirve el `$` al final de un texto?
Le marca a la función 09h dónde termina.

#### Si DL = 6, ¿qué hay que hacer para que la función 02h muestre un 6?
Sumarle `'0'`: `add dl, '0'`.

## R01-N02 · Los cajones con nombre: variables

```meta
tipo: tema
criatura: goblin
padre: R01-N01
precio: 0
temas: prog.variables, maq.memoria
```

### Crónica

Las palancas no alcanzan: Nova tiene que recordar muchas cosas y el Gólem tiene solo un puñado de manos. —Lo demás lo guardo en mis **cajones** —dice {mentor}, y abre una pared llena de cajoncitos numerados, miles y miles.

—¿Y cómo sé cuál es cuál? —pregunta Nova.

—Les ponés **nombre**. Pero cuidado —agrega Gheco, mostrando dos cajones—: hay cajones de **un byte** y cajones de **dos**. Si mezclás tamaños, aparecen los goblins.

### Objetivos

Declarar **variables** en `.data` con `db` (un byte) y `dw` (dos bytes, un *word*), leerlas y escribirlas con
`mov`, operar directo sobre ellas con `inc`, declarar **constantes** con `equ`, y entender por qué los tamaños
tienen que coincidir.

### Antes de empezar

- Registros, `mov`, AH y AL (Clase 0).
- La función 02h y el truco de `'0'` (nodo anterior).

### Explicación

#### Una variable es un cajón con nombre
En la sección `.data`, cada variable es un **nombre** para un cajón de la memoria:
```asm
.data
pociones db 3       ; un cajón de 1 byte, con un 3 adentro
vida     dw 300     ; un cajón de 2 bytes (un word), con 300 adentro
```

| Directiva | Ocupa | Guarda |
|---|---|---|
| `db` (*define byte*) | 1 byte | 0 a 255, o un carácter |
| `dw` (*define word*) | 2 bytes | 0 a 65535 |

> **Puente con otras lenguas.** Es exactamente `char pociones = 3;` y `short vida = 300;` en C, o
> `pociones = 3` en Python. La diferencia es que acá **vos elegís el tamaño** de cada cajón.

#### Leer y escribir una variable
```asm
mov al, pociones    ; leer:    AL = lo que hay en el cajón pociones
mov pociones, 5     ; escribir: el cajón pociones pasa a tener un 5
```
Y se puede operar **directo sobre el cajón**, sin pasar por una palanca:
```asm
inc pociones        ; pociones = pociones + 1  (como pociones++ en C)
dec pociones        ; pociones = pociones - 1
```

En el tablero, la pestaña **Cajones** muestra los bytes de la memoria; el lugar donde empieza cada variable
aparece **subrayado** (pasá el mouse para ver su nombre).

#### Los tamaños tienen que coincidir
`pociones` es de 1 byte y `AX` de 2: `mov ax, pociones` no se puede (¿qué haría con el byte que falta?). Hay que
usar una palanca del mismo tamaño:
```asm
mov al, pociones    ; byte con byte: bien
mov ax, vida        ; word con word: bien
mov ax, pociones    ; ✗ goblin: Operands must be the same size: 2 - 1
```

#### De memoria a memoria, no
El Gólem no puede pasar algo de un cajón a otro de una sola vez: siempre **pasa por una palanca**.
```asm
mov al, pociones    ; del cajón a la palanca
mov guardadas, al   ; de la palanca al otro cajón
```

#### Constantes con `equ`
```asm
MAXIMO equ 9
```
Una constante **no ocupa cajón**: el ensamblador reemplaza el nombre por el número antes de empezar. Sirve para
no repetir números mágicos.

> **Puente con otras lenguas.** Es el `#define MAXIMO 9` o el `const int MAXIMO = 9;` de C, o una constante
> en mayúsculas de Python.

### Código de ejemplo

```asm
.model small
.stack 100h
MAXIMO equ 9
.data
pociones db 3
vida     dw 300
.code
main proc
    mov ax, @data
    mov ds, ax

    inc pociones          ; pociones = 4
    mov al, pociones      ; AL = 4
    mov ax, vida          ; AX = 300 = 012Ch
    mov bl, MAXIMO        ; BL = 9

    mov dl, pociones      ; mostrar pociones como dígito
    add dl, '0'
    mov ah, 02h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

### Salida esperada

```
4
```

### ¿Para qué sirve?

Toda variable de cualquier lengua es, por debajo, un cajón con un tamaño. Entender los tamaños explica por qué
un número «se da vuelta» cuando se pasa de largo (el overflow), por qué en C hay `char`, `short`, `int` y
`long`, y cuánta memoria usa un programa.

### Errores habituales

**Goblin: tamaños distintos.** `mov ax, pociones` (`pociones` es byte):
```
main.asm(11) : Error A2048: Operands must be the same size: 2 - 1
```

**Goblin: de memoria a memoria.** `mov guardadas, pociones`: el 8086 no copia de un cajón a otro; hace falta pasar
por una palanca.

**Esqueleto: el nombre que no existe.** Un error de tipeo (`pocion` en vez de `pociones`):
```
main.asm(11) : Error A2102: Symbol not defined : pocion
```

**Slime: palabras reservadas.** Algunos nombres ya los usa el ensamblador (`name`, `size`, `type`, `length`…):
```
main.asm(4) : Error A2209: Syntax error: size
```

### Micro-misión R01-N02-P1 · El primer cajón

```meta
lugar: La pared de los cajones
personajes: Nova, Gheco, Axón
carta: db | nombre db valor · un cajón de 1 byte · como char pociones = 3; en C
recompensa: xp 10, oro 10
```

#### Escena
Nova encuentra un cajón vacío y le pone una etiqueta: **pociones**. Adentro guarda tres frasquitos de luz.

#### Gheco sugiere
En `.data` se declara con `nombre db valor`. Después, `mov al, pociones` copia lo que hay en el cajón a la palanca AL.

#### Desafío
Declará la variable `pociones` con el valor **3** y copiala en **AL**.

#### Código inicial
```asm
.model small
.stack 100h
.data
pociones db ___
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, ___

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
AL = 3
[pociones] = 3
```

#### Solución
```asm
.model small
.stack 100h
.data
pociones db 3
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, pociones

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El cajón **pociones** brilla en la pared. Nova abre la pestaña Cajones del tablero y lo encuentra: un **03** subrayado. —Ese soy yo guardando algo.

#### Imagen
- Una pared de cajoncitos de bronce; uno brilla con una etiqueta de luz lisa con el dibujo de un frasquito.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) guarda tres frasquitos de luz dentro del cajón.
- Gheco (gecko de luz cian con antiparras, chiquito) sostiene la etiqueta.

### Micro-misión R01-N02-P2 · Cambiar lo que hay adentro

```meta
lugar: La pared de los cajones
personajes: Nova, Gheco
carta: Escribir una variable | mov variable, valor · como pociones = 5
recompensa: xp 10, oro 10
```

#### Escena
Nova encuentra dos pociones más tiradas en un pasillo. Ahora tiene **5**, y el cajón todavía dice 3.

#### Gheco sugiere
Para escribir en un cajón, el nombre va de destino: `mov pociones, 5`. Como en Python `pociones = 5`.

#### Desafío
Completá la orden para que el cajón **pociones** pase a tener **5**.

#### Código inicial
```asm
.model small
.stack 100h
.data
pociones db 3
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ___, ___

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
[pociones] = 5
```

#### Solución
```asm
.model small
.stack 100h
.data
pociones db 3
.code
main proc
    mov ax, @data
    mov ds, ax

    mov pociones, 5

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El 03 del cajón se vuelve 05. —No hace falta pasar por una palanca para poner un número —se sorprende Nova.

#### Imagen
- Un cajón de bronce abierto con cinco frasquitos de luz ámbar.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) agrega dos frasquitos con cuidado.
- Gheco (gecko de luz cian con antiparras, chiquito) cuenta con los dedos sentado en el borde del cajón.

### Micro-misión R01-N02-P3 · Una más

```meta
lugar: La pared de los cajones
personajes: Nova, Gheco
carta: inc y dec | inc pociones = pociones + 1 · dec = - 1 · como pociones++ en C
recompensa: xp 10, oro 10
```

#### Escena
Gheco aparece con una poción más en la cola. —¿Hay que sacar todo, sumar y volver a guardar?

#### Gheco sugiere
No: `inc pociones` suma 1 **directo en el cajón**. `dec` resta 1. Es el `pociones++` de C o el `pociones += 1` de Python.

#### Desafío
Agregá la orden que suma **una** poción, para que el cajón quede en **4**.

#### Código inicial
```asm
.model small
.stack 100h
.data
pociones db 3
.code
main proc
    mov ax, @data
    mov ds, ax

    ___

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
[pociones] = 4
```

#### Solución
```asm
.model small
.stack 100h
.data
pociones db 3
.code
main proc
    mov ax, @data
    mov ds, ax

    inc pociones

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Cuatro pociones. Nova prueba `dec` también, solo para ver, y vuelve a poner `inc`. —Uno más, uno menos. Lo voy a usar todo el tiempo.

#### Imagen
- Un cajón de bronce con cuatro frasquitos de luz y un quinto frasquito flotando hacia adentro.
- Gheco (gecko de luz cian con antiparras, chiquito) empuja el frasquito con la cola.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) aplaude.

### Micro-misión R01-N02-P4 · El cajón doble

```meta
lugar: La pared de los cajones
personajes: Nova, Gheco, Axón
carta: dw | nombre dw valor · 2 bytes (un word) · va con palancas de 16 bits (AX, BX…)
recompensa: xp 10, oro 10
```

#### Escena
La vida del Gólem es **300**, y no entra en un cajón chico (hasta 255). {mentor} le muestra a Nova un cajón **doble**.

#### Gheco sugiere
`dw` declara un *word*: dos bytes, hasta 65535. Se lee con una palanca entera de 16 bits: `mov ax, vida`.

#### Desafío
Declará `vida` como **word** con el valor **300** y copiala en **AX**.

#### Código inicial
```asm
.model small
.stack 100h
.data
vida ___ 300
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ___, vida

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
AX = 300
word [vida] = 300
```

#### Solución
```asm
.model small
.stack 100h
.data
vida dw 300
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, vida

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El visor de AX marca **012C**: 300 en hexadecimal. En la pestaña Cajones, Nova ve que `vida` ocupa **dos** cajones: `2C` y `01`. —¿Están al revés? —Así guardo los words —dice {mentor}—: primero la mitad baja.

#### Imagen
- Un cajón de bronce doble, el doble de ancho que los demás, con una etiqueta de luz lisa con el dibujo de un corazón.
- Axón (gólem de bronce gigante con un único ojo redondo de cristal) lo señala con un dedo enorme.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) abre el cajón doble con las dos manos.
- Gheco (gecko de luz cian con antiparras, chiquito) mira por la rendija.

### Micro-misión R01-N02-P5 · El goblin de los tamaños

```meta
lugar: La pared de los cajones
personajes: Nova, Gheco
criatura: goblin
carta: Mismo tamaño | byte con byte (AL, BL…) · word con word (AX, BX…) · si no: Operands must be the same size
recompensa: xp 15, oro 15
```

#### Escena
Nova intenta llevar sus pociones a la palanca AX y aparece un **goblin**, riéndose: *«Operands must be the same size: 2 - 1»*.

#### Gheco sugiere
`pociones` es de **1 byte** y `AX` de **2**. Usá la mitad de 1 byte: `AL`. El mensaje dice los tamaños: 2 (AX) contra 1 (pociones).

#### Desafío
Tocá **Ejecutar** para ver el error del goblin. Después arreglá la orden para que las pociones queden en **AL**.

#### Código inicial
```asm
.model small
.stack 100h
.data
pociones db 3
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, pociones

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
AL = 3
```

#### Solución
```asm
.model small
.stack 100h
.data
pociones db 3
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, pociones

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El goblin se queda sin chiste y desaparece entre los cajones. Nova ya sabe leer el mensaje: *el primer número es el tamaño de la izquierda; el segundo, el de la derecha*.

#### Imagen
- Un goblin verde y flaco que se ríe colgado de una palanca de bronce grande.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) le muestra un cajón chico y una palanca chica que encajan perfecto.
- Gheco (gecko de luz cian con antiparras, chiquito) le saca la lengua al goblin.

### Micro-misión R01-N02-P6 · El número que no cambia

```meta
lugar: El núcleo del Gólem
personajes: Nova, Gheco, Axón
carta: equ | NOMBRE equ 9 · no ocupa cajón · como #define o const en C
recompensa: xp 20, oro 20
```

#### Escena
—¿Cuántas pociones puedo cargar como máximo? —pregunta Nova. —**Nueve** —responde {mentor}—. Siempre nueve. Eso no es un cajón: es una regla.

#### Gheco sugiere
`MAXIMO equ 9` define una **constante**: no ocupa cajón, el ensamblador cambia el nombre por el 9. Se usa como un número: `mov bl, MAXIMO`.

#### Desafío
Completá la constante con el valor **9** y cargala en **BL**. Después mostrala en el ojo como dígito (las órdenes de mostrar ya están).

#### Código inicial
```asm
.model small
.stack 100h
MAXIMO equ ___
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bl, ___

    mov dl, bl
    add dl, '0'
    mov ah, 02h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
9
```

#### Estado esperado
```
BL = 9
```

#### Solución
```asm
.model small
.stack 100h
MAXIMO equ 9
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bl, MAXIMO

    mov dl, bl
    add dl, '0'
    mov ah, 02h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Un 9 aparece en el ojo. {mentor} graba una etiqueta de bronce y se la pega en el pecho: **MAXIMO = 9**. —Las reglas no se guardan en cajones —dice—. Se escriben una vez y se respetan siempre.

#### Imagen
- Un gólem de bronce gigante con una placa de bronce lisa en el pecho, con el dibujo grabado de nueve frasquitos.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) toca la placa con la punta de los dedos.
- Gheco (gecko de luz cian con antiparras, chiquito) lustra la placa con la cola.

### Prueba del sello

#### ¿Qué diferencia hay entre `db` y `dw`?
`db` reserva 1 byte (hasta 255); `dw` reserva 2 bytes, un word (hasta 65535).

#### ¿Por qué `mov ax, pociones` da error si `pociones` es `db`?
Porque AX es de 2 bytes y pociones de 1: los tamaños tienen que coincidir. Se usa AL.

#### ¿Cómo se pasa el valor de un cajón a otro?
Pasando por una palanca: `mov al, uno` y después `mov otro, al`.

#### ¿Ocupa memoria una constante declarada con `equ`?
No: el ensamblador reemplaza el nombre por su valor antes de traducir.

## R01-N03 · Dirección y contenido: dónde vive cada cajón

```meta
tipo: tema
criatura: ogre
padre: R01-N02
precio: 0
temas: maq.direcciones, maq.memoria
```

### Crónica

Nova ya les pone nombre a sus cajones, pero cuando le pide a {mentor} que muestre su nombre en el ojo, el Gólem contesta:

—No me des el nombre. Dame **dónde** está.

Nova no entiende. Gheco se para frente a la pared de cajones y la recorre con la cola: —Cada cajón tiene un **número**, empezando por el 0. El nombre es la etiqueta que vos le pegaste; el número es su **dirección**. A veces el Gólem quiere lo que hay **adentro**, y a veces quiere saber **dónde** está.

### Objetivos

Distinguir la **dirección** de una variable (`offset`, `lea`) de su **contenido** (el nombre solo), reservar
varios cajones de una vez con `dup` y `?`, llegar al cajón siguiente con `nombre+1`, y entender por qué los
words se guardan «al revés» (*little endian*) y para qué sirve `byte ptr`.

### Antes de empezar

- Variables con `db`, `dw` y `equ` (nodo anterior).
- La función 09h, que pide la dirección del texto en DX (La voz del Gólem).

### Explicación

#### La pared de cajones
La memoria es una fila larguísima de cajones de **un byte**, numerados desde el 0. Cada variable de `.data`
ocupa uno o más cajones seguidos, en el orden en que la declarás:

```asm
.data
nombre   db 'Nova$'     ; cajones 0, 1, 2, 3 y 4
pociones db 3           ; cajón 5
```

```
dirección:   0    1    2    3    4    5
contenido:  'N'  'o'  'v'  'a'  '$'   3
            └──────── nombre ───────┘ pociones
```

#### Dirección y contenido
- `mov al, pociones` → AL recibe el **contenido**: 3.
- `mov bx, offset pociones` → BX recibe la **dirección**: 5.

`offset` quiere decir «¿en qué cajón empieza?». Por eso la función 09h pide `offset saludo`: DOS necesita saber
**dónde** empieza el texto para ir leyendo cajón por cajón hasta el `'$'`.

> **Puente con otras lenguas.** `offset pociones` es el `&pociones` de C: la dirección de la variable. Un
> **puntero** no es más que una palanca que guarda una dirección, como BX acá.

#### `lea`: la otra forma de pedir la dirección
```asm
lea dx, saludo          ; igual que mov dx, offset saludo
```
`lea` (*load effective address*, «cargá la dirección») hace lo mismo que `offset`. Vas a ver las dos en
programas ajenos; elegí la que te resulte más clara.

#### Muchos cajones de una vez: `dup` y `?`
```asm
mochila db 5 dup('-'), '$'   ; cinco '-' seguidos y un '$': seis cajones
puntos  dw 10 dup(0)         ; diez words en 0: veinte cajones
llave   db ?                 ; un cajón sin valor elegido
```
- `N dup(x)` repite `x` N veces.
- `?` reserva el lugar sin elegir qué hay adentro: no confíes en lo que tiene hasta que lo escribas.

> **Puente con otras lenguas.** `mochila db 5 dup('-')` es el `char mochila[5]` de C o la lista
> `['-'] * 5` de Python: un **arreglo** es una fila de cajones seguidos.

#### El cajón siguiente: `nombre+1`
`mochila` es el primer cajón de la mochila; `mochila+1`, el segundo; `mochila+2`, el tercero…

```asm
mov mochila+1, 'P'      ; el segundo cajón pasa a tener una P
```

Es el `mochila[1] = 'P'` de C o Python: el índice es cuántos cajones avanzás desde el primero.

#### Little endian: los words al revés
Un `dw` ocupa **dos** cajones, y el 8086 guarda **primero el byte bajo**:

```asm
monedas dw 4142h
```
```
dirección:   monedas   monedas+1
contenido:     42h        41h
```

Si lo leés entero (`mov bx, monedas`), vuelve a ser `4142h`. Si lo leés de a un byte, aparecen al revés. Las
PC de hoy guardan los números igual.

#### `byte ptr`: tomá solo un byte
`monedas` es un word, así que `mov al, monedas` despierta al goblin (AL es de 1 byte). Con `byte ptr` le
decís al ensamblador «de esta variable, tomá **un solo** byte»:

```asm
mov al, byte ptr monedas       ; AL = 42h (el primer cajón)
mov ah, byte ptr monedas+1     ; AH = 41h (el segundo)
```

### Código de ejemplo

```asm
.model small
.stack 100h
.data
nombre   db 'Nova$'
mochila  db 5 dup('-'), '$'
monedas  dw 4142h
salto    db 13, 10, '$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, nombre            ; la dirección del texto
    mov ah, 09h
    int 21h
    mov dx, offset salto
    int 21h

    mov mochila, 'E'          ; el primer cajón de la mochila
    mov mochila+1, 'P'        ; el segundo
    lea dx, mochila
    int 21h
    mov dx, offset salto
    int 21h

    mov dl, byte ptr monedas    ; los dos bytes de monedas, en el orden de la memoria
    mov ah, 02h
    int 21h
    mov dl, byte ptr monedas+1
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

### Salida esperada

```
Nova
EP---
BA
```

### ¿Para qué sirve?

La diferencia entre dirección y contenido es **la** idea detrás de los punteros de C y C++, de las
referencias de Java y Python y de cómo se pasa un arreglo a una función (se pasa dónde empieza, no una copia).
El little endian aparece cada vez que se leen archivos binarios o se mandan números por la red.

### Errores habituales

**Goblin: el contenido en vez de la dirección.** `mov dx, nombre` antes de la 09h (`nombre` es `db` y DX es
de 2 bytes):
```
main.asm(12) : Error A2048: Operands must be the same size: 2 - 1
```
Faltó `offset`: `mov dx, offset nombre` (o `lea dx, nombre`).

**Ogro: la dirección en vez del contenido.** Querías las pociones en BL (`mov bl, pociones`) y escribiste
`mov bx, offset pociones`: no da error, pero BL queda con el número del cajón (5), no con las pociones (3). El programa corre y da otra cosa. Se
descubre con el paso a paso.

**Goblin: un byte de un word.** `mov al, monedas` (`monedas` es `dw`):
```
main.asm(12) : Error A2048: Operands must be the same size: 1 - 2
```
Se arregla con `byte ptr monedas`.

**Orco: el texto sin `'$'`.** `mochila db 5 dup('-')` sin el `'$'` final: la 09h sigue mostrando los cajones
que vienen después, hasta encontrar un `'$'` en cualquier lado.

### Micro-misión R01-N03-P1 · ¿En qué cajón vivís?

```meta
lugar: La pared de los cajones
personajes: Nova, Gheco, Axón
carta: offset | offset x = la dirección (el número del cajón) · x solo = el contenido · como &x en C
recompensa: xp 10, oro 10
```

#### Escena
Nova señala el cajón de las pociones. —Adentro hay 3. Pero ¿cuál es su **número** en la pared? {mentor} espera, inmóvil: quiere las dos cosas.

#### Gheco sugiere
`mov al, pociones` copia lo que hay **adentro**. `mov bx, offset pociones` copia **dónde está**. Contá: la pared empieza en el cajón 0, y `nombre` ocupa los cinco primeros (`N`, `o`, `v`, `a` y `$`).

#### Desafío
Completá las dos órdenes: que **BX** quede con la **dirección** de `pociones` y **AL** con su **contenido**. Antes de ejecutar, adiviná cuánto va a valer BX.

#### Código inicial
```asm
.model small
.stack 100h
.data
nombre   db 'Nova$'
pociones db 3
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bx, ___ pociones     ; la dirección
    mov al, ___              ; el contenido

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
BX = 5
AL = 3
```

#### Solución
```asm
.model small
.stack 100h
.data
nombre   db 'Nova$'
pociones db 3
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bx, offset pociones
    mov al, pociones

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
BX marca 0005 y AL marca 03. —El cajón **cinco** tiene **tres** pociones —dice Nova despacito, para no confundirse—. Dónde y qué. Son dos preguntas distintas.

#### Imagen
- Una pared de cajoncitos de bronce; uno brilla, con cinco rayitas grabadas en el marco y tres frasquitos de luz adentro.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) señala con una mano el marco y con la otra los frasquitos.
- Gheco (gecko de luz cian con antiparras, chiquito) camina por el borde de los cajones contando con la cola.

### Micro-misión R01-N03-P2 · La otra forma de señalar

```meta
lugar: El ojo del Gólem
personajes: Nova, Gheco
carta: lea | lea dx, texto = mov dx, offset texto · carga la dirección, no el contenido
recompensa: xp 10, oro 10
```

#### Escena
—Siempre escribo `offset` antes del texto —dice Nova—. ¿Hay otra forma? Gheco saca de la cola una palabra corta: **lea**.

#### Gheco sugiere
`lea dx, saludo` deja en DX la dirección de `saludo`, igual que `mov dx, offset saludo`. Es justo lo que la 09h necesita.

#### Desafío
Completá la orden con `lea` para que el ojo muestre el saludo de Nova.

#### Código inicial
```asm
.model small
.stack 100h
.data
saludo db 'Ya se donde vivo$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea ___, ___
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
Ya se donde vivo
```

#### Solución
```asm
.model small
.stack 100h
.data
saludo db 'Ya se donde vivo$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, saludo
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El ojo del Gólem escribe la frase de Nova. —`offset` o `lea` —dice Gheco—. Las dos señalan el mismo cajón. Usá la que te salga más natural.

#### Imagen
- El ojo redondo de cristal de un gólem de bronce, encendido con una línea de luz cian.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) apunta al ojo con el dedo, y del dedo sale un hilo de luz.
- Gheco (gecko de luz cian con antiparras, chiquito) sigue el hilo de luz caminando por el aire.

### Micro-misión R01-N03-P3 · La mochila de cinco bolsillos

```meta
lugar: La pared de los cajones
personajes: Nova, Gheco
carta: dup | nombre db 5 dup('-') · cinco cajones seguidos iguales · como ['-'] * 5 en Python
recompensa: xp 10, oro 10
```

#### Escena
Nova quiere una mochila con **cinco** bolsillos vacíos. —¿Tengo que declarar cinco cajones, uno por uno?

#### Gheco sugiere
`5 dup('-')` repite el `'-'` cinco veces, en cinco cajones seguidos. Después va el `'$'`, para que la 09h sepa dónde termina.

#### Desafío
Completá la declaración para que la mochila tenga **cinco** guiones (los bolsillos vacíos) y el ojo los muestre.

#### Código inicial
```asm
.model small
.stack 100h
.data
mochila db ___ dup(___), '$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, mochila
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
-----
```

#### Estado esperado
```
[mochila+4] = '-'
[mochila+5] = '$'
```

#### Solución
```asm
.model small
.stack 100h
.data
mochila db 5 dup('-'), '$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, mochila
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Cinco bolsillos vacíos, uno al lado del otro. —Es una **fila** de cajones —dice Nova—. Con un solo nombre.

#### Imagen
- Una mochila de bronce con cinco bolsillos iguales en fila, todos vacíos, colgada de una pared de cajoncitos.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se cuelga la mochila al hombro, contenta.
- Gheco (gecko de luz cian con antiparras, chiquito) se asoma desde el último bolsillo.

### Micro-misión R01-N03-P4 · El segundo bolsillo

```meta
lugar: La pared de los cajones
personajes: Nova, Gheco
carta: nombre+1 | mochila = el primer cajón · mochila+1 = el segundo · como mochila[1] en C o Python
recompensa: xp 10, oro 10
```

#### Escena
Nova encuentra una pluma de luz y la quiere guardar en el **segundo** bolsillo de la mochila, sin tocar los demás.

#### Gheco sugiere
`mochila` es el primer cajón; `mochila+1`, el que sigue. `mov mochila+1, 'P'` escribe una P solo ahí. Es el `mochila[1] = 'P'` de C o Python.

#### Desafío
Completá la orden para que el **segundo** bolsillo tenga una **P** (de pluma). El ojo tiene que mostrar `-P---`.

#### Código inicial
```asm
.model small
.stack 100h
.data
mochila db 5 dup('-'), '$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ___, 'P'

    lea dx, mochila
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
-P---
```

#### Estado esperado
```
[mochila] = '-'
[mochila+1] = 'P'
```

#### Solución
```asm
.model small
.stack 100h
.data
mochila db 5 dup('-'), '$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov mochila+1, 'P'

    lea dx, mochila
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
La pluma brilla en el segundo bolsillo. —El primero es el **cero** —se da cuenta Nova—: `mochila+0`. Por eso el segundo es el `+1`.

#### Imagen
- Una mochila de bronce con cinco bolsillos en fila; solo el segundo tiene una pluma de luz cian que asoma.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) guarda la pluma con cuidado.
- Gheco (gecko de luz cian con antiparras, chiquito) señala el primer bolsillo, vacío.

### Micro-misión R01-N03-P5 · Las monedas al revés

```meta
lugar: La pared de los cajones
personajes: Nova, Gheco, Axón
carta: Little endian | un dw se guarda con el byte bajo primero · 4142h queda 42h, 41h
recompensa: xp 15, oro 15
```

#### Escena
Nova guarda `4142h` monedas en un cajón doble y mira la pestaña **Cajones**: ve un `42` y **después** un `41`. —¡Se dio vuelta! —Así guardo los words —dice {mentor}—: la mitad baja, primero.

#### Gheco sugiere
En `4142h`, la mitad **baja** son las dos cifras de la derecha: `42h`. Esa va en el primer cajón. Si dudás, ejecutá el programa: el ojo muestra los dos bytes en el orden en que están guardados (`41h` es la letra A y `42h` la B).

#### Desafío
Predecí: ¿qué byte está en el **primer** cajón de `monedas`? Escribilo en hexa en lugar de `___`, para que **BL** quede con ese byte.

#### Código inicial
```asm
.model small
.stack 100h
.data
monedas dw 4142h
.code
main proc
    mov ax, @data
    mov ds, ax

    mov dl, byte ptr monedas      ; el primer cajón
    mov ah, 02h
    int 21h
    mov dl, byte ptr monedas+1    ; el segundo
    int 21h

    mov bl, ___      ; ¿qué byte está primero?

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
BA
```

#### Estado esperado
```
BL = 42h
[monedas] = 42h
[monedas+1] = 41h
```

#### Solución
```asm
.model small
.stack 100h
.data
monedas dw 4142h
.code
main proc
    mov ax, @data
    mov ds, ax

    mov dl, byte ptr monedas      ; el primer cajón
    mov ah, 02h
    int 21h
    mov dl, byte ptr monedas+1    ; el segundo
    int 21h

    mov bl, 42h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El ojo muestra **BA**, no AB. —Leído de a uno, al revés —dice Nova—. Leído entero, al derecho. {mentor} asiente con un crujido: las PC de hoy, siglos después, guardan los números igual que él.

#### Imagen
- Un cajón doble de bronce abierto: en la mitad izquierda una moneda dorada con una estrella, en la derecha una moneda dorada con una luna.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) inclina la cabeza, desconcertada, como leyendo al revés.
- Gheco (gecko de luz cian con antiparras, chiquito) hace la vertical sobre el cajón.

### Micro-misión R01-N03-P6 · El goblin del cajón doble

```meta
lugar: La pared de los cajones
personajes: Nova, Gheco
criatura: goblin
carta: byte ptr | byte ptr variable = tomá un solo byte · byte ptr x+1 = el segundo
recompensa: xp 15, oro 15
```

#### Escena
Nova quiere solo la mitad **alta** de las monedas (el `41h`, la letra A) en AL. Escribe `mov al, monedas` y aparece un goblin: *«Operands must be the same size: 1 - 2»*.

#### Gheco sugiere
`monedas` es un word (2 bytes) y AL es de 1. Con `byte ptr` tomás un solo byte: `byte ptr monedas` es el primer cajón y `byte ptr monedas+1` el segundo. La mitad alta está en el **segundo** (acordate del little endian).

#### Desafío
Tocá **Ejecutar** para ver al goblin. Después arreglá la orden para que **AL** quede con la mitad alta de `monedas` (`41h`), y el ojo muestre la A.

#### Código inicial
```asm
.model small
.stack 100h
.data
monedas dw 4142h
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, monedas

    mov bl, al
    mov dl, bl
    mov ah, 02h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
A
```

#### Estado esperado
```
BL = 41h
```

#### Solución
```asm
.model small
.stack 100h
.data
monedas dw 4142h
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, byte ptr monedas+1

    mov bl, al
    mov dl, bl
    mov ah, 02h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Una A en el ojo. El goblin se rasca la cabeza: no esperaba que Nova supiera pedir **un pedazo** de un cajón doble. Se va refunfuñando.

#### Imagen
- Un goblin verde y flaco sentado sobre un cajón doble de bronce, con cara de enojado.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) saca una sola moneda dorada de la mitad derecha del cajón, sin abrir la otra.
- Gheco (gecko de luz cian con antiparras, chiquito) le sostiene una lupa.

### Micro-misión R01-N03-P7 · La mochila de Nova

```meta
lugar: El núcleo del Gólem
personajes: Nova, Gheco, Axón
carta: Dirección y contenido | offset y lea = dónde · el nombre = qué hay · nombre+1 = el cajón siguiente
recompensa: xp 20, oro 20
```

#### Escena
Antes de seguir, Nova arma su mochila de viaje: una **E** (de espada de luz) en el primer bolsillo y una **P** (la pluma) en el segundo. {mentor} quiere verla en el ojo.

#### Gheco sugiere
Necesitás tres cosas que ya sabés: escribir en `mochila` y en `mochila+1`, dejar en DX la **dirección** de la mochila (`lea` u `offset`) y pedir la 09h.

#### Desafío
Escribí las órdenes desde cero, donde dice `; tus órdenes`, para que el ojo muestre `EP---`.

#### Código inicial
```asm
.model small
.stack 100h
.data
mochila db 5 dup('-'), '$'
.code
main proc
    mov ax, @data
    mov ds, ax

    ; tus órdenes

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
EP---
```

#### Estado esperado
```
[mochila] = 'E'
[mochila+1] = 'P'
```

#### Solución
```asm
.model small
.stack 100h
.data
mochila db 5 dup('-'), '$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov mochila, 'E'
    mov mochila+1, 'P'
    lea dx, mochila
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
**EP---** brilla en el ojo. La pared de cajones entera se ilumina por un instante, de punta a punta: Nova ya sabe **dónde** vive cada cosa. —Ahora me falta escuchar —dice—. Hasta ahora solo hablo yo.

#### Imagen
- Una pared enorme de cajoncitos de bronce que se ilumina de punta a punta con luz cian.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) con una mochila de bronce al hombro, de la que asoman una espada de luz y una pluma.
- Axón (gólem de bronce gigante con un único ojo redondo de cristal) la mira desde arriba con el ojo encendido.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre la mochila.

### Prueba del sello

#### ¿Qué diferencia hay entre `mov al, pociones` y `mov bx, offset pociones`?
La primera copia el contenido del cajón (lo que hay adentro); la segunda, su dirección (en qué cajón está).

#### ¿Qué hace `lea dx, saludo`?
Deja en DX la dirección de `saludo`, igual que `mov dx, offset saludo`.

#### ¿Cuántos cajones ocupa `mochila db 5 dup('-'), '$'`?
Seis: cinco guiones y el `'$'`.

#### Si `monedas dw 1234h`, ¿qué byte está primero en la memoria?
34h: el 8086 guarda primero el byte bajo (little endian).

#### ¿Para qué sirve `byte ptr`?
Para tomar un solo byte de una variable más grande, como un word.
