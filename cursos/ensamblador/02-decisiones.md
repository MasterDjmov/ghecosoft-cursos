# RAMA R02 · Decisiones y repeticiones: las compuertas del Gólem

```meta
tipo: tronco
posicion: 2
```

## R02-N01 · Las compuertas: comparar y saltar

```meta
tipo: tema
criatura: skeleton
padre: R01-N06
precio: 0
temas: maq.saltos, maq.banderas, prog.condicionales
```

### Crónica

Con el brazo libre, {mentor} quiere bajar a ver sus piernas. Nova se desliza por un tubo de bronce hasta las rodillas del Gólem y encuentra un pasillo lleno de **compuertas** cerradas, una detrás de otra.

—Hasta ahora hice todo en orden, de arriba abajo —dice Nova—. ¿Cómo hago para **elegir** un camino?

—Yo no elijo —contesta el Gólem—. Pero puedo **mirar un interruptor** y, según cómo esté, seguir derecho o **saltar** a otra parte.

### Objetivos

Marcar lugares del programa con **etiquetas**, saltar siempre con `jmp`, comparar con `cmp` (que solo prende
interruptores) y saltar **según cómo salió** la comparación con `je` y `jne`: el `if` de todas las lenguas.

### Antes de empezar

- Las banderas ZF, SF y CF (Las cuentas del Gólem).
- Leer una tecla con la `01h` y la `07h` (La boca de bronce).

### Explicación

#### Etiquetas y `jmp`
Una **etiqueta** es un nombre seguido de dos puntos que marca un lugar del programa (como `fin:`, que ya
conocés). `jmp etiqueta` **salta siempre** ahí: el Gólem deja de seguir en orden y continúa desde la etiqueta.
```asm
    mov bl, 1
    jmp listo        ; salta por encima de la orden siguiente
    mov bl, 9        ; esta nunca se ejecuta
listo:
```

#### `cmp`: comparar sin cambiar nada
`cmp a, b` hace la resta `a − b` **sin guardar el resultado**: solo prende o apaga los interruptores. Si `a` y `b`
son iguales, la resta da 0 y se prende **ZF**.
```asm
mov al, 7
cmp al, 7        ; AL sigue valiendo 7; ZF = 1
```

#### Saltar según el interruptor
| Salto | Salta si… | Mira |
|---|---|---|
| `je etiqueta` (*jump if equal*) | eran iguales | ZF = 1 |
| `jne etiqueta` (*jump if not equal*) | eran distintos | ZF = 0 |

Si la condición **no** se cumple, el Gólem sigue con la orden de abajo, como si el salto no estuviera.

#### El `if` por dentro
```asm
    cmp al, 's'
    je  abrir            ; if (al == 's') goto abrir
    lea dx, t_no         ; si no: el mensaje de "no"
    jmp mostrar          ; y saltar por encima del otro camino
abrir:
    lea dx, t_si         ; el mensaje de "sí"
mostrar:                 ; los dos caminos se juntan acá
    mov ah, 09h
    int 21h
```

> **Puente con otras lenguas.** Esto es exactamente lo que hacen el `if` de Python y el `if (…) { } else { }` de
> C y Java: un `cmp` y un salto. Cada `if` que escribiste en tu vida, el procesador lo ejecutó así.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
pide db 'Abro la compuerta? (s/n) $'
t_si db 13, 10, 'Se abre la compuerta.$'
t_no db 13, 10, 'Sigue cerrada.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h

    cmp al, 's'
    je  abrir
    lea dx, t_no
    jmp mostrar
abrir:
    lea dx, t_si
mostrar:
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

### Entrada de ejemplo

```
s
```

### Salida esperada

```
Abro la compuerta? (s/n) s
Se abre la compuerta.
```

### ¿Para qué sirve?

Sin saltos, un programa hace siempre lo mismo. Con un `cmp` y un salto ya puede **decidir**: responder distinto
según lo que tipea una persona, frenar si algo salió mal, elegir un camino. Todas las decisiones de todos los
programas, por debajo, son esto.

### Errores habituales

**Esqueleto: la etiqueta que no existe.** `jmp abirr` (con la etiqueta escrita `abrir:`):
```
main.asm(17) : Error A2102: Symbol not defined : abirr
```

**Slime: la etiqueta repetida.** Cada etiqueta existe una sola vez:
```
main.asm(20) : Error A2056: Symbol already defined: mostrar
```
Usá nombres distintos: `mostrar2`, `fin_menu`…

**Ogro: el salto al revés.** `je` donde iba `jne`: el programa corre, pero hace lo contrario.

**Ogro: las banderas pisadas.** Entre el `cmp` y el salto hay un `add`, `sub`, `inc` o `dec`: los interruptores ya
son otros. (`mov` y `lea` no los tocan.)

### Micro-misión R02-N01-P1 · La primera comparación

```meta
lugar: Las compuertas
personajes: Nova, Gheco
carta: cmp | cmp a, b = resta a - b sin guardar · solo cambia los interruptores · iguales: ZF = 1
recompensa: xp 10, oro 10
```

#### Escena
La primera compuerta tiene una cerradura con un número grabado: el **7**. Nova tiene un 7 en AL. —¿Cómo le pregunto al Gólem si son iguales?

#### Gheco sugiere
`cmp al, 7` resta 7 a AL **sin cambiar AL**: solo prende los interruptores. Si son iguales, la resta da 0 y se prende **ZF**.

#### Desafío
Completá la comparación para que se prenda **ZF**, y fijate que AL siga valiendo 7.

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
    cmp al, ___

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
AL = 7
ZF = 1
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
    cmp al, 7

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Clic: la luz de ZF se enciende sobre la cerradura. La compuerta no se abre todavía, pero ahora **sabe** que el número es el correcto.

#### Imagen
- Una compuerta redonda de bronce con una cerradura en el centro grabada con siete puntitos.
- Una lucecita cian encendida sobre la cerradura.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) acerca a la cerradura una llave de luz con siete puntitos iguales.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre su hombro, mirando la lucecita.

### Micro-misión R02-N01-P2 · El salto que siempre salta

```meta
lugar: Las compuertas
personajes: Nova, Gheco
carta: jmp | jmp etiqueta = seguí desde ahí, siempre · etiqueta: nombre con dos puntos
recompensa: xp 10, oro 10
```

#### Escena
Detrás de la primera compuerta hay una trampa: una orden que pone un **9** en BL. Nova la quiere esquivar entera, sin borrarla.

#### Gheco sugiere
`jmp listo` salta **siempre** a la etiqueta `listo:`, y lo que queda en el medio no se ejecuta.

#### Desafío
Completá el salto para que el Gólem pase por encima de la trampa y BL se quede en **1**.

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
    jmp ___
    mov bl, 9        ; la trampa
listo:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
BL = 1
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
    jmp listo
    mov bl, 9        ; la trampa
listo:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Nova pasa por arriba de la trampa de un salto. Ejecutá **paso a paso**: la flechita de la línea actual también salta, y la orden del medio queda sin tocar.

