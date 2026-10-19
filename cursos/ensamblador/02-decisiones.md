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

## R02-N05 · Repetir: `loop`

```meta
tipo: tema
criatura: ogre
padre: R02-N04
precio: 0
temas: prog.bucles, maq.saltos
```

### Crónica

Para que la pierna se mueva, alguien tiene que darle **cuerda** al resorte del muslo: girar la manivela una vez, y otra, y otra. Nova la gira cinco veces escribiendo cinco órdenes iguales y se cansa.

—¿Y si fueran cien? —protesta.

{mentor} hace sonar un engranaje, divertido. —Decime **cuántas veces**, decime **qué**, y yo lo repito. Para eso tengo la palanca **CX**: la palanca de contar.

### Objetivos

Repetir un bloque una cantidad fija de veces con `loop` y CX, acumular un resultado dentro de un bucle, evitar el
`loop` con CX en 0 (`jcxz`) y anidar dos bucles sin que se pisen el contador.

### Antes de empezar

- Etiquetas y saltos (Las compuertas).
- `add`, `inc`, `dec` y el truco de las dos cifras (Las cuentas del Gólem).

### Explicación

#### `loop`: repetir CX veces
```asm
    mov cx, 5            ; cuántas vueltas
vuelta:
    ...                  ; el cuerpo
    loop vuelta          ; CX = CX - 1; si CX no llegó a 0, vuelve a "vuelta"
```
`loop` resta 1 a CX y, si no llegó a 0, salta a la etiqueta. Dentro del cuerpo, CX va valiendo 5, 4, 3, 2, 1:
se puede usar para mostrar una cuenta regresiva.

#### Acumular
Un **acumulador** es una palanca que empieza en 0 y en cada vuelta suma algo:
```asm
    mov bl, 0
    mov cx, 5
suma:
    add bl, cl           ; 5 + 4 + 3 + 2 + 1
    loop suma            ; BL = 15
```

#### `loop` con CX en 0: 65.536 vueltas
`loop` **primero resta** y después mira: si CX valía 0, pasa a 65535 y da la vuelta completa. Si la cantidad puede
ser 0, poné antes `jcxz` (*jump if CX is zero*), que salta por encima del bucle:
```asm
    jcxz sin_vueltas
vuelta:
    ...
    loop vuelta
sin_vueltas:
```

#### Bucles anidados
Si los dos bucles usan `loop`, comparten CX: el de adentro lo deja en 0 y rompe al de afuera. Que el de afuera
cuente con **otra palanca** (BL, por ejemplo) con `dec` y `jnz`:
```asm
    mov bl, 3            ; 3 filas
filas:
    mov cx, 6            ; 6 ladrillos por fila
ladrillos:
    ...
    loop ladrillos
    dec bl
    jnz filas            ; jnz: salta si el dec no dio 0
```

> **Puente con otras lenguas.** `loop` es el `for i in range(5)` de Python o el `for (int i = 5; i > 0; i--)` de
> C, contado hacia atrás. Y el «acumulador» es el `total += x` de siempre.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
t_cuenta db 'Cuenta regresiva: $'
t_muro   db 13, 10, 'Muralla:', 13, 10, '$'
salto    db 13, 10, '$'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_cuenta
    mov ah, 09h
    int 21h
    mov cx, 5
cuenta:
    mov dl, cl
    add dl, '0'
    mov ah, 02h
    int 21h
    mov dl, ' '
    int 21h
    loop cuenta

    lea dx, t_muro
    mov ah, 09h
    int 21h
    mov bl, 2
filas:
    mov cx, 4
ladrillos:
    mov dl, '#'
    mov ah, 02h
    int 21h
    loop ladrillos
    lea dx, salto
    mov ah, 09h
    int 21h
    dec bl
    jnz filas

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

### Salida esperada

```
Cuenta regresiva: 5 4 3 2 1
Muralla:
####
####
```

### ¿Para qué sirve?

Recorrer una lista, dibujar una fila, repetir un intento, sumar todos los precios de un carrito: todo bucle de
todo lenguaje termina siendo un contador, una comparación y un salto hacia atrás.

### Errores habituales

**Ogro: `loop` con CX en 0.** Da 65.536 vueltas. Si la cantidad puede ser 0, `jcxz` antes del bucle.

**Ogro: el CX compartido.** Dos `loop` anidados con el mismo CX: el de afuera da una sola vuelta (o infinitas).
Usá otra palanca para el de afuera.

**Ogro: pisar CX adentro del cuerpo.** Un `mov cx, …` dentro del bucle (para otra cosa) arruina la cuenta.

**Ogro: el `mov cx` adentro de la etiqueta.** Si `mov cx, 5` queda **después** de `vuelta:`, cada vuelta vuelve a
poner 5 y el bucle no termina nunca: «El Gólem se quedó dando vueltas».

### Micro-misión R02-N05-P1 · Cuenta regresiva

```meta
lugar: El muslo del Gólem
personajes: Nova, Gheco
carta: loop | mov cx, n · cuerpo · loop etiqueta = CX - 1 y, si no es 0, volvé · como for
recompensa: xp 10, oro 10
```

#### Escena
Antes de girar la manivela, Nova quiere contar para atrás, como en las carreras: 5, 4, 3, 2, 1.

#### Gheco sugiere
Poné en CX cuántas vueltas querés. Adentro, CX va valiendo 5, 4, 3, 2, 1: mostralo con `+ '0'`. Al final del cuerpo, `loop` con el nombre de la etiqueta.

#### Desafío
Completá la cantidad de vueltas y el `loop` para que el ojo muestre la cuenta regresiva.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov cx, ___
cuenta:
    mov dl, cl
    add dl, '0'
    mov ah, 02h
    int 21h
    mov dl, ' '
    int 21h
    loop ___

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
5 4 3 2 1
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
    mov dl, cl
    add dl, '0'
    mov ah, 02h
    int 21h
    mov dl, ' '
    int 21h
    loop cuenta

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
¡Uno! Nova gira la manivela de un tirón. Ejecutá **paso a paso** y mirá cómo CX baja en la pestaña **Palancas**, vuelta por vuelta.

#### Imagen
- Una manivela de bronce enorme en el muslo de un gólem, con un resorte en espiral a la vista.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) agarra la manivela con las dos manos, lista para girar.
- Gheco (gecko de luz cian con antiparras, chiquito) levanta una banderita lisa, como largador de carrera.

### Micro-misión R02-N05-P2 · Cinco vueltas de cuerda

```meta
lugar: El muslo del Gólem
personajes: Nova, Gheco
carta: Acumulador | empieza en 0 · en cada vuelta suma algo · como total += x
recompensa: xp 15, oro 15
```

#### Escena
Cada vuelta de manivela le da al resorte tanta fuerza como el número de la vuelta: la quinta da 5, la cuarta 4… Nova quiere saber cuánta fuerza juntó en total.

#### Gheco sugiere
BL es el **acumulador**: empieza en 0. En cada vuelta, sumale CL (que va 5, 4, 3, 2, 1).

#### Desafío
Completá la suma de adentro del bucle para que BL termine con la fuerza total.

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
    mov cx, 5
cuerda:
    add bl, ___
    loop cuerda

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
BL = 15
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

    mov bl, 0
    mov cx, 5
cuerda:
    add bl, cl
    loop cuerda

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Quince de fuerza. El resorte del muslo queda tenso, vibrando. —Un `total += x` —dice Nova—, pero con mis propias palancas.

#### Imagen
- Un resorte de bronce enorme, tenso y brillante, dentro del muslo de un gólem.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se seca la frente, cansada pero contenta, apoyada en la manivela.
- Gheco (gecko de luz cian con antiparras, chiquito) mide el resorte con una cinta métrica lisa.

### Micro-misión R02-N05-P3 · Cero vueltas

```meta
lugar: El muslo del Gólem
personajes: Nova, Gheco
criatura: ogre
carta: jcxz | salta si CX = 0 · ponelo antes de un loop si la cantidad puede ser 0
recompensa: xp 15, oro 15
```

#### Escena
Kira dejó anotado en un cajón cuántas estrellas hay que dibujar en el muslo: **0**. Nova arma el bucle… y el Gólem empieza a dibujar estrellas sin parar. Un ogro aplaude.

#### Gheco sugiere
`loop` primero resta: con CX en 0, pasa a 65535 y da la vuelta entera. Antes del bucle, `jcxz sin_estrellas` salta por encima si CX vale 0.

#### Desafío
Tocá **Ejecutar** y mirá lo que pasa. Después agregá el `jcxz` para que, con 0 estrellas, no se dibuje ninguna.

#### Código inicial
```asm
.model small
.stack 100h
.data
cuantas db 0
titulo  db 'Estrellas: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, titulo
    mov ah, 09h
    int 21h

    mov cl, cuantas
    mov ch, 0
estrella:
    mov dl, '*'
    mov ah, 02h
    int 21h
    loop estrella
sin_estrellas:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
Estrellas:
```

