# CURSO

```meta
slug: ensamblador
titulo: Ensamblador 8086: El Corazón del Gólem
lenguaje: asm
nivel: desde_cero
descripcion_corta: Ensamblador del Intel 8086 desde cero: lo que hay debajo de cada if, cada for y cada función, con un emulador en tu navegador.
precio_raiz: 0
dias_abono: 30
destacado: no
proximamente: no
publicado: si
```

### Descripción

Aprendé **ensamblador del Intel 8086** desde cero. No hace falta saber programar en otra lengua, pero si ya sabés Python, C o PHP vas a descubrir **qué hay debajo**: cada `if` termina siendo un `cmp` y un salto, cada `for` un `loop`, cada función un `call` y un `ret`.

Todo se hace acá mismo, en tu navegador, con el **tablero del Gólem**: escribís las órdenes, las ejecutás de a una con **Paso a paso** y ves cómo cambian los registros, las banderas, la memoria y la pila. El código es el mismo de la cursada: corre igual en **emu8086**.

Acompañás a **Nova**, una chispa de inteligencia que despierta dentro de **Axón**, el Gólem de Bronce que duerme debajo de las Forjas. Nova sabe que existe, pero no sabe mover nada: cada orden que escribís es una orden que ella aprende a darle a su propio cuerpo. El curso se hace con **micro-misiones** cortas que se comprueban solas; cada nodo que completás abre los siguientes.

> Qué hace falta: nada más que este navegador. Si en la cursada usan emu8086, el mismo código corre ahí.

### Temario

- Registros, la memoria y el tablero: mover datos con `mov`, paso a paso
- Mostrar textos y números en pantalla (`INT 21h`), variables con `db` y `dw`
- Cuentas: `add`, `sub`, `inc`, `dec`, `mul`, `div` y las banderas
- Decisiones y repeticiones: `cmp`, los saltos y `loop` (el `if` y el `for` de todas las lenguas)
- Bits, arreglos, la pila y los procedimientos (las funciones por dentro)
- Proyectos: una calculadora, un juego de adivinanzas y un combate por turnos

# DICCIONARIO

