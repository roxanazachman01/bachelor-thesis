import pandas as pd
import torch


class CsvUtils:
    @staticmethod
    def read_data(path, offset=None, nrows=None):
        df = pd.read_csv(path, skiprows=offset, nrows=nrows, header=None)
        df.iloc[:, :] = df.iloc[:][:].astype(float)
        return torch.tensor(df.values, dtype=torch.float64)
