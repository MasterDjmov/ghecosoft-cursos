# RAMA R04 · Proyectos: el Gólem trabaja

```meta
tipo: tronco
posicion: 4
```

## R04-N01 · Proyecto: la calculadora del Gremio

```meta
tipo: tema
criatura: ogre
padre: R03-N07
precio: 0
temas: prog.menu, err.validacion
usa: prog.funciones, prog.condicionales, prog.bucles, prog.entrada, prog.salida
```

### Crónica

El Gólem camina, y la noticia llega al **Gremio de Comerciantes** de las Forjas. Al día siguiente, una comitiva de enanos con balanzas y libros de cuentas se planta frente a {mentor}.

—Dicen que hacés cuentas —dice la jefa del Gremio—. Necesitamos una **calculadora**: sumar, restar, multiplicar y dividir números grandes. Y que no se rompa cuando alguien se equivoca. —Mira de reojo a su comitiva—. Nos equivocamos mucho.

Nova acepta. Es su primer trabajo **de verdad**.

### Objetivos

Armar un programa completo, pieza por pieza: un **menú que se repite**, números de varias cifras y **todos los
errores contemplados** (opción que no existe, número mal escrito, resultado que no entra en 16 bits, resta
negativa y división por cero).

### Antes de empezar

- Decisiones, bucles y rutinas (ramas anteriores) y el grimorio de los números.

### Explicación

#### Un programa grande, hecho de piezas chicas
```
main:            el menú que se repite: leer la opción, 0 sale, 1 a 4 elige, lo demás «no existe»
pedir_numeros:   num1 y num2 (repite hasta que sean válidos)
sumar, restar, multiplicar, dividir: una operación cada una, con su error
grimorio:        imprimir_numero, leer_numero, nueva_linea, mostrar_cadena
```
El programa principal solo **decide**; cada operación es una rutina. Así cada parte se prueba sola y los saltos
quedan cortos.

#### Cada operación y su error
| Operación | Cómo | Qué puede salir mal | Cómo se detecta |
|---|---|---|---|
| suma | `add ax, num2` | pasa de 65.535 | CF = 1 → `jc` |
| resta | `sub ax, num2` | num1 < num2 (negativo) | `cmp` + `jae`; si no, se muestra `-` y `num2 − num1` |
| multiplicación | `mul num2` → DX:AX | no entra en 16 bits | CF = 1 → `jc` |
| división | `div num2` → AX, resto en DX | divisor 0 | se compara **antes** de dividir |

La división por cero **no se ataja después**: el Gólem se detiene. Hay que mirarla antes.

#### Variables en vez de palancas
`num1` y `num2` son variables (`dw`): pasan por muchas rutinas, y en palancas se pisarían. Las operaciones las leen
directo (`add ax, num2`, `mul num2`, `div num2`).

> **Puente con otras lenguas.** Este es el mismo programa que se hace en el primer año de cualquier carrera, en
> Python, C o Java: un menú, validación y casos de error. La diferencia es que acá ves **todo** lo que hay
> debajo: cada `if`, cada bucle y cada función.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
num1     dw 1250
num2     dw 750
t_mas    db ' + $'
t_igual  db ' = $'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, num1
    call imprimir_numero
    lea dx, t_mas
    call mostrar_cadena
    mov ax, num2
    call imprimir_numero
    lea dx, t_igual
    call mostrar_cadena
    mov ax, num1
    add ax, num2
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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

### Salida esperada

```
1250 + 750 = 2000
```

### ¿Para qué sirve?

Así se arma cualquier programa de verdad: piezas chicas que se prueban de a una y un programa principal que las
combina. Y así se piensa en los errores: qué puede escribir mal una persona, qué cuenta puede desbordar, qué no se
puede hacer nunca (dividir por cero).

### Errores habituales

**Ogro: el desborde que no se mira.** `add` o `mul` sin `jc` después: 60.000 + 7.000 muestra 1.464, como si nada.

**Ogro: la resta negativa.** 300 − 1.000 sin signo da 64.836. Hay que comparar antes y mostrar el `-`.

**Ogro: dividir por cero.** Detiene el Gólem; se compara con 0 **antes** del `div`.

**Orco: el salto demasiado largo.** Un salto condicional llega solo hasta 127 bytes. Si el programa principal crece
mucho, los saltos no llegan: por eso cada operación va en su rutina.

### Micro-misión R04-N01-P1 · El menú del Gremio

```meta
lugar: La sala del Gremio
personajes: Nova, Gheco
carta: Menú con rango | cmp con '0' y '4' · lo de afuera: «no existe» · como el default de un switch
```

#### Escena
La jefa del Gremio prueba el menú y aprieta el **9**. —¿Y esto? —pregunta. El Gólem tiene que contestar que esa opción no existe.

#### Gheco sugiere
Las opciones válidas van del `'0'` al `'4'`. Lo que sea menor que `'0'` o mayor que `'4'` va a `no_existe`.

#### Desafío
Completá el rango para que, con el `9`, el ojo diga que la opción no existe.

#### Código inicial
```asm
.model small
.stack 100h
.data
menu db '1) Sumar 2) Restar 3) Multiplicar 4) Dividir 0) Salir', 13, 10, 'Opcion: $'
t_ok db 13, 10, 'Opcion elegida.$'
t_no db 13, 10, 'Esa opcion no existe.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, menu
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h

    cmp al, ___
    jb  no_existe
    cmp al, ___
    ja  no_existe
    lea dx, t_ok
    jmp mostrar
no_existe:
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

#### Entrada
```
9
```

#### Salida esperada
```
1) Sumar 2) Restar 3) Multiplicar 4) Dividir 0) Salir
Opcion: 9
Esa opcion no existe.
```

#### Solución
```asm
.model small
.stack 100h
.data
menu db '1) Sumar 2) Restar 3) Multiplicar 4) Dividir 0) Salir', 13, 10, 'Opcion: $'
t_ok db 13, 10, 'Opcion elegida.$'
t_no db 13, 10, 'Esa opcion no existe.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, menu
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h

    cmp al, '0'
    jb  no_existe
    cmp al, '4'
    ja  no_existe
    lea dx, t_ok
    jmp mostrar
no_existe:
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

#### Al superarla
—Esa opción no existe —repite la jefa, leyendo el ojo—. Bien. Los de mi comitiva van a apretar cualquier cosa.

#### Imagen
- Una sala de reuniones de enanos con una mesa larga, balanzas y libros de cuentas cerrados.
- La jefa del Gremio, una enana robusta con anteojos redondos y un chaleco con muchos bolsillos, aprieta una tecla de bronce con desconfianza.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se asoma por el ojo de un gólem gigante que ocupa el fondo de la sala.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre la mesa, al lado de una balanza.

### Micro-misión R04-N01-P2 · La suma que se pasó

```meta
lugar: La sala del Gremio
personajes: Nova, Gheco
criatura: ogre
carta: jc después de add | si la suma pasa de 65535, CF = 1 · mirarlo enseguida
```

#### Escena
Un comerciante suma sus dos depósitos: **60.000** y **7.000**. El Gólem contesta, muy tranquilo, **1464**. El comerciante se desmaya. Un ogro, en el fondo, aplaude.

#### Gheco sugiere
La suma no entra en 16 bits: AX dio la vuelta y se prendió **CF**. Justo después del `add`, un `jc desborde` salta al mensaje de error.

#### Desafío
Tocá **Ejecutar** y mirá el resultado. Después agregá el salto que falta para que el Gólem avise que no entra.

#### Código inicial
```asm
.model small
.stack 100h
.data
num1     dw 60000
num2     dw 7000
t_mas    db ' + $'
t_igual  db ' = $'
t_grande db 'El resultado no entra en 16 bits.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, num1
    call imprimir_numero
    lea dx, t_mas
    call mostrar_cadena
    mov ax, num2
    call imprimir_numero
    lea dx, t_igual
    call mostrar_cadena

    mov ax, num1
    add ax, num2
    call imprimir_numero
    jmp listo
desborde:
    call nueva_linea
    lea dx, t_grande
    call mostrar_cadena
listo:

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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Salida esperada
```
60000 + 7000 =
El resultado no entra en 16 bits.
```

#### Solución
```asm
.model small
.stack 100h
.data
num1     dw 60000
num2     dw 7000
t_mas    db ' + $'
t_igual  db ' = $'
t_grande db 'El resultado no entra en 16 bits.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, num1
    call imprimir_numero
    lea dx, t_mas
    call mostrar_cadena
    mov ax, num2
    call imprimir_numero
    lea dx, t_igual
    call mostrar_cadena

    mov ax, num1
    add ax, num2
    jc  desborde
    call imprimir_numero
    jmp listo
desborde:
    call nueva_linea
    lea dx, t_grande
    call mostrar_cadena
listo:

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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Al superarla
El comerciante se despierta y lee el aviso. —Bueno —suspira—, por lo menos no me mintió.

#### Imagen
- Un comerciante enano desmayado en una silla, con un abanico de papel liso en la mano.
- Un ogro grandote y torpe aplaude en el fondo de la sala.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) sacude la mano para despertar al comerciante.
- Gheco (gecko de luz cian con antiparras, chiquito) le acerca un vaso de agua.

### Micro-misión R04-N01-P3 · La resta negativa

```meta
lugar: La sala del Gremio
personajes: Nova, Gheco
carta: Resta con signo | si num1 < num2: mostrar '-' y num2 - num1 · si no, num1 - num2
```

#### Escena
Otro comerciante tenía **300** monedas y gastó **1.000**. Sin signo, el Gólem diría 64.836. Tiene que decir la verdad: **−700**.

#### Gheco sugiere
Compará num1 con num2. Si num1 es mayor o igual (`jae`), la resta es normal. Si no, mostrá un `'-'` con la `02h` y calculá `num2 − num1`, que da positivo. Al final, `imprimir_numero`.

#### Desafío
Escribí la resta donde dice `; tus órdenes`, para que el ojo diga `300 - 1000 = -700`.

#### Código inicial
```asm
.model small
.stack 100h
.data
num1     dw 300
num2     dw 1000
t_menos  db ' - $'
t_igual  db ' = $'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, num1
    call imprimir_numero
    lea dx, t_menos
    call mostrar_cadena
    mov ax, num2
    call imprimir_numero
    lea dx, t_igual
    call mostrar_cadena

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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Salida esperada
```
300 - 1000 = -700
```

#### Solución
```asm
.model small
.stack 100h
.data
num1     dw 300
num2     dw 1000
t_menos  db ' - $'
t_igual  db ' = $'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, num1
    call imprimir_numero
    lea dx, t_menos
    call mostrar_cadena
    mov ax, num2
    call imprimir_numero
    lea dx, t_igual
    call mostrar_cadena

    mov ax, num1
    cmp ax, num2
    jae positivo
    mov dl, '-'
    mov ah, 02h
    int 21h
    mov ax, num2
    sub ax, num1
    jmp resultado
positivo:
    sub ax, num2
resultado:
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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Al superarla
−700. El comerciante se pone pálido, pero agradece la sinceridad. —Las deudas, con su signo —anota Nova.

#### Imagen
- Un comerciante enano mirando una bolsa de monedas vacía, dada vuelta.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) le muestra una balanza inclinada hacia un lado.
- Gheco (gecko de luz cian con antiparras, chiquito) con una monedita en la mano, ofreciéndosela al comerciante.

### Micro-misión R04-N01-P4 · La multiplicación gigante

```meta
lugar: La sala del Gremio
personajes: Nova, Gheco
carta: jc después de mul | mul deja DX:AX · si DX no es 0, CF = 1: no entra en 16 bits
```

#### Escena
Un enano quiere saber cuánto cuestan **300** cajones a **300** monedas cada uno. El resultado (90.000) no entra en una palanca.

#### Gheco sugiere
`mul num2` deja el resultado en DX:AX. Si DX no quedó en 0, el resultado no entra en AX y se prende **CF**. Saltá al mensaje de error con `jc`.

#### Desafío
Completá el salto para que el Gólem avise que el resultado no entra.

#### Código inicial
```asm
.model small
.stack 100h
.data
num1     dw 300
num2     dw 300
t_por    db ' x $'
t_igual  db ' = $'
t_grande db 'El resultado no entra en 16 bits.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, num1
    call imprimir_numero
    lea dx, t_por
    call mostrar_cadena
    mov ax, num2
    call imprimir_numero
    lea dx, t_igual
    call mostrar_cadena

    mov ax, num1
    mul num2
    ___ grande
    call imprimir_numero
    jmp listo
grande:
    call nueva_linea
    lea dx, t_grande
    call mostrar_cadena
listo:

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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Salida esperada
```
300 x 300 =
El resultado no entra en 16 bits.
```

#### Solución
```asm
.model small
.stack 100h
.data
num1     dw 300
num2     dw 300
t_por    db ' x $'
t_igual  db ' = $'
t_grande db 'El resultado no entra en 16 bits.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, num1
    call imprimir_numero
    lea dx, t_por
    call mostrar_cadena
    mov ax, num2
    call imprimir_numero
    lea dx, t_igual
    call mostrar_cadena

    mov ax, num1
    mul num2
    jc  grande
    call imprimir_numero
    jmp listo
grande:
    call nueva_linea
    lea dx, t_grande
    call mostrar_cadena
listo:

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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Al superarla
El enano decide comprar menos cajones. —Así sí me entra en la cabeza —dice.

#### Imagen
- Una montaña altísima de cajones de madera apilados hasta el techo de una sala.
- Un enano con casco mira la montaña, mareado.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) señala la cima con cara de «demasiado».
- Gheco (gecko de luz cian con antiparras, chiquito) en la cima de la montaña de cajones, saludando.

### Micro-misión R04-N01-P5 · Nunca por cero

```meta
lugar: La sala del Gremio
personajes: Nova, Gheco
carta: Dividir con cuidado | cmp num2, 0 antes del div · DX en 0 · AX = cociente · DX = resto
```

#### Escena
La jefa del Gremio reparte **100** monedas entre **7** socios, y después prueba, por las dudas, entre **0**. —Si el Gólem se rompe —dice—, no lo contrato.

#### Gheco sugiere
Adentro de `dividir`, después de mostrar la cuenta: si `num2` es 0, saltá al mensaje. Si no, AX = num1, DX en 0, `div num2`. El cociente queda en AX y el resto en DX: guardá el resto (por ejemplo en BX) antes de mostrar `, resto `.

#### Desafío
Escribí el resto de la rutina donde dice `; tus órdenes`.

#### Código inicial
```asm
.model small
.stack 100h
.data
num1     dw 100
num2     dw 7
t_div    db ' / $'
t_igual  db ' = $'
t_resto  db ', resto $'
t_cero   db 'No se puede dividir por cero.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    call dividir
    call nueva_linea
    mov num2, 0
    call dividir

fin:
    mov ax, 4C00h
    int 21h
main endp

; dividir: muestra num1 / num2 = cociente, resto r
dividir proc
    push ax
    push bx
    push dx
    mov ax, num1
    call imprimir_numero
    lea dx, t_div
    call mostrar_cadena
    mov ax, num2
    call imprimir_numero
    lea dx, t_igual
    call mostrar_cadena

    ; tus órdenes

    pop dx
    pop bx
    pop ax
    ret
dividir endp

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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Salida esperada
```
100 / 7 = 14, resto 2
100 / 0 =
No se puede dividir por cero.
```

#### Solución
```asm
.model small
.stack 100h
.data
num1     dw 100
num2     dw 7
t_div    db ' / $'
t_igual  db ' = $'
t_resto  db ', resto $'
t_cero   db 'No se puede dividir por cero.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    call dividir
    call nueva_linea
    mov num2, 0
    call dividir

fin:
    mov ax, 4C00h
    int 21h
main endp

; dividir: muestra num1 / num2 = cociente, resto r
dividir proc
    push ax
    push bx
    push dx
    mov ax, num1
    call imprimir_numero
    lea dx, t_div
    call mostrar_cadena
    mov ax, num2
    call imprimir_numero
    lea dx, t_igual
    call mostrar_cadena

    cmp num2, 0
    je  por_cero
    mov ax, num1
    mov dx, 0
    div num2
    mov bx, dx
    call imprimir_numero
    lea dx, t_resto
    call mostrar_cadena
    mov ax, bx
    call imprimir_numero
    jmp fin_dividir
por_cero:
    call nueva_linea
    lea dx, t_cero
    call mostrar_cadena
fin_dividir:

    pop dx
    pop bx
    pop ax
    ret
dividir endp

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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Al superarla
Catorce para cada socio y sobran dos. Y por cero, un aviso educado. La jefa asiente despacio: es lo más cerca de una sonrisa que se le vio.

