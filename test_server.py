from backends.jetson.jetson_backend import JetsonBackend
from networking.grpc.server import GRPCServer
from orchestration.node import Node


backend = JetsonBackend()
server = GRPCServer(node=Node(backend))
server.start()

