import socket
import threading
from multiprocessing import freeze_support
from blockchain import Wallet


HEADER = 128

nodes = []
nodes_lock = threading.Lock()


def handle_client(clientsock, caddr):
    response = clientsock.recv(HEADER).decode("utf-8")
    ip, port = response.split(" ")
    client = str(ip), int(port)

    print(f"client added: {client}")
    add_node(client)

    msg = str(response).encode("utf-8")
    msg_len = len(msg)
    send_len = str(msg_len).encode("utf-8")
    send_len += b" " * (HEADER - len(send_len))

    data = clientsock.recv(HEADER).decode("utf-8")
    prpthread = threading.Thread(
        target=propagate_nodes, args=(clientsock, caddr), daemon=True
    )
    if data == "Prop":
        prpthread.start()


def propagate_nodes(clientsock, caddr):
    connected = True
    while connected:
        for client in nodes:
            for other_client in nodes:
                if client != other_client:
                    ip, port = other_client
                    nmsg = f"{ip} {port}".encode("utf-8")
                    # Remove the brackets and split the string into IP and port components
                    try:
                        clientsock.send(nmsg)
                    except:
                        ConnectionResetError or ConnectionAbortedError
                        None
    print("Propagation done")


def add_node(args):
    with nodes_lock:
        nodes.append(args)


def new_message(args):
    for client in nodes:
        bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bcsock.connect(client)
        bcsock.sendall(f"{args}:{bcsock.getsockname()}".encode("utf-8"))
        bcsock.close()


def generate_wallet():
    wallet = Wallet.generate_keys(self=True)
    return wallet


# create rendevous server for nodes
def rendevous():
    rsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rende_addr = ("localhost", 7000)
    # bind, listen: rende
    try:
        rsock.bind(rende_addr)
        rsock.listen(5)
        while True:
            clientsock, addr = rsock.accept()
            print(f"client connected:{clientsock}")
            thread_sp = threading.Thread(target=handle_client, args=(clientsock, addr))
            thread_sp.start()
    except OSError as e:
        None


rdvthread = threading.Thread(target=rendevous, daemon=True)

if __name__ == "__main__":
    rdvthread.start()
