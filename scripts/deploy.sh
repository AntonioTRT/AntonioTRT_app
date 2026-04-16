#!/bin/bash

###############################################################################
# TRT Deployment Script - Flashea firmware en Arduino/ESP32
# Uso: ./scripts/deploy.sh [--board uno|esp32] [--port /dev/ttyUSB0]
###############################################################################

set -e  # Exit on error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuración por defecto
BOARD="uno"
SERIAL_PORT="/dev/ttyUSB0"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIRMWARE_DIR="$PROJECT_ROOT/firmware"

# Parsear argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --board)
            BOARD="$2"
            shift 2
            ;;
        --port)
            SERIAL_PORT="$2"
            shift 2
            ;;
        *)
            echo "Opción desconocida: $1"
            exit 1
            ;;
    esac
done

echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  TRT Deployment Script - Flashear Firmware ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
echo ""
echo -e "📋 Configuración:"
echo "  Board: $BOARD"
echo "  Puerto: $SERIAL_PORT"
echo "  Directorio: $FIRMWARE_DIR"
echo ""

# Verificar que arduino-cli está instalado
if ! command -v arduino-cli &> /dev/null; then
    echo -e "${RED}✗ Error: arduino-cli no está instalado${NC}"
    echo "  Instala con: curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh"
    exit 1
fi

echo -e "${YELLOW}🔧 Compilando firmware...${NC}"

case $BOARD in
    uno)
        FQBN="arduino:avr:uno"
        SKETCH_DIR="$FIRMWARE_DIR/arduino-uno"
        ;;
    esp32)
        FQBN="esp32:esp32:esp32"
        SKETCH_DIR="$FIRMWARE_DIR/esp32"
        ;;
    *)
        echo -e "${RED}✗ Error: Board no soportada: $BOARD${NC}"
        exit 1
        ;;
esac

# Actualizar cores si es necesario
arduino-cli core update-index
arduino-cli core install "$FQBN" || true

# Compilar
if [ -f "$SKETCH_DIR/sketch.ino" ]; then
    BUILD_DIR="/tmp/trt_build_$BOARD"
    mkdir -p "$BUILD_DIR"
    
    arduino-cli compile --fqbn "$FQBN" \
        "$SKETCH_DIR" \
        --output-dir "$BUILD_DIR" \
        --verbose
    
    echo -e "${GREEN}✓ Compilación exitosa${NC}"
    
    # Buscar archivo .hex o .bin compilado
    HEX_FILE=$(find "$BUILD_DIR" -name "*.hex" -o -name "*.bin" | head -1)
    
    if [ -z "$HEX_FILE" ]; then
        echo -e "${RED}✗ No se encontró archivo compilado (.hex o .bin)${NC}"
        exit 1
    fi
    
    echo ""
    echo -e "${YELLOW}⚡ Flasheando a puerto $SERIAL_PORT...${NC}"
    
    # Flashear según la placa
    case $BOARD in
        uno)
            # Usar avrdude (incluido con Arduino)
            avrdude -C/etc/avrdude.conf -v -p m328p -c arduino \
                -P "$SERIAL_PORT" -b 115200 -D \
                -U flash:w:"$HEX_FILE":i
            ;;
        esp32)
            # Usar esptool.py
            esptool.py --chip esp32 --port "$SERIAL_PORT" --baud 230400 \
                --before default_reset --after hard_reset write_flash \
                -z -fm keep -ff 40m 0x1000 "$BUILD_DIR"/bootloader.bin \
                0x8000 "$BUILD_DIR"/partition-table.bin \
                0x10000 "$HEX_FILE"
            ;;
    esac
    
    echo -e "${GREEN}✓ Firmware flasheado exitosamente${NC}"
else
    echo -e "${RED}✗ No se encontró sketch.ino en $SKETCH_DIR${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✓ Deployment completado                  ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
