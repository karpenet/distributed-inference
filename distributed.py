import torch.nn as nn

from backends.jetson.jetson_backend import JetsonBackend
from networking.grpc.client import GRPCNode

class Distributed(nn.Module):
    def __init__(self, model: nn.Module, device_ids: list):
        super().__init__()
        self.model = model
        self.device_ids = device_ids
        self.node_ip = {
            0: 'localhost',
            1: '192.168.1.101'
        }
        self.server = GRPCNode(self.node_ip[device_ids[0]])

    def forward(self, *inputs):
        return self.model(**inputs)

    def _init_comms(self):
        pass

    def _broadcast_model(self):
        pass

    def _broadcast_checkpoints(self):
        pass