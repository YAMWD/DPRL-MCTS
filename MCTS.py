import numpy as np
import copy
import matplotlib.pyplot as plt

class Node:
    def __init__(self, board, parent = None):

        self.board = board
        self.num_simulations = 0
        self.num_wins = 0
        self.c = np.sqrt(2)
        self.parent = parent
        self.children = []
    
        action_list = self.get_action_list()

        for action in action_list:

            inter_next_state = self.make_move(cur_player = 1, action = action)
            inter_next_node = Node(inter_next_state)

            next_action_list = inter_next_node.get_action_list()
            if len(next_action_list):
                for next_action in next_action_list:
                    next_state = inter_next_node.make_move(cur_player = 2, action = next_action)
                    next_node = Node(next_state, parent = self)
                    self.children.append(next_node)
            else:
                self.children.append(inter_next_node)

    def get_win_rate(self):
        return self.num_wins / self.num_simulations if self.num_simulations else 0

    def get_scores(self):    
        return [child.num_wins / child.num_simulations + self.c * np.sqrt(np.log(self.num_simulations) / child.num_simulations) if child.num_simulations else np.inf for child in self.children]

    def get_action_list(self):
        action_list = []

        #Check if it is leaf node
        if((not self.check_playable()) or self.check_board()):
            return action_list

        for i in range(7):
            if(self.check_mobility(i)):
                action_list.append(i)
        return action_list

    def check_child(self, board):
        # Check if next board states exists in current children
        for child in self.children:
            if (child.board == board).all:
                return child

        return False

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

    def check_playable(self):
        #if no 0 in the board it means there is no room for next step
        return 0 in self.board

    def make_move(self, cur_player, action):
        cur_board = copy.deepcopy(self.board)
        pos = np.where(cur_board[:, action] == 0)[0][-1]
        cur_board[:, action][pos] = cur_player

        return cur_board

class MCT:
    def __init__(self, board):
        self.init_node = Node(board)

    def selection(self, node, method = None):
        #Check if it is leaf node
        if((not node.check_playable()) or node.check_board()):
            return node

        if(method == 'random'):
            action_list = node.get_action_list()
            action = np.random.choice(action_list)
            return action

        # selection based on UCB rule
        scores = node.get_scores()
        return node.children[np.argmax(scores)]

    def expand(self, child):
        return self.selection(child)

    def rollout(self, node):
        cur_node = node
        cur_player = 1
        while(cur_node.check_playable() and (not cur_node.check_board())):
            action = self.selection(cur_node, method = 'random')
            next_state = cur_node.make_move(cur_player = cur_player, action = action)
            cur_node = Node(next_state)
            if(cur_player == 1):
                cur_player = 2
            else:
                cur_player = 1
        
        result = cur_node.check_board() == 1
        self.back_prop(node, result)

    def back_prop(self, node, result):
        node.num_wins += result
        node.num_simulations += 1
        if(node.parent != None):
            self.back_prop(node.parent, result)
            

    def search(self, node):
        #Check if it is leaf node
        if((not node.check_playable()) or node.check_board()):
            return

        child = self.selection(node)

        if child.num_simulations:
            next_child = self.expand(child)
            self.rollout(next_child)
        else:
            self.rollout(child)
        
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
    prev_win_rate = -2
    cur_win_rate = -1
    ths = 1e-5
    '''
    while np.abs(cur_win_rate - prev_win_rate) >= ths:
        test.search(test.init_node)
        prev_win_rate = cur_win_rate
        cur_win_rate = test.init_node.get_win_rate()
        print(prev_win_rate, cur_win_rate)
    '''

    win_rates = []
    for i in range(1000):
        test.search(test.init_node)
        win_rate = test.init_node.get_win_rate()
        win_rates.append(win_rate)
        print(win_rate)
    
    plt.plot(range(len(win_rates)), win_rates)
    plt.show()

