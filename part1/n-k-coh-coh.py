import sys
import numpy as np
import copy
import math

# Global Variable h for height of tree
h = 6

# Global Variable terminals for the terminal nodes for backtracking
terminals = []
k = 0

# Assumptions:
# 1 - White
# 2 - Black
# 
# DOCUMENTATION BEGINS
# 
# The problem was formulated in the following way:
# 
# > State Space: All possible moves that involve placing a marble in an empty space on the board with one marble 
# 	occupying exactly one place.
# 
# > Initial State: Any legit move that satisfies that each marble occupy one space and should not be a terminal state.
# 
# > Successor function: All possible successors from a given initial state where each successor would 
# 	have an empty tile filled with a marble of a particular color (depending on the player). Minimax prunes successors based
# 	on their evaluation score so some successors would not be generated/explored.
# 
# > Valid State: A Valid State is a state wherein there are exactly even numbers if it is the 1st Players turn & odd if is the 
# 	2nd players turn. There can be only one marble in one space and losing/winning is a legit state but the next state should/would not
# 	be played.
# 	
# > Heuristics: We evaluate each state by applying the following rules.
# 	- If it is Max:
# 	 * We find contigouos runs of w or b (depending upon turn) and raise 10 to the power of n. So if you find 'www' in any row/column/diagonal
# 	 	we would score it 1000.
# 	- If it is Min:
# 	 * We do the same but negate the cost value.
# 
# > The search algorithm works by finding whether the max or the min player is playing and recursing from the bottom of 
# 	the tree to find the best possible next move by either maximizing or minimizing the score depending on the Player.
# 
# > There were a few problems faced such as recursion depth and time trade off. You either had to chose from the two, we have come halfway.
# 	The other idea was to implement the tree iteratively to a depth until the time given as an input was left.
# 	This did not give the next best move like recursing through the whole tree gave.
# 
# DOCUMENTATION ENDS

class State(object):
	"""
	Representation of a certain state.
	"""
	height = 0
	parent = None
	evaluation_value = 0

	def __init__ (self, board, minormax):
		"""
		Basic Constructor
		"""
		self.board = board
		self.minormax = minormax

	def evaluation(self, playing_for, playa):
		"""
		Evaluation function for the current state.
		"""
		cost = 0

		# Row Wise Scanning
		for each_row in range(len(self.board)):
			current_row = self.board[each_row]
			cost += self.row_cost(current_row, playing_for)

		for each_column in range(len(self.board)):
			current_col = self.board[:,each_column]
			cost += self.row_cost(current_col, playing_for)

		# To help myself with extracting all diagonals from top-left corner to bottom right corner
		# http://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python
		
		# Making a deep copy to make sure shape function does not mess around with the original board
		copy_board = copy.deepcopy(self.board)

		diags = [copy_board[::-1,:].diagonal(i) for i in range(-copy_board.shape[0]+1,copy_board.shape[1])]
		diags.extend(copy_board.diagonal(i) for i in range(copy_board.shape[1]-1,-copy_board.shape[0],-1))
		for each_diagonal in range(len(diags)):
			cost += self.row_cost(copy_board.diagonal(each_diagonal), playing_for)

		if (playa == "max"):
			return cost
		
		return -cost

	def row_cost(self, current_row, playing_for):
		"""
		Computes cost of a row, column or diagonal
		"""
		element_iterator = 0
		cost = 0
		while element_iterator < (len(current_row) - 1):
			# Find continous runs of the players playing for
			if (current_row[element_iterator] == playing_for and current_row[element_iterator + 1] == playing_for):
				power = 1
				penalty = 1

				# While next element and so on is the same, keep penalising it more and more.
				while (element_iterator < (len(current_row) - 1) and (current_row[element_iterator] == current_row[element_iterator + 1])):
					penalty = 10**power
					power += 1
					element_iterator += 1
				cost += penalty
			# Else if simply add single penalty to cost
			elif current_row[element_iterator] == playing_for:
				cost += 1
				element_iterator += 1

			# Else just iterate through
			else: element_iterator += 1

		return cost

	def game_over(self):
		"""
		Is the game over yet? Is the board full?
		"""
		if (np.count_nonzero(self.board) == ((len(self.board) * len(self.board)))):
			#print(self.board)
			return True
		return False

	def get_successors(self, playing_for):
		"""
		Get the successor from the current state based on player.
		"""
		successor_list = []
		for row in range(len(self.board)):
			for column in range(len(self.board[row])):
				if (self.board[row][column] == 0):
					newboard = copy.deepcopy(self.board)
					newboard[row][column] = playing_for
					newstate = State(newboard, "min")
					successor_list.append(newstate)
		return successor_list

