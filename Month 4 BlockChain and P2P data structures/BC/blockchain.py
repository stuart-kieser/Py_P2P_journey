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
import copy


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

    def __repr__(self):
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
    difficulty = 6
    isvalid = True

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
                print(f"{time_difference_minutes}\n")
                if time_difference_minutes < float(3):
                    self.difficulty += 0  # change to 1
                    print(f"mined: {block}\n")
                    return block

                elif time_difference_minutes > float(5):
                    self.difficulty -= 0
                    print(f"mined: {block}\n")
                    return block

                elif time_difference_minutes > float(7):
                    self.difficulty -= 0
                    print(f"mined: {block}\n")
                    return block

                else:
                    self.difficulty -= 0
                    print(f"mined: {block}\n")
                    return block

            else:
                block.nonce += 1

    def is_valid(self, block):
        if IndexError:
            return True
        else:
            previous_block = self.chain[-1]
            # Check if the block's timestamp is reasonable (within a certain range of current time)
            current_time = time.time()
            time_difference = abs(current_time - block.timestamp)
            max_time_difference = (
                600  # Maximum allowed time difference in seconds (adjust as needed)
            )
            # Check if the previous hash matches the hash of the previous block
            if block.previous != previous_block.get_hash():
                return False

            # Check to see if block number matches
            if block.number != blockchain.chain[-1].number + 1:
                return False

            if time_difference > max_time_difference:
                return False

            else:
                return True

    def add(self, block):
        with globallock:
            self.chain.append(block)
            print(f"Block minted: {block}\n")


