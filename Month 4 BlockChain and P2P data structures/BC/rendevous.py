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
            print(f"Propagating clients to client: {client_addr, client_port}")
            for other_client in clients:
                time.sleep(2)
                other_client_addr, other_client_port = other_client
                print(f"client: {client}, otherClient: {other_client}")
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
                        print("client sent")
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

        sock.sendto(b"AKK", address)
        if address not in clients:
            clients.append(address)

        print("Client List:", len(clients))
        if data.decode() == "AKK":
            propogation_running = False
            waiting_for_clients = True
            print("Propagation halted, waiting for new connections")

    except ConnectionResetError:
        print("Error receiving data")
        break


def test_bc():
    while True:
        a = "txu:sender:amount:receiver"
        b = "bcu:number:data:previous"
