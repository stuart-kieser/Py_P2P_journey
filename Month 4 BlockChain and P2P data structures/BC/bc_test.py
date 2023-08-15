import unittest
from unittest.mock import MagicMock, patch
import threading
from blockchain import (
    Block,
    Blockchain,
    Wallet,
    Transaction,
    Container,
    GENESIS_HASH,
    Server,
    MessageFunctions,
    Clients,
    TransactionPool,
)


class TestBlock(unittest.TestCase):
    def test_get_previous_hash(self):
        # Initialize a mock Block object
        blockchain = Blockchain()
        server = Server("localhost", 0)
        clients = Clients()
        clients.add(server.main_addr)
        wallet = Wallet()

        block3 = Block(address=wallet, previous=None)
        blockchain.mine(block3)

        block2 = Block(address=wallet, previous=None)
        blockchain.mine(block2)

        block = Block(address=wallet, previous=None)
        blockchain.mine(block)

        print(f"\nblock previous hash: {block3.previous}\n")
        print(f"\nblock previous hash: {block2.previous}\n")
        print(f"\nblock previous hash: {block.previous}\n")

        self.assertEqual(blockchain.chain[-1], block2.get_hash())

    def test_get_hash(self):
        wallet = Wallet()
        block = Block(address=wallet, number=1)
        self.assertIsInstance(block.get_hash(), str)

    # Add more tests for Block class here


class TestBlockchain(unittest.TestCase):
    def test_isValid(self):
        # Initialize a mock Block object
        block = MagicMock()
        block.get_hash.return_value = "h.hexdigest()"
        blockchain = Blockchain(chain=[block])

        self.assertIs(blockchain.isValid(block), block)

    # Add more tests for Blockchain class here


class TestWallet(unittest.TestCase):
    def test_get_balance(self):
        wallet = Wallet(public_key="public_key")
        blockchain = MagicMock()
        blockchain.chain = [MagicMock()]
        wallet.get_balance(public_key="public_key")
        # Perform your assertions here

    # Add more tests for Wallet class here


class TestTransaction(unittest.TestCase):
    def test_valid_amount(self):
        sender_wallet = MagicMock()
        recipient_wallet = MagicMock()
        sender_wallet.get_balance.return_value = 100

        tx = Transaction(sender=sender_wallet, amount=50, recipient=recipient_wallet)
        self.assertTrue(tx.valid_amount(sender_wallet))

    # Add more tests for Transaction class here


class TestContainer(unittest.TestCase):
    def test_generate_id(self):
        container = Container(owner="owner", containerid=None, container=None)
        self.assertIsInstance(container.generate_id(), str)

    # Add more tests for Container class here


class TestServer(unittest.TestCase):
    clients = Clients()

    server = Server("localhost", 0)
    clients.add(server.main_addr)

    def create_tx():
        messagefunctions = MessageFunctions()
        txpool = TransactionPool()
        for i in range(10):
            wallet = Wallet()
            wallet2 = Wallet()
            tx = Transaction(wallet, 100, wallet2)
            print(f"sending tx")
            messagefunctions.bc_interact("tx", tx)

        for tx in txpool.tx_pool:
            print(f"TX: {tx}")

    threading.Thread(target=server.server, daemon=True)
    threading.Thread(target=create_tx, daemon=True)


if __name__ == "__main__":
    unittest.main()
