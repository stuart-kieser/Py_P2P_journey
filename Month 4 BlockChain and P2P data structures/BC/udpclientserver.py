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

msg_ = []
clients = []

PORT = int(input("select a port in the range 8000 - 9000:"))

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", PORT))
server.sendto(b"0", rendevous_server)


while True:
    data = server.recv(1024).decode()

    if data.strip() == "ready":
        print("checked in with server, waiting")
        break

data = server.recv(1024).decode()
ip, sport, dport = data.split(" ")
sport = int(sport)
dport = int(dport)
clients.append({ip: any, sport: int, dport: int})


print("\nGot peer")
print("ip:{}".format(ip))
print("sport:{}".format(sport))
print("dport:{}\n".format(dport))
print("Punching hole...")


server.sendto(b"0", (ip, dport))

print("Data exchange is ready")


def show_nodes():
    return clients


def listen():
    while True:
        data = server.recv(1024)
        msg_.append(data)
        print("\rpeer: {}\n> ".format(data.decode("utf-8")), end="")


listener = threading.Thread(target=listen, daemon=True)
listener.start()


def broadcast():
    while True:
        for data in list(msg.queue):
            try:
                decoded_message = msg.decode("utf-8")
                if decoded_message.startswith("BCU:"):
                    message_parts = decoded_message.split(":")[1:]
                    if len(message_parts) == 5:
                        number, data, previous, nonce, timestamp = message_parts
                    blockchain.mine(
                        blockchain.Block(number, data, previous, nonce, timestamp)
                    )
                    server.sendto("AKK".encode(), sport)
                else:
                    server.sendto(msg, sport)
            except:
                msg.remove(data)


t2 = threading.Thread(target=broadcast)

while True:
    msg = input("> ")
    if msg == "!q":
        quit()
    elif msg == "show_nodes()":
        print(list(show_nodes()))
    else:
        for client in clients:
            ip, sport, dport = client
            server.sendto(msg.encode(), (ip, sport))
