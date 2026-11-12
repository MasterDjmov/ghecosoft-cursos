# RAMA S01 · Senda del Taller de Aparatos: in, out y los aparatos de emu8086

```meta
tipo: senda
posicion: 5
```

## S01-N01 · Los nervios del Gólem: `in` y `out`

```meta
tipo: tema
padre: R02-N09
precio: 0
criatura: goblin
temas: maq.interrupciones, maq.registros
```

### Crónica

Ahora que {mentor} está de pie, Kira baja del Gremio de las Forjas con una idea. —Arriba hay un montón de aparatos que nadie sabe manejar —dice—: el semáforo de la encrucijada, el visor del Gremio, el termómetro del horno, la grúa, la impresora, el robot de las minas. Y el Gólem tiene **nervios** que llegan a todos.

{mentor} levanta una mano enorme: de las yemas salen cientos de cables finos, numerados. —Mis **puertos** —dice—. Por cada uno puedo mandar un byte, o escuchar lo que me mandan.

### Objetivos

Mandar datos a un aparato con `out`, leer lo que un aparato deja con `in`, saber qué palancas acepta cada una (AL o
AX, y un número de puerto o DX), y usar la solapa **Aparatos · puertos** del tablero, con los mismos aparatos y
números de puerto que trae emu8086.

### Antes de empezar

- Registros, bytes y words (Clase 0 y Los cajones con nombre).
- Binario y bits (Bits y máscaras).
- `cmp`, saltos y `loop` (la rama de Decisiones y repeticiones).

### Explicación

#### Puertos: la otra memoria
Además de los cajones (la memoria), el 8086 tiene **65.536 puertos**: lugares por donde habla con los aparatos (el
teclado, la pantalla, los discos, el parlante). No se usan con `mov`, sino con dos órdenes propias:

| Orden | Hace | Como… |
|---|---|---|
| `out puerto, al` | manda el byte de AL al puerto | escribir en un cajón del aparato |
| `out puerto, ax` | manda el word de AX (el puerto y el siguiente) | |
| `in al, puerto` | trae a AL el byte que dejó el aparato | leer un cajón del aparato |
| `in ax, puerto` | trae el word | |

Las reglas son estrictas: el dato va **siempre** en AL o AX, y el número de puerto es un número de **0 a 255** o
la palanca **DX** (para cualquier puerto, hasta 65.535).

```asm
mov al, 0A7h
out 110, al         ; manda A7h al puerto 110
mov dx, 300
out dx, al          ; el puerto 300 no entra en un byte: va en DX
in al, 110          ; lee lo que hay en el puerto 110
```

#### Los aparatos del taller
Son los mismos que trae emu8086 (en su menú *virtual devices*), con sus mismos puertos:

| Aparato | Puertos |
|---|---|
| Puertos simples (para probar) | 110 (byte) y 112 (word) |
| Semáforo de la encrucijada | 4 (word) |
| Motor paso a paso de la grúa | 7 |
| Robot de las minas | 9 (orden), 10 (dato), 11 (estado) |
| Termómetro del horno | 125 (temperatura) y 127 (calefactor) |
| Impresora del Gremio | 130 |
| Visor de números del Gremio | 199 (word con signo) |

Cuando el programa usa un puerto, en el tablero aparece la solapa **Aparatos · puertos** con el aparato dibujado.
En el estado esperado, `puerto 110 = A7h` dice qué quedó en un puerto (con `word` delante, dos bytes).

