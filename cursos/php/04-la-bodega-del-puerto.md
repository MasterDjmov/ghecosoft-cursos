# RAMA R04 · La Bodega del Puerto: MySQL y MariaDB

```meta
tipo: tronco
posicion: 4
```

## R04-N01 · Bases de datos y MariaDB

```meta
tipo: tema
padre: R03-N09
precio: 10
criatura: slime
```

### Crónica

Debajo de la torre, bajando una escalera de piedra, está la **Bodega del Puerto**: galerías enteras de estanterías, cada una con fichas ordenadas en columnas iguales. Un bodeguero anciano encuentra cualquier ficha en segundos, aunque haya millones, y nunca deja entrar una ficha mal completada.

—Los archivos JSON sirvieron para empezar —dice {mentor}—, pero cuando llegan mil pedidos a la vez, se traban y se mezclan. Los sistemas serios guardan todo en una **base de datos**: un programa especializado en guardar, ordenar y buscar. Acá usamos **MariaDB**, {heroe}, que habla SQL: la lengua de las bodegas de todo el mundo.

### Objetivos

- Entender qué es una base de datos relacional: tablas, filas y columnas.
- Instalar MariaDB (o MySQL) y conectarse con la consola y con phpMyAdmin.
- Crear una base y tablas con tipos, clave primaria y restricciones.
- Cargar datos con `INSERT` y verlos con `SELECT`.
- Ejecutar un script SQL desde un archivo.

### Antes de empezar

- La Oficina de Correos (rama 3), en especial guardar datos en JSON (R03-N07).

### Explicación

#### ¿Por qué una base de datos?
Un archivo JSON se lee y se escribe **entero** cada vez, dos pedidos al mismo tiempo
pueden pisarse, y buscar "los pedidos de octubre de más de $10000" obliga a
recorrer todo. Una **base de datos** resuelve eso: guarda millones de registros,
busca rápido, deja trabajar a muchos a la vez y **no deja entrar datos inválidos**.

Una base **relacional** guarda los datos en **tablas**: cada **fila** es un
registro (un barco) y cada **columna** es un dato con un tipo fijo (nombre,
capacidad). Se maneja con **SQL**, un lenguaje para pedirle cosas a la base.

#### MariaDB y MySQL
**MariaDB** nació como una copia libre de **MySQL** y hoy son casi iguales: todo lo
de este curso funciona en los dos. Los hostings compartidos (cPanel) traen uno u
otro.

- **Windows**: XAMPP ya trae MariaDB. Abrí el panel de XAMPP y dale **Start** a
  *MySQL*. Para administrarla con el navegador está **phpMyAdmin**
  (`http://localhost/phpmyadmin`). El usuario es `root` **sin contraseña**.
- **Linux**: `sudo apt install mariadb-server`, y para entrar la primera vez
  `sudo mariadb`. Conviene crear un usuario para tus pruebas (ver abajo).

La consola:
```bash
mariadb -u root -p          # pide la contraseña (en XAMPP, Enter vacío). En MySQL: mysql -u root -p
```
Adentro se escriben instrucciones SQL terminadas en `;`. Se sale con `exit`.

#### Crear la base
```sql
CREATE DATABASE puerto CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE puerto;
```
`utf8mb4` es el UTF-8 completo (tildes, ñ y emojis). Siempre `utf8mb4`: el viejo
`utf8` de MySQL no guarda todos los caracteres.

En Linux, para no usar `root` en tus programas:
```sql
CREATE USER 'puerto'@'localhost' IDENTIFIED BY 'una-clave-larga';
GRANT ALL PRIVILEGES ON puerto.* TO 'puerto'@'localhost';
```
En el curso los ejemplos usan `root` sin clave (lo de XAMPP); cambialo por tu
usuario si hace falta.

#### Crear una tabla
```sql
CREATE TABLE barco (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL UNIQUE,
    capacidad DECIMAL(8, 2) NOT NULL CHECK (capacidad > 0),
    tipo ENUM('velero', 'pesquero', 'carguero') NOT NULL DEFAULT 'velero',
    botado DATE NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);
```
| Tipo | Para | Ejemplo |
|---|---|---|
| `INT` | enteros | `42` |
| `DECIMAL(8,2)` | plata y medidas exactas (8 cifras, 2 decimales) | `1200.50` |
| `VARCHAR(40)` | textos cortos, hasta 40 caracteres | `'Gaviota'` |
| `TEXT` | textos largos | una descripción |
| `DATE`, `DATETIME` | fechas, fechas con hora | `'2026-10-03'`, `'2026-10-03 09:40:00'` |
| `BOOLEAN` | sí/no (se guarda como `1`/`0`) | `TRUE` |
| `ENUM('a','b')` | uno de una lista fija | `'velero'` |

Restricciones (las reglas que la base **no deja romper**):
- **`PRIMARY KEY`**: identifica cada fila; no se repite. Con **`AUTO_INCREMENT`**, la
  base le pone el número sola (1, 2, 3…).
- **`NOT NULL`**: obligatorio. `NULL` significa "sin dato" (no es lo mismo que `0`
  ni que `''`).
- **`UNIQUE`**: no se repite (un email, una patente).
- **`DEFAULT`**: el valor si no se indica.
- **`CHECK`**: una condición que tiene que cumplirse.

#### Cargar datos
```sql
INSERT INTO barco (nombre, capacidad, tipo, botado)
VALUES ('Gaviota', 450, 'velero', '2019-04-12'),
       ('Albatros', 1200.5, 'carguero', NULL);
```
- Los textos y las fechas van entre comillas simples; los números, sin comillas.
- Las fechas se escriben `'AAAA-MM-DD'`.
- No se pone el `id`: lo genera `AUTO_INCREMENT`.

#### Ver los datos
```sql
SELECT * FROM barco;                          -- todas las columnas
SELECT nombre, capacidad FROM barco;          -- algunas
```
`--` es un comentario en SQL.

#### Cuando la base dice que no
```
ERROR 1062 (23000): Duplicate entry 'Gaviota' for key 'nombre'
ERROR 4025 (23000): CONSTRAINT `barco.capacidad` failed for `puerto`.`barco`
ERROR 1364 (HY000): Field 'capacidad' doesn't have a default value
```
Esa es la gran ventaja: la base **rechaza** los datos que rompen las reglas, aunque
tu programa se olvide de validarlos.

#### Scripts
En lugar de escribir instrucción por instrucción, se guardan en un archivo
`.sql` y se ejecutan juntas:
```bash
mariadb -u root -p -t puerto < barcos.sql      # -t muestra los resultados como tablas
```
(en phpMyAdmin: pestaña **SQL**, pegar y **Continuar**, o **Importar** el archivo).
Conviene empezar los scripts con `DROP TABLE IF EXISTS …;` para poder ejecutarlos
muchas veces.

### Código de ejemplo

```sql
-- La primera estantería de la Bodega: crear, cargar y consultar.
DROP TABLE IF EXISTS barco;

CREATE TABLE barco (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL UNIQUE,
    capacidad DECIMAL(8, 2) NOT NULL CHECK (capacidad > 0),
    tipo ENUM('velero', 'pesquero', 'carguero') NOT NULL DEFAULT 'velero',
    botado DATE NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO barco (nombre, capacidad, tipo, botado) VALUES
    ('Gaviota', 450, 'velero', '2019-04-12'),
    ('Albatros', 1200.5, 'carguero', '2026-08-20'),
    ('Tortuga', 80, 'pesquero', '1998-01-05'),
    ('Ñandú', 300, 'velero', NULL);

INSERT INTO barco (nombre, capacidad) VALUES ('Brisa', 120);

SELECT * FROM barco;
SELECT nombre, tipo, capacidad FROM barco;
```

### Salida esperada

```
+----+----------+-----------+----------+------------+--------+
| id | nombre   | capacidad | tipo     | botado     | activo |
+----+----------+-----------+----------+------------+--------+
|  1 | Gaviota  |    450.00 | velero   | 2019-04-12 |      1 |
|  2 | Albatros |   1200.50 | carguero | 2026-08-20 |      1 |
|  3 | Tortuga  |     80.00 | pesquero | 1998-01-05 |      1 |
|  4 | Ñandú    |    300.00 | velero   | NULL       |      1 |
|  5 | Brisa    |    120.00 | velero   | NULL       |      1 |
+----+----------+-----------+----------+------------+--------+
+----------+----------+-----------+
| nombre   | tipo     | capacidad |
+----------+----------+-----------+
| Gaviota  | velero   |    450.00 |
| Albatros | carguero |   1200.50 |
| Tortuga  | pesquero |     80.00 |
| Ñandú    | velero   |    300.00 |
| Brisa    | velero   |    120.00 |
+----------+----------+-----------+
```

### ¿Para qué sirve?

Detrás de casi cualquier sistema hay una base de datos: WordPress guarda las entradas en MySQL, las tiendas online sus productos y pedidos, los bancos sus movimientos, esta misma plataforma sus alumnos y entregas (en MariaDB). Diseñar bien las tablas, con los tipos y las restricciones correctas, es lo que evita la mitad de los errores de un sistema.

### Errores habituales

**Slime: la coma de más o de menos.** En `CREATE TABLE`, cada columna va separada
por coma, pero **la última no lleva**: `activo BOOLEAN,\n);` da `You have an error in
your SQL syntax`.

**Goblin: comillas dobles o sin comillas en los textos.** En SQL los textos van entre
comillas **simples**: `'Gaviota'`. Sin comillas, la base cree que es el nombre de
una columna: `Unknown column 'Gaviota' in 'field list'`.

**Ogro: `FLOAT` para plata.** Igual que en PHP, los `FLOAT` no son exactos. Para
precios, `DECIMAL(10, 2)`.

**Goblin: la fecha en formato argentino.** `'03/10/2026'` no es una fecha válida para
la base: se escribe `'2026-10-03'`.

**Slime: el `;` que falta en la consola.** La consola no ejecuta hasta que escribís
`;` (queda esperando con `->`).

### Misión R04-N01-M1 · La tabla de pasajeros

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí un script SQL que cree la tabla `pasajero` con:

- `id` entero autoincremental, clave primaria;
- `nombre` (hasta 60 caracteres, obligatorio);
- `dni` (8 caracteres, obligatorio y único);
- `edad` (entero, obligatorio, con `CHECK` entre 0 y 120);
- `nacionalidad` (hasta 30 caracteres, por defecto `'argentina'`);
- `vip` (booleano, por defecto falso).

Cargá cuatro pasajeros (uno sin indicar nacionalidad ni `vip`) y mostralos todos.
Empezá el script con `DROP TABLE IF EXISTS`.

#### Criterio de aprobación

- Usa `PRIMARY KEY`, `AUTO_INCREMENT`, `NOT NULL`, `UNIQUE`, `CHECK` y `DEFAULT`.
- La salida coincide con la esperada.

#### Salida esperada

```
+----+--------------------+----------+------+--------------+-----+
| id | nombre             | dni      | edad | nacionalidad | vip |
+----+--------------------+----------+------+--------------+-----+
|  1 | Kira Valdez        | 40111222 |   17 | argentina    |   0 |
|  2 | Bron de las Forjas | 25333444 |   45 | chilena      |   1 |
|  3 | Lía del Valle      | 38555666 |   29 | uruguaya     |   0 |
|  4 | Olmo Ríos          | 41777888 |   33 | argentina    |   0 |
+----+--------------------+----------+------+--------------+-----+
```

#### Solución de referencia

```sql
-- Mision 1 - La tabla de pasajeros: tipos y restricciones.
DROP TABLE IF EXISTS pasajero;

CREATE TABLE pasajero (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    dni CHAR(8) NOT NULL UNIQUE,
    edad INT NOT NULL CHECK (edad BETWEEN 0 AND 120),
    nacionalidad VARCHAR(30) NOT NULL DEFAULT 'argentina',
    vip BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO pasajero (nombre, dni, edad, nacionalidad, vip) VALUES
    ('Kira Valdez', '40111222', 17, 'argentina', FALSE),
    ('Bron de las Forjas', '25333444', 45, 'chilena', TRUE),
    ('Lía del Valle', '38555666', 29, 'uruguaya', FALSE);
INSERT INTO pasajero (nombre, dni, edad) VALUES ('Olmo Ríos', '41777888', 33);

SELECT * FROM pasajero;
```

### Misión R04-N01-M2 · El inventario de la bodega

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La bodega guarda productos. Creá la tabla `producto` con `codigo` (texto de 6
caracteres, **clave primaria**, no autoincremental), `descripcion` (hasta 80),
`precio` (`DECIMAL` con 2 decimales, mayor que 0), `stock` (entero, no negativo, por
defecto 0), `categoria` (`ENUM` con `almacen`, `limpieza`, `bebidas`) y `vence`
(fecha, puede faltar). Cargá seis productos (dos sin fecha de vencimiento, uno sin
stock indicado) y mostrá solo el código, la descripción y el precio.

#### Criterio de aprobación

- La clave primaria es el código (texto).
- Usa `DECIMAL`, `ENUM`, `CHECK` y `DEFAULT`.
- La salida coincide con la esperada.

#### Salida esperada

```
+--------+-------------------------+---------+
| codigo | descripcion             | precio  |
+--------+-------------------------+---------+
| ALM001 | Yerba mate 1 kg         | 4200.00 |
| ALM002 | Fideos tirabuzón 500 g  | 1100.00 |
| ALM003 | Dulce de cayote 500 g   | 5800.00 |
| BEB001 | Agua mineral 2 l        | 1300.00 |
| BEB002 | Vino torrontés 750 ml   | 6800.00 |
| LIM001 | Lavandina 1 l           |  950.00 |
+--------+-------------------------+---------+
```

#### Solución de referencia

```sql
-- Mision 2 - El inventario de la bodega: una clave primaria de texto.
DROP TABLE IF EXISTS producto;

CREATE TABLE producto (
    codigo CHAR(6) PRIMARY KEY,
    descripcion VARCHAR(80) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio > 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    categoria ENUM('almacen', 'limpieza', 'bebidas') NOT NULL,
    vence DATE NULL
);

INSERT INTO producto (codigo, descripcion, precio, stock, categoria, vence) VALUES
    ('ALM001', 'Yerba mate 1 kg', 4200, 40, 'almacen', '2027-06-30'),
    ('ALM002', 'Fideos tirabuzón 500 g', 1100, 60, 'almacen', '2027-02-15'),
    ('LIM001', 'Lavandina 1 l', 950, 25, 'limpieza', NULL),
    ('BEB001', 'Agua mineral 2 l', 1300, 48, 'bebidas', '2027-01-10'),
    ('BEB002', 'Vino torrontés 750 ml', 6800, 12, 'bebidas', NULL);
INSERT INTO producto (codigo, descripcion, precio, categoria, vence) VALUES
    ('ALM003', 'Dulce de cayote 500 g', 5800, 'almacen', '2026-12-31');

SELECT codigo, descripcion, precio FROM producto;
```

### Misión R04-N01-M3 · La tabla que no se deja

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Esta tabla de socios se diseñó sin reglas y quedó llena de basura: un socio sin
nombre, dos con el mismo DNI, una cuota negativa. Reescribí el `CREATE TABLE` con
las restricciones necesarias para que la base **rechace** esos datos:

- el nombre es obligatorio;
- el DNI es obligatorio y único;
- la cuota es obligatoria y mayor que 0 (con dos decimales);
- la categoría es una de `activo`, `cadete`, `vitalicio` (por defecto `activo`);
- la fecha de alta es obligatoria.

Cargá solo los socios **válidos** del código inicial (corregí la fecha que está en
formato argentino) y mostrálos. En un comentario al final del script, anotá qué
error daría cada uno de los inválidos si lo intentaras cargar.

#### Criterio de aprobación

- Las restricciones impiden los datos inválidos del código inicial.
- Se cargan solo los válidos, con la fecha en formato `AAAA-MM-DD`.
- La salida coincide con la esperada.

#### Código inicial

```sql
CREATE TABLE socio (id INT, nombre VARCHAR(50), dni VARCHAR(8), cuota FLOAT, categoria VARCHAR(20), alta VARCHAR(10));
INSERT INTO socio VALUES (1, 'Ana Pérez', '30111222', 12000, 'activo', '2024-03-01');
INSERT INTO socio VALUES (2, NULL, '31222333', 12000, 'activo', '2024-05-10');
INSERT INTO socio VALUES (3, 'Beto Díaz', '30111222', 8000, 'cadete', '2025-01-15');
INSERT INTO socio VALUES (4, 'Caro Ríos', '32333444', -500, 'activo', '2025-02-20');
INSERT INTO socio VALUES (5, 'Dani Luna', '33444555', 0, 'vitalicio', '15/08/2023');
```

#### Salida esperada

```
+----+------------+----------+----------+-----------+------------+
| id | nombre     | dni      | cuota    | categoria | alta       |
+----+------------+----------+----------+-----------+------------+
|  1 | Ana Pérez  | 30111222 | 12000.00 | activo    | 2024-03-01 |
+----+------------+----------+----------+-----------+------------+
```

#### Solución de referencia

```sql
-- Mision 3 - La tabla que no se deja: las restricciones rechazan la basura.
DROP TABLE IF EXISTS socio;

CREATE TABLE socio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    dni CHAR(8) NOT NULL UNIQUE,
    cuota DECIMAL(10, 2) NOT NULL CHECK (cuota > 0),
    categoria ENUM('activo', 'cadete', 'vitalicio') NOT NULL DEFAULT 'activo',
    alta DATE NOT NULL
);

INSERT INTO socio (nombre, dni, cuota, categoria, alta) VALUES
    ('Ana Pérez', '30111222', 12000, 'activo', '2024-03-01');

SELECT * FROM socio;

-- Los inválidos:
-- (2) nombre NULL           → ERROR 1048: Column 'nombre' cannot be null
-- (3) DNI 30111222 repetido → ERROR 1062: Duplicate entry '30111222' for key 'dni'
-- (4) cuota -500            → ERROR 4025: CONSTRAINT `socio.cuota` failed
-- (5) cuota 0 y fecha '15/08/2023' → la cuota no pasa el CHECK; la fecha se escribe '2023-08-15'
```

### Encargo R04-N01-E1 · La base del consultorio

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un consultorio médico quiere empezar a usar una base de datos. Diseñá la tabla
`paciente` pensando qué datos hacen falta y qué reglas tienen: nombre y apellido
(separados), DNI (único), fecha de nacimiento, teléfono, email (opcional pero
único si está), obra social (una lista fija de 4 más `particular`, por defecto
`particular`), número de afiliado (opcional) y la fecha y hora del alta (por defecto,
el momento en que se carga: `DEFAULT CURRENT_TIMESTAMP`). Cargá cinco pacientes y
mostrá el apellido, el nombre, la obra social y el afiliado (no muestres la columna
del alta, que depende del momento en que se ejecuta).

#### Criterio de aprobación

- Cada columna tiene el tipo y las restricciones que corresponden.
- Usa `DEFAULT CURRENT_TIMESTAMP` para el alta.
- La salida coincide con la esperada.

#### Salida esperada

```
+----------+--------+-------------+-----------+
| apellido | nombre | obra_social | afiliado  |
+----------+--------+-------------+-----------+
| Pérez    | Ana    | APOS        | A-55120   |
| Díaz     | Beto   | PAMI        | 150998877 |
| Gómez    | Carla  | OSPRERA     | OS-7788   |
| Ruiz     | Diego  | particular  | NULL      |
| Sosa     | Elena  | particular  | NULL      |
+----------+--------+-------------+-----------+
```

#### Solución de referencia

```sql
-- Encargo - La base del consultorio: diseñar una tabla con sus reglas.
DROP TABLE IF EXISTS paciente;

CREATE TABLE paciente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    dni CHAR(8) NOT NULL UNIQUE,
    nacimiento DATE NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(100) NULL UNIQUE,
    obra_social ENUM('OSPRERA', 'IOSFA', 'PAMI', 'APOS', 'particular') NOT NULL DEFAULT 'particular',
    afiliado VARCHAR(20) NULL,
    alta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO paciente (nombre, apellido, dni, nacimiento, telefono, email, obra_social, afiliado) VALUES
    ('Ana', 'Pérez', '30111222', '1983-05-14', '380-4123456', 'ana@correo.com', 'APOS', 'A-55120'),
    ('Beto', 'Díaz', '25333444', '1976-11-02', '380-4555666', NULL, 'PAMI', '150998877'),
    ('Carla', 'Gómez', '42555666', '2000-02-29', '380-4999000', 'carla@correo.com', 'OSPRERA', 'OS-7788');
INSERT INTO paciente (nombre, apellido, dni, nacimiento, telefono) VALUES
    ('Diego', 'Ruiz', '38777888', '1995-07-21', '380-4222333'),
    ('Elena', 'Sosa', '29888999', '1981-09-09', '380-4777111');

SELECT apellido, nombre, obra_social, afiliado FROM paciente;
```

### Prueba del sello

#### ¿Qué es una tabla en una base relacional?

Un conjunto de filas (registros) con las mismas columnas (datos), cada columna con un tipo fijo.

#### ¿Para qué sirve `PRIMARY KEY` con `AUTO_INCREMENT`?

Para identificar cada fila con un número único que la base asigna sola (1, 2, 3…).

#### ¿Qué tipo se usa para guardar precios y por qué?

`DECIMAL(10, 2)`, porque guarda los decimales exactos (los `FLOAT` no).

#### ¿Qué significa `NULL` en una columna?

Que no hay dato. No es lo mismo que `0` ni que un texto vacío.

#### ¿Por qué conviene poner restricciones (`NOT NULL`, `UNIQUE`, `CHECK`) en la base?

Porque la base rechaza los datos inválidos aunque el programa se olvide de validarlos.

### Soluciones (docente)

Nodo nuevo: el capítulo original usaba SQLite (`21-PHP/17-PDO-SQLite`); a pedido del docente el curso se orienta a MySQL/MariaDB. Las salidas son las de `mariadb -t puerto < script.sql` (MariaDB 10.11; en MySQL 8 son iguales). Con XAMPP en Windows, se pueden ejecutar desde la pestaña SQL de phpMyAdmin. El `CHECK` se respeta desde MariaDB 10.2 y MySQL 8.0.16.

## R04-N02 · Consultas: filtrar, ordenar y agrupar

```meta
tipo: tema
padre: R04-N01
precio: 10
criatura: ogre
```

### Crónica

Al bodeguero anciano le llegan preguntas todo el día: *"¿qué barcos de más de 500 kilos salieron en octubre?"*, *"¿cuánto facturó cada muelle?"*, *"¿quién pidió yerba y no la retiró?"*. Él no recorre las estanterías una por una: escribe la pregunta en un papel con palabras precisas y la bodega le devuelve exactamente lo pedido.

—Ese papel es una **consulta** —dice {mentor}—. `SELECT` elige qué columnas, `WHERE` qué filas, `ORDER BY` en qué orden, y `GROUP BY` junta y resume. Con cuatro palabras le preguntás cualquier cosa a millones de fichas, {heroe}. Y con otras dos, las cambiás o las borrás… con mucho cuidado.

### Objetivos

- Filtrar filas con `WHERE`: comparaciones, `AND`/`OR`, `IN`, `BETWEEN`, `LIKE` e `IS NULL`.
- Ordenar con `ORDER BY` y limitar con `LIMIT`.
- Calcular con funciones: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `ROUND`, `CONCAT`, `DATE_FORMAT`.
- Agrupar con `GROUP BY` y filtrar grupos con `HAVING`.
- Modificar con `UPDATE` y borrar con `DELETE`, siempre con `WHERE`.

### Antes de empezar

- Crear tablas y cargar datos (R04-N01).

### Explicación

#### Filtrar con `WHERE`
```sql
SELECT nombre, capacidad FROM barco WHERE capacidad > 500;
SELECT * FROM barco WHERE tipo = 'velero' AND activo = TRUE;
SELECT * FROM barco WHERE tipo = 'velero' OR capacidad < 100;
SELECT * FROM barco WHERE tipo IN ('velero', 'pesquero');
SELECT * FROM barco WHERE capacidad BETWEEN 100 AND 500;       -- incluye los extremos
SELECT * FROM barco WHERE nombre LIKE 'G%';                    -- empieza con G
SELECT * FROM barco WHERE nombre LIKE '%a%';                   -- contiene una a
SELECT * FROM barco WHERE botado IS NULL;                      -- sin fecha
```
- En `LIKE`, `%` es "cualquier cosa" y `_` es "un carácter".
- Con `NULL` **no** se usa `=`: `botado = NULL` nunca es verdadero. Se usa `IS NULL`
  o `IS NOT NULL`.
- Con la colación `utf8mb4_unicode_ci`, las comparaciones de texto **no distinguen
  mayúsculas ni tildes**: `'gaviota' = 'Gaviota'` es verdadero.

#### Ordenar y limitar
```sql
SELECT * FROM barco ORDER BY capacidad DESC;              -- de mayor a menor
SELECT * FROM barco ORDER BY tipo, nombre;                -- por tipo y, a igual tipo, por nombre
SELECT * FROM barco ORDER BY capacidad DESC LIMIT 3;      -- los 3 más grandes
SELECT * FROM barco ORDER BY id LIMIT 3 OFFSET 3;         -- saltea 3 y trae 3 (la "página 2")
```
Sin `ORDER BY`, la base devuelve las filas en el orden que le resulte cómodo: si
el orden importa, **pedilo**.

Un detalle: una columna `ENUM` se ordena por el **orden en que declaraste los
valores**, no alfabéticamente. Con `ENUM('almacen', 'limpieza', 'bebidas')`,
`ORDER BY categoria` da almacén, limpieza, bebidas. Para orden alfabético:
`ORDER BY CAST(categoria AS CHAR)`.

#### Calcular y renombrar
```sql
SELECT nombre, capacidad * 1000 AS gramos FROM barco;          -- AS pone un nombre a la columna
SELECT CONCAT(nombre, ' (', tipo, ')') AS etiqueta FROM barco;
SELECT nombre, DATE_FORMAT(botado, '%d/%m/%Y') AS fecha FROM barco;
SELECT nombre, YEAR(botado) AS anio FROM barco;
```

#### Resumir: funciones de agregado
```sql
SELECT COUNT(*) AS barcos, SUM(capacidad) AS total, ROUND(AVG(capacidad), 1) AS promedio,
       MIN(capacidad) AS menor, MAX(capacidad) AS mayor
FROM barco;
```
`COUNT(*)` cuenta filas; `COUNT(botado)` cuenta las que **no** tienen `NULL` en esa
columna.

#### Agrupar con `GROUP BY`
Para resumir **por categoría**:
```sql
SELECT tipo, COUNT(*) AS cantidad, SUM(capacidad) AS capacidad_total
FROM barco
GROUP BY tipo
ORDER BY capacidad_total DESC;
```
Cada grupo da una fila. Las columnas del `SELECT` tienen que ser las del `GROUP BY`
o funciones de agregado.

`HAVING` filtra **grupos** (después de agrupar), `WHERE` filtra **filas** (antes):
```sql
SELECT tipo, COUNT(*) AS cantidad FROM barco
WHERE activo = TRUE          -- primero: solo los activos
GROUP BY tipo
HAVING COUNT(*) >= 2;        -- después: solo los tipos con 2 o más
```

#### Modificar y borrar
```sql
UPDATE barco SET capacidad = capacidad * 1.1 WHERE tipo = 'carguero';
UPDATE barco SET activo = FALSE, botado = '2020-01-01' WHERE id = 3;
DELETE FROM barco WHERE activo = FALSE;
```
**Un `UPDATE` o un `DELETE` sin `WHERE` cambia o borra TODA la tabla.** Antes de
ejecutarlos, probá el mismo `WHERE` con un `SELECT` para ver qué filas toca.

#### El orden de las partes
```sql
SELECT … FROM … WHERE … GROUP BY … HAVING … ORDER BY … LIMIT …;
```
Siempre en ese orden.

### Código de ejemplo

```sql
-- Las preguntas del bodeguero: filtrar, ordenar, agrupar y modificar.
DROP TABLE IF EXISTS viaje;

CREATE TABLE viaje (
    id INT AUTO_INCREMENT PRIMARY KEY,
    barco VARCHAR(40) NOT NULL,
    muelle TINYINT NOT NULL,
    destino VARCHAR(40) NOT NULL,
    fecha DATE NOT NULL,
    kilos DECIMAL(8, 2) NOT NULL,
    pasajeros INT NOT NULL DEFAULT 0,
    observaciones VARCHAR(100) NULL
);

INSERT INTO viaje (barco, muelle, destino, fecha, kilos, pasajeros, observaciones) VALUES
    ('Gaviota', 1, 'Valle', '2026-10-01', 450, 34, NULL),
    ('Albatros', 2, 'Imperio', '2026-10-01', 1200, 120, 'carga frágil'),
    ('Tortuga', 3, 'Forjas', '2026-10-02', 80, 5, NULL),
    ('Gaviota', 1, 'Valle', '2026-10-03', 520, 41, NULL),
    ('Cóndor', 2, 'Ciudadela', '2026-10-03', 760, 12, 'llegó tarde'),
    ('Albatros', 2, 'Imperio', '2026-10-05', 980, 98, NULL),
    ('Tortuga', 3, 'Forjas', '2026-10-06', 95, 8, NULL);

-- Filtrar y ordenar
SELECT barco, destino, kilos FROM viaje WHERE kilos > 500 ORDER BY kilos DESC;
SELECT barco, DATE_FORMAT(fecha, '%d/%m') AS dia FROM viaje WHERE destino IN ('Valle', 'Forjas') AND fecha BETWEEN '2026-10-02' AND '2026-10-05' ORDER BY fecha;
SELECT barco, observaciones FROM viaje WHERE observaciones IS NOT NULL;

-- Resumir
SELECT COUNT(*) AS viajes, SUM(kilos) AS kilos, ROUND(AVG(pasajeros), 1) AS pasajeros_promedio FROM viaje;

-- Agrupar
SELECT muelle, COUNT(*) AS viajes, SUM(kilos) AS kilos FROM viaje GROUP BY muelle ORDER BY muelle;
SELECT barco, SUM(pasajeros) AS pasajeros FROM viaje GROUP BY barco HAVING SUM(pasajeros) > 50 ORDER BY pasajeros DESC;

-- Modificar y borrar (con WHERE)
UPDATE viaje SET observaciones = 'revisado' WHERE barco = 'Tortuga';
DELETE FROM viaje WHERE kilos < 90;
SELECT id, barco, kilos, observaciones FROM viaje WHERE barco = 'Tortuga';
```

### Salida esperada

```
+----------+-----------+---------+
| barco    | destino   | kilos   |
+----------+-----------+---------+
| Albatros | Imperio   | 1200.00 |
| Albatros | Imperio   |  980.00 |
| Cóndor   | Ciudadela |  760.00 |
| Gaviota  | Valle     |  520.00 |
+----------+-----------+---------+
+---------+-------+
| barco   | dia   |
+---------+-------+
| Tortuga | 02/10 |
| Gaviota | 03/10 |
+---------+-------+
+----------+---------------+
| barco    | observaciones |
+----------+---------------+
| Albatros | carga frágil  |
| Cóndor   | llegó tarde   |
+----------+---------------+
+--------+---------+--------------------+
| viajes | kilos   | pasajeros_promedio |
+--------+---------+--------------------+
|      7 | 4085.00 |               45.4 |
+--------+---------+--------------------+
+--------+--------+---------+
| muelle | viajes | kilos   |
+--------+--------+---------+
|      1 |      2 |  970.00 |
|      2 |      3 | 2940.00 |
|      3 |      2 |  175.00 |
+--------+--------+---------+
+----------+-----------+
| barco    | pasajeros |
+----------+-----------+
| Albatros |       218 |
| Gaviota  |        75 |
+----------+-----------+
+----+---------+-------+---------------+
| id | barco   | kilos | observaciones |
+----+---------+-------+---------------+
|  7 | Tortuga | 95.00 | revisado      |
+----+---------+-------+---------------+
```

### ¿Para qué sirve?

Cada listado, filtro, reporte y total de un sistema es una consulta: "los pedidos pendientes de hoy", "las ventas por mes", "los 10 productos más vendidos", "los clientes que no compran hace 90 días". Saber escribirlas bien (y rápidas) es de lo que más se pide en cualquier trabajo con datos, y en PHP vas a mandarlas a la base con PDO.

### Errores habituales

**Troll: el `UPDATE` o `DELETE` sin `WHERE`.** `DELETE FROM viaje;` borra todo, sin
preguntar. Probá primero el `WHERE` con un `SELECT`.

**Ogro: `= NULL`.** `WHERE observaciones = NULL` no devuelve nada nunca. Es
`IS NULL`.

**Ogro: `AND` y `OR` sin paréntesis.** `WHERE tipo = 'velero' OR tipo = 'pesquero' AND
kilos > 100` se lee `velero OR (pesquero AND kilos > 100)`. Poné paréntesis, o usá
`IN`.

**Slime: el orden de las cláusulas.** `SELECT … ORDER BY … WHERE …` da error de
sintaxis: el `WHERE` va antes del `ORDER BY`.

**Goblin: una columna que no está en el `GROUP BY`.** `SELECT barco, destino,
COUNT(*) … GROUP BY barco` puede dar un destino cualquiera del grupo (o un error en
MySQL con `ONLY_FULL_GROUP_BY`). En el `SELECT` van las columnas agrupadas y los
agregados.