class BlockPool:
    def __init__(self, blockpool=[]):
        self.blockpool = blockpool

    def add(self, block):
        with globallock:
            self.blockpool.append(block)
            print(f"blockpool size:{len(self.blockpool)}\n")
            print(f"clients list size:{len(clients.clients)}:\n")

    def validation(self):
        if len(blockpool.blockpool) == (len(clients.clients)):
            max_timestamp = max(self.blockpool, key=lambda b: float(b.nonce))
            if blockchain.is_valid(max_timestamp):
                blockchain.add(max_timestamp)
                coinbase.reward_miner(max_timestamp)
                self.blockpool.clear()
                return
            else:
                print(f"Block has been flagged {max_timestamp}\n")


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
    public_key: str

    # this wallet object is the address endpoint for the network
    def __init__(self, public_key=None, balance=0):
        self.public_key = public_key or self.generate_keys()
        self.balance = balance or self.get_balance(self.public_key)
        self.containers = {}

    def generate_keys(self) -> str:
        while True:
            key_base = random.randint(1, 50000000000000000000000000000)
            private_key_hash = hashlib.sha256(str(key_base).encode()).hexdigest()
            public_key_hash = hashlib.sha256(
                str(private_key_hash + str(key_base)).encode()
            ).hexdigest()
            if public_key_hash.startswith("f0"):
                break
        return public_key_hash

    def get_balance(self, public_key):
        calc = 0
        self.public_key = public_key
        for block in blockchain.chain:
            if block.address.public_key == self.public_key:
                calc += 50
            for tx in block.data:
                if isinstance(tx, Transaction):
                    if tx.sender == self.public_key:
                        calc -= int(tx.amount)
                    if tx.recipient == self.public_key:
                        calc += int(tx.amount)
                    self.balance = calc
        if AttributeError:
            return calc

        return self.balance

    def fetch_containers(self):
        pass

    def add_wallet(arg):
        walletpool.add(arg)
        return arg

    def wallet_get_addr(self):
        return self.public_key

    def __str__(self) -> str:
        return f"pkr {self.public_key}"

    def __repr__(self) -> str:
        return f"pkr {self.public_key}"


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
        check2 = self.valid_recipient(recipient)
        check3 = self.valid_amount(sender)
        if check1 and check2:
            if check3 > self.amount:
                self.execute(sender, amount, recipient)
        else:
            print(f"CHECKS FAILED: CHECK3{check3} CHECK2 {check2}\n")

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
                print(f"addr does not exist: {arg}\n")
                return False

    def valid_recipient(self, arg):
        for wallet in walletpool.walletpool:
            if arg == wallet.public_key:
                print(f"addr verified: {arg, wallet.public_key}\n")
                return True
            else:
                print(f"addr does not exist: {arg}\n")
                return False

    def valid_amount(self, sender):
        true_amt = sender.get_balance(public_key=sender.public_key)
        print(f"{true_amt, self.amount}\n")
        check = int(true_amt) - int(self.amount)
        if check > 0:
            print(f"{true_amt, check}\n")
            return check
        else:
            return False, print(f"{sender} does not have enough funds to transact\n")

    def execute(self, sender, amount, recipient):
        sender.balance -= int(amount)
        for wallet in walletpool.walletpool:
            if recipient == wallet.public_key:
                wallet.balance += int(amount)

    def __str__(self) -> str:
        return f"{self.sender.public_key} {self.amount} {self.recipient} {self.cd}\n"

    def __repr__(self) -> str:
        return f"{self.sender.public_key} {self.amount} {self.recipient} {self.cd}\n"


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
                print(f"owner is valid\n")
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
                            break

                elif info == "ct":
                    contract = data_depickled
                    if isinstance(contract, Container):
                        print(f"New container:{contract, type(contract)}\n")
                        if contract not in txpool.tx_pool:
                            txpool.add(contract)
                            break

                # new public key registration
                elif info == "pkr":
                    wallet = data_depickled
                    if isinstance(wallet, Wallet):
                        print(f"New wallet:{wallet, type(wallet)}\n")
                        if wallet not in walletpool.walletpool:
                            walletpool.add(wallet)
                            txpool.add(wallet)
                            break

                # signifies block chain update
                elif info == "bcu":
                    if caddr not in clients.clients:
                        clients.clients.append(caddr)

                    if isinstance(data_depickled, Block):
                        print(f"block from miner:{data_depickled.address}\n")
                        if data_depickled not in blockpool.blockpool:
                            print(f"Adding clients block to pool: {data_depickled}\n")
                            blockpool.add(data_depickled)
                            blockpool.validation()
                            # add arg to bc mine function
                            break

                elif info == "NEWNODE":
                    print(f"New node has joined the network {caddr}\n")
                    if caddr not in clients.clients:
                        clients.add(caddr)
                        continue
                    if isinstance(data_depickled, Blockchain):
                        print(f"{caddr} is requesting the BC\n")
                        propthread1 = threading.Thread(
                            target=propagatefunctions.prop_blockchain,
                            args=(clientsocket, caddr),
                            daemon=True,
                        )
                        propthread1.start()

                    if isinstance(data_depickled, WalletPool):
                        print(f"{caddr} is requesting the WP\n")
                        propthread2 = threading.Thread(
                            target=propagatefunctions.prop_walletpool,
                            args=(clientsocket, caddr),
                            daemon=True,
                        )
                        propthread2.start()

                    if isinstance(data_depickled, TransactionPool):
                        print(f"{caddr} is requesting the TXP\n")
                        propthread3 = threading.Thread(
                            target=propagatefunctions.prop_txpool,
                            args=(clientsocket, caddr),
                            daemon=True,
                        )
                        propthread3.start()

                    if isinstance(data_depickled, Clients):
                        print(f"{caddr} is requesting the CP\n")
                        propthread4 = threading.Thread(
                            target=propagatefunctions.prop_clients,
                            args=(clientsocket, caddr),
                            daemon=True,
                        )
                        propthread4.start()
                        if caddr not in clients.clients:
                            clients.add(caddr)
                    break

                else:
                    None

            except EOFError:
                None


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
        msg = f"{ip} {port}".encode("ascii")
        csock.sendall(msg)
        time.sleep(0.1)
        # main loop to accept in propagated clients
        csock.sendall(f"Prop".encode("ascii"))
        connected = True
        while connected:
            data = csock.recv(HEADER).decode()
            try:
                (
                    ip,
                    port,
                ) = data.split(" ")
                node = str(ip), int(port)
                if node not in clients.clients:
                    node != server.main_addr
                    clients.add(node)
                    print(f"NODE:{node}\n")
            except ValueError or ConnectionRefusedError:
                connected = False
                csock.close()
                break
            connected = False
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
        return

    def broadcast_to_clients(self, info, msg):
        pickled_msg = pickle.dumps((info, msg, server.main_addr))
        for client in clients.clients:
            if client != server.main_addr:
                bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                bcsock.bind(("localhost", 0))
                bcsock.connect(client)
                bcsock.send(pickled_msg)
                bcsock.close()
        return

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
                    print(f"NODE:{node}\n")
                    print("-" * 20)
            except ValueError:
                connected = False
        csock.close()
        return

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
                    print(f"bc_sync rep: {response}\n")

                except:
                    bcsock.close()
                    break


