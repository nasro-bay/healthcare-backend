
# healthcare-navigation/tests/test_search.py

import unittest
import networkx as nx
from search.bfs import BFSSearch
from search.dfs import DFSSearch
from search.astar import AStarSearch
from search.dijkstra import DijkstraSearch

class MockProblem:
    def __init__(self, G, start, goals):
        self.G = G
        self.initial_osmid = start
        self.goal_osmids = goals

class TestSearchAlgorithms(unittest.TestCase):
    def setUp(self):
        # Create a simple line graph: 1 -> 2 -> 3 -> 4 -> 5
        self.G = nx.MultiDiGraph()
        for i in range(1, 5):
            self.G.add_node(i, y=36.0, x=2.0 + i*0.01)
            self.G.add_node(i+1, y=36.0, x=2.0 + (i+1)*0.01)
            self.G.add_edge(i, i+1, length=100.0)
        
        self.problem = MockProblem(self.G, 1, {5})

    def test_bfs(self):
        search = BFSSearch(self.problem)
        path = search.search()
        self.assertEqual(path, [1, 2, 3, 4, 5])

    def test_dijkstra(self):
        # Add a shortcut 1 -> 5 with length 500 (longer than 1-2-3-4-5 which is 400)
        self.G.add_edge(1, 5, length=500.0)
        search = DijkstraSearch(self.problem)
        path = search.search()
        self.assertEqual(path, [1, 2, 3, 4, 5]) # Should still pick the shorter path

if __name__ == "__main__":
    unittest.main()