### Misión R04-N02-M1 · Las preguntas de la aduana

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con esta tabla de declaraciones de la aduana, respondé cada pregunta con **una**
consulta (en el orden pedido):

1. Las declaraciones de más de $100000, de mayor a menor valor.
2. Las de origen `Imperio` o `Ciudadela` entre el 3 y el 7 de octubre, ordenadas
   por fecha.
3. Las mercancías que contienen la palabra `vino` (sin importar mayúsculas).
4. Las que todavía no tienen inspector asignado.
5. Las 3 declaraciones de menor peso.

#### Criterio de aprobación

- Usa `WHERE` con `>`, `IN`, `BETWEEN`, `LIKE` e `IS NULL`, `ORDER BY` y `LIMIT`.
- La salida coincide con la esperada.

#### Salida esperada

```
+--------------------+-----------+
| mercancia          | valor     |
+--------------------+-----------+
| Vino torrontés     | 540000.00 |
| Lingotes de hierro | 380000.00 |
| Engranajes         | 215000.00 |
| Relojes            | 176000.00 |
| Vino patero        | 120000.00 |
+--------------------+-----------+
+---------------+-----------+------------+
| mercancia     | origen    | fecha      |
+---------------+-----------+------------+
| Telas de seda | Imperio   | 2026-10-03 |
| Engranajes    | Ciudadela | 2026-10-05 |
| Especias      | Imperio   | 2026-10-07 |
+---------------+-----------+------------+
+-----------------+
| mercancia       |
+-----------------+
| Vino torrontés  |
| Vino patero     |
+-----------------+
+---------------+---------+
| mercancia     | origen  |
+---------------+---------+
| Telas de seda | Imperio |
| Especias      | Imperio |
| Vino patero   | Valle   |
+---------------+---------+
+---------------+---------+
| mercancia     | peso_kg |
+---------------+---------+
| Relojes       |    8.00 |
| Especias      |   12.00 |
| Telas de seda |   35.00 |
+---------------+---------+
```

#### Solución de referencia

```sql
-- Mision 1 - Las preguntas de la aduana: filtrar y ordenar.
DROP TABLE IF EXISTS declaracion;
CREATE TABLE declaracion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mercancia VARCHAR(60) NOT NULL,
    origen VARCHAR(30) NOT NULL,
    fecha DATE NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    peso_kg DECIMAL(8, 2) NOT NULL,
    inspector VARCHAR(40) NULL
);
INSERT INTO declaracion (mercancia, origen, fecha, valor, peso_kg, inspector) VALUES
    ('Vino torrontés', 'Valle', '2026-10-02', 540000, 118, 'Ramos'),
    ('Telas de seda', 'Imperio', '2026-10-03', 98000, 35, NULL),
    ('Engranajes', 'Ciudadela', '2026-10-05', 215000, 410, 'Ramos'),
    ('Lingotes de hierro', 'Forjas', '2026-10-05', 380000, 900, 'Quiroga'),
    ('Especias', 'Imperio', '2026-10-07', 64000, 12, NULL),
    ('Vino patero', 'Valle', '2026-10-08', 120000, 40, NULL),
    ('Relojes', 'Ciudadela', '2026-10-09', 176000, 8, 'Quiroga');

SELECT mercancia, valor FROM declaracion WHERE valor > 100000 ORDER BY valor DESC;
SELECT mercancia, origen, fecha FROM declaracion WHERE origen IN ('Imperio', 'Ciudadela') AND fecha BETWEEN '2026-10-03' AND '2026-10-07' ORDER BY fecha;
SELECT mercancia FROM declaracion WHERE mercancia LIKE '%VINO%';
SELECT mercancia, origen FROM declaracion WHERE inspector IS NULL;
SELECT mercancia, peso_kg FROM declaracion ORDER BY peso_kg LIMIT 3;
```

### Misión R04-N02-M2 · El balance de la fonda

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La fonda registra cada venta (plato, categoría, cantidad, precio unitario, mozo y
fecha). Respondé con consultas:

1. El total vendido, la cantidad de ventas y el ticket promedio (redondeado a 2
   decimales). El total de una venta es `cantidad * precio`.
2. Por **categoría**: cantidad de platos vendidos y total, de mayor a menor total.
3. Por **mozo**: cuántas ventas hizo y cuánto facturó, solo los que facturaron más
   de $20000.
4. El plato más vendido (por cantidad de unidades).
5. Por **día**: la fecha en formato `dd/mm` y el total, en orden de fecha.

#### Criterio de aprobación

- Usa `SUM`, `COUNT`, `AVG`, `ROUND`, `GROUP BY`, `HAVING` y `DATE_FORMAT`.
- La salida coincide con la esperada.

#### Salida esperada

```
+----------+--------+-----------------+
| total    | ventas | ticket_promedio |
+----------+--------+-----------------+
| 84700.00 |      8 |        10587.50 |
+----------+--------+-----------------+
+-----------+--------+----------+
| categoria | platos | total    |
+-----------+--------+----------+
| principal |      6 | 48900.00 |
| entrada   |     18 | 16200.00 |
| bebida    |      5 | 10000.00 |
| postre    |      3 |  9600.00 |
+-----------+--------+----------+
+------+--------+-----------+
| mozo | ventas | facturado |
+------+--------+-----------+
| Nora |      3 |  43800.00 |
| Tito |      3 |  24900.00 |
+------+--------+-----------+
+-----------+----------+
| plato     | unidades |
+-----------+----------+
| Empanadas |       18 |
+-----------+----------+
+-------+----------+
| dia   | total    |
+-------+----------+
| 01/10 | 23200.00 |
| 02/10 | 49800.00 |
| 03/10 | 11700.00 |
+-------+----------+
```

#### Solución de referencia

```sql
-- Mision 2 - El balance de la fonda: agrupar y resumir.
DROP TABLE IF EXISTS venta;
CREATE TABLE venta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plato VARCHAR(40) NOT NULL,
    categoria ENUM('entrada', 'principal', 'postre', 'bebida') NOT NULL,
    cantidad INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    mozo VARCHAR(20) NOT NULL,
    fecha DATE NOT NULL
);
INSERT INTO venta (plato, categoria, cantidad, precio, mozo, fecha) VALUES
    ('Empanadas', 'entrada', 6, 900, 'Tito', '2026-10-01'),
    ('Locro', 'principal', 2, 6500, 'Tito', '2026-10-01'),
    ('Vino de la casa', 'bebida', 1, 4800, 'Nora', '2026-10-01'),
    ('Cabrito', 'principal', 3, 9800, 'Nora', '2026-10-02'),
    ('Quesillo con cayote', 'postre', 3, 3200, 'Nora', '2026-10-02'),
    ('Empanadas', 'entrada', 12, 900, 'Lalo', '2026-10-02'),
    ('Agua', 'bebida', 4, 1300, 'Lalo', '2026-10-03'),
    ('Locro', 'principal', 1, 6500, 'Tito', '2026-10-03');

SELECT SUM(cantidad * precio) AS total, COUNT(*) AS ventas, ROUND(AVG(cantidad * precio), 2) AS ticket_promedio FROM venta;
SELECT categoria, SUM(cantidad) AS platos, SUM(cantidad * precio) AS total FROM venta GROUP BY categoria ORDER BY total DESC;
SELECT mozo, COUNT(*) AS ventas, SUM(cantidad * precio) AS facturado FROM venta GROUP BY mozo HAVING facturado > 20000 ORDER BY facturado DESC;
SELECT plato, SUM(cantidad) AS unidades FROM venta GROUP BY plato ORDER BY unidades DESC LIMIT 1;
SELECT DATE_FORMAT(fecha, '%d/%m') AS dia, SUM(cantidad * precio) AS total FROM venta GROUP BY fecha ORDER BY fecha;
```

### Misión R04-N02-M3 · La limpieza de fin de mes

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

A fin de mes la bodega actualiza precios y limpia registros. Con la tabla de
productos del ejemplo, en este orden:

1. Mostrá los productos que se van a tocar en el paso 2 (con un `SELECT` que use el
   mismo `WHERE`).
2. Aumentá un 8% el precio de los de categoría `almacen`, redondeado a 2 decimales.
3. Poné el stock en 0 a los que vencen antes del `2026-11-01`.
4. Borrá los que tienen stock 0 **y** están marcados como discontinuados.
5. Mostrá cómo quedó la tabla, ordenada por código.

#### Criterio de aprobación

- Cada `UPDATE` y `DELETE` tiene su `WHERE`.
- Antes del primer `UPDATE`, un `SELECT` con el mismo `WHERE`.
- La salida coincide con la esperada.

#### Salida esperada

```
+--------+--------------------+---------+
| codigo | descripcion        | precio  |
+--------+--------------------+---------+
| ALM001 | Yerba mate 1 kg    | 4200.00 |
| ALM002 | Galletitas de agua | 1150.00 |
| ALM003 | Harina 000         |  890.00 |
+--------+--------------------+---------+
+--------+--------------------+---------+-------+
| codigo | descripcion        | precio  | stock |
+--------+--------------------+---------+-------+
| ALM001 | Yerba mate 1 kg    | 4536.00 |    40 |
| ALM002 | Galletitas de agua | 1242.00 |     0 |
| BEB002 | Agua mineral 2 l   | 1300.00 |    48 |
| LIM001 | Lavandina 1 l      |  950.00 |    25 |
+--------+--------------------+---------+-------+
```

#### Solución de referencia

```sql
-- Mision 3 - La limpieza de fin de mes: UPDATE y DELETE siempre con WHERE.
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (
    codigo CHAR(6) PRIMARY KEY,
    descripcion VARCHAR(80) NOT NULL,
    categoria ENUM('almacen', 'limpieza', 'bebidas') NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    vence DATE NULL,
    discontinuado BOOLEAN NOT NULL DEFAULT FALSE
);
INSERT INTO producto VALUES
    ('ALM001', 'Yerba mate 1 kg', 'almacen', 4200, 40, '2027-06-30', FALSE),
    ('ALM002', 'Galletitas de agua', 'almacen', 1150, 15, '2026-10-20', FALSE),
    ('ALM003', 'Harina 000', 'almacen', 890, 0, '2027-01-15', TRUE),
    ('LIM001', 'Lavandina 1 l', 'limpieza', 950, 25, NULL, FALSE),
    ('BEB001', 'Gaseosa lima 2 l', 'bebidas', 2100, 6, '2026-10-28', TRUE),
    ('BEB002', 'Agua mineral 2 l', 'bebidas', 1300, 48, '2027-01-10', FALSE);

SELECT codigo, descripcion, precio FROM producto WHERE categoria = 'almacen';
UPDATE producto SET precio = ROUND(precio * 1.08, 2) WHERE categoria = 'almacen';
UPDATE producto SET stock = 0 WHERE vence < '2026-11-01';
DELETE FROM producto WHERE stock = 0 AND discontinuado = TRUE;
SELECT codigo, descripcion, precio, stock FROM producto ORDER BY codigo;
```

### Encargo R04-N02-E1 · El reporte de la biblioteca popular

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

La biblioteca popular del barrio registra sus préstamos en una tabla (libro,
género, socio, fecha de préstamo y fecha de devolución, que es `NULL` si todavía no
lo devolvió). La comisión directiva pide un reporte con:

1. Cuántos préstamos hubo en total y cuántos siguen sin devolver.
2. Los préstamos sin devolver hechos **antes** del 1 de octubre (atrasados), con el
   socio y la fecha en formato `dd/mm/aaaa`.
3. Préstamos por género, con la cantidad, ordenados de más a menos.
4. Los socios con 2 o más préstamos.
5. Los días que tardó cada devolución (`DATEDIFF(devolucion, prestamo)`), solo de
   los devueltos, y el promedio.

#### Criterio de aprobación

- Usa `IS NULL`, `COUNT` con y sin columna, `GROUP BY`, `HAVING`, `DATE_FORMAT` y `DATEDIFF`.
- La salida coincide con la esperada.

#### Salida esperada

```
+-----------+--------------+
| prestamos | sin_devolver |
+-----------+--------------+
|         7 |            4 |
+-----------+--------------+
+-----------+--------------+------------+
| libro     | socio        | desde      |
+-----------+--------------+------------+
| Ficciones | Beto Díaz    | 10/09/2026 |
| Bestiario | Carla Gómez  | 28/09/2026 |
+-----------+--------------+------------+
+----------+-----------+
| genero   | prestamos |
+----------+-----------+
| novela   |         3 |
| cuentos  |         2 |
| crónica  |         1 |
| poesía   |         1 |
+----------+-----------+
+------------+-----------+
| socio      | prestamos |
+------------+-----------+
| Ana Pérez  |         3 |
| Beto Díaz  |         2 |
+------------+-----------+
+------------------+------+
| libro            | dias |
+------------------+------+
| Poemas de otoño  |    4 |
| El túnel         |    7 |
| Rayuela          |   18 |
+------------------+------+
+---------------+
| promedio_dias |
+---------------+
|           9.7 |
+---------------+
```

#### Solución de referencia

```sql
-- Encargo - El reporte de la biblioteca popular.
DROP TABLE IF EXISTS prestamo;
CREATE TABLE prestamo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    libro VARCHAR(60) NOT NULL,
    genero VARCHAR(20) NOT NULL,
    socio VARCHAR(40) NOT NULL,
    prestamo DATE NOT NULL,
    devolucion DATE NULL
);
INSERT INTO prestamo (libro, genero, socio, prestamo, devolucion) VALUES
    ('Rayuela', 'novela', 'Ana Pérez', '2026-09-02', '2026-09-20'),
    ('Ficciones', 'cuentos', 'Beto Díaz', '2026-09-10', NULL),
    ('El túnel', 'novela', 'Ana Pérez', '2026-09-15', '2026-09-22'),
    ('Bestiario', 'cuentos', 'Carla Gómez', '2026-09-28', NULL),
    ('Poemas de otoño', 'poesía', 'Beto Díaz', '2026-10-01', '2026-10-05'),
    ('La China Iron', 'novela', 'Diego Ruiz', '2026-10-02', NULL),
    ('Operación masacre', 'crónica', 'Ana Pérez', '2026-10-03', NULL);

SELECT COUNT(*) AS prestamos, COUNT(*) - COUNT(devolucion) AS sin_devolver FROM prestamo;
SELECT libro, socio, DATE_FORMAT(prestamo, '%d/%m/%Y') AS desde FROM prestamo WHERE devolucion IS NULL AND prestamo < '2026-10-01' ORDER BY prestamo;
SELECT genero, COUNT(*) AS prestamos FROM prestamo GROUP BY genero ORDER BY prestamos DESC, genero;
SELECT socio, COUNT(*) AS prestamos FROM prestamo GROUP BY socio HAVING COUNT(*) >= 2 ORDER BY prestamos DESC;
SELECT libro, DATEDIFF(devolucion, prestamo) AS dias FROM prestamo WHERE devolucion IS NOT NULL ORDER BY dias;
SELECT ROUND(AVG(DATEDIFF(devolucion, prestamo)), 1) AS promedio_dias FROM prestamo WHERE devolucion IS NOT NULL;
```

### Prueba del sello

#### ¿Qué diferencia hay entre `WHERE` y `HAVING`?

`WHERE` filtra filas antes de agrupar; `HAVING` filtra grupos después del `GROUP BY` (y puede usar agregados como `COUNT(*)`).

#### ¿Cómo se buscan las filas que no tienen dato en una columna?

Con `IS NULL` (con `= NULL` nunca da verdadero).

#### ¿Qué hace `LIKE '%vino%'`?

Busca los textos que contienen "vino" en cualquier lugar (`%` es cualquier cantidad de caracteres).

#### ¿Qué pasa con un `DELETE FROM tabla;` sin `WHERE`?

Borra todas las filas de la tabla.

#### ¿Qué devuelve `COUNT(columna)` y en qué se diferencia de `COUNT(*)`?

`COUNT(columna)` cuenta las filas donde esa columna no es `NULL`; `COUNT(*)` cuenta todas las filas.

### Soluciones (docente)

Nodo nuevo, con MariaDB. En la misión 2, `HAVING facturado > 20000` usa el alias (MariaDB y MySQL lo permiten; el estándar pide repetir la expresión). En el encargo, `COUNT(*) - COUNT(devolucion)` es una forma corta de contar los `NULL`; también sirve `SUM(devolucion IS NULL)`.

## R04-N03 · Relaciones y JOIN

```meta
tipo: tema
padre: R04-N02
precio: 10
criatura: troll
```

### Crónica

En una estantería de la Bodega, cada ficha de viaje repetía todo el barco: nombre, capitán, teléfono del capitán, capacidad. Cuando el capitán de la *Gaviota* cambió de teléfono, hubo que corregir trescientas fichas… y se olvidaron cuarenta. Ahora hay dos estanterías: una de **barcos** y otra de **viajes**, y cada viaje solo anota el **número** de su barco.

—Cada dato se guarda **una sola vez**, en su tabla —dice {mentor}—, y las tablas se **relacionan** por números. Cuando necesitás verlo todo junto, se **une** en la consulta. Pero ojo, {heroe}: si borrás un barco que tiene viajes, esos viajes quedan apuntando a la nada. La bodega te tiene que frenar.

### Objetivos

- Separar los datos en tablas relacionadas para no repetir información.
- Crear claves foráneas (`FOREIGN KEY`) y elegir qué pasa al borrar (`RESTRICT`, `CASCADE`, `SET NULL`).
- Modelar relaciones uno a muchos y muchos a muchos (con una tabla intermedia).
- Unir tablas con `INNER JOIN` y `LEFT JOIN`.
- Agrupar y resumir sobre tablas unidas, y usar subconsultas simples.

### Antes de empezar

- Consultas con `WHERE`, `GROUP BY` y `HAVING` (R04-N02).

### Explicación

#### El problema de repetir
Si cada viaje guarda el nombre, el capitán y el teléfono del barco:
- el mismo dato está en mil lugares (y ocupa mil veces);
- cambiarlo obliga a actualizar mil filas (y si te olvidás una, hay dos verdades);
- un error de tipeo (`Gaviota` / `Gaviotta`) crea un barco "nuevo".

La solución es **normalizar**: cada cosa en su tabla, y las relaciones por el `id`.

#### Uno a muchos
Un barco hace **muchos** viajes; cada viaje es de **un** barco. La tabla del lado
"muchos" guarda el `id` del otro lado:
```sql
CREATE TABLE barco (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL UNIQUE,
    capitan VARCHAR(40) NOT NULL
);

CREATE TABLE viaje (
    id INT AUTO_INCREMENT PRIMARY KEY,
    barco_id INT NOT NULL,
    destino VARCHAR(40) NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (barco_id) REFERENCES barco(id) ON DELETE RESTRICT
);
```
La **clave foránea** (`FOREIGN KEY`) le dice a la base: *`barco_id` tiene que ser
el `id` de un barco que exista*. Si intentás cargar un viaje con `barco_id = 99` y
no hay barco 99, la base lo rechaza.

#### Qué pasa al borrar
| Opción | Si borrás el barco… |
|---|---|
| `ON DELETE RESTRICT` (por defecto) | no te deja mientras tenga viajes (`Cannot delete or update a parent row`) |
| `ON DELETE CASCADE` | se borran también sus viajes |
| `ON DELETE SET NULL` | los viajes quedan con `barco_id = NULL` (la columna tiene que admitir `NULL`) |

`RESTRICT` es lo más seguro: los registros históricos (ventas, viajes, notas) no se
borran en cascada por accidente.

#### Muchos a muchos
Un pasajero hace muchos viajes, y un viaje lleva muchos pasajeros. Se resuelve con
una **tabla intermedia** que guarda los pares:
```sql
CREATE TABLE pasaje (
    viaje_id INT NOT NULL,
    pasajero_id INT NOT NULL,
    asiento VARCHAR(4) NOT NULL,
    PRIMARY KEY (viaje_id, pasajero_id),            -- el mismo pasajero no va dos veces en un viaje
    FOREIGN KEY (viaje_id) REFERENCES viaje(id) ON DELETE CASCADE,
    FOREIGN KEY (pasajero_id) REFERENCES pasajero(id)
);
```

#### Unir tablas: `INNER JOIN`
```sql
SELECT v.fecha, v.destino, b.nombre AS barco, b.capitan
FROM viaje v
INNER JOIN barco b ON b.id = v.barco_id
ORDER BY v.fecha;
```
- `viaje v` le pone un **alias** corto a la tabla.
- `ON` dice cómo se corresponden las filas.
- `INNER JOIN` devuelve solo las filas que **tienen pareja** en las dos tablas.

#### `LEFT JOIN`: incluir los que no tienen pareja
```sql
SELECT b.nombre, COUNT(v.id) AS viajes
FROM barco b
LEFT JOIN viaje v ON v.barco_id = b.id
GROUP BY b.id, b.nombre;
```
`LEFT JOIN` devuelve **todas** las filas de la tabla de la izquierda, y `NULL` en las
columnas de la derecha cuando no hay pareja. Así aparecen los barcos **sin viajes**
(con `COUNT(v.id) = 0`). Con `INNER JOIN` no aparecerían.

Para buscar "los que no tienen": `LEFT JOIN … WHERE v.id IS NULL`.

#### Varias tablas
```sql
SELECT p.nombre, v.destino, b.nombre AS barco
FROM pasaje pj
JOIN pasajero p ON p.id = pj.pasajero_id
JOIN viaje v ON v.id = pj.viaje_id
JOIN barco b ON b.id = v.barco_id;
```
(`JOIN` a secas es `INNER JOIN`.)

#### Subconsultas
Una consulta adentro de otra:
```sql
SELECT nombre FROM barco WHERE id IN (SELECT barco_id FROM viaje WHERE destino = 'Valle');
SELECT nombre, capacidad FROM barco WHERE capacidad > (SELECT AVG(capacidad) FROM barco);
```

### Código de ejemplo

```sql
-- Las dos estanterías: barcos, viajes, pasajeros y pasajes.
DROP TABLE IF EXISTS pasaje;
DROP TABLE IF EXISTS pasajero;
DROP TABLE IF EXISTS viaje;
DROP TABLE IF EXISTS barco;

CREATE TABLE barco (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL UNIQUE,
    capitan VARCHAR(40) NOT NULL
);
CREATE TABLE viaje (
    id INT AUTO_INCREMENT PRIMARY KEY,
    barco_id INT NOT NULL,
    destino VARCHAR(40) NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (barco_id) REFERENCES barco(id) ON DELETE RESTRICT
);
CREATE TABLE pasajero (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL
);
CREATE TABLE pasaje (
    viaje_id INT NOT NULL,
    pasajero_id INT NOT NULL,
    asiento VARCHAR(4) NOT NULL,
    PRIMARY KEY (viaje_id, pasajero_id),
    FOREIGN KEY (viaje_id) REFERENCES viaje(id) ON DELETE CASCADE,
    FOREIGN KEY (pasajero_id) REFERENCES pasajero(id)
);

INSERT INTO barco (nombre, capitan) VALUES ('Gaviota', 'Kira'), ('Albatros', 'Bron'), ('Tortuga', 'Lía'), ('Delfín', 'Olmo');
INSERT INTO viaje (barco_id, destino, fecha) VALUES (1, 'Valle', '2026-10-01'), (2, 'Imperio', '2026-10-01'), (1, 'Valle', '2026-10-03'), (3, 'Forjas', '2026-10-04');
INSERT INTO pasajero (nombre) VALUES ('Ana'), ('Beto'), ('Carla'), ('Diego');
INSERT INTO pasaje (viaje_id, pasajero_id, asiento) VALUES (1, 1, '1A'), (1, 2, '1B'), (2, 3, '3C'), (3, 1, '2A'), (4, 4, '1A');

-- INNER JOIN: cada viaje con su barco
SELECT v.fecha, v.destino, b.nombre AS barco, b.capitan FROM viaje v INNER JOIN barco b ON b.id = v.barco_id ORDER BY v.fecha, b.nombre;

-- LEFT JOIN: todos los barcos, también los que no viajaron
SELECT b.nombre, COUNT(v.id) AS viajes FROM barco b LEFT JOIN viaje v ON v.barco_id = b.id GROUP BY b.id, b.nombre ORDER BY viajes DESC, b.nombre;

-- Tres tablas: quién viajó en qué barco
SELECT p.nombre AS pasajero, v.destino, b.nombre AS barco, pj.asiento FROM pasaje pj JOIN pasajero p ON p.id = pj.pasajero_id JOIN viaje v ON v.id = pj.viaje_id JOIN barco b ON b.id = v.barco_id ORDER BY p.nombre, v.fecha;

-- Subconsulta: los barcos que fueron al Valle
SELECT nombre FROM barco WHERE id IN (SELECT barco_id FROM viaje WHERE destino = 'Valle');
```

### Salida esperada

```
+------------+---------+----------+---------+
| fecha      | destino | barco    | capitan |
+------------+---------+----------+---------+
| 2026-10-01 | Imperio | Albatros | Bron    |
| 2026-10-01 | Valle   | Gaviota  | Kira    |
| 2026-10-03 | Valle   | Gaviota  | Kira    |
| 2026-10-04 | Forjas  | Tortuga  | Lía     |
+------------+---------+----------+---------+
+----------+--------+
| nombre   | viajes |
+----------+--------+
| Gaviota  |      2 |
| Albatros |      1 |
| Tortuga  |      1 |
| Delfín   |      0 |
+----------+--------+
+----------+---------+----------+---------+
| pasajero | destino | barco    | asiento |
+----------+---------+----------+---------+
| Ana      | Valle   | Gaviota  | 1A      |
| Ana      | Valle   | Gaviota  | 2A      |
| Beto     | Valle   | Gaviota  | 1B      |
| Carla    | Imperio | Albatros | 3C      |
| Diego    | Forjas  | Tortuga  | 1A      |
+----------+---------+----------+---------+
+---------+
| nombre  |
+---------+
| Gaviota |
+---------+
```

### ¿Para qué sirve?

Todos los sistemas reales son tablas relacionadas: clientes y pedidos, pedidos y productos, alumnos y materias, usuarios y roles. Diseñar bien las relaciones evita datos duplicados e inconsistentes, y los `JOIN` son la consulta más usada de todas: "los pedidos con el nombre del cliente", "los productos con su categoría". Laravel los arma por vos con sus relaciones (`hasMany`, `belongsTo`), que son exactamente esto.

### Errores habituales

**Troll: el `JOIN` sin `ON`.** `SELECT * FROM viaje JOIN barco` sin condición combina
**cada** viaje con **cada** barco (4 × 4 = 16 filas sin sentido). Siempre `ON`.

**Esqueleto: la columna ambigua.** `SELECT nombre FROM pasaje JOIN pasajero … JOIN
barco …` da `Column 'nombre' in field list is ambiguous`: las dos tablas tienen
`nombre`. Usá el alias: `p.nombre`, `b.nombre`.

**Ogro: `INNER` cuando querías `LEFT`.** Un listado de "todos los clientes con su
cantidad de pedidos" con `INNER JOIN` esconde a los que no compraron nunca.

**Troll: borrar el padre.** `DELETE FROM barco WHERE id = 1` con viajes da `Cannot
delete or update a parent row: a foreign key constraint fails`. Es la base
protegiéndote: decidí si borrar los hijos, reasignarlos o no borrar.

**Esqueleto: el orden al crear y al borrar tablas.** No se puede crear `viaje` antes
que `barco` (la clave foránea apunta a una tabla que no existe), y no se puede
borrar `barco` antes que `viaje`. Se crean de padres a hijos y se borran al revés.

### Misión R04-N03-M1 · Los alumnos de la escuela náutica

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La escuela náutica tiene **cursos** (nombre y cupo) y **alumnos** (nombre y el curso
en el que está anotado, con clave foránea). Escribí el script que cree las dos
tablas (con `ON DELETE RESTRICT`), cargue 3 cursos y 6 alumnos (un curso sin
alumnos), y responda:

1. Cada alumno con el nombre de su curso, ordenado por curso y alumno.
2. Cada curso con la cantidad de alumnos y los lugares libres (cupo menos
   anotados), **incluyendo** el curso sin alumnos.
3. Los cursos sin ningún alumno (con `LEFT JOIN … IS NULL`).

#### Criterio de aprobación

- La tabla de alumnos tiene una clave foránea al curso.
- Usa `INNER JOIN` para la primera y `LEFT JOIN` para las otras dos.
- La salida coincide con la esperada.

#### Salida esperada

```
+--------------------+--------+
| curso              | alumno |
+--------------------+--------+
| Navegación a vela  | Lía    |
| Navegación a vela  | Olmo   |
| Navegación a vela  | Tomi   |
| Timonel            | Ana    |
| Timonel            | Bron   |
| Timonel            | Kira   |
+--------------------+--------+
+--------------------+----------+--------+
| curso              | anotados | libres |
+--------------------+----------+--------+
| Navegación a vela  |        3 |      3 |
| Primeros auxilios  |        0 |     10 |
| Timonel            |        3 |      1 |
+--------------------+----------+--------+
+-------------------+
| sin_alumnos       |
+-------------------+
| Primeros auxilios |
+-------------------+
```

#### Solución de referencia

```sql
-- Mision 1 - Los alumnos de la escuela náutica: uno a muchos y JOIN.
DROP TABLE IF EXISTS alumno;
DROP TABLE IF EXISTS curso;

CREATE TABLE curso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL,
    cupo INT NOT NULL
);
CREATE TABLE alumno (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL,
    curso_id INT NOT NULL,
    FOREIGN KEY (curso_id) REFERENCES curso(id) ON DELETE RESTRICT
);

INSERT INTO curso (nombre, cupo) VALUES ('Timonel', 4), ('Navegación a vela', 6), ('Primeros auxilios', 10);
INSERT INTO alumno (nombre, curso_id) VALUES ('Kira', 1), ('Bron', 1), ('Lía', 2), ('Olmo', 2), ('Tomi', 2), ('Ana', 1);

SELECT c.nombre AS curso, a.nombre AS alumno FROM alumno a INNER JOIN curso c ON c.id = a.curso_id ORDER BY c.nombre, a.nombre;
SELECT c.nombre AS curso, COUNT(a.id) AS anotados, c.cupo - COUNT(a.id) AS libres FROM curso c LEFT JOIN alumno a ON a.curso_id = c.id GROUP BY c.id, c.nombre, c.cupo ORDER BY c.nombre;
SELECT c.nombre AS sin_alumnos FROM curso c LEFT JOIN alumno a ON a.curso_id = c.id WHERE a.id IS NULL;
```

### Misión R04-N03-M2 · Los pedidos del almacén

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Modelá los pedidos de un almacén con cuatro tablas: `cliente`, `producto`,
`pedido` (cliente y fecha) y `detalle` (pedido, producto, cantidad y el **precio al
momento de la venta**; clave primaria compuesta por pedido y producto). Cargá datos
de ejemplo y respondé:

1. Cada pedido con el nombre del cliente y su total (suma de cantidad × precio del
   detalle), ordenado por número de pedido.
2. El total gastado por cada cliente, incluyendo a los que no compraron (con 0:
   `COALESCE(SUM(…), 0)`).
3. Los productos que **nunca** se vendieron.
4. Los clientes que gastaron más que el promedio de gasto por pedido (subconsulta).

#### Criterio de aprobación

- Relación muchos a muchos entre pedidos y productos con una tabla intermedia.
- El detalle guarda el precio de la venta (si mañana cambia el precio, el pedido viejo no cambia).
- La salida coincide con la esperada.

#### Salida esperada

```
+--------+---------+----------+
| pedido | cliente | total    |
+--------+---------+----------+
|      1 | Ana     | 11300.00 |
|      2 | Beto    |  1500.00 |
|      3 | Ana     |  6400.00 |
+--------+---------+----------+
+--------+----------+
| nombre | gastado  |
+--------+----------+
| Ana    | 17700.00 |
| Beto   |  1500.00 |
| Carla  |     0.00 |
+--------+----------+
+---------------+
| nunca_vendido |
+---------------+
| Aceite        |
+---------------+
+--------+----------+
| nombre | gastado  |
+--------+----------+
| Ana    | 17700.00 |
+--------+----------+
```

#### Solución de referencia

```sql
-- Mision 2 - Los pedidos del almacén: muchos a muchos con precio histórico.
DROP TABLE IF EXISTS detalle;
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS producto;
DROP TABLE IF EXISTS cliente;

CREATE TABLE cliente (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(40) NOT NULL);
CREATE TABLE producto (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(40) NOT NULL, precio DECIMAL(10, 2) NOT NULL);
CREATE TABLE pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);
CREATE TABLE detalle (
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (pedido_id, producto_id),
    FOREIGN KEY (pedido_id) REFERENCES pedido(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES producto(id)
);

INSERT INTO cliente (nombre) VALUES ('Ana'), ('Beto'), ('Carla');
INSERT INTO producto (nombre, precio) VALUES ('Yerba', 4200), ('Azúcar', 1500), ('Fideos', 1100), ('Aceite', 3800);
INSERT INTO pedido (cliente_id, fecha) VALUES (1, '2026-10-01'), (2, '2026-10-02'), (1, '2026-10-04');
INSERT INTO detalle (pedido_id, producto_id, cantidad, precio) VALUES (1, 1, 2, 4000), (1, 3, 3, 1100), (2, 2, 1, 1500), (3, 1, 1, 4200), (3, 3, 2, 1100);

SELECT p.id AS pedido, c.nombre AS cliente, SUM(d.cantidad * d.precio) AS total FROM pedido p JOIN cliente c ON c.id = p.cliente_id JOIN detalle d ON d.pedido_id = p.id GROUP BY p.id, c.nombre ORDER BY p.id;
SELECT c.nombre, COALESCE(SUM(d.cantidad * d.precio), 0) AS gastado FROM cliente c LEFT JOIN pedido p ON p.cliente_id = c.id LEFT JOIN detalle d ON d.pedido_id = p.id GROUP BY c.id, c.nombre ORDER BY gastado DESC;
SELECT pr.nombre AS nunca_vendido FROM producto pr LEFT JOIN detalle d ON d.producto_id = pr.id WHERE d.pedido_id IS NULL;
SELECT c.nombre, SUM(d.cantidad * d.precio) AS gastado FROM cliente c JOIN pedido p ON p.cliente_id = c.id JOIN detalle d ON d.pedido_id = p.id GROUP BY c.id, c.nombre
HAVING gastado > (SELECT AVG(t.total) FROM (SELECT SUM(cantidad * precio) AS total FROM detalle GROUP BY pedido_id) t);
```

