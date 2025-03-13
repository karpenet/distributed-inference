import grpc
from concurrent import futures
import node_service_pb2
import node_service_pb2_grpc


class GRPCServer(node_service_pb2_grpc.NodeServiceServicer):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server = None

    def start(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        node_service_pb2_grpc.add_NodeServiceServicer_to_server(self, self.server)
        address = f"{self.host}:{self.port}"
        self.server.add_insecure_port('[::]:50051')
        self.server.start()
        print(f"Server started on port {self.port}.")
        self.server.wait_for_termination()

    def stop(self):
        if self.server:
            self.server.stop(grace=5)
            self.server.wait_for_termination()
        
    def SendCheckpoint(self, request, context):
        # Do something
        tensor_data = None
        result = None
        return node_service_pb2.Tensor(tensor_data=tensor_data, shape=result.shape, dtype=str(result.dtype)) if result is not None else node_service_pb2.Tensor()

    def SayHello(self, request, context):
        return node_service_pb2.HelloReply(message=f"Hello, {request.name}!")


if __name__ == "__main__":
    server = GRPCServer('10.0.0.173', '8000')
    server.start()
