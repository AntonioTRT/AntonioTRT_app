
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        ui_file = QFile("ui/ventana.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.ui.showFullScreen()
        # Conectar el botón 'Inicio' a la función para mostrar la página de Antonio
        start_button = self.ui.findChild(type(self.ui.findChild(QLabel)), "startButton")
        if start_button is not None:
            start_button.clicked.connect(self.show_antonio_page)
        self.close()

    def show_antonio_page(self):
        antonio_widget = QWidget()
        layout = QVBoxLayout(antonio_widget)
        label = QLabel("antonio")
        label.setStyleSheet("font-size: 96px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.ui.setCentralWidget(antonio_widget)
