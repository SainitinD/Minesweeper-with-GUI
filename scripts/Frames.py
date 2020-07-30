import tkinter as tk
from Images import get_smile_img, get_flag_img
import threading
import time

class Bottom_frame:
    """ The bottom frame of the mine sweeper game """
    def __init__(self, root, class_ref):
        # Define a frame to place all the widgets onto. 
        self.frame = tk.LabelFrame(root,bd=7)

        # get the total ammount of flags from :cls: mine_sweeper 
        self.flag_count = class_ref.flag_count
        # get the flag image
        self.flag_img = get_flag_img()
        # define a flag label that indicates the ammount of mines on field. 
        self.flag_label = tk.Label(self.frame,
                                   image=self.flag_img,
                                   text=': {}'.format(self.flag_count),
                                   compound='left',
                                   relief='ridge'
        )
        # Place the flag label onto the pre-defined frame
        self.flag_label.pack(side=tk.LEFT,
                             padx=18,
                             ipadx=8,
                             ipady=1,
                             pady=1
        )

        # get the smile image
        self.smile_img = get_smile_img((30,22))
        # define the smile button that resets the game whenever the player clicks on it. 
        self.smile_button = tk.Button(self.frame,
                                      image=self.smile_img,
                                      bd=3,
                                      relief='raised',
                                      command=self.smile_click
        )
        # put the smile button inside the pre-defined frame
        self.smile_button.pack(side=tk.LEFT,
                               padx=18,
                               ipady=1,
                               pady=1
        )

        # Create a solve button that solves the game whenever the player clicks it. 
        self.solve_button = tk.Button(self.frame,
                                      text='SOLVE',
                                      bd=3,
                                      relief='raised',
                                      command=class_ref.solve_game
        )

        # place the solve button onto the pre-defined frame. 
        self.solve_button.pack(side=tk.LEFT,
                               padx=18,
                               ipadx=10,
                               ipady=1,
                               pady=1
        )

        # Place the pre-defined frame onto the main screen. 
        self.frame.grid(row=class_ref.grid_size[0]+1,
                        ipady=0,
                        columnspan=class_ref.grid_size[1],
                        ipadx=class_ref.grid_size[0]*0
        )

        # get a reference for the main mine_sweeper class. 
        self.class_ref = class_ref

    def smile_click(self):
        """ Function linked to the smile button. Resets the game when clicked. """
        self.class_ref.reset_game()
    
    def flag_clicked(self):
        """ Function linked to the flag label. Updates the flag-remaining counter """
        self.flag_label.configure(text=': {}'.format(self.class_ref.flag_count))