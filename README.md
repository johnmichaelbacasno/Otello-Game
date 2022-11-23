*Othello Game*
=======

An implementation of the 2-player board game Othello using Python Tkinter

## Description ##

The goal of this project was to create the Othello board game using artificial
intelligence (AI). The board is solved using Minimax and Alpha-Beta Pruning
algorithm with a Static Weights as part of the heuristic function.

## Dependencies ##
* Python 3.0 and above
* pillow (install using pip)
* tkinter (comes default with python)

## How to Run ##
Once requirements are met, simply run ``` python run.py```

## How to Play ##
The game has 3 player types: player vs player, computer vs player, and
player vs computer. For player vs player, there is no AI agent present.
For computer vs player, the computer will be the first to play as black while
the player will play as white. For player vs computer, the player will first
play as black and then the computer as white. You can change the player type
by clicking the 'change play' button. Click 'reset' button to restart the game.
To play, simply click on the suggested valid tiles and wait for your turn.

## Reference ##
Sannidhanam V. & Annamalai M. (n. d.). [An Analysis of Heuristics in Othello](https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSsIA/Final_Paper.pdf?fbclid=IwAR2ut8zr9hxj9p6WKkzkNsG_KopZSXVwPX5YJhfXccKkjcGhHDZdCY11-C4).