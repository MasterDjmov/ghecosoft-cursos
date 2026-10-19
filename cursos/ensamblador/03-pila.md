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
