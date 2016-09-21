import sys
import os
import copy
import heapq

class State:

	def __init__ (self, puzzle, link):
		self.puzzle = puzzle
		self.link = link

"""
Declaring all the variables needed throughout.
"""
n = 4
goal_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

def get_puzzle():

	"""
	Get puzzle, returns the default state board,
	if no input is found then a default input is provided
	"""

	if (sys.argv[1] and os.path.isfile(sys.argv[1])):
		file = open(sys.argv[1])
	else:
		print("No file found, using default file!")
		file = open('input.txt','r',encoding='utf-8')

	reader = file.read()
	file.close()
	reader = get_list(reader)
	return reader

def get_list(reader, n=4):
	"""
	Returns an integer list of the input
	"""
	lst = reader.split()

	#This step is done to avoid utf-8 encoding
	lst[-1] = lst[-1].replace('\ufeff','')

	matrix = [[0 for x in range(n)] for y in range(n)]
	counter = 0;
	for each_row in range(n):
		for each_column in range(n):
			matrix[each_row][each_column] = int(lst[counter])
			counter += 1;
	return matrix

def calc_hamming (puzzle):

	"""
	Returns hamming distance between goal state and current state.
	Hamming distance is when a tile is not in place the count is incremented by 1
	"""
	total = 0
	for each_row in range(len(goal_state)):
		for each_column in range(len(goal_state[each_row])):
			if (goal_state[each_row][each_column] != puzzle[each_row][each_column]):
				total += 1
	return total

def get_successor (state):

	"""
	Returns a valid successor from the current state
	"""

	row, column = find_empty_space(state)
	successors = []
	successor_object = []
	successor1, cost1 = move_up (state, row, column)
	successors.append(successor1)
	successor11 = State(successor1, cost1)
	successor_object.append(successor11)
	successor2, cost2 = move_down (state, row, column)
	successors.append(successor2)
	successor21 = State(successor2, cost2)
	successor_object.append(successor21)
	successor3, cost3 = move_left (state, row, column)
	successors.append(successor3)
	successor31 = State(successor3, cost3)
	successor_object.append(successor31)
	successor4, cost4 = move_right (state, row, column)
	successors.append(successor4)
	successor41 = State(successor4, cost4)
	successor_object.append(successor41)

	return successors, successor_object

def move_up(state, row, column):

	"""
	Returns the Left movement of the blank tile in the current state
	"""
	newstate = copy.deepcopy(state)
	temp = newstate[row][column]
	if (row == 0):
		newstate[row][column] = newstate[3][column]
		newstate[3][column] = temp

	else:
		newstate[row][column] = newstate[row-1][column]
		newstate[row-1][column] = temp
	return newstate, calc_hamming(newstate)

def move_down(state, row, column):

	"""
	Returns the Left movement of the blank tile in the current state
	"""
	newstate = copy.deepcopy(state)
	temp = newstate[row][column]
	if (row == 3):
		newstate[row][column] = newstate[0][column]
		newstate[0][column] = temp

	else:
		newstate[row][column] = newstate[row+1][column]
		newstate[row+1][column] = temp
	return newstate, calc_hamming(newstate)

def move_left(state, row, column):

	"""
	Returns the Left movement of the blank tile in the current state
	"""
	newstate = copy.deepcopy(state)
	temp = newstate[row][column]
	if (column == 0):
		newstate[row][column] = newstate[row][3]
		newstate[row][3] = temp

	else:
		newstate[row][column] = newstate[row][column-1]
		newstate[row][column-1] = temp
	return newstate, calc_hamming(newstate)

def move_right(state, row, column):

	"""
	Returns the Left movement of the blank tile in the current state
	"""
	newstate = copy.deepcopy(state)
	temp = newstate[row][column]
	if (column == 3):
		newstate[row][column] = newstate[row][0]
		newstate[row][0] = temp

	else:
		newstate[row][column] = newstate[row][column+1]
		newstate[row][column+1] = temp
	return newstate, calc_hamming(newstate)

def find_empty_space (state):

	"""
	Find the empty tile and return its location
	"""
	for each_row in range(len(state)):
		for each_column in range(len(state[each_row])):
			if (state[each_row][each_column] == 0): return each_row,each_column


def main():
	heap = []
	puzzle = get_puzzle()
	visited = set()
	heapq.heappush(heap, (1,puzzle))
	while (len(heap) > 0):
		print("Visited: " + str(len(visited)) + " Queue Size: " + str(len(heap)))
		current = heapq.heappop(heap)[1]
		visited.add(str(current))
		if (current == goal_state): 
			print(current)
			print("END")
			break
		
		successors,successor_list = get_successor(current)
		for each_successor in successor_list:
			print(each_successor.puzzle,puzzle.link)

		for each_successor in successors:
			if (str(each_successor) not in str(visited)):
				heapq.heappush(heap, (1,each_successor))

		

if __name__ == "__main__":
	main()