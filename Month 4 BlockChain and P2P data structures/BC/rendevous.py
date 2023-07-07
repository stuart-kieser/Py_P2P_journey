import socket
import threading

known_port = 55555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("localhost", known_port))
print(f"binding port to: {known_port}")

condition = threading.Condition()
clients = []


def propogate_clients():
    while True:
        with condition:
            condition.wait()

            for client in clients:
                client_addr, client_port = client

                for other_client in clients:
                    other_client_addr, other_client_port = other_client

                    if client != other_client:
                        sock.sendto(b"ready", address)
                        sock.sendto(
                            "{} {} {}".format(
                                other_client_addr, other_client_port, known_port
                            ).encode(),
                            (client_addr, client_port),
                        )


thread = threading.Thread(target=propogate_clients)
thread.start()


while True:
    data, address = sock.recvfrom(1024)

    print("connection from: {}".format(address))
    clients.append(address)

    sock.sendto(b"ready", address)

    with condition:
        clients.append(address)
        condition.notify_all()
        print("propogating peer details to other peers")
        break
