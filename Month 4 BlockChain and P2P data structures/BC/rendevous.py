import socket
import threading

known_port = 55555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("localhost", known_port))
print(f"binding port to: {known_port}")

while True:
    clients = []

    while True:
        data, address = sock.recvfrom(1024)

        print("connection from: {}".format(address))
        clients.append(address)

        sock.sendto(b"ready", address)

        if len(clients) > 1:
            print("propogating peer details to other peers")
            break

    c1 = clients.pop()
    c1_addr, c1_port = c1
    c2 = clients.pop()
    c2_addr, c2_port = c2

    sock.sendto("{} {} {}".format(c1_addr, c1_port, known_port).encode(), c2)
    sock.sendto("{} {} {}".format(c2_addr, c2_port, known_port).encode(), c1)