#### Imagen
- Un pasillo de bronce con una trampa de pinchos en el piso, a medio camino.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) salta por encima de la trampa dejando una estela de luz cian en arco.
- Gheco (gecko de luz cian con antiparras, chiquito) la espera del otro lado, aplaudiendo.

### Micro-misión R02-N01-P3 · El esqueleto de la etiqueta

```meta
lugar: Las compuertas
personajes: Nova, Gheco
criatura: skeleton
carta: Symbol not defined | el salto y la etiqueta tienen que llamarse igual, letra por letra
recompensa: xp 15, oro 15
```

#### Escena
Nova escribe un salto a toda velocidad y aparece un **esqueleto**: *«Symbol not defined»*. El Gólem busca un lugar que no existe.

#### Gheco sugiere
Leé el error: dice la línea y el nombre que no encuentra. Comparalo letra por letra con la etiqueta que sí existe.

#### Desafío
Tocá **Ejecutar**, leé el error y arreglá el nombre para que el ojo diga `Compuerta abierta`.

#### Código inicial
```asm
.model small
.stack 100h
.data
t_cerrada db 'Cerrada$'
t_abierta db 'Compuerta abierta$'
.code
main proc
    mov ax, @data
    mov ds, ax

    jmp abirr
    lea dx, t_cerrada
    jmp mostrar
abrir:
    lea dx, t_abierta
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
Compuerta abierta
```

#### Solución
```asm
.model small
.stack 100h
.data
t_cerrada db 'Cerrada$'
t_abierta db 'Compuerta abierta$'
.code
main proc
    mov ax, @data
    mov ds, ax

    jmp abrir
    lea dx, t_cerrada
    jmp mostrar
abrir:
    lea dx, t_abierta
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
El esqueleto se desarma: era un nombre sin cuerpo. La compuerta se abre con un siseo de vapor.

#### Imagen
- Un esqueleto flaco desarmándose delante de una compuerta redonda de bronce que se abre echando vapor.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) sostiene un cartel liso con un dibujito de flecha.
- Gheco (gecko de luz cian con antiparras, chiquito) se asoma por la compuerta abierta.

### Micro-misión R02-N01-P4 · Si dice que sí

```meta
lugar: Las compuertas
personajes: Nova, Gheco, Kira
carta: je | cmp + je = si son iguales, saltá · si no, seguí de largo
recompensa: xp 15, oro 15
```

#### Escena
Kira llega a la segunda compuerta y {mentor} le pregunta si quiere pasar. Si aprieta la **s**, la compuerta tiene que abrirse; con cualquier otra tecla, no.

#### Gheco sugiere
Compará la tecla con `'s'` y, si son iguales (`je`), saltá a `abrir`, donde BL se pone en 1. Si no, el Gólem sigue de largo y BL queda en 0.

#### Desafío
Completá la comparación y el salto para que, con la `s`, BL termine en **1**.

#### Código inicial
```asm
.model small
.stack 100h
.data
pide db 'Pasas? (s/n) $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h

    mov bl, 0
    cmp al, ___
    je  ___
    jmp listo
abrir:
    mov bl, 1
listo:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Entrada
```
s
```

#### Salida esperada
```
Pasas? (s/n) s
```

#### Estado esperado
```
BL = 1
```

#### Solución
```asm
.model small
.stack 100h
.data
pide db 'Pasas? (s/n) $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h

    mov bl, 0
    cmp al, 's'
    je  abrir
    jmp listo
abrir:
    mov bl, 1
listo:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
La compuerta se abre y Kira pasa. —El Gólem no decidió nada —dice Gheco—. Miró un interruptor y saltó. Vos decidiste **qué** mirar.

#### Imagen
- Una compuerta de bronce abierta a la mitad, con luz ámbar saliendo por la rendija.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) pasa agachándose por la rendija.
- Gheco (gecko de luz cian con antiparras, chiquito) sostiene la compuerta desde arriba, exagerando el esfuerzo.

### Micro-misión R02-N01-P5 · La runa equivocada

```meta
lugar: Las compuertas
personajes: Nova, Gheco, Kira
carta: jne | cmp + jne = si son distintos, saltá · los caminos se juntan en una etiqueta
recompensa: xp 20, oro 20
```

#### Escena
La última compuerta del pasillo pide una runa secreta: la **R**. Si la runa es otra, el ojo tiene que avisar «Runa equivocada»; si es la R, dejar pasar a Nova.

#### Gheco sugiere
Compará con `'R'`. Con `jne equivocada` saltás al mensaje malo; si no saltó, cargá el bueno y hacé `jmp mostrar` para no pasar por el malo. En `mostrar:` los dos caminos se juntan y se muestra el que quedó en DX.

#### Desafío
Escribí las órdenes desde cero, donde dice `; tus órdenes`. Kira va a apretar la `R`.

#### Código inicial
```asm
.model small
.stack 100h
.data
pide db 'Runa: $'
bien db '*', 13, 10, 'Pasa, Nova.$'
mal  db '*', 13, 10, 'Runa equivocada.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 07h
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
R
```

#### Salida esperada
```
Runa: *
Pasa, Nova.
```

#### Solución
```asm
.model small
.stack 100h
.data
pide db 'Runa: $'
bien db '*', 13, 10, 'Pasa, Nova.$'
mal  db '*', 13, 10, 'Runa equivocada.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 07h
    int 21h

    cmp al, 'R'
    jne equivocada
    lea dx, bien
    jmp mostrar
equivocada:
    lea dx, mal
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
La última compuerta se abre y, del otro lado, Nova encuentra la **rodilla** del Gólem: una articulación enorme, quieta desde hace siglos. —Si aprendo a decidir bien —piensa—, voy a poder caminar.

#### Imagen
- La articulación de la rodilla de un gólem de bronce gigante, vista desde adentro: engranajes enormes quietos, cubiertos de polvo.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) apoya la mano en un engranaje, pensativa.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) ilumina los engranajes con una linterna.
- Gheco (gecko de luz cian con antiparras, chiquito) sopla el polvo de un diente del engranaje.

### Prueba del sello

#### ¿Qué hace `cmp al, 5`?
Resta 5 a AL sin guardar el resultado: solo cambia los interruptores (ZF = 1 si AL valía 5).

#### ¿Qué diferencia hay entre `jmp` y `je`?
`jmp` salta siempre; `je` salta solo si la última comparación dio igual (ZF = 1).

#### Si un salto condicional no se cumple, ¿qué hace el Gólem?
Sigue con la orden de abajo, como si el salto no estuviera.

#### ¿Para qué va el `jmp mostrar` al final de un camino?
Para saltar por encima del otro camino; si no, se ejecutan los dos.

## R02-N02 · Dos caminos: el if y el else

```meta
tipo: tema
criatura: ogre
padre: R02-N01
precio: 0
temas: prog.condicionales, maq.saltos
```

### Crónica

En la rodilla del Gólem hay dos engranajes: uno la dobla para **adelante**, el otro para **atrás**. —Tengo que elegir uno —dice Nova—, y **nunca** los dos a la vez, o me rompo la pierna.

Gheco se ríe nervioso. —Eso es un **if** y un **else**. Y el ogro que vive acá se alimenta de los que se olvidan de saltar al final del primero.

### Objetivos

