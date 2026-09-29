# RAMA R03 · Los Archivos Imperiales: colecciones y errores

```meta
tipo: tronco
posicion: 3
```

## R03-N01 · Paquetes, import y archivos .jar

```meta
tipo: tema
padre: R02-N11
precio: 10
criatura: skeleton
```

### Crónica

Los **Archivos Imperiales** ocupan un palacio entero: salas, pasillos, estantes con etiquetas. *Modelo*, *Servicios*, *Pantallas*. Cada pergamino tiene su sala, y para pedir uno de otra sala hay que decir su dirección completa.

—Un programa grande con todas sus clases en un solo archivo es un depósito sin estantes —dice {mentor}—. En el Imperio, cada clase vive en su **paquete**. Aprendé a ordenarlas, a compilarlas juntas y a empaquetarlas en un **jar** que cualquiera pueda ejecutar, {heroe}.

### Objetivos

- Organizar un programa en varios archivos y paquetes.
- Usar `package` e `import`, y entender el nombre completo de una clase.
- Compilar y ejecutar un proyecto con `javac -d` y `java -cp`.
- Ver en la práctica la diferencia entre `public`, `protected`, sin modificador y `private`.
- Crear un `.jar` ejecutable y usar librerías `.jar` de otros.

### Antes de empezar

- Toda la rama de objetos (La Academia de los Moldes).

### Explicación

#### Un archivo por clase pública
En un proyecto de verdad, cada clase `public` va en **su propio archivo**, con el
mismo nombre: `Heroe.java`, `Inventario.java`, `Main.java`.

#### Paquetes: carpetas de clases
Un **paquete** agrupa clases relacionadas. Se declara en la **primera línea** del
archivo, y el archivo tiene que estar en la carpeta que corresponde:
```java
// archivo src/imperio/modelo/Heroe.java
package imperio.modelo;

public class Heroe { … }
```
| Paquete | Carpeta |
|---|---|
| `imperio.modelo` | `src/imperio/modelo/` |
| `imperio.servicios` | `src/imperio/servicios/` |
| `imperio` | `src/imperio/` |

Por convención los paquetes van en minúscula y empiezan con el dominio de la
organización al revés (`ar.edu.unlar.sistemas`), para que no choquen con los de otros.

El **nombre completo** de la clase incluye el paquete: `imperio.modelo.Heroe`. Dos
clases pueden llamarse igual si están en paquetes distintos (`java.util.List` y
`java.awt.List` existen las dos).

#### `import`
Para usar una clase de **otro** paquete se importa (o se escribe el nombre completo):
```java
package imperio;

import imperio.modelo.Heroe;          // una clase
import imperio.servicios.*;           // todas las del paquete (no los subpaquetes)

public class Main { … }
```
Las clases de `java.lang` (`String`, `Math`, `System`) y las del **mismo paquete** no
necesitan `import`.

#### Compilar y ejecutar un proyecto
Desde la carpeta del proyecto (la que contiene `src/`):
```bash
javac -d out $(find src -name "*.java")     # compila todo y deja los .class en out/
java -cp out imperio.Main                   # ejecuta: -cp dice dónde buscar las clases
```
- `-d out` crea en `out/` la misma estructura de carpetas de los paquetes.
- `-cp` (*classpath*) es la lista de lugares donde Java busca clases: carpetas o
  archivos `.jar`, separados por `:` en Linux y macOS y por `;` en Windows.
- Se ejecuta con el **nombre completo** de la clase que tiene el `main`.

En Windows (PowerShell), en lugar de `$(find …)`: `javac -d out (Get-ChildItem -Recurse src -Filter *.java).FullName`.
Los IDE (NetBeans, IntelliJ, VS Code) hacen todo esto con un botón, pero conviene
saber qué pasa por debajo.

#### Los niveles de acceso, ahora sí
Con paquetes se ve la tabla completa del nodo de encapsulamiento:
```java
package imperio.modelo;
public class Heroe {
    private int vida;            // solo Heroe
    int nivel;                   // (sin modificador) todo imperio.modelo
    protected String titulo;     // imperio.modelo + las subclases de cualquier paquete
    public String nombre;        // cualquiera
}
```
Desde `imperio.Main` (otro paquete, no es subclase) solo se ve `nombre`. Desde una
subclase en otro paquete se ven `nombre` y `titulo`. Desde otra clase de
`imperio.modelo`, todo menos `vida`.

#### Archivos `.jar`
Un **`.jar`** es un zip con clases compiladas (y otros recursos). Sirve para dos cosas:
1. **Distribuir tu programa**: un jar *ejecutable* sabe cuál es su clase principal.
   ```bash
   jar --create --file imperio.jar --main-class imperio.Main -C out .
   java -jar imperio.jar
   ```
2. **Usar librerías de otros**: se agregan al classpath al compilar y al ejecutar.
   ```bash
   javac -cp lib/postgresql.jar -d out $(find src -name "*.java")
   java -cp "out:lib/postgresql.jar" imperio.Main
   ```
   Así vas a usar el driver de PostgreSQL y JUnit más adelante. Las herramientas como
   Maven o Gradle bajan las librerías solas (lo vas a ver en la Senda de Spring).

> **Si venís de C/C++.** Los paquetes cumplen el papel de los *namespaces* y de la
> organización en carpetas; `import` no copia código como `#include`: solo permite
> usar el nombre corto. Un `.jar` es parecido a una biblioteca `.a`/`.so`, pero
> multiplataforma.
>
> **Si venís de Python.** Un paquete de Java es como un paquete de Python (una
> carpeta de módulos), y `import imperio.modelo.Heroe;` es como `from imperio.modelo
> import Heroe`.

### Código de ejemplo

Un proyecto con tres paquetes. Cada bloque es un archivo, en la carpeta que indica su
`package`.

`src/imperio/modelo/Heroe.java`

```java
package imperio.modelo;

/** Un héroe del Imperio. Muestra los cuatro niveles de acceso. */
public class Heroe {
    private int vida;              // solo esta clase
    int nivel = 1;                 // todo el paquete imperio.modelo
    protected String titulo;       // el paquete y las subclases de otros paquetes
    public final String nombre;    // cualquiera

    public Heroe(String nombre, int vida) {
        this.nombre = nombre;
        this.vida = vida;
        this.titulo = "aprendiz";
    }

    public int getVida() {
        return vida;
    }

    public void recibirDanio(int danio) {
        vida = Math.max(0, vida - danio);
    }

    @Override
    public String toString() {
        return nombre + " (" + titulo + ", nivel " + nivel + ", vida " + vida + ")";
    }
}
```

`src/imperio/modelo/Academia.java`

```java
package imperio.modelo;

/** Otra clase del mismo paquete: ve lo que no es private. */
public class Academia {
    public static void ascender(Heroe h) {
        h.nivel++;                  // sin modificador: visible en el paquete
        h.titulo = "graduada";      // protected: también visible en el paquete
        // h.vida = 100;            // no compila: vida has private access in Heroe
    }
}
```

`src/imperio/servicios/Paladin.java`

```java
package imperio.servicios;

import imperio.modelo.Heroe;

/** Una subclase en OTRO paquete: ve lo protected, no lo que no tiene modificador. */
public class Paladin extends Heroe {
    public Paladin(String nombre) {
        super(nombre, 60);
        titulo = "paladín";         // protected: la subclase lo ve
        // nivel = 5;               // no compila: nivel is not public in Heroe; cannot be accessed from outside package
    }
}
```

`src/imperio/Main.java`

```java
package imperio;

import imperio.modelo.Academia;
import imperio.modelo.Heroe;
import imperio.servicios.Paladin;

public class Main {
    public static void main(String[] args) {
        Heroe kira = new Heroe("Kira", 30);
        Paladin bron = new Paladin("Bron");
        System.out.println(kira);
        System.out.println(bron);

        Academia.ascender(kira);
        kira.recibirDanio(12);
        System.out.println(kira);

        System.out.println("Nombre (public): " + kira.nombre);
        // System.out.println(kira.titulo);   // no compila: titulo has protected access in Heroe
        System.out.println("Clase completa: " + bron.getClass().getName());
    }
}
```

### Salida esperada

```
Kira (aprendiz, nivel 1, vida 30)
Bron (paladín, nivel 1, vida 60)
Kira (graduada, nivel 2, vida 18)
Nombre (public): Kira
Clase completa: imperio.servicios.Paladin
```

### ¿Para qué sirve?

Todo proyecto real está organizado en paquetes: en la facultad y en las empresas es común la estructura `modelo`, `dao`, `controlador` y `vista` (la vas a usar en la rama del escritorio). Saber compilar a mano y manejar el classpath te salva cuando el IDE falla o cuando hay que correr algo en un servidor, y los `.jar` son la forma estándar de entregar un programa Java y de usar librerías.

### Errores habituales

**Esqueleto: el `package` no coincide con la carpeta.**
```
error: class Heroe is in package imperio.modelo, but the file is in src/Heroe.java
```
O, al ejecutar: `Error: Could not find or load main class Main. Caused by:
java.lang.NoClassDefFoundError: imperio/Main (wrong name: Main)`. El archivo tiene que
estar en la carpeta del paquete, y se ejecuta con el nombre completo.

**Esqueleto: falta el `import`.** `cannot find symbol: class Heroe`. Importala o usá
el nombre completo.

**Esqueleto: una clase sin `public` usada desde otro paquete.** `Heroe is not public
in imperio.modelo; cannot be accessed from outside package`.

**Goblin: el classpath incompleto.** `NoClassDefFoundError` o
`ClassNotFoundException: org.postgresql.Driver`: falta la carpeta o el `.jar` en `-cp`.

**Ogro: `:` o `;` en el classpath.** En Linux y macOS se separa con `:` y en Windows
con `;`.

### Misión R03-N01-M1 · El proyecto de la biblioteca

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Reorganizá la misión *Del plano al código* (la biblioteca con estantes) como proyecto
con paquetes:

- `biblioteca.modelo`: `Libro`, `Novela`, `Enciclopedia`, `Prestable`.
- `biblioteca.servicios`: `Estante` y `Biblioteca`.
- `biblioteca`: `Main`.

Cada clase `public` en su archivo, con los `import` necesarios. Los atributos quedan
`private`; lo que otro paquete necesita, `public`. Entregá un `.zip` con la carpeta
`src/` y un `LEEME.txt` con los comandos para compilar y ejecutar.

#### Criterio de aprobación

- Cada clase en su archivo y en la carpeta de su paquete.
- Compila con `javac -d out` y corre con `java -cp out biblioteca.Main`.
- La salida es la misma que la de la misión original.

#### Salida esperada

```
Estante 1: Rayuela, de Cortázar | Enciclopedia del Imperio, tomo 1
Estante 2: Ficciones, de Borges | Enciclopedia del Imperio, tomo 2
Estante 3: (vacío)
Se pueden prestar: 2
```

#### Solución de referencia

`src/biblioteca/modelo/Prestable.java`

```java
package biblioteca.modelo;

public interface Prestable {
    boolean sePuedePrestar();
}
```

`src/biblioteca/modelo/Libro.java`

```java
package biblioteca.modelo;

public abstract class Libro implements Prestable {
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
```

`src/biblioteca/modelo/Novela.java`

```java
package biblioteca.modelo;

public class Novela extends Libro {
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
```

`src/biblioteca/modelo/Enciclopedia.java`

```java
package biblioteca.modelo;

public class Enciclopedia extends Libro {
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
```

`src/biblioteca/servicios/Estante.java`

```java
package biblioteca.servicios;

import biblioteca.modelo.Libro;

public class Estante {
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
```

`src/biblioteca/servicios/Biblioteca.java`

```java
package biblioteca.servicios;

import biblioteca.modelo.Libro;

public class Biblioteca {
    private final Estante[] estantes = new Estante[3];

    public Biblioteca() {
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

`src/biblioteca/Main.java`

```java
package biblioteca;

import biblioteca.modelo.Enciclopedia;
import biblioteca.modelo.Novela;
import biblioteca.servicios.Biblioteca;

public class Main {
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
```

`LEEME.txt`

```
Compilar (desde la carpeta que contiene src/):
  javac -d out $(find src -name "*.java")
Ejecutar:
  java -cp out biblioteca.Main
```

### Misión R03-N01-M2 · El jar del conversor

```meta
entrega: archivo
entorno: local
extensiones: zip, jar
monedas: 4
xp: 10
```

#### Consigna

Armá un pequeño proyecto `conversor` con dos paquetes: `conversor.unidades` (una
clase `Longitud` con métodos `static` para pasar entre metros, pies y leguas: 1 legua =
4828.03 m, 1 pie = 0.3048 m) y `conversor` (el `Main`, que recibe **por argumentos**
el valor y las unidades: `java -jar conversor.jar 10 leguas metros`). Generá un **jar
ejecutable** y entregá un `.zip` con `src/`, el `conversor.jar` y los comandos que
usaste. Si faltan argumentos, el programa explica cómo usarlo.

#### Criterio de aprobación

- El jar se ejecuta con `java -jar conversor.jar` (tiene clase principal).
- Usa `args` y valida la cantidad de argumentos.
- Muestra el resultado con 2 decimales.

#### Salida esperada

```
Uso: java -jar conversor.jar VALOR DESDE HACIA (ejemplo: 10 leguas metros)
10.00 leguas = 48280.30 metros
```

#### Solución de referencia

`src/conversor/unidades/Longitud.java`

```java
package conversor.unidades;

public final class Longitud {
    private static final double METROS_POR_PIE = 0.3048;
    private static final double METROS_POR_LEGUA = 4828.03;

    private Longitud() {
    }

    public static double aMetros(double valor, String unidad) {
        return switch (unidad) {
            case "metros" -> valor;
            case "pies" -> valor * METROS_POR_PIE;
            case "leguas" -> valor * METROS_POR_LEGUA;
            default -> throw new IllegalArgumentException("unidad desconocida: " + unidad);
        };
    }

    public static double desdeMetros(double metros, String unidad) {
        return switch (unidad) {
            case "metros" -> metros;
            case "pies" -> metros / METROS_POR_PIE;
            case "leguas" -> metros / METROS_POR_LEGUA;
            default -> throw new IllegalArgumentException("unidad desconocida: " + unidad);
        };
    }
}
```

`src/conversor/Main.java`

```java
package conversor;

import conversor.unidades.Longitud;
import java.util.Locale;

public class Main {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        if (args.length != 3) {
            args = new String[]{"10", "leguas", "metros"};   // sin argumentos: un ejemplo
            System.out.println("Uso: java -jar conversor.jar VALOR DESDE HACIA (ejemplo: 10 leguas metros)");
        }
        double valor = Double.parseDouble(args[0]);
        double metros = Longitud.aMetros(valor, args[1]);
        double resultado = Longitud.desdeMetros(metros, args[2]);
        System.out.printf("%.2f %s = %.2f %s%n", valor, args[1], resultado, args[2]);
    }
}
```

`COMANDOS.txt`

```
javac -d out $(find src -name "*.java")
jar --create --file conversor.jar --main-class conversor.Main -C out .
java -jar conversor.jar 10 leguas metros
```

### Misión R03-N01-M3 · Las puertas de los paquetes

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Esta misión se entrega pegando el texto: respondé, para el proyecto del **código de
ejemplo** de este nodo, qué pasa en cada caso (compila o no, y por qué), y después
verificalo en tu compu descomentando cada línea:

1. En `Main`: `System.out.println(kira.titulo);`
2. En `Academia`: `h.vida = 100;`
3. En `Paladin`: `nivel = 5;`
4. En `Paladin`: `System.out.println(nombre);`
5. En `Main`: `System.out.println(new Academia());` (Academia es `public`, pero no tiene constructor escrito).

Escribí las respuestas como comentarios dentro de una clase Java que compile.

#### Criterio de aprobación

- Las cinco respuestas son correctas y explican el nivel de acceso involucrado.

#### Salida esperada

```
1 no, 2 no, 3 no, 4 sí, 5 sí
```

#### Solución de referencia

```java
// Mision 3 - Las puertas de los paquetes: respuestas como comentarios.
public class Respuestas {
    public static void main(String[] args) {
        // 1. No compila: titulo es protected; Main no es subclase ni está en imperio.modelo.
        // 2. No compila: vida es private; solo la ve la clase Heroe.
        // 3. No compila: nivel no tiene modificador (paquete) y Paladin está en otro paquete,
        //    aunque sea subclase.
        // 4. Compila: nombre es public.
        // 5. Compila: Academia es public y, al no escribir constructores, tiene el constructor
        //    por defecto, que es public como la clase.
        System.out.println("1 no, 2 no, 3 no, 4 sí, 5 sí");
    }
}
```

### Encargo R03-N01-E1 · La librería de validaciones

```meta
entrega: archivo
entorno: local
extensiones: zip, jar
monedas: 1
xp: 15
```

#### Consigna

Muchos sistemas validan DNI, CUIT y emails. Escribí una **librería**: un proyecto con
el paquete `ar.validaciones` y una clase `Validador` con métodos `static`
(`dniValido`, `cuitValido`, `emailValido`). Empaquetala en `validaciones.jar` (sin
clase principal). Después, en **otro proyecto aparte**, escribí un `Main` que use la
librería agregando el jar al classpath al compilar y al ejecutar. Entregá un `.zip`
con los dos proyectos y los comandos.

#### Criterio de aprobación

- La librería es un jar sin `main`.
- El segundo proyecto la usa con `-cp`.

#### Solución de referencia

`libreria/src/ar/validaciones/Validador.java`

```java
package ar.validaciones;

public final class Validador {
    private Validador() {
    }

    public static boolean dniValido(String dni) {
        return dni != null && dni.replace(".", "").matches("\\d{7,8}");
    }

    public static boolean emailValido(String email) {
        return email != null && email.matches("[\\w.+-]+@[\\w-]+(\\.[\\w-]+)+");
    }

    public static boolean cuitValido(String cuit) {
        if (cuit == null) {
            return false;
        }
        String d = cuit.replace("-", "");
        if (!d.matches("\\d{11}")) {
            return false;
        }
        int[] pesos = {5, 4, 3, 2, 7, 6, 5, 4, 3, 2};
        int suma = 0;
        for (int i = 0; i < 10; i++) {
            suma += (d.charAt(i) - '0') * pesos[i];
        }
        int v = 11 - suma % 11;
        v = v == 11 ? 0 : v;
        return v != 10 && v == d.charAt(10) - '0';
    }
}
```

`app/src/app/Main.java`

```java
package app;

import ar.validaciones.Validador;

public class Main {
    public static void main(String[] args) {
        System.out.println("DNI 30.111.222: " + Validador.dniValido("30.111.222"));
        System.out.println("Email ana@correo.com: " + Validador.emailValido("ana@correo.com"));
        System.out.println("CUIT 20-12345678-6: " + Validador.cuitValido("20-12345678-6"));
    }
}
```

`COMANDOS.txt`

```
# Librería
cd libreria
javac -d out $(find src -name "*.java")
jar --create --file validaciones.jar -C out .
# Aplicación que la usa
cd ../app
javac -cp ../libreria/validaciones.jar -d out $(find src -name "*.java")
java -cp "out:../libreria/validaciones.jar" app.Main
```

### Prueba del sello

#### ¿Dónde tiene que estar el archivo de una clase del paquete `imperio.modelo`?

En la carpeta `imperio/modelo/` (dentro de `src/`), y su primera línea es `package imperio.modelo;`.

#### ¿Qué clases se pueden usar sin `import`?

Las de `java.lang` y las del mismo paquete.

#### ¿Quién ve un atributo sin modificador de acceso?

Solo las clases del mismo paquete (ni siquiera las subclases de otro paquete).

#### ¿Qué hace `-cp` al ejecutar `java`?

Indica dónde buscar las clases: carpetas y archivos `.jar`.

#### ¿Qué diferencia hay entre un jar ejecutable y una librería?

El ejecutable indica su clase principal y se corre con `java -jar`; la librería no tiene `main` y se agrega al classpath de otro programa.

### Soluciones (docente)

Sale de `18-Java/19-Paquetes-Jar` (unidad 2: paquetes y librerías). Demuestra con código real la diferencia entre `protected` y sin modificador que la auditoría pedía. La salida esperada de la misión 2 es la del ejemplo que el `Main` usa cuando no recibe argumentos.

## R03-N02 · ArrayList y genéricos

```meta
tipo: tema
padre: R03-N01
precio: 10
criatura: orc
```

### Crónica

El archivista del ala norte está desesperado: le dieron un estante con 10 lugares fijos y ya tiene 14 pergaminos. Para agregar uno tiene que pedir un estante nuevo, copiar todo y tirar el viejo.

—Los arrays tienen tamaño fijo —dice {mentor}—. Para las colecciones que crecen y se achican, el Imperio tiene **listas**. Y gracias a los **genéricos**, una lista de pergaminos solo acepta pergaminos, {heroe}: la Aduana lo controla al compilar.

### Objetivos

- Usar `ArrayList` para guardar colecciones que cambian de tamaño.
- Declarar con la interfaz `List` y entender los genéricos (`List<String>`).
- Usar las clases envoltorio (`Integer`, `Double`) y el autoboxing.
- Recorrer, buscar, ordenar y borrar elementos de una lista sin errores.
- Escribir una clase genérica propia.

### Antes de empezar

- Paquetes, import y archivos .jar.
- Interfaces y `Comparable` (Interfaces: contratos).

### Explicación

#### `ArrayList`: un array que crece
```java
import java.util.ArrayList;
import java.util.List;

