#!/usr/bin/env bash
# Copia de seguridad de producción (docs/DEPLOY.md § 8): la base y los archivos subidos.
# Corre en el servidor: todos los días desde Cron Jobs de cPanel y antes de cada scripts/deploy.sh.
#
#   bash ~/gamificado.lariojaclick.ar/scripts/backup.sh
#
# Deja en ~/backups/ghecosoft (fuera de la web):
#   db-AAAA-MM-DD_HHMM.sql.gz        la base entera (mysqldump)
#   archivos-AAAA-MM-DD_HHMM.tar.gz  storage/app/private (comprobantes, entregas, apuntes, autorizaciones)
#                                    y storage/app/public (logos, íconos, insignias)
# y borra los de más de BACKUP_DAYS días (14 por defecto). Lo que pasa se anota en backup.log;
# si algo falla, sale con error (cPanel manda el aviso por mail si tiene una casilla configurada).
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${BACKUP_DIR:-$HOME/backups/ghecosoft}"
DAYS="${BACKUP_DAYS:-14}"
STAMP="$(date +%F_%H%M)"

mkdir -p "$DEST"
chmod 700 "$DEST"
log() { echo "$(date '+%F %T') $*" >> "$DEST/backup.log"; }

# Datos de la base, del .env (con o sin comillas).
env_value() {
    local value
    value="$(grep -E "^$1=" "$APP_DIR/.env" | tail -1 | cut -d= -f2-)"
    value="${value%$'\r'}"
    [[ "$value" =~ ^\"(.*)\"$ || "$value" =~ ^\'(.*)\'$ ]] && value="${BASH_REMATCH[1]}"
    printf '%s' "$value"
}
DB_HOST="$(env_value DB_HOST)"
DB_PORT="$(env_value DB_PORT)"
DB_DATABASE="$(env_value DB_DATABASE)"
DB_USERNAME="$(env_value DB_USERNAME)"
DB_PASSWORD="$(env_value DB_PASSWORD)"

# La clave va en un archivo temporal que solo lee el usuario, nunca en la línea de comandos.
CNF="$(mktemp "$DEST/.my.cnf.XXXXXX")"
DB_FILE="$DEST/db-$STAMP.sql.gz"
FILES_FILE="$DEST/archivos-$STAMP.tar.gz"
cleanup() { rm -f "$CNF"; }
fail() {
    log "ERROR: $1"
    rm -f "$DB_FILE" "$FILES_FILE"
    echo "Copia de seguridad fallida: $1 (detalle en $DEST/backup.log)" >&2
    exit 1
}
trap cleanup EXIT
chmod 600 "$CNF"
escaped="${DB_PASSWORD//\\/\\\\}"
escaped="${escaped//\"/\\\"}"
printf '[client]\nuser="%s"\npassword="%s"\nhost="%s"\nport="%s"\n' \
    "$DB_USERNAME" "$escaped" "${DB_HOST:-127.0.0.1}" "${DB_PORT:-3306}" > "$CNF"

# 1. La base: una foto consistente sin bloquear las tablas (InnoDB).
mysqldump --defaults-extra-file="$CNF" --single-transaction --quick --routines --triggers \
    --default-character-set=utf8mb4 --no-tablespaces "$DB_DATABASE" 2>> "$DEST/backup.log" \
    | gzip -9 > "$DB_FILE" || fail "no se pudo copiar la base $DB_DATABASE"
gzip -t "$DB_FILE" || fail "la copia de la base quedó dañada"

# 2. Los archivos subidos.
tar czf "$FILES_FILE" --exclude=private/livewire-tmp -C "$APP_DIR/storage/app" private public 2>> "$DEST/backup.log" \
    || fail "no se pudieron copiar los archivos de storage/app"

chmod 600 "$DB_FILE" "$FILES_FILE"

# 3. Rotación: se quedan los últimos DAYS días.
find "$DEST" -maxdepth 1 -type f \( -name 'db-*.sql.gz' -o -name 'archivos-*.tar.gz' \) -mtime +"$DAYS" -delete

log "OK base $(du -h "$DB_FILE" | cut -f1), archivos $(du -h "$FILES_FILE" | cut -f1)"
