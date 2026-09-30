#!/usr/bin/env bash
# Actualiza producción (docs/DEPLOY.md § 6).
# El hosting no puede compilar los assets (CloudLinux corta los hilos de Vite),
# así que se compilan acá y se sube public/build/ por SSH.
#
#   scripts/deploy.sh            # código + assets + migraciones (+ public/toolchains si cambió)
#   scripts/deploy.sh --cursos   # además reimporta cursos/python, cursos/c, cursos/cpp, cursos/java y cursos/php
#
# Requiere el alias "ghecosoft-prod" en ~/.ssh/config (o DEPLOY_HOST=...).
set -euo pipefail

HOST="${DEPLOY_HOST:-ghecosoft-prod}"
APP_DIR="${DEPLOY_DIR:-gamificado.lariojaclick.ar}"
URL="${DEPLOY_URL:-https://gamificado.lariojaclick.ar}"
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

# 2. Assets en esta compu.
npm run build

# 3. Código, dependencias y migraciones en el servidor (con pantalla de mantenimiento).
ssh "$HOST" bash -s <<EOF
set -euo pipefail
cd ~/$APP_DIR
php artisan down --retry=30 || true
git pull --ff-only
composer install --no-dev --optimize-autoloader --no-interaction
php artisan migrate --force
EOF

# 4. public/build: se sube a una carpeta nueva y se reemplaza de una vez.
tar czf - -C public build | ssh "$HOST" "cd ~/$APP_DIR/public && rm -rf build.new && mkdir build.new && tar xzf - -C build.new --strip-components=1 && rm -rf build && mv build.new build"

# 4b. public/toolchains (compilador de C/C++ para corregir en el navegador, D66): se arma con
#     scripts/build-cpp-toolchain.sh y se sube solo si cambió (pesa ~20 MB).
if [[ -d public/toolchains ]]; then
    LOCAL_SUM=$(cd public && find toolchains -type f | sort | xargs sha1sum | sha1sum | cut -d' ' -f1)
    REMOTE_SUM=$(ssh "$HOST" "cat ~/$APP_DIR/public/toolchains/.sum 2>/dev/null || true")
    if [[ "$LOCAL_SUM" != "$REMOTE_SUM" ]]; then
        echo "→ Subiendo public/toolchains…"
        tar czf - -C public toolchains | ssh "$HOST" "cd ~/$APP_DIR/public && rm -rf toolchains.new && mkdir toolchains.new && tar xzf - -C toolchains.new --strip-components=1 && echo $LOCAL_SUM > toolchains.new/.sum && rm -rf toolchains && mv toolchains.new toolchains"
    fi
else
    echo "(Sin public/toolchains: C/C++ no se va a poder ejecutar al corregir. Correlo con scripts/build-cpp-toolchain.sh.)"
fi

# 5. Cursos (opcional), caché y salir del mantenimiento.
ssh "$HOST" bash -s <<EOF
set -euo pipefail
cd ~/$APP_DIR
if [[ $CURSOS == 1 ]]; then
    for c in cursos/python/ cursos/c/ cursos/cpp/ cursos/java/ cursos/php/; do php artisan app:import-course "\$c" --apply; done
fi
php artisan optimize:clear
php artisan config:cache
php artisan route:cache
php artisan view:cache
php artisan up
git log --oneline -1
EOF

code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 30 "$URL/")
echo "$URL → $code"
[[ "$code" == 200 ]]
