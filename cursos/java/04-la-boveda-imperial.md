# RAMA R04 · La Bóveda Imperial: archivos y bases de datos

```meta
tipo: tronco
posicion: 4
```

## R04-N01 · Archivos de texto, CSV y .properties

```meta
tipo: tema
padre: R03-N08
precio: 10
criatura: goblin
temas: arch.texto, arch.csv, arch.config
```

### Crónica

Bajo el palacio de los Archivos hay una escalera de piedra que baja a la **Bóveda Imperial**, donde se guarda todo lo que el Imperio no puede olvidar. En el primer piso, los escribas copian registros en libros: cada renglón, un dato; cada dato, separado por comas.

—Hasta ahora tus programas olvidaban todo al terminar —dice {mentor}—. Lo que queda en un **archivo** sobrevive. Pero cuidado, {heroe}: los archivos se corrompen, las líneas vienen mal y los discos se llenan. Leé siempre como si alguien hubiera escrito mal.

### Objetivos

- Leer y escribir archivos de texto con `Files` y `Path`.
- Leer archivos grandes línea por línea con `BufferedReader` y `try` con recursos.
- Leer y escribir archivos CSV validando cada línea.
- Guardar configuración en un archivo `.properties`.

### Antes de empezar

- Excepciones, `try` con recursos y colecciones (rama 3).

### Explicación

#### `Path` y `Files`
`Path` representa una ruta de archivo; `Files` tiene los métodos para usarla
(`import java.nio.file.*;`):
```java
Path ruta = Path.of("datos", "partidas.txt");       // datos/partidas.txt
Files.exists(ruta);
Files.createDirectories(ruta.getParent());         // crea las carpetas que falten

Files.writeString(ruta, "Kira;30\nBron;45\n");       // escribe (reemplaza el contenido)
Files.writeString(ruta, "Lía;20\n", StandardOpenOption.APPEND);   // agrega al final

String todo = Files.readString(ruta);                // lee todo como un texto
List<String> lineas = Files.readAllLines(ruta);      // una línea por elemento
Files.delete(ruta);
```
Todos lanzan `IOException` (checked): hay que atraparla o declararla. Las rutas
relativas (`datos/partidas.txt`) se buscan desde la carpeta **donde se ejecuta** el
programa. Java usa UTF-8 para leer y escribir texto con estos métodos.

#### Línea por línea: `BufferedReader` y `BufferedWriter`
`readAllLines` carga todo el archivo en memoria. Para archivos grandes, se lee de a una
línea, y **siempre** con `try` con recursos para que el archivo se cierre:
```java
try (BufferedReader lector = Files.newBufferedReader(ruta)) {
    String linea;
    while ((linea = lector.readLine()) != null) {    // null = se terminó el archivo
        procesar(linea);
    }
}
try (BufferedWriter escritor = Files.newBufferedWriter(ruta)) {
    escritor.write("Kira;30");
    escritor.newLine();
}
```

#### CSV: datos separados por comas
Un **CSV** (*comma-separated values*) es un archivo de texto donde cada línea es un
registro y los campos se separan con coma (o, en países que usan coma decimal, con
punto y coma). Lo abren Excel y LibreOffice, y es la forma más simple de intercambiar
datos.
```
nombre;clase;vida
Kira;arquera;30
Bron;guerrero;45
```
Leerlo es `split(";")` en cada línea, pero **hay que validar** cada una: puede faltar
un campo, sobrar un espacio o venir una letra donde iba un número. Una línea mala no
tiene que romper todo el archivo: se informa y se sigue.

(Un CSV "de verdad" puede tener campos entre comillas con el separador adentro:
`"Díaz; Marta";30`. Para esos casos se usa una librería como OpenCSV; en este curso
trabajamos con CSV simples.)

#### `.properties`: la configuración
Un archivo `.properties` guarda pares `clave=valor`, uno por línea, y se usa para la
**configuración** de un programa (así no se escribe en el código):
```
# configuración de la Bóveda
url=jdbc:postgresql://localhost:5432/imperio
usuario=imperio
intentos=3
```
```java
Properties config = new Properties();
try (BufferedReader r = Files.newBufferedReader(Path.of("boveda.properties"))) {
    config.load(r);
}
String url = config.getProperty("url");
int intentos = Integer.parseInt(config.getProperty("intentos", "1"));   // con valor por defecto
```
Es la forma recomendada de guardar los datos de conexión a la base de datos, que vas
a usar en los próximos nodos.

> **Si venís de Python.** `Files.readAllLines` es `open(...).readlines()`, y el `try`
> con recursos es el `with open(...) as f`. `Properties` se parece a `configparser`.

### Código de ejemplo

Para probarlo, creá un archivo `partidas.csv` en la misma carpeta con este contenido:

`partidas.csv`

```
heroe;enemigo;danio
Kira;goblin;12
Bron;orco;30
Lía;slime;x
Kira;orco;18
Olmo
Bron;goblin;9
```

```java
/*
 * Archivos: el primer piso de la Bóveda.
 * Lee un CSV validando cada línea, escribe un resumen y usa un .properties.
 */
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.TreeMap;

public class PrimerPiso {
    public static void main(String[] args) throws IOException {
        Path csv = Path.of("partidas.csv");
        Map<String, Integer> danioPorHeroe = new TreeMap<>();
        int numero = 0;

        try (BufferedReader lector = Files.newBufferedReader(csv)) {
            String linea = lector.readLine();                 // la primera línea es el encabezado
            while ((linea = lector.readLine()) != null) {
                numero++;
                String[] campos = linea.split(";");
                if (campos.length != 3) {
                    System.out.println("Línea " + numero + " descartada: faltan campos");
                    continue;
                }
                try {
                    int danio = Integer.parseInt(campos[2].trim());
                    danioPorHeroe.merge(campos[0].trim(), danio, Integer::sum);
                } catch (NumberFormatException e) {
                    System.out.println("Línea " + numero + " descartada: daño '" + campos[2] + "' no es un número");
                }
            }
        }
        System.out.println("Daño por héroe: " + danioPorHeroe);

        // Escribir un resumen
        Path resumen = Path.of("resumen.txt");
        try (BufferedWriter escritor = Files.newBufferedWriter(resumen)) {
            for (Map.Entry<String, Integer> e : danioPorHeroe.entrySet()) {
                escritor.write(e.getKey() + " hizo " + e.getValue() + " de daño");
                escritor.newLine();
            }
        }
        List<String> leido = Files.readAllLines(resumen);
        System.out.println("El resumen tiene " + leido.size() + " líneas; la primera: " + leido.get(0));

        // Configuración en un .properties
        Path archivoConfig = Path.of("boveda.properties");
        Files.writeString(archivoConfig, "# configuración de la Bóveda\nnombre=Bóveda Imperial\npisos=3\n");
        Properties config = new Properties();
        try (BufferedReader r = Files.newBufferedReader(archivoConfig)) {
            config.load(r);
        }
        System.out.println(config.getProperty("nombre") + ", " + config.getProperty("pisos") + " pisos, guardia: "
                + config.getProperty("guardia", "sin asignar"));

        Files.delete(resumen);
        Files.delete(archivoConfig);
    }
}
```

### Salida esperada

```
Línea 3 descartada: daño 'x' no es un número
Línea 5 descartada: faltan campos
Daño por héroe: {Bron=39, Kira=30}
El resumen tiene 2 líneas; la primera: Bron hizo 39 de daño
Bóveda Imperial, 3 pisos, guardia: sin asignar
```

### ¿Para qué sirve?

Todo sistema guarda algo en archivos: la configuración, los registros de actividad (*logs*), los datos que se exportan a Excel, los que se importan de otro sistema. Leer un CSV validando cada línea es una tarea diaria en cualquier empresa (cargar un padrón, una lista de precios del proveedor, las ventas del día).

### Errores habituales

**Goblin: el archivo que no está.**
```
Exception in thread "main" java.nio.file.NoSuchFileException: partidas.csv
```
La ruta relativa se busca desde la carpeta donde ejecutás. Revisá dónde estás parado
(`pwd`) o usá una ruta absoluta.

**Orco: el campo que falta.** `campos[2]` en una línea con dos campos corta con
`ArrayIndexOutOfBoundsException`. Validá `campos.length` antes.

**Troll: el archivo que no se cierra.** Sin `try` con recursos, un error deja el
archivo abierto y, en Windows, bloqueado.

**Ogro: `writeString` que borra todo.** Por defecto reemplaza el contenido. Para
agregar: `StandardOpenOption.APPEND`.

**Goblin: los espacios de más.** `" 30"` no es un número para `parseInt`: hacé `trim()`
de cada campo.

### Misión R04-N01-M1 · El padrón de la frontera

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El archivo `padron.csv` (con encabezado) tiene viajeros con `nombre;edad;ciudad`. Leelo
**línea por línea**, descartando (e informando con el número de línea) las que no
tienen tres campos o tienen una edad que no es un número o está fuera de 0 a 120.
Mostrá cuántos viajeros válidos hay por ciudad (ordenado) y la edad promedio con un
decimal. Después escribí los válidos **mayores de edad** en `mayores.csv` (con
encabezado) y mostrá cuántas líneas tiene el archivo escrito.

`padron.csv`

```
nombre;edad;ciudad
Kira;19;Valle
Bron;45;Forjas
Pip;12;Valle
Lía;veinte;Valle
Nara;33;Ciudadela
Olmo;140;Forjas
Tesla;38;Ciudadela
Ada
```

#### Criterio de aprobación

- Lee con `BufferedReader` y `try` con recursos.
- Valida cada línea sin cortar el programa.
- Escribe el archivo nuevo con encabezado.

#### Salida esperada

```
Línea 5: edad inválida 'veinte'
Línea 7: edad fuera de rango (140)
Línea 9: faltan campos
Por ciudad: {Ciudadela=2, Forjas=1, Valle=2}
Edad promedio: 29.4
mayores.csv tiene 5 líneas
```

#### Solución de referencia

`padron.csv`

```
nombre;edad;ciudad
Kira;19;Valle
Bron;45;Forjas
Pip;12;Valle
Lía;veinte;Valle
Nara;33;Ciudadela
Olmo;140;Forjas
Tesla;38;Ciudadela
Ada
```

```java
// Mision 1 - El padron de la frontera: leer un CSV validando y escribir otro.
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.TreeMap;

public class Padron {
    public static void main(String[] args) throws IOException {
        Locale.setDefault(Locale.US);
        Map<String, Integer> porCiudad = new TreeMap<>();
        List<String> mayores = new ArrayList<>();
        int sumaEdades = 0;
        int validos = 0;
        int numero = 1;
        try (BufferedReader r = Files.newBufferedReader(Path.of("padron.csv"))) {
            String linea = r.readLine();
            while ((linea = r.readLine()) != null) {
                numero++;
                String[] c = linea.split(";");
                if (c.length != 3) {
                    System.out.println("Línea " + numero + ": faltan campos");
                    continue;
                }
                int edad;
                try {
                    edad = Integer.parseInt(c[1].trim());
                } catch (NumberFormatException e) {
                    System.out.println("Línea " + numero + ": edad inválida '" + c[1] + "'");
                    continue;
                }
                if (edad < 0 || edad > 120) {
                    System.out.println("Línea " + numero + ": edad fuera de rango (" + edad + ")");
                    continue;
                }
                validos++;
                sumaEdades += edad;
                porCiudad.merge(c[2].trim(), 1, Integer::sum);
                if (edad >= 18) {
                    mayores.add(linea);
                }
            }
        }
        System.out.println("Por ciudad: " + porCiudad);
        System.out.printf("Edad promedio: %.1f%n", (double) sumaEdades / validos);

        Path salida = Path.of("mayores.csv");
        try (BufferedWriter w = Files.newBufferedWriter(salida)) {
            w.write("nombre;edad;ciudad");
            w.newLine();
            for (String m : mayores) {
                w.write(m);
                w.newLine();
            }
        }
        System.out.println("mayores.csv tiene " + Files.readAllLines(salida).size() + " líneas");
    }
}
```

### Misión R04-N01-M2 · El diario de la posada

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La posada anota cada huésped que llega en `diario.txt`. Leé nombres de la entrada
(uno por línea, hasta una vacía) y **agregalos** al final del diario (sin borrar lo que
había) con la hora de llegada que viene en la misma línea: `Kira 21:30`. Si el diario
no existe, crealo con un título. Al final, leé el diario entero y mostralo numerando
las líneas. Para que la prueba sea repetible, borrá el diario al empezar.

#### Criterio de aprobación

- Usa `StandardOpenOption.APPEND` (o `CREATE` + `APPEND`) para agregar.
- Crea el archivo con título si no existe.

#### Entrada de ejemplo

```
Kira 21:30
Bron 22:05
Lía 23:40

```

#### Salida esperada

```
1. == Diario de la posada La Taza ==
2. 21:30 llegó Kira
3. 22:05 llegó Bron
4. 23:40 llegó Lía
```

#### Solución de referencia

```java
// Mision 2 - El diario de la posada: agregar al final de un archivo.
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.List;
import java.util.Scanner;

public class DiarioPosada {
    public static void main(String[] args) throws IOException {
        Path diario = Path.of("diario.txt");
        Files.deleteIfExists(diario);                 // para que cada prueba arranque igual
        Scanner teclado = new Scanner(System.in);
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.isEmpty()) {
                break;
            }
            if (!Files.exists(diario)) {
                Files.writeString(diario, "== Diario de la posada La Taza ==\n");
            }
            String[] p = linea.split(" ");
            Files.writeString(diario, p[1] + " llegó " + p[0] + "\n", StandardOpenOption.APPEND);
        }
        List<String> lineas = Files.readAllLines(diario);
        for (int i = 0; i < lineas.size(); i++) {
            System.out.println((i + 1) + ". " + lineas.get(i));
        }
    }
}
```

#### Pruebas

##### Un solo huésped
```entrada
Pip 08:00
```
```salida
1. == Diario de la posada La Taza ==
2. 08:00 llegó Pip
```


### Misión R04-N01-M3 · La configuración del juego

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un juego guarda su configuración en `juego.properties`. Escribí un programa que lo
lea y muestre la dificultad, el volumen y el nombre del jugador, usando valores por
defecto para lo que falte (`dificultad` normal, `volumen` 50, `jugador` Anónimo). El
volumen tiene que ser un número de 0 a 100: si no lo es, se usa 50 y se avisa. Después
**cambiá** la dificultad a `dificil`, guardá el archivo con `store` y volvé a leerlo
para mostrar que quedó guardado.

`juego.properties`

```
# configuración del Arcade Imperial
jugador=Kira
volumen=muy alto
```

#### Criterio de aprobación

- Usa `Properties` con `load`, `getProperty` con valor por defecto, `setProperty` y `store`.
- Valida el volumen.

#### Salida esperada

```
Jugador: Kira
Dificultad: normal
Volumen inválido, uso 50
Volumen: 50
Guardado: dificultad=dificil, volumen=50
```

#### Solución de referencia

`juego.properties`

```
# configuración del Arcade Imperial
jugador=Kira
volumen=muy alto
```

```java
// Mision 3 - La configuracion del juego: Properties con valores por defecto y store.
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;

public class ConfigJuego {
    public static void main(String[] args) throws IOException {
        Path ruta = Path.of("juego.properties");
        Properties p = leer(ruta);
        System.out.println("Jugador: " + p.getProperty("jugador", "Anónimo"));
        System.out.println("Dificultad: " + p.getProperty("dificultad", "normal"));
        int volumen = 50;
        try {
            volumen = Integer.parseInt(p.getProperty("volumen", "50"));
            if (volumen < 0 || volumen > 100) {
                throw new NumberFormatException();
            }
        } catch (NumberFormatException e) {
            System.out.println("Volumen inválido, uso 50");
            volumen = 50;
        }
        System.out.println("Volumen: " + volumen);

        p.setProperty("dificultad", "dificil");
        p.setProperty("volumen", String.valueOf(volumen));
        try (BufferedWriter w = Files.newBufferedWriter(ruta)) {
            p.store(w, "configuración del Arcade Imperial");
        }
        Properties otra = leer(ruta);
        System.out.println("Guardado: dificultad=" + otra.getProperty("dificultad") + ", volumen=" + otra.getProperty("volumen"));
    }

    static Properties leer(Path ruta) throws IOException {
        Properties p = new Properties();
        try (BufferedReader r = Files.newBufferedReader(ruta)) {
            p.load(r);
        }
        return p;
    }
}
```

### Encargo R04-N01-E1 · La lista de precios del proveedor

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un almacén recibe de su proveedor `precios.csv` con `codigo;producto;precio` (el
precio con punto decimal). Leelo validando, aplicá un aumento del 12 % a todos los
precios y escribí `precios_nuevos.csv` con el mismo formato y dos decimales. Mostrá
cuántos productos se actualizaron, cuántas líneas se descartaron y el producto más caro
después del aumento.

`precios.csv`

```
codigo;producto;precio
A1;Yerba 1 kg;4200.50
A2;Azúcar 1 kg;1350
A3;Aceite 900 ml;
A4;Harina 1 kg;980.00
A5;Fideos;precio
```

#### Criterio de aprobación

- Valida cada línea (campos y número).
- Escribe con dos decimales y punto, en cualquier compu.

#### Salida esperada

```
Actualizados: 3, descartados: 2
El más caro: Yerba 1 kg (4704.56)
[codigo;producto;precio, A1;Yerba 1 kg;4704.56, A2;Azúcar 1 kg;1512.00, A4;Harina 1 kg;1097.60]
```

#### Solución de referencia

`precios.csv`

```
codigo;producto;precio
A1;Yerba 1 kg;4200.50
A2;Azúcar 1 kg;1350
A3;Aceite 900 ml;
A4;Harina 1 kg;980.00
A5;Fideos;precio
```

```java
// Encargo - La lista de precios del proveedor: leer, transformar y escribir un CSV.
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;

public class Precios {
    public static void main(String[] args) throws IOException {
        Locale.setDefault(Locale.US);
        int actualizados = 0;
        int descartados = 0;
        String masCaro = "";
        double precioMasCaro = -1;
        try (BufferedReader r = Files.newBufferedReader(Path.of("precios.csv"));
             BufferedWriter w = Files.newBufferedWriter(Path.of("precios_nuevos.csv"))) {
            w.write(r.readLine());
            w.newLine();
            String linea;
            while ((linea = r.readLine()) != null) {
                String[] c = linea.split(";");
                try {
                    double nuevo = Double.parseDouble(c[2]) * 1.12;
                    w.write(String.format("%s;%s;%.2f", c[0], c[1], nuevo));
                    w.newLine();
                    actualizados++;
                    if (nuevo > precioMasCaro) {
                        precioMasCaro = nuevo;
                        masCaro = c[1];
                    }
                } catch (NumberFormatException | ArrayIndexOutOfBoundsException e) {
                    descartados++;
                }
            }
        }
        System.out.println("Actualizados: " + actualizados + ", descartados: " + descartados);
        System.out.printf("El más caro: %s (%.2f)%n", masCaro, precioMasCaro);
        System.out.println(Files.readAllLines(Path.of("precios_nuevos.csv")));
    }
}
```

### Prueba del sello

#### ¿Desde dónde se busca una ruta relativa como `datos/x.txt`?

Desde la carpeta donde se ejecuta el programa.

#### ¿Qué devuelve `readLine()` cuando se termina el archivo?

`null`.

#### ¿Por qué se abre un archivo con `try` con recursos?

Para que se cierre siempre, aunque haya un error en el medio.

#### ¿Qué pasa si hacés `Files.writeString` sobre un archivo que ya existe?

Reemplaza todo su contenido, salvo que uses `StandardOpenOption.APPEND`.

#### ¿Para qué sirve un archivo `.properties`?

Para guardar configuración en pares `clave=valor` fuera del código, como los datos de conexión a una base.

### Soluciones (docente)

Nodo nuevo (el 29 del índice de `18-Java` estaba por crear; en el original estaba adentro del de JDBC), unidad 5. Corrige lo que marcó la auditoría: el ejemplo usa un `try` con recursos de verdad y una línea mal formada no corta el programa. Los archivos de datos de cada práctica se muestran en la consigna para que el alumno los cree.

## R04-N02 · SQL: tablas, restricciones y ABM

```meta
tipo: tema
padre: R04-N01
precio: 10
criatura: skeleton
temas: sql.modelo, sql.abm
```

### Crónica

En el segundo piso de la Bóveda, los registros ya no están en libros sueltos: están en **tablas** talladas en la pared, con columnas que no aceptan cualquier cosa. En la columna "vida" no entra una palabra; en la columna "héroe" de las partidas no entra un héroe que no exista.

—Un archivo acepta lo que le escribas —dice {mentor}—. Una **base de datos** tiene reglas, y las hace cumplir aunque el programa se equivoque. Esta es la lengua de la Bóveda, {heroe}: se llama **SQL**.

### Objetivos

- Instalar PostgreSQL y crear una base de datos para el curso.
- Crear tablas con tipos de datos adecuados.
- Declarar restricciones: clave primaria, clave foránea, `NOT NULL`, `UNIQUE`, `CHECK` y `DEFAULT`.
- Hacer el ABM (altas, bajas y modificaciones) con `INSERT`, `UPDATE` y `DELETE`.
- Escribir scripts que se puedan volver a correr.

### Antes de empezar

- Archivos de texto, CSV y .properties.

### Explicación

#### Qué es una base de datos relacional
Una base de datos **relacional** guarda los datos en **tablas**: cada tabla tiene
**columnas** (con un tipo) y **filas** (los registros). Las tablas se relacionan entre
sí por medio de claves. El programa que la maneja (el **motor**) hace cumplir las
reglas y permite consultar los datos con **SQL**. En este curso usamos **PostgreSQL**,
libre y muy usado en empresas.

#### Instalar y preparar la base del curso
En Linux:
```bash
sudo apt install postgresql
sudo -u postgres psql -c "CREATE ROLE imperio LOGIN PASSWORD 'imperio';"
sudo -u postgres psql -c "CREATE DATABASE imperio OWNER imperio;"
```
En Windows y macOS, el instalador de PostgreSQL trae **pgAdmin** (una herramienta
gráfica) y la consola `psql`; creá el usuario y la base desde ahí con los mismos
comandos.

Para ejecutar un archivo `.sql` y ver los resultados:
```bash
psql -X -q -h localhost -U imperio -d imperio -f tablas.sql
```
(pide la clave `imperio`). `-q` oculta los mensajes de "tabla creada". Si tu `psql` está
en castellano, al pie de cada resultado vas a ver `(2 filas)` en lugar de `(2 rows)`.
Los avisos `NOTICE` que aparecen al borrar algo que no existía no son errores.

#### Crear una tabla
```sql
CREATE TABLE heroe (
    id       SERIAL PRIMARY KEY,                    -- número que se genera solo
    nombre   VARCHAR(40) NOT NULL UNIQUE,           -- obligatorio y sin repetir
    clase    VARCHAR(20) NOT NULL,
    vida     INTEGER NOT NULL DEFAULT 30 CHECK (vida >= 0),
    oro      NUMERIC(10, 2) NOT NULL DEFAULT 0,
    alta     DATE NOT NULL DEFAULT CURRENT_DATE
);
```
| Tipo | Guarda |
|---|---|
| `INTEGER`, `BIGINT` | enteros |
| `SERIAL` | entero que se autoincrementa (ideal para `id`) |
| `NUMERIC(p, d)` | decimales **exactos** (dinero): `p` dígitos, `d` decimales |
| `VARCHAR(n)`, `TEXT` | textos (con o sin largo máximo) |
| `BOOLEAN` | verdadero o falso |
| `DATE`, `TIMESTAMP` | fecha / fecha y hora |

#### Las restricciones
| Restricción | Hace cumplir |
|---|---|
| `PRIMARY KEY` | identifica cada fila: única y no nula |
| `NOT NULL` | que la columna tenga valor |
| `UNIQUE` | que no haya dos filas con el mismo valor |
| `CHECK (condición)` | una regla sobre el valor |
| `DEFAULT valor` | el valor si no se especifica |
| `REFERENCES tabla(columna)` | **clave foránea**: el valor tiene que existir en la otra tabla |

#### Relacionar tablas: la clave foránea
```sql
CREATE TABLE partida (
    id        SERIAL PRIMARY KEY,
    heroe_id  INTEGER NOT NULL REFERENCES heroe(id) ON DELETE CASCADE,
    enemigo   VARCHAR(30) NOT NULL,
    danio     INTEGER NOT NULL CHECK (danio > 0)
);
```
`heroe_id` tiene que ser el `id` de un héroe que existe: la base rechaza partidas de
héroes inventados. `ON DELETE CASCADE` dice que, si se borra un héroe, se borran sus
partidas (sin eso, la base no deja borrar un héroe que tiene partidas).

#### ABM: altas, bajas y modificaciones
```sql
INSERT INTO heroe (nombre, clase, vida) VALUES ('Kira', 'arquera', 30);
INSERT INTO heroe (nombre, clase) VALUES ('Bron', 'guerrero'), ('Lía', 'maga');   -- varias; vida por defecto

UPDATE heroe SET vida = vida - 5 WHERE nombre = 'Kira';      -- modificar
DELETE FROM heroe WHERE nombre = 'Lía';                       -- borrar

SELECT * FROM heroe;                                          -- ver todo (lo ampliamos en el nodo que viene)
```
**Siempre con `WHERE`** en `UPDATE` y `DELETE`: sin él, se modifican o se borran
**todas** las filas.

#### Scripts que se pueden volver a correr
Un script que empieza creando tablas falla la segunda vez ("la tabla ya existe"). Se
empieza borrando lo que había, en orden inverso a las dependencias:
```sql
DROP TABLE IF EXISTS partida;       -- primero la que depende
DROP TABLE IF EXISTS heroe;
CREATE TABLE heroe ( … );
CREATE TABLE partida ( … );
```
(o `DROP TABLE IF EXISTS heroe CASCADE;`, que borra también lo que depende de ella).
Así el script deja la base siempre en el mismo estado.

> **Si usaste una planilla de cálculo.** Una tabla se parece a una hoja, pero cada
> columna tiene un tipo fijo y reglas, y las hojas se conectan por claves en lugar de
> copiar datos de una a otra.

### Código de ejemplo