class PropagateFunctions:
    # propagate functions help in set up
    def request_prop(self, info, msg):
        client_ = random.choice(clients.clients)
        if client_ != server.main_addr:
            pickled_msg = pickle.dumps((info, msg, server.main_addr))
            print(f"{client_}\n")
            bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bcsock.bind(("localhost", 0))
            bcsock.connect(client_)
            bcsock.send(pickled_msg)
            while True:
                data = bcsock.recv(HEADER)
                object_, depickled = pickle.loads(data)
                try:
                    print(f"OBJECT: {object_}\n")
                    print(f"{depickled}\n")

                    if object_ == Blockchain:
                        for block in depickled:
                            print(f"adding blocks to chain\n")
                            if block not in blockchain.chain:
                                blockchain.add(block)
                        break

                    if object_ == WalletPool:
                        if depickled is None:
                            print(f"No wallets to propagate\n")
                        for wallet in depickled:
                            print(f"adding wallets to pool\n")
                            if wallet not in walletpool.walletpool:
                                walletpool.add(wallet)
                        break

                    if object_ == TransactionPool:
                        if depickled is None:
                            print(f"No trasnactions to propagate\n")
                        for tx in depickled:
                            print(f"adding transactions to pool\n")
                            if tx not in txpool.tx_pool:
                                txpool.add(tx)
                        break

                    if object_ == Clients:
                        if depickled is None:
                            print(f"No clients to propagate\n")
                        for client in depickled:
                            print(f"adding clients to pool\n")
                            if client not in clients.clients:
                                clients.add(client)
                        break
                    else:
                        print(f"this is a foreign object\n")

                    break

                except:
                    print(f"Failed...\n")
                    None
                    break

    def prop_blockchain(self, clientsocket, addr):
        bcpickled = pickle.dumps((Blockchain, blockchain.chain))
        print(f"propagating bc to new node\n")
        clientsocket.sendall(bcpickled)
        return

    def prop_walletpool(self, clientsocket, addr):
        wppickled = pickle.dumps((WalletPool, walletpool.walletpool))
        print(f"propagating WalletPool to new node\n")
        clientsocket.sendall(wppickled)
        return

    def prop_txpool(self, clientsocket, addr):
        twpickled = pickle.dumps((TransactionPool, txpool.tx_pool))
        print(f"propagating txpool to new node\n")
        clientsocket.sendall(twpickled)
        return

    def prop_clients(self, clientsocket, addr):
        pcpickcled = pickle.dumps((Clients, clients.clients))
        print(f"propagating nodes to new node\n")
        clientsocket.sendall(pcpickcled)
        return


