#!/bin/bash

###############################################################################
# TRT Auto-Update Watcher Script
# Monitorea cambios en remoto y auto-actualiza Raspberry Pi
# Se ejecuta periódicamente via crontab
#
# Instalación en crontab (ejecutar cada 5 minutos):
#   */5 * * * * /home/pi/ruta/scripts/autoupdate.sh >> /tmp/trt_autoupdate.log 2>&1
#
# O cada 10 minutos:
#   */10 * * * * /home/pi/ruta/scripts/autoupdate.sh >> /tmp/trt_autoupdate.log 2>&1
###############################################################################

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuración
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_FILE="/tmp/trt_autoupdate.log"
LOCK_FILE="/tmp/trt_autoupdate.lock"
CONFIG_FILE="$PROJECT_ROOT/config/local_config.yaml"
SERVICE_NAME="trt_ui.service"

# Funciones
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_section() {
    echo "" | tee -a "$LOG_FILE"
    log "${BLUE}=== $1 ===${NC}"
}

error() {
    log "${RED}✗ ERROR: $1${NC}"
}

success() {
    log "${GREEN}✓ $1${NC}"
}

# Prevenir ejecución concurrente
if [ -f "$LOCK_FILE" ]; then
    LOCK_PID=$(cat "$LOCK_FILE")
    if ps -p "$LOCK_PID" > /dev/null 2>&1; then
        log "⏭️  Ya se está ejecutando una actualización (PID: $LOCK_PID)"
        exit 0
    else
        rm -f "$LOCK_FILE"
    fi
fi

echo $$ > "$LOCK_FILE"
trap "rm -f $LOCK_FILE" EXIT

log_section "Iniciando búsqueda de actualizaciones"

# 1. Navegar al proyecto
if [ ! -d "$PROJECT_ROOT" ]; then
    error "Directorio de proyecto no encontrado: $PROJECT_ROOT"
    exit 1
fi

cd "$PROJECT_ROOT"
success "Ubicación: $PROJECT_ROOT"

# 2. Verificar conexión git
log_section "Verificando repositorio git"

if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    error "No se está dentro de un repositorio git"
    exit 1
fi

# 3. Ejecutar git fetch
log "Obteniendo información del repositorio remoto..."
if ! git fetch --quiet; then
    error "No se pudo hacer fetch del repositorio"
    exit 1
fi
success "Git fetch completado"

# 4. Comparar versiones local vs remota
log_section "Comparando versiones"

LOCAL_COMMIT=$(git rev-parse HEAD)
REMOTE_COMMIT=$(git rev-parse origin/main 2>/dev/null || echo "")

if [ -z "$REMOTE_COMMIT" ]; then
    log "⚠️  No se puede acceder a origin/main"
    exit 0
fi

log "Commit local:  ${LOCAL_COMMIT:0:8}"
log "Commit remoto: ${REMOTE_COMMIT:0:8}"

if [ "$LOCAL_COMMIT" = "$REMOTE_COMMIT" ]; then
    log "✓ Ya está actualizado"
    exit 0
fi

# 5. Detectar si hay cambios en firmware/
log_section "Analizando cambios"

GIT_DIFF=$(git diff HEAD origin/main --name-only 2>/dev/null || echo "")
FIRMWARE_CHANGED=false

if echo "$GIT_DIFF" | grep -q "^firmware/"; then
    FIRMWARE_CHANGED=true
    log "🔴 Cambios detectados en firmware"
fi

if echo "$GIT_DIFF" | grep -q "^core/"; then
    log "🟡 Cambios detectados en core/"
fi

if echo "$GIT_DIFF" | grep -q "^trtappUI/"; then
    log "🟡 Cambios detectados en trtappUI/"
fi

# 6. Ejecutar git pull
log_section "Descargando actualizaciones"

log "Ejecutando: git pull --recurse-submodules"
if ! git pull --recurse-submodules; then
    error "No se pudo hacer pull de los cambios"
    exit 1
fi
success "Git pull completado"

# 6.5. Sincronizar configuración (preservar valores locales)
log_section "Sincronizando configuración"

if command -v python3 &> /dev/null; then
    if [ -f "config/merge_config.py" ]; then
        python3 config/merge_config.py --quiet
        success "Configuración sincronizada (valores locales preservados)"
    fi
fi

# 7. Actualizar dependencias Python si hay cambios
if echo "$GIT_DIFF" | grep -q "requirements.txt"; then
    log_section "Actualizando dependencias Python"
    
    if [ -f "requirements.txt" ]; then
        if command -v pip3 &> /dev/null; then
            pip3 install -r requirements.txt --quiet
            success "Dependencias Python actualizadas"
        fi
    fi
    
    if [ -f "trtappUI/py/requirements.txt" ]; then
        if command -v pip3 &> /dev/null; then
            pip3 install -r trtappUI/py/requirements.txt --quiet
            success "Dependencias UI actualizadas"
        fi
    fi
fi

# 8. Flashear firmware si hubo cambios
if [ "$FIRMWARE_CHANGED" = true ]; then
    log_section "Flasheando nuevo firmware"
    
    # Leer configuración local
    if [ -f "$CONFIG_FILE" ]; then
        BOARD_TYPE=$(grep "board_type:" "$CONFIG_FILE" | awk '{print $2}')
        SERIAL_PORT=$(grep "serial_port:" "$CONFIG_FILE" | awk '{print $2}' | tr -d '"')
    else
        BOARD_TYPE="uno"
        SERIAL_PORT="/dev/ttyUSB0"
    fi
    
    log "Board type: $BOARD_TYPE"
    log "Serial port: $SERIAL_PORT"
    
    if bash "$PROJECT_ROOT/scripts/deploy.sh" --board "$BOARD_TYPE" --port "$SERIAL_PORT"; then
        success "Firmware flasheado exitosamente"
    else
        error "No se pudo flashear el firmware (continuando...)"
    fi
fi

# 9. Reiniciar servicio UI
log_section "Reiniciando servicio"

if systemctl is-active --quiet "$SERVICE_NAME" 2>/dev/null; then
    log "Reiniciando: $SERVICE_NAME"
    if sudo systemctl restart "$SERVICE_NAME" 2>/dev/null; then
        success "Servicio reiniciado"
    else
        error "No se pudo reiniciar el servicio (permiso denegado)"
    fi
else
    log "ℹ️  Servicio $SERVICE_NAME no está activo"
fi

# 10. Resumen final
log_section "Actualización completada"
log "${GREEN}✓ Sistema actualizado a ${REMOTE_COMMIT:0:8}${NC}"

# Limpiar logs antiguos (más de 30 días)
find /tmp/trt_autoupdate.log* -mtime +30 -delete 2>/dev/null || true

exit 0
