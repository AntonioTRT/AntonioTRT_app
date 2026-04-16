"""
Pruebas unitarias para el módulo core.trtmsg
Verifica que el protocolo TRT genera correctamente los comandos
sin necesidad de hardware físico conectado.
"""

import sys
import os
from pathlib import Path
import unittest
from unittest.mock import Mock, patch, MagicMock

# Añadir raíz del proyecto al path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.trtmsg import TRTMessageHandler, get_trt_handler


class TestTRTMessageHandler(unittest.TestCase):
    """Pruebas para TRTMessageHandler sin hardware."""

    def setUp(self):
        """Preparar antes de cada test."""
        # Mock de la configuración YAML
        self.mock_config = {
            "pi_name": "RaspberryPi-Test",
            "board_type": "uno",
            "serial_port": "/dev/ttyUSB0",
            "baudrate": 9600,
            "features": {
                "has_lcd": False,
                "has_fan": False
            }
        }

    def test_handler_initialization(self):
        """Prueba que el handler se inicializa correctamente."""
        with patch.object(TRTMessageHandler, '_load_config', return_value=self.mock_config):
            handler = TRTMessageHandler()
            self.assertEqual(handler.config["pi_name"], "RaspberryPi-Test")
            self.assertEqual(handler.config["board_type"], "uno")
            self.assertFalse(handler.is_connected)

    def test_get_board_info(self):
        """Prueba que get_board_info retorna información correcta."""
        with patch.object(TRTMessageHandler, '_load_config', return_value=self.mock_config):
            handler = TRTMessageHandler()
            info = handler.get_board_info()
            
            self.assertEqual(info["pi_name"], "RaspberryPi-Test")
            self.assertEqual(info["board"], "uno")
            self.assertEqual(info["port"], "/dev/ttyUSB0")
            self.assertEqual(info["baudrate"], "9600")

    def test_send_command_format(self):
        """Prueba que los comandos se formatean correctamente."""
        with patch.object(TRTMessageHandler, '_load_config', return_value=self.mock_config):
            with patch('serial.Serial'):
                handler = TRTMessageHandler()
                handler.serial_conn = MagicMock()
                handler.is_connected = True
                
                # Enviar comando
                result = handler.send_command("LED_ON")
                
                # Verificar que write fue llamado con el formato correcto
                handler.serial_conn.write.assert_called_once()
                call_args = handler.serial_conn.write.call_args[0][0]
                self.assertIn(b"LED_ON", call_args)
                self.assertTrue(call_args.endswith(b'\n'))

    def test_send_command_disconnected(self):
        """Prueba que send_command retorna False si no está conectado."""
        with patch.object(TRTMessageHandler, '_load_config', return_value=self.mock_config):
            handler = TRTMessageHandler()
            handler.is_connected = False
            handler.serial_conn = None
            
            result = handler.send_command("LED_ON")
            self.assertFalse(result)

    def test_protocol_messages(self):
        """Prueba que se generan correctamente los mensajes del protocolo TRT."""
        test_cases = [
            ("SET:FAN:255", b"SET:FAN:255\n"),      # PWM al máximo
            ("SET:FAN:128", b"SET:FAN:128\n"),      # PWM al 50%
            ("SENSOR_READ:0", b"SENSOR_READ:0\n"),  # Lectura sensor
            ("RELAY_ON", b"RELAY_ON\n"),            # Relé encendido
            ("RELAY_OFF", b"RELAY_OFF\n"),          # Relé apagado
        ]
        
        with patch.object(TRTMessageHandler, '_load_config', return_value=self.mock_config):
            with patch('serial.Serial'):
                handler = TRTMessageHandler()
                handler.serial_conn = MagicMock()
                handler.is_connected = True
                
                for cmd, expected_bytes in test_cases:
                    handler.serial_conn.reset_mock()
                    handler.send_command(cmd)
                    handler.serial_conn.write.assert_called_once_with(expected_bytes)

    def test_read_sensor_mock(self):
        """Prueba lectura de sensor (sin hardware)."""
        with patch.object(TRTMessageHandler, '_load_config', return_value=self.mock_config):
            with patch('serial.Serial'):
                handler = TRTMessageHandler()
                handler.serial_conn = MagicMock()
                handler.is_connected = True
                
                # Mock de la respuesta del sensor
                handler.serial_conn.in_waiting = 1
                handler.serial_conn.readline.return_value = b"25.5\n"
                
                # Leer sensor
                value = handler.read_sensor(0)
                self.assertEqual(value, 25.5)

    def test_connect_with_mock_serial(self):
        """Prueba conexión con serial mockeado."""
        with patch.object(TRTMessageHandler, '_load_config', return_value=self.mock_config):
            with patch('serial.Serial') as mock_serial_class:
                mock_serial = MagicMock()
                mock_serial_class.return_value = mock_serial
                
                handler = TRTMessageHandler()
                result = handler.connect()
                
                self.assertTrue(result)
                self.assertTrue(handler.is_connected)
                mock_serial.dtr = False  # DTR debe estar deshabilitado

    def test_singleton_pattern(self):
        """Prueba que get_trt_handler retorna la misma instancia."""
        with patch.object(TRTMessageHandler, '_load_config', return_value=self.mock_config):
            handler1 = get_trt_handler()
            handler2 = get_trt_handler()
            
            self.assertIs(handler1, handler2)


class TestTRTProtocol(unittest.TestCase):
    """Pruebas específicas del protocolo TRT."""

    def test_write_pin_format(self):
        """Prueba formato de escritura en pines."""
        mock_config = {
            "pi_name": "Test",
            "board_type": "uno",
            "serial_port": "/dev/ttyUSB0",
            "baudrate": 9600,
            "features": {}
        }
        
        with patch.object(TRTMessageHandler, '_load_config', return_value=mock_config):
            with patch('serial.Serial'):
                handler = TRTMessageHandler()
                handler.serial_conn = MagicMock()
                handler.is_connected = True
                
                # Escribir en pin 13 con valor 255
                handler.write_pin(13, 255)
                
                # Verificar formato
                call_args = handler.serial_conn.write.call_args[0][0]
                self.assertIn(b"WRITE_PIN:13:255", call_args)

    def test_dtr_disabled_on_connect(self):
        """Verifica que DTR se deshabilite en conexión (evita auto-reset Arduino)."""
        mock_config = {
            "pi_name": "Test",
            "board_type": "uno",
            "serial_port": "/dev/ttyUSB0",
            "baudrate": 9600,
            "features": {}
        }
        
        with patch.object(TRTMessageHandler, '_load_config', return_value=mock_config):
            with patch('serial.Serial') as mock_serial_class:
                mock_serial = MagicMock()
                mock_serial_class.return_value = mock_serial
                
                handler = TRTMessageHandler()
                handler.connect()
                
                # Verificar que dtr fue seteado a False
                self.assertEqual(mock_serial.dtr, False)


if __name__ == '__main__':
    unittest.main()
