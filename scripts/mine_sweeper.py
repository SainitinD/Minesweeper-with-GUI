import tkinter as tk
import random
import copy
import math

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

        # The main root.
        self.root = root

        # Get the grid size based on the chosen game-mode
        self.grid_size = self.game_size[game_mode]

        # Get the maximum no. of bombs for the specified gamemode
        self.num_of_bombs = self.bomb_max[game_mode]

        # Contains a list to contain all the bomb locations
        self.bomb_location_list = []

        # Contains a dictionary of all the assets. It is fed as a parameter to each button instance.  
        self.image_dict = image_dict

        # A grid that will hold all the references to button (tile) objects. 
        self.grid = []

        # A flag count same as num.of bombs for outside classes to reference. 
        self.flag_count = self.bomb_max[game_mode]

        # A frame which contains all the GUI of button objects. 
        self.top_frame = tk.LabelFrame(root, bd=6)
        self.top_frame.grid(row=1, columnspan=self.grid_size[1], rowspan=self.grid_size[0])

        # An instance of bottom_frame. It is the container of all the widgets underneath the grid. 
        self.bottom_frame = Bottom_frame(root, self)

        # A Score var holding max ammount of points. 
        self.score = self.grid_size[0] * self.grid_size[1] - self.num_of_bombs

        # A bool to check if the game is over or not.
        self.is_game_over = False

        self.effect_count = round(self.num_of_bombs * .15)

        self.effect_location_list = set()

        # Assemble the game
        self.main()


    def main(self):
        """ Initialize the game """
        self.create_grid()
        self.create_bombs()
        self.update_button_scores()
        self.create_magic_nums(self.effect_count)
        #self.show_all_bombs()

    
    def create_grid(self):
        """ Creates the object's grid filled with button objects """
        x_max, y_max = self.grid_size

        cls_ref = self

        for x_cord in range(x_max):
            small_list = []
            for y_cord in range(y_max):
                # Create the button object. 
                button = Button(root = self.top_frame,
                                x_cord = x_cord,
                                y_cord = y_cord,
                                val=0,
                                class_ref=cls_ref,
                                isPressed = False,
                                image_dict=self.image_dict,
                                image=self.image_dict[0],
                                relief='raised',
                                bd=3
                )

                # Set the button clicked action to its :meth: left_click
                button.configure(command = button.left_click)
                # Bind the button's right-click action to its :meth: right_click
                button.bind("<Button-3>", button.right_click)
                # Place the button on the grid. 
                button.grid(row=x_cord+1, column=y_cord+1)
                small_list.append(button)
            self.grid.append(small_list)

    def create_bombs(self):
        """ Updates the object's grid with bombs """
        for i in range(self.num_of_bombs):
            # Get a random coordinate to put the bomb. 
            x_cord, y_cord = self._get_random_coord()
            
            # Place the bomb. -1 indictes a bomb. 
            button = self.grid[x_cord][y_cord]
            button.Value = -1

            # Add the bomb's location to the bomb locations list
            self.bomb_location_list.append((x_cord, y_cord))

    def create_magic_nums(self, max_num):
        """ Create the magic numbers """
        for i in range(max_num):
            x, y = self._get_random_magic_coord()
            button = self.grid[x][y]
            button.isGold = True

    def _get_random_magic_coord(self):
        """ Creates a random x,y coordinate on the grid.
            Utilized by :meth: create_bombs to create bombs on grid. 
        """
        max_x_idx = self.grid_size[0]-1
        max_y_idx = self.grid_size[1]-1
        while True:
            random_x = random.randint(0, max_x_idx)
            random_y = random.randint(0, max_y_idx)

            try:
                button = self.grid[random_x][random_y]
                assert button.Value > 0
            except:
                print(button.get_coords())
                continue

            coord = (random_x, random_y)
            # Make sure the coordinate doesn't already have a bomb. 
            if coord not in self.effect_location_list:
                return coord
            else:
                continue
    def _get_random_coord(self):
        """ Creates a random x,y coordinate on the grid.
            Utilized by :meth: create_bombs to create bombs on grid. 
        """
        max_x_idx = self.grid_size[0]-1
        max_y_idx = self.grid_size[1]-1
        while True:
            random_x = random.randint(0, max_x_idx)
            random_y = random.randint(0, max_y_idx)

            coord = (random_x, random_y)

            # Make sure the coordinate doesn't already have a bomb. 
            if coord not in self.bomb_location_list:
                return coord
            else:
                continue

    def update_button_scores(self):
        """ For each bomb_location from bomb_location_list, this function increases the surrounding (1-tile) button's value.
            FYI: The higher the value a tile shows, the greater the ammount of bombs surrounding it.
        """
        for bomb_location in self.bomb_location_list:
            for x,y in self.get_surround_coords(bomb_location):
                try:
                    val = self.grid[x][y].Value
                    if val != -1:
                        self.grid[x][y].Value += 1
                except:
                    continue


    def get_surround_coords(self, coord):
        """ Creates a generator containting the indices of tiles that surround the :arg: coord.
            Each iteration it sends a coordinate of a tile around the initial coord. 
        
        Args:
            coord (tuple): A tuple containing x,y coords of the function. 
        Returns:
            coord_list (list of tuples): A list of tuples containing indices of surrounding tiles. 
        """

        x_cord, y_cord = coord
        #upd_coord = set()
        #upd_coord = {yieldfor x in range(x_cord-1, x_cord+2) for y in range(y_cord-1, y_cord+2)}
        for x in range(x_cord-1, x_cord+2):
            for y in range(y_cord-1, y_cord+2):
                # Make sure the surrounding coords isn't negatives.
                try:
                    assert 0 <= x and x < self.grid_size[0]
                    assert 0 <= y and y < self.grid_size[1]
                    yield x,y
                except:
                    continue

    def flood_fill_v2(self, button):
        """ The main brains of the minesweeper. This is my implementation of the flood-fill algorithm. 
            Bascially, whenever you click a 0, this algorithm gets called and bascially reveals all the 0's
            connected to this zero. It also reveals a single tile around the pool of zeros. 
        
        Args:
            button (obj) : A reference to the inital 0 value button is passed here.
        """
        coords = button.x_cord,button.y_cord
        coords = self.get_surround_coords(coords)

        for new_x,new_y in coords:
            try:
                # # Make sure the coords are on the grid and not negative. 
                # assert (0 <= new_x < self.grid_size[0])
                # assert (0 <= new_y < self.grid_size[1])
                
                new_button = self.grid[new_x][new_y]
                val = new_button.Value
                if val == 0:
                    new_button.isGold == False
                    new_button.left_click()     
                elif val != -1:
                    new_button.left_click()
            except:
                continue

    def reset_game(self):
        """ This function is called whenever the smiley face is clicked. Basically resets the game. """
        self._reset_values()
        self.main()

    def _reset_values(self):
        """ Internal function used to reset values in the mine_sweeper class. """
        for button in self._getbutton():
            del button
        del self.bomb_location_list
        del self.grid
        del self.flag_count
        del self.score
        self.flag_count = copy.copy(self.num_of_bombs)
        self.bomb_location_list = []
        self.grid = []
        self.score = self.grid_size[0] * self.grid_size[1] - self.num_of_bombs
        self.is_game_over = False
        self.flag_count = self.num_of_bombs

    def solve_game(self):
        """ Called whenever the solve button is clicked.
            Basically, iterates through each button and reveals its value with its appropriate image.
        """
        if self.is_game_over == False: 
            for smal_list in self.grid:
                for button in smal_list:
                    button.solve_button_clicked()#.button_side_click()
            self.is_game_over = True

    def game_over(self):
        """ Called whenever the player clicks on a bomb.
            Displays 'GameOver' message and reveals all bombs
        """
        self._disable_buttons()
        label = messagebox.showinfo("GAME OVER", "YOU LOSE")
        self._reveal_bombs('lost')
        self.is_game_over = True

    def _disable_buttons(self):
        """ Used internally inside the game_over function.
            Disables all the buttons inside the grid.
        """
        for button in self._getbutton():
            button.configure(state='disabled')

    def _getbutton(self):
        """ A generator that yields a each button from the self.grid attribute.
            Created to increase the efficiency of the program. 
        """
        for small_list in self.grid:
            for button in small_list:
                yield button

    def _game_won(self):
        """ Called when the player successfully finds all the numbers without clicking on any mines.
            Displays 'YOU WON' message and reveals the bombs with a green background.
        """
        label = messagebox.showinfo("GAME OVER", "YOU WIN!!!")
        self._reveal_bombs('won')
        self.is_game_over = True

    def check_game(self):
        """ Called whenever a button is clicked. If the mine_sweeper's
            score attribute is zero or lower, indicates the player has won. 
        """
        if self.score <= 0:
            self._game_won()

    def _reveal_bombs(self, result='won'):
        """ Used internally to reveal the bombs and set their backgrounds depending on result's value.
            If result is 'won', background is green. Else its red.
        """
        for bomb_location in self.bomb_location_list:
            x,y = bomb_location
            button = self.grid[x][y]
            button.set_bomb_green(result)
            button.reveal()

    def get_score(self):
        return self.score

    def update_score(self, new_score):
        self.score += new_score

    def get_flagcount(self):
        return self.flag_count

    def update_flagcount(self, new_flagcount):
        self.flag_count += new_flagcount


    def cross_reveal(self, button):
        """ A Effect. Clears all the buttons in the same row and column as :arg: button """
        x,y = button.get_coords()

        # Create a generator that gets button_rows from self.grid
        button_row = (button_row for button_row in self.grid)

        # Reveal all the buttons in the same column as :arg: button
        for button_row in self.grid:
            for button in button_row:
                if button.y_cord != y:
                    continue
                else:
                    button.isGold = False
                    button.effect_click()
        print('CROSS-REVEAL')

        # Reveal all the buttons in the same row as :arg: button
        for button in self.grid[x]:
            button.isGold = False
            button.effect_click()

    def box_effect(self, button):
        coords = button.get_coords()
        for x,y in self.get_surround_coords(coords):
            button = self.grid[x][y]
            button.isGold = False
            button.effect_click()
        print('BOX-REVEAL')

    def button_generator(self):
        for row in self.grid:
            for button in row:
                yield button

    def same_num_effect(self, button):
        value = button.Value
        for button in self.button_generator():
            if button.Value != value:
                continue
            else:
                button.isGold = False
                button.effect_click()
        button.isGold = False

        print('SAME-NUM-REVEAL')

    def generate_effect(self, button, effect_num):
        if effect_num == 1:
            self.cross_reveal(button)
        elif effect_num == 2:
            self.box_effect(button)
        else:
            self.same_num_effect(button)

    def show_all_bombs(self):
        for bomb_loc in self.bomb_location_list:
            x,y = bomb_loc
            self.grid[x][y].reveal()

    def effect_flood_fill(self, button):
        if button.Value != 0:
            return
        else:
            self.flood_fill_v2(button)




