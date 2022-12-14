import os
import tkinter as tk
import time
from tkinter import ttk
from PIL import Image, ImageTk
from threading import Thread

from src.config import *
from src.utils import *

class Othello(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Othello Game')
        self.geometry('750x750')
        self.resizable(False, False)
        self.iconbitmap('src/assets/images/app.ico')
        self.protocol('WM_DELETE_WINDOW', lambda: os._exit(0))
        
        self.container = tk.Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.show_frame(OthelloPage, **BASIC_FRAME_PROPERTIES)
    
    def show_frame(self, page, *args, **kwargs):
        frame = page(self.container, self, *args, **kwargs)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.tkraise()

class OthelloPage(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller
        
        self.tile_images = [ImageTk.PhotoImage(Image.open(f'src/assets/images/tile_{n}.png')) for n in range(7)]
        self.board = [x[:] for x in [[None] * 8] * 8]
        self.current_board_state = []

        self.is_moving = False
        self.AI_player = 0
        
        self.display_widgets()
        
        self.reset_board()
    
    def display_widgets(self):
        # Title section
        self.frame_title = tk.Frame(self, **BASIC_FRAME_PROPERTIES)
        self.frame_title.pack(pady=25)
        
        self.label_heading = tk.Label(self.frame_title, text='Othello Game', **HEADING_LABEL_PROPERTIES)
        self.label_heading.pack()
        
        self.label_subheading = tk.Label(self.frame_title, text=f'player vs player', **SUBHEADING_LABEL_PROPERTIES)
        self.label_subheading.pack()
        
        # Puzzle section
        self.frame_puzzle = tk.Frame(self, **BASIC_FRAME_PROPERTIES)
        self.frame_puzzle.pack(padx=10, pady=10)
        
        #Button section
        self.frame_buttons = tk.Frame(self, **BASIC_FRAME_PROPERTIES)
        self.frame_buttons.pack(pady=20)
        
        self.button_reset = tk.Button(self.frame_buttons, text='reset game', command=lambda: self.reset_board(), **SECONDARY_BUTTON_PROPERTIES)
        self.button_reset.grid(row=0, column=1, padx=10, pady=10)
        
        self.button_reset = tk.Button(self.frame_buttons, text='change play', command=lambda: self.change_play(), **TERTIARY_BUTTON_PROPERTIES)
        self.button_reset.grid(row=0, column=2, padx=10, pady=10)
        
        self.label_scores = tk.Label(self.frame_puzzle, text=f'P1: 02 | P2: 02', **TEXT_LABEL_PROPERTIES)
        self.label_scores.grid(row=0, column=0, sticky='w', padx=10, pady=5)
        
        self.label_status = tk.Label(self.frame_puzzle, text=f'Playing...', **TEXT_LABEL_PROPERTIES)
        self.label_status.grid(row=0, column=1, sticky='e', padx=10, pady=5)
        
        self.separator = ttk.Separator(self.frame_puzzle, orient='horizontal')
        self.separator.grid(row=1, columnspan=2, sticky='ew', pady=10)
        
        self.frame_board = tk.Frame(self.frame_puzzle, **BASIC_FRAME_PROPERTIES)
        self.frame_board.grid(row=2, columnspan=2)
        
        self.initialize_board()
    
    def change_play(self):
        if not self.is_moving:
            if self.AI_player == 0:
                self.AI_player = 1
                self.label_subheading.configure(text=f'computer vs player')
                self.reset_board()
            elif self.AI_player == 1:
                self.AI_player = 2
                self.label_subheading.configure(text=f'player vs computer')
                self.reset_board()
            elif self.AI_player == 2:
                self.AI_player = 0
                self.label_subheading.configure(text=f'player vs player')
                self.reset_board()
            '''
            elif self.AI == 2:
                self.AI = 3
                self.label_subheading.configure(text=f'computer vs computer')
                self.reset_board()
            elif self.AI == 3:
                self.AI = 0
                self.label_subheading.configure(text=f'player vs player')
                self.reset_board()
            '''
    
    def initialize_board(self):
         for i in range(8):
            for j in range(8):
                self.board[i][j] = tk.Button(self.frame_board, **TILE_BUTTON_PROPERTIES)
                self.board[i][j].grid(row=i, column=j, padx=2, pady=2)
    
    def populate_board(self, state):
        for i in range(8):
            for j in range(8):
                self.board[i][j].configure(
                    text=state[i][j],
                    image=self.tile_images[int(state[i][j])],
                    state='normal',
                    command=lambda tile_x=i, tile_y=j: self.process_click(tile_x, tile_y)
                )
        
        self.current_board_state = state
        self.update_scores()
    
    def update_board(self, state):
        self.populate_board(state)
    
    def reset_board(self):
        self.stop()
        if not self.is_moving:
            state =  [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 2, 1, 0, 0, 0],
                [0, 0, 0, 1, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
            
            '''
            # no move state
            state =  [
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 0],
                [2, 2, 2, 2, 2, 2, 0, 0],
                [2, 2, 2, 2, 2, 2, 0, 0],
                [2, 2, 2, 2, 2, 2, 2, 0],
                [2, 2, 2, 2, 2, 1, 2, 2],
            ]
            '''
            
            self.is_stopped = True
            self.is_done = False
            #self.P1 = 1
            #self.P2 = 2
            self.P1_score = 0
            self.P2_score = 0
            
            self.populate_board(state)
            self.current_player = 2
            
            '''
            if self.AI_player == 3:
                Thread(target=self.turn_by_turn_AI).start()
            else: self.game_conditions()
            '''
            
            self.game_conditions()
    
    def stop(self):
        if self.is_moving and not self.is_stopped:
            self.is_stopped = True
        self.is_done = False
    
    def suggest_moves(self, stone):
        moves = Board.get_valid_moves(self.current_board_state, stone)
        if moves:
            for move in moves:
                x, y = move.coords
                self.board[x][y].configure(image=self.tile_images[stone + 2])
    
    def process_click(self, tile_x, tile_y):
        player = self.current_player
        
        if not self.is_done and not self.is_moving and Board.is_valid(self.current_board_state, tile_x, tile_y, player):
            state =  Board.transform_board(self.current_board_state, (tile_x, tile_y), player)
            
            self.update_board(state)
            
            self.board[tile_x][tile_y].configure(image=self.tile_images[player + 4]) # mark move
            
            self.game_conditions()
    
    def animate_AI(self, player):
        self.animation_thread = Thread(target=self.move_AI, args=(player,))
        self.animation_thread.start()
    
    def move_AI(self, player):
        self.is_moving = True
        
        move = Board.best_move(self.current_board_state, player, 5).coords
        state =  Board.transform_board(self.current_board_state, move, player)
        time.sleep(0.5)
        self.update_board(state)
        
        if move: self.board[move[0]][move[1]].configure(image=self.tile_images[player + 4]) # mark move
        
        self.is_moving = False
        
        self.game_conditions()
    
    '''
    def turn_by_turn_AI(self):
        self.is_stopped = False
        player = 1
        while True:
            if self.is_stopped:
                break
            else:
                self.assign_player(player)
                
                self.is_moving = True
                move = Board.move(self.current_board_state, player, 5)
                state =  Board.transform_board(self.current_board_state, move, player)
                time.sleep(0.5)
                self.update_board(state)
                
                if move: self.board[move[0]][move[1]].configure(image=self.tile_images[player+4]) # mark move
                
                p1_has_no_move = Board.has_no_move(self.current_board_state, 1)
                p2_has_no_move = Board.has_no_move(self.current_board_state, 2)
                
                if (self.P1_score + self.P2_score == 64) or (p1_has_no_move and p2_has_no_move):
                    if self.P1_score < self.P2_score:
                        self.update_status('P2 wins')
                    elif self.P1_score > self.P2_score:
                        self.update_status('P1 wins')
                    else:
                        self.update_status('draw')
                    self.is_done = True
                    time.sleep(2.5)
                    break
                else:
                    if player == 1:
                        player = 2
                    elif player == 2:
                        player = 1
        
        #time.sleep(1)
        self.is_moving = False
        self.reset_board()
    '''
    
    def game_conditions(self):
        p1_has_no_move = Board.has_no_move(self.current_board_state, 1)
        p2_has_no_move = Board.has_no_move(self.current_board_state, 2)
        
        if (self.P1_score + self.P2_score == 64) or (p1_has_no_move and p2_has_no_move):
            if self.P1_score < self.P2_score:
                self.update_status('P2 wins')
            elif self.P1_score > self.P2_score:
                self.update_status('P1 wins')
            else:
                self.update_status('draw')
            self.is_done = True
        else:
            if self.current_player == 1:
                if p2_has_no_move:
                    self.assign_player(1)
                else:
                    self.change_player()
            elif self.current_player == 2:
                if p1_has_no_move:
                   self.assign_player(2)
                else:
                   self.change_player()
    
    def change_player(self):
        if self.current_player == 1:
            self.assign_player(2)
            if self.AI_player == 2:
                self.animate_AI(2)
        
        elif self.current_player == 2:
            self.assign_player(1)
            if self.AI_player == 1:
                self.animate_AI(1)
    
    def assign_player(self, player):
        self.suggest_moves(player)
        self.update_status(f'P{player}\'s turn')
        self.current_player = player
    
    def update_scores(self):
        self.P1_score, self.P2_score = Board.player_scores(self.current_board_state, 1, 2)
        self.label_scores.configure(text=f'P1: {self.P1_score:02} | P2: {self.P2_score:02}')
    
    def update_status(self, status):
        self.label_status.configure(text=status)
