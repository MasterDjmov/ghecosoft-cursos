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
