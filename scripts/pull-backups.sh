#!/usr/bin/env bash
# Trae a esta compu las copias de seguridad del servidor (docs/DEPLOY.md § 8). Una copia que vive
# solo en el servidor no sirve si se pierde el servidor: correr esto cada tanto (por ejemplo, una vez por semana).
#
#   scripts/pull-backups.sh            # a ~/Respaldos/ghecosoft (o BACKUP_LOCAL=...)
#
# Requiere el alias "ghecosoft-prod" en ~/.ssh/config (o DEPLOY_HOST=...). Solo agrega: no borra nada acá.
set -euo pipefail

HOST="${DEPLOY_HOST:-ghecosoft-prod}"
LOCAL="${BACKUP_LOCAL:-$HOME/Respaldos/ghecosoft}"

mkdir -p "$LOCAL"
chmod 700 "$LOCAL"
# El servidor no tiene rsync: se piden por ssh + tar solo las copias que todavía no están acá.
missing=()
while IFS= read -r name; do
    [[ -n "$name" && ! -f "$LOCAL/$name" ]] && missing+=("$name")
done < <(ssh "$HOST" 'cd backups/ghecosoft && ls -1 db-*.sql.gz archivos-*.tar.gz 2>/dev/null')
if (( ${#missing[@]} )); then
    ssh "$HOST" "cd backups/ghecosoft && tar cf - ${missing[*]} backup.log" | tar xf - -C "$LOCAL"
    echo "Traje ${#missing[@]} archivo(s)."
else
    echo "No hay copias nuevas."
fi
echo "Copias en $LOCAL:"
ls -1t "$LOCAL" | grep -v backup.log | head -6
