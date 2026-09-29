# RAMA S03 · Senda del Puerto de Spring: servicios web

```meta
tipo: senda
posicion: 8
```

## S03-N01 · Maven y el contenedor de Spring

```meta
tipo: tema
padre: R05-N09
precio: 3
moneda: comodin
criatura: slime
ejecutable: no
```

### Crónica

La tercera avenida baja hasta el **Puerto de Spring**, el más grande del Imperio. Nadie carga los barcos a mano: una grúa gigante, el **Contenedor**, sabe qué pieza va en cada barco y las coloca sola. Los capitanes solo dicen *"necesito un timonel y una brújula"*, y el Contenedor se los entrega armados.

—Hasta ahora hacías `new` de todo y conectabas las piezas vos —dice {mentor}—. En el Puerto, **Spring** crea los objetos y se los pasa a quien los necesita. Y **Maven** trae las bibliotecas del mundo sin que copies un solo `.jar`. Es la forma en que se hacen hoy la mayoría de los sistemas en Java, {heroe}.

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
de esta Senda usan **Spring Boot 3.3** y un paquete que empieza con `imperio.`.

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

### Misión S03-N01-M1 · El reloj del puerto

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

### Misión S03-N01-M2 · Dos notificadores

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

### Misión S03-N01-M3 · El conversor configurable

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

### Encargo S03-N01-E1 · El despachante de pedidos

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

## S03-N02 · Servicios REST

```meta
tipo: tema
padre: S03-N01
precio: 10
criatura: orc
ejecutable: no
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
`AtomicLong` (lo viste en la Senda de las Corrientes).

**Slime: el puerto ocupado.** `Port 8080 was already in use`: quedó otra aplicación
corriendo. Cerrala o cambiá `server.port` en `application.properties`.

### Misión S03-N02-M1 · La API de la biblioteca

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

### Misión S03-N02-M2 · El catálogo con filtros

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

### Misión S03-N02-M3 · Las tareas del taller

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

### Encargo S03-N02-E1 · El turnero del consultorio

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

## S03-N03 · DTO, validaciones y errores

```meta
tipo: tema
padre: S03-N02
precio: 10
criatura: troll
ejecutable: no
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

### Misión S03-N03-M1 · El registro de usuarios

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

### Misión S03-N03-M2 · El presupuesto con Lombok

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

### Misión S03-N03-M3 · Las reservas del hotel

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

### Encargo S03-N03-E1 · La mesa de ayuda

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

## S03-N04 · JPA: la bóveda del Puerto

```meta
tipo: tema
padre: S03-N03
precio: 10
criatura: skeleton
ejecutable: no
```

### Crónica

Debajo del Puerto hay una bóveda como la que conociste en la cuarta rama, pero sin escribas. Cuando un capitán guarda un cargamento, unos espíritus lo anotan solos en las tablas, arman las consultas y hasta crean los estantes si faltan.

—En la Bóveda Imperial escribías cada `INSERT` y cada `ResultSet` a mano —dice {mentor}—. Estaba bien: ahora sabés lo que pasa por debajo. En el Puerto, **JPA** hace ese trabajo: vos decís qué clase va en qué tabla, y los repositorios aparecen solos. Pero ojo, {heroe}: los espíritus hacen lo que les pedís, no lo que querías pedir.

### Objetivos

- Mapear clases a tablas con `@Entity`, `@Id`, `@GeneratedValue`, `@Column`.
- Usar `JpaRepository`: el CRUD listo y las consultas derivadas del nombre del método.
- Escribir consultas con `@Query` (JPQL) y relacionar entidades con `@ManyToOne` y `@OneToMany`.
- Usar `@Transactional` en los servicios y paginar resultados.
- Conectar la aplicación a PostgreSQL y probar con `@DataJpaTest`.

### Antes de empezar

- DTO, validaciones y errores.
- La Bóveda Imperial (SQL, JDBC, DAO y transacciones) del tronco.

### Explicación

#### ORM y JPA
Un **ORM** (*Object-Relational Mapping*) traduce entre objetos y tablas. **JPA** es la
especificación de Java para eso, e **Hibernate** la implementación que usa Spring. Con
`spring-boot-starter-data-jpa` y el driver de PostgreSQL, Spring Boot arma la conexión,
el pool y los repositorios.

#### Entidades
Una **entidad** es una clase que corresponde a una tabla:
```java
@Entity
@Table(name = "heroe")
@Getter @Setter @NoArgsConstructor
public class Heroe {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)   // SERIAL / IDENTITY de PostgreSQL
    private Long id;

    @Column(nullable = false, length = 40)
    private String nombre;

    private int nivel;

    @ManyToOne(optional = false)
    @JoinColumn(name = "gremio_id")                         // la clave foránea
    private Gremio gremio;
}
```
JPA necesita un constructor sin parámetros (`@NoArgsConstructor`) y no se lleva bien con
`record` para las entidades: las entidades cambian, los `record` no. Los `record` quedan
para los DTO.

#### Repositorios: el DAO que no escribís
```java
public interface HeroeRepository extends JpaRepository<Heroe, Long> {
    List<Heroe> findByGremioNombre(String gremio);                       // consulta derivada del nombre
    List<Heroe> findByNivelGreaterThanOrderByNivelDesc(int nivel);
    boolean existsByNombre(String nombre);

    @Query("select h.gremio.nombre as gremio, count(h) as cantidad from Heroe h group by h.gremio.nombre order by h.gremio.nombre")
    List<Conteo> contarPorGremio();                                     // JPQL: sobre clases, no tablas
}
```
Spring **implementa la interfaz solo**. `JpaRepository` ya trae `save`, `findById`
(devuelve `Optional`), `findAll`, `deleteById`, `count` y más. Las **consultas
derivadas** se arman con el nombre del método: `findBy` + propiedad + condición
(`GreaterThan`, `Containing`, `Between`, `IgnoreCase`…) + `OrderBy`.

**JPQL** se parece a SQL, pero habla de **clases y atributos** (`Heroe h`, `h.gremio.nombre`),
no de tablas y columnas. El resultado de una consulta con `as` se puede recibir en una
interfaz de proyección (`interface Conteo { String getGremio(); long getCantidad(); }`).

#### Relaciones
| Anotación | Caso |
|---|---|
| `@ManyToOne` | muchos héroes, un gremio (tiene la clave foránea) |
| `@OneToMany(mappedBy = "gremio")` | un gremio, su lista de héroes (el lado inverso) |
| `@ManyToMany` | héroes y misiones (con tabla intermedia) |

Las relaciones se cargan **perezosamente** por defecto en `@OneToMany`: la lista se trae
de la base recién cuando se la recorre, y solo dentro de una transacción. Por eso **no se
devuelven entidades por la API**: se convierten a DTO dentro del servicio.

#### `@Transactional`
Un método de servicio con `@Transactional` corre dentro de **una transacción**: si lanza
una excepción, todo se deshace (`ROLLBACK`), como hacías a mano con JDBC. Dentro de la
transacción, los cambios a una entidad leída se guardan solos al terminar.

#### Paginar
Con miles de filas no se devuelve todo: `findAll(PageRequest.of(pagina, tamanio,
Sort.by("nombre")))` devuelve un `Page` con los elementos, el total y la cantidad de
páginas.

#### Configurar PostgreSQL y las pruebas
`src/main/resources/application.properties` apunta a la base `imperio` de la cuarta rama:
```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/imperio
spring.datasource.username=imperio
spring.datasource.password=imperio
spring.jpa.hibernate.ddl-auto=update
spring.jpa.open-in-view=false
```
`ddl-auto=update` crea o completa las tablas a partir de las entidades: cómodo para
aprender. En un sistema real las tablas se crean con *scripts* de migración (Flyway o
Liquibase) y se usa `validate`.

Para que las pruebas no dependan de tener PostgreSQL corriendo, usan **H2**, una base en
memoria: se agrega como dependencia de prueba, y un
`src/test/resources/application.properties` reemplaza la configuración en las pruebas.
`@DataJpaTest` levanta solo JPA (sin controladores) y deshace cada prueba al terminar.

> **Si venís de Python.** JPA es a Java lo que el ORM de Django o SQLAlchemy a Python:
> `Heroe.objects.filter(nivel__gt=5)` es `findByNivelGreaterThan(5)`.

### Código de ejemplo

Los gremios y sus héroes en PostgreSQL: entidades, repositorios con consultas derivadas y
JPQL, un servicio transaccional y la API con DTO.

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
    <artifactId>gremios</artifactId>
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
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
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
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
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
spring.datasource.url=jdbc:postgresql://localhost:5432/imperio
spring.datasource.username=imperio
spring.datasource.password=imperio
spring.jpa.hibernate.ddl-auto=update
spring.jpa.open-in-view=false
```

`src/test/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
spring.datasource.url=jdbc:h2:mem:imperio;MODE=PostgreSQL;DB_CLOSE_DELAY=-1
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.open-in-view=false
```

`src/main/java/imperio/gremios/GremiosApplication.java`

```java
package imperio.gremios;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class GremiosApplication {
    public static void main(String[] args) {
        SpringApplication.run(GremiosApplication.class, args);
    }
}
```

`src/main/java/imperio/gremios/Gremio.java`

```java
package imperio.gremios;

import java.util.ArrayList;
import java.util.List;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Getter
@Setter
@NoArgsConstructor
public class Gremio {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 40)
    private String nombre;

    @OneToMany(mappedBy = "gremio")
    private List<Heroe> heroes = new ArrayList<>();

    public Gremio(String nombre) {
        this.nombre = nombre;
    }
}
```

`src/main/java/imperio/gremios/Heroe.java`

```java
package imperio.gremios;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Getter
@Setter
@NoArgsConstructor
public class Heroe {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 40)
    private String nombre;

    private int nivel;

    @ManyToOne(optional = false)
    @JoinColumn(name = "gremio_id")
    private Gremio gremio;

    public Heroe(String nombre, int nivel, Gremio gremio) {
        this.nombre = nombre;
        this.nivel = nivel;
        this.gremio = gremio;
    }
}
```

`src/main/java/imperio/gremios/GremioRepository.java`

```java
package imperio.gremios;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

public interface GremioRepository extends JpaRepository<Gremio, Long> {
    Optional<Gremio> findByNombreIgnoreCase(String nombre);
}
```

`src/main/java/imperio/gremios/HeroeRepository.java`

```java
package imperio.gremios;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface HeroeRepository extends JpaRepository<Heroe, Long> {
    List<Heroe> findByGremioNombreOrderByNombre(String gremio);

    List<Heroe> findByNivelGreaterThanOrderByNivelDescNombreAsc(int nivel);

    boolean existsByNombreIgnoreCase(String nombre);

    interface Conteo {
        String getGremio();

        long getCantidad();

        double getNivelPromedio();
    }

    @Query("""
            select h.gremio.nombre as gremio, count(h) as cantidad, avg(h.nivel) as nivelPromedio
            from Heroe h
            group by h.gremio.nombre
            order by h.gremio.nombre
            """)
    List<Conteo> resumenPorGremio();
}
```

`src/main/java/imperio/gremios/HeroeDto.java`

```java
package imperio.gremios;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

public final class HeroeDto {
    private HeroeDto() {
    }

    public record Pedido(@NotBlank String nombre, @Min(1) @Max(100) int nivel, @NotBlank String gremio) {
    }

    public record Vista(long id, String nombre, int nivel, String gremio) {
        static Vista de(Heroe h) {
            return new Vista(h.getId(), h.getNombre(), h.getNivel(), h.getGremio().getNombre());
        }
    }
}
```

`src/main/java/imperio/gremios/ServicioGremios.java`

```java
package imperio.gremios;

import java.util.List;

import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

@Service
@RequiredArgsConstructor
public class ServicioGremios {
    private final GremioRepository gremios;
    private final HeroeRepository heroes;

