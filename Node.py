import numpy as np
import random

class Node:
    
    def __init__(self,id):
        '''
        id: Node name
        '''

        self.id = id
        self.visited = False # Visited property for future algorithms
        self.level = 0 # Level property for future algorithms
        self.coordinate = np.array([random.random(),random.random()]) # Node coordinates on a plain
        self.neighbors = [] # Neighbors List
        self.edges =[] # Edges list
        self.degree = 0 # Degree value

    def addNeighbor(self,v): # Add a neighbor node to the list
        if not v in self.neighbors:
            self.neighbors.append(v)

    def addEdge(self,v): # Add an edge to the list
        if not v in self.neighbors:
            self.neighbors.append(v)