#### Solución
```asm
.model small
.stack 100h
.data
cuantas db 0
titulo  db 'Estrellas: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, titulo
    mov ah, 09h
    int 21h

    mov cl, cuantas
    mov ch, 0
    jcxz sin_estrellas
estrella:
    mov dl, '*'
    mov ah, 02h
    int 21h
    loop estrella
sin_estrellas:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Ninguna estrella, como pedía Kira. El ogro se queda con las manos en el aire, a mitad del aplauso.

#### Imagen
- El muslo de bronce de un gólem gigante cubierto de estrellitas cian dibujadas, demasiadas, una al lado de otra.
- Un ogro grandote y torpe aplaudiendo, encantado.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) borra las estrellas con un trapo de luz.
- Gheco (gecko de luz cian con antiparras, chiquito) se tapa los ojos.

### Micro-misión R02-N05-P4 · La muralla

```meta
lugar: El muslo del Gólem
personajes: Nova, Gheco
carta: Bucles anidados | el de adentro con loop (CX) · el de afuera con otra palanca: dec bl + jnz
recompensa: xp 15, oro 15
```

#### Escena
Para proteger el resorte, Nova quiere levantar una muralla de **3** filas de **6** ladrillos cada una.

#### Gheco sugiere
El bucle de adentro dibuja una fila con `loop` (CX = 6). El de afuera cuenta las filas con **BL**: después de cada fila, salto de renglón, `dec bl` y `jnz filas` (salta si BL no llegó a 0). Ojo: el `mov cx, 6` va **adentro** del bucle de afuera, para que cada fila empiece de nuevo.

#### Desafío
Completá las tres órdenes que faltan para que se dibujen las 3 filas.

#### Código inicial
```asm
.model small
.stack 100h
.data
salto db 13, 10, '$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bl, ___
filas:
    mov cx, ___
ladrillos:
    mov dl, '#'
    mov ah, 02h
    int 21h
    loop ladrillos
    lea dx, salto
    mov ah, 09h
    int 21h
    dec bl
    ___ filas

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
######
######
######
```

#### Solución
```asm
.model small
.stack 100h
.data
salto db 13, 10, '$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bl, 3
filas:
    mov cx, 6
ladrillos:
    mov dl, '#'
    mov ah, 02h
    int 21h
    loop ladrillos
    lea dx, salto
    mov ah, 09h
    int 21h
    dec bl
    jnz filas

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Tres filas parejas. —Un bucle adentro de otro —dice Nova—, cada uno con su propia palanca de contar.

#### Imagen
- Una muralla chica de ladrillos de bronce, tres filas de seis, delante de un resorte enorme.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) coloca el último ladrillo.
- Gheco (gecko de luz cian con antiparras, chiquito) camina por arriba de la muralla, como un equilibrista.

### Micro-misión R02-N05-P5 · La feria de los números

```meta
lugar: El muslo del Gólem
personajes: Nova, Gheco, Kira
carta: loop + acumulador | sumar 1 + 2 + … + 9 · mostrar el resultado en dos cifras
recompensa: xp 20, oro 20
```

#### Escena
En la feria de las Forjas hay un juego: el que diga cuánto da **1 + 2 + 3 + … + 9** se lleva un premio. Kira desafía al Gólem.

#### Gheco sugiere
Un `loop` con CX = 9 y un acumulador en BL que suma CL en cada vuelta. Después, el truco de las dos cifras: AL = BL, AH en 0, dividí por 10, guardá AX en CX y mostrá las dos.

#### Desafío
Escribí las órdenes desde cero, donde dice `; tus órdenes`, para que el ojo diga `Suma: 45`.

#### Código inicial
```asm
.model small
.stack 100h
.data
texto db 'Suma: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, texto
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
Suma: 45
```

#### Solución
```asm
.model small
.stack 100h
.data
texto db 'Suma: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, texto
    mov ah, 09h
    int 21h

    mov bl, 0
    mov cx, 9
sumar:
    add bl, cl
    loop sumar

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
end main
```

#### Al superarla
«Suma: 45». El feriante le entrega a Kira un muñequito de bronce del Gólem. Ella se lo regala a Nova, que no tiene manos de verdad para agarrarlo, pero lo guarda en un cajón igual.

#### Imagen
- Un puesto de feria de las Forjas, con banderines lisos de colores y faroles.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) recibe un muñequito de bronce con forma de gólem de manos del feriante, un enano sonriente.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre el mostrador.
- Al fondo, el ojo de un gólem gigante encendido, mirando la feria.

### Prueba del sello

#### ¿Qué hace `loop vuelta`?
Le resta 1 a CX y, si CX no llegó a 0, salta a `vuelta`.

#### ¿Qué pasa si se entra a un `loop` con CX en 0?
Da 65.536 vueltas, porque `loop` primero resta. Se evita con `jcxz` antes del bucle.

#### En dos bucles anidados, ¿por qué el de afuera no puede usar `loop` también?
Porque compartirían CX: el de adentro lo deja en 0 y arruina la cuenta del de afuera.

#### ¿Qué es un acumulador?
Una palanca (o variable) que empieza en 0 y en cada vuelta suma algo.

## R02-N06 · Mientras y hasta que

```meta
tipo: tema
criatura: ogre
padre: R02-N05
precio: 0
temas: prog.bucles, maq.saltos
```

### Crónica

En la cadera del Gólem hay un **horno** pequeño que calienta el aceite de las piernas. Hay que soplar el fuelle **mientras** el horno esté frío, y no se sabe de antemano cuántas veces.

Kira, del otro lado de una puerta, golpea para entrar. —¿Cuántas veces va a golpear? —pregunta Nova. —No sé —dice Gheco—. **Hasta que** diga basta.

### Objetivos

Repetir mientras se cumpla una condición (**mientras**, que pregunta antes de cada vuelta) y repetir hasta que
algo pase (**hacer… hasta que**, que pregunta al final y se ejecuta al menos una vez); evitar el bucle infinito y
el «uno de más»; leer teclas hasta un terminador.

### Antes de empezar

- `loop` y los bucles anidados (Repetir).
- `ja`, `jae`, `jb`, `jbe` (Dos caminos).

### Explicación

#### Mientras: la pregunta va antes
```asm
mientras:
    cmp calor, 8
    jae fin_mientras     ; si NO se cumple "calor < 8", se termina
    add calor, 3         ; el cuerpo
    jmp mientras         ; volver a preguntar
fin_mientras:
```
Se compara al principio y se **sale** con el salto **contrario** a la condición. Si de entrada no se cumple, el
cuerpo no se ejecuta nunca.

#### Hacer… hasta que: la pregunta va al final
```asm
hacer:
    mov ah, 01h          ; el cuerpo: leer una tecla
    int 21h
    cmp al, 'x'
    jne hacer            ; repetir hasta que sea 'x'
```
El cuerpo va primero y la pregunta al final, así que se ejecuta **al menos una vez**. Es lo ideal para menús y
para leer hasta que el usuario diga basta.

#### Algo tiene que cambiar
En un «mientras», el cuerpo tiene que cambiar algo que la condición mira. Si no, la condición nunca deja de
cumplirse: el Gólem se queda dando vueltas para siempre.

> **Puente con otras lenguas.** El primero es el `while` de C, Python y Java; el segundo, el `do { } while` de C
> y Java (Python no lo tiene: se arma con `while True` y un `break`).

### Código de ejemplo

