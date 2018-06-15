from sys import exit

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from createBoardAndProgram import *
from solveRobots import *

SQUARE_SIZE = 50
BOARD_SIZE_X = 12
BOARD_SIZE_Y = 12
LENGTH_OF_PROGRAM = 4
SCORE_TEXT_HEIGHT = 30
WIDTH = BOARD_SIZE_X * SQUARE_SIZE
HEIGHT = BOARD_SIZE_Y * SQUARE_SIZE + SCORE_TEXT_HEIGHT

EMPTY = 0
BOX = 1
START = 2
GOAL = 3

RED = 1, 0, 0
GREEN = 0, 1, 0
YELLOW = 1, 1, 0
BLUE = 0, 0, 1
BLACK = 0, 0, 0
GREY = 0.5, 0.5, 0.5
WHITE = 1, 1, 1

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

ANIMATION_SPEED = 0.005
GAMES_TO_PLAY = 100


class Display:
    def __init__(self, windowName):
        glutInit()
        glutInitDisplayMode(GLUT_MULTISAMPLE | GLUT_DOUBLE)
        glutInitWindowSize(WIDTH, HEIGHT)
        glutCreateWindow(windowName.encode("ascii"))
        glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)

    def reshape(self, x, y):
        if x / y > WIDTH / HEIGHT:
            glViewport(0, 0, int(y * WIDTH / HEIGHT), y)
        else:
            glViewport(0, 0, x, int(x * HEIGHT / WIDTH))

    animationCallbacks = []

    def animate(self):
        for i in Display.animationCallbacks:
            i()

    def startDraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def endDraw(self):
        glutSwapBuffers()

    def drawString(self, x, y, colour, string):
        glColor(colour)
        glLineWidth(2)
        # glDisable(GL_MULTISAMPLE)
        glPushMatrix()
        glDepthMask(GL_FALSE)
        glTranslate(x, y, 0);
        glScale(0.15, 0.15, 1)
        width = 0
        for i in string:
            width += glutStrokeWidth(GLUT_STROKE_ROMAN, ord(i))
        glTranslate(-width / 2, 0, 0);
        for i in string:
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(i))
        glDepthMask(GL_TRUE)
        glPopMatrix()
        # glEnable(GL_MULTISAMPLE)

    def drawSquare(self, x, y):
        glColor(GREY)
        glRecti(x * SQUARE_SIZE + 1, y * SQUARE_SIZE + 1, (x + 1) * SQUARE_SIZE - 1, (y + 1) * SQUARE_SIZE - 1)

    def drawBox(self, x, y):
        glColor(YELLOW)
        glRecti(x * SQUARE_SIZE + 1, y * SQUARE_SIZE + 1, (x + 1) * SQUARE_SIZE - 1, (y + 1) * SQUARE_SIZE - 1)
        glColor(BLACK)
        glLineWidth(1)
        glBegin(GL_LINES)
        glVertex((x + 0.2) * SQUARE_SIZE, y * SQUARE_SIZE)
        glVertex((x + 0.2) * SQUARE_SIZE, (y + 1) * SQUARE_SIZE)
        glVertex((x + 0.8) * SQUARE_SIZE, y * SQUARE_SIZE)
        glVertex((x + 0.8) * SQUARE_SIZE, (y + 1) * SQUARE_SIZE)
        glVertex((x + 0.2) * SQUARE_SIZE, (y + 0.2) * SQUARE_SIZE)
        glVertex((x + 0.8) * SQUARE_SIZE, (y + 0.2) * SQUARE_SIZE)
        glVertex((x + 0.2) * SQUARE_SIZE, (y + 0.8) * SQUARE_SIZE)
        glVertex((x + 0.8) * SQUARE_SIZE, (y + 0.8) * SQUARE_SIZE)
        glVertex((x + 0.4) * SQUARE_SIZE, (y + 0.2) * SQUARE_SIZE)
        glVertex((x + 0.4) * SQUARE_SIZE, (y + 0.8) * SQUARE_SIZE)
        glVertex((x + 0.6) * SQUARE_SIZE, (y + 0.2) * SQUARE_SIZE)
        glVertex((x + 0.6) * SQUARE_SIZE, (y + 0.8) * SQUARE_SIZE)
        glEnd()

    def drawDisk(self, cx, cy, r):
        c = 0.951056516295154  # cos(18°)
        s = 0.309016994374947  # sin(18°)
        x = r
        y = 0
        glBegin(GL_POLYGON)
        for i in range(20):
            glVertex(cx + x, cy + y)
            t = x
            x = c * x - s * y
            y = s * t + c * y
        glEnd()

    def drawStart(self, x, y):
        self.drawString((x + 0.5) * SQUARE_SIZE, (y + 0.4) * SQUARE_SIZE, BLUE, "start")

    def drawGoal(self, x, y):
        self.drawString((x + 0.5) * SQUARE_SIZE, (y + 0.4) * SQUARE_SIZE, GREEN, "goal")

    def drawRobot(self, x, y, colour, steps):
        glColor(colour)
        self.drawDisk((x + 0.5) * SQUARE_SIZE, (y + 0.75) * SQUARE_SIZE, 0.2 * SQUARE_SIZE)
        self.drawDisk((x + 0.5) * SQUARE_SIZE, (y + 0.35) * SQUARE_SIZE, 0.3 * SQUARE_SIZE)
        self.drawString((x + 0.5) * SQUARE_SIZE, (y + 0.2) * SQUARE_SIZE, WHITE, str(steps))

    def drawScore(self, played, won, lost):
        if played > 0:
            score = round(100 * won / played)
        else:
            score = "--"
        self.drawString(WIDTH / 2, HEIGHT - 0.7 * SCORE_TEXT_HEIGHT, WHITE,
                        "Games played: " + str(played) + "; Won: " + str(won) + "; Lost: " + str(
                            lost) + "; Score: " + str(score) + "%")


