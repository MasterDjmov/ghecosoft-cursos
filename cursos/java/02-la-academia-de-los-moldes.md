# RAMA R02 · La Academia de los Moldes: objetos

```meta
tipo: tronco
posicion: 2
```

## R02-N01 · Clases y objetos

```meta
tipo: tema
padre: R01-N09
precio: 10
criatura: skeleton
temas: poo.clases
```

### Crónica

Con el Sello de Entrada en el bolsillo, Zed cruza la Aduana por la puerta grande. La avenida lo lleva a la **Academia de los Moldes**: un edificio enorme lleno de talleres donde nadie fabrica cosas, sino **moldes**. De un molde de soldado salen mil soldados, cada uno con su nombre y su armadura, pero todos con la misma forma. Nadia camina a su lado: «hasta que aprenda», dice.

—Hasta ahora guardabas los datos de un viajero en tres arrays distintos —dice {mentor}—. Acá aprendés a escribir el **molde**: una clase `Viajero` que guarda sus datos y sabe hacer sus cosas. De ahí en adelante, Zed, en el Imperio todo es un objeto.

### Objetivos

- Entender qué es una clase y qué es un objeto (estado, comportamiento e identidad).
- Declarar atributos y métodos de instancia.
- Crear objetos con `new` y mandarles mensajes.
- Escribir `toString` para mostrar un objeto.

### Antes de empezar

- Métodos (Métodos: dividir el trabajo).
- Arrays (Arrays y matrices).

### Explicación

#### Clase y objeto
Una **clase** es un molde: describe qué **datos** tiene algo (sus *atributos*) y qué
**sabe hacer** (sus *métodos*). Un **objeto** es una cosa concreta hecha con ese
molde: una *instancia* de la clase.

| Idea | En el Imperio | En Java |
|---|---|---|
| Clase | el molde de soldado | `class Soldado { … }` |
| Objeto | el soldado Baldo | `new Soldado()` |
| Estado | su vida y su arma | los valores de sus atributos |
| Comportamiento | atacar, curarse | sus métodos |
| Identidad | es *ese* soldado y no otro | cada objeto es único, aunque tenga los mismos datos |

A pedirle algo a un objeto se le dice **mandarle un mensaje**: `baldo.atacar()` le
manda el mensaje `atacar` al objeto `baldo`.

#### Declarar una clase
```java
class Heroe {
    // Atributos: el estado de cada héroe
    String nombre;
    int vida;
    int nivel;

    // Métodos: lo que sabe hacer cada héroe (sin static)
    void recibirDanio(int danio) {
        vida -= danio;
        if (vida < 0) {
            vida = 0;
        }
    }

    boolean estaVivo() {
        return vida > 0;
    }
}
```
Los métodos de instancia **no llevan `static`**: trabajan con los atributos del objeto
que recibe el mensaje. Dentro de un método, `vida` es la vida **de ese** héroe.

#### Crear objetos y usarlos
```java
Heroe nadia = new Heroe();       // new crea un objeto nuevo
nadia.nombre = "Nadia";           // punto: acceder a un atributo...
nadia.vida = 30;
nadia.recibirDanio(12);          // ...o mandar un mensaje
System.out.println(nadia.vida);  // 18

Heroe baldo = new Heroe();       // otro objeto, con su propio estado
baldo.vida = 45;
```
Cada objeto tiene **su propia copia** de los atributos: cambiar `nadia.vida` no toca a
`baldo.vida`. Los atributos arrancan con valores por defecto: `0`, `false` o `null`.

(Asignar los atributos desde afuera, como acá, funciona pero no es buena práctica:
en los nodos siguientes vas a ver **constructores** para crear el objeto ya armado y
**encapsulamiento** para proteger sus datos.)

#### `toString`: cómo se muestra un objeto
Si hacés `System.out.println(nadia)`, Java muestra algo como `Heroe@5ca881b5`. Para
que muestre algo útil, la clase define un método `toString` que devuelve un texto:
```java
public String toString() {
    return nombre + " (nivel " + nivel + ", vida " + vida + ")";
}
```
`println` y el `+` con textos llaman a `toString` solos. (Lleva `public` porque
reemplaza a un método que todas las clases ya tienen; eso se entiende con la
herencia.)

#### Varias clases en un archivo
Un archivo puede tener **varias clases**, pero **solo una `public`**, que se llama
como el archivo. Para correrlo con `java Archivo.java`, la clase del `main` tiene que
ser **la primera**:
```java
public class Academia {          // primera: tiene el main
    public static void main(String[] args) { … }
}

class Heroe {                     // sin public
    …
}
```

#### Un array de objetos
```java
Heroe[] grupo = new Heroe[3];     // tres lugares en null
grupo[0] = nadia;
grupo[1] = baldo;
for (Heroe h : grupo) {
    if (h != null) {
        System.out.println(h);
    }
}
```
Adiós a los arrays paralelos: cada lugar guarda un héroe entero.

> **Si venís de C.** Una clase es un `struct` que además tiene funciones adentro. Las
> variables de tipo clase son referencias (parecidas a punteros, pero sin
> aritmética ni `free`).
>
> **Si venís de Python.** No hay `self`: dentro de un método los atributos se usan
> directo (o con `this`, que vas a ver en el nodo siguiente). Los atributos se
> declaran en la clase, con su tipo.

### Código de ejemplo

```java
/*
 * Clases y objetos: los moldes de la Academia.
 */
public class Academia {
    public static void main(String[] args) {
        Heroe nadia = new Heroe();
        nadia.nombre = "Nadia";
        nadia.vida = 30;
        nadia.nivel = 2;

        Heroe baldo = new Heroe();
        baldo.nombre = "Baldo";
        baldo.vida = 45;
        baldo.nivel = 3;

        System.out.println(nadia);
        System.out.println(baldo);

        // Mensajes: cada objeto cambia su propio estado
        nadia.recibirDanio(12);
        baldo.subirNivel();
        System.out.println("Después del combate:");
        System.out.println("  " + nadia);
        System.out.println("  " + baldo);

        nadia.recibirDanio(50);
        System.out.println(nadia.nombre + " ¿vivo? " + nadia.estaVivo());

        // Un array de objetos
        Heroe[] grupo = {nadia, baldo, new Heroe()};
        grupo[2].nombre = "Lía";
        grupo[2].vida = 20;
        grupo[2].nivel = 1;
        int vivos = 0;
        for (Heroe h : grupo) {
            if (h.estaVivo()) {
                vivos++;
            }
        }
        System.out.println("Héroes en pie: " + vivos + " de " + grupo.length);

        // Sin toString se vería el nombre de la clase y un número interno
        Moneda denario = new Moneda();
        System.out.println("Una moneda sin toString: " + (denario.toString().startsWith("Moneda@") ? "Moneda@..." : "?"));
    }
}

class Heroe {
    String nombre;
    int vida;
    int nivel;

    void recibirDanio(int danio) {
        vida -= danio;
        if (vida < 0) {
            vida = 0;
        }
    }

    void subirNivel() {
        nivel++;
        vida += 10;
    }

    boolean estaVivo() {
        return vida > 0;
    }

    public String toString() {
        return nombre + " (nivel " + nivel + ", vida " + vida + ")";
    }
}

class Moneda {
    int valor;
}
```

### Salida esperada

```
Nadia (nivel 2, vida 30)
Baldo (nivel 3, vida 45)
Después del combate:
  Nadia (nivel 2, vida 18)
  Baldo (nivel 4, vida 55)
Nadia ¿vivo? false
Héroes en pie: 2 de 3
Una moneda sin toString: Moneda@...
```

### ¿Para qué sirve?

Casi todo el software que se escribe en Java es orientado a objetos: un sistema de un banco tiene clases `Cuenta`, `Cliente` y `Movimiento`; un juego, `Jugador`, `Enemigo` y `Arma`; una app de turnos, `Paciente` y `Turno`. Pensar en objetos (qué cosas hay y qué sabe hacer cada una) es la forma de ordenar programas grandes para que se entiendan.

### Errores habituales

**Troll: usar un objeto que no se creó.**
```
Exception in thread "main" java.lang.NullPointerException: Cannot assign field "vida" because "nadia" is null
        at Academia.main(Academia.java:6)
```
Declarar `Heroe nadia;` no crea nada: falta `= new Heroe()`.

**Esqueleto: llamar un método de instancia sin objeto.** `Heroe.estaVivo()` no
compila (`non-static method estaVivo() cannot be referenced from a static
context`): se llama sobre un objeto, `nadia.estaVivo()`.

**Slime: dos clases `public` en el mismo archivo.** `class Heroe is public, should
be declared in a file named Heroe.java`. Solo la del archivo lleva `public`.

**Ogro: el `main` no es la primera clase.** Con `java Academia.java` se ejecuta la
primera clase del archivo: si es `Heroe`, dice `error: can't find main(String[])
method in class: Heroe`.

**Ogro: `toString` mal escrito.** `tostring` o `toString(int x)` son métodos
nuevos: `println` sigue mostrando `Heroe@5ca881b5`.

### Micro-misión R02-N01-P1 · El primer molde

```meta
lugar: Los talleres de la Academia de los Moldes
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: Clase y objeto | class Viajero { String nombre; } es el molde · new Viajero() crea un objeto · v.nombre = "Zed"; le da un dato
recompensa: xp 10, oro 10
```

#### Escena
Con el Sello de Entrada en el bolsillo, Zed llega a la **Academia de los Moldes**. La **Maestra de Moldes**, con el delantal lleno de virutas de bronce, le señala tres arrays sueltos en su pizarra: nombres, edades y oficios. —Así guardabas a tus viajeros. Desde hoy, cada viajero sale de un **molde**.

#### Gheco sugiere
Una **clase** es el molde: dice qué datos tiene cada objeto (`String nombre; int edad;`). `new Viajero()` crea un **objeto** nuevo de ese molde, y con el punto le cargás sus datos: `v.nombre = "Zed";`.

#### Desafío
Creá el objeto con `new`.

#### Código inicial
```java
public class Molde {
    public static void main(String[] args) {
        Viajero v = ___;
        v.nombre = "Zed";
        v.edad = 19;
        v.oficio = "ladrón retirado";
        System.out.println(v.nombre + ", " + v.edad + " años, " + v.oficio);
    }
}

class Viajero {
    String nombre;
    int edad;
    String oficio;
}
```

#### Salida esperada
```
Zed, 19 años, ladrón retirado
```

#### Solución
```java
public class Molde {
    public static void main(String[] args) {
        Viajero v = new Viajero();
        v.nombre = "Zed";
        v.edad = 19;
        v.oficio = "ladrón retirado";
        System.out.println(v.nombre + ", " + v.edad + " años, " + v.oficio);
    }
}

class Viajero {
    String nombre;
    int edad;
    String oficio;
}
```

#### Al superarla
—«Retirado» —lee Nadia, y levanta una ceja. —Desde la semana pasada —dice Zed. La Maestra se ríe: es el primer viajero que sale entero de un molde, con todos sus datos juntos.

#### Imagen
- Un taller enorme de la Academia de los Moldes, con moldes de bronce colgando del techo.
- La Maestra de Moldes (delantal con virutas de bronce) señalando una pizarra con tres arrays tachados.
- Zed (pelo blanco plateado, visor rojo) frente a un molde con forma de persona; Nadia y Gheco a su lado.

### Micro-misión R02-N01-P2 · Un molde, muchos viajeros

```meta
lugar: Los talleres de la Academia de los Moldes
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: Cada objeto es otro | dos new = dos objetos · cada uno con sus propios datos · cambiar uno no cambia el otro
recompensa: xp 10, oro 10
```

#### Escena
—Si cambio el nombre de este viajero —pregunta Zed—, ¿se cambia el de todos los que salieron del molde? La Maestra le pone dos viajeros enfrente. —Probalo.

#### Gheco sugiere
Cada `new` fabrica un objeto **distinto**, con su propia copia de los atributos. `a.nombre` y `b.nombre` son dos cajones diferentes.

#### Desafío
Creá el segundo viajero, `b`, con su propio `new`.

#### Código inicial
```java
public class DosViajeros {
    public static void main(String[] args) {
        Viajero a = new Viajero();
        Viajero b = ___;
        a.nombre = "Zed";
        b.nombre = "Nadia";
        a.nombre = "Zed del Puerto";
        System.out.println("a: " + a.nombre);
        System.out.println("b: " + b.nombre);
    }
}

class Viajero {
    String nombre;
}
```

#### Salida esperada
```
a: Zed del Puerto
b: Nadia
```

#### Solución
```java
public class DosViajeros {
    public static void main(String[] args) {
        Viajero a = new Viajero();
        Viajero b = new Viajero();
        a.nombre = "Zed";
        b.nombre = "Nadia";
        a.nombre = "Zed del Puerto";
        System.out.println("a: " + a.nombre);
        System.out.println("b: " + b.nombre);
    }
}

class Viajero {
    String nombre;
}
```

#### Al superarla
Zed cambió su nombre y el de Nadia siguió igual. —Por suerte —dice ella—. No quiero llamarme «del Puerto».

#### Imagen
- Dos figuras recién salidas del mismo molde de bronce, cada una con una etiqueta distinta: «Zed del Puerto» y «Nadia».
- Nadia cruzada de brazos; Zed sonriendo.

### Micro-misión R02-N01-P3 · El molde que sabe hacer cosas

```meta
lugar: Los talleres de la Academia de los Moldes
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: Método de instancia | String saludo() { return "Soy " + nombre; } · usa los datos de SU objeto · v.saludo()
recompensa: xp 15, oro 15
```

#### Escena
—Un molde no guarda solo datos —dice la Maestra—. También sabe **hacer** cosas. Cada viajero sabe presentarse, y se presenta con **su** nombre.

#### Gheco sugiere
Un método **sin `static`** pertenece a cada objeto: adentro, `nombre` es el nombre de **ese** objeto. Se llama con el punto: `zed.saludo()`.

#### Desafío
Completá el `return` del método `saludo`: «Soy <nombre>. Origen: <origen>».

#### Código inicial
```java
public class Presentacion {
    public static void main(String[] args) {
        Viajero zed = new Viajero();
        zed.nombre = "Zed";
        zed.origen = "el Puerto";
        Viajero nadia = new Viajero();
        nadia.nombre = "Nadia";
        nadia.origen = "la Aduana";
        System.out.println(zed.saludo());
        System.out.println(nadia.saludo());
    }
}

class Viajero {
    String nombre;
    String origen;

    String saludo() {
        return ___;
    }
}
```

#### Salida esperada
```
Soy Zed. Origen: el Puerto
Soy Nadia. Origen: la Aduana
```

#### Solución
```java
public class Presentacion {
    public static void main(String[] args) {
        Viajero zed = new Viajero();
        zed.nombre = "Zed";
        zed.origen = "el Puerto";
        Viajero nadia = new Viajero();
        nadia.nombre = "Nadia";
        nadia.origen = "la Aduana";
        System.out.println(zed.saludo());
        System.out.println(nadia.saludo());
    }
}

class Viajero {
    String nombre;
    String origen;

    String saludo() {
        return "Soy " + nombre + ". Origen: " + origen;
    }
}
```

#### Al superarla
Un solo método y cada uno se presenta a su manera. —Es como los libritos de la Aduana —dice Zed—, pero cada viajero lleva el suyo en el bolsillo.

#### Imagen
- Dos figuras de bronce con globos de diálogo distintos que salen del mismo libro abierto.
- La Maestra de Moldes asintiendo; Gheco anotando en el aire con una pluma de luz.

### Micro-misión R02-N01-P4 · El fantasma del molde

```meta
lugar: Los talleres de la Academia de los Moldes
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
criatura: esqueleto
carta: toString | public String toString() { return …; } · lo que se muestra al imprimir el objeto · sin él: Clase@1b6d3586
recompensa: xp 15, oro 15
```

#### Escena
Zed imprime a su viajero directamente y en la consola aparece algo como `Viajero@1b6d3586`. Del molde sale un **esqueleto** que repite ese código como un nombre sin cuerpo.
—Java no sabe cómo querés que se vea tu objeto —dice Gheco—. Decíselo.

#### Gheco sugiere
Al imprimir un objeto, Java llama a su método `toString()`. Si no lo escribiste, muestra la clase y un código raro. Escribilo vos: `public String toString() { return …; }`.

#### Desafío
Completá el nombre del método para que `println(v)` muestre al viajero.

#### Código inicial
```java
public class Fantasma {
    public static void main(String[] args) {
        Viajero v = new Viajero();
        v.nombre = "Zed";
        v.edad = 19;
        System.out.println(v);
    }
}

class Viajero {
    String nombre;
    int edad;

    public String ___() {
        return "Viajero[" + nombre + ", " + edad + "]";
    }
}
```

#### Salida esperada
```
Viajero[Zed, 19]
```

#### Solución
```java
public class Fantasma {
    public static void main(String[] args) {
        Viajero v = new Viajero();
        v.nombre = "Zed";
        v.edad = 19;
        System.out.println(v);
    }
}

class Viajero {
    String nombre;
    int edad;

    public String toString() {
        return "Viajero[" + nombre + ", " + edad + "]";
    }
}
```

#### Al superarla
«Viajero[Zed, 19]». El esqueleto se mira las manos, encuentra un nombre y se desarma tranquilo. Al lado, un soldado sale de un molde… sin espada.

#### Imagen
- Un esqueleto con una etiqueta «Viajero@1b6d3586» desarmándose en paz.
- Al fondo, un soldado de bronce recién salido de un molde, con la mano vacía donde debería ir la espada.

### Misión R02-N01-M1 · El molde de la espada

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Espada` con nombre, filo (un entero de 0 a 100) y material.
Tiene tres métodos: `usar()` (baja el filo en 15, sin pasar de 0), `afilar()` (lo
sube en 30, sin pasar de 100) y `estaRota()` (el filo es 0). Agregale `toString`.
En el `main`, creá dos espadas, usalas y afilalas, y mostrá su estado en cada paso.

#### Criterio de aprobación

- La clase tiene atributos, tres métodos de instancia y `toString`.
- Las dos espadas cambian cada una su propio estado.

#### Salida esperada

```
Colmillo de acero (filo 50)
Brisa de bronce (filo 20)
Después de pelear:
  Colmillo de acero (filo 35)
  Brisa de bronce (filo 0) ¡ROTA!
Después del herrero:
  Colmillo de acero (filo 95)
  Brisa de bronce (filo 30)
```

#### Solución de referencia

```java
// Mision 1 - El molde de la espada: atributos, metodos y toString.
public class Forja {
    public static void main(String[] args) {
        Espada colmillo = new Espada();
        colmillo.nombre = "Colmillo";
        colmillo.filo = 50;
        colmillo.material = "acero";

        Espada brisa = new Espada();
        brisa.nombre = "Brisa";
        brisa.filo = 20;
        brisa.material = "bronce";

        System.out.println(colmillo);
        System.out.println(brisa);
        colmillo.usar();
        brisa.usar();
        brisa.usar();
        System.out.println("Después de pelear:");
        System.out.println("  " + colmillo);
        System.out.println("  " + brisa + (brisa.estaRota() ? " ¡ROTA!" : ""));
        brisa.afilar();
        colmillo.afilar();
        colmillo.afilar();
        System.out.println("Después del herrero:");
        System.out.println("  " + colmillo);
        System.out.println("  " + brisa);
    }
}

class Espada {
    String nombre;
    int filo;
    String material;

    void usar() {
        filo = Math.max(0, filo - 15);
    }

    void afilar() {
        filo = Math.min(100, filo + 30);
    }

    boolean estaRota() {
        return filo == 0;
    }

    public String toString() {
        return nombre + " de " + material + " (filo " + filo + ")";
    }
}
```

### Misión R02-N01-M2 · La alcancía

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Alcancia` con un dueño y una cantidad de denarios. Métodos:
`depositar(int monto)` (solo si el monto es positivo), `boolean retirar(int monto)`
(devuelve `false` y no hace nada si no alcanza) y `toString`. En el `main` creá la
alcancía de Nadia, hacé un depósito, un retiro que alcanza y otro que no, mostrando el
resultado de cada operación.

#### Criterio de aprobación

- `retirar` devuelve un `boolean` y no deja el saldo negativo.
- `depositar` ignora montos negativos o cero.

#### Salida esperada

```
Alcancía de Nadia: 0 denarios
Alcancía de Nadia: 80 denarios
Retirar 30: ok
Retirar 100: no alcanza
Alcancía de Nadia: 50 denarios
```

#### Solución de referencia

```java
// Mision 2 - La alcancia: metodos que validan y devuelven boolean.
public class Ahorros {
    public static void main(String[] args) {
        Alcancia alcancia = new Alcancia();
        alcancia.duenio = "Nadia";
        System.out.println(alcancia);
        alcancia.depositar(80);
        alcancia.depositar(-20);
        System.out.println(alcancia);
        System.out.println("Retirar 30: " + (alcancia.retirar(30) ? "ok" : "no alcanza"));
        System.out.println("Retirar 100: " + (alcancia.retirar(100) ? "ok" : "no alcanza"));
        System.out.println(alcancia);
    }
}

class Alcancia {
    String duenio;
    int denarios;

    void depositar(int monto) {
        if (monto > 0) {
            denarios += monto;
        }
    }

    boolean retirar(int monto) {
        if (monto <= 0 || monto > denarios) {
            return false;
        }
        denarios -= monto;
        return true;
    }

    public String toString() {
        return "Alcancía de " + duenio + ": " + denarios + " denarios";
    }
}
```

### Misión R02-N01-M3 · La compañía de la caravana

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Mula` con nombre, carga actual y carga máxima, y un método
`boolean cargar(int kilos)` que solo acepta si no se pasa del máximo. En el `main`
armá un **array** de tres mulas y repartí una lista de bultos `{40, 25, 60, 10, 35}`:
cada bulto va a la primera mula que lo acepte; si ninguna puede, se avisa. Al final
mostrá cada mula y el total cargado.

#### Criterio de aprobación

- Usa un array de objetos.
- Cada bulto se intenta en orden y se informa si no entra en ninguna.

#### Salida esperada

```
Bulto de 40 kg -> Terca
Bulto de 25 kg -> Lenta
Bulto de 60 kg -> Brava
Bulto de 10 kg -> Terca
Bulto de 35 kg: no entra en ninguna mula
Terca: 50/60 kg
Lenta: 25/50 kg
Brava: 60/70 kg
Total cargado: 135 kg
```

#### Solución de referencia

```java
// Mision 3 - La compania de la caravana: un array de objetos.
public class Caravana {
    public static void main(String[] args) {
        Mula[] mulas = {new Mula(), new Mula(), new Mula()};
        String[] nombres = {"Terca", "Lenta", "Brava"};
        int[] maximos = {60, 50, 70};
        for (int i = 0; i < mulas.length; i++) {
            mulas[i].nombre = nombres[i];
            mulas[i].cargaMaxima = maximos[i];
        }

        int[] bultos = {40, 25, 60, 10, 35};
        for (int bulto : bultos) {
            boolean ubicado = false;
            for (Mula m : mulas) {
                if (m.cargar(bulto)) {
                    System.out.println("Bulto de " + bulto + " kg -> " + m.nombre);
                    ubicado = true;
                    break;
                }
            }
            if (!ubicado) {
                System.out.println("Bulto de " + bulto + " kg: no entra en ninguna mula");
            }
        }

        int total = 0;
        for (Mula m : mulas) {
            System.out.println(m);
            total += m.carga;
        }
        System.out.println("Total cargado: " + total + " kg");
    }
}

class Mula {
    String nombre;
    int carga;
    int cargaMaxima;

    boolean cargar(int kilos) {
        if (carga + kilos > cargaMaxima) {
            return false;
        }
        carga += kilos;
        return true;
    }

    public String toString() {
        return nombre + ": " + carga + "/" + cargaMaxima + " kg";
    }
}
```

### Encargo R02-N01-E1 · El termostato

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Modelá el termostato de una casa: una clase `Termostato` con la temperatura actual,
la deseada y si la calefacción está prendida. Un método `actualizar()` prende la
calefacción si la actual está más de 1 grado por debajo de la deseada, la apaga si
llegó, y si está prendida sube la actual medio grado. En el `main`, arrancá en 18.0 con
21.0 deseada y llamá a `actualizar()` 8 veces mostrando el estado.

#### Criterio de aprobación

- Toda la lógica está en la clase, no en el `main`.
- Tiene `toString`.

#### Salida esperada

```
Paso 1: 18.5 °C, deseada 21.0 °C, calefacción prendida
Paso 2: 19.0 °C, deseada 21.0 °C, calefacción prendida
Paso 3: 19.5 °C, deseada 21.0 °C, calefacción prendida
Paso 4: 20.0 °C, deseada 21.0 °C, calefacción prendida
Paso 5: 20.5 °C, deseada 21.0 °C, calefacción prendida
Paso 6: 21.0 °C, deseada 21.0 °C, calefacción prendida
Paso 7: 21.0 °C, deseada 21.0 °C, calefacción apagada
Paso 8: 21.0 °C, deseada 21.0 °C, calefacción apagada
```

#### Solución de referencia

```java
// Encargo - El termostato: el comportamiento vive en la clase.
public class Casa {
    public static void main(String[] args) {
        Termostato t = new Termostato();
        t.actual = 18.0;
        t.deseada = 21.0;
        for (int i = 1; i <= 8; i++) {
            t.actualizar();
            System.out.println("Paso " + i + ": " + t);
        }
    }
}

class Termostato {
    double actual;
    double deseada;
    boolean calefaccion;

    void actualizar() {
        if (actual < deseada - 1) {
            calefaccion = true;
        } else if (actual >= deseada) {
            calefaccion = false;
        }
        if (calefaccion) {
            actual += 0.5;
        }
    }

    public String toString() {
        return actual + " °C, deseada " + deseada + " °C, calefacción " + (calefaccion ? "prendida" : "apagada");
    }
}
```

### Prueba del sello

#### ¿Qué diferencia hay entre una clase y un objeto?

La clase es el molde (qué datos y qué comportamiento tiene); el objeto es una cosa concreta creada con `new` a partir de ese molde.

#### ¿Qué es el estado de un objeto?

Los valores de sus atributos en un momento dado.

#### ¿Por qué `Heroe nadia; nadia.vida = 3;` falla?

Porque `nadia` no apunta a ningún objeto (no se hizo `new`): da error o `NullPointerException`.

#### ¿Para qué sirve `toString`?

Para definir cómo se muestra el objeto como texto; lo usan `println` y el `+` con textos.

#### Si dos objetos tienen los mismos datos, ¿son el mismo objeto?

No: cada objeto tiene su identidad. Son dos objetos distintos con el mismo estado.

### Soluciones (docente)

Sale de `18-Java/09-Clases-Objetos` (unidad 1: clase, objeto, estado, comportamiento, identidad y mensaje). `toString` se presenta sin `@Override`, que se explica con la herencia.

## R02-N02 · Constructores, this y sobrecarga

```meta
tipo: tema
padre: R02-N01
precio: 10
criatura: goblin
temas: poo.constructores
```

### Crónica

En el taller de los soldados, un aprendiz arma soldados a mano: primero el cuerpo, después el casco, después el nombre… y a la mitad se olvida la espada. Al lado, la **Maestra de Moldes** aprieta una palanca y el soldado sale **completo**.

—Un objeto a medio armar es un objeto roto —dice {mentor}—. El **constructor** es la palanca: garantiza que cada objeto nazca con todo lo que necesita.

### Objetivos

- Escribir constructores para crear objetos completos y válidos.
- Usar `this` para distinguir atributos de parámetros.
- Sobrecargar constructores y reutilizarlos con `this(...)`.
- Conocer el constructor por defecto.

### Antes de empezar

- Clases y objetos.

### Explicación

#### El constructor
Un **constructor** es un método especial que se ejecuta al hacer `new`. Se llama
**igual que la clase** y **no tiene tipo de retorno** (ni siquiera `void`):
```java
class Heroe {
    String nombre;
    int vida;

    Heroe(String nombre, int vida) {
        this.nombre = nombre;
        this.vida = vida;
    }
}

Heroe nadia = new Heroe("Nadia", 30);    // nace completa
```

#### `this`
`this` es **el objeto que se está construyendo** (o que recibe el mensaje). Cuando un
parámetro se llama igual que un atributo, el parámetro "tapa" al atributo: `nombre`
es el parámetro y `this.nombre` es el atributo.
```java
this.nombre = nombre;    // al atributo le asigno el parámetro
```
Sin `this`, `nombre = nombre;` asigna el parámetro a sí mismo y el atributo queda en
`null` (un error clásico).

#### Validar en el constructor
El constructor es el lugar para asegurar que el objeto nace **válido**:
```java
Heroe(String nombre, int vida) {
    if (nombre == null || nombre.isBlank()) {
        throw new IllegalArgumentException("El héroe necesita un nombre");
    }
    this.nombre = nombre.trim();
    this.vida = Math.max(1, vida);
}
```
`throw new IllegalArgumentException(...)` corta la creación con un error que explica
qué pasó (las excepciones se ven a fondo en la rama 3).

#### Sobrecarga de constructores
Como los métodos, se pueden tener varios constructores con distintos parámetros:
```java
Heroe(String nombre, int vida) { … }
Heroe(String nombre) { … }           // con vida por defecto
```
Para no repetir código, un constructor puede llamar a otro con `this(...)`, que tiene
que ser **la primera línea**:
```java
Heroe(String nombre) {
    this(nombre, 30);                 // usa el constructor de dos parámetros
}
```

#### El constructor por defecto
Si una clase **no escribe ningún** constructor, Java le agrega uno vacío, sin
parámetros (por eso funcionaba `new Heroe()` en el nodo anterior). En cuanto
escribís uno, ese constructor vacío **desaparece**: `new Heroe()` deja de compilar si
no lo escribís vos.

#### Inicializar atributos al declararlos
Un atributo puede tener un valor inicial en su declaración; se asigna antes de
ejecutar el constructor:
```java
int nivel = 1;
String[] mochila = new String[5];
```

> **Si venís de C++.** No hay lista de inicialización ni destructores: la memoria la
> libera el recolector de basura. `this` es una referencia, no un puntero (`this.x`,
> no `this->x`).
>
> **Si venís de Python.** El constructor no se llama `__init__` sino como la clase, y
> `this` es el equivalente de `self`, pero no se escribe como parámetro.

### Código de ejemplo

```java
/*
 * Constructores, this y sobrecarga: la palanca del taller de moldes.
 */
public class TallerMoldes {
    public static void main(String[] args) {
        Soldado baldo = new Soldado("Baldo", 45, "lanza");
        Soldado lia = new Soldado("Lía", 30);          // arma por defecto
        Soldado recluta = new Soldado("  Pip  ");       // vida y arma por defecto

        System.out.println(baldo);
        System.out.println(lia);
        System.out.println(recluta);
        System.out.println("Soldados creados: " + Soldado.creados);

        // Un objeto con datos inválidos no llega a nacer
        try {
            Soldado fantasma = new Soldado("   ", 10);
            System.out.println(fantasma);
        } catch (IllegalArgumentException e) {
            System.out.println("No se pudo crear: " + e.getMessage());
        }

        // Vec2: constructores sobrecargados para un punto del mapa
        Vec2 origen = new Vec2();
        Vec2 torre = new Vec2(3, 4);
        Vec2 copia = new Vec2(torre);
        copia.x = 10;
        System.out.println("Origen " + origen + ", torre " + torre + ", copia movida " + copia);
        System.out.println("Distancia de la torre al origen: " + torre.distanciaA(origen));
    }
}

class Soldado {
    static int creados = 0;      // uno solo para toda la clase (se ve en el próximo nodo)

    String nombre;
    int vida;
    String arma;
    int nivel = 1;               // valor inicial al declararlo

    Soldado(String nombre, int vida, String arma) {
        if (nombre == null || nombre.isBlank()) {
            throw new IllegalArgumentException("el soldado necesita un nombre");
        }
        this.nombre = nombre.trim();
        this.vida = Math.max(1, vida);
        this.arma = arma;
        creados++;
    }

    Soldado(String nombre, int vida) {
        this(nombre, vida, "espada corta");
    }

    Soldado(String nombre) {
        this(nombre, 25);
    }

    public String toString() {
        return nombre + " [vida " + vida + ", " + arma + ", nivel " + nivel + "]";
    }
}

class Vec2 {
    double x;
    double y;

    Vec2() {
        this(0, 0);
    }

    Vec2(double x, double y) {
        this.x = x;
        this.y = y;
    }

    Vec2(Vec2 otro) {             // constructor de copia
        this(otro.x, otro.y);
    }

    double distanciaA(Vec2 otro) {
        double dx = x - otro.x;
        double dy = y - otro.y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    public String toString() {
        return "(" + x + ", " + y + ")";
    }
}
```

### Salida esperada

```
Baldo [vida 45, lanza, nivel 1]
Lía [vida 30, espada corta, nivel 1]
Pip [vida 25, espada corta, nivel 1]
Soldados creados: 3
No se pudo crear: el soldado necesita un nombre
Origen (0.0, 0.0), torre (3.0, 4.0), copia movida (10.0, 4.0)
Distancia de la torre al origen: 5.0
```

### ¿Para qué sirve?

Los constructores evitan objetos a medio armar: una `Factura` sin cliente, un `Turno` sin fecha, una `Cuenta` con saldo negativo. Validar en el constructor hace que el resto del programa pueda confiar en que todo objeto que existe está bien formado, y la sobrecarga permite crear objetos de varias formas cómodas (con datos completos o con valores por defecto).

### Errores habituales

**Troll: `nombre = nombre;` sin `this`.** El atributo queda en `null` y el parámetro
se asigna a sí mismo. Va `this.nombre = nombre;`.

**Esqueleto: el constructor vacío que ya no existe.**
```
TallerMoldes.java:4: error: constructor Soldado in class Soldado cannot be applied to given types;
        Soldado s = new Soldado();
                    ^
  required: String,int,String
  found:    no arguments
```
Al escribir un constructor, el vacío desaparece.

**Slime: `this(...)` que no es la primera línea.** `call to this must be first
statement in constructor`.

**Ogro: el constructor con `void`.** `void Soldado(...)` no es un constructor: es un
método que se llama igual que la clase. `new` no lo ejecuta.

### Micro-misión R02-N02-P1 · La palanca del molde

```meta
lugar: El taller de los soldados
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: Constructor | Soldado(String nombre, String arma) { … } · se llama como la clase y no devuelve nada · new Soldado("Lía", "espada")
recompensa: xp 10, oro 10
```

#### Escena
Un aprendiz arma soldados a mano: primero el cuerpo, después el casco, después el nombre… y a la mitad se olvida la espada. La Maestra aprieta una palanca y el soldado sale **completo**. —Esa palanca es el **constructor**.

#### Gheco sugiere
Un **constructor** se llama igual que la clase y no tiene tipo de retorno. Recibe los datos y los guarda en el objeto: `this.arma = arma;` (`this.arma` es el atributo; `arma`, el parámetro).

#### Desafío
Completá la línea que guarda el arma en el objeto.

#### Código inicial
```java
public class Palanca {
    public static void main(String[] args) {
        Soldado a = new Soldado("Lía", "espada");
        Soldado b = new Soldado("Teo", "lanza");
        System.out.println(a.nombre + " con " + a.arma);
        System.out.println(b.nombre + " con " + b.arma);
    }
}

class Soldado {
    String nombre;
    String arma;

    Soldado(String nombre, String arma) {
        this.nombre = nombre;
        ___;
    }
}
```

#### Salida esperada
```
Lía con espada
Teo con lanza
```

#### Solución
```java
public class Palanca {
    public static void main(String[] args) {
        Soldado a = new Soldado("Lía", "espada");
        Soldado b = new Soldado("Teo", "lanza");
        System.out.println(a.nombre + " con " + a.arma);
        System.out.println(b.nombre + " con " + b.arma);
    }
}

class Soldado {
    String nombre;
    String arma;

    Soldado(String nombre, String arma) {
        this.nombre = nombre;
        this.arma = arma;
    }
}
```

#### Al superarla
Los dos soldados salen armados. El aprendiz mira la palanca como si fuera magia. —No es magia —le dice Zed—. Es que el molde no te deja olvidarte.

#### Imagen
- Una palanca de bronce bajando y un soldado completo saliendo del molde con su espada.
- Un aprendiz con las piezas de un soldado desparramadas en la mesa, sorprendido.

### Micro-misión R02-N02-P2 · Los soldados de nadie

```meta
lugar: El taller de los soldados
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
criatura: troll
carta: this | si el parámetro se llama igual que el atributo, nombre = nombre; no guarda nada · this.nombre = nombre; sí
recompensa: xp 15, oro 15
```

#### Escena
El aprendiz escribió su propio constructor. Compila, corre… y todos los soldados salen llamándose `null`. Un **troll** asoma detrás de los moldes, encantado.

#### Gheco sugiere
Adentro del constructor, `nombre` es el **parámetro**. `nombre = nombre;` lo copia sobre sí mismo y el atributo queda en `null`. Para hablar del atributo del objeto se usa `this.nombre`.

#### Desafío
Ejecutalo, mirá los `null` y arreglá las dos asignaciones con `this`.

#### Código inicial
```java
public class Nadie {
    public static void main(String[] args) {
        Soldado s = new Soldado("Lía", "arco");
        System.out.println(s.nombre + " con " + s.arma);
    }
}

class Soldado {
    String nombre;
    String arma;

    Soldado(String nombre, String arma) {
        nombre = nombre;
        arma = arma;
    }
}
```

#### Salida esperada
```
Lía con arco
```

#### Solución
```java
public class Nadie {
    public static void main(String[] args) {
        Soldado s = new Soldado("Lía", "arco");
        System.out.println(s.nombre + " con " + s.arma);
    }
}

class Soldado {
    String nombre;
    String arma;

    Soldado(String nombre, String arma) {
        this.nombre = nombre;
        this.arma = arma;
    }
}
```

#### Al superarla
«Lía con arco.» El troll se esconde de nuevo, decepcionado: sin `null`, no tiene de qué alimentarse.

#### Imagen
- Una fila de soldados de bronce con etiquetas en blanco que dicen «null».
- Un troll espiando detrás de los moldes, sonriendo; Zed señalando la palabra `this` en la pizarra.

### Micro-misión R02-N02-P3 · Dos palancas

```meta
lugar: El taller de los soldados
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: Sobrecarga de constructores | Soldado(String nombre) { this(nombre, "lanza"); } · un constructor llama a otro con this(...) · va en la primera línea
recompensa: xp 15, oro 15
```

#### Escena
La mayoría de los reclutas lleva lanza. La Maestra agrega una segunda palanca: si no decís el arma, sale con lanza. —Pero no copies el código del otro constructor —advierte—. **Llamalo**.

#### Gheco sugiere
Se pueden tener varios constructores con distintos parámetros (sobrecarga). Uno puede llamar a otro con `this(...)`, en su **primera línea**: `this(nombre, "lanza");`.

#### Desafío
Completá la llamada al otro constructor con el arma por defecto, "lanza".

#### Código inicial
```java
public class DosPalancas {
    public static void main(String[] args) {
        Soldado a = new Soldado("Lía", "espada");
        Soldado b = new Soldado("Teo");
        System.out.println(a.nombre + " con " + a.arma);
        System.out.println(b.nombre + " con " + b.arma);
    }
}

class Soldado {
    String nombre;
    String arma;

    Soldado(String nombre, String arma) {
        this.nombre = nombre;
        this.arma = arma;
    }

    Soldado(String nombre) {
        ___;
    }
}
```

#### Salida esperada
```
Lía con espada
Teo con lanza
```

#### Solución
```java
public class DosPalancas {
    public static void main(String[] args) {
        Soldado a = new Soldado("Lía", "espada");
        Soldado b = new Soldado("Teo");
        System.out.println(a.nombre + " con " + a.arma);
        System.out.println(b.nombre + " con " + b.arma);
    }
}

class Soldado {
    String nombre;
    String arma;

    Soldado(String nombre, String arma) {
        this.nombre = nombre;
        this.arma = arma;
    }

    Soldado(String nombre) {
        this(nombre, "lanza");
    }
}
```

#### Al superarla
Teo sale con su lanza sin que nadie se la pida. —Una palanca usa la otra —dice Gheco—. Si mañana cambia cómo se arma un soldado, se cambia en un solo lugar.

#### Imagen
- Dos palancas de bronce conectadas por un engranaje: la chica empuja a la grande.
- Teo, un recluta joven, con una lanza recién salida del molde.

### Micro-misión R02-N02-P4 · El constructor que desapareció

```meta
lugar: El taller de los soldados
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
criatura: goblin
carta: Constructor por defecto | si no escribís ninguno, Java pone uno vacío · si escribís uno, el vacío desaparece · new Soldado() deja de compilar
recompensa: xp 15, oro 15
```

#### Escena
Un **goblin** se ríe en el taller: alguien escribió `new Soldado()` sin datos y el molde no lo acepta. —¡Antes andaba! —protesta el aprendiz. —Antes no había palancas —dice la Maestra.

#### Gheco sugiere
Si una clase no tiene constructores, Java le pone uno **vacío**. Apenas escribís uno con parámetros, ese vacío **desaparece**. Si lo querés, escribilo vos: `Soldado() { this("recluta", "palo"); }`.

#### Desafío
Ejecutalo, leé el error y agregá un constructor sin parámetros que arme un "recluta" con un "palo".

#### Código inicial
```java
public class Desaparecido {
    public static void main(String[] args) {
        Soldado s = new Soldado();
        System.out.println(s.nombre + " con " + s.arma);
    }
}

class Soldado {
    String nombre;
    String arma;

    Soldado(String nombre, String arma) {
        this.nombre = nombre;
        this.arma = arma;
    }
}
```

#### Salida esperada
```
recluta con palo
```

#### Solución
```java
public class Desaparecido {
    public static void main(String[] args) {
        Soldado s = new Soldado();
        System.out.println(s.nombre + " con " + s.arma);
    }
}

class Soldado {
    String nombre;
    String arma;

    Soldado() {
        this("recluta", "palo");
    }

    Soldado(String nombre, String arma) {
        this.nombre = nombre;
        this.arma = arma;
    }
}
```

#### Al superarla
«recluta con palo.» El goblin se va refunfuñando. La Maestra los manda a la tesorería a buscar el pago del día. Zed va adelante: el cofre de la Academia está abierto, a la vista de todos.

#### Imagen
- Un goblin riéndose sobre un molde vacío que no se cierra.
- Un recluta con un palo de madera, orgulloso igual.

### Misión R02-N02-M1 · La poción del alquimista

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Pocion` con nombre, poder (1 a 100) y dosis restantes. Tres
constructores: con los tres datos, con nombre y poder (3 dosis), y solo con nombre
(poder 10, 3 dosis), reutilizando el primero con `this(...)`. El poder se ajusta al
rango 1-100 en el constructor. Un método `int beber()` devuelve el poder si queda
alguna dosis (y descuenta una) o 0 si está vacía. Probá los tres constructores.

#### Criterio de aprobación

- Los constructores usan `this(...)` para no repetir código.
- El poder queda siempre entre 1 y 100.

#### Salida esperada

```
Poción de Vida (poder 40, 2 dosis)
Poción de Furia (poder 100, 3 dosis)
Poción de Agua (poder 10, 3 dosis)
Bebo Vida: +40
Bebo Vida: +40
Bebo Vida: +0
Poción de Vida (poder 40, 0 dosis)
```

#### Solución de referencia

```java
// Mision 1 - La pocion del alquimista: constructores sobrecargados con this(...).
public class Alquimista {
    public static void main(String[] args) {
        Pocion vida = new Pocion("Vida", 40, 2);
        Pocion furia = new Pocion("Furia", 250);
        Pocion agua = new Pocion("Agua");
        System.out.println(vida);
        System.out.println(furia);
        System.out.println(agua);
        System.out.println("Bebo Vida: +" + vida.beber());
        System.out.println("Bebo Vida: +" + vida.beber());
        System.out.println("Bebo Vida: +" + vida.beber());
        System.out.println(vida);
    }
}

class Pocion {
    String nombre;
    int poder;
    int dosis;

    Pocion(String nombre, int poder, int dosis) {
        this.nombre = nombre;
        this.poder = Math.max(1, Math.min(100, poder));
        this.dosis = dosis;
    }

    Pocion(String nombre, int poder) {
        this(nombre, poder, 3);
    }

    Pocion(String nombre) {
        this(nombre, 10);
    }

    int beber() {
        if (dosis == 0) {
            return 0;
        }
        dosis--;
        return poder;
    }

    public String toString() {
        return "Poción de " + nombre + " (poder " + poder + ", " + dosis + " dosis)";
    }
}
```

### Misión R02-N02-M2 · El pasaporte

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Pasaporte` con titular, número y año de vencimiento. El
constructor **rechaza** con `IllegalArgumentException` un titular vacío, un número que
no sea de 8 dígitos o un año anterior a 2026 (con un mensaje claro para cada caso).
En el `main`, intentá crear cuatro pasaportes (uno válido y tres inválidos) dentro de
un `try`/`catch` como el del ejemplo, y mostrá qué pasó con cada uno.

#### Criterio de aprobación

- La validación está en el constructor.
- Cada error tiene su mensaje.

#### Salida esperada

```
Emitido: Nadia Valdez N° 12345678 (vence 2030)
Rechazado: falta el titular
Rechazado: el número tiene que tener 8 dígitos
Rechazado: el pasaporte está vencido
```

#### Solución de referencia

```java
// Mision 2 - El pasaporte: validar en el constructor.
public class Frontera {
    public static void main(String[] args) {
        crear("Nadia Valdez", "12345678", 2030);
        crear("", "12345678", 2030);
        crear("Baldo Tallo", "12-34", 2030);
        crear("Lía Ferrari", "87654321", 2020);
    }

    static void crear(String titular, String numero, int vence) {
        try {
            Pasaporte p = new Pasaporte(titular, numero, vence);
            System.out.println("Emitido: " + p);
        } catch (IllegalArgumentException e) {
            System.out.println("Rechazado: " + e.getMessage());
        }
    }
}

class Pasaporte {
    String titular;
    String numero;
    int vence;

    Pasaporte(String titular, String numero, int vence) {
        if (titular == null || titular.isBlank()) {
            throw new IllegalArgumentException("falta el titular");
        }
        if (numero == null || !numero.matches("\\d{8}")) {
            throw new IllegalArgumentException("el número tiene que tener 8 dígitos");
        }
        if (vence < 2026) {
            throw new IllegalArgumentException("el pasaporte está vencido");
        }
        this.titular = titular;
        this.numero = numero;
        this.vence = vence;
    }

    public String toString() {
        return titular + " N° " + numero + " (vence " + vence + ")";
    }
}
```

### Misión R02-N02-M3 · El reloj de arena

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Duracion` que guarda una cantidad de segundos. Constructores:
`Duracion(int segundos)`, `Duracion(int minutos, int segundos)` y
`Duracion(int horas, int minutos, int segundos)`, todos reutilizando el primero.
Métodos: `Duracion sumar(Duracion otra)` que devuelve **una nueva** duración (sin
cambiar las originales) y `toString` en formato `hh:mm:ss` con ceros (`String.format`).

#### Criterio de aprobación

- Tres constructores encadenados con `this(...)`.
- `sumar` devuelve un objeto nuevo.
- `toString` usa `%02d`.

#### Salida esperada

```
a = 00:01:35
b = 00:12:30
c = 01:59:45
a + b + c = 02:13:50
a sigue siendo 00:01:35
```

#### Solución de referencia

```java
// Mision 3 - El reloj de arena: constructores encadenados y un metodo que devuelve un objeto nuevo.
public class RelojArena {
    public static void main(String[] args) {
        Duracion a = new Duracion(95);
        Duracion b = new Duracion(12, 30);
        Duracion c = new Duracion(1, 59, 45);
        System.out.println("a = " + a);
        System.out.println("b = " + b);
        System.out.println("c = " + c);
        Duracion total = a.sumar(b).sumar(c);
        System.out.println("a + b + c = " + total);
        System.out.println("a sigue siendo " + a);
    }
}

class Duracion {
    int segundos;

    Duracion(int segundos) {
        this.segundos = segundos;
    }

    Duracion(int minutos, int segundos) {
        this(minutos * 60 + segundos);
    }

    Duracion(int horas, int minutos, int segundos) {
        this(horas * 3600 + minutos * 60 + segundos);
    }

    Duracion sumar(Duracion otra) {
        return new Duracion(segundos + otra.segundos);
    }

    public String toString() {
        return String.format("%02d:%02d:%02d", segundos / 3600, segundos % 3600 / 60, segundos % 60);
    }
}
```

### Encargo R02-N02-E1 · El producto del almacén

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un almacén carga productos con código, descripción, precio y stock. Escribí la clase
`Producto` con un constructor completo y otro sin stock (stock 0). El constructor
rechaza precios negativos. Métodos: `vender(int cantidad)` (devuelve el importe o -1
si no hay stock suficiente), `reponer(int cantidad)` y `toString` con el precio con 2
decimales. En el `main`, creá dos productos, vendé, reponé y mostrá los resultados.

#### Criterio de aprobación

- Dos constructores encadenados; el precio se valida.
- `vender` no deja el stock negativo.

#### Salida esperada

```
[YER-1] Yerba 1 kg $4200.50 (stock 10)
[AZU-1] Azúcar 1 kg $1350.00 (stock 0)
Vender 3 yerbas: 12601.5
Vender 1 azúcar: -1.0
Vender 5 azúcar: 6750.0
[YER-1] Yerba 1 kg $4200.50 (stock 7)
[AZU-1] Azúcar 1 kg $1350.00 (stock 15)
```

#### Solución de referencia

```java
// Encargo - El producto del almacen: constructores, validacion y metodos de negocio.
import java.util.Locale;

public class Almacen {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Producto yerba = new Producto("YER-1", "Yerba 1 kg", 4200.5, 10);
        Producto azucar = new Producto("AZU-1", "Azúcar 1 kg", 1350);
        System.out.println(yerba);
        System.out.println(azucar);
        System.out.println("Vender 3 yerbas: " + yerba.vender(3));
        System.out.println("Vender 1 azúcar: " + azucar.vender(1));
        azucar.reponer(20);
        System.out.println("Vender 5 azúcar: " + azucar.vender(5));
        System.out.println(yerba);
        System.out.println(azucar);
    }
}

class Producto {
    String codigo;
    String descripcion;
    double precio;
    int stock;

    Producto(String codigo, String descripcion, double precio, int stock) {
        if (precio < 0) {
            throw new IllegalArgumentException("precio negativo");
        }
        this.codigo = codigo;
        this.descripcion = descripcion;
        this.precio = precio;
        this.stock = stock;
    }

    Producto(String codigo, String descripcion, double precio) {
        this(codigo, descripcion, precio, 0);
    }

    double vender(int cantidad) {
        if (cantidad <= 0 || cantidad > stock) {
            return -1;
        }
        stock -= cantidad;
        return cantidad * precio;
    }

    void reponer(int cantidad) {
        if (cantidad > 0) {
            stock += cantidad;
        }
    }

    public String toString() {
        return String.format("[%s] %s $%.2f (stock %d)", codigo, descripcion, precio, stock);
    }
}
```

### Prueba del sello

#### ¿En qué se diferencia un constructor de un método común?

Se llama igual que la clase, no tiene tipo de retorno y se ejecuta al hacer `new`.

#### ¿Para qué sirve `this.nombre = nombre;`?

Para asignarle al atributo `nombre` el valor del parámetro `nombre`, que lo tapa.

#### ¿Qué hace `this(nombre, 30);` dentro de un constructor?

Llama a otro constructor de la misma clase. Tiene que ser la primera línea.

#### ¿Por qué `new Heroe()` puede dejar de compilar cuando le agregás un constructor a la clase?

Porque el constructor vacío por defecto solo existe si la clase no declara ninguno.

#### ¿Dónde conviene validar los datos de un objeto?

En el constructor: así ningún objeto nace inválido.

### Soluciones (docente)

Sale de `18-Java/10-Constructores-Sobrecarga` (unidad 4). Se adelanta `throw new IllegalArgumentException` y un `try`/`catch` mínimo para validar; la rama 3 los explica a fondo. `Soldado.creados` adelanta los miembros `static` del nodo siguiente.

## R02-N03 · Encapsulamiento y miembros static

```meta
tipo: tema
padre: R02-N02
precio: 10
criatura: troll
temas: poo.encapsulamiento, poo.static
```

### Crónica

En la tesorería de la Academia, el cofre del oro está a la vista de todos, con la tapa abierta. Zed mete la mano por costumbre, saca más de lo que hay y en la etiqueta queda escrito «-500». Nadie sabe cuánto hay. La Maestra no lo reta: le da el molde del cofre. Por primera vez, a Zed le toca arreglar lo que rompió.

—Un objeto que deja tocar sus datos a cualquiera termina así —dice {mentor}—. Se **encapsula**: los datos quedan adentro, bajo llave, y solo se tocan por las ventanillas que el objeto decide abrir. Así el cofre nunca queda en negativo. Ni siquiera con vos cerca.

### Objetivos

- Proteger los atributos con `private` y exponer solo lo necesario.
- Escribir *getters* y *setters* que validan.
- Conocer los cuatro niveles de acceso: `private`, sin modificador, `protected` y `public`.
- Usar atributos y métodos `static` (de la clase, no de cada objeto) y atributos `final`.

### Antes de empezar

- Constructores, this y sobrecarga.

### Explicación

#### El problema: datos a la vista
```java
class Cofre {
    int oro;
}
Cofre c = new Cofre();
c.oro = -500;          // nadie lo impide
```
Si cualquiera puede escribir los atributos, la clase no puede garantizar nada.

#### La solución: `private` + métodos
**Encapsular** es esconder los datos (`private`) y ofrecer métodos que controlan cómo
se leen y se cambian:
```java
class Cofre {
    private int oro;                    // solo se ve dentro de esta clase

    public int getOro() {               // getter: leer
        return oro;
    }

    public void depositar(int monto) {  // cambiar, con reglas
        if (monto <= 0) {
            throw new IllegalArgumentException("el monto tiene que ser positivo");
        }
        oro += monto;
    }
}
c.oro = -500;          // error de compilación: oro has private access in Cofre
```

#### Getters y setters
Por convención, el método que devuelve un atributo se llama `getX()` (o `isX()` si es
`boolean`) y el que lo cambia, `setX(valor)`:
```java
public String getNombre() { return nombre; }
public void setNombre(String nombre) {
    if (nombre == null || nombre.isBlank()) {
        throw new IllegalArgumentException("nombre vacío");
    }
    this.nombre = nombre;
}
public boolean isActivo() { return activo; }
```
No hace falta un setter para cada atributo: si un dato no debe cambiar después de
crear el objeto (un DNI, un código), **no tiene setter**. Y en lugar de un
`setOro` que acepta cualquier valor, suele ser mejor ofrecer operaciones con sentido
(`depositar`, `retirar`).

#### Los cuatro niveles de acceso
| Modificador | Misma clase | Mismo paquete | Subclase (en otro paquete) | Cualquier otro |
|---|---|---|---|---|
| `private` | ✔ | ✘ | ✘ | ✘ |
| *(sin modificador)* | ✔ | ✔ | ✘ | ✘ |
| `protected` | ✔ | ✔ | ✔ | ✘ |
| `public` | ✔ | ✔ | ✔ | ✔ |

Ojo con `protected`: **no** es "solo para las subclases". También lo ven **todas las
clases del mismo paquete**. Un **paquete** es una carpeta de clases relacionadas (se
ven en la rama siguiente). Mientras trabajes con todas las clases en un solo archivo,
todas están en el mismo paquete y la diferencia entre "sin modificador", `protected`
y `public` no se nota: solo `private` esconde de verdad.

La regla práctica: **atributos `private`**; métodos `public` si son para usar desde
afuera y `private` si son ayudantes internos.

#### Miembros `static`: de la clase
Un atributo `static` es **uno solo para toda la clase**, compartido por todos los
objetos. Se usa con el nombre de la clase:
```java
class Soldado {
    private static int creados = 0;     // uno solo, compartido
    private final int numero;           // uno por soldado

    Soldado() {
        creados++;
        numero = creados;
    }

    public static int getCreados() {    // método static: no necesita un objeto
        return creados;
    }
}
Soldado.getCreados();
```
Un método `static` no tiene `this`: no puede usar atributos de instancia (¿de qué
objeto serían?). Por eso `main` y los métodos que usabas en la rama 1 eran `static`.
`Math.sqrt` e `Integer.parseInt` son métodos `static` de sus clases.

#### Atributos `final`
Un atributo `final` se asigna **una sola vez** (al declararlo o en el constructor) y
después no cambia. Es ideal para identificadores:
```java
private final String dni;
```
Las constantes de la clase son `static final`, con nombre en mayúsculas:
`public static final int VIDA_MAXIMA = 100;`.

> **Si venís de Python.** En Python "privado" es una convención (`_oro`); en Java
> es una regla que controla el compilador.

### Código de ejemplo

```java
/*
 * Encapsulamiento y static: la tesorería de la Academia.
 */
public class Tesoreria {
    public static void main(String[] args) {
        CuentaImperial nadia = new CuentaImperial("Nadia", 100);
        CuentaImperial baldo = new CuentaImperial("Baldo");

        nadia.depositar(50);
        baldo.depositar(30);
        System.out.println(nadia);
        System.out.println(baldo);

        System.out.println("¿Nadia puede pagar 500? " + nadia.retirar(500));
        System.out.println("¿Nadia puede pagar 120? " + nadia.retirar(120));
        System.out.println(nadia);

        try {
            baldo.depositar(-40);
        } catch (IllegalArgumentException e) {
            System.out.println("Depósito rechazado: " + e.getMessage());
        }

        nadia.setTitular("Nadia Valdez");
        System.out.println("Titular: " + nadia.getTitular() + ", número " + nadia.getNumero());
        System.out.println("Cuentas abiertas: " + CuentaImperial.getCuentasAbiertas());
        System.out.println("Oro total del Imperio: " + CuentaImperial.getOroTotal());
        System.out.println("Límite por retiro: " + CuentaImperial.LIMITE_RETIRO);
        // nadia.saldo = 1_000_000;   // no compila: saldo has private access in CuentaImperial
    }
}

class CuentaImperial {
    public static final int LIMITE_RETIRO = 200;   // constante de la clase
    private static int cuentasAbiertas = 0;         // compartido por todas las cuentas
    private static int oroTotal = 0;

    private final int numero;                       // no cambia nunca
    private String titular;
    private int saldo;

    public CuentaImperial(String titular, int saldoInicial) {
        setTitular(titular);
        cuentasAbiertas++;
        numero = 1000 + cuentasAbiertas;
        depositar(saldoInicial);
    }

    public CuentaImperial(String titular) {
        setTitular(titular);
        cuentasAbiertas++;
        numero = 1000 + cuentasAbiertas;
    }

    public int getNumero() {
        return numero;
    }

    public String getTitular() {
        return titular;
    }

    public void setTitular(String titular) {
        if (titular == null || titular.isBlank()) {
            throw new IllegalArgumentException("titular vacío");
        }
        this.titular = titular.trim();
    }

    public int getSaldo() {
        return saldo;
    }

    public void depositar(int monto) {
        if (monto <= 0) {
            throw new IllegalArgumentException("el monto tiene que ser positivo");
        }
        saldo += monto;
        oroTotal += monto;
    }

    public boolean retirar(int monto) {
        if (monto <= 0 || monto > saldo || monto > LIMITE_RETIRO) {
            return false;
        }
        saldo -= monto;
        oroTotal -= monto;
        return true;
    }

    public static int getCuentasAbiertas() {
        return cuentasAbiertas;
    }

    public static int getOroTotal() {
        return oroTotal;
    }

    public String toString() {
        return "Cuenta " + numero + " de " + titular + ": " + saldo + " denarios";
    }
}
```

### Salida esperada

```
Cuenta 1001 de Nadia: 150 denarios
Cuenta 1002 de Baldo: 30 denarios
¿Nadia puede pagar 500? false
¿Nadia puede pagar 120? true
Cuenta 1001 de Nadia: 30 denarios
Depósito rechazado: el monto tiene que ser positivo
Titular: Nadia Valdez, número 1001
Cuentas abiertas: 2
Oro total del Imperio: 60
Límite por retiro: 200
```

### ¿Para qué sirve?

El encapsulamiento es lo que permite que un sistema grande no se desarme: una `Cuenta` bancaria nunca queda con saldo imposible, un `Turno` no puede tener una fecha pasada, un `Stock` no baja de cero. Si la regla cambia, se cambia en un solo método. Los `static` se usan para contadores, constantes y utilidades que no dependen de un objeto (como `Math`).

### Errores habituales

**Esqueleto: acceder a un atributo privado desde afuera.**
```
Tesoreria.java:22: error: saldo has private access in CuentaImperial
        nadia.saldo = 1_000_000;
            ^
```
Usá los métodos públicos de la clase.

**Esqueleto: usar un atributo de instancia desde un método `static`.**
`non-static variable saldo cannot be referenced from a static context`: un método
`static` no tiene objeto.

**Ogro: el setter que no valida.** Un `setVida(int vida) { this.vida = vida; }` para
cada atributo es casi lo mismo que dejarlos públicos. Validá, o no pongas setter.

**Ogro: creer que `protected` es solo para subclases.** También lo ve todo el
paquete.

**Slime: asignar un `final` dos veces.** `cannot assign a value to final variable
numero`.

### Micro-misión R02-N03-P1 · El cofre en negativo

```meta
lugar: La tesorería de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: private | private int saldo; · nadie de afuera lo toca · se cambia solo por los métodos del objeto, que validan
recompensa: xp 10, oro 15
```

#### Escena
El cofre de la tesorería está abierto y Zed, por costumbre, mete la mano. Saca más de lo que hay y en la etiqueta queda escrito **«-500»**. La Maestra no lo reta: le da el molde del cofre. —Lo rompiste vos. Arreglalo vos: que **nadie**, ni vos, lo pueda dejar en negativo.

#### Gheco sugiere
Con `private int saldo;` el saldo solo se toca desde **adentro** de la clase. Desde afuera se usa `retirar(monto)`, que puede negarse: si el monto es mayor que el saldo, devuelve `false` y no cambia nada.

#### Desafío
Completá la condición: no se puede retirar más de lo que hay.

#### Código inicial
```java
public class Tesoreria {
    public static void main(String[] args) {
        Cofre cofre = new Cofre(300);
        System.out.println("Retiro 200: " + cofre.retirar(200));
        System.out.println("Retiro 500: " + cofre.retirar(500));
        System.out.println("Saldo: " + cofre.getSaldo());
    }
}

class Cofre {
    private int saldo;

    Cofre(int saldoInicial) {
        saldo = saldoInicial;
    }

    boolean retirar(int monto) {
        if (___) {
            return false;
        }
        saldo -= monto;
        return true;
    }

    int getSaldo() {
        return saldo;
    }
}
```

#### Salida esperada
```
Retiro 200: true
Retiro 500: false
Saldo: 100
```

#### Solución
```java
public class Tesoreria {
    public static void main(String[] args) {
        Cofre cofre = new Cofre(300);
        System.out.println("Retiro 200: " + cofre.retirar(200));
        System.out.println("Retiro 500: " + cofre.retirar(500));
        System.out.println("Saldo: " + cofre.getSaldo());
    }
}

class Cofre {
    private int saldo;

    Cofre(int saldoInicial) {
        saldo = saldoInicial;
    }

    boolean retirar(int monto) {
        if (monto > saldo) {
            return false;
        }
        saldo -= monto;
        return true;
    }

    int getSaldo() {
        return saldo;
    }
}
```

#### Al superarla
El segundo retiro rebota y el cofre queda en 100. Zed lo cierra él mismo. Es la primera vez que arregla algo que rompió, y no se siente mal: se siente raro.

#### Imagen
- Un cofre de bronce cerrado con candado, con una etiqueta que dice «100» y otra vieja tachada que decía «-500».
- Zed cerrando el cofre; la Maestra de Moldes mirándolo con los brazos cruzados, aprobando.

### Micro-misión R02-N03-P2 · La ventanilla de lectura

```meta
lugar: La tesorería de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
criatura: troll
carta: Getter | int getSaldo() { return saldo; } · deja LEER sin dejar tocar · desde afuera: cofre.getSaldo(), nunca cofre.saldo
recompensa: xp 10, oro 10
```

#### Escena
Nadia quiere anotar el saldo en su libreta y escribe `cofre.saldo`. La Aduana del compilador la frena: **`saldo has private access`**. —Hasta el reglamento me cierra la puerta —protesta.

#### Gheco sugiere
Un atributo `private` no se lee desde otra clase. Para eso el objeto abre una **ventanilla de lectura**, un *getter*: `getSaldo()`. Desde afuera se usa siempre el método.

#### Desafío
Ejecutalo, leé el error y cambiá `cofre.saldo` por el getter.

#### Código inicial
```java
public class Ventanilla {
    public static void main(String[] args) {
        Cofre cofre = new Cofre(250);
        System.out.println("Saldo para la libreta: " + cofre.saldo);
    }
}

class Cofre {
    private int saldo;

    Cofre(int saldoInicial) {
        saldo = saldoInicial;
    }

    int getSaldo() {
        return saldo;
    }
}
```

#### Salida esperada
```
Saldo para la libreta: 250
```

#### Solución
```java
public class Ventanilla {
    public static void main(String[] args) {
        Cofre cofre = new Cofre(250);
        System.out.println("Saldo para la libreta: " + cofre.getSaldo());
    }
}

class Cofre {
    private int saldo;

    Cofre(int saldoInicial) {
        saldo = saldoInicial;
    }

    int getSaldo() {
        return saldo;
    }
}
```

#### Al superarla
Nadia anota «250» con letra prolija. —Así me gusta —dice—: una ventanilla, un reglamento, nadie metiendo la mano.

#### Imagen
- Una ventanilla pequeña en el cofre de bronce por la que se ve un número, sin poder meter la mano.
- Nadia escribiendo en su libreta, satisfecha.

### Micro-misión R02-N03-P3 · La lista de inscriptos

```meta
lugar: La entrada de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: static | static int inscriptos; es UNO para toda la clase · lo comparten todos los objetos · se usa Alumno.inscriptos
recompensa: xp 15, oro 15
```

#### Escena
En la entrada, la Maestra quiere saber cuántos alumnos se inscribieron hoy. Cada alumno tiene su nombre, pero el número de inscriptos no es de ninguno: es **de la Academia**.

#### Gheco sugiere
Un atributo `static` es **de la clase**, no de cada objeto: hay uno solo, compartido. Si el constructor hace `inscriptos++`, cada `new` suma uno al mismo contador. Desde afuera se lee con el nombre de la clase: `Alumno.inscriptos`.

#### Desafío
Completá la declaración para que el contador sea uno solo para toda la clase.

#### Código inicial
```java
public class Inscripcion {
    public static void main(String[] args) {
        Alumno a = new Alumno("Zed");
        Alumno b = new Alumno("Nadia");
        Alumno c = new Alumno("Teo");
        System.out.println(a.nombre + ", " + b.nombre + " y " + c.nombre);
        System.out.println("Inscriptos: " + Alumno.inscriptos);
    }
}

class Alumno {
    ___ int inscriptos = 0;
    String nombre;

    Alumno(String nombre) {
        this.nombre = nombre;
        inscriptos++;
    }
}
```

#### Salida esperada
```
Zed, Nadia y Teo
Inscriptos: 3
```

#### Solución
```java
public class Inscripcion {
    public static void main(String[] args) {
        Alumno a = new Alumno("Zed");
        Alumno b = new Alumno("Nadia");
        Alumno c = new Alumno("Teo");
        System.out.println(a.nombre + ", " + b.nombre + " y " + c.nombre);
        System.out.println("Inscriptos: " + Alumno.inscriptos);
    }
}

class Alumno {
    static int inscriptos = 0;
    String nombre;

    Alumno(String nombre) {
        this.nombre = nombre;
        inscriptos++;
    }
}
```

#### Al superarla
«Inscriptos: 3.» —¿Nadia también se inscribió? —pregunta Zed. —Alguien tiene que vigilarte adentro —responde ella, sin mirarlo.

#### Imagen
- Un libro de inscripción gigante en la entrada de la Academia, con un contador de bronce que marca 3.
- Nadia firmando el libro; Zed sorprendido.

### Micro-misión R02-N03-P4 · La tasa que no se toca

```meta
lugar: La tesorería de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: final | static final double TASA = 0.10; · una constante: no se puede cambiar · en mayúsculas por costumbre
recompensa: xp 15, oro 15
```

#### Escena
La Academia cobra una tasa del 10 % sobre cada molde vendido. Zed, viejas mañas, intenta bajarla a escondidas desde el `main`. La Aduana del compilador lo atrapa en el acto.

#### Gheco sugiere
Un atributo `final` no se puede volver a asignar: `static final double TASA = 0.10;` es una **constante**. Si alguien escribe `Tesoro.TASA = 0.01;`, no compila. La solución no es pelear con el compilador: es **sacar** esa línea.

#### Desafío
Ejecutalo, leé el error y borrá la línea de la trampa.

#### Código inicial
```java
public class Tasa {
    public static void main(String[] args) {
        Tesoro.TASA = 0.01;
        double venta = 400;
        System.out.println("Venta: " + venta);
        System.out.println("Tasa: " + venta * Tesoro.TASA);
    }
}

class Tesoro {
    static final double TASA = 0.10;
}
```

#### Salida esperada
```
Venta: 400.0
Tasa: 40.0
```

#### Solución
```java
public class Tasa {
    public static void main(String[] args) {
        double venta = 400;
        System.out.println("Venta: " + venta);
        System.out.println("Tasa: " + venta * Tesoro.TASA);
    }
}

class Tesoro {
    static final double TASA = 0.10;
}
```

#### Al superarla
Cuarenta denarios de tasa, como dice el reglamento. —Ni lo intentes otra vez —dice Nadia, y por primera vez Zed no lo intenta.
En el depósito de la Academia, dos alumnos discuten frente a un escudo dorado abollado. Cada uno jura que no lo tocó.

#### Imagen
- Una placa de bronce atornillada en la pared de la tesorería: «TASA 10 %», con un candado.
- Zed con las manos en los bolsillos; Nadia vigilándolo.

### Misión R02-N03-M1 · El termómetro sellado

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Termometro` con la temperatura `private` en grados Celsius. El
constructor y el setter rechazan temperaturas por debajo de -273.15 (el cero
absoluto). Getters: `getCelsius()`, `getFahrenheit()` y `getKelvin()` (calculados, no
guardados). Un método `static double aCelsius(double fahrenheit)` convierte sin
necesitar un objeto. En el `main`, probá todo, incluido un valor inválido.

#### Criterio de aprobación

- La temperatura es `private` y se valida en constructor y setter.
- Fahrenheit y Kelvin se calculan en los getters.
- `aCelsius` es `static` y se llama con el nombre de la clase.

#### Salida esperada

```
25.00 C = 77.00 F = 298.15 K
-10.50 C = 13.10 F = 262.65 K
98.6 F son 37.00 C
Rechazado: no existe una temperatura menor al cero absoluto
Sigue en -10.50 C
```

#### Solución de referencia

```java
// Mision 1 - El termometro sellado: atributo privado, getters calculados y un metodo static.
import java.util.Locale;

public class Laboratorio {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Termometro t = new Termometro(25);
        System.out.printf("%.2f C = %.2f F = %.2f K%n", t.getCelsius(), t.getFahrenheit(), t.getKelvin());
        t.setCelsius(-10.5);
        System.out.printf("%.2f C = %.2f F = %.2f K%n", t.getCelsius(), t.getFahrenheit(), t.getKelvin());
        System.out.printf("98.6 F son %.2f C%n", Termometro.aCelsius(98.6));
        try {
            t.setCelsius(-300);
        } catch (IllegalArgumentException e) {
            System.out.println("Rechazado: " + e.getMessage());
        }
        System.out.printf("Sigue en %.2f C%n", t.getCelsius());
    }
}

class Termometro {
    private double celsius;

    public Termometro(double celsius) {
        setCelsius(celsius);
    }

    public double getCelsius() {
        return celsius;
    }

    public void setCelsius(double celsius) {
        if (celsius < -273.15) {
            throw new IllegalArgumentException("no existe una temperatura menor al cero absoluto");
        }
        this.celsius = celsius;
    }

    public double getFahrenheit() {
        return celsius * 9 / 5 + 32;
    }

    public double getKelvin() {
        return celsius + 273.15;
    }

    public static double aCelsius(double fahrenheit) {
        return (fahrenheit - 32) * 5 / 9;
    }
}
```

### Misión R02-N03-M2 · El registro de reclutas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Recluta` con nombre y un número de legajo `final` que se asigna
solo, en orden (1, 2, 3…), usando un contador `static`. Agregá un atributo `static`
que cuente cuántos reclutas están activos y un método `darDeBaja()` que lo descuente
(una sola vez por recluta). Mostrá los legajos y los contadores después de crear
cuatro reclutas y dar de baja a uno (dos veces, para ver que no descuenta de más).

#### Criterio de aprobación

- El legajo es `final` y sale de un contador `static`.
- `darDeBaja` no descuenta dos veces al mismo recluta.

#### Salida esperada

```
#1 Pip, #2 Lía, #3 Olmo, #4 Nara
Activos: 4
#2 Lía (baja)
Activos: 3 de 4
```

#### Solución de referencia

```java
// Mision 2 - El registro de reclutas: contadores static y un atributo final.
public class Reclutamiento {
    public static void main(String[] args) {
        Recluta a = new Recluta("Pip");
        Recluta b = new Recluta("Lía");
        Recluta c = new Recluta("Olmo");
        Recluta d = new Recluta("Nara");
        System.out.println(a + ", " + b + ", " + c + ", " + d);
        System.out.println("Activos: " + Recluta.getActivos());
        b.darDeBaja();
        b.darDeBaja();
        System.out.println(b);
        System.out.println("Activos: " + Recluta.getActivos() + " de " + Recluta.getTotal());
    }
}

class Recluta {
    private static int total = 0;
    private static int activos = 0;

    private final int legajo;
    private final String nombre;
    private boolean activo = true;

    public Recluta(String nombre) {
        this.nombre = nombre;
        total++;
        activos++;
        legajo = total;
    }

    public void darDeBaja() {
        if (activo) {
            activo = false;
            activos--;
        }
    }

    public static int getActivos() {
        return activos;
    }

    public static int getTotal() {
        return total;
    }

    public String toString() {
        return "#" + legajo + " " + nombre + (activo ? "" : " (baja)");
    }
}
```

### Misión R02-N03-M3 · El inventario encapsulado

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Mochila` con un array `private` de `String` de capacidad fija (se
pasa al constructor) y la cantidad de objetos. Métodos: `boolean guardar(String
objeto)` (falso si está llena o el objeto está vacío), `boolean sacar(String
objeto)` (lo busca con `equals` y corre los siguientes un lugar), `int getCantidad()`,
`boolean contiene(String objeto)` y `toString`. **Nadie de afuera puede tocar el
array.** Probala en el `main`.

#### Criterio de aprobación

- El array es `private` y no hay un getter que lo devuelva.
- `sacar` compara con `equals` y no deja huecos.

#### Salida esperada

```
true true true false
[mapa, pan, soga]
¿Tiene pan? true
Sacar pan: true
Sacar oro: false
[mapa, soga] (2 objetos)
Guardar vela: true
[mapa, soga, vela]
```

#### Solución de referencia

```java
// Mision 3 - El inventario encapsulado: un array privado detras de metodos.
public class Viaje {
    public static void main(String[] args) {
        Mochila m = new Mochila(3);
        System.out.println(m.guardar("mapa") + " " + m.guardar("pan") + " " + m.guardar("soga") + " " + m.guardar("vela"));
        System.out.println(m);
        System.out.println("¿Tiene pan? " + m.contiene("pan"));
        System.out.println("Sacar pan: " + m.sacar("pan"));
        System.out.println("Sacar oro: " + m.sacar("oro"));
        System.out.println(m + " (" + m.getCantidad() + " objetos)");
        System.out.println("Guardar vela: " + m.guardar("vela"));
        System.out.println(m);
    }
}

class Mochila {
    private final String[] objetos;
    private int cantidad;

    public Mochila(int capacidad) {
        objetos = new String[capacidad];
    }

    public boolean guardar(String objeto) {
        if (objeto == null || objeto.isBlank() || cantidad == objetos.length) {
            return false;
        }
        objetos[cantidad] = objeto;
        cantidad++;
        return true;
    }

    public boolean sacar(String objeto) {
        for (int i = 0; i < cantidad; i++) {
            if (objetos[i].equals(objeto)) {
                for (int j = i; j < cantidad - 1; j++) {
                    objetos[j] = objetos[j + 1];
                }
                cantidad--;
                objetos[cantidad] = null;
                return true;
            }
        }
        return false;
    }

    public boolean contiene(String objeto) {
        for (int i = 0; i < cantidad; i++) {
            if (objetos[i].equals(objeto)) {
                return true;
            }
        }
        return false;
    }

    public int getCantidad() {
        return cantidad;
    }

    public String toString() {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < cantidad; i++) {
            if (i > 0) {
                sb.append(", ");
            }
            sb.append(objetos[i]);
        }
        return sb.append("]").toString();
    }
}
```

### Encargo R02-N03-E1 · La tarjeta SUBE

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Modelá una tarjeta de transporte: número (final, generado con un contador `static`
empezando en 6061), saldo `private`, y un saldo negativo permitido de hasta -1000
(constante `static final`). `cargar(double monto)` acepta montos positivos;
`boolean viajar(double tarifa)` solo cobra si el saldo no queda por debajo del
límite. Mostrá con 2 decimales. En el `main`, cargá, viajá varias veces hasta que no
alcance.

#### Criterio de aprobación

- El saldo es `private` y solo cambia por los métodos.
- El límite negativo es una constante `static final`.

#### Salida esperada

```
Tarjeta 6061, saldo $1500.00
Viaje 1: Tarjeta 6061, saldo $800.00
Viaje 2: Tarjeta 6061, saldo $100.00
Viaje 3: Tarjeta 6061, saldo $-600.00
No alcanza para otro viaje. Tarjeta 6061, saldo $-600.00
Otra tarjeta: Tarjeta 6062, saldo $0.00
```

#### Solución de referencia

```java
// Encargo - La tarjeta SUBE: encapsulamiento, constante static final y contador static.
import java.util.Locale;

public class Colectivo {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Tarjeta t = new Tarjeta();
        t.cargar(1500);
        System.out.println(t);
        int viajes = 0;
        while (t.viajar(700)) {
            viajes++;
            System.out.println("Viaje " + viajes + ": " + t);
        }
        System.out.println("No alcanza para otro viaje. " + t);
        System.out.println("Otra tarjeta: " + new Tarjeta());
    }
}

class Tarjeta {
    public static final double LIMITE_NEGATIVO = -1000;
    private static int ultimoNumero = 6060;

    private final int numero;
    private double saldo;

    public Tarjeta() {
        ultimoNumero++;
        numero = ultimoNumero;
    }

    public void cargar(double monto) {
        if (monto > 0) {
            saldo += monto;
        }
    }

    public boolean viajar(double tarifa) {
        if (saldo - tarifa < LIMITE_NEGATIVO) {
            return false;
        }
        saldo -= tarifa;
        return true;
    }

    public String toString() {
        return String.format("Tarjeta %d, saldo $%.2f", numero, saldo);
    }
}
```

### Prueba del sello

#### ¿Qué es encapsular?

Esconder los datos del objeto (`private`) y permitir usarlos solo a través de métodos que controlan las reglas.

#### ¿Quién puede ver un atributo `protected`?

La misma clase, todas las clases del mismo paquete y las subclases (aunque estén en otro paquete).

#### ¿Qué diferencia hay entre un atributo `static` y uno común?

El `static` es uno solo, compartido por toda la clase; el común es uno por objeto.

#### ¿Por qué un método `static` no puede usar `this`?

Porque se llama sin objeto: no hay un "este" objeto.

#### ¿Siempre conviene un setter para cada atributo?

No. Si un dato no debe cambiar (un DNI), no lleva setter; y muchas veces es mejor un método con sentido (`depositar`) que un `setSaldo`.

### Soluciones (docente)

Sale de `18-Java/11-Encapsulamiento-Acceso` (unidad 1). Corrige el error del capítulo original, que decía que `protected` era "solo para subclases": la tabla muestra que también lo ve el paquete. La diferencia entre paquetes se demuestra en la rama 3 (Paquetes y `.jar`).

## R02-N04 · Referencias, null y equals

```meta
tipo: tema
padre: R02-N03
precio: 10
criatura: troll
temas: prog.referencias
```

### Crónica

En el depósito de la Academia hay un solo escudo dorado. Dos alumnos tienen una tarjeta que dice «escudo dorado, estante 7». Uno lo lleva a pulir y lo abolla en el camino. El otro va al estante, lo ve abollado y no entiende nada: *¡si yo no lo toqué!*

—Las dos tarjetas señalaban **el mismo escudo** —dice {mentor}—. Eso es una **referencia**: no es el objeto, es la dirección donde está. Si no lo entendés, Zed, el troll te va a dar sorpresas toda la vida.

### Objetivos

- Entender que las variables de tipo clase guardan referencias, no objetos.
- Reconocer los alias y el estado compartido.
- Manejar `null` y evitar el `NullPointerException`.
- Distinguir identidad (`==`) de igualdad (`equals`) y escribir `equals` y `hashCode`.

### Antes de empezar

- Encapsulamiento y miembros static.

### Explicación

#### Primitivos y referencias
Una variable de tipo **primitivo** (`int`, `double`, `boolean`…) guarda el **valor**.
Una variable de tipo **clase** (`String`, `Heroe`, un array) guarda una
**referencia**: la dirección del objeto.
```java
int a = 5;
int b = a;          // b recibe una copia del 5
b = 9;              // a sigue en 5

Heroe h1 = new Heroe("Nadia", 30);
Heroe h2 = h1;      // h2 recibe una copia de la REFERENCIA: apunta al mismo héroe
h2.recibirDanio(10);
System.out.println(h1.getVida());   // 20: es el mismo objeto
```
`h1` y `h2` son **alias**: dos nombres para el mismo objeto. Para tener dos objetos
distintos hay que crear otro con `new` (por ejemplo, con un constructor de copia).

#### Pasar objetos a métodos
Como con los arrays, al pasar un objeto se copia la referencia: el método puede
**cambiar el objeto** (y el cambio se ve afuera), pero si hace `param = new
Heroe(...)`, eso no afecta a la variable de afuera.

#### `null`: la referencia que no apunta a nada
```java
Heroe nadie = null;
nadie.getVida();         // NullPointerException
```
`null` es el valor de una referencia sin objeto: los atributos de tipo clase y los
lugares de `new Heroe[3]` empiezan así. Mandarle un mensaje a `null` corta el programa
con `NullPointerException`. Java moderno dice qué era `null`:
```
Exception in thread "main" java.lang.NullPointerException: Cannot invoke "Heroe.getVida()" because "nadie" is null
```
Se evita **preguntando antes** (`if (h != null)`) o, mejor, diseñando para que no
haya `null` (constructores que exigen todos los datos).

#### Identidad (`==`) e igualdad (`equals`)
- `a == b` entre objetos pregunta si son **el mismo objeto** (la misma dirección).
- `a.equals(b)` pregunta si son **iguales** según lo que decida la clase.

Toda clase hereda un `equals` de la clase `Object` (la madre de todas; se ve en el
nodo de herencia), que por defecto hace lo mismo que `==`. Para que dos objetos con
los mismos datos sean iguales, la clase **redefine** `equals`:
```java
@Override
public boolean equals(Object otro) {
    if (this == otro) return true;                       // el mismo objeto
    if (!(otro instanceof Moneda)) return false;         // null o de otra clase
    Moneda m = (Moneda) otro;                            // ahora sé que es una Moneda
    return valor == m.valor && metal.equals(m.metal);
}
```
`@Override` avisa que estás redefiniendo un método que ya existe: si te equivocás en
el nombre o los parámetros, el compilador te lo marca. `instanceof` pregunta si un
objeto es de una clase (y da `false` con `null`).

#### `hashCode` va con `equals`
Si redefinís `equals`, redefiní también `hashCode`: dos objetos iguales tienen que
tener el mismo `hashCode`. Lo usan los mapas y conjuntos (`HashMap`, `HashSet`, en la
rama siguiente); si no coincide, ahí se comportan mal.
```java
@Override
public int hashCode() {
    return Objects.hash(valor, metal);      // import java.util.Objects;
}
```
`Objects.equals(a, b)` también es útil: compara sin romperse si alguno es `null`.

> **Si venís de C.** Una referencia es parecida a un puntero, pero no se puede hacer
> aritmética ni apuntar a cualquier lado, y la memoria se libera sola cuando ya nadie
> apunta al objeto.
>
> **Si venís de Python.** Es exactamente como en Python: las variables son etiquetas
> que apuntan a objetos. `==` de Java es `is` de Python, y `equals` es `==`.

### Código de ejemplo

```java
/*
 * Referencias, null y equals: el escudo del estante 7.
 */
import java.util.Objects;

public class Referencias {
    public static void main(String[] args) {
        // Primitivos: se copia el valor
        int a = 5;
        int b = a;
        b = 9;
        System.out.println("a = " + a + ", b = " + b);

        // Objetos: se copia la referencia (alias)
        Escudo dorado = new Escudo("dorado", 100);
        Escudo tarjeta2 = dorado;
        tarjeta2.abollar(35);
        System.out.println("El original después de abollar el alias: " + dorado);
        System.out.println("¿Mismo objeto? " + (dorado == tarjeta2));

        // Una copia de verdad
        Escudo copia = new Escudo(dorado);
        copia.abollar(10);
        System.out.println("Original " + dorado + ", copia " + copia);

        // Un método recibe la referencia: puede cambiar el objeto...
        pulir(dorado);
        System.out.println("Después de pulir: " + dorado);
        // ...pero reasignar el parámetro no cambia la variable de afuera
        reemplazar(dorado);
        System.out.println("Después de reemplazar: " + dorado);

        // null
        Escudo[] estante = new Escudo[3];
        estante[0] = dorado;
        for (int i = 0; i < estante.length; i++) {
            if (estante[i] != null) {
                System.out.println("Estante " + i + ": " + estante[i]);
            } else {
                System.out.println("Estante " + i + ": vacío");
            }
        }

        // == contra equals
        Moneda m1 = new Moneda(10, "plata");
        Moneda m2 = new Moneda(10, "plata");
        Moneda m3 = new Moneda(5, "plata");
        System.out.println("m1 == m2: " + (m1 == m2));
        System.out.println("m1.equals(m2): " + m1.equals(m2));
        System.out.println("m1.equals(m3): " + m1.equals(m3));
        System.out.println("m1.equals(null): " + m1.equals(null));
        System.out.println("Mismo hashCode m1 y m2: " + (m1.hashCode() == m2.hashCode()));
    }

    static void pulir(Escudo e) {
        e.reparar(20);
    }

    static void reemplazar(Escudo e) {
        e = new Escudo("de madera", 30);    // solo cambia la copia de la referencia
    }
}

class Escudo {
    private final String tipo;
    private int integridad;

    public Escudo(String tipo, int integridad) {
        this.tipo = tipo;
        this.integridad = integridad;
    }

    public Escudo(Escudo otro) {
        this(otro.tipo, otro.integridad);
    }

    public void abollar(int golpe) {
        integridad = Math.max(0, integridad - golpe);
    }

    public void reparar(int puntos) {
        integridad = Math.min(100, integridad + puntos);
    }

    @Override
    public String toString() {
        return "escudo " + tipo + " (" + integridad + "%)";
    }
}

class Moneda {
    private final int valor;
    private final String metal;

    public Moneda(int valor, String metal) {
        this.valor = valor;
        this.metal = metal;
    }

    @Override
    public boolean equals(Object otro) {
        if (this == otro) {
            return true;
        }
        if (!(otro instanceof Moneda)) {
            return false;
        }
        Moneda m = (Moneda) otro;
        return valor == m.valor && metal.equals(m.metal);
    }

    @Override
    public int hashCode() {
        return Objects.hash(valor, metal);
    }
}
```

### Salida esperada

```
a = 5, b = 9
El original después de abollar el alias: escudo dorado (65%)
¿Mismo objeto? true
Original escudo dorado (65%), copia escudo dorado (55%)
Después de pulir: escudo dorado (85%)
Después de reemplazar: escudo dorado (85%)
Estante 0: escudo dorado (85%)
Estante 1: vacío
Estante 2: vacío
m1 == m2: false
m1.equals(m2): true
m1.equals(m3): false
m1.equals(null): false
Mismo hashCode m1 y m2: true
```

### ¿Para qué sirve?

Entender las referencias evita los errores más desconcertantes de Java: un dato que "cambia solo" porque otra parte del programa tenía un alias, una lista que se modificó desde otro lado, un `NullPointerException` en producción. Y `equals`/`hashCode` bien escritos son necesarios para buscar objetos en listas, mapas y conjuntos, y para comparar registros que vienen de una base de datos.

### Errores habituales

**Troll: el `NullPointerException`.**
```
Exception in thread "main" java.lang.NullPointerException: Cannot invoke "Escudo.abollar(int)" because "estante[1]" is null
        at Referencias.main(Referencias.java:30)
```
El mensaje dice qué referencia era `null`: revisá dónde debería haberse creado.

**Troll: el alias inesperado.** Guardar el mismo objeto en dos lugares y
modificarlo en uno. Si necesitás objetos independientes, creá una copia.

**Ogro: comparar objetos con `==`.** Da `false` aunque tengan los mismos datos. Va
`equals` (y la clase tiene que redefinirlo).

**Ogro: `equals(Moneda otra)` en lugar de `equals(Object otro)`.** Eso es una
sobrecarga, no una redefinición: las colecciones siguen usando el `equals` viejo. Con
`@Override` el compilador lo detecta: `method does not override or implement a
method from a supertype`.

**Ogro: `equals` sin `hashCode`.** Funciona en una lista, pero en un `HashSet` dos
objetos iguales pueden aparecer duplicados.

### Micro-misión R02-N04-P1 · El escudo abollado

```meta
lugar: El depósito de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
criatura: troll
carta: Referencia | Escudo b = a; NO copia el escudo: las dos variables señalan el MISMO objeto · para otro escudo, otro new
recompensa: xp 10, oro 10
```

#### Escena
Dos alumnos tienen una tarjeta que dice «escudo dorado, estante 7». Uno lo lleva a pulir y lo abolla. El otro va al estante, lo ve abollado y no entiende nada. Un **troll** se ríe desde el estante.
—Las dos tarjetas señalaban **el mismo escudo** —dice Gheco.

#### Gheco sugiere
Una variable de tipo clase guarda una **referencia**: la dirección del objeto, no el objeto. `Escudo b = a;` hace que `b` señale al mismo escudo que `a`. Para que cada uno tenga el suyo, `b` necesita su propio `new`.

#### Desafío
Ejecutalo y fijate que se abollan los dos. Después hacé que `b` sea un escudo nuevo.

#### Código inicial
```java
public class Escudos {
    public static void main(String[] args) {
        Escudo a = new Escudo();
        Escudo b = a;
        b.abollado = true;
        System.out.println("Escudo de a abollado: " + a.abollado);
        System.out.println("Escudo de b abollado: " + b.abollado);
    }
}

class Escudo {
    boolean abollado;
}
```

#### Salida esperada
```
Escudo de a abollado: false
Escudo de b abollado: true
```

#### Solución
```java
public class Escudos {
    public static void main(String[] args) {
        Escudo a = new Escudo();
        Escudo b = new Escudo();
        b.abollado = true;
        System.out.println("Escudo de a abollado: " + a.abollado);
        System.out.println("Escudo de b abollado: " + b.abollado);
    }
}

class Escudo {
    boolean abollado;
}
```

#### Al superarla
Ahora hay dos escudos, y solo uno abollado. Los alumnos se dan la mano. El troll, aburrido, se mete en otro estante.

#### Imagen
- Dos tarjetas con flechas de luz que apuntan al mismo escudo dorado abollado.
- Un troll riéndose desde un estante alto; Zed con un escudo nuevo en la mano.

### Micro-misión R02-N04-P2 · El viajero que no estaba

```meta
lugar: El registro de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
criatura: troll
carta: null | una referencia que no señala nada · v.metodo() con v null da NullPointerException · preguntá antes: if (v != null)
recompensa: xp 15, oro 15
```

#### Escena
Zed busca en el registro a un viajero que llegó «con un vitral». La búsqueda no lo encuentra y devuelve `null`. Al usarlo, el programa se corta con un **NullPointerException** y el troll vuelve, feliz.

#### Gheco sugiere
`null` significa «no hay objeto». Llamar un método sobre `null` corta el programa. Antes de usar una referencia que puede no estar, preguntá: `if (v != null) { … } else { … }`.

#### Desafío
Completá la condición para usar al viajero solo si se encontró.

#### Código inicial
```java
public class Registro {
    static Viajero buscar(String nombre) {
        if (nombre.equals("Zed")) {
            Viajero v = new Viajero();
            v.nombre = "Zed";
            return v;
        }
        return null;
    }

    public static void main(String[] args) {
        String[] pedidos = {"Zed", "el Vidriero"};
        for (String p : pedidos) {
            Viajero v = buscar(p);
            if (___) {
                System.out.println("Encontrado: " + v.nombre.toUpperCase());
            } else {
                System.out.println(p + ": no está en el registro");
            }
        }
    }
}

class Viajero {
    String nombre;
}
```

#### Salida esperada
```
Encontrado: ZED
el Vidriero: no está en el registro
```

#### Solución
```java
public class Registro {
    static Viajero buscar(String nombre) {
        if (nombre.equals("Zed")) {
            Viajero v = new Viajero();
            v.nombre = "Zed";
            return v;
        }
        return null;
    }

    public static void main(String[] args) {
        String[] pedidos = {"Zed", "el Vidriero"};
        for (String p : pedidos) {
            Viajero v = buscar(p);
            if (v != null) {
                System.out.println("Encontrado: " + v.nombre.toUpperCase());
            } else {
                System.out.println(p + ": no está en el registro");
            }
        }
    }
}

class Viajero {
    String nombre;
}
```

#### Al superarla
«el Vidriero: no está en el registro.» Pero alguien lo buscó antes que Zed: en el margen hay una marca a lápiz. Nadia la mira y no dice nada.

#### Imagen
- Un registro de la Academia abierto; un renglón vacío con una marca a lápiz en el margen.
- El troll escondiéndose al ver el `if`; Nadia mirando la marca, pensativa.

### Micro-misión R02-N04-P3 · Dos sellos iguales

```meta
lugar: El depósito de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: equals | == pregunta si es EL MISMO objeto · equals pregunta si son IGUALES · hay que escribirlo: public boolean equals(Object o)
recompensa: xp 15, oro 15
```

#### Escena
Hay dos sellos con el mismo código, «A-7». Son dos objetos distintos, pero valen lo mismo. Con `==` dan `false`, y con `equals`… también, porque nadie le explicó al molde cuándo dos sellos son iguales.

#### Gheco sugiere
`==` compara **identidad** (si es el mismo objeto). `equals` compara **igualdad**, pero hay que escribirlo: si el otro es un `Sello`, son iguales cuando tienen el mismo `codigo`. Los `String` se comparan con `equals`.

#### Desafío
Completá el `return` de `equals`: iguales si tienen el mismo código.

#### Código inicial
```java
public class Sellos {
    public static void main(String[] args) {
        Sello a = new Sello("A-7");
        Sello b = new Sello("A-7");
        Sello c = new Sello("B-2");
        System.out.println("a == b: " + (a == b));
        System.out.println("a.equals(b): " + a.equals(b));
        System.out.println("a.equals(c): " + a.equals(c));
    }
}

class Sello {
    String codigo;

    Sello(String codigo) {
        this.codigo = codigo;
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Sello)) {
            return false;
        }
        Sello otro = (Sello) o;
        return ___;
    }
}
```

#### Salida esperada
```
a == b: false
a.equals(b): true
a.equals(c): false
```

#### Solución
```java
public class Sellos {
    public static void main(String[] args) {
        Sello a = new Sello("A-7");
        Sello b = new Sello("A-7");
        Sello c = new Sello("B-2");
        System.out.println("a == b: " + (a == b));
        System.out.println("a.equals(b): " + a.equals(b));
        System.out.println("a.equals(c): " + a.equals(c));
    }
}

class Sello {
    String codigo;

    Sello(String codigo) {
        this.codigo = codigo;
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Sello)) {
            return false;
        }
        Sello otro = (Sello) o;
        return codigo.equals(otro.codigo);
    }
}
```

#### Al superarla
«a == b: false. a.equals(b): true.» —Son dos sellos, pero valen lo mismo —resume Zed—. Como en la Aduana con los textos. —Exacto —dice Nadia—. Lo aprendiste allá y no te diste cuenta.

#### Imagen
- Dos sellos de bronce idénticos con el código «A-7», uno al lado del otro, unidos por un signo igual de luz.
- Un tercer sello «B-2» apartado.

### Micro-misión R02-N04-P4 · La huella del sello

```meta
lugar: El depósito de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: hashCode | si dos objetos son equals, tienen que dar el mismo hashCode · return Objects.hash(codigo); · import java.util.Objects;
recompensa: xp 15, oro 15
```

#### Escena
—Si escribís `equals`, escribí también `hashCode` —dice la Maestra—. Es la **huella** del objeto: dos sellos iguales tienen que dejar la misma huella. Los archivos del Imperio buscan por huella, y si no coincide, no los encuentran.

#### Gheco sugiere
`hashCode()` devuelve un número que resume al objeto. La regla: si `a.equals(b)`, entonces `a.hashCode() == b.hashCode()`. Lo más simple: `return Objects.hash(codigo);` con los mismos campos que usa `equals`.

#### Desafío
Completá el `hashCode` con el mismo campo que usa `equals`.

#### Código inicial
```java
import java.util.Objects;

public class Huella {
    public static void main(String[] args) {
        Sello a = new Sello("A-7");
        Sello b = new Sello("A-7");
        System.out.println("Iguales: " + a.equals(b));
        System.out.println("Misma huella: " + (a.hashCode() == b.hashCode()));
    }
}

class Sello {
    String codigo;

    Sello(String codigo) {
        this.codigo = codigo;
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Sello)) {
            return false;
        }
        return codigo.equals(((Sello) o).codigo);
    }

    @Override
    public int hashCode() {
        return ___;
    }
}
```

#### Salida esperada
```
Iguales: true
Misma huella: true
```

#### Solución
```java
import java.util.Objects;

public class Huella {
    public static void main(String[] args) {
        Sello a = new Sello("A-7");
        Sello b = new Sello("A-7");
        System.out.println("Iguales: " + a.equals(b));
        System.out.println("Misma huella: " + (a.hashCode() == b.hashCode()));
    }
}

class Sello {
    String codigo;

    Sello(String codigo) {
        this.codigo = codigo;
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Sello)) {
            return false;
        }
        return codigo.equals(((Sello) o).codigo);
    }

    @Override
    public int hashCode() {
        return Objects.hash(codigo);
    }
}
```

#### Al superarla
Misma huella, iguales en todo. La Maestra guarda los sellos en su lugar.
En el ala oeste, cubierto de polvo, hay un molde viejísimo con una palabra grabada: **Personaje**. De él salieron todos los demás.

#### Imagen
- Dos sellos estampados en lacre que dejan exactamente la misma huella brillante.
- Al fondo, en un pasillo oscuro, un molde viejo y enorme con la palabra «Personaje» grabada.

### Misión R02-N04-M1 · Los mapas copiados

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Mapa` con un nombre y una cantidad de marcas, un método
`agregarMarca()` y un constructor de copia. En el `main`:

1. Creá un mapa, hacé un **alias** y agregá dos marcas por el alias. Mostrá el
   original.
2. Hacé una **copia** con el constructor de copia y agregá una marca a la copia.
   Mostrá los dos.
3. Mostrá con `==` cuáles son el mismo objeto.

#### Criterio de aprobación

- Se ve que el alias modifica el original y la copia no.
- Tiene constructor de copia.

#### Salida esperada

```
Original: mapa de Frontera con 2 marcas
Original: mapa de Frontera con 2 marcas
Copia: mapa de Frontera con 3 marcas
original == alias: true
original == copia: false
```

#### Solución de referencia

```java
// Mision 1 - Los mapas copiados: alias contra copia.
public class Cartografia {
    public static void main(String[] args) {
        Mapa original = new Mapa("Frontera");
        Mapa alias = original;
        alias.agregarMarca();
        alias.agregarMarca();
        System.out.println("Original: " + original);

        Mapa copia = new Mapa(original);
        copia.agregarMarca();
        System.out.println("Original: " + original);
        System.out.println("Copia: " + copia);

        System.out.println("original == alias: " + (original == alias));
        System.out.println("original == copia: " + (original == copia));
    }
}

class Mapa {
    private final String nombre;
    private int marcas;

    public Mapa(String nombre) {
        this.nombre = nombre;
    }

    public Mapa(Mapa otro) {
        this.nombre = otro.nombre;
        this.marcas = otro.marcas;
    }

    public void agregarMarca() {
        marcas++;
    }

    @Override
    public String toString() {
        return "mapa de " + nombre + " con " + marcas + " marcas";
    }
}
```

### Misión R02-N04-M2 · Los libros repetidos

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La biblioteca de la Academia quiere detectar libros repetidos. Escribí una clase
`Libro` con ISBN, título y año, donde **dos libros son iguales si tienen el mismo
ISBN** (sin importar el título). Redefiní `equals` y `hashCode` con `@Override`. En un
array de 5 libros (con dos ISBN repetidos), contá y mostrá los repetidos comparando
cada par con `equals`.

#### Criterio de aprobación

- `equals(Object)` con `@Override`, `instanceof` y comparación de ISBN con `equals`.
- `hashCode` coherente con `equals`.
- Detecta los dos repetidos.

#### Salida esperada

```
Repetido: "El arte de programar" (1968) y "El arte de programar (2a ed.)" (1973)
Repetido: "Estructuras de datos" (1985) y "Estructuras de datos" (1985)
Pares repetidos: 2
Mismo hashCode el 0 y el 2: true
```

#### Solución de referencia

```java
// Mision 2 - Los libros repetidos: equals y hashCode por ISBN.
import java.util.Objects;

public class Biblioteca {
    public static void main(String[] args) {
        Libro[] libros = {
            new Libro("978-1", "El arte de programar", 1968),
            new Libro("978-2", "Estructuras de datos", 1985),
            new Libro("978-1", "El arte de programar (2a ed.)", 1973),
            new Libro("978-3", "Java desde cero", 2020),
            new Libro("978-2", "Estructuras de datos", 1985),
        };
        int repetidos = 0;
        for (int i = 0; i < libros.length; i++) {
            for (int j = i + 1; j < libros.length; j++) {
                if (libros[i].equals(libros[j])) {
                    System.out.println("Repetido: " + libros[i] + " y " + libros[j]);
                    repetidos++;
                }
            }
        }
        System.out.println("Pares repetidos: " + repetidos);
        System.out.println("Mismo hashCode el 0 y el 2: " + (libros[0].hashCode() == libros[2].hashCode()));
    }
}

class Libro {
    private final String isbn;
    private final String titulo;
    private final int anio;

    public Libro(String isbn, String titulo, int anio) {
        this.isbn = isbn;
        this.titulo = titulo;
        this.anio = anio;
    }

    @Override
    public boolean equals(Object otro) {
        if (this == otro) {
            return true;
        }
        if (!(otro instanceof Libro)) {
            return false;
        }
        return isbn.equals(((Libro) otro).isbn);
    }

    @Override
    public int hashCode() {
        return Objects.hash(isbn);
    }

    @Override
    public String toString() {
        return "\"" + titulo + "\" (" + anio + ")";
    }
}
```

### Misión R02-N04-M3 · La guardia de la puerta

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Una puerta tiene tres turnos de guardia (un array de `Guardia` de 3 lugares) y
algunos turnos pueden estar **vacíos** (`null`). Escribí un método `static String
quienCuida(Guardia[] turnos, int turno)` que devuelve el nombre del guardia o "nadie"
si el turno está vacío o el número es inválido, **sin que nunca salte un
`NullPointerException`**. Escribí también `static int contarPresentes(Guardia[]
turnos)`. Probalo con los turnos 0 a 3 y con un array donde el turno 1 está vacío.

#### Criterio de aprobación

- Pregunta por `null` antes de usar cada referencia.
- Maneja el índice fuera de rango.

#### Salida esperada

```
Turno 0: Baldo
Turno 1: nadie
Turno 2: Nara
Turno 3: nadie
Presentes: 2
```

#### Solución de referencia

```java
// Mision 3 - La guardia de la puerta: trabajar con null sin romperse.
public class Guardias {
    public static void main(String[] args) {
        Guardia[] turnos = new Guardia[3];
        turnos[0] = new Guardia("Baldo");
        turnos[2] = new Guardia("Nara");
        for (int t = 0; t <= 3; t++) {
            System.out.println("Turno " + t + ": " + quienCuida(turnos, t));
        }
        System.out.println("Presentes: " + contarPresentes(turnos));
    }

    static String quienCuida(Guardia[] turnos, int turno) {
        if (turnos == null || turno < 0 || turno >= turnos.length || turnos[turno] == null) {
            return "nadie";
        }
        return turnos[turno].getNombre();
    }

    static int contarPresentes(Guardia[] turnos) {
        int presentes = 0;
        for (Guardia g : turnos) {
            if (g != null) {
                presentes++;
            }
        }
        return presentes;
    }
}

class Guardia {
    private final String nombre;

    public Guardia(String nombre) {
        this.nombre = nombre;
    }

    public String getNombre() {
        return nombre;
    }
}
```

### Encargo R02-N04-E1 · Los clientes del padrón

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un padrón de clientes identifica a cada uno por su DNI. Escribí la clase `Cliente`
(DNI, nombre, email) donde dos clientes son iguales si tienen el mismo DNI, **y el
email puede ser `null`**. Usá `Objects.equals` para comparar sin romperse y
`Objects.hash` en `hashCode`. Escribí un método que, dado un array de clientes y un
cliente buscado, devuelva la posición del primero igual (o -1). Probalo con un cliente
que está (cargado con otro nombre) y uno que no.

#### Criterio de aprobación

- `equals` y `hashCode` por DNI, con `@Override`.
- El email `null` no produce ningún error al mostrar o comparar.

#### Salida esperada

```
Buscado está en: 1
Nuevo está en: -1
Emails iguales (null y null): true
30111222 Marta Díaz <marta@correo.com>
28999000 Juan Pérez <sin email>
33444555 Ana Ruiz <ana@correo.com>
```

#### Solución de referencia

```java
// Encargo - Los clientes del padron: equals por DNI y Objects.equals con null.
import java.util.Objects;

public class Padron {
    public static void main(String[] args) {
        Cliente[] clientes = {
            new Cliente("30111222", "Marta Díaz", "marta@correo.com"),
            new Cliente("28999000", "Juan Pérez", null),
            new Cliente("33444555", "Ana Ruiz", "ana@correo.com"),
        };
        Cliente buscado = new Cliente("28999000", "J. Perez", null);
        Cliente nuevo = new Cliente("40000001", "Leo Paz", null);
        System.out.println("Buscado está en: " + buscar(clientes, buscado));
        System.out.println("Nuevo está en: " + buscar(clientes, nuevo));
        System.out.println("Emails iguales (null y null): " + Objects.equals(clientes[1].getEmail(), buscado.getEmail()));
        for (Cliente c : clientes) {
            System.out.println(c);
        }
    }

    static int buscar(Cliente[] clientes, Cliente buscado) {
        for (int i = 0; i < clientes.length; i++) {
            if (clientes[i].equals(buscado)) {
                return i;
            }
        }
        return -1;
    }
}

class Cliente {
    private final String dni;
    private final String nombre;
    private final String email;

    public Cliente(String dni, String nombre, String email) {
        this.dni = dni;
        this.nombre = nombre;
        this.email = email;
    }

    public String getEmail() {
        return email;
    }

    @Override
    public boolean equals(Object otro) {
        if (this == otro) {
            return true;
        }
        if (!(otro instanceof Cliente)) {
            return false;
        }
        return Objects.equals(dni, ((Cliente) otro).dni);
    }

    @Override
    public int hashCode() {
        return Objects.hash(dni);
    }

    @Override
    public String toString() {
        return dni + " " + nombre + " <" + (email == null ? "sin email" : email) + ">";
    }
}
```

### Prueba del sello

#### Después de `Heroe h2 = h1;`, ¿cuántos objetos hay?

Uno solo, con dos referencias (alias) que apuntan a él.

#### ¿Qué pasa si llamás un método sobre una referencia `null`?

El programa se corta con `NullPointerException`.

#### ¿Qué diferencia hay entre `a == b` y `a.equals(b)` con objetos?

`==` pregunta si son el mismo objeto; `equals`, si son iguales según lo que defina la clase.

#### ¿Por qué `equals` recibe un `Object` y no un `Libro`?

Porque redefine el `equals(Object)` que toda clase hereda de `Object`; con otro parámetro sería una sobrecarga y las colecciones no lo usarían.

#### Si redefinís `equals`, ¿qué otro método tenés que redefinir?

`hashCode`, para que dos objetos iguales tengan el mismo código.

### Soluciones (docente)

Sale de `18-Java/12-Referencias-Object` (unidad 2), que en el capítulo original era el viejo 09 con los tipos. Se presenta `@Override` con `equals` antes de la herencia, explicando que `Object` es la madre de todas las clases; el nodo siguiente lo retoma.

## R02-N05 · Herencia: extends y super

```meta
tipo: tema
padre: R02-N04
precio: 10
criatura: skeleton
temas: poo.herencia
```

### Crónica

En el ala oeste de la Academia hay un molde viejo y gastado con la palabra **Personaje**. De él salieron todos los demás: el molde de la Guerrera, el de la Arquera, el de la Maga. Cada uno agrega lo suyo, pero todos tienen nombre, vida y la costumbre de caerse cuando la vida llega a cero.

—No escribas dos veces lo que todos tienen —dice {mentor}—. Escribilo una vez en el molde padre y que los hijos lo **hereden**. Cada hijo agrega lo que lo hace especial, o cambia lo que hace distinto. Vos heredaste un oficio, Zed. Ya vas a ver que se puede sobrescribir.

### Objetivos

- Crear subclases con `extends` y reutilizar el código de la superclase.
- Llamar al constructor del padre con `super(...)` y a sus métodos con `super.metodo()`.
- Sobrescribir métodos con `@Override`.
- Conocer la clase `Object`, `protected` en la herencia y los métodos y clases `final`.

### Antes de empezar

- Referencias, null y equals.

### Explicación

#### `extends`: una clase que es otra, más algo
```java
class Personaje {
    protected String nombre;
    protected int vida;

    public Personaje(String nombre, int vida) {
        this.nombre = nombre;
        this.vida = vida;
    }

    public void recibirDanio(int danio) {
        vida = Math.max(0, vida - danio);
    }

    public String describir() {
        return nombre + " (vida " + vida + ")";
    }
}

class Guerrero extends Personaje {         // un Guerrero ES un Personaje
    private int fuerza;

    public Guerrero(String nombre, int vida, int fuerza) {
        super(nombre, vida);                  // primero se construye la parte de Personaje
        this.fuerza = fuerza;
    }

    public int atacar() {
        return fuerza;
    }
}
```
`Guerrero` **hereda** los atributos y métodos de `Personaje`: un guerrero tiene
`nombre`, `vida`, `recibirDanio` y `describir` sin escribirlos. `Personaje` es la
**superclase** (o clase padre) y `Guerrero`, la **subclase** (o clase hija).

La herencia expresa la relación **"es un"**: un guerrero *es un* personaje. Si la
frase no tiene sentido ("una espada es un guerrero"), no corresponde herencia.

#### `super(...)`: el constructor del padre
El constructor de la subclase tiene que construir primero la parte del padre, con
`super(...)` como **primera línea**. Si no lo escribís, Java llama a `super()` sin
parámetros; si el padre no tiene ese constructor, no compila.

#### Sobrescribir: `@Override`
Una subclase puede **redefinir** un método heredado para comportarse distinto:
```java
class Arquera extends Personaje {
    private int flechas;
    …
    @Override
    public String describir() {
        return super.describir() + " con " + flechas + " flechas";   // reutiliza la versión del padre
    }
}
```
- La firma tiene que ser **la misma** (nombre y parámetros).
- `@Override` le pide al compilador que verifique que de verdad estás sobrescribiendo
  algo: si escribís mal el nombre, te avisa.
- `super.describir()` llama a la versión del padre.

No confundas: **sobrecargar** es el mismo nombre con otros parámetros (en la misma
clase); **sobrescribir** es la misma firma en una subclase.

#### `protected` en la herencia
Los atributos `private` del padre **existen** en el hijo, pero el hijo no los puede
tocar directo (usa los métodos públicos del padre). Si el padre los declara
`protected`, el hijo los ve. Recordá que `protected` también los abre a todo el
paquete: muchas veces es mejor dejar los atributos `private` y darle al hijo métodos
`protected` para lo que necesite.

#### `Object`: la madre de todas las clases
Toda clase que no dice `extends` hereda de `Object`. De ahí vienen `toString`,
`equals` y `hashCode`, y por eso los sobrescribimos con `@Override`.

#### `final` en la herencia
- Un **método `final`** no se puede sobrescribir: `public final int getVida()`.
- Una **clase `final`** no se puede heredar: `final class Moneda` (como `String`).

Se usa cuando cambiar ese comportamiento rompería las reglas de la clase.

#### Herencia simple
Una clase hereda de **una sola** superclase (`extends` una sola). Para "ser" varias
cosas a la vez están las interfaces (se ven en dos nodos).

> **Si venís de C++.** No hay herencia múltiple de clases ni `virtual`: en Java todos
> los métodos se pueden sobrescribir salvo los `final`, `static` y `private`.
>
> **Si venís de Python.** `super(nombre, vida)` en el constructor equivale a
> `super().__init__(nombre, vida)`, y `super.metodo()` a `super().metodo()`.

### Código de ejemplo

```java
/*
 * Herencia: los moldes que salen del molde Personaje.
 */
public class MoldesHijos {
    public static void main(String[] args) {
        Guerrero baldo = new Guerrero("Baldo", 45, 12);
        Arquera lia = new Arquera("Lía", 30, 6);
        Personaje aldeano = new Personaje("Olmo", 20);

        System.out.println(baldo.describir());
        System.out.println(lia.describir());
        System.out.println(aldeano.describir());

        // Métodos heredados y métodos propios
        lia.recibirDanio(baldo.atacar());
        System.out.println("Baldo golpea a Lía: " + lia.describir());
        System.out.println("Lía dispara: " + lia.disparar() + " de daño");
        System.out.println("Lía dispara: " + lia.disparar() + " de daño");
        System.out.println(lia.describir());

        // toString viene de Object; Guerrero lo sobrescribe
        System.out.println("toString de Baldo: " + baldo);
        System.out.println("¿Baldo es un Personaje? " + (baldo instanceof Personaje));
        System.out.println("Vida máxima (método final): " + baldo.getVidaMaxima());
    }
}

class Personaje {
    protected String nombre;
    protected int vida;
    private final int vidaMaxima;

    public Personaje(String nombre, int vida) {
        this.nombre = nombre;
        this.vida = vida;
        this.vidaMaxima = vida;
    }

    public void recibirDanio(int danio) {
        vida = Math.max(0, vida - danio);
    }

    public boolean estaVivo() {
        return vida > 0;
    }

    public final int getVidaMaxima() {       // ninguna subclase puede cambiarlo
        return vidaMaxima;
    }

    public String describir() {
        return nombre + " (vida " + vida + "/" + vidaMaxima + ")";
    }
}

class Guerrero extends Personaje {
    private final int fuerza;

    public Guerrero(String nombre, int vida, int fuerza) {
        super(nombre, vida);
        this.fuerza = fuerza;
    }

    public int atacar() {
        return fuerza;
    }

    @Override
    public String describir() {
        return "Guerrero " + super.describir() + ", fuerza " + fuerza;
    }

    @Override
    public String toString() {
        return "Guerrero[" + nombre + "]";
    }
}

class Arquera extends Personaje {
    private int flechas;

    public Arquera(String nombre, int vida, int flechas) {
        super(nombre, vida);
        this.flechas = flechas;
    }

    public int disparar() {
        if (flechas == 0) {
            return 0;
        }
        flechas--;
        return 8;
    }

    @Override
    public String describir() {
        return "Arquera " + super.describir() + ", " + flechas + " flechas";
    }
}
```

### Salida esperada

```
Guerrero Baldo (vida 45/45), fuerza 12
Arquera Lía (vida 30/30), 6 flechas
Olmo (vida 20/20)
Baldo golpea a Lía: Arquera Lía (vida 18/30), 6 flechas
Lía dispara: 8 de daño
Lía dispara: 8 de daño
Arquera Lía (vida 18/30), 4 flechas
toString de Baldo: Guerrero[Baldo]
¿Baldo es un Personaje? true
Vida máxima (método final): 45
```

### ¿Para qué sirve?

La herencia permite escribir una sola vez lo común y especializar lo distinto: en un sistema de una empresa, `Empleado` con `Gerente` y `Vendedor`; en un banco, `Cuenta` con `CajaDeAhorro` y `CuentaCorriente`; en Swing, todas las ventanas y botones heredan de `JComponent`. Usada con criterio ("es un"), ahorra código repetido; usada de más, ata las clases entre sí (en el nodo de composición vas a ver la alternativa).

### Errores habituales

**Esqueleto: el padre no tiene constructor sin parámetros.**
```
MoldesHijos.java:40: error: constructor Personaje in class Personaje cannot be applied to given types;
    public Guerrero(String nombre, int vida, int fuerza) {
                                                         ^
  required: String,int
  found:    no arguments
```
Falta `super(nombre, vida);` como primera línea del constructor de la subclase.

**Ogro: creer que sobrescribís y en realidad sobrecargás.** `public String
describir(int detalle)` es un método nuevo. Con `@Override` el compilador avisa:
`method does not override or implement a method from a supertype`.

**Esqueleto: usar un atributo `private` del padre.** `vidaMaxima has private access
in Personaje`: usá un getter o declaralo `protected`.

**Slime: sobrescribir un método `final`.** `describir() in Guerrero cannot override
describir() in Personaje; overridden method is final`.

**Ogro: herencia sin "es un".** `class Espada extends Guerrero` para reutilizar un
método: está mal. Si no *es un*, se usa composición.

### Micro-misión R02-N05-P1 · El molde Personaje

```meta
lugar: El ala oeste de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: extends | class Guerrero extends Personaje · el hijo HEREDA los atributos y métodos del padre · agrega lo suyo
recompensa: xp 10, oro 10
```

#### Escena
En el ala oeste, el molde **Personaje** tiene nombre, vida y un método para describirse. De él salen los demás. —No escribas dos veces lo que todos tienen —dice la Maestra—. El Guerrero **es** un Personaje: que lo herede.

#### Gheco sugiere
`class Guerrero extends Personaje` hace que el Guerrero tenga todo lo del Personaje (`nombre`, `vida`, `describir()`) sin escribirlo de nuevo, y le suma lo suyo (`fuerza`).

#### Desafío
Completá la palabra que hace que el Guerrero herede del Personaje.

#### Código inicial
```java
public class AlaOeste {
    public static void main(String[] args) {
        Guerrero g = new Guerrero();
        g.nombre = "Lía";
        g.vida = 120;
        g.fuerza = 9;
        System.out.println(g.describir());
        System.out.println("Fuerza: " + g.fuerza);
    }
}

class Personaje {
    String nombre;
    int vida;

    String describir() {
        return nombre + " (" + vida + " de vida)";
    }
}

class Guerrero ___ Personaje {
    int fuerza;
}
```

#### Salida esperada
```
Lía (120 de vida)
Fuerza: 9
```

#### Solución
```java
public class AlaOeste {
    public static void main(String[] args) {
        Guerrero g = new Guerrero();
        g.nombre = "Lía";
        g.vida = 120;
        g.fuerza = 9;
        System.out.println(g.describir());
        System.out.println("Fuerza: " + g.fuerza);
    }
}

class Personaje {
    String nombre;
    int vida;

    String describir() {
        return nombre + " (" + vida + " de vida)";
    }
}

class Guerrero extends Personaje {
    int fuerza;
}
```

#### Al superarla
Lía sale del molde Guerrero con nombre, vida y fuerza, y nadie escribió `describir` dos veces. —Es como heredar el oficio del padre —dice Zed—. Yo heredé el de ladrón. —Y lo estás sobrescribiendo —responde Nadia.

#### Imagen
- El molde viejo «Personaje» en el centro y, saliendo de él con ramas de bronce, los moldes Guerrero, Arquero y Maga.
- Lía, una guerrera joven, recién salida del molde Guerrero.

### Micro-misión R02-N05-P2 · Primero el padre

```meta
lugar: El ala oeste de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: super(...) | el constructor del hijo llama al del padre con super(nombre, vida); · en la primera línea · el padre arma su parte
recompensa: xp 15, oro 15
```

#### Escena
El molde Personaje ahora tiene constructor: pide nombre y vida. El molde Guerrero ya no compila. —El hijo tiene que dejar que el padre arme **su parte** primero —dice la Maestra.

#### Gheco sugiere
Si el padre tiene un constructor con parámetros, el hijo lo llama con `super(…)` en la **primera línea** del suyo: `super(nombre, 120);`. Después, el hijo arma lo propio: `this.fuerza = fuerza;`.

#### Desafío
Completá la llamada al constructor del padre: los guerreros arrancan con 120 de vida.

#### Código inicial
```java
public class PrimeroElPadre {
    public static void main(String[] args) {
        Guerrero g = new Guerrero("Lía", 9);
        System.out.println(g.describir() + ", fuerza " + g.fuerza);
    }
}

class Personaje {
    String nombre;
    int vida;

    Personaje(String nombre, int vida) {
        this.nombre = nombre;
        this.vida = vida;
    }

    String describir() {
        return nombre + " (" + vida + " de vida)";
    }
}

class Guerrero extends Personaje {
    int fuerza;

    Guerrero(String nombre, int fuerza) {
        ___;
        this.fuerza = fuerza;
    }
}
```

#### Salida esperada
```
Lía (120 de vida), fuerza 9
```

#### Solución
```java
public class PrimeroElPadre {
    public static void main(String[] args) {
        Guerrero g = new Guerrero("Lía", 9);
        System.out.println(g.describir() + ", fuerza " + g.fuerza);
    }
}

class Personaje {
    String nombre;
    int vida;

    Personaje(String nombre, int vida) {
        this.nombre = nombre;
        this.vida = vida;
    }

    String describir() {
        return nombre + " (" + vida + " de vida)";
    }
}

class Guerrero extends Personaje {
    int fuerza;

    Guerrero(String nombre, int fuerza) {
        super(nombre, 120);
        this.fuerza = fuerza;
    }
}
```

#### Al superarla
El molde Guerrero vuelve a cerrar. Primero el padre pone nombre y vida, después el hijo pone la fuerza. —Orden —dice Gheco—. Como con el Centinela.

#### Imagen
- Dos moldes encastrados: el grande (Personaje) se cierra primero y el chico (Guerrero) encaja encima.
- La Maestra de Moldes ajustando una tuerca; Zed mirando con atención.

### Micro-misión R02-N05-P3 · El arquero sin nombre

```meta
lugar: El ala oeste de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
criatura: esqueleto
carta: @Override | el hijo REEMPLAZA un método del padre con el mismo nombre y parámetros · @Override hace que el compilador lo controle
recompensa: xp 15, oro 15
```

#### Escena
El Arquero quiere describirse a su manera, pero quien escribió su método se equivocó en una letra. Gracias a `@Override`, la Aduana del compilador lo frena: ese método no reemplaza a nada. Un **esqueleto** sale del molde, sin nombre que lo sostenga.

#### Gheco sugiere
Para **sobrescribir** un método, el hijo lo escribe con el **mismo nombre y parámetros** que el padre. `@Override` le pide al compilador que lo controle: si el nombre está mal escrito, avisa.

#### Desafío
Ejecutalo, leé el error y corregí el nombre del método del Arquero.

#### Código inicial
```java
public class Arqueros {
    public static void main(String[] args) {
        Personaje p = new Personaje("Teo");
        Arquero a = new Arquero("Mira");
        System.out.println(p.describir());
        System.out.println(a.describir());
    }
}

class Personaje {
    String nombre;

    Personaje(String nombre) {
        this.nombre = nombre;
    }

    String describir() {
        return nombre + ", un personaje";
    }
}

class Arquero extends Personaje {
    Arquero(String nombre) {
        super(nombre);
    }

    @Override
    String descrbir() {
        return nombre + ", arquera que nunca falla";
    }
}
```

#### Salida esperada
```
Teo, un personaje
Mira, arquera que nunca falla
```

#### Solución
```java
public class Arqueros {
    public static void main(String[] args) {
        Personaje p = new Personaje("Teo");
        Arquero a = new Arquero("Mira");
        System.out.println(p.describir());
        System.out.println(a.describir());
    }
}

class Personaje {
    String nombre;

    Personaje(String nombre) {
        this.nombre = nombre;
    }

    String describir() {
        return nombre + ", un personaje";
    }
}

class Arquero extends Personaje {
    Arquero(String nombre) {
        super(nombre);
    }

    @Override
    String describir() {
        return nombre + ", arquera que nunca falla";
    }
}
```

#### Al superarla
Mira se presenta como arquera, no como «un personaje». El esqueleto encuentra su nombre en la etiqueta corregida y se desarma tranquilo.

#### Imagen
- Una etiqueta de bronce con «descrbir» tachado y «describir» escrito encima.
- Mira, una arquera de capa verde, con el arco tenso; un esqueleto desarmándose a sus pies.

### Micro-misión R02-N05-P4 · Lo del padre, y algo más

```meta
lugar: El ala oeste de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: super.metodo() | el hijo usa lo que hacía el padre y le agrega lo suyo · return super.describir() + " …";
recompensa: xp 15, oro 15
```

#### Escena
La Maga quiere describirse como cualquier personaje (nombre y vida), **más** su hechizo. —No copies lo del padre —dice la Maestra—. Pedíselo.

#### Gheco sugiere
Adentro de un método sobrescrito, `super.describir()` llama a la versión del **padre**. Así el hijo reutiliza lo que ya existe y le agrega lo suyo.

#### Desafío
Completá el `return`: lo que describe el padre, más " y lanza rayos".

#### Código inicial
```java
public class Magas {
    public static void main(String[] args) {
        Maga m = new Maga("Sol", 80);
        System.out.println(m.describir());
    }
}

class Personaje {
    String nombre;
    int vida;

    Personaje(String nombre, int vida) {
        this.nombre = nombre;
        this.vida = vida;
    }

    String describir() {
        return nombre + " (" + vida + " de vida)";
    }
}

class Maga extends Personaje {
    Maga(String nombre, int vida) {
        super(nombre, vida);
    }

    @Override
    String describir() {
        return ___;
    }
}
```

#### Salida esperada
```
Sol (80 de vida) y lanza rayos
```

#### Solución
```java
public class Magas {
    public static void main(String[] args) {
        Maga m = new Maga("Sol", 80);
        System.out.println(m.describir());
    }
}

class Personaje {
    String nombre;
    int vida;

    Personaje(String nombre, int vida) {
        this.nombre = nombre;
        this.vida = vida;
    }

    String describir() {
        return nombre + " (" + vida + " de vida)";
    }
}

class Maga extends Personaje {
    Maga(String nombre, int vida) {
        super(nombre, vida);
    }

    @Override
    String describir() {
        return super.describir() + " y lanza rayos";
    }
}
```

#### Al superarla
«Sol (80 de vida) y lanza rayos.» Guerrera, arquera y maga: tres moldes, un solo padre.
Desde el patio llega un grito: la Maestra reúne a todos los alumnos para un ejercicio con una sola orden.

#### Imagen
- Sol, una maga joven de túnica azul, con un rayo entre las manos.
- Detrás, Lía y Mira; al fondo, el patio de armas de la Academia lleno de alumnos.

### Misión R02-N05-M1 · Los empleados del gremio

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Empleado` (nombre y sueldo base) con un método `double
sueldo()` que devuelve el base y `toString`. Dos subclases: `Vendedor` (agrega las
ventas del mes y cobra el base más el 5 % de las ventas) y `Gerente` (agrega un bono
fijo que se suma al base). Sobrescribí `sueldo()` y `toString()` usando `super`.
Mostrá el sueldo de un empleado de cada tipo con 2 decimales.

#### Criterio de aprobación

- Las subclases usan `super(...)` en el constructor.
- `sueldo()` se sobrescribe con `@Override` y reutiliza `super.sueldo()`.

#### Salida esperada

```
Olmo   cobra 400000.00
Nara   cobra 425000.00 (vendedor, ventas 2500000.00)
Tesla  cobra 950000.00 (gerente)
```

#### Solución de referencia

```java
// Mision 1 - Los empleados del gremio: extends, super y @Override.
import java.util.Locale;

public class Gremio {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Empleado olmo = new Empleado("Olmo", 400_000);
        Vendedor nara = new Vendedor("Nara", 300_000, 2_500_000);
        Gerente tesla = new Gerente("Tesla", 700_000, 250_000);
        System.out.println(olmo);
        System.out.println(nara);
        System.out.println(tesla);
    }
}

class Empleado {
    private final String nombre;
    private final double sueldoBase;

    public Empleado(String nombre, double sueldoBase) {
        this.nombre = nombre;
        this.sueldoBase = sueldoBase;
    }

    public String getNombre() {
        return nombre;
    }

    public double sueldo() {
        return sueldoBase;
    }

    @Override
    public String toString() {
        return String.format("%-6s cobra %.2f", nombre, sueldo());
    }
}

class Vendedor extends Empleado {
    private final double ventas;

    public Vendedor(String nombre, double sueldoBase, double ventas) {
        super(nombre, sueldoBase);
        this.ventas = ventas;
    }

    @Override
    public double sueldo() {
        return super.sueldo() + ventas * 0.05;
    }

    @Override
    public String toString() {
        return super.toString() + " (vendedor, ventas " + String.format("%.2f", ventas) + ")";
    }
}

class Gerente extends Empleado {
    private final double bono;

    public Gerente(String nombre, double sueldoBase, double bono) {
        super(nombre, sueldoBase);
        this.bono = bono;
    }

    @Override
    public double sueldo() {
        return super.sueldo() + bono;
    }

    @Override
    public String toString() {
        return super.toString() + " (gerente)";
    }
}
```

### Misión R02-N05-M2 · Las cuentas del banco imperial

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Cuenta` con saldo `private`, `depositar`, `getSaldo` y un método
`boolean extraer(double monto)` que no deja el saldo negativo. Subclases:
`CajaAhorro`, que solo permite 3 extracciones (después devuelve `false`), y
`CuentaCorriente`, que permite un descubierto (el saldo puede quedar negativo hasta
un límite). Sobrescribí `extraer` en las dos. Como el saldo es `private`, la
subclase que necesita cambiarlo usa un método `protected void setSaldo(double)` del
padre. Probá las dos cuentas.

#### Criterio de aprobación

- El saldo es `private` y las subclases lo cambian por un método `protected`.
- Cada subclase sobrescribe `extraer` con su regla.

#### Salida esperada

```
Caja: extracción 1 de 100 -> true, saldo 900.0
Caja: extracción 2 de 100 -> true, saldo 800.0
Caja: extracción 3 de 100 -> true, saldo 700.0
Caja: extracción 4 de 100 -> false, saldo 700.0
Corriente: extraer 600 -> true, saldo -400.0
Corriente: extraer 200 -> false, saldo -400.0
```

#### Solución de referencia

```java
// Mision 2 - Las cuentas del banco imperial: sobrescribir con reglas distintas.
import java.util.Locale;

public class BancoImperial {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        CajaAhorro caja = new CajaAhorro();
        caja.depositar(1000);
        for (int i = 1; i <= 4; i++) {
            System.out.println("Caja: extracción " + i + " de 100 -> " + caja.extraer(100) + ", saldo " + caja.getSaldo());
        }
        CuentaCorriente cc = new CuentaCorriente(500);
        cc.depositar(200);
        System.out.println("Corriente: extraer 600 -> " + cc.extraer(600) + ", saldo " + cc.getSaldo());
        System.out.println("Corriente: extraer 200 -> " + cc.extraer(200) + ", saldo " + cc.getSaldo());
    }
}

class Cuenta {
    private double saldo;

    public void depositar(double monto) {
        if (monto > 0) {
            saldo += monto;
        }
    }

    public double getSaldo() {
        return saldo;
    }

    protected void setSaldo(double saldo) {
        this.saldo = saldo;
    }

    public boolean extraer(double monto) {
        if (monto <= 0 || monto > saldo) {
            return false;
        }
        saldo -= monto;
        return true;
    }
}

class CajaAhorro extends Cuenta {
    private int extracciones = 0;

    @Override
    public boolean extraer(double monto) {
        if (extracciones == 3) {
            return false;
        }
        boolean ok = super.extraer(monto);
        if (ok) {
            extracciones++;
        }
        return ok;
    }
}

class CuentaCorriente extends Cuenta {
    private final double descubierto;

    public CuentaCorriente(double descubierto) {
        this.descubierto = descubierto;
    }

    @Override
    public boolean extraer(double monto) {
        if (monto <= 0 || getSaldo() - monto < -descubierto) {
            return false;
        }
        setSaldo(getSaldo() - monto);
        return true;
    }
}
```

### Misión R02-N05-M3 · Las figuras del cartógrafo

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Figura` con un nombre, un método `double area()` que devuelve 0 y
un método **`final`** `String ficha()` que arma `"nombre: área X.XX"` usando `area()`.
Subclases `Rectangulo` (base y altura), `Circulo` (radio) y `Cuadrado`, que **hereda
de `Rectangulo`** (un cuadrado es un rectángulo con base igual a la altura) y solo
tiene un constructor. Sobrescribí `area()` donde haga falta y mostrá la ficha de una
figura de cada tipo.

#### Criterio de aprobación

- `ficha()` es `final` y usa `area()`.
- `Cuadrado` hereda de `Rectangulo` y no vuelve a escribir `area()`.

#### Salida esperada

```
rectángulo: área 10.00
círculo: área 28.27
cuadrado: área 25.00
¿Un cuadrado es un rectángulo? true
```

#### Solución de referencia

```java
// Mision 3 - Las figuras del cartografo: herencia en varios niveles y un metodo final.
import java.util.Locale;

public class Cartografo {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        System.out.println(new Rectangulo(4, 2.5).ficha());
        System.out.println(new Circulo(3).ficha());
        System.out.println(new Cuadrado(5).ficha());
        Cuadrado c = new Cuadrado(2);
        System.out.println("¿Un cuadrado es un rectángulo? " + (c instanceof Rectangulo));
    }
}

class Figura {
    private final String nombre;

    public Figura(String nombre) {
        this.nombre = nombre;
    }

    public double area() {
        return 0;
    }

    public final String ficha() {
        return String.format("%s: área %.2f", nombre, area());
    }
}

class Rectangulo extends Figura {
    private final double base;
    private final double altura;

    public Rectangulo(double base, double altura) {
        this("rectángulo", base, altura);
    }

    protected Rectangulo(String nombre, double base, double altura) {
        super(nombre);
        this.base = base;
        this.altura = altura;
    }

    @Override
    public double area() {
        return base * altura;
    }
}

class Circulo extends Figura {
    private final double radio;

    public Circulo(double radio) {
        super("círculo");
        this.radio = radio;
    }

    @Override
    public double area() {
        return Math.PI * radio * radio;
    }
}

class Cuadrado extends Rectangulo {
    public Cuadrado(double lado) {
        super("cuadrado", lado, lado);
    }
}
```

### Encargo R02-N05-E1 · Los vehículos de la flota

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una empresa de logística tiene `Vehiculo` (patente, kilómetros) con un método
`double costoPorKm()` y `double costoViaje(double km)`, que multiplica. Subclases:
`Moto` (costo 45 por km), `Camioneta` (120 por km) y `Camion` (250 por km más 30 por
cada tonelada de carga, que es un atributo). Cada viaje suma los kilómetros al
vehículo. Mostrá el costo de un viaje de 350 km para cada uno, con 2 decimales, y los
kilómetros acumulados.

#### Criterio de aprobación

- `costoPorKm` se sobrescribe en cada subclase; `costoViaje` está una sola vez en el padre.
- Los kilómetros son `private` en el padre.

#### Salida esperada

```
A123BC: viaje de 350 km = $15750.00
AE456FG: viaje de 350 km = $42000.00
AD789HJ: viaje de 350 km = $213500.00
A123BC lleva 350.0 km
AE456FG lleva 350.0 km
AD789HJ lleva 470.0 km
```

#### Solución de referencia

```java
// Encargo - Los vehiculos de la flota: un metodo del padre que usa uno sobrescrito.
import java.util.Locale;

public class Flota {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Vehiculo[] flota = {new Moto("A123BC"), new Camioneta("AE456FG"), new Camion("AD789HJ", 12)};
        for (Vehiculo v : flota) {
            System.out.printf("%s: viaje de 350 km = $%.2f%n", v.getPatente(), v.costoViaje(350));
        }
        flota[2].costoViaje(120);
        for (Vehiculo v : flota) {
            System.out.println(v.getPatente() + " lleva " + v.getKilometros() + " km");
        }
    }
}

class Vehiculo {
    private final String patente;
    private double kilometros;

    public Vehiculo(String patente) {
        this.patente = patente;
    }

    public String getPatente() {
        return patente;
    }

    public double getKilometros() {
        return kilometros;
    }

    public double costoPorKm() {
        return 0;
    }

    public double costoViaje(double km) {
        kilometros += km;
        return km * costoPorKm();
    }
}

class Moto extends Vehiculo {
    public Moto(String patente) {
        super(patente);
    }

    @Override
    public double costoPorKm() {
        return 45;
    }
}

class Camioneta extends Vehiculo {
    public Camioneta(String patente) {
        super(patente);
    }

    @Override
    public double costoPorKm() {
        return 120;
    }
}

class Camion extends Vehiculo {
    private final double toneladas;

    public Camion(String patente, double toneladas) {
        super(patente);
        this.toneladas = toneladas;
    }

    @Override
    public double costoPorKm() {
        return 250 + 30 * toneladas;
    }
}
```

### Prueba del sello

#### ¿Qué relación expresa la herencia?

"Es un": la subclase es un caso particular de la superclase.

#### ¿Para qué sirve `super(...)` y dónde va?

Para llamar al constructor de la superclase; tiene que ser la primera línea del constructor.

#### ¿Qué diferencia hay entre sobrecargar y sobrescribir?

Sobrecargar es mismo nombre con otros parámetros; sobrescribir es redefinir en la subclase un método con la misma firma.

#### ¿Qué ventaja da escribir `@Override`?

El compilador verifica que de verdad estés sobrescribiendo un método del padre.

#### ¿De qué clase hereda una clase que no dice `extends`?

De `Object`.

### Soluciones (docente)

Sale de `18-Java/13-Herencia-Final` (unidades 1 y 4). Corrige el `protected` del original (el ejemplo lo usa con criterio y se muestra la alternativa de `private` + método `protected`) y suma los métodos y clases `final` que pide el programa.

## R02-N06 · Polimorfismo y clases abstractas

```meta
tipo: tema
padre: R02-N05
precio: 10
criatura: goblin
temas: poo.polimorfismo, poo.abstractas
```

### Crónica

En el patio de armas, la Maestra de Moldes grita una sola orden: *¡Ataquen!* Y cada alumno ataca a su manera: Lía con la espada, Mira con el arco, Sol con un rayo. La Maestra no necesita saber qué es cada uno; sabe que todos saben atacar.

—Eso es el **polimorfismo** —dice {mentor}—: un mismo mensaje, muchas formas de responderlo. Y fijate en el molde de Personaje: nadie es «un personaje» a secas. Es un molde **abstracto**: existe para que los demás lo completen.

### Objetivos

- Usar una referencia de la superclase para manejar objetos de las subclases.
- Entender la ligadura dinámica: qué método se ejecuta de verdad.
- Declarar clases y métodos abstractos.
- Usar `instanceof` y el casting de referencias, y saber por qué conviene evitarlos.
- Distinguir los tipos de polimorfismo.

### Antes de empezar

- Herencia: extends y super.

### Explicación

#### Una referencia del padre, un objeto del hijo
Una variable de tipo `Personaje` puede apuntar a **cualquier subclase**:
```java
Personaje p = new Guerrero("Baldo", 45, 12);    // un guerrero ES un personaje
Personaje[] grupo = {new Guerrero(...), new Arquera(...), new Maga(...)};
```
Con esa referencia solo se pueden usar los métodos que **declara** `Personaje` (el
compilador mira el tipo de la variable). Pero al ejecutarse, corre la versión **del
objeto real** (la JVM mira el objeto):
```java
for (Personaje p : grupo) {
    System.out.println(p.atacar());    // cada uno ataca a su manera
}
```
Eso se llama **ligadura dinámica**: qué método se ejecuta se decide al correr, según
el objeto. Es lo que permite agregar una clase nueva (`Clériga`) sin tocar el bucle.

#### Clases y métodos abstractos
Si "un personaje genérico" no tiene sentido y cada subclase **tiene que** saber
atacar, se declara así:
```java
abstract class Personaje {
    …
    public abstract int atacar();    // sin cuerpo: cada subclase lo implementa
}
```
- Una clase `abstract` **no se puede instanciar**: `new Personaje(...)` no compila.
- Un método `abstract` no tiene cuerpo (termina en `;`) y obliga a las subclases
  concretas a implementarlo. Si una subclase no lo hace, también tiene que ser
  abstracta.
- Una clase abstracta **sí** puede tener atributos, constructores y métodos con
  código: guarda todo lo común.

#### `instanceof` y el casting de referencias
A veces necesitás algo que solo tiene una subclase. Primero preguntás y después
convertís la referencia:
```java
if (p instanceof Arquera) {
    Arquera a = (Arquera) p;          // casting: ahora la veo como Arquera
    a.recogerFlechas();
}
```
Desde Java 16, el *pattern matching* hace las dos cosas juntas:
```java
if (p instanceof Arquera a) {
    a.recogerFlechas();
}
```
Un casting equivocado corta el programa con `ClassCastException`.

Si tu código se llena de `instanceof`, suele ser señal de que falta un método en la
superclase que cada subclase implemente a su manera. El polimorfismo existe para
**no tener que preguntar** qué es cada objeto.

#### Tipos de polimorfismo
| Tipo | Qué es | En Java |
|---|---|---|
| **De inclusión** (o de subtipos) | un objeto de la subclase se usa donde se espera la superclase, y responde con su propia versión | herencia + sobrescritura (este nodo) |
| **Ad hoc** (sobrecarga) | el mismo nombre con distintos parámetros | métodos sobrecargados (`mayor(int, int)` y `mayor(double, double)`) |
| **Paramétrico** | código que funciona con cualquier tipo | genéricos: `ArrayList<String>`, `ArrayList<Heroe>` (rama 3) |

`instanceof` **no** es un tipo de polimorfismo: es justamente preguntar el tipo para
salirse de él.

> **Si venís de C++.** Todos los métodos son "virtuales" por defecto, y una clase
> abstracta es una con al menos un método "virtual puro".

### Código de ejemplo

```java
/*
 * Polimorfismo y clases abstractas: la orden de atacar.
 */
public class OrdenDeAtacar {
    public static void main(String[] args) {
        Personaje[] grupo = {
            new Guerrera("Nara", 45, 12),
            new Arquera("Lía", 30, 3),
            new Mago("Olmo", 25, 20),
        };

        // El mismo mensaje, tres respuestas distintas (ligadura dinámica)
        int danioTotal = 0;
        for (int ronda = 1; ronda <= 2; ronda++) {
            System.out.println("Ronda " + ronda);
            for (Personaje p : grupo) {
                int danio = p.atacar();
                danioTotal += danio;
                System.out.println("  " + p.getNombre() + " " + p.grito() + " -> " + danio);
            }
        }
        System.out.println("Daño total: " + danioTotal);

        // instanceof con pattern matching: solo las arqueras recogen flechas
        for (Personaje p : grupo) {
            if (p instanceof Arquera a) {
                a.recogerFlechas(2);
                System.out.println(a.getNombre() + " recoge flechas: " + a);
            }
        }

        // Un casting equivocado
        try {
            Mago m = (Mago) grupo[0];
            System.out.println(m);
        } catch (ClassCastException e) {
            System.out.println("Casting imposible: una guerrera no es un mago");
        }

        // new Personaje("Nadie", 1);   // no compila: Personaje is abstract; cannot be instantiated
    }
}

abstract class Personaje {
    private final String nombre;
    protected int vida;

    protected Personaje(String nombre, int vida) {
        this.nombre = nombre;
        this.vida = vida;
    }

    public String getNombre() {
        return nombre;
    }

    public abstract int atacar();          // cada subclase lo implementa

    public String grito() {                // uno común que se puede sobrescribir
        return "ataca";
    }
}

class Guerrera extends Personaje {
    private final int fuerza;

    public Guerrera(String nombre, int vida, int fuerza) {
        super(nombre, vida);
        this.fuerza = fuerza;
    }

    @Override
    public int atacar() {
        return fuerza;
    }

    @Override
    public String grito() {
        return "blande la espada";
    }
}

class Arquera extends Personaje {
    private int flechas;

    public Arquera(String nombre, int vida, int flechas) {
        super(nombre, vida);
        this.flechas = flechas;
    }

    @Override
    public int atacar() {
        if (flechas == 0) {
            return 2;                      // sin flechas, un golpe con el arco
        }
        flechas--;
        return 9;
    }

    public void recogerFlechas(int cantidad) {
        flechas += cantidad;
    }

    @Override
    public String toString() {
        return flechas + " flechas";
    }
}

class Mago extends Personaje {
    private int mana;

    public Mago(String nombre, int vida, int mana) {
        super(nombre, vida);
        this.mana = mana;
    }

    @Override
    public int atacar() {
        if (mana >= 15) {
            mana -= 15;
            return 18;
        }
        return 3;
    }

    @Override
    public String grito() {
        return "lanza un rayo";
    }
}
```

### Salida esperada

```
Ronda 1
  Nara blande la espada -> 12
  Lía ataca -> 9
  Olmo lanza un rayo -> 18
Ronda 2
  Nara blande la espada -> 12
  Lía ataca -> 9
  Olmo lanza un rayo -> 3
Daño total: 63
Lía recoge flechas: 3 flechas
Casting imposible: una guerrera no es un mago
```

### ¿Para qué sirve?

El polimorfismo es lo que hace extensibles a los programas grandes: un sistema de pagos procesa `Tarjeta`, `Transferencia` y `MercadoPago` con el mismo código; un editor dibuja `Circulo`, `Rectangulo` y `Texto` recorriendo una lista de `Figura`; Swing trata igual a un botón y a una etiqueta porque todos son `JComponent`. Agregar un caso nuevo es agregar una clase, sin tocar lo que ya funciona.

### Errores habituales

**Esqueleto: llamar un método que la variable no conoce.**
```
error: cannot find symbol
        p.recogerFlechas(2);
         ^
  symbol:   method recogerFlechas(int)
  location: variable p of type Personaje
```
El compilador mira el tipo de la variable: si el método es solo de `Arquera`, hace
falta `instanceof` y casting (o, mejor, pensar si el método debería estar en el
padre).

**Goblin: el casting equivocado.** `Exception in thread "main"
java.lang.ClassCastException: class Guerrera cannot be cast to class Mago`.

**Slime: instanciar una clase abstracta.** `Personaje is abstract; cannot be
instantiated`.

**Slime: no implementar el método abstracto.** `Guerrera is not abstract and does
not override abstract method atacar() in Personaje`.

**Ogro: una cadena de `instanceof`.** `if (p instanceof Guerrera) … else if (p
instanceof Arquera) …`: cada vez que agregues una clase vas a tener que tocar ese
código. Poné un método en el padre.

### Micro-misión R02-N06-P1 · Una sola orden

```meta
lugar: El patio de armas de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: Polimorfismo | Personaje[] tropa = {new Guerrera(), new Arquera()} · un mismo mensaje (atacar) · cada objeto responde a su manera
recompensa: xp 10, oro 10
```

#### Escena
En el patio de armas, la Maestra grita una sola orden: **¡Ataquen!** Y cada alumno ataca a su manera. Ella no necesita saber quién es quién: sabe que todos son personajes y que todos saben atacar.

#### Gheco sugiere
Una variable (o un array) del tipo del **padre** puede guardar objetos de cualquier hijo: `Personaje[] tropa`. Al llamar `p.atacar()`, se ejecuta el método del objeto **real**: el de la guerrera, el de la arquera…

#### Desafío
Completá el tipo del array para que entren los tres alumnos.

#### Código inicial
```java
public class Patio {
    public static void main(String[] args) {
        ___[] tropa = {new Guerrera("Lía"), new Arquera("Mira"), new Maga("Sol")};
        for (Personaje p : tropa) {
            System.out.println(p.nombre + ": " + p.atacar());
        }
    }
}

class Personaje {
    String nombre;

    Personaje(String nombre) {
        this.nombre = nombre;
    }

    String atacar() {
        return "empuja";
    }
}

class Guerrera extends Personaje {
    Guerrera(String nombre) { super(nombre); }

    @Override
    String atacar() { return "golpe de espada"; }
}

class Arquera extends Personaje {
    Arquera(String nombre) { super(nombre); }

    @Override
    String atacar() { return "flecha certera"; }
}

class Maga extends Personaje {
    Maga(String nombre) { super(nombre); }

    @Override
    String atacar() { return "rayo"; }
}
```

#### Salida esperada
```
Lía: golpe de espada
Mira: flecha certera
Sol: rayo
```

#### Solución
```java
public class Patio {
    public static void main(String[] args) {
        Personaje[] tropa = {new Guerrera("Lía"), new Arquera("Mira"), new Maga("Sol")};
        for (Personaje p : tropa) {
            System.out.println(p.nombre + ": " + p.atacar());
        }
    }
}

class Personaje {
    String nombre;

    Personaje(String nombre) {
        this.nombre = nombre;
    }

    String atacar() {
        return "empuja";
    }
}

class Guerrera extends Personaje {
    Guerrera(String nombre) { super(nombre); }

    @Override
    String atacar() { return "golpe de espada"; }
}

class Arquera extends Personaje {
    Arquera(String nombre) { super(nombre); }

    @Override
    String atacar() { return "flecha certera"; }
}

class Maga extends Personaje {
    Maga(String nombre) { super(nombre); }

    @Override
    String atacar() { return "rayo"; }
}
```

#### Al superarla
Espada, flecha y rayo, con una sola orden. —Un mismo mensaje, muchas formas de responderlo —dice Gheco—. Eso es el **polimorfismo**.

#### Imagen
- El patio de armas de la Academia: la Maestra de Moldes gritando una orden con el brazo en alto.
- Lía con espada, Mira con arco y Sol con un rayo, atacando a la vez a muñecos de práctica.

### Micro-misión R02-N06-P2 · Nadie es un personaje a secas

```meta
lugar: El patio de armas de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: Clase abstracta | abstract class Personaje · no se puede hacer new Personaje() · abstract String atacar(); obliga a cada hijo a escribirlo
recompensa: xp 15, oro 15
```

#### Escena
—¿Y si alguien sale del molde Personaje, sin ser guerrero ni arquero ni nada? —pregunta Zed. —Sería un alumno que no sabe atacar —dice la Maestra—. Por eso ese molde es **abstracto**: existe para que los demás lo completen.

#### Gheco sugiere
Una clase `abstract` no se puede instanciar: solo sirve de padre. Un método `abstract` no tiene cuerpo (`abstract String atacar();`) y **obliga** a cada hijo concreto a escribirlo. Si una clase tiene un método abstracto, la clase también tiene que ser `abstract`.

#### Desafío
Completá la palabra que hace abstracta a la clase Personaje.

#### Código inicial
```java
public class Abstracto {
    public static void main(String[] args) {
        Personaje[] tropa = {new Guerrera("Lía"), new Arquera("Mira")};
        for (Personaje p : tropa) {
            System.out.println(p.nombre + ": " + p.atacar());
        }
    }
}

___ class Personaje {
    String nombre;

    Personaje(String nombre) {
        this.nombre = nombre;
    }

    abstract String atacar();
}

class Guerrera extends Personaje {
    Guerrera(String nombre) { super(nombre); }

    @Override
    String atacar() { return "golpe de espada"; }
}

class Arquera extends Personaje {
    Arquera(String nombre) { super(nombre); }

    @Override
    String atacar() { return "flecha certera"; }
}
```

#### Salida esperada
```
Lía: golpe de espada
Mira: flecha certera
```

#### Solución
```java
public class Abstracto {
    public static void main(String[] args) {
        Personaje[] tropa = {new Guerrera("Lía"), new Arquera("Mira")};
        for (Personaje p : tropa) {
            System.out.println(p.nombre + ": " + p.atacar());
        }
    }
}

abstract class Personaje {
    String nombre;

    Personaje(String nombre) {
        this.nombre = nombre;
    }

    abstract String atacar();
}

class Guerrera extends Personaje {
    Guerrera(String nombre) { super(nombre); }

    @Override
    String atacar() { return "golpe de espada"; }
}

class Arquera extends Personaje {
    Arquera(String nombre) { super(nombre); }

    @Override
    String atacar() { return "flecha certera"; }
}
```

#### Al superarla
El molde Personaje queda cerrado con un candado: de ahí ya no sale nadie a medio hacer. Solo sirve para que los otros moldes se apoyen en él.

#### Imagen
- El molde viejo «Personaje» con un candado de bronce y la palabra «abstract» grabada.
- Los moldes Guerrera y Arquera, abiertos y brillantes, apoyados en él.

### Micro-misión R02-N06-P3 · La maga disfrazada

```meta
lugar: El patio de armas de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
criatura: goblin
carta: instanceof y casting | if (p instanceof Maga) { Maga m = (Maga) p; m.curar(); } · preguntá antes de convertir · sin preguntar: ClassCastException
recompensa: xp 15, oro 15
```

#### Escena
En la tropa, Lía está herida. Solo una maga puede curar, pero en el array todas son `Personaje`, y un `Personaje` no sabe curar. Un **goblin** se ofrece a convertir a cualquiera en maga «a la fuerza».

#### Gheco sugiere
Con una variable `Personaje` solo se ven los métodos de `Personaje`. Para usar uno de `Maga`, primero preguntá con `instanceof` y después convertí la referencia con un **casting**: `Maga m = (Maga) p;`. Convertir sin preguntar es lo que quiere el goblin.

#### Desafío
Completá el casting para usar a la maga.

#### Código inicial
```java
public class Disfraz {
    public static void main(String[] args) {
        Personaje[] tropa = {new Guerrera("Lía"), new Maga("Sol")};
        for (Personaje p : tropa) {
            if (p instanceof Maga) {
                Maga m = ___;
                System.out.println(m.nombre + " cura: " + m.curar());
            } else {
                System.out.println(p.nombre + " no sabe curar");
            }
        }
    }
}

class Personaje {
    String nombre;

    Personaje(String nombre) { this.nombre = nombre; }
}

class Guerrera extends Personaje {
    Guerrera(String nombre) { super(nombre); }
}

class Maga extends Personaje {
    Maga(String nombre) { super(nombre); }

    int curar() { return 30; }
}
```

#### Salida esperada
```
Lía no sabe curar
Sol cura: 30
```

#### Solución
```java
public class Disfraz {
    public static void main(String[] args) {
        Personaje[] tropa = {new Guerrera("Lía"), new Maga("Sol")};
        for (Personaje p : tropa) {
            if (p instanceof Maga) {
                Maga m = (Maga) p;
                System.out.println(m.nombre + " cura: " + m.curar());
            } else {
                System.out.println(p.nombre + " no sabe curar");
            }
        }
    }
}

class Personaje {
    String nombre;

    Personaje(String nombre) { this.nombre = nombre; }
}

class Guerrera extends Personaje {
    Guerrera(String nombre) { super(nombre); }
}

class Maga extends Personaje {
    Maga(String nombre) { super(nombre); }

    int curar() { return 30; }
}
```

#### Al superarla
Sol cura a Lía. El goblin se queda con las ganas: nadie se convirtió en lo que no era. —Igual —dice la Maestra—, si tenés que preguntar mucho «¿sos maga?», a lo mejor te falta un contrato.

#### Imagen
- Sol curando a Lía con una luz verde.
- Un goblin con un disfraz de maga en las manos, frustrado.

### Micro-misión R02-N06-P4 · El turno de cada uno

```meta
lugar: El patio de armas de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: Lo común en el padre | la clase abstracta escribe lo que todos hacen igual (turno) · deja abstracto lo que cada uno hace distinto (atacar)
recompensa: xp 15, oro 15
```

#### Escena
La Maestra escribe en el molde Personaje cómo es un **turno**: decir el nombre y atacar. Eso es igual para todos. Lo único distinto es **cómo** ataca cada uno. Falta el molde de la arquera.

#### Gheco sugiere
Una clase abstracta puede tener métodos **con cuerpo** que usan los abstractos: `turno()` arma el texto y llama a `atacar()`, que cada hijo escribe a su manera.

#### Desafío
Completá el `return` del `atacar` de la Arquera: "flecha certera".

#### Código inicial
```java
public class Turnos {
    public static void main(String[] args) {
        Personaje[] tropa = {new Guerrera("Lía"), new Arquera("Mira")};
        for (Personaje p : tropa) {
            System.out.println(p.turno());
        }
    }
}

abstract class Personaje {
    String nombre;

    Personaje(String nombre) { this.nombre = nombre; }

    abstract String atacar();

    String turno() {
        return "Turno de " + nombre + ": " + atacar();
    }
}

class Guerrera extends Personaje {
    Guerrera(String nombre) { super(nombre); }

    @Override
    String atacar() { return "golpe de espada"; }
}

class Arquera extends Personaje {
    Arquera(String nombre) { super(nombre); }

    @Override
    String atacar() { return ___; }
}
```

#### Salida esperada
```
Turno de Lía: golpe de espada
Turno de Mira: flecha certera
```

#### Solución
```java
public class Turnos {
    public static void main(String[] args) {
        Personaje[] tropa = {new Guerrera("Lía"), new Arquera("Mira")};
        for (Personaje p : tropa) {
            System.out.println(p.turno());
        }
    }
}

abstract class Personaje {
    String nombre;

    Personaje(String nombre) { this.nombre = nombre; }

    abstract String atacar();

    String turno() {
        return "Turno de " + nombre + ": " + atacar();
    }
}

class Guerrera extends Personaje {
    Guerrera(String nombre) { super(nombre); }

    @Override
    String atacar() { return "golpe de espada"; }
}

class Arquera extends Personaje {
    Arquera(String nombre) { super(nombre); }

    @Override
    String atacar() { return "flecha certera"; }
}
```

#### Al superarla
Dos turnos, un solo método `turno`. Al terminar el ejercicio, Zed intenta abrir con su ganzúa la puerta de la sala de al lado, por costumbre. La ganzúa no entra. En el cartel dice: **Sala de los Pactos**.

#### Imagen
- Lía y Mira tomando turnos frente a un muñeco de práctica.
- Zed con la ganzúa contra una cerradura que no tiene ojo: la puerta de la Sala de los Pactos.

### Misión R02-N06-M1 · El zoológico de criaturas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase abstracta `Criatura` con nombre, un método abstracto `String
sonido()` y uno abstracto `int patas()`, y un método concreto `String presentarse()`
que los use. Subclases concretas: `Dragon`, `Grifo` y `Serpiente`. En el `main`
guardalas en un array de `Criatura`, mostrá la presentación de cada una y el total de
patas del zoológico.

#### Criterio de aprobación

- `Criatura` es abstracta y tiene métodos abstractos y uno concreto.
- El `main` recorre el array sin preguntar el tipo de cada criatura.

#### Salida esperada

```
Ignis dice "ROAAR" y tiene 4 patas
Plumaferro dice "kriii" y tiene 4 patas
Ofidia dice "sss" y tiene 0 patas
Patas en el zoológico: 8
```

#### Solución de referencia

```java
// Mision 1 - El zoologico de criaturas: clase abstracta y polimorfismo.
public class Zoologico {
    public static void main(String[] args) {
        Criatura[] criaturas = {new Dragon("Ignis"), new Grifo("Plumaferro"), new Serpiente("Ofidia")};
        int patas = 0;
        for (Criatura c : criaturas) {
            System.out.println(c.presentarse());
            patas += c.patas();
        }
        System.out.println("Patas en el zoológico: " + patas);
    }
}

abstract class Criatura {
    private final String nombre;

    protected Criatura(String nombre) {
        this.nombre = nombre;
    }

    public abstract String sonido();

    public abstract int patas();

    public String presentarse() {
        return nombre + " dice \"" + sonido() + "\" y tiene " + patas() + " patas";
    }
}

class Dragon extends Criatura {
    public Dragon(String nombre) {
        super(nombre);
    }

    @Override
    public String sonido() {
        return "ROAAR";
    }

    @Override
    public int patas() {
        return 4;
    }
}

class Grifo extends Criatura {
    public Grifo(String nombre) {
        super(nombre);
    }

    @Override
    public String sonido() {
        return "kriii";
    }

    @Override
    public int patas() {
        return 4;
    }
}

class Serpiente extends Criatura {
    public Serpiente(String nombre) {
        super(nombre);
    }

    @Override
    public String sonido() {
        return "sss";
    }

    @Override
    public int patas() {
        return 0;
    }
}
```

### Misión R02-N06-M2 · La nómina polimórfica

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Una clase abstracta `Trabajador` con nombre y un método abstracto `double
pagoMensual()`. Subclases: `Asalariado` (sueldo fijo), `PorHora` (horas y valor por
hora; las horas que pasan de 160 se pagan al 150 %) y `Contratado` (monto del
contrato dividido en los meses que dura). Recorré un array de trabajadores, mostrá el
pago de cada uno con 2 decimales y el total de la nómina. Después, recorré de nuevo y
mostrá **solo** las horas de los `PorHora` usando `instanceof` con pattern matching.

#### Criterio de aprobación

- `pagoMensual` es abstracto y se calcula en cada subclase.
- El total se calcula sin `instanceof`; solo el listado de horas lo usa.

#### Salida esperada

```
Nara     650000.00
Pip      665000.00
Olmo     300000.00
Lía      480000.00
Total   2095000.00
Pip trabajó 180 horas
Lía trabajó 120 horas
```

#### Solución de referencia

```java
// Mision 2 - La nomina polimorfica: metodo abstracto, ligadura dinamica e instanceof.
import java.util.Locale;

public class Nomina {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Trabajador[] nomina = {
            new Asalariado("Nara", 650_000),
            new PorHora("Pip", 180, 3500),
            new Contratado("Olmo", 1_800_000, 6),
            new PorHora("Lía", 120, 4000),
        };
        double total = 0;
        for (Trabajador t : nomina) {
            System.out.printf("%-5s %12.2f%n", t.getNombre(), t.pagoMensual());
            total += t.pagoMensual();
        }
        System.out.printf("Total %12.2f%n", total);
        for (Trabajador t : nomina) {
            if (t instanceof PorHora ph) {
                System.out.println(ph.getNombre() + " trabajó " + ph.getHoras() + " horas");
            }
        }
    }
}

abstract class Trabajador {
    private final String nombre;

    protected Trabajador(String nombre) {
        this.nombre = nombre;
    }

    public String getNombre() {
        return nombre;
    }

    public abstract double pagoMensual();
}

class Asalariado extends Trabajador {
    private final double sueldo;

    public Asalariado(String nombre, double sueldo) {
        super(nombre);
        this.sueldo = sueldo;
    }

    @Override
    public double pagoMensual() {
        return sueldo;
    }
}

class PorHora extends Trabajador {
    private final int horas;
    private final double valorHora;

    public PorHora(String nombre, int horas, double valorHora) {
        super(nombre);
        this.horas = horas;
        this.valorHora = valorHora;
    }

    public int getHoras() {
        return horas;
    }

    @Override
    public double pagoMensual() {
        int normales = Math.min(horas, 160);
        int extra = Math.max(0, horas - 160);
        return normales * valorHora + extra * valorHora * 1.5;
    }
}

class Contratado extends Trabajador {
    private final double monto;
    private final int meses;

    public Contratado(String nombre, double monto, int meses) {
        super(nombre);
        this.monto = monto;
        this.meses = meses;
    }

    @Override
    public double pagoMensual() {
        return monto / meses;
    }
}
```

### Misión R02-N06-M3 · Las trampas de la mazmorra

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Una clase abstracta `Trampa` con un método abstracto `int activar(int vidaDelHeroe)`
que devuelve la vida que le queda al héroe, y un método concreto `String nombre()`.
Tres trampas: `Pinchos` (quita 10), `Veneno` (quita el 25 % de la vida actual,
redondeando para abajo) y `Fuente` (no es una trampa mala: **suma** 15, sin pasar de
100). Nadia arranca con 80 de vida y cruza un pasillo de 6 trampas guardadas en un
array. Mostrá la vida después de cada una y si llega a la salida.

#### Criterio de aprobación

- Cada trampa implementa `activar` a su manera.
- El recorrido del pasillo no pregunta el tipo de trampa.

#### Salida esperada

```
Pinchos -> vida 70
Veneno -> vida 53
Fuente curativa -> vida 68
Pinchos -> vida 58
Veneno -> vida 44
Pinchos -> vida 34
¡Nadia llega a la salida con 34 de vida!
```

#### Solución de referencia

```java
// Mision 3 - Las trampas de la mazmorra: polimorfismo con un metodo que transforma un valor.
public class Mazmorra {
    public static void main(String[] args) {
        Trampa[] pasillo = {new Pinchos(), new Veneno(), new Fuente(), new Pinchos(), new Veneno(), new Pinchos()};
        int vida = 80;
        for (Trampa t : pasillo) {
            vida = t.activar(vida);
            System.out.println(t.nombre() + " -> vida " + vida);
            if (vida <= 0) {
                break;
            }
        }
        System.out.println(vida > 0 ? "¡Nadia llega a la salida con " + vida + " de vida!" : "Nadia cae en la mazmorra");
    }
}

abstract class Trampa {
    public abstract int activar(int vidaDelHeroe);

    public String nombre() {
        return getClass().getSimpleName();
    }
}

class Pinchos extends Trampa {
    @Override
    public int activar(int vida) {
        return vida - 10;
    }
}

class Veneno extends Trampa {
    @Override
    public int activar(int vida) {
        return vida - vida / 4;
    }
}

class Fuente extends Trampa {
    @Override
    public int activar(int vida) {
        return Math.min(100, vida + 15);
    }

    @Override
    public String nombre() {
        return "Fuente curativa";
    }
}
```

### Encargo R02-N06-E1 · Los medios de pago

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una tienda acepta varios medios de pago. Clase abstracta `MedioPago` con un método
abstracto `double totalAPagar(double monto)` y uno abstracto `String descripcion()`.
Implementá `Efectivo` (10 % de descuento), `Debito` (sin cambios) y `Credito` (con
cuotas: 3 cuotas recargan 10 %, 6 cuotas 20 %, 1 cuota nada). Para una compra de
50 000, mostrá el total con cada medio y cuál conviene.

#### Criterio de aprobación

- La elección del más barato recorre un array de `MedioPago` sin `instanceof`.
- Los montos se muestran con 2 decimales.

#### Salida esperada

```
Efectivo (-10%)        45000.00
Débito                 50000.00
Crédito 1 cuota        50000.00
Crédito 3 cuotas       55000.00
Crédito 6 cuotas       60000.00
Conviene: Efectivo (-10%)
```

#### Solución de referencia

```java
// Encargo - Los medios de pago: polimorfismo para comparar opciones.
import java.util.Locale;

public class Caja {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        double compra = 50_000;
        MedioPago[] medios = {new Efectivo(), new Debito(), new Credito(1), new Credito(3), new Credito(6)};
        MedioPago mejor = medios[0];
        for (MedioPago m : medios) {
            System.out.printf("%-20s %10.2f%n", m.descripcion(), m.totalAPagar(compra));
            if (m.totalAPagar(compra) < mejor.totalAPagar(compra)) {
                mejor = m;
            }
        }
        System.out.println("Conviene: " + mejor.descripcion());
    }
}

abstract class MedioPago {
    public abstract double totalAPagar(double monto);

    public abstract String descripcion();
}

class Efectivo extends MedioPago {
    @Override
    public double totalAPagar(double monto) {
        return monto * 0.9;
    }

    @Override
    public String descripcion() {
        return "Efectivo (-10%)";
    }
}

class Debito extends MedioPago {
    @Override
    public double totalAPagar(double monto) {
        return monto;
    }

    @Override
    public String descripcion() {
        return "Débito";
    }
}

class Credito extends MedioPago {
    private final int cuotas;

    public Credito(int cuotas) {
        this.cuotas = cuotas;
    }

    @Override
    public double totalAPagar(double monto) {
        double recargo = switch (cuotas) {
            case 3 -> 0.10;
            case 6 -> 0.20;
            default -> 0;
        };
        return monto * (1 + recargo);
    }

    @Override
    public String descripcion() {
        return "Crédito " + cuotas + " cuota" + (cuotas == 1 ? "" : "s");
    }
}
```

### Prueba del sello

#### Si `Personaje p = new Guerrera(...)` y las dos clases tienen `atacar()`, ¿cuál se ejecuta en `p.atacar()`?

El de `Guerrera`: la JVM usa la versión del objeto real (ligadura dinámica).

#### ¿Por qué `p.recogerFlechas()` no compila si `p` es de tipo `Personaje`?

Porque el compilador solo permite los métodos que declara el tipo de la variable.

#### ¿Qué diferencia hay entre una clase abstracta y una clase común?

La abstracta no se puede instanciar y puede tener métodos abstractos (sin cuerpo) que las subclases están obligadas a implementar.

#### ¿Qué hace `if (p instanceof Arquera a)`?

Pregunta si `p` es una `Arquera` y, si lo es, la deja disponible convertida en la variable `a`.

#### Nombrá los tres tipos de polimorfismo y un ejemplo de cada uno.

De inclusión (una `Guerrera` usada como `Personaje`), ad hoc o sobrecarga (`mayor(int,int)` y `mayor(double,double)`) y paramétrico (genéricos: `ArrayList<String>`).

### Soluciones (docente)

Sale de `18-Java/14-Polimorfismo-Abstractas` (unidades 1 y 2). Corrige la tabla del capítulo original, que llamaba "paramétrico" a la sobrecarga y contaba a `instanceof` como un tipo de polimorfismo. El pattern matching de `instanceof` es de Java 16+.

## R02-N07 · Interfaces: contratos

```meta
tipo: tema
padre: R02-N06
precio: 10
criatura: skeleton
temas: poo.interfaces
```

### Crónica

La puerta de la Sala de los Pactos no tiene cerradura, y la ganzúa de Zed no sirve de nada. Adentro cuelgan pergaminos firmados: *«Quien firme este contrato se compromete a saber nadar»*, *«…a saber volar»*, *«…a poder ser comparado»*. Un grifo firmó el de volar y el de nadar. Un barco firmó el de nadar. No se parecen en nada, pero los dos cumplen el mismo contrato.

—En el Imperio, las puertas se abren con **contratos** —explica {mentor}—. La herencia dice qué **sos**; una interfaz dice qué **sabés hacer**. Y a diferencia de los moldes, podés firmar todos los que quieras.

### Objetivos

- Declarar interfaces e implementarlas con `implements`.
- Usar una interfaz como tipo para tratar igual a clases que no se parecen.
- Implementar varias interfaces a la vez.
- Usar métodos `default` y constantes en una interfaz.
- Implementar `Comparable` para ordenar objetos con `Arrays.sort`.

### Antes de empezar

- Polimorfismo y clases abstractas.

### Explicación

#### Una interfaz es un contrato
Una **interfaz** declara qué métodos tiene que tener una clase, sin decir cómo:
```java
interface Nadador {
    void nadar(int metros);          // public y abstract automáticamente
    int velocidadEnAgua();
}

class Grifo implements Nadador {      // "firma" el contrato
    @Override
    public void nadar(int metros) { … }

    @Override
    public int velocidadEnAgua() { return 4; }
}
```
La clase que dice `implements Nadador` **tiene que** implementar todos sus métodos
(con `public`), o el compilador no la deja pasar.

#### La interfaz como tipo
Como con la herencia, una variable de tipo `Nadador` puede apuntar a cualquier objeto
que implemente la interfaz, aunque las clases no tengan nada más en común:
```java
Nadador[] nadadores = {new Grifo(), new Barco(), new Nadia()};
for (Nadador n : nadadores) {
    n.nadar(100);
}
```

#### Varias interfaces a la vez
Una clase hereda de **una** clase pero puede implementar **muchas** interfaces:
```java
class Grifo extends Criatura implements Volador, Nadador { … }
```
Así se resuelve lo que la herencia simple no permite: ser varias cosas a la vez.

#### Métodos `default` y constantes
Desde Java 8, una interfaz puede traer métodos con código, marcados `default`. Las
clases los heredan y pueden sobrescribirlos:
```java
interface Nadador {
    int velocidadEnAgua();

    default String describirNado() {
        return "nada a " + velocidadEnAgua() + " m/s";
    }
}
```
Una interfaz también puede tener **constantes** (son `public static final`
automáticamente) y métodos `static`. Lo que **no** tiene es estado: no hay atributos
de instancia ni constructores.

#### Interfaz o clase abstracta
| | Clase abstracta | Interfaz |
|---|---|---|
| Qué expresa | "es un" (una familia) | "sabe hacer" (una capacidad) |
| Cuántas | se hereda de una sola | se implementan muchas |
| Atributos | sí, con estado | solo constantes |
| Constructores | sí | no |
| Métodos con código | sí | solo `default` y `static` |

Regla práctica: si varias clases **comparten datos y código**, clase abstracta; si
solo **comparten una capacidad**, interfaz.

#### `Comparable`: una interfaz de la biblioteca
Java trae muchas interfaces. `Comparable` es la que usa `Arrays.sort` para ordenar
objetos: la clase implementa `compareTo`, que devuelve un número negativo si `this` va
antes que el otro, 0 si son iguales y positivo si va después:
```java
class Heroe implements Comparable<Heroe> {
    …
    @Override
    public int compareTo(Heroe otro) {
        return Integer.compare(otro.nivel, this.nivel);   // de mayor a menor nivel
    }
}
Arrays.sort(grupo);    // ahora sabe ordenarlos
```
El `<Heroe>` indica con qué tipo se compara (son los *genéricos*, que se explican en
la rama 3). `Integer.compare(a, b)` y `a.compareTo(b)` entre textos arman el resultado
sin errores de desbordamiento.

> **Si venís de C++.** Una interfaz es una clase con todos sus métodos virtuales
> puros, pero con reglas propias: Java no tiene herencia múltiple de clases, sí de
> interfaces.
>
> **Si venís de Python.** Se parece a una clase abstracta de `abc`, pero la verifica el
> compilador. En Python alcanza con tener el método (*duck typing*); en Java hay que
> declarar el `implements`.

### Código de ejemplo

```java
/*
 * Interfaces: los contratos de la sala de los pactos.
 */
import java.util.Arrays;

public class SalaDePactos {
    public static void main(String[] args) {
        Grifo grifo = new Grifo("Plumaferro");
        Barco barco = new Barco("La Tetera");
        Pato pato = new Pato();

        // La misma interfaz, clases que no se parecen
        Nadador[] nadadores = {grifo, barco, pato};
        for (Nadador n : nadadores) {
            System.out.println(n.getClass().getSimpleName() + " " + n.describirNado());
        }

        Volador[] voladores = {grifo, pato};
        for (Volador v : voladores) {
            System.out.println(v.getClass().getSimpleName() + " vuela hasta " + v.alturaMaxima() + " m");
        }
        System.out.println("Altura mínima de vuelo en el Imperio: " + Volador.ALTURA_MINIMA + " m");

        // Comparable: ordenar objetos propios
        Aspirante[] aspirantes = {
            new Aspirante("Pip", 72), new Aspirante("Lía", 95), new Aspirante("Olmo", 72), new Aspirante("Nara", 88),
        };
        Arrays.sort(aspirantes);
        System.out.println("Orden de mérito: " + Arrays.toString(aspirantes));
    }
}

interface Nadador {
    int velocidadEnAgua();

    default String describirNado() {
        return "nada a " + velocidadEnAgua() + " m/s";
    }
}

interface Volador {
    int ALTURA_MINIMA = 2;          // constante: public static final

    int alturaMaxima();
}

class Grifo implements Nadador, Volador {
    private final String nombre;

    public Grifo(String nombre) {
        this.nombre = nombre;
    }

    @Override
    public int velocidadEnAgua() {
        return 3;
    }

    @Override
    public int alturaMaxima() {
        return 900;
    }

    @Override
    public String describirNado() {       // sobrescribe el default
        return "(" + nombre + ") nada mal, a " + velocidadEnAgua() + " m/s";
    }
}

class Barco implements Nadador {
    private final String nombre;

    public Barco(String nombre) {
        this.nombre = nombre;
    }

    @Override
    public int velocidadEnAgua() {
        return 8;
    }
}

class Pato implements Nadador, Volador {
    @Override
    public int velocidadEnAgua() {
        return 1;
    }

    @Override
    public int alturaMaxima() {
        return 300;
    }
}

class Aspirante implements Comparable<Aspirante> {
    private final String nombre;
    private final int puntaje;

    public Aspirante(String nombre, int puntaje) {
        this.nombre = nombre;
        this.puntaje = puntaje;
    }

    @Override
    public int compareTo(Aspirante otro) {
        int porPuntaje = Integer.compare(otro.puntaje, this.puntaje);   // mayor puntaje primero
        if (porPuntaje != 0) {
            return porPuntaje;
        }
        return this.nombre.compareTo(otro.nombre);                       // empate: alfabético
    }

    @Override
    public String toString() {
        return nombre + " " + puntaje;
    }
}
```

### Salida esperada

```
Grifo (Plumaferro) nada mal, a 3 m/s
Barco nada a 8 m/s
Pato nada a 1 m/s
Grifo vuela hasta 900 m
Pato vuela hasta 300 m
Altura mínima de vuelo en el Imperio: 2 m
Orden de mérito: [Lía 95, Nara 88, Olmo 72, Pip 72]
```

### ¿Para qué sirve?

Las interfaces son el pegamento de los sistemas grandes: un programa guarda datos "en algún lugar que implemente `Repositorio`" y se le puede cambiar la base de datos sin tocar el resto; Swing avisa los clics a "quien implemente `ActionListener`"; JDBC funciona con cualquier base porque todas implementan `Connection`. Programar contra interfaces es la base del diseño en capas que vas a usar en la rama del escritorio.

### Errores habituales

**Slime: no implementar un método de la interfaz.**
```
SalaDePactos.java:40: error: Barco is not abstract and does not override abstract method velocidadEnAgua() in Nadador
class Barco implements Nadador {
^
```

**Slime: implementar sin `public`.** Los métodos de una interfaz son públicos: `void
nadar()` en la clase da `attempting to assign weaker access privileges; was public`.

**Esqueleto: instanciar una interfaz.** `new Nadador()` no compila: `Nadador is
abstract; cannot be instantiated`.

**Ogro: `compareTo` restando.** `return this.puntaje - otro.puntaje;` parece andar,
pero con números muy grandes se desborda y ordena mal. Usá `Integer.compare`.

**Goblin: ordenar objetos que no son `Comparable`.** `Arrays.sort` con una clase que
no implementa `Comparable` corta con `ClassCastException: class Aspirante cannot be
cast to class java.lang.Comparable`.

### Micro-misión R02-N07-P1 · La puerta sin cerradura

```meta
lugar: La Sala de los Pactos
personajes: Zed, Gheco, Nadia, Kaffa
carta: interface | interface Nadador { String nadar(); } · un contrato: QUÉ sabe hacer · class Barco implements Nadador lo firma y lo cumple
recompensa: xp 10, oro 10
```

#### Escena
La puerta de la Sala de los Pactos no tiene cerradura: tiene un pergamino. **Kaffa** aparece con su taza de café. —En el Imperio, las puertas no se abren con ganzúa, Zed. Se abren con **contratos**. Adentro cuelgan muchos: «quien firme este se compromete a saber nadar».

#### Gheco sugiere
Una **interfaz** dice qué métodos tiene que tener quien la firme, sin decir cómo. `class Barco implements Nadador` firma el contrato y **tiene** que escribir `nadar()`. Un barco y un grifo no se parecen, pero los dos pueden nadar.

#### Desafío
Completá la palabra con la que el Barco firma el contrato `Nadador`.

#### Código inicial
```java
public class Pactos {
    public static void main(String[] args) {
        Nadador[] nadadores = {new Grifo(), new Barco()};
        for (Nadador n : nadadores) {
            System.out.println(n.nadar());
        }
    }
}

interface Nadador {
    String nadar();
}

class Grifo implements Nadador {
    public String nadar() { return "El grifo nada con las alas plegadas"; }
}

class Barco ___ Nadador {
    public String nadar() { return "El barco flota y avanza"; }
}
```

#### Salida esperada
```
El grifo nada con las alas plegadas
El barco flota y avanza
```

#### Solución
```java
public class Pactos {
    public static void main(String[] args) {
        Nadador[] nadadores = {new Grifo(), new Barco()};
        for (Nadador n : nadadores) {
            System.out.println(n.nadar());
        }
    }
}

interface Nadador {
    String nadar();
}

class Grifo implements Nadador {
    public String nadar() { return "El grifo nada con las alas plegadas"; }
}

class Barco implements Nadador {
    public String nadar() { return "El barco flota y avanza"; }
}
```

#### Al superarla
Un grifo y un barco, en el mismo array, porque los dos cumplen el contrato. —La herencia dice qué **sos** —dice Kaffa—. Una interfaz dice qué **sabés hacer**.

#### Imagen
- La Sala de los Pactos: pergaminos firmados colgando de las paredes, con sellos de cera.
- Kaffa (el Arquitecto Imperial) con su taza de café; Zed mirando su ganzúa inútil.
- Un grifo y un pequeño barco dibujados en el mismo pergamino «Nadador».

### Micro-misión R02-N07-P2 · Todos los contratos que quieras

```meta
lugar: La Sala de los Pactos
personajes: Zed, Gheco, Nadia, Kaffa
carta: Varias interfaces | class Grifo implements Volador, Nadador · se heredan de UNA clase, pero se firman muchas interfaces
recompensa: xp 15, oro 15
```

#### Escena
El grifo firmó dos pergaminos: el de volar y el de nadar. —Moldes padre hay uno solo —dice Kaffa—. Contratos, todos los que puedas cumplir.

#### Gheco sugiere
Una clase puede implementar **varias** interfaces, separadas por coma: `implements Volador, Nadador`. Tiene que escribir los métodos de todas.

#### Desafío
Completá la segunda interfaz que firma el Grifo.

#### Código inicial
```java
public class DosContratos {
    public static void main(String[] args) {
        Grifo g = new Grifo();
        System.out.println(g.volar());
        System.out.println(g.nadar());
        Volador v = g;
        Nadador n = g;
        System.out.println("Vuela y nada: " + (v == n));
    }
}

interface Volador {
    String volar();
}

interface Nadador {
    String nadar();
}

class Grifo implements Volador, ___ {
    public String volar() { return "El grifo sube en espiral"; }

    public String nadar() { return "El grifo nada con las alas plegadas"; }
}
```

#### Salida esperada
```
El grifo sube en espiral
El grifo nada con las alas plegadas
Vuela y nada: true
```

#### Solución
```java
public class DosContratos {
    public static void main(String[] args) {
        Grifo g = new Grifo();
        System.out.println(g.volar());
        System.out.println(g.nadar());
        Volador v = g;
        Nadador n = g;
        System.out.println("Vuela y nada: " + (v == n));
    }
}

interface Volador {
    String volar();
}

interface Nadador {
    String nadar();
}

class Grifo implements Volador, Nadador {
    public String volar() { return "El grifo sube en espiral"; }

    public String nadar() { return "El grifo nada con las alas plegadas"; }
}
```

#### Al superarla
El mismo grifo, visto como Volador o como Nadador: `true`, es uno solo. Nadia anota en su libreta: «contratos: muchos. Padres: uno».

#### Imagen
- Un grifo dorado con dos pergaminos firmados atados al cuello: «Volador» y «Nadador».
- Nadia anotando en su libreta.

### Micro-misión R02-N07-P3 · La cláusula por defecto

```meta
lugar: La Sala de los Pactos
personajes: Zed, Gheco, Nadia, Kaffa
carta: Método default | default String bucear() { … } en la interfaz · ya viene escrito · quien firma puede usarlo o sobrescribirlo
recompensa: xp 15, oro 15
```

#### Escena
Al contrato de nadar le agregaron una cláusula nueva: **bucear**. Los que ya lo habían firmado no quieren reescribir nada. —Entonces la cláusula viene **con su respuesta por defecto** —dice Kaffa—. El que quiera, la cambia.

#### Gheco sugiere
Un método `default` en una interfaz tiene cuerpo: todas las clases que la firman lo reciben hecho. Una clase puede sobrescribirlo si necesita otra cosa.

#### Desafío
Completá la palabra que le da cuerpo a `bucear` dentro de la interfaz.

#### Código inicial
```java
public class Clausula {
    public static void main(String[] args) {
        Nadador[] nadadores = {new Grifo(), new Submarino()};
        for (Nadador n : nadadores) {
            System.out.println(n.bucear());
        }
    }
}

interface Nadador {
    String nadar();

    ___ String bucear() {
        return "se sumerge un poco y sube";
    }
}

class Grifo implements Nadador {
    public String nadar() { return "nada"; }
}

class Submarino implements Nadador {
    public String nadar() { return "avanza"; }

    @Override
    public String bucear() { return "baja hasta el fondo del río"; }
}
```

#### Salida esperada
```
se sumerge un poco y sube
baja hasta el fondo del río
```

#### Solución
```java
public class Clausula {
    public static void main(String[] args) {
        Nadador[] nadadores = {new Grifo(), new Submarino()};
        for (Nadador n : nadadores) {
            System.out.println(n.bucear());
        }
    }
}

interface Nadador {
    String nadar();

    default String bucear() {
        return "se sumerge un poco y sube";
    }
}

class Grifo implements Nadador {
    public String nadar() { return "nada"; }
}

class Submarino implements Nadador {
    public String nadar() { return "avanza"; }

    @Override
    public String bucear() { return "baja hasta el fondo del río"; }
}
```

#### Al superarla
El grifo bucea un poco y sube; el submarino llega al fondo. Nadie tuvo que reescribir el contrato viejo.

#### Imagen
- Un pergamino de contrato con una cláusula nueva agregada abajo, brillando.
- Un grifo sumergiéndose apenas en el río; a su lado, un submarino de bronce bajando al fondo.

### Micro-misión R02-N07-P4 · La ganzúa echa dientes

```meta
lugar: La Sala de los Pactos
personajes: Zed, Gheco, Nadia, Kaffa
carta: Comparable | class Llave implements Comparable<Llave> · int compareTo(Llave otra) · Arrays.sort(llaves) usa ese orden
recompensa: xp 15, oro 20
```

#### Escena
El último pergamino dice: «quien firme este se compromete a **poder ser comparado**». Kaffa le pide a Zed que ordene las llaves del Imperio por cantidad de dientes. Zed apoya su ganzúa en la mesa, al lado de las llaves, y le parece que se mueve.

#### Gheco sugiere
`Comparable<Llave>` obliga a escribir `compareTo(Llave otra)`: negativo si esta va antes, positivo si va después, 0 si da igual. Para enteros: `Integer.compare(dientes, otra.dientes)`. Con eso, `Arrays.sort(llaves)` sabe ordenarlas.

#### Desafío
Completá el `return` de `compareTo`: de menos dientes a más.

#### Código inicial
```java
import java.util.Arrays;

public class Llaves {
    public static void main(String[] args) {
        Llave[] llaves = {new Llave("la del Archivo", 7), new Llave("la de la Torre", 12), new Llave("la ganzúa de Zed", 1), new Llave("la del Cofre", 4)};
        Arrays.sort(llaves);
        for (Llave l : llaves) {
            System.out.println(l.dientes + " dientes: " + l.nombre);
        }
    }
}

class Llave implements Comparable<Llave> {
    String nombre;
    int dientes;

    Llave(String nombre, int dientes) {
        this.nombre = nombre;
        this.dientes = dientes;
    }

    @Override
    public int compareTo(Llave otra) {
        return ___;
    }
}
```

#### Salida esperada
```
1 dientes: la ganzúa de Zed
4 dientes: la del Cofre
7 dientes: la del Archivo
12 dientes: la de la Torre
```

#### Solución
```java
import java.util.Arrays;

public class Llaves {
    public static void main(String[] args) {
        Llave[] llaves = {new Llave("la del Archivo", 7), new Llave("la de la Torre", 12), new Llave("la ganzúa de Zed", 1), new Llave("la del Cofre", 4)};
        Arrays.sort(llaves);
        for (Llave l : llaves) {
            System.out.println(l.dientes + " dientes: " + l.nombre);
        }
    }
}

class Llave implements Comparable<Llave> {
    String nombre;
    int dientes;

    Llave(String nombre, int dientes) {
        this.nombre = nombre;
        this.dientes = dientes;
    }

    @Override
    public int compareTo(Llave otra) {
        return Integer.compare(dientes, otra.dientes);
    }
}
```

#### Al superarla
Las llaves quedan en fila. La ganzúa de Zed, primera, con un solo diente… y de repente, con un chasquido, le **crece un segundo diente**, como a una llave de verdad. Kaffa sonríe detrás de su taza. —Firmaste tu primer contrato.
En el taller de al lado, un aprendiz intenta que un caballero herede de una armadura, de una espada y de un caballo a la vez.

#### Imagen
- Cuatro llaves ordenadas sobre una mesa, de menos a más dientes; la ganzúa de Zed, primera, echando un segundo diente con un destello.
- Kaffa sonriendo detrás de su taza; Zed mirando la ganzúa, asombrado.

### Misión R02-N07-M1 · Los curanderos

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Declará una interfaz `Curador` con `int curar(int vidaActual)` (devuelve la vida
después de curar) y un método `default String describir()` que diga `"cura"`. Tres
clases que no se parecen la implementan: `Clerigo` (suma 20), `PocionMenor` (suma 8) y
`Fuente` (deja la vida en 100). La vida nunca pasa de 100. Nadia empieza con 35 y usa,
en orden, los tres curadores guardados en un array de `Curador`: mostrá la vida
después de cada uno. `Fuente` sobrescribe `describir()`.

#### Criterio de aprobación

- Las tres clases implementan `Curador` y se usan a través de la interfaz.
- Hay un método `default` y al menos una clase lo sobrescribe.

#### Salida esperada

```
Vida inicial: 35
PocionMenor cura -> 43
Clerigo cura -> 63
Fuente restaura toda la vida -> 100
```

#### Solución de referencia

```java
// Mision 1 - Los curanderos: una interfaz implementada por clases distintas.
public class Curanderos {
    public static void main(String[] args) {
        Curador[] curadores = {new PocionMenor(), new Clerigo(), new Fuente()};
        int vida = 35;
        System.out.println("Vida inicial: " + vida);
        for (Curador c : curadores) {
            vida = c.curar(vida);
            System.out.println(c.getClass().getSimpleName() + " " + c.describir() + " -> " + vida);
        }
    }
}

interface Curador {
    int VIDA_MAXIMA = 100;

    int curar(int vidaActual);

    default String describir() {
        return "cura";
    }
}

class Clerigo implements Curador {
    @Override
    public int curar(int vidaActual) {
        return Math.min(VIDA_MAXIMA, vidaActual + 20);
    }
}

class PocionMenor implements Curador {
    @Override
    public int curar(int vidaActual) {
        return Math.min(VIDA_MAXIMA, vidaActual + 8);
    }
}

class Fuente implements Curador {
    @Override
    public int curar(int vidaActual) {
        return VIDA_MAXIMA;
    }

    @Override
    public String describir() {
        return "restaura toda la vida";
    }
}
```

### Misión R02-N07-M2 · El ranking de la arena

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Luchador` (nombre, victorias, derrotas) que implemente
`Comparable<Luchador>`: se ordena por **más victorias**; si empatan, por **menos
derrotas**; y si también empatan, por nombre alfabético. Agregá un método
`double efectividad()` (victorias sobre combates, en porcentaje). Ordená un array de
6 luchadores con `Arrays.sort` y mostrá el ranking con `printf`.

#### Criterio de aprobación

- `compareTo` usa `Integer.compare` y los tres criterios en orden.
- El ranking sale de `Arrays.sort`.

#### Salida esperada

```
1. Lía    15V  2D   88.2%
2. Nara   15V  5D   75.0%
3. Ada    12V  1D   92.3%
4. Pip    12V  1D   92.3%
5. Baldo  12V  3D   80.0%
6. Olmo    4V  9D   30.8%
```

#### Solución de referencia

```java
// Mision 2 - El ranking de la arena: Comparable con tres criterios.
import java.util.Arrays;
import java.util.Locale;

public class Arena {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Luchador[] luchadores = {
            new Luchador("Baldo", 12, 3), new Luchador("Nara", 15, 5), new Luchador("Pip", 12, 1),
            new Luchador("Ada", 12, 1), new Luchador("Olmo", 4, 9), new Luchador("Lía", 15, 2),
        };
        Arrays.sort(luchadores);
        int puesto = 1;
        for (Luchador l : luchadores) {
            System.out.printf("%d. %-6s %2dV %2dD  %5.1f%%%n", puesto, l.getNombre(), l.getVictorias(), l.getDerrotas(), l.efectividad());
            puesto++;
        }
    }
}

class Luchador implements Comparable<Luchador> {
    private final String nombre;
    private final int victorias;
    private final int derrotas;

    public Luchador(String nombre, int victorias, int derrotas) {
        this.nombre = nombre;
        this.victorias = victorias;
        this.derrotas = derrotas;
    }

    public String getNombre() {
        return nombre;
    }

    public int getVictorias() {
        return victorias;
    }

    public int getDerrotas() {
        return derrotas;
    }

    public double efectividad() {
        return 100.0 * victorias / (victorias + derrotas);
    }

    @Override
    public int compareTo(Luchador otro) {
        int c = Integer.compare(otro.victorias, victorias);
        if (c != 0) {
            return c;
        }
        c = Integer.compare(derrotas, otro.derrotas);
        if (c != 0) {
            return c;
        }
        return nombre.compareTo(otro.nombre);
    }
}
```

### Misión R02-N07-M3 · Lo que se puede vender

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

En el mercado del Imperio se venden cosas muy distintas. Declará una interfaz
`Vendible` con `double precio()` y `String etiqueta()`, y una interfaz `Gravable` con
`double impuesto()` (una tasa, por ejemplo 0.21) y un método `default double
precioFinal()`… que no puede ir en `Gravable` porque no conoce el precio. Resolvelo
así: `Gravable` **extiende** `Vendible` (`interface Gravable extends Vendible`) y
agrega el `default precioFinal()` = precio × (1 + impuesto). Implementá `Pan`
(`Vendible`, sin impuesto), `Espada` y `Servicio` (`Gravable`). Mostrá precio y precio
final de cada uno, usando `instanceof` solo para saber si se le cobra impuesto.

#### Criterio de aprobación

- Una interfaz extiende a otra.
- `precioFinal` es un método `default` que usa los otros métodos de la interfaz.

#### Salida esperada

```
Pan        1200.00 ->   1200.00
Espada    85000.00 -> 102850.00
Afilado    3000.00 ->   3315.00
Total                 107365.00
```

#### Solución de referencia

```java
// Mision 3 - Lo que se puede vender: una interfaz que extiende a otra, con un default.
import java.util.Locale;

public class Mercado {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Vendible[] cosas = {new Pan(), new Espada(), new Servicio("Afilado", 3000)};
        double total = 0;
        for (Vendible v : cosas) {
            double precioFinal = v instanceof Gravable g ? g.precioFinal() : v.precio();
            System.out.printf("%-8s %9.2f -> %9.2f%n", v.etiqueta(), v.precio(), precioFinal);
            total += precioFinal;
        }
        System.out.printf("Total    %22.2f%n", total);
    }
}

interface Vendible {
    double precio();

    String etiqueta();
}

interface Gravable extends Vendible {
    double impuesto();

    default double precioFinal() {
        return precio() * (1 + impuesto());
    }
}

class Pan implements Vendible {
    @Override
    public double precio() {
        return 1200;
    }

    @Override
    public String etiqueta() {
        return "Pan";
    }
}

class Espada implements Gravable {
    @Override
    public double precio() {
        return 85000;
    }

    @Override
    public String etiqueta() {
        return "Espada";
    }

    @Override
    public double impuesto() {
        return 0.21;
    }
}

class Servicio implements Gravable {
    private final String nombre;
    private final double precio;

    public Servicio(String nombre, double precio) {
        this.nombre = nombre;
        this.precio = precio;
    }

    @Override
    public double precio() {
        return precio;
    }

    @Override
    public String etiqueta() {
        return nombre;
    }

    @Override
    public double impuesto() {
        return 0.105;
    }
}
```

### Encargo R02-N07-E1 · Las notificaciones

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un sistema avisa los vencimientos por distintos canales. Una interfaz `Notificador`
con `boolean enviar(String destino, String mensaje)` (devuelve si se pudo) y un método
`default String nombre()`. Implementaciones: `Email` (solo acepta destinos con `@`),
`Sms` (solo acepta destinos de 10 dígitos y corta el mensaje a 20 caracteres) y
`Consola` (siempre funciona y muestra el mensaje). Enviá el mismo aviso a tres
destinos por los tres canales y mostrá qué salió y qué no. Los "envíos" se simulan
mostrando texto.

#### Criterio de aprobación

- Los tres canales implementan la misma interfaz y se recorren en un array.
- Cada uno valida el destino a su manera.

#### Salida esperada

```
Email para ana@correo.com: Tu cuota vence el viernes 10
  [Email a ana@correo.com] enviado
  [SMS a ana@correo.com] no corresponde
>> ana@correo.com: Tu cuota vence el viernes 10
  [Consola a ana@correo.com] enviado
  [Email a 3804123456] no corresponde
SMS a 3804123456: Tu cuota vence el vi…
  [SMS a 3804123456] enviado
>> 3804123456: Tu cuota vence el viernes 10
  [Consola a 3804123456] enviado
  [Email a vecino] no corresponde
  [SMS a vecino] no corresponde
>> vecino: Tu cuota vence el viernes 10
  [Consola a vecino] enviado
```

#### Solución de referencia

```java
// Encargo - Las notificaciones: una interfaz, tres canales.
public class Avisos {
    public static void main(String[] args) {
        Notificador[] canales = {new Email(), new Sms(), new Consola()};
        String[] destinos = {"ana@correo.com", "3804123456", "vecino"};
        String mensaje = "Tu cuota vence el viernes 10";
        for (String destino : destinos) {
            for (Notificador canal : canales) {
                boolean ok = canal.enviar(destino, mensaje);
                System.out.println("  [" + canal.nombre() + " a " + destino + "] " + (ok ? "enviado" : "no corresponde"));
            }
        }
    }
}

interface Notificador {
    boolean enviar(String destino, String mensaje);

    default String nombre() {
        return getClass().getSimpleName();
    }
}

class Email implements Notificador {
    @Override
    public boolean enviar(String destino, String mensaje) {
        if (!destino.contains("@")) {
            return false;
        }
        System.out.println("Email para " + destino + ": " + mensaje);
        return true;
    }
}

class Sms implements Notificador {
    @Override
    public boolean enviar(String destino, String mensaje) {
        if (!destino.matches("\\d{10}")) {
            return false;
        }
        String corto = mensaje.length() > 20 ? mensaje.substring(0, 20) + "…" : mensaje;
        System.out.println("SMS a " + destino + ": " + corto);
        return true;
    }

    @Override
    public String nombre() {
        return "SMS";
    }
}

class Consola implements Notificador {
    @Override
    public boolean enviar(String destino, String mensaje) {
        System.out.println(">> " + destino + ": " + mensaje);
        return true;
    }
}
```

### Prueba del sello

#### ¿Qué diferencia hay entre `extends` e `implements`?

`extends` hereda de una clase (una sola); `implements` firma el contrato de una o varias interfaces.

#### ¿Qué pasa si una clase implementa una interfaz y le falta un método?

No compila, salvo que la clase sea abstracta.

#### ¿Para qué sirven los métodos `default`?

Para dar una implementación por defecto dentro de la interfaz, que las clases heredan y pueden sobrescribir.

#### ¿Cuándo elegís una interfaz y cuándo una clase abstracta?

Interfaz para una capacidad que comparten clases distintas; clase abstracta para una familia que comparte datos y código.

#### ¿Qué tiene que devolver `compareTo`?

Un número negativo si `this` va antes, 0 si son iguales y positivo si va después.

### Soluciones (docente)

Sale de `18-Java/15-Interfaces` (unidad 1). Se suma `Comparable`, que el capítulo original no tenía y que la rama 3 retoma con `Comparator` y lambdas.

## R02-N08 · Composición, agregación y delegación

```meta
tipo: tema
padre: R02-N07
precio: 10
criatura: troll
temas: poo.composicion
```

### Crónica

En el taller de armaduras, un aprendiz intenta que la clase `Caballero` herede de `Armadura`, de `Espada` y de `Caballo` a la vez. No compila, y aunque compilara, no tendría sentido: un caballero no **es** una armadura.

—Un caballero **tiene** una armadura —corrige {mentor}—. Y una espada. Y un caballo que, si el caballero cae, sigue existiendo. Eso es **composición** y **agregación**: construir cosas grandes con cosas chicas, en lugar de heredar de todo. Zed mira su ganzúa, que ahora tiene dos dientes, y piensa que él también está hecho de piezas.

### Objetivos

- Modelar la relación "tiene un" con atributos que son objetos.
- Distinguir composición (la parte vive y muere con el todo) de agregación (la parte existe por su cuenta).
- Delegar: que un objeto le pase el trabajo a sus partes.
- Saber cuándo conviene composición en lugar de herencia.

### Antes de empezar

- Interfaces: contratos.

### Explicación

#### "Tiene un": objetos dentro de objetos
Un atributo puede ser otro objeto:
```java
class Caballero {
    private final String nombre;
    private final Armadura armadura;     // tiene una armadura
    private Espada espada;               // tiene una espada (se puede cambiar)
    …
}
```

#### Composición
La parte **se crea dentro** del todo y no tiene sentido sin él: si el todo desaparece,
la parte también. El todo es su único dueño y no la comparte.
```java
class Caballero {
    private final Armadura armadura;

    public Caballero(String nombre) {
        this.nombre = nombre;
        this.armadura = new Armadura(50);    // nace con el caballero
    }
}
```

#### Agregación
La parte **existe por su cuenta** y el todo solo la usa: se crea afuera y se le pasa.
Puede compartirse o cambiarse, y sobrevive al todo.
```java
Caballo tormenta = new Caballo("Tormenta");
Caballero c = new Caballero("Baldo", tormenta);   // la recibe
c.montar(otroCaballo);                            // la puede cambiar
```
| | Composición | Agregación |
|---|---|---|
| Quién crea la parte | el todo | alguien de afuera |
| ¿Sobrevive al todo? | no | sí |
| ¿Se comparte? | no | puede |
| UML | rombo relleno ◆ | rombo vacío ◇ |
| Ejemplo | una factura y sus renglones | un equipo y sus jugadores |

#### Delegación
Cuando al todo le piden algo que en realidad hace una parte, **se lo pasa**:
```java
public int defensa() {
    return armadura.getProteccion();       // delega en la armadura
}
public int atacar() {
    return espada == null ? 1 : espada.danio();
}
```
Quien usa `Caballero` no necesita saber que la defensa viene de la armadura: solo
llama `defensa()`.

#### Composición en lugar de herencia
La herencia ata mucho: la subclase depende de todos los detalles del padre, y solo se
hereda de uno. Si la relación es "tiene un" (o "usa un"), va composición. Un ejemplo
clásico: en lugar de `class ArqueroConCaballo extends Arquero`, un `Arquero` que
**tiene** una `Montura` que puede ser `null` o cambiarse. Con herencia harían falta
clases para cada combinación; con composición, se combinan objetos.

#### Cuidado con las partes que se escapan
Si una clase devuelve su parte interna (un getter que devuelve la armadura o un
array), quien la recibe la puede modificar por fuera. Para la composición, conviene
devolver datos (`getProteccion()`) o una **copia**, no la parte original.

> **Si venís de C++.** En Java no hay objetos "por valor" dentro de otros: todo
> atributo de tipo clase es una referencia. La composición se garantiza por diseño (el
> todo crea la parte y no la entrega), no por la sintaxis.

### Código de ejemplo

```java
/*
 * Composición, agregación y delegación: el caballero y sus cosas.
 */
public class TallerArmaduras {
    public static void main(String[] args) {
        Caballo tormenta = new Caballo("Tormenta", 12);
        Caballo niebla = new Caballo("Niebla", 9);

        Caballero baldo = new Caballero("Baldo", tormenta);       // agregación: el caballo viene de afuera
        baldo.equipar(new Espada("Colmillo", 11));
        System.out.println(baldo);

        // Delegación: el caballero pasa el trabajo a sus partes
        System.out.println("Ataque: " + baldo.atacar());
        System.out.println("Defensa: " + baldo.defensa());
        System.out.println("Velocidad: " + baldo.velocidad());

        baldo.recibirGolpe(20);
        baldo.recibirGolpe(35);
        System.out.println("Después de dos golpes: " + baldo);

        // Agregación: el caballo se cambia y sigue existiendo por su cuenta
        baldo.montar(niebla);
        System.out.println("Cambia de caballo: " + baldo);
        System.out.println("Tormenta sigue en el establo: " + tormenta);

        // Sin espada: la delegación maneja la parte que falta
        Caballero recluta = new Caballero("Pip", null);
        System.out.println(recluta + " ataca con " + recluta.atacar() + " y corre a " + recluta.velocidad());
    }
}

class Caballero {
    private final String nombre;
    private final Armadura armadura;   // composición: nace y muere con el caballero
    private Espada espada;             // agregación: se equipa y se cambia
    private Caballo caballo;           // agregación: existe por su cuenta

    public Caballero(String nombre, Caballo caballo) {
        this.nombre = nombre;
        this.armadura = new Armadura(50);
        this.caballo = caballo;
    }

    public void equipar(Espada espada) {
        this.espada = espada;
    }

    public void montar(Caballo caballo) {
        this.caballo = caballo;
    }

    public int atacar() {
        return espada == null ? 1 : espada.danio();
    }

    public int defensa() {
        return armadura.getProteccion();
    }

    public int velocidad() {
        return caballo == null ? 3 : caballo.getVelocidad();
    }

    public void recibirGolpe(int fuerza) {
        armadura.absorber(fuerza);
    }

    @Override
    public String toString() {
        return nombre + " [" + armadura + ", " + (espada == null ? "sin espada" : espada)
                + ", " + (caballo == null ? "a pie" : "montando a " + caballo.getNombre()) + "]";
    }
}

class Armadura {
    private int proteccion;

    public Armadura(int proteccion) {
        this.proteccion = proteccion;
    }

    public int getProteccion() {
        return proteccion;
    }

    public void absorber(int golpe) {
        proteccion = Math.max(0, proteccion - golpe / 2);
    }

    @Override
    public String toString() {
        return "armadura " + proteccion;
    }
}

class Espada {
    private final String nombre;
    private final int danio;

    public Espada(String nombre, int danio) {
        this.nombre = nombre;
        this.danio = danio;
    }

    public int danio() {
        return danio;
    }

    @Override
    public String toString() {
        return "espada " + nombre;
    }
}

class Caballo {
    private final String nombre;
    private final int velocidad;

    public Caballo(String nombre, int velocidad) {
        this.nombre = nombre;
        this.velocidad = velocidad;
    }

    public String getNombre() {
        return nombre;
    }

    public int getVelocidad() {
        return velocidad;
    }

    @Override
    public String toString() {
        return nombre + " (velocidad " + velocidad + ")";
    }
}
```

### Salida esperada

```
Baldo [armadura 50, espada Colmillo, montando a Tormenta]
Ataque: 11
Defensa: 50
Velocidad: 12
Después de dos golpes: Baldo [armadura 23, espada Colmillo, montando a Tormenta]
Cambia de caballo: Baldo [armadura 23, espada Colmillo, montando a Niebla]
Tormenta sigue en el establo: Tormenta (velocidad 12)
Pip [armadura 50, sin espada, a pie] ataca con 1 y corre a 3
```

### ¿Para qué sirve?

Casi todo lo que modela un sistema real es composición: una `Factura` tiene `Renglones`, un `Pedido` tiene un `Cliente` y una `Direccion`, un `Auto` tiene un `Motor`. Pensar en qué partes tiene cada cosa, quién crea a quién y quién le pasa el trabajo a quién es la mitad del diseño orientado a objetos (y es lo que muestran los diagramas UML del nodo que viene).

### Errores habituales

**Ogro: herencia donde va composición.** `class Caballero extends Armadura` compila,
pero dice que un caballero *es* una armadura. Si la frase suena mal, es "tiene un".

**Troll: la parte `null`.** Si la espada es opcional y el método no lo contempla,
`espada.danio()` corta con `NullPointerException`. Manejá la ausencia al delegar.

**Troll: la parte que se escapa.** Un `getArmadura()` que devuelve el objeto interno
permite que cualquiera la cambie sin pasar por el caballero. Devolvé datos o copias.

**Ogro: la agregación compartida sin querer.** Si dos caballeros montan el mismo
`Caballo` y uno lo cansa, el otro también lo ve cansado. A veces es lo que se busca;
si no, cada uno necesita su propio objeto.

### Micro-misión R02-N08-P1 · Un caballero no es una armadura

```meta
lugar: El taller de armaduras
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: Tiene un | class Caballero { Armadura armadura; } · un atributo que es otro objeto · «tiene un», no «es un»
recompensa: xp 10, oro 10
```

#### Escena
En el taller de armaduras, un aprendiz intenta que `Caballero` herede de `Armadura`. —Un caballero no **es** una armadura —le dice la Maestra—. **Tiene** una.

#### Gheco sugiere
Cuando algo **tiene** otra cosa, la parte va como **atributo**: `Armadura armadura;`. Para usarla, se pasa por el atributo: `armadura.defensa`.

#### Desafío
Completá el tipo del atributo `armadura`.

#### Código inicial
```java
public class Taller {
    public static void main(String[] args) {
        Caballero c = new Caballero("Teo", new Armadura("de placas", 8));
        System.out.println(c.nombre + " lleva armadura " + c.armadura.tipo + " (defensa " + c.armadura.defensa + ")");
    }
}

class Armadura {
    String tipo;
    int defensa;

    Armadura(String tipo, int defensa) {
        this.tipo = tipo;
        this.defensa = defensa;
    }
}

class Caballero {
    String nombre;
    ___ armadura;

    Caballero(String nombre, Armadura armadura) {
        this.nombre = nombre;
        this.armadura = armadura;
    }
}
```

#### Salida esperada
```
Teo lleva armadura de placas (defensa 8)
```

#### Solución
```java
public class Taller {
    public static void main(String[] args) {
        Caballero c = new Caballero("Teo", new Armadura("de placas", 8));
        System.out.println(c.nombre + " lleva armadura " + c.armadura.tipo + " (defensa " + c.armadura.defensa + ")");
    }
}

class Armadura {
    String tipo;
    int defensa;

    Armadura(String tipo, int defensa) {
        this.tipo = tipo;
        this.defensa = defensa;
    }
}

class Caballero {
    String nombre;
    Armadura armadura;

    Caballero(String nombre, Armadura armadura) {
        this.nombre = nombre;
        this.armadura = armadura;
    }
}
```

#### Al superarla
Teo sale del taller con su armadura puesta, no convertido en una. —Ahora sí tiene sentido —dice el aprendiz, aliviado.

#### Imagen
- El taller de armaduras: yunques, chispas y armaduras colgadas.
- Teo (el recluta de la lanza) probándose una armadura de placas; la Maestra ajustándole una correa.

### Micro-misión R02-N08-P2 · Nace y muere con él

```meta
lugar: El taller de armaduras
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: Composición | la parte se crea ADENTRO del todo (new en el constructor) · nace y muere con él · nadie más la tiene
recompensa: xp 15, oro 15
```

#### Escena
Las armaduras del taller se forjan **a medida**: cada una se hace para un caballero y no le sirve a nadie más. Cuando el caballero se retira, su armadura se funde.

#### Gheco sugiere
En la **composición**, el todo crea su parte: el constructor del `Caballero` hace `this.armadura = new Armadura(...)`. Nadie de afuera tiene esa armadura: vive y muere con el caballero.

#### Desafío
Completá la línea que forja la armadura adentro del constructor, con la defensa que recibe.

#### Código inicial
```java
public class AMedida {
    public static void main(String[] args) {
        Caballero a = new Caballero("Teo", 8);
        Caballero b = new Caballero("Lía", 10);
        System.out.println(a.nombre + ": defensa " + a.armadura.defensa);
        System.out.println(b.nombre + ": defensa " + b.armadura.defensa);
        System.out.println("¿Comparten armadura? " + (a.armadura == b.armadura));
    }
}

class Armadura {
    int defensa;

    Armadura(int defensa) { this.defensa = defensa; }
}

class Caballero {
    String nombre;
    Armadura armadura;

    Caballero(String nombre, int defensa) {
        this.nombre = nombre;
        ___;
    }
}
```

#### Salida esperada
```
Teo: defensa 8
Lía: defensa 10
¿Comparten armadura? false
```

#### Solución
```java
public class AMedida {
    public static void main(String[] args) {
        Caballero a = new Caballero("Teo", 8);
        Caballero b = new Caballero("Lía", 10);
        System.out.println(a.nombre + ": defensa " + a.armadura.defensa);
        System.out.println(b.nombre + ": defensa " + b.armadura.defensa);
        System.out.println("¿Comparten armadura? " + (a.armadura == b.armadura));
    }
}

class Armadura {
    int defensa;

    Armadura(int defensa) { this.defensa = defensa; }
}

class Caballero {
    String nombre;
    Armadura armadura;

    Caballero(String nombre, int defensa) {
        this.nombre = nombre;
        this.armadura = new Armadura(defensa);
    }
}
```

#### Al superarla
Cada caballero con su armadura, forjada para él. «¿Comparten armadura? false.» —Como los sellos de la Aduana —dice Nadia—: cada uno, el suyo.

#### Imagen
- Dos armaduras forjándose a la vez en dos yunques, cada una con el nombre grabado: «Teo» y «Lía».
- Chispas doradas; Nadia observando con la libreta.

### Micro-misión R02-N08-P3 · El caballo sigue

```meta
lugar: Las caballerizas de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
criatura: troll
carta: Agregación | la parte existe por su cuenta y se pasa al todo · si el caballero cae (null), el caballo sigue existiendo
recompensa: xp 15, oro 15
```

#### Escena
En las caballerizas, el caballo **Rayo** ya existía antes de que Teo llegara. Teo lo monta, pero no es suyo para siempre. Un **troll** espera que, si Teo cae, Rayo desaparezca con él.

#### Gheco sugiere
En la **agregación**, la parte se crea **afuera** y se le pasa al todo: `new Caballero("Teo", rayo)`. Si después `teo = null`, el objeto caballo sigue vivo mientras alguien lo señale (la variable `rayo`).

#### Desafío
Completá el `new Caballero` pasándole el caballo que ya existe.

#### Código inicial
```java
public class Caballerizas {
    public static void main(String[] args) {
        Caballo rayo = new Caballo("Rayo");
        Caballero teo = new Caballero("Teo", ___);
        System.out.println(teo.nombre + " monta a " + teo.caballo.nombre);
        teo = null;
        System.out.println("Teo cayó. " + rayo.nombre + " sigue en las caballerizas");
    }
}

class Caballo {
    String nombre;

    Caballo(String nombre) { this.nombre = nombre; }
}

class Caballero {
    String nombre;
    Caballo caballo;

    Caballero(String nombre, Caballo caballo) {
        this.nombre = nombre;
        this.caballo = caballo;
    }
}
```

#### Salida esperada
```
Teo monta a Rayo
Teo cayó. Rayo sigue en las caballerizas
```

#### Solución
```java
public class Caballerizas {
    public static void main(String[] args) {
        Caballo rayo = new Caballo("Rayo");
        Caballero teo = new Caballero("Teo", rayo);
        System.out.println(teo.nombre + " monta a " + teo.caballo.nombre);
        teo = null;
        System.out.println("Teo cayó. " + rayo.nombre + " sigue en las caballerizas");
    }
}

class Caballo {
    String nombre;

    Caballo(String nombre) { this.nombre = nombre; }
}

class Caballero {
    String nombre;
    Caballo caballo;

    Caballero(String nombre, Caballo caballo) {
        this.nombre = nombre;
        this.caballo = caballo;
    }
}
```

#### Al superarla
Teo se cae del caballo en la práctica (de verdad), y Rayo sigue ahí, comiendo pasto. El troll se va sin nada.

#### Imagen
- Rayo, un caballo gris, comiendo tranquilo en las caballerizas.
- Teo sentado en el piso, riéndose; un troll yéndose decepcionado.

### Micro-misión R02-N08-P4 · Que lo haga la armadura

```meta
lugar: El taller de armaduras
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: Delegación | el todo le pasa el trabajo a su parte · int recibir(int golpe) { return armadura.absorber(golpe); }
recompensa: xp 15, oro 15
```

#### Escena
Cuando a un caballero le pegan, no es él quien frena el golpe: es su armadura. —El caballero **delega** —dice la Maestra—. No sabe de placas ni de remaches. Le pasa el golpe a quien sabe.

#### Gheco sugiere
**Delegar** es que un método del todo llame a un método de la parte: `return armadura.absorber(golpe);`. El caballero no repite la cuenta: la hace la armadura.

#### Desafío
Completá el `return` de `recibir`: que la armadura absorba el golpe.

#### Código inicial
```java
public class Delegar {
    public static void main(String[] args) {
        Caballero teo = new Caballero("Teo", new Armadura(8));
        System.out.println("Golpe de 20, daño: " + teo.recibir(20));
        System.out.println("Golpe de 5, daño: " + teo.recibir(5));
    }
}

class Armadura {
    int defensa;

    Armadura(int defensa) { this.defensa = defensa; }

    int absorber(int golpe) {
        return Math.max(0, golpe - defensa);
    }
}

class Caballero {
    String nombre;
    Armadura armadura;

    Caballero(String nombre, Armadura armadura) {
        this.nombre = nombre;
        this.armadura = armadura;
    }

    int recibir(int golpe) {
        return ___;
    }
}
```

#### Salida esperada
```
Golpe de 20, daño: 12
Golpe de 5, daño: 0
```

#### Solución
```java
public class Delegar {
    public static void main(String[] args) {
        Caballero teo = new Caballero("Teo", new Armadura(8));
        System.out.println("Golpe de 20, daño: " + teo.recibir(20));
        System.out.println("Golpe de 5, daño: " + teo.recibir(5));
    }
}

class Armadura {
    int defensa;

    Armadura(int defensa) { this.defensa = defensa; }

    int absorber(int golpe) {
        return Math.max(0, golpe - defensa);
    }
}

class Caballero {
    String nombre;
    Armadura armadura;

    Caballero(String nombre, Armadura armadura) {
        this.nombre = nombre;
        this.armadura = armadura;
    }

    int recibir(int golpe) {
        return armadura.absorber(golpe);
    }
}
```

#### Al superarla
Doce de daño en lugar de veinte, y el golpe chico ni se siente. Teo le agradece a su armadura con una palmadita.
En el archivo de la Academia, alguien escribió en la pizarra «arquero», «ARQERO» y «ARQUERO». Nadie sabe cuántos arqueros hay.

#### Imagen
- Una espada golpeando una armadura de placas: el golpe se frena en un destello.
- Teo dándole una palmadita a su armadura.

### Misión R02-N08-M1 · La factura y sus renglones

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Renglon` (descripción, cantidad, precio unitario, con `subtotal()`)
y una clase `Factura` que **compone** sus renglones: tiene un array interno de
`Renglon` y un método `agregar(String descripcion, int cantidad, double precio)` que
**crea** el renglón adentro (nadie de afuera los crea ni los recibe). La factura delega
en los renglones para calcular el total. Mostrá la factura completa con 2 decimales.

#### Criterio de aprobación

- Los renglones se crean dentro de la factura (composición).
- El total se calcula delegando en `subtotal()` de cada renglón.

#### Salida esperada

```
Factura para Posada La Taza
  Guiso          2 x   1200.00 =   2400.00
  Café           3 x    450.00 =   1350.00
  Habitación     1 x  18000.00 =  18000.00
  TOTAL                           21750.00
```

#### Solución de referencia

```java
// Mision 1 - La factura y sus renglones: composicion y delegacion.
import java.util.Locale;

public class Facturacion {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Factura f = new Factura("Posada La Taza", 5);
        f.agregar("Guiso", 2, 1200);
        f.agregar("Café", 3, 450);
        f.agregar("Habitación", 1, 18000);
        f.imprimir();
    }
}

class Factura {
    private final String cliente;
    private final Renglon[] renglones;
    private int cantidad;

    public Factura(String cliente, int maxRenglones) {
        this.cliente = cliente;
        this.renglones = new Renglon[maxRenglones];
    }

    public boolean agregar(String descripcion, int cantidad, double precio) {
        if (this.cantidad == renglones.length) {
            return false;
        }
        renglones[this.cantidad] = new Renglon(descripcion, cantidad, precio);
        this.cantidad++;
        return true;
    }

    public double total() {
        double total = 0;
        for (int i = 0; i < cantidad; i++) {
            total += renglones[i].subtotal();
        }
        return total;
    }

    public void imprimir() {
        System.out.println("Factura para " + cliente);
        for (int i = 0; i < cantidad; i++) {
            System.out.println("  " + renglones[i]);
        }
        System.out.printf("  %-31s%9.2f%n", "TOTAL", total());
    }
}

class Renglon {
    private final String descripcion;
    private final int cantidad;
    private final double precio;

    public Renglon(String descripcion, int cantidad, double precio) {
        this.descripcion = descripcion;
        this.cantidad = cantidad;
        this.precio = precio;
    }

    public double subtotal() {
        return cantidad * precio;
    }

    @Override
    public String toString() {
        return String.format("%-12s %3d x %9.2f = %9.2f", descripcion, cantidad, precio, subtotal());
    }
}
```

### Misión R02-N08-M2 · El equipo de la expedición

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Aventurero` (nombre, fuerza) y una clase `Expedicion` que
**agrega** aventureros: los recibe ya creados con `sumar(Aventurero a)` (hasta 4) y
los puede `quitar(String nombre)`. La expedición delega para calcular su fuerza total.
Creá cinco aventureros, armá **dos** expediciones que compartan a uno de ellos,
quitá a otro de una expedición y mostrá que el aventurero sigue existiendo.

#### Criterio de aprobación

- Los aventureros se crean afuera y se pasan (agregación).
- Un mismo aventurero está en dos expediciones.
- Quitar de una expedición no destruye al aventurero.

#### Salida esperada

```
Expedición Norte: Nadia (9), Baldo (14), Lía (7) | fuerza 30
Expedición Sur: Baldo (14), Pip (4), Nara (11) | fuerza 29
Sin Lía: Expedición Norte: Nadia (9), Baldo (14) | fuerza 23
Lía sigue existiendo: Lía (7)
```

#### Solución de referencia

```java
// Mision 2 - El equipo de la expedicion: agregacion.
public class Expediciones {
    public static void main(String[] args) {
        Aventurero nadia = new Aventurero("Nadia", 9);
        Aventurero baldo = new Aventurero("Baldo", 14);
        Aventurero lia = new Aventurero("Lía", 7);
        Aventurero pip = new Aventurero("Pip", 4);
        Aventurero nara = new Aventurero("Nara", 11);

        Expedicion norte = new Expedicion("Norte");
        norte.sumar(nadia);
        norte.sumar(baldo);
        norte.sumar(lia);
        Expedicion sur = new Expedicion("Sur");
        sur.sumar(baldo);
        sur.sumar(pip);
        sur.sumar(nara);
        System.out.println(norte);
        System.out.println(sur);

        norte.quitar("Lía");
        System.out.println("Sin Lía: " + norte);
        System.out.println("Lía sigue existiendo: " + lia);
    }
}

class Aventurero {
    private final String nombre;
    private final int fuerza;

    public Aventurero(String nombre, int fuerza) {
        this.nombre = nombre;
        this.fuerza = fuerza;
    }

    public String getNombre() {
        return nombre;
    }

    public int getFuerza() {
        return fuerza;
    }

    @Override
    public String toString() {
        return nombre + " (" + fuerza + ")";
    }
}

class Expedicion {
    private final String nombre;
    private final Aventurero[] miembros = new Aventurero[4];
    private int cantidad;

    public Expedicion(String nombre) {
        this.nombre = nombre;
    }

    public boolean sumar(Aventurero a) {
        if (cantidad == miembros.length || a == null) {
            return false;
        }
        miembros[cantidad++] = a;
        return true;
    }

    public boolean quitar(String nombre) {
        for (int i = 0; i < cantidad; i++) {
            if (miembros[i].getNombre().equals(nombre)) {
                miembros[i] = miembros[cantidad - 1];
                miembros[--cantidad] = null;
                return true;
            }
        }
        return false;
    }

    public int fuerzaTotal() {
        int total = 0;
        for (int i = 0; i < cantidad; i++) {
            total += miembros[i].getFuerza();
        }
        return total;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("Expedición " + nombre + ": ");
        for (int i = 0; i < cantidad; i++) {
            sb.append(i > 0 ? ", " : "").append(miembros[i]);
        }
        return sb.append(" | fuerza ").append(fuerzaTotal()).toString();
    }
}
```

### Misión R02-N08-M3 · El personaje con montura

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un arquero puede ir a pie o montar distintos animales. En lugar de crear
`ArqueroConCaballo`, `ArqueroConGrifo`… usá **composición con una interfaz**: una
interfaz `Montura` con `int velocidad()` y `String nombre()`, implementada por
`Caballo` y `Grifo`. La clase `Arquero` tiene una `Montura` que puede ser `null` (a
pie) y un método `cambiarMontura(Montura m)`. Su velocidad delega en la montura (a pie
es 3). Mostrá al arquero a pie, a caballo y en grifo.

#### Criterio de aprobación

- `Arquero` tiene una `Montura` (interfaz) en lugar de heredar.
- La velocidad delega y contempla la montura `null`.

#### Salida esperada

```
Lía a pie, velocidad 3
Lía en caballo, velocidad 12
Lía en grifo, velocidad 30
Lía a pie, velocidad 3
```

#### Solución de referencia

```java
// Mision 3 - El personaje con montura: composicion en lugar de herencia.
public class Monturas {
    public static void main(String[] args) {
        Arquero lia = new Arquero("Lía");
        System.out.println(lia);
        lia.cambiarMontura(new Caballo());
        System.out.println(lia);
        lia.cambiarMontura(new Grifo());
        System.out.println(lia);
        lia.cambiarMontura(null);
        System.out.println(lia);
    }
}

interface Montura {
    int velocidad();

    String nombre();
}

class Caballo implements Montura {
    @Override
    public int velocidad() {
        return 12;
    }

    @Override
    public String nombre() {
        return "caballo";
    }
}

class Grifo implements Montura {
    @Override
    public int velocidad() {
        return 30;
    }

    @Override
    public String nombre() {
        return "grifo";
    }
}

class Arquero {
    private final String nombre;
    private Montura montura;

    public Arquero(String nombre) {
        this.nombre = nombre;
    }

    public void cambiarMontura(Montura montura) {
        this.montura = montura;
    }

    public int velocidad() {
        return montura == null ? 3 : montura.velocidad();
    }

    @Override
    public String toString() {
        return nombre + " " + (montura == null ? "a pie" : "en " + montura.nombre()) + ", velocidad " + velocidad();
    }
}
```

### Encargo R02-N08-E1 · El auto del taller

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un taller registra autos: cada `Auto` (patente, modelo) **compone** un `Motor`
(cilindrada, horas de uso) que crea en su constructor, y **agrega** un `Duenio`
(nombre, teléfono) que puede cambiar si se vende. Métodos del auto: `usar(int horas)`
(delega en el motor), `necesitaService()` (el motor tiene más de 500 horas desde el
último service), `hacerService()` y `vender(Duenio nuevo)`. Mostrá el recorrido de un
auto: uso, service, venta.

#### Criterio de aprobación

- El motor lo crea el auto; el dueño viene de afuera y se cambia.
- `necesitaService` delega en el motor.

#### Salida esperada

```
AE123CD Sedán 1.6 (1600 cc, 320 h) de Marta Díaz | ¿service? false
AE123CD Sedán 1.6 (1600 cc, 570 h) de Marta Díaz | ¿service? true
Después del service: AE123CD Sedán 1.6 (1600 cc, 570 h) de Marta Díaz | ¿service? false
Vendido: AE123CD Sedán 1.6 (1600 cc, 570 h) de Juan Pérez
Marta sigue en el padrón: Marta Díaz (3804111222)
```

#### Solución de referencia

```java
// Encargo - El auto del taller: composicion (motor) y agregacion (duenio).
public class Taller {
    public static void main(String[] args) {
        Duenio marta = new Duenio("Marta Díaz", "3804111222");
        Auto auto = new Auto("AE123CD", "Sedán 1.6", 1600, marta);
        auto.usar(320);
        System.out.println(auto + " | ¿service? " + auto.necesitaService());
        auto.usar(250);
        System.out.println(auto + " | ¿service? " + auto.necesitaService());
        auto.hacerService();
        System.out.println("Después del service: " + auto + " | ¿service? " + auto.necesitaService());
        auto.vender(new Duenio("Juan Pérez", "3804999888"));
        System.out.println("Vendido: " + auto);
        System.out.println("Marta sigue en el padrón: " + marta);
    }
}

class Auto {
    private final String patente;
    private final String modelo;
    private final Motor motor;
    private Duenio duenio;

    public Auto(String patente, String modelo, int cilindrada, Duenio duenio) {
        this.patente = patente;
        this.modelo = modelo;
        this.motor = new Motor(cilindrada);
        this.duenio = duenio;
    }

    public void usar(int horas) {
        motor.sumarHoras(horas);
    }

    public boolean necesitaService() {
        return motor.horasDesdeService() > 500;
    }

    public void hacerService() {
        motor.registrarService();
    }

    public void vender(Duenio nuevo) {
        duenio = nuevo;
    }

    @Override
    public String toString() {
        return patente + " " + modelo + " (" + motor + ") de " + duenio.getNombre();
    }
}

class Motor {
    private final int cilindrada;
    private int horas;
    private int horasEnUltimoService;

    public Motor(int cilindrada) {
        this.cilindrada = cilindrada;
    }

    public void sumarHoras(int horas) {
        this.horas += horas;
    }

    public int horasDesdeService() {
        return horas - horasEnUltimoService;
    }

    public void registrarService() {
        horasEnUltimoService = horas;
    }

    @Override
    public String toString() {
        return cilindrada + " cc, " + horas + " h";
    }
}

class Duenio {
    private final String nombre;
    private final String telefono;

    public Duenio(String nombre, String telefono) {
        this.nombre = nombre;
        this.telefono = telefono;
    }

    public String getNombre() {
        return nombre;
    }

    @Override
    public String toString() {
        return nombre + " (" + telefono + ")";
    }
}
```

### Prueba del sello

#### ¿Qué relación expresa la composición y cuál la herencia?

La composición, "tiene un"; la herencia, "es un".

#### ¿Qué diferencia hay entre composición y agregación?

En la composición la parte la crea el todo y no sobrevive sin él; en la agregación la parte existe por su cuenta, viene de afuera y se puede compartir.

#### ¿Qué es delegar?

Que un objeto responda un mensaje pasándole el trabajo a una de sus partes.

#### ¿Por qué `ArqueroConCaballo extends Arquero` es un mal diseño?

Porque cada combinación necesitaría una clase nueva; con composición, el arquero tiene una montura que se cambia.

#### ¿Qué riesgo tiene un getter que devuelve una parte interna?

Que quien la recibe la modifique sin pasar por las reglas del objeto que la contiene.

### Soluciones (docente)

Sale de `18-Java/16-Composicion-Delegacion` (unidad 4). Corrige el detalle del original: el `Arma` que se creaba afuera y se pasaba a `equipar` es agregación, no composición.

## R02-N09 · enum y record

```meta
tipo: tema
padre: R02-N08
precio: 10
criatura: goblin
temas: prog.enums, poo.records
```

### Crónica

En el archivo de la Academia hay una pizarra con las clases de soldado permitidas: *INFANTE, ARQUERO, JINETE*. Alguien escribió abajo, con tiza, *arquero* en minúsculas, y un goblin *ARQERO*. Tres palabras para lo mismo, y el sistema ya no sabe cuántos arqueros hay.

—Cuando los valores posibles son una lista cerrada, no los escribas como texto: declaralos como **enum** —dice {mentor}—. Y cuando un objeto es solo un paquete de datos que no cambia, no escribas cincuenta líneas: usá un **record**.

### Objetivos

- Declarar un `enum` para un conjunto fijo de valores.
- Agregarle atributos, constructor y métodos a un `enum`.
- Usar `enum` en un `switch` y recorrer sus valores con `values()`.
- Declarar un `record` para objetos de datos inmutables y validarlos.

### Antes de empezar

- Composición, agregación y delegación.

### Explicación

#### `enum`: una lista cerrada de valores
```java
enum Clase {
    INFANTE, ARQUERO, JINETE
}

Clase c = Clase.ARQUERO;
if (c == Clase.ARQUERO) { … }       // los enum se comparan con == sin problema
```
Con un `enum`, un valor mal escrito **no compila** (`Clase.ARQERO` no existe), y no
hay forma de crear un valor nuevo por fuera. Son ideales para estados (`PENDIENTE`,
`APROBADO`), días, categorías, direcciones, rangos.

Métodos que ya trae todo `enum`:
```java
Clase.values();              // un array con todos: [INFANTE, ARQUERO, JINETE]
c.name();                    // "ARQUERO"
c.ordinal();                 // 1: su posición (mejor no depender de esto)
Clase.valueOf("JINETE");     // el valor a partir del texto (o IllegalArgumentException)
```

#### Un `enum` en un `switch`
```java
int costo = switch (c) {
    case INFANTE -> 10;
    case ARQUERO -> 15;
    case JINETE -> 30;
};
```
Dentro del `switch` se escribe el nombre solo (`INFANTE`, no `Clase.INFANTE`). Si el
`switch` es una expresión y cubre todos los valores, no hace falta `default`.

#### Un `enum` con datos y comportamiento
Cada valor de un `enum` es un **objeto**: puede tener atributos, un constructor y
métodos.
```java
enum Clase {
    INFANTE("espada", 10), ARQUERO("arco", 15), JINETE("lanza", 30);

    private final String arma;
    private final int costo;

    Clase(String arma, int costo) {        // el constructor es privado siempre
        this.arma = arma;
        this.costo = costo;
    }

    public String getArma() { return arma; }
    public int getCosto() { return costo; }
}
```
Así el dato vive **junto al valor**, y agregar una clase nueva es agregar una línea.

#### `record`: clases de datos en una línea
Muchas clases son solo **datos que no cambian**: un punto, una fecha, un registro de
una consulta. Escribirlas a mano pide atributos `private final`, constructor,
getters, `equals`, `hashCode` y `toString`. Un `record` (Java 16+) hace todo eso en una
línea:
```java
record Punto(int x, int y) { }

Punto p = new Punto(3, 4);
p.x();                        // 3 (los "getters" se llaman como el campo, sin get)
p.equals(new Punto(3, 4));    // true: compara los datos
System.out.println(p);        // Punto[x=3, y=4]
```
Un `record` es **inmutable** (no hay setters) y no puede heredar de otra clase (sí
implementar interfaces).

#### Validar en un `record`
El *constructor compacto* valida sin repetir las asignaciones:
```java
record Punto(int x, int y) {
    Punto {
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException("coordenadas negativas");
        }
    }

    double distanciaAlOrigen() {          // puede tener métodos
        return Math.sqrt(x * x + y * y);
    }
}
```

> **Si venís de C.** Un `enum` de Java no es un número disfrazado: es un tipo con sus
> propios objetos, que puede tener datos y métodos.
>
> **Si venís de Python.** `enum` se parece a `Enum` del módulo `enum`, y `record` a una
> `dataclass(frozen=True)`.

### Código de ejemplo

```java
/*
 * enum y record: el archivo de la Academia.
 */
public class ArchivoAcademia {
    public static void main(String[] args) {
        // Recorrer los valores de un enum con sus datos
        for (Clase c : Clase.values()) {
            System.out.printf("%-8s arma: %-6s costo: %d%n", c, c.getArma(), c.getCosto());
        }

        // Un enum en un switch
        Clase elegida = Clase.valueOf("ARQUERO");
        String consejo = switch (elegida) {
            case INFANTE -> "quedate adelante";
            case ARQUERO -> "buscá altura";
            case JINETE -> "cargá por los flancos";
        };
        System.out.println(elegida + ": " + consejo);
        System.out.println("¿Es arquero? " + (elegida == Clase.ARQUERO));

        // Un texto que no es un valor del enum
        try {
            Clase.valueOf("ARQERO");
        } catch (IllegalArgumentException e) {
            System.out.println("ARQERO no es una clase válida");
        }

        // record: datos inmutables con equals, hashCode y toString gratis
        Recluta r1 = new Recluta("Pip", Clase.INFANTE, 3);
        Recluta r2 = new Recluta("Pip", Clase.INFANTE, 3);
        System.out.println(r1);
        System.out.println("Nombre: " + r1.nombre() + ", clase: " + r1.clase());
        System.out.println("r1.equals(r2): " + r1.equals(r2) + ", r1 == r2: " + (r1 == r2));
        System.out.println("Costo de equipar a Pip: " + r1.costoTotal());

        // Validación en el constructor compacto
        try {
            new Recluta("Nara", Clase.JINETE, -2);
        } catch (IllegalArgumentException e) {
            System.out.println("Recluta rechazado: " + e.getMessage());
        }
    }
}

enum Clase {
    INFANTE("espada", 10), ARQUERO("arco", 15), JINETE("lanza", 30);

    private final String arma;
    private final int costo;

    Clase(String arma, int costo) {
        this.arma = arma;
        this.costo = costo;
    }

    public String getArma() {
        return arma;
    }

    public int getCosto() {
        return costo;
    }
}

record Recluta(String nombre, Clase clase, int anios) {
    Recluta {
        if (nombre == null || nombre.isBlank()) {
            throw new IllegalArgumentException("falta el nombre");
        }
        if (anios < 0) {
            throw new IllegalArgumentException("los años de servicio no pueden ser negativos");
        }
    }

    int costoTotal() {
        return clase.getCosto() + anios * 2;
    }
}
```

### Salida esperada

```
INFANTE  arma: espada costo: 10
ARQUERO  arma: arco   costo: 15
JINETE   arma: lanza  costo: 30
ARQUERO: buscá altura
¿Es arquero? true
ARQERO no es una clase válida
Recluta[nombre=Pip, clase=INFANTE, anios=3]
Nombre: Pip, clase: INFANTE
r1.equals(r2): true, r1 == r2: false
Costo de equipar a Pip: 16
Recluta rechazado: los años de servicio no pueden ser negativos
```

### ¿Para qué sirve?

Los `enum` están en todo sistema: el estado de un pedido, el tipo de documento, los roles de usuario, los días de la semana. Evitan los errores de escribir mal un texto y juntan en un lugar el dato de cada valor. Los `record` son la forma moderna de escribir los objetos que solo transportan datos: los resultados de una consulta, los mensajes entre capas (los DTO que vas a ver en la Senda de Spring), las coordenadas de un juego.

### Errores habituales

**Esqueleto: un valor que no existe.** `Clase.ARQERO` no compila (`cannot find
symbol`), que es justamente la ventaja del `enum`.

**Goblin: `valueOf` con un texto inválido.** `IllegalArgumentException: No enum
constant Clase.arquero`: distingue mayúsculas. Pasalo a mayúsculas antes, o validá.

**Slime: el prefijo en el `switch`.** `case Clase.INFANTE ->` no compila en Java 17:
dentro del `switch` va el nombre solo.

**Esqueleto: buscar el getter con `get`.** En un `record` es `r.nombre()`, no
`r.getNombre()`.

**Slime: querer cambiar un `record`.** No tiene setters ni se puede asignar un campo:
se crea uno nuevo con los datos cambiados.

### Micro-misión R02-N09-P1 · Tres palabras para lo mismo

```meta
lugar: El archivo de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
criatura: goblin
carta: enum | enum Clase { INFANTE, ARQUERO, JINETE } · una lista cerrada de valores · Clase.values() los recorre
recompensa: xp 10, oro 10
```

#### Escena
En la pizarra del archivo dice «arquero», «ARQERO» y «ARQUERO». Un **goblin** escribió el del medio. —Cuando los valores posibles son una lista cerrada —dice la Maestra—, no los escribas como texto. Declaralos.

#### Gheco sugiere
Un `enum` es un tipo con una lista **cerrada** de valores: `enum Clase { INFANTE, ARQUERO, JINETE }`. No hay forma de escribir `ARQERO`: no compila. `Clase.values()` devuelve todos, en orden.

#### Desafío
Recorré todos los valores del enum con el método que los devuelve.

#### Código inicial
```java
public class Pizarra {
    public static void main(String[] args) {
        Clase deMira = Clase.ARQUERO;
        System.out.println("Mira es " + deMira);
        for (Clase c : Clase.___()) {
            System.out.println("- " + c);
        }
    }
}

enum Clase {
    INFANTE, ARQUERO, JINETE
}
```

#### Salida esperada
```
Mira es ARQUERO
- INFANTE
- ARQUERO
- JINETE
```

#### Solución
```java
public class Pizarra {
    public static void main(String[] args) {
        Clase deMira = Clase.ARQUERO;
        System.out.println("Mira es " + deMira);
        for (Clase c : Clase.values()) {
            System.out.println("- " + c);
        }
    }
}

enum Clase {
    INFANTE, ARQUERO, JINETE
}
```

#### Al superarla
Tres clases, escritas una sola vez. La Maestra borra la pizarra entera y el goblin se queda sin tiza.

#### Imagen
- Una pizarra con «arquero», «ARQERO» y «ARQUERO» tachados y, encima, un cartel de bronce: INFANTE · ARQUERO · JINETE.
- Un goblin con una tiza rota en la mano.

### Micro-misión R02-N09-P2 · La paga de cada clase

```meta
lugar: El archivo de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: enum con datos | INFANTE(10), ARQUERO(12) · un atributo final y un constructor · cada valor lleva lo suyo
recompensa: xp 15, oro 15
```

#### Escena
Cada clase de soldado cobra distinto. En lugar de una tabla aparte, la Maestra quiere que **cada valor del enum lleve su paga**.

#### Gheco sugiere
Un `enum` puede tener atributos, constructor y métodos: `INFANTE(10)` llama al constructor con 10. El constructor guarda el dato: `this.paga = paga;`.

#### Desafío
Completá el constructor del enum: guardá la paga.

#### Código inicial
```java
public class Paga {
    public static void main(String[] args) {
        for (Clase c : Clase.values()) {
            System.out.println(c + ": " + c.getPaga() + " denarios");
        }
    }
}

enum Clase {
    INFANTE(10), ARQUERO(12), JINETE(20);

    private final int paga;

    Clase(int paga) {
        ___;
    }

    int getPaga() {
        return paga;
    }
}
```

#### Salida esperada
```
INFANTE: 10 denarios
ARQUERO: 12 denarios
JINETE: 20 denarios
```

#### Solución
```java
public class Paga {
    public static void main(String[] args) {
        for (Clase c : Clase.values()) {
            System.out.println(c + ": " + c.getPaga() + " denarios");
        }
    }
}

enum Clase {
    INFANTE(10), ARQUERO(12), JINETE(20);

    private final int paga;

    Clase(int paga) {
        this.paga = paga;
    }

    int getPaga() {
        return paga;
    }
}
```

#### Al superarla
Cada clase con su paga, sin tablas sueltas. —Los jinetes cobran el doble —protesta Teo—. —Tienen que alimentar al caballo —le contesta Nadia.

#### Imagen
- Tres placas de bronce: INFANTE 10, ARQUERO 12, JINETE 20, con monedas apiladas al lado.
- Teo protestando; Nadia señalando a Rayo, el caballo.

### Micro-misión R02-N09-P3 · Una orden para cada clase

```meta
lugar: El patio de armas de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: enum en switch | switch (c) { case INFANTE -> …; case ARQUERO -> …; } · sin escribir Clase. adelante · con los tres casos no hace falta default
recompensa: xp 15, oro 15
```

#### Escena
En el patio, la Maestra da órdenes distintas según la clase. Zed le arma la tabla de órdenes con un `switch`.

#### Gheco sugiere
Un `enum` va perfecto en un `switch`: cada `case` es un valor (`case ARQUERO ->`). Si el `switch` devuelve un valor y cubre **todos** los valores del enum, no hace falta `default`.

#### Desafío
Completá el caso que falta: los arqueros «disparan».

#### Código inicial
```java
public class Ordenes {
    static String orden(Clase c) {
        return switch (c) {
            case INFANTE -> "avanzan";
            case ___ -> "disparan";
            case JINETE -> "flanquean";
        };
    }

    public static void main(String[] args) {
        for (Clase c : Clase.values()) {
            System.out.println(c + ": " + orden(c));
        }
    }
}

enum Clase {
    INFANTE, ARQUERO, JINETE
}
```

#### Salida esperada
```
INFANTE: avanzan
ARQUERO: disparan
JINETE: flanquean
```

#### Solución
```java
public class Ordenes {
    static String orden(Clase c) {
        return switch (c) {
            case INFANTE -> "avanzan";
            case ARQUERO -> "disparan";
            case JINETE -> "flanquean";
        };
    }

    public static void main(String[] args) {
        for (Clase c : Clase.values()) {
            System.out.println(c + ": " + orden(c));
        }
    }
}

enum Clase {
    INFANTE, ARQUERO, JINETE
}
```

#### Al superarla
Las tres órdenes, sin una sola palabra mal escrita. Si mañana se agrega una clase nueva, el compilador va a avisar que falta su caso.

#### Imagen
- El patio de armas: infantes avanzando, arqueros disparando y jinetes rodeando por el costado.
- La Maestra con un cartel de órdenes; Zed a su lado.

### Micro-misión R02-N09-P4 · La ficha que no cambia

```meta
lugar: El archivo de la Academia
personajes: Zed, Gheco, Nadia, la Maestra de Moldes
carta: record | record Recluta(String nombre, Clase clase) {} · constructor, getters nombre(), equals y toString hechos · no se puede cambiar
recompensa: xp 15, oro 15
```

#### Escena
Las fichas de los reclutas son solo datos: nombre y clase. Escribirlas como clase lleva cincuenta líneas. —Para un paquete de datos que no cambia —dice la Maestra—, un **record**.

#### Gheco sugiere
`record Recluta(String nombre, Clase clase) {}` crea el constructor, un método para leer cada dato (`r.nombre()`, sin `get`), `equals` y `toString`, y no deja cambiar nada.

#### Desafío
Completá el método que lee el nombre del recluta.

#### Código inicial
```java
public class Fichas {
    public static void main(String[] args) {
        Recluta a = new Recluta("Mira", Clase.ARQUERO);
        Recluta b = new Recluta("Mira", Clase.ARQUERO);
        System.out.println(a);
        System.out.println("Nombre: " + a.___());
        System.out.println("Iguales: " + a.equals(b));
    }
}

enum Clase {
    INFANTE, ARQUERO, JINETE
}

record Recluta(String nombre, Clase clase) {
}
```

#### Salida esperada
```
Recluta[nombre=Mira, clase=ARQUERO]
Nombre: Mira
Iguales: true
```

#### Solución
```java
public class Fichas {
    public static void main(String[] args) {
        Recluta a = new Recluta("Mira", Clase.ARQUERO);
        Recluta b = new Recluta("Mira", Clase.ARQUERO);
        System.out.println(a);
        System.out.println("Nombre: " + a.nombre());
        System.out.println("Iguales: " + a.equals(b));
    }
}

enum Clase {
    INFANTE, ARQUERO, JINETE
}

record Recluta(String nombre, Clase clase) {
}
```

#### Al superarla
Una línea en lugar de cincuenta, con `toString` y `equals` incluidos. La Maestra archiva las fichas.
Esa tarde, Kaffa los cita en la biblioteca. Desenrolla un plano lleno de cajas y flechas, sin una sola línea de código.

#### Imagen
- Una ficha de bronce que se escribe sola: «Recluta[nombre=Mira, clase=ARQUERO]».
- Al fondo, la puerta de la biblioteca de la Academia, con Kaffa esperando con un plano enrollado.

### Misión R02-N09-M1 · Los días del mercado

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Declará un `enum Dia` con los siete días. Agregale un método `boolean
esFinDeSemana()` y otro `Dia siguiente()` (el domingo sigue al lunes: usá `values()` y
`ordinal()`). Pedí un día por teclado (en cualquier combinación de mayúsculas),
convertilo con `valueOf` y mostrá si es fin de semana, cuál es el siguiente y, con un
`switch`, qué se vende ese día en el mercado (inventá: pescado los viernes, etc.).
Si el texto no es un día, avisá.

#### Criterio de aprobación

- `Dia` es un `enum` con métodos.
- Maneja el texto inválido.
- Usa un `switch` sobre el `enum`.

#### Entrada de ejemplo

```
viernes
```

#### Salida esperada

```
Día: 
VIERNES es día hábil
Mañana es SABADO
En el mercado hoy: pescado
```

#### Solución de referencia

```java
// Mision 1 - Los dias del mercado: enum con metodos, valueOf y switch.
import java.util.Scanner;

public class Mercado {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        System.out.print("Día: ");
        String texto = teclado.nextLine().trim().toUpperCase();
        System.out.println();
        Dia dia;
        try {
            dia = Dia.valueOf(texto);
        } catch (IllegalArgumentException e) {
            System.out.println(texto + " no es un día");
            return;
        }
        System.out.println(dia + (dia.esFinDeSemana() ? " es fin de semana" : " es día hábil"));
        System.out.println("Mañana es " + dia.siguiente());
        String puesto = switch (dia) {
            case LUNES, MIERCOLES -> "verduras";
            case MARTES, JUEVES -> "telas";
            case VIERNES -> "pescado";
            case SABADO -> "feria de artesanos";
            case DOMINGO -> "cerrado";
        };
        System.out.println("En el mercado hoy: " + puesto);
    }
}

enum Dia {
    LUNES, MARTES, MIERCOLES, JUEVES, VIERNES, SABADO, DOMINGO;

    public boolean esFinDeSemana() {
        return this == SABADO || this == DOMINGO;
    }

    public Dia siguiente() {
        Dia[] todos = values();
        return todos[(ordinal() + 1) % todos.length];
    }
}
```

#### Pruebas

##### Domingo
```entrada
domingo
```
```salida
Día:
DOMINGO es fin de semana
Mañana es LUNES
En el mercado hoy: cerrado
```

##### Mayúsculas mezcladas
```entrada
LuNeS
```
```salida
Día:
LUNES es día hábil
Mañana es MARTES
En el mercado hoy: verduras
```

##### No es un día
```entrada
feriado
```
```salida
Día:
FERIADO no es un día
```

### Misión R02-N09-M2 · Los pedidos de la herrería

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un pedido pasa por estados: `PENDIENTE → EN_FORJA → TERMINADO → ENTREGADO`, y en
cualquier momento antes de entregarse puede quedar `CANCELADO`. Declará un `enum
Estado` con un atributo que diga el texto para mostrar y un método `boolean
puedePasarA(Estado otro)` con esas reglas. Una clase `Pedido` (número, estado) tiene
un método `cambiarEstado(Estado nuevo)` que solo lo cambia si está permitido. Mostrá
un recorrido con cambios válidos e inválidos.

#### Criterio de aprobación

- Las reglas de transición están en el `enum`.
- `Pedido` rechaza los cambios no permitidos.

#### Salida esperada

```
Pedido 101 (pendiente)
A terminado: no permitido -> Pedido 101 (pendiente)
A en la forja: ok -> Pedido 101 (en la forja)
A terminado: ok -> Pedido 101 (terminado)
A cancelado: ok -> Pedido 101 (cancelado)
A entregado: no permitido -> Pedido 101 (cancelado)
A cancelado: no permitido -> Pedido 101 (cancelado)
```

#### Solución de referencia

```java
// Mision 2 - Los pedidos de la herreria: enum con atributos y reglas de transicion.
public class Herreria {
    public static void main(String[] args) {
        Pedido p = new Pedido(101);
        System.out.println(p);
        Estado[] intentos = {Estado.TERMINADO, Estado.EN_FORJA, Estado.TERMINADO, Estado.CANCELADO, Estado.ENTREGADO, Estado.CANCELADO};
        for (Estado e : intentos) {
            boolean ok = p.cambiarEstado(e);
            System.out.println("A " + e.getTexto() + ": " + (ok ? "ok" : "no permitido") + " -> " + p);
        }
    }
}

enum Estado {
    PENDIENTE("pendiente"), EN_FORJA("en la forja"), TERMINADO("terminado"), ENTREGADO("entregado"), CANCELADO("cancelado");

    private final String texto;

    Estado(String texto) {
        this.texto = texto;
    }

    public String getTexto() {
        return texto;
    }

    public boolean puedePasarA(Estado otro) {
        if (otro == CANCELADO) {
            return this != ENTREGADO && this != CANCELADO;
        }
        return switch (this) {
            case PENDIENTE -> otro == EN_FORJA;
            case EN_FORJA -> otro == TERMINADO;
            case TERMINADO -> otro == ENTREGADO;
            case ENTREGADO, CANCELADO -> false;
        };
    }
}

class Pedido {
    private final int numero;
    private Estado estado = Estado.PENDIENTE;

    public Pedido(int numero) {
        this.numero = numero;
    }

    public boolean cambiarEstado(Estado nuevo) {
        if (!estado.puedePasarA(nuevo)) {
            return false;
        }
        estado = nuevo;
        return true;
    }

    @Override
    public String toString() {
        return "Pedido " + numero + " (" + estado.getTexto() + ")";
    }
}
```

### Misión R02-N09-M3 · Las coordenadas del mapa

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Declará un `record Coordenada(int fila, int columna)` que rechace valores negativos
en su constructor compacto y tenga dos métodos: `Coordenada mover(Direccion d)` (que
devuelve una coordenada **nueva**) y `int distanciaA(Coordenada otra)` (distancia
"Manhattan": la suma de las diferencias absolutas). `Direccion` es un `enum` con
`NORTE, SUR, ESTE, OESTE`, cada una con su desplazamiento de fila y columna como
atributos. Partí de (5, 5), seguí el camino `N, N, E, E, E, S` y mostrá cada paso y la
distancia al punto de partida.

#### Criterio de aprobación

- `Coordenada` es un `record` validado; mover devuelve un record nuevo.
- `Direccion` es un `enum` con atributos.

#### Salida esperada

```
NORTE -> Coordenada[fila=4, columna=5]
NORTE -> Coordenada[fila=3, columna=5]
ESTE -> Coordenada[fila=3, columna=6]
ESTE -> Coordenada[fila=3, columna=7]
ESTE -> Coordenada[fila=3, columna=8]
SUR -> Coordenada[fila=4, columna=8]
Distancia al inicio: 4
El inicio no cambió: Coordenada[fila=5, columna=5]
No se puede salir del mapa: coordenada negativa (0, -1)
```

#### Solución de referencia

```java
// Mision 3 - Las coordenadas del mapa: record inmutable y enum con atributos.
public class Camino {
    public static void main(String[] args) {
        Coordenada inicio = new Coordenada(5, 5);
        Coordenada actual = inicio;
        Direccion[] pasos = {Direccion.NORTE, Direccion.NORTE, Direccion.ESTE, Direccion.ESTE, Direccion.ESTE, Direccion.SUR};
        for (Direccion d : pasos) {
            actual = actual.mover(d);
            System.out.println(d + " -> " + actual);
        }
        System.out.println("Distancia al inicio: " + actual.distanciaA(inicio));
        System.out.println("El inicio no cambió: " + inicio);
        try {
            new Coordenada(0, 0).mover(Direccion.OESTE);
        } catch (IllegalArgumentException e) {
            System.out.println("No se puede salir del mapa: " + e.getMessage());
        }
    }
}

enum Direccion {
    NORTE(-1, 0), SUR(1, 0), ESTE(0, 1), OESTE(0, -1);

    private final int dFila;
    private final int dColumna;

    Direccion(int dFila, int dColumna) {
        this.dFila = dFila;
        this.dColumna = dColumna;
    }

    public int getDFila() {
        return dFila;
    }

    public int getDColumna() {
        return dColumna;
    }
}

record Coordenada(int fila, int columna) {
    Coordenada {
        if (fila < 0 || columna < 0) {
            throw new IllegalArgumentException("coordenada negativa (" + fila + ", " + columna + ")");
        }
    }

    Coordenada mover(Direccion d) {
        return new Coordenada(fila + d.getDFila(), columna + d.getDColumna());
    }

    int distanciaA(Coordenada otra) {
        return Math.abs(fila - otra.fila) + Math.abs(columna - otra.columna);
    }
}
```

### Encargo R02-N09-E1 · Los planes del gimnasio

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un gimnasio tiene planes `BASICO`, `PLUS` y `TOTAL`, cada uno con su cuota mensual y
la cantidad de clases por semana (el `TOTAL` no tiene límite: guardá -1 y mostralo
como "libre"). Declaralos como `enum` con atributos. Los socios son un `record Socio(String
nombre, Plan plan, int mesesPagos)` con un método que calcula lo pagado. Mostrá la
lista de planes y el total que pagó cada socio de un array de cuatro.

#### Criterio de aprobación

- El `enum` tiene atributos y un método para mostrar las clases.
- `Socio` es un `record` con un método propio.

#### Salida esperada

```
BASICO: $18000 por mes, 2 clases por semana
PLUS: $25000 por mes, 4 clases por semana
TOTAL: $34000 por mes, clases libres
Marta (BASICO) pagó $108000
Juan (TOTAL) pagó $102000
Ana (PLUS) pagó $300000
Leo (PLUS) pagó $25000
```

#### Solución de referencia

```java
// Encargo - Los planes del gimnasio: enum con datos y record con un metodo.
public class Gimnasio {
    public static void main(String[] args) {
        for (Plan p : Plan.values()) {
            System.out.println(p + ": $" + p.getCuota() + " por mes, " + p.clasesTexto());
        }
        Socio[] socios = {
            new Socio("Marta", Plan.BASICO, 6),
            new Socio("Juan", Plan.TOTAL, 3),
            new Socio("Ana", Plan.PLUS, 12),
            new Socio("Leo", Plan.PLUS, 1),
        };
        for (Socio s : socios) {
            System.out.println(s.nombre() + " (" + s.plan() + ") pagó $" + s.totalPagado());
        }
    }
}

enum Plan {
    BASICO(18_000, 2), PLUS(25_000, 4), TOTAL(34_000, -1);

    private final int cuota;
    private final int clasesPorSemana;

    Plan(int cuota, int clasesPorSemana) {
        this.cuota = cuota;
        this.clasesPorSemana = clasesPorSemana;
    }

    public int getCuota() {
        return cuota;
    }

    public String clasesTexto() {
        return clasesPorSemana < 0 ? "clases libres" : clasesPorSemana + " clases por semana";
    }
}

record Socio(String nombre, Plan plan, int mesesPagos) {
    int totalPagado() {
        return plan.getCuota() * mesesPagos;
    }
}
```

### Prueba del sello

#### ¿Qué ventaja tiene un `enum` sobre guardar el valor como texto?

Un valor mal escrito no compila, no se pueden inventar valores nuevos y cada valor puede traer sus datos y métodos.

#### ¿Qué devuelve `Clase.values()`?

Un array con todos los valores del `enum`, en el orden en que se declararon.

#### ¿Qué te da un `record` sin escribirlo?

Atributos `private final`, constructor, métodos de acceso (`x()`), `equals`, `hashCode` y `toString`.

#### ¿Cómo se valida en un `record`?

En el constructor compacto: `NombreDelRecord { … }`, sin repetir las asignaciones.

#### ¿Se puede cambiar un campo de un `record` después de crearlo?

No: es inmutable. Se crea uno nuevo con los datos cambiados.

### Soluciones (docente)

Nodo nuevo (el 17 del índice de `18-Java` estaba por crear). `record` es de Java 16+ y el curso pide Java 17.

## R02-N10 · Diagramas UML

```meta
tipo: tema
padre: R02-N09
precio: 10
criatura: ogre
temas: diseno.uml
```

### Crónica

En la biblioteca de la Academia, {mentor} desenrolla uno de sus planos. No hay código en él: hay cajas, flechas y rombos. —Antes de levantar un edificio, lo dibujo —dice—. Así lo discuto, lo corrijo y lo explico sin escribir una línea.

—Estos dibujos tienen un idioma común, Zed: el **UML**. Cualquier arquitecta del Imperio los lee igual. Aprendé a leerlos y a dibujarlos: en la facultad y en las empresas te los van a pedir. Nadia ya está copiando las flechas en su libreta.

### Objetivos

- Leer y dibujar diagramas de clases: atributos, métodos, visibilidad y relaciones.
- Distinguir asociación, agregación, composición, herencia, realización y dependencia.
- Indicar multiplicidades.
- Leer y dibujar diagramas de secuencia (interacción entre objetos).
- Pasar de un diagrama a código y de código a un diagrama.

### Antes de empezar

- Todas las relaciones de la rama: herencia, interfaces, composición y agregación.

### Explicación

#### La caja de una clase
Una clase se dibuja como una caja con tres partes: **nombre**, **atributos** y
**métodos**. Cada miembro lleva su visibilidad:

| Símbolo | Visibilidad |
|---|---|
| `+` | `public` |
| `-` | `private` |
| `#` | `protected` |
| `~` | sin modificador (paquete) |

```
┌──────────────────────────┐
│        Caballero         │
├──────────────────────────┤
│ - nombre : String        │
│ - vida : int             │
├──────────────────────────┤
│ + atacar() : int         │
│ + recibirGolpe(f : int)  │
└──────────────────────────┘
```
Los tipos van después de dos puntos. Los miembros `static` se subrayan y las clases y
métodos abstractos van en *cursiva* (o con `{abstract}`).

#### Las relaciones
| Relación | Dibujo | Significa | En Java |
|---|---|---|---|
| Herencia (generalización) | línea con triángulo vacío ▷ hacia el padre | "es un" | `extends` |
| Realización | línea punteada con triángulo vacío hacia la interfaz | "implementa" | `implements` |
| Asociación | línea simple (con flecha si se navega en un sentido) | "conoce a" / "usa" | un atributo de ese tipo |
| Agregación | línea con rombo vacío ◇ del lado del todo | "tiene un" (la parte vive sola) | atributo que viene de afuera |
| Composición | línea con rombo lleno ◆ del lado del todo | "tiene un" (la parte muere con el todo) | atributo creado adentro |
| Dependencia | flecha punteada | "usa temporalmente" | un parámetro o una variable local |

#### Multiplicidad
En los extremos de una asociación se indica **cuántos**: `1` (exactamente uno),
`0..1` (cero o uno), `*` o `0..*` (muchos), `1..*` (al menos uno). Por ejemplo, entre
`Factura` y `Renglon`: una factura tiene `1..*` renglones y cada renglón pertenece a
`1` factura.

#### Diagramas en texto: Mermaid
Dibujar a mano es lento de corregir. **Mermaid** es un formato de texto que se
convierte en diagrama: lo muestran GitHub, GitLab, muchos editores y la página
[mermaid.live](https://mermaid.live). Un diagrama de clases:
```
classDiagram
    class Personaje {
        <<abstract>>
        -String nombre
        #int vida
        +atacar() int*
    }
    class Guerrera {
        -int fuerza
        +atacar() int
    }
    class Curador {
        <<interface>>
        +curar(int vida) int
    }
    Personaje <|-- Guerrera
    Curador <|.. Clerigo
    Caballero *-- "1" Armadura : compone
    Caballero o-- "0..1" Caballo : monta
    Factura "1" *-- "1..*" Renglon
```
| Mermaid | Relación |
|---|---|
| `A <\|-- B` | B hereda de A |
| `A <\|.. B` | B implementa A |
| `A *-- B` | A se compone de B |
| `A o-- B` | A agrega a B |
| `A --> B` | A se asocia con B |
| `A ..> B` | A depende de B |

#### El diagrama de secuencia
Muestra **quién le manda qué mensaje a quién, en qué orden**. Cada objeto tiene una
línea de vida vertical y los mensajes son flechas horizontales, de arriba hacia abajo
en el tiempo:
```
sequenceDiagram
    participant M as main
    participant C as Caballero
    participant A as Armadura
    M->>C: recibirGolpe(20)
    C->>A: absorber(20)
    A-->>C: (proteccion baja)
    M->>C: defensa()
    C->>A: getProteccion()
    A-->>C: 40
    C-->>M: 40
```
Las flechas llenas (`->>`) son llamadas y las punteadas (`-->>`), respuestas. Sirve
para ver la **delegación**: el `main` le habla al caballero, y el caballero a su
armadura.

#### Del diagrama al código (y al revés)
- Cada caja es una clase; cada `-atributo : Tipo`, un `private Tipo atributo;`.
- Una flecha de herencia es un `extends`; una de realización, un `implements`.
- Un rombo lleno: el todo crea la parte en su constructor. Uno vacío: la recibe.
- Una multiplicidad `*` es un array (o, en la rama siguiente, una lista).

> **En la facultad.** La unidad 1 de *Paradigmas y Lenguajes III* pide diagramas de
> clases y de interacción. Mermaid sirve para practicar y entregar; en un examen se
> dibujan a mano con los mismos símbolos.

### Código de ejemplo

Este código corresponde al diagrama de clases de la explicación (la parte de
`Personaje`, `Guerrera`, `Curador` y `Clerigo`). Comparalos línea por línea.

```java
/*
 * Del diagrama al código: Personaje, Guerrera, Curador y Clerigo.
 */
public class DelDiagramaAlCodigo {
    public static void main(String[] args) {
        Personaje nara = new Guerrera("Nara", 45, 12);
        Clerigo tomas = new Clerigo("Tomás", 30);
        System.out.println(nara.getNombre() + " ataca con " + nara.atacar());
        System.out.println(tomas.getNombre() + " ataca con " + tomas.atacar() + " y cura hasta " + tomas.curar(10));
    }
}

abstract class Personaje {                 // <<abstract>>
    private final String nombre;           // -String nombre
    protected int vida;                    // #int vida

    protected Personaje(String nombre, int vida) {
        this.nombre = nombre;
        this.vida = vida;
    }

    public String getNombre() {
        return nombre;
    }

    public abstract int atacar();          // +atacar() int*   (abstracto)
}

class Guerrera extends Personaje {         // Personaje <|-- Guerrera
    private final int fuerza;              // -int fuerza

    public Guerrera(String nombre, int vida, int fuerza) {
        super(nombre, vida);
        this.fuerza = fuerza;
    }

    @Override
    public int atacar() {                  // +atacar() int
        return fuerza;
    }
}

interface Curador {                        // <<interface>>
    int curar(int vida);                   // +curar(int vida) int
}

class Clerigo extends Personaje implements Curador {    // Curador <|.. Clerigo
    public Clerigo(String nombre, int vida) {
        super(nombre, vida);
    }

    @Override
    public int atacar() {
        return 4;
    }

    @Override
    public int curar(int vida) {
        return vida + 20;
    }
}
```

### Salida esperada

```
Nara ataca con 12
Tomás ataca con 4 y cura hasta 30
```

### ¿Para qué sirve?

Los diagramas UML se usan para pensar un sistema antes de programarlo, para discutirlo con otras personas y para documentar cómo está armado. En los equipos de desarrollo se dibujan en pizarrones y documentos de diseño; en la facultad se evalúan en los exámenes. Saber leerlos te permite entender rápido un sistema que no escribiste.

### Errores habituales

**Ogro: la flecha de herencia al revés.** El triángulo apunta **al padre**:
`Personaje <|-- Guerrera` se lee "Guerrera hereda de Personaje".

**Ogro: el rombo del lado equivocado.** El rombo va del lado del **todo** (la factura),
no de la parte (el renglón).

**Ogro: confundir composición y agregación.** Preguntate: ¿la parte puede existir sin
el todo? Si sí, es agregación (rombo vacío).

**Ogro: poner los atributos que son relaciones.** Si `Caballero` tiene una
`Armadura`, se dibuja la relación (la línea con rombo), no además un atributo
`-armadura : Armadura` (salvo que el docente lo pida así).

**Slime: la sintaxis de Mermaid.** Si mermaid.live no dibuja nada, revisá que la
primera línea sea `classDiagram` o `sequenceDiagram` y que las llaves estén cerradas.

### Micro-misión R02-N10-P1 · Leer una caja

```meta
lugar: La biblioteca de la Academia
personajes: Zed, Gheco, Nadia, Kaffa
carta: Clase en UML | caja con tres partes: nombre, atributos y métodos · - es private · + es public · nombre: Tipo
recompensa: xp 10, oro 10
```

#### Escena
Kaffa señala la primera caja del plano:
`Viajero` / `- nombre: String` / `- edad: int` / `+ getNombre(): String`.
—Antes de levantar un edificio, lo dibujo —dice—. Este idioma lo lee cualquier arquitecta del Imperio. El **menos** es privado; el **más**, público.

#### Gheco sugiere
En una caja de UML, `- nombre: String` es un atributo **private** de tipo `String`, y `+ getNombre(): String` es un método **public** que devuelve un `String`. Primero el nombre, después los dos puntos y el tipo.

#### Desafío
Pasá la caja a código: completá la visibilidad de los dos atributos.

#### Código inicial
```java
public class Caja {
    public static void main(String[] args) {
        Viajero v = new Viajero("Zed", 19);
        System.out.println("Nombre: " + v.getNombre());
    }
}

class Viajero {
    ___ String nombre;
    ___ int edad;

    Viajero(String nombre, int edad) {
        this.nombre = nombre;
        this.edad = edad;
    }

    public String getNombre() {
        return nombre;
    }
}
```

#### Salida esperada
```
Nombre: Zed
```

#### Solución
```java
public class Caja {
    public static void main(String[] args) {
        Viajero v = new Viajero("Zed", 19);
        System.out.println("Nombre: " + v.getNombre());
    }
}

class Viajero {
    private String nombre;
    private int edad;

    Viajero(String nombre, int edad) {
        this.nombre = nombre;
        this.edad = edad;
    }

    public String getNombre() {
        return nombre;
    }
}
```

#### Al superarla
La caja del plano y el código dicen lo mismo. —Ahora, al revés —dice Kaffa—: cuando leas código, imaginate la caja.

#### Imagen
- Un plano de pergamino desenrollado sobre una mesa con una caja dibujada: «Viajero», sus atributos con «-» y su método con «+».
- Kaffa señalando con una pluma; Zed y Nadia inclinados sobre el plano.

### Micro-misión R02-N10-P2 · Las dos flechas huecas

```meta
lugar: La biblioteca de la Academia
personajes: Zed, Gheco, Nadia, Kaffa
carta: Herencia y realización | flecha llena con triángulo hueco: extends · flecha punteada con triángulo hueco: implements («interface»)
recompensa: xp 15, oro 15
```

#### Escena
En el plano hay dos flechas con punta de triángulo hueco. Una, de línea **llena**: de `Arquero` a `Personaje`. La otra, **punteada**: de `Grifo` a `«interface» Volador`.

#### Gheco sugiere
Triángulo hueco con línea llena: **herencia** (`extends`). Triángulo hueco con línea punteada: **realización**, una clase que implementa una interfaz (`implements`).

#### Desafío
Completá las dos palabras según las flechas del plano.

#### Código inicial
```java
public class Flechas {
    public static void main(String[] args) {
        Personaje p = new Arquero("Mira");
        Volador v = new Grifo();
        System.out.println(p.describir());
        System.out.println(v.volar());
    }
}

class Personaje {
    String nombre;

    Personaje(String nombre) { this.nombre = nombre; }

    String describir() { return nombre + ", un personaje"; }
}

class Arquero ___ Personaje {
    Arquero(String nombre) { super(nombre); }

    @Override
    String describir() { return nombre + ", arquera"; }
}

interface Volador {
    String volar();
}

class Grifo ___ Volador {
    public String volar() { return "El grifo vuela"; }
}
```

#### Salida esperada
```
Mira, arquera
El grifo vuela
```

#### Solución
```java
public class Flechas {
    public static void main(String[] args) {
        Personaje p = new Arquero("Mira");
        Volador v = new Grifo();
        System.out.println(p.describir());
        System.out.println(v.volar());
    }
}

class Personaje {
    String nombre;

    Personaje(String nombre) { this.nombre = nombre; }

    String describir() { return nombre + ", un personaje"; }
}

class Arquero extends Personaje {
    Arquero(String nombre) { super(nombre); }

    @Override
    String describir() { return nombre + ", arquera"; }
}

interface Volador {
    String volar();
}

class Grifo implements Volador {
    public String volar() { return "El grifo vuela"; }
}
```

#### Al superarla
Las dos flechas, traducidas. —Línea llena, lo que sos; punteada, lo que prometiste —resume Nadia, y lo anota así en la libreta.

#### Imagen
- Dos flechas dibujadas en el plano: una de línea llena con triángulo hueco y otra punteada, con el «interface» escrito arriba.
- Nadia anotando el resumen en su libreta.

### Micro-misión R02-N10-P3 · Rombo negro, rombo blanco

```meta
lugar: La biblioteca de la Academia
personajes: Zed, Gheco, Nadia, Kaffa
criatura: ogro
carta: Composición y agregación en UML | rombo negro (◆): composición, la parte se crea adentro · rombo blanco (◇): agregación, la parte viene de afuera
recompensa: xp 15, oro 15
```

#### Escena
En el plano, `Caballero ◆—— Armadura` y `Caballero ◇—— Caballo`. Un aprendiz los pasó a código al revés: el caballo nace con el caballero y la armadura viene de afuera. Compila y corre… pero no es el diseño. Un **ogro** lo aplaude.

#### Gheco sugiere
Rombo **negro** (composición): el caballero crea la armadura en su constructor (`new Armadura(...)`). Rombo **blanco** (agregación): el caballo existe antes y se pasa como parámetro.

#### Desafío
Completá el constructor según el plano: la armadura se crea adentro y el caballo llega de afuera.

#### Código inicial
```java
public class Rombos {
    public static void main(String[] args) {
        Caballo rayo = new Caballo("Rayo");
        Caballero teo = new Caballero("Teo", 8, rayo);
        System.out.println(teo.nombre + ": armadura " + teo.armadura.defensa + ", caballo " + teo.caballo.nombre);
        System.out.println("Es el mismo caballo: " + (teo.caballo == rayo));
    }
}

class Armadura {
    int defensa;

    Armadura(int defensa) { this.defensa = defensa; }
}

class Caballo {
    String nombre;

    Caballo(String nombre) { this.nombre = nombre; }
}

class Caballero {
    String nombre;
    Armadura armadura;
    Caballo caballo;

    Caballero(String nombre, int defensa, Caballo caballo) {
        this.nombre = nombre;
        this.armadura = ___;
        this.caballo = ___;
    }
}
```

#### Salida esperada
```
Teo: armadura 8, caballo Rayo
Es el mismo caballo: true
```

#### Solución
```java
public class Rombos {
    public static void main(String[] args) {
        Caballo rayo = new Caballo("Rayo");
        Caballero teo = new Caballero("Teo", 8, rayo);
        System.out.println(teo.nombre + ": armadura " + teo.armadura.defensa + ", caballo " + teo.caballo.nombre);
        System.out.println("Es el mismo caballo: " + (teo.caballo == rayo));
    }
}

class Armadura {
    int defensa;

    Armadura(int defensa) { this.defensa = defensa; }
}

class Caballo {
    String nombre;

    Caballo(String nombre) { this.nombre = nombre; }
}

class Caballero {
    String nombre;
    Armadura armadura;
    Caballo caballo;

    Caballero(String nombre, int defensa, Caballo caballo) {
        this.nombre = nombre;
        this.armadura = new Armadura(defensa);
        this.caballo = caballo;
    }
}
```

#### Al superarla
El código y el plano coinciden: armadura a medida, Rayo prestado. El ogro deja de aplaudir: un programa que anda pero no respeta el diseño era su favorito.

#### Imagen
- En el plano, un rombo negro hacia «Armadura» y un rombo blanco hacia «Caballo», con Teo dibujado en el centro.
- Un ogro con las manos quietas, decepcionado.

### Micro-misión R02-N10-P4 · Uno o más artesanos

```meta
lugar: La biblioteca de la Academia
personajes: Zed, Gheco, Nadia, Kaffa
carta: Multiplicidad | 1 exactamente uno · 0..1 uno o ninguno · * o 0..* muchos · 1..* al menos uno · en código, un array o una colección
recompensa: xp 15, oro 20
```

#### Escena
Al pie del plano, `Gremio "1" ◇—— "1..*" Artesano`: cada gremio tiene **al menos un** artesano. —Los números de las puntas dicen **cuántos** —explica Kaffa—. Y un gremio vacío no es un gremio.

#### Gheco sugiere
`1..*` del lado de `Artesano` significa que el gremio tiene **uno o más**: en código, un array `Artesano[] artesanos`. Para respetar el «al menos uno», el gremio pide un artesano al crearse.

#### Desafío
Completá el método que cuenta los artesanos usando el largo del array.

#### Código inicial
```java
public class Multiplicidad {
    public static void main(String[] args) {
        Artesano[] miembros = {new Artesano("la Maestra de Moldes"), new Artesano("Teo"), new Artesano("Zed")};
        Gremio gremio = new Gremio("Gremio de los Moldes", miembros);
        System.out.println(gremio.nombre + ": " + gremio.cantidad() + " artesanos");
        System.out.println("El último en entrar: " + gremio.artesanos[gremio.cantidad() - 1].nombre);
    }
}

class Artesano {
    String nombre;

    Artesano(String nombre) { this.nombre = nombre; }
}

class Gremio {
    String nombre;
    Artesano[] artesanos;

    Gremio(String nombre, Artesano[] artesanos) {
        this.nombre = nombre;
        this.artesanos = artesanos;
    }

    int cantidad() {
        return ___;
    }
}
```

#### Salida esperada
```
Gremio de los Moldes: 3 artesanos
El último en entrar: Zed
```

#### Solución
```java
public class Multiplicidad {
    public static void main(String[] args) {
        Artesano[] miembros = {new Artesano("la Maestra de Moldes"), new Artesano("Teo"), new Artesano("Zed")};
        Gremio gremio = new Gremio("Gremio de los Moldes", miembros);
        System.out.println(gremio.nombre + ": " + gremio.cantidad() + " artesanos");
        System.out.println("El último en entrar: " + gremio.artesanos[gremio.cantidad() - 1].nombre);
    }
}

class Artesano {
    String nombre;

    Artesano(String nombre) { this.nombre = nombre; }
}

class Gremio {
    String nombre;
    Artesano[] artesanos;

    Gremio(String nombre, Artesano[] artesanos) {
        this.nombre = nombre;
        this.artesanos = artesanos;
    }

    int cantidad() {
        return artesanos.length;
    }
}
```

#### Al superarla
«El último en entrar: Zed.» Un ladrón en un gremio de artesanos. Kaffa enrolla el plano… y Zed ve, en una esquina, un molde que nadie terminó de dibujar, **firmado con el dibujo de un vitral**.
Desde el sótano de la Academia llega un rugido de tres voces distintas.

#### Imagen
- En la esquina del plano, una caja a medio dibujar con una firma pequeña: un vitral de colores.
- Zed mirando la firma, con la llave del vitral en la otra mano; el piso de la biblioteca vibrando por un rugido.

### Misión R02-N10-M1 · Dibujá la herrería

```meta
entrega: archivo
entorno: local
extensiones: md, txt, png, jpg, pdf
monedas: 4
xp: 10
```

#### Consigna

Dibujá el **diagrama de clases** del ejemplo del nodo *Composición, agregación y
delegación* (`Caballero`, `Armadura`, `Espada`, `Caballo`): cada clase con sus
atributos y métodos con visibilidad, y las relaciones con el tipo correcto
(composición o agregación) y sus multiplicidades.

Podés escribirlo en Mermaid (entregá el `.md` o `.txt` con el texto) o dibujarlo y
entregar una foto o un PDF.

#### Criterio de aprobación

- Las cuatro clases con atributos y métodos, con `+` y `-` correctos.
- `Caballero` compone la `Armadura` (rombo lleno) y agrega la `Espada` y el `Caballo` (rombo vacío).
- Las multiplicidades tienen sentido (por ejemplo, `0..1` para el caballo).

#### Solución de referencia

```
classDiagram
    class Caballero {
        -String nombre
        +equipar(Espada espada)
        +montar(Caballo caballo)
        +atacar() int
        +defensa() int
        +velocidad() int
        +recibirGolpe(int fuerza)
    }
    class Armadura {
        -int proteccion
        +getProteccion() int
        +absorber(int golpe)
    }
    class Espada {
        -String nombre
        -int danio
        +danio() int
    }
    class Caballo {
        -String nombre
        -int velocidad
        +getNombre() String
        +getVelocidad() int
    }
    Caballero "1" *-- "1" Armadura : compone
    Caballero o-- "0..1" Espada : equipa
    Caballero o-- "0..1" Caballo : monta
```

### Misión R02-N10-M2 · Del plano al código

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Programá exactamente lo que dice este diagrama (respetando visibilidades, herencia,
interfaz y composición). `Biblioteca` crea sus estantes en el constructor (3
estantes, con capacidad 2 libros cada uno) y `agregar` pone el libro en el primer
estante con lugar. `Prestable` indica si un libro se puede prestar: los de
`Enciclopedia` nunca. En el `main`, agregá cuatro libros y mostrá cada estante y
cuántos se pueden prestar.

```
classDiagram
    class Libro {
        <<abstract>>
        -String titulo
        +getTitulo() String
        +descripcion()* String
    }
    class Novela {
        -String autor
        +descripcion() String
    }
    class Enciclopedia {
        -int tomo
        +descripcion() String
    }
    class Prestable {
        <<interface>>
        +sePuedePrestar() boolean
    }
    class Estante {
        -Libro[] libros
        -int cantidad
        +guardar(Libro l) boolean
    }
    class Biblioteca {
        -Estante[] estantes
        +agregar(Libro l) boolean
        +prestables() int
    }
    Libro <|-- Novela
    Libro <|-- Enciclopedia
    Prestable <|.. Libro
    Biblioteca "1" *-- "3" Estante
    Estante o-- "0..2" Libro
```

#### Criterio de aprobación

- Cada clase, interfaz, atributo y método del diagrama está en el código con su visibilidad.
- `Libro` es abstracta e implementa `Prestable`; la composición y la agregación se respetan.

#### Salida esperada

```
Estante 1: Rayuela, de Cortázar | Enciclopedia del Imperio, tomo 1
Estante 2: Ficciones, de Borges | Enciclopedia del Imperio, tomo 2
Estante 3: (vacío)
Se pueden prestar: 2
```

#### Solución de referencia

```java
// Mision 2 - Del plano al codigo: implementar un diagrama de clases.
public class Plano {
    public static void main(String[] args) {
        Biblioteca b = new Biblioteca();
        b.agregar(new Novela("Rayuela", "Cortázar"));
        b.agregar(new Enciclopedia("Enciclopedia del Imperio", 1));
        b.agregar(new Novela("Ficciones", "Borges"));
        b.agregar(new Enciclopedia("Enciclopedia del Imperio", 2));
        b.mostrar();
        System.out.println("Se pueden prestar: " + b.prestables());
    }
}

interface Prestable {
    boolean sePuedePrestar();
}

abstract class Libro implements Prestable {
    private final String titulo;

    protected Libro(String titulo) {
        this.titulo = titulo;
    }

    public String getTitulo() {
        return titulo;
    }

    public abstract String descripcion();

    @Override
    public boolean sePuedePrestar() {
        return true;
    }
}

class Novela extends Libro {
    private final String autor;

    public Novela(String titulo, String autor) {
        super(titulo);
        this.autor = autor;
    }

    @Override
    public String descripcion() {
        return getTitulo() + ", de " + autor;
    }
}

class Enciclopedia extends Libro {
    private final int tomo;

    public Enciclopedia(String titulo, int tomo) {
        super(titulo);
        this.tomo = tomo;
    }

    @Override
    public String descripcion() {
        return getTitulo() + ", tomo " + tomo;
    }

    @Override
    public boolean sePuedePrestar() {
        return false;
    }
}

class Estante {
    private final Libro[] libros = new Libro[2];
    private int cantidad;

    public boolean guardar(Libro l) {
        if (cantidad == libros.length) {
            return false;
        }
        libros[cantidad++] = l;
        return true;
    }

    public int prestables() {
        int n = 0;
        for (int i = 0; i < cantidad; i++) {
            if (libros[i].sePuedePrestar()) {
                n++;
            }
        }
        return n;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < cantidad; i++) {
            sb.append(i > 0 ? " | " : "").append(libros[i].descripcion());
        }
        return cantidad == 0 ? "(vacío)" : sb.toString();
    }
}

class Biblioteca {
    private final Estante[] estantes;

    public Biblioteca() {
        estantes = new Estante[3];
        for (int i = 0; i < estantes.length; i++) {
            estantes[i] = new Estante();
        }
    }

    public boolean agregar(Libro l) {
        for (Estante e : estantes) {
            if (e.guardar(l)) {
                return true;
            }
        }
        return false;
    }

    public int prestables() {
        int total = 0;
        for (Estante e : estantes) {
            total += e.prestables();
        }
        return total;
    }

    public void mostrar() {
        for (int i = 0; i < estantes.length; i++) {
            System.out.println("Estante " + (i + 1) + ": " + estantes[i]);
        }
    }
}
```

### Misión R02-N10-M3 · La secuencia del cobro

```meta
entrega: archivo
entorno: local
extensiones: md, txt, png, jpg, pdf
monedas: 4
xp: 10
```

#### Consigna

Dibujá el **diagrama de secuencia** de lo que pasa cuando el `main` de la misión *La
factura y sus renglones* llama a `f.imprimir()` con dos renglones: qué mensajes se
mandan, entre qué objetos y en qué orden (incluí las llamadas a `total()` y a
`subtotal()` de cada renglón, y las respuestas).

En Mermaid o dibujado a mano (foto o PDF).

#### Criterio de aprobación

- Aparecen `main`, la factura y los dos renglones como participantes.
- Los mensajes siguen el orden real del código, con sus respuestas.

#### Solución de referencia

```
sequenceDiagram
    participant M as main
    participant F as Factura
    participant R1 as renglon1
    participant R2 as renglon2
    M->>F: imprimir()
    F->>R1: toString()
    R1->>R1: subtotal()
    R1-->>F: texto del renglón 1
    F->>R2: toString()
    R2->>R2: subtotal()
    R2-->>F: texto del renglón 2
    F->>F: total()
    F->>R1: subtotal()
    R1-->>F: 2400.0
    F->>R2: subtotal()
    R2-->>F: 1350.0
    F-->>M: (muestra la factura)
```

### Encargo R02-N10-E1 · El sistema del consultorio

```meta
entrega: archivo
entorno: local
extensiones: md, txt, png, jpg, pdf
monedas: 1
xp: 15
```

#### Consigna

Un consultorio quiere un sistema de turnos: hay **pacientes** (nombre, DNI, obra
social opcional), **profesionales** (nombre, matrícula, especialidad) y **turnos**
(fecha, hora, un paciente y un profesional, y un estado: pendiente, atendido o
cancelado). Los médicos y los kinesiólogos son profesionales con datos propios. Hacé
el **diagrama de clases** completo, con un `enum` para el estado, las relaciones
correctas (¿el turno compone o agrega al paciente?) y las multiplicidades.

#### Criterio de aprobación

- Herencia para los tipos de profesional y un `enum` para el estado.
- Las relaciones del turno con paciente y profesional son agregaciones o asociaciones (existen por su cuenta).
- Multiplicidades razonables (un paciente tiene `0..*` turnos).

#### Solución de referencia

```
classDiagram
    class Paciente {
        -String nombre
        -String dni
        -String obraSocial
    }
    class Profesional {
        <<abstract>>
        -String nombre
        -String matricula
        +especialidad()* String
    }
    class Medico {
        -String especialidad
        +especialidad() String
    }
    class Kinesiologo {
        -int sesionesPorSemana
        +especialidad() String
    }
    class EstadoTurno {
        <<enumeration>>
        PENDIENTE
        ATENDIDO
        CANCELADO
    }
    class Turno {
        -String fecha
        -String hora
        -EstadoTurno estado
        +atender()
        +cancelar()
    }
    Profesional <|-- Medico
    Profesional <|-- Kinesiologo
    Turno "0..*" --> "1" Paciente
    Turno "0..*" --> "1" Profesional
    Turno --> EstadoTurno
```

### Prueba del sello

#### ¿Qué significan `+`, `-` y `#` en un diagrama de clases?

`public`, `private` y `protected`.

#### ¿Hacia dónde apunta el triángulo de la herencia?

Hacia la superclase (el padre).

#### ¿Qué diferencia hay entre un rombo lleno y uno vacío?

El lleno es composición (la parte vive y muere con el todo); el vacío, agregación (la parte existe por su cuenta).

#### ¿Qué muestra un diagrama de secuencia?

Qué mensajes se mandan los objetos entre sí y en qué orden.

#### En un diagrama, `Factura "1" *-- "1..*" Renglon`, ¿qué dice la multiplicidad?

Que cada factura tiene uno o más renglones y cada renglón pertenece a una sola factura.

### Soluciones (docente)

Sale de `18-Java/18-Diagramas-UML` (unidad 1). Suma lo que el capítulo original no tenía: asociación, multiplicidad, dependencia, soluciones de los diagramas y el pasaje en los dos sentidos. Las misiones 1 y 3 y el encargo se corrigen mirando el diagrama: hay más de una respuesta válida (por ejemplo, agregación o asociación simple entre el turno y el paciente).

## R02-N11 · Jefe: la Quimera de las Mil Herencias

```meta
tipo: jefe
padre: R02-N10
precio: 10
criatura: dragon
insignia: Sello de la Quimera
insignia_descripcion: Venciste a la Quimera de las Mil Herencias: pensás en objetos.
usa: poo.herencia, poo.interfaces, poo.composicion, diseno.uml
```

### Crónica

En el sótano de la Academia vive algo que nadie se animó a diseñar: la **Quimera de las Mil Herencias**. Un aprendiz intentó que heredara de León, de Cabra y de Serpiente a la vez, y el molde se rompió. Ahora es una criatura de tres cabezas, cada una con su elemento, que cambia de forma cada vez que la golpean.

—No se la vence con un solo molde —dice {mentor}—. Se la vence **modelándola bien**: qué es, qué tiene, qué sabe hacer. Si el diseño está bien, Zed, el combate se escribe solo.

### Objetivos

- Diseñar un programa orientado a objetos completo antes de escribirlo.
- Combinar herencia, clases abstractas, interfaces, `enum`, `record`, composición y polimorfismo.
- Elegir, para cada relación, la herramienta adecuada.

### Antes de empezar

- Toda la rama: clases, constructores, encapsulamiento, referencias, herencia, polimorfismo, interfaces, composición, `enum`, `record` y UML.

### Explicación

#### Diseñar antes de programar
Con objetos, el trabajo más importante pasa **antes** de escribir código:
1. **Buscá los sustantivos** de la consigna: son candidatos a clases (héroe, cabeza,
   quimera, ataque).
2. **Buscá los verbos**: son candidatos a métodos (atacar, recibir daño, curar).
3. **Decidí las relaciones**, frase por frase:
   - "una guerrera **es un** héroe" → herencia;
   - "una quimera **tiene** tres cabezas que mueren con ella" → composición;
   - "un clérigo y una poción **saben** curar" → interfaz;
   - "los elementos son fuego, hielo o veneno, y nada más" → `enum`;
   - "un golpe es un paquete de datos que no cambia" → `record`.
4. **Dibujá el diagrama de clases** (aunque sea en un papel).
5. **Escribí de a una clase** y probala desde el `main` antes de seguir.

#### Una tabla de efectividad con `enum`
Cuando el resultado depende de **dos** valores de un `enum` (el elemento del ataque y
el de la defensa), la regla puede vivir en el propio `enum`:
```java
enum Elemento {
    FUEGO, HIELO, VENENO;

    double contra(Elemento defensa) {
        if (this == defensa) return 0.5;                              // se resiste a sí mismo
        return switch (this) {
            case FUEGO -> defensa == HIELO ? 2.0 : 1.0;
            case HIELO -> defensa == VENENO ? 2.0 : 1.0;
            case VENENO -> defensa == FUEGO ? 2.0 : 1.0;
        };
    }
}
```

### Código de ejemplo

```java
/*
 * Jefe de la rama 2: el modelo de la Quimera.
 * Herencia (Heroe), interfaz (Curador), enum (Elemento), record (Golpe),
 * composición (la Quimera y sus Cabezas) y polimorfismo (cada héroe ataca a su manera).
 */
public class ModeloQuimera {
    public static void main(String[] args) {
        Quimera quimera = new Quimera(Elemento.FUEGO, Elemento.HIELO, Elemento.VENENO);
        Heroe[] grupo = {new Guerrera("Nara", Elemento.FUEGO), new Maga("Olmo", Elemento.HIELO), new Clerigo("Tomás")};
        System.out.println(quimera);

        for (Heroe h : grupo) {
            Golpe g = h.atacar();                         // polimorfismo
            int danio = quimera.recibir(g);               // la quimera delega en su cabeza activa
            System.out.println(h.getNombre() + " golpea con " + g.elemento() + " (" + g.fuerza() + ") -> " + danio + " de daño");
        }
        System.out.println(quimera);

        // Solo los que saben curar (interfaz)
        for (Heroe h : grupo) {
            if (h instanceof Curador c) {
                System.out.println(h.getNombre() + " cura " + c.curar() + " puntos al grupo");
            }
        }
        System.out.println("FUEGO contra HIELO x" + Elemento.FUEGO.contra(Elemento.HIELO)
                + ", FUEGO contra FUEGO x" + Elemento.FUEGO.contra(Elemento.FUEGO));
    }
}

enum Elemento {
    FUEGO, HIELO, VENENO;

    double contra(Elemento defensa) {
        if (this == defensa) {
            return 0.5;
        }
        return switch (this) {
            case FUEGO -> defensa == HIELO ? 2.0 : 1.0;
            case HIELO -> defensa == VENENO ? 2.0 : 1.0;
            case VENENO -> defensa == FUEGO ? 2.0 : 1.0;
        };
    }
}

record Golpe(int fuerza, Elemento elemento) { }

interface Curador {
    int curar();
}

abstract class Heroe {
    private final String nombre;

    protected Heroe(String nombre) {
        this.nombre = nombre;
    }

    public String getNombre() {
        return nombre;
    }

    public abstract Golpe atacar();
}

class Guerrera extends Heroe {
    private final Elemento elemento;

    public Guerrera(String nombre, Elemento elemento) {
        super(nombre);
        this.elemento = elemento;
    }

    @Override
    public Golpe atacar() {
        return new Golpe(14, elemento);
    }
}

class Maga extends Heroe {
    private final Elemento elemento;

    public Maga(String nombre, Elemento elemento) {
        super(nombre);
        this.elemento = elemento;
    }

    @Override
    public Golpe atacar() {
        return new Golpe(10, elemento);
    }
}

class Clerigo extends Heroe implements Curador {
    public Clerigo(String nombre) {
        super(nombre);
    }

    @Override
    public Golpe atacar() {
        return new Golpe(4, Elemento.VENENO);
    }

    @Override
    public int curar() {
        return 12;
    }
}

class Cabeza {
    private final Elemento elemento;
    private int vida = 40;

    Cabeza(Elemento elemento) {
        this.elemento = elemento;
    }

    int recibir(Golpe g) {
        int danio = (int) (g.fuerza() * g.elemento().contra(elemento));
        vida = Math.max(0, vida - danio);
        return danio;
    }

    boolean viva() {
        return vida > 0;
    }

    @Override
    public String toString() {
        return elemento + " " + vida;
    }
}

class Quimera {
    private final Cabeza[] cabezas;       // composición: nacen con la quimera
    private int activa = 0;

    Quimera(Elemento... elementos) {
        cabezas = new Cabeza[elementos.length];
        for (int i = 0; i < elementos.length; i++) {
            cabezas[i] = new Cabeza(elementos[i]);
        }
    }

    int recibir(Golpe g) {
        int danio = cabezas[activa].recibir(g);
        activa = (activa + 1) % cabezas.length;   // cambia de cabeza en cada golpe
        return danio;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("Quimera [");
        for (int i = 0; i < cabezas.length; i++) {
            sb.append(i > 0 ? " | " : "").append(cabezas[i]);
        }
        return sb.append("]").toString();
    }
}
```

### Salida esperada

```
Quimera [FUEGO 40 | HIELO 40 | VENENO 40]
Nara golpea con FUEGO (14) -> 7 de daño
Olmo golpea con HIELO (10) -> 5 de daño
Tomás golpea con VENENO (4) -> 2 de daño
Quimera [FUEGO 33 | HIELO 35 | VENENO 38]
Tomás cura 12 puntos al grupo
FUEGO contra HIELO x2.0, FUEGO contra FUEGO x0.5
```

### ¿Para qué sirve?

Así se diseña cualquier sistema orientado a objetos: un e-commerce (productos, carritos, medios de pago), un sistema escolar (alumnos, materias, notas), un juego (personajes, armas, niveles). Los mismos pasos (sustantivos, verbos, relaciones, diagrama, código de a una clase) sirven para el trabajo final de la facultad y para el primer proyecto en una empresa.

### Errores habituales

**Dragón: escribir antes de diseñar.** Empezar por el `main` y agregar clases a medida
que hacen falta termina en herencias sin sentido y métodos repetidos. Dibujá primero.

**Ogro: herencia para todo.** Si la frase no es "es un", no va `extends`. La quimera no
*es* una cabeza: *tiene* cabezas.

**Ogro: `instanceof` en todos lados.** Si cada método pregunta el tipo de cada objeto,
falta un método abstracto en el padre. Reservá `instanceof` para lo excepcional (como
las capacidades opcionales de una interfaz).

**Troll: el lugar vacío que deja una excepción.** En `notas[cantidad++] = new
Nota(m, v);`, Java incrementa `cantidad` **antes** de crear la nota. Si el constructor
lanza una excepción, queda un `null` en el array y más adelante aparece un
`NullPointerException`. Creá el objeto primero y guardalo después.

**Troll: la parte compartida sin querer.** Si dos quimeras reciben el mismo array de
cabezas, un golpe a una daña a la otra. En la composición, el todo crea sus partes.

### Micro-misión R02-N11-P1 · Qué es cada cabeza

```meta
lugar: El sótano de la Academia
personajes: Zed, Gheco, Nadia, Kaffa, la Maestra de Moldes
criatura: dragon
carta: Modelar lo que ES | una clase abstracta para lo común (Cabeza) · cada cabeza es un hijo que completa lo abstracto
recompensa: xp 20, oro 20
```

#### Escena
En el sótano vive la **Quimera de las Mil Herencias**: alguien quiso que heredara de León, de Cabra y de Serpiente a la vez, y el molde se rompió. Ahora tiene tres cabezas, cada una con su elemento.
—No se la vence con un solo molde —dice Kaffa—. Se la vence **modelándola bien**: qué es, qué tiene, qué sabe hacer. Empezá por lo que **es**: cada cabeza es una Cabeza.

#### Gheco sugiere
Lo que tienen todas las cabezas (nombre, vida y un ataque) va en la clase abstracta `Cabeza`. Cada cabeza concreta **extiende** a `Cabeza` y escribe su `atacar()`.

#### Desafío
Completá el ataque de la cabeza de Serpiente: "muerde con veneno".

#### Código inicial
```java
public class Quimera1 {
    public static void main(String[] args) {
        Cabeza[] cabezas = {new Leon(), new Cabra(), new Serpiente()};
        for (Cabeza c : cabezas) {
            System.out.println(c.nombre + " (" + c.vida + "): " + c.atacar());
        }
    }
}

abstract class Cabeza {
    String nombre;
    int vida;

    Cabeza(String nombre, int vida) {
        this.nombre = nombre;
        this.vida = vida;
    }

    abstract String atacar();
}

class Leon extends Cabeza {
    Leon() { super("León", 60); }

    @Override
    String atacar() { return "escupe fuego"; }
}

class Cabra extends Cabeza {
    Cabra() { super("Cabra", 40); }

    @Override
    String atacar() { return "embiste con hielo"; }
}

class Serpiente extends Cabeza {
    Serpiente() { super("Serpiente", 30); }

    @Override
    String atacar() { return ___; }
}
```

#### Salida esperada
```
León (60): escupe fuego
Cabra (40): embiste con hielo
Serpiente (30): muerde con veneno
```

#### Solución
```java
public class Quimera1 {
    public static void main(String[] args) {
        Cabeza[] cabezas = {new Leon(), new Cabra(), new Serpiente()};
        for (Cabeza c : cabezas) {
            System.out.println(c.nombre + " (" + c.vida + "): " + c.atacar());
        }
    }
}

abstract class Cabeza {
    String nombre;
    int vida;

    Cabeza(String nombre, int vida) {
        this.nombre = nombre;
        this.vida = vida;
    }

    abstract String atacar();
}

class Leon extends Cabeza {
    Leon() { super("León", 60); }

    @Override
    String atacar() { return "escupe fuego"; }
}

class Cabra extends Cabeza {
    Cabra() { super("Cabra", 40); }

    @Override
    String atacar() { return "embiste con hielo"; }
}

class Serpiente extends Cabeza {
    Serpiente() { super("Serpiente", 30); }

    @Override
    String atacar() { return "muerde con veneno"; }
}
```

#### Al superarla
Fuego, hielo y veneno: tres cabezas, un solo molde abstracto. La Quimera ruge y cambia de forma, pero ahora Zed sabe qué es cada parte.

#### Imagen
- La Quimera de las Mil Herencias: un cuerpo de bronce agrietado con tres cabezas, león de fuego, cabra de hielo y serpiente de veneno.
- Zed, Nadia y Gheco frente a ella en un sótano lleno de moldes rotos; Kaffa y la Maestra atrás.

### Micro-misión R02-N11-P2 · El golpe justo

```meta
lugar: El sótano de la Academia
personajes: Zed, Gheco, Nadia, Kaffa
carta: enum y record juntos | enum Elemento { FUEGO, HIELO, VENENO } · record Golpe(int danio, Elemento elemento) · el switch decide
recompensa: xp 20, oro 20
```

#### Escena
Cada cabeza es débil a un elemento: el León al hielo, la Cabra al fuego, la Serpiente al hielo también. Zed no puede improvisar los golpes: los tiene que **declarar**.

#### Gheco sugiere
Los elementos son una lista cerrada: un `enum`. Un golpe es solo un paquete de datos: un `record`. La debilidad de cada cabeza se decide con un `switch` sobre el nombre.

#### Desafío
Completá el caso de la Cabra: es débil al FUEGO.

#### Código inicial
```java
public class Quimera2 {
    static Elemento debilidad(String cabeza) {
        return switch (cabeza) {
            case "León" -> Elemento.HIELO;
            case "Cabra" -> ___;
            default -> Elemento.HIELO;
        };
    }

    public static void main(String[] args) {
        String[] cabezas = {"León", "Cabra", "Serpiente"};
        for (String c : cabezas) {
            Golpe g = new Golpe(25, debilidad(c));
            System.out.println(c + ": " + g);
        }
    }
}

enum Elemento {
    FUEGO, HIELO, VENENO
}

record Golpe(int danio, Elemento elemento) {
}
```

#### Salida esperada
```
León: Golpe[danio=25, elemento=HIELO]
Cabra: Golpe[danio=25, elemento=FUEGO]
Serpiente: Golpe[danio=25, elemento=HIELO]
```

#### Solución
```java
public class Quimera2 {
    static Elemento debilidad(String cabeza) {
        return switch (cabeza) {
            case "León" -> Elemento.HIELO;
            case "Cabra" -> Elemento.FUEGO;
            default -> Elemento.HIELO;
        };
    }

    public static void main(String[] args) {
        String[] cabezas = {"León", "Cabra", "Serpiente"};
        for (String c : cabezas) {
            Golpe g = new Golpe(25, debilidad(c));
            System.out.println(c + ": " + g);
        }
    }
}

enum Elemento {
    FUEGO, HIELO, VENENO
}

record Golpe(int danio, Elemento elemento) {
}
```

#### Al superarla
Tres golpes declarados, cada uno con su elemento. La Quimera retrocede: por primera vez, alguien la atacó con un plan.

#### Imagen
- Tres esferas de luz flotando frente a Zed: dos de hielo (celestes) y una de fuego (naranja), cada una con una etiqueta.
- La Quimera retrocediendo contra la pared del sótano.

### Micro-misión R02-N11-P3 · Lo que tiene la Quimera

```meta
lugar: El sótano de la Academia
personajes: Zed, Gheco, Nadia, Kaffa
carta: Composición y delegación | la Quimera TIENE cabezas (un array) · su vida es la suma de las de sus cabezas · le delega a cada una
recompensa: xp 20, oro 25
```

#### Escena
—La Quimera no **es** un león, ni una cabra, ni una serpiente —dice Kaffa—. **Tiene** tres cabezas. Ese fue el error del aprendiz. Su vida es la de sus cabezas, sumadas.

#### Gheco sugiere
La `Quimera` tiene un array de `Cabeza` (composición). Para saber su vida total, recorre las cabezas y le **pregunta a cada una** su vida: `total += c.getVida();`.

#### Desafío
Completá el acumulador: sumá la vida de cada cabeza.

#### Código inicial
```java
public class Quimera3 {
    public static void main(String[] args) {
        Quimera q = new Quimera();
        System.out.println("Vida de la Quimera: " + q.vidaTotal());
        q.cabezas[2].recibir(30);
        System.out.println("Después de golpear a la Serpiente: " + q.vidaTotal());
    }
}

class Cabeza {
    private String nombre;
    private int vida;

    Cabeza(String nombre, int vida) {
        this.nombre = nombre;
        this.vida = vida;
    }

    int getVida() { return vida; }

    void recibir(int danio) { vida = Math.max(0, vida - danio); }
}

class Quimera {
    Cabeza[] cabezas = {new Cabeza("León", 60), new Cabeza("Cabra", 40), new Cabeza("Serpiente", 30)};

    int vidaTotal() {
        int total = 0;
        for (Cabeza c : cabezas) {
            ___;
        }
        return total;
    }
}
```

#### Salida esperada
```
Vida de la Quimera: 130
Después de golpear a la Serpiente: 100
```

#### Solución
```java
public class Quimera3 {
    public static void main(String[] args) {
        Quimera q = new Quimera();
        System.out.println("Vida de la Quimera: " + q.vidaTotal());
        q.cabezas[2].recibir(30);
        System.out.println("Después de golpear a la Serpiente: " + q.vidaTotal());
    }
}

class Cabeza {
    private String nombre;
    private int vida;

    Cabeza(String nombre, int vida) {
        this.nombre = nombre;
        this.vida = vida;
    }

    int getVida() { return vida; }

    void recibir(int danio) { vida = Math.max(0, vida - danio); }
}

class Quimera {
    Cabeza[] cabezas = {new Cabeza("León", 60), new Cabeza("Cabra", 40), new Cabeza("Serpiente", 30)};

    int vidaTotal() {
        int total = 0;
        for (Cabeza c : cabezas) {
            total += c.getVida();
        }
        return total;
    }
}
```

#### Al superarla
De 130 a 100: la Serpiente cae y su cabeza se apaga. Quedan dos.

#### Imagen
- La cabeza de serpiente de la Quimera apagándose, gris; las otras dos rugiendo.
- Un contador de vida de bronce sobre la Quimera bajando de 130 a 100.

### Micro-misión R02-N11-P4 · El combate se escribe solo

```meta
lugar: El sótano de la Academia
personajes: Zed, Gheco, Nadia, Kaffa, la Maestra de Moldes
carta: Todo junto | herencia, polimorfismo, composición, enum y record · si el diseño está bien, el combate es un bucle de cinco líneas
recompensa: xp 25, oro 30
item: Guantes del Artesano
```

#### Escena
Quedan el León y la Cabra. —Si el diseño está bien —dice Kaffa—, el combate se escribe solo. Cada cabeza sabe su debilidad; vos solo tenés que **pegarle con lo que le duele**.

#### Gheco sugiere
Cada `Cabeza` sabe su debilidad (`debilidad()`). Un golpe con ese elemento hace el **doble** de daño. En el bucle, armá el golpe con la debilidad de **esa** cabeza: `new Golpe(35, c.debilidad())`.

#### Desafío
Completá el golpe: 35 de daño, con el elemento al que es débil cada cabeza.

#### Código inicial
```java
public class Quimera4 {
    public static void main(String[] args) {
        Cabeza[] cabezas = {new Leon(), new Cabra()};
        for (Cabeza c : cabezas) {
            Golpe g = ___;
            c.recibir(g);
            System.out.println(c.nombre + " recibe " + g.elemento() + ": le queda " + c.vida);
        }
        System.out.println("La Quimera cae.");
    }
}

enum Elemento {
    FUEGO, HIELO, VENENO
}

record Golpe(int danio, Elemento elemento) {
}

abstract class Cabeza {
    String nombre;
    int vida;

    Cabeza(String nombre, int vida) {
        this.nombre = nombre;
        this.vida = vida;
    }

    abstract Elemento debilidad();

    void recibir(Golpe g) {
        int danio = g.elemento() == debilidad() ? g.danio() * 2 : g.danio();
        vida = Math.max(0, vida - danio);
    }
}

class Leon extends Cabeza {
    Leon() { super("León", 60); }

    @Override
    Elemento debilidad() { return Elemento.HIELO; }
}

class Cabra extends Cabeza {
    Cabra() { super("Cabra", 40); }

    @Override
    Elemento debilidad() { return Elemento.FUEGO; }
}
```

#### Salida esperada
```
León recibe HIELO: le queda 0
Cabra recibe FUEGO: le queda 0
La Quimera cae.
```

#### Solución
```java
public class Quimera4 {
    public static void main(String[] args) {
        Cabeza[] cabezas = {new Leon(), new Cabra()};
        for (Cabeza c : cabezas) {
            Golpe g = new Golpe(35, c.debilidad());
            c.recibir(g);
            System.out.println(c.nombre + " recibe " + g.elemento() + ": le queda " + c.vida);
        }
        System.out.println("La Quimera cae.");
    }
}

enum Elemento {
    FUEGO, HIELO, VENENO
}

record Golpe(int danio, Elemento elemento) {
}

abstract class Cabeza {
    String nombre;
    int vida;

    Cabeza(String nombre, int vida) {
        this.nombre = nombre;
        this.vida = vida;
    }

    abstract Elemento debilidad();

    void recibir(Golpe g) {
        int danio = g.elemento() == debilidad() ? g.danio() * 2 : g.danio();
        vida = Math.max(0, vida - danio);
    }
}

class Leon extends Cabeza {
    Leon() { super("León", 60); }

    @Override
    Elemento debilidad() { return Elemento.HIELO; }
}

class Cabra extends Cabeza {
    Cabra() { super("Cabra", 40); }

    @Override
    Elemento debilidad() { return Elemento.FUEGO; }
}
```

#### Al superarla
Hielo al León, fuego a la Cabra, y la Quimera cae. Del molde roto queda un par de **guantes de cuero y bronce**: la Maestra se los da a Zed. —Los **Guantes del Artesano**. Desde hoy sos aprendiz de la Academia.
Kaffa termina su café. —Los Archivos Imperiales guardan el registro de todos los que cruzaron. También el de alguien que llegó con un vitral.

#### Imagen
- La Quimera derrumbándose en el sótano entre moldes rotos, con las tres cabezas apagadas.
- La Maestra de Moldes entregándole a Zed un par de guantes de cuero con remaches de bronce.
- Kaffa con su taza; Nadia y Gheco celebrando atrás.

### Misión R02-N11-M1 · La batalla contra la Quimera

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Programá la batalla completa. El grupo es: **Nara**, guerrera de fuego (fuerza 14),
**Olmo**, mago de hielo (fuerza 10, pero cada 3 ataques lanza un hechizo de 25) y
**Tomás**, clérigo (ataca con veneno de fuerza 4 y además es `Curador`: cura 12). La
Quimera tiene tres cabezas (fuego, hielo y veneno, 40 de vida cada una) y cambia de
cabeza activa después de cada golpe, **salteando las cabezas muertas**.

Cada ronda: los tres héroes atacan en orden; después, cada cabeza viva de la quimera
ataca al héroe con más vida con fuerza 8 multiplicada por la efectividad de su
elemento contra el elemento del héroe (el clérigo no tiene elemento: efectividad 1).
Al terminar la ronda, el clérigo cura 12 al héroe con menos vida (sin pasar de su
vida máxima). Los héroes arrancan con 60 (guerrera), 40 (mago) y 45 (clérigo) de vida.
La batalla termina cuando mueren las tres cabezas o todos los héroes. Mostrá cada
ronda y el resultado. No hay azar: el resultado sale siempre igual.

#### Criterio de aprobación

- `Heroe` es abstracta; `Curador` es una interfaz; `Elemento` es un `enum` con la tabla de efectividad; `Golpe` es un `record`.
- La quimera compone sus cabezas y saltea las muertas.
- Cada héroe ataca a su manera sin que el bucle pregunte su tipo (salvo para curar).
- La salida coincide con la esperada.

#### Salida esperada

```
--- Ronda 1 ---
Nara -> cabeza de FUEGO: 7
Olmo -> cabeza de HIELO: 5
Tomás -> cabeza de VENENO: 2
Cabeza de FUEGO -> Nara: 4
Cabeza de HIELO -> Nara: 8
Cabeza de VENENO -> Nara: 16
Tomás cura a Nara
Quimera [FUEGO 33 | HIELO 35 | VENENO 38] | Nara 44  Olmo 40  Tomás 45
--- Ronda 2 ---
Nara -> cabeza de FUEGO: 7
Olmo -> cabeza de HIELO: 5
Tomás -> cabeza de VENENO: 2
Cabeza de FUEGO -> Tomás: 8
Cabeza de HIELO -> Nara: 8
Cabeza de VENENO -> Olmo: 8
Tomás cura a Olmo
Quimera [FUEGO 26 | HIELO 30 | VENENO 36] | Nara 36  Olmo 40  Tomás 37
--- Ronda 3 ---
Nara -> cabeza de FUEGO: 7
Olmo -> cabeza de HIELO: 12
Tomás -> cabeza de VENENO: 2
Cabeza de FUEGO -> Olmo: 16
Cabeza de HIELO -> Tomás: 8
Cabeza de VENENO -> Nara: 16
Tomás cura a Nara
Quimera [FUEGO 19 | HIELO 18 | VENENO 34] | Nara 32  Olmo 24  Tomás 29
--- Ronda 4 ---
Nara -> cabeza de FUEGO: 7
Olmo -> cabeza de HIELO: 5
Tomás -> cabeza de VENENO: 2
Cabeza de FUEGO -> Nara: 4
Cabeza de HIELO -> Tomás: 8
Cabeza de VENENO -> Nara: 16
Tomás cura a Nara
Quimera [FUEGO 12 | HIELO 13 | VENENO 32] | Nara 24  Olmo 24  Tomás 21
--- Ronda 5 ---
Nara -> cabeza de FUEGO: 7
Olmo -> cabeza de HIELO: 5
Tomás -> cabeza de VENENO: 2
Cabeza de FUEGO -> Nara: 4
Cabeza de HIELO -> Olmo: 4
Cabeza de VENENO -> Tomás: 8
Tomás cura a Tomás
Quimera [FUEGO 5 | HIELO 8 | VENENO 30] | Nara 20  Olmo 20  Tomás 25
--- Ronda 6 ---
Nara -> cabeza de FUEGO: 7
Olmo -> cabeza de HIELO: 12
Tomás -> cabeza de VENENO: 2
Cabeza de VENENO -> Tomás: 8
Tomás cura a Tomás
Quimera [FUEGO 0 | HIELO 0 | VENENO 28] | Nara 20  Olmo 20  Tomás 29
--- Ronda 7 ---
Nara -> cabeza de VENENO: 14
Olmo -> cabeza de VENENO: 20
Tomás cura a Nara
Quimera [FUEGO 0 | HIELO 0 | VENENO 0] | Nara 32  Olmo 20  Tomás 29
¡La Quimera cae en la ronda 7!
```

#### Solución de referencia

```java
// Jefe R02 - Mision 1: la batalla contra la Quimera.
public class BatallaQuimera {
    public static void main(String[] args) {
        Heroe[] grupo = {new Guerrera("Nara", Elemento.FUEGO, 60), new Mago("Olmo", Elemento.HIELO, 40), new Clerigo("Tomás", 45)};
        Quimera quimera = new Quimera(Elemento.FUEGO, Elemento.HIELO, Elemento.VENENO);
        int ronda = 0;
        while (quimera.viva() && hayVivos(grupo) && ronda < 20) {
            ronda++;
            System.out.println("--- Ronda " + ronda + " ---");
            for (Heroe h : grupo) {
                if (h.vivo() && quimera.viva()) {
                    Golpe g = h.atacar();
                    String cabeza = quimera.cabezaActiva();
                    int danio = quimera.recibir(g);
                    System.out.println(h.getNombre() + " -> cabeza de " + cabeza + ": " + danio);
                }
            }
            for (Cabeza c : quimera.cabezasVivas()) {
                Heroe objetivo = masVida(grupo);
                if (objetivo == null) {
                    break;
                }
                int danio = (int) (8 * c.getElemento().contra(objetivo.getElemento()));
                objetivo.recibir(danio);
                System.out.println("Cabeza de " + c.getElemento() + " -> " + objetivo.getNombre() + ": " + danio);
            }
            for (Heroe h : grupo) {
                if (h instanceof Curador cur && h.vivo()) {
                    Heroe herido = menosVida(grupo);
                    if (herido != null) {
                        herido.curarse(cur.curar());
                        System.out.println(h.getNombre() + " cura a " + herido.getNombre());
                    }
                }
            }
            System.out.println(quimera + " | " + estado(grupo));
        }
        System.out.println(quimera.viva() ? "La Quimera sigue en pie." : "¡La Quimera cae en la ronda " + ronda + "!");
    }

    static boolean hayVivos(Heroe[] grupo) {
        for (Heroe h : grupo) {
            if (h.vivo()) {
                return true;
            }
        }
        return false;
    }

    static Heroe masVida(Heroe[] grupo) {
        Heroe mejor = null;
        for (Heroe h : grupo) {
            if (h.vivo() && (mejor == null || h.getVida() > mejor.getVida())) {
                mejor = h;
            }
        }
        return mejor;
    }

    static Heroe menosVida(Heroe[] grupo) {
        Heroe peor = null;
        for (Heroe h : grupo) {
            if (h.vivo() && (peor == null || h.getVida() < peor.getVida())) {
                peor = h;
            }
        }
        return peor;
    }

    static String estado(Heroe[] grupo) {
        StringBuilder sb = new StringBuilder();
        for (Heroe h : grupo) {
            sb.append(h.getNombre()).append(" ").append(h.getVida()).append("  ");
        }
        return sb.toString().trim();
    }
}

enum Elemento {
    FUEGO, HIELO, VENENO;

    double contra(Elemento defensa) {
        if (defensa == null) {
            return 1.0;
        }
        if (this == defensa) {
            return 0.5;
        }
        return switch (this) {
            case FUEGO -> defensa == HIELO ? 2.0 : 1.0;
            case HIELO -> defensa == VENENO ? 2.0 : 1.0;
            case VENENO -> defensa == FUEGO ? 2.0 : 1.0;
        };
    }
}

record Golpe(int fuerza, Elemento elemento) { }

interface Curador {
    int curar();
}

abstract class Heroe {
    private final String nombre;
    private final Elemento elemento;
    private final int vidaMaxima;
    private int vida;

    protected Heroe(String nombre, Elemento elemento, int vida) {
        this.nombre = nombre;
        this.elemento = elemento;
        this.vidaMaxima = vida;
        this.vida = vida;
    }

    public String getNombre() {
        return nombre;
    }

    public Elemento getElemento() {
        return elemento;
    }

    public int getVida() {
        return vida;
    }

    public boolean vivo() {
        return vida > 0;
    }

    public void recibir(int danio) {
        vida = Math.max(0, vida - danio);
    }

    public void curarse(int puntos) {
        vida = Math.min(vidaMaxima, vida + puntos);
    }

    public abstract Golpe atacar();
}

class Guerrera extends Heroe {
    public Guerrera(String nombre, Elemento elemento, int vida) {
        super(nombre, elemento, vida);
    }

    @Override
    public Golpe atacar() {
        return new Golpe(14, getElemento());
    }
}

class Mago extends Heroe {
    private int ataques = 0;

    public Mago(String nombre, Elemento elemento, int vida) {
        super(nombre, elemento, vida);
    }

    @Override
    public Golpe atacar() {
        ataques++;
        return new Golpe(ataques % 3 == 0 ? 25 : 10, getElemento());
    }
}

class Clerigo extends Heroe implements Curador {
    public Clerigo(String nombre, int vida) {
        super(nombre, null, vida);
    }

    @Override
    public Golpe atacar() {
        return new Golpe(4, Elemento.VENENO);
    }

    @Override
    public int curar() {
        return 12;
    }
}

class Cabeza {
    private final Elemento elemento;
    private int vida = 40;

    Cabeza(Elemento elemento) {
        this.elemento = elemento;
    }

    Elemento getElemento() {
        return elemento;
    }

    int recibir(Golpe g) {
        int danio = (int) (g.fuerza() * g.elemento().contra(elemento));
        vida = Math.max(0, vida - danio);
        return danio;
    }

    boolean viva() {
        return vida > 0;
    }

    @Override
    public String toString() {
        return elemento + " " + vida;
    }
}

class Quimera {
    private final Cabeza[] cabezas;
    private int activa = 0;

    Quimera(Elemento... elementos) {
        cabezas = new Cabeza[elementos.length];
        for (int i = 0; i < elementos.length; i++) {
            cabezas[i] = new Cabeza(elementos[i]);
        }
    }

    boolean viva() {
        for (Cabeza c : cabezas) {
            if (c.viva()) {
                return true;
            }
        }
        return false;
    }

    String cabezaActiva() {
        return cabezas[activa].getElemento().toString();
    }

    int recibir(Golpe g) {
        int danio = cabezas[activa].recibir(g);
        avanzar();
        return danio;
    }

    private void avanzar() {
        for (int i = 1; i <= cabezas.length; i++) {
            int siguiente = (activa + i) % cabezas.length;
            if (cabezas[siguiente].viva()) {
                activa = siguiente;
                return;
            }
        }
    }

    Cabeza[] cabezasVivas() {
        int n = 0;
        for (Cabeza c : cabezas) {
            if (c.viva()) {
                n++;
            }
        }
        Cabeza[] vivas = new Cabeza[n];
        int i = 0;
        for (Cabeza c : cabezas) {
            if (c.viva()) {
                vivas[i++] = c;
            }
        }
        return vivas;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("Quimera [");
        for (int i = 0; i < cabezas.length; i++) {
            sb.append(i > 0 ? " | " : "").append(cabezas[i]);
        }
        return sb.append("]").toString();
    }
}
```

### Misión R02-N11-M2 · El legajo de la Academia

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

La Academia lleva el legajo de sus estudiantes. Modelá:

- un `enum Materia` con nombre visible y **carga horaria**: `ALGEBRA` (96 h),
  `PROGRAMACION` (128 h), `DISENO` (64 h) y `BASES_DE_DATOS` (96 h);
- un `record Nota(Materia materia, int valor)` que rechaza valores fuera de 1 a 10;
- una clase `Estudiante` (legajo `final`, nombre) que **compone** un array de hasta
  10 notas y sabe `registrar(Materia, int)`, `promedio()`, `aprobadas()` (nota ≥ 4) y
  `horasAprobadas()`; implementa `Comparable<Estudiante>` (mejor promedio primero; si
  empatan, por legajo).

Leé las notas de la entrada con el formato `legajo;nombre;MATERIA;nota` (un
estudiante puede aparecer en varias líneas) hasta una línea vacía. Las líneas con
errores (materia inexistente, nota fuera de rango) se informan y se saltean. Al final,
mostrá el ranking ordenado con promedio, materias aprobadas y horas aprobadas.

#### Criterio de aprobación

- `Materia` es un `enum` con atributos; `Nota` es un `record` validado.
- `Estudiante` compone sus notas y es `Comparable`.
- Las líneas inválidas se informan sin cortar el programa.
- La salida coincide con la esperada.

#### Entrada de ejemplo

```
101;Nadia;PROGRAMACION;9
102;Baldo;ALGEBRA;6
101;Nadia;ALGEBRA;7
103;Lía;DISENO;10
102;Baldo;PROGRAMACION;3
103;Lía;QUIMICA;8
101;Nadia;DISENO;11
103;Lía;BASES_DE_DATOS;8
102;Baldo;BASES_DE_DATOS;9

```

#### Salida esperada

```
Línea salteada [103;Lía;QUIMICA;8]: No enum constant Materia.QUIMICA
Línea salteada [101;Nadia;DISENO;11]: nota fuera de rango: 11

Ranking de la Academia
1. Lía (103)  promedio 9.00  aprobadas 2  horas 160
2. Nadia (101)  promedio 8.00  aprobadas 2  horas 224
3. Baldo (102)  promedio 6.00  aprobadas 2  horas 192
```

#### Solución de referencia

```java
// Jefe R02 - Mision 2: el legajo de la Academia.
import java.util.Arrays;
import java.util.Locale;
import java.util.Scanner;

public class Legajos {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Scanner teclado = new Scanner(System.in);
        Estudiante[] estudiantes = new Estudiante[20];
        int cantidad = 0;

        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.isEmpty()) {
                break;
            }
            String[] p = linea.split(";");
            try {
                int legajo = Integer.parseInt(p[0]);
                Materia materia = Materia.valueOf(p[2]);
                int valor = Integer.parseInt(p[3]);
                Estudiante e = buscar(estudiantes, cantidad, legajo);
                if (e == null) {
                    e = new Estudiante(legajo, p[1]);
                    estudiantes[cantidad++] = e;
                }
                e.registrar(materia, valor);
            } catch (IllegalArgumentException | ArrayIndexOutOfBoundsException ex) {
                System.out.println("Línea salteada [" + linea + "]: " + ex.getMessage());
            }
        }

        Estudiante[] ranking = Arrays.copyOf(estudiantes, cantidad);
        Arrays.sort(ranking);
        System.out.println();
        System.out.println("Ranking de la Academia");
        int puesto = 1;
        for (Estudiante e : ranking) {
            System.out.printf("%d. %s  promedio %.2f  aprobadas %d  horas %d%n",
                    puesto++, e, e.promedio(), e.aprobadas(), e.horasAprobadas());
        }
    }

    static Estudiante buscar(Estudiante[] lista, int n, int legajo) {
        for (int i = 0; i < n; i++) {
            if (lista[i].getLegajo() == legajo) {
                return lista[i];
            }
        }
        return null;
    }
}

enum Materia {
    ALGEBRA("Álgebra", 96), PROGRAMACION("Programación", 128), DISENO("Diseño", 64), BASES_DE_DATOS("Bases de datos", 96);

    private final String nombre;
    private final int horas;

    Materia(String nombre, int horas) {
        this.nombre = nombre;
        this.horas = horas;
    }

    public String getNombre() {
        return nombre;
    }

    public int getHoras() {
        return horas;
    }
}

record Nota(Materia materia, int valor) {
    Nota {
        if (valor < 1 || valor > 10) {
            throw new IllegalArgumentException("nota fuera de rango: " + valor);
        }
    }

    boolean aprobada() {
        return valor >= 4;
    }
}

class Estudiante implements Comparable<Estudiante> {
    private final int legajo;
    private final String nombre;
    private final Nota[] notas = new Nota[10];
    private int cantidad;

    public Estudiante(int legajo, String nombre) {
        this.legajo = legajo;
        this.nombre = nombre;
    }

    public int getLegajo() {
        return legajo;
    }

    public void registrar(Materia materia, int valor) {
        Nota nota = new Nota(materia, valor);      // primero se crea (puede fallar)...
        if (cantidad < notas.length) {
            notas[cantidad++] = nota;               // ...y recién después se guarda
        }
    }

    public double promedio() {
        if (cantidad == 0) {
            return 0;
        }
        int suma = 0;
        for (int i = 0; i < cantidad; i++) {
            suma += notas[i].valor();
        }
        return (double) suma / cantidad;
    }

    public int aprobadas() {
        int n = 0;
        for (int i = 0; i < cantidad; i++) {
            if (notas[i].aprobada()) {
                n++;
            }
        }
        return n;
    }

    public int horasAprobadas() {
        int horas = 0;
        for (int i = 0; i < cantidad; i++) {
            if (notas[i].aprobada()) {
                horas += notas[i].materia().getHoras();
            }
        }
        return horas;
    }

    @Override
    public int compareTo(Estudiante otro) {
        int c = Double.compare(otro.promedio(), promedio());
        return c != 0 ? c : Integer.compare(legajo, otro.legajo);
    }

    @Override
    public String toString() {
        return nombre + " (" + legajo + ")";
    }
}
```

#### Pruebas

##### Un solo estudiante
```entrada
200;Zoe;ALGEBRA;4
200;Zoe;DISENO;3
```
```salida
Ranking de la Academia
1. Zoe (200)  promedio 3.50  aprobadas 1  horas 96
```

##### Empate de promedio
```entrada
2;B;ALGEBRA;8
1;A;DISENO;8
```
```salida
Ranking de la Academia
1. A (1)  promedio 8.00  aprobadas 1  horas 64
2. B (2)  promedio 8.00  aprobadas 1  horas 96
```

##### Solo errores
```entrada
5;X;MAGIA;5
6;Y;ALGEBRA;0
```
```salida
Línea salteada [5;X;MAGIA;5]: No enum constant Materia.MAGIA
Línea salteada [6;Y;ALGEBRA;0]: nota fuera de rango: 0

Ranking de la Academia
1. Y (6)  promedio 0.00  aprobadas 0  horas 0
```

### Encargo R02-N11-E1 · El estacionamiento

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 30
```

#### Consigna

Diseñá y programá un estacionamiento con 6 cocheras. Hay tres tipos de vehículo
(`MOTO`, `AUTO`, `CAMIONETA`, un `enum` con la tarifa por hora: 800, 1500 y 2200).
Cada `Vehiculo` es un `record` (patente, tipo). Cada `Cochera` (número) puede estar
libre u ocupada por un vehículo con su hora de entrada (un entero de 0 a 23). El
`Estacionamiento` compone sus cocheras y sabe `ingresar(Vehiculo v, int hora)` (en la
primera libre; las camionetas solo entran en las cocheras 5 y 6), `egresar(String
patente, int hora)` (devuelve el importe: horas × tarifa, mínimo una hora) y mostrar
el estado. Procesá los movimientos de la entrada (`E patente TIPO hora` o `S patente
hora`) y mostrá la recaudación total.

#### Criterio de aprobación

- Usa `enum`, `record` y composición.
- Las reglas (cocheras para camionetas, hora mínima) están en las clases, no en el `main`.

#### Entrada de ejemplo

```
E AB123CD AUTO 8
E A111AA MOTO 9
E AE555FG CAMIONETA 9
E AC777HH CAMIONETA 10
E AF888JJ CAMIONETA 10
S A111AA 11
S AB123CD 8
S AE555FG 14
E AD999KK AUTO 15
S AD999KK 18

```

#### Salida esperada

```
AB123CD entra a la cochera 1
A111AA entra a la cochera 2
AE555FG entra a la cochera 5
AC777HH entra a la cochera 6
AF888JJ: no hay cochera para CAMIONETA
A111AA sale y paga $1600
AB123CD sale y paga $1500
AE555FG sale y paga $11000
AD999KK entra a la cochera 1
AD999KK sale y paga $4500
Cocheras: 1:libre 2:libre 3:libre 4:libre 5:libre 6:AC777HH
Recaudación: $18600
```

#### Solución de referencia

```java
// Jefe R02 - Encargo: el estacionamiento.
import java.util.Scanner;

public class Estacionamientos {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        Estacionamiento est = new Estacionamiento(6);
        int recaudado = 0;
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.isEmpty()) {
                break;
            }
            String[] p = linea.split(" ");
            if (p[0].equals("E")) {
                Vehiculo v = new Vehiculo(p[1], Tipo.valueOf(p[2]));
                int cochera = est.ingresar(v, Integer.parseInt(p[3]));
                System.out.println(cochera > 0 ? p[1] + " entra a la cochera " + cochera : p[1] + ": no hay cochera para " + v.tipo());
            } else {
                int importe = est.egresar(p[1], Integer.parseInt(p[2]));
                if (importe < 0) {
                    System.out.println(p[1] + " no está en el estacionamiento");
                } else {
                    System.out.println(p[1] + " sale y paga $" + importe);
                    recaudado += importe;
                }
            }
        }
        System.out.println(est);
        System.out.println("Recaudación: $" + recaudado);
    }
}

enum Tipo {
    MOTO(800), AUTO(1500), CAMIONETA(2200);

    private final int tarifaHora;

    Tipo(int tarifaHora) {
        this.tarifaHora = tarifaHora;
    }

    public int getTarifaHora() {
        return tarifaHora;
    }
}

record Vehiculo(String patente, Tipo tipo) { }

class Cochera {
    private final int numero;
    private Vehiculo vehiculo;
    private int horaEntrada;

    Cochera(int numero) {
        this.numero = numero;
    }

    int getNumero() {
        return numero;
    }

    boolean libre() {
        return vehiculo == null;
    }

    boolean aceptaCamionetas() {
        return numero >= 5;
    }

    boolean tiene(String patente) {
        return vehiculo != null && vehiculo.patente().equals(patente);
    }

    void ocupar(Vehiculo v, int hora) {
        vehiculo = v;
        horaEntrada = hora;
    }

    int liberar(int hora) {
        int horas = Math.max(1, hora - horaEntrada);
        int importe = horas * vehiculo.tipo().getTarifaHora();
        vehiculo = null;
        return importe;
    }

    @Override
    public String toString() {
        return numero + ":" + (libre() ? "libre" : vehiculo.patente());
    }
}

class Estacionamiento {
    private final Cochera[] cocheras;

    Estacionamiento(int cantidad) {
        cocheras = new Cochera[cantidad];
        for (int i = 0; i < cantidad; i++) {
            cocheras[i] = new Cochera(i + 1);
        }
    }

    int ingresar(Vehiculo v, int hora) {
        for (Cochera c : cocheras) {
            boolean permitida = v.tipo() != Tipo.CAMIONETA || c.aceptaCamionetas();
            if (c.libre() && permitida) {
                c.ocupar(v, hora);
                return c.getNumero();
            }
        }
        return -1;
    }

    int egresar(String patente, int hora) {
        for (Cochera c : cocheras) {
            if (c.tiene(patente)) {
                return c.liberar(hora);
            }
        }
        return -1;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("Cocheras:");
        for (Cochera c : cocheras) {
            sb.append(" ").append(c);
        }
        return sb.toString();
    }
}
```

#### Pruebas

##### Estacionamiento lleno
```entrada
E AA1 AUTO 1
E AA2 AUTO 1
E AA3 AUTO 1
E AA4 AUTO 1
E AA5 AUTO 1
E AA6 AUTO 1
E AA7 MOTO 1
```
```salida
AA1 entra a la cochera 1
AA2 entra a la cochera 2
AA3 entra a la cochera 3
AA4 entra a la cochera 4
AA5 entra a la cochera 5
AA6 entra a la cochera 6
AA7: no hay cochera para MOTO
Cocheras: 1:AA1 2:AA2 3:AA3 4:AA4 5:AA5 6:AA6
Recaudación: $0
```

##### Sale lo que no está
```entrada
S ZZ999 10
```
```salida
ZZ999 no está en el estacionamiento
Cocheras: 1:libre 2:libre 3:libre 4:libre 5:libre 6:libre
Recaudación: $0
```

##### Misma hora (mínimo una hora)
```entrada
E M1 MOTO 5
S M1 5
```
```salida
M1 entra a la cochera 1
M1 sale y paga $800
Cocheras: 1:libre 2:libre 3:libre 4:libre 5:libre 6:libre
Recaudación: $800
```

### Prueba del sello

#### Al diseñar, ¿qué palabras de la consigna suelen ser clases y cuáles métodos?

Los sustantivos, clases; los verbos, métodos.

#### ¿Qué herramienta elegís para "los elementos posibles son fuego, hielo o veneno"?

Un `enum`.

#### ¿Y para "un golpe es un paquete de datos que no cambia"?

Un `record`.

#### ¿Por qué la quimera compone sus cabezas en lugar de heredar de ellas?

Porque la quimera no *es* una cabeza: *tiene* cabezas, que nacen y mueren con ella.

#### ¿Cuándo está bien usar `instanceof`?

Para capacidades opcionales (por ejemplo, si un héroe implementa `Curador`), no para reemplazar un método que debería ser polimórfico.

### Soluciones (docente)

Jefe nuevo, integrador de la unidad 1. La batalla no usa azar: si se cambian vidas o fuerzas, regenerar la salida esperada. En el legajo se atrapa `IllegalArgumentException` (que incluye `NumberFormatException` y el `valueOf` de un `enum` inexistente) con un `try`/`catch` adelantado de la rama 3.

