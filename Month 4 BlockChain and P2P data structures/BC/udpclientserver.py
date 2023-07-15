import socket
import threading
import random
from blockchain import (
    Block,
    blockchain,
    bc_client as bc_client,
    blockpool as blockpool,
    add_tx_to_pool,
    main,
)


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

    bc_main_flag = True

    while True:
        data = server.recv(1024).decode("utf-8")
        if data.startswith("tx:"):
            info, sender, amount, receiver = data.split(":")
            tx = sender, amount, receiver
            info = str(info)
            sender = str(sender)
            amount = int(amount)
            receiver = str(receiver)

            print(f"New transaction:{tx, type(tx)}\n")
            add_tx_to_pool(tx)

            if bc_main_flag:
                returned_block = main(tx)
                broad_cast_new_block(block=returned_block)
                print("Returned block:\n", returned_block)

        elif data.startswith("bcu:"):
            print("bcu received:")
            print(data, "\n")
            info, number, received_data, previous_hash, nonce, timestamp = data.split(
                ":"
            )
            info = str(info)
            number = int(number)
            received_data = str(received_data)
            previous_hash = str(previous_hash)
            nonce = int(nonce)
            timestamp = str(timestamp)
            bcu_block = Block(number, previous_hash, received_data, 0, timestamp)
            blockchain.mine(bcu_block)
            bc_main_flag = False
        bc_main_flag = True


def receive_client():
    while True:
        data = sock.recv(1024).decode()
        print(data)
        if data == "AKK":
            print("Rendevous server is finished propagating\n")
            break

        ip, sport, dport = data.split(" ")
        print("receiveing client\n")
        print("IP:", ip)

        sport = int(sport)
        dport = int(dport)
        client = ip, sport, dport

        print("printing client:", client)

        if client not in clients:
            bc_client.add_clients(client)
            clients.append(client)
            print("BC clients list:", bc_client.clients)
        elif client in clients:
            sock.sendto(b"AKK\n", rendevous_server)

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


def broad_cast_new_block(block):
    number = block.number
    data = block.data
    previous = block.previous
    nonce = block.nonce
    timestamp = block.timestamp
    bcu = (
        "bcu"
        + ":"
        + str(number)
        + ":"
        + str(data)
        + ":"
        + str(previous)
        + ":"
        + str(nonce)
        + ":"
        + str(timestamp)
    )
    msg = bcu

    print(f"broadcasting new block\n")
    print(f"block to broadcast: {msg}\n")
    for client in clients:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(msg.encode(), (client[0], client[1]))
        client_socket.close()


def test_tx():
    amount = random.randint(10, 100)
    accounts = ["abc", "def", "ghi", "qwd", "gtr"]
    first_account = random.choice(accounts)
    remaining_accounts = [account for account in accounts if account != first_account]
    second_account = random.choice(remaining_accounts)
    tx = str(first_account), str(amount), str(second_account)
    return tx


while True:
    msg = input(">")
    if msg == "show_bc":
        for block in blockchain.chain:
            print(block)
    elif msg == "show_nodes":
        print(list(show_nodes()))
    elif msg == "new_propagation":
        break
    elif msg.startswith("tx:"):
        tx_tuple = test_tx()
        tx = tx_tuple
        for data in tx:
            first_account, amount, second_account = tx

        print(f"New transaction:{tx, type(tx)}\n")
        add_tx_to_pool(tx)
        tx = str(first_account) + ":" + str(amount) + ":" + str(second_account)
        msg_tx = msg + tx

        for client in clients:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.sendto(msg_tx.encode(), (client[0], client[1]))
            client_socket.close()

        if True:
            returned_block = main(tx_tuple)
            broad_cast_new_block(returned_block)
            print("Returned block:\n", returned_block)
    else:
        for client in clients:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.sendto(msg.encode(), (client[0], client[1]))
            client_socket.close()
