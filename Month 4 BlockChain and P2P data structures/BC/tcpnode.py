import socket
import threading
import time
from blockchain import (
    Block,
    block,
    Wallet,
    blockchain,
    clients as clients,
    blockpool as blockpool,
    add_tx_to_pool,
    wallet_addrs,
    tx_pool,
)


nodes = []

main_addr = ("localhost", int(input("Select main node port")))
mip, mport = main_addr

HEADER = 128


def show_nodes():
    return nodes


# creates block to send to clients
def own_block(block):
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
            if tx not in tx_pool:
                add_tx_to_pool(tx)

        # new public key registration
        elif data.startswith("public_keyr:"):
            print(f"DATA:{data}\n")
            info, public_key, node = data.split(":")
            info = str(info)
            public_key = str(public_key)
            node = str(node)
            tx = info, public_key

            # check if key exists in bc history
            wallet_addrs(public_key)
            print(f"public key registration:{tx, type(tx)}\n")

        elif data.startswith("public_keyn:"):
            print(f"DATA:{data}\n")
            info, public_key, node = data.split(":")
            info = str(info)
            public_key = str(public_key)
            node = str(node)
            tx = info, public_key

            # add wallet to tx
            add_tx_to_pool(tx)
            Wallet.add_wallet(public_key)

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

        elif data.startswith("NEWNODE:"):
            prop_bc(clientsocket=clientsocket, addr=addr, data=data)

        elif data == "bc":
            bcthread.start()

        else:
            None


def prop_bc(clientsocket, addr, data):
    try:
        info, ip, port = data.split(" ")
        node = str(ip), int(port)
        if node not in nodes:
            node != main_addr
            clients.add_clients(node)
            nodes.append(node)
            print(f"DATA:{node}")

        # intitiate bc migration to new node

        clientsocket.sendall(f"{str(blockchain.chain.__sizeof__())}")
        data = clientsocket.recv(1024).decode("utf-8")
        if data == "AKK":
            clientsocket.sendall(f"{blockchain.chain}".encode("utf-8"))
            return
    except ValueError:
        connected = False


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
    input("Wait for more clients to join")
    csock.sendall(f"Prop".encode("utf-8"))
    connected = True
    while connected:
        data = csock.recv(HEADER).decode()
        try:
            ip, port = data.split(" ")
            node = str(ip), int(port)
            if node not in nodes:
                node != main_addr
                clients.add_clients(node)
                nodes.append(node)
                print(f"NODE:{node}")
        except ValueError:
            connected = False


def broadcast_to_clients(msg):
    for client in nodes:
        if client != main_addr:
            bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bcsock.bind(("localhost", 0))
            bcsock.connect(client)
            bcsock.send(f"{msg}:{main_addr}".encode("utf-8"))
            bcsock.close()


def rdv_msg(args):
    csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    csock.connect(("localhost", 7000))
    csock.sendall(f"{mip} {mport}".encode("utf-8"))
    time.sleep(1)
    csock.sendall(f"{args}".encode("utf-8"))
    connected = True
    while connected:
        data = csock.recv(HEADER).decode()
        try:
            ip, port = data.split(" ")
            node = str(ip), int(port)
            if node not in nodes:
                node != main_addr
                clients.add_clients(node)
                nodes.append(node)
                print(f"NODE:{node}")
        except ValueError:
            connected = False
    csock.close()


def bc_sync():
    for node in nodes:
        if node != main_addr:
            bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bcsock.bind(("localhost", 0))
            bcsock.connect(node)
            bcsock.send(f"NEWNODE:{mip}:{mport}".encode("utf-8"))

            # await bc migration size
            response = bcsock.recv(HEADER).decode()
            response = int(response)
            bcsock.send(f"AKK:{main_addr}".encode("utf-8"))

            # true migration
            try:
                response = bcsock.recv(HEADER).decode()
                print(f"bc_sync rep:", response)

            except:
                bcsock.close()
                break


def mine_main():
    while True:
        blockchain.mine()
        broadcast_to_clients(block)


sthread = threading.Thread(target=server)
cthread = threading.Thread(target=client, daemon=True)
bcthread = threading.Thread(target=mine_main)


"""def server_main():
    while True:
        msg = input(">")
        if msg == "show_bc":
            for block in blockchain.chain:
                print(block)
        elif msg == "bc":
            bcthread.start()
        elif msg == "show_nodes":
            print(list(show_nodes()))

        elif msg == "create wallet":
            own_wallet = wallet()
            own_wallet.private_key
            own_wallet.public_key
            own_wallet.key_base

        elif msg.startswith("tx:"):
            # tx_tuple = test_tx()
            # tx = tx_tuple
            first_account, amount, second_account = tx
            add_tx_to_pool(tx)
            tx = str(first_account) + ":" + str(amount) + ":" + str(second_account)
            msg_tx = msg + tx
            print(f"New transaction:{msg_tx, type(tx)}\n")
            broadcast_to_clients(msg_tx)"""


if __name__ == "__main__":
    sthread.start()
    cthread.start()
    # server_main()
