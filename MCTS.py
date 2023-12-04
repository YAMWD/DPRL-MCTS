import numpy as np

class MCT:
    def __init__(self, board):
        self.board = board

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
        pos = np.where(self.board[:, action] == 0)[0][-1]
        self.board[:, action][pos] = cur_player

    def MCTS(self):
        return 0

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

    print(test.check_board())
    
    if(test.check_mobility(action = 0)):

        test.make_move(cur_player = 1, action = 0)

        print(test.board)
