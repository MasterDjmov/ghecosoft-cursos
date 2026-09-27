# Subir GhecoSoft-Code al servidor (Duplika · cPanel · servidor `mate`)

> **Estado (2026-09-27):** todavía **no** se subió. Primero se pulen detalles; la lista de pendientes está en [PLAN.md § 10](PLAN.md).

Guía paso a paso para el hosting compartido (CloudLinux, PHP 8.3, MariaDB, Node 20 por SSH).
La plataforma **no necesita** workers, colas, cron ni "Setup Python App": el código de los alumnos corre en su navegador.

> Convención: `~` es tu carpeta de usuario en el servidor (por ejemplo `/home/tuusuario`). La app vive **fuera** de `public_html`, y el dominio apunta a su carpeta `public/`.

---

## 1. Antes de empezar (una sola vez, en cPanel)

1. **PHP 8.3** en *Select PHP Version* (o *MultiPHP Manager*) para el dominio o subdominio.
2. **Extensiones de PHP** activadas (en *Select PHP Version → Extensions*):
   `bcmath`, `ctype`, `curl`, `dom`, `fileinfo`, `filter`, `gd`, `intl`, `mbstring`, `openssl`, `pdo`, `pdo_mysql`, `session`, `tokenizer`, `xml`, `zip`.
   Opcional: `opcache` (ya viene activa).
3. **Límites de PHP** (*Select PHP Version → Options*):
   - `upload_max_filesize` = **25M** y `post_max_size` = **30M** (los recursos de un nodo pesan hasta 20 MB; las entregas hasta 10 MB);
   - `memory_limit` = **256M**;
   - `max_execution_time` = **60**.
4. **Base de datos** (*MySQL Databases*):
   - crear la base, por ejemplo `tuusuario_ghecosoft`;
   - crear un usuario con una contraseña larga;
   - darle **todos los privilegios** sobre esa base.
5. **Dominio o subdominio** (*Domains*): por ejemplo `code.ghecosoft.com`, con **document root** `~/ghecosoft-code/public`.
   Si el panel no deja elegir esa carpeta, ver § 7.
6. **SSL**: que *SSL/TLS Status → AutoSSL* cubra el dominio. La app fuerza HTTPS en producción.
7. **Correo** (opcional pero recomendado): crear una casilla, por ejemplo `no-responder@ghecosoft.com`, para los avisos por mail.

## 2. Primera instalación (por SSH)

```bash
cd ~
git clone <URL-del-repositorio> ghecosoft-code
cd ghecosoft-code

# Dependencias de PHP sin las de desarrollo
composer install --no-dev --optimize-autoloader

# Assets (Tailwind, Livewire, árbol, editor). Node 20 ya está en el servidor.
npm ci
npm run build
```

> Si `npm` no está disponible por SSH, corré `npm ci && npm run build` en tu máquina y subí la carpeta `public/build/` completa.

## 3. Configuración (`.env`)

```bash
cp .env.example .env
php artisan key:generate
nano .env
```

Valores a cambiar:

| Clave | Valor |
|---|---|
| `APP_ENV` | `production` |
| `APP_DEBUG` | `false` (**nunca** `true` en el servidor: mostraría datos internos) |
| `APP_URL` | `https://code.ghecosoft.com` (con https) |
| `LOG_LEVEL` | `warning` |
| `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD` | los del paso 1.4 (`DB_HOST=localhost` suele funcionar mejor que `127.0.0.1` en cPanel) |
| `MAIL_MAILER` | `smtp` (o dejar `log` si no vas a mandar mails) |
| `MAIL_HOST` / `MAIL_PORT` / `MAIL_SCHEME` | `mail.ghecosoft.com` / `465` / `smtps` (según cPanel → *Connect Devices*) |
| `MAIL_USERNAME` / `MAIL_PASSWORD` | la casilla del paso 1.7 |
| `MAIL_FROM_ADDRESS` | la misma casilla |
| `QUEUE_CONNECTION` | `sync` (dejarlo así: no hay workers) |
| `PYODIDE_URL` | dejar el de `.env.example` (Python 3.13 desde jsDelivr) |

