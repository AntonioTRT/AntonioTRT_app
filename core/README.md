# 🔌 Core - Motor de Comunicación TRT

Módulo central de TRT-AntonioTRT_app que proporciona abstracción para comunicación con Arduino y ESP32.

## Estructura

```
core/
├── __init__.py        # Exporta la API pública
├── trtmsg.py         # Motor de comunicación (protocolo TRT)
└── README.md         # Este archivo
```

## Protocolo TRT (Text Reference Transmission)

Protocolo simple basado en texto para comunicación serie con microcontroladores.

### Características

✓ **Sin dependencias externas** (solo pyserial)  
✓ **Legible en texto plano** (fácil debugging)  
✓ **Compatible con Arduino y ESP32**  
✓ **Previene auto-reset** (DTR=False)  
✓ **Manejo de configuración YAML**  

### Formato de Mensajes

Todos los mensajes terminan con `\n` (newline).

#### Comandos Estándar

```
LED_ON              → Enciende LED
LED_OFF             → Apaga LED
RELAY_ON            → Activa relé
RELAY_OFF           → Desactiva relé
SET:FAN:255         → PWM ventilador a 100% (0-255)
SET:FAN:128         → PWM ventilador a 50%
SENSOR_READ:0       → Lee sensor en pin 0
WRITE_PIN:13:255    → Escribe valor 255 en pin 13
```

#### Respuestas

```
OK                  → Comando ejecutado correctamente
ERROR               → Comando inválido
25.5                → Valor de sensor (número)
```

## Uso

### Inicialización

```python
from core import get_trt_handler

# Obtener instancia (singleton)
handler = get_trt_handler()

# Leer configuración
board_info = handler.get_board_info()
print(board_info)
# Output: {'pi_name': 'RaspberryPi-5', 'board': 'uno', 'port': '/dev/ttyUSB0', 'baudrate': '9600', 'connected': 'False'}
```

### Conectar

```python
# Conectar al dispositivo
if handler.connect():
    print("✓ Conectado")
else:
    print("✗ No se pudo conectar")
```

### Enviar Comandos

```python
# Enviar comando simple
handler.send_command("LED_ON")

# Enviar con parámetro
handler.send_command("SET:FAN:200")

# yyear respuesta
response = handler.read_response(timeout=1.0)
```

### Leer Sensores

```python
# Leer sensor en pin 0
temperature = handler.read_sensor(0)
print(f"Temperatura: {temperature}°C")
```

### Escribir Pines

```python
# Escribir PWM en pin 13
handler.write_pin(13, 255)  # Máximo
handler.write_pin(13, 128)  # 50%
handler.write_pin(13, 0)    # Mínimo (apagado)
```

### Desconectar

```python
handler.disconnect()
```

## Ejemplo Completo

```python
from core import get_trt_handler

def main():
    handler = get_trt_handler()
    
    # Conectar
    if not handler.connect():
        print("Error de conexión")
        return
    
    # Obtener info
    info = handler.get_board_info()
    print(f"Conectado a: {info['pi_name']} en puerto {info['port']}")
    
    # Encender LED
    handler.send_command("LED_ON")
    
    # Esperar respuesta
    response = handler.read_response()
    print(f"Respuesta: {response}")
    
    # Leer sensor
    temp = handler.read_sensor(0)
    print(f"Temperatura: {temp}")
    
    # Controlar PWM
    for pwm_value in range(0, 256, 10):
        handler.write_pin(13, pwm_value)
        print(f"PWM: {pwm_value}")
    
    # Desconectar
    handler.disconnect()

if __name__ == "__main__":
    main()
```

## Configuración

El handler lee automáticamente la configuración desde:

1. **`config/local_config.yaml`** - Configuración local (específica de cada Pi)
2. **`config/default_config.yaml`** - Configuración por defecto

Ver [config/README.md](../config/README.md) para detalles.

## API Completa

### Clase: `TRTMessageHandler`

#### Constructor
```python
handler = TRTMessageHandler(config_path=None)
```
- `config_path` (opcional): Ruta a YAML de configuración

#### Métodos Públicos

| Método | Descripción | Retorna |
|--------|-------------|---------|
| `connect()` | Abre conexión serie | `bool` |
| `disconnect()` | Cierra conexión | `None` |
| `send_command(cmd: str)` | Envía comando | `bool` |
| `read_response(timeout=1.0)` | Lee respuesta | `str \| None` |
| `read_sensor(sensor_id: int)` | Lee sensor | `float \| None` |
| `write_pin(pin: int, value: int)` | Escribe pin | `bool` |
| `get_board_info()` | Info del dispositivo | `dict` |

#### Propiedades

| Propiedad | Tipo | Descripción |
|-----------|------|-------------|
| `config` | `dict` | Configuración cargada |
| `is_connected` | `bool` | Estado de conexión |
| `serial_conn` | `Serial` | Conexión pyserial |

### Función Singleton
```python
def get_trt_handler(config_path=None) -> TRTMessageHandler
```
Retorna instancia única del handler (patrón singleton).

## Testing

Ejecutar pruebas unitarias:

```bash
pytest tests/test_core.py -v
```

Las pruebas usan `unittest.mock` para simular hardware sin tener Arduino conectado.

## Detalles Técnicos

### DTR (Data Terminal Ready)

DTR se desactiva automáticamente al conectar:
```python
self.serial_conn.dtr = False
```

Esto **previene el auto-reset del Arduino** que ocurre cuando se abre la conexión serie.

### Encod

Todos los mensajes usan codificación UTF-8 (por defecto).

### Timeouts

- `read_response()` espera 1 segundo por defecto
- Configurable con el parámetro `timeout`

## Troubleshooting

### "No se pudo abrir el puerto serial"
- Verifica que el puerto existe: `ls /dev/tty*`
- Comprueba que el usuario tiene permisos: `sudo usermod -a -G dialout $USER`
- Reinicia sesión después de cambiar permisos

### Arduino no responde
- Verifica DTR está disabled: Revisa que `dtr = False` en `core/trtmsg.py`
- Espera 2 segundos después de conectar: `time.sleep(2)`
- Verifica baudrate coincide: Por defecto 9600

### Conflictos de puerto
- Asegúrate de que una sola app usa el puerto
- Cierra terminal serial: `sudo fuser -k /dev/ttyUSB0`

## Contributing

Para añadir nuevos comandos al protocolo TRT:

1. Documenta el nuevo comando aquí
2. Implementa en `trtmsg.py`
3. Añade tests en `tests/test_core.py`
4. Actualiza el firmware correspondiente

---

**Última actualización:** 2026-04-16  
**Versión:** 1.0.0