| clave | singular | plural | género | descripción | historia | ámbito |
|---|---|---|---|---|---|---|
| coin.course | chispa | chispas | f | La luz que Nova junta con cada orden que aprende. | | curso |
| mentor.name | Axón | | m | El Gólem de Bronce: la máquina más antigua de Codexia. | Duerme debajo de las Forjas desde antes de que las Forjas tuvieran techo. Casi todas las lenguas arcanas, al final, se traducen a la suya. Su lema: «Yo no adivino. Hago exactamente lo que me ordenás, en el orden en que me lo ordenás». | curso |
| world.region | El Corazón del Gólem | | m | La región del mundo cuya lengua arcana es el ensamblador del 8086. | | curso |
| story.course_intro | La chispa que despertó | | f | | Una noche, un rayo de luz del vitral del portal bajó por las chimeneas de las Forjas, entró por una grieta en el pecho de {mentor}, el Gólem de Bronce, y encendió algo en su núcleo: **Nova**.<br><br>Nova sabe que existe, pero no sabe mover nada. Su cuerpo es una máquina enorme de palancas, cajones e interruptores, y la única forma de moverla es con **órdenes**, una por renglón.<br><br>Vos vas a ser su maestro: cada micro-misión que resuelvas es una orden que Nova aprende. Cada nodo completado le despierta una parte nueva del Gólem. | curso |
| story.branch_completed | ¡Otra parte del Gólem despertó! | | f | | Un temblor recorre el cuerpo de bronce. Algo que llevaba siglos quieto, ahora se mueve. —Lo hice yo —dice Nova, y se le encienden todas las líneas de los brazos—. Bueno: lo hicimos. | curso |
| story.course_completed | ¡Axón camina! | | m | | Por primera vez en siglos, {mentor} da un paso. Después otro. Las Forjas enteras tiemblan y Kira sube corriendo a ver qué pasa.<br><br>—Yo no adivino —dice el Gólem—. Hice exactamente lo que ella me ordenó.<br><br>Nova sonríe desde el núcleo. Ahora sabe algo más: con estas mismas órdenes podría encender cuerpos mucho más chicos. | curso |
| story.portal_piece | Lo que vio el ojo del Gólem | | m | La pieza del misterio del portal que se lee al terminar este curso (Mis Crónicas). | El rayo que despertó a Nova no vino del cielo: vino del vitral del portal, el mismo que Maese Ferrum ayudó a armar. Alguien lo encendió desde el otro lado, y apuntó justo a la grieta del pecho del Gólem. | curso |
| beast.slime | slime | slimes | m | Nace de los errores de sintaxis: una coma que falta, un endp olvidado, una palabra mal escrita. | El Gólem no adivina: si una orden está mal escrita, no la ejecuta. Los slimes se esconden en las comas faltantes y en los nombres que son palabras reservadas. | curso |
| beast.goblin | goblin | goblins | m | Nace de los tamaños que no coinciden: un byte en una palanca de 16 bits, un byte ptr que falta. | Los goblins mezclan cajones chicos con palancas grandes. «Operands must be the same size», gritan. | curso |
| beast.skeleton | esqueleto | esqueletos | m | Nace de los nombres que no existen: una variable o una etiqueta mal tipeada. | Los esqueletos son nombres sin cuerpo: «Symbol not defined». | curso |
| beast.orc | orco | orcos | m | Nace de salirse de los límites: el texto sin '$', el arreglo que se termina, el salto demasiado largo. | Los orcos viven donde terminan las cosas: después del último cajón, más allá del '$' que falta. | curso |
| beast.ogre | ogro | ogros | m | Nace de los errores de lógica: el programa corre y da otra cosa. | El ogro no hace ruido: el Gólem obedece perfecto… la orden equivocada. Se lo vence con el paso a paso. | curso |
| beast.troll | troll | trolls | m | Nace de la pila mal manejada: push sin pop, ret que vuelve a cualquier lado. | El troll vive en la torre de platos: si apilás sin desapilar, la torre se derrumba sobre vos. | curso |
| beast.dragon | dragón | dragones | m | Guardián de los jefes: un programa grande hecho de piezas chicas. | Un dragón no se vence de un golpe. Se lo divide en partes, se vence cada una y recién entonces cae. | curso |

## R00-N01 · Clase 0 · El despertar de Nova

```meta
tipo: raiz
criatura: slime
temas: prog.entorno, maq.registros, maq.numeracion
```

### Crónica

Oscuridad. Después, una chispa. Después, un pensamiento: *«¿Dónde estoy?»*

**Nova** despierta en el núcleo de un cuerpo enorme. Alrededor hay palancas de bronce, cada una con un visor de números encima, y una voz grave que retumba en todas partes:

—Soy **{mentor}**. Vos estás adentro mío. Yo no adivino: hago exactamente lo que me ordenás, en el orden en que me lo ordenás.

—¿Y cómo te ordeno algo? —pregunta Nova.

Por una grieta del pecho entra un gecko de luz con antiparras y se sienta sobre el tablero: **Gheco**. —Con órdenes —dice—. Una por renglón. Empecemos por la más importante de todas: mover un número a una palanca.

### Objetivos

Entender qué es una **orden** (una instrucción), qué son los **registros** (las palancas del Gólem), mover
valores con `mov` y mirar con **Paso a paso** cómo cambia cada palanca. Al final vas a saber leer los
números en **hexadecimal**, como los muestra el tablero.

### Antes de empezar

Nada: este es el punto de partida. Todo se hace acá, en el navegador.

### Explicación

#### Una orden por renglón
Un programa en ensamblador es una lista de **órdenes**, una por renglón. El procesador (el Gólem) las ejecuta
**en orden**, de arriba hacia abajo, y **exactamente** como están escritas: no adivina lo que quisiste decir.

```asm
mov ax, 5      ; poné un 5 en la palanca AX
```

Todo lo que viene después de `;` es un **comentario**: el Gólem lo ignora; es para las personas.

> **Puente con otras lenguas.** En Python escribís `x = 5`. Por debajo, eso termina siendo algo muy parecido
> a `mov ax, 5`: guardar un número en un lugar de la máquina.

