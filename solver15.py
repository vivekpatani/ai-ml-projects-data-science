#!/usr/local/bin/python3

import sys
import os
import copy
import heapq
import math
import numpy as np
import datetime

class State(object):

	puzzle = None
	link = None
	cost = None
	heuristic_cost = None

	def __init__ (self, puzzle, link, cost, heuristic_cost):
		self.puzzle = puzzle
		self.link = link
		self.cost = cost
		self.heuristic_cost = heuristic_cost

	def __eq__ (self, other):
	 	return self.cost == other.cost

	def __lt__ (self, other):
		return self.cost < other.cost

	def __gt__ (self, other):
		return self.cost > other.cost

"""
Declaring all the variables needed throughout.
"""
n = 4
goal_state = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])

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
	origin = State (np.array(reader), '0', 0, 0)
	return origin

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

def calc_manhattan (puzzle):

	"""
	Returns Manhattan distance between goal state and current state.
	Manhattan distance is the distance of each tile from its original position
	"""
	final = {0:None,
			1:[0,0], 2:[0,1], 3:[0,2],4:[0,3],
			5:[1,0], 6:[1,1], 7:[1,2], 8:[1,3],
			9:[2,0], 10:[2,1], 11:[2,2], 12:[2,3],
			13:[3,0], 14:[3,1], 15:[3,2]}

	current = {}
	for each_row in range(len(puzzle)):
		for each_column in range(len(puzzle[each_row])):
			temp = []
			output = np.where(puzzle == puzzle[each_row][each_column])
			for each_section in output:
				temp.append(each_section[0])
			current[puzzle[each_row][each_column]] = temp

	total = 0
	for key in current:
		a = current[key]
		b = final[key]
		if b:
			#print(str(a[0]) + " - " + str(b[0]) + " = " +  str(abs(a[0] - b[0])) + " " + str(a[1]) + " - " + str(b[1]) + " = " + str(abs(a[1] - b[1])))
			x = abs(a[0] - b[0])
			y = abs(a[1] - b[1])
			if x >= 3:
				x = 1
			if y >= 3:
				y = 1
			cost = x + y
			total += cost
	
	# print("TOTAL")
	# print(total)
	# print(puzzle)
	return total
	#return calc_hamming(puzzle)

def get_successor (state):

	"""
	Returns a valid successor from the current state
	"""

	# Getting the location of empty tile
	row, column = find_coordinates(state.puzzle)
	successor_object = []

	# To Get Up Successor
	successor1, h_cost1 = move_up (state.puzzle, row, column)
	successor11 = State(successor1, state.link + 'D', 1 + state.cost, state.heuristic_cost + h_cost1)
	if (state.link[-1] != 'U'):
		successor_object.append(successor11)

	# To Get Down Successor
	successor2, h_cost2 = move_down (state.puzzle, row, column)
	successor21 = State(successor2, state.link + 'U', 1 + state.cost, state.heuristic_cost + h_cost2)
	if (state.link[-1] != 'D'):
		successor_object.append(successor21)
	
	# To Get Left Successor
	successor3, h_cost3 = move_left (state.puzzle, row, column)
	successor31 = State(successor3, state.link + 'R', 1 + state.cost, state.heuristic_cost + h_cost3)
	if (state.link[-1] != 'L'):
		successor_object.append(successor31)

	# To Get Right Successor
	successor4, h_cost4 = move_right (state.puzzle, row, column)
	successor41 = State(successor4, state.link + 'L', 1 + state.cost, state.heuristic_cost + h_cost4)
	if (state.link[-1] != 'R'):
		successor_object.append(successor41)

	return successor_object

def move_up(state, row, column):

	"""
	Returns the Left movement of the blank tile in the current state
	"""
	newstate = copy.deepcopy(state)
	temp = newstate[row][column]
	if (row == 0):
		newstate[row][column] = newstate[n-1][column]
		newstate[n-1][column] = temp

	else:
		newstate[row][column] = newstate[row-1][column]
		newstate[row-1][column] = temp
	return newstate, calc_manhattan(newstate)

def move_down(state, row, column):

	"""
	Returns the Left movement of the blank tile in the current state
	"""
	newstate = copy.deepcopy(state)
	temp = newstate[row][column]
	if (row == (n-1)):
		newstate[row][column] = newstate[0][column]
		newstate[0][column] = temp

	else:
		newstate[row][column] = newstate[row+1][column]
		newstate[row+1][column] = temp
	return newstate, calc_manhattan(newstate)

def move_left(state, row, column):

	"""
	Returns the Left movement of the blank tile in the current state
	"""
	newstate = copy.deepcopy(state)
	temp = newstate[row][column]
	if (column == 0):
		newstate[row][column] = newstate[row][n-1]
		newstate[row][n-1] = temp

	else:
		newstate[row][column] = newstate[row][column-1]
		newstate[row][column-1] = temp
	return newstate, calc_manhattan(newstate)

def move_right(state, row, column):

	"""
	Returns the Left movement of the blank tile in the current state
	"""
	newstate = copy.deepcopy(state)
	temp = newstate[row][column]
	if (column == (n-1)):
		newstate[row][column] = newstate[row][0]
		newstate[row][0] = temp

	else:
		newstate[row][column] = newstate[row][column+1]
		newstate[row][column+1] = temp
	return newstate, calc_manhattan(newstate)

def find_coordinates (state, n=0):

	"""
	Find the empty tile and return its location
	"""
	for each_row in range(len(state)):
		for each_column in range(len(state[each_row])):
			if (state[each_row][each_column] == n): return each_row,each_column


def main():

	a = datetime.datetime.now()
	heap = []
	puzzle = get_puzzle()
	visited = set()
	count = 0
	heapq.heappush(heap, (calc_manhattan(puzzle.puzzle),puzzle))
	while (len(heap) > 0):
		count+=1
		current = heapq.heappop(heap)[1]
		#print(current.heuristic_cost)
		#print("Visited: " + str(len(visited)) + " Queue Size: " + str(len(heap)) + " Heuristic: " + str(current.heuristic_cost) + " Type: " + str(type(current.puzzle)))
		if (count == 100):
			print(current.puzzle)
			count = 0
		visited.add(tuple(map(tuple,current.puzzle)))
		temp = tuple(map(tuple,current.puzzle))
		if (np.array_equal(current.puzzle,goal_state)): 
			print(current.puzzle)
			print(current.link)
			print(current.cost)
			print("END")
			b = datetime.datetime.now()
			print(b-a)
			break
		
		successor_list = get_successor(current)
		for each_successor in successor_list:

			if (tuple(map(tuple,each_successor.puzzle)) not in visited):
				heapq.heappush(heap, (each_successor.heuristic_cost, each_successor))

			for current_obj in heap:
				if (np.array_equal(each_successor.puzzle,current_obj[1].puzzle)):
					if (each_successor.heuristic_cost < current_obj[1].heuristic_cost):
						print("Init Cost: " + str(current_obj[1].heuristic_cost) + "   Final Cost: " + str(each_successor.heuristic_cost))
						heap.remove(current_obj)
						heapq.heappush(heap, (each_successor.heuristic_cost, each_successor))



if __name__ == "__main__":
	main()