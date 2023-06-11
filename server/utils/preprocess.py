import torch

from torch_geometric.data import Data

from utils.constants import G


class Preprocessor:
    @staticmethod
    def __simulate(data, steps=4, dt=0.005, device=torch.device('cpu')):
        num_particles = len(data)
        nodes_r = data[:, :3]
        nodes_v = data[:, 3:6]
        nodes_mass = data[:, -1]
        edges = torch.combinations(torch.arange(num_particles, device=device), r=2).T
        total_forces = torch.zeros((num_particles, 3), device=device)
        for _ in range(steps):
            rij = nodes_r[edges[0]] - nodes_r[edges[1]]
            r = torch.sqrt(torch.sum(rij ** 2, dim=1))
            mass_prod = nodes_mass[edges[0]] * nodes_mass[edges[1]]
            mass_prod = mass_prod.unsqueeze(1)
            forces = G * mass_prod * rij / (r ** 3).unsqueeze(1)
            for i in range(edges.shape[1]):
                total_forces[edges[0][i]] += forces[i]
                total_forces[edges[1][i]] -= forces[i]
            acceleration = total_forces / nodes_mass.unsqueeze(1)
            nodes_v = torch.cat((nodes_v, nodes_v[:, -3:] + acceleration * dt), dim=1)
            nodes_r += nodes_v[:, -3:] * dt
            total_forces.fill_(0)

        rij = nodes_r[edges[0]] - nodes_r[edges[1]]
        r = torch.sqrt(torch.sum(rij ** 2, dim=1))
        mass_prod = nodes_mass[edges[0]] * nodes_mass[edges[1]]
        mass_prod = mass_prod.unsqueeze(1)
        forces = G * mass_prod * rij / (r ** 3).unsqueeze(1)
        for i in range(edges.shape[1]):
            total_forces[edges[0][i]] += forces[i]
            total_forces[edges[1][i]] -= forces[i]
        acceleration = total_forces / nodes_mass.unsqueeze(1)

        return nodes_r, nodes_v, acceleration, edges, nodes_mass

    @staticmethod
    def get(content, dt=0.005, steps=4, device=torch.device('cpu')):
        raw_data = torch.tensor(content, dtype=torch.double, device=device)
        nodes_r, nodes_v, acceleration, edges, mass = Preprocessor.__simulate(raw_data, dt=dt, steps=steps,
                                                                              device=device)

        num_particles = len(raw_data)

        nodes_feats = torch.cat((nodes_r, nodes_v), dim=1).to(device)

        edge_index = torch.combinations(torch.arange(num_particles), r=2).to(device)
        edge_index = torch.cat([edge_index, edge_index.flip(dims=(1,))]).T.to(device)

        rij = nodes_r[edge_index[0]] - nodes_r[edge_index[1]]

        return Data(x=nodes_feats, edge_index=edge_index, edge_attr=rij, pos=nodes_r, y=acceleration), mass
