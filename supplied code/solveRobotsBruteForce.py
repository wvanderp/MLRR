NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

BOX = 1

MAX_DEPTH = 4

def init():
    pass

def findOne(board):
    for i, row in enumerate(board):
        if 1 in row:
            return row.index(1), i

def test(sx, sy, gx, gy, boxBoard, depth, program):
    if depth == MAX_DEPTH:
        return -1
    for direction in range(4):
        x = sx
        y = sy
        if direction == NORTH:
            dx = 0
            dy = 1
        elif direction == EAST:
            dx = 1
            dy = 0
        elif direction == SOUTH:
            dx = 0
            dy = -1
        elif direction == WEST:
            dx = -1
            dy = 0
        while boxBoard[y + dy][x + dx] != BOX:
            x += dx
            y += dy
            if x == gx and y == gy:
                return program + [direction]
        nextStep = test(x, y, gx, gy, boxBoard, depth + 1, program + [direction])
        if nextStep != -1:
            return nextStep
    return -1

    
def solve(boxBoard, startBoard, goalBoard):
    sx, sy = findOne(startBoard)
    gx, gy = findOne(goalBoard)
    return test(sx, sy, gx, gy, boxBoard, 0, [])
