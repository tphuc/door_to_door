from tkinter import *

root = Tk()
variable = StringVar(root)
variable.set("one")
w = OptionMenu(root, variable, "one", "two", "three")
w.pack()


mainloop()