> **Puente con otras lenguas.** En C para microcontroladores (Arduino, por ejemplo), `digitalWrite` y
> `analogRead` hacen esto: mandar y leer de un puerto. En una compu de hoy, los programas no tocan los puertos:
> le piden al sistema operativo que lo haga un **controlador** (*driver*), que está escrito justamente con `in` y
> `out`.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
t db 'Volvio: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 'K'
    out 110, al         ; al puerto 110
    mov al, 0
    in al, 110          ; y de vuelta
    mov bl, al

    lea dx, t
    mov ah, 09h
    int 21h
    mov dl, bl
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
Volvio: K
```

### ¿Para qué sirve?

Todo lo que una compu le dice a un aparato pasa por puertos o por memoria mapeada: el teclado avisa qué tecla se
apretó, la placa de sonido recibe las ondas, el disco recibe qué sector leer. Los microcontroladores (Arduino,
ESP32, los de un lavarropas o un auto) se programan casi solo así: mandando y leyendo bits de sus puertos.

### Errores habituales

**Goblin: el dato en otra palanca.** `out 110, bl` no existe: el dato va en AL o AX.

**Goblin: un puerto de más de 255 con número.** `out 300, al`:
```
main.asm(9) : Error A2049: Invalid instruction operands
```
`mov dx, 300` y `out dx, al`.

**Ogro: el orden al revés.** En `out` va primero el puerto y después el dato; en `in`, primero la palanca y después
el puerto.

**Ogro: byte o word.** `out 112, ax` escribe dos puertos (112 y 113); para un aparato de un byte, `out 112, al`.

### Micro-misión S01-N01-P1 · El primer nervio

```meta
lugar: El taller de aparatos
personajes: Nova, Gheco, Kira
carta: out | out puerto, al · manda el byte de AL a un aparato · el dato siempre en AL o AX
recompensa: xp 15, oro 15
```

#### Escena
Kira conecta una cajita de prueba a los nervios del Gólem, en el puerto **110**. —Mandale algo —dice—. Cualquier cosa.

#### Gheco sugiere
**`out`** manda un byte a un puerto: `out 110, al` manda lo que hay en AL al puerto 110. El dato va **siempre** en AL (o AX, si es un word). En la solapa **Aparatos · puertos** del tablero vas a ver el puerto con su valor.

#### Desafío
Completá la orden que manda AL al puerto 110, para que el puerto quede con `A7h`.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 0A7h
    ___ 110, al

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
puerto 110 = A7h
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

    mov al, 0A7h
    out 110, al

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Una lucecita de la cajita de prueba se prende y muestra `A7`. —Te escuchó —dice Kira—. Ahora preguntale algo.

#### Imagen
- Un taller lleno de aparatos de bronce y cables finos que salen de la mano enorme de un gólem, conectados a una cajita de bronce con una lucecita cian encendida.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) enchufa un cable en la cajita.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) mira la lucecita, contenta.
- Gheco (gecko de luz cian con antiparras, chiquito) camina por un cable como por una cuerda floja.

### Micro-misión S01-N01-P2 · La respuesta del aparato

```meta
lugar: El taller de aparatos
personajes: Nova, Gheco
carta: in | in al, puerto · trae a AL el byte del aparato · primero la palanca, después el puerto
recompensa: xp 15, oro 15
```

#### Escena
La cajita guarda lo que le mandan. Nova quiere comprobarlo: leer el puerto 110 y ver si el `A7h` sigue ahí.

#### Gheco sugiere
**`in`** es lo contrario de `out`: `in al, 110` trae a AL el byte que hay en el puerto 110. Ojo con el orden: en `in` va primero la palanca (AL) y después el puerto.

#### Desafío
Completá la orden que lee el puerto 110 en AL, para que BL quede con `A7h`.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 0A7h
    out 110, al
    mov al, 0           ; AL vacío
    ___ al, 110
    mov bl, al

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
BL = A7h
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

    mov al, 0A7h
    out 110, al
    mov al, 0           ; AL vacío
    in al, 110
    mov bl, al

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
BL = `A7h`: la cajita lo devolvió intacto. —Mando por un nervio y escucho por el mismo —dice Nova.

#### Imagen
- Una cajita de bronce con una lucecita cian encendida, de la que sale un pulso de luz que viaja por un cable fino hacia una mano mecánica enorme.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) pone la oreja cerca del cable, escuchando.
- Gheco (gecko de luz cian con antiparras, chiquito) sigue el pulso de luz con la cabeza.

### Micro-misión S01-N01-P3 · Un word por dos nervios

```meta
lugar: El taller de aparatos
personajes: Nova, Gheco
carta: out con AX | out 112, ax · manda un word: el byte bajo al puerto 112 y el alto al 113
recompensa: xp 15, oro 15
```

#### Escena
La cajita tiene otro lugar, el puerto **112**, que guarda un número de dos bytes. Kira quiere guardar ahí el **1234h**.

#### Gheco sugiere
Con **AX**, `out` manda un **word**: el byte bajo (AL) al puerto 112 y el alto (AH) al 113. Igual que un word en los cajones: primero la mitad baja.

#### Desafío
Completá la palanca del `out`, para que en el puerto 112 quede el word `1234h`.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 1234h
    out 112, ___

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
word puerto 112 = 1234h
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

    mov ax, 1234h
    out 112, ax

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
En la solapa de aparatos aparecen dos puertos: el 112 con `34h` y el 113 con `12h`. —Al revés, como en los cajones —sonríe Nova.

#### Imagen
- Dos cables finos de bronce paralelos, cada uno llevando un pulso de luz cian, entrando en una cajita de bronce con dos lucecitas.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) sostiene los dos cables, uno en cada mano.
- Gheco (gecko de luz cian con antiparras, chiquito) sentado sobre la cajita.

### Micro-misión S01-N01-P4 · El nervio número 300

```meta
lugar: El taller de aparatos
personajes: Nova, Gheco
criatura: goblin
carta: Puerto en DX | con número, solo puertos 0 a 255 · para más: mov dx, 300 · out dx, al
recompensa: xp 20, oro 20
```

#### Escena
Kira enchufa un aparato nuevo en el nervio **300**. Nova escribe `out 300, al` y un goblin se ríe desde la maraña de cables: *«Invalid instruction operands»*.

#### Gheco sugiere
Escrito como número, el puerto entra en **un byte**: de 0 a 255. Para cualquier otro (hasta 65.535), el número va en **DX**: `mov dx, 300` y después `out dx, al`.

#### Desafío
Tocá **Ejecutar** para ver el error. Después arreglalo con DX, para que el puerto 300 quede con un **5**.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 5
    out 300, al

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
puerto 300 = 5
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

    mov al, 5
    mov dx, 300
    out dx, al

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El aparato del nervio 300 se prende. El goblin se enreda solo en los cables y desaparece. —Con número, hasta 255 —repite Nova—. Con DX, cualquiera.

#### Imagen
- Una maraña de cables finos de bronce con etiquetas lisas, uno de ellos brillando cian, conectado a un aparato que se enciende.
- Un goblin verde y flaco de caricatura, con ropa de tela cerrada, enredado en los cables, de cabeza.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) desenreda el cable que brilla.
- Gheco (gecko de luz cian con antiparras, chiquito) se ríe en su hombro.

### Prueba del sello

#### ¿En qué palancas va el dato de `in` y `out`?
Siempre en AL (un byte) o AX (un word).

#### ¿Cómo se escribe en el puerto 300?
Con el número en DX: `mov dx, 300` y `out dx, al`. Como número solo entran puertos de 0 a 255.

#### ¿Qué diferencia hay entre `out 112, al` y `out 112, ax`?
Con AL se escribe un byte en el puerto 112; con AX, dos: el bajo en el 112 y el alto en el 113.

## S01-N02 · El visor del Gremio

```meta
tipo: tema
padre: S01-N01
precio: 0
criatura: goblin
temas: maq.registros, maq.numeracion
```

### Crónica

Arriba, en el salón del Gremio, hay un **visor de números**: cinco cifras rojas de luz donde se anotan los puntajes de las carreras. Nadie sabe moverlo desde que se rompió la palanca. Kira le lleva a Nova el cable: va al puerto **199**.

### Objetivos

Mostrar números en el visor de emu8086 (puerto 199, un word con signo), mostrar negativos, hacer una cuenta
regresiva y mostrar el resultado de una cuenta sin tener que convertirlo a texto.

### Antes de empezar

- `out` con AX (Los nervios del Gólem).
- Números con signo (Con signo y sin signo).
- `loop` (Repetir).

### Explicación

#### Un word, cinco cifras
El visor lee el **word** del puerto 199 (dos bytes: 199 y 200) como un número **con signo** y lo muestra en
decimal, con un signo menos si hace falta: de −32.768 a 32.767. No hay que convertir nada a texto: el visor hace
el trabajo que en la pantalla hacía el grimorio de los números.

```asm
mov ax, 1234
out 199, ax         ; el visor muestra 1234
mov ax, -42
out 199, ax         ; muestra -42
```

Cada `out` reemplaza lo anterior: el visor siempre muestra el **último** número que recibió.

> **Puente con otras lenguas.** Es como un `print` que no necesita convertir el número a texto, porque el aparato
> lo hace solo. Los visores de siete segmentos de los microondas, los relojes y los surtidores de nafta se manejan
> así: mandando un número a un puerto.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 2026
    out 199, ax         ; 2026
    mov cx, 3
cuenta:
    mov ax, cx
    out 199, ax         ; 3, 2, 1
    loop cuenta
    mov ax, -1
    out 199, ax         ; -1

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

### ¿Para qué sirve?

Los marcadores, los contadores de personas, los relojes y los instrumentos de medición muestran números así. En el
paso a paso del tablero se ve cada número aparecer en el visor, uno por uno.

### Errores habituales

**Ogro: mandar un byte.** `out 199, al` escribe solo el byte bajo: el alto queda con lo que tenía y el visor muestra
otro número. Al visor, siempre `out 199, ax`.

**Ogro: números de más.** El visor tiene cinco cifras y signo: más de 32.767 aparece como negativo, porque lo lee
con signo.

### Micro-misión S01-N02-P1 · El puntaje

```meta
lugar: El salón del Gremio
personajes: Nova, Gheco, Kira
carta: Visor (199) | out 199, ax · muestra el word con signo, en decimal · cada out reemplaza el anterior
recompensa: xp 15, oro 15
```

#### Escena
El campeón de la carrera de hoy hizo **1234** puntos, y el visor del Gremio sigue mostrando ceros.

#### Gheco sugiere
El visor lee el **word** del puerto 199 y lo muestra en decimal: `mov ax, 1234` y `out 199, ax`. Tiene que ser AX, no AL: el visor usa dos bytes.

#### Desafío
Completá el puerto y la palanca, para que el visor muestre **1234**.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 1234
    out ___, ___

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
word puerto 199 = 1234
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

    mov ax, 1234
    out 199, ax

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El visor del Gremio se enciende con un **1234** rojo. Desde el salón se oyen aplausos. Kira levanta el pulgar hacia el ojo de {mentor}.

#### Imagen
- Un salón de piedra del Gremio de las Forjas con un visor grande de cinco cifras rojas de luz en la pared, encendido (cifras sin forma legible).
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) levanta el pulgar.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) sostiene un cable fino que llega al visor.
- Gheco (gecko de luz cian con antiparras, chiquito) aplaude sobre el visor.

### Micro-misión S01-N02-P2 · La deuda en el visor

```meta
lugar: El salón del Gremio
personajes: Nova, Gheco
carta: Negativos en el visor | el visor lee con signo · -42 aparece como -42 · más de 32767 se ve negativo
recompensa: xp 15, oro 15
```

#### Escena
El Gremio anota también las deudas: el taller de Gheco debe **42** chispas, y el visor tiene que mostrarlo con su signo.

#### Gheco sugiere
El visor lee el word **con signo**: `mov ax, -42` deja AX en `FFD6h`, y el visor muestra **−42**. No hace falta hacer nada más.

#### Desafío
Completá el número, para que el visor muestre **−42**.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, ___
    out 199, ax

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
word puerto 199 = -42
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

    mov ax, -42
    out 199, ax

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
**−42** en rojo. Gheco se esconde detrás de Nova. —No hacía falta mostrarlo tan grande —murmura.

#### Imagen
- Un visor grande de cifras rojas de luz con un signo menos al principio (cifras sin forma legible), en la pared de piedra del Gremio.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se ríe, mirando el visor.
- Gheco (gecko de luz cian con antiparras, chiquito) se esconde detrás de su capa, avergonzado.

### Micro-misión S01-N02-P3 · La cuenta regresiva de la carrera

```meta
lugar: El salón del Gremio
personajes: Nova, Gheco, Kira
carta: Visor en un bucle | out 199, ax dentro de loop · el visor muestra cada número · el último queda
recompensa: xp 15, oro 15
```

#### Escena
La próxima carrera arranca con una cuenta regresiva en el visor: **5, 4, 3, 2, 1**… y **0**, ¡largada!

#### Gheco sugiere
Dentro del bucle, cada vuelta manda CX al visor (`mov ax, cx` y `out 199, ax`). `loop` cuenta 5, 4, 3, 2, 1. Después del bucle, falta mandar el **0** de la largada.

#### Desafío
Escribí las dos órdenes que mandan el 0 al visor después del bucle, donde dice `; tus órdenes`.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov cx, 5
cuenta:
    mov ax, cx
    out 199, ax
    loop cuenta
    ; tus órdenes

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
word puerto 199 = 0
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

    mov cx, 5
cuenta:
    mov ax, cx
    out 199, ax
    loop cuenta
    mov ax, 0
    out 199, ax

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
5, 4, 3, 2, 1… **0**. Kira sale disparada en la carrera. Con el paso a paso, Nova ve cada número aparecer en el visor del tablero.

#### Imagen
- Un visor grande de cifras rojas de luz en la pared de un salón de piedra, y abajo una pista de carreras con una línea de largada brillante.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) sale corriendo desde la línea de largada.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) baja una banderita.
- Gheco (gecko de luz cian con antiparras, chiquito) sentado arriba del visor.

### Micro-misión S01-N02-P4 · La suma del Gremio

```meta
lugar: El salón del Gremio
personajes: Nova, Gheco
carta: Visor sin convertir | el visor muestra el número en decimal solo · sin dividir por 10 ni sumar '0'
recompensa: xp 20, oro 20
```

#### Escena
El Gremio quiere saber cuántas monedas juntó en diez días si cada día juntó una más que el anterior: 1 + 2 + … + 10. En la pantalla habría que convertir el resultado a cifras. En el visor, no.

#### Gheco sugiere
Sumá con un bucle: AX empieza en 0 y en cada vuelta le sumás CX (10, 9, …, 1). Al final, `out 199, ax` y el visor muestra el resultado en decimal, sin `div` ni `+ '0'`.

#### Desafío
Escribí las órdenes desde cero, donde dice `; tus órdenes`, para que el visor muestre la suma: **55**.

#### Código inicial
```asm
.model small
.stack 100h
.data
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