    // Si el gremio no existe, se crea: las dos cosas en la misma transacción.
    @Transactional
    public HeroeDto.Vista reclutar(HeroeDto.Pedido p) {
        if (heroes.existsByNombreIgnoreCase(p.nombre())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "ya existe " + p.nombre());
        }
        Gremio gremio = gremios.findByNombreIgnoreCase(p.gremio()).orElseGet(() -> gremios.save(new Gremio(p.gremio())));
        return HeroeDto.Vista.de(heroes.save(new Heroe(p.nombre(), p.nivel(), gremio)));
    }

    @Transactional(readOnly = true)
    public List<HeroeDto.Vista> delGremio(String gremio) {
        return heroes.findByGremioNombreOrderByNombre(gremio).stream().map(HeroeDto.Vista::de).toList();
    }

    @Transactional
    public HeroeDto.Vista subirNivel(long id) {
        Heroe h = heroes.findById(id).orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "no existe el héroe " + id));
        h.setNivel(h.getNivel() + 1);           // dentro de la transacción se guarda solo
        return HeroeDto.Vista.de(h);
    }
}
```

`src/main/java/imperio/gremios/HeroeController.java`

```java
package imperio.gremios;

import java.util.List;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class HeroeController {
    private final ServicioGremios servicio;
    private final HeroeRepository heroes;

    @PostMapping("/heroes")
    @ResponseStatus(HttpStatus.CREATED)
    public HeroeDto.Vista reclutar(@Valid @RequestBody HeroeDto.Pedido pedido) {
        return servicio.reclutar(pedido);
    }

    @GetMapping("/heroes")
    public List<HeroeDto.Vista> delGremio(@RequestParam String gremio) {
        return servicio.delGremio(gremio);
    }

    @PostMapping("/heroes/{id}/nivel")
    public HeroeDto.Vista subirNivel(@PathVariable long id) {
        return servicio.subirNivel(id);
    }

    @GetMapping("/gremios/resumen")
    public List<HeroeRepository.Conteo> resumen() {
        return heroes.resumenPorGremio();
    }
}
```

`src/test/java/imperio/gremios/HeroeRepositoryTest.java`

```java
package imperio.gremios;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;

// Solo JPA, sobre H2; cada prueba se deshace al terminar.
@DataJpaTest
class HeroeRepositoryTest {
    @Autowired
    private GremioRepository gremios;

    @Autowired
    private HeroeRepository heroes;

    @BeforeEach
    void cargar() {
        Gremio arqueros = gremios.save(new Gremio("Arqueros"));
        Gremio magos = gremios.save(new Gremio("Magos"));
        heroes.saveAll(List.of(new Heroe("Kira", 7, arqueros), new Heroe("Ada", 9, arqueros),
                new Heroe("Lía", 5, magos), new Heroe("Olmo", 9, magos), new Heroe("Pip", 2, arqueros)));
    }

    @Test
    void lasConsultasDerivadas() {
        assertThat(heroes.findByGremioNombreOrderByNombre("Magos")).extracting(Heroe::getNombre).containsExactly("Lía", "Olmo");
        assertThat(heroes.findByNivelGreaterThanOrderByNivelDescNombreAsc(6)).extracting(Heroe::getNombre).containsExactly("Ada", "Olmo", "Kira");
        assertThat(heroes.existsByNombreIgnoreCase("kira")).isTrue();
        assertThat(gremios.findByNombreIgnoreCase("MAGOS")).isPresent();
    }

    @Test
    void elResumenConJpql() {
        List<HeroeRepository.Conteo> r = heroes.resumenPorGremio();
        assertThat(r).extracting(HeroeRepository.Conteo::getGremio).containsExactly("Arqueros", "Magos");
        assertThat(r.get(0).getCantidad()).isEqualTo(3);
        assertThat(r.get(1).getNivelPromedio()).isEqualTo(7.0);
    }
}
```

`src/test/java/imperio/gremios/HeroeControllerTest.java`

```java
package imperio.gremios;

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
class HeroeControllerTest {
    @Autowired
    private MockMvc mvc;

    private ResultActions reclutar(String nombre, int nivel, String gremio) throws Exception {
        return mvc.perform(post("/heroes").contentType(MediaType.APPLICATION_JSON)
                .content("{\"nombre\": \"" + nombre + "\", \"nivel\": " + nivel + ", \"gremio\": \"" + gremio + "\"}"));
    }

    @Test
    void reclutaCreandoElGremioSiFalta() throws Exception {
        reclutar("Kira", 7, "Arqueros").andExpect(status().isCreated()).andExpect(jsonPath("$.gremio").value("Arqueros"));
        reclutar("Ada", 9, "arqueros").andExpect(jsonPath("$.gremio").value("Arqueros"));
        reclutar("Lía", 5, "Magos");
        mvc.perform(get("/heroes").param("gremio", "Arqueros")).andExpect(jsonPath("$.length()").value(2));
        mvc.perform(get("/gremios/resumen"))
                .andExpect(jsonPath("$[0].gremio").value("Arqueros"))
                .andExpect(jsonPath("$[0].cantidad").value(2))
                .andExpect(jsonPath("$[1].nivelPromedio").value(5.0));
    }

    @Test
    void elRepetidoEs409ElInexistente404() throws Exception {
        reclutar("Kira", 7, "Arqueros");
        reclutar("KIRA", 3, "Magos").andExpect(status().isConflict());
        mvc.perform(post("/heroes/1/nivel")).andExpect(jsonPath("$.nivel").value(8));
        mvc.perform(post("/heroes/99/nivel")).andExpect(status().isNotFound());
    }
}
```

Con PostgreSQL corriendo y la base `imperio`, `./mvnw spring-boot:run` crea las tablas
`gremio` y `heroe` (miralas con `\d heroe` en `psql`) y la API guarda de verdad.

### ¿Para qué sirve?

JPA con Spring Data es la forma más común de trabajar con bases de datos en Java: la mayoría de los sistemas empresariales la usan. Con un repositorio de cuatro líneas tenés el CRUD y las consultas, y con `@Transactional` las operaciones quedan consistentes. Saber lo que pasa por debajo (la Bóveda Imperial) es lo que te va a permitir entender los errores cuando aparezcan.

### Errores habituales

**Dragón: la recursión infinita.** Devolver una entidad `Gremio` con su lista de
`Heroe`, y cada héroe con su `Gremio`… el JSON no termina nunca (o falla con
`LazyInitializationException`). Devolvé DTO.

**Liche: el N+1.** Recorrer 100 gremios y pedir `getHeroes()` de cada uno hace 101
consultas. Para traer todo junto: `@Query("select g from Gremio g join fetch g.heroes")` o
`@EntityGraph`.

**Ogro: el nombre de método mal escrito.** `findByNivell` hace fallar el arranque:
`No property 'nivell' found for type 'Heroe'`. Por lo menos avisa al arrancar.

**Troll: `@Transactional` que no hace nada.** Solo funciona en métodos `public` de un bean
llamados **desde otro bean**: llamarlo desde el mismo objeto (`this.metodo()`) se saltea
la transacción.

**Goblin: la entidad sin constructor vacío.** `No default constructor for entity`: JPA
necesita uno (puede ser `protected`, o `@NoArgsConstructor`).

**Ogro: `ddl-auto=create` en producción.** Borra y recrea las tablas en cada arranque:
se pierden los datos. En producción, `validate` y migraciones.

### Misión S03-N04-M1 · El inventario persistente

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Hacé una API para el inventario de un almacén, guardado en PostgreSQL con JPA. La
entidad `Producto` tiene código (único), nombre, rubro, precio (`BigDecimal`) y stock.
El repositorio tiene consultas derivadas para:

- los productos de un rubro ordenados por nombre;
- los que tienen stock menor a un valor;
- los que contienen un texto en el nombre, sin importar mayúsculas;
- buscar por código (`Optional`).

La API: `POST /productos` (409 si el código existe), `GET /productos/{codigo}` (404),
`GET /productos?rubro=` y `GET /productos/faltantes?menosDe=5`, y `PATCH
/productos/{codigo}/stock` con `{"cambio": -3}` que suma o resta y responde 409 si el
stock quedaría negativo. Probá el repositorio con `@DataJpaTest` y la API con `MockMvc`.

#### Criterio de aprobación

- Entidad con `@Entity` y repositorio `JpaRepository` con consultas derivadas.
- El cambio de stock es `@Transactional` y no deja stock negativo; las pruebas corren sobre H2.

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
    <artifactId>almacen</artifactId>
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
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
spring.datasource.url=jdbc:postgresql://localhost:5432/imperio
spring.datasource.username=imperio
spring.datasource.password=imperio
spring.jpa.hibernate.ddl-auto=update
spring.jpa.open-in-view=false
```

`src/test/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
spring.datasource.url=jdbc:h2:mem:imperio;MODE=PostgreSQL;DB_CLOSE_DELAY=-1
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.open-in-view=false
```

`src/main/java/imperio/almacen/AlmacenApplication.java`

```java
package imperio.almacen;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class AlmacenApplication {
    public static void main(String[] args) {
        SpringApplication.run(AlmacenApplication.class, args);
    }
}
```

`src/main/java/imperio/almacen/Producto.java`

```java
package imperio.almacen;

import java.math.BigDecimal;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Producto {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 20)
    private String codigo;

    @Column(nullable = false)
    private String nombre;

    @Column(nullable = false)
    private String rubro;

    @Column(nullable = false, precision = 12, scale = 2)
    private BigDecimal precio;

    private int stock;

    protected Producto() {
    }

    public Producto(String codigo, String nombre, String rubro, BigDecimal precio, int stock) {
        this.codigo = codigo;
        this.nombre = nombre;
        this.rubro = rubro;
        this.precio = precio;
        this.stock = stock;
    }

    public String getCodigo() {
        return codigo;
    }

    public String getNombre() {
        return nombre;
    }

    public String getRubro() {
        return rubro;
    }

    public BigDecimal getPrecio() {
        return precio;
    }

    public int getStock() {
        return stock;
    }

    public void setStock(int stock) {
        this.stock = stock;
    }
}
```

`src/main/java/imperio/almacen/ProductoRepository.java`

```java
package imperio.almacen;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductoRepository extends JpaRepository<Producto, Long> {
    List<Producto> findByRubroOrderByNombre(String rubro);

    List<Producto> findByStockLessThanOrderByStock(int stock);

    List<Producto> findByNombreContainingIgnoreCase(String texto);

    Optional<Producto> findByCodigo(String codigo);

    boolean existsByCodigo(String codigo);
}
```

`src/main/java/imperio/almacen/ProductoVista.java`

```java
package imperio.almacen;

import java.math.BigDecimal;

public record ProductoVista(String codigo, String nombre, String rubro, BigDecimal precio, int stock) {
    static ProductoVista de(Producto p) {
        return new ProductoVista(p.getCodigo(), p.getNombre(), p.getRubro(), p.getPrecio(), p.getStock());
    }
}
```

`src/main/java/imperio/almacen/ServicioInventario.java`

```java
package imperio.almacen;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

@Service
public class ServicioInventario {
    private final ProductoRepository productos;

    public ServicioInventario(ProductoRepository productos) {
        this.productos = productos;
    }

    @Transactional
    public ProductoVista crear(ProductoVista datos) {
        if (productos.existsByCodigo(datos.codigo())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "el código " + datos.codigo() + " ya existe");
        }
        return ProductoVista.de(productos.save(new Producto(datos.codigo(), datos.nombre(), datos.rubro(), datos.precio(), datos.stock())));
    }

    @Transactional(readOnly = true)
    public ProductoVista buscar(String codigo) {
        return productos.findByCodigo(codigo).map(ProductoVista::de)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "no existe " + codigo));
    }

    @Transactional(readOnly = true)
    public List<ProductoVista> delRubro(String rubro) {
        return productos.findByRubroOrderByNombre(rubro).stream().map(ProductoVista::de).toList();
    }

    @Transactional(readOnly = true)
    public List<ProductoVista> faltantes(int menosDe) {
        return productos.findByStockLessThanOrderByStock(menosDe).stream().map(ProductoVista::de).toList();
    }

    @Transactional
    public ProductoVista cambiarStock(String codigo, int cambio) {
        Producto p = productos.findByCodigo(codigo)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "no existe " + codigo));
        if (p.getStock() + cambio < 0) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "no alcanza el stock de " + codigo);
        }
        p.setStock(p.getStock() + cambio);
        return ProductoVista.de(p);
    }
}
```

