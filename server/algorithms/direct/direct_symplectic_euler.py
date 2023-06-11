import time

import torch
import websockets

from algorithms.algorithm import SimulationAlgorithm
from utils.constants import G
from utils.websocket import WebsocketMessage


class DirectSymplecticEuler(SimulationAlgorithm):
    def __init__(self, connection, content, dt, device):
        super().__init__(connection, content, dt, device)

    async def run(self):
        try:
            await self._conn.send(WebsocketMessage.create(masses=self._mass, colors=self._colors))
            total_forces = torch.zeros((self._num_particles, self._dim), device=self._device)
            while self._active:
                start_time = time.perf_counter_ns()
                rij = self._r[self._edges[0]] - self._r[self._edges[1]]
                r = torch.sqrt(torch.sum(rij ** 2, dim=1))
                # r = torch.norm(rij, dim=1)
                mass_prod = self._mass[self._edges[0]] * self._mass[self._edges[1]]
                # mass_prod = torch.einsum('i,i->i', self._mass[self._edges[0]], self._mass[self._edges[1]])
                forces = G * mass_prod.unsqueeze(1) * rij / (r ** 3).unsqueeze(1)
                # forces = G * torch.mul(mass_prod.unsqueeze(1), rij / torch.pow(r, 3).unsqueeze(1))
                for i in range(self._edges.shape[1]):
                    total_forces[self._edges[0][i]] += forces[i]
                    total_forces[self._edges[1][i]] -= forces[i]
                acceleration = total_forces / self._mass.unsqueeze(1)
                total_forces.fill_(0)
                self._v += acceleration * self._dt
                self._r += self._v * self._dt
                end_time = time.perf_counter_ns()
                print(f"Computing: {(end_time - start_time) / 1e9:.4f} s")
                await self._conn.send(WebsocketMessage.create(position=self._r, velocity=self._v))
        except websockets.exceptions.WebSocketException as e:
            pass
