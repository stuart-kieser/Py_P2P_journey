import socket
import threading
import queue
import blockchain
import random

# this module is for receiving BC updates such as:

"""
BC block mintings
BC transaction updates
BC node bans
BC node updates
"""

msg = queue.Queue()
clients = []

PORT = int(input("select a port in the range 8000 - 9000:"))

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", PORT))


def show_nodes():
    return clients


def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            msg.put((message, addr))
        except:
            pass


def broadcast():
    while True:
        while not msg.empty():
            message, addr = msg.get()
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                try:
                    decoded_message = message.decode("utf-8")
                    if decoded_message.startswith("BCU:"):
                        message_parts = decoded_message.split(":")[1:]
                        if len(message_parts) == 5:
                            number, data, previous, nonce, timestamp = message_parts
                        blockchain.mine(
                            blockchain.Block(number, data, previous, nonce, timestamp)
                        )
                        server.sendto("AKK".encode(), addr)
                    else:
                        server.sendto(message, client)
                except:
                    clients.remove(client)


t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)


t1.start()
t2.start()

print(f"Server is listening on PORT[{PORT}]")


while True:
    message = input("")
    if message == "!q":
        quit()
    elif message == "show_nodes()":
        print(show_nodes())
    else:
        for client in clients:
            for addr in client:
                server.sendto(message.encode(), ("localhost", addr))
