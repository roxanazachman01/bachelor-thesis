import os.path

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QMainWindow

from gui.opengl.opengl_widget import SimulationWidget
from gui.side_panel.panel_widget import MenuWidget
from utils.constants import WINDOW_SIZE


class AppWindow(QMainWindow):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.setStyleSheet(open(os.path.join('gui', 'style', 'style.qss')).read())
        self.setWindowTitle("N-Body Simulation")
        self.setGeometry(0, 0, *WINDOW_SIZE)

        self.layout = QHBoxLayout(self)
        screen = QWidget()
        screen.setLayout(self.layout)
        self.setCentralWidget(screen)

        self.menu = MenuWidget(self.connection, screen)
        self.simulation_widget = SimulationWidget(screen, self.connection)

        self.layout.addWidget(self.menu)
        self.layout.addWidget(self.simulation_widget)

    def closeEvent(self, event):
        self.connection.connection.close()
        self.connection.requestInterruption()
        self.connection.wait()
        event.accept()
