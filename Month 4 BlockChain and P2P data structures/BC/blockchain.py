from hashlib import sha256
import hashlib
from typing import Optional
import time
import random
import socket
import threading
import time
import pickle
import random
import tkinter as tk
from tkinter import messagebox


GENESIS_HASH = "0" * 64

HEADER = 1024

globallock = threading.Lock()


def show_nodes():
    return clients.clients


def update_hash(*args):
    hashing_text = ""
    h = sha256()

    for arg in args:
        hashing_text += str(arg)
    h.update(hashing_text.encode("utf-8"))

    return h.hexdigest()


class Block:
    # actual block structure

    address: ["Wallet"]
    number: Optional[int]
    previous: Optional["Block"]
    data: Optional[dict]
    nonce: Optional[int]
    timestamp: float

    def __init__(
        self, address, number=0, previous=None, data=[], nonce=0, timestamp=None
    ):
        self.address = address
        self.number = number
        self.data = data or self.build_data()
        self.previous = previous or GENESIS_HASH
        self.nonce = nonce
        self.timestamp = timestamp or self.get_timestamp()

    def build_data(self):
        data = []
        tx_bin = []

        for tx in txpool.tx_pool:
            with globallock:
                data.append(tx)
                tx_bin.append(tx)

        for tx in tx_bin:
            with globallock:
                txpool.tx_pool.remove(tx)

        return data

    def get_previous_hash(self):
        if self.previous is None or IndexError:
            return GENESIS_HASH
        else:
            return blockchain.chain[-1].get_hash()

    def get_hash(self):
        return update_hash(
            self.address.public_key,
            self.number,
            self.data,
            self.previous,
            self.nonce,
            self.timestamp,
        )

    def get_timestamp(self):
        struct_time = time.localtime()
        timestamp = time.mktime(struct_time)
        return timestamp

    def __str__(self):
        return str(
            "\nMiner: %s\nBlock#: %s\nHash: %s\nPrevious: %s\nData: %s\nNonce: %s\nTimestamp: %s\n"
            % (
                self.address.public_key,
                self.number,
                self.get_hash(),
                self.previous,
                self.data,
                self.nonce,
                self.timestamp,
            ),
        )


class Blockchain:
    difficulty = 5

    def __init__(self, chain=[]):
        self.chain = chain

    def mine(self, block):
        struct_time = time.localtime()
        minestamp = time.mktime(struct_time)
        print(f"Mining start time: {minestamp}\n")
        try:
            block.previous = self.chain[-1].get_hash()
        except IndexError:
            pass

        while True:
            timestamp = time.time()

            if block.get_hash()[: self.difficulty] == "0" * self.difficulty:
                # Get the current timestamp in seconds since the epoch
                timestamp = time.time()
                time_difference_minutes = (timestamp - minestamp) / 60
                print(time_difference_minutes)
                if time_difference_minutes < float(3):
                    self.difficulty += 0  # change to 1
                    print(f"increase diff: {self.difficulty}")
                    messagefunctions.broadcast_to_clients("bcu", block)
                    blockpool.add(block)
                    break
                    # block.nonce = 0

                elif time_difference_minutes > float(5):
                    print(block.nonce)
                    self.difficulty -= 0
                    print(f"decrease diff: {self.difficulty}")
                    blockpool.add(block)
                    break

                elif time_difference_minutes > float(7):
                    print(block.nonce)
                    self.difficulty -= 3
                    print(f"decrease diff: {self.difficulty}")
                    blockpool.add(block)
                    break

                else:
                    blockpool.add(block)
                    self.difficulty -= 2
                    break

            else:
                block.nonce += 1

    def isValid(self, block):
        try:
            previousblock = self.chain[-1]
        except IndexError:
            return True

        if block.previous == previousblock.get_hash():
            return previousblock.get_hash()

        else:
            return False

    def add(self, block):
        with globallock:
            self.chain.append(block)
        return