`src/main/java/imperio/almacen/ProductoController.java`

```java
package imperio.almacen;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/productos")
public class ProductoController {
    private final ServicioInventario servicio;

    public ProductoController(ServicioInventario servicio) {
        this.servicio = servicio;
    }

    record CambioStock(int cambio) {
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public ProductoVista crear(@RequestBody ProductoVista datos) {
        return servicio.crear(datos);
    }

    @GetMapping("/{codigo}")
    public ProductoVista buscar(@PathVariable String codigo) {
        return servicio.buscar(codigo);
    }

    @GetMapping
    public List<ProductoVista> delRubro(@RequestParam String rubro) {
        return servicio.delRubro(rubro);
    }

    @GetMapping("/faltantes")
    public List<ProductoVista> faltantes(@RequestParam(defaultValue = "5") int menosDe) {
        return servicio.faltantes(menosDe);
    }

    @PatchMapping("/{codigo}/stock")
    public ProductoVista cambiarStock(@PathVariable String codigo, @RequestBody CambioStock cambio) {
        return servicio.cambiarStock(codigo, cambio.cambio());
    }
}
```

`src/test/java/imperio/almacen/ProductoRepositoryTest.java`

```java
package imperio.almacen;

import static org.assertj.core.api.Assertions.assertThat;

import java.math.BigDecimal;
import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;

@DataJpaTest
class ProductoRepositoryTest {
    @Autowired
    private ProductoRepository repo;

    @BeforeEach
    void cargar() {
        repo.saveAll(List.of(
                new Producto("A1", "Yerba Suave", "almacén", new BigDecimal("4200.50"), 20),
                new Producto("A2", "Yerba Intensa", "almacén", new BigDecimal("4500"), 2),
                new Producto("L1", "Lavandina", "limpieza", new BigDecimal("900"), 0),
                new Producto("A3", "Arroz", "almacén", new BigDecimal("1450"), 30)));
    }

    @Test
    void lasConsultasDerivadas() {
        assertThat(repo.findByRubroOrderByNombre("almacén")).extracting(Producto::getNombre)
                .containsExactly("Arroz", "Yerba Intensa", "Yerba Suave");
        assertThat(repo.findByStockLessThanOrderByStock(5)).extracting(Producto::getCodigo).containsExactly("L1", "A2");
        assertThat(repo.findByNombreContainingIgnoreCase("YERBA")).hasSize(2);
        assertThat(repo.findByCodigo("A1")).get().extracting(Producto::getPrecio).isEqualTo(new BigDecimal("4200.50"));
        assertThat(repo.findByCodigo("Z9")).isEmpty();
    }
}
```

`src/test/java/imperio/almacen/ProductoControllerTest.java`

```java
package imperio.almacen;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
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

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class ProductoControllerTest {
    @Autowired
    private MockMvc mvc;

    private void crear(String codigo, String nombre, int stock) throws Exception {
        mvc.perform(post("/productos").contentType(MediaType.APPLICATION_JSON).content(
                        "{\"codigo\": \"" + codigo + "\", \"nombre\": \"" + nombre + "\", \"rubro\": \"almacén\", \"precio\": 1000, \"stock\": " + stock + "}"))
                .andExpect(status().isCreated());
    }

    @Test
    void creaBuscaYListaFaltantes() throws Exception {
        crear("A1", "Yerba", 20);
        crear("A2", "Arroz", 3);
        mvc.perform(post("/productos").contentType(MediaType.APPLICATION_JSON).content(
                        "{\"codigo\": \"A1\", \"nombre\": \"Otra\", \"rubro\": \"x\", \"precio\": 1, \"stock\": 1}"))
                .andExpect(status().isConflict());
        mvc.perform(get("/productos/A1")).andExpect(jsonPath("$.nombre").value("Yerba"));
        mvc.perform(get("/productos/Z9")).andExpect(status().isNotFound());
        mvc.perform(get("/productos").param("rubro", "almacén")).andExpect(jsonPath("$[0].nombre").value("Arroz"));
        mvc.perform(get("/productos/faltantes")).andExpect(jsonPath("$.length()").value(1));
    }

    @Test
    void elStockNoQuedaNegativo() throws Exception {
        crear("A2", "Arroz", 3);
        mvc.perform(patch("/productos/A2/stock").contentType(MediaType.APPLICATION_JSON).content("{\"cambio\": -2}"))
                .andExpect(jsonPath("$.stock").value(1));
        mvc.perform(patch("/productos/A2/stock").contentType(MediaType.APPLICATION_JSON).content("{\"cambio\": -2}"))
                .andExpect(status().isConflict());
        mvc.perform(get("/productos/A2")).andExpect(jsonPath("$.stock").value(1));
    }
}
```

### Misión S03-N04-M2 · Autores y libros

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Modelá con JPA `Autor` (nombre, país) y `Libro` (título, año, autor) con
`@ManyToOne`/`@OneToMany`. Hacé:

- `POST /autores` y `POST /autores/{id}/libros` (404 si el autor no existe).
- `GET /autores/{id}` — el autor **con sus libros** ordenados por año, como DTO (sin
  recursión infinita), cargados con **una sola consulta** (`join fetch`).
- `GET /autores/ranking` — cada autor con su cantidad de libros, de más a menos (JPQL con
  `group by` y una proyección), incluidos los que tienen cero (`left join`).

Probá con `@DataJpaTest` y con `MockMvc`.

#### Criterio de aprobación

- La relación está bien mapeada (`mappedBy`) y la API devuelve DTO.
- El detalle usa `join fetch` y el ranking una consulta JPQL con `left join` y `group by`.

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
    <artifactId>autores</artifactId>
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
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
spring.datasource.url=jdbc:postgresql://localhost:5432/imperio
spring.datasource.username=imperio
spring.datasource.password=imperio
spring.jpa.hibernate.ddl-auto=update
spring.jpa.open-in-view=false
```

`src/test/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
spring.datasource.url=jdbc:h2:mem:imperio;MODE=PostgreSQL;DB_CLOSE_DELAY=-1
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.open-in-view=false
```

`src/main/java/imperio/autores/AutoresApplication.java`

```java
package imperio.autores;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class AutoresApplication {
    public static void main(String[] args) {
        SpringApplication.run(AutoresApplication.class, args);
    }
}
```

`src/main/java/imperio/autores/Autor.java`

```java
package imperio.autores;

import java.util.ArrayList;
import java.util.List;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;

@Entity
public class Autor {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String nombre;

    private String pais;

    @OneToMany(mappedBy = "autor")
    private List<Libro> libros = new ArrayList<>();

    protected Autor() {
    }

    public Autor(String nombre, String pais) {
        this.nombre = nombre;
        this.pais = pais;
    }

    public Long getId() {
        return id;
    }

    public String getNombre() {
        return nombre;
    }

    public String getPais() {
        return pais;
    }

    public List<Libro> getLibros() {
        return libros;
    }
}
```

`src/main/java/imperio/autores/Libro.java`

```java
package imperio.autores;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;

@Entity
public class Libro {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String titulo;

    private int anio;

    @ManyToOne(optional = false)
    private Autor autor;

    protected Libro() {
    }

    public Libro(String titulo, int anio, Autor autor) {
        this.titulo = titulo;
        this.anio = anio;
        this.autor = autor;
    }

    public String getTitulo() {
        return titulo;
    }

    public int getAnio() {
        return anio;
    }
}
```

`src/main/java/imperio/autores/AutorRepository.java`

```java
package imperio.autores;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface AutorRepository extends JpaRepository<Autor, Long> {
    @Query("select a from Autor a left join fetch a.libros where a.id = :id")
    Optional<Autor> conLibros(long id);

    interface Cantidad {
        String getNombre();

        long getLibros();
    }

    @Query("""
            select a.nombre as nombre, count(l) as libros
            from Autor a left join a.libros l
            group by a.id, a.nombre
            order by count(l) desc, a.nombre
            """)
    List<Cantidad> ranking();
}
```

`src/main/java/imperio/autores/LibroRepository.java`

```java
package imperio.autores;

import org.springframework.data.jpa.repository.JpaRepository;

public interface LibroRepository extends JpaRepository<Libro, Long> {
}
```

`src/main/java/imperio/autores/Dto.java`

```java
package imperio.autores;

import java.util.Comparator;
import java.util.List;

public final class Dto {
    private Dto() {
    }

    public record AutorPedido(String nombre, String pais) {
    }

    public record LibroPedido(String titulo, int anio) {
    }

    public record LibroVista(String titulo, int anio) {
    }

    public record AutorVista(long id, String nombre, String pais, List<LibroVista> libros) {
        static AutorVista de(Autor a) {
            List<LibroVista> libros = a.getLibros().stream()
                    .sorted(Comparator.comparingInt(Libro::getAnio))
                    .map(l -> new LibroVista(l.getTitulo(), l.getAnio()))
                    .toList();
            return new AutorVista(a.getId(), a.getNombre(), a.getPais(), libros);
        }
    }
}
```

`src/main/java/imperio/autores/ServicioAutores.java`

```java
package imperio.autores;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

@Service
public class ServicioAutores {
    private final AutorRepository autores;
    private final LibroRepository libros;

    public ServicioAutores(AutorRepository autores, LibroRepository libros) {
        this.autores = autores;
        this.libros = libros;
    }

    @Transactional
    public long crearAutor(Dto.AutorPedido p) {
        return autores.save(new Autor(p.nombre(), p.pais())).getId();
    }

    @Transactional
    public void agregarLibro(long autorId, Dto.LibroPedido p) {
        Autor a = autores.findById(autorId).orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "no existe el autor"));
        libros.save(new Libro(p.titulo(), p.anio(), a));
    }

    @Transactional(readOnly = true)
    public Dto.AutorVista detalle(long id) {
        return autores.conLibros(id).map(Dto.AutorVista::de)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "no existe el autor"));
    }

    @Transactional(readOnly = true)
    public List<AutorRepository.Cantidad> ranking() {
        return autores.ranking();
    }
}
```

`src/main/java/imperio/autores/AutorController.java`

```java
package imperio.autores;

import java.net.URI;
import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/autores")
public class AutorController {
    private final ServicioAutores servicio;

    public AutorController(ServicioAutores servicio) {
        this.servicio = servicio;
    }

    @PostMapping
    public ResponseEntity<Void> crear(@RequestBody Dto.AutorPedido p) {
        return ResponseEntity.created(URI.create("/autores/" + servicio.crearAutor(p))).build();
    }

    @PostMapping("/{id}/libros")
    @ResponseStatus(HttpStatus.CREATED)
    public void agregarLibro(@PathVariable long id, @RequestBody Dto.LibroPedido p) {
        servicio.agregarLibro(id, p);
    }

    @GetMapping("/{id}")
    public Dto.AutorVista detalle(@PathVariable long id) {
        return servicio.detalle(id);
    }

    @GetMapping("/ranking")
    public List<AutorRepository.Cantidad> ranking() {
        return servicio.ranking();
    }
}
```

`src/test/java/imperio/autores/AutorControllerTest.java`

```java
package imperio.autores;

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
class AutorControllerTest {
    @Autowired
    private MockMvc mvc;

    private void json(String ruta, String cuerpo) throws Exception {
        mvc.perform(post(ruta).contentType(MediaType.APPLICATION_JSON).content(cuerpo)).andExpect(status().isCreated());
    }

