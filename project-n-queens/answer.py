# -*- coding: utf-8 -*-
"""
Spyder Editor

This is the solution for N Queens/Rooks problem.
CSCI - B 551
vpatani (Vivek Patani)
"""
import sys
import numpy as np

#Increase the recursion stack limit
sys.setrecursionlimit(1000000000)

#This is the number of Rooks/Queens
N = int(sys.argv[2])

#The option to choose from Queens or Rooks
option = int(sys.argv[1])


"""
Newly Added Function Starts
"""
# This functions moves from one state to another and returns all the valid successors which is the final solution
def successors3 (columns, starting_point = 0):
    # success/base condition
    if ( len(columns) == N ):
        return columns
    else:
        #keep checking rows for each columns
        for this_row in range (starting_point, N):
            if (isPlacable (columns, len(columns), this_row)):
                columns.append(this_row)
                return successors3(columns)
        else:
            #Invalid State
            if (len(columns) == 0): return False # If empty, no solution at all!
            current = columns.pop()
            return successors3(columns, current+1) #check next possible successor i.e. next row

# This is used to check the validity of position, this is the optimisation.
def isPlacable (columns, this_column, this_row):
    # Checking for attacking positions if any for queens
    if (option == 1):
        for current_row in columns:
            current_column = columns.index(current_row) #Obtain the current column
            if (this_row == current_row or this_column == current_column): return False #Formula for horizontal/vertical
            elif (current_row + current_column == this_row + this_column or current_row - current_column == this_row - this_column): return False #Formula for diagonals
        return True
    elif (option == 2) :
        for current_row in columns:
            current_column = columns.index(current_row) #Obtain the current column
            if (this_row == current_row or this_column == current_column): return False #Formula for horizontal/vertical
        return True
    else: return False

# Printable Function
def printable_board2(board):
    
    if (not board): print("Sorry! Meh, no solution was available.")
    else:
        tag = 'Q'
        if (option == 2): tag = 'R'
        answer = [['_' for x in range(N)] for y in range(N)]
        for element in range(len(board)):
            answer[element][board[element]] = tag

        answer_string = ""
        for each_row in range(len(answer)):
            for each_column in range(len(answer[each_row])):
                answer_string += answer[each_row][each_column] + " "
            answer_string += "\n"

        print(answer_string)

"""
Newly Added Function Ends
"""

    # Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ " ".join([ "Q" if col else "_" for col in row ]) for row in board])

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors(board):
    return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]

# Improved version of successor.
def successors2(board):
    return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) if count_pieces(board) <= N and add_piece(board,r,c) != board ]

# The more improved version of successor.
def put(board):
	# Finds all the valid successors and returns a solution if it exists
    return successors3 (board, starting_point=0)

# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )

# Solve n-rooks!
def solve(initial_board):

    #Toggle Switch #2
    if True:
        return put(initial_board)
    else:
        fringe = [initial_board]
        while len(fringe) > 0:
            for s in successors2( fringe.pop() ):
                if is_goal(s):
                    return(s)
                fringe.append(s)
        return False
 
#Toggle Switch #1
if True:
    initial_board = [[0]*N]*N
    solution = solve([] * N)
    print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")
    printable_board2(solution)
else:
    initial_board = [[0]*N]*N
    print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")
    solution = solve(initial_board)
    printable_board(solution)
    print (printable_board(solution) if solution else "Sorry, no solution found. :(")