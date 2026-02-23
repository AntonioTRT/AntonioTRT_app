# AntonioTRT App - Qt GUI para Raspberry Pi

Aplicacion Qt minimalista con interfaz grafica (GUI) para ejecutarse en Raspberry Pi o Windows.

## Caracteristicas

Ventana pantalla completa  
Texto "hola" centrado  
Barra de menus (File, Edit, Help)  
Estructura escalable y organizada  
Entorno virtual (venv) auto-activable  

## Instalacion (primera vez)

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar (Windows)
venv\Scripts\activate
# O en Linux/RPi
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecucion

### Opcion 1: Tarea VS Code (Recomendado)
Presiona **Ctrl+Shift+B** desde VS Code

### Opcion 2: Batch (Windows)
```cmd
run_app.bat
```

### Opcion 3: PowerShell (Windows)
```powershell
.\run_app.ps1
```

### Opcion 4: Terminal manual
```bash
python main.py
```

### Opcion 5: Raspberry Pi
```bash
python3 main.py
```

## Estructura del Proyecto

```
.
 app/
    __init__.py          # Exporta MainWindow
    window.py            # Interfaz principal (QMainWindow)
    controller.py        # Logica de la aplicacion
 main.py                  # Punto de entrada (auto-activa venv)
 requirements.txt         # Dependencias (PySide6)
 .vscode/tasks.json       # Tareas de VS Code
 run_app.bat              # Script ejecutable (Windows)
 run_app.ps1              # Script PowerShell (Windows)
 README.md                # Este archivo
```

## Desarrollo

- **Interfaz:** Editar app/window.py (MainWindow)
- **Logica:** Agregar metodos en app/controller.py
- **Menus:** Expandir en _create_menu() (window.py)

## Notas

- El main.py detecta automaticamente el venv y lo activa (util en RPi)
- Presiona Esc o usa File / Exit para cerrar
- Compatible con Python 3.8+