Armar un **if/else** completo (un camino u otro, nunca los dos), usar los saltos de **mayor y menor** para
cantidades (`ja`, `jae`, `jb`, `jbe`), saltar con la **condición contraria** para ejecutar un bloque solo si algo
se cumple, y encadenar varios saltos después de un mismo `cmp`.

### Antes de empezar

- Etiquetas, `jmp`, `cmp`, `je` y `jne` (Las compuertas).
- `div` y el resto en AH (Las cuentas del Gólem).

### Explicación

#### Mayor y menor
| Salto | Salta si `a` es… | Como en C |
|---|---|---|
| `ja` (*above*) | mayor que `b` | `a > b` |
| `jae` | mayor o igual | `a >= b` |
| `jb` (*below*) | menor que `b` | `a < b` |
| `jbe` | menor o igual | `a <= b` |

Estos son para **cantidades y letras** (números sin signo). Para números que pueden ser negativos hay otros: los
vas a ver en un nodo que viene.

#### El if/else completo
```asm
    cmp pociones, 3
    ja  sobran           ; if (pociones > 3) goto sobran
    lea dx, t_faltan     ; else: el camino de abajo
    jmp listo            ; ¡saltar por encima del otro camino!
sobran:
    lea dx, t_sobran
listo:
```

#### Un bloque que se hace solo a veces: la condición contraria
Para «si la tecla es `x`, hacé esto», se salta **por encima** del bloque cuando **no** se cumple:
```asm
    cmp al, 'x'
    jne sigue            ; si NO es 'x', saltá el bloque
    mov bl, 1            ; el bloque del if
sigue:
```
Es la forma más corta del `if` sin `else`: el salto lleva la condición **al revés**.

#### Varios saltos después de un `cmp`
Los interruptores siguen igual hasta la próxima cuenta, así que después de un `cmp` se pueden poner varios saltos
seguidos: `ja gana` y enseguida `je empate`. Así se arma el **else if**.

> **Puente con otras lenguas.** `if … elif … else` de Python, `if … else if … else` de C y Java, o un `switch`:
> todos se traducen en una fila de comparaciones y saltos, y cada caso termina con un salto al final común.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
pide    db 'Un numero: $'
t_par   db 13, 10, 'Es par.$'
t_impar db 13, 10, 'Es impar.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h
    sub al, '0'

    mov ah, 0
    mov bl, 2
    div bl               ; AH = el resto de dividir por 2
    cmp ah, 0
    je  par
    lea dx, t_impar
    jmp mostrar
par:
    lea dx, t_par
mostrar:
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

### Entrada de ejemplo

```
7
```

### Salida esperada

```
Un numero: 7
Es impar.
```

### ¿Para qué sirve?

El if/else está en todos lados: un menú, un juego que decide quién gana, un formulario que valida lo que se
escribió. Saber que por debajo es «saltá por encima de lo que no va» ayuda a leer cualquier código, y explica por
qué en C un `if` sin llaves se «come» solo la primera línea.

### Errores habituales

**Ogro: se cayó por el borde.** Te olvidaste el `jmp` al final del primer camino: se ejecuta también el de
abajo, y salen los dos mensajes.

**Ogro: la condición al revés.** Un `je` donde iba `jne` (o `ja` donde iba `jbe`): el bloque se ejecuta justo
cuando no tenía que hacerlo.

**Ogro: uno de más o uno de menos.** `ja` donde iba `jae`: el caso del borde (el 3 justo) cae del lado
equivocado. Probá siempre el valor del borde.

**Ogro: las banderas pisadas.** Un `add` o `dec` entre el `cmp` y el salto cambia los interruptores.

### Micro-misión R02-N02-P1 · ¿Sobran o faltan?

```meta
lugar: La rodilla del Gólem
personajes: Nova, Gheco
carta: ja | cmp a, b + ja = si a es mayor que b, saltá · jb: menor · jae y jbe: con el igual
recompensa: xp 10, oro 10
```

#### Escena
Para mover la rodilla, el Gólem necesita **más de 3** pociones de aceite. Nova tiene 5 en el cajón. ¿Sobran o faltan?

#### Gheco sugiere
`cmp pociones, 3` y después `ja sobran`: si hay más de 3, salta. Si no, sigue de largo hasta el mensaje de «faltan» (que ya salta al final con `jmp`).

#### Desafío
Completá el salto para que, con 5 pociones, el ojo diga `Sobran pociones`.

#### Código inicial
```asm
.model small
.stack 100h
.data
pociones db 5
t_sobran db 'Sobran pociones$'
t_faltan db 'Faltan pociones$'
.code
main proc
    mov ax, @data
    mov ds, ax

    cmp pociones, 3
    ___ sobran
    lea dx, t_faltan
    jmp mostrar
sobran:
    lea dx, t_sobran
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
Sobran pociones
```

#### Solución
```asm
.model small
.stack 100h
.data
pociones db 5
t_sobran db 'Sobran pociones$'
t_faltan db 'Faltan pociones$'
.code
main proc
    mov ax, @data
    mov ds, ax

    cmp pociones, 3
    ja  sobran
    lea dx, t_faltan
    jmp mostrar
sobran:
    lea dx, t_sobran
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
Nova vierte el aceite en la rodilla y el engranaje gira un diente. —**Above** es «arriba de» —anota—: `ja`, mayor. **Below**, «abajo de»: `jb`, menor.

#### Imagen
- Un engranaje enorme de bronce en la rodilla de un gólem, con gotas de aceite dorado cayendo sobre sus dientes.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) vierte aceite de un frasquito.
- A su lado, en una repisa, otros frasquitos de luz en fila.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre la repisa, contando los frasquitos con la cola.

### Micro-misión R02-N02-P2 · El ogro que se cae por el borde

```meta
lugar: La rodilla del Gólem
personajes: Nova, Gheco
criatura: ogre
carta: jmp al final | cada camino del if termina saltando al final común · si no, se ejecutan los dos
recompensa: xp 15, oro 15
```

#### Escena
Ahora quedan **2** pociones, y el ojo dice «Faltan pociones**Sobran pociones**», todo junto. La rodilla intenta doblarse para los dos lados a la vez. Un ogro se ríe.

#### Gheco sugiere
Seguí el programa **paso a paso**: después de mostrar «Faltan», el Gólem sigue de largo y entra en el camino de «Sobran». Al final del primer camino falta un salto **por encima** del segundo.

#### Desafío
Tocá **Ejecutar** y mirá los dos mensajes. Después agregá lo que falta para que, con 2 pociones, el ojo diga solo `Faltan pociones`.

#### Código inicial
```asm
.model small
.stack 100h
.data
pociones db 2
t_sobran db 'Sobran pociones$'
t_faltan db 'Faltan pociones$'
.code
main proc
    mov ax, @data
    mov ds, ax

    cmp pociones, 3
    ja  sobran
    lea dx, t_faltan
    mov ah, 09h
    int 21h
sobran:
    lea dx, t_sobran
    mov ah, 09h
    int 21h