List<String> pergaminos = new ArrayList<>();
pergaminos.add("Mapa del norte");         // agrega al final
pergaminos.add("Tratado de paz");
pergaminos.add(0, "Índice");              // agrega en una posición
pergaminos.get(1);                        // "Mapa del norte"
pergaminos.set(1, "Mapa del sur");        // reemplaza
pergaminos.size();                        // 3
pergaminos.remove("Tratado de paz");      // borra por valor (con equals)
pergaminos.remove(0);                     // borra por posición
pergaminos.contains("Mapa del sur");      // true
pergaminos.indexOf("Mapa del sur");       // 0
pergaminos.isEmpty();
pergaminos.clear();
```
La lista crece sola: no hay que saber de antemano cuántos elementos va a tener.

#### Declarar con la interfaz
`List` es una **interfaz** y `ArrayList` una de sus implementaciones. Conviene declarar
la variable con la interfaz (`List<String> x = new ArrayList<>();`): así el resto del
código no depende de cuál es, y se puede cambiar por otra (`LinkedList`) sin tocar
nada más. Es el mismo principio de "programar contra interfaces" de la rama anterior.

`Vector` es la versión vieja de `ArrayList` (de antes de Java 2): funciona igual pero es
más lenta porque está sincronizada para varios hilos. En código nuevo se usa `ArrayList`.

#### Genéricos: `<Tipo>`
Lo que va entre `< >` es el **tipo de los elementos**. El compilador lo controla:
```java
List<String> nombres = new ArrayList<>();
nombres.add("Kira");
nombres.add(42);                 // no compila: incompatible types: int cannot be converted to String
String primero = nombres.get(0); // sin casting: el compilador sabe que es un String
```
El `<>` vacío del `new ArrayList<>()` (el "diamante") deja que Java deduzca el tipo.
Esto es el **polimorfismo paramétrico** que nombramos en la rama anterior: el mismo
código de `ArrayList` sirve para cualquier tipo.

#### Los primitivos no entran: clases envoltorio
Los genéricos funcionan con **objetos**, no con primitivos. Por eso existen clases
envoltorio: `Integer` para `int`, `Double` para `double`, `Boolean`, `Character`,
`Long`.
```java
List<Integer> puntajes = new ArrayList<>();     // List<int> no compila
puntajes.add(90);                                // autoboxing: el int 90 se envuelve en un Integer
int primero = puntajes.get(0);                   // unboxing: el Integer se desenvuelve
```
Dos trampas de los envoltorios:
- `puntajes.remove(1)` borra la **posición** 1; para borrar el **valor** 1:
  `puntajes.remove(Integer.valueOf(1))`.
- Entre `Integer` no uses `==`: compara objetos. Con valores chicos (de -128 a 127)
  suele funcionar por casualidad, y con más grandes falla. Usá `equals` o pasalos a
  `int`.

#### Recorrer
```java
for (String p : pergaminos) {                   // for-each: lo más común
    System.out.println(p);
}
for (int i = 0; i < pergaminos.size(); i++) {   // con índice
    System.out.println(i + ": " + pergaminos.get(i));
}
```
**No borres elementos dentro de un for-each**: corta con
`ConcurrentModificationException`. Para borrar mientras recorrés, usá un `Iterator` o
`removeIf` (este último con lambdas, dos nodos más adelante):
```java
Iterator<String> it = pergaminos.iterator();
while (it.hasNext()) {
    if (it.next().startsWith("Borrador")) {
        it.remove();
    }
}
```

#### Ordenar
Con `Collections` (`import java.util.Collections;`):
```java
Collections.sort(nombres);           // orden natural (Comparable): alfabético, números de menor a mayor
Collections.reverse(nombres);
Collections.max(puntajes);
Collections.shuffle(lista, new Random(7));   // mezclar con semilla
```
Si los elementos son objetos tuyos, tienen que ser `Comparable` (o se pasa un
`Comparator`, que vas a ver con las lambdas).

Los textos se ordenan por el **código** de cada carácter, no como en el diccionario:
las mayúsculas van antes que las minúsculas y las letras con tilde, después de la `z`
(`"Índice"` queda al final). Para un orden alfabético en español se usa un `Collator`:
`lista.sort(Collator.getInstance(Locale.forLanguageTag("es")));` (con `import java.text.Collator;`).

#### Crear listas cortas
`List.of("a", "b", "c")` crea una lista **inmutable** (no se le puede agregar ni
quitar). Para una modificable a partir de ella: `new ArrayList<>(List.of(...))`.

#### Clases genéricas propias
Una clase puede recibir un tipo como parámetro:
```java
class Caja<T> {
    private T contenido;
    void guardar(T cosa) { contenido = cosa; }
    T sacar() { return contenido; }
}
Caja<String> c1 = new Caja<>();
Caja<Integer> c2 = new Caja<>();
```
`T` es un nombre para "el tipo que elija quien use la clase".

> **Si venís de Python.** `ArrayList` es la `list` de Python, pero con un solo tipo de
> elemento y sin índices negativos ni *slicing* (hay `subList(desde, hasta)`).
>
> **Si venís de C++.** `List<T>` y `ArrayList<T>` son como `std::vector<T>`, pero los
> genéricos de Java solo aceptan objetos (de ahí los envoltorios).

### Código de ejemplo

```java
/*
 * ArrayList y genéricos: el archivo del ala norte.
 */
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;

public class AlaNorte {
    public static void main(String[] args) {
        List<String> pergaminos = new ArrayList<>();
        pergaminos.add("Mapa del norte");
        pergaminos.add("Tratado de paz");
        pergaminos.add("Borrador de ley");
        pergaminos.add(0, "Índice");
        System.out.println(pergaminos + " (" + pergaminos.size() + ")");

        pergaminos.set(1, "Mapa del sur");
        System.out.println("¿Está el tratado? " + pergaminos.contains("Tratado de paz") + ", en la posición " + pergaminos.indexOf("Tratado de paz"));

        // Borrar mientras se recorre: con un Iterator
        Iterator<String> it = pergaminos.iterator();
        while (it.hasNext()) {
            if (it.next().startsWith("Borrador")) {
                it.remove();
            }
        }
        Collections.sort(pergaminos);
        System.out.println("Ordenados: " + pergaminos);

        // Envoltorios y autoboxing
        List<Integer> puntajes = new ArrayList<>(List.of(90, 45, 300, 1, 72));
        puntajes.add(18);                                // autoboxing
        int suma = 0;
        for (int p : puntajes) {                         // unboxing
            suma += p;
        }
        System.out.println("Puntajes " + puntajes + ", suma " + suma + ", máximo " + Collections.max(puntajes));
        puntajes.remove(1);                              // borra la POSICIÓN 1 (el 45)
        puntajes.remove(Integer.valueOf(1));             // borra el VALOR 1
        System.out.println("Después de borrar: " + puntajes);

        Integer a = 300;
        Integer b = 300;
        System.out.println("300 == 300 con Integer: " + (a == b) + ", con equals: " + a.equals(b));

        // Una lista de objetos propios
        List<Heroe> grupo = new ArrayList<>();
        grupo.add(new Heroe("Kira", 3));
        grupo.add(new Heroe("Bron", 5));
        grupo.add(new Heroe("Lía", 2));
        Collections.sort(grupo);                          // Heroe es Comparable
        System.out.println("Por nivel: " + grupo);

        // Una clase genérica propia
        Caja<String> cofre = new Caja<>("una llave");
        Caja<Integer> bolsa = new Caja<>(250);
        System.out.println("En el cofre hay " + cofre.ver() + "; en la bolsa, " + (bolsa.ver() + 50) + " denarios");
    }
}

class Heroe implements Comparable<Heroe> {
    private final String nombre;
    private final int nivel;

    Heroe(String nombre, int nivel) {
        this.nombre = nombre;
        this.nivel = nivel;
    }

    @Override
    public int compareTo(Heroe otro) {
        return Integer.compare(nivel, otro.nivel);
    }

    @Override
    public String toString() {
        return nombre + " " + nivel;
    }
}

class Caja<T> {
    private final T contenido;

    Caja(T contenido) {
        this.contenido = contenido;
    }

    T ver() {
        return contenido;
    }
}
```

### Salida esperada

```
[Índice, Mapa del norte, Tratado de paz, Borrador de ley] (4)
¿Está el tratado? true, en la posición 2
Ordenados: [Mapa del sur, Tratado de paz, Índice]
Puntajes [90, 45, 300, 1, 72, 18], suma 526, máximo 300
Después de borrar: [90, 300, 72, 18]
300 == 300 con Integer: false, con equals: true
Por nivel: [Lía 2, Kira 3, Bron 5]
En el cofre hay una llave; en la bolsa, 300 denarios
```

### ¿Para qué sirve?

Las listas son la estructura de datos más usada en cualquier programa Java: los productos de un carrito, los alumnos de un curso, las filas que devuelve una consulta a la base de datos, los enemigos de un nivel. Los genéricos hacen que esos programas sean seguros: el compilador impide mezclar tipos y evita los castings.

### Errores habituales

**Orco: la posición que no existe.**
```
Exception in thread "main" java.lang.IndexOutOfBoundsException: Index 3 out of bounds for length 3
```
Las posiciones van de `0` a `size() - 1`.

**Troll: borrar dentro de un for-each.**
`java.util.ConcurrentModificationException`. Usá un `Iterator` con `it.remove()` o
`removeIf`.

**Goblin: `List<int>`.** `unexpected type; required: reference; found: int`. Va
`List<Integer>`.

**Ogro: `remove(1)` en una lista de `Integer`.** Borra la posición 1, no el valor 1.

**Ogro: comparar `Integer` con `==`.** Con valores grandes da `false` aunque sean
iguales. Usá `equals`.

**Goblin: modificar una lista de `List.of`.** `UnsupportedOperationException`: es
inmutable. Creá un `new ArrayList<>(List.of(...))`.

### Misión R03-N02-M1 · La lista de compras de la posada

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé comandos hasta `fin` para manejar la lista de compras de la posada:
`agregar ITEM`, `quitar ITEM`, `ver` y `ordenar`. No se agregan items repetidos (se
avisa) y quitar uno que no está también se avisa. Al final mostrá la lista y cuántos
items tiene.

#### Criterio de aprobación

- Usa `List<String>` con `ArrayList`.
- Usa `contains`, `remove` y `Collections.sort`.

#### Entrada de ejemplo

```
agregar harina
agregar huevos
agregar café
agregar harina
ver
quitar sal
quitar huevos
agregar azúcar
ordenar
fin
```

#### Salida esperada

```
harina ya está en la lista
Lista: [harina, huevos, café]
sal no estaba en la lista
Final: [azúcar, café, harina] (3 items)
```

#### Solución de referencia

```java
// Mision 1 - La lista de compras: ArrayList con comandos.
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;

public class Compras {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        List<String> lista = new ArrayList<>();
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.equals("fin")) {
                break;
            }
            String[] partes = linea.split(" ", 2);
            switch (partes[0]) {
                case "agregar" -> {
                    if (lista.contains(partes[1])) {
                        System.out.println(partes[1] + " ya está en la lista");
                    } else {
                        lista.add(partes[1]);
                    }
                }
                case "quitar" -> {
                    if (!lista.remove(partes[1])) {
                        System.out.println(partes[1] + " no estaba en la lista");
                    }
                }
                case "ver" -> System.out.println("Lista: " + lista);
                case "ordenar" -> Collections.sort(lista);
                default -> System.out.println("Comando desconocido: " + partes[0]);
            }
        }
        System.out.println("Final: " + lista + " (" + lista.size() + " items)");
    }
}
```

### Misión R03-N02-M2 · Los puntajes del torneo

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé puntajes enteros (uno por línea) hasta una línea vacía y guardalos en un
`List<Integer>`. Mostrá: la lista, el promedio (un decimal), el máximo y el mínimo con
`Collections`, cuántos superan el promedio, la lista **sin los puntajes menores a
50** (borrando con un `Iterator`) y los tres mejores.

#### Criterio de aprobación

- Usa `List<Integer>` y `Collections.max`/`min`.
- Borra con `Iterator` (no en un for-each).

#### Entrada de ejemplo

```
120
35
88
47
210
99

```

#### Salida esperada

```
Puntajes: [120, 35, 88, 47, 210, 99]
Promedio: 99.8
Máximo: 210, mínimo: 35
Superan el promedio: 2
Sin los menores a 50: [120, 88, 210, 99]
Los tres mejores: [210, 120, 99]
```

#### Solución de referencia

```java
// Mision 2 - Los puntajes del torneo: List<Integer>, Collections e Iterator.
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.Locale;
import java.util.Scanner;

public class Torneo {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Scanner teclado = new Scanner(System.in);
        List<Integer> puntajes = new ArrayList<>();
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.isEmpty()) {
                break;
            }
            puntajes.add(Integer.parseInt(linea));
        }
        double suma = 0;
        for (int p : puntajes) {
            suma += p;
        }
        double promedio = suma / puntajes.size();
        int sobre = 0;
        for (int p : puntajes) {
            if (p > promedio) {
                sobre++;
            }
        }
        System.out.println("Puntajes: " + puntajes);
        System.out.printf("Promedio: %.1f%n", promedio);
        System.out.println("Máximo: " + Collections.max(puntajes) + ", mínimo: " + Collections.min(puntajes));
        System.out.println("Superan el promedio: " + sobre);

        Iterator<Integer> it = puntajes.iterator();
        while (it.hasNext()) {
            if (it.next() < 50) {
                it.remove();
            }
        }
        System.out.println("Sin los menores a 50: " + puntajes);

        List<Integer> ordenados = new ArrayList<>(puntajes);
        Collections.sort(ordenados);
        Collections.reverse(ordenados);
        System.out.println("Los tres mejores: " + ordenados.subList(0, Math.min(3, ordenados.size())));
    }
}
```

### Misión R03-N02-M3 · El cofre genérico

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase genérica `Estante<T>` que guarda una lista de elementos de tipo `T`
con una **capacidad máxima**. Métodos: `boolean poner(T cosa)` (falso si está lleno),
`T sacarUltimo()` (devuelve `null` si está vacío), `int cantidad()`, `boolean
lleno()` y `toString`. Usala con un `Estante<String>` de pociones y un
`Estante<Integer>` de monedas; sumá las monedas después de sacarlas.

#### Criterio de aprobación

- `Estante<T>` usa una `List<T>` por dentro.
- Se usa con dos tipos distintos sin castings.

#### Salida esperada

```
true true false
Pociones: [vida, furia], ¿lleno? true
Saco: furia
Total de monedas: 40, estante vacío: [], saco otra: null
```

#### Solución de referencia

```java
// Mision 3 - El cofre generico: una clase Estante<T>.
import java.util.ArrayList;
import java.util.List;

public class Estantes {
    public static void main(String[] args) {
        Estante<String> pociones = new Estante<>(2);
        System.out.println(pociones.poner("vida") + " " + pociones.poner("furia") + " " + pociones.poner("sueño"));
        System.out.println("Pociones: " + pociones + ", ¿lleno? " + pociones.lleno());
        System.out.println("Saco: " + pociones.sacarUltimo());

        Estante<Integer> monedas = new Estante<>(5);
        monedas.poner(10);
        monedas.poner(25);
        monedas.poner(5);
        int total = 0;
        while (monedas.cantidad() > 0) {
            total += monedas.sacarUltimo();
        }
        System.out.println("Total de monedas: " + total + ", estante vacío: " + monedas + ", saco otra: " + monedas.sacarUltimo());
    }
}

class Estante<T> {
    private final List<T> cosas = new ArrayList<>();
    private final int capacidad;

    Estante(int capacidad) {
        this.capacidad = capacidad;
    }

    boolean poner(T cosa) {
        if (lleno()) {
            return false;
        }
        cosas.add(cosa);
        return true;
    }

    T sacarUltimo() {
        if (cosas.isEmpty()) {
            return null;
        }
        return cosas.remove(cosas.size() - 1);
    }

    int cantidad() {
        return cosas.size();
    }

    boolean lleno() {
        return cosas.size() == capacidad;
    }

    @Override
    public String toString() {
        return cosas.toString();
    }
}
```

### Encargo R03-N02-E1 · La fila del banco

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Simulá la fila de un banco con una `List<String>`: los comandos son `llega NOMBRE`
(se pone al final), `prioridad NOMBRE` (se pone al principio: embarazadas, mayores),
`atender` (atiende al primero y lo saca) y `se-va NOMBRE` (se cansó de esperar). Al
final mostrá a quién se atendió, en orden, y quiénes quedaron esperando.

#### Criterio de aprobación

- Usa `add`, `add(0, …)`, `remove(0)` y `remove(Object)`.
- Maneja `atender` con la fila vacía.

#### Entrada de ejemplo

```
llega Marta
llega Juan
prioridad Doña Rosa
atender
llega Ana
se-va Juan
atender
atender
atender
llega Leo

```

#### Salida esperada

```
Atendiendo a Doña Rosa
Atendiendo a Marta
Atendiendo a Ana
No hay nadie para atender
Atendidos: [Doña Rosa, Marta, Ana]
Esperando: [Leo]
```

#### Solución de referencia

```java
// Encargo - La fila del banco: una lista usada como cola con prioridades.
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class FilaBanco {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        List<String> fila = new ArrayList<>();
        List<String> atendidos = new ArrayList<>();
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.isEmpty()) {
                break;
            }
            String[] p = linea.split(" ", 2);
            switch (p[0]) {
                case "llega" -> fila.add(p[1]);
                case "prioridad" -> fila.add(0, p[1]);
                case "se-va" -> fila.remove(p[1]);
                case "atender" -> {
                    if (fila.isEmpty()) {
                        System.out.println("No hay nadie para atender");
                    } else {
                        String persona = fila.remove(0);
                        atendidos.add(persona);
                        System.out.println("Atendiendo a " + persona);
                    }
                }
                default -> System.out.println("?");
            }
        }
        System.out.println("Atendidos: " + atendidos);
        System.out.println("Esperando: " + fila);
    }
}
```

### Prueba del sello

#### ¿Qué ventaja tiene un `ArrayList` sobre un array?

Cambia de tamaño solo: se agregan y quitan elementos sin saber de antemano cuántos van a ser.

#### ¿Por qué se declara `List<String> x = new ArrayList<>();` y no `ArrayList<String>`?

Para programar contra la interfaz: el resto del código no depende de la implementación y se puede cambiar.

#### ¿Por qué no existe `List<int>`?

Porque los genéricos trabajan con objetos; para enteros se usa `List<Integer>` y el autoboxing convierte solo.

#### En una `List<Integer>`, ¿qué borra `lista.remove(2)`?

El elemento de la posición 2, no el valor 2.

#### ¿Cómo se borran elementos mientras se recorre una lista?

Con un `Iterator` y `it.remove()`, o con `removeIf`; nunca con `remove` dentro de un for-each.

### Soluciones (docente)

Nodo nuevo (el 20 del índice de `18-Java` estaba por crear), con la parte de `ArrayList` que el capítulo original tenía en el viejo 10. Incluye `Vector` porque lo nombra el programa de la unidad 4. La comparación de `Integer` con `==` usa 300 a propósito (fuera de la caché de -128 a 127): da `false` en cualquier JVM estándar.

## R03-N03 · Mapas y conjuntos: HashMap y HashSet

```meta
tipo: tema
padre: R03-N02
precio: 10
criatura: troll
```

### Crónica

En el ala sur de los Archivos no hay estantes numerados: hay **fichas**. Cada ficha tiene una etiqueta (el nombre de una ciudad) y, detrás, todo lo que se sabe de ella. El archivista no busca de a uno: va directo a la ficha que necesita.

—Una lista sirve cuando te importa el orden —dice {mentor}—. Cuando querés **buscar por una clave**, usá un **mapa**. Y cuando lo único que te importa es si algo está o no, sin repetidos, un **conjunto**, {heroe}.

### Objetivos

- Guardar pares clave-valor en un `Map` (`HashMap`, `TreeMap`, `LinkedHashMap`).
- Buscar, actualizar, contar y recorrer un mapa.
- Guardar elementos sin repetidos en un `Set` (`HashSet`, `TreeSet`).
- Elegir la colección adecuada para cada problema.

### Antes de empezar

- ArrayList y genéricos.
- `equals` y `hashCode` (Referencias, null y equals).

### Explicación

#### `Map`: claves y valores
Un mapa asocia cada **clave** con un **valor**. Las claves no se repiten.
```java
import java.util.HashMap;
import java.util.Map;

