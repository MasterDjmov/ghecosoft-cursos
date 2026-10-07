# CURSO

```meta
slug: java
titulo: Java: El Imperio de las Clases
lenguaje: java
nivel: desde_cero
descripcion_corta: Java desde cero: objetos, colecciones, bases de datos y aplicaciones de escritorio.
precio_raiz: 10
dias_abono: 30
destacado: si
proximamente: no
publicado: si
```

### Descripción

Aprendé **Java desde cero**. No hace falta saber programar: cada tema se explica antes de usarse. El curso llega hasta aplicaciones de escritorio completas, con ventanas, base de datos y el estilo en capas que se usa en las empresas y en la facultad.

Java es la lengua de los sistemas de gestión de bancos, hospitales y comercios, de Android, de los servidores de miles de empresas y de Minecraft. En el Imperio **nada existe suelto**: todo vive en una clase, cada clase en su paquete, y cada acuerdo se firma como un contrato.

Cada tema es un **nodo** del árbol. En cada uno leés la explicación, compilás el ejemplo en tu compu y resolvés las **misiones**: al aprobarlas ganás denarios para abrir el siguiente. Cada rama termina con un **jefe**, un proyecto que junta todo lo que aprendiste.

El curso sigue el programa de **Paradigmas y Lenguajes III** (Licenciatura en Sistemas, UNLaR): cada nodo dice a qué unidad corresponde.

Al final del camino principal llegás a la **Encrucijada de los Denarios**, de donde salen tres Sendas optativas: un **juego 2D** con Swing, **Java moderno** (streams, patrones y concurrencia) y **APIs web con Spring Boot**.

> Qué hace falta: una compu con **Java 17 o más nuevo** (el JDK: `sudo apt install openjdk-17-jdk` en Linux, o el instalador de Adoptium en Windows y macOS) y, desde la cuarta rama, **PostgreSQL**. Los programas de Java se compilan y se prueban en tu compu, y se entregan pegando el código o subiendo un archivo.

### Temario

- Compilar, tipos, textos, entrada por teclado, decisiones, bucles, arrays y métodos
- Clases y objetos: constructores, encapsulamiento, herencia, polimorfismo e interfaces
- `enum`, `record`, composición y diagramas UML
- Paquetes, `.jar`, colecciones y genéricos, excepciones y lambdas
- Pruebas con JUnit, depuración y logging
- SQL con PostgreSQL y acceso a datos con JDBC: DAO y transacciones
- Aplicaciones de escritorio con Swing: layouts, tablas, MDI y MVC

# DICCIONARIO

