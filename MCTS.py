import numpy as np
import copy

class Node:
    def __init__(self, board):

        self.board = board

        self.num_simu = 0
        
        self.num_wins = 0

        self.c = np.sqrt(2)

        self.child = []

    def check_board(self):
        # Check horizontally
        for row in self.board:
            for col in range(len(row) - 3):
                if row[col] == row[col + 1] == row[col + 2] == row[col + 3] != 0:
                    return row[col]

        # Check vertically
        for col in range(len(self.board[0])):
            for row in range(len(self.board) - 3):
                if self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col] == self.board[row + 3][col] != 0:
                    return self.board[row][col]

        # Check diagonally (positive slope)
        for row in range(len(self.board) - 3):
            for col in range(len(self.board[0]) - 3):
                if self.board[row][col] == self.board[row + 1][col + 1] == self.board[row + 2][col + 2] == self.board[row + 3][col + 3] != 0:
                    return self.board[row][col]

        # Check diagonally (negative slope)
        for row in range(3, len(self.board)):
            for col in range(len(self.board[0]) - 3):
                if self.board[row][col] == self.board[row - 1][col + 1] == self.board[row - 2][col + 2] == self.board[row - 3][col + 3] != 0:
                    return self.board[row][col]

        # No win found
        return 0

    def check_mobility(self, action):
        return 0 in self.board[:, action]

    def make_move(self, cur_player, action):
        cur_board = copy.deepcopy(self.board)
        pos = np.where(cur_board[:, action] == 0)[0][-1]
        cur_board[:, action][pos] = cur_player

        return cur_board

class MCT:
    def __init__(self, board):
        self.init_node = Node(board)

    def search(self):
    
        print(self.init_node.check_board())
        
        if(self.init_node.check_mobility(action = 0)):
            next_state = self.init_node.make_move(cur_player = 1, action = 0)
            print(next_state)

if __name__ == '__main__':

    board = np.array([
        [0, 1, 2, 2, 1, 2, 0],
        [0, 1, 1, 2, 2, 1, 0],
        [0, 2, 2, 2, 1, 2, 0],
        [0, 1, 1, 1, 2, 1, 0],
        [0, 1, 2, 2, 1, 2, 0],
        [2, 1, 1, 1, 2, 2, 1]
    ])

    test = MCT(board)

    test.search()
