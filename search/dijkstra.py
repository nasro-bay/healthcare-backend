
# healthcare-navigation/search/dijkstra.py

import heapq
from search.base import BaseSearch
from search.node import Node

class DijkstraSearch(BaseSearch):
    """
    Dijkstra's Algorithm implementation.
    """
    def search(self) -> list:
        start_node = Node(self.problem.initial_osmid)
        
        # Priority queue entry: (g_cost, Node)
        frontier = [(start_node.g_cost, start_node)]
        
        # explored stores osmid -> best g_cost found so far
        explored = {}

        while frontier:
            current_g, current = heapq.heappop(frontier)
            
            if current.osmid in self.problem.goal_osmids:
                return current.path()
            
            if current.osmid in explored and explored[current.osmid] <= current_g:
                continue
            explored[current.osmid] = current_g
            
            for neighbor in self.problem.G[current.osmid]:
                edge_weight = self.problem.G[current.osmid][neighbor][0]['length']
                new_g = current_g + edge_weight
                
                if neighbor not in explored or new_g < explored[neighbor]:
                    child = Node(osmid=neighbor, g_cost=new_g, parent=current)
                    heapq.heappush(frontier, (new_g, child))
        return []