| clave | singular | plural | género | descripción | historia | ámbito |
|---|---|---|---|---|---|---|
| coin.course | denario | denarios | m | La moneda del Imperio: se gana aprobando misiones obligatorias y abre los nodos del curso. | | curso |
| mentor.name | Kaffa | | m | El Arquitecto Imperial: diseñó los planos de la capital del Imperio de las Clases. | Kaffa trazó los planos de la capital cuando el Imperio era un montón de piedras sueltas. Su regla es simple: **nada existe suelto**. Cada cosa tiene su clase, cada clase su paquete y cada acuerdo su contrato. Es exigente, pero siempre explica por qué. En sus planos nunca falta una taza de café. | curso |
| world.region | Imperio de las Clases | | m | La región del mundo cuya lengua arcana es Java. | | curso |
| story.course_intro | Bienvenida al Imperio | | f | | Zed robaba en los techos del Puerto hasta que tocó una **llave de plomo y vidrio** que decía *«para quien llegue»*. Un vitral se encendió como un portal y despertó en la fila de la **Aduana del Compilador**, sin un solo papel.<br><br>Soy {mentor}, el Arquitecto Imperial. Acá **nada existe suelto** y nada pasa sin declararse: la Aduana revisa todo lo que Zed escribe. Parece estricta, y lo es, pero cada error que marca en la frontera es uno que no va a sufrir adentro.<br><br>Vos vas a ser su mente: cada micro-misión que resuelvas lo hace avanzar, cada tema que domines le abre una puerta del Imperio y cada misión aprobada te da denarios para abrir la siguiente. | curso |
| story.branch_completed | ¡Distrito conquistado! | | m | | {mentor} desenrolla un plano nuevo y marca con tinta un distrito entero. —Esta parte del Imperio ya funciona con tus clases, Zed. Nadia lo anota en su libreta, y por una vez no agrega ningún comentario. | curso |
| story.course_completed | ¡Dominaste la lengua del Imperio! | | f | | {mentor} te entrega su compás de arquitecto y una taza de café recién hecha. —Ya sos arquitecta o arquitecto del Imperio, {heroe}. Desde la Encrucijada de los Denarios salen tres caminos: el Arcade, las Corrientes y el Puerto de Spring. Elegí el tuyo. | curso |
| story.portal_piece | Lo que no pudo ordenar Kaffa | | f | La pieza del misterio del portal que se lee al terminar este curso (Mis Crónicas). | Trató de explicarme qué estaba construyendo y no pude ponerlo en ninguna clase. Es lo único que nunca supe ordenar: algo que no es de ningún lugar, porque es de todos. | curso |
| beast.slime | slime | slimes | m | Nace de los errores de sintaxis: la Aduana no deja pasar ni una línea. | Los slimes brotan de los punto y coma olvidados, las llaves sin cerrar y las comillas perdidas. La Aduana los detecta al compilar con mensajes como `';' expected`. Son débiles, pero hasta que no los eliminás no se ejecuta nada. | curso |
| beast.goblin | goblin | goblins | m | Nace de los tipos que no encajan: `incompatible types`, `NumberFormatException`, `ClassCastException`. | Los goblins viven en las conversiones: un `double` que no entra en un `int`, un texto que no es un número, un objeto que no es de la clase que creías. La Aduana atrapa a muchos al compilar; los más astutos esperan a que el programa corra. | curso |
| beast.skeleton | esqueleto | esqueletos | m | Nace de los nombres que no existen: `cannot find symbol`. | Los esqueletos son nombres sin cuerpo: una variable mal escrita, un método que no está en la clase, un `import` que falta. Java distingue mayúsculas: `string` no es `String`. | curso |
| beast.orc | orco | orcos | m | Nace de los índices fuera de rango: `ArrayIndexOutOfBoundsException`. | Los orcos atacan donde terminan los arrays y las listas: la posición 10 de un array de 10, el `get` de una lista vacía. Java no los deja pasar en silencio: corta el programa y deja un pergamino con la línea exacta. | curso |
| beast.ogre | ogro | ogros | m | Nace de los errores de lógica, entre ellos comparar textos con `==`. | El ogro es el más traicionero: el programa compila, corre y termina tranquilo… con el resultado equivocado. Su truco favorito en el Imperio es `==` entre textos, que a veces da `true` y a veces no. Solo lo vence quien prueba y depura. | curso |
| beast.troll | troll | trolls | m | Nace de las referencias: `NullPointerException`, alias y estado compartido. | El troll se esconde detrás de las referencias: una variable que apunta a `null`, dos variables que apuntan al mismo objeto y se pisan, una lista que alguien modificó desde otro lado. Su marca es el `NullPointerException`. | curso |
| beast.dragon | dragón | dragones | m | Guardián de los jefes: un problema grande hecho de problemas chicos. | Un dragón no se vence de un golpe. Se lo divide en clases y métodos, se vence cada uno y recién entonces cae. | curso |

## R00-N01 · Clase 0 · Hola, Java

```meta
tipo: raiz
criatura: slime
temas: prog.entorno, prog.salida, herr.compilacion
```

### Crónica

