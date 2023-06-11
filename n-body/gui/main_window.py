import os.path

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QMainWindow

from gui.opengl.opengl_widget import SimulationWidget
from gui.side_panel.panel_widget import MenuWidget
from utils.constants import SIM_WINDOW_SIZE
from utils.constants import WINDOW_SIZE


class AppWindow(QMainWindow):
    start_loading_signal = pyqtSignal()
    stop_loading_signal = pyqtSignal()

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

        self.menu = MenuWidget(self.connection, parent=self)
        self.simulation_widget = SimulationWidget(self.connection, parent=self)

        self.layout.addWidget(self.menu)
        self.layout.addWidget(self.simulation_widget)

        self.loading_frame = QFrame(self)
        self.loading_frame.setStyleSheet("background-color: rgba(0, 0, 0, 128);")
        self.loading_frame.setWindowFlags(Qt.FramelessWindowHint)
        self.loading_frame.setVisible(False)

        self.movie = QMovie(os.path.join('utils', 'loading.gif'), parent=self.loading_frame)
        self.loading_icon = QLabel(self.loading_frame)
        self.loading_icon.setMovie(self.movie)

        loading_layout = QVBoxLayout(self.loading_frame)
        loading_layout.addWidget(self.loading_icon)
        loading_layout.setAlignment(Qt.AlignCenter)

        self.start_loading_signal.connect(self.start_loading)
        self.stop_loading_signal.connect(self.stop_loading)

    def start_loading(self):
        # self.loading_frame.setGeometry(300, 0, *SIM_WINDOW_SIZE)
        self.loading_frame.setGeometry(self.simulation_widget.geometry())
        self.loading_frame.setVisible(True)
        self.movie.start()

    def stop_loading(self):
        self.loading_frame.setVisible(False)
        self.movie.stop()

    def closeEvent(self, event):
        self.connection.connection.close()
        self.connection.requestInterruption()
        self.connection.wait()
        event.accept()
