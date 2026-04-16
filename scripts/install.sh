#!/bin/bash

###############################################################################
# TRT Installation Script - Instalá dependencias en Raspberry Pi
# Uso: ./scripts/install.sh
###############################################################################

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  TRT Installation Script                   ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
echo ""

# 1. Actualizar sistema
echo -e "${YELLOW}📦 Actualizando paquetes del sistema...${NC}"
sudo apt-get update
sudo apt-get upgrade -y

# 2. Instalar dependencias del sistema
echo -e "${YELLOW}📦 Instalando dependencias del sistema...${NC}"
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    python3-serial \
    git \
    curl \
    wget \
    build-essential

# 3. Instalar arduino-cli
echo -e "${YELLOW}🔧 Instalando arduino-cli...${NC}"

# Descargar e instalar arduino-cli
if command -v arduino-cli &> /dev/null; then
    echo -e "${GREEN}✓ arduino-cli ya está instalado${NC}"
else
    curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
    
    # Mover a /usr/local/bin para que esté en PATH
    if [ -f "$HOME/.local/bin/arduino-cli" ]; then
        sudo mv "$HOME/.local/bin/arduino-cli" /usr/local/bin/
    fi
    
    echo -e "${GREEN}✓ arduino-cli instalado${NC}"
fi

# 4. Instalar esptool (para ESP32)
echo -e "${YELLOW}🔧 Instalando esptool.py (ESP32)...${NC}"
pip3 install esptool

# 5. Crear entorno virtual
echo -e "${YELLOW}📦 Creando entorno virtual...${NC}"
cd "$PROJECT_ROOT"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}✓ Entorno virtual creado${NC}"
else
    echo -e "${GREEN}✓ Entorno virtual ya existe${NC}"
fi

# 6. Activar venv e instalar requisitos
echo -e "${YELLOW}📦 Instalando dependencias de Python...${NC}"
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r trtappUI/py/requirements.txt

# 7. Sincronizar configuración YAML (preserve local values)
echo -e "${YELLOW}⚙️  Sincronizando configuración...${NC}"

if command -v python3 &> /dev/null; then
    python3 "$PROJECT_ROOT/config/merge_config.py" || {
        echo -e "${YELLOW}⚠️  Fallback: Creando config manual${NC}"
        if [ ! -f "config/local_config.yaml" ]; then
            cp "config/default_config.yaml" "config/local_config.yaml"
        fi
    }
fi

if [ ! -f "config/local_config.yaml" ]; then
    echo -e "${RED}✗ ERROR: No se pudo crear config/local_config.yaml${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Configuración sincronizada${NC}"
echo "  Edita: $PROJECT_ROOT/config/local_config.yaml"

# 8. Hacer scripts ejecutables
echo -e "${YELLOW}🔐 Configurando permisos...${NC}"
chmod +x "$PROJECT_ROOT/scripts/deploy.sh"
chmod +x "$PROJECT_ROOT/scripts/autoupdate.sh"
chmod +x "$PROJECT_ROOT/scripts/install.sh"

# 9. Crear symlink para trtmsg (global)
echo -e "${YELLOW}🔗 Creando alias global 'trtmsg'...${NC}"

ALIAS_SCRIPT="/usr/local/bin/trtmsg"
if [ ! -f "$ALIAS_SCRIPT" ]; then
    sudo tee "$ALIAS_SCRIPT" > /dev/null << EOF
#!/bin/bash
cd "$PROJECT_ROOT"
source .venv/bin/activate
python3 -c "from core import get_trt_handler; h = get_trt_handler(); h.connect()" "\$@"
EOF
    sudo chmod +x "$ALIAS_SCRIPT"
    echo -e "${GREEN}✓ Alias 'trtmsg' creado (disponible globalmente)${NC}"
else
    echo -e "${GREEN}✓ Alias 'trtmsg' ya existe${NC}"
fi

# 10. Configurar systemd service (opcional)
echo -e "${YELLOW}⚙️  Configurando servicio systemd...${NC}"

SERVICE_FILE="/etc/systemd/system/trt_ui.service"
if [ ! -f "$SERVICE_FILE" ]; then
    cat > /tmp/trt_ui.service << EOF
[Unit]
Description=TRT App UI
After=network.target

[Service]
Type=simple
User=\$USER
WorkingDirectory=$PROJECT_ROOT
ExecStart=$PROJECT_ROOT/.venv/bin/python3 $PROJECT_ROOT/trtappUI/py/main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    echo "Para instalar el servicio, ejecuta:"
    echo "  sudo cp /tmp/trt_ui.service $SERVICE_FILE"
    echo "  sudo systemctl daemon-reload"
    echo "  sudo systemctl enable trt_ui.service"
    echo "  sudo systemctl start trt_ui.service"
else
    echo -e "${GREEN}✓ Servicio ya existe${NC}"
fi

# 11. Configurar crontab para autoupdate (opcional)
echo ""
echo -e "${YELLOW}⏰ Para configurar auto-actualizaciones${NC}"
echo "Edita tu crontab con: crontab -e"
echo "Y añade una de estas líneas:"
echo ""
echo "  # Verificar actualizaciones cada 5 minutos:"
echo "  */5 * * * * $PROJECT_ROOT/scripts/autoupdate.sh >> /tmp/trt_autoupdate.log 2>&1"
echo ""
echo "  # Verificar actualizaciones cada 10 minutos:"
echo "  */10 * * * * $PROJECT_ROOT/scripts/autoupdate.sh >> /tmp/trt_autoupdate.log 2>&1"
echo ""

# Verificación final
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✓ Instalación completada                 ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
echo ""
echo "Próximos pasos:"
echo "  1. Edita config/local_config.yaml"
echo "  2. Ejecuta: source .venv/bin/activate"
echo "  3. Corre la app: python3 trtappUI/py/main.py"
echo ""