### Misión R04-N03-M3 · El borrado prohibido

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un club tiene **socios** y sus **pagos** de cuota, y **actividades** con sus
**inscripciones** (socio y actividad). Elegí para cada clave foránea el `ON DELETE`
que corresponde y justificalo en un comentario:

- los **pagos** son historia contable: si alguien intenta borrar un socio con pagos,
  la base tiene que **impedirlo**;
- las **inscripciones** no tienen sentido sin su actividad: si se borra una
  actividad, se borran sus inscripciones;
- cada socio puede tener un **padrino** (otro socio, opcional): si se borra el
  padrino, el ahijado queda sin padrino.

Cargá datos, borrá una actividad (con inscripciones) y un socio que es padrino **y
no tiene pagos**, y mostrá cómo quedaron las inscripciones y los padrinos.

#### Criterio de aprobación

- Usa `RESTRICT`, `CASCADE` y `SET NULL` donde corresponde, con un comentario.
- La salida coincide con la esperada.

#### Salida esperada

```
+-------+-----------+
| socio | actividad |
+-------+-----------+
| Carla | Natación  |
| Diego | Natación  |
+-------+-----------+
+--------+------------+
| nombre | padrino_id |
+--------+------------+
| Beto   |       NULL |
| Carla  |       NULL |
| Diego  |       NULL |
+--------+------------+
```

#### Solución de referencia

```sql
-- Mision 3 - El borrado prohibido: RESTRICT, CASCADE y SET NULL.
DROP TABLE IF EXISTS inscripcion;
DROP TABLE IF EXISTS actividad;
DROP TABLE IF EXISTS pago;
DROP TABLE IF EXISTS socio;

CREATE TABLE socio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL,
    padrino_id INT NULL,
    -- SET NULL: si se borra el padrino, el socio sigue, sin padrino.
    FOREIGN KEY (padrino_id) REFERENCES socio(id) ON DELETE SET NULL
);
CREATE TABLE pago (
    id INT AUTO_INCREMENT PRIMARY KEY,
    socio_id INT NOT NULL,
    mes CHAR(7) NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    -- RESTRICT: los pagos son historia contable; no se borra un socio que pagó.
    FOREIGN KEY (socio_id) REFERENCES socio(id) ON DELETE RESTRICT
);
CREATE TABLE actividad (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(40) NOT NULL);
CREATE TABLE inscripcion (
    socio_id INT NOT NULL,
    actividad_id INT NOT NULL,
    PRIMARY KEY (socio_id, actividad_id),
    FOREIGN KEY (socio_id) REFERENCES socio(id) ON DELETE RESTRICT,
    -- CASCADE: una inscripción no tiene sentido sin su actividad.
    FOREIGN KEY (actividad_id) REFERENCES actividad(id) ON DELETE CASCADE
);

INSERT INTO socio (nombre, padrino_id) VALUES ('Ana', NULL), ('Beto', 1), ('Carla', 1), ('Diego', NULL);
INSERT INTO pago (socio_id, mes, monto) VALUES (2, '2026-09', 12000), (3, '2026-09', 12000);
INSERT INTO actividad (nombre) VALUES ('Fútbol'), ('Natación');
INSERT INTO inscripcion (socio_id, actividad_id) VALUES (2, 1), (3, 1), (3, 2), (4, 2);

DELETE FROM actividad WHERE nombre = 'Fútbol';
DELETE FROM socio WHERE nombre = 'Ana';

SELECT s.nombre AS socio, a.nombre AS actividad FROM inscripcion i JOIN socio s ON s.id = i.socio_id JOIN actividad a ON a.id = i.actividad_id ORDER BY s.nombre;
SELECT nombre, padrino_id FROM socio ORDER BY nombre;
```

### Encargo R04-N03-E1 · El sistema de turnos del consultorio

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Diseñá la base de un consultorio con varios profesionales: `profesional` (nombre y
especialidad), `paciente` (nombre y obra social), `turno` (profesional, paciente
—opcional: un turno puede estar libre—, fecha y hora con `DATETIME`, y estado
`libre`, `reservado`, `atendido` o `ausente`). Un profesional no puede tener dos
turnos a la misma hora (`UNIQUE (profesional_id, fecha_hora)`). Cargá datos y
respondé:

1. La agenda del día 2026-10-06: hora (`%H:%i`), profesional, paciente (o
   `libre` con `COALESCE`) y estado, ordenada por profesional y hora.
2. Por profesional: turnos totales, atendidos y ausentes
   (`SUM(estado = 'ausente')` cuenta los verdaderos).
3. Los pacientes que faltaron alguna vez, con cuántas veces.

#### Criterio de aprobación

- Tres tablas relacionadas, con la regla de un turno por hora por profesional.
- Usa `LEFT JOIN` para mostrar los turnos libres.
- La salida coincide con la esperada.

#### Salida esperada

```
+-------+-------------+------------+-----------+
| hora  | profesional | paciente   | estado    |
+-------+-------------+------------+-----------+
| 10:00 | Dr. Ávila   | Tomi Ruiz  | reservado |
| 10:20 | Dr. Ávila   | libre      | libre     |
| 09:00 | Dra. Molina | Beto Díaz  | reservado |
| 09:20 | Dra. Molina | libre      | libre     |
+-------+-------------+------------+-----------+
+-------------+--------+-----------+----------+
| profesional | turnos | atendidos | ausentes |
+-------------+--------+-----------+----------+
| Dr. Ávila   |      3 |         0 |        1 |
| Dra. Molina |      4 |         1 |        1 |
+-------------+--------+-----------+----------+
+------------+-----------+
| nombre     | ausencias |
+------------+-----------+
| Beto Díaz  |         1 |
| Tomi Ruiz  |         1 |
+------------+-----------+
```

#### Solución de referencia

```sql
-- Encargo - El sistema de turnos del consultorio: relaciones y reportes.
DROP TABLE IF EXISTS turno;
DROP TABLE IF EXISTS paciente;
DROP TABLE IF EXISTS profesional;

CREATE TABLE profesional (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(40) NOT NULL, especialidad VARCHAR(30) NOT NULL);
CREATE TABLE paciente (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(40) NOT NULL, obra_social VARCHAR(20) NOT NULL DEFAULT 'particular');
CREATE TABLE turno (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profesional_id INT NOT NULL,
    paciente_id INT NULL,
    fecha_hora DATETIME NOT NULL,
    estado ENUM('libre', 'reservado', 'atendido', 'ausente') NOT NULL DEFAULT 'libre',
    UNIQUE (profesional_id, fecha_hora),
    FOREIGN KEY (profesional_id) REFERENCES profesional(id),
    FOREIGN KEY (paciente_id) REFERENCES paciente(id) ON DELETE SET NULL
);

INSERT INTO profesional (nombre, especialidad) VALUES ('Dra. Molina', 'clínica'), ('Dr. Ávila', 'pediatría');
INSERT INTO paciente (nombre, obra_social) VALUES ('Ana Pérez', 'APOS'), ('Beto Díaz', 'PAMI'), ('Tomi Ruiz', 'particular');
INSERT INTO turno (profesional_id, paciente_id, fecha_hora, estado) VALUES
    (1, 1, '2026-10-05 09:00', 'atendido'),
    (1, 2, '2026-10-05 09:20', 'ausente'),
    (1, 2, '2026-10-06 09:00', 'reservado'),
    (1, NULL, '2026-10-06 09:20', 'libre'),
    (2, 3, '2026-10-06 10:00', 'reservado'),
    (2, NULL, '2026-10-06 10:20', 'libre'),
    (2, 3, '2026-10-02 10:00', 'ausente');

SELECT DATE_FORMAT(t.fecha_hora, '%H:%i') AS hora, pr.nombre AS profesional, COALESCE(pa.nombre, 'libre') AS paciente, t.estado
FROM turno t JOIN profesional pr ON pr.id = t.profesional_id LEFT JOIN paciente pa ON pa.id = t.paciente_id
WHERE DATE(t.fecha_hora) = '2026-10-06' ORDER BY pr.nombre, t.fecha_hora;
SELECT pr.nombre AS profesional, COUNT(t.id) AS turnos, SUM(t.estado = 'atendido') AS atendidos, SUM(t.estado = 'ausente') AS ausentes
FROM profesional pr LEFT JOIN turno t ON t.profesional_id = pr.id GROUP BY pr.id, pr.nombre ORDER BY pr.nombre;
SELECT pa.nombre, COUNT(*) AS ausencias FROM turno t JOIN paciente pa ON pa.id = t.paciente_id WHERE t.estado = 'ausente' GROUP BY pa.id, pa.nombre ORDER BY ausencias DESC, pa.nombre;
```

### Prueba del sello

#### ¿Por qué no se repiten los datos del barco en cada viaje?

Porque cambiar un dato obligaría a actualizar muchas filas (y si falta una, hay datos contradictorios). Cada cosa se guarda una vez y se relaciona por el `id`.

#### ¿Qué hace una clave foránea?

Obliga a que el valor exista en la otra tabla: no se puede cargar un viaje de un barco que no existe, y controla qué pasa al borrar el barco.

#### ¿Qué diferencia hay entre `INNER JOIN` y `LEFT JOIN`?

`INNER JOIN` devuelve solo las filas con pareja en las dos tablas; `LEFT JOIN` devuelve todas las de la izquierda, con `NULL` donde no hay pareja.

#### ¿Cómo se modela una relación muchos a muchos?

Con una tabla intermedia que guarda los pares de claves (por ejemplo, `pasaje` con `viaje_id` y `pasajero_id`).

#### ¿Qué hace `ON DELETE CASCADE`?

Al borrar la fila padre, borra también las filas hijas que apuntan a ella.

### Soluciones (docente)

Nodo nuevo. En la misión 2, guardar el precio en el detalle es la decisión de diseño clave (los precios cambian, las ventas pasadas no): conviene discutirla. En el encargo, `SUM(estado = 'ausente')` funciona porque en MariaDB/MySQL una comparación vale 1 o 0.

## R04-N04 · PDO: conectarse desde PHP

```meta
tipo: tema
padre: R04-N03
precio: 10
criatura: skeleton
```

### Crónica

Entre la Oficina de Correos y la Bodega hay un montacargas. Hasta ahora nadie lo usaba: los empleados de arriba escribían en archivos y los de abajo en sus fichas, y nunca se hablaban. {mentor} tira de la cuerda y el montacargas empieza a subir y bajar con pedidos y respuestas.

—Tu PHP ya arma páginas; tu base ya guarda datos. Falta que se hablen —dice—. El montacargas se llama **PDO**: le das la dirección de la bodega, el usuario y la clave, y desde ahí le mandás consultas y recibís las filas. Configuralo bien desde el principio, {heroe}: que avise fuerte cuando algo falla.

### Objetivos

- Conectarse a MariaDB/MySQL con PDO y las opciones recomendadas.
- Guardar los datos de conexión en un archivo de configuración.
- Ejecutar consultas con `query` y leer los resultados con `fetch`, `fetchAll` y `fetchColumn`.
- Ejecutar instrucciones que no devuelven filas con `exec`.
- Manejar los errores de la base con `PDOException`.
- Mostrar datos de la base en una página web.

### Antes de empezar

- Consultas y `JOIN` (R04-N02 y R04-N03), excepciones (R02-N09) y configuración en un archivo (R01-N09).

### Explicación

#### Qué es PDO
**PDO** (*PHP Data Objects*) es la forma estándar de hablar con bases de datos desde
PHP. Sirve para MariaDB, MySQL, PostgreSQL, SQLite… con los mismos métodos. Necesita
la extensión `pdo_mysql` (viene en XAMPP; en Linux, `sudo apt install php-mysql`).

#### Conectarse
```php
$pdo = new PDO(
    'mysql:host=localhost;dbname=puerto;charset=utf8mb4',   // el "DSN": motor, servidor, base y juego de caracteres
    'root',                                                   // usuario
    '',                                                       // contraseña
    [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,          // los errores lanzan excepciones
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,     // las filas como arrays asociativos
    ]
);
```
- El DSN empieza con `mysql:` también para MariaDB.
- `charset=utf8mb4` hace que las tildes y las ñ viajen bien.
- **`ERRMODE_EXCEPTION`**: si una consulta falla, PDO lanza una `PDOException` en
  lugar de devolver `false` en silencio. (Desde PHP 8 es el valor por defecto, pero
  se pone igual para que quede claro.)
- **`FETCH_ASSOC`**: cada fila llega como `['nombre' => 'Gaviota', …]`.

#### La configuración, aparte
Los datos de conexión no van en cada archivo: van en uno solo, fuera de `public/`, y
**nunca** se suben a un repositorio público.

`config.php`
```php
<?php
return [
    'dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4',
    'usuario' => 'root',
    'clave' => '',
];
```
`src/db.php`
```php
function conectar(): PDO
{
    static $pdo = null;                   // una sola conexión por pedido
    if ($pdo === null) {
        $c = require __DIR__ . '/../config.php';
        $pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);
    }
    return $pdo;
}
```

#### Leer
```php
$pdo = conectar();

$barcos = $pdo->query('SELECT id, nombre, capacidad FROM barco ORDER BY nombre')->fetchAll();
foreach ($barcos as $b) {
    echo "{$b['nombre']}: {$b['capacidad']} kg\n";
}

$primero = $pdo->query('SELECT * FROM barco ORDER BY id LIMIT 1')->fetch();   // una fila (o false si no hay)
$cantidad = $pdo->query('SELECT COUNT(*) FROM barco')->fetchColumn();          // un solo valor
```
| Método | Devuelve |
|---|---|
| `fetchAll()` | todas las filas, en un array |
| `fetch()` | la siguiente fila, o `false` si no quedan |
| `fetchColumn()` | el primer valor de la siguiente fila |

Con muchas filas, se recorre sin cargar todo en memoria:
```php
$consulta = $pdo->query('SELECT nombre FROM barco');
while ($fila = $consulta->fetch()) { … }
```

#### Los tipos que llegan
Con MariaDB y PHP 8.1 o más, los `INT` llegan como `int`, pero los **`DECIMAL`
llegan como texto** (`"450.00"`) para no perder precisión, y las fechas como
texto (`"2026-10-03"`). Convertilos cuando haga falta: `(float) $b['capacidad']`,
`new DateTimeImmutable($b['botado'])`.

#### Escribir con `exec`
Para instrucciones que no devuelven filas **y no llevan datos de afuera**:
```php
$pdo->exec('CREATE TABLE IF NOT EXISTS log (id INT AUTO_INCREMENT PRIMARY KEY, texto VARCHAR(100))');
$filas = $pdo->exec("UPDATE barco SET activo = FALSE WHERE capacidad < 100");   // devuelve cuántas filas cambió
```
**Atención**: en cuanto un dato viene de un formulario o de la dirección, **no** se
mete en el texto de la consulta. Eso es lo que resuelve el próximo nodo (consultas
preparadas), y es la regla más importante de toda la rama.

#### Errores
```php
try {
    $pdo = conectar();
    $pdo->query('SELECT * FROM barcos');     // la tabla se llama barco
} catch (PDOException $e) {
    error_log($e->getMessage());             // se registra el detalle…
    echo "No pudimos consultar la bodega.";  // …y al usuario se le muestra algo amable
}
```
Mensajes típicos:
```
SQLSTATE[HY000] [1045] Access denied for user 'root'@'localhost' (using password: YES)
SQLSTATE[HY000] [1049] Unknown database 'puerto'
SQLSTATE[42S02]: Base table or view not found: 1146 Table 'puerto.barcos' doesn't exist
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry 'Gaviota' for key 'nombre'
```
`$e->errorInfo[1]` trae el número de error de MariaDB (`1062`, `1451`…), útil para
reaccionar distinto a cada uno.

### Código de ejemplo

`esquema.sql`
```sql
DROP TABLE IF EXISTS viaje;
DROP TABLE IF EXISTS barco;
CREATE TABLE barco (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL UNIQUE,
    capacidad DECIMAL(8, 2) NOT NULL,
    botado DATE NULL
);
CREATE TABLE viaje (
    id INT AUTO_INCREMENT PRIMARY KEY,
    barco_id INT NOT NULL,
    destino VARCHAR(40) NOT NULL,
    kilos DECIMAL(8, 2) NOT NULL,
    FOREIGN KEY (barco_id) REFERENCES barco(id)
);
INSERT INTO barco (nombre, capacidad, botado) VALUES ('Gaviota', 450, '2019-04-12'), ('Albatros', 1200.5, '2026-08-20'), ('Tortuga', 80, NULL);
INSERT INTO viaje (barco_id, destino, kilos) VALUES (1, 'Valle', 420), (2, 'Imperio', 1100), (1, 'Valle', 380), (2, 'Ciudadela', 950);
```

`config.php`
```php
<?php
return [
    'dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4',
    'usuario' => 'root',
    'clave' => '',
];
```

`db.php`
```php
<?php
declare(strict_types=1);

function conectar(): PDO
{
    static $pdo = null;
    if ($pdo === null) {
        $c = require __DIR__ . '/config.php';
        $pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);
    }
    return $pdo;
}
```

`main.php`
```php
<?php
declare(strict_types=1);
/*
 * El montacargas: PHP le pregunta a la Bodega con PDO.
 * Antes, cargá el esquema: mariadb -u root -p puerto < esquema.sql
 */
require __DIR__ . '/db.php';

try {
    $pdo = conectar();

    echo "Barcos:\n";
    foreach ($pdo->query('SELECT nombre, capacidad, botado FROM barco ORDER BY nombre') as $b) {
        $botado = $b['botado'] === null ? 'sin fecha' : (new DateTimeImmutable($b['botado']))->format('d/m/Y');
        printf("  %-9s %8.2f kg  botado: %s\n", $b['nombre'], (float) $b['capacidad'], $botado);
    }

    $cantidad = $pdo->query('SELECT COUNT(*) FROM viaje')->fetchColumn();
    echo "Viajes registrados: $cantidad\n";

    $resumen = $pdo->query(
        'SELECT b.nombre, COUNT(v.id) AS viajes, COALESCE(SUM(v.kilos), 0) AS kilos
         FROM barco b LEFT JOIN viaje v ON v.barco_id = b.id
         GROUP BY b.id, b.nombre ORDER BY kilos DESC'
    )->fetchAll();
    echo "Por barco:\n";
    foreach ($resumen as $r) {
        echo "  {$r['nombre']}: {$r['viajes']} viaje/s, {$r['kilos']} kg\n";
    }

    $mayor = $pdo->query('SELECT nombre FROM barco ORDER BY capacidad DESC LIMIT 1')->fetch();
    echo "El más grande: {$mayor['nombre']}\n";
    var_dump($resumen[0]['viajes'], $resumen[0]['kilos']);

    $cambiadas = $pdo->exec("UPDATE barco SET botado = '2000-01-01' WHERE botado IS NULL");
    echo "Filas actualizadas: $cambiadas\n";

    $pdo->query('SELECT * FROM barcos');
} catch (PDOException $e) {
    echo "Error de la base: ", $e->getMessage(), "\n";
}
```

### Salida esperada

```
Barcos:
  Albatros   1200.50 kg  botado: 20/08/2026
  Gaviota     450.00 kg  botado: 12/04/2019
  Tortuga      80.00 kg  botado: sin fecha
Viajes registrados: 4
Por barco:
  Albatros: 2 viaje/s, 2050.00 kg
  Gaviota: 2 viaje/s, 800.00 kg
  Tortuga: 0 viaje/s, 0.00 kg
El más grande: Albatros
int(2)
string(7) "2050.00"
Filas actualizadas: 1
Error de la base: SQLSTATE[42S02]: Base table or view not found: 1146 Table 'puerto.barcos' doesn't exist
```

### ¿Para qué sirve?

PDO es la puerta entre PHP y la base: la usan WordPress (con su propia capa), Laravel (Eloquent y el Query Builder están hechos sobre PDO) y cualquier sistema PHP. Configurarlo bien (excepciones, `utf8mb4`, una sola conexión, datos de acceso en un archivo aparte) es lo primero que se hace en todo proyecto con base de datos.

### Errores habituales

**Goblin: `could not find driver`.** Falta la extensión `pdo_mysql`. En XAMPP viene;
en Linux, `sudo apt install php-mysql` (y reiniciar el servidor web).

**Esqueleto: `Unknown database 'puerto'`.** La base no existe: creala con `CREATE
DATABASE` (o revisá el nombre en el DSN).

**Troll: sin `ERRMODE_EXCEPTION`.** Con los modos viejos, una consulta mal escrita
devuelve `false` y el programa sigue: el error aparece más adelante como `Call to a
member function fetchAll() on bool`.

**Ogro: las tildes rotas.** Sin `charset=utf8mb4` en el DSN, "Ñandú" puede llegar como
"Ã‘andÃº". Base, tablas y conexión en `utf8mb4`.

**Troll: la clave en el repositorio.** Si subís `config.php` con la contraseña real a
GitHub, cualquiera la ve. Se sube un `config.ejemplo.php` sin datos reales.

### Misión R04-N04-M1 · El listado de la bodega

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Con la tabla de productos (`esquema.sql` incluido en la entrega), escribí
`main.php` que se conecte con una función `conectar()` (datos en `config.php`) y
muestre en la terminal:

1. todos los productos ordenados por categoría y descripción, con el precio con
   `number_format` a la argentina;
2. la cantidad de productos y el valor total del stock (`SUM(precio * stock)`,
   con `fetchColumn`);
3. el producto más caro (con `fetch`);
4. por categoría, la cantidad y el stock total.

Todo dentro de un `try` que atrapa `PDOException` y muestra un mensaje amable.

#### Criterio de aprobación

- Conecta con PDO, `ERRMODE_EXCEPTION`, `FETCH_ASSOC` y `utf8mb4`, con los datos en `config.php`.
- Usa `fetchAll`/`foreach`, `fetch` y `fetchColumn`.
- La salida coincide con la esperada.

#### Salida esperada

```
ALM002 [almacen] Fideos tirabuzón 500 g: $1.100,00
ALM001 [almacen] Yerba mate 1 kg: $4.200,00
LIM001 [limpieza] Lavandina 1 l: $950,00
BEB001 [bebidas] Agua mineral 2 l: $1.300,00
BEB002 [bebidas] Vino torrontés 750 ml: $6.800,00
Productos: 5 · valor del stock: $401.750,00
El más caro: Vino torrontés 750 ml ($6.800,00)
  almacen: 2 producto/s, 100 unidades
  limpieza: 1 producto/s, 25 unidades
  bebidas: 2 producto/s, 60 unidades
```

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (
    codigo CHAR(6) PRIMARY KEY,
    descripcion VARCHAR(80) NOT NULL,
    categoria ENUM('almacen', 'limpieza', 'bebidas') NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0
);
INSERT INTO producto VALUES
    ('ALM001', 'Yerba mate 1 kg', 'almacen', 4200, 40),
    ('ALM002', 'Fideos tirabuzón 500 g', 'almacen', 1100, 60),
    ('LIM001', 'Lavandina 1 l', 'limpieza', 950, 25),
    ('BEB001', 'Agua mineral 2 l', 'bebidas', 1300, 48),
    ('BEB002', 'Vino torrontés 750 ml', 'bebidas', 6800, 12);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`main.php`
```php
<?php
declare(strict_types=1);
// Mision 1 - El listado de la bodega: consultas con PDO.

function conectar(): PDO
{
    static $pdo = null;
    if ($pdo === null) {
        $c = require __DIR__ . '/config.php';
        $pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);
    }
    return $pdo;
}

function pesos(float $n): string
{
    return '$' . number_format($n, 2, ',', '.');
}

try {
    $pdo = conectar();
    foreach ($pdo->query('SELECT codigo, descripcion, categoria, precio FROM producto ORDER BY categoria, descripcion') as $p) {
        echo "{$p['codigo']} [{$p['categoria']}] {$p['descripcion']}: ", pesos((float) $p['precio']), "\n";
    }
    $cantidad = $pdo->query('SELECT COUNT(*) FROM producto')->fetchColumn();
    $valor = $pdo->query('SELECT SUM(precio * stock) FROM producto')->fetchColumn();
    echo "Productos: $cantidad · valor del stock: ", pesos((float) $valor), "\n";
    $caro = $pdo->query('SELECT descripcion, precio FROM producto ORDER BY precio DESC LIMIT 1')->fetch();
    echo "El más caro: {$caro['descripcion']} (", pesos((float) $caro['precio']), ")\n";
    foreach ($pdo->query('SELECT categoria, COUNT(*) AS productos, SUM(stock) AS stock FROM producto GROUP BY categoria ORDER BY categoria') as $c) {
        echo "  {$c['categoria']}: {$c['productos']} producto/s, {$c['stock']} unidades\n";
    }
} catch (PDOException $e) {
    echo "No pudimos consultar la bodega. (", $e->getMessage(), ")\n";
}
```

### Misión R04-N04-M2 · La cartelera desde la base

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Rehacé la **cartelera del ferry** (R03-N01-M1), pero con los datos en MariaDB: una
tabla `salida` (hora `TIME`, destino, lugares libres). Armá un proyecto web chico:

- `esquema.sql` con la tabla y 5 salidas;
- `config.php` y `src/db.php` con `conectar()`;
- `public/index.php` que muestra la tabla de salidas ordenadas por hora (`TIME_FORMAT(hora, '%H:%i')`),
  `COMPLETO` si no hay lugares, y el total de lugares libres (consultado con
  `SUM`, no sumado en PHP).

Si la base no responde, la página muestra `La cartelera no está disponible.` con
código **503**.

#### Criterio de aprobación

- Los datos salen de MariaDB con PDO; la configuración está fuera de `public/`.
- El total se calcula en SQL.
- Un error de conexión muestra un mensaje amable con 503.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS salida;
CREATE TABLE salida (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hora TIME NOT NULL,
    destino VARCHAR(40) NOT NULL,
    libres INT NOT NULL
);
INSERT INTO salida (hora, destino, libres) VALUES
    ('07:00', 'Valle de la Serpiente', 12), ('09:30', 'Forjas de Hierro', 0), ('13:15', 'Imperio de las Clases', 4),
    ('16:00', 'Ciudadela de los Artífices', 9), ('18:40', 'Valle de la Serpiente', 0);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`src/db.php`
```php
<?php
declare(strict_types=1);

function conectar(): PDO
{
    static $pdo = null;
    if ($pdo === null) {
        $c = require __DIR__ . '/../config.php';
        $pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);
    }
    return $pdo;
}
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Mision 2 - La cartelera desde la base: una página que lee de MariaDB.
require __DIR__ . '/../src/db.php';

try {
    $pdo = conectar();
    $salidas = $pdo->query("SELECT TIME_FORMAT(hora, '%H:%i') AS hora, destino, libres FROM salida ORDER BY hora")->fetchAll();
    $libres = (int) $pdo->query('SELECT SUM(libres) FROM salida')->fetchColumn();
} catch (PDOException $e) {
    http_response_code(503);
    exit('La cartelera no está disponible.');
}
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Ferry</title></head>
<body>
    <h1>Salidas del ferry</h1>
    <table>
        <?php foreach ($salidas as $s): ?>
            <tr><td><?= $s['hora'] ?></td><td><?= htmlspecialchars($s['destino']) ?></td>
                <td><?= $s['libres'] === 0 ? 'COMPLETO' : $s['libres'] ?></td></tr>
        <?php endforeach; ?>
    </table>
    <p>Lugares libres en total: <?= $libres ?></p>
</body>
</html>
```

### Misión R04-N04-M3 · El instalador de la base

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Escribí `instalar.php`, un script de terminal que prepara la base de un sistema
nuevo: con `exec`, crea (si no existen) las tablas `categoria` y `articulo` (con
clave foránea), carga las categorías **solo si la tabla está vacía** (consultá con
`fetchColumn`) y muestra un resumen. Tiene que poder ejecutarse muchas veces sin
duplicar datos ni fallar. Si la conexión falla, muestra el motivo y termina con
`exit(1)`. Al final lista las tablas de la base (`SHOW TABLES`) y cuántas
categorías hay.

#### Criterio de aprobación

- Usa `CREATE TABLE IF NOT EXISTS` y carga los datos solo si hace falta.
- Ejecutarlo dos veces da el mismo resultado.
- Maneja el error de conexión con `exit(1)`.

#### Salida esperada

```
Tablas listas.
Vuelta 1: se cargaron 3 categorías.
Vuelta 2: las categorías ya estaban.
Tablas: articulo, categoria
Categorías: 3
```

#### Solución de referencia

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`instalar.php`
```php
<?php
declare(strict_types=1);
// Mision 3 - El instalador de la base: exec, IF NOT EXISTS y datos iniciales una sola vez.
$c = require __DIR__ . '/config.php';
try {
    $pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
} catch (PDOException $e) {
    echo "No me pude conectar: ", $e->getMessage(), "\n";
    exit(1);
}

$pdo->exec('CREATE TABLE IF NOT EXISTS categoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL UNIQUE
)');
$pdo->exec('CREATE TABLE IF NOT EXISTS articulo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    categoria_id INT NOT NULL,
    nombre VARCHAR(60) NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categoria(id)
)');
echo "Tablas listas.\n";

for ($vez = 1; $vez <= 2; $vez++) {
    if ((int) $pdo->query('SELECT COUNT(*) FROM categoria')->fetchColumn() === 0) {
        $cargadas = $pdo->exec("INSERT INTO categoria (nombre) VALUES ('herramientas'), ('pinturas'), ('electricidad')");
        echo "Vuelta $vez: se cargaron $cargadas categorías.\n";
    } else {
        echo "Vuelta $vez: las categorías ya estaban.\n";
    }
}

$tablas = $pdo->query('SHOW TABLES')->fetchAll(PDO::FETCH_COLUMN);
sort($tablas);
echo "Tablas: ", implode(', ', array_intersect($tablas, ['articulo', 'categoria'])), "\n";
echo "Categorías: ", $pdo->query('SELECT COUNT(*) FROM categoria')->fetchColumn(), "\n";
```

### Encargo R04-N04-E1 · El tablero del gerente

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

El gerente de un supermercado quiere un **tablero** web con los números del día,
tomados de la base. Con las tablas `venta` (fecha, sucursal, total, medio de pago)
del `esquema.sql`, armá `public/index.php` que muestre:

- las ventas del día `2026-10-03` (cantidad y total), en tarjetas;
- el total por sucursal (de mayor a menor) en una tabla;
- el porcentaje de ventas por medio de pago (con `ROUND(… * 100 / (SELECT COUNT(*) …), 1)`);
- la mejor venta del día con su sucursal.

Cada número sale de **una consulta SQL** (nada de sumar en PHP). Usá `conectar()`
en `src/db.php` y la configuración fuera de `public/`.

#### Criterio de aprobación

- Todos los cálculos se hacen en SQL.
- La configuración y la conexión están fuera de `public/`.
- Los importes se muestran con `number_format` a la argentina.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS venta;
CREATE TABLE venta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    sucursal VARCHAR(30) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    medio ENUM('efectivo', 'débito', 'crédito', 'transferencia') NOT NULL
);
INSERT INTO venta (fecha, sucursal, total, medio) VALUES
    ('2026-10-03', 'Centro', 18500, 'débito'), ('2026-10-03', 'Centro', 42300, 'crédito'),
    ('2026-10-03', 'Costanera', 9800, 'efectivo'), ('2026-10-03', 'Costanera', 25600, 'transferencia'),
    ('2026-10-03', 'Faldeo', 61200, 'crédito'), ('2026-10-02', 'Centro', 30000, 'efectivo');
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`src/db.php`
```php
<?php
declare(strict_types=1);

function conectar(): PDO
{
    static $pdo = null;
    if ($pdo === null) {
        $c = require __DIR__ . '/../config.php';
        $pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);
    }
    return $pdo;
}

function pesos(float|string $n): string
{
    return '$' . number_format((float) $n, 2, ',', '.');
}
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Encargo - El tablero del gerente: cada número sale de una consulta.
require __DIR__ . '/../src/db.php';
$pdo = conectar();
$dia = "'2026-10-03'";

$hoy = $pdo->query("SELECT COUNT(*) AS ventas, SUM(total) AS total FROM venta WHERE fecha = $dia")->fetch();
$porSucursal = $pdo->query("SELECT sucursal, SUM(total) AS total FROM venta WHERE fecha = $dia GROUP BY sucursal ORDER BY total DESC")->fetchAll();
$porMedio = $pdo->query("SELECT medio, ROUND(COUNT(*) * 100 / (SELECT COUNT(*) FROM venta WHERE fecha = $dia), 1) AS porcentaje FROM venta WHERE fecha = $dia GROUP BY medio ORDER BY porcentaje DESC, medio")->fetchAll();
$mejor = $pdo->query("SELECT sucursal, total FROM venta WHERE fecha = $dia ORDER BY total DESC LIMIT 1")->fetch();
?>
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Tablero</title></head>
<body>
    <h1>Tablero del 03/10/2026</h1>
    <div class="tarjeta">Ventas: <?= $hoy['ventas'] ?></div>
    <div class="tarjeta">Facturado: <?= pesos($hoy['total']) ?></div>
    <h2>Por sucursal</h2>
    <table>
        <?php foreach ($porSucursal as $s): ?><tr><td><?= htmlspecialchars($s['sucursal']) ?></td><td><?= pesos($s['total']) ?></td></tr><?php endforeach; ?>
    </table>
    <h2>Medios de pago</h2>
    <ul>
        <?php foreach ($porMedio as $m): ?><li><?= htmlspecialchars($m['medio']) ?>: <?= $m['porcentaje'] ?>%</li><?php endforeach; ?>
    </ul>
    <p>Mejor venta: <?= pesos($mejor['total']) ?> en <?= htmlspecialchars($mejor['sucursal']) ?></p>
</body>
</html>
```

