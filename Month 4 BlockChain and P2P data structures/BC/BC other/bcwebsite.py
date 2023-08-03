from flask import Flask, render_template, request, redirect, url_for

from rdvtcp import new_message
from blockchain import Wallet


app = Flask(__name__)
# setting up BC interface, create wallet, send txs, receive txs


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
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
