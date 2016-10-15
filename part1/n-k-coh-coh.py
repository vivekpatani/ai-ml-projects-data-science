import sys
import numpy as np
import copy

#Global Variable h for height of tree
h = 100

# Assumptions:
# 1 - White
# 2 - Black

class State(object):
	height = 0
	parent = None

	def __init__ (self, board, minormax):
		self.board = board
		self.minormax = minormax

	def evaluation(self, playing_for):
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
		for each_diagonal in range(copy_board.shape[1] - 1, -copy_board.shape[0], -1):
			cost += self.row_cost(copy_board.diagonal(each_diagonal), playing_for)

		return cost

	def row_cost(self, current_row, playing_for):
		
		element_iterator = 0
		cost = 0
		while element_iterator < (len(current_row) - 1):
			# Find continous runs of the players playing for
			if (current_row[element_iterator] == playing_for and current_row[element_iterator + 1] == playing_for):
				power = 1
				penalty = 1
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
			print(self.board)
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

def build_tree(current_state, height, playing_for, leaves):
	"""
	Build the tree recursively.
	"""
	if (current_state.game_over()):
		leaves.append(current_state)
		print(current_state.evaluation(playing_for))
		return leaves, current_state

	successors = current_state.get_successors(playing_for)

	if (playing_for == 2):
		playing_for = 1
	else: playing_for = 2

	for each_successor in successors:
		each_successor.parent = current_state
		build_tree(each_successor, height+1, playing_for, leaves)

def main():
	"""

	"""
	# Get Details about the board
	n, k, board_state_string, board_state, time = get_input()
	start = State(board_state,"max")

	# If the player is white
	if (((np.count_nonzero(start.board == 1) + np.count_nonzero(start.board == 2)) % 2) == 0):
		leaves = build_tree(start, 0, 1, [])
		print(leaves)

	# If the player is Black
	else: print("Black")

if __name__ == "__main__":
	main()