### Prueba del sello

#### ¿Qué hace la opción `PDO::ERRMODE_EXCEPTION`?

Hace que cualquier error de la base lance una `PDOException`, en lugar de devolver `false` en silencio.

#### ¿Qué diferencia hay entre `fetch`, `fetchAll` y `fetchColumn`?

`fetch` trae una fila, `fetchAll` todas en un array y `fetchColumn` un solo valor (la primera columna de la fila).

#### ¿Por qué `charset=utf8mb4` en el DSN?

Para que las tildes, las ñ y los emojis viajen bien entre PHP y la base.

#### ¿De qué tipo llegan los `DECIMAL` de MariaDB a PHP?

Como texto (`"450.00"`), para no perder precisión: se convierten con `(float)` si hace falta calcular.

#### ¿Cuándo no se puede usar `query`/`exec` con el texto de la consulta armado a mano?

Cuando la consulta lleva datos que vienen de afuera (un formulario, la dirección): para eso están las consultas preparadas.

### Soluciones (docente)

Sale de `21-PHP/17-PDO-SQLite`, llevado a MariaDB. Todos los proyectos incluyen su `esquema.sql`, que se carga antes con `mariadb -u root -p puerto < esquema.sql` (o desde phpMyAdmin). En el encargo, `$dia` es un valor fijo del programa (no viene del usuario), por eso se puede meter en el texto; en el nodo siguiente se ve por qué con datos de afuera no.

## R04-N05 · Consultas preparadas e inyección SQL

```meta
tipo: tema
padre: R04-N04
precio: 10
criatura: troll
```

### Crónica

Un día llegó al montacargas un pedido extraño. Donde tenía que decir el nombre de un barco, decía: `Gaviota' OR '1'='1`. El bodeguero, que copiaba los pedidos tal cual en su libreta de consultas, leyó: *"traeme los barcos que se llamen Gaviota… o cualquiera"*. Y subió toda la bodega.

—Eso se llama **inyección SQL** —dice {mentor}, pálida—, y es una de las formas más viejas y más usadas de robar datos. Pasa cuando un dato de afuera se **pega** en el texto de la consulta: el dato se convierte en código. La cura es separar las dos cosas para siempre, {heroe}: la consulta va por un lado, con huecos; los datos, por otro.

### Objetivos

- Entender cómo funciona un ataque de inyección SQL.
- Usar consultas preparadas con `prepare` y `execute`, con parámetros `?` y con nombre.
- Pasar enteros a `LIMIT`/`OFFSET` y configurar `ATTR_EMULATE_PREPARES`.
- Insertar, actualizar y borrar con parámetros, y leer `lastInsertId` y `rowCount`.
- Buscar con `LIKE` y listas `IN` usando parámetros.
- Reaccionar a los errores de la base (duplicados, claves foráneas).

### Antes de empezar

- PDO: conectarse, `query` y `fetch` (R04-N04).

### Explicación

#### El ataque
Un buscador de barcos, escrito **mal**:
```php
$nombre = $_GET['nombre'];
$sql = "SELECT * FROM barco WHERE nombre = '$nombre'";   // ¡NUNCA!
$barcos = $pdo->query($sql)->fetchAll();
```
Si alguien escribe `Gaviota`, la consulta es la esperada. Pero si escribe
`x' OR '1'='1`, la consulta queda:
```sql
SELECT * FROM barco WHERE nombre = 'x' OR '1'='1'
```
y como `'1'='1'` siempre es verdadero, devuelve **todos** los barcos. Con otras
variantes se pueden leer otras tablas (usuarios, contraseñas), saltear un login o
borrar datos. Todo porque el dato se **pegó** en el código SQL.

#### La cura: consultas preparadas
Se manda la consulta con **huecos** (`?` o `:nombre`), y los datos **aparte**:
```php
$consulta = $pdo->prepare('SELECT * FROM barco WHERE nombre = ?');
$consulta->execute([$nombre]);
$barcos = $consulta->fetchAll();
```
La base recibe primero la estructura y después los valores, y los trata **siempre
como datos**: `x' OR '1'='1` se busca como un nombre (raro) y no aparece nada.

Con nombres, más claro cuando hay muchos:
```php
$consulta = $pdo->prepare('SELECT * FROM viaje WHERE destino = :destino AND kilos >= :minimo');
$consulta->execute(['destino' => $destino, 'minimo' => $minimo]);
```

**Regla del Puerto: todo dato que viene de afuera (formularios, dirección,
archivos, cookies, otras APIs) va como parámetro. Siempre. Sin excepciones.**

#### Lo que no puede ser parámetro
Los parámetros son para **valores**, no para nombres de tablas, columnas ni
palabras clave (`ASC`/`DESC`). Si el usuario elige por qué columna ordenar, se
valida contra una **lista blanca**:
```php
$columnas = ['nombre' => 'nombre', 'capacidad' => 'capacidad'];
$orden = $columnas[$_GET['orden'] ?? ''] ?? 'nombre';          // solo valores de la lista
$sentido = ($_GET['sentido'] ?? '') === 'desc' ? 'DESC' : 'ASC';
$sql = "SELECT * FROM barco ORDER BY $orden $sentido";         // seguro: no vino tal cual del usuario
```

#### `LIMIT` y la emulación
Por defecto, PDO con MySQL/MariaDB **emula** las consultas preparadas: arma el texto
él mismo, poniendo cada valor entre comillas. Con `LIMIT ?` eso da
`LIMIT '5'` y un error de sintaxis. Dos soluciones:
```php
// 1. Pasar el tipo:
$c = $pdo->prepare('SELECT * FROM barco ORDER BY id LIMIT :cantidad OFFSET :desde');
$c->bindValue('cantidad', 5, PDO::PARAM_INT);
$c->bindValue('desde', 10, PDO::PARAM_INT);
$c->execute();

// 2. Desactivar la emulación al conectar (preparadas "de verdad"):
$pdo = new PDO($dsn, $usuario, $clave, [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);
```
Desde acá, los `conectar()` del curso desactivan la emulación.

#### Insertar, actualizar y borrar
```php
$alta = $pdo->prepare('INSERT INTO barco (nombre, capacidad) VALUES (:nombre, :capacidad)');
$alta->execute(['nombre' => 'Delfín', 'capacidad' => 300]);
$id = (int) $pdo->lastInsertId();          // el id que generó AUTO_INCREMENT

$cambio = $pdo->prepare('UPDATE barco SET capacidad = ? WHERE id = ?');
$cambio->execute([350, $id]);
echo $cambio->rowCount();                  // cuántas filas cambió (0 si el valor era el mismo o no existía)

$baja = $pdo->prepare('DELETE FROM barco WHERE id = ?');
$baja->execute([$id]);
```
Una consulta preparada se puede ejecutar **muchas veces** con distintos valores
(más rápido para cargar muchas filas).

#### `LIKE` e `IN` con parámetros
```php
// El % va en el VALOR, no en la consulta:
$c = $pdo->prepare('SELECT nombre FROM barco WHERE nombre LIKE ?');
$c->execute(['%' . $texto . '%']);

// IN con una lista de largo variable: un ? por elemento
$ids = [3, 7, 9];
$huecos = implode(', ', array_fill(0, count($ids), '?'));   // "?, ?, ?"
$c = $pdo->prepare("SELECT * FROM barco WHERE id IN ($huecos)");
$c->execute($ids);
```

#### Cuando la base dice que no
Las restricciones de la base (UNIQUE, claves foráneas) siguen protegiendo. Se
atrapa la excepción y se mira el código de MariaDB:
```php
try {
    $alta->execute(['nombre' => 'Gaviota', 'capacidad' => 100]);
} catch (PDOException $e) {
    if (($e->errorInfo[1] ?? null) === 1062) {        // entrada duplicada
        $error = 'Ya existe un barco con ese nombre.';
    } else {
        throw $e;                                     // otro problema: que siga subiendo
    }
}
```
| Código | Significa |
|---|---|
| `1062` | valor duplicado en una columna `UNIQUE` o clave primaria |
| `1451` | no se puede borrar: hay filas que lo usan (clave foránea) |
| `1452` | no se puede cargar: la clave foránea apunta a algo que no existe |
| `4025` | no se cumple un `CHECK` |

### Código de ejemplo

`esquema.sql`
```sql
DROP TABLE IF EXISTS barco;
CREATE TABLE barco (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL UNIQUE,
    capacidad DECIMAL(8, 2) NOT NULL,
    tipo ENUM('velero', 'pesquero', 'carguero') NOT NULL
);
INSERT INTO barco (nombre, capacidad, tipo) VALUES
    ('Gaviota', 450, 'velero'), ('Albatros', 1200, 'carguero'), ('Tortuga', 80, 'pesquero'),
    ('Garza', 300, 'velero'), ('Cóndor', 760, 'carguero');
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`main.php`
```php
<?php
declare(strict_types=1);
/*
 * El montacargas seguro: la inyección SQL y cómo se evita con consultas preparadas.
 */
$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

$ataque = "x' OR '1'='1";

// MAL: el dato pegado en la consulta
$filas = $pdo->query("SELECT nombre FROM barco WHERE nombre = '$ataque'")->fetchAll();
echo "Pegando el dato: ", count($filas), " barco/s (¡todos!)\n";

// BIEN: consulta preparada
$buscar = $pdo->prepare('SELECT nombre FROM barco WHERE nombre = ?');
$buscar->execute([$ataque]);
echo "Con parámetro: ", count($buscar->fetchAll()), " barco/s\n";
$buscar->execute(['Gaviota']);
echo "Buscando Gaviota: ", $buscar->fetchColumn(), "\n";

// Parámetros con nombre, LIKE e IN
$filtro = $pdo->prepare('SELECT nombre, capacidad FROM barco WHERE nombre LIKE :texto AND capacidad >= :minimo ORDER BY nombre');
$filtro->execute(['texto' => '%a%', 'minimo' => 300]);
foreach ($filtro as $b) {
    echo "  {$b['nombre']} ({$b['capacidad']} kg)\n";
}
$ids = [1, 3, 5];
$huecos = implode(', ', array_fill(0, count($ids), '?'));
$lista = $pdo->prepare("SELECT nombre FROM barco WHERE id IN ($huecos) ORDER BY id");
$lista->execute($ids);
echo "Por id: ", implode(', ', $lista->fetchAll(PDO::FETCH_COLUMN)), "\n";

// Orden elegido por el usuario: lista blanca
$pedido = 'capacidad; DROP TABLE barco';
$columna = ['nombre' => 'nombre', 'capacidad' => 'capacidad'][$pedido] ?? 'nombre';
echo "Ordenado por: $columna\n";

// LIMIT con parámetros (sin emulación, funciona con execute)
$pagina = $pdo->prepare('SELECT nombre FROM barco ORDER BY id LIMIT ? OFFSET ?');
$pagina->execute([2, 2]);
echo "Página 2: ", implode(', ', $pagina->fetchAll(PDO::FETCH_COLUMN)), "\n";

// Insertar, actualizar, borrar
$alta = $pdo->prepare('INSERT INTO barco (nombre, capacidad, tipo) VALUES (:nombre, :capacidad, :tipo)');
$alta->execute(['nombre' => 'Delfín', 'capacidad' => 300, 'tipo' => 'velero']);
$id = (int) $pdo->lastInsertId();
echo "Nuevo barco con id $id\n";
$cambio = $pdo->prepare('UPDATE barco SET capacidad = ? WHERE id = ?');
$cambio->execute([350, $id]);
echo "Filas cambiadas: ", $cambio->rowCount(), "\n";

// Un duplicado: la base lo rechaza y reaccionamos
try {
    $alta->execute(['nombre' => 'Gaviota', 'capacidad' => 100, 'tipo' => 'velero']);
} catch (PDOException $e) {
    echo $e->errorInfo[1] === 1062 ? "Ya existe un barco con ese nombre.\n" : "Otro error\n";
}
echo "Barcos: ", $pdo->query('SELECT COUNT(*) FROM barco')->fetchColumn(), "\n";
```

### Salida esperada

```
Pegando el dato: 5 barco/s (¡todos!)
Con parámetro: 0 barco/s
Buscando Gaviota: Gaviota
  Albatros (1200.00 kg)
  Garza (300.00 kg)
  Gaviota (450.00 kg)
Por id: Gaviota, Tortuga, Cóndor
Ordenado por: nombre
Página 2: Tortuga, Garza
Nuevo barco con id 6
Filas cambiadas: 1
Ya existe un barco con ese nombre.
Barcos: 6
```

### ¿Para qué sirve?

La inyección SQL estuvo durante años en el primer puesto de las fallas de seguridad de la web, y sigue apareciendo: filtraciones de millones de usuarios empezaron por un buscador que pegaba el texto en la consulta. Con consultas preparadas desaparece. Laravel y cualquier ORM las usan por debajo; cuando escribas SQL a mano (y lo vas a hacer), es tu responsabilidad.

### Errores habituales

**Troll: pegar el dato "solo esta vez".** `"… WHERE id = $id"` parece inofensivo
porque "el id es un número"… hasta que alguien manda `1 OR 1=1`. Parámetros siempre.

**Troll: escapar a mano.** `addslashes` o `str_replace("'", "\\'", …)` no alcanzan
(hay casos que se escapan). La única forma segura son los parámetros.

**Goblin: `LIMIT '5'`.** Con la emulación activada, `execute([5])` en un `LIMIT ?`
da error de sintaxis. Usá `bindValue(…, PDO::PARAM_INT)` o `ATTR_EMULATE_PREPARES =>
false`.

**Esqueleto: el nombre de columna como parámetro.** `ORDER BY ?` no ordena por la
columna: ordena por un texto fijo (no hace nada). Las columnas se eligen con una
lista blanca.

**Goblin: el mismo parámetro dos veces.** Sin emulación, `WHERE apellido LIKE :texto
OR dni LIKE :texto` da `SQLSTATE[HY093]: Invalid parameter number`: cada nombre se
usa una sola vez (`:apellido`, `:dni`) y se pasa el valor dos veces.

**Ogro: las comillas alrededor del hueco.** `WHERE nombre = '?'` busca el texto
`?` literal. El hueco va sin comillas: `WHERE nombre = ?`.

### Misión R04-N05-M1 · El buscador blindado

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Escribí `buscador.php`, un programa de terminal que busca pasajeros. Recibe por
argumentos (`$argv`) un texto para el nombre y, opcionalmente, una edad mínima:
`php buscador.php "an" 18`. Tiene que:

- buscar con `LIKE` (el texto en cualquier parte del nombre) y edad `>=`, con una
  consulta preparada con parámetros con nombre;
- validar la edad con `filter_var` (si no es un entero válido, se usa 0);
- probar, además, los argumentos de ataque `"' OR '1'='1"` y `"%"` y mostrar que
  no devuelven lo que no deben (el `%` literal hay que escaparlo: reemplazá `%` y `_`
  por `\%` y `\_` antes de armar el patrón).

Para poder probarlo sin escribir argumentos, si no se pasa ninguno se ejecutan las
búsquedas del ejemplo.

#### Criterio de aprobación

- Usa `prepare`/`execute` con parámetros con nombre; nada de datos pegados.
- Escapa `%` y `_` en el texto buscado.
- La salida coincide con la esperada.

#### Salida esperada

```
«an» desde 18 años: Ana Pérez (34), Dante 100% (30), Mariana Luz (22)
«an» desde mil años: Ana Pérez (34), Dante 100% (30), Juan Álvarez (16), Mariana Luz (22)
«' OR '1'='1» desde 0 años: nadie
«%» desde 0 años: Dante 100% (30)
«100%» desde 0 años: Dante 100% (30)
```

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS pasajero;
CREATE TABLE pasajero (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(40) NOT NULL, edad INT NOT NULL);
INSERT INTO pasajero (nombre, edad) VALUES ('Ana Pérez', 34), ('Juan Álvarez', 16), ('Mariana Luz', 22), ('Bron', 45), ('Dante 100%', 30);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`buscador.php`
```php
<?php
declare(strict_types=1);
// Mision 1 - El buscador blindado: LIKE con parámetros y comodines escapados.
$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

function buscar(PDO $pdo, string $texto, string $edad): array
{
    $minimo = filter_var($edad, FILTER_VALIDATE_INT) ?: 0;
    $patron = '%' . str_replace(['%', '_'], ['\%', '\_'], $texto) . '%';
    $consulta = $pdo->prepare('SELECT nombre, edad FROM pasajero WHERE nombre LIKE :patron AND edad >= :minimo ORDER BY nombre');
    $consulta->execute(['patron' => $patron, 'minimo' => $minimo]);
    return $consulta->fetchAll();
}

$pruebas = $argc > 1 ? [[$argv[1], $argv[2] ?? '0']] : [['an', '18'], ['an', 'mil'], ["' OR '1'='1", '0'], ['%', '0'], ['100%', '0']];
foreach ($pruebas as [$texto, $edad]) {
    $filas = buscar($pdo, $texto, $edad);
    echo "«{$texto}» desde $edad años: ", $filas === [] ? 'nadie' : implode(', ', array_map(fn($f) => "{$f['nombre']} ({$f['edad']})", $filas)), "\n";
}
```

### Misión R04-N05-M2 · El ordenamiento elegido

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Una página lista productos y deja elegir **por qué columna ordenar**, el
**sentido** y la **página** por GET (`?orden=precio&sentido=desc&pagina=2`). Escribí
`public/index.php` que:

- ordena solo por `descripcion`, `precio` o `stock` (lista blanca; si no, por
  `descripcion`) y en `ASC` o `DESC`;
- pagina de a 3 con `LIMIT` y `OFFSET` como parámetros enteros;
- muestra enlaces para ordenar por cada columna (el que ya está elegido cambia el
  sentido al hacer clic) y para las páginas.

Probá la dirección `?orden=precio;DROP TABLE producto` y verificá que no pasa nada.

#### Criterio de aprobación

- Columnas y sentido por lista blanca; `LIMIT`/`OFFSET` como parámetros.
- Nada del pedido se pega en la consulta.
- La tabla sigue intacta después del intento de ataque.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (id INT AUTO_INCREMENT PRIMARY KEY, descripcion VARCHAR(60) NOT NULL, precio DECIMAL(10, 2) NOT NULL, stock INT NOT NULL);
INSERT INTO producto (descripcion, precio, stock) VALUES
    ('Yerba', 4200, 40), ('Azúcar', 1500, 10), ('Fideos', 1100, 60), ('Aceite', 3800, 5),
    ('Arroz', 1700, 25), ('Harina', 890, 80), ('Café', 6900, 12);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Mision 2 - El ordenamiento elegido: lista blanca para columnas y LIMIT con parámetros.
$c = require __DIR__ . '/../config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);
const COLUMNAS = ['descripcion' => 'Producto', 'precio' => 'Precio', 'stock' => 'Stock'];
const POR_PAGINA = 3;

$orden = array_key_exists($_GET['orden'] ?? '', COLUMNAS) ? $_GET['orden'] : 'descripcion';
$sentido = ($_GET['sentido'] ?? '') === 'desc' ? 'desc' : 'asc';
$total = (int) $pdo->query('SELECT COUNT(*) FROM producto')->fetchColumn();
$paginas = (int) ceil($total / POR_PAGINA);
$pagina = min(max(1, (int) ($_GET['pagina'] ?? 1)), $paginas);

$consulta = $pdo->prepare("SELECT descripcion, precio, stock FROM producto ORDER BY $orden $sentido, id LIMIT ? OFFSET ?");
$consulta->execute([POR_PAGINA, ($pagina - 1) * POR_PAGINA]);
$filas = $consulta->fetchAll();
$enlace = fn(array $extra): string => '?' . http_build_query(array_merge(['orden' => $orden, 'sentido' => $sentido, 'pagina' => $pagina], $extra));
?>
<table>
    <tr>
        <?php foreach (COLUMNAS as $columna => $titulo): ?>
            <th><a href="<?= $enlace(['orden' => $columna, 'sentido' => $columna === $orden && $sentido === 'asc' ? 'desc' : 'asc', 'pagina' => 1]) ?>"><?= $titulo ?></a></th>
        <?php endforeach; ?>
    </tr>
    <?php foreach ($filas as $f): ?>
        <tr><td><?= htmlspecialchars($f['descripcion']) ?></td><td><?= $f['precio'] ?></td><td><?= $f['stock'] ?></td></tr>
    <?php endforeach; ?>
</table>
<p>Página <?= $pagina ?> de <?= $paginas ?> · orden: <?= $orden ?> <?= $sentido ?>
    <?php for ($p = 1; $p <= $paginas; $p++): ?> <a href="<?= $enlace(['pagina' => $p]) ?>"><?= $p ?></a><?php endfor; ?></p>
```

### Misión R04-N05-M3 · La carga masiva

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Un importador lee socios desde la entrada estándar (`NOMBRE;DNI;CATEGORIA`, uno por
renglón) y los carga en la tabla `socio` (DNI único, categoría `ENUM`). Escribí
`importar.php` que:

- prepara **una sola vez** el `INSERT` y lo ejecuta para cada renglón;
- si un DNI ya existe (error `1062`), lo informa y sigue;
- si la categoría no es válida, la base la rechaza (en modo estricto da el error
  `1265`, *Data truncated*): informalo y seguí;
- al final muestra cuántos se cargaron, cuántos fallaron y el último `id` generado.

#### Criterio de aprobación

- Un solo `prepare`, muchos `execute`.
- Atrapa los errores por código y sigue con el resto.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
Ana Pérez;30111222;activo
Beto Díaz;31222333;cadete
Carla Gómez;30111222;activo
Diego Ruiz;33444555;honorario
Elena Sosa;34555666;vitalicio
```

#### Salida esperada

```
Renglón 3: el DNI 30111222 ya está cargado
Renglón 4: la categoría «honorario» no existe
Cargados: 3 · fallados: 2 · último id: 4
```

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS socio;
CREATE TABLE socio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    dni CHAR(8) NOT NULL UNIQUE,
    categoria ENUM('activo', 'cadete', 'vitalicio') NOT NULL
);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`importar.php`
```php
<?php
declare(strict_types=1);
// Mision 3 - La carga masiva: un prepare, muchos execute y errores por código.
$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);
$pdo->exec("SET SESSION sql_mode = 'STRICT_ALL_TABLES'");   // rechazar valores inválidos en lugar de truncarlos

$alta = $pdo->prepare('INSERT INTO socio (nombre, dni, categoria) VALUES (?, ?, ?)');
$cargados = 0;
$fallados = 0;
$numero = 0;
while (($linea = fgets(STDIN)) !== false) {
    $numero++;
    if (trim($linea) === '') {
        continue;
    }
    [$nombre, $dni, $categoria] = array_map('trim', explode(';', $linea));
    try {
        $alta->execute([$nombre, $dni, $categoria]);
        $cargados++;
    } catch (PDOException $e) {
        $fallados++;
        $motivo = match ($e->errorInfo[1] ?? null) {
            1062 => "el DNI $dni ya está cargado",
            1265 => "la categoría «{$categoria}» no existe",
            default => throw $e,
        };
        echo "Renglón $numero: $motivo\n";
    }
}
echo "Cargados: $cargados · fallados: $fallados · último id: ", $pdo->lastInsertId(), "\n";
```

### Encargo R04-N05-E1 · El login contra la base, sin agujeros

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Este login de un sistema de gestión tiene un agujero clásico: arma la consulta
pegando el usuario y la contraseña. Con `' OR '1'='1' -- ` como usuario, entra
cualquiera. Reescribilo:

- la tabla `usuario` guarda el **hash** de la contraseña (el `esquema.sql` ya trae
  dos usuarios con hash de `ancla123` y `faro2026`);
- se busca **solo por usuario**, con una consulta preparada, y la contraseña se
  comprueba con `password_verify`;
- el mensaje de error no dice qué falló.

Hacelo como programa de terminal que prueba varios intentos (incluido el ataque) y
muestra `Acceso concedido: NOMBRE (rol)` o `Usuario o contraseña incorrectos.` para
cada uno.

#### Criterio de aprobación

- Consulta preparada por usuario y `password_verify`; nada pegado.
- El ataque no entra.
- La salida coincide con la esperada.

#### Código inicial

```php
$sql = "SELECT * FROM usuario WHERE usuario = '$usuario' AND clave = '$clave'";
$fila = $pdo->query($sql)->fetch();
echo $fila ? "Acceso concedido: {$fila['nombre']}" : "Usuario o contraseña incorrectos.";
```

#### Salida esperada

```
«kira»              Acceso concedido: Kira Valdez (admin)
«bron»              Usuario o contraseña incorrectos.
«' OR '1'='1' -- »  Usuario o contraseña incorrectos.
«Bron»              Acceso concedido: Bron (vendedor)
«nadie»             Usuario o contraseña incorrectos.
```

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS usuario;
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(40) NOT NULL,
    rol ENUM('admin', 'vendedor') NOT NULL,
    hash VARCHAR(255) NOT NULL
);
INSERT INTO usuario (usuario, nombre, rol, hash) VALUES
    ('kira', 'Kira Valdez', 'admin', '$2y$10$R7flf57cYzLAnMr14xX56OhKUJ5qlAco9VY/EbWmghiXoQB.vb5yS'),
    ('bron', 'Bron', 'vendedor', '$2y$10$sY48d8IabcyzFGOVp12ZpuujEDnEgiSNQdtdVIB1rIGD4/BG9LYF6');
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`login.php`
```php
<?php
declare(strict_types=1);
// Encargo - El login contra la base: buscar por usuario con parámetros y verificar el hash.
$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

function login(PDO $pdo, string $usuario, string $clave): ?array
{
    $consulta = $pdo->prepare('SELECT nombre, rol, hash FROM usuario WHERE usuario = ?');
    $consulta->execute([mb_strtolower(trim($usuario))]);
    $fila = $consulta->fetch();
    return $fila !== false && password_verify($clave, $fila['hash']) ? $fila : null;
}

$intentos = [['kira', 'ancla123'], ['bron', 'ancla123'], ["' OR '1'='1' -- ", 'cualquiera'], ['Bron', 'faro2026'], ['nadie', 'x']];
foreach ($intentos as [$usuario, $clave]) {
    $yo = login($pdo, $usuario, $clave);
    echo str_pad("«{$usuario}»", 22), $yo !== null ? "Acceso concedido: {$yo['nombre']} ({$yo['rol']})" : 'Usuario o contraseña incorrectos.', "\n";
}
```

### Prueba del sello

#### ¿Qué es la inyección SQL?

Un ataque en el que un dato de afuera, pegado en el texto de una consulta, se convierte en código SQL y cambia lo que hace la consulta.

#### ¿Cómo la evitan las consultas preparadas?

Mandando la consulta con huecos y los datos aparte: la base trata los datos siempre como valores, nunca como código.

#### ¿Se puede poner el nombre de una columna como parámetro?

No: los parámetros son solo para valores. Las columnas elegidas por el usuario se validan contra una lista blanca.

#### ¿Por qué falla `LIMIT ?` con `execute([5])` en la configuración por defecto?

Porque PDO emula las preparadas y pone el valor entre comillas (`LIMIT '5'`). Se resuelve con `bindValue(…, PDO::PARAM_INT)` o con `ATTR_EMULATE_PREPARES => false`.

#### ¿Qué devuelve `lastInsertId()`?

El `id` que generó `AUTO_INCREMENT` en el último `INSERT` de esa conexión.

### Soluciones (docente)

Sale de `21-PHP/17-PDO-SQLite` (la parte de prepared statements), con MariaDB y el ataque demostrado. En la misión 3, el último id es 4 aunque se cargaron 3 socios: un `INSERT` que falla puede consumir un número de `AUTO_INCREMENT` (los ids no son correlativos sin huecos, y no hay que usarlos como numeración de comprobantes). También se fuerza `STRICT_ALL_TABLES` para que un `ENUM` inválido dé error (en XAMPP suele venir activado; en algunos servidores viejos no, y el valor se guardaba vacío). En el encargo, el `-- ` del ataque comenta el resto de la consulta vulnerable: vale la pena mostrarlo en clase contra el código inicial (en una base de práctica).

## R04-N06 · Un ABM web

```meta
tipo: tema
padre: R04-N05
precio: 10
criatura: goblin
```

### Crónica

La Capitana te da una llave de la Bodega con una etiqueta: *Inventario de repuestos*. —Hasta hoy lo llevaba un empleado en una planilla, y cada tanto se le borraba una fila —dice—. Quiero que el taller pueda **ver** los repuestos, **agregar** los nuevos, **corregir** los que están mal y **dar de baja** los que ya no se usan. Todo desde el navegador, {heroe}, y sin que nadie pueda romper nada.

Lo que te pide tiene un nombre en todos los sistemas del mundo: un **ABM** (alta, baja, modificación), el CRUD de los programadores.

### Objetivos

- Armar un listado, un alta, una edición y una baja de una tabla desde la web.
- Reusar el mismo formulario para el alta y la edición.
- Validar en PHP y dejar que la base proteja lo suyo (duplicados, claves foráneas).
- Usar consultas preparadas, CSRF, PRG y mensajes flash en cada acción.
- Confirmar las bajas y responder 404 cuando el registro no existe.

### Antes de empezar

- Consultas preparadas (R04-N05) y formularios seguros con plantillas (R03-N03 a R03-N08).

### Explicación

#### Las cuatro operaciones
| Acción | Método | SQL |
|---|---|---|
| **Listar** | GET `?accion=listar` | `SELECT … ORDER BY …` |
| **Alta** | GET muestra el formulario vacío; POST lo guarda | `INSERT` |
| **Modificación** | GET `?accion=editar&id=5` muestra el formulario lleno; POST lo guarda | `UPDATE … WHERE id = ?` |
| **Baja** | POST (nunca un GET: un enlace no puede borrar) | `DELETE … WHERE id = ?` |

#### Un solo formulario
El alta y la edición usan el **mismo** formulario: si hay un `id`, es edición
(se precargan los datos y se hace `UPDATE`); si no, es alta (`INSERT`). La
validación también es la misma función.

#### Buscar el registro o 404
```php
function buscarRepuesto(PDO $pdo, int $id): ?array
{
    $c = $pdo->prepare('SELECT * FROM repuesto WHERE id = ?');
    $c->execute([$id]);
    return $c->fetch() ?: null;       // fetch da false si no hay fila
}

$repuesto = buscarRepuesto($pdo, (int) ($_GET['id'] ?? 0));
if ($repuesto === null) {
    http_response_code(404);
    exit('Ese repuesto no existe.');
}
```

#### Validar en PHP… y en la base
- En PHP se valida lo que se puede explicar bien al usuario: campos obligatorios,
  largos, números, listas.
- La base protege lo que PHP no puede garantizar solo: dos personas cargando el
  mismo código **al mismo tiempo** pasan la validación de PHP, pero la base rechaza
  el segundo (`UNIQUE`, error `1062`). Se atrapa y se muestra como error del campo.

#### Borrar con cuidado
- Siempre por **POST** con CSRF (un enlace `?borrar=5` lo puede disparar cualquier
  sitio o un buscador que recorra la página).
- Confirmar antes (`onclick="return confirm('¿Seguro?')"` en el botón es lo
  mínimo; mejor una pantalla de confirmación).
- Si hay otras tablas que lo usan, la clave foránea lo impide (`1451`): se avisa
  "No se puede borrar: está en uso". Muchas veces, en lugar de borrar, se
  **desactiva** (`activo = FALSE`): se lo llama *baja lógica*.

### Código de ejemplo

`esquema.sql`
```sql
DROP TABLE IF EXISTS repuesto;
CREATE TABLE repuesto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(10) NOT NULL UNIQUE,
    descripcion VARCHAR(80) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio > 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0)
);
INSERT INTO repuesto (codigo, descripcion, precio, stock) VALUES
    ('HEL-01', 'Hélice de bronce 3 palas', 185000, 2),
    ('BUJ-12', 'Bujía para motor fuera de borda', 7800, 40),
    ('CAB-05', 'Cabo de amarre 10 m', 22500, 15);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`src/app.php`
```php
<?php
declare(strict_types=1);

