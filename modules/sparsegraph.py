import numpy as np

class SparseGraph:
    '''
    SparseGraph(n)

    Create graph with n vertices.
    '''
    def __init__(self, n):
        self.__edges = set()
        self.__n = n

    '''
    graph.vertices()

    Return iterator of all vertices.
    '''
    def vertices(self):
        return range(self.__n)

    '''
    graph.edges()

    Return iterator of all edges.
    '''
    def edges(self):
        return (edge for edge in self.__edges)

    '''
    graph.add_edge(u, v)

    Add edge (u, v) to graph. Throws if u == v or u and v are not vertices.
    '''
    def add_edge(self, u, v):
        if not self.__edge_valid((u, v)):
            raise Exception('invalid edge')
        if (u > v):
            u, v = v, u
        self.__edges.add((u, v))

    '''
    graph.remove_edge(u, v)

    Remove edge (u, v) from graph.
    '''
    def remove_edge(self, u, v):
        if (u > v):
            u, v = v, u
        self.__edges.remove((u, v))

    '''
    graph.clear_edges()

    Remove all edges from graph.
    '''
    def clear_edges(self):
        self.__edges.clear()

    '''
    graph.adjacency_matrix()

    Return numpy adjacency matrix, where element at index [u, v]
    of matrix is 1 if edge is in graph, else 0.
    '''
    def adjacency_matrix(self):
        matrix = np.zeros((self.__n, self.__n))
        for (u,v) in self.edges():
            matrix[(u, v)] = 1
            matrix[(v, u)] = 1
        return matrix

    '''
    graph.degree(vertex)

    Return degree of vertex.
    '''
    def degree(self, vertex):
        return sum(1 for i in range(self.__n) if (vertex, i) in self)

    '''
    x in graph

    Returns whether vertex (as number) or edge (as tuple of vertices)
    is in graph.
    '''
    def __contains__(self, value):
        try:
            return 0 <= value < self.__n
        except:
            try:
                (u, v) = value
                if (u > v):
                    u, v = v, u
                return (u, v) in self.__edges
            except:
                return False

    '''
    graph[(u, v)]

    Returns 1 if edge index = (u, v) is in graph, else 0.
    '''
    def __getitem__(self, index):
        (u, v) = index
        if (u > v):
            u, v = v, u
        if (u, v) in self.__edges:
            return 1
        return 0

    '''
    str(graph)

    Returns string representation of graph and its edges.
    '''
    def __str__(self):
        return 'Graph(n=' + str(self.__n) + ', ' + str(self.__edges) + ')'

    def __repr__(self):
        return str(self)

    def __edge_valid(self, edge):
        (u, v) = edge
        if u == v or u < 0 or u >= self.__n or v < 0 or v >= self.__n:
            return False
        return True
