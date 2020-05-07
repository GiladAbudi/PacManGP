import random
import json
import time
import argparse
import os
import sys
import copy
from decimal import Decimal
import math
import functools
import operator

WALL = 0
CANDY = 1
EMPTY = 2
ENEMY = 3
PACMAN_POS = 4

GAME_ON = 0
GAME_OVER = 1

FUNCTIONS = ['+', '-', '*', '/']
DISTANCE_TO_NEAREST_GHOST = 'G'
DISTANCE_TO_NEAREST_PILL = 'P'
PLACE_COUNT = 'T'
CONSTANT = 'C'
PILLS_IN_DISTANCE = 'D'
GHOSTS_IN_DISTANCE = 'E'
DISTANCE_TO_NEAREST_CORNER = 'N'

PACMAN_TERMINALS = [DISTANCE_TO_NEAREST_GHOST, DISTANCE_TO_NEAREST_PILL, PLACE_COUNT, PILLS_IN_DISTANCE,
                    GHOSTS_IN_DISTANCE, CONSTANT, DISTANCE_TO_NEAREST_CORNER]
CONSTANT_MIN = -1
CONSTANT_MAX = 10
PRINT = True
# Allowed movements
PACMAN_MOVES = [[0, 1], [0, -1], [1, 0], [-1, 0]]
GHOST_MOVES = [[0, 1], [0, -1], [1, 0], [-1, 0]]

MAX_TREE_DEPTH = 3
TOURNAMENT_SIZE = 3
POPULATION_SIZE = 100
NUMBER_OF_GENERATIONS = 100
CROSSOVER_PROB = 0.7
MUTATION_PROB = 0.05
NUMBER_OF_OFFSPRINGS = POPULATION_SIZE * CROSSOVER_PROB / 2
NUMBER_OF_EVALUATION = POPULATION_SIZE + (NUMBER_OF_GENERATIONS - 2) * (NUMBER_OF_OFFSPRINGS)
NUMBER_OF_RUNS = 1
PENALTY_COEFFICIENT = 1
level1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 2, 2, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 2, 3, 3, 2, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 2, 2, 3, 2, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
];

level2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 0, 2, 2, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 2, 3, 3, 2, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
];

level3 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 4, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
];

level4 = [  # 23X26
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 2, 2, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 2, 2, 3, 2, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 2, 3, 3, 2, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
];


def deepgetattr(obj, attr):
    """Recurses through an attribute chain to get the ultimate value."""
    return functools.reduce(getattr, attr.split('.'), obj)


def deepsetattr(obj, attr, val):
    """Recurses through an attribute chain to set the ultimate value."""
    pre, _, post = attr.rpartition('.')
    return setattr(deepgetattr(obj, pre) if pre else obj, post, val)


def nodeParent(nodeID):
    """Return ID of parent of a node"""
    if nodeID > 1:
        return int((nodeID - 1) / 2)
    else:
        return 0


def nodeLeftChild(nodeID):
    """Return ID of left child of a node"""
    return (nodeID * 2) + 1


def nodeRightChild(nodeID):
    """Return ID of right child of a node"""
    return (nodeID * 2) + 2


def totalNumberOfNodes(height):
    """Return total number of nodes in a tree with given height"""
    return 2 ** (height + 1) - 1


class WriteToFile(object):
    """Write outputs to file"""

    def __init__(self):
        pass

    def writeHeaderToLog(self):
        print('Number of runs: ' + str(Decimal(NUMBER_OF_RUNS)) + '\n')
        print('Number of fitness evaluations: ' + str(Decimal(NUMBER_OF_EVALUATION)) + '\n')
        print('PacMan population Size: ' + str(Decimal(POPULATION_SIZE)) + '\n')
        print('Number Of Genrations: ' + str(Decimal(NUMBER_OF_GENERATIONS)) + '\n')
        print('Tournament size for PacMan survival selection: ' + str(Decimal(TOURNAMENT_SIZE)) + '\n')
        print('Mutation probability: ' + str(round(MUTATION_PROB, 4)) + '\n')
        print('Crossover probability: ' + str(round(CROSSOVER_PROB, 4)) + '\n')

    def writeResultsLabelToLog(self):
        """Append results header to log file"""
        print('\nResult Log\n ')
        print('BestFitnees \t AvgFitness \t MinFitness\n ')

    def writeResultsToLog(self, eval, *args):
        lst = []
        for arg in args:
            lst.append(arg)
        print(lst)

    def writeToSolutionLog(self, solution):
        print("\n\n")
        print(str(solution))


