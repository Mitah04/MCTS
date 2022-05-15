from AI_Tools import *
from Carrier import *
import copy


class Node:

    def __init__(self, board):
        self.state = board
        self.parent = None
        self.children = []
        self.visited = 0
        self.wins = 0
        self.score = 0
        self.stats = None
        self.move = None
        self.maximize = True

    def AllDeveloped(self):
        for nodes in self.children:
            if nodes.visited == 0:
                return False
        return True

    def setStatistics(self, res):
        self.stats = res

    def CreateAllStates(self, maximize, playerAI, otherPlayer):
        reverse = False
        if playerAI == 1:
            reverse = True
        board = self.state
        Tools = AI_Tools(board)
        Mover = Carrier(board)
        allPossiblities = Tools.all_possible_movement(maximize, playerAI, otherPlayer)
        if reverse:
             allPossiblities = allPossiblities[::-1]
        for move in allPossiblities:
            src = board[move[0][0]][move[0][1]]
            save = board[move[1][0]][move[1][1]]
            Mover.play_move(move, playerAI) if maximize else Mover.play_move(move, otherPlayer)
            state = copy.deepcopy(self.state)
            self.children.append(Node(state))
            self.children[-1].parent = self
            self.children[-1].move = move
            self.children[-1].maximize = maximize
            Mover.play_move(move[::-1], playerAI, save) if maximize else Mover.play_move(move[::-1], otherPlayer, save)
        self.developed = self.AllDeveloped()
