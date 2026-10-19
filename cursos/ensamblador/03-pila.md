# RAMA R03 · Pila, procedimientos y pantalla: la torre de platos

```meta
tipo: tronco
posicion: 3
```

## R03-N01 · La torre de platos: `push` y `pop`

```meta
tipo: tema
criatura: troll
padre: R02-N09
precio: 0
temas: maq.pila, col.pilas-colas
```

### Crónica

{mentor} está de pie, pero no se anima a dar un paso. —Para caminar —explica— tengo que guardar dónde estaba antes de cada movimiento, y volver a ese lugar si algo sale mal. Lo guardo en mi **espalda**.

Nova sube por la columna del Gólem y encuentra una **torre de platos** de metal: una pila altísima, que llega al techo. Gheco pone uno arriba, con cuidado. —Acá se apila **arriba** y se saca **de arriba** —dice—. El último que ponés es el primero que sacás. Y cuidado con el que vive al fondo: el **troll**.

### Objetivos

Usar la **pila** para guardar y recuperar valores con `push` y `pop`, entender que lo último que entra es lo
primero que sale (LIFO), intercambiar e invertir con ella, y respetar la regla de oro: cada `push` con su `pop`,
en orden inverso.

### Antes de empezar

- `loop` (Repetir) y `[si]` (Arreglos e índices).

### Explicación

#### Último en entrar, primero en salir
La **pila** (*stack*) es una zona de la memoria (la que reserva `.stack 100h`) que se usa como una torre de
platos:
- `push ax` pone una copia de AX **arriba** de la torre.
- `pop bx` saca el plato de **arriba** y lo pone en BX.

La palanca **SP** (*stack pointer*) señala el plato de arriba. La torre **crece hacia abajo** en la memoria: cada
`push` le resta 2 a SP y cada `pop` le suma 2. En el tablero, la pestaña **Pila** muestra la torre.

#### Siempre de a dos cajones
`push` y `pop` trabajan con **words**: `push ax` sí, `push al` no. Para apilar un carácter se apila la palanca
entera, y al sacarla se usa la mitad que interesa. En el 8086 tampoco existen `push 5` ni `pusha` (llegaron con
procesadores más nuevos): `mov ax, 5` y `push ax`.

#### Para qué sirve
1. **Guardar y recuperar:** `push ax`, usar AX para otra cosa, `pop ax`.
2. **Intercambiar:** `push ax`, `push bx`, `pop ax`, `pop bx` cambia los valores (salen al revés).
3. **Invertir:** apilar letras y desapilarlas las da al revés.
4. **Las rutinas** (el próximo nodo): `call` guarda en la pila el lugar al que hay que volver.

#### La regla de oro
Cada `push` con su `pop`, **en orden inverso**. Lo que se apila último se saca primero: si guardás algo y
después apilás encima, para recuperarlo primero tenés que sacar lo de encima.

> **Puente con otras lenguas.** Es la estructura *pila* (`stack`) de todos los lenguajes: `append` y `pop` de una
> lista de Python, `push` y `pop` de `std::stack` en C++. Y es la misma pila que se ve en un error de Python
> («Traceback»), con las funciones que se fueron llamando una arriba de otra.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
palabra db 'ROMA'
titulo  db 'Al derecho: ROMA', 13, 10, 'Al reves: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, titulo
    mov ah, 09h
    int 21h

    lea si, palabra
    mov cx, 4
apilar:
    mov al, [si]
    push ax              ; se apila AX entero; interesa AL
    inc si
    loop apilar

    mov cx, 4
desapilar:
    pop dx               ; sale primero la última letra
    mov ah, 02h
    int 21h
    loop desapilar

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

### Salida esperada

```
Al derecho: ROMA
Al reves: AMOR
```

### ¿Para qué sirve?

La pila es lo que hace posibles las funciones de todos los lenguajes: cada llamada guarda ahí adónde volver y sus
variables locales. Cuando un programa en Python o Java dice «stack overflow», es esta torre que se llenó. También
se usa para deshacer (*undo*), para recorrer laberintos y para evaluar cuentas como `3 + 4 * 2`.

### Errores habituales

**Goblin: apilar un byte.** `push al`:
```
main.asm(11) : Error A2049: Invalid instruction operands
```

**Goblin: órdenes de otro procesador.** `push 5` o `pusha`:
```
main.asm(11) : Error A2030: Instruction or register not accepted in current CPU mode
```

**Troll: el valor guardado debajo.** `push cx` para guardar una cantidad, y **encima** se apilan letras: el
`pop cx` saca la última letra, no la cantidad.

**Troll: la pila despareja.** Más `push` que `pop` (o al revés): la torre queda corrida. En una rutina, eso hace
que el Gólem vuelva a cualquier lado.

**Ogro: el orden de los `pop`.** `push ax`, `push bx`, `pop ax`, `pop bx` **intercambia**. Para dejarlos como
estaban: `pop bx` y después `pop ax`.

### Micro-misión R03-N01-P1 · El primer plato

```meta
lugar: La torre de platos
personajes: Nova, Gheco
carta: push y pop | push ax = una copia de AX arriba de la torre · pop ax = la saca y la pone en AX
recompensa: xp 10, oro 10
```

#### Escena
Nova tiene un **5** en AX, pero necesita AX para otra cuenta. No quiere perder el 5: lo deja un ratito en la torre.

#### Gheco sugiere
`push ax` pone una copia arriba de la torre. Usá AX para lo que quieras, y después `pop ax` lo devuelve como estaba.

#### Desafío
Completá el `push` y el `pop` para que, al final, AX vuelva a valer **5**, BX tenga el **9** de la otra cuenta y la torre quede como empezó (SP = 100h).

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 5
    push ___
    mov ax, 9        ; la otra cuenta
    mov bx, ax
    pop ___

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
AX = 5
BX = 9
SP = 100h
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

    mov ax, 5
    push ax
    mov ax, 9        ; la otra cuenta
    mov bx, ax
    pop ax

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El 5 vuelve a su palanca. Ejecutá **paso a paso** y mirá la pestaña **Pila**: el plato aparece arriba con el `push` y desaparece con el `pop`. SP baja 2 y vuelve a subir.

#### Imagen
- Una torre altísima de platos de metal dentro de la espalda de un gólem de bronce, que sube hasta perderse en la penumbra.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) apoya con cuidado un plato con cinco puntitos de luz arriba de la torre.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre el plato de arriba.

### Micro-misión R03-N01-P2 · El intercambio

```meta
lugar: La torre de platos
personajes: Nova, Gheco
carta: Intercambiar | push ax · push bx · pop ax · pop bx = salen al revés y se cambian
recompensa: xp 15, oro 15
```

#### Escena
Kira dejó las llaves cambiadas: la de la puerta (**2**) está en AX y la del cofre (**1**) en BX. Nova quiere intercambiarlas usando la torre.

#### Gheco sugiere
Apilá las dos (primero AX, después BX) y sacalas en el **mismo** orden de nombres: la primera que sale es la última que entró, así que se cruzan.

#### Desafío
Escribí las cuatro órdenes donde dice `; tus órdenes` para que AX y BX se intercambien y la torre quede pareja.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 2
    mov bx, 1
    ; tus órdenes

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
AX = 1
BX = 2
SP = 100h
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

    mov ax, 2
    mov bx, 1
    push ax
    push bx
    pop ax
    pop bx

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Las llaves vuelven a su lugar. —Salen al revés de como entran —dice Nova—. Eso, a veces, es justo lo que quiero.

#### Imagen
- Dos llaves de bronce cruzándose en el aire, una con un dibujito de puerta y otra con un dibujito de cofre.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) hace malabares con ellas al lado de la torre de platos.
- Gheco (gecko de luz cian con antiparras, chiquito) atrapa una con la cola.

### Micro-misión R03-N01-P3 · El plato de un solo cajón

```meta
lugar: La torre de platos
personajes: Nova, Gheco
criatura: goblin
carta: Siempre de a words | push ax sí · push al no · se apila la palanca entera y se usa la mitad
recompensa: xp 15, oro 15
```

#### Escena
Nova lee una tecla y quiere guardarla en la torre mientras muestra un mensaje. Escribe `push al` y un goblin salta del plato: *«Invalid instruction operands»*.

#### Gheco sugiere
En la torre solo entran platos **dobles**: words. Apilá AX entero (`push ax`), y al sacarlo (`pop ax`) la tecla vuelve a estar en AL.

#### Desafío
Tocá **Ejecutar** para ver al goblin. Después arreglá el `push` y el `pop`. Vas a tipear la `K`.

#### Código inicial
```asm
.model small
.stack 100h
.data
t_guarda db 13, 10, 'Guardada: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ah, 01h
    int 21h
    push al

    lea dx, t_guarda
    mov ah, 09h
    int 21h

    pop al
    mov dl, al
    mov ah, 02h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Entrada
```
K
```

#### Salida esperada
```
K
Guardada: K
```

#### Solución
```asm
.model small
.stack 100h
.data
t_guarda db 13, 10, 'Guardada: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ah, 01h
    int 21h
    push ax

    lea dx, t_guarda
    mov ah, 09h
    int 21h

    pop ax
    mov dl, al
    mov ah, 02h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
La K sobrevive al mensaje. El goblin se tira de cabeza de la torre, ofendido, y aterriza sobre un plato más abajo.

#### Imagen
- Un goblin verde y flaco, enojado, sentado sobre un platito chico que no encaja en una torre de platos grandes.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) apoya un plato grande y doble arriba de la torre.
- Gheco (gecko de luz cian con antiparras, chiquito) mide los dos platos con las patitas.

### Micro-misión R03-N01-P4 · El espejo

```meta
lugar: La torre de platos
personajes: Nova, Gheco
carta: Invertir | apilar en orden · desapilar sale al revés · ROMA -> AMOR
recompensa: xp 15, oro 15
```

#### Escena
En la torre hay grabada una palabra: **ROMA**. Gheco jura que, leída desde la torre, dice otra cosa.

#### Gheco sugiere
Las letras ya están apiladas, de la R a la A. Ahora sacalas: cada `pop dx` deja una letra en DL, lista para la `02h`. Salen al revés.

#### Desafío
Escribí el bucle que desapila donde dice `; tus órdenes`, para que el ojo muestre `AMOR`.

#### Código inicial
```asm
.model small
.stack 100h
.data
palabra db 'ROMA'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, palabra
    mov cx, 4
apilar:
    mov al, [si]
    push ax
    inc si
    loop apilar

    ; tus órdenes

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
AMOR
```

#### Estado esperado
```
SP = 100h
```

#### Solución
```asm
.model small
.stack 100h
.data
palabra db 'ROMA'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, palabra
    mov cx, 4
apilar:
    mov al, [si]
    push ax
    inc si
    loop apilar

    mov cx, 4
desapilar:
    pop dx
    mov ah, 02h
    int 21h
    loop desapilar

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
**AMOR**. Gheco se pone colorado (más cian) y Nova se ríe. —La torre da vuelta todo —dice.

#### Imagen
- Una torre de platos de metal con cuatro platos de arriba brillando en cian, cada uno con un símbolo distinto: una corona, una hoja, una gota y un sol.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) saca el plato de arriba de todo.
- Gheco (gecko de luz cian con antiparras, chiquito) con un corazoncito de luz flotando sobre la cabeza, avergonzado.

### Micro-misión R03-N01-P5 · El plato de abajo

```meta
lugar: La torre de platos
personajes: Nova, Gheco
criatura: troll
carta: Lo guardado, arriba | si apilás encima, lo guardado queda abajo · guardalo en otra palanca
recompensa: xp 20, oro 20
```

#### Escena
Nova quiere invertir la palabra **SOL** sin escribir dos veces el 3. Guarda la cantidad en la torre con `push cx`, apila las letras encima y, al hacer `pop cx`… el Gólem saca cualquier cosa. Desde el fondo de la torre, algo enorme y gris gruñe: el **troll**.

#### Gheco sugiere
`push cx` dejó la cantidad **abajo** de las letras. El `pop cx` saca la **última letra**, no la cantidad. La cantidad no tiene que ir a la torre: guardala en otra palanca (`mov bx, cx`) y recuperala de ahí (`mov cx, bx`).

#### Desafío
Tocá **Ejecutar** y mirá lo que pasa. Después arreglá el programa para que el ojo muestre `LOS`.

#### Código inicial
```asm
.model small
.stack 100h
.data
palabra db 'SOL'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov cx, 3
    push cx              ; guardo la cantidad
    lea si, palabra
apilar:
    mov al, [si]
    push ax
    inc si
    loop apilar

    pop cx               ; recupero la cantidad
desapilar:
    pop dx
    mov ah, 02h
    int 21h
    loop desapilar

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
LOS
```

#### Solución
```asm
.model small
.stack 100h
.data
palabra db 'SOL'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov cx, 3
    mov bx, cx           ; guardo la cantidad en otra palanca
    lea si, palabra
apilar:
    mov al, [si]
    push ax
    inc si
    loop apilar

    mov cx, bx           ; recupero la cantidad
desapilar:
    pop dx
    mov ah, 02h
    int 21h
    loop desapilar

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
**LOS**. El gruñido del fondo se apaga, pero no del todo: el troll sigue ahí abajo, esperando una torre despareja.

#### Imagen
- La base de una torre de platos de metal, en penumbra, y dos ojos grandes y grises brillando detrás.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se asoma desde arriba de la torre, con cuidado.
- Gheco (gecko de luz cian con antiparras, chiquito) se esconde detrás de su pelo.

### Micro-misión R03-N01-P6 · Ida y vuelta

```meta
lugar: La torre de platos
personajes: Nova, Gheco
carta: Pila sin arreglo | ida: mostrar y apilar · vuelta: desapilar y mostrar · sale al revés
recompensa: xp 20, oro 20
```

