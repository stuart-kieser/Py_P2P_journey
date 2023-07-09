import socket
import threading

known_port = 55555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("localhost", known_port))
print(f"binding port to: {known_port}")


clients = []
propogation_running = False


def propogate_clients():
    while True:
        for client in clients:
            client_addr, client_port = client
            for other_client in clients:
                other_client_addr, other_client_port = other_client

                if client != other_client:
                    try:
                        sock.sendto(
                            "{} {} {}".format(
                                other_client_addr, other_client_port, known_port
                            ).encode(),
                            (client_addr, client_port),
                        )
                    except ConnectionResetError:
                        print("Client closed the connection", client)
                    break


propogation = threading.Thread(target=propogate_clients)
propogation.start()

while True:
    try:
        data, address = sock.recvfrom(1024)
        print("connecting from {}".format(address))
        print(address, data)
        sock.sendto(b"AKK", address)
        clients.append(address)
        print("Client List:", len(clients))
        print(f"starting propogation: {propogation}")
    except:
        if ConnectionResetError:
            print("Error receiving data")
        break