#### Imagen
- La jefa del Gremio, una enana robusta con anteojos redondos y un chaleco con muchos bolsillos, con los brazos cruzados y un amago de sonrisa.
- Sobre la mesa, siete montoncitos iguales de monedas y dos sueltas aparte.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) flota al lado de la mesa, nerviosa.
- Gheco (gecko de luz cian con antiparras, chiquito) contando los montoncitos con la cola.

### Micro-misión R04-N01-P6 · La calculadora completa

```meta
lugar: La sala del Gremio
personajes: Nova, Gheco, Kira, Axón
carta: El menú que se repite | leer opción · 0 sale · 1 a 4: pedir números y elegir la rutina · lo demás: no existe · volver al menú
```

#### Escena
Llegó el día de la entrega. El Gremio entero se sienta frente a {mentor}, y Kira se ofrece a hacer la demostración. Todas las rutinas están listas: falta el **programa principal** que las une.

#### Gheco sugiere
Un menú que se repite: mostrar la pregunta, leer la opción con la `01h` y **guardarla en BL** (las rutinas no la tocan). Si es `'0'`, `salir`. Si está fuera de `'1'` a `'4'`, el mensaje de que no existe. Si no, `call pedir_numeros` y, según BL, la rutina que corresponda. Después de cada opción, `nueva_linea` y `jmp menu`.

#### Desafío
Escribí el programa principal donde dice `; tus órdenes`. Kira va a sumar 1250 y 750, restar 300 y 1000 (escribiendo primero `mil`, por error), dividir 100 por 7, probar la opción 9 y salir con el 0.

#### Código inicial
```asm
.model small
.stack 100h
.data
num1      dw ?
num2      dw ?
buffer    db 6, ?, 6 dup(?)
t_titulo  db '== CALCULADORA DEL GREMIO ==', 13, 10, '$'
t_opcion  db 13, 10, 'Opcion (1+ 2- 3x 4: 0 salir): $'
t_noex    db 'Esa opcion no existe.$'
t_n1      db 'Primer numero: $'
t_n2      db 'Segundo numero: $'
t_mal     db '  (tiene que ser un numero de 0 a 65535) $'
t_mas     db ' + $'
t_menos   db ' - $'
t_por     db ' x $'
t_div     db ' / $'
t_igual   db ' = $'
t_resto   db ', resto $'
t_grande  db 'El resultado no entra en 16 bits.$'
t_cero    db 'No se puede dividir por cero.$'
t_chau    db 'Hasta la proxima.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    ; tus órdenes

fin:
    mov ax, 4C00h
    int 21h
main endp

; pedir_numeros: pide num1 y num2 hasta que sean válidos
pedir_numeros proc
    push ax
    push dx
pedir1:
    lea dx, t_n1
    call mostrar_cadena
    call leer_numero
    jnc ok1
    lea dx, t_mal
    call mostrar_cadena
    jmp pedir1
ok1:
    mov num1, ax
pedir2:
    lea dx, t_n2
    call mostrar_cadena
    call leer_numero
    jnc ok2
    lea dx, t_mal
    call mostrar_cadena
    jmp pedir2
ok2:
    mov num2, ax
    pop dx
    pop ax
    ret
pedir_numeros endp

; cuenta: muestra "num1 <DX> num2 = "
cuenta proc
    push ax
    push dx
    mov ax, num1
    call imprimir_numero
    pop dx
    call mostrar_cadena
    mov ax, num2
    call imprimir_numero
    lea dx, t_igual
    call mostrar_cadena
    pop ax
    ret
cuenta endp

sumar proc
    push ax
    push dx
    lea dx, t_mas
    call cuenta
    mov ax, num1
    add ax, num2
    jc  sumar_grande
    call imprimir_numero
    jmp sumar_fin
sumar_grande:
    call nueva_linea
    lea dx, t_grande
    call mostrar_cadena
sumar_fin:
    pop dx
    pop ax
    ret
sumar endp

restar proc
    push ax
    push dx
    lea dx, t_menos
    call cuenta
    mov ax, num1
    cmp ax, num2
    jae restar_pos
    mov dl, '-'
    mov ah, 02h
    int 21h
    mov ax, num2
    sub ax, num1
    jmp restar_fin
restar_pos:
    sub ax, num2
restar_fin:
    call imprimir_numero
    pop dx
    pop ax
    ret
restar endp

multiplicar proc
    push ax
    push dx
    lea dx, t_por
    call cuenta
    mov ax, num1
    mul num2
    jc  mult_grande
    call imprimir_numero
    jmp mult_fin
mult_grande:
    call nueva_linea
    lea dx, t_grande
    call mostrar_cadena
mult_fin:
    pop dx
    pop ax
    ret
multiplicar endp

dividir proc
    push ax
    push bx
    push dx
    lea dx, t_div
    call cuenta
    cmp num2, 0
    je  div_cero
    mov ax, num1
    mov dx, 0
    div num2
    mov bx, dx
    call imprimir_numero
    lea dx, t_resto
    call mostrar_cadena
    mov ax, bx
    call imprimir_numero
    jmp div_fin
div_cero:
    call nueva_linea
    lea dx, t_cero
    call mostrar_cadena
div_fin:
    pop dx
    pop bx
    pop ax
    ret
dividir endp

; leer_numero: AX = el número tipeado; CF = 1 si no es válido
leer_numero proc
    push bx
    push cx
    push dx
    push si
    mov ah, 0Ah
    lea dx, buffer
    int 21h
    call nueva_linea
    mov cl, buffer+1
    mov ch, 0
    jcxz invalido
    lea si, buffer+2
    mov ax, 0
convertir:
    mov bl, [si]
    cmp bl, '0'
    jb  invalido
    cmp bl, '9'
    ja  invalido
    sub bl, '0'
    mov bh, 0
    mov dx, 10
    mul dx
    jc  invalido
    add ax, bx
    jc  invalido
    inc si
    loop convertir
    clc
    jmp leer_fin
invalido:
    stc
leer_fin:
    pop si
    pop dx
    pop cx
    pop bx
    ret
leer_numero endp

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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Entrada
```
1
1250
750
2
300
mil
1000
4
100
7
9
0
```

#### Salida esperada
```
== CALCULADORA DEL GREMIO ==

Opcion (1+ 2- 3x 4: 0 salir): 1
Primer numero: 1250
Segundo numero: 750
1250 + 750 = 2000

Opcion (1+ 2- 3x 4: 0 salir): 2
Primer numero: 300
Segundo numero: mil
  (tiene que ser un numero de 0 a 65535) Segundo numero: 1000
300 - 1000 = -700

Opcion (1+ 2- 3x 4: 0 salir): 4
Primer numero: 100
Segundo numero: 7
100 / 7 = 14, resto 2

Opcion (1+ 2- 3x 4: 0 salir): 9
Esa opcion no existe.

Opcion (1+ 2- 3x 4: 0 salir): 0
Hasta la proxima.
```

#### Solución
```asm
.model small
.stack 100h
.data
num1      dw ?
num2      dw ?
buffer    db 6, ?, 6 dup(?)
t_titulo  db '== CALCULADORA DEL GREMIO ==', 13, 10, '$'
t_opcion  db 13, 10, 'Opcion (1+ 2- 3x 4: 0 salir): $'
t_noex    db 'Esa opcion no existe.$'
t_n1      db 'Primer numero: $'
t_n2      db 'Segundo numero: $'
t_mal     db '  (tiene que ser un numero de 0 a 65535) $'
t_mas     db ' + $'
t_menos   db ' - $'
t_por     db ' x $'
t_div     db ' / $'
t_igual   db ' = $'
t_resto   db ', resto $'
t_grande  db 'El resultado no entra en 16 bits.$'
t_cero    db 'No se puede dividir por cero.$'
t_chau    db 'Hasta la proxima.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_titulo
    call mostrar_cadena
menu:
    lea dx, t_opcion
    call mostrar_cadena
    mov ah, 01h
    int 21h
    mov bl, al
    call nueva_linea
    cmp bl, '0'
    je  salir
    cmp bl, '1'
    jb  no_existe
    cmp bl, '4'
    ja  no_existe
    call pedir_numeros
    cmp bl, '1'
    jne no_suma
    call sumar
    jmp otra
no_suma:
    cmp bl, '2'
    jne no_resta
    call restar
    jmp otra
no_resta:
    cmp bl, '3'
    jne no_mult
    call multiplicar
    jmp otra
no_mult:
    call dividir
    jmp otra
no_existe:
    lea dx, t_noex
    call mostrar_cadena
otra:
    call nueva_linea
    jmp menu
salir:
    lea dx, t_chau
    call mostrar_cadena

fin:
    mov ax, 4C00h
    int 21h
main endp

; pedir_numeros: pide num1 y num2 hasta que sean válidos
pedir_numeros proc
    push ax
    push dx
pedir1:
    lea dx, t_n1
    call mostrar_cadena
    call leer_numero
    jnc ok1
    lea dx, t_mal
    call mostrar_cadena
    jmp pedir1
ok1:
    mov num1, ax
pedir2:
    lea dx, t_n2
    call mostrar_cadena
    call leer_numero
    jnc ok2
    lea dx, t_mal
    call mostrar_cadena
    jmp pedir2
ok2:
    mov num2, ax
    pop dx
    pop ax
    ret
pedir_numeros endp

; cuenta: muestra "num1 <DX> num2 = "
cuenta proc
    push ax
    push dx
    mov ax, num1
    call imprimir_numero
    pop dx
    call mostrar_cadena
    mov ax, num2
    call imprimir_numero
    lea dx, t_igual
    call mostrar_cadena
    pop ax
    ret
cuenta endp

sumar proc
    push ax
    push dx
    lea dx, t_mas
    call cuenta
    mov ax, num1
    add ax, num2
    jc  sumar_grande
    call imprimir_numero
    jmp sumar_fin
sumar_grande:
    call nueva_linea
    lea dx, t_grande
    call mostrar_cadena
sumar_fin:
    pop dx
    pop ax
    ret
sumar endp

restar proc
    push ax
    push dx
    lea dx, t_menos
    call cuenta
    mov ax, num1
    cmp ax, num2
    jae restar_pos
    mov dl, '-'
    mov ah, 02h
    int 21h
    mov ax, num2
    sub ax, num1
    jmp restar_fin
restar_pos:
    sub ax, num2
restar_fin:
    call imprimir_numero
    pop dx
    pop ax
    ret
restar endp

multiplicar proc
    push ax
    push dx
    lea dx, t_por
    call cuenta
    mov ax, num1
    mul num2
    jc  mult_grande
    call imprimir_numero
    jmp mult_fin
mult_grande:
    call nueva_linea
    lea dx, t_grande
    call mostrar_cadena
mult_fin:
    pop dx
    pop ax
    ret
multiplicar endp

dividir proc
    push ax
    push bx
    push dx
    lea dx, t_div
    call cuenta
    cmp num2, 0
    je  div_cero
    mov ax, num1
    mov dx, 0
    div num2
    mov bx, dx
    call imprimir_numero
    lea dx, t_resto
    call mostrar_cadena
    mov ax, bx
    call imprimir_numero
    jmp div_fin
div_cero:
    call nueva_linea
    lea dx, t_cero
    call mostrar_cadena
div_fin:
    pop dx
    pop bx
    pop ax
    ret
dividir endp

; leer_numero: AX = el número tipeado; CF = 1 si no es válido
leer_numero proc
    push bx
    push cx
    push dx
    push si
    mov ah, 0Ah
    lea dx, buffer
    int 21h
    call nueva_linea
    mov cl, buffer+1
    mov ch, 0
    jcxz invalido
    lea si, buffer+2
    mov ax, 0
convertir:
    mov bl, [si]
    cmp bl, '0'
    jb  invalido
    cmp bl, '9'
    ja  invalido
    sub bl, '0'
    mov bh, 0
    mov dx, 10
    mul dx
    jc  invalido
    add ax, bx
    jc  invalido
    inc si
    loop convertir
    clc
    jmp leer_fin
invalido:
    stc
leer_fin:
    pop si
    pop dx
    pop cx
    pop bx
    ret
leer_numero endp

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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Al superarla
La comitiva aplaude. Kira se equivocó a propósito con `mil` y el Gólem le pidió, con toda paciencia, que lo escribiera de nuevo. La jefa del Gremio firma el contrato con una pluma de bronce.

—Primer trabajo —dice Nova, emocionada—. Y nadie se rompió.

#### Imagen
- La sala del Gremio llena de enanos aplaudiendo, de pie, frente a un gólem de bronce gigante con el ojo encendido.
- La jefa del Gremio firma un pergamino cerrado con una pluma de bronce.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) hace una reverencia exagerada.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se asoma por el pecho del gólem, radiante.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre la cabeza del gólem, con los brazos en alto.

### Prueba del sello

#### ¿Por qué cada operación de la calculadora va en su propia rutina?
Para que cada parte se pruebe sola, el programa principal solo decida, y los saltos queden cortos.

#### ¿Cómo se detecta que una suma no entra en 16 bits?
Con `jc` justo después del `add`: CF queda en 1.

#### ¿Por qué la división por cero se revisa antes del `div` y no después?
Porque el `div` por cero detiene el programa: no hay un después.

#### ¿Dónde conviene guardar la opción del menú mientras se llaman las rutinas?
En una palanca que las rutinas no toquen (o en una variable), como BL acá.

## R04-N02 · Proyecto: el Oráculo del Gólem

```meta
tipo: tema
criatura: ogre
padre: R04-N01
precio: 0
temas: prog.matematica-azar, alg.busqueda
usa: prog.bucles, prog.condicionales, prog.funciones, err.validacion
```

### Crónica

Con la plata del Gremio, Kira compra un regalo para el Gólem: un juego. —Pensá un número del 1 al 100 —le propone—, y yo lo adivino en **siete** intentos. Vos solo decís «más alto» o «más bajo».

—No puedo pensar —dice {mentor}—. Pero puedo **calcular** uno que parezca pensado.

Nova se entusiasma: es el primer juego que el Gólem va a jugar en siglos.

### Objetivos

Armar un juego completo: un número secreto con `azar`, pistas con comparaciones, el **valor absoluto** con `neg`
para el «muy cerca», turnos que se cuentan, entradas que no gastan intentos y la opción de jugar otra vez.

### Antes de empezar

- `azar` (El ojo del Gólem), `leer_numero` e `imprimir_numero` (El grimorio de los números).
- La calculadora del Gremio (rutinas que se combinan).

### Explicación

#### La estructura
```
partida:  secreto = azar(100) + 1, quedan = 7, usados = 0
turno:    leer un número
            inválido o fuera de 1..100 -> no cuenta, repetir el turno
            igual al secreto            -> ganó
            si no: «Mas ALTO» o «Mas BAJO» (+ «muy cerca» si está a 3 o menos)
            quedan - 1; si quedan > 0, otro turno; si no, perdió
main:     partida; ¿jugar otra vez? s -> partida
```

#### Más alto o más bajo
```asm
cmp ax, secreto
je  gano
lea dx, t_alto
jb  pista            ; lo que dijo es MENOR: el secreto es más alto
lea dx, t_bajo
pista:
```
Los interruptores del `cmp` sirven para los dos saltos: el `lea` del medio no los cambia.

#### «Muy cerca»: el valor absoluto
`dicho − secreto` puede ser negativo. Si el resultado tiene el bit de signo prendido, `neg` lo da vuelta. `jns`
(*jump if not sign*) salta si ya era positivo:
```asm
mov bx, ax
sub bx, secreto
jns positivo
neg bx               ; ahora BX es la distancia, siempre positiva
positivo:
```

#### La mejor estrategia: partir a la mitad
Decir 50, después 25 o 75, y así: cada intento descarta la **mitad** de los números que quedan
(100 → 50 → 25 → 13 → 7 → 4 → 2 → 1). Con 7 intentos alcanza **siempre**, porque 2⁷ = 128 ≥ 100. Se llama
**búsqueda binaria**.

#### Mayúscula o minúscula
Para «¿Jugar otra vez?», `or al, 20h` (el bit 5) pasa `'S'` a `'s'`: acepta las dos.

> **Puente con otras lenguas.** La búsqueda binaria es uno de los algoritmos más famosos de la informática: se usa
> para buscar en listas ordenadas, en bases de datos y hasta en `git bisect`. Y el «número que parece al azar» es
> el `random.randint(1, 100)` de Python.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
semilla dw 2026
t_pens  db 'Modo trampa: el Golem penso el $'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bl, 100
    call azar
    mov ah, 0
    inc ax               ; de 1 a 100
    push ax
    lea dx, t_pens
    mov ah, 09h
    int 21h
    pop ax
    call imprimir_numero

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
    mov al, ah
    mov ah, 0
    div bl
    mov al, ah
    pop dx
    ret