class BCGUI:
    FONT = ("Arial", 18)

    def __init__(self):
        # set up screen for gui
        self.root = tk.Tk()
        self.msgbox = "Error"
        self.mining = True
        self.inputvar = tk.StringVar()
        self.root.geometry("800x500")
        self.root.title("BC GUI")
        self.stats = tk.Frame(self.root)
        self.bclabel1 = tk.Label(
            self.stats, text=f"Active nodes: {len(clients.clients)}"
        ).grid(row=0, column=0)
        self.bclabel2 = tk.Label(
            self.stats, text=f"Active block number: {len(blockchain.chain)}"
        ).grid(row=0, column=1)
        self.stats.pack()

        #### set up buttons for screen
        # create wallet button with option to link to mining
        self.wbutton = tk.Button(
            self.root, command=self.create_wallet, text="Create a wallet."
        )
        self.wbutton.pack()

        # start node button, should go through check list before mining to do propagations and such
        self.nbutton = tk.Button(self.root, command=self.set_up_node, text="Start node")
        self.nbutton.pack()
        self.root.mainloop()
        # add container to tx button, container must have a file upload box

    def create_wallet(self):
        global wallet_
        wallet_ = Wallet()
        walletpool.add(wallet_)
        self.createdwallet = True
        messagebox.showinfo(
            "Wallet details:",
            f"Never share your private key with anyone:\n{wallet_.public_key}",
        )
        walletpool.add(wallet_)
        self.wbutton.config(text="Open wallet", command=self.wallet)
        self.root.mainloop()

    def wallet(self):
        self.wallettop = tk.Toplevel()
        print(f"wallet addr {wallet_.public_key}\n")
        self.wallettop.geometry("350x500")
        self.logout = tk.Button(
            self.wallettop, command=self.logout_wallet, text="Logout"
        )
        self.logout.pack()
        self.balance = tk.Label(
            self.wallettop,
            text=f"Balance: {wallet_.get_balance(wallet_.public_key)}",
        )
        self.balance.pack()

        self.publickey = tk.Label(
            self.wallettop,
            text=f"Wallet Address:\n {wallet_.public_key}",
        )
        self.publickey.pack()

        # create transaction in frame
        self.txbox = tk.Frame(self.wallettop, bd=5)
        self.recipientbx = tk.Frame(self.txbox)
        self.recipiententry = tk.Entry(self.recipientbx, textvariable=str)
        self.recipiententry.pack(side="right")
        self.recipientlb = tk.Label(self.recipientbx, text="Enter recipient address")
        self.recipientlb.pack(side="left")
        self.recipientbx.pack()

        self.amtbx = tk.Frame(self.txbox)
        self.amountentry = tk.Entry(self.amtbx, textvariable=int)
        self.amountentry.pack(side="right")
        self.amountlb = tk.Label(self.amtbx, text="Enter amount to send")
        self.amountlb.pack(side="left")
        self.amtbx.pack()

        self.txsend = tk.Button(
            self.txbox,
            command=self.buildtx,
            text="Send transaction",
        )
        self.txsend.pack(side="bottom")
        self.txbox.pack()
        self.root.mainloop()

    def logout_wallet(self):
        self.wallettop.destroy()
        self.wbutton.config(command=self.create_wallet, text="Create a wallet.")

    def buildtx(self):
        sender = wallet_
        amount = self.amountentry.get()
        recipient = self.recipiententry.get()
        tx = Transaction(sender, amount, recipient)
        print(f"{tx}\n")
        self.bcmsg("tx", tx)

    def set_up_node(self):
        self.setupnode = tk.Toplevel(self.root)
        if not wallet_:
            messagebox.showinfo(f"{self.msgbox}", f"You need to create a wallet")
            self.setupnode.destroy()
        elif wallet_:
            sthread.start()
            clients.add(server.main_addr)
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
        self.stop_node = tk.Button(
            self.nodesettings, command=self.stopnode, text="Stop node"
        )
        self.start = tk.Button(
            self.setupnode, command=self.startprop, text="Start propagation"
        )
        self.start.pack()
        self.stop_node.pack()

    def stopnode(self):
        self.nodesettings.destroy()
        self.mining = False
        self.nbutton.config(command=self.set_up_node, text="Start node")

    def startprop(self):
        self.bcgthread = threading.Thread(target=self.bcprop, daemon=True)
        self.bcgthread.start()

    def bcprop(self):
        propagatefunctions.request_prop("NEWNODE", clients)
        propagatefunctions.request_prop("NEWNODE", blockchain)
        propagatefunctions.request_prop("NEWNODE", walletpool)
        propagatefunctions.request_prop("NEWNODE", txpool)
        return

    def start_mining(self):
        messagefunctions.bc_interact("pkr", wallet_)
        mainthread.start()
        self.setupnode.destroy()
        self.nbutton.config(command=self.node_settings, text="Node settings")

    def bcmsg(self, info, msg):
        messagefunctions.bc_interact(info=info, msg=msg)


def scriptmain():
    while True:
        block = Block(number=(len(blockchain.chain)), address=wallet_)
        minedblock = blockchain.mine(block=block)
        blockpool.add(minedblock)
        messagefunctions.broadcast_to_clients("bcu", minedblock)
        blockpool.validation()


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
mainthread = threading.Thread(target=scriptmain)

if __name__ == "__main__":
    bcgui = BCGUI()
