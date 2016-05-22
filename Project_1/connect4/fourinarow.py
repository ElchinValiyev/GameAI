import matplotlib.pyplot as plt
import numpy as np
import pygame
import random
from Tkinter import *
from pygame.locals import *

BOARDWIDTH = 7  # how many spaces wide the board is
BOARDHEIGHT = 6  # how many spaces tall the board is
assert BOARDWIDTH >= 4 and BOARDHEIGHT >= 4, 'Board must be at least 4x4.'

INIT_SPEED = 15  # Speed with which User tokens move
SPACESIZE = 50  # size of the tokens and individual board spaces in pixels

FPS = 60  # frames per second to update the screen
WINDOWWIDTH = 520  # width of the program's window, in pixels
WINDOWHEIGHT = 480  # height in pixels

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * SPACESIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - BOARDHEIGHT * SPACESIZE) / 2)

Custom_Color = (50, 50, 155)
WHITE = (255, 255, 255)
BGCOLOR = Custom_Color
TEXTCOLOR = WHITE

RED = 1
BLACK = -1
EMPTY = 0
HUMAN = 1
COMPUTER = -1
lookup = np.zeros((7, 6)) # Defining a matrix to store all moves of the winning player and create a lookup table


def play_with_ui(agent_1, agent_2):

	#Getting the type of the game User wants 
    game_choice = get_input()

    #Setting up UI envirnment

    global FPSCLOCK, DISPLAYSURF, REDPILERECT, BLACKPILERECT, REDTOKENIMG
    global BLACKTOKENIMG, BOARDIMG, ARROWIMG, ARROWRECT, HUMANWINNERIMG
    global COMPUTERWINNERIMG, WINNERRECT, TIEWINNERIMG
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Four in a Row')

    REDPILERECT = pygame.Rect(int(SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
    BLACKPILERECT = pygame.Rect(WINDOWWIDTH - int(3 * SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE,
                                SPACESIZE)
    REDTOKENIMG = pygame.image.load('4row_red.png')
    REDTOKENIMG = pygame.transform.smoothscale(REDTOKENIMG, (SPACESIZE, SPACESIZE))
    BLACKTOKENIMG = pygame.image.load('4row_black.png')
    BLACKTOKENIMG = pygame.transform.smoothscale(BLACKTOKENIMG, (SPACESIZE, SPACESIZE))
    BOARDIMG = pygame.image.load('4row_board.png')
    BOARDIMG = pygame.transform.smoothscale(BOARDIMG, (SPACESIZE, SPACESIZE))

    HUMANWINNERIMG = pygame.image.load('4row_humanwinner.png')
    COMPUTERWINNERIMG = pygame.image.load('4row_computerwinner.png')
    TIEWINNERIMG = pygame.image.load('4row_tie.png')
    WINNERRECT = HUMANWINNERIMG.get_rect()
    WINNERRECT.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    ARROWIMG = pygame.image.load('4row_arrow.png')
    ARROWRECT = ARROWIMG.get_rect()
    ARROWRECT.left = REDPILERECT.right + 10
    ARROWRECT.centery = REDPILERECT.centery

    # Initializing the game parameters 
    red_wins = 0
    black_wins = 0
    tie = 0

    #  Playing the game 
    while True:
        result, state = run_game(agent_1, agent_2, game_choice)
        if result == 1:
            red_wins += 1
        elif result == -1:
            black_wins += 1
        elif result == -2:
            tie += 1
        if state == -1:
            pygame.quit()
            plotResults(red_wins, black_wins, tie)
            sys.exit()


def get_input():
	# Input dialog box prompting game type seletion
    master = Tk()
    master.wm_title("Select the type of game")
    master.minsize(width=400, height=50)
    var = StringVar(master)
    default_choice='Random_Vs_Random' #default choice of game_type
    var.set(default_choice) # initial value
    option = OptionMenu(master, var, "Random_Vs_Random", "Statistical_Vs_Random", "Statistical_Vs_Statistical")
    option.pack()

    def ok():
        global seletion
        # Get the user seletion from the dialog box
        default_choice = var.get()
        seletion = default_choice
        master.destroy()
    
    button = Button(master, text="OK", command=ok) # Button when clicked calls the ok() function which returns user seletion
    button.pack()
    mainloop()
    return seletion


def plotResults(red_wins, black_wins, tie):

    # Adjusting the plot results to not show 0%`s
    def make_autopct(values):
        def my_autopct(pct):
            if pct == 0:
                return ""
            else:
                return '{p:.1f}% '.format(p=pct)

        return my_autopct

    # Setting up plot variables
    labels = ['Red Wins', 'Black Wins', 'Ties']
    sizes = [red_wins, black_wins, tie]
    colors = ['yellowgreen', 'gold', 'lightskyblue']
    explode = (0.1, 0, 0)

    plt.pie(sizes, colors=colors, explode=explode, labels=labels, autopct=make_autopct(sizes), shadow=True,
            startangle=70)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
    print "number of red wins ", red_wins
    print "number of black wins ", black_wins
    print "number of ties ", tie


def run_game(agent_1, agent_2, game_type):
	# Maing Game logic
    turn = HUMAN
    winner = 0 # winner = 1 means player winner = -1 computer.winner = -2 is for tie
    state = 0  # it is -1 when user quits
    # Set up a blank board data structure.
    mainBoard = getNewBoard()

    while True:  # main game loop
        if turn == HUMAN:
            # player's turn.
            if game_type!='Random_Vs_Random':
                board, column = statistical_move(mainBoard, 1)
                animateComputerMoving(mainBoard, column, HUMAN)
            else:
                column = agent_1(mainBoard) #get the column to make next move in
                animateComputerMoving(mainBoard, column, HUMAN) #Animate the move
                status, row = makeMove(mainBoard, RED, column) #make a move and return the row number and status of the playing board

                # check if the move made was the winning move
            if isWinner(mainBoard, RED):
                winnerImg = HUMANWINNERIMG #In case of player Set the image showing game result to player win
                winner = 1
                break
            turn = COMPUTER  # switch to other player's turn
        else:
            # Computer's turn.
            if game_type=='Statistical_Vs_Random' or game_type=='Random_Vs_Random':

                column = agent_2(mainBoard) #get the column to make next move in
                animateComputerMoving(mainBoard, column, COMPUTER) #Animate the move
                status, row = makeMove(mainBoard, BLACK, column)
            else:
                board, column = statistical_move(mainBoard, -1)
                animateComputerMoving(mainBoard, column, COMPUTER)

            # check if the move made was the winning move
            if isWinner(mainBoard, BLACK):
                winnerImg = COMPUTERWINNERIMG #In case of computer Set the image showing game result to computer win
                winner = -1
                break
            turn = HUMAN  # switch to other player's turn

        if isBoardFull(mainBoard):
            # A completely filled board means it's a tie.
            winnerImg = TIEWINNERIMG #In case of tie Set the image showing game result to tie
            winner = -2
            break
    while True:
        # Keep looping until player clicks the mouse or quits.
        drawBoard(mainBoard)
        DISPLAYSURF.blit(winnerImg, WINNERRECT)
        pygame.display.update()
        FPSCLOCK.tick()

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                state = -1
                return winner, state
            elif event.type == MOUSEBUTTONUP:
                return winner, state


def makeMove(board, player, column):
    # Finding the lowest row for the selected column to place the player
    lowest = getLowestEmptySpace(board, column)
    if lowest != -1:
        board[column][lowest] = player
    return board, lowest


def drawBoard(board, extraToken=None):
    # Background Color 
    DISPLAYSURF.fill(BGCOLOR)

    # draw tokens
    spaceRect = pygame.Rect(0, 0, SPACESIZE, SPACESIZE)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
            if board[x][y] == RED:
                DISPLAYSURF.blit(REDTOKENIMG, spaceRect)
            elif board[x][y] == BLACK:
                DISPLAYSURF.blit(BLACKTOKENIMG, spaceRect)

    # draw the extra token
    if extraToken != None:
        if extraToken['color'] == RED:
            DISPLAYSURF.blit(REDTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))
        elif extraToken['color'] == BLACK:
            DISPLAYSURF.blit(BLACKTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))

    # draw board over the tokens
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
            DISPLAYSURF.blit(BOARDIMG, spaceRect)

    # draw the red and black tokens off to the side
    DISPLAYSURF.blit(REDTOKENIMG, REDPILERECT)  # red on the left
    DISPLAYSURF.blit(BLACKTOKENIMG, BLACKPILERECT)  # black on the right


def getNewBoard():
    # Create a new board and initilize all fields to zero
    board = np.zeros((BOARDWIDTH, BOARDHEIGHT))
    return board


def animateDroppingToken(board, column, color):
    x = XMARGIN + column * SPACESIZE
    y = YMARGIN - SPACESIZE
    dropSpeed = INIT_SPEED

    lowestEmptySpace = getLowestEmptySpace(board, column)

    while True:
        y += int(dropSpeed)
        if int((y - YMARGIN) / SPACESIZE) >= lowestEmptySpace:
            return
        drawBoard(board, {'x': x, 'y': y, 'color': color})
        pygame.display.update()
        FPSCLOCK.tick()


def animateComputerMoving(board, column, player):
    if player == COMPUTER:
        color = BLACK
        x = BLACKPILERECT.left
        y = BLACKPILERECT.top
    else:
        color = RED
        x = REDPILERECT.left
        y = REDPILERECT.top
    speed = INIT_SPEED
    # moving the black tile up
    while y > (YMARGIN - SPACESIZE):
        y -= int(speed)
        # speed += 0.5
        drawBoard(board, {'x': x, 'y': y, 'color': color})
        pygame.display.update()
        FPSCLOCK.tick()
    # moving the black tile over
    y = YMARGIN - SPACESIZE
    speed = INIT_SPEED
    while x * player < player * (XMARGIN + column * SPACESIZE):
        x += player * int(speed)
        # speed += 0.5
        drawBoard(board, {'x': x, 'y': y, 'color': color})
        pygame.display.update()
        FPSCLOCK.tick()
    # dropping the black tile
    animateDroppingToken(board, column, color)


def getComputerMove(board):
    # pick a random column number which is Valid 
    while True:
        x = random.randint(0, 6)
        if isValidMove(board, x):
            return x


def getLowestEmptySpace(board, column):
    # Return the row number of the lowest empty row in the given column.
    for y in range(BOARDHEIGHT - 1, -1, -1):
        if board[column][y] == EMPTY:
            return y
    return -1


def statistical_move(board, player):
    # getting the next best move by choosing a valid row and col combination which was used the most in lookup  
    valid_column_moves = []
    valid_row_moves = []
    maximum_value = 0
    # getting all the valid column possible moves
    for x in range(7):
        if isValidMove(board, x):
            valid_row_moves.append(x)
    test = np.load("test_table.npy")
    
    # find all the valid moves
    for i in range(7):
        lowest = getLowestEmptySpace(board, i)
        if lowest != -1:
            valid_column_moves.append(lowest)
        else:
            valid_column_moves.append(-1)

    # go through all the valid moves and find the one with the largest value 
    for y in range(len(valid_column_moves)):
        if valid_column_moves[y] != -1:
            if maximum_value < test[y][valid_column_moves[y]]:
                maximum_value = test[y][valid_column_moves[y]]
                max_row = y
                max_column = valid_column_moves[y]
            
    board[max_row][max_column] = player

    # return the valid move with the highest value along with board state
    return board, max_column


def isValidMove(board, column):
    # Returns True if there is an empty space in the given column.
    # Otherwise returns False.
    if column < 0 or column >= (BOARDWIDTH) or board[column][0] != EMPTY:
        return False
    return True


def isBoardFull(board):
    # Returns True if there are no empty spaces anywhere on the board.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == EMPTY:
                return False
    return True


def isWinner(board, tile): #Checks if the move was the winning move
    # check horizontal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT):
            if board[x][y] == tile and board[x + 1][y] == tile and board[x + 2][y] == tile and board[x + 3][y] == tile:
                return True
    # check vertical spaces
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x][y + 1] == tile and board[x][y + 2] == tile and board[x][y + 3] == tile:
                return True
    # check / diagonal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(3, BOARDHEIGHT):
            if board[x][y] == tile and board[x + 1][y - 1] == tile and board[x + 2][y - 2] == tile and board[x + 3][
                        y - 3] == tile:
                return True
    # check \ diagonal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x + 1][y + 1] == tile and board[x + 2][y + 2] == tile and board[x + 3][
                        y + 3] == tile:
                return True
    return False