#### Estado esperado
```
word puerto 199 = 55
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

    mov ax, 0
    mov cx, 10
suma:
    add ax, cx
    loop suma
    out 199, ax

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
**55** en el visor. Los del Gremio no lo pueden creer: —¡Más rápido que el contador! —Y sin convertir nada —dice Nova—. El visor hace la parte difícil.

#### Imagen
- Un visor grande de cifras rojas de luz encendido en la pared del Gremio, con una pila de monedas doradas lisas debajo.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) cuenta con los dedos, sonriendo.
- Gheco (gecko de luz cian con antiparras, chiquito) sentado sobre la pila de monedas.

### Prueba del sello

#### ¿Por qué al visor hay que mandarle AX y no AL?
Porque lee un word (los puertos 199 y 200); con AL, el byte alto queda con cualquier cosa.

#### ¿Cómo muestra el visor un −42?
Con su signo: lee el word con signo. Basta `mov ax, -42` y `out 199, ax`.

## S01-N03 · El semáforo de la encrucijada

```meta
tipo: tema
padre: S01-N02
precio: 0
criatura: ogre
temas: prog.bits, maq.registros
```

### Crónica

En la encrucijada de las Forjas, donde se cruzan los carros de carbón, hay un semáforo de bronce con **cuatro** esquinas. Desde que se trabó, los carros chocan todos los días. Kira encontró su cable: va al puerto **4**.

### Objetivos

Manejar el semáforo de emu8086 (puerto 4, un word con un bit por luz): prender y apagar luces con máscaras, armar
situaciones en binario, esperar un tiempo con `INT 15h` (función 86h) y recorrer una tabla de situaciones.

### Antes de empezar

- Bits, máscaras y números en binario (Bits y máscaras).
- `out` con AX (Los nervios del Gólem).
- Arreglos de words y `lodsw` (Arreglos e índices; Las órdenes de fila, si las hiciste).

### Explicación

#### Un bit por luz
El semáforo tiene **12 luces**: 4 esquinas con rojo, amarillo y verde. Cada luz es un **bit** del word que se
manda al puerto 4: 1 prendida, 0 apagada.

| Bits | Esquina | Rojo | Amarillo | Verde |
|---|---|---|---|---|
| 0 a 2 | abajo (los que suben) | bit 0 | bit 1 | bit 2 |
| 3 a 5 | derecha | bit 3 | bit 4 | bit 5 |
| 6 a 8 | arriba | bit 6 | bit 7 | bit 8 |
| 9 a 11 | izquierda | bit 9 | bit 10 | bit 11 |

Escrito en binario, se lee de derecha a izquierda, de a tres. **Todo en rojo** es `0000001001001001b` (los bits
0, 3, 6 y 9). emu8086 deja separar las cifras con guiones bajos (`0000_0010_0100_1001b`), pero MASM no: acá se
escriben juntas.

#### Esperar
Un semáforo que cambia en un instante no sirve. La BIOS tiene una función para **esperar**: `INT 15h` con AH = 86h
espera CX:DX microsegundos (un millón es un segundo).

```asm
mov cx, 0Fh         ; CX:DX = 000F4240h = 1.000.000 µs = 1 segundo
mov dx, 4240h
mov ah, 86h
int 15h
```

En el tablero, el reloj del Gólem avanza ese tiempo de una vez: no hay que esperar de verdad.

> **Puente con otras lenguas.** Los bits del semáforo son las «banderas» que se usan en C, Python o JavaScript
> (`ROJO_ABAJO = 1 << 0`, `VERDE_ABAJO = 1 << 2`) y se combinan con `|`. La espera es el `sleep` de Python, el
> `delay` de Arduino o el `setTimeout` de JavaScript.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 0000001001001001b   ; todo en rojo
    out 4, ax
    mov ax, 0000001001001100b   ; verde para los de abajo
    out 4, ax
    mov cx, 0Fh                 ; un segundo
    mov dx, 4240h
    mov ah, 86h
    int 15h
    mov ax, 0000001001001010b   ; amarillo para los de abajo
    out 4, ax

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

### ¿Para qué sirve?

Así se controlan de verdad los semáforos, los carteles de luces y las máquinas industriales: un controlador manda
patrones de bits a sus salidas, cada uno con su tiempo. Es la base de la **domótica** y de cualquier tablero de
control.

### Errores habituales

**Ogro: contar los bits desde la izquierda.** El bit 0 es el de **más a la derecha**. Rojo abajo es `...001b`, no
`100...b`.

**Ogro: dos colores en la misma esquina.** Verde y rojo prendidos juntos en una esquina: los carros no saben qué
hacer. Una luz por esquina.

**Ogro: la espera con AX.** `INT 15h` (86h) mira CX:DX, no AX: CX la parte alta y DX la baja.

### Micro-misión S01-N03-P1 · Todo en rojo

```meta
lugar: La encrucijada de las Forjas
personajes: Nova, Gheco, Kira
criatura: ogre
carta: Semáforo (puerto 4) | 12 bits: rojo, amarillo y verde de cada esquina, de a 3 · todo en rojo: bits 0, 3, 6 y 9
recompensa: xp 15, oro 15
```

#### Escena
Lo primero es frenar a todos: el semáforo tiene que mostrar **rojo en las cuatro esquinas**. Un ogro carretero espera, impaciente, en el cruce.

#### Gheco sugiere
Cada esquina usa 3 bits: rojo (el de la derecha), amarillo y verde. El rojo de cada esquina es el bit 0, 3, 6 y 9. En binario, de derecha a izquierda (y separado de a cuatro para leerlo mejor): `0000 0010 0100 1001`, que se escribe junto con una `b` al final.

#### Desafío
Completá el número binario de «todo en rojo» y mandalo al semáforo.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, ___
    out 4, ax

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
word puerto 4 = 0249h
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

    mov ax, 0000001001001001b
    out 4, ax

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Las cuatro esquinas se ponen en rojo. Los carros frenan. El ogro carretero refunfuña, pero se queda quieto.

#### Imagen
- Un cruce de calles de piedra en una ciudad de forjas de noche, con un semáforo de bronce de cuatro caras, todas con la luz roja encendida.
- Un ogro grandote y torpe, con ropa de cuero cerrada, frena un carro de carbón con cara de fastidio.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) levanta la mano en señal de alto.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) flota junto al semáforo; Gheco (gecko de luz cian con antiparras, chiquito) está sentado arriba del semáforo.

### Micro-misión S01-N03-P2 · Verde para los de abajo

```meta
lugar: La encrucijada de las Forjas
personajes: Nova, Gheco
carta: Prender un verde | partir de todo en rojo · en la esquina de abajo: apagar el bit 0 y prender el bit 2
recompensa: xp 15, oro 15
```

#### Escena
Los carros de abajo esperan desde hace rato. Nova quiere darles **verde**, sin tocar el rojo de las otras tres esquinas.

#### Gheco sugiere
Partí de «todo en rojo» (`0000001001001001b`). En la esquina de abajo (bits 0 a 2), el rojo es el bit 0 y el verde el bit 2: hay que apagar el bit 0 y prender el bit 2. Queda `0000001001001100b`.

#### Desafío
Completá el binario, para que la esquina de abajo quede en verde y las otras tres en rojo.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 0000001001001001b   ; todo en rojo
    out 4, ax
    mov ax, ___                    ; verde abajo
    out 4, ax

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
word puerto 4 = 024Ch
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

    mov ax, 0000001001001001b   ; todo en rojo
    out 4, ax
    mov ax, 0000001001001100b   ; verde abajo
    out 4, ax

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
La esquina de abajo se pone en verde y los carros de carbón avanzan. Las otras tres siguen en rojo. —Tres bits por esquina —dice Nova—. Como los interruptores de la cintura.

#### Imagen
- Un semáforo de bronce de cuatro caras en un cruce de piedra de noche: una cara con luz verde y tres con luz roja, y carros de carbón avanzando.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) hace señas a los carros para que pasen.
- Gheco (gecko de luz cian con antiparras, chiquito) sentado arriba del semáforo, con una banderita verde.

### Micro-misión S01-N03-P3 · El amarillo, con tiempo

```meta
lugar: La encrucijada de las Forjas
personajes: Nova, Gheco, Kira
carta: INT 15h, 86h | espera CX:DX microsegundos · 1 segundo = 000F4240h · como sleep o delay
recompensa: xp 15, oro 15
```

#### Escena
El verde no puede pasar a rojo de golpe: los carros necesitan el **amarillo** un ratito. Kira propone: verde, esperar un segundo, amarillo, esperar otro segundo, rojo.

#### Gheco sugiere
La BIOS espera con **`INT 15h`**, función **86h**: CX:DX microsegundos. Un segundo es un millón: `000F4240h`, así que CX = `0Fh` y DX = `4240h`. En el tablero no hay que esperar de verdad: el reloj del Gólem salta ese tiempo.

#### Desafío
Completá la segunda espera de un segundo (entre el amarillo y el rojo), igual que la primera. Al terminar, el semáforo tiene que quedar todo en rojo.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 0000001001001100b      ; verde abajo
    out 4, ax
    mov cx, 0Fh                    ; esperar un segundo
    mov dx, 4240h
    mov ah, 86h
    int 15h
    mov ax, 0000001001001010b      ; amarillo abajo
    out 4, ax
    mov cx, 0Fh                    ; esperar otro segundo
    mov dx, ___
    mov ah, ___
    int ___
    mov ax, 0000001001001001b      ; todo en rojo
    out 4, ax

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
word puerto 4 = 0249h
DX = 4240h
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

    mov ax, 0000001001001100b      ; verde abajo
    out 4, ax
    mov cx, 0Fh                    ; esperar un segundo
    mov dx, 4240h
    mov ah, 86h
    int 15h
    mov ax, 0000001001001010b      ; amarillo abajo
    out 4, ax
    mov cx, 0Fh                    ; esperar otro segundo
    mov dx, 4240h
    mov ah, 86h
    int 15h
    mov ax, 0000001001001001b      ; todo en rojo
    out 4, ax

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Verde, amarillo, rojo, con su tiempo. Los carros frenan sin chocar. Kira aplaude desde la vereda. —Ahora sí es un semáforo —dice.

#### Imagen
- Un semáforo de bronce de cuatro caras en un cruce de piedra de noche, con la luz amarilla encendida en una cara, y un reloj de arena de bronce flotando al lado.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) aplaude desde la vereda.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) da vuelta el reloj de arena.
- Gheco (gecko de luz cian con antiparras, chiquito) sentado arriba del semáforo.

### Micro-misión S01-N03-P4 · La tabla del semáforo

```meta
lugar: La encrucijada de las Forjas
personajes: Nova, Gheco
carta: Tabla de situaciones | situaciones dw ... · recorrer con [si] y add si, 2 (o lodsw) · out 4, ax en cada vuelta
recompensa: xp 20, oro 20
```

#### Escena
Kira anotó las cuatro situaciones del cruce en una tabla: rojo para todos, verde abajo, amarillo abajo y verde a la derecha. Nova quiere que el Gólem las recorra solo, una tras otra.

#### Gheco sugiere
Las situaciones son words seguidos en `.data`. Con `lea si, situaciones` y un `loop` de 4 vueltas: en cada vuelta, `mov ax, [si]`, `out 4, ax` y `add si, 2` (cada situación ocupa 2 cajones).

#### Desafío
Completá las tres órdenes del bucle (donde dice `; tus órdenes`), para que el semáforo pase por las cuatro situaciones y termine con verde a la derecha (`0261h`).

#### Código inicial
```asm
.model small
.stack 100h
.data
situaciones dw 0000001001001001b   ; todo en rojo
            dw 0000001001001100b   ; verde abajo
            dw 0000001001001010b   ; amarillo abajo
            dw 0000001001100001b   ; verde a la derecha
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, situaciones
    mov cx, 4
paso:
    ; tus órdenes
    loop paso

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
word puerto 4 = 0261h
```

#### Solución
```asm
.model small
.stack 100h
.data
situaciones dw 0000001001001001b   ; todo en rojo
            dw 0000001001001100b   ; verde abajo
            dw 0000001001001010b   ; amarillo abajo
            dw 0000001001100001b   ; verde a la derecha
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, situaciones
    mov cx, 4
