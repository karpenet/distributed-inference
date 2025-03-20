import grpc
from concurrent import futures
from networking.grpc import node_service_pb2
from networking.grpc import node_service_pb2_grpc
import torch
from orchestration.node import Node


class GRPCServer(node_service_pb2_grpc.NodeServiceServicer):
    def __init__(self, node: Node):
        self.node = node
        self.server = None

    def start(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        node_service_pb2_grpc.add_NodeServiceServicer_to_server(self, self.server)
        self.server.add_insecure_port('[::]:50051')
        self.server.start()
        print("Server started on port 50051.")
        self.server.wait_for_termination()

    def stop(self):
        if self.server:
            self.server.stop(grace=5)
            self.server.wait_for_termination()

    def SendModel(self, request, context):
        print("Received model bytes:", len(request.model_file))
        self.node.download_model(request.model_file)
        return node_service_pb2.Empty()
        
    def SendCheckpoint(self, request, context):
        # Do something
        tensor_data = None
        result = None
        return node_service_pb2.Tensor(tensor_data=tensor_data, shape=result.shape, dtype=str(result.dtype)) if result is not None else node_service_pb2.Tensor()


if __name__ == "__main__":
    server = GRPCServer('10.0.0.173', '8000')
    server.start()
