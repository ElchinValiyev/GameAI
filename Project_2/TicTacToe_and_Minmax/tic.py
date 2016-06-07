from Board import BoardImplementation as Board
import numpy as np


def build_tree():
    branch_number = []  # for branching factor calculation
    winners = [0, 0, 0]  # draw,x,o
    leaf_nodes = [0]
    nodes = [1]
    init_board = Board()

    # init_board.make_move((0, 0))
    # init_board.make_move((2, 1))
    # init_board.make_move((1, 1))
    # init_board.make_move((2, 2))
    # init_board.make_move((0, 1))

    unique_gamestates = set()  # unique boards
    unique_gamestates.add(str(init_board.state))
    unique_draw = set()

    def traverse(board):
        xs, ys = board.get_moves()
        if xs.size == 0:  # no moves possible
            nodes[0] += 1
            leaf_nodes[0] += 1
            unique_draw.add(str(board.state))
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
                    leaf_nodes[0] += 1
                    winners[new_board.player] += 1
                else:
                    traverse(new_board)

    traverse(init_board)

    print  np.mean([n for n in branch_number if n != 1])
    print  winners
    print leaf_nodes
    print nodes
    print  len(unique_gamestates)
    print len(unique_draw)


tree = build_tree()
print tree
