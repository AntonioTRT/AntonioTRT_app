from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hola App")
        self._create_menu()
        self._create_central()
        self.showFullScreen()

    def _create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        edit_menu = menubar.addMenu("Edit")
        help_menu = menubar.addMenu("Help")

        file_menu.addAction(QAction("New", self))
        file_menu.addAction(QAction("Open...", self))
        file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu.addAction(QAction("Undo", self))
        help_menu.addAction(QAction("About", self))

    def _create_central(self):
        central = QWidget()
        layout = QVBoxLayout(central)
        label = QLabel("hola")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 96px;")
        layout.addWidget(label)
        self.setCentralWidget(central)