```asm
.model small
.stack 100h
.data
calor   db 0
golpes  db 0
t_fuel  db 'Fuelle: $'
t_golpe db 13, 10, 'Golpes (x para terminar): $'
t_total db 13, 10, 'Golpes dados: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_fuel
    mov ah, 09h
    int 21h
mientras:
    cmp calor, 8
    jae fin_mientras
    add calor, 3
    mov dl, calor
    add dl, '0'
    mov ah, 02h
    int 21h
    mov dl, ' '
    int 21h
    jmp mientras
fin_mientras:

    lea dx, t_golpe
    mov ah, 09h
    int 21h
hacer:
    mov ah, 01h
    int 21h
    cmp al, 'g'
    jne no_golpe
    inc golpes
no_golpe:
    cmp al, 'x'
    jne hacer

    lea dx, t_total
    mov ah, 09h
    int 21h
    mov dl, golpes
    add dl, '0'
    mov ah, 02h
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

### Entrada de ejemplo

```
g
g
z
g
x
```

### Salida esperada

```
Fuelle: 3 6 9
Golpes (x para terminar): ggzgx
Golpes dados: 3
```

### ¿Para qué sirve?

La mayoría de los bucles reales no saben de antemano cuántas vueltas van a dar: leer un archivo hasta el final,
esperar que el jugador apriete una tecla, reintentar hasta que la conexión ande. Para eso están el «mientras» y
el «hasta que».

### Errores habituales

**Ogro: el bucle infinito.** Un «mientras» en el que nada cambia la condición (falta el `add calor, 3`): «El Gólem
se quedó dando vueltas».

**Ogro: uno de más.** `ja` donde iba `jae` da una vuelta extra. Revisá siempre el primer y el último valor.

**Ogro: el «mientras» que nunca entra.** Si la condición ya no se cumple de entrada, el cuerpo no se ejecuta ni
una vez. Si tiene que ejecutarse al menos una vez, es un «hasta que».

### Micro-misión R02-N06-P1 · El fuelle

```meta
lugar: La cadera del Gólem
personajes: Nova, Gheco
carta: Mientras | pregunta antes · se sale con el salto contrario · jmp para volver a preguntar
recompensa: xp 10, oro 10
```

#### Escena
El horno de la cadera necesita llegar a **8** de calor. Cada soplido del fuelle suma 3. Nova sopla **mientras** el calor sea menor que 8.

#### Gheco sugiere
Arriba de todo, la pregunta: `cmp calor, 8` y, si ya es **mayor o igual**, salir (`jae fin_mientras`). Al final del cuerpo, `jmp mientras` para volver a preguntar.

#### Desafío
Completá el salto de salida y el de vuelta.

#### Código inicial
```asm
.model small
.stack 100h
.data
calor db 0
.code
main proc
    mov ax, @data
    mov ds, ax

mientras:
    cmp calor, 8
    ___ fin_mientras
    add calor, 3
    ___ mientras
fin_mientras:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
[calor] = 9
```

#### Solución
```asm
.model small
.stack 100h
.data
calor db 0
.code
main proc
    mov ax, @data
    mov ds, ax

mientras:
    cmp calor, 8
    jae fin_mientras
    add calor, 3
    jmp mientras
fin_mientras:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Tres soplidos: 3, 6, 9. El horno ruge. —No sabía cuántas veces iba a soplar —dice Nova—. El Gólem preguntó cada vez.

#### Imagen
- Un horno pequeño de bronce con la boca encendida de luz naranja, en la cadera de un gólem.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) aprieta un fuelle de cuero y bronce.
- Gheco (gecko de luz cian con antiparras, chiquito) se calienta las patitas delante del horno.

### Micro-misión R02-N06-P2 · El fuelle que no termina

```meta
lugar: La cadera del Gólem
personajes: Nova, Gheco
criatura: ogre
carta: Bucle infinito | algo del cuerpo tiene que cambiar lo que mira la condición
recompensa: xp 15, oro 15
```

#### Escena
Nova vuelve a escribir el bucle del fuelle de memoria, ejecuta… y el Gólem se queda soplando para siempre. Un ogro, muerto de risa, se sienta a mirar.

#### Gheco sugiere
Ejecutá **paso a paso**: ¿qué cambia en cada vuelta? Si `calor` no sube nunca, la pregunta da siempre igual y el bucle no termina. Falta la orden que **sopla**.

#### Desafío
Tocá **Ejecutar** y mirá el aviso. Después agregá lo que falta para que el calor suba de a 3 y el bucle termine.

#### Código inicial
```asm
.model small
.stack 100h
.data
calor db 0
.code
main proc
    mov ax, @data
    mov ds, ax

mientras:
    cmp calor, 8
    jae fin_mientras
    jmp mientras
fin_mientras:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
[calor] = 9
```

#### Solución
```asm
.model small
.stack 100h
.data
calor db 0
.code
main proc
    mov ax, @data
    mov ds, ax

mientras:
    cmp calor, 8
    jae fin_mientras
    add calor, 3
    jmp mientras
fin_mientras:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El fuelle se detiene a tiempo. El ogro, aburrido, se va a buscar otro bucle donde reírse.

#### Imagen
- Un fuelle de cuero y bronce gastado, echando humo, con remiendos.
- Un ogro grandote y torpe sentado en el piso, con los codos en las rodillas, mirando divertido.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) frena el fuelle con las dos manos.
- Gheco (gecko de luz cian con antiparras, chiquito) mareado, con los ojitos en espiral.

### Micro-misión R02-N06-P3 · Los escalones

```meta
lugar: La cadera del Gólem
personajes: Nova, Gheco
criatura: ogre
carta: Uno de más | ja = mayor · jae = mayor o igual · probá el primer y el último valor
recompensa: xp 15, oro 15
```

#### Escena
Una escalera sube de la cadera a la cintura: **5** escalones. Nova los numera mientras sube, pero el ojo muestra **123456**: un escalón de más, que no existe. Un ogro lo subió y se cayó.

#### Gheco sugiere
Con `ja`, el bucle sigue también cuando el escalón ya es 5. Para salir apenas llega a 5, el salto tiene que ser **mayor o igual**.

#### Desafío
Tocá **Ejecutar** y mirá el escalón de más. Después arreglá el salto para que muestre `12345`.

#### Código inicial
```asm
.model small
.stack 100h
.data
escalon db 0
.code
main proc
    mov ax, @data
    mov ds, ax

subir:
    cmp escalon, 5
    ja  arriba
    inc escalon
    mov dl, escalon
    add dl, '0'
    mov ah, 02h
    int 21h
    jmp subir
arriba:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
12345
```

#### Solución
```asm
.model small
.stack 100h
.data
escalon db 0
.code
main proc
    mov ax, @data
    mov ds, ax

subir:
    cmp escalon, 5
    jae arriba
    inc escalon
    mov dl, escalon
    add dl, '0'
    mov ah, 02h
    int 21h
    jmp subir
arriba:

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Cinco escalones, justos. El ogro, sentado en el piso con un chichón, se rasca la cabeza.

#### Imagen
- Una escalera de bronce de cinco escalones que sube por el interior de un gólem, con un hueco de aire donde estaría un sexto.
- Un ogro grandote sentado en el piso al pie de la escalera, con un chichón en la cabeza.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) parada en el quinto escalón, mirando hacia abajo, preocupada.
- Gheco (gecko de luz cian con antiparras, chiquito) le alcanza al ogro una curita.

### Micro-misión R02-N06-P4 · Los golpes en la puerta

```meta
lugar: La cadera del Gólem
personajes: Nova, Gheco, Kira
carta: Hasta que | cuerpo primero · cmp + salto al final · se ejecuta al menos una vez · como do-while
recompensa: xp 15, oro 15
```

#### Escena
Kira golpea la puerta de la cadera para que le abran: cada **g** es un golpe, y la **x** quiere decir «basta». El Gólem tiene que contar los golpes **hasta que** llegue la x.

#### Gheco sugiere
El cuerpo va primero: leer una tecla y, si es `'g'`, sumar un golpe. Al final, la pregunta: si **no** es la `'x'`, volver a `hacer`.

#### Desafío
Completá la comparación del final y el salto de vuelta. Kira va a golpear `g`, `g`, `z`, `g` y `x`.

#### Código inicial
```asm
.model small
.stack 100h
.data
golpes db 0
t_tot  db 13, 10, 'Golpes: $'
.code
main proc
    mov ax, @data
    mov ds, ax

hacer:
    mov ah, 01h
    int 21h
    cmp al, 'g'
    jne no_golpe
    inc golpes
no_golpe:
    cmp al, ___
    ___ hacer

    lea dx, t_tot
    mov ah, 09h
    int 21h
    mov dl, golpes
    add dl, '0'
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
g
g
z
g
x
```

#### Salida esperada
```
ggzgx
Golpes: 3
```

#### Solución
```asm
.model small
.stack 100h
.data
golpes db 0
t_tot  db 13, 10, 'Golpes: $'
.code
main proc
    mov ax, @data
    mov ds, ax

hacer:
    mov ah, 01h
    int 21h
    cmp al, 'g'
    jne no_golpe
    inc golpes
no_golpe:
    cmp al, 'x'
    jne hacer

    lea dx, t_tot
    mov ah, 09h
    int 21h
    mov dl, golpes
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
Tres golpes, y la puerta se abre. Kira entra frotándose los nudillos. —La **z** fue sin querer —se excusa.

#### Imagen
- Una puerta redonda de bronce abriéndose en la cadera de un gólem gigante.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) entra frotándose los nudillos.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) la recibe del otro lado, contando con los dedos.
- Gheco (gecko de luz cian con antiparras, chiquito) con tres rayitas dibujadas en una pizarrita lisa.

### Micro-misión R02-N06-P5 · Las aes del hechizo

```meta
lugar: La cadera del Gólem
personajes: Nova, Gheco, Kira
carta: Leer hasta un terminador | hacer… hasta que la tecla sea '.' · contar las que cumplen algo
recompensa: xp 20, oro 20
```

#### Escena
Kira encontró un hechizo grabado en la cadera, pero solo funciona si se cuentan sus **aes**. Le va a dictar al Gólem las letras una por una, y un **punto** al final.

#### Gheco sugiere
Un «hasta que»: leer una tecla; si es `'a'`, sumar 1 a un contador; repetir hasta que la tecla sea `'.'`. Al final, mostrar el contador con `+ '0'`.

#### Desafío
Escribí las órdenes desde cero, donde dice `; tus órdenes`. Kira va a dictar `h`, `a`, `d`, `a`, `a` y `.`, y el ojo tiene que terminar diciendo `Aes: 3`.

#### Código inicial
```asm
.model small
.stack 100h
.data
aes   db 0
t_aes db 13, 10, 'Aes: $'
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