```sql
-- Segundo piso de la Bóveda: tablas, restricciones y ABM.
-- Se puede correr muchas veces: siempre deja la base igual.
DROP TABLE IF EXISTS partida;
DROP TABLE IF EXISTS heroe;

CREATE TABLE heroe (
    id      SERIAL PRIMARY KEY,
    nombre  VARCHAR(40) NOT NULL UNIQUE,
    clase   VARCHAR(20) NOT NULL,
    vida    INTEGER NOT NULL DEFAULT 30 CHECK (vida >= 0),
    oro     NUMERIC(10, 2) NOT NULL DEFAULT 0
);

CREATE TABLE partida (
    id        SERIAL PRIMARY KEY,
    heroe_id  INTEGER NOT NULL REFERENCES heroe(id) ON DELETE CASCADE,
    enemigo   VARCHAR(30) NOT NULL,
    danio     INTEGER NOT NULL CHECK (danio > 0)
);

-- Altas
INSERT INTO heroe (nombre, clase, vida, oro) VALUES ('Kira', 'arquera', 30, 120.50);
INSERT INTO heroe (nombre, clase) VALUES ('Bron', 'guerrero'), ('Lía', 'maga');
INSERT INTO partida (heroe_id, enemigo, danio) VALUES (1, 'goblin', 12), (1, 'orco', 18), (2, 'orco', 30), (3, 'slime', 4);

SELECT * FROM heroe ORDER BY id;

-- Modificaciones (siempre con WHERE)
UPDATE heroe SET vida = vida - 5, oro = oro + 30 WHERE nombre = 'Kira';
UPDATE heroe SET clase = 'hechicera' WHERE id = 3;

-- Baja: con ON DELETE CASCADE se van también sus partidas
DELETE FROM heroe WHERE nombre = 'Bron';

SELECT * FROM heroe ORDER BY id;
SELECT * FROM partida ORDER BY id;
```

### Salida esperada

```
 id | nombre |  clase   | vida |  oro   
----+--------+----------+------+--------
  1 | Kira   | arquera  |   30 | 120.50
  2 | Bron   | guerrero |   30 |   0.00
  3 | Lía    | maga     |   30 |   0.00
(3 rows)

 id | nombre |   clase   | vida |  oro   
----+--------+-----------+------+--------
  1 | Kira   | arquera   |   25 | 150.50
  3 | Lía    | hechicera |   30 |   0.00
(2 rows)

 id | heroe_id | enemigo | danio 
----+----------+---------+-------
  1 |        1 | goblin  |    12
  2 |        1 | orco    |    18
  4 |        3 | slime   |     4
(3 rows)
```

### ¿Para qué sirve?

Casi todo sistema de gestión guarda sus datos en una base de datos relacional: clientes, productos, ventas, turnos, notas. Las restricciones son la última línea de defensa: aunque un programa tenga un error, la base no acepta un precio negativo, un email repetido o una venta de un cliente que no existe. SQL es uno de los conocimientos más pedidos en cualquier trabajo de sistemas.

### Errores habituales

**Esqueleto: la tabla que ya existe.** `ERROR: relation "heroe" already exists`. Empezá
el script con `DROP TABLE IF EXISTS`.

**Goblin: violar una restricción.**
```
ERROR:  new row for relation "heroe" violates check constraint "heroe_vida_check"
ERROR:  duplicate key value violates unique constraint "heroe_nombre_key"
ERROR:  insert or update on table "partida" violates foreign key constraint "partida_heroe_id_fkey"
```
El mensaje dice qué regla se violó: revisá el dato.

**Dragón: `UPDATE` o `DELETE` sin `WHERE`.** Modifica o borra **todas** las filas. Antes
de un `DELETE`, probá el mismo `WHERE` con un `SELECT`.

**Slime: las comillas.** En SQL los textos van entre comillas **simples** (`'Kira'`).
Las dobles son para nombres de columnas o tablas.

**Ogro: el orden de los `DROP`.** Borrar primero la tabla de la que otra depende falla:
`cannot drop table heroe because other objects depend on it`. Borrá primero la que
depende (o usá `CASCADE`).

### Misión R04-N02-M1 · Las tablas de la herrería

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí un script que se pueda correr muchas veces y cree dos tablas para la herrería:

- `arma`: id autoincremental, nombre (obligatorio, único, hasta 40 caracteres),
  tipo (obligatorio), filo (entero de 0 a 100, por defecto 50) y precio (decimal exacto,
  mayor que 0).
- `encargo`: id, el arma encargada (clave foránea; si se borra el arma, se borran sus
  encargos), el cliente (obligatorio) y la cantidad (mayor que 0).

Cargá tres armas y cuatro encargos, subí 10 el filo de todas las espadas, borrá un
arma que tenga encargos, y mostrá las dos tablas ordenadas por id.

#### Criterio de aprobación

- Empieza con `DROP TABLE IF EXISTS` en el orden correcto.
- Usa `SERIAL`, `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`, `NUMERIC` y `REFERENCES ... ON DELETE CASCADE`.
- `UPDATE` y `DELETE` tienen `WHERE`.

#### Salida esperada

```
 id |       nombre       |  tipo  | filo |  precio  
----+--------------------+--------+------+----------
  1 | Colmillo           | espada |   80 | 85000.00
  3 | Martillo del Norte | maza   |   50 | 61000.00
(2 rows)

 id | arma_id | cliente | cantidad 
----+---------+---------+----------
  1 |       1 | Bron    |        1
  3 |       3 | Nara    |        1
(2 rows)
```

#### Solución de referencia

```sql
-- Mision 1 - Las tablas de la herreria.
DROP TABLE IF EXISTS encargo;
DROP TABLE IF EXISTS arma;

CREATE TABLE arma (
    id      SERIAL PRIMARY KEY,
    nombre  VARCHAR(40) NOT NULL UNIQUE,
    tipo    VARCHAR(20) NOT NULL,
    filo    INTEGER NOT NULL DEFAULT 50 CHECK (filo BETWEEN 0 AND 100),
    precio  NUMERIC(10, 2) NOT NULL CHECK (precio > 0)
);

CREATE TABLE encargo (
    id        SERIAL PRIMARY KEY,
    arma_id   INTEGER NOT NULL REFERENCES arma(id) ON DELETE CASCADE,
    cliente   VARCHAR(40) NOT NULL,
    cantidad  INTEGER NOT NULL CHECK (cantidad > 0)
);

INSERT INTO arma (nombre, tipo, filo, precio) VALUES ('Colmillo', 'espada', 70, 85000);
INSERT INTO arma (nombre, tipo, precio) VALUES ('Brisa', 'espada', 42000.50), ('Martillo del Norte', 'maza', 61000);
INSERT INTO encargo (arma_id, cliente, cantidad) VALUES (1, 'Bron', 1), (2, 'Guardia real', 12), (3, 'Nara', 1), (2, 'Kira', 2);

UPDATE arma SET filo = filo + 10 WHERE tipo = 'espada';
DELETE FROM arma WHERE nombre = 'Brisa';

SELECT * FROM arma ORDER BY id;
SELECT * FROM encargo ORDER BY id;
```

### Misión R04-N02-M2 · Las reglas que protegen

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Creá una tabla `cuenta` (id, titular obligatorio, email único, saldo decimal que no
puede ser negativo, por defecto 0, y `activa` booleana por defecto verdadera). Cargá
dos cuentas válidas. Después escribí, **comentados** (con `--`), tres `INSERT` o
`UPDATE` que la base **rechazaría** (uno por cada restricción: email repetido, saldo
negativo, titular nulo), y al lado el nombre de la restricción que lo impide (probalos
de a uno en tu compu para ver el mensaje). Terminá con un `UPDATE` válido que acredite
un interés del 3 % a las cuentas activas y mostrá la tabla.

#### Criterio de aprobación

- La tabla tiene las restricciones pedidas.
- Los tres casos rechazados están comentados con el motivo.
- El `UPDATE` final usa `WHERE activa`.

#### Salida esperada

```
 id | titular |      email       |  saldo  | activa 
----+---------+------------------+---------+--------
  1 | Kira    | kira@imperio.com | 1030.00 | t
  2 | Bron    | bron@imperio.com | 5000.00 | f
(2 rows)
```

#### Solución de referencia

```sql
-- Mision 2 - Las reglas que protegen.
DROP TABLE IF EXISTS cuenta;

CREATE TABLE cuenta (
    id       SERIAL PRIMARY KEY,
    titular  VARCHAR(40) NOT NULL,
    email    VARCHAR(60) UNIQUE,
    saldo    NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (saldo >= 0),
    activa   BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO cuenta (titular, email, saldo) VALUES ('Kira', 'kira@imperio.com', 1000);
INSERT INTO cuenta (titular, email, saldo, activa) VALUES ('Bron', 'bron@imperio.com', 5000, FALSE);

-- Rechazados (probalos de a uno):
-- INSERT INTO cuenta (titular, email) VALUES ('Otra Kira', 'kira@imperio.com');   -- cuenta_email_key (UNIQUE)
-- UPDATE cuenta SET saldo = -10 WHERE titular = 'Kira';                            -- cuenta_saldo_check (CHECK)
-- INSERT INTO cuenta (email) VALUES ('nadie@imperio.com');                         -- NOT NULL de titular

UPDATE cuenta SET saldo = saldo * 1.03 WHERE activa;

SELECT * FROM cuenta ORDER BY id;
```

### Misión R04-N02-M3 · El registro de la biblioteca

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Diseñá las tablas de la biblioteca de la Academia: `socio` (id, nombre, DNI único de
7 u 8 dígitos con un `CHECK` que use `~ '^[0-9]{7,8}$'`), `libro` (id, título, autor,
año entre 1450 y 2100) y `prestamo` (id, socio y libro como claves foráneas, fecha de
préstamo por defecto `CURRENT_DATE` y fecha de devolución que puede ser nula). Si se
borra un libro, **no** se tienen que perder sus préstamos: la base tiene que impedir
borrarlo (clave foránea sin `CASCADE`). Cargá datos, marcá un préstamo como devuelto y
mostrá los préstamos **sin mostrar la fecha** (que cambia cada día).

#### Criterio de aprobación

- Tres tablas con claves foráneas.
- El `CHECK` del DNI usa una expresión regular.
- La consulta final no depende de la fecha del día.

#### Salida esperada

```
 id | socio_id | libro_id | devuelto 
----+----------+----------+----------
  1 |        1 |        1 | f
  2 |        2 |        2 | t
  3 |        1 |        2 | f
(3 rows)
```

#### Solución de referencia

```sql
-- Mision 3 - El registro de la biblioteca.
DROP TABLE IF EXISTS prestamo;
DROP TABLE IF EXISTS libro;
DROP TABLE IF EXISTS socio;

CREATE TABLE socio (
    id      SERIAL PRIMARY KEY,
    nombre  VARCHAR(40) NOT NULL,
    dni     VARCHAR(8) NOT NULL UNIQUE CHECK (dni ~ '^[0-9]{7,8}$')
);

CREATE TABLE libro (
    id      SERIAL PRIMARY KEY,
    titulo  VARCHAR(80) NOT NULL,
    autor   VARCHAR(40) NOT NULL,
    anio    INTEGER NOT NULL CHECK (anio BETWEEN 1450 AND 2100)
);

CREATE TABLE prestamo (
    id          SERIAL PRIMARY KEY,
    socio_id    INTEGER NOT NULL REFERENCES socio(id),
    libro_id    INTEGER NOT NULL REFERENCES libro(id),
    prestado    DATE NOT NULL DEFAULT CURRENT_DATE,
    devuelto    DATE
);

INSERT INTO socio (nombre, dni) VALUES ('Kira', '40111222'), ('Bron', '1234567');
INSERT INTO libro (titulo, autor, anio) VALUES ('Rayuela', 'Cortázar', 1963), ('Ficciones', 'Borges', 1944);
INSERT INTO prestamo (socio_id, libro_id) VALUES (1, 1), (2, 2), (1, 2);

UPDATE prestamo SET devuelto = prestado WHERE id = 2;

-- DELETE FROM libro WHERE id = 1;   -- la base lo impide: el libro tiene préstamos

SELECT id, socio_id, libro_id, devuelto IS NOT NULL AS devuelto FROM prestamo ORDER BY id;
```

### Encargo R04-N02-E1 · La base del kiosco

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un kiosco quiere dejar de anotar en un cuaderno. Diseñá las tablas `producto` (código
de texto como clave primaria, descripción, precio decimal mayor que 0, stock entero no
negativo) y `venta` (id, producto, cantidad mayor que 0, precio unitario al momento de
la venta). Cargá cinco productos y tres ventas; descontá del stock lo vendido con
`UPDATE`, aumentá un 8 % los precios de los productos con stock menor a 10 y borrá los
productos sin stock que **no** tengan ventas. Mostrá la tabla de productos.

#### Criterio de aprobación

- Clave primaria de texto y clave foránea a ella.
- Cada `UPDATE` y `DELETE` tiene su `WHERE`.

#### Salida esperada

```
 codigo | descripcion | precio  | stock 
--------+-------------+---------+-------
 AGU    | Agua 500 ml | 1188.00 |     8
 ALF    | Alfajor     |  900.00 |    37
 CHI    | Chicles     |  486.00 |     6
(3 rows)
```

#### Solución de referencia

```sql
-- Encargo - La base del kiosco.
DROP TABLE IF EXISTS venta;
DROP TABLE IF EXISTS producto;

CREATE TABLE producto (
    codigo       VARCHAR(10) PRIMARY KEY,
    descripcion  VARCHAR(40) NOT NULL,
    precio       NUMERIC(10, 2) NOT NULL CHECK (precio > 0),
    stock        INTEGER NOT NULL CHECK (stock >= 0)
);

CREATE TABLE venta (
    id        SERIAL PRIMARY KEY,
    codigo    VARCHAR(10) NOT NULL REFERENCES producto(codigo),
    cantidad  INTEGER NOT NULL CHECK (cantidad > 0),
    precio    NUMERIC(10, 2) NOT NULL
);

INSERT INTO producto VALUES
    ('ALF', 'Alfajor', 900, 40),
    ('AGU', 'Agua 500 ml', 1100, 12),
    ('CHI', 'Chicles', 450, 8),
    ('GAL', 'Galletitas', 1500, 0),
    ('CAR', 'Caramelos', 50, 0);

INSERT INTO venta (codigo, cantidad, precio) VALUES ('ALF', 3, 900), ('AGU', 4, 1100), ('CHI', 2, 450);

UPDATE producto SET stock = stock - 3 WHERE codigo = 'ALF';
UPDATE producto SET stock = stock - 4 WHERE codigo = 'AGU';
UPDATE producto SET stock = stock - 2 WHERE codigo = 'CHI';

UPDATE producto SET precio = precio * 1.08 WHERE stock < 10;

DELETE FROM producto p WHERE p.stock = 0 AND NOT EXISTS (SELECT 1 FROM venta v WHERE v.codigo = p.codigo);

SELECT * FROM producto ORDER BY codigo;
```

### Prueba del sello

#### ¿Qué garantiza una `PRIMARY KEY`?

Que cada fila tenga un valor único y no nulo en esa columna: la identifica.

#### ¿Qué hace una clave foránea?

Exige que el valor exista en la columna referenciada de otra tabla.

#### ¿Qué pasa si hacés `DELETE FROM heroe;` sin `WHERE`?

Se borran todas las filas de la tabla.

#### ¿Por qué el dinero se guarda en `NUMERIC` y no en un tipo de punto flotante?

Porque `NUMERIC` es exacto; los tipos de punto flotante tienen errores de redondeo.

#### ¿Cómo se hace un script que se pueda correr muchas veces?

Empezando con `DROP TABLE IF EXISTS` (en orden inverso a las dependencias o con `CASCADE`) antes de crear las tablas.

### Soluciones (docente)

Sale de `18-Java/26-SQL-Diseno-Consultas` (unidad 3), la parte de diseño y ABM. Corrige los dos problemas del original: el script ahora se puede volver a correr (`DROP` en orden) y las salidas son siempre las mismas. Las salidas esperadas se generaron con `psql -X -q` en inglés (`(2 rows)`); con `psql` en castellano dice `(2 filas)`.

## R04-N03 · SQL: consultas, JOIN y vistas

```meta
tipo: tema
padre: R04-N02
precio: 10
criatura: ogre
temas: sql.consultas, sql.joins
```

### Crónica

En el tercer piso de la Bóveda trabaja la **Oráculo de las Tablas**: le hacés una pregunta —*¿qué héroes nunca pelearon contra un orco?*— y ella cruza tablas, filtra, cuenta y te devuelve la respuesta en una tabla nueva. No toca un solo dato: solo **consulta**.

—Guardar datos es fácil —dice {mentor}—. El poder está en **preguntarles**. Aprendé a cruzar tablas como la Oráculo, {heroe}, y ninguna pregunta del Imperio va a quedar sin respuesta.

### Objetivos

- Consultar con `SELECT`, `WHERE`, `ORDER BY` y `LIMIT`.
- Filtrar con `LIKE`, `IN`, `BETWEEN` e `IS NULL`.
- Resumir con funciones de agregación, `GROUP BY` y `HAVING`.
- Cruzar tablas con los cinco `JOIN`: `INNER`, `LEFT`, `RIGHT`, `FULL` y `CROSS`.
- Usar subconsultas, `EXISTS`, `UNION` y vistas.

### Antes de empezar

- SQL: tablas, restricciones y ABM.

### Explicación

#### `SELECT`: elegir columnas y filas
```sql
SELECT nombre, vida FROM heroe;                          -- algunas columnas
SELECT nombre, vida * 2 AS doble FROM heroe;             -- calcular y renombrar (AS)
SELECT * FROM heroe WHERE vida < 30 AND clase = 'mago';  -- filtrar
SELECT DISTINCT clase FROM heroe;                        -- sin repetidos
SELECT * FROM heroe ORDER BY vida DESC, nombre;          -- ordenar (DESC: de mayor a menor)
SELECT * FROM heroe ORDER BY vida DESC LIMIT 3;          -- los tres primeros
```
Sin `ORDER BY`, el orden de las filas **no está garantizado**.

#### Filtros útiles
```sql
WHERE nombre LIKE 'K%'             -- empieza con K (% es "cualquier texto", _ es "un carácter")
WHERE nombre ILIKE '%ra%'          -- contiene "ra", sin importar mayúsculas (PostgreSQL)
WHERE clase IN ('mago', 'clérigo') -- alguno de esos valores
WHERE vida BETWEEN 20 AND 40       -- entre, incluidos los extremos
WHERE clan IS NULL                 -- sin valor (con = NULL no funciona)
```

#### Agregar: contar, sumar, promediar
```sql
SELECT COUNT(*), SUM(danio), AVG(danio), MIN(danio), MAX(danio) FROM partida;
```
Con **`GROUP BY`** se calcula por grupo, y con **`HAVING`** se filtran los grupos:
```sql
SELECT enemigo, COUNT(*) AS veces, SUM(danio) AS total
FROM partida
GROUP BY enemigo
HAVING COUNT(*) >= 2          -- solo los enemigos con 2 o más partidas
ORDER BY total DESC;
```
`WHERE` filtra **filas** antes de agrupar; `HAVING` filtra **grupos** después. Las
columnas del `SELECT` tienen que estar en el `GROUP BY` o dentro de una función de
agregación.

#### Cruzar tablas: `JOIN`
Supongamos estos datos (los del código de ejemplo):
- héroes: Kira, Bron, Lía, **Olmo (sin partidas)**;
- partidas de Kira, Bron y Lía, y **una partida de un héroe que ya no está en la
  tabla** (su `heroe_id` es 9 y no tiene clave foránea, para poder mostrarlo).

| JOIN | Devuelve | En el ejemplo |
|---|---|---|
| `INNER JOIN` | solo las filas que coinciden en las dos tablas | las partidas de Kira, Bron y Lía |
| `LEFT JOIN` | todas las de la **izquierda**, y de la derecha lo que coincida (o `NULL`) | …y además Olmo, con la partida en `NULL` |
| `RIGHT JOIN` | todas las de la **derecha**, y de la izquierda lo que coincida | …y además la partida del héroe 9, con el nombre en `NULL` |
| `FULL JOIN` | todas las de las dos | Olmo y la partida huérfana |
| `CROSS JOIN` | todas las combinaciones (producto cartesiano) | cada héroe con cada enemigo |

```sql
SELECT h.nombre, p.enemigo
FROM heroe h
LEFT JOIN partida p ON p.heroe_id = h.id;     -- h y p son alias
```
El `LEFT JOIN` con `WHERE p.id IS NULL` responde las preguntas del tipo *"¿quiénes
nunca…?"*.

#### Subconsultas y `EXISTS`
Una consulta dentro de otra:
```sql
SELECT nombre FROM heroe WHERE vida > (SELECT AVG(vida) FROM heroe);
SELECT nombre FROM heroe h
WHERE NOT EXISTS (SELECT 1 FROM partida p WHERE p.heroe_id = h.id AND p.enemigo = 'orco');
```

#### `UNION`: juntar resultados
```sql
SELECT nombre FROM heroe
UNION                               -- sin repetidos (UNION ALL los deja)
SELECT nombre FROM enemigo_famoso;
```
Las dos consultas tienen que tener la misma cantidad de columnas, de tipos compatibles.

#### Vistas: consultas con nombre
Una **vista** guarda una consulta con un nombre, y se usa como si fuera una tabla:
```sql
CREATE VIEW ranking AS
SELECT h.nombre, COALESCE(SUM(p.danio), 0) AS danio_total
FROM heroe h LEFT JOIN partida p ON p.heroe_id = h.id
GROUP BY h.nombre;

SELECT * FROM ranking ORDER BY danio_total DESC;
```
`COALESCE(x, 0)` devuelve 0 si `x` es `NULL` (útil con los `LEFT JOIN`). Recordá
borrar las vistas al principio del script (`DROP VIEW IF EXISTS`), antes que las
tablas que usan.

### Código de ejemplo

```sql
-- Tercer piso: la Oráculo de las Tablas. Datos armados para que cada JOIN muestre su diferencia.
DROP VIEW IF EXISTS ranking;
DROP TABLE IF EXISTS partida;
DROP TABLE IF EXISTS heroe;

CREATE TABLE heroe (
    id     INTEGER PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,
    clase  VARCHAR(20) NOT NULL,
    vida   INTEGER NOT NULL,
    clan   VARCHAR(20)
);
CREATE TABLE partida (                -- sin clave foránea, para poder mostrar una partida "huérfana"
    id        INTEGER PRIMARY KEY,
    heroe_id  INTEGER NOT NULL,
    enemigo   VARCHAR(20) NOT NULL,
    danio     INTEGER NOT NULL
);

INSERT INTO heroe VALUES (1, 'Kira', 'arquera', 30, 'valle'), (2, 'Bron', 'guerrero', 45, 'forjas'),
                         (3, 'Lía', 'maga', 20, 'valle'), (4, 'Olmo', 'mago', 25, NULL);
INSERT INTO partida VALUES (1, 1, 'goblin', 12), (2, 1, 'orco', 18), (3, 2, 'orco', 30),
                           (4, 3, 'slime', 4), (5, 2, 'goblin', 9), (6, 9, 'dragón', 50);

-- Filtros y orden
SELECT nombre, vida FROM heroe WHERE clase LIKE 'mag%' OR clan IS NULL ORDER BY vida DESC;

-- Agregación por grupo
SELECT enemigo, COUNT(*) AS veces, SUM(danio) AS total
FROM partida GROUP BY enemigo HAVING COUNT(*) >= 2 ORDER BY total DESC;

-- Los cinco JOIN
SELECT h.nombre, p.enemigo FROM heroe h INNER JOIN partida p ON p.heroe_id = h.id ORDER BY p.id;
SELECT h.nombre, p.enemigo FROM heroe h LEFT JOIN partida p ON p.heroe_id = h.id ORDER BY h.id, p.id;
SELECT h.nombre, p.enemigo FROM heroe h RIGHT JOIN partida p ON p.heroe_id = h.id ORDER BY p.id;
SELECT h.nombre, p.enemigo FROM heroe h FULL JOIN partida p ON p.heroe_id = h.id ORDER BY h.id, p.id;
SELECT h.nombre, e.enemigo FROM heroe h CROSS JOIN (SELECT DISTINCT enemigo FROM partida WHERE enemigo IN ('goblin', 'orco')) e
WHERE h.clase = 'arquera' ORDER BY e.enemigo;

-- ¿Quiénes nunca pelearon? (LEFT JOIN + IS NULL)
SELECT h.nombre FROM heroe h LEFT JOIN partida p ON p.heroe_id = h.id WHERE p.id IS NULL;

-- Subconsulta y NOT EXISTS: héroes que nunca enfrentaron un orco
SELECT h.nombre FROM heroe h
WHERE NOT EXISTS (SELECT 1 FROM partida p WHERE p.heroe_id = h.id AND p.enemigo = 'orco') ORDER BY h.nombre;

-- UNION: todos los nombres de clanes y clases en una sola lista
SELECT clan AS nombre FROM heroe WHERE clan IS NOT NULL
UNION
SELECT clase FROM heroe
ORDER BY nombre;

-- Una vista
CREATE VIEW ranking AS
SELECT h.nombre, COALESCE(SUM(p.danio), 0) AS danio_total
FROM heroe h LEFT JOIN partida p ON p.heroe_id = h.id
GROUP BY h.nombre;

SELECT * FROM ranking ORDER BY danio_total DESC, nombre;
```

### Salida esperada

```
 nombre | vida 
--------+------
 Olmo   |   25
 Lía    |   20
(2 rows)

 enemigo | veces | total 
---------+-------+-------
 orco    |     2 |    48
 goblin  |     2 |    21
(2 rows)

 nombre | enemigo 
--------+---------
 Kira   | goblin
 Kira   | orco
 Bron   | orco
 Lía    | slime
 Bron   | goblin
(5 rows)

 nombre | enemigo 
--------+---------
 Kira   | goblin
 Kira   | orco
 Bron   | orco
 Bron   | goblin
 Lía    | slime
 Olmo   | 
(6 rows)

 nombre | enemigo 
--------+---------
 Kira   | goblin
 Kira   | orco
 Bron   | orco
 Lía    | slime
 Bron   | goblin
        | dragón
(6 rows)

 nombre | enemigo 
--------+---------
 Kira   | goblin
 Kira   | orco
 Bron   | orco
 Bron   | goblin
 Lía    | slime
 Olmo   | 
        | dragón
(7 rows)

 nombre | enemigo 
--------+---------
 Kira   | goblin
 Kira   | orco
(2 rows)

 nombre 
--------
 Olmo
(1 row)

 nombre 
--------
 Lía
 Olmo
(2 rows)

  nombre  
----------
 arquera
 forjas
 guerrero
 maga
 mago
 valle
(6 rows)

 nombre | danio_total 
--------+-------------
 Bron   |          39
 Kira   |          30
 Lía    |           4
 Olmo   |           0
(4 rows)
```

### ¿Para qué sirve?

