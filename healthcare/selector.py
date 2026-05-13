
# healthcare-navigation/healthcare/selector.py

from graph.utils import haversine_distance

def rank_hospitals(G, goal_osmids, initial_osmid):
    """
    Ranks hospitals based on straight-line distance.
    This acts as a placeholder for more complex ranking criteria.
    Args:
        G: Graph.
        goal_osmids: Set of goal integers.
        initial_osmid: Starting node integer.
    Returns:
        list: Sorted list of goal OSMIDs.
    """
    start_node = G.nodes[initial_osmid]
    
    ranked = []
    for goal_id in goal_osmids:
        goal_node = G.nodes[goal_id]
        dist = haversine_distance(start_node['y'], start_node['x'], goal_node['y'], goal_node['x'])
        ranked.append((dist, goal_id))
    
    ranked.sort()
    return [item[1] for item in ranked]
