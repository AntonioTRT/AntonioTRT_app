import os
import sys
from PySide6.QtWidgets import QApplication
from app.window import MainWindow


def _ensure_venv_and_reexec():
    # If running inside a virtualenv already, do nothing
    in_venv = (
        hasattr(sys, "real_prefix") or
        (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix) or
        bool(os.environ.get("VIRTUAL_ENV"))
    )
    if in_venv:
        return

    # Locate a local venv directory next to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(script_dir, "venv")
    if not os.path.isdir(venv_dir):
        return

    # Choose the interpreter inside the venv
    if os.name == "nt":
        candidate = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        candidate = os.path.join(venv_dir, "bin", "python3")
        if not os.path.exists(candidate):
            candidate = os.path.join(venv_dir, "bin", "python")

    if not os.path.exists(candidate):
        return

    # Re-exec with the venv python if it's different
    try:
        if os.path.realpath(candidate) != os.path.realpath(sys.executable):
            print(f"Activando venv y re-ejecutando con: {candidate}")
            os.execv(candidate, [candidate] + sys.argv)
    except Exception:
        # If re-exec fails, continue with current interpreter
        return


_ensure_venv_and_reexec()


# Entry point for the application
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    # controller = AppController(window)  # hook for future logic
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
