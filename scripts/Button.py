import tkinter as tk
import random
import time
from PIL import Image, ImageTk

class Button(tk.Button):
    """ Custom Button class for the mine-sweeper game. Objects of this class makes up the individual tiles in 
    my minesweeper game """

    def __init__(self, root=None, x_cord=0, y_cord=0, class_ref=None, val=0, image_dict=None, isPressed=False, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.class_ref = class_ref


        self.x_cord = x_cord
        self.y_cord = y_cord

        self.isPressed = isPressed
        self.Value = val

        self.image_dict = image_dict
        self.Flaged = False

    def button_click(self):
        """ Main method that gets called whenever a button gets clicked. """
        if self.isPressed is False:
            if self.Value == -1:
                self.button_side_click()
                self.class_ref.game_over()
                return
            self.isPressed = True
            self.configure(relief='groove', state='disabled', borderwidth=3, highlightbackground='#808080')
            self._set_bg()
            if self.Value == 0:
                self.class_ref.flood_fill_v2(self)
            self.button_reveal()
            self.update_flag_count()
            self.change_score()
            #self.class_ref.score -= 1
            #self.class_ref.check_game()

    def change_score(self):
        print(self.class_ref.score)
        self.class_ref.score -= 1
        self.class_ref.check_game()

    def button_side_click(self):
        """ Used by minesweeper's flood-fill algorithm to indirectly replicate the button_click effect. """
        if self.isPressed is False:
            self.isPressed = True
            self.configure(relief='groove', state='disabled', borderwidth=3, highlightbackground='#808080')
            self._set_bg()
            self.button_reveal()
            self.update_flag_count()
            self.change_score()

        #self.class_ref.score -= 1
        #self.class_ref.check_game()

    def _set_bg(self):
        """ Used internally to set the background color of tiles.
        If the button is a bomb, set the color to red. Otherwise, set the bg color to gray. """
        if self.Value >= 0:
            self.configure(bg='#BDBDBD')
        else:
            self.configure(bg='#DC143C')

    def set_bomb_green(self, result='won'):
        if result == 'won':
            self.configure(bg='#32CD32')
        else:
            self.configure(bg='#DC143C')

    
    def button_reveal(self):
        """ Reveal the button. Called by :meth: button_click and :meth: button_side_click """
        val = self.Value
        img = self.image_dict[val]
        self.configure(image=img)

    def right_click(self, event):
        """ Place a flag on the button if the player right-clicks it """
        if self.isPressed == False:
            if self.Flaged == False and self.class_ref.flag_count > 0:
                flag_img = self.image_dict[9]
                event.widget.configure(image=flag_img)
                self.Flaged = True
                self.class_ref.flag_count -= 1
                self.class_ref.bottom_frame.flag_clicked()
            elif self.Flaged == True:
                self.Flaged = False
                null = self.image_dict[0]
                event.widget.configure(image=null)
                self.class_ref.flag_count += 1
                self.class_ref.bottom_frame.flag_clicked()

    def update_flag_count(self):
        """ If a button is flagged and then clicked.
        This method makes sure to update the :attr: flag_remaining of :cls: mine_sweeper and :cls: top_frame. """
        if self.isPressed == True and self.Flaged == True:
            self.class_ref.flag_count += 1
            self.class_ref.top_frame.flag_clicked()