azar endp

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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
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
Modo trampa: el Golem penso el 7
```

### ¿Para qué sirve?

Un juego completo usa todo junto: azar, bucles anidados (partidas y turnos), validación y estado (intentos,
secreto). Y la estrategia de partir a la mitad es la idea detrás de buscar rápido en millones de datos.

### Errores habituales

**Ogro: el intento que no tenía que contar.** Si lo inválido gasta un intento, el jugador pierde por un error de
tipeo.

**Ogro: la distancia negativa.** Sin `neg`, `40 − 42` da 65.534: nunca está «muy cerca».

**Ogro: la pista al revés.** Si lo que dijo es **menor**, el secreto es **más alto**. Es fácil escribir el salto
justo al revés.

**Ogro: la semilla fija.** En un juego de verdad la semilla sale del reloj (`int 21h`, `2Ch`). Acá está fija para
poder comprobar.

### Micro-misión R04-N02-P1 · Más alto o más bajo

```meta
lugar: La sala del juego
personajes: Nova, Gheco, Kira
carta: Pista | cmp ax, secreto · je: ganó · jb: lo dicho es menor, el secreto es MÁS ALTO
```

#### Escena
El Gólem pensó el **42** (por ahora, a mano). Kira dice **50**. ¿Qué tiene que contestar el ojo?

#### Gheco sugiere
Después del `cmp`, primero `je gano`. Si no ganó: se carga «Mas ALTO» y, si lo que dijo es **menor** (`jb`), se salta a mostrarlo; si no, se cambia por «Mas BAJO».

#### Desafío
Completá los dos saltos para que, con el 50, el ojo diga `Mas BAJO`.

#### Código inicial
```asm
.model small
.stack 100h
.data
secreto dw 42
buffer  db 6, ?, 6 dup(?)
t_intento db 'Intento $'
t_dos     db ': $'
t_alto    db '  Mas ALTO$'
t_bajo    db '  Mas BAJO$'
t_cerca   db ' (muy cerca!)$'
t_gano  db '  ACERTASTE!$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_intento
    call mostrar_cadena
    call leer_numero

    cmp ax, secreto
    je  ___
    lea dx, t_alto
    jb  ___
    lea dx, t_bajo
dar_pista:
    call mostrar_cadena
    jmp listo
gano:
    lea dx, t_gano
    call mostrar_cadena
listo:

fin:
    mov ax, 4C00h
    int 21h
main endp

; leer_numero: AX = el número tipeado; CF = 1 si no es válido
leer_numero proc
    push bx
    push cx
    push dx
    push si
    mov ah, 0Ah
    lea dx, buffer
    int 21h
    call nueva_linea
    mov cl, buffer+1
    mov ch, 0
    jcxz invalido
    lea si, buffer+2
    mov ax, 0
convertir:
    mov bl, [si]
    cmp bl, '0'
    jb  invalido
    cmp bl, '9'
    ja  invalido
    sub bl, '0'
    mov bh, 0
    mov dx, 10
    mul dx
    jc  invalido
    add ax, bx
    jc  invalido
    inc si
    loop convertir
    clc
    jmp leer_fin
invalido:
    stc
leer_fin:
    pop si
    pop dx
    pop cx
    pop bx
    ret
leer_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Entrada
```
50
```

#### Salida esperada
```
Intento 50
  Mas BAJO
```

#### Solución
```asm
.model small
.stack 100h
.data
secreto dw 42
buffer  db 6, ?, 6 dup(?)
t_intento db 'Intento $'
t_dos     db ': $'
t_alto    db '  Mas ALTO$'
t_bajo    db '  Mas BAJO$'
t_cerca   db ' (muy cerca!)$'
t_gano  db '  ACERTASTE!$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_intento
    call mostrar_cadena
    call leer_numero

    cmp ax, secreto
    je  gano
    lea dx, t_alto
    jb  dar_pista
    lea dx, t_bajo
dar_pista:
    call mostrar_cadena
    jmp listo
gano:
    lea dx, t_gano
    call mostrar_cadena
listo:

fin:
    mov ax, 4C00h
    int 21h
main endp

; leer_numero: AX = el número tipeado; CF = 1 si no es válido
leer_numero proc
    push bx
    push cx
    push dx
    push si
    mov ah, 0Ah
    lea dx, buffer
    int 21h
    call nueva_linea
    mov cl, buffer+1
    mov ch, 0
    jcxz invalido
    lea si, buffer+2
    mov ax, 0
convertir:
    mov bl, [si]
    cmp bl, '0'
    jb  invalido
    cmp bl, '9'
    ja  invalido
    sub bl, '0'
    mov bh, 0
    mov dx, 10
    mul dx
    jc  invalido
    add ax, bx
    jc  invalido
    inc si
    loop convertir
    clc
    jmp leer_fin
invalido:
    stc
leer_fin:
    pop si
    pop dx
    pop cx
    pop bx
    ret
leer_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Al superarla
«Mas BAJO». Kira entrecierra los ojos y piensa. —Entonces es menos de 50 —murmura—. Ya te agarro.

#### Imagen
- Una sala de juegos dentro de un gólem de bronce, con un tablero gigante de cien casilleros lisos en la pared.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) con la mano en el mentón, pensando.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) flota al lado del tablero con cara de saber el secreto.
- Gheco (gecko de luz cian con antiparras, chiquito) tapándose la boca para no decir nada.

### Micro-misión R04-N02-P2 · Muy cerca

```meta
lugar: La sala del juego
personajes: Nova, Gheco, Kira
carta: Valor absoluto | sub · jns positivo · neg · la distancia, siempre positiva
```

#### Escena
Kira dice **40**, y el secreto es el 42. A Nova se le escapa: —¡Uy, muy cerca! El Gólem quiere avisarlo también.

#### Gheco sugiere
Calculá la distancia en BX: `dicho − secreto`. Si salió negativa (no salta el `jns`), dala vuelta con `neg bx`. Si es **3 o menos**, mostrá « (muy cerca!)».

#### Desafío
Escribí el cálculo donde dice `; tus órdenes`, para que con el 40 el ojo diga `Mas ALTO (muy cerca!)`.

#### Código inicial
```asm
.model small
.stack 100h
.data
secreto dw 42
buffer  db 6, ?, 6 dup(?)
t_intento db 'Intento $'
t_dos     db ': $'
t_alto    db '  Mas ALTO$'
t_bajo    db '  Mas BAJO$'
t_cerca   db ' (muy cerca!)$'
t_gano  db '  ACERTASTE!$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_intento
    call mostrar_cadena
    call leer_numero

    cmp ax, secreto
    lea dx, t_alto
    jb  dar_pista
    lea dx, t_bajo
dar_pista:
    call mostrar_cadena

    ; tus órdenes (el muy cerca)

fin:
    mov ax, 4C00h
    int 21h
main endp

; leer_numero: AX = el número tipeado; CF = 1 si no es válido
leer_numero proc
    push bx
    push cx
    push dx
    push si
    mov ah, 0Ah
    lea dx, buffer
    int 21h
    call nueva_linea
    mov cl, buffer+1
    mov ch, 0
    jcxz invalido
    lea si, buffer+2
    mov ax, 0
convertir:
    mov bl, [si]
    cmp bl, '0'
    jb  invalido
    cmp bl, '9'
    ja  invalido
    sub bl, '0'
    mov bh, 0
    mov dx, 10
    mul dx
    jc  invalido
    add ax, bx
    jc  invalido
    inc si
    loop convertir
    clc
    jmp leer_fin
invalido:
    stc
leer_fin:
    pop si
    pop dx
    pop cx
    pop bx
    ret
leer_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Entrada
```
40
```

#### Salida esperada
```
Intento 40
  Mas ALTO (muy cerca!)
```

#### Solución
```asm
.model small
.stack 100h
.data
secreto dw 42
buffer  db 6, ?, 6 dup(?)
t_intento db 'Intento $'
t_dos     db ': $'
t_alto    db '  Mas ALTO$'
t_bajo    db '  Mas BAJO$'
t_cerca   db ' (muy cerca!)$'
t_gano  db '  ACERTASTE!$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_intento
    call mostrar_cadena
    call leer_numero

    cmp ax, secreto
    lea dx, t_alto
    jb  dar_pista
    lea dx, t_bajo
dar_pista:
    call mostrar_cadena

    mov bx, ax
    sub bx, secreto
    jns positivo
    neg bx
positivo:
    cmp bx, 3
    ja  lejos
    lea dx, t_cerca
    call mostrar_cadena
lejos:

fin:
    mov ax, 4C00h
    int 21h
main endp

; leer_numero: AX = el número tipeado; CF = 1 si no es válido
leer_numero proc
    push bx
    push cx
    push dx
    push si
    mov ah, 0Ah
    lea dx, buffer
    int 21h
    call nueva_linea
    mov cl, buffer+1
    mov ch, 0
    jcxz invalido
    lea si, buffer+2
    mov ax, 0
convertir:
    mov bl, [si]
    cmp bl, '0'
    jb  invalido
    cmp bl, '9'
    ja  invalido
    sub bl, '0'
    mov bh, 0
    mov dx, 10
    mul dx
    jc  invalido
    add ax, bx
    jc  invalido
    inc si
    loop convertir
    clc
    jmp leer_fin
invalido:
    stc
leer_fin:
    pop si
    pop dx
    pop cx
    pop bx
    ret
leer_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Al superarla
—¡Lo sabía! —grita Kira—. Es el 41 o el 42 o el 43. —Gheco la mira de reojo: sabe que Kira no sabía.

#### Imagen
- Un tablero de cien casilleros en una pared de bronce, con tres casilleros juntos iluminados en ámbar.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) salta de entusiasmo.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se tapa la boca, culpable por haberse dejado escapar la pista.
- Gheco (gecko de luz cian con antiparras, chiquito) niega con la cabeza, divertido.

### Micro-misión R04-N02-P3 · Siete intentos

```meta
lugar: La sala del juego
personajes: Nova, Gheco, Kira
carta: Turnos | inc usados · leer · je gano · pista · dec quedan · jnz otra vuelta · si no, perdió
```

#### Escena
Ahora sí, el juego entero: **siete** intentos. Kira va a jugar como le enseñó Gheco, partiendo a la mitad.

#### Gheco sugiere
Un «hasta que» con la etiqueta `jugar:`. En cada vuelta: sumá 1 a `usados` y mostralo («Intento N: »), leé el número, si es el secreto saltá a `gano`; si no, `call pista`, restale 1 a `quedan` y, si no llegó a 0 (`jnz`), volvé a `jugar`. Si se acabaron, el mensaje de que perdió. En `gano`, el mensaje y cuántos intentos usó. La rutina `pista` ya está.

#### Desafío
Escribí el bucle de turnos donde dice `; tus órdenes`. Kira va a decir 50, 25, 37, 43 y 42.

#### Código inicial
```asm
.model small
.stack 100h
.data
secreto  dw 42
quedan   db 7
usados   dw 0
buffer   db 6, ?, 6 dup(?)
t_intento db 'Intento $'
t_dos     db ': $'
t_alto    db '  Mas ALTO$'
t_bajo    db '  Mas BAJO$'
t_cerca   db ' (muy cerca!)$'
t_gano   db 13, 10, 'ACERTASTE! Intentos usados: $'
t_perdio db 13, 10, 'Se acabaron los intentos.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    ; tus órdenes

fin:
    mov ax, 4C00h
    int 21h
main endp

; pista: AX = lo que se dijo; muestra Mas ALTO / Mas BAJO (y muy cerca si está a 3 o menos)
pista proc
    push ax
    push bx
    push dx
    cmp ax, secreto
    lea dx, t_alto
    jb  pista_texto
    lea dx, t_bajo
pista_texto:
    call mostrar_cadena
    mov bx, ax
    sub bx, secreto
    jns pista_pos
    neg bx
pista_pos:
    cmp bx, 3
    ja  pista_fin
    lea dx, t_cerca
    call mostrar_cadena
pista_fin:
    call nueva_linea
    pop dx
    pop bx
    pop ax
    ret
pista endp

; leer_numero: AX = el número tipeado; CF = 1 si no es válido
leer_numero proc
    push bx
    push cx
    push dx
    push si
    mov ah, 0Ah
    lea dx, buffer
    int 21h
    call nueva_linea
    mov cl, buffer+1
    mov ch, 0
    jcxz invalido
    lea si, buffer+2
    mov ax, 0
convertir:
    mov bl, [si]
    cmp bl, '0'
    jb  invalido
    cmp bl, '9'
    ja  invalido
    sub bl, '0'
    mov bh, 0
    mov dx, 10
    mul dx
    jc  invalido
    add ax, bx
    jc  invalido
    inc si
    loop convertir
    clc
    jmp leer_fin
invalido:
    stc
leer_fin:
    pop si
    pop dx
    pop cx
    pop bx
    ret
leer_numero endp

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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Entrada
```
50
25
37
43
42
```

#### Salida esperada
```
Intento 1: 50
  Mas BAJO
Intento 2: 25
  Mas ALTO
Intento 3: 37
  Mas ALTO
Intento 4: 43
  Mas BAJO (muy cerca!)
Intento 5: 42

ACERTASTE! Intentos usados: 5
```

#### Solución
```asm
.model small
.stack 100h
.data
secreto  dw 42
quedan   db 7
usados   dw 0
buffer   db 6, ?, 6 dup(?)
t_intento db 'Intento $'
t_dos     db ': $'
t_alto    db '  Mas ALTO$'
t_bajo    db '  Mas BAJO$'
t_cerca   db ' (muy cerca!)$'
t_gano   db 13, 10, 'ACERTASTE! Intentos usados: $'
t_perdio db 13, 10, 'Se acabaron los intentos.$'
.code
main proc
    mov ax, @data
    mov ds, ax

jugar:
    inc usados
    lea dx, t_intento
    call mostrar_cadena
    mov ax, usados
    call imprimir_numero
    lea dx, t_dos
    call mostrar_cadena
    call leer_numero
    cmp ax, secreto
    je  gano
    call pista
    dec quedan
    jnz jugar
    lea dx, t_perdio
    call mostrar_cadena
    jmp terminado
gano:
    lea dx, t_gano
    call mostrar_cadena
    mov ax, usados
    call imprimir_numero
terminado:

fin:
    mov ax, 4C00h
    int 21h
main endp

; pista: AX = lo que se dijo; muestra Mas ALTO / Mas BAJO (y muy cerca si está a 3 o menos)
pista proc
    push ax
    push bx
    push dx
    cmp ax, secreto
    lea dx, t_alto
    jb  pista_texto
    lea dx, t_bajo
pista_texto:
    call mostrar_cadena
    mov bx, ax
    sub bx, secreto
    jns pista_pos
    neg bx
pista_pos:
    cmp bx, 3
    ja  pista_fin
    lea dx, t_cerca
    call mostrar_cadena
pista_fin:
    call nueva_linea
    pop dx
    pop bx
    pop ax
    ret
pista endp

; leer_numero: AX = el número tipeado; CF = 1 si no es válido
leer_numero proc
    push bx
    push cx
    push dx
    push si
    mov ah, 0Ah
    lea dx, buffer
    int 21h
    call nueva_linea
    mov cl, buffer+1
    mov ch, 0
    jcxz invalido
    lea si, buffer+2
    mov ax, 0
convertir:
    mov bl, [si]
    cmp bl, '0'
    jb  invalido
    cmp bl, '9'
    ja  invalido
    sub bl, '0'
    mov bh, 0
    mov dx, 10
    mul dx
    jc  invalido
    add ax, bx
    jc  invalido
    inc si
    loop convertir
    clc
    jmp leer_fin
invalido:
    stc
leer_fin:
    pop si
    pop dx
    pop cx
    pop bx
    ret
leer_numero endp

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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Al superarla
ACERTASTE en el intento 5. Kira levanta los brazos. —Partir a la mitad —le explica a Nova—. Nunca falla.

#### Imagen
- Un tablero de cien casilleros en una pared de bronce, con casi todos apagados y uno solo brillando en dorado.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) con los brazos en alto, triunfante.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) aplaude flotando.
- Gheco (gecko de luz cian con antiparras, chiquito) hace confeti con papelitos de colores lisos.

### Micro-misión R04-N02-P4 · Lo que no cuenta

```meta
lugar: La sala del juego
personajes: Nova, Gheco, Kira
criatura: ogre
carta: No gastar intentos | lo inválido vuelve a pedir sin restar quedan · y descuenta el usados que ya sumó
```

#### Escena
Para la revancha, el Gólem da solo **3** intentos. Kira se pone nerviosa y escribe `cien` en letras y después `150`. Pierde sin haber jugado de verdad. Un ogro se ríe en la tribuna.

#### Gheco sugiere
Lo inválido salta a `no_vale`, que muestra el aviso… y después va a `siguiente`, donde se resta un intento. Lo que no vale tiene que volver a `jugar` **sin** restar `quedan`, y deshacer el `inc usados` del principio con `dec usados`.

#### Desafío
Tocá **Ejecutar** y mirá cómo pierde. Después arreglá el final de `no_vale` para que lo inválido no cuente. Kira va a decir 50, cien, 150 y 42.

#### Código inicial
```asm
.model small
.stack 100h
.data
secreto  dw 42
quedan   db 3
usados   dw 0
buffer   db 6, ?, 6 dup(?)
t_intento db 'Intento $'
t_dos     db ': $'
t_alto    db '  Mas ALTO$'
t_bajo    db '  Mas BAJO$'
t_cerca   db ' (muy cerca!)$'
t_gano   db 13, 10, 'ACERTASTE! Intentos usados: $'
t_perdio db 13, 10, 'Se acabaron los intentos.$'
t_novale db '  Eso no es un numero del 1 al 100 (no cuenta).$'
.code
main proc
    mov ax, @data
    mov ds, ax

