# 🧪 Tests - Pruebas Unitarias

Contiene pruebas automáticas del módulo `core.trtmsg` usando `pytest` y `unittest.mock`.

## Estructura

```
tests/
├── __init__.py
├── test_core.py       # Pruebas del protocolo TRT
└── README.md          # Este archivo
```

## Requisitos

```bash
pip install pytest pytest-cov
```

O instalar desde requirements.txt:
```bash
pip install -r requirements.txt
pip install -r tests/requirements.txt  # Si existe
```

## Ejecutar Pruebas

### Ejecutar todos los tests

```bash
pytest tests/
```

### Ejecutar test específico

```bash
pytest tests/test_core.py::TestTRTMessageHandler::test_handler_initialization -v
```

### Ejecutar con cobertura

```bash
pytest tests/ --cov=core --cov=trtappUI/py/controller --cov-report=term-missing
```

### Ejecutar con reporte HTML

```bash
pytest tests/ --cov=core --cov-report=html
# Abre: htmlcov/index.html
```

### Modo verbose (detallado)

```bash
pytest tests/ -v -s
# -v: verbose
# -s: show print statements
```

## Test Suites

### `TestTRTMessageHandler`

Pruebas principales del handler de comunicación.

| Test | Descripción |
|------|-------------|
| `test_handler_initialization` | El handler se inicializa correctamente |
| `test_get_board_info` | Retorna info del dispositivo |
| `test_send_command_format` | Los comandos se formatean con `\n` |
| `test_send_command_disconnected` | Retorna error si no conectado |
| `test_protocol_messages` | Mensajes TRT válidos (SET:FAN:255, etc) |
| `test_read_sensor_mock` | Lee sensor mockeado |
| `test_connect_with_mock_serial` | Conexión serial mockeada |
| `test_singleton_pattern` | get_trt_handler retorna misma instancia |

### `TestTRTProtocol`

Pruebas específicas del protocolo TRT.

| Test | Descripción |
|------|-------------|
| `test_write_pin_format` | Formato WRITE_PIN:13:255 |
| `test_dtr_disabled_on_connect` | DTR deshabilitado (evita auto-reset) |

## Mocking (Pruebas sin Hardware)

Las pruebas usan **`unittest.mock`** para simular hardware sin tener Arduino conectado.

### Ejemplo: Mockear conexión serial

```python
from unittest.mock import patch, MagicMock

with patch('serial.Serial') as mock_serial:
    # Configurearmock
    mock_serial.return_value.is_open = True
    mock_serial.return_value.write.return_value = 10
    
    # Probar código
    handler = TRTMessageHandler()
    handler.connect()
    
    # Verificar que se llamó correctamente
    mock_serial.assert_called_once()
```

### Ejemplo: Mockear configuración YAML

```python
from unittest.mock import patch

mock_config = {
    "pi_name": "RaspberryPi-Test",
    "board_type": "uno",
    "serial_port": "/dev/ttyUSB0",
    "baudrate": 9600,
    "features": {}
}

with patch.object(TRTMessageHandler, '_load_config', return_value=mock_config):
    handler = TRTMessageHandler()
    # Handler usa la config mockeada
```

## Escribir Nuevas Pruebas

### Template para nuevo test

```python
import unittest
from unittest.mock import patch, MagicMock
from core.trtmsg import TRTMessageHandler

class TestNewFeature(unittest.TestCase):
    
    def setUp(self):
        """Preparación antes de cada test"""
        self.mock_config = {
            "pi_name": "Test",
            "board_type": "uno",
            "serial_port": "/dev/ttyUSB0",
            "baudrate": 9600,
            "features": {}
        }
    
    def test_my_feature(self):
        """Descripción de qué se prueba"""
        with patch.object(TRTMessageHandler, '_load_config', return_value=self.mock_config):
            handler = TRTMessageHandler()
            
            # Ejecutar
            result = handler.my_method()
            
            # Verificar
            self.assertEqual(result, expected_value)
    
    def tearDown(self):
        """Limpieza después de cada test"""
        pass

if __name__ == '__main__':
    unittest.main()
```

### Checklist antes de commitear

- [ ] Todos los tests pasan: `pytest tests/ -v`
- [ ] Cobertura > 80%: `pytest tests/ --cov=core`
- [ ] Sin warnings: `pytest tests/ -W default`
- [ ] Documentado: Docstring en cada test

## CI/CD Integration

Estos tests se ejecutan automáticamente en **GitHub Actions** cuando haces push:

Ver [`.github/workflows/ci_check.yml`](../.github/workflows/ci_check.yml)

El workflow:
1. Instala dependencias
2. Ejecuta pytest
3. Genera reporte de cobertura
4. Sube a Codecov (si existe integración)

## Troubleshooting

### "ImportError: No module named 'core'"

Verifica que ejecutas desde la raíz del proyecto:
```bash
cd /path/to/project
pytest tests/
```

### "ModuleNotFoundError: No module named 'serial'"

Instala pyserial:
```bash
pip install pyserial
```

### Tests lentos

Algunos tests esperan timeouts. Para acelerar:
```bash
pytest tests/ -v --timeout=5
# Timeout de 5 segundos por test
```

### Ver qué hace cada test

```bash
pytest tests/ -v -s
# -s: muestra print() dentro de tests
```

## Mejores Prácticas

✓ **Un test = una responsabilidad**  
✓ **Nombres descriptivos**: `test_sends_command_with_newline()`  
✓ **Mockear dependencias externas** (serial, YAML, etc)  
✓ **Setup/teardown compartido** en `setUp()` y `tearDown()`  
✓ **Documentar el por qué**, no solo el qué  
✓ **DRY**: No repetir código, usar **fixtures**  

## Fixtures (Reutilizar Setup)

```python
import pytest

@pytest.fixture
def trt_handler():
    """Fixture: Retorna handler mockeado"""
    with patch.object(...):
        return TRTMessageHandler()

def test_something(trt_handler):
    """Usa fixture automáticamente"""
    handler = trt_handler
    # ...
```

## Cobertura de Código

Generar reporte visual:

```bash
pytest tests/ --cov=core --cov-report=html --cov-report=term
# Abre: htmlcov/index.html
```

Buscar líneas no cubiertas:
```bash
# Mostrar líneas sin cobertura
grep "NO COVER" htmlcov/core_*.html
```

---

**Última actualización:** 2026-04-16  
**Versión:** 1.0.0  
**Frameworks:** pytest, unittest.mock
