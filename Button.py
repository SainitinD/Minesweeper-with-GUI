import tkinter as tk
import random
import time
from PIL import Image, ImageTk

class Button(tk.Button):
    button_color_dict = {1: '#0000ff', 2: '#00f000', 3: '#ffff00', 4: '#00008b', 5: '#006400', 6: '#640000', 7: '#00ffff', 8: '#ff0000'}

    def __init__(self, root, x_cord, y_cord, class_ref, image_dict,   *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.class_ref = class_ref

        self.x_cord = x_cord
        self.y_cord = y_cord

        self.isPressed = False
        self.Value = 0

        self.image_dict = image_dict

    def button_click(self):
        if self.isPressed is False:
            self.isPressed = True
            self.configure(relief='groove', state='disabled', bg='#BDBDBD', borderwidth=2, highlightbackground='#808080')
            if self.Value == 0:
                self.class_ref.flood_fill(self)
            self.button_reveal()


    def button_side_click(self):
        self.isPressed = True
        self.configure(relief='groove', state='disabled', bg='#BDBDBD', borderwidth=2, highlightbackground='#808080')
        self.button_reveal()
        #self.configure(text=str(self.Value))
    
    def button_reveal(self):
        val = self.Value
        img = self.image_dict[val]
        self.configure(image=img)
            