#### Entrada
```
h
a
d
a
a
.
```

#### Salida esperada
```
hadaa.
Aes: 3
```

#### Solución
```asm
.model small
.stack 100h
.data
aes   db 0
t_aes db 13, 10, 'Aes: $'
.code
main proc
    mov ax, @data
    mov ds, ax

leer:
    mov ah, 01h
    int 21h
    cmp al, 'a'
    jne no_a
    inc aes
no_a:
    cmp al, '.'
    jne leer

    lea dx, t_aes
    mov ah, 09h
    int 21h
    mov dl, aes
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
«Aes: 3». El hechizo se activa: las piernas del Gólem se calientan de golpe y, por primera vez en siglos, los dedos del pie se mueven. Abajo, en la taberna, se caen todos los vasos.

#### Imagen
- Los dedos de bronce de un pie gigante moviéndose, y una taberna de enanos entre ellos con vasos de madera volando por el aire.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) se asoma desde arriba, tapándose la boca, entre culpable y divertida.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) se ríe a carcajadas.
- Gheco (gecko de luz cian con antiparras, chiquito) atrapa un vaso en el aire.

### Prueba del sello

#### ¿Qué diferencia hay entre un «mientras» y un «hacer… hasta que»?
El «mientras» pregunta antes (puede no ejecutarse nunca); el «hasta que» pregunta al final (se ejecuta al menos una vez).

#### ¿Por qué un «mientras» puede no terminar nunca?
Porque nada en el cuerpo cambia lo que mira la condición.

#### En un «mientras calor < 8», ¿con qué salto se sale?
Con el contrario: `jae` (mayor o igual).

#### ¿Qué conviene usar para leer teclas hasta que el usuario escriba un punto?
Un «hacer… hasta que»: leer primero y preguntar al final.

## R02-N07 · Bits y máscaras: los interruptores de a uno

```meta
tipo: tema
criatura: goblin
padre: R02-N06
precio: 0
temas: prog.bits, maq.numeracion
```

### Crónica

En la cintura del Gólem hay un tablero con **ocho** interruptores chiquitos en fila, uno por cada bit de un cajón. Cada uno controla algo distinto: una luz, una válvula, un freno.

—Quiero prender **solo** el de la válvula —dice Nova—, sin tocar los demás.

Gheco saca de la cola un cartoncito con agujeros. —Para eso se usa una **máscara**: tapa los que no querés tocar y deja pasar el que sí.

### Objetivos

Operar **bit por bit** con `and`, `or`, `xor`, `not` y `test`; usar **máscaras** para apagar, prender, invertir o
consultar bits; escribir números en binario (`00100000b`); y multiplicar o dividir por 2 corriendo los bits con
`shl`, `shr` y `sar`.

### Antes de empezar

- Binario y hexadecimal (Clase 0).
- `cmp`, `je`, `jne` y `loop` (nodos anteriores).

### Explicación

#### Bit por bit
Estas órdenes comparan cada bit del destino con el de la fuente, de a uno:

| a | b | `and` | `or` | `xor` |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 |

`not` invierte todos los bits. Un número en binario se escribe con `b` al final: `00100000b`.

#### Las máscaras
| Para… | Orden | La máscara tiene… | Ejemplo |
|---|---|---|---|
| **apagar** bits | `and` | 0 en los bits a apagar | `and x, 11111101b` apaga el bit 1 |
| **prender** bits | `or` | 1 en los bits a prender | `or x, 00000100b` prende el bit 2 |
| **invertir** bits | `xor` | 1 en los bits a invertir | `xor x, 00000001b` |
| **consultar** un bit | `test` | 1 en el bit a mirar | `test x, 1` + `jz` / `jnz` |

Los bits se numeran desde la **derecha**, empezando por el 0. `test` es un `and` que no guarda el resultado: solo
prende ZF si el bit estaba en 0.

#### Mayúsculas y minúsculas
`'A'` es `01000001b` y `'a'` es `01100001b`: solo cambia el **bit 5** (que vale 32). `or al, 00100000b` pasa a
minúscula; `and al, 11011111b`, a mayúscula; `xor al, 00100000b` invierte.

#### Correr los bits
- `shl x, 1`: corre los bits a la izquierda (entra un 0 por la derecha; el que se cae va a **CF**): **× 2**.
- `shr x, 1`: los corre a la derecha: **÷ 2** sin signo. `sar x, 1` hace lo mismo con signo (conserva el bit de
  signo).
- En el 8086, para correr **más de un lugar**, la cantidad va en CL: `mov cl, 3` y `shl al, cl`.

> **Puente con otras lenguas.** `&`, `|`, `^`, `~`, `<<` y `>>` de C, Python, Java y JavaScript son exactamente
> estas órdenes. Los permisos de un archivo (`rwx`), los colores (`0xFF00FF`) y las teclas presionadas en un juego
> se guardan así: un bit por cosa.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
t_letra db 'K en binario: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_letra
    mov ah, 09h
    int 21h

    mov bl, 'K'
    mov cx, 8
bits:
    shl bl, 1            ; el bit más alto cae en CF
    mov dl, '0'
    jnc es_cero          ; jnc: salta si CF = 0
    mov dl, '1'
es_cero:
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
K en binario: 01001011
```

### ¿Para qué sirve?

Los bits están en todos lados: permisos de archivos, banderas de configuración, colores, compresión, gráficos,
protocolos de red. Y `shl`/`shr` son la forma más rápida de multiplicar y dividir por 2: los compiladores los
usan solos cuando escribís `x * 8`.

### Errores habituales

**Goblin: `shl` de más de un lugar.** `shl al, 3` no existe en el 8086:
```
main.asm(9) : Error A2030: Instruction or register not accepted in current CPU mode
```
`mov cl, 3` y `shl al, cl`.

**Ogro: la máscara al revés.** `and x, 00000100b` para «apagar el bit 2» apaga **todos los demás** y deja solo
ese. Para apagar, la máscara tiene 0 donde se apaga.

**Ogro: `test` y el salto equivocado.** `jz` salta si el bit es **0**; `jnz`, si es 1.

**Ogro: `shr` a un negativo.** `shr` mete ceros: −8 (`F8h`) pasa a 124. Para dividir con signo, `sar`.

### Micro-misión R02-N07-P1 · Apagar el freno

```meta
lugar: La cintura del Gólem
personajes: Nova, Gheco
carta: and | apaga bits · máscara con 0 donde se apaga y 1 en el resto
recompensa: xp 10, oro 10
```

#### Escena
El tablero de la cintura tiene prendidos tres interruptores: `00000111b`. El del **bit 1** es el freno de la pierna, y hay que **apagarlo** sin tocar los otros dos.

#### Gheco sugiere
`and` con una máscara que tenga **0** en el bit a apagar y **1** en todos los demás: lo que tiene 1 en la máscara queda como estaba. Los bits se cuentan desde la derecha, empezando en 0.

#### Desafío
Completá la máscara para que el tablero quede en `00000101b` (5).

#### Código inicial
```asm
.model small
.stack 100h
.data
tablero db 00000111b
.code
main proc
    mov ax, @data
    mov ds, ax

    and tablero, ___

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
[tablero] = 5
```

