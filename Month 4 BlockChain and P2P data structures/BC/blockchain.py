from hashlib import sha256
from typing import Optional
import time
import subprocess

GENESIS_HASH = "0" * 64
tx_pool = []


def update_hash(*args):
    hashing_text = ""
    h = sha256()

    for arg in args:
        hashing_text += str(arg)

    hash = h.update(hashing_text.encode("utf-8"))
    return h.hexdigest()


class Block:
    # actual block structure
    number: int
    previous: Optional["Block"]
    data: Optional[dict]
    nonce: int
    timestamp: any

    def __init__(
        self, number=0, previous=None, data=None, nonce=0, timestamp=any
    ) -> None:
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

    def get_transaction(self):
        tx_list = []
        for tx in tx_pool in range(10):
            tx_list.append(tx)


class Blockchain:
    difficulty = 3

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

    def get_transaction(self):
        tx_list = []
        for i, tx in enumerate(tx_pool):
            tx_list.append(tx)
            if i == 9:
                break
        return tx_list


def blockchain_broadcast_update(number, data, previous, nonce, timestamp):
    block = Block(number, data, previous, nonce, timestamp)
    Blockchain.mine(block)


def main():
    blockchain = Blockchain()

    num = len(blockchain.chain)

    num += 1

    for num in range(25):
        tx = blockchain.get_transaction()
        blockchain.mine(Block(num, None, tx))

    for block in blockchain.chain:
        print(block)
        print(blockchain.isValid())


if __name__ == "__main__":
    main()
