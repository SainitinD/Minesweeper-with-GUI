import tkinter as tk
import random
import copy
from tkinter import messagebox

from Frames import Bottom_frame#, Top_frame
from Button import Button


class Mine_Sweeper(tk.Frame):

    game_size = {'easy': (8,10),
                 'medium': (14,18),
                 'hard': (20,24)}

    bomb_max = {'easy': 10, 'medium': 40, 'hard': 99}

    def __init__(self, root, image_dict, game_mode='easy', *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.root = root

        # Get the grid size based on the chosen game-mode
        self.grid_size = self.game_size[game_mode]

        # Get the maximum no. of bombs for the specified gamemode
        self.num_of_bombs = self.bomb_max[game_mode]

        # Contains a list to contain all the bomb locations
        self.bomb_location_list = []

        # Contains a dictionary of all the assets. 
        self.image_dict = image_dict

        # A grid filled with button objects
        self.grid = []

        self.flag_count = self.bomb_max[game_mode]

        #self.top_frame = Top_frame(root, self)

        self.mid_frame = tk.LabelFrame(root, bd=6)
        self.mid_frame.grid(row=1, columnspan=self.grid_size[1], rowspan=self.grid_size[0])

        self.bottom_frame = Bottom_frame(root, self)

        self.score = self.grid_size[0] * self.grid_size[1] - self.num_of_bombs

        # Assemble the game
        self.main()


    def main(self):
        """ Initialize the game """
        self.create_grid()
        self.create_bombs()
        self.update_button_scores()
        #self.set_images()
        #self.show_all_nums()

    
    def create_grid(self):
        """ Creates the object's grid filled with button objects """
        x_max, y_max = self.grid_size

        cls_ref = self

        for x_cord in range(x_max):
            small_list = []
            for y_cord in range(y_max):
                button = Button(root = self.mid_frame, x_cord = x_cord, y_cord = y_cord, val=0, class_ref=cls_ref, isPressed = False, image_dict=self.image_dict, image=self.image_dict[0], relief='raised', bd=3)
                button.configure(command = button.button_click)
                button.bind("<Button-3>", button.right_click)
                button.grid(row=x_cord+1, column=y_cord+1)
                small_list.append(button)
            self.grid.append(small_list)

    def create_bombs(self):
        """ Updates the object's grid with bombs """
        
        for i in range(self.num_of_bombs):
            # Update the button's value to indicate bomb
            x_cord, y_cord = self.get_random_coord()
            self.grid[x_cord][y_cord].Value = -1

            # Add the bomb locations to bomb locations list
            self.bomb_location_list.append((x_cord, y_cord))

    def get_random_coord(self):
        max_x_idx = self.grid_size[0]-1
        max_y_idx = self.grid_size[1]-1
        while True:
            random_x = random.randint(0, max_x_idx)
            random_y = random.randint(0, max_y_idx)

            coord = (random_x, random_y)

            if coord not in self.bomb_location_list:
                return coord
            else:
                continue

    def update_button_scores(self):
        for bomb_location in self.bomb_location_list:
            #print('===================BOMB at location ({}) finished ======================'.format(bomb_location))
            #x_cord, y_cord = bomb_location
            #for x in range(x_cord-1, x_cord+2):
                #for y in range(y_cord-1, y_cord+2):
            for x,y in self.get_surround_coords(bomb_location):
                try:
                    assert 0 <= x and x < self.grid_size[0]
                    assert 0 <= y and y < self.grid_size[1]

                    val = self.grid[x][y].Value
                    if val != -1:
                        self.grid[x][y].Value += 1
                        #print('Button at ( {}, {} ) had value changed from {} to {}'.format(x, y, val, self.grid[x][y].Value))
                except:
                    continue


    def get_surround_coords(self, coord):
        coord_list = []

        x_cord, y_cord = coord
        for x in range(x_cord-1, x_cord+2):
            for y in range(y_cord-1, y_cord+2):
                coord_list.append((x,y))

        return coord_list

    def flood_fill_v2(self, button):
        coords = button.x_cord,button.y_cord
        coords = self.get_surround_coords(coords)

        for new_x,new_y in coords:
            try:
                #new_x, new_y = x-1, y
                assert (0 <= new_x < self.grid_size[0])
                assert (0 <= new_y < self.grid_size[1])
                new_button = self.grid[new_x][new_y]
                val = new_button.Value

                if val == 0:
                    new_button.button_click()
                    #self.flood_fill(new_button)
                elif val != -1:
                    new_button.button_side_click()
            except:
                continue

    def show_all_nums(self):
        for smal_list in self.grid:
            for button in smal_list:
                if button.Value != 0:
                    button.configure(text=str(button.Value))

#columnspan=self.grid_size[1], ipady=5, ipadx=self.grid_size[1]*8)

    def reset_game(self):
        self.reset_values()
        self.main()

    def solve_game(self):
        for smal_list in self.grid:
            for button in smal_list:
                button.button_side_click()
                button.configure(state='disabled', relief='groove')

    def reset_values(self):
        for small_list in self.grid:
            for button in small_list:
                del button
        del self.bomb_location_list
        del self.grid
        del self.flag_count
        del self.score
        self.flag_count = copy.copy(self.num_of_bombs)
        self.bomb_location_list = []
        self.grid = []
        self.score = self.grid_size[0] * self.grid_size[1] - self.num_of_bombs

    def game_over(self):
        self.disable_buttons()
        label = messagebox.showinfo("GAME OVER", "YOU LOSE")
        self.reveal_bombs('lost')

    def game_won(self):
        label = messagebox.showinfo("GAME OVER", "YOU WIN!!!")
        self.reveal_bombs('won')


    def check_game(self):
        if self.score <= 0:
            self.game_won()

    def reveal_bombs(self, result='won'):
        for bomb_location in self.bomb_location_list:
            x,y = bomb_location
            button = self.grid[x][y]
            button.set_bomb_green(result)
            button.button_reveal()

    def disable_buttons(self):
        for small_list in self.grid:
            for button in small_list:
                button.configure(state='disabled')