paso:
    mov ax, [si]
    out 4, ax
    add si, 2
    loop paso

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El semáforo pasa por las cuatro situaciones y queda en verde para los de la derecha. Con el paso a paso, Nova ve cada situación encenderse en el tablero. —Una tabla y un bucle —dice—. Y el cruce se maneja solo.

#### Imagen
- Una tabla de bronce con cuatro filas de lucecitas de colores, al lado de un semáforo de bronce de cuatro caras en un cruce de piedra de noche.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) recorre la tabla con el dedo.
- Gheco (gecko de luz cian con antiparras, chiquito) salta de fila en fila sobre la tabla.

### Prueba del sello

#### ¿Qué bits usa la esquina de abajo del semáforo?
Del 0 al 2: rojo el 0, amarillo el 1 y verde el 2.

#### ¿Cómo se espera un segundo con la BIOS?
`INT 15h` con AH = 86h y CX:DX = 000F4240h (un millón de microsegundos).

## S01-N04 · El termostato del horno

```meta
tipo: tema
padre: S01-N03
precio: 0
criatura: ogre
temas: maq.saltos, prog.condiciones
```

### Crónica

El horno grande de las Forjas tiene que estar **entre 60 y 80 grados**: más frío, el bronce no se funde; más caliente, se arruinan los moldes. El horno tiene un termómetro y un calefactor, y alguien tiene que mirarlo todo el día. —O un programa —dice Nova.

### Objetivos

Leer la temperatura del termómetro de emu8086 (puerto 125, con signo), prender y apagar el calefactor (puerto
127: 1 prendido, 0 apagado) y escribir un **termostato**: un bucle que mira y decide, para siempre.

### Antes de empezar

- `in` y `out` (Los nervios del Gólem).
- `cmp`, `jl`, `jg` y el if/else (Dos caminos; Con signo y sin signo).
- Bucles (Repetir; Mientras y hasta que).

### Explicación

#### El termómetro y el calefactor
| Puerto | Qué es |
|---|---|
| 125 | la temperatura, en grados, con signo (`in al, 125`) |
| 127 | el calefactor: `out 127, al` con 1 lo prende y con 0 lo apaga |

El horno empieza **frío** (a la temperatura del aire, 0°). Con el calefactor prendido, la temperatura sube; apagado,
baja despacio. El tiempo es el reloj del Gólem: cada vuelta de un bucle lo hace avanzar.

#### Un termostato
Un termostato es un bucle que nunca termina: mira la temperatura y decide.

```asm
vuelta:
    in al, 125
    cmp al, 60
    jl prender          ; si está fría, prender
    cmp al, 80
    jg apagar           ; si está muy caliente, apagar
    jmp vuelta          ; si está bien, no tocar nada
prender:
    mov al, 1
    out 127, al
    jmp vuelta
apagar:
    mov al, 0
    out 127, al
    jmp vuelta
```

Así es el ejemplo de emu8086 (`thermometer.asm`). En las micro-misiones el bucle da una cantidad fija de vueltas,
para que termine.

> **Puente con otras lenguas.** Es el `while True:` con un `if` adentro que controla cualquier aparato: una
> heladera, el aire acondicionado, el control de un horno en Arduino. Que la temperatura no salte entre
> «prendido» y «apagado» a cada rato (tener un margen de 60 a 80) se llama **histéresis**, y se usa en todos los
> termostatos reales.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
t db 'El horno llego a 60 grados$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 1
    out 127, al         ; prender el calefactor
calentar:
    in al, 125
    cmp al, 60
    jl calentar         ; esperar a que llegue a 60
    mov al, 0
    out 127, al         ; apagar

    lea dx, t
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

### Salida esperada

```
El horno llego a 60 grados
```

### ¿Para qué sirve?

Casi todo lo automático funciona así: leer un sensor, comparar y actuar. Heladeras, hornos, invernaderos, el
control de velocidad de un auto, los drones que se mantienen en el aire. Es la primera idea de la **robótica** y
del **control automático**.

### Errores habituales

**Ogro: el `jl` que debió ser `jb`, o al revés.** La temperatura puede ser negativa: se compara con signo (`jl`,
`jg`).

**Ogro: prender y nunca apagar.** Sin la rama de «apagar», el horno sube hasta el máximo.

**Ogro: el bucle que no vuelve a leer.** Si el `in` queda afuera del bucle, el programa mira siempre la misma
temperatura vieja.

### Micro-misión S01-N04-P1 · ¿Qué temperatura hay?

```meta
lugar: El horno de las Forjas
personajes: Nova, Gheco, Kira
carta: Termómetro (125) | in al, 125 · la temperatura en grados, con signo · el horno empieza frío (0°)
recompensa: xp 15, oro 15
```

#### Escena
Antes de prender nada, Nova quiere saber cómo está el horno. Kira le alcanza el cable del termómetro: puerto **125**.

#### Gheco sugiere
`in al, 125` trae la temperatura a AL. El horno está apagado desde anoche, así que está a la temperatura del aire: **0** grados. Guardala en BL para no perderla.

#### Desafío
Completá la orden que lee el termómetro, para que BL quede con la temperatura (0) y el calefactor siga apagado.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 99          ; todavía no leyó
    ___ al, 125
    mov bl, al

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
BL = 0
puerto 127 = 0
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

    mov al, 99          ; todavía no leyó
    in al, 125
    mov bl, al

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
BL = 0: el horno está helado. En la solapa de aparatos, el termómetro marca 0° y el calefactor está apagado. —Hay que calentarlo —dice Kira.

#### Imagen
- Un horno enorme de piedra y bronce apagado en una forja de noche, con un termómetro de bronce grande al costado cuya columna cian está abajo de todo.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) se frota las manos por el frío.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) mira el termómetro.
- Gheco (gecko de luz cian con antiparras, chiquito) se abraza a la columna del termómetro, tiritando.

### Micro-misión S01-N04-P2 · Calentar hasta 60

```meta
lugar: El horno de las Forjas
personajes: Nova, Gheco
carta: Calefactor (127) | out 127, al con 1 prende y con 0 apaga · esperar en un bucle: in, cmp, jl
recompensa: xp 15, oro 15
```

#### Escena
Para fundir bronce, el horno tiene que llegar a **60** grados. Nova prende el calefactor… y tiene que esperar mirando el termómetro.

#### Gheco sugiere
Primero `mov al, 1` y `out 127, al` para prender el calefactor. Después, un bucle que lee la temperatura y vuelve mientras sea menor a 60: `in al, 125`, `cmp al, 60`, `jl calentar`. Cuando sale del bucle, AL tiene 60.

#### Desafío
Completá el puerto del calefactor y el salto del bucle, para que el horno llegue a **60** grados (AL = 60) con el calefactor prendido.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 1
    out ___, al         ; prender el calefactor
calentar:
    in al, 125
    cmp al, 60
    ___ calentar        ; volver mientras esté fría

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
AL = 60
puerto 127 = 1
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

    mov al, 1
    out 127, al         ; prender el calefactor
calentar:
    in al, 125
    cmp al, 60
    jl calentar         ; volver mientras esté fría

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El termómetro sube despacito hasta **60**. En el paso a paso se ve el bucle dar vueltas y vueltas mientras la columna crece. —El programa espera por mí —dice Nova.

#### Imagen
- Un horno de piedra y bronce encendido con fuego naranja en una forja de noche, con un termómetro de bronce cuya columna cian sube hasta la mitad.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) baja una palanca grande junto al horno.
- Gheco (gecko de luz cian con antiparras, chiquito) se calienta las patitas cerca del fuego, contento.

### Micro-misión S01-N04-P3 · El termostato

```meta
lugar: El horno de las Forjas
personajes: Nova, Gheco, Kira
criatura: ogre
carta: Termostato | en cada vuelta: fría (jl 60) → prender · muy caliente (jg 80) → apagar · si no, no tocar
recompensa: xp 20, oro 20
```

#### Escena
Kira deja a Nova a cargo del horno toda la tarde. Un ogro fundidor avisa, preocupado: —Si pasa de 80 se rajan los moldes. Y el programa de Nova solo sabe prender.

#### Gheco sugiere
El bucle ya prende el calefactor cuando la temperatura es menor a 60. Falta la otra mitad: si es **mayor a 80** (`cmp al, 80` y `jg apagar`), apagarlo con `mov al, 0` y `out 127, al`. Al final, el programa mide y dice si quedó entre 60 y 80.

#### Desafío
Escribí la rama que apaga el calefactor, donde dice `; tus órdenes`, para que al terminar el ojo diga `Entre 60 y 80`.

#### Código inicial
```asm
.model small
.stack 100h
.data
t_bien db 'Entre 60 y 80$'
t_mal  db 'Fuera de rango$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov cx, 30000       ; toda la tarde
vuelta:
    in al, 125
    cmp al, 60
    jl prender
    ; tus órdenes
    jmp sigue
prender:
    mov al, 1
    out 127, al
sigue:
    loop vuelta

    in al, 125          ; ¿cómo quedó?
    cmp al, 60
    jl fuera
    cmp al, 80
    jg fuera
    lea dx, t_bien
    jmp mostrar
fuera:
    lea dx, t_mal
mostrar:
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
Entre 60 y 80
```

