
# healthcare-navigation/tests/test_graph.py

import unittest
import networkx as nx
from graph.utils import haversine_distance, cost

class TestGraphUtils(unittest.TestCase):
    def test_haversine(self):
        # Distance between school and a nearby point (approx)
        # 36.6886, 2.8662 to 36.6896, 2.8672
        dist = haversine_distance(36.6886, 2.8662, 36.6896, 2.8672)
        self.assertGreater(dist, 100)
        self.assertLess(dist, 200)

    def test_cost(self):
        # Create a mock graph
        G = nx.MultiDiGraph()
        G.add_edge(1, 2, length=10.5)
        G.add_edge(2, 3, length=20.0)
        
        route = [1, 2, 3]
        self.assertEqual(cost(G, route), 30.5)

if __name__ == "__main__":
    unittest.main()
