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
rendevous_server = ("localhost", 55555)
clients = []

PORT = int(input("select a port in the range 8000 - 9000:"))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("localhost", PORT))
sock.sendto(b"55555", rendevous_server)
print(f"Binding on port: {PORT}, sending bytes to: {rendevous_server}")


def listen():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("localhost", PORT))

    while True:
        data = server.recv(1024)
        print("\rpeer: {}\n> ".format(data.decode("utf-8")), end="")


listener = threading.Thread(target=listen, daemon=True)

while True:
    data = sock.recv(1024).decode()
    print(f"receving data:\n")
    print(data)

    if data.strip() == "AKK":
        print("checked in with server, waiting")
        break

print("Waiting to receive other client addresses")

data = sock.recv(1024).decode()
sock.close()
listener.start()

print(f"peer details:{data}")

ip, sport, dport = data.split(" ")
sport = int(sport)
dport = int(dport)
clients.append(data)


print("\nGot peer")
print("ip:{}".format(ip))
print("sport:{}".format(sport))
print("dport:{}\n".format(dport))
print("Punching hole...")
print("Data exchange is ready\n")


print("Listening for BC updates:")


def show_nodes():
    return clients


while True:
    msg = input("> ")
    if msg == "!q":
        quit()
    elif msg == "show_nodes()":
        print(list(show_nodes()))
    else:
        for data in clients:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.sendto(msg.encode(), (ip, sport))
            client_socket.close()
