import socket
import threading
import time
from flask import Flask, render_template, request, redirect, url_for
from blockchain import Wallet

nodes = []

HEADER = 128

app = Flask(__name__)
# setting up BC interface, create wallet, send txs, receive txs


# create rendevous server for nodes
def rendevous():
    rsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rende_addr = ("localhost", 7000)
    print("RDV starting")

    # bind, listen: rende
    rsock.bind(rende_addr)
    rsock.listen(5)

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


def new_message(args):
    print("sending to clients")
    for client in nodes:
        print("connecting to client")
        bcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bcsock.bind(("localhost", 0))
        bcsock.connect(client)
        bcsock.send(f"{args}".encode("utf-8"))
        print(f"sending: {args}")
        data = bcsock.recv(HEADER).decode()
        if data:
            bcsock.close()
            return data


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if request.form.get("form1"):
            created_wallet = generate_wallet()
            print("BCweb sending message")
            new_message("public_keyn:" + str(created_wallet))
            return redirect(url_for("wallet", public_key=created_wallet))

    if request.method == "GET":
        public_key = request.args.get("public_key")
        located_key = new_message("public_keyr:" + str(public_key))
        print(f"located key not found: {located_key}")
        if located_key:
            return redirect(url_for("wallet", public_key=public_key))
    return render_template("home.html")


@app.route("/wallet/<public_key>", methods=["GET", "POST"])
def wallet(public_key):
    wallet_balance = balance(public_key)
    new_message("bal" + str(public_key))
    return render_template(
        "wallet.html", public_key=public_key, wallet_balance=wallet_balance
    )
    # with in the wallet you have buy sell and send functions


def generate_wallet():
    wallet = Wallet.generate_keys(self=True)
    return wallet


def balance(arg):
    balance = Wallet.get_balance(self=True, public_key=arg)
    return balance


if __name__ == "__main__":
    thread_1 = threading.Thread(target=rendevous)
    thread_1.start()
    app.run(debug=True, port=8000)
