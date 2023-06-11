from random import randint

import torch


class SimulationAlgorithm:
    # file path for a file having format (position vector, velocity vector, mass) - 2d: 5 values, 3d: 7 values
    def __init__(self, connection, content, dt=0.005, device=torch.device('cpu')):
        self._conn = connection
        self._content = content
        self._dt = dt
        self._dim = 3
        self._num_particles = 0
        self._r = None
        self._v = None
        self._mass = None
        self._active = True
        self._edges = None
        self._device = device
        self._load_file()
        self._colors = []
        self._generate_colors()

    def _load_file(self):
        tensor = torch.tensor(self._content, dtype=torch.double, device=self._device)

        self._r = tensor[:, :self._dim]
        self._v = tensor[:, self._dim:2 * self._dim]
        self._mass = tensor[:, -1]

        self._num_particles = len(self._r)
        self._edges = torch.combinations(torch.arange(self._num_particles), r=2).T
        # self._edges = torch.cat([self.__edges, self.__edges.flip(dims=(1,))]).T

    def stop(self):
        self._active = False

    async def run(self):
        pass

    def _generate_colors(self):
        for _ in range(self._num_particles):
            color = (randint(187, 255) / 255.0, randint(63, 100) / 255.0, randint(187, 255) / 255.0)
            self._colors.append(color)


class NullAlgorithm(SimulationAlgorithm):
    def __init__(self, connection):
        super().__init__(connection, "")

    def _load_file(self):
        pass

    def stop(self):
        pass

    async def run(self):
        pass
