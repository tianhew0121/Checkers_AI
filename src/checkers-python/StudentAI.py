from random import randint
from BoardClasses import Move
from BoardClasses import Board
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
        #print(self.color)
        #moves = self.board.get_all_possible_moves(self.color)
        #index = randint(0, len(moves) - 1)
        #inner_index = randint(0, len(moves[index]) - 1)
        #move = moves[index][inner_index]
        move = self.minimax_search()
        print('my turn')
        #print(type(move))
        self.board.make_move(move, self.color)
        return move

    def minimax_search(self):
        #print(self.board.get_all_possible_moves(self.color))
        _, move = self.max_val(5)
        return move

    def max_val(self,depth, mv=None):
        #print('in max', depth)
        
        v = float('-inf')
        all_moves = self.board.get_all_possible_moves(self.color)
        if len(all_moves) == 0:
            return float('inf'), None
        if depth <= 0: # time to evaluate the board
            return sum([len(i) for i in all_moves])*0.7 + len(self.board.get_all_possible_moves(self.color)) - len(self.board.get_all_possible_moves(self.opponent[self.color])), mv


        for r in range(len(all_moves)):
            for c in range(len(all_moves[r])):
                mv = all_moves[r][c]
                self.board.make_move(mv, self.color)
                v2, mv2 = self.min_val(depth-1,mv)
                if v2 > v:
                    v, mv = v2, mv2
                self.board.undo()

        return v, mv
    
    def min_val(self,depth, mv):
        #print('in min', depth)
        
        v = float('-inf')
        all_moves = self.board.get_all_possible_moves(self.opponent[self.color])
        if len(all_moves) == 0:
            return float('-inf'), None
        if depth <= 0: # time to evaluate the board
            return sum([len(i) for i in all_moves])*0.7 + len(self.board.get_all_possible_moves(self.opponent[self.color])) - len(self.board.get_all_possible_moves(self.color)), mv
        
        for r in range(len(all_moves)):
            for c in range(len(all_moves[r])):
                mv = all_moves[r][c]
                self.board.make_move(mv, self.opponent[self.color])
                v2, mv2 = self.max_val(depth-1, mv)
                if v2 < v:
                    v, mv = v2, mv2
                self.board.undo()
        return v, mv

