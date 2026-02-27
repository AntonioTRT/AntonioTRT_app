
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QMenuBar, QMenu
from PySide6.QtGui import QAction
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar UI
        loader = QUiLoader()
        ui_file = QFile("ui/ventana.ui")
        ui_file.open(QFile.ReadOnly)

        print("[DEBUG] Cargando ui/ventana.ui ...")
        ui = loader.load(ui_file, self)
        ui_file.close()
        if ui is None:
            print("[ERROR] No se pudo cargar ui/ventana.ui")
        else:
            print("[DEBUG] UI cargada correctamente")

        # Asignar centralWidget y exponerlo
        self.central_widget = ui.findChild(QWidget, "centralwidget") if ui else None
        if self.central_widget is None:
            print("[ERROR] No se encontró 'centralwidget' en la UI")
            self.setCentralWidget(ui)
        else:
            print("[DEBUG] 'centralwidget' encontrado y asignado")
            self.setCentralWidget(self.central_widget)

        # Mostrar el puerto en label1
        from config import SERIAL_PORT
        label1 = self.findChild(QLabel, "label1")
        if label1:
            label1.setText(f"Puerto: {SERIAL_PORT}")
            label1.setStyleSheet("font-size: 24px; color: #fff;")

        # Tema oscuro
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
            "QMenuBar, QMenu {"
            "background-color: #222;"
            "color: #fff;"
            "}"
        )
        self.setStyleSheet(dark_stylesheet)

        # Menú clásico
        menubar = QMenuBar(self)
        file_menu = QMenu("File", self)
        edit_menu = QMenu("Edit", self)
        about_menu = QMenu("About", self)

        file_menu.addAction(QAction("New", self))
        file_menu.addAction(QAction("Open", self))
        file_menu.addSeparator()
        file_menu.addAction(QAction("Exit", self, triggered=self.close))

        edit_menu.addAction(QAction("Undo", self))

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_page)
        about_menu.addAction(about_action)

        menubar.addMenu(file_menu)
        menubar.addMenu(edit_menu)
        menubar.addMenu(about_menu)
        self.setMenuBar(menubar)

        self.setWindowTitle("Hola App")
        self.showFullScreen()

    def show_about_page(self):
        from PySide6.QtUiTools import QUiLoader
        from PySide6.QtCore import QFile
        from PySide6.QtWidgets import QMainWindow
        loader = QUiLoader()
        ui_file = QFile("ui/about.ui")
        ui_file.open(QFile.ReadOnly)
        about_widget = loader.load(ui_file)
        ui_file.close()
        about_window = QMainWindow()
        central = about_widget.findChild(QWidget, "centralwidget")
        if central:
            about_window.setCentralWidget(central)
        else:
            about_window.setCentralWidget(about_widget)
        about_window.setWindowTitle("About")
        about_window.show()


    def show_second_window(self):
        second_window = SecondWindow()
        second_window.showFullScreen()
        second_window.show()
        self.close()
        from PySide6.QtWidgets import QApplication
        QApplication.instance().quit()


class SecondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel("¡Bienvenido a la segunda ventana!")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 48px;")
        layout.addWidget(label)
        self.setCentralWidget(widget)
        self.setWindowTitle("Segunda Ventana")
        self.showFullScreen()
        # Tema oscuro
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
            "QMenuBar, QMenu {"
            "background-color: #222;"
            "color: #fff;"
            "}"
        )
        self.setStyleSheet(dark_stylesheet)

        # Menú clásico
        menubar = QMenuBar(self)
        file_menu = QMenu("File", self)
        edit_menu = QMenu("Edit", self)
        about_menu = QMenu("About", self)

        file_menu.addAction(QAction("New", self))
        file_menu.addAction(QAction("Open", self))
        file_menu.addSeparator()
        file_menu.addAction(QAction("Exit", self, triggered=self.close))

        edit_menu.addAction(QAction("Undo", self))

        about_menu.addAction(QAction("About", self))

        menubar.addMenu(file_menu)
        menubar.addMenu(edit_menu)
        menubar.addMenu(about_menu)
        self.setMenuBar(menubar)
        self.setStyleSheet(dark_stylesheet)

        # Conectar el botón 'inicio' desde el .ui
        start_button = self.ui.findChild(QWidget, "startButton")
        if start_button:
            start_button.clicked.connect(self.show_second_window)

        # Menú clásico
        menubar = QMenuBar(self)
        file_menu = QMenu("File", self)
        edit_menu = QMenu("Edit", self)
        about_menu = QMenu("About", self)

        file_menu.addAction(QAction("New", self))
        file_menu.addAction(QAction("Open", self))
        file_menu.addSeparator()
        file_menu.addAction(QAction("Exit", self, triggered=self.close))

        edit_menu.addAction(QAction("Undo", self))

        about_menu.addAction(QAction("About", self))

        menubar.addMenu(file_menu)
        menubar.addMenu(edit_menu)
        menubar.addMenu(about_menu)
        self.setMenuBar(menubar)

        # Contenido de la segunda ventana
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel("¡Bienvenido a la segunda ventana!")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 48px;")
        layout.addWidget(label)
        self.setCentralWidget(widget)

    def show_antonio_page(self):
        antonio_widget = QWidget()
        layout = QVBoxLayout(antonio_widget)
        label = QLabel("antonio")
        label.setStyleSheet("font-size: 96px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.ui.setCentralWidget(antonio_widget)
