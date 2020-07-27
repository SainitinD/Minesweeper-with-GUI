import tkinter as tk
import random

class Button(tk.Button):
    def __init__(self, root, x_cord, y_cord, class_ref,  *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.class_ref = class_ref

        self.x_cord = x_cord
        self.y_cord = y_cord

        self.isPressed = False
        self.Value = 0

    def button_click(self):
        if self.isPressed is False:
            self.isPressed = True
            self.configure(relief='groove', state='disabled', bg='#BDBDBD', borderwidth=2)
            if self.Value != 0:
                self.configure(text=str(self.Value))
            else:
                self.class_ref.flood_fill(self)

    def button_side_click(self):
        self.isPressed = True
        self.configure(relief='groove', state='disabled', bg='#BDBDBD', borderwidth=2)
        self.configure(text=str(self.Value))
            

class Mine_Sweeper(tk.Frame):

    game_size = {'easy': (8,10),
                 'medium': (14,18),
                 'hard': (20,24)}

    bomb_max = {'easy': 10, 'medium': 40, 'hard': 99}

    def __init__(self, root, game_mode='easy'):
        super().__init__()

        self.root = root

        # Get the grid size based on the chosen game-mode
        self.grid_size = self.game_size[game_mode]

        # A grid filled with button objects
        self.grid = []

        # Button Width and height defined
        self.width = 2
        self.height = 1

        # Get the maximum no. of bombs for the specified gamemode
        self.num_of_bombs = self.bomb_max[game_mode]

        # Contains a list to contain all the bomb locations
        self.bomb_location_list = []

        # Assemble the game
        self.main()

    def main(self):
        """ Initialize the game """
        self.create_grid()
        self.create_bombs()
        self.update_button_scores()
        #self.show_all_nums()


    def create_grid(self):
        """ Creates the object's grid filled with button objects """
        x_max, y_max = self.grid_size

        cls_ref = self

        for x_cord in range(x_max):
            small_list = []
            for y_cord in range(y_max):
                button = Button(self.root, x_cord, y_cord, class_ref=cls_ref, width=2, height=1)
                button.configure(command = button.button_click)
                button.grid(row=x_cord, column=y_cord)
                small_list.append(button)
            self.grid.append(small_list)

    def create_bombs(self):
        """ Updates the object's grid with bombs """
        
        for i in range(self.num_of_bombs):
            # Update the button's value to indicate bomb
            #print(random_x, random_y)
            x_cord, y_cord = self.get_random_coord()
            self.grid[x_cord][y_cord].Value = -1

            # Add the bomb locations to bomb locations list
            self.bomb_location_list.append((x_cord, y_cord))

    def get_random_coord(self):
        max_idx = self.grid_size[0]-1
        while True:
            random_x = random.randint(0, max_idx)
            random_y = random.randint(0, max_idx)

            coord = (random_x, random_y)

            if coord not in self.bomb_location_list:
                return coord
            else:
                continue

    def update_button_scores(self):
        for bomb_location in self.bomb_location_list:
            print('===================BOMB at location ({}) finished ======================'.format(bomb_location))
            x_cord, y_cord = bomb_location
            for x in range(x_cord-1, x_cord+2):
                for y in range(y_cord-1, y_cord+2):
                    try:
                        assert 0 <= x and x < self.grid_size[0]
                        assert 0 <= y and y < self.grid_size[0]

                        val = self.grid[x][y].Value
                        if val != -1:
                            self.grid[x][y].Value += 1
                            print('Button at ( {}, {} ) had value changed from {} to {}'.format(x, y, val, self.grid[x][y].Value))
                    except:
                        continue


    def flood_fill(self, button):
        x,y = button.x_cord,button.y_cord
        print(x, y)
        for i in range(4):
            if i == 0:
                try:
                    new_x, new_y = x-1, y
                    assert (new_x >= 0 and new_x < self.grid_size[0])
                    new_button = self.grid[new_x][new_y]
                    val = new_button.Value

                    if val == 0:
                        new_button.button_click()
                        #self.flood_fill(new_button)
                    else:
                        new_button.button_side_click()
                except:
                    continue

            if i == 1:
                # Look on the y- side of tile
                try:
                    new_x, new_y = x+1, y
                    assert (0 <= new_x < self.grid_size[0])

                    new_button = self.grid[new_x][new_y]
                    val = new_button.Value

                    if val == 0:
                        new_button.button_click()
                        #self.flood_fill(new_button)
                    else:
                        new_button.button_side_click()
                except:
                    continue

            if i == 2:
                # Look on the x+ side of tile
                try:
                    new_x, new_y = x, y+1
                    assert (0 <= new_y < self.grid_size[1])

                    new_button = self.grid[new_x][new_y]
                    val = new_button.Value

                    if val == 0:
                        new_button.button_click()
                        #self.flood_fill(new_button)
                    else:
                        new_button.button_side_click()
                except:
                    continue

            if i == 3:
                # Look on the x- side of tile
                try:
                    new_x, new_y = x, y-1
                    assert (0 <= new_y < self.grid_size[1])

                    new_button = self.grid[new_x][new_y]
                    val = new_button.Value

                    if val == 0:
                        new_button.button_click()
                        #self.flood_fill(new_button)
                    else:
                        new_button.button_side_click()
                except:
                    continue

    def show_all_nums(self):
        for smal_list in self.grid:
            for button in smal_list:
                if button.Value != 0:
                    button.configure(text=str(button.Value))

 
root = tk.Tk()

mine = Mine_Sweeper(root, game_mode='easy')


mine.mainloop()