listo:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
Faltan pociones
```

#### Solución
```asm
.model small
.stack 100h
.data
pociones db 2
t_sobran db 'Sobran pociones$'
t_faltan db 'Faltan pociones$'
.code
main proc
    mov ax, @data
    mov ds, ax

    cmp pociones, 3
    ja  sobran
    lea dx, t_faltan
    mov ah, 09h
    int 21h
    jmp listo
sobran:
    lea dx, t_sobran
    mov ah, 09h
    int 21h
listo:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
La rodilla deja de temblar. El ogro, que esperaba ver al Gólem en el piso, se va arrastrando los pies. —Cada camino, con su salida —dice Nova.

#### Imagen
- La rodilla de bronce de un gólem gigante, con dos engranajes: uno girando y el otro quieto.
- Un ogro grandote y torpe se aleja de espaldas, decepcionado, arrastrando los pies.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) traba con una barra de luz cian el engranaje quieto.
- Gheco (gecko de luz cian con antiparras, chiquito) le saca la lengua al ogro.

### Micro-misión R02-N02-P3 · Solo si es la x

```meta
lugar: La rodilla del Gólem
personajes: Nova, Gheco
carta: Condición contraria | if sin else: saltá POR ENCIMA del bloque cuando NO se cumple · jne sigue
recompensa: xp 15, oro 15
```

#### Escena
Gheco quiere ponerse su sombrero de explorador (BL = 1), pero solo si Nova aprieta la **x**. Con cualquier otra tecla, nada.

#### Gheco sugiere
Para hacer algo **solo** si es la `x`, saltá **por encima** del bloque cuando **no** es la `x`: `jne sigue`. Si es la `x`, el salto no se cumple y el Gólem entra al bloque.

#### Desafío
Completá el salto para que, con la `x`, BL termine en **1**.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bl, 0
    mov ah, 07h
    int 21h

    cmp al, 'x'
    ___ sigue
    mov bl, 1        ; el sombrero
sigue:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Entrada
```
x
```

#### Estado esperado
```
BL = 1
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

    mov bl, 0
    mov ah, 07h
    int 21h

    cmp al, 'x'
    jne sigue
    mov bl, 1        ; el sombrero
sigue:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Gheco se pone el sombrero, que le queda grande y le tapa las antiparras. —Para hacer algo **si** pasa —anota Nova—, salto por encima **cuando no** pasa.

#### Imagen
- Gheco (gecko de luz cian con antiparras, chiquito) con un sombrero de explorador enorme que le tapa media cara, sentado sobre un engranaje de bronce.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se ríe tapándose la boca.
- Fondo: el interior de la rodilla de un gólem, con engranajes y luz ámbar.

### Micro-misión R02-N02-P4 · Par o impar

```meta
lugar: La rodilla del Gólem
personajes: Nova, Gheco, Kira
carta: Par o impar | div por 2 · AH = el resto · resto 0: par · como n % 2 == 0
recompensa: xp 15, oro 15
```

#### Escena
Kira inventa un juego: dice un número y el Gólem tiene que contestar si es **par** o **impar**. —Si es par, la rodilla se dobla para adelante —propone.

#### Gheco sugiere
Dividí por 2 y mirá el **resto**, que queda en AH: si es 0, el número es par. Compará AH con 0 y saltá a `par` si son iguales.

#### Desafío
Completá la comparación y el salto. Kira va a decir el `7`.

#### Código inicial
```asm
.model small
.stack 100h
.data
pide    db 'Un numero: $'
t_par   db 13, 10, 'Es par.$'
t_impar db 13, 10, 'Es impar.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h
    sub al, '0'

    mov ah, 0
    mov bl, 2
    div bl
    cmp ah, ___
    ___ par
    lea dx, t_impar
    jmp mostrar
par:
    lea dx, t_par
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
7
```

#### Salida esperada
```
Un numero: 7
Es impar.
```

#### Solución
```asm
.model small
.stack 100h
.data
pide    db 'Un numero: $'
t_par   db 13, 10, 'Es par.$'
t_impar db 13, 10, 'Es impar.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h
    sub al, '0'

    mov ah, 0
    mov bl, 2
    div bl
    cmp ah, 0
    je  par
    lea dx, t_impar
    jmp mostrar
par:
    lea dx, t_par
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
—¡Impar! —grita Kira, y la rodilla se dobla para atrás, con un crujido. Nova se ríe: es la primera vez que la pierna del Gólem se mueve.

#### Imagen
- La pierna de bronce de un gólem gigante doblando la rodilla hacia atrás, levantando polvo.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) levanta siete dedos, divertida.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se ríe, flotando.
- Gheco (gecko de luz cian con antiparras, chiquito) se agarra fuerte a la rodilla.

### Micro-misión R02-N02-P5 · El pulso

```meta
lugar: La rodilla del Gólem
personajes: Nova, Gheco, Kira
carta: else if | un cmp y varios saltos seguidos: ja gana · je empate · si no, pierde
recompensa: xp 20, oro 20
```

#### Escena
Kira desafía a un ogro a una pulseada sobre la rodilla del Gólem. Cada uno dice su fuerza, de 0 a 9. El Gólem tiene que anunciar: «Gana Kira», «Empate» o «Gana el ogro».

#### Gheco sugiere
Después de leer, la fuerza de Kira está en BL y la del ogro en AL. Un solo `cmp bl, al` y dos saltos seguidos: `ja gana` y `je empate`. Si no saltó ninguno, ganó el ogro. Cada caso carga su mensaje en DX y salta a `mostrar`.

#### Desafío
Escribí las órdenes desde cero, donde dice `; tus órdenes`. Kira y el ogro van a decir `5` y `5`.

#### Código inicial
```asm
.model small
.stack 100h
.data
pide    db 'Kira y el ogro: $'
t_gana  db 13, 10, 'Gana Kira.$'
t_empa  db 13, 10, 'Empate.$'
t_pierd db 13, 10, 'Gana el ogro.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h
    mov bl, al       ; la fuerza de Kira
    mov ah, 01h
    int 21h          ; la del ogro, en AL

    ; tus órdenes

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Entrada
```
5
5
```

#### Salida esperada
```
Kira y el ogro: 55
Empate.
```

#### Solución
```asm
.model small
.stack 100h
.data
pide    db 'Kira y el ogro: $'
t_gana  db 13, 10, 'Gana Kira.$'
t_empa  db 13, 10, 'Empate.$'
t_pierd db 13, 10, 'Gana el ogro.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h
    mov bl, al       ; la fuerza de Kira
    mov ah, 01h
    int 21h          ; la del ogro, en AL

    cmp bl, al
    ja  gana
    je  empate
    lea dx, t_pierd
    jmp mostrar
gana:
    lea dx, t_gana
    jmp mostrar
empate:
    lea dx, t_empa
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
«Empate». El ogro y Kira se dan la mano, sorprendidos. —Con un solo `cmp` —dice Nova— el Gólem eligió entre **tres** caminos.

#### Imagen
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) y un ogro grandote haciendo una pulseada sobre un engranaje de bronce que hace de mesa, los dos con la cara roja de esfuerzo.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) hace de árbitro con la mano levantada.
- Gheco (gecko de luz cian con antiparras, chiquito) mira con las patitas en la cara, nervioso.

### Prueba del sello

