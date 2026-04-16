"""
Configuración de la aplicación TRT UI
Carga configuración desde YAML centralizado
"""

import sys
import os
from pathlib import Path

# Detectar raíz del proyecto
def get_project_root():
    """Retorna la ruta raíz del proyecto (donde está este script)"""
    current = Path(__file__).parent.parent.parent
    return current

PROJECT_ROOT = get_project_root()
sys.path.insert(0, str(PROJECT_ROOT))

# Importar handler de configuración
from core import get_trt_handler

# Inicializar handler TRT
_trt_handler = get_trt_handler()
_board_info = _trt_handler.get_board_info()

# Configuración compatibilidad con código antiguo
SERIAL_PORT = _board_info.get("port", "/dev/ttyUSB0")
BAUDRATE = int(_board_info.get("baudrate", 9600))
APP_TITLE = "TRT App - " + _board_info.get("pi_name", "RaspberryPi")

# Ruta a archivos UI
UI_DIR = os.path.join(os.path.dirname(__file__), "ui")
VENTANA_UI = os.path.join(UI_DIR, "ventana.ui")
ABOUT_UI = os.path.join(UI_DIR, "about.ui")

def get_trt_handler_instance():
    """Obtiene instancia del handler TRT para usar en la app."""
    return _trt_handler
