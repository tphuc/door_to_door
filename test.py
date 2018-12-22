import tkinter as tk

def show():
    canvas.pack()

def hide():
    canvas.pack_forget()

root = tk.Tk()
root.geometry("400x400")
canvas_parent = tk.Canvas(root)
show_button = tk.Button(root, text="show", command=show)
hide_button = tk.Button(root, text="hide", command=hide)

canvas = tk.Canvas(root, background="pink")
show_button.pack(side="top")
hide_button.pack(side="top")
canvas.pack(side="top")

root.mainloop()