from ast import copy_location
from random import choice, randint
from BoardClasses import Move
from BoardClasses import Board
import copy
import config
from math import sqrt, log
from collections import defaultdict
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
from time import time
##########################Config
c = 4
debug = False
#sim_count = 350 #450 # together with simulation limit, help control system usage no matter what the size of the board is.
sim_count = 450
sim_minimum = 1
sim_scaler = 0.7
reset_counter = 100000
p_scaler = 1.0
p_shrink = 1
p_min = 1
simulation_scaler = 1
simulation_max = 35    #   35
simulation_limit = 5000   # Not necessaryly the higher this number the better the result. 
                        #Since we used AMAF H, making this value small might help select the 
                        # moves that leads to actually winning faster.
final_total = 0         # Total time so far


class Board(Board):
    def is_win(self,turn):
        """
        this function tracks if any player has won
        @param :
        @param :
        @return :
        @raise :
        """
        if turn == "W":
            turn = 2
        elif turn == "B":
            turn =  1
        W_has_move = True
        B_has_move = True
        if len(self.get_all_possible_moves(1)) == 0:
            if turn != 1:
                B_has_move = False
        elif len(self.get_all_possible_moves(2)) == 0:
            if turn != 2:
                W_has_move = False

        if W_has_move and not B_has_move:
            return 2
        elif not W_has_move and B_has_move:
            return 1

        W = True
        B = True

        for row in range(self.row):
            for col in range(self.col):
                checker = self.board[row][col]
                if checker.color == 'W':
                    W = False
                elif checker.color == 'B':
                    B = False
                if not W and not B:
                    return 0
        if W:
            return 2
        elif B:
            return 1
        else:
            return 0


DEBUG =  debug
opponent = {2:1, 1:2}
mcts = None
round_counter = 0
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
        global mcts, round_counter, final_total, sim_count
        #round_counter += 1
        #print('In get move')
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1
        #print(mcts != None)
        #if round_counter ==  reset_counter:
            #tree_reset()
        '''if mcts != None :
            #print(mcts.root.is_leaf())
            if not mcts.root.is_leaf():
                #print(self.board.saved_move)
                mcts.reuse_tree(self.board.saved_move[-1][0])'''
        ##############################################################
        '''if mcts == None:
            mcts = MCTS(self.board, self.color)'''
        t1 = time()
        mcts = MCTS(self.board, self.color)
        move = mcts.search()
        t2 = time()
        each_total = t2 - t1
        final_total += each_total
        if final_total >= 420:
            sim_count *= sim_scaler
        '''mcts.reuse_tree(move)'''
        ##############################################################
        self.board.make_move(move, self.color)
        #tree_reset()
        #print(self.board.is_win(self.color))
        return move

def all_moves(board, color):
    move_matrix = board.get_all_possible_moves(color)
    move_lst= []
    for i in range(len(move_matrix)):
        for j in range(len(move_matrix[i])):
            move_lst.append(move_matrix[i][j])        
    return move_lst

def my_piece(board, color):
    move_matrix = board.get_all_possible_moves(color)
    piece = []
    for i in range(len(move_matrix)):
        piece.append(move_matrix[i][0][0])
    return piece

def pick_random_move_from(moves):
    if len(moves) == 1:
        return moves[0]
    rand_ind = randint(0, len(moves) - 1)
    return moves[rand_ind]

def reverse_board(board, i):
    for k in range(i+1):
        board.undo()


class Node(object):
    def __init__(self, parent, p_first=1.0) -> None:
        self.parent = parent
        self.p_move_first = p_first
        self.children = {} # key: move value: node  ---> node[move] = child
        self.si = 1 # number of time this node is visited
        self.wi = 0
        self.uct = 0
        


    def Node_UCT(self, final=False):
        if not self.parent:
            sp = self.si
        else:
            sp = self.parent.si
        si = self.si
        if self.si == 0:
            si = 1
        #p_first = self.p_move_first / sum([c.p_move_first for c in self.parent.children.values()])
        
        return self.wi + c*sqrt(log(sp)/(si)) * (len(self.parent.children))

    def update(self, val) -> None:
        self.si += 1 # visit once and also avoid division zero
        #print('updated, si:', self.si, 'sp:',self.sp)
        self.wi -= val
        
        #self.uct = self.Node_UCT()

    def update_AMAF(self, val, moves):
        #moves = [str(i) for i in moves]
        #p_scal = {-1: 2- p_scaler, 1:  p_scaler}
        #p_scal = {-1: 1, 1: mcts.p_scal}
        #p_scal = {-1: 1/ p_scaler, 1: mcts.p_scal, 0:1}
        #if val != 0 and self.parent:
        #    for mvs in self.children.keys():
        #        if str(mvs) in moves:
        #            self.children[mvs].p_move_first *= mcts.p_scal
                    #print('AMAF')
                    #self.children[mvs].p_move_first *= p_scal[val]
        self.update(val)

    def update_recurse(self, val, moves):
        #print('now is update recurse, val is:', val)
        #print('val in update recurse', val)
        if self.parent:
            #print('this node has parent')
            self.parent.update_recurse(-val, moves)
        #print('reached parent, am i root?\n', self == mcts.root, '\nmy children are\n', self.children.keys(), '\n')
        #self.update(val)
        self.update_AMAF(val, moves)

    def selection(self):
        #print("In selection")
        #print(self.children)
        for mv in self.children:
            #print("in for selection", mv)
            if self.children[mv].si == 0 :
                #print('returning:', mv, self.children[mv])
                return mv, self.children[mv] # if child's node has time visited == 0, select that node
        #node_selected = sorted(self.children.items(), key=lambda mv: UCT(self.children[mv[0]]))[-1]
        node_selected = max(self.children.items(), key=lambda mv: mv[1].Node_UCT())
        #print('node select', node_selected[1].UCT)
        #print("after getting node_selected")
        return node_selected # returns the node with largest UCT value
    
    def selection_recurse(self):
        if not self.is_leaf:
            return self.selection().selection_recurse() # return the selected
        return self

    def expansion(self, moves):
        for move in moves:
            self.children[move] = Node(self, 1.0/len(moves))

    def is_leaf(self):
        return len(self.children) == 0



