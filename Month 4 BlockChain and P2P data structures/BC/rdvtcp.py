import socket
import threading
import multiprocessing
from multiprocessing import freeze_support
import time
from flask import Flask, render_template, request, redirect, url_for
from blockchain import Wallet


HEADER = 128

nodes = []
nodes_lock = threading.Lock()


"""app = Flask(__name__)
# setting up BC interface, create wallet, send txs, receive txs


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        created_wallet = Wallet.generate_keys(self=True)
        new_message(nodes, f"public_keyn:{created_wallet}")
        print(f"Created wallet: {created_wallet}")
        return redirect(url_for("wallet", public_key=created_wallet))

    if request.method == "GET":
        public_key = request.args.get("public_key")
        located_key = new_message(nodes, f"public_keyr:{public_key}")
        print(f"located key not found: {located_key}")
        if located_key:
            return redirect(url_for("wallet", public_key=public_key))
    return render_template("home.html")


@app.route("/wallet/<public_key>", methods=["GET", "POST"])
def wallet(public_key):
    if request.method == "POST":
        amt = request.form.get("amt")
        recpaddr = request.form.get("recpaddr")
        print(f"AMT:{amt} RECPADDR:{recpaddr}")
        new_message(nodes, f"tx:{public_key}:{amt}:{recpaddr}")

    wallet_balance = balance(public_key)
    new_message(nodes, "bal:" + str(public_key))
    return render_template(
        "wallet.html", public_key=public_key, wallet_balance=wallet_balance
    )
    # with in the wallet you have buy sell and send functions"""


def start_propagation(clientsock, caddr):
    response = clientsock.recv(HEADER).decode("utf-8")
    ip, port = response.split(" ")
    client = str(ip), int(port)

    add_node(client)

    print(f"RESPONSE:{caddr}:{response}")
    print(f"NODES:{nodes}")

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
                    except ConnectionResetError:
                        None
                    return
    print("Propagation done")


def add_node(args):
    with nodes_lock:
        nodes.append(args)


def new_message(nodes, args):
    print("sending to clients")
    print(nodes)
    for client in nodes:
        print(f"connecting to client: {client}")
        bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bcsock.connect(client)
        bcsock.sendall(f" ".encode("utf-8"))
        bcsock.sendall(f"{args}:{bcsock.getsockname()}".encode("utf-8"))
        print(f"sending: {args}")
        bcsock.close()


def generate_wallet():
    wallet = Wallet.generate_keys(self=True)
    return wallet


def balance(arg):
    balance = Wallet.get_balance(self=True, public_key=arg)
    return balance


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
            thread_sp = threading.Thread(
                target=start_propagation, args=(clientsock, addr)
            )
            thread_sp.start()
    except OSError as e:
        None


rdvthread = threading.Thread(target=rendevous, daemon=True)

if __name__ == "__main__":
    nodes_manager = multiprocessing.Manager()
    nodes = nodes_manager.list()
    rdvthread.start()
    # app.run(debug=True, port=8000)
