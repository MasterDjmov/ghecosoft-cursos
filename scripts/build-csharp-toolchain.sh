#!/usr/bin/env bash
# Arma el ejecutor de C# para el navegador (el compilador Roslyn y el runtime de .NET en WebAssembly):
#   public/toolchains/csharp/_framework/…  (los .wasm van solo comprimidos: los descomprime el worker)
# Uso: scripts/build-csharp-toolchain.sh   (una vez, o al cambiar scripts/csharp-runner/). Necesita el SDK de .NET 10.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/scripts/csharp-runner"
BUILD="${TMPDIR:-/tmp}/csharp-runner-build"
OUT="$ROOT/public/toolchains/csharp"
export DOTNET_NOLOGO=1 DOTNET_CLI_TELEMETRY_OPTOUT=1

mkdir -p "$BUILD"
dotnet publish "$SRC/CsharpRunner.csproj" -c Release -o "$BUILD/out" -p:BaseIntermediateOutputPath="$BUILD/obj/" -p:BaseOutputPath="$BUILD/bin/" --nologo -v q

mkdir -p "$OUT.new/_framework"
cd "$BUILD/out/wwwroot/_framework"
for file in *; do
    case "$file" in
        *.gz|*.br) ;;
        *.wasm|*.dat) gzip -9 -n -c "$file" > "$OUT.new/_framework/$file.gz" ;;
        *) [[ -f "$file" ]] && cp "$file" "$OUT.new/_framework/" ;;
    esac
done
for folder in */; do
    [[ -d "$folder" ]] || continue
    mkdir -p "$OUT.new/_framework/$folder"
    for file in "$folder"*; do
        case "$file" in *.gz|*.br) ;; *) gzip -9 -n -c "$file" > "$OUT.new/_framework/$file.gz" ;; esac
    done
done
rm -rf "$OUT"
mv "$OUT.new" "$OUT"
du -sh "$OUT"
