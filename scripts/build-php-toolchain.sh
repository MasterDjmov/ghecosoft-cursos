#!/usr/bin/env bash
# Arma el ejecutor de PHP para correr entregas en el navegador del docente (D68):
#   public/toolchains/php/php-<versión>.wasm.gz  → PHP 8.3 en WebAssembly (asyncify), de @php-wasm/web-8-3
# El cargador JS va en el build (Vite); el .wasm no, para que no se suba en cada deploy.
# Uso: scripts/build-php-toolchain.sh   (después de npm install; una vez, o al cambiar la versión de @php-wasm/web-8-3;
#      resources/js/runners/php-config.js tiene la misma versión)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION=$(sed -n "s/^export const PHP_VERSION = '\(.*\)';/\1/p" "$ROOT/resources/js/runners/php-config.js")
MINOR="${VERSION%.*}"
SRC="$ROOT/node_modules/@php-wasm/web-8-3/asyncify/${VERSION//./_}/php_${MINOR//./_}.wasm"
OUT="$ROOT/public/toolchains/php"

if [[ ! -f "$SRC" ]]; then
    echo "No está $SRC: corré npm install (o revisá que php-config.js y @php-wasm/web-8-3 tengan la misma versión)." >&2
    exit 1
fi

mkdir -p "$OUT"
rm -f "$OUT"/php-*.wasm.gz
gzip -9 -n -c "$SRC" > "$OUT/php-$VERSION.wasm.gz"
ls -la "$OUT"
