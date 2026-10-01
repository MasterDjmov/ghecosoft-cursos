# Subir GhecoSoft-Code al servidor (Duplika · cPanel · servidor `mate`)

> **Estado (2026-09-28):** **subido.** `https://gamificado.lariojaclick.ar` (subdominio de cPanel detrás de **Cloudflare**).
>
> - La app vive en `~/gamificado.lariojaclick.ar` (clonada ahí) y el **document root** del subdominio apunta a `gamificado.lariojaclick.ar/public`.
> - Repositorio: `git@github.com:MasterDjmov/ghecosoft-cursos.git`. El servidor lo lee con la deploy key `~/.ssh/ghecosoft_code` y el alias `github-ghecosoft_code` (§ 2).
> - Base: `lariojac_code_cursos`. Cursos importados: Python, C, C++, Java y PHP.
> - Para actualizar: `scripts/deploy.sh` desde la compu (§ 6). En el servidor **no** se compilan los assets.

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
5. **Dominio o subdominio** (*Domains*): `gamificado.lariojaclick.ar` (ya creado), con **document root** `gamificado.lariojaclick.ar/public` (la carpeta donde se clona el repo).
   Si el panel no deja elegir esa carpeta, ver § 7.
6. **SSL**: que *SSL/TLS Status → AutoSSL* cubra el dominio. La app fuerza HTTPS en producción.
7. **Correo** (opcional pero recomendado): crear una casilla, por ejemplo `no-responder@lariojaclick.ar`, para los avisos por mail.

## 2. Primera instalación (por SSH)

Antes, una sola vez: que el servidor pueda leer el repo de GitHub por SSH. Con un nombre y un alias propios, para no pisar otras claves del servidor:

```bash
ssh-keygen -t ed25519 -C "servidor-mate-ghecosoft_code" -f ~/.ssh/ghecosoft_code -N ""
cat ~/.ssh/ghecosoft_code.pub
```

Esa clave pública se carga en GitHub → repo *ghecosoft-cursos* → *Settings → Deploy keys* (solo lectura). Después:

```bash
cat >> ~/.ssh/config <<'CFG'

Host github-ghecosoft_code
    HostName github.com
    User git
    IdentityFile ~/.ssh/ghecosoft_code
    IdentitiesOnly yes
CFG
chmod 600 ~/.ssh/config
ssh -T git@github-ghecosoft_code    # tiene que saludar con el nombre del repo
```

Si el hosting bloquea el puerto 22 hacia afuera, usar `HostName ssh.github.com` y `Port 443` en ese mismo bloque.

La carpeta del subdominio ya existe (con archivos ocultos de cPanel), así que en vez de `git clone` se arma el repo en el lugar, y el document root se apunta a su `public/` **antes** de crear el `.env`:

```bash
cd ~/gamificado.lariojaclick.ar
rm index.html                        # la página de prueba
git init -b main
git remote add origin git@github-ghecosoft_code:MasterDjmov/ghecosoft-cursos.git
git fetch origin
git checkout -t origin/main

# Dependencias de PHP sin las de desarrollo
composer install --no-dev --optimize-autoloader

# Assets (Tailwind, Livewire, árbol, editor). Node 20 ya está en el servidor.
npm ci
npm run build
```

> En `mate`, `npm run build` **falla** (CloudLinux limita los hilos). Compilá en tu máquina y subí `public/build/` completa; `scripts/deploy.sh` lo hace (§ 6).

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
| `APP_URL` | `https://gamificado.lariojaclick.ar` (con https) |
| `LOG_LEVEL` | `warning` |
| `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD` | los del paso 1.4 (`DB_HOST=localhost` suele funcionar mejor que `127.0.0.1` en cPanel) |
| `MAIL_MAILER` | `smtp` (o dejar `log` si no vas a mandar mails) |
| `MAIL_HOST` / `MAIL_PORT` / `MAIL_SCHEME` | `mail.lariojaclick.ar` / `465` / `smtps` (según cPanel → *Connect Devices*) |
| `MAIL_USERNAME` / `MAIL_PASSWORD` | la casilla del paso 1.7 |
| `MAIL_FROM_ADDRESS` | la misma casilla |
| `QUEUE_CONNECTION` | `sync` (dejarlo así: no hay workers) |
| `PYODIDE_URL` | dejar el de `.env.example` (Python 3.13 desde jsDelivr) |
| `TRUSTED_PROXIES` | `cloudflare` (la IP real del alumno para los límites de intentos; ver § 9) |
| `SESSION_SECURE_COOKIE` | `true` (la cookie de sesión viaja solo por HTTPS) |