#### Solución
```asm
.model small
.stack 100h
.data
tablero db 00000111b
.code
main proc
    mov ax, @data
    mov ds, ax

    and tablero, 11111101b

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Clic: se apaga una sola lucecita, la del medio. La pierna del Gólem, sin freno, se balancea suave.

#### Imagen
- Un tablero de bronce con ocho interruptores chiquitos en fila, cada uno con una lucecita: la primera y la tercera de la derecha encendidas en cian, la del medio recién apagada.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) sostiene sobre el tablero un cartoncito con agujeros.
- Gheco (gecko de luz cian con antiparras, chiquito) mira por uno de los agujeros.

### Micro-misión R02-N07-P2 · La letra chiquita

```meta
lugar: La cintura del Gólem
personajes: Nova, Gheco
carta: or | prende bits · 'A' or 00100000b = 'a' · el bit 5 separa mayúsculas de minúsculas
recompensa: xp 15, oro 15
```

#### Escena
En el tablero hay grabada una **K** mayúscula, pero el hechizo de la cintura pide la **k** minúscula. Gheco recuerda que entre las dos hay **un solo** bit de diferencia.

#### Gheco sugiere
`'K'` y `'k'` solo difieren en el **bit 5**. Prendelo con `or` y una máscara que tenga un 1 solo ahí: `00100000b`.

#### Desafío
Completá la máscara para que AL pase de `'K'` a `'k'` y el ojo la muestre.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 'K'
    or  al, ___

    mov dl, al
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
k
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

    mov al, 'K'
    or  al, 00100000b

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
La K grabada se achica sola en el bronce. —Una mayúscula es una minúscula con un interruptor apagado —dice Nova, maravillada.

#### Imagen
- Una placa de bronce con dos rombos grabados, uno grande y uno chico, y una chispa cian saltando del grande al chico.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) toca la placa con un dedo.
- Gheco (gecko de luz cian con antiparras, chiquito) se achica a propósito, haciéndose bolita.

### Micro-misión R02-N07-P3 · ¿Par o impar? Con un bit

```meta
lugar: La cintura del Gólem
personajes: Nova, Gheco, Kira
carta: test | test x, 1 = mira el bit 0 · jz: estaba en 0 (par) · jnz: estaba en 1 (impar)
recompensa: xp 15, oro 15
```

#### Escena
Kira vuelve con su juego del par o impar. Esta vez Gheco tiene un truco: no hace falta dividir. Alcanza con mirar **un bit**.

#### Gheco sugiere
Todo número impar tiene el **bit 0** prendido. `test al, 1` lo consulta sin cambiar AL: si estaba en 0, se prende ZF y `jz` salta.

#### Desafío
Completá el `test` y el salto. Kira va a decir el `6`.

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

    test al, ___
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
6
```

#### Salida esperada
```
Un numero: 6
Es par.
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

    test al, 1
    jz  par
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
—¡Ni siquiera tuviste que restar el `'0'`! —se sorprende Kira. —El `'6'` también es par —explica Gheco—: su bit 0 está apagado igual.

#### Imagen
- Un tablero de bronce con ocho interruptores en fila; el de la derecha de todo, apagado, iluminado por una lupa cian.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) levanta seis dedos.
- Gheco (gecko de luz cian con antiparras, chiquito) sostiene la lupa.

### Micro-misión R02-N07-P4 · El goblin del corrimiento

```meta
lugar: La cintura del Gólem
personajes: Nova, Gheco
criatura: goblin
carta: shl con CL | shl x, 1 = x · 2 · para correr más lugares: mov cl, n + shl x, cl
recompensa: xp 15, oro 15
```

#### Escena
Para multiplicar la fuerza de la pierna por **8**, Nova corre los bits tres lugares: `shl al, 3`. Un goblin aparece gritando *«not accepted in current CPU mode»*.

#### Gheco sugiere
Correr 3 lugares a la izquierda es multiplicar por 2 × 2 × 2 = 8. Pero en el 8086, la cantidad (si es más de 1) va en **CL**: `mov cl, 3` y `shl al, cl`.

#### Desafío
Tocá **Ejecutar** para ver al goblin. Después arreglalo para que AL pase de 3 a **24**.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov al, 3
    shl al, 3

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
AL = 24
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

    mov al, 3
    mov cl, 3
    shl al, cl

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
La pierna se tensa con fuerza de 24. El goblin se va gruñendo: en un procesador más nuevo le habría ganado.

#### Imagen
- Un goblin verde y flaco, enojado, empujando una fila de bloquecitos de bronce que se corren hacia la izquierda.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) sostiene una palanquita con tres rayitas.
- Gheco (gecko de luz cian con antiparras, chiquito) se cae de un bloquecito que se corrió.

### Micro-misión R02-N07-P5 · El nombre en binario

```meta
lugar: La cintura del Gólem
personajes: Nova, Gheco
carta: Mostrar en binario | 8 vueltas · shl bl, 1 · el bit cae en CF · jnc elige '0' o '1'
recompensa: xp 20, oro 20
```

#### Escena
Nova quiere ver cómo se escribe **su** inicial en el idioma de los interruptores: la **N**, bit por bit.

#### Gheco sugiere
Un `loop` de 8 vueltas. En cada una, `shl bl, 1` empuja el bit más alto a **CF**. Si CF quedó en 0 (`jnc`), mostrás `'0'`; si no, `'1'`.

#### Desafío
Escribí las órdenes desde cero, donde dice `; tus órdenes`, para que el ojo muestre la N en binario.

#### Código inicial
```asm
.model small
.stack 100h
.data
texto db 'N = $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, texto
    mov ah, 09h
    int 21h

    mov bl, 'N'
    ; tus órdenes

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
N = 01001110
```

#### Solución
```asm
.model small
.stack 100h
.data
texto db 'N = $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, texto
    mov ah, 09h
    int 21h

    mov bl, 'N'
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

#### Al superarla
**01001110**. Los ocho interruptores de la cintura se acomodan solos en ese orden y la cintura del Gólem gira, por primera vez, de un lado al otro.

#### Imagen
- Un tablero de bronce con ocho interruptores en fila, cuatro encendidos en cian y cuatro apagados, alternados.
- La cintura de un gólem gigante girando, con engranajes en movimiento.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) con los brazos abiertos, girando con la cintura.
- Gheco (gecko de luz cian con antiparras, chiquito) agarrado a un interruptor encendido.

### Prueba del sello

#### ¿Qué orden y qué máscara apagan el bit 0 de AL?
`and al, 11111110b`.

#### ¿Qué diferencia hay entre `and` y `test`?
`test` hace el mismo `and` pero no guarda el resultado: solo cambia los interruptores.

#### ¿Qué hace `shl al, 1` con el número?
Lo multiplica por 2 (y el bit que se cae queda en CF).

#### ¿Qué bit separa las mayúsculas de las minúsculas?
El bit 5 (vale 32).

## R02-N08 · Arreglos e índices: muchos cajones, un nombre

```meta
tipo: tema
criatura: orc
padre: R02-N07
precio: 0
temas: col.arrays, col.matrices, maq.direcciones
```

### Crónica

En el muslo derecho del Gólem hay un **arsenal**: una fila de cajones con las armas de los antiguos guardianes, y al lado otra fila con el daño de cada una. Kira quiere saber cuál es la más débil, para no elegirla.

—Son muchas —dice Nova—. No voy a escribir una orden por cajón.

—No hace falta —dice Gheco—. Una palanca que **señale** el cajón, y un bucle que la vaya corriendo.

### Objetivos

Recorrer un **arreglo** con un puntero (`[si]`) o con un índice (`danio[si]`), saber cuánto avanzar en arreglos
de bytes y de words, buscar el mínimo guardando su **posición**, y ubicar un elemento en una **matriz** guardada
fila tras fila.

### Antes de empezar

- `offset`, `dup`, `nombre+1` y `byte ptr` (Dirección y contenido).
- `[si]` (La boca de bronce).
- `loop` (Repetir).

### Explicación

#### Un arreglo es una fila de cajones
```asm
armas   db 'E', 'A', 'B', 'L', 'D'    ; 5 bytes seguidos
danio   db 3, 5, 2, 7, 4
escudos dw 6, 9, 4                    ; 3 words: 6 bytes
```
`armas` es el **primer** cajón; el elemento `i` está en `armas + i`. En un arreglo de **words**, cada elemento
ocupa 2 cajones: el elemento `i` está en `escudos + 2*i`.

#### Recorrer con un puntero
```asm
    lea si, armas          ; SI señala el primero
    mov cx, 5
ver:
    mov dl, [si]           ; el cajón que señala SI
    ...
    inc si                 ; el siguiente (en words: add si, 2)
    loop ver
```

#### Recorrer con un índice
```asm
    mov si, 3
    mov al, danio[si]      ; el cajón danio + 3: AL = 7
```
Las dos formas valen; la del índice deja a mano la **posición**, útil para saber **dónde** está algo.

#### Las palancas que pueden señalar
Entre corchetes solo pueden ir **BX, SI, DI y BP**. Se pueden combinar: `[bx + si]`, `[bx + 2]`, `danio[si]`.

#### Matrices
Una matriz de 3 filas × 4 columnas se guarda **fila tras fila**. El elemento `[fila][col]` está en
`mapa + fila * 4 + col`. Al revés: si sabés la posición, dividila por 4: el cociente es la fila y el resto la
columna.

> **Puente con otras lenguas.** `danio[si]` es el `danio[i]` de C, Python o Java; `[si]` con `inc si` es recorrer
> con un puntero (`*p++` en C). Y la fórmula de la matriz es la que usa C por dentro con `mapa[fila][col]`.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
armas  db 'E', 'A', 'B', 'L', 'D'
danio  db 3, 5, 2, 7, 4
t_arm  db 'Armas: $'
t_tot  db 13, 10, 'Dano total: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_arm
    mov ah, 09h
    int 21h
    lea si, armas
    mov cx, 5
