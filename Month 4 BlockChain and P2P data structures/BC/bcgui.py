import tkinter as tk
from blockchain import wallet

FONT = ("Arial", 18)

root = tk.Tk()

root.geometry("1000x500")
root.title("BC GUI")

label = tk.Label(root, text="Start node.", font=FONT)
label.pack(padx=20, pady=20)

textbox = tk.Text(root, height=3, font=FONT)
textbox.pack()

button = tk.Button(root, text="START NODE", font=FONT, command=wallet.generate_keys)
button.pack()


buttonframe = tk.Frame()
buttonframe.columnconfigure(0, weight=1)
buttonframe.columnconfigure(1, weight=1)
buttonframe.columnconfigure(2, weight=1)

btn1 = tk.Button(buttonframe, text="1", font=FONT)
btn1.grid(row=0, column=0, sticky=tk.W + tk.E)

btn2 = tk.Button(buttonframe, text="2", font=FONT)
btn2.grid(row=1, column=1, sticky=tk.W + tk.E)

buttonframe.pack(fill="x")

root.mainloop()