Zed robaba en los techos del **Puerto de los Mensajeros** desde que tenía memoria. Esa noche abrió un paquete sin remitente: adentro había una **llave de plomo y vidrios de colores**, con una etiqueta que decía *«para quien llegue»*. La tocó, un vitral del depósito se encendió como un portal… y despertó en una fila, frente a la muralla del **Imperio de las Clases**.

Delante de él, un mercader entrega un pergamino; el aduanero lo lee y se lo devuelve con una marca roja: *falta un punto y coma en la línea 3*. Una aduanera de uniforme azul, **Nadia**, le pide a Zed sus papeles. Él no tiene ninguno.

—Así funciona la frontera —dice {mentor}, el Arquitecto Imperial, con su taza de café en la mano—. El **compilador** revisa todo antes de dejarlo entrar. Molesta al principio. Después lo vas a agradecer, Zed: acá los errores se ven en la puerta y no a mitad del camino.

### Objetivos

- Instalar el JDK y comprobar que funciona.
- Escribir, compilar y ejecutar tu primer programa en Java.
- Entender la anatomía de un programa: la clase, el método `main` y las instrucciones.
- Mostrar texto con `System.out.println` y `System.out.print`, y escribir comentarios.
- Distinguir un **error de compilación** de un **error de ejecución** y leer un *stack trace*.

### Antes de empezar

Nada: este es el primer nodo. Solo necesitás una compu y ganas.

### Explicación

#### Qué es Java y qué es el JDK
Java es un lenguaje **compilado a bytecode**. Escribís el programa en un archivo
`.java` (texto), el compilador `javac` lo revisa y lo traduce a **bytecode**
(archivos `.class`), y la **JVM** (la máquina virtual de Java) ejecuta ese bytecode.
Por eso el mismo `.class` corre en Linux, Windows y macOS sin cambios.

| Pieza | Qué es |
|---|---|
| **JDK** | el kit de desarrollo: trae el compilador `javac`, la JVM y las herramientas |
| **`javac`** | el compilador: revisa y traduce `.java` → `.class` (es la Aduana) |
| **`java`** | lanza la JVM y ejecuta el programa |
| **JVM** | la máquina virtual que corre el bytecode |

Para instalarlo en Linux: `sudo apt install openjdk-17-jdk`. En Windows o macOS,
bajá el instalador del JDK 17 (o más nuevo) de *Adoptium* (Temurin). Después, en
una terminal:
```bash
java -version
javac -version
```
Si los dos responden con un número de versión (17 o más), está listo.

#### Tu primer programa
Creá un archivo llamado **`HolaImperio.java`** (el nombre tiene que coincidir con
el de la clase, con las mismas mayúsculas):
```java
public class HolaImperio {
    public static void main(String[] args) {
        System.out.println("Hola, Imperio");
    }
}
```
Y ejecutalo desde la carpeta donde lo guardaste:
```bash
java HolaImperio.java
```
Con un solo archivo, `java` compila y ejecuta en un paso. Cuando el programa tenga
varios archivos vas a usar los dos pasos por separado:
```bash
javac HolaImperio.java     # compila: crea HolaImperio.class
java HolaImperio           # ejecuta la clase (sin .java ni .class)
```

#### La anatomía de un programa
En Java **nada existe suelto**: todo el código vive dentro de una **clase**.

| Parte | Qué significa |
|---|---|
| `public class HolaImperio { … }` | declara una clase llamada `HolaImperio`; todo va entre sus llaves |
| `public static void main(String[] args)` | el **punto de entrada**: la JVM empieza a ejecutar acá |
| `System.out.println("…");` | una **instrucción**: muestra el texto y pasa a la línea siguiente |
| `;` | cada instrucción termina con punto y coma |

Por ahora, `public static void main(String[] args)` se escribe siempre igual (lo
vas a entender palabra por palabra más adelante: `public` es "visible desde
afuera", `static` es "de la clase", `void` es "no devuelve nada" y `args` son los
argumentos de la línea de comandos).

Java **distingue mayúsculas de minúsculas**: `System` no es `system`, y `String`
no es `string`.