#### Solución
```asm
.model small
.stack 100h
.data
t_bien db 'Entre 60 y 80$'
t_mal  db 'Fuera de rango$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov cx, 30000       ; toda la tarde
vuelta:
    in al, 125
    cmp al, 60
    jl prender
    cmp al, 80
    jg apagar
    jmp sigue
apagar:
    mov al, 0
    out 127, al
    jmp sigue
prender:
    mov al, 1
    out 127, al
sigue:
    loop vuelta

    in al, 125          ; ¿cómo quedó?
    cmp al, 60
    jl fuera
    cmp al, 80
    jg fuera
    lea dx, t_bien
    jmp mostrar
fuera:
    lea dx, t_mal
mostrar:
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
«Entre 60 y 80». El horno se pasa la tarde subiendo y bajando entre los dos números, sin pasarse nunca. El ogro fundidor se va a dormir la siesta, tranquilo.

#### Imagen
- Un horno de piedra y bronce con fuego tranquilo en una forja de noche, con un termómetro de bronce cuya columna cian está entre dos marcas lisas.
- Un ogro grandote y torpe, con delantal de cuero cerrado, se acomoda para dormir la siesta en un banco.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) le choca los cinco a Nova.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) sonríe; Gheco (gecko de luz cian con antiparras, chiquito) duerme sobre el termómetro.

### Prueba del sello

#### ¿Qué puertos usa el termómetro de emu8086?
El 125 para leer la temperatura y el 127 para prender (1) o apagar (0) el calefactor.

#### ¿Qué hace un termostato?
Mira la temperatura en un bucle: si está fría prende el calefactor, si está muy caliente lo apaga y, si no, no toca nada.

## S01-N05 · La grúa del puerto de carga

```meta
tipo: tema
padre: S01-N04
precio: 0
criatura: goblin
temas: prog.bits, maq.saltos
```

### Crónica

La grúa que sube los bloques de bronce a los carros se mueve con un **motor paso a paso**: tres imanes que, prendidos en el orden justo, hacen girar el eje un poquito por vez. Desde que se fue el grúista, nadie sabe en qué orden prenderlos. El motor está en el puerto **7**.

### Objetivos

Manejar el motor paso a paso de emu8086 (puerto 7): prender sus tres imanes con los bits 0, 1 y 2, esperar a que
esté listo mirando el bit 7 al leer el puerto, y hacerlo girar con una tabla de pasos.

### Antes de empezar

- Bits y `test` (Bits y máscaras).
- `in` y `out` (Los nervios del Gólem).
- Arreglos de bytes y `loop` (Arreglos e índices).

### Explicación

#### Tres imanes
El motor tiene tres imanes, uno por bit del puerto 7 (bits 0, 1 y 2). El eje gira hacia el imán prendido. Si se
prenden en orden, gira: `001b` → `011b` → `010b` → `110b` son tres **medios pasos** en el sentido de las agujas
del reloj (el ejemplo de emu8086).

#### Esperar a que esté listo
El motor es mecánico: tarda un instante en moverse. Si le mandás otro paso antes, lo pierde. Al **leer** el puerto
7, el bit 7 dice si está listo (1) o todavía moviéndose (0):

```asm
espera:
    in al, 7
    test al, 10000000b  ; ¿bit 7 en 1?
    jz espera           ; todavía no: esperar
```

> **Puente con otras lenguas.** Esperar mirando un bit hasta que el aparato esté listo se llama **sondeo**
> (*polling*): es lo que hace un `while (!listo) {}` en C para Arduino. Los motores paso a paso mueven las
> impresoras 3D, los escáneres y los brazos robóticos.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
pasos db 001b, 011b, 010b, 110b
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, pasos
    mov cx, 4
paso:
espera:
    in al, 7
    test al, 10000000b
    jz espera           ; esperar a que esté listo
    mov al, [si]
    out 7, al           ; el próximo paso
    inc si
    loop paso

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

### ¿Para qué sirve?

Los motores paso a paso están en las impresoras (comunes y 3D), en los lectores de discos, en las cámaras de
seguridad que giran y en los robots. Y la idea de esperar a que un aparato esté listo antes de mandarle lo
siguiente está en toda comunicación con hardware: impresoras, discos, redes.

### Errores habituales

**Ogro: no esperar.** Mandar los pasos seguidos, sin mirar el bit 7: el motor está ocupado y los pierde.

**Ogro: el `jz` al revés.** `test al, 80h` + `jz` vuelve mientras el bit 7 está en **0** (ocupado). Con `jnz`, el
programa esperaría justo cuando está listo.

**Goblin: el orden de los imanes.** Saltar de `001b` a `110b` no hace girar: hay que pasar por los del medio.

### Micro-misión S01-N05-P1 · El primer paso

```meta
lugar: El puerto de carga
personajes: Nova, Gheco
carta: Motor paso a paso (7) | bits 0, 1 y 2 = los tres imanes · out 7, al · el eje gira hacia el imán prendido
recompensa: xp 15, oro 15
```

#### Escena
La grúa está quieta. Nova prueba prender el **primer** imán, a ver si el eje se mueve.

#### Gheco sugiere
Cada imán es un bit del puerto 7. El primero es el bit 0: `mov al, 001b` y `out 7, al`. En la solapa de aparatos vas a ver el imán prenderse en rojo.

#### Desafío
Completá la orden que manda el paso al motor, para que el puerto 7 quede con `001b`.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 001b
    ___ 7, al

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
puerto 7 = 1
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

    mov al, 001b
    out 7, al

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
*Clac*. El eje de la grúa da un saltito. —Se mueve —dice Nova—. Ahora, en orden.

#### Imagen
- Una grúa de bronce en un puerto de carga de noche, con un motor redondo a la vista: tres imanes, uno encendido en rojo.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) mira el motor de cerca.
- Gheco (gecko de luz cian con antiparras, chiquito) sentado sobre el gancho de la grúa.

### Micro-misión S01-N05-P2 · Esperar a la grúa

```meta
lugar: El puerto de carga
personajes: Nova, Gheco
criatura: goblin
carta: Listo (bit 7) | in al, 7 · test al, 80h · jz espera: vuelve mientras está ocupado · polling
recompensa: xp 15, oro 15
```

#### Escena
Nova manda dos pasos seguidos y el segundo se pierde: la grúa todavía se estaba moviendo. Un goblin se ríe colgado del gancho.

#### Gheco sugiere
Al **leer** el puerto 7, el bit 7 dice si el motor está listo. Antes de cada paso: `in al, 7`, `test al, 10000000b` y `jz espera` (vuelve mientras el bit 7 esté en 0).

#### Desafío
Completá la espera antes del segundo paso, para que el puerto 7 termine con `011b`.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 001b
    out 7, al           ; primer paso
espera:
    in al, 7
    test al, ___
    ___ espera          ; volver mientras esté ocupado
    mov al, 011b
    out 7, al           ; segundo paso

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
puerto 7 = 3
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

    mov al, 001b
    out 7, al           ; primer paso
espera:
    in al, 7
    test al, 10000000b
    jz espera           ; volver mientras esté ocupado
    mov al, 011b
    out 7, al           ; segundo paso

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Dos pasos, sin perder ninguno. El goblin se cae del gancho por el envión. —Primero pregunto si está lista —dice Nova—, después le pido.

#### Imagen
- Una grúa de bronce girando un poquito en un puerto de carga de noche, con dos imanes encendidos en rojo en su motor.
- Un goblin verde y flaco de caricatura, con ropa de tela cerrada, cayéndose del gancho de la grúa.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) espera con los brazos cruzados, paciente.
- Gheco (gecko de luz cian con antiparras, chiquito) mira un relojito de bolsillo.

### Micro-misión S01-N05-P3 · La vuelta de la grúa

```meta
lugar: El puerto de carga
personajes: Nova, Gheco, Kira
carta: Tabla de pasos | pasos db 001b, 011b, 010b, 110b · esperar listo · out 7 · inc si · loop
recompensa: xp 20, oro 20
```

#### Escena
Kira necesita que la grúa gire para subir un bloque al carro: los **cuatro** medios pasos de la tabla, uno tras otro, esperando a la grúa en cada uno.

#### Gheco sugiere
Recorré la tabla con SI: en cada vuelta, esperá a que el motor esté listo, mandá `[si]` al puerto 7 e `inc si`. Es el ejemplo de emu8086 (`stepper_motor.asm`), en chico.

#### Desafío
Escribí el cuerpo del bucle, donde dice `; tus órdenes`, para que la grúa dé los cuatro pasos y el puerto 7 termine con `110b`.

#### Código inicial
```asm
.model small
.stack 100h
.data
pasos db 001b, 011b, 010b, 110b
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, pasos
    mov cx, 4
paso:
    ; tus órdenes
    loop paso

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
puerto 7 = 6
```

#### Solución
```asm
.model small
.stack 100h
.data
pasos db 001b, 011b, 010b, 110b
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, pasos
    mov cx, 4
paso:
espera:
    in al, 7
    test al, 10000000b
    jz espera
    mov al, [si]
    out 7, al
    inc si
    loop paso

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
La grúa gira suave, levanta el bloque de bronce y lo deja en el carro. Kira silba desde abajo. —Cuatro imanes en orden —dice Nova—, y la grúa baila.

#### Imagen
- Una grúa de bronce levantando un bloque de bronce brillante hacia un carro, en un puerto de carga de noche.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) silba desde abajo, con los dedos en la boca.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) maneja la grúa desde una cabina de bronce.
- Gheco (gecko de luz cian con antiparras, chiquito) viaja parado sobre el bloque.

### Prueba del sello

#### ¿Cómo se sabe si el motor está listo para otro paso?
Leyendo el puerto 7: si el bit 7 está en 1, está listo.

#### ¿Por qué hay que esperar entre paso y paso?
Porque el motor tarda en moverse: si le llega otro paso mientras está ocupado, lo pierde.

## S01-N06 · La impresora del Gremio

```meta
tipo: tema
padre: S01-N05
precio: 0
criatura: goblin
temas: prog.cadenas, maq.interrupciones
```

### Crónica

El Gremio tiene una impresora de tipos de bronce que imprime los recibos de las carreras. Hace años que no imprime nada, y los recibos se escriben a mano. Su cable va al puerto **130**.

### Objetivos

Imprimir en la impresora de emu8086: un carácter con la función 05h de DOS o con `out 130, al`, un texto entero
recorriéndolo con un bucle, y los caracteres especiales (Enter, tabulación y hoja nueva).

### Antes de empezar

- `out` (Los nervios del Gólem).
- Recorrer un texto con `[si]` o `lodsb` (Arreglos e índices; Las órdenes de fila).

### Explicación

#### Dos formas de imprimir
| Forma | Cómo |
|---|---|
| DOS, función 05h | `mov dl, 'A'`, `mov ah, 05h`, `int 21h` (lo que usa el ejemplo de emu8086) |
| Directo al puerto | `mov al, 'A'` y `out 130, al` |

La impresora no tiene `$` ni función 09h: se imprime **carácter por carácter**, con un bucle. Algunos caracteres
son órdenes: **13** vuelve al principio del renglón, **10** baja un renglón, **9** es una tabulación y **12** saca
la hoja y empieza una nueva.

