import numpy as np
import heapq

class HNSW:
    """
    A class implementing the HNSW (Hierarchical Navigable Small World) algorithm for efficient nearest neighbor search.

    This implementation supports adding vectors, searching for the nearest neighbors, and handling the graph structure
    used in HNSW. It supports both cosine and Euclidean distances for neighbor search.

    Attributes:
        M (int): The maximum number of neighbors for each node.
        ef_construction (int): The size of the dynamic list of candidates during index construction.
        ef_search (int): The size of the dynamic list of candidates during search.
        space (str): The distance metric to use for neighbor search. Can be "cosine" or "euclidean".
        graph (dict): A dictionary storing the graph where nodes are connected by edges (representing neighbors).
        vectors (dict): A dictionary storing the vectors associated with each node.
        entry_point (str or None): The entry point for the search, representing the starting node.
    """

    def __init__(self, M=16, ef_construction=200, ef_search=50, space="cosine"):
        """
        Initializes an HNSW index.

        Args:
            M (int): The maximum number of neighbors for each node. Defaults to 16.
            ef_construction (int): The size of the dynamic list of candidates during index construction. Defaults to 200.
            ef_search (int): The size of the dynamic list of candidates during search. Defaults to 50.
            space (str): The distance metric for neighbor search. Can be "cosine" or "euclidean". Defaults to "cosine".

        Returns:
            None
        """
        self.M = M
        self.ef_construction = ef_construction
        self.ef_search = ef_search
        self.space = space
        self.graph = {}
        self.vectors = {}
        self.entry_point = None

    def add(self, vector, node_id):
        """
        Adds a vector to the HNSW index and connects it to its neighbors.

        Args:
            vector (list or np.ndarray): The vector to add to the index.
            node_id (str): The unique identifier for the node.

        Returns:
            None
        """
        if len(self.graph) == 0:
            self.entry_point = node_id

        self.vectors[node_id] = vector
        self.graph[node_id] = []
        neighbors = self._search_neighbors(vector)
        self.graph[node_id].extend(neighbors)
        for neighbor in neighbors:
            self.graph[neighbor].append(node_id)

        # Truncate the neighbors to the maximum size M
        for node in self.graph:
            self.graph[node] = self.graph[node][:self.M]

    def _search_neighbors(self, query_vector):
        """
        Searches for the closest neighbors of the given query vector.

        Args:
            query_vector (list or np.ndarray): The query vector for which to find neighbors.

        Returns:
            list: A list of node ids representing the closest neighbors.
        """
        candidates = {self.entry_point}
        visited = set()
        neighbors = []
        while candidates:
            node = candidates.pop()
            visited.add(node)
            dist = self._distance(query_vector, self.vectors[node])
            if len(neighbors) < self.M:
                heapq.heappush(neighbors, (-dist, node))
            else:
                if dist < -neighbors[0][0]:
                    heapq.heapreplace(neighbors, (-dist, node))

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    candidates.add(neighbor)
        return [node for _, node in neighbors]

    def _distance(self, v1, v2):
        """
        Computes the distance between two vectors using the specified distance metric.

        Args:
            v1 (list or np.ndarray): The first vector.
            v2 (list or np.ndarray): The second vector.

        Returns:
            float: The distance between the two vectors.
        """
        if self.space == "cosine":
            return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        elif self.space == "euclidean":
            return np.linalg.norm(np.array(v1) - np.array(v2))

    def search(self, query_vector, k=2):
        """
        Searches for the top `k` nearest neighbors of the given query vector.

        Args:
            query_vector (list or np.ndarray): The query vector to search for.
            k (int): The number of nearest neighbors to return. Defaults to 2.

        Returns:
            list: A list of tuples containing the distance and node id of the top `k` nearest neighbors.
        """
        neighbors = self._search_neighbors(query_vector)
        distances = [(self._distance(query_vector, self.vectors[node]), node) for node in neighbors]
        distances.sort(key=lambda x: x[0])
        return distances[:k]