Los avisos siempre aparecen en la campanita; por mail salen solo si `MAIL_MAILER=smtp` y hay un host real.

## 4. Base de datos, admin y permisos

```bash
php artisan migrate --force
php artisan db:seed --class=ProductionSeeder --force   # configuración, moneda comodín y niveles
php artisan app:create-admin                           # tu usuario docente (clave fuerte)
php artisan storage:link                               # logos, íconos e insignias

# Los cursos (cursos/python/, cursos/c/, cursos/cpp/, cursos/java/, cursos/php/): igual que Admin → Cursos → Importar (sin usuarios de prueba)
php artisan app:import-course cursos/python/ --apply
php artisan app:import-course cursos/c/ --apply
php artisan app:import-course cursos/cpp/ --apply
php artisan app:import-course cursos/java/ --apply
php artisan app:import-course cursos/php/ --apply

# Ejecutores para corregir en el navegador: C/C++ (D66) se arma en la compu con
# scripts/build-cpp-toolchain.sh; PHP (D68) lo arma scripts/deploy.sh desde node_modules
# (scripts/build-php-toolchain.sh). deploy.sh sube public/toolchains/ cuando cambia.

# Caché de configuración, rutas y vistas (más rápido)
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Permisos de escritura
chmod -R ug+rwX storage bootstrap/cache
```

⚠️ **No correr** `php artisan db:seed` a secas ni `migrate:fresh` en el servidor: crea los usuarios de prueba (`admin/admin123`, `cliente/cliente123`) o borra todo. En producción, `migrate:fresh` está bloqueado a propósito.

## 5. Revisar que quedó bien

1. Entrar a `https://gamificado.lariojaclick.ar` → aparece el login con el geco.
2. Entrar con el admin creado en el paso 4 → *Configuración*: cargar tu **WhatsApp** y el mensaje.
3. `https://gamificado.lariojaclick.ar/.env` tiene que dar **404** (si se ve algo, el document root está mal: ver § 7).
4. `https://gamificado.lariojaclick.ar/storage/` no tiene que listar archivos. Los comprobantes, entregas, recursos y autorizaciones **no** están ahí: van a `storage/app/private` y solo se bajan con permiso.
5. Registrar un alumno de prueba, pedir inscripción, aprobarla, abrir la clase 0 y tocar **Ejecutar** en el ejemplo. La primera vez tarda unos segundos porque descarga Python.

## 6. Actualizar a una versión nueva

**En el servidor `mate` no se puede compilar** (`npm run build` se corta con `OS can't spawn worker thread`: CloudLinux limita los hilos). Los assets se compilan en la compu del docente y se sube `public/build/`. Todo eso lo hace un script, desde la compu:

```bash
git push                      # el servidor baja de GitHub
scripts/deploy.sh             # build local + git pull, composer, migraciones, public/build y caché
scripts/deploy.sh --cursos    # además reimporta los cursos de cursos/
```

Necesita en `~/.ssh/config` de la compu un alias `ghecosoft-prod` (HostName, Port 4444, User `lariojac`, la clave autorizada en el servidor). El servidor lee el repo con su propia deploy key, por el alias `github-ghecosoft_code` de su `~/.ssh/config`.

A mano (si el servidor pudiera compilar):