#### Escena
Para probar las piernas, {mentor} quiere contar sus pasos de ida y de vuelta: **12345** al ir, y **54321** al volver. Sin arreglos: la vuelta tiene que salir de la torre.

#### Gheco sugiere
En la ida, un bucle del 1 al 5 (podés usar BL, que empieza en `'1'` y sube): mostrá cada dígito y apilalo. Después un espacio. En la vuelta, 5 veces: `pop dx` y mostrar.

#### Desafío
Escribí las órdenes desde cero, donde dice `; tus órdenes`, para que el ojo muestre `12345 54321`.

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

#### Salida esperada
```
12345 54321
```

#### Estado esperado
```
SP = 100h
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

    mov bl, '1'
    mov cx, 5
ida:
    mov dl, bl
    mov ah, 02h
    int 21h
    push dx
    inc bl
    loop ida

    mov dl, ' '
    mov ah, 02h
    int 21h

    mov cx, 5
vuelta:
    pop dx
    mov ah, 02h
    int 21h
    loop vuelta

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Cinco pasos de ida y cinco de vuelta: el Gólem camina en el lugar, ida y vuelta, sin moverse de su sitio. —Me acuerdo de cada paso —dice {mentor}—. Ahora quiero acordarme de **rutinas enteras**.

#### Imagen
- Un gólem de bronce gigante dando un paso adelante y uno atrás en una caverna, con huellas marcadas en el piso de piedra.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se asoma por la puerta del pecho, contando con los dedos.
- Gheco (gecko de luz cian con antiparras, chiquito) salta de huella en huella.

### Prueba del sello

#### Si se hace `push ax` y después `push bx`, ¿qué saca el primer `pop`?
El valor de BX: el último que entró sale primero.

#### ¿Por qué no se puede hacer `push al`?
Porque la pila trabaja de a words (dos bytes): se apila AX entero.

#### ¿Qué le pasa a SP en cada `push`?
Le resta 2 (la torre crece hacia abajo en la memoria); cada `pop` le suma 2.

#### ¿Cómo se dejan AX y BX como estaban después de `push ax` y `push bx`?
Con `pop bx` y después `pop ax`: en orden inverso.

## R03-N02 · Las rutinas: `call` y `ret`

```meta
tipo: tema
criatura: troll
padre: R03-N01
precio: 0
temas: prog.funciones, maq.pila
```

### Crónica

Para dar un paso, el Gólem hace siempre lo mismo: levantar el pie, adelantarlo, apoyarlo. Nova lo escribe una vez, y otra, y otra… y se aburre.

—Escribilo **una sola vez** —le dice {mentor}— y ponele un nombre. Después me decís «hacé eso» y yo lo hago, y **vuelvo** exactamente adonde estaba.

—¿Y cómo sabés adónde volver? —pregunta Nova.

El Gólem señala la torre de platos con el pulgar.

### Objetivos

Escribir **procedimientos** (rutinas con nombre) con `proc` y `endp`, llamarlos con `call` y volver con `ret`,
entender que `call` guarda en la pila el lugar al que hay que volver, y pasarles datos por registros.

### Antes de empezar

- `push` y `pop` (La torre de platos).

### Explicación

#### Definir y llamar
```asm
nueva_linea proc
    mov dl, 13
    mov ah, 02h
    int 21h
    mov dl, 10
    int 21h
    ret
nueva_linea endp
```
- `call nueva_linea` **apila** el lugar de la orden siguiente y salta a la rutina.
- `ret` **desapila** ese lugar y vuelve ahí.

Los procedimientos se escriben **después** de `main endp` y **antes** de `end main`. El programa principal termina
con la `4Ch`, así que el Gólem nunca entra en ellos por accidente.

#### Pasar datos: por palancas
En ensamblador no hay parámetros con nombre: se acuerda **en qué palanca** va cada dato y se anota en un
comentario:
```asm
; mostrar_digito: muestra AL (de 0 a 9) como carácter
; entrada: AL = el dígito
```

#### Por qué importa la torre pareja
`ret` saca de la torre **el plato de arriba** y lo usa como lugar de vuelta. Si la rutina hizo un `push` y se
olvidó el `pop`, `ret` saca ese valor en vez del lugar de vuelta, y el Gólem salta a cualquier lado.

> **Puente con otras lenguas.** Un procedimiento es una **función**: `def` en Python, una función de C o un método
> de Java. Llamar a una función es un `call`, y el `return` es el `ret`. La pila de llamadas que muestran los
> errores de Python y Java es, literalmente, esta torre con los lugares de vuelta.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 7
    call mostrar_digito
    call nueva_linea
    mov al, 0
    call mostrar_digito
    call nueva_linea
    mov al, 3
    call mostrar_digito

fin:
    mov ax, 4C00h
    int 21h
main endp

; mostrar_digito: muestra AL (0 a 9) como carácter
mostrar_digito proc
    mov dl, al
    add dl, '0'
    mov ah, 02h
    int 21h
    ret
mostrar_digito endp

; nueva_linea: pasa al renglón siguiente
nueva_linea proc
    mov dl, 13
    mov ah, 02h
    int 21h
    mov dl, 10
    int 21h
    ret
nueva_linea endp

end main
```

### Salida esperada

```
7
0
3
```

### ¿Para qué sirve?

Las funciones son la herramienta más importante para escribir programas grandes: se escribe algo una vez, se
prueba, se le pone nombre y se usa mil veces. Todo lenguaje las tiene, y todas, por debajo, son un `call`, un
`ret` y la torre que recuerda adónde volver.

### Errores habituales

**Troll: el `ret` con la torre despareja.** Un `push` sin su `pop` adentro de la rutina: `ret` usa ese valor como
lugar de vuelta y el Gólem salta a una dirección sin órdenes.

**Ogro: caerse dentro de una rutina.** Si el programa principal no termina con la `4Ch`, el Gólem sigue de largo,
entra en la primera rutina y su `ret` vuelve a cualquier lado.

**Slime: `endp` con otro nombre.** `mostrar proc` … `mostar endp`:
```
main.asm(30) : Error A2142: Unmatched block nesting: mostrar
```

**Esqueleto: la rutina que no existe.** `call mostar`:
```
main.asm(10) : Error A2102: Symbol not defined : mostar
```

### Micro-misión R03-N02-P1 · Llamar a la rutina

```meta
lugar: La columna del Gólem
personajes: Nova, Gheco
carta: call | call rutina = guardá adónde volver y saltá · ret = volvé
recompensa: xp 10, oro 10
```

#### Escena
Gheco ya escribió una rutina que pasa de renglón: `salto`. Nova solo tiene que **llamarla** entre las dos palabras.

#### Gheco sugiere
`call salto` hace todo lo que está entre `salto proc` y su `ret`, y vuelve a la orden siguiente.

#### Desafío
Completá la llamada para que las palabras salgan en dos renglones.

#### Código inicial
```asm
.model small
.stack 100h
.data
arriba db 'Arriba$'
abajo  db 'Abajo$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, arriba
    mov ah, 09h
    int 21h
    call ___
    lea dx, abajo
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp

salto proc
    mov dl, 13
    mov ah, 02h
    int 21h
    mov dl, 10
    int 21h
    ret
salto endp

end main
```

#### Salida esperada
```
Arriba
Abajo
```

#### Solución
```asm
.model small
.stack 100h
.data
arriba db 'Arriba$'
abajo  db 'Abajo$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, arriba
    mov ah, 09h
    int 21h
    call salto
    lea dx, abajo
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp

salto proc
    mov dl, 13
    mov ah, 02h
    int 21h
    mov dl, 10
    int 21h
    ret
salto endp

end main
```

#### Al superarla
Ejecutalo **paso a paso** y mirá la **Pila**: con el `call` aparece un plato nuevo (el lugar de vuelta), y con el `ret` desaparece. La flechita salta a la rutina y vuelve.

#### Imagen
- Un pasillo de bronce dentro de la columna de un gólem, con una puerta lateral abierta y un camino de luz cian que entra y vuelve a salir por ella.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) sigue el camino de luz con la mirada.
- Gheco (gecko de luz cian con antiparras, chiquito) sostiene un platito con una flecha de vuelta dibujada.

### Micro-misión R03-N02-P2 · Mi primera rutina

```meta
lugar: La columna del Gólem
personajes: Nova, Gheco
carta: proc | nombre proc … ret … nombre endp · después de main endp · datos por palancas
recompensa: xp 15, oro 15
```

#### Escena
Ahora le toca a Nova escribir una rutina propia: `mostrar_digito`, que muestra el dígito que haya en AL. El programa principal ya la llama tres veces, con el 7, el 0 y el 3.

#### Gheco sugiere
Adentro de la rutina: pasá AL a DL, sumale `'0'`, la `02h` y, al final, `ret` para volver.

#### Desafío
Escribí el cuerpo de la rutina donde dice `; tus órdenes`, para que el ojo muestre `703`.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 7
    call mostrar_digito
    mov al, 0
    call mostrar_digito
    mov al, 3
    call mostrar_digito

fin:
    mov ax, 4C00h
    int 21h
main endp

; mostrar_digito: muestra AL (0 a 9) como carácter
mostrar_digito proc
    ; tus órdenes
mostrar_digito endp

end main
```

#### Salida esperada
```
703
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

    mov al, 7
    call mostrar_digito
    mov al, 0
    call mostrar_digito
    mov al, 3
    call mostrar_digito

fin:
    mov ax, 4C00h
    int 21h
main endp

; mostrar_digito: muestra AL (0 a 9) como carácter
mostrar_digito proc
    mov dl, al
    add dl, '0'
    mov ah, 02h
    int 21h
    ret
mostrar_digito endp

end main
```

#### Al superarla
**703**: el número de la puerta de la columna. —Una rutina que escribí yo —dice Nova, orgullosa— y la usé tres veces.

#### Imagen
- Una puerta de bronce en la columna de un gólem, con tres símbolos de luz cian encendiéndose uno por uno sobre el marco: un rayo, un círculo y una media luna.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) con las manos juntas, orgullosa.
- Gheco (gecko de luz cian con antiparras, chiquito) aplaude sobre el marco.

### Micro-misión R03-N02-P3 · El plato olvidado

```meta
lugar: La columna del Gólem
personajes: Nova, Gheco
criatura: troll
carta: Torre pareja | cada push de la rutina con su pop antes del ret · si no, ret vuelve a cualquier lado
recompensa: xp 20, oro 20
```

#### Escena
Nova mejora su rutina: guarda DX en la torre para no pisárselo a nadie. Pero se olvida de algo, ejecuta… y el Gólem salta a un lugar sin órdenes. El **troll** de la torre se ríe con una voz muy grave.

#### Gheco sugiere
La rutina hace `push dx` y llega al `ret` sin el `pop`. Entonces `ret` saca **DX** de la torre y lo usa como lugar de vuelta. Antes del `ret`, devolvé el plato con `pop dx`.

#### Desafío
Tocá **Ejecutar** y leé el aviso. Después arreglá la rutina para que el ojo muestre `703` y el Gólem vuelva bien.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 7
    call mostrar_digito
    mov al, 0
    call mostrar_digito
    mov al, 3
    call mostrar_digito

fin:
    mov ax, 4C00h
    int 21h
main endp

mostrar_digito proc
    push dx
    mov dl, al
    add dl, '0'
    mov ah, 02h
    int 21h
    ret
mostrar_digito endp

end main
```

#### Salida esperada
```
703
```

#### Estado esperado
```
SP = 100h
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

    mov al, 7
    call mostrar_digito
    mov al, 0
    call mostrar_digito
    mov al, 3
    call mostrar_digito

fin:
    mov ax, 4C00h
    int 21h
main endp

mostrar_digito proc
    push dx
    mov dl, al
    add dl, '0'
    mov ah, 02h
    int 21h
    pop dx
    ret
mostrar_digito endp

end main
```

#### Al superarla
El Gólem vuelve exactamente adonde estaba. El troll deja de reírse: esta vez la torre quedó pareja.

#### Imagen
- Un troll grande y gris, de piel como piedra, asomado desde la base de una torre de platos de metal, con cara de fastidio.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) saca un plato de arriba de la torre, firme.
- Gheco (gecko de luz cian con antiparras, chiquito) señala al troll con la cola, haciéndole burla.

### Micro-misión R03-N02-P4 · El que se cayó adentro

```meta
lugar: La columna del Gólem
personajes: Nova, Gheco
criatura: ogre
carta: Terminar main | el programa principal termina con mov ax, 4C00h + int 21h · si no, sigue de largo
recompensa: xp 15, oro 15
```

#### Escena
Nova escribe un programa cortito que llama a su rutina con un 5… y se olvida de terminarlo. El Gólem muestra el 5, sigue caminando hacia abajo, entra en la rutina sin que nadie lo llame y se pierde. Un ogro lo ve caer.

#### Gheco sugiere
Después de la etiqueta `fin:` faltan las dos órdenes que apagan el programa. Sin ellas, el Gólem sigue con lo que haya abajo: la rutina. Y su `ret` no tiene adónde volver.

#### Desafío
Tocá **Ejecutar** y leé el aviso. Después agregá lo que falta para que el ojo muestre solo el `5` y el programa termine.

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
    call mostrar_digito

fin:
main endp

mostrar_digito proc
    mov dl, al
    add dl, '0'
    mov ah, 02h
    int 21h
    ret
mostrar_digito endp

end main
```

#### Salida esperada
```
5
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
    call mostrar_digito

fin:
    mov ax, 4C00h
    int 21h
main endp

mostrar_digito proc
    mov dl, al
    add dl, '0'
    mov ah, 02h
    int 21h
    ret
mostrar_digito endp