Las consultas son lo que convierte los datos en información: el reporte de ventas del mes por vendedor, los clientes que no compran hace tres meses, los alumnos que adeudan cuotas, el ranking de productos. Todo sistema de gestión tiene decenas de consultas con `JOIN` y `GROUP BY`, y las vistas guardan las más usadas para que el programa las pida por nombre.

### Errores habituales

**Ogro: `= NULL`.** `WHERE clan = NULL` no devuelve nada nunca. Va `IS NULL`.

**Esqueleto: una columna que no está en el `GROUP BY`.** `ERROR: column "heroe.nombre"
must appear in the GROUP BY clause or be used in an aggregate function`.

**Ogro: el `INNER JOIN` que esconde filas.** Si querés ver también los héroes sin
partidas, hace falta `LEFT JOIN`: el `INNER` solo trae los que coinciden.

**Dragón: el `JOIN` sin `ON`.** Un `JOIN` sin condición (o con una equivocada) cruza
todo con todo: miles de filas repetidas.

**Ogro: `WHERE` con un agregado.** `WHERE COUNT(*) > 2` no se permite: los grupos se
filtran con `HAVING`.

### Misión R04-N03-M1 · El informe del torneo

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con estas tablas (copialas al principio de tu script), respondé con una consulta cada
pregunta:

1. Los luchadores de clase `guerrero` o `paladín` con más de 40 de fuerza, ordenados por fuerza de mayor a menor.
2. Cuántas peleas ganó cada luchador (los que ganaron al menos una), de más a menos.
3. El promedio de duración de las peleas por arena, redondeado a un decimal (`ROUND(AVG(x), 1)`), solo de las arenas con más de una pelea.
4. Todas las peleas con el nombre del ganador y del perdedor (dos `JOIN` a la misma tabla, con alias distintos).

```sql
DROP TABLE IF EXISTS pelea;
DROP TABLE IF EXISTS luchador;
CREATE TABLE luchador (id INTEGER PRIMARY KEY, nombre VARCHAR(20), clase VARCHAR(20), fuerza INTEGER);
CREATE TABLE pelea (id INTEGER PRIMARY KEY, ganador_id INTEGER REFERENCES luchador(id),
                    perdedor_id INTEGER REFERENCES luchador(id), arena VARCHAR(20), minutos INTEGER);
INSERT INTO luchador VALUES (1, 'Bron', 'guerrero', 52), (2, 'Nara', 'paladín', 47), (3, 'Pip', 'guerrero', 35),
                            (4, 'Lía', 'maga', 20), (5, 'Olmo', 'paladín', 38);
INSERT INTO pelea VALUES (1, 1, 3, 'norte', 12), (2, 2, 4, 'sur', 7), (3, 1, 2, 'norte', 20),
                         (4, 5, 3, 'sur', 9), (5, 1, 5, 'este', 15), (6, 2, 3, 'norte', 11);
```

#### Criterio de aprobación

- Cada pregunta tiene su consulta y todas tienen `ORDER BY`.
- Usa `IN`, `GROUP BY`, `HAVING`, `ROUND` y dos `JOIN` con alias.

#### Salida esperada

```
 nombre |  clase   | fuerza 
--------+----------+--------
 Bron   | guerrero |     52
 Nara   | paladín  |     47
(2 rows)

 nombre | victorias 
--------+-----------
 Bron   |         3
 Nara   |         2
 Olmo   |         1
(3 rows)

 arena | promedio 
-------+----------
 norte |     14.3
 sur   |      8.0
(2 rows)

 id | ganador | perdedor | arena 
----+---------+----------+-------
  1 | Bron    | Pip      | norte
  2 | Nara    | Lía      | sur
  3 | Bron    | Nara     | norte
  4 | Olmo    | Pip      | sur
  5 | Bron    | Olmo     | este
  6 | Nara    | Pip      | norte
(6 rows)
```

#### Solución de referencia

```sql
-- Mision 1 - El informe del torneo.
DROP TABLE IF EXISTS pelea;
DROP TABLE IF EXISTS luchador;
CREATE TABLE luchador (id INTEGER PRIMARY KEY, nombre VARCHAR(20), clase VARCHAR(20), fuerza INTEGER);
CREATE TABLE pelea (id INTEGER PRIMARY KEY, ganador_id INTEGER REFERENCES luchador(id),
                    perdedor_id INTEGER REFERENCES luchador(id), arena VARCHAR(20), minutos INTEGER);
INSERT INTO luchador VALUES (1, 'Bron', 'guerrero', 52), (2, 'Nara', 'paladín', 47), (3, 'Pip', 'guerrero', 35),
                            (4, 'Lía', 'maga', 20), (5, 'Olmo', 'paladín', 38);
INSERT INTO pelea VALUES (1, 1, 3, 'norte', 12), (2, 2, 4, 'sur', 7), (3, 1, 2, 'norte', 20),
                         (4, 5, 3, 'sur', 9), (5, 1, 5, 'este', 15), (6, 2, 3, 'norte', 11);

-- 1
SELECT nombre, clase, fuerza FROM luchador
WHERE clase IN ('guerrero', 'paladín') AND fuerza > 40 ORDER BY fuerza DESC;

-- 2
SELECT l.nombre, COUNT(*) AS victorias
FROM pelea p JOIN luchador l ON l.id = p.ganador_id
GROUP BY l.nombre ORDER BY victorias DESC, l.nombre;

-- 3
SELECT arena, ROUND(AVG(minutos), 1) AS promedio
FROM pelea GROUP BY arena HAVING COUNT(*) > 1 ORDER BY arena;

-- 4
SELECT p.id, g.nombre AS ganador, d.nombre AS perdedor, p.arena
FROM pelea p
JOIN luchador g ON g.id = p.ganador_id
JOIN luchador d ON d.id = p.perdedor_id
ORDER BY p.id;
```

### Misión R04-N03-M2 · Los que nunca…

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con las mismas tablas de la misión anterior, escribí las consultas para:

1. Los luchadores que **nunca ganaron** (con `LEFT JOIN` e `IS NULL`).
2. Los luchadores que **nunca perdieron** (con `NOT EXISTS`).
3. Los luchadores con fuerza **mayor al promedio** (con una subconsulta).
4. Una lista única de **todos los nombres de arenas y de clases** (con `UNION`), ordenada.
5. Una vista `resumen` con cada luchador, sus victorias y sus derrotas (0 si no tiene), y consultala ordenada por victorias.

#### Criterio de aprobación

- Usa `LEFT JOIN … IS NULL`, `NOT EXISTS`, una subconsulta, `UNION` y una vista.
- El script borra la vista al principio.

#### Salida esperada

```
 nombre 
--------
 Lía
 Pip
(2 rows)

 nombre 
--------
 Bron
(1 row)

 nombre | fuerza 
--------+--------
 Bron   |     52
 Nara   |     47
(2 rows)

  nombre  
----------
 este
 guerrero
 maga
 norte
 paladín
 sur
(6 rows)

 nombre | victorias | derrotas 
--------+-----------+----------
 Bron   |         3 |        0
 Nara   |         2 |        1
 Olmo   |         1 |        1
 Lía    |         0 |        1
 Pip    |         0 |        3
(5 rows)
```

#### Solución de referencia

```sql
-- Mision 2 - Los que nunca...
DROP VIEW IF EXISTS resumen;
DROP TABLE IF EXISTS pelea;
DROP TABLE IF EXISTS luchador;
CREATE TABLE luchador (id INTEGER PRIMARY KEY, nombre VARCHAR(20), clase VARCHAR(20), fuerza INTEGER);
CREATE TABLE pelea (id INTEGER PRIMARY KEY, ganador_id INTEGER REFERENCES luchador(id),
                    perdedor_id INTEGER REFERENCES luchador(id), arena VARCHAR(20), minutos INTEGER);
INSERT INTO luchador VALUES (1, 'Bron', 'guerrero', 52), (2, 'Nara', 'paladín', 47), (3, 'Pip', 'guerrero', 35),
                            (4, 'Lía', 'maga', 20), (5, 'Olmo', 'paladín', 38);
INSERT INTO pelea VALUES (1, 1, 3, 'norte', 12), (2, 2, 4, 'sur', 7), (3, 1, 2, 'norte', 20),
                         (4, 5, 3, 'sur', 9), (5, 1, 5, 'este', 15), (6, 2, 3, 'norte', 11);

-- 1
SELECT l.nombre FROM luchador l LEFT JOIN pelea p ON p.ganador_id = l.id
WHERE p.id IS NULL ORDER BY l.nombre;

-- 2
SELECT l.nombre FROM luchador l
WHERE NOT EXISTS (SELECT 1 FROM pelea p WHERE p.perdedor_id = l.id) ORDER BY l.nombre;

-- 3
SELECT nombre, fuerza FROM luchador WHERE fuerza > (SELECT AVG(fuerza) FROM luchador) ORDER BY fuerza DESC;

-- 4
SELECT arena AS nombre FROM pelea
UNION
SELECT clase FROM luchador
ORDER BY nombre;

-- 5
CREATE VIEW resumen AS
SELECT l.nombre,
       (SELECT COUNT(*) FROM pelea p WHERE p.ganador_id = l.id) AS victorias,
       (SELECT COUNT(*) FROM pelea p WHERE p.perdedor_id = l.id) AS derrotas
FROM luchador l;

SELECT * FROM resumen ORDER BY victorias DESC, derrotas, nombre;
```

### Misión R04-N03-M3 · La diferencia entre los JOIN

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Armá tus propias tablas `curso` (id, nombre) e `inscripcion` (id, alumno, curso_id,
**sin** clave foránea) con datos elegidos para que se note la diferencia: un curso sin
inscriptos y una inscripción a un curso que no existe. Escribí los cuatro `JOIN`
(`INNER`, `LEFT`, `RIGHT` y `FULL`) mostrando curso y alumno, y agregá antes de cada uno
un comentario que diga **qué filas de más aparecen** respecto del `INNER`. Terminá con
la cantidad de inscriptos por curso, **incluidos los cursos con 0**.

#### Criterio de aprobación

- Los datos hacen que los cuatro `JOIN` den resultados distintos.
- Los comentarios explican la diferencia.
- El conteo incluye los cursos sin inscriptos (con `LEFT JOIN` y `COUNT` de una columna de la derecha).

#### Salida esperada

```
 nombre | alumno 
--------+--------
 Java   | Kira
 Java   | Bron
 SQL    | Lía
(3 rows)

 nombre | alumno 
--------+--------
 Java   | Kira
 Java   | Bron
 SQL    | Lía
 Swing  | 
(4 rows)

 nombre | alumno 
--------+--------
 Java   | Kira
 Java   | Bron
 SQL    | Lía
        | Pip
(4 rows)

 nombre | alumno 
--------+--------
 Java   | Kira
 Java   | Bron
 SQL    | Lía
 Swing  | 
        | Pip
(5 rows)

 nombre | inscriptos 
--------+------------
 Java   |          2
 SQL    |          1
 Swing  |          0
(3 rows)
```

#### Solución de referencia

```sql
-- Mision 3 - La diferencia entre los JOIN.
DROP TABLE IF EXISTS inscripcion;
DROP TABLE IF EXISTS curso;
CREATE TABLE curso (id INTEGER PRIMARY KEY, nombre VARCHAR(30));
CREATE TABLE inscripcion (id INTEGER PRIMARY KEY, alumno VARCHAR(20), curso_id INTEGER);
INSERT INTO curso VALUES (1, 'Java'), (2, 'SQL'), (3, 'Swing');
INSERT INTO inscripcion VALUES (1, 'Kira', 1), (2, 'Bron', 1), (3, 'Lía', 2), (4, 'Pip', 7);

-- INNER: solo las inscripciones con un curso que existe.
SELECT c.nombre, i.alumno FROM curso c INNER JOIN inscripcion i ON i.curso_id = c.id ORDER BY i.id;
-- LEFT: además, Swing (curso sin inscriptos) con alumno NULL.
SELECT c.nombre, i.alumno FROM curso c LEFT JOIN inscripcion i ON i.curso_id = c.id ORDER BY c.id, i.id;
-- RIGHT: además, Pip (inscripto a un curso que no existe) con curso NULL.
SELECT c.nombre, i.alumno FROM curso c RIGHT JOIN inscripcion i ON i.curso_id = c.id ORDER BY i.id;
-- FULL: las dos cosas, Swing y Pip.
SELECT c.nombre, i.alumno FROM curso c FULL JOIN inscripcion i ON i.curso_id = c.id ORDER BY c.id, i.id;

-- Inscriptos por curso, con los de 0 (COUNT de una columna cuenta solo los no nulos)
SELECT c.nombre, COUNT(i.id) AS inscriptos
FROM curso c LEFT JOIN inscripcion i ON i.curso_id = c.id
GROUP BY c.id, c.nombre ORDER BY c.id;
```

### Encargo R04-N03-E1 · Las consultas del almacén

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un almacén tiene `producto(codigo, nombre, rubro, precio)` y `venta(id, codigo,
cantidad, mes)`. Inventá datos para 6 productos de 3 rubros y 10 ventas en 3 meses
(que un producto no se haya vendido nunca). Escribí consultas para: la facturación por
mes (cantidad × precio), el rubro que más facturó, los productos que nunca se
vendieron, el producto más vendido en unidades y una vista `ranking_productos` con
nombre, unidades y facturación de cada producto (los que no se vendieron, con 0).

#### Criterio de aprobación

- Cada consulta responde una pregunta y está ordenada.
- La vista incluye los productos sin ventas.

#### Salida esperada

```
 mes | facturacion 
-----+-------------
   1 |    31950.00
   2 |    33000.00
   3 |    23800.00
(3 rows)

  rubro  | facturacion 
---------+-------------
 almacén |    47250.00
(1 row)

 nombre 
--------
 Soda
(1 row)

 nombre  | unidades 
---------+----------
 Gaseosa |       16
(1 row)

   nombre   | unidades | facturacion 
------------+----------+-------------
 Yerba      |        9 |    37800.00
 Gaseosa    |       16 |    33600.00
 Azúcar     |        7 |     9450.00
 Lavandina  |        7 |     6300.00
 Detergente |        1 |     1600.00
 Soda       |        0 |           0
(6 rows)
```

#### Solución de referencia

```sql
-- Encargo - Las consultas del almacen.
DROP VIEW IF EXISTS ranking_productos;
DROP TABLE IF EXISTS venta;
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (codigo VARCHAR(5) PRIMARY KEY, nombre VARCHAR(20), rubro VARCHAR(20), precio NUMERIC(10, 2));
CREATE TABLE venta (id INTEGER PRIMARY KEY, codigo VARCHAR(5) REFERENCES producto(codigo), cantidad INTEGER, mes INTEGER);
INSERT INTO producto VALUES ('P1', 'Yerba', 'almacén', 4200), ('P2', 'Azúcar', 'almacén', 1350), ('P3', 'Lavandina', 'limpieza', 900),
                            ('P4', 'Detergente', 'limpieza', 1600), ('P5', 'Gaseosa', 'bebidas', 2100), ('P6', 'Soda', 'bebidas', 800);
INSERT INTO venta VALUES (1, 'P1', 3, 1), (2, 'P2', 5, 1), (3, 'P5', 6, 1), (4, 'P1', 2, 2), (5, 'P3', 4, 2),
                         (6, 'P5', 10, 2), (7, 'P4', 1, 3), (8, 'P1', 4, 3), (9, 'P2', 2, 3), (10, 'P3', 3, 3);

-- Facturación por mes
SELECT v.mes, SUM(v.cantidad * p.precio) AS facturacion
FROM venta v JOIN producto p ON p.codigo = v.codigo GROUP BY v.mes ORDER BY v.mes;

-- El rubro que más facturó
SELECT p.rubro, SUM(v.cantidad * p.precio) AS facturacion
FROM venta v JOIN producto p ON p.codigo = v.codigo GROUP BY p.rubro ORDER BY facturacion DESC LIMIT 1;

-- Productos que nunca se vendieron
SELECT p.nombre FROM producto p WHERE NOT EXISTS (SELECT 1 FROM venta v WHERE v.codigo = p.codigo) ORDER BY p.nombre;

-- El más vendido en unidades
SELECT p.nombre, SUM(v.cantidad) AS unidades
FROM venta v JOIN producto p ON p.codigo = v.codigo GROUP BY p.nombre ORDER BY unidades DESC LIMIT 1;

-- Vista con todos los productos
CREATE VIEW ranking_productos AS
SELECT p.nombre, COALESCE(SUM(v.cantidad), 0) AS unidades, COALESCE(SUM(v.cantidad * p.precio), 0) AS facturacion
FROM producto p LEFT JOIN venta v ON v.codigo = p.codigo GROUP BY p.nombre;

SELECT * FROM ranking_productos ORDER BY facturacion DESC, nombre;
```

### Prueba del sello

#### ¿Qué diferencia hay entre `WHERE` y `HAVING`?

`WHERE` filtra filas antes de agrupar; `HAVING` filtra grupos después de agrupar.

#### ¿Qué devuelve un `LEFT JOIN` que no devuelve un `INNER JOIN`?

Las filas de la tabla izquierda que no tienen coincidencia en la derecha, con `NULL` en las columnas de la derecha.

#### ¿Cómo encontrás "los clientes que nunca compraron"?

Con `LEFT JOIN` a las compras y `WHERE compra.id IS NULL`, o con `NOT EXISTS`.

#### ¿Qué diferencia hay entre `UNION` y `UNION ALL`?

`UNION` elimina los repetidos; `UNION ALL` los deja.

#### ¿Qué es una vista?

Una consulta guardada con un nombre, que se usa como si fuera una tabla.

### Soluciones (docente)

Sale de `18-Java/26-SQL-Diseno-Consultas` y del 27 por crear (unidad 3). Corrige el problema principal de la auditoría: los datos del ejemplo incluyen un héroe sin partidas y una partida sin héroe, así que los cinco `JOIN` dan resultados distintos; y suma `UNION`, que pedía el programa. La tabla `partida` del ejemplo no tiene clave foránea a propósito, para poder mostrar la fila huérfana del `RIGHT JOIN`.

## R04-N04 · SQL: funciones, procedimientos, triggers y roles

```meta
tipo: tema
padre: R04-N03
precio: 10
criatura: troll
temas: sql.avanzado
```

### Crónica

En el cuarto piso de la Bóveda, las tablas ya no esperan órdenes: **reaccionan**. Cuando alguien anota una partida, un mecanismo oculto le resta la vida al héroe y deja constancia en un libro de auditoría. En la puerta, un guardián revisa quién entra: los escribas pueden leer, pero solo los tesoreros pueden modificar el oro.

—La base de datos no es solo un depósito —dice {mentor}—. Puede tener **lógica propia**: funciones, procedimientos que hacen varias cosas juntas, reglas que se disparan solas y permisos por persona. Todo eso vive en la Bóveda y se cumple aunque el programa se olvide, {heroe}.

### Objetivos

- Escribir funciones en PL/pgSQL que devuelven un valor.
- Escribir procedimientos que ejecutan varias operaciones y llamarlos con `CALL`.
- Crear triggers que reaccionan a `INSERT`, `UPDATE` o `DELETE`.
- Conocer los roles y los permisos con `GRANT` y `REVOKE`.

### Antes de empezar

- SQL: consultas, JOIN y vistas.

### Explicación

#### Funciones
Una **función** recibe parámetros y **devuelve un valor**; se usa dentro de una
consulta. En PostgreSQL se escriben en **PL/pgSQL**, el lenguaje procedural de la base:
```sql
CREATE OR REPLACE FUNCTION nivel_de(vida INTEGER) RETURNS VARCHAR AS $$
BEGIN
    IF vida >= 40 THEN
        RETURN 'fuerte';
    ELSIF vida >= 20 THEN
        RETURN 'normal';
    ELSE
        RETURN 'débil';
    END IF;
END;
$$ LANGUAGE plpgsql;

SELECT nombre, nivel_de(vida) FROM heroe;
```
El cuerpo va entre `$$`. `CREATE OR REPLACE` permite volver a correr el script.

#### Procedimientos
Un **procedimiento** ejecuta varias operaciones y **no devuelve un valor** (Java los
llama con `CallableStatement`, en el nodo de transacciones). Se ejecuta con `CALL`:
```sql
CREATE OR REPLACE PROCEDURE registrar_partida(p_heroe INTEGER, p_enemigo VARCHAR, p_danio INTEGER) AS $$
BEGIN
    INSERT INTO partida (heroe_id, enemigo, danio) VALUES (p_heroe, p_enemigo, p_danio);
    UPDATE heroe SET vida = GREATEST(vida - p_danio / 4, 0) WHERE id = p_heroe;
END;
$$ LANGUAGE plpgsql;

CALL registrar_partida(1, 'orco', 20);
```
Dentro se pueden declarar variables (`DECLARE total INTEGER;`), usar `IF`, bucles y
lanzar errores con `RAISE EXCEPTION 'mensaje %', valor;`.

#### Triggers
Un **trigger** es una función que la base ejecuta **sola** cuando pasa algo en una
tabla. Primero se escribe la función (que devuelve `TRIGGER`), después se la conecta:
```sql
CREATE OR REPLACE FUNCTION auditar_vida() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.vida <> OLD.vida THEN
        INSERT INTO auditoria (heroe_id, antes, despues) VALUES (OLD.id, OLD.vida, NEW.vida);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_auditar_vida
AFTER UPDATE ON heroe
FOR EACH ROW EXECUTE FUNCTION auditar_vida();
```
- `OLD` es la fila antes del cambio y `NEW`, la fila después.
- `BEFORE` corre antes (y puede modificar `NEW` o cancelar con `RAISE EXCEPTION`);
  `AFTER` corre después.
- Se usan para auditoría, para mantener totales al día y para reglas que ninguna
  restricción puede expresar.

#### Roles y permisos
En PostgreSQL, los usuarios y los grupos son **roles**. Se crean con permisos
(necesita un rol administrador):
```sql
CREATE ROLE escriba LOGIN PASSWORD 'secreta';     -- un usuario que puede conectarse
CREATE ROLE tesoreros;                            -- un grupo
GRANT tesoreros TO escriba;                       -- el escriba pasa a ser tesorero

GRANT SELECT ON heroe, partida TO escriba;        -- solo lectura
GRANT SELECT, UPDATE (oro) ON heroe TO tesoreros; -- modificar solo la columna oro
REVOKE UPDATE ON heroe FROM escriba;              -- quitar un permiso
```
El principio es el **mínimo privilegio**: cada programa o persona se conecta con un rol
que tiene solo los permisos que necesita. La aplicación de un kiosco no necesita poder
borrar tablas.

### Código de ejemplo

```sql
-- Cuarto piso: la Bóveda con lógica propia.
DROP TABLE IF EXISTS auditoria;
DROP TABLE IF EXISTS partida;
DROP TABLE IF EXISTS heroe;

CREATE TABLE heroe (id SERIAL PRIMARY KEY, nombre VARCHAR(20) NOT NULL, vida INTEGER NOT NULL, oro INTEGER NOT NULL DEFAULT 0);
CREATE TABLE partida (id SERIAL PRIMARY KEY, heroe_id INTEGER NOT NULL REFERENCES heroe(id), enemigo VARCHAR(20), danio INTEGER);
CREATE TABLE auditoria (id SERIAL PRIMARY KEY, heroe_id INTEGER, antes INTEGER, despues INTEGER);

INSERT INTO heroe (nombre, vida, oro) VALUES ('Kira', 30, 100), ('Bron', 45, 20), ('Lía', 15, 60);

-- Una función que devuelve un valor
CREATE OR REPLACE FUNCTION nivel_de(p_vida INTEGER) RETURNS VARCHAR AS $$
BEGIN
    IF p_vida >= 40 THEN
        RETURN 'fuerte';
    ELSIF p_vida >= 20 THEN
        RETURN 'normal';
    END IF;
    RETURN 'débil';
END;
$$ LANGUAGE plpgsql;

SELECT nombre, vida, nivel_de(vida) AS nivel FROM heroe ORDER BY id;

-- Un trigger de auditoría
CREATE OR REPLACE FUNCTION auditar_vida() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.vida <> OLD.vida THEN
        INSERT INTO auditoria (heroe_id, antes, despues) VALUES (OLD.id, OLD.vida, NEW.vida);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_auditar_vida AFTER UPDATE ON heroe FOR EACH ROW EXECUTE FUNCTION auditar_vida();

-- Un procedimiento que hace dos cosas y valida
CREATE OR REPLACE PROCEDURE registrar_partida(p_heroe INTEGER, p_enemigo VARCHAR, p_danio INTEGER) AS $$
BEGIN
    IF p_danio <= 0 THEN
        RAISE EXCEPTION 'el daño tiene que ser positivo (%)', p_danio;
    END IF;
    INSERT INTO partida (heroe_id, enemigo, danio) VALUES (p_heroe, p_enemigo, p_danio);
    UPDATE heroe SET vida = GREATEST(vida - p_danio / 4, 0) WHERE id = p_heroe;
END;
$$ LANGUAGE plpgsql;

CALL registrar_partida(1, 'orco', 20);
CALL registrar_partida(2, 'goblin', 12);
CALL registrar_partida(1, 'slime', 8);
UPDATE heroe SET oro = oro + 50 WHERE id = 3;       -- no cambia la vida: no se audita

SELECT h.nombre, h.vida, nivel_de(h.vida) AS nivel, COUNT(p.id) AS partidas
FROM heroe h LEFT JOIN partida p ON p.heroe_id = h.id GROUP BY h.id ORDER BY h.id;
SELECT heroe_id, antes, despues FROM auditoria ORDER BY id;
```

### Salida esperada

```
 nombre | vida | nivel  
--------+------+--------
 Kira   |   30 | normal
 Bron   |   45 | fuerte
 Lía    |   15 | débil
(3 rows)

 nombre | vida | nivel  | partidas 
--------+------+--------+----------
 Kira   |   23 | normal |        2
 Bron   |   42 | fuerte |        1
 Lía    |   15 | débil  |        0
(3 rows)

 heroe_id | antes | despues 
----------+-------+---------
        1 |    30 |      25
        2 |    45 |      42
        1 |    25 |      23
(3 rows)
```

### ¿Para qué sirve?

Los procedimientos agrupan operaciones que tienen que hacerse juntas (registrar una venta y descontar el stock), los triggers mantienen auditorías que nadie puede saltearse (quién cambió un precio y cuándo) y los roles protegen los datos: en una empresa, el sistema de ventas no tiene permiso para tocar los sueldos. La cátedra evalúa estos temas en la unidad 3.

### Errores habituales

**Slime: el `$$` o el `;` que faltan.** `ERROR: unterminated dollar-quoted string`: el
cuerpo tiene que abrir y cerrar con `$$`, y cada instrucción adentro termina con `;`.