def play_without_ui(agent_1, agent_2):
    # Set up a blank board data structure.
    board = getNewBoard()
    player = 1

    # temporary lookup matrixs to store moves of both player , after a non tie game moves of the winner are used to
    # increment the main lookup table 
    lookup1 = np.zeros((7, 6))
    lookup2 = np.zeros((7, 6))
    while True:  # main game loop
        if player == 1:
            # Human player's turn.
            column = agent_1(board)
            state, row = makeMove(board, player, column)
            lookup1[column][row] += 1
        else:
            column = agent_2(board)
            state, row = makeMove(board, player, column)
            lookup2[column][row] += 1
        if wasWinningMove(board, player, column):
            build_lookup_table(player, lookup1, lookup2)
            return player
        player *= -1  # switch to other player's turn
        if isBoardFull(board):
            # A completely filled board means it's a tie.
            return 0


def build_lookup_table(player, lookup1, lookup2):
    # add all the moves of the winning player to build a lookup table
    for x in range(7):
        for y in range(6):
            if player == 1:
                lookup[x][y] += lookup1[x][y]
            else:
                lookup[x][y] += lookup2[x][y]


def learn_from_random_play(iterations):
    # randomly plays the game and saves the lookup table 
    # which is the number of times a field was used by the winning player
    for i in range(iterations):
        play_without_ui(getComputerMove, getComputerMove)
    np.save("lookup.npy", lookup)


