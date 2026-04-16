"""
Controlador de la aplicación TRT UI
Maneja lógica de negocio, comunicación seria y signals Qt
"""

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget

from config import get_trt_handler_instance, SERIAL_PORT


class AppController(QObject):
    """Controlador principal de la aplicación."""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.trt_handler = get_trt_handler_instance()
        
        # Intentar conexión serial
        self.setup_connections()
        self.connect_serial()

    def setup_connections(self):
        """Conecta signals Qt para sincronización de UI."""
        # Sincronizar QDial y QProgressBar
        dial = self.main_window.findChild(QWidget, "dial")
        progress = self.main_window.findChild(QWidget, "progressBar")
        if dial and progress:
            dial.valueChanged.connect(progress.setValue)

        # Sincronizar QDial (dial1) y QProgressBar si existe
        dial1 = self.main_window.findChild(QWidget, "dial1")
        if dial1 and progress:
            dial1.valueChanged.connect(progress.setValue)

    def connect_serial(self):
        """Intenta conectar con el dispositivo serial via TRT Handler."""
        try:
            if self.trt_handler.connect():
                print(f"✓ Controlador conectado a puerto {SERIAL_PORT}")
            else:
                print("⚠️  No se pudo conectar al puerto serial (modo simulación)")
        except Exception as e:
            print(f"✗ Error en conexión serial: {e}")

    def send_command(self, cmd: str) -> bool:
        """
        Envía comando al dispositivo via TRT Handler.
        
        Args:
            cmd: Comando a enviar (ej: "LED_ON")
            
        Returns:
            True si se envió exitosamente
        """
        return self.trt_handler.send_command(cmd)

    def read_response(self):
        """Lee respuesta del dispositivo."""
        return self.trt_handler.read_response()

    def read_sensor(self, sensor_id: int):
        """Lee valor de sensor específico."""
        return self.trt_handler.read_sensor(sensor_id)

    def close_serial(self):
        """Cierra la conexión serial."""
        self.trt_handler.disconnect()
