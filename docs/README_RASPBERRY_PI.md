Proyecto Qt minimal para Raspberry Pi

## Estructura

- `app/` — código de la aplicación (`MainWindow`, controladores, etc.)
- `main.py` — entrada de la aplicación
- `requirements.txt` — dependencias
- `run_app.bat` / `run_app.ps1` — scripts para ejecutar (Windows)
- `.vscode/tasks.json` — tareas configuradas en VS Code

## Instalación (Windows / RPi)

**Primera vez:**
```bash
python3 -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

### Opción 1: Tarea VS Code (recomendado)
Presiona `Ctrl+Shift+B` (ejecuta la tarea por defecto "Run App").

### Opción 2: Script batch (Windows)
```cmd
run_app.bat
```

### Opción 3: Script PowerShell (Windows)
```powershell
.\run_app.ps1
```

### Opción 4: Terminal manual
```bash
python3 main.py
# O con venv activado: python main.py
```

### Opción 5: Raspberry Pi
```bash
cd /path/to/AntonioTRT_app
python3 main.py
```
El script detecta y activa automáticamente el `venv` si existe.

## Notas

- La ventana abre en **pantalla completa** y muestra "hola" centrado.
- Barra de menús: `File`, `Edit`, `Help` (placeholder para expandir).
- Para ampliar: editar `app/window.py` y lógica en `app/controller.py`.
- El `venv` no es un contenedor Docker — es un entorno virtual aislado de Python que no se ejecuta automáticamente.