class BlockPool:
    def __init__(self, blockpool=[], ownblock=[]):
        self.blockpool = blockpool
        self.ownblock = ownblock

    def add(self, block):
        with globallock:
            self.blockpool.append(block)
        print(f"blockpool size:{len(self.blockpool)}\n")
        print(f"clients list size:{len(clients.clients)}:\n")

        while True:
            if len(self.blockpool) == (len(clients.clients)):
                self.validation()
                return

    def validation(self):
        max_timestamp = min(self.blockpool, key=lambda b: float(b.timestamp))
        if blockchain.isValid(block=max_timestamp):
            blockchain.add(max_timestamp)
            coinbase.reward_miner(max_timestamp)
            self.blockpool.clear()
            self.ownblock.clear()
            print(f"Block minted: {max_timestamp}\n")
        else:
            print(f"FLAGGED: \n{max_timestamp}")

        return


class Clients:
    # froms the node pool. any and all active connections are kept in memory wild also kept in external db
    def __init__(self, clients=None):
        if clients is None:
            self.clients = []
        else:
            self.clients = clients

    def add(self, client):
        with globallock:
            self.clients.append(client)
        print("client added on blockchain side\n")


class Wallet:
    # this wallet object is the address endpoint for the network
    def __init__(self, public_key=None, balance=0, containers=None):
        self.public_key = public_key or self.generate_keys()
        self.balance = balance or self.get_balance(self.public_key)
        self.containers = containers or self.fetch_containers()

    def generate_keys(self) -> str:
        while True:
            key_base = random.randint(
                100000000000000000000, 50000000000000000000000000000
            )
            private_key_hash = hashlib.sha256(str(key_base).encode()).hexdigest()
            public_key_hash = hashlib.sha256(
                str(private_key_hash + str(key_base)).encode()
            ).hexdigest()
            if public_key_hash.startswith("f0"):
                break
        return str(public_key_hash)

    def get_balance(self, public_key):
        calc = 0
        self.public_key = public_key
        for block in blockchain.chain:
            if block.address.public_key == self.public_key:
                calc += 50
            for tx in block.data:
                if tx.sender == self.public_key:
                    calc -= tx.amount
                if tx.recipient == self.public_key:
                    calc += tx.amount
                self.balance = calc
        if AttributeError:
            return calc

        return self.balance

    def fetch_containers(self):
        containers = {}
        for block in blockchain.chain:
            for _object in block.data:
                if _object == Container:
                    if _object.owner == self.public_key:
                        if _object not in self.containers:
                            with globallock:
                                self.containers.update(_object)
        return containers

    def add_wallet(arg):
        walletpool.add(arg)
        return arg


class Transaction:
    # Transaction can holder a container, container is meant to represent any smart contract or file
    cd: Optional["Container"]

    def __init__(self, sender, amount, recipient, cd=None):
        self.sender = sender
        self.amount = amount
        self.recipient = recipient
        self.timestamp = self.get_timestamp()
        self.cd = cd
        check1 = self.valid_address(sender)
        check2 = self.valid_address(recipient)
        check3 = self.valid_amount(sender)
        if check1 and check2 and check3:
            self.execute(sender, amount, recipient)

    def get_timestamp(self):
        struct_time = time.localtime()
        timestamp = time.mktime(struct_time)
        return timestamp

    def valid_address(self, arg):
        for wallet in walletpool.walletpool:
            if arg.public_key == wallet.public_key:
                print(f"addr verified: {arg, wallet.public_key}\n")
                return True
        else:
            return False

    def valid_amount(self, sender):
        true_amt = sender.get_balance(public_key=sender.public_key)
        check = true_amt - self.amount
        if check > 0:
            print(true_amt, check)
            return check
        else:
            return False, print(f"{sender} does not have enough funds to transact\n")

    def execute(self, sender, amount, recpient):
        sender.balance -= amount
        recpient.balance += amount

    def __str__(self) -> str:
        return f"{self.sender.public_key} {self.amount} {self.recipient.public_key} {self.cd}"

    def __repr__(self) -> str:
        return f"{self.sender.public_key} {self.amount} {self.recipient.public_key} {self.cd}"