class Robot:
    def __init__(self, x, y, colour, board, program):
        self.posX = x
        self.posY = y
        self.colour = colour
        self.board = board
        self.program = program
        self.steps = 0

    def draw(self, display):
        display.drawRobot(self.posX, self.posY, self.colour, self.steps)

    def go(self, parent):
        self.parent = parent
        if len(self.program) > 0:
            self.steps += 1
            direction = self.program.pop(0)
            if direction == NORTH:
                self.vectorX = 0
                self.vectorY = 1
            elif direction == EAST:
                self.vectorX = 1
                self.vectorY = 0
            elif direction == SOUTH:
                self.vectorX = 0
                self.vectorY = -1
            elif direction == WEST:
                self.vectorX = -1
                self.vectorY = 0
            self.prevTime = glutGet(GLUT_ELAPSED_TIME)
            Display.animationCallbacks.append(self.animate)
        else:
            parent.played += 1
            parent.lost += 1
            parent.newBoard()

    def animate(self):
        time = glutGet(GLUT_ELAPSED_TIME)
        elapsedTime = time - self.prevTime
        self.prevTime = time
        self.posX += self.vectorX * elapsedTime * ANIMATION_SPEED
        self.posY += self.vectorY * elapsedTime * ANIMATION_SPEED
        thisSquare = self.board[round(self.posY - 0.5 * self.vectorY)][round(self.posX - 0.5 * self.vectorX)]
        nextSquare = self.board[round(self.posY + 0.5 * self.vectorY)][round(self.posX + 0.5 * self.vectorX)]
        if thisSquare == GOAL or nextSquare == BOX:
            self.posX = round(self.posX)
            self.posY = round(self.posY)
            Display.animationCallbacks.remove(self.animate)
        if thisSquare == GOAL:
            self.parent.played += 1
            self.parent.won += 1
            self.parent.newBoard()
        elif nextSquare == BOX:
            self.go(self.parent)
        glutPostRedisplay()


class Main:
    played = 0
    won = 0
    lost = 0

    def __init__(self):
        self.display = Display("Ricochet Robots")
        glutDisplayFunc(self.draw)
        glutKeyboardFunc(self.keyboardFunc)
        glutIdleFunc(self.display.animate)
        glutReshapeFunc(self.display.reshape)
        init()
        self.newBoard()
        glutMainLoop()

    def newBoard(self):
        if self.played < GAMES_TO_PLAY:
            self.board, startX, startY, goalX, goalY, program = createBoardAndProgram(BOARD_SIZE_X, BOARD_SIZE_Y, 10, 4)
            startBoard = [[0] * BOARD_SIZE_X for i in range(BOARD_SIZE_Y)]
            startBoard[startY][startX] = 1
            goalBoard = [[0] * BOARD_SIZE_X for i in range(BOARD_SIZE_Y)]
            goalBoard[goalY][goalX] = 1
            program = solve(self.board, startBoard, goalBoard)
            self.board[startY][startX] = START
            self.board[goalY][goalX] = GOAL
            self.robot = Robot(startX, startY, RED, self.board, program)
            self.robot.go(self)

    def draw(self):
        self.display.startDraw()
        for y in range(BOARD_SIZE_Y):
            for x in range(BOARD_SIZE_X):
                if self.board[y][x] == BOX:
                    self.display.drawBox(x, y)
                else:
                    self.display.drawSquare(x, y)
                if self.board[y][x] == START:
                    self.display.drawStart(x, y)
                elif self.board[y][x] == GOAL:
                    self.display.drawGoal(x, y)
        self.robot.draw(self.display)
        self.display.drawScore(self.played, self.won, self.lost)
        self.display.endDraw()

    def keyboardFunc(self, key, x, y):
        if key == b"\x1b":  # escape
            exit()


Main()
