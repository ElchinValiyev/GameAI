from Board import BoardImplementation as Board
import numpy as np


def build_tree():
    branch_number = []  # for branching factor calculation
    winners = [0, 0, 0]  # draw,x,o
    nodes = [1]  # counter of tree nodes
    init_board = Board()

    unique_gamestates = set()  # unique boards
    unique_gamestates.add(str(init_board.state))

    def traverse(board):
        xs, ys = board.get_moves()
        if xs.size == 0:  # no moves possible
            winners[0] += 1  # record the draw
            return
        else:
            branch_number.append(xs.size)
            for i in range(xs.size):
                new_board = board.copy()
                new_board.make_move((xs[i], ys[i]))
                nodes[0] += 1
                unique_gamestates.add(str(new_board.state))
                # If was winning move record winner
                # No need to go down that branch
                if new_board.game_is_over():
                    winners[new_board.player] += 1
                else:
                    traverse(new_board)

    traverse(init_board)

    print "Branching factor: " + str(np.mean([n for n in branch_number if n != 1]))
    print "X wins: " + str(winners[1]) + "  O wins: " + str(winners[-1]) + "  Draws: " + str(winners[0])
    print "Leaf nodes: " + str(np.sum(winners))
    print "Number of nodes in game: " + str(nodes[0])
    print "Unique gamestates: " + str(len(unique_gamestates))


if __name__ == '__main__':
    build_tree()
