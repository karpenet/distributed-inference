import grpc
import node_service_pb2
import node_service_pb2_grpc


class GRPCNode:
    def __init__(self):
        self.stub = None
        self.address = None
        self.channel = None
        self.channel_options = []

    def connect(self):
        self.channel = grpc.insecure_channel(
            # self.address,
            'localhost:50051'
            # channel_options=self.channel_options,
        )
        self.stub = node_service_pb2_grpc.NodeServiceStub(self.channel)

    def disconnect(self):
        pass

    def say_hello(self):
        response = self.stub.SayHello(node_service_pb2.HelloRequest(name="KedarKarpe"))
        print("Greeter client received:", response.message)

    def send_checkpoint(self):
        request = node_service_pb2.ModelRequest(model_file=model_data)
        result = self.stub.CheckpointRequest(request)
        print(f"Jetson {self.address} - Accuracy: {result.accuracy}, Loss: {result.loss}, Notes: {result.notes}")

if __name__ == "__main__":
    node = GRPCNode()
    node.connect()
    node.say_hello()

