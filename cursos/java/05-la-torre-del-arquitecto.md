# RAMA R05 · La Torre del Arquitecto: diseño, Spring y el examen

```meta
tipo: tronco
posicion: 5
```

## R05-N03 · Maven y el contenedor de Spring

```meta
tipo: tema
padre: R04-N06
criatura: slime
ejecutable: no
temas: fw.spring, diseno.inyeccion
usa: cal.build
precio: 10
```

### Crónica

Con el vitral del viajero envuelto en lona, Zed sube a la **Torre del Arquitecto**, donde {mentor} dibuja los planos del Imperio. En el tercer piso hay un taller que arma solo: nadie fabrica sus propias piezas. Una grúa gigante, el **Contenedor**, sabe qué pieza va en cada lugar y la coloca. Los maestros solo dicen *"necesito un timonel y una brújula"*, y el Contenedor se los entrega armados. Por la ventana, lejos, se ve el Puerto: la casa de Zed.

—Hasta ahora hacías `new` de todo y conectabas las piezas vos —dice {mentor}—. En el Puerto, **Spring** crea los objetos y se los pasa a quien los necesita. Y **Maven** trae las bibliotecas del mundo sin que copies un solo `.jar`. Es la forma en que se hacen hoy la mayoría de los sistemas en Java, Zed.

### Objetivos

- Entender qué hace Maven: el `pom.xml`, las dependencias y la estructura de carpetas.
- Crear un proyecto de Spring Boot y correrlo.
- Entender la inversión de control y la inyección de dependencias por constructor.
- Usar `@Component`, `@Service`, `@Repository`, `@Value` y `application.properties`.
- Probar los componentes con JUnit, con y sin Spring.

### Antes de empezar

- Interfaces, paquetes, JUnit y el patrón DAO del tronco.
- Instalar un IDE con soporte de Maven (IntelliJ IDEA Community, VS Code con el
  *Extension Pack for Java* o NetBeans). Los proyectos traen el *Maven Wrapper*
  (`mvnw`), así que no hace falta instalar Maven aparte.

### Explicación

#### Maven: el que trae las bibliotecas
En la bóveda copiaste a mano el `.jar` del driver de PostgreSQL. Con diez bibliotecas,
cada una con sus propias dependencias, eso es imposible. **Maven** lo resuelve: en un
archivo `pom.xml` decís **qué** bibliotecas usás y Maven las baja (con todo lo que
ellas necesitan), compila, corre las pruebas y empaqueta.

Todo proyecto Maven tiene la misma forma:
```
mi-proyecto/
├── pom.xml                         ← qué es el proyecto y qué usa
├── mvnw, mvnw.cmd, .mvn/           ← el wrapper: trae Maven solo
└── src/
    ├── main/java/…                 ← el código
    ├── main/resources/             ← configuración (application.properties)
    └── test/java/…                 ← las pruebas
```
| Comando | Hace |
|---|---|
| `./mvnw compile` | compila |
| `./mvnw test` | compila y corre todas las pruebas |
| `./mvnw spring-boot:run` | arranca la aplicación |
| `./mvnw package` | arma un `.jar` ejecutable en `target/` |

En Windows es `mvnw.cmd` en lugar de `./mvnw`.

#### Crear el proyecto
La forma más simple es **start.spring.io** (*Spring Initializr*): elegís Maven, Java
17, el nombre del paquete y las dependencias, y bajás un zip listo. Todos los proyectos
de esta rama usan **Spring Boot 3.3** y un paquete que empieza con `imperio.`.

#### Inversión de control e inyección de dependencias
Sin Spring, cada clase crea lo que necesita:
```java
public class ServicioHeroes {
    private final RepositorioHeroes repositorio = new RepositorioHeroes();   // atado a esta clase concreta
}
```
Con Spring, la clase **pide** lo que necesita en el constructor, y el **contenedor**
(el `ApplicationContext`) crea los objetos y se los pasa:
```java
@Service
public class ServicioHeroes {
    private final RepositorioHeroes repositorio;
    private final Notificador notificador;

    public ServicioHeroes(RepositorioHeroes repositorio, Notificador notificador) {
        this.repositorio = repositorio;
        this.notificador = notificador;
    }
}
```
Eso es la **inversión de control**: ya no controlás vos cuándo se crean los objetos. Y
la **inyección de dependencias**: se las pasan desde afuera. Los objetos que maneja
Spring se llaman **beans**; por defecto hay **uno solo** de cada uno en toda la
aplicación.

| Anotación | Marca |
|---|---|
| `@SpringBootApplication` | la clase principal: arranca todo y busca beans en su paquete y los de abajo |
| `@Component` | un bean cualquiera |
| `@Service` | un bean de lógica de negocio |
| `@Repository` | un bean de acceso a datos |
| `@Value("${clave}")` | inyecta un valor de `application.properties` |
| `@Primary` | si hay dos beans del mismo tipo, cuál se elige |

La ventaja se ve en las pruebas: como el servicio recibe un `Notificador` (una
interfaz), en una prueba le pasás uno falso con `new` y probás el servicio **sin
Spring**, en milisegundos.

#### `application.properties`
La configuración va en `src/main/resources/application.properties`, no en el código:
```properties
spring.main.banner-mode=off
puerto.bienvenida=Bienvenida al Puerto de Spring
```

#### Pruebas con Spring
`@SpringBootTest` arranca el contenedor completo en la prueba y deja inyectar beans con
`@Autowired`. Es más lento que una prueba común, así que se usa para comprobar que todo
se conecta bien; la lógica se prueba con pruebas comunes.

> **Si venís de Python.** Maven hace lo que `pip` + `requirements.txt` + `pytest`, todo
> junto. Spring Boot se parece a Django o FastAPI: un marco que te da la estructura.

### Código de ejemplo

Un proyecto completo: un repositorio en memoria, un notificador (interfaz) y un
servicio que los recibe por constructor. Al arrancar, un `CommandLineRunner` registra
dos héroes. Descargá el esqueleto de start.spring.io (sin dependencias extra) y
reemplazá los archivos.

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>puerto</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
puerto.bienvenida=Bienvenida al Puerto de Spring
```

`src/main/java/imperio/puerto/PuertoApplication.java`

```java
package imperio.puerto;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class PuertoApplication {
    public static void main(String[] args) {
        SpringApplication.run(PuertoApplication.class, args);
    }

    // Se ejecuta una vez, cuando el contenedor terminó de armar todo.
    @Bean
    CommandLineRunner alArrancar(ServicioHeroes servicio) {
        return args -> {
            servicio.registrar("Kira", 7);
            servicio.registrar("Bron", 9);
            System.out.println("Héroes: " + servicio.todos());
        };
    }
}
```

`src/main/java/imperio/puerto/Heroe.java`

```java
package imperio.puerto;

public record Heroe(String nombre, int nivel) {
}
```

`src/main/java/imperio/puerto/RepositorioHeroes.java`

```java
package imperio.puerto;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Repository;

@Repository
public class RepositorioHeroes {
    private final List<Heroe> heroes = new ArrayList<>();

    public void guardar(Heroe heroe) {
        heroes.add(heroe);
    }

    public List<Heroe> todos() {
        return List.copyOf(heroes);
    }
}
```

`src/main/java/imperio/puerto/Notificador.java`

```java
package imperio.puerto;

public interface Notificador {
    void avisar(String mensaje);
}
```

`src/main/java/imperio/puerto/NotificadorConsola.java`

```java
package imperio.puerto;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class NotificadorConsola implements Notificador {
    private final String prefijo;

    public NotificadorConsola(@Value("${puerto.bienvenida}") String prefijo) {
        this.prefijo = prefijo;
    }

    @Override
    public void avisar(String mensaje) {
        System.out.println("[" + prefijo + "] " + mensaje);
    }
}
```

`src/main/java/imperio/puerto/ServicioHeroes.java`

```java
package imperio.puerto;

import java.util.List;

import org.springframework.stereotype.Service;

@Service
public class ServicioHeroes {
    private final RepositorioHeroes repositorio;
    private final Notificador notificador;

    // Un solo constructor: Spring lo usa para inyectar (no hace falta @Autowired).
    public ServicioHeroes(RepositorioHeroes repositorio, Notificador notificador) {
        this.repositorio = repositorio;
        this.notificador = notificador;
    }

    public Heroe registrar(String nombre, int nivel) {
        if (nombre == null || nombre.isBlank()) {
            throw new IllegalArgumentException("el héroe necesita un nombre");
        }
        Heroe heroe = new Heroe(nombre, nivel);
        repositorio.guardar(heroe);
        notificador.avisar("llegó " + nombre + " (nivel " + nivel + ")");
        return heroe;
    }

    public List<Heroe> todos() {
        return repositorio.todos();
    }
}
```

`src/test/java/imperio/puerto/ServicioHeroesTest.java`

```java
package imperio.puerto;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.Test;

// Prueba común, sin Spring: el servicio recibe un notificador falso por constructor.
class ServicioHeroesTest {
    private final List<String> avisos = new ArrayList<>();
    private final ServicioHeroes servicio = new ServicioHeroes(new RepositorioHeroes(), avisos::add);

    @Test
    void registrarGuardaYAvisa() {
        servicio.registrar("Lía", 5);
        assertEquals(List.of(new Heroe("Lía", 5)), servicio.todos());
        assertEquals(List.of("llegó Lía (nivel 5)"), avisos);
    }

    @Test
    void sinNombreNoSeRegistra() {
        assertThrows(IllegalArgumentException.class, () -> servicio.registrar(" ", 3));
        assertEquals(List.of(), avisos);
    }
}
```

`src/test/java/imperio/puerto/PuertoApplicationTest.java`

```java
package imperio.puerto;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

// Prueba con Spring: comprueba que el contenedor arma y conecta los beans.
@SpringBootTest
class PuertoApplicationTest {
    @Autowired
    private ServicioHeroes servicio;

    @Autowired
    private Notificador notificador;

    @Test
    void elContenedorInyectaLosBeans() {
        assertInstanceOf(NotificadorConsola.class, notificador);
        assertEquals(2, servicio.todos().size());      // los dos del CommandLineRunner
    }
}
```

Al correr `./mvnw spring-boot:run` se ve:

```
[Bienvenida al Puerto de Spring] llegó Kira (nivel 7)
[Bienvenida al Puerto de Spring] llegó Bron (nivel 9)
Héroes: [Heroe[nombre=Kira, nivel=7], Heroe[nombre=Bron, nivel=9]]
```

Y `./mvnw test` corre las tres pruebas.

### ¿Para qué sirve?

Casi todas las empresas que usan Java arman sus sistemas con Spring Boot y Maven (o Gradle). Saber leer un `pom.xml`, entender por qué las clases reciben todo por constructor y probarlas sin levantar el sistema entero es lo primero que se pide en un puesto de desarrollador Java.

### Errores habituales

**Ogro: el bean que no aparece.** `No qualifying bean of type…`: la clase no tiene
`@Component`/`@Service`/`@Repository`, o está en un paquete que no está **debajo** del
de la clase `@SpringBootApplication`.

**Troll: el `new` de un bean.** Hacer `new ServicioHeroes(...)` dentro de otro bean crea
un objeto que Spring no conoce (con otro repositorio). Pedilo por constructor.

**Goblin: dos candidatos.** Si hay dos clases que implementan `Notificador`, Spring no
sabe cuál inyectar (`expected single matching bean but found 2`). Marcá una con
`@Primary` o elegí con `@Qualifier`.

**Ogro: la clave mal escrita.** `@Value("${puerto.bienvenidas}")` con una clave que no
existe hace fallar el arranque: `Could not resolve placeholder`.

**Slime: inyección en el atributo.** `@Autowired private Repositorio r;` funciona, pero
el atributo no puede ser `final` y la clase no se puede probar sin Spring. Preferí el
constructor.

### Misión R05-N03-M1 · El reloj del puerto

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Creá un proyecto de Spring Boot con un servicio `ServicioTurnos` que asigna turnos de
carga a los barcos (`asignar(String barco)` devuelve un `record Turno(int numero, String
barco, String hora)`). La hora sale de un bean `Reloj` (una **interfaz** con un método
`String ahora()`): en la aplicación, un `@Component` `RelojDelSistema` que devuelve la
hora real con formato `HH:mm`. La cantidad máxima de turnos del día sale de
`application.properties` (`puerto.turnos-maximos=3`): pasado el máximo, `asignar` lanza
`IllegalStateException`.

Escribí pruebas **sin Spring** con un reloj falso que siempre devuelve `"08:30"`, y una
prueba con `@SpringBootTest` que compruebe que el máximo se leyó de la configuración.
Entregá el proyecto en un zip (sin la carpeta `target`).

#### Criterio de aprobación

- El servicio recibe el reloj y el máximo por constructor; nada hace `new` de un bean.
- Las pruebas con el reloj falso cubren la numeración y el máximo, y pasan con `./mvnw test`.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>turnos</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
puerto.turnos-maximos=3
```

`src/main/java/imperio/turnos/TurnosApplication.java`

```java
package imperio.turnos;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TurnosApplication {
    public static void main(String[] args) {
        SpringApplication.run(TurnosApplication.class, args);
    }
}
```

`src/main/java/imperio/turnos/Reloj.java`

```java
package imperio.turnos;

public interface Reloj {
    String ahora();
}
```

`src/main/java/imperio/turnos/RelojDelSistema.java`

```java
package imperio.turnos;

import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

import org.springframework.stereotype.Component;

@Component
public class RelojDelSistema implements Reloj {
    @Override
    public String ahora() {
        return LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm"));
    }
}
```

`src/main/java/imperio/turnos/Turno.java`

```java
package imperio.turnos;

public record Turno(int numero, String barco, String hora) {
}
```

`src/main/java/imperio/turnos/ServicioTurnos.java`

```java
package imperio.turnos;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class ServicioTurnos {
    private final Reloj reloj;
    private final int maximo;
    private int asignados;

    public ServicioTurnos(Reloj reloj, @Value("${puerto.turnos-maximos}") int maximo) {
        this.reloj = reloj;
        this.maximo = maximo;
    }

    public synchronized Turno asignar(String barco) {
        if (asignados >= maximo) {
            throw new IllegalStateException("no quedan turnos hoy (máximo " + maximo + ")");
        }
        asignados++;
        return new Turno(asignados, barco, reloj.ahora());
    }

    public int maximo() {
        return maximo;
    }
}
```

`src/test/java/imperio/turnos/ServicioTurnosTest.java`

