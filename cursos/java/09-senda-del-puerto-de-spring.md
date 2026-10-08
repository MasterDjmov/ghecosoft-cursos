# RAMA S04 · Senda del Puerto de Spring: persistencia con JPA

```meta
tipo: senda
posicion: 9
```

## S04-N01 · JPA: la bóveda del Puerto

```meta
tipo: tema
padre: R05-N07
criatura: skeleton
ejecutable: no
temas: sql.orm
usa: fw.spring, sql.modelo
precio: 3
requiere: S01-N02
moneda: comodin
```

### Crónica

Debajo del Puerto hay una bóveda como la de la Senda de la Bóveda, pero sin escribas. Cuando un capitán guarda un cargamento, unos espíritus lo anotan solos en las tablas, arman las consultas y hasta crean los estantes si faltan.

—En la Bóveda Imperial escribías cada `INSERT` y cada `ResultSet` a mano —dice {mentor}—. Estaba bien: ahora sabés lo que pasa por debajo. En el Puerto, **JPA** hace ese trabajo: vos decís qué clase va en qué tabla, y los repositorios aparecen solos. Pero ojo, Zed: los espíritus hacen lo que les pedís, no lo que querías pedir.

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
`src/main/resources/application.properties` apunta a la base `imperio` de la Senda de la Bóveda:
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

### Misión S04-N01-M1 · El inventario persistente

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

### Misión S04-N01-M2 · Autores y libros

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

### Misión S04-N01-M3 · La transferencia transaccional

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

### Encargo S04-N01-E1 · El padrón paginado

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

## S04-N02 · Jefe del Puerto: el Kraken de los Servicios

```meta
tipo: jefe
padre: S04-N01
precio: 10
criatura: dragon
ejecutable: no
insignia: Capitán del Puerto de Spring
insignia_descripcion: Venciste al Kraken de los Servicios: construiste una API REST completa con Spring Boot, JPA y pruebas.
usa: fw.spring, web.api-rest, sql.orm, diseno.capas
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

### Misión S04-N02-M1 · Tu servicio del Puerto

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
