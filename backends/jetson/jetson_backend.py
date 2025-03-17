import torch
import torch.nn as nn
import io
from ..backends import BaseBackend


class JetsonBackend(BaseBackend):
    def pack_model(self, model: nn.Module):
        packed_model = io.BytesIO()
        torch.jit.script(model, packed_model)
        return packed_model

    def unpack_model(self, packed_model: io.BytesIO):
        return torch.jit.load(packed_model)