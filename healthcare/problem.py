
# healthcare/problem.py

from graph.virtual_node import get_nearest_node
from search.bfs import BFSSearch
from search.dfs import DFSSearch
from search.astar import AStarSearch
from search.dijkstra import DijkstraSearch
from search.hill_climbing import HillClimbingSearch
from healthcare.hospitals import get_hospital_availability

class HealthcareProblem:
    def __init__(self, initial_coords, goal_osmids_list, G, G_projected):
        self.G = G
        self.G_projected = G_projected
        self.initial_osmid = get_nearest_node(initial_coords, G, G_projected)
        
        valid_goals = set()
        for gid in goal_osmids_list:
            if gid not in G.nodes:
                continue
            
            avail = get_hospital_availability(gid)
            if avail['status'] == "Open" and avail['capacity'] < 100:
                valid_goals.add(gid)
        
        self.goal_osmids = valid_goals
        if not self.goal_osmids:
            # Fallback: if all filtered goals are closed, include all for safety in routing
            self.goal_osmids = {gid for gid in goal_osmids_list if gid in G.nodes}
            if not self.goal_osmids:
                raise ValueError("No valid hospital IDs found in graph.")

    def solve(self, strategy: str) -> list:
        strategy_map = {
            "BFS": BFSSearch,
            "DFS": DFSSearch,
            "A_STAR": AStarSearch,
            "Dijkstra": DijkstraSearch,
            "HILL_CLIMBING": HillClimbingSearch
        }
        if strategy not in strategy_map:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        search_engine = strategy_map[strategy](self)
        return search_engine.search()