    @Test
    void elDetalleTraeLosLibrosOrdenadosSinRecursion() throws Exception {
        mvc.perform(post("/autores").contentType(MediaType.APPLICATION_JSON).content("{\"nombre\": \"Borges\", \"pais\": \"Argentina\"}"))
                .andExpect(header().string("Location", "/autores/1"));
        json("/autores/1/libros", "{\"titulo\": \"El Aleph\", \"anio\": 1949}");
        json("/autores/1/libros", "{\"titulo\": \"Ficciones\", \"anio\": 1944}");
        mvc.perform(get("/autores/1"))
                .andExpect(jsonPath("$.nombre").value("Borges"))
                .andExpect(jsonPath("$.libros[0].titulo").value("Ficciones"))
                .andExpect(jsonPath("$.libros[1].autor").doesNotExist());
        mvc.perform(post("/autores/7/libros").contentType(MediaType.APPLICATION_JSON).content("{\"titulo\": \"X\", \"anio\": 1}"))
                .andExpect(status().isNotFound());
    }

    @Test
    void elRankingIncluyeALosQueNoTienenLibros() throws Exception {
        json("/autores", "{\"nombre\": \"Cortázar\", \"pais\": \"Argentina\"}");
        json("/autores", "{\"nombre\": \"Ocampo\", \"pais\": \"Argentina\"}");
        json("/autores", "{\"nombre\": \"Storni\", \"pais\": \"Argentina\"}");
        json("/autores/1/libros", "{\"titulo\": \"Rayuela\", \"anio\": 1963}");
        json("/autores/1/libros", "{\"titulo\": \"Bestiario\", \"anio\": 1951}");
        json("/autores/3/libros", "{\"titulo\": \"Ocre\", \"anio\": 1925}");
        mvc.perform(get("/autores/ranking"))
                .andExpect(jsonPath("$[0].nombre").value("Cortázar"))
                .andExpect(jsonPath("$[0].libros").value(2))
                .andExpect(jsonPath("$[1].nombre").value("Storni"))
                .andExpect(jsonPath("$[2].nombre").value("Ocampo"))
                .andExpect(jsonPath("$[2].libros").value(0));
    }
}
```

### Misión S03-N04-M3 · La transferencia transaccional

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Con JPA, una entidad `Cuenta` (titular, saldo `BigDecimal`) y otra `Movimiento` (cuenta,
monto, descripción, fecha). Escribí un servicio `transferir(origen, destino, monto)`
**`@Transactional`** que: descuenta del origen, registra un movimiento, acredita al
destino y registra otro movimiento. Si el origen no tiene saldo, lanza una excepción
**después** de haber registrado el primer movimiento (simulando un error a mitad de
camino), para comprobar que **nada** queda guardado. Probá con `@SpringBootTest` (sin
MockMvc) que una transferencia correcta mueve la plata y registra dos movimientos, y que
una fallida deja los saldos y los movimientos como estaban.

#### Criterio de aprobación

- El servicio es `@Transactional` y la prueba demuestra el `ROLLBACK`.
- Usa `BigDecimal` para los montos.

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
    <artifactId>banco</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
spring.datasource.url=jdbc:postgresql://localhost:5432/imperio
spring.datasource.username=imperio
spring.datasource.password=imperio
spring.jpa.hibernate.ddl-auto=update
```

`src/test/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
spring.datasource.url=jdbc:h2:mem:imperio;MODE=PostgreSQL;DB_CLOSE_DELAY=-1
spring.jpa.hibernate.ddl-auto=create-drop
```

`src/main/java/imperio/banco/BancoApplication.java`

```java
package imperio.banco;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class BancoApplication {
    public static void main(String[] args) {
        SpringApplication.run(BancoApplication.class, args);
    }
}
```

`src/main/java/imperio/banco/Cuenta.java`

```java
package imperio.banco;

import java.math.BigDecimal;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Cuenta {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String titular;

    @Column(precision = 14, scale = 2)
    private BigDecimal saldo;

    protected Cuenta() {
    }

    public Cuenta(String titular, BigDecimal saldo) {
        this.titular = titular;
        this.saldo = saldo;
    }

    public Long getId() {
        return id;
    }

    public BigDecimal getSaldo() {
        return saldo;
    }

    public void mover(BigDecimal monto) {
        saldo = saldo.add(monto);
    }
}
```

`src/main/java/imperio/banco/Movimiento.java`

```java
package imperio.banco;

import java.math.BigDecimal;
import java.time.LocalDateTime;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;

@Entity
public class Movimiento {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(optional = false)
    private Cuenta cuenta;

    @Column(precision = 14, scale = 2)
    private BigDecimal monto;

    private String descripcion;

    private LocalDateTime fecha;

    protected Movimiento() {
    }

    public Movimiento(Cuenta cuenta, BigDecimal monto, String descripcion) {
        this.cuenta = cuenta;
        this.monto = monto;
        this.descripcion = descripcion;
        this.fecha = LocalDateTime.now();
    }
}
```

`src/main/java/imperio/banco/CuentaRepository.java`

```java
package imperio.banco;

import org.springframework.data.jpa.repository.JpaRepository;

public interface CuentaRepository extends JpaRepository<Cuenta, Long> {
}
```

`src/main/java/imperio/banco/MovimientoRepository.java`

```java
package imperio.banco;

import org.springframework.data.jpa.repository.JpaRepository;

public interface MovimientoRepository extends JpaRepository<Movimiento, Long> {
}
```

`src/main/java/imperio/banco/SaldoInsuficiente.java`

```java
package imperio.banco;

public class SaldoInsuficiente extends RuntimeException {
    public SaldoInsuficiente(String mensaje) {
        super(mensaje);
    }
}
```

`src/main/java/imperio/banco/ServicioTransferencias.java`

```java
package imperio.banco;

import java.math.BigDecimal;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ServicioTransferencias {
    private final CuentaRepository cuentas;
    private final MovimientoRepository movimientos;

    public ServicioTransferencias(CuentaRepository cuentas, MovimientoRepository movimientos) {
        this.cuentas = cuentas;
        this.movimientos = movimientos;
    }

    @Transactional
    public void transferir(long origenId, long destinoId, BigDecimal monto) {
        Cuenta origen = cuentas.findById(origenId).orElseThrow();
        Cuenta destino = cuentas.findById(destinoId).orElseThrow();

        origen.mover(monto.negate());
        movimientos.save(new Movimiento(origen, monto.negate(), "transferencia a " + destinoId));
        movimientos.flush();                    // el INSERT ya se mandó a la base…

        if (origen.getSaldo().signum() < 0) {
            // …pero al lanzar la excepción, la transacción entera se deshace.
            throw new SaldoInsuficiente("la cuenta " + origenId + " no tiene saldo suficiente");
        }
        destino.mover(monto);
        movimientos.save(new Movimiento(destino, monto, "transferencia de " + origenId));
    }
}
```

`src/test/java/imperio/banco/TransferenciaTest.java`

```java
package imperio.banco;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.math.BigDecimal;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class TransferenciaTest {
    @Autowired
    private ServicioTransferencias servicio;

    @Autowired
    private CuentaRepository cuentas;

    @Autowired
    private MovimientoRepository movimientos;

    private long ana;
    private long leo;

    @BeforeEach
    void cuentas() {
        movimientos.deleteAll();
        cuentas.deleteAll();
        ana = cuentas.save(new Cuenta("Ana", new BigDecimal("1000.00"))).getId();
        leo = cuentas.save(new Cuenta("Leo", new BigDecimal("50.00"))).getId();
    }

    private BigDecimal saldo(long id) {
        return cuentas.findById(id).orElseThrow().getSaldo();
    }

    @Test
    void unaTransferenciaCorrectaMueveLaPlata() {
        servicio.transferir(ana, leo, new BigDecimal("250.50"));
        assertEquals(new BigDecimal("749.50"), saldo(ana));
        assertEquals(new BigDecimal("300.50"), saldo(leo));
        assertEquals(2, movimientos.count());
    }

    @Test
    void unaFallidaNoDejaNadaGuardado() {
        assertThrows(SaldoInsuficiente.class, () -> servicio.transferir(leo, ana, new BigDecimal("80.00")));
        assertEquals(new BigDecimal("50.00"), saldo(leo));
        assertEquals(new BigDecimal("1000.00"), saldo(ana));
        assertEquals(0, movimientos.count());
    }
}
```

### Encargo S03-N04-E1 · El padrón paginado

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Un club tiene cientos de socios. Con JPA, hacé `GET /socios?pagina=0&tamanio=10&orden=apellido`
que devuelva una página de socios con los datos de la página: número, tamaño, total de
elementos, total de páginas y si es la última (un DTO propio, no el `Page` de Spring).
Sumá un filtro opcional por categoría (`?categoria=cadete`) con una consulta derivada
paginada (`Page<Socio> findByCategoria(String, Pageable)`). El tamaño máximo es 50 (si
piden más, se usa 50). Cargá 57 socios de prueba al arrancar las pruebas y probá la
primera, una del medio y la última página.

#### Criterio de aprobación

- Usa `Pageable`/`PageRequest` y `Sort`; la respuesta es un DTO con los datos de la página.
- El filtro por categoría también pagina y el tamaño se limita a 50.

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
    <artifactId>club</artifactId>
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
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

`src/main/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
spring.datasource.url=jdbc:postgresql://localhost:5432/imperio
spring.datasource.username=imperio
spring.datasource.password=imperio
spring.jpa.hibernate.ddl-auto=update
spring.jpa.open-in-view=false
```

`src/test/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
spring.datasource.url=jdbc:h2:mem:imperio;MODE=PostgreSQL;DB_CLOSE_DELAY=-1
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.open-in-view=false
```

`src/main/java/imperio/club/ClubApplication.java`

```java
package imperio.club;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ClubApplication {
    public static void main(String[] args) {
        SpringApplication.run(ClubApplication.class, args);
    }
}
```

`src/main/java/imperio/club/Socio.java`

```java
package imperio.club;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Socio {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String apellido;

    private String nombre;

    private String categoria;

    protected Socio() {
    }

    public Socio(String apellido, String nombre, String categoria) {
        this.apellido = apellido;
        this.nombre = nombre;
        this.categoria = categoria;
    }

    public String getApellido() {
        return apellido;
    }

    public String getNombre() {
        return nombre;
    }

    public String getCategoria() {
        return categoria;
    }
}
```

`src/main/java/imperio/club/SocioRepository.java`

```java
package imperio.club;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

public interface SocioRepository extends JpaRepository<Socio, Long> {
    Page<Socio> findByCategoria(String categoria, Pageable pagina);
}
```

`src/main/java/imperio/club/Pagina.java`

```java
package imperio.club;

import java.util.List;
import java.util.function.Function;

import org.springframework.data.domain.Page;

public record Pagina<T>(List<T> elementos, int numero, int tamanio, long total, int paginas, boolean ultima) {
    static <E, T> Pagina<T> de(Page<E> page, Function<E, T> convertir) {
        return new Pagina<>(page.getContent().stream().map(convertir).toList(), page.getNumber(), page.getSize(),
                page.getTotalElements(), page.getTotalPages(), page.isLast());
    }
}
```

`src/main/java/imperio/club/SocioController.java`

```java
package imperio.club;

import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SocioController {
    static final int TAMANIO_MAXIMO = 50;

    record SocioVista(String apellido, String nombre, String categoria) {
    }

    private final SocioRepository socios;

    public SocioController(SocioRepository socios) {
        this.socios = socios;
    }

    @GetMapping("/socios")
    @Transactional(readOnly = true)
    public Pagina<SocioVista> listar(@RequestParam(defaultValue = "0") int pagina,
                                     @RequestParam(defaultValue = "10") int tamanio,
                                     @RequestParam(defaultValue = "apellido") String orden,
                                     @RequestParam(required = false) String categoria) {
        PageRequest pedido = PageRequest.of(Math.max(pagina, 0), Math.min(Math.max(tamanio, 1), TAMANIO_MAXIMO),
                Sort.by(orden).and(Sort.by("nombre")));
        var page = categoria == null ? socios.findAll(pedido) : socios.findByCategoria(categoria, pedido);
        return Pagina.de(page, s -> new SocioVista(s.getApellido(), s.getNombre(), s.getCategoria()));
    }
}
```