```java
package imperio.turnos;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class ServicioTurnosTest {
    private final ServicioTurnos servicio = new ServicioTurnos(() -> "08:30", 2);

    @Test
    void losTurnosSeNumeranConLaHoraDelReloj() {
        assertEquals(new Turno(1, "Gaviota", "08:30"), servicio.asignar("Gaviota"));
        assertEquals(new Turno(2, "Albatros", "08:30"), servicio.asignar("Albatros"));
    }

    @Test
    void pasadoElMaximoNoHayMasTurnos() {
        servicio.asignar("Gaviota");
        servicio.asignar("Albatros");
        IllegalStateException e = assertThrows(IllegalStateException.class, () -> servicio.asignar("Petrel"));
        assertEquals("no quedan turnos hoy (máximo 2)", e.getMessage());
    }
}
```

`src/test/java/imperio/turnos/TurnosApplicationTest.java`

```java
package imperio.turnos;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class TurnosApplicationTest {
    @Autowired
    private ServicioTurnos servicio;

    @Test
    void elMaximoSaleDeLaConfiguracion() {
        assertEquals(3, servicio.maximo());
        assertTrue(servicio.asignar("Gaviota").hora().matches("\\d{2}:\\d{2}"));
    }
}
```

### Misión R05-N03-M2 · Dos notificadores

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Partiendo del ejemplo, agregá una segunda implementación de `Notificador`,
`NotificadorArchivo`, que **guarda** los avisos en una lista en memoria (simula un
archivo de registro) y los devuelve con `registrados()`. Hacé que Spring use
`NotificadorArchivo` por defecto con `@Primary`, y que un bean `ServicioAlertas` reciba
**específicamente** el de consola con `@Qualifier("notificadorConsola")`. Probá con
`@SpringBootTest` que el servicio de héroes avisa al de archivo y que las alertas van al
de consola.

#### Criterio de aprobación

- Usa `@Primary` y `@Qualifier` y la aplicación arranca sin el error de "dos candidatos".
- La prueba demuestra a qué notificador llega cada aviso.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>puerto</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
puerto.bienvenida=Puerto
```

`src/main/java/imperio/puerto/PuertoApplication.java`

```java
package imperio.puerto;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class PuertoApplication {
    public static void main(String[] args) {
        SpringApplication.run(PuertoApplication.class, args);
    }
}
```

`src/main/java/imperio/puerto/Heroe.java`

```java
package imperio.puerto;

public record Heroe(String nombre, int nivel) {
}
```

`src/main/java/imperio/puerto/RepositorioHeroes.java`

```java
package imperio.puerto;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Repository;

@Repository
public class RepositorioHeroes {
    private final List<Heroe> heroes = new ArrayList<>();

    public void guardar(Heroe heroe) {
        heroes.add(heroe);
    }

    public List<Heroe> todos() {
        return List.copyOf(heroes);
    }
}
```

`src/main/java/imperio/puerto/Notificador.java`

```java
package imperio.puerto;

public interface Notificador {
    void avisar(String mensaje);
}
```

`src/main/java/imperio/puerto/NotificadorConsola.java`

```java
package imperio.puerto;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class NotificadorConsola implements Notificador {
    private final String prefijo;
    private final List<String> mostrados = new ArrayList<>();

    public NotificadorConsola(@Value("${puerto.bienvenida}") String prefijo) {
        this.prefijo = prefijo;
    }

    @Override
    public void avisar(String mensaje) {
        String linea = "[" + prefijo + "] " + mensaje;
        mostrados.add(linea);
        System.out.println(linea);
    }

    public List<String> mostrados() {
        return List.copyOf(mostrados);
    }
}
```

`src/main/java/imperio/puerto/NotificadorArchivo.java`

```java
package imperio.puerto;

import java.util.ArrayList;
import java.util.List;

import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Component;

@Component
@Primary
public class NotificadorArchivo implements Notificador {
    private final List<String> registrados = new ArrayList<>();

    @Override
    public void avisar(String mensaje) {
        registrados.add(mensaje);
    }

    public List<String> registrados() {
        return List.copyOf(registrados);
    }
}
```

`src/main/java/imperio/puerto/ServicioHeroes.java`

```java
package imperio.puerto;

import java.util.List;

import org.springframework.stereotype.Service;

@Service
public class ServicioHeroes {
    private final RepositorioHeroes repositorio;
    private final Notificador notificador;

    public ServicioHeroes(RepositorioHeroes repositorio, Notificador notificador) {
        this.repositorio = repositorio;
        this.notificador = notificador;
    }

    public Heroe registrar(String nombre, int nivel) {
        Heroe heroe = new Heroe(nombre, nivel);
        repositorio.guardar(heroe);
        notificador.avisar("llegó " + nombre);
        return heroe;
    }

    public List<Heroe> todos() {
        return repositorio.todos();
    }
}
```

`src/main/java/imperio/puerto/ServicioAlertas.java`

```java
package imperio.puerto;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

@Service
public class ServicioAlertas {
    private final Notificador consola;

    public ServicioAlertas(@Qualifier("notificadorConsola") Notificador consola) {
        this.consola = consola;
    }

    public void alertar(String problema) {
        consola.avisar("ALERTA: " + problema);
    }
}
```

`src/test/java/imperio/puerto/NotificadoresTest.java`

```java
package imperio.puerto;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class NotificadoresTest {
    @Autowired
    private ServicioHeroes heroes;

    @Autowired
    private ServicioAlertas alertas;

    @Autowired
    private NotificadorArchivo archivo;

    @Autowired
    private NotificadorConsola consola;

    @Test
    void cadaAvisoVaAlNotificadorQueCorresponde() {
        heroes.registrar("Kira", 7);
        alertas.alertar("marea alta");
        assertEquals(List.of("llegó Kira"), archivo.registrados());
        assertEquals(List.of("[Puerto] ALERTA: marea alta"), consola.mostrados());
    }
}
```

### Misión R05-N03-M3 · El conversor configurable

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá un proyecto con un servicio `Conversor` que convierte montos entre pesos y otras
monedas. Las cotizaciones vienen de una interfaz `FuenteCotizaciones` (`double
cotizacion(String moneda)`); en la aplicación, un `@Component` las lee de
`application.properties` con `@Value` (`conversor.dolar=1250`, `conversor.euro=1370`,
`conversor.real=230`) y lanza `IllegalArgumentException` si la moneda no existe. El
conversor redondea a 2 decimales. Probalo con una fuente falsa (sin Spring) y con
`@SpringBootTest`.

#### Criterio de aprobación

- Las cotizaciones salen de la configuración, no del código.
- Hay pruebas sin Spring (con una fuente falsa) y con Spring, y pasan.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>conversor</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
conversor.dolar=1250
conversor.euro=1370
conversor.real=230
```

`src/main/java/imperio/conversor/ConversorApplication.java`

```java
package imperio.conversor;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ConversorApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConversorApplication.class, args);
    }
}
```

`src/main/java/imperio/conversor/FuenteCotizaciones.java`

```java
package imperio.conversor;

public interface FuenteCotizaciones {
    double cotizacion(String moneda);
}
```

`src/main/java/imperio/conversor/CotizacionesConfiguradas.java`

```java
package imperio.conversor;

import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class CotizacionesConfiguradas implements FuenteCotizaciones {
    private final Map<String, Double> cotizaciones;

    public CotizacionesConfiguradas(@Value("${conversor.dolar}") double dolar,
                                    @Value("${conversor.euro}") double euro,
                                    @Value("${conversor.real}") double real) {
        this.cotizaciones = Map.of("dolar", dolar, "euro", euro, "real", real);
    }

    @Override
    public double cotizacion(String moneda) {
        Double valor = cotizaciones.get(moneda);
        if (valor == null) {
            throw new IllegalArgumentException("moneda desconocida: " + moneda);
        }
        return valor;
    }
}
```

`src/main/java/imperio/conversor/Conversor.java`

```java
package imperio.conversor;

import org.springframework.stereotype.Service;

@Service
public class Conversor {
    private final FuenteCotizaciones fuente;

    public Conversor(FuenteCotizaciones fuente) {
        this.fuente = fuente;
    }

    public double aPesos(double monto, String moneda) {
        return redondear(monto * fuente.cotizacion(moneda));
    }

    public double desdePesos(double pesos, String moneda) {
        return redondear(pesos / fuente.cotizacion(moneda));
    }

    private static double redondear(double valor) {
        return Math.round(valor * 100) / 100.0;
    }
}
```

`src/test/java/imperio/conversor/ConversorTest.java`

```java
package imperio.conversor;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class ConversorTest {
    private final Conversor conversor = new Conversor(moneda -> {
        if (!moneda.equals("dolar")) {
            throw new IllegalArgumentException("moneda desconocida: " + moneda);
        }
        return 1000;
    });

    @Test
    void convierteYRedondea() {
        assertEquals(15000.0, conversor.aPesos(15, "dolar"));
        assertEquals(3.33, conversor.desdePesos(3333, "dolar"));
    }

    @Test
    void unaMonedaDesconocidaFalla() {
        assertThrows(IllegalArgumentException.class, () -> conversor.aPesos(1, "yen"));
    }
}
```

`src/test/java/imperio/conversor/ConversorApplicationTest.java`

```java
package imperio.conversor;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class ConversorApplicationTest {
    @Autowired
    private Conversor conversor;

    @Test
    void usaLasCotizacionesDeLaConfiguracion() {
        assertEquals(12500.0, conversor.aPesos(10, "dolar"));
        assertEquals(100.0, conversor.desdePesos(137000, "euro"));
        assertEquals(10.87, conversor.desdePesos(2500, "real"));
    }
}
```

### Encargo R05-N03-E1 · El despachante de pedidos

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Una distribuidora quiere un servicio `Despachante` que reciba un pedido (`record
Pedido(String cliente, double kilos, String zona)`) y le asigne un transporte: tiene una
**lista de beans** que implementan `Transporte` (`boolean puedeLlevar(Pedido)`,
`double costo(Pedido)`, `String nombre()`), por ejemplo `Moto` (hasta 10 kg, solo zona
"centro"), `Camioneta` (hasta 500 kg, solo en la ciudad: zonas "centro", "norte" y "sur") y `Camion` (cualquier peso, mínimo 100 kg). El
despachante elige el **más barato** que puede llevarlo (Spring le inyecta todos los
`Transporte` en un `List<Transporte>`) y devuelve un `Optional` vacío si ninguno puede.
Probalo con `@SpringBootTest`.

#### Criterio de aprobación

- El despachante recibe un `List<Transporte>` por constructor y no conoce las clases concretas.
- Agregar un transporte nuevo es agregar una clase, sin tocar el despachante.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>despacho</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/despacho/DespachoApplication.java`

```java
package imperio.despacho;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DespachoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DespachoApplication.class, args);
    }
}
```

`src/main/java/imperio/despacho/Pedido.java`

```java
package imperio.despacho;

public record Pedido(String cliente, double kilos, String zona) {
}
```

`src/main/java/imperio/despacho/Transporte.java`

```java
package imperio.despacho;

public interface Transporte {
    String nombre();

    boolean puedeLlevar(Pedido pedido);

    double costo(Pedido pedido);
}
```

`src/main/java/imperio/despacho/Moto.java`

```java
package imperio.despacho;

import org.springframework.stereotype.Component;

@Component
public class Moto implements Transporte {
    public String nombre() {
        return "moto";
    }

    public boolean puedeLlevar(Pedido p) {
        return p.kilos() <= 10 && p.zona().equals("centro");
    }

    public double costo(Pedido p) {
        return 1500;
    }
}
```

`src/main/java/imperio/despacho/Camioneta.java`

```java
package imperio.despacho;

import java.util.List;

import org.springframework.stereotype.Component;

@Component
public class Camioneta implements Transporte {
    public String nombre() {
        return "camioneta";
    }

    public boolean puedeLlevar(Pedido p) {
        return p.kilos() <= 500 && List.of("centro", "norte", "sur").contains(p.zona());
    }

    public double costo(Pedido p) {
        return 4000 + p.kilos() * 20;
    }
}
```

`src/main/java/imperio/despacho/Camion.java`

```java
package imperio.despacho;

import org.springframework.stereotype.Component;

@Component
public class Camion implements Transporte {
    public String nombre() {
        return "camión";
    }

    public boolean puedeLlevar(Pedido p) {
        return p.kilos() >= 100;
    }

    public double costo(Pedido p) {
        return 9000 + p.kilos() * 8;
    }
}
```

`src/main/java/imperio/despacho/Despachante.java`

```java
package imperio.despacho;

import java.util.Comparator;
import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;

@Service
public class Despachante {
    private final List<Transporte> transportes;

    public Despachante(List<Transporte> transportes) {
        this.transportes = transportes;
    }