#
def generate_statistics(agent_1, agent_2, iterations):
    red_wins = 0
    black_wins = 0
    tie = 0
    game_type = get_input()
    print game_type
    for i in range(iterations):
        result = gather_stats(agent_1, agent_2, game_type)
        if result == 1:
            red_wins += 1
        elif result == -1:
            black_wins += 1
        elif result == -2:
            tie += 1
    pygame.quit()
    plotResults(red_wins, black_wins, tie)


def gather_stats(agent_1, agent_2, game_choice):
    turn = HUMAN
    winner = 0
    state = 0
    lookup1 = np.zeros((7, 6))
    lookup2 = np.zeros((7, 6))
    # Set up a blank board data structure.
    mainBoard = getNewBoard()

    while True:  # main game loop
        if turn == HUMAN:
            # Human player's turn.
            if game_choice!='Random_Vs_Random':
                board, column = statistical_move(mainBoard, 1)
            else:
                column = agent_1(mainBoard)
                status, row = makeMove(mainBoard, RED, column)

            if isWinner(mainBoard, RED):
                # winnerImg = HUMANWINNERIMG
                winner = 1
                break
            turn = COMPUTER  # switch to other player's turn
        else:
            # Computer player's turn.
            # board, column = statistical_move(mainBoard, -1)
            if game_choice=='Statistical_Vs_Statistical':
                board, column = statistical_move(mainBoard, -1)
            else:
                column = agent_2(mainBoard)
                status, row = makeMove(mainBoard, BLACK, column)

            if isWinner(mainBoard, BLACK):
                # winnerImg = COMPUTERWINNERIMG
                winner = -1
                break
            turn = HUMAN  # switch to other player's turn

        if isBoardFull(mainBoard):
            # A completely filled board means it's a tie.
            winner = -2
            break
    return winner


if __name__ == '__main__':
    # learn_from_random_play(10000)
    # generate_statistics(getComputerMove, getComputerMove, 10000)
    play_with_ui(getComputerMove, getComputerMove)