**Esqueleto: la función que ya existe con otros parámetros.** `CREATE OR REPLACE` no
cambia la cantidad o el tipo de los parámetros: hay que borrarla antes (`DROP FUNCTION
IF EXISTS nombre(INTEGER);`).

**Ogro: el trigger que no devuelve `NEW`.** En un trigger `BEFORE`, devolver `NULL`
cancela la operación sin avisar. En uno `AFTER`, el valor se ignora, pero la función
igual tiene que tener `RETURN`.

**Troll: el trigger que se dispara a sí mismo.** Un trigger `AFTER UPDATE` sobre una
tabla que hace un `UPDATE` sobre la misma tabla se vuelve a disparar sin fin.

**Esqueleto: sin permiso.** `ERROR: permission denied for table heroe`: el rol con el
que te conectaste no tiene el `GRANT` necesario.

### Misión R04-N04-M1 · La función del descuento

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con una tabla `producto(id, nombre, precio NUMERIC(10,2), categoria)`, escribí una
función `precio_final(p_precio NUMERIC, p_categoria VARCHAR, p_socio BOOLEAN)` que
aplique: 10 % de descuento a la categoría `oferta`, 0 % al resto, y un 5 % extra si es
socio (sobre el precio ya descontado), redondeado a 2 decimales. Usala en una consulta
que muestre cada producto con su precio para no socios y para socios.

#### Criterio de aprobación

- La función es PL/pgSQL, con `IF` y `RETURN`.
- Se usa dentro de un `SELECT`.

#### Salida esperada

```
 nombre |  precio  | no_socio |  socio   
--------+----------+----------+----------
 Espada | 85000.00 | 85000.00 | 80750.00
 Poción |  3200.00 |  2880.00 |  2736.00
 Escudo | 41000.00 | 36900.00 | 35055.00
 Mapa   |   900.00 |   900.00 |   855.00
(4 rows)
```

#### Solución de referencia

```sql
-- Mision 1 - La funcion del descuento.
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (id SERIAL PRIMARY KEY, nombre VARCHAR(30), precio NUMERIC(10, 2), categoria VARCHAR(20));
INSERT INTO producto (nombre, precio, categoria) VALUES ('Espada', 85000, 'armas'), ('Poción', 3200, 'oferta'),
                                                        ('Escudo', 41000, 'oferta'), ('Mapa', 900, 'varios');

CREATE OR REPLACE FUNCTION precio_final(p_precio NUMERIC, p_categoria VARCHAR, p_socio BOOLEAN) RETURNS NUMERIC AS $$
DECLARE
    resultado NUMERIC := p_precio;
BEGIN
    IF p_categoria = 'oferta' THEN
        resultado := resultado * 0.9;
    END IF;
    IF p_socio THEN
        resultado := resultado * 0.95;
    END IF;
    RETURN ROUND(resultado, 2);
END;
$$ LANGUAGE plpgsql;

SELECT nombre, precio, precio_final(precio, categoria, FALSE) AS no_socio, precio_final(precio, categoria, TRUE) AS socio
FROM producto ORDER BY id;
```

### Misión R04-N04-M2 · El procedimiento de la venta

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con las tablas `articulo(id, nombre, stock)` y `venta(id, articulo_id, cantidad)`,
escribí un procedimiento `vender(p_articulo INTEGER, p_cantidad INTEGER)` que
**valide** que la cantidad sea positiva y que haya stock (si no, `RAISE EXCEPTION` con
un mensaje que incluya el stock disponible), registre la venta y descuente el stock.
Llamalo tres veces con ventas válidas y mostrá las dos tablas. En un comentario, poné
una llamada que fallaría y el mensaje que da.

#### Criterio de aprobación

- El procedimiento valida y lanza errores con `RAISE EXCEPTION`.
- Registra la venta y descuenta el stock en la misma llamada.

#### Salida esperada

```
 id | nombre | stock 
----+--------+-------
  1 | Flecha |    70
  2 | Arco   |     0
  3 | Carcaj |    10
(3 rows)

 id | articulo_id | cantidad 
----+-------------+----------
  1 |           1 |       30
  2 |           2 |        5
  3 |           3 |        2
(3 rows)
```

#### Solución de referencia

```sql
-- Mision 2 - El procedimiento de la venta.
DROP TABLE IF EXISTS venta;
DROP TABLE IF EXISTS articulo;
CREATE TABLE articulo (id SERIAL PRIMARY KEY, nombre VARCHAR(30), stock INTEGER NOT NULL CHECK (stock >= 0));
CREATE TABLE venta (id SERIAL PRIMARY KEY, articulo_id INTEGER REFERENCES articulo(id), cantidad INTEGER);
INSERT INTO articulo (nombre, stock) VALUES ('Flecha', 100), ('Arco', 5), ('Carcaj', 12);

CREATE OR REPLACE PROCEDURE vender(p_articulo INTEGER, p_cantidad INTEGER) AS $$
DECLARE
    disponible INTEGER;
BEGIN
    IF p_cantidad <= 0 THEN
        RAISE EXCEPTION 'la cantidad tiene que ser positiva';
    END IF;
    SELECT stock INTO disponible FROM articulo WHERE id = p_articulo;
    IF disponible IS NULL THEN
        RAISE EXCEPTION 'no existe el artículo %', p_articulo;
    END IF;
    IF disponible < p_cantidad THEN
        RAISE EXCEPTION 'stock insuficiente: hay %', disponible;
    END IF;
    INSERT INTO venta (articulo_id, cantidad) VALUES (p_articulo, p_cantidad);
    UPDATE articulo SET stock = stock - p_cantidad WHERE id = p_articulo;
END;
$$ LANGUAGE plpgsql;

CALL vender(1, 30);
CALL vender(2, 5);
CALL vender(3, 2);
-- CALL vender(2, 1);   -- ERROR: stock insuficiente: hay 0

SELECT * FROM articulo ORDER BY id;
SELECT * FROM venta ORDER BY id;
```

### Misión R04-N04-M3 · El guardián de los precios

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con una tabla `producto(id, nombre, precio)` y una tabla `historial_precio(id,
producto_id, anterior, nuevo)`, escribí **dos triggers**:

1. Un `BEFORE UPDATE` que **impida** subir un precio más del 50 % de una vez (con
   `RAISE EXCEPTION`).
2. Un `AFTER UPDATE` que registre en el historial cada cambio de precio.

Hacé tres cambios de precio válidos (uno de ellos a un producto dos veces), dejá
comentado uno inválido con su mensaje, y mostrá el historial con el nombre del
producto.

#### Criterio de aprobación

- Un trigger `BEFORE` que valida y uno `AFTER` que audita.
- Solo se registran los cambios de precio reales.

#### Salida esperada

```
 nombre | anterior |  nuevo  
--------+----------+---------
 Pan    |  1200.00 | 1500.00
 Café   |   450.00 |  520.00
 Pan    |  1500.00 | 1650.00
(3 rows)
```

#### Solución de referencia

```sql
-- Mision 3 - El guardian de los precios: un trigger BEFORE que valida y uno AFTER que audita.
DROP TABLE IF EXISTS historial_precio;
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (id SERIAL PRIMARY KEY, nombre VARCHAR(30), precio NUMERIC(10, 2));
CREATE TABLE historial_precio (id SERIAL PRIMARY KEY, producto_id INTEGER, anterior NUMERIC(10, 2), nuevo NUMERIC(10, 2));
INSERT INTO producto (nombre, precio) VALUES ('Pan', 1200), ('Café', 450), ('Guiso', 2500);

CREATE OR REPLACE FUNCTION validar_aumento() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.precio > OLD.precio * 1.5 THEN
        RAISE EXCEPTION 'aumento de más del 50%% en %', OLD.nombre;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION registrar_precio() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.precio <> OLD.precio THEN
        INSERT INTO historial_precio (producto_id, anterior, nuevo) VALUES (OLD.id, OLD.precio, NEW.precio);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_validar BEFORE UPDATE ON producto FOR EACH ROW EXECUTE FUNCTION validar_aumento();
CREATE TRIGGER tr_historial AFTER UPDATE ON producto FOR EACH ROW EXECUTE FUNCTION registrar_precio();

UPDATE producto SET precio = 1500 WHERE nombre = 'Pan';
UPDATE producto SET precio = 520 WHERE nombre = 'Café';
UPDATE producto SET precio = 1650 WHERE nombre = 'Pan';
UPDATE producto SET nombre = 'Guiso de lentejas' WHERE id = 3;     -- no cambia el precio: no se registra
-- UPDATE producto SET precio = 5000 WHERE id = 3;   -- ERROR: aumento de más del 50% en Guiso de lentejas

SELECT p.nombre, h.anterior, h.nuevo FROM historial_precio h JOIN producto p ON p.id = h.producto_id ORDER BY h.id;
```

### Encargo R04-N04-E1 · Los permisos del consultorio

```meta
entrega: archivo
entorno: local
extensiones: sql, txt, md
monedas: 1
xp: 15
```

#### Consigna

Un consultorio tiene las tablas `paciente`, `turno` e `historia_clinica`. Escribí el
script de **roles y permisos** (con un usuario administrador de PostgreSQL, como
`postgres`) para tres perfiles:

- `recepcion`: ve y carga pacientes y turnos, pero no puede ver las historias clínicas.
- `medico`: ve pacientes y turnos, y ve y carga historias clínicas, pero no borra nada.
- `auditoria`: solo puede leer todo.

Creá los tres roles como grupos, un usuario de ejemplo en cada uno, y los `GRANT`
necesarios. Explicá en comentarios por qué cada permiso es el mínimo necesario.

#### Criterio de aprobación

- Tres roles de grupo y un usuario por rol, con `GRANT … TO`.
- Ningún rol tiene más permisos de los que necesita (mínimo privilegio).

#### Solución de referencia

```sql
-- Encargo - Los permisos del consultorio (correr como postgres).
CREATE ROLE recepcion;
CREATE ROLE medico;
CREATE ROLE auditoria;

-- Recepción: atiende la agenda. Ve y carga pacientes y turnos (sin borrar), nunca las historias.
GRANT SELECT, INSERT, UPDATE ON paciente, turno TO recepcion;

-- Médico: consulta la agenda y escribe historias clínicas. No borra nada.
GRANT SELECT ON paciente, turno TO medico;
GRANT SELECT, INSERT, UPDATE ON historia_clinica TO medico;

-- Auditoría: solo lectura de todo.
GRANT SELECT ON paciente, turno, historia_clinica TO auditoria;

-- Usuarios de ejemplo, uno por perfil
CREATE ROLE marta LOGIN PASSWORD 'cambiar-esta-clave';
CREATE ROLE dr_perez LOGIN PASSWORD 'cambiar-esta-clave';
CREATE ROLE auditor LOGIN PASSWORD 'cambiar-esta-clave';
GRANT recepcion TO marta;
GRANT medico TO dr_perez;
GRANT auditoria TO auditor;

-- Las secuencias de los SERIAL también necesitan permiso para poder insertar:
-- GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO recepcion, medico;
```

### Prueba del sello

#### ¿Qué diferencia hay entre una función y un procedimiento?

La función devuelve un valor y se usa dentro de una consulta; el procedimiento ejecuta operaciones sin devolver un valor y se llama con `CALL`.

#### ¿Qué son `OLD` y `NEW` en un trigger?

La fila antes del cambio y la fila después del cambio.

#### ¿Cuándo usarías un trigger `BEFORE` y cuándo uno `AFTER`?

`BEFORE` para validar o modificar los datos antes de guardarlos (puede cancelar la operación); `AFTER` para reaccionar a un cambio ya hecho, como auditar.

#### ¿Qué es el principio de mínimo privilegio?

Que cada usuario o programa tenga solo los permisos que necesita para su tarea.

#### ¿Cómo se lanza un error desde PL/pgSQL?

Con `RAISE EXCEPTION 'mensaje %', valor;`.

### Soluciones (docente)

Sale de `18-Java/28-SQL-Procedimientos-Roles` (unidad 3). El encargo de roles no se ejecuta en el súper test porque necesita un superusuario (`CREATE ROLE`); se corrige leyendo el script. En `RAISE EXCEPTION`, el `%%` escribe un `%` literal. El procedimiento del ejemplo se llama desde Java con `CallableStatement` en el nodo de transacciones.

## R04-N05 · JDBC: conectarse y consultar

```meta
tipo: tema
padre: R04-N04
precio: 10
criatura: goblin
temas: sql.desde-codigo, sql.inyeccion
```

### Crónica

La Bóveda tiene sus propias reglas y su propia lengua. Pero los programas del Imperio viven arriba, en Java. Entre los dos pisos hay un **tubo de bronce**: arriba se escribe una pregunta en SQL, se la manda por el tubo, y abajo la Oráculo responde con una tabla que sube de vuelta.

—Ese tubo se llama **JDBC** —dice {mentor}—. Con él, tus programas guardan y consultan datos en la Bóveda. Pero cuidado con lo que mandás por el tubo, {heroe}: hay quienes esconden órdenes en un nombre para robar lo que no les corresponde.

### Objetivos

- Conectarse a PostgreSQL desde Java con el driver JDBC.
- Ejecutar consultas con `PreparedStatement` y recorrer un `ResultSet`.
- Entender la inyección SQL y por qué nunca hay que armar SQL concatenando textos.
- Cerrar conexiones con `try` con recursos y manejar `SQLException`.
- Leer los metadatos de un resultado con `ResultSetMetaData`.

### Antes de empezar

- SQL: consultas, JOIN y vistas.
- Excepciones y `try` con recursos (rama 3).

### Explicación

#### Las piezas de JDBC
| Pieza | Qué es |
|---|---|
| **Driver** | la librería que sabe hablar con cada motor (un `.jar`; el de PostgreSQL es `postgresql-42.x.jar`) |
| `DriverManager` | abre conexiones a partir de una URL |
| `Connection` | la conexión abierta con la base |
| `PreparedStatement` | una sentencia SQL con parámetros `?` |
| `ResultSet` | el resultado de una consulta, fila por fila |
| `SQLException` | la excepción (checked) de todo lo que sale mal |

Todas son **interfaces** de `java.sql`: el mismo código funciona con PostgreSQL, MySQL
u Oracle cambiando el driver y la URL.

#### Conseguir el driver y ejecutar
Bajá el driver de PostgreSQL (`postgresql-42.7.x.jar`, de jdbc.postgresql.org o de
Maven Central) y ponelo junto a tu programa. Con un programa de un archivo:
```bash
java -cp postgresql-42.7.4.jar Heroes.java
```

#### La conexión
```java
String url = "jdbc:postgresql://localhost:5432/imperio";   // motor, servidor, puerto y base
try (Connection con = DriverManager.getConnection(url, "imperio", "imperio")) {
    …
}   // al salir del bloque, la conexión se cierra
```
Las conexiones son un recurso caro: **siempre** con `try` con recursos.

Los datos de conexión conviene tenerlos **en un solo lugar**. En este curso usamos una
clase `Conexion` con constantes; en un sistema real se leen de un `.properties` o de
variables de entorno (así la clave no queda escrita en el código ni se sube a un
repositorio):
```java
final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

#### Consultar: `PreparedStatement` y `ResultSet`
```java
String sql = "SELECT nombre, vida FROM heroe WHERE clase = ? ORDER BY nombre";
try (Connection con = Conexion.abrir();
     PreparedStatement ps = con.prepareStatement(sql)) {
    ps.setString(1, "mago");                      // el primer ? (se cuenta desde 1)
    try (ResultSet rs = ps.executeQuery()) {
        while (rs.next()) {                       // avanza a la próxima fila; false si no hay más
            String nombre = rs.getString("nombre");
            int vida = rs.getInt("vida");
            System.out.println(nombre + " " + vida);
        }
    }
}
```
- Los `?` se completan con `setString`, `setInt`, `setDouble`, `setBigDecimal`,
  `setDate`… según el tipo, contando desde **1**.
- `executeQuery()` es para `SELECT` (devuelve un `ResultSet`); `executeUpdate()` es
  para `INSERT`, `UPDATE` y `DELETE` (devuelve cuántas filas cambió).
- `rs.getX("columna")` lee una columna de la fila actual. Para un `NULL` de la base,
  `getInt` devuelve 0: si importa, preguntá después con `rs.wasNull()`.

#### La inyección SQL
**Nunca** armes el SQL concatenando lo que escribió el usuario:
```java
String sql = "SELECT * FROM usuario WHERE nombre = '" + nombre + "' AND clave = '" + clave + "'";
```
Si alguien escribe como clave `' OR '1'='1`, la consulta queda
`… AND clave = '' OR '1'='1'`, que es verdadera para **todas** las filas: entra sin
saber la clave. Con `PreparedStatement` y `?`, el valor viaja **separado** del SQL y la
base nunca lo interpreta como código. Es la vulnerabilidad más conocida de la web, y se
evita siempre de la misma forma.

#### Metadatos: `ResultSetMetaData`
Para mostrar un resultado sin saber de antemano qué columnas tiene (como hace una
`JTable` genérica), se piden los **metadatos**:
```java
ResultSetMetaData md = rs.getMetaData();
int columnas = md.getColumnCount();
for (int i = 1; i <= columnas; i++) {
    System.out.print(md.getColumnName(i) + " ");
}
```

#### Cuando algo sale mal
Todo en JDBC puede lanzar `SQLException`: la base apagada, la clave mal, una tabla que
no existe, una restricción violada. `e.getMessage()` trae el mensaje de PostgreSQL y
`e.getSQLState()` un código estándar (`23505` es clave duplicada, `23503` clave
foránea violada).

> **Si venís de Python.** JDBC cumple el papel de `psycopg2` (o de la DB-API): la
> conexión es `connect`, el `PreparedStatement` es el cursor con parámetros `%s`, y el
> `ResultSet` son las filas de `fetchall`.

### Código de ejemplo

Antes de ejecutarlo, cargá las tablas en tu base con `psql … -f schema.sql`.

`schema.sql`

```sql
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS heroe;
CREATE TABLE heroe (id SERIAL PRIMARY KEY, nombre VARCHAR(20) NOT NULL, clase VARCHAR(20) NOT NULL, vida INTEGER NOT NULL);
CREATE TABLE usuario (nombre VARCHAR(20) PRIMARY KEY, clave VARCHAR(20) NOT NULL);
INSERT INTO heroe (nombre, clase, vida) VALUES ('Kira', 'arquera', 30), ('Olmo', 'mago', 25), ('Bron', 'guerrero', 45), ('Lía', 'mago', 20);
INSERT INTO usuario VALUES ('kaffa', 'cafe123');
```

```java
/*
 * JDBC: el tubo de bronce entre Java y la Bóveda.
 * Ejecutar con: java -cp postgresql-42.7.4.jar TuboDeBronce.java
 */
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;

public class TuboDeBronce {
    public static void main(String[] args) {
        try (Connection con = Conexion.abrir()) {
            System.out.println("Conectado a " + con.getMetaData().getDatabaseProductName());

            // Consulta con un parámetro
            try (PreparedStatement ps = con.prepareStatement("SELECT nombre, vida FROM heroe WHERE clase = ? ORDER BY nombre")) {
                ps.setString(1, "mago");
                try (ResultSet rs = ps.executeQuery()) {
                    while (rs.next()) {
                        System.out.println("  mago: " + rs.getString("nombre") + " (" + rs.getInt("vida") + ")");
                    }
                }
            }

            // Metadatos: mostrar una tabla sin conocer sus columnas
            try (Statement st = con.createStatement();
                 ResultSet rs = st.executeQuery("SELECT * FROM heroe ORDER BY id")) {
                ResultSetMetaData md = rs.getMetaData();
                StringBuilder encabezado = new StringBuilder();
                for (int i = 1; i <= md.getColumnCount(); i++) {
                    encabezado.append(String.format("%-10s", md.getColumnName(i)));
                }
                System.out.println(encabezado.toString().trim());
                while (rs.next()) {
                    StringBuilder fila = new StringBuilder();
                    for (int i = 1; i <= md.getColumnCount(); i++) {
                        fila.append(String.format("%-10s", rs.getString(i)));
                    }
                    System.out.println(fila.toString().trim());
                }
            }

            // La inyección SQL: la misma "clave" con los dos métodos
            String clave = "' OR '1'='1";
            System.out.println("Login concatenando: " + loginInseguro(con, "kaffa", clave));
            System.out.println("Login con PreparedStatement: " + loginSeguro(con, "kaffa", clave));
            System.out.println("Login con la clave real: " + loginSeguro(con, "kaffa", "cafe123"));
        } catch (SQLException e) {
            System.out.println("Error de base de datos: " + e.getMessage());
        }
    }

    // MAL: nunca armes SQL concatenando datos del usuario.
    static boolean loginInseguro(Connection con, String nombre, String clave) throws SQLException {
        String sql = "SELECT 1 FROM usuario WHERE nombre = '" + nombre + "' AND clave = '" + clave + "'";
        try (Statement st = con.createStatement(); ResultSet rs = st.executeQuery(sql)) {
            return rs.next();
        }
    }

