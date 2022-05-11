from asyncio.windows_events import NULL
from Node import *
from Graph import *
import random
import math


def dist(a,b):
    ''' 
    Apply distance between two nodes coordinates formula \n
    a: first node name \n
    b: second node name \n
    return: distance value between node a and b
    '''
    return math.sqrt((a.coordinate[0] - b.coordinate[0])**2 + (a.coordinate[1] - b.coordinate[1])**2)

def randomArray(s):
    '''
    Create an integers array from 1 to s in a random order \n
    s: maximun value in the array \n 
    return an array
    '''
    
    arr = np.array(random.randint(1,s)) # Create the first random value
    while arr.size < s: # Adding numbers untill we get the expected length without repeated values 
        a = random.randint(1,s)
        if a not in arr:
            arr= np.append(arr,a)
    return arr
   
def randomErdos(n,v,directed,autocycles,graph_name):
    ''' 
    Create a Graph by using the Erdos-Renyi method \n
    n: Desired nodes quantity \n
    v: Desired edges quantity \n
    directed: True or False about the graph's direction
    autocycles: True or False about the autocycles on the graph existence
    graph_name: Created Graph's name
    return: a random graph object
    '''

    g=Graph(directed,autocycles,graph_name) # Initializing the graph 

    for i in range(n-1): # Adding nodes one by one untill we get the desired quantity
        g.addNode(str(i))
    
    while len(list(g.edges.values())) < v: # Adding edges untill we get the desired quantity by conecting random source and targets
        s=random.randint(0,n-1)
        t=random.randint(0,n-1)
        if s != t:
            g.addEdge(str(s)+" -> "+str(t),str(s),str(t),NULL)
    
    return g

def randomGilbert(n,p,directed,autocycles,graph_name):
    ''' 
    Create a Graph by using the Gilbert method \n
    n: Desired nodes quantity \n
    p: Probability of creating an edge [0,1]  \n
    directed: True or False about the graph's direction
    autocycles: True or False about the autocycles on the graph existence
    graph_name: Created Graph's name
    return: a random graph object
    '''

    g=Graph(directed,autocycles,graph_name) # Initializing the graph

    for s in range(n):
        g.addNode(str(s)) # Adding source nodes
        for t in range(n):
            if random.random() < p: # Creating targets if we get the desired probability value 
                if (s != t):
                    g.addEdge(str(s) + " -> " +str(t),str(s),str(t),NULL)

    return g

def randomGeo(n,r,directed,autocycles,graph_name):
    ''' 
    Create a Graph by using the Geographic method \n
    n: Desired nodes quantity \n
    r: Maximum distance to conect a node [0,1]  \n
    directed: True or False about the graph's direction
    autocycles: True or False about the autocycles on the graph existence
    graph_name: Created Graph's name
    return: a random graph object
    '''

    g=Graph(directed,autocycles,graph_name) # Initializing the graph
    
    for i in range(n):
        node = g.addNode(str(i)) # Adding nodes and their random coordinates
        node.coordinate[0] = random.random()
        node.coordinate[1] = random.random()


    for i in range(n):
        for j in range(n): # Comparing every node with each other
            if i!=j:
                d = dist(g.getNode(str(i)),g.getNode(str(j))) # Creating an edge if two different nodes meet the distance
                if d <= r:
                    g.addEdge(str(i) + " -> " + str(j),str(i),str(j),NULL)

    return g

def randomGrid(m,n,diagonals,directed,autocycles,graph_name):
    ''' 
    Create a Graph by using the Geographic method \n
    m: Desired columns quantity \n
    n: Desired files quantity  \n
    diagonals: True or False about the graph's diagonals existence 
    directed: True or False about the graph's direction
    autocycles: True or False about the autocycles on the graph existence
    graph_name: Created Graph's name
    return: a random graph object
    '''
    if n == 0: # Case where user forgets the files number
        n=m
    
    m=max(2,m) # Minimal case is a square
    n=max(2,n)

    g=Graph(directed,autocycles,graph_name) # Initializing the graph 

    for i in range (m): 
        for j in range(n):
            node = g.addNode(str(i*n + j)) # Adding nodes and their coordinates
            node.coordinate[0] = float(i)
            node.coordinate[1] = float(j)

            if j < n-1: # Joining file nodes
                g.addEdge(str(i*n + j)+ " -> " + str(i*n + j + 1),str(i*n + j),str(i*n + j + 1),NULL)
            if i < m-1: # Joining columns
                g.addEdge(str(i*n + j)+ " -> " + str((i+1)*n + j),str(i*n + j),str((i+1)*n + j),NULL)
            if i < m-1 and j < n-1 and diagonals: # Joining diagonals
                g.addEdge(str(i*n + j)+ " -> " + str((i+1)*n + j + 1),str(i*n + j),str((i+1)*n + j + 1),NULL)
            if i > 0 and j < n-1 and diagonals:
                g.addEdge(str(i*n + j)+ " -> " + str((i-1)*n + j + 1),str(i*n + j),str((i-1)*n + j + 1),NULL)
    
    return g

def randomBarabasi(n,d,directed,autocycles,graph_name):
    ''' 
    Create a Graph by using the Barabasi-Albert method \n
    n: Desired nodes quantity \n
    d: Max degree allowed per node \n 
    directed: True or False about the graph's direction
    autocycles: True or False about the autocycles on the graph existence
    graph_name: Created Graph's name
    return: a random graph object
    '''
    g=Graph(directed,autocycles,graph_name) # Initializing the graph
    g.addNode(str(0)) # Adding the first node

    for i in range(1,n):
        randNodes = randomArray(i) # Array with the possible conections ordered in a random way
        for j in range(1,i):
            deg = g.getDegree(str(randNodes[j])) # Reading the possible source and target degree 
            deg2 = g.getDegree(str(i))
            p1 = 1 - deg/d # Getting the source and target probabilities
            p2 = 1 - deg2/d
            if random.random() < p1 and random.random() < p2: # Adding edges if both probabilities hold 
                if randNodes[j] != i:
                    g.addEdge(str(i) + " -> " + str(randNodes[j]), str(i), str(randNodes[j]),NULL)

    return g

def randomDoroMendes(n,directed,autocycles,graph_name):
    '''
    Create a Graph by using the Dorogovtov-Mendes method \n
    n: Desired nodes quantity \n
    directed: True or False about the graph's direction \n
    autocycles: True or False about the autocycles on the graph existence \n
    graph_name: Created Graph's name \n
    return: a random graph object
    '''    
    if int (n) >= 3: # Evaluating minimal nodes quantity
        g=Graph(directed,autocycles,graph_name) # Initializing the graph

        for i in range(0,2): # Creating firt triangle 
            g.addNode(str(i))
        
        g.addEdge(str(0) + " -> " + str(1), str(0), str(1),NULL)
        g.addEdge(str(1) + " -> " + str(2), str(1), str(2),NULL)
        g.addEdge(str(2) + " -> " + str(0), str(2), str(0),NULL)

        for i in range(3,int (n+1)): # Creating nodes and selecting random edges to connect
            g.addNode(str(i))
            e = g.getRandEdge()
            g.addEdge(str(i) + " -> " + str(e.n0.id), str(i), str(e.n0.id),NULL)
            
    else:
        print("Invalid nodes quantity")

    return g

