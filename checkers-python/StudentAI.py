from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.

class StudentAI():
    
    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1: 2, 2: 1}
        self.color = 2
        self.exploration_parameter = 1
    
    #get my move
    def get_move(self, move):
        #do opponent's move if it is 
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1
        
        #default tree depth
        depth = 4
        root = MCTS(self.opponent[self.color])  #set the root
        self.build_tree(root, depth) #build the initial tree with depth 5
        #do some number of times selections and expansions
        for i in range(100):
            path = self.selection(root)
            self.expand(root, path)
        #do the heuristic for each node in the tree
        self.board_heuristic(root, root.expand)
        #get the optimal move
        newmove = root.optimal[0]
        #make my move
        self.board.make_move(newmove, self.color)  
        #return my move
        return newmove

    def uct(self, parent_x, child_v, child_x):
        #calculate the uct value
        return child_v/child_x + self.exploration_parameter*math.sqrt(math.log(parent_x)/child_x)
    
    
    def selection(self, node):
        #select the best move and keep selecting until there is a node not reached before
        #return the path of this selection
            path = []
        #if not reached before
            if(len(node.children) == 0):
                path.append(node)
                return path
            b = float('-inf')
        #best move
            for i in node.children:
                if i.value > b:
                    b = i.value
                    newnode = i
            path.append(newnode)
        #return the path
            return path + self.selection(newnode)
            
    def expand(self, node, path):
        #do the moves to the last node
        for i in range(len(path)-1):
            self.board.make_move(path[i].move, path[i].color)
        #add children to the last node
        moves = self.board.get_all_possible_moves(self.opponent[path[-1].color])
        for i in moves:
            for j in i:
                path[-1].children.append(MCTS(self.opponent[path[-1].color], j))
        
        #undo what was done before
        for i in range(len(path)-1):
            self.board.undo()

    def points_evaluation(self):
        #evaluate the points of current board
        points = 0
        #store all the checkers' situations
        blackkings = []
        blacknotkings = []
        whitekings = []
        whitenotkings = []
        #add the checker with their row and col to the correct list
        for i in range(self.row):
            for j in range(self.col):
                #all the checkers
                checker = self.board.board[i][j]
                if checker.color == "B": 
                    if checker.is_king:
                        blackkings.append((i,j))
                    else:
                        blacknotkings.append((i,j))
                elif checker.color == "W": 
                    if checker.is_king:
                        whitekings.append((i,j))
                    else:
                        whitenotkings.append((i,j))
        
        #calculate the value for white checkers and black checkers
        points += self.white_value(whitekings, blackkings, whitenotkings, blacknotkings)
        points += self.black_value(blackkings, whitekings, blacknotkings, whitenotkings)
        
        #if my color is white then return white points, else return black points(they are opposite)
        if self.color == 2:
            return points 
        else: 
            return -points
    
    
    def white_value(self, mykings, opponentkings, mynotkings, opponentnotkings):
        #calculate white value based on its number of its kings, number of not a king, number of opponent's kings, number of opponent's not a king
        kingv = 9 + self.row
        points = 0
        for i in mykings:
            distance = 0
            points-= kingv
            for j in opponentkings:
                distance += self.distance_cal(i[0], j[0], i[1], j[1])
            for j in opponentnotkings:
                distance += self.distance_cal(i[0], j[0], i[1], j[1])
            if len(opponentkings) != 0 | len(opponentnotkings) != 0:
                points += distance/(len(opponentkings) + len(opponentnotkings))
        for i in opponentnotkings:
            points += (5 + i[0])
        return points
        
    def distance_cal(self, x1, y1, x2, y2):
        #calculate the distance between two points
        return math.sqrt((x1 - y1)**2 + (x2 - y2)**2)
        
    def black_value(self, mykings, opponentkings, mynotkings, opponentnotkings):
        #calculate black value based on its number of its kings, number of not a king, number of opponent's kings, number of opponent's not a king
        kingv = 9 + self.row
        points = 0
        for i in mykings:
            distance = 0
            points+= kingv
            for j in opponentkings:
                distance += math.sqrt((i[0] - j[0])**2 + (i[1] - j[1])**2)
            for j in opponentnotkings:
                distance += math.sqrt((i[0] - j[0])**2 + (i[1] - j[1])**2)
            if len(opponentkings)!= 0 | len(opponentnotkings) != 0:
                points -= distance/(len(opponentkings) + len(opponentnotkings))
        for i in opponentnotkings:
            points -= (5 + (self.row-1) - i[0])
        return points



    def build_tree(self, node, depth):  
        #build the default tree
        if depth == 0:
            return
        else:
            #make move if there is a move
            if node.move != None: 
                self.board.make_move(node.move, node.color)
            #add children
            moves = self.board.get_all_possible_moves(self.opponent[node.color])
            for i in moves:
                for j in i:
                    node.children.append(MCTS(self.opponent[node.color], j))
            #build subtree
            for i in node.children:
                self.build_tree(i, depth-1)
            #undo
            if node.move != None:
                self.board.undo()



    def board_heuristic(self, node, ex): 
        #the heuristic to define the choice of optimal move
        ex = node.expand
        #make move if there is a move
        if node.move != None: 
            self.board.make_move(node.move, node.color)
        #add evaluation points to the node
        if len(node.children) == 0: 
            node.value = self.points_evaluation()
        else:  
            #all children do the heuristic
            for i in node.children:
                self.board_heuristic(i, ex)
            #if color of the node is the same as my color, then do max
            if node.color == self.color:
                optimal = dict()
                for i in node.children:
                    optimal[i.value] = []
                #add move with key(evaluation points)
                for i in node.children:
                    optimal[i.value].append(i.move)
                #choose the best one
                best = max(optimal)
                node.value = best
                #add the list of best moves
                node.optimal = optimal[best]
                #calculate the uct value
                node.uct = self.uct(ex, node.value/10%1, node.expand)
                #add up the total value
                node.win_value += best
            #if color of the node is not the same as my color, then do min
            else:
                optimal = dict()
                for i in node.children:
                    optimal[i.value] = []
                #add move with key(evaluation points)
                for i in node.children:
                    optimal[i.value].append(i.move)
                #choose the best one
                best = min(optimal)
                node.value = best
                #add the list of best moves
                node.optimal = optimal[best]
                #calculate the uct value
                node.uct = self.uct(ex, node.value/10%1, node.expand)
                #add up the total value
                node.win_value += best
        #undo all the actions
        if node.move != None:
            self.board.undo()  

#MC Tree node
class MCTS():
    def __init__(self, color, move=None):
        self.color = color
        self.move = move
        self.children = []
        self.optimal = []
        self.value = float(0)
        self.expand = 1;
        self.uct = 0;
        self.win_value = 0;

