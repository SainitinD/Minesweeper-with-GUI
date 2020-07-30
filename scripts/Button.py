import tkinter as tk
import random
import time
from PIL import Image, ImageTk
#from Images import gather_images

class Button(tk.Button):
    """ Custom Button class for the mine-sweeper game. Objects of this class makes up the individual tiles in 
    my minesweeper game """

    def __init__(self, root=None, x_cord=0, y_cord=0, image_dict=None, class_ref=None, val=0, isPressed=False, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        # Set a reference to the mine_sweeper class
        self.class_ref = class_ref

        # X and Y coordinate of a button on the mine-sweeper grid
        self.x_cord = x_cord
        self.y_cord = y_cord

        # Indicite if the button has been pressed
        self.isPressed = isPressed

        # Hold the value of the button indicating how many mines surround it. 
        self.Value = val

        # get the image dictionary containing all image assets
        self.image_dict = image_dict

        # Indicate whether the button has a flag on it or not. 
        self.isFlaged = False

    def button_click(self):
        """ Main method that gets called whenever a button gets clicked. """
        if self.isPressed is False:
            self.isPressed = True
            self.configure(relief='groove', state='disabled', borderwidth=3, highlightbackground='#808080')
            self._set_bg()
            self.button_reveal()
            self.update_flag_count()
            self.change_score()
            if self.Value == -1:
                self.class_ref.game_over()
                return
            if self.Value == 0:
                self.class_ref.flood_fill_v2(self)

    def change_score(self):
        """ Called whenever a button is clicked. Changes the score in the mine_sweeper class"""
        self.class_ref.score -= 1
        self.class_ref.check_game()

    def solve_button_clicked(self):
        """ Activated when the solve button has been clicked. Just a low-poly version of button_click. 
        Makes all the buttons visible and sets the background of mines to red without messing with the attributes or minesweeper class. """
        self.configure(relief='groove', state='disabled', borderwidth=3, highlightbackground='#808080')
        self.button_reveal()
        self._set_bg()

    def _set_bg(self):
        """ Used internally to set the background color of tiles.
        If the button is a bomb, set the color to red. Otherwise, set the bg color to gray."""
        if self.Value >= 0:
            self.configure(bg='#BDBDBD')
        else:
            self.configure(bg='#DC143C')

    def set_bomb_green(self, result='won'):
        """ Sets the bomb's background color to green when the player wins the game. """
        if result == 'won':
            self.configure(bg='#32CD32')
        else:
            self.configure(bg='#DC143C')
    
    def button_reveal(self):
        """ Reveal the button. Called by :meth: button_click and :meth: button_side_click """
        val = self.Value
        img = self.image_dict[val]
        self.configure(image=img)
        self.configure(state='disabled', relief='groove')

    def right_click(self, event):
        """ Place a flag on the button if the player right-clicks it """
        if self.isPressed == False:
            if self.isFlaged == False and self.class_ref.flag_count > 0:
                flag_img = self.image_dict[9]
                event.widget.configure(image=flag_img)
                self.isFlaged = True
                self.class_ref.flag_count -= 1
            elif self.isFlaged == True:
                null = self.image_dict[0]
                event.widget.configure(image=null)
                self.isFlaged = False
                self.class_ref.flag_count += 1
            
            # Updates the flag counter on :cls: Bottom frame
            self.class_ref.bottom_frame.flag_clicked()

    def update_flag_count(self):
        """ If a button is flagged and then clicked.
        This method makes sure to update the :attr: flag_remaining of :cls: mine_sweeper and :cls: top_frame. """
        if self.isPressed == True and self.isFlaged == True:
            self.class_ref.flag_count += 1
            self.class_ref.bottom_frame.flag_clicked()