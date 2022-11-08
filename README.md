*Othello Game*
=======

An implementation of the 2-player board game Othello using Python Tkinter

## Description ##

The goal of this project was to create the Othello board game using artificial
intelligence (AI). The board is solved using Minimax and Alpha-Beta Pruning
algorithm with a heuristic function that calculates the score, which is the difference
of the coins of the Maximizing and the Minimizing player.

## Dependencies ##
* Python 3.0 and above
* pillow (install using pip)
* tkinter (comes default with python)

## How to Run ##
Once requirements are met, simply run ``` python run.py```

## How to Play ##
The game has 3 player types: player vs player, computer vs player, and
player vs computer. For player vs player, there is no AI agent present.
For computer vs player, computer will be the first to play as black while
the player will play as white. For player vs computer, the player will first
play as black and then the computer as white. You can change the player type
by clicking the 'change play' button. Click 'reset' button to restart the game.
To play, simply click on the suggested valid tiles and wait for your turn.