class World(object):
    """object of the world grid"""

    def __init__(self, level):
        self.pacmanscore = 0.000
        self.map = copy.deepcopy(level)
        self.wall = []
        self.pacman = []
        self.ghost = []
        self.pill = []
        self.empty = []
        self.numberOfPills = 0
        self.ghostscore = []
        self.placeMemory = {}
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 0:
                    self.wall.append([i, j])
                elif self.map[i][j] == 1:
                    self.pill.append([i, j])
                    self.numberOfPills += 1
                elif self.map[i][j] == 2:
                    self.empty.append([i, j])
                elif self.map[i][j] == 3:
                    self.ghost.append([i, j])
                else:
                    self.pacman = [i, j]
                    self.placeMemory.setdefault(str([i, j]), self.placeMemory.get(str([i, j]), 0) + 1)
        self.numberOfCurrPills = self.numberOfPills
        self.width = len(self.map[0])
        self.height = len(self.map)
        self.size = len(self.map) * len(self.map[0])
        self.candysInDis = -1
        self.ghostsInDis = -1
        self.nearestCandy = -1

    def resetMemory(self):
        self.candysInDis = -1
        self.ghostsInDis = -1
        self.nearestCandy = -1

    def getPacmanPosition(self):
        return self.pacman

    def getGoustPosition(self):
        return self.ghost

    def movePacman(self, move):
        self.pacman[0] += move[0]
        self.pacman[1] += move[1]

    def setPacMove(self, pos):
        self.pacman = pos

    def moveGhost(self, ghostLoc, move):
        self.ghost[ghostLoc][0] += move[0]
        self.ghost[ghostLoc][1] += move[1]

    def setGhostMove(self, ghostLoc, pos):
        self.ghost[ghostLoc] = pos


