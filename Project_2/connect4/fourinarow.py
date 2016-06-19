from Tkinter import *
import matplotlib.pyplot as plt
import pygame,numpy as np,time
from pygame.locals import *
import random
import pyprind

BOARDWIDTH = 7  # how many spaces wide the board is
BOARDHEIGHT = 6  # how many spaces tall the board is
assert BOARDWIDTH >= 4 and BOARDHEIGHT >= 4, 'Board must be at least 4x4.'

INIT_SPEED = 4  # Speed with which User tokens move
SPACESIZE = 50  # size of the tokens and individual board spaces in pixels
WINDOWWIDTH = 520  # width of the program's window, in pixels
WINDOWHEIGHT = 480  # height in pixels

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * SPACESIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - BOARDHEIGHT * SPACESIZE) / 2)

Custom_Color = (50, 50, 155)
WHITE = (255, 255, 255)
BGCOLOR = Custom_Color
TEXTCOLOR = WHITE

# Depth=2
RED = 1
BLACK = -1
EMPTY = 0
HUMAN = 1
COMPUTER = -1


def play_with_ui(agent_1, agent_2):

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
	depth = get_input()

	# Initializing the game parameters 
	red_wins = 0
	black_wins = 0
	tie = 0

	#  Game Loop
	while True:
		result, state = run_game(agent_1, agent_2,int(depth))
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
	master.wm_title("Select the depth for minimax")
	master.minsize(width=400, height=50)
	var = StringVar(master)
	default_choice='1' #default choice of game_type
	var.set(default_choice) # initial value
	option = OptionMenu(master, var, "1","2","3")
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
	explode = (0.1, 0, 0.5)

	plt.pie(sizes, colors=colors, explode=explode, labels=labels, autopct=make_autopct(sizes), shadow=True,
			startangle=70)
	plt.axis('equal')
	plt.tight_layout()
	plt.show()
	print "number of red wins ", red_wins
	print "number of black wins ", black_wins
	print "number of ties ", tie
	print "Depth ",depth


def run_game(agent_1, agent_2,depth):
	# Maing Game logic
	turn = HUMAN
	winner = 0 # winner = 1 means player winner = -1 computer.winner = -2 is for tie
	state = 0  # it is -1 when user quits
	# Set up a blank board data structure.
	mainBoard = getNewBoard()

	while True:  # main game loop
		if turn == HUMAN:
			# player's turn.
			column,bestValue=minimax(mainBoard,depth,True,0,1)#get the column to make next move in
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

			column  = getRandomMove(mainBoard)#agent_2(Depth,mainBoard,-1) #get the column to make next move in
			animateComputerMoving(mainBoard, column, COMPUTER) #Animate the move
			status = makeMove(mainBoard, BLACK, column)

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
	# print "required column is ", column
	lowest = getLowestEmptySpace(board, column)
	if lowest != -1:
		board[column][lowest] = player
	return board

def minimax(node, depth, maximizingPlayer,column,player1):
	#Check if the move was a winning move
	if maximizingPlayer:
		current_player=1
	else:current_player=-1

	if isWinner(node,player1):
	    return column,9999999
	elif isWinner(node,player1*-1):
	    return column,-9999999   

	if depth == 0 or isBoardFull(node):
		return evaluate(player1,node,column)
    
	best_move = None		
	tupleList= []
	for i in range(BOARDWIDTH):
		# if column i is a legal move...
		if isValidMove(node,i):
			temp = make_temporary_move(node,current_player,i)
			tupleTable = (i,temp) # Store All possible moves and their respective columns
			tupleList.append(tupleTable)

	if maximizingPlayer:
	    bestValue = float('-inf')
	    for i,j in tupleList:	# Make all valid moves and choose the move with highest reward
	        current_move,current_value = minimax(j, depth - 1, False,i,player1)
	        # print "\n",np.matrix(j),"   ",current_value,"\n"
	        # time.sleep(2)
	        if(bestValue<current_value):
	        	bestValue=current_value
	        	best_move= i 	

	else: #Minimizer
	    bestValue = float('inf')
	    for x,y in tupleList: # Make all valid moves
	        current_move,current_value = minimax(y, depth - 1, True,x,player1)
	        # print "\n",np.matrix(y),"   ",current_value,"\n"
	        # time.sleep(2)
	        if(bestValue>current_value):
	        	bestValue=current_value
	        	best_move = x
	return best_move,bestValue

