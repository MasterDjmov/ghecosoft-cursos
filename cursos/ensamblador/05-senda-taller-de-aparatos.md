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
