# 🎨 TRT App UI - Interfaz Gráfica

Interfaz gráfica de usuario para TRT-AntonioTRT_app basada en **PySide6 (Qt6 para Python)**.

## Estructura

```
trtappUI/
├── py/
│   ├── main.py              # Punto de entrada
│   ├── config.py            # Carga configuración YAML
│   ├── controller.py        # Lógica de la aplicación
│   ├── requirements.txt     # Dependencias Python
│   └── ui/
│       ├── __init__.py
│       ├── window.py        # Ventana principal (Qt)
│       ├── ventana.ui       # Interfaz Qt Designer
│       └── about.ui         # Ventana "About"
└── README.md (este archivo)
```

## Requisitos

- **Python 3.9+**
- **PySide6** (Qt 6 para Python)
- **pyserial** (comunicación con Arduino)
- **PyYAML** (carga de configuración)

Instalar automáticamente:
```bash
./scripts/install.sh
```

O manualmente:
```bash
pip install -r requirements.txt
pip install -r trtappUI/py/requirements.txt
```

## Ejecución

### En Desktop (Linux/Windows/macOS)

```bash
# Activar venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate.ps1 # Windows (PowerShell)

# Ejecutar
python3 trtappUI/py/main.py
```

### En Raspberry Pi (Headless, por SSH)

Si quieres que la UI aparezca en el monitor HDMI:

```bash
# En la Raspberry Pi con display conectado
ssh pi@raspberry.local
python3 trtappUI/py/main.py
```

### Como Servicio Systemd (Auto-arrange)

```bash
# Instalar servicio
sudo cp /tmp/trt_ui.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable trt_ui.service

# Iniciar
sudo systemctl start trt_ui.service

# Ver logs
journalctl -u trt_ui.service -f
```

## Arquitectura

### main.py

Punto de entrada que:
1. Verifica si se ejecuta en venv (si no, lo re-ejecuta)
2. Inicializa QApplication
3. Crea MainWindow
4. Conecta AppController
5. Muestra interfaz

### config.py

- Carga configuración YAML (`config/local_config.yaml` o `config/default_config.yaml`)
- Expone variables globales: `SERIAL_PORT`, `BAUDRATE`, `APP_TITLE`
- Obtiene instancia del `TRTMessageHandler` del módulo `core`

### controller.py (AppController)

Lógica de negocio:
- Inicializa conexión serial via `core.trtmsg`
- Sincroniza widgets Qt (signals/slots)
- Maneja envío de comandos
- Lee sensores

### ui/window.py (MainWindow)

- Carga interfaz gráfica desde `.ui` files
- Aplica tema oscuro
- Configura menú
- Actualiza labels con info del puerto

## Personalización

### Cambiar Tema

En `ui/window.py`, modificar `_setup_styles()`:

```python
dark_stylesheet = (
    "QMainWindow {"
    "background-color: #1e1e1e;"  # Más claro
    "}"
    # ... más estilos
)
```

### Agregar Nuevos Controles

1. Editar `ui/ventana.ui` con **Qt Designer**
   - Herramienta visual para editar interfaces
   
2. O editar XML directamente en `ventana.ui`

3. En `controller.py`, conectar los nuevos widgets:

```python
def setup_connections(self):
    new_button = self.main_window.findChild(QPushButton, "pushButton_New")
    if new_button:
        new_button.clicked.connect(self.on_button_clicked)

def on_button_clicked(self):
    print("Botón presionado!")
    self.send_command("LED_ON")
```

### Cambiar Resolución

Editar `ui/ventana.ui` → Buscar `<width>` y `<height>`

O en `MainWindow.__init__()`:
```python
self.setGeometry(0, 0, 1920, 1080)  # Fullscreen en resolución específica
```

## Comunicación con Hardware

### Desde controller.py

```python
# Enviar comando
self.send_command("LED_ON")

# Leer sensor
temperature = self.read_sensor(0)
print(f"Temp: {temperature}°C")

# Escribir PWM
self.trt_handler.write_pin(13, 200)  # 78% de potencia
```

### Integración Qt

Los datos del hardware pueden actualizar widgets automáticamente:

```python
def on_temperature_changed(self, temp_value):
    label = self.main_window.findChild(QLabel, "labelTemp")
    if label:
        label.setText(f"Temp: {temp_value}°C")

# En thread o timer:
temp = self.read_sensor(0)
self.on_temperature_changed(temp)
```

## Debugging

### Ver logs de conexión serial

```bash
# Ejecutar con output verbose
python3 trtappUI/py/main.py 2>&1 | tee trt_debug.log
```

### Inspeccionar widgets

En `ui/window.py`, al final de `__init__()`:

```python
debug_widgets = self.findChildren(QWidget)
for w in debug_widgets:
    print(f"Widget: {w.objectName()}, Tipo: {type(w).__name__}")
```

### Probar conexión serial sin UI

```bash
python3 -c "
from core import get_trt_handler
h = get_trt_handler()
print(h.get_board_info())
h.connect()
h.send_command('LED_ON')
h.disconnect()
"
```

## Distribución

### Crear ejecutable (Windows)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed trtappUI/py/main.py
# Ejecutable en: dist/main.exe
```

### En Raspberry Pi

No necesita compilación, se ejecuta directamente con Python.

Para distribuir: Hacer git clone del repo en cada Pi.

## Troubleshooting

### "No se puede cargar ui/ventana.ui"

Verifica que estés ejecutando desde el directorio correcto:
```bash
cd /path/to/project
python3 trtappUI/py/main.py
```

### Qt Platform Plugin not found

Instalar librerías gráficas:
```bash
sudo apt-get install libqt6gui6 libqt6core6
```

### Puerto serial no funciona

Ver troubleshooting en [core/README.md](../core/README.md#troubleshooting)

## Extensiones Futuras

Posibles mejoras:
- Gráficos en tiempo real (matplotlib/pyqtgraph)
- Historial de datos (base de datos SQLite)
- Notificaciones en escritorio
- Control remoto web (Django/Flask backend)
- Temas personalizables

---

**Última actualización:** 2026-04-16  
**Versión:** 1.0.0  
**Dependencia:** PySide6 6.4+
