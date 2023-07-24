import socket
import threading
import time

nodes = []

HEADER = 128


# create rendevous server for nodes
def rendevous():
    rsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rende_addr = ("localhost", 7000)

    # bind, listen: rende
    rsock.bind(rende_addr)
    rsock.listen()

    while True:
        clientsock, addr = rsock.accept()
        thread_sp = threading.Thread(target=start_propagation, args=(clientsock, addr))
        thread_sp.start()


def start_propagation(clientsock, caddr):
    time.sleep(3)
    response = clientsock.recv(HEADER).decode("utf-8")
    print(f"{caddr}:{response}")
    ip, port = response.split(" ")
    client = ip, port
    nodes.append(client)
    msg = str(response).encode("utf-8")
    msg_len = len(msg)
    send_len = str(msg_len).encode("utf-8")
    send_len += b" " * (HEADER - len(send_len))
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
                        time.sleep(0.2)
                    except ConnectionResetError:
                        None


def new_wallet_addr(public_key):
    for client in nodes:
        bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bcsock.bind(("localhost", 0))
        bcsock.connect(client)
        bcsock.send(f"public_key:{public_key}".encode("utf-8"))
        bcsock.close()
