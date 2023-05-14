import torch
from torch_geometric.data import Data
from torch_geometric.typing import SparseTensor, Union, torch_scatter
from torch_geometric.nn import MessagePassing
from torch import Tensor, nn


class FeatureMLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        # input dim = nr_features*nr_nodes
        super(FeatureMLP, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim).to(torch.float64)
        self.fc2 = nn.Linear(hidden_dim, output_dim).to(torch.float64)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out


class Encoder(nn.Module):
    def __init__(self, node_channels, edge_channels, hidden_size=16):
        super(Encoder, self).__init__()
        self.node_mlp = FeatureMLP(node_channels, hidden_size, node_channels)
        self.edge_mlp = FeatureMLP(edge_channels, hidden_size, edge_channels)

    def forward(self, x, edge_attr):
        x = self.node_mlp(x)
        edge_attr = self.edge_mlp(edge_attr)
        return x, edge_attr


class Processor(MessagePassing):
    def __init__(self, node_channels, edge_channels):
        super(Processor, self).__init__(aggr='add')
        self.node_mlp = FeatureMLP(node_channels + edge_channels, 32, node_channels)
        self.edge_mlp = FeatureMLP(2 * node_channels + edge_channels, 32, edge_channels)

    def message_and_aggregate(self, adj_t: Union[SparseTensor, Tensor]) -> Tensor:
        pass

    def edge_update(self) -> Tensor:
        pass

    def aggregate(self, inputs, index):
        out = torch_scatter.scatter(inputs, index, dim=self.node_dim, reduce="sum")
        return (inputs, out)

    def update(self, aggr_out):
        # aggr_out is the output of the message aggregation step.
        # x is the node feature matrix of shape [num_nodes, node_channels].

        # Update node features with residual connection.
        return aggr_out

    def message(self, x_i, x_j, edge_feature):
        """
        Creates message of shape [num_edges, 2*num_node_feats+num_edge_features]
        Encodes message to shape [num_edges, num_edge_features]
        :param x_i: features for each source node, shape [num_edges, num_node_feats]
        :param x_j: features for each target node, shape [num_edges, num_node_feats]
        :param edge_feature: edge features, shape [num_edges, num_edge_features]
        :return:
        """
        edge_msg = torch.cat((x_i, x_j, edge_feature), dim=-1)
        edge_msg = self.edge_mlp(edge_msg)
        return edge_msg

    def forward(self, x, edge_index, edge_feature):
        # x is the node feature matrix of shape [num_nodes, node_channels].
        # edge_index is a tuple of LongTensors representing the edge connectivity in COO format.
        # edge_attr is the edge feature matrix of shape [num_edges, edge_channels].

        edge_out, aggr = self.propagate(edge_index, x=(x, x), edge_feature=edge_feature)
        node_out = self.node_mlp(torch.cat((x, aggr), dim=-1))
        edge_out = edge_feature + edge_out
        node_out = x + node_out
        return node_out, edge_out


class Decoder(nn.Module):
    def __init__(self, node_channels, hidden_size=16):
        super(Decoder, self).__init__()
        self.node_mlp = FeatureMLP(node_channels, hidden_size, 3)

    def symplectic_euler_integrator(self, nodes_r, nodes_v, acc, dt=0.005):
        nodes_v = torch.cat((nodes_v[:, 3:], nodes_v[:, -3:] + acc * dt), dim=1)
        nodes_r += nodes_v[:, -3:] * dt
        return nodes_r, nodes_v

    def forward(self, x, dt=0.005, data=None, get_graph=False):
        acc_y = self.node_mlp(x)
        if not get_graph:
            return acc_y
        nodes_r = data.x[:, :3]
        nodes_v = data.x[:, -7:-4]
        nodes_r, nodes_v = self.symplectic_euler_integrator(nodes_r, nodes_v, acc_y, dt)

        new_x = torch.cat((nodes_r, nodes_v), dim=1)
        edge_index = data.edge_index
        rij = nodes_r[edge_index[0]] - nodes_r[edge_index[1]]
        return Data(x=new_x, edge_index=edge_index, edge_attr=rij, pos=nodes_r, y=acc_y)


class SimulatorModel(torch.nn.Module):
    def __init__(self,
                 hidden_size=64,
                 n_mp_layers=10,  # number of GNN layers
                 num_node_features=18,
                 num_edge_features=3,
                 dim=3,  # dimension of the world, typical 2D or 3D
                 window_size=5,  # the model looks into W frames before the frame to be predicted
                 ):
        super().__init__()
        self.encoder = Encoder(num_node_features, num_edge_features, hidden_size=hidden_size)
        self.decoder = Decoder(num_node_features)
        self.n_mp_layers = n_mp_layers
        self.layers = torch.nn.ModuleList([Processor(num_node_features, num_edge_features) for _ in range(n_mp_layers)])

    def reset_parameters(self):
        torch.nn.init.xavier_uniform_(self.embed_type.weight)

    def forward(self, data, get_graph=False):
        # pre-processing
        # node feature: combine categorical feature data.x and contiguous feature data.pos.
        node_encoded, edge_encoded = self.encoder(data.x, data.edge_attr)
        # stack of GNN layers
        for i in range(self.n_mp_layers):
            node_encoded, edge_encoded = self.layers[i](node_encoded, data.edge_index, edge_feature=edge_encoded)

        # post-processing
        out = self.decoder(node_encoded, data=data, get_graph=get_graph)
        return out
