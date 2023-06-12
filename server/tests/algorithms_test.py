import unittest

import torch
from torch import float64

from algorithms.direct.direct_symplectic_euler import DirectSymplecticEuler


class AlgorithmTest(unittest.TestCase):
    def test_direct_symplectic_euler(self):
        content = [[0, 0, 0, 1, 1, 1, 1e9], [1, 1, 1, -1, -1, -1, 1e9]]
        algorithm = DirectSymplecticEuler(None, content, 0.005, 'cpu')
        expected_r = torch.tensor([[0.0050, 0.0050, 0.0050], [0.9950, 0.9950, 0.9950]], dtype=float64)
        expected_v = torch.tensor([[0.9999, 0.9999, 0.9999], [-0.9999, -0.9999, -0.9999]], dtype=float64)
        new_r, new_v = algorithm.compute()

        self.assertTrue(torch.allclose(expected_r, new_r, atol=0.1))
        self.assertTrue(torch.allclose(expected_v, new_v, atol=0.1))


if __name__ == '__main__':
    unittest.main()
