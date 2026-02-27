import serial
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget
from config import SERIAL_PORT, BAUDRATE

class AppController(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_connections()
        self.serial = None
        self.connect_serial()

    def setup_connections(self):
        from PySide6.QtWidgets import QWidget
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
        try:
            # self.serial = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)  # Comentado para evitar error en Windows
            self.serial = None  # Evita error, pero mantiene la funcionalidad para descomentar
        except Exception as e:
            print(f"No se pudo abrir el puerto serial: {e}")

    def send_serial(self, data):
        if self.serial and self.serial.is_open:
            self.serial.write(data.encode())

    def close_serial(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
