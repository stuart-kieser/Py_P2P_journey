import tkinter as tk
from blockchain import wallet, blockchain
import rdvtcp

FONT = ("Arial", 18)

root = tk.Tk()

root.geometry("1000x500")
root.title("BC GUI")

grid = tk.Grid()


node = tk.Button(
    command=rdvtcp.rdvthread.start(),
    height=2,
    width=20,
    state="active",
    font=("Arial", 12),
    text="Start node?",
)
node.pack(side="left")

wallet = tk.Button(
    command=wallet.generate_keys(),
    height=2,
    width=20,
    state="active",
    font=("Arial", 12),
    text="Create a wallet address",
)
wallet.pack(side="right")

sendframe = tk.Frame(root)
sendframe.pack()

# create send button
txbtn = tk.Button(sendframe, command=rdvtcp.new_message(args=None))
txbtn.pack(side="right")

# create send amount line
txamt = tk.Entry(sendframe, textvariable=int)
txamt.pack(side="left")

root.mainloop()
