import numpy as np

class SparseGraph:

    def __init__(self, n):
        """
        Create graph with n vertices.
        """
        self.__edges = set()
        self.__n = n

    @property
    def n(self):
        """
        Returns number of vertices in graph.
        """
        return self.__n

    def vertices(self):
        """
        Returns iterator of all vertices.
        """
        return range(self.__n)

    def edges(self):
        """
        Return iterator of all edges.
        """
        return (edge for edge in self.__edges)

    def edges_count(self):
        """
        Return number |E| of all edges.
        """
        return len(self.__edges)

    def add_edge(self, u, v):
        """
        Add edge (u, v) to graph. Throws if u == v or u and v are not vertices.
        """
        if not self.__edge_valid((u, v)):
            raise Exception('invalid edge')
        if (u > v):
            u, v = v, u
        self.__edges.add((u, v))

    def remove_edge(self, u, v):
        """
        Remove edge (u, v) from graph.
        """
        if (u > v):
            u, v = v, u
        self.__edges.remove((u, v))

    def clear_edges(self):
        """
        Remove all edges from graph.
        """
        self.__edges.clear()

    def adjacency_matrix(self):
        """
        Return numpy adjacency matrix, where element at index [u, v]
        of matrix is 1 if edge is in graph, else 0.
        """
        matrix = np.zeros((self.__n, self.__n))
        for (u,v) in self.edges():
            matrix[(u, v)] = 1
            matrix[(v, u)] = 1
        return matrix

    def degree(self, vertex):
        """
        Return degree of vertex.
        """
        return sum(1 for i in range(self.__n) if (vertex, i) in self)

    def __contains__(self, value):
        """
        Returns whether vertex (as number) or edge (as tuple of vertices)
        is in graph.
        """
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

    def __getitem__(self, index):
        """
        Returns 1 if edge index = (u, v) is in graph, else 0. (graph[(u, v)])
        """
        (u, v) = index
        if (u > v):
            u, v = v, u
        if (u, v) in self.__edges:
            return 1
        return 0

    def __str__(self):
        """
        Returns string representation of graph and its edges.
        """
        return 'Graph(n=' + str(self.__n) + ', ' + str(self.__edges) + ')'

    def __repr__(self):
        return str(self)

    def __edge_valid(self, edge):
        (u, v) = edge
        if u == v or u < 0 or u >= self.__n or v < 0 or v >= self.__n:
            return False
        return True