jugar:
    inc usados
    lea dx, t_intento
    call mostrar_cadena
    mov ax, usados
    call imprimir_numero
    lea dx, t_dos
    call mostrar_cadena
    call leer_numero
    jc  no_vale
    cmp ax, 1
    jb  no_vale
    cmp ax, 100
    ja  no_vale
    cmp ax, secreto
    je  gano
    call pista
siguiente:
    dec quedan
    jnz jugar
    lea dx, t_perdio
    call mostrar_cadena
    jmp terminado
no_vale:
    lea dx, t_novale
    call mostrar_cadena
    call nueva_linea
    jmp siguiente
gano:
    lea dx, t_gano
    call mostrar_cadena
    mov ax, usados
    call imprimir_numero
terminado:

fin:
    mov ax, 4C00h
    int 21h
main endp

; pista: AX = lo que se dijo; muestra Mas ALTO / Mas BAJO (y muy cerca si está a 3 o menos)
pista proc
    push ax
    push bx
    push dx
    cmp ax, secreto
    lea dx, t_alto
    jb  pista_texto
    lea dx, t_bajo
pista_texto:
    call mostrar_cadena
    mov bx, ax
    sub bx, secreto
    jns pista_pos
    neg bx
pista_pos:
    cmp bx, 3
    ja  pista_fin
    lea dx, t_cerca
    call mostrar_cadena
pista_fin:
    call nueva_linea
    pop dx
    pop bx
    pop ax
    ret
pista endp

; leer_numero: AX = el número tipeado; CF = 1 si no es válido
leer_numero proc
    push bx
    push cx
    push dx
    push si
    mov ah, 0Ah
    lea dx, buffer
    int 21h
    call nueva_linea
    mov cl, buffer+1
    mov ch, 0
    jcxz invalido
    lea si, buffer+2
    mov ax, 0
convertir:
    mov bl, [si]
    cmp bl, '0'
    jb  invalido
    cmp bl, '9'
    ja  invalido
    sub bl, '0'
    mov bh, 0
    mov dx, 10
    mul dx
    jc  invalido
    add ax, bx
    jc  invalido
    inc si
    loop convertir
    clc
    jmp leer_fin
invalido:
    stc
leer_fin:
    pop si
    pop dx
    pop cx
    pop bx
    ret
leer_numero endp

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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Entrada
```
50
cien
150
42
```

#### Salida esperada
```
Intento 1: 50
  Mas BAJO
Intento 2: cien
  Eso no es un numero del 1 al 100 (no cuenta).
Intento 2: 150
  Eso no es un numero del 1 al 100 (no cuenta).
Intento 2: 42

ACERTASTE! Intentos usados: 2
```

#### Solución
```asm
.model small
.stack 100h
.data
secreto  dw 42
quedan   db 3
usados   dw 0
buffer   db 6, ?, 6 dup(?)
t_intento db 'Intento $'
t_dos     db ': $'
t_alto    db '  Mas ALTO$'
t_bajo    db '  Mas BAJO$'
t_cerca   db ' (muy cerca!)$'
t_gano   db 13, 10, 'ACERTASTE! Intentos usados: $'
t_perdio db 13, 10, 'Se acabaron los intentos.$'
t_novale db '  Eso no es un numero del 1 al 100 (no cuenta).$'
.code
main proc
    mov ax, @data
    mov ds, ax

jugar:
    inc usados
    lea dx, t_intento
    call mostrar_cadena
    mov ax, usados
    call imprimir_numero
    lea dx, t_dos
    call mostrar_cadena
    call leer_numero
    jc  no_vale
    cmp ax, 1
    jb  no_vale
    cmp ax, 100
    ja  no_vale
    cmp ax, secreto
    je  gano
    call pista
siguiente:
    dec quedan
    jnz jugar
    lea dx, t_perdio
    call mostrar_cadena
    jmp terminado
no_vale:
    lea dx, t_novale
    call mostrar_cadena
    call nueva_linea
    dec usados
    jmp jugar
gano:
    lea dx, t_gano
    call mostrar_cadena
    mov ax, usados
    call imprimir_numero
terminado:

fin:
    mov ax, 4C00h
    int 21h
main endp

; pista: AX = lo que se dijo; muestra Mas ALTO / Mas BAJO (y muy cerca si está a 3 o menos)
pista proc
    push ax
    push bx
    push dx
    cmp ax, secreto
    lea dx, t_alto
    jb  pista_texto
    lea dx, t_bajo
pista_texto:
    call mostrar_cadena
    mov bx, ax
    sub bx, secreto
    jns pista_pos
    neg bx
pista_pos:
    cmp bx, 3
    ja  pista_fin
    lea dx, t_cerca
    call mostrar_cadena
pista_fin:
    call nueva_linea
    pop dx
    pop bx
    pop ax
    ret
pista endp

; leer_numero: AX = el número tipeado; CF = 1 si no es válido
leer_numero proc
    push bx
    push cx
    push dx
    push si
    mov ah, 0Ah
    lea dx, buffer
    int 21h
    call nueva_linea
    mov cl, buffer+1
    mov ch, 0
    jcxz invalido
    lea si, buffer+2
    mov ax, 0
convertir:
    mov bl, [si]
    cmp bl, '0'
    jb  invalido
    cmp bl, '9'
    ja  invalido
    sub bl, '0'
    mov bh, 0
    mov dx, 10
    mul dx
    jc  invalido
    add ax, bx
    jc  invalido
    inc si
    loop convertir
    clc
    jmp leer_fin
invalido:
    stc
leer_fin:
    pop si
    pop dx
    pop cx
    pop bx
    ret
leer_numero endp

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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Al superarla
Gana en el intento 2, como corresponde. El ogro de la tribuna se va refunfuñando: «antes era más fácil hacer trampa».

#### Imagen
- Una tribuna de madera chica con un ogro grandote sentado solo, enojado, con los brazos cruzados.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) festeja frente a un tablero de cien casilleros con uno dorado.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) sostiene un cartel liso con un dibujito de tilde.
- Gheco (gecko de luz cian con antiparras, chiquito) le saca la lengua al ogro.

### Micro-misión R04-N02-P5 · Otra partida

```meta
lugar: La sala del juego
personajes: Nova, Gheco, Kira, Axón
carta: Jugar otra vez | call partida · preguntar · or al, 20h acepta S y s · je otra_partida
```

#### Escena
El Oráculo está listo: la rutina `partida` juega un juego entero con un secreto de `azar`. Falta lo último: que, al terminar, el Gólem pregunte si quieren **jugar otra vez**.

#### Gheco sugiere
El programa principal muestra el título y entra en un bucle: `call partida`, la pregunta, leer una tecla con la `01h`, pasarla a minúscula con `or al, 20h` y, si es `'s'`, volver a `otra_partida`. Si no, despedirse.

#### Desafío
Escribí el programa principal donde dice `; tus órdenes`. Kira va a jugar dos partidas (contestando `S` en mayúscula a la primera pregunta) y después `n`.

#### Código inicial
```asm
.model small
.stack 100h
.data
semilla  dw 2026
secreto  dw ?
quedan   db ?
usados   dw ?
buffer   db 6, ?, 6 dup(?)
t_titulo db '== EL ORACULO DEL GOLEM ==$'
t_pensado db 13, 10, 'El Golem penso un numero del 1 al 100. Tenes 7 intentos.', 13, 10, '$'
t_intento db 'Intento $'
t_dos     db ': $'
t_alto    db '  Mas ALTO$'
t_bajo    db '  Mas BAJO$'
t_cerca   db ' (muy cerca!)$'
t_novale db '  Eso no es un numero del 1 al 100 (no cuenta).$'
t_gano   db 13, 10, 'ACERTASTE! Intentos usados: $'
t_perdio db 13, 10, 'Se acabaron los intentos. Era el $'
t_otra   db 13, 10, 'Jugar otra vez? (s/n) $'
t_chau   db 13, 10, 'El Golem se inclina. Hasta la proxima.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    ; tus órdenes

fin:
    mov ax, 4C00h
    int 21h
main endp

; partida: un juego completo (secreto con azar, 7 intentos)
partida proc
    push ax
    push bx
    push dx
    mov bl, 100
    call azar
    mov ah, 0
    inc ax
    mov secreto, ax
    mov quedan, 7
    mov usados, 0
    lea dx, t_pensado
    call mostrar_cadena
jugar:
    inc usados
    lea dx, t_intento
    call mostrar_cadena
    mov ax, usados
    call imprimir_numero
    lea dx, t_dos
    call mostrar_cadena
    call leer_numero
    jc  no_vale
    cmp ax, 1
    jb  no_vale
    cmp ax, 100
    ja  no_vale
    cmp ax, secreto
    je  gano
    call pista
    dec quedan
    jnz jugar
    lea dx, t_perdio
    call mostrar_cadena
    mov ax, secreto
    call imprimir_numero
    jmp partida_fin
no_vale:
    lea dx, t_novale
    call mostrar_cadena
    call nueva_linea
    dec usados
    jmp jugar
gano:
    lea dx, t_gano
    call mostrar_cadena
    mov ax, usados
    call imprimir_numero
partida_fin:
    pop dx
    pop bx
    pop ax
    ret
partida endp

; pista: AX = lo que se dijo; muestra Mas ALTO / Mas BAJO (y muy cerca si está a 3 o menos)
pista proc
    push ax
    push bx
    push dx
    cmp ax, secreto
    lea dx, t_alto
    jb  pista_texto
    lea dx, t_bajo
pista_texto:
    call mostrar_cadena
    mov bx, ax
    sub bx, secreto
    jns pista_pos
    neg bx
pista_pos:
    cmp bx, 3
    ja  pista_fin
    lea dx, t_cerca
    call mostrar_cadena
pista_fin:
    call nueva_linea
    pop dx
    pop bx
    pop ax
    ret
pista endp

; azar: AL = número de 0 a BL-1 (avanza la semilla)
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

; leer_numero: AX = el número tipeado; CF = 1 si no es válido
leer_numero proc
    push bx
    push cx
    push dx
    push si
    mov ah, 0Ah
    lea dx, buffer
    int 21h
    call nueva_linea
    mov cl, buffer+1
    mov ch, 0
    jcxz invalido
    lea si, buffer+2
    mov ax, 0
convertir:
    mov bl, [si]
    cmp bl, '0'
    jb  invalido
    cmp bl, '9'
    ja  invalido
    sub bl, '0'
    mov bh, 0
    mov dx, 10
    mul dx
    jc  invalido
    add ax, bx
    jc  invalido
    inc si
    loop convertir
    clc
    jmp leer_fin
invalido:
    stc
leer_fin:
    pop si
    pop dx
    pop cx
    pop bx
    ret
leer_numero endp

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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Entrada
```
50
25
12
6
7
S
50
75
87
93
96
99
98
n
```

#### Salida esperada
```
== EL ORACULO DEL GOLEM ==
El Golem penso un numero del 1 al 100. Tenes 7 intentos.
Intento 1: 50
  Mas BAJO
Intento 2: 25
  Mas BAJO
Intento 3: 12
  Mas BAJO
Intento 4: 6
  Mas ALTO (muy cerca!)
Intento 5: 7

ACERTASTE! Intentos usados: 5
Jugar otra vez? (s/n) S
El Golem penso un numero del 1 al 100. Tenes 7 intentos.
Intento 1: 50
  Mas ALTO
Intento 2: 75
  Mas ALTO
Intento 3: 87
  Mas ALTO
Intento 4: 93
  Mas ALTO
Intento 5: 96
  Mas ALTO (muy cerca!)
Intento 6: 99
  Mas BAJO (muy cerca!)
Intento 7: 98

ACERTASTE! Intentos usados: 7
Jugar otra vez? (s/n) n
El Golem se inclina. Hasta la proxima.
```

