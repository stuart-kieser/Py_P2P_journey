import socket
import threading
import time
from tests_p2p import test_tx
from blockchain import (
    Block,
    wallet,
    blockchain,
    bc_client as bc_client,
    blockpool as blockpool,
    add_tx_to_pool,
    main,
    wallet_addrs,
)


nodes = []


clients_got = False

main_addr = ("localhost", int(input("Select main node port")))

HEADER = 128


def show_nodes():
    return nodes


# creates block from incoming tx: data
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
    broadcast_to_clients(msg)


def server():
    print(f"Starting server: {main_addr}")
    # create the server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket and listen for incoming requests
    sock.bind(main_addr)
    sock.listen()
    # accept incoming connections
    while True:
        clientsock, addr = sock.accept()
        thread_hc = threading.Thread(
            target=handle_client, args=(clientsock, addr), daemon=True
        )
        thread_hc.start()


def handle_client(clientsocket, addr):
    bc_main_flag = True
    while True:
        data = clientsocket.recv(1024).decode("utf-8")
        # signifies new tx update
        if data.startswith("tx:"):
            print(f"DATA:{data}\n")
            info, sender, amount, receiver, node = data.split(":")
            info = str(info)
            sender = str(sender)
            amount = int(amount)
            receiver = str(receiver)
            node = str(node)
            tx = sender, amount, receiver

            print(f"New transaction:{tx, type(tx)}\n")
            add_tx_to_pool(tx)

        # new public key registration
        elif data.startswith("public_keyr:"):
            print(f"DATA:{data}\n")
            info, public_key = data.split(":")
            info = str(info)
            public_key = str(public_key)
            tx = info, public_key

            # check if key exists in bc history
            wallet_addrs(public_keyn)
            print(f"public key request:{tx, type(tx)}\n")

        elif data.startswith("public_keyn:"):
            print(f"DATA:{data}\n")
            info, public_keyn = data.split(":")
            info = str(info)
            public_key = str(public_key)
            tx = info, public_key

            # add wallet to tx
            add_tx_to_pool(tx)
            wallet.add_wallet(public_key)

        # signifies block chain update
        elif data.startswith("bcu:"):
            print(f"DATA:{data}\n")
            (
                info,
                number,
                received_data,
                previous_hash,
                nonce,
                timestamp,
                node,
            ) = data.split(":")
            info = str(info)
            number = int(number)
            received_data = str(received_data)
            previous_hash = str(previous_hash)
            nonce = int(nonce)
            timestamp = str(timestamp)
            node = str(node)
            bcu_block = Block(number, previous_hash, received_data, 0, timestamp)
            blockchain.mine(bcu_block)
            bc_main_flag = False

        elif data == "bc":
            bcthread.start()


def client():
    # create client socket to communicate with server
    csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_addr = ("localhost", int(input("select a node client port:\n")))
    print(f"Starting client on:{client_addr}\n")

    # bind socket to local addr
    csock.bind(client_addr)

    # connect to server
    node_addr = ("localhost", 7000)
    csock.connect(node_addr)
    ip, port = main_addr
    msg = f"{ip} {port}"
    csock.sendall(f"{msg}".encode("utf-8"))
    # main loop to accept in propagated clients
    connected = True
    while connected:
        data = csock.recv(HEADER).decode()
        try:
            ip, port = data.split(" ")
            node = str(ip), int(port)
            if node not in nodes:
                bc_client.add_clients(node)
                nodes.append(node)
                print(f"DATA:{node}")
        except ValueError:
            connected = False


def broadcast_to_clients(msg):
    print("connecting to clients")
    for client in nodes:
        if client != main_addr:
            bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bcsock.bind(("localhost", 0))
            bcsock.connect(client)
            bcsock.send(f"{msg}:{main_addr}".encode("utf-8"))
            bcsock.close()


sthread = threading.Thread(target=server)
cthread = threading.Thread(target=client)
bcthread = threading.Thread(target=main)

sthread.start()
cthread.start()

time.sleep(1)


def server_main():
    while True:
        msg = input(">")
        if msg == "show_bc":
            for block in blockchain.chain:
                print(block)

        elif msg == "show_nodes":
            print(list(show_nodes()))

        elif msg == "create wallet":
            own_wallet = wallet()
            own_wallet.private_key
            own_wallet.public_key
            own_wallet.key_base

        elif msg.startswith("tx:"):
            tx_tuple = test_tx()
            tx = tx_tuple
            first_account, amount, second_account = tx
            add_tx_to_pool(tx)
            tx = str(first_account) + ":" + str(amount) + ":" + str(second_account)
            msg_tx = msg + tx
            print(f"New transaction:{msg_tx, type(tx)}\n")
            broadcast_to_clients(msg_tx)


if __name__ == "__main__":
    server_main()
