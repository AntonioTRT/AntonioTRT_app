#!/bin/bash
# Script de configuración para AntonioTRT_app en Raspberry Pi
# Activa el entorno virtual, instala dependencias y verifica configuración

set -e  # Salir si hay error

echo "=== Configuración de AntonioTRT_app ==="

# Verificar si estamos en el directorio correcto
if [ ! -f "requirements.txt" ]; then
    echo "Error: Ejecuta este script desde la raíz del proyecto (AntonioTRT_app/)"
    exit 1
fi

# Verificar/crear entorno virtual
if [ ! -d ".venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv .venv
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source .venv/bin/activate

# Verificar Python
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Verificar instalación
echo "Verificando instalación..."
python -c "import PySide6, serial, yaml; print('Todas las dependencias instaladas correctamente')"

# Agregar scripts al PATH temporalmente
export PATH="$PATH:$(pwd)/scripts"

# Verificar trtmsg
echo "Verificando trtmsg..."
if ./scripts/trtmsg version > /dev/null 2>&1; then
    echo "trtmsg funciona correctamente"
else
    echo "Error: trtmsg no funciona"
    exit 1
fi

echo ""
echo "=== Configuración completada ==="
echo "Entorno virtual activado. Para futuras sesiones:"
echo "  cd AntonioTRT_app"
echo "  source .venv/bin/activate"
echo "  export PATH=\"\$PATH:$(pwd)/scripts\""
echo ""
echo "Comandos disponibles:"
echo "  trtmsg help"
echo "  trtmsg devices"
echo "  ./trtappUI/py/main.py  # Para la interfaz Qt"