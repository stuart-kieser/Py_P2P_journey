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
)

nodes = []

clients_got = False

main_addr = ("localhost", int(input("Select main node port")))

HEADER = 128


def show_nodes():
    return nodes


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
    connected = True
    bc_main_flag = True
    while True:
        data = clientsocket.recv(1024).decode("utf-8")
        # signifies new tx update
        if data.startswith("tx:"):
            print(f"DATA:{data}")
            info, sender, amount, receiver, node = data.split(":")
            tx = sender, amount, receiver
            info = str(info)
            sender = str(sender)
            amount = int(amount)
            receiver = str(receiver)
            node = str(node)

            print(f"New transaction:{tx, type(tx)}\n")
            add_tx_to_pool(tx)

            if bc_main_flag:
                returned_block = main(tx)
                broad_cast_new_block(block=returned_block)
                print("\nReturned block:", returned_block)


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
        ip, port = data.split(" ")
        node = str(ip), int(port)
        if node not in nodes:
            nodes.append(node)
            print(f"DATA:{node}")
        else:
            time.sleep(3)
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

sthread.start()
cthread.start()

time.sleep(1)
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
        for data in tx:
            first_account, amount, second_account = tx
        add_tx_to_pool(tx)
        tx = str(first_account) + ":" + str(amount) + ":" + str(second_account)
        msg_tx = msg + tx
        print(f"New transaction:{msg_tx, type(tx)}\n")
        broadcast_to_clients(msg_tx)

        if True:
            returned_block = main(tx_tuple)
            broad_cast_new_block(returned_block)
            print("Returned block:\n", returned_block)
