#!/usr/bin/env bash
# Arma el toolchain de C++ para ejecutar entregas en el navegador del docente (D66):
#   public/toolchains/cpp/sysroot-<wasi>.tar.gz  → la biblioteca estándar de wasi-sdk CON excepciones (headers + libs)
#   public/toolchains/cpp/comun-<clang>.pch.gz    → encabezado precompilado con los #include de siempre (compila ~3x más rápido)
# Clang (YoWASP, WebAssembly) se descarga del CDN en el navegador: acá solo se usa para generar el PCH.
# Uso: scripts/build-cpp-toolchain.sh   (una vez, o al cambiar las versiones; resources/js/runners/cpp-config.js tiene las mismas)
set -euo pipefail

WASI_SDK=34
YOWASP_CLANG=22.0.0-git20542-10
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/public/toolchains/cpp"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo "→ Bajando el sysroot de wasi-sdk-$WASI_SDK…"
curl -sSL -o "$WORK/sysroot.tar.gz" "https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-$WASI_SDK/wasi-sysroot-$WASI_SDK.0.tar.gz"
tar xzf "$WORK/sysroot.tar.gz" -C "$WORK" "wasi-sysroot-$WASI_SDK.0/include/wasm32-wasip1" "wasi-sysroot-$WASI_SDK.0/lib/wasm32-wasip1"
SRC="$WORK/wasi-sysroot-$WASI_SDK.0"

echo "→ Armando el subconjunto (C++ con excepciones)…"
SUB="$WORK/sub"
mkdir -p "$SUB/include" "$SUB/lib/wasm32-wasip1/eh"
rsync -a --exclude noeh "$SRC/include/wasm32-wasip1" "$SUB/include/"
cp "$SRC"/lib/wasm32-wasip1/{crt1-command.o,crt1.o,libc.a,libm.a} "$SUB/lib/wasm32-wasip1/"
cp "$SRC"/lib/wasm32-wasip1/eh/{libc++.a,libc++abi.a,libunwind.a} "$SUB/lib/wasm32-wasip1/eh/"

mkdir -p "$OUT"
rm -f "$OUT"/sysroot-*.tar.gz "$OUT"/comun-*.pch*
tar czf "$OUT/sysroot-$WASI_SDK.tar.gz" -C "$SUB" .

echo "→ Generando el encabezado precompilado con clang $YOWASP_CLANG (baja ~105 MB la primera vez)…"
(cd "$WORK" && npm init -y >/dev/null && npm install --silent "@yowasp/clang@$YOWASP_CLANG" >/dev/null)
cp "$ROOT/resources/js/runners/cpp-comun.hpp" "$WORK/comun.hpp"
cat > "$WORK/pch.mjs" <<'JS'
import { runClang } from '@yowasp/clang';
import fs from 'node:fs';
import path from 'node:path';
const tree = (dir) => Object.fromEntries(fs.readdirSync(dir, { withFileTypes: true })
    .map((e) => [e.name, e.isDirectory() ? tree(path.join(dir, e.name)) : fs.readFileSync(path.join(dir, e.name))]));
const flags = JSON.parse(process.argv[2]);
const out = await runClang(['clang++', ...flags, '-x', 'c++-header', 'comun.hpp', '-o', 'comun.pch'],
    { sysroot: tree('sub'), 'comun.hpp': fs.readFileSync('comun.hpp') });
fs.writeFileSync(process.argv[3], out['comun.pch']);
JS
FLAGS=$(node -e "import('$ROOT/resources/js/runners/cpp-config.js').then(m => console.log(JSON.stringify(m.COMPILE_FLAGS)))")
(cd "$WORK" && node pch.mjs "$FLAGS" "$WORK/comun.pch" 2>&1 | grep -v "fetched\|ExperimentalWarning\|trace-warnings" || true)
gzip -9 -c "$WORK/comun.pch" > "$OUT/comun-$YOWASP_CLANG.pch.gz"

ls -lh "$OUT"
echo "✓ Listo. Se sube con scripts/deploy.sh (sube public/toolchains si cambió)."