    public Optional<Transporte> elegir(Pedido pedido) {
        return transportes.stream()
                .filter(t -> t.puedeLlevar(pedido))
                .min(Comparator.comparingDouble(t -> t.costo(pedido)));
    }
}
```

`src/test/java/imperio/despacho/DespachanteTest.java`

```java
package imperio.despacho;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class DespachanteTest {
    @Autowired
    private Despachante despachante;

    private String elegido(double kilos, String zona) {
        return despachante.elegir(new Pedido("Ana", kilos, zona)).map(Transporte::nombre).orElse("ninguno");
    }

    @Test
    void eligeElMasBaratoQuePuede() {
        assertEquals("moto", elegido(5, "centro"));
        assertEquals("camioneta", elegido(5, "norte"));
        assertEquals("camioneta", elegido(300, "norte"));
        assertEquals("camión", elegido(450, "sur"));
        assertEquals("camión", elegido(2000, "sur"));
    }

    @Test
    void sinTransportePosibleDevuelveVacio() {
        assertTrue(despachante.elegir(new Pedido("Ana", 50, "rural")).isEmpty());
        assertEquals("camión", elegido(150, "rural"));
    }
}
```

### Prueba del sello

#### ¿Para qué sirve el `pom.xml`?

Describe el proyecto y sus dependencias; Maven las baja y sabe cómo compilar, probar y empaquetar.

#### ¿Qué es la inversión de control?

Que no es tu código el que crea y conecta los objetos, sino el contenedor de Spring.

#### ¿Por qué conviene la inyección por constructor?

Porque las dependencias quedan explícitas, los atributos pueden ser `final` y la clase se puede probar sin Spring pasándole objetos falsos.

#### ¿Qué pasa si hay dos beans del mismo tipo?

Spring no sabe cuál inyectar y falla; se resuelve con `@Primary` o `@Qualifier`.

#### ¿Para qué sirve `application.properties`?

Para la configuración (puertos, claves, valores) fuera del código; se lee con `@Value`.

### Soluciones (docente)

Sale de `19-Java-Avanzado/12-Spring-Boot-IoC-DI`. Las soluciones se verifican con `mvn test` (Spring Boot 3.3.5, Java 17). Se corrige descomprimiendo el zip y corriendo `./mvnw test`.

## R05-N04 · Servicios REST

```meta
tipo: tema
padre: R05-N03
precio: 10
criatura: orc
ejecutable: no
temas: web.http, web.api-rest
usa: fw.spring
```

### Crónica

En el muelle central del Puerto hay una ventanilla que nunca cierra. Llegan mensajeros de todo el Imperio con pedidos escritos siempre igual: *"DAME el barco 7"*, *"AGREGÁ este cargamento"*, *"BORRÁ el turno 3"*. La ventanilla contesta con un número y un papel: *200, acá está*; *404, ese barco no existe*.

—Así se hablan hoy los sistemas —dice {mentor}—: por **HTTP**, con verbos y códigos que todos entienden. Una app de celular, una página web, otro sistema: todos le piden datos a un **servicio REST**. Tu ventanilla va a ser un `@RestController`, {heroe}.

### Objetivos

- Entender HTTP: verbos, rutas, códigos de estado y JSON.
- Crear un `@RestController` con `@GetMapping`, `@PostMapping`, `@PutMapping` y `@DeleteMapping`.
- Recibir datos con `@PathVariable`, `@RequestParam` y `@RequestBody`.
- Responder con el código correcto usando `ResponseEntity`.
- Probar la API con `MockMvc`, sin levantar el servidor.

### Antes de empezar

- Maven y el contenedor de Spring.

### Explicación

#### HTTP en dos minutos
Un **pedido** HTTP tiene un **verbo**, una **ruta** y, a veces, un **cuerpo** (en JSON).
La **respuesta** trae un **código de estado** y, a veces, un cuerpo.
| Verbo | Para | Ejemplo |
|---|---|---|
| `GET` | leer | `GET /heroes`, `GET /heroes/3` |
| `POST` | crear | `POST /heroes` con el héroe en el cuerpo |
| `PUT` | reemplazar | `PUT /heroes/3` con el héroe completo |
| `PATCH` | modificar una parte | `PATCH /heroes/3/nivel` |
| `DELETE` | borrar | `DELETE /heroes/3` |

| Código | Significa |
|---|---|
| `200 OK` | salió bien, acá está |
| `201 Created` | se creó (con la ruta del nuevo en el encabezado `Location`) |
| `204 No Content` | salió bien, no hay nada que devolver |
| `400 Bad Request` | el pedido está mal armado |
| `404 Not Found` | eso no existe |
| `409 Conflict` | choca con algo que ya existe |

**REST** es una forma de ordenar las rutas: los **recursos** son sustantivos en plural
(`/heroes`), y el verbo dice qué se hace con ellos.

#### El controlador
Con `spring-boot-starter-web`, Spring Boot trae un servidor (Tomcat) adentro. Un
`@RestController` atiende pedidos; lo que devuelve cada método se convierte en JSON solo
(los `record` se convierten perfecto):
```java
@RestController
@RequestMapping("/heroes")
public class HeroeController {
    private final ServicioHeroes servicio;

    public HeroeController(ServicioHeroes servicio) {
        this.servicio = servicio;
    }

    @GetMapping
    public List<Heroe> listar(@RequestParam(required = false) String clase) { … }

    @GetMapping("/{id}")
    public ResponseEntity<Heroe> buscar(@PathVariable long id) {
        return servicio.buscar(id)
                .map(ResponseEntity::ok)                       // 200 con el héroe
                .orElse(ResponseEntity.notFound().build());    // 404
    }

    @PostMapping
    public ResponseEntity<Heroe> crear(@RequestBody Heroe nuevo) {
        Heroe creado = servicio.crear(nuevo);
        return ResponseEntity.created(URI.create("/heroes/" + creado.id())).body(creado);   // 201
    }
}
```
| Anotación | Toma el dato de |
|---|---|
| `@PathVariable` | la ruta: `/heroes/{id}` |
| `@RequestParam` | la consulta: `/heroes?clase=maga` (`required = false` si es opcional) |
| `@RequestBody` | el cuerpo JSON del pedido |

El controlador **no tiene lógica**: recibe, llama al servicio y arma la respuesta. Las
reglas están en el servicio (que se prueba sin HTTP).

#### Probar con MockMvc
`MockMvc` simula pedidos HTTP sin abrir un puerto, y deja comprobar el código y el JSON
de la respuesta con `jsonPath`:
```java
mvc.perform(get("/heroes/1"))
   .andExpect(status().isOk())
   .andExpect(jsonPath("$.nombre").value("Kira"));

mvc.perform(post("/heroes").contentType(MediaType.APPLICATION_JSON)
        .content("""
                {"nombre": "Lía", "clase": "maga", "nivel": 5}
                """))
   .andExpect(status().isCreated())
   .andExpect(header().string("Location", "/heroes/3"));
```
`$.nombre` es un campo del objeto; `$[0].nombre`, del primero de una lista;
`$.length()`, el tamaño.

#### Probar a mano
Con la aplicación corriendo (`./mvnw spring-boot:run`, puerto 8080), un `GET` se prueba
desde el navegador (`http://localhost:8080/heroes`). Para los demás verbos, `curl` o una
herramienta como Bruno o Postman:
```
curl -X POST localhost:8080/heroes -H "Content-Type: application/json" -d '{"nombre":"Lía","clase":"maga","nivel":5}'
```

> **Si venís de Python.** Es lo mismo que una ruta de Flask o FastAPI:
> `@app.get("/heroes/{id}")` en FastAPI es `@GetMapping("/{id}")` acá.

### Código de ejemplo

La ventanilla de los héroes: una API REST completa en memoria, con sus pruebas.

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>ventanilla</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/ventanilla/VentanillaApplication.java`

```java
package imperio.ventanilla;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class VentanillaApplication {
    public static void main(String[] args) {
        SpringApplication.run(VentanillaApplication.class, args);
    }
}
```

`src/main/java/imperio/ventanilla/Heroe.java`

```java
package imperio.ventanilla;

public record Heroe(Long id, String nombre, String clase, int nivel) {
    public Heroe conId(long nuevoId) {
        return new Heroe(nuevoId, nombre, clase, nivel);
    }
}
```

`src/main/java/imperio/ventanilla/ServicioHeroes.java`

```java
package imperio.ventanilla;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.stereotype.Service;

@Service
public class ServicioHeroes {
    private final Map<Long, Heroe> heroes = new ConcurrentHashMap<>();
    private final AtomicLong proximoId = new AtomicLong(1);

    public ServicioHeroes() {
        crear(new Heroe(null, "Kira", "arquera", 7));
        crear(new Heroe(null, "Bron", "guerrero", 9));
    }

    public List<Heroe> listar(String clase) {
        return heroes.values().stream()
                .filter(h -> clase == null || h.clase().equals(clase))
                .sorted((a, b) -> Long.compare(a.id(), b.id()))
                .toList();
    }

    public Optional<Heroe> buscar(long id) {
        return Optional.ofNullable(heroes.get(id));
    }

    public Heroe crear(Heroe nuevo) {
        Heroe conId = nuevo.conId(proximoId.getAndIncrement());
        heroes.put(conId.id(), conId);
        return conId;
    }

    public Optional<Heroe> reemplazar(long id, Heroe datos) {
        if (!heroes.containsKey(id)) {
            return Optional.empty();
        }
        Heroe nuevo = datos.conId(id);
        heroes.put(id, nuevo);
        return Optional.of(nuevo);
    }

    public boolean borrar(long id) {
        return heroes.remove(id) != null;
    }
}
```

`src/main/java/imperio/ventanilla/HeroeController.java`

```java
package imperio.ventanilla;

import java.net.URI;
import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/heroes")
public class HeroeController {
    private final ServicioHeroes servicio;

    public HeroeController(ServicioHeroes servicio) {
        this.servicio = servicio;
    }

