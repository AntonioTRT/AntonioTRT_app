Proyecto Qt minimal para Raspberry Pi

Estructura recomendada:
- app/ : código de la aplicación (`MainWindow`, controladores, etc.)
- main.py : entrada de la aplicación
- requirements.txt : dependencias

Instalación y ejecución (Raspberry Pi, asumiendo Python 3):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

Notas:
- La ventana abre en pantalla completa y muestra "hola" centrado.
- La barra de menús incluye `File`, `Edit` y `Help` con acciones placeholder.
- Para ampliar, editar `app/window.py` y añadir lógica en `app/controller.py`.
