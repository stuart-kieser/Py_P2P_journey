from hashlib import sha256
from typing import Optional
import time
import queue

gENESIS_HASH = "0" * 64

tx_pool = queue.Queue(maxsize=0)
tx_list = []


def update_hash(*args):
    hashing_text = ""
    h = sha256()

    for arg in args:
        hashing_text += str(arg)
    h.update(hashing_text.encode("utf-8"))

    return h.hexdigest()


def add_tx_to_pool(args):
    tx_pool.put(args)


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
        try:
            block.previous = self.chain[-1].get_hash()
        except IndexError:
            pass

        while True:
            if block.get_hash()[: self.difficulty] == "0" * self.difficulty:
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


class BlockPool:
    def __init__(self, block_pool=[]):
        self.block_pool = block_pool

    def add(self, block):
        self.block = block
        self.block_pool.append(block)
        print(f"blockpool updated:\n")

        if len(self.block_pool) == (len(bc_client.clients) + 1):
            validation(self)
            return


def validation(self):
    print("Block Pool size:", len(self.block_pool))
    print("Client list size:", (len(bc_client.clients) + 1), "\n")
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


def main(args):
    struct_time = time.localtime()
    timestamp = time.mktime(struct_time)

    print(f"Mining start time: {timestamp}\n")

    num = len(blockchain.chain)
    tx_list.append(args)

    print(f"BLOCK ARGS: {type(args)}\n")
    print(f"transaction list: {tx_list}\n")

    block = Block(num, None, args, 0, None)
    blockchain.mine(block)

    return block


def bc_update():
    num = len(blockchain.chain)
    while True:
        new_num = len(blockchain.chain)
        if new_num > num:
            new_num = num
        try:
            return blockchain.chain[-1]
        except IndexError:
            return None


blockchain = Blockchain()
blockpool = BlockPool()
bc_client = Clients()