#### Solución
```asm
.model small
.stack 100h
.data
semilla  dw 2026
secreto  dw ?
quedan   db ?
usados   dw ?
buffer   db 6, ?, 6 dup(?)
t_titulo db '== EL ORACULO DEL GOLEM ==$'
t_pensado db 13, 10, 'El Golem penso un numero del 1 al 100. Tenes 7 intentos.', 13, 10, '$'
t_intento db 'Intento $'
t_dos     db ': $'
t_alto    db '  Mas ALTO$'
t_bajo    db '  Mas BAJO$'
t_cerca   db ' (muy cerca!)$'
t_novale db '  Eso no es un numero del 1 al 100 (no cuenta).$'
t_gano   db 13, 10, 'ACERTASTE! Intentos usados: $'
t_perdio db 13, 10, 'Se acabaron los intentos. Era el $'
t_otra   db 13, 10, 'Jugar otra vez? (s/n) $'
t_chau   db 13, 10, 'El Golem se inclina. Hasta la proxima.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_titulo
    call mostrar_cadena
otra_partida:
    call partida
    lea dx, t_otra
    call mostrar_cadena
    mov ah, 01h
    int 21h
    or  al, 20h          ; 'S' -> 's'
    cmp al, 's'
    je  otra_partida
    lea dx, t_chau
    call mostrar_cadena

fin:
    mov ax, 4C00h
    int 21h
main endp

; partida: un juego completo (secreto con azar, 7 intentos)
partida proc
    push ax
    push bx
    push dx
    mov bl, 100
    call azar
    mov ah, 0
    inc ax
    mov secreto, ax
    mov quedan, 7
    mov usados, 0
    lea dx, t_pensado
    call mostrar_cadena
jugar:
    inc usados
    lea dx, t_intento
    call mostrar_cadena
    mov ax, usados
    call imprimir_numero
    lea dx, t_dos
    call mostrar_cadena
    call leer_numero
    jc  no_vale
    cmp ax, 1
    jb  no_vale
    cmp ax, 100
    ja  no_vale
    cmp ax, secreto
    je  gano
    call pista
    dec quedan
    jnz jugar
    lea dx, t_perdio
    call mostrar_cadena
    mov ax, secreto
    call imprimir_numero
    jmp partida_fin
no_vale:
    lea dx, t_novale
    call mostrar_cadena
    call nueva_linea
    dec usados
    jmp jugar
gano:
    lea dx, t_gano
    call mostrar_cadena
    mov ax, usados
    call imprimir_numero
partida_fin:
    pop dx
    pop bx
    pop ax
    ret
partida endp

; pista: AX = lo que se dijo; muestra Mas ALTO / Mas BAJO (y muy cerca si está a 3 o menos)
pista proc
    push ax
    push bx
    push dx
    cmp ax, secreto
    lea dx, t_alto
    jb  pista_texto
    lea dx, t_bajo
pista_texto:
    call mostrar_cadena
    mov bx, ax
    sub bx, secreto
    jns pista_pos
    neg bx
pista_pos:
    cmp bx, 3
    ja  pista_fin
    lea dx, t_cerca
    call mostrar_cadena
pista_fin:
    call nueva_linea
    pop dx
    pop bx
    pop ax
    ret
pista endp

; azar: AL = número de 0 a BL-1 (avanza la semilla)
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

; leer_numero: AX = el número tipeado; CF = 1 si no es válido
leer_numero proc
    push bx
    push cx
    push dx
    push si
    mov ah, 0Ah
    lea dx, buffer
    int 21h
    call nueva_linea
    mov cl, buffer+1
    mov ch, 0
    jcxz invalido
    lea si, buffer+2
    mov ax, 0
convertir:
    mov bl, [si]
    cmp bl, '0'
    jb  invalido
    cmp bl, '9'
    ja  invalido
    sub bl, '0'
    mov bh, 0
    mov dx, 10
    mul dx
    jc  invalido
    add ax, bx
    jc  invalido
    inc si
    loop convertir
    clc
    jmp leer_fin
invalido:
    stc
leer_fin:
    pop si
    pop dx
    pop cx
    pop bx
    ret
leer_numero endp

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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Al superarla
Dos partidas, dos victorias: una en 5 intentos y otra justo en el 7. Kira se tira en el piso de la sala, agotada y feliz.

{mentor} hace un ruido que nadie había escuchado nunca: un engranaje que gira rápido, como una risa. —Jugué —dice—. Por primera vez en siglos, **jugué**.

#### Imagen
- Un gólem de bronce gigante sentado en el piso de una caverna, con el ojo encendido y una postura relajada, como si se riera.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) tirada en el piso boca arriba, agotada y sonriente.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) flota sobre ella, riéndose.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre la panza de Kira, con los brazos abiertos.

### Prueba del sello

#### Si lo que dijo el jugador es menor que el secreto, ¿qué pista se da?
«Más alto»: el secreto está arriba.

#### ¿Cómo se calcula la distancia entre dos números sin que dé negativa?
Se restan y, si el resultado es negativo (no salta `jns`), se le da vuelta el signo con `neg`.

#### ¿Por qué con 7 intentos alcanza siempre para adivinar entre 1 y 100?
Porque partiendo a la mitad cada intento descarta la mitad de los números, y 2⁷ = 128 ≥ 100 (búsqueda binaria).

#### ¿Qué hace `or al, 20h` con una letra?
Prende el bit 5: la pasa a minúscula (`'S'` → `'s'`).

## R04-N03 · Proyecto: Kira contra el Autómata de Hierro

```meta
tipo: tema
criatura: ogre
padre: R04-N02
precio: 0
temas: juegos.bucle, prog.menu
usa: prog.funciones, prog.matematica-azar, prog.bits, maq.direcciones
```

### Crónica

Maese Ferrum baja desde las Forjas a ver al Gólem que camina. Trae un regalo para Kira: un **autómata de hierro** de entrenamiento, alto como dos enanos, con un garrote de práctica. —Antes de que te enfrentes a algo de verdad —le dice—, entrená.

Kira tiene su espada, un escudo y dos pociones. {mentor} lleva la cuenta de cada golpe en sus palancas. —Es la prueba de todo lo que aprendiste, Nova —dice el Gólem—. Cada rutina que escribiste, junta.

### Objetivos

Integrar todo en un **combate por turnos**: variables de estado, menú con teclas sin eco, azar, comparaciones,
bits para multiplicar y dividir (`shl`, `shr`), una rutina que trabaja con la **dirección** de una variable
(`[si]`), barras de vida y el bucle de rondas.

### Antes de empezar

- Todo el curso, en especial las rutinas, el grimorio de los números, bits y el azar.

### Explicación

#### Las reglas
- Kira: 30 de vida y 2 pociones. El autómata: 40 de vida.
- Turno de Kira (tecla sin eco; las inválidas se ignoran):
  1. **Atacar**: daño de 3 a 8; 1 de cada 6 es **crítico** (daño × 2).
  2. **Defender**: este turno, el golpe del autómata vale la mitad.
  3. **Poción**: +10 de vida (con tope 30). Sin pociones, pierde el turno.
- Turno del autómata: daño de 2 a 7; 1 de cada 5 es **furia** (+4).
- Gana quien deja al otro en 0.

#### La estructura
```
main:           ronda nueva -> mostrar_estado -> turno_kira -> ¿autómata en 0? -> turno_auto -> ¿Kira en 0?
turno_kira:     leer_accion (1, 2 o 3) -> atacar / defender / pocion
turno_auto:     el golpe (furia, escudo)
quitar_vida:    SI = la dirección de la vida, CL = el daño; la vida no baja de 0
mostrar_estado: las dos barras con sus números
```

#### Una rutina para las dos vidas
`quitar_vida` recibe en SI **la dirección** de la vida (`lea si, vida_k` o `lea si, vida_o`) y trabaja con `[si]`.
El mismo código sirve para los dos personajes:
```asm
cmp cl, [si]
jae queda_cero         ; el daño es mayor o igual: queda en 0
sub [si], cl
```
Sin ese `cmp`, restar 8 a una vida de 5 da 253 (el byte da la vuelta) y el autómata «resucita».

#### Bits que multiplican y dividen
- Crítico: `shl cl, 1` (× 2).
- Escudo: `shr cl, 1` (÷ 2, redondeando para abajo).

> **Puente con otras lenguas.** Todo videojuego tiene este **bucle de juego**: leer lo que hace el jugador,
> actualizar el estado, dibujar, repetir. En Python con pygame, en C con SDL o en un motor como Godot, la forma es
> la misma. Y pasar «la dirección de la vida» es pasar un **puntero** (C) o una **referencia** (Java, Python).

### Código de ejemplo

```asm
.model small
.stack 100h
.data
vida_k db 30
vida_o db 40
t_kira db 'Kira     $'
t_auto db 'Automata $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, vida_o
    mov cl, 12
    call quitar_vida
    lea dx, t_kira
    mov ah, 09h
    int 21h
    mov al, vida_k
    mov bl, 30
    call barra
    call nueva_linea
    lea dx, t_auto
    mov ah, 09h
    int 21h
    mov al, vida_o
    mov bl, 40
    call barra

fin:
    mov ax, 4C00h
    int 21h
main endp

; quitar_vida: SI = dirección de la vida, CL = daño (la vida no baja de 0)
quitar_vida proc
    cmp cl, [si]
    jae queda_cero
    sub [si], cl
    ret
queda_cero:
    mov byte ptr [si], 0
    ret
quitar_vida endp

; barra: AL = vida, BL = máximo; un casillero cada 2 puntos (# lleno, . vacío)
barra proc
    push ax
    push bx
    push cx
    push dx
    shr al, 1
    shr bl, 1
    sub bl, al
    mov cl, al
    mov ch, 0
    mov dl, '#'
    mov ah, 02h
    jcxz sin_llenos
llenos:
    int 21h
    loop llenos
sin_llenos:
    mov cl, bl
    mov dl, '.'
    jcxz sin_vacios
vacios:
    int 21h
    loop vacios
sin_vacios:
    pop dx
    pop cx
    pop bx
    pop ax
    ret
barra endp

nueva_linea proc
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
nueva_linea endp

end main
```

### Salida esperada

```
Kira     ###############
Automata ##############......
```

### ¿Para qué sirve?

Un juego por turnos usa casi todo lo que sabe hacer un programador: estado, entrada, azar, reglas, pantalla y un
bucle que no termina hasta que alguien gana. Y la idea de pasar la **dirección** de un dato a una rutina, para que
lo cambie, está en el corazón de C, C++ y de cómo funcionan los objetos en todos los lenguajes.

### Errores habituales

**Ogro: la vida que da la vuelta.** `sub [si], cl` sin comparar antes: con 5 de vida y 8 de daño, quedan 253.

**Goblin: `sub [si], 8` sin tamaño.** Con un número suelto, el Gólem no sabe si `[si]` es uno o dos cajones:
`sub byte ptr [si], 8`. (Con `cl` no hace falta: CL ya dice que es un byte.)

**Ogro: el escudo que nunca se baja.** Si `defiende` no vuelve a 0 después del golpe, Kira queda protegida para
siempre.

**Troll: rutinas que pisan.** `atacar` usa BL y CL para el azar y el daño: si no los guarda, rompe a quien la
llamó.

### Micro-misión R04-N03-P1 · La vida que da la vuelta

```meta
lugar: El campo de entrenamiento
personajes: Nova, Gheco, Kira
criatura: ogre
carta: Una rutina, dos vidas | SI = la dirección de la vida · [si] = la vida · cmp antes de sub: no baja de 0
```

#### Escena
Kira le pega al autómata, que tenía **5** de vida, un golpe de **8**. El autómata no cae: se levanta con **253** de vida. Ferrum se rasca la barba. Un ogro, mirando desde la cerca, se ríe.

#### Gheco sugiere
`sub [si], cl` con 5 − 8 da la vuelta y queda en 253. Antes de restar, compará el daño con la vida (`cmp cl, [si]`): si es mayor o igual (`jae`), la vida queda en **0** (`mov byte ptr [si], 0`).

#### Desafío
Ejecutá y mirá los cajones de las vidas. Después arreglá `quitar_vida` para que la vida nunca baje de 0.

#### Código inicial
```asm
.model small
.stack 100h
.data
vida_k db 30
vida_o db 5
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, vida_k
    mov cl, 6
    call quitar_vida
    lea si, vida_o
    mov cl, 8
    call quitar_vida

fin:
    mov ax, 4C00h
    int 21h
main endp

; quitar_vida: SI = dirección de la vida, CL = daño (la vida no baja de 0)
quitar_vida proc
    sub [si], cl
    ret
quitar_vida endp

end main
```

#### Estado esperado
```
[vida_k] = 24
[vida_o] = 0
```

#### Solución
```asm
.model small
.stack 100h
.data
vida_k db 30
vida_o db 5
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, vida_k
    mov cl, 6
    call quitar_vida
    lea si, vida_o
    mov cl, 8
    call quitar_vida

fin:
    mov ax, 4C00h
    int 21h
main endp

; quitar_vida: SI = dirección de la vida, CL = daño (la vida no baja de 0)
quitar_vida proc
    cmp cl, [si]
    jae queda_cero
    sub [si], cl
    ret
queda_cero:
    mov byte ptr [si], 0
    ret
quitar_vida endp

end main
```

#### Al superarla
El autómata cae, como corresponde, y se queda quieto en el piso. —Una sola rutina para las dos vidas —dice Nova—. Le paso **dónde** está la vida, y ella la cambia.

#### Imagen
- Un autómata de hierro alto, de entrenamiento, con un garrote de práctica, cayendo de espaldas sobre el pasto.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) con la espada en alto, recién terminado el golpe.
- Un ogro grandote se ríe apoyado en una cerca de madera.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre la cerca, señalando al ogro.

### Micro-misión R04-N03-P2 · Crítico y escudo

```meta
lugar: El campo de entrenamiento
personajes: Nova, Gheco, Kira
carta: shl y shr | shl x, 1 = el doble · shr x, 1 = la mitad (redondea para abajo)
```

#### Escena
Kira practica dos cosas: el **golpe crítico** (que hace el doble de daño) y el **escudo** (que le saca la mitad al golpe del autómata).

#### Gheco sugiere
Correr los bits un lugar a la izquierda (`shl`) multiplica por 2; a la derecha (`shr`), divide por 2.

#### Desafío
Completá las dos órdenes para que el crítico de 7 haga **14** y el golpe de 9, con escudo, haga **4**.

#### Código inicial
```asm
.model small
.stack 100h
.data
danio db 7
golpe db 9
.code
main proc
    mov ax, @data
    mov ds, ax

    mov cl, danio
    ___ cl, 1            ; crítico: el doble
    mov dl, golpe
    ___ dl, 1            ; con escudo: la mitad

fin:
    mov ax, 4C00h
    int 21h
main endp

end main
```

#### Estado esperado
```
CL = 14
DL = 4
```

#### Solución
```asm
.model small
.stack 100h
.data
danio db 7
golpe db 9
.code
main proc
    mov ax, @data
    mov ds, ax

    mov cl, danio
    shl cl, 1            ; crítico: el doble
    mov dl, golpe
    shr dl, 1            ; con escudo: la mitad

fin:
    mov ax, 4C00h
    int 21h
main endp

end main
```

#### Al superarla
—Catorce y cuatro —anota Ferrum, impresionado—. ¿Y cómo dividiste tan rápido? —Moví los interruptores un lugar —dice Nova—. Nada más.

#### Imagen
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) cubriéndose con un escudo redondo de bronce mientras un garrote de práctica rebota en él.
- Maese Ferrum, un herrero humano enorme de unos dos metros, NO es enano, con barba gris trenzada, un ojo mecánico naranja y delantal de cuero, mira con los brazos cruzados.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) flota cerca, con una chispa cian en cada mano.
- Gheco (gecko de luz cian con antiparras, chiquito) sentado en el escudo.

### Micro-misión R04-N03-P3 · Las barras de vida

```meta
lugar: El campo de entrenamiento
personajes: Nova, Gheco
carta: Barra | llenos = vida / 2 · vacíos = máximo / 2 - llenos · shr para dividir · jcxz si son 0
```

#### Escena
El ojo del Gólem tiene que mostrar cómo va cada uno: una **barra** de `#` (lo que queda) y `.` (lo que se perdió), un casillero cada 2 puntos de vida.

#### Gheco sugiere
Con `shr al, 1` y `shr bl, 1` tenés los casilleros llenos y el total. Los vacíos son el total menos los llenos. Dos bucles con la `02h`: primero los `#`, después los `.`. Si alguno da 0, `jcxz` lo saltea (si no, `loop` daría 65.536 vueltas).

#### Desafío
Escribí el cuerpo de `barra` donde dice `; tus órdenes`.

#### Código inicial
```asm
.model small
.stack 100h
.data

.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 22
    mov bl, 30
    call barra
    call nueva_linea
    mov al, 7
    mov bl, 40
    call barra

fin:
    mov ax, 4C00h
    int 21h
main endp

; barra: AL = vida, BL = máximo; un casillero cada 2 puntos (# lleno, . vacío)
barra proc
    push ax
    push bx
    push cx
    push dx
    ; tus órdenes
    pop dx
    pop cx
    pop bx
    pop ax
    ret
barra endp

nueva_linea proc
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
nueva_linea endp

end main
```

#### Salida esperada
```
###########....
###.................
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

    mov al, 22
    mov bl, 30
    call barra
    call nueva_linea
    mov al, 7
    mov bl, 40
    call barra

fin:
    mov ax, 4C00h
    int 21h
main endp

; barra: AL = vida, BL = máximo; un casillero cada 2 puntos (# lleno, . vacío)
barra proc
    push ax
    push bx
    push cx
    push dx
    shr al, 1
    shr bl, 1
    sub bl, al
    mov cl, al
    mov ch, 0
    mov dl, '#'
    mov ah, 02h
    jcxz sin_llenos
llenos:
    int 21h
    loop llenos
sin_llenos:
    mov cl, bl
    mov dl, '.'
    jcxz sin_vacios
vacios:
    int 21h
    loop vacios
sin_vacios:
    pop dx
    pop cx
    pop bx
    pop ax
    ret
barra endp

nueva_linea proc
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
nueva_linea endp

end main
```

#### Al superarla
Dos barras en el ojo: Kira con 11 de 15 casilleros, el autómata con 3 de 20. —Ahora se ve quién va ganando —dice Gheco.

#### Imagen
- Dos barras horizontales de luz en un ojo de cristal gigante: una verde casi llena y una roja casi vacía.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) ajusta la barra verde con la mano.
- Gheco (gecko de luz cian con antiparras, chiquito) colgado de la barra roja, que se vacía.

### Micro-misión R04-N03-P4 · La tecla que vale

```meta
lugar: El campo de entrenamiento
personajes: Nova, Gheco, Kira
carta: Leer hasta que valga | 07h sin eco · fuera de '1'..'3': leer otra · la válida se muestra y se guarda
```

#### Escena
En medio del combate, Kira aprieta cualquier cosa: una **x**, un **5**… El Gólem tiene que ignorar lo que no es una acción y esperar a que llegue un 1, un 2 o un 3.

#### Gheco sugiere
Un «hasta que»: leé una tecla con la `07h` (sin eco); si es menor que `'1'` o mayor que `'3'`, volvé a leer. Cuando vale, guardala en `accion`, mostrala con la `02h` y pasá de renglón.

#### Desafío
Escribí el cuerpo de `leer_accion` donde dice `; tus órdenes`. Kira va a apretar `x`, `5` y `2`.

#### Código inicial
```asm
.model small
.stack 100h
.data
accion db ?
.code
main proc
    mov ax, @data
    mov ds, ax

    call leer_accion

fin:
    mov ax, 4C00h
    int 21h
main endp

; leer_accion: espera una tecla sin eco hasta que sea '1', '2' o '3'; la muestra y la guarda en accion
leer_accion proc
    push ax
    push dx
    ; tus órdenes
    pop dx
    pop ax
    ret
leer_accion endp

nueva_linea proc
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
nueva_linea endp

end main
```

#### Entrada
```
x
5
2
```

#### Salida esperada
```
2
```

#### Estado esperado
```
[accion] = '2'
```

#### Solución
```asm
.model small
.stack 100h
.data
accion db ?
.code
main proc
    mov ax, @data
    mov ds, ax

    call leer_accion

fin:
    mov ax, 4C00h
    int 21h
main endp

; leer_accion: espera una tecla sin eco hasta que sea '1', '2' o '3'; la muestra y la guarda en accion
leer_accion proc
    push ax
    push dx
otra_tecla:
    mov ah, 07h
    int 21h
    cmp al, '1'
    jb  otra_tecla
    cmp al, '3'
    ja  otra_tecla
    mov accion, al
    mov dl, al
    mov ah, 02h
    int 21h
    call nueva_linea
    pop dx
    pop ax
    ret
leer_accion endp

nueva_linea proc
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
nueva_linea endp

end main
```

