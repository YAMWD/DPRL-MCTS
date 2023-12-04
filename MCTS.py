import numpy as np
import copy

class Node:
    def __init__(self, board, parent = None):

        self.board = board
        self.num_simulations = 0
        self.num_wins = 0
        self.c = np.sqrt(2)
        self.parent = parent
        self.children = []
    
    def get_win_rate(self):
        return self.num_wins / self.num_simulations if self.num_simulations else 0

    def get_scores(self):    
        return [child.num_wins / child.num_simulations + self.c * np.sqrt(np.log(self.num_simulations) / child.num_simulations) for child in self.children]

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
        # selection based on UCB rule
        scores = node.get_scores()

        if(len(scores) == 0 or method == 'random'):
            action_list = []
            for i in range(7):
                if(node.check_mobility(i)):
                    action_list.append(i)
            action = np.random.choice(action_list)
        else:
            action = np.argmax(scores)
        
        return action

    def expand(self, node, next_node):
        node.children.append(next_node)

    def rollout(self, node):
        cur_node = copy.deepcopy(node)
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

        action = self.selection(node)

        inter_next_state = node.make_move(cur_player = 1, action = action)
        inter_next_node = Node(inter_next_state)

        next_action = self.selection(inter_next_node)
        next_state = inter_next_node.make_move(cur_player = 2, action = next_action)
        next_node = Node(next_state, parent = node)

        child = node.check_child(next_state)
        if(isinstance(child, bool)):
            self.expand(node, next_node)
            self.rollout(next_node)
            self.search(next_node)
        else:
            self.rollout(next_node)
            self.search(child)
        
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

    for i in range(10000):
        test.search(test.init_node)
        print(test.init_node.get_win_rate())
