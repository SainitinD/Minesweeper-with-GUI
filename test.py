import tkinter as tk
from PIL import ImageTk, Image
root = tk.Tk()
img = Image.open('assets/1.png')
img = ImageTk.PhotoImage(img.resize((20,20), Image.ANTIALIAS))
but = tk.Button(root)
but.pack()
but.configure(relief='groove', bd=2, state='disabled')
but.configure(image=img)
root.mainloop()