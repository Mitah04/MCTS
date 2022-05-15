import time
import random
from math import sqrt, log, e
from Winner import *


class MCTS:
    """
        A class to represent MonteCarloSearchTree
    """

    def __init__(self, PlayerAI, OtherPlayer, elaspedTime):
        """
            Constructs all the necessary attributes of our class
        :param PlayerAI: 1 or 2 The AI
        :param OtherPlayer: 1 or 2 The adversary
        :param elaspedTime: Time spent searching
        """
        self.racine = None
        self.playerAI = PlayerAI
        self.OtherPlayer = OtherPlayer
        self.elaspedTime = elaspedTime

    def MonteCarloTreeSearch(self, racine):
        """
            Calls the other functions
        :param racine: Node of the intial state of our board
        :return:
        """
        t_end = time.time() + self.elaspedTime
        self.racine = racine
        racine.CreateAllStates(True, self.playerAI, self.OtherPlayer)
        # print(len(racine.children))
        while time.time() < t_end:
            racine.developed = racine.AllDeveloped()
            # print(self.test.state)
            node = self.traverse(racine)
            # print(len(racine.children))
            res = self.simulation(node)
            self.retropropagation(node, res)
            node.score = (node.wins / node.visited) + 1.4 * sqrt(log(self.racine.visited, e) / node.visited)
            if node.parent:
                node.parent.score += node.score
            # print(node.score, res, self.racine.visited, node.visited, 'score2')

        return self.best_child(racine)

    def traverse(self, node):
        """
            Traverses our tree
        :param node: <<Node>>
        :return:
        """
        i = 0
        bestNode = node
        done = False
        try:
            while node.developed and not done:
                if bestNode.score < node.children[i].score:
                    bestNode = node.children[i]
                i += 1
        except IndexError:
            done = True
            # self.test = bestNode

        winCheck = Winner(bestNode.state)

        if not (winCheck.WinnerOverall(self.playerAI) or winCheck.WinnerOverall(self.OtherPlayer)):
            for child in bestNode.children:
                if child.visited == 0:
                    child.CreateAllStates(not child.maximize, self.playerAI, self.OtherPlayer)
                    return child

        return bestNode

    def simulation(self, node):
        """
            Choses a random path on our tree and returns the result
        :return Win or not
        """
        winCheck = Winner(node.state)
        # print(not (winCheck.WinnerOverall(1) or winCheck.WinnerOverall(2)), self.count)
        while not (winCheck.WinnerOverall(self.playerAI) or winCheck.WinnerOverall(self.OtherPlayer)):
            node = self.rollout_policy(node)
            # print(len(node.children), "simulation part2")
            node.CreateAllStates(not node.maximize, self.playerAI, self.OtherPlayer)
            # print(len(node.children), "simulation part3")
            winCheck = Winner(node.state)
        # print(not (winCheck.WinnerOverall(1) or winCheck.WinnerOverall(2)), self.count)
        # print(node.wins, 'wins')
        if winCheck.WinnerOverall(self.playerAI):
            # print('win')
            node.wins += 1000
        elif winCheck.WinnerOverall(self.OtherPlayer):
            # print('lose')
            node.wins -= 1000

        return node.wins
        # print(self.maximize, winCheck.WinnerOverall(1), node.wins)
        # print(node.wins, 'wins2')

    def rollout_policy(self, node):
        """
            Randomly choses on of the children
        :return: Random child
        """
        return random.choice(node.children)

    def retropropagation(self, node, res):
        """
            Goes back up on our tree and updates the statistics
        :param node: node from traverse function
        :param res: result from simulation
        :return:
        """
        # print(node.visited, node.state)
        if node.state == self.racine.state:
            self.racine.visited += 1
            self.racine.wins += res
            return None

        node.visited += 1
        node.wins += res
        self.retropropagation(node.parent, res)

    def best_child(self, node):
        """
            Verifies most visited
        :param node:
        :return:
        """
        visitList = []
        # print(len(node.children), 'here')
        for child in node.children:
            visitList.append(child.visited)
            # print(child.visited, child.score)
        posIndex = visitList.index(max(visitList))
        return node.children[posIndex]

