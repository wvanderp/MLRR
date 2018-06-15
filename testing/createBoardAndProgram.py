from random import randint

EMPTY = 0
BOX = 1

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


def createBoardAndProgram(width, height, numberOfBoxes, lengthOfProgram):
    board = [[BOX] * width]
    for i in range(height - 2):
        board.append([BOX] + [EMPTY] * (width - 2) + [BOX])
    board.append([BOX] * width)

    for i in range(numberOfBoxes + 1):
        tryAgain = True
        while tryAgain:
            x = randint(1, width - 2)
            y = randint(1, height - 2)
            if board[y][x] == EMPTY:
                if i < numberOfBoxes:  # the last iteration is used to place start
                    board[y][x] = BOX
                tryAgain = False

    startX = x
    startY = y
    program = [randint(0, 3)]  # initial direction

    for i in range(lengthOfProgram):
        if program[i] == NORTH:
            dx = 0
            dy = 1
        elif program[i] == EAST:
            dx = 1
            dy = 0
        elif program[i] == SOUTH:
            dx = 0
            dy = -1
        elif program[i] == WEST:
            dx = -1
            dy = 0
        if i == lengthOfProgram - 1:  # last leg
            steps = 2  # max number of steps
        else:
            steps = max(width, height)  # max number of steps; will hit a box before this is reached
            program.append((program[i] + 2 * randint(0, 1) - 1) % 4)  # turn left or right
        while board[y + dy][x + dx] != BOX and steps > 0:
            x += dx
            y += dy
            steps -= 1

    # x and y now contain goal position; it is possible that start and goal are identical
    return board, startX, startY, x, y, program