def evaluate(player1,node,column):
	#Simple heuristic for evaluation
    opp_player=player1*-1
    my_threes = checkForOpenStreak(node,player1, 3)
    my_twos = checkForOpenStreak(node,player1, 2)
    opp_fours = checkForOpenStreak(node,opp_player, 4)
    opp_threes = checkForOpenStreak(node,opp_player, 3)
    opp_twos = checkForOpenStreak(node,opp_player, 2) 
    value=(my_threes*100 + my_twos) - (opp_threes *50)
    return column,value


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
	board = []
	for x in range(BOARDWIDTH):
		board.append([0]*BOARDHEIGHT)
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
		x = random.randint(0, BOARDHEIGHT)
		if isValidMove(board, x):
			return x


def make_temporary_move(state,player,column):
	temp = [x[:] for x in state]
	lowest = getLowestEmptySpace(temp, column)
	if lowest != -1:
		temp[column][lowest] = player
	return temp

		
def checkForOpenStreak(state, color, streak):
	count = 0
	# for each piece in the board...
	for i in range(BOARDWIDTH):
		for j in range(BOARDHEIGHT):
			# ...that is of the color we're looking for...
			if state[i][j] == color:
				# check if a vertical streak starts at (i, j)
				count += verticalStreak(i, j, state,color,streak)
				
				# check if a horizontal four-in-a-row starts at (i, j)
				count += horizontalStreak(i, j, state,color, streak)
				
				# check if a diagonal (either way) four-in-a-row starts at (i, j)
				count += diagonalCheck(i, j, state,color,streak)
	# return the sum of streaks of length 'streak'
	return count
		
def verticalStreak(row, col, state,color, streak):
	consecutiveCount = 0
	open_streak=False
	for i in range(row, BOARDWIDTH):
		if state[i][col] == color:
			consecutiveCount += 1
		else:
			break
	if consecutiveCount >= streak:
		return 1
	else:
		return 0

def horizontalStreak(row, col, state,color, streak):
	consecutiveCount = 0
	open_streak=False
	for j in range(col,-1,-1):
		if state[row][j] == color:
			consecutiveCount += 1
		else:
			break
	if consecutiveCount >= streak:
		return 1
	else:
		return 0

def diagonalCheck(row, col, state,color, streak):

	total = 0
	
	# check for diagonals with negative slope
	consecutiveCount = 0
	open_streak=False
	j = col
	for i in range(row,BOARDHEIGHT):
		if j >5:
			break
		elif state[i][j] == color:
			consecutiveCount += 1
		else:
			break
		j += 1 # increment column when row is incremented

	if consecutiveCount >= streak:
		total += 1


	consecutiveCount = 0
	open_streak=False
	j = col
	for i in range(row,BOARDHEIGHT):
		if j <0:
			break
		elif state[i][j] == color:
			consecutiveCount += 1
		else:
			break
		j -= 1 # increment column when row is incremented

	if consecutiveCount >= streak:
		total += 1		

	return total


def getLowestEmptySpace(board, column):
	# Return the row number of the lowest empty row in the given column.
	# print column
	for y in range(BOARDHEIGHT - 1, -1, -1):
		if board[column][y] == 0:
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


def generate_statistics(agent_1, agent_2, iterations):
	red_wins = 0
	black_wins = 0
	tie = 0
	depth = get_input()
	my_perc = pyprind.ProgPercent(iterations, stream=2)
	for i in range(iterations):
		my_perc.update()
		result = gather_stats(agent_1, agent_2, int(depth))
		if result == 1:
			red_wins += 1
		elif result == -1:
			black_wins += 1
			# break
		elif result == -2:
			tie += 1
	pygame.quit()
	plotResults(red_wins, black_wins, tie)


def gather_stats(agent_1, agent_2, depth):
	turn = HUMAN
	winner = 0
	state = 0

	# Set up a blank board data structure.
	mainBoard = getNewBoard()

	while True:  # main game loop
		if turn == HUMAN:
			# Human player's turn.

			column,bestValue = minimax(mainBoard,depth,True,0,1)
			# print "column received here ", column
			status = makeMove(mainBoard, RED, column)

			if isWinner(mainBoard, RED):
				# winnerImg = HUMANWINNERIMG
				winner = 1
				break
			turn = COMPUTER  # switch to other player's turn
		else:
			# Computer player's turn.
			# board, column = statistical_move(mainBoard, -1)
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
    generate_statistics(minimax, getRandomMove,1000)
    # play_with_ui(minimax, getRandomMove)