#!/usr/bin/env bash
# Actualiza producción (docs/DEPLOY.md § 6) sin cortar la plataforma: la pantalla de mantenimiento (503) sale
# solo si hay migraciones nuevas o cambian las dependencias de composer, y solo mientras se aplican (segundos).
# El hosting no puede compilar los assets (CloudLinux corta los hilos de Vite),
# así que se compilan acá y se sube public/build/ por SSH.
#
#   scripts/deploy.sh            # código + assets + migraciones (+ public/toolchains si cambió)
#   scripts/deploy.sh --cursos   # además reimporta cursos/python, cursos/c, cursos/cpp, cursos/java, cursos/php, cursos/html, las Crónicas en Inglés (cursos/ingles-primaria, cursos/ingles-secundaria) Ensamblador (cursos/ensamblador), C# (cursos/csharp), JavaScript (cursos/javascript) y TypeScript (cursos/typescript)
#
# El orden importa para que nadie vea un error mientras sube:
#   1. public/build y public/toolchains primero, sin borrar los archivos de la versión anterior (Vite les pone
#      un nombre distinto en cada versión): la página que ya está abierta sigue encontrando los suyos.
#   2. Después el código (git), y el mantenimiento solo si hace falta.
#   3. Los cursos se reimportan con la plataforma abierta: cada curso entra en una sola transacción
#      (CourseImporter), así que un alumno ve el curso viejo o el nuevo, nunca uno a medias.
#
# Requiere el alias "ghecosoft-prod" en ~/.ssh/config (o DEPLOY_HOST=...).
# DEPLOY_SSH reemplaza al comando ssh (solo para probar el script en la compu; ver docs/DEPLOY.md § 6).
set -euo pipefail

HOST="${DEPLOY_HOST:-ghecosoft-prod}"
APP_DIR="${DEPLOY_DIR:-gamificado.lariojaclick.ar}"
URL="${DEPLOY_URL:-https://gamificado.lariojaclick.ar}"
SSH="${DEPLOY_SSH:-ssh}"
CURSOS=0
[[ "${1:-}" == "--cursos" ]] && CURSOS=1

cd "$(dirname "$0")/.."

# 1. Solo se sube lo que ya está en GitHub.
if [[ -n "$(git status --porcelain)" ]]; then
    echo "Hay cambios sin commitear. Commiteá (y pusheá) antes de subir." >&2
    exit 1
fi
git fetch -q origin
if [[ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]]; then
    echo "main local y origin/main no coinciden. Hacé git push (o git pull) antes de subir." >&2
    exit 1
fi

# public/toolchains se sube entero: sin la parte de C/C++ se borraría del servidor.
if [[ ! -d public/toolchains/cpp ]]; then
    echo "Falta public/toolchains/cpp (ejecutar C/C++ al corregir). Corré scripts/build-cpp-toolchain.sh antes de subir." >&2
    exit 1
fi

if [[ ! -d public/toolchains/csharp ]]; then
    echo "Falta public/toolchains/csharp (ejecutar C# en el navegador). Corré scripts/build-csharp-toolchain.sh antes de subir." >&2
    exit 1
fi

# 2. Assets en esta compu (y PHP en WebAssembly para corregir, D68: sale de node_modules).
npm run build
scripts/build-php-toolchain.sh >/dev/null
node scripts/build-typescript-toolchain.mjs >/dev/null

# 3. public/build: se arma en una carpeta nueva con lo recién compilado MÁS los assets de la versión anterior
#    (los de más de 3 días que ya no usa el manifest se borran), y se cambia de una vez.
echo "→ Subiendo public/build…"
tar czf - -C public build | $SSH "$HOST" "set -e; cd ~/$APP_DIR/public && rm -rf build.new build.old && mkdir build.new && tar xzf - -C build.new --strip-components=1 \
    && if [ -d build/assets ]; then cp -pn build/assets/* build.new/assets/ 2>/dev/null || true; \
         for f in build.new/assets/*; do n=\$(basename \"\$f\"); grep -q \"\$n\" build.new/manifest.json || find \"\$f\" -mtime +3 -delete; done; fi \
    && if [ -d build ]; then mv build build.old; fi && mv build.new build && rm -rf build.old"

# 3b. public/toolchains (ejecutores en el navegador: C/C++ D66, PHP D68, C# D119, TypeScript D115): C/C++ y C# se arman con
#     scripts/build-cpp-toolchain.sh y scripts/build-csharp-toolchain.sh (PHP, en el paso 2); se sube solo si cambió (pesa ~27 MB).
LOCAL_SUM=$(cd public && find toolchains -type f | sort | xargs -r sha1sum | sha1sum | cut -d' ' -f1)
REMOTE_SUM=$($SSH "$HOST" "cat ~/$APP_DIR/public/toolchains/.sum 2>/dev/null || true")
if [[ "$LOCAL_SUM" != "$REMOTE_SUM" ]]; then
    echo "→ Subiendo public/toolchains…"
    tar czf - -C public toolchains | $SSH "$HOST" "set -e; cd ~/$APP_DIR/public && rm -rf toolchains.new toolchains.old && mkdir toolchains.new && tar xzf - -C toolchains.new --strip-components=1 && echo $LOCAL_SUM > toolchains.new/.sum && if [ -d toolchains ]; then mv toolchains toolchains.old; fi && mv toolchains.new toolchains && rm -rf toolchains.old"
fi

# 4. Código, dependencias, migraciones, cursos y caché en el servidor.
$SSH "$HOST" bash -s <<EOF
set -euo pipefail
cd ~/$APP_DIR
git fetch -q origin
CHANGED=\$(git diff --name-only HEAD origin/main)

# ¿Hace falta cerrar? Solo si hay migraciones nuevas (o pendientes de antes) o cambian las dependencias.
DOWN=0
if grep -qE '^(database/migrations/|composer\.(json|lock)$)' <<< "\$CHANGED"; then DOWN=1; fi
if ! php artisan migrate:status --pending=1 >/dev/null 2>&1; then DOWN=1; fi

bash scripts/backup.sh   # copia de la base y los archivos antes de tocar nada (DEPLOY.md § 8)

if [[ \$DOWN == 1 ]]; then
    echo "→ Hay migraciones o dependencias nuevas: pantalla de mantenimiento mientras se aplican."
    php artisan down --retry=15 || true
else
    echo "→ Sin migraciones ni dependencias nuevas: se actualiza en vivo."
fi

git merge -q --ff-only origin/main
if grep -qE '^composer\.(json|lock)$' <<< "\$CHANGED"; then
    composer install --no-dev --optimize-autoloader --no-interaction
fi
php artisan migrate --force
php artisan optimize:clear
php artisan config:cache
php artisan route:cache
if [[ \$DOWN == 1 ]]; then php artisan up; fi

# Lo que sigue no necesita la plataforma cerrada (las vistas que alguien pida antes se compilan solas).
php artisan view:cache
php artisan app:game-items   # ítems de ejemplo del juego que falten (D90; no toca los existentes)
php artisan app:prune-access-logs   # IP y navegador de más de 12 meses (D113, Privacidad § 6)
if [[ $CURSOS == 1 ]]; then
    for c in cursos/python/ cursos/c/ cursos/cpp/ cursos/java/ cursos/php/ cursos/html/ cursos/ingles-primaria/ cursos/ingles-secundaria/ cursos/ensamblador/ cursos/csharp/ cursos/javascript/ cursos/typescript/; do php artisan app:import-course "\$c" --apply; done
fi
git log --oneline -1
EOF

code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 30 "$URL/")
echo "$URL → $code"
[[ "$code" == 200 ]]
