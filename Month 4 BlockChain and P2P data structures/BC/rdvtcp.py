import socket
import threading
import time

nodes = []

HEADER = 128


# create rendevous server for nodes
def rendevous():
    rsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rende_addr = ("localhost", 7000)

    # bind, listen: rende
    rsock.bind(rende_addr)
    rsock.listen()

    while True:
        clientsock, addr = rsock.accept()
        thread_sp = threading.Thread(target=start_propagation, args=(clientsock, addr))
        thread_sp.start()


def start_propagation(clientsock, caddr):
    time.sleep(3)
    response = clientsock.recv(HEADER).decode("utf-8")
    print(f"{caddr}:{response}")
    ip, port = response.split(" ")
    client = ip, port
    nodes.append(client)
    msg = str(response).encode("utf-8")
    msg_len = len(msg)
    send_len = str(msg_len).encode("utf-8")
    send_len += b" " * (HEADER - len(send_len))
    connected = True
    while connected:
        for client in nodes:
            for other_client in nodes:
                if client != other_client:
                    ip, port = other_client
                    nmsg = f"{ip} {port}".encode("utf-8")
                    # Remove the brackets and split the string into IP and port components
                    try:
                        clientsock.send(nmsg)
                        time.sleep(0.2)
                    except ConnectionResetError:
                        None


print("Starting rendevous server...")
rendevous()

""""HEADER = 1024
FORMAT = "utf-8"
SERVER = "localhost"
DISCONNECT_MESSAGE = "!DISCONNECT"


class Server:
    def __init__(self, host, port) -> None:
        self.clients = []
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print(f"Server started on {SERVER}:{self.port}")

        while True:
            clientsocket, address = self.sock.accept()
            print("waiting for clients")
            self.clients.append((clientsocket, address))
            threading.Thread(
                target=self.handle_client, args=(clientsocket, address)
            ).start()

    def handle_client(self, clientsocket, address):
        print(f"New connection: {address}\n")

        while True:
            data = clientsocket.recv(HEADER).decode(FORMAT)
            if data:
                try:
                    data_len = int(data_len)
                except ValueError:
                    continue

                data = clientsocket.recv(data_len).decode(FORMAT)
                print(f"[{address}] {data}")
                if data == DISCONNECT_MESSAGE:
                    clientsocket.close()

    def start(self):
        self.sock.bind((int(SERVER), self.port))
        self.sock.listen()
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, address = self.sock.accept()
            self.clients.append(client_socket)
            threading.Thread(
                target=self.handle_client, args=(client_socket, address)
            ).start()

    def connect_to_peer(self, peer_host, peer_port):
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            peer_socket.connect((peer_host, peer_port))
            print(f"Connected to {peer_host}:{peer_port}")
        except ConnectionRefusedError:
            print(f"Connection to {peer_host}:{peer_port} refused")
            return


if __name__ == "__main__":
    server = Server(SERVER, 8001)
    threading.Thread(target=server).start()
    print("STARTING CLIENT\n")

"""
"""import socket

laddr = int(input("Set port local: "))
raddr = int(input("Set port to connect to: "))


def bind_and_connect():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Enable the SO_REUSEADDR option
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to localhost:8000
    bind_address = ("localhost", laddr)
    client_socket.bind(bind_address)

    # Connect to the server on localhost:8001
    server_address = ("localhost", raddr)
    client_socket.connect(server_address)

    print(f"Connected to the server on {laddr}")

    # Your code logic goes here...

    # Example: Send and receive data
    client_socket.sendall(b"Hello server!")
    data = client_socket.recv(1024)
    print("Received data from server:", data.decode(), server_address)

    # Close the socket
    client_socket.close()


if __name__ == "__main__":
    bind_and_connect()"""
