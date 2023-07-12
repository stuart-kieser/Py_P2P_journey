from hashlib import sha256
from typing import Optional
import time
import queue
import random
import threading

GENESIS_HASH = "0" * 64

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
    print(f"adding tx to pool: {args}")
    tx_pool.put(args)


class Block:
    # actual block structure

    number: int
    previous: Optional["Block"]
    data: Optional[dict]
    nonce: int
    timestamp: any

    def __init__(self, number=0, previous=any, data=any, nonce=0, timestamp=any) -> any:
        self.number = number
        self.data = data
        self.previous = previous
        self.nonce = nonce
        self.timestamp = timestamp

    def get_previous_hash(self):
        if self.previous is None:
            return GENESIS_HASH
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
                self.get_timestamp(),
            )
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
                self.add(block)
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


def blockchain_broadcast_update(args):
    block_chain = Blockchain()
    block = Block(args)
    block_chain.mine(Block(args))
    return block


def get_tx():
    return tx_list


def main(args):
    struct_time = time.localtime()
    timestamp = time.mktime(struct_time)
    print(timestamp)
    num = len(blockchain.chain)
    initial_tx_pool = tx_pool.qsize()
    if tx_pool.qsize() != initial_tx_pool:
        for tx in tx_pool not in tx_list:
            tx = tx_pool.get()
            tx_list.append(tx)
    print(f"BLOCK ARGS: {type(args)}")
    block = Block(num, None, args, None, None)
    print(f"transaction list: {tx_list}")
    print(block)
    for block in blockchain.chain:
        print(block)
        print(blockchain.isValid())


blockchain = Blockchain()
