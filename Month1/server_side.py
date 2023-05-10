import socket
import random

IP = socket.gethostbyname(socket.gethostname())
PORT = 10000

clients = {}


class Server:
    def __init__(self):
        self.socket_handle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_handle.bind((IP, PORT))
        self.socket_handle.listen()

    def add_client(self):
        conn, addr = self.socket_handle.recv(1024).decode()
        clients[addr] = conn
        return conn


class HoldConnection(Server):
    def __init__(self):
        super().__init__(self)

    def handle_client(self, conn):
        while True:
            try:
                data = self.socket_handle.recv(1024).decode()
                if not data:
                    break

                result = self.process_data(data)
                return result
            except:
                break
        self.socket_handle.close()

    def process_data(self, data):
        return f"received bytes: {data}"

    def run(self):
        while True:
            conn = self.socket_handle.accept()
            self.handle_client(conn)


class FindConnection(Server):
    def __init__(self):
        super().__init__()

    def find_conn(self):
        if not clients:
            return None

        addr = random.choice(clients.keys())
        conn = clients[addr]
        try:
            conn.connect_ex(addr)
        except:
            return None
