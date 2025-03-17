import grpc
import node_service_pb2
import node_service_pb2_grpc


class GRPCNode:
    def __init__(self, address):
        self.stub = None
        self.address = address
        self.channel = None
        self.channel_options = []

    def connect(self):
        self.channel = grpc.insecure_channel(
            f"{self.address}:50051",
            channel_options=self.channel_options,
        )
        self.stub = node_service_pb2_grpc.NodeServiceStub(self.channel)

    def disconnect(self):
        pass

    def say_hello(self):
        response = self.stub.SayHello(node_service_pb2.HelloRequest(name="KedarKarpe"))
        print("Greeter client received:", response.message)

    def upload_model(self, model):
        request = node_service_pb2.ModelRequest(model_file=model)
        result = self.stub.CheckpointRequest(request)
        print(result)

    def upload_checkpoint(self, model_checkpoint):
        request = node_service_pb2.ModelRequest(model_file=model_checkpoint)
        result = self.stub.CheckpointRequest(request)
        print(result)

if __name__ == "__main__":
    node = GRPCNode()
    node.connect()
    node.say_hello()