ver:
    mov dl, [si]
    mov ah, 02h
    int 21h
    inc si
    loop ver

    mov bl, 0
    mov si, 0
    mov cx, 5
sumar:
    add bl, danio[si]
    inc si
    loop sumar

    lea dx, t_tot
    mov ah, 09h
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
end main
```

### Salida esperada

```
Armas: EABLD
Dano total: 21
```

### ¿Para qué sirve?

Las listas de Python, los arrays de C y Java, los textos, las imágenes (una matriz de puntos) y los mapas de los
juegos son, por debajo, cajones seguidos y una palanca que los recorre. Entender esto explica por qué en C un
índice fuera de rango no avisa y rompe cosas lejos de donde ocurrió.

### Errores habituales

**Orco: el word recorrido de a 1.** `inc si` en un arreglo de words lee medio elemento y medio del siguiente. En
words: `add si, 2`.

**Orco: salirse del arreglo.** Con CX o la condición de fin mal puestos, el bucle lee (o escribe) los cajones que
siguen: las otras variables. El 8086 **no avisa**.

**Goblin: una palanca que no puede señalar.** `mov al, [ax]` o `[cx]`:
```
main.asm(11) : Error A2033: Must be index or base register
```
Usá BX, SI, DI o BP.

**Goblin: tamaño ambiguo.** `inc [si]`: ¿un cajón o dos?
```
main.asm(11) : Error A2182: Instruction operand must have size
```
`inc byte ptr [si]` o `inc word ptr [si]`.

### Micro-misión R02-N08-P1 · El cuarto cajón

```meta
lugar: El arsenal del muslo
personajes: Nova, Gheco
carta: Índice | danio[si] = el cajón danio + SI · el primero es el 0 · como danio[3]
recompensa: xp 10, oro 10
```

#### Escena
Kira quiere saber cuánto daño hace la **cuarta** arma del arsenal. Nova cuenta: primera, segunda, tercera, cuarta…

#### Gheco sugiere
El primer elemento está en el índice **0**. El cuarto, entonces, en el índice 3. Poné ese número en SI y leé `danio[si]`.

#### Desafío
Completá el índice para que AL quede con el daño de la cuarta arma.

#### Código inicial
```asm
.model small
.stack 100h
.data
danio db 3, 5, 2, 7, 4
.code
main proc
    mov ax, @data
    mov ds, ax

    mov si, ___
    mov al, danio[si]

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
AL = 7
```

#### Solución
```asm
.model small
.stack 100h
.data
danio db 3, 5, 2, 7, 4
.code
main proc
    mov ax, @data
    mov ds, ax

    mov si, 3
    mov al, danio[si]

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Siete de daño: la lanza. —El cuarto está en el **tres** —repite Nova—. Como la mochila: el primero es el cero.

#### Imagen
- Una fila de cinco cajones de bronce abiertos en un arsenal, cada uno con un arma distinta: una espada, un arco, un bastón, una lanza y una daga.
- La cuarta, la lanza, brilla con luz cian.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) señala la lanza.
- Gheco (gecko de luz cian con antiparras, chiquito) sentado en el primer cajón.

### Micro-misión R02-N08-P2 · El inventario

```meta
lugar: El arsenal del muslo
personajes: Nova, Gheco
carta: Puntero | lea si, arreglo · [si] = el cajón que señala · inc si = el siguiente
recompensa: xp 15, oro 15
```

#### Escena
Nova quiere que el ojo del Gólem muestre la inicial de cada arma del arsenal, una al lado de la otra.

#### Gheco sugiere
SI empieza señalando el primer cajón. En cada vuelta: mostrar lo que hay en `[si]` y correr SI al siguiente con `inc si`.

#### Desafío
Completá la lectura y el avance para que el ojo muestre `EABLD`.

#### Código inicial
```asm
.model small
.stack 100h
.data
armas db 'E', 'A', 'B', 'L', 'D'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, armas
    mov cx, 5
ver:
    mov dl, [___]
    mov ah, 02h
    int 21h
    inc ___
    loop ver

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
EABLD
```

#### Solución
```asm
.model small
.stack 100h
.data
armas db 'E', 'A', 'B', 'L', 'D'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, armas
    mov cx, 5
ver:
    mov dl, [si]
    mov ah, 02h
    int 21h
    inc si
    loop ver

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Espada, arco, bastón, lanza, daga. Kira las anota en su libreta. —Ahora quiero saber cuál pega menos —dice.

#### Imagen
- Un arsenal con cinco armas colgadas en fila en una pared de bronce, y un haz de luz cian que las recorre de izquierda a derecha.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) sigue el haz con el dedo.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) toma notas en una libreta cerrada, apoyada en la rodilla.
- Gheco (gecko de luz cian con antiparras, chiquito) montado sobre el haz de luz.

### Micro-misión R02-N08-P3 · Los escudos partidos

```meta
lugar: El arsenal del muslo
personajes: Nova, Gheco
criatura: orc
carta: Words | cada elemento ocupa 2 cajones · avanzar con add si, 2 · inc si lee medio y medio
recompensa: xp 15, oro 15
```

#### Escena
En el arsenal también hay escudos, con su resistencia guardada en **cajones dobles**: 6, 9 y 4. Nova suma las tres y el Gólem dice un número rarísimo. Un orco, del otro lado del arreglo, se relame.

#### Gheco sugiere
Los escudos son **words**: cada uno ocupa 2 cajones. Con `inc si`, SI avanza medio escudo y lee pedazos mezclados (y hasta se sale del arreglo). Hay que avanzar de a **2**.

#### Desafío
Ejecutá y mirá AX. Después arreglá el avance para que AX termine con la resistencia total: **19**.

#### Código inicial
```asm
.model small
.stack 100h
.data
escudos dw 6, 9, 4
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 0
    lea si, escudos
    mov cx, 3
sumar:
    add ax, [si]
    inc si
    loop sumar

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
AX = 19
```

#### Solución
```asm
.model small
.stack 100h
.data
escudos dw 6, 9, 4
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 0
    lea si, escudos
    mov cx, 3
sumar:
    add ax, [si]
    add si, 2
    loop sumar

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Diecinueve de resistencia, justos. El orco se queda sin cajones ajenos para morder y se va.

#### Imagen
- Tres escudos redondos de bronce colgados en fila, cada uno ocupando dos cajones de una pared.
- Un orco robusto asomándose al final de la fila, con cara de hambre.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) salta de escudo en escudo, de a dos cajones.
- Gheco (gecko de luz cian con antiparras, chiquito) se aferra a su espalda.

### Micro-misión R02-N08-P4 · Afilar todas

```meta
lugar: El arsenal del muslo
personajes: Nova, Gheco
criatura: goblin
carta: inc byte ptr [si] | [si] no tiene tamaño · byte ptr aclara que es un cajón
recompensa: xp 15, oro 15
```

#### Escena
Kira afila las cinco armas: cada una gana **1** de daño. Nova escribe `inc [si]` dentro del bucle y un goblin protesta: *«Instruction operand must have size»*.

#### Gheco sugiere
`[si]` es un cajón… ¿o dos? El Gólem no lo sabe. Con `byte ptr [si]` le aclarás que es uno.

#### Desafío
Tocá **Ejecutar** para ver al goblin. Después arreglá la orden para que cada daño suba 1.

#### Código inicial
```asm
.model small
.stack 100h
.data
danio db 3, 5, 2, 7, 4
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, danio
    mov cx, 5
afilar:
    inc [si]
    inc si
    loop afilar

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
[danio] = 4
[danio+2] = 3
[danio+4] = 5
```

#### Solución
```asm
.model small
.stack 100h
.data
danio db 3, 5, 2, 7, 4
.code
main proc
    mov ax, @data
    mov ds, ax

    lea si, danio
    mov cx, 5
afilar:
    inc byte ptr [si]
    inc si
    loop afilar

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Las cinco armas brillan, afiladas. El goblin se lleva una piedra de afilar de recuerdo, sin que nadie lo vea.

#### Imagen
- Cinco armas brillando en fila después de ser afiladas, con chispitas cian en los filos.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) pasa una piedra de afilar por la espada.
- Un goblin verde y flaco se escapa de puntillas con otra piedra de afilar bajo el brazo.
- Gheco (gecko de luz cian con antiparras, chiquito) señala al goblin, indignado.

### Micro-misión R02-N08-P5 · Al revés

```meta
lugar: El arsenal del muslo
personajes: Nova, Gheco
carta: Recorrer al revés | SI empieza en el último (n - 1) · dec si en cada vuelta
recompensa: xp 15, oro 15
```

#### Escena
Para devolver las armas a su lugar, Kira quiere recorrer el arsenal **desde la última hasta la primera**.

#### Gheco sugiere
Hay 5 armas: la última está en el índice **4**. Empezá SI ahí, mostrá `armas[si]` y **bajá** SI en cada vuelta.

#### Desafío
Completá el índice inicial y la orden que lo hace bajar, para que el ojo muestre `DLBAE`.

#### Código inicial
```asm
.model small
.stack 100h
.data
armas db 'E', 'A', 'B', 'L', 'D'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov si, ___
    mov cx, 5
