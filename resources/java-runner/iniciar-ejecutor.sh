#!/bin/sh
# Ejecutor de Java de GhecoSoft-Code (Linux y Mac). Dejalo abierto mientras uses la plataforma.
cd "$(dirname "$0")" || exit 1
if ! command -v java >/dev/null 2>&1; then
    echo "No encontré Java. Instalá el JDK 21:"
    echo "  Ubuntu/Debian: sudo apt install openjdk-21-jdk"
    echo "  Otros: https://adoptium.net (Temurin 21 LTS)"
    exit 1
fi
exec java JavaRunner.java