end main
```

#### Al superarla
Un solo 5, y el Gólem se detiene donde corresponde. El ogro, que esperaba otra caída, se va decepcionado.

#### Imagen
- Una escalera de bronce dentro de la columna de un gólem, con un cartel liso con un dibujito de mano levantada al final del primer tramo.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) clava el cartel en su lugar.
- Un ogro grandote y torpe se asoma desde abajo de la escalera, decepcionado.
- Gheco (gecko de luz cian con antiparras, chiquito) se sienta sobre el cartel.

### Micro-misión R03-N02-P5 · El cartel

```meta
lugar: La columna del Gólem
personajes: Nova, Gheco
carta: Datos por palancas | AL = el carácter · CX = cuántas veces · la rutina repite con loop
recompensa: xp 20, oro 20
```

#### Escena
Nova quiere decorar la columna con un cartel: una línea de **=** y otra de **-**, de 10 cada una. Para eso escribe una rutina `separador` que dibuja AL tantas veces como diga CX.

#### Gheco sugiere
Adentro de `separador`: pasá AL a DL y repetí la `02h` con un `loop` (CX ya trae la cantidad). Al final, `ret`. El programa principal y `salto` ya están hechos.

#### Desafío
Escribí el cuerpo de la rutina donde dice `; tus órdenes`.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, '='
    mov cx, 10
    call separador
    call salto
    mov al, '-'
    mov cx, 10
    call separador

fin:
    mov ax, 4C00h
    int 21h
main endp

; separador: muestra AL, CX veces
separador proc
    ; tus órdenes
separador endp

salto proc
    mov dl, 13
    mov ah, 02h
    int 21h
    mov dl, 10
    int 21h
    ret
salto endp

end main
```

#### Salida esperada
```
==========
----------
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

    mov al, '='
    mov cx, 10
    call separador
    call salto
    mov al, '-'
    mov cx, 10
    call separador

fin:
    mov ax, 4C00h
    int 21h
main endp

; separador: muestra AL, CX veces
separador proc
    mov dl, al
    mov ah, 02h
repetir:
    int 21h
    loop repetir
    ret
separador endp

salto proc
    mov dl, 13
    mov ah, 02h
    int 21h
    mov dl, 10
    int 21h
    ret
salto endp

end main
```

#### Al superarla
El cartel queda colgado en la columna, prolijo. {mentor} levanta un pie, lo adelanta y lo apoya: **un paso**, el primero en siglos, con una rutina que se llama una y otra vez.

#### Imagen
- Un gólem de bronce gigante dando su primer paso en una caverna, con el pie adelantado en el aire y polvo cayendo.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) mira desde el piso, con las manos en la boca.
- En el pecho abierto del gólem, Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) festeja.
- Gheco (gecko de luz cian con antiparras, chiquito) en el hombro de Kira.

### Prueba del sello

#### ¿Qué hace `call` con la pila?
Apila el lugar de la orden siguiente (adónde volver) y salta a la rutina.

#### ¿Qué pasa si una rutina hace `push dx` y llega al `ret` sin `pop dx`?
`ret` saca DX de la pila y lo usa como lugar de vuelta: el Gólem salta a cualquier lado.

#### ¿Dónde se escriben los procedimientos?
Después de `main endp` y antes de `end main`.

#### ¿Cómo se le pasan datos a una rutina en ensamblador?
Por palancas (registros) acordadas, anotadas en un comentario.

## R03-N03 · Rutinas que cuidan sus palancas

```meta
tipo: tema
criatura: troll
padre: R03-N02
precio: 0
temas: prog.funciones, prog.alcance, maq.pila
```

### Crónica

Ahora el Gólem camina, pero tropieza: da tres pasos y de golpe se pone a dar pasos para siempre. Nova revisa y encuentra la causa: la rutina del paso usa **CX** para contar los movimientos del pie… y el programa que la llama también estaba usando CX para contar los pasos.

—Una rutina educada —dice Gheco— deja todo como lo encontró.

### Objetivos

Escribir rutinas que **guardan y devuelven** las palancas que usan (`push` al entrar, `pop` en orden inverso al
salir), que **devuelven un resultado** en una palanca acordada o en una bandera (CF con `stc` y `clc`), y saber que
después de un `call` los interruptores son los de la rutina.

### Antes de empezar

- `call`, `ret` y la torre pareja (Las rutinas).

### Explicación

#### Guardar lo que se usa
Una rutina que usa CX lo **pisa**, y quien la llamó puede estar usándolo (por ejemplo, para un `loop`). La regla:
**cada rutina guarda lo que usa y lo devuelve como estaba**, salvo la palanca donde devuelve el resultado.
```asm
estrellas proc
    push cx
    push dx
    ...
    pop dx           ; orden INVERSO
    pop cx
    ret
estrellas endp
```

#### Devolver un resultado
Se acuerda una palanca: «el mayor queda en AL». O una **bandera**, para decir sí o no: `clc` pone CF en 0 y `stc`
en 1. Quien llama decide con `jc` o `jnc`:
```asm
    call es_digito       ; CF = 0 si AL es un dígito
    jc  no_es
```
`pop` no cambia los interruptores, así que el CF llega intacto hasta quien llamó.

#### Los interruptores después de un `call`
Una rutina hace `cmp`, `add`, `div`… y cambia los interruptores. Un salto justo después de un `call` mira los de
**la rutina**, no los de antes.

> **Puente con otras lenguas.** En Python, Java o C cada función tiene sus **variables locales** y no le toca las
> suyas a nadie: el compilador hace, por vos, exactamente estos `push` y `pop`. Y devolver un `bool` es como
> devolver CF.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov cx, 3            ; 3 filas
filas:
    call estrellas
    loop filas

fin:
    mov ax, 4C00h
    int 21h
main endp

; estrellas: muestra *** y pasa de renglón (no toca ninguna palanca)
estrellas proc
    push ax
    push cx
    push dx
    mov cx, 3
    mov dl, '*'
    mov ah, 02h
una:
    int 21h
    loop una
    mov dl, 13
    int 21h
    mov dl, 10
    int 21h
    pop dx
    pop cx
    pop ax
    ret
estrellas endp

end main
```

### Salida esperada

```
***
***
***
```

### ¿Para qué sirve?

Las funciones que no tocan nada de afuera se pueden usar desde cualquier lado sin miedo: son las piezas con las que
se arman los programas grandes. Las que pisan cosas generan los errores más difíciles de encontrar, porque el
problema aparece lejos de donde se cometió.

### Errores habituales

**Troll: la rutina que pisa CX.** Llamarla desde adentro de un `loop` cambia la cantidad de vueltas (o las vuelve
infinitas).

**Ogro: el orden de los `pop`.** `push ax`, `push bx` … `pop ax`, `pop bx` le devuelve a quien llamó las palancas
**cruzadas**.

**Ogro: confiar en los interruptores después de un `call`.** Se miran enseguida, o se devuelven a propósito en CF.

### Micro-misión R03-N03-P1 · El paso que no termina

```meta
lugar: Las piernas del Gólem
personajes: Nova, Gheco
criatura: troll
carta: Guardar lo que se usa | push cx al entrar · pop cx antes del ret · la rutina no pisa a nadie
recompensa: xp 15, oro 15
```

#### Escena
El programa llama 3 veces a la rutina `paso`, pero el Gólem da pasos para siempre. El troll, desde la torre, se frota las manos.

#### Gheco sugiere
`paso` usa CX para su propio `loop` y lo deja en 0. Cuando vuelve, el `loop pasos` de afuera le resta 1 a 0… Guardá CX al entrar a la rutina y devolvelo antes del `ret`.

#### Desafío
Tocá **Ejecutar** y leé el aviso. Después arreglá la rutina para que el Gólem dé exactamente 3 pasos.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov cx, 3
pasos:
    call paso
    loop pasos

fin:
    mov ax, 4C00h
    int 21h
main endp

; paso: muestra "---> " (levanta, adelanta, apoya)
paso proc
    mov cx, 3
    mov dl, '-'
    mov ah, 02h
mov_pie:
    int 21h
    loop mov_pie
    mov dl, '>'
    int 21h
    mov dl, ' '
    int 21h
    ret
paso endp

end main
```

#### Salida esperada
```
---> ---> --->
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

    mov cx, 3
pasos:
    call paso
    loop pasos

fin:
    mov ax, 4C00h
    int 21h
main endp

; paso: muestra "---> " (levanta, adelanta, apoya)
paso proc
    push cx
    mov cx, 3
    mov dl, '-'
    mov ah, 02h
mov_pie:
    int 21h
    loop mov_pie
    mov dl, '>'
    int 21h
    mov dl, ' '
    int 21h
    pop cx
    ret
paso endp

end main
```

#### Al superarla
Tres pasos, y el Gólem se detiene. El troll gruñe: era su truco favorito.

#### Imagen
- Tres huellas enormes en fila en un piso de piedra, y un gólem de bronce gigante detenido justo después de la tercera.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se asoma por el pecho, aliviada.
- Gheco (gecko de luz cian con antiparras, chiquito) sentado dentro de la tercera huella.

### Micro-misión R03-N03-P2 · El mayor de tres

```meta
lugar: Las piernas del Gólem
personajes: Nova, Gheco
carta: Devolver en AL | entrada: AL y BL · salida: AL = el mayor · se usa varias veces
recompensa: xp 15, oro 15
```

#### Escena
Para elegir el camino más ancho, el Gólem mide tres pasillos: **4**, **8** y **6**. Nova escribe una rutina `mayor` que devuelve en AL el mayor entre AL y BL, y la usa dos veces.

#### Gheco sugiere
Adentro de `mayor`: compará AL con BL; si AL ya es mayor o igual (`jae`), no hagas nada; si no, `mov al, bl`. Después, `ret`.

#### Desafío
Escribí el cuerpo de la rutina donde dice `; tus órdenes`, para que AL termine con el mayor de los tres.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 4
    mov bl, 8
    call mayor
    mov bl, 6
    call mayor

fin:
    mov ax, 4C00h
    int 21h
main endp

; mayor: AL = el mayor entre AL y BL
mayor proc
    ; tus órdenes
mayor endp

end main
```

#### Estado esperado
```
AL = 8
SP = 100h
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

    mov al, 4
    mov bl, 8
    call mayor
    mov bl, 6
    call mayor

fin:
    mov ax, 4C00h
    int 21h
main endp

; mayor: AL = el mayor entre AL y BL
mayor proc
    cmp al, bl
    jae listo
    mov al, bl
listo:
    ret
mayor endp

end main
```

#### Al superarla
El pasillo de 8. El Gólem gira hacia él. —Escribí `mayor` una vez —dice Nova— y me sirve para comparar los que quiera.

#### Imagen
- Tres pasillos de bronce de distinto ancho saliendo de una sala circular; el del medio, el más ancho, iluminado.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) señala el pasillo ancho.
- Gheco (gecko de luz cian con antiparras, chiquito) mide la entrada de otro con los brazos abiertos.

### Micro-misión R03-N03-P3 · Las palancas cruzadas

```meta
lugar: Las piernas del Gólem
personajes: Nova, Gheco
criatura: ogre
carta: Orden inverso | push ax · push bx … pop bx · pop ax · si no, salen cruzadas
recompensa: xp 15, oro 15
```

#### Escena
Nova le pasa a la rutina `marcar` la llave de la puerta (1) en AX y la del cofre (2) en BX. La rutina las guarda y las devuelve… pero cruzadas. Un ogro se ríe con la llave equivocada en la mano.

#### Gheco sugiere
La rutina hace `push ax`, `push bx` y después `pop ax`, `pop bx`. Lo último que entró (BX) sale primero: va a parar a AX. Los `pop` van en orden **inverso**.

#### Desafío
Ejecutá y mirá AX y BX. Después arreglá el orden para que, al volver de la rutina, AX siga en **1** y BX en **2**.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 1
    mov bx, 2
    call marcar

fin:
    mov ax, 4C00h
    int 21h
main endp

; marcar: muestra una X (no tiene que cambiar AX ni BX)
marcar proc
    push ax
    push bx
    mov dl, 'X'
    mov ah, 02h
    int 21h
    mov bx, 0
    pop ax
    pop bx
    ret
marcar endp

end main
```

#### Salida esperada
```
X
```

#### Estado esperado
```
AX = 1
BX = 2
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

    mov ax, 1
    mov bx, 2
    call marcar

fin:
    mov ax, 4C00h
    int 21h
main endp

; marcar: muestra una X (no tiene que cambiar AX ni BX)
marcar proc
    push ax
    push bx
    mov dl, 'X'
    mov ah, 02h
    int 21h
    mov bx, 0
    pop bx
    pop ax
    ret
marcar endp

end main
```

#### Al superarla
Cada llave en su palanca. El ogro, sin nada que hacer, devuelve la que tenía.

#### Imagen
- Dos llaves de bronce colgadas de dos ganchos con dibujitos distintos (una puerta y un cofre), cada una en el suyo.
- Un ogro grandote y torpe devolviendo una llave con cara de nada.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) con la mano extendida.
- Gheco (gecko de luz cian con antiparras, chiquito) cuelga de uno de los ganchos.

### Micro-misión R03-N03-P4 · ¿Sí o no? En una bandera

```meta
lugar: Las piernas del Gólem
personajes: Nova, Gheco
carta: Devolver en CF | clc = CF en 0 (sí) · stc = CF en 1 (no) · quien llama decide con jc o jnc
recompensa: xp 20, oro 20
```

#### Escena
Nova quiere una rutina que conteste **sí o no**: «¿la tecla de AL es un dígito?». Gheco le propone contestar con un interruptor: **CF**.

#### Gheco sugiere
Si AL está entre `'0'` y `'9'`, terminá con `clc` (CF = 0: sí); si no, con `stc` (CF = 1: no). El programa principal ya decide con `jc`.

#### Desafío
Completá las dos órdenes que ponen CF en la rutina. Vas a tipear el `7`.

