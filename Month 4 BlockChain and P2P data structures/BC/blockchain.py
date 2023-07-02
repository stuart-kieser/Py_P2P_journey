from hashlib import sha256
import time


def update_hash(*args):
    hashing_text = ""
    h = sha256()
    for arg in args:
        hashing_text += str(arg)

    h.update(hashing_text.encode("utf-8"))
    return h.hexdigest()


class Block:
    data = None
    hash = None
    nonce = 0
    previous_hash = "0" * 64

    def __init__(self, data, number=0):
        self.data = data
        self.number = number

    def hash(self):
        return update_hash(self.previous_hash, self.number, self.data, self.nonce)

    def __str__(self):
        return str(
            "Block#: %s\nHash: %s\nPrevious: %s\nData: %s\nNonce: %s\n"
            % (self.number, self.hash(), self.previous_hash, self.data, self.nonce)
        )


class Blockchain:
    difficulty = 3

    def __init__(self, chain=[]):
        self.chain = chain

    def add(self, block):
        self.chain.append(block)

    def mine(self, block):
        try:
            block.previous_hash = self.chain[-1].hash()
        except IndexError:
            pass

        while True:
            if block.hash()[: self.difficulty] == "0" * self.difficulty:
                self.add(block)
                break
            else:
                block.nonce += 1


def main():
    blockchain = Blockchain()
    database = ["genesis"]

    num = 0
    for data in range(50):
        num += 1
        struct_time = time.localtime()
        timestamp = time.mktime(struct_time)
        blockchain.mine(Block(timestamp, num))

    for block in blockchain.chain:
        print(block)


if __name__ == "__main__":
    main()