#### Mostrar texto
```java
System.out.println("Con salto de línea al final");
System.out.print("Sin salto... ");
System.out.print("sigue en la misma línea\n");   // \n es un salto de línea
System.out.println("Comillas: \"así\" y barra: \\");
System.out.println();                           // una línea vacía
System.out.println("Suma: " + (2 + 3));        // + une texto con valores
```
Dentro de un texto, `\n` es un salto de línea, `\"` una comilla y `\\` una barra.

#### Comentarios
```java
// comentario de una línea
/* comentario
   de varias líneas */
/** comentario de documentación (Javadoc): lo vas a usar más adelante */
```
El compilador los ignora: son notas para las personas.

#### Dos clases de errores
1. **Error de compilación**: la Aduana no deja pasar el programa. No se ejecuta
   nada. El mensaje dice el archivo, la línea y qué espera:
   ```
   HolaImperio.java:3: error: ';' expected
           System.out.println("Hola, Imperio")
                                              ^
   1 error
   ```
2. **Error de ejecución** (una *excepción*): el programa compiló, empezó a correr y
   algo salió mal a mitad de camino. Java corta el programa y muestra un **stack
   trace**, el *pergamino de la maldición*:
   ```
   Exception in thread "main" java.lang.ArithmeticException: / by zero
           at Maldicion.main(Maldicion.java:5)
   ```
   Se lee así: **qué pasó** (`ArithmeticException: / by zero`, división por cero) y
   **dónde** (en el método `main` de la clase `Maldicion`, archivo
   `Maldicion.java`, **línea 5**). Siempre empezá a leer por arriba.

> **Si venís de C o C++.** No hay `#include`, ni punteros, ni `free`: la memoria se
> libera sola (el *recolector de basura*). `main` vive dentro de una clase y el
> programa no se compila a código de máquina sino a bytecode para la JVM.
>
> **Si venís de Python.** Los tipos se declaran, las instrucciones terminan con `;`,
> los bloques van entre llaves (la sangría es solo para leer mejor) y antes de
> ejecutar hay una compilación que revisa todo.

### Código de ejemplo

```java
/*
 * Clase 0 del Imperio: mostrar texto con println y print.
 * Se ejecuta con: java HolaImperio.java
 */
public class HolaImperio {
    public static void main(String[] args) {
        System.out.println("=== Aduana del Imperio de las Clases ===");
        System.out.println("Viajera: Kira");
        System.out.print("Destino: ");
        System.out.println("la capital");

        // Secuencias de escape dentro de un texto
        System.out.println("Sello: \"APROBADO\"");
        System.out.println("Ruta: C:\\imperio\\puerta");
        System.out.println("Equipaje:\n  - una espada\n  - un mapa");

        System.out.println();                                  // línea vacía
        System.out.println("Días de viaje: " + (3 + 4));        // + une texto y números
        System.out.println("Bienvenida al Imperio.");
    }
}
```

### Salida esperada

```
=== Aduana del Imperio de las Clases ===
Viajera: Kira
Destino: la capital
Sello: "APROBADO"
Ruta: C:\imperio\puerta
Equipaje:
  - una espada
  - un mapa

Días de viaje: 7
Bienvenida al Imperio.
```

### ¿Para qué sirve?

Todo programa, del más chico al más grande, arranca en un `main` y habla con quien lo usa mostrando texto. Los mensajes de la consola son también la primera herramienta para entender qué hace un programa: los programadores profesionales leen *stack traces* todos los días, y saber leerlos rápido es lo que más tiempo ahorra.

### Errores habituales

**Slime: falta el punto y coma.**
```
HolaImperio.java:7: error: ';' expected
```
Mirá la línea que dice el mensaje (o la anterior) y agregá el `;`.

**Esqueleto: una mayúscula de menos.** `system.out.println` o `string[] args`:
```
HolaImperio.java:3: error: package system does not exist
```
Java distingue mayúsculas: es `System` y `String`.

