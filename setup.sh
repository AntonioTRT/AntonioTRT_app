#!/bin/bash
# Script de configuración para AntonioTRT_app en Raspberry Pi
# Activa el entorno virtual, instala dependencias y verifica configuración

set -e  # Salir si hay error
 
echo "=== Configuración del entorno de AntonioTRT_app ==="
 
# 1. Verificar si python3-venv está instalado
if ! python3 -c "import venv" &> /dev/null; then
    echo "El paquete python3-venv no está instalado. Intentando instalar..."
    if sudo apt-get update -y && sudo apt-get install -y python3-venv; then
        echo "✓ python3-venv instalado correctamente."
    else
        echo "Error: No se pudo instalar python3-venv. Por favor, instálalo manualmente con 'sudo apt-get install python3-venv' y vuelve a ejecutar este script." >&2
        exit 1
    fi
fi
 
# 2. Verificar directorio del proyecto
if [ ! -f "requirements.txt" ]; then
    echo "Error: Ejecuta este script desde la raíz del proyecto (AntonioTRT_app/)"
    exit 1
fi

# 3. Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv .venv
fi
 
# 4. Activar entorno virtual
echo "Activando entorno virtual..."
source .venv/bin/activate
echo "Entorno virtual activado."
 
# Añadir el directorio de scripts al PATH para el subshell actual
# Esto es crucial para que el comando 'trtmsg' sea encontrado durante la verificación.
export PATH="$PATH:$(pwd)/scripts"

# Asegurarse de que el script trtmsg sea ejecutable
chmod +x scripts/trtmsg

# Asegurarse de que el wrapper trtmsg (sin extensión) en la raíz sea ejecutable
chmod +x trtmsg

# 5. Instalar dependencias
echo "Instalando dependencias desde requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt --quiet
 
# 6. Verificar dependencias
echo "Verificando dependencias..."
if python -c "import PySide6, serial, yaml" &> /dev/null; then
    echo "✓ Todas las dependencias principales están instaladas."
else
    echo "✗ Error: Faltan dependencias principales."
    exit 1
fi
 
# 7. Sincronizar configuración (crear local_config.yaml si no existe)
echo "Sincronizando configuración..."
CONFIG_DIR="$(pwd)/config"
DEFAULT_CONFIG="$CONFIG_DIR/default_config.yaml"
LOCAL_CONFIG="$CONFIG_DIR/local_config.yaml"
 
if [ ! -f "$LOCAL_CONFIG" ]; then
    if [ -f "$DEFAULT_CONFIG" ]; then
        cp "$DEFAULT_CONFIG" "$LOCAL_CONFIG"
        echo "✓ Creado $LOCAL_CONFIG a partir del default."
    fi
fi

# 8. Verificar que trtmsg funciona
echo "Verificando trtmsg..."
if ./trtmsg version > /dev/null 2>&1; then # Ahora 'trtmsg' (sin extensión) debería ser ejecutable
    echo "✓ El comando trtmsg funciona correctamente."
else
    echo "✗ Error: El comando trtmsg no funciona."
    exit 1
fi
echo ""
echo "=== Configuración completada ==="
echo "El entorno virtual está activo en esta terminal."
echo ""
echo "Para futuras sesiones, solo necesitas ejecutar:"
echo "  cd $(pwd)"
echo "  source .venv/bin/activate  # Y opcionalmente: export PATH=\"\$PATH:$(pwd)/scripts\" para usar 'trtmsg' directamente"
echo ""
echo "Comandos disponibles:"
echo "  trtmsg help"
echo "  trtmsg devices"
echo "  python3 trtappUI/py/main.py  # Para la interfaz Qt"

echo ""
echo "---"
echo "💡 Consejo de uso:"
echo "Para usar 'trtmsg' sin escribir './trtmsg', puedes añadir un alias a tu shell."
echo "Ejecuta esto una sola vez:"
echo ""
echo "echo \"alias trtmsg='$(pwd)/trtmsg'\" >> ~/.bashrc && source ~/.bashrc"
echo ""
echo "Después de eso, podrás usar 'trtmsg' desde cualquier lugar en futuras sesiones."