ver:
    mov dl, armas[si]
    mov ah, 02h
    int 21h
    ___ si
    loop ver

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
DLBAE
```

#### Solución
```asm
.model small
.stack 100h
.data
armas db 'E', 'A', 'B', 'L', 'D'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov si, 4
    mov cx, 5
ver:
    mov dl, armas[si]
    mov ah, 02h
    int 21h
    dec si
    loop ver

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Daga, lanza, bastón, arco, espada: cada una vuelve a su gancho, en orden inverso. Gheco aplaude la prolijidad.

#### Imagen
- Un arsenal con cinco ganchos en una pared de bronce y armas volviendo a colgarse de derecha a izquierda.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) cuelga la espada en el primer gancho.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) le alcanza el arma siguiente.
- Gheco (gecko de luz cian con antiparras, chiquito) aplaude desde un gancho.

### Micro-misión R02-N08-P6 · La más débil

```meta
lugar: El arsenal del muslo
personajes: Nova, Gheco, Kira
carta: Mínimo | el primero es el mínimo provisorio · si alguno es menor (jb), se guarda él y su posición
recompensa: xp 20, oro 20
```

#### Escena
Por fin, la pregunta de Kira: ¿cuál es el arma **más débil**? El ojo tiene que mostrar su inicial y su daño.

#### Gheco sugiere
Guardá en BL el **daño mínimo** y en DI su **posición**. Empezá con el primero (BL = `danio[0]`, DI = 0). Recorré con SI desde 1: si `danio[si]` es **menor** que BL (`jb`), actualizá BL y DI. Al final, la letra es `armas[di]`.

#### Desafío
Escribí las órdenes desde cero, donde dice `; tus órdenes`, para que el ojo diga `Mas debil: B 2`.

#### Código inicial
```asm
.model small
.stack 100h
.data
armas  db 'E', 'A', 'B', 'L', 'D'
danio  db 3, 5, 2, 7, 4
titulo db 'Mas debil: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, titulo
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
Mas debil: B 2
```

#### Estado esperado
```
BL = 2
DI = 2
```

#### Solución
```asm
.model small
.stack 100h
.data
armas  db 'E', 'A', 'B', 'L', 'D'
danio  db 3, 5, 2, 7, 4
titulo db 'Mas debil: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, titulo
    mov ah, 09h
    int 21h

    mov bl, danio
    mov di, 0
    mov si, 1
    mov cx, 4
buscar:
    mov al, danio[si]
    cmp al, bl
    jae no_menor
    mov bl, al
    mov di, si
no_menor:
    inc si
    loop buscar

    mov dl, armas[di]
    mov ah, 02h
    int 21h
    mov dl, ' '
    int 21h
    mov dl, bl
    add dl, '0'
    int 21h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
«Mas debil: B 2». El bastón. Kira lo deja colgado y elige la lanza. Y en ese momento, desde la cadera, se oye un rugido: alguien está **dando vuelta** todos los interruptores del Gólem.

#### Imagen
- Un bastón de madera sencillo colgado solo en una pared de bronce, mientras una lanza brillante es descolgada.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) empuña la lanza, mirando hacia arriba, alerta.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) mira hacia el mismo lado, asustada.
- Gheco (gecko de luz cian con antiparras, chiquito) con la cola erizada.

### Prueba del sello

#### En `danio db 3, 5, 2, 7, 4`, ¿qué hay en `danio[2]`?
Un 2: el tercer elemento (el primero es el índice 0).

#### ¿Cuánto avanza SI en un arreglo de words?
De a 2 (`add si, 2`): cada elemento ocupa dos cajones.

#### ¿Qué palancas pueden ir entre corchetes?
BX, SI, DI y BP.

#### En una matriz de 3 × 4, ¿dónde está el elemento de la fila 2, columna 1?
En `mapa + 2 * 4 + 1`, es decir `mapa + 9`.

## R02-N09 · Jefe: el Ogro de las Banderas

```meta
tipo: jefe
criatura: ogre
padre: R02-N08
precio: 0
insignia: Sello del Ogro
insignia_descripcion: Venciste al Ogro de las Banderas: decidís y repetís sin que nadie te dé vuelta los interruptores.
usa: prog.condicionales, prog.bucles, col.arrays, maq.saltos, maq.banderas
temas: cal.depuracion
```

### Crónica

En la cadera del Gólem, sentado sobre el tablero de los interruptores, hay un ogro enorme: el **Ogro de las Banderas**. No rompe nada. No grita. Solo da vuelta un interruptor acá y otro allá, y espera.

—El programa corre —dice Gheco en voz baja—. Pero hace otra cosa. Así trabajan los ogros.

{mentor} habla despacio: —Para pararme sobre mis piernas necesito que cada decisión y cada vuelta sean exactas. Si él me cambia un interruptor, me caigo.

### Objetivos

Vencer al jefe de la rama: encontrar **errores de lógica** (los que no dan ningún mensaje) siguiendo el programa
**paso a paso** y mirando los interruptores; y armar programas que combinen decisiones, bucles y arreglos.

### Antes de empezar

Toda la rama: comparar y saltar, if/else, rangos, con signo y sin signo, `loop`, mientras y hasta que, bits y
arreglos.

### Explicación

#### Cómo se caza un ogro
Un ogro no deja mensaje: el programa termina, pero el resultado está mal. El método:

1. **Ejecutá paso a paso** y mirá la flechita: ¿entra donde esperabas? ¿salta donde esperabas?
2. **Mirá los interruptores** justo antes de cada salto: ¿son los del `cmp` que vos pensás, o algo los cambió en el
   medio?
3. **Probá los bordes**: el primero, el último, el cero, el negativo.
4. **Cambiá una sola cosa** por vez y volvé a ejecutar.

#### Los ogros más comunes de esta rama
| Ogro | Pista |
|---|---|
| Las banderas pisadas | entre el `cmp` y el salto hay un `inc`, `dec`, `add` o `sub` |
| El signo equivocado | `ja`/`jb` con números negativos (o `jg`/`jl` con cantidades) |
| Uno de más o de menos | `ja` donde iba `jae`, o CX con un número equivocado |
| CX pisado | un `mov cx` o `loop` adentro del cuerpo de otro `loop` |

> **Puente con otras lenguas.** El «paso a paso» del tablero es el **depurador** de cualquier entorno (el *debugger*
> de VS Code, de PyCharm, `gdb` en C): se ejecuta de a una línea mirando cómo cambian las variables. Es la
> herramienta más poderosa para cazar ogros en cualquier lenguaje.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
ventas  dw 4, 7, 6, 2, 9, 5, 8
t_dias  db 'Dias de mas de 5: $'
.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, t_dias
    mov ah, 09h
    int 21h

    mov bl, 0
    lea si, ventas
    mov cx, 7
contar:
    cmp word ptr [si], 5
    jbe no_cuenta
    inc bl
no_cuenta:
    add si, 2
    loop contar

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

### Salida esperada

```
Dias de mas de 5: 4
```

### ¿Para qué sirve?

Los errores de lógica son los más caros de cualquier programa: el código corre, nadie se entera, y el resultado
está mal. Aprender a buscarlos con método (paso a paso, mirando el estado, probando los bordes) es lo que separa
a un programador que adivina de uno que encuentra.

### Errores habituales

**Ogro: las banderas pisadas.** Un `inc` entre el `cmp` y el salto: el salto mira el `inc`, no el `cmp`.

**Ogro: el signo equivocado.** `jb` para contar temperaturas bajo cero: −2 (`FEh`) no es menor que 0 sin signo.

**Ogro: CX pisado.** Un `mov cx` adentro de un bucle con `loop` lo reinicia en cada vuelta.

### Micro-misión R02-N09-P1 · El interruptor pisado

```meta
lugar: La cadera del Gólem
personajes: Nova, Gheco
criatura: ogre
carta: Banderas pisadas | entre el cmp y el salto no va ninguna cuenta · mov y lea sí pueden ir
recompensa: xp 20, oro 20
```

#### Escena
El Ogro de las Banderas se sienta al lado del primer programa: cuenta cuántas pociones hay **iguales a 3** en el estante. Hay dos, pero el Gólem dice otra cosa. El ogro sonríe.

#### Gheco sugiere
Ejecutá **paso a paso** y mirá ZF justo antes del `je`. El `inc si` está entre el `cmp` y el salto, y cambia los interruptores. Movelo a otro lugar del bucle.

#### Desafío
Ejecutá, mirá BL y encontrá al ogro. Arreglá el programa para que BL cuente bien: **2**.

#### Código inicial
```asm
.model small
.stack 100h
.data
estante db 3, 1, 3, 5
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bl, 0
    mov si, 0
    mov cx, 4