function conectar(): PDO
{
    static $pdo = null;
    if ($pdo === null) {
        $c = require __DIR__ . '/../config.php';
        $pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false,
        ]);
    }
    return $pdo;
}

function e(string $t): string
{
    return htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
}

function csrf(): string
{
    return $_SESSION['csrf'] ??= bin2hex(random_bytes(32));
}

function exigirCsrf(): void
{
    if (!hash_equals($_SESSION['csrf'] ?? '', $_POST['csrf'] ?? '')) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
}

function flash(?string $m = null): ?string
{
    if ($m !== null) {
        $_SESSION['flash'] = $m;
        return null;
    }
    $actual = $_SESSION['flash'] ?? null;
    unset($_SESSION['flash']);
    return $actual;
}

function volverAlListado(string $mensaje): never
{
    flash($mensaje);
    header('Location: index.php', true, 303);
    exit;
}

function noEncontrado(string $mensaje): never
{
    http_response_code(404);
    exit($mensaje);
}

function buscarRepuesto(int $id): ?array
{
    $c = conectar()->prepare('SELECT * FROM repuesto WHERE id = ?');
    $c->execute([$id]);
    return $c->fetch() ?: null;
}

/** Devuelve los errores por campo. */
function validarRepuesto(array $d): array
{
    $errores = [];
    if (!preg_match('/^[A-Z]{3}-\d{2}$/', $d['codigo'])) {
        $errores['codigo'] = 'El código es AAA-00 (tres letras, guion, dos números).';
    }
    if ($d['descripcion'] === '' || mb_strlen($d['descripcion']) > 80) {
        $errores['descripcion'] = 'La descripción va de 1 a 80 caracteres.';
    }
    if (filter_var($d['precio'], FILTER_VALIDATE_FLOAT) === false || (float) $d['precio'] <= 0) {
        $errores['precio'] = 'El precio tiene que ser un número mayor que 0.';
    }
    if (filter_var($d['stock'], FILTER_VALIDATE_INT, ['options' => ['min_range' => 0]]) === false) {
        $errores['stock'] = 'El stock es un entero de 0 en adelante.';
    }
    return $errores;
}
```

`vistas/listado.php`
```php
<h1>Repuestos</h1>
<?php if ($flash !== null): ?><p><strong><?= e($flash) ?></strong></p><?php endif; ?>
<p><a href="?accion=nuevo">Nuevo repuesto</a></p>
<table>
    <tr><th>Código</th><th>Descripción</th><th>Precio</th><th>Stock</th><th></th></tr>
    <?php foreach ($repuestos as $r): ?>
        <tr>
            <td><?= e($r['codigo']) ?></td><td><?= e($r['descripcion']) ?></td>
            <td>$<?= number_format((float) $r['precio'], 2, ',', '.') ?></td><td><?= $r['stock'] ?></td>
            <td>
                <a href="?accion=editar&amp;id=<?= $r['id'] ?>">Editar</a>
                <form method="post" action="?accion=borrar" style="display:inline">
                    <input type="hidden" name="csrf" value="<?= csrf() ?>">
                    <input type="hidden" name="id" value="<?= $r['id'] ?>">
                    <button onclick="return confirm('¿Borrar <?= e($r['codigo']) ?>?')">Borrar</button>
                </form>
            </td>
        </tr>
    <?php endforeach; ?>
</table>
```

`vistas/formulario.php`
```php
<h1><?= $id === null ? 'Nuevo repuesto' : 'Editar ' . e($datos['codigo']) ?></h1>
<form method="post">
    <input type="hidden" name="csrf" value="<?= csrf() ?>">
    <?php foreach (['codigo' => 'Código', 'descripcion' => 'Descripción', 'precio' => 'Precio', 'stock' => 'Stock'] as $campo => $etiqueta): ?>
        <p><label><?= $etiqueta ?>: <input name="<?= $campo ?>" value="<?= e((string) $datos[$campo]) ?>"></label>
            <?php if (isset($errores[$campo])): ?><strong><?= e($errores[$campo]) ?></strong><?php endif; ?></p>
    <?php endforeach; ?>
    <button>Guardar</button> <a href="index.php">Cancelar</a>
</form>
```

`public/index.php`
```php
<?php
declare(strict_types=1);
/*
 * El inventario de repuestos: listado, alta, modificación y baja con PDO.
 */
session_start();
require __DIR__ . '/../src/app.php';

function vista(string $__vista, array $__datos = []): string
{
    extract($__datos);
    ob_start();
    require __DIR__ . "/../vistas/$__vista.php";
    return ob_get_clean();
}

$accion = $_GET['accion'] ?? 'listar';
$pdo = conectar();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    exigirCsrf();
}

switch ($accion) {
    case 'nuevo':
    case 'editar':
        $id = $accion === 'editar' ? (int) ($_GET['id'] ?? 0) : null;
        $datos = ['codigo' => '', 'descripcion' => '', 'precio' => '', 'stock' => '0'];
        if ($id !== null) {
            $datos = buscarRepuesto($id) ?? noEncontrado('Ese repuesto no existe.');
        }
        $errores = [];
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            foreach (['codigo', 'descripcion', 'precio', 'stock'] as $campo) {
                $datos[$campo] = trim((string) ($_POST[$campo] ?? ''));
            }
            $datos['codigo'] = strtoupper($datos['codigo']);
            $datos['precio'] = str_replace(',', '.', $datos['precio']);
            $errores = validarRepuesto($datos);
            if ($errores === []) {
                $valores = [$datos['codigo'], $datos['descripcion'], $datos['precio'], $datos['stock']];
                try {
                    if ($id === null) {
                        $pdo->prepare('INSERT INTO repuesto (codigo, descripcion, precio, stock) VALUES (?, ?, ?, ?)')->execute($valores);
                        volverAlListado("Agregaste {$datos['codigo']}.");
                    }
                    $pdo->prepare('UPDATE repuesto SET codigo = ?, descripcion = ?, precio = ?, stock = ? WHERE id = ?')->execute([...$valores, $id]);
                    volverAlListado("Guardaste {$datos['codigo']}.");
                } catch (PDOException $e) {
                    if (($e->errorInfo[1] ?? null) !== 1062) {
                        throw $e;
                    }
                    $errores['codigo'] = 'Ya hay un repuesto con ese código.';
                }
            }
        }
        echo vista('formulario', ['id' => $id, 'datos' => $datos, 'errores' => $errores]);
        break;

    case 'borrar':
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            http_response_code(405);
            exit('Para borrar, usá el botón.');
        }
        $repuesto = buscarRepuesto((int) ($_POST['id'] ?? 0));
        if ($repuesto === null) {
            http_response_code(404);
            exit('Ese repuesto no existe.');
        }
        $pdo->prepare('DELETE FROM repuesto WHERE id = ?')->execute([$repuesto['id']]);
        volverAlListado("Borraste {$repuesto['codigo']}.");

    default:
        $repuestos = $pdo->query('SELECT * FROM repuesto ORDER BY codigo')->fetchAll();
        echo vista('listado', ['repuestos' => $repuestos, 'flash' => flash()]);
}
```

### ¿Para qué sirve?

La mitad de los sistemas de gestión son ABMs: productos, clientes, proveedores, empleados, turnos. Hacer uno completo, seguro y cómodo de usar es el ejercicio más pedido en entrevistas y en la facultad. Laravel los arma con *resource controllers* (`index`, `create`, `store`, `edit`, `update`, `destroy`): exactamente las acciones que armaste acá.

### Errores habituales

**Troll: borrar con un enlace.** `<a href="?borrar=5">` permite que cualquier sitio (o
un buscador que siga enlaces) borre datos. Las bajas van por POST con CSRF.

**Troll: el `UPDATE` sin `WHERE id = ?`.** Cambia **todos** los repuestos. Revisá que
cada `UPDATE` y `DELETE` tenga su `WHERE`.

**Esqueleto: editar algo que no existe.** `?accion=editar&id=999` sin buscar primero
da avisos de claves inexistentes. Buscá el registro y respondé 404.

**Goblin: el duplicado que llega igual.** Validar en PHP que el código no exista no
alcanza (dos personas a la vez). Dejá el `UNIQUE` en la base y atrapá el `1062`.

**Ogro: el formulario que se vacía.** Si el POST tiene errores y no volvés a poner
los valores en los `value`, la persona tiene que escribir todo de nuevo.

### Misión R04-N06-M1 · El ABM de proveedores

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Armá el ABM de **proveedores** del taller (razón social, CUIT único, teléfono,
email opcional y rubro de una lista fija), siguiendo el ejemplo del nodo:

- listado ordenado por razón social, con un buscador GET por razón social (`LIKE`
  con parámetro);
- alta y edición con el mismo formulario, validación por campo y el `1062` del
  CUIT atrapado como error del campo;
- baja por POST con CSRF, y 404 si no existe;
- PRG con mensajes flash.

#### Criterio de aprobación

- Las cuatro operaciones funcionan con consultas preparadas.
- Alta y edición comparten formulario y validación.
- Las bajas son POST con CSRF; los inexistentes dan 404.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS proveedor;
CREATE TABLE proveedor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    razon VARCHAR(60) NOT NULL,
    cuit CHAR(11) NOT NULL UNIQUE,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(80) NULL,
    rubro ENUM('repuestos', 'pinturas', 'electricidad', 'maderas') NOT NULL
);
INSERT INTO proveedor (razon, cuit, telefono, email, rubro) VALUES
    ('Náutica del Puerto SA', '30711222334', '380-4123456', 'ventas@nautica.com', 'repuestos'),
    ('Pinturerías Faro', '20123456786', '380-4555666', NULL, 'pinturas');
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Mision 1 - El ABM de proveedores: listado, alta, edición y baja.
session_start();
$c = require __DIR__ . '/../config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);
const RUBROS = ['repuestos', 'pinturas', 'electricidad', 'maderas'];

function e(?string $t): string
{
    return htmlspecialchars($t ?? '', ENT_QUOTES, 'UTF-8');
}

function ir(string $mensaje): never
{
    $_SESSION['flash'] = $mensaje;
    header('Location: index.php', true, 303);
    exit;
}

function noEncontrado(string $mensaje): never
{
    http_response_code(404);
    exit($mensaje);
}

function buscar(PDO $pdo, int $id): ?array
{
    $s = $pdo->prepare('SELECT * FROM proveedor WHERE id = ?');
    $s->execute([$id]);
    return $s->fetch() ?: null;
}

$_SESSION['csrf'] ??= bin2hex(random_bytes(32));
if ($_SERVER['REQUEST_METHOD'] === 'POST' && !hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
    http_response_code(403);
    exit('Pedido no válido.');
}
$accion = $_GET['accion'] ?? 'listar';

if ($accion === 'borrar' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $p = buscar($pdo, (int) ($_POST['id'] ?? 0)) ?? noEncontrado('No existe.');
    $pdo->prepare('DELETE FROM proveedor WHERE id = ?')->execute([$p['id']]);
    ir("Borraste a {$p['razon']}.");
}

if ($accion === 'nuevo' || $accion === 'editar') {
    $id = $accion === 'editar' ? (int) ($_GET['id'] ?? 0) : null;
    $d = $id === null ? ['razon' => '', 'cuit' => '', 'telefono' => '', 'email' => '', 'rubro' => 'repuestos'] : (buscar($pdo, $id) ?? noEncontrado('No existe.'));
    $errores = [];
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        foreach (['razon', 'cuit', 'telefono', 'email', 'rubro'] as $campo) {
            $d[$campo] = trim((string) ($_POST[$campo] ?? ''));
        }
        $d['cuit'] = str_replace('-', '', $d['cuit']);
        if (mb_strlen($d['razon']) < 3) {
            $errores['razon'] = 'La razón social es obligatoria.';
        }
        if (!preg_match('/^\d{11}$/', $d['cuit'])) {
            $errores['cuit'] = 'El CUIT tiene 11 números.';
        }
        if (!preg_match('/^[\d\s+-]{8,20}$/', $d['telefono'])) {
            $errores['telefono'] = 'El teléfono no es válido.';
        }
        if ($d['email'] !== '' && filter_var($d['email'], FILTER_VALIDATE_EMAIL) === false) {
            $errores['email'] = 'El email no es válido.';
        }
        if (!in_array($d['rubro'], RUBROS, true)) {
            $errores['rubro'] = 'Rubro inválido.';
        }
        if ($errores === []) {
            $valores = [$d['razon'], $d['cuit'], $d['telefono'], $d['email'] === '' ? null : $d['email'], $d['rubro']];
            try {
                if ($id === null) {
                    $pdo->prepare('INSERT INTO proveedor (razon, cuit, telefono, email, rubro) VALUES (?, ?, ?, ?, ?)')->execute($valores);
                } else {
                    $pdo->prepare('UPDATE proveedor SET razon = ?, cuit = ?, telefono = ?, email = ?, rubro = ? WHERE id = ?')->execute([...$valores, $id]);
                }
                ir("Guardaste a {$d['razon']}.");
            } catch (PDOException $ex) {
                if (($ex->errorInfo[1] ?? null) !== 1062) {
                    throw $ex;
                }
                $errores['cuit'] = 'Ya hay un proveedor con ese CUIT.';
            }
        }
    }
    ?>
    <h1><?= $id === null ? 'Nuevo proveedor' : 'Editar proveedor' ?></h1>
    <form method="post">
        <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
        <?php foreach (['razon' => 'Razón social', 'cuit' => 'CUIT', 'telefono' => 'Teléfono', 'email' => 'Email'] as $campo => $etiqueta): ?>
            <p><?= $etiqueta ?>: <input name="<?= $campo ?>" value="<?= e($d[$campo]) ?>"> <?= isset($errores[$campo]) ? '<strong>' . e($errores[$campo]) . '</strong>' : '' ?></p>
        <?php endforeach; ?>
        <select name="rubro"><?php foreach (RUBROS as $r): ?><option <?= $d['rubro'] === $r ? 'selected' : '' ?>><?= $r ?></option><?php endforeach; ?></select>
        <?= isset($errores['rubro']) ? '<strong>' . e($errores['rubro']) . '</strong>' : '' ?>
        <button>Guardar</button>
    </form>
    <?php
    exit;
}

$q = trim($_GET['q'] ?? '');
$s = $pdo->prepare('SELECT * FROM proveedor WHERE razon LIKE ? ORDER BY razon');
$s->execute(['%' . $q . '%']);
$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']);
?>
<h1>Proveedores</h1>
<?php if ($flash): ?><p><?= e($flash) ?></p><?php endif; ?>
<form method="get"><input name="q" value="<?= e($q) ?>"> <button>Buscar</button></form>
<p><a href="?accion=nuevo">Nuevo proveedor</a></p>
<ul>
    <?php foreach ($s as $p): ?>
        <li><?= e($p['razon']) ?> (<?= e($p['cuit']) ?>, <?= e($p['rubro']) ?>)
            <a href="?accion=editar&amp;id=<?= $p['id'] ?>">Editar</a>
            <form method="post" action="?accion=borrar" style="display:inline">
                <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>"><input type="hidden" name="id" value="<?= $p['id'] ?>"><button>Borrar</button>
            </form></li>
    <?php endforeach; ?>
</ul>
```

### Misión R04-N06-M2 · La baja lógica

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

En un sistema de **empleados**, no se borra a nadie (los recibos de sueldo lo
necesitan): se lo **da de baja** con fecha. Con la tabla `empleado` (nombre,
legajo único, puesto, `baja DATE NULL`), armá `public/index.php`:

- el listado muestra por defecto solo los activos (`baja IS NULL`); con
  `?ver=todos`, también los dados de baja (marcados `(baja: dd/mm/aaaa)`);
- **Dar de baja** (POST con CSRF) pone la fecha de hoy (`CURDATE()`) y **Reincorporar**
  la vuelve a `NULL`;
- un empleado dado de baja no se puede dar de baja de nuevo (`rowCount()` del
  `UPDATE … WHERE id = ? AND baja IS NULL` dice si cambió algo).

Mostrá mensajes flash con el resultado.

#### Criterio de aprobación

- No hay `DELETE`: la baja es una fecha.
- El listado filtra activos por defecto.
- Usa `rowCount()` para saber si la baja se aplicó.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS empleado;
CREATE TABLE empleado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    legajo INT NOT NULL UNIQUE,
    puesto VARCHAR(30) NOT NULL,
    baja DATE NULL
);
INSERT INTO empleado (nombre, legajo, puesto, baja) VALUES
    ('Ana Pérez', 101, 'administración', NULL), ('Beto Díaz', 102, 'depósito', NULL),
    ('Carla Gómez', 103, 'ventas', '2026-06-30'), ('Diego Ruiz', 104, 'ventas', NULL);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Mision 2 - La baja lógica: dar de baja con una fecha en lugar de borrar.
session_start();
$c = require __DIR__ . '/../config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);
$_SESSION['csrf'] ??= bin2hex(random_bytes(32));

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
    $id = (int) ($_POST['id'] ?? 0);
    if (($_POST['accion'] ?? '') === 'baja') {
        $s = $pdo->prepare('UPDATE empleado SET baja = CURDATE() WHERE id = ? AND baja IS NULL');
        $s->execute([$id]);
        $_SESSION['flash'] = $s->rowCount() === 1 ? 'Empleado dado de baja.' : 'Ese empleado ya estaba de baja (o no existe).';
    } else {
        $s = $pdo->prepare('UPDATE empleado SET baja = NULL WHERE id = ? AND baja IS NOT NULL');
        $s->execute([$id]);
        $_SESSION['flash'] = $s->rowCount() === 1 ? 'Empleado reincorporado.' : 'Ese empleado ya estaba activo (o no existe).';
    }
    header('Location: index.php' . (isset($_GET['ver']) ? '?ver=todos' : ''), true, 303);
    exit;
}

$todos = ($_GET['ver'] ?? '') === 'todos';
$empleados = $pdo->query('SELECT id, nombre, legajo, puesto, baja FROM empleado' . ($todos ? '' : ' WHERE baja IS NULL') . ' ORDER BY legajo')->fetchAll();
$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']);
?>
<h1>Empleados <?= $todos ? '(todos)' : '(activos)' ?></h1>
<?php if ($flash): ?><p><?= htmlspecialchars($flash) ?></p><?php endif; ?>
<p><a href="?ver=<?= $todos ? 'activos' : 'todos' ?>"><?= $todos ? 'Ver solo activos' : 'Ver todos' ?></a></p>
<ul>
    <?php foreach ($empleados as $emp): ?>
        <li><?= $emp['legajo'] ?> <?= htmlspecialchars($emp['nombre']) ?> (<?= htmlspecialchars($emp['puesto']) ?>)
            <?php if ($emp['baja'] !== null): ?>(baja: <?= (new DateTimeImmutable($emp['baja']))->format('d/m/Y') ?>)<?php endif; ?>
            <form method="post" style="display:inline">
                <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>"><input type="hidden" name="id" value="<?= $emp['id'] ?>">
                <button name="accion" value="<?= $emp['baja'] === null ? 'baja' : 'reincorporar' ?>"><?= $emp['baja'] === null ? 'Dar de baja' : 'Reincorporar' ?></button>
            </form></li>
    <?php endforeach; ?>
</ul>
```

### Misión R04-N06-M3 · El borrado que no se puede

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Un sistema tiene **categorías** y **productos** (cada producto con su categoría, clave
foránea con `RESTRICT`). Armá la pantalla de categorías con alta (nombre único) y
baja. Al borrar una categoría que tiene productos, la base lo impide (error
`1451`): atrapalo y mostrá `No se puede borrar «NOMBRE»: tiene N producto/s.` (contá
los productos con una consulta preparada). El listado de categorías muestra la
cantidad de productos de cada una (con `LEFT JOIN`), y el botón de borrar solo
aparece habilitado cuando no tiene productos (pero la regla se revisa igual en el
servidor).

#### Criterio de aprobación

- La clave foránea impide el borrado y el `1451` se atrapa con un mensaje claro.
- El listado cuenta productos con `LEFT JOIN`.
- La regla se revisa en el servidor aunque el botón esté deshabilitado.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS producto;
DROP TABLE IF EXISTS categoria;
CREATE TABLE categoria (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(30) NOT NULL UNIQUE);
CREATE TABLE producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    categoria_id INT NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categoria(id) ON DELETE RESTRICT
);
INSERT INTO categoria (nombre) VALUES ('herramientas'), ('pinturas'), ('jardín');
INSERT INTO producto (nombre, categoria_id) VALUES ('Martillo', 1), ('Serrucho', 1), ('Látex blanco 20 l', 2);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Mision 3 - El borrado que no se puede: la clave foránea protege y avisamos por qué.
session_start();
$c = require __DIR__ . '/../config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);
$_SESSION['csrf'] ??= bin2hex(random_bytes(32));

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        http_response_code(403);
        exit('Pedido no válido.');
    }
    if (($_POST['accion'] ?? '') === 'alta') {
        $nombre = mb_strtolower(trim($_POST['nombre'] ?? ''));
        try {
            if ($nombre === '') {
                throw new InvalidArgumentException('Falta el nombre.');
            }
            $pdo->prepare('INSERT INTO categoria (nombre) VALUES (?)')->execute([$nombre]);
            $_SESSION['flash'] = "Agregaste «{$nombre}».";
        } catch (InvalidArgumentException $e) {
            $_SESSION['flash'] = $e->getMessage();
        } catch (PDOException $e) {
            $_SESSION['flash'] = ($e->errorInfo[1] ?? null) === 1062 ? "Ya existe «{$nombre}»." : throw $e;
        }
    } else {
        $s = $pdo->prepare('SELECT id, nombre FROM categoria WHERE id = ?');
        $s->execute([(int) ($_POST['id'] ?? 0)]);
        $cat = $s->fetch();
        if ($cat === false) {
            http_response_code(404);
            exit('No existe.');
        }
        try {
            $pdo->prepare('DELETE FROM categoria WHERE id = ?')->execute([$cat['id']]);
            $_SESSION['flash'] = "Borraste «{$cat['nombre']}».";
        } catch (PDOException $e) {
            if (($e->errorInfo[1] ?? null) !== 1451) {
                throw $e;
            }
            $n = $pdo->prepare('SELECT COUNT(*) FROM producto WHERE categoria_id = ?');
            $n->execute([$cat['id']]);
            $_SESSION['flash'] = "No se puede borrar «{$cat['nombre']}»: tiene {$n->fetchColumn()} producto/s.";
        }
    }
    header('Location: index.php', true, 303);
    exit;
}

$categorias = $pdo->query('SELECT c.id, c.nombre, COUNT(p.id) AS productos FROM categoria c LEFT JOIN producto p ON p.categoria_id = c.id GROUP BY c.id, c.nombre ORDER BY c.nombre')->fetchAll();
$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']);
?>
<h1>Categorías</h1>
<?php if ($flash): ?><p><?= htmlspecialchars($flash) ?></p><?php endif; ?>
<ul>
    <?php foreach ($categorias as $cat): ?>
        <li><?= htmlspecialchars($cat['nombre']) ?> (<?= $cat['productos'] ?> producto/s)
            <form method="post" style="display:inline">
                <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>"><input type="hidden" name="id" value="<?= $cat['id'] ?>">
                <button name="accion" value="borrar" <?= $cat['productos'] > 0 ? 'disabled' : '' ?>>Borrar</button>
            </form></li>
    <?php endforeach; ?>
</ul>
<form method="post">
    <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
    <input name="nombre"> <button name="accion" value="alta">Agregar</button>
</form>
```

### Encargo R04-N06-E1 · La agenda del consultorio con base de datos

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

El consultorio que empezó con una planilla quiere su ABM de **pacientes** en la
web, con la tabla `paciente` del esquema (nombre, apellido, DNI único, fecha de
nacimiento, teléfono, obra social de una lista). Armalo con la estructura
`public/`, `src/`, `vistas/` y:

- listado paginado (de a 5, con `LIMIT`/`OFFSET` como parámetros) y buscador por
  apellido o DNI;
- la **edad** calculada en SQL (`TIMESTAMPDIFF(YEAR, nacimiento, CURDATE())`);
- alta y edición con el mismo formulario (la fecha con `<input type="date">`
  validada con `DateTimeImmutable` y que no sea futura);
- baja con confirmación por POST;
- el `1062` del DNI atrapado como error del campo.

#### Criterio de aprobación

- ABM completo con consultas preparadas, CSRF, PRG y 404.
- Paginación con parámetros enteros y buscador con `LIKE`.
- La edad se calcula en la base.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS paciente;
CREATE TABLE paciente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    dni CHAR(8) NOT NULL UNIQUE,
    nacimiento DATE NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    obra_social ENUM('APOS', 'PAMI', 'OSPRERA', 'IOSFA', 'particular') NOT NULL DEFAULT 'particular'
);
INSERT INTO paciente (nombre, apellido, dni, nacimiento, telefono, obra_social) VALUES
    ('Ana', 'Pérez', '30111222', '1983-05-14', '380-4123456', 'APOS'), ('Beto', 'Díaz', '25333444', '1976-11-02', '380-4555666', 'PAMI'),
    ('Carla', 'Gómez', '42555666', '2000-02-29', '380-4999000', 'OSPRERA'), ('Diego', 'Ruiz', '38777888', '1995-07-21', '380-4222333', 'particular'),
    ('Elena', 'Sosa', '29888999', '1981-09-09', '380-4777111', 'APOS'), ('Fabián', 'Luna', '36111000', '1992-01-30', '380-4333999', 'IOSFA');
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`src/app.php`
```php
<?php
declare(strict_types=1);

const OBRAS = ['APOS', 'PAMI', 'OSPRERA', 'IOSFA', 'particular'];
const POR_PAGINA = 5;

function conectar(): PDO
{
    static $pdo = null;
    if ($pdo === null) {
        $c = require __DIR__ . '/../config.php';
        $pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);
    }
    return $pdo;
}

function e(?string $t): string
{
    return htmlspecialchars($t ?? '', ENT_QUOTES, 'UTF-8');
}

function vista(string $__vista, array $__datos = []): string
{
    extract($__datos);
    ob_start();
    require __DIR__ . "/../vistas/$__vista.php";
    return ob_get_clean();
}

function csrf(): string
{
    return $_SESSION['csrf'] ??= bin2hex(random_bytes(32));
}

function irAlListado(string $mensaje): never
{
    $_SESSION['flash'] = $mensaje;
    header('Location: index.php', true, 303);
    exit;
}

function noEncontrado(string $mensaje): never
{
    http_response_code(404);
    exit($mensaje);
}

function paciente(int $id): ?array
{
    $s = conectar()->prepare('SELECT * FROM paciente WHERE id = ?');
    $s->execute([$id]);
    return $s->fetch() ?: null;
}

function validarPaciente(array $d): array
{
    $errores = [];
    foreach (['nombre' => 'El nombre', 'apellido' => 'El apellido'] as $campo => $texto) {
        if ($d[$campo] === '' || mb_strlen($d[$campo]) > 50) {
            $errores[$campo] = "$texto va de 1 a 50 caracteres.";
        }
    }
    if (!preg_match('/^\d{7,8}$/', $d['dni'])) {
        $errores['dni'] = 'El DNI tiene 7 u 8 números.';
    }
    $fecha = DateTimeImmutable::createFromFormat('!Y-m-d', $d['nacimiento']);
    if ($fecha === false || $fecha->format('Y-m-d') !== $d['nacimiento'] || $fecha > new DateTimeImmutable('today')) {
        $errores['nacimiento'] = 'La fecha de nacimiento no es válida.';
    }
    if (!preg_match('/^[\d\s+-]{8,20}$/', $d['telefono'])) {
        $errores['telefono'] = 'El teléfono no es válido.';
    }
    if (!in_array($d['obra_social'], OBRAS, true)) {
        $errores['obra_social'] = 'Elegí una obra social de la lista.';
    }
    return $errores;
}
```

`vistas/listado.php`
```php
<h1>Pacientes</h1>
<?php if ($flash): ?><p><?= e($flash) ?></p><?php endif; ?>
<form method="get"><input name="q" value="<?= e($q) ?>" placeholder="Apellido o DNI"> <button>Buscar</button></form>
<p><a href="?accion=nuevo">Nuevo paciente</a> · <?= $total ?> paciente/s</p>
<table>
    <?php foreach ($pacientes as $p): ?>
        <tr><td><?= e($p['apellido']) ?>, <?= e($p['nombre']) ?></td><td><?= e($p['dni']) ?></td><td><?= $p['edad'] ?> años</td><td><?= e($p['obra_social']) ?></td>
            <td><a href="?accion=editar&amp;id=<?= $p['id'] ?>">Editar</a>
                <form method="post" action="?accion=borrar" style="display:inline"><input type="hidden" name="csrf" value="<?= csrf() ?>"><input type="hidden" name="id" value="<?= $p['id'] ?>">
                    <button onclick="return confirm('¿Borrar a <?= e($p['apellido']) ?>?')">Borrar</button></form></td></tr>
    <?php endforeach; ?>
</table>
<p>Página <?= $pagina ?> de <?= $paginas ?>
    <?php for ($i = 1; $i <= $paginas; $i++): ?> <a href="?<?= http_build_query(['q' => $q, 'pagina' => $i]) ?>"><?= $i ?></a><?php endfor; ?></p>
```

`vistas/formulario.php`
```php
<h1><?= $id === null ? 'Nuevo paciente' : 'Editar paciente' ?></h1>
<form method="post">
    <input type="hidden" name="csrf" value="<?= csrf() ?>">
    <?php foreach (['nombre' => ['Nombre', 'text'], 'apellido' => ['Apellido', 'text'], 'dni' => ['DNI', 'text'], 'nacimiento' => ['Nacimiento', 'date'], 'telefono' => ['Teléfono', 'text']] as $campo => [$etiqueta, $tipo]): ?>
        <p><?= $etiqueta ?>: <input type="<?= $tipo ?>" name="<?= $campo ?>" value="<?= e($d[$campo]) ?>"> <?= isset($errores[$campo]) ? '<strong>' . e($errores[$campo]) . '</strong>' : '' ?></p>
    <?php endforeach; ?>
    <select name="obra_social"><?php foreach (OBRAS as $o): ?><option <?= $d['obra_social'] === $o ? 'selected' : '' ?>><?= $o ?></option><?php endforeach; ?></select>
    <?= isset($errores['obra_social']) ? '<strong>' . e($errores['obra_social']) . '</strong>' : '' ?>
    <button>Guardar</button>
</form>
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Encargo - La agenda del consultorio: ABM con paginación, búsqueda y edad calculada en SQL.
session_start();
require __DIR__ . '/../src/app.php';
$pdo = conectar();
if ($_SERVER['REQUEST_METHOD'] === 'POST' && !hash_equals(csrf(), $_POST['csrf'] ?? '')) {
    http_response_code(403);
    exit('Pedido no válido.');
}
$accion = $_GET['accion'] ?? 'listar';

if ($accion === 'borrar' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $p = paciente((int) ($_POST['id'] ?? 0)) ?? noEncontrado('No existe.');
    $pdo->prepare('DELETE FROM paciente WHERE id = ?')->execute([$p['id']]);
    irAlListado("Borraste a {$p['apellido']}, {$p['nombre']}.");
}

if ($accion === 'nuevo' || $accion === 'editar') {
    $id = $accion === 'editar' ? (int) ($_GET['id'] ?? 0) : null;
    $d = $id === null ? ['nombre' => '', 'apellido' => '', 'dni' => '', 'nacimiento' => '', 'telefono' => '', 'obra_social' => 'particular'] : (paciente($id) ?? noEncontrado('No existe.'));
    $errores = [];
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        foreach (['nombre', 'apellido', 'dni', 'nacimiento', 'telefono', 'obra_social'] as $campo) {
            $d[$campo] = trim((string) ($_POST[$campo] ?? ''));
        }
        $errores = validarPaciente($d);
        if ($errores === []) {
            $valores = [$d['nombre'], $d['apellido'], $d['dni'], $d['nacimiento'], $d['telefono'], $d['obra_social']];
            try {
                if ($id === null) {
                    $pdo->prepare('INSERT INTO paciente (nombre, apellido, dni, nacimiento, telefono, obra_social) VALUES (?, ?, ?, ?, ?, ?)')->execute($valores);
                } else {
                    $pdo->prepare('UPDATE paciente SET nombre = ?, apellido = ?, dni = ?, nacimiento = ?, telefono = ?, obra_social = ? WHERE id = ?')->execute([...$valores, $id]);
                }
                irAlListado("Guardaste a {$d['apellido']}, {$d['nombre']}.");
            } catch (PDOException $ex) {
                if (($ex->errorInfo[1] ?? null) !== 1062) {
                    throw $ex;
                }
                $errores['dni'] = 'Ya hay un paciente con ese DNI.';
            }
        }
    }
    echo vista('formulario', ['id' => $id, 'd' => $d, 'errores' => $errores]);
    exit;
}

$q = trim($_GET['q'] ?? '');
// Sin emulación, cada parámetro con nombre se usa una sola vez: por eso :apellido y :dni.
$filtro = 'WHERE apellido LIKE :apellido OR dni LIKE :dni';
$contar = $pdo->prepare("SELECT COUNT(*) FROM paciente $filtro");
$contar->execute(['apellido' => "%$q%", 'dni' => "%$q%"]);
$total = (int) $contar->fetchColumn();
$paginas = max(1, (int) ceil($total / POR_PAGINA));
$pagina = min(max(1, (int) ($_GET['pagina'] ?? 1)), $paginas);
$s = $pdo->prepare("SELECT id, nombre, apellido, dni, obra_social, TIMESTAMPDIFF(YEAR, nacimiento, CURDATE()) AS edad FROM paciente $filtro ORDER BY apellido, nombre LIMIT :cantidad OFFSET :desde");
$s->bindValue('apellido', "%$q%");
$s->bindValue('dni', "%$q%");
$s->bindValue('cantidad', POR_PAGINA, PDO::PARAM_INT);
$s->bindValue('desde', ($pagina - 1) * POR_PAGINA, PDO::PARAM_INT);
$s->execute();
$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']);
echo vista('listado', ['pacientes' => $s->fetchAll(), 'q' => $q, 'total' => $total, 'pagina' => $pagina, 'paginas' => $paginas, 'flash' => $flash]);
```

