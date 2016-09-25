#!/usr/local/bin/python3

import sys
import os
import copy
import math
import numpy as np
import datetime
from operator import itemgetter

n = 4

class State(object):
	
	puzzle = tuple()
	link = ''
	total = 0
	"""
	Constructor
	"""
	def __init__(self, puzzle, cost, link):
		self.puzzle = puzzle
		self.heuristic = self.manhattan()
		self.cost = cost
		self.link = link

	def __eq__ (self, other):
		return self.puzzle == other.puzzle

	def __ne__ (self, other):
		return self.puzzle != other.puzzle

	def __hash__ (self):
		return hash(self.puzzle)

	def successors(self):

		# Obtain coordinates of 0
		conv = np.asarray(self.puzzle)
		blank = np.where(conv == 0)
		x = blank[0][0]
		y = blank[1][0]

		successor_list = []

		if (self.link[-1] != 'U'):
			successor_list.append(self.move_down(np.asarray(copy.deepcopy(self.puzzle)), x, y, x-1, y)) # Move Down
		if (self.link[-1] != 'D'):
			successor_list.append(self.move_up(np.asarray(copy.deepcopy(self.puzzle)), x, y, x+1, y)) # Move Up
		if (self.link[-1] != 'R'):
			successor_list.append(self.move_left(np.asarray(copy.deepcopy(self.puzzle)), x, y, x, y+1)) # Move Left
		if (self.link[-1] != 'L'):
			successor_list.append(self.move_right(np.asarray(copy.deepcopy(self.puzzle)), x, y, x, y-1)) # Move right

		return successor_list

	def move_down(self, newstate, x0, y0, x1, y1):

		temp = newstate[x0][y0]
		if (x1 < 0):
			newstate[x0][y0] = newstate[n-1][y1]
			newstate[n-1][y1] = temp
		else:
			newstate[x0][y0] = newstate[x1][y1]
			newstate[x1][y1] = temp

		return State(tuple(map(tuple, newstate)), self.cost + 1, self.link + 'D')

	def move_up(self, newstate, x0, y0, x1, y1):

		temp = newstate[x0][y0]
		if (x1 > (n-1)):
			newstate[x0][y0] = newstate[0][y1]
			newstate[0][y1] = temp
		else:
			newstate[x0][y0] = newstate[x1][y1]
			newstate[x1][y1] = temp

		return State(tuple(map(tuple, newstate)), self.cost + 1, self.link + 'U')

	def move_right(self, newstate, x0, y0, x1, y1):

		temp = newstate[x0][y0]
		if (y1 < 0):
			newstate[x0][y0] = newstate[x1][n-1]
			newstate[x1][n-1] = temp
		else:
			newstate[x0][y0] = newstate[x1][y1]
			newstate[x1][y1] = temp

		return State(tuple(map(tuple, newstate)), self.cost + 1, self.link + 'R')

	def move_left(self, newstate, x0, y0, x1, y1):

		temp = newstate[x0][y0]
		if (y1 > (n-1)):
			newstate[x0][y0] = newstate[x1][0]
			newstate[x1][0] = temp
		else:
			newstate[x0][y0] = newstate[x1][y1]
			newstate[x1][y1] = temp

		return State(tuple(map(tuple, newstate)), self.cost + 1, self.link + 'L')

	def manhattan (self):

		goal = {0:None,
			1:[0,0], 2:[0,1], 3:[0,2], 4:[0,3],
			5:[1,0], 6:[1,1], 7:[1,2], 8:[1,3],
			9:[2,0], 10:[2,1], 11:[2,2], 12:[2,3],
			13:[3,0], 14:[3,1], 15:[3,2]}

		current = {}
		conv = np.asarray(self.puzzle)

		for each_row in range(len(conv)):
			for each_column in range(len(conv[each_row])):
				temp = []
				output = np.where(conv == conv[each_row][each_column])
				for each_section in output:
					temp.append(each_section[0])
				current[conv[each_row][each_column]] = temp

		total = 0
		for key in goal:
			a = current[key]
			b = goal[key]
			if b:
				x = abs(a[0] - b[0])
				y = abs(a[1] - b[1])
				if x >= 3: x = 1
				if y >= 3: y = 1
				total += (x+y)
		print(total)
		return total


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

    for each_item in range(len(matrix)):
        matrix[each_item] = tuple(matrix[each_item])

    return tuple(matrix)

def main():

	a = datetime.datetime.now()
	goal_state = tuple(((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 0)))
	goal = State(goal_state, 0, '')

	start_state = get_puzzle()
	start = State(start_state, 0, '0')
	if (start == goal):
		print()
		return
	start_data = (start.heuristic, start)

	visited = set()

	items = []
	fringe = {start: start_data}
	items.append(start_data)
	count = 0
	items = sorted(items,key=itemgetter(0))
	while items:

		#print(items)
		current_data = items.pop(0)
		heuristic_cost, current_state = current_data
		#print(np.asarray(current_state.puzzle))
		#print(items)

		# if count == 3:
		# 	break

		if (current_state == goal):
			#print(current_state.link)
			print(current_state.link[1:])
			print(len(current_state.link[1:]))
			b = datetime.datetime.now()
			print(b-a)
			print("Whoopie")
			break

		del fringe[current_state]
		visited.add(current_state.puzzle)

		for successor in current_state.successors():

			if successor.puzzle in visited:
				continue

			successor.total = successor.cost + successor.heuristic
			successor_data = (successor.total, successor)
			
			if successor not in fringe:
				fringe[successor] = successor_data
				items.append(successor_data)
			else:
				previous = fringe[successor]
				if successor.total < previous[1].total:
					previous = successor_data
			items = sorted(items,key=itemgetter(0))
					
		count += 1

if __name__ == "__main__":
	main