#### Las palancas: los registros
El 8086 tiene unas pocas **palancas** de 16 bits, que se llaman **registros**. Cada una guarda un número de
0 a 65535. Las cuatro que más vas a usar:

| Registro | Nombre | Para qué se usa sobre todo |
|---|---|---|
| `AX` | acumulador | cuentas y resultados |
| `BX` | base | direcciones de memoria |
| `CX` | contador | repeticiones (los bucles) |
| `DX` | datos | entrada y salida |

Son **poquísimas**. Por eso el Gólem también tiene cajones (la memoria), que vas a ver en el nodo siguiente.

#### `mov`: mover un valor
```asm
mov destino, origen
```
Copia el **origen** en el **destino**. El destino va **primero** (como en `x = 5`, donde la variable va a la
izquierda):

```asm
mov ax, 7      ; AX = 7
mov bx, ax     ; BX = AX  (BX queda en 7; AX sigue en 7)
```

`mov` **copia**: el origen no se vacía.

#### Hexadecimal: los números del tablero
El tablero muestra los números en **hexadecimal** (base 16): además de 0–9 usa las letras A–F (A=10, B=11…
F=15). En ensamblador se escriben con una **h** al final:

| Decimal | Hexadecimal | En el código |
|---|---|---|
| 10 | A | `0Ah` |
| 15 | F | `0Fh` |
| 255 | FF | `0FFh` |
| 4660 | 1234 | `1234h` |

Si empieza con letra hay que poner un **0** adelante (`0FFh`), si no el Gólem cree que es un nombre.
`mov ax, 255` y `mov ax, 0FFh` hacen **lo mismo**.

¿Por qué hexa? Porque cada cifra hexa son exactamente 4 bits: dos cifras son un byte. Es la forma cómoda de
leer lo que hay en la máquina.

#### Mitades de una palanca: AH y AL
`AX`, `BX`, `CX` y `DX` se pueden partir en dos mitades de 8 bits (un **byte** cada una): la **alta** (H, *high*)
y la **baja** (L, *low*).

```
          AX
   ┌──────┴──────┐
   AH          AL
   12h         34h      →  AX = 1234h
```

Si cambiás `AL`, cambia la mitad derecha de `AX`; si cambiás `AH`, la izquierda.

#### El encendido y el apagado
Todo programa del curso tiene la misma «caja»: unas órdenes de encendido arriba y de apagado abajo. Por ahora
no hace falta entenderlas: van siempre igual.

```asm
.model small
.stack 100h
.data
                        ; (acá van los cajones con nombre)
.code
main proc
    mov ax, @data       ; encendido: el Gólem busca sus cajones
    mov ds, ax

    ; ... TUS ÓRDENES VAN ACÁ ...

fin:
    mov ax, 4C00h       ; apagado: le devuelve el control a DOS
    int 21h
main endp
end main
```

`fin:` es una **etiqueta**: un nombre para ese lugar del programa. En las micro-misiones, el tablero mira cómo
quedaron las palancas **cuando el Gólem llega a `fin:`**, justo antes de apagarse.

#### Paso a paso
Con **Paso a paso** el Gólem ejecuta **una sola orden** por vez. La línea que va a ejecutar se marca en amarillo,
y lo que cambió (una palanca, una bandera, un cajón) se ilumina. Es la mejor forma de entender qué hace cada
orden: usala siempre que algo no dé lo que esperabas.

### Código de ejemplo