`src/test/java/imperio/club/SocioControllerTest.java`

```java
package imperio.club;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInstance;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class SocioControllerTest {
    @Autowired
    private MockMvc mvc;

    @Autowired
    private SocioRepository socios;

    @BeforeAll
    void cargar57() {
        List<Socio> lista = new ArrayList<>();
        for (int i = 1; i <= 57; i++) {
            lista.add(new Socio(String.format("Apellido%02d", i), "Nombre" + i, i % 3 == 0 ? "cadete" : "activo"));
        }
        socios.saveAll(lista);
    }

    @Test
    void primeraPagina() throws Exception {
        mvc.perform(get("/socios"))
                .andExpect(jsonPath("$.elementos.length()").value(10))
                .andExpect(jsonPath("$.elementos[0].apellido").value("Apellido01"))
                .andExpect(jsonPath("$.total").value(57))
                .andExpect(jsonPath("$.paginas").value(6))
                .andExpect(jsonPath("$.ultima").value(false));
    }

    @Test
    void unaDelMedioYLaUltima() throws Exception {
        mvc.perform(get("/socios").param("pagina", "2"))
                .andExpect(jsonPath("$.elementos[0].apellido").value("Apellido21"));
        mvc.perform(get("/socios").param("pagina", "5"))
                .andExpect(jsonPath("$.elementos.length()").value(7))
                .andExpect(jsonPath("$.ultima").value(true));
    }

    @Test
    void filtraPorCategoriaYLimitaElTamanio() throws Exception {
        mvc.perform(get("/socios").param("categoria", "cadete").param("tamanio", "5"))
                .andExpect(jsonPath("$.total").value(19))
                .andExpect(jsonPath("$.paginas").value(4))
                .andExpect(jsonPath("$.elementos[0].apellido").value("Apellido03"));
        mvc.perform(get("/socios").param("tamanio", "500"))
                .andExpect(jsonPath("$.tamanio").value(50))
                .andExpect(jsonPath("$.elementos.length()").value(50));
    }
}
```

### Prueba del sello

#### ¿Qué hace `JpaRepository`?

Da el CRUD (`save`, `findById`, `findAll`, `deleteById`…) de una entidad sin escribir la implementación, y permite declarar consultas por el nombre del método.

#### ¿En qué se diferencia JPQL de SQL?

JPQL consulta clases y atributos (`Heroe h`, `h.gremio.nombre`), no tablas y columnas.

#### ¿Por qué no conviene devolver entidades por la API?

Porque exponen todos los campos, pueden generar recursión infinita en las relaciones y fallar con la carga perezosa fuera de la transacción.

#### ¿Qué hace `@Transactional` si el método lanza una excepción?

Deshace todo lo que hizo el método en la base (`ROLLBACK`).

#### ¿Qué es el problema N+1 y cómo se evita?

Hacer una consulta por cada elemento de una lista para traer su relación; se evita trayendo todo junto con `join fetch` o `@EntityGraph`.

### Soluciones (docente)

Nodo nuevo de la Senda, apoyado en la rama 4 (la bóveda con JDBC). Las pruebas usan H2 en modo PostgreSQL para que corran sin base; la aplicación apunta a la base `imperio` de PostgreSQL. Se corrige con `./mvnw test` y, si se puede, arrancando la aplicación contra PostgreSQL.

## S03-N05 · Jefe del Puerto: el Kraken de los Servicios

```meta
tipo: jefe
padre: S03-N04
precio: 10
criatura: dragon
ejecutable: no
insignia: Capitán del Puerto de Spring
insignia_descripcion: Venciste al Kraken de los Servicios: construiste una API REST completa con Spring Boot, JPA y pruebas.
```

### Crónica

Una noche, las aguas del Puerto se agitan y ocho tentáculos salen del mar. Cada uno arrastra un pedido distinto: uno pide datos que no existen, otro manda formularios rotos, otro intenta vender lo que no hay en stock, otro quiere leer mil registros de una vez. Es el **Kraken de los Servicios**, y solo lo vence una API que no se rompa con nada.

—Juntá todo, {heroe} —dice {mentor}, sin soltar la taza—: entidades y repositorios, DTO validados, errores claros, transacciones que no dejan nada a medias, páginas en lugar de avalanchas. Y pruebas para cada tentáculo. Así se construyen los sistemas que usa la gente de verdad.

### Objetivos

- Diseñar y construir una API REST completa con Spring Boot, JPA y PostgreSQL.
- Aplicar las capas: controlador → servicio → repositorio, con DTO en los bordes.
- Proteger las reglas del negocio con validaciones, errores `ProblemDetail` y transacciones.
- Probar la API de punta a punta con `MockMvc`.

### Antes de empezar

- Toda la Senda del Puerto de Spring.

### Explicación

#### La forma de un servicio completo
```
controlador   → recibe DTO validados (@Valid), llama al servicio, devuelve DTO
servicio      → las reglas del negocio, @Transactional, lanza excepciones propias
repositorio   → JpaRepository con consultas derivadas y JPQL
entidades     → @Entity con sus relaciones (nunca salen por la API)
errores       → un @RestControllerAdvice que convierte excepciones en ProblemDetail
```
Cada capa conoce solo a la de abajo. El controlador no sabe de SQL; el repositorio no
sabe de HTTP.

#### Las reglas del negocio viven en el servicio
Validar que un campo no esté vacío es trabajo del DTO. Pero "no se puede cargar una nota
a un alumno que no está inscripto" o "no se vende lo que no hay en stock" son **reglas
del negocio**: van en el servicio, dentro de una transacción, y se prueban.

#### Pensar la API antes de escribirla
Antes de programar, escribí la tabla de rutas: verbo, ruta, qué recibe, qué devuelve y
qué errores puede dar. Es el contrato con quien va a usar tu API (la app de celular, la
página web).

### Código de ejemplo

Las actas de examen, ahora como servicio web (el mismo sistema que hiciste de escritorio
en el Palacio de las Ventanas): materias, alumnos, inscripciones y notas.

| Verbo y ruta | Hace | Errores |
|---|---|---|
| `POST /materias` | crea una materia | 400, 409 (código repetido) |
| `POST /alumnos` | crea un alumno | 400, 409 (legajo repetido) |
| `POST /materias/{codigo}/inscripciones` | inscribe un alumno por legajo | 404, 409 (ya inscripto) |
| `POST /materias/{codigo}/notas` | carga la nota de un inscripto | 400, 404, 409 (no inscripto o ya tiene nota) |
| `GET /materias/{codigo}/acta?pagina=` | el acta paginada, por apellido | 404 |
| `GET /materias/{codigo}/estadisticas` | inscriptos, aprobados, promedio | 404 |

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
    <artifactId>actas</artifactId>
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
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
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
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
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
spring.datasource.url=jdbc:postgresql://localhost:5432/imperio
spring.datasource.username=imperio
spring.datasource.password=imperio
spring.jpa.hibernate.ddl-auto=update
spring.jpa.open-in-view=false
```

`src/test/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
spring.datasource.url=jdbc:h2:mem:imperio;MODE=PostgreSQL;DB_CLOSE_DELAY=-1
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.open-in-view=false
```

`src/main/java/imperio/actas/ActasApplication.java`

```java
package imperio.actas;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ActasApplication {
    public static void main(String[] args) {
        SpringApplication.run(ActasApplication.class, args);
    }
}
```

`src/main/java/imperio/actas/modelo/Materia.java`

```java
package imperio.actas.modelo;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Getter
@NoArgsConstructor
public class Materia {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 10)
    private String codigo;

    @Column(nullable = false)
    private String nombre;

    public Materia(String codigo, String nombre) {
        this.codigo = codigo;
        this.nombre = nombre;
    }
}
```

`src/main/java/imperio/actas/modelo/Alumno.java`

```java
package imperio.actas.modelo;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Getter
@NoArgsConstructor
public class Alumno {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private int legajo;

    @Column(nullable = false)
    private String apellido;

    @Column(nullable = false)
    private String nombre;

    public Alumno(int legajo, String apellido, String nombre) {
        this.legajo = legajo;
        this.apellido = apellido;
        this.nombre = nombre;
    }
}
```

`src/main/java/imperio/actas/modelo/Inscripcion.java`

```java
package imperio.actas.modelo;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

// Un alumno inscripto en una materia; la nota se carga después.
@Entity
@Table(uniqueConstraints = @UniqueConstraint(columnNames = {"materia_id", "alumno_id"}))
@Getter
@NoArgsConstructor
public class Inscripcion {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(optional = false)
    private Materia materia;

    @ManyToOne(optional = false)
    private Alumno alumno;

    @Setter
    private Integer nota;

    public Inscripcion(Materia materia, Alumno alumno) {
        this.materia = materia;
        this.alumno = alumno;
    }
}
```

`src/main/java/imperio/actas/repositorio/MateriaRepository.java`

```java
package imperio.actas.repositorio;

import java.util.Optional;

import imperio.actas.modelo.Materia;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MateriaRepository extends JpaRepository<Materia, Long> {
    Optional<Materia> findByCodigo(String codigo);

    boolean existsByCodigo(String codigo);
}
```

`src/main/java/imperio/actas/repositorio/AlumnoRepository.java`

```java
package imperio.actas.repositorio;

import java.util.Optional;

import imperio.actas.modelo.Alumno;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AlumnoRepository extends JpaRepository<Alumno, Long> {
    Optional<Alumno> findByLegajo(int legajo);

    boolean existsByLegajo(int legajo);
}
```

`src/main/java/imperio/actas/repositorio/InscripcionRepository.java`

```java
package imperio.actas.repositorio;

import java.util.Optional;

import imperio.actas.modelo.Inscripcion;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface InscripcionRepository extends JpaRepository<Inscripcion, Long> {
    Optional<Inscripcion> findByMateriaCodigoAndAlumnoLegajo(String codigo, int legajo);

    Page<Inscripcion> findByMateriaCodigo(String codigo, Pageable pagina);

    interface Estadisticas {
        long getInscriptos();

        long getConNota();

        long getAprobados();

        Double getPromedio();
    }

    @Query("""
            select count(i) as inscriptos,
                   count(i.nota) as conNota,
                   sum(case when i.nota >= 4 then 1 else 0 end) as aprobados,
                   avg(i.nota) as promedio
            from Inscripcion i
            where i.materia.codigo = :codigo
            """)
    Estadisticas estadisticas(String codigo);
}
```

`src/main/java/imperio/actas/web/Dto.java`

```java
package imperio.actas.web;

import java.util.List;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;

public final class Dto {
    private Dto() {
    }

    public record MateriaPedido(
            @NotNull(message = "falta el código") @Pattern(regexp = "[A-Z]{3}\\d{2}", message = "el código es de 3 letras y 2 números (PRO01)") String codigo,
            @NotBlank(message = "falta el nombre") String nombre) {
    }

    public record AlumnoPedido(
            @Min(value = 1, message = "el legajo tiene que ser positivo") int legajo,
            @NotBlank(message = "falta el apellido") String apellido,
            @NotBlank(message = "falta el nombre") String nombre) {
    }

    public record InscripcionPedido(@Min(value = 1, message = "falta el legajo") int legajo) {
    }

    public record NotaPedido(
            @Min(value = 1, message = "falta el legajo") int legajo,
            @NotNull(message = "falta la nota") @Min(value = 1, message = "la nota va de 1 a 10") @Max(value = 10, message = "la nota va de 1 a 10") Integer nota) {
    }