Lo que imprime aparece en la solapa de aparatos y, en la salida, debajo de `── Impresora ──`.

> **Puente con otras lenguas.** En C, `fputc(c, stdprn)` mandaba un carácter a la impresora en DOS; hoy se manda
> un archivo entero al sistema operativo. El `\f` de C, Python y Java (el carácter 12, *form feed*) existe
> justamente para pedirle hoja nueva a una impresora.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
recibo db 'Recibo del Gremio', 13, 10, 'Carrera ganada', 0
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, recibo
imprimir:
    mov dl, [si]
    cmp dl, 0
    je listo            ; el 0 marca el final
    mov ah, 05h
    int 21h             ; a la impresora
    inc si
    jmp imprimir
listo:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

### Salida esperada

```
── Impresora ──
Recibo del Gremio
Carrera ganada
```

### ¿Para qué sirve?

Las impresoras de tickets de los comercios, las de etiquetas y las de los cajeros se siguen manejando así: un
carácter por vez, con caracteres especiales para cortar el papel o cambiar de renglón. Y la idea de terminar un
texto con un 0 (en vez de `$`) es la que usa C en todos sus textos.

### Errores habituales

**Ogro: usar la función 09h.** La 09h es para la pantalla; a la impresora se le manda de a un carácter.

**Ogro: el texto sin final.** Si el texto no tiene una marca de fin (un 0, o una cantidad fija), el bucle imprime
toda la memoria.

**Goblin: el 13 sin el 10.** El 13 vuelve al principio del renglón pero no baja: sin el 10, escribe encima.

### Micro-misión S01-N06-P1 · La primera letra

```meta
lugar: El salón del Gremio
personajes: Nova, Gheco, Kira
carta: Impresora | mov dl, 'K' · mov ah, 05h · int 21h · o mov al, 'K' y out 130, al
recompensa: xp 15, oro 15
```

#### Escena
Kira sopla el polvo de la impresora del Gremio. —Probá con una letra —dice—. La mía.

#### Gheco sugiere
La función **05h** de DOS manda el carácter de DL a la impresora: `mov dl, 'K'`, `mov ah, 05h` e `int 21h`. Es como la 02h, pero va al papel.

#### Desafío
Completá la función de DOS, para que la impresora imprima una **K**.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov dl, 'K'
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
── Impresora ──
K
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

    mov dl, 'K'
    mov ah, 05h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
La impresora tose, el carro se mueve, y una **K** de tinta aparece en el papel. Kira lo arranca y se lo guarda en el bolsillo, como un trofeo.

#### Imagen
- Una impresora antigua de tipos de bronce sobre una mesa de piedra del Gremio, con una hoja de papel saliendo, lisa, con una sola marca de tinta.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) sopla el polvo de la impresora.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) mira el papel salir.
- Gheco (gecko de luz cian con antiparras, chiquito) sentado sobre la impresora.

### Micro-misión S01-N06-P2 · El recibo

```meta
lugar: El salón del Gremio
personajes: Nova, Gheco
carta: Imprimir un texto | recorrer con [si] hasta el 0 · out 130, al en cada letra · sin $ ni 09h
recompensa: xp 15, oro 15
```

#### Escena
El primer recibo del Gremio en años: «Pagado: 5 chispas». La impresora no entiende de `$`: hay que mandarle letra por letra.

#### Gheco sugiere
El texto termina en **0**. Recorrelo con SI: en cada vuelta, `mov al, [si]`; si es 0, terminaste; si no, `out 130, al` (directo a la impresora) e `inc si`.

#### Desafío
Completá la orden que manda la letra a la impresora, para que se imprima el recibo.

#### Código inicial
```asm
.model small
.stack 100h
.data
recibo db 'Pagado: 5 chispas', 0
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, recibo
letra:
    mov al, [si]
    cmp al, 0
    je listo
    out ___, al
    inc si
    jmp letra
listo:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
── Impresora ──
Pagado: 5 chispas
```

#### Solución
```asm
.model small
.stack 100h
.data
recibo db 'Pagado: 5 chispas', 0
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, recibo
letra:
    mov al, [si]
    cmp al, 0
    je listo
    out 130, al
    inc si
    jmp letra
listo:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El recibo sale entero, con su tinta todavía húmeda. —Letra por letra —dice Nova—, como cuando aprendí a mostrar mi primer texto.

#### Imagen
- Una impresora antigua de tipos de bronce imprimiendo una tira de papel larga y lisa (sin letras legibles), en un salón de piedra.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) sostiene la punta del papel que sale.
- Gheco (gecko de luz cian con antiparras, chiquito) se envuelve en la tira de papel, jugando.

### Micro-misión S01-N06-P3 · Dos renglones y hoja nueva

```meta
lugar: El salón del Gremio
personajes: Nova, Gheco, Kira
carta: Caracteres de la impresora | 13 = principio del renglón · 10 = renglón nuevo · 12 = hoja nueva · 9 = tabulación
recompensa: xp 20, oro 20
```

#### Escena
Kira quiere el recibo en dos renglones, «Gremio» arriba y «Gracias» abajo, y que después la impresora saque la hoja para el próximo.

#### Gheco sugiere
Entre los dos renglones van el **13** (volver al principio) y el **10** (bajar un renglón). Al final, el **12** saca la hoja. Son bytes como cualquier otro: van en el texto, entre comas.

#### Desafío
Completá los dos bytes que separan los renglones y el byte de hoja nueva, en la declaración del texto.

#### Código inicial
```asm
.model small
.stack 100h
.data
recibo db 'Gremio', ___, ___, 'Gracias', ___, 0
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, recibo
letra:
    mov al, [si]
    cmp al, 0
    je listo
    out 130, al
    inc si
    jmp letra
listo:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
── Impresora ──
Gremio
Gracias
----- (hoja nueva) -----
```

#### Solución
```asm
.model small
.stack 100h
.data
recibo db 'Gremio', 13, 10, 'Gracias', 12, 0
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, recibo
letra:
    mov al, [si]
    cmp al, 0
    je listo
    out 130, al
    inc si
    jmp letra
listo:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Dos renglones, y la hoja sale sola. Kira la cuelga en la pared del Gremio. —El primer recibo impreso del Gremio en diez años —dice, orgullosa.

#### Imagen
- Una hoja de papel lisa colgada en la pared de piedra del Gremio con un clavo, y abajo una impresora antigua de bronce.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) cuelga la hoja, orgullosa.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) aplaude.
- Gheco (gecko de luz cian con antiparras, chiquito) sentado sobre la impresora, con una gorrita de papel.

### Prueba del sello

#### ¿Cómo se manda un carácter a la impresora?
Con la función 05h de DOS (`mov dl, c`, `mov ah, 05h`, `int 21h`) o directo con `out 130, al`.

#### ¿Qué hacen los caracteres 13, 10 y 12 en la impresora?
El 13 vuelve al principio del renglón, el 10 baja uno y el 12 saca la hoja.

## S01-N07 · El robot de las minas

```meta
tipo: tema
padre: S01-N06
precio: 0
criatura: goblin
temas: maq.saltos, prog.funciones
```

### Crónica

En las minas de las Forjas trabaja un robot de bronce chiquito que prende y apaga las lámparas de los túneles. Desde que se perdió su control remoto, se quedó quieto en la entrada, mirando al este. Sus cables van a los puertos **9**, **10** y **11**.

### Objetivos

Manejar el robot de emu8086: mandarle órdenes por el puerto 9, esperar a que termine mirando el estado (puerto 11),
leer lo que examinó (puerto 10) y armar un recorrido con una rutina que espera y manda.

### Antes de empezar

- `in`, `out` y la espera mirando un bit (Los nervios del Gólem; La grúa del puerto de carga).
- Rutinas con `call` y `ret` (Las rutinas).

### Explicación

#### Tres puertos
| Puerto | Qué es |
|---|---|
| 9 | la **orden**: 0 nada, 1 avanzar, 2 girar a la izquierda, 3 girar a la derecha, 4 examinar lo que tiene adelante, 5 prender la lámpara de adelante, 6 apagarla |
| 10 | el **dato** que dejó «examinar»: 255 pared, 0 nada, 7 lámpara prendida, 8 lámpara apagada |
| 11 | el **estado**: bit 0 = hay un dato nuevo, bit 1 = está ocupado, bit 2 = la última orden falló |

El robot es mecánico: cada orden le lleva un rato. Si le llega otra mientras está **ocupado** (bit 1 del estado),
la rechaza. Por eso, antes de cada orden, hay que esperar:

```asm
orden proc              ; manda la orden de AL, cuando el robot esté libre
    push ax
ocupado:
    in al, 11
    test al, 00000010b  ; ¿bit 1 (ocupado)?
    jnz ocupado
    pop ax
    out 9, al
    ret
orden endp
```

Lo que hace el robot aparece en la salida, debajo de `── Robot ──`, y en la solapa de aparatos se ve el mapa de la
mina: `#` pared, `*` lámpara prendida, `o` apagada, y el robot como una flecha.

> **Puente con otras lenguas.** Es la misma idea que programar un robot de juguete o una tortuga de Logo:
> «avanzar, girar, mirar». La rutina `orden` es una **función** que esconde el detalle (esperar) y deja el
> programa principal leyéndose como una lista de pasos.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 1           ; avanzar
    call orden
    mov al, 3           ; girar a la derecha
    call orden

fin:
    mov ax, 4C00h
    int 21h
main endp

orden proc
    push ax
ocupado:
    in al, 11
    test al, 00000010b
    jnz ocupado
    pop ax
    out 9, al
    ret