Map<String, Integer> poblacion = new HashMap<>();
poblacion.put("Capital", 120_000);          // agrega (o reemplaza si ya estaba)
poblacion.put("Puerto", 45_000);
poblacion.get("Capital");                   // 120000
poblacion.get("Atlántida");                 // null: no existe
poblacion.getOrDefault("Atlántida", 0);     // 0
poblacion.containsKey("Puerto");            // true
poblacion.remove("Puerto");
poblacion.size();
```

#### Contar con un mapa
El uso más común: contar cuántas veces aparece cada cosa.
```java
Map<String, Integer> conteo = new HashMap<>();
for (String palabra : palabras) {
    conteo.put(palabra, conteo.getOrDefault(palabra, 0) + 1);
}
// o, más corto:
conteo.merge(palabra, 1, Integer::sum);     // suma 1 al valor actual (o pone 1)
```

#### Recorrer un mapa
```java
for (String ciudad : poblacion.keySet()) { … }            // las claves
for (int habitantes : poblacion.values()) { … }           // los valores
for (Map.Entry<String, Integer> e : poblacion.entrySet()) {   // los pares
    System.out.println(e.getKey() + ": " + e.getValue());
}
```

#### El orden: tres mapas
| Clase | Orden al recorrer | Uso |
|---|---|---|
| `HashMap` | ninguno garantizado | el más rápido; cuando el orden no importa |
| `LinkedHashMap` | el orden en que se agregaron | cuando querés respetar el orden de llegada |
| `TreeMap` | ordenado por clave | cuando querés las claves ordenadas (alfabético, de menor a mayor) |

Ojo: el orden de un `HashMap` **no es el de inserción** y puede cambiar entre versiones
de Java. Si un programa necesita un orden (para mostrar un reporte), usá `TreeMap` o
`LinkedHashMap`.

#### `Set`: sin repetidos
Un conjunto guarda elementos **sin repetir**, sin posiciones:
```java
Set<String> visitadas = new HashSet<>();
visitadas.add("Capital");        // true: se agregó
visitadas.add("Capital");        // false: ya estaba
visitadas.contains("Puerto");    // búsqueda muy rápida
visitadas.size();
```
`TreeSet` los guarda ordenados y `LinkedHashSet` respeta el orden de llegada.
Operaciones de conjuntos: `a.addAll(b)` (unión), `a.retainAll(b)` (intersección),
`a.removeAll(b)` (diferencia).

#### Objetos propios como clave o en un `Set`
`HashMap` y `HashSet` usan **`hashCode` y `equals`** para saber si dos claves son la
misma. Si usás objetos tuyos, tienen que redefinir los dos (como viste en el nodo de
referencias), o dos objetos "iguales" van a aparecer repetidos. Los `record` ya los
traen bien hechos.

#### Qué colección elegir
| Necesito… | Uso |
|---|---|
| una secuencia ordenada por posición, con repetidos | `List` (`ArrayList`) |
| buscar un valor a partir de una clave | `Map` (`HashMap`) |
| saber si algo está, sin repetidos | `Set` (`HashSet`) |
| lo mismo, pero recorrerlo ordenado | `TreeMap` / `TreeSet` |
| respetar el orden en que llegaron | `LinkedHashMap` / `LinkedHashSet` |

> **Si venís de Python.** `HashMap` es el `dict` y `HashSet` el `set`. A diferencia del
> `dict` de Python moderno, un `HashMap` **no** conserva el orden de inserción: para eso
> está `LinkedHashMap`.

### Código de ejemplo

```java
/*
 * Mapas y conjuntos: las fichas del ala sur.
 */
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;

public class AlaSur {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);                     // %,d agrupa los miles con coma
        // Un mapa ordenado por clave
        Map<String, Integer> poblacion = new TreeMap<>();
        poblacion.put("Puerto", 45_000);
        poblacion.put("Capital", 120_000);
        poblacion.put("Frontera", 8_000);
        poblacion.put("Capital", 125_000);              // reemplaza el valor
        System.out.println(poblacion);
        System.out.println("Capital: " + poblacion.get("Capital") + ", Atlántida: " + poblacion.getOrDefault("Atlántida", 0));

        int total = 0;
        for (Map.Entry<String, Integer> e : poblacion.entrySet()) {
            System.out.printf("  %-9s %,8d%n", e.getKey(), e.getValue());
            total += e.getValue();
        }
        System.out.printf("  %-9s %,8d%n", "Total", total);

        // Contar palabras respetando el orden de aparición
        String texto = "el dragón vio el castillo y el castillo vio al dragón";
        Map<String, Integer> conteo = new LinkedHashMap<>();
        for (String palabra : texto.split(" ")) {
            conteo.merge(palabra, 1, Integer::sum);
        }
        System.out.println("Conteo: " + conteo);

        // Conjuntos
        Set<String> visitoKira = new TreeSet<>(Set.of("Capital", "Puerto", "Frontera"));
        Set<String> visitoBron = new TreeSet<>(Set.of("Puerto", "Montaña", "Capital"));
        Set<String> ambos = new TreeSet<>(visitoKira);
        ambos.retainAll(visitoBron);
        Set<String> alguno = new TreeSet<>(visitoKira);
        alguno.addAll(visitoBron);
        Set<String> soloKira = new TreeSet<>(visitoKira);
        soloKira.removeAll(visitoBron);
        System.out.println("Visitaron los dos: " + ambos);
        System.out.println("Visitó alguno: " + alguno);
        System.out.println("Solo Kira: " + soloKira);

        // Sin repetidos: con un record como elemento (trae equals y hashCode)
        Set<Posicion> pisadas = new HashSet<>();
        pisadas.add(new Posicion(2, 3));
        pisadas.add(new Posicion(2, 4));
        boolean nueva = pisadas.add(new Posicion(2, 3));
        System.out.println("¿(2,3) era nueva? " + nueva + " | casillas pisadas: " + pisadas.size());
    }
}

record Posicion(int x, int y) { }
```

### Salida esperada

```
{Capital=125000, Frontera=8000, Puerto=45000}
Capital: 125000, Atlántida: 0
  Capital    125,000
  Frontera     8,000
  Puerto      45,000
  Total      178,000
Conteo: {el=3, dragón=2, vio=2, castillo=2, y=1, al=1}
Visitaron los dos: [Capital, Puerto]
Visitó alguno: [Capital, Frontera, Montaña, Puerto]
Solo Kira: [Frontera]
¿(2,3) era nueva? false | casillas pisadas: 2
```

### ¿Para qué sirve?

Los mapas están en todos lados: el stock por código de producto, el precio por moneda, las notas por legajo, la configuración por nombre de opción, el caché de consultas. Contar con un mapa (palabras, ventas por vendedor, votos por candidato) es uno de los problemas más comunes de la programación. Los conjuntos evitan duplicados (emails de una lista de difusión) y responden rapidísimo "¿esto ya está?".

### Errores habituales

**Troll: el `null` de `get`.** `int n = mapa.get("x");` con una clave inexistente
corta con `NullPointerException` (no se puede pasar `null` a `int`). Usá
`getOrDefault` o `containsKey`.

**Ogro: esperar el orden de inserción en un `HashMap`.** El orden no está garantizado.
Usá `LinkedHashMap` o `TreeMap`.

**Ogro: objetos propios sin `equals`/`hashCode`.** En un `HashSet` aparecen repetidos
y en un `HashMap` no se encuentran por clave. Redefinilos (o usá un `record`).

**Troll: modificar un mapa mientras se lo recorre.** `ConcurrentModificationException`,
como con las listas. Para borrar mientras recorrés: `mapa.entrySet().removeIf(...)`.

**Goblin: `TreeMap` con claves que no son comparables.** `ClassCastException: class X
cannot be cast to class java.lang.Comparable`: las claves de un `TreeMap` tienen que
ser `Comparable`.

### Misión R03-N03-M1 · El censo de criaturas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Los exploradores reportan criaturas vistas, una por línea, con el formato
`criatura cantidad` (por ejemplo `goblin 3`), hasta una línea vacía. Una criatura puede
aparecer varias veces. Usá un `TreeMap<String, Integer>` para sumar los avistajes por
criatura y mostrá el censo ordenado alfabéticamente, el total y la criatura más vista.

#### Criterio de aprobación

- Acumula con `merge` o `getOrDefault`.
- Muestra el censo ordenado (por usar `TreeMap`).

#### Entrada de ejemplo

```
goblin 3
slime 12
troll 1
goblin 4
slime 2
orco 5

```

#### Salida esperada

```
goblin: 7
orco: 5
slime: 14
troll: 1
Total: 27
La más vista: slime
```

#### Solución de referencia

```java
// Mision 1 - El censo de criaturas: sumar por clave con un TreeMap.
import java.util.Map;
import java.util.Scanner;
import java.util.TreeMap;

public class Censo {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        Map<String, Integer> censo = new TreeMap<>();
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.isEmpty()) {
                break;
            }
            String[] p = linea.split(" ");
            censo.merge(p[0], Integer.parseInt(p[1]), Integer::sum);
        }
        int total = 0;
        String masVista = null;
        for (Map.Entry<String, Integer> e : censo.entrySet()) {
            System.out.println(e.getKey() + ": " + e.getValue());
            total += e.getValue();
            if (masVista == null || e.getValue() > censo.get(masVista)) {
                masVista = e.getKey();
            }
        }
        System.out.println("Total: " + total);
        System.out.println("La más vista: " + masVista);
    }
}
```

### Misión R03-N03-M2 · Los invitados del banquete

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Dos casas nobles mandan su lista de invitados al banquete (dos líneas, con nombres
separados por comas). Con conjuntos (`TreeSet`), mostrá: todos los invitados sin
repetir (unión), los que están en las dos listas, los que invitó solo la primera casa y
cuántos lugares hay que preparar. Los nombres se comparan sin importar mayúsculas ni
espacios (pasalos a un formato común antes de guardarlos).

#### Criterio de aprobación

- Usa `addAll`, `retainAll` y `removeAll` sobre copias.
- Normaliza los nombres antes de guardarlos.

#### Entrada de ejemplo

```
Kira, Bron, lía, Olmo, Nara
bron, Tesla, Kira , Pip
```

#### Salida esperada

```
Todos: [Bron, Kira, Lía, Nara, Olmo, Pip, Tesla]
Invitados por las dos casas: [Bron, Kira]
Solo de la primera casa: [Lía, Nara, Olmo]
Lugares a preparar: 7
```

#### Solución de referencia

```java
// Mision 2 - Los invitados del banquete: union, interseccion y diferencia con TreeSet.
import java.util.Scanner;
import java.util.Set;
import java.util.TreeSet;

public class Banquete {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        Set<String> casa1 = leerLista(teclado.nextLine());
        Set<String> casa2 = leerLista(teclado.nextLine());

        Set<String> todos = new TreeSet<>(casa1);
        todos.addAll(casa2);
        Set<String> ambas = new TreeSet<>(casa1);
        ambas.retainAll(casa2);
        Set<String> soloPrimera = new TreeSet<>(casa1);
        soloPrimera.removeAll(casa2);

        System.out.println("Todos: " + todos);
        System.out.println("Invitados por las dos casas: " + ambas);
        System.out.println("Solo de la primera casa: " + soloPrimera);
        System.out.println("Lugares a preparar: " + todos.size());
    }

    static Set<String> leerLista(String linea) {
        Set<String> nombres = new TreeSet<>();
        for (String n : linea.split(",")) {
            String limpio = n.trim().toLowerCase();
            if (!limpio.isEmpty()) {
                nombres.add(limpio.substring(0, 1).toUpperCase() + limpio.substring(1));
            }
        }
        return nombres;
    }
}
```

### Misión R03-N03-M3 · El inventario de la caravana

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un inventario es un `Map<String, Integer>` de producto a cantidad, en un
`LinkedHashMap` (para mostrar en el orden en que se cargaron). Leé operaciones hasta
`fin`: `+ producto cantidad` (suma), `- producto cantidad` (resta; si no alcanza, se
avisa y no se hace; si queda en 0, el producto se **quita** del mapa) y `?
producto` (muestra cuánto hay). Al final mostrá el inventario.

#### Criterio de aprobación

- Usa `LinkedHashMap` y `getOrDefault`.
- Quita los productos que llegan a 0.

#### Entrada de ejemplo

```
+ sal 10
+ tela 4
+ especias 7
- tela 4
- sal 12
? sal
? tela
+ tela 2
fin
```

#### Salida esperada

```
No alcanza sal: hay 10
sal: 10
tela: 0
Inventario: {sal=10, especias=7, tela=2}
```

#### Solución de referencia

```java
// Mision 3 - El inventario de la caravana: LinkedHashMap con altas, bajas y consultas.
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Scanner;

public class Caravana {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        Map<String, Integer> inventario = new LinkedHashMap<>();
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.equals("fin")) {
                break;
            }
            String[] p = linea.split(" ");
            String producto = p[1];
            int actual = inventario.getOrDefault(producto, 0);
            switch (p[0]) {
                case "+" -> inventario.put(producto, actual + Integer.parseInt(p[2]));
                case "-" -> {
                    int cantidad = Integer.parseInt(p[2]);
                    if (cantidad > actual) {
                        System.out.println("No alcanza " + producto + ": hay " + actual);
                    } else if (cantidad == actual) {
                        inventario.remove(producto);
                    } else {
                        inventario.put(producto, actual - cantidad);
                    }
                }
                case "?" -> System.out.println(producto + ": " + actual);
                default -> System.out.println("?");
            }
        }
        System.out.println("Inventario: " + inventario);
    }
}
```

### Encargo R03-N03-E1 · Las ventas por vendedor

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un comercio registra cada venta en una línea con el formato `vendedor;monto` hasta una
línea vacía. Con un `TreeMap<String, Double>` acumulá el total de cada vendedor y con
un `Map<String, Integer>` la cantidad de ventas. Mostrá un reporte con vendedor,
cantidad de ventas, total y promedio por venta (2 decimales), y el total general.

#### Criterio de aprobación

- Dos mapas acumulados en la misma pasada.
- El reporte sale ordenado por vendedor.

#### Entrada de ejemplo

```
Marta;15000
Juan;8200.5
Marta;4300
Ana;22000
Juan;1800
Marta;9900

```

#### Salida esperada

```
Vendedor Ventas      Total   Promedio
Ana           1   22000.00   22000.00
Juan          2   10000.50    5000.25
Marta         3   29200.00    9733.33
Total general: 61200.50
```

#### Solución de referencia

```java
// Encargo - Las ventas por vendedor: dos mapas y un reporte ordenado.
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.Scanner;
import java.util.TreeMap;

public class Ventas {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Scanner teclado = new Scanner(System.in);
        Map<String, Double> totales = new TreeMap<>();
        Map<String, Integer> cantidades = new HashMap<>();
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.isEmpty()) {
                break;
            }
            String[] p = linea.split(";");
            totales.merge(p[0], Double.parseDouble(p[1]), Double::sum);
            cantidades.merge(p[0], 1, Integer::sum);
        }
        double general = 0;
        System.out.printf("%-8s %6s %10s %10s%n", "Vendedor", "Ventas", "Total", "Promedio");
        for (Map.Entry<String, Double> e : totales.entrySet()) {
            int n = cantidades.get(e.getKey());
            System.out.printf("%-8s %6d %10.2f %10.2f%n", e.getKey(), n, e.getValue(), e.getValue() / n);
            general += e.getValue();
        }
        System.out.printf("Total general: %.2f%n", general);
    }
}
```

### Prueba del sello

#### ¿Qué devuelve `mapa.get(clave)` si la clave no existe?

`null`. Para evitarlo se usa `getOrDefault` o se pregunta antes con `containsKey`.

#### ¿Qué pasa si hacés `put` con una clave que ya estaba?

Se reemplaza el valor anterior.

#### ¿En qué orden se recorre un `HashMap`?

En ninguno garantizado. Para orden de inserción, `LinkedHashMap`; para orden por clave, `TreeMap`.

#### ¿Qué hace `set.add(x)` si `x` ya estaba?

Nada, y devuelve `false`: un conjunto no tiene repetidos.

#### ¿Qué necesita una clase tuya para funcionar bien como clave de un `HashMap`?

Redefinir `equals` y `hashCode` (o ser un `record`).

### Soluciones (docente)

Nodo nuevo (el 21 del índice de `18-Java` estaba por crear). `Integer::sum` y `Double::sum` son referencias a métodos que se explican dos nodos más adelante; acá se usan como "la forma de sumar" en `merge`. El formato `%,8d` agrupa miles con el separador de la configuración regional: con `Locale.US` es la coma.

## R03-N04 · Excepciones

```meta
tipo: tema
padre: R03-N03
precio: 10
criatura: troll
```

### Crónica

Una noche, en los Archivos, un pergamino maldito corta todo: el archivista pedía un tomo que no existía y el edificio entero se apagó. A la mañana siguiente, {mentor} instala en cada sala una **campana**: si algo sale mal, la campana suena, alguien la escucha y decide qué hacer. El resto del edificio sigue funcionando.

—Los errores van a pasar, {heroe} —dice—. Un archivo que no está, un número mal escrito, una conexión que se corta. Lo que importa es quién **escucha la campana** y qué hace con ella.

### Objetivos

- Atrapar excepciones con `try`/`catch` y ejecutar código siempre con `finally`.
- Distinguir las excepciones *checked* de las *unchecked* y usar `throws`.
- Lanzar excepciones con `throw` y crear excepciones propias.
- Cerrar recursos automáticamente con `try` con recursos.
- Leer un *stack trace* completo, incluida la causa.

### Antes de empezar

- Mapas y conjuntos (y todo lo anterior de la rama).

### Explicación

#### Qué es una excepción
Una **excepción** es un objeto que representa un error en tiempo de ejecución. Cuando
algo sale mal, Java la **lanza**: el método se corta en esa línea y la excepción "sube"
por los métodos que lo llamaron hasta que alguno la **atrapa**. Si nadie la atrapa,
llega al `main`, se muestra el *stack trace* y el programa termina.

#### `try` / `catch` / `finally`
```java
try {
    int edad = Integer.parseInt(texto);           // puede fallar
    System.out.println("Edad: " + edad);
} catch (NumberFormatException e) {               // se ejecuta solo si falla
    System.out.println("No es un número: " + e.getMessage());
} finally {                                       // se ejecuta SIEMPRE (falle o no)
    System.out.println("Fin del intento");
}
```
- Si el `try` no falla, se saltea el `catch`.
- Puede haber **varios `catch`**, del más específico al más general.
- Un `catch` puede atrapar varias a la vez: `catch (NumberFormatException |
  ArithmeticException e)` (*multi-catch*).
- `finally` sirve para liberar recursos o dejar todo en orden.

#### La familia de las excepciones
```
Throwable
├── Error                       (problemas graves de la JVM: OutOfMemoryError, StackOverflowError; no se atrapan)
└── Exception
    ├── IOException, SQLException, …        ← checked
    └── RuntimeException                    ← unchecked
        ├── NullPointerException
        ├── ArithmeticException
        ├── IndexOutOfBoundsException
        ├── IllegalArgumentException
        │   └── NumberFormatException
        └── ClassCastException, …
```
Un `catch (Exception e)` atrapa todas las de su rama. Atrapar `Exception` "por las
dudas" suele esconder errores: atrapá lo que sabés manejar.

#### *Checked* y *unchecked*
- Las **unchecked** (`RuntimeException` y sus hijas) son errores de programación: un
  `null`, un índice fuera de rango. El compilador no obliga a atraparlas.
- Las **checked** (las demás `Exception`, como `IOException` o `SQLException`) son
  problemas **esperables** que no dependen del programa: un archivo que no existe, una
  base de datos caída. El compilador **obliga** a hacer algo: atraparlas o declararlas
  con `throws` para que las maneje quien llamó.
```java
static String leerConfiguracion(String ruta) throws IOException {   // "puede lanzar"
    return Files.readString(Path.of(ruta));
}
```
Si no la atrapás ni la declarás: `unreported exception IOException; must be caught or
declared to be thrown`.

#### Lanzar: `throw`
```java
if (monto <= 0) {
    throw new IllegalArgumentException("el monto tiene que ser positivo");
}
```
Para validar parámetros se usan las de la biblioteca: `IllegalArgumentException`
(parámetro inválido) e `IllegalStateException` (el objeto no está en un estado que
permita esa operación).

#### Excepciones propias
Cuando el error es del **dominio** de tu programa, conviene una clase propia:
```java
class SaldoInsuficienteException extends Exception {        // checked
    private final double faltante;

    public SaldoInsuficienteException(double faltante) {
        super("faltan " + faltante + " denarios");
        this.faltante = faltante;
    }

