import fourinarow as c4
import numpy as np,time

Depth=2


def init_board():
	board = [[0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,-1,-1], [0,0,0,0,1,-1], [0,0,1,-1,-1,1], [0,0,0,0,0,-1] ,[0,0,0,0,0,1]]
	return board

def display_board(board):
	print np.matrix(board)

if __name__ == '__main__':
	board = init_board()
	display_board(board)
	column = c4.getComputerMove(Depth, board,1)
	state = c4.makeMove(board,1, column)
	time.sleep(1)
	print "\n\n Updated Board"
	display_board(board)