**Slime: el archivo no se llama como la clase.** Si la clase es `public class
HolaImperio`, el archivo tiene que ser `HolaImperio.java`:
```
Hola.java:1: error: class HolaImperio is public, should be declared in a file named HolaImperio.java
```

**Slime: comillas o llaves sin cerrar.** `unclosed string literal` o `reached end
of file while parsing`: falta cerrar una comilla o una llave.

**Goblin: `java` no encuentra la clase.** `Error: Could not find or load main class
HolaImperio`: estás en otra carpeta, o escribiste `java HolaImperio.class`
(se ejecuta sin la extensión).

### Micro-misión R00-N01-P1 · Declarar en la frontera

```meta
lugar: La fila de la Aduana del Compilador
personajes: Zed, Gheco, Nadia
carta: Mostrar texto | System.out.println("texto"); · muestra y salta de línea · cada instrucción termina con ;
recompensa: xp 10
```

#### Escena
Zed despierta en una fila larguísima frente a una muralla con vitrales dorados, con una llave de vidrio en la mano. Una aduanera de uniforme azul y rodete tirante le corta el paso: **Nadia**.
—Nombre y procedencia. Por escrito. En el Imperio, lo que no está declarado no existe.
Sobre el hombro de Zed aparece un gecko de luz con antiparras: **Gheco**. —Escribilo en el pergamino. Acá los pergaminos se **ejecutan**.

#### Gheco sugiere
`System.out.println("…");` muestra el texto entre comillas y salta a la línea siguiente. Para ejecutarlo: con el **Ejecutor de Java** abierto en tu compu (*Herramientas → Ejecutor de Java*), tocá **Ejecutar**. Si no lo tenés, corrélo en tu compu o tu IDE y pegá la salida abajo.

#### Desafío
Completá la instrucción para declarar quién sos.

#### Código inicial
```java
public class Declaracion {
    public static void main(String[] args) {
        System.out.___("Me llamo Zed y vengo del Puerto.");
    }
}
```

#### Salida esperada
```
Me llamo Zed y vengo del Puerto.
```

#### Solución
```java
public class Declaracion {
    public static void main(String[] args) {
        System.out.println("Me llamo Zed y vengo del Puerto.");
    }
}
```

#### Al superarla
Nadia lee la declaración, la sella y anota algo en su libreta. —Del Puerto. Ajá. —No suena a cumplido.

#### Imagen
- La muralla del Imperio de las Clases de noche, con vitrales dorados encendidos y una fila de viajeros.
- Nadia (uniforme azul de cuello alto, botones de bronce, rodete tirante, guantes blancos) le corta el paso a Zed.
- Zed (pelo blanco plateado, visor rojo, campera negra con vivos rojos) sostiene una llave de plomo y vidrios de colores.
- Gheco, gecko cian con antiparras, aparece sobre su hombro.

### Micro-misión R00-N01-P2 · Todo en una línea

```meta
lugar: La fila de la Aduana del Compilador
personajes: Zed, Gheco, Nadia
carta: print o println | print no salta de línea · println sí · se pueden combinar
recompensa: xp 10
```

#### Escena
—El formulario va en **una sola línea** —dice Nadia—: nombre, guion, oficio. Y la fecha abajo.

#### Gheco sugiere
`System.out.print(…)` muestra **sin** saltar de línea: lo siguiente sigue pegado. `println` salta al final.

#### Desafío
Usá `print` para que nombre y oficio queden en la misma línea.

#### Código inicial
```java
public class Formulario {
    public static void main(String[] args) {
        System.out.println("Zed");
        System.out.println(" - ladrón de techos");
        System.out.println("Llegada: hoy");
    }
}
```

#### Salida esperada
```
Zed - ladrón de techos
Llegada: hoy
```

#### Solución
```java
public class Formulario {
    public static void main(String[] args) {
        System.out.print("Zed");
        System.out.println(" - ladrón de techos");
        System.out.println("Llegada: hoy");
    }
}
```