#### Código inicial
```asm
.model small
.stack 100h
.data
t_si db 13, 10, 'Es un digito.$'
t_no db 13, 10, 'No es un digito.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ah, 01h
    int 21h
    call es_digito
    jc  no_es
    lea dx, t_si
    jmp mostrar
no_es:
    lea dx, t_no
mostrar:
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp

; es_digito: CF = 0 si AL es '0'..'9'; CF = 1 si no
es_digito proc
    cmp al, '0'
    jb  no_digito
    cmp al, '9'
    ja  no_digito
    ___
    ret
no_digito:
    ___
    ret
es_digito endp

end main
```

#### Entrada
```
7
```

#### Salida esperada
```
7
Es un digito.
```

#### Solución
```asm
.model small
.stack 100h
.data
t_si db 13, 10, 'Es un digito.$'
t_no db 13, 10, 'No es un digito.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ah, 01h
    int 21h
    call es_digito
    jc  no_es
    lea dx, t_si
    jmp mostrar
no_es:
    lea dx, t_no
mostrar:
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp

; es_digito: CF = 0 si AL es '0'..'9'; CF = 1 si no
es_digito proc
    cmp al, '0'
    jb  no_digito
    cmp al, '9'
    ja  no_digito
    clc
    ret
no_digito:
    stc
    ret
es_digito endp

end main
```

#### Al superarla
—Una rutina que contesta sí o no con un solo interruptor —dice Nova—. Como una función que devuelve verdadero o falso.

#### Imagen
- Un interruptor de bronce grande con una lucecita verde encendida, en una pared con engranajes.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) con el pulgar arriba.
- Gheco (gecko de luz cian con antiparras, chiquito) sentado sobre el interruptor.

### Micro-misión R03-N03-P5 · El ticket del almacén

```meta
lugar: Las piernas del Gólem
personajes: Nova, Gheco, Kira
carta: Rutina con acumulador | entrada: DX = producto · AL = precio · suma el precio a BL · muestra el renglón
recompensa: xp 25, oro 25
```

#### Escena
Kira volvió del almacén de las Forjas con pan, leche y queso, y quiere el **ticket** con el total. Nova escribe una rutina `renglon` que muestra cada producto con su precio y va sumando en BL.

#### Gheco sugiere
Adentro de `renglon`: mostrá el texto con la `09h` (DX ya lo trae), después el signo `$` con la `02h` (con la `09h` no se puede: cortaría el texto) y el precio con `+ '0'`; sumale el precio a BL y pasá de renglón con `salto`. Cuidado: AL trae el precio y la `09h` lo pisa. Guardalo primero en otra palanca. El final con el total ya está hecho.

#### Desafío
Escribí el cuerpo de `renglon` donde dice `; tus órdenes`.

#### Código inicial
```asm
.model small
.stack 100h
.data
p_pan   db 'Pan     $'
p_leche db 'Leche   $'
p_queso db 'Queso   $'
p_total db 'TOTAL   $'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bl, 0
    lea dx, p_pan
    mov al, 3
    call renglon
    lea dx, p_leche
    mov al, 4
    call renglon
    lea dx, p_queso
    mov al, 5
    call renglon

    lea dx, p_total
    mov ah, 09h
    int 21h
    mov dl, '$'
    mov ah, 02h
    int 21h
    mov al, bl
    mov ah, 0
    mov bl, 10
    div bl
    mov cx, ax
    mov dl, cl
    add dl, '0'
    mov ah, 02h
    int 21h
    mov dl, ch
    add dl, '0'
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp

; renglon: DX = producto, AL = precio (0 a 9); suma el precio a BL
renglon proc
    ; tus órdenes
renglon endp

salto proc
    push ax
    push dx
    mov dl, 13
    mov ah, 02h
    int 21h
    mov dl, 10
    int 21h
    pop dx
    pop ax
    ret
salto endp

end main
```

#### Salida esperada
```
Pan     $3
Leche   $4
Queso   $5
TOTAL   $12
```

#### Solución
```asm
.model small
.stack 100h
.data
p_pan   db 'Pan     $'
p_leche db 'Leche   $'
p_queso db 'Queso   $'
p_total db 'TOTAL   $'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bl, 0
    lea dx, p_pan
    mov al, 3
    call renglon
    lea dx, p_leche
    mov al, 4
    call renglon
    lea dx, p_queso
    mov al, 5
    call renglon

    lea dx, p_total
    mov ah, 09h
    int 21h
    mov dl, '$'
    mov ah, 02h
    int 21h
    mov al, bl
    mov ah, 0
    mov bl, 10
    div bl
    mov cx, ax
    mov dl, cl
    add dl, '0'
    mov ah, 02h
    int 21h
    mov dl, ch
    add dl, '0'
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp

; renglon: DX = producto, AL = precio (0 a 9); suma el precio a BL
renglon proc
    push cx
    mov cl, al           ; el precio, a salvo
    mov ah, 09h
    int 21h
    mov dl, '$'
    mov ah, 02h
    int 21h
    mov dl, cl
    add dl, '0'
    int 21h
    add bl, cl
    call salto
    pop cx
    ret
renglon endp

salto proc
    push ax
    push dx
    mov dl, 13
    mov ah, 02h
    int 21h
    mov dl, 10
    int 21h
    pop dx
    pop ax
    ret
salto endp

end main
```

#### Al superarla
El ticket sale perfecto, con el total al pie. Kira lo dobla y se lo guarda. —El almacenero me cobró 13 —dice, frunciendo el ceño—. Mañana vuelvo con esto.

#### Imagen
- Un ticket largo de papel saliendo de una ranura de bronce en la pierna de un gólem, con renglones de rayitas y dibujitos de pan, una botella de leche y un queso, sin letras.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) lo arranca, con el ceño fruncido.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre una canasta con pan, una botella y un queso.

### Prueba del sello

#### ¿Qué palancas tiene que guardar una rutina?
Todas las que usa, salvo la que devuelve el resultado.

#### Si una rutina hace `push ax` y `push bx`, ¿en qué orden van los `pop`?
`pop bx` y después `pop ax`.

#### ¿Qué hacen `clc` y `stc`?
Ponen CF en 0 y en 1. Sirven para que una rutina conteste sí o no.

#### ¿Por qué hay que tener cuidado con un salto justo después de un `call`?
Porque mira los interruptores que dejó la rutina, no los de antes.

## R03-N04 · El grimorio de los números

```meta
tipo: tema
criatura: ogre
padre: R03-N03
precio: 0
temas: prog.salida, prog.entrada, prog.variables
usa: maq.pila, prog.funciones
```

### Crónica

En la columna del Gólem, Nova encuentra un libro de bronce cerrado con un candado: el **grimorio de los números**. Gheco lo abre con la cola. Adentro no hay hechizos: hay **rutinas**.

—Hasta ahora solo podía mostrar números de una o dos cifras —dice Nova—. ¿Y si el Gólem quiere decir cuántos pasos dio desde que despertó? Pueden ser miles.

—Para eso está el grimorio —dice Gheco—. Una rutina para mostrar **cualquier** número, otra para los negativos y otra para leerlos del teclado. Se escriben una vez y se copian a cada programa.

### Objetivos

Mostrar cualquier número de 16 bits separando sus cifras con divisiones por 10 y la **pila** (`imprimir_numero`),
mostrar números con signo, y convertir un texto tipeado en un número (`leer_numero`), validando lo que se lee.

### Antes de empezar

- `div bx` con 16 bits (Las cuentas del Gólem).
- La pila y las rutinas que cuidan sus palancas (nodos anteriores).
- La función 0Ah y su bolsa (La boca de bronce).

### Explicación

#### De número a texto
Para mostrar 1234 hay que mostrar `'1'`, `'2'`, `'3'` y `'4'`. Dividiendo por 10, el **resto** es la última cifra:
```
1234 / 10 = 123  resto 4
 123 / 10 =  12  resto 3
  12 / 10 =   1  resto 2
   1 / 10 =   0  resto 1   -> se termina
```
Las cifras salen **al revés**: se **apilan**, y se muestran al desapilarlas. Como el número llega hasta 65.535, la
división es de 16 bits: `div bx` divide **DX:AX**, deja el cociente en AX y el resto en DX. Por eso, antes de
**cada** división, `mov dx, 0`.

```asm
imprimir_numero proc        ; muestra AX (0 a 65535)
    push ax
    push bx
    push cx
    push dx
    mov bx, 10
    mov cx, 0               ; cuántas cifras se apilaron
separar:
    mov dx, 0
    div bx                  ; AX = AX / 10, DX = la última cifra
    push dx
    inc cx
    cmp ax, 0
    jne separar             ; hasta que no quede nada (el 0 muestra "0")
mostrar:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp
```

#### Con signo
Si el bit 15 está prendido (`test ax, 8000h`), el número es negativo: se muestra un `'-'`, se le da vuelta el signo
con `neg ax` y se muestra como positivo.

#### De texto a número
Se lee una línea con la `0Ah` y se arma el número cifra por cifra:
```
"125":  n = 0
        n = 0  * 10 + 1 = 1
        n = 1  * 10 + 2 = 12
        n = 12 * 10 + 5 = 125
```
Y se **valida**: cada carácter tiene que estar entre `'0'` y `'9'`.

> **Puente con otras lenguas.** Esto es lo que hacen por dentro `print(n)` y `int(input())` de Python, `printf("%d")`
> y `scanf("%d")` de C, o `Integer.parseInt` de Java. Ahora sabés cuánto trabajo hay detrás de una sola línea.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
t_pasos db 'Pasos desde que desperte: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_pasos
    mov ah, 09h
    int 21h
    mov ax, 1234
    call imprimir_numero

fin:
    mov ax, 4C00h
    int 21h
main endp

imprimir_numero proc
    push ax
    push bx
    push cx
    push dx
    mov bx, 10
    mov cx, 0
separar:
    mov dx, 0
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne separar
mostrar:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

end main
```

### Salida esperada

```
Pasos desde que desperte: 1234
```

### ¿Para qué sirve?

Toda pantalla que muestra un número (un puntaje, un precio, una fecha) y todo formulario que lo lee hacen esta
conversión. Y la técnica de dividir por la base y apilar los restos sirve para pasar a binario, a hexadecimal o a
cualquier otra base.

### Errores habituales

**Ogro: DX sucio antes de `div bx`.** Se divide DX:AX: si DX tiene el resto de la vuelta anterior, el cociente no
entra y el Gólem se detiene (*Divide overflow*). `mov dx, 0` **adentro** del bucle, antes de cada división.

**Ogro: las cifras al revés.** Mostrar los restos a medida que salen da `4321`. Para eso está la pila.

**Goblin: el carácter que no es cifra.** Sin validar, `'a' - '0'` da 49 y «1a» se lee como 59. Siempre
`cmp bl, '0'` + `jb` y `cmp bl, '9'` + `ja`.

### Micro-misión R03-N04-P1 · La primera página

```meta
lugar: El grimorio de los números
personajes: Nova, Gheco
carta: Separar cifras | div por 10 · el resto (DX) es la última cifra · se apila · DX en 0 antes de dividir
recompensa: xp 15, oro 15
```

#### Escena
La primera página del grimorio está casi completa: es `imprimir_numero`. Le faltan dos palabras que se borraron con los siglos.

#### Gheco sugiere
Antes de cada `div bx`, DX tiene que estar en **0** (se divide DX:AX). Y después de dividir, el resto (la cifra) está en DX: eso es lo que se **apila**.

#### Desafío
Completá las dos palabras que faltan para que el ojo muestre `1234`.

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
    call imprimir_numero

fin:
    mov ax, 4C00h
    int 21h
main endp

imprimir_numero proc
    push ax
    push bx
    push cx
    push dx
    mov bx, 10
    mov cx, 0
separar:
    mov dx, ___
    div bx
    push ___
    inc cx
    cmp ax, 0
    jne separar
mostrar:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

end main
```

#### Salida esperada
```
1234
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
    call imprimir_numero

fin:
    mov ax, 4C00h
    int 21h
main endp

imprimir_numero proc
    push ax
    push bx
    push cx
    push dx
    mov bx, 10
    mov cx, 0
separar:
    mov dx, 0
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne separar
mostrar:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

end main
```

#### Al superarla
**1234** pasos. Ejecutalo **paso a paso** y mirá la **Pila**: las cifras se apilan 4, 3, 2, 1 y salen 1, 2, 3, 4.

#### Imagen
- Un libro grueso de bronce abierto sobre un atril, con páginas metálicas cubiertas de engranajes grabados y sin letras.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) repasa una línea con el dedo, que se enciende de cian.
- Gheco (gecko de luz cian con antiparras, chiquito) sostiene el candado abierto.

### Micro-misión R03-N04-P2 · El resto que se quedó

```meta
lugar: El grimorio de los números
personajes: Nova, Gheco
criatura: ogre
carta: DX en cada vuelta | div bx divide DX:AX · mov dx, 0 adentro del bucle, no afuera
recompensa: xp 20, oro 20
```

#### Escena
Nova copia la rutina en otra página para practicar, pero pone el `mov dx, 0` **antes** del bucle, «para ahorrar una orden». El Gólem se detiene de golpe: *Divide overflow*. Un ogro se asoma entre las páginas.

#### Gheco sugiere
En la primera vuelta DX vale 0, pero después del `div` queda con el **resto**. En la segunda vuelta se divide DX:AX con ese resto arriba: un número gigante. El `mov dx, 0` tiene que ir **adentro**, antes de cada división.

#### Desafío
Tocá **Ejecutar** y leé el aviso. Después mové la orden a su lugar para que el ojo muestre `2026`.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 2026
    call imprimir_numero

fin:
    mov ax, 4C00h
    int 21h
main endp

imprimir_numero proc
    push ax
    push bx
    push cx
    push dx
    mov bx, 10
    mov cx, 0
    mov dx, 0
separar:
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne separar
mostrar:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

end main
```

#### Salida esperada
```
2026
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

    mov ax, 2026
    call imprimir_numero

fin:
    mov ax, 4C00h
    int 21h
main endp

