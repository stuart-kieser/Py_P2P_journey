import socket
import threading
import blockchain
from blockchain import blockchain_broadcast_update
import random

tx_to_pool = blockchain.add_tx_to_pool
bc_update = blockchain.blockchain_broadcast_update
bc = blockchain.Blockchain()
block = blockchain.Block()
btx = blockchain.test_tx
bc_main = blockchain.main

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
sock.bind(("localhost", (PORT + 10)))
sock.sendto(b"55555", rendevous_server)
print(f"Binding on port: {PORT}, sending bytes to: {rendevous_server}")


def listen():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("localhost", PORT))

    while True:
        data = server.recv(1024).decode("utf-8")
        print(data)
        if data.startswith("tx:"):
            info, sender, amount, receiver = data.split(":")
            tx = sender, amount, receiver
            info = str(info)
            sender = str(sender)
            amount = int(amount)
            receiver = str(receiver)

            print(f"New transaction:{tx, type(tx)}\n")
            tx_to_pool(tx)
            bc_main(tx)

            print(f"transaction updated:\n {tx}\n")

        elif data.startswith("bcu:"):
            info, number, data, previous, nonce, timestamp = data.split(":")
            info = str(info)
            number = int(number)
            data = str(data)
            previous = str(previous)
            nonce = int(nonce)
            timestamp = float(timestamp)
            block_data = number, data, previous, nonce, timestamp

            blockchain_broadcast_update(args=block_data)

            print(f"blockchain updated:\n {block}\n")

            print(blockchain_broadcast_update(args=block_data), "\n")

        else:
            None


def receive_client():
    while True:
        data = sock.recv(1024).decode()
        print(data)
        if data == "AKK":
            print("Rendevous server is finished propagating")
            break

        ip, sport, dport = data.split(" ")
        print("receiveing client\n")
        print("IP:", ip)

        sport = int(sport)
        dport = int(dport)
        client = ip, sport, dport

        print("printing client:", client)

        if client not in clients:
            clients.append(client)
        elif client in clients:
            sock.sendto(b"AKK", rendevous_server)

        print("\nGot peers")
        for client in clients:
            print("ip:{}".format(client[0]))
            print("sport:{}".format(client[1]))
            print("dport:{}\n".format(client[2]))
        print("Punching hole...")
        print("Data exchange is ready\n")


listener = threading.Thread(target=listen, daemon=True)
receiver = threading.Thread(target=receive_client, daemon=True)

while True:
    data = sock.recv(1024).decode()
    print(f"receving data:\n")
    print(data)

    if data.strip() == "AKK":
        print("checked in with server, waiting")
        break

print("Waiting to receive other client addresses")

receiver.start()
listener.start()

print("Listening for BC updates:")


def show_nodes():
    return clients


def test_tx():
    amount = random.randint(10, 100)
    accounts = ["abc", "def", "ghi", "qwd", "gtr"]
    first_account = random.choice(accounts)
    remaining_accounts = [account for account in accounts if account != first_account]
    second_account = random.choice(remaining_accounts)
    tx = str(first_account), str(amount), str(second_account)
    print(type(tx))
    print(f"transaction update: {tx}")
    return tx


while True:
    msg = input("> ")
    if msg == "!q":
        quit()
    elif msg == "show_nodes()":
        print(list(show_nodes()))
    elif msg == "new_propagation":
        break
    elif msg.startswith("tx:"):
        tx_tuple = test_tx()
        tx = tx_tuple
        for data in tx:
            first_account, amount, second_account = tx
        tx_to_pool(tx)
        tx = str(first_account) + ":" + str(amount) + ":" + str(second_account)
        msg_tx = msg + tx
        print(msg_tx)
        for client in clients:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.sendto(msg_tx.encode(), (client[0], client[1]))
            client_socket.close()
        bc_main(tx_tuple)
    else:
        for client in clients:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.sendto(msg.encode(), (client[0], client[1]))
            client_socket.close()