    public record RenglonActa(int legajo, String alumno, Integer nota, String condicion) {
    }

    public record Acta(String materia, List<RenglonActa> renglones, int pagina, int paginas, long total) {
    }

    public record Estadisticas(String materia, long inscriptos, long conNota, long aprobados, double promedio) {
    }
}
```

`src/main/java/imperio/actas/servicio/Errores.java`

```java
package imperio.actas.servicio;

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

`src/main/java/imperio/actas/servicio/ServicioActas.java`

```java
package imperio.actas.servicio;

import imperio.actas.modelo.Alumno;
import imperio.actas.modelo.Inscripcion;
import imperio.actas.modelo.Materia;
import imperio.actas.repositorio.AlumnoRepository;
import imperio.actas.repositorio.InscripcionRepository;
import imperio.actas.repositorio.MateriaRepository;
import imperio.actas.web.Dto;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class ServicioActas {
    static final int RENGLONES_POR_PAGINA = 20;

    private final MateriaRepository materias;
    private final AlumnoRepository alumnos;
    private final InscripcionRepository inscripciones;

    @Transactional
    public void crearMateria(Dto.MateriaPedido p) {
        if (materias.existsByCodigo(p.codigo())) {
            throw new Errores.Conflicto("ya existe la materia " + p.codigo());
        }
        materias.save(new Materia(p.codigo(), p.nombre()));
    }

    @Transactional
    public void crearAlumno(Dto.AlumnoPedido p) {
        if (alumnos.existsByLegajo(p.legajo())) {
            throw new Errores.Conflicto("ya existe el legajo " + p.legajo());
        }
        alumnos.save(new Alumno(p.legajo(), p.apellido(), p.nombre()));
    }

    @Transactional
    public void inscribir(String codigo, int legajo) {
        Materia m = materia(codigo);
        Alumno a = alumnos.findByLegajo(legajo).orElseThrow(() -> new Errores.NoEncontrado("no existe el legajo " + legajo));
        if (inscripciones.findByMateriaCodigoAndAlumnoLegajo(codigo, legajo).isPresent()) {
            throw new Errores.Conflicto("el legajo " + legajo + " ya está inscripto en " + codigo);
        }
        inscripciones.save(new Inscripcion(m, a));
    }

    @Transactional
    public void cargarNota(String codigo, int legajo, int nota) {
        materia(codigo);
        Inscripcion i = inscripciones.findByMateriaCodigoAndAlumnoLegajo(codigo, legajo)
                .orElseThrow(() -> new Errores.Conflicto("el legajo " + legajo + " no está inscripto en " + codigo));
        if (i.getNota() != null) {
            throw new Errores.Conflicto("el legajo " + legajo + " ya tiene nota en " + codigo);
        }
        i.setNota(nota);
    }

    @Transactional(readOnly = true)
    public Dto.Acta acta(String codigo, int pagina) {
        Materia m = materia(codigo);
        Page<Inscripcion> page = inscripciones.findByMateriaCodigo(codigo,
                PageRequest.of(Math.max(pagina, 0), RENGLONES_POR_PAGINA, Sort.by("alumno.apellido", "alumno.nombre")));
        return new Dto.Acta(m.getNombre(), page.getContent().stream().map(ServicioActas::renglon).toList(),
                page.getNumber(), page.getTotalPages(), page.getTotalElements());
    }

    @Transactional(readOnly = true)
    public Dto.Estadisticas estadisticas(String codigo) {
        Materia m = materia(codigo);
        InscripcionRepository.Estadisticas e = inscripciones.estadisticas(codigo);
        double promedio = e.getPromedio() == null ? 0 : Math.round(e.getPromedio() * 100) / 100.0;
        return new Dto.Estadisticas(m.getNombre(), e.getInscriptos(), e.getConNota(), e.getAprobados(), promedio);
    }

    private Materia materia(String codigo) {
        return materias.findByCodigo(codigo).orElseThrow(() -> new Errores.NoEncontrado("no existe la materia " + codigo));
    }

    private static Dto.RenglonActa renglon(Inscripcion i) {
        Integer nota = i.getNota();
        String condicion = nota == null ? "AUSENTE" : nota >= 4 ? "APROBADO" : "DESAPROBADO";
        Alumno a = i.getAlumno();
        return new Dto.RenglonActa(a.getLegajo(), a.getApellido() + ", " + a.getNombre(), nota, condicion);
    }
}
```

`src/main/java/imperio/actas/web/ActasController.java`

```java
package imperio.actas.web;

import imperio.actas.servicio.ServicioActas;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class ActasController {
    private final ServicioActas servicio;

    @PostMapping("/materias")
    @ResponseStatus(HttpStatus.CREATED)
    public void crearMateria(@Valid @RequestBody Dto.MateriaPedido p) {
        servicio.crearMateria(p);
    }

    @PostMapping("/alumnos")
    @ResponseStatus(HttpStatus.CREATED)
    public void crearAlumno(@Valid @RequestBody Dto.AlumnoPedido p) {
        servicio.crearAlumno(p);
    }

    @PostMapping("/materias/{codigo}/inscripciones")
    @ResponseStatus(HttpStatus.CREATED)
    public void inscribir(@PathVariable String codigo, @Valid @RequestBody Dto.InscripcionPedido p) {
        servicio.inscribir(codigo, p.legajo());
    }

    @PostMapping("/materias/{codigo}/notas")
    @ResponseStatus(HttpStatus.CREATED)
    public void cargarNota(@PathVariable String codigo, @Valid @RequestBody Dto.NotaPedido p) {
        servicio.cargarNota(codigo, p.legajo(), p.nota());
    }

    @GetMapping("/materias/{codigo}/acta")
    public Dto.Acta acta(@PathVariable String codigo, @RequestParam(defaultValue = "0") int pagina) {
        return servicio.acta(codigo, pagina);
    }

    @GetMapping("/materias/{codigo}/estadisticas")
    public Dto.Estadisticas estadisticas(@PathVariable String codigo) {
        return servicio.estadisticas(codigo);
    }
}
```

`src/main/java/imperio/actas/web/ManejoDeErrores.java`

```java
package imperio.actas.web;

import java.util.Map;
import java.util.TreeMap;

import imperio.actas.servicio.Errores;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
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
}
```

`src/test/java/imperio/actas/ActasApiTest.java`

```java
package imperio.actas;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.BeforeEach;
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
@DirtiesContext(classMode = DirtiesContext.ClassMode.BEFORE_EACH_TEST_METHOD)
class ActasApiTest {
    @Autowired
    private MockMvc mvc;

    private ResultActions enviar(String ruta, String json) throws Exception {
        return mvc.perform(post(ruta).contentType(MediaType.APPLICATION_JSON).content(json));
    }

    @BeforeEach
    void cargar() throws Exception {
        enviar("/materias", "{\"codigo\": \"PRO01\", \"nombre\": \"Programación I\"}").andExpect(status().isCreated());
        String[][] alumnos = {{"101", "Ruiz", "Ana"}, {"102", "Díaz", "Leo"}, {"103", "Pérez", "Juan"}, {"104", "Acosta", "Mía"}};
        for (String[] a : alumnos) {
            enviar("/alumnos", "{\"legajo\": " + a[0] + ", \"apellido\": \"" + a[1] + "\", \"nombre\": \"" + a[2] + "\"}")
                    .andExpect(status().isCreated());
            enviar("/materias/PRO01/inscripciones", "{\"legajo\": " + a[0] + "}").andExpect(status().isCreated());
        }
    }

    @Test
    void elActaCompletaYSusEstadisticas() throws Exception {
        enviar("/materias/PRO01/notas", "{\"legajo\": 101, \"nota\": 9}").andExpect(status().isCreated());
        enviar("/materias/PRO01/notas", "{\"legajo\": 102, \"nota\": 3}");
        enviar("/materias/PRO01/notas", "{\"legajo\": 104, \"nota\": 6}");
        mvc.perform(get("/materias/PRO01/acta"))
                .andExpect(jsonPath("$.materia").value("Programación I"))
                .andExpect(jsonPath("$.total").value(4))
                .andExpect(jsonPath("$.renglones[0].alumno").value("Acosta, Mía"))
                .andExpect(jsonPath("$.renglones[1].condicion").value("DESAPROBADO"))
                .andExpect(jsonPath("$.renglones[2].condicion").value("AUSENTE"))
                .andExpect(jsonPath("$.renglones[3].nota").value(9));
        mvc.perform(get("/materias/PRO01/estadisticas"))
                .andExpect(jsonPath("$.inscriptos").value(4))
                .andExpect(jsonPath("$.conNota").value(3))
                .andExpect(jsonPath("$.aprobados").value(2))
                .andExpect(jsonPath("$.promedio").value(6.0));
    }

    @Test
    void lasReglasDelNegocio() throws Exception {
        enviar("/materias/PRO01/inscripciones", "{\"legajo\": 101}").andExpect(status().isConflict())
                .andExpect(jsonPath("$.detail").value("el legajo 101 ya está inscripto en PRO01"));
        enviar("/materias/PRO01/inscripciones", "{\"legajo\": 999}").andExpect(status().isNotFound());
        enviar("/alumnos", "{\"legajo\": 105, \"apellido\": \"Soto\", \"nombre\": \"Eva\"}");
        enviar("/materias/PRO01/notas", "{\"legajo\": 105, \"nota\": 8}").andExpect(status().isConflict())
                .andExpect(jsonPath("$.detail").value("el legajo 105 no está inscripto en PRO01"));
        enviar("/materias/PRO01/notas", "{\"legajo\": 101, \"nota\": 8}").andExpect(status().isCreated());
        enviar("/materias/PRO01/notas", "{\"legajo\": 101, \"nota\": 10}").andExpect(status().isConflict());
        mvc.perform(get("/materias/BAS99/acta")).andExpect(status().isNotFound());
    }

    @Test
    void lasValidaciones() throws Exception {
        enviar("/materias", "{\"codigo\": \"prog\", \"nombre\": \"\"}").andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.codigo").value("el código es de 3 letras y 2 números (PRO01)"))
                .andExpect(jsonPath("$.campos.nombre").value("falta el nombre"));
        enviar("/materias/PRO01/notas", "{\"legajo\": 101, \"nota\": 11}").andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.nota").value("la nota va de 1 a 10"));
        enviar("/materias", "{\"codigo\": \"PRO01\", \"nombre\": \"Otra\"}").andExpect(status().isConflict());
    }

    @Test
    void elActaSePagina() throws Exception {
        for (int legajo = 200; legajo < 223; legajo++) {
            enviar("/alumnos", "{\"legajo\": " + legajo + ", \"apellido\": \"Zeta" + legajo + "\", \"nombre\": \"X\"}");
            enviar("/materias/PRO01/inscripciones", "{\"legajo\": " + legajo + "}");
        }
        mvc.perform(get("/materias/PRO01/acta")).andExpect(jsonPath("$.renglones.length()").value(20))
                .andExpect(jsonPath("$.paginas").value(2));
        mvc.perform(get("/materias/PRO01/acta").param("pagina", "1")).andExpect(jsonPath("$.renglones.length()").value(7))
                .andExpect(jsonPath("$.renglones[6].alumno").value("Zeta222, X"));
    }
}
```

### ¿Para qué sirve?

Esto es, casi exactamente, lo que hace un desarrollador *backend* Java en su trabajo: una API con capas, reglas del negocio protegidas, errores claros, base de datos y pruebas. Con este proyecto en tu portfolio (y el de escritorio del Palacio de las Ventanas), podés mostrar que sabés construir un sistema de punta a punta.

### Errores habituales

**Kraken: la regla en el lugar equivocado.** Controlar "ya está inscripto" en el
controlador, o confiar solo en la restricción `unique` de la base (que termina en un 500
con un error de SQL). La regla va en el servicio, con su error claro; la restricción de la
base queda como red de seguridad.