### Prueba del sello

#### ¿Qué significa ABM?

Alta, baja y modificación (más el listado): las operaciones básicas sobre una tabla. En inglés, CRUD.

#### ¿Por qué el alta y la edición comparten formulario?

Porque piden los mismos datos con las mismas reglas: se escribe una vez el formulario y la validación, y solo cambia si se hace `INSERT` o `UPDATE`.

#### ¿Por qué una baja no puede ser un enlace (GET)?

Porque cualquier sitio o un robot que recorra enlaces podría borrar datos; las bajas van por POST con CSRF.

#### ¿Qué es una baja lógica?

Marcar un registro como dado de baja (una fecha o `activo = FALSE`) en lugar de borrarlo, para conservar la historia.

#### ¿Por qué se atrapa el error `1062` aunque ya se valide en PHP?

Porque dos personas pueden cargar el mismo dato al mismo tiempo: la validación de PHP pasa para las dos, pero la base rechaza la segunda.

### Soluciones (docente)

Nodo nuevo: el ABM completo con PDO, base de la rama 5 (MVC) y de la Senda de Laravel. `noEncontrado()` devuelve `never` (siempre corta), por eso se puede usar después de `??`: `buscar($id) ?? noEncontrado('…')`. Todos los proyectos se prueban con `php -S localhost:8000 -t public`, con el `esquema.sql` cargado antes.

## R04-N07 · Transacciones, índices y vistas

```meta
tipo: tema
padre: R04-N06
precio: 10
criatura: troll
```

### Crónica

Una tarde, el sistema del banco del Puerto se cortó a mitad de una transferencia: los sellos salieron de la cuenta de Kira… y nunca llegaron a la de Bron. Tres días tardaron en encontrar el error. Y mientras tanto, la bodega crecía tanto que buscar los movimientos de una cuenta tardaba lo que tarda el ferry en cruzar.

—Hay operaciones que son **todo o nada** —dice {mentor}—: o se hacen completas o no se hacen. Para eso están las **transacciones**. Y para encontrar rápido una ficha entre millones, la bodega necesita un **índice**, como el de un libro. Las dos cosas, {heroe}, separan a un sistema de juguete de uno de verdad.

### Objetivos

- Agrupar varias instrucciones en una transacción con `beginTransaction`, `commit` y `rollBack`.
- Deshacer todo si algo falla a mitad de camino.
- Evitar que dos pedidos simultáneos vendan el mismo stock (`SELECT … FOR UPDATE`).
- Crear índices y ver con `EXPLAIN` si una consulta los usa.
- Guardar consultas frecuentes como vistas (`CREATE VIEW`).

### Antes de empezar

- Consultas preparadas y ABM (R04-N05 y R04-N06), excepciones (R02-N09).

### Explicación

#### El problema del "a mitad de camino"
Transferir 500 sellos son **dos** `UPDATE`:
```sql
UPDATE cuenta SET saldo = saldo - 500 WHERE id = 1;   -- sale de Kira
UPDATE cuenta SET saldo = saldo + 500 WHERE id = 2;   -- entra a Bron
```
Si el programa falla entre los dos (un error, un corte de luz, una excepción), la
plata desaparece. Hace falta que los dos cuenten como **una sola operación**.

#### Transacciones
```php
try {
    $pdo->beginTransaction();
    $pdo->prepare('UPDATE cuenta SET saldo = saldo - ? WHERE id = ?')->execute([500, 1]);
    $pdo->prepare('UPDATE cuenta SET saldo = saldo + ? WHERE id = ?')->execute([500, 2]);
    $pdo->commit();           // confirma: los cambios quedan guardados
} catch (Throwable $e) {
    $pdo->rollBack();         // deshace TODO lo hecho desde beginTransaction
    throw $e;
}
```
- Mientras la transacción no se confirma, los demás no ven los cambios a medias.
- `rollBack` vuelve todo como estaba antes del `beginTransaction`.
- Funciona con tablas **InnoDB** (el motor por defecto de MariaDB y MySQL). Las
  instrucciones que cambian la estructura (`CREATE TABLE`, `ALTER`) confirman solas
  y no se pueden deshacer.

Para reglas del negocio ("no puede quedar saldo negativo"), se revisa **dentro** de
la transacción y, si no se cumple, se lanza una excepción que termina en
`rollBack`.

#### Dos compradores al mismo tiempo
Queda 1 poncho en stock y dos personas aprietan **Comprar** en el mismo segundo. Las
dos leen `stock = 1`, las dos venden. Para evitarlo, se **bloquea** la fila al leerla
dentro de la transacción:
```php
$pdo->beginTransaction();
$c = $pdo->prepare('SELECT stock FROM producto WHERE id = ? FOR UPDATE');   // bloquea esa fila
$c->execute([$id]);
$stock = (int) $c->fetchColumn();
if ($stock < $cantidad) {
    $pdo->rollBack();
    throw new DomainException('No hay stock suficiente');
}
$pdo->prepare('UPDATE producto SET stock = stock - ? WHERE id = ?')->execute([$cantidad, $id]);
$pdo->commit();
```
La segunda persona espera a que la primera termine, y cuando lee, ya ve `stock = 0`.

Otra forma, más corta: que el `UPDATE` incluya la condición y mirar `rowCount`:
```sql
UPDATE producto SET stock = stock - 1 WHERE id = ? AND stock >= 1
```
Si `rowCount()` da 0, no había stock.

#### Índices
Sin índice, para encontrar los movimientos de la cuenta 7 la base **recorre toda la
tabla**. Un **índice** es una lista ordenada aparte que le permite ir directo:
```sql
CREATE INDEX idx_movimiento_cuenta ON movimiento (cuenta_id);
CREATE INDEX idx_movimiento_cuenta_fecha ON movimiento (cuenta_id, fecha);   -- compuesto
```
- La clave primaria y las columnas `UNIQUE` ya tienen índice; las claves foráneas
  también (MariaDB lo crea solo).
- Conviene indexar las columnas que aparecen en `WHERE`, `JOIN` y `ORDER BY` de las
  consultas frecuentes.
- No se indexa todo: cada índice ocupa espacio y hace un poco más lentos los
  `INSERT` y `UPDATE`.

`EXPLAIN` muestra cómo va a ejecutar la base una consulta:
```sql
EXPLAIN SELECT * FROM movimiento WHERE cuenta_id = 7;
```
En la columna `type`, **`ALL`** significa "recorre toda la tabla" (malo con muchas
filas) y **`ref`** o **`const`** que usa un índice; la columna `key` dice cuál.

#### Vistas
Una **vista** es una consulta guardada con nombre, que se usa como si fuera una
tabla:
```sql
CREATE OR REPLACE VIEW saldo_por_cliente AS
SELECT c.nombre, SUM(m.monto) AS saldo
FROM cliente c JOIN movimiento m ON m.cliente_id = c.id
GROUP BY c.id, c.nombre;

SELECT * FROM saldo_por_cliente WHERE saldo < 0;
```
Sirven para no repetir consultas largas y para darle a alguien acceso solo a
ciertos datos.

### Código de ejemplo

`esquema.sql`
```sql
DROP VIEW IF EXISTS resumen_cuenta;
DROP TABLE IF EXISTS movimiento;
DROP TABLE IF EXISTS cuenta;
CREATE TABLE cuenta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titular VARCHAR(40) NOT NULL,
    saldo DECIMAL(12, 2) NOT NULL CHECK (saldo >= 0)
) ENGINE=InnoDB;
CREATE TABLE movimiento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cuenta_id INT NOT NULL,
    fecha DATE NOT NULL,
    monto DECIMAL(12, 2) NOT NULL,
    detalle VARCHAR(60) NOT NULL
) ENGINE=InnoDB;
INSERT INTO cuenta (titular, saldo) VALUES ('Kira', 1000), ('Bron', 250), ('Lía', 0);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`main.php`
```php
<?php
declare(strict_types=1);
/*
 * El banco del Puerto: transacciones todo-o-nada, un índice y una vista.
 */
$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

function transferir(PDO $pdo, int $desde, int $hacia, float $monto): void
{
    $pdo->beginTransaction();
    try {
        $saldo = $pdo->prepare('SELECT saldo FROM cuenta WHERE id = ? FOR UPDATE');
        $saldo->execute([$desde]);
        if ((float) $saldo->fetchColumn() < $monto) {
            throw new DomainException('Saldo insuficiente');
        }
        $mover = $pdo->prepare('UPDATE cuenta SET saldo = saldo + ? WHERE id = ?');
        $anotar = $pdo->prepare("INSERT INTO movimiento (cuenta_id, fecha, monto, detalle) VALUES (?, '2026-10-03', ?, ?)");
        $mover->execute([-$monto, $desde]);
        $anotar->execute([$desde, -$monto, "transferencia a $hacia"]);
        $mover->execute([$monto, $hacia]);
        if ($mover->rowCount() === 0) {
            throw new DomainException("No existe la cuenta $hacia");
        }
        $anotar->execute([$hacia, $monto, "transferencia de $desde"]);
        $pdo->commit();
    } catch (Throwable $e) {
        $pdo->rollBack();
        throw $e;
    }
}

function saldos(PDO $pdo): string
{
    return implode(' · ', array_map(fn($f) => "{$f['titular']} {$f['saldo']}", $pdo->query('SELECT titular, saldo FROM cuenta ORDER BY id')->fetchAll()));
}

echo "Al empezar: ", saldos($pdo), "\n";
foreach ([[1, 2, 300], [2, 3, 900], [1, 99, 100], [1, 3, 200]] as [$desde, $hacia, $monto]) {
    try {
        transferir($pdo, $desde, $hacia, $monto);
        echo "Transferencia de $monto: ok → ", saldos($pdo), "\n";
    } catch (DomainException $e) {
        echo "Transferencia de $monto: ", $e->getMessage(), " (se deshizo todo) → ", saldos($pdo), "\n";
    }
}
echo "Movimientos registrados: ", $pdo->query('SELECT COUNT(*) FROM movimiento')->fetchColumn(), "\n";

// Un índice: cargamos muchos movimientos y comparamos con EXPLAIN
$carga = $pdo->prepare("INSERT INTO movimiento (cuenta_id, fecha, monto, detalle) VALUES (?, '2026-09-01', 1, 'carga')");
$pdo->beginTransaction();
for ($i = 0; $i < 3000; $i++) {
    $carga->execute([$i % 50 + 1]);   // 50 cuentas: cada una tiene pocas filas
}
$pdo->commit();
$plan = fn() => $pdo->query('EXPLAIN SELECT * FROM movimiento WHERE cuenta_id = 2')->fetch();
$sin = $plan();
echo "Sin índice: type={$sin['type']}, key=", $sin['key'] ?? 'ninguno', "\n";
$pdo->exec('CREATE INDEX idx_movimiento_cuenta ON movimiento (cuenta_id)');
$pdo->query('ANALYZE TABLE movimiento')->fetchAll();   // devuelve filas: hay que leerlas
$con = $plan();
echo "Con índice: type={$con['type']}, key=", $con['key'] ?? 'ninguno', "\n";

// Una vista
$pdo->exec("CREATE OR REPLACE VIEW resumen_cuenta AS
    SELECT c.titular, COUNT(m.id) AS movimientos, COALESCE(SUM(m.monto), 0) AS neto
    FROM cuenta c LEFT JOIN movimiento m ON m.cuenta_id = c.id AND m.detalle <> 'carga'
    GROUP BY c.id, c.titular");
foreach ($pdo->query('SELECT * FROM resumen_cuenta ORDER BY titular') as $r) {
    echo "  {$r['titular']}: {$r['movimientos']} movimiento/s, neto {$r['neto']}\n";
}
```

### Salida esperada

```
Al empezar: Kira 1000.00 · Bron 250.00 · Lía 0.00
Transferencia de 300: ok → Kira 700.00 · Bron 550.00 · Lía 0.00
Transferencia de 900: Saldo insuficiente (se deshizo todo) → Kira 700.00 · Bron 550.00 · Lía 0.00
Transferencia de 100: No existe la cuenta 99 (se deshizo todo) → Kira 700.00 · Bron 550.00 · Lía 0.00
Transferencia de 200: ok → Kira 500.00 · Bron 550.00 · Lía 200.00
Movimientos registrados: 4
Sin índice: type=ALL, key=ninguno
Con índice: type=ref, key=idx_movimiento_cuenta
  Bron: 1 movimiento/s, neto 300.00
  Kira: 2 movimiento/s, neto -500.00
  Lía: 1 movimiento/s, neto 200.00
```

### ¿Para qué sirve?

Toda operación de plata o de stock va en una transacción: una venta que descuenta stock y registra el pago, una inscripción que ocupa un cupo y cobra, una transferencia. Sin ellas, un error a mitad de camino deja los datos inconsistentes. Y los índices son la diferencia entre una página que responde en 10 milisegundos y otra que tarda 10 segundos cuando la tabla llega al millón de filas.

### Errores habituales

**Troll: `commit` sin `rollBack`.** Si hay una excepción entre `beginTransaction` y
`commit` y no la atrapás para hacer `rollBack`, la transacción queda abierta y los
cambios se pierden (o bloquean filas) hasta que se cierra la conexión.

**Ogro: revisar el stock afuera de la transacción.** Leer el stock, decidir, y
después abrir la transacción para descontar deja la ventana para que dos personas
vendan lo mismo. La lectura con `FOR UPDATE` va **adentro**.

**Goblin: tablas MyISAM.** En tablas con motor `MyISAM`, las transacciones no hacen
nada (no hay `rollBack`). Usá `InnoDB` (el motor por defecto).

**Ogro: indexar todo.** Cada índice hace más lentas las escrituras y ocupa espacio.
Se indexa lo que se consulta seguido.

**Troll: el resultado que quedó sin leer.** `SQLSTATE[HY000]: General error: 2014
Cannot execute queries while other unbuffered queries are active` aparece cuando una
instrucción devuelve filas y nadie las leyó (por ejemplo, `exec('ANALYZE TABLE …')`,
que devuelve un resumen). Usá `query(…)->fetchAll()` para las que devuelven filas.

**Esqueleto: el índice que no se usa.** `WHERE YEAR(fecha) = 2026` no usa el índice de
`fecha` (la base tiene que calcular `YEAR` en cada fila). Escribilo como rango:
`WHERE fecha >= '2026-01-01' AND fecha < '2027-01-01'`.

### Misión R04-N07-M1 · La venta que se deshace

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Una venta de la ferretería es: crear el **pedido**, cargar cada **renglón** y
**descontar el stock** de cada producto. Escribí `vender(PDO $pdo, string $cliente,
array $items): int` (`$items` es `codigo => cantidad`) que haga todo en **una
transacción**:

- para cada producto, lee el precio y el stock con `FOR UPDATE`; si no existe o no
  alcanza el stock, lanza `DomainException` con el motivo;
- guarda el renglón con el precio del momento y descuenta el stock;
- devuelve el número de pedido (`lastInsertId`).

Si algo falla, no tiene que quedar **nada**: ni el pedido, ni renglones, ni stock
descontado. Probá una venta que sale bien y otra cuyo tercer producto no tiene
stock, y mostrá el stock y la cantidad de pedidos después de cada una.

#### Criterio de aprobación

- Todo va en una transacción con `rollBack` ante cualquier error.
- El stock se lee con `FOR UPDATE`.
- La salida coincide con la esperada.

#### Salida esperada

```
Venta a Ana: pedido 1
  stock: CLA010=25, LIJ120=2, MAR001=3 · pedidos: 1
Venta a Beto: No hay 5 de Lija 120 (quedan 2). No se guardó nada.
  stock: CLA010=25, LIJ120=2, MAR001=3 · pedidos: 1
```

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS renglon;
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (codigo CHAR(6) PRIMARY KEY, nombre VARCHAR(40) NOT NULL, precio DECIMAL(10, 2) NOT NULL, stock INT NOT NULL CHECK (stock >= 0));
CREATE TABLE pedido (id INT AUTO_INCREMENT PRIMARY KEY, cliente VARCHAR(40) NOT NULL);
CREATE TABLE renglon (
    pedido_id INT NOT NULL,
    codigo CHAR(6) NOT NULL,
    cantidad INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (pedido_id, codigo),
    FOREIGN KEY (pedido_id) REFERENCES pedido(id),
    FOREIGN KEY (codigo) REFERENCES producto(codigo)
);
INSERT INTO producto VALUES ('MAR001', 'Martillo', 12500, 5), ('CLA010', 'Clavos x100', 2300, 30), ('LIJ120', 'Lija 120', 800, 2);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`main.php`
```php
<?php
declare(strict_types=1);
// Mision 1 - La venta que se deshace: una transacción de varios pasos.
$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);

function vender(PDO $pdo, string $cliente, array $items): int
{
    $pdo->beginTransaction();
    try {
        $pdo->prepare('INSERT INTO pedido (cliente) VALUES (?)')->execute([$cliente]);
        $pedido = (int) $pdo->lastInsertId();
        $leer = $pdo->prepare('SELECT nombre, precio, stock FROM producto WHERE codigo = ? FOR UPDATE');
        $renglon = $pdo->prepare('INSERT INTO renglon (pedido_id, codigo, cantidad, precio) VALUES (?, ?, ?, ?)');
        $descontar = $pdo->prepare('UPDATE producto SET stock = stock - ? WHERE codigo = ?');
        foreach ($items as $codigo => $cantidad) {
            $leer->execute([$codigo]);
            $p = $leer->fetch();
            if ($p === false) {
                throw new DomainException("No existe el producto $codigo");
            }
            if ($p['stock'] < $cantidad) {
                throw new DomainException("No hay $cantidad de {$p['nombre']} (quedan {$p['stock']})");
            }
            $renglon->execute([$pedido, $codigo, $cantidad, $p['precio']]);
            $descontar->execute([$cantidad, $codigo]);
        }
        $pdo->commit();
        return $pedido;
    } catch (Throwable $e) {
        $pdo->rollBack();
        throw $e;
    }
}

function estado(PDO $pdo): string
{
    $stock = implode(', ', array_map(fn($p) => "{$p['codigo']}={$p['stock']}", $pdo->query('SELECT codigo, stock FROM producto ORDER BY codigo')->fetchAll()));
    return "stock: $stock · pedidos: " . $pdo->query('SELECT COUNT(*) FROM pedido')->fetchColumn();
}

foreach ([['Ana', ['MAR001' => 2, 'CLA010' => 5]], ['Beto', ['MAR001' => 1, 'CLA010' => 3, 'LIJ120' => 5]]] as [$cliente, $items]) {
    try {
        $numero = vender($pdo, $cliente, $items);
        echo "Venta a $cliente: pedido $numero\n";
    } catch (DomainException $e) {
        echo "Venta a $cliente: ", $e->getMessage(), ". No se guardó nada.\n";
    }
    echo "  ", estado($pdo), "\n";
}
```

### Misión R04-N07-M2 · El cupo que no se pasa

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Los talleres del club tienen **cupo**. Inscribir a alguien tiene que ocupar un lugar
sin pasarse nunca, aunque muchos se anoten a la vez. Escribí `inscribir(PDO $pdo,
int $taller, string $socio): bool` **sin** leer primero el cupo: con un solo
`UPDATE taller SET ocupados = ocupados + 1 WHERE id = ? AND ocupados < cupo` y
`rowCount()` para saber si había lugar; si había, en la misma transacción inserta la
inscripción (un mismo socio no puede anotarse dos veces: `UNIQUE`, y si pasa, se
deshace el lugar ocupado). Intentá anotar a 5 socios (uno repetido) en un taller de
cupo 3 y mostrá el resultado de cada intento y el estado final.

#### Criterio de aprobación

- El control de cupo está en el `UPDATE` con condición y `rowCount`.
- Un duplicado deshace el lugar ocupado (`rollBack`).
- La salida coincide con la esperada.

#### Salida esperada

```
Ana: inscripto
Beto: inscripto
Ana: ya estaba inscripto
Carla: inscripto
Diego: sin cupo
Nudos marineros: 3/3 · inscriptos: Ana, Beto, Carla
```

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS inscripcion;
DROP TABLE IF EXISTS taller;
CREATE TABLE taller (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(40) NOT NULL, cupo INT NOT NULL, ocupados INT NOT NULL DEFAULT 0);
CREATE TABLE inscripcion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    taller_id INT NOT NULL,
    socio VARCHAR(40) NOT NULL,
    UNIQUE (taller_id, socio),
    FOREIGN KEY (taller_id) REFERENCES taller(id)
);
INSERT INTO taller (nombre, cupo) VALUES ('Nudos marineros', 3);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`main.php`
```php
<?php
declare(strict_types=1);
// Mision 2 - El cupo que no se pasa: UPDATE con condición, rowCount y transacción.
$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);

function inscribir(PDO $pdo, int $taller, string $socio): string
{
    $pdo->beginTransaction();
    try {
        $ocupar = $pdo->prepare('UPDATE taller SET ocupados = ocupados + 1 WHERE id = ? AND ocupados < cupo');
        $ocupar->execute([$taller]);
        if ($ocupar->rowCount() === 0) {
            $pdo->rollBack();
            return 'sin cupo';
        }
        $pdo->prepare('INSERT INTO inscripcion (taller_id, socio) VALUES (?, ?)')->execute([$taller, $socio]);
        $pdo->commit();
        return 'inscripto';
    } catch (PDOException $e) {
        $pdo->rollBack();
        if (($e->errorInfo[1] ?? null) === 1062) {
            return 'ya estaba inscripto';
        }
        throw $e;
    }
}

foreach (['Ana', 'Beto', 'Ana', 'Carla', 'Diego'] as $socio) {
    echo "$socio: ", inscribir($pdo, 1, $socio), "\n";
}
$t = $pdo->query('SELECT nombre, cupo, ocupados FROM taller WHERE id = 1')->fetch();
echo "{$t['nombre']}: {$t['ocupados']}/{$t['cupo']} · inscriptos: ", implode(', ', $pdo->query('SELECT socio FROM inscripcion ORDER BY id')->fetchAll(PDO::FETCH_COLUMN)), "\n";
```

### Misión R04-N07-M3 · El reporte veloz

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Una cadena de farmacias tiene una tabla `venta` enorme. Escribí `optimizar.php` que:

1. cargue 5000 ventas de prueba (sucursal 1 a 10, fecha a lo largo de 2026 y un
   total), en **una** transacción con un `prepare` reutilizado;
2. muestre con `EXPLAIN` (solo `type` y `key`) cómo se ejecuta
   `SELECT SUM(total) FROM venta WHERE sucursal = 4 AND fecha >= '2026-06-01' AND fecha < '2026-07-01'`;
3. cree un índice **compuesto** por sucursal y fecha, y vuelva a mostrar el `EXPLAIN`;
4. cree la vista `ventas_mensuales` (sucursal, mes con `DATE_FORMAT(fecha, '%Y-%m')`,
   cantidad y total) y muestre de ella las 3 filas de la sucursal 4 con más
   ventas de junio a agosto.

Los datos de prueba se generan con `mt_srand(42)` y `mt_rand` para que salgan
siempre iguales.

#### Criterio de aprobación

- La carga masiva va en una transacción.
- El `EXPLAIN` cambia de `ALL` a usar el índice compuesto.
- La vista resume por sucursal y mes.
- La salida coincide con la esperada.

#### Salida esperada

```
Ventas cargadas: 5000
Antes: type=ALL, key=ninguno
Después: type=range, key=idx_venta_sucursal_fecha
Junio, sucursal 4: $17.226,26
  2026-08: 48 ventas, $24181.70
  2026-06: 43 ventas, $17226.26
  2026-07: 27 ventas, $11291.44
```

#### Solución de referencia

`esquema.sql`
```sql
DROP VIEW IF EXISTS ventas_mensuales;
DROP TABLE IF EXISTS venta;
CREATE TABLE venta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    total DECIMAL(10, 2) NOT NULL
) ENGINE=InnoDB;
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`optimizar.php`
```php
<?php
declare(strict_types=1);
// Mision 3 - El reporte veloz: carga en una transacción, índice compuesto y una vista.
$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);

mt_srand(42);
$alta = $pdo->prepare('INSERT INTO venta (sucursal, fecha, total) VALUES (?, ?, ?)');
$inicio = new DateTimeImmutable('2026-01-01');
$pdo->beginTransaction();
for ($i = 0; $i < 5000; $i++) {
    $alta->execute([mt_rand(1, 10), $inicio->modify('+' . mt_rand(0, 364) . ' days')->format('Y-m-d'), mt_rand(1000, 90000) / 100]);
}
$pdo->commit();
echo "Ventas cargadas: ", $pdo->query('SELECT COUNT(*) FROM venta')->fetchColumn(), "\n";

$consulta = "SELECT SUM(total) FROM venta WHERE sucursal = 4 AND fecha >= '2026-06-01' AND fecha < '2026-07-01'";
$plan = function () use ($pdo, $consulta): string {
    $p = $pdo->query("EXPLAIN $consulta")->fetch();
    return "type={$p['type']}, key=" . ($p['key'] ?? 'ninguno');
};
echo "Antes: ", $plan(), "\n";
$pdo->exec('CREATE INDEX idx_venta_sucursal_fecha ON venta (sucursal, fecha)');
$pdo->query('ANALYZE TABLE venta')->fetchAll();
echo "Después: ", $plan(), "\n";
echo "Junio, sucursal 4: $", number_format((float) $pdo->query($consulta)->fetchColumn(), 2, ',', '.'), "\n";

$pdo->exec("CREATE OR REPLACE VIEW ventas_mensuales AS
    SELECT sucursal, DATE_FORMAT(fecha, '%Y-%m') AS mes, COUNT(*) AS ventas, SUM(total) AS total
    FROM venta GROUP BY sucursal, DATE_FORMAT(fecha, '%Y-%m')");
$top = $pdo->prepare("SELECT mes, ventas, total FROM ventas_mensuales WHERE sucursal = ? AND mes BETWEEN '2026-06' AND '2026-08' ORDER BY ventas DESC, mes LIMIT 3");
$top->execute([4]);
foreach ($top as $f) {
    echo "  {$f['mes']}: {$f['ventas']} ventas, \${$f['total']}\n";
}
```

### Encargo R04-N07-E1 · El cierre de caja

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Un almacén hace el **cierre de caja** cada noche: pasa todas las ventas del día
que están `abiertas` a un **cierre** (tabla `cierre`: fecha, cantidad de ventas,
total, efectivo y tarjeta), marca esas ventas como `cerradas` con el número de
cierre, y no puede quedar a medias. Escribí `cerrarCaja(PDO $pdo, string $fecha):
array` que, en una transacción:

- no deja cerrar dos veces el mismo día: lo pregunta antes y, por si dos personas
  cierran a la vez, la fecha del cierre es `UNIQUE` (atrapá el `1062`);
- no cierra si no hay ventas abiertas ese día (`DomainException`);
- calcula los totales con **una** consulta `SUM(… )` agrupada por medio;
- inserta el cierre, actualiza las ventas con `UPDATE … WHERE fecha = ? AND estado =
  'abierta'` y verifica con `rowCount()` que se cerraron tantas como se sumaron.

Probá cerrar el 3/10 (sale bien), el 3/10 otra vez (ya cerrado) y el 4/10 (sin
ventas), y mostrá el resultado de cada uno.

#### Criterio de aprobación

- Todo en una transacción con `rollBack`.
- Los totales se calculan en SQL.
- La salida coincide con la esperada.

#### Salida esperada

```
Cierre 2026-10-03: n.º 1, 4 ventas, total 23890.00 (efectivo 5090.00, tarjeta 18800.00)
Cierre 2026-10-03: ese día ya estaba cerrado
Cierre 2026-10-04: no hay ventas abiertas ese día
Ventas abiertas: 1
```

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS venta;
DROP TABLE IF EXISTS cierre;
CREATE TABLE cierre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL UNIQUE,
    ventas INT NOT NULL,
    total DECIMAL(12, 2) NOT NULL,
    efectivo DECIMAL(12, 2) NOT NULL,
    tarjeta DECIMAL(12, 2) NOT NULL
);
CREATE TABLE venta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    medio ENUM('efectivo', 'tarjeta') NOT NULL,
    estado ENUM('abierta', 'cerrada') NOT NULL DEFAULT 'abierta',
    cierre_id INT NULL,
    FOREIGN KEY (cierre_id) REFERENCES cierre(id)
);
INSERT INTO venta (fecha, total, medio) VALUES
    ('2026-10-03', 4200, 'efectivo'), ('2026-10-03', 12500, 'tarjeta'), ('2026-10-03', 890, 'efectivo'),
    ('2026-10-03', 6300, 'tarjeta'), ('2026-10-02', 1500, 'efectivo');
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`main.php`
```php
<?php
declare(strict_types=1);
// Encargo - El cierre de caja: totales en SQL y todo en una transacción.
$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);

function cerrarCaja(PDO $pdo, string $fecha): array
{
    $pdo->beginTransaction();
    try {
        $ya = $pdo->prepare('SELECT COUNT(*) FROM cierre WHERE fecha = ?');
        $ya->execute([$fecha]);
        if ((int) $ya->fetchColumn() > 0) {
            throw new DomainException('ese día ya estaba cerrado');
        }
        $s = $pdo->prepare("SELECT COUNT(*) AS ventas, COALESCE(SUM(total), 0) AS total,
            COALESCE(SUM(CASE WHEN medio = 'efectivo' THEN total END), 0) AS efectivo,
            COALESCE(SUM(CASE WHEN medio = 'tarjeta' THEN total END), 0) AS tarjeta
            FROM venta WHERE fecha = ? AND estado = 'abierta' FOR UPDATE");
        $s->execute([$fecha]);
        $t = $s->fetch();
        if ((int) $t['ventas'] === 0) {
            throw new DomainException('no hay ventas abiertas ese día');
        }
        $pdo->prepare('INSERT INTO cierre (fecha, ventas, total, efectivo, tarjeta) VALUES (?, ?, ?, ?, ?)')
            ->execute([$fecha, $t['ventas'], $t['total'], $t['efectivo'], $t['tarjeta']]);
        $cierre = (int) $pdo->lastInsertId();
        $u = $pdo->prepare("UPDATE venta SET estado = 'cerrada', cierre_id = ? WHERE fecha = ? AND estado = 'abierta'");
        $u->execute([$cierre, $fecha]);
        if ($u->rowCount() !== (int) $t['ventas']) {
            throw new RuntimeException('Las ventas cambiaron durante el cierre');
        }
        $pdo->commit();
        return ['cierre' => $cierre] + $t;
    } catch (PDOException $e) {
        $pdo->rollBack();
        if (($e->errorInfo[1] ?? null) === 1062) {
            throw new DomainException('ese día ya estaba cerrado');
        }
        throw $e;
    } catch (Throwable $e) {
        $pdo->rollBack();
        throw $e;
    }
}

foreach (['2026-10-03', '2026-10-03', '2026-10-04'] as $fecha) {
    try {
        $r = cerrarCaja($pdo, $fecha);
        echo "Cierre $fecha: n.º {$r['cierre']}, {$r['ventas']} ventas, total {$r['total']} (efectivo {$r['efectivo']}, tarjeta {$r['tarjeta']})\n";
    } catch (DomainException $e) {
        echo "Cierre $fecha: ", $e->getMessage(), "\n";
    }
}
echo "Ventas abiertas: ", $pdo->query("SELECT COUNT(*) FROM venta WHERE estado = 'abierta'")->fetchColumn(), "\n";
```

### Prueba del sello

#### ¿Qué garantiza una transacción?

Que un grupo de instrucciones se haga completo o no se haga nada: si algo falla, `rollBack` deshace todo lo hecho desde `beginTransaction`.

#### ¿Para qué sirve `SELECT … FOR UPDATE`?

Para bloquear las filas leídas dentro de una transacción, así otro pedido simultáneo espera y no decide con datos viejos (por ejemplo, vender el mismo stock).

#### ¿Qué es un índice y cuándo conviene crearlo?

Una estructura ordenada que le permite a la base ir directo a las filas; conviene en las columnas que se usan seguido en `WHERE`, `JOIN` y `ORDER BY`.

#### ¿Qué indica `type = ALL` en un `EXPLAIN`?

Que la base va a recorrer toda la tabla (no usa ningún índice).

#### ¿Qué es una vista?

Una consulta guardada con nombre que se usa como si fuera una tabla.

### Soluciones (docente)