#### Al superarla
Nadia levanta una ceja. —¿«Ladrón de techos»? Por lo menos es honesto. —Y lo anota igual.

#### Imagen
- Un formulario de pergamino con tres renglones luminosos: los dos primeros unidos en uno.
- Nadia, con la pluma en alto, mira a Zed con una ceja levantada.

### Micro-misión R00-N01-P3 · El punto y coma olvidado

```meta
lugar: La fila de la Aduana del Compilador
personajes: Zed, Gheco, Nadia
criatura: slime
carta: Error de compilación | el compilador (javac) revisa ANTES de ejecutar · ';' expected: falta un punto y coma
recompensa: xp 10
```

#### Escena
Delante de Zed, un mercader entrega su pergamino y se lo devuelven con una marca roja. Del pergamino gotea un **slime**.
—La Aduana es el **compilador** —dice Gheco—. Revisa todo antes de dejarlo pasar. Si falta un signo, no se ejecuta nada.

#### Gheco sugiere
Un **error de compilación** aparece antes de ejecutar: el programa ni arranca. `';' expected` quiere decir que falta un punto y coma en esa línea.

#### Desafío
Arreglá el pergamino del mercader para que la Aduana lo deje pasar.

#### Código inicial
```java
public class Mercader {
    public static void main(String[] args) {
        System.out.println("Traigo tres barriles")
        System.out.println("y ninguna mala intención");
    }
}
```

#### Salida esperada
```
Traigo tres barriles
y ninguna mala intención
```

#### Solución
```java
public class Mercader {
    public static void main(String[] args) {
        System.out.println("Traigo tres barriles");
        System.out.println("y ninguna mala intención");
    }
}
```

#### Al superarla
El slime se evapora. El mercader, agradecido, le guiña un ojo a Zed. Nadia, en cambio, no le saca los ojos de encima.

#### Imagen
- Un pergamino con una marca roja en la línea 3, del que gotea un slime verde que se evapora.
- Un mercader agradecido; Zed con el pergamino corregido.

### Micro-misión R00-N01-P4 · Lo que explota adentro

```meta
lugar: La fila de la Aduana del Compilador
personajes: Zed, Gheco, Nadia
criatura: ogro
carta: Error de ejecución | compila, pero falla al correr · el stack trace dice la línea · dividir enteros por 0: ArithmeticException
recompensa: xp 10
```

#### Escena
Zed intenta repartir el peaje entre los viajeros de su fila… que son cero. El pergamino **compila**, pero al ejecutarse explota con un mensaje largo.
—Eso es un **error de ejecución** —dice Gheco—. La Aduana no lo vio venir. Leé la línea que te marca.

#### Gheco sugiere
Un **error de ejecución** pasa con el programa ya andando. El *stack trace* dice qué pasó (`ArithmeticException: / by zero`) y en qué línea. Dividir un entero por 0 lo provoca.

#### Desafío
Que el peaje se reparta entre los 4 viajeros de la fila.

#### Código inicial
```java
public class Peaje {
    public static void main(String[] args) {
        int peaje = 20;
        int viajeros = 0;
        System.out.println("Cada uno paga " + peaje / viajeros);
    }
}
```

#### Salida esperada
```
Cada uno paga 5
```

#### Solución
```java
public class Peaje {
    public static void main(String[] args) {
        int peaje = 20;
        int viajeros = 4;
        System.out.println("Cada uno paga " + peaje / viajeros);
    }
}
```

#### Al superarla
Cinco denarios cada uno. La fila avanza y Zed ya está frente al portón.

#### Imagen
- Un pergamino que explota en chispas rojas con el texto `/ by zero`.
- Zed retrocede de un salto; Gheco se tapa los ojos.

### Micro-misión R00-N01-P5 · Nada existe suelto

