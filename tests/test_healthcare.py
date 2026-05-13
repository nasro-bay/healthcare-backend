
# healthcare-navigation/tests/test_healthcare.py

import unittest
from unittest.mock import patch
from healthcare.problem import HealthcareProblem
import networkx as nx

class TestHealthcareLogic(unittest.TestCase):

    @patch('healthcare.problem.get_nearest_node')
    def test_problem_init_failure(self, mock_get_nearest):
        mock_get_nearest.return_value = 1
        G = nx.MultiDiGraph()
        G.add_node(1, y=36.0, x=2.0)
        G_proj = G # Mock
        
        # Goal ID 999 does not exist in graph
        with self.assertRaises(ValueError):
            HealthcareProblem((36.0, 2.0), [999], G, G_proj)

if __name__ == "__main__":
    unittest.main()