    public double getFaltante() { return faltante; }
}
```
Si hereda de `Exception` es *checked*; si hereda de `RuntimeException`, *unchecked*.
Regla práctica: *checked* si quien llama **puede y debe** recuperarse (pedir otro
monto); *unchecked* si es un error de programación.

#### Encadenar: la causa
Al traducir una excepción técnica en una del dominio, se pasa la original como
**causa**, para no perder información:
```java
try {
    …
} catch (IOException e) {
    throw new ArchivoCorruptoException("no se pudo leer el inventario", e);
}
```
El stack trace muestra las dos: la nueva y, abajo, `Caused by: …` con la original.

#### `try` con recursos
Los archivos, conexiones y otros recursos hay que **cerrarlos** siempre, aunque haya
un error. `try` con recursos los cierra solo, en orden inverso, al salir del bloque:
```java
try (BufferedReader lector = Files.newBufferedReader(Path.of("datos.txt"))) {
    …
}   // acá se llama lector.close(), falle o no
```
Funciona con cualquier objeto que implemente la interfaz `AutoCloseable`. Es la forma
correcta de trabajar con archivos (próxima rama) y con bases de datos.

#### Leer el stack trace
```
Exception in thread "main" SaldoInsuficienteException: faltan 30.0 denarios
        at Cuenta.retirar(Tesoreria.java:41)
        at Tesoreria.pagar(Tesoreria.java:18)
        at Tesoreria.main(Tesoreria.java:9)
```
1. La **primera línea**: qué excepción y su mensaje.
2. Las líneas `at`: el camino de llamadas, **de la más reciente a la más vieja**. La
   primera `at` de *tu* código (no de `java.base`) suele ser donde mirar.
3. Si hay `Caused by:`, bajá hasta la última causa: ahí está el origen.

`e.printStackTrace()` lo muestra sin terminar el programa (por la salida de errores).

> **Si venís de Python.** `try`/`except`/`finally` es `try`/`catch`/`finally`, `raise`
> es `throw` y `with` es el `try` con recursos. Lo nuevo son las *checked*: Python no
> obliga a declarar nada.
>
> **Si venís de C.** No se revisan códigos de error después de cada llamada: el error
> "salta" hasta quien lo pueda manejar.

### Código de ejemplo

```java
/*
 * Excepciones: las campanas de los Archivos.
 */
public class Campanas {
    public static void main(String[] args) {
        // try/catch/finally con varios catch
        String[] entradas = {"42", "cuarenta", "0"};
        for (String e : entradas) {
            try {
                int n = Integer.parseInt(e);
                System.out.println("100 / " + n + " = " + (100 / n));
            } catch (NumberFormatException ex) {
                System.out.println("'" + e + "' no es un número");
            } catch (ArithmeticException ex) {
                System.out.println("No se puede dividir por cero");
            } finally {
                System.out.println("  (campana revisada)");
            }
        }

        // Excepción propia checked: el compilador obliga a manejarla
        Cofre cofre = new Cofre(50);
        try {
            cofre.retirar(20);
            cofre.retirar(45);
            System.out.println("No se llega a esta línea");
        } catch (SaldoInsuficienteException ex) {
            System.out.println("Retiro rechazado: " + ex.getMessage() + " (faltante " + ex.getFaltante() + ")");
        }
        System.out.println("Quedan " + cofre.getSaldo());

        // Unchecked para un error de programación
        try {
            cofre.depositar(-5);
        } catch (IllegalArgumentException ex) {
            System.out.println("Error de uso: " + ex.getMessage());
        }

        // Encadenar una causa
        try {
            cargarInventario("12;x;7");
        } catch (InventarioInvalidoException ex) {
            System.out.println(ex.getMessage() + " | causa: " + ex.getCause());
        }

        // try con recursos: la puerta se cierra sola, aunque haya un error
        try (Puerta p = new Puerta("sala norte")) {
            p.cruzar();
            throw new IllegalStateException("el pasillo se derrumbó");
        } catch (IllegalStateException ex) {
            System.out.println("Atrapada: " + ex.getMessage());
        }
    }

    static int cargarInventario(String datos) throws InventarioInvalidoException {
        int total = 0;
        for (String parte : datos.split(";")) {
            try {
                total += Integer.parseInt(parte);
            } catch (NumberFormatException ex) {
                throw new InventarioInvalidoException("inventario ilegible en '" + parte + "'", ex);
            }
        }
        return total;
    }
}

class SaldoInsuficienteException extends Exception {
    private final int faltante;

    public SaldoInsuficienteException(int faltante) {
        super("faltan " + faltante + " denarios");
        this.faltante = faltante;
    }

    public int getFaltante() {
        return faltante;
    }
}

class InventarioInvalidoException extends Exception {
    public InventarioInvalidoException(String mensaje, Throwable causa) {
        super(mensaje, causa);
    }
}

class Cofre {
    private int saldo;

    public Cofre(int saldo) {
        this.saldo = saldo;
    }

    public int getSaldo() {
        return saldo;
    }

    public void depositar(int monto) {
        if (monto <= 0) {
            throw new IllegalArgumentException("el depósito tiene que ser positivo");
        }
        saldo += monto;
    }

    public void retirar(int monto) throws SaldoInsuficienteException {
        if (monto > saldo) {
            throw new SaldoInsuficienteException(monto - saldo);
        }
        saldo -= monto;
    }
}

class Puerta implements AutoCloseable {
    private final String nombre;

    public Puerta(String nombre) {
        this.nombre = nombre;
        System.out.println("Se abre la puerta de la " + nombre);
    }

    public void cruzar() {
        System.out.println("Cruzando la " + nombre);
    }

    @Override
    public void close() {
        System.out.println("Se cierra la puerta de la " + nombre);
    }
}
```

### Salida esperada

```
100 / 42 = 2
  (campana revisada)
'cuarenta' no es un número
  (campana revisada)
No se puede dividir por cero
  (campana revisada)
Retiro rechazado: faltan 15 denarios (faltante 15)
Quedan 30
Error de uso: el depósito tiene que ser positivo
inventario ilegible en 'x' | causa: java.lang.NumberFormatException: For input string: "x"
Se abre la puerta de la sala norte
Cruzando la sala norte
Se cierra la puerta de la sala norte
Atrapada: el pasillo se derrumbó
```

### ¿Para qué sirve?

Todo programa que habla con el mundo exterior tiene errores posibles: archivos que no están, datos mal cargados, redes que se cortan, bases de datos ocupadas. Las excepciones permiten separar el camino normal del manejo de errores, informar bien qué pasó y **no dejar recursos abiertos**. En un sistema de gestión, una excepción propia como `StockInsuficienteException` hace que el error se entienda en el idioma del negocio.

### Errores habituales

**Slime: una checked sin manejar.**
```
error: unreported exception SaldoInsuficienteException; must be caught or declared to be thrown
        cofre.retirar(45);
                     ^
```
Atrapala con `try`/`catch` o agregá `throws` al método.

**Ogro: el `catch` vacío.** `catch (Exception e) { }` se traga el error y el programa
sigue como si nada, con datos incorrectos. Como mínimo, informalo.

**Slime: el orden de los `catch`.** Si un `catch (Exception e)` va antes que uno más
específico, el segundo nunca se alcanza: `exception NumberFormatException has already
been caught`.

**Troll: el recurso sin cerrar.** Un archivo o una conexión abierta sin `close()` (o
cerrada solo en el camino feliz) termina agotando recursos. Usá `try` con recursos.

**Ogro: perder la causa.** `throw new MiExcepcion("falló");` dentro de un `catch` sin
pasar la original borra la pista del error real. Pasala como segundo argumento.

### Misión R03-N04-M1 · El conversor a prueba de balas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé líneas con dos números separados por `/` (por ejemplo `10/4`) hasta una línea
vacía y mostrá el resultado de la **división entera**. Cada línea puede fallar de
varias formas: sin `/` (índice fuera de rango al separar), texto que no es número o
división por cero. Atrapá cada caso con su propio `catch` y un mensaje claro, y un
`finally` que cuente las líneas procesadas. Al final mostrá cuántas salieron bien.

#### Criterio de aprobación

- Un `catch` específico por tipo de error, del más específico al más general.
- El `finally` cuenta todas las líneas, fallen o no.

#### Entrada de ejemplo

```
10/4
7/0
cien/2
15
81/9

```

#### Salida esperada

```
10/4 = 2
7/0: no se puede dividir por cero
cien/2: hay algo que no es un número
15: falta la barra
81/9 = 9
2 de 5 líneas salieron bien
```

#### Solución de referencia

```java
// Mision 1 - El conversor a prueba de balas: varios catch y finally.
import java.util.Scanner;

public class Divisiones {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        int procesadas = 0;
        int bien = 0;
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.isEmpty()) {
                break;
            }
            try {
                String[] partes = linea.split("/");
                int a = Integer.parseInt(partes[0]);
                int b = Integer.parseInt(partes[1]);
                System.out.println(linea + " = " + (a / b));
                bien++;
            } catch (NumberFormatException e) {
                System.out.println(linea + ": hay algo que no es un número");
            } catch (ArithmeticException e) {
                System.out.println(linea + ": no se puede dividir por cero");
            } catch (ArrayIndexOutOfBoundsException e) {
                System.out.println(linea + ": falta la barra");
            } finally {
                procesadas++;
            }
        }
        System.out.println(bien + " de " + procesadas + " líneas salieron bien");
    }
}
```

### Misión R03-N04-M2 · La herrería sin stock

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una excepción **checked** `StockInsuficienteException` que guarde el producto,
lo pedido y lo disponible, y una clase `Deposito` con un `Map<String, Integer>` de
stock y un método `void retirar(String producto, int cantidad) throws
StockInsuficienteException`. Si el producto no existe, lanzá una
`IllegalArgumentException` (unchecked: es un error de quien llama). Procesá la lista
de pedidos del `main` informando cada resultado, y al final mostrá el stock.

#### Criterio de aprobación

- `StockInsuficienteException` extiende `Exception` y tiene getters.
- `retirar` declara `throws` y el `main` maneja las dos excepciones por separado.

#### Salida esperada

```
Entregado: 2 espada
Sin stock: pidieron 2 escudo y hay 1
Pedido inválido: no existe el producto lanza
Entregado: 1 espada
Stock final: {escudo=1, espada=0}
```

#### Solución de referencia

```java
// Mision 2 - La herreria sin stock: una excepcion checked propia.
import java.util.Map;
import java.util.TreeMap;

public class Herreria {
    public static void main(String[] args) {
        Deposito d = new Deposito();
        d.cargar("espada", 3);
        d.cargar("escudo", 1);
        String[][] pedidos = {{"espada", "2"}, {"escudo", "2"}, {"lanza", "1"}, {"espada", "1"}};
        for (String[] p : pedidos) {
            try {
                d.retirar(p[0], Integer.parseInt(p[1]));
                System.out.println("Entregado: " + p[1] + " " + p[0]);
            } catch (StockInsuficienteException e) {
                System.out.println("Sin stock: pidieron " + e.getPedido() + " " + e.getProducto() + " y hay " + e.getDisponible());
            } catch (IllegalArgumentException e) {
                System.out.println("Pedido inválido: " + e.getMessage());
            }
        }
        System.out.println("Stock final: " + d);
    }
}

class StockInsuficienteException extends Exception {
    private final String producto;
    private final int pedido;
    private final int disponible;

    public StockInsuficienteException(String producto, int pedido, int disponible) {
        super("stock insuficiente de " + producto);
        this.producto = producto;
        this.pedido = pedido;
        this.disponible = disponible;
    }

    public String getProducto() {
        return producto;
    }

    public int getPedido() {
        return pedido;
    }

    public int getDisponible() {
        return disponible;
    }
}

class Deposito {
    private final Map<String, Integer> stock = new TreeMap<>();

    public void cargar(String producto, int cantidad) {
        stock.merge(producto, cantidad, Integer::sum);
    }

    public void retirar(String producto, int cantidad) throws StockInsuficienteException {
        if (!stock.containsKey(producto)) {
            throw new IllegalArgumentException("no existe el producto " + producto);
        }
        int hay = stock.get(producto);
        if (cantidad > hay) {
            throw new StockInsuficienteException(producto, cantidad, hay);
        }
        stock.put(producto, hay - cantidad);
    }

    @Override
    public String toString() {
        return stock.toString();
    }
}
```

### Misión R03-N04-M3 · La lectura del registro

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Registro` que implemente `AutoCloseable`: al crearla muestra
"abriendo registro", tiene un método `String leerLinea(int n)` que devuelve la línea `n`
de un array interno (y lanza `IllegalStateException` si el registro ya se cerró o
`IndexOutOfBoundsException` si `n` no existe), y `close()` muestra "cerrando registro".
En el `main`, usala dos veces con `try` con recursos: una que lee bien y otra que falla
a la mitad. Mostrá que se cierra en los dos casos. Escribí además un método que lea las
líneas y **traduzca** el error de índice en una excepción propia `RegistroException`
con la original como **causa**, y mostrá la causa.

#### Criterio de aprobación

- `Registro` implementa `AutoCloseable` y se usa con `try (…)`.
- El registro se cierra aunque haya un error.
- La excepción propia lleva la original como causa.

#### Salida esperada

```
abriendo registro
Kira entró por el portón norte
Bron pagó 30 denarios
cerrando registro
abriendo registro
Lía perdió su pase
cerrando registro
Error: no existe la línea 7
abriendo registro
Kira entró por el portón norte
cerrando registro
el registro no tiene todas las líneas pedidas | causa: IndexOutOfBoundsException
```

#### Solución de referencia

```java
// Mision 3 - La lectura del registro: try con recursos y excepciones encadenadas.
public class Lectura {
    public static void main(String[] args) {
        try (Registro r = new Registro()) {
            System.out.println(r.leerLinea(0));
            System.out.println(r.leerLinea(1));
        }
        try (Registro r = new Registro()) {
            System.out.println(r.leerLinea(2));
            System.out.println(r.leerLinea(7));
        } catch (IndexOutOfBoundsException e) {
            System.out.println("Error: " + e.getMessage());
        }
        try {
            leerVarias(new int[]{0, 5});
        } catch (RegistroException e) {
            System.out.println(e.getMessage() + " | causa: " + e.getCause().getClass().getSimpleName());
        }
    }

    static void leerVarias(int[] lineas) throws RegistroException {
        try (Registro r = new Registro()) {
            for (int n : lineas) {
                System.out.println(r.leerLinea(n));
            }
        } catch (IndexOutOfBoundsException e) {
            throw new RegistroException("el registro no tiene todas las líneas pedidas", e);
        }
    }
}

class RegistroException extends Exception {
    public RegistroException(String mensaje, Throwable causa) {
        super(mensaje, causa);
    }
}

class Registro implements AutoCloseable {
    private final String[] lineas = {"Kira entró por el portón norte", "Bron pagó 30 denarios", "Lía perdió su pase"};
    private boolean cerrado = false;

    public Registro() {
        System.out.println("abriendo registro");
    }

    public String leerLinea(int n) {
        if (cerrado) {
            throw new IllegalStateException("el registro está cerrado");
        }
        if (n < 0 || n >= lineas.length) {
            throw new IndexOutOfBoundsException("no existe la línea " + n);
        }
        return lineas[n];
    }

    @Override
    public void close() {
        cerrado = true;
        System.out.println("cerrando registro");
    }
}
```

### Encargo R03-N04-E1 · La transferencia bancaria

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Escribí una clase `Cuenta` (número, saldo) y un método `static void transferir(Cuenta
origen, Cuenta destino, double monto) throws TransferenciaException`. La transferencia
falla (con una `TransferenciaException` checked que explique el motivo) si el monto no
es positivo, si origen y destino son la misma cuenta o si no hay saldo. Tiene que ser
**todo o nada**: si algo falla, ninguna cuenta cambia. Probá cuatro transferencias
(una buena y tres que fallan por cada motivo) y mostrá los saldos al final con 2
decimales.

#### Criterio de aprobación

- Todas las validaciones se hacen antes de modificar los saldos.
- Cada error tiene su mensaje y los saldos quedan consistentes.

#### Salida esperada

```
Transferencia de 1500.00 de 1001 a 1002: ok
Transferencia de 5000.00 rechazada: saldo insuficiente en la cuenta 1002
Transferencia de 100.00 rechazada: origen y destino son la misma cuenta
Transferencia de -20.00 rechazada: el monto tiene que ser positivo
Cuenta 1001: 3500.00
Cuenta 1002: 2300.00
```

#### Solución de referencia

```java
// Encargo - La transferencia bancaria: validar todo antes de cambiar nada.
import java.util.Locale;

public class Transferencias {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Cuenta a = new Cuenta(1001, 5000);
        Cuenta b = new Cuenta(1002, 800);
        intentar(a, b, 1500);
        intentar(b, a, 5000);
        intentar(a, a, 100);
        intentar(a, b, -20);
        System.out.println(a);
        System.out.println(b);
    }

    static void intentar(Cuenta origen, Cuenta destino, double monto) {
        try {
            transferir(origen, destino, monto);
            System.out.printf("Transferencia de %.2f de %d a %d: ok%n", monto, origen.getNumero(), destino.getNumero());
        } catch (TransferenciaException e) {
            System.out.printf("Transferencia de %.2f rechazada: %s%n", monto, e.getMessage());
        }
    }

    static void transferir(Cuenta origen, Cuenta destino, double monto) throws TransferenciaException {
        if (monto <= 0) {
            throw new TransferenciaException("el monto tiene que ser positivo");
        }
        if (origen == destino) {
            throw new TransferenciaException("origen y destino son la misma cuenta");
        }
        if (origen.getSaldo() < monto) {
            throw new TransferenciaException("saldo insuficiente en la cuenta " + origen.getNumero());
        }
        origen.mover(-monto);
        destino.mover(monto);
    }
}

class TransferenciaException extends Exception {
    public TransferenciaException(String mensaje) {
        super(mensaje);
    }
}

class Cuenta {
    private final int numero;
    private double saldo;

    public Cuenta(int numero, double saldo) {
        this.numero = numero;
        this.saldo = saldo;
    }

    public int getNumero() {
        return numero;
    }

    public double getSaldo() {
        return saldo;
    }

    void mover(double monto) {
        saldo += monto;
    }

    @Override
    public String toString() {
        return String.format("Cuenta %d: %.2f", numero, saldo);
    }
}
```

### Prueba del sello

#### ¿Cuándo se ejecuta el bloque `finally`?

Siempre: si el `try` sale bien, si salta una excepción atrapada y aun si salta una que no se atrapa.

#### ¿Qué diferencia hay entre una excepción checked y una unchecked?

El compilador obliga a atrapar o declarar (`throws`) las checked; las unchecked (`RuntimeException` y sus hijas) no.

#### ¿Cuándo conviene que una excepción propia sea checked?

Cuando quien llama puede y debe recuperarse del problema (por ejemplo, pedir otro monto).

#### ¿Qué hace el `try` con recursos?

Llama a `close()` de los recursos declarados al salir del bloque, haya error o no.

#### En un stack trace con `Caused by:`, ¿dónde está el origen del problema?

En la última causa, la de más abajo.

### Soluciones (docente)

Sale de `18-Java/22-Excepciones` (unidad 2). Suma lo que la auditoría marcó como faltante: `try` con recursos de verdad, la excepción propia unchecked frente a la checked, el encadenamiento con `causa` y la lectura del stack trace.

## R03-N05 · Lambdas, clases anónimas y referencias a métodos

```meta
tipo: tema
padre: R03-N04
precio: 10
criatura: skeleton
```

### Crónica

El archivista jefe está cansado de dar instrucciones largas: *"Tomá cada pergamino, fijate si es del año 800, y si lo es, llevalo a la sala tres"*. Una aprendiz le pasa una tarjetita con una línea: `p -> p.anio() == 800`. El archivista la mira, sonríe, y la clava en la puerta.

—Muchas veces lo que querés pasarle a un método no es un dato, sino **una forma de hacer algo** —dice {mentor}—: cómo ordenar, qué filtrar, qué hacer cuando tocan un botón. Las **lambdas** son esa tarjetita, {heroe}.

### Objetivos

- Entender qué es una interfaz funcional.
- Escribir clases anónimas y reemplazarlas por lambdas.
- Usar referencias a métodos (`String::toUpperCase`, `Integer::sum`).
- Ordenar con `Comparator` y filtrar o transformar colecciones con `removeIf`, `forEach` y `replaceAll`.
- Usar las interfaces `Predicate`, `Function`, `Consumer` y `Supplier`.

### Antes de empezar

- Interfaces (Interfaces: contratos).
- Colecciones (ArrayList y genéricos, Mapas y conjuntos).

### Explicación

#### El problema: pasar comportamiento
Para ordenar héroes por nombre, `list.sort` necesita **una forma de comparar**: un
objeto que implemente la interfaz `Comparator<Heroe>`. Con lo que viste hasta ahora,
eso es una clase entera:
```java
class PorNombre implements Comparator<Heroe> {
    @Override
    public int compare(Heroe a, Heroe b) {
        return a.getNombre().compareTo(b.getNombre());
    }
}
grupo.sort(new PorNombre());
```

