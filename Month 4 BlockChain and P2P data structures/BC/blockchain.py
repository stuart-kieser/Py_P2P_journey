from hashlib import sha256
import hashlib
from typing import Optional, Tuple
import time
import random


gENESIS_HASH = "0" * 64

walletaddr = []
nodes = []
tx_pool = []


def update_hash(*args):
    hashing_text = ""
    h = sha256()

    for arg in args:
        hashing_text += str(arg)
    h.update(hashing_text.encode("utf-8"))

    return h.hexdigest()


def add_tx_to_pool(args):
    tx_pool.append(args)


def wallet_addrs(arg):
    if arg in walletaddr:
        return True
    else:
        return False


class Block:
    # actual block structure

    number: Optional[int]
    previous: Optional["Block"]
    data: Optional[dict]
    nonce: Optional[int]
    timestamp: float

    def __init__(self, number=0, previous=None, data=[], nonce=0, timestamp=None):
        self.number = number
        self.data = self.build_data()
        self.previous = previous
        self.nonce = nonce
        self.timestamp = timestamp or self.get_timestamp()

    def build_data(self):
        data = []
        try:
            for tx in tx_pool:
                for i in range(10):
                    if tx not in data:
                        data.append(tx)
                        tx_pool.remove(tx)
                    else:
                        None
            return data

        except:
            if tx_pool is None:
                data = "NO TRANSACTIONS"
            return data

    def get_previous_hash(self):
        if self.previous is None or IndexError:
            return gENESIS_HASH
        else:
            return self.previous.get_hash()

    def get_hash(self):
        return update_hash(
            self.number, self.data, self.previous, self.nonce, self.timestamp
        )

    def get_timestamp(self):
        struct_time = time.localtime()
        timestamp = time.mktime(struct_time)
        return timestamp

    def __str__(self):
        return str(
            "Block#: %s\nHash: %s\nPrevious: %s\nData: %s\nNonce: %s\nTimestamp: %s\n"
            % (
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

    def mine(self):
        block = Block(number=(len(self.chain)))
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
    def __init__(self, block_pool=[]):
        self.block_pool = block_pool

    def add(self, block):
        self.block_pool.append(block)
        print(f"blockpool updated:\n")
        print("Block Pool size:", len(self.block_pool), self.block_pool)
        print("Client list size:", (len(clients.clients) + 1), "\n")

        if len(self.block_pool) == (len(clients.clients) + 1):
            self.validation()
            return

    def validation(self):
        for block in self.block_pool:
            for other_block in self.block_pool:
                block != other_block
                if block.data != other_block.data:
                    self.block_pool.pop(other_block)

        max_timestamp = max(self.block_pool, key=lambda b: float(b.timestamp))
        blockchain.add(max_timestamp)
        self.block_pool.clear()
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
        for block in blockchain.chain:
            for data in block:
                for tx in data:
                    if len(tx) == 2:
                        if tx[0] == public_key:
                            self.balance += tx[1]
                        if tx[2] == public_key:
                            self.balance -= tx[1]
            return self.balance

    def add_wallet(public_key):
        walletaddr.append(public_key)
        return public_key


class Transaction:
    def __init__(self, sender, amount, recipient):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def valid_address(self, arg):
        if arg in walletaddr:
            return True
        else:
            return False

    def valid_amount(self, arg, amount):
        amount = 0
        for block in blockchain.chain:
            for block.data in block:
                for tx in block.data:
                    if len(tx) == 2:
                        if tx[0] == arg:
                            amount += tx[1]
                        if tx[2] == arg:
                            amount -= tx[1]

    def __repr__(self) -> str:
        f"{self.sender}:{self.amount}:{self.recipient}"


blockchain = Blockchain()
block = Block()
blockpool = BlockPool()
clients = Clients()
wallet = Wallet()


def main():
    global blockchain
    while True:
        blockchain.mine()


if __name__ == "__main__":
    main()