imprimir_numero proc
    push ax
    push bx
    push cx
    push dx
    mov bx, 10
    mov cx, 0
separar:
    mov dx, 0
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne separar
mostrar:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

end main
```

#### Al superarla
**2026**. El ogro cierra el grimorio de un golpe y se va. —Ahorrar una orden me costó una caída —anota Nova.

#### Imagen
- Un ogro grandote y torpe cerrando un libro de bronce de un golpe, con una nubecita de polvo.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se tapa los oídos.
- Gheco (gecko de luz cian con antiparras, chiquito) se cae del atril por el golpe.

### Micro-misión R03-N04-P3 · Los cuadrados

```meta
lugar: El grimorio de los números
personajes: Nova, Gheco
carta: Usar el grimorio | AX = el número · call imprimir_numero · mul para el cuadrado
recompensa: xp 20, oro 20
```

#### Escena
La segunda página del grimorio pide una tabla: los números del **1 al 12** y sus **cuadrados**, para medir las baldosas del piso del Gólem.

#### Gheco sugiere
Un bucle con BX de 1 a 12. En cada vuelta: mostrá BX con `imprimir_numero` (AX = BX), un espacio, después BX × BX (`mov ax, bx` y `mul bx`) con `imprimir_numero`, y pasá de renglón con `salto`. Ojo: `mul bx` pisa DX.

#### Desafío
Escribí el bucle donde dice `; tus órdenes`. Las rutinas `imprimir_numero`, `espacio` y `salto` ya están.

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

imprimir_numero proc
    push ax
    push bx
    push cx
    push dx
    mov bx, 10
    mov cx, 0
separar:
    mov dx, 0
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne separar
mostrar:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

espacio proc
    push ax
    push dx
    mov dl, ' '
    mov ah, 02h
    int 21h
    pop dx
    pop ax
    ret
espacio endp

salto proc
    push ax
    push dx
    mov dl, 13
    mov ah, 02h
    int 21h
    mov dl, 10
    int 21h
    pop dx
    pop ax
    ret
salto endp

end main
```

#### Salida esperada
```
1 1
2 4
3 9
4 16
5 25
6 36
7 49
8 64
9 81
10 100
11 121
12 144
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

    mov bx, 1
tabla:
    mov ax, bx
    call imprimir_numero
    call espacio
    mov ax, bx
    mul bx
    call imprimir_numero
    call salto
    inc bx
    cmp bx, 12
    jbe tabla

fin:
    mov ax, 4C00h
    int 21h
main endp

imprimir_numero proc
    push ax
    push bx
    push cx
    push dx
    mov bx, 10
    mov cx, 0
separar:
    mov dx, 0
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne separar
mostrar:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

espacio proc
    push ax
    push dx
    mov dl, ' '
    mov ah, 02h
    int 21h
    pop dx
    pop ax
    ret
espacio endp

salto proc
    push ax
    push dx
    mov dl, 13
    mov ah, 02h
    int 21h
    mov dl, 10
    int 21h
    pop dx
    pop ax
    ret
salto endp

end main
```

#### Al superarla
Doce renglones prolijos, del 1 al 144. —La rutina no sabe para qué la uso —dice Nova—. Solo muestra lo que le paso en AX.

#### Imagen
- Un piso de baldosas de bronce cuadradas de distintos tamaños, encajadas como un rompecabezas.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) mide una baldosa grande con una regla de luz.
- Gheco (gecko de luz cian con antiparras, chiquito) parado en la baldosa más chica.

### Micro-misión R03-N04-P4 · Bajo cero

```meta
lugar: El grimorio de los números
personajes: Nova, Gheco
carta: Con signo | test ax, 8000h = ¿bit 15 prendido? · mostrar '-' · neg ax · imprimir_numero
recompensa: xp 20, oro 20
```

#### Escena
La tercera página es para los números **negativos**: el termómetro de la cueva marca **−200** décimas de grado. `imprimir_numero` mostraría 65336.

#### Gheco sugiere
En `imprimir_con_signo`: si el bit 15 está prendido (`test ax, 8000h` + `jz` para saltar si no), mostrá un `'-'` y dale vuelta el signo con `neg ax`. Al final, siempre, `call imprimir_numero`. Cuidado: la `02h` usa AH, así que guardá AX en la torre mientras mostrás el `'-'`.

#### Desafío
Completá las tres palabras que faltan para que el ojo muestre `-200`.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, -200
    call imprimir_con_signo

fin:
    mov ax, 4C00h
    int 21h
main endp

imprimir_con_signo proc
    push ax
    push dx
    test ax, ___
    jz  positivo
    push ax
    mov dl, '-'
    mov ah, 02h
    int 21h
    pop ax
    ___ ax
positivo:
    call ___
    pop dx
    pop ax
    ret
imprimir_con_signo endp

imprimir_numero proc
    push ax
    push bx
    push cx
    push dx
    mov bx, 10
    mov cx, 0
separar:
    mov dx, 0
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne separar
mostrar:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

end main
```

#### Salida esperada
```
-200
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

    mov ax, -200
    call imprimir_con_signo

fin:
    mov ax, 4C00h
    int 21h
main endp

imprimir_con_signo proc
    push ax
    push dx
    test ax, 8000h
    jz  positivo
    push ax
    mov dl, '-'
    mov ah, 02h
    int 21h
    pop ax
    neg ax
positivo:
    call imprimir_numero
    pop dx
    pop ax
    ret
imprimir_con_signo endp

imprimir_numero proc
    push ax
    push bx
    push cx
    push dx
    mov bx, 10
    mov cx, 0
separar:
    mov dx, 0
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne separar
mostrar:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

end main
```

#### Al superarla
**−200**. Una rutina que llama a otra rutina, y cada una deja la torre como la encontró. —Una función que usa otra función —dice Nova—. Como en cualquier lenguaje.

#### Imagen
- Un termómetro de bronce con escarcha y la columna cian muy abajo, colgado en la pared de una cueva helada.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se abraza a sí misma, con frío.
- Gheco (gecko de luz cian con antiparras, chiquito) con bufanda y gorrito.

### Micro-misión R03-N04-P5 · El número tipeado

```meta
lugar: El grimorio de los números
personajes: Nova, Gheco, Kira
carta: Texto a número | n = n * 10 + cifra · por cada carácter de nombre+2 · validar el rango
recompensa: xp 25, oro 25
```

#### Escena
Kira quiere decirle al Gólem cuántos pasos dar, tipeando un número entero, como **125**. La `0Ah` lo atrapa en la bolsa como texto: `'1'`, `'2'`, `'5'`. Hay que convertirlo en un número de verdad.

#### Gheco sugiere
AX empieza en 0. Por cada carácter de la bolsa (desde `buffer+2`, tantos como dice `buffer+1`): pasalo a número (`sub bl, '0'`), multiplicá AX por 10 (`mul` con un 10 en DI, por ejemplo) y sumale la cifra. Al final, el programa ya muestra el **doble**, para que se note que es un número de verdad.

#### Desafío
Escribí la conversión donde dice `; tus órdenes`. Kira va a tipear `125`.

#### Código inicial
```asm
.model small
.stack 100h
.data
buffer  db 6, ?, 6 dup(?)
pide    db 'Pasos: $'
t_doble db 13, 10, 'Doble: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 0Ah
    lea dx, buffer
    int 21h

    ; tus órdenes (AX = el número)

    add ax, ax
    push ax
    lea dx, t_doble
    mov ah, 09h
    int 21h
    pop ax
    call imprimir_numero

fin:
    mov ax, 4C00h
    int 21h
main endp

imprimir_numero proc
    push ax
    push bx
    push cx
    push dx
    mov bx, 10
    mov cx, 0
separar:
    mov dx, 0
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne separar
mostrar:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

end main
```

#### Entrada
```
125
```

#### Salida esperada
```
Pasos: 125
Doble: 250
```

#### Solución
```asm
.model small
.stack 100h
.data
buffer  db 6, ?, 6 dup(?)
pide    db 'Pasos: $'
t_doble db 13, 10, 'Doble: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 0Ah
    lea dx, buffer
    int 21h

    mov ax, 0
    mov cl, buffer+1
    mov ch, 0
    lea si, buffer+2
    mov di, 10
convertir:
    mov bl, [si]
    sub bl, '0'
    mov bh, 0
    mul di
    add ax, bx
    inc si
    loop convertir

    add ax, ax
    push ax
    lea dx, t_doble
    mov ah, 09h
    int 21h
    pop ax
    call imprimir_numero

fin:
    mov ax, 4C00h
    int 21h
main endp

imprimir_numero proc
    push ax
    push bx
    push cx
    push dx
    mov bx, 10
    mov cx, 0
separar:
    mov dx, 0
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne separar
mostrar:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

end main
```

#### Al superarla
**Doble: 250**. El texto `'1' '2' '5'` ya es un número con el que se puede hacer cuentas. —Es el `int(input())` de Python —dice Gheco—, hecho a mano.

#### Imagen
- Tres fichas de bronce con dibujitos distintos (un punto, dos puntos, cinco puntos) fundiéndose en el aire en una sola moneda grande y brillante.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) mira asombrada.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) con las manos abiertas, guiando la fusión.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre la moneda.

### Micro-misión R03-N04-P6 · El reloj de la estación

```meta
lugar: El grimorio de los números
personajes: Nova, Gheco
carta: div de 16 bits | DX en 0 · div bx · AX = cociente · DX = resto · 3600 s = 1 h · 60 s = 1 min
recompensa: xp 25, oro 25
```

#### Escena
La última página del grimorio es un reloj sin agujas. Marca **3725** segundos, y pide mostrarlos en horas, minutos y segundos.

#### Gheco sugiere
Dividí por 3600 (con `div bx`, DX en 0): el cociente son las **horas** y el resto, los segundos que sobran. Ese resto dividilo por 60: cociente, **minutos**; resto, **segundos**. Mostrá cada uno con `imprimir_numero` y los textos que ya están.

#### Desafío
Escribí las órdenes desde cero, donde dice `; tus órdenes`, para que el ojo muestre `1 h 2 min 5 s`.

#### Código inicial
```asm
.model small
.stack 100h
.data
segundos dw 3725
t_h      db ' h $'
t_min    db ' min $'
t_s      db ' s$'
.code
main proc
    mov ax, @data
    mov ds, ax

    ; tus órdenes

fin:
    mov ax, 4C00h
    int 21h
main endp

imprimir_numero proc
    push ax
    push bx
    push cx
    push dx
    mov bx, 10
    mov cx, 0
separar:
    mov dx, 0
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne separar
mostrar:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

end main
```

#### Salida esperada
```
1 h 2 min 5 s
```

#### Solución
```asm
.model small
.stack 100h
.data
segundos dw 3725
t_h      db ' h $'
t_min    db ' min $'
t_s      db ' s$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, segundos
    mov dx, 0
    mov bx, 3600
    div bx              ; AX = horas, DX = segundos que sobran
    mov si, dx
    call imprimir_numero
    lea dx, t_h
    mov ah, 09h
    int 21h

    mov ax, si
    mov dx, 0
    mov bx, 60
    div bx              ; AX = minutos, DX = segundos
    mov si, dx
    call imprimir_numero
    lea dx, t_min
    mov ah, 09h
    int 21h

    mov ax, si
    call imprimir_numero
    lea dx, t_s
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp

imprimir_numero proc
    push ax
    push bx
    push cx
    push dx
    mov bx, 10
    mov cx, 0
separar:
    mov dx, 0
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne separar
mostrar:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

end main
```

#### Al superarla
Al reloj le crecen agujas de luz: una hora, dos minutos, cinco segundos. El grimorio se cierra solo y se cuelga del cinturón de Nova. —Lo voy a copiar en cada programa —promete.

#### Imagen
- Un reloj redondo de bronce sin números, con agujas de luz cian recién aparecidas.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) con un libro de bronce chico colgado del cinturón.
- Gheco (gecko de luz cian con antiparras, chiquito) colgado de una aguja del reloj.

### Prueba del sello

#### ¿Por qué `imprimir_numero` usa la pila?
Porque las cifras salen al revés (la última primero): se apilan y se muestran al desapilarlas.

#### ¿Qué divide `div bx`, y dónde quedan el cociente y el resto?
Divide DX:AX por BX; el cociente queda en AX y el resto en DX.

#### ¿Por qué `mov dx, 0` va adentro del bucle?
Porque cada `div` deja el resto en DX, y la próxima división lo tomaría como parte del número.

#### ¿Cómo se pasa el texto `"47"` al número 47?
n = 0; n = 0 × 10 + 4 = 4; n = 4 × 10 + 7 = 47.

## R03-N05 · Los atajos del Gólem: macros

```meta
tipo: tema
criatura: slime
padre: R03-N04
precio: 0
temas: prog.funciones, prog.modulos
```

### Crónica

Nova ya escribe `lea dx`, `mov ah, 09h`, `int 21h` tantas veces que lo hace dormida. —¿No hay una forma más corta? —le pregunta a {mentor}.

—Hay **atajos** —dice el Gólem—. Les ponés un nombre a varias órdenes, y cada vez que escribís el nombre, yo pongo las órdenes en su lugar. No las llamo: las **copio**.

### Objetivos

Definir **macros** con parámetros (`macro` … `endm`), usarlas, entender en qué se diferencian de un procedimiento
(se copian, no se llaman), evitar las etiquetas repetidas con `local` y saber cuándo conviene cada uno.

### Antes de empezar

- Las rutinas y la pila (nodos anteriores).

### Explicación

#### Definir y usar
```asm
imprimir macro texto
    push ax
    push dx
    lea dx, texto
    mov ah, 09h
    int 21h
    pop dx
    pop ax