#### ¿Qué diferencia hay entre `ja` y `jae`?
`ja` salta si es mayor; `jae`, si es mayor o igual.

#### ¿Qué pasa si te olvidás el `jmp` al final del primer camino de un if/else?
El Gólem sigue de largo y ejecuta también el segundo camino.

#### Para hacer algo solo si AL es `'x'`, ¿qué salto va antes del bloque?
`jne`: el salto contrario, para pasar por encima del bloque cuando no es `'x'`.

#### ¿Se pueden poner dos saltos seguidos después de un `cmp`?
Sí: los interruptores no cambian hasta la próxima cuenta.

## R02-N03 · Rangos y menús

```meta
tipo: tema
criatura: ogre
padre: R02-N02
precio: 0
temas: prog.condicionales, prog.menu, err.validacion
```

### Crónica

Al pie del Gólem hay una **taberna** de los enanos de las Forjas, construida entre los dedos del pie hace tanto que nadie se acuerda. La tabernera, al enterarse de que el Gólem habla, le pide un favor: —¿Me atendés las mesas? La gente aprieta cualquier tecla.

Nova acepta. Gheco le advierte: —Lo primero que hay que aprender en una taberna es a decir «eso no está en el menú».

### Objetivos

Validar que una tecla esté **dentro de un rango** (un dígito, una letra) con dos comparaciones, armar un **menú**
con varias opciones y un mensaje para las teclas inválidas, y probar siempre **los bordes** del rango.

### Antes de empezar

- `ja`, `jb`, `jae`, `jbe` y el if/else (Dos caminos).

### Explicación

#### Un rango: dos preguntas
«Es un dígito» quiere decir «no es menor que `'0'` **y** no es mayor que `'9'`». En ensamblador, se descarta lo
que queda afuera por cada lado:
```asm
    cmp al, '0'
    jb  no_digito        ; menor que '0': afuera
    cmp al, '9'
    ja  no_digito        ; mayor que '9': afuera
    ...                  ; si llegó acá, es un dígito
```
Las letras son iguales: de `'A'` a `'Z'` las mayúsculas, de `'a'` a `'z'` las minúsculas (los códigos ASCII de
cada grupo están seguidos).

#### Un menú
Una comparación y un salto por opción, y un caso final para lo que no coincidió con nada:
```asm
    cmp al, '1'
    je  sopa
    cmp al, '2'
    je  pan
    lea dx, t_invalida   ; ninguna de las anteriores
    jmp mostrar
sopa:
    ...
```

#### Los bordes
Los errores casi siempre están en los bordes: el `'0'`, el `'9'`, la primera y la última opción. `jae` en vez de
`ja` deja afuera justo el `'9'`. Probá siempre el primero, el último y uno de afuera.

> **Puente con otras lenguas.** `if '0' <= c <= '9'` de Python, `if (c >= '0' && c <= '9')` de C o
> `isdigit(c)`: por dentro, dos comparaciones. El menú es un `switch`/`match` con su `default`.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
pide      db 'Una tecla: $'
t_digito  db 13, 10, 'Es un digito.$'
t_otra    db 13, 10, 'No es un digito.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h

    cmp al, '0'
    jb  no_digito
    cmp al, '9'
    ja  no_digito
    lea dx, t_digito
    jmp mostrar
no_digito:
    lea dx, t_otra
mostrar:
    mov ah, 09h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

### Entrada de ejemplo

```
4
```

### Salida esperada

```
Una tecla: 4
Es un digito.
```

### ¿Para qué sirve?

Nunca se confía en lo que tipea una persona: una edad de 300 años, una opción 7 en un menú de 3, una letra donde
iba un número. Validar rangos es lo que separa un programa que se rompe de uno que dice «probá de nuevo».

### Errores habituales

**Ogro: el borde que queda afuera.** `jae` donde iba `ja` (o `jbe` donde iba `jb`): el `'9'` o el `'0'` quedan
del lado equivocado.

**Ogro: el menú sin caso final.** Si ninguna comparación coincide y no hay un mensaje de «inválida», el Gólem
sigue de largo y entra al primer caso que encuentre abajo.

**Ogro: comparar el número en vez del carácter.** Después de la `01h`, AL tiene el **carácter** `'4'` (34h), no
el número 4: se compara con `'4'`, o primero se hace `sub al, '0'`.

### Micro-misión R02-N03-P1 · ¿Es un dígito?

```meta
lugar: La taberna del pie
personajes: Nova, Gheco
carta: Rango | cmp al, '0' + jb afuera · cmp al, '9' + ja afuera · lo que queda, adentro
recompensa: xp 10, oro 10
```

#### Escena
El primer cliente tiene que decir cuántas sopas quiere, pero aprieta la **k**. Nova tiene que darse cuenta de que eso no es un número.

#### Gheco sugiere
Dos preguntas: si es **menor** que `'0'`, está afuera (`jb`); si es **mayor** que `'9'`, también (`ja`). Las dos saltan al mismo lugar: `no_digito`.

#### Desafío
Completá los dos saltos. El cliente va a apretar la `k`.

#### Código inicial
```asm
.model small
.stack 100h
.data
pide      db 'Cuantas sopas? $'
t_digito  db 13, 10, 'Ya salen.$'
t_otra    db 13, 10, 'Eso no es un numero.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h

    cmp al, '0'
    ___ no_digito
    cmp al, '9'
    ___ no_digito
    lea dx, t_digito
    jmp mostrar
no_digito:
    lea dx, t_otra
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
k
```

#### Salida esperada
```
Cuantas sopas? k
Eso no es un numero.
```

#### Solución
```asm
.model small
.stack 100h
.data
pide      db 'Cuantas sopas? $'
t_digito  db 13, 10, 'Ya salen.$'
t_otra    db 13, 10, 'Eso no es un numero.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h

    cmp al, '0'
    jb  no_digito
    cmp al, '9'
    ja  no_digito
    lea dx, t_digito
    jmp mostrar
no_digito:
    lea dx, t_otra
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
El cliente se rasca la cabeza y aprieta el **3**. La tabernera asiente: el Gólem ya no se confunde.

#### Imagen
- Una taberna rústica de enanos construida entre los dedos de bronce de un pie gigante, con mesas de madera y faroles.
- Un enano cliente rascándose la cabeza, confundido, delante de una tecla de bronce.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) le explica algo con paciencia, con una bandeja en la mano.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre la bandeja.

### Micro-misión R02-N03-P2 · El nueve que no entraba

```meta
lugar: La taberna del pie
personajes: Nova, Gheco
criatura: ogre
carta: Los bordes | ja = mayor (el 9 queda adentro) · jae = mayor o igual (el 9 queda afuera) · probá el borde
recompensa: xp 15, oro 15
```

#### Escena
Una mesa grande pide **9** sopas, y el Gólem contesta «Eso no es un numero». La tabernera frunce el ceño. Un ogro, en la mesa del fondo, se ríe en la sopa.

#### Gheco sugiere
Mirá la segunda comparación: `jae` salta si es **mayor o igual** a `'9'`, así que el `'9'` queda afuera. Para dejarlo adentro, alcanza con saltar solo si es **mayor**.

#### Desafío
Tocá **Ejecutar** con el `9` y mirá el error del ogro. Después arreglá el salto del borde.

#### Código inicial
```asm
.model small
.stack 100h
.data
pide      db 'Cuantas sopas? $'
t_digito  db 13, 10, 'Ya salen.$'
t_otra    db 13, 10, 'Eso no es un numero.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h

    cmp al, '0'
    jb  no_digito
    cmp al, '9'
    jae no_digito
    lea dx, t_digito
    jmp mostrar