contar:
    cmp estante[si], 3
    inc si
    jne no_es
    inc bl
no_es:
    loop contar

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
estante db 3, 1, 3, 5
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bl, 0
    mov si, 0
    mov cx, 4
contar:
    cmp estante[si], 3
    jne no_es
    inc bl
no_es:
    inc si
    loop contar

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El Ogro de las Banderas pierde la sonrisa. Da vuelta otro interruptor, más lejos, y espera.

#### Imagen
- Un ogro enorme y robusto sentado sobre un tablero de interruptores de bronce, con un dedo sobre uno, sonriendo con malicia.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) lo enfrenta con una lupa de luz cian en la mano.
- Gheco (gecko de luz cian con antiparras, chiquito) sobre el hombro de Nova, desafiante.

### Micro-misión R02-N09-P2 · Las noches heladas

```meta
lugar: La cadera del Gólem
personajes: Nova, Gheco
criatura: ogre
carta: Signo | temperaturas, saldos: jl y jg · cantidades y letras: jb y ja
recompensa: xp 20, oro 20
```

#### Escena
El segundo programa cuenta cuántas noches de la semana hizo **menos de 0** grados. Fueron tres, pero el Gólem dice cero. El ogro silba, mirando para otro lado.

#### Gheco sugiere
Las temperaturas pueden ser negativas. ¿Qué salto está usando para «menor»? Acordate: `jb` mira sin signo, y para él −2 es 254.

#### Desafío
Encontrá al ogro y arreglá el salto para que BL cuente bien: **3**.

#### Código inicial
```asm
.model small
.stack 100h
.data
noches db 4, -2, 0, -5, 3, -1, 2
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bl, 0
    mov si, 0
    mov cx, 7
contar:
    cmp noches[si], 0
    jb  helada
    jmp sigue
helada:
    inc bl
sigue:
    inc si
    loop contar

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
BL = 3
```

#### Solución
```asm
.model small
.stack 100h
.data
noches db 4, -2, 0, -5, 3, -1, 2
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bl, 0
    mov si, 0
    mov cx, 7
contar:
    cmp noches[si], 0
    jl  helada
    jmp sigue
helada:
    inc bl
sigue:
    inc si
    loop contar

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Tres noches heladas. El ogro gruñe: ya no le quedan muchos interruptores para dar vuelta.

#### Imagen
- Una fila de siete termómetros de bronce chiquitos; tres con escarcha y la columna cian muy baja.
- El ogro enorme con los brazos cruzados, de mal humor.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) señala los tres termómetros con escarcha.
- Gheco (gecko de luz cian con antiparras, chiquito) con bufanda, tiritando.

### Micro-misión R02-N09-P3 · La muralla que no crece

```meta
lugar: La cadera del Gólem
personajes: Nova, Gheco
criatura: ogre
carta: CX pisado | un loop adentro de otro loop comparte CX · el de afuera cuenta con otra palanca
recompensa: xp 20, oro 20
```

#### Escena
El tercer programa tendría que levantar una muralla de **2** filas de **3** ladrillos, pero el Gólem se queda dando vueltas para siempre. El ogro se estira, cómodo: este truco le encanta.

#### Gheco sugiere
Los dos bucles usan `loop`, y los dos cuentan con CX. Cuando termina el de adentro, CX vale 0, y el `loop filas` lo pasa a 65535… La fila de afuera tiene que contar con **otra palanca**, con `dec` y `jnz`.

#### Desafío
Tocá **Ejecutar** y mirá el aviso. Después arreglá el bucle de afuera para que use BL y la muralla salga bien.

#### Código inicial
```asm
.model small
.stack 100h
.data
salto db 13, 10, '$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov cx, 2
filas:
    mov cx, 3
ladrillos:
    mov dl, '#'
    mov ah, 02h
    int 21h
    loop ladrillos
    lea dx, salto
    mov ah, 09h
    int 21h
    loop filas

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Salida esperada
```
###
###
```

#### Solución
```asm
.model small
.stack 100h
.data
salto db 13, 10, '$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bl, 2
filas:
    mov cx, 3
ladrillos:
    mov dl, '#'
    mov ah, 02h
    int 21h
    loop ladrillos
    lea dx, salto
    mov ah, 09h
    int 21h
    dec bl
    jnz filas

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Dos filas de tres. El ogro se pone de pie, furioso: es la primera vez que alguien le gana tres veces seguidas.

#### Imagen
- Una muralla chica de ladrillos de bronce, dos filas de tres, perfecta.
- El ogro enorme poniéndose de pie, furioso, con los puños cerrados.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) parada detrás de la muralla, firme.
- Gheco (gecko de luz cian con antiparras, chiquito) se esconde detrás de un ladrillo.

### Micro-misión R02-N09-P4 · La suma de la piedra

```meta
lugar: La cadera del Gólem
personajes: Nova, Gheco, Kira, Axón
criatura: ogre
carta: Todo junto | hasta que '.' · validar el rango · acumular · par o impar con test · dos cifras
recompensa: xp 30, oro 30
```

#### Escena
El ogro juega su última carta: una **piedra** con un acertijo. —Te dicto números y letras mezclados, hasta un punto. Sumá **solo los dígitos**, decime la suma y si es **par** o **impar**. Si te equivocás, me quedo con tus piernas.

Kira se pone al lado de Nova. —Yo te dicto —le dice—. Vos no te equivoques.

#### Gheco sugiere
Un «hasta que» con la `01h` hasta el `'.'`. Adentro: si la tecla es un dígito (entre `'0'` y `'9'`), restale `'0'` y sumala a BL; si no, ignorala. Al final: mostrá BL en dos cifras (guardá antes una copia, porque el `div` la rompe) y usá `test` con el bit 0 para elegir «par» o «impar».

#### Desafío
Escribí las órdenes desde cero, donde dice `; tus órdenes`. Kira va a dictar `3`, `x`, `5`, `8` y `.`.

#### Código inicial
```asm
.model small
.stack 100h
.data
t_suma  db 13, 10, 'Suma: $'
t_par   db ', par.$'
t_impar db ', impar.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bl, 0
    ; tus órdenes

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Entrada
```
3
x
5
8
.
```

#### Salida esperada
```
3x58.
Suma: 16, par.
```

#### Solución
```asm
.model small
.stack 100h
.data
t_suma  db 13, 10, 'Suma: $'
t_par   db ', par.$'
t_impar db ', impar.$'
.code
main proc
    mov ax, @data
    mov ds, ax

    mov bl, 0
leer:
    mov ah, 01h
    int 21h
    cmp al, '.'
    je  listo
    cmp al, '0'
    jb  leer
    cmp al, '9'
    ja  leer
    sub al, '0'
    add bl, al
    jmp leer
listo:

    lea dx, t_suma
    mov ah, 09h
    int 21h
    mov bh, bl           ; una copia para el par o impar
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

    test bh, 1
    jz  es_par
    lea dx, t_impar
    jmp mostrar
es_par:
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
«Suma: 16, par.» La piedra se parte en dos. El Ogro de las Banderas se queda mirando los pedazos un rato largo, y después, por primera vez, se ríe de verdad: una carcajada enorme, sin malicia. —Bien jugado, chispita —dice, y se va caminando por el pasillo de las compuertas.

Entonces el Gólem tiembla de pies a cabeza. Las rodillas se doblan, los pies se apoyan, la cintura gira… y {mentor} **se pone de pie**. Desde arriba, en las Forjas, se oyen gritos de asombro.

—Todavía no camino —dice el Gólem—. Para caminar tengo que acordarme de **dónde estaba** a cada paso.

#### Imagen
- Un gólem de bronce gigante poniéndose de pie por primera vez en una caverna enorme, con polvo y piedras cayendo de sus hombros.
- En su pecho abierto se ve una lucecita cian: Nova, adentro.
- Abajo, un ogro enorme se aleja riendo, de espaldas.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) y Gheco (gecko de luz cian con antiparras, chiquito) miran hacia arriba, boquiabiertos, desde el piso.

### Prueba del sello

#### ¿Qué es un error de lógica y cómo se encuentra?
Un programa que corre pero da otro resultado. Se encuentra ejecutando paso a paso, mirando registros e interruptores y probando los bordes.

#### ¿Qué pasa si se pone un `inc` entre un `cmp` y su salto?
El salto mira los interruptores del `inc`, no los del `cmp`.

#### ¿Con qué salto se cuentan las temperaturas bajo cero?
Con `jl` (menor con signo).

#### ¿Por qué el bucle de afuera no puede usar `loop` si el de adentro también lo usa?
Porque comparten CX: el de adentro lo deja en 0 y rompe la cuenta del de afuera.
