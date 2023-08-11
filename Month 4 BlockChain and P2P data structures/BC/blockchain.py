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


gENESIS_HASH = "0" * 64

HEADER = 1024


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
        self.previous = previous
        self.nonce = nonce
        self.timestamp = timestamp or self.get_timestamp()

    def build_data(self):
        data = []
        tx_bin = []

        for tx in txpool.tx_pool:
            data.append(tx)
            tx_bin.append(tx)

        for tx in tx_bin:
            txpool.tx_pool.remove(tx)

        return data

    def get_previous_hash(self):
        if self.previous is None or IndexError:
            return gENESIS_HASH
        else:
            return self.previous.get_hash()

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

    def mine(self, block, arg):
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

    def isValid(self):
        for i in range(1, len(self.chain)):
            _previous = self.chain[i].previous
            _current = self.chain[i - 1].get_hash()
            if (
                _previous != _current
                or _current[: self.difficulty] != "0" * self.difficulty
            ):
                return False
            return True

    def add(self, block):
        self.chain.append(block)
        return


class BlockPool:
    def __init__(self, blockpool=[], ownblock=[]):
        self.blockpool = blockpool
        self.ownblock = ownblock

    def add(self, block):
        self.blockpool.append(block)
        print(f"blockpool size:{len(self.blockpool)}\n")
        print(f"clients list size:{len(clients.clients)}:\n")

        while True:
            if len(self.blockpool) == (len(clients.clients)):
                self.validation()
                return

    def validation(self):
        max_timestamp = min(self.blockpool, key=lambda b: float(b.timestamp))
        blockchain.add(max_timestamp)
        coinbase.reward_miner(max_timestamp)
        self.blockpool.clear()
        self.ownblock.clear()
        print(f"Block minted: {max_timestamp}\n")
        return


class Clients:
    def __init__(self, clients=None):
        if clients is None:
            self.clients = []
        else:
            self.clients = clients

    def add_clients(self, client):
        self.clients.append(client)
        print("client added on blockchain side\n")


class Wallet:
    balance: int

    def __init__(self, public_key=None, balance=0):
        self.public_key = public_key or self.generate_keys()
        self.balance = balance or self.get_balance(self.public_key)

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
        for block in blockchain.chain:
            if block.address.public_key == public_key:
                calc += 50
            for tx in block.data:
                if tx.sender == public_key:
                    calc -= tx.amount
                if tx.recipient == public_key:
                    calc += tx.amount
                self.balance = calc
        if AttributeError:
            return calc

        return self.balance

    def add_wallet(arg):
        walletpool.walletpool.append(arg)
        return arg


class Transaction:
    def __init__(self, sender, amount, recipient):
        self.sender = sender
        self.amount = amount
        self.recipient = recipient
        self.timestamp = self.get_timestamp()
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
        true_amt = Wallet.get_balance(self, public_key=sender)
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
        return f"{self.sender}:{self.amount}:{self.recipient}"

    def __repr__(self) -> str:
        return f"{self.sender}:{self.amount}:{self.recipient}"


class TransactionPool:
    def __init__(self, tx_pool=[]):
        self.tx_pool = tx_pool

    def checkpool(self):
        for tx in self.tx_pool:
            pass


class WalletPool:
    def __init__(self, walletpool=[]):
        self.walletpool = walletpool


class Coinbase:
    reward = 50
    supply = 200
    address: ["Wallet"]

    def reward_miner(self, block):
        block.address.balance += self.reward
        self.supply = self.supply - self.reward
        return self.supply


class Server:
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
                info, data_depickled, addr = pickle.loads(data)
                if info == "tx":
                    transaction = data_depickled
                    if isinstance(transaction, Transaction):
                        print(f"New transaction:{transaction, type(transaction)}\n")
                        if transaction not in txpool.tx_pool:
                            txpool.tx_pool.append(transaction)

                # new public key registration
                elif info == "pkr":
                    wallet = data_depickled
                    if isinstance(wallet, Wallet):
                        print(f"New wallet:{wallet, type(wallet)}\n")
                        if wallet not in walletpool.walletpool:
                            walletpool.walletpool.append(wallet)

                # signifies block chain update
                elif info == "bcu":
                    block = data_depickled
                    if isinstance(block, Block):
                        print(f"New block:{block, type(block)}\n")
                        if block not in blockpool.blockpool:
                            blockpool.blockpool.append(block)

                            # add arg to bc mine function

                elif info == "NEWNODE":
                    blockchain = data_depickled
                    if isinstance(blockchain, Blockchain):
                        PropgateFunctions.prop_blockchain(clientsocket, addr)

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
        input("Press enter to start propagation.\n")
        csock.sendall(f"Prop".encode("ascii"))
        connected = True
        while connected:
            data = csock.recv(HEADER).decode()
            try:
                ip, port = data.split(" ")
                node = str(ip), int(port)
                if node not in clients.clients:
                    node != server.main_addr
                    clients.add_clients(node)
                    print(f"NODE:{node}\n")
            except ValueError:
                connected = False
                csock.close()
                break


class MessageFunctions:
    def bc_interact(self, info, msg):
        pickled_msg = pickle.dumps((info, msg, server.main_addr))
        for client in clients.clients:
            bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bcsock.bind(("localhost", 0))
            bcsock.connect(client)
            bcsock.send(pickled_msg)
            bcsock.close()

    def broadcast_to_clients(self, info, msg):
        pickled_msg = pickle.dumps((info, msg, server.main_addr))
        for client in clients.clients:
            if client != server.main_addr:
                bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                bcsock.bind(("localhost", 0))
                bcsock.connect(client)
                bcsock.sendall(pickled_msg)
                bcsock.close()

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


class PropgateFunctions:
    def request_prop(self, info, msg):
        pickled_msg = pickle.dumps((info, msg))
        client = random.choice(clients.clients)
        bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bcsock.bind(("localhost", 0))
        bcsock.connect(client)
        bcsock.send(pickled_msg)
        while True:
            data = bcsock.recv(HEADER)
            try:
                depickled = pickle.loads(data)
                if isinstance(depickled, Blockchain):
                    for block in depickled:
                        blockchain.add(block)
                if depickled == "DONE":
                    break

            except:
                None

    def prop_blockchain(self, clientsocket, addr):
        bcpickled = pickle.dumps(blockchain)
        clientsocket.sendall(bcpickled)
        donepickled = "DONE"
        clientsocket.sendall(donepickled)

    def prop_blockpool():
        pass

    def prop_walletpool():
        pass

    def prop_txpool():
        pass

    def prop_coinbase():
        pass


def main(arg):
    for i in range(1):
        block = Block(number=(len(blockchain.chain)), address=arg)
        blockchain.mine(block=block, arg=arg)


blockchain = Blockchain()
blockpool = BlockPool()
clients = Clients()
coinbase = Coinbase()
txpool = TransactionPool()
walletpool = WalletPool()
messagefunctions = MessageFunctions()

server = Server("localhost", int(input("Select a server port: ")))
client = Client("localhost", int(input("Select a client port: ")))


sthread = threading.Thread(target=server.server)
cthread = threading.Thread(target=client.client, daemon=True)
