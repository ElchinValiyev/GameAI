# Add mouse controls
# add half size paddle after hitting back wall

import math, pygame, sys, shutil, getpass
from pygame.locals import *
from fuzzy_agent import FuzzyAgent
from fuzzy_trajectory import FuzzyTrajectory

pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((640, 480))  # create screen - 640 pix by 480 pix
pygame.display.set_caption('Breakout')  # set title bar
icon = pygame.image.load('breakout.png')
winner_image = pygame.image.load('/home/abbas/Desktop/winner.png')
winner_rect = winner_image.get_rect()
pygame.display.set_icon(icon)

# add the font; use PressStart2P, but otherwise default if not available
try:
    fontObj = pygame.font.Font('PressStart2P.ttf', 36)
except:
    fontObj = pygame.font.Font('freesansbold.ttf', 36)

# generic colors-------------------------------
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
white = pygame.Color(255, 255, 255)
grey = pygame.Color(142, 142, 142)
black = pygame.Color(0, 0, 0)

# row colors-----------------------------------
r1 = pygame.Color(200, 72, 72)
r2 = pygame.Color(198, 108, 58)
r3 = pygame.Color(180, 122, 48)
r4 = pygame.Color(162, 162, 42)
r5 = pygame.Color(72, 160, 72)
r6 = pygame.Color(67, 73, 202)
colors = [r1, r2, r3, r4, r5, r6]

# variables------------------------------------
controls = 'keys'  # control method
mousex, mousey = 0, 0  # mouse position
dx, dy = 18, 6  # dimensions of board
bx, by = 50, 150  # board position
score = 0  # score
wall1 = pygame.Rect(20, 100, 30, 380)  # walls of the game
wall2 = pygame.Rect(590, 100, 30, 380)
wall3 = pygame.Rect(20, 80, 600, 30)


# Creates a board of rectangles----------------
def new_board():
    board = []
    for x in range(dx):
        board.append([])
        for y in range(dy):
            board[x].append(1)
    return board


# Classes defined------------------------------
class Paddle:  # class for paddle vars
    x = 320
    y = 450
    size = 2  # 2 is normal size, 1 is half-size
    direction = 'none'


class Ball:  # class for ball vars
    def __init__(self):
        self.x = 0
        self.y = 0
        self.remaining = 3
        self.xPos = 1  # amount increasing by for x. adjusted for speed
        self.yPos = 1
        self.adjusted = False  # says whether the xPos and yPos have been adjusted for speed
        self.speed = 5
        self.collisions = 0
        self.alive = False
        self.moving = False

    def rect(self):
        return pygame.Rect(self.x - 3, self.y - 3, 6, 6)

    def adjust(self):  # adjusts the x and y being added to the ball to make the hypotenuse the ball speed
        tSlope = math.sqrt(self.xPos ** 2 + self.yPos ** 2)
        self.xPos *= (self.speed / tSlope)
        self.yPos *= (self.speed / tSlope)
        self.adjusted = True


# Functions defined----------------------------
def print_board(board, colors):  # prints the board
    for x in range(dx):
        for y in range(dy):
            if board[x][y] == 1:
                pygame.draw.rect(screen, colors[y], (((x * 30) + bx), ((y * 12) + by), 30, 12))


def print_paddle(paddle):  # prints the paddle
    if paddle.size == 2:
        pygame.draw.rect(screen, red, ((paddle.x - 20), (paddle.y), 40, 5))


def collide_paddle(paddle, ball):  # recalculates the trajectory for the ball after collision with the paddle
    ball.adjusted = False
    if ball.x - paddle.x != 0:
        difference=float(ball.x) - float(paddle.x)
        trajectory=FuzzyTrajectory().compute(difference)
        ball.xPos = float(trajectory)
        ball.yPos = -1
    else:
        print "ball position ", ball.x, " paddle position ", ball.yPos
        ball.xPos = 0
        ball.yPos = 1
    return ball.adjusted, float(ball.xPos), float(ball.yPos)


def write(x, y, color, msg):  # prints onto the screen in selected font
    msgSurfaceObj = fontObj.render(msg, False, color)
    msgRectobj = msgSurfaceObj.get_rect()
    msgRectobj.topleft = (x, y)
    screen.blit(msgSurfaceObj, msgRectobj)


