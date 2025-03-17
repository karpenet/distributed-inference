from backends.jetson.jetson_backend import JetsonBackend
from networking.grpc.server import GRPCServer



backend = JetsonBackend()
server = GRPCServer()
server.start()

