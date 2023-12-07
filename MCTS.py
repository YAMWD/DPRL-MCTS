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

    def selection(self, node):
        #Check if it is leaf node
        if len(node.children) == 0:
            return node

        # selection based on UCB rule
        scores = node.get_scores()
        return self.selection(node.children[np.argmax(scores)])

    def expand(self, node):
        action_list = node.get_action_list()

        for action in action_list:

            inter_next_state = node.make_move(cur_player = 1, action = action)
            inter_next_node = Node(inter_next_state, parent = node)

            next_action_list = inter_next_node.get_action_list()
            if len(next_action_list):
                for next_action in next_action_list:
                    next_state = inter_next_node.make_move(cur_player = 2, action = next_action)
                    next_node = Node(next_state, parent = node)
                    node.children.append(next_node)
            else:
                node.children.append(inter_next_node)    

    def rollout(self, node):
        cur_node = node
        cur_player = 1
        while(cur_node.check_playable() and (not cur_node.check_board())):
            action_list = cur_node.get_action_list()
            action = np.random.choice(action_list)
            next_state = cur_node.make_move(cur_player = cur_player, action = action)
            cur_node = Node(next_state)
            if(cur_player == 1):
                cur_player = 2
            else:
                cur_player = 1
        
        result = cur_node.check_board() == 1
        return result 

    def back_prop(self, node, result):
        node.num_wins += result
        node.num_simulations += 1
        if(node.parent != None):
            self.back_prop(node.parent, result)
            
    def search(self, node):
        if len(node.children) == 0:
            self.expand(node)

        child = self.selection(node)

        if child.num_simulations:
            self.expand(child)
            next_child = self.selection(child)
            result = self.rollout(next_child)
            self.back_prop(next_child, result)
        else:
            result = self.rollout(child)
            self.back_prop(child, result)

def print_tree(node, cur_depth = 0, max_depth = 0x3f3f3f):
    if cur_depth >= max_depth:
        return

    print(cur_depth, node.get_win_rate(), '\n', node.board)
    for child in node.children:
        print_tree(child, cur_depth + 1, max_depth)

def plot_board(board):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_axis_off()

    for i in range(7):
        for j in range(6):
            # Draw the circles representing the pieces
            circle = plt.Circle((i + 0.5, j + 0.5), 0.4, color='white', ec='black')
            ax.add_patch(circle)

            # Fill the circle based on the player's move
            if board[j, i] == 1:
                circle = plt.Circle((i + 0.5, j + 0.5), 0.4, color='red', ec='black')
                ax.add_patch(circle)
            elif board[j, i] == 2:
                circle = plt.Circle((i + 0.5, j + 0.5), 0.4, color='yellow', ec='black')
                ax.add_patch(circle)

    plt.xlim(0, 7)
    plt.ylim(0, 6)
    plt.gca().invert_yaxis()  # Invert the y-axis to start from the bottom

    # Create legend
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label='Player1', markerfacecolor='red', markersize=10),
                       plt.Line2D([0], [0], marker='o', color='w', label='Player2', markerfacecolor='yellow', markersize=10)]

    ax.legend(handles = legend_elements, loc = 'upper left', bbox_to_anchor=(1, 1))
    plt.savefig('plots/init_board.pdf', bbox_inches = 'tight')

if __name__ == '__main__':

    board = np.array([
        [0, 1, 2, 2, 1, 2, 0],
        [0, 1, 1, 2, 2, 1, 0],
        [0, 2, 2, 2, 1, 2, 0],
        [0, 1, 1, 1, 2, 1, 0],
        [0, 1, 2, 2, 1, 2, 0],
        [2, 1, 1, 1, 2, 2, 1]
    ])

    # plot_board(board)
    test = MCT(board)
    prev_win_rate = -1
    cur_win_rate = 0
    ths = 1e-5
    win_rates = []
    while np.abs(cur_win_rate - prev_win_rate) >= ths:
        test.search(test.init_node)
        prev_win_rate = cur_win_rate
        cur_win_rate = test.init_node.get_win_rate()
        #tackle edge case in order to prevent early stop in the first few steps of MCTS
        if prev_win_rate == cur_win_rate and (cur_win_rate == 0 or cur_win_rate == 1):
            prev_win_rate = -1

        win_rates.append(cur_win_rate)
        print(cur_win_rate)
    
    print_tree(test.init_node, max_depth = 3)

    plt.plot(range(len(win_rates)), win_rates)
    plt.show()
