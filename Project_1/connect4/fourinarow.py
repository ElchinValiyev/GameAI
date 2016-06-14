import matplotlib.pyplot as plt
import numpy as np
import pygame
import random
import time
from Tkinter import *
from pygame.locals import *
import copy

BOARDWIDTH = 7  # how many spaces wide the board is
BOARDHEIGHT = 6  # how many spaces tall the board is
assert BOARDWIDTH >= 4 and BOARDHEIGHT >= 4, 'Board must be at least 4x4.'

INIT_SPEED = 10  # Speed with which User tokens move
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

Depth=3
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
                row, column = statistical_move(mainBoard, 1)
                animateComputerMoving(mainBoard, column, HUMAN)
                mainBoard[column][row] = 1 #make the move
            else:
                column = agent_1(Depth,mainBoard,1) #get the column to make next move in
                print type(column)
                animateComputerMoving(mainBoard, column, HUMAN) #Animate the move
                status = makeMove(mainBoard, RED, column) #make a move and return the row number and status of the playing board

                # check if the move made was the winning move
            if isWinner(mainBoard, RED):
                winnerImg = HUMANWINNERIMG #In case of player Set the image showing game result to player win
                winner = 1
                break
            turn = COMPUTER  # switch to other player's turn
        else:
            # Computer's turn.
            if game_type=='Statistical_Vs_Random' or game_type=='Random_Vs_Random':

                column  = getRandomMove(mainBoard)#agent_2(Depth,mainBoard,-1) #get the column to make next move in
                animateComputerMoving(mainBoard, column, COMPUTER) #Animate the move
                status = makeMove(mainBoard, BLACK, column)
            else:
                row, column = statistical_move(mainBoard, -1)
                animateComputerMoving(mainBoard, column, COMPUTER)
                mainBoard[column][row] = -1 #make the move

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
    return board


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
        drawBoard(board, {'x': x, 'y': y, 'color': color})
        pygame.display.update()
        FPSCLOCK.tick()
    # moving the black tile over
    y = YMARGIN - SPACESIZE
    speed = INIT_SPEED
    while x * player < player * (XMARGIN + column * SPACESIZE):
        x += player * int(speed)
        drawBoard(board, {'x': x, 'y': y, 'color': color})
        pygame.display.update()
        FPSCLOCK.tick()
    # dropping the black tile
    animateDroppingToken(board, column, color)


def getRandomMove(board):
    # pick a random column number which is Valid 
    while True:
        x = random.randint(0, 6)
        if isValidMove(board, x):
			return x
def getComputerMove(depth, state, curr_player):
    """ Returns the best move (as a column number) and the associated alpha
        Calls search()
    """
    
    # determine opponent's color
    if curr_player == 1:
        opp_player = -1
    else:
        opp_player = 1
    
    # enumerate all legal moves
    legal_moves = {} # will map legal move states to their alpha values
    for col in range(6):
        # if column i is a legal move...
        if isValidMove(state,col):
            # make the move in column 'col' for curr_player
            dupeBoard = copy.deepcopy(state)
            temp = makeMove(dupeBoard,curr_player,col)
            legal_moves[col] = -search(depth-1, temp, opp_player)
    
    best_alpha = -99999999
    best_move = None
    moves = legal_moves.items()
    random.shuffle(list(moves))
    for move, alpha in moves:
        if alpha >= best_alpha:
            best_alpha = alpha
            best_move = move
    return best_move       



def search(depth, state, curr_player):
    """ Searches the tree at depth 'depth'
        By default, the state is the board, and curr_player is whomever 
        called this search
        
        Returns the alpha value
    """
    
    # enumerate all legal moves from this state
    legal_moves = []
    for i in range(6):
        # if column i is a legal move...
        if isValidMove(state,i):
            # make the move in column i for curr_player
            dupeBoard2 = copy.deepcopy(state)
            temp = makeMove(dupeBoard2,curr_player,i)
            legal_moves.append(temp)
    
    # if this node (state) is a terminal node or depth == 0...
    if depth == 0 or len(legal_moves) == 0 or gameIsOver(state) or isBoardFull(state):
        # return the heuristic value of node
        return value(state, curr_player)
    
    # determine opponent's color
    if curr_player == 1:
        opp_player = -1
    else:
        opp_player = 1

    alpha = -99999999
    for child in legal_moves:
        if child is not None:
        	alpha = max(alpha, -search(depth-1, child, opp_player))
        else:
        	print("child == None (search)")
        
    return alpha    


