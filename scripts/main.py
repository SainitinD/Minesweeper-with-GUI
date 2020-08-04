from mine_sweeper import Mine_Sweeper
import tkinter as tk
from Images import gather_images

""" The main file that runs the game. """
if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(width=False, height=False)
    root.title('MineSweeper by u/litteralyonfire')
    root.iconbitmap('icon.ico')

    img = gather_images()
    mine = Mine_Sweeper(root, img, game_mode='hard', bd=4)

    mine.mainloop()