orden endp
end main
```

### Salida esperada

```
── Robot ──
avanza a (2, 1)
gira a la derecha: mira al sur
```

### ¿Para qué sirve?

Así se programan los robots de verdad: órdenes simples, esperar a que terminen, mirar los sensores y decidir. Los
robots de los depósitos, las aspiradoras automáticas y los vehículos de Marte trabajan con estas mismas ideas.

### Errores habituales

**Ogro: órdenes seguidas sin esperar.** El robot está ocupado y rechaza la orden: en la salida aparece
`¡ocupado! (no tomó la orden)`.

**Ogro: leer el dato antes de tiempo.** Después de «examinar», hay que esperar el bit 0 del estado antes de leer el
puerto 10.

**Ogro: avanzar contra una pared.** El robot no se mueve y prende el bit 2 del estado (error).

### Micro-misión S01-N07-P1 · Un paso adelante

```meta
lugar: Las minas de las Forjas
personajes: Nova, Gheco, Kira
carta: Robot (puerto 9) | 1 avanzar · 2 girar a la izquierda · 3 a la derecha · 4 examinar · 5 prender · 6 apagar
recompensa: xp 15, oro 15
```

#### Escena
El robotito de las minas está quieto en la entrada, mirando al este. Kira le conecta el cable al puerto **9**. —Probá que camine —dice.

#### Gheco sugiere
Al puerto 9 se le manda la **orden**: el 1 es «avanzar». `mov al, 1` y `out 9, al`. Abajo de la salida va a aparecer lo que hizo el robot.

#### Desafío
Completá la orden que manda AL al robot, para que avance un lugar.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 1           ; avanzar
    ___ 9, al

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
── Robot ──
avanza a (2, 1)
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

    mov al, 1           ; avanzar
    out 9, al

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El robotito da un paso con un chirrido. Kira aplaude. En la solapa de aparatos, la flechita del robot se movió un lugar en el mapa de la mina.

#### Imagen
- La entrada de una mina de piedra con lámparas de bronce en las paredes, y un robot chiquito de bronce, con ruedas y un brazo, dando un paso.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) aplaude, agachada junto al robot.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) sostiene un cable fino conectado al robot.
- Gheco (gecko de luz cian con antiparras, chiquito) viaja sentado arriba del robot.

### Micro-misión S01-N07-P2 · Dos pasos, sin apuro

```meta
lugar: Las minas de las Forjas
personajes: Nova, Gheco
criatura: goblin
carta: Esperar al robot | in al, 11 · test al, 00000010b · jnz ocupado: vuelve mientras el bit 1 (ocupado) esté en 1
recompensa: xp 15, oro 15
```

#### Escena
Nova le manda dos pasos seguidos, pero el robot solo da uno: en la salida dice *«¡ocupado! (no tomó la orden)»*. Un goblin se ríe en el túnel.

#### Gheco sugiere
El robot tarda en dar cada paso. Mientras camina, el **bit 1** del estado (puerto 11) está en 1. Antes del segundo paso, esperá: `in al, 11`, `test al, 00000010b` y `jnz ocupado` (vuelve mientras esté ocupado).

#### Desafío
Tocá **Ejecutar** y mirá la salida. Después completá la espera antes del segundo paso, para que el robot avance dos lugares.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 1
    out 9, al           ; primer paso
ocupado:
    in al, 11
    test al, ___
    ___ ocupado         ; esperar mientras esté ocupado
    mov al, 1
    out 9, al           ; segundo paso

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
── Robot ──
avanza a (2, 1)
avanza a (3, 1)
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

    mov al, 1
    out 9, al           ; primer paso
ocupado:
    in al, 11
    test al, 00000010b
    jnz ocupado         ; esperar mientras esté ocupado
    mov al, 1
    out 9, al           ; segundo paso

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Dos pasos, uno detrás del otro. El goblin se queda sin chiste. —Igual que la grúa —dice Nova—: primero pregunto, después pido.

#### Imagen
- Un túnel de mina de piedra con lámparas de bronce, y un robot chiquito de bronce avanzando, con huellas detrás.
- Un goblin verde y flaco de caricatura, con ropa de tela cerrada, se ríe asomado detrás de una roca.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) acompaña al robot flotando a su lado.
- Gheco (gecko de luz cian con antiparras, chiquito) camina al lado del robot, imitando sus pasos.

### Micro-misión S01-N07-P3 · ¿Qué hay adelante?

```meta
lugar: Las minas de las Forjas
personajes: Nova, Gheco
carta: Examinar | orden 4 · esperar el bit 0 del estado (hay dato) · in al, 10: 255 pared, 0 nada, 7 lámpara prendida, 8 apagada
recompensa: xp 15, oro 15
```

#### Escena
El robot gira hacia el norte, y Nova quiere saber qué tiene adelante antes de mandarlo a caminar contra algo.

#### Gheco sugiere
La orden **4** es «examinar». Cuando termina, prende el **bit 0** del estado (hay un dato nuevo) y deja el resultado en el puerto **10**: 255 si es una pared. Esperá el bit 0 con `test al, 00000001b` y `jz` (vuelve mientras **no** haya dato), y después `in al, 10`.

#### Desafío
Completá la espera del dato, para que BL quede con lo que examinó el robot (una pared: `FFh`).

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 2           ; girar a la izquierda: mira al norte
    call orden
    mov al, 4           ; examinar
    call orden
dato:
    in al, 11
    test al, ___
    ___ dato            ; esperar mientras no haya dato
    in al, 10
    mov bl, al

fin:
    mov ax, 4C00h
    int 21h
main endp

orden proc
    push ax
ocupado:
    in al, 11
    test al, 00000010b
    jnz ocupado
    pop ax
    out 9, al
    ret
orden endp
end main
```

#### Salida esperada
```
── Robot ──
gira a la izquierda: mira al norte
examina: pared
```

#### Estado esperado
```
BL = FFh
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

    mov al, 2           ; girar a la izquierda: mira al norte
    call orden
    mov al, 4           ; examinar
    call orden
dato:
    in al, 11
    test al, 00000001b
    jz dato             ; esperar mientras no haya dato
    in al, 10
    mov bl, al

fin:
    mov ax, 4C00h
    int 21h
main endp

orden proc
    push ax
ocupado:
    in al, 11
    test al, 00000010b
    jnz ocupado
    pop ax
    out 9, al
    ret
orden endp
end main
```

#### Al superarla
BL = `FFh`: una pared. El robot no se chocó: miró antes. —Como Kira —dice Nova—: primero mira, después salta.

#### Imagen
- Un robot chiquito de bronce frente a una pared de roca de una mina, con un rayo de luz cian que sale de su ojo y la examina.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) espera detrás del robot.
- Gheco (gecko de luz cian con antiparras, chiquito) toca la pared con la patita.

### Micro-misión S01-N07-P4 · La lámpara del túnel

```meta
lugar: Las minas de las Forjas
personajes: Nova, Gheco, Kira
carta: Un recorrido | una orden por línea con call orden · girar, avanzar y prender (5) la lámpara de adelante
recompensa: xp 20, oro 20
```

#### Escena
Al sur de la entrada hay un túnel oscuro con una lámpara **apagada**. Kira necesita que el robot la prenda. Desde donde está (mirando al este): girar a la derecha, avanzar tres veces, girar a la izquierda… y la lámpara queda adelante.

#### Gheco sugiere
Con la rutina `orden`, cada paso es una línea: `mov al, número` y `call orden`. Las órdenes: 3 girar a la derecha, 1 avanzar, 2 girar a la izquierda y **5** prender la lámpara de adelante.

#### Desafío
Escribí el recorrido donde dice `; tus órdenes`, para que el robot prenda la lámpara del túnel.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    ; tus órdenes

fin:
    mov ax, 4C00h
    int 21h
main endp

orden proc
    push ax
ocupado:
    in al, 11
    test al, 00000010b
    jnz ocupado
    pop ax
    out 9, al
    ret
orden endp
end main
```

#### Salida esperada
```
── Robot ──
gira a la derecha: mira al sur
avanza a (1, 2)
avanza a (1, 3)
avanza a (1, 4)
gira a la izquierda: mira al este
prende la lámpara
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

    mov al, 3           ; girar a la derecha
    call orden
    mov al, 1           ; avanzar
    call orden
    mov al, 1
    call orden
    mov al, 1
    call orden
    mov al, 2           ; girar a la izquierda
    call orden
    mov al, 5           ; prender la lámpara
    call orden

fin:
    mov ax, 4C00h
    int 21h
main endp

orden proc
    push ax
ocupado:
    in al, 11
    test al, 00000010b
    jnz ocupado
    pop ax
    out 9, al
    ret
orden endp
end main
```

#### Al superarla
La lámpara del túnel se enciende y la mina se llena de luz cálida. Los mineros que esperaban afuera entran cantando. Kira abraza al robotito.

#### Imagen
- Un túnel de mina de piedra iluminándose con una lámpara de bronce recién encendida, con luz cálida.
- Un robot chiquito de bronce con el brazo estirado hacia la lámpara.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) abraza al robot, contenta.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) sonríe; Gheco (gecko de luz cian con antiparras, chiquito) sentado sobre la lámpara.

### Prueba del sello

#### ¿Por qué hay que esperar antes de cada orden al robot?
Porque mientras hace una orden está ocupado (bit 1 del puerto 11) y rechaza las nuevas.

#### ¿Cómo se lee lo que examinó el robot?
Esperando el bit 0 del puerto 11 (hay dato) y leyendo el puerto 10: 255 pared, 0 nada, 7 lámpara prendida, 8 apagada.

## S01-N08 · Jefe: el Goblin de los Cables

```meta
tipo: jefe
padre: S01-N07
precio: 0
criatura: goblin
insignia: Maestra de los Aparatos
insignia_descripcion: Venciste al Goblin de los Cables: el visor, el semáforo y la impresora te obedecen por los nervios del Gólem.
temas: maq.registros, prog.bits, maq.saltos
```

### Crónica

La noche de la gran carrera, un goblin se mete en el taller de aparatos y **cruza todos los cables**: el visor muestra cualquier cosa, el semáforo se queda en rojo y la impresora tira papel en blanco. La carrera empieza en minutos.

—Hay que arreglarlo todo en un solo programa —dice Kira—: la cuenta regresiva en el visor, el verde para los corredores y el recibo de largada.

### Objetivos

Combinar en un programa el visor, la espera de la BIOS, el semáforo y la impresora: cada aparato con su puerto, cada
paso en su orden.

### Antes de empezar

- El visor (199), el semáforo (4), la espera con `INT 15h` y la impresora (130).

### Explicación

#### Un programa, tres aparatos
El jefe se vence con lo que ya sabés, ordenado:

1. **Cuenta regresiva** en el visor: 3, 2, 1, con un segundo de espera entre cada número, y el 0 al final.
2. **Verde** para los corredores: la esquina de abajo en verde, las otras en rojo (`0000001001001100b`).
3. El **recibo** de largada en la impresora.

Cuando un programa maneja varios aparatos, conviene una **rutina** por tarea (esperar un segundo, imprimir un
texto), así el principal se lee como una lista de pasos.

> **Puente con otras lenguas.** Es un pequeño **sistema embebido**: el programa de un microcontrolador que
> coordina varios aparatos (un visor, unas luces, una impresora de tickets), como el de un surtidor de nafta o una
> máquina expendedora.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 0000001001001001b   ; todo en rojo
    out 4, ax
    mov ax, 9
    out 199, ax                 ; el visor, listo
    call segundo

fin:
    mov ax, 4C00h
    int 21h
main endp

segundo proc                    ; espera un segundo
    push ax
    push cx
    push dx
    mov cx, 0Fh
    mov dx, 4240h
    mov ah, 86h
    int 15h
    pop dx
    pop cx
    pop ax
    ret
segundo endp
end main
```