class Container:
    # container in container is physical block object, container id is unique and meant for querying bc
    def __init__(self, owner, containerid, container={}):
        self.owner = owner
        self.containerid = containerid or self.generate_id()
        self.container = container
        self.check_valid_owner(self.owner)

    def generate_id(self):
        id = random.randint(1, 10**18)
        self.containerid = hashlib.sha256(str(id).encode()).hexdigest()
        return self.containerid

    def add(self, args):
        self.container.update(args)

    def check_valid_owner(self, owner):
        for wallet in walletpool.walletpool:
            if wallet.public_key == owner:
                print(f"owner is valid")
                return True
            else:
                return False


class TransactionPool:
    # tx pool is held in memory for smaller tx and db for older transactions/onchain storage consisting of larger containers (docs, drawings, bigdata)
    def __init__(self, tx_pool=[]):
        self.tx_pool = tx_pool

    def add(self, tx):
        with globallock:
            self.tx_pool.append(tx)


class WalletPool:
    # hold all wallets, should be held in external db
    def __init__(self, walletpool=[]):
        self.walletpool = walletpool

    def add(self, wallet):
        with globallock:
            self.walletpool.append(wallet)


class Coinbase:
    # tokenomics for the win, look at burn algos and shifting to proof of stake or some other validation process
    reward = 50
    supply = 200
    address: ["Wallet"]

    def reward_miner(self, block):
        block.address.balance += self.reward
        self.supply = self.supply - self.reward
        return self.supply


class Server:
    # bc server in point
    def __init__(self, ip, port):
        self.mip = ip
        self.mport = port
        self.main_addr = self.mip, self.mport

    def server(self):
        print(f"Starting server: {self.main_addr}\n")
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
            data = clientsocket.recv(HEADER)
            try:
                info, data_depickled, caddr = pickle.loads(data)
                # new transaction
                if info == "tx":
                    transaction = data_depickled
                    if isinstance(transaction, Transaction):
                        print(f"New transaction:{transaction, type(transaction)}\n")
                        if transaction not in txpool.tx_pool:
                            txpool.add(transaction)

                elif info == "ct":
                    contract = data_depickled
                    if isinstance(contract, Container):
                        print(f"New container:{contract, type(contract)}\n")
                        if contract not in txpool.tx_pool:
                            txpool.add(contract)

                # new public key registration
                elif info == "pkr":
                    wallet = data_depickled
                    if isinstance(wallet, Wallet):
                        print(f"New wallet:{wallet, type(wallet)}\n")
                        if wallet not in walletpool.walletpool:
                            walletpool.add(wallet)

                # signifies block chain update
                elif info == "bcu":
                    if caddr not in clients.clients:
                        clients.clients.append(caddr)
                        print(f"Block received from new node")

                    block = data_depickled
                    if isinstance(block, Block):
                        print(f"New block:{block, type(block)}\n")
                        if block not in blockpool.blockpool:
                            blockpool.add(block)

                            # add arg to bc mine function

                elif info == "NEWNODE":
                    print(f"New node has joined the network {caddr}")

                    if isinstance(data_depickled, Blockchain):
                        print(f"{caddr} is requesting the BC")
                        threading.Thread(
                            target=propagatefunctions.prop_blockchain,
                            args=(clientsocket, caddr),
                            daemon=True,
                        ).start()

                    if isinstance(data_depickled, WalletPool):
                        print(f"{caddr} is requesting the WP")
                        threading.Thread(
                            target=propagatefunctions.prop_walletpool,
                            args=(clientsocket, caddr),
                            daemon=True,
                        ).start()

                    if isinstance(data_depickled, TransactionPool):
                        print(f"{caddr} is requesting the TXP")
                        threading.Thread(
                            target=propagatefunctions.prop_txpool,
                            args=(clientsocket, caddr),
                            daemon=True,
                        ).start()

                    if isinstance(data_depickled, Clients):
                        print(f"{caddr} is requesting the CP")
                        threading.Thread(
                            target=propagatefunctions.prop_clients,
                            args=(clientsocket, caddr),
                            daemon=True,
                        ).start()

                elif data_depickled == "bc":
                    main()

                else:
                    None

            except EOFError:
                None

            # old architecture, execute data from pickle loads
            # signifies new tx update

    def prop_bc(self, clientsocket, addr):
        try:
            info, ip, port = data.split(" ")
            node = str(ip), int(port)
            if node not in clients.clients:
                node != server.main_addr
                clients.add_clients(node)
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
    # meant for rdv start propagations
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
        time.sleep(0.1)
        # main loop to accept in propagated clients
        csock.sendall(f"Prop".encode("ascii"))
        connected = True
        while connected:
            data = csock.recv(HEADER).decode()
            try:
                ip, port = data.split(" ")
                node = str(ip), int(port)
                if node not in clients.clients:
                    node != server.main_addr
                    clients.add(node)
                    print(f"NODE:{node}\n")
            except ValueError or ConnectionRefusedError:
                connected = False
                csock.close()
                break