```meta
lugar: El portón de la Aduana
personajes: Zed, Gheco, Nadia, Kaffa
carta: La anatomía | public class Nombre { … } · public static void main(String[] args) { … } · en Java todo vive en una clase
recompensa: xp 15
item: Llave del Vitral
```

#### Escena
En el portón, un hombre alto con una taza de café mira el pergamino de Zed: **Kaffa**, el Arquitecto Imperial. Al pergamino le falta el comienzo.
—En el Imperio **nada existe suelto** —dice—. Cada instrucción vive en un método, y cada método, en una clase.

#### Gheco sugiere
Todo programa de Java tiene una **clase** (`public class Nombre { … }`) y adentro el método **`main`**, donde empieza a ejecutarse. Las llaves `{ }` marcan dónde empieza y termina cada uno.

#### Desafío
Escribí la línea que abre el método `main`.

#### Código inicial
```java
public class Porton {
    ___
        System.out.println("Zed, del Puerto");
        System.out.println("Declara: una llave de vidrio");
    }
}
```

#### Salida esperada
```
Zed, del Puerto
Declara: una llave de vidrio
```

#### Solución
```java
public class Porton {
    public static void main(String[] args) {
        System.out.println("Zed, del Puerto");
        System.out.println("Declara: una llave de vidrio");
    }
}
```

#### Al superarla
Kaffa toma la llave de vidrio, la mira contra la luz de los vitrales y se la devuelve, muy despacio.
—Pasás la Aduana como todos, Zed: **declarando**. Nadia te va a acompañar. —Ella no parece contenta. Él tampoco.
La **Llave del Vitral** va a tu mochila.

#### Imagen
- Kaffa (alto, de túnica de arquitecto, con una taza de café) mira una llave de plomo y vidrios de colores contra la luz de un vitral dorado.
- Zed y Nadia, uno al lado del otro, mirándose de reojo.
- El portón de la Aduana empieza a abrirse.

### Misión R00-N01-M1 · El pase de frontera

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí un programa `PaseFrontera.java` que muestre tu pase para entrar al Imperio,
exactamente así (con tus datos, si querés, pero con el mismo formato):

- Un título entre signos `=`.
- Tres renglones de datos: nombre, oficio y ciudad de origen.
- Una línea vacía.
- El sello final entre comillas dobles.

#### Criterio de aprobación

- La clase se llama como el archivo y tiene su `main`.
- Usa `println` para cada renglón y `\"` para las comillas.
- La salida coincide con la esperada.

#### Salida esperada

```
==== PASE DE FRONTERA ====
Nombre: Kira
Oficio: aprendiz de arquitectura
Origen: el Valle de la Serpiente

Sello: "PUEDE PASAR"
```

#### Solución de referencia

```java
// Mision 1 - El pase de frontera: mostrar texto con formato.
public class PaseFrontera {
    public static void main(String[] args) {
        System.out.println("==== PASE DE FRONTERA ====");
        System.out.println("Nombre: Kira");
        System.out.println("Oficio: aprendiz de arquitectura");
        System.out.println("Origen: el Valle de la Serpiente");
        System.out.println();
        System.out.println("Sello: \"PUEDE PASAR\"");
    }
}
```

### Misión R00-N01-M2 · El pergamino con manchas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Este programa tiene **cuatro errores** y la Aduana no lo deja pasar. Copialo,
compilalo, leé cada mensaje y arreglalo hasta que muestre la salida esperada.
No cambies los textos.

#### Criterio de aprobación

- Compila sin errores.
- La salida coincide con la esperada.

#### Código inicial

```java
public class Pergamino {
    public static void main(string[] args) {
        System.out.println("El pergamino dice:")
        system.out.println("  Quien sabe leer los errores,");
        System.out.println("  cruza la frontera antes.);
    }
}
```

#### Salida esperada

```
El pergamino dice:
  Quien sabe leer los errores,
  cruza la frontera antes.
```

#### Solución de referencia