class MCTS():
    def __init__(self, board, color) -> None:
        self.root = Node(None)
        self.board = board
        self.my_color = color
        self.p_scal = p_scaler
        self.sim_count = sim_count
        self.shrink_factor = sim_scaler
        self.simulation_lim = simulation_limit

    def reset(self):
        self.root = Node(None)

    def search(self):
        all_move = all_moves(self.board, self.my_color)
        if len(all_move) == 1:
            return all_move[0]
        for i in range(self.sim_count):
            #do one simulation and expand the nodes
            board = copy.deepcopy(self.board)
            current_color = self.my_color
            current_node = self.root
            #print('im not leaf')
            while not current_node.is_leaf():
                #print('im not leaf for')
                current_move, current_node = current_node.selection()
                board.make_move(current_move, current_color)
                current_color = opponent[current_color]
            #print('im not leaf')
            # current node is leaf
            all_move = all_moves(board, color=current_color)
            game_finished = board.is_win(current_color)
            if game_finished == 0  :
                if len(all_move) != 0:
                    #print('expanding')
                    current_node.expansion(all_move)
                    #current_color = opponent[current_color]
            # simulation step
            if game_finished == self.my_color  :
                current_node.update_recurse(-1.1, [])
            elif game_finished == opponent[self.my_color]  :
                current_node.update_recurse(-1, [])
            simulation_result, moves_to_end = self.simulation(board, current_color)
            # simulation result: 1 if winner is current_color, -1 if opponent
            if DEBUG:
                print(simulation_result, 'player:', current_color, 'mycolor:', self.my_color)
            if simulation_result != 0:
                current_node.update_recurse(simulation_result, moves_to_end)

        #self.size_reduce()
        choices = sorted(self.root.children.keys(), key= lambda x: self.root.children[x].si)
        #for choice in choices:
            #if self.root.children[choice].si > 0.3 *  sim_count and self.root.children[choice].wi/self.root.children[choice].si > 0.6:
                #choices.remove(choice)
        if DEBUG:
            for mv in choices:
                print("Move:", mv, "UCT:", self.root.children[mv].Node_UCT(DEBUG))
        #if len(self.root.children) == 0:
            #all_move = all_moves(self.board, self.my_color)
            #print("All move debug", all_move)
        return choices[-1]



    def size_reduce(self):
        self.sim_count *= self.shrink_factor
        self.sim_count = int(self.sim_count)
        self.shrink_factor *= self.shrink_factor
        if self.sim_count <  sim_minimum:
            self.sim_count =  sim_minimum
        self.simulation_lim *=  simulation_scaler
        if self.simulation_lim >  simulation_max:
            self.simulation_lim =  simulation_max
        self.p_scal *=  p_shrink
        if self.p_scal >  p_min:
            self.p_scal =  p_min


    def simulation(self,b, start_player):
        count = 0
        moves_to_end = []
        board = copy.deepcopy(b)
        win_type = board.is_win(start_player)
        current_player = start_player
        while win_type == 0:
            count += 1
            if count >  simulation_max:
                break
            all_mv = all_moves(board, current_player)
            #print(all_mv, current_player)
            #board.show_board()
            if len(all_mv) == 0:
                win_type = board.is_win(current_player)
                break
            sim_move = pick_random_move_from(all_mv)
            #if current_player == self.my_color:
                #moves_to_end.append(sim_move)
            board.make_move(sim_move, current_player)
            win_type = board.is_win(current_player)
            current_player = opponent[current_player]
        
        if win_type == opponent[start_player]: # I won
            return -1,moves_to_end
        elif win_type == start_player: # I lost
            return 1,moves_to_end
        else: # Draw
            return 0,moves_to_end
        


    def reuse_tree(self, move):
        for mv in self.root.children:
            if str(mv) == str(move):
                move = mv
        self.root = self.root.children[move]
        self.root.parent = None