    static boolean loginSeguro(Connection con, String nombre, String clave) throws SQLException {
        try (PreparedStatement ps = con.prepareStatement("SELECT 1 FROM usuario WHERE nombre = ? AND clave = ?")) {
            ps.setString(1, nombre);
            ps.setString(2, clave);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next();
            }
        }
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    private Conexion() {
    }

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Salida esperada

```
Conectado a PostgreSQL
  mago: Lía (20)
  mago: Olmo (25)
id        nombre    clase     vida
1         Kira      arquera   30
2         Olmo      mago      25
3         Bron      guerrero  45
4         Lía       mago      20
Login concatenando: true
Login con PreparedStatement: false
Login con la clave real: true
```

### ¿Para qué sirve?

JDBC es la base de todo acceso a datos en Java: los sistemas de escritorio de la cátedra, los servidores web con Spring (que usa JDBC por debajo) y las herramientas de reportes. Saber usarlo bien —con conexiones que se cierran y parámetros que evitan la inyección— es lo que separa un sistema seguro de uno que un curioso puede vaciar desde el formulario de login.

### Errores habituales

**Esqueleto: el driver no está en el classpath.**
```
Error de base de datos: No suitable driver found for jdbc:postgresql://localhost:5432/imperio
```
Ejecutá con `-cp postgresql-42.7.4.jar` (o agregá el jar a tu proyecto en el IDE).

**Goblin: la base no responde o la clave está mal.** `Connection refused` (PostgreSQL
no está corriendo o el puerto es otro) o `password authentication failed for user`.

**Orco: la columna 0.** `rs.getString(0)` corta con `The column index is out of range:
0`: las columnas y los `?` se cuentan desde **1**.

**Ogro: leer sin `next()`.** `rs.getString("nombre")` antes del primer `rs.next()`:
`ResultSet not positioned properly, perhaps you need to call next`.

**Dragón: la inyección SQL.** Cualquier SQL armado con `+` y datos del usuario es un
agujero de seguridad. Siempre `PreparedStatement` con `?`.

**Troll: la conexión que no se cierra.** Sin `try` con recursos, cada consulta deja una
conexión abierta hasta que la base dice `too many clients already`.

### Misión R04-N05-M1 · El listado de la Bóveda

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con las tablas de `schema.sql` (cargalas primero), escribí un programa JDBC que pida
un **precio máximo** por teclado y muestre las armas que cuestan eso o menos, con su
herrero, ordenadas por precio (usá un `JOIN` en el SQL y un `?` para el precio). Al
final mostrá cuántas armas se listaron. Mostrá los precios con 2 decimales.

`schema.sql`

```sql
DROP TABLE IF EXISTS arma;
DROP TABLE IF EXISTS herrero;
CREATE TABLE herrero (id SERIAL PRIMARY KEY, nombre VARCHAR(20) NOT NULL);
CREATE TABLE arma (id SERIAL PRIMARY KEY, nombre VARCHAR(30) NOT NULL, precio NUMERIC(10, 2) NOT NULL, herrero_id INTEGER REFERENCES herrero(id));
INSERT INTO herrero (nombre) VALUES ('Ferrum'), ('Tesla');
INSERT INTO arma (nombre, precio, herrero_id) VALUES ('Colmillo', 85000, 1), ('Brisa', 42000.5, 2), ('Daga', 9000, 1), ('Martillo', 61000, 2);
```

#### Criterio de aprobación

- Usa `PreparedStatement` con `?` y `try` con recursos.
- El SQL tiene el `JOIN` y el `ORDER BY`.

#### Entrada de ejemplo

```
61000
```

#### Salida esperada

```
Precio máximo: 
Daga          9000.00  (Ferrum)
Brisa        42000.50  (Tesla)
Martillo     61000.00  (Tesla)
3 armas
```

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS arma;
DROP TABLE IF EXISTS herrero;
CREATE TABLE herrero (id SERIAL PRIMARY KEY, nombre VARCHAR(20) NOT NULL);
CREATE TABLE arma (id SERIAL PRIMARY KEY, nombre VARCHAR(30) NOT NULL, precio NUMERIC(10, 2) NOT NULL, herrero_id INTEGER REFERENCES herrero(id));
INSERT INTO herrero (nombre) VALUES ('Ferrum'), ('Tesla');
INSERT INTO arma (nombre, precio, herrero_id) VALUES ('Colmillo', 85000, 1), ('Brisa', 42000.5, 2), ('Daga', 9000, 1), ('Martillo', 61000, 2);
```

```java
// Mision 1 - El listado de la Boveda: PreparedStatement con un parametro y un JOIN.
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Locale;
import java.util.Scanner;

public class ListadoBoveda {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Scanner teclado = new Scanner(System.in);
        System.out.print("Precio máximo: ");
        double maximo = Double.parseDouble(teclado.nextLine().trim());
        System.out.println();
        String sql = "SELECT a.nombre, a.precio, h.nombre AS herrero FROM arma a JOIN herrero h ON h.id = a.herrero_id "
                + "WHERE a.precio <= ? ORDER BY a.precio";
        try (Connection con = Conexion.abrir(); PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setDouble(1, maximo);
            int cantidad = 0;
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    System.out.printf("%-10s %10.2f  (%s)%n", rs.getString("nombre"), rs.getDouble("precio"), rs.getString("herrero"));
                    cantidad++;
                }
            }
            System.out.println(cantidad + " armas");
        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Misión R04-N05-M2 · El buscador de viajeros

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí un buscador: leé textos de la entrada (uno por línea, hasta una vacía) y, para
cada uno, mostrá los viajeros cuyo nombre **contiene** ese texto sin importar
mayúsculas (`ILIKE`), con su ciudad. El comodín `%` se agrega en Java al **valor** del
parámetro, no en el SQL (`ps.setString(1, "%" + texto + "%")`). Si no hay
resultados, decí "sin resultados". Probá también con un texto "malicioso" y mostrá que
no pasa nada raro.

`schema.sql`

```sql
DROP TABLE IF EXISTS viajero;
CREATE TABLE viajero (id SERIAL PRIMARY KEY, nombre VARCHAR(30) NOT NULL, ciudad VARCHAR(20));
INSERT INTO viajero (nombre, ciudad) VALUES ('Kira Valdez', 'Valle'), ('Bron Tallo', 'Forjas'),
                                            ('Lía Ferrari', 'Valle'), ('Nara Kel', 'Ciudadela'), ('Olmo Ríos', NULL);
```

#### Criterio de aprobación

- El `%` va en el valor del parámetro, no concatenado en el SQL.
- Maneja la ciudad `NULL`.

#### Entrada de ejemplo

```
ra
tallo
' OR '1'='1
zzz

```

#### Salida esperada

```
Buscando 'ra':
  Kira Valdez - Valle
  Lía Ferrari - Valle
  Nara Kel - Ciudadela
Buscando 'tallo':
  Bron Tallo - Forjas
Buscando '' OR '1'='1':
  sin resultados
Buscando 'zzz':
  sin resultados
```

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS viajero;
CREATE TABLE viajero (id SERIAL PRIMARY KEY, nombre VARCHAR(30) NOT NULL, ciudad VARCHAR(20));
INSERT INTO viajero (nombre, ciudad) VALUES ('Kira Valdez', 'Valle'), ('Bron Tallo', 'Forjas'),
                                            ('Lía Ferrari', 'Valle'), ('Nara Kel', 'Ciudadela'), ('Olmo Ríos', NULL);
```

```java
// Mision 2 - El buscador de viajeros: ILIKE con el comodin en el parametro.
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Scanner;

public class Buscador {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("SELECT nombre, ciudad FROM viajero WHERE nombre ILIKE ? ORDER BY nombre")) {
            while (teclado.hasNextLine()) {
                String texto = teclado.nextLine().trim();
                if (texto.isEmpty()) {
                    break;
                }
                ps.setString(1, "%" + texto + "%");
                System.out.println("Buscando '" + texto + "':");
                boolean alguno = false;
                try (ResultSet rs = ps.executeQuery()) {
                    while (rs.next()) {
                        String ciudad = rs.getString("ciudad");
                        System.out.println("  " + rs.getString("nombre") + " - " + (ciudad == null ? "ciudad desconocida" : ciudad));
                        alguno = true;
                    }
                }
                if (!alguno) {
                    System.out.println("  sin resultados");
                }
            }
        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Misión R04-N05-M3 · La tabla universal

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí un método `static void mostrar(Connection con, String consulta)` que ejecute
**cualquier** `SELECT` y lo muestre como tabla usando `ResultSetMetaData`: un
encabezado con los nombres de las columnas, cada columna con el ancho del dato más
largo (calculalo leyendo primero todas las filas en una lista), los `NULL` como
`(nulo)` y al final la cantidad de filas. Probalo con tres consultas distintas sobre las
tablas de `schema.sql`, incluida una con un `GROUP BY`.

`schema.sql`

```sql
DROP TABLE IF EXISTS partida;
DROP TABLE IF EXISTS heroe;
CREATE TABLE heroe (id SERIAL PRIMARY KEY, nombre VARCHAR(20), clan VARCHAR(20));
CREATE TABLE partida (id SERIAL PRIMARY KEY, heroe_id INTEGER REFERENCES heroe(id), enemigo VARCHAR(20), danio INTEGER);
INSERT INTO heroe (nombre, clan) VALUES ('Kira', 'Valle'), ('Bron', 'Forjas'), ('Olmo', NULL);
INSERT INTO partida (heroe_id, enemigo, danio) VALUES (1, 'goblin', 12), (1, 'orco', 18), (2, 'orco', 30);
```

#### Criterio de aprobación

- Usa `getColumnCount` y `getColumnName`/`getColumnLabel`.
- Los anchos se calculan con los datos y los `NULL` se muestran.

#### Salida esperada

```
id | nombre | clan
1  | Kira   | Valle
2  | Bron   | Forjas
3  | Olmo   | (nulo)
(3 filas)

nombre | enemigo | danio
Kira   | goblin  | 12
Kira   | orco    | 18
Bron   | orco    | 30
(3 filas)

enemigo | veces | total
goblin  | 1     | 12
orco    | 2     | 48
(2 filas)
```

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS partida;
DROP TABLE IF EXISTS heroe;
CREATE TABLE heroe (id SERIAL PRIMARY KEY, nombre VARCHAR(20), clan VARCHAR(20));
CREATE TABLE partida (id SERIAL PRIMARY KEY, heroe_id INTEGER REFERENCES heroe(id), enemigo VARCHAR(20), danio INTEGER);
INSERT INTO heroe (nombre, clan) VALUES ('Kira', 'Valle'), ('Bron', 'Forjas'), ('Olmo', NULL);
INSERT INTO partida (heroe_id, enemigo, danio) VALUES (1, 'goblin', 12), (1, 'orco', 18), (2, 'orco', 30);
```

```java
// Mision 3 - La tabla universal: ResultSetMetaData para mostrar cualquier consulta.
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

public class TablaUniversal {
    public static void main(String[] args) {
        try (Connection con = Conexion.abrir()) {
            mostrar(con, "SELECT * FROM heroe ORDER BY id");
            mostrar(con, "SELECT h.nombre, p.enemigo, p.danio FROM partida p JOIN heroe h ON h.id = p.heroe_id ORDER BY p.id");
            mostrar(con, "SELECT enemigo, COUNT(*) AS veces, SUM(danio) AS total FROM partida GROUP BY enemigo ORDER BY enemigo");
        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void mostrar(Connection con, String consulta) throws SQLException {
        try (Statement st = con.createStatement(); ResultSet rs = st.executeQuery(consulta)) {
            ResultSetMetaData md = rs.getMetaData();
            int n = md.getColumnCount();
            String[] encabezado = new String[n];
            int[] anchos = new int[n];
            for (int i = 0; i < n; i++) {
                encabezado[i] = md.getColumnLabel(i + 1);
                anchos[i] = encabezado[i].length();
            }
            List<String[]> filas = new ArrayList<>();
            while (rs.next()) {
                String[] fila = new String[n];
                for (int i = 0; i < n; i++) {
                    String valor = rs.getString(i + 1);
                    fila[i] = valor == null ? "(nulo)" : valor;
                    anchos[i] = Math.max(anchos[i], fila[i].length());
                }
                filas.add(fila);
            }
            imprimir(encabezado, anchos);
            for (String[] fila : filas) {
                imprimir(fila, anchos);
            }
            System.out.println("(" + filas.size() + " filas)");
            System.out.println();
        }
    }

    static void imprimir(String[] valores, int[] anchos) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < valores.length; i++) {
            sb.append(String.format("%-" + anchos[i] + "s", valores[i]));
            if (i < valores.length - 1) {
                sb.append(" | ");
            }
        }
        System.out.println(sb.toString().stripTrailing());
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Encargo R04-N05-E1 · El login del sistema

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Escribí el login de un sistema de gestión contra la tabla `usuario` de `schema.sql`:
leé pares usuario / clave (dos líneas cada uno) hasta una línea vacía y, para cada par,
mostrá si entra y con qué rol. Usá `PreparedStatement`. Si un usuario falla 3 veces
seguidas, queda **bloqueado** (actualizá la columna `bloqueado` con un `UPDATE`) y ya
no puede entrar aunque ponga bien la clave. Un login correcto pone los intentos en 0.
Probá también la inyección clásica.

`schema.sql`

```sql
DROP TABLE IF EXISTS usuario;
CREATE TABLE usuario (nombre VARCHAR(20) PRIMARY KEY, clave VARCHAR(30) NOT NULL, rol VARCHAR(20) NOT NULL,
                      intentos INTEGER NOT NULL DEFAULT 0, bloqueado BOOLEAN NOT NULL DEFAULT FALSE);
INSERT INTO usuario (nombre, clave, rol) VALUES ('kaffa', 'cafe123', 'admin'), ('bron', 'martillo', 'vendedor');
```

(En un sistema real las claves nunca se guardan tal cual: se guarda un *hash*. Para este
ejercicio alcanza con el texto.)

#### Criterio de aprobación

- Todo el acceso usa `PreparedStatement`.
- El bloqueo se guarda en la base y se respeta.

#### Entrada de ejemplo

```
bron
martillo
kaffa
' OR '1'='1
kaffa
te
kaffa
cafe
kaffa
cafe123

```

#### Salida esperada

```
bron: acceso concedido (rol vendedor)
kaffa: clave incorrecta (intento 1)
kaffa: clave incorrecta (intento 2)
kaffa: clave incorrecta: usuario bloqueado
kaffa: usuario bloqueado
```

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS usuario;
CREATE TABLE usuario (nombre VARCHAR(20) PRIMARY KEY, clave VARCHAR(30) NOT NULL, rol VARCHAR(20) NOT NULL,
                      intentos INTEGER NOT NULL DEFAULT 0, bloqueado BOOLEAN NOT NULL DEFAULT FALSE);
INSERT INTO usuario (nombre, clave, rol) VALUES ('kaffa', 'cafe123', 'admin'), ('bron', 'martillo', 'vendedor');
```

```java
// Encargo - El login del sistema: PreparedStatement, intentos y bloqueo guardados en la base.
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Scanner;

public class Login {
    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        try (Connection con = Conexion.abrir()) {
            while (teclado.hasNextLine()) {
                String usuario = teclado.nextLine().trim();
                if (usuario.isEmpty() || !teclado.hasNextLine()) {
                    break;
                }
                String clave = teclado.nextLine();
                System.out.println(usuario + ": " + intentar(con, usuario, clave));
            }
        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static String intentar(Connection con, String usuario, String clave) throws SQLException {
        try (PreparedStatement ps = con.prepareStatement("SELECT clave, rol, intentos, bloqueado FROM usuario WHERE nombre = ?")) {
            ps.setString(1, usuario);
            try (ResultSet rs = ps.executeQuery()) {
                if (!rs.next()) {
                    return "usuario inexistente";
                }
                if (rs.getBoolean("bloqueado")) {
                    return "usuario bloqueado";
                }
                if (rs.getString("clave").equals(clave)) {
                    actualizar(con, usuario, 0, false);
                    return "acceso concedido (rol " + rs.getString("rol") + ")";
                }
                int intentos = rs.getInt("intentos") + 1;
                boolean bloquear = intentos >= 3;
                actualizar(con, usuario, intentos, bloquear);
                return bloquear ? "clave incorrecta: usuario bloqueado" : "clave incorrecta (intento " + intentos + ")";
            }
        }
    }

    static void actualizar(Connection con, String usuario, int intentos, boolean bloqueado) throws SQLException {
        try (PreparedStatement ps = con.prepareStatement("UPDATE usuario SET intentos = ?, bloqueado = ? WHERE nombre = ?")) {
            ps.setInt(1, intentos);
            ps.setBoolean(2, bloqueado);
            ps.setString(3, usuario);
            ps.executeUpdate();
        }
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Prueba del sello

#### ¿Para qué sirve el driver JDBC?

Es la librería que sabe hablar con un motor de base de datos concreto; sin él, `DriverManager` no puede abrir la conexión.

#### ¿Qué diferencia hay entre `executeQuery` y `executeUpdate`?

`executeQuery` es para `SELECT` y devuelve un `ResultSet`; `executeUpdate` es para `INSERT`, `UPDATE` y `DELETE` y devuelve cuántas filas cambió.

#### ¿Desde qué número se cuentan los `?` y las columnas?

Desde 1.

#### ¿Por qué `PreparedStatement` evita la inyección SQL?

Porque el valor viaja separado del SQL y la base nunca lo interpreta como código.

#### ¿Qué hace `rs.next()`?

Avanza a la siguiente fila del resultado y devuelve `false` cuando no hay más.

### Soluciones (docente)

Sale de `18-Java/30-JDBC-Conexion` (unidad 5). Corrige lo que marcó la auditoría: los datos de conexión quedan en un solo lugar (la clase `Conexion`; en la rama del escritorio se leen de un `.properties`), todo usa `try` con recursos, y se suma `ResultSetMetaData`, que usa el caso práctico de la cátedra. El súper test corre los programas JDBC contra una base local con el `schema.sql` de cada práctica.

## R04-N06 · DAO: el ABM completo desde Java

```meta
tipo: tema
padre: R04-N05
precio: 10
criatura: skeleton
temas: diseno.capas
usa: sql.desde-codigo, poo.records
```

### Crónica

En la Bóveda trabajan los **Mensajeros**: cada uno se ocupa de una sola tabla. El de los héroes sabe listar héroes, buscarlos, darlos de alta, modificarlos y borrarlos; el resto del Imperio le pide cosas a él y nunca escribe SQL. Si mañana la Bóveda se muda, solo cambia el mensajero.

—No desparrames SQL por todo tu programa —dice {mentor}—. Juntalo en un **DAO**, un objeto de acceso a datos por cada tabla. Así el resto del código habla de héroes, no de columnas, {heroe}.

### Objetivos

- Separar el acceso a datos en clases DAO con una interfaz.
- Representar cada fila con un *bean* o un `record`.
- Hacer el ABM completo: listar, buscar, insertar (obteniendo el id generado), modificar y borrar.
- Traducir las `SQLException` en excepciones propias del sistema.

### Antes de empezar

- JDBC: conectarse y consultar.
- Interfaces y excepciones propias.

### Explicación

#### El problema
Si cada parte del programa escribe su propio SQL, un cambio en una tabla obliga a
buscar consultas por todos lados, y la lógica del negocio queda mezclada con
`PreparedStatement` y `ResultSet`.

#### El patrón DAO
Un **DAO** (*Data Access Object*) es una clase que concentra todo el acceso a **una
tabla** (o entidad). Se define con una **interfaz** y se implementa para un motor
concreto:
```java
interface HeroeDAO {
    List<Heroe> listar() throws DatosException;
    Heroe buscar(int id) throws DatosException;          // lanza NoEncontradoException si no existe
    Heroe insertar(Heroe h) throws DatosException;       // devuelve el héroe con su id
    void actualizar(Heroe h) throws DatosException;
    void eliminar(int id) throws DatosException;
}

class HeroeDAOPostgres implements HeroeDAO { … }
```
El resto del programa usa `HeroeDAO` (la interfaz): no sabe que hay PostgreSQL detrás.
Para probar sin base se puede escribir un `HeroeDAOMemoria` con un `Map`.

#### El bean: una fila como objeto
Cada fila se representa con un objeto: en la cátedra se lo llama **bean** (una clase
con atributos privados, constructor vacío, getters y setters), y en Java moderno se
puede usar un `record`:
```java
record Heroe(int id, String nombre, String clase, int vida) {
    Heroe conId(int nuevoId) {                            // un id nuevo para el que se insertó
        return new Heroe(nuevoId, nombre, clase, vida);
    }
}
```

#### Insertar y obtener el id generado
Con `SERIAL`, la base elige el id. Para saberlo después del `INSERT`:
```java
String sql = "INSERT INTO heroe (nombre, clase, vida) VALUES (?, ?, ?)";
try (PreparedStatement ps = con.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
    ps.setString(1, h.nombre());
    ps.setString(2, h.clase());
    ps.setInt(3, h.vida());
    ps.executeUpdate();
    try (ResultSet claves = ps.getGeneratedKeys()) {
        claves.next();
        return h.conId(claves.getInt(1));
    }
}
```
`getGeneratedKeys` funciona con cualquier motor (PostgreSQL también permite
`INSERT … RETURNING id`, pero es propio de PostgreSQL).

#### Modificar y borrar
`executeUpdate` devuelve cuántas filas cambió: si es 0, el id no existía.
```java
int filas = ps.executeUpdate();
if (filas == 0) {
    throw new NoEncontradoException("no existe el héroe " + id);
}
```

#### Excepciones propias en el DAO
El DAO atrapa las `SQLException` y lanza las del sistema, con la original como causa:
```java
} catch (SQLException e) {
    throw new DatosException("no se pudo guardar el héroe", e);
}
```
Así la capa de arriba no depende de JDBC, y el mensaje habla el idioma del negocio.

#### Una conexión por operación
En un programa chico, cada método del DAO abre su conexión con `try` con recursos y la
cierra al terminar. En sistemas grandes se usa un *pool* de conexiones (lo hace Spring,
en la Senda del Puerto).

### Código de ejemplo

`schema.sql`

```sql
DROP TABLE IF EXISTS heroe;
CREATE TABLE heroe (id SERIAL PRIMARY KEY, nombre VARCHAR(20) NOT NULL UNIQUE, clase VARCHAR(20) NOT NULL, vida INTEGER NOT NULL CHECK (vida >= 0));
INSERT INTO heroe (nombre, clase, vida) VALUES ('Kira', 'arquera', 30), ('Bron', 'guerrero', 45);
```

```java
/*
 * DAO: el mensajero de los héroes. Todo el SQL de la tabla heroe vive en HeroeDAOPostgres.
 */
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

public class Mensajeros {
    public static void main(String[] args) {
        HeroeDAO dao = new HeroeDAOPostgres();
        try {
            Heroe lia = dao.insertar(new Heroe(0, "Lía", "maga", 20));
            System.out.println("Insertada con id " + lia.id());
            dao.actualizar(new Heroe(lia.id(), "Lía", "hechicera", 26));
            dao.eliminar(2);
            for (Heroe h : dao.listar()) {
                System.out.println("  " + h);
            }
            System.out.println("Buscar 1: " + dao.buscar(1));
            dao.buscar(99);
        } catch (NoEncontradoException e) {
            System.out.println("No encontrado: " + e.getMessage());
        } catch (DatosException e) {
            System.out.println("Error de datos: " + e.getMessage());
        }

        try {
            dao.insertar(new Heroe(0, "Kira", "arquera", 10));      // nombre repetido
        } catch (DatosException e) {
            System.out.println("Error de datos: " + e.getMessage() + " (causa: " + e.getCause().getClass().getSimpleName() + ")");
        }
    }
}

record Heroe(int id, String nombre, String clase, int vida) {
    Heroe conId(int nuevoId) {
        return new Heroe(nuevoId, nombre, clase, vida);
    }
}

class DatosException extends Exception {
    public DatosException(String mensaje, Throwable causa) {
        super(mensaje, causa);
    }
}

class NoEncontradoException extends DatosException {
    public NoEncontradoException(String mensaje) {
        super(mensaje, null);
    }
}

interface HeroeDAO {
    List<Heroe> listar() throws DatosException;

    Heroe buscar(int id) throws DatosException;

    Heroe insertar(Heroe h) throws DatosException;

    void actualizar(Heroe h) throws DatosException;

    void eliminar(int id) throws DatosException;
}

class HeroeDAOPostgres implements HeroeDAO {
    @Override
    public List<Heroe> listar() throws DatosException {
        List<Heroe> lista = new ArrayList<>();
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("SELECT id, nombre, clase, vida FROM heroe ORDER BY id");
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                lista.add(leer(rs));
            }
            return lista;
        } catch (SQLException e) {
            throw new DatosException("no se pudo listar los héroes", e);
        }
    }

    @Override
    public Heroe buscar(int id) throws DatosException {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("SELECT id, nombre, clase, vida FROM heroe WHERE id = ?")) {
            ps.setInt(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                if (!rs.next()) {
                    throw new NoEncontradoException("no existe el héroe " + id);
                }
                return leer(rs);
            }
        } catch (SQLException e) {
            throw new DatosException("no se pudo buscar el héroe " + id, e);
        }
    }

    @Override
    public Heroe insertar(Heroe h) throws DatosException {
        String sql = "INSERT INTO heroe (nombre, clase, vida) VALUES (?, ?, ?)";
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, h.nombre());
            ps.setString(2, h.clase());
            ps.setInt(3, h.vida());
            ps.executeUpdate();
            try (ResultSet claves = ps.getGeneratedKeys()) {
                claves.next();
                return h.conId(claves.getInt(1));
            }
        } catch (SQLException e) {
            throw new DatosException("no se pudo guardar el héroe " + h.nombre(), e);
        }
    }

    @Override
    public void actualizar(Heroe h) throws DatosException {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("UPDATE heroe SET nombre = ?, clase = ?, vida = ? WHERE id = ?")) {
            ps.setString(1, h.nombre());
            ps.setString(2, h.clase());
            ps.setInt(3, h.vida());
            ps.setInt(4, h.id());
            if (ps.executeUpdate() == 0) {
                throw new NoEncontradoException("no existe el héroe " + h.id());
            }
        } catch (SQLException e) {
            throw new DatosException("no se pudo modificar el héroe " + h.id(), e);
        }
    }

    @Override
    public void eliminar(int id) throws DatosException {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("DELETE FROM heroe WHERE id = ?")) {
            ps.setInt(1, id);
            if (ps.executeUpdate() == 0) {
                throw new NoEncontradoException("no existe el héroe " + id);
            }
        } catch (SQLException e) {
            throw new DatosException("no se pudo borrar el héroe " + id, e);
        }
    }

    private Heroe leer(ResultSet rs) throws SQLException {
        return new Heroe(rs.getInt("id"), rs.getString("nombre"), rs.getString("clase"), rs.getInt("vida"));
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Salida esperada

```
Insertada con id 3
  Heroe[id=1, nombre=Kira, clase=arquera, vida=30]
  Heroe[id=3, nombre=Lía, clase=hechicera, vida=26]
Buscar 1: Heroe[id=1, nombre=Kira, clase=arquera, vida=30]
No encontrado: no existe el héroe 99
Error de datos: no se pudo guardar el héroe Kira (causa: PSQLException)
```

### ¿Para qué sirve?

El patrón DAO es la forma estándar de organizar el acceso a datos en Java: lo pide la cátedra en el caso práctico del final (paquete `DAO`), lo usan los sistemas de escritorio y es la base de los *repositorios* de Spring. Separar el SQL permite cambiar de base de datos, probar la lógica sin base (con un DAO en memoria) y leer el resto del programa sin ruido técnico.

### Errores habituales

**Ogro: SQL fuera del DAO.** Un `PreparedStatement` en la pantalla o en el `main` rompe
la separación: todo el SQL de una tabla va en su DAO.

**Esqueleto: el id que no vuelve.** Sin `Statement.RETURN_GENERATED_KEYS`,
`getGeneratedKeys()` viene vacío y `claves.next()` da `false`.

**Ogro: ignorar el resultado de `executeUpdate`.** Un `UPDATE` de un id inexistente no
es un error para la base (cambia 0 filas): si importa, revisá el número y lanzá una
excepción.

**Troll: perder la causa.** Un `throw new DatosException("error")` sin la `SQLException`
original borra el mensaje real de PostgreSQL. Pasala como causa.

**Goblin: los `?` en otro orden.** Si el SQL es `SET nombre = ?, vida = ? WHERE id = ?`
y hacés `setInt(1, id)`, la base intenta guardar el id en el nombre.

### Misión R04-N06-M1 · El DAO de productos

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí el DAO completo de la tabla `producto` de `schema.sql`: un `record Producto`,
una interfaz `ProductoDAO` (listar, buscar por código, insertar, actualizar precio y
stock, eliminar) y su implementación con PostgreSQL, con excepciones propias. El código
es la clave primaria (texto), así que no hay id generado. En el `main`: insertá un
producto, modificá otro, borrá uno, intentá buscar uno que no existe e insertar uno con
precio negativo (la base lo rechaza por el `CHECK`), y listá todo con 2 decimales.

`schema.sql`

```sql
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (codigo VARCHAR(10) PRIMARY KEY, nombre VARCHAR(30) NOT NULL,
                       precio NUMERIC(10, 2) NOT NULL CHECK (precio > 0), stock INTEGER NOT NULL CHECK (stock >= 0));
INSERT INTO producto VALUES ('YER', 'Yerba 1 kg', 4200.5, 20), ('AZU', 'Azúcar 1 kg', 1350, 35), ('HAR', 'Harina 1 kg', 980, 0);
```

#### Criterio de aprobación

- Interfaz DAO + implementación; el `main` no tiene SQL.
- Las `SQLException` se traducen en excepciones propias con causa.

#### Salida esperada

```
Buscar YER: Producto[codigo=YER, nombre=Yerba 1 kg, precio=4200.50, stock=20]
No encontrado: no existe el producto XXX
Error: no se pudo insertar SAL (la base rechazó los datos)
ACE  Aceite 900 ml    2890.00   12
AZU  Azúcar 1 kg      1420.00   30
YER  Yerba 1 kg       4200.50   20
```

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (codigo VARCHAR(10) PRIMARY KEY, nombre VARCHAR(30) NOT NULL,
                       precio NUMERIC(10, 2) NOT NULL CHECK (precio > 0), stock INTEGER NOT NULL CHECK (stock >= 0));
INSERT INTO producto VALUES ('YER', 'Yerba 1 kg', 4200.5, 20), ('AZU', 'Azúcar 1 kg', 1350, 35), ('HAR', 'Harina 1 kg', 980, 0);
```

```java
// Mision 1 - El DAO de productos.
import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class Almacen {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        ProductoDAO dao = new ProductoDAOPostgres();
        try {
            dao.insertar(new Producto("ACE", "Aceite 900 ml", new BigDecimal("2890.00"), 12));
            dao.actualizar(new Producto("AZU", "Azúcar 1 kg", new BigDecimal("1420.00"), 30));
            dao.eliminar("HAR");
            System.out.println("Buscar YER: " + dao.buscar("YER"));
            dao.buscar("XXX");
        } catch (NoEncontradoException e) {
            System.out.println("No encontrado: " + e.getMessage());
        } catch (DatosException e) {
            System.out.println("Error: " + e.getMessage());
        }
        try {
            dao.insertar(new Producto("SAL", "Sal fina", new BigDecimal("-5"), 3));
        } catch (DatosException e) {
            System.out.println("Error: " + e.getMessage());
        }
        try {
            for (Producto p : dao.listar()) {
                System.out.printf("%-4s %-14s %9.2f %4d%n", p.codigo(), p.nombre(), p.precio(), p.stock());
            }
        } catch (DatosException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}

record Producto(String codigo, String nombre, BigDecimal precio, int stock) { }

class DatosException extends Exception {
    public DatosException(String mensaje, Throwable causa) {
        super(mensaje, causa);
    }
}

class NoEncontradoException extends DatosException {
    public NoEncontradoException(String mensaje) {
        super(mensaje, null);
    }
}

interface ProductoDAO {
    List<Producto> listar() throws DatosException;

    Producto buscar(String codigo) throws DatosException;

    void insertar(Producto p) throws DatosException;

    void actualizar(Producto p) throws DatosException;

    void eliminar(String codigo) throws DatosException;
}

class ProductoDAOPostgres implements ProductoDAO {
    @Override
    public List<Producto> listar() throws DatosException {
        List<Producto> lista = new ArrayList<>();
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("SELECT * FROM producto ORDER BY codigo");
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                lista.add(leer(rs));
            }
            return lista;
        } catch (SQLException e) {
            throw new DatosException("no se pudo listar", e);
        }
    }

    @Override
    public Producto buscar(String codigo) throws DatosException {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("SELECT * FROM producto WHERE codigo = ?")) {
            ps.setString(1, codigo);
            try (ResultSet rs = ps.executeQuery()) {
                if (!rs.next()) {
                    throw new NoEncontradoException("no existe el producto " + codigo);
                }
                return leer(rs);
            }
        } catch (SQLException e) {
            throw new DatosException("no se pudo buscar " + codigo, e);
        }
    }

    @Override
    public void insertar(Producto p) throws DatosException {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("INSERT INTO producto VALUES (?, ?, ?, ?)")) {
            ps.setString(1, p.codigo());
            ps.setString(2, p.nombre());
            ps.setBigDecimal(3, p.precio());
            ps.setInt(4, p.stock());
            ps.executeUpdate();
        } catch (SQLException e) {
            throw new DatosException("no se pudo insertar " + p.codigo() + " (la base rechazó los datos)", e);
        }
    }

    @Override
    public void actualizar(Producto p) throws DatosException {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("UPDATE producto SET nombre = ?, precio = ?, stock = ? WHERE codigo = ?")) {
            ps.setString(1, p.nombre());
            ps.setBigDecimal(2, p.precio());
            ps.setInt(3, p.stock());
            ps.setString(4, p.codigo());
            if (ps.executeUpdate() == 0) {
                throw new NoEncontradoException("no existe el producto " + p.codigo());
            }
        } catch (SQLException e) {
            throw new DatosException("no se pudo actualizar " + p.codigo(), e);
        }
    }

    @Override
    public void eliminar(String codigo) throws DatosException {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("DELETE FROM producto WHERE codigo = ?")) {
            ps.setString(1, codigo);
            if (ps.executeUpdate() == 0) {
                throw new NoEncontradoException("no existe el producto " + codigo);
            }
        } catch (SQLException e) {
            throw new DatosException("no se pudo eliminar " + codigo, e);
        }
    }

    private Producto leer(ResultSet rs) throws SQLException {
        return new Producto(rs.getString("codigo"), rs.getString("nombre"), rs.getBigDecimal("precio"), rs.getInt("stock"));
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Misión R04-N06-M2 · El bean de la cátedra

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

En la cátedra, cada fila se representa con un **bean**: una clase con atributos
privados, un constructor vacío y getters y setters. Escribí `AlumnoBean` (legajo,
nombre, carrera, promedio) y un `AlumnoDAO` con `listarPorCarrera(String carrera)` y
`insertar(AlumnoBean a)` (que le **carga** al bean el legajo generado con
`getGeneratedKeys` usando su setter). En el `main`, insertá dos alumnos, mostrá los
legajos generados y listá los de `Sistemas` ordenados por promedio de mayor a menor.

`schema.sql`

```sql
DROP TABLE IF EXISTS alumno;
CREATE TABLE alumno (legajo SERIAL PRIMARY KEY, nombre VARCHAR(30) NOT NULL, carrera VARCHAR(30) NOT NULL, promedio NUMERIC(4, 2));
INSERT INTO alumno (nombre, carrera, promedio) VALUES ('Kira Valdez', 'Sistemas', 8.5), ('Bron Tallo', 'Contador', 7.25);
```

#### Criterio de aprobación

- `AlumnoBean` tiene constructor vacío, atributos privados, getters y setters.
- El DAO usa `RETURN_GENERATED_KEYS` y carga el legajo en el bean.

#### Salida esperada

```
Legajos generados: 3 y 4
  3 Lía Ferrari   9.10
  1 Kira Valdez   8.50
  4 Pip Nuez      6.75
```

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS alumno;
CREATE TABLE alumno (legajo SERIAL PRIMARY KEY, nombre VARCHAR(30) NOT NULL, carrera VARCHAR(30) NOT NULL, promedio NUMERIC(4, 2));
INSERT INTO alumno (nombre, carrera, promedio) VALUES ('Kira Valdez', 'Sistemas', 8.5), ('Bron Tallo', 'Contador', 7.25);
```

```java
// Mision 2 - El bean de la catedra: AlumnoBean con getters/setters y un DAO con getGeneratedKeys.
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class Alumnos {
    public static void main(String[] args) throws SQLException {
        Locale.setDefault(Locale.US);
        AlumnoDAO dao = new AlumnoDAO();
        AlumnoBean a1 = new AlumnoBean();
        a1.setNombre("Lía Ferrari");
        a1.setCarrera("Sistemas");
        a1.setPromedio(9.1);
        AlumnoBean a2 = new AlumnoBean();
        a2.setNombre("Pip Nuez");
        a2.setCarrera("Sistemas");
        a2.setPromedio(6.75);
        dao.insertar(a1);
        dao.insertar(a2);
        System.out.println("Legajos generados: " + a1.getLegajo() + " y " + a2.getLegajo());
        for (AlumnoBean a : dao.listarPorCarrera("Sistemas")) {
            System.out.printf("%3d %-12s %5.2f%n", a.getLegajo(), a.getNombre(), a.getPromedio());
        }
    }
}

class AlumnoBean {
    private int legajo;
    private String nombre;
    private String carrera;
    private double promedio;

    public AlumnoBean() {
    }

    public int getLegajo() {
        return legajo;
    }

    public void setLegajo(int legajo) {
        this.legajo = legajo;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getCarrera() {
        return carrera;
    }

    public void setCarrera(String carrera) {
        this.carrera = carrera;
    }

    public double getPromedio() {
        return promedio;
    }

    public void setPromedio(double promedio) {
        this.promedio = promedio;
    }
}

class AlumnoDAO {
    public void insertar(AlumnoBean a) throws SQLException {
        String sql = "INSERT INTO alumno (nombre, carrera, promedio) VALUES (?, ?, ?)";
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, a.getNombre());
            ps.setString(2, a.getCarrera());
            ps.setDouble(3, a.getPromedio());
            ps.executeUpdate();
            try (ResultSet claves = ps.getGeneratedKeys()) {
                claves.next();
                a.setLegajo(claves.getInt(1));
            }
        }
    }

    public List<AlumnoBean> listarPorCarrera(String carrera) throws SQLException {
        List<AlumnoBean> lista = new ArrayList<>();
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("SELECT * FROM alumno WHERE carrera = ? ORDER BY promedio DESC")) {
            ps.setString(1, carrera);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    AlumnoBean a = new AlumnoBean();
                    a.setLegajo(rs.getInt("legajo"));
                    a.setNombre(rs.getString("nombre"));
                    a.setCarrera(rs.getString("carrera"));
                    a.setPromedio(rs.getDouble("promedio"));
                    lista.add(a);
                }
            }
        }
        return lista;
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Misión R04-N06-M3 · El DAO en memoria

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Una de las ventajas del DAO es poder cambiar dónde se guardan los datos. Escribí una
interfaz `TareaDAO` (listar, insertar devolviendo la tarea con su id, completar(id),
eliminar(id)) con **dos** implementaciones: `TareaDAOMemoria` (con un `TreeMap` y un
contador de ids) y `TareaDAOPostgres`. Escribí una clase `Planificador` que recibe un
`TareaDAO` en el constructor y tiene la lógica: agregar tres tareas, completar la
segunda y mostrar las pendientes. Corré el **mismo** `Planificador` con las dos
implementaciones y mostrá que dan el mismo resultado.

`schema.sql`

```sql
DROP TABLE IF EXISTS tarea;
CREATE TABLE tarea (id SERIAL PRIMARY KEY, descripcion VARCHAR(50) NOT NULL, hecha BOOLEAN NOT NULL DEFAULT FALSE);
```

#### Criterio de aprobación

- Dos implementaciones de la misma interfaz.
- `Planificador` solo conoce la interfaz.

#### Salida esperada

```
En memoria: [1:Afilar la espada, 3:Comprar pan]
En PostgreSQL: [1:Afilar la espada, 3:Comprar pan]
```

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS tarea;
CREATE TABLE tarea (id SERIAL PRIMARY KEY, descripcion VARCHAR(50) NOT NULL, hecha BOOLEAN NOT NULL DEFAULT FALSE);
```

```java
// Mision 3 - El DAO en memoria: la misma logica con dos formas de guardar.
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public class Planificacion {
    public static void main(String[] args) throws Exception {
        System.out.println("En memoria: " + new Planificador(new TareaDAOMemoria()).probar());
        System.out.println("En PostgreSQL: " + new Planificador(new TareaDAOPostgres()).probar());
    }
}

record Tarea(int id, String descripcion, boolean hecha) { }

interface TareaDAO {
    List<Tarea> listar() throws Exception;

    Tarea insertar(String descripcion) throws Exception;

    void completar(int id) throws Exception;

    void eliminar(int id) throws Exception;
}

class Planificador {
    private final TareaDAO dao;

    Planificador(TareaDAO dao) {
        this.dao = dao;
    }

    List<String> probar() throws Exception {
        dao.insertar("Afilar la espada");
        Tarea mapa = dao.insertar("Copiar el mapa");
        dao.insertar("Comprar pan");
        dao.completar(mapa.id());
        List<String> pendientes = new ArrayList<>();
        for (Tarea t : dao.listar()) {
            if (!t.hecha()) {
                pendientes.add(t.id() + ":" + t.descripcion());
            }
        }
        return pendientes;
    }
}

class TareaDAOMemoria implements TareaDAO {
    private final Map<Integer, Tarea> tareas = new TreeMap<>();
    private int ultimoId = 0;

    @Override
    public List<Tarea> listar() {
        return new ArrayList<>(tareas.values());
    }

    @Override
    public Tarea insertar(String descripcion) {
        ultimoId++;
        Tarea t = new Tarea(ultimoId, descripcion, false);
        tareas.put(ultimoId, t);
        return t;
    }

    @Override
    public void completar(int id) {
        Tarea t = tareas.get(id);
        if (t != null) {
            tareas.put(id, new Tarea(id, t.descripcion(), true));
        }
    }

    @Override
    public void eliminar(int id) {
        tareas.remove(id);
    }
}

class TareaDAOPostgres implements TareaDAO {
    @Override
    public List<Tarea> listar() throws SQLException {
        List<Tarea> lista = new ArrayList<>();
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("SELECT * FROM tarea ORDER BY id");
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                lista.add(new Tarea(rs.getInt("id"), rs.getString("descripcion"), rs.getBoolean("hecha")));
            }
        }
        return lista;
    }

    @Override
    public Tarea insertar(String descripcion) throws SQLException {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("INSERT INTO tarea (descripcion) VALUES (?)", Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, descripcion);
            ps.executeUpdate();
            try (ResultSet k = ps.getGeneratedKeys()) {
                k.next();
                return new Tarea(k.getInt(1), descripcion, false);
            }
        }
    }

    @Override
    public void completar(int id) throws SQLException {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("UPDATE tarea SET hecha = TRUE WHERE id = ?")) {
            ps.setInt(1, id);
            ps.executeUpdate();
        }
    }

    @Override
    public void eliminar(int id) throws SQLException {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("DELETE FROM tarea WHERE id = ?")) {
            ps.setInt(1, id);
            ps.executeUpdate();
        }
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Encargo R04-N06-E1 · El padrón de socios del club

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un club de barrio quiere un ABM de socios de consola contra PostgreSQL. Escribí el
`SocioDAO` (con `record Socio`) y un menú que procese comandos de la entrada hasta
`salir`: `alta NOMBRE;DNI;CATEGORIA`, `baja NUMERO`, `cuota NUMERO` (marca la cuota del
mes como paga), `morosos` (los que no pagaron) y `lista`. El DNI es único: si se repite,
la base lo rechaza y el programa lo informa. Los números de socio los genera la base.

`schema.sql`

```sql
DROP TABLE IF EXISTS socio;
CREATE TABLE socio (numero SERIAL PRIMARY KEY, nombre VARCHAR(40) NOT NULL, dni VARCHAR(8) NOT NULL UNIQUE,
                    categoria VARCHAR(20) NOT NULL, cuota_paga BOOLEAN NOT NULL DEFAULT FALSE);
```

#### Criterio de aprobación

- Todo el SQL está en el DAO.
- El DNI repetido se informa sin cortar el programa.

#### Entrada de ejemplo

```
alta Marta Díaz;30111222;activo
alta Juan Pérez;28999000;cadete
alta Ana Ruiz;30111222;activo
alta Leo Paz;40000001;vitalicio
cuota 1
cuota 3
baja 2
morosos
lista
salir
```

#### Salida esperada

```
Socio N° 1: Marta Díaz
Socio N° 2: Juan Pérez
Error: ese DNI ya está registrado
Socio N° 4: Leo Paz
Cuota paga: socio 1
No existe el socio 3
Baja del socio 2
Morosos: [Leo Paz]
  1 Marta Díaz (activo)
  4 Leo Paz (vitalicio) debe
```

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS socio;
CREATE TABLE socio (numero SERIAL PRIMARY KEY, nombre VARCHAR(40) NOT NULL, dni VARCHAR(8) NOT NULL UNIQUE,
                    categoria VARCHAR(20) NOT NULL, cuota_paga BOOLEAN NOT NULL DEFAULT FALSE);
```

```java
// Encargo - El padron de socios del club: un ABM de consola con DAO.
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Club {
    public static void main(String[] args) {
        SocioDAO dao = new SocioDAO();
        Scanner teclado = new Scanner(System.in);
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.equals("salir")) {
                break;
            }
            String[] p = linea.split(" ", 2);
            try {
                switch (p[0]) {
                    case "alta" -> {
                        String[] d = p[1].split(";");
                        Socio s = dao.alta(d[0], d[1], d[2]);
                        System.out.println("Socio N° " + s.numero() + ": " + s.nombre());
                    }
                    case "baja" -> System.out.println(dao.baja(Integer.parseInt(p[1])) ? "Baja del socio " + p[1] : "No existe el socio " + p[1]);
                    case "cuota" -> System.out.println(dao.pagarCuota(Integer.parseInt(p[1])) ? "Cuota paga: socio " + p[1] : "No existe el socio " + p[1]);
                    case "morosos" -> System.out.println("Morosos: " + nombres(dao.morosos()));
                    case "lista" -> dao.listar().forEach(s -> System.out.println("  " + s.numero() + " " + s.nombre() + " (" + s.categoria() + ")" + (s.cuotaPaga() ? "" : " debe")));
                    default -> System.out.println("Comando inválido");
                }
            } catch (SQLException e) {
                System.out.println("Error: " + ("23505".equals(e.getSQLState()) ? "ese DNI ya está registrado" : e.getMessage()));
            }
        }
    }

    static List<String> nombres(List<Socio> socios) {
        List<String> n = new ArrayList<>();
        socios.forEach(s -> n.add(s.nombre()));
        return n;
    }
}

record Socio(int numero, String nombre, String dni, String categoria, boolean cuotaPaga) { }

class SocioDAO {
    Socio alta(String nombre, String dni, String categoria) throws SQLException {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("INSERT INTO socio (nombre, dni, categoria) VALUES (?, ?, ?)", Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, nombre);
            ps.setString(2, dni);
            ps.setString(3, categoria);
            ps.executeUpdate();
            try (ResultSet k = ps.getGeneratedKeys()) {
                k.next();
                return new Socio(k.getInt(1), nombre, dni, categoria, false);
            }
        }
    }

    boolean baja(int numero) throws SQLException {
        return actualizar("DELETE FROM socio WHERE numero = ?", numero);
    }

    boolean pagarCuota(int numero) throws SQLException {
        return actualizar("UPDATE socio SET cuota_paga = TRUE WHERE numero = ?", numero);
    }

    List<Socio> morosos() throws SQLException {
        return consultar("SELECT * FROM socio WHERE NOT cuota_paga ORDER BY numero");
    }

    List<Socio> listar() throws SQLException {
        return consultar("SELECT * FROM socio ORDER BY numero");
    }

    private boolean actualizar(String sql, int numero) throws SQLException {
        try (Connection con = Conexion.abrir(); PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, numero);
            return ps.executeUpdate() > 0;
        }
    }

    private List<Socio> consultar(String sql) throws SQLException {
        List<Socio> lista = new ArrayList<>();
        try (Connection con = Conexion.abrir(); PreparedStatement ps = con.prepareStatement(sql); ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                lista.add(new Socio(rs.getInt("numero"), rs.getString("nombre"), rs.getString("dni"),
                        rs.getString("categoria"), rs.getBoolean("cuota_paga")));
            }
        }
        return lista;
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Prueba del sello

#### ¿Qué es un DAO?

Un objeto que concentra todo el acceso a datos de una tabla o entidad, detrás de una interfaz.

#### ¿Por qué el resto del programa usa la interfaz del DAO y no la implementación?

Para no depender del motor de base de datos: se puede cambiar la implementación (otra base, o una en memoria para pruebas) sin tocar el resto.

#### ¿Cómo se obtiene el id que generó la base en un `INSERT`?

Preparando la sentencia con `Statement.RETURN_GENERATED_KEYS` y leyendo `ps.getGeneratedKeys()`.

#### ¿Qué indica que `executeUpdate()` devuelva 0 en un `UPDATE`?

Que ninguna fila cumplía el `WHERE`: por ejemplo, el id no existía.

#### ¿Qué es un bean en el estilo de la cátedra?

Una clase con atributos privados, un constructor vacío y getters y setters, que representa una fila.

### Soluciones (docente)

Sale de `18-Java/31-JDBC-ABM-Transacciones` (unidad 5), la parte del ABM. Suma lo que pedía la auditoría: la capa DAO con el nombre que usa la cátedra, el bean y `getGeneratedKeys` (portable, en lugar del `RETURNING` de PostgreSQL). El SQLState `23505` es el de clave duplicada en cualquier motor que siga el estándar. En el encargo, el socio que falla por DNI repetido **consume** el número 3 de la secuencia: por eso el siguiente es el 4. Los `SERIAL` pueden tener huecos y no hay que usarlos como numeración correlativa sin saltos.

## R04-N07 · Transacciones y CallableStatement

```meta
tipo: tema
padre: R04-N06
precio: 10
criatura: troll
temas: sql.transacciones
usa: sql.desde-codigo
```

### Crónica

Un tesorero de la Bóveda está pasando cien denarios del cofre de Kira al de Bron. Saca el oro del primer cofre… y en ese momento se apaga la antorcha. Cuando vuelve la luz, el oro no está en ningún cofre: salió de uno y nunca llegó al otro.

—Hay operaciones que tienen que pasar **enteras o nada** —dice {mentor}—. Sacar de un cofre y poner en el otro es **una sola cosa**, aunque sean dos pasos. En la Bóveda eso se llama **transacción**, {heroe}, y es lo que evita que el oro se evapore.

### Objetivos

- Entender las transacciones y las propiedades ACID.
- Agrupar varias operaciones con `setAutoCommit(false)`, `commit` y `rollback`.
- Llamar procedimientos y funciones de la base con `CallableStatement`.
- Usar un punto de guardado (`Savepoint`).

### Antes de empezar

- DAO: el ABM completo desde Java.
- SQL: funciones, procedimientos, triggers y roles.

### Explicación

#### Qué es una transacción
Una **transacción** es un grupo de operaciones que la base trata como **una sola**: o
se aplican todas, o ninguna. Sus propiedades se resumen en **ACID**:
| Propiedad | Significa |
|---|---|
| **A**tomicidad | todo o nada |
| **C**onsistencia | la base pasa de un estado válido a otro válido (se cumplen las restricciones) |
| a**I**slamiento | las transacciones que corren al mismo tiempo no se ven los cambios a medio hacer |
| **D**urabilidad | lo confirmado queda guardado aunque se corte la luz |

#### El modo automático
Por defecto, JDBC está en **auto-commit**: cada `executeUpdate` se confirma solo, al
instante. Para agrupar operaciones, se apaga:
```java
try (Connection con = Conexion.abrir()) {
    con.setAutoCommit(false);                   // empieza la transacción
    try {
        retirar(con, "Kira", 100);
        depositar(con, "Bron", 100);
        con.commit();                           // confirma las dos
    } catch (SQLException e) {
        con.rollback();                         // deshace todo lo de esta transacción
        throw e;
    }
}
```
**Todas** las operaciones de la transacción tienen que usar **la misma conexión**: por
eso los métodos reciben la `Connection` como parámetro.

#### Cuándo hace falta
Siempre que una operación del negocio toca varias filas o tablas que tienen que quedar
coherentes: una transferencia, una venta que registra el ticket y descuenta el stock,
un alta de pedido con sus renglones, una inscripción que ocupa un cupo.

#### Puntos de guardado
Dentro de una transacción se puede marcar un punto y deshacer **solo** hasta ahí:
```java
Savepoint antes = con.setSavepoint();
try {
    registrarPuntosExtra(con, …);
} catch (SQLException e) {
    con.rollback(antes);          // se pierde solo lo posterior al punto
}
con.commit();
```

#### `CallableStatement`: procedimientos y funciones de la base
Para ejecutar un procedimiento almacenado:
```java
try (CallableStatement cs = con.prepareCall("CALL vender(?, ?)")) {
    cs.setInt(1, 3);
    cs.setInt(2, 2);
    cs.execute();
}
```
Para una función que devuelve un valor, se usa la sintaxis de escape de JDBC con un
parámetro de salida:
```java
try (CallableStatement cs = con.prepareCall("{? = call precio_final(?, ?)}")) {
    cs.registerOutParameter(1, Types.NUMERIC);
    cs.setBigDecimal(2, new BigDecimal("1200"));
    cs.setString(3, "oferta");
    cs.execute();
    BigDecimal resultado = cs.getBigDecimal(1);
}
```
(En PostgreSQL también se puede llamar a una función con un `SELECT precio_final(?, ?)`
común.) Si el procedimiento hace `RAISE EXCEPTION`, en Java llega una `SQLException`
con ese mensaje.

> **En la facultad.** La unidad 5 pide transacciones y `CallableStatement`; el caso
> práctico del final registra un acta con sus renglones, que es exactamente una
> transacción.

### Código de ejemplo

`schema.sql`

```sql
DROP TABLE IF EXISTS movimiento;
DROP TABLE IF EXISTS cofre;
CREATE TABLE cofre (duenio VARCHAR(20) PRIMARY KEY, oro INTEGER NOT NULL CHECK (oro >= 0));
CREATE TABLE movimiento (id SERIAL PRIMARY KEY, desde VARCHAR(20), hacia VARCHAR(20), monto INTEGER);
INSERT INTO cofre VALUES ('Kira', 150), ('Bron', 40);

CREATE OR REPLACE FUNCTION oro_de(p_duenio VARCHAR) RETURNS INTEGER AS $$
BEGIN
    RETURN (SELECT oro FROM cofre WHERE duenio = p_duenio);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE bonificar(p_duenio VARCHAR, p_monto INTEGER) AS $$
BEGIN
    UPDATE cofre SET oro = oro + p_monto WHERE duenio = p_duenio;
END;
$$ LANGUAGE plpgsql;
```

```java
/*
 * Transacciones: el oro no se evapora.
 */
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Types;

public class Tesoreria {
    public static void main(String[] args) throws SQLException {
        transferir("Kira", "Bron", 100);
        mostrar();
        transferir("Kira", "Bron", 100);          // Kira ya no tiene 100: el CHECK lo impide
        mostrar();

        try (Connection con = Conexion.abrir()) {
            // Un procedimiento con CallableStatement
            try (CallableStatement cs = con.prepareCall("CALL bonificar(?, ?)")) {
                cs.setString(1, "Kira");
                cs.setInt(2, 25);
                cs.execute();
            }
            // Una función con parámetro de salida
            try (CallableStatement cs = con.prepareCall("{? = call oro_de(?)}")) {
                cs.registerOutParameter(1, Types.INTEGER);
                cs.setString(2, "Kira");
                cs.execute();
                System.out.println("Oro de Kira después de la bonificación: " + cs.getInt(1));
            }
        }
    }

    static void transferir(String desde, String hacia, int monto) throws SQLException {
        try (Connection con = Conexion.abrir()) {
            con.setAutoCommit(false);
            try {
                mover(con, hacia, monto);                 // primero se deposita...
                mover(con, desde, -monto);                // ...y después se retira (puede fallar)
                try (PreparedStatement ps = con.prepareStatement("INSERT INTO movimiento (desde, hacia, monto) VALUES (?, ?, ?)")) {
                    ps.setString(1, desde);
                    ps.setString(2, hacia);
                    ps.setInt(3, monto);
                    ps.executeUpdate();
                }
                con.commit();
                System.out.println("Transferencia de " + monto + " de " + desde + " a " + hacia + ": confirmada");
            } catch (SQLException e) {
                con.rollback();
                System.out.println("Transferencia de " + monto + " de " + desde + " a " + hacia + ": deshecha (" + e.getSQLState() + ")");
            }
        }
    }

    static void mover(Connection con, String duenio, int monto) throws SQLException {
        try (PreparedStatement ps = con.prepareStatement("UPDATE cofre SET oro = oro + ? WHERE duenio = ?")) {
            ps.setInt(1, monto);
            ps.setString(2, duenio);
            ps.executeUpdate();
        }
    }

    static void mostrar() throws SQLException {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("SELECT duenio, oro FROM cofre ORDER BY duenio");
             ResultSet rs = ps.executeQuery()) {
            StringBuilder sb = new StringBuilder("  Cofres:");
            while (rs.next()) {
                sb.append(" ").append(rs.getString(1)).append("=").append(rs.getInt(2));
            }
            try (PreparedStatement ps2 = con.prepareStatement("SELECT COUNT(*) FROM movimiento"); ResultSet rs2 = ps2.executeQuery()) {
                rs2.next();
                sb.append(" | movimientos: ").append(rs2.getInt(1));
            }
            System.out.println(sb);
        }
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Salida esperada

```
Transferencia de 100 de Kira a Bron: confirmada
  Cofres: Bron=140 Kira=50 | movimientos: 1
Transferencia de 100 de Kira a Bron: deshecha (23514)
  Cofres: Bron=140 Kira=50 | movimientos: 1
Oro de Kira después de la bonificación: 75
```

### ¿Para qué sirve?

Toda operación de un banco, un comercio o un sistema de reservas que toca más de una fila es una transacción: sin ellas, un corte de luz o un error a mitad de camino deja datos imposibles (plata que desaparece, stock descontado sin venta, un acta sin sus notas). Los procedimientos almacenados permiten que esa lógica viva en la base y la usen varios programas a la vez.

### Errores habituales

**Troll: operaciones en conexiones distintas.** Si cada método abre su propia conexión,
cada uno tiene su propia transacción y el `rollback` no deshace lo que hicieron los
otros. Pasá la misma `Connection`.

**Ogro: olvidarse del `commit`.** Con auto-commit apagado, sin `commit` los cambios se
pierden al cerrar la conexión.

**Ogro: el `rollback` que falta en el `catch`.** Si una operación falla y no deshacés,
lo que se hizo antes queda pendiente en la conexión.

**Esqueleto: llamar un procedimiento como función.** `{? = call vender(?, ?)}` con un
`PROCEDURE` falla: los procedimientos se llaman con `CALL vender(?, ?)`.

**Goblin: el tipo del parámetro de salida.** `registerOutParameter` tiene que indicar el
tipo que devuelve la función (`Types.INTEGER`, `Types.NUMERIC`, `Types.VARCHAR`).

### Misión R04-N07-M1 · La venta con renglones

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Registrá una venta con varios renglones **en una transacción**: insertar el ticket
(obteniendo su id), insertar cada renglón y descontar el stock de cada producto. Si
algún producto no tiene stock suficiente, el `CHECK (stock >= 0)` hace fallar el
`UPDATE` y **toda** la venta se deshace (incluido el ticket). Probá dos ventas: una
que se puede hacer y otra donde el último renglón no tiene stock. Mostrá al final los
tickets, los renglones y el stock.

`schema.sql`

```sql
DROP TABLE IF EXISTS renglon;
DROP TABLE IF EXISTS ticket;
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (codigo VARCHAR(5) PRIMARY KEY, stock INTEGER NOT NULL CHECK (stock >= 0));
CREATE TABLE ticket (id SERIAL PRIMARY KEY, cliente VARCHAR(20) NOT NULL);
CREATE TABLE renglon (id SERIAL PRIMARY KEY, ticket_id INTEGER REFERENCES ticket(id), codigo VARCHAR(5) REFERENCES producto(codigo), cantidad INTEGER);
INSERT INTO producto VALUES ('PAN', 10), ('CAF', 4), ('GUI', 2);
```

#### Criterio de aprobación

- Toda la venta usa una conexión con `setAutoCommit(false)`, `commit` y `rollback`.
- La venta fallida no deja ni el ticket ni los renglones.

#### Salida esperada

```
Venta a Kira: registrada
Venta a Bron: cancelada, falta stock
[1 Kira]
[1 PAN 3] [1 CAF 2]
[CAF 2] [GUI 2] [PAN 7]
```

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS renglon;
DROP TABLE IF EXISTS ticket;
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (codigo VARCHAR(5) PRIMARY KEY, stock INTEGER NOT NULL CHECK (stock >= 0));
CREATE TABLE ticket (id SERIAL PRIMARY KEY, cliente VARCHAR(20) NOT NULL);
CREATE TABLE renglon (id SERIAL PRIMARY KEY, ticket_id INTEGER REFERENCES ticket(id), codigo VARCHAR(5) REFERENCES producto(codigo), cantidad INTEGER);
INSERT INTO producto VALUES ('PAN', 10), ('CAF', 4), ('GUI', 2);
```

```java
// Mision 1 - La venta con renglones: todo o nada.
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class VentaRenglones {
    public static void main(String[] args) throws SQLException {
        vender("Kira", new String[]{"PAN", "CAF"}, new int[]{3, 2});
        vender("Bron", new String[]{"PAN", "GUI"}, new int[]{2, 5});
        mostrar("SELECT id, cliente FROM ticket ORDER BY id");
        mostrar("SELECT ticket_id, codigo, cantidad FROM renglon ORDER BY id");
        mostrar("SELECT codigo, stock FROM producto ORDER BY codigo");
    }

    static void vender(String cliente, String[] codigos, int[] cantidades) throws SQLException {
        try (Connection con = Conexion.abrir()) {
            con.setAutoCommit(false);
            try {
                int ticket;
                try (PreparedStatement ps = con.prepareStatement("INSERT INTO ticket (cliente) VALUES (?)", Statement.RETURN_GENERATED_KEYS)) {
                    ps.setString(1, cliente);
                    ps.executeUpdate();
                    try (ResultSet k = ps.getGeneratedKeys()) {
                        k.next();
                        ticket = k.getInt(1);
                    }
                }
                for (int i = 0; i < codigos.length; i++) {
                    try (PreparedStatement ps = con.prepareStatement("INSERT INTO renglon (ticket_id, codigo, cantidad) VALUES (?, ?, ?)")) {
                        ps.setInt(1, ticket);
                        ps.setString(2, codigos[i]);
                        ps.setInt(3, cantidades[i]);
                        ps.executeUpdate();
                    }
                    try (PreparedStatement ps = con.prepareStatement("UPDATE producto SET stock = stock - ? WHERE codigo = ?")) {
                        ps.setInt(1, cantidades[i]);
                        ps.setString(2, codigos[i]);
                        ps.executeUpdate();
                    }
                }
                con.commit();
                System.out.println("Venta a " + cliente + ": registrada");
            } catch (SQLException e) {
                con.rollback();
                System.out.println("Venta a " + cliente + ": cancelada, falta stock");
            }
        }
    }

    static void mostrar(String sql) throws SQLException {
        try (Connection con = Conexion.abrir(); PreparedStatement ps = con.prepareStatement(sql); ResultSet rs = ps.executeQuery()) {
            StringBuilder sb = new StringBuilder();
            while (rs.next()) {
                sb.append("[");
                for (int i = 1; i <= rs.getMetaData().getColumnCount(); i++) {
                    sb.append(i > 1 ? " " : "").append(rs.getString(i));
                }
                sb.append("] ");
            }
            System.out.println(sb.toString().trim());
        }
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Misión R04-N07-M2 · El procedimiento desde Java

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La base ya tiene el procedimiento `inscribir(p_alumno, p_curso)` (que valida el cupo
y lanza un error si está lleno) y la función `cupo_libre(p_curso)`. Desde Java, con
`CallableStatement`: mostrá el cupo libre del curso 1, inscribí a cuatro alumnos (el
último no entra), mostrando el resultado de cada intento con el mensaje del error de la
base, y volvé a mostrar el cupo.

`schema.sql`

```sql
DROP TABLE IF EXISTS inscripcion;
DROP TABLE IF EXISTS curso;
CREATE TABLE curso (id INTEGER PRIMARY KEY, nombre VARCHAR(30), cupo INTEGER NOT NULL);
CREATE TABLE inscripcion (id SERIAL PRIMARY KEY, alumno VARCHAR(20), curso_id INTEGER REFERENCES curso(id));
INSERT INTO curso VALUES (1, 'Java desde cero', 3);

CREATE OR REPLACE FUNCTION cupo_libre(p_curso INTEGER) RETURNS INTEGER AS $$
BEGIN
    RETURN (SELECT cupo FROM curso WHERE id = p_curso) - (SELECT COUNT(*) FROM inscripcion WHERE curso_id = p_curso);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE inscribir(p_alumno VARCHAR, p_curso INTEGER) AS $$
BEGIN
    IF cupo_libre(p_curso) <= 0 THEN
        RAISE EXCEPTION 'no hay cupo en el curso %', p_curso;
    END IF;
    INSERT INTO inscripcion (alumno, curso_id) VALUES (p_alumno, p_curso);
END;
$$ LANGUAGE plpgsql;
```

#### Criterio de aprobación

- Llama al procedimiento con `CALL` y a la función con `{? = call …}` y `registerOutParameter`.
- Muestra el mensaje del `RAISE EXCEPTION`.

#### Salida esperada

```
Cupo libre: 3
Kira: inscripto
Bron: inscripto
Lía: inscripto
Pip: rechazado (no hay cupo en el curso 1)
Cupo libre: 0
```

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS inscripcion;
DROP TABLE IF EXISTS curso;
CREATE TABLE curso (id INTEGER PRIMARY KEY, nombre VARCHAR(30), cupo INTEGER NOT NULL);
CREATE TABLE inscripcion (id SERIAL PRIMARY KEY, alumno VARCHAR(20), curso_id INTEGER REFERENCES curso(id));
INSERT INTO curso VALUES (1, 'Java desde cero', 3);

CREATE OR REPLACE FUNCTION cupo_libre(p_curso INTEGER) RETURNS INTEGER AS $$
BEGIN
    RETURN (SELECT cupo FROM curso WHERE id = p_curso) - (SELECT COUNT(*) FROM inscripcion WHERE curso_id = p_curso);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE inscribir(p_alumno VARCHAR, p_curso INTEGER) AS $$
BEGIN
    IF cupo_libre(p_curso) <= 0 THEN
        RAISE EXCEPTION 'no hay cupo en el curso %', p_curso;
    END IF;
    INSERT INTO inscripcion (alumno, curso_id) VALUES (p_alumno, p_curso);
END;
$$ LANGUAGE plpgsql;
```

```java
// Mision 2 - El procedimiento desde Java: CallableStatement con CALL y con {? = call ...}.
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Types;

public class Inscripciones {
    public static void main(String[] args) throws SQLException {
        try (Connection con = Conexion.abrir()) {
            System.out.println("Cupo libre: " + cupoLibre(con, 1));
            for (String alumno : new String[]{"Kira", "Bron", "Lía", "Pip"}) {
                try (CallableStatement cs = con.prepareCall("CALL inscribir(?, ?)")) {
                    cs.setString(1, alumno);
                    cs.setInt(2, 1);
                    cs.execute();
                    System.out.println(alumno + ": inscripto");
                } catch (SQLException e) {
                    String mensaje = e.getMessage().split("\n")[0].replace("ERROR: ", "");
                    System.out.println(alumno + ": rechazado (" + mensaje + ")");
                }
            }
            System.out.println("Cupo libre: " + cupoLibre(con, 1));
        }
    }

    static int cupoLibre(Connection con, int curso) throws SQLException {
        try (CallableStatement cs = con.prepareCall("{? = call cupo_libre(?)}")) {
            cs.registerOutParameter(1, Types.INTEGER);
            cs.setInt(2, curso);
            cs.execute();
            return cs.getInt(1);
        }
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Misión R04-N07-M3 · El punto de guardado

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Al cerrar una partida del Arcade se hacen tres cosas en una transacción: guardar la
partida, sumarle los puntos al jugador y, **si se puede**, darle una medalla (la
tabla `medalla` no permite dos medallas iguales para el mismo jugador). Si la medalla
falla, **no** hay que perder la partida ni los puntos: usá un `Savepoint` antes de la
medalla y deshacé solo hasta ahí. Cerrá dos partidas de Kira que ganan la misma medalla
y mostrá el estado final.

`schema.sql`

```sql
DROP TABLE IF EXISTS medalla;
DROP TABLE IF EXISTS partida;
DROP TABLE IF EXISTS jugador;
CREATE TABLE jugador (nombre VARCHAR(20) PRIMARY KEY, puntos INTEGER NOT NULL DEFAULT 0);
CREATE TABLE partida (id SERIAL PRIMARY KEY, jugador VARCHAR(20) REFERENCES jugador(nombre), puntos INTEGER);
CREATE TABLE medalla (jugador VARCHAR(20) REFERENCES jugador(nombre), nombre VARCHAR(30), PRIMARY KEY (jugador, nombre));
INSERT INTO jugador (nombre) VALUES ('Kira');
```

#### Criterio de aprobación

- Usa `setSavepoint` y `rollback(savepoint)`.
- La segunda partida se guarda aunque la medalla repetida falle.

#### Salida esperada

```
Partida de 1200 guardada con medalla
Partida de 800 guardada (la medalla ya la tenía)
Puntos de Kira: 2000
Partidas: 2
Medallas: 1
```

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS medalla;
DROP TABLE IF EXISTS partida;
DROP TABLE IF EXISTS jugador;
CREATE TABLE jugador (nombre VARCHAR(20) PRIMARY KEY, puntos INTEGER NOT NULL DEFAULT 0);
CREATE TABLE partida (id SERIAL PRIMARY KEY, jugador VARCHAR(20) REFERENCES jugador(nombre), puntos INTEGER);
CREATE TABLE medalla (jugador VARCHAR(20) REFERENCES jugador(nombre), nombre VARCHAR(30), PRIMARY KEY (jugador, nombre));
INSERT INTO jugador (nombre) VALUES ('Kira');
```

```java
// Mision 3 - El punto de guardado: deshacer solo una parte de la transaccion.
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Savepoint;

public class CierrePartida {
    public static void main(String[] args) throws SQLException {
        cerrar("Kira", 1200, "Primera victoria");
        cerrar("Kira", 800, "Primera victoria");
        try (Connection con = Conexion.abrir()) {
            System.out.println("Puntos de Kira: " + uno(con, "SELECT puntos FROM jugador WHERE nombre = 'Kira'"));
            System.out.println("Partidas: " + uno(con, "SELECT COUNT(*) FROM partida"));
            System.out.println("Medallas: " + uno(con, "SELECT COUNT(*) FROM medalla"));
        }
    }

    static void cerrar(String jugador, int puntos, String medalla) throws SQLException {
        try (Connection con = Conexion.abrir()) {
            con.setAutoCommit(false);
            try {
                ejecutar(con, "INSERT INTO partida (jugador, puntos) VALUES (?, ?)", jugador, puntos);
                ejecutar(con, "UPDATE jugador SET puntos = puntos + ? WHERE nombre = ?", puntos, jugador);
                Savepoint antesDeLaMedalla = con.setSavepoint();
                try {
                    ejecutar(con, "INSERT INTO medalla (jugador, nombre) VALUES (?, ?)", jugador, medalla);
                    System.out.println("Partida de " + puntos + " guardada con medalla");
                } catch (SQLException e) {
                    con.rollback(antesDeLaMedalla);
                    System.out.println("Partida de " + puntos + " guardada (la medalla ya la tenía)");
                }
                con.commit();
            } catch (SQLException e) {
                con.rollback();
                System.out.println("No se pudo cerrar la partida");
            }
        }
    }

    static void ejecutar(Connection con, String sql, Object... valores) throws SQLException {
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            for (int i = 0; i < valores.length; i++) {
                ps.setObject(i + 1, valores[i]);
            }
            ps.executeUpdate();
        }
    }

    static int uno(Connection con, String sql) throws SQLException {
        try (PreparedStatement ps = con.prepareStatement(sql); ResultSet rs = ps.executeQuery()) {
            rs.next();
            return rs.getInt(1);
        }
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Encargo R04-N07-E1 · La reserva de butacas

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un cine permite reservar **varias butacas juntas** para una función. La reserva es
todo o nada: si alguna butaca ya está ocupada (la clave primaria `(funcion, butaca)`
lo impide), no se reserva ninguna. Procesá los pedidos de la entrada (`CLIENTE;BUTACA1,BUTACA2,…`)
hasta una línea vacía, cada uno en su transacción, y al final mostrá el mapa de la
sala (10 butacas, `A1` a `A10`, con `X` las ocupadas y `.` las libres).

`schema.sql`

```sql
DROP TABLE IF EXISTS reserva;
CREATE TABLE reserva (funcion INTEGER, butaca VARCHAR(4), cliente VARCHAR(20) NOT NULL, PRIMARY KEY (funcion, butaca));
```

#### Criterio de aprobación

- Cada pedido es una transacción; un pedido con una butaca ocupada no reserva ninguna.
- El mapa final refleja solo las reservas confirmadas.

#### Entrada de ejemplo

```
Kira;A1,A2
Bron;A5,A6,A7
Lía;A7,A8
Pip;A3,A4

```

#### Salida esperada

```
Kira: reservó A1, A2
Bron: reservó A5, A6, A7
Lía: alguna butaca ya estaba ocupada, no se reservó nada
Pip: reservó A3, A4
Sala: XXXXXXX...
```

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS reserva;
CREATE TABLE reserva (funcion INTEGER, butaca VARCHAR(4), cliente VARCHAR(20) NOT NULL, PRIMARY KEY (funcion, butaca));
```

```java
// Encargo - La reserva de butacas: cada pedido es una transaccion.
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;

public class Cine {
    static final int FUNCION = 1;

    public static void main(String[] args) throws SQLException {
        Scanner teclado = new Scanner(System.in);
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.isEmpty()) {
                break;
            }
            String[] p = linea.split(";");
            reservar(p[0], p[1].split(","));
        }
        Set<String> ocupadas = new HashSet<>();
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("SELECT butaca FROM reserva WHERE funcion = ?")) {
            ps.setInt(1, FUNCION);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    ocupadas.add(rs.getString(1));
                }
            }
        }
        StringBuilder mapa = new StringBuilder("Sala: ");
        for (int i = 1; i <= 10; i++) {
            mapa.append(ocupadas.contains("A" + i) ? "X" : ".");
        }
        System.out.println(mapa);
    }

    static void reservar(String cliente, String[] butacas) throws SQLException {
        try (Connection con = Conexion.abrir()) {
            con.setAutoCommit(false);
            try (PreparedStatement ps = con.prepareStatement("INSERT INTO reserva (funcion, butaca, cliente) VALUES (?, ?, ?)")) {
                for (String b : butacas) {
                    ps.setInt(1, FUNCION);
                    ps.setString(2, b);
                    ps.setString(3, cliente);
                    ps.executeUpdate();
                }
                con.commit();
                System.out.println(cliente + ": reservó " + String.join(", ", butacas));
            } catch (SQLException e) {
                con.rollback();
                System.out.println(cliente + ": alguna butaca ya estaba ocupada, no se reservó nada");
            }
        }
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Prueba del sello

#### ¿Qué significa la A de ACID?

Atomicidad: las operaciones de la transacción se aplican todas o ninguna.

#### ¿Qué hace `con.setAutoCommit(false)`?

Apaga la confirmación automática: los cambios quedan pendientes hasta `commit()` o se deshacen con `rollback()`.

#### ¿Por qué todas las operaciones de una transacción tienen que usar la misma conexión?

Porque la transacción pertenece a la conexión: operaciones en otra conexión no se confirman ni se deshacen juntas.

#### ¿Para qué sirve un `Savepoint`?

Para deshacer solo una parte de la transacción, hasta ese punto, sin perder lo anterior.

#### ¿Cómo se llama a una función de la base que devuelve un valor con `CallableStatement`?

Con `prepareCall("{? = call nombre(?)}")`, registrando el primer parámetro con `registerOutParameter`.

### Soluciones (docente)

Sale de `18-Java/31-JDBC-ABM-Transacciones` y del 32 por crear (unidad 5): transacciones ACID y `CallableStatement`, que el original nunca llamaba desde Java. En el ejemplo, la segunda transferencia deposita primero y falla al retirar: así se ve que el `rollback` deshace también el depósito.

## R04-N08 · Jefe: el Liche de las Tablas Huérfanas

```meta
tipo: jefe
padre: R04-N07
precio: 10
criatura: dragon
insignia: Sello del Liche
insignia_descripcion: Venciste al Liche de las Tablas Huérfanas: tus datos quedan siempre coherentes.
usa: sql.joins, sql.transacciones, diseno.capas
```

### Crónica

En el último piso de la Bóveda, entre tablas polvorientas, vive el **Liche**: un hechicero que se alimenta de datos rotos. Pedidos sin cliente, renglones de facturas que ya no existen, stock negativo, pagos a medio registrar. Cada fila huérfana lo hace más fuerte.

—No se lo vence borrando lo que está mal —dice {mentor}—. Se lo vence construyendo un sistema donde **nada pueda quedar mal**: restricciones en la base, un DAO por tabla, transacciones para todo lo que va junto y consultas que digan la verdad. Esta es la prueba de toda la Bóveda, {heroe}.

### Objetivos

- Diseñar un esquema completo con restricciones que protejan la coherencia.
- Integrar DAO, transacciones, procedimientos y consultas con `JOIN` y agregados.
- Escribir un sistema de consola que procese comandos contra la base sin dejar datos rotos.

### Antes de empezar

- Toda la rama: archivos, SQL (tablas, consultas, procedimientos), JDBC, DAO y transacciones.

### Explicación

#### Las capas del sistema
Un sistema con base de datos bien armado tiene capas:
1. **La base**: tablas con claves foráneas y `CHECK` que impiden los datos imposibles.
2. **Los DAO**: todo el SQL de cada tabla, con excepciones propias.
3. **Los servicios**: las operaciones del negocio (vender, anular una venta) que usan
   varios DAO en **una transacción**, pasándoles la misma conexión.
4. **La interfaz**: el menú de consola (o, en la próxima rama, las ventanas), que no
   sabe nada de SQL.

#### Un DAO que participa de una transacción
Para que varios DAO trabajen en la misma transacción, sus métodos reciben la
`Connection` en lugar de abrir una propia:
```java
class StockDAO {
    void descontar(Connection con, String codigo, int cantidad) throws SQLException { … }
}
class VentaService {
    void vender(…) throws VentaException {
        try (Connection con = Conexion.abrir()) {
            con.setAutoCommit(false);
            try {
                int id = ventaDAO.insertar(con, cliente);
                for (…) {
                    renglonDAO.insertar(con, id, codigo, cantidad);
                    stockDAO.descontar(con, codigo, cantidad);
                }
                con.commit();
            } catch (SQLException e) {
                con.rollback();
                throw new VentaException("no se pudo registrar la venta", e);
            }
        }
    }
}
```

### Código de ejemplo

`schema.sql`

```sql
DROP TABLE IF EXISTS renglon;
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS cliente;
DROP TABLE IF EXISTS producto;
CREATE TABLE cliente (id SERIAL PRIMARY KEY, nombre VARCHAR(30) NOT NULL UNIQUE);
CREATE TABLE producto (codigo VARCHAR(5) PRIMARY KEY, nombre VARCHAR(30) NOT NULL, precio NUMERIC(10, 2) NOT NULL CHECK (precio > 0),
                       stock INTEGER NOT NULL CHECK (stock >= 0));
CREATE TABLE pedido (id SERIAL PRIMARY KEY, cliente_id INTEGER NOT NULL REFERENCES cliente(id), anulado BOOLEAN NOT NULL DEFAULT FALSE);
CREATE TABLE renglon (pedido_id INTEGER NOT NULL REFERENCES pedido(id) ON DELETE CASCADE,
                      codigo VARCHAR(5) NOT NULL REFERENCES producto(codigo), cantidad INTEGER NOT NULL CHECK (cantidad > 0),
                      precio NUMERIC(10, 2) NOT NULL, PRIMARY KEY (pedido_id, codigo));
INSERT INTO cliente (nombre) VALUES ('Posada La Taza'), ('Guardia Real');
INSERT INTO producto VALUES ('PAN', 'Pan', 1200, 50), ('CAF', 'Café', 450, 20), ('ESP', 'Espada', 85000, 2);
```

```java
/*
 * Jefe de la rama 4: un servicio de pedidos en capas (DAO + transacción).
 */
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

public class PedidosEnCapas {
    public static void main(String[] args) throws SQLException {
        Locale.setDefault(Locale.US);
        PedidoService servicio = new PedidoService();
        Map<String, Integer> p1 = new LinkedHashMap<>();
        p1.put("PAN", 10);
        p1.put("CAF", 5);
        Map<String, Integer> p2 = new LinkedHashMap<>();
        p2.put("PAN", 3);
        p2.put("ESP", 3);                 // hay solo 2 espadas
        for (Map<String, Integer> p : List.of(p1, p2)) {
            try {
                int id = servicio.crear(1, p);
                System.out.println("Pedido " + id + " registrado");
            } catch (PedidoException e) {
                System.out.println("Pedido rechazado: " + e.getMessage());
            }
        }
        servicio.informe();
    }
}

class PedidoException extends Exception {
    public PedidoException(String mensaje, Throwable causa) {
        super(mensaje, causa);
    }
}

class PedidoDAO {
    int insertar(Connection con, int clienteId) throws SQLException {
        try (PreparedStatement ps = con.prepareStatement("INSERT INTO pedido (cliente_id) VALUES (?)", Statement.RETURN_GENERATED_KEYS)) {
            ps.setInt(1, clienteId);
            ps.executeUpdate();
            try (ResultSet k = ps.getGeneratedKeys()) {
                k.next();
                return k.getInt(1);
            }
        }
    }
}

class RenglonDAO {
    void insertar(Connection con, int pedido, String codigo, int cantidad) throws SQLException {
        String sql = "INSERT INTO renglon (pedido_id, codigo, cantidad, precio) SELECT ?, codigo, ?, precio FROM producto WHERE codigo = ?";
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, pedido);
            ps.setInt(2, cantidad);
            ps.setString(3, codigo);
            if (ps.executeUpdate() == 0) {
                throw new SQLException("no existe el producto " + codigo);
            }
        }
    }
}

class StockDAO {
    void descontar(Connection con, String codigo, int cantidad) throws SQLException {
        try (PreparedStatement ps = con.prepareStatement("UPDATE producto SET stock = stock - ? WHERE codigo = ?")) {
            ps.setInt(1, cantidad);
            ps.setString(2, codigo);
            ps.executeUpdate();
        }
    }
}

class PedidoService {
    private final PedidoDAO pedidos = new PedidoDAO();
    private final RenglonDAO renglones = new RenglonDAO();
    private final StockDAO stock = new StockDAO();

    int crear(int clienteId, Map<String, Integer> items) throws PedidoException, SQLException {
        try (Connection con = Conexion.abrir()) {
            con.setAutoCommit(false);
            try {
                int id = pedidos.insertar(con, clienteId);
                for (Map.Entry<String, Integer> e : items.entrySet()) {
                    renglones.insertar(con, id, e.getKey(), e.getValue());
                    stock.descontar(con, e.getKey(), e.getValue());
                }
                con.commit();
                return id;
            } catch (SQLException e) {
                con.rollback();
                throw new PedidoException("sin stock suficiente o datos inválidos", e);
            }
        }
    }

    void informe() throws SQLException {
        String sql = "SELECT c.nombre, COUNT(DISTINCT p.id) AS pedidos, COALESCE(SUM(r.cantidad * r.precio), 0) AS total "
                + "FROM cliente c LEFT JOIN pedido p ON p.cliente_id = c.id LEFT JOIN renglon r ON r.pedido_id = p.id "
                + "GROUP BY c.nombre ORDER BY c.nombre";
        try (Connection con = Conexion.abrir(); PreparedStatement ps = con.prepareStatement(sql); ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                System.out.printf("%-15s pedidos: %d  total: %.2f%n", rs.getString(1), rs.getInt(2), rs.getDouble(3));
            }
        }
        try (Connection con = Conexion.abrir(); PreparedStatement ps = con.prepareStatement("SELECT codigo, stock FROM producto ORDER BY codigo");
             ResultSet rs = ps.executeQuery()) {
            StringBuilder sb = new StringBuilder("Stock:");
            while (rs.next()) {
                sb.append(" ").append(rs.getString(1)).append("=").append(rs.getInt(2));
            }
            System.out.println(sb);
        }
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Salida esperada

```
Pedido 1 registrado
Pedido rechazado: sin stock suficiente o datos inválidos
Guardia Real    pedidos: 0  total: 0.00
Posada La Taza  pedidos: 1  total: 14250.00
Stock: CAF=15 ESP=2 PAN=40
```

### ¿Para qué sirve?

Esta es la estructura de cualquier sistema de gestión real: la base protege los datos, los DAO esconden el SQL, los servicios aseguran que cada operación del negocio sea todo o nada, y la interfaz solo muestra. Es exactamente lo que vas a conectar con ventanas en la próxima rama, y lo que pide el caso práctico de la cátedra.

### Errores habituales

**Dragón: la lógica del negocio en el menú.** Si el `main` descuenta stock y arma SQL,
cada pantalla nueva va a repetir (y equivocar) esa lógica. Va en un servicio.

**Troll: un DAO que abre su propia conexión dentro de una transacción.** Rompe la
transacción: lo que haga no se deshace con el `rollback`. En operaciones compuestas, el
DAO recibe la conexión.

**Ogro: confiar solo en Java.** Si la regla "el stock no puede ser negativo" está solo
en Java, cualquier otro programa (o un `UPDATE` a mano) la rompe. Ponela también como
`CHECK` en la base.

**Ogro: el informe que miente.** Un `INNER JOIN` en un informe esconde a los clientes
sin pedidos. Pensá si hace falta `LEFT JOIN` y `COALESCE`.

### Misión R04-N08-M1 · El sistema del almacén imperial

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Programá el sistema del almacén con el esquema de `schema.sql`, en capas (DAO +
servicio con transacciones), procesando comandos hasta `salir`:

- `vender CLIENTE_ID CODIGO:CANT,CODIGO:CANT…` — registra un pedido en una
  transacción (pedido, renglones con el precio del momento y descuento de stock). Si
  algo falla, no queda nada.
- `anular PEDIDO_ID` — anula un pedido **y devuelve el stock** en una transacción; un
  pedido ya anulado no se puede anular dos veces.
- `stock` — muestra el stock de cada producto.
- `informe` — por cliente: pedidos **no anulados** y total facturado (con los clientes
  sin pedidos en 0).

Informá cada resultado con un mensaje; los errores no cortan el programa.

`schema.sql`

```sql
DROP TABLE IF EXISTS renglon;
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS cliente;
DROP TABLE IF EXISTS producto;
CREATE TABLE cliente (id SERIAL PRIMARY KEY, nombre VARCHAR(30) NOT NULL UNIQUE);
CREATE TABLE producto (codigo VARCHAR(5) PRIMARY KEY, nombre VARCHAR(30) NOT NULL, precio NUMERIC(10, 2) NOT NULL CHECK (precio > 0),
                       stock INTEGER NOT NULL CHECK (stock >= 0));
CREATE TABLE pedido (id SERIAL PRIMARY KEY, cliente_id INTEGER NOT NULL REFERENCES cliente(id), anulado BOOLEAN NOT NULL DEFAULT FALSE);
CREATE TABLE renglon (pedido_id INTEGER NOT NULL REFERENCES pedido(id) ON DELETE CASCADE,
                      codigo VARCHAR(5) NOT NULL REFERENCES producto(codigo), cantidad INTEGER NOT NULL CHECK (cantidad > 0),
                      precio NUMERIC(10, 2) NOT NULL, PRIMARY KEY (pedido_id, codigo));
INSERT INTO cliente (nombre) VALUES ('Posada La Taza'), ('Guardia Real'), ('Herrería Ferrum');
INSERT INTO producto VALUES ('PAN', 'Pan', 1200, 50), ('CAF', 'Café', 450, 20), ('ESP', 'Espada', 85000, 2), ('ESC', 'Escudo', 41000, 5);
```

#### Criterio de aprobación

- Capas separadas: DAO (reciben la conexión), servicio (transacciones) y menú.
- `vender` y `anular` son transacciones completas.
- El informe excluye los pedidos anulados e incluye a los clientes sin pedidos.
- La salida coincide con la esperada.

#### Entrada de ejemplo

```
vender 1 PAN:10,CAF:4
vender 2 ESP:2,ESC:3
vender 2 ESP:1
vender 1 PAN:5,XXX:1
stock
anular 1
anular 1
vender 3 CAF:20
informe
stock
salir
```

#### Salida esperada

```
Pedido 1 registrado
Pedido 2 registrado
Rechazado: sin stock suficiente o cliente inexistente
Rechazado: no existe el producto XXX
Stock: CAF=16 ESC=2 ESP=0 PAN=40
Pedido 1 anulado, stock devuelto
Rechazado: el pedido 1 ya estaba anulado
Pedido 5 registrado
Guardia Real     pedidos: 1  total: 293000.00
Herrería Ferrum  pedidos: 1  total: 9000.00
Posada La Taza   pedidos: 0  total: 0.00
Stock: CAF=0 ESC=2 ESP=0 PAN=50
```

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS renglon;
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS cliente;
DROP TABLE IF EXISTS producto;
CREATE TABLE cliente (id SERIAL PRIMARY KEY, nombre VARCHAR(30) NOT NULL UNIQUE);
CREATE TABLE producto (codigo VARCHAR(5) PRIMARY KEY, nombre VARCHAR(30) NOT NULL, precio NUMERIC(10, 2) NOT NULL CHECK (precio > 0),
                       stock INTEGER NOT NULL CHECK (stock >= 0));
CREATE TABLE pedido (id SERIAL PRIMARY KEY, cliente_id INTEGER NOT NULL REFERENCES cliente(id), anulado BOOLEAN NOT NULL DEFAULT FALSE);
CREATE TABLE renglon (pedido_id INTEGER NOT NULL REFERENCES pedido(id) ON DELETE CASCADE,
                      codigo VARCHAR(5) NOT NULL REFERENCES producto(codigo), cantidad INTEGER NOT NULL CHECK (cantidad > 0),
                      precio NUMERIC(10, 2) NOT NULL, PRIMARY KEY (pedido_id, codigo));
INSERT INTO cliente (nombre) VALUES ('Posada La Taza'), ('Guardia Real'), ('Herrería Ferrum');
INSERT INTO producto VALUES ('PAN', 'Pan', 1200, 50), ('CAF', 'Café', 450, 20), ('ESP', 'Espada', 85000, 2), ('ESC', 'Escudo', 41000, 5);
```

```java
// Jefe R04 - Mision 1: el sistema del almacen imperial.
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;
import java.util.Scanner;

public class AlmacenImperial {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        AlmacenService servicio = new AlmacenService();
        Scanner teclado = new Scanner(System.in);
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.equals("salir")) {
                break;
            }
            String[] p = linea.split(" ");
            try {
                switch (p[0]) {
                    case "vender" -> {
                        Map<String, Integer> items = new LinkedHashMap<>();
                        for (String item : p[2].split(",")) {
                            String[] ic = item.split(":");
                            items.put(ic[0], Integer.parseInt(ic[1]));
                        }
                        System.out.println("Pedido " + servicio.vender(Integer.parseInt(p[1]), items) + " registrado");
                    }
                    case "anular" -> {
                        servicio.anular(Integer.parseInt(p[1]));
                        System.out.println("Pedido " + p[1] + " anulado, stock devuelto");
                    }
                    case "stock" -> System.out.println(servicio.stock());
                    case "informe" -> servicio.informe().forEach(System.out::println);
                    default -> System.out.println("Comando inválido");
                }
            } catch (AlmacenException e) {
                System.out.println("Rechazado: " + e.getMessage());
            } catch (SQLException e) {
                System.out.println("Error de base de datos: " + e.getMessage());
            }
        }
    }
}

class AlmacenException extends Exception {
    public AlmacenException(String mensaje) {
        super(mensaje);
    }
}

class PedidoDAO {
    int insertar(Connection con, int clienteId) throws SQLException {
        try (PreparedStatement ps = con.prepareStatement("INSERT INTO pedido (cliente_id) VALUES (?)", Statement.RETURN_GENERATED_KEYS)) {
            ps.setInt(1, clienteId);
            ps.executeUpdate();
            try (ResultSet k = ps.getGeneratedKeys()) {
                k.next();
                return k.getInt(1);
            }
        }
    }

    Boolean estaAnulado(Connection con, int id) throws SQLException {
        try (PreparedStatement ps = con.prepareStatement("SELECT anulado FROM pedido WHERE id = ?")) {
            ps.setInt(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next() ? rs.getBoolean(1) : null;
            }
        }
    }

    void anular(Connection con, int id) throws SQLException {
        try (PreparedStatement ps = con.prepareStatement("UPDATE pedido SET anulado = TRUE WHERE id = ?")) {
            ps.setInt(1, id);
            ps.executeUpdate();
        }
    }
}

class RenglonDAO {
    boolean insertar(Connection con, int pedido, String codigo, int cantidad) throws SQLException {
        String sql = "INSERT INTO renglon (pedido_id, codigo, cantidad, precio) SELECT ?, codigo, ?, precio FROM producto WHERE codigo = ?";
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, pedido);
            ps.setInt(2, cantidad);
            ps.setString(3, codigo);
            return ps.executeUpdate() > 0;
        }
    }

    Map<String, Integer> delPedido(Connection con, int pedido) throws SQLException {
        Map<String, Integer> items = new LinkedHashMap<>();
        try (PreparedStatement ps = con.prepareStatement("SELECT codigo, cantidad FROM renglon WHERE pedido_id = ? ORDER BY codigo")) {
            ps.setInt(1, pedido);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    items.put(rs.getString(1), rs.getInt(2));
                }
            }
        }
        return items;
    }
}

class ProductoDAO {
    void moverStock(Connection con, String codigo, int delta) throws SQLException {
        try (PreparedStatement ps = con.prepareStatement("UPDATE producto SET stock = stock + ? WHERE codigo = ?")) {
            ps.setInt(1, delta);
            ps.setString(2, codigo);
            ps.executeUpdate();
        }
    }

    String listarStock(Connection con) throws SQLException {
        StringBuilder sb = new StringBuilder("Stock:");
        try (PreparedStatement ps = con.prepareStatement("SELECT codigo, stock FROM producto ORDER BY codigo"); ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                sb.append(" ").append(rs.getString(1)).append("=").append(rs.getInt(2));
            }
        }
        return sb.toString();
    }
}

class AlmacenService {
    private final PedidoDAO pedidos = new PedidoDAO();
    private final RenglonDAO renglones = new RenglonDAO();
    private final ProductoDAO productos = new ProductoDAO();

    int vender(int clienteId, Map<String, Integer> items) throws AlmacenException, SQLException {
        try (Connection con = Conexion.abrir()) {
            con.setAutoCommit(false);
            try {
                int id = pedidos.insertar(con, clienteId);
                for (Map.Entry<String, Integer> e : items.entrySet()) {
                    if (!renglones.insertar(con, id, e.getKey(), e.getValue())) {
                        throw new AlmacenException("no existe el producto " + e.getKey());
                    }
                    productos.moverStock(con, e.getKey(), -e.getValue());
                }
                con.commit();
                return id;
            } catch (AlmacenException e) {
                con.rollback();
                throw e;
            } catch (SQLException e) {
                con.rollback();
                throw new AlmacenException("sin stock suficiente o cliente inexistente");
            }
        }
    }

    void anular(int pedidoId) throws AlmacenException, SQLException {
        try (Connection con = Conexion.abrir()) {
            con.setAutoCommit(false);
            try {
                Boolean anulado = pedidos.estaAnulado(con, pedidoId);
                if (anulado == null) {
                    throw new AlmacenException("no existe el pedido " + pedidoId);
                }
                if (anulado) {
                    throw new AlmacenException("el pedido " + pedidoId + " ya estaba anulado");
                }
                for (Map.Entry<String, Integer> e : renglones.delPedido(con, pedidoId).entrySet()) {
                    productos.moverStock(con, e.getKey(), e.getValue());
                }
                pedidos.anular(con, pedidoId);
                con.commit();
            } catch (AlmacenException | SQLException e) {
                con.rollback();
                throw e;
            }
        }
    }

    String stock() throws SQLException {
        try (Connection con = Conexion.abrir()) {
            return productos.listarStock(con);
        }
    }

    java.util.List<String> informe() throws SQLException {
        String sql = "SELECT c.nombre, COUNT(DISTINCT p.id) AS pedidos, COALESCE(SUM(r.cantidad * r.precio), 0) AS total "
                + "FROM cliente c LEFT JOIN pedido p ON p.cliente_id = c.id AND NOT p.anulado "
                + "LEFT JOIN renglon r ON r.pedido_id = p.id GROUP BY c.nombre ORDER BY c.nombre";
        java.util.List<String> filas = new java.util.ArrayList<>();
        try (Connection con = Conexion.abrir(); PreparedStatement ps = con.prepareStatement(sql); ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                filas.add(String.format("%-16s pedidos: %d  total: %.2f", rs.getString(1), rs.getInt(2), rs.getDouble(3)));
            }
        }
        return filas;
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Misión R04-N08-M2 · La auditoría del Liche

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Un sistema viejo **no** tenía restricciones y dejó la base llena de datos rotos: la
tabla `factura` y `item` de `schema.sql` no tienen claves foráneas ni `CHECK`. Escribí
un script SQL que **audite** la base con una consulta por problema: (1) ítems cuya
factura no existe (huérfanos), (2) facturas sin ítems, (3) ítems con cantidad o precio
no positivos, (4) facturas cuyo total guardado no coincide con la suma de sus ítems
(con la diferencia). Después **reparalo** en una transacción SQL (`BEGIN` … `COMMIT`):
borrá los ítems huérfanos y los inválidos, recalculá los totales, y agregá las
restricciones que faltaban (clave foránea y `CHECK`) para que no vuelva a pasar.
Terminá mostrando las facturas corregidas.

`schema.sql`

```sql
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS factura;
CREATE TABLE factura (id INTEGER PRIMARY KEY, cliente VARCHAR(20), total NUMERIC(10, 2));
CREATE TABLE item (id INTEGER PRIMARY KEY, factura_id INTEGER, detalle VARCHAR(20), cantidad INTEGER, precio NUMERIC(10, 2));
INSERT INTO factura VALUES (1, 'Kira', 3000), (2, 'Bron', 900), (3, 'Lía', 500), (4, 'Nara', 0);
INSERT INTO item VALUES (1, 1, 'Pan', 2, 1200), (2, 1, 'Café', 1, 600), (3, 2, 'Guiso', 1, 1000),
                        (4, 7, 'Fantasma', 1, 100), (5, 3, 'Agua', -1, 500), (6, 3, 'Té', 1, 500), (7, 2, 'Pan', 0, 1200);
```

#### Criterio de aprobación

- Cuatro consultas de auditoría, cada una con un comentario.
- La reparación está entre `BEGIN` y `COMMIT` y termina agregando las restricciones.

#### Salida esperada

```
 id | factura_id | detalle  
----+------------+----------
  4 |          7 | Fantasma
(1 row)

 id | cliente 
----+---------
  4 | Nara
(1 row)

 id | factura_id | detalle | cantidad | precio  
----+------------+---------+----------+---------
  5 |          3 | Agua    |       -1 |  500.00
  7 |          2 | Pan     |        0 | 1200.00
(2 rows)

 id | total  | calculado | diferencia 
----+--------+-----------+------------
  2 | 900.00 |   1000.00 |    -100.00
  3 | 500.00 |      0.00 |     500.00
(2 rows)

 id | cliente |  total  | items 
----+---------+---------+-------
  1 | Kira    | 3000.00 |     2
  2 | Bron    | 1000.00 |     1
  3 | Lía     |  500.00 |     1
  4 | Nara    |    0.00 |     0
(4 rows)
```

#### Solución de referencia

```sql
-- Jefe R04 - Mision 2: la auditoria del Liche.
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS factura;
CREATE TABLE factura (id INTEGER PRIMARY KEY, cliente VARCHAR(20), total NUMERIC(10, 2));
CREATE TABLE item (id INTEGER PRIMARY KEY, factura_id INTEGER, detalle VARCHAR(20), cantidad INTEGER, precio NUMERIC(10, 2));
INSERT INTO factura VALUES (1, 'Kira', 3000), (2, 'Bron', 900), (3, 'Lía', 500), (4, 'Nara', 0);
INSERT INTO item VALUES (1, 1, 'Pan', 2, 1200), (2, 1, 'Café', 1, 600), (3, 2, 'Guiso', 1, 1000),
                        (4, 7, 'Fantasma', 1, 100), (5, 3, 'Agua', -1, 500), (6, 3, 'Té', 1, 500), (7, 2, 'Pan', 0, 1200);

-- 1. Ítems huérfanos: su factura no existe
SELECT i.id, i.factura_id, i.detalle FROM item i LEFT JOIN factura f ON f.id = i.factura_id WHERE f.id IS NULL ORDER BY i.id;

-- 2. Facturas sin ítems
SELECT f.id, f.cliente FROM factura f WHERE NOT EXISTS (SELECT 1 FROM item i WHERE i.factura_id = f.id) ORDER BY f.id;

-- 3. Ítems con cantidad o precio no positivos
SELECT id, factura_id, detalle, cantidad, precio FROM item WHERE cantidad <= 0 OR precio <= 0 ORDER BY id;

-- 4. Totales que no coinciden con la suma de los ítems
SELECT f.id, f.total, COALESCE(SUM(i.cantidad * i.precio), 0) AS calculado, f.total - COALESCE(SUM(i.cantidad * i.precio), 0) AS diferencia
FROM factura f LEFT JOIN item i ON i.factura_id = f.id
GROUP BY f.id, f.total HAVING f.total <> COALESCE(SUM(i.cantidad * i.precio), 0) ORDER BY f.id;

-- Reparación, todo o nada
BEGIN;
DELETE FROM item i WHERE NOT EXISTS (SELECT 1 FROM factura f WHERE f.id = i.factura_id);
DELETE FROM item WHERE cantidad <= 0 OR precio <= 0;
UPDATE factura f SET total = COALESCE((SELECT SUM(i.cantidad * i.precio) FROM item i WHERE i.factura_id = f.id), 0);
ALTER TABLE item ADD CONSTRAINT item_factura_fk FOREIGN KEY (factura_id) REFERENCES factura(id);
ALTER TABLE item ADD CONSTRAINT item_positivos CHECK (cantidad > 0 AND precio > 0);
COMMIT;

SELECT f.id, f.cliente, f.total, COUNT(i.id) AS items FROM factura f LEFT JOIN item i ON i.factura_id = f.id GROUP BY f.id ORDER BY f.id;
```

### Encargo R04-N08-E1 · El sistema de turnos del consultorio

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 30
```

#### Consigna

Programá la agenda de un consultorio contra PostgreSQL: pacientes, profesionales y
turnos (fecha y hora como texto `2026-10-05 10:00`, estado `pendiente`, `atendido` o
`cancelado`). Un profesional no puede tener dos turnos no cancelados en el mismo
horario (usá un índice único parcial: `CREATE UNIQUE INDEX … ON turno (profesional_id,
horario) WHERE estado <> 'cancelado'`). Comandos: `turno PACIENTE_ID PROFESIONAL_ID
HORARIO`, `atender TURNO_ID`, `cancelar TURNO_ID`, `agenda PROFESIONAL_ID` (sus turnos
no cancelados, ordenados) y `salir`. En capas, con DAO.

`schema.sql`

```sql
DROP TABLE IF EXISTS turno;
DROP TABLE IF EXISTS paciente;
DROP TABLE IF EXISTS profesional;
CREATE TABLE paciente (id SERIAL PRIMARY KEY, nombre VARCHAR(30) NOT NULL);
CREATE TABLE profesional (id SERIAL PRIMARY KEY, nombre VARCHAR(30) NOT NULL);
CREATE TABLE turno (id SERIAL PRIMARY KEY, paciente_id INTEGER NOT NULL REFERENCES paciente(id),
                    profesional_id INTEGER NOT NULL REFERENCES profesional(id), horario VARCHAR(16) NOT NULL,
                    estado VARCHAR(10) NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'atendido', 'cancelado')));
CREATE UNIQUE INDEX turno_unico ON turno (profesional_id, horario) WHERE estado <> 'cancelado';
INSERT INTO paciente (nombre) VALUES ('Marta Díaz'), ('Juan Pérez'), ('Ana Ruiz');
INSERT INTO profesional (nombre) VALUES ('Dra. Kaffa'), ('Dr. Ferrum');
```

#### Criterio de aprobación

- El índice único parcial impide los turnos superpuestos y el programa lo informa.
- Un turno cancelado libera el horario.

#### Entrada de ejemplo

```
turno 1 1 2026-10-05 10:00
turno 2 1 2026-10-05 10:00
turno 2 1 2026-10-05 10:30
turno 3 2 2026-10-05 10:00
cancelar 1
turno 2 1 2026-10-05 10:00
atender 3
atender 9
agenda 1
salir
```

#### Salida esperada

```
Turno 1 para 2026-10-05 10:00
Rechazado: el profesional ya tiene un turno en ese horario
Turno 3 para 2026-10-05 10:30
Turno 4 para 2026-10-05 10:00
Turno 1 cancelado
Turno 5 para 2026-10-05 10:00
Turno 3 atendido
No existe el turno 9
  2026-10-05 10:00 Juan Pérez (pendiente, turno 5)
  2026-10-05 10:30 Juan Pérez (atendido, turno 3)
```

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS turno;
DROP TABLE IF EXISTS paciente;
DROP TABLE IF EXISTS profesional;
CREATE TABLE paciente (id SERIAL PRIMARY KEY, nombre VARCHAR(30) NOT NULL);
CREATE TABLE profesional (id SERIAL PRIMARY KEY, nombre VARCHAR(30) NOT NULL);
CREATE TABLE turno (id SERIAL PRIMARY KEY, paciente_id INTEGER NOT NULL REFERENCES paciente(id),
                    profesional_id INTEGER NOT NULL REFERENCES profesional(id), horario VARCHAR(16) NOT NULL,
                    estado VARCHAR(10) NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'atendido', 'cancelado')));
CREATE UNIQUE INDEX turno_unico ON turno (profesional_id, horario) WHERE estado <> 'cancelado';
INSERT INTO paciente (nombre) VALUES ('Marta Díaz'), ('Juan Pérez'), ('Ana Ruiz');
INSERT INTO profesional (nombre) VALUES ('Dra. Kaffa'), ('Dr. Ferrum');
```

```java
// Jefe R04 - Encargo: el sistema de turnos del consultorio.
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Consultorio {
    public static void main(String[] args) {
        TurnoDAO dao = new TurnoDAO();
        Scanner teclado = new Scanner(System.in);
        while (teclado.hasNextLine()) {
            String linea = teclado.nextLine().trim();
            if (linea.equals("salir")) {
                break;
            }
            String[] p = linea.split(" ", 4);
            try {
                switch (p[0]) {
                    case "turno" -> System.out.println("Turno " + dao.crear(Integer.parseInt(p[1]), Integer.parseInt(p[2]), p[3]) + " para " + p[3]);
                    case "atender" -> System.out.println(dao.cambiarEstado(Integer.parseInt(p[1]), "atendido") ? "Turno " + p[1] + " atendido" : "No existe el turno " + p[1]);
                    case "cancelar" -> System.out.println(dao.cambiarEstado(Integer.parseInt(p[1]), "cancelado") ? "Turno " + p[1] + " cancelado" : "No existe el turno " + p[1]);
                    case "agenda" -> dao.agenda(Integer.parseInt(p[1])).forEach(t -> System.out.println("  " + t));
                    default -> System.out.println("Comando inválido");
                }
            } catch (SQLException e) {
                System.out.println("Rechazado: " + ("23505".equals(e.getSQLState()) ? "el profesional ya tiene un turno en ese horario" : e.getMessage()));
            }
        }
    }
}

class TurnoDAO {
    int crear(int paciente, int profesional, String horario) throws SQLException {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("INSERT INTO turno (paciente_id, profesional_id, horario) VALUES (?, ?, ?)",
                     Statement.RETURN_GENERATED_KEYS)) {
            ps.setInt(1, paciente);
            ps.setInt(2, profesional);
            ps.setString(3, horario);
            ps.executeUpdate();
            try (ResultSet k = ps.getGeneratedKeys()) {
                k.next();
                return k.getInt(1);
            }
        }
    }

    boolean cambiarEstado(int turno, String estado) throws SQLException {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("UPDATE turno SET estado = ? WHERE id = ?")) {
            ps.setString(1, estado);
            ps.setInt(2, turno);
            return ps.executeUpdate() > 0;
        }
    }

    List<String> agenda(int profesional) throws SQLException {
        String sql = "SELECT t.id, t.horario, p.nombre, t.estado FROM turno t JOIN paciente p ON p.id = t.paciente_id "
                + "WHERE t.profesional_id = ? AND t.estado <> 'cancelado' ORDER BY t.horario";
        List<String> lista = new ArrayList<>();
        try (Connection con = Conexion.abrir(); PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, profesional);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    lista.add(rs.getString("horario") + " " + rs.getString("nombre") + " (" + rs.getString("estado") + ", turno " + rs.getInt("id") + ")");
                }
            }
        }
        return lista;
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Prueba del sello

#### ¿Qué capas tiene un sistema con base de datos bien armado?

La base con sus restricciones, los DAO con el SQL, los servicios con las operaciones del negocio en transacciones, y la interfaz.

#### ¿Por qué los DAO de una operación compuesta reciben la conexión como parámetro?

Para que todas las operaciones compartan la misma transacción y el `rollback` las deshaga juntas.

#### ¿Por qué conviene poner las reglas también en la base y no solo en Java?

Porque la base las hace cumplir para cualquier programa o persona que la modifique.

#### ¿Qué es un dato "huérfano"?

Una fila que apunta a otra que no existe (por ejemplo, un ítem de una factura borrada). Se evita con claves foráneas.

### Soluciones (docente)

Jefe nuevo de la rama 4 (el Liche de las Tablas Huérfanas del guion), integrador de las unidades 3 y 5. La misión 2 es SQL puro y usa `BEGIN`/`COMMIT` de `psql` para mostrar la transacción del lado de la base.

