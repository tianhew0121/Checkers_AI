from random import randint
from BoardClasses import Move
from BoardClasses import Board
import config
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
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
        move = self.minimax_search()
        ##############################################################
        self.board.make_move(move, self.color)
        return move

    def minimax_search(self):
        ##############################################################
        #Recursion depth set in config.py
        ##############################################################
        _, move = self.max_val(config.depth)
        return move

    def max_val(self,depth, mv=None):
        ##############################################################
        # To Do:
        #       Add the game ending condition in sudo code in lecture slides
        #       Do the same for min_val()
        ##############################################################
        v = float('-inf')
        all_moves = self.board.get_all_possible_moves(self.color)
        if len(all_moves) == 0: # When there's no checkers that can be moved, consider a loss.
            return float('inf'), None

        if depth <= 0: # When Reached terminal depth, evaluate the current board
            return self.evaluate_board(self.color,self.opponent[self.color], mv)
            

        for r in range(len(all_moves)):
            for c in range(len(all_moves[r])):
                mv = all_moves[r][c]
                self.board.make_move(mv, self.color)
                v2, mv2 = self.min_val(depth-1,mv)
                if v2 > v:
                    v, mv = v2, mv2
                self.board.undo() #undo the move made earlier

        return v, mv
    
    def min_val(self,depth, mv):
        v = float('-inf')

        all_moves = self.board.get_all_possible_moves(self.opponent[self.color])

        if len(all_moves) == 0:
            return float('-inf'), None
        if depth <= 0: # evaluate the board
            return self.evaluate_board(self.opponent[self.color],self.color, mv)
            
        for r in range(len(all_moves)):
            for c in range(len(all_moves[r])):
                mv = all_moves[r][c]
                self.board.make_move(mv, self.opponent[self.color])
                v2, mv2 = self.max_val(depth-1, mv)
                if v2 < v:
                    v, mv = v2, mv2
                self.board.undo() # undo the move made earlier
        return v, mv

    def evaluate_board(self, my_color, oppo_color, mv): # return v, move
        ############################################################################################################################
        # Current v:
        #       Set to the difference between player1(my)'s piece count and player2(opponent)'s piece count
        #       In min_val, the player1(my) is the opponent of our agent
        # To Do:
        #       Optimize the this function so that every piece get to move rather than having one piece solo the game
        ############################################################################################################################
        return len(self.board.get_all_possible_moves(my_color)) - len(self.board.get_all_possible_moves(oppo_color)), mv