    @GetMapping
    public List<Heroe> listar(@RequestParam(required = false) String clase) {
        return servicio.listar(clase);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Heroe> buscar(@PathVariable long id) {
        return servicio.buscar(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Heroe> crear(@RequestBody Heroe nuevo) {
        Heroe creado = servicio.crear(nuevo);
        return ResponseEntity.created(URI.create("/heroes/" + creado.id())).body(creado);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Heroe> reemplazar(@PathVariable long id, @RequestBody Heroe datos) {
        return servicio.reemplazar(id, datos).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> borrar(@PathVariable long id) {
        return servicio.borrar(id) ? ResponseEntity.noContent().build() : ResponseEntity.notFound().build();
    }
}
```

`src/test/java/imperio/ventanilla/HeroeControllerTest.java`

```java
package imperio.ventanilla;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)   // cada prueba arranca con los datos iniciales
class HeroeControllerTest {
    @Autowired
    private MockMvc mvc;

    @Test
    void listaTodosYFiltraPorClase() throws Exception {
        mvc.perform(get("/heroes"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(2))
                .andExpect(jsonPath("$[0].nombre").value("Kira"));
        mvc.perform(get("/heroes").param("clase", "guerrero"))
                .andExpect(jsonPath("$.length()").value(1))
                .andExpect(jsonPath("$[0].nombre").value("Bron"));
    }

    @Test
    void buscaUnoOContesta404() throws Exception {
        mvc.perform(get("/heroes/2")).andExpect(status().isOk()).andExpect(jsonPath("$.nivel").value(9));
        mvc.perform(get("/heroes/99")).andExpect(status().isNotFound());
    }

    @Test
    void creaConCodigo201YLocation() throws Exception {
        mvc.perform(post("/heroes").contentType(MediaType.APPLICATION_JSON).content("""
                        {"nombre": "Lía", "clase": "maga", "nivel": 5}
                        """))
                .andExpect(status().isCreated())
                .andExpect(header().string("Location", "/heroes/3"))
                .andExpect(jsonPath("$.id").value(3));
        mvc.perform(get("/heroes")).andExpect(jsonPath("$.length()").value(3));
    }

    @Test
    void reemplazaYBorra() throws Exception {
        mvc.perform(put("/heroes/1").contentType(MediaType.APPLICATION_JSON).content("""
                        {"nombre": "Kira", "clase": "arquera", "nivel": 8}
                        """))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.nivel").value(8));
        mvc.perform(delete("/heroes/1")).andExpect(status().isNoContent());
        mvc.perform(delete("/heroes/1")).andExpect(status().isNotFound());
    }
}
```

Con la aplicación corriendo:

```
$ curl localhost:8080/heroes
[{"id":1,"nombre":"Kira","clase":"arquera","nivel":7},{"id":2,"nombre":"Bron","clase":"guerrero","nivel":9}]
$ curl -i localhost:8080/heroes/99
HTTP/1.1 404
```

### ¿Para qué sirve?

Todas las apps que usás le piden datos a un servicio REST: el home banking, la app del colectivo, una tienda online. El *backend* que las atiende muy a menudo está hecho con Spring Boot. Con lo de este nodo ya podés hacer el servidor de una app de celular o de una página hecha en JavaScript.

### Errores habituales

**Ogro: todo devuelve 200.** Devolver `null` (que da un 200 vacío) cuando algo no existe,
o 200 al crear. Usá `ResponseEntity` con el código que corresponde: 404, 201, 204.

**Troll: la lógica en el controlador.** Validar, calcular y guardar dentro del
controlador: queda imposible de probar sin HTTP y se repite. El controlador solo recibe y
responde; la lógica va en el servicio.

**Goblin: el `Content-Type` olvidado.** Un `POST` con JSON sin
`Content-Type: application/json` da `415 Unsupported Media Type`.

**Ogro: el `HashMap` compartido.** El servidor atiende muchos pedidos a la vez, en hilos
distintos: los datos en memoria van en un `ConcurrentHashMap` y los contadores en un
`AtomicLong` (lo viste en las Corrientes).

**Slime: el puerto ocupado.** `Port 8080 was already in use`: quedó otra aplicación
corriendo. Cerrala o cambiá `server.port` en `application.properties`.

### Misión R05-N04-M1 · La API de la biblioteca

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Hacé una API REST para los libros de una biblioteca (`record Libro(Long id, String
titulo, String autor, int anio, boolean prestado)`), en memoria, con tres libros
cargados al arrancar:

- `GET /libros` — todos, ordenados por id.
- `GET /libros/{id}` — uno, o 404.
- `POST /libros` — crea (siempre sin prestar), 201 con `Location`.
- `POST /libros/{id}/prestamo` — lo marca prestado; 404 si no existe, **409** si ya estaba
  prestado.
- `DELETE /libros/{id}/prestamo` — lo devuelve (204); 409 si no estaba prestado.

Probá cada ruta con `MockMvc`, incluidos los 404 y 409.

#### Criterio de aprobación

- Cada ruta responde el código correcto (200, 201, 204, 404, 409).
- La lógica está en el servicio y las pruebas pasan.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>biblioteca</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/biblioteca/BibliotecaApplication.java`

```java
package imperio.biblioteca;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class BibliotecaApplication {
    public static void main(String[] args) {
        SpringApplication.run(BibliotecaApplication.class, args);
    }
}
```

`src/main/java/imperio/biblioteca/Libro.java`

```java
package imperio.biblioteca;

public record Libro(Long id, String titulo, String autor, int anio, boolean prestado) {
    public Libro conId(long nuevoId) {
        return new Libro(nuevoId, titulo, autor, anio, false);
    }

    public Libro conPrestado(boolean valor) {
        return new Libro(id, titulo, autor, anio, valor);
    }
}
```

`src/main/java/imperio/biblioteca/Resultado.java`

```java
package imperio.biblioteca;

// Lo que puede pasar al prestar o devolver.
public enum Resultado { HECHO, NO_EXISTE, CONFLICTO }
```

`src/main/java/imperio/biblioteca/ServicioLibros.java`

```java
package imperio.biblioteca;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.stereotype.Service;

@Service
public class ServicioLibros {
    private final Map<Long, Libro> libros = new ConcurrentHashMap<>();
    private final AtomicLong proximoId = new AtomicLong(1);

    public ServicioLibros() {
        crear(new Libro(null, "Rayuela", "Julio Cortázar", 1963, false));
        crear(new Libro(null, "Ficciones", "Jorge Luis Borges", 1944, false));
        crear(new Libro(null, "El túnel", "Ernesto Sabato", 1948, false));
    }

    public List<Libro> todos() {
        return libros.values().stream().sorted(Comparator.comparing(Libro::id)).toList();
    }

    public Optional<Libro> buscar(long id) {
        return Optional.ofNullable(libros.get(id));
    }

    public Libro crear(Libro nuevo) {
        Libro libro = nuevo.conId(proximoId.getAndIncrement());
        libros.put(libro.id(), libro);
        return libro;
    }

    public synchronized Resultado cambiarPrestamo(long id, boolean prestar) {
        Libro libro = libros.get(id);
        if (libro == null) {
            return Resultado.NO_EXISTE;
        }
        if (libro.prestado() == prestar) {
            return Resultado.CONFLICTO;
        }
        libros.put(id, libro.conPrestado(prestar));
        return Resultado.HECHO;
    }
}
```

`src/main/java/imperio/biblioteca/LibroController.java`

```java
package imperio.biblioteca;

import java.net.URI;
import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/libros")
public class LibroController {
    private final ServicioLibros servicio;

    public LibroController(ServicioLibros servicio) {
        this.servicio = servicio;
    }

    @GetMapping
    public List<Libro> todos() {
        return servicio.todos();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Libro> buscar(@PathVariable long id) {
        return servicio.buscar(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Libro> crear(@RequestBody Libro nuevo) {
        Libro creado = servicio.crear(nuevo);
        return ResponseEntity.created(URI.create("/libros/" + creado.id())).body(creado);
    }

    @PostMapping("/{id}/prestamo")
    public ResponseEntity<Void> prestar(@PathVariable long id) {
        return responder(servicio.cambiarPrestamo(id, true));
    }

    @DeleteMapping("/{id}/prestamo")
    public ResponseEntity<Void> devolver(@PathVariable long id) {
        return responder(servicio.cambiarPrestamo(id, false));
    }

    private ResponseEntity<Void> responder(Resultado r) {
        return switch (r) {
            case HECHO -> ResponseEntity.noContent().build();
            case NO_EXISTE -> ResponseEntity.notFound().build();
            case CONFLICTO -> ResponseEntity.status(HttpStatus.CONFLICT).build();
        };
    }
}
```

`src/test/java/imperio/biblioteca/LibroControllerTest.java`

```java
package imperio.biblioteca;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class LibroControllerTest {
    @Autowired
    private MockMvc mvc;

    @Test
    void listaYBusca() throws Exception {
        mvc.perform(get("/libros")).andExpect(status().isOk()).andExpect(jsonPath("$.length()").value(3))
                .andExpect(jsonPath("$[1].autor").value("Jorge Luis Borges"));
        mvc.perform(get("/libros/3")).andExpect(jsonPath("$.titulo").value("El túnel"));
        mvc.perform(get("/libros/40")).andExpect(status().isNotFound());
    }

    @Test
    void creaSinPrestar() throws Exception {
        mvc.perform(post("/libros").contentType(MediaType.APPLICATION_JSON).content("""
                        {"titulo": "Zama", "autor": "Antonio Di Benedetto", "anio": 1956, "prestado": true}
                        """))
                .andExpect(status().isCreated())
                .andExpect(header().string("Location", "/libros/4"))
                .andExpect(jsonPath("$.prestado").value(false));
    }

    @Test
    void prestaYDevuelveConSusConflictos() throws Exception {
        mvc.perform(post("/libros/1/prestamo")).andExpect(status().isNoContent());
        mvc.perform(get("/libros/1")).andExpect(jsonPath("$.prestado").value(true));
        mvc.perform(post("/libros/1/prestamo")).andExpect(status().isConflict());
        mvc.perform(delete("/libros/1/prestamo")).andExpect(status().isNoContent());
        mvc.perform(delete("/libros/1/prestamo")).andExpect(status().isConflict());
        mvc.perform(post("/libros/99/prestamo")).andExpect(status().isNotFound());
    }
}
```

### Misión R05-N04-M2 · El catálogo con filtros

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Hacé `GET /productos` para el catálogo de una tienda (al menos 8 productos en memoria:
`record Producto(long id, String nombre, String rubro, double precio, int stock)`),
con parámetros **opcionales** que se combinan:

- `rubro` — solo ese rubro.
- `max` — precio máximo.
- `conStock` — `true` para dejar solo los que tienen stock.
- `orden` — `precio` (de menor a mayor) o `nombre` (por defecto, `id`).

Además, `GET /productos/resumen` devuelve un objeto con la cantidad de productos, el
precio promedio y los rubros distintos (un `record Resumen`). Probá varias combinaciones
de filtros con `MockMvc`.

#### Criterio de aprobación

- Los filtros son opcionales y se combinan (`@RequestParam(required = false)` o con `defaultValue`).
- El filtrado usa streams en el servicio y las pruebas cubren al menos 4 combinaciones.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>catalogo</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/catalogo/CatalogoApplication.java`

```java
package imperio.catalogo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class CatalogoApplication {
    public static void main(String[] args) {
        SpringApplication.run(CatalogoApplication.class, args);
    }
}
```

`src/main/java/imperio/catalogo/Producto.java`

```java
package imperio.catalogo;

public record Producto(long id, String nombre, String rubro, double precio, int stock) {
}
```

`src/main/java/imperio/catalogo/Resumen.java`

```java
package imperio.catalogo;

import java.util.List;

public record Resumen(int cantidad, double precioPromedio, List<String> rubros) {
}
```

`src/main/java/imperio/catalogo/ServicioCatalogo.java`

```java
package imperio.catalogo;

import java.util.Comparator;
import java.util.List;

import org.springframework.stereotype.Service;

@Service
public class ServicioCatalogo {
    private final List<Producto> productos = List.of(
            new Producto(1, "Yerba", "almacén", 4200, 20), new Producto(2, "Lavandina", "limpieza", 900, 3),
            new Producto(3, "Aceite", "almacén", 2890, 0), new Producto(4, "Detergente", "limpieza", 1600, 12),
            new Producto(5, "Queso", "fiambrería", 9800, 4), new Producto(6, "Jamón", "fiambrería", 12500, 0),
            new Producto(7, "Arroz", "almacén", 1450, 30), new Producto(8, "Esponja", "limpieza", 600, 25));

    public List<Producto> buscar(String rubro, Double max, boolean conStock, String orden) {
        Comparator<Producto> comparador = switch (orden) {
            case "precio" -> Comparator.comparingDouble(Producto::precio);
            case "nombre" -> Comparator.comparing(Producto::nombre);
            default -> Comparator.comparingLong(Producto::id);
        };
        return productos.stream()
                .filter(p -> rubro == null || p.rubro().equals(rubro))
                .filter(p -> max == null || p.precio() <= max)
                .filter(p -> !conStock || p.stock() > 0)
                .sorted(comparador)
                .toList();
    }

    public Resumen resumen() {
        double promedio = productos.stream().mapToDouble(Producto::precio).average().orElse(0);
        List<String> rubros = productos.stream().map(Producto::rubro).distinct().sorted().toList();
        return new Resumen(productos.size(), Math.round(promedio * 100) / 100.0, rubros);
    }
}
```

`src/main/java/imperio/catalogo/ProductoController.java`

```java
package imperio.catalogo;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/productos")
public class ProductoController {
    private final ServicioCatalogo servicio;

    public ProductoController(ServicioCatalogo servicio) {
        this.servicio = servicio;
    }

    @GetMapping
    public List<Producto> buscar(@RequestParam(required = false) String rubro,
                                 @RequestParam(required = false) Double max,
                                 @RequestParam(defaultValue = "false") boolean conStock,
                                 @RequestParam(defaultValue = "id") String orden) {
        return servicio.buscar(rubro, max, conStock, orden);
    }

    @GetMapping("/resumen")
    public Resumen resumen() {
        return servicio.resumen();
    }
}
```

`src/test/java/imperio/catalogo/ProductoControllerTest.java`

```java
package imperio.catalogo;

import static org.hamcrest.Matchers.contains;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class ProductoControllerTest {
    @Autowired
    private MockMvc mvc;

    @Test
    void sinFiltrosTraeTodosPorId() throws Exception {
        mvc.perform(get("/productos")).andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(8))
                .andExpect(jsonPath("$[0].nombre").value("Yerba"));
    }

    @Test
    void filtraPorRubroYOrdenaPorPrecio() throws Exception {
        mvc.perform(get("/productos").param("rubro", "limpieza").param("orden", "precio"))
                .andExpect(jsonPath("$[*].nombre", contains("Esponja", "Lavandina", "Detergente")));
    }

    @Test
    void combinaPrecioMaximoYStock() throws Exception {
        mvc.perform(get("/productos").param("max", "3000").param("conStock", "true").param("orden", "nombre"))
                .andExpect(jsonPath("$[*].nombre", contains("Arroz", "Detergente", "Esponja", "Lavandina")));
    }

    @Test
    void fiambreriaBarataNoHay() throws Exception {
        mvc.perform(get("/productos").param("rubro", "fiambrería").param("max", "9000"))
                .andExpect(jsonPath("$.length()").value(0));
    }

    @Test
    void elResumen() throws Exception {
        mvc.perform(get("/productos/resumen"))
                .andExpect(jsonPath("$.cantidad").value(8))
                .andExpect(jsonPath("$.precioPromedio").value(4242.5))
                .andExpect(jsonPath("$.rubros", contains("almacén", "fiambrería", "limpieza")));
    }
}
```

### Misión R05-N04-M3 · Las tareas del taller

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Un taller mecánico quiere una API para sus órdenes de trabajo (`record Orden(Long id,
String patente, String trabajo, String estado)`, con estado `PENDIENTE`, `EN_CURSO` o
`TERMINADA` como `enum`). Rutas:

- `POST /ordenes` — crea una orden `PENDIENTE` (201).
- `GET /ordenes?estado=…` — lista, filtrando por estado si viene.
- `PATCH /ordenes/{id}/avanzar` — pasa al estado siguiente (`PENDIENTE` → `EN_CURSO` →
  `TERMINADA`); 409 si ya estaba terminada; 404 si no existe.
- `PUT /ordenes/{id}` — cambia patente y trabajo (no el estado); 409 si está terminada.

Probalo con `MockMvc`.

#### Criterio de aprobación

- El estado es un `enum` y el avance se decide en el servicio con un `switch`.
- Las pruebas recorren el ciclo completo de una orden y los 404/409.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>taller</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/taller/TallerApplication.java`

```java
package imperio.taller;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TallerApplication {
    public static void main(String[] args) {
        SpringApplication.run(TallerApplication.class, args);
    }
}
```

`src/main/java/imperio/taller/Estado.java`

```java
package imperio.taller;

public enum Estado { PENDIENTE, EN_CURSO, TERMINADA }
```

`src/main/java/imperio/taller/Orden.java`

```java
package imperio.taller;

public record Orden(Long id, String patente, String trabajo, Estado estado) {
    public Orden con(Estado nuevo) {
        return new Orden(id, patente, trabajo, nuevo);
    }
}
```

`src/main/java/imperio/taller/Conflicto.java`

```java
package imperio.taller;

public class Conflicto extends RuntimeException {
    public Conflicto(String mensaje) {
        super(mensaje);
    }
}
```

`src/main/java/imperio/taller/ServicioOrdenes.java`

```java
package imperio.taller;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.stereotype.Service;

@Service
public class ServicioOrdenes {
    private final Map<Long, Orden> ordenes = new ConcurrentHashMap<>();
    private final AtomicLong proximoId = new AtomicLong(1);

    public Orden crear(String patente, String trabajo) {
        Orden orden = new Orden(proximoId.getAndIncrement(), patente, trabajo, Estado.PENDIENTE);
        ordenes.put(orden.id(), orden);
        return orden;
    }

    public List<Orden> listar(Estado estado) {
        return ordenes.values().stream()
                .filter(o -> estado == null || o.estado() == estado)
                .sorted(Comparator.comparing(Orden::id))
                .toList();
    }

    public synchronized Optional<Orden> avanzar(long id) {
        return Optional.ofNullable(ordenes.get(id)).map(o -> {
            Estado siguiente = switch (o.estado()) {
                case PENDIENTE -> Estado.EN_CURSO;
                case EN_CURSO -> Estado.TERMINADA;
                case TERMINADA -> throw new Conflicto("la orden " + id + " ya está terminada");
            };
            Orden nueva = o.con(siguiente);
            ordenes.put(id, nueva);
            return nueva;
        });
    }

    public synchronized Optional<Orden> modificar(long id, String patente, String trabajo) {
        return Optional.ofNullable(ordenes.get(id)).map(o -> {
            if (o.estado() == Estado.TERMINADA) {
                throw new Conflicto("no se modifica una orden terminada");
            }
            Orden nueva = new Orden(id, patente, trabajo, o.estado());
            ordenes.put(id, nueva);
            return nueva;
        });
    }
}
```

`src/main/java/imperio/taller/OrdenController.java`

```java
package imperio.taller;

import java.net.URI;
import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/ordenes")
public class OrdenController {
    private final ServicioOrdenes servicio;

    public OrdenController(ServicioOrdenes servicio) {
        this.servicio = servicio;
    }

    @PostMapping
    public ResponseEntity<Orden> crear(@RequestBody Orden datos) {
        Orden creada = servicio.crear(datos.patente(), datos.trabajo());
        return ResponseEntity.created(URI.create("/ordenes/" + creada.id())).body(creada);
    }

    @GetMapping
    public List<Orden> listar(@RequestParam(required = false) Estado estado) {
        return servicio.listar(estado);
    }

    @PatchMapping("/{id}/avanzar")
    public ResponseEntity<Orden> avanzar(@PathVariable long id) {
        return servicio.avanzar(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PutMapping("/{id}")
    public ResponseEntity<Orden> modificar(@PathVariable long id, @RequestBody Orden datos) {
        return servicio.modificar(id, datos.patente(), datos.trabajo()).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    // Una excepción del servicio se convierte en un 409.
    @ExceptionHandler(Conflicto.class)
    public ResponseEntity<String> conflicto(Conflicto e) {
        return ResponseEntity.status(HttpStatus.CONFLICT).body(e.getMessage());
    }
}
```

`src/test/java/imperio/taller/OrdenControllerTest.java`

```java
package imperio.taller;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class OrdenControllerTest {
    @Autowired
    private MockMvc mvc;

    private void crear(String patente, String trabajo) throws Exception {
        mvc.perform(post("/ordenes").contentType(MediaType.APPLICATION_JSON)
                        .content("{\"patente\": \"" + patente + "\", \"trabajo\": \"" + trabajo + "\"}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.estado").value("PENDIENTE"));
    }

    @Test
    void elCicloCompletoDeUnaOrden() throws Exception {
        crear("AB123CD", "cambio de aceite");
        mvc.perform(patch("/ordenes/1/avanzar")).andExpect(jsonPath("$.estado").value("EN_CURSO"));
        mvc.perform(put("/ordenes/1").contentType(MediaType.APPLICATION_JSON).content("""
                        {"patente": "AB123CD", "trabajo": "aceite y filtros"}
                        """))
                .andExpect(jsonPath("$.trabajo").value("aceite y filtros"))
                .andExpect(jsonPath("$.estado").value("EN_CURSO"));
        mvc.perform(patch("/ordenes/1/avanzar")).andExpect(jsonPath("$.estado").value("TERMINADA"));
        mvc.perform(patch("/ordenes/1/avanzar")).andExpect(status().isConflict())
                .andExpect(content().string("la orden 1 ya está terminada"));
        mvc.perform(put("/ordenes/1").contentType(MediaType.APPLICATION_JSON).content("""
                        {"patente": "ZZ999ZZ", "trabajo": "otro"}
                        """))
                .andExpect(status().isConflict());
    }

    @Test
    void filtraPorEstadoYContesta404() throws Exception {
        crear("AA111AA", "frenos");
        crear("BB222BB", "embrague");
        mvc.perform(patch("/ordenes/2/avanzar"));
        mvc.perform(get("/ordenes").param("estado", "PENDIENTE"))
                .andExpect(jsonPath("$.length()").value(1))
                .andExpect(jsonPath("$[0].patente").value("AA111AA"));
        mvc.perform(get("/ordenes")).andExpect(jsonPath("$.length()").value(2));
        mvc.perform(patch("/ordenes/7/avanzar")).andExpect(status().isNotFound());
    }
}
```

### Encargo R05-N04-E1 · El turnero del consultorio

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Un consultorio atiende de 9 a 12, con turnos cada 30 minutos (`09:00`, `09:30`, …,
`11:30`). Hacé la API:

- `GET /turnos/{fecha}/libres` — los horarios libres de ese día (fecha `AAAA-MM-DD`).
- `POST /turnos` con `{"fecha", "hora", "paciente"}` — reserva: 201; **409** si el horario
  ya está tomado; **400** si la hora no es uno de los horarios del consultorio.
- `DELETE /turnos/{fecha}/{hora}` — cancela: 204, o 404 si no había turno.

Guardá los turnos en un `ConcurrentHashMap` (la clave puede ser `fecha + " " + hora`) y
usá `putIfAbsent` para que dos pedidos simultáneos no reserven el mismo horario.
Probalo con `MockMvc`.

#### Criterio de aprobación

- La reserva usa una operación atómica (`putIfAbsent`) y responde 201, 400 o 409.
- Las pruebas cubren reservar, el horario tomado, la hora inválida, los libres y cancelar.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>turnero</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/turnero/TurneroApplication.java`

```java
package imperio.turnero;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TurneroApplication {
    public static void main(String[] args) {
        SpringApplication.run(TurneroApplication.class, args);
    }
}
```

`src/main/java/imperio/turnero/Turno.java`

```java
package imperio.turnero;

public record Turno(String fecha, String hora, String paciente) {
}
```

`src/main/java/imperio/turnero/ServicioTurnos.java`

```java
package imperio.turnero;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.stereotype.Service;

@Service
public class ServicioTurnos {
    public static final List<String> HORARIOS = List.of("09:00", "09:30", "10:00", "10:30", "11:00", "11:30");

    public enum Reserva { HECHA, HORA_INVALIDA, OCUPADO }

    private final Map<String, Turno> turnos = new ConcurrentHashMap<>();

    public List<String> libres(String fecha) {
        return HORARIOS.stream().filter(h -> !turnos.containsKey(fecha + " " + h)).toList();
    }

    public Reserva reservar(Turno turno) {
        if (!HORARIOS.contains(turno.hora())) {
            return Reserva.HORA_INVALIDA;
        }
        return turnos.putIfAbsent(turno.fecha() + " " + turno.hora(), turno) == null ? Reserva.HECHA : Reserva.OCUPADO;
    }

    public boolean cancelar(String fecha, String hora) {
        return turnos.remove(fecha + " " + hora) != null;
    }
}
```

`src/main/java/imperio/turnero/TurnoController.java`

```java
package imperio.turnero;

import java.net.URI;
import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/turnos")
public class TurnoController {
    private final ServicioTurnos servicio;

    public TurnoController(ServicioTurnos servicio) {
        this.servicio = servicio;
    }

    @GetMapping("/{fecha}/libres")
    public List<String> libres(@PathVariable String fecha) {
        return servicio.libres(fecha);
    }

    @PostMapping
    public ResponseEntity<Turno> reservar(@RequestBody Turno turno) {
        return switch (servicio.reservar(turno)) {
            case HECHA -> ResponseEntity.created(URI.create("/turnos/" + turno.fecha() + "/" + turno.hora())).body(turno);
            case HORA_INVALIDA -> ResponseEntity.badRequest().build();
            case OCUPADO -> ResponseEntity.status(HttpStatus.CONFLICT).build();
        };
    }

    @DeleteMapping("/{fecha}/{hora}")
    public ResponseEntity<Void> cancelar(@PathVariable String fecha, @PathVariable String hora) {
        return servicio.cancelar(fecha, hora) ? ResponseEntity.noContent().build() : ResponseEntity.notFound().build();
    }
}
```

`src/test/java/imperio/turnero/TurnoControllerTest.java`

```java
package imperio.turnero;

import static org.hamcrest.Matchers.contains;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class TurnoControllerTest {
    @Autowired
    private MockMvc mvc;

    private ResultActions reservar(String hora, String paciente) throws Exception {
        return mvc.perform(post("/turnos").contentType(MediaType.APPLICATION_JSON)
                .content("{\"fecha\": \"2026-10-05\", \"hora\": \"" + hora + "\", \"paciente\": \"" + paciente + "\"}"));
    }

    @Test
    void reservaYElHorarioQuedaTomado() throws Exception {
        reservar("09:30", "Ana").andExpect(status().isCreated());
        reservar("09:30", "Leo").andExpect(status().isConflict());
        reservar("11:00", "Leo").andExpect(status().isCreated());
        mvc.perform(get("/turnos/2026-10-05/libres"))
                .andExpect(jsonPath("$", contains("09:00", "10:00", "10:30", "11:30")));
        mvc.perform(get("/turnos/2026-10-06/libres")).andExpect(jsonPath("$.length()").value(6));
    }

    @Test
    void unaHoraFueraDelHorarioEs400() throws Exception {
        reservar("13:00", "Ana").andExpect(status().isBadRequest());
        reservar("09:15", "Ana").andExpect(status().isBadRequest());
    }

    @Test
    void cancelaYLiberaElHorario() throws Exception {
        reservar("10:00", "Ana");
        mvc.perform(delete("/turnos/2026-10-05/10:00")).andExpect(status().isNoContent());
        mvc.perform(delete("/turnos/2026-10-05/10:00")).andExpect(status().isNotFound());
        reservar("10:00", "Leo").andExpect(status().isCreated());
    }
}
```

### Prueba del sello

#### ¿Qué verbo HTTP usás para crear y qué código devolvés?

`POST`, y `201 Created` con la ruta del nuevo en `Location`.

#### ¿Qué diferencia hay entre `@PathVariable` y `@RequestParam`?

`@PathVariable` toma un dato de la ruta (`/heroes/3`); `@RequestParam`, de la consulta (`/heroes?clase=maga`).

#### ¿Para qué sirve `ResponseEntity`?

Para elegir el código de estado y los encabezados de la respuesta, además del cuerpo.

#### ¿Por qué el controlador no debería tener lógica?

Para que las reglas estén en el servicio, se prueben sin HTTP y no se repitan.

#### ¿Qué hace `MockMvc`?

Simula pedidos HTTP a la aplicación sin abrir un puerto, y deja comprobar el código y el JSON de la respuesta.

### Soluciones (docente)

Sale de `19-Java-Avanzado/09-Spring-MVC-REST`. Las pruebas usan `@DirtiesContext` para que cada una arranque con los datos iniciales (los servicios guardan en memoria). Se corrige con `./mvnw test` y probando un par de rutas con `curl`.

## R05-N05 · DTO, validaciones y errores

```meta
tipo: tema
padre: R05-N04
precio: 10
criatura: troll
ejecutable: no
temas: web.api-rest, err.validacion
usa: fw.spring
```

### Crónica

La ventanilla del muelle empezó a recibir cualquier cosa: pedidos sin nombre, cargamentos de peso negativo, correos sin arroba. Y cuando algo fallaba, devolvía un papel con trescientas líneas de error en idioma de máquina. Los mensajeros se iban sin entender nada.

—Una buena ventanilla **controla lo que entra** y **explica lo que sale** —dice {mentor}—. Lo que recibe se revisa antes de tocar nada, lo que devuelve muestra solo lo necesario, y cada error dice qué pasó en palabras que se entienden. Y de paso, vamos a dejar de escribir *getters* a mano, {heroe}.

### Objetivos

- Separar lo que entra y sale de la API (DTO) del modelo interno.
- Validar los datos de entrada con Bean Validation (`@NotBlank`, `@Email`, `@Min`, `@Size`, `@Valid`).
- Centralizar el manejo de errores con `@RestControllerAdvice` y responder con `ProblemDetail`.
- Reducir código repetido con Lombok.

### Antes de empezar

- Servicios REST.

### Explicación

#### DTO: lo que viaja no es lo que se guarda
Un **DTO** (*Data Transfer Object*) es un objeto pensado solo para entrar o salir por la
API. ¿Por qué no devolver directamente el modelo?
- El modelo puede tener datos que **no** tienen que salir (la clave de un usuario, un
  costo interno).
- Lo que se pide al crear no es lo mismo que lo que se devuelve (el `id` lo pone el
  sistema, no el cliente).
- Si cambia el modelo, la API no tiene que cambiar.

```java
public record AlumnoPedido(String nombre, String email, int edad) { }           // lo que entra
public record AlumnoRespuesta(long id, String nombre, String comision) { }      // lo que sale
```
Los `record` son perfectos para los DTO. El servicio convierte de uno a otro.

#### Validar lo que entra
Con `spring-boot-starter-validation`, los DTO se anotan con reglas y el controlador las
hace cumplir con `@Valid`:
```java
public record AlumnoPedido(
        @NotBlank(message = "el nombre es obligatorio") String nombre,
        @NotBlank @Email(message = "el email no es válido") String email,
        @Min(value = 16, message = "la edad mínima es 16") int edad) { }

@PostMapping
public ResponseEntity<AlumnoRespuesta> inscribir(@Valid @RequestBody AlumnoPedido pedido) { … }
```
Si algo no cumple, Spring **no llama** al método y responde `400 Bad Request`.

| Anotación | Exige |
|---|---|
| `@NotNull` | que no sea `null` |
| `@NotBlank` | texto no vacío (ni solo espacios) |
| `@Size(min, max)` | largo de un texto o de una lista |
| `@Min`, `@Max`, `@Positive` | rangos de números |
| `@Email`, `@Pattern(regexp)` | formato |
| `@Past`, `@Future` | fechas |
| `@AssertTrue` | que un método `boolean` dé `true` (reglas entre campos) |

#### Errores claros con `@RestControllerAdvice`
Un `@RestControllerAdvice` atrapa las excepciones de **todos** los controladores y las
convierte en respuestas. Spring trae `ProblemDetail`, un formato estándar para errores
(RFC 9457):
```java
@RestControllerAdvice
public class ManejoDeErrores {
    @ExceptionHandler(NoEncontrado.class)
    public ProblemDetail noEncontrado(NoEncontrado e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail invalido(MethodArgumentNotValidException e) {
        ProblemDetail p = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "datos inválidos");
        Map<String, String> campos = new TreeMap<>();
        e.getBindingResult().getFieldErrors().forEach(f -> campos.put(f.getField(), f.getDefaultMessage()));
        p.setProperty("campos", campos);
        return p;
    }
}
```
La respuesta queda así:
```json
{"type": "about:blank", "title": "Bad Request", "status": 400, "detail": "datos inválidos",
 "instance": "/alumnos", "campos": {"edad": "la edad mínima es 16", "nombre": "el nombre es obligatorio"}}
```
El servicio lanza excepciones propias (`NoEncontrado`, `Conflicto`) y ya no se ocupa de
HTTP; el *advice* decide el código.

#### Lombok: menos código repetido
Las clases del modelo (que no pueden ser `record` porque cambian, como las entidades del
próximo nodo) necesitan constructores, *getters* y *setters*. **Lombok** los genera al
compilar a partir de anotaciones:
| Anotación | Genera |
|---|---|
| `@Getter`, `@Setter` | los *getters* y *setters* |
| `@NoArgsConstructor`, `@AllArgsConstructor` | constructores |
| `@RequiredArgsConstructor` | un constructor con los atributos `final` (ideal para inyectar) |
| `@ToString`, `@EqualsAndHashCode` | esos métodos |
| `@Builder` | un constructor paso a paso: `Alumno.builder().nombre("Ana").edad(20).build()` |

```java
@Service
@RequiredArgsConstructor
public class ServicioAlumnos {
    private final RepositorioAlumnos repositorio;      // Lombok arma el constructor
}
```
Lombok necesita la dependencia en el `pom.xml` y, en el IDE, el plugin de Lombok (IntelliJ
ya lo trae). Desde Java 23 hay que declararlo también como procesador de anotaciones del
compilador: los `pom.xml` de este nodo ya lo hacen.

> **Si venís de Python.** Los DTO con validación se parecen a los modelos de Pydantic en
> FastAPI, y Lombok a los `@dataclass`.

### Código de ejemplo

La inscripción a las comisiones: DTO de entrada y salida, validación, errores con
`ProblemDetail` y el modelo con Lombok.

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>inscripciones</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                            <version>${lombok.version}</version>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/inscripciones/InscripcionesApplication.java`

```java
package imperio.inscripciones;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class InscripcionesApplication {
    public static void main(String[] args) {
        SpringApplication.run(InscripcionesApplication.class, args);
    }
}
```

`src/main/java/imperio/inscripciones/Alumno.java`

```java
package imperio.inscripciones;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

// El modelo interno: tiene el DNI, que nunca sale por la API.
@Getter
@Setter
@AllArgsConstructor
public class Alumno {
    private long id;
    private String nombre;
    private String email;
    private String dni;
    private String comision;
}
```

`src/main/java/imperio/inscripciones/AlumnoPedido.java`

```java
package imperio.inscripciones;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;

public record AlumnoPedido(
        @NotBlank(message = "el nombre es obligatorio") String nombre,
        @NotBlank(message = "el email es obligatorio") @Email(message = "el email no es válido") String email,
        @Pattern(regexp = "\\d{7,8}", message = "el DNI tiene que tener 7 u 8 dígitos") String dni,
        @Pattern(regexp = "[A-C]", message = "la comisión es A, B o C") String comision) {
}
```

`src/main/java/imperio/inscripciones/AlumnoRespuesta.java`

```java
package imperio.inscripciones;

public record AlumnoRespuesta(long id, String nombre, String email, String comision) {
    static AlumnoRespuesta de(Alumno a) {
        return new AlumnoRespuesta(a.getId(), a.getNombre(), a.getEmail(), a.getComision());
    }
}
```

`src/main/java/imperio/inscripciones/NoEncontrado.java`

```java
package imperio.inscripciones;

public class NoEncontrado extends RuntimeException {
    public NoEncontrado(String mensaje) {
        super(mensaje);
    }
}
```

`src/main/java/imperio/inscripciones/Conflicto.java`

```java
package imperio.inscripciones;

public class Conflicto extends RuntimeException {
    public Conflicto(String mensaje) {
        super(mensaje);
    }
}
```

`src/main/java/imperio/inscripciones/ServicioInscripciones.java`

```java
package imperio.inscripciones;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.stereotype.Service;

@Service
public class ServicioInscripciones {
    private final Map<Long, Alumno> alumnos = new ConcurrentHashMap<>();
    private final AtomicLong proximoId = new AtomicLong(1);

    public synchronized Alumno inscribir(AlumnoPedido pedido) {
        boolean repetido = alumnos.values().stream().anyMatch(a -> a.getDni().equals(pedido.dni()));
        if (repetido) {
            throw new Conflicto("ya hay un alumno con el DNI " + pedido.dni());
        }
        Alumno alumno = new Alumno(proximoId.getAndIncrement(), pedido.nombre(), pedido.email(), pedido.dni(), pedido.comision());
        alumnos.put(alumno.getId(), alumno);
        return alumno;
    }

    public Alumno buscar(long id) {
        Alumno a = alumnos.get(id);
        if (a == null) {
            throw new NoEncontrado("no existe el alumno " + id);
        }
        return a;
    }
}
```

`src/main/java/imperio/inscripciones/AlumnoController.java`

```java
package imperio.inscripciones;

import java.net.URI;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/alumnos")
@RequiredArgsConstructor
public class AlumnoController {
    private final ServicioInscripciones servicio;

    @PostMapping
    public ResponseEntity<AlumnoRespuesta> inscribir(@Valid @RequestBody AlumnoPedido pedido) {
        Alumno a = servicio.inscribir(pedido);
        return ResponseEntity.created(URI.create("/alumnos/" + a.getId())).body(AlumnoRespuesta.de(a));
    }

    @GetMapping("/{id}")
    public AlumnoRespuesta buscar(@PathVariable long id) {
        return AlumnoRespuesta.de(servicio.buscar(id));
    }
}
```

`src/main/java/imperio/inscripciones/ManejoDeErrores.java`

```java
package imperio.inscripciones;

import java.util.Map;
import java.util.TreeMap;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ManejoDeErrores {
    @ExceptionHandler(NoEncontrado.class)
    public ProblemDetail noEncontrado(NoEncontrado e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
    }

    @ExceptionHandler(Conflicto.class)
    public ProblemDetail conflicto(Conflicto e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail invalido(MethodArgumentNotValidException e) {
        ProblemDetail p = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "datos inválidos");
        Map<String, String> campos = new TreeMap<>();
        e.getBindingResult().getFieldErrors().forEach(f -> campos.putIfAbsent(f.getField(), f.getDefaultMessage()));
        p.setProperty("campos", campos);
        return p;
    }
}
```

`src/test/java/imperio/inscripciones/AlumnoControllerTest.java`

```java
package imperio.inscripciones;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class AlumnoControllerTest {
    @Autowired
    private MockMvc mvc;

    private ResultActions inscribir(String json) throws Exception {
        return mvc.perform(post("/alumnos").contentType(MediaType.APPLICATION_JSON).content(json));
    }

    @Test
    void inscribeYNoDevuelveElDni() throws Exception {
        inscribir("""
                {"nombre": "Ana Ruiz", "email": "ana@correo.com", "dni": "41222333", "comision": "B"}
                """)
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.comision").value("B"))
                .andExpect(jsonPath("$.dni").doesNotExist());
    }

    @Test
    void losDatosInvalidosDan400ConCadaCampo() throws Exception {
        inscribir("""
                {"nombre": " ", "email": "ana-correo", "dni": "123", "comision": "Z"}
                """)
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.detail").value("datos inválidos"))
                .andExpect(jsonPath("$.campos.nombre").value("el nombre es obligatorio"))
                .andExpect(jsonPath("$.campos.email").value("el email no es válido"))
                .andExpect(jsonPath("$.campos.dni").value("el DNI tiene que tener 7 u 8 dígitos"))
                .andExpect(jsonPath("$.campos.comision").value("la comisión es A, B o C"));
    }

    @Test
    void elDniRepetidoEs409YElInexistente404() throws Exception {
        String ana = """
                {"nombre": "Ana Ruiz", "email": "ana@correo.com", "dni": "41222333", "comision": "B"}
                """;
        inscribir(ana).andExpect(status().isCreated());
        inscribir(ana).andExpect(status().isConflict())
                .andExpect(jsonPath("$.detail").value("ya hay un alumno con el DNI 41222333"));
        mvc.perform(get("/alumnos/9")).andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status").value(404));
    }
}
```

Un pedido inválido contesta:

```
$ curl -s localhost:8080/alumnos -H "Content-Type: application/json" -d '{"nombre":"","email":"x","dni":"1","comision":"A"}'
{"type":"about:blank","title":"Bad Request","status":400,"detail":"datos inválidos","instance":"/alumnos",
 "campos":{"dni":"el DNI tiene que tener 7 u 8 dígitos","email":"el email no es válido","nombre":"el nombre es obligatorio"}}
```

### ¿Para qué sirve?

Una API pública recibe datos de cualquiera: validar en la entrada evita basura en la base y agujeros de seguridad. Los errores claros y uniformes le ahorran horas al equipo que arma la app o la página que usa tu API. Y los DTO evitan el clásico error de filtrar datos privados (claves, documentos) en una respuesta.

### Errores habituales

**Troll: el `@Valid` olvidado.** Las anotaciones del DTO no hacen nada si el parámetro no
tiene `@Valid`: los datos inválidos entran igual.

**Ogro: devolver la entidad.** Devolver el modelo interno expone todos sus campos
(claves, DNI, costos). Devolvé un DTO de respuesta.

**Goblin: el `@NotNull` en un `int`.** Un `int` nunca es `null`: si falta en el JSON vale
`0`. Para exigir que venga, usá `Integer` con `@NotNull`, o un `@Min`.

**Ogro: el `try`/`catch` en cada controlador.** Repetir el manejo de errores en cada
método. Lanzá excepciones propias desde el servicio y convertilas en un solo
`@RestControllerAdvice`.

**Slime: Lombok que no genera nada.** `cannot find symbol: method getNombre()`: falta el
plugin de Lombok en el IDE, o (desde Java 23) el procesador de anotaciones en el
`pom.xml`.

### Misión R05-N05-M1 · El registro de usuarios

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Hacé `POST /usuarios` para registrar usuarios con un DTO `RegistroPedido`: `usuario`
(3 a 20 letras, números o guion bajo), `email` (válido), `clave` (al menos 8
caracteres) y `fechaNacimiento` (`LocalDate`, en el pasado). La respuesta es un
`UsuarioRespuesta` **sin la clave**. El servicio guarda la clave **cifrada** (para esta
misión alcanza con el SHA-256 en hexadecimal) en el modelo `Usuario` hecho con Lombok, y
lanza un conflicto si el usuario o el email ya existen. Los errores salen como
`ProblemDetail` con los campos inválidos. `GET /usuarios/{usuario}` devuelve el usuario o
404.

#### Criterio de aprobación

- Validaciones con Bean Validation y `@Valid`; la clave nunca aparece en una respuesta.
- Errores 400 (con campos), 404 y 409 desde un `@RestControllerAdvice`.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>usuarios</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                            <version>${lombok.version}</version>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/usuarios/UsuariosApplication.java`

```java
package imperio.usuarios;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class UsuariosApplication {
    public static void main(String[] args) {
        SpringApplication.run(UsuariosApplication.class, args);
    }
}
```

`src/main/java/imperio/usuarios/Usuario.java`

```java
package imperio.usuarios;

import java.time.LocalDate;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class Usuario {
    private final String usuario;
    private final String email;
    private final String claveCifrada;
    private final LocalDate fechaNacimiento;
}
```

`src/main/java/imperio/usuarios/RegistroPedido.java`

```java
package imperio.usuarios;

import java.time.LocalDate;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Past;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

public record RegistroPedido(
        @NotNull(message = "el usuario es obligatorio")
        @Pattern(regexp = "\\w{3,20}", message = "el usuario lleva de 3 a 20 letras, números o _") String usuario,
        @NotBlank(message = "el email es obligatorio") @Email(message = "el email no es válido") String email,
        @NotNull(message = "la clave es obligatoria") @Size(min = 8, message = "la clave necesita al menos 8 caracteres") String clave,
        @NotNull(message = "la fecha de nacimiento es obligatoria") @Past(message = "la fecha de nacimiento tiene que ser pasada") LocalDate fechaNacimiento) {
}
```

`src/main/java/imperio/usuarios/UsuarioRespuesta.java`

```java
package imperio.usuarios;

import java.time.LocalDate;

public record UsuarioRespuesta(String usuario, String email, LocalDate fechaNacimiento) {
    static UsuarioRespuesta de(Usuario u) {
        return new UsuarioRespuesta(u.getUsuario(), u.getEmail(), u.getFechaNacimiento());
    }
}
```

`src/main/java/imperio/usuarios/NoEncontrado.java`

```java
package imperio.usuarios;

public class NoEncontrado extends RuntimeException {
    public NoEncontrado(String mensaje) {
        super(mensaje);
    }
}
```

`src/main/java/imperio/usuarios/Conflicto.java`

```java
package imperio.usuarios;

public class Conflicto extends RuntimeException {
    public Conflicto(String mensaje) {
        super(mensaje);
    }
}
```

`src/main/java/imperio/usuarios/ServicioUsuarios.java`

```java
package imperio.usuarios;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.stereotype.Service;

@Service
public class ServicioUsuarios {
    private final Map<String, Usuario> usuarios = new ConcurrentHashMap<>();

    public synchronized Usuario registrar(RegistroPedido p) {
        if (usuarios.containsKey(p.usuario())) {
            throw new Conflicto("el usuario " + p.usuario() + " ya existe");
        }
        if (usuarios.values().stream().anyMatch(u -> u.getEmail().equalsIgnoreCase(p.email()))) {
            throw new Conflicto("el email ya está registrado");
        }
        Usuario u = new Usuario(p.usuario(), p.email(), sha256(p.clave()), p.fechaNacimiento());
        usuarios.put(u.getUsuario(), u);
        return u;
    }

    public Usuario buscar(String usuario) {
        Usuario u = usuarios.get(usuario);
        if (u == null) {
            throw new NoEncontrado("no existe el usuario " + usuario);
        }
        return u;
    }

    static String sha256(String texto) {
        try {
            byte[] hash = MessageDigest.getInstance("SHA-256").digest(texto.getBytes(StandardCharsets.UTF_8));
            return HexFormat.of().formatHex(hash);
        } catch (NoSuchAlgorithmException e) {
            throw new IllegalStateException(e);
        }
    }
}
```

`src/main/java/imperio/usuarios/UsuarioController.java`

```java
package imperio.usuarios;

import java.net.URI;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/usuarios")
@RequiredArgsConstructor
public class UsuarioController {
    private final ServicioUsuarios servicio;

    @PostMapping
    public ResponseEntity<UsuarioRespuesta> registrar(@Valid @RequestBody RegistroPedido pedido) {
        Usuario u = servicio.registrar(pedido);
        return ResponseEntity.created(URI.create("/usuarios/" + u.getUsuario())).body(UsuarioRespuesta.de(u));
    }

    @GetMapping("/{usuario}")
    public UsuarioRespuesta buscar(@PathVariable String usuario) {
        return UsuarioRespuesta.de(servicio.buscar(usuario));
    }
}
```

`src/main/java/imperio/usuarios/ManejoDeErrores.java`

```java
package imperio.usuarios;

import java.util.Map;
import java.util.TreeMap;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ManejoDeErrores {
    @ExceptionHandler(NoEncontrado.class)
    public ProblemDetail noEncontrado(NoEncontrado e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
    }

    @ExceptionHandler(Conflicto.class)
    public ProblemDetail conflicto(Conflicto e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail invalido(MethodArgumentNotValidException e) {
        ProblemDetail p = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "datos inválidos");
        Map<String, String> campos = new TreeMap<>();
        e.getBindingResult().getFieldErrors().forEach(f -> campos.putIfAbsent(f.getField(), f.getDefaultMessage()));
        p.setProperty("campos", campos);
        return p;
    }
}
```

`src/test/java/imperio/usuarios/UsuarioControllerTest.java`

```java
package imperio.usuarios;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class UsuarioControllerTest {
    @Autowired
    private MockMvc mvc;

    @Autowired
    private ServicioUsuarios servicio;

    private ResultActions registrar(String json) throws Exception {
        return mvc.perform(post("/usuarios").contentType(MediaType.APPLICATION_JSON).content(json));
    }

    private static final String KIRA = """
            {"usuario": "kira_07", "email": "kira@correo.com", "clave": "flechas123", "fechaNacimiento": "2004-05-17"}
            """;

    @Test
    void registraSinDevolverLaClaveYLaGuardaCifrada() throws Exception {
        registrar(KIRA).andExpect(status().isCreated())
                .andExpect(jsonPath("$.usuario").value("kira_07"))
                .andExpect(jsonPath("$.clave").doesNotExist())
                .andExpect(jsonPath("$.claveCifrada").doesNotExist());
        assertEquals(64, servicio.buscar("kira_07").getClaveCifrada().length());
        mvc.perform(get("/usuarios/kira_07")).andExpect(jsonPath("$.fechaNacimiento").value("2004-05-17"));
    }

    @Test
    void validaCadaCampo() throws Exception {
        registrar("""
                {"usuario": "k!", "email": "kira", "clave": "corta", "fechaNacimiento": "2999-01-01"}
                """)
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.usuario").value("el usuario lleva de 3 a 20 letras, números o _"))
                .andExpect(jsonPath("$.campos.email").value("el email no es válido"))
                .andExpect(jsonPath("$.campos.clave").value("la clave necesita al menos 8 caracteres"))
                .andExpect(jsonPath("$.campos.fechaNacimiento").value("la fecha de nacimiento tiene que ser pasada"));
    }

    @Test
    void usuarioOEmailRepetidosDan409() throws Exception {
        registrar(KIRA).andExpect(status().isCreated());
        registrar(KIRA).andExpect(status().isConflict()).andExpect(jsonPath("$.detail").value("el usuario kira_07 ya existe"));
        registrar("""
                {"usuario": "otra", "email": "KIRA@correo.com", "clave": "flechas123", "fechaNacimiento": "2004-05-17"}
                """).andExpect(status().isConflict()).andExpect(jsonPath("$.detail").value("el email ya está registrado"));
        mvc.perform(get("/usuarios/nadie")).andExpect(status().isNotFound());
    }
}
```

### Misión R05-N05-M2 · El presupuesto con Lombok

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Un corralón arma presupuestos. Modelá con Lombok un `Presupuesto` (con `@Builder`,
`@Getter` y `@ToString`) que tiene cliente, una lista de `Item` (también con Lombok:
material, cantidad, precio unitario) y un descuento en porcentaje, con un método
`total()`. Hacé `POST /presupuestos` que recibe un DTO con validaciones **anidadas**: el
cliente es obligatorio, la lista de ítems no puede estar vacía (`@NotEmpty`) y **cada**
ítem se valida (`@Valid` en la lista: cantidad positiva, precio positivo); el descuento
va de 0 a 30. La respuesta trae el total calculado. Los errores de los ítems tienen que
indicar cuál (por ejemplo `items[1].cantidad`).

#### Criterio de aprobación

- El modelo usa Lombok (`@Builder`, `@Getter`) y el servicio `@RequiredArgsConstructor` o nada que inyectar.
- La validación anidada informa el ítem y el campo que fallan.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>corralon</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                            <version>${lombok.version}</version>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/corralon/CorralonApplication.java`

```java
package imperio.corralon;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class CorralonApplication {
    public static void main(String[] args) {
        SpringApplication.run(CorralonApplication.class, args);
    }
}
```

`src/main/java/imperio/corralon/Item.java`

```java
package imperio.corralon;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.ToString;

@Getter
@AllArgsConstructor
@ToString
public class Item {
    private final String material;
    private final int cantidad;
    private final double precioUnitario;

    public double subtotal() {
        return cantidad * precioUnitario;
    }
}
```

`src/main/java/imperio/corralon/Presupuesto.java`

```java
package imperio.corralon;

import java.util.List;

import lombok.Builder;
import lombok.Getter;
import lombok.Singular;
import lombok.ToString;

@Getter
@Builder
@ToString
public class Presupuesto {
    private final String cliente;
    @Singular
    private final List<Item> items;
    private final int descuento;

    public double total() {
        double bruto = items.stream().mapToDouble(Item::subtotal).sum();
        return Math.round(bruto * (100 - descuento)) / 100.0;
    }
}
```

`src/main/java/imperio/corralon/PresupuestoPedido.java`

```java
package imperio.corralon;

import java.util.List;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Positive;

public record PresupuestoPedido(
        @NotBlank(message = "el cliente es obligatorio") String cliente,
        @NotEmpty(message = "el presupuesto necesita al menos un ítem") List<@Valid ItemPedido> items,
        @Min(value = 0, message = "el descuento va de 0 a 30") @Max(value = 30, message = "el descuento va de 0 a 30") int descuento) {

    public record ItemPedido(
            @NotBlank(message = "falta el material") String material,
            @Positive(message = "la cantidad tiene que ser positiva") int cantidad,
            @Positive(message = "el precio tiene que ser positivo") double precioUnitario) {
    }
}
```

`src/main/java/imperio/corralon/PresupuestoRespuesta.java`

```java
package imperio.corralon;

public record PresupuestoRespuesta(String cliente, int items, int descuento, double total) {
    static PresupuestoRespuesta de(Presupuesto p) {
        return new PresupuestoRespuesta(p.getCliente(), p.getItems().size(), p.getDescuento(), p.total());
    }
}
```

`src/main/java/imperio/corralon/PresupuestoController.java`

```java
package imperio.corralon;

import java.util.Map;
import java.util.TreeMap;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/presupuestos")
public class PresupuestoController {
    @PostMapping
    public PresupuestoRespuesta armar(@Valid @RequestBody PresupuestoPedido pedido) {
        Presupuesto.PresupuestoBuilder b = Presupuesto.builder().cliente(pedido.cliente()).descuento(pedido.descuento());
        pedido.items().forEach(i -> b.item(new Item(i.material(), i.cantidad(), i.precioUnitario())));
        return PresupuestoRespuesta.de(b.build());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail invalido(MethodArgumentNotValidException e) {
        ProblemDetail p = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "datos inválidos");
        Map<String, String> campos = new TreeMap<>();
        e.getBindingResult().getFieldErrors().forEach(f -> campos.putIfAbsent(f.getField(), f.getDefaultMessage()));
        p.setProperty("campos", campos);
        return p;
    }
}
```

`src/test/java/imperio/corralon/PresupuestoTest.java`

```java
package imperio.corralon;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class PresupuestoTest {
    @Autowired
    private MockMvc mvc;

    @Test
    void elBuilderYElTotal() {
        Presupuesto p = Presupuesto.builder().cliente("Obra Ruiz").descuento(10)
                .item(new Item("cemento", 10, 9500)).item(new Item("arena m3", 2, 30000)).build();
        assertEquals(139500.0, p.total());
    }

    @Test
    void armaElPresupuesto() throws Exception {
        mvc.perform(post("/presupuestos").contentType(MediaType.APPLICATION_JSON).content("""
                        {"cliente": "Obra Ruiz", "descuento": 10, "items": [
                          {"material": "cemento", "cantidad": 10, "precioUnitario": 9500},
                          {"material": "arena m3", "cantidad": 2, "precioUnitario": 30000}]}
                        """))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.items").value(2))
                .andExpect(jsonPath("$.total").value(139500.0));
    }

    @Test
    void validaCadaItemYDiceCual() throws Exception {
        mvc.perform(post("/presupuestos").contentType(MediaType.APPLICATION_JSON).content("""
                        {"cliente": "", "descuento": 45, "items": [
                          {"material": "cemento", "cantidad": 10, "precioUnitario": 9500},
                          {"material": "", "cantidad": 0, "precioUnitario": 30000}]}
                        """))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.cliente").value("el cliente es obligatorio"))
                .andExpect(jsonPath("$.campos.descuento").value("el descuento va de 0 a 30"))
                .andExpect(jsonPath("$.campos['items[1].cantidad']").value("la cantidad tiene que ser positiva"))
                .andExpect(jsonPath("$.campos['items[1].material']").value("falta el material"));
    }

    @Test
    void sinItemsNoHayPresupuesto() throws Exception {
        mvc.perform(post("/presupuestos").contentType(MediaType.APPLICATION_JSON).content("""
                        {"cliente": "Obra Ruiz", "descuento": 0, "items": []}
                        """))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.items").value("el presupuesto necesita al menos un ítem"));
    }
}
```

### Misión R05-N05-M3 · Las reservas del hotel

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Hacé `POST /reservas` para un hotel con un DTO que tiene `huesped`, `habitacion` (1 a
20), `entrada` y `salida` (`LocalDate`) y `personas` (1 a 4). Además de las validaciones
de cada campo, hay reglas **entre campos**: la salida tiene que ser posterior a la
entrada y la estadía no puede pasar de 14 noches (usá métodos `@AssertTrue` en el
`record`). El servicio rechaza con 409 una reserva que se superpone con otra de la misma
habitación. La respuesta trae el id, las noches y el total (18 000 por noche por
persona, con 10 % de descuento desde 7 noches).

#### Criterio de aprobación

- Las reglas entre campos se validan con `@AssertTrue` y aparecen en los errores.
- La superposición se detecta en el servicio y responde 409.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>hotel</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/hotel/HotelApplication.java`

```java
package imperio.hotel;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class HotelApplication {
    public static void main(String[] args) {
        SpringApplication.run(HotelApplication.class, args);
    }
}
```

`src/main/java/imperio/hotel/ReservaPedido.java`

```java
package imperio.hotel;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.validation.constraints.AssertTrue;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record ReservaPedido(
        @NotBlank(message = "falta el huésped") String huesped,
        @Min(value = 1, message = "las habitaciones van del 1 al 20") @Max(value = 20, message = "las habitaciones van del 1 al 20") int habitacion,
        @NotNull(message = "falta la entrada") LocalDate entrada,
        @NotNull(message = "falta la salida") LocalDate salida,
        @Min(value = 1, message = "de 1 a 4 personas") @Max(value = 4, message = "de 1 a 4 personas") int personas) {

    @JsonIgnore
    @AssertTrue(message = "la salida tiene que ser posterior a la entrada")
    public boolean isFechasEnOrden() {
        return entrada == null || salida == null || salida.isAfter(entrada);
    }

    @JsonIgnore
    @AssertTrue(message = "la estadía máxima es de 14 noches")
    public boolean isEstadiaPermitida() {
        return entrada == null || salida == null || noches() <= 14;
    }

    public long noches() {
        return ChronoUnit.DAYS.between(entrada, salida);
    }
}
```

`src/main/java/imperio/hotel/Reserva.java`

```java
package imperio.hotel;

import java.time.LocalDate;

public record Reserva(long id, String huesped, int habitacion, LocalDate entrada, LocalDate salida, long noches, double total) {
    boolean seSuperponeCon(int otraHabitacion, LocalDate otraEntrada, LocalDate otraSalida) {
        return habitacion == otraHabitacion && otraEntrada.isBefore(salida) && entrada.isBefore(otraSalida);
    }
}
```

`src/main/java/imperio/hotel/Conflicto.java`

```java
package imperio.hotel;

public class Conflicto extends RuntimeException {
    public Conflicto(String mensaje) {
        super(mensaje);
    }
}
```

`src/main/java/imperio/hotel/ServicioReservas.java`

```java
package imperio.hotel;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

@Service
public class ServicioReservas {
    static final double POR_NOCHE_Y_PERSONA = 18000;

    private final List<Reserva> reservas = new ArrayList<>();

    public synchronized Reserva reservar(ReservaPedido p) {
        boolean ocupada = reservas.stream().anyMatch(r -> r.seSuperponeCon(p.habitacion(), p.entrada(), p.salida()));
        if (ocupada) {
            throw new Conflicto("la habitación " + p.habitacion() + " está ocupada en esas fechas");
        }
        long noches = p.noches();
        double total = noches * p.personas() * POR_NOCHE_Y_PERSONA * (noches >= 7 ? 0.9 : 1);
        Reserva r = new Reserva(reservas.size() + 1, p.huesped(), p.habitacion(), p.entrada(), p.salida(), noches, total);
        reservas.add(r);
        return r;
    }
}
```

`src/main/java/imperio/hotel/ReservaController.java`

```java
package imperio.hotel;

import java.util.Map;
import java.util.TreeMap;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/reservas")
public class ReservaController {
    private final ServicioReservas servicio;

    public ReservaController(ServicioReservas servicio) {
        this.servicio = servicio;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Reserva reservar(@Valid @RequestBody ReservaPedido pedido) {
        return servicio.reservar(pedido);
    }

    @ExceptionHandler(Conflicto.class)
    public ProblemDetail conflicto(Conflicto e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail invalido(MethodArgumentNotValidException e) {
        ProblemDetail p = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "datos inválidos");
        Map<String, String> campos = new TreeMap<>();
        e.getBindingResult().getFieldErrors().forEach(f -> campos.putIfAbsent(f.getField(), f.getDefaultMessage()));
        p.setProperty("campos", campos);
        return p;
    }
}
```

`src/test/java/imperio/hotel/ReservaControllerTest.java`

```java
package imperio.hotel;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class ReservaControllerTest {
    @Autowired
    private MockMvc mvc;

    private ResultActions reservar(int habitacion, String entrada, String salida, int personas) throws Exception {
        return mvc.perform(post("/reservas").contentType(MediaType.APPLICATION_JSON).content(
                "{\"huesped\": \"Ana\", \"habitacion\": " + habitacion + ", \"entrada\": \"" + entrada
                        + "\", \"salida\": \"" + salida + "\", \"personas\": " + personas + "}"));
    }

    @Test
    void calculaNochesYTotal() throws Exception {
        reservar(5, "2026-12-20", "2026-12-23", 2).andExpect(status().isCreated())
                .andExpect(jsonPath("$.noches").value(3))
                .andExpect(jsonPath("$.total").value(108000.0));
        reservar(6, "2027-01-02", "2027-01-09", 1).andExpect(jsonPath("$.total").value(113400.0));
    }

    @Test
    void lasReglasEntreCamposSeValidan() throws Exception {
        reservar(5, "2026-12-20", "2026-12-18", 2).andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.fechasEnOrden").value("la salida tiene que ser posterior a la entrada"));
        reservar(5, "2026-12-01", "2026-12-20", 2).andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.estadiaPermitida").value("la estadía máxima es de 14 noches"));
        reservar(25, "2026-12-01", "2026-12-02", 6).andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.habitacion").value("las habitaciones van del 1 al 20"))
                .andExpect(jsonPath("$.campos.personas").value("de 1 a 4 personas"));
    }

    @Test
    void laSuperposicionEs409() throws Exception {
        reservar(5, "2026-12-20", "2026-12-23", 2).andExpect(status().isCreated());
        reservar(5, "2026-12-22", "2026-12-25", 1).andExpect(status().isConflict())
                .andExpect(jsonPath("$.detail").value("la habitación 5 está ocupada en esas fechas"));
        reservar(5, "2026-12-23", "2026-12-25", 1).andExpect(status().isCreated());
        reservar(6, "2026-12-21", "2026-12-22", 1).andExpect(status().isCreated());
    }
}
```

### Encargo R05-N05-E1 · La mesa de ayuda

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Una mesa de ayuda recibe tickets. Hacé la API con DTO y validaciones:

- `POST /tickets` — `titulo` (5 a 80 caracteres), `descripcion` (obligatoria),
  `prioridad` (`BAJA`, `MEDIA` o `ALTA`, un `enum`: un valor inválido da 400) y `email` del
  solicitante. Se crea `ABIERTO`.
- `GET /tickets/{id}` — el ticket (sin el email del solicitante), o 404 con
  `ProblemDetail`.
- `POST /tickets/{id}/respuestas` — agrega una respuesta (`texto` obligatorio); 409 si el
  ticket está cerrado.
- `POST /tickets/{id}/cierre` — lo cierra; 409 si no tiene ninguna respuesta.

El modelo usa Lombok y los errores salen de un `@RestControllerAdvice`.

#### Criterio de aprobación

- DTO de entrada y de salida separados; el email no sale en las respuestas.
- Todos los errores (400, 404, 409) tienen formato `ProblemDetail`, incluido el de la prioridad inválida.

#### Solución de referencia

`pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>

    <groupId>imperio</groupId>
    <artifactId>ayuda</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                            <version>${lombok.version}</version>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
```

`src/main/java/imperio/ayuda/AyudaApplication.java`

```java
package imperio.ayuda;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class AyudaApplication {
    public static void main(String[] args) {
        SpringApplication.run(AyudaApplication.class, args);
    }
}
```

`src/main/java/imperio/ayuda/Ticket.java`

```java
package imperio.ayuda;

import java.util.ArrayList;
import java.util.List;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;

@Getter
@RequiredArgsConstructor
public class Ticket {
    public enum Prioridad { BAJA, MEDIA, ALTA }

    public enum Estado { ABIERTO, CERRADO }

    private final long id;
    private final String titulo;
    private final String descripcion;
    private final Prioridad prioridad;
    private final String email;
    private final List<String> respuestas = new ArrayList<>();
    @Setter
    private Estado estado = Estado.ABIERTO;
}
```

`src/main/java/imperio/ayuda/TicketPedido.java`

```java
package imperio.ayuda;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record TicketPedido(
        @NotNull(message = "falta el título") @Size(min = 5, max = 80, message = "el título va de 5 a 80 caracteres") String titulo,
        @NotBlank(message = "falta la descripción") String descripcion,
        @NotNull(message = "falta la prioridad") Ticket.Prioridad prioridad,
        @NotBlank(message = "falta el email") @Email(message = "el email no es válido") String email) {
}
```

`src/main/java/imperio/ayuda/RespuestaPedido.java`

```java
package imperio.ayuda;

import jakarta.validation.constraints.NotBlank;

public record RespuestaPedido(@NotBlank(message = "la respuesta no puede estar vacía") String texto) {
}
```

`src/main/java/imperio/ayuda/TicketVista.java`

```java
package imperio.ayuda;

import java.util.List;

public record TicketVista(long id, String titulo, String descripcion, Ticket.Prioridad prioridad, Ticket.Estado estado, List<String> respuestas) {
    static TicketVista de(Ticket t) {
        return new TicketVista(t.getId(), t.getTitulo(), t.getDescripcion(), t.getPrioridad(), t.getEstado(), List.copyOf(t.getRespuestas()));
    }
}
```

`src/main/java/imperio/ayuda/Errores.java`

```java
package imperio.ayuda;

public final class Errores {
    private Errores() {
    }

    public static class NoEncontrado extends RuntimeException {
        public NoEncontrado(String mensaje) {
            super(mensaje);
        }
    }

    public static class Conflicto extends RuntimeException {
        public Conflicto(String mensaje) {
            super(mensaje);
        }
    }
}
```

`src/main/java/imperio/ayuda/ServicioTickets.java`

```java
package imperio.ayuda;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.stereotype.Service;

@Service
public class ServicioTickets {
    private final Map<Long, Ticket> tickets = new ConcurrentHashMap<>();
    private final AtomicLong proximoId = new AtomicLong(1);

    public Ticket abrir(TicketPedido p) {
        Ticket t = new Ticket(proximoId.getAndIncrement(), p.titulo(), p.descripcion(), p.prioridad(), p.email());
        tickets.put(t.getId(), t);
        return t;
    }

    public Ticket buscar(long id) {
        Ticket t = tickets.get(id);
        if (t == null) {
            throw new Errores.NoEncontrado("no existe el ticket " + id);
        }
        return t;
    }

    public synchronized Ticket responder(long id, String texto) {
        Ticket t = buscar(id);
        if (t.getEstado() == Ticket.Estado.CERRADO) {
            throw new Errores.Conflicto("el ticket " + id + " está cerrado");
        }
        t.getRespuestas().add(texto);
        return t;
    }

    public synchronized Ticket cerrar(long id) {
        Ticket t = buscar(id);
        if (t.getRespuestas().isEmpty()) {
            throw new Errores.Conflicto("no se cierra un ticket sin respuestas");
        }
        t.setEstado(Ticket.Estado.CERRADO);
        return t;
    }
}
```

`src/main/java/imperio/ayuda/TicketController.java`

```java
package imperio.ayuda;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/tickets")
@RequiredArgsConstructor
public class TicketController {
    private final ServicioTickets servicio;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public TicketVista abrir(@Valid @RequestBody TicketPedido pedido) {
        return TicketVista.de(servicio.abrir(pedido));
    }

    @GetMapping("/{id}")
    public TicketVista ver(@PathVariable long id) {
        return TicketVista.de(servicio.buscar(id));
    }

    @PostMapping("/{id}/respuestas")
    public TicketVista responder(@PathVariable long id, @Valid @RequestBody RespuestaPedido pedido) {
        return TicketVista.de(servicio.responder(id, pedido.texto()));
    }

    @PostMapping("/{id}/cierre")
    public TicketVista cerrar(@PathVariable long id) {
        return TicketVista.de(servicio.cerrar(id));
    }
}
```

`src/main/java/imperio/ayuda/ManejoDeErrores.java`

```java
package imperio.ayuda;

import java.util.Map;
import java.util.TreeMap;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ManejoDeErrores {
    @ExceptionHandler(Errores.NoEncontrado.class)
    public ProblemDetail noEncontrado(Errores.NoEncontrado e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
    }

    @ExceptionHandler(Errores.Conflicto.class)
    public ProblemDetail conflicto(Errores.Conflicto e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail invalido(MethodArgumentNotValidException e) {
        ProblemDetail p = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "datos inválidos");
        Map<String, String> campos = new TreeMap<>();
        e.getBindingResult().getFieldErrors().forEach(f -> campos.putIfAbsent(f.getField(), f.getDefaultMessage()));
        p.setProperty("campos", campos);
        return p;
    }

    // Un JSON que no se puede leer (por ejemplo, una prioridad que no está en el enum).
    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ProblemDetail ilegible(HttpMessageNotReadableException e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "el pedido tiene un valor que no se entiende");
    }
}
```

`src/test/java/imperio/ayuda/TicketControllerTest.java`

```java
package imperio.ayuda;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class TicketControllerTest {
    @Autowired
    private MockMvc mvc;

    private ResultActions enviar(String ruta, String json) throws Exception {
        return mvc.perform(post(ruta).contentType(MediaType.APPLICATION_JSON).content(json));
    }

    private static final String TICKET = """
            {"titulo": "No anda la impresora", "descripcion": "Sale la hoja en blanco", "prioridad": "ALTA", "email": "leo@oficina.com"}
            """;

    @Test
    void abreYNoMuestraElEmail() throws Exception {
        enviar("/tickets", TICKET).andExpect(status().isCreated())
                .andExpect(jsonPath("$.estado").value("ABIERTO"))
                .andExpect(jsonPath("$.email").doesNotExist());
        mvc.perform(get("/tickets/1")).andExpect(jsonPath("$.prioridad").value("ALTA"));
        mvc.perform(get("/tickets/5")).andExpect(status().isNotFound()).andExpect(jsonPath("$.detail").value("no existe el ticket 5"));
    }

    @Test
    void validaYRechazaUnaPrioridadInexistente() throws Exception {
        enviar("/tickets", """
                {"titulo": "Uy", "descripcion": "", "prioridad": "BAJA", "email": "leo"}
                """).andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.titulo").value("el título va de 5 a 80 caracteres"))
                .andExpect(jsonPath("$.campos.descripcion").value("falta la descripción"))
                .andExpect(jsonPath("$.campos.email").value("el email no es válido"));
        enviar("/tickets", TICKET.replace("ALTA", "URGENTE")).andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.detail").value("el pedido tiene un valor que no se entiende"));
    }

    @Test
    void responderYCerrarConSusReglas() throws Exception {
        enviar("/tickets", TICKET);
        mvc.perform(post("/tickets/1/cierre")).andExpect(status().isConflict())
                .andExpect(jsonPath("$.detail").value("no se cierra un ticket sin respuestas"));
        enviar("/tickets/1/respuestas", "{\"texto\": \" \"}").andExpect(status().isBadRequest());
        enviar("/tickets/1/respuestas", "{\"texto\": \"Cambiamos el tóner\"}")
                .andExpect(jsonPath("$.respuestas[0]").value("Cambiamos el tóner"));
        mvc.perform(post("/tickets/1/cierre")).andExpect(jsonPath("$.estado").value("CERRADO"));
        enviar("/tickets/1/respuestas", "{\"texto\": \"¿Anduvo?\"}").andExpect(status().isConflict());
    }
}
```

### Prueba del sello

#### ¿Qué es un DTO y para qué sirve?

Un objeto pensado solo para entrar o salir por la API; separa lo que viaja del modelo interno y evita exponer datos privados.

#### ¿Qué hace `@Valid` en un parámetro del controlador?

Hace cumplir las validaciones del DTO; si alguna falla, Spring no llama al método y responde 400.

#### ¿Cómo validás una regla que involucra dos campos?

Con un método `boolean` anotado con `@AssertTrue` en el DTO (o con una validación propia).

#### ¿Qué ventaja tiene un `@RestControllerAdvice`?

Centraliza el manejo de errores de todos los controladores: el servicio lanza excepciones y el *advice* decide el código y el formato.

#### ¿Qué genera `@RequiredArgsConstructor` de Lombok?

Un constructor con todos los atributos `final`, ideal para la inyección de dependencias.

### Soluciones (docente)

Nodo nuevo de la Senda (`19-Java-Avanzado` no tiene validaciones ni Lombok). Los `pom.xml` con Lombok declaran el procesador de anotaciones para que compilen también con Java 23 o más nuevo.

## R05-N07 · La Encrucijada de los Denarios

```meta
tipo: ventana
padre: R05-N05
precio: 10
```

### Crónica

En lo más alto de la Torre hay una ventana que nunca se abrió, con un marco vacío. Zed desenvuelve el vitral del viajero y lo coloca; la Llave del Vitral entra justo. El vidrio se enciende y muestra, por un instante, un balcón con cuatro portales y una frase grabada en el marco: *«para quien llegue»*.

Abajo, en la plaza central del Imperio, hay una fuente con forma de denario gigante, y de ella salen cuatro avenidas: una baja a la Bóveda, otra al Palacio de las Ventanas, otra a una sala de juegos llena de luces y la última al Puerto. Nadia vuelve a la Aduana, ahora como jefa de turno. Gheco señala las avenidas.

{mentor} espera a Zed sentado en el borde de la fuente, con una taza de café. —Ya hablás la lengua del Imperio. Lo que sigue no es obligatorio: es **tuyo**. Pero antes de elegir, mirá hacia atrás. ¿Qué te llevás de este viaje?

### Objetivos

- Repasar todo el camino principal y reconocer lo que aprendiste.
- Conocer las Sendas optativas que salen de acá.

### Explicación

#### Lo que ya sabés hacer

- **La Aduana del Compilador**: compilar y ejecutar, tipos, operadores, textos, entrada por teclado, decisiones, bucles, arrays y métodos.
- **La Academia de los Moldes**: clases y objetos, constructores, encapsulamiento, referencias, herencia, polimorfismo, interfaces, composición, `enum`, `record` y diagramas UML.
- **Los Archivos Imperiales**: paquetes y `.jar`, listas con envoltorios y autoboxing, mapas y conjuntos, excepciones, lambdas, pruebas con JUnit y depuración.
- **Las Corrientes del Imperio**: *streams*, `Collectors` y `Optional`, comparadores y Java moderno, patrones de diseño y concurrencia.
- **La Torre del Arquitecto**: Spring Boot con su contenedor e inyección de dependencias, servicios REST, capas con DTO, validaciones y Lombok.

Con eso podés construir un servicio web en capas como el del examen final de *Paradigmas y Lenguajes III* y leer el código Java de otros. Lo que sigue son **especializaciones**.

#### Las Sendas

Cada Senda es un camino optativo: no hace falta para completar el curso, y su entrada se paga con **comodines** (los que ganaste con los encargos). Adentro, los nodos se pagan con denarios, como siempre.

- **Senda de la Bóveda Imperial**: archivos, **SQL con PostgreSQL** (tablas, consultas, procedimientos, triggers y roles), JDBC, DAO y transacciones.
- **Senda del Palacio de las Ventanas**: **aplicaciones de escritorio** con Swing: layouts, componentes, tablas y árboles, MDI, `SwingWorker` y el MVC de la cátedra, hasta un sistema de actas completo (pide la Bóveda).
- **Senda del Arcade Imperial**: un **juego 2D** con Swing y Java2D: dibujar en un lienzo, el bucle de juego con un `Timer`, teclado, sprites, colisiones y un juego completo.
- **Senda del Puerto de Spring**: **persistencia con JPA** en PostgreSQL y el Kraken de los Servicios (pide lo básico de SQL de la Bóveda).

### Misión R05-N07-M1 · Mirá hacia atrás

```meta
entrega: ninguna
entorno: navegador
monedas: 0
xp: 20
```

#### Consigna

Antes de elegir tu Senda, tomate cinco minutos:

1. ¿Cuál fue el tema que más te costó? ¿Qué te ayudó a entenderlo?
2. ¿Qué programa de todo el camino te dio más orgullo?
3. ¿Qué te gustaría construir ahora con Java?

Charlalo con el profe en la próxima clase (o escribíselo). Cuando lo tengas, marcá la misión como completada.

#### Criterio de aprobación

- Pensaste las tres preguntas y lo charlaste con el profe.

### Prueba del sello

#### ¿Cuántas Sendas salen de la Encrucijada y con qué se paga su entrada?

Tres (el Arcade Imperial, las Corrientes y el Puerto de Spring), y la entrada se paga con comodines.

#### ¿Hace falta completar una Senda para terminar el curso?

No: las Sendas son optativas.

### Soluciones (docente)

Nodo de cierre del tronco (tipo `ventana`), como la Encrucijada de los otros cursos. La misión es de reflexión y no se entrega.