endm
```
Y en el código: `imprimir t_titulo`. Antes de ejecutar, el ensamblador **reemplaza** esa línea por las órdenes de
la macro, con `texto` cambiado por `t_titulo`.
- Las macros se definen **antes** de usarse: arriba de todo, antes de `.model`.
- Pueden tener varios parámetros (`linea car, veces`) o ninguno (`salto`).
- Un parámetro puede ser un número, una palanca o una variable.

#### Macro o procedimiento
| | Macro | Procedimiento |
|---|---|---|
| Cómo se usa | se **copia** en cada uso | se **llama** con `call` |
| Tamaño | el programa crece con cada uso | el código está una sola vez |
| Parámetros | con nombre | por palancas |
| Etiquetas adentro | necesitan `local` | sin problema |

Regla práctica: **macros para cosas cortas** (mostrar un texto, pasar de renglón) y **procedimientos para la
lógica** (convertir números, dibujar).

#### Etiquetas adentro de una macro: `local`
Si una macro tiene una etiqueta y se usa dos veces, la etiqueta aparece dos veces y el ensamblador protesta.
`local otra` le pide que invente un nombre distinto en cada copia:
```asm
esperar macro
    local otra
    mov cx, 3
otra:
    loop otra
endm
```

> **Puente con otras lenguas.** Una macro es el `#define` con parámetros de C: un reemplazo de texto antes de
> compilar. El procedimiento es la función de verdad. En C pasa lo mismo: las macros son rápidas pero traicioneras.

### Código de ejemplo

```asm
imprimir macro texto
    push ax
    push dx
    lea dx, texto
    mov ah, 09h
    int 21h
    pop dx
    pop ax
endm

salto macro
    push ax
    push dx
    mov dl, 13
    mov ah, 02h
    int 21h
    mov dl, 10
    int 21h
    pop dx
    pop ax
endm

.model small
.stack 100h
.data
t_uno db 'Con macros$'
t_dos db 'se escribe menos$'
.code
main proc
    mov ax, @data
    mov ds, ax

    imprimir t_uno
    salto
    imprimir t_dos

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

### Salida esperada

```
Con macros
se escribe menos
```

### ¿Para qué sirve?

Las macros ahorran escritura y hacen el código más fácil de leer: `imprimir saludo` se entiende mejor que tres
órdenes sueltas. Los ensambladores de verdad vienen con bibliotecas de macros, y en C se usan para constantes y
atajos (`#define`).

### Errores habituales

**Slime: la macro usada antes de definirse.** En MASM y en emu8086, si la macro está definida más abajo, el
ensamblador todavía no la conoce y la toma como una palabra rara (`Syntax error: imprimir`). El tablero del Gólem
es más permisivo, pero definilas siempre arriba de todo: así tu código anda en cualquier ensamblador.

**Slime: la etiqueta repetida.** Una macro con etiqueta, usada dos veces:
```
main.asm(14) : Error A2056: Symbol already defined: otra
```
Agregá `local otra` como primera línea de la macro.

**Troll: la macro que pisa palancas.** Como se copia «invisible», si usa AX sin guardarlo, el error es difícil
de ver. Las macros de este nodo hacen `push`/`pop` de lo que usan.

**Orco: el `$` adentro del texto.** `'Precio: $9$'` muestra solo `Precio: `: la `09h` corta en el primer `$`.
Para mostrar un `$`, la `02h`.

### Micro-misión R03-N05-P1 · El primer atajo

```meta
lugar: El taller de atajos
personajes: Nova, Gheco
carta: Usar una macro | nombre_macro parámetro · se reemplaza por sus órdenes antes de ejecutar
recompensa: xp 10, oro 10
```

#### Escena
Gheco ya escribió la macro `imprimir`. Nova solo tiene que **usarla** con el texto del saludo.

#### Gheco sugiere
Escribí el nombre de la macro y, al lado, la variable del texto: `imprimir saludo`.

#### Desafío
Completá la línea para que el ojo muestre el saludo.

#### Código inicial
```asm
imprimir macro texto
    push ax
    push dx
    lea dx, texto
    mov ah, 09h
    int 21h
    pop dx
    pop ax
endm

.model small
.stack 100h
.data
saludo db 'Hola desde un atajo$'
.code
main proc
    mov ax, @data
    mov ds, ax

    ___ saludo

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
Hola desde un atajo
```

#### Solución
```asm
imprimir macro texto
    push ax
    push dx
    lea dx, texto
    mov ah, 09h
    int 21h
    pop dx
    pop ax
endm

.model small
.stack 100h
.data
saludo db 'Hola desde un atajo$'
.code
main proc
    mov ax, @data
    mov ds, ax

    imprimir saludo

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Ejecutalo **paso a paso**: la flechita recorre las órdenes de la macro como si estuvieran escritas ahí mismo. No hay `call` ni `ret`: la macro se **copió**.

#### Imagen
- Un taller de bronce con una prensa que estampa la misma figura de luz cian en varias placas en fila.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) baja la palanca de la prensa.
- Gheco (gecko de luz cian con antiparras, chiquito) acomoda las placas estampadas.

### Micro-misión R03-N05-P2 · El atajo del renglón

```meta
lugar: El taller de atajos
personajes: Nova, Gheco
carta: macro sin parámetros | nombre macro · órdenes · endm · arriba de todo
recompensa: xp 15, oro 15
```

#### Escena
Ahora Nova escribe su propio atajo: `salto`, que pasa de renglón. Sin parámetros.

#### Gheco sugiere
Adentro de la macro: guardá AX y DX, mostrá el 13 y el 10 con la `02h`, y devolvé AX y DX. La primera línea (`salto macro`) y la última (`endm`) ya están.

#### Desafío
Escribí las órdenes de la macro donde dice `; tus órdenes`, para que las dos palabras salgan en dos renglones.

#### Código inicial
```asm
imprimir macro texto
    push ax
    push dx
    lea dx, texto
    mov ah, 09h
    int 21h
    pop dx
    pop ax
endm

salto macro
    ; tus órdenes
endm

.model small
.stack 100h
.data
t_uno db 'Arriba$'
t_dos db 'Abajo$'
.code
main proc
    mov ax, @data
    mov ds, ax

    imprimir t_uno
    salto
    imprimir t_dos

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
Arriba
Abajo
```

#### Solución
```asm
imprimir macro texto
    push ax
    push dx
    lea dx, texto
    mov ah, 09h
    int 21h
    pop dx
    pop ax
endm

salto macro
    push ax
    push dx
    mov dl, 13
    mov ah, 02h
    int 21h
    mov dl, 10
    int 21h
    pop dx
    pop ax
endm

.model small
.stack 100h
.data
t_uno db 'Arriba$'
t_dos db 'Abajo$'
.code
main proc
    mov ax, @data
    mov ds, ax

    imprimir t_uno
    salto
    imprimir t_dos

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Dos atajos, y el programa principal se lee casi como una lista de pedidos. —Imprimir, salto, imprimir —lee Nova en voz alta—. Hasta Kira lo entendería.

#### Imagen
- Dos placas de bronce colgadas en una pared de taller, cada una con un dibujito distinto: una flecha que baja y un globito de diálogo vacío.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) cuelga la segunda placa.
- Gheco (gecko de luz cian con antiparras, chiquito) sostiene el martillo.

### Micro-misión R03-N05-P3 · El precio que se cortó

```meta
lugar: El taller de atajos
personajes: Nova, Gheco
criatura: orc
carta: El $ adentro | la 09h corta en el primer $ · para mostrar un $, la 02h
recompensa: xp 15, oro 15
```

#### Escena
La lavandería de las Forjas le pide al Gólem un cartel con el precio: `Lavado: $9`. Nova usa su atajo `imprimir`, pero el ojo muestra solo `Lavado: `. Un orco se come el resto del cartel.

#### Gheco sugiere
La `09h` termina en el **primer** `$` que encuentra: el del precio. Cortá el texto antes del signo (`'Lavado: $'`), y mostrá el `$` y el 9 aparte con la `02h`.

#### Desafío
Tocá **Ejecutar** y mirá lo que sale. Después arreglá el texto y agregá lo que falta para que el ojo muestre `Lavado: $9`.

#### Código inicial
```asm
imprimir macro texto
    push ax
    push dx
    lea dx, texto
    mov ah, 09h
    int 21h
    pop dx
    pop ax
endm

.model small
.stack 100h
.data
cartel db 'Lavado: $9$'
.code
main proc
    mov ax, @data
    mov ds, ax

    imprimir cartel

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
Lavado: $9
```

#### Solución
```asm
imprimir macro texto
    push ax
    push dx
    lea dx, texto
    mov ah, 09h
    int 21h
    pop dx
    pop ax
endm

.model small
.stack 100h
.data
cartel db 'Lavado: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    imprimir cartel
    mov dl, '$'
    mov ah, 02h
    int 21h
    mov dl, '9'
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El cartel completo cuelga en la puerta de la lavandería. El orco, con la boca llena de pedacitos de cartel, se va masticando.

#### Imagen
- Un cartel de madera liso colgado en la puerta de una lavandería de enanos, con un dibujito de burbujas y una moneda dorada.
- Un orco robusto se aleja masticando un pedazo de cartel.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) clava la mitad que faltaba con un martillito de luz.
- Gheco (gecko de luz cian con antiparras, chiquito) hace burbujas de jabón.

### Micro-misión R03-N05-P4 · La etiqueta repetida

```meta
lugar: El taller de atajos
personajes: Nova, Gheco
criatura: slime
carta: local | local etiqueta = un nombre distinto en cada copia de la macro
recompensa: xp 20, oro 20
```

#### Escena
Nova escribe un atajo `estrellas` que dibuja tres asteriscos con un bucle. Lo usa una vez: bien. Lo usa dos veces y aparece un slime: *«Symbol already defined: otra»*.

#### Gheco sugiere
Cada vez que se usa, la macro se **copia** con su etiqueta `otra:` adentro: dos copias, dos etiquetas iguales. Como primera línea de la macro, `local otra`: el ensamblador le pone un nombre distinto en cada copia.

#### Desafío
Tocá **Ejecutar**, leé el error y arreglá la macro para que el ojo muestre `******`.

#### Código inicial
```asm
estrellas macro
    mov cx, 3
    mov dl, '*'
    mov ah, 02h
otra:
    int 21h
    loop otra
endm

.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    estrellas
    estrellas

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
******
```

#### Solución
```asm
estrellas macro
    local otra
    mov cx, 3
    mov dl, '*'
    mov ah, 02h
otra:
    int 21h
    loop otra
endm

.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    estrellas
    estrellas

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Seis estrellas. El slime se resbala en su propia baba y desaparece por una rendija.

#### Imagen
- Dos filas de tres estrellitas de luz cian flotando en un taller de bronce.
- Un slime verde resbalándose hacia una rendija del piso.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) pega dos etiquetas lisas, una con un triángulo y otra con un círculo, en dos placas iguales.
- Gheco (gecko de luz cian con antiparras, chiquito) se ríe del slime.

### Micro-misión R03-N05-P5 · Sumar y mostrar

```meta
lugar: El taller de atajos
personajes: Nova, Gheco
carta: Macro con dos parámetros | nombre macro a, b · sirve con números, palancas o variables
recompensa: xp 20, oro 20
```

#### Escena
El último atajo del taller: `sumar_y_mostrar a, b`, que muestra la suma de dos números de una cifra. Nova quiere usarlo con números sueltos y con una palanca.

#### Gheco sugiere
Adentro de la macro: `mov dl, a`, `add dl, b`, `add dl, '0'` y la `02h`. Como `a` y `b` se reemplazan tal cual, sirve igual con `3` que con `bl`.

#### Desafío
Escribí las órdenes de la macro donde dice `; tus órdenes`, para que el ojo muestre `75`.

#### Código inicial
```asm
sumar_y_mostrar macro a, b
    ; tus órdenes
endm

.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    sumar_y_mostrar 3, 4
    mov bl, 2
    sumar_y_mostrar bl, 3

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
75
```