Nodo nuevo. Las transacciones requieren InnoDB (motor por defecto). En la misión 3, la cantidad de filas del `EXPLAIN` es una estimación y puede variar, por eso se muestran solo `type` y `key`. El ejemplo carga 3000 filas repartidas en 50 cuentas para que el `EXPLAIN` tenga sentido: si una consulta trae una gran parte de la tabla (o la tabla es chica), la base puede preferir recorrerla entera aunque haya índice.

## R04-N08 · Repositorios y login con base

```meta
tipo: tema
padre: R04-N07
precio: 10
criatura: skeleton
```

### Crónica

La Bodega ya tiene cientos de consultas desparramadas: una en la página de pedidos, otra parecida en el reporte, otra casi igual en el panel del gerente. Cuando cambió el nombre de una columna, hubo que buscarla en cuarenta archivos. {mentor} junta a los bodegueros y designa uno por estantería: *"de ahora en más, las fichas de barcos las pide solo Ramiro"*.

—Cada tabla tiene su **encargado**: un **repositorio** —dice—. El resto del sistema no escribe SQL: le pide al repositorio "dame los barcos activos" o "guardá este barco". Así el SQL vive en un solo lugar, {heroe}, y si mañana cambiás de base, cambiás solo los encargados.

### Objetivos

- Separar el acceso a datos en clases repositorio con métodos del dominio.
- Convertir filas en objetos (entidades) y objetos en filas.
- Definir una interfaz de repositorio y cambiar de implementación (memoria o PDO).
- Llevar el login a la base: tabla de usuarios, `password_hash`, roles y actualización del hash.
- Recibir la conexión por el constructor (inyección de dependencias).

### Antes de empezar

- Interfaces y composición (R02-N06 y R02-N07), login con sesiones (R03-N06), consultas preparadas (R04-N05).

### Explicación

#### El problema del SQL desparramado
Si cada página escribe su propio `SELECT`, el mismo SQL está repetido, un cambio en
la tabla obliga a revisar todo, y no se puede probar la lógica sin una base. El
**patrón repositorio** junta todo el acceso a una tabla en una clase:
```php
class BarcoRepositorio
{
    public function __construct(private PDO $pdo) {}

    public function buscar(int $id): ?Barco { … }
    public function activos(): array { … }          // Barco[]
    public function guardar(Barco $barco): Barco { … }
    public function borrar(int $id): void { … }
}
```
Las páginas y los servicios hablan con el repositorio en términos del problema
(`activos()`), no de SQL.

#### Entidades: de fila a objeto
El repositorio devuelve **objetos**, no arrays sueltos:
```php
readonly class Barco
{
    public function __construct(
        public ?int $id,
        public string $nombre,
        public float $capacidad,
    ) {}

    public static function desdeFila(array $f): self
    {
        return new self((int) $f['id'], $f['nombre'], (float) $f['capacidad']);
    }
}
```
Así los tipos quedan claros (`capacidad` es `float`, no el texto `"450.00"`) y la
validación vive en el objeto.

#### Guardar: alta o modificación
```php
public function guardar(Barco $b): Barco
{
    if ($b->id === null) {
        $this->pdo->prepare('INSERT INTO barco (nombre, capacidad) VALUES (?, ?)')->execute([$b->nombre, $b->capacidad]);
        return new Barco((int) $this->pdo->lastInsertId(), $b->nombre, $b->capacidad);
    }
    $this->pdo->prepare('UPDATE barco SET nombre = ?, capacidad = ? WHERE id = ?')->execute([$b->nombre, $b->capacidad, $b->id]);
    return $b;
}
```

#### Una interfaz, dos implementaciones
Con una interfaz `BarcoRepositorio` y dos clases (`BarcoRepositorioPdo` y
`BarcoRepositorioEnMemoria`), el resto del sistema no sabe dónde se guardan los
barcos. La de memoria sirve para **probar** la lógica sin base (lo vas a usar con
PHPUnit en la rama 5).

#### El login, con base
```sql
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    nombre VARCHAR(60) NOT NULL,
    rol ENUM('admin', 'operador', 'cliente') NOT NULL DEFAULT 'cliente',
    hash VARCHAR(255) NOT NULL,
    ultimo_acceso DATETIME NULL
);
```
```php
public function autenticar(string $email, string $clave): ?Usuario
{
    $s = $this->pdo->prepare('SELECT * FROM usuario WHERE email = ?');
    $s->execute([mb_strtolower(trim($email))]);
    $fila = $s->fetch();
    if ($fila === false || !password_verify($clave, $fila['hash'])) {
        return null;
    }
    if (password_needs_rehash($fila['hash'], PASSWORD_DEFAULT)) {       // si cambió el algoritmo
        $this->pdo->prepare('UPDATE usuario SET hash = ? WHERE id = ?')->execute([password_hash($clave, PASSWORD_DEFAULT), $fila['id']]);
    }
    $this->pdo->prepare('UPDATE usuario SET ultimo_acceso = NOW() WHERE id = ?')->execute([$fila['id']]);
    return Usuario::desdeFila($fila);
}
```
- `password_needs_rehash` actualiza el hash cuando PHP cambia el algoritmo o el costo
  por defecto: las contraseñas se van renovando solas al entrar.
- En la sesión se guarda **solo el id** del usuario (`$_SESSION['usuario_id']`); en
  cada pedido se lo busca con el repositorio, así un usuario borrado o con el rol
  cambiado pierde el acceso enseguida.

### Código de ejemplo

`esquema.sql`
```sql
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS barco;
CREATE TABLE barco (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL UNIQUE,
    capacidad DECIMAL(8, 2) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    nombre VARCHAR(60) NOT NULL,
    rol ENUM('admin', 'operador') NOT NULL DEFAULT 'operador',
    hash VARCHAR(255) NOT NULL,
    ultimo_acceso DATETIME NULL
);
INSERT INTO barco (nombre, capacidad, activo) VALUES ('Gaviota', 450, TRUE), ('Albatros', 1200, TRUE), ('Tortuga', 80, FALSE);
INSERT INTO usuario (email, nombre, rol, hash) VALUES
    ('kira@puerto.ar', 'Kira Valdez', 'admin', '$2y$10$R7flf57cYzLAnMr14xX56OhKUJ5qlAco9VY/EbWmghiXoQB.vb5yS'),
    ('bron@puerto.ar', 'Bron', 'operador', '$2y$04$x03MQT0AP9sjJnPQcmEn9.dktCp3kwxYSS3vulCFizcGrg5YaNTce');
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`src/Barco.php`
```php
<?php
declare(strict_types=1);

readonly class Barco
{
    public function __construct(public ?int $id, public string $nombre, public float $capacidad, public bool $activo = true)
    {
        if (trim($nombre) === '' || $capacidad <= 0) {
            throw new InvalidArgumentException('Barco inválido');
        }
    }

    public static function desdeFila(array $f): self
    {
        return new self((int) $f['id'], $f['nombre'], (float) $f['capacidad'], (bool) $f['activo']);
    }
}
```

`src/BarcoRepositorio.php`
```php
<?php
declare(strict_types=1);

interface BarcoRepositorio
{
    public function buscar(int $id): ?Barco;

    /** @return Barco[] */
    public function activos(): array;

    public function guardar(Barco $barco): Barco;
}
```

`src/BarcoRepositorioPdo.php`
```php
<?php
declare(strict_types=1);

class BarcoRepositorioPdo implements BarcoRepositorio
{
    public function __construct(private PDO $pdo) {}

    public function buscar(int $id): ?Barco
    {
        $s = $this->pdo->prepare('SELECT * FROM barco WHERE id = ?');
        $s->execute([$id]);
        $f = $s->fetch();
        return $f === false ? null : Barco::desdeFila($f);
    }

    public function activos(): array
    {
        return array_map([Barco::class, 'desdeFila'], $this->pdo->query('SELECT * FROM barco WHERE activo = TRUE ORDER BY nombre')->fetchAll());
    }

    public function guardar(Barco $b): Barco
    {
        if ($b->id === null) {
            $this->pdo->prepare('INSERT INTO barco (nombre, capacidad, activo) VALUES (?, ?, ?)')->execute([$b->nombre, $b->capacidad, (int) $b->activo]);
            return new Barco((int) $this->pdo->lastInsertId(), $b->nombre, $b->capacidad, $b->activo);
        }
        $this->pdo->prepare('UPDATE barco SET nombre = ?, capacidad = ?, activo = ? WHERE id = ?')->execute([$b->nombre, $b->capacidad, (int) $b->activo, $b->id]);
        return $b;
    }
}
```

`src/UsuarioRepositorio.php`
```php
<?php
declare(strict_types=1);

readonly class Usuario
{
    public function __construct(public int $id, public string $email, public string $nombre, public string $rol) {}
}

class UsuarioRepositorio
{
    public function __construct(private PDO $pdo) {}

    public function autenticar(string $email, string $clave): ?Usuario
    {
        $s = $this->pdo->prepare('SELECT * FROM usuario WHERE email = ?');
        $s->execute([mb_strtolower(trim($email))]);
        $f = $s->fetch();
        if ($f === false || !password_verify($clave, $f['hash'])) {
            return null;
        }
        if (password_needs_rehash($f['hash'], PASSWORD_DEFAULT)) {
            $this->pdo->prepare('UPDATE usuario SET hash = ? WHERE id = ?')->execute([password_hash($clave, PASSWORD_DEFAULT), $f['id']]);
        }
        $this->pdo->prepare('UPDATE usuario SET ultimo_acceso = NOW() WHERE id = ?')->execute([$f['id']]);
        return new Usuario((int) $f['id'], $f['email'], $f['nombre'], $f['rol']);
    }

    public function costoDelHash(string $email): int
    {
        $s = $this->pdo->prepare('SELECT hash FROM usuario WHERE email = ?');
        $s->execute([$email]);
        return password_get_info((string) $s->fetchColumn())['options']['cost'] ?? 0;
    }
}
```

`main.php`
```php
<?php
declare(strict_types=1);
/*
 * Los encargados de la Bodega: repositorios, entidades y login contra la base.
 */
foreach (glob(__DIR__ . '/src/*.php') as $archivo) {
    require_once $archivo;
}
$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);

$barcos = new BarcoRepositorioPdo($pdo);
echo "Activos: ", implode(', ', array_map(fn(Barco $b) => "{$b->nombre} ({$b->capacidad} kg)", $barcos->activos())), "\n";
$nuevo = $barcos->guardar(new Barco(null, 'Delfín', 300));
echo "Guardado con id {$nuevo->id}\n";
$tortuga = $barcos->buscar(3);
$barcos->guardar(new Barco($tortuga->id, $tortuga->nombre, $tortuga->capacidad, true));
echo "Activos ahora: ", count($barcos->activos()), "\n";
var_dump($barcos->buscar(99));

$usuarios = new UsuarioRepositorio($pdo);
foreach ([['KIRA@puerto.ar', 'ancla123'], ['kira@puerto.ar', 'mal'], ['bron@puerto.ar', 'faro2026']] as [$email, $clave]) {
    $u = $usuarios->autenticar($email, $clave);
    echo "$email: ", $u === null ? 'rechazado' : "entra {$u->nombre} ({$u->rol})", "\n";
}
echo "Costo del hash de Bron después de entrar: ", $usuarios->costoDelHash('bron@puerto.ar'), "\n";
```

### Salida esperada

```
Activos: Albatros (1200 kg), Gaviota (450 kg)
Guardado con id 4
Activos ahora: 4
NULL
KIRA@puerto.ar: entra Kira Valdez (admin)
kira@puerto.ar: rechazado
bron@puerto.ar: entra Bron (operador)
Costo del hash de Bron después de entrar: 10
```

### ¿Para qué sirve?

Separar el acceso a datos es lo que permite que un sistema crezca: las páginas quedan cortas y legibles, el SQL está en un solo lugar y la lógica se puede probar sin base. Es lo que hace Laravel con sus modelos Eloquent (`Barco::where('activo', true)->get()`) y lo que vas a usar en el jefe de esta rama y en el MVC de la siguiente.

### Errores habituales

**Esqueleto: el repositorio que devuelve arrays con claves de la tabla.** Si las
páginas usan `$fila['capacidad']`, un cambio de nombre en la tabla las rompe igual.
Devolvé objetos.

**Troll: `new PDO` adentro del repositorio.** Cada repositorio abriría su propia
conexión y no se podría probar. Recibí el `PDO` por el constructor.

**Troll: guardar el usuario entero en la sesión.** Si el admin le quita el rol a
alguien, la sesión sigue diciendo que es admin. Guardá el id y buscalo en cada
pedido.

**Goblin: los tipos de la fila.** `(float) $f['capacidad']`: los `DECIMAL` llegan como
texto; convertilos al armar la entidad.

**Ogro: métodos que exponen SQL.** `repositorio->consultar("SELECT …")` es SQL
desparramado con otro nombre. Los métodos dicen **qué** se busca: `activos()`,
`porCapitan($id)`.

### Misión R04-N08-M1 · El repositorio de socios

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Escribí la entidad `readonly` `Socio` (id, nombre, DNI, categoría y fecha de alta
como `DateTimeImmutable`) con `desdeFila`, y un `SocioRepositorio` con PDO que tenga:

- `buscarPorDni(string $dni): ?Socio`;
- `porCategoria(string $categoria): array` ordenados por nombre;
- `guardar(Socio $s): Socio` (alta o modificación);
- `cantidadPorCategoria(): array` (`categoria => cantidad`, con `FETCH_KEY_PAIR`).

`main.php` usa el repositorio para dar de alta un socio, cambiarle la categoría,
buscar uno que no existe y mostrar los resúmenes. No hay SQL fuera del repositorio.

#### Criterio de aprobación

- El SQL está solo en el repositorio y devuelve objetos `Socio`.
- El `PDO` se recibe por el constructor.
- La salida coincide con la esperada.

#### Salida esperada

```
Alta: Diego Ruiz con id 4
Beto pasó a: activo
DNI 99999999: no existe
Activos: Ana Pérez (desde 2020), Beto Díaz (desde 2024)
  activo: 2
  cadete: 1
  vitalicio: 1
```

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS socio;
CREATE TABLE socio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    dni CHAR(8) NOT NULL UNIQUE,
    categoria ENUM('activo', 'cadete', 'vitalicio') NOT NULL,
    alta DATE NOT NULL
);
INSERT INTO socio (nombre, dni, categoria, alta) VALUES
    ('Ana Pérez', '30111222', 'activo', '2020-03-01'), ('Beto Díaz', '31222333', 'cadete', '2024-05-10'), ('Carla Gómez', '25333444', 'vitalicio', '1998-08-15');
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`src/Socio.php`
```php
<?php
declare(strict_types=1);

readonly class Socio
{
    public function __construct(public ?int $id, public string $nombre, public string $dni, public string $categoria, public DateTimeImmutable $alta) {}

    public static function desdeFila(array $f): self
    {
        return new self((int) $f['id'], $f['nombre'], $f['dni'], $f['categoria'], new DateTimeImmutable($f['alta']));
    }

    public function conCategoria(string $categoria): self
    {
        return new self($this->id, $this->nombre, $this->dni, $categoria, $this->alta);
    }
}
```

`src/SocioRepositorio.php`
```php
<?php
declare(strict_types=1);

class SocioRepositorio
{
    public function __construct(private PDO $pdo) {}

    public function buscarPorDni(string $dni): ?Socio
    {
        $s = $this->pdo->prepare('SELECT * FROM socio WHERE dni = ?');
        $s->execute([$dni]);
        $f = $s->fetch();
        return $f === false ? null : Socio::desdeFila($f);
    }

    /** @return Socio[] */
    public function porCategoria(string $categoria): array
    {
        $s = $this->pdo->prepare('SELECT * FROM socio WHERE categoria = ? ORDER BY nombre');
        $s->execute([$categoria]);
        return array_map([Socio::class, 'desdeFila'], $s->fetchAll());
    }

    public function guardar(Socio $s): Socio
    {
        $valores = [$s->nombre, $s->dni, $s->categoria, $s->alta->format('Y-m-d')];
        if ($s->id === null) {
            $this->pdo->prepare('INSERT INTO socio (nombre, dni, categoria, alta) VALUES (?, ?, ?, ?)')->execute($valores);
            return new Socio((int) $this->pdo->lastInsertId(), $s->nombre, $s->dni, $s->categoria, $s->alta);
        }
        $this->pdo->prepare('UPDATE socio SET nombre = ?, dni = ?, categoria = ?, alta = ? WHERE id = ?')->execute([...$valores, $s->id]);
        return $s;
    }

    public function cantidadPorCategoria(): array
    {
        return $this->pdo->query('SELECT categoria, COUNT(*) FROM socio GROUP BY categoria ORDER BY categoria')->fetchAll(PDO::FETCH_KEY_PAIR);
    }
}
```

`main.php`
```php
<?php
declare(strict_types=1);
// Mision 1 - El repositorio de socios: entidades y SQL en un solo lugar.
require __DIR__ . '/src/Socio.php';
require __DIR__ . '/src/SocioRepositorio.php';
$c = require __DIR__ . '/config.php';
$repo = new SocioRepositorio(new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]));

$nuevo = $repo->guardar(new Socio(null, 'Diego Ruiz', '38777888', 'cadete', new DateTimeImmutable('2026-10-01')));
echo "Alta: {$nuevo->nombre} con id {$nuevo->id}\n";
$beto = $repo->buscarPorDni('31222333');
$repo->guardar($beto->conCategoria('activo'));
echo "Beto pasó a: ", $repo->buscarPorDni('31222333')->categoria, "\n";
echo "DNI 99999999: ", $repo->buscarPorDni('99999999') === null ? 'no existe' : 'existe', "\n";
echo "Activos: ", implode(', ', array_map(fn(Socio $s) => "{$s->nombre} (desde {$s->alta->format('Y')})", $repo->porCategoria('activo'))), "\n";
foreach ($repo->cantidadPorCategoria() as $categoria => $cantidad) {
    echo "  $categoria: $cantidad\n";
}
```

### Misión R04-N08-M2 · El repositorio de mentira

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Un servicio de **reservas de amarre** tiene una regla: un barco no puede reservar
más de 3 días seguidos ni superponerse con otra reserva del mismo muelle. La lógica
está en `ServicioReservas`, que recibe un `ReservaRepositorio` (interfaz con
`delMuelle(int $muelle): array` y `guardar(Reserva $r): void`). Escribí:

- la entidad `Reserva` (barco, muelle, desde y hasta como `DateTimeImmutable`);
- `ReservaRepositorioEnMemoria` (con un array) y `ReservaRepositorioPdo`;
- `ServicioReservas::reservar(...)` que aplica las reglas y lanza
  `DomainException` si no se cumplen.

`main.php` corre **las mismas reservas** con los dos repositorios y tiene que dar la
misma salida: así se prueba que la lógica no depende de la base.

#### Criterio de aprobación

- `ServicioReservas` depende de la interfaz, recibida por el constructor.
- Las dos implementaciones dan la misma salida.
- La salida coincide con la esperada.

#### Salida esperada

```
Con memoria:
  Gaviota en el muelle 1: reservado
  Albatros en el muelle 1: el muelle 1 ya está reservado por Gaviota
  Albatros en el muelle 2: una reserva va de 1 a 3 días (pediste 6)
  Albatros en el muelle 2: reservado
  Tortuga en el muelle 1: reservado
Con MariaDB:
  Gaviota en el muelle 1: reservado
  Albatros en el muelle 1: el muelle 1 ya está reservado por Gaviota
  Albatros en el muelle 2: una reserva va de 1 a 3 días (pediste 6)
  Albatros en el muelle 2: reservado
  Tortuga en el muelle 1: reservado
```

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS reserva;
CREATE TABLE reserva (
    id INT AUTO_INCREMENT PRIMARY KEY,
    barco VARCHAR(40) NOT NULL,
    muelle INT NOT NULL,
    desde DATE NOT NULL,
    hasta DATE NOT NULL,
    INDEX (muelle)
);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`src/reservas.php`
```php
<?php
declare(strict_types=1);

readonly class Reserva
{
    public function __construct(public string $barco, public int $muelle, public DateTimeImmutable $desde, public DateTimeImmutable $hasta) {}

    public function seSuperponeCon(Reserva $otra): bool
    {
        return $this->desde < $otra->hasta && $otra->desde < $this->hasta;
    }
}

interface ReservaRepositorio
{
    /** @return Reserva[] */
    public function delMuelle(int $muelle): array;

    public function guardar(Reserva $r): void;
}

class ReservaRepositorioEnMemoria implements ReservaRepositorio
{
    private array $reservas = [];

    public function delMuelle(int $muelle): array
    {
        return array_values(array_filter($this->reservas, fn(Reserva $r) => $r->muelle === $muelle));
    }

    public function guardar(Reserva $r): void
    {
        $this->reservas[] = $r;
    }
}

class ReservaRepositorioPdo implements ReservaRepositorio
{
    public function __construct(private PDO $pdo) {}

    public function delMuelle(int $muelle): array
    {
        $s = $this->pdo->prepare('SELECT * FROM reserva WHERE muelle = ? ORDER BY desde');
        $s->execute([$muelle]);
        return array_map(fn(array $f) => new Reserva($f['barco'], (int) $f['muelle'], new DateTimeImmutable($f['desde']), new DateTimeImmutable($f['hasta'])), $s->fetchAll());
    }

    public function guardar(Reserva $r): void
    {
        $this->pdo->prepare('INSERT INTO reserva (barco, muelle, desde, hasta) VALUES (?, ?, ?, ?)')
            ->execute([$r->barco, $r->muelle, $r->desde->format('Y-m-d'), $r->hasta->format('Y-m-d')]);
    }
}

class ServicioReservas
{
    public const MAX_DIAS = 3;

    public function __construct(private ReservaRepositorio $repositorio) {}

    public function reservar(string $barco, int $muelle, string $desde, string $hasta): Reserva
    {
        $nueva = new Reserva($barco, $muelle, new DateTimeImmutable($desde), new DateTimeImmutable($hasta));
        $dias = $nueva->desde->diff($nueva->hasta)->days;
        if ($nueva->hasta <= $nueva->desde || $dias > self::MAX_DIAS) {
            throw new DomainException("una reserva va de 1 a " . self::MAX_DIAS . " días (pediste $dias)");
        }
        foreach ($this->repositorio->delMuelle($muelle) as $existente) {
            if ($nueva->seSuperponeCon($existente)) {
                throw new DomainException("el muelle $muelle ya está reservado por {$existente->barco}");
            }
        }
        $this->repositorio->guardar($nueva);
        return $nueva;
    }
}
```

`main.php`
```php
<?php
declare(strict_types=1);
// Mision 2 - El repositorio de mentira: la misma lógica con memoria y con MariaDB.
require __DIR__ . '/src/reservas.php';
$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);

$pedidos = [
    ['Gaviota', 1, '2026-10-05', '2026-10-07'],
    ['Albatros', 1, '2026-10-06', '2026-10-08'],
    ['Albatros', 2, '2026-10-06', '2026-10-12'],
    ['Albatros', 2, '2026-10-06', '2026-10-09'],
    ['Tortuga', 1, '2026-10-07', '2026-10-08'],
];
foreach (['memoria' => new ReservaRepositorioEnMemoria(), 'MariaDB' => new ReservaRepositorioPdo($pdo)] as $nombre => $repo) {
    echo "Con $nombre:\n";
    $servicio = new ServicioReservas($repo);
    foreach ($pedidos as [$barco, $muelle, $desde, $hasta]) {
        try {
            $servicio->reservar($barco, $muelle, $desde, $hasta);
            echo "  $barco en el muelle $muelle: reservado\n";
        } catch (DomainException $e) {
            echo "  $barco en el muelle $muelle: ", $e->getMessage(), "\n";
        }
    }
}
```

### Misión R04-N08-M3 · El login del sistema de gestión

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Llevá el login de la Oficina (R03-N06) a MariaDB, como sitio web:

- tabla `usuario` (email único, nombre, rol `admin`/`operador`, hash, activo);
- `UsuarioRepositorio` con `autenticar()` (rechaza a los inactivos, usa
  `password_needs_rehash`) y `buscar(int $id)`;
- `public/index.php` con `?pagina=login|panel|salir`; en la sesión se guarda **solo el
  id**, y `panel` busca al usuario en cada pedido (si fue desactivado mientras tenía
  la sesión abierta, lo saca al login);
- CSRF, `session_regenerate_id` y mensaje de error que no revela nada.

El esquema trae los usuarios `kira@puerto.ar` (`ancla123`, admin) y
`bron@puerto.ar` (`faro2026`, operador, **inactivo**).

#### Criterio de aprobación

- La sesión guarda solo el id y el usuario se busca en cada pedido.
- Los inactivos no entran (ni siguen adentro si los desactivan).
- El acceso a datos está en el repositorio.

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS usuario;
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    nombre VARCHAR(60) NOT NULL,
    rol ENUM('admin', 'operador') NOT NULL,
    hash VARCHAR(255) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);
INSERT INTO usuario (email, nombre, rol, hash, activo) VALUES
    ('kira@puerto.ar', 'Kira Valdez', 'admin', '$2y$10$R7flf57cYzLAnMr14xX56OhKUJ5qlAco9VY/EbWmghiXoQB.vb5yS', TRUE),
    ('bron@puerto.ar', 'Bron', 'operador', '$2y$10$sY48d8IabcyzFGOVp12ZpuujEDnEgiSNQdtdVIB1rIGD4/BG9LYF6', FALSE);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`src/UsuarioRepositorio.php`
```php
<?php
declare(strict_types=1);

class UsuarioRepositorio
{
    public function __construct(private PDO $pdo) {}

    public function autenticar(string $email, string $clave): ?array
    {
        $s = $this->pdo->prepare('SELECT * FROM usuario WHERE email = ? AND activo = TRUE');
        $s->execute([mb_strtolower(trim($email))]);
        $u = $s->fetch();
        if ($u === false || !password_verify($clave, $u['hash'])) {
            return null;
        }
        if (password_needs_rehash($u['hash'], PASSWORD_DEFAULT)) {
            $this->pdo->prepare('UPDATE usuario SET hash = ? WHERE id = ?')->execute([password_hash($clave, PASSWORD_DEFAULT), $u['id']]);
        }
        return $u;
    }

    public function buscar(int $id): ?array
    {
        $s = $this->pdo->prepare('SELECT id, email, nombre, rol FROM usuario WHERE id = ? AND activo = TRUE');
        $s->execute([$id]);
        return $s->fetch() ?: null;
    }

    public function desactivar(int $id): void
    {
        $this->pdo->prepare('UPDATE usuario SET activo = FALSE WHERE id = ?')->execute([$id]);
    }
}
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Mision 3 - El login del sistema de gestión: usuarios en MariaDB y solo el id en la sesión.
session_start();
require __DIR__ . '/../src/UsuarioRepositorio.php';
$c = require __DIR__ . '/../config.php';
$usuarios = new UsuarioRepositorio(new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]));
$_SESSION['csrf'] ??= bin2hex(random_bytes(32));

function ir(string $pagina): never
{
    header('Location: index.php?pagina=' . $pagina, true, 303);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && !hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
    http_response_code(403);
    exit('Pedido no válido.');
}
$pagina = $_GET['pagina'] ?? 'panel';

if ($pagina === 'salir' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $_SESSION = [];
    session_destroy();
    ir('login');
}

if ($pagina === 'login') {
    $error = null;
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $u = $usuarios->autenticar($_POST['email'] ?? '', $_POST['clave'] ?? '');
        if ($u !== null) {
            session_regenerate_id(true);
            $_SESSION['usuario_id'] = (int) $u['id'];
            ir('panel');
        }
        $error = 'Email o contraseña incorrectos.';
    }
    ?>
    <h1>Sistema de gestión</h1>
    <?php if ($error): ?><p><?= $error ?></p><?php endif; ?>
    <form method="post"><input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
        <input name="email"> <input type="password" name="clave"> <button>Entrar</button></form>
    <?php
    exit;
}

$yo = isset($_SESSION['usuario_id']) ? $usuarios->buscar($_SESSION['usuario_id']) : null;
if ($yo === null) {
    $_SESSION = [];
    ir('login');
}
?>
<h1>Hola, <?= htmlspecialchars($yo['nombre']) ?> (<?= $yo['rol'] ?>)</h1>
<form method="post" action="?pagina=salir"><input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>"><button>Salir</button></form>
```

### Encargo R04-N08-E1 · La biblioteca con capas

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

La biblioteca popular quiere su sistema de préstamos por terminal, en capas:

- entidades `Libro` y `Prestamo`;
- `LibroRepositorio` (`buscarPorCodigo`, `disponibles`) y `PrestamoRepositorio`
  (`abiertosDe(string $socio)`, `registrar`, `devolver`) con PDO;
- `ServicioPrestamos` con las reglas: un socio no puede tener más de **2** préstamos
  abiertos; un libro prestado no se puede volver a prestar; al devolver, se calcula
  si hubo **atraso** (más de 14 días) y la multa ($500 por día de atraso). Préstamo
  y devolución van en **transacciones** (el libro cambia de estado y se registra el
  movimiento).

`main.php` procesa comandos de la entrada (`PRESTAR;CODIGO;SOCIO;FECHA` y
`DEVOLVER;CODIGO;FECHA`) y al final muestra los libros disponibles.

#### Criterio de aprobación

- Capas separadas: entidades, repositorios con PDO y servicio con las reglas.
- Préstamo y devolución en transacciones.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
PRESTAR;L-001;Ana;2026-09-01
PRESTAR;L-002;Ana;2026-09-02
PRESTAR;L-003;Ana;2026-09-03
PRESTAR;L-001;Beto;2026-09-04
DEVOLVER;L-001;2026-09-20
PRESTAR;L-001;Beto;2026-09-21
DEVOLVER;L-002;2026-09-10
DEVOLVER;L-004;2026-09-22
```

#### Salida esperada

```
«Rayuela» prestado a Ana
«Ficciones» prestado a Ana
No se pudo: Ana ya tiene 2 préstamos abiertos
No se pudo: «Rayuela» ya está prestado
«Rayuela» devuelto por Ana con 5 día/s de atraso: multa $2500
«Rayuela» prestado a Beto
«Ficciones» devuelto por Ana a tiempo
No se pudo: «Bestiario» no estaba prestado
Disponibles: Ficciones, El túnel, Bestiario
```

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS prestamo;
DROP TABLE IF EXISTS libro;
CREATE TABLE libro (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo CHAR(5) NOT NULL UNIQUE,
    titulo VARCHAR(60) NOT NULL,
    prestado BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE TABLE prestamo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    libro_id INT NOT NULL,
    socio VARCHAR(40) NOT NULL,
    desde DATE NOT NULL,
    devuelto DATE NULL,
    multa DECIMAL(10, 2) NOT NULL DEFAULT 0,
    FOREIGN KEY (libro_id) REFERENCES libro(id)
);
INSERT INTO libro (codigo, titulo) VALUES ('L-001', 'Rayuela'), ('L-002', 'Ficciones'), ('L-003', 'El túnel'), ('L-004', 'Bestiario');
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`src/biblioteca.php`
```php
<?php
declare(strict_types=1);

readonly class Libro
{
    public function __construct(public int $id, public string $codigo, public string $titulo, public bool $prestado) {}

    public static function desdeFila(array $f): self
    {
        return new self((int) $f['id'], $f['codigo'], $f['titulo'], (bool) $f['prestado']);
    }
}

readonly class Prestamo
{
    public function __construct(public int $id, public int $libroId, public string $socio, public DateTimeImmutable $desde) {}

    public static function desdeFila(array $f): self
    {
        return new self((int) $f['id'], (int) $f['libro_id'], $f['socio'], new DateTimeImmutable($f['desde']));
    }
}

class LibroRepositorio
{
    public function __construct(private PDO $pdo) {}

    public function buscarPorCodigo(string $codigo): ?Libro
    {
        $s = $this->pdo->prepare('SELECT * FROM libro WHERE codigo = ?');
        $s->execute([$codigo]);
        $f = $s->fetch();
        return $f === false ? null : Libro::desdeFila($f);
    }

    public function marcarPrestado(int $id, bool $prestado): void
    {
        $this->pdo->prepare('UPDATE libro SET prestado = ? WHERE id = ?')->execute([(int) $prestado, $id]);
    }

    /** @return Libro[] */
    public function disponibles(): array
    {
        return array_map([Libro::class, 'desdeFila'], $this->pdo->query('SELECT * FROM libro WHERE prestado = FALSE ORDER BY codigo')->fetchAll());
    }
}

class PrestamoRepositorio
{
    public function __construct(private PDO $pdo) {}

    public function abiertosDe(string $socio): int
    {
        $s = $this->pdo->prepare('SELECT COUNT(*) FROM prestamo WHERE socio = ? AND devuelto IS NULL');
        $s->execute([$socio]);
        return (int) $s->fetchColumn();
    }

    public function abiertoDelLibro(int $libroId): ?Prestamo
    {
        $s = $this->pdo->prepare('SELECT * FROM prestamo WHERE libro_id = ? AND devuelto IS NULL');
        $s->execute([$libroId]);
        $f = $s->fetch();
        return $f === false ? null : Prestamo::desdeFila($f);
    }

    public function registrar(int $libroId, string $socio, DateTimeImmutable $desde): void
    {
        $this->pdo->prepare('INSERT INTO prestamo (libro_id, socio, desde) VALUES (?, ?, ?)')->execute([$libroId, $socio, $desde->format('Y-m-d')]);
    }

    public function cerrar(int $id, DateTimeImmutable $fecha, float $multa): void
    {
        $this->pdo->prepare('UPDATE prestamo SET devuelto = ?, multa = ? WHERE id = ?')->execute([$fecha->format('Y-m-d'), $multa, $id]);
    }
}

class ServicioPrestamos
{
    public const MAX_ABIERTOS = 2;
    public const DIAS_PERMITIDOS = 14;
    public const MULTA_POR_DIA = 500;

    public function __construct(private PDO $pdo, private LibroRepositorio $libros, private PrestamoRepositorio $prestamos) {}

    public function prestar(string $codigo, string $socio, string $fecha): string
    {
        return $this->enTransaccion(function () use ($codigo, $socio, $fecha): string {
            $libro = $this->libros->buscarPorCodigo($codigo) ?? throw new DomainException("no existe el libro $codigo");
            if ($libro->prestado) {
                throw new DomainException("«{$libro->titulo}» ya está prestado");
            }
            if ($this->prestamos->abiertosDe($socio) >= self::MAX_ABIERTOS) {
                throw new DomainException("$socio ya tiene " . self::MAX_ABIERTOS . ' préstamos abiertos');
            }
            $this->prestamos->registrar($libro->id, $socio, new DateTimeImmutable($fecha));
            $this->libros->marcarPrestado($libro->id, true);
            return "«{$libro->titulo}» prestado a $socio";
        });
    }

    public function devolver(string $codigo, string $fecha): string
    {
        return $this->enTransaccion(function () use ($codigo, $fecha): string {
            $libro = $this->libros->buscarPorCodigo($codigo) ?? throw new DomainException("no existe el libro $codigo");
            $prestamo = $this->prestamos->abiertoDelLibro($libro->id) ?? throw new DomainException("«{$libro->titulo}» no estaba prestado");
            $dia = new DateTimeImmutable($fecha);
            $atraso = max(0, $prestamo->desde->diff($dia)->days - self::DIAS_PERMITIDOS);
            $multa = $atraso * self::MULTA_POR_DIA;
            $this->prestamos->cerrar($prestamo->id, $dia, $multa);
            $this->libros->marcarPrestado($libro->id, false);
            return "«{$libro->titulo}» devuelto por {$prestamo->socio}" . ($atraso > 0 ? " con $atraso día/s de atraso: multa \$$multa" : ' a tiempo');
        });
    }

    private function enTransaccion(callable $trabajo): string
    {
        $this->pdo->beginTransaction();
        try {
            $resultado = $trabajo();
            $this->pdo->commit();
            return $resultado;
        } catch (Throwable $e) {
            $this->pdo->rollBack();
            throw $e;
        }
    }
}
```

