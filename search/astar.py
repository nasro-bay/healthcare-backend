
# healthcare-navigation/search/astar.py

import heapq
from search.base import BaseSearch
from search.node import Node
from graph.utils import haversine_distance

class AStarSearch(BaseSearch):
    """
    A* Search implementation using a priority queue.
    """
    def search(self) -> list:
        start_node = Node(self.problem.initial_osmid)
        
        # Priority queue entry: (f_score, Node)
        # f_score = g_cost + heuristic
        h_start = self._lazy_heuristic(start_node.osmid)
        frontier = [(start_node.g_cost + h_start, start_node)]
        
        # explored stores osmid -> best g_cost found so far
        explored = {}

        while frontier:
            f_score, current = heapq.heappop(frontier)
            
            if current.osmid in self.problem.goal_osmids:
                return current.path()
            
            if current.osmid in explored and explored[current.osmid] <= current.g_cost:
                continue
            explored[current.osmid] = current.g_cost
            
            for neighbor in self.problem.G[current.osmid]:
                edge_weight = self.problem.G[current.osmid][neighbor][0]['length']
                new_g = current.g_cost + edge_weight
                
                if neighbor not in explored or new_g < explored[neighbor]:
                    child = Node(osmid=neighbor, g_cost=new_g, parent=current)
                    h = self._lazy_heuristic(neighbor)
                    heapq.heappush(frontier, (new_g + h, child))
        return []

    def _lazy_heuristic(self, node_osmid):
        """
        Computes the minimum haversine distance to any goal hospital.
        """
        node_data = self.problem.G.nodes[node_osmid]
        min_dist = float('inf')
        for goal_id in self.problem.goal_osmids:
            goal_data = self.problem.G.nodes[goal_id]
            dist = haversine_distance(node_data['y'], node_data['x'], goal_data['y'], goal_data['x'])
            if dist < min_dist:
                min_dist = dist
        return min_dist