no_digito:
    lea dx, t_otra
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
Cuantas sopas? 9
Ya salen.
```

#### Solución
```asm
.model small
.stack 100h
.data
pide      db 'Cuantas sopas? $'
t_digito  db 13, 10, 'Ya salen.$'
t_otra    db 13, 10, 'Eso no es un numero.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h

    cmp al, '0'
    jb  no_digito
    cmp al, '9'
    ja  no_digito
    lea dx, t_digito
    jmp mostrar
no_digito:
    lea dx, t_otra
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
Nueve sopas humeantes llegan a la mesa grande. El ogro, sin nada de qué reírse, pide una para él.

#### Imagen
- Una mesa larga de madera en una taberna de enanos, con nueve tazones de sopa humeante en fila.
- Un ogro grandote sentado al fondo, con una cuchara, mirando la sopa con ganas.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) apoya el último tazón.
- Gheco (gecko de luz cian con antiparras, chiquito) se asoma por el borde de un tazón.

### Micro-misión R02-N03-P3 · El menú de la taberna

```meta
lugar: La taberna del pie
personajes: Nova, Gheco, Kira
carta: Menú | cmp + je por opción · un caso final para lo inválido · como switch con default
recompensa: xp 15, oro 15
```

#### Escena
La tabernera cuelga el menú: **1** Sopa, **2** Pan, **3** Jugo. Kira se sienta y aprieta el **2**.

#### Gheco sugiere
Ya están los casos de la sopa y del jugo. Falta el del pan: una comparación con `'2'` y un `je pan`, **antes** del caso inválido.

#### Desafío
Agregá la comparación que falta para que, con el `2`, el ojo diga `Pan caliente.`

#### Código inicial
```asm
.model small
.stack 100h
.data
menu   db '1) Sopa 2) Pan 3) Jugo: $'
t_sopa db 13, 10, 'Sopa de hongos.$'
t_pan  db 13, 10, 'Pan caliente.$'
t_jugo db 13, 10, 'Jugo de manzana.$'
t_mal  db 13, 10, 'Eso no esta en el menu.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, menu
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h

    cmp al, '1'
    je  sopa
    ; falta el pan
    cmp al, '3'
    je  jugo
    lea dx, t_mal
    jmp mostrar
sopa:
    lea dx, t_sopa
    jmp mostrar
pan:
    lea dx, t_pan
    jmp mostrar
jugo:
    lea dx, t_jugo
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
2
```

#### Salida esperada
```
1) Sopa 2) Pan 3) Jugo: 2
Pan caliente.
```

#### Solución
```asm
.model small
.stack 100h
.data
menu   db '1) Sopa 2) Pan 3) Jugo: $'
t_sopa db 13, 10, 'Sopa de hongos.$'
t_pan  db 13, 10, 'Pan caliente.$'
t_jugo db 13, 10, 'Jugo de manzana.$'
t_mal  db 13, 10, 'Eso no esta en el menu.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, menu
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h

    cmp al, '1'
    je  sopa
    cmp al, '2'
    je  pan
    cmp al, '3'
    je  jugo
    lea dx, t_mal
    jmp mostrar
sopa:
    lea dx, t_sopa
    jmp mostrar
pan:
    lea dx, t_pan
    jmp mostrar
jugo:
    lea dx, t_jugo
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
Pan caliente para Kira, que lo parte en dos y le da la mitad a Gheco. La tabernera le guiña un ojo al Gólem.

#### Imagen
- Una pizarra de taberna colgada con tres dibujitos de tiza: un tazón, un pan y una jarra, sin letras.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) parte un pan caliente en dos, sentada a una mesa.
- Gheco (gecko de luz cian con antiparras, chiquito) recibe su mitad con las dos patitas.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) con una bandeja, sonriendo.

### Micro-misión R02-N03-P4 · Mayúscula o minúscula

```meta
lugar: La taberna del pie
personajes: Nova, Gheco
carta: Letras | 'A' a 'Z' mayúsculas · 'a' a 'z' minúsculas · cada grupo, seguido en ASCII
recompensa: xp 15, oro 15
```

#### Escena
La tabernera anota los pedidos con una letra por mesa, pero se le mezclan mayúsculas y minúsculas. Le pide al Gólem que le diga qué es cada una.

#### Gheco sugiere
Las mayúsculas van de `'A'` a `'Z'` y las minúsculas de `'a'` a `'z'`. Probá primero si está en el rango de las mayúsculas; si no, en el de las minúsculas; si no, es otra cosa. Ya está hecho el de las mayúsculas: copiá la idea.

#### Desafío
Completá el rango de las minúsculas. La tabernera va a apretar la `g`.

#### Código inicial
```asm
.model small
.stack 100h
.data
pide    db 'Letra: $'
t_mayus db 13, 10, 'Mayuscula.$'
t_minus db 13, 10, 'Minuscula.$'
t_otra  db 13, 10, 'No es una letra.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h

    cmp al, 'A'
    jb  no_mayus
    cmp al, 'Z'
    ja  no_mayus
    lea dx, t_mayus
    jmp mostrar
no_mayus:
    cmp al, ___
    jb  otra
    cmp al, ___
    ja  otra
    lea dx, t_minus
    jmp mostrar
otra:
    lea dx, t_otra
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
g
```

#### Salida esperada
```
Letra: g
Minuscula.
```

#### Solución
```asm
.model small
.stack 100h
.data
pide    db 'Letra: $'
t_mayus db 13, 10, 'Mayuscula.$'
t_minus db 13, 10, 'Minuscula.$'
t_otra  db 13, 10, 'No es una letra.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h

    cmp al, 'A'
    jb  no_mayus
    cmp al, 'Z'
    ja  no_mayus
    lea dx, t_mayus
    jmp mostrar
no_mayus:
    cmp al, 'a'
    jb  otra
    cmp al, 'z'
    ja  otra
    lea dx, t_minus
    jmp mostrar
otra:
    lea dx, t_otra
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
—Minúscula —confirma Nova—. Y entre la `Z` y la `a` hay unos signos raros: por eso no alcanza con un solo rango de la `A` a la `z`.

#### Imagen
- Una libreta cerrada de cuero sobre una mesa de taberna, y al lado dos fichas de madera lisas, una grande y una chica, con un dibujito de hoja cada una.
- La tabernera, una enana robusta de delantal, sostiene la ficha grande.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) señala la ficha chica.
- Gheco (gecko de luz cian con antiparras, chiquito) sentado en la libreta.

### Micro-misión R02-N03-P5 · La libreta de la escuela

```meta
lugar: La taberna del pie
personajes: Nova, Gheco
carta: Rangos en fila | primero lo inválido · después cada tramo con jbe · como if / elif / else
recompensa: xp 20, oro 20
```

