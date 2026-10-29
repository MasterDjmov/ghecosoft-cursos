# Plan ante una filtración de datos (D113)

Qué hacer si alguien entró donde no debía, se perdió una copia o un dato de alumnos quedó a la vista. La Privacidad (§ 7) promete avisar a los alumnos y contarles qué pasó: este plan lo cumple. Es una guía técnica, no asesoramiento legal.

## 1. Cortar (la primera hora)
- `php artisan down` en el servidor, o *Admin → Configuración → Mantenimiento* si la plataforma responde (D86).
- Cerrar todas las sesiones: `php artisan tinker --execute="DB::table('sessions')->truncate()"` (las sesiones están en la base).
- Cambiar las claves, empezando por la que pudo haberse filtrado:
  - cPanel y SSH (y sacar las llaves SSH que no reconozcas en *cPanel → SSH Access*);
  - el usuario de MariaDB (cPanel → *Bases de datos*) y después `DB_PASSWORD` en el `.env` del servidor;
  - la clave de aplicación de Gmail (`MAIL_PASSWORD`);
  - la cuenta de administrador de la plataforma.
- `APP_KEY`: cambiarla **solo si se filtró el `.env`**. Con ella están cifrados el doble factor y el código del CV: pasá la vieja a `APP_PREVIOUS_KEYS` para que se sigan leyendo, y recién después generá la nueva (`php artisan key:generate --show`).

## 2. Evaluar (el primer día)
- **Qué se vio:** ¿la base entera, una tabla, archivos de `storage/app/private` (comprobantes, entregas, autorizaciones), una copia de `scripts/backup.sh`?
- **De quiénes:** cuántos alumnos y cuántos menores. La fecha de nacimiento y las autorizaciones de *Admin → Autorizaciones* dicen quién es menor.
- **Desde cuándo:** `storage/logs/laravel.log`, el registro de accesos de cPanel (*Métricas → Errores* y *Raw Access*) y `session_evictions` (IP y navegador de cada cierre de sesión).
- **Cómo:** arreglar la causa antes de levantar la plataforma (actualizar, cerrar el agujero, sacar el archivo público).
- Si hace falta, comparar con la última copia buena (`scripts/pull-backups.sh` las trae a la compu, DEPLOY.md § 8).

## 3. Avisar (dentro de las 72 horas, si hay datos personales en juego)
- **A los alumnos afectados** y, si son menores, a su adulto responsable: un aviso en la campanita (y por mail a quien tiene email) con qué pasó, qué datos, qué hicimos y qué conviene que hagan (cambiar la clave, prestar atención a mails raros). Sin culpas ni tecnicismos.
- **A la AAIP:** la Ley 25.326 no obliga hoy a notificar, pero la Agencia lo recomienda (Res. 47/2018) y es la autoridad de control. Si se filtraron datos de muchos alumnos o de menores, conviene avisarle por su mesa de entradas digital.
- Si hubo un delito (alguien entró a propósito), hacer la denuncia en la Unidad Fiscal de Ciberdelitos o en la comisaría, con lo que se juntó en el paso 2.

## 4. Anotar
Al terminar, agregar una entrada abajo: fecha, qué pasó, qué datos, cuántos alumnos, a quiénes se avisó y qué se cambió para que no vuelva a pasar.

## Registro de incidentes
_(sin incidentes)_