#### Clases anónimas
Una **clase anónima** se declara y se crea en el mismo lugar, sin nombre:
```java
grupo.sort(new Comparator<Heroe>() {
    @Override
    public int compare(Heroe a, Heroe b) {
        return a.getNombre().compareTo(b.getNombre());
    }
});
```
Todavía se ven en código viejo y en Swing (el código que genera NetBeans las usa
mucho), así que conviene reconocerlas.

#### Lambdas
Cuando la interfaz tiene **un solo método abstracto** (se llama *interfaz funcional*),
la clase anónima se puede escribir como una **lambda**: solo los parámetros y el
cuerpo.
```java
grupo.sort((a, b) -> a.getNombre().compareTo(b.getNombre()));
```
La forma es `(parámetros) -> expresión` o `(parámetros) -> { instrucciones; }`:
```java
x -> x * 2                          // un parámetro: sin paréntesis
(a, b) -> a + b                     // dos parámetros
() -> System.out.println("hola")    // sin parámetros
s -> {                              // un bloque: con llaves y return
    String t = s.trim();
    return t.toUpperCase();
}
```
Los tipos de los parámetros los deduce el compilador por el contexto.

#### Referencias a métodos
Si la lambda solo llama a un método que ya existe, se puede escribir todavía más corta:
| Lambda | Referencia a método |
|---|---|
| `s -> s.toUpperCase()` | `String::toUpperCase` |
| `x -> System.out.println(x)` | `System.out::println` |
| `(a, b) -> Integer.sum(a, b)` | `Integer::sum` |
| `h -> h.getNombre()` | `Heroe::getNombre` |

#### Las interfaces funcionales de la biblioteca
El paquete `java.util.function` trae las más comunes:
| Interfaz | Método | Recibe → devuelve | Ejemplo |
|---|---|---|---|
| `Predicate<T>` | `test` | `T` → `boolean` | `h -> h.getVida() > 0` |
| `Function<T, R>` | `apply` | `T` → `R` | `h -> h.getNombre()` |
| `Consumer<T>` | `accept` | `T` → nada | `h -> h.curar(10)` |
| `Supplier<T>` | `get` | nada → `T` | `() -> new Heroe("Pip")` |
| `Comparator<T>` | `compare` | `T, T` → `int` | `(a, b) -> …` |
| `Runnable` | `run` | nada → nada | `() -> System.out.println("¡Ya!")` |

#### Comparadores cómodos
`Comparator` trae métodos que arman comparadores sin escribir el `compareTo`:
```java
grupo.sort(Comparator.comparing(Heroe::getNombre));               // por nombre
grupo.sort(Comparator.comparingInt(Heroe::getNivel).reversed());   // por nivel, de mayor a menor
grupo.sort(Comparator.comparingInt(Heroe::getNivel)
        .thenComparing(Heroe::getNombre));                         // desempate
```

#### Lambdas con colecciones
```java
grupo.forEach(h -> System.out.println(h));        // hacer algo con cada uno
grupo.removeIf(h -> h.getVida() == 0);            // borrar los que cumplen (sin ConcurrentModification)
nombres.replaceAll(String::toUpperCase);          // transformar cada uno
mapa.forEach((clave, valor) -> …);                // recorrer un mapa
```

#### Variables de afuera
Una lambda puede **leer** variables del método donde se escribe, pero solo si no
cambian después (tienen que ser *efectivamente finales*). Si intentás modificarlas:
`local variables referenced from a lambda expression must be final or effectively
final`.

> **Si venís de Python.** Una lambda de Java es como `lambda x: x * 2`, pero puede tener
> un bloque de varias líneas. `Comparator.comparing(Heroe::getNombre)` es como
> `sorted(grupo, key=lambda h: h.nombre)`.

### Código de ejemplo

```java
/*
 * Lambdas: las tarjetitas del archivista.
 */
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.function.Supplier;

public class Tarjetitas {
    public static void main(String[] args) {
        List<Pergamino> archivo = new ArrayList<>(List.of(
                new Pergamino("Tratado de paz", 812, 40),
                new Pergamino("Mapa del norte", 800, 12),
                new Pergamino("Leyes del puerto", 790, 95),
                new Pergamino("Diario de Kaffa", 800, 60)));

        // 1. Clase anónima
        archivo.sort(new Comparator<Pergamino>() {
            @Override
            public int compare(Pergamino a, Pergamino b) {
                return Integer.compare(a.anio(), b.anio());
            }
        });
        System.out.println("Por año (clase anónima): " + nombres(archivo));

        // 2. La misma idea con una lambda
        archivo.sort((a, b) -> a.titulo().compareTo(b.titulo()));
        System.out.println("Por título (lambda): " + nombres(archivo));

        // 3. Con Comparator.comparing y una referencia a método
        archivo.sort(Comparator.comparingInt(Pergamino::paginas).reversed());
        System.out.println("Por páginas, de más a menos: " + nombres(archivo));
        archivo.sort(Comparator.comparingInt(Pergamino::anio).thenComparing(Pergamino::titulo));
        System.out.println("Por año y título: " + nombres(archivo));

        // Predicate, Function y Supplier guardados en variables
        Predicate<Pergamino> delAnio800 = p -> p.anio() == 800;
        Function<Pergamino, String> etiqueta = p -> p.titulo().toUpperCase() + " (" + p.anio() + ")";
        Supplier<Pergamino> enBlanco = () -> new Pergamino("Sin título", 0, 0);
        for (Pergamino p : archivo) {
            if (delAnio800.test(p)) {
                System.out.println("  del año 800: " + etiqueta.apply(p));
            }
        }
        System.out.println("  uno nuevo: " + enBlanco.get());

        // Lambdas con colecciones
        archivo.removeIf(p -> p.paginas() < 20);
        System.out.println("Sin los finitos: " + nombres(archivo));
        List<String> titulos = new ArrayList<>();
        archivo.forEach(p -> titulos.add(p.titulo()));
        titulos.replaceAll(String::toUpperCase);
        titulos.forEach(System.out::println);
    }

    static List<String> nombres(List<Pergamino> lista) {
        List<String> r = new ArrayList<>();
        lista.forEach(p -> r.add(p.titulo()));
        return r;
    }
}

record Pergamino(String titulo, int anio, int paginas) { }
```

### Salida esperada

```
Por año (clase anónima): [Leyes del puerto, Mapa del norte, Diario de Kaffa, Tratado de paz]
Por título (lambda): [Diario de Kaffa, Leyes del puerto, Mapa del norte, Tratado de paz]
Por páginas, de más a menos: [Leyes del puerto, Diario de Kaffa, Tratado de paz, Mapa del norte]
Por año y título: [Leyes del puerto, Diario de Kaffa, Mapa del norte, Tratado de paz]
  del año 800: DIARIO DE KAFFA (800)
  del año 800: MAPA DEL NORTE (800)
  uno nuevo: Pergamino[titulo=Sin título, anio=0, paginas=0]
Sin los finitos: [Leyes del puerto, Diario de Kaffa, Tratado de paz]
LEYES DEL PUERTO
DIARIO DE KAFFA
TRATADO DE PAZ
```

### ¿Para qué sirve?

Las lambdas están en todo el Java moderno: los botones de Swing reaccionan a clics con una lambda, las listas se ordenan con `Comparator.comparing`, se filtran con `removeIf` y, en la Senda de Java moderno, se procesan enteras con *streams*. Permiten escribir "qué hacer" en una línea y reutilizar los algoritmos de la biblioteca en lugar de escribirlos de nuevo.

### Errores habituales

**Esqueleto: una lambda donde no va.** Una lambda solo se puede usar donde se espera
una interfaz funcional. `Object o = x -> x;` da `incompatible types: Object is not a
functional interface`.

**Slime: modificar una variable de afuera.**
```
error: local variables referenced from a lambda expression must be final or effectively final
        archivo.forEach(p -> total += p.paginas());
```
Usá un acumulador en un array de uno, un objeto, o un bucle común.

**Ogro: el `reversed()` que no invierte lo que creías.** En
`comparing(A).thenComparing(B).reversed()` se invierte **todo**, incluido el desempate.
Si solo querés invertir el primer criterio, poné el `reversed()` pegado a él.

**Slime: la lambda de bloque sin `return`.** `s -> { s.trim(); }` en una `Function` no
compila: con llaves hace falta `return`.

**Troll: `removeIf` sobre una lista inmutable.** `List.of(...).removeIf(...)` corta con
`UnsupportedOperationException`.

### Misión R03-N05-M1 · El ranking con comparadores

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con un `record Jugador(String nombre, int puntos, int partidas)` y una lista de 6
jugadores, mostrá la lista ordenada de cuatro formas, cada una en una línea:

1. por nombre, con una **clase anónima**;
2. por puntos de mayor a menor, con una **lambda**;
3. por partidas (menos primero) y, si empatan, por nombre, con
   `Comparator.comparingInt(...).thenComparing(...)`;
4. por promedio de puntos por partida, de mayor a menor (con `comparingDouble`).

#### Criterio de aprobación

- Usa las cuatro formas pedidas.
- Los desempates son correctos.

#### Salida esperada

```
Por nombre: [Ada, Bron, Lía, Nara, Olmo, Pip]
Por puntos: [Bron, Olmo, Lía, Nara, Ada, Pip]
Por partidas: [Ada, Pip, Lía, Nara, Olmo, Bron]
Por promedio: [Lía, Olmo, Ada, Nara, Pip, Bron]
```

#### Solución de referencia

```java
// Mision 1 - El ranking con comparadores: clase anonima, lambda y Comparator.comparing.
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Rankings {
    public static void main(String[] args) {
        List<Jugador> j = new ArrayList<>(List.of(
                new Jugador("Nara", 340, 10), new Jugador("Bron", 500, 20), new Jugador("Lía", 340, 8),
                new Jugador("Pip", 90, 3), new Jugador("Olmo", 410, 10), new Jugador("Ada", 120, 3)));

        j.sort(new Comparator<Jugador>() {
            @Override
            public int compare(Jugador a, Jugador b) {
                return a.nombre().compareTo(b.nombre());
            }
        });
        System.out.println("Por nombre: " + j);

        j.sort((a, b) -> Integer.compare(b.puntos(), a.puntos()));
        System.out.println("Por puntos: " + j);

        j.sort(Comparator.comparingInt(Jugador::partidas).thenComparing(Jugador::nombre));
        System.out.println("Por partidas: " + j);

        j.sort(Comparator.comparingDouble(Jugador::promedio).reversed());
        System.out.println("Por promedio: " + j);
    }
}

record Jugador(String nombre, int puntos, int partidas) {
    double promedio() {
        return (double) puntos / partidas;
    }

    @Override
    public String toString() {
        return nombre;
    }
}
```

### Misión R03-N05-M2 · La limpieza de la posada

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La posada guarda sus huéspedes en una lista de `record Huesped(String nombre, int
noches, boolean pago)`. Con **lambdas** y **referencias a métodos**, sin bucles `for`:

1. mostrá cada huésped con `forEach`;
2. borrá con `removeIf` los que tienen 0 noches;
3. con un `Predicate<Huesped>` guardado en una variable, mostrá los que deben;
4. armá una lista de nombres en mayúsculas (llenala con `forEach` y transformala con
   `replaceAll(String::toUpperCase)`);
5. ordenala alfabéticamente con `sort(Comparator.naturalOrder())`.

#### Criterio de aprobación

- No usa bucles `for` ni `while`.
- Usa al menos un `Predicate` guardado y una referencia a método.

#### Salida esperada

```
Huesped[nombre=Olmo, noches=3, pago=true]
Huesped[nombre=Pip, noches=0, pago=false]
Huesped[nombre=Nara, noches=5, pago=false]
Huesped[nombre=Bron, noches=1, pago=true]
Huesped[nombre=Lía, noches=0, pago=true]
Huesped[nombre=Ada, noches=2, pago=false]
Sin los de 0 noches: 4
Deben: Nara Ada
[ADA, BRON, NARA, OLMO]
```

#### Solución de referencia

```java
// Mision 2 - La limpieza de la posada: lambdas sobre colecciones, sin bucles.
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.function.Predicate;

public class Posada {
    public static void main(String[] args) {
        List<Huesped> huespedes = new ArrayList<>(List.of(
                new Huesped("Olmo", 3, true), new Huesped("Pip", 0, false), new Huesped("Nara", 5, false),
                new Huesped("Bron", 1, true), new Huesped("Lía", 0, true), new Huesped("Ada", 2, false)));

        huespedes.forEach(System.out::println);
        huespedes.removeIf(h -> h.noches() == 0);
        System.out.println("Sin los de 0 noches: " + huespedes.size());

        Predicate<Huesped> debe = h -> !h.pago();
        System.out.print("Deben:");
        huespedes.forEach(h -> {
            if (debe.test(h)) {
                System.out.print(" " + h.nombre());
            }
        });
        System.out.println();

        List<String> nombres = new ArrayList<>();
        huespedes.forEach(h -> nombres.add(h.nombre()));
        nombres.replaceAll(String::toUpperCase);
        nombres.sort(Comparator.naturalOrder());
        System.out.println(nombres);
    }
}

record Huesped(String nombre, int noches, boolean pago) { }
```

### Misión R03-N05-M3 · La calculadora de hechizos

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Declará tu propia **interfaz funcional** `Hechizo` con un método `int lanzar(int
poder)`. Guardá en un `Map<String, Hechizo>` (un `LinkedHashMap`) cinco hechizos
escritos como lambdas: `duplicar`, `cuadrado`, `mitad`, `invertir` (cambia el signo) y
`tope` (no deja pasar de 100). Leé líneas con `hechizo poder` hasta una vacía y
mostrá el resultado; si el hechizo no existe, avisá. Al final, aplicá **todos** los
hechizos en cadena a 7 recorriendo el mapa con `forEach`.

#### Criterio de aprobación

- `Hechizo` tiene un solo método abstracto (marcala con `@FunctionalInterface`).
- Los hechizos son lambdas guardadas en un mapa.

#### Entrada de ejemplo

```
duplicar 21
cuadrado 12
teletransportar 3
tope 150
mitad 9

```

#### Salida esperada

```
duplicar(21) = 42
cuadrado(12) = 144
No existe el hechizo teletransportar
tope(150) = 100
mitad(9) = 4
  tras duplicar: 14
  tras cuadrado: 196
  tras mitad: 98
  tras invertir: -98
  tras tope: -98
```

#### Solución de referencia

```java
// Mision 3 - La calculadora de hechizos: una interfaz funcional propia y lambdas en un mapa.
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Scanner;

public class Hechizos {
    public static void main(String[] args) {
        Map<String, Hechizo> libro = new LinkedHashMap<>();
        libro.put("duplicar", p -> p * 2);
        libro.put("cuadrado", p -> p * p);
        libro.put("mitad", p -> p / 2);
        libro.put("invertir", p -> -p);
        libro.put("tope", p -> Math.min(p, 100));

        Scanner teclado = new Scanner(System.in);
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.isEmpty()) {
                break;
            }
            String[] partes = linea.split(" ");
            Hechizo h = libro.get(partes[0]);
            if (h == null) {
                System.out.println("No existe el hechizo " + partes[0]);
            } else {
                System.out.println(partes[0] + "(" + partes[1] + ") = " + h.lanzar(Integer.parseInt(partes[1])));
            }
        }

        int[] valor = {7};
        libro.forEach((nombre, h) -> {
            valor[0] = h.lanzar(valor[0]);
            System.out.println("  tras " + nombre + ": " + valor[0]);
        });
    }
}

@FunctionalInterface
interface Hechizo {
    int lanzar(int poder);
}
```

### Encargo R03-N05-E1 · Los filtros de la tienda

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una tienda online filtra productos (`record Producto(String nombre, String categoria,
double precio, int stock)`). Escribí un método `static List<Producto>
filtrar(List<Producto> lista, Predicate<Producto> condicion)` que devuelva una lista
nueva con los que cumplen. Usalo con tres filtros: con stock, de la categoría
"hogar", y **combinados** con `and` (baratos: menos de 5000 **y** con stock) y `negate`
(sin stock). Mostrá cada resultado ordenado por precio.

#### Criterio de aprobación

- `filtrar` recibe un `Predicate` y no modifica la lista original.
- Usa `and` y `negate` para combinar condiciones.

#### Salida esperada

```
Con stock: [Cable, Pava, Lámpara, Auriculares]
Hogar: [Taza, Pava, Lámpara]
Baratos con stock: [Cable, Pava]
Sin stock: [Taza, Parlante]
```

#### Solución de referencia

```java
// Encargo - Los filtros de la tienda: Predicate como parametro, and y negate.
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.function.Predicate;

public class Tienda {
    public static void main(String[] args) {
        List<Producto> catalogo = List.of(
                new Producto("Lámpara", "hogar", 12500, 4), new Producto("Taza", "hogar", 3200, 0),
                new Producto("Auriculares", "audio", 18900, 7), new Producto("Pava", "hogar", 4800, 12),
                new Producto("Cable", "audio", 2100, 30), new Producto("Parlante", "audio", 25000, 0));

        Predicate<Producto> conStock = p -> p.stock() > 0;
        Predicate<Producto> hogar = p -> p.categoria().equals("hogar");
        Predicate<Producto> barato = p -> p.precio() < 5000;

        mostrar("Con stock", filtrar(catalogo, conStock));
        mostrar("Hogar", filtrar(catalogo, hogar));
        mostrar("Baratos con stock", filtrar(catalogo, barato.and(conStock)));
        mostrar("Sin stock", filtrar(catalogo, conStock.negate()));
    }

    static List<Producto> filtrar(List<Producto> lista, Predicate<Producto> condicion) {
        List<Producto> resultado = new ArrayList<>();
        for (Producto p : lista) {
            if (condicion.test(p)) {
                resultado.add(p);
            }
        }
        return resultado;
    }

    static void mostrar(String titulo, List<Producto> lista) {
        lista.sort(Comparator.comparingDouble(Producto::precio));
        List<String> nombres = new ArrayList<>();
        lista.forEach(p -> nombres.add(p.nombre()));
        System.out.println(titulo + ": " + nombres);
    }
}

record Producto(String nombre, String categoria, double precio, int stock) { }
```

### Prueba del sello

#### ¿Qué es una interfaz funcional?

Una interfaz con un solo método abstracto; se puede implementar con una lambda.

#### Escribí como lambda: una clase anónima de `Comparator<String>` que compara por largo.

`(a, b) -> Integer.compare(a.length(), b.length())`.

#### ¿Qué referencia a método equivale a `s -> s.trim()`?

`String::trim`.

#### ¿Por qué `removeIf` es mejor que borrar dentro de un for-each?

Porque borra de forma segura; el `remove` dentro de un for-each corta con `ConcurrentModificationException`.

#### ¿Qué devuelve un `Predicate<T>`?

Un `boolean` (su método es `test`).

### Soluciones (docente)

Nodo nuevo (el 23 del índice de `18-Java` estaba por crear). La auditoría marcaba que las lambdas se usaban en el 14, 19 y 20 sin explicarse, y que el 20 tenía clases anónimas y `this::metodo` sin presentar: acá se presentan antes de Swing. En la misión 3, `int[] valor = {7}` es el truco para acumular dentro de una lambda; se comenta en los errores habituales.

## R03-N06 · Pruebas con JUnit

```meta
tipo: tema
padre: R03-N05
precio: 10
criatura: ogre
```

### Crónica

En el Tribunal de las Pruebas, junto a los Archivos, cada ley nueva se somete a un juicio antes de publicarse: los jueces le presentan casos —*un mercader con 0 kilos, uno con carga negativa, uno con 10 000*— y la ley tiene que responder bien a todos. Si falla uno, vuelve al escritorio.

—Probar a mano es cansador y se olvida —dice {mentor}—. Escribí los casos **una vez**, como código, y hacelos correr cada vez que cambies algo. Así el ogro de la regresión no vuelve a entrar sin que te enteres, {heroe}.

### Objetivos

- Escribir pruebas automáticas con JUnit 5.
- Usar las comprobaciones principales: `assertEquals`, `assertTrue`, `assertThrows`.
- Organizar una prueba en preparar, ejecutar y comprobar.
- Compilar y correr las pruebas desde la terminal.
- Escribir las pruebas antes que el código (TDD).

### Antes de empezar

- Excepciones.
- Paquetes y archivos `.jar` (para usar la librería de JUnit).

### Explicación

#### Por qué pruebas automáticas
Cada vez que cambiás algo, podés romper otra cosa que andaba (una **regresión**).
Probar todo a mano cada vez es imposible. Una **prueba unitaria** es un método que
llama a tu código con un caso y **comprueba** el resultado. Se corren todas juntas en
segundos, cada vez que quieras.

#### Una clase de pruebas
Para una clase `Tarifa`, las pruebas van en `TarifaTest`:
```java
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class TarifaTest {
    @Test
    void cargaChicaPagaElMinimo() {
        // preparar
        Tarifa t = new Tarifa();
        // ejecutar
        double resultado = t.calcular(10);
        // comprobar
        assertEquals(5.0, resultado, 0.001);
    }

    @Test
    void cargaNegativaEsUnError() {
        Tarifa t = new Tarifa();
        assertThrows(IllegalArgumentException.class, () -> t.calcular(-1));
    }
}
```
- Cada método de prueba lleva `@Test`, es `void` y no recibe parámetros.
- El nombre dice **qué comportamiento** prueba.
- `import static` permite escribir `assertEquals` sin `Assertions.` adelante.
- Las pruebas son independientes: cada una prepara lo que necesita.