def convert_to_matrix(board_state_string, n):
	"""
	Converting the board to np matrix from input string
	"""
	index = 0
	board_state = np.zeros(shape=(n,n))
	
	# For each row and column convert
	for row in range(len(board_state)):
		for column in range(len(board_state[row])):
			if (board_state_string[index] == '.'):
				board_state[row][column] = 0
			elif (board_state_string[index] == 'w'):
				board_state[row][column] = 1
			elif (board_state_string[index] == 'b'):
				board_state[row][column] = 2
			else: 
				sys.exit("Excuse Me?!")
			index += 1
	return board_state

def get_input():
	"""
	Get Input and return the matrix
	"""
	n, k, board_state_string, time = sys.argv[1:]
	return int(n), int(k), board_state_string, convert_to_matrix(board_state_string, int(n)), int(time)

def build_tree(current_state, height, playing_for):
	"""
	Build the tree recursively.
	Old way to build tree, minimax is the new way.
	"""
	if (current_state.game_over()):
		current_state.evaluation_val = current_state.evaluation(playing_for)
		terminals.append(current_state)
		return current_state, current_state.evaluation_val

	successors = current_state.get_successors(playing_for)

	if (playing_for == 2):
		playing_for = 1
	else: playing_for = 2

	for each_successor in successors:
		each_successor.parent = current_state
		build_tree(each_successor, height+1, playing_for)

def minimax(current_state, height, playing_for, playa, alpha, beta):
	"""
	Build Max Tree Recursively.
	https://www.ntu.edu.sg/home/ehchua/programming/java/JavaGame_TicTacToe_AI.html
	"""
	score = 0
	# If the current state is game over, which means board is full exit
	if (current_state.game_over() or height == h):
		score = current_state.evaluation(playing_for, playa)
		current_state.evaluation_value = score
		terminals.append(current_state)
		return score

	# Get all successors
	successors = current_state.get_successors(playing_for)

	# Optimising the move for black or white
	if (playing_for == 2):
		playing_for = 1
	else: playing_for = 2

	for each_successor in successors:

		each_successor.parent = current_state
		# If Player is Max, maximise alpha
		if (playa == "max"):
			score = minimax(each_successor, height + 1, playing_for, "min", alpha, beta)
			if (score > alpha):
				alpha = score

		# Else minimise stuff
		else:
			score = minimax(each_successor, height + 1, playing_for, "max", alpha, beta)
			if (score < beta):
				beta = score

		if alpha >= beta: break

	if (playa == "max"):
		return alpha
	return beta

def trackback(terminals):
	"""
	Trackback to the the next best move that exist
	"""
	min_val = sys.maxsize
	min_state = None
	prev = None

	for each_item in terminals:
		#print(each_item.evaluation_value)
		if (math.fabs(each_item.evaluation_value) < min_val):
			min_val = math.fabs(each_item.evaluation_value)
			min_state = each_item

	while (min_state.parent != None):
		prev = min_state
		min_state = min_state.parent

	return prev

def convert_to_output(state):
	"""
	Converting the matrix back to string format.
	"""
	output = ""
	for each_row in range(len(state.board)):
		for each_column in range(len(state.board[each_row])):
			if (state.board[each_row][each_column] == 0): output += "."
			elif (state.board[each_row][each_column] == 1): output += "w"
			elif (state.board[each_row][each_column] == 2): output += "b"

	return output

def main():
	"""
	This is where all the action happens!
	"""
	n, k, board_state_string, board_state, time = get_input()
	global h

	# Updating Height
	if (n > 8): h = 2
	elif (n > 4 and n <= 8):
		h = 5
	else: h = 10
	
	# Get Details about the board
	start = State(board_state,"max")

	# If the player is white
	if (((np.count_nonzero(start.board == 1) + np.count_nonzero(start.board == 2)) % 2) == 0):
		#build_tree(start, 0, 1)
		minimax(start, 0, 1, "max", -sys.maxsize-1, sys.maxsize)


	# If the player is Black
	else:
		#build_tree(start, 0, 2)
		minimax(start, 0, 2, "max", -sys.maxsize-1, sys.maxsize)

	print(start.board)
	print(convert_to_output(trackback(terminals)))

if __name__ == "__main__":
	main()