class MessageFunctions:
    # message functions act as ways to interact with bc
    def bc_interact(self, info, msg):
        pickled_msg = pickle.dumps((info, msg, server.main_addr))
        for client in clients.clients:
            bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bcsock.bind(("localhost", 0))
            bcsock.connect(client)
            bcsock.send(pickled_msg)
            bcsock.close()

    def broadcast_to_clients(self, info, msg):
        with globallock:
            pickled_msg = pickle.dumps((info, msg, server.main_addr))

        for client in clients.clients:
            if client != server.main_addr:
                try:
                    bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    bcsock.bind(("localhost", 0))
                    bcsock.connect(client)
                    bcsock.sendall(pickled_msg)
                    bcsock.close()
                except ConnectionRefusedError as e:
                    clients.clients.remove(client)

    def rdv_msg(self, args):
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
                if node not in clients.clients:
                    node != server.main_addr
                    clients.add_clients(node)
                    print(f"NODE:{node}")
            except ValueError:
                connected = False
        csock.close()

    def bc_sync():
        for node in clients.clients:
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


class PropagateFunctions:
    # propagate functions help in set up
    def request_prop(self, info, msg):
        pickled_msg = pickle.dumps((info, msg, server.main_addr))
        client_ = random.choice(clients.clients)
        print(f"{client_}")
        bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bcsock.bind(("localhost", 0))
        bcsock.connect(client_)
        bcsock.send(pickled_msg)
        while True:
            data = bcsock.recv(HEADER)
            object_, depickled = pickle.loads(data)
            try:
                print(object_)
                print(depickled)

                if object_ == Blockchain:
                    for block in depickled:
                        print(f"adding blocks to chain")
                        if block not in blockchain.chain:
                            blockchain.add(block)
                    break

                if object_ == WalletPool:
                    for wallet in depickled:
                        print(f"adding wallets to pool")
                        if wallet not in walletpool.walletpool:
                            walletpool.add(wallet)
                    break

                if object_ == TransactionPool:
                    for tx in depickled:
                        print(f"adding transactions to pool")
                        if tx not in txpool.tx_pool:
                            txpool.add(tx)
                    break

                if object_ == Clients:
                    for client in depickled:
                        print(f"adding clients to pool")
                        if client not in clients.clients:
                            clients.add(client)
                    break
                else:
                    print(f"this is a foreign object")

                break

            except:
                print(f"Failed...")
                None
                break

    def prop_blockchain(clientsocket, addr):
        bcpickled = pickle.dumps((Blockchain, blockchain.chain))
        print(f"propagating bc to new node")
        clientsocket.sendall(bcpickled)

    def prop_walletpool(clientsocket, addr):
        wppickled = pickle.dumps((WalletPool, walletpool))
        print(f"propagating WalletPool to new node")
        clientsocket.sendall(wppickled)

    def prop_txpool(clientsocket, addr):
        twpickled = pickle.dumps((TransactionPool, txpool))
        print(f"propagating txpool to new node")
        clientsocket.sendall(twpickled)

    def prop_clients(clientsocket, addr):
        pcpickcled = pickle.dumps((Clients, clients))
        print(f"propagating nodes to new node")
        clientsocket.sendall(pcpickcled)


