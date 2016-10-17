# Simple tetris program! v0.2
# D. Crandall, Sept 2016

from AnimatedTetris import *
from SimpleTetris import *
from kbinput import *
import time, sys


class HumanPlayer:
    def get_moves(self, tetris):
        print "Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\nThen press enter. E.g.: bbbnn\n"
        moves = raw_input()
        return moves

    def control_game(self, tetris):
        while 1:
            c = get_char_keyboard()
            commands = {"b": tetris.left, "n": tetris.rotate, "m": tetris.right, " ": tetris.down}
            commands[c]()


#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. tetris is an object that lets you inspect the board, e.g.:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    def calcRange(self, rotatedPiece):
        return 1 + tetris.BOARD_WIDTH - ComputerPlayer.pieceWidth(self, rotatedPiece)

    def checkCollisionWithRow(self, board, piece, row, col):
        return row < tetris.BOARD_HEIGHT and TetrisGame.check_collision((board, 0), piece, row + 1,
                                                                        col)

    def calcAggregateHeight(self, board):
        aggHeight = []
        for i in range(0, tetris.BOARD_WIDTH):
            for j in range(len(board)):
                if board[j][i] == 'x':
                    aggHeight.append(len(board) - j)
                    break
                if j == len(board) - 1:
                    aggHeight.append(0)
        return aggHeight

    def calcBumpness(self, height):
        bumpness = 0

        for i in range(len(height)):
            if i < len(height) - 1:
                bumpness += abs(height[i] - height[i + 1])

        return bumpness

    def calcHoles(self, board, height):
        holes = 0

        for i in range(0, tetris.BOARD_WIDTH):
            if sum(height) != 0:
                for j in range(len(board) - height[i], len(board)):
                    if board[j][i] == ' ':
                        holes += 1

        return holes

    def calculateFullLines(self, board):
        completeLines = 0

        for i in range(len(board)):
            if board[i].count(board[i][0]) == len(board[i]) and board[i][0] == 'x':
                completeLines += 1

        return completeLines

    def calculateAlitude(self, height):
        return max(height) - min(height)

    def rotateAndPlace(self, origBoard, piece, nextPiece):
        tempBoard = origBoard[:]
        tempPiece = piece[:]
        tempNextPiece = nextPiece[:]

        angles = [0, 90, 180, 270]

        bestrow = -1
        bestcol = -1
        bestPiece = []
        angle = 0
        highestScore = -9999
        # Assigning a negative for Penalties or a positive values for Rewards
        penaltyForHigherLines = -1.5
        rewardForCompleteLines = 4.5
        penaltyForMoreHoles = -3
        penaltyForMoreBumpness = -1.5

        try:
            for rotation in angles:
                rotatedPiece = TetrisGame.rotate_piece(tempPiece, rotation)
                for column in range(ComputerPlayer.calcRange(self, rotatedPiece)):
                    row = 0

                    while not ComputerPlayer.checkCollisionWithRow(self, tempBoard, rotatedPiece, row, column):
                        row += 1

                    placedPiece = TetrisGame.place_piece((tempBoard, 0), rotatedPiece, row, column)
                    temporaryBoard = placedPiece[0][:]
                    placedRow = row - 1

                    for rotation1 in angles:
                        rotatedNextPiece = TetrisGame.rotate_piece(tempNextPiece, rotation1)
                        for col1 in range(ComputerPlayer.calcRange(self, rotatedNextPiece)):
                            row1 = 0
                            while not ComputerPlayer.checkCollisionWithRow(self, temporaryBoard, rotatedNextPiece, row1,
                                                                           col1):
                                row1 += 1
                            placedNextPiece = TetrisGame.place_piece((temporaryBoard, 0), rotatedNextPiece,
                                                                     row1, col1)

                            aggHeight = ComputerPlayer.calcAggregateHeight(self, placedNextPiece[0])

                            score = (penaltyForHigherLines * sum(aggHeight)) + (
                            rewardForCompleteLines * ComputerPlayer.calculateFullLines(self, placedNextPiece[0])) + (
                                        penaltyForMoreHoles * ComputerPlayer.calcHoles(self, placedNextPiece[0],
                                                                                       aggHeight)) + (
                                    penaltyForMoreBumpness * ComputerPlayer.calcBumpness(self, aggHeight))

                            if score > highestScore:
                                highestScore = score
                                bestrow = placedRow
                                bestcol = column
                                bestPiece = rotatedPiece
                                angle = rotation
        except:
            print 'Something Must have gone wrong'

        return bestrow, bestcol, bestPiece, angle

    def get_moves(self, tetris):
        rotationNumber = {0: 0, 90: 1, 180: 2, 270: 3}
        steps = ''
        while 1:
            row, col, piece1, angle = ComputerPlayer.rotateAndPlace(self, tetris.get_board(), tetris.get_piece()[0],
                                                                    tetris.get_next_piece())
            numberOfRotations = rotationNumber.get(angle)

            while numberOfRotations > 0:
                steps += 'n'
                numberOfRotations -= 1

            offset = tetris.col - col

            if offset > 0:
                while offset > 0:
                    steps += 'b'
                    offset -= 1
            else:
                while offset < 0:
                    steps += 'm'
                    offset += 1

            return steps

    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "tetris" object to control the movement. In particular:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    def pieceWidth(self, curPiece):
        maximumWidth = -9999
        for i in range(len(curPiece)):
            if len(curPiece[i]) > maximumWidth:
                maximumWidth = len(curPiece[i])
        return maximumWidth

    def control_game(self, tetris):
        rotationNumber = {0: 0, 90: 1, 180: 2, 270: 3}

        while 1:
            time.sleep(0.1)
            row, col, bestPiece, angle = ComputerPlayer.rotateAndPlace(self, tetris.get_board(), tetris.get_piece()[0],
                                                                       tetris.get_next_piece())
            numberOfRotations = rotationNumber.get(angle)

            while numberOfRotations > 0:
                tetris.rotate()
                numberOfRotations -= 1

            offset = tetris.col - col

            if offset > 0:
                while offset > 0:
                    tetris.left()
                    offset -= 1
            else:
                while offset < 0:
                    tetris.right()
                    offset += 1
            tetris.down()


(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print "unknown player!"

    if interface_opt == "simple":
        tetris = SimpleTetris()
    elif interface_opt == "animated":
        tetris = AnimatedTetris()
    else:
        print "unknown interface!"

    tetris.start_game(player)

except EndOfGame as s:
    print "\n\n\n", s



