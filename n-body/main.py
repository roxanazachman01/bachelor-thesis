import sys

from PyQt5.QtWidgets import QApplication

from connection.client import WebsocketConnection
from gui.main_window import AppWindow
from utils.constants import WINDOW_SIZE

if __name__ == "__main__":
    ws_connection = WebsocketConnection()
    ws_connection.start()

    app = QApplication([])
    window = AppWindow(ws_connection)
    window.resize(*WINDOW_SIZE)
    window.show()

    app.exec_()

    ws_connection.wait()
    sys.exit()
