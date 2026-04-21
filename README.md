TRT MasterControl

Este es el cerebro central para controlar mis Raspberry Pi (B, 4 y 5). Con esta app puedo manejar ventiladores, pantallas LCD y sensores usando Arduinos y ESP32 de forma organizada y sin complicaciones.

Que hace este proyecto?

Control Total: Una interfaz visual para manejar el hardware.
Multi-Placa: Funciona igual si conectas un Arduino o un ESP32.
Auto-Update: Las Raspberries se actualizan solas cuando subo cambios a GitHub.
Seguro: Diseñado para no quemar los pines usando transistores para la potencia.

Como esta organizado?

trtappUI/: La aplicacion que ves en pantalla.
core/: El motor que envia los mensajes (trtmsg).
firmware/: El codigo que se carga en el Arduino o ESP32.
config/: Los ajustes de cada Raspberry (nombre, puerto, etc.).
scripts/: Herramientas para instalar y actualizar todo con un clic.
docs/: Documentación adicional.

## Instalación en Raspberry Pi

1. Clona el repositorio:
   ```bash
   git clone https://github.com/AntonioTRT/AntonioTRT_app
   cd AntonioTRT_app
   ```

2. Ejecuta el script de configuración (activa venv e instala dependencias):
   ```bash
   ./setup.sh
   ```

3. El script verificará todo y dejará el entorno listo. Para futuras sesiones:
   ```bash
   cd AntonioTRT_app
   source .venv/bin/activate
   export PATH="$PATH:$(pwd)/scripts"
   ```

Como funciona trtmsg?

trtmsg es el sistema nervioso del proyecto. Funciona como un traductor universal: la Raspberry Pi envia una instruccion simple y el script se encarga de abrir el puerto correcto, gestionar la conexion y entregar el mensaje al microcontrolador de forma segura y sin reiniciar la placa.

El Concepto: Arduino como Puente

La filosofia de este proyecto es que el Arduino es solamente un puente.

Todo el control nace en la Raspberry Pi: la logica, las decisiones y la inteligencia viven en los scripts de Python. El microcontrolador no toma decisiones propias; se limita a escuchar lo que la Pi le ordena y aplicarlo a los pines fisicos, como escribir en la LCD o dar potencia al ventilador. Al tratar al microcontrolador como un simple puente, puedes cambiar de hardware facilmente sin tener que reprogramar la aplicacion principal.

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
