# La compu del docente: qué hay instalado y cómo restaurarla

Todo lo que se configuró **fuera del proyecto** en la compu del docente (Linux Mint), para volver a dejarla igual si se reinstala o se cambia de compu. Actualizado el 2026-10-01.

## Lo que NO está en el repositorio (guardalo aparte)

Esto no se sube a GitHub. Guardalo en un pendrive, en la nube personal o en un gestor de claves:

- **`~/.ssh/`** entera: la clave `id_ed25519` (con su `.pub`) y el archivo `config`. Con esa clave se entra al servidor y a GitHub.
- **`.env`** del proyecto local (y el de producción, que está en el servidor).
- **Los datos del servidor** para el alias `ghecosoft-prod`: IP, puerto SSH y usuario. Si los perdés, están en cPanel → *SSH Access* o te los da el hosting.
- **Las copias de seguridad** que trae `scripts/pull-backups.sh` a `~/Respaldos/ghecosoft`.

## Restaurar, paso a paso

### 1. Programas

```bash
sudo apt install git curl mariadb-server php8.4 php8.4-{cli,mysql,mbstring,xml,curl,zip,gd,intl,bcmath} \
    gcc g++ python3 openjdk-17-jdk rsync
```

- **PHP 8.3** además del 8.4 (`php8.3`): lo usa el súper test de PHP para correr como el hosting. Viene del PPA de Ondřej Surý (`sudo add-apt-repository ppa:ondrej/php`).
- **Node 20** y **Composer 2**: desde sus sitios oficiales (Node con `nvm` o el repositorio de NodeSource).

### 2. Las claves SSH

Copiá tu `~/.ssh` guardada y ajustá los permisos:

```bash
chmod 700 ~/.ssh && chmod 600 ~/.ssh/id_ed25519 ~/.ssh/config
```

Si no tenés el `config`, el bloque del servidor es este (completá los datos):

```
Host ghecosoft-prod
    HostName IP_DEL_SERVIDOR
    Port PUERTO_SSH
    User USUARIO_DE_CPANEL
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

Probalo con `ssh ghecosoft-prod`. Con una clave nueva, hay que autorizarla otra vez en cPanel (*SSH Access*) y en GitHub.

### 3. El proyecto

```bash
git clone git@github.com:MasterDjmov/ghecosoft-cursos.git /var/www/html/larioja-aprende-cursos
cd /var/www/html/larioja-aprende-cursos
cp /donde/lo/guardaste/.env .env        # o: cp .env.example .env && php artisan key:generate
composer install
npm ci
php artisan migrate:fresh --seed        # base local de prueba (o restaurá una copia)
php artisan storage:link
npm run build
scripts/build-cpp-toolchain.sh          # ejecutar C/C++ al corregir (D66)
scripts/build-php-toolchain.sh          # ejecutar PHP al corregir (D68)
```

La base de los tests (`ghecosoft_code_testing`) se crea vacía en MariaDB; `php artisan test` la llena sola.

### 4. El ejecutor de Java (arranca solo)

Para que *Ejecutar* ande en las entregas de Java (D69), el ejecutor corre de fondo como servicio de usuario y arranca con la sesión:

```bash
scripts/compu-docente/instalar-javarunner.sh
```

Instala `javarunner.service` (el de esta carpeta) en `~/.config/systemd/user/`.

En Chrome, la página de la plataforma necesita dos permisos (ícono a la izquierda de la dirección → *Configuración del sitio*): **Red local** y **Aplicaciones en el dispositivo**. Y **ninguna extensión que toque CORS** (como *CORS Unblock*) activa en esa pestaña: cambian el origen del pedido y el ejecutor lo rechaza. Cada pedido queda anotado en `journalctl --user -u javarunner`.

Comandos útiles:

```bash
systemctl --user status javarunner          # ¿está andando?
systemctl --user restart javarunner         # si Ejecutar deja de andar
systemctl --user disable --now javarunner   # sacarlo del arranque
```

### 5. Las copias de seguridad

- **En el servidor** corren solas todos los días (cPanel → *Cron Jobs*, a las 4:30) y antes de cada deploy. Eso está en el servidor: no hay que tocar nada al cambiar de compu. Ver [docs/DEPLOY.md § 8](../../docs/DEPLOY.md).
- **En la compu**, cada tanto: `scripts/pull-backups.sh` trae las copias a `~/Respaldos/ghecosoft`.

### 6. Comprobar que todo anda

```bash
php artisan test                         # la suite
php artisan app:course-tests cursos/cpp  # compiladores y pruebas de los cursos
ssh ghecosoft-prod 'echo ok'             # acceso al servidor
curl -s http://127.0.0.1:17017/ping -H "Origin: https://gamificado.lariojaclick.ar"   # ejecutor de Java
```

## Otros scripts

- [`scripts/pruebas/`](../pruebas/README.md): ayudantes para escribir las `#### Pruebas` de un curso (D73).
- `scripts/deploy.sh`, `scripts/backup.sh`, `scripts/pull-backups.sh` y los `build-*-toolchain.sh`: ver CLAUDE.md.