#### Al superarla
La x y el 5 no aparecen en el ojo: el Gólem los ignoró en silencio. Solo el 2. —Defender —dice Kira, y levanta el escudo justo a tiempo.

#### Imagen
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) con los dedos sobre una botonera de bronce de tres botones, con otros botones apagados alrededor.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) sostiene en las manos tres lucecitas: solo una brilla.
- Gheco (gecko de luz cian con antiparras, chiquito) barre con la cola dos lucecitas apagadas.

### Micro-misión R04-N03-P5 · La última poción

```meta
lugar: El campo de entrenamiento
personajes: Nova, Gheco, Kira
carta: Con tope | si no quedan: mensaje y nada más · si quedan: dec · add 10 · si pasa de 30, queda en 30
```

#### Escena
A Kira le quedan **25** de vida y **una** poción. Toma una, y después, distraída, intenta tomar otra.

#### Gheco sugiere
Si `pociones` es 0, mostrá el mensaje de que no quedan y listo. Si no: restale una poción, sumale 10 a `vida_k` y, si pasó de 30 (`jbe` para dejarla si no), ponela en 30. Después, el mensaje de la poción. Los textos ya están.

#### Desafío
Escribí el cuerpo de `pocion` donde dice `; tus órdenes`.

#### Código inicial
```asm
.model small
.stack 100h
.data
vida_k   db 25
pociones db 1
t_pocion db 'Kira bebe una pocion: +10 de vida.', 13, 10, '$'
t_sinpoc db 'No quedan pociones: Kira pierde el turno.', 13, 10, '$'
.code
main proc
    mov ax, @data
    mov ds, ax

    call pocion
    call pocion

fin:
    mov ax, 4C00h
    int 21h
main endp

; pocion: +10 de vida (tope 30) si quedan pociones; si no, pierde el turno
pocion proc
    push ax
    push dx
    ; tus órdenes
    pop dx
    pop ax
    ret
pocion endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Salida esperada
```
Kira bebe una pocion: +10 de vida.
No quedan pociones: Kira pierde el turno.
```

#### Estado esperado
```
[vida_k] = 30
[pociones] = 0
```

#### Solución
```asm
.model small
.stack 100h
.data
vida_k   db 25
pociones db 1
t_pocion db 'Kira bebe una pocion: +10 de vida.', 13, 10, '$'
t_sinpoc db 'No quedan pociones: Kira pierde el turno.', 13, 10, '$'
.code
main proc
    mov ax, @data
    mov ds, ax

    call pocion
    call pocion

fin:
    mov ax, 4C00h
    int 21h
main endp

; pocion: +10 de vida (tope 30) si quedan pociones; si no, pierde el turno
pocion proc
    push ax
    push dx
    cmp pociones, 0
    je  sin_pociones
    dec pociones
    add vida_k, 10
    cmp vida_k, 30
    jbe pocion_ok
    mov vida_k, 30
pocion_ok:
    lea dx, t_pocion
    call mostrar_cadena
    jmp pocion_fin
sin_pociones:
    lea dx, t_sinpoc
    call mostrar_cadena
pocion_fin:
    pop dx
    pop ax
    ret
pocion endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Al superarla
Vida llena (30, no 35) y ninguna poción. El segundo intento no hace nada más que avisar. —El tope es para que nadie sea más fuerte de lo que puede ser —dice Ferrum.

#### Imagen
- Un frasquito de vidrio vacío cayendo al pasto, y otro estante vacío al lado.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) se seca la boca con el dorso de la mano, renovada.
- Gheco (gecko de luz cian con antiparras, chiquito) da vuelta el frasquito vacío buscando una última gota.

### Micro-misión R04-N03-P6 · El combate

```meta
lugar: El campo de entrenamiento
personajes: Nova, Gheco, Kira, Axón
carta: Bucle de juego | ronda: estado · turno de Kira · ¿cayó el autómata? · turno del autómata · ¿cayó Kira? · otra ronda
```

#### Escena
Todas las piezas están listas: `turno_kira`, `turno_auto`, `quitar_vida`, `mostrar_estado`… Falta el corazón del juego: el **bucle de rondas**. Ferrum da la señal.

#### Gheco sugiere
Una etiqueta `ronda_nueva:`. En cada ronda: sumá 1 a `ronda` y mostrá el encabezado (`t_ronda`, el número, `t_rfin`), `call mostrar_estado`, `call turno_kira`; si `vida_o` quedó en 0, `gana`. Si no, `call turno_auto`; si `vida_k` quedó en 0, `pierde`. Si no, otra ronda. Al final, el mensaje que corresponda.

#### Desafío
Escribí el programa principal donde dice `; tus órdenes`. Kira va a jugar 1, 1, 1, 3, 1, 2 y 1.

#### Código inicial
```asm
.model small
.stack 100h
.data
semilla  dw 46
vida_k   db 30
vida_o   db 40
pociones db 2
defiende db 0
accion   db ?
ronda    dw 0
t_titulo db ' KIRA CONTRA EL AUTOMATA DE HIERRO$'
t_ronda  db 13, 10, '--- Ronda $'
t_rfin   db ' ---', 13, 10, '$'
t_kira   db 'Kira     $'
t_auto   db 'Automata $'
t_menu   db '1) Atacar  2) Defender  3) Pocion: $'
t_ataca  db 'Kira ataca: $'
t_crit   db 'CRITICO! $'
t_danio  db ' de danio.', 13, 10, '$'
t_defi   db 'Kira levanta el escudo.', 13, 10, '$'
t_pocion db 'Kira bebe una pocion: +10 de vida.', 13, 10, '$'
t_sinpoc db 'No quedan pociones: Kira pierde el turno.', 13, 10, '$'
t_golpe  db 'El automata golpea: $'
t_furia  db 'FURIA! $'
t_gana   db 13, 10, 'El automata cae. GANO KIRA!$'
t_pierde db 13, 10, 'Kira cae. Gano el automata.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_titulo
    call mostrar_cadena
    ; tus órdenes

fin:
    mov ax, 4C00h
    int 21h
main endp

; turno_kira: menú, acción
turno_kira proc
    push dx
    lea dx, t_menu
    call mostrar_cadena
    call leer_accion
    cmp accion, '1'
    jne no_ataca
    call atacar
    jmp turno_fin
no_ataca:
    cmp accion, '2'
    jne no_defiende
    mov defiende, 1
    lea dx, t_defi
    call mostrar_cadena
    jmp turno_fin
no_defiende:
    call pocion
turno_fin:
    pop dx
    ret
turno_kira endp

; atacar: daño de 3 a 8; 1 de cada 6 es crítico (daño x 2)
atacar proc
    push ax
    push bx
    push cx
    push dx
    lea dx, t_ataca
    call mostrar_cadena
    mov bl, 6
    call azar
    mov cl, al
    add cl, 3
    mov bl, 6
    call azar
    cmp al, 0
    jne sin_critico
    shl cl, 1
    lea dx, t_crit
    call mostrar_cadena
sin_critico:
    mov al, cl
    mov ah, 0
    call imprimir_numero
    lea dx, t_danio
    call mostrar_cadena
    lea si, vida_o
    call quitar_vida
    pop dx
    pop cx
    pop bx
    pop ax
    ret
atacar endp

; turno_auto: daño de 2 a 7; 1 de cada 5 es furia (+4); con escudo, la mitad
turno_auto proc
    push ax
    push bx
    push cx
    push dx
    lea dx, t_golpe
    call mostrar_cadena
    mov bl, 6
    call azar
    mov cl, al
    add cl, 2
    mov bl, 5
    call azar
    cmp al, 0
    jne sin_furia
    add cl, 4
    lea dx, t_furia
    call mostrar_cadena
sin_furia:
    cmp defiende, 0
    je  sin_escudo
    shr cl, 1
    mov defiende, 0
sin_escudo:
    mov al, cl
    mov ah, 0
    call imprimir_numero
    lea dx, t_danio
    call mostrar_cadena
    lea si, vida_k
    call quitar_vida
    pop dx
    pop cx
    pop bx
    pop ax
    ret
turno_auto endp

; pocion: +10 de vida (tope 30) si quedan pociones; si no, pierde el turno
pocion proc
    push ax
    push dx
    cmp pociones, 0
    je  sin_pociones
    dec pociones
    add vida_k, 10
    cmp vida_k, 30
    jbe pocion_ok
    mov vida_k, 30
pocion_ok:
    lea dx, t_pocion
    call mostrar_cadena
    jmp pocion_fin
sin_pociones:
    lea dx, t_sinpoc
    call mostrar_cadena
pocion_fin:
    pop dx
    pop ax
    ret
pocion endp

; leer_accion: espera una tecla sin eco hasta que sea '1', '2' o '3'; la muestra y la guarda en accion
leer_accion proc
    push ax
    push dx
otra_tecla:
    mov ah, 07h
    int 21h
    cmp al, '1'
    jb  otra_tecla
    cmp al, '3'
    ja  otra_tecla
    mov accion, al
    mov dl, al
    mov ah, 02h
    int 21h
    call nueva_linea
    pop dx
    pop ax
    ret
leer_accion endp

; mostrar_estado: las dos barras con sus números
mostrar_estado proc
    push ax
    push bx
    push dx
    lea dx, t_kira
    call mostrar_cadena
    mov al, vida_k
    mov bl, 30
    call barra
    call espacio
    mov ah, 0
    call imprimir_numero
    call nueva_linea
    lea dx, t_auto
    call mostrar_cadena
    mov al, vida_o
    mov bl, 40
    call barra
    call espacio
    mov ah, 0
    call imprimir_numero
    call nueva_linea
    pop dx
    pop bx
    pop ax
    ret
mostrar_estado endp

; barra: AL = vida, BL = máximo; un casillero cada 2 puntos (# lleno, . vacío)
barra proc
    push ax
    push bx
    push cx
    push dx
    shr al, 1
    shr bl, 1
    sub bl, al
    mov cl, al
    mov ch, 0
    mov dl, '#'
    mov ah, 02h
    jcxz sin_llenos
llenos:
    int 21h
    loop llenos
sin_llenos:
    mov cl, bl
    mov dl, '.'
    jcxz sin_vacios
vacios:
    int 21h
    loop vacios
sin_vacios:
    pop dx
    pop cx
    pop bx
    pop ax
    ret
barra endp

; quitar_vida: SI = dirección de la vida, CL = daño (la vida no baja de 0)
quitar_vida proc
    cmp cl, [si]
    jae queda_cero
    sub [si], cl
    ret
queda_cero:
    mov byte ptr [si], 0
    ret
quitar_vida endp

; azar: AL = número de 0 a BL-1 (avanza la semilla)
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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Entrada
```
1
1
1
3
1
2
1
```

#### Salida esperada
```
 KIRA CONTRA EL AUTOMATA DE HIERRO
--- Ronda 1 ---
Kira     ############### 30
Automata #################### 40
1) Atacar  2) Defender  3) Pocion: 1
Kira ataca: 6 de danio.
El automata golpea: 4 de danio.

--- Ronda 2 ---
Kira     #############.. 26
Automata #################... 34
1) Atacar  2) Defender  3) Pocion: 1
Kira ataca: CRITICO! 16 de danio.
El automata golpea: FURIA! 10 de danio.

--- Ronda 3 ---
Kira     ########....... 16
Automata #########........... 18
1) Atacar  2) Defender  3) Pocion: 1
Kira ataca: 3 de danio.
El automata golpea: FURIA! 10 de danio.

--- Ronda 4 ---
Kira     ###............ 6
Automata #######............. 15
1) Atacar  2) Defender  3) Pocion: 3
Kira bebe una pocion: +10 de vida.
El automata golpea: FURIA! 9 de danio.

--- Ronda 5 ---
Kira     ###............ 7
Automata #######............. 15
1) Atacar  2) Defender  3) Pocion: 1
Kira ataca: 8 de danio.
El automata golpea: 2 de danio.

--- Ronda 6 ---
Kira     ##............. 5
Automata ###................. 7
1) Atacar  2) Defender  3) Pocion: 2
Kira levanta el escudo.
El automata golpea: 3 de danio.

--- Ronda 7 ---
Kira     #.............. 2
Automata ###................. 7
1) Atacar  2) Defender  3) Pocion: 1
Kira ataca: 8 de danio.

El automata cae. GANO KIRA!
```

#### Solución
```asm
.model small
.stack 100h
.data
semilla  dw 46
vida_k   db 30
vida_o   db 40
pociones db 2
defiende db 0
accion   db ?
ronda    dw 0
t_titulo db ' KIRA CONTRA EL AUTOMATA DE HIERRO$'
t_ronda  db 13, 10, '--- Ronda $'
t_rfin   db ' ---', 13, 10, '$'
t_kira   db 'Kira     $'
t_auto   db 'Automata $'
t_menu   db '1) Atacar  2) Defender  3) Pocion: $'
t_ataca  db 'Kira ataca: $'
t_crit   db 'CRITICO! $'
t_danio  db ' de danio.', 13, 10, '$'
t_defi   db 'Kira levanta el escudo.', 13, 10, '$'
t_pocion db 'Kira bebe una pocion: +10 de vida.', 13, 10, '$'
t_sinpoc db 'No quedan pociones: Kira pierde el turno.', 13, 10, '$'
t_golpe  db 'El automata golpea: $'
t_furia  db 'FURIA! $'
t_gana   db 13, 10, 'El automata cae. GANO KIRA!$'
t_pierde db 13, 10, 'Kira cae. Gano el automata.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_titulo
    call mostrar_cadena
ronda_nueva:
    inc ronda
    lea dx, t_ronda
    call mostrar_cadena
    mov ax, ronda
    call imprimir_numero
    lea dx, t_rfin
    call mostrar_cadena
    call mostrar_estado
    call turno_kira
    cmp vida_o, 0
    je  gana
    call turno_auto
    cmp vida_k, 0
    je  pierde
    jmp ronda_nueva
gana:
    lea dx, t_gana
    call mostrar_cadena
    jmp termino
pierde:
    lea dx, t_pierde
    call mostrar_cadena
termino:

fin:
    mov ax, 4C00h
    int 21h
main endp

; turno_kira: menú, acción
turno_kira proc
    push dx
    lea dx, t_menu
    call mostrar_cadena
    call leer_accion
    cmp accion, '1'
    jne no_ataca
    call atacar
    jmp turno_fin
no_ataca:
    cmp accion, '2'
    jne no_defiende
    mov defiende, 1
    lea dx, t_defi
    call mostrar_cadena
    jmp turno_fin
no_defiende:
    call pocion
turno_fin:
    pop dx
    ret
turno_kira endp

; atacar: daño de 3 a 8; 1 de cada 6 es crítico (daño x 2)
atacar proc
    push ax
    push bx
    push cx
    push dx
    lea dx, t_ataca
    call mostrar_cadena
    mov bl, 6
    call azar
    mov cl, al
    add cl, 3
    mov bl, 6
    call azar
    cmp al, 0
    jne sin_critico
    shl cl, 1
    lea dx, t_crit
    call mostrar_cadena
sin_critico:
    mov al, cl
    mov ah, 0
    call imprimir_numero
    lea dx, t_danio
    call mostrar_cadena
    lea si, vida_o
    call quitar_vida
    pop dx
    pop cx
    pop bx
    pop ax
    ret
atacar endp

; turno_auto: daño de 2 a 7; 1 de cada 5 es furia (+4); con escudo, la mitad
turno_auto proc
    push ax
    push bx
    push cx
    push dx
    lea dx, t_golpe
    call mostrar_cadena
    mov bl, 6
    call azar
    mov cl, al
    add cl, 2
    mov bl, 5
    call azar
    cmp al, 0
    jne sin_furia
    add cl, 4
    lea dx, t_furia
    call mostrar_cadena
sin_furia:
    cmp defiende, 0
    je  sin_escudo
    shr cl, 1
    mov defiende, 0
sin_escudo:
    mov al, cl
    mov ah, 0
    call imprimir_numero
    lea dx, t_danio
    call mostrar_cadena
    lea si, vida_k
    call quitar_vida
    pop dx
    pop cx
    pop bx
    pop ax
    ret
turno_auto endp

; pocion: +10 de vida (tope 30) si quedan pociones; si no, pierde el turno
pocion proc
    push ax
    push dx
    cmp pociones, 0
    je  sin_pociones
    dec pociones
    add vida_k, 10
    cmp vida_k, 30
    jbe pocion_ok
    mov vida_k, 30