class GPTree(object):
    """Objects of genetic programming binary trees"""

    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None
        self.fitness = 0
        self.evals = 0
        self.normalizedFitness = 0

    def addLeftChild(self, value=None):
        """Add left child to the current node"""
        self.left = GPTree(value)

    def addRightChild(self, value=None):
        """Add right child to the current node"""
        self.right = GPTree(value)

    def getNodeByLocation(self, depth, index):
        """Return the node specified by depth and index"""
        if depth is 0:
            return self
        next = self
        for d in reversed(range(1, depth + 1)):
            if next is not None:
                if index < (2 ** (d - 1)):
                    next = next.left
                else:
                    next = next.right
                index = index % (2 ** (d - 1))
            else:
                return None
        return next

    def getNodeByID(self, id):
        """Return the node specified by its ID"""
        depth = int(math.log2(id + 1))
        index = id - (2 ** depth) + 1
        return self.getNodeByLocation(depth, index)

    def setNodeByLocation(self, depth, index, node):
        """Set the node specified by depth and index"""
        if depth is 0:
            self = node
            return 1
        attr = ''
        next = self
        for d in reversed(range(1, depth + 1)):
            if next is not None:
                if index < (2 ** (d - 1)):
                    next = next.left
                    attr += 'left.'
                else:
                    next = next.right
                    attr += 'right.'
                index = index % (2 ** (d - 1))
                if d is 1:
                    deepsetattr(self, attr[:-1], node)
                    return 1
            else:
                return 0
        return 1

    def setNodeByID(self, id, node):
        """Return the node specified by its ID"""
        depth = int(math.log2(id + 1))
        index = id - (2 ** depth) + 1
        return self.setNodeByLocation(depth, index, node)

    def isNodeNoneByLocation(self, depth, index):
        """Return True/False if the node specified by depth and index is/is not None"""
        node = self.getNodeByLocation(depth, index)
        if node is None:
            return True
        elif node.value is None:
            return True
        else:
            return False

    def isNodeNoneByID(self, id):
        """Return True/False if the node specified by its ID is/is not None"""
        depth = int(math.log2(id + 1))
        index = id - (2 ** depth) + 1
        return self.isNodeNoneByLocation(depth, index)

    def height(self):
        """Returns height of the tree"""
        height = 0
        while True:
            if any(not self.isNodeNoneByLocation(height, index) for index in range(2 ** height)):
                height += 1
            else:
                break;
        height -= 1
        return height

    def __str__(self):
        """For simple representation of trees"""
        str_ = ''
        height = self.height()
        for depth in range(height + 1):
            str_ += ' ' * 3 * (2 ** (height - depth) - 1)
            for index in range(2 ** depth):
                if self.isNodeNoneByLocation(depth, index):
                    str_ += '  .  '
                    str_ += ' ' * (3 * (2 ** (height - depth + 1) - 1) - 2)
                elif isinstance(self.getNodeByLocation(depth, index).value, (int, float)):
                    str_ += "{: 5.01f}".format(round(self.getNodeByLocation(depth, index).value, 1))
                    str_ += ' ' * (3 * (2 ** (height - depth + 1) - 1) - 2)
                else:
                    str_ += "{:^5}".format(self.getNodeByLocation(depth, index).value)
                    str_ += ' ' * (3 * (2 ** (height - depth + 1) - 1) - 2)
            str_ += '\n'
        return str_

    def makeTree(self):
        """Populate nodes of an initialized tree by ramped half-and-half method"""

        terminalsSet = PACMAN_TERMINALS
        # Ramped half-and-half initialization
        if random.random() > 0.5:
            # Full method
            for depth in range(MAX_TREE_DEPTH + 1):
                for index in range(2 ** depth):
                    node = self.getNodeByLocation(depth, index)
                    # non terminal node
                    if depth < MAX_TREE_DEPTH:
                        node.value = random.choice(FUNCTIONS)
                        node.addLeftChild()
                        node.addRightChild()
                    # leaf -> terminal node
                    else:
                        node.value = random.choice(terminalsSet)

                    if node.value is CONSTANT:
                        node.value = random.uniform(CONSTANT_MIN, CONSTANT_MAX)
        else:
            # Grow method
            for depth in range(MAX_TREE_DEPTH + 1):
                for index in range(2 ** depth):
                    node = self.getNodeByLocation(depth, index)
                    if depth is 0:
                        node.value = random.choice(FUNCTIONS + terminalsSet)
                        node.addLeftChild()
                        node.addRightChild()
                    else:
                        if depth < MAX_TREE_DEPTH:
                            node.addLeftChild()
                            node.addRightChild()
                            # if node's parent is non-terminal, create child (option to be terminal or not)
                            if self.getNodeByID(nodeParent((2 ** depth) + index - 1)).value in FUNCTIONS:
                                node.value = random.choice(FUNCTIONS + terminalsSet)
                        # max depth - if parents are non-terminal ->creat terminal child
                        elif self.getNodeByID(nodeParent((2 ** depth) + index - 1)).value in FUNCTIONS:
                            node.value = random.choice(terminalsSet)
                    if node.value is CONSTANT:
                        node.value = random.uniform(CONSTANT_MIN, CONSTANT_MAX)