#### Las comprobaciones
| Método | Comprueba |
|---|---|
| `assertEquals(esperado, real)` | que sean iguales (con `equals`) |
| `assertEquals(esperado, real, delta)` | decimales iguales con un margen (los `double` no son exactos) |
| `assertTrue(cond)` / `assertFalse(cond)` | una condición |
| `assertNull(x)` / `assertNotNull(x)` | que sea o no `null` |
| `assertThrows(Tipo.class, () -> …)` | que el código lance esa excepción |
| `assertAll(() -> …, () -> …)` | varias a la vez, informando todas las que fallan |

El orden importa: primero el **esperado**, después el **real**. Si están al revés, el
mensaje de error confunde.

#### Preparar antes de cada prueba
Si todas las pruebas usan el mismo objeto, se crea en un método `@BeforeEach`, que
JUnit corre antes de **cada** prueba (así cada una arranca de cero):
```java
private Inventario inv;

@BeforeEach
void preparar() {
    inv = new Inventario();
    inv.agregar("espada", 3);
}
```

#### Correr las pruebas desde la terminal
JUnit es una librería: se baja un `.jar` (*junit-platform-console-standalone*, desde
Maven Central) y se usa en el classpath.
```bash
javac -d out -cp junit.jar src/*.java test/*.java
java -jar junit.jar execute --class-path out --scan-class-path
```
La salida muestra un árbol con ✔ para cada prueba que pasa y ✘ con el detalle de las
que fallan:
```
├─ JUnit Jupiter ✔
│  └─ TarifaTest ✔
│     ├─ cargaChicaPagaElMinimo() ✔
│     └─ cargaNegativaEsUnError() ✔
[         2 tests successful      ]
[         0 tests failed          ]
```
Cuando una falla:
```
expected: <5.0> but was: <7.5>
```
NetBeans, IntelliJ y VS Code corren las pruebas con un botón y las pintan de verde o
rojo.

#### Qué probar
- El caso normal.
- Los **bordes**: 0, el máximo, un elemento, vacío, el límite exacto de una regla.
- Los errores: que se lance la excepción correcta con datos inválidos.

#### TDD: primero la prueba
En el *desarrollo guiado por pruebas* se escribe primero una prueba que falla, después
el código mínimo para que pase, y después se ordena el código (con las pruebas como red
de seguridad). Rojo, verde, refactorizar.

> **Si venís de Python.** JUnit es como `pytest` o `unittest`: `assertEquals` es
> `assert a == b` y `assertThrows` es `pytest.raises`.

### Código de ejemplo

`Tarifa.java`

```java
/** Calcula la tasa de la Aduana según la carga en kilos. */
public class Tarifa {
    public double calcular(int kilos) {
        if (kilos < 0) {
            throw new IllegalArgumentException("carga negativa: " + kilos);
        }
        if (kilos <= 50) {
            return 5;
        }
        if (kilos <= 200) {
            return 5 + (kilos - 50) * 0.1;
        }
        return 20 + (kilos - 200) * 0.25;
    }
}
```

`TarifaTest.java`

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class TarifaTest {
    private Tarifa tarifa;

    @BeforeEach
    void preparar() {
        tarifa = new Tarifa();
    }

    @Test
    void sinCargaPagaElMinimo() {
        assertEquals(5.0, tarifa.calcular(0), 0.001);
    }

    @Test
    void elLimiteDe50SiguePagandoElMinimo() {
        assertEquals(5.0, tarifa.calcular(50), 0.001);
    }

    @Test
    void cargaMedianaSumaDiezCentavosPorKilo() {
        assertEquals(12.5, tarifa.calcular(125), 0.001);
    }

    @Test
    void elLimiteDe200() {
        assertEquals(20.0, tarifa.calcular(200), 0.001);
    }

    @Test
    void cargaGrandeSumaVeinticincoCentavosPorKilo() {
        assertEquals(45.0, tarifa.calcular(300), 0.001);
    }

    @Test
    void cargaNegativaEsUnError() {
        IllegalArgumentException e = assertThrows(IllegalArgumentException.class, () -> tarifa.calcular(-1));
        assertEquals("carga negativa: -1", e.getMessage());
    }
}
```

### ¿Para qué sirve?

En cualquier equipo de desarrollo profesional, el código se entrega con pruebas y un servidor las corre solo cada vez que alguien sube un cambio. Las pruebas permiten cambiar código viejo sin miedo, documentan cómo se usa cada clase y encuentran errores de bordes (el 0, el límite exacto) que a mano nadie prueba.

### Errores habituales

**Esqueleto: JUnit no está en el classpath.**
```
TarifaTest.java:4: error: package org.junit.jupiter.api does not exist
```
Compilá con `-cp junit.jar` (o el nombre completo del jar que bajaste).

**Ogro: comparar decimales sin margen.** `assertEquals(0.3, 0.1 + 0.2)` falla
(`expected: <0.3> but was: <0.30000000000000004>`). Usá el tercer parámetro:
`assertEquals(0.3, 0.1 + 0.2, 0.0001)`.

**Ogro: esperado y real al revés.** El mensaje dice `expected: <lo que calculó> but
was: <lo que esperabas>` y confunde. El esperado va primero.

**Ogro: pruebas que dependen unas de otras.** Si una prueba usa un objeto que otra
modificó, el resultado depende del orden. Prepará todo en `@BeforeEach`.

**Slime: el método de prueba sin `@Test`.** JUnit no lo corre y parece que "pasó".

### Misión R03-N06-M1 · Las pruebas del cofre

```meta
entrega: archivo
entorno: local
extensiones: zip, java
monedas: 4
xp: 10
```

#### Consigna

Esta es la clase `Cofre` (copiala tal cual). Escribí `CofreTest` con **al menos seis
pruebas**: depositar suma, depositar un monto no positivo lanza
`IllegalArgumentException`, retirar resta, retirar más de lo que hay lanza
`IllegalStateException`, retirar exactamente todo deja el saldo en 0, y el historial
cuenta las operaciones. Usá `@BeforeEach`. Entregá los dos archivos (o un zip).

```java
public class Cofre {
    private int saldo;
    private int operaciones;

    public void depositar(int monto) {
        if (monto <= 0) {
            throw new IllegalArgumentException("monto inválido");
        }
        saldo += monto;
        operaciones++;
    }

    public void retirar(int monto) {
        if (monto > saldo) {
            throw new IllegalStateException("no alcanza");
        }
        saldo -= monto;
        operaciones++;
    }

    public int getSaldo() {
        return saldo;
    }

    public int getOperaciones() {
        return operaciones;
    }
}
```

#### Criterio de aprobación

- Seis pruebas o más, cada una con un nombre que dice qué prueba.
- Usa `assertEquals` y `assertThrows`, con el esperado primero.
- Todas pasan.

#### Solución de referencia

`Cofre.java`

```java
public class Cofre {
    private int saldo;
    private int operaciones;

    public void depositar(int monto) {
        if (monto <= 0) {
            throw new IllegalArgumentException("monto inválido");
        }
        saldo += monto;
        operaciones++;
    }

    public void retirar(int monto) {
        if (monto > saldo) {
            throw new IllegalStateException("no alcanza");
        }
        saldo -= monto;
        operaciones++;
    }

    public int getSaldo() {
        return saldo;
    }

    public int getOperaciones() {
        return operaciones;
    }
}
```

`CofreTest.java`

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class CofreTest {
    private Cofre cofre;

    @BeforeEach
    void preparar() {
        cofre = new Cofre();
        cofre.depositar(100);
    }

    @Test
    void depositarSumaAlSaldo() {
        cofre.depositar(50);
        assertEquals(150, cofre.getSaldo());
    }

    @Test
    void depositarCeroEsUnError() {
        assertThrows(IllegalArgumentException.class, () -> cofre.depositar(0));
    }

    @Test
    void retirarRestaDelSaldo() {
        cofre.retirar(30);
        assertEquals(70, cofre.getSaldo());
    }

    @Test
    void retirarDeMasEsUnError() {
        assertThrows(IllegalStateException.class, () -> cofre.retirar(101));
        assertEquals(100, cofre.getSaldo());
    }

    @Test
    void retirarTodoDejaElSaldoEnCero() {
        cofre.retirar(100);
        assertEquals(0, cofre.getSaldo());
    }

    @Test
    void cuentaLasOperacionesExitosas() {
        cofre.retirar(10);
        assertThrows(IllegalStateException.class, () -> cofre.retirar(1000));
        assertEquals(2, cofre.getOperaciones());
    }
}
```

### Misión R03-N06-M2 · El bug de los descuentos

```meta
entrega: archivo
entorno: local
extensiones: zip, java
monedas: 4
xp: 10
```

#### Consigna

La clase `Descuento` debería aplicar estas reglas: compras de hasta 10 000 sin
descuento; de más de 10 000 hasta 50 000, 10 %; de más de 50 000, 20 %; y los socios
tienen 5 % extra **sobre el precio ya descontado**. Nunca puede dar un total negativo
ni aceptar montos negativos. Tiene **dos errores**. Escribí las pruebas que los
encuentren (con los bordes 10 000 y 50 000), después corregí la clase y entregá las
dos.

```java
public class Descuento {
    public double total(double monto, boolean socio) {
        double total = monto;
        if (monto >= 10000) {
            total = monto * 0.9;
        } else if (monto > 50000) {
            total = monto * 0.8;
        }
        if (socio) {
            total = total * 0.95;
        }
        return total;
    }
}
```

#### Criterio de aprobación

- Hay pruebas para los bordes (10 000, un poco más, 50 000, un poco más) y para socios.
- Hay una prueba para montos negativos.
- La clase corregida pasa todas las pruebas.

#### Solución de referencia

`Descuento.java`

```java
// Corregido: el borde de 10000 no tiene descuento (> en lugar de >=), el caso de
// mas de 50000 se evalua primero, y los montos negativos se rechazan.
public class Descuento {
    public double total(double monto, boolean socio) {
        if (monto < 0) {
            throw new IllegalArgumentException("monto negativo");
        }
        double total = monto;
        if (monto > 50000) {
            total = monto * 0.8;
        } else if (monto > 10000) {
            total = monto * 0.9;
        }
        if (socio) {
            total = total * 0.95;
        }
        return total;
    }
}
```

`DescuentoTest.java`

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class DescuentoTest {
    private final Descuento d = new Descuento();

    @Test
    void hasta10000NoHayDescuento() {
        assertEquals(10000.0, d.total(10000, false), 0.001);
    }

    @Test
    void apenasMasDe10000Tiene10PorCiento() {
        assertEquals(9000.9, d.total(10001, false), 0.001);
    }

    @Test
    void en50000SigueEl10PorCiento() {
        assertEquals(45000.0, d.total(50000, false), 0.001);
    }

    @Test
    void masDe50000Tiene20PorCiento() {
        assertEquals(48000.0, d.total(60000, false), 0.001);
    }

    @Test
    void elSocioTiene5PorCientoSobreElDescontado() {
        assertEquals(45600.0, d.total(60000, true), 0.001);
    }

    @Test
    void montoNegativoEsUnError() {
        assertThrows(IllegalArgumentException.class, () -> d.total(-1, false));
    }
}
```

### Misión R03-N06-M3 · Primero la prueba

```meta
entrega: archivo
entorno: local
extensiones: zip, java
monedas: 4
xp: 10
```

#### Consigna

Con **TDD**: escribí primero las pruebas de una clase `Contrasena` que todavía no
existe, con un método `static List<String> problemas(String clave)` que devuelve la
lista de reglas que no se cumplen (lista vacía si está bien): al menos 8 caracteres
(`"muy corta"`), al menos un número (`"sin números"`), al menos una mayúscula (`"sin
mayúsculas"`) y sin espacios (`"tiene espacios"`). Después escribí la clase hasta que
pasen todas. Entregá las dos.

#### Criterio de aprobación

- Una prueba por regla, más una de una clave válida y una con varios problemas a la vez.
- La clase pasa todas las pruebas.

#### Solución de referencia

`Contrasena.java`

```java
import java.util.ArrayList;
import java.util.List;

public class Contrasena {
    public static List<String> problemas(String clave) {
        List<String> lista = new ArrayList<>();
        if (clave.length() < 8) {
            lista.add("muy corta");
        }
        if (!clave.matches(".*\\d.*")) {
            lista.add("sin números");
        }
        if (clave.equals(clave.toLowerCase())) {
            lista.add("sin mayúsculas");
        }
        if (clave.contains(" ")) {
            lista.add("tiene espacios");
        }
        return lista;
    }
}
```

`ContrasenaTest.java`

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.Test;

class ContrasenaTest {
    @Test
    void unaClaveBuenaNoTieneProblemas() {
        assertTrue(Contrasena.problemas("Imperio2026").isEmpty());
    }

    @Test
    void muyCorta() {
        assertEquals(List.of("muy corta"), Contrasena.problemas("Kaf2"));
    }

    @Test
    void sinNumeros() {
        assertEquals(List.of("sin números"), Contrasena.problemas("Arquitecta"));
    }

    @Test
    void sinMayusculas() {
        assertEquals(List.of("sin mayúsculas"), Contrasena.problemas("cafe12345"));
    }

    @Test
    void conEspacios() {
        assertEquals(List.of("tiene espacios"), Contrasena.problemas("Taza de 1 cafe"));
    }

    @Test
    void variosProblemasALaVez() {
        assertEquals(List.of("muy corta", "sin números", "sin mayúsculas", "tiene espacios"), Contrasena.problemas("a b"));
    }
}
```

### Encargo R03-N06-E1 · El carrito probado

```meta
entrega: archivo
entorno: local
extensiones: zip, java
monedas: 1
xp: 15
```

#### Consigna

Escribí una clase `Carrito` para una tienda online (agregar un producto con precio y
cantidad, quitar, total, cantidad de items, vaciar, y un cupón de descuento que solo se
puede aplicar una vez y solo si el total supera 20 000) **junto con** su clase de
pruebas `CarritoTest`, con al menos ocho pruebas que cubran los casos normales, los
bordes y los errores. Entregá las dos en un zip.

#### Criterio de aprobación

- Ocho pruebas o más, todas pasando.
- Se prueban el límite de 20 000 y el cupón aplicado dos veces.

#### Solución de referencia

`Carrito.java`

```java
import java.util.LinkedHashMap;
import java.util.Map;

public class Carrito {
    private final Map<String, Integer> cantidades = new LinkedHashMap<>();
    private final Map<String, Double> precios = new LinkedHashMap<>();
    private double descuento = 0;

    public void agregar(String producto, double precio, int cantidad) {
        if (precio < 0 || cantidad <= 0) {
            throw new IllegalArgumentException("precio o cantidad inválidos");
        }
        cantidades.merge(producto, cantidad, Integer::sum);
        precios.put(producto, precio);
    }

    public void quitar(String producto) {
        cantidades.remove(producto);
        precios.remove(producto);
    }

    public int items() {
        int total = 0;
        for (int c : cantidades.values()) {
            total += c;
        }
        return total;
    }

    public double subtotal() {
        double total = 0;
        for (String p : cantidades.keySet()) {
            total += cantidades.get(p) * precios.get(p);
        }
        return total;
    }

    public void aplicarCupon(double porcentaje) {
        if (descuento > 0) {
            throw new IllegalStateException("el cupón ya se aplicó");
        }
        if (subtotal() <= 20000) {
            throw new IllegalStateException("el cupón es para compras de más de 20000");
        }
        descuento = porcentaje / 100;
    }

    public double total() {
        return subtotal() * (1 - descuento);
    }

    public void vaciar() {
        cantidades.clear();
        precios.clear();
        descuento = 0;
    }
}
```

`CarritoTest.java`

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class CarritoTest {
    private Carrito c;

    @BeforeEach
    void preparar() {
        c = new Carrito();
    }

    @Test
    void unCarritoNuevoEstaVacio() {
        assertEquals(0, c.items());
        assertEquals(0.0, c.total(), 0.001);
    }

    @Test
    void agregarSumaItemsYTotal() {
        c.agregar("taza", 3000, 2);
        assertEquals(2, c.items());
        assertEquals(6000.0, c.total(), 0.001);
    }

    @Test
    void agregarElMismoProductoAcumula() {
        c.agregar("taza", 3000, 1);
        c.agregar("taza", 3000, 2);
        assertEquals(3, c.items());
    }

    @Test
    void quitarSacaElProducto() {
        c.agregar("taza", 3000, 1);
        c.agregar("pava", 8000, 1);
        c.quitar("taza");
        assertEquals(8000.0, c.total(), 0.001);
    }

    @Test
    void cantidadCeroEsUnError() {
        assertThrows(IllegalArgumentException.class, () -> c.agregar("taza", 3000, 0));
    }

    @Test
    void elCuponNoSeAplicaEn20000Justos() {
        c.agregar("lámpara", 20000, 1);
        assertThrows(IllegalStateException.class, () -> c.aplicarCupon(10));
    }

    @Test
    void elCuponDescuentaSobreMasDe20000() {
        c.agregar("lámpara", 25000, 1);
        c.aplicarCupon(10);
        assertEquals(22500.0, c.total(), 0.001);
    }

    @Test
    void elCuponNoSeAplicaDosVeces() {
        c.agregar("lámpara", 25000, 1);
        c.aplicarCupon(10);
        assertThrows(IllegalStateException.class, () -> c.aplicarCupon(10));
    }

    @Test
    void vaciarDejaTodoEnCero() {
        c.agregar("lámpara", 25000, 1);
        c.aplicarCupon(10);
        c.vaciar();
        assertEquals(0, c.items());
        assertEquals(0.0, c.total(), 0.001);
    }
}
```

### Prueba del sello

#### ¿Qué es una regresión?

Un error que aparece en algo que ya funcionaba, después de cambiar otra parte del código.

#### ¿Por qué `assertEquals` con `double` lleva un tercer parámetro?

Porque los decimales no son exactos: el tercer parámetro es el margen de error aceptado.

#### ¿Para qué sirve `@BeforeEach`?

Para preparar los objetos antes de cada prueba, así cada una arranca de cero y no depende de las otras.

#### ¿Cómo se prueba que un método lanza una excepción?

Con `assertThrows(TipoDeExcepcion.class, () -> codigo)`.

#### ¿Qué casos conviene probar además del normal?

Los bordes (0, vacío, el límite exacto de una regla) y los errores.

### Soluciones (docente)

Nodo nuevo (el 24 del índice de `18-Java` estaba por crear, bloque "Tribunal de las Pruebas"). Las pruebas se verificaron con JUnit 5 (*junit-platform-console-standalone* 1.11). En la misión 2, los dos errores son el `>=` del borde de 10 000 y el orden de las condiciones (el `else if (monto > 50000)` nunca se alcanza); la validación de negativos es el tercer pedido de la consigna.

## R03-N07 · Depuración, logging y Javadoc

```meta
tipo: tema
padre: R03-N06
precio: 10
criatura: ogre
```

### Crónica

En el ala de los errores de los Archivos, un escriba lleva un **diario**: anota cada cosa que pasa, con la hora y la gravedad. Cuando algo se rompe, nadie adivina: leen el diario. Al lado, otra escriba recorre un programa **paso a paso**, deteniéndose en cada línea para mirar cuánto vale cada variable.

—Los ogros más traicioneros no rompen nada: el programa termina tranquilo, con el resultado equivocado —dice {mentor}—. Para cazarlos no alcanza con mirar el código. Hay que **ver qué pasa por dentro**, {heroe}.

### Objetivos

- Buscar errores con un método: reproducir, aislar, observar, corregir, probar.
- Usar el depurador de un IDE: puntos de interrupción, paso a paso y variables.
- Registrar lo que pasa con `java.util.logging` en lugar de `println`.
- Usar `assert` para verificar suposiciones.
- Documentar clases y métodos con Javadoc.

### Antes de empezar

- Pruebas con JUnit.

### Explicación

#### Un método para depurar
1. **Reproducí** el error: encontrá una entrada que siempre lo produzca.
2. **Aislá**: achicá el caso hasta el mínimo que todavía falla (una prueba de JUnit es
   ideal para esto).
3. **Observá**: mirá qué valen las variables en el camino (con el depurador o con
   mensajes).
4. **Corregí** la causa, no el síntoma.
5. **Probá**: dejá la prueba que lo reproducía, para que no vuelva.

#### El depurador
Todos los IDE (NetBeans, IntelliJ, VS Code) traen un **depurador**:
- **Punto de interrupción** (*breakpoint*): hacé clic en el margen de una línea; al
  ejecutar en modo depuración, el programa se detiene ahí.
- **Paso a paso**: *Step Over* ejecuta la línea y pasa a la siguiente; *Step Into*
  entra en el método que se llama en esa línea; *Step Out* termina el método actual.
