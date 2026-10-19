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
