"""
Ventanas principales de la aplicación TRT UI
Interfaz gráfica usando Qt Designer (.ui files)
"""

import os
from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QMenuBar, QMenu
from PySide6.QtGui import QAction
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt


# Obtener ruta a archivos .ui
UI_DIR = Path(__file__).parent


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación TRT."""

    def __init__(self):
        super().__init__()
        self._load_ui()
        self._setup_styles()
        self._setup_menu()

    def _load_ui(self):
        """Carga interfaz gráfica desde archivos .ui"""
        loader = QUiLoader()
        
        # Cargar UI principal
        ui_file_path = UI_DIR / "ventana.ui"
        ui_file = QFile(str(ui_file_path))
        ui_file.open(QFile.ReadOnly)

        print(f"[DEBUG] Cargando UI desde: {ui_file_path}")
        ui = loader.load(ui_file, self)
        ui_file.close()
        
        if ui is None:
            print("[ERROR] No se pudo cargar la interfaz .ui")
            return

        # Asignar centralWidget
        self.central_widget = ui.findChild(QWidget, "centralwidget")
        if self.central_widget is None:
            print("[ERROR] 'centralwidget' no encontrado en .ui")
            self.setCentralWidget(ui)
        else:
            print("[DEBUG] UI cargada correctamente")
            self.setCentralWidget(self.central_widget)

        # Mostrar información del puerto en label
        self._update_serial_label()

    def _update_serial_label(self):
        """Actualiza label con info del puerto serial."""
        from config import SERIAL_PORT, get_trt_handler_instance
        
        label1 = self.findChild(QLabel, "label1")
        if label1:
            handler = get_trt_handler_instance()
            board_info = handler.get_board_info()
            status = "✓ Conectado" if handler.is_connected else "✗ No conectado"
            label1.setText(
                f"Puerto: {SERIAL_PORT} | {board_info.get('pi_name', 'N/A')} | {status}"
            )
            label1.setStyleSheet("font-size: 16px; color: #fff;")

    def _setup_styles(self):
        """Configura tema oscuro."""
        dark_stylesheet = (
            "QMainWindow, QWidget {"
            "background-color: #111;"
            "color: #fff;"
            "}"
            "QPushButton {"
            "background-color: #222;"
            "color: #fff;"
            "border-radius: 8px;"
            "padding: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #333;"
            "}"
            "QMenuBar, QMenu {"
            "background-color: #222;"
            "color: #fff;"
            "}"
            "QLabel {"
            "color: #fff;"
            "}"
        )
        self.setStyleSheet(dark_stylesheet)

    def _setup_menu(self):
        """Configura menú clásico."""
        menubar = QMenuBar(self)
        
        # Menú File
        file_menu = QMenu("File", self)
        file_menu.addAction(QAction("New", self))
        file_menu.addAction(QAction("Open", self))
        file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Menú Edit
        edit_menu = QMenu("Edit", self)
        edit_menu.addAction(QAction("Undo", self))

        # Menú Help
        help_menu = QMenu("Help", self)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

        menubar.addMenu(file_menu)
        menubar.addMenu(edit_menu)
        menubar.addMenu(help_menu)
        self.setMenuBar(menubar)

        self.setWindowTitle("TRT App UI")
        self.showFullScreen()

    def show_about_dialog(self):
        """Muestra ventana 'About'."""
        loader = QUiLoader()
        ui_file_path = UI_DIR / "about.ui"
        ui_file = QFile(str(ui_file_path))
        ui_file.open(QFile.ReadOnly)
        
        about_widget = loader.load(ui_file)
        ui_file.close()
        
        about_window = QMainWindow()
        central = about_widget.findChild(QWidget, "centralwidget") if about_widget else None
        
        if central:
            about_window.setCentralWidget(central)
        else:
            about_window.setCentralWidget(about_widget)
        
        about_window.setWindowTitle("Acerca de")
        about_window.show()


class SecondWindow(QMainWindow):
    """Ventana secundaria de ejemplo."""

    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel("¡Bienvenido a la segunda ventana!")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 48px; color: #fff;")
        layout.addWidget(label)
        self.setCentralWidget(widget)
        self.setWindowTitle("Segunda Ventana")
        
        self._setup_styles()
        self._setup_menu()
        self.showFullScreen()

    def _setup_styles(self):
        """Configura tema oscuro."""
        dark_stylesheet = (
            "QMainWindow, QWidget {"
            "background-color: #111;"
            "color: #fff;"
            "}"
            "QPushButton {"
            "background-color: #222;"
            "color: #fff;"
            "border-radius: 8px;"
            "}"
        )
        self.setStyleSheet(dark_stylesheet)

    def _setup_menu(self):
        """Configura menú."""
        menubar = QMenuBar(self)
        file_menu = QMenu("File", self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        menubar.addMenu(file_menu)
        self.setMenuBar(menubar)
