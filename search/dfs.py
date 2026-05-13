
# healthcare-navigation/search/dfs.py

from search.base import BaseSearch
from search.node import Node

class DFSSearch(BaseSearch):
    """
    Depth-First Search implementation.
    """
    def search(self) -> list:
        start_node = Node(self.problem.initial_osmid)
        if start_node.osmid in self.problem.goal_osmids:
            return [start_node.osmid]

        frontier = [start_node]
        explored = {start_node.osmid}

        while frontier:
            current = frontier.pop()
            
            for neighbor in self.problem.G[current.osmid]:
                if neighbor not in explored:
                    edge_data = self.problem.G[current.osmid][neighbor][0]
                    child = Node(osmid=neighbor, g_cost=current.g_cost + edge_data['length'], parent=current)
                    
                    if neighbor in self.problem.goal_osmids:
                        return child.path()
                    
                    explored.add(neighbor)
                    frontier.append(child)
        return []
