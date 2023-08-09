import socket
import threading
import time
import pickle
from blockchain import (
    Block,
    Wallet,
    blockchain,
    blockpool,
    clients,
    txpool,
    nodepool,
    walletpool,
    main,
)


HEADER = 128


def show_nodes():
    return nodepool.nodes


class Server:
    def __init__(self, ip, port):
        self.mip = ip
        self.mport = port
        self.main_addr = self.mip, self.mport

    def server(self):
        print(f"Starting server: {self.main_addr}")
        # create the server socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket and listen for incoming requests
        sock.bind(self.main_addr)
        sock.listen()
        # accept incoming connections
        while True:
            clientsock, addr = sock.accept()
            thread_hc = threading.Thread(
                target=self.handle_client, args=(clientsock, addr), daemon=True
            )
            thread_hc.start()

    def handle_client(self, clientsocket, addr):
        while True:
            data = clientsocket.recv(1024)
            try:
                info, data_depickled, addr = pickle.loads(data)
                if info == "tx:":
                    transaction = data_depickled
                    print(f"DATA:{transaction}\n")
                    print(
                        f"New transaction:{transaction.public_key, type(transaction)}\n"
                    )
                    txpool.tx_pool.append(transaction)
                    if data_depickled not in txpool.tx_pool:
                        txpool.tx_pool.append(transaction)

                # new public key registration
                elif data_depickled.startswith("public_keyr:"):
                    print(f"DATA:{data}\n")
                    info, public_key, node = data_depickled.split(":")
                    info = str(info)
                    public_key = str(public_key)
                    node = str(node)
                    tx = info, public_key

                    # check if key exists in bc history
                    walletpool.walletpool(public_key)
                    print(f"public key registration:{tx, type(tx)}\n")

                elif data_depickled.startswith("public_keyn:"):
                    print(f"DATA:{data}\n")
                    info, public_key, node = data_depickled.split(":")
                    info = str(info)
                    public_key = str(public_key)
                    node = str(node)
                    tx = info, public_key

                    # add wallet to tx
                    walletpool.walletpool.appent(tx)
                    Wallet.add_wallet(public_key)

                # signifies block chain update
                elif data_depickled.startswith("bcu:"):
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
                    bcu_block = Block(
                        number, previous_hash, received_data, 0, timestamp
                    )
                    blockchain.mine(bcu_block)

                elif data_depickled.startswith("NEWNODE:"):
                    prop_bc(clientsocket=clientsocket, addr=addr, data=data)

                elif data_depickled == "bc":
                    main()

                else:
                    None
            except EOFError:
                None

            # old architecture, execute data from pickle loads
            # signifies new tx update


def prop_bc(clientsocket, addr, data):
    try:
        info, ip, port = data.split(" ")
        node = str(ip), int(port)
        if node not in nodepool.nodepool:
            node != server.main_addr
            clients.add_clients(node)
            nodepool.nodes.append(node)
            print(f"DATA:{node}")

        # intitiate bc migration to new node

        clientsocket.sendall(f"{str(blockchain.chain.__sizeof__())}")
        data = clientsocket.recv(1024).decode("ascii")
        if data == "AKK":
            clientsocket.sendall(f"{blockchain.chain}".encode("ascii"))
            return
    except ValueError:
        connected = False


class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client_addr = ip, port

    def client(self):
        # create client socket to communicate with server
        csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Starting client on:{self.client_addr}\n")

        # bind socket to local addr
        csock.bind(self.client_addr)

        # connect to server
        node_addr = ("localhost", 7000)
        csock.connect(node_addr)
        ip, port = server.main_addr
        msg = f"{ip} {port}"
        csock.sendall(f"{msg}".encode("ascii"))
        # main loop to accept in propagated clients
        input("Wait for more clients to join")
        csock.sendall(f"Prop".encode("ascii"))
        connected = True
        while connected:
            data = csock.recv(HEADER).decode()
            try:
                ip, port = data.split(" ")
                node = str(ip), int(port)
                if node not in nodepool.nodes:
                    node != server.main_addr
                    clients.add_clients(node)
                    nodepool.nodes.append(node)
                    print(f"NODE:{node}")
            except ValueError:
                connected = False


def broadcast_to_clients(info, msg):
    pickled_msg = pickle.dumps((info, msg, server.main_addr))
    print(f"pickle: {pickled_msg}")
    for client in nodepool.nodes:
        if client != server.main_addr:
            bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bcsock.bind(("localhost", 0))
            bcsock.connect(client)
            bcsock.send(pickled_msg)
            bcsock.close()


def rdv_msg(args):
    csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    csock.connect(("localhost", 7000))
    csock.sendall(f"{server.mip} {server.mport}".encode("ascii"))
    time.sleep(1)
    csock.sendall(f"{args}".encode("ascii"))
    connected = True
    while connected:
        data = csock.recv(HEADER).decode()
        try:
            ip, port = data.split(" ")
            node = str(ip), int(port)
            if node not in nodepool.nodes:
                node != server.main_addr
                clients.add_clients(node)
                nodepool.nodes.append(node)
                print(f"NODE:{node}")
        except ValueError:
            connected = False
    csock.close()


def bc_sync():
    for node in nodepool.nodes:
        if node != server.main_addr:
            bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bcsock.bind(("localhost", 0))
            bcsock.connect(node)
            bcsock.send(f"NEWNODE:{server.mip}:{server.mport}".encode("ascii"))

            # await bc migration size
            response = bcsock.recv(HEADER).decode()
            response = int(response)
            bcsock.send(f"AKK:{server.main_addr}".encode("ascii"))

            # true migration
            try:
                response = bcsock.recv(HEADER).decode()
                print(f"bc_sync rep:", response)

            except:
                bcsock.close()
                break


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


server = Server("localhost", int(input("Select a server port: ")))
client = Client("localhost", int(input("Select a client port: ")))

sthread = threading.Thread(target=server.server)
cthread = threading.Thread(target=client.client, daemon=True)
