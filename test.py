import tkinter as tk
from PIL import ImageTk, Image
root = tk.Tk()

top_frame = tk.LabelFrame(root, text='touchy')
top_frame.grid(row=0, rowspan=5, columnspan=100)

bottom_frame = tk.LabelFrame(top_frame, text='bottom')
bottom_frame.grid(row=6, columnspan=100)

button_1 = tk.Button(top_frame, text='Clicky')
button_1.grid(row=0, padx=10)

#button_2 = tk.Button(top_frame, text='Clicky2')
#button_2.grid(row=0, padx=10)

button_3 = tk.Button(bottom_frame, text='Clicky')
button_3.pack()

root.mainloop()