```java
// Mision 2 - El pergamino con manchas: los cuatro errores eran
// string -> String, el ; que faltaba, system -> System y la comilla sin cerrar.
public class Pergamino {
    public static void main(String[] args) {
        System.out.println("El pergamino dice:");
        System.out.println("  Quien sabe leer los errores,");
        System.out.println("  cruza la frontera antes.");
    }
}
```

### Misión R00-N01-M3 · El cartel de la posada

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La posada de la frontera necesita un cartel. Mostralo usando **un solo**
`System.out.print` con saltos de línea `\n` para el menú, y después un `println`
con el total calculado dentro del programa: un guiso (1200) más un pan (300) más
un café (450).

#### Criterio de aprobación

- El menú sale de un único `print` con `\n`.
- El total se calcula con `+` entre paréntesis, no se escribe a mano.

#### Salida esperada

```
POSADA LA TAZA DE KAFFA
-----------------------
Guiso ....... 1200
Pan ......... 300
Café ........ 450
Total: 1950
```

#### Solución de referencia

```java
// Mision 3 - El cartel de la posada: \n dentro de un texto y un total calculado.
public class Posada {
    public static void main(String[] args) {
        System.out.print("POSADA LA TAZA DE KAFFA\n-----------------------\nGuiso ....... 1200\nPan ......... 300\nCafé ........ 450\n");
        System.out.println("Total: " + (1200 + 300 + 450));
    }
}
```

### Encargo R00-N01-E1 · El recibo del kiosco

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El kiosco de la esquina quiere imprimir un recibo en su impresora de tickets.
Mostrá el nombre del kiosco, la fecha, tres productos con su precio, una línea
separadora y el total (calculado con `+`). Agregá un comentario de una línea
arriba de cada parte del recibo.

#### Criterio de aprobación

- Tiene comentarios que explican cada parte.
- El total se calcula dentro del programa.

#### Salida esperada

```
KIOSCO EL FAROL
Fecha: 29/09/2026
Alfajor ........ 900
Agua ........... 1100
Chicles ........ 450
---------------------
TOTAL .......... 2450
```

#### Solución de referencia

```java
// Encargo - El recibo del kiosco.
public class Recibo {
    public static void main(String[] args) {
        // Encabezado
        System.out.println("KIOSCO EL FAROL");
        System.out.println("Fecha: 29/09/2026");
        // Productos
        System.out.println("Alfajor ........ 900");
        System.out.println("Agua ........... 1100");
        System.out.println("Chicles ........ 450");
        // Total
        System.out.println("---------------------");
        System.out.println("TOTAL .......... " + (900 + 1100 + 450));
    }
}
```

### Prueba del sello

#### ¿Qué hace `javac` y qué hace `java`?

`javac` compila: revisa el `.java` y lo traduce a bytecode (`.class`). `java` lanza la JVM y ejecuta el programa. Con un solo archivo, `java Archivo.java` hace los dos pasos juntos.

#### ¿Por qué el archivo tiene que llamarse igual que la clase pública?

Porque Java busca cada clase pública en un archivo con su mismo nombre (y las mismas mayúsculas). Si no coinciden, no compila.

#### ¿Qué diferencia hay entre `print` y `println`?

`println` agrega un salto de línea al final; `print` no, y lo siguiente sigue en la misma línea.

#### ¿Cómo distinguís un error de compilación de uno de ejecución?

El de compilación lo marca `javac` y el programa no llega a correr (`error: ...`). El de ejecución aparece con el programa andando: `Exception in thread "main"` y un stack trace.

#### En un stack trace, ¿dónde está la línea del error?

En el primer renglón `at Clase.metodo(Archivo.java:NÚMERO)`: el número después de los dos puntos.

### Soluciones (docente)

Sale de `18-Java/01-Hola-Java` (unidad 2 de la cátedra), reescrito para empezar de cero: se enseña primero `java Archivo.java` (Java 11+) y después `javac` + `java`. El stack trace de ejemplo es el de `Maldicion.java` del capítulo original.