class PacmanGP:
    """class of methods for simulating Pac-Man"""

    def pacmanController(self, world, stateEvaluator):
        """control movement of Ms. Pac-Man"""
        validMoves = []
        for move in PACMAN_MOVES:
            if world.pacman[0] + move[0] < world.height and world.pacman[0] + move[0] >= 0 and world.pacman[1] + move[
                1] < world.width and world.pacman[1] + move[1] >= 0 and world.map[world.pacman[0] + move[0]][
                world.pacman[1] + move[1]] != 0:
                validMoves.append(move)
        pacman_init_pos = copy.deepcopy(world.pacman)

        newStateGoodness = -100000  # very small number
        bestIdx = 0
        for idx, move in enumerate(validMoves):
            world.movePacman(move)
            world.resetMemory()
            stateGoodness = self.runTree(stateEvaluator, world)
            if newStateGoodness < stateGoodness:
                newStateGoodness = stateGoodness
                bestIdx = idx
            world.movePacman([-x for x in move])
        world.movePacman(validMoves[bestIdx])
        world.placeMemory[str(world.pacman)] = world.placeMemory.get(str(world.pacman), 0) + 1

    def ghostController(self, world):
        """Control movement of the ghosts"""
        for gIndex in range(len(world.ghost)):
            validMoves = []
            ghost = world.ghost[gIndex]
            ghostX = ghost[0]
            ghostY = ghost[1]
            for move in GHOST_MOVES:
                if (world.map[ghostX + move[0]][ghostY + move[1]] != WALL):
                    validMoves.append(move)
            # move the ghost to random place or rush - por 0.65 for rush
            if (random.random() > 0.35):  # rush !
                DisToPacman = 10000  # high number (low is better)
                bestIdx = 0
                for idx, move in enumerate(validMoves):
                    someMoveScore = self.manhattanDistance([ghostX + move[0], ghostY + move[1]], world.pacman)
                    if DisToPacman > someMoveScore:
                        DisToPacman = someMoveScore
                        bestIdx = idx
                world.moveGhost(gIndex, validMoves[bestIdx])
            else:  # random move
                index = int(random.random() * len(validMoves))
                world.moveGhost(gIndex, validMoves[index])

    def manhattanDistance(self, unit1, unit2):
        """Return Manhattan distance between two points"""
        x1 = unit1[0]
        y1 = unit1[1]
        x2 = unit2[0]
        y2 = unit2[1]
        distance = abs(x1 - x2) + abs(y1 - y2)
        return distance

    def functionOutput(self, parent, child1, child2):
        """Translate the given function and return its output for provided operands"""
        if parent is '+':
            return (child1 + child2)
        elif parent is '-':
            return (child1 - child2)
        elif parent is '*':
            return (child1 * child2)
        elif parent is '/':
            if child2 == 0:
                return 0
            else:
                return (child1 / child2)

    def runTree(self, tree, world):
        """Return the overall output value of a tree"""
        treeCpy = copy.deepcopy(tree)
        height = treeCpy.height()
        for id in reversed(range(totalNumberOfNodes(height))):
            if not treeCpy.isNodeNoneByID(id):
                node = treeCpy.getNodeByID(id)
                if node.value is DISTANCE_TO_NEAREST_GHOST:
                    node.value = self.distanceToNearestGhost(world.pacman, world.ghost)
                elif node.value is DISTANCE_TO_NEAREST_PILL:
                    node.value = self.distanceToNearestPill(world.pacman, world)
                elif node.value is PLACE_COUNT:
                    node.value = self.placeCount(world)
                elif node.value is PILLS_IN_DISTANCE:
                    node.value = self.pillsInDistanceK(world)
                elif node.value is GHOSTS_IN_DISTANCE:
                    node.value = self.ghostsInDistanceK(world)
                elif node.value is DISTANCE_TO_NEAREST_CORNER:
                    node.value = self.distanceToNearestCorner(world)
        for id in reversed(range(totalNumberOfNodes(height))):
            if not treeCpy.isNodeNoneByID(id):
                node = treeCpy.getNodeByID(id)
                if node.value in FUNCTIONS:
                    node.value = self.functionOutput(node.value, treeCpy.getNodeByID(nodeLeftChild(id)).value,
                                                     treeCpy.getNodeByID(nodeRightChild(id)).value)
        return node.value

    def distanceToNearestGhost(self, unit, ghosts):
        """Return Manhattan distance of the given unit to the nearest ghost"""
        return min(self.manhattanDistance(unit, ghost) for ghost in ghosts)

    def placeCount(self, world):
        return world.placeMemory.get(str(world.pacman), 0)

    def distanceToNearestCorner(self, world):
        corners = [[1, 1], [world.width - 1, world.height - 1], [1, world.width - 1], [world.height - 1, 1]]
        return min(self.manhattanDistance(world.pacman, corner) for corner in corners)

    def pillsInDistanceK(self, world):
        if (world.candysInDis != -1):
            return world.candysInDis
        counter = 0
        K_DISTANCE = 4
        for pill in world.pill:
            if world.pacman[0] + K_DISTANCE > pill[0] > world.pacman[0] - K_DISTANCE and world.pacman[1] + K_DISTANCE > \
                    pill[1] > world.pacman[1] - K_DISTANCE:
                counter += 1
        world.candysInDis = counter
        return counter

    def ghostsInDistanceK(self, world):
        if (world.ghostsInDis != -1):
            return world.ghostsInDis
        counter = 0
        K_DISTANCE = 4
        for ghost in world.ghost:
            if world.pacman[0] + K_DISTANCE > ghost[0] > world.pacman[0] - K_DISTANCE and world.pacman[1] + K_DISTANCE > \
                    ghost[1] > world.pacman[1] - K_DISTANCE:
                counter += 1
        world.ghostsInDis = counter
        return counter

    def distanceToNearestPill(self, unit, world):
        """Return Manhattan distance of the given unit to the nearest pill"""
        if (world.nearestCandy != -1):
            return world.nearestCandy
        distance = world.height + world.width - 2
        for i in range(world.height):
            for j in range(world.width):
                if world.map[i][j] is CANDY and distance > self.manhattanDistance(unit, [i, j]):
                    distance = self.manhattanDistance(unit, [i, j])
        world.nearestCandy = distance
        return distance

    def playTurn(self, time, world, individual):
        """Play the game for one time step"""
        gameState = GAME_ON
        # search and move pacman to the best place
        self.pacmanController(world, individual)
        self.ghostController(world)
        pacman = world.pacman
        for ghost in world.ghost:
            if pacman[0] == ghost[0] and pacman[1] == ghost[1]:
                gameState = GAME_OVER
        if world.map[pacman[0]][pacman[1]] == CANDY:
            world.map[pacman[0]][pacman[1]] = EMPTY
            world.numberOfCurrPills -= 1
            world.pill.remove(world.pacman)

        world.pacmanscore = (world.numberOfPills - world.numberOfCurrPills) / world.numberOfPills
        # if time == 0:
        #   print("Lose-time   { }\n",format(world.numberOfPills-world.numberOfCurrPills))
        if world.numberOfCurrPills == 0:
            gameState = GAME_OVER
            world.pacmanscore *= 0.95 + 0.05 * (1 - ((((2 * world.width * world.height) - time) - (
                        world.numberOfPills - world.numberOfCurrPills)) / ((
                                                                                       2 * world.width * world.height) - world.numberOfPills)))
        #  print("WIN WIN WIN WIN\n")
        elif gameState == GAME_OVER:
            world.pacmanscore *= 0.95 + 0.05 * (1 - ((((2 * world.width * world.height) - time) - (
                        world.numberOfPills - world.numberOfCurrPills)) / ((
                                                                                       2 * world.width * world.height) - world.numberOfPills))) - 0.1
        # print("Lose-Eat { }\n",format(world.numberOfPills-world.numberOfCurrPills))

        #  0.95(how much i eat) + 0.5(How effective I was)

        return gameState

    def playGame(self, individual=None):
        """Run the whole game until a game-over condition occurs - on 4 maps"""
        # init score
        score = [0, 0, 0, 0]
        # run the game on all maps
        for idx, level in enumerate([level2, level3, level1, level4]):
            world = World(level)
            time = 2 * world.size

            # pacman and ghost steps
            pacmanSeq = []
            ghostsSeq = []
            pacmanSeq.append(copy.deepcopy(world.getPacmanPosition()))
            ghostsSeq.append(copy.deepcopy(world.getGoustPosition()))

            gameState = GAME_ON

            while time != 0 and gameState != GAME_OVER:
                time -= 1
                gameState = self.playTurn(time, world, individual)
                pacmanSeq.append(copy.deepcopy([world.pacman, world.pacmanscore]))
                ghostsSeq.append(copy.deepcopy(world.getGoustPosition()))

            score[idx] = world.pacmanscore
        # Avg
        individual.fitness = sum(score) / len(score)

        individual.evals += 1
        return (world.pill, pacmanSeq, ghostsSeq)

    def sumFitness(self, population):
        """Calculate sum of all fitness values in the population"""
        return sum(individual.fitness for individual in population)

    def averageFitness(self, population):
        """Calculate average fitness in the population"""
        return round(self.sumFitness(population) / len(population), 2)

    def findFittest(self, population, n=1):
        """Find the (n) fittest individual(s) in the population and return it."""
        population.sort(key=operator.attrgetter('fitness'), reverse=True)
        if n == 1:
            return population[0]
        else:
            return population[0:n]

    def findMInFitness(self, population, n=1):
        population.sort(key=operator.attrgetter('fitness'), reverse=False)
        if n == 1:
            return population[0]
        else:
            return population[0:n]

    def NormalizeFitness(self, population):
        sumFitness = 0
        for individual in population:
            sumFitness += individual.fitness
        for individual in population:
            individual.normalizedFitness = individual.fitness / sumFitness

    def recombine(self, parent1, parent2):
        """Recombine two parents using sub-tree crossover and return two children"""
        rand_id1 = random.randint(0, totalNumberOfNodes(parent1.height()) - 1)
        while parent1.isNodeNoneByID(rand_id1):
            rand_id1 = random.randint(0, totalNumberOfNodes(parent1.height()) - 1)
        rand_id2 = random.randint(0, totalNumberOfNodes(parent2.height()) - 1)
        while parent2.isNodeNoneByID(rand_id2):
            rand_id2 = random.randint(0, totalNumberOfNodes(parent2.height()) - 1)

        p1 = copy.deepcopy(parent1)
        p2 = copy.deepcopy(parent2)
        crossoverNode1 = p1.getNodeByID(rand_id1)
        crossoverNode2 = p2.getNodeByID(rand_id2)
        p1.setNodeByID(rand_id1, crossoverNode2)
        p2.setNodeByID(rand_id2, crossoverNode1)
        children = [p1, p2]
        return children

    def mutate(self, individual):
        """Apply sub-tree mutation"""
        rand = random.randint(0, totalNumberOfNodes(individual.height()) - 1)
        while individual.isNodeNoneByID(rand):
            rand = random.randint(0, totalNumberOfNodes(individual.height()) - 1)
        subTree = GPTree()
        subTree.makeTree()
        individual.setNodeByID(rand, subTree)

    def parentSelection(self, parents, nSelectedParents):
        """Select nSelectedParents from provided parents using specified method in config file and return them"""
        parents.sort(key=operator.attrgetter('fitness'), reverse=True)
        selectedParents = []
        selectedIndices = []
        while len(selectedParents) < nSelectedParents:
            rand = random.random()
            position = 0
            for idx, individual in enumerate(parents):
                position += individual.normalizedFitness
                if rand < position:
                    if idx not in selectedIndices:
                        selectedParents.append(individual)
                        selectedIndices.append(idx)
                    break

        return selectedParents

    def survivalSelection(self, population, nSurvivors):
        """Select nSurvivors from the population using specified method in config file and return them"""
        populationCpy = copy.deepcopy(population)
        selectedPopulation = []

        # tournament selection
        while len(selectedPopulation) < nSurvivors:
            randIndices = random.sample(range(len(populationCpy)), TOURNAMENT_SIZE)
            bestFitness = -1000  # very small number
            bestIndividual = populationCpy[0]
            for idx in randIndices:
                if bestFitness < populationCpy[idx].fitness:
                    bestIndividual = populationCpy[idx]
                    bestFitness = bestIndividual.fitness
                    bestIdx = idx
            selectedPopulation.append(bestIndividual)
            del populationCpy[bestIdx]
        return selectedPopulation

    def drawWorld(self, world, pacman, ghosts, config):
        pass

    def runExperiment(self):
        """Main method for running the experiment"""
        log = WriteToFile()
        log.writeHeaderToLog()
        log.writeResultsLabelToLog()
        globalBestPacman = GPTree()
        gen = 1
        for run in range(NUMBER_OF_RUNS):

            # create population
            pacmanPopulation = []
            for idx in range(POPULATION_SIZE):
                pacmanIndividual = GPTree()
                pacmanIndividual.makeTree()
                pacmanPopulation.append(pacmanIndividual)

            for eval in range(POPULATION_SIZE):
                (pills, pacmanSeq, ghostsSeq) = self.playGame(individual=pacmanPopulation[eval % POPULATION_SIZE])
            self.NormalizeFitness(pacmanPopulation)

            localBestPacman = GPTree()

            bestFitnees = self.findFittest(pacmanPopulation, 1).fitness
            avgFitness = self.averageFitness(pacmanPopulation)
            minFitness = self.findMInFitness(pacmanPopulation).fitness
            log.writeResultsToLog(gen, round(bestFitnees, 5), round(avgFitness, 5), round(minFitness, 5))

            while gen < NUMBER_OF_GENERATIONS - 1:
                gen += 1
                # Selecting parents with selection function
                selectedPacmanParents = self.parentSelection(pacmanPopulation, NUMBER_OF_OFFSPRINGS)
                pacmanOffspring = []

                for idx in range(int(NUMBER_OF_OFFSPRINGS / 2)):
                    pacmanChildren = self.recombine(selectedPacmanParents.pop(), selectedPacmanParents.pop())
                    for pacmanChild in pacmanChildren:
                        if random.random() < MUTATION_PROB:
                            self.mutate(pacmanChild)
                    pacmanOffspring.extend(pacmanChildren)

                random.shuffle(pacmanOffspring)
                for idx in range(len(pacmanOffspring)):
                    individual = pacmanOffspring[idx % len(pacmanOffspring)]
                    (candies, pacmanSeq, ghostsSeq) = self.playGame(individual=individual)
                    eval += 1
                    # finding best offspring
                    if localBestPacman.fitness < individual.fitness:
                        localBestPacman = copy.deepcopy(individual)
                        # saving number of candies eaten, and pacman location & ghosts locations
                        localHighestScoreGamePills = copy.deepcopy(candies)
                        localHighestScoreGamePacmanSeq = copy.deepcopy(pacmanSeq)
                        localHighestScoreGameGhostsSeq = copy.deepcopy(ghostsSeq)

                # adding best offspring to population
                pacmanPopulation.extend(pacmanOffspring)
                # normalize population fitness
                self.NormalizeFitness(pacmanPopulation)
                # survival selection - saving best individuals
                pacmanPopulation = self.survivalSelection(pacmanPopulation, POPULATION_SIZE)
                # normalize population fitness
                self.NormalizeFitness(pacmanPopulation)

                bestFitnees = self.findFittest(pacmanPopulation, 1).fitness
                avgFitness = self.averageFitness(pacmanPopulation)
                minFitness = self.findMInFitness(pacmanPopulation).fitness
                log.writeResultsToLog(gen, round(bestFitnees, 5), round(avgFitness, 5), round(minFitness, 5))
                # print("/n best fitnees: {}   avg fitness {}",format(bestFitnees,avgFitness))

            # updating global best pacman tree
            if globalBestPacman.fitness < localBestPacman.fitness:
                globalBestPacman = copy.deepcopy(localBestPacman)
                globalHighestScoreGamePills = localHighestScoreGamePills
                globalHighestScoreGamePacmanSeq = localHighestScoreGamePacmanSeq
                globalHighestScoreGameGhostsSeq = localHighestScoreGameGhostsSeq
            log.writeToSolutionLog(globalBestPacman)

        print("finish!")


if __name__ == "__main__":
    runs = []
    gPac = PacmanGP()
    gPac.runExperiment()