**Dragón: el 500 que se escapa.** Una excepción sin manejar llega al usuario como
`500 Internal Server Error`. Toda situación esperable (no existe, ya existe, no se puede)
tiene su excepción y su código.

**Ogro: la prueba que depende de otra.** Si una prueba usa los datos que dejó otra, el
orden cambia el resultado. Cada prueba arranca de cero (`@DirtiesContext` o limpiando los
repositorios) y carga lo suyo.

**Goblin: el repositorio escondido.** Una interfaz de repositorio declarada **dentro** de
otra clase no se detecta: `No qualifying bean of type …Repositorio`. Cada repositorio va
en su propio archivo.

**Troll: el acta sin orden.** Paginar sin `Sort` da páginas con un orden arbitrario:
un renglón puede aparecer en dos páginas y otro en ninguna.

### Misión S03-N05-M1 · Tu servicio del Puerto

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 40
```

#### Consigna

Construí **tu** API REST completa con Spring Boot y PostgreSQL. Puede ser la de las
actas del ejemplo ampliada o una propia (pedidos de un comercio, turnos de un
consultorio, préstamos de una biblioteca, reservas de canchas). Tiene que tener:

1. Al menos **tres entidades** relacionadas (`@ManyToOne` / `@OneToMany`).
2. Capas separadas: controladores, servicios, repositorios y DTO (ninguna entidad sale
   por la API).
3. Validaciones con Bean Validation y errores 400, 404 y 409 con `ProblemDetail` desde un
   `@RestControllerAdvice`.
4. Al menos **dos reglas del negocio** en el servicio, dentro de transacciones (por
   ejemplo, no vender sin stock y descontarlo al confirmar un pedido).
5. Una consulta JPQL (un resumen, un ranking) y un listado paginado.
6. **Al menos 8 pruebas** con `MockMvc` que cubran los casos felices, las validaciones y
   las reglas del negocio, sobre H2.
7. Un `LEEME.md` con la tabla de rutas (verbo, ruta, qué hace, errores) y cómo
   arrancarla contra PostgreSQL.

Entregá el proyecto en un zip (sin `target`).

#### Criterio de aprobación

- Se cumplen los siete puntos, `./mvnw test` pasa y la aplicación arranca contra PostgreSQL.
- Las reglas del negocio están en el servicio y son transaccionales; ninguna entidad sale por la API.

#### Solución de referencia

Una API de pedidos para un comercio: clientes, productos y pedidos con sus renglones.
Confirmar un pedido descuenta el stock de todos los productos en una sola transacción (si
uno no alcanza, no se descuenta ninguno).

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
    <artifactId>pedidos</artifactId>
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
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
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
spring.datasource.url=jdbc:postgresql://localhost:5432/imperio
spring.datasource.username=imperio
spring.datasource.password=imperio
spring.jpa.hibernate.ddl-auto=update
spring.jpa.open-in-view=false
```

`src/test/resources/application.properties`

```properties
spring.main.banner-mode=off
logging.level.root=warn
spring.datasource.url=jdbc:h2:mem:imperio;MODE=PostgreSQL;DB_CLOSE_DELAY=-1
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.open-in-view=false
```

`LEEME.md`

```md
# API de pedidos

| Verbo y ruta | Hace | Errores |
|---|---|---|
| POST /clientes | crea un cliente | 400, 409 (email repetido) |
| POST /productos | crea un producto | 400, 409 (código repetido) |
| GET /productos?pagina= | productos paginados por nombre | |
| POST /pedidos | crea un pedido BORRADOR con sus renglones | 400, 404 (cliente o producto) |
| POST /pedidos/{id}/confirmacion | confirma y descuenta el stock | 404, 409 (sin stock o ya confirmado) |
| GET /pedidos/{id} | el pedido con sus renglones y total | 404 |
| GET /productos/mas-vendidos | ranking de unidades en pedidos confirmados | |

Arrancar contra PostgreSQL (base, usuario y clave `imperio`): `./mvnw spring-boot:run`.
Pruebas (sobre H2, sin base): `./mvnw test`.
```

`src/main/java/imperio/pedidos/PedidosApplication.java`

```java
package imperio.pedidos;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class PedidosApplication {
    public static void main(String[] args) {
        SpringApplication.run(PedidosApplication.class, args);
    }
}
```

`src/main/java/imperio/pedidos/modelo/Cliente.java`

```java
package imperio.pedidos.modelo;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Cliente {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String nombre;

    @Column(nullable = false, unique = true)
    private String email;

    protected Cliente() {
    }

    public Cliente(String nombre, String email) {
        this.nombre = nombre;
        this.email = email;
    }

    public Long getId() {
        return id;
    }

    public String getNombre() {
        return nombre;
    }
}
```

`src/main/java/imperio/pedidos/modelo/Producto.java`

```java
package imperio.pedidos.modelo;

import java.math.BigDecimal;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Producto {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 20)
    private String codigo;

    @Column(nullable = false)
    private String nombre;

    @Column(nullable = false, precision = 12, scale = 2)
    private BigDecimal precio;

    private int stock;

    protected Producto() {
    }

    public Producto(String codigo, String nombre, BigDecimal precio, int stock) {
        this.codigo = codigo;
        this.nombre = nombre;
        this.precio = precio;
        this.stock = stock;
    }

    public String getCodigo() {
        return codigo;
    }

    public String getNombre() {
        return nombre;
    }

    public BigDecimal getPrecio() {
        return precio;
    }

    public int getStock() {
        return stock;
    }

    public void descontar(int cantidad) {
        stock -= cantidad;
    }
}
```

`src/main/java/imperio/pedidos/modelo/Pedido.java`

```java
package imperio.pedidos.modelo;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;

@Entity
public class Pedido {
    public enum Estado { BORRADOR, CONFIRMADO }

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(optional = false)
    private Cliente cliente;

    @Enumerated(EnumType.STRING)
    private Estado estado = Estado.BORRADOR;

    // Los renglones se guardan y se borran junto con el pedido.
    @OneToMany(mappedBy = "pedido", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Renglon> renglones = new ArrayList<>();

    protected Pedido() {
    }

    public Pedido(Cliente cliente) {
        this.cliente = cliente;
    }

    public void agregar(Producto producto, int cantidad) {
        renglones.add(new Renglon(this, producto, cantidad));
    }

    public BigDecimal total() {
        return renglones.stream().map(Renglon::subtotal).reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    public Long getId() {
        return id;
    }

    public Cliente getCliente() {
        return cliente;
    }

    public Estado getEstado() {
        return estado;
    }

    public void confirmar() {
        estado = Estado.CONFIRMADO;
    }

    public List<Renglon> getRenglones() {
        return renglones;
    }
}
```

`src/main/java/imperio/pedidos/modelo/Renglon.java`

```java
package imperio.pedidos.modelo;

import java.math.BigDecimal;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;

@Entity
public class Renglon {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(optional = false)
    private Pedido pedido;

    @ManyToOne(optional = false)
    private Producto producto;

    private int cantidad;

    // El precio se copia al hacer el pedido: si después cambia, el pedido no cambia.
    @Column(precision = 12, scale = 2)
    private BigDecimal precioUnitario;

    protected Renglon() {
    }

    Renglon(Pedido pedido, Producto producto, int cantidad) {
        this.pedido = pedido;
        this.producto = producto;
        this.cantidad = cantidad;
        this.precioUnitario = producto.getPrecio();
    }

    public Producto getProducto() {
        return producto;
    }

    public int getCantidad() {
        return cantidad;
    }

    public BigDecimal subtotal() {
        return precioUnitario.multiply(BigDecimal.valueOf(cantidad));
    }
}
```

`src/main/java/imperio/pedidos/repositorio/ClienteRepository.java`

```java
package imperio.pedidos.repositorio;

import imperio.pedidos.modelo.Cliente;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ClienteRepository extends JpaRepository<Cliente, Long> {
    boolean existsByEmailIgnoreCase(String email);
}
```

`src/main/java/imperio/pedidos/repositorio/ProductoRepository.java`

```java
package imperio.pedidos.repositorio;

import java.util.List;
import java.util.Optional;

import imperio.pedidos.modelo.Producto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface ProductoRepository extends JpaRepository<Producto, Long> {
    Optional<Producto> findByCodigo(String codigo);

    boolean existsByCodigo(String codigo);

    interface Vendido {
        String getCodigo();

        long getUnidades();
    }

    @Query("""
            select r.producto.codigo as codigo, sum(r.cantidad) as unidades
            from Renglon r
            where r.pedido.estado = imperio.pedidos.modelo.Pedido.Estado.CONFIRMADO
            group by r.producto.codigo
            order by sum(r.cantidad) desc, r.producto.codigo
            """)
    List<Vendido> masVendidos();
}
```

`src/main/java/imperio/pedidos/repositorio/PedidoRepository.java`

```java
package imperio.pedidos.repositorio;

import imperio.pedidos.modelo.Pedido;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PedidoRepository extends JpaRepository<Pedido, Long> {
}
```

`src/main/java/imperio/pedidos/web/Dto.java`

```java
package imperio.pedidos.web;

import java.math.BigDecimal;
import java.util.List;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.PositiveOrZero;

public final class Dto {
    private Dto() {
    }

    public record ClientePedido(@NotBlank(message = "falta el nombre") String nombre,
                                @NotBlank(message = "falta el email") @Email(message = "el email no es válido") String email) {
    }

    public record ProductoPedido(@NotBlank(message = "falta el código") String codigo,
                                 @NotBlank(message = "falta el nombre") String nombre,
                                 @NotNull(message = "falta el precio") @Positive(message = "el precio tiene que ser positivo") BigDecimal precio,
                                 @PositiveOrZero(message = "el stock no puede ser negativo") int stock) {
    }

    public record ProductoVista(String codigo, String nombre, BigDecimal precio, int stock) {
    }

    public record RenglonPedido(@NotBlank(message = "falta el producto") String codigo,
                                @Min(value = 1, message = "la cantidad mínima es 1") int cantidad) {
    }

    public record PedidoPedido(@Min(value = 1, message = "falta el cliente") long clienteId,
                               @NotEmpty(message = "el pedido necesita al menos un renglón") List<@Valid RenglonPedido> renglones) {
    }

    public record RenglonVista(String codigo, String producto, int cantidad, BigDecimal subtotal) {
    }

    public record PedidoVista(long id, String cliente, String estado, List<RenglonVista> renglones, BigDecimal total) {
    }

    public record Pagina<T>(List<T> elementos, int numero, int paginas, long total) {
    }
}
```

`src/main/java/imperio/pedidos/servicio/Errores.java`

```java
package imperio.pedidos.servicio;

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

`src/main/java/imperio/pedidos/servicio/ServicioPedidos.java`

```java
package imperio.pedidos.servicio;

import java.util.List;