```bash
cd ~/gamificado.lariojaclick.ar
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

Lo que no se puede perder: **la base de datos**, **`storage/app/private`** (comprobantes, entregas, recursos y autorizaciones) y **`storage/app/public`** (logos, íconos e insignias). Además, el **`.env`**: guardalo en un lugar seguro, fuera del servidor.

`scripts/backup.sh` (corre en el servidor) copia la base (`mysqldump`, sin bloquear las tablas) y los archivos subidos a `~/backups/ghecosoft/`, fuera de la web, y borra los de más de 14 días. Anota cada copia en `~/backups/ghecosoft/backup.log` y, si falla, sale con error.

- **Todos los días**, desde cPanel → *Cron Jobs* → *Añadir nuevo trabajo de cron*: minuto `30`, hora `4`, día `*`, mes `*`, día de la semana `*`, y como comando:
  ```bash
  /bin/bash /home/lariojac/gamificado.lariojaclick.ar/scripts/backup.sh
  ```
  No escribe nada si sale bien; si falla, cPanel manda el error al mail configurado arriba de esa pantalla (*Correo electrónico de cron*).
- **Antes de cada actualización**: `scripts/deploy.sh` la corre sola, antes de las migraciones.
- **Fuera del servidor**: desde la compu del docente, `scripts/pull-backups.sh` trae a `~/Respaldos/ghecosoft` las copias que todavía no tiene (una vez por semana, por ejemplo). Sin esto, si se pierde el servidor se pierden también las copias.

Para restaurar (con cuidado: pisa la base):
```bash
gunzip -c ~/backups/ghecosoft/db-AAAA-MM-DD_HHMM.sql.gz | mysql -u USUARIO -p BASE
tar xzf ~/backups/ghecosoft/archivos-AAAA-MM-DD_HHMM.tar.gz -C ~/gamificado.lariojaclick.ar/storage/app
```

## 9. Cloudflare y el subdominio `gamificado.lariojaclick.ar`

El subdominio pasa por Cloudflare (proxy naranja). Al subir el proyecto:

1. **Borrar el `index.html` de prueba** de la carpeta del subdominio. Apache prefiere `index.html` a `index.php`: si queda, tapa la app. Después, apuntar el document root a `gamificado.lariojaclick.ar/public` (o el enlace del § 7).
2. **SSL en Cloudflare: *Full (strict)*** (*SSL/TLS → Overview*). Con *Flexible*, Cloudflare le habla al servidor por HTTP, la app redirige a HTTPS y queda un bucle de redirecciones. AutoSSL de cPanel da el certificado del servidor.
3. **Confiar en el proxy de Cloudflare**: `TRUSTED_PROXIES=cloudflare` en el `.env`. Sin eso, Laravel ve la IP de Cloudflare en vez de la del alumno (los límites de intentos del login y de entregas se comparten entre todos) y no detecta bien el HTTPS. Los rangos están en `config/security.php` (revisar de vez en cuando https://www.cloudflare.com/ips/).
4. **Nada de caché de HTML ni optimizaciones que tocan el JS**: en Cloudflare, *Rocket Loader* apagado (rompe Livewire y Alpine) y sin reglas de *Cache Everything* para las páginas. Cachear `/build/*` sí está bien: los archivos llevan hash.
5. **Límite de subida**: el plan gratis de Cloudflare acepta hasta 100 MB por pedido; nuestros archivos son de 25 MB como máximo, así que no molesta.
6. Si se ve algo raro después de actualizar, *Caching → Purge Everything* en Cloudflare.

## 10. Problemas comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| Error 500 en blanco | Permisos o `.env` | `tail -50 storage/logs/laravel.log`; revisar `chmod` del paso 4 |
| La página se ve sin estilos | No se compilaron los assets | `npm run build` (o subir `public/build/`) |
| No se ven logos ni insignias | Falta el enlace | `php artisan storage:link` |
| "413" o "El archivo es muy grande" | Límites de PHP | Subir `upload_max_filesize` y `post_max_size` (paso 1.3) |
| "Ejecutar" no responde | El navegador no llega a jsDelivr | Probar con otra red; se puede cambiar `PYODIDE_URL` |
| No llegan mails | SMTP | Revisar `MAIL_*`; los avisos igual se ven en la campanita |
| "Too many redirects" | Cloudflare en SSL *Flexible* | Pasar a *Full (strict)* (§ 9) |
| Se ve la página de prueba | Quedó el `index.html` | Borrarlo (§ 9) |
| Botones que no responden, errores de Alpine | *Rocket Loader* de Cloudflare | Apagarlo (§ 9) |
| Cambié el `.env` y no toma | Caché de configuración | `php artisan config:cache` |
