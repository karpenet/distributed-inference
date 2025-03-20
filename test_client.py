import torch.nn as nn
from networking.grpc.client import GRPCNode
from backends.jetson.jetson_backend import JetsonBackend

from distributed import 


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


backend = JetsonBackend()
model = SimpleModel()
packed_model = backend.pack_model(model)


# node = GRPCNode('192.168.1.101')
node = GRPCNode('localhost')
node.connect()
node.upload_model(packed_model)
# node.say_hello()