#### Escena
La hija de la tabernera trae su libreta: quiere saber cómo le fue según la nota, de 0 a 9. De **0 a 3**, desaprobada; de **4 a 6**, aprobada; de **7 a 9**, promocionada. Cualquier otra tecla, nota inválida.

#### Gheco sugiere
Primero descartá lo que no es un dígito (dos comparaciones). Después, los tramos en orden: si es `jbe '3'`, desaprobada; si no, si es `jbe '6'`, aprobada; si no, promocionada. Cada caso carga su mensaje y salta a `mostrar`.

#### Desafío
Escribí las órdenes desde cero, donde dice `; tus órdenes`. La nota va a ser un `7`.

#### Código inicial
```asm
.model small
.stack 100h
.data
pide   db 'Nota: $'
t_des  db 13, 10, 'Desaprobada.$'
t_apr  db 13, 10, 'Aprobada.$'
t_pro  db 13, 10, 'Promocionada.$'
t_inv  db 13, 10, 'Nota invalida.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 01h
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
7
```

#### Salida esperada
```
Nota: 7
Promocionada.
```

#### Solución
```asm
.model small
.stack 100h
.data
pide   db 'Nota: $'
t_des  db 13, 10, 'Desaprobada.$'
t_apr  db 13, 10, 'Aprobada.$'
t_pro  db 13, 10, 'Promocionada.$'
t_inv  db 13, 10, 'Nota invalida.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, pide
    mov ah, 09h
    int 21h
    mov ah, 01h
    int 21h

    cmp al, '0'
    jb  invalida
    cmp al, '9'
    ja  invalida
    cmp al, '3'
    jbe desaprobada
    cmp al, '6'
    jbe aprobada
    lea dx, t_pro
    jmp mostrar
desaprobada:
    lea dx, t_des
    jmp mostrar
aprobada:
    lea dx, t_apr
    jmp mostrar
invalida:
    lea dx, t_inv
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
«Promocionada». La nena sale saltando entre las mesas. La tabernera, emocionada, le regala al Gólem un barril de aceite para las rodillas.

#### Imagen
- Una nena enana con trenzas, de vestido largo y delantal, salta de alegría entre las mesas de una taberna, levantando una libreta cerrada.
- Su madre, la tabernera, rueda un barril de aceite hacia un pie de bronce gigante.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) aplaude.
- Gheco (gecko de luz cian con antiparras, chiquito) da una voltereta sobre una mesa.

### Prueba del sello

#### ¿Cómo se pregunta si AL es un dígito?
Con dos comparaciones: `cmp al, '0'` + `jb` afuera, y `cmp al, '9'` + `ja` afuera.

#### ¿Qué pasa en un menú si falta el caso de «inválida»?
Si ninguna opción coincide, el Gólem sigue de largo y entra en el primer caso que haya abajo.

#### ¿Qué valores conviene probar en un rango?
El primero, el último y uno de afuera de cada lado (los bordes).

#### Después de la `01h`, ¿con qué se compara la tecla `4`: con `4` o con `'4'`?
Con `'4'`: AL tiene el carácter, no el número.

## R02-N04 · Con signo y sin signo

```meta
tipo: tema
criatura: ogre
padre: R02-N03
precio: 0
temas: maq.banderas, maq.numeracion, maq.saltos
```

### Crónica

Afuera, en las Forjas, empieza a nevar: algo rarísimo. Kira mira el termómetro de bronce que el Gólem tiene en el tobillo: marca **−1**. Pero el Gólem anuncia, muy seguro: «Hace calor».

—¿Cómo puede equivocarse? —se enoja Nova—. ¡Él no adivina!

—No se equivocó —dice Gheco—. Hizo exactamente lo que le pediste. El problema es **cómo** le pediste que mire el número.

### Objetivos

Entender que un mismo byte se puede leer **sin signo** (0 a 255) o **con signo** (−128 a 127), elegir el salto
según el caso (`ja`/`jb` para cantidades y letras, `jg`/`jl` para números que pueden ser negativos) y conocer la
bandera **OF** (desborde con signo).

### Antes de empezar

- Los números negativos y `neg` (Las cuentas del Gólem).
- `ja`, `jb` y el if/else (Dos caminos).

### Explicación

#### Un byte, dos lecturas
`FFh` es **255** si lo leés sin signo, y **−1** si lo leés con signo. El Gólem no sabe cuál de las dos querías:
**vos** se lo decís con el salto que elegís.

| Sin signo (cantidades, letras) | Con signo (temperaturas, saldos) | Salta si `a` es… |
|---|---|---|
| `ja` (*above*) | `jg` (*greater*) | mayor |
| `jae` | `jge` | mayor o igual |
| `jb` (*below*) | `jl` (*less*) | menor |
| `jbe` | `jle` | menor o igual |

`je` y `jne` sirven para los dos: igual es igual.

```asm
mov al, 0FFh
cmp al, 1
ja  mayor      ; salta: 255 es mayor que 1
jg  mayor      ; NO salta: −1 es menor que 1
```

#### OF: el desborde con signo
Así como **CF** avisa que una cuenta sin signo se pasó, **OF** (*overflow*) avisa que una cuenta **con signo** no
entra: `127 + 1` en un byte da `−128` y prende OF. Los saltos con signo miran OF y SF; los sin signo, CF.

> **Puente con otras lenguas.** Es la diferencia entre `unsigned char` y `signed char` en C, o entre `int` y
> `unsigned int`. En C, comparar un número con signo con uno sin signo da resultados raros justamente por esto.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
t_sin db 'Sin signo: FFh es MAYOR que 1$'
t_con db 13, 10, 'Con signo: FFh es MENOR que 1$'
t_x   db 13, 10, '?$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 0FFh
    cmp al, 1
    ja  sin_mayor
    lea dx, t_x
    jmp muestra1
sin_mayor:
    lea dx, t_sin
muestra1:
    mov ah, 09h
    int 21h

    mov al, 0FFh
    cmp al, 1
    jl  con_menor
    lea dx, t_x
    jmp muestra2
con_menor:
    lea dx, t_con
muestra2:
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
Sin signo: FFh es MAYOR que 1
Con signo: FFh es MENOR que 1
```

### ¿Para qué sirve?

Saldos, temperaturas, coordenadas, velocidades: todo lo que puede ser negativo necesita los saltos con signo. Los
errores de signo son de los más difíciles de encontrar en C y C++, y entender el byte «con dos lecturas» los
vuelve obvios.

### Errores habituales

**Ogro: `ja` donde iba `jg`.** Comparar números negativos con saltos sin signo: −1 (`FFh`) «es mayor» que 1.

**Ogro: `jg` para letras o cantidades grandes.** Al revés: un 200 leído con signo es −56, y `jg` dice que es menor
que 1.

**Ogro: el desborde que no se mira.** `127 + 1` en un byte da −128 (y OF = 1): si el número puede crecer, usá 16
bits.

### Micro-misión R02-N04-P1 · El termómetro mentiroso