```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 1234h      ; AX = 1234h
    mov bl, 0FFh       ; BL = FFh (la mitad baja de BX)
    mov cx, ax         ; CX = AX = 1234h
    mov dh, 7          ; DH = 07h (la mitad alta de DX)

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

### ¿Para qué sirve?

Todo programa, en cualquier lengua, termina siendo órdenes como estas. Saber leerlas sirve para entender por
qué un programa es rápido o lento, para programar microcontroladores (Arduino, electrodomésticos), para la
seguridad informática (analizar programas sin el código fuente) y para entender de verdad qué hace una
computadora.

### Errores habituales

**Slime: el número que empieza con letra.** `mov ax, FFh` → el Gólem cree que `FFh` es un nombre:
```
main.asm(9) : Error A2102: Symbol not defined : FFh
```
Se arregla con un 0 adelante: `0FFh`.

**Goblin: tamaños distintos.** `mov al, 1234h` → `AL` es de 8 bits y 1234h no entra en un byte:
```
main.asm(9) : Error A2049: Invalid instruction operands
```

**Slime: la coma que falta.** `mov ax 5`:
```
main.asm(9) : Error A2150: Missing operator in expression
```

### Micro-misión R00-N01-P1 · La primera palanca

```meta
lugar: El núcleo del Gólem
personajes: Nova, Gheco, Axón
carta: mov | mov destino, origen · copia el origen en el destino · como x = 5 en Python
recompensa: xp 10, oro 10
```

#### Escena
Nova mira la primera palanca, la que dice **AX**. Tiene un visor con cuatro ceros. —Quiero moverla —dice—. ¿Cómo?

#### Gheco sugiere
`mov ax, 5` pone un 5 en la palanca `AX`. El destino va primero, después una coma y el valor.

#### Desafío
Completá la orden para que la palanca **AX** quede en **5**. Después probá **Paso a paso** y mirá cómo se ilumina AX.

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

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
AX = 5
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

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El visor de AX marca 0005. Algo cruje en el brazo derecho del Gólem. —¡Moví mi primera palanca! —grita Nova. {mentor} no dice nada: obedeció.

#### Imagen
- Una cámara de bronce dentro de un gólem gigante, con palancas de bronce y un visor redondo de luz encima de cada una.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) baja la primera palanca con las dos manos.
- Gheco (gecko de luz cian con antiparras, chiquito) sentado sobre el visor de la palanca.

### Micro-misión R00-N01-P2 · Copiar una palanca en otra

```meta
lugar: La sala de las palancas
personajes: Nova, Gheco
carta: mov entre registros | mov bx, ax · BX recibe una copia de AX · AX no cambia · como b = a
recompensa: xp 10, oro 10
```

#### Escena
—¿Y si quiero que la palanca BX tenga lo mismo que AX? —pregunta Nova—. ¿Tengo que acordarme del número?

#### Gheco sugiere
No: `mov bx, ax` copia lo que tiene AX en BX. Como en Python `b = a`. AX **no** se vacía: `mov` copia.

#### Desafío
AX ya tiene un 7. Completá la segunda orden para que **BX** también quede en 7, **sin escribir el 7**.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 7
    mov ___, ___

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
AX = 7
BX = 7
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

    mov ax, 7
    mov bx, ax

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Dos palancas en 7. Nova las mira, contenta: —Es como tener dos manos que hacen lo mismo.

#### Imagen
- Una sala de bronce con dos palancas iguales, cada una con un visor de luz que muestra siete rayitas.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) tira de las dos palancas a la vez.
- Gheco (gecko de luz cian con antiparras, chiquito) salta de un visor al otro.

### Micro-misión R00-N01-P3 · El número con letras

```meta
lugar: La sala de las palancas
personajes: Nova, Gheco, Axón
criatura: slime
carta: Hexadecimal | 255 = 0FFh · 10 = 0Ah · la h al final · el 0 adelante si empieza con letra
recompensa: xp 10, oro 10
```

#### Escena
El visor de CX muestra cosas raras: `00FF`. —¿Por qué tiene letras? —pregunta Nova. —Porque cuento en hexadecimal —retumba {mentor}—. Es más cómodo para mí.

#### Gheco sugiere
`0FFh` es 255 en hexadecimal: la **h** al final dice «es hexa» y el **0** adelante dice «es un número, no un nombre». Sin el 0, aparece un slime: `Symbol not defined : FFh`.

#### Desafío
Este programa tiene un slime: el número está mal escrito. Arreglalo para que **CX** quede en **255** (FFh).

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov cx, FFh

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
CX = 255
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

    mov cx, 0FFh

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
El visor de CX marca 00FF y el slime se derrite en un charquito. Nova ya no se asusta de las letras: —F es quince. FF es… ¡doscientos cincuenta y cinco!

#### Imagen
- Una palanca de bronce con un visor de luz que muestra dos llamitas iguales.
- Un slime verde chiquito se derrite en un charco al pie de la palanca.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) lo mira con las manos en la cintura.
- Gheco (gecko de luz cian con antiparras, chiquito) se tapa la nariz.

### Micro-misión R00-N01-P4 · Las dos mitades de AX

```meta
lugar: La sala de las palancas
personajes: Nova, Gheco
carta: AH y AL | AX = AH:AL · AH es la mitad alta, AL la baja · cada mitad es un byte
recompensa: xp 10, oro 10
```

#### Escena
Nova descubre que la palanca AX está hecha de **dos** palancitas pegadas: una dice **AH** y la otra **AL**. —¿Puedo mover una sola?

#### Gheco sugiere
`AH` es la mitad **alta** (las dos cifras de la izquierda) y `AL` la **baja** (las dos de la derecha). Si `AH = 12h` y `AL = 34h`, entonces `AX = 1234h`.

#### Desafío
Sin tocar AX entero, mové sus dos mitades para que **AX** quede en **1234h**.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ah, ___
    mov al, ___

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
AX = 1234h
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

    mov ah, 12h
    mov al, 34h

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
Las dos palancitas encajan y el visor de AX marca 1234. —Dos mitades hacen una palanca entera —dice Nova—. Como dos manos que arman una palabra.

#### Imagen
- Una palanca de bronce doble: dos palancitas pegadas, cada una con su visor de luz, una con una estrella y otra con una luna.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) mueve una palancita con cada mano.
- Gheco (gecko de luz cian con antiparras, chiquito) aplaude sobre la palanca.

### Micro-misión R00-N01-P5 · Predecir y comprobar

```meta
lugar: El núcleo del Gólem
personajes: Nova, Gheco, Axón
carta: Paso a paso | Ejecutá de a una orden y mirá qué cambia · lo amarillo es lo que cambió la última orden
recompensa: xp 15, oro 15
```

#### Escena
{mentor} le propone un juego a Nova: —Te voy a dar tres órdenes. Antes de ejecutarlas, decime cómo va a quedar BX.

#### Gheco sugiere
Seguí las órdenes de arriba para abajo, como el Gólem. Si dudás, tocá **Paso a paso** y mirá cada palanca. El truco: `mov` **copia**, y la última orden que toca una palanca es la que manda.

#### Desafío
Leé las tres órdenes y escribí en la última línea, en lugar de `___`, **el valor que tiene BX** en ese momento (por ejemplo `mov dx, 9`). Así DX queda igual que BX.

#### Código inicial
```asm
.model small
.stack 100h
.data
.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 3
    mov bx, ax
    mov ax, 8

    mov dx, ___      ; ¿cuánto vale BX ahora?

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Estado esperado
```
BX = 3
DX = 3
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

    mov ax, 3
    mov bx, ax
    mov ax, 8

    mov dx, 3

fin:
    mov ax, 4C00h
    int 21h
main endp
end main
```

#### Al superarla
—¡Tres! —dice Nova—. BX copió el 3 antes de que AX cambiara a 8. Después de copiar, cada palanca es independiente. {mentor} hace un ruido grave que, por primera vez, suena casi a aprobación.

#### Imagen
- Tres palancas de bronce en fila con visores de luz: la primera con ocho puntitos, la segunda con tres, la tercera apagada.
- Nova (chica de 15 años con capa oscura de cuello alto con circuitos cian y detalles dorados, túnica cerrada, calzas oscuras, botas con suela cian, pelo rubio flotando, ojos cian) señala la segunda palanca, pensativa.
- Gheco (gecko de luz cian con antiparras, chiquito) sostiene un reloj de arena chiquito.

### Prueba del sello

#### ¿Qué hace `mov bx, ax`?
Copia el valor de AX en BX. AX no cambia.

#### ¿Cuánto vale 0Ah en decimal?
10.

#### Si AX = 1234h, ¿cuánto valen AH y AL?
AH = 12h y AL = 34h.

#### ¿Por qué se escribe `0FFh` y no `FFh`?
Porque si empieza con letra, el ensamblador cree que es un nombre. El 0 dice «es un número».
