# 🔧 Firmware - Código para Microcontroladores

Contiene el código a compilar y flashear en Arduino Uno y ESP32.

## Estructura

```
firmware/
├── arduino-uno/
│   ├── sketch.ino
│   ├── config.h
│   └── README.md
├── esp32/
│   ├── sketch.ino
│   ├── config.h
│   └── README.md
├── common/
│   ├── trt_protocol.h
│   ├── trt_protocol.cpp
│   └── README.md
└── README.md (este archivo)
```

## Requisitos

### Para Arduino Uno

- Arduino IDE 1.8.x o superior
- Arduino AVR core
- Cable USB tipo A-B (o FTDI)

### Para ESP32

- Arduino IDE 1.8.x o superior
- ESP32 board support (https://github.com/espressif/arduino-esp32)
- Cable micro-USB

### Herramientas Automatizadas (Recomendado)

- **arduino-cli**: Compilación automática
- **avrdude**: Flasheo de Arduino Uno
- **esptool.py**: Flasheo de ESP32

Instalar con:
```bash
./scripts/install.sh
```

## Compilación y Flasheo

### Opción 1: Automático con deploy.sh

```bash
# Arduino Uno
./scripts/deploy.sh --board uno --port /dev/ttyUSB0

# ESP32
./scripts/deploy.sh --board esp32 --port /dev/ttyUSB0
```

### Opción 2: Manual con arduino-cli

```bash
# Compilar Arduino Uno
arduino-cli compile --fqbn arduino:avr:uno firmware/arduino-uno/

# Flashear Arduino Uno
arduino-cli upload --fqbn arduino:avr:uno --port /dev/ttyUSB0 firmware/arduino-uno/

# Compilar ESP32
arduino-cli compile --fqbn esp32:esp32:esp32 firmware/esp32/

# Flashear ESP32
arduino-cli upload --fqbn esp32:esp32:esp32 --port /dev/ttyUSB0 firmware/esp32/
```

## Protocolo TRT en Firmware

Los sketches implementan el protocolo TRT (Text Reference Transmission).

### Comandos Soportados

```cpp
// Ejemplos en el firmware

// LED
LED_ON   → digitalWrite(LED_PIN, HIGH)
LED_OFF  → digitalWrite(LED_PIN, LOW)

// RELÉ
RELAY_ON  → digitalWrite(RELAY_PIN, HIGH)
RELAY_OFF → digitalWrite(RELAY_PIN, LOW)

// PWM (Ventilador)
SET:FAN:255  → analogWrite(FAN_PIN, 255)  // 100%
SET:FAN:128  → analogWrite(FAN_PIN, 128)  // 50%

// SENSORES (Leer valor analógico)
SENSOR_READ:0  → Serial.println(analogRead(A0))

// ESCRITURA DE PIN
WRITE_PIN:13:255  → analogWrite(13, 255)
```

### Ejemplo de Respuesta

```
> LED_ON
< OK

> SENSOR_READ:0
< 512

> SET:FAN:200
< OK
```

## Pin Mapping

### Arduino Uno

| Función | Pin | Tipo |
|---------|-----|------|
| LED | 13 | Digital |
| Relé | 12 | Digital |
| Ventilador | 11 | PWM |
| Sensor Temp | A0 | Analógico |
| Sensor Humedad | A1 | Analógico |

### ESP32

| Función | Pin | Tipo |
|---------|-----|------|
| LED | GPIO2 | Digital |
| Relé | GPIO27 | Digital |
| Ventilador | GPIO25 | PWM |
| Sensor Temp | GPIO34 | ADC |
| Sensor Humedad | GPIO35 | ADC |

Editar en `config.h` de cada carpeta.

## Troubleshooting

### "arduino-cli: no existe"
```bash
# Instalar
./scripts/install.sh
```

### "Puerto no encontrado"
```bash
# Listar puertos
ls /dev/tty*
ls COM*  # Windows
```

### Arduino se resetea al abrir puerto
- Esto es normal (Arduino resetea en DTR)
- core/trtmsg.py maneja esto con: `serial_conn.dtr = False`

### ESP32 no flashea
```bash
# Mantener pulsado BOOT mientras flasheas
# O configurar en arduino-cli
```

## Desarrollo

### Agregar nuevo comando

1. Editar `firmware/common/trt_protocol.cpp`
2. Implementar en `firmware/arduino-uno/sketch.ino` y `esp32/sketch.ino`
3. Compilar y testear
4. Actualizar `core/trtmsg.py` si es necesario

### Debug Serial

Usar Serial Monitor a 9600 baud:
```cpp
Serial.println("Debug message");
```

## Actualizaciones Automáticas

Si configuras `scripts/autoupdate.sh` en crontab, la Raspberry Pi flasheará automáticamente cuando haya cambios en esta carpeta.

Ver [scripts/README.md](../scripts/README.md)

---

**Última actualización:** 2026-04-16  
**Versión Compatible:** TRT Protocol v1.0
