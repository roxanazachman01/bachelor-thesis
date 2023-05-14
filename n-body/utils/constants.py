import os
import time
from enum import Enum

import numpy as np
import pandas as pd
import torch

HEIGHT = 800
WINDOW_SIZE = (1500, HEIGHT)
SIM_WINDOW_SIZE = (1200, HEIGHT)
light_position = [-15.0, -15.0, -15.0, 1.0]
light_ambient = [0.1, 0.1, 0.1, 1.0]
light_diffuse = [0.5, 0.5, 0.5, 1.0]
material_ambient = [0.2, 0.2, 0.2, 1.0]
material_diffuse = [0.8, 0.8, 0.8, 1.0]
material_specular = [0.2, 0.2, 0.2, 1.0]
material_shininess = 20.0


class Algorithm(Enum):
    DIRECT_SYMPLECTIC_EULER = (1, 'Direct Symplectic Euler')
    GRAPH_NEURAL_NETWORK = (2, 'Graph Neural Network')


class Processor(Enum):
    CPU = 'CPU'
    GPU = 'GPU'

# def read_raw_data(path, offset=None, nrows=None):
#     df = pd.read_csv(path, skiprows=offset, nrows=nrows, header=None)
#     df.iloc[:, :-1] = df.iloc[:, :-1].astype(float)
#     # df['m'] = df['m'] * 1e4
#     df.columns = pd.read_csv(path, nrows=1, header=None).iloc[0]
#     df = df.drop(columns=['id'])
#     return torch.DoubleTensor(df.values.tolist())
#
#
# if __name__ == "__main__":
#     index = 0
#     bodies = 50
#     global_start_time = time.perf_counter_ns()
#     for i in range(0, 6400, bodies):
#         start_time = time.perf_counter_ns()
#
#         data = read_raw_data(path=os.path.join(os.getcwd(), '..', 'star_cluster', 'c_0000.csv'), offset=i + 1,
#                              nrows=bodies)
#         np.savetxt(os.path.join(os.getcwd(), '..', 'star_cluster', 'lala', f'n_{index}.csv'),
#                    data.numpy().astype(np.float64), delimiter=',')
#         index += 1
#         if index % 10 == 0:
#             break
#
#     end_time = time.perf_counter_ns()
#     print(f"Elapsed time {index}: {(end_time - start_time) / 1e9:.4f} seconds")
# global_end_time = time.perf_counter_ns()
# print(f"Total time {index}: {(global_end_time - global_start_time) / 1e9:.4f} seconds")