- **Variables**: mientras está detenido, el panel muestra cuánto vale cada variable y
  cada atributo de los objetos.
- **Punto condicional**: se detiene solo si se cumple una condición (`i == 57`).

Ver el programa por dentro, línea por línea, es la forma más rápida de encontrar un
ogro de lógica.

#### Logging: un diario en lugar de `println`
Los `println` de depuración se olvidan en el código, se mezclan con la salida del
programa y no se pueden apagar. Un **logger** registra mensajes con un **nivel** de
gravedad, y se configura qué niveles mostrar sin tocar el código:
```java
import java.util.logging.Logger;

private static final Logger LOG = Logger.getLogger(Aduana.class.getName());

LOG.info("abriendo la aduana");
LOG.warning("carga sospechosa: " + kilos);
LOG.severe("no se pudo guardar el registro");
LOG.fine("detalle para depurar: tasa=" + tasa);     // oculto por defecto
```
| Nivel | Para |
|---|---|
| `SEVERE` | errores graves |
| `WARNING` | algo raro que no impide seguir |
| `INFO` | eventos importantes del funcionamiento normal |
| `CONFIG` | configuración |
| `FINE`, `FINER`, `FINEST` | detalles para depurar (ocultos por defecto) |

Por defecto se muestran de `INFO` para arriba, por la **salida de errores**
(`System.err`), con fecha y hora. `LOG.setLevel(Level.WARNING)` muestra solo los
graves. En las empresas se usan librerías como Log4j o SLF4J, con la misma idea.

#### `assert`: verificar suposiciones
```java
assert tasa >= 0 : "la tasa no puede ser negativa: " + tasa;
```
Si la condición es falsa, lanza un `AssertionError` con el mensaje. Ojo: los `assert`
están **apagados por defecto**; se prenden con `java -ea Programa`. Sirven para
verificar lo que "no puede pasar" mientras desarrollás, no para validar datos del
usuario (para eso, excepciones).

#### Javadoc: documentar
Un comentario `/** … */` justo antes de una clase o un método es **documentación**:
```java
/**
 * Calcula la tasa de la Aduana.
 *
 * @param kilos la carga en kilos; no puede ser negativa
 * @param urgente si el trámite es urgente (recargo de 10)
 * @return la tasa en denarios
 * @throws IllegalArgumentException si la carga es negativa
 */
public double calcularTasa(int kilos, boolean urgente) { … }
```
Los IDE la muestran al pasar el mouse sobre el método, y la herramienta `javadoc` arma
páginas web con toda la documentación:
```bash
javadoc -d docs *.java
```
Así está documentada toda la biblioteca de Java. Documentá **qué hace y cómo se
usa** (parámetros, retorno, excepciones), no cómo está programado por dentro.

### Código de ejemplo

```java
/*
 * Depuración, logging y Javadoc: el diario del escriba.
 * El log sale por la salida de errores; la salida normal del programa no se mezcla.
 */
import java.util.List;
import java.util.Locale;
import java.util.logging.Level;
import java.util.logging.Logger;

public class DiarioEscriba {
    private static final Logger LOG = Logger.getLogger(DiarioEscriba.class.getName());

    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        LOG.info("abriendo la aduana");
        List<Integer> cargas = List.of(30, 180, -5, 420);
        double total = 0;
        for (int kilos : cargas) {
            try {
                double tasa = calcularTasa(kilos, kilos > 400);
                System.out.printf("%4d kg -> %.2f%n", kilos, tasa);
                total += tasa;
            } catch (IllegalArgumentException e) {
                LOG.warning("carga descartada: " + e.getMessage());
                System.out.printf("%4d kg -> descartada%n", kilos);
            }
        }
        System.out.printf("Total: %.2f%n", total);

        LOG.setLevel(Level.WARNING);          // de acá en adelante, solo advertencias y errores
        LOG.info("este mensaje ya no se muestra");
        LOG.severe("cierre de emergencia de prueba");
    }

    /**
     * Calcula la tasa de la Aduana según la carga.
     *
     * @param kilos la carga en kilos; no puede ser negativa
     * @param urgente si el trámite es urgente (recargo de 10 denarios)
     * @return la tasa en denarios
     * @throws IllegalArgumentException si la carga es negativa
     */
    static double calcularTasa(int kilos, boolean urgente) {
        if (kilos < 0) {
            throw new IllegalArgumentException("carga negativa (" + kilos + ")");
        }
        double tasa = kilos <= 50 ? 5 : 5 + (kilos - 50) * 0.1;
        assert tasa >= 5 : "la tasa mínima es 5";
        LOG.fine("tasa calculada: " + tasa);          // oculto por defecto
        return urgente ? tasa + 10 : tasa;
    }
}
```

### Salida esperada

```
  30 kg -> 5.00
 180 kg -> 18.00
  -5 kg -> descartada
 420 kg -> 52.00
Total: 75.00
```

### ¿Para qué sirve?

Depurar es la tarea que más tiempo ocupa en la vida real de un programador: un método ordenado y un depurador bien usado ahorran horas. Los logs son lo único que queda cuando algo falla en un servidor a las tres de la mañana y nadie estaba mirando. Y la documentación con Javadoc es lo que permite que otros (y vos, dentro de seis meses) usen tus clases sin leer su código.

### Errores habituales

**Ogro: cambiar cosas al azar.** Cambiar líneas "a ver si anda" sin haber entendido la
causa esconde el error en vez de corregirlo. Primero reproducí y observá.

**Ogro: los `println` olvidados.** Los mensajes de depuración que quedan en el código
ensucian la salida (y rompen la comparación con la salida esperada). Usá el logger con
nivel `FINE`, o borralos.

**Ogro: el `assert` que nunca se ejecuta.** Sin `-ea`, los `assert` no hacen nada. No
los uses para validar datos.

**Ogro: el log que no aparece.** `LOG.fine(...)` no se muestra con la configuración por
defecto: el nivel mínimo es `INFO`.

**Slime: el Javadoc en el lugar equivocado.** Tiene que estar **inmediatamente antes**
del método o la clase, y empezar con `/**` (dos asteriscos).

### Misión R03-N07-M1 · El promedio que miente

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Este programa debería mostrar el promedio de notas de cada estudiante y quién tiene el
mejor promedio, pero da resultados raros. Tiene **tres errores**. Usá el depurador (o
mensajes con un logger) para encontrarlos, corregilos y agregá un comentario arriba de
cada corrección explicando qué estaba mal.

```java
public class Promedios {
    public static void main(String[] args) {
        String[] nombres = {"Kira", "Bron", "Lía"};
        int[][] notas = {{8, 9, 7}, {6, 5, 10}, {9, 9, 8}};
        double mejor = 0;
        String mejorNombre = "";
        for (int i = 0; i <= nombres.length - 1; i++) {
            int suma = 0;
            for (int j = 1; j < notas[i].length; j++) {
                suma += notas[i][j];
            }
            double promedio = suma / notas[i].length;
            System.out.println(nombres[i] + ": " + promedio);
            if (promedio > mejor) {
                mejorNombre = nombres[i];
            }
        }
        System.out.println("Mejor promedio: " + mejorNombre);
    }
}
```

#### Criterio de aprobación

- Corrige los tres errores (el índice del bucle interno, la división entera y el mejor que no se actualiza).
- Cada corrección tiene su comentario.

#### Salida esperada

```
Kira: 8.00
Bron: 7.00
Lía: 8.67
Mejor promedio: Lía
```

#### Solución de referencia

```java
// Mision 1 - El promedio que miente: tres errores de logica corregidos.
import java.util.Locale;

public class Promedios {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        String[] nombres = {"Kira", "Bron", "Lía"};
        int[][] notas = {{8, 9, 7}, {6, 5, 10}, {9, 9, 8}};
        double mejor = 0;
        String mejorNombre = "";
        for (int i = 0; i <= nombres.length - 1; i++) {
            int suma = 0;
            // Error 1: el bucle empezaba en j = 1 y salteaba la primera nota.
            for (int j = 0; j < notas[i].length; j++) {
                suma += notas[i][j];
            }
            // Error 2: suma / length era una division entera; hace falta un double.
            double promedio = (double) suma / notas[i].length;
            System.out.printf("%s: %.2f%n", nombres[i], promedio);
            if (promedio > mejor) {
                // Error 3: nunca se actualizaba "mejor", asi que ganaba el ultimo mayor a 0.
                mejor = promedio;
                mejorNombre = nombres[i];
            }
        }
        System.out.println("Mejor promedio: " + mejorNombre);
    }
}
```

### Misión R03-N07-M2 · El diario del depósito

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Agregale un **logger** a este depósito: `INFO` cuando entra o sale mercadería,
`WARNING` cuando se pide sacar más de lo que hay (la operación no se hace) y `SEVERE`
si se intenta cargar una cantidad negativa (la operación no se hace). La salida
**normal** del programa (lo que muestra `System.out`) tiene que ser solo el stock
final, así que no uses `println` para los avisos. Procesá las operaciones de la entrada
(`+ producto cantidad` o `- producto cantidad`) hasta una línea vacía.

#### Criterio de aprobación

- Usa `Logger` con los tres niveles pedidos.
- La salida estándar tiene solo el stock final.

#### Entrada de ejemplo

```
+ sal 10
+ tela 4
- sal 3
- tela 9
+ hierro -2
+ hierro 7

```

#### Salida esperada

```
Stock final: {hierro=7, sal=7, tela=4}
```

#### Solución de referencia

```java
// Mision 2 - El diario del deposito: logger con INFO, WARNING y SEVERE.
import java.util.Map;
import java.util.Scanner;
import java.util.TreeMap;
import java.util.logging.Logger;

public class DiarioDeposito {
    private static final Logger LOG = Logger.getLogger(DiarioDeposito.class.getName());

    public static void main(String[] args) {
        Map<String, Integer> stock = new TreeMap<>();
        Scanner teclado = new Scanner(System.in);
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.isEmpty()) {
                break;
            }
            String[] p = linea.split(" ");
            String producto = p[1];
            int cantidad = Integer.parseInt(p[2]);
            int hay = stock.getOrDefault(producto, 0);
            if (p[0].equals("+")) {
                if (cantidad < 0) {
                    LOG.severe("carga negativa de " + producto + ": " + cantidad);
                    continue;
                }
                stock.put(producto, hay + cantidad);
                LOG.info("entran " + cantidad + " de " + producto);
            } else {
                if (cantidad > hay) {
                    LOG.warning("no alcanza " + producto + ": piden " + cantidad + ", hay " + hay);
                    continue;
                }
                stock.put(producto, hay - cantidad);
                LOG.info("salen " + cantidad + " de " + producto);
            }
        }
        System.out.println("Stock final: " + stock);
    }
}
```

### Misión R03-N07-M3 · La documentación de la balanza

```meta
entrega: archivo
entorno: local
extensiones: zip, java
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Balanza` (capacidad máxima, peso actual, `cargar(double kg)`,
`descargar(double kg)`, `porcentajeDeUso()`) **completamente documentada con
Javadoc**: la clase, el constructor y cada método público, con `@param`, `@return` y
`@throws` donde corresponda. Generá la documentación con `javadoc -d docs
Balanza.java` y entregá un zip con el `.java` y la carpeta `docs/`.

#### Criterio de aprobación

- Todos los elementos públicos tienen Javadoc con las etiquetas correspondientes.
- `javadoc` genera la documentación sin advertencias.

#### Solución de referencia

```java
/**
 * Una balanza con capacidad máxima, como las del depósito de la Aduana.
 * El peso nunca puede ser negativo ni superar la capacidad.
 */
public class Balanza {
    private final double capacidad;
    private double peso;

    /**
     * Crea una balanza vacía.
     *
     * @param capacidad la carga máxima en kilos; tiene que ser positiva
     * @throws IllegalArgumentException si la capacidad no es positiva
     */
    public Balanza(double capacidad) {
        if (capacidad <= 0) {
            throw new IllegalArgumentException("la capacidad tiene que ser positiva");
        }
        this.capacidad = capacidad;
    }

    /**
     * Agrega carga a la balanza.
     *
     * @param kg los kilos a cargar; tienen que ser positivos
     * @throws IllegalArgumentException si los kilos no son positivos
     * @throws IllegalStateException si con esa carga se supera la capacidad
     */
    public void cargar(double kg) {
        if (kg <= 0) {
            throw new IllegalArgumentException("los kilos tienen que ser positivos");
        }
        if (peso + kg > capacidad) {
            throw new IllegalStateException("se supera la capacidad");
        }
        peso += kg;
    }

    /**
     * Saca carga de la balanza.
     *
     * @param kg los kilos a sacar; no pueden ser más que el peso actual
     * @throws IllegalArgumentException si los kilos no son positivos o superan el peso actual
     */
    public void descargar(double kg) {
        if (kg <= 0 || kg > peso) {
            throw new IllegalArgumentException("cantidad inválida para descargar");
        }
        peso -= kg;
    }

    /**
     * Devuelve el peso actual.
     *
     * @return los kilos que hay sobre la balanza
     */
    public double getPeso() {
        return peso;
    }

    /**
     * Calcula qué parte de la capacidad está en uso.
     *
     * @return el porcentaje de uso, entre 0 y 100
     */
    public double porcentajeDeUso() {
        return peso / capacidad * 100;
    }
}
```

### Encargo R03-N07-E1 · El reporte de errores

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un sistema de facturación recibe líneas `cliente;monto` y a veces vienen mal. Procesá
las líneas de la entrada hasta una vacía: las válidas se suman por cliente; las
inválidas (sin `;`, monto no numérico o negativo) se registran con el logger como
`WARNING` indicando el número de línea y el motivo, y se siguen procesando las demás.
Al final mostrá (por la salida estándar) el total por cliente y cuántas líneas se
descartaron.

#### Criterio de aprobación

- Ninguna línea mala corta el programa.
- Los avisos van por el logger, no por `System.out`.

#### Entrada de ejemplo

```
Marta;1500
Juan;abc
Ana;3200.5
sin separador
Marta;-40
Juan;800

```

#### Salida esperada

```
Ana      3200.50
Juan      800.00
Marta    1500.00
Líneas descartadas: 3
```

#### Solución de referencia

```java
// Encargo - El reporte de errores: seguir procesando y registrar con el logger.
import java.util.Locale;
import java.util.Map;
import java.util.Scanner;
import java.util.TreeMap;
import java.util.logging.Logger;

public class ReporteErrores {
    private static final Logger LOG = Logger.getLogger(ReporteErrores.class.getName());

    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Scanner teclado = new Scanner(System.in);
        Map<String, Double> totales = new TreeMap<>();
        int numero = 0;
        int descartadas = 0;
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.isEmpty()) {
                break;
            }
            numero++;
            String[] p = linea.split(";");
            try {
                if (p.length != 2) {
                    throw new IllegalArgumentException("falta el separador ;");
                }
                double monto = Double.parseDouble(p[1]);
                if (monto < 0) {
                    throw new IllegalArgumentException("monto negativo");
                }
                totales.merge(p[0], monto, Double::sum);
            } catch (IllegalArgumentException e) {
                descartadas++;
                LOG.warning("línea " + numero + " descartada (" + linea + "): " + e.getMessage());
            }
        }
        totales.forEach((cliente, total) -> System.out.printf("%-6s %9.2f%n", cliente, total));
        System.out.println("Líneas descartadas: " + descartadas);
    }
}
```

### Prueba del sello

#### ¿Cuáles son los pasos para depurar un error?

Reproducirlo, aislarlo en el caso mínimo, observar qué pasa, corregir la causa y dejar una prueba que lo cubra.

#### ¿Qué es un punto de interrupción?

Una marca en una línea donde el depurador detiene el programa para mirar el estado de las variables.

#### ¿Por qué conviene un logger en lugar de `println` para los mensajes de depuración?

Porque tiene niveles que se pueden apagar sin tocar el código, sale por un canal separado y registra la hora.

#### ¿Qué pasa con un `assert` si no ejecutás con `-ea`?

Nada: los `assert` están apagados por defecto.

#### ¿Qué etiquetas de Javadoc documentan los parámetros, el resultado y las excepciones?

`@param`, `@return` y `@throws`.

### Soluciones (docente)

Nodo nuevo (el 25 del índice de `18-Java` estaba por crear). Los mensajes del logger salen por `System.err`, así que no forman parte de la salida esperada (el súper test compara solo la salida estándar). El depurador se explica en general porque cada IDE lo muestra distinto; en clase conviene hacer la misión 1 en vivo con NetBeans.

## R03-N08 · Jefe: el Espectro Nulo

```meta
tipo: jefe
padre: R03-N07
precio: 10
criatura: dragon
insignia: Sello del Espectro
insignia_descripcion: Venciste al Espectro Nulo: tus colecciones no se rompen y tus errores se entienden.
```

### Crónica

En lo más profundo de los Archivos hay una sala donde los pergaminos desaparecen. Pedís uno, el archivista va a buscarlo, vuelve con las manos vacías… y el sistema entero se congela con un grito: *NullPointerException*. Es el **Espectro Nulo**: aparece justo donde alguien supuso que algo existía.

—No se lo vence corriendo detrás de cada `null` —dice {mentor}—. Se lo vence **diseñando** para que no aparezca: validando en la entrada, devolviendo colecciones vacías en lugar de `null`, lanzando errores que digan qué pasó, y probando cada camino. Cuando tus clases lo hagan solas, {heroe}, el Espectro no tiene dónde esconderse.

### Objetivos

- Integrar colecciones, excepciones propias, lambdas y pruebas en un sistema completo.
- Diseñar clases que no devuelvan ni acepten `null` sin control.
- Procesar comandos de texto con manejo de errores que no corte el programa.

### Antes de empezar

- Toda la rama: paquetes, listas, mapas, conjuntos, excepciones, lambdas, JUnit y depuración.

### Explicación

#### Cómo se esconde el Espectro
El `NullPointerException` aparece siempre por el mismo motivo: alguien usó una
referencia suponiendo que apuntaba a un objeto. Los escondites favoritos:
- un `mapa.get(clave)` con una clave que no existe;
- un método que devuelve `null` para decir "no encontré nada";
- un atributo que nadie inicializó;
- un parámetro que alguien pasó en `null`.

#### Cuatro reglas para que no aparezca
1. **Validá en la puerta.** Los constructores y métodos públicos rechazan `null` y datos
   inválidos con una excepción clara (`Objects.requireNonNull(x, "falta x")` lanza un
   `NullPointerException` con ese mensaje, **en el lugar correcto** y no diez líneas
   después).
2. **Nunca devuelvas `null` para una colección.** Si no hay resultados, devolvé una
   lista vacía (`List.of()` o `new ArrayList<>()`): quien la recorra no tiene que
   preguntar nada.