#### Solución
```asm
sumar_y_mostrar macro a, b
    mov dl, a
    add dl, b
    add dl, '0'
    mov ah, 02h
    int 21h
endm

.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    sumar_y_mostrar 3, 4
    mov bl, 2
    sumar_y_mostrar bl, 3

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
7 y 5. El taller de atajos queda en silencio, ordenado. —Las macros, para lo corto —repite Nova—. Las rutinas, para lo que piensa.

#### Imagen
- Una estantería de taller con placas de bronce ordenadas, cada una con un dibujito distinto.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se sacude el polvo de las manos, satisfecha.
- Gheco (gecko de luz cian con antiparras, chiquito) duerme sobre la estantería.

### Prueba del sello

#### ¿Qué diferencia hay entre una macro y un procedimiento?
La macro se copia en cada lugar donde se usa; el procedimiento está una sola vez y se llama con `call`.

#### ¿Dónde se definen las macros?
Arriba de todo, antes de usarlas (antes de `.model`).

#### ¿Para qué sirve `local` en una macro?
Para que sus etiquetas tengan un nombre distinto en cada copia.

#### ¿Por qué no se puede mostrar `'Precio: $9$'` con la `09h`?
Porque la `09h` corta en el primer `$`; ese signo se muestra con la `02h`.

## R03-N06 · El ojo del Gólem: pantalla y azar

```meta
tipo: tema
criatura: ogre
padre: R03-N05
precio: 0
temas: maq.interrupciones, prog.matematica-azar
```

### Crónica

El ojo de {mentor} hasta ahora solo escribía de izquierda a derecha, renglón tras renglón, en verde. Nova descubre que tiene más: puede escribir **en cualquier lugar**, y **en colores**.

Y Kira trae un desafío. —Los juegos de las Forjas tienen dados —dice—. ¿El Gólem puede tirar un dado?

—Yo no adivino —contesta el Gólem—. Hago cuentas. —Y Gheco sonríe: —Entonces vamos a hacer una cuenta que **parezca** un dado.

### Objetivos

Usar el BIOS (`int 10h`) para mover el cursor, escribir con color y saber que su escritura no avanza sola;
entender cómo una computadora fabrica números «al azar» con una cuenta y una semilla; y tirar un dado con una
rutina.

### Antes de empezar

- Rutinas y macros (nodos anteriores); `div` y el resto (Las cuentas del Gólem).

### Explicación

#### DOS y el BIOS
El **BIOS** es el programa grabado en la máquina que maneja el hardware. DOS (`int 21h`) se apoya en él: es más
simple. El BIOS (`int 10h`, el video) permite cosas que DOS no hace, como el color o elegir dónde escribir.

| AH | `int 10h` hace | Datos |
|---|---|---|
| `02h` | mueve el cursor | DH = fila (0–24), DL = columna (0–79), BH = 0 |
| `03h` | lee el cursor | devuelve DH = fila y DL = columna |
| `09h` | escribe un carácter **con color** | AL = carácter, BL = color, CX = cuántas veces, BH = 0 |
| `0Eh` | escribe un carácter y avanza | AL = carácter |

La `09h` del BIOS **no mueve el cursor**: si escribís varias letras seguidas, caen todas en el mismo lugar. Hay
que avanzar a mano (leer con `03h`, sumar 1 a la columna y volver a poner con `02h`).

#### Colores
El color es un byte: **fondo × 16 + letra**. Por ejemplo, amarillo (14) sobre azul (1) es `1 * 16 + 14 = 1Eh`.
Algunos: 0 negro, 1 azul, 2 verde, 4 rojo, 7 gris, 10 verde claro, 12 rojo claro, 14 amarillo, 15 blanco.

#### El azar es una cuenta
Una computadora no tira dados: **calcula**. Un generador muy usado hace, una y otra vez:
```
semilla = semilla * 25173 + 13849      (en 16 bits: lo que se pasa, se pierde)
```
La secuencia **parece** al azar, pero si la semilla empieza igual, sale **siempre igual**. Por eso los juegos
toman la semilla del **reloj** (`int 21h`, función `2Ch`). Acá usamos una semilla fija, para que el resultado se
pueda comprobar. Para un número de 0 a N−1 se usa el **resto** de dividir por N.

> **Puente con otras lenguas.** El `random` de Python, el `rand()` de C y el `Math.random()` de JavaScript son
> generadores como este: una cuenta con una semilla. `random.seed(42)` hace que salga siempre lo mismo, justamente
> para poder probar.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
semilla dw 1234
t_dado  db 'Cinco dados: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_dado
    mov ah, 09h
    int 21h

    mov cx, 5
tirar:
    mov bl, 6
    call azar            ; AL = de 0 a 5
    add al, '1'          ; de '1' a '6'
    mov dl, al
    mov ah, 02h
    int 21h
    mov dl, ' '
    int 21h
    loop tirar

fin:
    mov ax, 4C00h
    int 21h
main endp

; azar: AL = número de 0 a BL-1 (avanza la semilla)
azar proc
    push dx
    mov ax, semilla
    mov dx, 25173
    mul dx
    add ax, 13849
    mov semilla, ax
    mov al, ah           ; el byte alto (los bits bajos se repiten mucho)
    mov ah, 0
    div bl
    mov al, ah           ; el resto
    pop dx
    ret
azar endp

end main
```

### Salida esperada

```
Cinco dados: 4 2 1 1 4
```

### ¿Para qué sirve?

Los dados de los juegos, las cartas mezcladas, los enemigos que aparecen en lugares distintos, las simulaciones y
hasta la criptografía usan generadores de números. Saber que son una cuenta explica por qué en los juegos se usa
la hora como semilla, y por qué con la misma semilla se puede repetir una partida exacta.

### Errores habituales

**Ogro: el cursor que no avanza.** Escribir varias letras con la `09h` del BIOS sin mover el cursor: caen todas en
el mismo lugar y solo se ve la última.

**Ogro: BH con basura.** La `02h` y la `09h` usan BH como página de video. Si no vale 0, se escribe en una página
que no se ve.

**Ogro: la semilla fija en un juego.** Si te olvidás de leer el reloj, todas las partidas salen iguales. (Para
probar, en cambio, es justo lo que querés.)

**Ogro: los bits bajos.** Usar el bit 0 de la semilla para cara o cruz da siempre cara, cruz, cara, cruz… Por eso
`azar` usa el byte alto.

### Micro-misión R03-N06-P1 · Escribir donde quiero

```meta
lugar: El ojo del Gólem
personajes: Nova, Gheco
carta: int 10h, 02h | mueve el cursor · DH = fila · DL = columna · BH = 0 · se cuenta desde 0
recompensa: xp 10, oro 10
```

#### Escena
Nova quiere marcar en el ojo dónde está el tesoro del mapa: en la **fila 2**, **columna 5**. Arriba, el título.

#### Gheco sugiere
Con `mov ah, 02h` e `int 10h` el cursor salta adonde digan DH (fila) y DL (columna), con BH en 0. Las filas y columnas se cuentan desde **0**. Después, lo que escribas sale ahí.

#### Desafío
Completá la fila y la columna para que la X quede en el lugar del tesoro.

#### Código inicial
```asm
.model small
.stack 100h
.data
titulo db 'Mapa:$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, titulo
    mov ah, 09h
    int 21h

    mov ah, 02h
    mov bh, 0
    mov dh, ___          ; fila
    mov dl, ___          ; columna
    int 10h

    mov dl, 'X'
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
Mapa:

     X
```

#### Solución
```asm
.model small
.stack 100h
.data
titulo db 'Mapa:$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, titulo
    mov ah, 09h
    int 21h

    mov ah, 02h
    mov bh, 0
    mov dh, 2            ; fila
    mov dl, 5            ; columna
    int 10h

    mov dl, 'X'
    mov ah, 02h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
La X aparece justo donde estaba el tesoro. —El ojo es una grilla —dice Nova—: 80 columnas y 25 filas.

#### Imagen
- Un ojo redondo de cristal gigante visto de cerca, con una grilla tenue de luz cian y una X brillante en un cuadrito.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) señala la X desde adentro del ojo.
- Gheco (gecko de luz cian con antiparras, chiquito) con un mapa enrollado bajo el brazo.

### Micro-misión R03-N06-P2 · La barra de vida

```meta
lugar: El ojo del Gólem
personajes: Nova, Gheco
carta: int 10h, 09h | AL = carácter · BL = color · CX = cuántas veces · BH = 0 · no mueve el cursor
recompensa: xp 15, oro 15
```

#### Escena
Para los juegos de Kira, el ojo tiene que mostrar una **barra de vida**: cinco bloques en **rojo claro**.

#### Gheco sugiere
La `09h` del BIOS escribe AL, con el color de BL, CX veces seguidas. El rojo claro es el **12** (fondo negro: 0 × 16 + 12).

#### Desafío
Completá el color y la cantidad para que el ojo muestre cinco `#` en rojo claro.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ah, 09h
    mov al, '#'
    mov bh, 0
    mov bl, ___          ; el color
    mov cx, ___          ; cuántas veces
    int 10h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
#####
```

#### Estado esperado
```
BL = 12
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

    mov ah, 09h
    mov al, '#'
    mov bh, 0
    mov bl, 12           ; el color
    mov cx, 5            ; cuántas veces
    int 10h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Cinco bloques rojos en el ojo del Gólem. Kira silba. —Ahora sí parece un juego.

#### Imagen
- Un ojo de cristal gigante con una barra horizontal de cinco bloques rojos brillando adentro.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) mira desde afuera, con los brazos cruzados y una sonrisa.
- Gheco (gecko de luz cian con antiparras, chiquito) en su hombro, señalando la barra.

### Micro-misión R03-N06-P3 · El nombre que se pisa

```meta
lugar: El ojo del Gólem
personajes: Nova, Gheco
criatura: ogre
carta: Avanzar el cursor | la 09h del BIOS no avanza · leer con 03h · inc dl · poner con 02h
recompensa: xp 20, oro 20
```

#### Escena
Nova quiere escribir su nombre en colores, letra por letra. El ojo muestra solo una **A**: las cuatro letras cayeron en el mismo lugar, una encima de la otra. Un ogro se ríe en la oscuridad.

#### Gheco sugiere
La `09h` del BIOS no mueve el cursor. Gheco ya escribió la rutina `avanzar`, que lo corre un lugar a la derecha. Llamala después de escribir **cada** letra.

#### Desafío
Tocá **Ejecutar** y mirá lo que sale. Después agregá la llamada que falta para que el ojo muestre `NOVA`.

#### Código inicial
```asm
.model small
.stack 100h
.data
nombre db 'NOVA'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, nombre
    mov cx, 4
letra:
    push cx
    mov ah, 09h
    mov al, [si]
    mov bh, 0
    mov bl, 0Bh
    mov cx, 1
    int 10h
    pop cx
    inc si
    loop letra

fin:
    mov ax, 4C00h
    int 21h
main endp

; avanzar: corre el cursor una columna a la derecha
avanzar proc
    push ax
    push bx
    push cx
    push dx
    mov ah, 03h
    mov bh, 0
    int 10h
    inc dl
    mov ah, 02h
    int 10h
    pop dx
    pop cx
    pop bx
    pop ax
    ret
avanzar endp

end main
```

#### Salida esperada
```
NOVA
```

#### Solución
```asm
.model small
.stack 100h
.data
nombre db 'NOVA'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, nombre
    mov cx, 4
letra:
    push cx
    mov ah, 09h
    mov al, [si]
    mov bh, 0
    mov bl, 0Bh
    mov cx, 1
    int 10h
    call avanzar
    pop cx
    inc si
    loop letra

fin:
    mov ax, 4C00h
    int 21h
main endp

; avanzar: corre el cursor una columna a la derecha
avanzar proc
    push ax
    push bx
    push cx
    push dx
    mov ah, 03h
    mov bh, 0
    int 10h
    inc dl
    mov ah, 02h
    int 10h
    pop dx
    pop cx
    pop bx
    pop ax
    ret
avanzar endp

end main
```

#### Al superarla
**NOVA**, en celeste brillante, letra por letra. Nova se queda mirando su nombre un rato largo, en silencio.

#### Imagen
- Cuatro símbolos de luz celeste brillante en fila dentro de un ojo de cristal gigante, cada uno distinto: una estrella, un círculo, una flecha y un triángulo.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) mira emocionada, con las manos en el pecho.
- Un ogro grandote se aleja en la oscuridad, de espaldas.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre el hombro de Nova.

### Micro-misión R03-N06-P4 · La misma semilla

```meta
lugar: El ojo del Gólem
personajes: Nova, Gheco, Kira
carta: Generador | semilla = semilla * 25173 + 13849 · misma semilla, misma secuencia · se toma el byte alto
recompensa: xp 15, oro 15
```

#### Escena
Kira tira el dado del Gólem dos veces y salen **los mismos números**. —¡Está trucado! —protesta. Nova revisa: la semilla empieza siempre en el mismo número.

#### Gheco sugiere
Mirá la rutina `azar`: la cuenta es `semilla * 25173 + 13849`. Completá los dos números. Después ejecutalo dos veces: sale siempre lo mismo, porque la semilla empieza igual.

#### Desafío
Completá la cuenta del generador para que el ojo muestre los cinco dados de la semilla 1234.

#### Código inicial
```asm
.model small
.stack 100h
.data
semilla dw 1234
.code
main proc
    mov ax, @data
    mov ds, ax

    mov cx, 5
tirar:
    mov bl, 6
    call azar
    add al, '1'
    mov dl, al
    mov ah, 02h
    int 21h
    loop tirar

fin:
    mov ax, 4C00h
    int 21h
main endp

azar proc
    push dx
    mov ax, semilla
    mov dx, ___
    mul dx
    add ax, ___
    mov semilla, ax
    mov al, ah
    mov ah, 0
    div bl
    mov al, ah
    pop dx
    ret
azar endp

end main
```

#### Salida esperada
```
42114
```

#### Solución
```asm
.model small
.stack 100h
.data
semilla dw 1234
.code
main proc
    mov ax, @data
    mov ds, ax

    mov cx, 5
tirar:
    mov bl, 6
    call azar
    add al, '1'
    mov dl, al
    mov ah, 02h
    int 21h
    loop tirar

fin:
    mov ax, 4C00h
    int 21h
main endp

azar proc
    push dx
    mov ax, semilla
    mov dx, 25173
    mul dx
    add ax, 13849
    mov semilla, ax
    mov al, ah
    mov ah, 0
    div bl
    mov al, ah
    pop dx
    ret
azar endp

end main
```

#### Al superarla
4, 2, 1, 1, 4. Y otra vez: 4, 2, 1, 1, 4. —No está trucado —le explica Nova a Kira—: es una cuenta. Para que cambie, la semilla tiene que salir del reloj.

#### Imagen
- Dos dados de bronce rodando lado a lado, idénticos, con la misma cara arriba.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) con el ceño fruncido, desconfiada.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) le explica con las manos abiertas.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre un dado, mareado.

### Micro-misión R03-N06-P5 · La moneda de las Forjas

```meta
lugar: El ojo del Gólem
personajes: Nova, Gheco
carta: Usar azar | BL = cuántos resultados · call azar · AL de 0 a BL-1
recompensa: xp 20, oro 20
```

#### Escena
En las Forjas, las discusiones se resuelven tirando una moneda: **C** (cara) o **X** (cruz). Nova quiere que el Gólem tire 6 veces y cuente las caras.

#### Gheco sugiere
`azar` con BL = 2 devuelve 0 o 1. Si es 0, mostrá `'C'` y sumá una cara en DI; si no, `'X'`. Hacelo 6 veces con un `loop`. Al final, mostrá las caras con `+ '0'`.

#### Desafío
Escribí el bucle donde dice `; tus órdenes`. La semilla es la 2026.

