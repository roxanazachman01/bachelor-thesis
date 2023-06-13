import time

from PyQt5.QtCore import pyqtSignal, QThread
from websocket import WebSocketApp

from utils.ws import WebsocketMessage


class WebsocketConnection(QThread):
    emitter = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.__connection = None
        self.start_time = time.perf_counter_ns()

    @property
    def connection(self):
        return self.__connection

    def on_message(self, ws, message):
        end_time = time.perf_counter_ns()
        print(f"Time since last message: {(end_time - self.start_time) / 1e9:.4f} s")
        self.start_time = end_time
        self.emitter.emit(WebsocketMessage.get(message))

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("Connection closed")

    def on_open(self, ws):
        print("Connection opened")

    def connect_to_server(self):
        self.__connection.on_open = self.on_open
        try:
            self.__connection.run_forever()
        except Exception as e:
            print(f"Exception in WebSocket thread: {e}")

    def run(self):
        self.__connection = WebSocketApp("ws://127.0.0.1:8000",
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.__connection.on_open = self.on_open
        try:
            self.__connection.run_forever()
        except Exception as e:
            print(f"Exception in WebSocket thread: {e}")
