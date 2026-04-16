"""
TRT App - Aplicación Principal
Punto de entrada para la interfaz gráfica de TRT-AntonioTRT_app
"""

import os
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QWidget
from ui.window import MainWindow
from controller import AppController
from config import APP_TITLE, get_trt_handler_instance


def _ensure_venv_and_reexec():
    """
    Verifica si se está ejecutando dentro de un venv.
    Si no, busca uno localmente y lo re-ejecuta.
    """
    in_venv = (
        hasattr(sys, "real_prefix") or
        (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix) or
        bool(os.environ.get("VIRTUAL_ENV"))
    )
    if in_venv:
        return

    # Buscar venv en la raíz del proyecto
    project_root = Path(__file__).parent.parent.parent
    venv_dirs = [
        project_root / ".venv",
        project_root / "venv",
    ]
    venv_dir = next((d for d in venv_dirs if d.is_dir()), None)
    if not venv_dir:
        return

    # Seleccionar intérprete dentro del venv
    if os.name == "nt":
        candidate = venv_dir / "Scripts" / "python.exe"
    else:
        candidate = venv_dir / "bin" / "python3"
        if not candidate.exists():
            candidate = venv_dir / "bin" / "python"

    if not candidate.exists():
        return

    # Re-ejecutar con python del venv si es diferente
    try:
        if Path(candidate).resolve() != Path(sys.executable).resolve():
            print(f"🔄 Re-ejecutando con venv: {candidate}")
            os.execv(str(candidate), [str(candidate)] + sys.argv)
    except Exception as e:
        print(f"⚠️  No se pudo re-ejecutar con venv: {e}")
        return


def main():
    """Función principal de la aplicación."""
    
    # Asegurar venv
    _ensure_venv_and_reexec()
    
    # Inicializar app Qt
    app = QApplication(sys.argv)
    
    # Crear ventana principal
    window = MainWindow()
    window.setWindowTitle(APP_TITLE)
    
    # Inicializar controlador
    controller = AppController(window)
    window.show()
    
    # Conectar señal de cierre
    app.aboutToQuit.connect(controller.close_serial)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
