# PLAYING X&0 - TIC TAC TOE against gravity!

#Problem:
 - N - K - Coh Coh - It is the opposite of Tic Tac Toe, where you avoid building series of same shapes, bang opposite of tic tac toe
 - Automate the game to provide the next best move - using Minimax Algorithm!

##The problem was formulated in the following way:  
 - State Space: All possible moves that involve placing a marble in an empty space on the board  
 - State Space: All possible moves that involve placing a marble in an empty space on the board with one marble occupying exactly one place.  
 - Initial State: Any legit move that satisfies that each marble occupy one space and should not be a terminal state.  
 - Successor function: All possible successors from a given initial state where each successor would have an empty tile filled with a marble of a particular color (depending on the player).  
 - Minimax prunes successors based on their evaluation score so some successors would not be generated/explored. 

##Heuristics:
 We evaluate each state by applying the following rules. 
 - If it is Max: 
 	- We find contiguous runs of w or b (depending upon turn) and raise 10 to the power of n. 
So if you find 'www' in any row/column/diagonal. 
we would score it 1000. 
- If it is Min:  
	- We do the same but negate the cost value.
- The search algorithm works by finding whether the max or the min player is playing and 
recursing from the bottom of the tree to find the best possible next move by either maximizing 
or minimizing the score depending on the Player. 
  
##Misc
There were a few problems faced such as recursion depth and time trade off. You either had to chose from the two, we have come halfway. 
The other idea was to implement the tree iteratively to a depth until the time given as an input 
was left.