import os.path
import time

import torch
import websockets
from websockets.exceptions import ConnectionClosedError

from algorithms.algorithm import SimulationAlgorithm
from utils.preprocess import Preprocessor
from utils.websocket import WebsocketMessage
from models.model_code import SimulatorModel


class GNN(SimulationAlgorithm):
    def __init__(self, connection, content, dt, device):
        self.__data = None
        super().__init__(connection, content, dt, device)

    def _load_file(self):
        self.__data, self._mass = Preprocessor.get(self._content, dt=self._dt, device=self._device)

        self._r = self.__data.x[:, :self._dim]
        # self._v = self.__data.x[:, self._dim:2 * self._dim]

        self._num_particles = len(self._r)
        # self._edges = self.__data.edge_index

    async def run(self):
        # model = torch.load(os.path.join(os.getcwd(), 'models', 'model.pth'))
        model = SimulatorModel()
        model.to(self._device)

        # state_dict = torch.load(os.path.join(os.path.join(os.getcwd(), 'models', 'model_state_dict.pth')),
        #                         map_location=torch.device('cpu'))
        state_dict = torch.load(os.path.join(os.path.join(os.getcwd(), 'models', 'model_state_dict.pth')),
                                map_location=torch.device(self._device))
        model.load_state_dict(state_dict)
        model.eval()
        try:
            await self._conn.send(WebsocketMessage.create(masses=self._mass, colors=self._colors))
            with torch.no_grad():
                while self._active:
                    start_time = time.perf_counter_ns()
                    output = model(self.__data, get_graph=True)
                    x = output.x
                    self._r = x[:, :self._dim]
                    self._v = x[:, self._dim:2 * self._dim]
                    end_time = time.perf_counter_ns()
                    print(f"Computing: {(end_time - start_time) / 1e9:.4f} s")
                    await self._conn.send(WebsocketMessage.create(self._r, self._v))
        except websockets.exceptions.WebSocketException as e:
            pass
