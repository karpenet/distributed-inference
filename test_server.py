import torch.nn as nn
from backends.jetson.jetson_backend import JetsonBackend
from networking.udp.discover_nodes import Discovery
from networking.grpc.server import GRPCServer

class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc1 = nn.Linear(10, 50)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(50, 1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

discovery = Discovery()
backend = JetsonBackend()

nodes = discovery.discover_nodes()
packed_model = backend.pack_model(SimpleModel())

server = GRPCServer('10.0.0.173', '8000')
server.start()