import imperio.pedidos.modelo.Cliente;
import imperio.pedidos.modelo.Pedido;
import imperio.pedidos.modelo.Producto;
import imperio.pedidos.modelo.Renglon;
import imperio.pedidos.repositorio.ClienteRepository;
import imperio.pedidos.repositorio.PedidoRepository;
import imperio.pedidos.repositorio.ProductoRepository;
import imperio.pedidos.web.Dto;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ServicioPedidos {
    private final ClienteRepository clientes;
    private final ProductoRepository productos;
    private final PedidoRepository pedidos;

    public ServicioPedidos(ClienteRepository clientes, ProductoRepository productos, PedidoRepository pedidos) {
        this.clientes = clientes;
        this.productos = productos;
        this.pedidos = pedidos;
    }

    @Transactional
    public long crearCliente(Dto.ClientePedido p) {
        if (clientes.existsByEmailIgnoreCase(p.email())) {
            throw new Errores.Conflicto("ya hay un cliente con el email " + p.email());
        }
        return clientes.save(new Cliente(p.nombre(), p.email())).getId();
    }

    @Transactional
    public void crearProducto(Dto.ProductoPedido p) {
        if (productos.existsByCodigo(p.codigo())) {
            throw new Errores.Conflicto("ya existe el producto " + p.codigo());
        }
        productos.save(new Producto(p.codigo(), p.nombre(), p.precio(), p.stock()));
    }

    @Transactional(readOnly = true)
    public Dto.Pagina<Dto.ProductoVista> productos(int pagina) {
        Page<Producto> page = productos.findAll(PageRequest.of(Math.max(pagina, 0), 10, Sort.by("nombre")));
        List<Dto.ProductoVista> elementos = page.getContent().stream()
                .map(p -> new Dto.ProductoVista(p.getCodigo(), p.getNombre(), p.getPrecio(), p.getStock())).toList();
        return new Dto.Pagina<>(elementos, page.getNumber(), page.getTotalPages(), page.getTotalElements());
    }

    @Transactional
    public Dto.PedidoVista crearPedido(Dto.PedidoPedido p) {
        Cliente cliente = clientes.findById(p.clienteId())
                .orElseThrow(() -> new Errores.NoEncontrado("no existe el cliente " + p.clienteId()));
        Pedido pedido = new Pedido(cliente);
        for (Dto.RenglonPedido r : p.renglones()) {
            Producto producto = productos.findByCodigo(r.codigo())
                    .orElseThrow(() -> new Errores.NoEncontrado("no existe el producto " + r.codigo()));
            pedido.agregar(producto, r.cantidad());
        }
        return vista(pedidos.save(pedido));
    }

    // Regla del negocio: se confirma una sola vez y solo si alcanza el stock de TODOS los renglones.
    @Transactional
    public Dto.PedidoVista confirmar(long id) {
        Pedido pedido = buscar(id);
        if (pedido.getEstado() == Pedido.Estado.CONFIRMADO) {
            throw new Errores.Conflicto("el pedido " + id + " ya está confirmado");
        }
        for (Renglon r : pedido.getRenglones()) {
            if (r.getProducto().getStock() < r.getCantidad()) {
                throw new Errores.Conflicto("no alcanza el stock de " + r.getProducto().getCodigo());
            }
            r.getProducto().descontar(r.getCantidad());
        }
        pedido.confirmar();
        return vista(pedido);
    }

    @Transactional(readOnly = true)
    public Dto.PedidoVista verPedido(long id) {
        return vista(buscar(id));
    }

    @Transactional(readOnly = true)
    public List<ProductoRepository.Vendido> masVendidos() {
        return productos.masVendidos();
    }

    private Pedido buscar(long id) {
        return pedidos.findById(id).orElseThrow(() -> new Errores.NoEncontrado("no existe el pedido " + id));
    }

    private static Dto.PedidoVista vista(Pedido p) {
        List<Dto.RenglonVista> renglones = p.getRenglones().stream()
                .map(r -> new Dto.RenglonVista(r.getProducto().getCodigo(), r.getProducto().getNombre(), r.getCantidad(), r.subtotal()))
                .toList();
        return new Dto.PedidoVista(p.getId(), p.getCliente().getNombre(), p.getEstado().name(), renglones, p.total());
    }
}
```

`src/main/java/imperio/pedidos/web/PedidosController.java`

```java
package imperio.pedidos.web;

import java.net.URI;
import java.util.List;

import imperio.pedidos.repositorio.ProductoRepository;
import imperio.pedidos.servicio.ServicioPedidos;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PedidosController {
    private final ServicioPedidos servicio;

    public PedidosController(ServicioPedidos servicio) {
        this.servicio = servicio;
    }

    @PostMapping("/clientes")
    public ResponseEntity<Void> crearCliente(@Valid @RequestBody Dto.ClientePedido p) {
        return ResponseEntity.created(URI.create("/clientes/" + servicio.crearCliente(p))).build();
    }

    @PostMapping("/productos")
    @ResponseStatus(HttpStatus.CREATED)
    public void crearProducto(@Valid @RequestBody Dto.ProductoPedido p) {
        servicio.crearProducto(p);
    }

    @GetMapping("/productos")
    public Dto.Pagina<Dto.ProductoVista> productos(@RequestParam(defaultValue = "0") int pagina) {
        return servicio.productos(pagina);
    }

    @GetMapping("/productos/mas-vendidos")
    public List<ProductoRepository.Vendido> masVendidos() {
        return servicio.masVendidos();
    }

    @PostMapping("/pedidos")
    public ResponseEntity<Dto.PedidoVista> crearPedido(@Valid @RequestBody Dto.PedidoPedido p) {
        Dto.PedidoVista v = servicio.crearPedido(p);
        return ResponseEntity.created(URI.create("/pedidos/" + v.id())).body(v);
    }

    @PostMapping("/pedidos/{id}/confirmacion")
    public Dto.PedidoVista confirmar(@PathVariable long id) {
        return servicio.confirmar(id);
    }

    @GetMapping("/pedidos/{id}")
    public Dto.PedidoVista ver(@PathVariable long id) {
        return servicio.verPedido(id);
    }
}
```

`src/main/java/imperio/pedidos/web/ManejoDeErrores.java`

```java
package imperio.pedidos.web;

import java.util.Map;
import java.util.TreeMap;

import imperio.pedidos.servicio.Errores;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
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
}
```

`src/test/java/imperio/pedidos/PedidosApiTest.java`

```java
package imperio.pedidos;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.BeforeEach;
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
@DirtiesContext(classMode = DirtiesContext.ClassMode.BEFORE_EACH_TEST_METHOD)
class PedidosApiTest {
    @Autowired
    private MockMvc mvc;

    private ResultActions enviar(String ruta, String json) throws Exception {
        return mvc.perform(post(ruta).contentType(MediaType.APPLICATION_JSON).content(json));
    }

    private ResultActions pedido(String renglones) throws Exception {
        return enviar("/pedidos", "{\"clienteId\": 1, \"renglones\": [" + renglones + "]}");
    }

    @BeforeEach
    void cargar() throws Exception {
        enviar("/clientes", "{\"nombre\": \"Marta\", \"email\": \"marta@correo.com\"}").andExpect(status().isCreated());
        enviar("/productos", "{\"codigo\": \"YER\", \"nombre\": \"Yerba\", \"precio\": 4200.50, \"stock\": 10}").andExpect(status().isCreated());
        enviar("/productos", "{\"codigo\": \"AZU\", \"nombre\": \"Azúcar\", \"precio\": 1500, \"stock\": 2}").andExpect(status().isCreated());
    }

    @Test
    void unPedidoCompletoDescuentaElStock() throws Exception {
        pedido("{\"codigo\": \"YER\", \"cantidad\": 3}, {\"codigo\": \"AZU\", \"cantidad\": 2}")
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.estado").value("BORRADOR"))
                .andExpect(jsonPath("$.total").value(15601.5));
        enviar("/pedidos/1/confirmacion", "").andExpect(jsonPath("$.estado").value("CONFIRMADO"));
        mvc.perform(get("/productos"))
                .andExpect(jsonPath("$.elementos[0].nombre").value("Azúcar"))
                .andExpect(jsonPath("$.elementos[0].stock").value(0))
                .andExpect(jsonPath("$.elementos[1].stock").value(7));
    }

    @Test
    void sinStockNoSeDescuentaNinguno() throws Exception {
        pedido("{\"codigo\": \"YER\", \"cantidad\": 5}, {\"codigo\": \"AZU\", \"cantidad\": 3}");
        enviar("/pedidos/1/confirmacion", "").andExpect(status().isConflict())
                .andExpect(jsonPath("$.detail").value("no alcanza el stock de AZU"));
        mvc.perform(get("/productos")).andExpect(jsonPath("$.elementos[1].stock").value(10));
        mvc.perform(get("/pedidos/1")).andExpect(jsonPath("$.estado").value("BORRADOR"));
    }

    @Test
    void noSeConfirmaDosVeces() throws Exception {
        pedido("{\"codigo\": \"YER\", \"cantidad\": 1}");
        enviar("/pedidos/1/confirmacion", "").andExpect(status().isOk());
        enviar("/pedidos/1/confirmacion", "").andExpect(status().isConflict())
                .andExpect(jsonPath("$.detail").value("el pedido 1 ya está confirmado"));
    }

    @Test
    void elPrecioDelPedidoQuedaFijo() throws Exception {
        pedido("{\"codigo\": \"YER\", \"cantidad\": 2}");
        mvc.perform(get("/pedidos/1")).andExpect(jsonPath("$.renglones[0].subtotal").value(8401.0));
    }

    @Test
    void losInexistentesDan404() throws Exception {
        pedido("{\"codigo\": \"ARR\", \"cantidad\": 1}").andExpect(status().isNotFound())
                .andExpect(jsonPath("$.detail").value("no existe el producto ARR"));
        enviar("/pedidos", "{\"clienteId\": 9, \"renglones\": [{\"codigo\": \"YER\", \"cantidad\": 1}]}").andExpect(status().isNotFound());
        mvc.perform(get("/pedidos/5")).andExpect(status().isNotFound());
    }

    @Test
    void lasValidaciones() throws Exception {
        enviar("/pedidos", "{\"clienteId\": 1, \"renglones\": []}").andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.renglones").value("el pedido necesita al menos un renglón"));
        pedido("{\"codigo\": \"YER\", \"cantidad\": 0}").andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos['renglones[0].cantidad']").value("la cantidad mínima es 1"));
        enviar("/productos", "{\"codigo\": \"\", \"nombre\": \"X\", \"precio\": -1, \"stock\": -2}").andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.campos.precio").value("el precio tiene que ser positivo"))
                .andExpect(jsonPath("$.campos.stock").value("el stock no puede ser negativo"));
    }

    @Test
    void losRepetidosDan409() throws Exception {
        enviar("/clientes", "{\"nombre\": \"Otra\", \"email\": \"MARTA@correo.com\"}").andExpect(status().isConflict());
        enviar("/productos", "{\"codigo\": \"YER\", \"nombre\": \"Otra\", \"precio\": 1, \"stock\": 1}").andExpect(status().isConflict());
    }

    @Test
    void elRankingSoloCuentaLosConfirmados() throws Exception {
        pedido("{\"codigo\": \"YER\", \"cantidad\": 2}, {\"codigo\": \"AZU\", \"cantidad\": 1}");
        pedido("{\"codigo\": \"YER\", \"cantidad\": 4}");
        pedido("{\"codigo\": \"AZU\", \"cantidad\": 1}");
        enviar("/pedidos/1/confirmacion", "");
        enviar("/pedidos/2/confirmacion", "");
        mvc.perform(get("/productos/mas-vendidos"))
                .andExpect(jsonPath("$.length()").value(2))
                .andExpect(jsonPath("$[0].codigo").value("YER"))
                .andExpect(jsonPath("$[0].unidades").value(6))
                .andExpect(jsonPath("$[1].unidades").value(1));
    }
}
```

### Prueba del sello

#### ¿Qué capas tiene un servicio web bien organizado y qué hace cada una?

El controlador recibe y responde con DTO; el servicio tiene las reglas del negocio y las transacciones; el repositorio accede a la base; las entidades representan las tablas.

#### ¿Dónde va una regla como "no se vende sin stock"?

En el servicio, dentro de una transacción, con una excepción propia que el *advice* convierte en un 409.

#### ¿Por qué el renglón del pedido guarda el precio?

Para que el pedido no cambie si después cambia el precio del producto.

#### ¿Qué garantiza `@Transactional` al confirmar un pedido con varios productos?

Que se descuenta el stock de todos o de ninguno: si uno falla, se deshace todo.

### Soluciones (docente)

Jefe de la Senda del Puerto de Spring. El ejemplo reutiliza el dominio del jefe del Palacio de las Ventanas (las actas) para que se vea el mismo sistema como servicio web. Se corrige corriendo `./mvnw test`, arrancando la aplicación contra PostgreSQL y probando un par de rutas con `curl` a partir del `LEEME.md`.