pocion_ok:
    lea dx, t_pocion
    call mostrar_cadena
    jmp pocion_fin
sin_pociones:
    lea dx, t_sinpoc
    call mostrar_cadena
pocion_fin:
    pop dx
    pop ax
    ret
pocion endp

; leer_accion: espera una tecla sin eco hasta que sea '1', '2' o '3'; la muestra y la guarda en accion
leer_accion proc
    push ax
    push dx
otra_tecla:
    mov ah, 07h
    int 21h
    cmp al, '1'
    jb  otra_tecla
    cmp al, '3'
    ja  otra_tecla
    mov accion, al
    mov dl, al
    mov ah, 02h
    int 21h
    call nueva_linea
    pop dx
    pop ax
    ret
leer_accion endp

; mostrar_estado: las dos barras con sus números
mostrar_estado proc
    push ax
    push bx
    push dx
    lea dx, t_kira
    call mostrar_cadena
    mov al, vida_k
    mov bl, 30
    call barra
    call espacio
    mov ah, 0
    call imprimir_numero
    call nueva_linea
    lea dx, t_auto
    call mostrar_cadena
    mov al, vida_o
    mov bl, 40
    call barra
    call espacio
    mov ah, 0
    call imprimir_numero
    call nueva_linea
    pop dx
    pop bx
    pop ax
    ret
mostrar_estado endp

; barra: AL = vida, BL = máximo; un casillero cada 2 puntos (# lleno, . vacío)
barra proc
    push ax
    push bx
    push cx
    push dx
    shr al, 1
    shr bl, 1
    sub bl, al
    mov cl, al
    mov ch, 0
    mov dl, '#'
    mov ah, 02h
    jcxz sin_llenos
llenos:
    int 21h
    loop llenos
sin_llenos:
    mov cl, bl
    mov dl, '.'
    jcxz sin_vacios
vacios:
    int 21h
    loop vacios
sin_vacios:
    pop dx
    pop cx
    pop bx
    pop ax
    ret
barra endp

; quitar_vida: SI = dirección de la vida, CL = daño (la vida no baja de 0)
quitar_vida proc
    cmp cl, [si]
    jae queda_cero
    sub [si], cl
    ret
queda_cero:
    mov byte ptr [si], 0
    ret
quitar_vida endp

; azar: AL = número de 0 a BL-1 (avanza la semilla)
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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Al superarla
**GANO KIRA**, con 2 de vida, en la séptima ronda. El autómata se desarma en el pasto con un ruido de ollas. Ferrum aplaude despacio, tres veces, y eso, viniendo de él, es una ovación.

Pero en ese momento, el piso tiembla. Desde lo más profundo del Gólem, desde el núcleo mismo, sube un calor que no es el de los hornos. Nova lo siente antes que nadie: **algo se despertó adentro**.

#### Imagen
- Un autómata de hierro de entrenamiento desarmado en el pasto, con piezas desparramadas.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) de rodillas, agotada pero sonriente, apoyada en su espada.
- Maese Ferrum, un herrero humano enorme de unos dos metros, NO es enano, con barba gris trenzada, un ojo mecánico naranja y delantal de cuero, aplaude.
- Al fondo, un gólem de bronce gigante con el pecho que empieza a brillar en rojo desde adentro.
- Gheco (gecko de luz cian con antiparras, chiquito) mira el brillo rojo, con la cola erizada.

### Prueba del sello

#### ¿Por qué `quitar_vida` recibe en SI la dirección de la vida y no la vida?
Para que la misma rutina pueda cambiar la vida de cualquiera de los dos: trabaja sobre el cajón al que apunta SI.

#### ¿Qué pasa si se resta el daño sin comparar antes?
Si el daño es mayor que la vida, el byte da la vuelta (5 − 8 = 253).

#### ¿Cómo se duplica y cómo se divide por 2 un daño con bits?
`shl cl, 1` lo duplica; `shr cl, 1` lo divide por 2 (redondeando para abajo).

#### ¿Qué partes tiene el bucle de un juego por turnos?
Mostrar el estado, el turno del jugador, ver si alguien cayó, el turno del rival, ver si alguien cayó, y repetir.

## R04-N04 · Jefe final: el Dragón del Gólem

```meta
tipo: jefe
criatura: dragon
padre: R04-N03
precio: 0
insignia: Sello del Dragón
insignia_descripcion: Venciste al Dragón del Gólem: armás programas grandes con piezas chicas, y el Gólem camina gracias a vos.
usa: prog.bits, col.arrays, maq.pila, prog.funciones, prog.matematica-azar, juegos.bucle
temas: cal.depuracion
```

### Crónica

En el núcleo de {mentor}, donde Nova despertó, hay algo que no estaba: un **dragón** de luz roja, enroscado alrededor del corazón de bronce. Nació hace siglos de todas las órdenes que nadie terminó de escribir, y dormía. El Gólem caminando lo despertó.

—Un dragón no se vence de un golpe —dice Gheco, muy serio por primera vez—. Se lo divide en partes. Se vence cada una. Y recién entonces cae.

Kira desenvaina la espada. Nova se pone a su lado. {mentor} habla bajito, desde todas partes a la vez: —Yo no adivino. Pero confío en lo que me enseñaste.

### Objetivos

Vencer al jefe final del curso: un **programa grande hecho de piezas chicas**. Cada parte del dragón se vence
con una herramienta distinta del curso: bits, arreglos de words con números grandes, la pila y, al final, el
combate completo con una rutina nueva.

### Antes de empezar

Todo el curso.

### Explicación

#### Dividir y vencer
El dragón tiene cuatro partes, y cada una pide algo distinto:

| Parte | Herramienta |
|---|---|
| Las escamas | bits: `shl` y `jnc`, contar los que están prendidos |
| El tesoro | un arreglo de words, `add si, 2` e `imprimir_numero` |
| El acertijo | la `0Ah`, la pila y una comparación letra por letra |
| El combate | una rutina nueva (`turno_dragon`) en el bucle de juego que ya armaste |

Esa es la forma de encarar **cualquier** programa grande, en cualquier lenguaje: partirlo en piezas que se puedan
escribir y probar solas, y después unirlas.

> **Puente con otras lenguas.** «Divide y vencerás» es un principio de diseño de todos los lenguajes: funciones
> chicas, módulos, clases. Y ahora sabés qué hay debajo de cada una de esas piezas: palancas, cajones, saltos y una
> torre de platos.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
escamas db 10110110b
t_esc   db 'Las escamas en binario: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_esc
    mov ah, 09h
    int 21h
    mov bl, escamas
    mov cx, 8
bits:
    shl bl, 1
    mov dl, '0'
    jnc cero
    mov dl, '1'
cero:
    mov ah, 02h
    int 21h
    loop bits

fin:
    mov ax, 4C00h
    int 21h
main endp

end main
```

### Salida esperada

```
Las escamas en binario: 10110110
```

### ¿Para qué sirve?

Este es el último paso del curso, y el más importante: ya no se trata de una orden nueva, sino de **combinar** todo
lo que sabés para resolver algo grande. Es lo que hace un programador todos los días, en cualquier lenguaje.

### Errores habituales

Todos los del bestiario pueden aparecer: el **slime** de la coma, el **goblin** del tamaño, el **esqueleto** del
nombre mal escrito, el **orco** que se sale del arreglo, el **ogro** de la lógica y el **troll** de la pila. El
método es siempre el mismo: leer el error (o ejecutar paso a paso), arreglar una cosa por vez y volver a probar.

### Micro-misión R04-N04-P1 · Las escamas encendidas

```meta
lugar: El núcleo del Gólem
personajes: Nova, Gheco
criatura: dragon
carta: Contar bits | 8 vueltas · shl bl, 1 · jnc: estaba en 0 · si no, contar uno más
```

#### Escena
La primera defensa del dragón son sus **escamas**: ocho, en fila, unas encendidas y otras apagadas. Para atravesarlas, Nova tiene que saber cuántas están **encendidas**.

#### Gheco sugiere
Las escamas son los 8 bits de un byte. Un bucle de 8 vueltas: `shl bl, 1` empuja cada bit a CF; si CF quedó en 1 (no salta el `jnc`), sumá uno al contador. Al final, mostrá el contador con `+ '0'`.

#### Desafío
Escribí las órdenes desde cero, donde dice `; tus órdenes`.

#### Código inicial
```asm
.model small
.stack 100h
.data
escamas db 10110110b
t_esc   db 'Escamas encendidas: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_esc
    mov ah, 09h
    int 21h

    ; tus órdenes

fin:
    mov ax, 4C00h
    int 21h
main endp

end main
```

#### Salida esperada
```
Escamas encendidas: 5
```

#### Solución
```asm
.model small
.stack 100h
.data
escamas db 10110110b
t_esc   db 'Escamas encendidas: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_esc
    mov ah, 09h
    int 21h

    mov bl, escamas
    mov bh, 0            ; el contador
    mov cx, 8
contar:
    shl bl, 1
    jnc apagada
    inc bh
apagada:
    loop contar
    mov dl, bh
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
Cinco escamas encendidas. Nova las apaga una por una, con cinco toques de luz. El dragón ruge: la primera defensa cayó.

#### Imagen
- Un dragón enorme de luz roja enroscado alrededor de un corazón de bronce gigante, con ocho escamas grandes en el lomo, unas brillando y otras apagadas.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) toca una escama encendida con la mano, que se apaga con una chispa cian.
- Gheco (gecko de luz cian con antiparras, chiquito) cuenta las escamas apagadas con la cola.

### Micro-misión R04-N04-P2 · El tesoro del dragón

```meta
lugar: El núcleo del Gólem
personajes: Nova, Gheco, Kira
criatura: dragon
carta: Arreglo de words | lea si · add ax, [si] · add si, 2 · imprimir_numero para números grandes
```

#### Escena
Debajo del dragón brilla su **tesoro**: cinco montañas de monedas. El dragón se alimenta de él. Si Nova sabe cuánto hay exactamente, puede devolverlo a las Forjas y dejarlo sin fuerza.

#### Gheco sugiere
El tesoro es un arreglo de **words**: recorrelo con SI (`lea si, tesoro`), sumá cada uno en AX y avanzá de a **2** (`add si, 2`). Cinco vueltas. Al final, `imprimir_numero`, que ya está.

#### Desafío
Escribí la suma donde dice `; tus órdenes`.

#### Código inicial
```asm
.model small
.stack 100h
.data
tesoro dw 1200, 3400, 560, 7800, 90
t_tes  db 'Tesoro del dragon: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_tes
    mov ah, 09h
    int 21h

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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
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
Tesoro del dragon: 13050
```

#### Solución
```asm
.model small
.stack 100h
.data
tesoro dw 1200, 3400, 560, 7800, 90
t_tes  db 'Tesoro del dragon: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_tes
    mov ah, 09h
    int 21h

    mov ax, 0
    lea si, tesoro
    mov cx, 5
sumar:
    add ax, [si]
    add si, 2
    loop sumar
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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

end main
```

#### Al superarla
13.050 monedas. Kira silba. Las montañas de oro empiezan a flotar hacia arriba, de vuelta a las Forjas, y el dragón se encoge un poco, furioso.

#### Imagen
- Montañas de monedas doradas flotando hacia arriba por un túnel de bronce, dejando un rastro de luz.
- Un dragón de luz roja más chico, enroscado y furioso.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) mira las monedas subir, boquiabierta.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) guía las monedas con las manos.
- Gheco (gecko de luz cian con antiparras, chiquito) se aferra a una moneda que sube.

### Micro-misión R04-N04-P3 · El acertijo

```meta
lugar: El núcleo del Gólem
personajes: Nova, Gheco, Kira
criatura: dragon
carta: Palíndromo | 0Ah · apilar las letras · desapilar comparando con la palabra · todas iguales: se lee igual al revés
```

#### Escena
El dragón, acorralado, habla por primera vez. —Te hago un acertijo —sisea—. Decime una palabra que se lea **igual al derecho y al revés**, y demostrá que lo es.

Kira escribe **RECONOCER**.

#### Gheco sugiere
La palabra ya está en la bolsa de la `0Ah`. Guardá la cantidad (`buffer+1`) en otra palanca y apilá las letras desde `buffer+2`. Después recorré la palabra de nuevo desde el principio, desapilando: cada letra que sale de la torre (la del final) se compara con la del principio. Si alguna es distinta, no es palíndromo.

#### Desafío
Escribí la comprobación donde dice `; tus órdenes`.

#### Código inicial
```asm
.model small
.stack 100h
.data
buffer db 21, ?, 21 dup(?)
t_pide db 'El acertijo: $'
t_si   db 'Se lee igual al reves. El dragon calla.$'
t_no   db 'No se lee igual al reves. El dragon se rie.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_pide
    mov ah, 09h
    int 21h
    mov ah, 0Ah
    lea dx, buffer
    int 21h
    mov dl, 13
    mov ah, 02h
    int 21h
    mov dl, 10
    int 21h

    ; tus órdenes

fin:
    mov ax, 4C00h
    int 21h
main endp

end main
```

#### Entrada
```
RECONOCER
```

#### Salida esperada
```
El acertijo: RECONOCER
Se lee igual al reves. El dragon calla.
```

#### Solución
```asm
.model small
.stack 100h
.data
buffer db 21, ?, 21 dup(?)
t_pide db 'El acertijo: $'
t_si   db 'Se lee igual al reves. El dragon calla.$'
t_no   db 'No se lee igual al reves. El dragon se rie.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_pide
    mov ah, 09h
    int 21h
    mov ah, 0Ah
    lea dx, buffer
    int 21h
    mov dl, 13
    mov ah, 02h
    int 21h
    mov dl, 10
    int 21h

    mov cl, buffer+1
    mov ch, 0
    mov bx, cx           ; la cantidad, a salvo
    lea si, buffer+2
apilar:
    mov al, [si]
    push ax
    inc si
    loop apilar

    mov cx, bx
    lea si, buffer+2
    mov bl, 1            ; 1 = por ahora se lee igual
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

#### Al superarla
—Reconocer —repite el dragón, despacio. Y por un momento parece que entiende algo. Su luz roja tiembla. Ya no le quedan defensas: solo pelear.

#### Imagen
- Un dragón de luz roja acorralado contra el corazón de bronce de un gólem, con la cabeza baja, pensativo.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) lo enfrenta con la espada baja, serena.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) sostiene en el aire una fila de nueve lucecitas cian simétricas.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre el hombro de Kira.

### Micro-misión R04-N04-P4 · El último combate

```meta
lugar: El núcleo del Gólem
personajes: Nova, Gheco, Kira, Axón
criatura: dragon
carta: Una pieza nueva | ronda múltiplo de 3: aliento de fuego (8) · si no: garra (azar 2 a 7) · con escudo: shr · bajar el escudo
```

#### Escena
El combate final. Todo el motor del juego está listo, el mismo del Autómata de Hierro. Falta lo único nuevo: cómo ataca **el dragón**. Cada **tres** rondas lanza su **aliento de fuego** (8 de daño, siempre); las demás, un zarpazo de 2 a 7. Y si Kira se defiende, el golpe vale la mitad.

#### Gheco sugiere
En `turno_dragon`, donde dice `; tus órdenes`: dividí `ronda` por 3 (AX = ronda, BL = 3, `div bl`); si el resto (AH) es 0, CL = 8 y el mensaje del fuego. Si no, la garra: `azar` con BL = 6, más 2. Después, si `defiende` no es 0, `shr cl, 1` y bajá el escudo (`defiende` en 0). Lo que sigue (mostrar el daño y quitar la vida) ya está.

#### Desafío
Escribí el ataque del dragón. Kira va a jugar 1, 1, 2, 1, 3, 2, 1 y 1: se defiende justo en las rondas del fuego.

#### Código inicial
```asm
.model small
.stack 100h
.data
semilla  dw 35
vida_k   db 30
vida_o   db 50
pociones db 3
defiende db 0
accion   db ?
ronda    dw 0
t_titulo db ' NOVA Y KIRA CONTRA EL DRAGON DEL GOLEM$'
t_ronda  db 13, 10, '--- Ronda $'
t_rfin   db ' ---', 13, 10, '$'
t_kira   db 'Kira   $'
t_auto   db 'Dragon $'
t_menu   db '1) Atacar  2) Defender  3) Pocion: $'
t_ataca  db 'Kira ataca: $'
t_crit   db 'CRITICO! $'
t_danio  db ' de danio.', 13, 10, '$'
t_defi   db 'Kira levanta el escudo.', 13, 10, '$'
t_pocion db 'Kira bebe una pocion: +10 de vida.', 13, 10, '$'
t_sinpoc db 'No quedan pociones: Kira pierde el turno.', 13, 10, '$'
t_golpe  db 'El dragon ataca: $'
t_fuego  db 'ALIENTO DE FUEGO! $'
t_gana   db 13, 10, 'El dragon se apaga. GANARON NOVA Y KIRA!$'
t_pierde db 13, 10, 'Kira cae. El dragon sigue despierto.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_titulo
    call mostrar_cadena
