import socket
import time


class Discovery:
    def __init__(self):
        self.discovery_msg = "DISCOVER_SERVER"
        self.response_msg = "CLIENT_HERE"
        self.broadcast_ip = '255.255.255.255'
        self.server_port = 50000
        self.timeout = 3

    def listen_for_discovery(self,):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', self.server_port))

        while True:
            data, addr = sock.recvfrom(1024)
            message = data.decode()
            if message == self.discovery_msg:
                print(f"Discovery message received from {addr}, responding...")
                sock.sendto(self.response_msg.encode(), addr)

    def discover_nodes(self):
        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(self.timeout)

        # Broadcast discovery message
        print("Sending discovery broadcast...")
        sock.sendto(self.discovery_msg.encode(), (self.broadcast_ip, self.server_port))

        # Collect responses
        start = time.time()
        discovered_clients = set()
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                if data.decode() == self.RESPONSE_MSG:
                    print(f"Discovered client at {addr[0]}")
                    discovered_clients.add(addr[0])
            except socket.timeout:
                break
            if time.time() - start > self.timeout:
                break

        return list(discovered_clients)


if __name__ == "__main__":
    discover = Discovery()
    discover.listen_for_discovery()
    # discover.discover_nodes()
    