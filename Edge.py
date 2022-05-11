class Edge:

    def __init__(self,name,source,target,weight):
        '''
        name: Edge name
        source: Source Node name
        target: Taget Node name
        weight: Edge weight value if it is necessary
        '''
        self.name = name
        self.n0 = source
        self.n1 = target
        self.weight = weight
        self.visited = False # Visited property for future algorithms
    