#### Código inicial
```asm
.model small
.stack 100h
.data
semilla dw 2026
t_caras db 13, 10, 'Caras: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov di, 0
    ; tus órdenes

    lea dx, t_caras
    mov ah, 09h
    int 21h
    mov dx, di
    add dl, '0'
    mov ah, 02h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp

azar proc
    push dx
    mov ax, semilla
    mov dx, 25173
    mul dx
    add ax, 13849
    mov semilla, ax
    mov al, ah
    mov ah, 0
    div bl
    mov al, ah
    pop dx
    ret
azar endp

end main
```

#### Salida esperada
```
CXXXXC
Caras: 2
```

#### Solución
```asm
.model small
.stack 100h
.data
semilla dw 2026
t_caras db 13, 10, 'Caras: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov di, 0
    mov cx, 6
tirar:
    mov bl, 2
    call azar
    cmp al, 0
    jne cruz
    mov dl, 'C'
    inc di
    jmp mostrar
cruz:
    mov dl, 'X'
mostrar:
    mov ah, 02h
    int 21h
    loop tirar

    lea dx, t_caras
    mov ah, 09h
    int 21h
    mov dx, di
    add dl, '0'
    mov ah, 02h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp

azar proc
    push dx
    mov ax, semilla
    mov dx, 25173
    mul dx
    add ax, 13849
    mov semilla, ax
    mov al, ah
    mov ah, 0
    div bl
    mov al, ah
    pop dx
    ret
azar endp

end main
```

#### Al superarla
Dos caras y cuatro cruces, con las caras en las puntas. Kira pierde la apuesta y le toca lavar los platos de la torre. Mientras los lava, nota algo: al fondo de la torre, en la oscuridad, **algo se mueve**.

#### Imagen
- Una moneda dorada girando en el aire, con una cara grabada con un sol y la otra con una luna.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) lava platos de metal con las mangas arremangadas, mirando de reojo hacia la oscuridad.
- Al fondo, en la penumbra, dos ojos grandes y grises.
- Gheco (gecko de luz cian con antiparras, chiquito) se esconde detrás de una pila de platos.

### Prueba del sello

#### ¿Qué hace la función `02h` de la `int 10h`?
Mueve el cursor a la fila DH y la columna DL (con BH = 0).

#### ¿Por qué hay que mover el cursor a mano después de la `09h` del BIOS?
Porque esa función escribe con color pero no avanza el cursor.

#### ¿Cómo se arma el color amarillo sobre azul?
Fondo × 16 + letra: 1 × 16 + 14 = 1Eh.

#### Si la semilla empieza siempre igual, ¿qué pasa con los números «al azar»?
Salen siempre iguales: el generador es una cuenta.

## R03-N07 · Jefe: el Troll de la Pila

```meta
tipo: jefe
criatura: troll
padre: R03-N06
precio: 0
insignia: Sello del Troll
insignia_descripcion: Venciste al Troll de la Pila: tus rutinas guardan, devuelven y vuelven siempre a su lugar.
usa: maq.pila, prog.funciones, col.pilas-colas
temas: cal.depuracion
```

### Crónica

Al fondo de la torre de platos, en la oscuridad, vive el **Troll de la Pila**. Es enorme, gris, lento, y se alimenta de platos que nadie viene a buscar: cada `push` sin su `pop` lo hace más fuerte.

—Si lo dejo crecer —dice {mentor}—, un día voy a querer volver de un paso y no voy a saber adónde. Y me caigo.

El troll se sienta sobre la torre y la sacude. Los platos tiemblan. Nova respira hondo: la torre es suya, y la va a dejar **pareja**.

### Objetivos

Vencer al jefe de la rama: encontrar y arreglar los errores de la pila (torres desparejas, rutinas que pisan
palancas, `pop` en el orden equivocado) y escribir programas que usen la pila y las rutinas como herramientas.

### Antes de empezar

Toda la rama: la pila, las rutinas, las rutinas que cuidan sus palancas, el grimorio, las macros y la pantalla.

### Explicación

#### Cómo se caza un troll
Los errores de la pila tienen un síntoma clásico: el Gólem **vuelve a cualquier lado** («saltó a una dirección sin
órdenes») o se queda dando vueltas. El método:

1. **Contá los platos**: en cada rutina, ¿cuántos `push` hay y cuántos `pop` antes de cada `ret`? Tienen que ser
   los mismos.
2. **Mirá el orden**: los `pop` van al revés que los `push`.
3. **Mirá la pestaña Pila** paso a paso: justo antes de un `ret`, arriba de todo tiene que estar el lugar de
   vuelta que dejó el `call`.
4. **Revisá qué palancas usa cada rutina** y si quien la llama las necesitaba.

> **Puente con otras lenguas.** El «stack overflow» de Java o Python y la «violación de segmento» de C muchas
> veces vienen de acá: una pila que creció sin control o una función que volvió adonde no debía. Los lenguajes de
> alto nivel te cuidan la pila; acá la cuidás vos.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
pal db 'NEUQUEN'
t_si db 'Se lee igual al reves.$'
t_no db 'No se lee igual al reves.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, pal
    mov cx, 7
apilar:
    mov al, [si]
    push ax
    inc si
    loop apilar

    lea si, pal
    mov cx, 7
    mov bl, 1            ; 1 = por ahora sí
comparar:
    pop ax
    cmp al, [si]
    je  igual
    mov bl, 0
igual:
    inc si
    loop comparar

    lea dx, t_si
    cmp bl, 1
    je  mostrar
    lea dx, t_no
mostrar:
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
Se lee igual al reves.
```

### ¿Para qué sirve?

Las pilas están en el centro de la computación: las llamadas a funciones, el «deshacer» de los editores, el botón
«atrás» del navegador, la evaluación de expresiones y la recursión. Quien entiende la pila del 8086 entiende qué
pasa por debajo de todas.

### Errores habituales

**Troll: la torre despareja.** Un `push` sin `pop` antes del `ret`: el Gólem vuelve a cualquier lado.

**Troll: la rutina que pisa.** Usa CX (o BX, o SI) sin guardarlo, y rompe el bucle de quien la llamó.

**Troll: desapilar de más.** Un `pop` con la torre vacía saca basura (o el lugar de vuelta de otro).

### Micro-misión R03-N07-P1 · La rutina dentro de la rutina

```meta
lugar: La base de la torre
personajes: Nova, Gheco
criatura: troll
carta: Contar platos | cada rutina: tantos pop como push antes del ret · también las de adentro
recompensa: xp 25, oro 25
```

#### Escena
El troll se mete en una rutina que llama a otra: `saludar` llama a `inicial`. El Gólem muestra la N… y salta a cualquier lado. El troll ríe con un ruido de platos rotos.

#### Gheco sugiere
Contá los platos de **cada** rutina, la de afuera y la de adentro. En una de las dos hay un `push` que nunca se devuelve antes del `ret`.

#### Desafío
Tocá **Ejecutar** y leé el aviso. Después encontrá la rutina despareja y arreglala para que el ojo muestre `N.` y el programa termine bien.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    call saludar

fin:
    mov ax, 4C00h
    int 21h
main endp

saludar proc
    push dx
    call inicial
    mov dl, '.'
    mov ah, 02h
    int 21h
    pop dx
    ret
saludar endp

inicial proc
    push ax
    push dx
    mov dl, 'N'
    mov ah, 02h
    int 21h
    pop dx
    ret
inicial endp

end main
```

#### Salida esperada
```
N.
```

#### Estado esperado
```
SP = 100h
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

    call saludar

fin:
    mov ax, 4C00h
    int 21h
main endp

saludar proc
    push dx
    call inicial
    mov dl, '.'
    mov ah, 02h
    int 21h
    pop dx
    ret
saludar endp

inicial proc
    push ax
    push dx
    mov dl, 'N'
    mov ah, 02h
    int 21h
    pop dx
    pop ax
    ret
inicial endp

end main
```

#### Al superarla
La torre deja de temblar. El troll se rasca la cabeza: le sacaron un plato de las manos.

#### Imagen
- Un troll enorme y gris, de piel como piedra, sentado sobre la base de una torre de platos de metal, con un plato en cada mano.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) le saca uno de los platos con firmeza.
- Gheco (gecko de luz cian con antiparras, chiquito) cuenta los platos de la torre con la cola.

### Micro-misión R03-N07-P2 · El contador robado

```meta
lugar: La base de la torre
personajes: Nova, Gheco
criatura: troll
carta: La rutina que pisa | si la rutina usa BX o CX, push al entrar y pop al salir
recompensa: xp 25, oro 25
```

#### Escena
El programa tendría que mostrar las cifras del 1 al 4 llamando a `cifra` en cada vuelta, pero muestra cualquier cosa. El troll se guardó algo en el bolsillo.

#### Gheco sugiere
El bucle de afuera usa **BL** para la cifra y **CX** para las vueltas. Mirá qué palancas toca `cifra` sin guardarlas.

#### Desafío
Ejecutá paso a paso, encontrá la palanca robada y arreglá la rutina para que el ojo muestre `1234`.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bl, 1
    mov cx, 4
vuelta:
    call cifra
    inc bl
    loop vuelta

fin:
    mov ax, 4C00h
    int 21h
main endp

; cifra: muestra BL (0 a 9) como carácter
cifra proc
    push ax
    push dx
    mov bh, 0
    add bx, '0'
    mov dl, bl
    mov ah, 02h
    int 21h
    pop dx
    pop ax
    ret
cifra endp

end main
```

#### Salida esperada
```
1234
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

    mov bl, 1
    mov cx, 4
vuelta:
    call cifra
    inc bl
    loop vuelta

fin:
    mov ax, 4C00h
    int 21h
main endp

; cifra: muestra BL (0 a 9) como carácter
cifra proc
    push ax
    push bx
    push dx
    mov bh, 0
    add bx, '0'
    mov dl, bl
    mov ah, 02h
    int 21h
    pop dx
    pop bx
    pop ax
    ret
cifra endp

end main
```

#### Al superarla
1, 2, 3, 4. El troll vacía el bolsillo, de mala gana: adentro estaba BX.

#### Imagen
- Un troll enorme y gris vaciando un bolsillo de cuero, del que caen engranajes y una palanquita de bronce.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) atrapa la palanquita en el aire.
- Gheco (gecko de luz cian con antiparras, chiquito) le señala el otro bolsillo al troll, desconfiado.

### Micro-misión R03-N07-P3 · Deshacer

```meta
lugar: La base de la torre
personajes: Nova, Gheco, Kira
criatura: troll
carta: Pila con cuidado | apilar letras · '<' desapila la última · nunca desapilar con la torre vacía
recompensa: xp 30, oro 30
```

#### Escena
El troll tiene una última trampa: un **editor** con botón de deshacer. Kira escribe letras hasta un punto, y cada **<** borra la última. Si el editor desapila con la torre vacía, el troll se queda con el lugar de vuelta del Gólem.

#### Gheco sugiere
Llevá la cuenta de cuántas letras hay en la torre (en BX). Leé teclas hasta el `'.'`: si es `'<'`, desapilá **solo si BX no es 0** (y restale 1); si es otra cosa, apilala (y sumale 1). Al final, desapilá BX letras y mostralas: salen al revés, como en la torre.

#### Desafío
Escribí las órdenes desde cero, donde dice `; tus órdenes`. Kira va a tipear `<`, `a`, `b`, `<`, `c`, `d` y `.`.

#### Código inicial
```asm
.model small
.stack 100h
.data
t_queda db 13, 10, 'Queda (al reves): $'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bx, 0
    ; tus órdenes

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Entrada
```
<
a
b
<
c
d
.
```

#### Salida esperada
```
<ab<cd.
Queda (al reves): dca
```

#### Estado esperado
```
SP = 100h
```

#### Solución
```asm
.model small
.stack 100h
.data
t_queda db 13, 10, 'Queda (al reves): $'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bx, 0
leer:
    mov ah, 01h
    int 21h
    cmp al, '.'
    je  listo
    cmp al, '<'
    jne apilar
    cmp bx, 0
    je  leer             ; torre vacía: no se desapila nada
    pop dx
    dec bx
    jmp leer
apilar:
    push ax
    inc bx
    jmp leer
listo:

    lea dx, t_queda
    mov ah, 09h
    int 21h
    mov cx, bx
    jcxz vacio
mostrar:
    pop dx
    mov ah, 02h
    int 21h
    loop mostrar
vacio:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
«dca». La torre queda pareja, plato por plato. El troll se levanta despacio, se sacude el polvo y, por primera vez, **ordena** él mismo un plato arriba de la torre. Después se va caminando hacia la oscuridad, satisfecho, como quien terminó su trabajo.

—Ya no me necesitás —dice desde lejos.

{mentor} da un paso. Otro. Otro más. Y esta vez, sabe volver. Las Forjas enteras tiemblan: **el Gólem camina**, aunque todavía con cuidado, como quien aprende.

—Ahora —dice Nova— quiero que haga algo **con** todo esto.

#### Imagen
- Un gólem de bronce gigante caminando por una caverna enorme, dejando huellas, con las Forjas iluminadas al fondo.
- Abajo, un troll gris enorme se aleja hacia la oscuridad, saludando con una mano.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) camina al lado del pie del gólem, mirando hacia arriba.
- En el pecho abierto del gólem, Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) y Gheco (gecko de luz cian con antiparras, chiquito) festejan.

### Prueba del sello

#### ¿Cuál es el síntoma típico de una pila despareja en una rutina?
El Gólem vuelve a cualquier lado («saltó a una dirección sin órdenes») o se cuelga.

#### ¿Qué hay que revisar en cada rutina para cazar un troll?
Que haya tantos `pop` como `push` antes de cada `ret`, en orden inverso, y que guarde las palancas que usa.

#### ¿Qué pasa si se hace `pop` con la torre vacía?
Se saca basura, o el lugar de vuelta de una rutina.

#### ¿Cómo se sabe si una palabra es palíndromo con la pila?
Se apilan las letras y se comparan, al desapilarlas, con la palabra original.
