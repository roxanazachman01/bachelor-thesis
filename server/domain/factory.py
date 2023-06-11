import asyncio

import torch
from algorithms.ai.gnn import GNN
from algorithms.algorithm import NullAlgorithm
from algorithms.direct.direct_symplectic_euler import DirectSymplecticEuler
from utils.websocket import WebsocketMessage


class AlgorithmFactory:
    def __init__(self, conn):
        self.__conn = conn
        self.__strategy = NullAlgorithm(conn)
        self.__run_task = asyncio.create_task(self.__strategy.run())

    def start_algorithm(self, message):
        algo, content, dt, processor = WebsocketMessage.get(message)
        device = torch.device('cuda' if torch.cuda.is_available() and processor == 'GPU' else 'cpu')
        self.__strategy.stop()
        self.__run_task.cancel()
        # try:
        self.__strategy = self.__get(algo, content, dt, device)
        self.__run_task = asyncio.create_task(self.__strategy.run())
        # except Exception:
        #     print("Invalid data")

    def __get(self, algo="", content="", dt=0.005, device=torch.device('cpu')):
        if algo == 1:
            return DirectSymplecticEuler(self.__conn, content, dt, device)
        elif algo == 2:
            return GNN(self.__conn, content, dt, device)
        else:
            return NullAlgorithm(self.__conn)
