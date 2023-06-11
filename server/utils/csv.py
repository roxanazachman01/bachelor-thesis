import pandas as pd
import torch


class CsvUtils:
    @staticmethod
    def read_star_clusters_data(path, device, offset=None, nrows=None):
        df = pd.read_csv(path, skiprows=offset, nrows=nrows, header=None)
        df.iloc[:, :-1] = df.iloc[:, :-1].astype(float)
        df.columns = pd.read_csv(path, nrows=1, header=None).iloc[0]
        df = df.drop(columns=['id'])
        return torch.tensor(df.values, dtype=torch.float64, device=device)

    @staticmethod
    def read_data(path, device, offset=None, nrows=None):
        df = pd.read_csv(path, skiprows=offset, nrows=nrows, header=None)
        df.iloc[:, :] = df.iloc[:][:].astype(float)
        return torch.tensor(df.values, dtype=torch.float64, device=device)
