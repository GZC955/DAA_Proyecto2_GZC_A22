from asyncio.windows_events import NULL
from Node import *
from Edge import *

class Graph:

    def __init__(self,directed,autocycles,graph_name):
        '''
        directed: True or False about the graph's direction
        autocycles: True or False about the autocycles on the graph existence
        graph_name: Created Graph's name
        '''
        self.name = graph_name
        self.nodes = {}
        self.edges = {}
        self.directed = False
        self.autocycles = False
        self.visited = False
    
    def addNode (self,name):
        '''
        Adding a new node to the node's graph dictionary
        name: New node name
        '''
        node = self.nodes.get(name)

        if node is None: # Check if the node already exists
            node = Node(name)
            self.nodes[name] = node # Add a new node

        return node

    def addEdge(self,name,node0,node1,weight):
        '''
        Adding a new edge to the edge's graph dictionary
        name: Edge name
        node0: source node
        node1: target node
        weight: Edge weight value if it is necessary
        '''
        ed = self.edges.get(name)
        
        if ed is None: # Check if the edge already exists
            n0 = self.addNode(node0)
            n1 = self.addNode(node1)
            ed = Edge(name,n0,n1,weight) # Creaating the edge object
            self.edges[name] = ed # Adding values to the edge dictionary

            n0.neighbors.append(n1) # Adding to each node their respective neigbors and edges list
            n1.neighbors.append(n0)

            n0.edges.append(ed)
            n1.edges.append(ed)

        return ed

    def getNode(self,name):
        '''
        Getting the Node as an object not just the name
        name: Node's name
        '''
        return self.nodes.get(name)

    def getDegree(self,node):
        '''
        Evaluate the quantity of neighbors on an specific node in the graph
        node: Node of interest name
        '''
        n = self.getNode(node)
        if n is None:
            return 0
        
        return len(n.neighbors)

    def getRandEdge(self):
        '''
        Get a random edge on the graph
        '''
        return random.choice(list(self.edges.values()))

    def printNodes(self):
        '''
        Printing the Graph nodes in console to verify functionality
        '''
        n = self.nodes.items()
        print(n)

    def printEdges(self):
        '''
        Printing the Graph edges in console to verify functionality
        '''
        e = self.edges.items()
        print(e)
    
    def toGVFormat(self):
        '''
        Create the GV file to show results on Gephi
        '''
        val = 'digraph '+ str(self.name) + ' {\n'
        for i in self.nodes.values():
            val += str(i.id) + ';'
        for e in self.edges.values():
            n0 = e.n0.id
            n1 = e.n1.id
            val += n0 + ' -> ' + n1 + ';\n'
        val += '}\n'
        with open ("./Graphs_Data/" + self.name +".gv","w") as gv:
          gv.write(val) 

    def BFS(self,s):
        '''
        Create the BFS tree graph starting at the node s
        s: Tree root node
        '''

        Tree_BFS = Graph(False,False,self.name + "_BFST") # Create the tree graph
        self.resetNodes() # Mark all nodes of the graph as unvisited
        
        L = {0:[s]} # Create the layers dictionary
        Tree_BFS.addNode(str(s)) # Adds the origin node chosen by the user to the tree
        k = 0 # Start the layer counter
        node = self.getNode(str(s)) # Take the node as an object
        node.visited = True # Mark it as visited

        while len(L[k]) != 0: # Check if the layer is empty
            L[k + 1] = [] # Create the next layer empty
            for i in range(len(L[k])): # Loop to evaluate each node in the layer 
                node = self.getNode(str(L[k][i]))  
                e = node.edges # Get neighbours from the edges
                for j in range(len(e)): # Loop to add the unvisited neigbors to the next layer
                    if e[j].n1.visited == False: 
                        e[j].n1.visited = True 
                        Tree_BFS.addNode(e[j].n1.id) 
                        Tree_BFS.addEdge(str(L[k][i])+" -> "+str(e[j].n1.id),str(L[k][i]),str(e[j].n1.id),NULL)
                        L[k + 1].append(e[j].n1.id)  # Add de node.id to the next layer

            k = k+1 # The layer counter pass to the next level

        print(L) 
        return Tree_BFS
    
    def resetNodes(self):
        '''
        Marks all the graph nodes as unvisited to start searchings
        '''
        n = len(self.nodes.items()) # Get the nodes quantity
        for i in range(n):
            node = self.getNode(str(i))  # Get nodes one by one
            node.visited = False  # Make the node as unvisited
    
    def DFS_R(self,s):
        '''
        Create the DFS tree graph starting at the node s by using the recursive algorithm
        s: Tree root node
        '''
        Tree_DFSR = Graph(False,False,self.name + "_DFSRT") # Create the tree graph
        self.resetNodes() # Mark all nodes of the graph as unvisited
        
        def DFRI(s2): # Define the internal function to be able to apply recursion
            node = self.getNode(str(s2)) # Take the root as an object
            node.visited = True # Mark it as visited
            Tree_DFSR.addNode(str(s2)) # Adds the root node to the tree
            e = node.edges # Get the root edges
            for i in range(len(e)): # For each edge evaluate if the neighbour is already visited
                if e[i].n1.visited == False: # If neighbour is not visited, add it to the tree and apply it the aboove steps
                    Tree_DFSR.addEdge(str(s2) + " -> " +str(e[i].n1.id),str(s2),str(e[i].n1.id),NULL)
                    DFRI(e[i].n1.id) # Apply the algorithm to the unvisited neighbour
                     

        DFRI(s) # Apply the recursive algorith startin with the node s chosen by the user    

        return Tree_DFSR
         
    def DFS_I(self,s):
        '''
        Create the DFS tree graph starting at the node s by using the iterative algorithm
        s: Tree root node
        '''
        Tree_DFSR = Graph(False,False,self.name + "_DFSIT") # Create the tree graph
        self.resetNodes() # Mark all nodes of the graph as unvisited
        S = [] # Create an empty stack to save the visited nodes
        S.append(self.getNode(str(s)).id) # Add the root node to the stack
        while len(S) != 0: # Executes the loop until there are no more connected nodes without visiting
            head = S.pop() # Take out the stack top
            node = self.getNode(str(head)) # Get the stack top as an object
            node.visited = True # Mark it as visited
            Tree_DFSR.addNode(node.id) # Add the stack top to the tree
            e = node.edges
            neis = list(map(lambda x : x.id ,node.neighbors)) # Get the stack top neighbors list 

            for i in range(len(e)): # Add the nodes to the stack if they were not in and have not been visited before. 
                if e[i].n1.id not in S and e[i].n1.visited == False:
                    S.append(e[i].n1.id)
                    Tree_DFSR.addEdge(node.id + " -> " + e[i].n1.id, node.id, e[i].n1.id,NULL)
        '''
        while len(S) != 0: # Executes the loop until there are no more connected nodes without visiting
            head = S.pop() # Take out the stack top
            node = self.getNode(str(head)) # Get the stack top as an object
            node.visited = True # Mark it as visited
            Tree_DFSR.addNode(node.id) # Add the stack top to the tree
            neis = list(map(lambda x : x.id ,node.neighbors)) # Get the stack top neighbors list 

            for i in range(len(neis)): # Add the nodes to the stack if they were not in and have not been visited before. 
                if neis[i] not in S and self.getNode(neis[i]).visited == False:
                    S.append(neis[i])
                    Tree_DFSR.addEdge(node.id + " -> " + self.getNode(neis[i]).id, node.id, self.getNode(neis[i]).id,NULL)
        '''

        return Tree_DFSR