```meta
lugar: El tobillo del Gólem
personajes: Nova, Gheco, Kira
criatura: ogre
carta: jg | mayor CON signo · para números que pueden ser negativos · ja es sin signo
recompensa: xp 15, oro 15
```

#### Escena
El termómetro marca **−1** y el Gólem dice «Hace calor». Un ogro, abrigado hasta las orejas, se ríe a carcajadas mientras tiembla de frío.

#### Gheco sugiere
`ja` lee el `−1` como **255**, y 255 es mayor que 0. Para una temperatura, que puede ser negativa, el salto tiene que ser **con signo**: `jg`.

#### Desafío
Tocá **Ejecutar** y mirá lo que dice. Después cambiá el salto para que, con −1, el ojo diga `Hace frio`.

#### Código inicial
```asm
.model small
.stack 100h
.data
temp    db -1
t_calor db 'Hace calor$'
t_frio  db 'Hace frio$'
.code
main proc
    mov ax, @data
    mov ds, ax

    cmp temp, 0
    ja  calor
    lea dx, t_frio
    jmp mostrar
calor:
    lea dx, t_calor
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
Hace frio
```

#### Solución
```asm
.model small
.stack 100h
.data
temp    db -1
t_calor db 'Hace calor$'
t_frio  db 'Hace frio$'
.code
main proc
    mov ax, @data
    mov ds, ax

    cmp temp, 0
    jg  calor
    lea dx, t_frio
    jmp mostrar
calor:
    lea dx, t_calor
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
«Hace frio». Kira se pone la bufanda, satisfecha. El ogro deja de reírse y estornuda.

#### Imagen
- Un termómetro de bronce con una columna de líquido cian bajita, en el tobillo de un gólem gigante, con copos de nieve cayendo.
- Un ogro grandote y torpe abrigado hasta las orejas, estornudando.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) se acomoda una bufanda.
- Gheco (gecko de luz cian con antiparras, chiquito) con un gorrito de lana.

### Micro-misión R02-N04-P2 · El desborde

```meta
lugar: El tobillo del Gólem
personajes: Nova, Gheco
carta: OF | desborde con signo · 127 + 1 en un byte da -128 · CF es el desborde sin signo
recompensa: xp 15, oro 15
```

#### Escena
El termómetro sube y sube con el sol: ya marca **127**, lo máximo que entra con signo en un cajón chico. Nova le suma un grado más y el termómetro marca… −128.

#### Gheco sugiere
`127 + 1` no entra en un byte con signo: da la vuelta a −128 y el Gólem prende **OF**, el interruptor del desborde. También se prende **SF**, porque el resultado quedó «negativo».

#### Desafío
Completá la suma para que AL pase de 127 al desborde, y mirá en **Interruptores** cómo se prenden OF y SF.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 127
    add al, ___

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
AL = -128
OF = 1
SF = 1
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

    mov al, 127
    add al, 1

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El termómetro se rompe con un *ping* y la columna cian cae de golpe hasta abajo. —Se pasó por arriba y apareció por abajo —dice Nova—. Como una vuelta al mundo.

#### Imagen
- Un termómetro de bronce rajado, con la columna de líquido cian cayendo de arriba abajo en espiral.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se cubre la cara con un brazo, sorprendida.
- Gheco (gecko de luz cian con antiparras, chiquito) atrapa una gota cian con un frasquito.

### Micro-misión R02-N04-P3 · La deuda de Gheco

```meta
lugar: El tobillo del Gólem
personajes: Nova, Gheco
carta: jl | menor CON signo · jl = less · jb = below, sin signo
recompensa: xp 15, oro 15
```

#### Escena
Gheco le debe **5** monedas a la tabernera: su saldo es **−5**. Nova quiere que el Gólem avise «Gheco debe monedas» cuando el saldo sea **menor que 0**.

#### Gheco sugiere
El saldo puede ser negativo, así que el salto va **con signo**: *menor* con signo es `jl` (*less*).

#### Desafío
Completá el salto para que, con −5, el ojo diga `Gheco debe monedas.`

#### Código inicial
```asm
.model small
.stack 100h
.data
saldo   dw -5
t_debe  db 'Gheco debe monedas.$'
t_libre db 'Gheco no debe nada.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    cmp saldo, 0
    ___ debe
    lea dx, t_libre
    jmp mostrar
debe:
    lea dx, t_debe
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
Gheco debe monedas.
```

#### Solución
```asm
.model small
.stack 100h
.data
saldo   dw -5
t_debe  db 'Gheco debe monedas.$'
t_libre db 'Gheco no debe nada.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    cmp saldo, 0
    jl  debe
    lea dx, t_libre
    jmp mostrar
debe:
    lea dx, t_debe
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
Gheco agacha la cabeza. Nova le presta cinco monedas, y él promete devolverlas. (Spoiler: tarda bastante.)

#### Imagen
- Gheco (gecko de luz cian con antiparras, chiquito) con cara de culpa, recibiendo cinco monedas doradas en sus patitas.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se las da con una sonrisa paciente.
- Al fondo, la tabernera enana de brazos cruzados.

### Micro-misión R02-N04-P4 · El más grande

```meta
lugar: El tobillo del Gólem
personajes: Nova, Gheco
carta: Máximo con signo | cmp a, b + jg · el mayor queda en BL · con ja, -3 parece 253
recompensa: xp 20, oro 20
```

#### Escena
Dos termómetros marcan **−3** y **2**. El Gólem tiene que guardar en BL **la temperatura más alta**, para decidir si encender la caldera.

#### Gheco sugiere
Poné la primera en AL y compará con la segunda. Si AL es **mayor con signo** (`jg`), el máximo es AL; si no, es la otra. Al final, el máximo tiene que quedar en BL.

#### Desafío
Escribí las órdenes desde cero, donde dice `; tus órdenes`, para que BL quede con la temperatura más alta.

#### Código inicial
```asm
.model small
.stack 100h
.data
temp1 db -3
temp2 db 2
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
BL = 2
```

#### Solución
```asm
.model small
.stack 100h
.data
temp1 db -3
temp2 db 2
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, temp1
    cmp al, temp2
    jg  primera
    mov bl, temp2
    jmp listo
primera:
    mov bl, al
listo:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
BL = 2. La caldera del tobillo no hace falta: con 2 grados alcanza. Nova anota en sus cajones la regla de oro: **letras y cantidades, `ja` y `jb`; lo que puede ser negativo, `jg` y `jl`**.

#### Imagen
- Dos termómetros de bronce lado a lado: uno con la columna cian bajita bajo una línea, el otro un poco más alto.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) señala el más alto.
- Gheco (gecko de luz cian con antiparras, chiquito) abrazado al más alto, para calentarse.

### Prueba del sello

#### ¿Qué vale `FFh` sin signo? ¿Y con signo?
255 sin signo; −1 con signo.

#### ¿Qué salto usás para «mayor» en una temperatura? ¿Y en una cantidad de pociones?
`jg` para la temperatura (puede ser negativa); `ja` para las pociones.

#### ¿Qué avisa OF?
Que una cuenta con signo no entró (por ejemplo, 127 + 1 en un byte).

#### ¿Sirven `je` y `jne` con signo y sin signo?
Sí: igual es igual en las dos lecturas.
