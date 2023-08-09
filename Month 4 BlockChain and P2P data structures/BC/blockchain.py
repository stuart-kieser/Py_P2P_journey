from hashlib import sha256
import hashlib
from typing import Optional, Tuple
import time
import random
from tcpnode import *


gENESIS_HASH = "0" * 64


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
                    print(block.nonce)
                    print(f"increase diff: {self.difficulty}")
                    blockpool.ownblock.append(block)
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


# block pool collects each block to be mined and i used in verification of blocks


class BlockPool:
    def __init__(self, block_pool=[], ownblock=[]):
        self.block_pool = block_pool
        self.ownblock = ownblock

    def add(self, block):
        self.block_pool.append(block)
        print(f"blockpool updated:\n")
        if len(self.block_pool) == (len(nodepool.nodes) + 1):
            self.validation()
            return

    def validation(self):
        max_timestamp = max(self.block_pool, key=lambda b: float(b.timestamp))
        blockchain.add(max_timestamp)
        coinbase.reward_miner(max_timestamp)
        self.block_pool.clear()
        self.ownblock.clear()
        print("Block minted:", max_timestamp)
        return


class Clients:
    def __init__(self, clients=None):
        if clients is None:
            self.clients = []
        else:
            self.clients = clients

    def add_clients(self, client):
        self.clients.append(client)
        print("client added on blockchain side")


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
    def __init__(self, sender, amount, recipient, timestamp):
        self.sender = sender
        self.amount = amount
        self.recipient = recipient
        self.timestamp = self.get_timestamp()
        self.valid_address(sender)
        self.valid_address(recipient)
        self.valid_amount(sender)

    def get_timestamp(self):
        struct_time = time.localtime()
        timestamp = time.mktime(struct_time)
        return timestamp

    def valid_address(self, arg):
        for wallet in walletpool.walletpool:
            if arg == wallet.public_key:
                print(f"addr verified: {arg, wallet}")
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
            return False, print(f"{sender} does not have enough funds to transact")

    def execute(
        self,
    ):
        pass

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


class Nodepool:
    def __init__(self, nodes=[]):
        self.nodes = nodes


def main(arg):
    for i in range(2):
        block = Block(number=(len(blockchain.chain)), address=arg)
        blockchain.mine(block=block, arg=arg)


blockchain = Blockchain()
blockpool = BlockPool()
clients = Clients()
coinbase = Coinbase()
txpool = TransactionPool()
nodepool = Nodepool()
walletpool = WalletPool()
