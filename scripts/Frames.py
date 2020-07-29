import tkinter as tk
from Images import get_smile_img, get_flag_img
import threading
import time

class Bottom_frame:
    """ The bottom frame of the mine sweeper game """
    def __init__(self, root, class_ref):
        self.frame = tk.LabelFrame(root, bd=7)

        self.flag_count = class_ref.flag_count
        self.flag_img = get_flag_img()

        self.flag_label = tk.Label(self.frame, image=self.flag_img, text=': {}'.format(self.flag_count), compound='left', relief='ridge')
        self.flag_label.pack(side=tk.LEFT, padx=18, ipadx=8, ipady=1, pady=1)

        self.smile_img = get_smile_img((30,22))
        self.smile_button = tk.Button(self.frame, image=self.smile_img, bd=3, relief='raised', command=self.smile_click)
        self.smile_button.pack(side=tk.LEFT, padx=18, ipady=1, pady=1)

        self.solve_button = tk.Button(self.frame, text='SOLVE', bd=3, relief='raised', command=class_ref.solve_game)
        self.solve_button.pack(side=tk.LEFT, padx=18, ipadx=10, ipady=1, pady=1)

        

        #self.retry_button = tk.Button(self.frame,
        #                              text='RETRY',
        #                              bd=3,
        #                              relief='raised',
        #                              command=class_ref.reset_game
        #)
        
        #self.retry_button.pack(side=tk.RIGHT,
        #                   padx=10,
        #                   ipadx=10,
        #                   ipady=1,
        #                   pady=3
        #)


        self.frame.grid(row=class_ref.grid_size[0]+1,
                        ipady=0,
                        columnspan=class_ref.grid_size[1],
                        ipadx=class_ref.grid_size[0]*0
        )

        self.class_ref = class_ref

    def smile_click(self):
        """ Literally updates the game """
        self.class_ref.reset_game()
    
    def flag_clicked(self):
        """ Updates the flag-remaining counter """
        self.flag_label.configure(text=': {}'.format(self.class_ref.flag_count))

class Top_frame:
    """ The top frame of the mine sweeper game"""
    def __init__(self, root, class_ref):
        frame = tk.LabelFrame(root, bd=7)
        frame.grid(row=0,
                        ipady=0,
                        columnspan=class_ref.grid_size[1],
                        ipadx=class_ref.grid_size[1]*9
        )

        self.mine_indicator = tk.Label(frame, )
        self.flag_remaining = class_ref.flag_count
        self.score_count = tk.Label(frame, text='FLAGS: {}'.format(self.flag_remaining), font='TIMES 10', relief='sunken', fg='#333333' )
        self.score_count.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=1, pady=3)#.grid(row=0, column=0, padx=10, ipadx=10, ipady=1, pady=3)

        #self.timer = 996
       # self.time_label = tk.Label(frame, text='{}'.format(self.timer), font='10', relief='sunken')
        #self.time_label.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=1, pady=3)

        #self.t = 'HighScore: '
        #self.label = tk.Label(frame, text=self.t, font='Times 15', relief='sunken')
        #self.label.grid(row=0, column=0, padx=10, ipadx=10, ipady=1, pady=3)

        #self.smile_img = Image.open('assets/smile.png')
        self.smile_img = get_smile_img()#ImageTk.PhotoImage(self.smile_img.resize((30,25), Image.ANTIALIAS))

        self.class_ref = class_ref
        #self.smile_img = get_smile_img()
        self.smile_button = tk.Button(frame, image=self.smile_img, command=self.smile_click)
        self.smile_button.pack(side=tk.RIGHT, padx=10, ipady=1, pady=3)#.grid(row=0, column=1, padx=10, ipady=1, pady=3)

        time_thread = threading.Thread(target=self.start_timer)
        time_thread.start()

    def smile_click(self):
        """ Literally updates the game """
        self.class_ref.reset_game()

    def flag_clicked(self):
        """ Updates the flag-remaining counter """
        self.score_count.configure(text='FLAGS: {}'.format(self.class_ref.flag_count))

    def start_timer(self):
        i = self.timer
        while i < 999: 
            self.timer += 1
            #print('HELLO')
            self.update_timer()
            i += 1
            time.sleep(1)

    def update_timer(self):
        self.time_label.configure(text='{}'.format(self.timer))
