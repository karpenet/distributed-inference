import socket
import time
import netifaces  # You'll need to install this: pip install netifaces


class Discovery:
    def __init__(self):
        self.discovery_msg = "DISCOVER_SERVER"
        self.response_msg = "CLIENT_HERE"
        self.broadcast_ip = '255.255.255.255'
        self.server_port = 50000
        self.timeout = 3
        self.ethernet_interfaces = self.get_ethernet_interfaces()

    def get_ethernet_interfaces(self):
        """Identify ethernet interfaces and their IP addresses."""
        ethernet_ips = []
        
        # Common ethernet interface name patterns
        ethernet_patterns = ['eth', 'en', 'em', 'eno', 'enp', 'Ethernet']
        
        for interface in netifaces.interfaces():
            # Skip loopback and wireless interfaces
            if interface == 'lo' or interface.startswith(('wl', 'ww', 'wi')):
                continue
                
            # Check if interface name matches ethernet patterns
            is_ethernet = any(pattern in interface for pattern in ethernet_patterns)
            
            if is_ethernet and netifaces.AF_INET in netifaces.ifaddresses(interface):
                for link in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                    if 'addr' in link:
                        ethernet_ips.append(link['addr'])
        
        print(f"Found ethernet interfaces with IPs: {ethernet_ips}")
        return ethernet_ips

    def listen_for_discovery(self):
        # Check if we have ethernet interfaces
        if not self.ethernet_interfaces:
            print("No ethernet interfaces found. Cannot listen for discovery.")
            return
            
        # Create socket for each ethernet interface
        for ip in self.ethernet_interfaces:
            # Run in separate thread for each interface
            # This is a simplified example - in production code, use threading
            self._listen_on_interface(ip)
    
    def _listen_on_interface(self, ip):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((ip, self.server_port))
        
        print(f"Listening for discovery on interface with IP: {ip}")
        
        while True:
            data, addr = sock.recvfrom(1024)
            message = data.decode()
            if message == self.discovery_msg:
                print(f"Discovery message received from {addr}, responding...")
                sock.sendto(self.response_msg.encode(), addr)

    def discover_nodes(self):
        # Check if we have ethernet interfaces
        if not self.ethernet_interfaces:
            print("No ethernet interfaces found. Cannot discover nodes.")
            return []
            
        discovered_clients = set()
        
        # Discover on each ethernet interface
        for ip in self.ethernet_interfaces:
            clients = self._discover_on_interface(ip)
            discovered_clients.update(clients)
            
        return list(discovered_clients)
    
    def _discover_on_interface(self, interface_ip):
        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(self.timeout)
        
        # Bind to specific interface
        sock.bind((interface_ip, 0))
        
        # Broadcast discovery message
        print(f"Sending discovery broadcast from {interface_ip}...")
        sock.sendto(self.discovery_msg.encode(), (self.broadcast_ip, self.server_port))

        # Collect responses
        start = time.time()
        discovered_clients = set()
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                if data.decode() == self.response_msg:  # Fixed attribute name
                    print(f"Discovered client at {addr[0]}")
                    discovered_clients.add(addr[0])
            except socket.timeout:
                break
            if time.time() - start > self.timeout:
                break

        return discovered_clients


if __name__ == "__main__":
    discover = Discovery()
    # To listen for discovery requests
    discover.listen_for_discovery()
    
    # To discover nodes
    # nodes = discover.discover_nodes()
    # print(f"Discovered nodes: {nodes}")
    