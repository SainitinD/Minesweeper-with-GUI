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
                 'hard': (20,24),
                 'expert':(24,35)}

    bomb_max = {'easy': 10, 'medium': 40, 'hard': 99, 'expert':159}

    box_effect_dict = {'easy': 2, 'medium':3, 'hard':4, 'expert':4}

    cross_reveal_dict = {'easy': 1, 'medium': 1, 'hard':3, 'expert':3}

    def __init__(self, root, image_dict, game_mode='easy', *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        # The main root.
        self.root = root

        # The game mode
        self.game_mode = game_mode

        # Get the grid size based on the chosen game_mode
        self.grid_size = self.game_size[game_mode]

        # Get the maximum no. of bombs for the specified game_mode
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

        self.effect_count = round((self.num_of_bombs * 0.05) + 2.5)

        self.effect_location_list = set()

        self.isFirst = False

        # Assemble the game
        self.main()


    def main(self):
        """ Initialize the game """
        self.create_grid()
        self.create_bombs()
        self.update_button_scores()
        #self.create_magic_nums(self.effect_count)
        #self.show_all_bombs()
        #self.get_game_description()

    
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
        num_of_bombs = self.num_of_bombs - len(self.bomb_location_list)
        
        if num_of_bombs < 1:
            return

        for i in range(num_of_bombs):
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
            self.effect_location_list.add((x,y))
            button = self.grid[x][y]
            button.isMagic = True
            #print(x,y)


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

    def zero_button_scores(self):
        """ Zeros all the button scores. """
        for button in self.button_generator():
            if button.Value != -1:
                button.Value = 0
            else:
                continue

    def update_button_scores(self):
        """ For each bomb_location from bomb_location_list, this function increases the surrounding (1-tile) button's value.
            FYI: The higher the value a tile shows, the greater the ammount of bombs surrounding it.
        """
        for bomb_location in self.bomb_location_list:
            for x,y in self.get_surround_coords(bomb_location):
                try:
                    button = self.grid[x][y]
                    val = button.Value
                    if val != -1:
                        self.grid[x][y].Value += 1
                except:
                    continue


    def get_surround_coords(self, coord, sub=-1, add=2):
        """ Creates a generator containting the indices of tiles that surround the :arg: coord.
            Each iteration it sends a coordinate of a tile around the initial coord. 

            It is also intended to be used by the :meth: box-effect to reveal numbers surrounding
            the magic number. 
        
        Args:
            coord (tuple): A tuple containing x,y coords of the function.
            sub (int): A number that lets us determine how many rows to search
            add (int): A number that lets us determine how many columns to search
        Returns:
            coord_list (list of tuples): A list of tuples containing indices of surrounding tiles. 
        """

        x_cord, y_cord = coord
        #upd_coord = set()
        #upd_coord = {yieldfor x in range(x_cord-1, x_cord+2) for y in range(y_cord-1, y_cord+2)}
        for x in range(x_cord+sub, x_cord+add):
            for y in range(y_cord+sub, y_cord+add):
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
                    if new_button.isMagic == False:
                        new_button.left_click()
                    else:
                        new_button.make_button_magic()    
                elif val != -1:
                    if new_button.isMagic == False:
                        new_button.left_click()
                    else:
                        new_button.make_button_magic()
            except:
                continue


    def reset_game(self):
        """ This function is called whenever the smiley face is clicked. Basically resets the game. """
        self._reset_values()
        self.main()
        self.isFirst = False


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
        """ A getter method for getting the score attribute """
        return self.score


    def update_score(self, new_score):
        """ A update method for updating the score attribute """
        self.score -= new_score


    def get_flagcount(self):
        """ A getter method for getting the flag_count attribute """
        return self.flag_count


    def update_flagcount(self, new_flagcount):
        """ A update method for updating the flag_count attribute """
        self.flag_count += new_flagcount


    def cross_reveal(self, button):
        """ This method applies the cross-reveal effect.
            Clears all the buttons in the same row and column as :arg: button.

        Args:
            button (Button obj): A Button obj reference chosen as the magic number. 
        """

        # Get the magic button's coordinates
        x,y = button.get_coords()

        # # Create a generator that gets button_rows from self.grid
        # button_row = (button_row for button_row in self.grid)

        # Reveal all the buttons in the same column as :arg: button
        for button_row in self.grid:
            for button in button_row:
                if button.y_cord != y:
                    continue
                else:
                    button.isMagic = False
                    button.effect_click()
        print('CROSS-REVEAL')

        # Reveal all the buttons in the same row as :arg: button
        for button in self.grid[x]:
            button.isMagic = False
            button.effect_click()


    def box_effect(self, button):
        """ The method that creates the box reveal effect in the minesweeper game.

            When this method gets called, the method randomly reveals a 3x3 or 4x4 or 5x5
            sub-grid of buttons around the initial :arg: button.

        Args:
            button (Button): A reference of a button object containing the magic attribute. 

        """
        # Get the max_lim of box_reveal size based on game_mode. 
        max_lim = self.box_effect_dict[self.game_mode]

        # Randomly choose a box size
        random_effect = random.randint(2,max_lim)

        # Create the sub and add parameters for the :meth: get_surround_coords
        sub = -(random_effect) + 1
        add = random_effect

        coords = button.get_coords()

        # Perform the box reveal. 
        for x,y in self.get_surround_coords(coords, sub, add):
            button = self.grid[x][y]
            button.isMagic = False
            button.effect_click()
        print('BOX-REVEAL')


    def button_generator(self):
        """ A generator function that returns each button from the grid. 
            Created for optimization.
            
            Used by the :meth: reset_game to efficiently reset the game. 
        """
        for row in self.grid:
            for button in row:
                yield button


    def same_num_effect(self, button):
        """ Iterate through each button on the grid and if the Value attribute of that button is equal to the Value of 
            the initial :arg: button, then reveal that button. 
        """
        value = button.Value
        for button in self.button_generator():
            if button.Value != value:
                continue
            else:
                button.isMagic = False
                button.effect_click()
        button.isMagic = False
        # coords = button.get_coords()
        # max_lim = round(self.grid_size[0] * 0.4)
        # sub = -(max_lim) + 1
        # add = max_lim
        # for x,y in self.get_surround_coords(coords, sub=sub, add=add):
        #     if button.Value != value:
        #         continue
        #     else:
        #         button = self.grid[x][y]
        #         button.isMagic = False
        #         button.effect_click()
        # button.isMagic = False

        print('SAME-NUM-REVEAL')


    def generate_effect(self, button, effect_num):
        """ The main method that gets called each time a magic number gets clicked.
            This method randomly selects a effect and shows it on screen. 
        """
        if button.Value >= 4:
            self.same_num_effect(button)
        else:
            if 0 < effect_num < 7:
                # self.same_num_effect(button)
                self.box_effect(button)
            else:
                # self.same_num_effect(button)
                self.cross_reveal(button)
        # else:
        #     self.same_num_effect(button)


    def show_all_bombs(self):
        """ Used for dev testing. It just reveals all the bomb locations """
        for bomb_loc in self.bomb_location_list:
            x,y = bomb_loc
            self.grid[x][y].reveal()


    def effect_flood_fill(self, button):
        """ Used when a magic button is clicked."""
        if button.Value != 0:
            return
        else:
            self.flood_fill_v2(button)

    def clear_surrounding_bombs(self, button):
        """ Used for the first click to clear some space for the player to start the game """
        coords = button.get_coords()
        #print(coords)
        for x,y in self.get_surround_coords(coords):
            button = self.grid[x][y]
            print(x,y)
            if button.Value == 0:
                continue
            else:
                if button.Value == -1:
                    button.Value = 0
                    self.bomb_location_list.remove(button.get_coords())
                    self.create_bombs()

        self.zero_button_scores()
        self.update_button_scores()
        self.create_magic_nums(self.effect_count)
        self.get_game_description()


    def get_game_description(self):
        """ Used for dev testing. Gives out a printed game description"""
        print('GAME MODE: {} \nTotal Bomb Count: {} \nTotal Magic Numbers: {} \nTotal Flag Count: {} \nInitial Score: {}'.format(self.game_mode, len(self.bomb_location_list), len(self.effect_location_list), len(self.bomb_location_list), self.score))