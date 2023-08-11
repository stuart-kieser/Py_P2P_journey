import socket
import threading
from multiprocessing import freeze_support
import pickle


HEADER = 128

nodes = []
nodes_lock = threading.Lock()


def handle_client(clientsock, caddr):
    response = clientsock.recv(HEADER).decode("utf-8")
    print(response)
    ip, port = response.split(" ")
    client = str(ip), int(port)

    print(f"client added: {client}")

    if client not in nodes:
        add_node(client)

    msg = str(response).encode("utf-8")
    msg_len = len(msg)
    send_len = str(msg_len).encode("utf-8")
    send_len += b" " * (HEADER - len(send_len))

    data = clientsock.recv(HEADER).decode("utf-8")
    pnthread = threading.Thread(
        target=propagate_nodes, args=(clientsock, caddr), daemon=True
    )
    if data or response == "Prop":
        pnthread.start()


def propagate_nodes(clientsock, caddr):
    for other_client in nodes:
        ip, port = other_client
        nmsg = f"{ip} {port}".encode("utf-8")
        try:
            print(f"sending: {nmsg}")
            clientsock.send(nmsg)
        except ConnectionResetError or ConnectionAbortedError:
            pass

    print("Propagation done")


def add_node(args):
    with nodes_lock:
        nodes.append(args)


def new_message(tag, args):
    for client in nodes:
        bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bcsock.connect(client)
        pickled_msg = pickle.dumps((tag, args, bcsock.getsockname()))

        bcsock.sendall(pickled_msg)
        bcsock.close()


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
