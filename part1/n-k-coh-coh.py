import sys
import numpy as np
import copy

#Global Variable h for height of treee
h = 100

class State(object):
	height = 0
	
	def __init__ (self, board, minormax):
		self.board = board
		self.minormax = minormax

	def evaluation():
		return len(self.board)

	def is_goal():
		return True

	def game_over(self):

		if (np.count_nonzero(self.board) == ((len(self.board) * len(self.board)))):
			print(self.board)
			return True
		return False

	def get_successors(self, playing_for):

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

	if (current_state.game_over()):
		leaves.append(current_state)
		return leaves, current_state

	successors = current_state.get_successors(playing_for)

	if (playing_for == 2):
		playing_for = 1
	else: playing_for = 2

	for each_successor in successors:
			build_tree(each_successor, height+1, playing_for, leaves)

def main():

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