from random import randint
from BoardClasses import Move
from BoardClasses import Board
import copy
import config
from math import sqrt
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class TestException(Exception):
    pass

class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1
        ##############################################################
        #Calls the new minimax
        move = MTCS(copy.deepcopy(self.board), self.color).final_decision
        ##############################################################
        self.board.make_move(move, self.color)
        return move

def format_all_move(move_matrix):
    move_lst= []
    for i in range(len(move_matrix)):
        for j in range(len(move_matrix[i])):
            move_lst.append(move_matrix[i][j])        
    return move_lst

def pick_random_move(moves):
    rand_ind = randint(0, len(moves) - 1)
    return moves[rand_ind]

class Node(object):
    # This class specify node object. Can do backtrack.
    def __init__(self, color):
        self.parent = None
        self.children = []
        self.time_visit = 0
        self.color = color
        self.sp = 0
        self.wi = 0
        self.si = 0
        self.move = 0

    def selection(self):
        selected_node = sorted(self.children, lambda x: x.wi/x.si + config.c * sqrt(self.sp/self.si))[-1]
        return selected_node

    def expansion(self, moves, color):
        for move in moves:
            new_node = Node(color)
            new_node.store_move(move)
            self.insert(new_node)

    def insert(self, node):
        self.children.append(node)
        node.parent = self


    def visit(self, val):
        self.si += 1
        if self.parent:
            self.sp = self.parent.si
        self.wi += val[self.color]


    def update(self, val):
        #color is the player who wins: 1/0
        if self.parent != None:
            self.parent.update(val)
        self.visit(val)


    def set_root(self):
        self.parent = None
        return self

    def store_move(self, move):
        self.move = move

    def is_root(self):
        return self.parent == None


    def is_leaf(self):
        return self.children == set()


class MTCS():

    def __init__(self, board, color):
        self.opponent = {1:2,2:1}
        self.root = Node(self.opponent[color])
        self.board = board
        self.color = color
        self.final_decision = 0
        self.run()

    def start_game(self):
        moves = format_all_move(self.board.get_all_possible_moves())
        self.root.expansion(moves)
        for node in self.root.children:
            if not node.is_leaf():
                node = node.selection()


            self.board.make_move(node.move)
            result = self.simulation()
            if result == 1:
                val = {self.color:1, self.opponent[self.color]:-1}
            elif result == -1:
                val = {self.color:-1, self.opponent[self.color]:1}
            else:
                val = {self.color:0, self.opponent[self.color]:0}
            node.update(val)

    def simulation(self):
        board = copy.deepcopy(self.board)
        color = self.color
        win = 0
        while win == 0:
            win = board.is_win(self.color)
            # play the game randomly to the end and record stats
            next_move = pick_random_move(format_all_move(board.get_all_possible_moves()))
            board.make_move(next_move, color)
            color = self.opponent[color]
        
        if win == self.color:
            return 1
        elif win == 0:
            return 0
        return -1

    def simulate(self,parent, color):
        # update the tree
        new_node = Node(color)
        parent.insert(new_node)
        return new_node
                
    def check_status_win(self, color):
        if self.board.is_win(color):
            return True