def gameIsOver(state):
    if checkForStreak(state, 1, 4) >= 1:
        return True
    elif checkForStreak(state, -1, 4) >= 1:
        return True
    else:
        return False

def value(state, color):
    """ Simple heuristic to evaluate board configurations
    """
    if color == 1:
        o_color = -1
    else:
        o_color = 1
    
    my_fours = checkForStreak(state, color, 4)
    my_threes = checkForStreak(state, color, 3)
    my_twos = checkForStreak(state, color, 2)
    opp_fours = checkForStreak(state, o_color, 4)
    opp_threes = checkForStreak(state, o_color, 3)
    opp_twos = checkForStreak(state, o_color, 2)
    if opp_fours > 0:
        return -99999999
    # elif opp_threes>0:
    # 	return -1000	
    else:
        return my_fours*99999999 + my_threes*975 +my_twos*2 -(opp_twos*5 + opp_threes *2550)
        
def checkForStreak(state, color, streak):
    count = 0
    # for each piece in the board...
    for i in range(7):
        for j in range(6):
            # ...that is of the color we're looking for...
            if state[i][j] == color:
                # check if a vertical streak starts at (i, j)
                count += verticalStreak(i, j, state, streak)
                
                # check if a horizontal four-in-a-row starts at (i, j)
                count += horizontalStreak(i, j, state, streak)
                
                # check if a diagonal (either way) four-in-a-row starts at (i, j)
                count += diagonalCheck(i, j, state, streak)
    # return the sum of streaks of length 'streak'
    return count
        
def verticalStreak(row, col, state, streak):
    consecutiveCount = 0
    for i in range(row, 7):
        if state[i][col] == state[row][col]:
            consecutiveCount += 1
        else:
            break

    if consecutiveCount >= streak:
        return 1
    else:
        return 0

def horizontalStreak(row, col, state, streak):
    consecutiveCount = 0
    for j in range(col, 6):
        if state[row][j] == state[row][col]:
            consecutiveCount += 1
        else:
            break

    if consecutiveCount >= streak:
        return 1
    else:
        return 0

def diagonalCheck(row, col, state, streak):

    total = 0
    # check for diagonals with positive slope
    consecutiveCount = 0
    j = col
    for i in range(row, 5):
        if j > 5:
            break
        elif state[i][j] == state[row][col]:
            consecutiveCount += 1
        else:
            break
        j += 1 # increment column when row is incremented
        
    if consecutiveCount >= streak:
        total += 1

    # check for diagonals with negative slope
    consecutiveCount = 0
    j = col
    for i in range(row, -1, -1):
        if j > 5:
            break
        elif state[i][j] == state[row][col]:
            consecutiveCount += 1
        else:
            break
        j += 1 # increment column when row is incremented

    if consecutiveCount >= streak:
        total += 1

    return total


def getLowestEmptySpace(board, column):
    # Return the row number of the lowest empty row in the given column.
    for y in range(BOARDHEIGHT - 1, -1, -1):
        if board[column][y] == EMPTY:
            return y
    return -1


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
    consecutiveCount = 0
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


def generate_statistics(agent_1, agent_2, iterations):
    red_wins = 0
    black_wins = 0
    tie = 0
    game_type = get_input()
    print game_type
    for i in range(iterations):
    	print i
        result = gather_stats(agent_1, agent_2, game_type)
        if result == 1:
            red_wins += 1
        elif result == -1:
            black_wins += 1
            # break
        elif result == -2:
            tie += 1
    pygame.quit()
    plotResults(red_wins, black_wins, tie)


def gather_stats(agent_1, agent_2, game_choice):
    turn = HUMAN
    winner = 0
    state = 0

    # Set up a blank board data structure.
    mainBoard = getNewBoard()

    while True:  # main game loop
        if turn == HUMAN:
            # Human player's turn.
            if game_choice!='Random_Vs_Random':
                board, column = statistical_move(mainBoard, 1)
            else:
                column = agent_1(Depth,mainBoard,1)
                status = makeMove(mainBoard, RED, column)

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
                status = makeMove(mainBoard, BLACK, column)

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
    generate_statistics(getComputerMove, getRandomMove,500)
    # play_with_ui(getComputerMove, getComputerMove)
    # valid_column_moves = []
    # board = getNewBoard()
    # for i in range(7):
    # 	lowest = getLowestEmptySpace(board, i)
    # 	if lowest != -1:
    #     	valid_column_moves.append(lowest)
    # 	else:
    #     	valid_column_moves.append(-1)
    # print valid_column_moves    	