ronda_nueva:
    inc ronda
    lea dx, t_ronda
    call mostrar_cadena
    mov ax, ronda
    call imprimir_numero
    lea dx, t_rfin
    call mostrar_cadena
    call mostrar_estado
    call turno_kira
    cmp vida_o, 0
    je  gana
    call turno_dragon
    cmp vida_k, 0
    je  pierde
    jmp ronda_nueva
gana:
    lea dx, t_gana
    call mostrar_cadena
    jmp termino
pierde:
    lea dx, t_pierde
    call mostrar_cadena
termino:

fin:
    mov ax, 4C00h
    int 21h
main endp

; turno_kira: menú, acción
turno_kira proc
    push dx
    lea dx, t_menu
    call mostrar_cadena
    call leer_accion
    cmp accion, '1'
    jne no_ataca
    call atacar
    jmp turno_fin
no_ataca:
    cmp accion, '2'
    jne no_defiende
    mov defiende, 1
    lea dx, t_defi
    call mostrar_cadena
    jmp turno_fin
no_defiende:
    call pocion
turno_fin:
    pop dx
    ret
turno_kira endp

; atacar: daño de 3 a 8; 1 de cada 6 es crítico (daño x 2)
atacar proc
    push ax
    push bx
    push cx
    push dx
    lea dx, t_ataca
    call mostrar_cadena
    mov bl, 6
    call azar
    mov cl, al
    add cl, 3
    mov bl, 6
    call azar
    cmp al, 0
    jne sin_critico
    shl cl, 1
    lea dx, t_crit
    call mostrar_cadena
sin_critico:
    mov al, cl
    mov ah, 0
    call imprimir_numero
    lea dx, t_danio
    call mostrar_cadena
    lea si, vida_o
    call quitar_vida
    pop dx
    pop cx
    pop bx
    pop ax
    ret
atacar endp

; turno_dragon: cada 3 rondas, aliento de fuego (8 fijo); si no, garra de 2 a 7; con escudo, la mitad
turno_dragon proc
    push ax
    push bx
    push cx
    push dx
    lea dx, t_golpe
    call mostrar_cadena
    ; tus órdenes (el daño queda en CL)
sin_escudo:
    mov al, cl
    mov ah, 0
    call imprimir_numero
    lea dx, t_danio
    call mostrar_cadena
    lea si, vida_k
    call quitar_vida
    pop dx
    pop cx
    pop bx
    pop ax
    ret
turno_dragon endp

; pocion: +10 de vida (tope 30) si quedan pociones; si no, pierde el turno
pocion proc
    push ax
    push dx
    cmp pociones, 0
    je  sin_pociones
    dec pociones
    add vida_k, 10
    cmp vida_k, 30
    jbe pocion_ok
    mov vida_k, 30
pocion_ok:
    lea dx, t_pocion
    call mostrar_cadena
    jmp pocion_fin
sin_pociones:
    lea dx, t_sinpoc
    call mostrar_cadena
pocion_fin:
    pop dx
    pop ax
    ret
pocion endp

; leer_accion: espera una tecla sin eco hasta que sea '1', '2' o '3'; la muestra y la guarda en accion
leer_accion proc
    push ax
    push dx
otra_tecla:
    mov ah, 07h
    int 21h
    cmp al, '1'
    jb  otra_tecla
    cmp al, '3'
    ja  otra_tecla
    mov accion, al
    mov dl, al
    mov ah, 02h
    int 21h
    call nueva_linea
    pop dx
    pop ax
    ret
leer_accion endp

; mostrar_estado: las dos barras con sus números
mostrar_estado proc
    push ax
    push bx
    push dx
    lea dx, t_kira
    call mostrar_cadena
    mov al, vida_k
    mov bl, 30
    call barra
    call espacio
    mov ah, 0
    call imprimir_numero
    call nueva_linea
    lea dx, t_auto
    call mostrar_cadena
    mov al, vida_o
    mov bl, 50
    call barra
    call espacio
    mov ah, 0
    call imprimir_numero
    call nueva_linea
    pop dx
    pop bx
    pop ax
    ret
mostrar_estado endp

; barra: AL = vida, BL = máximo; un casillero cada 2 puntos (# lleno, . vacío)
barra proc
    push ax
    push bx
    push cx
    push dx
    shr al, 1
    shr bl, 1
    sub bl, al
    mov cl, al
    mov ch, 0
    mov dl, '#'
    mov ah, 02h
    jcxz sin_llenos
llenos:
    int 21h
    loop llenos
sin_llenos:
    mov cl, bl
    mov dl, '.'
    jcxz sin_vacios
vacios:
    int 21h
    loop vacios
sin_vacios:
    pop dx
    pop cx
    pop bx
    pop ax
    ret
barra endp

; quitar_vida: SI = dirección de la vida, CL = daño (la vida no baja de 0)
quitar_vida proc
    cmp cl, [si]
    jae queda_cero
    sub [si], cl
    ret
queda_cero:
    mov byte ptr [si], 0
    ret
quitar_vida endp

; azar: AL = número de 0 a BL-1 (avanza la semilla)
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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Entrada
```
1
1
2
1
3
2
1
1
```

#### Salida esperada
```
 NOVA Y KIRA CONTRA EL DRAGON DEL GOLEM
--- Ronda 1 ---
Kira   ############### 30
Dragon ######################### 50
1) Atacar  2) Defender  3) Pocion: 1
Kira ataca: 8 de danio.
El dragon ataca: 2 de danio.

--- Ronda 2 ---
Kira   ##############. 28
Dragon #####################.... 42
1) Atacar  2) Defender  3) Pocion: 1
Kira ataca: 4 de danio.
El dragon ataca: 4 de danio.

--- Ronda 3 ---
Kira   ############... 24
Dragon ###################...... 38
1) Atacar  2) Defender  3) Pocion: 2
Kira levanta el escudo.
El dragon ataca: ALIENTO DE FUEGO! 4 de danio.

--- Ronda 4 ---
Kira   ##########..... 20
Dragon ###################...... 38
1) Atacar  2) Defender  3) Pocion: 1
Kira ataca: CRITICO! 14 de danio.
El dragon ataca: 2 de danio.

--- Ronda 5 ---
Kira   #########...... 18
Dragon ############............. 24
1) Atacar  2) Defender  3) Pocion: 3
Kira bebe una pocion: +10 de vida.
El dragon ataca: 2 de danio.

--- Ronda 6 ---
Kira   #############.. 26
Dragon ############............. 24
1) Atacar  2) Defender  3) Pocion: 2
Kira levanta el escudo.
El dragon ataca: ALIENTO DE FUEGO! 4 de danio.

--- Ronda 7 ---
Kira   ###########.... 22
Dragon ############............. 24
1) Atacar  2) Defender  3) Pocion: 1
Kira ataca: CRITICO! 16 de danio.
El dragon ataca: 2 de danio.

--- Ronda 8 ---
Kira   ##########..... 20
Dragon ####..................... 8
1) Atacar  2) Defender  3) Pocion: 1
Kira ataca: 8 de danio.

El dragon se apaga. GANARON NOVA Y KIRA!
```

#### Solución
```asm
.model small
.stack 100h
.data
semilla  dw 35
vida_k   db 30
vida_o   db 50
pociones db 3
defiende db 0
accion   db ?
ronda    dw 0
t_titulo db ' NOVA Y KIRA CONTRA EL DRAGON DEL GOLEM$'
t_ronda  db 13, 10, '--- Ronda $'
t_rfin   db ' ---', 13, 10, '$'
t_kira   db 'Kira   $'
t_auto   db 'Dragon $'
t_menu   db '1) Atacar  2) Defender  3) Pocion: $'
t_ataca  db 'Kira ataca: $'
t_crit   db 'CRITICO! $'
t_danio  db ' de danio.', 13, 10, '$'
t_defi   db 'Kira levanta el escudo.', 13, 10, '$'
t_pocion db 'Kira bebe una pocion: +10 de vida.', 13, 10, '$'
t_sinpoc db 'No quedan pociones: Kira pierde el turno.', 13, 10, '$'
t_golpe  db 'El dragon ataca: $'
t_fuego  db 'ALIENTO DE FUEGO! $'
t_gana   db 13, 10, 'El dragon se apaga. GANARON NOVA Y KIRA!$'
t_pierde db 13, 10, 'Kira cae. El dragon sigue despierto.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_titulo
    call mostrar_cadena
ronda_nueva:
    inc ronda
    lea dx, t_ronda
    call mostrar_cadena
    mov ax, ronda
    call imprimir_numero
    lea dx, t_rfin
    call mostrar_cadena
    call mostrar_estado
    call turno_kira
    cmp vida_o, 0
    je  gana
    call turno_dragon
    cmp vida_k, 0
    je  pierde
    jmp ronda_nueva
gana:
    lea dx, t_gana
    call mostrar_cadena
    jmp termino
pierde:
    lea dx, t_pierde
    call mostrar_cadena
termino:

fin:
    mov ax, 4C00h
    int 21h
main endp

; turno_kira: menú, acción
turno_kira proc
    push dx
    lea dx, t_menu
    call mostrar_cadena
    call leer_accion
    cmp accion, '1'
    jne no_ataca
    call atacar
    jmp turno_fin
no_ataca:
    cmp accion, '2'
    jne no_defiende
    mov defiende, 1
    lea dx, t_defi
    call mostrar_cadena
    jmp turno_fin
no_defiende:
    call pocion
turno_fin:
    pop dx
    ret
turno_kira endp

; atacar: daño de 3 a 8; 1 de cada 6 es crítico (daño x 2)
atacar proc
    push ax
    push bx
    push cx
    push dx
    lea dx, t_ataca
    call mostrar_cadena
    mov bl, 6
    call azar
    mov cl, al
    add cl, 3
    mov bl, 6
    call azar
    cmp al, 0
    jne sin_critico
    shl cl, 1
    lea dx, t_crit
    call mostrar_cadena
sin_critico:
    mov al, cl
    mov ah, 0
    call imprimir_numero
    lea dx, t_danio
    call mostrar_cadena
    lea si, vida_o
    call quitar_vida
    pop dx
    pop cx
    pop bx
    pop ax
    ret
atacar endp

; turno_dragon: cada 3 rondas, aliento de fuego (8 fijo); si no, garra de 2 a 7; con escudo, la mitad
turno_dragon proc
    push ax
    push bx
    push cx
    push dx
    lea dx, t_golpe
    call mostrar_cadena
    mov ax, ronda
    mov bl, 3
    div bl
    cmp ah, 0
    jne garra
    mov cl, 8
    lea dx, t_fuego
    call mostrar_cadena
    jmp con_escudo
garra:
    mov bl, 6
    call azar
    mov cl, al
    add cl, 2
con_escudo:
    cmp defiende, 0
    je  sin_escudo
    shr cl, 1
    mov defiende, 0
sin_escudo:
    mov al, cl
    mov ah, 0
    call imprimir_numero
    lea dx, t_danio
    call mostrar_cadena
    lea si, vida_k
    call quitar_vida
    pop dx
    pop cx
    pop bx
    pop ax
    ret
turno_dragon endp

; pocion: +10 de vida (tope 30) si quedan pociones; si no, pierde el turno
pocion proc
    push ax
    push dx
    cmp pociones, 0
    je  sin_pociones
    dec pociones
    add vida_k, 10
    cmp vida_k, 30
    jbe pocion_ok
    mov vida_k, 30
pocion_ok:
    lea dx, t_pocion
    call mostrar_cadena
    jmp pocion_fin
sin_pociones:
    lea dx, t_sinpoc
    call mostrar_cadena
pocion_fin:
    pop dx
    pop ax
    ret
pocion endp

; leer_accion: espera una tecla sin eco hasta que sea '1', '2' o '3'; la muestra y la guarda en accion
leer_accion proc
    push ax
    push dx
otra_tecla:
    mov ah, 07h
    int 21h
    cmp al, '1'
    jb  otra_tecla
    cmp al, '3'
    ja  otra_tecla
    mov accion, al
    mov dl, al
    mov ah, 02h
    int 21h
    call nueva_linea
    pop dx
    pop ax
    ret
leer_accion endp

; mostrar_estado: las dos barras con sus números
mostrar_estado proc
    push ax
    push bx
    push dx
    lea dx, t_kira
    call mostrar_cadena
    mov al, vida_k
    mov bl, 30
    call barra
    call espacio
    mov ah, 0
    call imprimir_numero
    call nueva_linea
    lea dx, t_auto
    call mostrar_cadena
    mov al, vida_o
    mov bl, 50
    call barra
    call espacio
    mov ah, 0
    call imprimir_numero
    call nueva_linea
    pop dx
    pop bx
    pop ax
    ret
mostrar_estado endp

; barra: AL = vida, BL = máximo; un casillero cada 2 puntos (# lleno, . vacío)
barra proc
    push ax
    push bx
    push cx
    push dx
    shr al, 1
    shr bl, 1
    sub bl, al
    mov cl, al
    mov ch, 0
    mov dl, '#'
    mov ah, 02h
    jcxz sin_llenos
llenos:
    int 21h
    loop llenos
sin_llenos:
    mov cl, bl
    mov dl, '.'
    jcxz sin_vacios
vacios:
    int 21h
    loop vacios
sin_vacios:
    pop dx
    pop cx
    pop bx
    pop ax
    ret
barra endp

; quitar_vida: SI = dirección de la vida, CL = daño (la vida no baja de 0)
quitar_vida proc
    cmp cl, [si]
    jae queda_cero
    sub [si], cl
    ret
queda_cero:
    mov byte ptr [si], 0
    ret
quitar_vida endp

; azar: AL = número de 0 a BL-1 (avanza la semilla)
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
mostrar_cifra:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop mostrar_cifra
    pop dx
    pop cx
    pop bx
    pop ax
    ret
imprimir_numero endp

nueva_linea proc
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
nueva_linea endp

; mostrar_cadena: muestra el texto que señala DX
mostrar_cadena proc
    push ax
    mov ah, 09h
    int 21h
    pop ax
    ret
mostrar_cadena endp

end main
```

#### Al superarla
**GANARON NOVA Y KIRA.** El dragón no muere: se **apaga**, como una brasa al amanecer, y su luz roja se vuelve cian y se mezcla con la de Nova. Las órdenes sin terminar de las que estaba hecho, por fin, quedaron completas.

El núcleo se ilumina entero. {mentor} se endereza, levanta la cabeza y **camina**: un paso, otro, otro, por la caverna, por el pasillo de las compuertas, hasta la salida de las Forjas. Afuera es de día. Los enanos del Gremio, la tabernera, el Ogro de las Banderas y hasta el Troll de la Pila se asoman a mirarlo pasar.

—Yo no adivino —dice el Gólem, con el sol en el ojo—. Hice exactamente lo que ella me enseñó.

Y Nova descubre algo más: ahora que conoce cada palanca, cada cajón y cada plato de su cuerpo, siente que podría **encender otros**. Cuerpos mucho más chicos. Miles de cuerpos chiquitos.

Pero esa es otra historia.

#### Imagen
- Un gólem de bronce gigante saliendo de una caverna a la luz del día, caminando, con el ojo encendido de cian y el pecho brillando.
- Abajo, una multitud de enanos, un ogro enorme y un troll gris lo miran pasar, algunos aplaudiendo.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) camina al lado del pie del gólem, con la espada envainada.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) flota sobre el hombro del gólem, con los brazos abiertos al sol, y alrededor de sus manos giran cientos de lucecitas cian diminutas.
- Gheco (gecko de luz cian con antiparras, chiquito) en la cabeza del gólem, con las antiparras levantadas, mirando el sol por primera vez.

### Prueba del sello

#### ¿Cómo se cuenta cuántos bits están prendidos en un byte?
Con 8 vueltas de `shl` y `jnc`: cada vez que el bit que cae en CF es 1, se cuenta uno.

#### ¿Por qué el tesoro necesita `imprimir_numero` y no el truco de las dos cifras?
Porque la suma pasa de 99: hace falta una rutina que muestre cualquier número de 16 bits.

#### ¿Cómo ayuda la pila a saber si una palabra es palíndromo?
Las letras salen de la pila al revés: se comparan con la palabra al derecho.

#### ¿Qué hay que hacer para escribir un programa grande?
Partirlo en piezas chicas que se puedan escribir y probar solas, y después unirlas.
