# CS-171 Checkers Project
This Checkers AI should be able to solve a Checkers game, which is provided.

## Checkers World Game Mechanics 
### Environment
This shell follows the American/British ruleset for Checkers. Found on https://en.wikipedia.org/wiki/English_draughts. The rules are similar except the Checkers board in this shell can have a variable size governed by the following rules:
### Board Parameters
	M = number of rows
	N = number of columns
	P = number of rows occupied by pieces in the initial state
	Q = number of unoccupied rows that separate the two sides in the initial state
### Parameter Constraints
	Q > 0
	M = 2P + Q
	N*P is even
### Actuators 
The AI will ONLY know what move your opponent just made. If my AI moves first, it will receive a Move object with col = -1, row = -1
### Sensors
My AI should return a Move object to tell the shell which step you are going to make.

## My AI Implemetation
This AI uses min-max to simulate each move with evaluation of the board. <br/>
This AI uses Monte Carlo tree search (MCTS) to expand the tree and make the choice.

