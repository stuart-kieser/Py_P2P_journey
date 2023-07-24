from hashlib import sha256
import hashlib
from typing import Optional, Tuple
import time
import queue
import random

gENESIS_HASH = "0" * 64

tx_pool = queue.Queue(maxsize=0)
tx_list = []
walletaddr = []


def update_hash(*args):
    hashing_text = ""
    h = sha256()

    for arg in args:
        hashing_text += str(arg)
    h.update(hashing_text.encode("utf-8"))

    return h.hexdigest()


def add_tx_to_pool(args):
    tx_pool.put(args)


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

    def __init__(self, number=0, previous=None, data=any, nonce=0, timestamp=None):
        self.number = number
        self.data = data
        self.previous = previous
        self.nonce = nonce
        self.timestamp = timestamp or self.get_timestamp()

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

    def add(self, block):
        self.chain.append(block)

    def mine(self, block):
        struct_time = time.localtime()
        minestamp = time.mktime(struct_time)
        print(f"Mining start time: {minestamp}\n")
        try:
            block.previous = self.chain[-1].get_hash()
        except IndexError:
            pass

        while True:
            if block.get_hash()[: self.difficulty] == "0" * self.difficulty:
                timestamp = (
                    time.time()
                )  # Get the current timestamp in seconds since the epoch
                time_difference_minutes = (timestamp - block.timestamp) / 60
                print(time_difference_minutes)
                if time_difference_minutes < 4:
                    print(block.nonce)
                    self.difficulty += 1
                    block.nonce = 0
                    print(f"new diff: {self.difficulty}")
                elif time_difference_minutes > 5:
                    print(block.nonce)
                    self.difficulty -= 1
                    block.nonce = 0
                    print(f"new diff: {self.difficulty}")
                else:
                    blockpool.add(block)
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


# block pool collects each block to be mined and i used in verification of blocks


class BlockPool:
    def __init__(self, block_pool=[]):
        self.block_pool = block_pool

    def add(self, block):
        self.block = block
        self.block_pool.append(block)
        print(f"blockpool updated:\n")

        if len(self.block_pool) == (len(bc_client.clients) + 1):
            print("Block Pool size:", len(self.block_pool))
            print("Client list size:", (len(bc_client.clients) + 1), "\n")
            self.validation()
            return

    def validation(self):
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
    def __init__(self, private_key=None, public_key=None, balance=0) -> None:
        self.private_key = private_key or self.generate_keys()
        self.public_key = public_key
        self.balance = self.get_balance(public_key)

    def generate_keys(self) -> Optional[tuple[str, str]]:
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
        return public_key_hash, private_key_hash, key_base

    def get_balance(self, public_key):
        balance = 0
        for block in blockchain.chain:
            for data in block:
                for tx in data:
                    if public_key is tx[2]:
                        balance = +tx[1]
                    if public_key is tx[0]:
                        balance = -tx[1]
        return balance

    def __str__(self) -> str:
        print(f"\nPublic_key: {self.public_key}")
        print(f"\nBalance   : {self.balance}")


def main(args):
    num = len(blockchain.chain)
    tx_list.append(args)

    print(f"BLOCK ARGS: {type(args)}\n")
    print(f"transaction list: {tx_list}\n")

    block = Block(num, None, args, 0, None)
    blockchain.mine(block)

    return block


blockchain = Blockchain()
blockpool = BlockPool()
bc_client = Clients()
