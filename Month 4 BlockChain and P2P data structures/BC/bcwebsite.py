import socket
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from blockchain import Wallet, Blockchain, wallet_addrs
from rdvtcp import new_wallet_addr, nodes

app = Flask(__name__)
# setting up BC interface, create wallet, send txs, receive txs


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        selfwallet = your_wallet()
        # send wallet address to rdvserver
        own_public_key = selfwallet.public_key
        print(selfwallet)
        new_wallet_addr(public_key=own_public_key)
        return redirect(url_for("wallet", own_public_key))
    return render_template("home.html")


@app.route("/wallet/<public_key>", methods=["GET"])
def wallet(public_key):
    return render_template("wallet.html")
    # with in the wallet you have buy sell and send functions


def your_wallet():
    wallet = Wallet()
    return wallet


if __name__ == "__main__":
    app.run(debug=True)
