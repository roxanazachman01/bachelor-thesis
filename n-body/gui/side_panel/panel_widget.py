from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox
from websocket import WebSocketConnectionClosedException

from gui.side_panel.algorithm_widget import AlgorithmWidget
from gui.side_panel.file_picker_widget import FilePickerWidget
from gui.side_panel.processor_widget import ProcessorWidget
from gui.side_panel.timestep_widget import TimestepWidget
from utils.ws import WebsocketMessage


class MenuWidget(QWidget):
    def __init__(self, connection, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.connection = connection
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        start_btn = QPushButton("Start")
        start_btn.clicked.connect(self.start_simulation)
        stop_btn = QPushButton("Stop")
        stop_btn.clicked.connect(self.stop_simulation)
        self.algorithm_widget = AlgorithmWidget(self)
        self.processor_widget = ProcessorWidget(self)
        self.dt_widget = TimestepWidget(self)
        self.file_widget = FilePickerWidget(self)

        self.layout.addWidget(self.algorithm_widget, alignment=Qt.AlignTop)
        self.layout.addWidget(self.processor_widget, alignment=Qt.AlignTop)
        self.layout.addWidget(self.dt_widget, alignment=Qt.AlignTop)
        self.layout.addWidget(self.file_widget, alignment=Qt.AlignTop)
        self.layout.addWidget(start_btn, alignment=Qt.AlignTop)
        self.layout.addWidget(stop_btn, alignment=Qt.AlignTop)

    def start_simulation(self):
        try:
            # todo validation
            algorithm = self.algorithm_widget.get()
            processor = self.processor_widget.get()
            dt = self.dt_widget.get()
            file_path = self.file_widget.get()

            self.connection.connection.send(
                WebsocketMessage.create(algo=algorithm, path=file_path, dt=dt, processor=processor))
            self.parent.start_loading_signal.emit()
        except WebSocketConnectionClosedException:
            QMessageBox.warning(self, "Warning", "Connection is down! Reconnecting...", QMessageBox.Ok)
            self.connection.start()

    def stop_simulation(self):
        try:
            self.connection.connection.send(WebsocketMessage.create())
            self.parent.stop_loading_signal.emit()
        except WebSocketConnectionClosedException:
            self.connection.start()
