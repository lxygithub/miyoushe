import tkinter as tk

root = tk.Tk()
root.geometry("200x200")

button1 = tk.Button(root, text="Button 1", height=3)
button1.grid(row=0, column=0, sticky="ns")

button2 = tk.Button(root, text="Button 2")
button2.grid(row=1, column=0, sticky="ew", pady=(5, 0))

root.mainloop()