`main.php`
```php
<?php
declare(strict_types=1);
// Encargo - La biblioteca con capas: entidades, repositorios, servicio y transacciones.
require __DIR__ . '/src/biblioteca.php';
$c = require __DIR__ . '/config.php';
$pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);
$libros = new LibroRepositorio($pdo);
$servicio = new ServicioPrestamos($pdo, $libros, new PrestamoRepositorio($pdo));

while (($linea = fgets(STDIN)) !== false) {
    $campos = explode(';', trim($linea));
    try {
        echo match ($campos[0]) {
            'PRESTAR' => $servicio->prestar($campos[1], $campos[2], $campos[3]),
            'DEVOLVER' => $servicio->devolver($campos[1], $campos[2]),
            default => "comando desconocido: {$campos[0]}",
        }, "\n";
    } catch (DomainException $e) {
        echo "No se pudo: ", $e->getMessage(), "\n";
    }
}
echo "Disponibles: ", implode(', ', array_map(fn(Libro $l) => $l->titulo, $libros->disponibles())), "\n";
```

### Prueba del sello

#### ¿Qué es un repositorio?

Una clase que junta todo el acceso a una tabla (o a un tipo de objeto) con métodos del problema (`activos()`, `guardar()`), para que el resto del sistema no escriba SQL.

#### ¿Por qué el repositorio recibe el `PDO` por el constructor?

Para compartir una sola conexión, poder usar transacciones que abarquen varios repositorios y poder reemplazarlo en las pruebas.

#### ¿Para qué sirve tener un repositorio en memoria además del de PDO?

Para probar la lógica del negocio sin base de datos, más rápido y sin depender de los datos cargados.

#### ¿Qué se guarda en la sesión después del login y por qué?

Solo el id del usuario: en cada pedido se lo busca en la base, así un usuario desactivado o con otro rol lo nota enseguida.

#### ¿Qué hace `password_needs_rehash`?

Dice si un hash se hizo con un algoritmo o costo viejo; si es así, se vuelve a calcular con la contraseña que acaba de escribir el usuario y se guarda el nuevo.

### Soluciones (docente)

Nodo nuevo; es el puente hacia el MVC (rama 5) y hacia Eloquent (Senda de Laravel). En el ejemplo, el hash de Bron tiene costo 4 a propósito (`$2y$04$…`, hecho con `password_hash('faro2026', PASSWORD_BCRYPT, ['cost' => 4])`): al entrar, `password_needs_rehash` lo actualiza al costo por defecto (10 en PHP 8.3; 12 en PHP 8.4). En la misión 2, la misma lógica corre sobre memoria y sobre MariaDB: anticipa las pruebas con PHPUnit.

## R04-N09 · Jefe: la Serpiente Marina de las Tablas

```meta
tipo: jefe
padre: R04-N08
precio: 10
criatura: dragon
insignia: Sello de la Serpiente Marina
insignia_descripcion: Venciste a la Serpiente Marina de las Tablas: construís sistemas sobre MySQL y MariaDB con transacciones y repositorios.
```

### Crónica

En lo más hondo de la Bodega, donde el agua del puerto se filtra entre las piedras, vive la **Serpiente Marina de las Tablas**. Se alimenta de los sistemas mal hechos: consultas armadas pegando textos, transferencias que se cortan a la mitad, stock que se vende dos veces, datos repetidos que se contradicen. Cada error la hace más grande, y ya se enroscó alrededor de los dos sistemas que construiste en la Oficina.

—Tus sistemas de reclamos y de artesanías funcionaban con archivos JSON —dice {mentor}—. La Serpiente los está ahogando: con muchos usuarios a la vez, los archivos se pisan. Llevalos a la Bodega, {heroe}. Tablas bien diseñadas, consultas preparadas, transacciones y repositorios. Cuando la Serpiente no encuentre por dónde entrar, se va a ir al fondo del mar.

### Objetivos

- Diseñar el esquema completo de un sistema: tablas, claves, relaciones e índices.
- Rehacer un sistema web sobre MariaDB con repositorios, consultas preparadas y transacciones.
- Proteger las operaciones concurrentes (stock) y conservar la historia (estados, precios).

### Antes de empezar

- Toda la Bodega (R04-N01 a R04-N08) y el jefe de la Oficina (R03-N09).

### Explicación

#### El escudo de la Bodega
Además de la lista del escudo de la Oficina (escapar, CSRF, validar, permisos,
PRG), revisá:
| Pregunta | Si la respuesta es no… |
|---|---|
| ¿Cada dato de afuera va como parámetro? | inyección SQL |
| ¿Las operaciones de varios pasos están en transacciones? | datos a medias |
| ¿El stock (o el cupo) se protege con `FOR UPDATE` o un `UPDATE` con condición? | ventas de más |
| ¿Las tablas tienen claves foráneas y `UNIQUE` donde corresponde? | datos huérfanos o duplicados |
| ¿Los precios y estados pasados se guardan (no se recalculan)? | historia que cambia sola |
| ¿El SQL está en repositorios? | SQL desparramado |
| ¿Las columnas de los `WHERE` frecuentes tienen índice? | un sistema que se arrastra |

#### Del JSON a la base, paso a paso
1. **Diseñá el esquema** en un `esquema.sql`: una tabla por cosa, claves foráneas,
   `UNIQUE`, `CHECK`, índices. Dibujalo en papel antes.
2. **Escribí los repositorios** (uno por tabla principal) y probalos con un script
   de terminal.
3. **Cambiá las páginas**: donde había `leerJson`/`guardarJson`, llamá al
   repositorio. Las vistas casi no cambian.
4. **Envolvé en transacciones** todo lo que toque más de una tabla.

### Misión R04-N09-M1 · Los reclamos en la Bodega

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 30
```

#### Consigna

Rehacé la **oficina de reclamos** (R03-N09-M1) con MariaDB:

- **Esquema**: `usuario` (email único, nombre, rol `vecino`/`operador`, hash),
  `reclamo` (número único `R-0001`, usuario, categoría, dirección, descripción,
  estado, fecha) y `cambio_estado` (reclamo, estado anterior, estado nuevo, quién lo
  cambió y cuándo). Índices por usuario y por estado.
- **Repositorios**: `UsuarioRepositorio` (autenticar, buscar) y `ReclamoRepositorio`
  (crear, delUsuario, todos con filtro por estado, avanzarEstado).
- **`avanzarEstado`** en una **transacción**: lee el reclamo con `FOR UPDATE`, calcula
  el estado siguiente, lo actualiza y registra el cambio en `cambio_estado`.
- **El número** `R-0001` se arma a partir del `id` generado (`sprintf('R-%04d', $id)`),
  en la misma transacción que el `INSERT`.
- La ficha de cada reclamo (`?pagina=ver&numero=R-0001`) muestra su historial de
  cambios con quién y cuándo; un vecino solo puede ver sus propios reclamos (403 si
  no).

El resto (login, roles, validación, CSRF, PRG, flash) igual que en la Oficina.

#### Criterio de aprobación

- Pasa el escudo de la Oficina y el de la Bodega.
- Los cambios de estado quedan registrados con transacción.
- Un vecino no puede ver reclamos ajenos (403).

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS cambio_estado;
DROP TABLE IF EXISTS reclamo;
DROP TABLE IF EXISTS usuario;
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    nombre VARCHAR(60) NOT NULL,
    rol ENUM('vecino', 'operador') NOT NULL,
    hash VARCHAR(255) NOT NULL
) ENGINE=InnoDB;
CREATE TABLE reclamo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero CHAR(6) NULL UNIQUE,
    usuario_id INT NOT NULL,
    categoria ENUM('alumbrado', 'baches', 'residuos', 'arbolado') NOT NULL,
    direccion VARCHAR(80) NOT NULL,
    descripcion VARCHAR(500) NOT NULL,
    estado ENUM('nuevo', 'en curso', 'resuelto') NOT NULL DEFAULT 'nuevo',
    creado DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    INDEX idx_reclamo_estado (estado)
) ENGINE=InnoDB;
CREATE TABLE cambio_estado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reclamo_id INT NOT NULL,
    anterior VARCHAR(10) NOT NULL,
    nuevo VARCHAR(10) NOT NULL,
    usuario_id INT NOT NULL,
    cuando DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reclamo_id) REFERENCES reclamo(id),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
) ENGINE=InnoDB;
INSERT INTO usuario (email, nombre, rol, hash) VALUES
    ('ana@vecinos.ar', 'Ana Pérez', 'vecino', '$2y$10$R7flf57cYzLAnMr14xX56OhKUJ5qlAco9VY/EbWmghiXoQB.vb5yS'),
    ('beto@vecinos.ar', 'Beto Díaz', 'vecino', '$2y$10$sY48d8IabcyzFGOVp12ZpuujEDnEgiSNQdtdVIB1rIGD4/BG9LYF6'),
    ('ofelia@muni.ar', 'Ofelia Ruiz', 'operador', '$2y$10$RkUlc28FIys.6Idh51m8LuGuli1S.au.X3HuqdvuzElfhWtzOf6FO');
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`src/app.php`
```php
<?php
declare(strict_types=1);

const CATEGORIAS = ['alumbrado', 'baches', 'residuos', 'arbolado'];
const ESTADOS = ['nuevo', 'en curso', 'resuelto'];

function conectar(): PDO
{
    static $pdo = null;
    if ($pdo === null) {
        $c = require __DIR__ . '/../config.php';
        $pdo = new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]);
    }
    return $pdo;
}

function e(?string $t): string
{
    return htmlspecialchars($t ?? '', ENT_QUOTES, 'UTF-8');
}

function csrf(): string
{
    return $_SESSION['csrf'] ??= bin2hex(random_bytes(32));
}

function ir(string $query, ?string $flash = null): never
{
    if ($flash !== null) {
        $_SESSION['flash'] = $flash;
    }
    header('Location: index.php?' . $query, true, 303);
    exit;
}

function prohibido(): never
{
    http_response_code(403);
    exit('No tenés permiso para esto.');
}

class UsuarioRepositorio
{
    public function __construct(private PDO $pdo) {}

    public function autenticar(string $email, string $clave): ?array
    {
        $s = $this->pdo->prepare('SELECT * FROM usuario WHERE email = ?');
        $s->execute([mb_strtolower(trim($email))]);
        $u = $s->fetch();
        return $u !== false && password_verify($clave, $u['hash']) ? $u : null;
    }

    public function buscar(int $id): ?array
    {
        $s = $this->pdo->prepare('SELECT id, nombre, rol FROM usuario WHERE id = ?');
        $s->execute([$id]);
        return $s->fetch() ?: null;
    }
}

class ReclamoRepositorio
{
    public function __construct(private PDO $pdo) {}

    public function crear(int $usuarioId, string $categoria, string $direccion, string $descripcion): string
    {
        $this->pdo->beginTransaction();
        try {
            $this->pdo->prepare('INSERT INTO reclamo (usuario_id, categoria, direccion, descripcion) VALUES (?, ?, ?, ?)')
                ->execute([$usuarioId, $categoria, $direccion, $descripcion]);
            $id = (int) $this->pdo->lastInsertId();
            $numero = sprintf('R-%04d', $id);
            $this->pdo->prepare('UPDATE reclamo SET numero = ? WHERE id = ?')->execute([$numero, $id]);
            $this->pdo->commit();
            return $numero;
        } catch (Throwable $e) {
            $this->pdo->rollBack();
            throw $e;
        }
    }

    public function delUsuario(int $usuarioId): array
    {
        $s = $this->pdo->prepare('SELECT * FROM reclamo WHERE usuario_id = ? ORDER BY id');
        $s->execute([$usuarioId]);
        return $s->fetchAll();
    }

    public function todos(string $estado): array
    {
        $sql = 'SELECT r.*, u.nombre AS vecino FROM reclamo r JOIN usuario u ON u.id = r.usuario_id';
        if ($estado === '') {
            return $this->pdo->query("$sql ORDER BY r.id")->fetchAll();
        }
        $s = $this->pdo->prepare("$sql WHERE r.estado = ? ORDER BY r.id");
        $s->execute([$estado]);
        return $s->fetchAll();
    }

    public function porNumero(string $numero): ?array
    {
        $s = $this->pdo->prepare('SELECT * FROM reclamo WHERE numero = ?');
        $s->execute([$numero]);
        return $s->fetch() ?: null;
    }

    public function historial(int $reclamoId): array
    {
        $s = $this->pdo->prepare("SELECT c.anterior, c.nuevo, u.nombre, DATE_FORMAT(c.cuando, '%d/%m/%Y') AS dia FROM cambio_estado c JOIN usuario u ON u.id = c.usuario_id WHERE c.reclamo_id = ? ORDER BY c.id");
        $s->execute([$reclamoId]);
        return $s->fetchAll();
    }

    /** Pasa al estado siguiente y lo registra; devuelve el estado nuevo o null si ya estaba resuelto. */
    public function avanzarEstado(string $numero, int $operadorId): ?string
    {
        $this->pdo->beginTransaction();
        try {
            $s = $this->pdo->prepare('SELECT id, estado FROM reclamo WHERE numero = ? FOR UPDATE');
            $s->execute([$numero]);
            $r = $s->fetch();
            $posicion = $r === false ? false : array_search($r['estado'], ESTADOS, true);
            if ($r === false || $posicion === count(ESTADOS) - 1) {
                $this->pdo->rollBack();
                return null;
            }
            $nuevo = ESTADOS[$posicion + 1];
            $this->pdo->prepare('UPDATE reclamo SET estado = ? WHERE id = ?')->execute([$nuevo, $r['id']]);
            $this->pdo->prepare('INSERT INTO cambio_estado (reclamo_id, anterior, nuevo, usuario_id) VALUES (?, ?, ?, ?)')->execute([$r['id'], $r['estado'], $nuevo, $operadorId]);
            $this->pdo->commit();
            return $nuevo;
        } catch (Throwable $e) {
            $this->pdo->rollBack();
            throw $e;
        }
    }
}
```

`public/index.php`
```php
<?php
declare(strict_types=1);
// Jefe R04 - Los reclamos en la Bodega: repositorios, transacciones e historial.
session_start();
require __DIR__ . '/../src/app.php';
$usuarios = new UsuarioRepositorio(conectar());
$reclamos = new ReclamoRepositorio(conectar());

$pagina = $_GET['pagina'] ?? 'inicio';
$post = $_SERVER['REQUEST_METHOD'] === 'POST';
if ($post && !hash_equals(csrf(), $_POST['csrf'] ?? '')) {
    prohibido();
}

if ($pagina === 'login') {
    $error = null;
    if ($post) {
        $u = $usuarios->autenticar($_POST['email'] ?? '', $_POST['clave'] ?? '');
        if ($u !== null) {
            session_regenerate_id(true);
            $_SESSION['usuario_id'] = (int) $u['id'];
            ir('pagina=inicio');
        }
        $error = 'Email o contraseña incorrectos.';
    }
    echo '<h1>Reclamos vecinales</h1>', $error ? '<p>' . e($error) . '</p>' : '',
        '<form method="post"><input type="hidden" name="csrf" value="' . csrf() . '"><input name="email"> <input type="password" name="clave"> <button>Entrar</button></form>';
    exit;
}

$yo = isset($_SESSION['usuario_id']) ? $usuarios->buscar($_SESSION['usuario_id']) : null;
if ($yo === null) {
    ir('pagina=login');
}

if ($pagina === 'salir' && $post) {
    $_SESSION = [];
    session_destroy();
    ir('pagina=login');
}

$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']);
echo '<nav>', e($yo['nombre']), ' (', $yo['rol'], ') <form method="post" action="?pagina=salir" style="display:inline"><input type="hidden" name="csrf" value="', csrf(), '"><button>Salir</button></form></nav>';
if ($flash !== null) {
    echo '<p><strong>', e($flash), '</strong></p>';
}

switch ($pagina) {
    case 'nuevo':
        if ($yo['rol'] !== 'vecino') {
            prohibido();
        }
        $d = ['categoria' => 'alumbrado', 'direccion' => '', 'descripcion' => ''];
        $errores = [];
        if ($post) {
            foreach (array_keys($d) as $campo) {
                $d[$campo] = trim((string) ($_POST[$campo] ?? ''));
            }
            if (!in_array($d['categoria'], CATEGORIAS, true)) {
                $errores[] = 'Elegí una categoría de la lista.';
            }
            if (mb_strlen($d['direccion']) < 5 || mb_strlen($d['direccion']) > 80) {
                $errores[] = 'La dirección va de 5 a 80 caracteres.';
            }
            if (mb_strlen($d['descripcion']) < 10 || mb_strlen($d['descripcion']) > 500) {
                $errores[] = 'La descripción va de 10 a 500 caracteres.';
            }
            if ($errores === []) {
                $numero = $reclamos->crear($yo['id'], $d['categoria'], $d['direccion'], $d['descripcion']);
                ir('pagina=inicio', "Registramos tu reclamo $numero.");
            }
        }
        echo '<h1>Nuevo reclamo</h1>';
        foreach ($errores as $error) {
            echo '<p>', e($error), '</p>';
        }
        echo '<form method="post"><input type="hidden" name="csrf" value="', csrf(), '"><select name="categoria">';
        foreach (CATEGORIAS as $cat) {
            echo '<option', $cat === $d['categoria'] ? ' selected' : '', '>', $cat, '</option>';
        }
        echo '</select><input name="direccion" value="', e($d['direccion']), '"><textarea name="descripcion">', e($d['descripcion']), '</textarea><button>Enviar</button></form>';
        break;

    case 'avanzar':
        if ($yo['rol'] !== 'operador' || !$post) {
            prohibido();
        }
        $numero = $_POST['numero'] ?? '';
        $nuevo = $reclamos->avanzarEstado($numero, $yo['id']);
        ir('pagina=inicio', $nuevo === null ? "$numero no se puede avanzar." : "$numero pasó a «{$nuevo}».");

    case 'ver':
        $r = $reclamos->porNumero($_GET['numero'] ?? '');
        if ($r === null) {
            http_response_code(404);
            exit('No existe ese reclamo.');
        }
        if ($yo['rol'] !== 'operador' && $r['usuario_id'] !== $yo['id']) {
            prohibido();
        }
        echo '<h1>', e($r['numero']), ' · ', e($r['categoria']), '</h1><p>', e($r['direccion']), ': ', e($r['descripcion']), '</p><p>Estado: ', $r['estado'], '</p><ul>';
        foreach ($reclamos->historial($r['id']) as $h) {
            echo '<li>', $h['dia'], ': ', $h['anterior'], ' → ', $h['nuevo'], ' (', e($h['nombre']), ')</li>';
        }
        echo '</ul>';
        break;

    default:
        if ($yo['rol'] === 'operador') {
            $filtro = in_array($_GET['estado'] ?? '', ESTADOS, true) ? $_GET['estado'] : '';
            $lista = $reclamos->todos($filtro);
        } else {
            $lista = $reclamos->delUsuario($yo['id']);
            echo '<p><a href="?pagina=nuevo">Nuevo reclamo</a></p>';
        }
        echo '<p>', count($lista), ' reclamo/s</p><ul>';
        foreach ($lista as $r) {
            echo '<li><a href="?pagina=ver&amp;numero=', e($r['numero']), '">', e($r['numero']), '</a> ', e($r['categoria']), ' · ', e($r['direccion']), ' · ', $r['estado'];
            if ($yo['rol'] === 'operador' && $r['estado'] !== 'resuelto') {
                echo ' <form method="post" action="?pagina=avanzar" style="display:inline"><input type="hidden" name="csrf" value="', csrf(), '"><input type="hidden" name="numero" value="', e($r['numero']), '"><button>Avanzar</button></form>';
            }
            echo '</li>';
        }
        echo '</ul>';
}
```

### Misión R04-N09-M2 · La tienda en la Bodega

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 30
```

#### Consigna

Rehacé la **tienda de artesanías** (R03-N09-M2) con MariaDB, como una API de
terminal (para concentrarte en la base; la web ya la sabés hacer):

- **Esquema**: `producto` (código, nombre, precio, stock con `CHECK >= 0`),
  `pedido` (número, cliente, email, total, fecha), `renglon` (pedido, producto,
  cantidad, **precio al momento**) e índices donde haga falta.
- **`ServicioVentas::comprar(string $cliente, string $email, array $carrito): string`**
  en una transacción: bloquea cada producto con `FOR UPDATE` **en orden de código**
  (para que dos compras no se traben entre sí), verifica el stock, crea el pedido,
  los renglones y descuenta; si algo falla, no queda nada. Devuelve el número
  `P-0001`.
- **`ServicioVentas::reporte(): array`** con una consulta: por producto, unidades
  vendidas, facturado y stock restante (incluyendo los no vendidos).
- **Precio histórico**: después de una compra, subí el precio de un producto y
  mostrá que el total del pedido viejo no cambia.

`main.php` procesa los comandos de la entrada (`COMPRAR;CLIENTE;EMAIL;COD:CANT,COD:CANT`,
`PRECIO;COD;NUEVO`, `PEDIDO;P-0001` y `REPORTE`).

#### Criterio de aprobación

- La compra es una transacción con `FOR UPDATE` y no deja nada a medias.
- Los renglones guardan el precio del momento.
- El reporte sale de una sola consulta con `LEFT JOIN`.
- La salida coincide con la esperada para la entrada de ejemplo.

#### Entrada de ejemplo

```
COMPRAR;Lucía Ávila;lu@correo.com;CES02:2,DUL04:3
COMPRAR;Tomás Ruiz;tomi@correo.com;TEJ03:1,PON01:3
PRECIO;CES02;29900
COMPRAR;Tomás Ruiz;tomi@correo.com;TEJ03:1,CES02:1
PEDIDO;P-0001
PEDIDO;P-0009
REPORTE
```

#### Salida esperada

```
Compra de Lucía Ávila: pedido P-0001
Compra de Tomás Ruiz: No hay 3 de Poncho de vicuña (quedan 2). No se guardó nada.
Nuevo precio de CES02: $29.900,00
Compra de Tomás Ruiz: pedido P-0002
Pedido P-0001 de Lucía Ávila: total $66.400,00
  2 × CES02 a $24.500,00
  3 × DUL04 a $5.800,00
No existe el pedido P-0009
  TEJ03  1 u.     $96.000,00  stock  0  Tapiz de telar criollo
  CES02  3 u.     $78.900,00  stock  3  Cesto de simbol
  DUL04  3 u.     $17.400,00  stock 17  Dulce de cayote (500 g)
  MAT05  0 u.          $0,00  stock  8  Mate de calabaza
  PON01  0 u.          $0,00  stock  2  Poncho de vicuña
```

#### Solución de referencia

`esquema.sql`
```sql
DROP TABLE IF EXISTS renglon;
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (
    codigo CHAR(5) PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio > 0),
    stock INT NOT NULL CHECK (stock >= 0)
) ENGINE=InnoDB;
CREATE TABLE pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero CHAR(6) NULL UNIQUE,
    cliente VARCHAR(60) NOT NULL,
    email VARCHAR(100) NOT NULL,
    total DECIMAL(12, 2) NOT NULL DEFAULT 0,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_pedido_email (email)
) ENGINE=InnoDB;
CREATE TABLE renglon (
    pedido_id INT NOT NULL,
    codigo CHAR(5) NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (pedido_id, codigo),
    FOREIGN KEY (pedido_id) REFERENCES pedido(id),
    FOREIGN KEY (codigo) REFERENCES producto(codigo)
) ENGINE=InnoDB;
INSERT INTO producto VALUES
    ('PON01', 'Poncho de vicuña', 380000, 2), ('CES02', 'Cesto de simbol', 24500, 6),
    ('TEJ03', 'Tapiz de telar criollo', 96000, 1), ('DUL04', 'Dulce de cayote (500 g)', 5800, 20),
    ('MAT05', 'Mate de calabaza', 12000, 8);
```

`config.php`
```php
<?php
return ['dsn' => 'mysql:host=localhost;dbname=puerto;charset=utf8mb4', 'usuario' => 'root', 'clave' => ''];
```

`src/ServicioVentas.php`
```php
<?php
declare(strict_types=1);

class ServicioVentas
{
    public function __construct(private PDO $pdo) {}

    /** @param array<string, int> $carrito código => cantidad */
    public function comprar(string $cliente, string $email, array $carrito): string
    {
        if ($carrito === [] || filter_var($email, FILTER_VALIDATE_EMAIL) === false) {
            throw new InvalidArgumentException('Pedido inválido');
        }
        ksort($carrito);                          // bloquear siempre en el mismo orden evita que dos compras se traben
        $this->pdo->beginTransaction();
        try {
            $leer = $this->pdo->prepare('SELECT nombre, precio, stock FROM producto WHERE codigo = ? FOR UPDATE');
            $productos = [];
            foreach ($carrito as $codigo => $cantidad) {
                $leer->execute([$codigo]);
                $p = $leer->fetch() ?: throw new DomainException("No existe el producto $codigo");
                if ($p['stock'] < $cantidad) {
                    throw new DomainException("No hay $cantidad de {$p['nombre']} (quedan {$p['stock']})");
                }
                $productos[$codigo] = $p;
            }
            $this->pdo->prepare('INSERT INTO pedido (cliente, email) VALUES (?, ?)')->execute([$cliente, $email]);
            $id = (int) $this->pdo->lastInsertId();
            $renglon = $this->pdo->prepare('INSERT INTO renglon (pedido_id, codigo, cantidad, precio) VALUES (?, ?, ?, ?)');
            $descontar = $this->pdo->prepare('UPDATE producto SET stock = stock - ? WHERE codigo = ?');
            $total = 0;
            foreach ($carrito as $codigo => $cantidad) {
                $renglon->execute([$id, $codigo, $cantidad, $productos[$codigo]['precio']]);
                $descontar->execute([$cantidad, $codigo]);
                $total += $cantidad * (float) $productos[$codigo]['precio'];
            }
            $numero = sprintf('P-%04d', $id);
            $this->pdo->prepare('UPDATE pedido SET numero = ?, total = ? WHERE id = ?')->execute([$numero, $total, $id]);
            $this->pdo->commit();
            return $numero;
        } catch (Throwable $e) {
            $this->pdo->rollBack();
            throw $e;
        }
    }

    public function cambiarPrecio(string $codigo, float $precio): void
    {
        $this->pdo->prepare('UPDATE producto SET precio = ? WHERE codigo = ?')->execute([$precio, $codigo]);
    }

    public function pedido(string $numero): ?array
    {
        $s = $this->pdo->prepare('SELECT p.numero, p.cliente, p.total, r.codigo, r.cantidad, r.precio FROM pedido p JOIN renglon r ON r.pedido_id = p.id WHERE p.numero = ? ORDER BY r.codigo');
        $s->execute([$numero]);
        $filas = $s->fetchAll();
        return $filas === [] ? null : $filas;
    }

    public function reporte(): array
    {
        return $this->pdo->query(
            'SELECT pr.codigo, pr.nombre, COALESCE(SUM(r.cantidad), 0) AS unidades, COALESCE(SUM(r.cantidad * r.precio), 0) AS facturado, pr.stock
             FROM producto pr LEFT JOIN renglon r ON r.codigo = pr.codigo
             GROUP BY pr.codigo, pr.nombre, pr.stock ORDER BY facturado DESC, pr.codigo'
        )->fetchAll();
    }
}
```

`main.php`
```php
<?php
declare(strict_types=1);
// Jefe R04 - La tienda en la Bodega: compra con transacción, FOR UPDATE y precio histórico.
require __DIR__ . '/src/ServicioVentas.php';
$c = require __DIR__ . '/config.php';
$ventas = new ServicioVentas(new PDO($c['dsn'], $c['usuario'], $c['clave'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]));
$pesos = fn($n): string => '$' . number_format((float) $n, 2, ',', '.');

while (($linea = fgets(STDIN)) !== false) {
    $campos = explode(';', trim($linea));
    try {
        switch ($campos[0]) {
            case 'COMPRAR':
                $carrito = [];
                foreach (explode(',', $campos[3]) as $item) {
                    [$codigo, $cantidad] = explode(':', $item);
                    $carrito[$codigo] = (int) $cantidad;
                }
                $numero = $ventas->comprar($campos[1], $campos[2], $carrito);   // primero comprar, después mostrar
                echo "Compra de {$campos[1]}: pedido $numero\n";
                break;
            case 'PRECIO':
                $ventas->cambiarPrecio($campos[1], (float) $campos[2]);
                echo "Nuevo precio de {$campos[1]}: ", $pesos($campos[2]), "\n";
                break;
            case 'PEDIDO':
                $filas = $ventas->pedido($campos[1]);
                if ($filas === null) {
                    echo "No existe el pedido {$campos[1]}\n";
                    break;
                }
                echo "Pedido {$filas[0]['numero']} de {$filas[0]['cliente']}: total ", $pesos($filas[0]['total']), "\n";
                foreach ($filas as $f) {
                    echo "  {$f['cantidad']} × {$f['codigo']} a ", $pesos($f['precio']), "\n";
                }
                break;
            case 'REPORTE':
                foreach ($ventas->reporte() as $r) {
                    printf("  %s %2d u. %14s  stock %2d  %s\n", $r['codigo'], $r['unidades'], $pesos($r['facturado']), $r['stock'], $r['nombre']);
                }
                break;
        }
    } catch (DomainException | InvalidArgumentException $e) {
        echo "Compra de {$campos[1]}: ", $e->getMessage(), ". No se guardó nada.\n";
    }
}
```

### Prueba del sello

#### ¿Por qué el número de reclamo se arma en la misma transacción que el `INSERT`?

Para que no quede nunca un reclamo sin número: si algo falla entre el `INSERT` y el `UPDATE`, se deshacen los dos.

#### ¿Para qué se bloquean los productos siempre en el mismo orden?

Para evitar que dos compras simultáneas se traben esperándose una a la otra (un "abrazo mortal" o *deadlock*).

#### ¿Por qué el renglón del pedido guarda el precio?

Porque el precio del producto puede cambiar después: el pedido tiene que mostrar lo que se cobró en su momento.

#### ¿Qué tabla guarda la historia de los estados y por qué no alcanza con la columna `estado`?

`cambio_estado`: la columna solo dice el estado actual; la historia (quién, cuándo, de qué a qué) necesita su propia tabla.

#### ¿Cómo se incluyen en el reporte los productos que nunca se vendieron?

Con un `LEFT JOIN` desde `producto` y `COALESCE(SUM(...), 0)`.

### Soluciones (docente)

Jefe de la rama 4: los dos sistemas del jefe de la Oficina, llevados a MariaDB. La misión 1 es web (se prueba con `php -S localhost:8000 -t public`); la 2 es de terminal para concentrarse en las transacciones. Los hashes corresponden a `ancla123` (Ana), `faro2026` (Beto) y `timon77` (Ofelia). En la misión 2, la segunda compra falla por el poncho (piden 3, hay 2) y **no** descuenta el tapiz, que se vende en la tercera.

