import socket
import threading
import time
import random

known_port = 55555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("localhost", known_port))
print(f"binding port to: {known_port}")


clients = []
propogation_running = True
waiting_for_clients = False


def propogate_clients():
    while propogation_running:
        for client in clients:
            client_addr, client_port = client
            for other_client in clients:
                time.sleep(1)
                other_client_addr, other_client_port = other_client
                if client != other_client:
                    try:
                        sock.sendto(
                            "{} {} {}".format(
                                other_client_addr,
                                (other_client_port - 10),
                                known_port,
                            ).encode(),
                            (client_addr, client_port),
                        )
                    except ConnectionResetError:
                        print("Client closed the connection", client)


propogation = threading.Thread(target=propogate_clients, daemon=True)
propogation.start()

print(f"starting propogation: {propogation.getName()}")

while True:
    try:
        if waiting_for_clients:
            print("waiting for clients to join")
            time.sleep(10)
            continue

        data, address = sock.recvfrom(1024)

        print("connection from {}".format(address))
        print(f"address:{address} data:{data}")

        if address not in clients:
            sock.sendto(b"AKK", address)
            clients.append(address)

        print("Client List:", len(clients))
        if data.decode() == "AKK":
            print("Propagation halted, waiting for new connections")
            propogation_running = False
            waiting_for_clients = True
            continue

    except ConnectionResetError:
        print("Error receiving data")
