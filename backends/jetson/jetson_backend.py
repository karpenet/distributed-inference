import torch
import torch.nn as nn
import io
from ..backends import BaseBackend


class JetsonBackend(BaseBackend):
    def pack_model(self, model: nn.Module):
        packed_model = io.BytesIO()
        jit_model = torch.jit.script(model)
        torch.jit.save(jit_model, packed_model)
        packed_model.seek(0)
        return packed_model.getvalue()

    def unpack_model(self, packed_model_bytes: io.BytesIO):
        packed_model = io.BytesIO(packed_model_bytes)
        return torch.jit.load(packed_model)

    def download_model(self, packed_model_bytes: io.BytesIO):
        model_buffer = io.BytesIO(packed_model_bytes)
        model_buffer.seek(0)
        model = torch.jit.load(model_buffer)
        torch.jit.save(model, 'model.pt')

        print(model(torch.randn(10)))