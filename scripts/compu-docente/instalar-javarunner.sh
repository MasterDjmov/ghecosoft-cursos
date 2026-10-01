#!/usr/bin/env bash
# Deja el ejecutor de Java (D69) corriendo de fondo y arrancando solo con la sesión del docente
# (servicio de usuario de systemd). Correrlo una vez, desde la carpeta del proyecto ya clonada.
#
#   scripts/compu-docente/instalar-javarunner.sh
#
# Para sacarlo:  systemctl --user disable --now javarunner
set -euo pipefail

PROYECTO="$(cd "$(dirname "$0")/../.." && pwd)"
command -v java >/dev/null || { echo "Falta Java 17 o más: sudo apt install openjdk-17-jdk" >&2; exit 1; }

mkdir -p ~/.config/systemd/user
# El .service del repo apunta a /var/www/html/larioja-aprende-cursos: se ajusta si el proyecto está en otro lado.
sed "s|^WorkingDirectory=.*|WorkingDirectory=$PROYECTO|" "$PROYECTO/scripts/compu-docente/javarunner.service" > ~/.config/systemd/user/javarunner.service
systemctl --user daemon-reload
systemctl --user enable --now javarunner.service
sleep 5
systemctl --user --no-pager status javarunner.service | sed -n 1,4p