3. **Si "no encontrado" es un error, lanzalo.** `buscar(codigo)` puede lanzar una
   `NoEncontradoException` con el código que faltaba, en lugar de devolver `null`.
   (En la Senda de Java moderno vas a ver `Optional`, otra forma de decir "puede no
   haber".)
4. **Inicializá todo** en la declaración o en el constructor, y usá `final` donde se
   pueda.

#### Un procesador de comandos que no se cae
Los programas del jefe leen comandos y los ejecutan. El patrón:
```java
while (teclado.hasNextLine()) {
    String linea = teclado.nextLine().trim();
    if (linea.equals("salir")) break;
    try {
        ejecutar(linea);                         // puede lanzar excepciones del dominio
    } catch (BibliotecaException e) {
        System.out.println("Error: " + e.getMessage());
    } catch (RuntimeException e) {               // cualquier otro problema de la línea
        System.out.println("Comando inválido: " + linea);
    }
}
```
Un error en una línea se informa y el programa **sigue** con la próxima.

#### Una jerarquía de excepciones propias
Para un sistema, conviene una excepción base y varias hijas:
```java
class BibliotecaException extends Exception { … }
class LibroNoEncontradoException extends BibliotecaException { … }
class LibroPrestadoException extends BibliotecaException { … }
```
Quien llama puede atraparlas todas juntas (`catch (BibliotecaException e)`) o de a una.

### Código de ejemplo

```java
/*
 * Jefe de la rama 3: el registro de reliquias, a prueba de Espectros.
 */
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.TreeMap;

public class RegistroReliquias {
    public static void main(String[] args) {
        Registro registro = new Registro();
        registro.agregar(new Reliquia("R-01", "Cáliz de plata", 800));
        registro.agregar(new Reliquia("R-02", "Espada rota", 120));
        registro.agregar(new Reliquia("R-03", "Mapa estelar", 950));

        String[] pedidos = {"R-02", "R-09", "R-03"};
        for (String codigo : pedidos) {
            try {
                System.out.println("Encontrada: " + registro.buscar(codigo));
            } catch (ReliquiaNoEncontradaException e) {
                System.out.println("Error: " + e.getMessage());
            }
        }

        // Una colección vacía en lugar de null: nadie tiene que preguntar nada
        System.out.println("Anteriores al año 100: " + registro.masAntiguasQue(100));
        for (Reliquia r : registro.masAntiguasQue(900)) {
            System.out.println("Anterior al año 900: " + r);
        }

        // Validar en la puerta
        try {
            registro.agregar(new Reliquia(null, "Nada", 1));
        } catch (NullPointerException e) {
            System.out.println("Rechazada: " + e.getMessage());
        }
        try {
            registro.agregar(new Reliquia("R-01", "Copia del cáliz", 5));
        } catch (IllegalArgumentException e) {
            System.out.println("Rechazada: " + e.getMessage());
        }

        registro.porAntiguedad().forEach(r -> System.out.println("  " + r));
    }
}

class ReliquiaNoEncontradaException extends Exception {
    public ReliquiaNoEncontradaException(String codigo) {
        super("no hay ninguna reliquia con el código " + codigo);
    }
}

record Reliquia(String codigo, String nombre, int anio) {
    Reliquia {
        Objects.requireNonNull(codigo, "la reliquia necesita un código");
        Objects.requireNonNull(nombre, "la reliquia necesita un nombre");
    }

    @Override
    public String toString() {
        return codigo + " " + nombre + " (año " + anio + ")";
    }
}

class Registro {
    private final Map<String, Reliquia> reliquias = new TreeMap<>();

    public void agregar(Reliquia r) {
        Objects.requireNonNull(r, "reliquia nula");
        if (reliquias.containsKey(r.codigo())) {
            throw new IllegalArgumentException("ya existe el código " + r.codigo());
        }
        reliquias.put(r.codigo(), r);
    }

    public Reliquia buscar(String codigo) throws ReliquiaNoEncontradaException {
        Reliquia r = reliquias.get(codigo);
        if (r == null) {
            throw new ReliquiaNoEncontradaException(codigo);
        }
        return r;
    }

    public List<Reliquia> masAntiguasQue(int anio) {
        List<Reliquia> resultado = new ArrayList<>();          // nunca null: a lo sumo, vacía
        for (Reliquia r : reliquias.values()) {
            if (r.anio() < anio) {
                resultado.add(r);
            }
        }
        return resultado;
    }

    public List<Reliquia> porAntiguedad() {
        List<Reliquia> lista = new ArrayList<>(reliquias.values());
        lista.sort(Comparator.comparingInt(Reliquia::anio));
        return lista;
    }
}
```

### Salida esperada

```
Encontrada: R-02 Espada rota (año 120)
Error: no hay ninguna reliquia con el código R-09
Encontrada: R-03 Mapa estelar (año 950)
Anteriores al año 100: []
Anterior al año 900: R-01 Cáliz de plata (año 800)
Anterior al año 900: R-02 Espada rota (año 120)
Rechazada: la reliquia necesita un código
Rechazada: ya existe el código R-01
  R-02 Espada rota (año 120)
  R-01 Cáliz de plata (año 800)
  R-03 Mapa estelar (año 950)
```

### ¿Para qué sirve?

Todos los sistemas de gestión tienen esta forma: un registro de cosas (productos, clientes, turnos) con operaciones que pueden fallar por motivos del negocio. Un sistema que no devuelve `null`, valida en la entrada y lanza errores con nombre es un sistema que se puede mantener: cuando algo falla, el mensaje dice qué pasó y dónde.

### Errores habituales

**Dragón: el `null` que viaja.** Un método devuelve `null`, otro lo guarda, un tercero
lo pasa, y el `NullPointerException` explota lejos del origen. Cortalo en la puerta.

**Troll: `mapa.get` sin preguntar.** Toda búsqueda por clave tiene que contemplar que
la clave no exista.

**Ogro: atrapar `NullPointerException` para "arreglarlo".** Un `catch
(NullPointerException e)` esconde el error. Evitá que ocurra.

**Ogro: el `catch (Exception e)` que se traga todo.** En el procesador de comandos,
atrapá primero las excepciones de tu dominio con su mensaje, y dejá el genérico para
lo inesperado.

### Misión R03-N08-M1 · La biblioteca encantada

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Programá la biblioteca de los Archivos con estos comandos (uno por línea, hasta
`salir`):

- `alta CODIGO;TITULO;AUTOR` — agrega un libro (código único).
- `prestar CODIGO;SOCIO` — presta un libro a un socio.
- `devolver CODIGO` — lo devuelve.
- `socio SOCIO` — muestra los libros que tiene ese socio, ordenados por título (o
  `ninguno`).
- `disponibles` — muestra los libros no prestados, ordenados por autor y título.

Modelá: un `record Libro(String codigo, String titulo, String autor)` validado, una
clase `Biblioteca` con un `Map<String, Libro>` y un `Map<String, String>` de préstamos
(código → socio), y una jerarquía de excepciones checked: `BibliotecaException` con
las hijas `LibroNoEncontradoException`, `LibroPrestadoException` y
`LibroNoPrestadoException`. Ningún método devuelve `null`. Cada error se informa y el
programa sigue. Una línea mal formada muestra `Comando inválido`.

#### Criterio de aprobación

- Jerarquía de excepciones propias y un procesador de comandos que no se corta.
- Los listados se ordenan con `Comparator` y nunca son `null`.
- La salida coincide con la esperada.

#### Entrada de ejemplo

```
alta L1;Rayuela;Cortázar
alta L2;Ficciones;Borges
alta L3;El Aleph;Borges
alta L2;Repetido;Nadie
prestar L2;Kira
prestar L2;Bron
prestar L9;Bron
prestar L3;Kira
socio Kira
socio Bron
devolver L1
disponibles
devolver L2
disponibles
alta sin datos
salir
```

#### Salida esperada

```
Alta de L1
Alta de L2
Alta de L3
Error: ya existe el código L2
L2 prestado a Kira
Error: el libro L2 ya lo tiene Kira
Error: no existe el libro L9
L3 prestado a Kira
Kira: [El Aleph, Ficciones]
Bron: ninguno
Error: el libro L1 no estaba prestado
Disponibles: [Rayuela]
L2 devuelto
Disponibles: [Ficciones, Rayuela]
Comando inválido: alta sin datos
```

#### Solución de referencia

```java
// Jefe R03 - Mision 1: la biblioteca encantada.
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Scanner;
import java.util.TreeMap;

public class BibliotecaEncantada {
    public static void main(String[] args) {
        Biblioteca b = new Biblioteca();
        Scanner teclado = new Scanner(System.in);
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.equals("salir")) {
                break;
            }
            try {
                ejecutar(b, linea);
            } catch (BibliotecaException e) {
                System.out.println("Error: " + e.getMessage());
            } catch (RuntimeException e) {
                System.out.println("Comando inválido: " + linea);
            }
        }
    }

    static void ejecutar(Biblioteca b, String linea) throws BibliotecaException {
        String[] partes = linea.split(" ", 2);
        switch (partes[0]) {
            case "alta" -> {
                String[] d = partes[1].split(";");
                b.alta(new Libro(d[0], d[1], d[2]));
                System.out.println("Alta de " + d[0]);
            }
            case "prestar" -> {
                String[] d = partes[1].split(";");
                b.prestar(d[0], d[1]);
                System.out.println(d[0] + " prestado a " + d[1]);
            }
            case "devolver" -> {
                b.devolver(partes[1]);
                System.out.println(partes[1] + " devuelto");
            }
            case "socio" -> {
                List<Libro> libros = b.librosDe(partes[1]);
                System.out.println(partes[1] + ": " + (libros.isEmpty() ? "ninguno" : titulos(libros)));
            }
            case "disponibles" -> System.out.println("Disponibles: " + titulos(b.disponibles()));
            default -> throw new IllegalArgumentException("comando desconocido");
        }
    }

    static List<String> titulos(List<Libro> libros) {
        List<String> t = new ArrayList<>();
        libros.forEach(l -> t.add(l.titulo()));
        return t;
    }
}

class BibliotecaException extends Exception {
    public BibliotecaException(String mensaje) {
        super(mensaje);
    }
}

class LibroNoEncontradoException extends BibliotecaException {
    public LibroNoEncontradoException(String codigo) {
        super("no existe el libro " + codigo);
    }
}

class LibroPrestadoException extends BibliotecaException {
    public LibroPrestadoException(String codigo, String socio) {
        super("el libro " + codigo + " ya lo tiene " + socio);
    }
}

class LibroNoPrestadoException extends BibliotecaException {
    public LibroNoPrestadoException(String codigo) {
        super("el libro " + codigo + " no estaba prestado");
    }
}

record Libro(String codigo, String titulo, String autor) {
    Libro {
        Objects.requireNonNull(codigo);
        Objects.requireNonNull(titulo);
        Objects.requireNonNull(autor);
    }
}

class Biblioteca {
    private final Map<String, Libro> libros = new TreeMap<>();
    private final Map<String, String> prestamos = new HashMap<>();

    public void alta(Libro libro) throws BibliotecaException {
        if (libros.containsKey(libro.codigo())) {
            throw new BibliotecaException("ya existe el código " + libro.codigo());
        }
        libros.put(libro.codigo(), libro);
    }

    private Libro buscar(String codigo) throws LibroNoEncontradoException {
        Libro l = libros.get(codigo);
        if (l == null) {
            throw new LibroNoEncontradoException(codigo);
        }
        return l;
    }

    public void prestar(String codigo, String socio) throws BibliotecaException {
        buscar(codigo);
        String actual = prestamos.get(codigo);
        if (actual != null) {
            throw new LibroPrestadoException(codigo, actual);
        }
        prestamos.put(codigo, socio);
    }

    public void devolver(String codigo) throws BibliotecaException {
        buscar(codigo);
        if (prestamos.remove(codigo) == null) {
            throw new LibroNoPrestadoException(codigo);
        }
    }

    public List<Libro> librosDe(String socio) {
        List<Libro> lista = new ArrayList<>();
        prestamos.forEach((codigo, quien) -> {
            if (quien.equals(socio)) {
                lista.add(libros.get(codigo));
            }
        });
        lista.sort(Comparator.comparing(Libro::titulo));
        return lista;
    }

    public List<Libro> disponibles() {
        List<Libro> lista = new ArrayList<>();
        for (Libro l : libros.values()) {
            if (!prestamos.containsKey(l.codigo())) {
                lista.add(l);
            }
        }
        lista.sort(Comparator.comparing(Libro::autor).thenComparing(Libro::titulo));
        return lista;
    }
}
```

### Misión R03-N08-M2 · El Espectro en el código

```meta
entrega: archivo
entorno: local
extensiones: zip, java
monedas: 6
xp: 30
```

#### Consigna

Esta clase `Agenda` guarda los turnos de un consultorio y está **llena de escondites
del Espectro**: métodos que devuelven `null`, un mapa que se consulta sin preguntar,
un atributo sin inicializar. Escribí primero una clase de pruebas `AgendaTest` que
muestre los `NullPointerException` (con `assertThrows` o pruebas que fallen), después
**rediseñá** `Agenda` con las cuatro reglas del nodo (validar en la puerta, colecciones
vacías en lugar de `null`, excepción propia `TurnoInexistenteException` para lo que no
se encuentra, todo inicializado) y dejá pruebas que verifiquen el comportamiento nuevo.
Entregá las dos clases corregidas.

```java
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Agenda {
    private Map<String, List<String>> turnosPorDia;       // dia -> pacientes

    public void agendar(String dia, String paciente) {
        if (turnosPorDia == null) {
            turnosPorDia = new HashMap<>();
        }
        turnosPorDia.get(dia).add(paciente);
    }

    public List<String> turnosDel(String dia) {
        return turnosPorDia.get(dia);
    }

    public String primerTurno(String dia) {
        List<String> t = turnosPorDia.get(dia);
        return t.isEmpty() ? null : t.get(0);
    }

    public int cantidad(String dia) {
        return turnosDel(dia).size();
    }
}
```

#### Criterio de aprobación

- La `Agenda` nueva nunca devuelve `null` ni lanza `NullPointerException` por un día sin turnos.
- `agendar` crea la lista del día si no existe y rechaza datos vacíos.
- `primerTurno` lanza `TurnoInexistenteException` (checked) si no hay turnos.
- Las pruebas cubren todos los métodos y pasan.

#### Solución de referencia

`TurnoInexistenteException.java`

```java
public class TurnoInexistenteException extends Exception {
    public TurnoInexistenteException(String dia) {
        super("no hay turnos el " + dia);
    }
}
```

`Agenda.java`

```java
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Agenda {
    private final Map<String, List<String>> turnosPorDia = new HashMap<>();   // siempre inicializado

    public void agendar(String dia, String paciente) {
        if (dia == null || dia.isBlank() || paciente == null || paciente.isBlank()) {
            throw new IllegalArgumentException("día y paciente son obligatorios");
        }
        turnosPorDia.computeIfAbsent(dia, d -> new ArrayList<>()).add(paciente);
    }

    public List<String> turnosDel(String dia) {
        return List.copyOf(turnosPorDia.getOrDefault(dia, List.of()));    // nunca null
    }

    public String primerTurno(String dia) throws TurnoInexistenteException {
        List<String> turnos = turnosDel(dia);
        if (turnos.isEmpty()) {
            throw new TurnoInexistenteException(dia);
        }
        return turnos.get(0);
    }

    public int cantidad(String dia) {
        return turnosDel(dia).size();
    }
}
```

`AgendaTest.java`

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class AgendaTest {
    private Agenda agenda;

    @BeforeEach
    void preparar() {
        agenda = new Agenda();
    }

    @Test
    void agendarEnUnDiaNuevoCreaLaLista() {
        agenda.agendar("lunes", "Marta");
        assertEquals(List.of("Marta"), agenda.turnosDel("lunes"));
    }

    @Test
    void unDiaSinTurnosDevuelveListaVacia() {
        assertTrue(agenda.turnosDel("martes").isEmpty());
        assertEquals(0, agenda.cantidad("martes"));
    }

    @Test
    void elPrimerTurnoEsElPrimeroAgendado() throws TurnoInexistenteException {
        agenda.agendar("lunes", "Marta");
        agenda.agendar("lunes", "Juan");
        assertEquals("Marta", agenda.primerTurno("lunes"));
    }

    @Test
    void primerTurnoDeUnDiaVacioEsUnError() {
        assertThrows(TurnoInexistenteException.class, () -> agenda.primerTurno("viernes"));
    }

    @Test
    void noSeAgendaSinPaciente() {
        assertThrows(IllegalArgumentException.class, () -> agenda.agendar("lunes", " "));
        assertThrows(IllegalArgumentException.class, () -> agenda.agendar(null, "Ana"));
    }

    @Test
    void laListaDevueltaNoModificaLaAgenda() {
        agenda.agendar("lunes", "Marta");
        List<String> copia = agenda.turnosDel("lunes");
        assertThrows(UnsupportedOperationException.class, () -> copia.add("Intruso"));
        assertEquals(1, agenda.cantidad("lunes"));
    }
}
```

### Encargo R03-N08-E1 · La agenda de contactos

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 30
```

#### Consigna

Programá una agenda de contactos de consola con comandos hasta `salir`: `nuevo
NOMBRE;TELEFONO;ETIQUETAS` (etiquetas separadas por comas, pueden ser ninguna),
`buscar TEXTO` (contactos cuyo nombre contiene el texto, sin importar mayúsculas),
`etiqueta ETIQUETA` (los que tienen esa etiqueta), `borrar NOMBRE` y `etiquetas`
(todas las etiquetas usadas, sin repetir y ordenadas). El teléfono tiene que tener
entre 8 y 13 dígitos (con guiones opcionales) y el nombre no puede repetirse. Usá un
`Map` de contactos, un `Set` de etiquetas por contacto, excepciones propias para los
errores y lambdas para filtrar y ordenar. Ningún listado es `null`.

#### Criterio de aprobación

- Usa `Map`, `Set`, excepciones propias y lambdas.
- Los errores se informan y el programa sigue.

#### Entrada de ejemplo

```
nuevo Marta Díaz;380-4111222;familia,club
nuevo Juan Pérez;11-5555-6666;trabajo
nuevo Ana Ruiz;3804;club
nuevo Leo Paz;3804999888;
nuevo marta díaz;3804000000;
buscar ma
etiqueta club
etiquetas
borrar Juan Pérez
borrar Nadie
buscar a
salir
```

#### Salida esperada

```
Agregado: Marta Díaz
Agregado: Juan Pérez
Error: teléfono inválido: 3804
Agregado: Leo Paz
Error: ya existe marta díaz
Buscar 'ma': [Marta Díaz (380-4111222)]
Etiqueta club: [Marta Díaz (380-4111222)]
Etiquetas: [club, familia, trabajo]
Borrado: Juan Pérez
Error: no existe Nadie
Buscar 'a': [Leo Paz (3804999888), Marta Díaz (380-4111222)]
```

#### Solución de referencia

```java
// Jefe R03 - Encargo: la agenda de contactos.
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;

public class AgendaContactos {
    public static void main(String[] args) {
        Agenda agenda = new Agenda();
        Scanner teclado = new Scanner(System.in);
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.equals("salir")) {
                break;
            }
            String[] p = linea.split(" ", 2);
            try {
                switch (p[0]) {
                    case "nuevo" -> {
                        String[] d = p[1].split(";", -1);
                        agenda.nuevo(d[0], d[1], d[2]);
                        System.out.println("Agregado: " + d[0]);
                    }
                    case "buscar" -> System.out.println("Buscar '" + p[1] + "': " + agenda.buscar(p[1]));
                    case "etiqueta" -> System.out.println("Etiqueta " + p[1] + ": " + agenda.conEtiqueta(p[1]));
                    case "etiquetas" -> System.out.println("Etiquetas: " + agenda.etiquetas());
                    case "borrar" -> {
                        agenda.borrar(p[1]);
                        System.out.println("Borrado: " + p[1]);
                    }
                    default -> System.out.println("Comando inválido: " + linea);
                }
            } catch (AgendaException e) {
                System.out.println("Error: " + e.getMessage());
            }
        }
    }
}

class AgendaException extends Exception {
    public AgendaException(String mensaje) {
        super(mensaje);
    }
}

record Contacto(String nombre, String telefono, Set<String> etiquetas) {
    @Override
    public String toString() {
        return nombre + " (" + telefono + ")";
    }
}

class Agenda {
    private final Map<String, Contacto> contactos = new TreeMap<>(String.CASE_INSENSITIVE_ORDER);

    public void nuevo(String nombre, String telefono, String etiquetas) throws AgendaException {
        if (nombre.isBlank()) {
            throw new AgendaException("el nombre es obligatorio");
        }
        if (!telefono.replace("-", "").matches("\\d{8,13}")) {
            throw new AgendaException("teléfono inválido: " + telefono);
        }
        if (contactos.containsKey(nombre)) {
            throw new AgendaException("ya existe " + nombre);
        }
        Set<String> tags = new TreeSet<>();
        for (String t : etiquetas.split(",")) {
            if (!t.isBlank()) {
                tags.add(t.trim().toLowerCase());
            }
        }
        contactos.put(nombre, new Contacto(nombre, telefono, tags));
    }

    public List<Contacto> buscar(String texto) {
        List<Contacto> r = new ArrayList<>();
        contactos.values().forEach(c -> {
            if (c.nombre().toLowerCase().contains(texto.toLowerCase())) {
                r.add(c);
            }
        });
        return r;
    }

    public List<Contacto> conEtiqueta(String etiqueta) {
        List<Contacto> r = new ArrayList<>(contactos.values());
        r.removeIf(c -> !c.etiquetas().contains(etiqueta.toLowerCase()));
        r.sort(Comparator.comparing(Contacto::nombre));
        return r;
    }

    public Set<String> etiquetas() {
        Set<String> todas = new TreeSet<>();
        contactos.values().forEach(c -> todas.addAll(c.etiquetas()));
        return todas;
    }

    public void borrar(String nombre) throws AgendaException {
        if (contactos.remove(nombre) == null) {
            throw new AgendaException("no existe " + nombre);
        }
    }
}
```

### Prueba del sello

#### ¿Por qué conviene devolver una lista vacía en lugar de `null`?

Porque quien la recibe la puede recorrer sin preguntar nada; con `null`, cualquier uso sin verificar lanza `NullPointerException`.

#### ¿Qué hace `Objects.requireNonNull(x, "mensaje")`?

Lanza un `NullPointerException` con ese mensaje si `x` es `null`, en el lugar donde se valida.

#### ¿Qué ventaja tiene una jerarquía de excepciones propias?

Que quien llama puede atraparlas todas juntas con la excepción base o de a una con las hijas.

#### En un procesador de comandos, ¿cómo evitás que un error corte el programa?

Envolviendo la ejecución de cada línea en un `try`/`catch` dentro del bucle, e informando el error.

### Soluciones (docente)

Jefe nuevo de la rama 3 (el Espectro Nulo del guion). La misión 2 se corrige corriendo las pruebas del alumno contra su `Agenda` y, si se quiere, contra la de referencia. `String.CASE_INSENSITIVE_ORDER` en el encargo hace que "Marta Díaz" y "marta díaz" sean la misma clave del mapa.