### ¿Para qué sirve?

Los aparatos de verdad casi nunca están solos: una máquina coordina luces, motores, visores e impresoras. Saber
ordenar los pasos y separar las tareas en rutinas es lo que permite programar algo grande sin perderse.

### Errores habituales

**Ogro: la cuenta regresiva sin esperas.** Los números pasan en un instante y nadie los ve.

**Ogro: CX pisado por la espera.** La espera usa CX: si el `loop` de la cuenta también usa CX, la rutina tiene que
guardarlo (`push cx` / `pop cx`).

**Goblin: el verde en la esquina equivocada.** El verde de abajo es el bit 2; el de la derecha, el 5.

### Micro-misión S01-N08-P1 · La cuenta regresiva

```meta
lugar: El taller de aparatos
personajes: Nova, Gheco, Kira
criatura: goblin
carta: Cuenta con espera | loop con CX: mostrar CX en el visor y call segundo · la rutina guarda CX
recompensa: xp 20, oro 20
```

#### Escena
El goblin dejó el visor mostrando números al azar. Lo primero: la cuenta regresiva de la largada, **3, 2, 1, 0**, con un segundo entre cada número.

#### Gheco sugiere
En el bucle: `mov ax, cx`, `out 199, ax` y `call segundo`. La rutina `segundo` guarda CX, así que el `loop` no se rompe. Después del bucle, el 0.

#### Desafío
Completá las tres órdenes del cuerpo del bucle (qué mostrar, dónde y qué rutina llamar), para que el visor cuente 3, 2, 1 con su espera y termine en 0.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 9999                ; lo que dejó el goblin
    out 199, ax
    mov cx, 3
cuenta:
    mov ax, ___
    out ___, ax
    call ___
    loop cuenta
    mov ax, 0
    out 199, ax

fin:
    mov ax, 4C00h
    int 21h
main endp

segundo proc
    push ax
    push cx
    push dx
    mov cx, 0Fh
    mov dx, 4240h
    mov ah, 86h
    int 15h
    pop dx
    pop cx
    pop ax
    ret
segundo endp
end main
```

#### Estado esperado
```
word puerto 199 = 0
CX = 0
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

    mov ax, 9999                ; lo que dejó el goblin
    out 199, ax
    mov cx, 3
cuenta:
    mov ax, cx
    out 199, ax
    call segundo
    loop cuenta
    mov ax, 0
    out 199, ax

fin:
    mov ax, 4C00h
    int 21h
main endp

segundo proc
    push ax
    push cx
    push dx
    mov cx, 0Fh
    mov dx, 4240h
    mov ah, 86h
    int 15h
    pop dx
    pop cx
    pop ax
    ret
segundo endp
end main
```

#### Al superarla
3… 2… 1… 0. El visor vuelve a obedecer. El goblin, que esperaba ver el caos, frunce el ceño y se esconde detrás del semáforo.

#### Imagen
- Un taller de aparatos de bronce de noche, con un visor grande de cifras rojas de luz en la pared y una maraña de cables cruzados.
- Un goblin verde y flaco de caricatura, con ropa de tela cerrada, se esconde detrás de un semáforo de bronce, frunciendo el ceño.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) cuenta con los dedos levantados.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) desenreda un cable; Gheco (gecko de luz cian con antiparras, chiquito) en su hombro.

### Micro-misión S01-N08-P2 · Verde y recibo

```meta
lugar: El taller de aparatos
personajes: Nova, Gheco
criatura: goblin
carta: Dos aparatos | out 4, ax con el verde de abajo · después el recibo a la impresora, letra por letra
recompensa: xp 20, oro 20
```

#### Escena
El semáforo de la largada sigue clavado en rojo y la impresora no imprime. El goblin cruzó los cables al revés.

#### Gheco sugiere
Primero el semáforo: verde abajo y rojo en las otras tres (`0000001001001100b`) al puerto 4. Después, el recibo: el texto termina en 0, y cada letra va a la impresora con `out 130, al`.

#### Desafío
Completá el número del verde y el puerto de la impresora, para que el semáforo dé verde a los corredores y se imprima `Largada!`.

#### Código inicial
```asm
.model small
.stack 100h
.data
recibo db 'Largada!', 0
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, ___                 ; verde abajo
    out 4, ax

    lea si, recibo
letra:
    mov al, [si]
    cmp al, 0
    je listo
    out ___, al
    inc si
    jmp letra
listo:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
── Impresora ──
Largada!
```

#### Estado esperado
```
word puerto 4 = 024Ch
```

#### Solución
```asm
.model small
.stack 100h
.data
recibo db 'Largada!', 0
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 0000001001001100b   ; verde abajo
    out 4, ax

    lea si, recibo
letra:
    mov al, [si]
    cmp al, 0
    je listo
    out 130, al
    inc si
    jmp letra
listo:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Verde para los corredores, y la impresora escupe el recibo de largada. El goblin se rasca la cabeza: le quedan pocos cables por cruzar.

#### Imagen
- Un semáforo de bronce con la luz verde encendida en una cara y una impresora antigua de bronce sacando una tira de papel lisa, en un taller de noche.
- Un goblin verde y flaco de caricatura, con ropa de tela cerrada, se rasca la cabeza con un cable en la mano.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) conecta un cable al semáforo.
- Gheco (gecko de luz cian con antiparras, chiquito) tira de la tira de papel.

### Micro-misión S01-N08-P3 · La gran largada

```meta
lugar: El taller de aparatos
personajes: Nova, Gheco, Kira, Axón
criatura: goblin
carta: Todo junto | rojo · cuenta 3, 2, 1, 0 con esperas · verde abajo · recibo «Largada!» a la impresora
recompensa: xp 30, oro 30
```

#### Escena
Faltan segundos para la carrera. El goblin cruza el último cable y apaga todo. Hay que hacerlo **todo junto**, en orden: todo en rojo, la cuenta regresiva, el verde y el recibo.

#### Gheco sugiere
Ya tenés todas las piezas. En orden:

1. `0000001001001001b` al puerto 4 (todo en rojo).
2. La cuenta regresiva en el visor: 3, 2, 1 con `call segundo` entre cada uno, y el 0.
3. `0000001001001100b` al puerto 4 (verde abajo).
4. El recibo, letra por letra, al puerto 130.

#### Desafío
Escribí el programa entero donde dice `; tus órdenes` (la rutina `segundo` ya está), para que la largada salga completa.

#### Código inicial
```asm
.model small
.stack 100h
.data
recibo db 'Largada!', 0
.code
main proc
    mov ax, @data
    mov ds, ax

    ; tus órdenes

fin:
    mov ax, 4C00h
    int 21h
main endp

segundo proc
    push ax
    push cx
    push dx
    mov cx, 0Fh
    mov dx, 4240h
    mov ah, 86h
    int 15h
    pop dx
    pop cx
    pop ax
    ret
segundo endp
end main
```

#### Salida esperada
```
── Impresora ──
Largada!
```

#### Estado esperado
```
word puerto 4 = 024Ch
word puerto 199 = 0
```

#### Solución
```asm
.model small
.stack 100h
.data
recibo db 'Largada!', 0
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 0000001001001001b   ; todo en rojo
    out 4, ax

    mov cx, 3
cuenta:
    mov ax, cx
    out 199, ax
    call segundo
    loop cuenta
    mov ax, 0
    out 199, ax

    mov ax, 0000001001001100b   ; verde abajo
    out 4, ax

    lea si, recibo
letra:
    mov al, [si]
    cmp al, 0
    je listo
    out 130, al
    inc si
    jmp letra
listo:

fin:
    mov ax, 4C00h
    int 21h
main endp

segundo proc
    push ax
    push cx
    push dx
    mov cx, 0Fh
    mov dx, 4240h
    mov ah, 86h
    int 15h
    pop dx
    pop cx
    pop ax
    ret
segundo endp
end main
```

#### Al superarla
Rojo. 3, 2, 1… **0**. ¡Verde! Los corredores salen disparados y la impresora entrega el recibo de largada. El Goblin de los Cables, sin un solo cable cruzado que le quede, levanta las manos y se ríe: —Me ganaste, chispita.

{mentor} hace brillar su ojo, orgulloso. —Ahora mis nervios llegan a todo el Gremio —dice—. Y vos sabés usarlos.

#### Imagen
- Una pista de carreras de noche en las Forjas, con un semáforo de bronce en verde, un visor grande de cifras rojas y una impresora sacando un papel, y corredores saliendo disparados.
- Axón (gólem de bronce gigante con un único ojo redondo de cristal) mira desde atrás, con el ojo brillando orgulloso.
- Un goblin verde y flaco de caricatura, con ropa de tela cerrada, levanta las manos riéndose, derrotado.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) corre entre los corredores, festejando.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) levanta los brazos; Gheco (gecko de luz cian con antiparras, chiquito) en su hombro.

### Prueba del sello

#### ¿En qué orden van los pasos de la largada?
Todo en rojo, la cuenta regresiva en el visor con esperas, el verde abajo y el recibo en la impresora.

#### ¿Por qué la rutina `segundo` guarda CX?
Porque la espera de la BIOS usa CX, y el `loop` de la cuenta también: sin guardarlo, el bucle se rompe.