def game(score, paddle, ball, board, wall1, agent):  # The game itself
    # starting variables
    running = True
    ball.alive = True
    ball.moving = False
    ball.x = 53
    ball.y = 300
    ball.collisions, ball.speed = 0, 5
    colO = False  # check collision with the orange row, for speed purposes
    colR = False  # same but for red row
    ball.speed = 5
    ball.xPos = 1
    ball.yPos = 1
    ball.adjusted = False

    while running:
        # Draw all the things------------------------------
        screen.fill(black)
        pygame.draw.rect(screen, grey, wall1)
        pygame.draw.rect(screen, grey, wall2)
        pygame.draw.rect(screen, grey, wall3)
        pygame.draw.rect(screen, red, (ball.x - 3, ball.y - 3, 6, 6))  # drawing ball
        print_board(board, colors)
        print_paddle(paddle)
        write(20, 20, grey, str(score))  # score
        temp = 0
        for life in range(ball.remaining):  # drawing life rectangles on the right side
            if life != 0:
                pygame.draw.rect(screen, red, (600, 400 - temp, 10, 10))
                temp += 15

        # check all the collisions-------------------------
        if ball.moving:
            if not ball.adjusted:
                ball.adjust()
            ball.x += ball.xPos
            ball.y += ball.yPos
            if ball.y < 455 and ball.y > 445:
                if ball.x > paddle.x - 20 and ball.x < paddle.x + 20:
                    ball.adjusted, ball.xPos, ball.yPos = collide_paddle(paddle, ball)  # paddle collide
                    ball.collisions += 1
                    # increase ball speeds at 4 hits on paddle, 12 hits, orange row, red row
                    if ball.collisions % 4 == 0:
                        ball.speed += 0.24

            # check wall collide----------------------------
            if wall1.colliderect(ball.rect()) or wall2.colliderect(ball.rect()):
                ball.xPos = -(ball.xPos)
            if wall3.colliderect(ball.rect()):
                ball.yPos = -(ball.yPos)

            # check collision with bricks-------------------
            Break = False
            for x in range(dx):
                for y in range(dy):
                    if board[x][y] == 1:
                        block = pygame.Rect(30 * x + bx - 1, 12 * y + by - 1, 32, 14)
                        if block.collidepoint(ball.x, ball.y):
                            board[x][y] = 0
                            ball.yPos = -ball.yPos
                            if y == 4 or y == 5:
                                score += 1
                            elif y == 2 or y == 3:
                                score += 4
                                if colO == False:
                                    colO = True
                                    ball.speed += 0.25
                            else:
                                score += 7
                                if colR == False:
                                    colR = True
                                    ball.speed += 0.5
                            Break = True
                            # ball.speed += 1
                    if Break:
                        break
                if Break:
                    break
            if ball.y > 460:
                ball.alive = False
        if score == 432:
            running = False
        # check if ball was lost
        if not ball.alive:
            running = False
            ball.remaining -= 1

        agent_move(ball, paddle, agent)

        # get user input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if not ball.moving:
                        ball.moving = True
        # update display
        pygame.display.update()
        fpsClock.tick(120)
    return score


def agent_move(ball, paddle, agent):
    distance = paddle.x - ball.x
    paddle.x += agent.compute(distance)


# -----------------------------------------------------
if __name__ == '__main__':
    replay = False
    loop = 0
    while True:
        screen.fill(black)
        if replay:
            board = new_board()
            score = 0
            paddle = Paddle()
            ball = Ball()
            agent = FuzzyAgent()
            while ball.remaining > 0:
                score = game(score, paddle, ball, board, wall1, agent)
                if score == 432:
                    replay = True
                    break
                if ball.remaining == 0:
                    for x in range(16):
                        for y in range(12):
                            pygame.draw.rect(screen, black, (x * 40, y * 40, 40, 40))
                            pygame.display.update()
                            pygame.time.wait(10)
                            boardcheck = 0
                    for x in range(len(board)):
                        for y in range(len(board[x])):
                            boardcheck += board[x][y]
                    if boardcheck == 0:
                        paddle = Paddle()
                        ball = Ball()
                        board = new_board()
                        while ball.remaining > 0:
                            score = game(score, paddle, ball, board, wall1, agent)
                            if score == 432:
                                for x in range(16):
                                    for y in range(12):
                                        pygame.draw.rect(screen, black, (x * 40, y * 40, 40, 40))
                                        pygame.display.update()
                                        pygame.time.wait(10)

                            if ball.remaining == 0:
                                for x in range(16):
                                    for y in range(12):
                                        pygame.draw.rect(screen, black, (x * 40, y * 40, 40, 40))
                                        pygame.display.update()
                                        pygame.time.wait(10)
                    replay = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        replay = True
        loop += 1
        pygame.display.update()