class BCGUI:
    FONT = ("Arial", 18)

    def __init__(self):
        # set up screen for gui
        self.root = tk.Tk()
        self.root.geometry("1000x500")
        self.root.title("BC GUI")
        self.grid = tk.Grid()
        #### set up buttons for screen
        # create wallet button with option to link to mining
        self.wbutton = tk.Button(
            self.root, command=self.create_wallet, text="Create a wallet."
        )
        self.wbutton.pack()

        # start node button, should go through check list before mining to do propagations and such
        self.nbutton = tk.Button(self.root, command=self.set_up_node, text="Start node")
        self.nbutton.pack()

        # create transaction button with window pop up for creating tx
        # add container to tx button, container must have a file upload box

        self.root.mainloop()

    def create_wallet(self):
        self.wallet_ = Wallet()
        messagebox.showinfo(
            "Wallet details:",
            f"Never share your private key with anyone:\n{self.wallet_.public_key}",
        )
        walletpool.add(self.wallet)
        self.wbutton.config(text="Open wallet", command=self.wallet)

    def wallet(self):
        self.wallettop = tk.Toplevel()
        self.wallettop.geometry("300x500")
        self.logout = tk.Button(
            self.wallettop, command=self.logout_wallet, text="Logout"
        )
        self.logout.pack()
        self.balance = tk.Label(
            self.wallettop,
            text=f"Balance: {Wallet.get_balance(self.wallet_, self.wallet_)}",
        )
        self.balance.pack()
        self.wallettop.mainloop()

    def logout_wallet(self):
        self.wallettop.destroy()
        self.wbutton.config(command=self.create_wallet, text="Create a wallet.")

    def set_up_node(self):
        self.setupnode = tk.Toplevel(self.root)
        sthread.start()
        self.connect = tk.Button(
            self.setupnode, command=cthread.start, text="connect to network"
        )
        self.connect.pack()

        self.start = tk.Button(
            self.setupnode, command=self.startprop, text="Start propagation"
        )
        self.mine_ = tk.Button(
            self.setupnode, command=self.start_mining, text="Start mining"
        )
        self.mine_.pack()
        self.start.pack()

    def node_settings(self):
        self.nodesettings = tk.Toplevel(self.root)
        self.stop_node = tk.Button(self.nodesettings, command=self.stopnode)
        self.stop_node.pack()
        self.nodesettings.mainloop()

    def stopnode(self):
        self.nodesettings.destroy()
        self.nbutton.config(command=self.set_up_node, text="Start node")

    def startprop(self):
        propagatefunctions.request_prop("NEWNODE", blockchain)
        propagatefunctions.request_prop("NEWNODE", walletpool)
        propagatefunctions.request_prop("NEWNODE", clients)
        propagatefunctions.request_prop("NEWNODE", txpool)

    def start_mining(self):
        self.nbutton.config(command=self.node_settings, text="Node settings")
        while True:
            block = Block(number=(len(blockchain.chain)), address=self.wallet_)
            blockchain.mine(block=block)


def main(wallet):
    while True:
        block = Block(number=(len(blockchain.chain)), address=wallet.public_key)
        blockchain.mine(block=block)


blockchain = Blockchain()
blockpool = BlockPool()
clients = Clients()
coinbase = Coinbase()
txpool = TransactionPool()
walletpool = WalletPool()
messagefunctions = MessageFunctions()
propagatefunctions = PropagateFunctions()

server = Server("localhost", int(input("pick server port: ")))
client = Client("localhost", 0)

sthread = threading.Thread(target=server.server)
cthread = threading.Thread(target=client.client, daemon=True)

BCGUI()