Los avisos siempre aparecen en la campanita; por mail salen solo si `MAIL_MAILER=smtp` y hay un host real.

## 4. Base de datos, admin y permisos

```bash
php artisan migrate --force
php artisan db:seed --class=ProductionSeeder --force   # configuración, moneda comodín y niveles
php artisan app:create-admin                           # tu usuario docente (clave fuerte)
php artisan storage:link                               # logos, íconos e insignias

# Opcional: el curso demo de Python como punto de partida (sin usuarios de prueba)
php artisan db:seed --class=PythonDemoCourseSeeder --force

# Caché de configuración, rutas y vistas (más rápido)
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Permisos de escritura
chmod -R ug+rwX storage bootstrap/cache
```

⚠️ **No correr** `php artisan db:seed` a secas ni `migrate:fresh` en el servidor: crea los usuarios de prueba (`admin/admin123`, `cliente/cliente123`) o borra todo. En producción, `migrate:fresh` está bloqueado a propósito.

## 5. Revisar que quedó bien

1. Entrar a `https://code.ghecosoft.com` → aparece el login con el geco.
2. Entrar con el admin creado en el paso 4 → *Configuración*: cargar tu **WhatsApp** y el mensaje.
3. `https://code.ghecosoft.com/.env` tiene que dar **404** (si se ve algo, el document root está mal: ver § 7).
4. `https://code.ghecosoft.com/storage/` no tiene que listar archivos. Los comprobantes, entregas, recursos y autorizaciones **no** están ahí: van a `storage/app/private` y solo se bajan con permiso.
5. Registrar un alumno de prueba, pedir inscripción, aprobarla, abrir la clase 0 y tocar **Ejecutar** en el ejemplo. La primera vez tarda unos segundos porque descarga Python.

## 6. Actualizar a una versión nueva

```bash
cd ~/ghecosoft-code
php artisan down                      # pantalla de mantenimiento
git pull
composer install --no-dev --optimize-autoloader
npm ci && npm run build
php artisan migrate --force
php artisan optimize:clear
php artisan config:cache && php artisan route:cache && php artisan view:cache
php artisan up
```

## 7. Si el panel no deja apuntar el dominio a `public/`

Dejá la app en `~/ghecosoft-code` y reemplazá `public_html` (o la carpeta del subdominio) por un enlace a `public/`:

```bash
mv ~/public_html ~/public_html.bak      # solo si está vacío o no se usa
ln -s ~/ghecosoft-code/public ~/public_html
```

**Nunca** copies todo el proyecto dentro de `public_html`: quedaría expuesto el `.env` con las claves.

## 8. Copias de seguridad

Lo que no se puede perder:

- **La base de datos**: cPanel → *Backup* → *Download a MySQL Database Backup*, o por SSH:
  ```bash
  mysqldump -u USUARIO -p BASE > ~/backups/ghecosoft-$(date +%F).sql
  ```
- **`storage/app/private`**: comprobantes, entregas, recursos y autorizaciones.
- **`storage/app/public`**: logos, íconos e insignias.
- **`.env`**: guardalo en un lugar seguro, fuera del servidor.

Recomendado: una copia por semana, más una antes de cada actualización.

## 9. Problemas comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| Error 500 en blanco | Permisos o `.env` | `tail -50 storage/logs/laravel.log`; revisar `chmod` del paso 4 |
| La página se ve sin estilos | No se compilaron los assets | `npm run build` (o subir `public/build/`) |
| No se ven logos ni insignias | Falta el enlace | `php artisan storage:link` |
| "413" o "El archivo es muy grande" | Límites de PHP | Subir `upload_max_filesize` y `post_max_size` (paso 1.3) |
| "Ejecutar" no responde | El navegador no llega a jsDelivr | Probar con otra red; se puede cambiar `PYODIDE_URL` |
| No llegan mails | SMTP | Revisar `MAIL_*`; los avisos igual se ven en la campanita |
| Cambié el `.env` y no toma | Caché de configuración | `php artisan config:cache` |
