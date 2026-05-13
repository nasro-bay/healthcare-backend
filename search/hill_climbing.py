
# healthcare-navigation/search/hill_climbing.py

from search.base import BaseSearch
from search.node import Node
from graph.utils import haversine_distance

class HillClimbingSearch(BaseSearch):
    """
    Hill Climbing (Greedy Local Search) implementation.
    Always moves to the neighbor closest to the goal.
    """
    def search(self) -> list:
        current_osmid = self.problem.initial_osmid
        start_node = Node(current_osmid)
        
        if current_osmid in self.problem.goal_osmids:
            return [current_osmid]

        path_nodes = [start_node]
        visited = {current_osmid}
        
        current = start_node
        
        # Max iterations to prevent infinite loops in cycles
        for _ in range(2000):
            self.nodes_visited += 1
            
            neighbors = list(self.problem.G[current.osmid])
            if not neighbors:
                break
                
            best_neighbor = None
            min_dist = float('inf')
            
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                    
                dist = self._heuristic(neighbor)
                if dist < min_dist:
                    min_dist = dist
                    best_neighbor = neighbor
            
            if best_neighbor is None:
                # Stuck in local optimum or dead end
                break
                
            edge_data = self.problem.G[current.osmid][best_neighbor][0]
            child = Node(osmid=best_neighbor, g_cost=current.g_cost + edge_data['length'], parent=current)
            
            current = child
            visited.add(current.osmid)
            
            if current.osmid in self.problem.goal_osmids:
                return current.path()
                
        return []

    def _heuristic(self, node_osmid):
        node_data = self.problem.G.nodes[node_osmid]
        min_h = float('inf')
        for goal_id in self.problem.goal_osmids:
            goal_data = self.problem.G.nodes[goal_id]
            h = haversine_distance(node_data['y'], node_data['x'], goal_data['y'], goal_data['x'])
            if h < min_h:
                min_h = h
        return min_h
